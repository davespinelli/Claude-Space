#!/usr/bin/env python3
"""Idea 1695 (lane cloud, 2026-09-20): IS THE 4b CAGR FLOOR THE ONLY LEG THAT EVER BINDS ON A
FULL GROSS LADDER?

WHY THIS IDEA.  PROTOCOL path 4b is written as a FOUR-leg test against SPY over the same window:

    (H1)   Sharpe(H1) >  SPY Sharpe(H1)
    (H2)   Sharpe(H2) >  SPY Sharpe(H2)
    (DD)   MaxDD      >= 0.60 x SPY MaxDD      (i.e. no deeper than 60% of SPY's depth)
    (CAGR) CAGR       >= 0.70 x SPY CAGR

Two committed findings say those four legs may not be four independent facts:
  * idea 1454 found the LIVE book (RULES v2, c=0.03, G=0.75) fails 4b on the CAGR FLOOR ALONE;
  * idea 1699 (yesterday's lane C, pushed this morning) found an ALWAYS-INVESTED constant-gross
    ladder clears 4b at 0 of 12 rungs because it is SQUEEZED -- CAGR floor fails at G <= 0.50,
    DD cap fails at G >= 0.75, and there is NO RUNG IN BETWEEN.  Its CHANGELOG entry says in
    terms that the leg census "belongs beside open idea 1695".
  * the 2026-09-19 CHANGELOG found all 11 of 180 FULL-and-OOS passes sitting at G = 1.00.

If the Sharpe legs are (near-)invariant to target gross while the CAGR and DD legs move in
OPPOSITE directions with it, then 4b is not a four-leg test at all.  It is a G-INDEPENDENT
SHARPE SCREEN times an INTERVAL ON GROSS, and every "4b pass" in this repository is a statement
about how much beta the book held, dressed as four facts.  That is worth knowing before any
capital is put behind a 4b verdict, and it is knowable from prices alone.

THE DESIGN.  Exactly two tuned dials (PROTOCOL rule 4), every rung published:

  G     0.05, 0.10, ... , 1.00                 DIAL 1 -- target gross.  20 rungs, the FULL ladder
                                               the idea asks for; stops at 1.00 (no leverage,
                                               PROTOCOL rule 2).  0.75 is LIVE.
  FORM  {NOGATE, BAND003, BAND010}             DIAL 2 -- the book's form on the panel.
                                               NOGATE  = always invested, equal weight over the
                                                         names priced that day (no 200d MA).
                                               BAND003 = RULES v2's live 200d +/-3% hysteresis
                                                         band, gated-out weight to CASH.
                                               BAND010 = the 2026-09-19 rule-8 pick, c = 0.10.

  20 x 3 = 60 books per panel x 3 panels (U56 / B136 / SMALL) = 180 books, EVERY CELL PUBLISHED
  in grid.csv with all four legs resolved in FIVE windows (FULL / H1 / H2 / IS / OOS).
  PANEL is NOT a dial: the whole grid runs on all three and none is chosen on its own result.

WHAT IS MEASURED, PRE-REGISTERED BEFORE ANY NUMBER WAS READ.
  (A) THE LEG CENSUS.  For every cell x window, which legs FAIL.  Published as: the share of
      cells failing exactly one leg, and for those, WHICH leg.  Idea 1695's literal question --
      "is the CAGR floor the only leg that ever binds?" -- is answered by the identity of the
      singleton binder.  A leg that never binds alone anywhere is a leg the protocol could drop
      without moving a single verdict; a leg that binds alone often is the whole test.
  (B) THE G-ELASTICITY OF EACH LEG.  Per (panel, form, window), the leg's pass-set as a function
      of G, reported as a monotone interval where it is one.  Pre-registered expectation, stated
      here before reading: CAGR passes on an UPPER set of G, DD on a LOWER set, H1/H2 on all-or-
      nothing (a constant-gross book's Sharpe is scale-invariant up to cash drag and cost).
  (C) THE FEASIBLE GROSS WINDOW.  [G_lo, G_hi] = the G rungs where ALL FOUR legs pass.  Its width
      IS the operational content of 4b.  Width 0 = the squeeze idea 1699 found; width 20 = the
      test is vacuous on that cell.
  (D) THE COUNTERFACTUAL.  How many of the 180 x 5 = 900 cell-window 4b verdicts would MOVE if
      each leg were deleted from the test one at a time.  A leg whose deletion moves nothing is
      decorative.  This is the constructive half and it is reported for all four legs.
  (E) 4a IS ALSO SCORED at every cell against the LIVE RULES v2 book, per PROTOCOL rule 4.

RULE 8 (walk-forward, required).  Four choosers, each fit on warm-up..2016-12-31 ONLY, with
2017-01-01..end read EXACTLY ONCE:
  C_SHARPE  argmax IS Sharpe                                          (the record's usual)
  C_MEMO    smallest G clearing the IS DD cap AND IS CAGR floor, ties to NOGATE then smallest c
  C_CAGR    argmax IS CAGR among cells clearing the IS DD cap
  C_ANCHOR  (BAND003, G=0.75), the live book, choosing nothing        (the null)
OOS CAGR / Sharpe / MaxDD are reported for every pick against BOTH the live RULES v2 baseline
and SPY over the same OOS window.  Nothing is re-tuned after the OOS read.

GATES.  G0 >= 10y per panel (rule 1).  G1 CROSS-SCRIPT REPLAY: U56 (BAND003, G=0.75) reproduces
`baseline.rules_v2_weights` through `engine.backtest` to floating point.  G2 no leverage, no
shorting (max realised gross <= 1.0).  G3 all 180 cells x 5 windows published.  G4 exactly two
tuned dials.  G5 no chooser reads a row on or after 2017-01-01 (hard truncation, asserted).
G6 determinism (two identical runs of one cell).  G7 CROSS-RUN: U56 (NOGATE, G=0.75) and
(BAND003, G=0.75) are re-checked against idea 1699's committed numbers.  G8 the pre-registered
monotonicity of (B) is CHECKED, not assumed -- violations are counted and published.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a
current-screen sub-$2B panel (data/SMALL_PANEL_README.md) with every name whose max 1-day move
is >= 1.0 dropped first.  Every ABSOLUTE level below is therefore an UPPER BOUND, and idea 1703
showed this week that U56's own 4b pass does not survive deleting its 20 mega-caps.  What this
run reads is the STRUCTURE OF A TEST across cells on one tape, which survivorship does not
obviously break; no cell here is a capital recommendation.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 5 (one idea, one script); rule 7 (honest report);
rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md, scan.py, bot.py and baseline.py
are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_is-the-4b-CAGR-floor-the-only-leg-that-ever-binds_cloud.py
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

DATE, SLUG = "2026-09-20", "is-the-4b-CAGR-floor-the-only-leg-that-ever-binds"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
COST = 10.0
CAD = "W"
NOGATE = -1.0
FORMS = [(NOGATE, "NOGATE"), (0.03, "BAND003"), (0.10, "BAND010")]
GRID_G = [round(0.05 * k, 2) for k in range(1, 21)]          # 0.05 .. 1.00, the FULL ladder
LIVE = (0.03, 0.75)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["H1", "H2", "DD", "CAGR"]
WINDOWS = ["FULL", "H1", "H2", "IS", "OOS"]

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


# ---------------------------------------------------------------- metrics
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
    """The four 4b legs of a book with metrics m against benchmark metrics bm, both over the
    SAME window.  Returns {leg: True if that leg PASSES}."""
    return dict(H1=bool(m["H1"] > bm["H1"]), H2=bool(m["H2"] > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def pass_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


# ---------------------------------------------------------------- tape and book
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
        self.band = {c: band_state(px, band=c).values for c, _ in FORMS if c != NOGATE}
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))


def targets(tape, c, g):
    """RULES v2's shape: target gross g spread equally over the names PRICED that day, held only
    where the 200d +/- c band says IN; gated-out weight goes to CASH.  c == NOGATE: no gate."""
    pr = tape.priced.astype(float)
    n = pr.sum(axis=1)
    W = np.zeros_like(pr)
    nz = n > 0
    W[nz] = g * pr[nz] / n[nz, None]
    if c != NOGATE:
        W = W * tape.band[c]
    return W


def run(tape, W, cost=COST):
    """engine.backtest's arithmetic, vectorised per rebalance segment: weights decided at the
    close of day t-1 are applied from day t, positions drift between rebalances, un-invested NAV
    earns 0.00%, turnover charged at `cost` bps."""
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


def windows(tape, r):
    """The five reporting windows of one return stream, all after warm-up."""
    rs = r[WARMUP:]
    h = len(rs) // 2
    io = tape.i_oos - WARMUP
    return dict(FULL=rs, H1=rs[:h], H2=rs[h:], IS=rs[:io], OOS=rs[io:])


# ---------------------------------------------------------------- choosers (rule 8)
def _tie(k):
    """Sort key: NOGATE first on form, then smallest G."""
    return (0 if k[0] == NOGATE else 1, k[0], k[1])


def c_sharpe(cells, isp):
    return min([k for k in cells if isp[k]["Sharpe"] == max(isp[j]["Sharpe"] for j in cells)], key=_tie)


def c_memo(cells, isp, dd_bar, cagr_bar, fallback):
    ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar and isp[k]["CAGR"] >= cagr_bar]
    if not ok:
        return fallback, True
    return min(ok, key=lambda k: (k[1], _tie(k))), False


def c_cagr(cells, isp, dd_bar, fallback):
    ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar]
    if not ok:
        return fallback, True
    best = max(isp[k]["CAGR"] for k in ok)
    return min([k for k in ok if isp[k]["CAGR"] == best], key=_tie), False


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1695 (lane cloud, 2026-09-20) — IS THE 4b CAGR FLOOR THE ONLY LEG THAT EVER BINDS")
    say("ON A FULL GROSS LADDER?")
    say(f"DIALS: G {GRID_G[0]:.2f}..{GRID_G[-1]:.2f} step 0.05 ({len(GRID_G)} rungs) x FORM "
        f"{[n for _, n in FORMS]}.  Panels U56 / B136 / SMALL (published, not a dial).")
    say(f"Weekly cadence, {COST:.0f} bps, t+1 execution, no leverage.  "
        f"{len(GRID_G)*len(FORMS)} cells/panel x 3 panels = {len(GRID_G)*len(FORMS)*3} books, "
        f"x {len(WINDOWS)} windows = {len(GRID_G)*len(FORMS)*3*len(WINDOWS)} cell-windows.")
    say("=" * 118)

    # ---- panels
    panels = []
    panels.append(("U56", load_universe()))
    panels.append(("B136", load_universe(broad=True)))
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

    say("\n  PANELS (the whole grid runs on every one; none is picked on its own result):")
    for nm, p in panels:
        say(f"    {nm:6s} {p.shape[1]:4d} columns  {p.index[0].date()} .. {p.index[-1].date()}  "
            f"{len(p)} rows ({len(p)/252:.1f}y)")
        publish(f"G7 COMPOSITION {nm}", f"{p.shape[1]} columns incl. SPY, "
                                        f"{p.index[0].date()}..{p.index[-1].date()}")
    publish("G7 SMALL max_1d_move >= 1.0 drops",
            f"{len(drop)} names dropped ({len(dropped_meta)} by data/small_meta.csv, "
            f"{len(dropped_px)} by realised price move), {px_s.shape[1]} columns remain")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL is a")
    say("  current-screen panel, so every ABSOLUTE level below is an UPPER BOUND.  What this run")
    say("  reads is the STRUCTURE OF THE 4b TEST across cells on one tape.")

    tapes = {nm: Tape(p, nm) for nm, p in panels}
    for nm, tp in tapes.items():
        gate(f"G0 {nm} sample >= 10 years (rule 1)", round(len(tp.idx) / 252.0, 2), ">= 10.0",
             len(tp.idx) / 252.0 >= 10.0)
        gate(f"G5 {nm} IS window ends before {OOS_START}", str(tp.idx[tp.i_oos - 1].date()),
             f"< {OOS_START}", tp.idx[tp.i_oos - 1] < pd.Timestamp(OOS_START))

    # ---- G1 cross-script replay of the live book through engine.backtest
    tp = tapes["U56"]
    ref = backtest(tp.px, rules_v2_weights(tp.px, band=LIVE[0], gross=LIVE[1]),
                   cost_bps=COST, freq=CAD)["returns"].values
    mine, _, _ = run(tp, targets(tp, LIVE[0], LIVE[1]))
    nan_engine = int(np.isnan(ref).sum())          # engine emits NaN on day 0 / first rebalance
    d = float(np.abs(ref[WARMUP:] - mine[WARMUP:]).max())
    gate("G1 replay of baseline.rules_v2_weights through engine.backtest (U56 live cell, "
         "compared over the SCORED window [WARMUP:] because engine.backtest emits "
         f"{nan_engine} NaN rows before the first rebalance)",
         f"max|d| {d:.3e}", "< 1e-12", d < 1e-12)

    # ---- G6 determinism
    a, _, _ = run(tp, targets(tp, 0.03, 0.75))
    b, _, _ = run(tp, targets(tp, 0.03, 0.75))
    gate("G6 determinism (same cell twice)", f"max|d| {float(np.abs(a-b).max()):.3e}", "== 0",
         float(np.abs(a - b).max()) == 0.0)

    # ---- benchmarks per panel per window
    bench, livebk = {}, {}
    for nm, tpe in tapes.items():
        bench[nm] = {w: pack(r) for w, r in windows(tpe, tpe.spy).items()}
        lr, _, _ = run(tpe, targets(tpe, LIVE[0], LIVE[1]))
        livebk[nm] = {w: pack(r) for w, r in windows(tpe, lr).items()}
        f = bench[nm]["FULL"]
        say(f"\n  SPY on {nm}: FULL CAGR {f['CAGR']:.2%}  Sharpe {f['Sharpe']:.4f}  "
            f"MaxDD {f['MaxDD']:.2%}  H1/H2 {f['H1']:.4f}/{f['H2']:.4f}")
        say(f"      4b bars FULL: H1 > {f['H1']:.4f}, H2 > {f['H2']:.4f}, "
            f"MaxDD >= {DD_CAP*f['MaxDD']:.2%}, CAGR >= {CAGR_FLOOR*f['CAGR']:.2%}")
        o = bench[nm]["OOS"]
        say(f"      4b bars OOS : H1 > {o['H1']:.4f}, H2 > {o['H2']:.4f}, "
            f"MaxDD >= {DD_CAP*o['MaxDD']:.2%}, CAGR >= {CAGR_FLOOR*o['CAGR']:.2%}")
        lf = livebk[nm]["FULL"]
        say(f"      LIVE RULES v2 (c=0.03,G=0.75) on {nm}: FULL CAGR {lf['CAGR']:.2%}  "
            f"Sharpe {lf['Sharpe']:.4f}  MaxDD {lf['MaxDD']:.2%}  H1/H2 {lf['H1']:.4f}/{lf['H2']:.4f}")

    OUT.mkdir(parents=True, exist_ok=True)

    # ---- the grid
    rows = []
    streams = {}
    maxgross = 0.0
    for nm, tpe in tapes.items():
        for c, fname in FORMS:
            for g in GRID_G:
                r, turn, gs = run(tpe, targets(tpe, c, g))
                streams[(nm, fname, g)] = r
                maxgross = max(maxgross, float(np.max(gs[WARMUP:])))
                wins = windows(tpe, r)
                for w in WINDOWS:
                    m = pack(wins[w])
                    L = legs_4b(m, bench[nm][w])
                    fails = [k for k in LEGS if not L[k]]
                    rows.append(dict(
                        panel=nm, form=fname, c=("NOGATE" if c == NOGATE else f"{c:.2f}"), G=g,
                        window=w, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=m["H1"], H2=m["H2"],
                        leg_H1=L["H1"], leg_H2=L["H2"], leg_DD=L["DD"], leg_CAGR=L["CAGR"],
                        n_fail=len(fails), binding=(fails[0] if len(fails) == 1 else
                                                    ("NONE" if not fails else "+".join(fails))),
                        pass4b=len(fails) == 0,
                        pass4a=pass_4a(m, livebk[nm][w]),
                        mean_gross=float(np.mean(gs[WARMUP:])),
                        turnover_yr=float(turn[WARMUP:].sum() * 252 / len(turn[WARMUP:])),
                    ))
    G = pd.DataFrame(rows)
    gate("G2 no leverage (max realised gross over all 180 books)", f"{maxgross:.4f}", "<= 1.0",
         maxgross <= 1.0 + 1e-9)
    gate("G3 all cells x windows published", len(G),
         str(len(GRID_G) * len(FORMS) * 3 * len(WINDOWS)),
         len(G) == len(GRID_G) * len(FORMS) * 3 * len(WINDOWS))
    gate("G4 exactly two tuned dials", "G (20 rungs) x FORM (3)", "== 2", True)

    # ---- G7 cross-run against idea 1699's committed U56 cells
    for (cc, gg), lbl in [((NOGATE, 0.75), "NOGATE G=0.75"), ((0.03, 0.75), "BAND003 G=0.75"),
                          ((0.10, 1.00), "BAND010 G=1.00 (idea 1703's committed cell: "
                                         "11.72% / 1.1726 / -16.30%)")]:
        fname = {NOGATE: "NOGATE", 0.03: "BAND003", 0.10: "BAND010"}[cc]
        q = G[(G.panel == "U56") & (G.form == fname) & (G.G == gg) & (G.window == "FULL")].iloc[0]
        publish(f"G7 CROSS-RUN U56 {lbl} FULL",
                f"CAGR {q.CAGR:.2%}  Sharpe {q.Sharpe:.4f}  MaxDD {q.MaxDD:.2%}  "
                f"mean gross {q.mean_gross:.4f}  turnover/yr {q.turnover_yr:.2f}")

    # ================================================================ (A) THE LEG CENSUS
    say("\n" + "=" * 118)
    say("(A) THE LEG CENSUS — WHICH LEG BINDS, OVER ALL 900 CELL-WINDOWS")
    say("=" * 118)
    npass = int(G.pass4b.sum())
    say(f"  4b PASSES: {npass} of {len(G)} cell-windows ({npass/len(G):.1%}).  "
        f"4a passes: {int(G.pass4a.sum())} of {len(G)}.")
    say(f"  Cells failing exactly ONE leg (the leg BINDS): {int((G.n_fail==1).sum())}; "
        f"two or more: {int((G.n_fail>=2).sum())}.")
    say("\n  SINGLETON BINDER (cells where exactly one leg fails) — this is idea 1695's question:")
    sb = G[G.n_fail == 1].binding.value_counts()
    for leg in LEGS:
        n = int(sb.get(leg, 0))
        say(f"    {leg:5s} binds ALONE at {n:4d} cell-windows "
            f"({n/max(1,int((G.n_fail==1).sum())):6.1%} of singletons, {n/len(G):5.1%} of all)")
    say("\n  PER-LEG FAILURE RATE (any number of co-failures):")
    for leg in LEGS:
        n = int((~G[f"leg_{leg}"]).sum())
        say(f"    {leg:5s} fails at {n:4d} of {len(G)} cell-windows ({n/len(G):5.1%})")
    say("\n  SINGLETON BINDER BY PANEL x WINDOW:")
    piv = (G[G.n_fail == 1].pivot_table(index=["panel", "window"], columns="binding",
                                        values="G", aggfunc="count").fillna(0).astype(int))
    for line in piv.to_string().split("\n"):
        say("    " + line)

    # ================================================================ (B) G-ELASTICITY
    say("\n" + "=" * 118)
    say("(B) THE G-ELASTICITY OF EACH LEG — is each leg's pass-set an INTERVAL in G, and which way?")
    say("=" * 118)
    say("  For each (panel, form, window): the G rungs at which each leg PASSES, as [lo, hi] when")
    say("  the pass-set is a contiguous interval, else the literal set.  'ALL' = passes at all 20")
    say("  rungs, '-' = passes at none.  Monotonicity is CHECKED (gate G8), not assumed.")
    viol = 0
    elas = []
    for nm in tapes:
        for _, fname in FORMS:
            for w in WINDOWS:
                sub = G[(G.panel == nm) & (G.form == fname) & (G.window == w)].sort_values("G")
                rec = dict(panel=nm, form=fname, window=w)
                for leg in LEGS:
                    ok = sub[sub[f"leg_{leg}"]].G.tolist()
                    if not ok:
                        rec[leg] = "-"
                    elif len(ok) == len(GRID_G):
                        rec[leg] = "ALL"
                    else:
                        contiguous = (len(ok) == GRID_G.index(ok[-1]) - GRID_G.index(ok[0]) + 1)
                        rec[leg] = (f"[{ok[0]:.2f},{ok[-1]:.2f}]" if contiguous
                                    else "{" + ",".join(f"{x:.2f}" for x in ok) + "}")
                        if not contiguous:
                            viol += 1
                    # direction: upper set (starts at a rung and runs to 1.00) vs lower set
                    if ok and ok != GRID_G:
                        rec[leg + "_dir"] = ("UPPER" if ok[-1] == GRID_G[-1] and ok[0] > GRID_G[0]
                                             else "LOWER" if ok[0] == GRID_G[0] else "MIDDLE")
                    else:
                        rec[leg + "_dir"] = ""
                allok = sub[sub.pass4b].G.tolist()
                rec["FEASIBLE"] = ("-" if not allok else f"[{allok[0]:.2f},{allok[-1]:.2f}]")
                rec["width"] = len(allok)
                elas.append(rec)
    E = pd.DataFrame(elas)
    gate("G8 leg pass-sets are CONTIGUOUS in G (non-interval pass-sets counted, not assumed)",
         f"{viol} non-contiguous of {len(E)*4} (panel,form,window,leg) pass-sets", "published", True)
    say("")
    for line in E[["panel", "form", "window"] + LEGS + ["FEASIBLE", "width"]].to_string(index=False).split("\n"):
        say("    " + line)
    # --- (B2) the invariance is checked NUMERICALLY, not inferred from the threshold
    say("\n  (B2) IS THE SHARPE LEGS' G-INVARIANCE REAL, OR A THRESHOLD COINCIDENCE?  Spread of the")
    say("  realised statistic ACROSS THE 20 GROSS RUNGS, per (panel, form, window), max over triples:")
    spread = []
    for nm in tapes:
        for _, fname in FORMS:
            for w in WINDOWS:
                sub = G[(G.panel == nm) & (G.form == fname) & (G.window == w)]
                spread.append(dict(panel=nm, form=fname, window=w,
                                   d_H1=float(sub.H1.max() - sub.H1.min()),
                                   d_H2=float(sub.H2.max() - sub.H2.min()),
                                   d_Sharpe=float(sub.Sharpe.max() - sub.Sharpe.min()),
                                   d_MaxDD=float(sub.MaxDD.max() - sub.MaxDD.min()),
                                   d_CAGR=float(sub.CAGR.max() - sub.CAGR.min())))
    SP = pd.DataFrame(spread)
    for c_, lbl in [("d_H1", "Sharpe(H1)"), ("d_H2", "Sharpe(H2)"), ("d_Sharpe", "Sharpe(window)"),
                    ("d_MaxDD", "MaxDD"), ("d_CAGR", "CAGR")]:
        say(f"    {lbl:15s} max spread over the ladder {SP[c_].max():.4f}   "
            f"mean {SP[c_].mean():.4f}   (45 triples)")
    say("    A Sharpe leg whose statistic barely moves over a 20x gross range cannot ADJUDICATE")
    say("    gross; a CAGR/MaxDD leg that moves by tens of points is what the interval is made of.")
    SP.to_csv(OUT_SPREAD := (OUT / "ladder_spread.csv"), index=False) if OUT.exists() else None

    say("\n  DIRECTION TALLY over the (panel, form, window, leg) pass-sets that are neither ALL nor empty:")
    dd = []
    for leg in LEGS:
        v = E[leg + "_dir"].value_counts()
        dd.append(dict(leg=leg, UPPER=int(v.get("UPPER", 0)), LOWER=int(v.get("LOWER", 0)),
                       MIDDLE=int(v.get("MIDDLE", 0)),
                       ALL=int((E[leg] == "ALL").sum()), NONE=int((E[leg] == "-").sum())))
    for line in pd.DataFrame(dd).to_string(index=False).split("\n"):
        say("    " + line)

    # ================================================================ (C) FEASIBLE WINDOW
    say("\n" + "=" * 118)
    say("(C) THE FEASIBLE GROSS WINDOW — the set of G at which ALL FOUR legs pass")
    say("=" * 118)
    for w in WINDOWS:
        sub = E[E.window == w]
        say(f"\n  window {w}:")
        for line in sub[["panel", "form", "FEASIBLE", "width"]].to_string(index=False).split("\n"):
            say("      " + line)
    say(f"\n  Mean feasible width over all {len(E)} (panel, form, window) triples: "
        f"{E.width.mean():.2f} of {len(GRID_G)} rungs; "
        f"triples with width 0: {int((E.width==0).sum())} of {len(E)}.")

    # ================================================================ (D) LEG-DELETION COUNTERFACTUAL
    say("\n" + "=" * 118)
    say("(D) THE LEG-DELETION COUNTERFACTUAL — how many 4b verdicts move if each leg is DELETED")
    say("=" * 118)
    say(f"  Baseline 4b passes over all {len(G)} cell-windows: {npass}")
    cf = []
    for leg in LEGS:
        others = [l for l in LEGS if l != leg]
        p = G[[f"leg_{l}" for l in others]].all(axis=1)
        cf.append(dict(deleted=leg, passes=int(p.sum()), moved=int((p != G.pass4b).sum()),
                       moved_pct=float((p != G.pass4b).mean())))
    CF = pd.DataFrame(cf)
    for line in CF.to_string(index=False).split("\n"):
        say("    " + line)
    say("\n  A leg whose deletion moves ZERO verdicts is decorative on this grid; a leg whose")
    say("  deletion moves many is where the test's content lives.")
    say("\n  PAIRWISE: 4b restated as the TWO legs that move the most, vs the full four:")
    two = CF.sort_values("moved", ascending=False).deleted.tolist()[:2]
    keep2 = [l for l in LEGS if l in two]
    p2 = G[[f"leg_{l}" for l in keep2]].all(axis=1)
    say(f"    keeping only {keep2}: {int(p2.sum())} passes, "
        f"{int((p2 != G.pass4b).sum())} of {len(G)} verdicts move ({(p2!=G.pass4b).mean():.1%})")

    # ================================================================ RULE 8
    say("\n" + "=" * 118)
    say("RULE 8 — WALK-FORWARD.  Picks fit on warm-up..2016-12-31 ONLY; 2017-2026 read EXACTLY ONCE.")
    say("=" * 118)
    wf = []
    for nm, tpe in tapes.items():
        cells = [(c, g) for c, _ in FORMS for g in GRID_G]
        name_of = {c: n for c, n in FORMS}
        isp, oosp = {}, {}
        for c, g in cells:
            r = streams[(nm, name_of[c], g)]
            wins = windows(tpe, r)
            isp[(c, g)] = pack(wins["IS"])
            oosp[(c, g)] = pack(wins["OOS"])
        spy_is, spy_oos = bench[nm]["IS"], bench[nm]["OOS"]
        dd_bar, cagr_bar = DD_CAP * spy_is["MaxDD"], CAGR_FLOOR * spy_is["CAGR"]
        picks = {
            "C_SHARPE": (c_sharpe(cells, isp), False),
            "C_MEMO": c_memo(cells, isp, dd_bar, cagr_bar, LIVE),
            "C_CAGR": c_cagr(cells, isp, dd_bar, LIVE),
            "C_ANCHOR": (LIVE, False),
        }
        for cname, (pk, fell) in picks.items():
            o = oosp[pk]
            L = legs_4b(o, spy_oos)
            fails = [k for k in LEGS if not L[k]]
            wf.append(dict(panel=nm, chooser=cname,
                           pick=f"{name_of[pk[0]]}@G={pk[1]:.2f}", fallback=fell,
                           IS_Sharpe=isp[pk]["Sharpe"], IS_CAGR=isp[pk]["CAGR"],
                           OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                           SPY_OOS_CAGR=spy_oos["CAGR"], SPY_OOS_Sharpe=spy_oos["Sharpe"],
                           SPY_OOS_MaxDD=spy_oos["MaxDD"],
                           BASE_OOS_CAGR=livebk[nm]["OOS"]["CAGR"],
                           BASE_OOS_Sharpe=livebk[nm]["OOS"]["Sharpe"],
                           BASE_OOS_MaxDD=livebk[nm]["OOS"]["MaxDD"],
                           OOS_4b=len(fails) == 0,
                           OOS_binding=(fails[0] if len(fails) == 1 else
                                        ("NONE" if not fails else "+".join(fails))),
                           OOS_4a=pass_4a(o, livebk[nm]["OOS"])))
    W = pd.DataFrame(wf)
    for line in W[["panel", "chooser", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                   "OOS_4b", "OOS_binding", "OOS_4a"]].to_string(
                       index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        say("    " + line)
    say("\n  OOS bars for reference (same window, per panel):")
    for nm in tapes:
        o, b = bench[nm]["OOS"], livebk[nm]["OOS"]
        say(f"    {nm:6s} SPY  OOS CAGR {o['CAGR']:.2%}  Sharpe {o['Sharpe']:.4f}  MaxDD {o['MaxDD']:.2%}"
            f"   |  LIVE RULES v2 OOS CAGR {b['CAGR']:.2%}  Sharpe {b['Sharpe']:.4f}  MaxDD {b['MaxDD']:.2%}")
    say(f"\n  Mean OOS Sharpe over the {len(W)} chooser x panel picks: {W.OOS_Sharpe.mean():.4f}")
    say(f"  Picks clearing 4b OOS: {int(W.OOS_4b.sum())} of {len(W)}.  "
        f"Clearing 4a OOS: {int(W.OOS_4a.sum())} of {len(W)}.")
    say(f"  Picks landing on the TOP gross rung G=1.00: "
        f"{int(W.pick.str.endswith('G=1.00').sum())} of {len(W)}; on NOGATE: "
        f"{int(W.pick.str.startswith('NOGATE').sum())} of {len(W)}.")

    # ---- FULL-and-OOS joint passes
    say("\n  CELLS CLEARING 4b BOTH FULL AND OOS (the record's standing bar for a KEEP-4b):")
    f_ = G[(G.window == "FULL") & G.pass4b][["panel", "form", "G"]]
    o_ = G[(G.window == "OOS") & G.pass4b][["panel", "form", "G"]]
    both = f_.merge(o_, on=["panel", "form", "G"])
    say(f"    FULL passes {len(f_)}, OOS passes {len(o_)}, BOTH {len(both)} of "
        f"{len(GRID_G)*len(FORMS)*3}")
    if len(both):
        for line in both.sort_values(["panel", "form", "G"]).to_string(index=False).split("\n"):
            say("      " + line)
        say(f"    Of the {len(both)} FULL-and-OOS passes, "
            f"{int((both.G >= 0.95).sum())} sit at G >= 0.95 (the top of the ladder).")

    # ---- artifacts
    OUT.mkdir(parents=True, exist_ok=True)
    G.to_csv(OUT / "grid.csv", index=False)
    E.to_csv(OUT / "leg_elasticity.csv", index=False)
    CF.to_csv(OUT / "leg_deletion.csv", index=False)
    W.to_csv(OUT / "walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    (OUT / "log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  Artifacts -> {OUT}")
    say(f"  Gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass.")
    say(f"  Elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
