#!/usr/bin/env python3
"""Idea 52 - "small-cap-slower-trend": is WHIPSAW the mechanism behind idea 49's 5.4pp
filter cost on small caps, and does slowing the filter down recover it?

The question
------------
Idea 49 (lane B, 2026-09-04) found that on the 439-name sub-$2B panel the RULES v1
eligibility filter (200d MA + vol20 < 0.60) SUBTRACTS 6.6pp/yr of CAGR from its own asset
class: equal-weighting all 439 names with no filter returns 10.2%/0.677/-36.2%, while the
same book restricted to eligible names (arm F f=1.00, always 75% invested) returns 3.5%.
Only ~1.2pp of that is turnover; ~5.4pp is the filter's own TIMING at 0 bps.

The whipsaw hypothesis: small caps cross their own 200d average far more often than mega
caps, so a hard gate sells them into every dip and re-buys after the rebound, harvesting the
loss both ways.  If that is the mechanism, a SLOWER filter - the same 200d average with a
re-entry band (hysteresis), or a slower rebalance cadence - should cut the number of
crossings and recover part of the 5.4pp.

The pre-registered test (from the QUEUE wording): the filter must not merely STOP LOSING, it
must BEAT the no-filter control.  Expect PARK.

Tuned parameters (PROTOCOL rule 4: at most two)
------------------------------------------------
    band b   : 200d hysteresis half-width.  IN above ma*(1+b), OUT below ma*(1-b), previous
               state in between (baseline.band_state, the exact RULES v2 clause-2 form).
               b = 0.00 reproduces the hard gate.   b in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}
    cadence  : rebalance frequency, {W, M, Q}.
ALL 18 grid points are reported for every arm.

Reported (NOT tuned) dimensions - the walk-forward selector runs INSIDE each of these arms
over the (band, cadence) grid only, so no third parameter is ever chosen on the data:
    gate form      MA     = 200d band only (the half idea 52 names)
                   MAVOL  = 200d band AND vol20 < 0.60 (the full RULES v1 filter, so band=0
                            /W/RESPREAD reproduces idea 49's f=1.00 arm exactly)
    construction   RESPREAD = gross/E_t across the gated-IN names, always 75% invested.
                              This is idea 49's f=1.00 construction: the filter is PURE
                              SELECTION, exposure is held constant, so any difference vs the
                              control is timing, not de-risking.
                   DEGROSS  = gross/N_live per live name, gated-out weight goes to CASH.
                              This is the RULES v2 form: selection AND exposure.
    Control (the thing the filter must beat): every live name equal-weighted at 75% gross, no
    filter of any kind.  Reported at each cadence; it is identical under both constructions.

Grid: 6 bands x 3 cadences x 2 gates x 2 constructions = 72 points, + 3 controls = 75, each
also re-run at 0 bps (turnover-vs-timing decomposition, idea 49's method) = 150 backtests.
The two headline points are re-run at 25 bps (sub-$2B names; 10 bps is optimistic).

Mechanism diagnostic (this is what actually answers "is it whipsaw?")
----------------------------------------------------------------------
For each (gate, band) the script reports gate STATE FLIPS per name per year, both daily and
as sampled on the rebalance schedule, plus realised annual turnover.  If whipsaw is the
mechanism, flips must fall steeply with b and with slower cadence, and the CAGR gap to the
control must close in step.  If flips fall and the gap does NOT close, whipsaw is refuted and
the filter's cost is a selection effect, not a churn effect.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number is read
------------------------------------------------------------------------------------
Parameters chosen on 2010-2016 ONLY, evaluated untouched 2017-2026.
    S1 (Sharpe):   highest in-sample Sharpe in the arm's 18-point grid; ties -> larger b, then
                   slower cadence.
    S2 (4b-aware): the same, restricted to points whose in-sample MaxDD is within 60% of SPY's
                   in-sample MaxDD.  "none" if no point qualifies.
OOS CAGR/Sharpe/MaxDD are reported for the picks against the baseline OOS, SPY OOS, the
no-filter control OOS, and the best OOS cell in the arm (regret).

Benchmarks and verdicts
-----------------------
    4a (beat the book):  Sharpe > the LIVE book in BOTH halves AND MaxDD no worse.  The live
                         book is RULES v2 (band 0.03, gross 0.75, weekly) on
                         research/universe.json, restricted to THIS sample window.  v2 applied
                         to the small panel itself is printed as a construction control.
    4b (capital-worthy): Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
                         CAGR >= 70% of SPY's.
There is no small-cap benchmark in the offline cache (no IWM/IJR column), so SPY is the only
4b comparand and the comparison is stated as such.  Idea 54 (lane B, 2026-09-06) bounded the
panel's survivorship: SMALL439 EW buy-and-hold beats IWM by +3.43pp/yr, so SPY understates the
passive small-cap alternative and every 4b PASS here would be weak evidence.

SURVIVORSHIP: all 483 names in data/prices_small.csv.gz trade through 2026-09-03 - a screen of
CURRENT sub-$2B constituents, no delistings, no bankruptcies.  The bias inflates the NO-FILTER
control most (it is the arm that holds the beaten-down names the gate excludes), so it runs
AGAINST the filter and a KILL of the filter is correspondingly weakened; idea 54 measured that
correction (the gate's cost shrinks but never flips sign, 0/36 and 0/36, at plausible hazards).

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSS = 0.75
MAX_VOL = 0.60
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
CADENCES = ["W", "M", "Q"]
GATES = ["MA", "MAVOL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- universe
def small_panel():
    """The 439 investable names (SPY held out as benchmark, 44 corrupted names dropped)."""
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    return px[inv], px["SPY"], sorted(bad)


# ---------------------------------------------------------------- gates and books
def gate_mask(px, gate, band):
    """Boolean frame: True = the name is IN on that day.  Never in before it is priced."""
    g = band_state(px, band)
    if gate == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g & px.notna() & px.shift(1).notna()


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def book(px, gate, band, construction):
    g = gate_mask(px, gate, band)
    if construction == "RESPREAD":                     # always GROSS invested among the IN names
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)                               # DEGROSS: gated-out weight -> cash
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


# ---------------------------------------------------------------- metric helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def stat(r, r_is, r_oos):
    m, mo = metrics(r), metrics(r_oos)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                isSharpe=metrics(r_is)["Sharpe"], isMaxDD=metrics(r_is)["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def tests_4b(s, spy_s):
    return {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
            "OOS": s["oSharpe"] > spy_s["oSharpe"],
            "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
            "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}


def fail_4b(s, spy_s):
    f = [k for k, v in tests_4b(s, spy_s).items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def main():
    px, spy_px, bad = small_panel()
    start = px.index[260]                                   # warm-up skip, same as baseline.compare
    yrs = px.index.to_series().groupby(px.index.year).count()

    print("=" * 160)
    print(f"Idea 52 small-cap-slower-trend (lane B) | {SCRIPT}")
    print("=" * 160)
    print(f"Small-cap panel: {px.shape[1]} investable tickers "
          f"({px.shape[1] + len(bad)} in file, {len(bad)} excluded for max_1d_move >= 1.0), "
          f"{px.index[0].date()} -> {px.index[-1].date()}; evaluation starts {start.date()}")
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2013:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting.")
        sys.exit(1)
    print(f"Costs {COST_BPS} bps, gross {GROSS}, next-day execution, 4b vs SPY (no small-cap "
          f"benchmark offline).  Bands {BANDS}, cadences {CADENCES}.")

    def slices(r):
        r = r.loc[start:]
        return r, r.loc[:IS_END], r.loc[OOS_START:]

    spy_r, spy_is, spy_oos = slices(spy_px.pct_change().fillna(0.0))
    spy_s = stat(spy_r, spy_is, spy_oos)

    # ---- reference books -------------------------------------------------
    print("\n" + "-" * 160)
    print("REFERENCE BOOKS")
    print("-" * 160)
    refs = {}
    for cad in CADENCES:
        rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
        refs[f"CONTROL EWall {cad}"] = (stat(*slices(rc["returns"])), rc)
    rc0 = backtest(px, control_book(px), cost_bps=0, freq="W")
    ctrl0_cagr = metrics(rc0["returns"].loc[start:])["CAGR"]

    # live book: RULES v2 on universe.json, restricted to this window
    px_u = load_universe()
    rv2 = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")
    live_r = rv2["returns"].reindex(px.index).fillna(0.0)
    live_s = stat(*slices(live_r))
    # construction control: v2 applied to the small panel itself
    rv2s = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")
    v2small_s = stat(*slices(rv2s["returns"]))

    ref_rows = {k: v[0] for k, v in refs.items()}
    ref_rows["RULES v2 on universe.json (LIVE BOOK, 4a comparand)"] = live_s
    ref_rows["RULES v2 on the small panel (construction control)"] = v2small_s
    ref_rows["SPY (4b comparand)"] = spy_s
    print(fmt(pd.DataFrame(ref_rows).T))
    print(f"\n4b bars from SPY: H1>{spy_s['H1']:.3f}, H2>{spy_s['H2']:.3f}, OOS Sharpe>{spy_s['oSharpe']:.3f}, "
          f"MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%}, CAGR>={0.70 * spy_s['CAGR']:.2%}")
    print(f"Idea 49 reproduction check - EWall W control: CAGR {ref_rows['CONTROL EWall W']['CAGR']:.1%} "
          f"(idea 49: 10.2%), Sharpe {ref_rows['CONTROL EWall W']['Sharpe']:.3f} (0.677), "
          f"MaxDD {ref_rows['CONTROL EWall W']['MaxDD']:.1%} (-36.2%); at 0 bps CAGR {ctrl0_cagr:.1%}")

    # ---- mechanism: how often does the gate flip? ------------------------
    print("\n" + "-" * 160)
    print("MECHANISM - gate state flips per name per year (daily, and as SAMPLED on the rebalance schedule)")
    print("-" * 160)
    live = live_mask(px)
    years = len(px.loc[start:]) / 252
    flip_rows = []
    gates_cache = {}
    for gate in GATES:
        for b in BANDS:
            g = gate_mask(px, gate, b)
            gates_cache[(gate, b)] = g
            gs = g.loc[start:]
            ls = live.loc[start:]
            daily = ((gs != gs.shift(1)) & ls & ls.shift(1)).sum().sum() / (ls.sum(axis=1).mean() * years)
            row = dict(gate=gate, band=b, mean_in_pct=100 * gs.sum(axis=1).mean() / ls.sum(axis=1).mean(),
                       flips_daily=daily)
            for cad in CADENCES:
                from engine import rebalance_mask
                m = rebalance_mask(px.index, cad).reindex(px.index).fillna(False)
                gsub = g.loc[start:][m.loc[start:].values]
                lsub = live.loc[start:][m.loc[start:].values]
                row[f"flips_{cad}"] = ((gsub != gsub.shift(1)) & lsub & lsub.shift(1)).sum().sum() / (
                    ls.sum(axis=1).mean() * years)
            flip_rows.append(row)
    flips = pd.DataFrame(flip_rows)
    print(fmt(flips.set_index(["gate", "band"])))

    # ---- the grid --------------------------------------------------------
    print("\n" + "-" * 160)
    print("GRID - all 72 points (6 bands x 3 cadences x 2 gate forms x 2 constructions), 10 bps and 0 bps")
    print("-" * 160)
    rows = []
    for con in CONSTRUCTIONS:
        for gate in GATES:
            for cad in CADENCES:
                cbase = refs[f"CONTROL EWall {cad}"][0]
                for b in BANDS:
                    w = book(px, gate, b, con)
                    res = backtest(px, w, cost_bps=COST_BPS, freq=cad)
                    r, r_is, r_oos = slices(res["returns"])
                    s = stat(r, r_is, r_oos)
                    r0 = backtest(px, w, cost_bps=0, freq=cad)["returns"].loc[start:]
                    turn = res["turnover"].loc[start:].sum() / years
                    rows.append(dict(con=con, gate=gate, cad=cad, band=b, **s,
                                     dCAGR_ctrl=s["CAGR"] - cbase["CAGR"],
                                     dSharpe_ctrl=s["Sharpe"] - cbase["Sharpe"],
                                     dMaxDD_ctrl=s["MaxDD"] - cbase["MaxDD"],
                                     CAGR0=metrics(r0)["CAGR"], turn_yr=turn,
                                     p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
            "dCAGR_ctrl", "dSharpe_ctrl", "dMaxDD_ctrl", "CAGR0", "turn_yr", "p4a", "f4b"]
    for con in CONSTRUCTIONS:
        for gate in GATES:
            sub = G[(G.con == con) & (G.gate == gate)].set_index(["cad", "band"])[cols]
            print(f"\n--- {con} / gate {gate} ---   (dX_ctrl = idea vs the no-filter EWall control at the SAME cadence)")
            print(fmt(sub))

    print("\n" + "-" * 160)
    print("TURNOVER-vs-TIMING DECOMPOSITION (idea 49's method): filter cost at 10 bps vs at 0 bps")
    print("-" * 160)
    dec = []
    for con in CONSTRUCTIONS:
        for gate in GATES:
            for cad in CADENCES:
                cb = refs[f"CONTROL EWall {cad}"][0]["CAGR"]
                cb0 = metrics(backtest(px, control_book(px), cost_bps=0, freq=cad)["returns"].loc[start:])["CAGR"]
                for b in BANDS:
                    g = G[(G.con == con) & (G.gate == gate) & (G.cad == cad) & (G.band == b)].iloc[0]
                    dec.append(dict(con=con, gate=gate, cad=cad, band=b,
                                    total_cost_pp=100 * (cb - g.CAGR),
                                    timing_cost_pp=100 * (cb0 - g.CAGR0),
                                    turnover_cost_pp=100 * ((cb - g.CAGR) - (cb0 - g.CAGR0))))
    D = pd.DataFrame(dec)
    print(fmt(D.set_index(["con", "gate", "cad", "band"])))
    r49 = D[(D.con == "RESPREAD") & (D.gate == "MAVOL") & (D.cad == "W") & (D.band == 0.0)].iloc[0]
    print(f"\nIdea 49's cell (RESPREAD/MAVOL/W/band=0.00, = its f=1.00 arm): total "
          f"{r49.total_cost_pp:.2f}pp (idea 49: 6.6pp), timing {r49.timing_cost_pp:.2f}pp (5.4pp), "
          f"turnover {r49.turnover_cost_pp:.2f}pp (1.2pp)")

    # ---- the pre-registered question ------------------------------------
    print("\n" + "-" * 160)
    print("THE PRE-REGISTERED QUESTION: does any slower filter BEAT the no-filter control?")
    print("-" * 160)
    beat = G[(G.dCAGR_ctrl > 0) & (G.dSharpe_ctrl > 0)]
    print(f"Points beating the matched-cadence control on BOTH CAGR and Sharpe: {len(beat)} of {len(G)}")
    if len(beat):
        print(fmt(beat.set_index(["con", "gate", "cad", "band"])[cols]))
    print(f"Points beating it on Sharpe alone: {(G.dSharpe_ctrl > 0).sum()} of {len(G)}; "
          f"on CAGR alone: {(G.dCAGR_ctrl > 0).sum()} of {len(G)}")
    print(f"Best dSharpe_ctrl {G.dSharpe_ctrl.max():+.3f} at "
          f"{G.loc[G.dSharpe_ctrl.idxmax(), ['con', 'gate', 'cad', 'band']].to_dict()}")
    print(f"Best dCAGR_ctrl  {G.dCAGR_ctrl.max():+.2%} at "
          f"{G.loc[G.dCAGR_ctrl.idxmax(), ['con', 'gate', 'cad', 'band']].to_dict()}")
    print("\nDoes the band recover the cost?  timing cost (pp of CAGR vs the 0-bps control) by band, "
          "RESPREAD (pure selection, exposure held constant):")
    piv = D[D.con == "RESPREAD"].pivot_table(index=["gate", "cad"], columns="band", values="timing_cost_pp")
    print(fmt(piv))
    print("\nSame, DEGROSS (selection + exposure):")
    print(fmt(D[D.con == "DEGROSS"].pivot_table(index=["gate", "cad"], columns="band", values="timing_cost_pp")))
    print("\nFlips vs recovery, MA gate, weekly, RESPREAD (the whipsaw test - flips must fall AND cost must fall):")
    fl = flips[flips.gate == "MA"].set_index("band")[["flips_daily", "flips_W", "mean_in_pct"]]
    cst = D[(D.con == "RESPREAD") & (D.gate == "MA") & (D.cad == "W")].set_index("band")[["timing_cost_pp"]]
    print(fmt(fl.join(cst)))

    # ---- verdict counts --------------------------------------------------
    print("\n" + "-" * 160)
    print("VERDICT COUNTS")
    print("-" * 160)
    print(f"4a passes (vs RULES v2 on universe.json): {int(G.p4a.sum())} of {len(G)}")
    print(f"4b passes (vs SPY): {int(G.p4b.sum())} of {len(G)}")
    print("4b failure modes:\n" + G.f4b.value_counts().to_string())
    if G.p4b.any():
        print("\n4b PASSING points:\n" + fmt(G[G.p4b].set_index(["con", "gate", "cad", "band"])[cols]))
    for k, v in ref_rows.items():
        if k.startswith("CONTROL"):
            print(f"  {k}: 4a {verdict_4a(v, live_s)}, 4b fails [{fail_4b(v, spy_s)}]")

    # ---- walk-forward (PROTOCOL rule 8) ----------------------------------
    print("\n" + "-" * 160)
    print("WALK-FORWARD (rule 8): (band, cadence) chosen on 2010-2016 only, evaluated 2017-2026 untouched")
    print("-" * 160)
    dd_cap_is = 0.60 * abs(metrics(spy_is)["MaxDD"])
    wf = []
    for con in CONSTRUCTIONS:
        for gate in GATES:
            sub = G[(G.con == con) & (G.gate == gate)].copy()
            sub["tie"] = list(zip(sub.isSharpe, sub.band, sub.cad.map({"W": 0, "M": 1, "Q": 2})))
            s1 = sub.sort_values("tie", ascending=False).iloc[0]
            q = sub[sub.isMaxDD.abs() <= dd_cap_is]
            s2 = q.sort_values("tie", ascending=False).iloc[0] if len(q) else None
            best = sub.sort_values("oSharpe", ascending=False).iloc[0]
            for tag, p in (("S1 Sharpe", s1), ("S2 4b-aware", s2)):
                if p is None:
                    wf.append(dict(con=con, gate=gate, sel=tag, pick="none (no IS point met the DD cap)"))
                    continue
                wf.append(dict(con=con, gate=gate, sel=tag, pick=f"b={p.band:.2f}/{p.cad}",
                               isSharpe=p.isSharpe, oCAGR=p.oCAGR, oSharpe=p.oSharpe, oMaxDD=p.oMaxDD,
                               best_oSharpe=best.oSharpe, best_pick=f"b={best.band:.2f}/{best.cad}",
                               regret=p.oSharpe - best.oSharpe))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["con", "gate", "sel"])))
    print(f"\nOOS comparands  SPY: CAGR {spy_s['oCAGR']:.2%} Sharpe {spy_s['oSharpe']:.3f} MaxDD {spy_s['oMaxDD']:.1%}"
          f"  |  LIVE BOOK (v2/U56): CAGR {live_s['oCAGR']:.2%} Sharpe {live_s['oSharpe']:.3f} "
          f"MaxDD {live_s['oMaxDD']:.1%}")
    for cad in CADENCES:
        c = refs[f"CONTROL EWall {cad}"][0]
        print(f"  NO-FILTER CONTROL {cad}: OOS CAGR {c['oCAGR']:.2%} Sharpe {c['oSharpe']:.3f} MaxDD {c['oMaxDD']:.1%}")
    beats_ctrl = [r for _, r in W.dropna(subset=["oSharpe"]).iterrows()
                  if r.oSharpe > refs["CONTROL EWall W"][0]["oSharpe"]]
    print(f"Walk-forward picks whose OOS Sharpe beats the weekly no-filter control "
          f"({refs['CONTROL EWall W'][0]['oSharpe']:.3f}): {len(beats_ctrl)} of {len(W.dropna(subset=['oSharpe']))}")

    # ---- cost sensitivity on the headline points -------------------------
    print("\n" + "-" * 160)
    print("COST SENSITIVITY (sub-$2B names; 10 bps is optimistic)")
    print("-" * 160)
    heads = [("CONTROL", None, None, "W"), ("RESPREAD", "MAVOL", 0.00, "W"),
             ("RESPREAD", "MA", G[(G.con == 'RESPREAD') & (G.gate == 'MA')].sort_values('Sharpe').iloc[-1].band,
              G[(G.con == 'RESPREAD') & (G.gate == 'MA')].sort_values('Sharpe').iloc[-1].cad),
             ("DEGROSS", "MA", G[(G.con == 'DEGROSS') & (G.gate == 'MA')].sort_values('Sharpe').iloc[-1].band,
              G[(G.con == 'DEGROSS') & (G.gate == 'MA')].sort_values('Sharpe').iloc[-1].cad)]
    crows = []
    for con, gate, b, cad in heads:
        w = control_book(px) if con == "CONTROL" else book(px, gate, b, con)
        row = dict(point=f"{con}/{gate}/b={b}/{cad}" if con != "CONTROL" else "CONTROL EWall/W")
        for c in (0, 10, 25, 50):
            m = metrics(backtest(px, w, cost_bps=c, freq=cad)["returns"].loc[start:])
            row[f"CAGR@{c}"] = m["CAGR"]; row[f"Sharpe@{c}"] = m["Sharpe"]
        crows.append(row)
    print(fmt(pd.DataFrame(crows).set_index("point")))

    G.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".grid.csv"), index=False)
    D.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".decomp.csv"), index=False)
    flips.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".flips.csv"), index=False)
    W.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".walkforward.csv"), index=False)

    print("\n" + "=" * 160)
    print("LEADERBOARD rows written to console block below; CSVs written beside the script.")
    print("=" * 160)
    lb = []
    for _, g in G.iterrows():
        v = ("KEEP-4b" if g.p4b else ("KEEP-4a" if g.p4a else f"KILL 4a / KILL 4b ({g.f4b})"))
        lb.append(f"| 2026-09-06 | 52 {g.con} {g.gate} b={g.band:.2f} {g.cad} (small panel) | {g.CAGR:.1%} | "
                  f"{g.Sharpe:.2f} | {g.MaxDD:.1%} | {g.H1:.2f} / {g.H2:.2f} | "
                  f"{live_s['Sharpe']:.2f} ({live_s['H1']:.2f}/{live_s['H2']:.2f}) | {v} | "
                  f"research/backtests/{SCRIPT} |")
    print("\n".join(lb))


if __name__ == "__main__":
    main()
