#!/usr/bin/env python3
"""Idea 291 - "does-the-banded-slow-filter-survive-on-the-large-cap-panels".

The question
------------
Idea 52 (lane B, 2026-09-06) swept a SLOWED 200d trend filter on the 439-name sub-$2B panel:
the 200d moving average with a hysteresis band b (IN above ma*(1+b), OUT below ma*(1-b),
previous state in between) at three rebalance cadences, with exposure held constant so the
filter is pure SELECTION.  On that panel the filter is a destroyer at every setting, and its
ONE positive-price form was `200d band only, b >= 0.05, quarterly, RESPREAD`, which beat the
no-filter control by +0.053 Sharpe - but 0 of 72 points cleared 4b there.

On the large-cap panels the same 200d clause is ASSUMED to be the edge, and it has never been
run at any band or any cadence other than weekly.  Idea 289 (cloud, this morning) narrowed
what is left to find: on U56/B136 the hard 200d gate and scan.py's soft tilt are ONE
instrument worth a mean -0.006 of Sharpe, and RULES v1's whole eligibility effect is the
`vol20 < 0.60` clause.  But idea 289 only ever ran the gate FAST (weekly, no band).  This run
asks the remaining question directly: does SLOWING the trend filter - band, cadence, or both -
turn it from a null into an edge on large caps, or does it hurt there?

Pre-registered expectation: on large caps a band should matter LESS than on small caps
(mega caps cross their own 200d average far less often), so the 18-point grid should be
flat and the verdict a KILL of "slowing helps".  The interesting alternative is that it
HURTS, i.e. the large-cap gate's only value is its speed.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. band b in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}   (b=0.00 reproduces the hard gate;
                                                         b=0.03 is RULES v2's live clause)
    2. cadence in {W, M, Q}
That is idea 52's exact 18-point grid, re-run here.  ALL 18 points are reported for every arm.

Reported decomposition axes - never selected on; the rule-8 selection runs strictly INSIDE
each (universe, gate, construction) arm over the (band, cadence) grid only:
    universe       U56  = research/universe.json (55 tradables + SPY)
                   B136 = research/universe_broad.json (survivorship: current constituents)
    gate form      MA    = 200d band only - the form idea 52 found positive on small caps
                   MAVOL = the 200d band AND vol20 < 0.60 (RULES v1's full filter)
    construction   RESPREAD = gross/E_t across the gated-IN names, always 75% invested.
                              Exposure is held constant, so any difference vs the control is
                              TIMING/selection, not de-risking.  This is the axis idea 291
                              names and the one the verdict is read off.
                   DEGROSS  = gross/N_live per live name, gated-out weight goes to CASH
                              (the RULES v2 form), reported as a control.

Control (the thing the filter must beat): EWall - every live name equal-weighted at 75%
gross, no filter of any kind, reported at each cadence.  Identical under both constructions.

Grid = 6 bands x 3 cadences x 2 gates x 2 constructions x 2 universes = 144 book cells,
+ 3 controls x 2 constructions-equal x 2 universes, ALL reported.  Each cell is also re-run
at 0 bps so the turnover half of any cadence effect can be separated from the timing half.

Mechanism diagnostic: gate state flips per name per year (daily, and as SAMPLED on the
rebalance schedule) plus realised annual turnover, so "slowing" is measured, not assumed.

Rule 8 walk-forward: (band, cadence) chosen on <= 2016-12-31 by in-sample Sharpe inside each
(universe, gate, construction) arm; 2017-2026 read ONCE.  Reported against SPY OOS, RULES v2
OOS, the no-filter control OOS, the pre-registered anchor (b=0.03, W - the live clause at the
live cadence) and the best OOS cell in the arm (regret).

Both KEEP paths evaluated on every cell:
    4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2's
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's

Outputs: .grid.csv, .flips.csv, .walkforward.csv, .console.txt, .result.md
Deterministic, standalone, no network.  Nothing in RULES.md, scan.py, bot.py or baseline.py
is modified.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

COST, GROSS, MAX_VOL = 10, 0.75, 0.60
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
CADENCES = ["W", "M", "Q"]
GATES = ["MA", "MAVOL"]
CONS = ["RESPREAD", "DEGROSS"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
ANCHOR = (0.03, "W")                       # the live clause at the live cadence


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, gate, band):
    g = band_state(px, band)
    if gate == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g & live_mask(px)


def book(px, gate, band, con):
    g = gate_mask(px, gate, band)
    if con == "RESPREAD":                                 # always 75% invested among IN names
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)                                  # DEGROSS: gated-out weight -> cash
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


def st(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x); return m["CAGR"], m["Sharpe"], m["MaxDD"]


def row_of(r):
    h = len(r) // 2
    c, s, d = st(r)
    oc, os_, od = st(r, OOS_START)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=metrics(r.iloc[:h])["Sharpe"],
                H2=metrics(r.iloc[h:])["Sharpe"], IS_Sharpe=st(r, None, IS_END)[1],
                IS_MaxDD=st(r, None, IS_END)[2], OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_paths(x, spy, v2):
    a = (x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])
    b = (x["H1"] > spy["H1"] and x["H2"] > spy["H2"] and x["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and x["MaxDD"] >= 0.60 * spy["MaxDD"] and x["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def first_fail_4b(x, spy):
    for lbl, ok in (("H1", x["H1"] > spy["H1"]), ("H2", x["H2"] > spy["H2"]),
                    ("OOS", x["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                    ("DD", x["MaxDD"] >= 0.60 * spy["MaxDD"]),
                    ("CAGR", x["CAGR"] >= 0.70 * spy["CAGR"])):
        if not ok:
            return lbl
    return "-"


def main():
    unis = {"U56": load_universe(), "B136": load_universe(broad=True)}
    rows, flip_rows, ctrl_rows, refs, ctrls = [], [], [], {}, {}

    P("=" * 150)
    P("Idea 291  does-the-banded-slow-filter-survive-on-the-large-cap-panels   (cloud, 2026-09-06)")
    P("=" * 150)
    P(f"Idea 52's 18-point grid (band x cadence) re-run on the LARGE-CAP panels at RESPREAD "
      f"(exposure held constant) plus DEGROSS as a control.")
    P(f"Costs {COST} bps/unit turnover, gross {GROSS}, next-day execution. "
      f"Tuned: band {BANDS} x cadence {CADENCES}. Reported: universe x gate x construction.")

    for uname, px_all in unis.items():
        px_all = px_all.dropna(how="all").ffill()
        tr = [c for c in px_all.columns if c != "SPY"]
        px = px_all[tr]
        start = px_all.index[260]
        years = len(px_all.loc[start:]) / 252
        yrs = px_all.index.to_series().groupby(px_all.index.year).count()

        P(f"\n{'='*150}\n{uname}: {len(tr)} tradables + SPY, {px_all.index[0].date()} .. "
          f"{px_all.index[-1].date()}, evaluated from {start.date()}")
        P(f"  index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, "
          f"2024 {yrs.get(2024)}")
        if yrs.loc[2013:2024].max() > 300:
            P("  !! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        P("=" * 150)

        spy = row_of(px_all["SPY"].pct_change().fillna(0).loc[start:])
        v2 = row_of(backtest(px_all, rules_v2_weights(px).reindex(columns=px_all.columns).fillna(0.0),
                             cost_bps=COST, freq="W")["returns"].loc[start:])
        refs[uname] = dict(SPY=spy, v2=v2)

        # -- controls: EWall, no filter, at each cadence ---------------------
        P("\n-- CONTROLS: EWall (every live name, 75% gross, NO filter) - the book the filter must beat --")
        P(f"  {'cad':4s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} {'IS_S':>6s} "
          f"{'OOS_C':>7s} {'OOS_S':>6s} {'OOS_DD':>8s} {'turn/yr':>8s} {'CAGR@0bps':>10s}")
        for cad in CADENCES:
            rc = backtest(px_all, control_book(px).reindex(columns=px_all.columns).fillna(0.0),
                          cost_bps=COST, freq=cad)
            x = row_of(rc["returns"].loc[start:])
            c0 = metrics(backtest(px_all, control_book(px).reindex(columns=px_all.columns).fillna(0.0),
                                  cost_bps=0, freq=cad)["returns"].loc[start:])["CAGR"]
            turn = rc["turnover"].loc[start:].sum() / years
            ctrls[(uname, cad)] = x
            ctrl_rows.append(dict(universe=uname, cad=cad, **x, turnover_yr=turn, CAGR_0bps=c0))
            P(f"  {cad:4s} {x['CAGR']:7.2%} {x['Sharpe']:7.3f} {x['MaxDD']:8.2%} {x['H1']:6.3f} "
              f"{x['H2']:6.3f} {x['IS_Sharpe']:6.3f} {x['OOS_CAGR']:7.2%} {x['OOS_Sharpe']:6.3f} "
              f"{x['OOS_MaxDD']:8.2%} {turn:8.2f} {c0:10.2%}")
        for tag, x in (("SPY", spy), ("RULES v2 (live)", v2)):
            P(f"  {tag:16s} CAGR {x['CAGR']:6.2%}  Sharpe {x['Sharpe']:.3f}  MaxDD {x['MaxDD']:7.2%}"
              f"  H1/H2 {x['H1']:.3f}/{x['H2']:.3f}"
              f"  OOS {x['OOS_CAGR']:6.2%}/{x['OOS_Sharpe']:.3f}/{x['OOS_MaxDD']:7.2%}")
        P(f"  4b bars on {uname}: Sharpe > SPY in both halves AND OOS, MaxDD >= "
          f"{0.60*spy['MaxDD']:.2%}, CAGR >= {0.70*spy['CAGR']:.2%}")

        # -- mechanism: does the band actually slow the gate down? -----------
        P(f"\n-- {uname} MECHANISM: gate state flips per name per year (daily, and as SAMPLED on "
          f"the rebalance schedule) --")
        P(f"  {'gate':6s} {'band':>5s} {'mean_in%':>9s} {'flips_daily':>12s} "
          + " ".join(f"{'flips_'+c:>11s}" for c in CADENCES))
        live = live_mask(px)
        ls = live.loc[start:]
        denom = ls.sum(axis=1).mean() * years
        masks = {c: rebalance_mask(px_all.index, c).reindex(px_all.index).fillna(False) for c in CADENCES}
        for gate in GATES:
            for b in BANDS:
                g = gate_mask(px, gate, b)
                gs = g.loc[start:]
                daily = ((gs != gs.shift(1)) & ls & ls.shift(1)).sum().sum() / denom
                row = dict(universe=uname, gate=gate, band=b,
                           mean_in_pct=100 * gs.sum(axis=1).mean() / ls.sum(axis=1).mean(),
                           flips_daily=daily)
                for cad in CADENCES:
                    m = masks[cad].loc[start:]
                    gsub, lsub = gs[m.values], ls[m.values]
                    row[f"flips_{cad}"] = ((gsub != gsub.shift(1)) & lsub & lsub.shift(1)).sum().sum() / denom
                flip_rows.append(row)
                P(f"  {gate:6s} {b:5.2f} {row['mean_in_pct']:8.1f}% {daily:12.3f} "
                  + " ".join(f"{row['flips_'+c]:11.3f}" for c in CADENCES))

        # -- the grid ---------------------------------------------------------
        for con in CONS:
            for gate in GATES:
                P(f"\n-- {uname} / {con} / gate {gate}   (deltas are vs the EWall control at the "
                  f"SAME cadence) --")
                P(f"  {'cad':4s} {'band':>5s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} "
                  f"{'H2':>6s} {'IS_S':>6s} {'OOS_C':>7s} {'OOS_S':>6s} {'OOS_DD':>8s} "
                  f"{'dCAGR':>7s} {'dSharpe':>8s} {'dMaxDD':>7s} {'CAGR@0':>7s} {'turn':>6s} "
                  f"{'gross':>6s} {'4a':>5s} {'4b':>5s} {'fail4b':>7s}")
                for cad in CADENCES:
                    cb = ctrls[(uname, cad)]
                    for b in BANDS:
                        w = book(px, gate, b, con).reindex(columns=px_all.columns).fillna(0.0)
                        res = backtest(px_all, w, cost_bps=COST, freq=cad)
                        r = res["returns"].loc[start:]
                        x = row_of(r)
                        c0 = metrics(backtest(px_all, w, cost_bps=0, freq=cad)["returns"].loc[start:])["CAGR"]
                        turn = res["turnover"].loc[start:].sum() / years
                        gross = res["weights"].loc[start:].sum(axis=1).mean()
                        a4, b4 = keep_paths(x, spy, v2)
                        fb = first_fail_4b(x, spy)
                        rows.append(dict(universe=uname, con=con, gate=gate, cad=cad, band=b, **x,
                                         dCAGR_ctrl=x["CAGR"] - cb["CAGR"],
                                         dSharpe_ctrl=x["Sharpe"] - cb["Sharpe"],
                                         dMaxDD_ctrl=x["MaxDD"] - cb["MaxDD"],
                                         dOOS_Sharpe_ctrl=x["OOS_Sharpe"] - cb["OOS_Sharpe"],
                                         CAGR_0bps=c0, turnover_yr=turn, mean_gross=gross,
                                         pass4a=a4, pass4b=b4, first_fail_4b=fb,
                                         ctrl_Sharpe=cb["Sharpe"], ctrl_CAGR=cb["CAGR"],
                                         ctrl_OOS_Sharpe=cb["OOS_Sharpe"],
                                         spy_S=spy["Sharpe"], spy_OOS_S=spy["OOS_Sharpe"],
                                         v2_S=v2["Sharpe"], v2_OOS_S=v2["OOS_Sharpe"]))
                        P(f"  {cad:4s} {b:5.2f} {x['CAGR']:7.2%} {x['Sharpe']:7.3f} {x['MaxDD']:8.2%} "
                          f"{x['H1']:6.3f} {x['H2']:6.3f} {x['IS_Sharpe']:6.3f} {x['OOS_CAGR']:7.2%} "
                          f"{x['OOS_Sharpe']:6.3f} {x['OOS_MaxDD']:8.2%} "
                          f"{x['CAGR']-cb['CAGR']:+7.2%} {x['Sharpe']-cb['Sharpe']:+8.3f} "
                          f"{x['MaxDD']-cb['MaxDD']:+7.2%} {c0:7.2%} {turn:6.2f} {gross:6.3f} "
                          f"{str(a4):>5s} {str(b4):>5s} {fb:>7s}")

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(flip_rows).to_csv(f"{OUT}.flips.csv", index=False)
    pd.DataFrame(ctrl_rows).to_csv(f"{OUT}.controls.csv", index=False)

    # ---------------- Q1: does SLOWING help or hurt? ----------------------
    P(f"\n{'='*150}\nQ1  DOES SLOWING HELP OR HURT?   dSharpe vs the EWall control at the same "
      f"cadence, RESPREAD (the answer axis)\n{'='*150}")
    for uname in unis:
        for gate in GATES:
            d = grid[(grid.universe == uname) & (grid.con == "RESPREAD") & (grid.gate == gate)]
            P(f"\n  {uname} / RESPREAD / {gate}    dSharpe vs control (rows = band, cols = cadence)")
            P(f"    {'band':>5s} " + " ".join(f"{c:>12s}" for c in CADENCES)
              + f"   |  {'dCAGR W':>9s} {'dCAGR M':>9s} {'dCAGR Q':>9s}")
            for b in BANDS:
                P(f"    {b:5.2f} " + " ".join(
                    f"{d[(d.band==b)&(d.cad==c)].iloc[0].dSharpe_ctrl:+12.3f}" for c in CADENCES)
                  + "   |  " + " ".join(
                    f"{d[(d.band==b)&(d.cad==c)].iloc[0].dCAGR_ctrl:+9.2%}" for c in CADENCES))
            pos = int((d.dSharpe_ctrl > 0).sum())
            P(f"    -> beats the no-filter control on Sharpe in {pos} of {len(d)} points; "
              f"mean dSharpe {d.dSharpe_ctrl.mean():+.4f}, best {d.dSharpe_ctrl.max():+.4f} at "
              f"band {d.loc[d.dSharpe_ctrl.idxmax()].band:.2f}/{d.loc[d.dSharpe_ctrl.idxmax()].cad}")

    P(f"\n  BAND effect at fixed cadence (Sharpe at band b minus Sharpe at band 0.00), RESPREAD:")
    for uname in unis:
        for gate in GATES:
            d = grid[(grid.universe==uname)&(grid.con=="RESPREAD")&(grid.gate==gate)]
            for cad in CADENCES:
                b0 = d[(d.band == 0.00) & (d.cad == cad)].iloc[0]
                P(f"    {uname:5s} {gate:6s} {cad}  " + " ".join(
                    f"b={b:.2f} {d[(d.band==b)&(d.cad==cad)].iloc[0].Sharpe-b0.Sharpe:+.3f}"
                    for b in BANDS[1:]))
    P(f"\n  CADENCE effect at fixed band (Sharpe at cadence c minus Sharpe weekly), RESPREAD:")
    for uname in unis:
        for gate in GATES:
            d = grid[(grid.universe==uname)&(grid.con=="RESPREAD")&(grid.gate==gate)]
            for b in BANDS:
                w0 = d[(d.band == b) & (d.cad == "W")].iloc[0]
                P(f"    {uname:5s} {gate:6s} b={b:.2f}  " + " ".join(
                    f"{c} {d[(d.band==b)&(d.cad==c)].iloc[0].Sharpe-w0.Sharpe:+.3f}" for c in CADENCES[1:]))

    P(f"\n  IDEA 52's SMALL-CAP WINNER re-priced here: gate MA, band >= 0.05, cadence Q, RESPREAD")
    P(f"    (on SMALL439 it beat the control by +0.053 Sharpe)")
    for uname in unis:
        for b in [0.05, 0.08, 0.12]:
            r = grid[(grid.universe==uname)&(grid.con=="RESPREAD")&(grid.gate=="MA")
                     &(grid.band==b)&(grid.cad=="Q")].iloc[0]
            P(f"    {uname:5s} b={b:.2f} Q  CAGR {r.CAGR:7.2%} Sharpe {r.Sharpe:.3f} "
              f"MaxDD {r.MaxDD:7.2%}  vs control dS {r.dSharpe_ctrl:+.3f} dCAGR {r.dCAGR_ctrl:+.2%} "
              f"dMaxDD {r.dMaxDD_ctrl:+.2%}   4b {r.pass4b} (fails {r.first_fail_4b})")

    # ---------------- Q2: timing vs turnover ------------------------------
    P(f"\n{'='*150}\nQ2  IS ANY CADENCE EFFECT TURNOVER OR TIMING?   CAGR at 0 bps vs 10 bps, "
      f"RESPREAD\n{'='*150}")
    for uname in unis:
        for gate in GATES:
            d = grid[(grid.universe==uname)&(grid.con=="RESPREAD")&(grid.gate==gate)]
            P(f"\n  {uname} / {gate}   {'band':>5s} " + " ".join(
                f"{'CAGR0 '+c:>12s} {'turn '+c:>9s}" for c in CADENCES))
            for b in BANDS:
                P(f"  {'':16s} {b:5.2f} " + " ".join(
                    f"{d[(d.band==b)&(d.cad==c)].iloc[0].CAGR_0bps:12.2%} "
                    f"{d[(d.band==b)&(d.cad==c)].iloc[0].turnover_yr:9.2f}" for c in CADENCES))

    # ---------------- rule 8 ----------------------------------------------
    P(f"\n{'='*150}\nRULE 8 WALK-FORWARD - (band, cadence) chosen on <= {IS_END} by IS Sharpe "
      f"inside each (universe, gate, construction); {OOS_START}+ read once\n{'='*150}")
    wf = []
    P(f"  {'uni':5s} {'con':9s} {'gate':6s} {'pick':>10s} {'IS_S':>6s} | {'OOS CAGR':>9s} "
      f"{'OOS S':>7s} {'OOS DD':>8s} | {'anchor(.03,W) OOS S':>20s} {'ctrl OOS S':>11s} "
      f"{'SPY OOS S':>10s} {'v2 OOS S':>9s} | {'best OOS':>10s} {'regret':>7s} {'beats ctrl':>11s}")
    for uname in unis:
        spy, v2 = refs[uname]["SPY"], refs[uname]["v2"]
        for con in CONS:
            for gate in GATES:
                d = grid[(grid.universe==uname)&(grid.con==con)&(grid.gate==gate)]
                pick = d.sort_values(["IS_Sharpe", "band"], ascending=[False, False]).iloc[0]
                anc = d[(d.band == ANCHOR[0]) & (d.cad == ANCHOR[1])].iloc[0]
                best = d.sort_values("OOS_Sharpe", ascending=False).iloc[0]
                cO = ctrls[(uname, pick.cad)]["OOS_Sharpe"]
                wf.append(dict(universe=uname, con=con, gate=gate, pick_band=pick.band,
                               pick_cad=pick.cad, pick_IS_Sharpe=pick.IS_Sharpe,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, anchor_OOS_Sharpe=anc.OOS_Sharpe,
                               control_OOS_Sharpe=cO, spy_OOS_Sharpe=spy["OOS_Sharpe"],
                               v2_OOS_Sharpe=v2["OOS_Sharpe"], best_band=best.band,
                               best_cad=best.cad, best_OOS_Sharpe=best.OOS_Sharpe,
                               regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                               beats_control_OOS=bool(pick.OOS_Sharpe > cO),
                               beats_spy_OOS=bool(pick.OOS_Sharpe > spy["OOS_Sharpe"]),
                               pick_pass4a=bool(pick.pass4a), pick_pass4b=bool(pick.pass4b)))
                P(f"  {uname:5s} {con:9s} {gate:6s} {f'({pick.band:.2f},{pick.cad})':>10s} "
                  f"{pick.IS_Sharpe:6.3f} | {pick.OOS_CAGR:9.2%} {pick.OOS_Sharpe:7.3f} "
                  f"{pick.OOS_MaxDD:8.2%} | {anc.OOS_Sharpe:20.3f} {cO:11.3f} "
                  f"{spy['OOS_Sharpe']:10.3f} {v2['OOS_Sharpe']:9.3f} | "
                  f"{f'({best.band:.2f},{best.cad})':>10s} {best.OOS_Sharpe-pick.OOS_Sharpe:7.3f} "
                  f"{str(bool(pick.OOS_Sharpe>cO)):>11s}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\n  Chooser beats the no-filter control OOS in {int(W.beats_control_OOS.sum())} of {len(W)} arms; "
      f"beats SPY OOS in {int(W.beats_spy_OOS.sum())}.")
    P(f"  Chooser vs the pre-registered anchor (b=0.03, W): mean OOS Sharpe {W.OOS_Sharpe.mean():.4f} "
      f"vs {W.anchor_OOS_Sharpe.mean():.4f} ({W.OOS_Sharpe.mean()-W.anchor_OOS_Sharpe.mean():+.4f}); "
      f"chooser wins {int((W.OOS_Sharpe>W.anchor_OOS_Sharpe).sum())} of {len(W)}.")
    P(f"  Picked cadences: {W.pick_cad.value_counts().to_dict()}; picked bands: "
      f"{W.pick_band.value_counts().to_dict()}.  Mean regret {W.regret.mean():.4f}")

    # ---------------- KEEP tallies ----------------------------------------
    P(f"\n{'='*150}\nKEEP PATHS over all {len(grid)} cells\n{'='*150}")
    P(f"  4a passes: {int(grid.pass4a.sum())} / {len(grid)}      4b passes: "
      f"{int(grid.pass4b.sum())} / {len(grid)}")
    P("  first failing 4b bar, counts: " + str(grid.first_fail_4b.value_counts().to_dict()))
    for uname in unis:
        for con in CONS:
            d = grid[(grid.universe == uname) & (grid.con == con)]
            P(f"    {uname} {con}: 4a {int(d.pass4a.sum())}/{len(d)}, 4b {int(d.pass4b.sum())}/{len(d)}")
    if grid.pass4b.any():
        P("\n  4b passers (all of them):")
        for _, r in grid[grid.pass4b].sort_values("OOS_Sharpe", ascending=False).iterrows():
            P(f"    {r.universe} {r.con} {r.gate} b={r.band:.2f} {r.cad}  CAGR {r.CAGR:.2%} "
              f"Sharpe {r.Sharpe:.3f} MaxDD {r.MaxDD:.2%} H1/H2 {r.H1:.3f}/{r.H2:.3f} "
              f"OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.2%} "
              f"| vs control dS {r.dSharpe_ctrl:+.3f}")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {OUT}.grid.csv, {OUT}.flips.csv, {OUT}.controls.csv, "
          f"{OUT}.walkforward.csv, {OUT}.console.txt")


if __name__ == "__main__":
    main()
