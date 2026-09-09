#!/usr/bin/env python3
"""Idea 558 (cloud, 2026-09-09) - publish-BOTH-beside-every-SELECTION-LEVEL-TIMING-split.

QUESTION
--------
Idea 556 found that the SELECTION leg of the MA-vs-depth-matched-QUANTILE attribution hides a
fourth leg.  The matching sets the quantile depth x to the MA gate's MEAN mask fraction, so the
two arms hold the same names at DIFFERENT weights on any given day; that shared-names weight
gap (BOTH) was 31.5% of the decomposed magnitude and exceeded |SELECTION| in 17 of 27 cells at
cadence W / QUANTILE-M.  The queue asks: re-read EVERY committed SELECTION/LEVEL/TIMING split
in the record with BOTH published, and report how many published SELECTION numbers are
majority-BOTH.

WHAT IS BEING AUDITED
---------------------
The record's split is  dCAGR0_dg_pp = SELECTION + LEVEL + TIMING  (idea 305's definition,
reproduced verbatim here):

    SELECTION = 100 * (CAGR(r0 of the RESPREAD MA arm) - CAGR(r0 of the RESPREAD quantile arm))
    LEVEL     = pred0_pp(MA) - pred0_pp(Q),   pred0 = 100*(CAGR(c_bar * r_rs0) - CAGR(r_rs0))
    TIMING    = resid0_pp(MA) - resid0_pp(Q), resid0 = gap0 - pred0

SELECTION is a "which names" statistic ONLY if the two arms hold the shared names at the same
weight.  They do not.  The exact identity (idea 556) is

    gap_t = sum_i (W^MA - W^Q)_i,t r_i,t
          =  sum_{i in ADD}  W^MA_i,t r_i,t        (names only the MA slice holds)
          -  sum_{i in DROP} W^Q_i,t  r_i,t        (names only the quantile slice holds)
          +  sum_{i in BOTH} (W^MA - W^Q)_i,t r_i,t   (shared names, DEPTH-MISMATCH weight gap)

so ADD + DROP + BOTH = the arithmetic SELECTION gap exactly, and BOTH is the part of the
published SELECTION number that is NOT about which names are held.

PRE-REGISTERED DEFINITION (stated before any result is read)
------------------------------------------------------------
A published SELECTION number is MAJORITY-BOTH  <=>  |BOTH_pp| > |sel_geo_pp|, i.e. the
unpublished depth-mismatch leg is larger in absolute size than the published number it hides
inside.  Secondary reading DOMINANT-BOTH  <=>  |BOTH_pp| = max(|ADD_pp|, |DROP_pp|, |BOTH_pp|).
Both are reported for every cell; neither is tuned.

PRE-REGISTERED HYPOTHESES
-------------------------
H_MAJ   : >= 50% of the record's DISTINCT published SELECTION numbers are majority-BOTH
          (idea 556's 17/27 = 63.0% at cadence W / QUANTILE-M is the anchor).
H_CAD   : the majority-BOTH rate is a property of the CELL, not of the cadence dial - the rate
          at each of W / M / Q lies within +/-10 pp of the pooled rate.
H_DEPTH : majority-BOTH is a function of the matched depth x, not of the panel label - the
          pooled rank correlation of |BOTH|/|sel_geo| with x is |rho| >= 0.30, and panel dummies
          cut the residual SD of log(|BOTH|/|sel_geo|) ~ x by < 25%.

TUNED PARAMETERS: exactly 2 - panel {U56, B136, SMALL439} x theta (9 rungs).  x is a
deterministic function of theta (the matching), not a dial.  Cadence {W,M,Q}, quantile family
{QUANTILE-M, QUANTILE-F} and construction {RESPREAD, DEGROSS} are REPORTED contrasts, not
selected over.  Every grid point is reported.

GATES
-----
G1 zero-cost identity : max |sum_i W_i r_i - (returns + turnover*bps/1e4)| < 1e-12.
G2 three-leg identity : max |ADD + DROP + BOTH - gap| < 1e-12 over every cell/window.
G3 record split       : max |SELECTION + LEVEL + TIMING - dCAGR0_dg_pp| < 1e-9 (the record's
                        own identity, recomputed).
R1 idea 305 pairs.csv : all 324 committed rows, columns sel_pp / level_pp / timing_pp /
                        dCAGR0_dg_pp / dCAGR0_rs_pp / dSharpe / dSharpe_oos, to 1e-9.
R2 idea 51R matched   : all 54 committed rows of the SMALL439 lane-C file, same columns, 1e-9.
R3 idea 556 legs.csv  : the cadence-W ADD/DROP/BOTH/sel_geo rows, to 1e-9.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine), no shorting, no leverage,
gross 0.75.  Rule 8 walk-forward IS = start..2016-12-31 (choice), OOS = 2017-01-01..end (read
once): WF-A does a cell's majority-BOTH label chosen on IS hold OOS; WF-B pick the book with
the best IS Sharpe over the whole 486-book grid and read its OOS once against RULES v2 and SPY;
WF-C does an IS-fitted |BOTH|/|sel| ~ x model beat the pooled IS mean OOS.  BOTH KEEP paths
(4a vs the live RULES v2 book, 4b vs SPY) evaluated on all 486 books.

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels are inflated and the
4a/4b columns are NOT immune.  The ADD/DROP/BOTH legs are same-panel arm-minus-arm differences
so the bias very largely cancels there, but the ADD side is exactly the side survivorship
flatters most.  SMALL439 drops the 44 names with max_1d_move >= 1.0 in data/small_meta.csv.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .census.csv .grid.csv .legs.csv .pairs.csv .cells.csv .walkforward.csv .keeppaths.csv
         .console.txt
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
FAMILIES = ["MA-THRESH", "QUANTILE-M", "QUANTILE-F"]
Q_FAMS = ["QUANTILE-M", "QUANTILE-F"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS = 1e-12
BAR_R0 = 1e-12
BAR_IDENT = 1e-12
BAR_SPLIT = 1e-9
R1_TOL = 1e-9
RHO_BAR = 0.30                 # H_DEPTH (a)
PANEL_DUMMY_BAR = 0.25         # H_DEPTH (b)
CAD_BAR = 0.10                 # H_CAD

BT = REPO / "research" / "backtests"
IDEA305 = BT / "2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.pairs.csv"
IDEA51R = BT / "2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.matched.csv"
IDEA556 = BT / "2026-09-09_why-does-the-MA-SLICE-flip-from-better-to-worse-at-the-panel-boundary_C.legs.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- C0: the census
def census():
    """Mechanically scan every committed CSV in research/backtests for the record's
    SELECTION/LEVEL/TIMING split.  A file is IN SCOPE iff its header carries all three of
    sel_pp, level_pp, timing_pp.  No hand-picked list."""
    rows = []
    for f in sorted(BT.glob("*.csv")):
        try:
            head = f.open().readline().strip().split(",")
        except Exception:
            continue
        if {"sel_pp", "level_pp", "timing_pp"} <= set(head):
            df = pd.read_csv(f)
            keys = [c for c in ["panel", "theta", "cad", "qfam"] if c in df.columns]
            rows.append(dict(file=f.name, n_rows=len(df), key_cols=";".join(keys),
                             n_distinct_cells=len(df.drop_duplicates(subset=keys)) if keys else np.nan,
                             has_panel=("panel" in df.columns), has_qfam=("qfam" in df.columns),
                             has_BOTH=("BOTH_pp" in df.columns)))
    return pd.DataFrame(rows)


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


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def dist_rank(px):
    live = live_mask(px)
    return (px / px.rolling(200).mean() - 1).where(live), live


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    dist, live = dist_rank(px)
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def quantile_gate_frac(px, x):
    dist, live = dist_rank(px)
    n = live.sum(axis=1)
    kf = x * n
    kfl = np.floor(kf)
    rank = dist.rank(axis=1, ascending=False, method="first")
    full = (rank.le(kfl, axis=0).fillna(False) & live).astype(float)
    marg = (rank.eq(kfl + 1, axis=0).fillna(False) & live).astype(float)
    return full + marg.mul(kf - kfl, axis=0)


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


# ---------------------------------------------------------------- the four legs
def legs(Wm, Wq, R, turn_m, turn_q, lo, hi, tag):
    sl = slice(lo, hi)
    A, B, r = Wm.loc[sl], Wq.loc[sl], R.loc[sl]
    on_a, on_b = A > EPS, B > EPS
    add, drop, both = on_a & ~on_b, on_b & ~on_a, on_a & on_b

    cA = (A.where(add, 0.0) * r).sum(axis=1)
    cD = -(B.where(drop, 0.0) * r).sum(axis=1)
    cC = ((A.where(both, 0.0) - B.where(both, 0.0)) * r).sum(axis=1)
    r0m, r0q = (A * r).sum(axis=1), (B * r).sum(axis=1)
    gap = r0m - r0q
    ident = float((cA + cD + cC - gap).abs().max())

    wA = A.where(add, 0.0).sum(axis=1)
    wD = B.where(drop, 0.0).sum(axis=1)
    yrs = len(r) / 252.0
    cost_pp = -100.0 * (turn_m.loc[sl].sum() - turn_q.loc[sl].sum()) * COST_BPS / 1e4 / yrs

    add_pp, drop_pp = 252 * 100 * cA.mean(), 252 * 100 * cD.mean()
    both_pp = 252 * 100 * cC.mean()
    geo = 100 * (cagr(r0m) - cagr(r0q))
    mag = abs(add_pp) + abs(drop_pp) + abs(both_pp)
    dom = ["ADD", "DROP", "BOTH"][int(np.argmax([abs(add_pp), abs(drop_pp), abs(both_pp)]))]
    return dict(
        window=tag, ident_max=ident,
        ADD_pp=add_pp, DROP_pp=drop_pp, BOTH_pp=both_pp,
        arith_pp=add_pp + drop_pp + both_pp, sel_geo_pp=geo,
        jensen_pp=geo - (add_pp + drop_pp + both_pp),
        COST_pp=cost_pp, net10_pp=add_pp + drop_pp + both_pp + cost_pp,
        both_share=(abs(both_pp) / mag if mag > 1e-12 else np.nan),
        both_over_sel=(abs(both_pp) / abs(geo) if abs(geo) > 1e-12 else np.inf),
        majority_BOTH=bool(abs(both_pp) > abs(geo)),
        dominant=dom, dominant_BOTH=bool(dom == "BOTH"),
        n_add=float(add.sum(axis=1).mean()), n_drop=float(drop.sum(axis=1).mean()),
        n_both=float(both.sum(axis=1).mean()), n_ma=float(on_a.sum(axis=1).mean()),
        overlap=float(both.sum(axis=1).mean() / max(on_a.sum(axis=1).mean(), 1e-9)),
        w_add=float(wA.mean()), w_drop=float(wD.mean()),
        rbar_add=(252 * 100 * cA.sum() / wA.sum()) if wA.sum() > 1e-12 else np.nan,
        rbar_drop=(252 * 100 * (-cD).sum() / wD.sum()) if wD.sum() > 1e-12 else np.nan,
        sign_sel=int(np.sign(geo)),
        turn_ma=float(turn_m.loc[sl].sum() / yrs), turn_q=float(turn_q.loc[sl].sum() / yrs))


def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b, y - X @ b


# ---------------------------------------------------------------- main
def main():
    CEN = census()
    PN, n_dropped = panels()

    P("=" * 185)
    P("Idea 558 publish-BOTH-beside-every-SELECTION-LEVEL-TIMING-split (cloud) | "
      + Path(__file__).name)
    P("=" * 185)
    P("QUESTION: re-read every committed SELECTION/LEVEL/TIMING split with the shared-names "
      "depth-mismatch leg BOTH published,")
    P("          and report how many published SELECTION numbers are MAJORITY-BOTH.")
    P("PRE-REGISTERED  majority-BOTH := |BOTH_pp| > |sel_geo_pp|   "
      "(secondary: dominant-BOTH := |BOTH| = max(|ADD|,|DROP|,|BOTH|))")
    P(f"                H_MAJ   : >= 50% of the DISTINCT published SELECTION numbers are "
      f"majority-BOTH (anchor: idea 556's 17/27 = 63.0%).")
    P(f"                H_CAD   : the majority-BOTH rate at each cadence is within "
      f"+/-{CAD_BAR:.0%} of the pooled rate.")
    P(f"                H_DEPTH : |rho(|BOTH|/|sel|, x)| >= {RHO_BAR:.2f} and panel dummies "
      f"cut the residual SD by < {PANEL_DUMMY_BAR:.0%}.")
    P(f"costs {COST_BPS} bps, gross {GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): panel {PANELS} x theta {MA_THETA}.")
    P(f"reported contrasts: cadence {CADENCES} x family {FAMILIES} x construction "
      f"{CONSTRUCTIONS} = "
      f"{len(PANELS)*len(MA_THETA)*len(CADENCES)*len(FAMILIES)*len(CONSTRUCTIONS)} books, "
      f"all reported.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels inflated and "
      "the 4a/4b columns NOT immune.")
    P("              The legs are same-panel arm-minus-arm differences so the bias very largely "
      "cancels; the ADD side is the")
    P("              side survivorship flatters most.  Restated beside the headline.")
    for pn in PANELS:
        px, _ = PN[pn]
        P(f"  PANEL {pn:9s}: {px.shape[1]:3d} names, {px.index[0].date()}..{px.index[-1].date()}"
          f", {len(px)} bars"
          + (f" ({n_dropped} dropped for max_1d_move >= 1.0)" if pn == "SMALL439" else ""))

    P("\n" + "=" * 185)
    P("C0  THE CENSUS - every committed CSV in research/backtests whose header carries "
      "sel_pp AND level_pp AND timing_pp")
    P("=" * 185)
    P(fmt(CEN.reset_index(drop=True)))
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    P(f"\n  files in scope: {len(CEN)}   committed rows: {int(CEN.n_rows.sum())}   "
      f"files that already publish BOTH: {int(CEN.has_BOTH.sum())}")
    flush_log()

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, pairs, legrows, matchrows = [], [], [], []
    r0_gate_max = 0.0
    spy_by_panel, live_by_panel = {}, {}

    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        R = px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        spy_by_panel[pn], live_by_panel[pn] = spy_s, live_s

        P("\n" + "=" * 185)
        P(f"PANEL {pn} - comparands over {start.date()}..{px.index[-1].date()} ({years:.2f} yrs)")
        P("=" * 185)
        P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} "
          f"OOS {spy_s['oSharpe']:.4f} oCAGR {spy_s['oCAGR']:.4f} oMaxDD {spy_s['oMaxDD']:.4f}")
        P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS {live_s['oSharpe']:.4f} oCAGR {live_s['oCAGR']:.4f} oMaxDD {live_s['oMaxDD']:.4f}")
        P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")

        live = live_mask(px).loc[start:]
        nlive = live.sum(axis=1)
        ctrl = {}
        for cad in CADENCES:
            ctrl[cad] = stat(backtest(px, control_book(px), cost_bps=COST_BPS,
                                      freq=cad)["returns"].loc[start:])
            P(f"CONTROL EWall {cad}  (no gate)  : CAGR {ctrl[cad]['CAGR']:.4f} Sharpe "
              f"{ctrl[cad]['Sharpe']:.4f} MaxDD {ctrl[cad]['MaxDD']:.4f}")

        gates = {}
        for th in MA_THETA:
            gm = ma_gate(px, th)
            frac_ma = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gq, gf = quantile_gate(px, frac_ma), quantile_gate_frac(px, frac_ma)
            gates[th] = {"MA-THRESH": gm, "QUANTILE-M": gq, "QUANTILE-F": gf}
            matchrows.append(dict(panel=pn, theta=th, x=frac_ma,
                                  frac_q=float((gq.loc[start:].sum(axis=1) / nlive).mean()),
                                  frac_f=float((gf.loc[start:].sum(axis=1) / nlive).mean()),
                                  k_ma=float(gm.loc[start:].sum(axis=1).mean()),
                                  k_q=float(gq.loc[start:].sum(axis=1).mean())))

        for th in MA_THETA:
            xth = float([m["x"] for m in matchrows
                         if m["panel"] == pn and m["theta"] == th][0])
            for cad in CADENCES:
                arms, cells = {}, {}
                for fam in FAMILIES:
                    for con in CONSTRUCTIONS:
                        res = backtest(px, book(px, gates[th][fam], con),
                                       cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        W = res["weights"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        r0_gate_max = max(r0_gate_max,
                                          float(((W * R).sum(axis=1) - r0).abs().max()))
                        s = stat(r10)
                        arms[(fam, con)] = dict(W=W, turn=turn, s=s, r0=r0,
                                                gross=W.sum(axis=1))
                        rows.append(dict(panel=pn, theta=th, x=xth, cad=cad, family=fam,
                                         con=con, **s, CAGR0=cagr(r0),
                                         turn_yr=float(turn.sum() / years),
                                         dCAGR_ctrl=s["CAGR"] - ctrl[cad]["CAGR"],
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))

                    # idea 305's LEVEL/TIMING cells for this family
                    dg, rs = arms[(fam, "DEGROSS")], arms[(fam, "RESPREAD")]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    cf = {}
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        sl = slice(lo, hi)
                        rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                        cb = float(c_t.loc[sl].mean())
                        g0 = 100 * (cagr(rd) - cagr(rr))
                        p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        cf[tag] = dict(c_bar=cb, c_sd=float(c_t.loc[sl].std()), gap0_pp=g0,
                                       pred0_pp=p0, resid0_pp=g0 - p0,
                                       CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd))
                    cells[fam] = cf

                ma_rs = arms[("MA-THRESH", "RESPREAD")]
                for qfam in Q_FAMS:
                    q_rs = arms[(qfam, "RESPREAD")]
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        d = legs(ma_rs["W"], q_rs["W"], R, ma_rs["turn"], q_rs["turn"],
                                 lo, hi, tag)
                        legrows.append(dict(panel=pn, theta=th, x=xth, cad=cad, qfam=qfam, **d))
                    cm, cq = cells["MA-THRESH"], cells[qfam]
                    for con in CONSTRUCTIONS:
                        a, b = arms[("MA-THRESH", con)]["s"], arms[(qfam, con)]["s"]
                        pairs.append(dict(
                            panel=pn, theta=th, x=xth, cad=cad, con=con, qfam=qfam,
                            Sharpe_ma=a["Sharpe"], Sharpe_q=b["Sharpe"],
                            dSharpe=a["Sharpe"] - b["Sharpe"],
                            dSharpe_oos=a["oSharpe"] - b["oSharpe"],
                            dCAGR_pp=100 * (a["CAGR"] - b["CAGR"]),
                            dMaxDD_pp=100 * (a["MaxDD"] - b["MaxDD"]),
                            sel_pp=100 * (cm["FULL"]["CAGR_rs0"] - cq["FULL"]["CAGR_rs0"]),
                            level_pp=cm["FULL"]["pred0_pp"] - cq["FULL"]["pred0_pp"],
                            timing_pp=cm["FULL"]["resid0_pp"] - cq["FULL"]["resid0_pp"],
                            dCAGR0_dg_pp=100 * (cm["FULL"]["CAGR_dg0"] - cq["FULL"]["CAGR_dg0"]),
                            dCAGR0_rs_pp=100 * (cm["FULL"]["CAGR_rs0"] - cq["FULL"]["CAGR_rs0"]),
                        ))
            P(f"  {pn}: theta {th:+.2f} (x={xth:.4f}) done "
              f"({len(CADENCES)*len(FAMILIES)*len(CONSTRUCTIONS)} books)")
            flush_log()

    G, L = pd.DataFrame(rows), pd.DataFrame(legrows)
    PR, M = pd.DataFrame(pairs), pd.DataFrame(matchrows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L.to_csv(f"{OUT}.legs.csv", index=False)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)

    # ------------------------------------------------------------ gates
    P("\n" + "=" * 185)
    P("GATES")
    P("=" * 185)
    P(f"G1 zero-cost identity  : max |sum_i W_i r_i - (ret + turnover*bps/1e4)| over "
      f"{len(G)} books = {r0_gate_max:.3e}  (bar {BAR_R0:.0e})  "
      f"{'PASS' if r0_gate_max < BAR_R0 else 'FAIL'}")
    im = float(L.ident_max.max())
    P(f"G2 three-leg identity  : max |ADD+DROP+BOTH - gap| over {len(L)} cells = {im:.3e}  "
      f"(bar {BAR_IDENT:.0e})  {'PASS' if im < BAR_IDENT else 'FAIL'}")
    split_err = float((PR.dCAGR0_dg_pp - (PR.sel_pp + PR.level_pp + PR.timing_pp)).abs().max())
    P(f"G3 record split identity: max |SEL+LEVEL+TIMING - dCAGR0_dg_pp| over {len(PR)} rows = "
      f"{split_err:.3e}  (bar {BAR_SPLIT:.0e})  "
      f"{'PASS' if split_err < BAR_SPLIT else 'FAIL'}")

    REPRO_COLS = ["sel_pp", "level_pp", "timing_pp", "dCAGR0_dg_pp", "dCAGR0_rs_pp",
                  "dSharpe", "dSharpe_oos", "dCAGR_pp", "dMaxDD_pp"]
    gates_ok = [r0_gate_max < BAR_R0, im < BAR_IDENT, split_err < BAR_SPLIT]

    def repro(path, keys, label):
        if not path.exists():
            P(f"{label}: FILE NOT FOUND - gate could not be run")
            return None
        old = pd.read_csv(path)
        mine = PR.copy()
        if "panel" not in old.columns:
            mine = mine[mine.panel == "SMALL439"]
            if "qfam" not in old.columns:
                mine = mine[mine.qfam == "QUANTILE-M"]
        m = mine.merge(old, on=keys, suffixes=("", "_old"))
        cols = [c for c in REPRO_COLS if c in old.columns and c in mine.columns]
        worst, worst_col = 0.0, None
        for c in cols:
            d = float((m[c] - m[c + "_old"]).abs().max())
            if d > worst:
                worst, worst_col = d, c
        ok = (len(m) == len(old)) and worst < R1_TOL
        P(f"{label}: {len(m)}/{len(old)} rows x {len(cols)} cols, worst |d| = {worst:.3e} "
          f"({worst_col})  (bar {R1_TOL:.0e})  {'PASS' if ok else 'FAIL'}")
        return ok

    k305 = ["panel", "theta", "cad", "con", "qfam"]
    gates_ok.append(repro(IDEA305, k305, "R1 idea 305 pairs.csv "))
    gates_ok.append(repro(IDEA51R, ["theta", "cad", "con"], "R2 idea 51R matched.csv"))

    if IDEA556.exists():
        o = pd.read_csv(IDEA556)
        mineW = L[L.cad == "W"]
        m = mineW.merge(o, on=["panel", "theta", "qfam", "window"], suffixes=("", "_old"))
        cols = ["ADD_pp", "DROP_pp", "BOTH_pp", "sel_geo_pp", "arith_pp", "jensen_pp"]
        worst = max(float((m[c] - m[c + "_old"]).abs().max()) for c in cols)
        ok = (len(m) == len(o)) and worst < R1_TOL
        P(f"R3 idea 556 legs.csv  : {len(m)}/{len(o)} cadence-W rows x {len(cols)} cols, "
          f"worst |d| = {worst:.3e}  (bar {R1_TOL:.0e})  {'PASS' if ok else 'FAIL'}")
        gates_ok.append(ok)
    else:
        P("R3 idea 556 legs.csv  : FILE NOT FOUND")
        gates_ok.append(None)

    if not all(g for g in gates_ok if g is not None):
        P("\n*** A GATE FAILED - the headline below is reported but must not be quoted. ***")
    flush_log()

    # ------------------------------------------------------------ the headline
    F = L[L.window == "FULL"].copy()
    F["cell"] = F.panel + "|" + F.theta.map(lambda t: f"{t:+.2f}") + "|" + F.cad + "|" + F.qfam
    F.to_csv(f"{OUT}.cells.csv", index=False)

    P("\n" + "=" * 185)
    P("THE HEADLINE - every published SELECTION number re-read with BOTH beside it "
      "(FULL sample, pp/yr, ZERO cost).")
    P("SELECTION = ADD + DROP + BOTH + Jensen.  BOTH is the SHARED-names weight gap: it is in "
      "the published SELECTION number")
    P("and is NOT a 'which names' effect.  majority-BOTH := |BOTH| > |SELECTION|.")
    P("=" * 185)
    show = ["panel", "theta", "x", "cad", "qfam", "ADD_pp", "DROP_pp", "BOTH_pp", "arith_pp",
            "jensen_pp", "sel_geo_pp", "both_over_sel", "both_share", "majority_BOTH",
            "dominant", "overlap"]
    P(fmt(F[show].reset_index(drop=True)))

    n_all = len(F)
    n_maj = int(F.majority_BOTH.sum())
    n_dom = int(F.dominant_BOTH.sum())
    P(f"\n>>> OVER THE RECORD'S {n_all} DISTINCT PUBLISHED SELECTION NUMBERS "
      f"(3 panels x 9 theta x 3 cadences x 2 quantile families):")
    P(f"    MAJORITY-BOTH (|BOTH| > |SELECTION|) : {n_maj}/{n_all} = {n_maj/n_all:.1%}")
    P(f"    DOMINANT-BOTH (|BOTH| is the largest leg) : {n_dom}/{n_all} = {n_dom/n_all:.1%}")
    P(f"    mean |BOTH|/|SELECTION| = {F.both_over_sel.replace(np.inf, np.nan).mean():.3f}   "
      f"median {F.both_over_sel.replace(np.inf, np.nan).median():.3f}   "
      f"mean BOTH share of |ADD|+|DROP|+|BOTH| = {F.both_share.mean():.1%}")
    P(f"    H_MAJ (>= 50%): {'HOLDS' if n_maj / n_all >= 0.50 else 'FAILS'}")

    P("\nBY PANEL:")
    P(fmt(F.groupby("panel").agg(n=("majority_BOTH", "size"),
                                 maj=("majority_BOTH", "sum"),
                                 rate=("majority_BOTH", "mean"),
                                 domBOTH=("dominant_BOTH", "sum"),
                                 mean_ratio=("both_over_sel",
                                             lambda s: s.replace(np.inf, np.nan).mean()),
                                 mean_BOTH=("BOTH_pp", "mean"),
                                 mean_SEL=("sel_geo_pp", "mean"),
                                 mean_share=("both_share", "mean")).reindex(PANELS)))
    P("\nBY CADENCE (H_CAD):")
    bc = F.groupby("cad").agg(n=("majority_BOTH", "size"), maj=("majority_BOTH", "sum"),
                              rate=("majority_BOTH", "mean"),
                              mean_BOTH=("BOTH_pp", "mean"), mean_SEL=("sel_geo_pp", "mean"),
                              mean_share=("both_share", "mean")).reindex(CADENCES)
    P(fmt(bc))
    pooled = n_maj / n_all
    worst_cad = float((bc.rate - pooled).abs().max())
    P(f"  worst |rate - pooled| across cadences = {worst_cad:.3f} (bar {CAD_BAR:.2f})  "
      f"H_CAD {'HOLDS' if worst_cad < CAD_BAR else 'FAILS'}")
    P("\nBY QUANTILE FAMILY:")
    P(fmt(F.groupby("qfam").agg(n=("majority_BOTH", "size"), maj=("majority_BOTH", "sum"),
                                rate=("majority_BOTH", "mean"),
                                mean_BOTH=("BOTH_pp", "mean"),
                                mean_SEL=("sel_geo_pp", "mean"))))
    P("\nBY THETA (the matching depth rung):")
    P(fmt(F.groupby("theta").agg(x=("x", "mean"), n=("majority_BOTH", "size"),
                                 maj=("majority_BOTH", "sum"), rate=("majority_BOTH", "mean"),
                                 mean_BOTH=("BOTH_pp", "mean"),
                                 mean_SEL=("sel_geo_pp", "mean"),
                                 overlap=("overlap", "mean")).sort_index(ascending=False)))

    # which of the RECORD'S OWN committed rows are majority-BOTH
    P("\n" + "=" * 185)
    P("THE COMMITTED ROWS THEMSELVES.  Each committed row is joined to its cell's BOTH leg; "
      "'con' duplicates SELECTION by construction.")
    P("=" * 185)
    key = F.set_index(["panel", "theta", "cad", "qfam"])
    tot_rows, tot_maj = 0, 0
    for path, keys in ((IDEA305, k305), (IDEA51R, ["theta", "cad", "con"])):
        if not path.exists():
            continue
        old = pd.read_csv(path)
        if "panel" not in old.columns:
            old["panel"] = "SMALL439"
        if "qfam" not in old.columns:
            old["qfam"] = "QUANTILE-M"
        j = old.merge(F[["panel", "theta", "cad", "qfam", "BOTH_pp", "sel_geo_pp",
                         "both_over_sel", "majority_BOTH", "dominant"]],
                      on=["panel", "theta", "cad", "qfam"], how="left")
        nm = int(j.majority_BOTH.sum())
        tot_rows += len(j)
        tot_maj += nm
        P(f"  {path.name:78s}  {len(j):4d} committed rows, {nm:4d} majority-BOTH "
          f"({nm/len(j):.1%})")
    P(f"  {'TOTAL committed rows carrying a SELECTION number':78s}  {tot_rows:4d} rows, "
      f"{tot_maj:4d} majority-BOTH ({tot_maj/max(tot_rows,1):.1%})")
    P(f"  (the two files overlap: idea 51R's 54 rows are an exact subset of idea 305's "
      f"SMALL439 / QUANTILE-M rows - see R2's worst |d|.)")

    # ------------------------------------------------------------ H_DEPTH
    P("\n" + "=" * 185)
    P("H_DEPTH - is the mismatch leg a function of the matched depth x, or of the panel label?")
    P("=" * 185)
    D = F[np.isfinite(F.both_over_sel) & (F.both_over_sel > 0)].copy()
    D["lr"] = np.log(D.both_over_sel)
    rho = float(pd.Series(D.both_over_sel).rank().corr(pd.Series(D.x).rank()))
    X0 = np.column_stack([np.ones(len(D)), D.x.values])
    _, e0 = ols(X0, D.lr.values)
    dum = pd.get_dummies(D.panel, drop_first=True).astype(float).values
    X1 = np.column_stack([X0, dum])
    _, e1 = ols(X1, D.lr.values)
    cut = 1 - e1.std() / e0.std()
    P(f"  rank rho(|BOTH|/|SEL|, x) over {len(D)} cells = {rho:+.4f}  (bar |rho| >= {RHO_BAR})")
    P(f"  residual SD of log(|BOTH|/|SEL|) ~ x : {e0.std():.4f} -> {e1.std():.4f} with panel "
      f"dummies, cut {cut:.1%} (bar < {PANEL_DUMMY_BAR:.0%})")
    P(f"  H_DEPTH {'HOLDS' if (abs(rho) >= RHO_BAR and cut < PANEL_DUMMY_BAR) else 'FAILS'}"
      f"  (a: {'pass' if abs(rho) >= RHO_BAR else 'fail'}, "
      f"b: {'pass' if cut < PANEL_DUMMY_BAR else 'fail'})")
    P(f"  overlap (share of the MA slice's names also in the quantile slice) mean "
      f"{F.overlap.mean():.4f}, min {F.overlap.min():.4f}, max {F.overlap.max():.4f} - "
      f"the mismatch channel is open wherever overlap < 1 at unequal weights.")
    flush_log()

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 185)
    P(f"RULE 8 WALK-FORWARD.  IS <= {IS_END} (choice), OOS >= {OOS_START} (read once).")
    P("=" * 185)
    wf = []
    IS = L[L.window == "IS"].set_index(["panel", "theta", "cad", "qfam"])
    OS = L[L.window == "OOS"].set_index(["panel", "theta", "cad", "qfam"])
    common = IS.index.intersection(OS.index)
    agree_maj = int((IS.loc[common, "majority_BOTH"].values ==
                     OS.loc[common, "majority_BOTH"].values).sum())
    agree_dom = int((IS.loc[common, "dominant"].values ==
                     OS.loc[common, "dominant"].values).sum())
    agree_sign = int((np.sign(IS.loc[common, "sel_geo_pp"].values) ==
                      np.sign(OS.loc[common, "sel_geo_pp"].values)).sum())
    n_c = len(common)
    P(f"WF-A  the majority-BOTH LABEL chosen on IS and read on OOS: agrees "
      f"{agree_maj}/{n_c} = {agree_maj/n_c:.1%}")
    P(f"      the DOMINANT leg agrees {agree_dom}/{n_c} = {agree_dom/n_c:.1%};  "
      f"the SELECTION SIGN agrees {agree_sign}/{n_c} = {agree_sign/n_c:.1%}")
    P(f"      IS majority-BOTH rate {IS.loc[common,'majority_BOTH'].mean():.1%}  ->  "
      f"OOS {OS.loc[common,'majority_BOTH'].mean():.1%}")
    wf.append(dict(test="WF-A majority-BOTH label", n=n_c, agree=agree_maj,
                   rate=agree_maj / n_c))
    wf.append(dict(test="WF-A dominant leg", n=n_c, agree=agree_dom, rate=agree_dom / n_c))
    wf.append(dict(test="WF-A SELECTION sign", n=n_c, agree=agree_sign, rate=agree_sign / n_c))

    P("\nWF-B  pick the single book with the best IS Sharpe (per panel, over all 162 books of "
      "that panel) and read its OOS ONCE:")
    for pn in PANELS:
        sub = G[G.panel == pn]
        b = sub.loc[sub.isSharpe.idxmax()]
        sp, lv = spy_by_panel[pn], live_by_panel[pn]
        P(f"  {pn:9s} IS pick: theta {b.theta:+.2f} {b.cad} {b.family}/{b.con} "
          f"(IS Sharpe {b.isSharpe:.4f})  ->  OOS Sharpe {b.oSharpe:.4f} "
          f"CAGR {b.oCAGR:.2%} MaxDD {b.oMaxDD:.1%}   |   "
          f"RULES v2 OOS {lv['oSharpe']:.4f}  SPY OOS {sp['oSharpe']:.4f} "
          f"(CAGR {sp['oCAGR']:.2%})   beats v2 "
          f"{'YES' if b.oSharpe > lv['oSharpe'] else 'no'}, beats SPY "
          f"{'YES' if b.oSharpe > sp['oSharpe'] else 'no'}")
        wf.append(dict(test=f"WF-B {pn}", pick=f"{b.theta:+.2f}/{b.cad}/{b.family}/{b.con}",
                       IS_Sharpe=b.isSharpe, OOS_Sharpe=b.oSharpe, OOS_CAGR=b.oCAGR,
                       OOS_MaxDD=b.oMaxDD, v2_OOS=lv["oSharpe"], spy_OOS=sp["oSharpe"],
                       beat_v2=bool(b.oSharpe > lv["oSharpe"]),
                       beat_spy=bool(b.oSharpe > sp["oSharpe"])))
    nb_v2 = sum(1 for w in wf if w["test"].startswith("WF-B") and w.get("beat_v2"))
    nb_spy = sum(1 for w in wf if w["test"].startswith("WF-B") and w.get("beat_spy"))
    P(f"  WF-B books beating RULES v2 OOS: {nb_v2}/{len(PANELS)};  beating SPY OOS: "
      f"{nb_spy}/{len(PANELS)}")

    P("\nWF-C  fit log(|BOTH|/|SEL|) ~ x on IS cells, score on OOS cells (MAE vs the pooled IS "
      "mean and vs zero):")
    Di = L[(L.window == "IS") & np.isfinite(L.both_over_sel) & (L.both_over_sel > 0)].copy()
    Do = L[(L.window == "OOS") & np.isfinite(L.both_over_sel) & (L.both_over_sel > 0)].copy()
    Di["lr"], Do["lr"] = np.log(Di.both_over_sel), np.log(Do.both_over_sel)
    for pn in ["ALL"] + PANELS:
        di = Di if pn == "ALL" else Di[Di.panel == pn]
        do = Do if pn == "ALL" else Do[Do.panel == pn]
        if len(di) < 5 or len(do) < 5:
            continue
        bcoef, _ = ols(np.column_stack([np.ones(len(di)), di.x.values]), di.lr.values)
        pred = np.column_stack([np.ones(len(do)), do.x.values]) @ bcoef
        mae_m = float(np.abs(do.lr.values - pred).mean())
        mae_c = float(np.abs(do.lr.values - di.lr.mean()).mean())
        mae_0 = float(np.abs(do.lr.values).mean())
        P(f"  {pn:9s} n_IS {len(di):3d} n_OOS {len(do):3d}  MAE model {mae_m:.4f}  "
          f"IS-mean {mae_c:.4f}  zero {mae_0:.4f}  -> model "
          f"{'BEATS' if mae_m < mae_c and mae_m < mae_0 else 'does NOT beat'} both")
        wf.append(dict(test=f"WF-C {pn}", n=len(do), mae_model=mae_m, mae_ismean=mae_c,
                       mae_zero=mae_0,
                       beats=bool(mae_m < mae_c and mae_m < mae_0)))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)
    flush_log()

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 185)
    P(f"KEEP PATHS over all {len(G)} books (4a vs the live RULES v2 book, 4b vs SPY; "
      f"both evaluated for every book).")
    P("=" * 185)
    G.to_csv(f"{OUT}.keeppaths.csv", index=False)
    n4a, n4b = int(G.p4a.sum()), int(G.p4b.sum())
    both_k = int((G.p4a & G.p4b).sum())
    P(f"  4a passers: {n4a}/{len(G)}    4b passers: {n4b}/{len(G)}    BOTH: {both_k}/{len(G)}")
    P("  4b failure reasons (first-fail SET, not first clause):")
    P(fmt(G.f4b.value_counts().rename("n").to_frame()))
    if n4b:
        P("\n  every 4b passer:")
        P(fmt(G[G.p4b][["panel", "theta", "cad", "family", "con", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "oCAGR", "turn_yr"]].reset_index(drop=True)))
    if n4a:
        P("\n  every 4a passer:")
        P(fmt(G[G.p4a][["panel", "theta", "cad", "family", "con", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "f4b"]].reset_index(drop=True)))
    P("\n  best book per panel by full-sample Sharpe (reference only, chosen with hindsight):")
    for pn in PANELS:
        sub = G[G.panel == pn]
        b = sub.loc[sub.Sharpe.idxmax()]
        P(f"    {pn:9s} theta {b.theta:+.2f} {b.cad} {b.family}/{b.con}: CAGR {b.CAGR:.2%} "
          f"Sharpe {b.Sharpe:.4f} MaxDD {b.MaxDD:.1%} halves {b.H1:.3f}/{b.H2:.3f} "
          f"4a {b.p4a} 4b-fails {b.f4b}")

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 185)
    P("VERDICT")
    P("=" * 185)
    P(f"1. The record's SELECTION/LEVEL/TIMING split lives in {len(CEN)} committed files, "
      f"{int(CEN.n_rows.sum())} rows, {n_all} distinct cells.")
    P(f"2. {n_maj}/{n_all} = {n_maj/n_all:.1%} of the distinct published SELECTION numbers are "
      f"MAJORITY-BOTH; {n_dom}/{n_all} = {n_dom/n_all:.1%} are dominant-BOTH.")
    P(f"   H_MAJ {'HOLDS' if n_maj/n_all >= 0.50 else 'FAILS'}.  "
      f"H_CAD {'HOLDS' if worst_cad < CAD_BAR else 'FAILS'}.  "
      f"H_DEPTH {'HOLDS' if (abs(rho) >= RHO_BAR and cut < PANEL_DUMMY_BAR) else 'FAILS'}.")
    P(f"3. Rule 8: the majority-BOTH label chosen IS holds OOS {agree_maj}/{n_c} "
      f"({agree_maj/n_c:.1%}); WF-B beats RULES v2 OOS {nb_v2}/{len(PANELS)} and SPY "
      f"{nb_spy}/{len(PANELS)}.")
    P(f"4. KEEP: 4a {n4a}/{len(G)}, 4b {n4b}/{len(G)}, BOTH {both_k}/{len(G)}.  "
      f"No book is promoted by this idea.")
    P("5. SURVIVORSHIP restated: B136 / SMALL439 are current constituents; the CAGR and 4b "
      "columns are not immune.")
    flush_log()


if __name__ == "__main__":
    main()
