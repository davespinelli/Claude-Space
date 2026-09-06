#!/usr/bin/env python3
"""Idea 302 - "why-is-MONTHLY-the-least-negative-cadence-for-the-de-gross-timing-residual"
(lane cloud, 2026-09-06).

QUEUE wording (verbatim)
------------------------
    "idea 297 found the residual is NOT monotone in cadence on any of three panels:
     W -0.27/-0.31/-0.49, M **-0.18/-0.07/-0.30**, Q -0.75/-0.52/-0.67 pp/yr, and all 6
     non-negative cells in a 216-cell grid are monthly.  Test whether that is a rebalance-PHASE
     artefact (re-run M and Q at all 4/13 phase offsets and read the phase-averaged residual) or
     a real timing effect.  Max 2 params."

What is at stake
----------------
Idea 290 split a DEGROSS book's 0-bps CAGR gap against its RESPREAD twin into

    gap0 = [ constant-leverage cash drag at the cell's own mean leverage c_bar ]   <- exposure
         + [ residual from the TIMING of c_t ]                                     <- gate content

Idea 297 re-read that residual on three panels and found MONTHLY is the least negative rung
everywhere (-0.1835 / -0.0719 / -0.3017 pp/yr on SMALL439 / U56 / B136) against quarterly
(-0.7453 / -0.5165 / -0.6662) and weekly (-0.2726 / -0.3097 / -0.4887), and that every one of
the 6 non-negative cells in its 216-cell grid is monthly.  Read literally that says the timing
content of a de-grossing gate is best at a monthly dial - a claim the project would then carry
into cadence choices.

But idea 187 showed that a single rebalance PHASE is an arbitrary draw fixed by the sample start
date, and that at a 6-week block the phase spread of OOS Sharpe (0.15-0.40) is LARGER than the
whole cadence effect being measured; idea 222 then built the phase-averaged estimator.  Neither
was ever applied to the residual.  Idea 297's M and Q are calendar points: `to_period("M")` and
`to_period("Q")`, i.e. ONE alignment each, month-end and quarter-end.  Month-end and quarter-end
are also the two dates on which everybody else's flows land, so a calendar-anchored dial could
be picking up an alignment effect that has nothing to do with cadence LENGTH.

This run collapses the draw.  It re-runs the residual at the two BLOCK cadences of matching
length - 4W (4 weekly phases) and 13W (13 weekly phases) - at EVERY phase, and reads the
phase-averaged residual beside idea 297's calendar points.

Cadence points (5), every one reported
--------------------------------------
    W       weekly, k=1, ONE phase.  Negative control: zero phase freedom must produce zero
            averaging effect.  Reproduces idea 297's W column exactly.
    CAL-M   calendar month-end (`to_period("M")`).  IDEA 297's M - the incumbent.
    CAL-Q   calendar quarter-end (`to_period("Q")`).  IDEA 297's Q - the incumbent.
    4W      4-week block, phases 0..3.   The block twin of CAL-M.
    13W     13-week block, phases 0..12. The block twin of CAL-Q.
    => 1 + 1 + 1 + 4 + 13 = 20 phase-runs per cell.

Two collapses, kept apart on purpose (idea 222's distinction)
-------------------------------------------------------------
    PH0     phase 0 only - what the record reports.
    MEANPH  the mean ACROSS PHASES of each phase's own statistic.  The honest expectation of
            drawing a phase at random, and THE estimator for every claim below.  At a k=1 point
            (W, CAL-M, CAL-Q) it is identically PH0.
    BLEND-DR (mean of the k phase RETURN series) is reported for the level columns only, as the
            implementable book; it carries a k-growing diversification bonus and is NEVER used
            to read the residual's cadence shape.

Pre-registered hypotheses (bars fixed before any number was read)
-----------------------------------------------------------------
The published M-minus-Q gap this run is testing is GAP_PUB = M - Q from idea 297's committed
decomp.csv, FULL window, mean over the 12 (gate x band) cells per panel:
        SMALL439 +0.5618,  U56 +0.4446,  B136 +0.3645 pp/yr.

A1  PHASE SPREAD >= EFFECT.  For each panel, the RANGE (max-min over phases) of the panel-mean
    residual at 13W, and at 4W, against GAP_PUB.  Declared reading: the calendar ordering is a
    DRAW rather than an estimate if range(13W) >= GAP_PUB on at least 2 of 3 panels.

A2  THE GAP SURVIVES AVERAGING.  MEANPH mean residual at 4W minus at 13W, per panel, against
    GAP_PUB.  Declared bar: the cadence effect is REAL if that phase-averaged gap is at least
    0.5 * GAP_PUB on each of the three panels; it is largely a phase/calendar artefact if it
    comes in under 0.5 * GAP_PUB on at least 2 of 3 panels.

A3  CALENDAR RANK.  Insertion rank of CAL-M's panel-mean residual among the 4 phase values of
    4W, and of CAL-Q's among the 13 of 13W (rank 1 = least negative).  Declared reading:
    calendar luck if CAL-M lands in the top half of its 4W phases on >= 2 panels AND CAL-Q lands
    in the bottom half of its 13W phases on >= 2 panels.

A4  THE NON-NEGATIVE CELLS.  Idea 297's 6 non-negative FULL-window cells are all monthly.  Count
    non-negative cells (of 36 per cadence point: 3 panels x 2 gates x 6 bands) at MEANPH-4W and
    MEANPH-13W, and count how many of the 4W ones are non-negative at EVERY one of their 4
    phases.  Declared reading: the sign anomaly is a phase draw if no 4W cell is non-negative at
    all 4 phases.

A5  ESTIMATOR WALK-FORWARD (rule 8, applied to the estimator itself).  Fit each cell's residual
    on IS (<= 2016-12-31) two ways - PH0 and MEANPH - and predict its OWN OOS (2017-) MEANPH
    residual.  Report MAE for each against the naive zero.  Declared bar: phase averaging is the
    better estimator if MEANPH's OOS MAE is below PH0's on at least 2 of 3 panels.

Controls, asserted before any new number is read
------------------------------------------------
  [a] ENGINE EQUIVALENCE.  The vectorised backtester used here vs `engine.backtest` on 6 books
      (one per panel x construction) at W and CAL-M: max |return diff| must be < 1e-12, and the
      held-gross series must agree to < 1e-12.
  [b] MASK EQUIVALENCE.  cad_mask(W/M/Q, phase 0) must equal `engine.rebalance_mask` exactly, so
      that the W / CAL-M / CAL-Q points ARE idea 297's points and not a re-definition.
  [c] B0 REPRODUCTION.  The W / CAL-M / CAL-Q rows of this run must reproduce idea 297's
      committed `.decomp.csv` on c_bar, gap0_pp, pred0_pp, resid0_pp to < 1e-6 on all four
      windows (432 rows).  If [c] fails the rest of the script is measuring something else.
  [d] IDENTITY EXACTNESS.  r_dg,t == c_t * r_rs,t at 0 bps on every one of the 1440 pairs
      (bar 1e-12) - the decomposition must stay algebraically exact at every phase.
  [e] K=1 NEGATIVE CONTROL.  At W, CAL-M and CAL-Q, MEANPH must equal PH0 to 0.0 exactly.

Tuned parameters (PROTOCOL rule 4: at most two)
-----------------------------------------------
    band b   in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}
    cadence  in {W, CAL-M, CAL-Q, 4W, 13W}
Reported at EVERY value, selected at none except inside the rule-8 walk-forward.  PHASE is not a
tuned parameter - it is not a tradable choice, and the whole point of the run is that it must be
integrated out.  Panel, gate form (MA / MAVOL) and construction (DEGROSS / RESPREAD) are
REPORTED dimensions.

Grid: 3 panels x 2 gates x 6 bands x 2 constructions x 20 phase-runs = 1440 backtests, each
scored at 0 bps (for the decomposition) and 10 bps (for the level columns; costs are linear in
turnover so one run serves both rungs exactly).  Plus 15 cadence-matched no-filter controls, the
live RULES v2 book and SPY.  Every cell printed.

Walk-forward (PROTOCOL rule 8): (band, cadence) chosen on <= 2016-12-31 by IS Sharpe inside each
panel x gate x construction arm under BOTH collapses (PH0 = the incumbent reading, MEANPH = the
honest one); 2017-2026 read once.  OOS CAGR / Sharpe / MaxDD reported against the live RULES v2
book, SPY and the matched no-filter control.  Both KEEP paths (4a vs the live book, 4b vs SPY)
evaluated on every cell.

SURVIVORSHIP: all three panels are CURRENT constituents - prices_small.csv is a screen of
today's sub-$2B names (44 dropped for max_1d_move >= 1.0) and universe(_broad).json are today's
large caps / ETFs; no delistings.  Every headline here is an arm-minus-arm contrast on the SAME
names and days (DEGROSS and RESPREAD share one gate mask; phases share everything but the
rebalance calendar), so the bias very largely cancels out of the residual; it does NOT cancel out
of the 4a / 4b columns, which are levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
Writes .console.txt, .phaserows.csv, .collapse.csv, .hypo.csv, .walkforward.csv, .result.md.
"""
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, band_state, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

STEM = Path(__file__).with_suffix("").name
OUT = Path(__file__).with_suffix("")
PARENT = REPO / "research" / "backtests" / \
    "2026-09-06_is-the-negative-exposure-timing-residual-a-general-property-of-gates_B.decomp.csv"

COST_BPS = 10
GROSS = 0.75
MAX_VOL = 0.60
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
GATES = ["MA", "MAVOL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
PANELS = ["SMALL439", "U56", "B136"]
POINTS = ["W", "CAL-M", "CAL-Q", "4W", "13W"]
NPHASE = {"W": 1, "CAL-M": 1, "CAL-Q": 1, "4W": 4, "13W": 13}
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# idea 297's committed FULL-window panel means (decomp.csv, mean over 12 gate x band cells)
PUB = {"SMALL439": {"W": -0.2726, "M": -0.1835, "Q": -0.7453},
       "U56": {"W": -0.3097, "M": -0.0719, "Q": -0.5165},
       "B136": {"W": -0.4887, "M": -0.3017, "Q": -0.6662}}
GAP_PUB = {k: v["M"] - v["Q"] for k, v in PUB.items()}

TOL_ENGINE = 1e-12
TOL_REPRO = 1e-6
TOL_IDENT = 1e-12

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def flush():
    OUT.with_suffix(".console.txt").write_text("\n".join(_lines) + "\n")


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ------------------------------------------------------------------ cadence masks (idea 187/222)
_WEEK_K = {"W": 1, "4W": 4, "13W": 13}
_PER_K = {"CAL-M": "M", "CAL-Q": "Q"}


def cad_mask(idx, cad, phase=0):
    """True on the last bar of each cadence block.  Weekly-block points take a phase offset in
    weeks; the calendar points are k=1 and have exactly one phase."""
    n = len(idx)
    if cad in _WEEK_K:
        ordi = np.asarray(idx.to_period("W").astype("int64"))
        ordi = ordi - ordi[0]
        key = (ordi + phase) // _WEEK_K[cad]
    elif cad in _PER_K:
        if phase != 0:
            raise ValueError("calendar points have one phase")
        key = np.asarray(idx.to_period(_PER_K[cad]).astype("int64"))
    else:
        raise ValueError(cad)
    m = np.empty(n, bool)
    m[:-1] = key[:-1] != key[1:]
    m[-1] = True
    return pd.Series(m, index=idx)


def fast_backtest(prices, weights, cad="W", phase=0):
    """Vectorised equivalent of engine.backtest (control [a]).  Returns the 0-bps return series,
    the turnover series (costs are linear, so any rung follows) and the held gross."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad, phase).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1)
    return dict(r0=pd.Series(port, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(held.sum(axis=1), index=idx))


# ------------------------------------------------------------------ books (idea 297 verbatim)
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, gate, band):
    g = band_state(px, band)
    if gate == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g & live_mask(px)


def book_w(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


# ------------------------------------------------------------------ stats
def cagr_of(r):
    return metrics(r)["CAGR"]


def stat(r):
    m = metrics(r)
    h = len(r) // 2
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def decompose(r_dg0, r_rs0, g_dg, g_rs, window):
    """idea 290's constant-leverage split, restricted to `window`."""
    d, r_, hd, hr = (s.loc[window] for s in (r_dg0, r_rs0, g_dg, g_rs))
    if len(d) < 60:
        return None
    c_t = (hd / hr.replace(0, np.nan)).fillna(0.0)
    c_bar = float(c_t.mean())
    cagr_rs = cagr_of(r_)
    gap0 = 100 * (cagr_of(d) - cagr_rs)
    pred0 = 100 * (cagr_of(c_bar * r_) - cagr_rs)
    return dict(c_bar=c_bar, c_sd=float(c_t.std()), gap0_pp=gap0, pred0_pp=pred0,
                resid0_pp=gap0 - pred0,
                share=(pred0 / gap0) if abs(gap0) > 1e-12 else np.nan, n_days=len(d))


# ------------------------------------------------------------------ main
def main():
    t_start = time.time()
    P("=" * 175)
    P(f"IDEA 302 - why-is-MONTHLY-the-least-negative-cadence-for-the-de-gross-timing-residual "
      f"(lane cloud, {pd.Timestamp.today().date()})")
    P("=" * 175)
    P("Idea 297 read the de-gross timing residual at THREE calendar points and found monthly the")
    P("least negative rung on all three panels.  A calendar point is ONE phase.  This run re-runs")
    P("the residual at the block twins 4W (4 phases) and 13W (13 phases), every phase, and reads")
    P("the phase-averaged residual beside idea 297's calendar numbers.")
    P(f"Costs {COST_BPS} bps (plus a 0-bps rung for the decomposition), gross {GROSS}, next-day "
      f"execution, no shorting, no leverage.")
    P(f"Published FULL-window M-minus-Q gap under test: " +
      ", ".join(f"{k} {GAP_PUB[k]:+.4f}" for k in PANELS) + " pp/yr.")

    # ---------------- panels
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    PX = {"SMALL439": (pxs[inv], pxs["SPY"]),
          "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
          "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"])}
    P(f"\npanels: SMALL439 {PX['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0), U56 {PX['U56'][0].shape[1]}, B136 {PX['B136'][0].shape[1]}")
    starts = {k: v[0].index[260] for k, v in PX.items()}
    ends = {k: v[0].index[-1] for k, v in PX.items()}
    common_start, common_end = max(starts.values()), min(ends.values())
    for k in PANELS:
        P(f"  {k}: {PX[k][0].index[0].date()} .. {ends[k].date()}; evaluated from "
          f"{starts[k].date()} ({len(PX[k][0].loc[starts[k]:]) / 252:.2f} yrs)")
    P(f"  COMMON window: {common_start.date()} .. {common_end.date()}")

    # ---------------- controls [a] and [b]
    P("\n" + "-" * 175)
    P("CONTROLS ASSERTED BEFORE ANY NEW NUMBER IS READ")
    P("-" * 175)
    mask_ok = True
    for k in PANELS:
        idx = PX[k][0].index
        for cad, eng in (("W", "W"), ("CAL-M", "M"), ("CAL-Q", "Q")):
            ok = bool((cad_mask(idx, cad, 0) == rebalance_mask(idx, eng)).all())
            mask_ok &= ok
    P(f"  [b] cad_mask(W/CAL-M/CAL-Q, phase 0) == engine.rebalance_mask on all 3 panels: "
      f"{'HOLDS' if mask_ok else 'FAILS'}")

    eq_err, eq_gross = 0.0, 0.0
    for k in PANELS:
        px = PX[k][0]
        g = gate_mask(px, "MA", 0.03)
        for con in CONSTRUCTIONS:
            w = book_w(px, g, con)
            for cad, eng in (("W", "W"), ("CAL-M", "M")):
                f = fast_backtest(px, w, cad, 0)
                e = backtest(px, w, cost_bps=COST_BPS, freq=eng)
                eq_err = max(eq_err, float(((f["r0"] - f["turn"] * COST_BPS / 1e4)
                                            - e["returns"]).abs().max()))
                eq_gross = max(eq_gross, float((f["gross"] - e["weights"].sum(axis=1)).abs().max()))
    P(f"  [a] vectorised backtester vs engine.backtest, 12 books: max |return diff| {eq_err:.3e}, "
      f"max |gross diff| {eq_gross:.3e} (bar {TOL_ENGINE:g}) -> "
      f"{'HOLDS' if max(eq_err, eq_gross) < TOL_ENGINE else 'FAILS'}")
    if not mask_ok or max(eq_err, eq_gross) >= TOL_ENGINE:
        P("!! control [a]/[b] failed - aborting."); flush(); sys.exit(1)

    # ---------------- reference books
    ctrl, spy_stat = {}, {}
    for k in PANELS:
        px, spy = PX[k]
        st = starts[k]
        for cad in POINTS:
            rs = []
            for ph in range(NPHASE[cad]):
                f = fast_backtest(px, control_book(px), cad, ph)
                rs.append((f["r0"] - f["turn"] * COST_BPS / 1e4).loc[st:])
            ctrl[(k, cad)] = stat(sum(rs) / len(rs))          # MEANPH-of-returns control
        spy_stat[k] = stat(spy.pct_change().fillna(0.0).loc[st:])
    px_u = load_universe()
    live_s = stat(backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                           freq="W")["returns"].loc[starts["U56"]:])
    ref = {f"CONTROL EWall {k} {c} (no filter, phase-blended)": ctrl[(k, c)]
           for k in PANELS for c in POINTS}
    ref["RULES v2 on universe.json (LIVE BOOK, 4a comparand)"] = live_s
    for k in PANELS:
        ref[f"SPY on {k} window (4b comparand)"] = spy_stat[k]
    P("\nREFERENCE BOOKS")
    P(fmt(pd.DataFrame(ref).T))

    # ---------------- the grid
    P("\n" + "-" * 175)
    P(f"GRID - 3 panels x 2 gates x 6 bands x 2 constructions x {sum(NPHASE.values())} "
      f"phase-runs = {3 * 2 * 6 * 2 * sum(NPHASE.values())} backtests")
    P("-" * 175)
    wins = {"FULL": None, "COMMON": slice(common_start, common_end),
            "IS": slice(None, IS_END), "OOS": slice(OOS_START, None)}
    rows, ident_err, n_pairs = [], 0.0, 0
    blend = {}                       # (panel,gate,band,con,point) -> phase-mean 10bps returns
    for k in PANELS:
        px, _ = PX[k]
        st = starts[k]
        years = len(px.loc[st:]) / 252
        for gate in GATES:
            for b in BANDS:
                g = gate_mask(px, gate, b)
                w = {con: book_w(px, g, con) for con in CONSTRUCTIONS}
                for cad in POINTS:
                    acc = {con: [] for con in CONSTRUCTIONS}
                    for ph in range(NPHASE[cad]):
                        f = {con: fast_backtest(px, w[con], cad, ph) for con in CONSTRUCTIONS}
                        r0 = {c: f[c]["r0"].loc[st:] for c in CONSTRUCTIONS}
                        r10 = {c: (f[c]["r0"] - f[c]["turn"] * COST_BPS / 1e4).loc[st:]
                               for c in CONSTRUCTIONS}
                        gr = {c: f[c]["gross"].loc[st:] for c in CONSTRUCTIONS}
                        c_t = (gr["DEGROSS"] / gr["RESPREAD"].replace(0, np.nan)).fillna(0.0)
                        ident_err = max(ident_err,
                                        float((r0["DEGROSS"] - c_t * r0["RESPREAD"]).abs().max()))
                        n_pairs += 1
                        for con in CONSTRUCTIONS:
                            acc[con].append(r10[con])
                        base = dict(panel=k, gate=gate, band=b, point=cad, phase=ph)
                        for wn, sl in wins.items():
                            sl = slice(None) if sl is None else sl
                            d = decompose(r0["DEGROSS"], r0["RESPREAD"],
                                          gr["DEGROSS"], gr["RESPREAD"], sl)
                            if d is None:
                                continue
                            rows.append(dict(**base, window=wn, **d))
                        for con in CONSTRUCTIONS:
                            s = stat(r10[con])
                            rows.append(dict(**base, window="LEVEL", con=con, **s,
                                             turn_yr=f[con]["turn"].loc[st:].sum() / years,
                                             gross_mean=float(gr[con].mean()),
                                             p4a=verdict_4a(s, live_s),
                                             f4b=fail_4b(s, spy_stat[k])))
                    for con in CONSTRUCTIONS:
                        blend[(k, gate, b, con, cad)] = sum(acc[con]) / len(acc[con])
        P(f"  {k} done ({time.time() - t_start:.0f}s)")
    R = pd.DataFrame(rows)
    R.to_csv(OUT.with_suffix(".phaserows.csv"), index=False)
    P(f"  [d] identity r_dg,t == c_t*r_rs,t at 0 bps on all {n_pairs} pairs: worst "
      f"{ident_err:.3e} (bar {TOL_IDENT:g}) -> {'HOLDS' if ident_err < TOL_IDENT else 'FAILS'}")

    # ---------------- control [c]: reproduce idea 297
    D = R[R.window != "LEVEL"].copy()
    old = pd.read_csv(PARENT)
    ren = {"W": "W", "CAL-M": "M", "CAL-Q": "Q"}
    new = D[D.point.isin(ren)].copy()
    new["cad"] = new.point.map(ren)
    m = old.merge(new, on=["panel", "window", "gate", "cad", "band"], suffixes=("_o", "_n"))
    cols = ["c_bar", "gap0_pp", "pred0_pp", "resid0_pp"]
    worst = max(float((m[f"{c}_o"] - m[f"{c}_n"]).abs().max()) for c in cols)
    P(f"  [c] B0 reproduction of idea 297 decomp.csv: {len(m)} of {len(old)} rows matched, "
      f"worst |diff| {worst:.3e} (bar {TOL_REPRO:g}) -> "
      f"{'HOLDS' if (worst < TOL_REPRO and len(m) == len(old)) else 'FAILS'}")
    if worst >= TOL_REPRO or len(m) != len(old):
        P("!! control [c] failed - this script is not measuring idea 297's quantity. Aborting.")
        flush(); sys.exit(1)

    # ---------------- collapses
    P("\n" + "-" * 175)
    P("COLLAPSE - PH0 vs MEANPH, per (panel, gate, band, point)")
    P("-" * 175)
    key = ["panel", "window", "gate", "band", "point"]
    ph0 = D[D.phase == 0].set_index(key)["resid0_pp"].rename("PH0")
    mph = D.groupby(key)["resid0_pp"].mean().rename("MEANPH")
    sdp = D.groupby(key)["resid0_pp"].std().rename("SDPH")
    rng = (D.groupby(key)["resid0_pp"].max() - D.groupby(key)["resid0_pp"].min()).rename("RANGEPH")
    C = pd.concat([ph0, mph, sdp, rng], axis=1).reset_index()
    C.to_csv(OUT.with_suffix(".collapse.csv"), index=False)

    k1 = C[C.point.isin(["W", "CAL-M", "CAL-Q"])]
    e_err = float((k1.PH0 - k1.MEANPH).abs().max())
    P(f"  [e] k=1 negative control (W, CAL-M, CAL-Q): max |MEANPH - PH0| = {e_err:.3e} "
      f"-> {'HOLDS' if e_err == 0.0 else 'FAILS'}")

    for wn in ["FULL", "OOS"]:
        sub = C[C.window == wn]
        P(f"\n  panel-mean residual (pp/yr), window {wn} (mean over 12 gate x band cells)")
        P(fmt(sub.pivot_table(index="panel", columns="point", values=["PH0", "MEANPH"],
                              aggfunc="mean")[["PH0", "MEANPH"]].reindex(PANELS)))

    # ---------------- A1 phase spread vs effect
    P("\n" + "-" * 175)
    P("A1 - IS THE PHASE SPREAD AS LARGE AS THE CADENCE EFFECT?  (FULL window)")
    P("-" * 175)
    F = D[D.window == "FULL"]
    pm = F.groupby(["panel", "point", "phase"])["resid0_pp"].mean().reset_index()   # panel-mean per phase
    a1 = []
    for k in PANELS:
        r = {}
        for cad in ["4W", "13W"]:
            v = pm[(pm.panel == k) & (pm.point == cad)]["resid0_pp"]
            r[f"{cad}_min"], r[f"{cad}_max"] = v.min(), v.max()
            r[f"{cad}_range"] = v.max() - v.min()
            r[f"{cad}_sd"] = v.std()
        a1.append(dict(panel=k, **r, GAP_PUB=GAP_PUB[k],
                       range13_ge_gap=bool(r["13W_range"] >= GAP_PUB[k]),
                       range4_ge_gap=bool(r["4W_range"] >= GAP_PUB[k])))
    A1 = pd.DataFrame(a1).set_index("panel")
    P(fmt(A1))
    a1_hits = int(A1.range13_ge_gap.sum())
    P(f"A1: range(13W panel-mean residual) >= GAP_PUB on {a1_hits}/3 panels -> "
      f"{'PHASE SPREAD DOMINATES' if a1_hits >= 2 else 'effect exceeds phase spread'}")

    # ---------------- A2 does the gap survive averaging
    P("\n" + "-" * 175)
    P("A2 - DOES THE M-MINUS-Q GAP SURVIVE PHASE AVERAGING?  (FULL window, MEANPH)")
    P("-" * 175)
    a2 = []
    for k in PANELS:
        sub = C[(C.window == "FULL") & (C.panel == k)]
        g = {p: sub[sub.point == p].MEANPH.mean() for p in POINTS}
        gap_block = g["4W"] - g["13W"]
        a2.append(dict(panel=k, W=g["W"], CAL_M=g["CAL-M"], CAL_Q=g["CAL-Q"],
                       BLK_4W=g["4W"], BLK_13W=g["13W"],
                       gap_cal=g["CAL-M"] - g["CAL-Q"], gap_block=gap_block,
                       GAP_PUB=GAP_PUB[k], frac_of_pub=gap_block / GAP_PUB[k],
                       survives=bool(gap_block >= 0.5 * GAP_PUB[k])))
    A2 = pd.DataFrame(a2).set_index("panel")
    P(fmt(A2))
    a2_hits = int(A2.survives.sum())
    P(f"A2: phase-averaged block gap >= 0.5*GAP_PUB on {a2_hits}/3 panels -> "
      f"{'REAL TIMING EFFECT' if a2_hits == 3 else 'gap does NOT survive averaging on all panels'}")

    # ---------------- A3 calendar rank
    P("\n" + "-" * 175)
    P("A3 - WHERE DO THE CALENDAR POINTS SIT INSIDE THEIR OWN BLOCK PHASE DISTRIBUTIONS?")
    P("-" * 175)
    a3 = []
    for k in PANELS:
        for cal, blk in (("CAL-M", "4W"), ("CAL-Q", "13W")):
            v = np.sort(pm[(pm.panel == k) & (pm.point == blk)]["resid0_pp"].values)[::-1]
            c = float(pm[(pm.panel == k) & (pm.point == cal)]["resid0_pp"].iloc[0])
            rank = int((v > c).sum()) + 1                    # 1 = least negative
            a3.append(dict(panel=k, calendar=cal, block=blk, cal_resid=c,
                           blk_best=v[0], blk_worst=v[-1], blk_mean=v.mean(),
                           rank_of_cal=rank, n_phases=len(v),
                           pctile=1 - (rank - 0.5) / len(v)))
    A3 = pd.DataFrame(a3)
    P(fmt(A3.set_index(["panel", "calendar"])))
    m_top = int(((A3.calendar == "CAL-M") & (A3.rank_of_cal <= A3.n_phases / 2)).sum())
    q_bot = int(((A3.calendar == "CAL-Q") & (A3.rank_of_cal > A3.n_phases / 2)).sum())
    P(f"A3: CAL-M in the top half of its 4W phases on {m_top}/3 panels; CAL-Q in the bottom half "
      f"of its 13W phases on {q_bot}/3 -> "
      f"{'CALENDAR LUCK' if (m_top >= 2 and q_bot >= 2) else 'no consistent calendar tilt'}")

    # ---------------- A4 non-negative cells
    P("\n" + "-" * 175)
    P("A4 - THE NON-NEGATIVE CELLS (idea 297: 6, all monthly)")
    P("-" * 175)
    a4 = []
    for cad in POINTS:
        sub = C[(C.window == "FULL") & (C.point == cad)]
        allph = F[F.point == cad].groupby(["panel", "gate", "band"])["resid0_pp"].max()
        allpos = F[F.point == cad].groupby(["panel", "gate", "band"])["resid0_pp"].min()
        a4.append(dict(point=cad, n_cells=len(sub), meanph_nonneg=int((sub.MEANPH >= 0).sum()),
                       ph0_nonneg=int((sub.PH0 >= 0).sum()),
                       any_phase_nonneg=int((allph >= 0).sum()),
                       every_phase_nonneg=int((allpos >= 0).sum())))
    A4 = pd.DataFrame(a4).set_index("point")
    P(fmt(A4))
    nn = C[(C.window == "FULL") & (C.MEANPH >= 0)]
    P(f"\n  non-negative MEANPH cells ({len(nn)}):")
    P(fmt(nn[["panel", "gate", "band", "point", "PH0", "MEANPH", "SDPH", "RANGEPH"]]
          .set_index(["panel", "point"])) if len(nn) else "  (none)")
    e4 = int(A4.loc["4W", "every_phase_nonneg"])
    P(f"A4: 4W cells non-negative at EVERY one of their 4 phases: {e4} -> "
      f"{'the sign anomaly is a phase draw' if e4 == 0 else 'a phase-robust non-negative cell exists'}")

    # ---------------- A5 estimator walk-forward
    P("\n" + "-" * 175)
    P("A5 - RULE 8 ON THE ESTIMATOR: does phase averaging predict the OOS residual better?")
    P("-" * 175)
    piv = C.pivot_table(index=["panel", "gate", "band", "point"], columns="window",
                        values=["PH0", "MEANPH"])
    blk = piv.reset_index()
    blk = blk[blk.point.isin(["4W", "13W"])]
    a5 = []
    for k in PANELS:
        s = blk[blk.panel == k]
        tgt = s[("MEANPH", "OOS")]
        for est, col in (("PH0(IS)", ("PH0", "IS")), ("MEANPH(IS)", ("MEANPH", "IS")),
                         ("zero", None)):
            pred = pd.Series(0.0, index=s.index) if col is None else s[col]
            a5.append(dict(panel=k, estimator=est, n=len(s),
                           MAE=float((pred - tgt).abs().mean()),
                           bias=float((pred - tgt).mean())))
    A5 = pd.DataFrame(a5)
    P(fmt(A5.pivot_table(index="panel", columns="estimator", values="MAE").reindex(PANELS)))
    wins_mph = 0
    for k in PANELS:
        a = A5[(A5.panel == k) & (A5.estimator == "MEANPH(IS)")].MAE.iloc[0]
        b = A5[(A5.panel == k) & (A5.estimator == "PH0(IS)")].MAE.iloc[0]
        wins_mph += int(a < b)
    P(f"A5: MEANPH(IS) beats PH0(IS) on OOS MAE on {wins_mph}/3 panels -> "
      f"{'phase averaging is the better estimator' if wins_mph >= 2 else 'no estimator gain'}")

    # ---------------- levels, 4a/4b census, walk-forward
    P("\n" + "-" * 175)
    P("LEVELS - both KEEP paths on every cell (10 bps).  MEANPH collapse of the level stats.")
    P("-" * 175)
    L = R[R.window == "LEVEL"].copy()
    lk = ["panel", "gate", "band", "point", "con"]
    LM = L.groupby(lk)[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "isSharpe", "oCAGR",
                        "oSharpe", "oMaxDD", "turn_yr", "gross_mean"]].mean().reset_index()
    LM["p4a"] = [verdict_4a(r, live_s) for _, r in LM.iterrows()]
    LM["f4b"] = [fail_4b(r, spy_stat[r.panel]) for _, r in LM.iterrows()]
    LM["p4b"] = LM.f4b == "-"
    P(f"cells: {len(LM)} (MEANPH).  4a pass {int(LM.p4a.sum())}/{len(LM)}, "
      f"4b pass {int(LM.p4b.sum())}/{len(LM)}")
    P("\n4b failure reasons (MEANPH cells):")
    P(fmt(LM.f4b.value_counts().to_frame("n")))
    for k in PANELS:
        for con in CONSTRUCTIONS:
            sub = LM[(LM.panel == k) & (LM.con == con)].set_index(["gate", "point", "band"])
            P(f"\n--- {k} / {con} (MEANPH) ---")
            P(fmt(sub[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
                       "turn_yr", "gross_mean", "p4a", "f4b"]]))
    if LM.p4b.any():
        P("\n4b PASSING cells:")
        P(fmt(LM[LM.p4b].set_index(["panel", "con", "gate", "point", "band"])
              [["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "oMaxDD"]]))

    P("\n" + "-" * 175)
    P("WALK-FORWARD (PROTOCOL rule 8): (band, cadence) chosen on IS Sharpe per panel x gate x")
    P("construction arm, under BOTH collapses; 2017- read once.")
    P("-" * 175)
    wf = []
    for k in PANELS:
        for gate in GATES:
            for con in CONSTRUCTIONS:
                for coll, src in (("PH0", L[L.phase == 0]), ("MEANPH", LM)):
                    s = src[(src.panel == k) & (src.gate == gate) & (src.con == con)]
                    pick = s.loc[s.isSharpe.idxmax()]
                    wf.append(dict(panel=k, gate=gate, con=con, collapse=coll,
                                   band=pick.band, point=pick.point, isSharpe=pick.isSharpe,
                                   oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                                   ctrl_oSharpe=ctrl[(k, pick.point)]["oSharpe"],
                                   spy_oSharpe=spy_stat[k]["oSharpe"],
                                   live_oSharpe=live_s["oSharpe"],
                                   spy_oCAGR=spy_stat[k]["oCAGR"], live_oCAGR=live_s["oCAGR"],
                                   spy_oMaxDD=spy_stat[k]["oMaxDD"],
                                   beats_spy=bool(pick.oSharpe > spy_stat[k]["oSharpe"]),
                                   beats_live=bool(pick.oSharpe > live_s["oSharpe"]),
                                   beats_ctrl=bool(pick.oSharpe > ctrl[(k, pick.point)]["oSharpe"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P(fmt(WF.set_index(["panel", "gate", "con", "collapse"])))
    P(f"\nOOS: beats SPY {int(WF.beats_spy.sum())}/{len(WF)}, live book "
      f"{int(WF.beats_live.sum())}/{len(WF)}, matched no-filter control "
      f"{int(WF.beats_ctrl.sum())}/{len(WF)}")
    agree = WF.pivot_table(index=["panel", "gate", "con"], columns="collapse",
                           values="oSharpe")
    P(f"OOS Sharpe, PH0-chosen vs MEANPH-chosen arm: mean {agree['PH0'].mean():.4f} vs "
      f"{agree['MEANPH'].mean():.4f} (delta {agree['MEANPH'].mean() - agree['PH0'].mean():+.4f})")
    same = WF.pivot_table(index=["panel", "gate", "con"], columns="collapse",
                          values="point", aggfunc="first")
    P(f"the two collapses pick the SAME cadence point in {int((same['PH0'] == same['MEANPH']).sum())}"
      f"/{len(same)} arms")

    # ---------------- summary
    P("\n" + "=" * 175)
    P("SUMMARY")
    P("=" * 175)
    hyp = pd.DataFrame([
        dict(test="A1 phase spread >= published gap (13W)", bar=">=2/3 panels",
             result=f"{a1_hits}/3", reading="phase spread dominates" if a1_hits >= 2 else "effect exceeds spread"),
        dict(test="A2 phase-averaged 4W-13W gap >= 0.5*GAP_PUB", bar="3/3 panels",
             result=f"{a2_hits}/3", reading="real timing effect" if a2_hits == 3 else "gap does not survive"),
        dict(test="A3 CAL-M top half AND CAL-Q bottom half", bar=">=2/3 each",
             result=f"M {m_top}/3, Q {q_bot}/3",
             reading="calendar luck" if (m_top >= 2 and q_bot >= 2) else "no consistent tilt"),
        dict(test="A4 4W cells non-negative at every phase", bar="0 = phase draw",
             result=f"{e4}", reading="phase draw" if e4 == 0 else "phase-robust cell exists"),
        dict(test="A5 MEANPH(IS) beats PH0(IS) on OOS MAE", bar=">=2/3 panels",
             result=f"{wins_mph}/3",
             reading="averaging helps" if wins_mph >= 2 else "no estimator gain"),
    ])
    P(fmt(hyp.set_index("test")))
    hyp.to_csv(OUT.with_suffix(".hypo.csv"), index=False)
    P(f"\n4a pass {int(LM.p4a.sum())}/{len(LM)} MEANPH cells; 4b pass {int(LM.p4b.sum())}/{len(LM)}.")
    P(f"runtime {time.time() - t_start:.0f}s")
    flush()


if __name__ == "__main__":
    main()
