#!/usr/bin/env python3
"""IDEA 562 - price the ENGINE DRIFT leg on every published arm-minus-arm decomposition.
Lane B, 2026-09-11.

THE QUESTION
------------
Idea 559 reported that its BOTH leg (the shared-name term of an arm-minus-arm split) is
"EXACTLY 0 at cadence D under an exact daily match" but reaches 0.0766 pp/yr at cadence W
"purely from the engine's daily re-normalisation of drifted weights".  The engine holds a
TARGET only on rebalance days; in between, `cur = growth / tot` renormalises each arm by ITS
OWN total, so two arms holding a shared name at the SAME target hold it at DIFFERENT weights
between rebalances.  That residue is an ENGINE ARTEFACT, not a property of either arm.

This run measures that artefact exactly and asks whether the record's published legs are
inside it.

THE SPLIT (arithmetic, the record's own convention; ADD + DROP + BOTH = arith)
-----------------------------------------------------------------------------
For arms A (MA-THRESH) and B (MOM-D, daily depth-matched, idea 559's own pair), on every bar
with held weights h and target-in-force T:
    memA = T_A > 0, memB = T_B > 0
    ADD   =  252 x 100 x mean_t  sum_{j in A only}  h_A r
    DROP  = -252 x 100 x mean_t  sum_{j in B only}  h_B r
    BOTH  =  252 x 100 x mean_t  sum_{j in both}   (h_A - h_B) r
and BOTH splits further, exactly, into
    DRIFT = the part over shared names whose TARGETS are equal (|T_A - T_B| <= 1e-15)
    MRES  = the part over shared names whose targets differ (depth-match residual)
At cadence D the engine sets h == T on every bar, so DRIFT is ZERO BY CONSTRUCTION (gate G2,
bar 0.0 exact).  At W/M/Q it is pure renormalisation.  DRIFT is therefore a NOISE FLOOR: no
published leg smaller than it carries information about the arms.

THE BOOK LEG (this lane's mandate: both KEEP paths + rule 8 on every grid point)
-------------------------------------------------------------------------------
The same channel priced as capital rather than as a decomposition term: every book is run
twice at each cadence -
    DRIFT  = the engine's native behaviour (weights drift between rebalances), and
    RTT    = "rebalance to target" - the same cadence targets restored EVERY day (freq='D' on
             the cadence-ffilled target matrix), i.e. the drift channel switched off, paying
             10 bps on the extra turnover.
If drift is only an accounting artefact the two books should be indistinguishable net of cost;
if it is worth capital (or costs it) that shows up here, under both KEEP paths.

2 TUNED PARAMS: CADENCE {D,W,M,Q} x PANEL {U56,B136,SMALL439}.  Theta, arm, construction and
handling are REPORTED axes, never selected over.  Gross is pinned at the live 0.75.
Costs 10 bps per unit turnover (0 and 25 derived exactly and reported), next-day execution.
IS = start..2016-12-31, OOS = 2017-01-01..end, read once (PROTOCOL rule 8).

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; dead names are absent and CAGR
levels are inflated.  The 44 SMALL names with max_1d_move >= 1.0 are dropped (data/small_meta.csv,
idea 559's own filter).  The drift leg is an arm-minus-arm quantity inside one panel at
identical depth, where the bias very largely cancels; the KEEP columns and the rule-8 levels
are NOT protected and are read with that caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .drift.csv .grid.csv .walkforward.csv .keeppaths.csv .census.csv .censusfile.csv
         .rungs.csv .console.txt
"""
import glob
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
PANELS = ["U56", "B136", "SMALL439"]
THETA = [0.20, 0.06, 0.00, -0.12, -0.25]
ARMS = ["MA-THRESH", "MOM-D"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
CADENCES = ["D", "W", "M", "Q"]          # tuned param 1
GROSS = 0.75                             # the live gross, pinned
HANDLING = ["DRIFT", "RTT"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS_TGT = 1e-15
BAR_ENGINE = 1e-12
BAR_RUNG = 1e-15
BAR_IDENT = 1e-12

# the record's committed set-decomposition legs (STRICT tier: files carrying BOTH_pp)
STRICT_LEGS = ["ADD_pp", "DROP_pp", "BOTH_pp", "arith_pp", "sel_geo_pp", "sel_arith_pp",
               "jensen_pp", "COST_pp", "net10_pp"]
# WIDE tier: any committed column that is an arm-minus-arm leg in pp/yr
WIDE_LEGS = STRICT_LEGS + ["sel_pp", "level_pp", "timing_pp", "exp_pp", "EXP_pp", "SEL_pp",
                           "resid_pp", "dCAGR_pp", "dCAGR0_pp", "dCAGR0_dg_pp", "dCAGR0_rs_pp",
                           "gap_pp", "ann_pp", "raw_per_pp", "conv_per_pp"]

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def run(px, W, freq):
    """engine.backtest's arithmetic, returning the zero-cost path, turnover, the HELD weight
    matrix and the TARGET-IN-FORCE matrix (gate G0 checks it against engine.backtest)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
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


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def mom_rank(px):
    return (px.shift(21) / px.shift(252) - 1).where(live_mask(px))


def daily_matched(sig, live, gm):
    """idea 559's daily match: k_t = k_ma_t every day, clipped to the rankable count."""
    k_ma = gm.sum(axis=1)
    kt = np.minimum(k_ma, sig.notna().sum(axis=1))
    return sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def book(px, g, construction, gross=GROSS):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def rtt_weights(W, idx, freq):
    """The cadence's targets restored EVERY day: sample W on the cadence schedule, hold flat."""
    m = rebalance_mask(idx, freq)
    return W.where(m, np.nan).ffill().fillna(0.0)


# ================================================================== main
def main():
    P("=" * 170)
    P("IDEA 562 - price the ENGINE DRIFT leg on every published arm-minus-arm decomposition"
      "   (lane B, 2026-09-11)")
    P("=" * 170)
    P("PROTOCOL: 10 bps per unit turnover (0/25 derived exactly and reported), next-day")
    P(f"execution, no shorting, no leverage.  IS = start..{IS_END}, OOS = {OOS_START}..end.")
    P(f"2 tuned params: CADENCE {CADENCES} x PANEL {PANELS}.  Theta {THETA}, arm {ARMS},")
    P(f"construction {CONSTRUCTIONS}, handling {HANDLING} are reported axes, never selected")
    P(f"over.  Gross pinned at the live {GROSS}.  Both KEEP paths on every book.")
    P("SURVIVORSHIP: B136/SMALL439 are current constituents only; CAGR inflated, KEEP not immune.")
    flush_log()

    u, b = load_universe(), load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL439": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "  ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")

    # -------------------------------------------------------------- G0 / G1
    P("\n" + "=" * 170)
    P("G0  run() vs engine.backtest       G1  derived cost rung vs a fresh run at that rung")
    P("=" * 170)
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
        P(f"  {pn:9s} G0 {g0:.3e}   G1 {g1:.3e}")
    P(f"  G0 max {g0:.3e} (bar {BAR_ENGINE:.0e})  {'PASS' if g0 < BAR_ENGINE else 'FAIL'}   "
      f"G1 max {g1:.3e} (bar {BAR_RUNG:.0e})  {'PASS' if g1 < BAR_RUNG else 'FAIL'}")
    flush_log()

    # -------------------------------------------------------------- comparands
    COMP = {}
    P("\n" + "=" * 170)
    P("COMPARANDS per panel (RULES v2 = the 4a bar, weekly, 10 bps; SPY = the 4b bar)")
    P("=" * 170)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        r0, tn, _, _ = run(px, rules_v2_weights(px), "W")
        live_s = stat(rung(r0, tn, COST_BPS).loc[start:])
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        COMP[pn] = dict(live=live_s, spy=spy_s, start=start,
                        years=len(px.loc[start:]) / 252)
        P(f"  {pn:9s} {start.date()}..{px.index[-1].date()} ({COMP[pn]['years']:.2f} yrs, "
          f"{px.shape[1]} names)")
        P(f"      RULES v2 CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} MaxDD "
          f"{live_s['MaxDD']:.4f} H1/H2 {live_s['H1']:.4f}/{live_s['H2']:.4f}  OOS "
          f"{live_s['oCAGR']:.4f}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
        P(f"      SPY      CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD "
          f"{spy_s['MaxDD']:.4f} H1/H2 {spy_s['H1']:.4f}/{spy_s['H2']:.4f}  OOS "
          f"{spy_s['oCAGR']:.4f}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
        P(f"      4b bars: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} OOS>{spy_s['oSharpe']:.4f} "
          f"MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%} CAGR>={0.70*spy_s['CAGR']:.2%}")
    flush_log()

    # -------------------------------------------------------------- the grid
    P("\n" + "=" * 170)
    P(f"THE GRID - {len(PANELS)} panels x {len(THETA)} theta x {len(CONSTRUCTIONS)} constructions"
      f" x {len(CADENCES)} cadences = {len(PANELS)*len(THETA)*len(CONSTRUCTIONS)*len(CADENCES)}"
      f" arm pairs; {len(ARMS)*len(HANDLING)} books each")
    P("=" * 170)
    drift, books, rungs = [], [], []
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = COMP[pn]["start"]
        live_s, spy_s = COMP[pn]["live"], COMP[pn]["spy"]
        live = live_mask(px)
        mom = mom_rank(px)
        R = px.pct_change().fillna(0.0).values
        sel = px.index >= start
        for th in THETA:
            gates = {"MA-THRESH": ma_gate(px, th)}
            gates["MOM-D"] = daily_matched(mom, live, gates["MA-THRESH"])
            dk = (gates["MOM-D"].sum(axis=1).loc[start:]
                  - gates["MA-THRESH"].sum(axis=1).loc[start:])
            for con in CONSTRUCTIONS:
                W = {a: book(px, gates[a], con) for a in ARMS}
                for cad in CADENCES:
                    res = {}
                    for a in ARMS:
                        for hnd in HANDLING:
                            Wx = W[a] if hnd == "DRIFT" else rtt_weights(W[a], px.index, cad)
                            fq = cad if hnd == "DRIFT" else "D"
                            r0, tn, held, tgt = run(px, Wx, fq)
                            res[(a, hnd)] = (r0, tn, held, tgt)
                            st = stat(rung(r0, tn, COST_BPS).loc[start:])
                            row = dict(panel=pn, theta=th, con=con, cad=cad, arm=a, hnd=hnd,
                                       gross=GROSS, turn_yr=float(tn.loc[start:].sum()
                                                                  / COMP[pn]["years"]),
                                       expo=float(pd.Series(held.sum(axis=1),
                                                            index=px.index).loc[start:].mean()),
                                       **st)
                            row["pass4a"] = verdict_4a(st, live_s)
                            row["f4b"] = fail_4b(st, spy_s)
                            row["pass4b"] = row["f4b"] == "-"
                            books.append(row)
                            for c in RUNGS:
                                if c != COST_BPS:
                                    sc = stat(rung(r0, tn, c).loc[start:])
                                    rungs.append(dict(panel=pn, theta=th, con=con, cad=cad,
                                                      arm=a, hnd=hnd, bps=c,
                                                      CAGR=sc["CAGR"], Sharpe=sc["Sharpe"],
                                                      MaxDD=sc["MaxDD"],
                                                      pass4a=verdict_4a(sc, live_s),
                                                      pass4b=fail_4b(sc, spy_s) == "-"))
                    # ---- the arm-minus-arm split, per handling
                    for hnd in HANDLING:
                        _, _, hA, tA = res[("MA-THRESH", hnd)]
                        _, _, hB, tB = res[("MOM-D", hnd)]
                        memA, memB = tA > 0, tB > 0
                        both = memA & memB
                        eq = both & (np.abs(tA - tB) <= EPS_TGT)
                        d = (hA - hB) * R
                        ann = 252 * 100
                        f = lambda M: float(np.nansum(np.where(M, d, 0.0), axis=1)[sel].mean() * ann)
                        add = float(np.nansum(np.where(memA & ~memB, hA * R, 0.0),
                                              axis=1)[sel].mean() * ann)
                        drp = -float(np.nansum(np.where(memB & ~memA, hB * R, 0.0),
                                               axis=1)[sel].mean() * ann)
                        DR, MR = f(eq), f(both & ~eq)
                        drift.append(dict(
                            panel=pn, theta=th, con=con, cad=cad, hnd=hnd,
                            ADD_pp=add, DROP_pp=drp, BOTH_pp=DR + MR, DRIFT_pp=DR, MRES_pp=MR,
                            arith_pp=add + drp + DR + MR,
                            n_both=float(both[sel].sum(axis=1).mean()),
                            n_eq=float(eq[sel].sum(axis=1).mean()),
                            eq_share=float(eq[sel].sum() / max(both[sel].sum(), 1)),
                            dk_abs=float(dk.abs().mean()),
                            exact_share=float((dk == 0).mean()),
                            ident_max=float(np.abs(hA - hB)[sel][eq[sel]].max()
                                            if eq[sel].any() else 0.0)))
        P(f"  {pn:9s} done ({len([x for x in books if x['panel']==pn])} books, "
          f"{len([x for x in drift if x['panel']==pn])} splits)")
        flush_log()

    DF = pd.DataFrame(books)
    DR = pd.DataFrame(drift)
    RG = pd.DataFrame(rungs)
    DF.to_csv(f"{OUT}.grid.csv", index=False)
    DR.to_csv(f"{OUT}.drift.csv", index=False)
    RG.to_csv(f"{OUT}.rungs.csv", index=False)

    # -------------------------------------------------------------- G2 the structural gate
    P("\n" + "=" * 170)
    P("G2  DRIFT is ZERO BY CONSTRUCTION at cadence D (held == target on every bar)")
    P("=" * 170)
    dD = DR[DR.cad == "D"]
    g2 = float(dD.DRIFT_pp.abs().max())
    g2i = float(dD.ident_max.max())
    P(f"  max |DRIFT_pp| over the {len(dD)} cadence-D splits: {g2:.3e}   (bar 0.0 exact)  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    P(f"  max |h_A - h_B| on equal-target shared cells at D: {g2i:.3e} (bar {BAR_IDENT:.0e})  "
      f"{'PASS' if g2i < BAR_IDENT else 'FAIL'}")
    P(f"  and at D the residue that remains is the DEPTH-MATCH residual, not drift: "
      f"max |MRES_pp| {float(dD.MRES_pp.abs().max()):.4f} pp/yr, "
      f"mean exact-match day share {float(dD.exact_share.mean()):.4f}")
    flush_log()

    # -------------------------------------------------------------- A. the drift floor
    P("\n" + "=" * 170)
    P("A.  THE DRIFT FLOOR - |DRIFT_pp| by cadence (native DRIFT handling, all panels/theta/con)")
    P("=" * 170)
    nat = DR[DR.hnd == "DRIFT"]
    tab = nat.groupby("cad").DRIFT_pp.agg(
        n="size", median=lambda x: x.abs().median(), p90=lambda x: x.abs().quantile(0.90),
        max=lambda x: x.abs().max(), signed_mean="mean")
    tab = tab.reindex(CADENCES)
    P(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  by cadence x panel (max |DRIFT_pp| pp/yr):")
    P(nat.pivot_table(index="cad", columns="panel", values="DRIFT_pp",
                      aggfunc=lambda x: x.abs().max()).reindex(CADENCES)[PANELS]
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  by cadence x construction (max |DRIFT_pp| pp/yr):")
    P(nat.pivot_table(index="cad", columns="con", values="DRIFT_pp",
                      aggfunc=lambda x: x.abs().max()).reindex(CADENCES)
      .to_string(float_format=lambda x: f"{x:.4f}"))
    FLOOR = {c: float(nat[nat.cad == c].DRIFT_pp.abs().max()) for c in CADENCES}
    FLOOR_PANEL = {(c, p): float(nat[(nat.cad == c) & (nat.panel == p)].DRIFT_pp.abs().max())
                   for c in CADENCES for p in PANELS}
    P(f"\n  FLOOR (max |DRIFT_pp|, pp/yr): " + "  ".join(f"{c} {FLOOR[c]:.4f}" for c in CADENCES))
    P(f"  idea 559 published max 0.0766 pp/yr at cadence W on its own 9-theta grid; this run's "
      f"W floor is {FLOOR['W']:.4f}.")
    P(f"  DRIFT as a share of its own BOTH leg: median "
      f"{float((nat[nat.cad!='D'].DRIFT_pp.abs() / nat[nat.cad!='D'].BOTH_pp.abs().clip(lower=1e-12)).median()):.4f}"
      f" on W/M/Q.")
    P("\n  the split itself, medians by cadence (pp/yr, native handling):")
    P(nat.groupby("cad")[["ADD_pp", "DROP_pp", "BOTH_pp", "DRIFT_pp", "MRES_pp", "arith_pp"]]
      .median().reindex(CADENCES).to_string(float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # -------------------------------------------------------------- B. census of the record
    P("\n" + "=" * 170)
    P("B.  THE CENSUS - how many committed published legs sit INSIDE the drift floor")
    P("=" * 170)
    bt = REPO / "research" / "backtests"
    crows, frows = [], []
    for f in sorted(glob.glob(str(bt / "*.csv"))):
        name = Path(f).name
        if name.startswith(OUT.name):
            continue
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        cols = [c for c in d.columns if c in WIDE_LEGS]
        if not cols:
            continue
        strict_file = "BOTH_pp" in d.columns
        cadcol = "cad" if "cad" in d.columns else ("cadence" if "cadence" in d.columns else None)
        pancol = "panel" if "panel" in d.columns else None
        nin = {c: 0 for c in CADENCES}
        for c in cols:
            v = pd.to_numeric(d[c], errors="coerce")
            for i, val in v.items():
                if not np.isfinite(val):
                    continue
                cd = str(d[cadcol].iloc[i]) if cadcol else ""
                cd = cd if cd in CADENCES else "W"      # the record's default cadence
                pnl = str(d[pancol].iloc[i]) if pancol else ""
                fl = FLOOR_PANEL.get((cd, pnl), FLOOR[cd])
                crows.append(dict(file=name, col=c, tier="STRICT" if strict_file else "WIDE",
                                  cad_stated=bool(cadcol), cad=cd, panel=pnl, value=float(val),
                                  floor=fl, inside=abs(float(val)) <= fl,
                                  inside_W=abs(float(val)) <= FLOOR["W"],
                                  inside_Q=abs(float(val)) <= FLOOR["Q"]))
        sub = [r for r in crows if r["file"] == name]
        frows.append(dict(file=name, tier="STRICT" if strict_file else "WIDE", n=len(sub),
                          n_inside=sum(r["inside"] for r in sub),
                          share_inside=np.mean([r["inside"] for r in sub]) if sub else np.nan,
                          cad_stated=bool(cadcol),
                          med_abs=float(np.median([abs(r["value"]) for r in sub])) if sub else np.nan))
    CE = pd.DataFrame(crows)
    FE = pd.DataFrame(frows)
    CE.to_csv(f"{OUT}.census.csv", index=False)
    FE.to_csv(f"{OUT}.censusfile.csv", index=False)
    P(f"  {len(FE)} committed CSVs carry a leg column in pp/yr; {len(CE)} published leg values "
      f"({int((FE.tier=='STRICT').sum())} files STRICT = carry ADD/DROP/BOTH).")
    P(f"  cadence STATED on the row: {CE.cad_stated.mean():.1%} of values "
      f"(the rest are read at the record's default cadence W).")
    for t in ("STRICT", "WIDE"):
        c = CE[CE.tier == t]
        if not len(c):
            continue
        P(f"\n  --- {t} tier: {len(c)} values, {int(c.inside.sum())} inside their own "
          f"(cadence,panel) drift floor = {c.inside.mean():.2%}")
        P(c.groupby("col").agg(n=("value", "size"),
                               med_abs=("value", lambda x: x.abs().median()),
                               inside=("inside", "sum"),
                               share=("inside", "mean")).sort_values("n", ascending=False)
          .head(20).to_string(float_format=lambda x: f"{x:.4f}"))
    st = CE[CE.tier == "STRICT"]
    P(f"\n  STRICT BOTH_pp alone: {int((st.col=='BOTH_pp').sum())} values, "
      f"{int(st[st.col=='BOTH_pp'].inside.sum())} inside "
      f"({st[st.col=='BOTH_pp'].inside.mean():.2%}); "
      f"median |BOTH_pp| {float(st[st.col=='BOTH_pp'].value.abs().median()):.4f} pp/yr")
    for col in ("ADD_pp", "DROP_pp", "sel_geo_pp"):
        sc = st[st.col == col]
        if len(sc):
            P(f"  STRICT {col:12s}: {len(sc)} values, {int(sc.inside.sum())} inside "
              f"({sc.inside.mean():.2%}); median |value| {float(sc.value.abs().median()):.4f}")
    P(f"\n  worst case reading (every value judged against the WIDEST floor, "
      f"Q = {FLOOR['Q']:.4f} pp/yr): STRICT {CE[CE.tier=='STRICT'].inside_Q.mean():.2%} inside, "
      f"WIDE {CE[CE.tier=='WIDE'].inside_Q.mean():.2%} inside.")
    P("  files whose published legs are MOSTLY inside the floor (share >= 0.5):")
    bad_f = FE[(FE.share_inside >= 0.5) & (FE.n >= 3)].sort_values("share_inside",
                                                                  ascending=False)
    P("    none" if not len(bad_f) else
      bad_f.head(15).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # -------------------------------------------------------------- C. the book leg
    P("\n" + "=" * 170)
    P("C.  THE BOOK LEG - DRIFT (native) minus RTT (drift switched off) at 10 bps")
    P("=" * 170)
    key = ["panel", "theta", "con", "cad", "arm"]
    piv = DF.pivot_table(index=key, columns="hnd",
                         values=["CAGR", "Sharpe", "MaxDD", "oSharpe", "oCAGR", "turn_yr"])
    H = pd.DataFrame(index=piv.index)
    for m in ("CAGR", "Sharpe", "MaxDD", "oSharpe", "oCAGR", "turn_yr"):
        H["d" + m] = piv[(m, "DRIFT")] - piv[(m, "RTT")]
    H = H.reset_index()
    P(f"  {len(H)} matched pairs.  DRIFT beats RTT on full-sample Sharpe in "
      f"{(H.dSharpe > 0).mean():.1%} of pairs (median {H.dSharpe.median():+.4f}); "
      f"on CAGR {(H.dCAGR > 0).mean():.1%} (median {H.dCAGR.median():+.4f} = "
      f"{100*H.dCAGR.median():+.2f} pp/yr).")
    P(f"  turnover bought by RTT: median {-H.dturn_yr.median():.2f}x/yr extra "
      f"(= {-H.dturn_yr.median()*COST_BPS/1e4*100:.2f} pp/yr of cost at {COST_BPS} bps).")
    P("\n  by cadence (dSharpe / dCAGR pp / d turnover x per yr, DRIFT minus RTT):")
    P(H.groupby("cad")[["dSharpe", "dCAGR", "dMaxDD", "doSharpe", "dturn_yr"]].median()
      .reindex(CADENCES).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  by panel:")
    P(H.groupby("panel")[["dSharpe", "dCAGR", "dMaxDD", "doSharpe", "dturn_yr"]].median()
      .reindex(PANELS).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  share of pairs where DRIFT wins Sharpe, by cadence x panel:")
    P(H.assign(win=H.dSharpe > 0).pivot_table(index="cad", columns="panel", values="win")
      .reindex(CADENCES)[PANELS].to_string(float_format=lambda x: f"{x:.3f}"))
    flush_log()

    # -------------------------------------------------------------- D. KEEP paths
    P("\n" + "=" * 170)
    P("D.  BOTH KEEP PATHS on all " + str(len(DF)) + " books (4a vs RULES v2, 4b vs SPY, 10 bps)")
    P("=" * 170)
    P(f"  4a passes {int(DF.pass4a.sum())}/{len(DF)}   4b passes {int(DF.pass4b.sum())}/{len(DF)}"
      f"   BOTH {int((DF.pass4a & DF.pass4b).sum())}/{len(DF)}")
    P("\n  4a / 4b counts by cadence x handling:")
    P(DF.pivot_table(index="cad", columns="hnd", values=["pass4a", "pass4b"], aggfunc="sum")
      .reindex(CADENCES).to_string())
    P("\n  4b counts by panel x arm:")
    P(DF.pivot_table(index="panel", columns="arm", values="pass4b", aggfunc="sum")
      .reindex(PANELS).to_string())
    P("\n  4b failing-bar histogram (books failing exactly one bar are named by it):")
    P(DF.f4b.value_counts().head(12).to_string())
    kp = DF[DF.pass4b | DF.pass4a]
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    if len(kp):
        P(f"\n  the {len(kp)} passing books:")
        P(kp.sort_values("Sharpe", ascending=False)
          .head(25)[["panel", "theta", "con", "cad", "arm", "hnd", "CAGR", "Sharpe", "MaxDD",
                     "H1", "H2", "oSharpe", "pass4a", "pass4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  cost-rung check (4a/4b counts at 0 and 25 bps vs 10):")
    P(RG.groupby("bps")[["pass4a", "pass4b"]].sum().to_string())
    flush_log()

    # -------------------------------------------------------------- E. rule 8
    P("\n" + "=" * 170)
    P("E.  RULE 8 WALK-FORWARD - (cadence, panel) chosen on IS Sharpe alone, OOS untouched")
    P("=" * 170)
    wf = []
    for (arm, con, hnd, th), g in DF.groupby(["arm", "con", "hnd", "theta"]):
        pick = g.loc[g.isSharpe.idxmax()]
        lv, sp = COMP[pick.panel]["live"], COMP[pick.panel]["spy"]
        wf.append(dict(arm=arm, con=con, hnd=hnd, theta=th, pick_cad=pick.cad,
                       pick_panel=pick.panel, isSharpe=pick.isSharpe,
                       oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                       base_oCAGR=lv["oCAGR"], base_oSharpe=lv["oSharpe"],
                       base_oMaxDD=lv["oMaxDD"], spy_oCAGR=sp["oCAGR"],
                       spy_oSharpe=sp["oSharpe"], spy_oMaxDD=sp["oMaxDD"],
                       beats_base=pick.oSharpe > lv["oSharpe"],
                       beats_spy=pick.oSharpe > sp["oSharpe"],
                       oos4b=(pick.oSharpe > sp["oSharpe"]
                              and abs(pick.oMaxDD) <= 0.60 * abs(sp["oMaxDD"])
                              and pick.oCAGR >= 0.70 * sp["oCAGR"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  {len(WF)} selector cells (arm x construction x handling x theta), each picking one of "
      f"{len(CADENCES)*len(PANELS)} (cadence, panel) points on IS Sharpe.")
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  OOS: picks beat RULES v2 on Sharpe {int(WF.beats_base.sum())}/{len(WF)}, "
      f"beat SPY {int(WF.beats_spy.sum())}/{len(WF)}, clear the OOS 4b legs "
      f"{int(WF.oos4b.sum())}/{len(WF)}.")
    P(f"  mean OOS CAGR {WF.oCAGR.mean():.4f} / Sharpe {WF.oSharpe.mean():.4f} / MaxDD "
      f"{WF.oMaxDD.mean():.4f}   vs baseline {WF.base_oCAGR.mean():.4f}/"
      f"{WF.base_oSharpe.mean():.4f}/{WF.base_oMaxDD.mean():.4f}   vs SPY "
      f"{WF.spy_oCAGR.mean():.4f}/{WF.spy_oSharpe.mean():.4f}/{WF.spy_oMaxDD.mean():.4f}")
    P(f"  cadence picked: {WF.pick_cad.value_counts().to_dict()}   panel picked: "
      f"{WF.pick_panel.value_counts().to_dict()}")
    P(f"  handling picked by the selector where it is free to choose (DRIFT vs RTT, IS Sharpe):")
    hsel = DF.loc[DF.groupby(["arm", "con", "theta", "panel", "cad"]).isSharpe.idxmax()]
    P(f"    DRIFT chosen in {int((hsel.hnd=='DRIFT').sum())}/{len(hsel)} cells "
      f"({(hsel.hnd=='DRIFT').mean():.1%}); OOS Sharpe of the IS-chosen handling "
      f"{hsel.oSharpe.mean():.4f} vs the other {DF.loc[DF.groupby(['arm','con','theta','panel','cad']).isSharpe.idxmin()].oSharpe.mean():.4f}")
    flush_log()

    P("\n" + "=" * 170)
    P("SUMMARY")
    P("=" * 170)
    P(f"  drift floor (max |DRIFT_pp|): D {FLOOR['D']:.4f}  W {FLOOR['W']:.4f}  "
      f"M {FLOOR['M']:.4f}  Q {FLOOR['Q']:.4f} pp/yr")
    P(f"  census: {int(CE.inside.sum())}/{len(CE)} published leg values inside their own floor "
      f"({CE.inside.mean():.2%}); STRICT tier {CE[CE.tier=='STRICT'].inside.mean():.2%}")
    P(f"  book leg: DRIFT beats RTT on Sharpe {(H.dSharpe>0).mean():.1%} of "
      f"{len(H)} pairs, median {H.dSharpe.median():+.4f}")
    P(f"  KEEP: 4a {int(DF.pass4a.sum())}/{len(DF)}, 4b {int(DF.pass4b.sum())}/{len(DF)}, "
      f"BOTH {int((DF.pass4a & DF.pass4b).sum())}/{len(DF)}")
    P(f"  rule 8: {int(WF.beats_base.sum())}/{len(WF)} picks beat RULES v2 OOS, "
      f"{int(WF.beats_spy.sum())}/{len(WF)} beat SPY")
    P(f"  gates: G0 {g0:.3e}  G1 {g1:.3e}  G2 {g2:.3e} (exact-zero bar)")
    flush_log()


if __name__ == "__main__":
    main()
