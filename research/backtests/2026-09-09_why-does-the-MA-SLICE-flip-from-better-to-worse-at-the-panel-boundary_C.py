#!/usr/bin/env python3
"""Idea 556 (lane C, 2026-09-09) - why-does-the-MA-SLICE-flip-from-better-to-worse-at-the-
panel-boundary.

QUESTION
--------
Idea 305's exact attribution of the MA gate's zero-cost CAGR advantage over a DEPTH-MATCHED
quantile gate splits it as

    dCAGR0_dg = SELECTION + LEVEL + TIMING          (pp/yr)

and reports the SELECTION leg as **+1.2436 (SMALL439)** against **-0.5779 (U56)** and
**-0.4058 (B136)** - the same gate, the same ranking, the same matching, yet the MA
threshold's slice is a BETTER slice on small caps and a WORSE one on large caps.  The queue
asks: decompose SELECTION into the names the MA slice ADDS and the names it DROPS at matched
depth, and report which side carries the sign.

WHAT SELECTION IS
-----------------
SELECTION = 100 * (CAGR of the zero-cost RESPREAD MA book - CAGR of the zero-cost RESPREAD
depth-matched QUANTILE book).  RESPREAD spreads a FIXED gross of 0.75 over whatever names the
gate admits, so both arms carry the same exposure every day and the difference is purely
"which names".  The two gates are depth-matched by construction: x is set to the MA gate's
own mean mask fraction at that theta (idea 300's matching, reproduced here).

THE DECOMPOSITION (exact, no modelling)
---------------------------------------
Let W^MA_t and W^Q_t be the two arms' HELD weights (post-lag, post-drift, straight out of the
engine) and r_t the daily name returns.  The zero-cost book return is exactly
r0_t = sum_i W_i,t r_i,t, so

    gap_t = sum_i (W^MA - W^Q)_i,t r_i,t
          = sum_{i in ADD}  W^MA_i,t r_i,t          (names only the MA slice holds)
          - sum_{i in DROP} W^Q_i,t  r_i,t          (names only the quantile slice holds)
          + sum_{i in BOTH} (W^MA - W^Q)_i,t r_i,t  (shared names, DEPTH-MISMATCH weight gap)

with ADD/DROP/BOTH read off the two weight matrices day by day.  The three legs sum to gap_t
identically (gate: max |residual| < 1e-12).  Annualised arithmetically (252 x mean x 100) they
are ADD_pp, DROP_pp, BOTH_pp; the difference between their sum and idea 305's geometric
SELECTION is a pure Jensen term, reported.  A fourth leg COST_pp = -(turn_ma - turn_q)*bps/1e4
annualised carries the 10-bps rung, so the four legs sum to the NET (10 bps) arithmetic gap.

PRE-REGISTERED HYPOTHESES (stated before any result is read)
------------------------------------------------------------
H_ADD      : on SMALL439, over the thetas where SELECTION > 0, the ADD leg is the larger of
             the two by absolute size (|ADD_pp| > |DROP_pp|) - i.e. the small-cap MA slice
             wins by the names it BUYS, not by the names it AVOIDS.
H_PANEL    : the dominant side is a PANEL property - the same side dominates at every theta
             within a panel, and the dominant side differs between SMALL439 and U56/B136.
H_DEPTH    : the alternative - SELECTION's sign is a function of the MATCHED DEPTH x, not of
             the panel.  Tested two ways: (a) nearest-x cross-panel pairs (|dx| <= 0.05) agree
             in sign; (b) in a pooled regression of sel_pp on x, the panel dummies are not
             needed (drop in residual SD from adding them < 25%).

TUNED PARAMETERS: exactly 2 - panel {U56, B136, SMALL439} x theta (9 rungs).  x is a
deterministic function of theta (the matching), not a dial.  Cadence is FIXED at W (the live
cadence).  Family {MA-THRESH, QUANTILE-M, QUANTILE-F} and construction {RESPREAD, DEGROSS} are
REPORTED contrasts, not selected over.  Every grid point is reported.

REPRODUCTION GATE (R1): every cadence-W row of idea 305's committed pairs.csv - sel_pp,
level_pp, timing_pp, dCAGR0_dg_pp, dSharpe, dSharpe_oos over 108 rows - must be reproduced
to 1e-9 before any new number is read.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine), no shorting, no leverage,
gross 0.75.  Rule 8 walk-forward IS = start..2016-12-31 (choice), OOS = 2017-01-01..end (read
once): WF-A sign-hold of the dominant side, WF-B book pick by IS Sharpe scored OOS against
RULES v2 and SPY, WF-C the depth-vs-panel model fitted IS and scored OOS.  BOTH KEEP paths
(4a vs the live RULES v2 book, 4b vs SPY) evaluated on all 162 books.

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels are inflated and
the 4a/4b columns are not immune.  The ADD/DROP legs are same-panel arm-minus-arm differences
so the bias very largely cancels there, but the ADD side is exactly the side survivorship
flatters most (names that survived), which is stated again beside the headline.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .legs.csv .pairs.csv .grid.csv .depth.csv .walkforward.csv .keeppaths.csv .console.txt
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
CADENCE = "W"                                  # FIXED (live cadence) - not a dial here
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M", "QUANTILE-F"]
Q_FAMS = ["QUANTILE-M", "QUANTILE-F"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS = 1e-12                    # a name is "held" if its drifted weight exceeds this
BAR_IDENT = 1e-12              # ADD+DROP+BOTH must reconstruct the gap to this
BAR_R0 = 1e-12                 # (W*r).sum must equal returns + turnover*bps/1e4 to this
DX_BAR = 0.05                  # nearest-x cross-panel pairing tolerance (H_DEPTH a)
PANEL_DUMMY_BAR = 0.25         # H_DEPTH b: panel dummies must cut residual SD by < 25%

IDEA305 = REPO / "research" / "backtests" / \
    "2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.pairs.csv"
R1_TOL = 1e-9

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 700)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- panels (idea 300/305/306)
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


# ---------------------------------------------------------------- the ADD / DROP decomposition
def legs(Wm, Wq, R, turn_m, turn_q, lo, hi, tag, years_full, n_full):
    """Exact three-leg split of the zero-cost RESPREAD gap over a window, plus the cost leg."""
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
    return dict(
        window=tag, ident_max=ident,
        ADD_pp=add_pp, DROP_pp=drop_pp, BOTH_pp=both_pp,
        arith_pp=add_pp + drop_pp + both_pp, sel_geo_pp=geo,
        jensen_pp=geo - (add_pp + drop_pp + both_pp),
        COST_pp=cost_pp, net10_pp=add_pp + drop_pp + both_pp + cost_pp,
        n_add=float(add.sum(axis=1).mean()), n_drop=float(drop.sum(axis=1).mean()),
        n_both=float(both.sum(axis=1).mean()), n_ma=float(on_a.sum(axis=1).mean()),
        overlap=float(both.sum(axis=1).mean() / max(on_a.sum(axis=1).mean(), 1e-9)),
        w_add=float(wA.mean()), w_drop=float(wD.mean()),
        rbar_add=(252 * 100 * cA.sum() / wA.sum()) if wA.sum() > 1e-12 else np.nan,
        rbar_drop=(252 * 100 * (-cD).sum() / wD.sum()) if wD.sum() > 1e-12 else np.nan,
        dom=("ADD" if abs(add_pp) > abs(drop_pp) else "DROP"),
        sign_sel=int(np.sign(geo)),
        turn_ma=float(turn_m.loc[sl].sum() / yrs), turn_q=float(turn_q.loc[sl].sum() / yrs))


# ---------------------------------------------------------------- main
def main():
    PN, n_dropped = panels()

    P("=" * 180)
    P("Idea 556 why-does-the-MA-SLICE-flip-from-better-to-worse-at-the-panel-boundary "
      "(lane C) | " + Path(__file__).name)
    P("=" * 180)
    P("QUESTION: idea 305's SELECTION leg is +1.2436 pp/yr (SMALL439) vs -0.5779 (U56) and "
      "-0.4058 (B136) for the same gate on")
    P("          the same ranking at matched depth.  Split SELECTION into the names the MA "
      "slice ADDS and the ones it DROPS.")
    P("PRE-REGISTERED  H_ADD    : on SMALL439, at every theta with SELECTION > 0, "
      "|ADD_pp| > |DROP_pp|.")
    P("                H_PANEL  : the dominant side is a panel property - constant within a "
      "panel, different on SMALL439 vs U56/B136.")
    P(f"                H_DEPTH  : SELECTION's sign tracks the matched depth x, not the panel."
      f"  (a) nearest-x pairs (|dx| <= {DX_BAR}) agree in sign;")
    P(f"                           (b) panel dummies cut the residual SD of sel_pp ~ x by "
      f"< {PANEL_DUMMY_BAR:.0%}.")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = sum_i W_i r_i, gated at "
      f"{BAR_R0:.0e} against returns + turnover*bps/1e4),")
    P(f"gross {GROSS}, next-day execution, no shorting, no leverage, cadence {CADENCE} FIXED.")
    P(f"tuned dials (2): panel {PANELS} x theta {MA_THETA}.  x = the MA gate's own mean mask "
      f"fraction, a deterministic function of theta.")
    P(f"reported contrasts: family {FAMILIES} x construction {CONSTRUCTIONS} = "
      f"{len(PANELS) * len(MA_THETA) * len(FAMILIES) * len(CONSTRUCTIONS)} books, all reported.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels inflated and "
      "4a/4b columns NOT immune.  The ADD/DROP")
    P("              legs are same-panel arm-minus-arm differences so the bias very largely "
      "cancels, but the ADD side is the side")
    P("              survivorship flatters most - restated beside the headline.")
    for pn in PANELS:
        px, _ = PN[pn]
        P(f"  PANEL {pn:9s}: {px.shape[1]:3d} names, {px.index[0].date()}..{px.index[-1].date()}"
          f", {len(px)} bars"
          + (f" ({n_dropped} dropped for max_1d_move >= 1.0)" if pn == "SMALL439" else ""))
    flush_log()

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, pairs, legrows, matchrows = [], [], [], []
    r0_gate_max = 0.0
    spy_by_panel, live_by_panel, ctrl_by_panel = {}, {}, {}

    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        R = px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        spy_by_panel[pn], live_by_panel[pn] = spy_s, live_s

        rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=CADENCE)
        ctrl = stat(rc["returns"].loc[start:])
        ctrl_by_panel[pn] = ctrl

        P("\n" + "=" * 180)
        P(f"PANEL {pn} - comparands over {start.date()}..{px.index[-1].date()} ({years:.2f} yrs)")
        P("=" * 180)
        P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} "
          f"OOS {spy_s['oSharpe']:.4f} oCAGR {spy_s['oCAGR']:.4f} oMaxDD {spy_s['oMaxDD']:.4f}")
        P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS {live_s['oSharpe']:.4f} oCAGR {live_s['oCAGR']:.4f} oMaxDD {live_s['oMaxDD']:.4f}")
        P(f"CONTROL EWall {CADENCE} (no gate)   : CAGR {ctrl['CAGR']:.4f} Sharpe "
          f"{ctrl['Sharpe']:.4f} MaxDD {ctrl['MaxDD']:.4f}")
        P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70 * spy_s['CAGR']:.2%}")

        live = live_mask(px).loc[start:]
        nlive = live.sum(axis=1)
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
            arms = {}
            for fam in FAMILIES:
                for con in CONSTRUCTIONS:
                    res = backtest(px, book(px, gates[th][fam], con),
                                   cost_bps=COST_BPS, freq=CADENCE)
                    r10 = res["returns"].loc[start:]
                    turn = res["turnover"].loc[start:]
                    W = res["weights"].loc[start:]
                    r0 = r10 + turn * COST_BPS / 1e4
                    r0_gate_max = max(r0_gate_max, float(((W * R).sum(axis=1) - r0).abs().max()))
                    s = stat(r10)
                    arms[(fam, con)] = dict(W=W, turn=turn, s=s, r0=r0)
                    rows.append(dict(panel=pn, theta=th, x=xth, cad=CADENCE, family=fam,
                                     con=con, **s, CAGR0=cagr(r0),
                                     turn_yr=float(turn.sum() / years),
                                     dCAGR_ctrl=s["CAGR"] - ctrl["CAGR"],
                                     dSharpe_ctrl=s["Sharpe"] - ctrl["Sharpe"],
                                     p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))

            ma_rs = arms[("MA-THRESH", "RESPREAD")]
            for qfam in Q_FAMS:
                q_rs = arms[(qfam, "RESPREAD")]
                for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                    ("OOS", OOS_START, None)):
                    d = legs(ma_rs["W"], q_rs["W"], R, ma_rs["turn"], q_rs["turn"],
                             lo, hi, tag, years, len(R))
                    legrows.append(dict(panel=pn, theta=th, x=xth, qfam=qfam, **d))
                for con in CONSTRUCTIONS:
                    a, b = arms[("MA-THRESH", con)]["s"], arms[(qfam, con)]["s"]
                    pairs.append(dict(panel=pn, theta=th, x=xth, con=con, qfam=qfam,
                                      Sharpe_ma=a["Sharpe"], Sharpe_q=b["Sharpe"],
                                      dSharpe=a["Sharpe"] - b["Sharpe"],
                                      dSharpe_oos=a["oSharpe"] - b["oSharpe"],
                                      dCAGR_pp=100 * (a["CAGR"] - b["CAGR"]),
                                      dMaxDD_pp=100 * (a["MaxDD"] - b["MaxDD"])))
            P(f"  {pn}: theta {th:+.2f} (x={xth:.4f}) done "
              f"({len(FAMILIES) * len(CONSTRUCTIONS)} books)")
            flush_log()

    G, L = pd.DataFrame(rows), pd.DataFrame(legrows)
    PR, M = pd.DataFrame(pairs), pd.DataFrame(matchrows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L.to_csv(f"{OUT}.legs.csv", index=False)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)

    # ------------------------------------------------------------ gates
    P("\n" + "=" * 180)
    P("GATES")
    P("=" * 180)
    P(f"G1 zero-cost identity  : max |sum_i W_i r_i - (ret + turnover*bps/1e4)| = "
      f"{r0_gate_max:.3e}  (bar {BAR_R0:.0e})  "
      f"{'PASS' if r0_gate_max < BAR_R0 else 'FAIL'}")
    im = float(L.ident_max.max())
    P(f"G2 three-leg identity  : max |ADD+DROP+BOTH - gap| over {len(L)} cells = {im:.3e}  "
      f"(bar {BAR_IDENT:.0e})  {'PASS' if im < BAR_IDENT else 'FAIL'}")

    # R1 reproduction of idea 305's cadence-W rows
    if IDEA305.exists():
        old = pd.read_csv(IDEA305)
        old = old[old.cad == "W"].copy()
        mine = PR.merge(old, on=["panel", "theta", "con", "qfam"], suffixes=("", "_305"))
        cols = [("dSharpe", "dSharpe_305"), ("dSharpe_oos", "dSharpe_oos_305"),
                ("dCAGR_pp", "dCAGR_pp_305"), ("dMaxDD_pp", "dMaxDD_pp_305")]
        worst = max(float((mine[a] - mine[b]).abs().max()) for a, b in cols)
        selchk = L[(L.window == "FULL") & (L.qfam == "QUANTILE-M")][
            ["panel", "theta", "sel_geo_pp"]]
        o2 = old[(old.con == "RESPREAD") & (old.qfam == "QUANTILE-M")][
            ["panel", "theta", "sel_pp"]]
        s2 = selchk.merge(o2, on=["panel", "theta"])
        worst_sel = float((s2.sel_geo_pp - s2.sel_pp).abs().max())
        P(f"R1 idea-305 pairs.csv  : {len(mine)} cadence-W rows x 4 columns, worst |d| = "
          f"{worst:.3e} (bar {R1_TOL:.0e})  {'PASS' if worst < R1_TOL else 'FAIL'}")
        P(f"R1b SELECTION leg      : {len(s2)} rows, worst |sel_geo - sel_305| = "
          f"{worst_sel:.3e} (bar {R1_TOL:.0e})  "
          f"{'PASS' if worst_sel < R1_TOL else 'FAIL'}")
    else:
        P("R1 idea-305 pairs.csv  : NOT FOUND - reproduction gate could not be run")

    # ------------------------------------------------------------ headline
    F = L[(L.window == "FULL") & (L.qfam == "QUANTILE-M")].copy()
    P("\n" + "=" * 180)
    P("THE DECOMPOSITION.  SELECTION = ADD + DROP + BOTH (+ Jensen).  ADD = names only the MA "
      "slice holds (its own weights);")
    P("DROP = -1 x names only the depth-matched quantile slice holds; BOTH = shared names at "
      "the two arms' weight difference.")
    P("All pp/yr, ZERO cost (COST_pp is the 10-bps leg; net10 = arith + COST).  "
      "QUANTILE-M (integer gate) shown; QUANTILE-F below.")
    P("=" * 180)
    show = ["panel", "theta", "x", "ADD_pp", "DROP_pp", "BOTH_pp", "arith_pp", "jensen_pp",
            "sel_geo_pp", "COST_pp", "net10_pp", "n_add", "n_drop", "n_both", "overlap",
            "w_add", "w_drop", "rbar_add", "rbar_drop", "dom"]
    P(fmt(F[show].reset_index(drop=True)))

    P("\nPANEL MEANS over the 9 thetas (QUANTILE-M, FULL sample):")
    agg = F.groupby("panel").agg(ADD=("ADD_pp", "mean"), DROP=("DROP_pp", "mean"),
                                 BOTH=("BOTH_pp", "mean"), arith=("arith_pp", "mean"),
                                 jensen=("jensen_pp", "mean"), SEL=("sel_geo_pp", "mean"),
                                 COST=("COST_pp", "mean"), net10=("net10_pp", "mean"),
                                 rbar_add=("rbar_add", "mean"),
                                 rbar_drop=("rbar_drop", "mean"),
                                 n_add=("n_add", "mean"), n_drop=("n_drop", "mean"),
                                 overlap=("overlap", "mean"),
                                 dom_ADD=("dom", lambda s: int((s == "ADD").sum())),
                                 pos_sel=("sign_sel", lambda s: int((s > 0).sum())))
    agg = agg.reindex(PANELS)
    P(fmt(agg))
    P("\n(idea 305's published SELECTION panel means, pooled over 3 cadences and 2 qfams: "
      "U56 -0.5779 / B136 -0.4058 / SMALL439 +1.2436.")
    P(" The column SEL above is the same statistic at cadence W and QUANTILE-M only, so it is "
      "a SUBSET of that pool, not a restatement.)")

    P("\nWHERE THE PANEL SPREAD LIVES.  SMALL439 minus U56, per leg (pp/yr, and as a share of "
      "the SELECTION spread):")
    sp_row = agg.loc["SMALL439"] - agg.loc["U56"]
    tot = sp_row["SEL"]
    for leg in ["ADD", "DROP", "BOTH", "arith", "jensen", "SEL"]:
        P(f"    {leg:7s}: {sp_row[leg]:+8.4f}"
          + (f"   ({sp_row[leg] / tot:+.1%} of the SELECTION spread)"
             if leg not in ("SEL",) and abs(tot) > 1e-9 else ""))
    sp_b = agg.loc["SMALL439"] - agg.loc["B136"]
    P("  SMALL439 minus B136: " + " ".join(f"{k} {sp_b[k]:+.4f}"
                                           for k in ["ADD", "DROP", "BOTH", "SEL"]))

    P("\nIS 'SELECTION' EVEN A NAMES STATISTIC?  BOTH is the SHARED names carried at DIFFERENT "
      "weights - a daily depth mismatch, not a")
    P("choice of names.  The matching pins the MEAN mask fraction, not the daily one.  "
      "|BOTH| as a share of |ADD|+|DROP|+|BOTH|:")
    absshare = F.assign(sh=F.BOTH_pp.abs() /
                        (F.ADD_pp.abs() + F.DROP_pp.abs() + F.BOTH_pp.abs()))
    P("    " + "  ".join(f"{pn} {absshare[absshare.panel == pn].sh.mean():.1%}"
                         for pn in PANELS)
      + f"   | pooled {absshare.sh.mean():.1%}"
      + f"   | cells where |BOTH| > |SELECTION|: "
        f"{int((F.BOTH_pp.abs() > F.sel_geo_pp.abs()).sum())}/{len(F)}")

    P("\nQUANTILE-F (fractional gate, exact depth match) panel means:")
    FF = L[(L.window == "FULL") & (L.qfam == "QUANTILE-F")]
    P(fmt(FF.groupby("panel").agg(ADD=("ADD_pp", "mean"), DROP=("DROP_pp", "mean"),
                                  BOTH=("BOTH_pp", "mean"), SEL=("sel_geo_pp", "mean"),
                                  dom_ADD=("dom", lambda s: int((s == "ADD").sum()))
                                  ).reindex(PANELS)))

    # ------------------------------------------------------------ H_ADD
    P("\n" + "=" * 180)
    P("H_ADD: on SMALL439, at every theta with SELECTION > 0, is |ADD_pp| > |DROP_pp| ?")
    P("=" * 180)
    hadd = {}
    for pn in PANELS:
        sub = F[(F.panel == pn) & (F.sel_geo_pp > 0)]
        n = len(sub)
        k = int((sub.ADD_pp.abs() > sub.DROP_pp.abs()).sum())
        hadd[pn] = (k, n)
        P(f"  {pn:9s}: {k}/{n} positive-SELECTION thetas carried by the ADD side"
          + ("" if n else "   (no positive-SELECTION theta)"))
    ver_add = ("HOLDS" if hadd["SMALL439"][1] and hadd["SMALL439"][0] == hadd["SMALL439"][1]
               else "FAILS")
    P(f"  H_ADD on SMALL439: {ver_add}")

    P("\nSide-by-side of the two per-name rates (exposure-weighted annualised % of the slice):")
    P(fmt(F[["panel", "theta", "x", "rbar_add", "rbar_drop", "sel_geo_pp"]].assign(
        d_rate=F.rbar_add - F.rbar_drop).reset_index(drop=True)))
    P("\n  corr(sel_geo_pp, rbar_add - rbar_drop) pooled = "
      f"{F.sel_geo_pp.corr(F.rbar_add - F.rbar_drop):.4f}; "
      f"per panel " + ", ".join(
          f"{pn} {F[F.panel == pn].sel_geo_pp.corr((F[F.panel == pn].rbar_add - F[F.panel == pn].rbar_drop)):.4f}"
          for pn in PANELS))

    # ------------------------------------------------------------ H_PANEL
    P("\n" + "=" * 180)
    P("H_PANEL: is the dominant side a PANEL property (constant within panel, different on "
      "SMALL439) ?")
    P("=" * 180)
    for pn in PANELS:
        sub = F[F.panel == pn]
        P(f"  {pn:9s}: dominant side by theta "
          + " ".join(f"{t:+.2f}:{d}" for t, d in zip(sub.theta, sub.dom))
          + f"   | ADD dominates {int((sub.dom == 'ADD').sum())}/9"
          + f"   | SELECTION > 0 at {int((sub.sign_sel > 0).sum())}/9")
    const = {pn: F[F.panel == pn].dom.nunique() == 1 for pn in PANELS}
    ver_panel = "HOLDS" if all(const.values()) and \
        F[F.panel == "SMALL439"].dom.iloc[0] != F[F.panel == "U56"].dom.iloc[0] else "FAILS"
    P(f"  within-panel constancy: " + ", ".join(f"{k} {v}" for k, v in const.items()))
    P(f"  H_PANEL: {ver_panel}")

    # ------------------------------------------------------------ H_DEPTH
    P("\n" + "=" * 180)
    P("H_DEPTH: does SELECTION's sign track the MATCHED DEPTH x rather than the panel ?")
    P("=" * 180)
    P("  Note the theta -> x map is panel-specific: theta +0.30 is x = "
      + ", ".join(f"{pn} {float(F[(F.panel == pn) & (F.theta == 0.30)].x.iloc[0]):.4f}"
                  for pn in PANELS) + ".")
    dep = []
    for i, a in F.iterrows():
        for j, b in F.iterrows():
            if a.panel >= b.panel:
                continue
            if abs(a.x - b.x) <= DX_BAR:
                dep.append(dict(pa=a.panel, tha=a.theta, xa=a.x, sa=a.sel_geo_pp, doma=a.dom,
                                pb=b.panel, thb=b.theta, xb=b.x, sb=b.sel_geo_pp, domb=b.dom,
                                dx=abs(a.x - b.x), same_sign=int(np.sign(a.sel_geo_pp) ==
                                                                 np.sign(b.sel_geo_pp)),
                                same_dom=int(a.dom == b.dom)))
    DEP = pd.DataFrame(dep)
    DEP.to_csv(f"{OUT}.depth.csv", index=False)
    if len(DEP):
        P(f"\n  (a) nearest-x cross-panel pairs with |dx| <= {DX_BAR}: {len(DEP)} pairs")
        P(fmt(DEP))
        P(f"      SELECTION sign agrees in {int(DEP.same_sign.sum())}/{len(DEP)}; "
          f"dominant side agrees in {int(DEP.same_dom.sum())}/{len(DEP)}")
    else:
        P("  (a) no cross-panel pair within the tolerance")

    # (b) pooled regression sel ~ x (+ x^2) with and without panel dummies
    X0 = np.column_stack([np.ones(len(F)), F.x.values, F.x.values ** 2])
    D = pd.get_dummies(F.panel, drop_first=True).astype(float).values
    X1 = np.column_stack([X0, D])
    y = F.sel_geo_pp.values
    b0, *_ = np.linalg.lstsq(X0, y, rcond=None)
    b1, *_ = np.linalg.lstsq(X1, y, rcond=None)
    e0, e1 = y - X0 @ b0, y - X1 @ b1
    sd0, sd1 = float(e0.std(ddof=X0.shape[1])), float(e1.std(ddof=X1.shape[1]))
    cut = 1 - sd1 / sd0
    P(f"\n  (b) pooled sel_geo_pp ~ 1 + x + x^2 : resid SD {sd0:.4f} pp/yr, "
      f"R2 {1 - e0.var() / y.var():.4f}")
    P(f"      + panel dummies                : resid SD {sd1:.4f} pp/yr, "
      f"R2 {1 - e1.var() / y.var():.4f}; dummies cut the resid SD by {cut:.1%} "
      f"(bar < {PANEL_DUMMY_BAR:.0%})")
    P(f"      x-only fit: sel = {b0[0]:+.4f} {b0[1]:+.4f}*x {b0[2]:+.4f}*x^2")
    # honest reading of (b): the resid-SD cut is small only because the dummies cost 2 df.
    # Report the incremental F on the panel dummies as well, and say which reading is used.
    r2_0, r2_1 = 1 - e0.var() / y.var(), 1 - e1.var() / y.var()
    df_n = len(F) - X1.shape[1]
    Fstat = ((r2_1 - r2_0) / 2) / ((1 - r2_1) / df_n) if r2_1 < 1 else np.inf
    P(f"      incremental F on the 2 panel dummies = {Fstat:.3f} on (2, {df_n}) df "
      f"(dR2 {r2_1 - r2_0:+.4f}); F < 3.44 is p > 0.05")
    P("      READ HONESTLY: the x-only fit explains only "
      f"{r2_0:.1%} of the cell-level variation, so neither reading is a strong model; the "
      "claim tested here is only")
    P("      that the PANEL LABEL adds nothing once depth is held, which is what the F says.")
    P("\n  (c) the leg that carries the sign, against x: DROP_pp ~ 1 + x + x^2 pooled")
    yD = F.DROP_pp.values
    bD, *_ = np.linalg.lstsq(X0, yD, rcond=None)
    eD = yD - X0 @ bD
    XD1 = np.column_stack([X0, D])
    bD1, *_ = np.linalg.lstsq(XD1, yD, rcond=None)
    eD1 = yD - XD1 @ bD1
    P(f"      x only: R2 {1 - eD.var() / yD.var():.4f}; + panel dummies: "
      f"R2 {1 - eD1.var() / yD.var():.4f}   "
      f"fit: DROP = {bD[0]:+.4f} {bD[1]:+.4f}*x {bD[2]:+.4f}*x^2")
    ver_depth = "HOLDS" if (len(DEP) and DEP.same_sign.mean() >= 0.75
                            and cut < PANEL_DUMMY_BAR) else "FAILS"
    P(f"  H_DEPTH: {ver_depth}")

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 180)
    P(f"RULE 8 WALK-FORWARD.  IS = start..{IS_END} (choice), OOS = {OOS_START}..end (read once)")
    P("=" * 180)
    wf = []

    P("\nWF-A  the sign claim: dominant side and SELECTION sign chosen on IS, checked OOS "
      "(per panel x qfam, 9 thetas each)")
    for pn in PANELS:
        for qf in Q_FAMS:
            a = L[(L.panel == pn) & (L.qfam == qf) & (L.window == "IS")].set_index("theta")
            o = L[(L.panel == pn) & (L.qfam == qf) & (L.window == "OOS")].set_index("theta")
            dom_hold = int((a.dom == o.dom).sum())
            sgn_hold = int((np.sign(a.sel_geo_pp) == np.sign(o.sel_geo_pp)).sum())
            P(f"  {pn:9s} {qf:11s}: dominant side holds {dom_hold}/9, SELECTION sign holds "
              f"{sgn_hold}/9 | IS ADD mean {a.ADD_pp.mean():+.4f} DROP {a.DROP_pp.mean():+.4f}"
              f" -> OOS ADD {o.ADD_pp.mean():+.4f} DROP {o.DROP_pp.mean():+.4f}")
            wf.append(dict(test="WF-A", panel=pn, qfam=qf, dom_hold=dom_hold,
                           sign_hold=sgn_hold, n=9,
                           IS_ADD=a.ADD_pp.mean(), IS_DROP=a.DROP_pp.mean(),
                           OOS_ADD=o.ADD_pp.mean(), OOS_DROP=o.DROP_pp.mean(),
                           IS_SEL=a.sel_geo_pp.mean(), OOS_SEL=o.sel_geo_pp.mean()))

    P("\nWF-B  book pick: per (panel, family, construction) take the theta with the best IS "
      "Sharpe, then read OOS once")
    for pn in PANELS:
        sp, lv = spy_by_panel[pn], live_by_panel[pn]
        for fam in FAMILIES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == pn) & (G.family == fam) & (G.con == con)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                P(f"  {pn:9s} {fam:11s} {con:8s}: IS pick theta {pick.theta:+.2f} "
                  f"(IS Sharpe {pick.isSharpe:.4f}) -> OOS CAGR {pick.oCAGR:.4f} Sharpe "
                  f"{pick.oSharpe:.4f} MaxDD {pick.oMaxDD:.4f} | RULES v2 OOS "
                  f"{lv['oCAGR']:.4f}/{lv['oSharpe']:.4f}/{lv['oMaxDD']:.4f} | SPY OOS "
                  f"{sp['oCAGR']:.4f}/{sp['oSharpe']:.4f}/{sp['oMaxDD']:.4f} | "
                  f"beats v2 {'Y' if pick.oSharpe > lv['oSharpe'] else 'N'} "
                  f"beats SPY {'Y' if pick.oSharpe > sp['oSharpe'] else 'N'}")
                wf.append(dict(test="WF-B", panel=pn, family=fam, con=con, theta=pick.theta,
                               isSharpe=pick.isSharpe, oCAGR=pick.oCAGR,
                               oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                               v2_oSharpe=lv["oSharpe"], spy_oSharpe=sp["oSharpe"],
                               beats_v2=bool(pick.oSharpe > lv["oSharpe"]),
                               beats_spy=bool(pick.oSharpe > sp["oSharpe"])))

    P("\nWF-C  the depth-vs-panel model: fit sel ~ 1+x+x^2 (DEPTH) and a panel-mean model "
      "(PANEL) on IS, score both on OOS")
    LI = L[(L.window == "IS") & (L.qfam == "QUANTILE-M")]
    LO = L[(L.window == "OOS") & (L.qfam == "QUANTILE-M")].reset_index(drop=True)
    Xi = np.column_stack([np.ones(len(LI)), LI.x.values, LI.x.values ** 2])
    bi, *_ = np.linalg.lstsq(Xi, LI.sel_geo_pp.values, rcond=None)
    Xo = np.column_stack([np.ones(len(LO)), LO.x.values, LO.x.values ** 2])
    pred_depth = Xo @ bi
    pm = LI.groupby("panel").sel_geo_pp.mean()
    pred_panel = LO.panel.map(pm).values
    yo = LO.sel_geo_pp.values
    mae = lambda p: float(np.abs(yo - p).mean())
    P(f"  OOS MAE  DEPTH model {mae(pred_depth):.4f} | PANEL model {mae(pred_panel):.4f} | "
      f"zero {mae(np.zeros_like(yo)):.4f} | pooled IS mean "
      f"{mae(np.full_like(yo, LI.sel_geo_pp.mean())):.4f}  (pp/yr, n={len(yo)})")
    P(f"  OOS sign agreement  DEPTH {int((np.sign(pred_depth) == np.sign(yo)).sum())}/{len(yo)}"
      f" | PANEL {int((np.sign(pred_panel) == np.sign(yo)).sum())}/{len(yo)}")
    wf.append(dict(test="WF-C", mae_depth=mae(pred_depth), mae_panel=mae(pred_panel),
                   mae_zero=mae(np.zeros_like(yo)), n=len(yo),
                   sign_depth=int((np.sign(pred_depth) == np.sign(yo)).sum()),
                   sign_panel=int((np.sign(pred_panel) == np.sign(yo)).sum())))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 180)
    P("BOTH KEEP PATHS over all books (4a vs the live RULES v2 book; 4b vs SPY, 10 bps, "
      "full sample)")
    P("=" * 180)
    K = G.copy()
    P(f"  4a passers: {int(K.p4a.sum())}/{len(K)}   4b passers: {int(K.p4b.sum())}/{len(K)}   "
      f"BOTH: {int((K.p4a & K.p4b).sum())}/{len(K)}")
    fails = {}
    for s in K.loc[~K.p4b, "f4b"]:
        for tok in s.split(","):
            fails[tok] = fails.get(tok, 0) + 1
    P("  4b failing legs: " + ", ".join(f"{k} {v}"
                                        for k, v in sorted(fails.items(),
                                                           key=lambda kv: -kv[1])))
    if K.p4a.any():
        P("\n  4a passers:")
        P(fmt(K[K.p4a][["panel", "theta", "x", "family", "con", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "f4b"]].reset_index(drop=True)))
    if K.p4b.any():
        P("\n  4b passers:")
        P(fmt(K[K.p4b][["panel", "theta", "x", "family", "con", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "p4a"]].reset_index(drop=True)))
    K[["panel", "theta", "x", "family", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
       "oSharpe", "oCAGR", "oMaxDD", "p4a", "p4b", "f4b"]].to_csv(
        f"{OUT}.keeppaths.csv", index=False)

    P("\n  the matching (theta -> x) actually achieved:")
    P(fmt(M.reset_index(drop=True)))

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 180)
    P("VERDICT")
    P("=" * 180)
    P(f"  H_ADD   : {ver_add}")
    P(f"  H_PANEL : {ver_panel}")
    P(f"  H_DEPTH : {ver_depth}")
    P(f"  KEEP    : 4a {int(K.p4a.sum())}/{len(K)}, 4b {int(K.p4b.sum())}/{len(K)}, "
      f"BOTH {int((K.p4a & K.p4b).sum())}/{len(K)}")
    flush_log()


if __name__ == "__main__":
    main()
