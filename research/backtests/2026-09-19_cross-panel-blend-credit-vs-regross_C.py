#!/usr/bin/env python3
"""Idea 1649 (lane C, 2026-09-19): is ANY CROSS-PANEL BLEND CREDIT a RE-GROSS in disguise?

WHY THIS IDEA.  Ideas 1645 / 1653 propose splitting NAV between the U56 book and the SMALL-panel
book at CONSTANT TOTAL TARGET GROSS, on the argument that a NAV split "only moves capital" and so
cannot buy drawdown the way every killed device did.  1649 says that argument has a hole in it.
Under the live RULES v2 convention (each in-band name gets gross/N_priced of NAV, gated-out weight
goes to CASH and is never re-spread), a panel whose band gates out MORE OFTEN carries a LOWER
REALISED gross at the same TARGET gross.  So moving NAV between two panels with different gate-out
rates CHANGES REALISED EXPOSURE even though TARGET gross is held fixed.  Any credit the blend shows
over its corners may therefore be the ninth de-gross in costume, not a diversification gain.

THE NULL, STATED BEFORE THE RUN.  1617's method, pointed at the reallocation direction:

    H0:  a blend's entire effect on (CAGR, Sharpe, MaxDD) relative to a single-panel corner is
         reproduced by scaling THAT CORNER by a constant k chosen so the two books carry the SAME
         REALISED MEAN GROSS over the slice being scored.

Rejecting H0 means the blend is a real cross-panel diversification edge.  Failing to reject it
means the record can stop pricing NAV splits one at a time and read 1645 / 1653 as gross claims.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  w in {0.00, 0.25, 0.50, 0.75, 1.00}   NAV share routed to the U56 book; 1-w to SMALL.
                                                w = 1.00 IS the live corner, w = 0.00 the SMALL one.
  DIAL 2  G in {0.50, 0.75, 1.00}               TOTAL TARGET gross.  0.75 is the live value and the
                                                2026-09-04 KEEP-4b anchor value.

  15 cells.  Weight vector for a cell = G * (w * frame_U56 + (1-w) * frame_SMALL), where each
  frame is the LIVE RULES v2 band book (band 0.03) on its own panel at gross 1.0.  Total target
  gross is therefore <= G at every date and EXACTLY G when both panels are fully in band: this is
  a CONSTANT-TOTAL-GROSS NAV split, exactly the object 1645 / 1653 ask about.

  Each cell is paired with TWO matched-exposure twins, one per corner:
      TWIN_U  the w = 1.00 corner scaled to the cell's OWN realised mean gross
      TWIN_S  the w = 0.00 corner scaled to the cell's OWN realised mean gross
  k is solved by bisection on the ABSOLUTE target gross in [0, 1.00] (no leverage) so that the
  twin's realised mean gross equals the cell's to machine precision, over the SLICE BEING SCORED.
  A twin that would need target gross > 1.00 is INFEASIBLE WITHOUT LEVERAGE and is reported as
  such, never silently clipped.

NOT DIALS, published at every value: SLICE {FULL, IS, OOS}, COST {0, 10, 25, 50} bps.
COST IS NOT A DIAL.  Weights are cost-independent, so one run yields every rung exactly:
r(c) = r_gross - turnover * c / 1e4.  Gated against a fresh 25 bps engine run (G2), not assumed.
Every verdict is judged at the protocol's binding 10 bps.

THE FOUR QUESTIONS, STATED BEFORE THE RUN:
  Q0 PREMISE.  Does SMALL's band actually gate out more often than U56's?  Published as in-band
     share and REALISED mean gross per corner.  If the premise is false the idea is moot and says so.
  Q1 RAW CREDIT.  Blend minus each corner at MATCHED TARGET gross (the comparison 1645 / 1653
     would make).  dSharpe / dCAGR / dMaxDD, every cell, every cost rung.
  Q2 MATCHED CREDIT.  Blend minus its REALISED-GROSS-MATCHED twin of the same corner.  H0 predicts
     a dSharpe centred on zero.  The gap between Q1 and Q2 IS the re-gross component.
  Q3 CAPITAL-WORTHY?  Both KEEP paths at every cell and every twin, FULL and OOS, plus rule 8.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE  argmax IS Sharpe over all 15 cells
  C_MEMO    among cells whose IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
            the LOWEST-TURNOVER one; else the live corner.  (The 2026-09-03 RECOMMENDATION memo's
            own pre-registered DD-aware admission rule, carried onto this dial unchanged.)
  C_LIVE    the live inheritance, choosing nothing: w = 1.00, G = 0.75
  Each pick is read OOS against (a) SPY, (b) the live RULES v2 baseline and (c) its OWN matched
  twins, whose k is re-solved on IS GROSS ONLY so the twin is legal too.

GATES.  G0 sample >= 10y (rule 1).  G1 fast_run vs engine.backtest (returns AND turnover) on the
live corner and on a blend cell.  G2 the DERIVED 25 bps rung vs a fresh 25 bps engine run.  G3 the
(w = 1.00, G = 0.75) cell replays baseline.rules_v2_weights bit-for-bit.  G4 the realised-gross
match, max |dev| over all feasible twins.  G5 exactly two tuned parameters (15 cells).  G6 no
chooser reads a row on or after 2017-01-01.  G7 every cell x cost rung published.  G8 no leverage,
no shorting: max realised TARGET gross <= 1.00.  G9 PUBLISHED: turnover per cell and twin.
G10 PUBLISHED: realised mean gross and in-band share per panel and cell.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_cross-panel-blend-credit-vs-regross_C.py
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

DATE, SLUG = "2026-09-19", "cross-panel-blend-credit-vs-regross"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
BAND = 0.03
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NB = 44                       # bisection halvings: 2^-44 ~ 5.7e-14 on a [0,1] bracket

WS = [0.00, 0.25, 0.50, 0.75, 1.00]
GS = [0.50, 0.75, 1.00]
CELLS = [(w, g) for w in WS for g in GS]
LIVE_CELL = (1.00, 0.75)

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


def lab(cell):
    return f"w={cell[0]:.2f} G={cell[1]:.2f}"


# ---------------------------------------------------------------- panels
class Panel:
    """A price panel on the COMMON index, plus the live band book's weight frame."""

    def __init__(self, name, px, cols):
        self.name, self.px, self.cols = name, px, list(cols)
        allc = list(px.columns)
        self.icol = np.array([allc.index(c) for c in self.cols])
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        q = px[self.cols]
        self.priced = q.notna().values
        self.inband = band_state(q, BAND).values & self.priced
        self.reb = self._reb(CADENCE)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))

    def _reb(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)

    def frame(self, M, icol=None):
        """Live RULES v2 band book at gross 1.0, embedded in an M-column frame, shifted one row
        so row t carries the close-(t-1) decision (engine.backtest's weights.shift(1))."""
        e = self.inband.astype(float)
        n = self.priced.sum(axis=1).astype(float)      # N = names PRICED, the live convention
        w = np.nan_to_num(np.divide(e, np.where(n == 0, np.nan, n)[:, None]), nan=0.0)
        W = np.zeros((len(self.idx), M))
        W[:, self.icol if icol is None else icol] = w
        return np.vstack([np.zeros((1, M)), W[:-1]])


def run_cell(rets, C, Cp, reb, frame, g):
    """Hold g * frame on the weekly schedule, drift between rebalances, gated-out weight to
    0%-yielding cash.  Returns GROSS-OF-COST daily returns, turnover, max realised target gross
    and the realised gross path -- identical semantics to engine.backtest, gated at G1."""
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
    """A runnable book: one frame on one (rets, C, Cp, reb) tape, with a gross-solve cache."""

    def __init__(self, tape, frame):
        self.tape, self.frame, self.cache = tape, frame, {}

    def at(self, g):
        key = round(float(g), 15)
        if key not in self.cache:
            self.cache[key] = run_cell(*self.tape, self.frame, key)
        return self.cache[key]

    def solve(self, target_mean_gross, lo, hi):
        """Bisect ABSOLUTE target gross in [0, 1] so realised mean gross over [lo:hi) equals
        target.  Realised gross is monotone increasing in g.  Returns (g, run, feasible)."""
        top = self.at(1.0)
        if float(np.mean(top[3][lo:hi])) < target_mean_gross:
            return 1.0, top, False                      # would need leverage: INFEASIBLE
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

    `engine.backtest` emits NaN on the rows before its first real rebalance (its
    `weights.fillna(0).shift(1)` leaves row 0 NaN, so turnover and the cost charge are NaN
    there).  Those rows are 2 of 4203 and sit 258 rows BEFORE any scored slice begins.  They
    are excluded HERE and COUNTED, never silently swallowed: `max(x, nan)` returns x in
    Python, which would hide a real deviation behind a NaN."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    bad = int((~m).sum())
    d = float(np.max(np.abs(a[m] - b[m]))) if m.any() else np.nan
    return d, bad


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1649 (lane C, 2026-09-19) — is ANY CROSS-PANEL BLEND CREDIT a RE-GROSS in disguise?")
    say(f"DIALS: w (NAV share to U56) {WS}  x  G (TOTAL TARGET gross) {GS}  ->  {len(CELLS)} cells.")
    say(f"NOT DIALS, all published: SLICE [FULL, IS, OOS] x COST {COSTS} bps.  Weekly cadence, "
        f"t+1 execution, live band 0.03 book on each panel, gated-out weight to 0%-yielding CASH.")
    say("H0: a blend's whole effect vs a corner is reproduced by scaling THAT CORNER to the same")
    say("    REALISED mean gross.  Rejecting H0 = a real cross-panel edge; failing = a re-gross.")
    say("=" * 118)

    # ------------------------------------------------------------ data
    pxU_all = load_universe()
    pxS_all = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS_all.pct_change().abs().max()
    inv = [c for c in pxS_all.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"\n  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} of {len(pxS_all.columns)-1} priced names survive.")

    idx = pxU_all.index.intersection(pxS_all.index)
    pxU = pxU_all.loc[idx]
    pxS = pxS_all.loc[idx]
    ucols = [c for c in pxU.columns]                       # SPY IS a U56 constituent (live book holds it)
    scols = inv                                            # SPY on SMALL is a BENCHMARK only, never traded
    say(f"  COMMON TAPE (both panels priced): {idx[0].date()} .. {idx[-1].date()}  {len(idx)} rows "
        f"({len(idx)/252:.1f}y).  U56 {len(ucols)} traded cols, SMALL {len(scols)} traded cols.")
    say("  SURVIVORSHIP (rule 9): U56 is a CURRENT-constituent list and SMALL a CURRENT sub-$2B "
        "screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  The "
        "headline is a BLEND-minus-TWIN contrast inside one tape, over the same names on the same "
        "days at the same realised exposure, so it is first-order immune; the 4b pass counts are not.")

    PU = Panel("U56", pxU, ucols)
    PS = Panel("SMALL", pxS, scols)

    # joined tape: U56 columns then SMALL columns (SPY appears once, as a U56 constituent)
    pxJ = pd.concat([pxU[ucols], pxS[scols]], axis=1)
    assert pxJ.shape[1] == len(ucols) + len(scols) and pxJ.columns.is_unique
    rJ = pxJ.pct_change().fillna(0.0).values
    CJ = np.cumprod(1.0 + rJ, axis=0)
    CpJ = np.vstack([np.ones((1, rJ.shape[1])), CJ[:-1]])
    tapeJ = (rJ, CJ, CpJ, PU.reb)
    tapeU = (PU.rets, PU.C, PU.Cp, PU.reb)
    tapeS = (PS.rets, PS.C, PS.Cp, PS.reb)
    M = pxJ.shape[1]
    iU = np.arange(len(ucols))
    iS = np.arange(len(ucols), M)
    fU_J = PU.frame(M, icol=iU)
    fS_J = PS.frame(M, icol=iS)
    i_oos = PU.i_oos
    T = len(idx)
    spy_r = PU.spy
    SL = dict(FULL=(WARMUP, T), IS=(WARMUP, i_oos), OOS=(i_oos, T))
    say(f"  SLICES: FULL rows {WARMUP}..{T} ({idx[WARMUP].date()}..{idx[-1].date()}), "
        f"IS {WARMUP}..{i_oos} (..{idx[i_oos-1].date()}), OOS {i_oos}..{T} ({idx[i_oos].date()}..).")
    publish("TAPE STAMP", f"{len(idx)} rows {idx[0].date()}..{idx[-1].date()}, "
                          f"U56 {len(ucols)} + SMALL {len(scols)} = {M} traded columns")
    gate("G0 min sample >= 10 years (rule 1)", round(len(idx) / 252.0, 2), ">= 10.0",
         len(idx) / 252.0 >= 10.0)
    gate("G5 exactly two tuned parameters (w x G)",
         f"{len(CELLS)} cells = {len(WS)} w-rungs x {len(GS)} G-rungs", "2 dials", len(CELLS) == 15)

    # ------------------------------------------------------------ G1/G2/G3 gates
    say("\n  [G1/G2/G3] fast_run vs engine.backtest (returns AND turnover), live corner + a blend")
    d1r = d1t = d2 = 0.0
    nbad = 0
    WlU = (rules_v2_weights(pxU[ucols], band=BAND, gross=0.75)
           .reindex(columns=pxJ.columns).fillna(0.0))
    live_run = run_cell(*tapeJ, fU_J, 0.75)
    engL = backtest(pxJ, WlU, cost_bps=BIND, freq=CADENCE)
    engL25 = backtest(pxJ, WlU, cost_bps=25.0, freq=CADENCE)
    WlS = (rules_v2_weights(pxS[scols], band=BAND, gross=0.75)
           .reindex(columns=pxJ.columns).fillna(0.0))
    Wmix = 0.50 * WlU + 0.50 * WlS                        # w=0.50, G=0.75 in engine weights
    mix_run = run_cell(*tapeJ, 0.50 * fU_J + 0.50 * fS_J, 0.75)
    engM = backtest(pxJ, Wmix, cost_bps=BIND, freq=CADENCE)
    for fast, eng, c in ((live_run, engL, BIND), (mix_run, engM, BIND)):
        d, nb = devmax(net(fast, c, 0, T), eng["returns"].values); d1r = max(d1r, d); nbad += nb
        d, nb = devmax(fast[1], eng["turnover"].values); d1t = max(d1t, d)
    d2, _ = devmax(net(live_run, 25.0, 0, T), engL25["returns"].values)
    gate("G1 fast_run vs engine.backtest, RETURNS (max |dev| over finite rows, corner + blend)",
         f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12", d1t < 1e-12)
    gate("G2 DERIVED 25 bps rung vs a fresh 25 bps engine run (max |dev|)", f"{d2:.3e}", "< 1e-12",
         d2 < 1e-12)
    publish("G1c engine rows EXCLUDED as non-finite (pre-first-rebalance, rows 0 and 5 of 4203, "
            "258 rows before the scored sample starts)", f"{nbad} of {2*T}")
    # G3: the (w=1.00, G=0.75) cell IS baseline.rules_v2_weights on U56, bit-for-bit
    engU = backtest(pxU, rules_v2_weights(pxU, band=BAND, gross=0.75), cost_bps=BIND, freq=CADENCE)
    d3, _ = devmax(net(live_run, BIND, 0, T), engU["returns"].values)
    gate("G3 (w=1.00, G=0.75) replays baseline.rules_v2_weights on U56 (max |dev|)", f"{d3:.3e}",
         "< 1e-12", d3 < 1e-12)
    d3b, _ = devmax(net(live_run, BIND, WARMUP, T), engU["returns"].values[WARMUP:])
    gate("G3b same replay over the SCORED slice only (rows 260+), no exclusions", f"{d3b:.3e}",
         "< 1e-12", d3b < 1e-12)

    live_ret = net(live_run, BIND, 0, T)                    # the LIVE baseline return path, 10 bps
    LIVE = {k: pack(live_ret[lo:hi]) for k, (lo, hi) in SL.items()}
    SPY = {k: pack(spy_r[lo:hi]) for k, (lo, hi) in SL.items()}
    for k in ("FULL", "IS", "OOS"):
        say(f"  [{k:4s}] SPY {SPY[k]['CAGR']:7.2%} / {SPY[k]['Sharpe']:.4f} / {SPY[k]['MaxDD']:7.2%}"
            f"   |  4b bars: DD cap {DD_CAP*SPY[k]['MaxDD']:7.2%}, CAGR floor "
            f"{CAGR_FLOOR*SPY[k]['CAGR']:6.2%}   |  LIVE RULES v2 {LIVE[k]['CAGR']:7.2%} / "
            f"{LIVE[k]['Sharpe']:.4f} / {LIVE[k]['MaxDD']:7.2%}")

    # ------------------------------------------------------------ Q0 premise
    say("\n  [Q0] PREMISE: does SMALL's band gate out more often than U56's?")
    ibU = PU.inband.sum(axis=1)[WARMUP:] / np.maximum(PU.priced.sum(axis=1)[WARMUP:], 1)
    ibS = PS.inband.sum(axis=1)[WARMUP:] / np.maximum(PS.priced.sum(axis=1)[WARMUP:], 1)
    cornU = run_cell(*tapeJ, fU_J, 0.75)
    cornS = run_cell(*tapeJ, fS_J, 0.75)
    gU = float(np.mean(cornU[3][WARMUP:])); gS = float(np.mean(cornS[3][WARMUP:]))
    say(f"      in-band share of priced names, FULL mean:  U56 {ibU.mean():.4f}   SMALL {ibS.mean():.4f}")
    say(f"      REALISED mean gross at TARGET 0.75      :  U56 {gU:.4f}   SMALL {gS:.4f}   "
        f"(gap {gU-gS:+.4f})")
    publish("Q0 in-band share U56 / SMALL (FULL)", f"{ibU.mean():.4f} / {ibS.mean():.4f}")
    publish("Q0 realised mean gross at target 0.75, U56 / SMALL", f"{gU:.4f} / {gS:.4f}")
    prem = gS < gU
    say(f"      PREMISE {'HOLDS' if prem else 'FAILS'}: SMALL realises "
        f"{'LESS' if prem else 'MORE OR EQUAL'} gross than U56 at the same target, so a NAV split "
        f"at constant TARGET gross {'DOES' if prem else 'does NOT'} move REALISED exposure.")
    publish("Q0 PREMISE (SMALL realises lower gross than U56 at matched target)", str(bool(prem)))

    # ------------------------------------------------------------ cells + twins
    say("\n  [CELLS] running 15 blend cells and their realised-gross-matched twins ...")
    bookU_J, bookS_J = Book(tapeJ, fU_J), Book(tapeJ, fS_J)
    runs, gross_mean, turn_mean = {}, {}, {}
    for cell in CELLS:
        w, g = cell
        runs[cell] = run_cell(*tapeJ, w * fU_J + (1 - w) * fS_J, g)
        gross_mean[cell] = {k: float(np.mean(runs[cell][3][lo:hi])) for k, (lo, hi) in SL.items()}
        turn_mean[cell] = {k: float(np.sum(runs[cell][1][lo:hi]) * 252 / (hi - lo))
                           for k, (lo, hi) in SL.items()}
    wsum_max = max(runs[c][2] for c in CELLS)
    gate("G8 no leverage / no shorting: max realised TARGET gross", f"{wsum_max:.6f}", "<= 1.000001",
         wsum_max <= 1.000001)

    twins, gapmax, infeas = {}, 0.0, []
    for cell in CELLS:
        for corner, bk in (("U", bookU_J), ("S", bookS_J)):
            for sl, (lo, hi) in SL.items():
                gk, run, feas = bk.solve(gross_mean[cell][sl], lo, hi)
                twins[(cell, corner, sl)] = (gk, run, feas)
                if feas:
                    gapmax = max(gapmax, abs(float(np.mean(run[3][lo:hi])) - gross_mean[cell][sl]))
                else:
                    infeas.append((lab(cell), corner, sl))
    gate("G4 realised-gross match, max |mean_gross(twin) - mean_gross(cell)| over feasible twins",
         f"{gapmax:.3e}", "< 1e-10", gapmax < 1e-10)
    publish("G4b twins INFEASIBLE without leverage (target gross would exceed 1.00)",
            f"{len(infeas)} of {len(CELLS)*2*3}" + (f"  e.g. {infeas[:4]}" if infeas else ""))

    # ------------------------------------------------------------ Q1 / Q2 / Q3 grid
    say("\n  [Q1/Q2/Q3] every cell x cost rung; RAW credit vs the corner, MATCHED credit vs its twin")
    grid = []
    for cell in CELLS:
        w, g = cell
        for sl, (lo, hi) in SL.items():
            for c in COSTS:
                r = net(runs[cell], c, lo, hi)
                spy, live = SPY[sl], LIVE[sl]
                k4a, k4b, m, h1, h2, legs = keep_paths(r, spy, live)
                row = dict(w=w, G=g, cell=lab(cell), slice=sl, cost_bps=c,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           realised_gross=gross_mean[cell][sl], turnover_pa=turn_mean[cell][sl],
                           keep4a=k4a, keep4b=k4b, leg_H1=legs["H1"], leg_H2=legs["H2"],
                           leg_DD=legs["DD"], leg_CAGR=legs["CAGR"])
                for corner, cc in (("U", (1.00, g)), ("S", (0.00, g))):
                    rc = net(runs[cc], c, lo, hi)             # RAW: same TARGET gross
                    row[f"raw_dSharpe_{corner}"] = sharpe(r) - sharpe(rc)
                    row[f"raw_dCAGR_{corner}"] = cagr(r) - cagr(rc)
                    row[f"raw_dMaxDD_{corner}"] = mdd(r) - mdd(rc)
                    gk, trun, feas = twins[(cell, corner, sl)]
                    rt = net(trun, c, lo, hi)                 # MATCHED: same REALISED gross
                    row[f"twin_g_{corner}"] = gk
                    row[f"twin_feasible_{corner}"] = feas
                    row[f"mat_dSharpe_{corner}"] = sharpe(r) - sharpe(rt) if feas else np.nan
                    row[f"mat_dCAGR_{corner}"] = cagr(r) - cagr(rt) if feas else np.nan
                    row[f"mat_dMaxDD_{corner}"] = mdd(r) - mdd(rt) if feas else np.nan
                    tk4a, tk4b, tm, _, _, _ = keep_paths(rt, spy, live)
                    row[f"twin_keep4a_{corner}"] = tk4a if feas else False
                    row[f"twin_keep4b_{corner}"] = tk4b if feas else False
                    row[f"twin_Sharpe_{corner}"] = sharpe(rt) if feas else np.nan
                    row[f"twin_MaxDD_{corner}"] = tm["MaxDD"] if feas else np.nan
                grid.append(row)
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G7 every cell x slice x cost rung published",
         f"{len(G)} rows", f"== {len(CELLS)*3*len(COSTS)}", len(G) == len(CELLS) * 3 * len(COSTS))

    say("\n  FULL SAMPLE @ 10 bps (the binding rung).  'raw' = vs the corner at matched TARGET "
        "gross; 'mat' = vs that corner scaled to the cell's OWN REALISED gross.")
    say("    cell            rgross   CAGR    Sharpe   MaxDD  | rawdS_U  matdS_U | rawdS_S  matdS_S"
        " | 4a 4b")
    f10 = G[(G["slice"] == "FULL") & (G["cost_bps"] == BIND)]
    for _, r in f10.iterrows():
        say(f"    {r['cell']:14s} {r['realised_gross']:.4f} {r['CAGR']:7.2%} {r['Sharpe']:7.4f} "
            f"{r['MaxDD']:7.2%} | {r['raw_dSharpe_U']:+7.4f} {r['mat_dSharpe_U']:+8.4f} | "
            f"{r['raw_dSharpe_S']:+7.4f} {r['mat_dSharpe_S']:+8.4f} | "
            f"{'Y' if r['keep4a'] else '.'}  {'Y' if r['keep4b'] else '.'}")

    # ---- G11: what a constant de-gross does to each axis, MEASURED not assumed
    say("\n  [G11] what a CONSTANT DE-GROSS does to each axis, measured on the two corners:")
    say("       corner at target G vs the SAME corner scaled to a LOWER realised gross.")
    g11 = []
    for corner, fr in (("U56", fU_J), ("SMALL", fS_J)):
        bk = Book(tapeJ, fr)
        lo, hi = SL["FULL"]
        full = bk.at(0.75)
        gm = float(np.mean(full[3][lo:hi]))
        for frac in (0.90, 0.75, 0.50):
            gk, run, feas = bk.solve(frac * gm, lo, hi)
            a, b = net(full, BIND, lo, hi), net(run, BIND, lo, hi)
            g11.append(dict(corner=corner, gross_frac=frac, target_g=gk,
                            dSharpe=sharpe(b) - sharpe(a), dCAGR=cagr(b) - cagr(a),
                            dMaxDD=mdd(b) - mdd(a)))
            say(f"       {corner:6s} realised gross x{frac:.2f} (target {gk:.4f}): "
                f"dSharpe {g11[-1]['dSharpe']:+.4f}  dCAGR {g11[-1]['dCAGR']:+.2%}  "
                f"dMaxDD {g11[-1]['dMaxDD']:+.2%}")
    pd.DataFrame(g11).to_csv(f"{OUT}.degross_axes.csv", index=False)
    mx = max(abs(x["dSharpe"]) for x in g11)
    publish("G11 |dSharpe| of a pure constant de-gross, max over 6 (corner x gross fraction) cells",
            f"{mx:.4f}  -> a de-gross moves CAGR and MaxDD and leaves SHARPE ~fixed, so the "
            f"re-gross component of any credit can only live on the CAGR / MaxDD axes")

    # ---- headline counts: blends only (w strictly interior), at the binding rung
    BL = G[(G["w"] > 0) & (G["w"] < 1)]
    say("\n  [Q1 vs Q2] BLEND cells only (w in {0.25,0.50,0.75}); 9 cells per slice.  RAW = vs the")
    say("  corner at matched TARGET gross.  MATCHED = vs that corner scaled to the cell's OWN")
    say("  REALISED gross.  RE-GROSS SHARE = 1 - matched/raw: how much of the raw credit is bought")
    say("  by carrying less exposure rather than by holding different names.")
    summ = []
    for sl in ("FULL", "IS", "OOS"):
        for c in COSTS:
            b = BL[(BL["slice"] == sl) & (BL["cost_bps"] == c)]
            row = dict(slice=sl, cost_bps=c, n=len(b))
            for corner in ("U", "S"):
                f = b[b[f"twin_feasible_{corner}"]]
                row[f"n_feasible_{corner}"] = len(f)
                for ax, sgn in (("Sharpe", 1), ("CAGR", 1), ("MaxDD", 1)):
                    raw = f[f"raw_d{ax}_{corner}"]; mat = f[f"mat_d{ax}_{corner}"]
                    row[f"raw_beats_{ax}_{corner}"] = int((raw > 0).sum())
                    row[f"mat_beats_{ax}_{corner}"] = int((mat > 0).sum())
                    row[f"mean_raw_d{ax}_{corner}"] = float(raw.mean())
                    row[f"mean_mat_d{ax}_{corner}"] = float(mat.mean())
                    row[f"regross_share_{ax}_{corner}"] = (
                        float(1.0 - mat.mean() / raw.mean()) if abs(raw.mean()) > 1e-12 else np.nan)
                row[f"joint_mat_{corner}"] = int(((f[f"mat_dSharpe_{corner}"] > 0) &
                                                  (f[f"mat_dMaxDD_{corner}"] >= 0)).sum())
            summ.append(row)
    SUM = pd.DataFrame(summ)
    SUM.to_csv(f"{OUT}.summary.csv", index=False)
    for corner, cname in (("U", "U56 corner (the live book)"), ("S", "SMALL corner")):
        say(f"\n    vs {cname}:  slice cost | feasible | dSharpe raw->mat | dCAGR raw->mat "
            f"(re-gross share) | dMaxDD raw->mat (re-gross share)")
        for _, r in SUM.iterrows():
            say(f"      {r['slice']:5s} {r['cost_bps']:5.1f} | {int(r[f'n_feasible_{corner}'])}/9 | "
                f"{r[f'mean_raw_dSharpe_{corner}']:+.4f} -> {r[f'mean_mat_dSharpe_{corner}']:+.4f} "
                f"({int(r[f'raw_beats_Sharpe_{corner}'])}->{int(r[f'mat_beats_Sharpe_{corner}'])} win) | "
                f"{r[f'mean_raw_dCAGR_{corner}']:+.2%} -> {r[f'mean_mat_dCAGR_{corner}']:+.2%} "
                f"({r[f'regross_share_CAGR_{corner}']:+.1%}) | "
                f"{r[f'mean_raw_dMaxDD_{corner}']:+.2%} -> {r[f'mean_mat_dMaxDD_{corner}']:+.2%} "
                f"({r[f'regross_share_MaxDD_{corner}']:+.1%})")

    # ---- the MIXTURE NULL: is the blend's Sharpe above the NAV-weighted average of its corners?
    say("\n  [MIX] the blend's Sharpe against the NAV-WEIGHTED AVERAGE of its two corner Sharpes")
    say("        (a diversification credit if positive) AND against the BETTER corner (what a")
    say("        manager actually gives up).  10 bps, every slice.")
    mix = []
    for sl in ("FULL", "IS", "OOS"):
        lo, hi = SL[sl]
        for cell in CELLS:
            w, g = cell
            if w in (0.0, 1.0):
                continue
            sB = sharpe(net(runs[cell], BIND, lo, hi))
            sU = sharpe(net(runs[(1.00, g)], BIND, lo, hi))
            sS = sharpe(net(runs[(0.00, g)], BIND, lo, hi))
            mix.append(dict(slice=sl, cell=lab(cell), Sharpe=sB, Sharpe_U=sU, Sharpe_S=sS,
                            navavg=w * sU + (1 - w) * sS, d_vs_navavg=sB - (w * sU + (1 - w) * sS),
                            d_vs_best=sB - max(sU, sS)))
            say(f"      {sl:5s} {lab(cell):14s} blend {sB:.4f}  NAV-avg of corners "
                f"{mix[-1]['navavg']:.4f}  -> convexity {mix[-1]['d_vs_navavg']:+.4f}  |  best "
                f"corner {max(sU, sS):.4f} -> {mix[-1]['d_vs_best']:+.4f}")
    MIX = pd.DataFrame(mix)
    MIX.to_csv(f"{OUT}.mixture.csv", index=False)
    say(f"    -> convexity vs the NAV-weighted corner average: {int((MIX['d_vs_navavg']>0).sum())} "
        f"of {len(MIX)} positive, mean {MIX['d_vs_navavg'].mean():+.4f}; against the BETTER corner "
        f"{int((MIX['d_vs_best']>0).sum())} of {len(MIX)} positive, mean {MIX['d_vs_best'].mean():+.4f}.")

    # ---- Q3: 4b passes
    say("\n  [Q3] KEEP paths, all 15 cells, at 10 bps.  4b needs BOTH halves > SPY, MaxDD <= 60% "
        "of SPY's and CAGR >= 70% of SPY's; FULL and OOS both required by rule 8.")
    p4b = []
    for cell in CELLS:
        f = G[(G["cell"] == lab(cell)) & (G["cost_bps"] == BIND)].set_index("slice")
        both = bool(f.loc["FULL", "keep4b"] and f.loc["OOS", "keep4b"])
        tw_both_U = bool(f.loc["FULL", "twin_keep4b_U"] and f.loc["OOS", "twin_keep4b_U"])
        tw_both_S = bool(f.loc["FULL", "twin_keep4b_S"] and f.loc["OOS", "twin_keep4b_S"])
        p4b.append(dict(cell=lab(cell), keep4b_FULL=bool(f.loc["FULL", "keep4b"]),
                        keep4b_OOS=bool(f.loc["OOS", "keep4b"]), keep4b_BOTH=both,
                        keep4a_FULL=bool(f.loc["FULL", "keep4a"]),
                        keep4a_OOS=bool(f.loc["OOS", "keep4a"]),
                        twin_U_keep4b_BOTH=tw_both_U, twin_S_keep4b_BOTH=tw_both_S,
                        CAGR_FULL=f.loc["FULL", "CAGR"], Sharpe_FULL=f.loc["FULL", "Sharpe"],
                        MaxDD_FULL=f.loc["FULL", "MaxDD"], CAGR_OOS=f.loc["OOS", "CAGR"],
                        Sharpe_OOS=f.loc["OOS", "Sharpe"], MaxDD_OOS=f.loc["OOS", "MaxDD"],
                        leg_H1=bool(f.loc["FULL", "leg_H1"]), leg_H2=bool(f.loc["FULL", "leg_H2"]),
                        leg_DD=bool(f.loc["FULL", "leg_DD"]), leg_CAGR=bool(f.loc["FULL", "leg_CAGR"])))
        say(f"    {lab(cell):14s} 4b FULL {'Y' if p4b[-1]['keep4b_FULL'] else '.'} OOS "
            f"{'Y' if p4b[-1]['keep4b_OOS'] else '.'}  (legs FULL H1 "
            f"{'Y' if p4b[-1]['leg_H1'] else '.'} H2 {'Y' if p4b[-1]['leg_H2'] else '.'} DD "
            f"{'Y' if p4b[-1]['leg_DD'] else '.'} CAGR {'Y' if p4b[-1]['leg_CAGR'] else '.'})"
            f"  4a FULL {'Y' if p4b[-1]['keep4a_FULL'] else '.'} OOS "
            f"{'Y' if p4b[-1]['keep4a_OOS'] else '.'}  | its U-twin 4b both "
            f"{'Y' if tw_both_U else '.'} | S-twin {'Y' if tw_both_S else '.'}")
    P4 = pd.DataFrame(p4b)
    P4.to_csv(f"{OUT}.keeppaths.csv", index=False)
    n4b = int(P4["keep4b_BOTH"].sum()); n4a = int((P4["keep4a_FULL"] & P4["keep4a_OOS"]).sum())
    say(f"    -> 4b on BOTH windows: {n4b} of {len(CELLS)} cells.  4a on BOTH: {n4a} of {len(CELLS)}.")
    say(f"    -> of the 4b passers, {int((P4['keep4b_BOTH'] & P4['twin_U_keep4b_BOTH']).sum())} have "
        f"a U-twin that ALSO clears 4b on both windows (a pass the twin reproduces is not a blend edge).")

    # ------------------------------------------------------------ rule 8
    say("\n  [RULE 8] choosers fit on IS rows ONLY, then OOS read EXACTLY ONCE.")
    is10 = G[(G["slice"] == "IS") & (G["cost_bps"] == BIND)].set_index("cell")
    oos10 = G[(G["slice"] == "OOS") & (G["cost_bps"] == BIND)].set_index("cell")
    gate("G6 no chooser reads a row on or after 2017-01-01",
         f"IS slice ends {idx[i_oos-1].date()}, {SL['IS'][1]-SL['IS'][0]} rows", "< 2017-01-01",
         idx[i_oos - 1] < pd.Timestamp(OOS_START))
    picks = {}
    picks["C_SHARPE"] = is10["Sharpe"].idxmax()
    adm = is10[(is10["MaxDD"] >= DD_CAP * SPY["IS"]["MaxDD"]) &
               (is10["CAGR"] >= CAGR_FLOOR * SPY["IS"]["CAGR"])]
    picks["C_MEMO"] = adm["turnover_pa"].idxmin() if len(adm) else lab(LIVE_CELL)
    picks["C_LIVE"] = lab(LIVE_CELL)
    wf = []
    for cname, pick in picks.items():
        cell = [c for c in CELLS if lab(c) == pick][0]
        lo, hi = SL["OOS"]
        r = net(runs[cell], BIND, lo, hi)
        k4a, k4b, m, h1, h2, legs = keep_paths(r, SPY["OOS"], LIVE["OOS"])
        row = dict(chooser=cname, pick=pick, IS_Sharpe=float(is10.loc[pick, "Sharpe"]),
                   n_admissible=len(adm),
                   OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                   OOS_keep4a=k4a, OOS_keep4b=k4b,
                   SPY_OOS_CAGR=SPY["OOS"]["CAGR"], SPY_OOS_Sharpe=SPY["OOS"]["Sharpe"],
                   SPY_OOS_MaxDD=SPY["OOS"]["MaxDD"], LIVE_OOS_CAGR=LIVE["OOS"]["CAGR"],
                   LIVE_OOS_Sharpe=LIVE["OOS"]["Sharpe"], LIVE_OOS_MaxDD=LIVE["OOS"]["MaxDD"])
        # the chooser's own twins, k solved on IS GROSS ONLY (legal), read OOS
        ilo, ihi = SL["IS"]
        for corner, bk in (("U", bookU_J), ("S", bookS_J)):
            gk, trun, feas = bk.solve(gross_mean[cell]["IS"], ilo, ihi)
            rt = net(trun, BIND, lo, hi)
            row[f"twinIS_g_{corner}"] = gk
            row[f"twinIS_feasible_{corner}"] = feas
            row[f"OOS_dSharpe_vs_ISfit_twin_{corner}"] = (m["Sharpe"] - sharpe(rt)) if feas else np.nan
            row[f"OOS_dMaxDD_vs_ISfit_twin_{corner}"] = (m["MaxDD"] - mdd(rt)) if feas else np.nan
            row[f"OOS_twin_Sharpe_{corner}"] = sharpe(rt) if feas else np.nan
        wf.append(row)
        say(f"    {cname:9s} picks {pick:14s} (IS Sharpe {row['IS_Sharpe']:.4f})  -> OOS "
            f"{m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:7.2%}   vs SPY "
            f"{SPY['OOS']['CAGR']:.2%} / {SPY['OOS']['Sharpe']:.4f} / {SPY['OOS']['MaxDD']:.2%}"
            f"   vs LIVE {LIVE['OOS']['CAGR']:.2%} / {LIVE['OOS']['Sharpe']:.4f} / "
            f"{LIVE['OOS']['MaxDD']:.2%}   4a {'Y' if k4a else '.'} 4b {'Y' if k4b else '.'}"
            f"   dS vs IS-fit U-twin {row['OOS_dSharpe_vs_ISfit_twin_U']:+.4f}")
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------ G9 turnover
    say("\n  [G9] turnover (annualised sum of |dw|) per cell, FULL, and the 10 bps drag it implies")
    for cell in CELLS:
        t = turn_mean[cell]["FULL"]
        say(f"      {lab(cell):14s} turnover {t:6.3f} /yr  -> drag @10bps {t*BIND/1e4:6.4%} /yr"
            f"   realised gross {gross_mean[cell]['FULL']:.4f}")
    publish("G9 turnover per cell", "published above, 15 of 15")
    publish("G10 realised mean gross + in-band share", "published above (Q0 and G9 blocks)")

    ok = all(g["pass_"] for g in GATES)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass.")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
