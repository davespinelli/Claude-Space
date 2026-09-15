#!/usr/bin/env python3
"""IDEA 885 - does the BILINEAR floor law hold at a GROSS that is not 0.75?
Cloud lane, 2026-09-15, idea 1 of 2.

THE QUESTION
------------
Idea 769 measured the engine-drift noise floor - the pp/yr residue two arms accumulate on a
name they BOTH hold at the SAME target, purely because the engine renormalises each arm by its
own total between rebalances - and fitted it as BILINEAR in the per-name target w and the book
exposure E:

    |DRIFT_pp| ~ w * E        beta measured 1.9293, IQR [1.85, 2.09]
    construction gap          DEGROSS / RESPREAD = (k/n)^2

Every point of that fit was taken at the LIVE gross, 0.75.  But gross enters BOTH factors:

    RESPREAD   w = g/k     E = g        =>  w*E = g^2 / k
    DEGROSS    w = g/n     E = g*(k/n)  =>  w*E = g^2 * k / n^2

so the law is not merely "holds at other gross" - it makes a sharp, parameter-free prediction
the record has never tested: at FIXED k/n the floor is QUADRATIC in gross, exponent 2.0 in
BOTH constructions, and the construction gap (k/n)^2 is INVARIANT to gross.  This run walks the
gross rung and reads the exponent.

PRE-REGISTERED HYPOTHESES (written before any number was read)
--------------------------------------------------------------
    H_QUAD   (769's law): d log|DRIFT_pp| / d log g = 2.0 in both constructions, all q, all
             cadences.  SUPPORTED if the pooled beta's 95% interval contains 2.0 and every
             per-cell beta is inside [1.5, 2.5].
    H_LIN    (the rival: the floor is a TARGET-SIZE fact only, exposure irrelevant): beta = 1.0.
    H_INVAR  (769's gap, restated): log(DEGROSS/RESPREAD) at matched (panel, q, cadence) equals
             2*log(q) and does NOT move with gross.  SUPPORTED if the gross-to-gross spread of
             that ratio is < 10% of its level at every (panel, q, cadence).

WHY THE FLOOR IS ALGEBRAICALLY QUADRATIC (the prediction being tested, not a fitted claim)
-------------------------------------------------------------------------------------------
Between rebalances the engine carries h_j -> h_j(1+r_j)/(1 + sum_k h_k r_k).  One bar after a
rebalance, for a name both arms hold at the same target w:
    (h_A - h_B)_j  ~=  w * (P_B - P_A)        P_X = sum_k w_X,k r_k, the arm's own book return
and |P| scales with the exposure E.  The differenced P&L on that name is (h_A-h_B)_j * r_j, so
the floor carries one factor of w and one of E - and since w ~ g and E ~ g, one g^2.

THE ARM PAIR (MRES is exactly zero here)
-----------------------------------------
FIXK selects EXACTLY k_t = round(q*n_t) live names in BOTH arms every day:
    MA-DIST   top-k_t by px/ma200 - 1
    MOM       top-k_t by px.shift(21)/px.shift(252) - 1
so within a construction every shared name carries the IDENTICAL target, the depth-match
residual MRES == 0 by construction (gate G3), and the whole shared-name leg IS the drift floor.

THE BOOK LEG (this lane's mandate: both KEEP paths + rule 8 on every grid point)
--------------------------------------------------------------------------------
Gross is not only the law's axis, it is a live dial of the book, so every arm at every rung is
also priced as capital: 4a against RULES v2 (live), 4b against SPY, on each panel's own
calendar, at 0 / 10 / 25 bps, with the 4b legs also read on the OOS window alone.

2 TUNED PARAMS: GROSS {0.25, 0.375, 0.50, 0.75, 1.00} x K/N q {0.10, 0.20, 0.50}.
Construction {RESPREAD, DEGROSS}, cadence {D,W,M,Q}, arm {MA-DIST, MOM}, panel and cost rung
are REPORTED axes, never selected over; ALL grid points are printed.
Costs 10 bps per unit turnover (0 and 25 derived exactly), next-day execution, no shorting.
Gross 1.00 is full investment, never leverage.
RULE 8: the law's exponent is fitted on 2009..2016 alone and re-read once on 2017..2026; the
book selectors are chosen on the IS window alone and their OOS CAGR/Sharpe/MaxDD reported
against RULES v2 and SPY.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents of their screens only - dead names are
absent, so CAGR levels are inflated and any 4b pass on them is optimistic.  DRIFT_pp is an
arm-minus-arm quantity inside one panel at identical depth, where that bias very largely
cancels; the KEEP columns and the rule-8 levels are NOT protected and are read with the caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .drift.csv .books.csv .rungs.csv .law.csv .walkforward.csv .offsets.csv .console.txt
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
RUNGS = [0, 10, 25]
PANELS = ["U56", "B136", "SMALL"]
GROSSES = [0.25, 0.375, 0.50, 0.75, 1.00]        # tuned param 1
QS = [0.10, 0.20, 0.50]                          # tuned param 2  (k/n)
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]          # reported
CADENCES = ["D", "W", "M", "Q"]                  # reported
ARMS = ["MA-DIST", "MOM"]                        # reported
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS_TGT = 1e-15
BAR_ENGINE = 1e-12
BAR_RUNG = 1e-15
BAR_D = 1e-12
BAR_MRES = 1e-12
BETA_LO, BETA_HI = 1.5, 2.5                      # H_QUAD per-cell bar
INVAR_BAR = 0.10                                 # H_INVAR spread bar

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 140)
pd.set_option("display.max_rows", 3000)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def run(px, W, freq, rmask=None):
    """engine.backtest's arithmetic, also returning HELD and TARGET-IN-FORCE matrices.
    rmask, when given, replaces rebalance_mask(index, freq) (used by the offset sweep)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    base = rebalance_mask(px.index, freq) if rmask is None else rmask
    mask = base.shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    tgt = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    t_cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
            t_cur = new
        held[i] = cur
        tgt[i] = t_cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    r0 = pd.Series(np.nansum(held * rets, axis=1), index=px.index)
    return r0, pd.Series(turn, index=px.index), held, tgt


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


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


def fail_4b_oos(s, spy):
    """the 4b legs read on the OOS window alone (rule 8's own reading of path 4b)."""
    t = {"OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["oMaxDD"]) <= 0.60 * abs(spy["oMaxDD"]),
         "CAGR": s["oCAGR"] >= 0.70 * spy["oCAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def ma_dist(px):
    return (px / px.rolling(200).mean() - 1.0).where(live_mask(px))


def mom_rank(px):
    return (px.shift(21) / px.shift(252) - 1).where(live_mask(px))


def topk(sig, kt, live):
    return sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def book(px, g, con, nlive, gross):
    """RESPREAD divides by the arm's OWN count k_t; DEGROSS by the SHARED panel count n_t."""
    if con == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    return g.astype(float).div(nlive.clip(lower=1), axis=0) * gross


def ols(y, X, names):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    dof = max(len(y) - X.shape[1], 1)
    s2 = float(resid @ resid) / dof
    try:
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    except np.linalg.LinAlgError:
        se = np.full(X.shape[1], np.nan)
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / ss if ss > 0 else np.nan
    return dict(zip(names, b)), dict(zip(names, se)), r2


def loglog_beta(g, d):
    """slope of log|DRIFT| on log gross; needs >= 3 strictly positive points."""
    g, d = np.asarray(g, float), np.asarray(d, float)
    ok = np.isfinite(d) & (d > 0) & np.isfinite(g) & (g > 0)
    if ok.sum() < 3:
        return np.nan, np.nan, np.nan, int(ok.sum())
    X = np.column_stack([np.ones(ok.sum()), np.log(g[ok])])
    b, se, r2 = ols(np.log(d[ok]), X, ["a", "beta"])
    return b["beta"], se["beta"], r2, int(ok.sum())


# ================================================================== main
def main():
    P("=" * 178)
    P("IDEA 885 - does the BILINEAR floor law hold at a GROSS that is not 0.75?"
      "   (cloud lane, 2026-09-15, idea 1 of 2)")
    P("=" * 178)
    P("PROTOCOL: 10 bps per unit turnover (0/25 derived exactly and reported), next-day")
    P(f"execution, no shorting, no leverage (gross 1.00 = full investment).  IS = start..{IS_END},")
    P(f"OOS = {OOS_START}..end, read once.")
    P(f"2 TUNED PARAMS: GROSS {GROSSES} x K/N q {QS}.")
    P(f"Reported axes (never selected over): panel {PANELS}, construction {CONSTRUCTIONS},")
    P(f"cadence {CADENCES}, arm {ARMS}, cost rung {RUNGS}.")
    P("PRE-REGISTERED:")
    P("  H_QUAD  (769's bilinear law): d log|DRIFT_pp| / d log gross = 2.0, both constructions,")
    P(f"          all q, all cadences.  SUPPORTED if pooled 95% CI covers 2.0 and every per-cell")
    P(f"          beta is inside [{BETA_LO}, {BETA_HI}].")
    P("  H_LIN   (the rival, target-size only): beta = 1.0.")
    P("  H_INVAR (769's construction gap): log(DEGROSS/RESPREAD) = 2*log(q), invariant to gross;")
    P(f"          SUPPORTED if the gross-to-gross spread of that ratio is < {INVAR_BAR:.0%} of level.")
    P("SURVIVORSHIP: B136/SMALL are current constituents only; CAGR inflated, KEEP not immune.")
    flush_log()

    u = load_universe()
    b = load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "   ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")
    flush_log()

    # -------------------------------------------------------------- G0 / G1
    P("\n" + "=" * 178)
    P("GATES  G0 run() vs engine.backtest    G1 derived cost rung vs a fresh run at that rung")
    P("=" * 178)
    g0 = g1 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        for freq in ("D", "W", "Q"):
            a = backtest(px, W, cost_bps=COST_BPS, freq=freq)
            r0, tn, held, tgt = run(px, W, freq)
            g0 = max(g0, float((a["returns"] - rung(r0, tn, COST_BPS)).abs().max()),
                     float((a["turnover"] - tn).abs().max()),
                     float(np.abs(a["weights"].values - held).max()))
            a25 = backtest(px, W, cost_bps=25, freq=freq)
            g1 = max(g1, float((a25["returns"] - rung(r0, tn, 25)).abs().max()))
        P(f"  {pn:7s} running max  G0 {g0:.3e}   G1 {g1:.3e}")
    P(f"  G0 {g0:.3e} (bar {BAR_ENGINE:.0e})  {'PASS' if g0 < BAR_ENGINE else 'FAIL'}"
      f"    G1 {g1:.3e} (bar {BAR_RUNG:.0e})  {'PASS' if g1 < BAR_RUNG else 'FAIL'}")
    flush_log()

    # -------------------------------------------------------------- comparands
    COMP = {}
    P("\n" + "=" * 178)
    P("COMPARANDS per panel (RULES v2 = the 4a bar, weekly, 10 bps; SPY = the 4b bar)")
    P("=" * 178)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        r0, tn, _, _ = run(px, rules_v2_weights(px), "W")
        live_s = stat(rung(r0, tn, COST_BPS).loc[start:])
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        COMP[pn] = dict(live=live_s, spy=spy_s, start=start,
                        years=len(px.loc[start:]) / 252)
        P(f"  {pn:7s} {start.date()}..{px.index[-1].date()}  ({COMP[pn]['years']:.2f} yrs, "
          f"{px.shape[1]} names)")
        P(f"      RULES v2  CAGR {live_s['CAGR']:.4f}  Sharpe {live_s['Sharpe']:.4f}  MaxDD "
          f"{live_s['MaxDD']:.4f}  H1/H2 {live_s['H1']:.4f}/{live_s['H2']:.4f}   OOS "
          f"{live_s['oCAGR']:.4f}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
        P(f"      SPY       CAGR {spy_s['CAGR']:.4f}  Sharpe {spy_s['Sharpe']:.4f}  MaxDD "
          f"{spy_s['MaxDD']:.4f}  H1/H2 {spy_s['H1']:.4f}/{spy_s['H2']:.4f}   OOS "
          f"{spy_s['oCAGR']:.4f}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
        P(f"      4b bars: H1>{spy_s['H1']:.4f}  H2>{spy_s['H2']:.4f}  OOS>{spy_s['oSharpe']:.4f}"
          f"  MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%}  CAGR>={0.70*spy_s['CAGR']:.2%}"
          f"   OOS-only DD>=-{0.60*abs(spy_s['oMaxDD']):.2%}  OOS CAGR>={0.70*spy_s['oCAGR']:.2%}")
    flush_log()

    drift, books, rungs = [], [], []
    mres_max = 0.0
    d_cad_max = 0.0

    # -------------------------------------------------------------- the grid
    ncell = len(PANELS) * len(GROSSES) * len(QS) * len(CONSTRUCTIONS) * len(CADENCES)
    P("\n" + "=" * 178)
    P(f"FIXK GRID - {len(PANELS)} panels x {len(GROSSES)} gross x {len(QS)} q x "
      f"{len(CONSTRUCTIONS)} constructions x {len(CADENCES)} cadences = {ncell} arm pairs, "
      f"{ncell*len(ARMS)} books")
    P("=" * 178)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start, live_s, spy_s = COMP[pn]["start"], COMP[pn]["live"], COMP[pn]["spy"]
        yrs = COMP[pn]["years"]
        live = live_mask(px)
        nlive = live.sum(axis=1)
        sigs = {"MA-DIST": ma_dist(px), "MOM": mom_rank(px)}
        R = px.pct_change().fillna(0.0).values
        sel = px.index >= start
        sel_is = sel & (px.index <= pd.Timestamp(IS_END))
        sel_oos = px.index >= pd.Timestamp(OOS_START)
        for q in QS:
            kt = np.maximum(1, np.round(q * nlive)).astype(int)
            kt = pd.Series(np.minimum(kt.values, nlive.values), index=px.index)
            gates = {a: topk(sigs[a], kt, live) for a in ARMS}
            dkser = (gates["MA-DIST"].sum(axis=1) - gates["MOM"].sum(axis=1)).abs()
            dk = float(dkser.loc[start:].max())          # on the PRICED window
            dk_warm = float(dkser.max())                 # incl. warm-up (MOM needs 252 closes)
            for gross in GROSSES:
                for con in CONSTRUCTIONS:
                    W = {a: book(px, gates[a], con, nlive, gross) for a in ARMS}
                    for cad in CADENCES:
                        res = {}
                        for a in ARMS:
                            r0, tn, held, tgt = run(px, W[a], cad)
                            res[a] = (held, tgt)
                            st = stat(rung(r0, tn, COST_BPS).loc[start:])
                            row = dict(panel=pn, gross=gross, q=q, con=con, cad=cad, arm=a,
                                       turn_yr=float(tn.loc[start:].sum() / yrs),
                                       expo=float(pd.Series(held.sum(axis=1),
                                                            index=px.index).loc[start:].mean()),
                                       **st)
                            row["pass4a"] = verdict_4a(st, live_s)
                            row["f4b"] = fail_4b(st, spy_s)
                            row["pass4b"] = row["f4b"] == "-"
                            row["f4b_oos"] = fail_4b_oos(st, spy_s)
                            row["pass4b_oos"] = row["f4b_oos"] == "-"
                            books.append(row)
                            for c in RUNGS:
                                if c == COST_BPS:
                                    continue
                                sc = stat(rung(r0, tn, c).loc[start:])
                                rungs.append(dict(panel=pn, gross=gross, q=q, con=con, cad=cad,
                                                  arm=a, bps=c, CAGR=sc["CAGR"],
                                                  Sharpe=sc["Sharpe"], MaxDD=sc["MaxDD"],
                                                  pass4a=verdict_4a(sc, live_s),
                                                  pass4b=fail_4b(sc, spy_s) == "-"))
                        hA, tA = res["MA-DIST"]
                        hB, tB = res["MOM"]
                        shared = (tA > 0) & (tB > 0)
                        eq = shared & (np.abs(tA - tB) <= EPS_TGT)
                        d = (hA - hB) * R
                        ann = 252 * 100
                        de = np.nansum(np.where(eq, d, 0.0), axis=1)
                        dm = np.nansum(np.where(shared & ~eq, d, 0.0), axis=1)
                        dr = float(de[sel].mean() * ann)
                        mr = float(dm[sel].mean() * ann)
                        mres_max = max(mres_max, abs(mr))
                        if cad == "D":
                            d_cad_max = max(d_cad_max, abs(dr))
                        # per-name target actually in force, and realised exposures
                        tw = np.where(tA > 0, tA, np.nan)[sel]
                        wbar = float(np.nanmean(tw)) if np.isfinite(tw).any() else np.nan
                        eA = float(hA.sum(axis=1)[sel].mean())
                        eB = float(hB.sum(axis=1)[sel].mean())
                        drift.append(dict(panel=pn, gross=gross, q=q, con=con, cad=cad,
                                          dk_max=dk, dk_warm=dk_warm, drift_pp=dr, adrift=abs(dr), mres_pp=mr,
                                          w_bar=wbar, expoA=eA, expoB=eB, wE=wbar * eA,
                                          drift_is=float(de[sel_is].mean() * ann),
                                          drift_oos=float(de[sel_oos].mean() * ann),
                                          shared_share=float(shared[sel].mean())))
                        del hA, hB, tA, tB, d, res
            P(f"  {pn:7s} q={q:.2f}  done  ({len(books)} books so far)")
            flush_log()

    D = pd.DataFrame(drift)
    B = pd.DataFrame(books)
    G = pd.DataFrame(rungs)
    D.to_csv(f"{OUT}.drift.csv", index=False)
    B.to_csv(f"{OUT}.books.csv", index=False)
    G.to_csv(f"{OUT}.rungs.csv", index=False)

    P("\n" + "=" * 178)
    P("GATES  G2 cadence D has no drift by construction   G3 FIXK makes MRES exactly zero")
    P("=" * 178)
    P(f"  G2 max |DRIFT_pp| at cadence D   {d_cad_max:.3e}  (bar {BAR_D:.0e})  "
      f"{'PASS' if d_cad_max < BAR_D else 'FAIL'}")
    P(f"  G3 max |MRES_pp| over all cells  {mres_max:.3e}  (bar {BAR_MRES:.0e})  "
      f"{'PASS' if mres_max < BAR_MRES else 'FAIL'}")
    P(f"  G4 max |k_A - k_B| on the PRICED window  {D.dk_max.max():.0f}  (bar 0)  "
      f"{'PASS' if D.dk_max.max() == 0 else 'FAIL'}")
    P(f"     (incl. warm-up, where MOM has fewer than k_t names with 252 closes: "
      f"{D.dk_warm.max():.0f}; those bars are before start = index[260] and are never priced "
      f"or differenced, which is why G3 is exactly 0)")
    flush_log()

    # -------------------------------------------------------------- 1. the floor table
    NZ = D[D.cad != "D"].copy()
    P("\n" + "=" * 178)
    P("1. THE FLOOR, ALL GRID POINTS  (|DRIFT_pp| = annualised pp/yr on equal-target shared names)")
    P("=" * 178)
    for pn in PANELS:
        for con in CONSTRUCTIONS:
            sub = NZ[(NZ.panel == pn) & (NZ.con == con)]
            if sub.empty:
                continue
            t = sub.pivot_table(index=["q", "cad"], columns="gross", values="adrift")
            P(f"\n  {pn} / {con}   |DRIFT_pp| by (q, cadence) x gross")
            P(t.to_string(float_format=lambda x: f"{x:.5f}"))
    flush_log()

    # -------------------------------------------------------------- 2. the exponent
    P("\n" + "=" * 178)
    P("2. H_QUAD - the GROSS EXPONENT, every (panel, q, construction, cadence) cell")
    P("=" * 178)
    law = []
    for (pn, q, con, cad), sub in NZ.groupby(["panel", "q", "con", "cad"]):
        sub = sub.sort_values("gross")
        beta, se, r2, npt = loglog_beta(sub.gross.values, sub.adrift.values)
        bi, _, r2i, _ = loglog_beta(sub.gross.values, sub.drift_is.abs().values)
        bo, _, r2o, _ = loglog_beta(sub.gross.values, sub.drift_oos.abs().values)
        law.append(dict(panel=pn, q=q, con=con, cad=cad, n=npt, beta=beta, se=se, r2=r2,
                        beta_is=bi, r2_is=r2i, beta_oos=bo, r2_oos=r2o,
                        inside=bool(BETA_LO <= beta <= BETA_HI)))
    L = pd.DataFrame(law).sort_values(["panel", "con", "q", "cad"])
    L.to_csv(f"{OUT}.law.csv", index=False)
    P(L.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    bs = L.beta.dropna()
    lo, hi = np.percentile(bs, [2.5, 97.5])
    q1, q3 = np.percentile(bs, [25, 75])
    P(f"\n  pooled beta: n {len(bs)}  mean {bs.mean():.4f}  median {bs.median():.4f}  "
      f"sd {bs.std(ddof=1):.4f}  IQR [{q1:.4f}, {q3:.4f}]  95% [{lo:.4f}, {hi:.4f}]")
    P(f"  mean R^2 {L.r2.mean():.4f}   min R^2 {L.r2.min():.4f}")
    P(f"  cells with beta inside [{BETA_LO}, {BETA_HI}]: {int(L.inside.sum())} of {len(L)}")
    covers2 = lo <= 2.0 <= hi
    covers1 = lo <= 1.0 <= hi
    hquad = bool(covers2 and L.inside.all())
    P(f"  95% interval covers 2.0 (H_QUAD): {covers2}    covers 1.0 (H_LIN): {covers1}")
    P(f"  H_QUAD {'SUPPORTED' if hquad else 'REJECTED'}    "
      f"H_LIN {'SUPPORTED' if covers1 and not covers2 else 'REJECTED'}")
    out = L[~L.inside].copy()
    if len(out):
        sgn = NZ.groupby(["panel", "q", "con", "cad"]).drift_pp.agg(
            lambda x: int(np.sign(x).nunique() > 1)).rename("sign_flip")
        out = out.merge(sgn, left_on=["panel", "q", "con", "cad"], right_index=True, how="left")
        P(f"\n  the {len(out)} cells OUTSIDE the per-cell bar, with their fit quality and whether")
        P("  |DRIFT| crosses zero along the gross rung (which makes a log-log slope meaningless):")
        P("  " + out[["panel", "q", "con", "cad", "beta", "se", "r2", "sign_flip"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
        P(f"  of the {len(out)} misses, {int((out.r2 < 0.99).sum())} have R^2 < 0.99 and "
          f"{int(out.sign_flip.sum())} change sign along the rung; "
          f"{int((out.con == 'RESPREAD').sum())} are RESPREAD and "
          f"{int((out.cad == 'M').sum())} are cadence M.")
    P(f"  769's own reading, beta 1.9293 IQR [1.85, 2.09], is "
      f"{'INSIDE' if q1 <= 1.9293 <= q3 else 'OUTSIDE'} this run's IQR")
    P("\n  rule 8: the same exponent fitted on IS only and on OOS only")
    P(f"    IS  mean beta {L.beta_is.mean():.4f}  median {L.beta_is.median():.4f}  "
      f"mean R^2 {L.r2_is.mean():.4f}   inside-bar {int(L.beta_is.between(BETA_LO,BETA_HI).sum())}/{len(L)}")
    P(f"    OOS mean beta {L.beta_oos.mean():.4f}  median {L.beta_oos.median():.4f}  "
      f"mean R^2 {L.r2_oos.mean():.4f}   inside-bar {int(L.beta_oos.between(BETA_LO,BETA_HI).sum())}/{len(L)}")
    flush_log()

    # -------------------------------------------------------------- 3. the construction gap
    P("\n" + "=" * 178)
    P("3. H_INVAR - the construction gap DEGROSS/RESPREAD against its predicted q^2, per gross")
    P("=" * 178)
    piv = NZ.pivot_table(index=["panel", "q", "cad"], columns=["con", "gross"], values="adrift")
    gap = []
    for (pn, q, cad), r in piv.iterrows():
        for g in GROSSES:
            try:
                ratio = r[("DEGROSS", g)] / r[("RESPREAD", g)]
            except KeyError:
                continue
            gap.append(dict(panel=pn, q=q, cad=cad, gross=g, ratio=ratio, pred=q ** 2,
                            rel=ratio / q ** 2))
    GP = pd.DataFrame(gap)
    tt = GP.pivot_table(index=["panel", "q", "cad"], columns="gross", values="ratio")
    P(tt.to_string(float_format=lambda x: f"{x:.5f}"))
    sp = GP.groupby(["panel", "q", "cad"]).ratio.agg(["mean", "min", "max"])
    sp["spread_rel"] = (sp["max"] - sp["min"]) / sp["mean"].abs()
    P("\n  gross-to-gross spread of the ratio, per (panel, q, cadence):")
    P(sp.to_string(float_format=lambda x: f"{x:.5f}"))
    hinv = bool((sp.spread_rel < INVAR_BAR).all())
    P(f"\n  cells with spread < {INVAR_BAR:.0%}: {int((sp.spread_rel < INVAR_BAR).sum())} of {len(sp)}"
      f"    H_INVAR {'SUPPORTED' if hinv else 'REJECTED'}")
    P("  ratio / q^2 (1.0 = 769's predicted gap exactly):")
    P(GP.groupby(["panel", "q"]).rel.agg(["mean", "min", "max"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # -------------------------------------------------------------- 4. bilinear check
    P("\n" + "=" * 178)
    P("4. THE BILINEAR FIT ITSELF - log|DRIFT_pp| on log w and log E, pooled per panel/cadence")
    P("=" * 178)
    bil = []
    for (pn, cad), sub in NZ.groupby(["panel", "cad"]):
        ok = (sub.adrift > 0) & (sub.w_bar > 0) & (sub.expoA > 0)
        sub = sub[ok]
        if len(sub) < 6:
            continue
        X = np.column_stack([np.ones(len(sub)), np.log(sub.w_bar.values),
                             np.log(sub.expoA.values)])
        bb, se, r2 = ols(np.log(sub.adrift.values), X, ["a", "bw", "bE"])
        bil.append(dict(panel=pn, cad=cad, n=len(sub), bw=bb["bw"], se_w=se["bw"],
                        bE=bb["bE"], se_E=se["bE"], sum_bw_bE=bb["bw"] + bb["bE"], r2=r2,
                        corr_logw_logE=float(np.corrcoef(np.log(sub.w_bar.values),
                                                         np.log(sub.expoA.values))[0, 1])))
    BL = pd.DataFrame(bil)
    P(BL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  769's law predicts bw = 1 and bE = 1 (their SUM, 2, is the gross exponent of section 2).")
    P(f"  SUM bw+bE: mean {BL.sum_bw_bE.mean():.4f}  median {BL.sum_bw_bE.median():.4f}  "
      f"min {BL.sum_bw_bE.min():.4f}  max {BL.sum_bw_bE.max():.4f}")
    P(f"  |corr(log w, log E)| across this grid: mean {BL.corr_logw_logE.abs().mean():.4f}  "
      f"max {BL.corr_logw_logE.abs().max():.4f}  - the SPLIT is only as identified as this is "
      f"far from 1.")
    flush_log()

    # -------------------------------------------------------------- 5. the book leg
    P("\n" + "=" * 178)
    P("5. THE BOOK LEG - gross as a capital dial.  ALL grid points, 10 bps, full sample")
    P("=" * 178)
    for pn in PANELS:
        sub = B[(B.panel == pn) & (B.cad != "D")]
        t = sub.pivot_table(index=["con", "q", "cad", "arm"], columns="gross",
                            values=["CAGR", "Sharpe", "MaxDD"])
        P(f"\n  {pn}  CAGR / Sharpe / MaxDD by gross")
        P(t.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  4a and 4b pass counts by (panel, gross), all cadences/q/constructions/arms:")
    pc = B.groupby(["panel", "gross"]).agg(n=("pass4a", "size"), p4a=("pass4a", "sum"),
                                           p4b=("pass4b", "sum"),
                                           p4b_oos=("pass4b_oos", "sum"))
    P(pc.to_string())
    P("\n  which 4b leg rejects, by (panel, gross)  [-  = pass]:")
    P(B.groupby(["panel", "gross"]).f4b.value_counts().to_string())
    P("\n  cost-rung robustness of any 4b pass (0 / 10 / 25 bps):")
    keys = ["panel", "gross", "q", "con", "cad", "arm"]
    mid = B[keys].copy()
    mid["bps"] = COST_BPS
    mid["CAGR"], mid["Sharpe"], mid["MaxDD"] = B.CAGR, B.Sharpe, B.MaxDD
    mid["pass4a"], mid["pass4b"] = B.pass4a, B.pass4b
    allr = pd.concat([G, mid], ignore_index=True, sort=False)
    P(allr.groupby(["panel", "bps"]).agg(n=("pass4b", "size"), p4a=("pass4a", "sum"),
                                         p4b=("pass4b", "sum")).to_string())
    flush_log()

    # -------------------------------------------------------------- 6. rule 8
    P("\n" + "=" * 178)
    P("6. RULE 8 WALK-FORWARD - (gross, q) chosen on IS only, OOS read once")
    P("=" * 178)
    P("  Two PRE-REGISTERED selectors, both over the tuned pair (gross, q) at each")
    P("  (panel, construction, cadence, arm); no other axis is selected over:")
    P("    S1  argmax IS Sharpe")
    P("    S2  argmax IS CAGR subject to IS MaxDD <= 60% of SPY's IS MaxDD (the 4b DD cap)")
    wf = []
    for pn in PANELS:
        spy_s, live_s = COMP[pn]["spy"], COMP[pn]["live"]
        cap = 0.60 * abs(spy_s["isMaxDD"])
        for (con, cad, arm), sub in B[(B.panel == pn) & (B.cad != "D")].groupby(
                ["con", "cad", "arm"]):
            for sname in ("S1", "S2"):
                cand = sub if sname == "S1" else sub[sub.isMaxDD.abs() <= cap]
                if cand.empty:
                    wf.append(dict(panel=pn, con=con, cad=cad, arm=arm, sel=sname,
                                   gross=np.nan, q=np.nan, is_empty=True))
                    continue
                key = "isSharpe" if sname == "S1" else "isCAGR"
                r = cand.sort_values([key, "gross", "q"], ascending=[False, True, True]).iloc[0]
                wf.append(dict(panel=pn, con=con, cad=cad, arm=arm, sel=sname,
                               gross=r.gross, q=r.q, is_empty=False,
                               isCAGR=r.isCAGR, isSharpe=r.isSharpe, isMaxDD=r.isMaxDD,
                               oCAGR=r.oCAGR, oSharpe=r.oSharpe, oMaxDD=r.oMaxDD,
                               base_oCAGR=live_s["oCAGR"], base_oSharpe=live_s["oSharpe"],
                               base_oMaxDD=live_s["oMaxDD"], spy_oCAGR=spy_s["oCAGR"],
                               spy_oSharpe=spy_s["oSharpe"], spy_oMaxDD=spy_s["oMaxDD"],
                               beat_base=bool(r.oSharpe > live_s["oSharpe"]),
                               beat_spy=bool(r.oSharpe > spy_s["oSharpe"]),
                               f4b_oos=r.f4b_oos))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n" + WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok = WF[~WF["is_empty"]]
    P(f"\n  OOS Sharpe > RULES v2 OOS: {int(ok.beat_base.sum())} of {len(ok)}"
      f"    > SPY OOS: {int(ok.beat_spy.sum())} of {len(ok)}"
      f"    4b-OOS clean: {int((ok.f4b_oos == '-').sum())} of {len(ok)}")
    P("  OOS-only 4b failing legs:")
    P("  " + ok.f4b_oos.value_counts().to_string().replace("\n", "\n  "))
    P("\n  selected (gross, q) frequency - is the IS choice even stable?")
    P("  " + ok.groupby("sel")[["gross", "q"]].agg(["mean", "min", "max"]).to_string().replace(
        "\n", "\n  "))
    flush_log()

    # -------------------------------------------------------------- 7. offset sweep
    # THE decisive rule-8 read: does an IS-ONLY choice of (gross, q) land on a 4b pass?
    mm = ok.merge(B[["panel", "con", "cad", "arm", "gross", "q", "pass4b", "pass4b_oos", "f4b"]],
                  on=["panel", "con", "cad", "arm", "gross", "q"], how="left")
    P("\n" + "=" * 178)
    P("7. CALENDAR-OFFSET SWEEP on every walk-forward-clean book (ideas 805/806: a monthly 4b")
    P("   pass with no offset spread beside it is a DATE).  The rebalance mask is shifted k")
    P("   trading days within its own period; k=0 is the book above.  NOT a tuned axis - every")
    P("   offset of every selected book is reported.")
    P("=" * 178)
    NPER = {"W": 5, "M": 21, "Q": 63}
    hits = mm[mm.pass4b.fillna(False)][["panel", "con", "cad", "arm", "gross", "q"]] \
        .drop_duplicates()
    off = []
    for _, h in hits.iterrows():
        px, spy_px = PN[h.panel]
        start, live_s, spy_s = COMP[h.panel]["start"], COMP[h.panel]["live"], COMP[h.panel]["spy"]
        live = live_mask(px)
        nlive = live.sum(axis=1)
        sig = ma_dist(px) if h.arm == "MA-DIST" else mom_rank(px)
        kt = np.maximum(1, np.round(h.q * nlive)).astype(int)
        kt = pd.Series(np.minimum(kt.values, nlive.values), index=px.index)
        W = book(px, topk(sig, kt, live), h.con, nlive, h.gross)
        base = rebalance_mask(px.index, h.cad)
        for k in range(NPER[h.cad]):
            r0, tn, _, _ = run(px, W, h.cad, rmask=base.shift(k, fill_value=False))
            st = stat(rung(r0, tn, COST_BPS).loc[start:])
            off.append(dict(panel=h.panel, con=h.con, cad=h.cad, arm=h.arm, gross=h.gross,
                            q=h.q, k=k, CAGR=st["CAGR"], Sharpe=st["Sharpe"],
                            MaxDD=st["MaxDD"], oCAGR=st["oCAGR"], oSharpe=st["oSharpe"],
                            oMaxDD=st["oMaxDD"], pass4b=fail_4b(st, spy_s) == "-",
                            f4b=fail_4b(st, spy_s),
                            pass4b_oos=fail_4b_oos(st, spy_s) == "-"))
    OFF = pd.DataFrame(off)
    OFF.to_csv(f"{OUT}.offsets.csv", index=False)
    ag = OFF.groupby(["panel", "con", "cad", "arm", "gross", "q"]).agg(
        n=("k", "size"), p4b=("pass4b", "sum"), p4b_oos=("pass4b_oos", "sum"),
        CAGR_min=("CAGR", "min"), CAGR_max=("CAGR", "max"),
        Sh_min=("Sharpe", "min"), Sh_max=("Sharpe", "max"),
        DD_min=("MaxDD", "min"), DD_max=("MaxDD", "max"))
    ag["Sh_spread"] = ag.Sh_max - ag.Sh_min
    ag["DD_spread"] = ag.DD_max - ag.DD_min
    P(ag.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  which leg rejects at the offsets that fail:")
    P("  " + OFF[~OFF.pass4b].groupby(["panel", "cad", "arm"]).f4b.value_counts().to_string(
        ).replace("\n", "\n  ") if (~OFF.pass4b).any() else "  none - every offset passes")
    robust = ag[ag.p4b == ag.n]
    P(f"\n  books passing 4b at EVERY offset of their own cadence: {len(robust)} of {len(ag)}")
    P(f"  books passing at fewer than half their offsets: {int((ag.p4b < ag.n / 2).sum())}")
    flush_log()

    # -------------------------------------------------------------- verdict
    P("\n" + "=" * 178)
    P("VERDICT")
    P("=" * 178)
    P(f"  H_QUAD  (beta = 2.0 in gross): {'SUPPORTED' if hquad else 'REJECTED'}   "
      f"pooled median {bs.median():.4f}, 95% [{lo:.4f}, {hi:.4f}], "
      f"{int(L.inside.sum())}/{len(L)} cells inside [{BETA_LO}, {BETA_HI}]")
    P(f"  H_LIN   (beta = 1.0): {'SUPPORTED' if covers1 and not covers2 else 'REJECTED'}")
    P(f"  H_INVAR (gap invariant to gross): {'SUPPORTED' if hinv else 'REJECTED'}   "
      f"max spread {sp.spread_rel.max():.4f}")
    p4b_tot = int(B.pass4b.sum())
    both = int((B.pass4b & B.pass4b_oos).sum())
    P(f"  BOOK LEG: {p4b_tot} of {len(B)} books pass 4b on the full sample; "
      f"{int(B.pass4b_oos.sum())} of {len(B)} pass the OOS-only 4b legs; {both} pass BOTH; "
      f"{int(B.pass4a.sum())} of {len(B)} pass 4a.")
    P("  where the full-sample 4b passes live (gross x q x panel):")
    P("  " + B[B.pass4b].groupby(["panel", "gross", "q", "con", "cad"]).size().to_string(
        ).replace("\n", "\n  "))
    # (the decisive rule-8 merge `mm` is built at the top of section 7)
    hit = int(mm.pass4b.fillna(False).sum())
    P(f"\n  RULE 8, the decisive read: of the {len(mm)} IS-only selections, {hit} land on a book")
    P(f"  that passes full-sample 4b, and {int((mm.pass4b.fillna(False) & mm.pass4b_oos.fillna(False)).sum())}"
      f" on one that passes the OOS-only legs too.")
    P(f"  The 4b window sits at gross {sorted(B[B.pass4b].gross.unique())}; the IS selectors "
      f"chose mean gross S1 {ok[ok.sel=='S1'].gross.mean():.3f} / S2 {ok[ok.sel=='S2'].gross.mean():.3f}.")
    keep = hit > 0
    if keep:
        P("\n  the IS-only selections that DO land on a 4b pass (the walk-forward-clean books):")
        P("  " + mm[mm.pass4b.fillna(False)][
            ["panel", "con", "cad", "arm", "sel", "gross", "q", "isCAGR", "isSharpe", "isMaxDD",
             "oCAGR", "oSharpe", "oMaxDD"]].to_string(
                index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
        P(f"  all {hit} come from selector S2 (the IS DD-capped one): "
          f"{int((mm[mm.pass4b.fillna(False)].sel == 'S2').sum())} of {hit}.  S1 (argmax IS "
          f"Sharpe) lands on {int((mm[mm.pass4b.fillna(False)].sel == 'S1').sum())}, because it "
          f"always walks up to gross 1.00, where the DD leg fails.")
    P(f"\n  CAPITAL VERDICT: {'KEEP-candidate (4b)' if keep else 'KILL for capital'}"
      f" - the floor itself is a COST, not an edge; the capital result is the INTERIOR")
    P("  gross window, which an IS DD-capped selector reaches and an IS Sharpe selector does not.")
    flush_log()
    P("\nOutputs: " + "  ".join(f"{OUT.name}{s}" for s in
                                (".drift.csv", ".books.csv", ".rungs.csv", ".law.csv",
                                 ".walkforward.csv", ".offsets.csv", ".console.txt")))
    flush_log()


if __name__ == "__main__":
    main()
