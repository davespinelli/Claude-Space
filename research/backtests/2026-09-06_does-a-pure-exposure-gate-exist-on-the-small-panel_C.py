#!/usr/bin/env python3
"""Idea 300 - "does-a-pure-exposure-gate-exist-on-the-small-panel" (lane C, 2026-09-06).

The question
------------
Idea 298 established two facts on three panels:

  * a QUANTILE gate (hold the top ceil(x*n_t) live names by px/ma200-1, so the exposure
    c_t == x BY CONSTRUCTION) has timing residual -0.017..+0.003 pp/yr and exposure share
    0.9936..1.0025 from c_bar 0.21 to 0.96.  It is PURE CASH DRAG at every strictness.
  * the record's own MA gate (px > ma200*(1+theta)) is not: its residual is a
    level-independent lump of roughly -0.3..-0.6 pp/yr.

The queue's question is whether that extra residual is a COST or a PRICE.  Both readings are
alive after idea 298, which measured the residual but never priced it:

    the residual is the CAGR the MA gate gives up relative to a constant-leverage book at the
    same mean exposure.  If the MA gate's time-varying exposure is buying downside protection,
    that CAGR is a premium paid for a better risk profile and the Sharpe should be HIGHER.
    If it is not, the MA gate is a strictly worse way to spend the same average exposure and
    the pure-exposure gate is the control the record should be using.

So: hold the ranking fixed, hold the mean exposure fixed, and vary ONLY whether the gate's
depth moves.  On SMALL439 only, per the queue.

Why this is a clean experiment (and not just two gates side by side)
-------------------------------------------------------------------
Both families order names by the SAME statistic, dist_t = px/ma200 - 1.  MA-THRESH holds
{dist_t > theta}: a prefix of that ranking whose LENGTH moves with the market.  QUANTILE holds
the top ceil(x*n_t): a prefix of the SAME ranking at CONSTANT length.  Matching x to the MA
gate's own mean mask fraction therefore removes cross-sectional selection skill and mean
exposure from the comparison and leaves exactly one difference: whether the depth is
time-varying.  That difference IS the timing residual.

Two rival hypotheses, both pre-registered with bars, before any number was read
------------------------------------------------------------------------------
H_TIMING_PAYS.  The MA gate's residual is a premium for de-grossing into weakness: it costs
    CAGR and buys risk.  BAR: mean dSharpe (MA minus matched-QUANTILE, DEGROSS, full sample)
    over the 27 cells > +0.05, AND dSharpe > 0 in >= 19/27 cells, AND mean dSharpe over the
    untouched 2017-2026 window > 0.

H_PURE_DRAG.  The residual is uncompensated: a constant-depth gate at the same mean exposure
    is as good or better, so a pure-exposure gate EXISTS on this panel and should be the
    record's control.  BAR: mean full-sample dSharpe <= 0, OR (dSharpe > 0 in < 19/27 cells
    AND |mean dSharpe| <= 0.05).

The two are mutually exclusive by construction.  Whichever wins, the deliverable is the same
table: what the MA gate's 0.3-0.6 pp/yr buys, in Sharpe and in MaxDD, cell by cell.

B_MATCH (reproduction/validity gate, asserted before any headline number is read)
    (i) matching quality: |mask-fraction(QUANTILE) - mask-fraction(MA)| < 0.01 in all 27 cells,
        and |realised c_bar difference| < 0.02 in all 27 cells.  Without this the "matched
        c_bar" claim is not true and nothing below means anything.
    (ii) idea 290's identity r_dg,t == c_t * r_rs,t at 0 bps, max |error| < 1e-12.
    (iii) idea 298's residual reading must reproduce: on the MA arms, mean resid0 must land in
        [-0.70, -0.20] pp/yr, and on the QUANTILE arms within +/-0.05 pp/yr of zero.

The exact attribution (an identity, not a fit)
----------------------------------------------
At 0 bps, for either family, CAGR0_dg = CAGR0_rs + gap0 and gap0 = pred0 + resid0, so

    CAGR0_dg(MA) - CAGR0_dg(Q)  =  [CAGR0_rs(MA) - CAGR0_rs(Q)]   <- SELECTION (slice depth)
                                +  [pred0(MA)    - pred0(Q)]      <- LEVEL (should be ~0: matched)
                                +  [resid0(MA)   - resid0(Q)]     <- TIMING (the thing at issue)

reported cell by cell and asserted to close to 1e-9.

Design
------
PANEL: SMALL439 (sub-$2B names from data/prices_small.csv.gz, the 44 with max_1d_move >= 1.0
       dropped, exactly idea 290/298's panel).  SPY joined only as a benchmark.

FAMILIES (a REPORTED contrast, not a dial - it is the object under test):
  MA-THRESH   IN where px > ma200*(1+theta).  c_bar is an outcome.
  QUANTILE-M  IN the top ceil(x*n_t) live names by dist, with x set to the MA arm's OWN mean
              mask fraction at that theta.  "M" = matched.  c_t == x by construction.

CONSTRUCTIONS (reported, both): RESPREAD (w = g/k_t * G, gross constant) and DEGROSS
  (w = g/n_t * G, gated weight to cash).  The headline is the DEGROSS pair; RESPREAD is
  carried because it isolates the selection term with exposure held at 1.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. strictness theta   (9 values, idea 298's grid verbatim)
    2. cadence            (3 values: W, M, Q)
Reported at every one of the 27 combinations; selected at none except inside the rule-8
walk-forward.  x is NOT a third dial - it is a deterministic function of theta (the matching).
Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps rung is DERIVED
exactly (r0 = r10 + turnover*cost_bps/1e4), not re-run, so it is the same book.

Grid: 9 thetas x 3 cadences x 2 families x 2 constructions = 108 books; 54 decomposition cells.

Rule 8 walk-forward (required; three, all directions fixed before any OOS number was read)
  WF-A (the book).  Inside each family x construction arm, (theta, cadence) is chosen on
        2010..2016-12-31 by IS Sharpe; 2017-01-01..end read ONCE.  OOS CAGR/Sharpe/MaxDD
        reported against RULES v2 (live), SPY, and the cadence-matched no-gate control.
  WF-B (the headline).  Per cell, pick the family with the higher IS Sharpe (DEGROSS), read
        OOS once, and compare against always-MA and always-QUANTILE.  If family choice is not
        learnable IS->OOS, no future study should treat the MA form as the informed default.
  WF-C (the residual).  Fit nothing: check that the IS-window per-arm mean resid0 predicts the
        OOS-window resid0 better than zero, i.e. that idea 298's constant-residual discount
        walks forward on this panel.  Reported as MAE in pp/yr against the zero baseline.

Verdicts (both KEEP paths, on every one of the 108 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: data/prices_small.csv.gz is CURRENT constituents of the screen - no delistings -
so every CAGR LEVEL here is inflated and the 4a/4b columns inherit that bias whole.  The
headline is an arm-minus-arm contrast on the SAME names, the SAME ranking and the SAME days,
so the bias very largely cancels out of dCAGR / dSharpe / resid0; it does NOT cancel out of
the KEEP columns.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .matched.csv .walkforward.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSS = 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# pre-registered bars
BAR_DS_MEAN = 0.05          # |mean dSharpe| threshold separating the hypotheses
BAR_DS_CELLS = 19           # of 27 cells positive, for H_TIMING_PAYS
BAR_MASK_TOL = 0.01         # matching quality on mask fraction
BAR_CBAR_TOL = 0.02         # matching quality on realised c_bar
BAR_IDENT = 1e-12
BAR_MA_RESID = (-0.70, -0.20)   # idea 298's MA-gate residual band, pp/yr
BAR_Q_RESID = 0.05              # QUANTILE residual must be within this of zero, pp/yr

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


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
    """px/ma200 - 1, and the live mask.  Both families order names by this."""
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

    P("=" * 170)
    P("Idea 300 does-a-pure-exposure-gate-exist-on-the-small-panel (lane C) | " + Path(__file__).name)
    P("=" * 170)
    P(f"PANEL SMALL439: {px.shape[1]} names ({n_dropped} dropped for max_1d_move >= 1.0), "
      f"{px.index[0].date()}..{px.index[-1].date()}; evaluation from {start.date()} ({years:.2f} yrs).")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), "
      f"gross {GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): theta {MA_THETA} x cadence {CADENCES}.  x is a deterministic function "
      f"of theta (the matching), not a dial.")
    P(f"reported contrasts: family {FAMILIES} x construction {CONSTRUCTIONS}.")
    P("pre-registered bars:")
    P(f"  H_TIMING_PAYS : mean dSharpe(MA - QUANTILE-M, DEGROSS, full) > +{BAR_DS_MEAN} AND "
      f"positive in >= {BAR_DS_CELLS}/27 cells AND mean OOS dSharpe > 0")
    P(f"  H_PURE_DRAG   : mean full dSharpe <= 0, OR (positive in < {BAR_DS_CELLS}/27 AND "
      f"|mean dSharpe| <= {BAR_DS_MEAN})")
    P(f"  B_MATCH       : |d mask fraction| < {BAR_MASK_TOL} and |d realised c_bar| < "
      f"{BAR_CBAR_TOL} in all 27 cells; identity < {BAR_IDENT}; "
      f"mean MA resid0 in {BAR_MA_RESID} pp/yr; |mean QUANTILE resid0| < {BAR_Q_RESID} pp/yr")
    P("SURVIVORSHIP: current constituents only; CAGR levels inflated, arm-minus-arm contrasts "
      "very largely immune, 4a/4b columns are not.")

    # --------------------------------------------- comparands
    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]
    live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
    ctrl, ctrl0 = {}, {}
    for cad in CADENCES:
        rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
        r10 = rc["returns"].loc[start:]
        ctrl[cad] = stat(r10)
        ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
    P("")
    P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
      f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS {spy_s['oSharpe']:.4f}")
    P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
      f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS {live_s['oSharpe']:.4f}")
    for cad in CADENCES:
        P(f"CONTROL EWall {cad} (no gate)   : CAGR {ctrl[cad]['CAGR']:.4f} Sharpe {ctrl[cad]['Sharpe']:.4f} "
          f"MaxDD {ctrl[cad]['MaxDD']:.4f} | 0 bps CAGR {ctrl0[cad]:.4f}")
    P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} OOS>{spy_s['oSharpe']:.3f} "
      f"MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} CAGR>={0.70 * spy_s['CAGR']:.2%}")
    flush_log()

    # --------------------------------------------- the matching (theta -> x)
    P("\n" + "=" * 170)
    P("THE MATCHING: x is set to the MA gate's OWN mean mask fraction at that theta")
    P("=" * 170)
    live = live_mask(px).loc[start:]
    nlive = live.sum(axis=1)
    match = []
    gates = {}
    for th in MA_THETA:
        gm = ma_gate(px, th)
        frac_ma = float((gm.loc[start:].sum(axis=1) / nlive).mean())
        x = frac_ma
        gq = quantile_gate(px, x)
        frac_q = float((gq.loc[start:].sum(axis=1) / nlive).mean())
        gates[th] = {"MA-THRESH": gm, "QUANTILE-M": gq}
        match.append(dict(theta=th, x=x, frac_ma=frac_ma, frac_q=frac_q,
                          d_frac=frac_q - frac_ma,
                          k_ma_mean=float(gm.loc[start:].sum(axis=1).mean()),
                          k_q_mean=float(gq.loc[start:].sum(axis=1).mean()),
                          k_ma_sd=float(gm.loc[start:].sum(axis=1).std()),
                          k_q_sd=float(gq.loc[start:].sum(axis=1).std())))
    M = pd.DataFrame(match)
    P(fmt(M.set_index("theta")))
    P(f"\nworst |d mask fraction| = {M.d_frac.abs().max():.5f}  "
      f"({'PASS' if M.d_frac.abs().max() < BAR_MASK_TOL else 'FAIL'} at {BAR_MASK_TOL})")
    P("k_*_sd is the point of the experiment: the MA gate's depth moves, the matched "
      "QUANTILE gate's does not (its sd is only the live-count drift).")
    flush_log()

    # --------------------------------------------- the grid
    rows, decomp, pair = [], [], []
    for th in MA_THETA:
        for cad in CADENCES:
            got = {}
            for fam in FAMILIES:
                g = gates[th][fam]
                arms = {}
                for con in CONSTRUCTIONS:
                    res = backtest(px, book(px, g, con), cost_bps=COST_BPS, freq=cad)
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

                def dec(lo, hi, tag):
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

            # ---- the headline paired comparison, at matched c_bar
            for con in CONSTRUCTIONS:
                a = got["MA-THRESH"]["arms"][con]["s"]
                b = got["QUANTILE-M"]["arms"][con]["s"]
                pair.append(dict(
                    theta=th, cad=cad, con=con,
                    c_bar_ma=got["MA-THRESH"]["cells"]["FULL"]["c_bar"],
                    c_bar_q=got["QUANTILE-M"]["cells"]["FULL"]["c_bar"],
                    d_c_bar=got["QUANTILE-M"]["cells"]["FULL"]["c_bar"]
                    - got["MA-THRESH"]["cells"]["FULL"]["c_bar"],
                    Sharpe_ma=a["Sharpe"], Sharpe_q=b["Sharpe"], dSharpe=a["Sharpe"] - b["Sharpe"],
                    CAGR_ma=a["CAGR"], CAGR_q=b["CAGR"], dCAGR_pp=100 * (a["CAGR"] - b["CAGR"]),
                    MaxDD_ma=a["MaxDD"], MaxDD_q=b["MaxDD"], dMaxDD_pp=100 * (a["MaxDD"] - b["MaxDD"]),
                    H1_ma=a["H1"], H1_q=b["H1"], dH1=a["H1"] - b["H1"],
                    H2_ma=a["H2"], H2_q=b["H2"], dH2=a["H2"] - b["H2"],
                    isSharpe_ma=a["isSharpe"], isSharpe_q=b["isSharpe"],
                    dSharpe_is=a["isSharpe"] - b["isSharpe"],
                    oSharpe_ma=a["oSharpe"], oSharpe_q=b["oSharpe"],
                    dSharpe_oos=a["oSharpe"] - b["oSharpe"],
                    oCAGR_ma=a["oCAGR"], oCAGR_q=b["oCAGR"],
                    dCAGR_oos_pp=100 * (a["oCAGR"] - b["oCAGR"]),
                    oMaxDD_ma=a["oMaxDD"], oMaxDD_q=b["oMaxDD"],
                    turn_ma=float(got["MA-THRESH"]["arms"][con]["turn"].sum() / years),
                    turn_q=float(got["QUANTILE-M"]["arms"][con]["turn"].sum() / years),
                    # exact attribution of the 0-bps DEGROSS CAGR difference
                    sel_pp=100 * (got["MA-THRESH"]["cells"]["FULL"]["CAGR_rs0"]
                                  - got["QUANTILE-M"]["cells"]["FULL"]["CAGR_rs0"]),
                    level_pp=(got["MA-THRESH"]["cells"]["FULL"]["pred0_pp"]
                              - got["QUANTILE-M"]["cells"]["FULL"]["pred0_pp"]),
                    timing_pp=(got["MA-THRESH"]["cells"]["FULL"]["resid0_pp"]
                               - got["QUANTILE-M"]["cells"]["FULL"]["resid0_pp"]),
                    dCAGR0_dg_pp=100 * (got["MA-THRESH"]["cells"]["FULL"]["CAGR_dg0"]
                                        - got["QUANTILE-M"]["cells"]["FULL"]["CAGR_dg0"]),
                    dCAGR0_rs_pp=100 * (got["MA-THRESH"]["cells"]["FULL"]["CAGR_rs0"]
                                        - got["QUANTILE-M"]["cells"]["FULL"]["CAGR_rs0"]),
                ))
        P(f"  ... theta {th:+.2f} done ({len(CADENCES) * 4} books)")
        flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    PR = pd.DataFrame(pair)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    PR.to_csv(f"{OUT}.matched.csv", index=False)
    F = D[D.window == "FULL"].copy()
    PD_ = PR[PR.con == "DEGROSS"].copy()
    PRS = PR[PR.con == "RESPREAD"].copy()

    # --------------------------------------------- B_MATCH
    P("\n" + "=" * 170)
    P("B_MATCH - validity gate, read BEFORE the headline")
    P("=" * 170)
    ident = F.ident_max_err.max()
    ok_ident = ident < BAR_IDENT
    P(f"(ii) identity max |r_dg,t - c_t*r_rs,t| over {len(F)} cells = {ident:.3e}  "
      f"{'PASS' if ok_ident else 'FAIL'} at {BAR_IDENT}")
    dcb = PD_.d_c_bar.abs().max()
    ok_cbar = dcb < BAR_CBAR_TOL
    P(f"(i)  worst |d realised c_bar| over 27 cells = {dcb:.5f}  "
      f"{'PASS' if ok_cbar else 'FAIL'} at {BAR_CBAR_TOL}   "
      f"(mask-fraction gate above: {'PASS' if M.d_frac.abs().max() < BAR_MASK_TOL else 'FAIL'})")
    rma = F[F.family == "MA-THRESH"].resid0_pp
    rq = F[F.family == "QUANTILE-M"].resid0_pp
    ok_rma = BAR_MA_RESID[0] <= rma.mean() <= BAR_MA_RESID[1]
    ok_rq = abs(rq.mean()) < BAR_Q_RESID
    P(f"(iii) MA-THRESH  resid0 mean {rma.mean():+.4f} pp/yr (sd {rma.std():.4f}, "
      f"range {rma.min():+.4f}..{rma.max():+.4f})  {'PASS' if ok_rma else 'FAIL'} in {BAR_MA_RESID}")
    P(f"      QUANTILE-M resid0 mean {rq.mean():+.4f} pp/yr (sd {rq.std():.4f}, "
      f"range {rq.min():+.4f}..{rq.max():+.4f})  {'PASS' if ok_rq else 'FAIL'} at +/-{BAR_Q_RESID}")
    P(f"  B_MATCH: {'PASS' if (ok_ident and ok_cbar and ok_rma and ok_rq) else 'FAIL'}")
    flush_log()

    # --------------------------------------------- decomposition table
    P("\n" + "=" * 170)
    P("DECOMPOSITION - all 54 full-sample cells (0 bps), both families")
    P("=" * 170)
    for fam in FAMILIES:
        P(f"\n--- {fam} ---")
        P(fmt(F[F.family == fam].set_index(["theta", "cad"])[
            ["c_bar", "c_sd", "CAGR_rs0", "CAGR_dg0", "gap0_pp", "pred0_pp", "resid0_pp", "share"]]))

    # --------------------------------------------- THE HEADLINE
    P("\n" + "=" * 170)
    P("HEADLINE - MA-THRESH minus matched QUANTILE-M, DEGROSS, all 27 cells (10 bps)")
    P("=" * 170)
    P(fmt(PD_.set_index(["theta", "cad"])[
        ["c_bar_ma", "c_bar_q", "Sharpe_ma", "Sharpe_q", "dSharpe", "dH1", "dH2",
         "dSharpe_oos", "CAGR_ma", "CAGR_q", "dCAGR_pp", "MaxDD_ma", "MaxDD_q", "dMaxDD_pp",
         "turn_ma", "turn_q"]]))
    P("\n(dSharpe > 0 means the MA gate's time-varying depth is worth paying for; "
      "dMaxDD_pp > 0 means the MA gate drew down LESS.)")

    n_pos = int((PD_.dSharpe > 0).sum())
    mean_ds = float(PD_.dSharpe.mean())
    mean_ds_oos = float(PD_.dSharpe_oos.mean())
    n_pos_oos = int((PD_.dSharpe_oos > 0).sum())
    P("\n" + "-" * 170)
    P(f"dSharpe  full : mean {mean_ds:+.4f}  median {PD_.dSharpe.median():+.4f}  "
      f"sd {PD_.dSharpe.std():.4f}  positive in {n_pos}/27  "
      f"range {PD_.dSharpe.min():+.4f}..{PD_.dSharpe.max():+.4f}")
    P(f"dSharpe  H1/H2: positive in {(PD_.dH1 > 0).sum()}/27 and {(PD_.dH2 > 0).sum()}/27  "
      f"(means {PD_.dH1.mean():+.4f} / {PD_.dH2.mean():+.4f})")
    P(f"dSharpe  OOS  : mean {mean_ds_oos:+.4f}  positive in {n_pos_oos}/27")
    P(f"dCAGR    full : mean {PD_.dCAGR_pp.mean():+.4f} pp/yr  positive in "
      f"{(PD_.dCAGR_pp > 0).sum()}/27")
    P(f"dMaxDD   full : mean {PD_.dMaxDD_pp.mean():+.4f} pp  MA shallower in "
      f"{(PD_.dMaxDD_pp > 0).sum()}/27")
    P(f"turnover      : MA {PD_.turn_ma.mean():.3f}/yr vs QUANTILE-M {PD_.turn_q.mean():.3f}/yr "
      f"(ratio {PD_.turn_ma.mean() / PD_.turn_q.mean():.3f}x)")
    P("\nby cadence:")
    P(fmt(PD_.groupby("cad").agg(n=("dSharpe", "size"), dSharpe=("dSharpe", "mean"),
                                 pos=("dSharpe", lambda s: int((s > 0).sum())),
                                 dCAGR_pp=("dCAGR_pp", "mean"),
                                 dMaxDD_pp=("dMaxDD_pp", "mean"),
                                 dSharpe_oos=("dSharpe_oos", "mean"))))
    P("\nby strictness (c_bar rung):")
    P(fmt(PD_.set_index("theta")[["c_bar_ma", "dSharpe", "dCAGR_pp", "dMaxDD_pp", "dSharpe_oos"]]
          .groupby("theta").mean()))
    P("\nRESPREAD arm (exposure held at 1; isolates the slice-depth SELECTION effect):")
    P(f"  dSharpe mean {PRS.dSharpe.mean():+.4f}, positive in {(PRS.dSharpe > 0).sum()}/27; "
      f"dCAGR mean {PRS.dCAGR_pp.mean():+.4f} pp/yr; dMaxDD mean {PRS.dMaxDD_pp.mean():+.4f} pp")

    # verdicts on the pre-registered bars
    timing_pays = (mean_ds > BAR_DS_MEAN) and (n_pos >= BAR_DS_CELLS) and (mean_ds_oos > 0)
    pure_drag = (mean_ds <= 0) or ((n_pos < BAR_DS_CELLS) and (abs(mean_ds) <= BAR_DS_MEAN))
    P("\n" + "=" * 170)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 170)
    P(f"  H_TIMING_PAYS (mean dSharpe > +{BAR_DS_MEAN} AND >= {BAR_DS_CELLS}/27 positive AND "
      f"OOS mean > 0): mean {mean_ds:+.4f}, {n_pos}/27, OOS {mean_ds_oos:+.4f}  "
      f"-> {'HOLDS' if timing_pays else 'FAILS'}")
    P(f"  H_PURE_DRAG   (mean <= 0, or < {BAR_DS_CELLS}/27 and |mean| <= {BAR_DS_MEAN}): "
      f"-> {'HOLDS' if pure_drag else 'FAILS'}")
    flush_log()

    # --------------------------------------------- exact attribution
    P("\n" + "=" * 170)
    P("EXACT ATTRIBUTION of the 0-bps DEGROSS CAGR difference (identity, not a fit)")
    P("   dCAGR0_dg = SELECTION + LEVEL + TIMING")
    P("=" * 170)
    PD_ = PD_.assign(check=PD_.dCAGR0_dg_pp - (PD_.sel_pp + PD_.level_pp + PD_.timing_pp))
    P(fmt(PD_.set_index(["theta", "cad"])[
        ["dCAGR0_dg_pp", "sel_pp", "level_pp", "timing_pp", "check"]]))
    P(f"\nidentity closes to {PD_.check.abs().max():.3e} pp "
      f"({'PASS' if PD_.check.abs().max() < 1e-9 else 'FAIL'} at 1e-9)")
    P(f"means over 27 cells: dCAGR0_dg {PD_.dCAGR0_dg_pp.mean():+.4f} = SELECTION "
      f"{PD_.sel_pp.mean():+.4f} + LEVEL {PD_.level_pp.mean():+.4f} + TIMING "
      f"{PD_.timing_pp.mean():+.4f}  (pp/yr)")

    # --------------------------------------------- KEEP paths
    P("\n" + "=" * 170)
    P("KEEP PATHS on all 108 books")
    P("=" * 170)
    P(f"4a passes: {int(G.p4a.sum())}/{len(G)}    4b passes: {int(G.p4b.sum())}/{len(G)}")
    P("4b failure reasons (count of books by failing clause set):")
    P(fmt(G.f4b.value_counts().to_frame("n"), 0))
    if G.p4b.any():
        P("\n4b PASSERS:")
        P(fmt(G[G.p4b].set_index(["family", "con", "theta", "cad"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "turn_yr"]]))
    P("\nbest full-sample Sharpe per family x construction:")
    P(fmt(G.loc[G.groupby(["family", "con"]).Sharpe.idxmax()].set_index(["family", "con"])[
        ["theta", "cad", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]]))
    flush_log()

    # --------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 170)
    P("RULE 8 WALK-FORWARD.  IS = start..2016-12-31 (selection), OOS = 2017-01-01..end (read once)")
    P("=" * 170)
    wf = []
    P("\nWF-A: (theta, cadence) picked by IS Sharpe inside each family x construction arm")
    for (fam, con), sub in G.groupby(["family", "con"]):
        pick = sub.loc[sub.isSharpe.idxmax()]
        wf.append(dict(test="WF-A", arm=f"{fam}/{con}", pick=f"theta {pick.theta:+.2f} cad {pick.cad}",
                       isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                       oMaxDD=pick.oMaxDD))
        P(f"  {fam:11s}/{con:8s} picks theta {pick.theta:+.2f} cad {pick.cad} "
          f"(IS Sharpe {pick.isSharpe:.4f})  ->  OOS CAGR {pick.oCAGR:.4f} Sharpe "
          f"{pick.oSharpe:.4f} MaxDD {pick.oMaxDD:.4f}")
    P(f"  comparands OOS: SPY CAGR {spy_s['oCAGR']:.4f} Sharpe {spy_s['oSharpe']:.4f} "
      f"MaxDD {spy_s['oMaxDD']:.4f} | RULES v2 CAGR {live_s['oCAGR']:.4f} Sharpe "
      f"{live_s['oSharpe']:.4f} MaxDD {live_s['oMaxDD']:.4f}")
    for cad in CADENCES:
        P(f"  comparand OOS EWall {cad}: CAGR {ctrl[cad]['oCAGR']:.4f} Sharpe "
          f"{ctrl[cad]['oSharpe']:.4f} MaxDD {ctrl[cad]['oMaxDD']:.4f}")

    P("\nWF-B: per cell pick the family with the higher IS Sharpe (DEGROSS), read OOS once")
    picked_ma = PD_.dSharpe_is > 0
    oos_pick = np.where(picked_ma, PD_.oSharpe_ma, PD_.oSharpe_q)
    oos_pick_c = np.where(picked_ma, PD_.oCAGR_ma, PD_.oCAGR_q)
    P(f"  IS prefers MA-THRESH in {int(picked_ma.sum())}/27 cells")
    P(f"  OOS Sharpe: PICK {oos_pick.mean():.4f} | always-MA {PD_.oSharpe_ma.mean():.4f} | "
      f"always-QUANTILE-M {PD_.oSharpe_q.mean():.4f}")
    P(f"  OOS CAGR  : PICK {oos_pick_c.mean():.4f} | always-MA {PD_.oCAGR_ma.mean():.4f} | "
      f"always-QUANTILE-M {PD_.oCAGR_q.mean():.4f}")
    hit = float(((PD_.dSharpe_is > 0) == (PD_.dSharpe_oos > 0)).mean())
    P(f"  IS->OOS sign agreement of dSharpe: {hit:.4f} ({int(hit * 27)}/27) "
      f"[0.5 = family choice is not learnable]")
    wf.append(dict(test="WF-B", arm="family pick (DEGROSS)", pick=f"MA in {int(picked_ma.sum())}/27",
                   isSharpe=np.nan, oCAGR=float(oos_pick_c.mean()), oSharpe=float(oos_pick.mean()),
                   oMaxDD=np.nan))

    P("\nWF-C: does idea 298's constant-residual discount walk forward on this panel?")
    for fam in FAMILIES:
        di = D[(D.family == fam) & (D.window == "IS")].set_index(["theta", "cad"]).resid0_pp
        do = D[(D.family == fam) & (D.window == "OOS")].set_index(["theta", "cad"]).resid0_pp
        mae_zero = float(do.abs().mean())
        mae_const = float((do - di.mean()).abs().mean())
        mae_cell = float((do - di).abs().mean())
        P(f"  {fam:11s}: IS mean resid0 {di.mean():+.4f} pp/yr, OOS mean {do.mean():+.4f}  | "
          f"OOS MAE vs zero {mae_zero:.4f} | vs IS-mean constant {mae_const:.4f} | "
          f"vs own IS cell {mae_cell:.4f} pp/yr")
        wf.append(dict(test="WF-C", arm=fam, pick="IS-mean constant", isSharpe=di.mean(),
                       oCAGR=do.mean(), oSharpe=mae_const, oMaxDD=mae_zero))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # --------------------------------------------- answer
    P("\n" + "=" * 170)
    P("ANSWER")
    P("=" * 170)
    exists = pure_drag and not timing_pays
    P(f"Does a pure exposure gate exist on SMALL439?  "
      f"{'YES' if exists else 'NO' if timing_pays else 'INCONCLUSIVE'}")
    P(f"  the matched QUANTILE-M gate reproduces the MA gate's mean exposure to "
      f"{PD_.d_c_bar.abs().max():.4f} of c_bar and carries {rq.mean():+.4f} pp/yr of timing "
      f"residual against the MA gate's {rma.mean():+.4f} pp/yr.")
    P(f"  the MA gate's extra residual buys {mean_ds:+.4f} of Sharpe on average "
      f"({n_pos}/27 cells positive; OOS {mean_ds_oos:+.4f}, {n_pos_oos}/27) and "
      f"{PD_.dMaxDD_pp.mean():+.4f} pp of MaxDD.")
    P(f"  4a {int(G.p4a.sum())}/108, 4b {int(G.p4b.sum())}/108.")
    flush_log()
    P(f"\nwrote {OUT.name}.grid.csv .decomp.csv .matched.csv .walkforward.csv .console.txt")
    flush_log()


if __name__ == "__main__":
    main()
