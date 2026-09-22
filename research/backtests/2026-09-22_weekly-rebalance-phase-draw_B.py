#!/usr/bin/env python3
"""Idea 2274 (lane B, 2026-09-22) — IS THE STANDING 4b CANDIDATE A REBALANCE-PHASE DRAW,
AND DOES TRANCHING ACROSS PHASES FIX IT?

WHERE THIS COMES FROM.  CHANGELOG 2026-09-22 / idea 2264 filed the record's only standing
KEEP-4b candidate: the live RULES v2 band book on u56 at gross 1.00 instead of 0.75, nothing
else changed, OOS 12.67% / 1.2760 / -15.91% with OOS margins DD +4.32 pp and CAGR +1.97 pp.
Every weekly number in this record — that candidate's included — sits on ONE rebalance phase:
`engine.rebalance_mask(freq='W')` fires on the last trading day of each ISO week (Friday), and
the other four weekdays have never been priced.  Idea 963 measured phase-family CAGR spreads of
median 3.04 pp (M) and 4.37 pp (Q).  If the WEEKLY spread is of that order, the candidate's
margins are inside its own phase noise and the pass is a draw, not a result.

THE GRID.  2 panels (u56, b136) x 4 gross rungs {0.25, 0.50, 0.75, 1.00} x 6 phase arms
(W0..W4 plus PHAVG, the 5-tranche phase-averaged book) x 4 cost rungs {0, 10, 25, 50} bps
= 192 published cells, all in `.grid.csv`.  TWO TUNED DIALS AND NO MORE: **GROSS and PHASE**.
Band (3%), cadence (weekly), delay (t+1), panel and cost are reported, never selected.
PROTOCOL rule 2's no-leverage cap is respected: gross <= 1.00, no shorting.

PHASE DEFINITION.  Phase p in {0..4}: weeks are grouped on `(idx - p days).to_period('W')` and
the mask fires on the last trading day of each shifted week.  p = 0 is EXACTLY engine's
freq='W' (gate G1).  p = 1..4 walk the rebalance weekday back one day at a time.  Every arm
rebalances once per 7 calendar days; only WHICH day moves.

PHAVG.  Five equal sleeves, sleeve i rebalancing on phase i, never rebalanced against each
other (so it costs no extra turnover): portfolio equity = mean of the five sleeve equities.
This is an actually-executable, ZERO-PARAMETER control on the phase axis.

Outputs: .grid.csv (192 cells), .phase_spread.csv, .walkforward.csv, .gates.csv, .console.txt
"""
import sys, itertools, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
BAND = 0.03
GROSS = [0.25, 0.50, 0.75, 1.00]
PHASES = [0, 1, 2, 3, 4]
COSTS = [0, 10, 25, 50]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
KAPPA = 0.60          # PROTOCOL 4b's own delta, pre-registered 2026-09-04, NOT chosen here
CAGR_FLOOR = 0.70     # PROTOCOL 4b

_log = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _log.append(s)

# ---------------------------------------------------------------- harness
def phase_mask(idx: pd.DatetimeIndex, p: int) -> pd.Series:
    """Last trading day of each week, with week boundaries shifted back p days. p=0 == engine 'W'."""
    key = pd.Series((idx - pd.Timedelta(days=p)).to_period("W"), index=idx)
    return key != key.shift(-1)

def bt_mask(prices: pd.DataFrame, weights: pd.DataFrame, mask: pd.Series):
    """engine.backtest with a SUPPLIED rebalance mask and zero cost; returns gross returns
    and the turnover series so every cost rung is exact (the engine never feeds cost back
    into positions)."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    m = mask.shift(1, fill_value=False)
    held = np.zeros((len(prices), prices.shape[1]))
    cur = np.zeros(prices.shape[1]); turn = np.zeros(len(prices))
    R = rets.values; W = w_target.values; M = m.values
    for i in range(len(prices)):
        if M[i] or i == 0:
            new = W[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + R[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    port = (held * R).sum(axis=1)
    return pd.Series(port, index=prices.index), pd.Series(turn, index=prices.index)

def net(gross_ret, turn, bps):
    return gross_ret - turn * bps / 1e4

def band_book(px, gross):
    return rules_v2_weights(px, band=BAND, gross=gross)

# ---------------------------------------------------------------- legs
def legs(r, spy, start_oos=OOS_START):
    """PROTOCOL 4b legs on the window `r` covers, plus the halves of that window."""
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    s, s1, s2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    ro, so = r.loc[start_oos:], spy.loc[start_oos:]
    mo, so_m = metrics(ro), metrics(so)
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
        spyCAGR=s["CAGR"], spySharpe=s["Sharpe"], spyMaxDD=s["MaxDD"], spyH1=s1["Sharpe"], spyH2=s2["Sharpe"],
        oosSharpe=mo["Sharpe"], spyOosSharpe=so_m["Sharpe"],
        L_H1=m1["Sharpe"] > s1["Sharpe"], L_H2=m2["Sharpe"] > s2["Sharpe"],
        L_OOS=mo["Sharpe"] > so_m["Sharpe"],
        L_DD=abs(m["MaxDD"]) <= KAPPA * abs(s["MaxDD"]),
        L_CAGR=m["CAGR"] >= CAGR_FLOOR * s["CAGR"],
        dd_margin=KAPPA * abs(s["MaxDD"]) - abs(m["MaxDD"]),
        cagr_margin=m["CAGR"] - CAGR_FLOOR * s["CAGR"],
    )

def pass4b(d): return bool(d["L_H1"] and d["L_H2"] and d["L_OOS"] and d["L_DD"] and d["L_CAGR"])

def legs_window(r, spy):
    """4b read ENTIRELY inside one window (used for the OOS leg-set): halves of that window,
    and the 'OOS' Sharpe leg collapses to the window's own Sharpe."""
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    s, s1, s2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
        spyCAGR=s["CAGR"], spySharpe=s["Sharpe"], spyMaxDD=s["MaxDD"],
        L_H1=m1["Sharpe"] > s1["Sharpe"], L_H2=m2["Sharpe"] > s2["Sharpe"],
        L_OOS=m["Sharpe"] > s["Sharpe"],
        L_DD=abs(m["MaxDD"]) <= KAPPA * abs(s["MaxDD"]),
        L_CAGR=m["CAGR"] >= CAGR_FLOOR * s["CAGR"],
        dd_margin=KAPPA * abs(s["MaxDD"]) - abs(m["MaxDD"]),
        cagr_margin=m["CAGR"] - CAGR_FLOOR * s["CAGR"],
    )

def pass4a(d, b):
    """PROTOCOL 4a vs the LIVE book: Sharpe > live in BOTH halves and MaxDD no worse."""
    return bool(d["H1"] > b["H1"] and d["H2"] > b["H2"] and d["MaxDD"] >= b["MaxDD"])

# ---------------------------------------------------------------- run
def main():
    gates = []
    panels = {"u56": load_universe(), "b136": load_universe(broad=True)}

    say("=" * 100)
    say("IDEA 2274 — is the standing 4b candidate a REBALANCE-PHASE DRAW? (lane B, 2026-09-22)")
    say("=" * 100)

    # ---- G1: phase 0 == engine's freq='W'
    idx = panels["u56"].index
    g1 = int((phase_mask(idx, 0).values != rebalance_mask(idx, "W").values).sum())
    gates.append(("G1 phase0 mask == engine rebalance_mask(W), mismatches", g1, g1 == 0))
    say(f"G1  phase-0 mask vs engine freq='W': {g1} mismatches of {len(idx)}  -> {'PASS' if g1==0 else 'FAIL'}")
    for p in PHASES:
        wd = pd.Series(idx[phase_mask(idx, p).values]).dt.dayofweek.value_counts().sort_index()
        say(f"    phase W{p}: {int(phase_mask(idx,p).sum())} rebalance days, weekday mix "
            + ", ".join(f"{'MonTueWedThuFri'[3*k:3*k+3]}={v}" for k, v in wd.items() if k < 5))

    # ---- store every (panel, gross, phase) zero-cost run once
    raw = {}
    for pn, px in panels.items():
        for g in GROSS:
            w = band_book(px, g)
            for p in PHASES:
                raw[(pn, g, p)] = bt_mask(px, w, phase_mask(px.index, p))
        say(f"    ran {len(GROSS)*len(PHASES)} zero-cost books on {pn}")

    # ---- G2: harness == engine.backtest on the LIVE book (gross 0.75, phase 0, 10 bps)
    px = panels["u56"]
    gr, tn = raw[("u56", 0.75, 0)]
    eng = backtest(px, band_book(px, 0.75), cost_bps=10, freq="W")["returns"]
    d2 = float(np.abs(net(gr, tn, 10) - eng).max())
    gates.append(("G2 harness == engine.backtest, max|dr|", d2, d2 < 1e-12))
    say(f"G2  harness vs engine.backtest (u56, RULES v2, 10 bps): max|dr| = {d2:.3e}  -> {'PASS' if d2<1e-12 else 'FAIL'}")

    # ---- G3: derived cost ladder == full re-simulation
    eng50 = backtest(px, band_book(px, 1.00), cost_bps=50, freq="W")["returns"]
    gr1, tn1 = raw[("u56", 1.00, 0)]
    d3 = float(np.abs(net(gr1, tn1, 50) - eng50).max())
    gates.append(("G3 derived 50 bps rung == re-simulation, max|dr|", d3, d3 < 1e-12))
    say(f"G3  derived cost rung vs re-simulation (u56, gross 1.00, 50 bps): max|dr| = {d3:.3e}  -> {'PASS' if d3<1e-12 else 'FAIL'}")

    # ---- G4: gross 0.75 book IS the live book
    w_live = rules_v2_weights(px)
    d4 = float(np.abs(band_book(px, 0.75) - w_live).values.max())
    gates.append(("G4 gross 0.75 book == baseline.rules_v2_weights, max|dw|", d4, d4 == 0.0))
    say(f"G4  gross-0.75 arm vs baseline.rules_v2_weights: max|dw| = {d4:.3e}  -> {'PASS' if d4==0.0 else 'FAIL'}")

    # ---- build the grid
    rows = []
    spy_all = {pn: panels[pn]["SPY"].pct_change().fillna(0.0) for pn in panels}
    starts = {pn: panels[pn].index[260] for pn in panels}

    def series(pn, g, arm, bps):
        """net daily returns of one arm, trimmed to the common start."""
        st = starts[pn]
        if arm == "PHAVG":
            eqs = []
            for p in PHASES:
                gr, tn = raw[(pn, g, p)]
                eqs.append((1 + net(gr, tn, bps).loc[st:]).cumprod())
            eq = sum(eqs) / len(eqs)
            return eq.pct_change().fillna(0.0)
        gr, tn = raw[(pn, g, arm)]
        return net(gr, tn, bps).loc[st:]

    def turn_of(pn, g, arm):
        st = starts[pn]
        if arm == "PHAVG":
            return float(np.mean([raw[(pn, g, p)][1].loc[st:].sum() for p in PHASES]) / (len(raw[(pn,g,0)][1].loc[st:]) / 252))
        t = raw[(pn, g, arm)][1].loc[st:]
        return float(t.sum() / (len(t) / 252))

    # G5: PHAVG equity-mean vs return-mean
    a = series("u56", 1.00, "PHAVG", 10)
    b = pd.concat([series("u56", 1.00, p, 10) for p in PHASES], axis=1).mean(axis=1)
    d5 = float(np.abs((1 + a).cumprod().iloc[-1] / (1 + b).cumprod().iloc[-1] - 1))
    gates.append(("G5 PHAVG buy-and-hold tranche vs daily-rebalanced mix, |dTotal|", d5, True))
    say(f"G5  PHAVG (tranche, executable) vs daily-rebalanced mix, terminal-wealth gap: {d5:.4%}  -> reported")

    base_cache = {}
    for pn in panels:
        for bps in COSTS:
            gr, tn = raw[(pn, 0.75, 0)]
            base_cache[(pn, bps)] = net(gr, tn, bps).loc[starts[pn]:]

    for pn in panels:
        spy = spy_all[pn].loc[starts[pn]:]
        for g, arm, bps in itertools.product(GROSS, PHASES + ["PHAVG"], COSTS):
            r = series(pn, g, arm, bps)
            f = legs(r, spy)
            o = legs_window(r.loc[OOS_START:], spy.loc[OOS_START:])
            bl = legs(base_cache[(pn, bps)], spy)
            blo = legs_window(base_cache[(pn, bps)].loc[OOS_START:], spy.loc[OOS_START:])
            rows.append(dict(
                panel=pn, gross=g, phase=("PHAVG" if arm == "PHAVG" else f"W{arm}"), bps=bps,
                CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=f["H1"], H2=f["H2"],
                oos_CAGR=o["CAGR"], oos_Sharpe=o["Sharpe"], oos_MaxDD=o["MaxDD"],
                oos_H1=o["H1"], oos_H2=o["H2"],
                turnover=turn_of(pn, g, arm),
                L_H1=f["L_H1"], L_H2=f["L_H2"], L_OOS=f["L_OOS"], L_DD=f["L_DD"], L_CAGR=f["L_CAGR"],
                pass4b_full=pass4b(f),
                o_L_H1=o["L_H1"], o_L_H2=o["L_H2"], o_L_OOS=o["L_OOS"], o_L_DD=o["L_DD"], o_L_CAGR=o["L_CAGR"],
                pass4b_oos=pass4b(o),
                dd_margin_full=f["dd_margin"], cagr_margin_full=f["cagr_margin"],
                dd_margin_oos=o["dd_margin"], cagr_margin_oos=o["cagr_margin"],
                pass4a_full=pass4a(f, bl), pass4a_oos=pass4a(o, blo),
                spy_CAGR=f["spyCAGR"], spy_Sharpe=f["spySharpe"], spy_MaxDD=f["spyMaxDD"],
                spy_oos_CAGR=o["spyCAGR"], spy_oos_Sharpe=o["spySharpe"], spy_oos_MaxDD=o["spyMaxDD"],
                live_Sharpe=bl["Sharpe"], live_CAGR=bl["CAGR"], live_MaxDD=bl["MaxDD"],
                live_oos_Sharpe=blo["Sharpe"], live_oos_CAGR=blo["CAGR"], live_oos_MaxDD=blo["MaxDD"],
            ))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    n_exp = len(panels) * len(GROSS) * (len(PHASES) + 1) * len(COSTS)
    gates.append(("G6 cells published", len(G), len(G) == n_exp))
    say(f"G6  cells published: {len(G)} of {n_exp}  -> {'PASS' if len(G)==n_exp else 'FAIL'}")

    # ---- G7: reproduce 2264's committed candidate numbers
    c = G[(G.panel == "u56") & (G.gross == 1.00) & (G.phase == "W0") & (G.bps == 10)].iloc[0]
    l = G[(G.panel == "u56") & (G.gross == 0.75) & (G.phase == "W0") & (G.bps == 10)].iloc[0]
    ref = dict(cand_CAGR=0.1153, cand_Sharpe=1.2009, cand_DD=-0.1591, cand_oCAGR=0.1267, cand_oSharpe=1.2760,
               live_CAGR=0.0862, live_Sharpe=1.2010, live_DD=-0.1205, spy_CAGR=0.1514, spy_Sharpe=0.8851, spy_DD=-0.3372)
    got = dict(cand_CAGR=c.CAGR, cand_Sharpe=c.Sharpe, cand_DD=c.MaxDD, cand_oCAGR=c.oos_CAGR, cand_oSharpe=c.oos_Sharpe,
               live_CAGR=l.CAGR, live_Sharpe=l.Sharpe, live_DD=l.MaxDD, spy_CAGR=c.spy_CAGR, spy_Sharpe=c.spy_Sharpe, spy_DD=c.spy_MaxDD)
    d7 = max(abs(got[k] - ref[k]) for k in ref)
    gates.append(("G7 reproduces idea 2264's committed cells, max|d|", d7, d7 < 5e-4))
    say(f"G7  reproduction of idea 2264's committed numbers: max|d| = {d7:.2e}  -> {'PASS' if d7<5e-4 else 'FAIL'}")
    for k in ref: say(f"      {k:14s} ref {ref[k]:+.4f}  got {got[k]:+.4f}")

    # ---- PART 1: the phase spread
    say("\n" + "=" * 100)
    say("PART 1 — THE PHASE SPREAD.  Five weekly phases of the SAME book, nothing else moved.")
    say("=" * 100)
    ph = G[G.phase != "PHAVG"]
    sp = (ph.groupby(["panel", "gross", "bps"])
            .agg(oosCAGR_min=("oos_CAGR", "min"), oosCAGR_max=("oos_CAGR", "max"),
                 oosSharpe_min=("oos_Sharpe", "min"), oosSharpe_max=("oos_Sharpe", "max"),
                 oosDD_min=("oos_MaxDD", "min"), oosDD_max=("oos_MaxDD", "max"),
                 fullCAGR_min=("CAGR", "min"), fullCAGR_max=("CAGR", "max"),
                 fullSharpe_min=("Sharpe", "min"), fullSharpe_max=("Sharpe", "max"),
                 n4b_full=("pass4b_full", "sum"), n4b_oos=("pass4b_oos", "sum"),
                 n4a=("pass4a_full", "sum")).reset_index())
    for col, lo, hi in [("oosCAGR", "oosCAGR_min", "oosCAGR_max"), ("oosSharpe", "oosSharpe_min", "oosSharpe_max"),
                        ("oosDD", "oosDD_min", "oosDD_max"), ("fullCAGR", "fullCAGR_min", "fullCAGR_max"),
                        ("fullSharpe", "fullSharpe_min", "fullSharpe_max")]:
        sp[col + "_spread"] = sp[hi] - sp[lo]
    sp.to_csv(OUT / f"{STEM}.phase_spread.csv", index=False)

    say("\nPhase spread (max - min over W0..W4) by (panel, gross, cost):")
    say(sp[["panel", "gross", "bps", "fullCAGR_spread", "fullSharpe_spread", "oosCAGR_spread",
            "oosSharpe_spread", "oosDD_spread", "n4b_full", "n4b_oos", "n4a"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\nMedian phase spread over all {len(sp)} (panel, gross, cost) families:")
    for col in ["fullCAGR_spread", "oosCAGR_spread", "fullSharpe_spread", "oosSharpe_spread", "oosDD_spread"]:
        say(f"    {col:20s} median {sp[col].median():.4f}   max {sp[col].max():.4f}")

    # the candidate's own family
    fam = sp[(sp.panel == "u56") & (sp.gross == 1.00) & (sp.bps == 10)].iloc[0]
    say(f"\nTHE CANDIDATE'S OWN FAMILY (u56, gross 1.00, 10 bps):")
    say(f"    OOS CAGR   W0..W4 span {fam.oosCAGR_min:.2%} .. {fam.oosCAGR_max:.2%}  = {fam.oosCAGR_spread*100:.2f} pp")
    say(f"    OOS Sharpe W0..W4 span {fam.oosSharpe_min:.4f} .. {fam.oosSharpe_max:.4f} = {fam.oosSharpe_spread:.4f}")
    say(f"    OOS MaxDD  W0..W4 span {fam.oosDD_min:.2%} .. {fam.oosDD_max:.2%}  = {fam.oosDD_spread*100:.2f} pp")
    say(f"    idea 2264 quoted OOS margins: DD +4.32 pp, CAGR +1.97 pp")
    cf = G[(G.panel == "u56") & (G.gross == 1.00) & (G.bps == 10) & (G.phase != "PHAVG")]
    say("\n    per-phase reading of the candidate cell:")
    say(cf[["phase", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD",
            "cagr_margin_oos", "dd_margin_oos", "pass4b_full", "pass4b_oos", "turnover"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pa = G[(G.panel == "u56") & (G.gross == 1.00) & (G.bps == 10) & (G.phase == "PHAVG")].iloc[0]
    say(f"\n    PHAVG (5 tranches): FULL {pa.CAGR:.2%} / {pa.Sharpe:.4f} / {pa.MaxDD:.2%}  "
        f"OOS {pa.oos_CAGR:.2%} / {pa.oos_Sharpe:.4f} / {pa.oos_MaxDD:.2%}  "
        f"4b full {bool(pa.pass4b_full)} oos {bool(pa.pass4b_oos)}  turnover {pa.turnover:.2f}x/yr")

    # ---- PART 2: KEEP counts
    say("\n" + "=" * 100)
    say("PART 2 — KEEP PATHS over all 192 cells")
    say("=" * 100)
    say(f"  4a (vs live RULES v2, both halves + MaxDD): {int(G.pass4a_full.sum())} of {len(G)} full, "
        f"{int(G.pass4a_oos.sum())} of {len(G)} OOS-window")
    say(f"  4b FULL: {int(G.pass4b_full.sum())} of {len(G)};  4b OOS: {int(G.pass4b_oos.sum())} of {len(G)};  "
        f"BOTH(FULL & OOS): {int((G.pass4b_full & G.pass4b_oos).sum())};  "
        f"BOTH(4a & 4b): {int((G.pass4a_full & G.pass4b_full & G.pass4b_oos).sum())}")
    fails = G[~G.pass4b_full]
    say(f"  binding legs over the {len(fails)} 4b-FULL fails: "
        + ", ".join(f"{k} {int((~fails[k]).sum())}" for k in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]))
    say("\n  4b FULL&OOS pass count by phase arm:")
    say(G.groupby("phase").agg(n4b_full=("pass4b_full", "sum"), n4b_oos=("pass4b_oos", "sum"),
                               n_both=("pass4b_full", lambda s: 0)).drop(columns="n_both").to_string())
    both = G[G.pass4b_full & G.pass4b_oos]
    say(f"\n  the {len(both)} cells clearing 4b in FULL and OOS:")
    if len(both):
        say(both[["panel", "gross", "phase", "bps", "CAGR", "Sharpe", "MaxDD", "oos_CAGR", "oos_Sharpe",
                  "oos_MaxDD", "cagr_margin_oos", "dd_margin_oos", "turnover"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- PART 3: rule 8 walk-forward
    say("\n" + "=" * 100)
    say("PART 3 — RULE 8 WALK-FORWARD.  Choose on 2009-2016 only, read 2017-2026 once.")
    say("=" * 100)
    wf = []
    for pn in panels:
        spy = spy_all[pn].loc[starts[pn]:]
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        is_dd_cap = KAPPA * abs(metrics(spy_is)["MaxDD"])
        for bps in COSTS:
            cand = {}
            for g, arm in itertools.product(GROSS, PHASES + ["PHAVG"]):
                r = series(pn, g, arm, bps)
                mi = metrics(r.loc[:IS_END])
                cand[(g, "PHAVG" if arm == "PHAVG" else f"W{arm}")] = (mi["Sharpe"], mi["MaxDD"], mi["CAGR"])
            picks = {}
            # C_LIVE: the shipped book, zero information
            picks["C_LIVE"] = (0.75, "W0")
            # C_SHARPE: habitual chooser over BOTH dials
            picks["C_SHARPE"] = max(cand, key=lambda k: cand[k][0])
            # C_DDB (idea 2264): largest gross whose IS MaxDD is inside the 4b DD budget;
            #                    phase then by IS Sharpe within that gross
            ok_g = [g for g in GROSS if any(abs(cand[(g, p)][1]) <= is_dd_cap
                                            for p in [f"W{x}" for x in PHASES] + ["PHAVG"])]
            gsel = max(ok_g) if ok_g else min(GROSS)
            psel = max([p for p in [f"W{x}" for x in PHASES] + ["PHAVG"] if abs(cand[(gsel, p)][1]) <= is_dd_cap]
                       or [f"W{x}" for x in PHASES], key=lambda p: cand[(gsel, p)][0])
            picks["C_DDB"] = (gsel, psel)
            # C_DDB_PHAVG: same gross, phase axis NOT chosen at all — the tranche
            picks["C_DDB_PHAVG"] = (gsel, "PHAVG")
            # C_ORACLE: best OOS Sharpe, reported as an upper bound only
            orc = max(cand, key=lambda k: metrics(series(pn, k[0], 0 if k[1] == "W0" else
                        ("PHAVG" if k[1] == "PHAVG" else int(k[1][1:])), bps).loc[OOS_START:])["Sharpe"])
            picks["C_ORACLE"] = orc
            for nm, (g, p) in picks.items():
                arm = "PHAVG" if p == "PHAVG" else int(p[1:])
                r = series(pn, g, arm, bps)
                o = legs_window(r.loc[OOS_START:], spy_oos)
                wf.append(dict(panel=pn, bps=bps, chooser=nm, pick_gross=g, pick_phase=p,
                               oos_CAGR=o["CAGR"], oos_Sharpe=o["Sharpe"], oos_MaxDD=o["MaxDD"],
                               oos_4b=pass4b(o), cagr_margin_oos=o["cagr_margin"], dd_margin_oos=o["dd_margin"],
                               spy_oos_CAGR=o["spyCAGR"], spy_oos_Sharpe=o["spySharpe"], spy_oos_MaxDD=o["spyMaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  4b-OOS reach by chooser (of 8 panel x cost cells each):")
    say(W.groupby("chooser").agg(n_4b_oos=("oos_4b", "sum"), med_oos_Sharpe=("oos_Sharpe", "median"),
                                 med_oos_CAGR=("oos_CAGR", "median"), med_oos_MaxDD=("oos_MaxDD", "median")).to_string())

    # ---- phase persistence IS -> OOS
    say("\n  IS -> OOS phase persistence (does the phase that won 2009-2016 win 2017-2026?):")
    pers = []
    for pn in panels:
        for g, bps in itertools.product(GROSS, COSTS):
            iss = [metrics(series(pn, g, p, bps).loc[:IS_END])["Sharpe"] for p in PHASES]
            oos = [metrics(series(pn, g, p, bps).loc[OOS_START:])["Sharpe"] for p in PHASES]
            rho = float(pd.Series(iss).rank().corr(pd.Series(oos).rank()))  # spearman = pearson on ranks (no scipy in sandbox)
            pers.append(dict(panel=pn, gross=g, bps=bps, rho=rho,
                             is_argmax=f"W{int(np.argmax(iss))}", oos_argmax=f"W{int(np.argmax(oos))}",
                             hit=int(np.argmax(iss)) == int(np.argmax(oos))))
    P = pd.DataFrame(pers)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"    median spearman(IS phase Sharpe, OOS phase Sharpe) = {P.rho.median():.4f} over {len(P)} families; "
        f"IS argmax == OOS argmax at {int(P.hit.sum())} of {len(P)} (uniform would be {len(P)/5:.1f})")

    gates.append(("G8 phase persistence families priced", len(P), len(P) == len(panels)*len(GROSS)*len(COSTS)))
    pd.DataFrame([dict(gate=g, value=v, ok=bool(o)) for g, v, o in gates]).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    say("\nGATES: " + ", ".join(f"{g.split()[0]}={'PASS' if o else 'FAIL'}" for g, v, o in gates))
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")

if __name__ == "__main__":
    main()
