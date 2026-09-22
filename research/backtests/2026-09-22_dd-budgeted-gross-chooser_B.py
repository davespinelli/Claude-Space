#!/usr/bin/env python3
"""Idea 2264 (2026-09-22, lane B) -- DOES A DRAWDOWN-BUDGETED IS-ONLY GROSS CHOOSER MAKE THE
RECORD'S ONLY RELIABLE 4b PASSER RULE-8 REACHABLE?

WHY THIS RUN EXISTS
    Three independent runs agree on both halves of a contradiction nobody has resolved.

    (i)  The ONLY cells clearing PROTOCOL path 4b anywhere on this corpus are plain GROSS rungs
         of the LIVE symmetric band book.  Idea 2233 (cloud): "all 4 of the grid's 96 4b passes
         at 10 bps are GROSS passes at the untouched b = 0.03 band (U56 and B136, gross 1.00 and
         1.25); 0 come from the BIN or MATCH arms."  Idea 953 (cloud) found the same 4 of 84.
         Idea 2237 (C) found every b_out cell that clears 4b is STRICTLY DOMINATED by a gross
         cell, and priced gross as the CHEAPEST dial per pp of drawdown surrendered.

    (ii) Those cells are NOT rule-8 reachable, always for the same reason: IS Sharpe is gross-
         INVARIANT (U56 1.2010 -> 1.2000 over g = 0.25..1.50, flat to ~0.003), so the record's
         habitual IS-Sharpe chooser takes the ladder END g = 1.50 on every panel and blows the
         OOS DD cap (-23.38% / -23.75% / -22.79% against -20.23%).

    The chooser has never been matched to the leg that actually binds.  This run tests the
    obvious one: pick the LARGEST gross whose IN-SAMPLE MaxDD stays inside kappa x (IS SPY
    MaxDD) -- the 4b drawdown cap itself, computed on 2009-2016 alone.  It is legal (IS-only,
    no lookahead), it is what an allocator with a risk budget actually does, and drawdown is
    the one statistic gross is NOT invariant to.

THE BOOK
    `baseline.rules_v2_weights(px, band=0.03, gross=g)` -- the LIVE book, re-sized and nothing
    else.  Band 3%, weekly cadence, t+1 execution, gated-out weight to CASH (never re-spread).

THE GRID (every point published, pass or fail)
    GROSS g in {0.250 .. 1.500 step 0.125}                       -> 11 rungs
      x COST {0, 5, 10, 25, 50} bps  x  PANEL {u56, b136}        -> 110 published book rows
    CHOOSERS: C_DDB(kappa) for kappa in {0.40,0.50,0.60,0.70,0.80,0.90,1.00}; U_DDB(kappa), the
      SAME rule under PROTOCOL rule 2's no-leverage constraint g <= 1.00; and three comparands --
      C_SHARPE (the record's habitual), C_CALMAR, C_LIVE (fixed g = 0.75, the shipped default, a
      no-information control)                                    -> 170 published chooser rows
    ARM F: a flat financing charge of (g-1) x rate on every levered rung, rate in {0,2%,4%}/yr.
    ARM R: the REVERSED walk-forward (2017-2026 chooses, 2009-2016 read) -- a falsification test,
      because the forward run is flattered by tape order (IS SPY MaxDD -22.06% is SHALLOWER than
      OOS SPY's -33.72%, so an IS budget is automatically conservative out of sample).
      Both arms are REPORTED axes, never selected on.
    Two tuned dials and NO MORE: kappa and GROSS.  Cost rung, panel, band (3%) and cadence (W)
    are REPORTED axes, never selected on.

    COST IS DERIVED, NOT RE-SIMULATED.  `engine.backtest` subtracts `turnover * bps/1e4` from
    the return line and never feeds cost back into positions, so one zero-cost simulation per
    (panel, g) reproduces every cost rung EXACTLY.  Gate G6 checks this against a full re-run.

GATES (printed before any hypothesis is read)
    G1  g = 0.75 reproduces `baseline.rules_v2_weights` at max|dw| = 0 and its 10 bps return
        line at max|dr| = 0 on both panels.
    G2  the dial is pure sizing: w(g) = (g/0.75) * w(0.75) at max|dw| = 0, all 11 rungs.
    G3  the committed cells reproduce: live v2 U56 @10 bps = 8.62%/1.2010/-12.05% (halves
        1.2276/1.1806, OOS 9.46%/1.2767/-12.05%); U56 g=1.00 @10 bps = 11.53%/1.2009/-15.91%
        (OOS 12.67%/1.2760/-15.91%); SPY OOS 15.29%/0.8751/-33.72%.      [ideas 2233 / 2237]
    G4  IS MaxDD is monotone NON-INCREASING in g on both panels (the chooser is well defined).
    G5  every one of the 110 book cells and 170 chooser cells is published.
    G6  the derived cost ladder equals a full re-simulation at 25 bps to < 1e-15.

RULE 8 (PROTOCOL rule 8 -- walk-forward, 2017-2026 READ ONCE)
    Every chooser sees 2009-2016 ONLY.  The 2017-2026 leg is then read once and reported
    untouched against the live RULES v2 book's OOS and SPY's OOS.

CAVEATS carried
    LEVERAGE: rungs g > 1.00 are levered and the engine charges NO financing, borrow or margin
    cost for them.  The record's own gross ladder (idea 2233) runs to 1.50 so the ladder is kept
    for comparability, but every headline is also reported on the UNLEVERED sub-ladder g <= 1.00.
    SURVIVORSHIP (PROTOCOL rule 9 / idea 54): u56 and b136 are CURRENT constituents held from
    2008, so every CAGR level is optimistic and both 4b level legs are easier than on a
    point-in-time panel.  Costs are flat per unit turnover, no spread/impact/borrow.  One
    cadence (W), one delay (t+1), one band (3%).
    Deterministic, standalone.  Writes .console.txt, .grid.csv, .choosers.csv next to itself.
    Modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-22_dd-budgeted-gross-chooser_B"
OUT = ROOT / "research" / "backtests"

GROSSES = [0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000, 1.125, 1.250, 1.375, 1.500]
KAPPAS = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
PANELS = ["u56", "b136"]
BAND, LIVE_GROSS, FREQ = 0.03, 0.75, "W"
PHI, DELTA = 0.70, 0.60          # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers
OOS_START = "2017-01-01"         # rule 8: params chosen on 2009-2016, this leg read once

_LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ----------------------------------------------------------------------------- metrics helpers
def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def legs_4b(r, spy):
    """PROTOCOL 4b on ONE window: Sharpe > SPY, MaxDD >= DELTA*SPY_DD, CAGR >= PHI*SPY_CAGR."""
    c, s, d = m3(r)
    cs, ss, ds = m3(spy)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, L_SHARPE=s > ss, L_DD=d >= DELTA * ds,
                L_CAGR=c >= PHI * cs, cap=DELTA * ds, floor=PHI * cs)


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


# ----------------------------------------------------------------------------- simulation core
def sim(px, weights):
    """One zero-cost simulation; returns (gross return line, turnover line)."""
    res = backtest(px, weights, cost_bps=0.0, freq=FREQ)
    return res["returns"], res["turnover"]


def at_cost(r0, to, bps):
    return r0 - to * bps / 1e4


def main():
    say(f"# {STEM}")
    say("# idea 2264 -- a DD-BUDGETED IS-only gross chooser on the live RULES v2 band book")
    say(f"# grosses={GROSSES}\n# kappas={KAPPAS}\n# costs={COSTS} bps  panels={PANELS}"
        f"  band={BAND}  cadence={FREQ}  t+1")
    say("")

    gate_rows, grid_rows, ch_rows = [], [], []

    for panel in PANELS:
        px = load_universe(broad=(panel == "b136"))
        start = px.index[260]                                   # baseline.compare's warm-up
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        idx = spy_full.index
        is_mask = idx < pd.Timestamp(OOS_START)
        oos_mask = ~is_mask

        # ---- simulate every gross rung once, at zero cost
        raw = {}
        for g in GROSSES:
            w = rules_v2_weights(px, band=BAND, gross=g)
            r0, to = sim(px, w)
            raw[g] = (r0.loc[start:], to.loc[start:])

        # ---- GATES -------------------------------------------------------------------------
        w75 = rules_v2_weights(px, band=BAND, gross=LIVE_GROSS)
        wlive = rules_v2_weights(px)                            # library default gross=0.75
        g1w = float((w75 - wlive).abs().max().max())
        r0_live, to_live = raw[LIVE_GROSS]
        rl_ref, to_ref = sim(px, wlive)
        g1r = float((at_cost(r0_live, to_live, 10.0) - at_cost(rl_ref.loc[start:], to_ref.loc[start:], 10.0)).abs().max())
        gate_rows.append(dict(panel=panel, gate="G1 g=0.75 IS the live book", stat_w=g1w, stat_r=g1r,
                              passed=bool(g1w == 0.0 and g1r == 0.0)))

        g2 = max(float((rules_v2_weights(px, band=BAND, gross=g) - (g / LIVE_GROSS) * w75).abs().max().max())
                 for g in GROSSES)
        gate_rows.append(dict(panel=panel, gate="G2 gross is pure sizing", stat_w=g2, stat_r=np.nan,
                              passed=bool(g2 < 1e-15)))

        g6a = at_cost(raw[1.0][0], raw[1.0][1], 25.0)
        g6b = backtest(px, rules_v2_weights(px, band=BAND, gross=1.0), cost_bps=25.0, freq=FREQ)["returns"].loc[start:]
        g6 = float((g6a - g6b).abs().max())
        gate_rows.append(dict(panel=panel, gate="G6 derived cost == re-simulated", stat_w=np.nan,
                              stat_r=g6, passed=bool(g6 < 1e-15)))

        # ---- the comparands the whole run is scored against --------------------------------
        live10 = at_cost(r0_live, to_live, 10.0)
        lc, ls, ld = m3(live10)
        lh1, lh2 = (metrics(x)["Sharpe"] for x in halves(live10))
        lo_c, lo_s, lo_d = m3(live10[oos_mask])
        sc, ss_, sd = m3(spy_full)
        so_c, so_s, so_d = m3(spy_full[oos_mask])
        one10 = at_cost(*raw[1.000], 10.0)
        oc, os_, od = m3(one10)
        ooc, oos_s, ood = m3(one10[oos_mask])
        say(f"[{panel}] live RULES v2 @10bps  FULL {lc:.2%} / {ls:.4f} / {ld:.2%}   halves "
            f"{lh1:.4f} / {lh2:.4f}   OOS {lo_c:.2%} / {lo_s:.4f} / {lo_d:.2%}")
        say(f"[{panel}] gross 1.00   @10bps  FULL {oc:.2%} / {os_:.4f} / {od:.2%}"
            f"                        OOS {ooc:.2%} / {oos_s:.4f} / {ood:.2%}")
        say(f"[{panel}] SPY                   FULL {sc:.2%} / {ss_:.4f} / {sd:.2%}"
            f"                        OOS {so_c:.2%} / {so_s:.4f} / {so_d:.2%}")

        if panel == "u56":
            ref = dict(live=(0.0862, 1.2010, -0.1205, 1.2276, 1.1806, 0.0946, 1.2767, -0.1205),
                       one=(0.1153, 1.2009, -0.1591, 0.1267, 1.2760, -0.1591),
                       spy_oos=(0.1529, 0.8751, -0.3372))
            d1 = max(abs(lc - ref["live"][0]), abs(ls - ref["live"][1]), abs(ld - ref["live"][2]),
                     abs(lh1 - ref["live"][3]), abs(lh2 - ref["live"][4]), abs(lo_c - ref["live"][5]),
                     abs(lo_s - ref["live"][6]), abs(lo_d - ref["live"][7]))
            d2 = max(abs(oc - ref["one"][0]), abs(os_ - ref["one"][1]), abs(od - ref["one"][2]),
                     abs(ooc - ref["one"][3]), abs(oos_s - ref["one"][4]), abs(ood - ref["one"][5]))
            d3 = max(abs(so_c - ref["spy_oos"][0]), abs(so_s - ref["spy_oos"][1]), abs(so_d - ref["spy_oos"][2]))
            gate_rows.append(dict(panel=panel, gate="G3 committed cells reproduce",
                                  stat_w=max(d1, d2, d3), stat_r=np.nan,
                                  passed=bool(max(d1, d2, d3) < 5e-4)))

        # ---- the published book grid --------------------------------------------------------
        for bps in COSTS:
            base_r = at_cost(r0_live, to_live, bps)             # live v2 at THIS cost = 4a comparand
            b_h1, b_h2 = (metrics(x)["Sharpe"] for x in halves(base_r))
            b_dd = metrics(base_r)["MaxDD"]
            b_oos = metrics(base_r[oos_mask])["Sharpe"]
            for g in GROSSES:
                r = at_cost(*raw[g], bps)
                h1, h2 = halves(r)
                f = legs_4b(r, spy_full)
                o = legs_4b(r[oos_mask], spy_full[oos_mask])
                sh1, sh2 = (metrics(x)["Sharpe"] for x in halves(spy_full))
                p4b_full = (metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                            and f["L_DD"] and f["L_CAGR"])
                p4b_oos = o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"]
                p4a = (metrics(h1)["Sharpe"] > b_h1 and metrics(h2)["Sharpe"] > b_h2
                       and f["MaxDD"] >= b_dd)
                ic, isharpe, idd = m3(r[is_mask])
                grid_rows.append(dict(
                    panel=panel, cost_bps=bps, gross=g,
                    CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                    H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                    IS_CAGR=ic, IS_Sharpe=isharpe, IS_MaxDD=idd,
                    OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                    turnover_yr=float(raw[g][1].sum() / (len(r) / 252)),
                    L_DD_full=f["L_DD"], L_CAGR_full=f["L_CAGR"],
                    L_SHARPE_oos=o["L_SHARPE"], L_DD_oos=o["L_DD"], L_CAGR_oos=o["L_CAGR"],
                    pass_4b_full=p4b_full, pass_4b_oos=p4b_oos, pass_4a=p4a,
                    base_Sharpe=metrics(base_r)["Sharpe"], base_OOS_Sharpe=b_oos,
                    cap_full=f["cap"], floor_full=f["floor"], cap_oos=o["cap"], floor_oos=o["floor"]))

        # ---- G4: IS MaxDD monotone in gross ------------------------------------------------
        isdd = [metrics(at_cost(*raw[g], 10.0)[is_mask])["MaxDD"] for g in GROSSES]
        mono = all(isdd[i + 1] <= isdd[i] + 1e-12 for i in range(len(isdd) - 1))
        gate_rows.append(dict(panel=panel, gate="G4 IS MaxDD monotone in gross",
                              stat_w=float(np.min(np.diff(isdd))), stat_r=float(np.max(np.diff(isdd))),
                              passed=bool(mono)))

        # ---- THE CHOOSERS (IS 2009-2016 only) ----------------------------------------------
        for bps in COSTS:
            rs = {g: at_cost(*raw[g], bps) for g in GROSSES}
            is_dd = {g: metrics(rs[g][is_mask])["MaxDD"] for g in GROSSES}
            is_sh = {g: metrics(rs[g][is_mask])["Sharpe"] for g in GROSSES}
            is_cal = {g: metrics(rs[g][is_mask])["Calmar"] for g in GROSSES}
            spy_is_dd = metrics(spy_full[is_mask])["MaxDD"]

            picks = {}
            for k in KAPPAS:
                ok = [g for g in GROSSES if is_dd[g] >= k * spy_is_dd]
                picks[f"C_DDB{k:.2f}"] = (max(ok) if ok else np.nan)
            for k in KAPPAS:
                ok = [g for g in GROSSES if is_dd[g] >= k * spy_is_dd and g <= 1.0]
                picks[f"U_DDB{k:.2f}"] = (max(ok) if ok else np.nan)
            picks["C_SHARPE"] = max(GROSSES, key=lambda g: is_sh[g])
            picks["C_CALMAR"] = max(GROSSES, key=lambda g: is_cal[g])
            picks["C_LIVE"] = LIVE_GROSS

            base_r = at_cost(r0_live, to_live, bps)
            b_h1, b_h2 = (metrics(x)["Sharpe"] for x in halves(base_r))
            b_dd, b_oos = metrics(base_r)["MaxDD"], metrics(base_r[oos_mask])["Sharpe"]
            b_oos_dd = metrics(base_r[oos_mask])["MaxDD"]
            sh1, sh2 = (metrics(x)["Sharpe"] for x in halves(spy_full))

            for name, g in picks.items():
                if not (isinstance(g, float) and g == g):
                    ch_rows.append(dict(panel=panel, cost_bps=bps, chooser=name, pick=np.nan,
                                        abstain=True))
                    continue
                r = rs[g]
                h1, h2 = halves(r)
                f, o = legs_4b(r, spy_full), legs_4b(r[oos_mask], spy_full[oos_mask])
                ch_rows.append(dict(
                    panel=panel, cost_bps=bps, chooser=name, pick=g, abstain=False,
                    IS_MaxDD=is_dd[g], IS_budget=k if name.startswith("C_DDB") else np.nan,
                    IS_SPY_MaxDD=spy_is_dd,
                    CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                    H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                    OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                    turnover_yr=float(raw[g][1].sum() / (len(r) / 252)),
                    pass_4b_full=bool(metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                                      and f["L_DD"] and f["L_CAGR"]),
                    pass_4b_oos=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"]),
                    pass_4a_full=bool(metrics(h1)["Sharpe"] > b_h1 and metrics(h2)["Sharpe"] > b_h2
                                      and f["MaxDD"] >= b_dd),
                    pass_4a_oos=bool(o["Sharpe"] > b_oos and o["MaxDD"] >= b_oos_dd),
                    L_SHARPE_oos=o["L_SHARPE"], L_DD_oos=o["L_DD"], L_CAGR_oos=o["L_CAGR"],
                    cap_oos=o["cap"], floor_oos=o["floor"],
                    base_OOS_Sharpe=b_oos, base_OOS_MaxDD=b_oos_dd,
                    spy_OOS_Sharpe=metrics(spy_full[oos_mask])["Sharpe"]))

    G = pd.DataFrame(gate_rows)
    D = pd.DataFrame(grid_rows)
    C = pd.DataFrame(ch_rows)
    gate_rows.append(dict(panel="both", gate="G5 all cells published", stat_w=len(D), stat_r=len(C),
                          passed=bool(len(D) == len(PANELS) * len(COSTS) * len(GROSSES)
                                      and len(C) == len(PANELS) * len(COSTS) * (2 * len(KAPPAS) + 3))))
    G = pd.DataFrame(gate_rows)

    say("\n=== GATES (printed before any hypothesis is read) ===")
    say(G.to_string(index=False))
    say(f"GATES: {int(G.passed.sum())} of {len(G)} PASS")

    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    C.to_csv(OUT / f"{STEM}.choosers.csv", index=False)

    # ---------------------------------------------------------------- PART 1: the book ladder
    say("\n=== PART 1 -- THE GROSS LADDER, EVERY PUBLISHED CELL (10 bps headline rung) ===")
    for panel in PANELS:
        sub = D[(D.panel == panel) & (D.cost_bps == 10.0)]
        say(f"\n[{panel}] 10 bps")
        say(sub[["gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_MaxDD", "OOS_CAGR",
                 "OOS_Sharpe", "OOS_MaxDD", "turnover_yr", "pass_4a", "pass_4b_full",
                 "pass_4b_oos"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say(f"     4b FULL cap {sub.cap_full.iloc[0]:.4f}  floor {sub.floor_full.iloc[0]:.4f}"
            f"   |   4b OOS cap {sub.cap_oos.iloc[0]:.4f}  floor {sub.floor_oos.iloc[0]:.4f}")

    say("\n--- KEEP-path census over all 110 published book cells ---")
    say(f"4a           : {int(D.pass_4a.sum())} of {len(D)}")
    say(f"4b FULL      : {int(D.pass_4b_full.sum())} of {len(D)}")
    say(f"4b OOS       : {int(D.pass_4b_oos.sum())} of {len(D)}")
    unlev = D[D.gross <= 1.0]
    say(f"unlevered only (g <= 1.00, {len(unlev)} cells): 4a {int(unlev.pass_4a.sum())}, "
        f"4b FULL {int(unlev.pass_4b_full.sum())}, 4b OOS {int(unlev.pass_4b_oos.sum())}")
    fails = D[~D.pass_4b_full]
    say(f"binding leg over the {len(fails)} 4b-FULL fails: CAGR floor {int((~fails.L_CAGR_full).sum())}, "
        f"DD cap {int((~fails.L_DD_full).sum())}")
    fo = D[~D.pass_4b_oos]
    say(f"binding leg over the {len(fo)} 4b-OOS  fails: CAGR floor {int((~fo.L_CAGR_oos).sum())}, "
        f"DD cap {int((~fo.L_DD_oos).sum())}, Sharpe {int((~fo.L_SHARPE_oos).sum())}")

    # ------------------------------------------------------- PART 2: rule 8, the chooser test
    say("\n=== PART 2 -- RULE 8: 2009-2016 CHOOSES, 2017-2026 READ ONCE ===")
    for panel in PANELS:
        for bps in COSTS:
            sub = C[(C.panel == panel) & (C.cost_bps == bps)]
            say(f"\n[{panel}] {bps:.0f} bps   (IS SPY MaxDD {sub.IS_SPY_MaxDD.dropna().iloc[0]:.4f})")
            say(sub[["chooser", "pick", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                     "turnover_yr", "pass_4b_oos", "pass_4b_full", "pass_4a_full", "pass_4a_oos"]]
                .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n--- CHOOSER SCOREBOARD (reachability is the whole question) ---")
    fam = C.assign(family=C.chooser.str.replace(r"\d.*", "", regex=True))
    for name, sub in C.groupby("chooser"):
        n = len(sub)
        say(f"{name:>12}: 4b OOS {int(sub.pass_4b_oos.fillna(False).sum())}/{n}   "
            f"4b FULL {int(sub.pass_4b_full.fillna(False).sum())}/{n}   "
            f"4a FULL {int(sub.pass_4a_full.fillna(False).sum())}/{n}   "
            f"4a OOS {int(sub.pass_4a_oos.fillna(False).sum())}/{n}   "
            f"picks {sorted(set(sub.pick.dropna()))}   "
            f"median OOS Sharpe {sub.OOS_Sharpe.median():.4f}")

    ddb = C[C.chooser.str.startswith("C_DDB")]
    say(f"\nC_DDB family pooled: 4b OOS {int(ddb.pass_4b_oos.fillna(False).sum())} of {len(ddb)}, "
        f"4a FULL {int(ddb.pass_4a_full.fillna(False).sum())} of {len(ddb)}, "
        f"abstentions {int(ddb.abstain.sum())}")
    hab = C[C.chooser == "C_SHARPE"]
    say(f"C_SHARPE (habitual): 4b OOS {int(hab.pass_4b_oos.fillna(False).sum())} of {len(hab)}, "
        f"picks {sorted(set(hab.pick.dropna()))}")

    # ------------------------------------------- ARM F: financing charge on the levered picks
    say("\n=== ARM F -- WHAT LEVERAGE ACTUALLY COSTS (reported axis, not tuned) ===")
    say("The engine charges NO financing on g > 1.00.  Re-read each levered pick with a flat")
    say("annual charge of (g - 1) x rate on the borrowed fraction, rate in {0, 2%, 4%}/yr.")
    fin_rows = []
    for panel in PANELS:
        pxp = load_universe(broad=(panel == "b136"))
        startp = pxp.index[260]
        spyp = pxp["SPY"].pct_change().fillna(0.0).loc[startp:]
        oosm = spyp.index >= pd.Timestamp(OOS_START)
        for g in [g for g in GROSSES if g > 1.0]:
            w = rules_v2_weights(pxp, band=BAND, gross=g)
            r0, to = sim(pxp, w)
            r0, to = r0.loc[startp:], to.loc[startp:]
            for rate in (0.0, 0.02, 0.04):
                r = at_cost(r0, to, 10.0) - (g - 1.0) * rate / 252.0
                o = legs_4b(r[oosm], spyp[oosm])
                fin_rows.append(dict(panel=panel, gross=g, rate=rate, OOS_CAGR=o["CAGR"],
                                     OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                                     pass_4b_oos=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"])))
    F = pd.DataFrame(fin_rows)
    F.to_csv(OUT / f"{STEM}.financing.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for rate in (0.0, 0.02, 0.04):
        s = F[F.rate == rate]
        say(f"  financing {rate:.0%}/yr: 4b OOS {int(s.pass_4b_oos.sum())} of {len(s)} levered rungs")

    # --------------------------------------- ARM R: reversed walk-forward (falsification test)
    say("\n=== ARM R -- REVERSED WALK-FORWARD (2017-2026 chooses, 2009-2016 read) ===")
    say("The forward test is flattered by tape order: IS SPY MaxDD is SHALLOWER than OOS SPY's,")
    say("so an IS budget is conservative out of sample.  Reverse the windows to see whether the")
    say("device survives when the BUDGET window is the violent one.  Reported, never selected on.")
    rev_rows = []
    for panel in PANELS:
        pxp = load_universe(broad=(panel == "b136"))
        startp = pxp.index[260]
        spyp = pxp["SPY"].pct_change().fillna(0.0).loc[startp:]
        am = spyp.index >= pd.Timestamp(OOS_START)      # the CHOOSING window now
        bm = ~am                                         # the READ window now
        rawp = {}
        for g in GROSSES:
            w = rules_v2_weights(pxp, band=BAND, gross=g)
            r0, to = sim(pxp, w)
            rawp[g] = (r0.loc[startp:], to.loc[startp:])
        spy_a_dd = metrics(spyp[am])["MaxDD"]
        for bps in COSTS:
            rs = {g: at_cost(*rawp[g], bps) for g in GROSSES}
            dda = {g: metrics(rs[g][am])["MaxDD"] for g in GROSSES}
            for k in KAPPAS:
                ok = [g for g in GROSSES if dda[g] >= k * spy_a_dd]
                pick = max(ok) if ok else np.nan
                if pick != pick:
                    rev_rows.append(dict(panel=panel, cost_bps=bps, kappa=k, pick=np.nan,
                                         pass_4b_read=False)); continue
                o = legs_4b(rs[pick][bm], spyp[bm])
                rev_rows.append(dict(panel=panel, cost_bps=bps, kappa=k, pick=pick,
                                     READ_CAGR=o["CAGR"], READ_Sharpe=o["Sharpe"],
                                     READ_MaxDD=o["MaxDD"], cap=o["cap"], floor=o["floor"],
                                     L_SHARPE=o["L_SHARPE"], L_DD=o["L_DD"], L_CAGR=o["L_CAGR"],
                                     pass_4b_read=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"])))
            pick_s = max(GROSSES, key=lambda g: metrics(rs[g][am])["Sharpe"])
            o = legs_4b(rs[pick_s][bm], spyp[bm])
            rev_rows.append(dict(panel=panel, cost_bps=bps, kappa=np.nan, pick=pick_s,
                                 READ_CAGR=o["CAGR"], READ_Sharpe=o["Sharpe"], READ_MaxDD=o["MaxDD"],
                                 cap=o["cap"], floor=o["floor"], L_SHARPE=o["L_SHARPE"],
                                 L_DD=o["L_DD"], L_CAGR=o["L_CAGR"],
                                 pass_4b_read=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"])))
    R = pd.DataFrame(rev_rows)
    R.to_csv(OUT / f"{STEM}.reversed.csv", index=False)
    say(f"choosing-window SPY MaxDD {spy_a_dd:.4f} vs read-window "
        f"{metrics(spyp[bm])['MaxDD']:.4f}  (forward run: IS -0.2206, OOS -0.3372)")
    say(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for k in KAPPAS:
        s = R[R.kappa == k]
        say(f"  reversed kappa {k:.2f}: 4b on the read window {int(s.pass_4b_read.sum())} of {len(s)}, "
            f"picks {sorted(set(s.pick.dropna()))}")
    sfail = R[~R.pass_4b_read]
    say(f"  reversed binding leg over {len(sfail)} fails: CAGR floor {int((~sfail.L_CAGR.fillna(False)).sum())}, "
        f"DD cap {int((~sfail.L_DD.fillna(False)).sum())}, Sharpe {int((~sfail.L_SHARPE.fillna(False)).sum())}")

    say("\n--- THE ANSWER ---")
    reach = ddb[ddb.pass_4b_oos.fillna(False)]
    if len(reach):
        say(f"REACHABLE: {len(reach)} of {len(ddb)} C_DDB cells clear 4b OOS.")
        say(reach[["panel", "cost_bps", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                   "pass_4b_full", "pass_4a_full"]].to_string(index=False,
                                                              float_format=lambda x: f"{x:.4f}"))
    else:
        say("NOT REACHABLE: 0 of "
            f"{len(ddb)} C_DDB cells clear 4b OOS.")
    both = ddb[ddb.pass_4b_oos.fillna(False) & ddb.pass_4b_full.fillna(False)]
    say(f"C_DDB cells clearing 4b in FULL *and* OOS: {len(both)} of {len(ddb)}")
    ul = ddb[(ddb.pick <= 1.0)]
    say(f"C_DDB cells whose pick is UNLEVERED (g <= 1.00): {len(ul)} of {len(ddb)}; "
        f"of those, 4b OOS {int(ul.pass_4b_oos.fillna(False).sum())}")
    udb = C[C.chooser.str.startswith("U_DDB")]
    say(f"\nU_DDB (the SAME chooser with PROTOCOL rule 2's no-leverage constraint, g <= 1.00): "
        f"4b OOS {int(udb.pass_4b_oos.fillna(False).sum())} of {len(udb)}, "
        f"4b FULL {int(udb.pass_4b_full.fillna(False).sum())} of {len(udb)}, "
        f"4a FULL {int(udb.pass_4a_full.fillna(False).sum())} of {len(udb)}")
    for name, sub in udb.groupby("chooser"):
        say(f"  {name}: 4b OOS {int(sub.pass_4b_oos.fillna(False).sum())}/{len(sub)}  "
            f"picks {sorted(set(sub.pick.dropna()))}")
    say(udb[udb.pass_4b_oos.fillna(False)][["panel", "cost_bps", "chooser", "pick", "CAGR",
        "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover_yr"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\nwrote {STEM}.grid.csv ({len(D)} rows), {STEM}.choosers.csv ({len(C)} rows), "
        f"{STEM}.console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
