#!/usr/bin/env python3
"""Idea 51 — cash-secured put-writing forward PAPER book.

No free history of option prices exists, so idea 51 cannot be backtested; it has to be
run forward. This script is the book. It runs once a day, AFTER research/options_cache.py
has written today's snapshot into data/options/iv_panel.csv, and it:

  1. generates candidates from today's snapshot under the QUEUE idea-51 rules (binding),
  2. pulls the live option chain for each candidate and opens what fits the book,
  3. marks every open position to the current mid,
  4. settles positions whose expiry has passed (assignment marked at the expiry close),
  5. rewrites the three artefacts below.

Candidate rules (QUEUE idea 51, verbatim):
    (a) Deep Value triage score >= 5 (research/deepvalue/TRIAGE.md) AND a real quote in
        data/options/iv_panel.csv: iv_src != 'yahoo' and stale_days <= 2
    (b) cash-secured only, monthly expiry 30-45 DTE, strike 10-15% OTM
    (c) enter only when ATM IV - RV20 >= 8 vol points AND skew is positive
    (d) size so one full assignment is <= 10% of the book
    (e) costs = full bid-ask spread crossing (a seller is filled at the BID) + $0.65/contract

Book rules:
    $100,000 notional, cash-secured, <= 8 open positions, at most one per ticker,
    held to expiry. Candidates are ranked by IV-RV spread when there are more of them
    than there are free slots.

Outputs:
    research/backtests/putwrite_paper_positions.csv   one row per position
    research/backtests/putwrite_paper_daily.csv       one row per day
    research/backtests/PUTWRITE_PAPER.md              human-readable book + stats

Idempotent: re-running on the same date re-marks and rewrites but never opens a second
position for a date that has already been processed. Never fabricates a quote — a
contract with no two-sided quote is skipped and logged.

Run: .venv/bin/python research/putwrite_paper.py
"""
import datetime as dt
import math
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data" / "options" / "iv_panel.csv"
TRIAGE = ROOT / "research" / "deepvalue" / "TRIAGE.md"
OUTDIR = ROOT / "research" / "backtests"
POS_CSV = OUTDIR / "putwrite_paper_positions.csv"
DAY_CSV = OUTDIR / "putwrite_paper_daily.csv"
REPORT = OUTDIR / "PUTWRITE_PAPER.md"

# ---- binding parameters (idea 51) -------------------------------------------------
BOOK = 100_000.0        # notional book size
MAX_POS = 8             # max simultaneous open positions
MAX_POS_FRAC = 0.10     # one full assignment <= 10% of book
MIN_SCORE = 5           # triage score floor
MAX_STALE = 2.0         # stale_days ceiling for a "real" quote
DTE_LO, DTE_HI = 30, 45
OTM_LO, OTM_HI = 0.10, 0.15   # strike 10-15% below spot
MIN_IV_RV = 0.08        # 8 vol points
COMMISSION = 0.65       # $ per contract
MULT = 100              # shares per contract

POS_COLS = [
    "id", "status", "ticker", "triage_score", "entry_date", "expiry", "dte_at_entry",
    "spot_entry", "strike", "otm_pct", "open_interest", "bid", "ask", "mid",
    "contract_iv", "atm_iv", "rv20", "iv_rv_spread", "skew_5pct", "notional",
    "premium_gross", "commission", "premium_net", "mark_date", "mark_spot", "mark_mid",
    "unrealized_pnl", "exit_date", "exit_spot", "assigned", "realized_pnl",
]
DAY_COLS = [
    "date", "open_positions", "premium_collected", "marked_pnl", "realized_pnl",
    "unrealized_pnl", "equity", "max_drawdown", "notional_deployed", "candidates",
    "opened_today",
]

LOG = []


def log(msg):
    LOG.append(msg)
    print(f"  {msg}")


# ---------------------------------------------------------------- Black-Scholes IV
# Reused from research/options_cache.py: Yahoo's own impliedVolatility field is a
# failed-solve ladder and unusable, so we solve our own from the quote.
def _ndtr(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_put(S, K, T, r, sigma):
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * _ndtr(-d2) - S * _ndtr(-d1)


def put_iv(price, S, K, T, r):
    if not all(np.isfinite([price, S, K, T, r])) or price <= 0 or T <= 0:
        return np.nan
    lo, hi = 1e-4, 5.0
    if price <= bs_put(S, K, T, r, lo) or price >= bs_put(S, K, T, r, hi):
        return np.nan
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if bs_put(S, K, T, r, m) < price:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- inputs
def load_triage():
    """ticker -> best (highest) triage score from the markdown log."""
    if not TRIAGE.exists():
        return pd.DataFrame(columns=["ticker", "score"])
    rows = []
    for ln in TRIAGE.read_text().splitlines():
        if not ln.startswith("|"):
            continue
        p = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(p) < 7 or p[0].lower() == "date" or set(p[0]) <= set("-: "):
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", p[0]):
            continue
        try:
            score = float(p[5])
        except ValueError:
            continue
        rows.append({"ticker": p[1].strip().upper(), "score": score, "tdate": p[0]})
    t = pd.DataFrame(rows)
    if not len(t):
        return pd.DataFrame(columns=["ticker", "score"])
    return (t.sort_values(["ticker", "score"]).drop_duplicates("ticker", keep="last")
             [["ticker", "score"]].reset_index(drop=True))


def load_panel():
    if not PANEL.exists():
        return pd.DataFrame()
    d = pd.read_csv(PANEL)
    d["date"] = d["date"].astype(str)
    for c in ("atm_iv", "rv20", "skew_5pct", "stale_days", "spot", "dte", "iv_rv_spread"):
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    return d


def read_csv(path, cols):
    if path.exists():
        d = pd.read_csv(path)
        for c in cols:
            if c not in d.columns:
                d[c] = np.nan
        return d[cols]
    return pd.DataFrame(columns=cols)


# ---------------------------------------------------------------- candidates
def near_miss_probe(panel, triage, run_date, limit=8):
    """Diagnostic, run only when nothing qualifies: take the rows that pass every gate
    EXCEPT quote freshness and report whether a tradable strike even exists 10-15% OTM.
    Distinguishes 'the gates are binding' from 'this name has no quotes'."""
    global MAX_STALE
    keep = MAX_STALE
    try:
        MAX_STALE = float("inf")
        near, _ = candidates(panel, triage, run_date)
    finally:
        MAX_STALE = keep
    out = []
    for _, c in near.head(limit).iterrows():
        puts = get_puts(str(c["ticker"]), str(c["expiry"]))
        spot = float(c["spot"])
        lo, hi = spot * (1 - OTM_HI), spot * (1 - OTM_LO)
        if puts is None:
            out.append((str(c["ticker"]), float(c["stale_days"]), 0, 0))
            continue
        band = puts[(puts["strike"] >= lo) & (puts["strike"] <= hi)]
        quoted = int(((band["bid"] > 0) & (band["ask"] >= band["bid"])).sum())
        out.append((str(c["ticker"]), float(c["stale_days"]), len(band), quoted))
    return out


def candidates(panel, triage, run_date):
    """Rows of today's snapshot that pass every idea-51 entry rule. Returns
    (candidates_df, funnel_dict)."""
    snap = panel[panel["date"] == run_date].copy()
    funnel = {"snapshot rows": len(snap)}
    if not len(snap):
        return snap, funnel

    snap = snap.merge(triage, on="ticker", how="left")
    snap["score"] = pd.to_numeric(snap["score"], errors="coerce")

    steps = [
        ("triage score >= 5", snap["score"] >= MIN_SCORE),
        ("monthly, 30-45 DTE", (snap["dte"] >= DTE_LO) & (snap["dte"] <= DTE_HI)
                               & snap["is_monthly"].astype(str).str.lower().isin(["true", "1"])),
        ("iv_src != 'yahoo'", snap["iv_src"].astype(str).str.lower() != "yahoo"),
        ("ATM IV - RV20 >= 8 vp", (snap["atm_iv"] - snap["rv20"]) >= MIN_IV_RV),
        ("skew > 0", snap["skew_5pct"] > 0),
        # staleness applied last so the funnel shows how much of the loss is the
        # quote-freshness rule alone (it is the whole of it on a market holiday)
        (f"stale_days <= {MAX_STALE:g}", snap["stale_days"] <= MAX_STALE),
    ]
    cur = snap
    for name, mask in steps:
        cur = cur[mask.reindex(cur.index).fillna(False)]
        funnel[name] = len(cur)
    cur = cur.copy()
    cur["edge"] = cur["atm_iv"] - cur["rv20"]
    cur = cur.sort_values("edge", ascending=False).reset_index(drop=True)
    return cur, funnel


# ---------------------------------------------------------------- chain access
_CHAIN_CACHE = {}


def get_puts(ticker, expiry):
    """Live put chain for one ticker/expiry. None on any failure (logged by caller)."""
    key = (ticker, expiry)
    if key in _CHAIN_CACHE:
        return _CHAIN_CACHE[key]
    out = None
    try:
        ch = yf.Ticker(ticker).option_chain(expiry)
        p = getattr(ch, "puts", None)
        if p is not None and len(p):
            p = p.copy()
            for c in ("strike", "bid", "ask", "lastPrice", "openInterest", "impliedVolatility"):
                if c not in p.columns:
                    p[c] = np.nan
                p[c] = pd.to_numeric(p[c], errors="coerce")
            out = p
    except Exception as e:
        log(f"chain {ticker} {expiry}: {type(e).__name__}: {e}")
    _CHAIN_CACHE[key] = out
    return out


def pick_put(puts, spot):
    """Highest-open-interest put with strike 10-15% below spot and a real two-sided
    quote. Returns the row or None."""
    if puts is None or not len(puts):
        return None
    lo, hi = spot * (1 - OTM_HI), spot * (1 - OTM_LO)
    band = puts[(puts["strike"] >= lo) & (puts["strike"] <= hi)].copy()
    if not len(band):
        return None
    band = band[(band["bid"] > 0) & (band["ask"] >= band["bid"])]
    if not len(band):
        return None
    band["openInterest"] = band["openInterest"].fillna(0.0)
    return band.sort_values(["openInterest", "strike"], ascending=[False, False]).iloc[0]


def last_close(ticker, on_date):
    """Close on or immediately before `on_date` (used for expiry settlement)."""
    try:
        d = dt.date.fromisoformat(str(on_date))
        h = yf.Ticker(ticker).history(start=str(d - dt.timedelta(days=10)),
                                      end=str(d + dt.timedelta(days=1)),
                                      auto_adjust=False)["Close"].dropna()
        if len(h):
            return float(h.iloc[-1])
    except Exception as e:
        log(f"settle price {ticker} {on_date}: {type(e).__name__}")
    return np.nan


def spot_now(ticker, fallback=np.nan):
    try:
        v = float(yf.Ticker(ticker).fast_info["last_price"])
        if np.isfinite(v) and v > 0:
            return v
    except Exception:
        pass
    return fallback


# ---------------------------------------------------------------- book mechanics
def settle(pos, run_date):
    """Settle any open position whose expiry has passed. Mutates `pos` in place."""
    n = 0
    for i, row in pos[pos["status"] == "open"].iterrows():
        if str(row["expiry"]) >= run_date:
            continue
        px = last_close(row["ticker"], row["expiry"])
        if not np.isfinite(px):
            log(f"cannot settle {row['ticker']} {row['expiry']}: no close, left open")
            continue
        K, prem = float(row["strike"]), float(row["premium_net"])
        assigned = px < K
        realized = prem - (K - px) * MULT if assigned else prem
        for col, val in (("status", "expired"), ("exit_date", str(row["expiry"])),
                         ("exit_spot", round(px, 4)), ("assigned", str(bool(assigned))),
                         ("realized_pnl", round(realized, 2)), ("unrealized_pnl", 0.0)):
            pos.at[i, col] = val
        n += 1
        log(f"settled {row['ticker']} {K:g}P {row['expiry']}: spot {px:.2f} "
            f"{'ASSIGNED' if assigned else 'expired worthless'}, P&L ${realized:,.0f}")
    return n


def mark(pos, run_date):
    """Mark every open position to the current mid of its own contract."""
    for i, row in pos[pos["status"] == "open"].iterrows():
        puts = get_puts(row["ticker"], str(row["expiry"]))
        mid = np.nan
        if puts is not None:
            m = puts[np.isclose(puts["strike"].astype(float), float(row["strike"]))]
            if len(m):
                b, a = float(m["bid"].iloc[0]), float(m["ask"].iloc[0])
                if np.isfinite(b) and np.isfinite(a) and a >= b > 0:
                    mid = (a + b) / 2.0
                elif np.isfinite(m["lastPrice"].iloc[0]) and m["lastPrice"].iloc[0] > 0:
                    mid = float(m["lastPrice"].iloc[0])
        if not np.isfinite(mid):
            log(f"no mark for {row['ticker']} {row['strike']:g}P {row['expiry']}; "
                f"carrying previous mark")
            continue
        sp = spot_now(row["ticker"], float(row["spot_entry"]))
        for col, val in (("mark_date", run_date), ("mark_spot", round(sp, 4)),
                         ("mark_mid", round(mid, 4)),
                         ("unrealized_pnl",
                          round(float(row["premium_net"]) - mid * MULT, 2))):
            pos.at[i, col] = val


def open_new(pos, cands, run_date):
    """Open positions from today's candidates, respecting every book constraint."""
    opened = []
    already = set(pos.loc[pos["status"] == "open", "ticker"].astype(str))
    n_open = int((pos["status"] == "open").sum())
    deployed = float(pd.to_numeric(pos.loc[pos["status"] == "open", "notional"],
                                   errors="coerce").fillna(0).sum())
    max_notional = BOOK * MAX_POS_FRAC

    for _, c in cands.iterrows():
        if n_open >= MAX_POS:
            log(f"book full at {MAX_POS} positions; {c['ticker']} not opened")
            break
        t = str(c["ticker"])
        if t in already:
            log(f"{t}: already open, skipped (one position per ticker)")
            continue
        spot = float(c["spot"])
        if not (np.isfinite(spot) and spot > 0):
            log(f"{t}: no spot in snapshot, skipped")
            continue
        puts = get_puts(t, str(c["expiry"]))
        if puts is None:
            log(f"{t} {c['expiry']}: chain missing, skipped")
            continue
        row = pick_put(puts, spot)
        if row is None:
            log(f"{t} {c['expiry']}: no two-sided quote 10-15% OTM, skipped")
            continue
        K = float(row["strike"])
        notional = K * MULT
        if notional > max_notional:
            log(f"{t}: {K:g} strike is ${notional:,.0f} notional > "
                f"{MAX_POS_FRAC:.0%} of book, skipped")
            continue
        if deployed + notional > BOOK:
            log(f"{t}: ${notional:,.0f} would exceed cash-secured book, skipped")
            continue
        bid, ask = float(row["bid"]), float(row["ask"])
        mid = (bid + ask) / 2.0
        gross = bid * MULT                     # fill at the BID: seller crosses the spread
        net = gross - COMMISSION
        if net <= 0:
            log(f"{t}: bid ${bid:.2f} does not cover commission, skipped")
            continue
        T = max(int(c["dte"]), 1) / 365.25
        r = float(c["r"]) if np.isfinite(pd.to_numeric(c.get("r"), errors="coerce")) else 0.04
        civ = put_iv(mid, spot, K, T, r)
        pos.loc[len(pos)] = {
            "id": f"{t}_{c['expiry']}_{K:g}_{run_date}", "status": "open", "ticker": t,
            "triage_score": float(c["score"]), "entry_date": run_date,
            "expiry": str(c["expiry"]), "dte_at_entry": int(c["dte"]),
            "spot_entry": round(spot, 4), "strike": K,
            "otm_pct": round(100 * (1 - K / spot), 2),
            "open_interest": float(row["openInterest"]), "bid": round(bid, 4),
            "ask": round(ask, 4), "mid": round(mid, 4),
            "contract_iv": round(civ, 6) if np.isfinite(civ) else np.nan,
            "atm_iv": round(float(c["atm_iv"]), 6), "rv20": round(float(c["rv20"]), 6),
            "iv_rv_spread": round(float(c["atm_iv"]) - float(c["rv20"]), 6),
            "skew_5pct": round(float(c["skew_5pct"]), 6), "notional": notional,
            "premium_gross": round(gross, 2), "commission": COMMISSION,
            "premium_net": round(net, 2), "mark_date": run_date,
            "mark_spot": round(spot, 4), "mark_mid": round(mid, 4),
            "unrealized_pnl": round(net - mid * MULT, 2), "exit_date": "",
            "exit_spot": np.nan, "assigned": "", "realized_pnl": np.nan,
        }
        opened.append(dict(ticker=t, strike=K, expiry=str(c["expiry"]), bid=bid,
                           notional=notional, premium_net=net))
        already.add(t)
        n_open += 1
        deployed += notional
        log(f"OPENED {t} {K:g}P {c['expiry']} @ bid ${bid:.2f} "
            f"(net ${net:,.0f}, notional ${notional:,.0f}, OI {row['openInterest']:.0f})")
    return opened


# ---------------------------------------------------------------- reporting
def score_bucket(s):
    if not np.isfinite(s):
        return "no triage"
    if s <= 2:
        return "0-2"
    if s <= 4:
        return "3-4"
    if s <= 6:
        return "5-6"
    return "7-8"


BUCKET_ORDER = ["0-2", "3-4", "5-6", "7-8", "no triage"]


def iv_rv_by_score(panel, triage):
    """Cross-sectional median IV-RV spread by triage score bucket, over every
    30-45 DTE monthly row in the panel with a usable, non-Yahoo IV."""
    d = panel.copy()
    d = d[(d["dte"] >= DTE_LO) & (d["dte"] <= DTE_HI)]
    d = d[d["is_monthly"].astype(str).str.lower().isin(["true", "1"])]
    d = d[d["iv_src"].astype(str).str.lower().isin(["mid", "last", "mixed"])]
    d = d.dropna(subset=["atm_iv", "rv20"])
    if not len(d):
        return pd.DataFrame(), np.nan, 0
    d = d.merge(triage, on="ticker", how="left")
    d["score"] = pd.to_numeric(d["score"], errors="coerce")
    d["edge"] = d["atm_iv"] - d["rv20"]
    d["bucket"] = d["score"].apply(score_bucket)
    g = d.groupby("bucket").agg(
        n=("edge", "size"), tickers=("ticker", "nunique"),
        med_iv=("atm_iv", "median"), med_rv=("rv20", "median"),
        med_edge=("edge", "median"),
        pct_edge_ge8=("edge", lambda s: 100.0 * (s >= MIN_IV_RV).mean()),
        pct_skew_pos=("skew_5pct", lambda s: 100.0 * (s > 0).mean()),
    ).reindex([b for b in BUCKET_ORDER if b in set(d["bucket"])])
    scored = d.dropna(subset=["score"])
    rho = np.nan
    if len(scored) > 5 and scored["score"].nunique() > 1:
        rho = float(scored["score"].corr(scored["edge"], method="spearman"))
    return g, rho, int(len(scored))


def write_report(pos, daily, funnel, bucket, rho, n_scored, run_date, opened,
                 probe=()):
    p = pos.copy()
    for c in ("premium_net", "realized_pnl", "unrealized_pnl", "notional", "strike",
              "bid", "mark_mid", "iv_rv_spread"):
        p[c] = pd.to_numeric(p[c], errors="coerce")
    op = p[p["status"] == "open"]
    cl = p[p["status"] == "expired"]
    prem = float(p["premium_net"].sum())
    real = float(cl["realized_pnl"].sum())
    unre = float(op["unrealized_pnl"].sum())
    last = daily.iloc[-1] if len(daily) else None
    mdd = float(last["max_drawdown"]) if last is not None else 0.0
    days = int(daily["date"].nunique()) if len(daily) else 0

    L = []
    L.append("# Idea 51 — cash-secured put-writing, forward paper book")
    L.append("")
    L.append(f"Generated {run_date} by `research/putwrite_paper.py` from the "
             f"`data/options/iv_panel.csv` snapshot of the same date. "
             f"Book ${BOOK:,.0f} notional, cash-secured, max {MAX_POS} positions, "
             f"one per ticker, held to expiry. Entries filled at the **bid** "
             f"(seller crosses the spread) less ${COMMISSION:.2f}/contract.")
    L.append("")
    L.append(f"**Day {days} of the >= 60 trading days idea 51 requires before a verdict.** "
             "Nothing here is a result yet.")
    L.append("")
    L.append("## Cumulative")
    L.append("")
    L.append("| Stat | Value |")
    L.append("|---|---|")
    L.append(f"| Trading days recorded | {days} |")
    L.append(f"| Positions opened, all time | {len(p)} |")
    L.append(f"| Open now | {len(op)} |")
    L.append(f"| Expired | {len(cl)} |")
    L.append(f"| Assigned | {int((cl['assigned'].astype(str).str.lower()=='true').sum())} |")
    L.append(f"| Premium collected (net of commission) | ${prem:,.2f} |")
    L.append(f"| Realized P&L | ${real:,.2f} |")
    L.append(f"| Unrealized (open marked to mid) | ${unre:,.2f} |")
    L.append(f"| Marked P&L (realized + unrealized) | ${real+unre:,.2f} |")
    L.append(f"| Max drawdown of marked equity | ${mdd:,.2f} |")
    L.append(f"| Notional deployed | ${float(op['notional'].sum()):,.0f} "
             f"of ${BOOK:,.0f} |")
    L.append("")

    L.append("## Current book")
    L.append("")
    if len(op):
        L.append("| Ticker | Score | Strike | Expiry | OTM% | Entry | Bid | Net premium "
                 "| Notional | Mark | Unrealized |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for _, r in op.sort_values("expiry").iterrows():
            L.append(f"| {r['ticker']} | {r['triage_score']:g} | {r['strike']:g} | "
                     f"{r['expiry']} | {r['otm_pct']:.1f}% | {r['entry_date']} | "
                     f"${r['bid']:.2f} | ${r['premium_net']:,.2f} | "
                     f"${r['notional']:,.0f} | ${r['mark_mid']:.2f} | "
                     f"${r['unrealized_pnl']:,.2f} |")
    else:
        L.append("_No open positions._")
    L.append("")

    if len(cl):
        L.append("## Closed")
        L.append("")
        L.append("| Ticker | Strike | Expiry | Spot at expiry | Assigned | Net premium | P&L |")
        L.append("|---|---|---|---|---|---|---|")
        for _, r in cl.sort_values("exit_date").iterrows():
            L.append(f"| {r['ticker']} | {r['strike']:g} | {r['expiry']} | "
                     f"${r['exit_spot']:.2f} | {r['assigned']} | "
                     f"${r['premium_net']:,.2f} | ${r['realized_pnl']:,.2f} |")
        L.append("")

    L.append(f"## Candidate funnel, {run_date}")
    L.append("")
    L.append("| Gate | Rows surviving |")
    L.append("|---|---|")
    for k, v in funnel.items():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append(f"Opened today: {len(opened)}"
             + (" — " + ", ".join(f"{o['ticker']} {o['strike']:g}P {o['expiry']}"
                                  for o in opened) if opened else "."))
    L.append("")
    if len(probe):
        L.append("Nothing qualified, so the rows that pass every gate **except** quote "
                 "freshness were probed against the live chain:")
        L.append("")
        L.append("| Ticker | stale_days | Strikes 10-15% OTM | With a two-sided quote |")
        L.append("|---|---|---|---|")
        for t, st, nb, nq in probe:
            L.append(f"| {t} | {st:.1f} | {nb} | {nq} |")
        L.append("")

    L.append("## Does 'reads well' predict overpriced puts?")
    L.append("")
    L.append("Cross-section of every 30-45 DTE monthly row in `iv_panel.csv` with a "
             "non-Yahoo IV, bucketed by Deep Value triage score. Positive IV-RV means "
             "the option market charges more vol than the stock has recently realised.")
    L.append("")
    if len(bucket):
        L.append("| Triage score | Rows | Tickers | Median ATM IV | Median RV20 | "
                 "Median IV-RV | % with IV-RV >= 8vp | % skew > 0 |")
        L.append("|---|---|---|---|---|---|---|---|")
        for b, r in bucket.iterrows():
            L.append(f"| {b} | {int(r['n'])} | {int(r['tickers'])} | "
                     f"{100*r['med_iv']:.1f} | {100*r['med_rv']:.1f} | "
                     f"{100*r['med_edge']:+.1f} | {r['pct_edge_ge8']:.0f}% | "
                     f"{r['pct_skew_pos']:.0f}% |")
        L.append("")
        L.append(f"Spearman rho(triage score, IV-RV spread) = "
                 f"{'n/a' if not np.isfinite(rho) else f'{rho:+.3f}'} "
                 f"over {n_scored} scored rows. Units are vol points.")
    else:
        L.append("_Not enough panel rows yet._")
    L.append("")

    L.append("## Daily series")
    L.append("")
    L.append("`research/backtests/putwrite_paper_daily.csv`; positions in "
             "`research/backtests/putwrite_paper_positions.csv`.")
    if len(daily):
        L.append("")
        tail = daily.tail(10)
        L.append("| Date | Open | Premium to date | Marked P&L | Realized | Max DD |")
        L.append("|---|---|---|---|---|---|")
        for _, r in tail.iterrows():
            L.append(f"| {r['date']} | {int(r['open_positions'])} | "
                     f"${float(r['premium_collected']):,.2f} | "
                     f"${float(r['marked_pnl']):,.2f} | "
                     f"${float(r['realized_pnl']):,.2f} | "
                     f"${float(r['max_drawdown']):,.2f} |")
    L.append("")
    if LOG:
        L.append("## Log")
        L.append("")
        for m in LOG[:40]:
            L.append(f"- {m}")
        if len(LOG) > 40:
            L.append(f"- ... {len(LOG)-40} more")
        L.append("")
    REPORT.write_text("\n".join(L) + "\n")


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    panel = load_panel()
    if not len(panel):
        print("no data/options/iv_panel.csv — run research/options_cache.py first")
        return 1
    triage = load_triage()
    today = str(dt.date.today())
    run_date = today if today in set(panel["date"]) else str(panel["date"].max())
    print(f"putwrite_paper {run_date}: panel {len(panel)} rows over "
          f"{panel['date'].nunique()} days; triage {len(triage)} tickers "
          f"({int((triage['score']>=MIN_SCORE).sum())} at score >= {MIN_SCORE})")
    if run_date != today:
        log(f"no snapshot for {today}; using latest panel date {run_date}")

    pos = read_csv(POS_CSV, POS_COLS)
    daily = read_csv(DAY_CSV, DAY_COLS)
    already_ran = run_date in set(daily["date"].astype(str))
    if already_ran:
        log(f"{run_date} already in the daily file — re-marking only, no new entries")

    settle(pos, run_date)

    cands, funnel = candidates(panel, triage, run_date)
    print(f"  candidates: {len(cands)} " +
          (", ".join(f"{r.ticker}({r.edge*100:.0f}vp)" for r in cands.itertuples())
           if len(cands) else "(none pass the idea-51 gates)"))
    for k, v in funnel.items():
        print(f"    {k:<24} {v}")

    probe = []
    if not len(cands):
        probe = near_miss_probe(panel, triage, run_date)
        for t, st, nb, nq in probe:
            log(f"near miss {t}: stale_days {st:.1f}, {nb} strike(s) 10-15% OTM, "
                f"{nq} two-sided")

    opened = [] if already_ran else open_new(pos, cands, run_date)
    mark(pos, run_date)

    # --- daily row
    p = pos.copy()
    for c in ("premium_net", "realized_pnl", "unrealized_pnl", "notional"):
        p[c] = pd.to_numeric(p[c], errors="coerce")
    op = p[p["status"] == "open"]
    real = float(p.loc[p["status"] == "expired", "realized_pnl"].sum())
    unre = float(op["unrealized_pnl"].sum())
    row = {
        "date": run_date, "open_positions": len(op),
        "premium_collected": round(float(p["premium_net"].sum()), 2),
        "marked_pnl": round(real + unre, 2), "realized_pnl": round(real, 2),
        "unrealized_pnl": round(unre, 2), "equity": round(real + unre, 2),
        "max_drawdown": 0.0,
        "notional_deployed": round(float(op["notional"].sum()), 2),
        "candidates": len(cands), "opened_today": len(opened),
    }
    daily = daily[daily["date"].astype(str) != run_date]
    daily = pd.concat([daily, pd.DataFrame([row])], ignore_index=True)
    daily["date"] = daily["date"].astype(str)
    daily = daily.sort_values("date").reset_index(drop=True)
    eq = pd.to_numeric(daily["equity"], errors="coerce").fillna(0.0)
    daily["max_drawdown"] = (eq - eq.cummax()).cummin().round(2)

    pos.to_csv(POS_CSV, index=False)
    daily.to_csv(DAY_CSV, index=False)
    bucket, rho, n_scored = iv_rv_by_score(panel, triage)
    write_report(pos, daily, funnel, bucket, rho, n_scored, run_date, opened, probe)

    print(f"  book: {len(op)} open, {int((p['status']=='expired').sum())} expired, "
          f"premium ${float(p['premium_net'].sum()):,.2f}, marked P&L "
          f"${real+unre:,.2f}, maxDD ${float(daily['max_drawdown'].iloc[-1]):,.2f}")
    if len(bucket):
        print("  IV-RV by triage bucket (vol points): " +
              ", ".join(f"{b}:{100*r['med_edge']:+.1f}(n={int(r['n'])})"
                        for b, r in bucket.iterrows()) +
              f"; rho={'n/a' if not np.isfinite(rho) else f'{rho:+.3f}'}")
    print(f"  wrote {POS_CSV.name}, {DAY_CSV.name}, {REPORT.name} in {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
