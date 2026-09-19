#!/usr/bin/env python3
"""Idea 1660 (lane C, 2026-09-19): does the BAND's GATE-OUT RATE predict a panel's REALISED
GROSS well enough to RETIRE the BISECTED TWIN?

WHY THIS IDEA.  Idea 1649 (lane C, this morning) reported two panels sitting at in-band shares
0.7051 / 0.5482 and REALISED mean gross 0.5293 / 0.4113 at the SAME target gross 0.75 — ratios
0.7507 and 0.7503, a near-exact proportionality to the target.  If that is a law and not a
coincidence of one cell, then the matched-exposure TWIN — the control every device in this
record is now priced against, and which currently costs a 44-step BISECTION per slice per cell —
is a CLOSED FORM, and the record can stop solving for it.

THE FORM, STATED BEFORE THE RUN.  Under the live RULES v2 convention each in-band name carries
G / N_priced of NAV and gated-out weight goes to CASH (never re-spread).  So the book's TARGET
gross on any row is G * s_t, s_t = n_inband / n_priced.  The claim under test is that the
REALISED mean gross R (which differs from target by intra-period drift and by the NAV
normalisation A/V) is recovered by the target alone:

    FORM A  (the 1649 proportionality, zero runs needed):   R_hat_A = G * mean_slice(s_t)
    FORM B  (the stale-weight refinement, zero runs needed): R_hat_B = mean_slice(G * s_at_last_rebalance)

and, for the twin itself, that an UNGATED equal-weight book asked for target k realises k, so the
twin's solved gross is just k* = R_cell with no bisection at all.  The three ways to build the
SAME control are therefore:

    TWIN_BISECT  k solved by 44-step bisection so realised mean gross == R_cell   (the status quo)
    TWIN_R       k = R_cell                      (no bisection; assumes the twin has no drift)
    TWIN_A       k = G * mean_slice(s_t)         (no runs at all; the full closed form)

The gap TWIN_R - TWIN_BISECT isolates the UNGATED twin's own drift; TWIN_A - TWIN_R isolates the
gate-out formula.  Both are priced as REAL BOOKS, not as gross numbers: a formula that lands the
gross to 3 decimals but moves Sharpe is not a retirement.

THE RETIREMENT BARS, PRE-REGISTERED (no bar is chosen after seeing a number):
    BAR_SHARPE = 0.0089 pp-of-Sharpe — the record's own SMALLEST committed device margin
                 (idea 1617's MAXVOL-vs-twin edge at 10 bps, the number that run called too thin
                 to trade).  A substitution that moves Sharpe by less than the smallest margin the
                 record has ever quoted cannot change any committed verdict.
    BAR_DD     = 2.93 pp — idea 1511's MEASURED paired circular-block bootstrap SE of a MaxDD
                 contrast (LB = 65 blocks, 240 cells).
    RETIRE iff max |dSharpe| < BAR_SHARPE AND max |dMaxDD| < BAR_DD over EVERY published cell at
    the binding 10 bps, on FULL and on OOS, for the substitution being judged.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    DIAL 1  band c in {0.00, 0.01, 0.03, 0.05, 0.10}   0.03 is the LIVE clause-2 value.
    DIAL 2  G    in {0.25, 0.50, 0.75, 1.00}           0.75 is the LIVE value and the
                                                       2026-09-04 KEEP-4b anchor.
    20 cells.  (c = 0.00 is the degenerate no-hysteresis 200d MA gate, kept as the family's edge.)

NOT DIALS, published at every value: PANEL {U56, B136, SMALL}, CADENCE {W, M, Q}, SLICE
{FULL, IS, OOS}, COST {0, 10, 25, 50} bps.  180 (panel, cadence, cell) books, each with three
twins.  COST IS NOT A DIAL: weights are cost-independent so r(c) = r_gross - turnover*c/1e4 is
exact off one run, gated against a fresh 25 bps engine run (G2).  Every verdict is judged at the
protocol's binding 10 bps.

THE QUESTIONS, STATED BEFORE THE RUN:
  Q0 THE FORM.      Residual R - R_hat for FORM A and FORM B at all 180 cells x 3 slices, in pp
                    of NAV.  Published in full; the headline is max |residual|, not the mean.
  Q1 THE TWIN.      Does the closed form reproduce the BISECTED twin as a PRICED BOOK?
                    dSharpe / dCAGR / dMaxDD of TWIN_R and TWIN_A against TWIN_BISECT, every cell,
                    every cost rung, FULL and OOS.  Adjudicated against the pre-registered bars.
  Q2 CAPITAL.       Both KEEP paths (4a vs live RULES v2, 4b vs SPY) at every cell AND every twin,
                    FULL and OOS.  A formula-built twin that changes a KEEP verdict is not a twin.
  Q3 RULE 8.        Choosers fit on warm-up..2016-12-31 ONLY, 2017-2026 read EXACTLY ONCE, each
                    pick read OOS against SPY, the live RULES v2 baseline, and its own three twins
                    (all solved / evaluated on IS rows only, so the twin is legal too).

CHOOSERS (rule 8), over the 20 cells, per panel x cadence:
  C_SHARPE  argmax IS Sharpe.
  C_MEMO    among cells with IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
            the LOWEST-TURNOVER one; else the live cell.  (The 2026-09-03 RECOMMENDATION memo's
            own pre-stated DD-aware admission rule, carried onto this dial unchanged.)
  C_LIVE    the live inheritance, choosing nothing: c = 0.03, G = 0.75.

GATES.  G0 sample >= 10y per panel (rule 1).  G1 fast_run vs engine.backtest, RETURNS and
TURNOVER, on the live cell and on an ungated twin.  G2 the DERIVED 25 bps rung vs a fresh 25 bps
engine run.  G3 the (U56, W, c=0.03, G=0.75) cell replays baseline.rules_v2_weights bit-for-bit.
G4 bisection quality: max |realised(TWIN_BISECT) - R_cell| over every twin.  G5 exactly two tuned
parameters.  G6 no chooser reads a row on or after 2017-01-01 (tested on a HARD-TRUNCATED array).
G7 every cell x slice x cost rung published to CSV.  G8 no leverage / no shorting.  G9 PUBLISHED:
turnover per cell and twin.  G10 PUBLISHED: in-band share and realised gross per cell.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_band-gate-out-rate-predicts-realised-gross_C.py
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

DATE, SLUG = "2026-09-19", "band-gate-out-rate-predicts-realised-gross"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NB = 44                       # bisection halvings: 2^-44 ~ 5.7e-14 on a [0,1] bracket

BANDS = [0.00, 0.01, 0.03, 0.05, 0.10]
GS = [0.25, 0.50, 0.75, 1.00]
CELLS = [(c, g) for c in BANDS for g in GS]
LIVE_CELL = (0.03, 0.75)
CADENCES = ["W", "M", "Q"]
LIVE_CAD = "W"
LIVE_PANEL = "U56"

BAR_SHARPE = 0.0089           # idea 1617's smallest committed device margin
BAR_DD = 0.0293               # idea 1511's measured paired MaxDD-contrast SE (2.93 pp)

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


# ---------------------------------------------------------------- engine-equivalent fast path
def run_cell(rets, C, Cp, reb, frame, g):
    """Hold g * frame on the rebalance schedule, drift between rebalances, gated-out weight to
    0%-yielding cash.  GROSS-of-cost daily returns, turnover, max realised TARGET gross, and the
    realised gross path -- identical semantics to engine.backtest, gated at G1."""
    T, M = rets.shape
    turn = np.zeros(T); out = np.zeros(T); gsum = np.zeros(T)
    curw = np.zeros(M); wsum_max = 0.0
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


class Book:
    """A runnable book: one frame on one tape, with a gross-solve cache."""

    def __init__(self, tape, frame):
        self.tape, self.frame, self.cache = tape, frame, {}

    def at(self, g):
        key = round(float(g), 15)
        if key not in self.cache:
            self.cache[key] = run_cell(*self.tape, self.frame, key)
        return self.cache[key]

    def solve(self, target_mean_gross, lo, hi):
        """Bisect ABSOLUTE target gross in [0, 1] so realised mean gross over [lo:hi) equals
        target.  Realised gross is monotone increasing in g."""
        top = self.at(1.0)
        if float(np.mean(top[3][lo:hi])) < target_mean_gross:
            return 1.0, top, False                       # would need leverage: INFEASIBLE
        a, b = 0.0, 1.0
        for _ in range(NB):
            m = 0.5 * (a + b)
            if float(np.mean(self.at(m)[3][lo:hi])) < target_mean_gross:
                a = m
            else:
                b = m
        g = 0.5 * (a + b)
        return g, self.at(g), True


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


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, spy, live):
    """(4a vs the live book, 4b vs SPY) exactly as PROTOCOL rule 4 words them."""
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > spy["H1"]), H2=bool(h2 > spy["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def net(run, c, lo, hi):
    return run[0][lo:hi] - run[1][lo:hi] * c / 1e4


def devmax(a, b):
    """max |a - b| over rows where BOTH are finite, plus the count of non-finite rows.
    engine.backtest emits NaN on the rows before its first real rebalance; those rows are
    excluded HERE and COUNTED, never silently swallowed."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    bad = int((~m).sum())
    d = float(np.max(np.abs(a[m] - b[m]))) if m.any() else np.nan
    return d, bad


# ---------------------------------------------------------------- panels
class Panel:
    def __init__(self, name, px, cols):
        self.name, self.px, self.cols = name, px, list(cols)
        self.idx = px.index
        q = px[cols]
        self.rets = px[cols].pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.priced = q.notna().values
        self.npriced = self.priced.sum(axis=1).astype(float)
        self.T = len(self.idx)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        self.SL = dict(FULL=(WARMUP, self.T), IS=(WARMUP, self.i_oos), OOS=(self.i_oos, self.T))
        self._band_cache = {}
        self._reb_cache = {}

    def reb(self, cad):
        if cad not in self._reb_cache:
            m = rebalance_mask(self.idx, cad).shift(1, fill_value=False).values.copy()
            m[0] = True
            self._reb_cache[cad] = np.flatnonzero(m)
        return self._reb_cache[cad]

    def frame(self, band):
        """Live RULES v2 band book at gross 1.0, shifted one row so row t carries the close-(t-1)
        decision (engine.backtest's weights.shift(1)).  Row sums are exactly s_t = n_in / n_priced.
        band = None -> UNGATED equal-weight over every priced name (the twin frame, s == 1)."""
        key = band
        if key not in self._band_cache:
            if band is None:
                e = self.priced.astype(float)
            else:
                e = (band_state(self.px[self.cols], band).values & self.priced).astype(float)
            w = np.nan_to_num(np.divide(e, np.where(self.npriced == 0, np.nan, self.npriced)[:, None]),
                              nan=0.0)
            self._band_cache[key] = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
        return self._band_cache[key]

    def tape(self, cad):
        return (self.rets, self.C, self.Cp, self.reb(cad))


def held_target_path(frame, reb, T, g):
    """The TARGET gross actually carried on each row: g * s at the last rebalance, held.
    This is FORM B and costs zero runs."""
    s = frame.sum(axis=1)
    out = np.zeros(T)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        if i1 > i0:
            out[i0:i1] = g * s[i0]
    return out


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1660 (lane C, 2026-09-19) — does the BAND's GATE-OUT RATE predict a panel's REALISED")
    say("GROSS well enough to RETIRE the BISECTED TWIN?")
    say(f"DIALS: band c {BANDS}  x  G {GS}  ->  {len(CELLS)} cells.")
    say(f"NOT DIALS, all published: PANEL [U56, B136, SMALL] x CADENCE {CADENCES} x "
        f"SLICE [FULL, IS, OOS] x COST {COSTS} bps.")
    say("FORM A: R_hat = G * mean(s_t).   FORM B: R_hat = mean(held target path).")
    say("TWINS:  TWIN_BISECT (44-step bisection, status quo) | TWIN_R (k = R_cell) | "
        "TWIN_A (k = G * mean(s_t), zero runs)")
    say(f"PRE-REGISTERED RETIREMENT BARS: |dSharpe| < {BAR_SHARPE} (idea 1617's smallest committed "
        f"device margin), |dMaxDD| < {BAR_DD*100:.2f} pp (idea 1511's measured paired SE).")
    say("=" * 118)

    # ------------------------------------------------------------ data
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS_all = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS_all.pct_change().abs().max()
    scols = [c for c in pxS_all.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"\n  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(scols)} of {len(pxS_all.columns)-1} priced names survive.")

    PANELS = [Panel("U56", pxU, list(pxU.columns)),
              Panel("B136", pxB, list(pxB.columns)),
              Panel("SMALL", pxS_all, scols)]
    for P in PANELS:
        publish(f"TAPE STAMP {P.name}", f"{P.T} rows {P.idx[0].date()}..{P.idx[-1].date()}, "
                                       f"{len(P.cols)} traded columns, OOS from {P.idx[P.i_oos].date()}")
        gate(f"G0 {P.name} sample >= 10 years (rule 1)", round(P.T / 252.0, 2), ">= 10.0",
             P.T / 252.0 >= 10.0)
    gate("G5 exactly two tuned parameters (band c x gross G)",
         f"{len(CELLS)} cells = {len(BANDS)} band rungs x {len(GS)} gross rungs", "2 dials",
         len(CELLS) == 20)
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND. "
        "The headline is a TWIN-minus-TWIN contrast inside one frame on the same names, same days, "
        "same realised exposure, so it is first-order immune; the 4b pass counts are NOT.")

    # ------------------------------------------------------------ G1/G2/G3 gates on the live config
    say("\n  [G1/G2/G3] fast_run vs engine.backtest (returns AND turnover), live cell + ungated twin")
    PU = PANELS[0]
    tU = PU.tape(LIVE_CAD)
    fLive = PU.frame(LIVE_CELL[0])
    fUng = PU.frame(None)
    live_run = run_cell(*tU, fLive, LIVE_CELL[1])
    ung_run = run_cell(*tU, fUng, 0.50)
    WlU = rules_v2_weights(pxU, band=LIVE_CELL[0], gross=LIVE_CELL[1])
    engL = backtest(pxU, WlU, cost_bps=BIND, freq=LIVE_CAD)
    engL25 = backtest(pxU, WlU, cost_bps=25.0, freq=LIVE_CAD)
    e = pd.DataFrame(1.0, index=pxU.index, columns=pxU.columns).where(pxU.notna(), 0.0)
    Wung = 0.50 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    engU = backtest(pxU, Wung, cost_bps=BIND, freq=LIVE_CAD)
    d1r = d1t = 0.0; nbad = 0
    for fast, eng in ((live_run, engL), (ung_run, engU)):
        d, nb = devmax(net(fast, BIND, 0, PU.T), eng["returns"].values); d1r = max(d1r, d); nbad += nb
        d, _ = devmax(fast[1], eng["turnover"].values); d1t = max(d1t, d)
    d2, _ = devmax(net(live_run, 25.0, 0, PU.T), engL25["returns"].values)
    gate("G1 fast_run vs engine.backtest, RETURNS (max |dev|, live cell + ungated twin)",
         f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12", d1t < 1e-12)
    gate("G2 DERIVED 25 bps rung vs a fresh 25 bps engine run (max |dev|)", f"{d2:.3e}", "< 1e-12",
         d2 < 1e-12)
    publish("G1c engine rows EXCLUDED as non-finite (pre-first-rebalance)", f"{nbad} of {2*PU.T}")
    d3, _ = devmax(net(live_run, BIND, WARMUP, PU.T), engL["returns"].values[WARMUP:])
    gate("G3 (U56, W, c=0.03, G=0.75) replays baseline.rules_v2_weights over the SCORED slice",
         f"{d3:.3e}", "< 1e-12", d3 < 1e-12)

    # ------------------------------------------------------------ per-panel reference books
    REF = {}
    for P in PANELS:
        lr = net(run_cell(*P.tape(LIVE_CAD), P.frame(LIVE_CELL[0]), LIVE_CELL[1]), BIND, 0, P.T)
        REF[P.name] = dict(
            LIVE={k: pack(lr[lo:hi]) for k, (lo, hi) in P.SL.items()},
            SPY={k: pack(P.spy[lo:hi]) for k, (lo, hi) in P.SL.items()})
        for k in ("FULL", "IS", "OOS"):
            s, l = REF[P.name]["SPY"][k], REF[P.name]["LIVE"][k]
            say(f"  [{P.name:5s} {k:4s}] SPY {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%}"
                f"  | 4b bars DD {DD_CAP*s['MaxDD']:7.2%}, CAGR {CAGR_FLOOR*s['CAGR']:6.2%}"
                f"  | LIVE RULES v2 {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:7.2%}")

    # ------------------------------------------------------------ the grid
    say(f"\n  [GRID] {len(PANELS)} panels x {len(CADENCES)} cadences x {len(CELLS)} cells = "
        f"{len(PANELS)*len(CADENCES)*len(CELLS)} books, each with 3 twins, 3 slices, 4 cost rungs ...")
    rows, wf_rows = [], []
    gross_dev = 0.0
    wsum_max = 0.0
    infeasible = 0
    for P in PANELS:
        spy_all, live_all = REF[P.name]["SPY"], REF[P.name]["LIVE"]
        for cad in CADENCES:
            tape = P.tape(cad)
            reb = P.reb(cad)
            twin_book = Book(tape, P.frame(None))
            cellpack = {}
            for (c, g) in CELLS:
                fr = P.frame(c)
                run = run_cell(*tape, fr, g)
                wsum_max = max(wsum_max, run[2])
                s_path = fr.sum(axis=1)
                held = held_target_path(fr, reb, P.T, g)
                rec = {}
                for sl, (lo, hi) in P.SL.items():
                    R = float(np.mean(run[3][lo:hi]))
                    hatA = g * float(np.mean(s_path[lo:hi]))
                    hatB = float(np.mean(held[lo:hi]))
                    kB, runB, feasB = (R, twin_book.at(min(R, 1.0)), R <= 1.0)
                    kA, runA, feasA = (hatA, twin_book.at(min(hatA, 1.0)), hatA <= 1.0)
                    kS, runS, feasS = twin_book.solve(R, lo, hi)
                    infeasible += int(not feasS) + int(not feasA) + int(not feasB)
                    gross_dev = max(gross_dev, abs(float(np.mean(runS[3][lo:hi])) - R) if feasS else 0.0)
                    rec[sl] = dict(R=R, hatA=hatA, hatB=hatB, s=float(np.mean(s_path[lo:hi])),
                                   kS=kS, kB=kB, kA=kA, feasS=feasS,
                                   runs=dict(CELL=run, TWIN_BISECT=runS, TWIN_R=runB, TWIN_A=runA))
                    for cost in COSTS:
                        base = dict(panel=P.name, cadence=cad, band=c, gross=g, slice=sl, cost_bps=cost,
                                    realised_gross=R, s_mean=rec[sl]["s"], hatA=hatA, hatB=hatB,
                                    resid_A_pp=(R - hatA) * 100, resid_B_pp=(R - hatB) * 100,
                                    k_bisect=kS, k_R=kB, k_A=kA, twin_feasible=feasS)
                        ref = None
                        for nm, rn in rec[sl]["runs"].items():
                            rr = net(rn, cost, lo, hi)
                            k4a, k4b, m, h1, h2, legs = keep_paths(rr, spy_all[sl], live_all[sl])
                            turn = float(np.sum(rn[1][lo:hi]) * 252 / (hi - lo))
                            row = dict(base, book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                       MaxDD=m["MaxDD"], H1=h1, H2=h2, turnover=turn,
                                       keep4a=k4a, keep4b=k4b,
                                       leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                       leg_CAGR=legs["CAGR"])
                            if nm == "TWIN_BISECT":
                                ref = row
                            rows.append(row)
                        for row in rows[-4:]:
                            row["dSharpe_vs_bisect"] = row["Sharpe"] - ref["Sharpe"]
                            row["dCAGR_vs_bisect"] = row["CAGR"] - ref["CAGR"]
                            row["dMaxDD_vs_bisect"] = row["MaxDD"] - ref["MaxDD"]
                cellpack[(c, g)] = rec
                # bound memory: the bisection cache holds ~44 full run tuples per solve and is
                # never reused ACROSS cells (each cell targets a different realised gross).  The
                # runs actually needed are already referenced by `rec`.
                twin_book.cache = {k: v for k, v in twin_book.cache.items() if k == 1.0}

            # ---------------- rule 8 walk-forward for this (panel, cadence)
            loI, hiI = P.SL["IS"]
            loO, hiO = P.SL["OOS"]
            trunc = {}
            for cell in CELLS:
                r_is = net(cellpack[cell]["IS"]["runs"]["CELL"], BIND, loI, hiI)
                trunc[cell] = dict(S=sharpe(r_is), C=cagr(r_is), D=mdd(r_is),
                                   T=float(np.sum(cellpack[cell]["IS"]["runs"]["CELL"][1][loI:hiI])
                                           * 252 / (hiI - loI)))
            spy_is = spy_all["IS"]
            picks = {"C_SHARPE": max(CELLS, key=lambda c: trunc[c]["S"])}
            adm = [c for c in CELLS if trunc[c]["D"] >= DD_CAP * spy_is["MaxDD"]
                   and trunc[c]["C"] >= CAGR_FLOOR * spy_is["CAGR"]]
            picks["C_MEMO"] = min(adm, key=lambda c: trunc[c]["T"]) if adm else LIVE_CELL
            picks["C_LIVE"] = LIVE_CELL
            for cname, cell in picks.items():
                # twins re-solved on IS ROWS ONLY, then held into OOS: the twin is legal too
                isrec = cellpack[cell]["IS"]
                kS_is, kB_is, kA_is = isrec["kS"], isrec["kB"], isrec["kA"]
                for bname, k in (("CELL", None), ("TWIN_BISECT", kS_is), ("TWIN_R", kB_is),
                                 ("TWIN_A", kA_is)):
                    if bname == "CELL":
                        rn = cellpack[cell]["OOS"]["runs"]["CELL"]
                    else:
                        rn = twin_book.at(min(k, 1.0))
                    rr = net(rn, BIND, loO, hiO)
                    k4a, k4b, m, h1, h2, legs = keep_paths(rr, spy_all["OOS"], live_all["OOS"])
                    wf_rows.append(dict(panel=P.name, cadence=cad, chooser=cname, band=cell[0],
                                        gross=cell[1], book=bname, k_IS=(np.nan if k is None else k),
                                        OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                                        OOS_MaxDD=m["MaxDD"], OOS_H1=h1, OOS_H2=h2,
                                        keep4a=k4a, keep4b=k4b,
                                        SPY_OOS_CAGR=spy_all["OOS"]["CAGR"],
                                        SPY_OOS_Sharpe=spy_all["OOS"]["Sharpe"],
                                        SPY_OOS_MaxDD=spy_all["OOS"]["MaxDD"],
                                        LIVE_OOS_Sharpe=live_all["OOS"]["Sharpe"],
                                        LIVE_OOS_MaxDD=live_all["OOS"]["MaxDD"]))
            say(f"    {P.name:5s} {cad}  done  ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(rows)
    W = pd.DataFrame(wf_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    gate("G4 bisection quality: max |realised(TWIN_BISECT) - R_cell|", f"{gross_dev:.3e}", "< 1e-9",
         gross_dev < 1e-9)
    gate("G8 no leverage / no shorting: max realised TARGET gross", f"{wsum_max:.6f}", "<= 1.000001",
         wsum_max <= 1.000001)
    publish("twins needing leverage (INFEASIBLE, reported never clipped silently)", infeasible)
    gate("G7 every cell x slice x cost rung x book published",
         f"{len(G)} rows = {len(PANELS)}x{len(CADENCES)}x{len(CELLS)}x3 slices x{len(COSTS)} costs x4 books",
         f"{len(PANELS)*len(CADENCES)*len(CELLS)*3*len(COSTS)*4}",
         len(G) == len(PANELS) * len(CADENCES) * len(CELLS) * 3 * len(COSTS) * 4)

    # G6: no chooser reads a 2017+ row -- re-derive C_SHARPE on a HARD-TRUNCATED array
    P = PANELS[0]; loI, hiI = P.SL["IS"]
    tape_t = (P.rets[:hiI], P.C[:hiI], P.Cp[:hiI], P.reb(LIVE_CAD)[P.reb(LIVE_CAD) < hiI])
    sh_t, sh_f = {}, {}
    for cell in CELLS:
        fr = P.frame(cell[0])
        rt = run_cell(*tape_t, fr[:hiI], cell[1])
        sh_t[cell] = sharpe(net(rt, BIND, loI, hiI))
        rf = run_cell(*P.tape(LIVE_CAD), fr, cell[1])
        sh_f[cell] = sharpe(net(rf, BIND, loI, hiI))
    d6 = max(abs(sh_t[c] - sh_f[c]) for c in CELLS)
    same = max(CELLS, key=lambda c: sh_t[c]) == max(CELLS, key=lambda c: sh_f[c])
    gate("G6 no chooser reads a 2017+ row (IS Sharpe on a HARD-TRUNCATED tape, max |dev| + same argmax)",
         f"{d6:.3e}, argmax identical={same}", "< 1e-12 and True", d6 < 1e-12 and same)

    # ------------------------------------------------------------ Q0 the form
    say("\n" + "=" * 118)
    say("  [Q0] THE FORM — residual (REALISED mean gross) - (predicted), in pp of NAV")
    q0 = G[(G["book"] == "CELL") & (G["cost_bps"] == BIND)][
        ["panel", "cadence", "band", "gross", "slice", "s_mean", "realised_gross",
         "hatA", "hatB", "resid_A_pp", "resid_B_pp"]].copy()
    q0.to_csv(f"{OUT}.form.csv", index=False)
    for form in ("A", "B"):
        col = f"resid_{form}_pp"
        say(f"      FORM {form}: mean {q0[col].mean():+.4f} pp   mean|.| {q0[col].abs().mean():.4f} pp"
            f"   max|.| {q0[col].abs().max():.4f} pp   at "
            f"{q0.loc[q0[col].abs().idxmax(), ['panel','cadence','band','gross','slice']].to_dict()}")
        publish(f"Q0 FORM {form} residual mean|.| / max|.| (pp of NAV, {len(q0)} cells)",
                f"{q0[col].abs().mean():.4f} / {q0[col].abs().max():.4f}")
    say("      ratio R / (G * s_mean), the 1649 proportionality, by panel:")
    q0["ratio"] = q0["realised_gross"] / (q0["gross"] * q0["s_mean"])
    for p in q0["panel"].unique():
        sub = q0[q0["panel"] == p]["ratio"]
        say(f"        {p:5s}  mean {sub.mean():.6f}  min {sub.min():.6f}  max {sub.max():.6f}")
    say("      by cadence (FORM A |residual|, pp):")
    for cd in CADENCES:
        sub = q0[q0["cadence"] == cd]["resid_A_pp"].abs()
        say(f"        {cd}  mean {sub.mean():.4f}  max {sub.max():.4f}")

    # ------------------------------------------------------------ Q1 the twin, priced
    say("\n  [Q1] THE TWIN, PRICED — TWIN_R and TWIN_A against TWIN_BISECT at the binding 10 bps")
    q1 = G[(G["cost_bps"] == BIND) & (G["book"].isin(["TWIN_R", "TWIN_A"]))]
    verdict_bits = {}
    for bk in ("TWIN_R", "TWIN_A"):
        for sl in ("FULL", "OOS"):
            sub = q1[(q1["book"] == bk) & (q1["slice"] == sl)]
            ms = sub["dSharpe_vs_bisect"].abs().max()
            mdd_ = sub["dMaxDD_vs_bisect"].abs().max()
            mc = sub["dCAGR_vs_bisect"].abs().max()
            ok = bool(ms < BAR_SHARPE and mdd_ < BAR_DD)
            verdict_bits[(bk, sl)] = (ms, mdd_, mc, ok)
            say(f"      {bk:11s} {sl:4s}  max|dSharpe| {ms:.6f} (bar {BAR_SHARPE})   "
                f"max|dMaxDD| {mdd_*100:.4f} pp (bar {BAR_DD*100:.2f})   max|dCAGR| {mc*100:.4f} pp"
                f"   -> {'WITHIN BARS' if ok else 'OUTSIDE BARS'}  ({len(sub)} cells)")
    say("      ALL cost rungs, max |dSharpe| vs TWIN_BISECT:")
    for cost in COSTS:
        for bk in ("TWIN_R", "TWIN_A"):
            sub = G[(G["cost_bps"] == cost) & (G["book"] == bk)]
            say(f"        {cost:5.1f} bps  {bk:11s}  max|dSharpe| "
                f"{sub['dSharpe_vs_bisect'].abs().max():.6f}   max|dMaxDD| "
                f"{sub['dMaxDD_vs_bisect'].abs().max()*100:.4f} pp")

    # ------------------------------------------------------------ Q2 capital
    say("\n  [Q2] CAPITAL — both KEEP paths at every cell and every book, 10 bps")
    q2 = G[G["cost_bps"] == BIND]
    tab = (q2[q2["slice"].isin(["FULL", "OOS"])]
           .groupby(["book", "slice"])[["keep4a", "keep4b"]].sum().astype(int))
    n_each = len(PANELS) * len(CADENCES) * len(CELLS)
    say(f"      pass counts out of {n_each} cells per (book, slice):")
    say(tab.to_string())
    q2.groupby(["book", "slice"])[["keep4a", "keep4b"]].sum().to_csv(f"{OUT}.keep.csv")
    # does a formula twin ever CHANGE a KEEP verdict against the bisected twin?
    piv = q2.pivot_table(index=["panel", "cadence", "band", "gross", "slice"], columns="book",
                         values=["keep4a", "keep4b"], aggfunc="first")
    flips = {}
    for pth in ("keep4a", "keep4b"):
        for bk in ("TWIN_R", "TWIN_A"):
            f = int((piv[(pth, bk)] != piv[(pth, "TWIN_BISECT")]).sum())
            flips[(pth, bk)] = f
            say(f"      VERDICT FLIPS {pth} {bk} vs TWIN_BISECT: {f} of {len(piv)}")
    say(f"      4b FULL-and-OOS passers among CELL books: "
        f"{int((q2[(q2['book']=='CELL')&(q2['slice']=='FULL')]['keep4b'].values & q2[(q2['book']=='CELL')&(q2['slice']=='OOS')]['keep4b'].values).sum())}"
        f" of {n_each}")

    # ------------------------------------------------------------ Q3 rule 8
    say("\n  [Q3] RULE 8 — choosers fit on IS ONLY, 2017-2026 read exactly once")
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"      OOS 4b passes by (chooser, book): ")
    say(W.groupby(["chooser", "book"])[["keep4a", "keep4b"]].sum().to_string())
    say(f"      max |OOS Sharpe(TWIN_A) - OOS Sharpe(TWIN_BISECT)| over choosers: "
        f"{(W[W['book']=='TWIN_A'].set_index(['panel','cadence','chooser'])['OOS_Sharpe'] - W[W['book']=='TWIN_BISECT'].set_index(['panel','cadence','chooser'])['OOS_Sharpe']).abs().max():.6f}")

    # ------------------------------------------------------------ headline verdict
    say("\n" + "=" * 118)
    retireR = all(verdict_bits[("TWIN_R", s)][3] for s in ("FULL", "OOS"))
    retireA = all(verdict_bits[("TWIN_A", s)][3] for s in ("FULL", "OOS"))
    noflipA = flips[("keep4a", "TWIN_A")] == 0 and flips[("keep4b", "TWIN_A")] == 0
    noflipR = flips[("keep4a", "TWIN_R")] == 0 and flips[("keep4b", "TWIN_R")] == 0
    say(f"  RETIREMENT TEST (pre-registered bars, 10 bps, FULL and OOS):")
    say(f"    TWIN_R (k = R_cell, no bisection)        within bars: {retireR}   verdict flips: "
        f"{flips[('keep4a','TWIN_R')]} 4a / {flips[('keep4b','TWIN_R')]} 4b")
    say(f"    TWIN_A (k = G * mean s, zero runs)       within bars: {retireA}   verdict flips: "
        f"{flips[('keep4a','TWIN_A')]} 4a / {flips[('keep4b','TWIN_A')]} 4b")
    vr = ("KEEP (method)" if (retireR and noflipR) else "KILL")
    va = ("KEEP (method)" if (retireA and noflipA) else "KILL")
    say(f"    => TWIN_R substitution {vr};  TWIN_A (full closed form) substitution {va}")
    say("=" * 118)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  GATES {sum(g['pass_'] for g in GATES if g['target'] != 'published, not asserted')}"
        f"/{sum(1 for g in GATES if g['target'] != 'published, not asserted')} PASS.  "
        f"Deterministic, offline, {time.time()-t0:.0f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
