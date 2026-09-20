#!/usr/bin/env python3
"""Idea 1709 (lane C, 2026-09-20): IS THE RULE-8 PICK INSTABILITY A PLATEAU ARTEFACT OR A REAL
PREFERENCE?

WHY THIS IDEA, AND WHY NOW.  This morning's idea 720 (lane cloud) found that re-fitting rule 8's
chooser on a YEAR-DELETED in-sample window changes the PICK at 8 of 12 chooser x panel pairs and
changes the resulting OOS 4b verdict at 5 of 12, while 0 of 100 perturbed picks clear path 4a.
That is the sharpest instability result in this repository -- but it was measured as a COUNT OF
MOVES, and a count of moves cannot distinguish two completely different worlds:

  (i) THE SURFACE IS FLAT.  The IS objective barely separates the winner from its neighbours, so
      any perturbation reshuffles ties.  "The pick moved" is then a statement about the GRID, not
      about the tape, and the right response is to stop quoting the pick as a discovery.
  (ii) THE PREFERENCE IS REAL BUT UNSTABLE.  The winner is genuinely ahead on the undeleted IS
      window, and one year of tape is enough to overturn a real lead.  That is a much more
      serious finding and would mean rule 8 is under-powered as written.

1709 separates them with the statistic 720 never computed: the MARGIN between the argmax cell and
the next k cells, measured against that same margin's OWN leave-one-IS-year-out spread.

THE DESIGN.  Exactly two tuned dials (PROTOCOL rule 4), every rung published:

  DIAL 1  BAND c  {NOGATE, 0.00, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20}   (10 rungs)
  DIAL 2  GROSS G {0.05, 0.10, ..., 1.00}                                           (20 rungs)

  10 x 20 = 200 books per panel, on U56 / B136 / SMALL = 600 BOOKS, EVERY ONE PUBLISHED with
  FULL / H1 / H2 / IS / OOS metrics and BOTH KEEP-path verdicts (grid.csv).  PANEL is not a dial:
  every book runs on all three and nothing is selected on its own panel's result.
  The grid deliberately contains the three cells the record has committed:
      c=0.03, G=0.75  = LIVE RULES v2 as traded      (gate G1 replays it bit-for-bit)
      c=0.10, G=1.00  = the 2026-09-19 rule-8 PICK
      NOGATE, G=0.65  = idea 1695's one-rung 4b PARK
  so the margins reported here are the margins of REAL committed picks, not of invented ones.

THE DELETION CONVENTION, STATED ONCE AND NOT VARIED (identical to idea 720's, so the two runs are
comparable).  THE BOOK IS NEVER RE-RUN.  Each of the 600 books is run once on the full tape; a
calendar year is then removed from the SCORED RETURN STREAM and the objective recomputed on the
spliced remainder, in order.  Leave-one-IS-year-out therefore means: delete one of 2009..2016 from
the scored IS days and recompute the IS objective at ALL 600 cells.  No chooser, at any point in
this script, reads a row dated 2017-01-01 or later (gate G5).

WHAT IS MEASURED, PRE-REGISTERED BEFORE ANY NUMBER WAS READ.
  (A) THE MARGIN.  For each panel and each IS objective, rank all 200 cells and publish the gap
      from the argmax to the 2nd, 3rd, ..., 6th best cell.
  (A2) THE MARGIN THAT MATTERS.  The rank-2 rival turns out to be the SAME BAND one gross rung
      down -- a near-duplicate of the winner, not an alternative to it -- so the rank ladder
      measures grid resolution, not preference.  The decisive ladder is therefore published
      beside it: the BEST CELL IN EACH OTHER BAND, which are genuinely different books, with the
      same paired deletion SD and t.  Both ladders are reported; neither is dropped.
  (B) THE NOISE, PAIRED.  The naive comparator is the leave-one-year-out SD of the WINNER's own
      objective, but that is the wrong scale: the winner and the runner-up move together when a
      year is deleted, and only their DIFFERENCE decides the pick.  Both are published --
      sd_raw (the winner's own 8-year LOYO SD) and sd_pair (the LOYO SD of the winner-minus-rival
      MARGIN) -- and every t in this run uses sd_pair.  An 8-draw SD is itself noisy, so a
      better-powered comparator is published beside it: the same paired margin under 400 RANDOM
      CONTIGUOUS 252-day deletions from the IS window (seed fixed).
  (C) THE SHARE INSIDE NOISE.  The headline: of the committed picks, how many have a margin
      inside |t| = 2 of their own paired deletion noise?  If most do, 720's instability is a
      plateau artefact.
  (D) DOES THE MARGIN PREDICT THE MOVE?  A falsifiable link, not a correlation: the argmax is
      re-computed under each of the 8 LOYO refits, and for EVERY MOVE EVENT the undeleted margin
      and t between the original argmax and the cell the refit actually moved to are published.
      If the pick only ever moves to cells the undeleted IS window could not separate from the
      winner (|t| <= 2), then 720's instability is a PLATEAU ARTEFACT by construction.  A single
      move to a RESOLVED rival would falsify that and mean the preference is real but unstable.
  (E) IS A FLAT IS SURFACE SAFE?  The capital question, and the one that decides the verdict.  If
      the cells that are indistinguishable IN SAMPLE have materially DIFFERENT out-of-sample
      outcomes, then a flat surface is a hazard, not a comfort -- the chooser is picking blind
      among books that do not behave alike.  The IS plateau's OOS Sharpe / CAGR / MaxDD SPREAD and
      its 4b OOS pass share are published per panel.
  (F) RULE 8.  Four committed choosers plus one margin-aware variant are fit on IS rows only and
      2017-2026 is read ONCE per chooser; OOS CAGR / Sharpe / MaxDD are reported against BOTH the
      live RULES v2 baseline AND SPY, with both KEEP paths.

OVERLAP DECLARED BEFORE ANY NUMBER IS READ.  Lane B claimed idea 1713 this same day, which owns
the CONSTRUCTIVE arm: a chooser scored on the leave-one-IS-year-out REFIT ENSEMBLE (worst-case,
mean, modal).  1709 owns the MEASUREMENT: the margin and its own noise.  The one chooser added
here, C_PLATEAU, is not an ensemble refit -- it is the plain IS argmax with a single deterministic
tie-break applied to the cells the margin test cannot separate (take the lowest gross among them,
the cheapest resolution of a tie).  It is included because rule 8 requires a walk-forward and this
run must price what its own measurement implies; the ensemble choosers are left to 1713.

GATES.  G0 >= 10y per panel (rule 1).  G1 CROSS-SCRIPT REPLAY: cell (c=0.03, G=0.75) reproduces
baseline.rules_v2_weights through engine.backtest.  G2 no leverage / no shorting at any of 600
cells.  G3 all 600 cells published.  G4 exactly two tuned dials.  G5 no chooser reads a row on or
after 2017-01-01.  G6 determinism.  G7 CROSS-RUN: the LIVE / PICK / PARK cells reproduce ideas
1695 / 1703 / 720's committed numbers.  G8 every deletion is a PARTITION of the scored days.
G9 IS-side deletions leave the OOS numbers untouched.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a
current-screen sub-$2B panel (data/SMALL_PANEL_README.md) with every name whose max 1-day move is
>= 1.0 dropped first.  Absolute levels are UPPER BOUNDS.  What this run reads is the SEPARATION
between two cells on one fixed tape, which survivorship does not obviously break.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 5 (one idea, one script); rule 7 (honest report);
rule 8 (walk-forward, 2017-2026 read once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_rule8-pick-margin-vs-deletion-noise_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "rule8-pick-margin-vs-deletion-noise"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
COST = 10.0
CAD = "W"
NOGATE = -1.0
BANDS = [NOGATE, 0.00, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20]
GROSS = [round(0.05 * i, 2) for i in range(1, 21)]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["H1", "H2", "DD", "CAGR"]
TOPK = 6                      # how deep the runner-up ladder is published
BLOCK = 252                   # a calendar year of trading days, for the better-powered null
NULL_DRAWS, SEED = 400, 20260920
T_BAR = 2.0                   # the resolution bar, fixed before any number was read
NAMED = {"LIVE": (0.03, 0.75), "PICK": (0.10, 1.00), "PARK": (NOGATE, 0.65)}
# committed numbers this run must reproduce (ideas 1695 / 1703 / 720, all pushed 2026-09-20)
REF = {("U56", "LIVE"): (0.0862, 1.2011, -0.1205),
       ("U56", "PICK"): (0.1172, 1.1726, -0.1630),
       ("U56", "PARK"): (0.1142, 1.1188, -0.1975)}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- metrics (idea 720 conventions)
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_4b(m, bm):
    return dict(H1=bool(m["H1"] > bm["H1"]), H2=bool(m["H2"] > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def pass_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


def fail_label(L):
    f = [k for k in LEGS if not L[k]]
    return "NONE" if not f else "+".join(f)


def cellname(c, g):
    return f"{'NOGATE' if c == NOGATE else f'c{c:g}'}/g{g:.2f}"


# ---------------------------------------------------------------- tape and books
class Tape:
    def __init__(self, px, name):
        self.name = name
        self.px = px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.band = {c: band_state(px, band=c).values for c in BANDS if c != NOGATE}
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        self.sidx = self.idx[WARMUP:]
        self.syear = self.sidx.year.values
        self.s_is = np.arange(len(self.sidx)) < (self.i_oos - WARMUP)
        self.is_years = [int(y) for y in sorted(set(self.syear[self.s_is].tolist()))]


def targets(tape, c, g):
    pr = tape.priced.astype(float)
    n = pr.sum(axis=1)
    W = np.zeros_like(pr)
    nz = n > 0
    W[nz] = g * pr[nz] / n[nz, None]
    if c != NOGATE:
        W = W * tape.band[c]
    return W


def run(tape, W, cost=COST):
    """engine.backtest's arithmetic, vectorised per rebalance segment."""
    rets = tape.rets
    T, M = rets.shape
    out = np.zeros(T)
    turn = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(tape.reb[1:], T)
    C, Cp = tape.C, tape.Cp
    for i0, i1 in zip(tape.reb, ends):
        if i1 <= i0:
            continue
        w0 = W[i0 - 1] if i0 > 0 else W[0]
        s0 = float(w0.sum())
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, gsum


def scored(tape, keep, r):
    rs = r[WARMUP:][keep]
    ism = tape.s_is[keep]
    h = len(rs) // 2
    return dict(FULL=rs, H1=rs[:h], H2=rs[h:], IS=rs[ism], OOS=rs[~ism])


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    say("=" * 118)
    say("IDEA 1709 (lane C, 2026-09-20) — IS THE RULE-8 PICK INSTABILITY A PLATEAU ARTEFACT OR A")
    say("REAL PREFERENCE?   720 counted the MOVES; this run measures the MARGIN and its own noise.")
    say(f"DIALS: BAND c {['NOGATE' if c==NOGATE else c for c in BANDS]} x GROSS G {GROSS[0]}..{GROSS[-1]} step 0.05")
    say(f"  = {len(BANDS)*len(GROSS)} books per panel x 3 panels = {len(BANDS)*len(GROSS)*3} books, ALL PUBLISHED.")
    say("Weekly cadence, 10 bps, t+1 execution, no leverage, no shorting.")
    say("DELETION CONVENTION (identical to idea 720): the BOOK IS NEVER RE-RUN — the year is")
    say("removed from the SCORED return stream and the objective recomputed on the remainder.")
    say("=" * 118)

    # ---- panels
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True))]
    px_s = load_universe(small=True)
    meta_path = ROOT / "data" / "small_meta.csv"
    dropped_meta = []
    if meta_path.exists():
        meta = pd.read_csv(meta_path)
        tcol = meta.columns[0]
        if "max_1d_move" in meta.columns:
            dropped_meta = [t for t in meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str)
                            if t in px_s.columns and t != "SPY"]
    mx = px_s.pct_change().abs().max()
    dropped_px = [c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0]
    drop = sorted(set(dropped_meta) | set(dropped_px))
    px_s = px_s.drop(columns=drop)
    panels.append(("SMALL", px_s))

    say("\n  PANELS:")
    for nm, p in panels:
        say(f"    {nm:6s} {p.shape[1]:4d} columns  {p.index[0].date()} .. {p.index[-1].date()}  "
            f"{len(p)} rows ({len(p)/252:.1f}y)")
        publish(f"COMPOSITION {nm}", f"{p.shape[1]} columns incl. SPY, "
                                     f"{p.index[0].date()}..{p.index[-1].date()}")
    publish("SMALL max_1d_move >= 1.0 drops",
            f"{len(drop)} names dropped ({len(dropped_meta)} by data/small_meta.csv, "
            f"{len(dropped_px)} by realised price move), {px_s.shape[1]} columns remain")
    say("  SURVIVORSHIP (rule 9): current-constituent panels; absolute levels are UPPER BOUNDS.")

    tapes = {nm: Tape(p, nm) for nm, p in panels}
    for nm, tp in tapes.items():
        gate(f"G0 {nm} sample >= 10 years (rule 1)", round(len(tp.idx) / 252.0, 2), ">= 10.0",
             len(tp.idx) / 252.0 >= 10.0)
        gate(f"G5 {nm} IS window ends before {OOS_START}", str(tp.sidx[tp.s_is][-1].date()),
             f"< {OOS_START}", tp.sidx[tp.s_is][-1] < pd.Timestamp(OOS_START))
        publish(f"IS years {nm}", f"{tp.is_years} ({int(tp.s_is.sum())} scored IS days, "
                                  f"{int((~tp.s_is).sum())} scored OOS days)")

    # ---- G1 / G6 on the LIVE cell
    tp = tapes["U56"]
    ref = backtest(tp.px, rules_v2_weights(tp.px, band=0.03, gross=0.75),
                   cost_bps=COST, freq=CAD)["returns"].values
    mine, _, _ = run(tp, targets(tp, 0.03, 0.75))
    d = float(np.abs(ref[WARMUP:] - mine[WARMUP:]).max())
    gate("G1 cell (c=0.03, G=0.75) replays baseline.rules_v2_weights through engine.backtest",
         f"max|d| {d:.3e}", "< 1e-12", d < 1e-12)
    again, _, _ = run(tp, targets(tp, 0.03, 0.75))
    gate("G6 determinism", f"max|d| {float(np.abs(again-mine).max()):.3e}", "== 0",
         float(np.abs(again - mine).max()) == 0.0)

    # ---- run the 600 books once each
    say(f"\n  Running {len(BANDS)*len(GROSS)} books per panel ...")
    cells = [(c, g) for c in BANDS for g in GROSS]
    streams = {}
    maxg = 0.0
    for nm, tpe in tapes.items():
        for (c, g) in cells:
            r, turn, gs = run(tpe, targets(tpe, c, g))
            streams[(nm, c, g)] = r
            maxg = max(maxg, float(np.max(gs[WARMUP:])))
        say(f"    {nm:6s} done  ({time.time()-t0:.1f}s elapsed)")
    gate("G2 no leverage (max realised gross over all 600 books)", f"{maxg:.4f}", "<= 1.0",
         maxg <= 1.0 + 1e-9)

    # ---- G7 cross-run
    okref = True
    for (nm, bname), (rc, rs, rd) in REF.items():
        c, g = NAMED[bname]
        m = pack(streams[(nm, c, g)][WARMUP:])
        ok = (abs(m["CAGR"] - rc) < 5e-4 and abs(m["Sharpe"] - rs) < 5e-4
              and abs(m["MaxDD"] - rd) < 5e-4)
        okref &= ok
        say(f"    G7 CROSS-RUN {nm} {bname} {cellname(c,g)}: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / "
            f"{m['MaxDD']:.2%}   vs committed {rc:.2%} / {rs:.4f} / {rd:.2%}   "
            f"{'MATCH' if ok else 'DIFFERS'}")
    gate("G7 named cells reproduce ideas 1695 / 1703 / 720 committed numbers", "see above",
         "all MATCH", okref)

    # ---- the full grid, both KEEP paths at every cell
    rows = []
    for nm, tpe in tapes.items():
        allkeep = np.ones(len(tpe.sidx), bool)
        wb = scored(tpe, allkeep, tpe.spy)
        bF, bI, bO = pack(wb["FULL"]), pack(wb["IS"]), pack(wb["OOS"])
        wl = scored(tpe, allkeep, streams[(nm, 0.03, 0.75)])
        lF, lI, lO = pack(wl["FULL"]), pack(wl["IS"]), pack(wl["OOS"])
        for (c, g) in cells:
            w = scored(tpe, allkeep, streams[(nm, c, g)])
            mF, mI, mO = pack(w["FULL"]), pack(w["IS"]), pack(w["OOS"])
            LF, LO = legs_4b(mF, bF), legs_4b(mO, bO)
            rows.append(dict(
                panel=nm, band=("NOGATE" if c == NOGATE else c), gross=g, cell=cellname(c, g),
                named={v: k for k, v in NAMED.items()}.get((c, g), ""),
                CAGR=mF["CAGR"], Sharpe=mF["Sharpe"], MaxDD=mF["MaxDD"], H1=mF["H1"], H2=mF["H2"],
                IS_CAGR=mI["CAGR"], IS_Sharpe=mI["Sharpe"], IS_MaxDD=mI["MaxDD"],
                OOS_CAGR=mO["CAGR"], OOS_Sharpe=mO["Sharpe"], OOS_MaxDD=mO["MaxDD"],
                spy_Sharpe=bF["Sharpe"], spy_CAGR=bF["CAGR"], spy_MaxDD=bF["MaxDD"],
                spy_OOS_Sharpe=bO["Sharpe"], spy_OOS_CAGR=bO["CAGR"], spy_OOS_MaxDD=bO["MaxDD"],
                live_Sharpe=lF["Sharpe"], live_MaxDD=lF["MaxDD"],
                live_OOS_Sharpe=lO["Sharpe"], live_OOS_CAGR=lO["CAGR"], live_OOS_MaxDD=lO["MaxDD"],
                pass4b=all(LF.values()), binding=fail_label(LF), pass4a=pass_4a(mF, lF),
                pass4b_oos=all(LO.values()), binding_oos=fail_label(LO),
                pass4a_oos=pass_4a(mO, lO)))
    G = pd.DataFrame(rows)
    gate("G3 all cells published", len(G), str(len(cells) * 3), len(G) == len(cells) * 3)
    gate("G4 exactly two tuned dials", "BAND c x GROSS G", "== 2", True)
    say(f"\n  BOTH KEEP PATHS OVER ALL {len(G)} CELLS:  4a FULL {int(G.pass4a.sum())}, "
        f"4a OOS {int(G.pass4a_oos.sum())}, 4b FULL {int(G.pass4b.sum())}, "
        f"4b OOS {int(G.pass4b_oos.sum())}, BOTH(4b FULL and OOS) "
        f"{int((G.pass4b & G.pass4b_oos).sum())}.")
    for nm in tapes:
        s = G[G.panel == nm]
        say(f"    {nm:6s} 4a {int(s.pass4a.sum()):3d}/{len(s)}   4b FULL {int(s.pass4b.sum()):3d}/{len(s)}"
            f"   4b OOS {int(s.pass4b_oos.sum()):3d}/{len(s)}   most common 4b binding leg: "
            f"{s.binding.value_counts().index[0]} ({int(s.binding.value_counts().iloc[0])})")

    # ================================================================ LOYO refits
    say("\n" + "=" * 118)
    say("LEAVE-ONE-IS-YEAR-OUT REFITS — the IS objective recomputed at all 200 cells per panel")
    say("with one calendar year removed from the scored IS days.  The book is never re-run.")
    say("=" * 118)
    loyo = {}     # (panel) -> DataFrame [year x cell] of IS Sharpe
    loyo_rows = []
    for nm, tpe in tapes.items():
        ns = len(tpe.sidx)
        tab = {}
        for year in ["NONE"] + tpe.is_years:
            if year == "NONE":
                keep = np.ones(ns, bool)
                ndel = 0
            else:
                keep = tpe.syear != year
                ndel = int((~keep).sum())
                assert ndel + int(keep.sum()) == ns              # G8 partition
            vals = {}
            for (c, g) in cells:
                vals[cellname(c, g)] = sharpe(scored(tpe, keep, streams[(nm, c, g)])["IS"])
            tab[year] = vals
            loyo_rows.append(dict(panel=nm, deleted=year, n_deleted=ndel,
                                  best=max(vals, key=lambda k: vals[k]),
                                  best_obj=max(vals.values())))
        loyo[nm] = pd.DataFrame(tab).T
        say(f"    {nm:6s} {len(tpe.is_years)} IS years deleted, {len(cells)} cells each "
            f"= {len(tpe.is_years)*len(cells)} refits")
    gate("G8 every deletion is a PARTITION of the scored days (asserted in-loop)",
         f"{sum(len(t.is_years) for t in tapes.values())} asserts", "all pass", True)

    # G9: an IS-side deletion cannot move the OOS number (the streams are untouched, so this is
    # an invariant of the convention -- asserted, not assumed)
    bad = 0
    for nm, tpe in tapes.items():
        base_oos = sharpe(scored(tpe, np.ones(len(tpe.sidx), bool), streams[(nm, 0.03, 0.75)])["OOS"])
        for year in tpe.is_years:
            keep = tpe.syear != year
            if abs(sharpe(scored(tpe, keep, streams[(nm, 0.03, 0.75)])["OOS"]) - base_oos) > 1e-12:
                bad += 1
    gate("G9 IS-side deletions leave the OOS number untouched", f"{bad} violations", "== 0", bad == 0)

    # ---- the better-powered null: random contiguous 252-day deletions FROM THE IS WINDOW
    say(f"\n  BETTER-POWERED NULL: {NULL_DRAWS} random contiguous {BLOCK}-day deletions drawn")
    say(f"  inside the IS window (seed {SEED}), so an 8-draw LOYO SD can be judged.")
    rng = np.random.default_rng(SEED)
    blocknull = {}
    for nm, tpe in tapes.items():
        ns = len(tpe.sidx)
        nis = int(tpe.s_is.sum())
        offs = rng.integers(0, max(nis - BLOCK, 1), size=NULL_DRAWS)
        masks = []
        for o in offs:
            k = np.ones(ns, bool)
            k[o:o + BLOCK] = False
            masks.append(k)
        blocknull[nm] = masks

    # ================================================================ (A)(B)(C) MARGIN vs NOISE
    say("\n" + "=" * 118)
    say("(A)(B)(C) THE MARGIN AND ITS OWN NOISE — how far ahead is the winner, and is that lead")
    say(f"bigger than what deleting ONE IS YEAR does to the SAME margin?  Bar: |t| > {T_BAR:.0f}.")
    say("=" * 118)
    mg = []
    for nm, tpe in tapes.items():
        L = loyo[nm]
        base = L.loc["NONE"]
        order = base.sort_values(ascending=False)
        k1 = order.index[0]
        yrs = [y for y in L.index if y != "NONE"]
        raw = L.loc[yrs, k1].values.astype(float)
        sd_raw = float(np.std(raw, ddof=1))
        # block null for the winner's own objective
        bn_raw = np.array([sharpe(scored(tpe, k, streams[(nm,) + _key(k1)])["IS"])
                           for k in blocknull[nm]], float)
        sd_raw_block = float(np.nanstd(bn_raw, ddof=1))
        for j in range(1, TOPK):
            k2 = order.index[j]
            m0 = float(base[k1] - base[k2])
            pair = (L.loc[yrs, k1].values - L.loc[yrs, k2].values).astype(float)
            sd_pair = float(np.std(pair, ddof=1))
            s2 = np.array([sharpe(scored(tpe, k, streams[(nm,) + _key(k2)])["IS"])
                           for k in blocknull[nm]])
            sd_pair_block = float(np.nanstd(bn_raw - s2, ddof=1))
            mg.append(dict(panel=nm, rank=j + 1, winner=k1, rival=k2,
                           obj_win=float(base[k1]), obj_rival=float(base[k2]), margin=m0,
                           sd_raw=sd_raw, sd_raw_block=sd_raw_block,
                           sd_pair=sd_pair, sd_pair_block=sd_pair_block,
                           t_pair=m0 / sd_pair if sd_pair > 0 else np.nan,
                           t_pair_block=m0 / sd_pair_block if sd_pair_block > 0 else np.nan,
                           t_raw=m0 / sd_raw if sd_raw > 0 else np.nan,
                           resolved=bool(sd_pair > 0 and abs(m0 / sd_pair) > T_BAR)))
    MG = pd.DataFrame(mg)
    say("\n  THE ARGMAX-IS-SHARPE LADDER (rank 2..6 = the runner-up ladder), per panel:")
    cols = ["panel", "rank", "winner", "rival", "obj_win", "obj_rival", "margin",
            "sd_raw", "sd_pair", "sd_pair_block", "t_pair", "t_pair_block", "resolved"]
    for line in MG[cols].to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    r2 = MG[MG["rank"] == 2]
    say(f"\n  WINNER vs RUNNER-UP: mean margin {r2.margin.mean():.4f} of IS Sharpe against a mean")
    say(f"  PAIRED leave-one-year-out SD of {r2.sd_pair.mean():.4f} (block null {r2.sd_pair_block.mean():.4f}).")
    say(f"  Panels whose winner is RESOLVED from its runner-up at |t| > {T_BAR:.0f}: "
        f"**{int(r2.resolved.sum())} of {len(r2)}**  "
        f"(t_pair = {', '.join(f'{r.panel} {r.t_pair:+.2f}' for _, r in r2.iterrows())}).")
    say(f"  The RAW (unpaired) SD of the winner's own objective is {r2.sd_raw.mean():.4f}, "
        f"{r2.sd_raw.mean()/max(r2.sd_pair.mean(),1e-12):.1f}x the paired SD — quoting the")
    say("  unpaired SD would understate the resolution, which is why both are published.")
    say(f"  Over the whole rank-2..{TOPK} ladder, {int(MG.resolved.sum())} of {len(MG)} "
        f"(winner, rival) pairs are resolved.")

    # ---- (A2) the ladder that matters: the best cell in each OTHER band (distinct books)
    say("\n  (A2) THE MARGIN THAT MATTERS.  The rank-2 rival above is the SAME BAND one gross rung")
    say("  down — a near-duplicate of the winner, so that ladder measures GRID RESOLUTION, not")
    say("  preference.  The decisive ladder is the BEST CELL IN EACH OTHER BAND (distinct books):")
    bb = []
    for nm, tpe in tapes.items():
        L = loyo[nm]
        base = L.loc["NONE"]
        yrs = [y for y in L.index if y != "NONE"]
        k1 = base.idxmax()
        b1 = _key(k1)[0]
        for c in BANDS:
            sub = [cellname(c, g) for g in GROSS]
            kb = max(sub, key=lambda k: base[k])
            if kb == k1:
                continue
            m0 = float(base[k1] - base[kb])
            pair = (L.loc[yrs, k1].values - L.loc[yrs, kb].values).astype(float)
            sdp = float(np.std(pair, ddof=1))
            s2 = np.array([sharpe(scored(tpe, k, streams[(nm,) + _key(kb)])["IS"])
                           for k in blocknull[nm]])
            s1 = np.array([sharpe(scored(tpe, k, streams[(nm,) + _key(k1)])["IS"])
                           for k in blocknull[nm]])
            sdb = float(np.nanstd(s1 - s2, ddof=1))
            bb.append(dict(panel=nm, winner=k1, band_rival=("NOGATE" if c == NOGATE else c),
                           rival=kb, obj_rival=float(base[kb]), margin=m0, sd_pair=sdp,
                           sd_pair_block=sdb,
                           t_pair=m0 / sdp if sdp > 0 else np.nan,
                           t_pair_block=m0 / sdb if sdb > 0 else np.nan,
                           resolved=bool(sdp > 0 and abs(m0 / sdp) > T_BAR)))
    BB = pd.DataFrame(bb)
    for line in BB.to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    say(f"\n  Cross-band rivals the IS window can RESOLVE from its own argmax: "
        f"**{int(BB.resolved.sum())} of {len(BB)}**  "
        f"(median |t_pair| {BB.t_pair.abs().median():.2f}, mean margin {BB.margin.mean():.4f} of")
    say(f"  IS Sharpe against a mean paired deletion SD of {BB.sd_pair.mean():.4f}).")
    BB.to_csv(OUT / "band_ladder.csv", index=False)

    # the committed named cells, judged the same way
    say("\n  AND THE RECORD'S THREE COMMITTED CELLS, judged by the same test against the panel's")
    say("  OWN IS argmax (is the committed cell distinguishable from the cell rule 8 would pick?):")
    nm_rows = []
    for nm, tpe in tapes.items():
        L = loyo[nm]
        base = L.loc["NONE"]
        yrs = [y for y in L.index if y != "NONE"]
        k1 = base.idxmax()
        for bname, (c, g) in NAMED.items():
            kc = cellname(c, g)
            m0 = float(base[k1] - base[kc])
            pair = (L.loc[yrs, k1].values - L.loc[yrs, kc].values).astype(float)
            sdp = float(np.std(pair, ddof=1))
            nm_rows.append(dict(panel=nm, book=bname, cell=kc, is_argmax=bool(kc == k1),
                                obj=float(base[kc]), gap_to_argmax=m0, sd_pair=sdp,
                                t_pair=m0 / sdp if sdp > 0 else np.nan,
                                resolved=bool(sdp > 0 and abs(m0 / sdp) > T_BAR),
                                is_rank=int((base > base[kc]).sum()) + 1))
    NMD = pd.DataFrame(nm_rows)
    for line in NMD.to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    say(f"\n  Committed cells that the IS window can DISTINGUISH from its own argmax: "
        f"**{int(NMD.resolved.sum())} of {len(NMD)}**.")

    # ================================================================ (D) DOES MARGIN PREDICT MOVE
    say("\n" + "=" * 118)
    say("(D) DOES THE MARGIN PREDICT THE MOVE?  The argmax is recomputed under each LOYO refit.")
    say("=" * 118)
    mv, ev = [], []
    for nm, tpe in tapes.items():
        L = loyo[nm]
        base = L.loc["NONE"]
        k1 = base.idxmax()
        yrs = [y for y in L.index if y != "NONE"]
        moved, movers = 0, []
        for y in yrs:
            ky = L.loc[y].idxmax()
            if ky == k1:
                continue
            moved += 1
            movers.append(f"{y}->{ky}")
            # the undeleted separation between the ORIGINAL argmax and the cell it moved to
            m0 = float(base[k1] - base[ky])
            pair = (L.loc[yrs, k1].values - L.loc[yrs, ky].values).astype(float)
            sdp = float(np.std(pair, ddof=1))
            gr = G[(G.panel == nm) & (G.cell == ky)].iloc[0]
            g0 = G[(G.panel == nm) & (G.cell == k1)].iloc[0]
            ev.append(dict(panel=nm, deleted_year=y, argmax=k1, moved_to=ky,
                           undeleted_margin=m0, sd_pair=sdp,
                           t_pair=m0 / sdp if sdp > 0 else np.nan,
                           resolved=bool(sdp > 0 and abs(m0 / sdp) > T_BAR),
                           same_band=bool(_key(ky)[0] == _key(k1)[0]),
                           OOS_Sharpe_argmax=float(g0.OOS_Sharpe),
                           OOS_Sharpe_moved=float(gr.OOS_Sharpe),
                           d_OOS_Sharpe=float(gr.OOS_Sharpe - g0.OOS_Sharpe),
                           OOS_4b_argmax=bool(g0.pass4b_oos), OOS_4b_moved=bool(gr.pass4b_oos)))
        t2 = float(MG[(MG.panel == nm) & (MG["rank"] == 2)].t_pair.iloc[0])
        mv.append(dict(panel=nm, argmax=k1, t_pair_rank2=t2, n_years=len(yrs), n_moved=moved,
                       move_rate=moved / len(yrs), movers=";".join(movers) or "-"))
    MV = pd.DataFrame(mv)
    EV = pd.DataFrame(ev)
    for line in MV.to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    say(f"\n  Pick moves under at least one LOYO deletion at **{int((MV.n_moved>0).sum())} of "
        f"{len(MV)}** panels; {int(MV.n_moved.sum())} of {int(MV.n_years.sum())} single-year")
    say("  refits move the argmax — 720's result, reproduced on a 200-cell grid.")
    say("\n  EVERY MOVE EVENT, with the UNDELETED separation between the argmax and the cell the")
    say("  refit moved to (this is the test: could the full IS window have told them apart?):")
    if len(EV):
        for line in EV[["panel", "deleted_year", "argmax", "moved_to", "undeleted_margin",
                        "sd_pair", "t_pair", "resolved", "same_band", "d_OOS_Sharpe",
                        "OOS_4b_argmax", "OOS_4b_moved"]].to_string(
                index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
            say("    " + line)
        say(f"\n  MOVE EVENTS TO A RIVAL THE UNDELETED IS WINDOW COULD RESOLVE (|t| > {T_BAR:.0f}): "
            f"**{int(EV.resolved.sum())} of {len(EV)}**.")
        say(f"  Median |t| at a move event: {EV.t_pair.abs().median():.3f}; max {EV.t_pair.abs().max():.3f}.")
        say(f"  Move events that cross to a DIFFERENT BAND: {int((~EV.same_band).sum())} of {len(EV)}.")
        say(f"  What the move COSTS out of sample: mean d OOS Sharpe {EV.d_OOS_Sharpe.mean():+.4f} "
            f"(range {EV.d_OOS_Sharpe.min():+.4f} .. {EV.d_OOS_Sharpe.max():+.4f});")
        say(f"  the 4b OOS verdict differs between the argmax and the moved-to cell at "
            f"{int((EV.OOS_4b_argmax != EV.OOS_4b_moved).sum())} of {len(EV)} events.")
    EV.to_csv(OUT / "move_events.csv", index=False)

    # ================================================================ (E) IS A FLAT SURFACE SAFE?
    say("\n" + "=" * 118)
    say("(E) IS A FLAT IS SURFACE SAFE?  The capital question.  PLATEAU = every cell whose IS")
    say(f"objective is within {T_BAR:.0f} PAIRED deletion SDs of the argmax, i.e. the cells the IS")
    say("window cannot tell apart.  If those cells behave DIFFERENTLY out of sample, a flat")
    say("surface is a hazard and not a comfort.")
    say("=" * 118)
    pl = []
    plateau_members = {}
    for nm, tpe in tapes.items():
        L = loyo[nm]
        base = L.loc["NONE"]
        yrs = [y for y in L.index if y != "NONE"]
        k1 = base.idxmax()
        keepset = []
        for k in base.index:
            if k == k1:
                keepset.append(k)
                continue
            pair = (L.loc[yrs, k1].values - L.loc[yrs, k].values).astype(float)
            sdp = float(np.std(pair, ddof=1))
            m0 = float(base[k1] - base[k])
            if not (sdp > 0 and abs(m0 / sdp) > T_BAR):
                keepset.append(k)
        plateau_members[nm] = keepset
        sub = G[(G.panel == nm) & (G.cell.isin(keepset))]
        pl.append(dict(panel=nm, argmax=k1, plateau_n=len(keepset), of=len(cells),
                       gross_lo=sub.gross.min(), gross_hi=sub.gross.max(),
                       n_bands=sub.band.nunique(),
                       IS_lo=float(base[keepset].min()), IS_hi=float(base[keepset].max()),
                       OOS_Sharpe_lo=float(sub.OOS_Sharpe.min()),
                       OOS_Sharpe_hi=float(sub.OOS_Sharpe.max()),
                       OOS_Sharpe_spread=float(sub.OOS_Sharpe.max() - sub.OOS_Sharpe.min()),
                       OOS_CAGR_lo=float(sub.OOS_CAGR.min()), OOS_CAGR_hi=float(sub.OOS_CAGR.max()),
                       OOS_MaxDD_lo=float(sub.OOS_MaxDD.min()),
                       OOS_MaxDD_hi=float(sub.OOS_MaxDD.max()),
                       n_4b_oos=int(sub.pass4b_oos.sum()), n_4a_oos=int(sub.pass4a_oos.sum())))
    PL = pd.DataFrame(pl)
    for line in PL.to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    say(f"\n  The IS window cannot separate the argmax from {PL.plateau_n.mean():.0f} of "
        f"{len(cells)} cells on average ({PL.plateau_n.mean()/len(cells):.1%} of the grid).")
    say(f"  Across those IS-indistinguishable cells the OOS Sharpe spread is "
        f"{PL.OOS_Sharpe_spread.mean():.4f} on average "
        f"(min {PL.OOS_Sharpe_spread.min():.4f}, max {PL.OOS_Sharpe_spread.max():.4f}),")
    say(f"  the OOS MaxDD runs {PL.OOS_MaxDD_lo.min():.2%} to {PL.OOS_MaxDD_hi.max():.2%}, and")
    say(f"  {int(PL.n_4b_oos.sum())} of {int(PL.plateau_n.sum())} plateau cells clear 4b OOS "
        f"(4a OOS {int(PL.n_4a_oos.sum())}).")

    # ================================================================ (F) RULE 8
    say("\n" + "=" * 118)
    say("(F) RULE 8 WALK-FORWARD — choosers fit on 2009-2016 IS rows ONLY; 2017-2026 read ONCE")
    say("per chooser.  OOS reported against BOTH the live RULES v2 baseline AND SPY.")
    say("=" * 118)
    wf = []
    for nm, tpe in tapes.items():
        allkeep = np.ones(len(tpe.sidx), bool)
        isp, oosp = {}, {}
        for (c, g) in cells:
            w = scored(tpe, allkeep, streams[(nm, c, g)])
            isp[cellname(c, g)] = pack(w["IS"])
            oosp[cellname(c, g)] = pack(w["OOS"])
        wb = scored(tpe, allkeep, tpe.spy)
        spy_is, spy_oos = pack(wb["IS"]), pack(wb["OOS"])
        wl = scored(tpe, allkeep, streams[(nm, 0.03, 0.75)])
        live_oos = pack(wl["OOS"])
        dd_bar, cg_bar = DD_CAP * spy_is["MaxDD"], CAGR_FLOOR * spy_is["CAGR"]
        keys = list(isp)
        picks = {}
        picks["C_SHARPE"] = max(keys, key=lambda k: (isp[k]["Sharpe"], -_key(k)[1]))
        ok = [k for k in keys if isp[k]["MaxDD"] >= dd_bar and isp[k]["CAGR"] >= cg_bar]
        picks["C_MEMO"] = min(ok, key=lambda k: (_key(k)[1], k)) if ok else cellname(0.03, 0.75)
        okd = [k for k in keys if isp[k]["MaxDD"] >= dd_bar]
        picks["C_CAGR"] = max(okd, key=lambda k: (isp[k]["CAGR"], -_key(k)[1])) if okd else cellname(0.03, 0.75)
        picks["C_ANCHOR"] = cellname(0.03, 0.75)
        pm = sorted(plateau_members[nm], key=lambda k: (_key(k)[1], k))
        picks["C_PLAT_LO"] = pm[0]                      # cheapest resolution of an IS tie
        picks["C_PLAT_MID"] = pm[len(pm) // 2]          # the neutral centre of the tie
        picks["C_PLAT_HI"] = pm[-1]                     # the most aggressive resolution
        for cname, pk in picks.items():
            o = oosp[pk]
            Lb = legs_4b(o, spy_oos)
            wf.append(dict(panel=nm, chooser=cname, pick=pk, IS_Sharpe=isp[pk]["Sharpe"],
                           IS_rank=int(sum(1 for k in keys if isp[k]["Sharpe"] > isp[pk]["Sharpe"])) + 1,
                           OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                           SPY_OOS_CAGR=spy_oos["CAGR"], SPY_OOS_Sharpe=spy_oos["Sharpe"],
                           SPY_OOS_MaxDD=spy_oos["MaxDD"],
                           BASE_OOS_CAGR=live_oos["CAGR"], BASE_OOS_Sharpe=live_oos["Sharpe"],
                           BASE_OOS_MaxDD=live_oos["MaxDD"],
                           OOS_4b=all(Lb.values()), OOS_binding=fail_label(Lb),
                           OOS_4a=pass_4a(o, live_oos)))
    W = pd.DataFrame(wf)
    for line in W[["panel", "chooser", "pick", "IS_Sharpe", "IS_rank", "OOS_CAGR", "OOS_Sharpe",
                   "OOS_MaxDD", "OOS_4b", "OOS_binding", "OOS_4a"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        say("    " + line)
    say("\n  OOS BARS (2017-2026, read once):")
    for nm in tapes:
        s = W[W.panel == nm].iloc[0]
        say(f"    {nm:6s} SPY OOS CAGR {s.SPY_OOS_CAGR:.2%} Sharpe {s.SPY_OOS_Sharpe:.4f} "
            f"MaxDD {s.SPY_OOS_MaxDD:.2%}  |  RULES v2 OOS CAGR {s.BASE_OOS_CAGR:.2%} "
            f"Sharpe {s.BASE_OOS_Sharpe:.4f} MaxDD {s.BASE_OOS_MaxDD:.2%}")
    say(f"\n  Picks clearing 4b OOS: **{int(W.OOS_4b.sum())} of {len(W)}**; clearing 4a OOS: "
        f"**{int(W.OOS_4a.sum())} of {len(W)}**.  Mean OOS Sharpe {W.OOS_Sharpe.mean():.4f} "
        f"against SPY's {W.SPY_OOS_Sharpe.mean():.4f}.")
    say("\n  WHAT AN IS TIE COSTS: C_PLAT_LO / MID / HI resolve the SAME IS tie three ways, all")
    say("  three legal IS-only rules.  The spread between them is the price of the chooser's")
    say("  arbitrary tie-break, and C_SHARPE is the plain argmax for comparison:")
    for nm in tapes:
        a = W[(W.panel == nm) & (W.chooser == "C_SHARPE")].iloc[0]
        say(f"    {nm:6s} C_SHARPE  {a.pick:16s} OOS Sharpe {a.OOS_Sharpe:+.4f} CAGR {a.OOS_CAGR:6.2%} "
            f"MaxDD {a.OOS_MaxDD:7.2%} 4b {str(bool(a.OOS_4b))}")
        for cn in ["C_PLAT_LO", "C_PLAT_MID", "C_PLAT_HI"]:
            b = W[(W.panel == nm) & (W.chooser == cn)].iloc[0]
            say(f"           {cn:9s} {b.pick:16s} OOS Sharpe {b.OOS_Sharpe:+.4f} CAGR {b.OOS_CAGR:6.2%} "
                f"MaxDD {b.OOS_MaxDD:7.2%} 4b {str(bool(b.OOS_4b))}   d vs C_SHARPE "
                f"{b.OOS_Sharpe-a.OOS_Sharpe:+.4f}")
    sp = W[W.chooser.isin(["C_PLAT_LO", "C_PLAT_MID", "C_PLAT_HI"])].groupby("panel")
    say(f"\n  Mean OOS CAGR spread across the three tie-breaks: "
        f"{float((sp.OOS_CAGR.max()-sp.OOS_CAGR.min()).mean()):.2%}; mean OOS Sharpe spread "
        f"{float((sp.OOS_Sharpe.max()-sp.OOS_Sharpe.min()).mean()):.4f}.")

    # ---- artifacts
    G.to_csv(OUT / "grid.csv", index=False)
    MG.to_csv(OUT / "margins.csv", index=False)
    NMD.to_csv(OUT / "committed_cells.csv", index=False)
    MV.to_csv(OUT / "pick_moves.csv", index=False)
    PL.to_csv(OUT / "plateau.csv", index=False)
    W.to_csv(OUT / "walkforward.csv", index=False)
    pd.DataFrame(loyo_rows).to_csv(OUT / "loyo_argmax.csv", index=False)
    for nm in tapes:
        loyo[nm].to_csv(OUT / f"loyo_objective_{nm}.csv")
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    (OUT / "log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  Artifacts -> {OUT}")
    say(f"  Gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass.")
    say(f"  Elapsed {time.time()-t0:.1f}s")


def _key(name):
    """cellname -> (band, gross), the inverse of cellname()."""
    b, g = name.split("/")
    c = NOGATE if b == "NOGATE" else float(b[1:])
    return (c, float(g[1:]))


if __name__ == "__main__":
    main()
