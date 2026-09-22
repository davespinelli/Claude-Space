#!/usr/bin/env python3
"""Idea 2260 (2026-09-22, lane C) -- DOES A VOLATILITY-TARGETED GROSS CLEAR 4b WHERE A
CONSTANT GROSS ONLY DOES AT g = 1.00, AND DOES IT BUY THE DRAWDOWN LEG MORE CHEAPLY?

WHY THIS RUN EXISTS
    The record's only reliable PROTOCOL-4b passers are CONSTANT gross rungs of the LIVE
    RULES v2 band book (ideas 2233 / 953 / 2237: g = 1.00 and 1.25 on U56 and B136, and
    2264 made g = 1.00 rule-8 reachable with a drawdown-budgeted IS-only chooser).  Idea
    2237 priced gross as the CHEAPEST dial per pp of drawdown surrendered (R_DD 1.324 vs
    b_out 2.380).  But a CONSTANT gross spends the drawdown budget UNIFORMLY across calm
    and violent tape.  A trailing-realised-vol target spends it where it is cheap.

    The question this run answers is therefore NOT "does a vol target pass 4b" (idea 794
    and the 2026-09-20 `voltgt` memos already price vol targets, on an equal-weight panel
    book without the band).  It is the MATCHED question the record has never asked on the
    band book: at the SAME CAGR as a constant-gross rung, is the vol-targeted book's
    MaxDD SHALLOWER -- i.e. does it clear 4b with MORE margin on the DD leg?

THE BOOK UNDER TEST
    Base  W_base_t = `baseline.rules_v2_weights(px, band=0.03, gross=1.00)` -- the LIVE
          book at unit gross, band 3% FROZEN (not a dial), weekly cadence, t+1 execution,
          gated-out weight to CASH and never re-spread.
    Risk proxy (no costs, no lookahead): u_t = the gross-of-cost daily return line of that
          base book; sigma_t = std(u_{t-L+1..t}) * sqrt(252), information through close t.
    Scaler  s_t = clip(TARGET / sigma_t, 0, CAP).  Before L observations of u exist,
          s_t = 0.75 (the live gross, a no-information default).
    Book    W_t = W_base_t * s_t, decided at close t, executed t+1, every change charged.

TUNED PARAMETERS -- EXACTLY TWO (PROTOCOL rule 4)
    1. TARGET in {0.06, 0.08, 0.10, 0.12, 0.15, 0.20}      annualised vol target
    2. CAP    in {0.75, 1.00, 1.25, 1.50}                  hard gross cap
    REPORTED AXES, never selected on: LOOKBACK L in {20, 63, 126} (headline L = 20, the
    `sigma_20` convention of the committed 2026-09-20 voltgt memo), COST in {0,5,10,25,50}
    bps, PANEL in {u56, b136}, the band (0.03) and the cadence (W).

THE GRID (every point published, pass or fail)
    VOL-TARGET BOOK  2 panels x 3 lookbacks x 6 targets x 4 caps x 5 cost rungs = 720 rows
    CONSTANT-GROSS LADDER  g in {0.250 .. 1.500 step 0.125} x 2 panels x 5 costs = 110 rows
    MATCHED-CAGR PAIRS     one per vol-target row that lies inside the ladder's CAGR range
    CHOOSERS (rule 8)      4 IS-only choosers x 2 panels x 3 lookbacks x 5 costs = 120 rows

    COST IS DERIVED, NOT RE-SIMULATED: `engine.backtest` subtracts `turnover * bps/1e4`
    from the return line and never feeds cost back into positions, so ONE zero-cost
    simulation per (panel, L, TARGET, CAP) reproduces every cost rung exactly.  Gate G5
    checks this against a full re-simulation at 25 bps.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    H1 EXISTENCE : some (TARGET, CAP) cell clears all four 4b legs on the FULL sample AND
                   all three on the rule-8 OOS window, on U56 at 10 bps.
    H2 CHEAPER-DD: among the cells that clear 4b, at least one has MaxDD strictly SHALLOWER
                   than the constant-gross rung MATCHED on full-sample CAGR (dDD > 0).
                   This is the idea's own claim.  Falsified if dDD <= 0 everywhere.
    H3 MORE-MARGIN-THAN-g1: some 4b-passing cell has CAGR >= the g = 1.00 rung's AND a
                   strictly larger 4b DD margin (MaxDD - 0.60 x SPY MaxDD) than g = 1.00.
                   This is the idea's question in its literal wording.
    H4 RULE 8    : an IS-only chooser (2009-2016 alone) over the 24-cell (TARGET, CAP) grid
                   reaches a cell that clears 4b on 2017-2026 read once.
    H5 4a        : any cell beats the live RULES v2 book's Sharpe in BOTH halves with MaxDD
                   no worse.  (The record says no; stated so the test is not silent.)

GATES (printed before any hypothesis is read)
    G1 constant gross 0.75 reproduces `baseline.rules_v2_weights` at max|dw| = 0 and its
       10 bps return line at max|dr| = 0, on both panels.
    G2 DEGENERATE LIMIT: at TARGET = 10.0 the scaler pins to CAP, so the vol-target book
       equals the constant-gross book at g = CAP on every date where sigma_t is defined.
    G3 COMMITTED CELLS REPRODUCE (ideas 2233 / 2237 / 2264): U56 live RULES v2 @10 bps
       8.62% / 1.2010 / -12.05% (halves 1.2276 / 1.1806, OOS 9.46% / 1.2767 / -12.05%);
       U56 g = 1.00 @10 bps 11.53% / 1.2009 / -15.91% (OOS 12.67% / 1.2760 / -15.91%);
       SPY OOS 15.29% / 0.8751 / -33.72%.
    G4 NO LOOKAHEAD: sigma_t recomputed from a return line truncated at t equals the
       full-sample sigma_t, on 5 pre-chosen dates x 3 lookbacks.
    G5 the derived cost ladder equals a full re-simulation at 25 bps to < 1e-15.
    G6 every one of the 720 book / 110 ladder / 120 chooser rows is published.
    G7 the constant-gross ladder's FULL CAGR is strictly increasing in g (so the
       matched-CAGR inversion is well defined); min consecutive difference reported.

RULE 8 (PROTOCOL rule 8 -- walk-forward, 2017-2026 READ ONCE)
    Every chooser sees 2009-2016 ONLY: C_SHARPE (max IS Sharpe, the record's habitual),
    C_CALMAR (max IS Calmar), C_DDB060 (max IS CAGR among cells whose IS MaxDD stays inside
    0.60 x IS SPY MaxDD -- PROTOCOL 4b's own delta, the chooser idea 2264 certified) and
    C_LIVE (fixed TARGET = 0.10, CAP = 1.00, the committed memo's convention, a
    no-information control).  kappa = 0.60 is NOT tuned here; it is taken from PROTOCOL 4b.

CAVEATS CARRIED
    LEVERAGE: CAP rungs above 1.00 are levered and the engine charges NO financing, borrow
    or margin cost.  Every headline is therefore ALSO reported on the unlevered sub-grid
    CAP <= 1.00, which is what PROTOCOL rule 2 permits.
    SURVIVORSHIP (PROTOCOL rule 9 / idea 54): u56 and b136 are CURRENT constituents held
    from 2008, so every CAGR level is optimistic and both 4b level legs are easier than on
    a point-in-time panel.  Costs are flat per unit turnover: no spread, impact or borrow.
    One cadence (W), one delay (t+1), one band (3%).
    Deterministic, standalone.  Writes .console.txt, .grid.csv, .ladder.csv, .matched.csv,
    .choosers.csv, .gates.csv next to itself.  Modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-22_voltgt-gross-vs-constant-gross-at-matched-CAGR_C"
OUT = ROOT / "research" / "backtests"

TARGETS = [0.06, 0.08, 0.10, 0.12, 0.15, 0.20]
CAPS = [0.75, 1.00, 1.25, 1.50]
LOOKBACKS = [20, 63, 126]
GROSSES = [0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000, 1.125, 1.250, 1.375, 1.500]
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
PANELS = ["u56", "b136"]
BAND, LIVE_GROSS, FREQ = 0.03, 0.75, "W"
PHI, DELTA = 0.70, 0.60           # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers
KAPPA = 0.60                      # C_DDB budget = PROTOCOL 4b's own DELTA, not tuned here
HEAD_L, HEAD_COST = 20, 10.0
OOS_START = "2017-01-01"

_LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def at_cost(r0, to, bps):
    return r0 - to * bps / 1e4


def sigma_of(u, L):
    """Annualised trailing realised vol of the risk-proxy return line, information
    through close t only (pandas .rolling is right-aligned and inclusive of t)."""
    return u.rolling(L).std() * np.sqrt(252.0)


def scaler(u, L, target, cap):
    sig = sigma_of(u, L)
    s = (target / sig).clip(upper=cap, lower=0.0)
    return s.where(sig.notna() & (sig > 0), LIVE_GROSS), sig


def legs_4b(r, spy):
    c, s, d = m3(r)
    cs, ss, ds = m3(spy)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, L_SHARPE=bool(s > ss), L_DD=bool(d >= DELTA * ds),
                L_CAGR=bool(c >= PHI * cs), cap=DELTA * ds, floor=PHI * cs)


def main():
    say(f"# {STEM}")
    say("# idea 2260 -- does a VOL-TARGETED gross clear 4b where a CONSTANT gross only does at g=1.00,")
    say("#              and does it buy the DRAWDOWN leg more cheaply AT MATCHED CAGR?")
    say(f"# targets={TARGETS}\n# caps={CAPS}\n# lookbacks={LOOKBACKS} (headline {HEAD_L})")
    say(f"# grosses={GROSSES}\n# costs={COSTS} bps  panels={PANELS}  band={BAND}  cadence={FREQ}  t+1")
    say("")

    gate_rows, grid_rows, lad_rows, match_rows, ch_rows = [], [], [], [], []
    store = {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "b136"))
        start = px.index[260]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        idx = spy_full.index
        is_mask = idx < pd.Timestamp(OOS_START)
        oos_mask = ~is_mask

        # ---------------- constant-gross ladder (the comparand the whole run is scored against)
        raw_g = {}
        for g in GROSSES:
            res = backtest(px, rules_v2_weights(px, band=BAND, gross=g), cost_bps=0.0, freq=FREQ)
            raw_g[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])

        # risk proxy: the gross-of-cost return line of the g = 1.00 base book
        u = raw_g[1.000][0]

        # ---------------- GATES G1, G3, G5, G7 ------------------------------------------------
        w75 = rules_v2_weights(px, band=BAND, gross=LIVE_GROSS)
        wlive = rules_v2_weights(px)
        g1w = float((w75 - wlive).abs().max().max())
        rl = backtest(px, wlive, cost_bps=0.0, freq=FREQ)
        g1r = float((at_cost(*raw_g[LIVE_GROSS], 10.0)
                     - at_cost(rl["returns"].loc[start:], rl["turnover"].loc[start:], 10.0)).abs().max())
        gate_rows.append(dict(panel=panel, gate="G1 constant g=0.75 IS the live book",
                              stat_a=g1w, stat_b=g1r, passed=bool(g1w == 0.0 and g1r == 0.0)))

        g5a = at_cost(*raw_g[1.000], 25.0)
        g5b = backtest(px, rules_v2_weights(px, band=BAND, gross=1.0), cost_bps=25.0,
                       freq=FREQ)["returns"].loc[start:]
        g5 = float((g5a - g5b).abs().max())
        gate_rows.append(dict(panel=panel, gate="G5 derived cost == re-simulated",
                              stat_a=np.nan, stat_b=g5, passed=bool(g5 < 1e-15)))

        lad_cagr = [m3(at_cost(*raw_g[g], HEAD_COST))[0] for g in GROSSES]
        dmin = float(np.min(np.diff(lad_cagr)))
        gate_rows.append(dict(panel=panel, gate="G7 ladder CAGR strictly increasing in g",
                              stat_a=dmin, stat_b=float(np.max(np.diff(lad_cagr))),
                              passed=bool(dmin > 0.0)))

        live10 = at_cost(*raw_g[LIVE_GROSS], 10.0)
        lc, ls, ld = m3(live10)
        lh1, lh2 = (metrics(x)["Sharpe"] for x in halves(live10))
        lo_c, lo_s, lo_d = m3(live10[oos_mask])
        one10 = at_cost(*raw_g[1.000], 10.0)
        oc, os_, od = m3(one10)
        ooc, oos_s, ood = m3(one10[oos_mask])
        sc, ss_, sd = m3(spy_full)
        so_c, so_s, so_d = m3(spy_full[oos_mask])
        say(f"[{panel}] live RULES v2 (g=0.75) @10bps  FULL {lc:.2%} / {ls:.4f} / {ld:.2%}   "
            f"halves {lh1:.4f} / {lh2:.4f}   OOS {lo_c:.2%} / {lo_s:.4f} / {lo_d:.2%}")
        say(f"[{panel}] constant gross 1.00   @10bps  FULL {oc:.2%} / {os_:.4f} / {od:.2%}"
            f"                         OOS {ooc:.2%} / {oos_s:.4f} / {ood:.2%}")
        say(f"[{panel}] SPY                            FULL {sc:.2%} / {ss_:.4f} / {sd:.2%}"
            f"                         OOS {so_c:.2%} / {so_s:.4f} / {so_d:.2%}")
        say(f"[{panel}] 4b bars: FULL CAGR floor {PHI*sc:.2%}, DD cap {DELTA*sd:.2%}; "
            f"OOS CAGR floor {PHI*so_c:.2%}, DD cap {DELTA*so_d:.2%}")

        if panel == "u56":
            ref = [(lc, 0.0862), (ls, 1.2010), (ld, -0.1205), (lh1, 1.2276), (lh2, 1.1806),
                   (lo_c, 0.0946), (lo_s, 1.2767), (lo_d, -0.1205),
                   (oc, 0.1153), (os_, 1.2009), (od, -0.1591),
                   (ooc, 0.1267), (oos_s, 1.2760), (ood, -0.1591),
                   (so_c, 0.1529), (so_s, 0.8751), (so_d, -0.3372)]
            d3 = max(abs(a - b) for a, b in ref)
            gate_rows.append(dict(panel=panel, gate="G3 committed cells reproduce",
                                  stat_a=d3, stat_b=np.nan, passed=bool(d3 < 5e-4)))

        # ---------------- G4: no lookahead in sigma ------------------------------------------
        g4 = 0.0
        for L in LOOKBACKS:
            sig_full = sigma_of(u, L)
            for k in (400, 900, 1500, 2200, 3000):
                t = u.index[k]
                sig_trunc = sigma_of(u.loc[:t], L).iloc[-1]
                g4 = max(g4, abs(float(sig_trunc) - float(sig_full.loc[t])))
        gate_rows.append(dict(panel=panel, gate="G4 sigma_t uses no future data",
                              stat_a=g4, stat_b=np.nan, passed=bool(g4 < 1e-15)))

        # ---------------- G2: degenerate limit -> constant gross at CAP -----------------------
        g2 = 0.0
        for cap in CAPS:
            s_deg, sig = scaler(u, HEAD_L, 10.0, cap)
            w_deg = rules_v2_weights(px, band=BAND, gross=1.0).loc[start:].mul(s_deg, axis=0)
            w_ref = rules_v2_weights(px, band=BAND, gross=cap).loc[start:]
            ok = sig.notna() & (sig > 0)
            g2 = max(g2, float((w_deg[ok] - w_ref[ok]).abs().max().max()))
        gate_rows.append(dict(panel=panel, gate="G2 TARGET=10 pins to CAP == constant gross",
                              stat_a=g2, stat_b=np.nan, passed=bool(g2 < 1e-15)))

        # ---------------- the published ladder rows -------------------------------------------
        for bps in COSTS:
            base_r = at_cost(*raw_g[LIVE_GROSS], bps)
            b_h1, b_h2 = (metrics(x)["Sharpe"] for x in halves(base_r))
            b_dd = metrics(base_r)["MaxDD"]
            sh1, sh2 = (metrics(x)["Sharpe"] for x in halves(spy_full))
            for g in GROSSES:
                r = at_cost(*raw_g[g], bps)
                h1, h2 = halves(r)
                f = legs_4b(r, spy_full)
                o = legs_4b(r[oos_mask], spy_full[oos_mask])
                lad_rows.append(dict(
                    panel=panel, cost_bps=bps, gross=g, CAGR=f["CAGR"], Sharpe=f["Sharpe"],
                    MaxDD=f["MaxDD"], H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                    OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                    turnover_yr=float(raw_g[g][1].sum() / (len(r) / 252)),
                    DD_margin_full=f["MaxDD"] - f["cap"], DD_margin_oos=o["MaxDD"] - o["cap"],
                    pass_4b_full=bool(metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                                      and f["L_DD"] and f["L_CAGR"]),
                    pass_4b_oos=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"]),
                    pass_4a=bool(metrics(h1)["Sharpe"] > b_h1 and metrics(h2)["Sharpe"] > b_h2
                                 and f["MaxDD"] >= b_dd)))

        # ---------------- the vol-target grid --------------------------------------------------
        w_base = rules_v2_weights(px, band=BAND, gross=1.0)
        raw_v = {}
        for L in LOOKBACKS:
            for tg in TARGETS:
                for cap in CAPS:
                    s, _ = scaler(u, L, tg, cap)
                    w = w_base.mul(s.reindex(w_base.index).fillna(LIVE_GROSS), axis=0)
                    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                    raw_v[(L, tg, cap)] = (res["returns"].loc[start:], res["turnover"].loc[start:],
                                           float(s.mean()))

        sh1, sh2 = (metrics(x)["Sharpe"] for x in halves(spy_full))
        for bps in COSTS:
            base_r = at_cost(*raw_g[LIVE_GROSS][:2], bps)
            b_h1, b_h2 = (metrics(x)["Sharpe"] for x in halves(base_r))
            b_dd = metrics(base_r)["MaxDD"]
            b_oos_s = metrics(base_r[oos_mask])["Sharpe"]
            b_oos_dd = metrics(base_r[oos_mask])["MaxDD"]
            # ladder at this cost rung, for the matched-CAGR inversion
            lc_cagr = np.array([m3(at_cost(*raw_g[g], bps))[0] for g in GROSSES])
            lc_dd = np.array([m3(at_cost(*raw_g[g], bps))[2] for g in GROSSES])
            one = at_cost(*raw_g[1.000], bps)
            one_c, one_s, one_dd = m3(one)
            one_margin = one_dd - DELTA * sd
            for L in LOOKBACKS:
                for tg in TARGETS:
                    for cap in CAPS:
                        r0, to, mean_s = raw_v[(L, tg, cap)]
                        r = at_cost(r0, to, bps)
                        h1, h2 = halves(r)
                        f = legs_4b(r, spy_full)
                        o = legs_4b(r[oos_mask], spy_full[oos_mask])
                        ic, ish, idd = m3(r[is_mask])
                        p4b_full = bool(metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                                        and f["L_DD"] and f["L_CAGR"])
                        p4b_oos = bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"])
                        p4a = bool(metrics(h1)["Sharpe"] > b_h1 and metrics(h2)["Sharpe"] > b_h2
                                   and f["MaxDD"] >= b_dd)
                        # --- matched-CAGR constant-gross twin
                        inside = lc_cagr[0] <= f["CAGR"] <= lc_cagr[-1]
                        if inside:
                            gstar = float(np.interp(f["CAGR"], lc_cagr, GROSSES))
                            dd_m = float(np.interp(gstar, GROSSES, lc_dd))
                        else:
                            gstar, dd_m = np.nan, np.nan
                        dDD = (f["MaxDD"] - dd_m) if inside else np.nan
                        grid_rows.append(dict(
                            panel=panel, cost_bps=bps, lookback=L, target=tg, cap=cap,
                            mean_scaler=mean_s,
                            CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                            H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                            IS_CAGR=ic, IS_Sharpe=ish, IS_MaxDD=idd,
                            OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                            turnover_yr=float(to.sum() / (len(r) / 252)),
                            L_DD_full=f["L_DD"], L_CAGR_full=f["L_CAGR"],
                            L_SHARPE_oos=o["L_SHARPE"], L_DD_oos=o["L_DD"], L_CAGR_oos=o["L_CAGR"],
                            pass_4b_full=p4b_full, pass_4b_oos=p4b_oos, pass_4a=p4a,
                            DD_margin_full=f["MaxDD"] - f["cap"],
                            DD_margin_oos=o["MaxDD"] - o["cap"],
                            CAGR_margin_full=f["CAGR"] - f["floor"],
                            g_matched=gstar, MaxDD_matched=dd_m, dDD_vs_matched=dDD,
                            inside_ladder=bool(inside),
                            dCAGR_vs_g1=f["CAGR"] - one_c, dDD_vs_g1=f["MaxDD"] - one_dd,
                            dDDmargin_vs_g1=(f["MaxDD"] - DELTA * sd) - one_margin,
                            base_OOS_Sharpe=b_oos_s, base_OOS_MaxDD=b_oos_dd))

        store[panel] = dict(raw_v=raw_v, raw_g=raw_g, spy=spy_full, is_mask=is_mask,
                            oos_mask=oos_mask, sd=sd, so_d=so_d)

        # ---------------- RULE 8 choosers (IS 2009-2016 only) ----------------------------------
        cells = [(tg, cap) for tg in TARGETS for cap in CAPS]
        spy_is_dd = metrics(spy_full[is_mask])["MaxDD"]
        for L in LOOKBACKS:
            for bps in COSTS:
                rs = {c: at_cost(*raw_v[(L,) + c][:2], bps) for c in cells}
                is_m = {c: metrics(rs[c][is_mask]) for c in cells}
                picks = {
                    "C_SHARPE": max(cells, key=lambda c: is_m[c]["Sharpe"]),
                    "C_CALMAR": max(cells, key=lambda c: is_m[c]["Calmar"]),
                }
                ok = [c for c in cells if is_m[c]["MaxDD"] >= KAPPA * spy_is_dd]
                picks["C_DDB060"] = max(ok, key=lambda c: is_m[c]["CAGR"]) if ok else None
                picks["C_LIVE"] = (0.10, 1.00)
                base_r = at_cost(*raw_g[LIVE_GROSS][:2], bps)
                b_oos_s = metrics(base_r[oos_mask])["Sharpe"]
                b_oos_dd = metrics(base_r[oos_mask])["MaxDD"]
                for nm, c in picks.items():
                    if c is None:
                        ch_rows.append(dict(panel=panel, lookback=L, cost_bps=bps, chooser=nm,
                                            abstain=True))
                        continue
                    r = rs[c]
                    h1, h2 = halves(r)
                    f, o = legs_4b(r, spy_full), legs_4b(r[oos_mask], spy_full[oos_mask])
                    ch_rows.append(dict(
                        panel=panel, lookback=L, cost_bps=bps, chooser=nm, abstain=False,
                        pick_target=c[0], pick_cap=c[1],
                        IS_Sharpe=is_m[c]["Sharpe"], IS_MaxDD=is_m[c]["MaxDD"],
                        IS_SPY_MaxDD=spy_is_dd,
                        CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                        H1=metrics(h1)["Sharpe"], H2=metrics(h2)["Sharpe"],
                        OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                        turnover_yr=float(raw_v[(L,) + c][1].sum() / (len(r) / 252)),
                        pass_4b_full=bool(metrics(h1)["Sharpe"] > sh1 and metrics(h2)["Sharpe"] > sh2
                                          and f["L_DD"] and f["L_CAGR"]),
                        pass_4b_oos=bool(o["L_SHARPE"] and o["L_DD"] and o["L_CAGR"]),
                        L_SHARPE_oos=o["L_SHARPE"], L_DD_oos=o["L_DD"], L_CAGR_oos=o["L_CAGR"],
                        cap_oos=o["cap"], floor_oos=o["floor"],
                        base_OOS_Sharpe=b_oos_s, base_OOS_MaxDD=b_oos_dd,
                        spy_OOS_Sharpe=metrics(spy_full[oos_mask])["Sharpe"]))
        say("")

    D = pd.DataFrame(grid_rows)
    Lad = pd.DataFrame(lad_rows)
    C = pd.DataFrame(ch_rows)
    n_exp_D = len(PANELS) * len(COSTS) * len(LOOKBACKS) * len(TARGETS) * len(CAPS)
    n_exp_L = len(PANELS) * len(COSTS) * len(GROSSES)
    n_exp_C = len(PANELS) * len(LOOKBACKS) * len(COSTS) * 4
    gate_rows.append(dict(panel="both", gate="G6 all cells published", stat_a=len(D),
                          stat_b=len(Lad) + len(C),
                          passed=bool(len(D) == n_exp_D and len(Lad) == n_exp_L and len(C) == n_exp_C)))
    G = pd.DataFrame(gate_rows)

    say("=== GATES (printed before any hypothesis is read) ===")
    say(G.to_string(index=False))
    say(f"GATES: {int(G.passed.sum())} of {len(G)} PASS   "
        f"(published: {len(D)} book / {len(Lad)} ladder / {len(C)} chooser rows)")

    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    Lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    C.to_csv(OUT / f"{STEM}.choosers.csv", index=False)
    G.to_csv(OUT / f"{STEM}.gates.csv", index=False)
    D[D.inside_ladder].to_csv(OUT / f"{STEM}.matched.csv", index=False)

    # ------------------------------------------------------------------ PART 1: the headline grid
    say("\n=== PART 1 -- THE VOL-TARGET GRID, HEADLINE RUNG (L=20, 10 bps), EVERY CELL ===")
    for panel in PANELS:
        sub = D[(D.panel == panel) & (D.lookback == HEAD_L) & (D.cost_bps == HEAD_COST)]
        say(f"\n[{panel}]  (mean_s = realised mean scaler; dDD = MaxDD minus the CONSTANT-GROSS "
            f"rung matched on FULL CAGR; + = vol target SHALLOWER)")
        cols = ["target", "cap", "mean_scaler", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover_yr", "g_matched",
                "MaxDD_matched", "dDD_vs_matched", "pass_4b_full", "pass_4b_oos", "pass_4a"]
        say(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n=== the CONSTANT-GROSS ladder at the same rung (the comparand) ===")
    for panel in PANELS:
        sub = Lad[(Lad.panel == panel) & (Lad.cost_bps == HEAD_COST)]
        say(f"\n[{panel}]")
        say(sub[["gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                 "OOS_MaxDD", "turnover_yr", "pass_4b_full", "pass_4b_oos", "pass_4a"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ PART 2: H1 / H5
    say("\n=== PART 2 -- H1 (EXISTENCE) and H5 (4a) over ALL 720 published cells ===")
    say(f"4b FULL passes : {int(D.pass_4b_full.sum())} of {len(D)}")
    say(f"4b OOS passes  : {int(D.pass_4b_oos.sum())} of {len(D)}")
    say(f"4b BOTH        : {int((D.pass_4b_full & D.pass_4b_oos).sum())} of {len(D)}")
    say(f"4a passes      : {int(D.pass_4a.sum())} of {len(D)}   <- H5")
    unlev = D[D.cap <= 1.0]
    say(f"UNLEVERED sub-grid (cap <= 1.00, PROTOCOL rule 2): 4b BOTH "
        f"{int((unlev.pass_4b_full & unlev.pass_4b_oos).sum())} of {len(unlev)}, "
        f"4a {int(unlev.pass_4a.sum())} of {len(unlev)}")
    for panel in PANELS:
        s = D[(D.panel == panel) & (D.cost_bps == HEAD_COST) & (D.lookback == HEAD_L)]
        say(f"  [{panel}] headline rung: 4b FULL {int(s.pass_4b_full.sum())}/24, "
            f"4b OOS {int(s.pass_4b_oos.sum())}/24, BOTH "
            f"{int((s.pass_4b_full & s.pass_4b_oos).sum())}/24, 4a {int(s.pass_4a.sum())}/24")
    say("\nFIRST FAILING 4b LEG, counted over all 720 cells (FULL then OOS):")
    say(f"  FULL  DD leg fails {int((~D.L_DD_full).sum())}, CAGR floor fails {int((~D.L_CAGR_full).sum())}")
    say(f"  OOS   Sharpe {int((~D.L_SHARPE_oos).sum())}, DD {int((~D.L_DD_oos).sum())}, "
        f"CAGR {int((~D.L_CAGR_oos).sum())}")

    # ------------------------------------------------------------------ PART 3: H2, the run's claim
    say("\n=== PART 3 -- H2: AT MATCHED FULL-SAMPLE CAGR, IS THE VOL TARGET SHALLOWER? ===")
    say("dDD_vs_matched = MaxDD(vol target) - MaxDD(constant gross interpolated to the same "
        "FULL CAGR).  POSITIVE = vol target shallower = it buys the DD leg more cheaply.")
    M = D[D.inside_ladder]
    say(f"cells inside the ladder's CAGR range: {len(M)} of {len(D)}")
    say(f"dDD > 0 : {int((M.dDD_vs_matched > 0).sum())} of {len(M)}  "
        f"({(M.dDD_vs_matched > 0).mean():.3f})")
    say(f"dDD median {M.dDD_vs_matched.median():+.4%}   mean {M.dDD_vs_matched.mean():+.4%}   "
        f"min {M.dDD_vs_matched.min():+.4%}   max {M.dDD_vs_matched.max():+.4%}")
    say("\nby panel x lookback x cost (median dDD, share positive, n):")
    agg = (M.groupby(["panel", "lookback", "cost_bps"])["dDD_vs_matched"]
           .agg(median="median", share_pos=lambda s: (s > 0).mean(), n="size").reset_index())
    say(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nsame, restricted to the cells that CLEAR 4b FULL:")
    MP = M[M.pass_4b_full]
    if len(MP):
        say(f"n={len(MP)}, dDD > 0 in {int((MP.dDD_vs_matched > 0).sum())}, median "
            f"{MP.dDD_vs_matched.median():+.4%}, max {MP.dDD_vs_matched.max():+.4%}")
    else:
        say("  none")

    # ------------------------------------------------------------------ PART 4: H3, literal wording
    say("\n=== PART 4 -- H3: ANY 4b PASSER WITH CAGR >= g=1.00's AND A BIGGER DD MARGIN? ===")
    say("dDDmargin_vs_g1 > 0 means the cell sits FURTHER INSIDE the 4b DD cap than g = 1.00 does.")
    H3 = D[(D.pass_4b_full) & (D.pass_4b_oos) & (D.dCAGR_vs_g1 >= 0) & (D.dDDmargin_vs_g1 > 0)]
    say(f"H3 cells: {len(H3)} of {len(D)}")
    if len(H3):
        say(H3[["panel", "cost_bps", "lookback", "target", "cap", "CAGR", "Sharpe", "MaxDD",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "dCAGR_vs_g1", "dDDmargin_vs_g1",
                "turnover_yr"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    H3b = D[(D.pass_4b_full) & (D.pass_4b_oos) & (D.dDDmargin_vs_g1 > 0)]
    say(f"\nrelaxed (4b BOTH + bigger DD margin than g=1.00, CAGR not required to match): {len(H3b)}")
    if len(H3b):
        say(H3b.groupby(["panel", "cost_bps"]).size().to_string())
        best = H3b.sort_values("dDDmargin_vs_g1", ascending=False).head(12)
        say(best[["panel", "cost_bps", "lookback", "target", "cap", "CAGR", "Sharpe", "MaxDD",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "dCAGR_vs_g1", "dDDmargin_vs_g1",
                  "turnover_yr"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ PART 5: rule 8
    say("\n=== PART 5 -- RULE 8: 2009-2016 CHOOSES, 2017-2026 READ ONCE (120 chooser rows) ===")
    act = C[~C.abstain.fillna(False)]
    say(act[["panel", "lookback", "cost_bps", "chooser", "pick_target", "pick_cap", "CAGR",
             "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass_4b_full",
             "pass_4b_oos"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nchooser scoreboard (4b OOS passes out of 30 panel x lookback x cost cells each):")
    sb = act.groupby("chooser").agg(n=("pass_4b_oos", "size"),
                                    oos_4b=("pass_4b_oos", "sum"),
                                    full_4b=("pass_4b_full", "sum"),
                                    med_OOS_Sharpe=("OOS_Sharpe", "median"),
                                    med_OOS_CAGR=("OOS_CAGR", "median"),
                                    med_OOS_MaxDD=("OOS_MaxDD", "median"))
    say(sb.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\nH4 verdict: " + ("SUPPORTED -- at least one chooser reaches a 4b-OOS cell"
                            if act.pass_4b_oos.any() else
                            "FALSIFIED -- no IS-only chooser reaches a 4b-OOS cell"))

    # ------------------------------------------------------------------ PART 6: cost ladder
    say("\n=== PART 6 -- COST DURABILITY of the best cells (4b BOTH, by cost rung) ===")
    both = D[D.pass_4b_full & D.pass_4b_oos]
    if len(both):
        say(both.groupby(["panel", "cost_bps"]).size().to_string())
        say("\nunlevered (cap <= 1.00) only:")
        bu = both[both.cap <= 1.0]
        say(bu.groupby(["panel", "cost_bps"]).size().to_string() if len(bu) else "  none")
    else:
        say("  no cell clears 4b on both windows")

    # ------------------------------------------------------------------ verdict
    say("\n=== PRE-REGISTERED HYPOTHESES, READ ===")
    h1 = bool((D[(D.panel == 'u56') & (D.cost_bps == HEAD_COST) & (D.lookback == HEAD_L)]
               .pipe(lambda s: s.pass_4b_full & s.pass_4b_oos)).any())
    h2 = bool(len(MP) and (MP.dDD_vs_matched > 0).any())
    h3 = bool(len(H3))
    h4 = bool(act.pass_4b_oos.any())
    h5 = bool(D.pass_4a.any())
    for k, v in [("H1 EXISTENCE (u56 @10bps, L=20)", h1), ("H2 CHEAPER-DD at matched CAGR", h2),
                 ("H3 MORE DD MARGIN THAN g=1.00 at >= its CAGR", h3),
                 ("H4 RULE 8 chooser reaches a 4b-OOS cell", h4), ("H5 4a", h5)]:
        say(f"  {k:48s} {'SUPPORTED' if v else 'FALSIFIED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt / .grid.csv / .ladder.csv / .matched.csv / "
          f".choosers.csv / .gates.csv")


if __name__ == "__main__":
    main()
