#!/usr/bin/env python3
"""Idea 2266 (2026-09-22, lane B) -- DOES THE DD-BUDGETED IS-ONLY CHOOSER GENERALISE TO A DIAL
THAT IS NOT GROSS?

WHY THIS RUN EXISTS
    Idea 2264 (lane B, this morning) established that the record's "not rule-8 reachable" verdict
    on its only reliable 4b passer was a claim about the CHOOSER, not about the cell: IS Sharpe is
    the one statistic GROSS is invariant to (U56 1.2010 -> 1.2000 over g = 0.25..1.50), so the
    habitual IS-Sharpe chooser takes the ladder END and blows the OOS drawdown cap, while an
    IS-only DRAWDOWN-BUDGET chooser -- take the largest rung whose IS MaxDD stays inside
    kappa x (IS SPY MaxDD) -- reaches the 4b cell at 9 of 10 panel x cost cells.

    But 2264 tested the fix on GROSS ALONE.  On gross, IS MaxDD is MONOTONE in the dial and the
    budget is slack at the top, so under PROTOCOL rule 2's no-leverage cap the device degenerates
    to the ZERO-parameter rule "take the largest legal gross" -- it picked g = 1.00 at every one
    of its cells.  A rule that always returns the ladder end has not been tested; the tape never
    had a chance to move it.

    THIS RUN asks the question 2264 could not: on a dial where the budget does NOT saturate --
    where IS MaxDD is NOT monotone, so the constraint has to actually choose -- does the device
    buy anything over the habitual chooser and over the shipped default?

THE TWO DIALS THAT ARE NOT GROSS (both walked on the LIVE book, nothing else changed)
    DIAL BAND  `baseline.rules_v2_weights(px, band=b, gross=g)`, b in {0.00,0.01,0.02,0.03,0.05,
               0.08,0.12,0.16,0.20,0.30,0.40}, 11 rungs.  b = 0.03 is the SHIPPED incumbent.
    DIAL TOPN  the same book restricted to the top-N names by the composite rank (12-1 momentum +
               6m + 3m, percentile-ranked and averaged, NO vol scaling -- idea 951's constructor)
               among the names INSIDE the 3% band, equal weight at gross/N, gated-out weight to
               CASH and never re-spread.  N in {5,10,15,20,30,40,ALL}, 7 rungs.  N = ALL is the
               SHIPPED incumbent and is `rules_v2_weights` itself (gate G1).
    DIAL GROSS (CONTROL, not an answer) 2264's own ladder g in {0.250..1.500 step 0.125}, re-run
               here so the degeneracy is re-measured inside this harness rather than quoted.

    CONFOUND, stated up front: at finite N the top-N book deploys MORE gross than the ALL book
    (gross/N on N names vs gross/N_priced on the in-band names), so N is not a pure selection
    dial.  ARM M re-prices every finite-N rung rescaled to the ALL book's IS-window mean deployed
    gross (an IS-only constant, legal, de-grossing only) and both arms are published.

THE CHOOSERS (all IS-ONLY on 2009-2016; every pick is a member of the published ladder)
    C_DDB_CAGR(kappa)    among rungs whose IS MaxDD is inside kappa x (IS SPY MaxDD), argmax IS
                         CAGR.  This is the FAITHFUL generalisation of 2264's rule: on the gross
                         dial CAGR is monotone in g, so it returns "the largest gross inside the
                         budget" exactly -- gate G4 asserts it reproduces 2264's picks.
    C_DDB_SHARPE(kappa)  the same feasible set, argmax IS SHARPE (idea 960's variant of the
                         device).  Published beside it because the tie-break is the whole
                         content of the rule once the dial stops being monotone.
    C_SHARPE             argmax IS Sharpe over the whole ladder            (the habitual chooser)
    C_CALMAR             argmax IS CAGR / |IS MaxDD|                       (a DD-aware comparand)
    C_LIVE               the shipped rung (b = 0.03 / N = ALL / g = 0.75)  (no-information control)
    ORACLE_OOS           argmax OOS Sharpe -- ILLEGAL, published only as the regret yardstick.
    kappa in {0.40,0.50,0.60,0.70,0.80,0.90,1.00}; 0.60 is PROTOCOL 4b's own delta.

    TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4): kappa and the DIAL VALUE (b, or N, or g).
    PANEL {u56,b136}, GROSS rung {0.75 live, 1.00 = 2264's candidate}, COST {0,5,10,25,50} bps,
    cadence (W) and t+1 execution are REPORTED axes, never selected on.

GATES (printed before any hypothesis is read)
    G1  N = ALL and b = 0.03 ARE the live book: max|dw| = 0 against `rules_v2_weights`, and the
        10 bps return lines agree at max|dr| = 0.
    G2  the derived cost ladder equals a full re-simulation at 25 bps to < 1e-15 (the engine
        subtracts turnover*bps/1e4 and never feeds cost back into positions).
    G3  2264's committed cells reproduce: u56 live v2 @10bps 8.62%/1.2010/-12.05%, halves
        1.2276/1.1806, OOS 9.46%/1.2767/-12.05%; u56 g=1.00 @10bps 11.53%/1.2009/-15.91%, OOS
        12.67%/1.2760/-15.91%; SPY OOS 15.29%/0.8751/-33.72%.
    G4  DEGENERACY CONTROL: on the GROSS dial C_DDB_CAGR's pick == max{g : IS MaxDD >= kappa x IS
        SPY MaxDD} at every kappa x cost x panel cell -- i.e. the CAGR tie-break IS 2264's rule.
    G5  every book cell and every chooser cell is published (counts asserted).
    G6  SATURATION STRUCTURE: IS MaxDD is monotone in GROSS (2264's G4) and is NOT monotone on
        BAND or TOPN -- the premise of this run, measured rather than assumed.

RULE 8 (PROTOCOL rule 8): every chooser sees 2009-2016 ONLY; 2017-2026 is read once and reported
    untouched against the live RULES v2 book's OOS and SPY's OOS.

CAVEATS carried
    SURVIVORSHIP (PROTOCOL rule 9 / idea 54): u56 and b136 are CURRENT constituents held from
    2008, so every CAGR level is optimistic and both 4b level legs are easier than on a
    point-in-time panel.  Costs are flat per unit turnover: no spread, impact or borrow.  One
    cadence (W), one delay (t+1).  The IS window is flattered by tape order (IS SPY MaxDD -22.06%
    is SHALLOWER than OOS SPY's -33.72%), so an IS drawdown budget is automatically conservative
    out of sample -- 2264 flagged this and it applies here unchanged.
    Deterministic, standalone.  Writes .console.txt, .grid.csv, .choosers.csv next to itself.
    Modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-22_dd-budget-chooser-off-the-gross-dial_B"
OUT = ROOT / "research" / "backtests"

BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.30, 0.40]
NS = [5, 10, 15, 20, 30, 40, "ALL"]
GROSSES = [0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000, 1.125, 1.250, 1.375, 1.500]
KAPPAS = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
PANELS = ["u56", "b136"]
GROSS_RUNGS = [0.75, 1.00]        # reported axis for the BAND / TOPN dials, never selected on
LIVE_BAND, LIVE_GROSS, FREQ = 0.03, 0.75, "W"
PHI, DELTA = 0.70, 0.60           # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers
OOS_START = "2017-01-01"

_LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------- books
def topn_weights(px, n, band=LIVE_BAND, gross=1.0):
    """The live band book restricted to the top-n names by composite rank INSIDE the band.
    Equal weight gross/n; if fewer than n names are in the band the rest of NAV is CASH."""
    if n == "ALL":
        return rules_v2_weights(px, band=band, gross=gross)
    st = band_state(px, band) & px.notna()
    sc, _, _ = score(px, vol_scale=False)
    elig = sc.where(st)
    rank = elig.rank(axis=1, ascending=False)
    return ((rank <= n) & st).astype(float) * (gross / n)


# ------------------------------------------------------------------- metrics helpers
def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def sim(px, w):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"], res["turnover"]


def at_cost(r0, to, bps):
    return r0 - to * bps / 1e4


def legs_4b(r, spy):
    c, s, d = m3(r)
    cs, ss, ds = m3(spy)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, L_SHARPE=bool(s > ss), L_DD=bool(d >= DELTA * ds),
                L_CAGR=bool(c >= PHI * cs), cap=DELTA * ds, floor=PHI * cs)


def main():
    say(f"# {STEM}")
    say("# idea 2266 -- does 2264's IS-only DRAWDOWN-BUDGET chooser buy anything on a dial that "
        "is NOT gross?")
    say(f"# BANDS={BANDS}\n# NS={NS}\n# GROSSES(control)={GROSSES}")
    say(f"# kappas={KAPPAS}  costs={COSTS} bps  panels={PANELS}  gross rungs={GROSS_RUNGS}  "
        f"cadence={FREQ}  t+1")
    say("")

    gate_rows, grid_rows, ch_rows = [], [], []
    nsim = 0

    for panel in PANELS:
        px = load_universe(broad=(panel == "b136"))
        start = px.index[260]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        idx = spy_full.index
        is_mask = idx < pd.Timestamp(OOS_START)
        oos_mask = ~is_mask
        yrs = len(idx) / 252

        # ---------------- simulate every rung once, at zero cost -----------------------------
        raw = {}          # (dial, arm, gross_rung, rung) -> (r0, turnover)
        mg = {}           # realised IS-window mean deployed gross of the TARGET weights
        for g in GROSS_RUNGS:
            for b in BANDS:
                w = rules_v2_weights(px, band=b, gross=g)
                raw[("BAND", "P", g, b)] = tuple(x.loc[start:] for x in sim(px, w))
                mg[("BAND", "P", g, b)] = float(w.loc[start:][is_mask].sum(axis=1).mean())
                nsim += 1
            for n in NS:
                w = topn_weights(px, n, band=LIVE_BAND, gross=g)
                raw[("TOPN", "P", g, n)] = tuple(x.loc[start:] for x in sim(px, w))
                mg[("TOPN", "P", g, n)] = float(w.loc[start:][is_mask].sum(axis=1).mean())
                nsim += 1
            # ARM M: finite-N rungs rescaled to the ALL book's IS mean deployed gross (IS-only)
            gall = mg[("TOPN", "P", g, "ALL")]
            for n in [x for x in NS if x != "ALL"]:
                c = gall / mg[("TOPN", "P", g, n)]
                w = topn_weights(px, n, band=LIVE_BAND, gross=g * c)
                raw[("TOPN", "M", g, n)] = tuple(x.loc[start:] for x in sim(px, w))
                mg[("TOPN", "M", g, n)] = float(w.loc[start:][is_mask].sum(axis=1).mean())
                nsim += 1
            raw[("TOPN", "M", g, "ALL")] = raw[("TOPN", "P", g, "ALL")]
            mg[("TOPN", "M", g, "ALL")] = gall
        for gg in GROSSES:                                  # the CONTROL dial (2264's ladder)
            w = rules_v2_weights(px, band=LIVE_BAND, gross=gg)
            raw[("GROSS", "P", None, gg)] = tuple(x.loc[start:] for x in sim(px, w))
            mg[("GROSS", "P", None, gg)] = float(w.loc[start:][is_mask].sum(axis=1).mean())
            nsim += 1

        # ---------------- GATES ---------------------------------------------------------------
        wlive = rules_v2_weights(px)
        g1a = float((rules_v2_weights(px, band=LIVE_BAND, gross=LIVE_GROSS) - wlive).abs().max().max())
        g1b = float((topn_weights(px, "ALL", band=LIVE_BAND, gross=LIVE_GROSS) - wlive).abs().max().max())
        rl_ref, to_ref = sim(px, wlive)
        r0L, toL = raw[("BAND", "P", 0.75, LIVE_BAND)]
        g1r = float((at_cost(r0L, toL, 10.0)
                     - at_cost(rl_ref.loc[start:], to_ref.loc[start:], 10.0)).abs().max())
        gate_rows.append(dict(panel=panel, gate="G1 b=0.03 and N=ALL ARE the live book",
                              stat_a=max(g1a, g1b), stat_b=g1r,
                              passed=bool(max(g1a, g1b) == 0.0 and g1r == 0.0)))

        g2a = at_cost(*raw[("TOPN", "P", 1.00, 20)], 25.0)
        g2b = backtest(px, topn_weights(px, 20, gross=1.00), cost_bps=25.0,
                       freq=FREQ)["returns"].loc[start:]
        g2 = float((g2a - g2b).abs().max())
        gate_rows.append(dict(panel=panel, gate="G2 derived cost == re-simulated",
                              stat_a=np.nan, stat_b=g2, passed=bool(g2 < 1e-15)))

        live10 = at_cost(*raw[("BAND", "P", 0.75, LIVE_BAND)], 10.0)
        one10 = at_cost(*raw[("GROSS", "P", None, 1.000)], 10.0)
        lc, ls, ld = m3(live10)
        lh1, lh2 = (metrics(x)["Sharpe"] for x in halves(live10))
        lo_c, lo_s, lo_d = m3(live10[oos_mask])
        oc, os_, od = m3(one10)
        ooc, oos_s, ood = m3(one10[oos_mask])
        sc_, ss_, sd_ = m3(spy_full)
        so_c, so_s, so_d = m3(spy_full[oos_mask])
        say(f"[{panel}] live RULES v2 @10bps  FULL {lc:.2%} / {ls:.4f} / {ld:.2%}   halves "
            f"{lh1:.4f} / {lh2:.4f}   OOS {lo_c:.2%} / {lo_s:.4f} / {lo_d:.2%}")
        say(f"[{panel}] gross 1.00   @10bps  FULL {oc:.2%} / {os_:.4f} / {od:.2%}"
            f"                         OOS {ooc:.2%} / {oos_s:.4f} / {ood:.2%}")
        say(f"[{panel}] SPY                   FULL {sc_:.2%} / {ss_:.4f} / {sd_:.2%}"
            f"                         OOS {so_c:.2%} / {so_s:.4f} / {so_d:.2%}")
        if panel == "u56":
            ref = [(lc, 0.0862), (ls, 1.2010), (ld, -0.1205), (lh1, 1.2276), (lh2, 1.1806),
                   (lo_c, 0.0946), (lo_s, 1.2767), (lo_d, -0.1205), (oc, 0.1153), (os_, 1.2009),
                   (od, -0.1591), (ooc, 0.1267), (oos_s, 1.2760), (ood, -0.1591),
                   (so_c, 0.1529), (so_s, 0.8751), (so_d, -0.3372)]
            d3 = max(abs(a - b) for a, b in ref)
            gate_rows.append(dict(panel=panel, gate="G3 idea 2264's committed cells reproduce",
                                  stat_a=d3, stat_b=np.nan, passed=bool(d3 < 5e-4)))

        # ---------------- the published book grid --------------------------------------------
        sh1, sh2 = (metrics(x)["Sharpe"] for x in halves(spy_full))
        LADDERS = ([("BAND", "P", g, BANDS) for g in GROSS_RUNGS]
                   + [("TOPN", "P", g, NS) for g in GROSS_RUNGS]
                   + [("TOPN", "M", g, NS) for g in GROSS_RUNGS]
                   + [("GROSS", "P", None, GROSSES)])
        for bps in COSTS:
            base_r = at_cost(*raw[("BAND", "P", 0.75, LIVE_BAND)], bps)      # 4a comparand
            b_h1, b_h2 = (metrics(x)["Sharpe"] for x in halves(base_r))
            b_dd = metrics(base_r)["MaxDD"]
            b_oos_s = metrics(base_r[oos_mask])["Sharpe"]
            b_oos_dd = metrics(base_r[oos_mask])["MaxDD"]
            for dial, arm, g, rungs in LADDERS:
                for v in rungs:
                    r0, to = raw[(dial, arm, g, v)]
                    r = at_cost(r0, to, bps)
                    h1, h2 = halves(r)
                    f = legs_4b(r, spy_full)
                    o = legs_4b(r[oos_mask], spy_full[oos_mask])
                    ic, ish, idd = m3(r[is_mask])
                    grid_rows.append(dict(
                        panel=panel, dial=dial, arm=arm, gross_rung=g, rung=str(v), cost_bps=bps,
                        CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                        H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                        IS_CAGR=ic, IS_Sharpe=ish, IS_MaxDD=idd,
                        OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                        mean_gross_IS=mg[(dial, arm, g, v)], turnover_yr=float(to.sum() / yrs),
                        L_DD_full=f["L_DD"], L_CAGR_full=f["L_CAGR"],
                        L_SHARPE_oos=o["L_SHARPE"], L_DD_oos=o["L_DD"], L_CAGR_oos=o["L_CAGR"],
                        pass_4b_full=bool(metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                                          and f["L_DD"] and f["L_CAGR"]),
                        pass_4b_oos=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"]),
                        pass_4a=bool(metrics(h1)["Sharpe"] > b_h1 and metrics(h2)["Sharpe"] > b_h2
                                     and f["MaxDD"] >= b_dd),
                        cap_full=f["cap"], floor_full=f["floor"], cap_oos=o["cap"],
                        floor_oos=o["floor"], base_MaxDD=b_dd, base_OOS_Sharpe=b_oos_s,
                        base_OOS_MaxDD=b_oos_dd))

        # ---------------- G6: saturation structure -------------------------------------------
        for dial, arm, g, rungs in LADDERS:
            dd = [metrics(at_cost(*raw[(dial, arm, g, v)], 10.0)[is_mask])["MaxDD"] for v in rungs]
            diffs = np.diff(dd)
            mono = bool(all(d <= 1e-12 for d in diffs))        # deeper (more negative) as rung rises
            # G6 is the run's PREMISE, asserted as a gate: IS MaxDD must be monotone on GROSS
            # (2264's dial, where the budget saturates) and must NOT be on BAND / TOPN (the
            # dials under test).  The gate passes when the structure is what the idea claims.
            want = (dial == "GROSS")
            gate_rows.append(dict(panel=panel,
                                  gate=f"G6 IS MaxDD monotone on {dial}/{arm}/g={g} "
                                       f"(expected {want})",
                                  stat_a=float(np.min(diffs)), stat_b=float(np.max(diffs)),
                                  passed=bool(mono == want)))

        # ---------------- THE CHOOSERS (IS 2009-2016 only) ------------------------------------
        spy_is_dd = metrics(spy_full[is_mask])["MaxDD"]
        for bps in COSTS:
            base_r = at_cost(*raw[("BAND", "P", 0.75, LIVE_BAND)], bps)
            b_h1, b_h2 = (metrics(x)["Sharpe"] for x in halves(base_r))
            b_dd = metrics(base_r)["MaxDD"]
            b_oos_s = metrics(base_r[oos_mask])["Sharpe"]
            b_oos_dd = metrics(base_r[oos_mask])["MaxDD"]
            for dial, arm, g, rungs in LADDERS:
                rs = {v: at_cost(*raw[(dial, arm, g, v)], bps) for v in rungs}
                is_dd = {v: metrics(rs[v][is_mask])["MaxDD"] for v in rungs}
                is_cg = {v: metrics(rs[v][is_mask])["CAGR"] for v in rungs}
                is_sh = {v: metrics(rs[v][is_mask])["Sharpe"] for v in rungs}
                is_cal = {v: metrics(rs[v][is_mask])["Calmar"] for v in rungs}
                oos_sh = {v: metrics(rs[v][oos_mask])["Sharpe"] for v in rungs}
                live_rung = {"BAND": LIVE_BAND, "TOPN": "ALL", "GROSS": LIVE_GROSS}[dial]
                unc_cagr = max(rungs, key=lambda v: is_cg[v])   # budget-free tie-break argmax
                unc_sh = max(rungs, key=lambda v: is_sh[v])

                picks = {}
                for k in KAPPAS:
                    ok = [v for v in rungs if is_dd[v] >= k * spy_is_dd]
                    picks[f"C_DDB_CAGR{k:.2f}"] = (max(ok, key=lambda v: is_cg[v]) if ok else None)
                    picks[f"C_DDB_SHARPE{k:.2f}"] = (max(ok, key=lambda v: is_sh[v]) if ok else None)
                picks["C_SHARPE"] = unc_sh
                picks["C_CALMAR"] = max(rungs, key=lambda v: is_cal[v])
                picks["C_LIVE"] = live_rung
                picks["ORACLE_OOS"] = max(rungs, key=lambda v: oos_sh[v])   # ILLEGAL yardstick
                best_oos = oos_sh[picks["ORACLE_OOS"]]

                for name, v in picks.items():
                    if v is None:
                        ch_rows.append(dict(panel=panel, dial=dial, arm=arm, gross_rung=g,
                                            cost_bps=bps, chooser=name, pick=None, abstain=True,
                                            kappa=float(name[-4:]), binds=np.nan))
                        continue
                    r = rs[v]
                    h1, h2 = halves(r)
                    f = legs_4b(r, spy_full)
                    o = legs_4b(r[oos_mask], spy_full[oos_mask])
                    kap = float(name[-4:]) if name.startswith("C_DDB") else np.nan
                    if name.startswith("C_DDB_CAGR"):
                        binds = bool(v != unc_cagr)
                    elif name.startswith("C_DDB_SHARPE"):
                        binds = bool(v != unc_sh)
                    else:
                        binds = np.nan
                    ch_rows.append(dict(
                        panel=panel, dial=dial, arm=arm, gross_rung=g, cost_bps=bps, chooser=name,
                        pick=str(v), abstain=False, kappa=kap, binds=binds,
                        at_ladder_end=bool(v == rungs[-1]), is_live_rung=bool(v == live_rung),
                        IS_MaxDD=is_dd[v], IS_SPY_MaxDD=spy_is_dd, IS_Sharpe=is_sh[v],
                        CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                        H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                        OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                        regret_OOS_Sharpe=float(oos_sh[v] - best_oos),
                        turnover_yr=float(raw[(dial, arm, g, v)][1].sum() / yrs),
                        mean_gross_IS=mg[(dial, arm, g, v)],
                        pass_4b_full=bool(metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                                          and f["L_DD"] and f["L_CAGR"]),
                        pass_4b_oos=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"]),
                        pass_4a_full=bool(metrics(h1)["Sharpe"] > b_h1 and metrics(h2)["Sharpe"] > b_h2
                                          and f["MaxDD"] >= b_dd),
                        pass_4a_oos=bool(o["Sharpe"] > b_oos_s and o["MaxDD"] >= b_oos_dd),
                        L_SHARPE_oos=o["L_SHARPE"], L_DD_oos=o["L_DD"], L_CAGR_oos=o["L_CAGR"],
                        cap_oos=o["cap"], floor_oos=o["floor"],
                        base_OOS_Sharpe=b_oos_s, base_OOS_MaxDD=b_oos_dd,
                        spy_OOS_Sharpe=metrics(spy_full[oos_mask])["Sharpe"]))

    D = pd.DataFrame(grid_rows)
    C = pd.DataFrame(ch_rows)

    # G4: the degeneracy control -- on GROSS, C_DDB_CAGR IS 2264's "largest gross inside budget"
    g4_bad = 0
    for panel in PANELS:
        sub = D[(D.panel == panel) & (D.dial == "GROSS")]
        for bps in COSTS:
            s = sub[sub.cost_bps == bps].set_index("rung")
            spy_is = C[(C.panel == panel) & (C.dial == "GROSS") & (C.cost_bps == bps)
                       & C.IS_SPY_MaxDD.notna()].IS_SPY_MaxDD.iloc[0]
            for k in KAPPAS:
                ok = [gg for gg in GROSSES if s.loc[str(gg), "IS_MaxDD"] >= k * spy_is]
                want = str(max(ok)) if ok else None
                row = C[(C.panel == panel) & (C.dial == "GROSS") & (C.cost_bps == bps)
                        & (C.chooser == f"C_DDB_CAGR{k:.2f}")]
                got = row.pick.iloc[0] if len(row) else "MISSING"
                if (want is None and not bool(row.abstain.iloc[0])) or \
                   (want is not None and got != want):
                    g4_bad += 1
    gate_rows.append(dict(panel="both", gate="G4 on GROSS, C_DDB_CAGR == 2264's largest-gross rule",
                          stat_a=float(g4_bad), stat_b=np.nan, passed=bool(g4_bad == 0)))

    n_books = len(PANELS) * len(COSTS) * (2 * len(BANDS) + 4 * len(NS) + len(GROSSES))
    n_ch = len(PANELS) * len(COSTS) * 7 * (2 * len(KAPPAS) + 4)
    gate_rows.append(dict(panel="both", gate="G5 all cells published", stat_a=float(len(D)),
                          stat_b=float(len(C)),
                          passed=bool(len(D) == n_books and len(C) == n_ch)))
    G = pd.DataFrame(gate_rows)

    say(f"\n# {nsim} book simulations run (zero-cost; every cost rung derived exactly, gate G2)")
    say("\n=== GATES (printed before any hypothesis is read) ===")
    say(G.to_string(index=False, float_format=lambda x: f"{x:.6g}"))
    say(f"GATES: {int(G.passed.sum())} of {len(G)} PASS   "
        f"(expected books {n_books}, got {len(D)}; expected choosers {n_ch}, got {len(C)})")

    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.choosers.csv", index=False)

    # ---------------------------------------------------- PART 1: the ladders, every cell
    say("\n=== PART 1 -- THE PUBLISHED LADDERS (10 bps headline rung, gross rung 1.00) ===")
    cols = ["rung", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_MaxDD", "IS_Sharpe", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "mean_gross_IS", "turnover_yr", "pass_4a", "pass_4b_full",
            "pass_4b_oos"]
    for panel in PANELS:
        for dial, arm, g in [("BAND", "P", 1.00), ("TOPN", "P", 1.00), ("TOPN", "M", 1.00),
                             ("GROSS", "P", None)]:
            sub = D[(D.panel == panel) & (D.dial == dial) & (D.arm == arm)
                    & (D.gross_rung.isna() if g is None else (D.gross_rung == g))
                    & (D.cost_bps == 10.0)]
            say(f"\n[{panel}] dial={dial} arm={arm} gross={g} @10bps   "
                f"4b FULL cap {sub.cap_full.iloc[0]:.4f} floor {sub.floor_full.iloc[0]:.4f} | "
                f"OOS cap {sub.cap_oos.iloc[0]:.4f} floor {sub.floor_oos.iloc[0]:.4f}")
            say(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n--- KEEP-path census over ALL published book cells ---")
    for dial in ["BAND", "TOPN", "GROSS"]:
        s = D[D.dial == dial]
        say(f"{dial:6s} n={len(s):4d}   4a {int(s.pass_4a.sum()):4d}   "
            f"4b FULL {int(s.pass_4b_full.sum()):4d}   4b OOS {int(s.pass_4b_oos.sum()):4d}   "
            f"4b FULL+OOS {int((s.pass_4b_full & s.pass_4b_oos).sum()):4d}")
    say(f"ALL    n={len(D):4d}   4a {int(D.pass_4a.sum()):4d}   "
        f"4b FULL {int(D.pass_4b_full.sum()):4d}   4b OOS {int(D.pass_4b_oos.sum()):4d}   "
        f"4b FULL+OOS {int((D.pass_4b_full & D.pass_4b_oos).sum()):4d}")

    # ---------------------------------------------------- PART 2: does the budget SATURATE?
    say("\n=== PART 2 -- DOES THE BUDGET SATURATE THE DIAL? (the premise, measured) ===")
    sat = []
    for dial in ["GROSS", "BAND", "TOPN"]:
        s = C[(C.dial == dial) & C.chooser.str.startswith("C_DDB_CAGR")]
        live = C[(C.dial == dial) & (C.chooser == "C_LIVE")]
        sat.append(dict(dial=dial, n=len(s), abstain=int(s.abstain.sum()),
                        at_ladder_end=float(s[~s.abstain].at_ladder_end.mean()),
                        budget_BINDS=float(s[~s.abstain].binds.mean()),
                        picks_live_rung=float(s[~s.abstain].is_live_rung.mean()),
                        distinct_picks=int(s[~s.abstain].pick.nunique())))
    S = pd.DataFrame(sat)
    say(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  at_ladder_end = the pick is the last rung (2264's degeneracy);  budget_BINDS = the "
        "budget moved the pick off its own budget-free argmax.")

    # ---------------------------------------------------- PART 3: does it BUY anything (rule 8)
    say("\n=== PART 3 -- RULE 8: WHAT EACH CHOOSER DELIVERS OUT OF SAMPLE (2017-2026, read once) ===")
    keep = ["C_DDB_CAGR0.60", "C_DDB_SHARPE0.60", "C_SHARPE", "C_CALMAR", "C_LIVE", "ORACLE_OOS"]
    for dial in ["GROSS", "BAND", "TOPN"]:
        s = C[(C.dial == dial) & C.chooser.isin(keep) & (~C.abstain)]
        agg = s.groupby("chooser").agg(
            n=("pick", "size"), OOS_Sharpe=("OOS_Sharpe", "median"),
            OOS_CAGR=("OOS_CAGR", "median"), OOS_MaxDD=("OOS_MaxDD", "median"),
            regret=("regret_OOS_Sharpe", "median"),
            reach_4b_oos=("pass_4b_oos", "sum"), reach_4b_full=("pass_4b_full", "sum"),
            reach_4a=("pass_4a_full", "sum")).reindex(keep)
        say(f"\n[{dial}] median over all panel x gross-rung x cost cells (ORACLE_OOS is ILLEGAL, "
            f"published as the regret yardstick only)")
        say(agg.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n--- the full kappa ladder, 4b-OOS reach and median regret, per dial ---")
    for dial in ["GROSS", "BAND", "TOPN"]:
        s = C[(C.dial == dial) & C.chooser.str.startswith("C_DDB")]
        t = s.groupby("chooser").agg(n=("chooser", "size"), abstain=("abstain", "sum"),
                                     reach_4b_oos=("pass_4b_oos", "sum"),
                                     reach_4b_full=("pass_4b_full", "sum"),
                                     reach_4a=("pass_4a_full", "sum"),
                                     regret=("regret_OOS_Sharpe", "median"),
                                     OOS_Sharpe=("OOS_Sharpe", "median"),
                                     OOS_MaxDD=("OOS_MaxDD", "median"))
        say(f"\n[{dial}]")
        say(t.to_string(float_format=lambda x: f"{x:.4f}"))

    # head-to-head against the two comparands that matter, cell by cell
    say("\n--- HEAD-TO-HEAD: C_DDB_CAGR0.60 minus C_SHARPE and minus C_LIVE, per cell ---")
    hh = []
    for dial in ["GROSS", "BAND", "TOPN"]:
        key = ["panel", "arm", "gross_rung", "cost_bps"]
        s = C[(C.dial == dial)].copy()
        s["gross_rung"] = s.gross_rung.fillna(-1.0)
        a = s[s.chooser == "C_DDB_CAGR0.60"].set_index(key)
        for comp in ["C_SHARPE", "C_LIVE"]:
            b = s[s.chooser == comp].set_index(key)
            j = a.join(b, rsuffix="_c", how="inner")
            j = j[~j.abstain]
            hh.append(dict(dial=dial, vs=comp, n=len(j),
                           dOOS_Sharpe=float((j.OOS_Sharpe - j.OOS_Sharpe_c).median()),
                           dOOS_MaxDD_pp=float(100 * (j.OOS_MaxDD - j.OOS_MaxDD_c).median()),
                           dOOS_CAGR_pp=float(100 * (j.OOS_CAGR - j.OOS_CAGR_c).median()),
                           win_OOS_Sharpe=float((j.OOS_Sharpe > j.OOS_Sharpe_c).mean()),
                           same_pick=float((j.pick == j.pick_c).mean()),
                           d_reach_4b_oos=int(j.pass_4b_oos.sum() - j.pass_4b_oos_c.sum())))
    H = pd.DataFrame(hh)
    say(H.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------- PART 4: KEEP candidates
    say("\n=== PART 4 -- KEEP PATHS ===")
    cand = C[(~C.abstain) & (C.chooser != "ORACLE_OOS") & C.pass_4b_full & C.pass_4b_oos]
    say(f"chooser-reachable cells clearing 4b FULL **and** OOS: {len(cand)}")
    if len(cand):
        say(cand[["panel", "dial", "arm", "gross_rung", "cost_bps", "chooser", "pick", "CAGR",
                  "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                  "turnover_yr", "pass_4a_full"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    a4 = C[(~C.abstain) & (C.chooser != "ORACLE_OOS") & C.pass_4a_full]
    say(f"\nchooser-reachable cells clearing 4a (both halves vs live RULES v2 + MaxDD no worse): "
        f"{len(a4)}")
    if len(a4):
        say(a4[["panel", "dial", "arm", "gross_rung", "cost_bps", "chooser", "pick", "CAGR",
                "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                "turnover_yr", "pass_4a_oos"]].head(40)
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------- PART 5: is kappa transferable?
    say("\n=== PART 5 -- IS THE BUDGET FRACTION KAPPA TRANSFERABLE ACROSS DIALS? ===")
    tr = []
    for tb in ["C_DDB_CAGR", "C_DDB_SHARPE"]:
        for dial in ["GROSS", "BAND", "TOPN"]:
            s = C[(C.dial == dial) & C.chooser.str.startswith(tb)]
            t = s.groupby("chooser").pass_4b_oos.sum()
            best = t.idxmax()
            tr.append(dict(tiebreak=tb, dial=dial, best_kappa=float(best[len(tb):]),
                           best_reach=int(t.max()), n_cells=int(len(s) // len(KAPPAS)),
                           reach_at_060=int(t.get(f"{tb}0.60", 0))))
    say(pd.DataFrame(tr).to_string(index=False))
    say("  (best_kappa = the kappa with the most 4b-OOS passes on that dial; reach_at_060 = what "
        "PROTOCOL 4b's own delta, the value 2264 shipped, delivers there.)")

    say("\n=== PART 6 -- DOES THE TIE-BREAK MATTER? (same-pick rate of the two readings of the "
        "SAME device) ===")
    tb_rows = []
    for dial in ["GROSS", "BAND", "TOPN"]:
        s = C[C.dial == dial].copy()
        s["gross_rung"] = s.gross_rung.fillna(-1.0)
        key = ["panel", "arm", "gross_rung", "cost_bps"]
        for k in KAPPAS:
            a = s[s.chooser == f"C_DDB_CAGR{k:.2f}"].set_index(key)
            b = s[s.chooser == f"C_DDB_SHARPE{k:.2f}"].set_index(key)
            j = a.join(b, rsuffix="_s", how="inner")
            j = j[(~j.abstain) & (~j.abstain_s)]
            tb_rows.append(dict(dial=dial, kappa=k, n=len(j),
                                same_pick=float((j["pick"].astype(str) == j.pick_s.astype(str)).mean()),
                                d_OOS_Sharpe=float((j.OOS_Sharpe - j.OOS_Sharpe_s).median())))
    say(pd.DataFrame(tb_rows).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\nwrote {STEM}.console.txt / .grid.csv / .choosers.csv")


if __name__ == "__main__":
    main()
