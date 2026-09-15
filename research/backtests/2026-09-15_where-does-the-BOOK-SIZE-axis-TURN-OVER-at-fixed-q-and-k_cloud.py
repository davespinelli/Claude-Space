#!/usr/bin/env python3
"""Idea 929 (cloud, 2026-09-15) -- where does the BOOK SIZE axis TURN OVER at fixed q and k?

THE QUESTION (queue, 2026-09-15)
  Idea 686 ran a (q = cap mix, k = panel width, n = book size) ladder and found BOOK SIZE the
  only axis clearing the record's own |rho| >= 0.30 bar (+0.3125): CAND5 cleared 4b on 0 of 438
  book-cells while CAND30 cleared 0.800 at q = 0.  But 686's n axis STOPS AT 30, because its
  envelope requires max(n) < min(k) = 40.  A monotone reading over 5..30 cannot distinguish "4b
  likes big books" from "4b likes books so big they are the whole eligible set".  The queue asks:
  price the book-size axis ON ITS OWN at fixed (q, k) with k >= 100 so n can run to 60, and report
  WHERE THE PASS RATE TURNS OVER.

WHAT THIS RUN CHANGES, AND WHAT IT DELIBERATELY DOES NOT
  It changes ONE thing: the n ladder is extended from {5,10,15,20,30} to {5,10,15,20,30,40,50,60}
  on the k >= 100 slice, where 60 < k holds.  Everything else is imported and called unmodified:
  the panels come from idea 686's own `build_ladder` (so the k >= 100 panels are THE SAME COLUMN
  LISTS 686 priced), and every book, metric and 4a/4b verdict comes from idea 525's `do_panel`.
  Because of that, the n <= 30 half of this run's book table must be BYTE-IDENTICAL to 686's
  committed books.csv, which is gate G3 -- an exact cross-run reproduction, not a tolerance.

THE AXIS, AND WHY ITS FAR END MATTERS
  n  BOOK SIZE   how many names the book HOLDS (CAND-n at gross 0.75, equal weight)
  The n axis has a natural right end: at n -> (eligible count) CAND-n IS EWall, the whole eligible
  set equal-weighted.  EWall is priced on every panel here as that limit point.  If the 4b pass
  rate rises all the way to the limit, "book size" is not a dial with an optimum -- it is a
  statement that concentration costs 4b, and the record's n* = 30 is an artefact of where its
  ladder happened to stop.  If it turns over at an interior n, there is a real book size.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  n, 8 levels, every one reported: 5 / 10 / 15 / 20 / 30 / 40 / 50 / 60
  TUNED 2  k, 3 levels, every one reported: 100 / 200 / 400
  REPORTED AXES (nothing fitted on them, every point published): q in {0.00,0.25,0.50,0.75,1.00}
  as the feasible envelope allows, 3 seeded draws per cell (686's own), EWall as the n -> limit
  point, and the FULL / IS / OOS windows.

PRE-REGISTERED BARS (fixed before any number below was read; the record's own |rho| >= 0.30 with
idea 286's 8-of-11 sign-consistency share applied to the cell count)
  H_TURN   (THE QUEUE'S QUESTION) the n axis turns over INSIDE the ladder iff some interior level
           n* in {10..50} has a pooled 4b pass rate STRICTLY GREATER than both the n = 5 rate and
           the n = 60 rate, AND the same interior peak (within one ladder step) is the per-cell
           argmax in >= ceil(8/11 x L) of the L cells carrying any pass.
  H_MONO_N the pooled 4b pass rate is NON-DECREASING across all 8 n levels (686's reading,
           extended).  H_TURN and H_MONO_N cannot both pass except through a tie.
  H_N      686's own bar, restated on the longer axis: |mean within-cell rho(pass4b, n)| >= 0.30
           with the sign holding in >= ceil(8/11 x L) cells.
  H_SHARPE the SHARPE (not the thresholded pass indicator) turns over in n: the per-cell argmax
           over the 8 levels is interior (n* < 60) in >= ceil(8/11 x L_all) cells.
  H_EW     the limit point beats the whole ladder: EWall's Sharpe exceeds max_n CAND-n's Sharpe
           in >= ceil(8/11 x L_all) cells.  If H_EW passes, the book-size "optimum" is the limit.
  H_WF     (rule 8, REQUIRED) the cell (q, k, n) chosen on 2009-2016 ALONE, 2017-2026 read ONCE,
           both KEEP paths, OOS CAGR/Sharpe/MaxDD against SPY and RULES v2 on the same panel.
           This run additionally computes an OOS-WINDOW-ONLY 4a/4b (halves of 2017-2026), which
           is a strictly harder read than the full-sample verdict 686 published beside its picks.

GATES (all printed before any result number)
  G1  the feasible envelope holds on the k >= 100 slice: exact width, exact cap mix, no duplicate
      columns, no pool overflow, and max(n) = 60 < min(k) = 100
  G2  the k-identity log(Ebar) == log(breadth) + log(k) on every panel (525's identity)
  G3  CROSS-RUN EXACT: on n in {5,10,15,20,30} and the k >= 100 panels, every CAND row and every
      EWall row reproduces idea 686's committed books.csv to 1e-12 on CAGR/Sharpe/MaxDD/Ebar/
      breadth and exactly on pass4a/pass4b
  G4  determinism: one panel's book rows rebuilt from scratch, compared exactly
  G5  the shared SPY benchmark column is identical across panels (one spy triple, not 28)

PROTOCOL: 10 bps primary, t+1, weekly, gross 0.75, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: the small-cap pool (data/prices_small.csv, dropping every ticker with max_1d_move
>= 1.0 per data/small_meta.csv) and BSTK100 are CURRENT constituents of their screens, so every
CAGR and drawdown LEVEL below is optimistic and the 4b bars are EASIER here than on a
point-in-time panel.  The n contrasts are same-panel, same-days comparisons and are far less
exposed; the pass COUNTS and the rule-8 triples are levels read against SPY, which is not
survivorship-inflated, so those are upper bounds.  Stated, not hidden.

Outputs: .books.csv .panels.csv .naxis.csv .cells.csv .legs.csv .gates.csv .walkforward.csv
         .hypotheses.csv .console.txt .result.md
"""
from __future__ import annotations

import importlib.util
import math
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
BT = ROOT / "research" / "backtests"
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from engine import metrics                                  # noqa: E402
from baseline import rules_v2_weights                        # noqa: E402


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
M525 = _load(BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B.py", "idea525")
M686 = _load(BT / "2026-09-15_is-the-4b-FOOTPRINT-still-a-cap-mix-function-once-k-is-a-free-axis_cloud.py", "idea686")

do_panel, panel_measures = M525.do_panel, M525.panel_measures
spearman = M286.spearman
cand_weights, ewall_weights, run = M286.cand_weights, M286.ewall_weights, M286.run
IS_END, OOS_START = M286.IS_END, M286.OOS_START

NS = [5, 10, 15, 20, 30, 40, 50, 60]          # TUNED 1 -- the axis under test
NS_686 = M525.NS_LAD                          # [5,10,15,20,30] -- the overlap used by G3
K_MIN = 100                                   # TUNED 2 lives on k >= 100 so max(n)=60 < k
BAR_RHO, SHARE = 0.30, 8 / 11                 # the record's own bar and sign share
BK686 = BT / "2026-09-15_is-the-4b-FOOTPRINT-still-a-cap-mix-function-once-k-is-a-free-axis_cloud.books.csv"

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def need(levels):
    return int(math.ceil(SHARE * levels))


def verdict(ok, label, detail):
    P(f"    {label:10s} {detail:<74s} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


def stats_win(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    if len(x) < 60:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan)
    m = metrics(x)
    h = len(x) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(x.iloc[:h])["Sharpe"], H2=metrics(x.iloc[h:])["Sharpe"])


def keep_on_window(row, spy, v2):
    """PROTOCOL 4a/4b evaluated INSIDE one window, using that window's own halves."""
    a = (row["H1"] > v2["H1"] and row["H2"] > v2["H2"] and row["MaxDD"] >= v2["MaxDD"])
    b = (row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["Sharpe"] > spy["Sharpe"]
         and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 929 (cloud, 2026-09-15) -- where does the BOOK SIZE axis TURN OVER at fixed q and k?")
    P("=" * 100)
    P("PRE-REGISTERED BARS (docstring, fixed before any number below was read):")
    P(f"  H_TURN interior argmax of the pooled 4b pass rate, confirmed per-cell in "
      f">= ceil({SHARE:.3f} x L) cells")
    P(f"  H_MONO_N pooled pass rate non-decreasing over all {len(NS)} n levels")
    P(f"  H_N |mean within-cell rho(pass4b, n)| >= {BAR_RHO:.2f}, sign in >= ceil({SHARE:.3f} x L)")
    P("  H_SHARPE per-cell Sharpe argmax interior (n < 60);  H_EW EWall > max_n CAND-n")
    P("  H_WF rule 8: cell chosen on 2009-2016 alone, 2017-2026 read once, both KEEP paths")
    P("")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built_all, from525 = M686.build_ladder(s_stk, b_stk)
    built = [b for b in built_all if b[1] >= K_MIN]
    cells = sorted({(q, k) for q, k, *_ in built})
    P(f"idea 686's ladder: {len(built_all)} panels; this run takes the k >= {K_MIN} slice = "
      f"{len(built)} panels over {len(cells)} (q,k) cells")
    P("  cells: " + ", ".join(f"({q:.2f},{k})" for q, k in cells))
    P(f"  n ladder {NS}  (686 stopped at {max(NS_686)}; 60 < min k = {min(k for _, k in cells)})")
    P("  NOT ORTHOGONAL, stated up front: the envelope ((1-q)k <= 100) forces q >= 0.50 at k=200")
    P("  and q >= 0.75 at k=400, so k and q cannot be read independently here.  Every conclusion")
    P("  below is a WITHIN-CELL read of the n axis; no k-vs-q claim is made.")
    P("")

    # ---------------- G1 ----------------
    gates, bad = [], []
    for q, k, d, sc, lc in built:
        if len(sc) > len(s_stk) or len(lc) > len(b_stk):
            bad.append((q, k, d, "pool overflow"))
        if len(set(sc)) != len(sc) or len(set(lc)) != len(lc):
            bad.append((q, k, d, "duplicate column"))
        if len(sc) + len(lc) != k:
            bad.append((q, k, d, "width mismatch"))
        if abs(len(sc) - round(q * k)) > 0:
            bad.append((q, k, d, "cap mix mismatch"))
        if max(NS) >= k:
            bad.append((q, k, d, "max(n) >= k"))
    gates.append(dict(gate="G1 envelope on the k>=100 slice: width, cap mix, no dup cols, "
                           "no overflow, max(n)=60 < min(k)",
                      stat=f"{len(built)} panels, {len(bad)} violations", passed=not bad))

    # ---------------- run the ladder ----------------
    P("=" * 100)
    P("RUNNING THE LADDER")
    P("=" * 100)
    brows, srows, meas_rows = [], [], []
    panels = {}
    for i, (q, k, d, sc, lc) in enumerate(built):
        cols = list(sc) + list(lc)
        px = pd.concat([pxs_c[list(sc)], pxb_c[list(lc)], pxb_c[["SPY"]]], axis=1)
        tag = f"q{q:.2f}_k{k}_d{d}"
        panels[tag] = (px, cols)
        do_panel(tag, "naxis", q, d, px, cols, brows, srows, NS, {"LAD": NS})
        m = panel_measures(px, cols)
        meas_rows.append(dict(panel=tag, q=q, draw=d, from525=(q, k, d) in from525, **m))
        P(f"  {i+1:3d}/{len(built)} {tag:16s} Ebar {m['Ebar']:6.1f} breadth {m['breadth']:.4f} "
          f"({time.time()-t0:.0f}s)")
    bk = pd.DataFrame(brows)
    bk["k"] = bk["k"].astype(int)
    ms = pd.DataFrame(meas_rows)
    dump(bk, "books.csv")
    dump(ms, "panels.csv")
    P("")

    # ---------------- remaining gates ----------------
    P("=" * 100)
    P("GATES (printed before any result number)")
    P("=" * 100)
    ident = float(np.abs(np.log(ms.Ebar.clip(lower=1e-12))
                         - (np.log(ms.breadth.clip(lower=1e-12)) + np.log(ms.k))).max())
    gates.append(dict(gate="G2 k-identity log(Ebar) == log(breadth) + log(k) on every panel",
                      stat=f"max |residual| {ident:.3e} over {len(ms)} panels",
                      passed=bool(ident < 1e-9)))

    key = ["q", "k", "draw", "arm"]
    o686 = pd.read_csv(BK686)
    o686 = o686[o686.k >= K_MIN].copy()
    o686["k"] = o686["k"].astype(int)
    mine = bk[bk.arm.isin([f"CAND{n}" for n in NS_686] + ["EWall"])].copy()
    a = mine.set_index(key).sort_index()
    o = o686.set_index(key).sort_index()
    common = a.index.intersection(o.index)
    cols_num = ["CAGR", "Sharpe", "MaxDD", "Ebar", "breadth"]
    worst = max(float(np.abs(a.loc[common, c].values - o.loc[common, c].values).max())
                for c in cols_num)
    vmatch = bool((a.loc[common, "pass4b"].values == o.loc[common, "pass4b"].values).all()
                  and (a.loc[common, "pass4a"].values == o.loc[common, "pass4a"].values).all())
    g3 = bool(len(common) == len(o) and worst < 1e-12 and vmatch)
    gates.append(dict(gate="G3 CROSS-RUN EXACT vs idea 686's committed books.csv "
                           "(n<=30 and EWall, k>=100)",
                      stat=f"{len(common)} of 686's {len(o)} rows matched; worst |delta| on "
                           f"{'/'.join(cols_num)} {worst:.3e}; 4a/4b identical {vmatch}",
                      passed=g3))

    tag0 = list(panels)[0]
    px0, cols0 = panels[tag0]
    b2, s2 = [], []
    do_panel(tag0, "naxis", bk.loc[bk.panel == tag0, "q"].iloc[0],
             int(bk.loc[bk.panel == tag0, "draw"].iloc[0]), px0, cols0, b2, s2, NS, {"LAD": NS})
    r1 = bk[bk.panel == tag0].set_index("arm").sort_index()
    r2 = pd.DataFrame(b2).set_index("arm").sort_index()
    det = max(float(np.abs(r1[c].values - r2[c].values).max()) for c in ["CAGR", "Sharpe", "MaxDD"])
    gates.append(dict(gate="G4 determinism: one panel's book rows rebuilt from scratch",
                      stat=f"panel {tag0}, max |delta| {det:.3e}", passed=bool(det == 0.0)))

    spy_uniq = bk[["spy_CAGR", "spy_S", "spy_DD", "spy_OOS_S"]].drop_duplicates()
    gates.append(dict(gate="G5 the shared SPY column is one benchmark, not 28",
                      stat=f"{len(spy_uniq)} distinct SPY triples over {len(bk)} book rows",
                      passed=bool(len(spy_uniq) == 1)))

    gdf = pd.DataFrame(gates)
    for _, g in gdf.iterrows():
        P(f"  {'PASS' if g.passed else 'FAIL'}  {g.gate}")
        P(f"        {g.stat}")
    dump(gdf, "gates.csv")
    P(f"  gates passed {int(gdf.passed.sum())} of {len(gdf)}")
    P("")

    # ---------------- THE n AXIS, every grid point ----------------
    P("=" * 100)
    P("THE n AXIS -- every grid point, pooled over the 28 panels")
    P("=" * 100)
    cand = bk[bk.arm.str.startswith("CAND")].copy()
    cand["n"] = cand["n"].astype(int)
    spy = bk.iloc[0]
    legs = dict(
        L1_H1=lambda d: d.H1 > d.spy_H1,
        L2_H2=lambda d: d.H2 > d.spy_H2,
        L3_OOS=lambda d: d.OOS_Sharpe > d.spy_OOS_S,
        L4_DD=lambda d: d.MaxDD >= 0.60 * d.spy_DD,
        L5_CAGR=lambda d: d.CAGR >= 0.70 * d.spy_CAGR,
    )
    nrows = []
    for n, sub in cand.groupby("n"):
        row = dict(n=int(n), cells=len(sub), pass4b=float(sub.pass4b.mean()),
                   pass4a=float(sub.pass4a.mean()), Sharpe=float(sub.Sharpe.mean()),
                   CAGR=float(sub.CAGR.mean()), MaxDD=float(sub.MaxDD.mean()),
                   OOS_Sharpe=float(sub.OOS_Sharpe.mean()), IS_Sharpe=float(sub.IS_Sharpe.mean()))
        for ln, fn in legs.items():
            row[ln] = float(fn(sub).mean())
        nrows.append(row)
    ew = bk[bk.arm == "EWall"]
    nrows.append(dict(n=-1, cells=len(ew), pass4b=float(ew.pass4b.mean()),
                      pass4a=float(ew.pass4a.mean()), Sharpe=float(ew.Sharpe.mean()),
                      CAGR=float(ew.CAGR.mean()), MaxDD=float(ew.MaxDD.mean()),
                      OOS_Sharpe=float(ew.OOS_Sharpe.mean()), IS_Sharpe=float(ew.IS_Sharpe.mean()),
                      **{ln: float(fn(ew).mean()) for ln, fn in legs.items()}))
    na = pd.DataFrame(nrows)
    dump(na, "naxis.csv")
    P(f"  SPY (shared): FULL {spy.spy_CAGR:.2%} / {spy.spy_S:.3f} / {spy.spy_DD:.2%}   "
      f"OOS Sharpe {spy.spy_OOS_S:.3f}   4b bars: DD >= {0.60*spy.spy_DD:.2%}, "
      f"CAGR >= {0.70*spy.spy_CAGR:.2%}")
    P(f"  RULES v2 on these panels: Sharpe mean {bk.v2_S.mean():.3f}, "
      f"OOS Sharpe mean {bk.v2_OOS_S.mean():.3f}")
    P("")
    P("    n     4b     4a  Sharpe    CAGR   MaxDD  OOS_S   IS_S |  L1_H1  L2_H2 L3_OOS  L4_DD L5_CAGR")
    for _, r in na.iterrows():
        lab = "EWall" if r.n < 0 else f"{int(r.n):5d}"
        P(f"  {lab:>5s} {r.pass4b:6.3f} {r.pass4a:6.3f} {r.Sharpe:7.3f} {r.CAGR:7.2%} "
          f"{r.MaxDD:7.2%} {r.OOS_Sharpe:6.3f} {r.IS_Sharpe:6.3f} | {r.L1_H1:6.3f} {r.L2_H2:6.3f} "
          f"{r.L3_OOS:6.3f} {r.L4_DD:6.3f} {r.L5_CAGR:7.3f}")
    P("")

    # ---------------- per-cell ----------------
    crows = []
    for (q, k), sub in cand.groupby(["q", "k"]):
        per_n = sub.groupby("n").agg(pass4b=("pass4b", "mean"), Sharpe=("Sharpe", "mean"),
                                     IS_Sharpe=("IS_Sharpe", "mean")).reindex(NS)
        ews = float(bk[(bk.q == q) & (bk.k == k) & (bk.arm == "EWall")].Sharpe.mean())
        rho = spearman(sub.n.values, sub.pass4b.astype(float).values)
        any_pass = bool(per_n.pass4b.fillna(0).max() > 0)
        arg_pass = int(per_n.pass4b.idxmax()) if any_pass else -1
        crows.append(dict(q=q, k=int(k), any_pass=any_pass, rho_n=rho,
                          argmax_pass_n=arg_pass, max_pass=float(per_n.pass4b.max()),
                          pass_n5=float(per_n.pass4b.loc[5]), pass_n60=float(per_n.pass4b.loc[60]),
                          argmax_Sharpe_n=int(per_n.Sharpe.idxmax()),
                          max_Sharpe=float(per_n.Sharpe.max()), EW_Sharpe=ews,
                          EW_beats_ladder=bool(ews > per_n.Sharpe.max()),
                          **{f"p4b_n{n}": float(per_n.pass4b.loc[n]) for n in NS},
                          **{f"S_n{n}": float(per_n.Sharpe.loc[n]) for n in NS}))
    cl = pd.DataFrame(crows).sort_values(["k", "q"])
    dump(cl, "cells.csv")
    P("PER-CELL (every (q,k) cell, 4b pass rate at each n; L = " + str(len(cl)) + " cells)")
    P("     q    k |" + "".join(f"  n={n:<4d}" for n in NS) + " | EWall_S argS argP  rho_n")
    for _, r in cl.iterrows():
        rho_s = f"{r.rho_n:+.3f}" if np.isfinite(r.rho_n) else "   nan"
        P(f"  {r.q:.2f} {int(r.k):4d} |" + "".join(f" {r[f'p4b_n{n}']:6.2f}" for n in NS)
          + f" | {r.EW_Sharpe:7.3f} {int(r.argmax_Sharpe_n):4d} {int(r.argmax_pass_n):4d} {rho_s}")
    P("")
    P("PER-CELL SHARPE (same cells, mean Sharpe at each n)")
    P("     q    k |" + "".join(f"  n={n:<4d}" for n in NS) + " |   EWall")
    for _, r in cl.iterrows():
        P(f"  {r.q:.2f} {r.k:4d} |" + "".join(f" {r[f'S_n{n}']:6.3f}" for n in NS)
          + f" | {r.EW_Sharpe:7.3f}")
    P("")
    dump(pd.DataFrame([dict(leg=k, **{f"n{n}": float(na.loc[na.n == n, k].iloc[0]) for n in NS},
                            EWall=float(na.loc[na.n == -1, k].iloc[0]))
                       for k in legs]), "legs.csv")

    # ---------------- hypotheses ----------------
    P("=" * 100)
    P("HYPOTHESES")
    P("=" * 100)
    pooled = na[na.n > 0].set_index("n").reindex(NS)
    interior = [n for n in NS if n not in (5, 60)]
    p5, p60 = float(pooled.pass4b.loc[5]), float(pooled.pass4b.loc[60])
    best_int = max(interior, key=lambda n: float(pooled.pass4b.loc[n]))
    pbest = float(pooled.pass4b.loc[best_int])
    passcells = cl[cl.any_pass]
    L_pass = len(passcells)
    step = {n: i for i, n in enumerate(NS)}
    conf = int(sum(1 for _, r in passcells.iterrows()
                   if abs(step[int(r.argmax_pass_n)] - step[best_int]) <= 1)) if L_pass else 0
    H_TURN = verdict(pbest > p5 and pbest > p60 and L_pass > 0 and conf >= need(L_pass),
                     "H_TURN", f"pooled 4b n=5 {p5:.3f} / best interior n={best_int} {pbest:.3f} / "
                     f"n=60 {p60:.3f}; per-cell confirm {conf} of {L_pass} (need "
                     f"{need(L_pass) if L_pass else 0})")
    diffs = np.diff(pooled.pass4b.values)
    H_MONO_N = verdict(bool((diffs >= -1e-12).all()), "H_MONO_N",
                       f"pass rate {' '.join(f'{v:.3f}' for v in pooled.pass4b.values)}; "
                       f"min step {diffs.min():+.3f}")
    rhos = cl.rho_n.dropna().values
    mrho = float(rhos.mean()) if len(rhos) else np.nan
    sgn = int((np.sign(rhos) == np.sign(mrho)).sum()) if len(rhos) and mrho else 0
    H_N = verdict(np.isfinite(mrho) and abs(mrho) >= BAR_RHO and sgn >= need(len(rhos)), "H_N",
                  f"mean within-cell rho(pass4b, n) {mrho:+.4f}; sign {sgn} of {len(rhos)} "
                  f"(need {need(len(rhos))}); 686 read +0.3125 on n<=30")
    int_sh = int((cl.argmax_Sharpe_n < 60).sum())
    H_SHARPE = verdict(int_sh >= need(len(cl)), "H_SHARPE",
                       f"per-cell Sharpe argmax interior in {int_sh} of {len(cl)} cells "
                       f"(need {need(len(cl))}); argmax levels "
                       f"{dict(cl.argmax_Sharpe_n.value_counts().sort_index())}")
    ewb = int(cl.EW_beats_ladder.sum())
    H_EW = verdict(ewb >= need(len(cl)), "H_EW",
                   f"EWall Sharpe > max_n CAND-n in {ewb} of {len(cl)} cells "
                   f"(need {need(len(cl))})")
    P("")

    # ---------------- RULE 8 ----------------
    P("=" * 100)
    P("RULE 8 -- cell chosen on 2009-2016 ALONE, 2017-2026 read ONCE, both KEEP paths")
    P("=" * 100)
    allbk = bk.copy()
    cellIS = allbk.groupby(["q", "k", "arm"]).agg(
        IS_Sharpe=("IS_Sharpe", "mean"), n=("n", "mean")).reset_index()
    sel_sets = {"ALL": cellIS,
                "CAND_ONLY": cellIS[cellIS.arm != "EWall"],
                "BIG_N_ONLY": cellIS[cellIS.arm.isin([f"CAND{n}" for n in NS if n > 30])],
                "K100": cellIS[cellIS.k == 100]}
    picks = {}
    for sname, sl in sel_sets.items():
        if not len(sl):
            continue
        r = sl.loc[sl.IS_Sharpe.idxmax()]
        picks[f"PICK_ISSHARPE_{sname}"] = (r.q, int(r.k), r.arm, float(r.IS_Sharpe))
    # the record's own candidate shape: largest book on the widest panel, chosen without OOS
    r = cellIS[(cellIS.k == cellIS.k.max()) & (cellIS.arm == "CAND60")]
    if len(r):
        r = r.loc[r.IS_Sharpe.idxmax()]
        picks["PICK_KMAX_N60"] = (r.q, int(r.k), r.arm, float(r.IS_Sharpe))

    wrows = []
    for pname, (q, k, arm, is_s) in picks.items():
        draws = [t for t in panels if t.startswith(f"q{q:.2f}_k{k}_")]
        for tag in draws:
            px, cols = panels[tag]
            st = px.index[260]
            wfn = ewall_weights if arm == "EWall" else cand_weights(int(arm[4:]))
            r_ = run(px, wfn).loc[st:]
            spy_r = px["SPY"].pct_change().fillna(0).loc[st:]
            v2_r = run(px, lambda p: rules_v2_weights(p).drop(columns=["SPY"], errors="ignore")
                       .reindex(columns=p.columns).fillna(0.0)).loc[st:]
            oo, so, vo = (stats_win(x, OOS_START) for x in (r_, spy_r, v2_r))
            fa, fb = keep_on_window(stats_win(r_), stats_win(spy_r), stats_win(v2_r))
            a4, b4 = keep_on_window(oo, so, vo)
            wrows.append(dict(selector=pname, panel=tag, q=q, k=k, arm=arm, IS_Sharpe=is_s,
                              OOS_CAGR=oo["CAGR"], OOS_Sharpe=oo["Sharpe"], OOS_MaxDD=oo["MaxDD"],
                              OOS_H1=oo["H1"], OOS_H2=oo["H2"],
                              spy_OOS_CAGR=so["CAGR"], spy_OOS_Sharpe=so["Sharpe"],
                              spy_OOS_MaxDD=so["MaxDD"],
                              v2_OOS_CAGR=vo["CAGR"], v2_OOS_Sharpe=vo["Sharpe"],
                              v2_OOS_MaxDD=vo["MaxDD"],
                              full4a=fa, full4b=fb, oos4a=a4, oos4b=b4))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward.csv")
    for _, r in wf.iterrows():
        P(f"  {r.selector:24s} {r.panel:16s} {r.arm:7s} IS {r.IS_Sharpe:6.3f} | OOS "
          f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / {r.OOS_MaxDD:7.2%}  vs SPY "
          f"{r.spy_OOS_CAGR:7.2%} / {r.spy_OOS_Sharpe:6.3f} / {r.spy_OOS_MaxDD:7.2%}  vs v2 "
          f"{r.v2_OOS_CAGR:7.2%} / {r.v2_OOS_Sharpe:6.3f} / {r.v2_OOS_MaxDD:7.2%}  "
          f"FULL 4a/4b {int(r.full4a)}/{int(r.full4b)}  OOS-WINDOW 4a/4b {int(r.oos4a)}/{int(r.oos4b)}")
    H_WF = bool(wf.oos4b.any())
    P(f"  OOS-WINDOW 4b: {int(wf.oos4b.sum())} of {len(wf)} rule-8 picks;  "
      f"4a: {int(wf.oos4a.sum())} of {len(wf)};  "
      f"FULL-SAMPLE 4b on the same picks: {int(wf.full4b.sum())} of {len(wf)}")
    P("")

    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hyp = dict(H_TURN=H_TURN, H_MONO_N=H_MONO_N, H_N=H_N, H_SHARPE=H_SHARPE, H_EW=H_EW, H_WF=H_WF)
    for kk, vv in hyp.items():
        P(f"  {kk:9s} {'PASS' if vv else 'FAIL'}")
    P(f"  gates {int(gdf.passed.sum())} of {len(gdf)};  runtime {time.time()-t0:.0f}s")
    pd.DataFrame([hyp]).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(hyp=hyp, bk=bk, cl=cl, na=na, wf=wf, gates=gdf)


if __name__ == "__main__":
    main()
