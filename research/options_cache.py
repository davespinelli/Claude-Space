#!/usr/bin/env python3
"""Idea 35 — daily options implied-vol snapshot cache.

No free source of historical option-chain data exists, so this builds one forward from
today. For every ticker in research/universe.json (crypto excluded — no listed options)
plus the top 40 rows of research/deepvalue/candidates.csv, it pulls the yfinance option
chain for the two nearest *monthly* (third-Friday) expiries and records, per ticker per
expiry per day:

    spot, ATM call IV, ATM put IV, ATM IV, 25-delta-ish skew proxy
    (IV of the ~5% OTM put minus IV of the ~5% OTM call), put/call open-interest ratio,
    total OI, days to expiry, realised 20d vol and the IV-RV spread.

Outputs (both long format, one row per date x ticker x expiry):
    data/options/iv_YYYY-MM-DD.csv   today's snapshot (append + dedupe if re-run)
    data/options/iv_panel.csv        the full history, deduped on (date,ticker,expiry)

Run: .venv/bin/python research/options_cache.py
Runtime target < 10 min; ~100 tickers at 8 threads finishes in about a minute.
"""
import json, sys, math, time, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "options"
N_EXPIRIES = 2          # two nearest monthlies
N_CANDIDATES = 40       # top 40 deep-value candidates
MIN_DTE = 3             # skip anything expiring within 3 days (IVs go haywire into expiry)
OTM = 0.05              # skew proxy: 5% OTM put vs 5% OTM call
MAX_WORKERS = 8
IV_LO, IV_HI = 0.01, 5.0  # plausibility band for any IV we keep
MAX_REL_SPREAD = 1.0      # reject a quote whose bid-ask spread exceeds its own mid
DEFAULT_R = 0.04          # fallback risk-free rate if ^IRX is unavailable

KEY = ["date", "ticker", "expiry"]
COLS = ["date", "ticker", "expiry", "dte", "is_monthly", "spot", "atm_call_iv", "atm_put_iv",
        "atm_iv", "skew_5pct", "put_oi", "call_oi", "total_oi", "pc_oi_ratio",
        "rv20", "iv_rv_spread", "n_calls", "n_puts", "n_quoted", "iv_src", "stale_days",
        "r", "asof"]


# ---------------------------------------------------------------- Black-Scholes
# Yahoo's impliedVolatility field is unusable. Its solver bails out and reports a
# value on the ladder 0.0625 * 2**-k (observed 2026-09-04: every ATM call in the
# universe tagged at exactly 0.125009 pre-open and 0.250007 mid-session; SPY's whole
# September chain on the ladder at 10:00 ET). Free Yahoo option data also carries no
# bid/ask at all for many of the most liquid names -- SPY, AAPL and NVDA were all
# bid = ask = 0 across every strike during regular hours.
#
# So we solve our own Black-Scholes IV, preferring in order:
#   "mid"   bid-ask midpoint, when a two-sided quote exists      (best)
#   "last"  lastPrice, which is a real trade but may be stale    (usually available)
#   "yahoo" Yahoo's own field, only when it is not a ladder value (last resort)
# `iv_src` and `stale_days` are written to every row so a future study can drop
# whatever it does not trust.
def _ndtr(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(S, K, T, r, sigma, call=True):
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return max(0.0, (S - K) if call else (K - S))
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if call:
        return S * _ndtr(d1) - K * math.exp(-r * T) * _ndtr(d2)
    return K * math.exp(-r * T) * _ndtr(-d2) - S * _ndtr(-d1)


def bs_iv(price, S, K, T, r, call=True):
    """Bisection on [1e-4, 5]. Returns nan if the price is outside the no-arbitrage band."""
    if not all(map(np.isfinite, (price, S, K, T, r))) or price <= 0 or T <= 0:
        return np.nan
    lo, hi = 1e-4, 5.0
    if price <= bs_price(S, K, T, r, lo, call) or price >= bs_price(S, K, T, r, hi, call):
        return np.nan
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if bs_price(S, K, T, r, mid, call) < price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def is_ladder(v):
    """True for Yahoo's failed-solve sentinel values (0.0625 * 2**-k + 1e-5, and 1e-5)."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return True
    if not np.isfinite(v):
        return True
    if abs(v) < 2e-5:                  # the 1e-5 sentinel
        return True
    for k in range(-6, 16):            # 4.0, 2.0, 1.0, ... 0.125, 0.0625, ... ~1e-6
        lad = 0.0625 * 2.0 ** -k
        if abs(v - lad) < max(3e-5, 1e-4 * lad):   # float32 round-trip needs a relative band
            return True
    return False


# ---------------------------------------------------------------- ticker universe
def universe_tickers():
    u = json.loads((ROOT / "research" / "universe.json").read_text())
    eq = sorted({t for g in u.values() for t in g if not t.endswith("-USD")})
    cand = []
    p = ROOT / "research" / "deepvalue" / "candidates.csv"
    if p.exists():
        c = pd.read_csv(p)
        if "score" in c.columns:
            c = c.sort_values("score", ascending=False)
        cand = [str(t).strip().upper() for t in c["ticker"].head(N_CANDIDATES).dropna()]
    return sorted(set(eq) | set(cand)), eq, cand


# ---------------------------------------------------------------- expiry selection
def is_third_friday(d: dt.date) -> bool:
    return d.weekday() == 4 and 15 <= d.day <= 21


def pick_expiries(exp_strings, today):
    """Two nearest third-Friday monthlies with dte >= MIN_DTE.
    Falls back to the nearest ordinary expiries when a name lists no monthlies."""
    parsed = []
    for s in exp_strings:
        try:
            d = dt.date.fromisoformat(s)
        except Exception:
            continue
        dte = (d - today).days
        if dte >= MIN_DTE:
            parsed.append((s, d, dte))
    parsed.sort(key=lambda x: x[2])
    monthly = [p for p in parsed if is_third_friday(p[1])]
    out = [(s, dte, True) for s, _, dte in monthly[:N_EXPIRIES]]
    if len(out) < N_EXPIRIES:                       # pad with whatever is listed
        have = {s for s, _, _ in out}
        for s, _, dte in parsed:
            if s not in have:
                out.append((s, dte, False))
            if len(out) == N_EXPIRIES:
                break
    return out


# ---------------------------------------------------------------- IV extraction
def clean(df, S, T, r, call):
    """Normalise a call/put table and attach a trustworthy `iv` column.

    iv comes from our own bisection on the bid-ask mid where a two-sided quote
    exists (`iv_src` = "mid"); otherwise from Yahoo's field, but only when it is
    not one of its failed-solve ladder values (`iv_src` = "yahoo")."""
    if df is None or len(df) == 0:
        return None
    d = df.copy()
    for c in ("strike", "impliedVolatility", "openInterest", "bid", "ask", "lastPrice", "volume"):
        if c not in d.columns:
            d[c] = np.nan
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[d["strike"] > 0].copy()
    if not len(d):
        return None

    if "lastTradeDate" in d.columns:
        age = (pd.Timestamp.now(tz="UTC") - pd.to_datetime(d["lastTradeDate"], utc=True,
                                                           errors="coerce")).dt.total_seconds() / 86400
    else:
        age = pd.Series(np.nan, index=d.index)
    d["age_days"] = age

    bid, ask = d["bid"].fillna(0.0), d["ask"].fillna(0.0)
    two_sided = (bid > 0) & (ask > 0) & (ask >= bid)
    mid = (bid + ask) / 2.0
    with np.errstate(invalid="ignore", divide="ignore"):
        tight = two_sided & (((ask - bid) / mid.replace(0, np.nan)) <= MAX_REL_SPREAD)
    d["quoted"] = tight.fillna(False)

    ok = lambda x: isinstance(x, float) and np.isfinite(x) and IV_LO < x < IV_HI
    ivs, srcs = [], []
    for K, m, q, lp, yv in zip(d["strike"], mid, d["quoted"], d["lastPrice"],
                               d["impliedVolatility"]):
        v, src = np.nan, ""
        if q:
            v, src = bs_iv(float(m), S, float(K), T, r, call), "mid"
        if not ok(v) and np.isfinite(lp) and lp > 0:
            v, src = bs_iv(float(lp), S, float(K), T, r, call), "last"
        if not ok(v):
            v, src = (float(yv), "yahoo") if not is_ladder(yv) else (np.nan, "")
        if not ok(v):
            v, src = np.nan, ""
        ivs.append(v); srcs.append(src)
    d["iv"], d["iv_src"] = ivs, srcs
    return d


def iv_at(df, target):
    """IV interpolated across strike at `target`. Returns nan when no usable quotes."""
    if df is None:
        return np.nan
    d = df.dropna(subset=["strike", "iv"]).sort_values("strike")
    if len(d) == 0:
        return np.nan
    if len(d) == 1:
        return float(d["iv"].iloc[0])
    k = d["strike"].to_numpy(float)
    v = d["iv"].to_numpy(float)
    if target < k[0] or target > k[-1]:             # outside the quoted strip -> nearest
        return float(v[int(np.argmin(np.abs(k - target)))])
    return float(np.interp(target, k, v))


def oi_sum(df):
    if df is None:
        return 0.0
    return float(pd.to_numeric(df["openInterest"], errors="coerce").fillna(0).sum())


# ---------------------------------------------------------------- per-ticker worker
def snapshot(ticker, today, spot_hint, rv20, r):
    rows, note = [], ""
    try:
        tk = yf.Ticker(ticker)
        exps = tk.options or []
    except Exception as e:
        return rows, f"{ticker}: options list failed ({type(e).__name__})"
    if not exps:
        return rows, f"{ticker}: no listed options"
    picks = pick_expiries(exps, today)
    if not picks:
        return rows, f"{ticker}: no expiry beyond {MIN_DTE}d"

    spot = float(spot_hint) if spot_hint == spot_hint else np.nan
    if not (np.isfinite(spot) and spot > 0):
        try:
            spot = float(tk.fast_info["last_price"])
        except Exception:
            spot = np.nan
    if not (np.isfinite(spot) and spot > 0):
        return rows, f"{ticker}: no spot"

    for exp, dte, monthly in picks:
        try:
            ch = tk.option_chain(exp)
        except Exception as e:
            note = f"{ticker} {exp}: chain failed ({type(e).__name__})"
            continue
        T = max(dte, 1) / 365.25
        calls = clean(getattr(ch, "calls", None), spot, T, r, True)
        puts = clean(getattr(ch, "puts", None), spot, T, r, False)
        if calls is None and puts is None:
            continue

        c_iv, p_iv = iv_at(calls, spot), iv_at(puts, spot)
        atm = np.nan if (np.isnan(c_iv) and np.isnan(p_iv)) else float(np.nanmean([c_iv, p_iv]))
        otm_put = iv_at(puts, spot * (1 - OTM))
        otm_call = iv_at(calls, spot * (1 + OTM))
        skew = np.nan if (np.isnan(otm_put) or np.isnan(otm_call)) else otm_put - otm_call
        coi, poi = oi_sum(calls), oi_sum(puts)
        used = pd.concat([df[df["iv"].notna()] for df in (calls, puts) if df is not None]) \
            if any(df is not None for df in (calls, puts)) else pd.DataFrame()
        srcs = [x for x in used.get("iv_src", pd.Series(dtype=str)) if x]
        stale = used["age_days"].median() if len(used) and "age_days" in used else np.nan
        rows.append(dict(
            date=str(today), ticker=ticker, expiry=exp, dte=dte, is_monthly=bool(monthly),
            spot=round(spot, 4),
            atm_call_iv=_r(c_iv), atm_put_iv=_r(p_iv), atm_iv=_r(atm), skew_5pct=_r(skew),
            put_oi=poi, call_oi=coi, total_oi=poi + coi,
            pc_oi_ratio=_r(poi / coi) if coi > 0 else np.nan,
            rv20=_r(rv20),
            iv_rv_spread=np.nan if (np.isnan(atm) or np.isnan(rv20)) else _r(atm - rv20),
            n_calls=0 if calls is None else int(len(calls)),
            n_puts=0 if puts is None else int(len(puts)),
            n_quoted=int(sum(int(df["quoted"].sum()) for df in (calls, puts) if df is not None)),
            iv_src=(sorted(set(srcs))[0] if len(set(srcs)) == 1 else "mixed") if srcs else "none",
            stale_days=_r(stale, 2),
            r=round(r, 5),
            asof=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    if not rows and not note:
        note = f"{ticker}: chains empty"
    return rows, note


def _r(x, n=6):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return np.nan
    return np.nan if math.isnan(x) else round(x, n)


# ---------------------------------------------------------------- spot + realised vol
def risk_free():
    """13-week T-bill (^IRX) as the discount rate for the IV solve."""
    try:
        h = yf.Ticker("^IRX").history(period="10d")["Close"].dropna()
        if len(h):
            v = float(h.iloc[-1]) / 100.0
            if 0.0 <= v < 0.25:
                return v
    except Exception:
        pass
    return DEFAULT_R


def spots_and_rv(tickers):
    """One batched download for last close and annualised 20d realised vol."""
    spot, rv = {}, {}
    try:
        px = yf.download(tickers, period="3mo", auto_adjust=True, progress=False, threads=True)["Close"]
        if isinstance(px, pd.Series):
            px = px.to_frame(tickers[0])
        for t in px.columns:
            s = px[t].dropna()
            if len(s):
                spot[t] = float(s.iloc[-1])
            if len(s) >= 21:
                rv[t] = float(s.pct_change().iloc[-20:].std() * np.sqrt(252))
    except Exception as e:
        print(f"  ! batched price download failed: {type(e).__name__}: {e}", file=sys.stderr)
    return spot, rv


# ---------------------------------------------------------------- io
def merge_write(path, new):
    old = pd.read_csv(path) if path.exists() else None
    df = pd.concat([old, new], ignore_index=True) if old is not None and len(old) else new
    for c in COLS:
        if c not in df.columns:
            df[c] = np.nan
    df = df[COLS]
    df["date"] = df["date"].astype(str)
    df = (df.sort_values(KEY + ["asof"])
            .drop_duplicates(subset=KEY, keep="last")
            .sort_values(KEY).reset_index(drop=True))
    df.to_csv(path, index=False)
    return df


def main():
    t0 = time.time()
    tickers, eq, cand = universe_tickers()
    today = dt.date.today()
    print(f"options_cache {today}: {len(tickers)} tickers "
          f"({len(eq)} universe ex-crypto + {len(cand)} candidates, {len(set(eq) & set(cand))} overlap)")

    spot, rv = spots_and_rv(tickers)
    r = risk_free()
    print(f"  prices: spot for {len(spot)}/{len(tickers)}, rv20 for {len(rv)}; r={r:.3%}")

    rows, notes = [], []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        for got, n in ex.map(lambda t: snapshot(t, today, spot.get(t, np.nan),
                                                rv.get(t, np.nan), r), tickers):
            rows.extend(got)
            if n:
                notes.append(n)

    if not rows:
        print("  no chains retrieved — nothing written")
        return 1
    new = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    day = merge_write(OUT / f"iv_{today}.csv", new)
    panel = merge_write(OUT / "iv_panel.csv", new)

    covered = sorted(new["ticker"].unique())
    missing = [t for t in tickers if t not in set(covered)]
    both = new.groupby("ticker")["expiry"].nunique()
    print(f"  chains: {len(covered)}/{len(tickers)} tickers "
          f"({(both >= 2).sum()} with 2 expiries, {(both == 1).sum()} with 1); {len(new)} rows")
    print(f"  atm_iv present on {new['atm_iv'].notna().sum()}/{len(new)} rows; "
          f"skew on {new['skew_5pct'].notna().sum()}; pc_oi on {new['pc_oi_ratio'].notna().sum()}")
    print(f"  iv_src: {new['iv_src'].value_counts().to_dict()}; "
          f"rows with >=1 two-sided quote: {(new['n_quoted'] > 0).sum()}")
    print(f"  median quote age of contracts used: {new['stale_days'].median():.2f} days")
    if (new["iv_src"] == "none").mean() > 0.3:
        print("  WARNING: over 30% of rows have no usable IV at all.")
    if missing:
        print(f"  no options: {', '.join(missing)}")
    for n in notes[:15]:
        print(f"  note: {n}")
    if len(notes) > 15:
        print(f"  ... {len(notes)-15} more notes")
    print(f"  wrote data/options/iv_{today}.csv ({len(day)} rows) and "
          f"data/options/iv_panel.csv ({len(panel)} rows, "
          f"{panel['date'].nunique()} days) in {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
