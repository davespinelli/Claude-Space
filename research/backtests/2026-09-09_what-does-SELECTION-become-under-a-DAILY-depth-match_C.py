#!/usr/bin/env python3
"""Idea 559 (lane C, 2026-09-09) - what-does-SELECTION-become-under-a-DAILY-depth-match.

QUESTION
--------
Idea 305 decomposes the MA-THRESH gate's zero-cost CAGR advantage over a DEPTH-MATCHED
quantile gate as dCAGR0 = SELECTION + LEVEL + TIMING and publishes the SELECTION leg as
+1.2436 pp/yr (SMALL439) against -0.5779 (U56) and -0.4058 (B136).  Idea 556 split that
SELECTION into ADD / DROP / BOTH and found BOTH - the SHARED names carried at DIFFERENT
weights - is 31.5% of the decomposed magnitude and exceeds |SELECTION| in 17 of 27 cells,
because the matching pins the MEAN mask fraction and not the daily one.

The queue's follow-up: pin k_q to k_ma EVERY DAY instead of on average, so the mismatch
channel is closed, and report what SELECTION and its PANEL ORDERING become.

THE THING THAT HAS TO BE SAID FIRST
-----------------------------------
The MA-THRESH gate is `px > MA200 * (1 + theta)`, i.e. `dist > theta` with
`dist = px/MA200 - 1`.  Idea 305's quantile gate ranks on THE SAME `dist`.  So the daily
depth match - take the top k_ma(t) names by dist, where k_ma(t) is the number the MA gate
admits that day - returns the MA gate's OWN SET, day for day.  The contrast is not
narrowed by closing the mismatch channel; it is ANNIHILATED.  That is a testable claim
(H_IDENT, gated at set equality on every day of every panel at every theta), not a remark,
and if it holds then idea 305's SELECTION leg is 100% depth-timing and 0% "which names".

So a second question has to be asked for the run to carry any content: with the mismatch
channel closed, what does a REAL selection contrast look like?  A genuinely different
ranker is needed.  This run uses the record's own 12-1 momentum, `px.shift(21)/px.shift(252)
- 1`, at daily-matched depth (MOM-D) and at idea-305 mean-matched depth (MOM-M), so the
mean-vs-daily channel can be measured on a non-degenerate ranker.

PRE-REGISTERED HYPOTHESES (stated before any result is read)
------------------------------------------------------------
H_IDENT : the daily-matched quantile gate on the MA gate's OWN ranking variable equals the
          MA gate set-for-set on every (panel, theta, day).  Consequence: ADD = DROP =
          BOTH = SELECTION = 0 exactly, and idea 305's SELECTION leg is entirely a depth
          -mismatch artefact.  Bar: max cell disagreement 0, |SELECTION| < 1e-12 pp/yr.
H_ORDER : with the mismatch channel closed and a genuinely different ranker (MOM-D), the
          PANEL ORDERING of the SELECTION leg survives - SMALL439 > B136 > U56, matching
          idea 305's +1.2436 / -0.4058 / -0.5779.
H_DRIFT : the queue's "BOTH is zero by construction" is exact only where there is no
          drift.  At the live weekly cadence the engine re-normalises drifted weights each
          day, so two arms holding a shared name at the same TARGET hold it at different
          weights between rebalances.  Predicted: BOTH_pp is exactly 0 at cadence D and
          non-zero at cadence W for MOM-D, and its share of the decomposed magnitude at W
          is materially below idea 556's mean-matched 31.5%.

TUNED PARAMETERS: exactly 2 - panel {U56, B136, SMALL439} x theta (9 rungs).  The matched
depth is a deterministic function of theta (mean match) or of the day (daily match), not a
dial.  Family {MA-THRESH, QUANTILE-M, QUANTILE-D, MOM-M, MOM-D}, construction {RESPREAD,
DEGROSS} and cadence {W, D} are REPORTED contrasts, not selected over.  Every grid point is
reported.

REPRODUCTION GATES
------------------
R1: idea 556's legs.csv - ADD_pp, DROP_pp, BOTH_pp, sel_geo_pp over its QUANTILE-M rows
    (FULL/IS/OOS x 27 cells) - reproduced to 1e-9.
R2: idea 305's pairs.csv cadence-W QUANTILE-M rows - dSharpe, dSharpe_oos, dCAGR_pp,
    dMaxDD_pp - reproduced to 1e-9.
G1: zero-cost identity sum_i W_i r_i == returns + turnover*bps/1e4 to 1e-12.
G2: three-leg identity ADD+DROP+BOTH == gap to 1e-12 in every cell.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine), no shorting, no leverage,
gross 0.75.  Rule 8 walk-forward IS = start..2016-12-31 (choice), OOS = 2017-01-01..end
(read once): WF-A sign/dominant-side hold, WF-B book pick by IS Sharpe scored OOS against
RULES v2 and SPY, WF-C the depth-vs-panel model for the non-degenerate SELECTION.  BOTH
KEEP paths (4a vs the live RULES v2 book, 4b vs SPY) evaluated on every book.

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels are inflated and
the 4a/4b columns are NOT immune.  The ADD/DROP legs are same-panel arm-minus-arm
differences so the bias very largely cancels there.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its
outputs.  Outputs: .legs.csv .pairs.csv .grid.csv .match.csv .walkforward.csv
.keeppaths.csv .console.txt
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
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
# families: the gate, idea 305's mean-matched control, the daily-matched control on the
# gate's own ranker, and the same two matches on a genuinely different ranker.
FAM_W = ["MA-THRESH", "QUANTILE-M", "QUANTILE-D", "MOM-M", "MOM-D"]
FAM_D = ["MA-THRESH", "QUANTILE-D", "MOM-D"]          # cadence-D contrast, RESPREAD only
CONTROLS_W = ["QUANTILE-M", "QUANTILE-D", "MOM-M", "MOM-D"]
CONTROLS_D = ["QUANTILE-D", "MOM-D"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS = 1e-12
BAR_IDENT = 1e-12
BAR_R0 = 1e-12
BAR_ZERO = 1e-12               # H_IDENT: |SELECTION| under the same-ranker daily match

IDEA556 = REPO / "research" / "backtests" / \
    "2026-09-09_why-does-the-MA-SLICE-flip-from-better-to-worse-at-the-panel-boundary_C.legs.csv"
IDEA305 = REPO / "research" / "backtests" / \
    "2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.pairs.csv"
R_TOL = 1e-9

# idea 305's published SELECTION panel means (pooled over 3 cadences x 2 qfams)
SEL305 = {"U56": -0.5779, "B136": -0.4058, "SMALL439": +1.2436}

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- panels (idea 300/305/556)
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
    """The MA gate's OWN ranking variable: px/MA200 - 1."""
    live = live_mask(px)
    return (px / px.rolling(200).mean() - 1).where(live), live


def mom_rank(px):
    """A genuinely different ranker: the record's 12-1 momentum."""
    live = live_mask(px)
    return (px.shift(21) / px.shift(252) - 1).where(live), live


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def _rank(sig):
    return sig.rank(axis=1, ascending=False, method="first")


def mean_matched(sig, live, x):
    """idea 305's match: k_t = ceil(x * n_live_t) with x the MA gate's MEAN mask fraction."""
    kt = np.ceil(x * live.sum(axis=1)).astype(int).clip(lower=1)
    return _rank(sig).le(kt, axis=0).fillna(False) & live


def daily_matched(sig, live, gm):
    """The queue's match: k_t = k_ma_t, pinned every day (clipped to the rankable count)."""
    k_ma = gm.sum(axis=1)
    n_rank = sig.notna().sum(axis=1)
    kt = np.minimum(k_ma, n_rank)
    return _rank(sig).le(kt, axis=0).fillna(False) & live


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


# ---------------------------------------------------------------- the ADD / DROP / BOTH split
def legs(Wm, Wq, R, turn_m, turn_q, lo, hi, tag, years_full):
    """Exact three-leg split of the zero-cost RESPREAD gap over a window, plus the cost leg.
    Identical arithmetic to idea 556 so its rows reproduce bit-for-bit."""
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
    return dict(
        window=tag, ident_max=ident,
        ADD_pp=add_pp, DROP_pp=drop_pp, BOTH_pp=both_pp,
        arith_pp=add_pp + drop_pp + both_pp, sel_geo_pp=geo,
        jensen_pp=geo - (add_pp + drop_pp + both_pp),
        COST_pp=cost_pp, net10_pp=add_pp + drop_pp + both_pp + cost_pp,
        both_share=(abs(both_pp) / mag) if mag > 1e-15 else 0.0,
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

    P("=" * 185)
    P("Idea 559 what-does-SELECTION-become-under-a-DAILY-depth-match (lane C) | "
      + Path(__file__).name)
    P("=" * 185)
    P("QUESTION: pin k_q to k_ma EVERY DAY instead of on average, and report what idea 305's "
      "SELECTION leg and its panel ordering become.")
    P("PRE-REGISTERED  H_IDENT : the daily-matched quantile gate on the MA gate's OWN ranker "
      "IS the MA gate, set-for-set, every day")
    P("                          -> ADD=DROP=BOTH=SELECTION=0 exactly, and idea 305's "
      "SELECTION is 100% depth mismatch.")
    P("                H_ORDER : on a genuinely different ranker (12-1 momentum) at daily-"
      "matched depth, the panel ordering of SELECTION")
    P("                          survives: SMALL439 > B136 > U56 (idea 305: +1.2436 / -0.4058 "
      "/ -0.5779 pp/yr).")
    P("                H_DRIFT : 'BOTH is zero by construction' is exact only without drift - "
      "BOTH_pp = 0 at cadence D and non-zero")
    P("                          at cadence W, with a W share well below idea 556's mean-"
      "matched 31.5%.")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = sum_i W_i r_i, gated at "
      f"{BAR_R0:.0e}), gross {GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): panel {PANELS} x theta {MA_THETA}.  depth is a deterministic function "
      f"of theta (mean match) or of the day (daily match).")
    P(f"reported contrasts: family {FAM_W} x construction {CONSTRUCTIONS} at cadence W "
      f"({len(PANELS) * len(MA_THETA) * len(FAM_W) * len(CONSTRUCTIONS)} books)")
    P(f"                  + family {FAM_D} RESPREAD at cadence D "
      f"({len(PANELS) * len(MA_THETA) * len(FAM_D)} books).  Every grid point is reported.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels inflated and "
      "the 4a/4b columns NOT immune.")
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
    setdiff_max = 0
    spy_by_panel, live_by_panel, ctrl_by_panel = {}, {}, {}

    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        R = px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        spy_by_panel[pn], live_by_panel[pn] = spy_s, live_s

        rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq="W")
        ctrl = stat(rc["returns"].loc[start:])
        ctrl_by_panel[pn] = ctrl

        P("\n" + "=" * 185)
        P(f"PANEL {pn} - comparands over {start.date()}..{px.index[-1].date()} ({years:.2f} yrs)")
        P("=" * 185)
        P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} "
          f"OOS {spy_s['oSharpe']:.4f} oCAGR {spy_s['oCAGR']:.4f} oMaxDD {spy_s['oMaxDD']:.4f}")
        P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS {live_s['oSharpe']:.4f} oCAGR {live_s['oCAGR']:.4f} oMaxDD {live_s['oMaxDD']:.4f}")
        P(f"CONTROL EWall W (no gate)    : CAGR {ctrl['CAGR']:.4f} Sharpe {ctrl['Sharpe']:.4f} "
          f"MaxDD {ctrl['MaxDD']:.4f}")
        P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70 * spy_s['CAGR']:.2%}")

        live = live_mask(px)
        nlive_w = live.loc[start:].sum(axis=1)
        dist, _ = dist_rank(px)
        mom, _ = mom_rank(px)

        gates = {}
        for th in MA_THETA:
            gm = ma_gate(px, th)
            x = float((gm.loc[start:].sum(axis=1) / nlive_w).mean())
            g_qm = mean_matched(dist, live, x)
            g_qd = daily_matched(dist, live, gm)
            g_mm = mean_matched(mom, live, x)
            g_md = daily_matched(mom, live, gm)
            gates[th] = {"MA-THRESH": gm, "QUANTILE-M": g_qm, "QUANTILE-D": g_qd,
                         "MOM-M": g_mm, "MOM-D": g_md}

            # H_IDENT: set equality of the same-ranker daily match with the MA gate
            sd = int((gm.loc[start:] != g_qd.loc[start:]).sum().sum())
            setdiff_max = max(setdiff_max, sd)
            k_ma = gm.loc[start:].sum(axis=1)
            matchrows.append(dict(
                panel=pn, theta=th, x=x,
                k_ma=float(k_ma.mean()),
                k_qm=float(g_qm.loc[start:].sum(axis=1).mean()),
                k_qd=float(g_qd.loc[start:].sum(axis=1).mean()),
                k_mm=float(g_mm.loc[start:].sum(axis=1).mean()),
                k_md=float(g_md.loc[start:].sum(axis=1).mean()),
                # daily depth error of each match (mean absolute names/day)
                dk_qm=float((g_qm.loc[start:].sum(axis=1) - k_ma).abs().mean()),
                dk_qd=float((g_qd.loc[start:].sum(axis=1) - k_ma).abs().mean()),
                dk_mm=float((g_mm.loc[start:].sum(axis=1) - k_ma).abs().mean()),
                dk_md=float((g_md.loc[start:].sum(axis=1) - k_ma).abs().mean()),
                setdiff_qd=sd,
                mom_rankable=float(mom.loc[start:].notna().sum(axis=1).mean()),
                nlive=float(nlive_w.mean())))

        for th in MA_THETA:
            xth = float([m["x"] for m in matchrows
                         if m["panel"] == pn and m["theta"] == th][0])
            for cad, fams, cons, controls in (("W", FAM_W, CONSTRUCTIONS, CONTROLS_W),
                                              ("D", FAM_D, ["RESPREAD"], CONTROLS_D)):
                arms = {}
                for fam in fams:
                    for con in cons:
                        res = backtest(px, book(px, gates[th][fam], con),
                                       cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        W = res["weights"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        r0_gate_max = max(r0_gate_max,
                                          float(((W * R).sum(axis=1) - r0).abs().max()))
                        s = stat(r10)
                        arms[(fam, con)] = dict(W=W, turn=turn, s=s, r0=r0)
                        rows.append(dict(panel=pn, theta=th, x=xth, cad=cad, family=fam,
                                         con=con, **s, CAGR0=cagr(r0),
                                         turn_yr=float(turn.sum() / years),
                                         dCAGR_ctrl=s["CAGR"] - ctrl["CAGR"],
                                         dSharpe_ctrl=s["Sharpe"] - ctrl["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))

                ma_rs = arms[("MA-THRESH", "RESPREAD")]
                for qfam in controls:
                    q_rs = arms[(qfam, "RESPREAD")]
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        d = legs(ma_rs["W"], q_rs["W"], R, ma_rs["turn"], q_rs["turn"],
                                 lo, hi, tag, years)
                        legrows.append(dict(panel=pn, theta=th, x=xth, cad=cad,
                                            qfam=qfam, **d))
                    for con in cons:
                        a, b = arms[("MA-THRESH", con)]["s"], arms[(qfam, con)]["s"]
                        pairs.append(dict(panel=pn, theta=th, x=xth, cad=cad, con=con,
                                          qfam=qfam,
                                          Sharpe_ma=a["Sharpe"], Sharpe_q=b["Sharpe"],
                                          dSharpe=a["Sharpe"] - b["Sharpe"],
                                          dSharpe_oos=a["oSharpe"] - b["oSharpe"],
                                          dCAGR_pp=100 * (a["CAGR"] - b["CAGR"]),
                                          dMaxDD_pp=100 * (a["MaxDD"] - b["MaxDD"])))
            P(f"  {pn}: theta {th:+.2f} (x={xth:.4f}) done")
            flush_log()

    G, L = pd.DataFrame(rows), pd.DataFrame(legrows)
    PR, M = pd.DataFrame(pairs), pd.DataFrame(matchrows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L.to_csv(f"{OUT}.legs.csv", index=False)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)
    M.to_csv(f"{OUT}.match.csv", index=False)

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

    if IDEA556.exists():
        old = pd.read_csv(IDEA556)
        old = old[old.qfam == "QUANTILE-M"]
        mine = L[(L.cad == "W") & (L.qfam == "QUANTILE-M")]
        m1 = mine.merge(old, on=["panel", "theta", "qfam", "window"], suffixes=("", "_556"))
        cols = ["ADD_pp", "DROP_pp", "BOTH_pp", "sel_geo_pp"]
        worst = max(float((m1[c] - m1[f"{c}_556"]).abs().max()) for c in cols)
        P(f"R1 idea-556 legs.csv   : {len(m1)} rows x {len(cols)} columns, worst |d| = "
          f"{worst:.3e} (bar {R_TOL:.0e})  {'PASS' if worst < R_TOL else 'FAIL'}")
    else:
        P("R1 idea-556 legs.csv   : NOT FOUND")

    if IDEA305.exists():
        o305 = pd.read_csv(IDEA305)
        o305 = o305[(o305.cad == "W") & (o305.qfam == "QUANTILE-M")]
        m2 = PR[(PR.cad == "W") & (PR.qfam == "QUANTILE-M")].merge(
            o305, on=["panel", "theta", "con", "qfam"], suffixes=("", "_305"))
        cols = ["dSharpe", "dSharpe_oos", "dCAGR_pp", "dMaxDD_pp"]
        worst2 = max(float((m2[c] - m2[f"{c}_305"]).abs().max()) for c in cols)
        P(f"R2 idea-305 pairs.csv  : {len(m2)} cadence-W rows x {len(cols)} columns, worst |d| "
          f"= {worst2:.3e} (bar {R_TOL:.0e})  {'PASS' if worst2 < R_TOL else 'FAIL'}")
    else:
        P("R2 idea-305 pairs.csv  : NOT FOUND")

    # ------------------------------------------------------------ H_IDENT
    P("\n" + "=" * 185)
    P("H_IDENT.  Is the daily-matched quantile gate on the MA gate's OWN ranker (dist = "
      "px/MA200 - 1) the SAME SET as the MA gate?")
    P("=" * 185)
    QD = L[(L.qfam == "QUANTILE-D") & (L.cad == "W")]
    QDD = L[(L.qfam == "QUANTILE-D") & (L.cad == "D")]
    worst_sel = float(pd.concat([QD.sel_geo_pp, QDD.sel_geo_pp]).abs().max())
    worst_leg = float(pd.concat([QD.ADD_pp.abs(), QD.DROP_pp.abs(), QD.BOTH_pp.abs(),
                                 QDD.ADD_pp.abs(), QDD.DROP_pp.abs(),
                                 QDD.BOTH_pp.abs()]).max())
    P(f"  max daily set disagreement over {len(M)} (panel, theta) cells x all bars : "
      f"{setdiff_max} cells")
    P(f"  max |SELECTION| over the {len(QD) + len(QDD)} QUANTILE-D leg rows (W and D)  : "
      f"{worst_sel:.3e} pp/yr  (bar {BAR_ZERO:.0e})")
    P(f"  max |ADD|,|DROP|,|BOTH| over the same rows                        : "
      f"{worst_leg:.3e} pp/yr")
    ver_ident = "HOLDS" if (setdiff_max == 0 and worst_sel < BAR_ZERO
                            and worst_leg < BAR_ZERO) else "FAILS"
    P(f"  H_IDENT: {ver_ident}")
    if ver_ident == "HOLDS":
        P("  READING: closing the mismatch channel on idea 305's own ranker does not shrink "
          "SELECTION, it ANNIHILATES the contrast.")
        P("           Idea 305's SELECTION leg (+1.2436 / -0.4058 / -0.5779) and idea 556's "
          "ADD/DROP/BOTH split of it are 100%")
        P("           depth-timing statistics: the MA gate and the quantile gate hold the SAME "
          "NAMES at equal daily depth, and differ")
        P("           only in HOW MANY they hold on a given day.  There is no 'which names' "
          "content in the contrast at all.")

    # ------------------------------------------------------------ the match quality
    P("\n" + "=" * 185)
    P("THE MATCH ACTUALLY ACHIEVED.  k_* = mean names/day; dk_* = MEAN ABSOLUTE daily depth "
      "error against k_ma (names/day).")
    P("=" * 185)
    P(fmt(M.reset_index(drop=True)))
    P("\n  mean daily depth error by match, pooled over 27 cells (names/day):")
    P(f"    MEAN-matched  QUANTILE-M {M.dk_qm.mean():7.3f}   MOM-M {M.dk_mm.mean():7.3f}")
    P(f"    DAILY-matched QUANTILE-D {M.dk_qd.mean():7.3f}   MOM-D {M.dk_md.mean():7.3f}"
      f"   (non-zero only where the 12-1 ranker has fewer rankable names than k_ma)")

    # ------------------------------------------------------------ the non-degenerate SELECTION
    P("\n" + "=" * 185)
    P("WHAT SELECTION BECOMES ON A REAL RANKER.  MA-THRESH vs 12-1 MOMENTUM at MEAN-matched "
      "depth (MOM-M, idea 305's match) and at")
    P("DAILY-matched depth (MOM-D, the queue's match).  All pp/yr, zero cost, RESPREAD, "
      "cadence W, FULL sample.")
    P("=" * 185)
    show = ["panel", "theta", "x", "qfam", "ADD_pp", "DROP_pp", "BOTH_pp", "arith_pp",
            "jensen_pp", "sel_geo_pp", "both_share", "COST_pp", "net10_pp", "n_add", "n_drop",
            "n_both", "overlap", "rbar_add", "rbar_drop", "dom"]
    FW = L[(L.window == "FULL") & (L.cad == "W")]
    P(fmt(FW[FW.qfam.isin(["MOM-M", "MOM-D"])][show].sort_values(
        ["panel", "qfam", "theta"]).reset_index(drop=True)))

    P("\nPANEL MEANS of the SELECTION leg over the 9 thetas (FULL sample, RESPREAD):")
    tab = []
    for cad in ("W", "D"):
        sub = L[(L.window == "FULL") & (L.cad == cad)]
        for qf in sorted(sub.qfam.unique()):
            s2 = sub[sub.qfam == qf]
            row = dict(cad=cad, qfam=qf)
            have = [p for p in PANELS if (s2.panel == p).any()]
            for pn in have:
                row[pn] = float(s2[s2.panel == pn].sel_geo_pp.mean())
            if "SMALL439" in row and "U56" in row:
                row["S-U"] = row["SMALL439"] - row["U56"]
            row["order"] = " > ".join(sorted(have, key=lambda p: -row[p]))
            tab.append(row)
    T = pd.DataFrame(tab)
    P(fmt(T))
    P(f"\n  idea 305's published SELECTION panel means (pooled over 3 cadences x 2 qfams): "
      + "  ".join(f"{k} {v:+.4f}" for k, v in SEL305.items())
      + f"   order {' > '.join(sorted(SEL305, key=lambda p: -SEL305[p]))}")

    # H_ORDER
    P("\n" + "=" * 185)
    P("H_ORDER: does the panel ordering SMALL439 > B136 > U56 survive on MOM-D (daily-matched, "
      "real ranker)?")
    P("=" * 185)
    ref_order = sorted(SEL305, key=lambda p: -SEL305[p])
    ver_order = {}
    for cad in ("W", "D"):
        for qf in ("MOM-M", "MOM-D"):
            r = T[(T.cad == cad) & (T.qfam == qf)]
            if not len(r):
                continue
            r = r.iloc[0]
            got = r["order"].split(" > ")
            ok = got == ref_order
            ver_order[(cad, qf)] = ok
            P(f"  cad {cad} {qf:11s}: "
              + "  ".join(f"{pn} {r[pn]:+.4f}" for pn in PANELS if pn in r.index)
              + f"   order {r['order']}   matches idea 305 {'YES' if ok else 'NO'}")
    md_key = ("W", "MOM-D")
    ver_ord = "HOLDS" if ver_order.get(md_key) else "FAILS"
    P(f"  H_ORDER (the pre-registered cell, cadence W MOM-D): {ver_ord}")

    P("\n  per-theta SELECTION sign, MOM-D cadence W (is the panel ordering even stable "
      "within a panel?):")
    for pn in PANELS:
        sub = FW[(FW.qfam == "MOM-D") & (FW.panel == pn)].sort_values("theta")
        P(f"    {pn:9s} " + " ".join(f"{t:+.2f}:{v:+7.3f}"
                                     for t, v in zip(sub.theta, sub.sel_geo_pp))
          + f"   | positive {int((sub.sel_geo_pp > 0).sum())}/9"
          + f"   | dominant side ADD {int((sub.dom == 'ADD').sum())}/9")

    # ------------------------------------------------------------ H_DRIFT
    P("\n" + "=" * 185)
    P("H_DRIFT: is 'BOTH = 0 by construction' true?  BOTH is the shared names' WEIGHT gap; a "
      "daily depth match equalises the TARGETS,")
    P("but the engine re-normalises drifted weights daily, so two arms drift apart between "
      "weekly rebalances.")
    P("=" * 185)
    for cad in ("W", "D"):
        sub = L[(L.window == "FULL") & (L.cad == cad)]
        for qf in sorted(sub.qfam.unique()):
            s2 = sub[sub.qfam == qf]
            P(f"  cad {cad} {qf:11s}: mean |BOTH| {s2.BOTH_pp.abs().mean():8.4f} pp/yr | "
              f"max |BOTH| {s2.BOTH_pp.abs().max():8.4f} | mean BOTH share of |ADD|+|DROP|+"
              f"|BOTH| {s2.both_share.mean():6.1%} | cells |BOTH| > |SEL| "
              f"{int((s2.BOTH_pp.abs() > s2.sel_geo_pp.abs()).sum())}/{len(s2)}")
    bw = L[(L.window == "FULL") & (L.cad == "W") & (L.qfam == "MOM-D")]
    bd = L[(L.window == "FULL") & (L.cad == "D") & (L.qfam == "MOM-D")]
    ver_drift = "HOLDS" if (float(bd.BOTH_pp.abs().max()) < BAR_ZERO
                            and float(bw.BOTH_pp.abs().max()) > BAR_ZERO
                            and float(bw.both_share.mean()) < 0.315) else "FAILS"
    P(f"  MOM-D: max |BOTH| at cadence D = {float(bd.BOTH_pp.abs().max()):.3e} pp/yr, at "
      f"cadence W = {float(bw.BOTH_pp.abs().max()):.4f} pp/yr, W share "
      f"{float(bw.both_share.mean()):.1%} vs idea 556's mean-matched 31.5%")
    P(f"  H_DRIFT: {ver_drift}")

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 185)
    P(f"RULE 8 WALK-FORWARD.  IS = start..{IS_END} (choice), OOS = {OOS_START}..end (read once)")
    P("=" * 185)
    wf = []

    P("\nWF-A  the sign claim: SELECTION sign and dominant side chosen on IS, checked OOS "
      "(9 thetas per cell)")
    for cad in ("W", "D"):
        for pn in PANELS:
            for qf in sorted(L[L.cad == cad].qfam.unique()):
                a = L[(L.cad == cad) & (L.panel == pn) & (L.qfam == qf) &
                      (L.window == "IS")].set_index("theta")
                o = L[(L.cad == cad) & (L.panel == pn) & (L.qfam == qf) &
                      (L.window == "OOS")].set_index("theta")
                if not len(a):
                    continue
                dom_hold = int((a.dom == o.dom).sum())
                sgn_hold = int((np.sign(a.sel_geo_pp) == np.sign(o.sel_geo_pp)).sum())
                P(f"  cad {cad} {pn:9s} {qf:11s}: dominant side holds {dom_hold}/9, SELECTION "
                  f"sign holds {sgn_hold}/9 | IS SEL {a.sel_geo_pp.mean():+8.4f} -> OOS "
                  f"{o.sel_geo_pp.mean():+8.4f}")
                wf.append(dict(test="WF-A", cad=cad, panel=pn, qfam=qf, dom_hold=dom_hold,
                               sign_hold=sgn_hold, n=9, IS_SEL=a.sel_geo_pp.mean(),
                               OOS_SEL=o.sel_geo_pp.mean(),
                               IS_ADD=a.ADD_pp.mean(), OOS_ADD=o.ADD_pp.mean(),
                               IS_DROP=a.DROP_pp.mean(), OOS_DROP=o.DROP_pp.mean()))

    P("\nWF-B  book pick: per (panel, cadence, family, construction) take the theta with the "
      "best IS Sharpe, then read OOS once")
    for pn in PANELS:
        sp, lv = spy_by_panel[pn], live_by_panel[pn]
        for cad in ("W", "D"):
            for fam in sorted(G[G.cad == cad].family.unique()):
                for con in sorted(G[(G.cad == cad) & (G.family == fam)].con.unique()):
                    sub = G[(G.panel == pn) & (G.cad == cad) & (G.family == fam) &
                            (G.con == con)]
                    if not len(sub):
                        continue
                    pick = sub.loc[sub.isSharpe.idxmax()]
                    P(f"  {pn:9s} cad {cad} {fam:11s} {con:8s}: IS pick theta "
                      f"{pick.theta:+.2f} (IS Sharpe {pick.isSharpe:.4f}) -> OOS CAGR "
                      f"{pick.oCAGR:.4f} Sharpe {pick.oSharpe:.4f} MaxDD {pick.oMaxDD:.4f} | "
                      f"RULES v2 OOS {lv['oCAGR']:.4f}/{lv['oSharpe']:.4f}/{lv['oMaxDD']:.4f} "
                      f"| SPY OOS {sp['oCAGR']:.4f}/{sp['oSharpe']:.4f}/{sp['oMaxDD']:.4f} | "
                      f"beats v2 {'Y' if pick.oSharpe > lv['oSharpe'] else 'N'} beats SPY "
                      f"{'Y' if pick.oSharpe > sp['oSharpe'] else 'N'}")
                    wf.append(dict(test="WF-B", panel=pn, cad=cad, family=fam, con=con,
                                   theta=pick.theta, isSharpe=pick.isSharpe,
                                   oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                                   oMaxDD=pick.oMaxDD, v2_oSharpe=lv["oSharpe"],
                                   spy_oSharpe=sp["oSharpe"],
                                   beats_v2=bool(pick.oSharpe > lv["oSharpe"]),
                                   beats_spy=bool(pick.oSharpe > sp["oSharpe"])))
    nb = [w for w in wf if w["test"] == "WF-B"]
    P(f"  WF-B totals: beats RULES v2 OOS {sum(w['beats_v2'] for w in nb)}/{len(nb)}, "
      f"beats SPY OOS {sum(w['beats_spy'] for w in nb)}/{len(nb)}")

    P("\nWF-C  the depth-vs-panel model on the NON-DEGENERATE SELECTION (MOM-D, cadence W): "
      "fit sel ~ 1+x+x^2 (DEPTH) and a panel-mean")
    P("      model (PANEL) on IS, score both on OOS")
    LI = L[(L.window == "IS") & (L.cad == "W") & (L.qfam == "MOM-D")]
    LO = L[(L.window == "OOS") & (L.cad == "W") & (L.qfam == "MOM-D")].reset_index(drop=True)
    Xi = np.column_stack([np.ones(len(LI)), LI.x.values, LI.x.values ** 2])
    bi, *_ = np.linalg.lstsq(Xi, LI.sel_geo_pp.values, rcond=None)
    Xo = np.column_stack([np.ones(len(LO)), LO.x.values, LO.x.values ** 2])
    pred_depth = Xo @ bi
    pm = LI.groupby("panel").sel_geo_pp.mean()
    pred_panel = LO.panel.map(pm).values
    yo = LO.sel_geo_pp.values
    mae = lambda p: float(np.abs(yo - p).mean())
    P(f"  OOS MAE  DEPTH {mae(pred_depth):.4f} | PANEL {mae(pred_panel):.4f} | zero "
      f"{mae(np.zeros_like(yo)):.4f} | pooled IS mean "
      f"{mae(np.full_like(yo, LI.sel_geo_pp.mean())):.4f}  (pp/yr, n={len(yo)})")
    P(f"  OOS sign agreement  DEPTH {int((np.sign(pred_depth) == np.sign(yo)).sum())}/{len(yo)}"
      f" | PANEL {int((np.sign(pred_panel) == np.sign(yo)).sum())}/{len(yo)}")
    wf.append(dict(test="WF-C", qfam="MOM-D", cad="W", mae_depth=mae(pred_depth),
                   mae_panel=mae(pred_panel), mae_zero=mae(np.zeros_like(yo)), n=len(yo),
                   sign_depth=int((np.sign(pred_depth) == np.sign(yo)).sum()),
                   sign_panel=int((np.sign(pred_panel) == np.sign(yo)).sum())))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 185)
    P("BOTH KEEP PATHS over every book (4a vs the live RULES v2 book; 4b vs SPY, 10 bps, "
      "full sample)")
    P("=" * 185)
    K = G.copy()
    P(f"  4a passers: {int(K.p4a.sum())}/{len(K)}   4b passers: {int(K.p4b.sum())}/{len(K)}   "
      f"BOTH: {int((K.p4a & K.p4b).sum())}/{len(K)}")
    fails = {}
    for s in K.loc[~K.p4b, "f4b"]:
        for tok in s.split(","):
            fails[tok] = fails.get(tok, 0) + 1
    P("  4b failing legs: " + ", ".join(f"{k} {v}" for k, v in
                                        sorted(fails.items(), key=lambda kv: -kv[1])))
    P("\n  pass counts by family x cadence:")
    P(fmt(K.groupby(["cad", "family"]).agg(n=("p4a", "size"), pass4a=("p4a", "sum"),
                                           pass4b=("p4b", "sum"))))
    if K.p4a.any():
        P("\n  4a passers:")
        P(fmt(K[K.p4a][["panel", "theta", "x", "cad", "family", "con", "CAGR", "Sharpe",
                        "MaxDD", "H1", "H2", "oSharpe", "f4b"]].reset_index(drop=True)))
    if K.p4b.any():
        P("\n  4b passers:")
        P(fmt(K[K.p4b][["panel", "theta", "x", "cad", "family", "con", "CAGR", "Sharpe",
                        "MaxDD", "H1", "H2", "oSharpe", "p4a"]].reset_index(drop=True)))
    K[["panel", "theta", "x", "cad", "family", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
       "oSharpe", "oCAGR", "oMaxDD", "p4a", "p4b", "f4b"]].to_csv(
        f"{OUT}.keeppaths.csv", index=False)

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 185)
    P("VERDICT")
    P("=" * 185)
    P(f"  H_IDENT : {ver_ident}")
    P(f"  H_ORDER : {ver_ord}")
    P(f"  H_DRIFT : {ver_drift}")
    P(f"  KEEP    : 4a {int(K.p4a.sum())}/{len(K)}, 4b {int(K.p4b.sum())}/{len(K)}, "
      f"BOTH {int((K.p4a & K.p4b).sum())}/{len(K)}")
    flush_log()


if __name__ == "__main__":
    main()
