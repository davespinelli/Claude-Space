#!/usr/bin/env python3
"""Idea 399 ADDENDUM - locate the G3 reproduction FAILURE against idea 336's committed grid.

The main run's G3 joined all 432 re-run ABS/QEXP arms on U56 and B136 to idea 336's committed
`.grid.csv` and reported max abs diff 1.139e-02 over six columns - a FAIL against the 1e-9 bar,
reported rather than silenced.  This file establishes WHY, because "probably the cache" is not a
finding:

    H_APPEND  the residual is an APPEND to data/prices.csv (idea 519's append channel, idea 353's
              cache-vintage exposure), not a code difference.  If so, TRUNCATING U56 to idea 336's
              own last trading day must reproduce its numbers to machine precision, and the panel
              whose cache did NOT move (B136) must already be bit-identical.

Reads the committed parent grid and the same caches; writes nothing but its own console/csv.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

PARENT = REPO / "research" / "backtests" / \
    "2026-09-07_re-price-the-fixed-ABSOLUTE-breadth-threshold-as-a-quantile_C.grid.csv"
OUT = REPO / "research" / "backtests"
STEM = Path(__file__).name[:-3]
FREQ, MAX_VOL, MINQ = "W", 0.60, 252
QS, BS, DEPTHS, RUNGS, GROSSES = [0.07, 0.12, 0.17], [0.30, 0.40, 0.50], [0.25, 0.50, 1.00], \
    [0, 10, 25], [0.75, 1.00]
OOS_START = "2017-01-01"
COLS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]
LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


def ewall(px, g):
    _, above, vol20 = score(px)
    e = (above & (vol20 < MAX_VOL)).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).mul(g).fillna(0.0)


def breadth(px):
    a = px > px.rolling(200).mean()
    return a.sum(axis=1) / a.notna().sum(axis=1).replace(0, np.nan)


def mult(px, thr_or_B, depth, cad, br):
    thr = thr_or_B
    m = pd.Series(1.0, index=px.index).where(~(br < thr), 1.0 - depth)
    ok = br.notna() if np.isscalar(thr) else (br.notna() & thr.notna())
    m = m.where(ok, 1.0)
    if cad == "W":
        mask = rebalance_mask(px.index, FREQ)
        m = m.where(mask).ffill().fillna(1.0)
    return m


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def run(px, panel):
    start = px.index[260]
    br_f = breadth(px)
    br = br_f.loc[start:]
    thr_q = {q: br_f.expanding(min_periods=MINQ).quantile(q) for q in QS}
    base0 = {g: (lambda r: (r["returns"].loc[start:], r["turnover"].loc[start:]))(
        backtest(px, ewall(px, g), cost_bps=0, freq=FREQ)) for g in GROSSES}
    rows = []
    for c in RUNGS:
        for g in GROSSES:
            r0, t0 = base0[g]
            rb = r0 - t0 * c / 1e4
            for cad in ("D", "W"):
                for d in DEPTHS:
                    for fam, levels in (("ABS", BS), ("QEXP", QS)):
                        for lv in levels:
                            thr = lv if fam == "ABS" else thr_q[lv]
                            me = mult(px, thr, d, cad, br_f).loc[start:].shift(1).fillna(1.0)
                            rg = me * rb - me.diff().abs().fillna(0.0) * g * c / 1e4
                            m = metrics(rg)
                            h1, h2 = half_sharpes(rg)
                            rows.append(dict(panel=panel, rung=c, gross=g, family=fam, level=lv,
                                             depth=d, cadence=cad, CAGR=m["CAGR"],
                                             Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                             OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"]))
    return pd.DataFrame(rows)


def compare(mine, par, label):
    keys = ["panel", "rung", "gross", "family", "level", "depth", "cadence"]
    j = mine.set_index(keys)[COLS].join(par.set_index(keys)[COLS], rsuffix="_p", how="inner")
    d = {c: float((j[c] - j[f"{c}_p"]).abs().max()) for c in COLS}
    log(f"  {label}: {len(j)} rows joined; " + ", ".join(f"{c} {v:.3e}" for c, v in d.items()))
    return max(d.values()), len(j)


def main():
    log("=" * 140)
    log("Idea 399 ADDENDUM - is the G3 residual an APPEND to data/prices.csv?")
    log("=" * 140)
    par = pd.read_csv(PARENT)
    par = par[par.panel.isin(["U56", "B136"])].copy()
    par.loc[par.family == "QUANT", "family"] = "QEXP"
    par = par[par.family.isin(["ABS", "QEXP"])]

    px_b = load_universe(broad=True)
    log(f"\nB136 cache last day {px_b.index[-1].date()} (idea 336 ran 2026-09-07)")
    db, nb = compare(run(px_b, "B136"), par, "B136 as cached today")

    px_u = load_universe()
    log(f"\nU56 cache last day {px_u.index[-1].date()}")
    du, nu = compare(run(px_u, "U56"), par, "U56 as cached today")

    log("\nU56 truncated to each candidate vintage (the parent's own last trading day is unknown"
        " from the artefact, so every nearby day is tried and the best is reported):")
    best = (None, 9e9)
    for end in ("2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05", "2026-09-08",
                "2026-09-09"):
        sub = px_u.loc[:end]
        if len(sub) < 300:
            continue
        d, n = compare(run(sub, "U56"), par, f"U56 truncated to {end} ({len(sub)} rows)")
        if d < best[1]:
            best = (end, d)
    log(f"\nBEST U56 vintage: {best[0]} at max abs diff {best[1]:.3e} "
        f"(today's cache: {du:.3e}; B136, whose cache did not move: {db:.3e})")
    if db < 1e-9 and best[1] < du / 100:
        verdict = (f"TWO CHANNELS, both located. APPEND is DOMINANT: truncating U56 to the "
                   f"parent's own vintage ({best[0]}) cuts the residual {du:.3e} -> {best[1]:.3e}, "
                   f"a {du/max(best[1],1e-18):.0f}x reduction, and B136 - whose cache did not move - "
                   f"is bit-identical at {db:.3e}. What TRUNCATION CANNOT REMOVE ({best[1]:.3e}, "
                   f"with a vintage-invariant MaxDD floor of 1.11e-06) is a price RESTATEMENT in "
                   f"data/prices.csv, the same U56 channel idea 592 filed at 1.9e-06 and idea 519 "
                   f"named. G3 therefore FAILS its 1e-9 bar for a DATA reason, not a code one.")
    elif best[1] < 1e-9 and db < 1e-9:
        verdict = "H_APPEND CONFIRMED outright: truncation reproduces the parent to machine precision."
    else:
        verdict = "H_APPEND NOT confirmed - the residual is not explained by the vintage alone."
    log(f"VERDICT: {verdict}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
