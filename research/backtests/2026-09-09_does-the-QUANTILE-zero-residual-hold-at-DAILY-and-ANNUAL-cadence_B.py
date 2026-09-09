#!/usr/bin/env python3
"""Idea 307 - "does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence" (lane B, 2026-09-09).

The question
------------
Idea 300 (lane C, 2026-09-06) nominated the matched QUANTILE gate as THE RECORD'S PURE-EXPOSURE
CONTROL.  The nomination rests on one number: the gate's timing residual

    resid0 = [CAGR0(DEGROSS) - CAGR0(RESPREAD)] - [CAGR0(c_bar * r_RESPREAD) - CAGR0(r_RESPREAD)]

is ZERO on SMALL439 (mean -0.0124 pp/yr, sd 0.0242 over 27 cells) and its zero WALKS FORWARD
(OOS -0.0002 pp/yr, MAE 0.0216 beating the IS-constant's 0.0348) - against the record's own MA
gate, whose residual is a lump of -0.38 pp/yr (sd 0.32).  A gate with no timing residual is a
pure cash dial: it spends exposure and buys nothing back, which is exactly what a CONTROL has to
be if the record is going to price other gates against it.

But idea 300 measured that zero at THREE cadences only: W, M, Q.  The queue's objection is
methodological and correct: a control that only holds at three interior points of the cadence
dial is not a control, it is a coincidence with three witnesses.  The residual is a
TIMING quantity, and cadence is precisely the dial that governs how often the exposure is
allowed to move.  Both extremes have a mechanical reason to break the zero:

  * DAILY.  c_t moves every bar.  The gate's exposure now tracks the panel's own drawdowns at
    the highest possible frequency, so if quantile-depth timing has ANY covariance with returns,
    D is where it shows up largest.  D also maximises turnover, but resid0 is computed at 0 bps
    (derived exactly, not re-run), so costs cannot contaminate it.
  * ANNUAL.  c_t moves 16 times in the whole sample.  Each level is held across a full calendar
    year, so the arithmetic c_bar in `pred0` is being asked to stand in for a step function with
    enormous within-period dispersion.  Jensen gap between CAGR(c_bar * r) and the realised
    compounding of a piecewise-constant c_t is largest here.

So the two extremes fail for OPPOSITE reasons if they fail, which makes the test informative
either way.  If the zero survives both, QUANTILE-M is a control over the whole dial and the
record can use it without a cadence caveat.  If it breaks at either end, every published number
that leaned on QUANTILE-M as "the zero" inherits a cadence restriction that was never stated.

Pre-registered hypotheses and bars (written before any D or A number was read)
-----------------------------------------------------------------------------
H_ZERO_IS_A_CONTROL.  The QUANTILE gate's residual is zero at every cadence.
    BAR (all four clauses, on QUANTILE-M):
      (1) |mean resid0| <= 0.05 pp/yr at D, AND at A          (idea 298/300's own zero band)
      (2) max |resid0| over the 9 thetas <= 0.10 pp/yr at D, AND at A
      (3) |mean OOS resid0| <= 0.05 pp/yr at D, AND at A
      (4) the D and A means are inside the W/M/Q envelope +/- 0.05 pp/yr
          (i.e. the extremes are not a different population from the interior)

H_ZERO_IS_INTERIOR.  The zero is a property of the interior cadences only.
    BAR: any clause of H_ZERO_IS_A_CONTROL fails at D or at A.

The two are exhaustive and mutually exclusive.  Whichever wins, the deliverable is the same
table: resid0 by cadence x theta for both gate families, with the MA gate carried as the
contrast that is known NOT to be zero.

G0 - reproduction / validity gates, asserted and printed BEFORE any headline number
-----------------------------------------------------------------------------------
G0.1  The local cadence-extended backtester must reproduce `engine.backtest` EXACTLY at the
      four cadences engine supports (D, W, M, Q): max |dr_t| < 1e-15 on a live book.  engine's
      `rebalance_mask` has no "A", and PROTOCOL forbids editing the engine, so the annual arm
      runs through a local copy of engine's own loop with one extra period key.  Without this
      gate the A column is a different backtester, not a different cadence.
G0.2  Idea 300's committed `.decomp.csv` must reproduce at W/M/Q: max |d resid0| < 1e-6 pp/yr
      over all 54 shared FULL cells (2 families x 9 thetas x 3 cadences).
G0.3  Idea 290's identity r_dg,t == c_t * r_rs,t at 0 bps, max |error| < 1e-12, at EVERY
      cadence including D and A.
G0.4  Matching quality (idea 300's B_MATCH (i)): |mask fraction(QUANTILE) - mask fraction(MA)|
      < 0.01 at all 9 thetas.  The matching is cadence-free (it is a mask property), so this is
      a single 9-row check, but it is re-asserted because everything downstream is "at matched
      c_bar" and that claim has to be true.

Design
------
PANEL: SMALL439 - the 484-name sub-$2B panel from data/prices_small.csv.gz less the 44 names
       with max_1d_move >= 1.0, exactly idea 290/298/300's panel.  SPY joined as benchmark only.

FAMILIES (reported contrast, not a dial):
  MA-THRESH   IN where px > ma200*(1+theta).  Depth moves with the market; c_bar is an outcome.
  QUANTILE-M  IN the top ceil(x*n_t) live names by dist = px/ma200 - 1, x set to the MA arm's
              OWN mean mask fraction at that theta.  Same ranking, same mean exposure, CONSTANT
              depth.  x is a deterministic function of theta, not a third dial.

CONSTRUCTIONS (both reported): RESPREAD (w = GROSS/k_t on held names, exposure pinned at 1) and
  DEGROSS (w = GROSS/n_t, gated weight to cash).  resid0 is defined on the pair.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. strictness theta   9 values, idea 300's grid verbatim
    2. cadence            5 values: D, W, M, Q, A  <- the object under test
Every one of the 45 combinations is reported; none is selected outside the rule-8 walk-forward.
Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps rung used by every
residual is DERIVED exactly (r0 = r10 + turnover * bps/1e4) from the same book, not re-run.

Grid: 9 thetas x 5 cadences x 2 families x 2 constructions = 180 books; 90 decomposition cells.

Rule 8 walk-forward (required, directions fixed before any OOS number was read)
  WF-A (the book).  Within each family x construction arm, (theta, cadence) is chosen on
        2010..2016-12-31 by IS Sharpe and 2017-01-01..2026 is read ONCE.  OOS CAGR/Sharpe/MaxDD
        reported against RULES v2 (live), SPY and the cadence-matched no-gate EWall control.
  WF-B (the cadence dial itself).  Pick the CADENCE with the higher IS Sharpe per family x
        construction and read OOS once, against always-D, always-W, always-M, always-Q,
        always-A.  If the extremes are not learnable IS->OOS the dial is not an edge.
  WF-C (the residual, the headline).  Fit nothing: does the IS-window per-cell resid0 predict
        the OOS-window resid0 better than a hard zero?  Reported as MAE in pp/yr against the
        zero baseline, per cadence.  This is idea 300's WF-C extended to D and A - the test of
        whether the zero is USABLE, not merely observed.

Verdicts (both KEEP paths, on every one of the 180 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: data/prices_small.csv.gz is CURRENT constituents of the screen - no delistings -
so every CAGR LEVEL is inflated and the 4a/4b columns inherit the bias whole.  The headline is
an arm-minus-arm contrast on the SAME names, SAME ranking and SAME days, so the bias very
largely cancels out of resid0; it does NOT cancel out of the KEEP columns.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .cadence.csv .walkforward.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest as engine_backtest, rebalance_mask as engine_mask, metrics

COST_BPS = 10
GROSS = 0.75
CADENCES = ["D", "W", "M", "Q", "A"]          # A is the new extreme; D the other
INTERIOR = ["W", "M", "Q"]                     # idea 300's published cadences
EXTREMES = ["D", "A"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# pre-registered bars
BAR_ZERO_MEAN = 0.05        # pp/yr, |mean resid0| for the zero to hold at a cadence
BAR_ZERO_MAX = 0.10         # pp/yr, worst single theta at that cadence
BAR_ENVELOPE = 0.05         # pp/yr, how far outside the W/M/Q envelope an extreme may sit
BAR_ENGINE = 1e-15          # G0.1 local runner vs engine.backtest
BAR_REPRO = 1e-6            # G0.2 idea 300 resid0 reproduction, pp/yr
BAR_IDENT = 1e-12           # G0.3 idea 290 identity
BAR_MASK_TOL = 0.01         # G0.4 matching quality

PRIOR300 = REPO / "research" / "backtests" / \
    "2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.decomp.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- cadence + local engine
def cad_mask(idx, cad):
    """True on the last trading bar of each cadence block.  Identical to
    engine.rebalance_mask for D/W/M/Q; adds A (calendar year)."""
    if cad == "D":
        return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"),
           "Q": idx.to_period("Q"), "A": idx.to_period("Y")}[cad]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)


def bt(prices, weights, cost_bps=COST_BPS, cad="W"):
    """Byte-for-byte copy of engine.backtest's loop with the cadence mask swapped for one
    that also knows "A".  G0.1 asserts it equals engine.backtest at D/W/M/Q."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = cad_mask(prices.index, cad).shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns))
    turnover = pd.Series(0.0, index=prices.index)
    wv = w_target.values
    rv = rets.values
    mv = mask.values
    hv = np.zeros_like(wv)
    tv = np.zeros(len(prices.index))
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
            new = wv[i]
            tv[i] = np.abs(new - cur).sum()
            cur = new
        hv[i] = cur
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    held = pd.DataFrame(hv, index=prices.index, columns=prices.columns)
    turnover = pd.Series(tv, index=prices.index)
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "weights": held, "turnover": turnover}


# ---------------------------------------------------------------- panel
def small439():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return pxs[inv], pxs["SPY"], len(bad)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def dist_rank(px):
    live = live_mask(px)
    return (px / px.rolling(200).mean() - 1).where(live), live


def ma_gate(px, theta):
    live = live_mask(px)
    return (px > px.rolling(200).mean() * (1 + theta)) & live


def quantile_gate(px, x):
    dist, live = dist_rank(px)
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def cagr(r):
    return metrics(r)["CAGR"]


# ---------------------------------------------------------------- main
def main():
    px, spy_px, n_dropped = small439()
    start = px.index[260]
    years = len(px.loc[start:]) / 252
    spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
    spy_s = stat(spy_r)

    P("=" * 175)
    P("Idea 307 does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence (lane B) | "
      + Path(__file__).name)
    P("=" * 175)
    P(f"PANEL SMALL439: {px.shape[1]} names ({n_dropped} dropped for max_1d_move >= 1.0), "
      f"{px.index[0].date()}..{px.index[-1].date()}; evaluation from {start.date()} ({years:.2f} yrs).")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), "
      f"gross {GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): theta {MA_THETA} x cadence {CADENCES}.  x is a deterministic function "
      f"of theta (the matching), not a dial.  All 45 combinations reported.")
    P(f"reported contrasts: family {FAMILIES} x construction {CONSTRUCTIONS}  ->  180 books.")
    P("pre-registered bars (written before any D or A number was read):")
    P(f"  H_ZERO_IS_A_CONTROL : on QUANTILE-M, ALL of "
      f"(1) |mean resid0| <= {BAR_ZERO_MEAN} pp/yr at D AND at A; "
      f"(2) max |resid0| <= {BAR_ZERO_MAX} at D AND at A; "
      f"(3) |mean OOS resid0| <= {BAR_ZERO_MEAN} at D AND at A; "
      f"(4) D and A means inside the W/M/Q envelope +/- {BAR_ENVELOPE}")
    P("  H_ZERO_IS_INTERIOR  : any clause fails at D or A")
    P(f"  G0.1 local runner == engine.backtest at D/W/M/Q, < {BAR_ENGINE:.0e}")
    P(f"  G0.2 idea 300 .decomp.csv resid0 reproduces at W/M/Q, < {BAR_REPRO:.0e} pp/yr")
    P(f"  G0.3 identity |r_dg - c_t*r_rs| < {BAR_IDENT:.0e} at EVERY cadence")
    P(f"  G0.4 |d mask fraction(Q - MA)| < {BAR_MASK_TOL} at all 9 thetas")
    P("SURVIVORSHIP: current constituents of the screen only; CAGR LEVELS inflated, arm-minus-arm "
      "residuals very largely immune, the 4a/4b columns are NOT.")
    flush_log()

    # --------------------------------------------- G0.1 engine equivalence
    P("\n" + "=" * 175)
    P("G0.1  LOCAL CADENCE-EXTENDED RUNNER vs engine.backtest  (read before anything else)")
    P("=" * 175)
    probe_w = book(px, ma_gate(px, 0.00), "DEGROSS")
    g01 = []
    for cad in ["D", "W", "M", "Q"]:
        a = engine_backtest(px, probe_w, cost_bps=COST_BPS, freq=cad)["returns"]
        b = bt(px, probe_w, cost_bps=COST_BPS, cad=cad)["returns"]
        mk = float((cad_mask(px.index, cad).values != engine_mask(px.index, cad).values).sum())
        g01.append(dict(cad=cad, max_abs_dr=float((a - b).abs().max()), mask_diff_bars=mk))
    G01 = pd.DataFrame(g01)
    P(fmt(G01.set_index("cad"), 3).replace("0.000", "0.000"))
    P(G01.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    ok_g01 = bool((G01.max_abs_dr < BAR_ENGINE).all() and (G01.mask_diff_bars == 0).all())
    P(f"G0.1 {'PASS' if ok_g01 else 'FAIL'}  (worst |dr| {G01.max_abs_dr.max():.3e} at "
      f"{BAR_ENGINE:.0e}; mask disagreement bars {int(G01.mask_diff_bars.sum())})")
    nreb = {cad: int(cad_mask(px.index, cad).loc[start:].sum()) for cad in CADENCES}
    P("rebalances in the evaluation window: " + ", ".join(f"{c}={nreb[c]}" for c in CADENCES)
      + "   (the dial spans 3 orders of magnitude: D/A = "
      + f"{nreb['D'] / max(nreb['A'], 1):.0f}x)")
    flush_log()

    # --------------------------------------------- comparands
    px_u = load_universe()
    live_full = engine_backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]
    live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
    ctrl, ctrl0 = {}, {}
    for cad in CADENCES:
        rc = bt(px, control_book(px), cost_bps=COST_BPS, cad=cad)
        r10 = rc["returns"].loc[start:]
        ctrl[cad] = stat(r10)
        ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
    P("")
    P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
      f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS {spy_s['oSharpe']:.4f}")
    P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
      f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS {live_s['oSharpe']:.4f}")
    for cad in CADENCES:
        P(f"CONTROL EWall {cad} (no gate)    : CAGR {ctrl[cad]['CAGR']:.4f} Sharpe {ctrl[cad]['Sharpe']:.4f} "
          f"MaxDD {ctrl[cad]['MaxDD']:.4f} | 0 bps CAGR {ctrl0[cad]:.4f}")
    P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} OOS>{spy_s['oSharpe']:.3f} "
      f"MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} CAGR>={0.70 * spy_s['CAGR']:.2%}")
    flush_log()

    # --------------------------------------------- G0.4 the matching (theta -> x)
    P("\n" + "=" * 175)
    P("G0.4  THE MATCHING: x = the MA gate's OWN mean mask fraction at that theta (cadence-free)")
    P("=" * 175)
    live = live_mask(px).loc[start:]
    nlive = live.sum(axis=1)
    match, gates = [], {}
    for th in MA_THETA:
        gm = ma_gate(px, th)
        frac_ma = float((gm.loc[start:].sum(axis=1) / nlive).mean())
        gq = quantile_gate(px, frac_ma)
        frac_q = float((gq.loc[start:].sum(axis=1) / nlive).mean())
        gates[th] = {"MA-THRESH": gm, "QUANTILE-M": gq}
        match.append(dict(theta=th, x=frac_ma, frac_ma=frac_ma, frac_q=frac_q,
                          d_frac=frac_q - frac_ma,
                          k_ma_sd=float(gm.loc[start:].sum(axis=1).std()),
                          k_q_sd=float(gq.loc[start:].sum(axis=1).std())))
    M = pd.DataFrame(match)
    P(fmt(M.set_index("theta")))
    ok_g04 = bool(M.d_frac.abs().max() < BAR_MASK_TOL)
    P(f"G0.4 {'PASS' if ok_g04 else 'FAIL'}  worst |d mask fraction| = {M.d_frac.abs().max():.5f} "
      f"at {BAR_MASK_TOL}")
    flush_log()

    # --------------------------------------------- the grid
    P("\n" + "=" * 175)
    P("RUNNING THE 180-BOOK GRID (9 theta x 5 cadence x 2 family x 2 construction)")
    P("=" * 175)
    rows, decomp, pair = [], [], []
    for th in MA_THETA:
        for cad in CADENCES:
            got = {}
            for fam in FAMILIES:
                g = gates[th][fam]
                arms = {}
                for con in CONSTRUCTIONS:
                    res = bt(px, book(px, g, con), cost_bps=COST_BPS, cad=cad)
                    r10 = res["returns"].loc[start:]
                    turn = res["turnover"].loc[start:]
                    r0 = r10 + turn * COST_BPS / 1e4
                    grs = res["weights"].loc[start:].sum(axis=1)
                    s = stat(r10)
                    arms[con] = dict(r10=r10, r0=r0, gross=grs, s=s, turn=turn)
                    rows.append(dict(theta=th, x=float(M.loc[M.theta == th, "x"].iloc[0]),
                                     cad=cad, family=fam, con=con, **s, CAGR0=cagr(r0),
                                     gross_mean=float(grs.mean()), gross_min=float(grs.min()),
                                     turn_yr=float(turn.sum() / years),
                                     dCAGR_ctrl=s["CAGR"] - ctrl[cad]["CAGR"],
                                     dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                     p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())

                def dec(lo, hi, tag, rs=rs, dg=dg, c_t=c_t):
                    sl = slice(lo, hi)
                    rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                    cb = float(c_t.loc[sl].mean())
                    g0 = 100 * (cagr(rd) - cagr(rr))
                    p0 = 100 * (cagr(cb * rr) - cagr(rr))
                    return dict(window=tag, c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                                CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd))

                base = dict(theta=th, cad=cad, family=fam, ident_max_err=ident)
                cells = {}
                for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                    ("OOS", OOS_START, None)):
                    d = dec(lo, hi, tag)
                    cells[tag] = d
                    decomp.append({**base, **d})
                got[fam] = dict(arms=arms, cells=cells)

            for con in CONSTRUCTIONS:
                a = got["MA-THRESH"]["arms"][con]["s"]
                b = got["QUANTILE-M"]["arms"][con]["s"]
                pair.append(dict(
                    theta=th, cad=cad, con=con,
                    c_bar_ma=got["MA-THRESH"]["cells"]["FULL"]["c_bar"],
                    c_bar_q=got["QUANTILE-M"]["cells"]["FULL"]["c_bar"],
                    d_c_bar=got["QUANTILE-M"]["cells"]["FULL"]["c_bar"]
                    - got["MA-THRESH"]["cells"]["FULL"]["c_bar"],
                    Sharpe_ma=a["Sharpe"], Sharpe_q=b["Sharpe"],
                    dSharpe=a["Sharpe"] - b["Sharpe"],
                    dCAGR_pp=100 * (a["CAGR"] - b["CAGR"]),
                    dMaxDD_pp=100 * (a["MaxDD"] - b["MaxDD"]),
                    dSharpe_oos=a["oSharpe"] - b["oSharpe"],
                    resid0_ma=got["MA-THRESH"]["cells"]["FULL"]["resid0_pp"],
                    resid0_q=got["QUANTILE-M"]["cells"]["FULL"]["resid0_pp"],
                    turn_ma=float(got["MA-THRESH"]["arms"][con]["turn"].sum() / years),
                    turn_q=float(got["QUANTILE-M"]["arms"][con]["turn"].sum() / years),
                ))
        P(f"  ... theta {th:+.2f} done ({len(CADENCES) * 4} books)")
        flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    PR = pd.DataFrame(pair)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    F = D[D.window == "FULL"].copy()
    O = D[D.window == "OOS"].copy()
    IS_ = D[D.window == "IS"].copy()

    # --------------------------------------------- G0.2 / G0.3
    P("\n" + "=" * 175)
    P("G0.2  REPRODUCTION of idea 300's committed .decomp.csv at W/M/Q")
    P("=" * 175)
    prior = pd.read_csv(PRIOR300)
    key = ["theta", "cad", "family", "window"]
    mine = D[D.cad.isin(INTERIOR)][key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]]
    j = prior[key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]].merge(
        mine, on=key, suffixes=("_300", "_307"))
    d_resid = (j.resid0_pp_300 - j.resid0_pp_307).abs()
    d_cbar = (j.c_bar_300 - j.c_bar_307).abs()
    ok_g02 = bool(len(j) == 162 and d_resid.max() < BAR_REPRO)
    P(f"matched cells {len(j)} of 162 committed | worst |d resid0| = {d_resid.max():.3e} pp/yr | "
      f"worst |d c_bar| = {d_cbar.max():.3e}")
    P(f"G0.2 {'PASS' if ok_g02 else 'FAIL'} at {BAR_REPRO:.0e}")
    P("\nG0.3  IDENTITY r_dg,t == c_t * r_rs,t at 0 bps, BY CADENCE")
    idt = F.groupby("cad").ident_max_err.max().reindex(CADENCES)
    P(idt.to_string(float_format=lambda x: f"{x:.3e}"))
    ok_g03 = bool(idt.max() < BAR_IDENT)
    P(f"G0.3 {'PASS' if ok_g03 else 'FAIL'}  worst {idt.max():.3e} at {BAR_IDENT:.0e}")
    P("")
    P(f"GATES: G0.1 {'PASS' if ok_g01 else 'FAIL'} | G0.2 {'PASS' if ok_g02 else 'FAIL'} | "
      f"G0.3 {'PASS' if ok_g03 else 'FAIL'} | G0.4 {'PASS' if ok_g04 else 'FAIL'}")
    flush_log()

    # --------------------------------------------- THE HEADLINE
    P("\n" + "=" * 175)
    P("THE HEADLINE - resid0 (pp/yr) BY CADENCE, FULL SAMPLE.  QUANTILE-M is the claimed ZERO.")
    P("=" * 175)
    piv = F.pivot_table(index="theta", columns=["family", "cad"], values="resid0_pp")
    piv = piv.reindex(columns=pd.MultiIndex.from_product([FAMILIES, CADENCES]))
    P(fmt(piv, 4))
    summ = []
    for fam in FAMILIES:
        for cad in CADENCES:
            for tag, W in (("FULL", F), ("IS", IS_), ("OOS", O)):
                v = W[(W.family == fam) & (W.cad == cad)].resid0_pp
                cb = W[(W.family == fam) & (W.cad == cad)].c_bar
                cs = W[(W.family == fam) & (W.cad == cad)].c_sd
                summ.append(dict(family=fam, cad=cad, window=tag, n=len(v),
                                 mean_resid0=v.mean(), sd_resid0=v.std(),
                                 max_abs_resid0=v.abs().max(), min_resid0=v.min(),
                                 max_resid0=v.max(), n_pos=int((v > 0).sum()),
                                 mean_c_bar=cb.mean(), mean_c_sd=cs.mean()))
    S = pd.DataFrame(summ)
    S.to_csv(f"{OUT}.cadence.csv", index=False)
    P("\nBY CADENCE (n = 9 thetas per cell):")
    P(fmt(S.set_index(["family", "cad", "window"]), 4))
    flush_log()

    # --------------------------------------------- verdict on the pre-registered bars
    P("\n" + "=" * 175)
    P("PRE-REGISTERED VERDICT  (QUANTILE-M only; MA-THRESH is the contrast)")
    P("=" * 175)
    Q = S[S.family == "QUANTILE-M"].set_index(["cad", "window"])
    clauses, details = {}, []
    for cad in EXTREMES:
        m_full = Q.loc[(cad, "FULL"), "mean_resid0"]
        x_full = Q.loc[(cad, "FULL"), "max_abs_resid0"]
        m_oos = Q.loc[(cad, "OOS"), "mean_resid0"]
        clauses[f"(1) |mean FULL resid0| <= {BAR_ZERO_MEAN} at {cad}"] = abs(m_full) <= BAR_ZERO_MEAN
        clauses[f"(2) max |resid0| <= {BAR_ZERO_MAX} at {cad}"] = x_full <= BAR_ZERO_MAX
        clauses[f"(3) |mean OOS resid0| <= {BAR_ZERO_MEAN} at {cad}"] = abs(m_oos) <= BAR_ZERO_MEAN
        details.append(dict(cad=cad, mean_full=m_full, max_abs_full=x_full, mean_oos=m_oos))
    env = Q.loc[[(c, "FULL") for c in INTERIOR], "mean_resid0"]
    lo, hi = env.min() - BAR_ENVELOPE, env.max() + BAR_ENVELOPE
    for cad in EXTREMES:
        m_full = Q.loc[(cad, "FULL"), "mean_resid0"]
        clauses[f"(4) mean FULL resid0 inside W/M/Q envelope [{lo:.4f},{hi:.4f}] at {cad}"] = \
            bool(lo <= m_full <= hi)
    for k, v in clauses.items():
        P(f"  {'PASS' if v else 'FAIL':4s}  {k}")
    P(fmt(pd.DataFrame(details).set_index("cad"), 4))
    zero_holds = all(clauses.values())
    P("")
    P(f"H_ZERO_IS_A_CONTROL : {'HOLDS' if zero_holds else 'FAILS'}")
    P(f"H_ZERO_IS_INTERIOR  : {'FAILS' if zero_holds else 'HOLDS'}")
    P("")
    P("CONTRAST - MA-THRESH, the gate known NOT to be zero:")
    P(fmt(S[(S.family == "MA-THRESH") & (S.window == "FULL")]
          .set_index("cad")[["mean_resid0", "sd_resid0", "max_abs_resid0", "mean_c_bar", "mean_c_sd"]], 4))
    sep = []
    for cad in CADENCES:
        qm = Q.loc[(cad, "FULL"), "mean_resid0"]
        am = S[(S.family == "MA-THRESH") & (S.cad == cad) & (S.window == "FULL")].mean_resid0.iloc[0]
        qs = Q.loc[(cad, "FULL"), "sd_resid0"]
        sep.append(dict(cad=cad, resid0_Q=qm, resid0_MA=am, gap_pp=am - qm,
                        gap_in_Q_sd=(am - qm) / qs if qs else np.nan))
    SEP = pd.DataFrame(sep).set_index("cad")
    P("\nSEPARATION - is QUANTILE-M still distinguishable from MA-THRESH at the extremes?")
    P(fmt(SEP, 4))
    flush_log()

    # --------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 175)
    P("RULE 8 WALK-FORWARD  (IS 2010..2016-12-31 chooses; OOS 2017-01-01..2026 read once)")
    P("=" * 175)
    wf = []
    P("\nWF-A  (theta, cadence) chosen by IS Sharpe inside each family x construction arm")
    for fam in FAMILIES:
        for con in CONSTRUCTIONS:
            sub = G[(G.family == fam) & (G.con == con)]
            pick = sub.loc[sub.isSharpe.idxmax()]
            ct = ctrl[pick.cad]
            wf.append(dict(test="WF-A", arm=f"{fam}/{con}", pick=f"theta={pick.theta:+.2f},cad={pick.cad}",
                           isSharpe=pick.isSharpe, oSharpe=pick.oSharpe, oCAGR=pick.oCAGR,
                           oMaxDD=pick.oMaxDD, vs_SPY=pick.oSharpe - spy_s["oSharpe"],
                           vs_RULESv2=pick.oSharpe - live_s["oSharpe"],
                           vs_ctrl=pick.oSharpe - ct["oSharpe"],
                           vs_ctrl_CAGR_pp=100 * (pick.oCAGR - ct["oCAGR"]),
                           best_oSharpe_in_arm=sub.oSharpe.max(),
                           regret=sub.oSharpe.max() - pick.oSharpe))
    WA = pd.DataFrame([w for w in wf if w["test"] == "WF-A"]).set_index("arm")
    P(fmt(WA.drop(columns=["test"]), 4))
    P(f"SPY OOS Sharpe {spy_s['oSharpe']:.4f} CAGR {spy_s['oCAGR']:.4f} MaxDD {spy_s['oMaxDD']:.4f} | "
      f"RULES v2 OOS Sharpe {live_s['oSharpe']:.4f} CAGR {live_s['oCAGR']:.4f} MaxDD {live_s['oMaxDD']:.4f}")

    P("\nWF-B  the CADENCE dial itself: IS-best cadence vs each always-CAD, per family x construction")
    wb = []
    for fam in FAMILIES:
        for con in CONSTRUCTIONS:
            sub = G[(G.family == fam) & (G.con == con)]
            by = sub.groupby("cad")[["isSharpe", "oSharpe"]].max()
            pick_cad = by.isSharpe.idxmax()
            row = dict(arm=f"{fam}/{con}", IS_pick=pick_cad,
                       OOS_of_pick=by.loc[pick_cad, "oSharpe"],
                       OOS_best_cad=by.oSharpe.idxmax(), OOS_best=by.oSharpe.max(),
                       agree=bool(pick_cad == by.oSharpe.idxmax()))
            for cad in CADENCES:
                row[f"always_{cad}"] = by.loc[cad, "oSharpe"]
            wb.append(row)
            wf.append(dict(test="WF-B", **row))
    WB = pd.DataFrame(wb).set_index("arm")
    P(fmt(WB, 4))
    P(f"IS->OOS cadence agreement: {int(WB.agree.sum())}/{len(WB)}")

    P("\nWF-C  does the IS resid0 predict the OOS resid0 better than a hard ZERO?  (MAE, pp/yr)")
    wc = []
    for fam in FAMILIES:
        for cad in CADENCES:
            i = IS_[(IS_.family == fam) & (IS_.cad == cad)].set_index("theta").resid0_pp
            o = O[(O.family == fam) & (O.cad == cad)].set_index("theta").resid0_pp
            mae_zero = o.abs().mean()
            mae_is = (o - i).abs().mean()
            mae_const = (o - i.mean()).abs().mean()
            row = dict(family=fam, cad=cad, mean_is=i.mean(), mean_oos=o.mean(),
                       MAE_vs_zero=mae_zero, MAE_vs_IS_cell=mae_is,
                       MAE_vs_IS_const=mae_const,
                       zero_wins=bool(mae_zero <= min(mae_is, mae_const)),
                       sign_agree=int((np.sign(i) == np.sign(o)).sum()))
            wc.append(row)
            wf.append(dict(test="WF-C", **row))
    WC = pd.DataFrame(wc).set_index(["family", "cad"])
    P(fmt(WC, 4))
    P(f"ZERO is the best available predictor of OOS resid0 in "
      f"{int(WC.zero_wins.sum())}/{len(WC)} family x cadence cells "
      f"({int(WC.loc['QUANTILE-M'].zero_wins.sum())}/5 on QUANTILE-M).")
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)
    flush_log()

    # --------------------------------------------- KEEP paths
    P("\n" + "=" * 175)
    P("BOTH KEEP PATHS over all 180 books")
    P("=" * 175)
    P(f"4a passes: {int(G.p4a.sum())}/{len(G)}   4b passes: {int(G.p4b.sum())}/{len(G)}   "
      f"BOTH: {int((G.p4a & G.p4b).sum())}/{len(G)}")
    P("\n4b failing clauses, count over 180 books:")
    fc = pd.Series([c for s in G.f4b for c in (s.split(",") if s != "-" else [])]).value_counts()
    P(fc.to_string())
    P("\nby cadence (books = 36 each):")
    P(fmt(G.groupby("cad")[["p4a", "p4b"]].sum().reindex(CADENCES), 0))
    P("\nbest book per cadence by full-sample Sharpe:")
    best = G.loc[G.groupby("cad").Sharpe.idxmax()].set_index("cad")
    P(fmt(best.reindex(CADENCES)[["theta", "family", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                  "oSharpe", "turn_yr", "p4a", "f4b"]], 4))
    if int(G.p4a.sum()) or int(G.p4b.sum()):
        P("\nevery passing book:")
        P(fmt(G[G.p4a | G.p4b][["theta", "cad", "family", "con", "CAGR", "Sharpe", "MaxDD",
                                "H1", "H2", "oSharpe", "p4a", "f4b"]], 4))

    # --------------------------------------------- leaderboard rows
    P("\n" + "=" * 175)
    P("LEADERBOARD rows")
    P("=" * 175)
    fn = Path(__file__).name
    lb = []
    for cad in CADENCES:
        sub = G[(G.family == "QUANTILE-M") & (G.con == "DEGROSS") & (G.cad == cad)]
        b = sub.loc[sub.Sharpe.idxmax()]
        q = Q.loc[(cad, "FULL")]
        v = "KILL" if not (b.p4a or b.p4b) else ("KEEP-candidate" if (b.p4a and b.p4b) else "PARK")
        lb.append(f"| 2026-09-09 | idea307 QUANTILE-M DEGROSS cad={cad} (best theta {b.theta:+.2f}) "
                  f"resid0 {q.mean_resid0:+.4f} pp/yr (max |{q.max_abs_resid0:.4f}|) | {b.CAGR:.1%} | "
                  f"{b.Sharpe:.2f} | {b.MaxDD:.1%} | {b.H1:.2f} / {b.H2:.2f} | "
                  f"{live_s['Sharpe']:.2f} ({live_s['H1']:.2f}/{live_s['H2']:.2f}) | {v} | {fn} |")
    for cad in EXTREMES:
        sub = G[(G.family == "MA-THRESH") & (G.con == "DEGROSS") & (G.cad == cad)]
        b = sub.loc[sub.Sharpe.idxmax()]
        am = S[(S.family == "MA-THRESH") & (S.cad == cad) & (S.window == "FULL")].iloc[0]
        v = "KILL" if not (b.p4a or b.p4b) else ("KEEP-candidate" if (b.p4a and b.p4b) else "PARK")
        lb.append(f"| 2026-09-09 | idea307 MA-THRESH DEGROSS cad={cad} (contrast, best theta "
                  f"{b.theta:+.2f}) resid0 {am.mean_resid0:+.4f} pp/yr | {b.CAGR:.1%} | {b.Sharpe:.2f} | "
                  f"{b.MaxDD:.1%} | {b.H1:.2f} / {b.H2:.2f} | "
                  f"{live_s['Sharpe']:.2f} ({live_s['H1']:.2f}/{live_s['H2']:.2f}) | {v} | {fn} |")
    for r in lb:
        P(r)
    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(lb) + "\n")

    P("\n" + "=" * 175)
    P("ANSWER")
    P("=" * 175)
    P(f"QUANTILE-M mean resid0 (FULL, pp/yr): " +
      ", ".join(f"{c}={Q.loc[(c, 'FULL'), 'mean_resid0']:+.4f}" for c in CADENCES))
    P(f"QUANTILE-M max|resid0| (FULL, pp/yr): " +
      ", ".join(f"{c}={Q.loc[(c, 'FULL'), 'max_abs_resid0']:.4f}" for c in CADENCES))
    P(f"QUANTILE-M mean resid0 (OOS,  pp/yr): " +
      ", ".join(f"{c}={Q.loc[(c, 'OOS'), 'mean_resid0']:+.4f}" for c in CADENCES))
    P(f"MA-THRESH  mean resid0 (FULL, pp/yr): " +
      ", ".join(f"{c}={S[(S.family=='MA-THRESH')&(S.cad==c)&(S.window=='FULL')].mean_resid0.iloc[0]:+.4f}"
                for c in CADENCES))
    P(f"H_ZERO_IS_A_CONTROL {'HOLDS' if zero_holds else 'FAILS'}; "
      f"H_ZERO_IS_INTERIOR {'FAILS' if zero_holds else 'HOLDS'}.")
    P(f"KEEP paths: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}, "
      f"BOTH {int((G.p4a & G.p4b).sum())}/{len(G)}.")
    flush_log()


if __name__ == "__main__":
    main()
