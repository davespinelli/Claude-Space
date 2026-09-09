#!/usr/bin/env python3
"""Idea 552 - "is-the-ANNUAL-collapse-a-JENSEN-artefact-of-the-c_bar-PREDICTOR"
(cloud, 2026-09-09).

The question
------------
Idea 551 found that the MA-minus-QUANTILE separation of the exposure-timing residual collapses
to +0.0539 (U56) / -0.0456 (B136) / +0.0162 (SMALL439) pp/yr at ANNUAL cadence on all three
panels, against interior (D/W/M/Q) cells of -0.23 to -0.70, and read that as "at annual the MA
gate is indistinguishable from a pure-exposure gate".

But the decomposition it read that off is

    gap0   = CAGR(DEGROSS, 0 bps) - CAGR(RESPREAD, 0 bps)
    pred0  = CAGR(c_bar * RESPREAD, 0 bps) - CAGR(RESPREAD, 0 bps)      c_bar = MEAN(c_t)
    resid0 = gap0 - pred0

and `c_bar` is the ARITHMETIC mean of the exposure path against a CAGR, which is a geometric
object.  At annual cadence the mask is a step function held for a whole calendar year, so the
dispersion of c_t inside the window is at its largest and the AM-vs-GM gap is at its largest
too.  The queue asks:

  QUEUE'S EXACT TEST: re-run the decomposition with a compounding-consistent predictor
  (geometric / log c_t) and report whether the annual break survives, on all three panels.

What resid0 actually is (proved here as gate G3, not asserted)
--------------------------------------------------------------
The two constructions differ only by the exposure path: r_dg,t = c_t * r_rs,t exactly (gate G1).
So

    resid0 = CAGR(c_t * r_rs) - CAGR(c * r_rs)

for whatever scalar c the predictor uses: resid0 is ENTIRELY the difference between scaling by
the PATH and scaling by a CONSTANT.  Which constant is therefore not a detail of the estimator,
it is half the definition of the statistic - and the record has only ever used one.

The dials (exactly 2, as the queue specifies, both fully reported)
-----------------------------------------------------------------
    PREDICTOR FORM (dial 1)  five zero-parameter location estimators of the SAME path c_t, none
        of which may look at returns (a constant fitted to r would absorb the timing term it is
        supposed to measure and the whole decomposition would be circular):
            ARITH   mean(c_t)                          - the record's own
            GEO     exp(mean(log c_t))                 - the queue's compounding-consistent one
            HARM    1 / mean(1 / c_t)
            MEDIAN  median(c_t)
            JADJ    mean(c_t) - var(c_t) / (2*mean(c_t))  - the AM->GM second-order correction,
                    which is GEO to second order but stays defined when c_t touches zero
        AM >= GEO >= HARM holds cell by cell (gate G2).  A sixth form, PATH (c_t itself), is
        carried as gate G3: it must reproduce gap0 exactly, i.e. drive resid0 to 0.
    CADENCE (dial 2)  D, W, M, Q, A - idea 551's own grid verbatim.
    Nothing is selected on either dial outside rule 8; every one of the 5 x 5 combinations is
    printed for every panel, family and construction.

theta (9 values, idea 298/300/305/551's grid verbatim) and PANEL (3) are NOT dials here: the
published statistic idea 551 reported IS a 9-theta mean per panel, so reproducing and
restating it requires the same grid.  Both are reported at every level and selected at none
outside rule 8.

    Grid: 3 panels x 9 theta x 5 cadences x 3 families x 2 constructions = 810 books,
    each decomposed under 5 predictor forms x 3 windows.  ALL points written to .decomp.csv.

Families
    MA-THRESH   IN where px > ma200*(1+theta).
    QUANTILE-M  same ranking (dist = px/ma200 - 1), top ceil(x*n_t) names, x = the MA arm's own
                mean mask fraction.  Idea 551's control, carried so R1 can reproduce its
                published separation on the arm it actually used.
    QUANTILE-F  the same control with the marginal name fractionally weighted so the mask
                fraction is EXACTLY x every day.  Idea 551's own gate G0.5 FAILED for
                QUANTILE-M on U56 (0.01396 against a 0.01 bar, the ceil() granularity floor at
                n=55); QUANTILE-F is idea 305's fix for it and is the matched restatement here.
    Both controls are reported side by side; the headline is read on both.

Constructions: RESPREAD (w = g/k_t, gross pinned) and DEGROSS (w = g/n_t, gated weight to
cash).  Gross 0.75, 10 bps, next-day execution, no shorting, no leverage; the 0-bps rung every
residual uses is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run.

Pre-registered hypotheses and bars (written before any predictor-form number was read)
--------------------------------------------------------------------------------------
Define, per panel and predictor form, the COLLAPSE RATIO

    R = |sep_A| / min over c in {D,W,M,Q} of |sep_c|,     sep_c = resid0_MA - resid0_QUANTILE

"the annual collapse is present" means R < 0.5.  Under the record's ARITH predictor idea 551's
own numbers give R = 0.234 (U56), 0.137 (B136), 0.181 (SMALL439) - present on all three, which
is what R1 must reproduce.

H_JENSEN.  The collapse is an artefact of the arithmetic predictor.  BAR: under the
    compounding-consistent GEO predictor, R >= 0.5 on ALL THREE panels.
H_REAL.  R < 0.5 under GEO on at least one panel: the annual break is a property of the gate,
    not of the estimator, and idea 551's reading stands (with the predictor named).
Exhaustive and mutually exclusive.  R is reported for all five forms on all three panels and
both controls whichever side it falls, and the JENSEN TERM pred0(ARITH) - pred0(GEO) is
reported per cadence, because that term is the whole mechanism under test.

Reproduction gates (a FAIL is reported, not repaired)
-----------------------------------------------------
    G0  the cadence-extended runner (D/W/M/Q/A) matches engine.backtest on returns AND turnover
        at D/W/M/Q (engine has no A), every panel: < 1e-12.
    G1  identity r_dg,t = c_t * r_rs,t at 0 bps in every cell: < 1e-12.
    G2  AM >= GEO >= HARM in every decomposition cell (a violation is an arithmetic bug).
    G3  the PATH predictor drives resid0 to 0 in every cell: < 1e-12.  This is the proof that
        resid0 is a constant-vs-path statistic and nothing else.
    R1  reproduce idea 551's published FULL-sample ARITH numbers, MA-THRESH resid0 (15 cells)
        and the MA-minus-QUANTILE-M separation (15 cells), to 0.01 pp/yr.  Idea 551 itself
        documented a data-vintage drift of ~8e-4 pp/yr on U56 (data/prices.csv refreshes daily,
        the broad and small caches weekly), so the bar is set above that drift, not at machine
        precision, and the realised gap is reported.

Rule 8 walk-forward (required; every direction fixed before any OOS number was read)
------------------------------------------------------------------------------------
    IS = start..2016-12-31 (selection), OOS = 2017-01-01..end (read once).
    WF-A (statistic)  the collapse ratio R computed on the IS window alone and then read once
        on the untouched OOS window, per panel x predictor form.  A break that is a property of
        the gate replicates; one that is a property of 2008-2016 does not.
    WF-B (book)       (theta, cadence) chosen on IS Sharpe inside each panel x family x
        construction arm; OOS CAGR/Sharpe/MaxDD read once against RULES v2 (live), SPY and the
        cadence-matched no-gate EWall control on the same panel.

Verdicts (both KEEP paths, on every one of the 810 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: B136 (research/universe_broad.json) and SMALL439 (data/prices_small.csv.gz) are
CURRENT constituents - no delistings - so every CAGR LEVEL on those panels, and both KEEP
columns, are inflated.  resid0 and the separation are arm-minus-arm contrasts on the SAME
names, the SAME ranking and the SAME days, so the bias very largely cancels out of them.
SMALL439: tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped first.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .sep.csv .jensen.csv .walkforward.csv .keeppaths.csv
.console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
GROSS = 0.75
CADENCES = ["D", "W", "M", "Q", "A"]
INTERIOR = ["D", "W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M", "QUANTILE-F"]
CONTROLS = ["QUANTILE-M", "QUANTILE-F"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FORMS = ["ARITH", "GEO", "HARM", "MEDIAN", "JADJ"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

COLLAPSE = 0.50              # R < 0.50 == "the annual collapse is present"
BAR_IDENT = 1e-12
R1_TOL = 0.01                # pp/yr
EPS = 1e-9

# idea 551's published FULL-sample ARITH numbers (pp/yr)
R1_RESID = {  # MA-THRESH mean resid0
    ("U56", "D"): -0.2636, ("U56", "W"): -0.4439, ("U56", "M"): -0.2957,
    ("U56", "Q"): -0.2728, ("U56", "A"): +0.0727,
    ("B136", "D"): -0.3776, ("B136", "W"): -0.4688, ("B136", "M"): -0.3723,
    ("B136", "Q"): -0.4284, ("B136", "A"): -0.0843,
    ("SMALL439", "D"): -0.0904, ("SMALL439", "W"): -0.2164, ("SMALL439", "M"): -0.2416,
    ("SMALL439", "Q"): -0.6871, ("SMALL439", "A"): -0.1078,
}
R1_SEP = {  # MA-THRESH minus QUANTILE-M
    ("U56", "D"): -0.2606, ("U56", "W"): -0.4325, ("U56", "M"): -0.2562,
    ("U56", "Q"): -0.2306, ("U56", "A"): +0.0539,
    ("B136", "D"): -0.3773, ("B136", "W"): -0.4573, ("B136", "M"): -0.3317,
    ("B136", "Q"): -0.3842, ("B136", "A"): -0.0456,
    ("SMALL439", "D"): -0.0897, ("SMALL439", "W"): -0.2070, ("SMALL439", "M"): -0.2025,
    ("SMALL439", "Q"): -0.6985, ("SMALL439", "A"): +0.0162,
}

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- cadence + backtest
def rmask(idx, freq):
    """engine.rebalance_mask extended with 'A' (last trading day of each calendar year)."""
    if freq == "A":
        s = pd.Series(idx.to_period("Y"), index=idx)
        return s != s.shift(-1)
    return rebalance_mask(idx, freq)


def fast_backtest(px, weights, freq):
    """Vectorised twin of engine.backtest at ZERO cost, with the A cadence; gated in G0."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rmask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n)
    turn = np.zeros(n)
    gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(gross, index=idx))


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def dist_rank(px):
    return (px / px.rolling(200).mean() - 1).where(live_mask(px))


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    dist = dist_rank(px)
    live = live_mask(px)
    kt = np.ceil(x * live.sum(axis=1)).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return (rank.le(kt, axis=0).fillna(False) & live).astype(float)


def quantile_gate_frac(px, x):
    dist = dist_rank(px)
    live = live_mask(px)
    kf = x * live.sum(axis=1)
    kfl = np.floor(kf)
    rank = dist.rank(axis=1, ascending=False, method="first")
    full = (rank.le(kfl, axis=0).fillna(False) & live).astype(float)
    marg = (rank.eq(kfl + 1, axis=0).fillna(False) & live).astype(float)
    return full + marg.mul(kf - kfl, axis=0)


def book(px, g, construction):
    gf = g.astype(float)
    if construction == "RESPREAD":
        return gf.div(gf.sum(axis=1).clip(lower=1e-12), axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return gf.div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def cagr(r):
    return (1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1


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


def constants(c):
    """The five zero-parameter location estimators of the exposure path, plus diagnostics.
    None of them looks at returns."""
    v = c.values.astype(float)
    am = float(np.mean(v))
    pos = v[v > EPS]
    zshare = float((v <= EPS).mean())
    geo = float(np.exp(np.mean(np.log(pos)))) if len(pos) else np.nan
    harm = float(1.0 / np.mean(1.0 / pos)) if len(pos) else np.nan
    if zshare > 0:                      # GEO/HARM are undefined on a support containing zero
        geo *= (1 - zshare)             # the zero mass contributes zero growth in exposure
        harm *= (1 - zshare)
    med = float(np.median(v))
    jadj = am - float(np.var(v)) / (2 * am) if am > EPS else am
    return dict(ARITH=am, GEO=geo, HARM=harm, MEDIAN=med, JADJ=jadj), zshare, float(np.std(v))


# ---------------------------------------------------------------- panels
def panels():
    out = {}
    u = load_universe()
    out["U56"] = (u.drop(columns=["SPY"]), u["SPY"])
    b = load_universe(broad=True)
    out["B136"] = (b.drop(columns=["SPY"], errors="ignore"), b["SPY"])
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out["SMALL439"] = (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])
    return out, len(bad)


# ---------------------------------------------------------------- main
def main():
    PN, n_dropped = panels()

    P("=" * 180)
    P("Idea 552 is-the-ANNUAL-collapse-a-JENSEN-artefact-of-the-c_bar-PREDICTOR (cloud) | "
      + Path(__file__).name)
    P("=" * 180)
    P("QUESTION: idea 551's MA-minus-QUANTILE separation collapses at ANNUAL (+0.0539 U56 / "
      "-0.0456 B136 / +0.0162 SMALL439 pp/yr).")
    P("          pred0 uses the ARITHMETIC mean of c_t against a CAGR.  Does the annual break "
      "survive a compounding-consistent predictor?")
    P("WHAT resid0 IS: r_dg,t = c_t*r_rs,t exactly, so resid0 = CAGR(c_t*r_rs) - CAGR(c*r_rs) "
      "- entirely a PATH-vs-CONSTANT statistic (gate G3).")
    P(f"PRE-REGISTERED  collapse ratio R = |sep_A| / min_(D,W,M,Q) |sep_c|; 'collapse present' "
      f"means R < {COLLAPSE}.")
    P(f"                H_JENSEN : under GEO, R >= {COLLAPSE} on ALL THREE panels (the collapse "
      f"is the estimator's).")
    P(f"                H_REAL   : R < {COLLAPSE} under GEO on at least one panel (the break is "
      f"the gate's).")
    P(f"dials (2, the queue's own): predictor form {FORMS} x cadence {CADENCES}.  theta "
      f"({len(MA_THETA)}) and panel ({len(PANELS)}) are the published")
    P("                 statistic's own domain - reported at every level, selected at none "
      "outside rule 8.")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), gross "
      f"{GROSS}, next-day execution, no shorting, no leverage.")
    P(f"grid: {len(PANELS)} panels x {len(MA_THETA)} theta x {len(CADENCES)} cadences x "
      f"{len(FAMILIES)} families x {len(CONSTRUCTIONS)} constructions = "
      f"{len(PANELS) * len(MA_THETA) * len(CADENCES) * len(FAMILIES) * len(CONSTRUCTIONS)} "
      f"books, each decomposed under {len(FORMS)} forms x 3 windows.  ALL points reported.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only - CAGR LEVELS and both "
      "KEEP columns inflated; arm-minus-arm")
    P(f"              contrasts very largely immune.  SMALL439 drops {n_dropped} tickers with "
      f"max_1d_move >= 1.0.")
    for pn in PANELS:
        px, _ = PN[pn]
        P(f"  PANEL {pn:9s}: {px.shape[1]:3d} names, {px.index[0].date()}..{px.index[-1].date()}"
          f", {len(px)} bars")
    flush_log()

    # ------------------------------------------------- G0
    P("\n" + "=" * 180)
    P("G0 - cadence-extended runner vs engine.backtest at D/W/M/Q (engine has no A), "
      "MA-THRESH theta 0.00 DEGROSS")
    P("=" * 180)
    g0 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        w = book(px, ma_gate(px, 0.0), "DEGROSS")
        errs = []
        for cad in INTERIOR:
            r_f, t_f, _ = fast_backtest(px, w, cad)
            eng = backtest(px, w, cost_bps=0.0, freq=cad)
            e = max(float((r_f - eng["returns"]).abs().max()),
                    float((t_f - eng["turnover"]).abs().max()))
            errs.append(e)
            g0 = max(g0, e)
        P(f"  {pn:9s} " + "  ".join(f"{c} {e:.3e}" for c, e in zip(INTERIOR, errs)))
    nA = {pn: int(rmask(PN[pn][0].index, "A").sum()) for pn in PANELS}
    P(f"  A cadence rebalance counts: " + "  ".join(f"{k} {v}" for k, v in nA.items()))
    P(f"G0 {'PASS' if g0 < BAR_IDENT else 'FAIL'} (max {g0:.3e} < {BAR_IDENT:.0e})")
    flush_log()

    # ------------------------------------------------- the grid
    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp = [], []
    ident_max = 0.0
    spy_by, live_by, ctrl_by = {}, {}, {}

    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        spy_by[pn], live_by[pn] = spy_s, live_s

        ctrl = {}
        for cad in CADENCES:
            r0c, tc, _ = fast_backtest(px, control_book(px), cad)
            ctrl[cad] = stat((r0c - tc * COST_BPS / 1e4).loc[start:])
        ctrl_by[pn] = ctrl

        P("\n" + "=" * 180)
        P(f"PANEL {pn} - comparands over {start.date()}..{px.index[-1].date()} "
          f"({years:.2f} yrs)")
        P("=" * 180)
        P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe "
          f"{spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/"
          f"{spy_s['H2']:.4f} OOS {spy_s['oSharpe']:.4f}")
        P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe "
          f"{live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/"
          f"{live_s['H2']:.4f} OOS {live_s['oSharpe']:.4f}")
        for cad in CADENCES:
            P(f"CONTROL EWall {cad} (no gate)   : CAGR {ctrl[cad]['CAGR']:.4f} Sharpe "
              f"{ctrl[cad]['Sharpe']:.4f} MaxDD {ctrl[cad]['MaxDD']:.4f}")
        P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70 * spy_s['CAGR']:.2%}")
        flush_log()

        live = live_mask(px).loc[start:]
        nlive = live.sum(axis=1)
        gates, xs = {}, {}
        for th in MA_THETA:
            gm = ma_gate(px, th)
            x = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gates[th] = {"MA-THRESH": gm.astype(float),
                         "QUANTILE-M": quantile_gate(px, x),
                         "QUANTILE-F": quantile_gate_frac(px, x)}
            xs[th] = x

        for th in MA_THETA:
            for cad in CADENCES:
                for fam in FAMILIES:
                    arms = {}
                    for con in CONSTRUCTIONS:
                        r0, turn, grs = fast_backtest(px, book(px, gates[th][fam], con), cad)
                        r0, turn, grs = r0.loc[start:], turn.loc[start:], grs.loc[start:]
                        r10 = r0 - turn * COST_BPS / 1e4
                        s = stat(r10)
                        arms[con] = dict(r0=r0, gross=grs, s=s, turn=turn)
                        rows.append(dict(panel=pn, theta=th, x=xs[th], cad=cad, family=fam,
                                         con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=float(grs.mean()),
                                         turn_yr=float(turn.sum() / years),
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident_max = max(ident_max,
                                    float((dg["r0"] - c_t * rs["r0"]).abs().max()))
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        sl = slice(lo, hi)
                        rr, rd, cc = rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl]
                        base = cagr(rr)
                        gap0 = 100 * (cagr(rd) - base)
                        cons, zsh, csd = constants(cc)
                        rec = dict(panel=pn, theta=th, cad=cad, family=fam, window=tag,
                                   c_bar=cons["ARITH"], c_sd=csd, zero_share=zsh,
                                   gap0_pp=gap0, CAGR_rs0=base, CAGR_dg0=cagr(rd))
                        for f in FORMS:
                            p0 = 100 * (cagr(cons[f] * rr) - base)
                            rec[f"c_{f}"] = cons[f]
                            rec[f"pred0_{f}"] = p0
                            rec[f"resid0_{f}"] = gap0 - p0
                        rec["resid0_PATH"] = gap0 - 100 * (cagr(cc * rr) - base)
                        rec["jensen_pp"] = rec["pred0_ARITH"] - rec["pred0_GEO"]
                        rec["am_ge_geo"] = cons["ARITH"] >= cons["GEO"] - 1e-12
                        rec["geo_ge_harm"] = cons["GEO"] >= cons["HARM"] - 1e-12
                        decomp.append(rec)
            P(f"  {pn}: theta {th:+.2f} done "
              f"({len(CADENCES) * len(FAMILIES) * 2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    F = D[D.window == "FULL"]

    # ------------------------------------------------- gates G1-G3, R1
    P("\n" + "=" * 180)
    P("VALIDITY AND REPRODUCTION GATES (read before the headline)")
    P("=" * 180)
    P(f"G1 identity r_dg = c_t*r_rs      : max {ident_max:.3e} (< {BAR_IDENT:.0e}) -> "
      f"{'PASS' if ident_max < BAR_IDENT else 'FAIL'}")
    ok_g2 = bool(D.am_ge_geo.all() and D.geo_ge_harm.all())
    P(f"G2 AM >= GEO >= HARM cellwise    : {int(D.am_ge_geo.sum())}/{len(D)} and "
      f"{int(D.geo_ge_harm.sum())}/{len(D)} -> {'PASS' if ok_g2 else 'FAIL'}")
    g3 = float(D.resid0_PATH.abs().max())
    P(f"G3 PATH predictor drives resid0=0: max {g3:.3e} pp/yr (< {BAR_IDENT:.0e}) -> "
      f"{'PASS' if g3 < BAR_IDENT else 'FAIL'}")
    P("   (G3 is the proof that resid0 is a CONSTANT-vs-PATH statistic and nothing else, so "
      "'which constant' is half its definition.)")
    P(f"   exposure path zero-share: max {D.zero_share.max():.5f}, mean "
      f"{D.zero_share.mean():.5f} (GEO/HARM are computed on the positive support and "
      f"re-weighted by 1 - zero_share)")

    MA = F[F.family == "MA-THRESH"]
    rp = MA.groupby(["panel", "cad"]).resid0_ARITH.mean()
    d1 = max(abs(rp[k] - v) for k, v in R1_RESID.items())
    P(f"R1a idea 551's MA resid0, 15 cells: max |d| {d1:.5f} pp/yr (< {R1_TOL}) -> "
      f"{'PASS' if d1 < R1_TOL else 'FAIL'}")
    QM = F[F.family == "QUANTILE-M"].groupby(["panel", "cad"]).resid0_ARITH.mean()
    sep_arith = rp - QM
    d2 = max(abs(sep_arith[k] - v) for k, v in R1_SEP.items())
    P(f"R1b idea 551's separation, 15 cells: max |d| {d2:.5f} pp/yr (< {R1_TOL}) -> "
      f"{'PASS' if d2 < R1_TOL else 'FAIL'}")
    P("\n  published vs this run (MA resid0 / separation, pp/yr):")
    for pn in PANELS:
        P(f"   {pn:9s} resid0  " + "  ".join(
            f"{c} {rp[(pn, c)]:+.4f} (pub {R1_RESID[(pn, c)]:+.4f})" for c in CADENCES))
        P(f"   {pn:9s} sep     " + "  ".join(
            f"{c} {sep_arith[(pn, c)]:+.4f} (pub {R1_SEP[(pn, c)]:+.4f})" for c in CADENCES))
    flush_log()

    # ------------------------------------------------- the headline
    P("\n" + "=" * 180)
    P("THE HEADLINE - separation (MA-THRESH minus control) under every predictor form, "
      "every cadence, every panel, both controls")
    P("=" * 180)
    seps, ratios = [], []
    for ctlfam in CONTROLS:
        Q = F[F.family == ctlfam].groupby(["panel", "cad"])
        for pn in PANELS:
            for form in FORMS:
                col = f"resid0_{form}"
                ma = MA[MA.panel == pn].groupby("cad")[col].mean()
                qq = F[(F.family == ctlfam) & (F.panel == pn)].groupby("cad")[col].mean()
                sep = ma - qq
                for c in CADENCES:
                    seps.append(dict(control=ctlfam, panel=pn, form=form, cad=c,
                                     sep_pp=float(sep[c]), ma_pp=float(ma[c]),
                                     ctl_pp=float(qq[c])))
                interior = min(abs(float(sep[c])) for c in INTERIOR)
                R = abs(float(sep["A"])) / interior if interior > 0 else np.inf
                ratios.append(dict(control=ctlfam, panel=pn, form=form,
                                   sep_A=float(sep["A"]), interior_min=interior,
                                   R=R, collapse=R < COLLAPSE))
    SEP = pd.DataFrame(seps)
    RAT = pd.DataFrame(ratios)
    SEP.to_csv(f"{OUT}.sep.csv", index=False)
    RAT.to_csv(f"{OUT}.ratios.csv", index=False)

    for ctlfam in CONTROLS:
        P(f"\nseparation (pp/yr), control = {ctlfam}:")
        P(fmt(SEP[SEP.control == ctlfam]
              .pivot_table(index=["panel", "form"], columns="cad", values="sep_pp")
              [CADENCES], 4))
    P("\nCOLLAPSE RATIO R = |sep_A| / min_(D,W,M,Q) |sep_c|   (R < "
      f"{COLLAPSE} == the annual collapse is present):")
    P(fmt(RAT.pivot_table(index=["control", "panel"], columns="form", values="R")[FORMS], 4))
    P("\ncollapse present? (True = collapsed)")
    P(RAT.pivot_table(index=["control", "panel"], columns="form",
                      values="collapse", aggfunc="first")[FORMS].to_string())

    geo = RAT[(RAT.form == "GEO") & (RAT.control == "QUANTILE-M")]
    h_jensen = bool((geo.R >= COLLAPSE).all())
    geoF = RAT[(RAT.form == "GEO") & (RAT.control == "QUANTILE-F")]
    h_jensen_F = bool((geoF.R >= COLLAPSE).all())
    P(f"\nPRE-REGISTERED READ (control QUANTILE-M, idea 551's own arm): GEO gives R = "
      + ", ".join(f"{r.panel} {r.R:.4f}" for r in geo.itertuples())
      + f" -> {'H_JENSEN' if h_jensen else 'H_REAL'}")
    P(f"MATCHED RESTATEMENT (control QUANTILE-F): GEO gives R = "
      + ", ".join(f"{r.panel} {r.R:.4f}" for r in geoF.itertuples())
      + f" -> {'H_JENSEN' if h_jensen_F else 'H_REAL'}")
    flush_log()

    # ------------------------------------------------- the Jensen term itself
    P("\n" + "=" * 180)
    P("THE MECHANISM - the Jensen term pred0(ARITH) - pred0(GEO), and the exposure-path "
      "dispersion that drives it, by cadence")
    P("=" * 180)
    J = (F.groupby(["panel", "family", "cad"])
         .agg(jensen_pp=("jensen_pp", "mean"), c_bar=("c_bar", "mean"),
              c_sd=("c_sd", "mean"), c_GEO=("c_GEO", "mean"),
              am_minus_geo=("c_ARITH", "mean"), zero=("zero_share", "mean"))
         .reset_index())
    J["am_minus_geo"] = J["am_minus_geo"] - J["c_GEO"]
    J.to_csv(f"{OUT}.jensen.csv", index=False)
    P(fmt(J.pivot_table(index=["panel", "family"], columns="cad",
                        values="jensen_pp")[CADENCES], 4))
    P("\nexposure-path SD c_sd by cadence (the dispersion the Jensen gap is a function of):")
    P(fmt(J.pivot_table(index=["panel", "family"], columns="cad",
                        values="c_sd")[CADENCES], 4))
    P("\nAM - GM of the exposure path itself, by cadence:")
    P(fmt(J.pivot_table(index=["panel", "family"], columns="cad",
                        values="am_minus_geo")[CADENCES], 4))
    flush_log()

    # ------------------------------------------------- rule 8
    P("\n" + "=" * 180)
    P("RULE 8 WF-A (statistic) - the collapse ratio computed on IS alone, then read once "
      "on the untouched OOS window")
    P("=" * 180)
    wfa = []
    for wtag in ("IS", "OOS"):
        W = D[D.window == wtag]
        for ctlfam in CONTROLS:
            for pn in PANELS:
                for form in FORMS:
                    col = f"resid0_{form}"
                    ma = W[(W.family == "MA-THRESH") & (W.panel == pn)].groupby("cad")[col].mean()
                    qq = W[(W.family == ctlfam) & (W.panel == pn)].groupby("cad")[col].mean()
                    sep = ma - qq
                    interior = min(abs(float(sep[c])) for c in INTERIOR)
                    R = abs(float(sep["A"])) / interior if interior > 0 else np.inf
                    wfa.append(dict(window=wtag, control=ctlfam, panel=pn, form=form,
                                    sep_A=float(sep["A"]), R=R, collapse=R < COLLAPSE))
    WA = pd.DataFrame(wfa)
    WA.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WA.pivot_table(index=["control", "panel", "form"], columns="window",
                         values="R")[["IS", "OOS"]], 4))
    agree = WA.pivot_table(index=["control", "panel", "form"], columns="window",
                           values="collapse", aggfunc="first")
    P(f"\nIS/OOS agreement on 'collapse present': "
      f"{float((agree['IS'] == agree['OOS']).mean()):.4f} over {len(agree)} "
      f"(control, panel, form) cells")
    P(agree.to_string())
    flush_log()

    P("\n" + "=" * 180)
    P("RULE 8 WF-B (book) - (theta, cadence) chosen on IS Sharpe per panel x family x "
      "construction; OOS read once")
    P("=" * 180)
    wfb = []
    for (pn, fam, con), sub in G.groupby(["panel", "family", "con"]):
        pick = sub.loc[sub.isSharpe.idxmax()]
        wfb.append(dict(panel=pn, family=fam, con=con, theta_IS=pick.theta, cad_IS=pick.cad,
                        isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                        oMaxDD=pick.oMaxDD,
                        ctl_oSharpe=ctrl_by[pn][pick.cad]["oSharpe"],
                        ctl_oCAGR=ctrl_by[pn][pick.cad]["oCAGR"],
                        spy_oSharpe=spy_by[pn]["oSharpe"], spy_oCAGR=spy_by[pn]["oCAGR"],
                        live_oSharpe=live_by[pn]["oSharpe"], live_oCAGR=live_by[pn]["oCAGR"],
                        beats_ctl=pick.oSharpe > ctrl_by[pn][pick.cad]["oSharpe"],
                        beats_spy=pick.oSharpe > spy_by[pn]["oSharpe"],
                        beats_live=pick.oSharpe > live_by[pn]["oSharpe"],
                        p4a=pick.p4a, f4b=pick.f4b))
    WB = pd.DataFrame(wfb)
    WB.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(fmt(WB, 4))
    P(f"\nbeats the no-gate EWall control OOS: {int(WB.beats_ctl.sum())}/{len(WB)} | "
      f"beats SPY {int(WB.beats_spy.sum())}/{len(WB)} | beats RULES v2 (live) "
      f"{int(WB.beats_live.sum())}/{len(WB)}")

    P("\n" + "=" * 180)
    P("KEEP PATHS over the FULL grid (both paths, every book)")
    P("=" * 180)
    P(f"4a passes: {int(G.p4a.sum())} of {len(G)}   4b passes: {int(G.p4b.sum())} of {len(G)}"
      f"   BOTH: {int((G.p4a & G.p4b).sum())}")
    P("4b failing-bar frequency (SET semantics):")
    P(fmt(G.f4b.str.split(",").explode().value_counts().to_frame("rows").T, 0))
    for tag, sub in (("4b", G[G.p4b]), ("4a", G[G.p4a])):
        P(f"\n{tag} passers (all reported):")
        P(fmt(sub[["panel", "theta", "cad", "family", "con", "CAGR", "Sharpe", "MaxDD",
                   "H1", "H2", "oSharpe"]], 4) if len(sub) else "  none")

    # ------------------------------------------------- verdict
    P("\n" + "=" * 180)
    P("VERDICT")
    P("=" * 180)
    P(f"GATES: G0 {'PASS' if g0 < BAR_IDENT else 'FAIL'}  G1 "
      f"{'PASS' if ident_max < BAR_IDENT else 'FAIL'}  G2 {'PASS' if ok_g2 else 'FAIL'}  "
      f"G3 {'PASS' if g3 < BAR_IDENT else 'FAIL'}  R1a "
      f"{'PASS' if d1 < R1_TOL else 'FAIL'}  R1b {'PASS' if d2 < R1_TOL else 'FAIL'}")
    P(f"=> {'H_JENSEN' if h_jensen else 'H_REAL'} on idea 551's own control (QUANTILE-M); "
      f"{'H_JENSEN' if h_jensen_F else 'H_REAL'} on the matched restatement (QUANTILE-F)")
    P("KEEP: no book is promoted on this run - it is a decomposition study on "
      "survivorship-inflated panels; 4a/4b are reported for PROTOCOL compliance.")
    flush_log()


if __name__ == "__main__":
    main()
