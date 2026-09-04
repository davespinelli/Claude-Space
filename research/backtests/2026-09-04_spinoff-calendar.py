#!/usr/bin/env python3
"""Idea 36 — spin-off calendar, first-pass event study (2026-09-04).

Hypothesis (Cusatis-Miles-Woolridge 1993): shares of spun-off subsidiaries beat the
market over the 6-24 months after the distribution, because index funds and the
parent's shareholders dump a small, unfamiliar, uncovered stock in the first weeks.

Design, fixed before any result was read:
Two arms, both fully reported, screen fixed before any number was read:
  ALL         every 10-12B registrant whose ticker resolves to prices
  INVESTABLE  + listed on NYSE/Nasdaq, entry close >= $5, and 20d median dollar
              volume at entry >= $1m. Form 10-12B is NOT a synonym for "spin-off":
              a large minority of these registrants are shell / blank-check
              distributions, and they are what the ALL arm's headline number is.

  event date  = the security's FIRST TRADED DAY (from prices, not from filings —
                the CERT/8-K dates in data/spinoffs.csv lead the listing by weeks)
  entry       = close of first_trade_day + ENTRY_LAG (30) trading days
  hold        = HOLD (252) trading days, equal weight across whatever is live
  benchmark   = IWM (the brief's choice; SPY reported alongside)
  costs       = 10 bps on entry and on exit, per PROTOCOL rule 2
  empty days  = cash at 0% (the portfolio is only invested ~X% of days; reported)

Calendar-time portfolio: on each day, equal weight over all positions currently in
their holding window. This is the standard construction for staggered events and it
does NOT let a crowded year dominate a thin one the way event-time averaging does.

Ticker-recycling guard: a spin-off's ticker is often reused later (or was used before)
by an unrelated company. A ticker is only accepted when its price history BEGINS
within [-60d, +730d] of the 10-12B filing date. This is what keeps e.g. a 2025
registrant from inheriting a decade of some other issuer's prices.

Run: .venv/bin/python research/backtests/2026-09-04_spinoff-calendar.py
"""
import sys, datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[2]
SPINOFFS = ROOT / "data" / "spinoffs.csv"
PRICES = ROOT / "research" / "backtests" / ".spinoff_prices.csv"   # local cache
VOLUME = ROOT / "research" / "backtests" / ".spinoff_volume.csv"

ENTRY_LAG = 30        # trading days after first trade
HOLD = 252            # trading days held
COST = 0.0010         # 10 bps each way
BENCH = ["IWM", "SPY"]
PRE_WINDOW = 60       # price history may begin up to 60d BEFORE the 10-12B (when-issued)
POST_WINDOW = 730     # ... and up to 730d after; outside that the ticker is not this issuer
MIN_PRICE_DAYS = ENTRY_LAG + 21   # need at least the lag plus a month to be usable
MIN_PX = 5.0                      # investable arm: entry close
MIN_ADV = 1_000_000.0             # investable arm: 20d median dollar volume at entry

np.random.seed(0)


# ---------------------------------------------------------------- stats
def ann_stats(r):
    """r: daily simple returns. -> CAGR, Sharpe, MaxDD, vol."""
    r = pd.Series(r).dropna()
    if len(r) < 2:
        return dict(cagr=np.nan, sharpe=np.nan, maxdd=np.nan, vol=np.nan, n=len(r))
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = r.std() * np.sqrt(252)
    return dict(cagr=cagr, sharpe=(r.mean() * 252) / vol if vol > 0 else np.nan,
                maxdd=(eq / eq.cummax() - 1).min(), vol=vol, n=len(r))


def line(label, s):
    print(f"  {label:<34} CAGR {s['cagr']:>7.1%}  Sharpe {s['sharpe']:>6.2f}  "
          f"MaxDD {s['maxdd']:>7.1%}  vol {s['vol']:>6.1%}  n={s['n']}")


# ---------------------------------------------------------------- data
def load_prices(tickers, start):
    have = None
    if PRICES.exists() and VOLUME.exists():
        have = (pd.read_csv(PRICES, index_col=0, parse_dates=True),
                pd.read_csv(VOLUME, index_col=0, parse_dates=True))
        if not [t for t in tickers if t not in have[0].columns]:
            return have
    missing = [t for t in tickers if have is None or t not in have[0].columns]
    print(f"  downloading {len(missing)} tickers from yfinance ...")
    cf, vf = [], []
    for i in range(0, len(missing), 40):
        chunk = missing[i:i + 40]
        d = yf.download(chunk, start=start, auto_adjust=True, progress=False,
                        threads=True, group_by="column")
        c, v = d["Close"], d["Volume"]
        if isinstance(c, pd.Series):
            c, v = c.to_frame(chunk[0]), v.to_frame(chunk[0])
        cf.append(c); vf.append(v)
    px = pd.concat(cf, axis=1) if cf else pd.DataFrame()
    vo = pd.concat(vf, axis=1) if vf else pd.DataFrame()
    if have is not None:
        px, vo = have[0].join(px, how="outer"), have[1].join(vo, how="outer")
    px = px.loc[:, ~px.columns.duplicated()].dropna(how="all")
    vo = vo.loc[:, ~vo.columns.duplicated()].reindex(px.index)
    px.round(4).to_csv(PRICES); vo.round(0).to_csv(VOLUME)
    return px, vo


def main():
    if not SPINOFFS.exists():
        print("data/spinoffs.csv missing — run research/spinoffs.py first")
        return 1
    sp = pd.read_csv(SPINOFFS)
    sp["ticker"] = sp["ticker"].fillna("").astype(str).str.strip().str.upper()
    sp = sp[(sp["ticker"] != "") & (sp["ticker"].str.len() <= 5)]
    sp["filing_dt"] = pd.to_datetime(sp["filing_date"], errors="coerce")
    sp = sp.dropna(subset=["filing_dt"]).drop_duplicates(subset=["ticker"], keep="first")
    print(f"spin-off event study — {len(sp)} 10-12B registrants with a ticker\n")

    tickers = sorted(sp["ticker"])
    px, vol = load_prices(tickers + BENCH, start="2014-06-01")

    # ---- resolve each event to a usable price series -------------------------
    events, dropped = [], {"no_prices": [], "wrong_issuer": [], "too_short": [], "no_window": []}
    for _, row in sp.iterrows():
        t = row["ticker"]
        if t not in px.columns:
            dropped["no_prices"].append(t); continue
        s = px[t].dropna()
        if len(s) == 0:
            dropped["no_prices"].append(t); continue
        first = s.index[0]
        lo = row["filing_dt"] - pd.Timedelta(days=PRE_WINDOW)
        hi = row["filing_dt"] + pd.Timedelta(days=POST_WINDOW)
        if not (lo <= first <= hi):
            dropped["wrong_issuer"].append(f"{t}({first.date()} vs filing {row['filing_dt'].date()})")
            continue
        if len(s) < MIN_PRICE_DAYS:
            dropped["too_short"].append(t); continue
        events.append(dict(ticker=t, name=row["name"], filing_date=row["filing_dt"],
                           exchange=str(row.get("exchange", "") or ""), first_trade=first,
                           series=s))

    print(f"  usable events: {len(events)}")
    for k, v in dropped.items():
        if v:
            print(f"  dropped [{k}]: {len(v)} -> {', '.join(map(str, v[:12]))}"
                  f"{' ...' if len(v) > 12 else ''}")

    # ---- per-event returns ---------------------------------------------------
    cal = px.index                       # common trading calendar
    bench_r = {b: px[b].reindex(cal).ffill().pct_change() for b in BENCH}
    recs, daily = [], {}
    for e in events:
        s = e["series"]
        if len(s) <= ENTRY_LAG + 1:
            continue
        entry_day = s.index[ENTRY_LAG]
        seg = s.iloc[ENTRY_LAG:ENTRY_LAG + HOLD + 1]
        if len(seg) < 2:
            continue
        r = seg.pct_change().dropna()
        truncated = len(seg) < HOLD + 1
        r.iloc[0] -= COST
        r.iloc[-1] -= COST
        daily[e["ticker"]] = r

        # investability, measured at the entry bar only (no look-ahead)
        entry_px = float(s.iloc[ENTRY_LAG])
        v = vol[e["ticker"]].reindex(s.index[:ENTRY_LAG + 1]).tail(20) if e["ticker"] in vol.columns \
            else pd.Series(dtype=float)
        adv = float((v * s.reindex(v.index)).median()) if len(v.dropna()) else np.nan
        listed = e["exchange"].strip().lower() in ("nyse", "nasdaq")
        inv = bool(listed and entry_px >= MIN_PX and np.isfinite(adv) and adv >= MIN_ADV)

        tot = float((1 + r).prod() - 1)
        exc = {}
        for b in BENCH:
            br = bench_r[b].reindex(r.index).fillna(0)
            exc[b] = tot - float((1 + br).prod() - 1)
        recs.append(dict(ticker=e["ticker"], name=e["name"], first_trade=e["first_trade"].date(),
                         entry=entry_day.date(), exit=r.index[-1].date(), days=len(r),
                         exchange=e["exchange"], entry_px=round(entry_px, 2),
                         adv20=round(adv, 0) if np.isfinite(adv) else np.nan, investable=inv,
                         truncated=truncated, ret=tot,
                         **{f"exc_{b}": exc[b] for b in BENCH}, year=e["first_trade"].year))
    ev = pd.DataFrame(recs)
    if not len(ev):
        print("no events survived"); return 1
    print(f"  investable (NYSE/Nasdaq, >= ${MIN_PX:.0f}, >= ${MIN_ADV/1e6:.0f}m ADV20 at entry): "
          f"{int(ev['investable'].sum())} of {len(ev)}")

    # ---- portfolios ----------------------------------------------------------
    def portfolio(names, drift):
        """Calendar-time book over `names`.
        drift=False: equal weight, rebalanced daily (Fama calendar-time convention).
        drift=True : equal dollars at each event's own entry, weights drift after."""
        R = pd.DataFrame({t: daily[t] for t in names if t in daily}).reindex(cal)
        act = R.notna().sum(axis=1)
        if drift:
            v = R.notna().astype(float)                # 1.0 on the day a position is live
            v = v.where(v > 0).mul(0)                  # placeholder, filled below
            vals = pd.DataFrame(0.0, index=R.index, columns=R.columns)
            prev = pd.Series(0.0, index=R.columns)
            rets = []
            for d in R.index:
                row = R.loc[d]
                live = row.notna()
                new = live & (prev == 0)
                base = prev.copy()
                base[new] = 1.0                        # inject $1 at entry
                tot0 = base[live].sum()
                grown = base[live] * (1 + row[live])
                rets.append((grown.sum() / tot0 - 1) if tot0 > 0 else 0.0)
                nxt = pd.Series(0.0, index=R.columns)
                nxt[live] = grown
                prev = nxt
            p = pd.Series(rets, index=R.index)
        else:
            p = R.mean(axis=1).fillna(0.0)
        span = p.index[act > 0]
        if not len(span):
            return None, None
        p = p.loc[span[0]:span[-1]]
        return p, act.loc[p.index]

    arms = [("ALL", list(daily.keys())),
            ("INVESTABLE", list(ev.loc[ev["investable"], "ticker"]))]
    for arm, names in arms:
        for drift, tag in [(False, "daily-EW"), (True, "drift")]:
            p, act = portfolio(names, drift)
            if p is None:
                continue
            if not drift:
                print(f"\n=== {arm} calendar-time portfolio, n={len(names)} events "
                      f"({p.index[0].date()} .. {p.index[-1].date()}) ===")
                print(f"  positions: mean {act.mean():.1f}, median {int(act.median())}, "
                      f"max {int(act.max())}; invested {float((act>0).mean()):.0%} of days")
            line(f"{arm} {tag}", ann_stats(p))
            if drift:
                for b in BENCH:
                    line(f"  {b} buy & hold (same window)", ann_stats(bench_r[b].loc[p.index]))
                mid = p.index[len(p) // 2]
                for lbl, sl in [("H1", p.loc[:mid]), ("H2", p.loc[mid:])]:
                    line(f"  {lbl} {sl.index[0].date()}..{sl.index[-1].date()}", ann_stats(sl))
                    for b in BENCH:
                        line(f"    {b}", ann_stats(bench_r[b].loc[sl.index]))

    # ---- event-level hit rate ------------------------------------------------
    for arm, sub in [("ALL", ev), ("INVESTABLE", ev[ev["investable"]])]:
        print(f"\n=== {arm}: per-event 12-month holds (n={len(sub)}) ===")
        for b in BENCH:
            c = f"exc_{b}"
            x = sub[c]
            t = x.mean() / (x.std() / np.sqrt(len(x))) if x.std() > 0 else np.nan
            print(f"  vs {b}: hit rate {(x>0).mean():.1%}  mean excess {x.mean():+.1%}  "
                  f"median {x.median():+.1%}  t {t:+.2f}  [worst {x.min():+.0%}, best {x.max():+.0%}]")
        # log-return t-test: the arithmetic mean is meaningless under this skew
        lr = np.log1p(sub["ret"].clip(lower=-0.999))
        print(f"  raw 12m return: mean {sub['ret'].mean():+.1%}, median {sub['ret'].median():+.1%}, "
              f"{(sub['ret']>0).mean():.0%} positive; mean log return {lr.mean():+.3f} "
              f"(t {lr.mean()/(lr.std()/np.sqrt(len(lr))):+.2f})")
        print(f"  truncated (delisted/acquired before 252d): {int(sub['truncated'].sum())}")

    inv = ev[ev["investable"]]
    print("\n  INVESTABLE by first-trade year (median excess vs IWM):")
    for y, r in inv.groupby("year").agg(n=("ret", "size"), med=("exc_IWM", "median"),
                                        hit=("exc_IWM", lambda x: (x > 0).mean())).iterrows():
        print(f"    {y}  n={int(r['n']):>3}  median excess {r['med']:+7.1%}  hit {r['hit']:.0%}")

    print("\n  INVESTABLE best 6 / worst 6 by excess vs IWM:")
    for lbl, g in [("best", inv.nlargest(6, "exc_IWM")), ("worst", inv.nsmallest(6, "exc_IWM"))]:
        for _, r in g.iterrows():
            print(f"    {lbl:>5} {r['ticker']:<6} {str(r['name'])[:32]:<32} "
                  f"{r['entry']} ret {r['ret']:+7.1%} exc {r['exc_IWM']:+7.1%}")

    # ---- robustness: how much of this is one name? ---------------------------
    print("\n=== INVESTABLE robustness ===")
    base, _ = portfolio(list(inv["ticker"]), False)
    bs = ann_stats(base)
    line("all 105", bs)
    for k in (1, 3, 5):
        drop = set(inv.nlargest(k, "ret")["ticker"])
        p2, _ = portfolio([t for t in inv["ticker"] if t not in drop], False)
        line(f"ex top-{k} by return ({','.join(sorted(drop))})"[:34], ann_stats(p2))
    for k in (1, 3):
        drop = set(inv.nsmallest(k, "ret")["ticker"])
        p2, _ = portfolio([t for t in inv["ticker"] if t not in drop], False)
        line(f"ex worst-{k} ({','.join(sorted(drop))})"[:34], ann_stats(p2))
    x = inv["exc_IWM"]
    print(f"  trimmed mean excess vs IWM (10% each tail): "
          f"{x.sort_values().iloc[len(x)//10:len(x)-len(x)//10].mean():+.1%}")
    print(f"  sign test on excess vs IWM: {int((x>0).sum())}/{len(x)} positive, "
          f"binomial p(one-sided) ~ "
          f"{1 - __import__('math').fsum(__import__('math').comb(len(x), i) * 0.5**len(x) for i in range(int((x>0).sum()))):.3f}")

    out = ROOT / "research" / "backtests" / "2026-09-04_spinoff-calendar.events.csv"
    ev.sort_values("entry").to_csv(out, index=False)
    print(f"\n  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
