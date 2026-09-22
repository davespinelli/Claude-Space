#!/usr/bin/env python3
"""Idea 2296 (lane B, 2026-09-22) — does the 4b DRAWDOWN SLACK buy the 4b CAGR FLOOR
under a DRAWDOWN-BUDGET RE-GROSS?

Idea 2284 found the 4b DD cap binds in 0 of 240 cells while the CAGR floor binds ALONE in
225, and the live band book's MaxDD sits ~9 pp INSIDE a -20.2% budget (60% of SPY's
-33.7%).  The book is carrying risk it is allowed to take and is not taking.  This run
prices a RE-GROSS that spends that slack: the target gross G_t is set each day from the
LIVE book's own trailing realised vol (VOL) or its own peak-to-trough (DD) against a
budget, HARD-CAPPED AT 1.00 so no leverage is ever introduced.

TWO TUNED DIALS AND NO MORE: **budget target B and lookback L**.  Signal kind {VOL, DD},
allocation {SCALE, FILL}, panel {U56, B136} and cost rung {0, 10, 25, 50} bps are
REPORTED at every grid point, never selected on.

THE PRE-REGISTERED FALSIFIER, declared before any number was read: a CONSTANT-GROSS book
at the SAME REALISED MEAN GROSS is a ZERO-PARAMETER competitor.  Raising gross raises CAGR
by itself; the dynamic budget device only earns its two dials if it beats that matched
static control.  Every cell is scored against it, and against the two frozen comparands
(static 0.75 = the live book, static 1.00).

CAUSALITY: G_t is a function of the live book's realised returns up to and including
close t; the engine applies weights at t+1.  No dial is fitted on the outcome window.

Run:  python3 research/backtests/2026-09-22_drawdown-budget-regross_B.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state   # noqa
from engine import backtest, metrics                                                 # noqa

OUT = Path(__file__).with_suffix("")
BAND, GROSS, FREQ = 0.03, 0.75, "W"          # the LIVE book, untouched
CAP = 1.00                                   # hard cap: no leverage at any grid point
COSTS = [0, 10, 25, 50]
LIVE_COST = 10
KINDS = ["VOL", "DD"]
ALLOCS = ["SCALE", "FILL"]
LOOKBACKS = [20, 40, 60, 120, 252]
BUDGETS = {"VOL": [0.06, 0.08, 0.10, 0.12, 0.15],     # annualised vol target
           "DD":  [0.10, 0.15, 0.20, 0.25, 0.30]}     # peak-to-trough budget
STATIC_LADDER = [0.50, 0.60, 0.75, 0.85, 1.00]
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# ------------------------------------------------------------------ books -----
def unit_weights(px, alloc, band=BAND):
    """The allocation at target gross G == 1.0.  Every book in this run is `G_t * unit`.

    SCALE keeps the live de-gross: gated-out weight goes to cash and is never re-spread
    (RULES v2 clause 4), so unit gross == the in-band share of the panel.
    FILL re-spreads across the IN names, so unit gross == 1 whenever anything is IN.
    """
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    inb = e.where(band_state(px, band), 0.0)
    if alloc == "SCALE":
        return inb.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return inb.div(inb.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def gross_path(ref_r, kind, B, L):
    """Target gross G_t in [0, CAP], causal in the LIVE book's own realised path.

    VOL: G = B / trailing-L realised annualised vol      (spend the budget in vol units)
    DD : G = 1 - |peak-to-trough over L| / B             (spend the budget in DD units)
    Before L observations exist the device is OFF and G == the live gross 0.75.
    """
    if kind == "VOL":
        v = ref_r.rolling(L).std() * np.sqrt(252)
        g = (B / v.replace(0.0, np.nan))
    else:
        eq = (1.0 + ref_r).cumprod()
        dd = eq / eq.rolling(L).max() - 1.0
        g = 1.0 - dd.abs() / B
    return g.clip(lower=0.0, upper=CAP).fillna(GROSS)


def held_run(px, w, freq=FREQ):
    """One engine pass.  Held weights and turnover do not depend on cost (engine.backtest
    subtracts cost only at the end), so ONE pass serves every cost rung exactly."""
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return res["returns"], res["turnover"], res["weights"]


def rets_at(gross_r, turn, cost):
    return gross_r - turn * cost / 1e4


# ---------------------------------------------------------------- scoring -----
def legs(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o, i = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Calmar=m["Calmar"],
                H1=m1["Sharpe"], H2=m2["Sharpe"],
                oCAGR=o["CAGR"], oSharpe=o["Sharpe"], oMaxDD=o["MaxDD"],
                iSharpe=i["Sharpe"], iCAGR=i["CAGR"], iCalmar=i["Calmar"])


def path4a(c, b):
    """Sharpe > live RULES v2 in BOTH halves and MaxDD no worse than live."""
    return bool(c["H1"] > b["H1"] and c["H2"] > b["H2"] and c["MaxDD"] >= b["MaxDD"])


def path4b_full(c, s):
    return bool(c["H1"] > s["H1"] and c["H2"] > s["H2"]
                and c["MaxDD"] >= 0.60 * s["MaxDD"] and c["CAGR"] >= 0.70 * s["CAGR"])


def path4b_oos(c, s):
    return bool(c["oSharpe"] > s["oSharpe"] and c["oMaxDD"] >= 0.60 * s["oMaxDD"]
                and c["oCAGR"] >= 0.70 * s["oCAGR"])


def path4b(c, s):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  (MaxDD is negative, so 'no worse than 60%' is '>= 0.60*SPY')."""
    return bool(path4b_full(c, s) and c["oSharpe"] > s["oSharpe"])


def which_4b_legs_fail(c, s):
    f = []
    if not c["H1"] > s["H1"]: f.append("H1")
    if not c["H2"] > s["H2"]: f.append("H2")
    if not c["oSharpe"] > s["oSharpe"]: f.append("oSharpe")
    if not c["MaxDD"] >= 0.60 * s["MaxDD"]: f.append("DD")
    if not c["CAGR"] >= 0.70 * s["CAGR"]: f.append("CAGR")
    return "+".join(f) if f else "-none-"


# ---------------------------------------------------------------- driver ------
def run_panel(name, px, say):
    start = px.index[260]                                  # skip warm-up, as baseline.compare
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    spy = legs(spy_r)

    base_w = rules_v2_weights(px, band=BAND, gross=GROSS)
    b_gross, b_turn, b_held = held_run(px, base_w)
    base_r = {c: rets_at(b_gross, b_turn, c).loc[start:] for c in COSTS}
    base = {c: legs(base_r[c]) for c in COSTS}
    ref_r = base_r[LIVE_COST]                              # the signal's source series

    units = {a: unit_weights(px, a) for a in ALLOCS}
    ug = {a: units[a].loc[start:].sum(axis=1) for a in ALLOCS}   # unit target gross path

    # ---- static ladder (zero-parameter comparands, and the matched-control engine) ----
    static_cache = {}
    def static_cell(alloc, g):
        key = (alloc, round(float(g), 6))
        if key not in static_cache:
            gr, tn, hd = held_run(px, units[alloc] * g)
            static_cache[key] = (gr, tn, hd)
        return static_cache[key]

    rows, mrows = [], []
    for alloc in ALLOCS:
        for g in STATIC_LADDER:
            gr, tn, hd = static_cell(alloc, g)
            for cost in COSTS:
                r = rets_at(gr, tn, cost).loc[start:]
                c = legs(r)
                c.update(panel=name, cost=cost, kind="STATIC", alloc=alloc, B=np.nan, L=0,
                         Gmean=float((units[alloc].loc[start:].sum(axis=1)).mean()) * g,
                         Gmax=float((units[alloc].loc[start:].sum(axis=1)).max()) * g,
                         heldmax=float(hd.loc[start:].sum(axis=1).max()),
                         turnover=float(tn.loc[start:].sum() / (len(r) / 252)),
                         p4a=path4a(c, base[cost]), p4b_full=path4b_full(c, spy),
                         p4b_oos=path4b_oos(c, spy), p4b=path4b(c, spy),
                         fail4b=which_4b_legs_fail(c, spy), label=f"STATIC{g:.2f}")
                rows.append(c)

    # ------------------------------ dynamic grid --------------------------------
    for kind in KINDS:
        for B in BUDGETS[kind]:
            for L in LOOKBACKS:
                G = gross_path(ref_r, kind, B, L).reindex(px.index).ffill().fillna(GROSS)
                for alloc in ALLOCS:
                    w = units[alloc].mul(G, axis=0)
                    gr, tn, hd = held_run(px, w)
                    tgt = w.loc[start:].sum(axis=1)
                    gstar = float(tgt.mean() / ug[alloc].mean())      # matched mean gross
                    sgr, stn, shd = static_cell(alloc, min(gstar, CAP))
                    for cost in COSTS:
                        r = rets_at(gr, tn, cost).loc[start:]
                        sr = rets_at(sgr, stn, cost).loc[start:]
                        c, sc = legs(r), legs(sr)
                        c.update(panel=name, cost=cost, kind=kind, alloc=alloc, B=B, L=L,
                                 Gmean=float(tgt.mean()), Gmax=float(tgt.max()),
                                 heldmax=float(hd.loc[start:].sum(axis=1).max()),
                                 turnover=float(tn.loc[start:].sum() / (len(r) / 252)),
                                 p4a=path4a(c, base[cost]), p4b_full=path4b_full(c, spy),
                                 p4b_oos=path4b_oos(c, spy), p4b=path4b(c, spy),
                                 fail4b=which_4b_legs_fail(c, spy),
                                 label=f"{kind}/B{B}/L{L}")
                        rows.append(c)
                        mrows.append(dict(panel=name, cost=cost, kind=kind, alloc=alloc,
                                          B=B, L=L, gstar=gstar,
                                          Gmean=float(tgt.mean()),
                                          Gmean_static=float(ug[alloc].mean() * min(gstar, CAP)),
                                          dSharpe=c["Sharpe"] - sc["Sharpe"],
                                          dCAGR=c["CAGR"] - sc["CAGR"],
                                          dMaxDD=c["MaxDD"] - sc["MaxDD"],
                                          dCalmar=c["Calmar"] - sc["Calmar"],
                                          doSharpe=c["oSharpe"] - sc["oSharpe"],
                                          doCAGR=c["oCAGR"] - sc["oCAGR"],
                                          dturn=float(tn.loc[start:].sum() / (len(r) / 252))
                                                - float(stn.loc[start:].sum() / (len(r) / 252)),
                                          dyn4b=path4b(c, spy), st4b=path4b(sc, spy),
                                          dyn4a=path4a(c, base[cost]), st4a=path4a(sc, base[cost])))
    df = pd.DataFrame(rows)
    md = pd.DataFrame(mrows)
    extras = dict(spy=spy, base=base, start=start, units=units, ug=ug, ref_r=ref_r,
                  base_r=base_r, static_cell=static_cell, px=px, b_held=b_held)
    return df, md, extras


# ------------------------------------------------------------- rule 8 ---------
def walkforward(name, df, extras, say):
    """Dials (B, L) chosen on IS ONLY (warm-up .. 2016-12-31), 2017-2026 read ONCE."""
    spy, base = extras["spy"], extras["base"]
    out = []
    for kind in KINDS:
        for alloc in ALLOCS:
            for cost in COSTS:
                sub = df[(df.panel == name) & (df.kind == kind) & (df.alloc == alloc)
                         & (df.cost == cost)]
                if sub.empty: continue
                frozen = df[(df.panel == name) & (df.kind == "STATIC") & (df.alloc == alloc)
                            & (df.cost == cost)]
                for chooser, col in [("C_ISSHARPE", "iSharpe"), ("C_ISCALMAR", "iCalmar")]:
                    pick = sub.loc[sub[col].idxmax()]
                    out.append(dict(panel=name, kind=kind, alloc=alloc, cost=cost,
                                    chooser=chooser, B=pick["B"], L=int(pick["L"]),
                                    isStat=pick[col],
                                    oCAGR=pick["oCAGR"], oSharpe=pick["oSharpe"],
                                    oMaxDD=pick["oMaxDD"],
                                    base_oSharpe=base[cost]["oSharpe"],
                                    base_oCAGR=base[cost]["oCAGR"],
                                    base_oMaxDD=base[cost]["oMaxDD"],
                                    spy_oSharpe=spy["oSharpe"], spy_oCAGR=spy["oCAGR"],
                                    spy_oMaxDD=spy["oMaxDD"],
                                    frozen075_oSharpe=float(frozen[frozen.label == "STATIC0.75"]["oSharpe"].iloc[0]),
                                    frozen075_oCAGR=float(frozen[frozen.label == "STATIC0.75"]["oCAGR"].iloc[0]),
                                    frozen100_oSharpe=float(frozen[frozen.label == "STATIC1.00"]["oSharpe"].iloc[0]),
                                    frozen100_oCAGR=float(frozen[frozen.label == "STATIC1.00"]["oCAGR"].iloc[0]),
                                    p4b_oos=bool(pick["p4b_oos"]), p4b=bool(pick["p4b"]),
                                    p4a=bool(pick["p4a"])))
    return pd.DataFrame(out)


def main():
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)
    report = []
    def say(s=""):
        print(s); report.append(str(s))

    say("=" * 118)
    say("IDEA 2296 — DRAWDOWN-BUDGET RE-GROSS ON THE LIVE RULES v2 BAND BOOK (lane B, 2026-09-22)")
    say(f"book band={BAND} freq={FREQ}; TUNED DIALS = (budget target B, lookback L) ONLY; "
        f"cap {CAP:.2f} (no leverage)")
    say(f"REPORTED not selected: kind {KINDS}, alloc {ALLOCS}, panel [U56,B136], cost {COSTS} bps")
    say(f"FALSIFIER (pre-registered): matched-MEAN-GROSS constant-gross control, zero parameters")
    say("=" * 118)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    dfs, mds, ex = [], [], {}
    for nm, px in panels.items():
        d, m, e = run_panel(nm, px, say)
        dfs.append(d); mds.append(m); ex[nm] = e
    df = pd.concat(dfs, ignore_index=True); md = pd.concat(mds, ignore_index=True)
    df.to_csv(str(OUT) + ".grid.csv", index=False)
    md.to_csv(str(OUT) + ".matched.csv", index=False)

    # ------------------------------------------------------- gates ------------
    gates = []
    for nm, px in panels.items():
        e = ex[nm]; start = e["start"]
        bit = rules_v2_weights(px, band=BAND, gross=GROSS)
        rep = e["units"]["SCALE"] * GROSS
        gates.append(dict(gate="G1 static0.75/SCALE reproduces baseline.rules_v2 bit-identically",
                          panel=nm, value=float((bit - rep).abs().max().max()), ok=bool((bit - rep).abs().max().max() < 1e-12)))
        sub = df[(df.panel == nm)]
        gates.append(dict(gate="G2 no leverage: max TARGET gross <= 1.00 at every grid point",
                          panel=nm, value=float(sub["Gmax"].max()), ok=bool(sub["Gmax"].max() <= CAP + 1e-9)))
        gates.append(dict(gate="G3 no leverage: max HELD gross <= 1.00 after drift",
                          panel=nm, value=float(sub["heldmax"].max()), ok=bool(sub["heldmax"].max() <= CAP + 1e-9)))
        # G4 causality: recomputing the signal on a truncated tape leaves G_t unchanged for t <= cut
        cut = "2018-06-29"
        g_full = gross_path(e["ref_r"], "DD", 0.20, 60).loc[:cut]
        g_trunc = gross_path(e["ref_r"].loc[:cut], "DD", 0.20, 60)
        gates.append(dict(gate="G4 causality: DD signal on truncated tape identical up to cut",
                          panel=nm, value=float((g_full - g_trunc).abs().max()), ok=bool((g_full - g_trunc).abs().max() < 1e-12)))
        g_full = gross_path(e["ref_r"], "VOL", 0.10, 60).loc[:cut]
        g_trunc = gross_path(e["ref_r"].loc[:cut], "VOL", 0.10, 60)
        gates.append(dict(gate="G5 causality: VOL signal on truncated tape identical up to cut",
                          panel=nm, value=float((g_full - g_trunc).abs().max()), ok=bool((g_full - g_trunc).abs().max() < 1e-12)))
        # G6 the signal is not a cost artefact: signal from the 0 vs 50 bps reference
        g0 = gross_path(e["base_r"][0], "DD", 0.20, 60); g50 = gross_path(e["base_r"][50], "DD", 0.20, 60)
        gates.append(dict(gate="G6 signal source insensitive to cost rung (corr G(0bps),G(50bps))",
                          panel=nm, value=float(g0.corr(g50)), ok=bool(g0.corr(g50) > 0.99)))
        # G7 matched control really is matched
        mm = md[md.panel == nm]
        gates.append(dict(gate="G7 matched control mean gross within 1e-6 of the dynamic book's",
                          panel=nm, value=float((mm["Gmean"] - mm["Gmean_static"]).abs().max()),
                          ok=bool((mm["Gmean"] - mm["Gmean_static"]).abs().max() < 1e-6)))
    gdf = pd.DataFrame(gates); gdf.to_csv(str(OUT) + ".gates.csv", index=False)
    say(); say("GATES"); say(gdf.to_string(index=False))
    say(f"GATES: {int(gdf.ok.sum())} of {len(gdf)} pass")

    # ------------------------------------------------- per-panel dumps --------
    for nm, px in panels.items():
        e = ex[nm]; spy = e["spy"]; base = e["base"]
        say(); say("=" * 118)
        say(f"--- PANEL {nm} ({px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}); "
            f"eval from {e['start'].date()} ---")
        say(f"SPY: CAGR {spy['CAGR']:.4%} Sharpe {spy['Sharpe']:.4f} MaxDD {spy['MaxDD']:.4%} "
            f"halves {spy['H1']:.4f}/{spy['H2']:.4f} | OOS {spy['oCAGR']:.4%}/{spy['oSharpe']:.4f}/{spy['oMaxDD']:.4%}")
        say(f"4b bars: CAGR floor {0.70*spy['CAGR']:.4%}  DD cap {0.60*spy['MaxDD']:.4%} | "
            f"OOS floor {0.70*spy['oCAGR']:.4%}  cap {0.60*spy['oMaxDD']:.4%}")
        b = base[LIVE_COST]
        say(f"LIVE RULES v2 @10bps: CAGR {b['CAGR']:.4%} Sharpe {b['Sharpe']:.4f} MaxDD {b['MaxDD']:.4%} "
            f"halves {b['H1']:.4f}/{b['H2']:.4f} | OOS {b['oCAGR']:.4%}/{b['oSharpe']:.4f}/{b['oMaxDD']:.4%}")
        say(f"DD SLACK the idea proposes to spend: live MaxDD {b['MaxDD']:.4%} vs 4b budget "
            f"{0.60*spy['MaxDD']:.4%}  =>  {100*(b['MaxDD'] - 0.60*spy['MaxDD']):.2f} pp unused")
        say(); say("ALL GRID POINTS (every cell, every cost rung):")
        show = df[df.panel == nm][["cost", "kind", "alloc", "B", "L", "Gmean", "Gmax",
                                   "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe",
                                   "oMaxDD", "turnover", "p4a", "p4b_full", "p4b_oos", "p4b",
                                   "fail4b"]].copy()
        for c in ["CAGR", "MaxDD", "oCAGR", "oMaxDD"]: show[c] = (show[c] * 100).round(3)
        for c in ["Sharpe", "H1", "H2", "oSharpe", "turnover", "Gmean", "Gmax"]: show[c] = show[c].round(4)
        say(show.to_string(index=False))

    # -------------------------------------------------- headline A -----------
    say(); say("=" * 118)
    say("A) BOTH KEEP PATHS AT EVERY GRID POINT")
    say("=" * 118)
    dyn = df[df.kind != "STATIC"]; st = df[df.kind == "STATIC"]
    say(f"DYNAMIC cells: {len(dyn)} book-rungs ({len(dyn)//len(COSTS)} distinct books). "
        f"4a {int(dyn.p4a.sum())}, 4b_FULL {int(dyn.p4b_full.sum())}, 4b_OOS {int(dyn.p4b_oos.sum())}, "
        f"4b(FULL+OOS Sharpe) {int(dyn.p4b.sum())}, BOTH(4a&4b) {int((dyn.p4a & dyn.p4b).sum())}")
    say(f"STATIC cells:  {len(st)} book-rungs. 4a {int(st.p4a.sum())}, 4b_FULL {int(st.p4b_full.sum())}, "
        f"4b_OOS {int(st.p4b_oos.sum())}, 4b {int(st.p4b.sum())}")
    say()
    say("4b failing-leg census over the DYNAMIC grid (which leg blocks, by cost rung):")
    say(pd.crosstab(dyn.fail4b, dyn.cost).to_string())
    say()
    say("4b failing-leg census over the STATIC ladder:")
    say(pd.crosstab(st.fail4b, st.cost).to_string())
    say()
    for nm in panels:
        for cost in COSTS:
            s = dyn[(dyn.panel == nm) & (dyn.cost == cost)]
            t = st[(st.panel == nm) & (st.cost == cost)]
            say(f"  {nm} @{cost:>2}bps: dynamic 4a {int(s.p4a.sum())}/{len(s)}  4b {int(s.p4b.sum())}/{len(s)}"
                f"   | static 4a {int(t.p4a.sum())}/{len(t)}  4b {int(t.p4b.sum())}/{len(t)}")

    # ------------------------------------------- headline B: the falsifier ----
    say(); say("=" * 118)
    say("B) THE FALSIFIER — DYNAMIC minus MATCHED-MEAN-GROSS STATIC (zero-parameter control)")
    say("=" * 118)
    for nm in panels:
        for cost in COSTS:
            m = md[(md.panel == nm) & (md.cost == cost)]
            say(f"  {nm} @{cost:>2}bps  n={len(m):3d}  dSharpe med {m.dSharpe.median():+.4f} "
                f"[win {int((m.dSharpe>0).sum())}/{len(m)}]  dCAGR med {100*m.dCAGR.median():+.4f}pp "
                f"[win {int((m.dCAGR>0).sum())}/{len(m)}]  dMaxDD med {100*m.dMaxDD.median():+.4f}pp "
                f"[better {int((m.dMaxDD>0).sum())}/{len(m)}]  dOOS-Sharpe med {m.doSharpe.median():+.4f} "
                f"[win {int((m.doSharpe>0).sum())}/{len(m)}]  dturn med {m.dturn.median():+.4f}x/yr")
    say()
    say("  by (kind, alloc) at the LIVE 10 bps rung, both panels pooled:")
    m10 = md[md.cost == LIVE_COST]
    agg = m10.groupby(["kind", "alloc"]).agg(n=("dSharpe", "size"),
                                             dSharpe_med=("dSharpe", "median"),
                                             dSharpe_win=("dSharpe", lambda x: (x > 0).sum()),
                                             dCAGR_med=("dCAGR", "median"),
                                             dMaxDD_med=("dMaxDD", "median"),
                                             doSharpe_med=("doSharpe", "median"),
                                             doSharpe_win=("doSharpe", lambda x: (x > 0).sum()),
                                             dyn4b=("dyn4b", "sum"), st4b=("st4b", "sum"),
                                             dyn4a=("dyn4a", "sum"), st4a=("st4a", "sum"))
    say(agg.round(4).to_string())
    say()
    say(f"  VERDICT COUNTS at 10 bps: cells where the DYNAMIC book passes 4b and its matched "
        f"static does NOT: {int((m10.dyn4b & ~m10.st4b).sum())} of {len(m10)}; "
        f"static passes and dynamic does not: {int((~m10.dyn4b & m10.st4b).sum())}")
    say(f"  same for 4a: dynamic-only {int((m10.dyn4a & ~m10.st4a).sum())}, "
        f"static-only {int((~m10.dyn4a & m10.st4a).sum())}")

    # ------------------------------------------------- headline C: rule 8 -----
    say(); say("=" * 118)
    say("C) RULE 8 WALK-FORWARD — (B, L) chosen on 2009-2016 ONLY, 2017-2026 read ONCE")
    say("=" * 118)
    wfs = [walkforward(nm, df, ex[nm], say) for nm in panels]
    wf = pd.concat(wfs, ignore_index=True); wf.to_csv(str(OUT) + ".walkforward.csv", index=False)
    w = wf.copy()
    for c in ["oCAGR", "oMaxDD", "base_oCAGR", "base_oMaxDD", "spy_oCAGR", "spy_oMaxDD",
              "frozen075_oCAGR", "frozen100_oCAGR"]:
        w[c] = (w[c] * 100).round(3)
    for c in ["oSharpe", "base_oSharpe", "spy_oSharpe", "frozen075_oSharpe", "frozen100_oSharpe",
              "isStat"]:
        w[c] = w[c].round(4)
    say(w.to_string(index=False))
    say()
    say(f"  picks that beat the LIVE book OOS on Sharpe: {int((wf.oSharpe > wf.base_oSharpe).sum())} of {len(wf)}")
    say(f"  picks that beat SPY OOS on Sharpe:           {int((wf.oSharpe > wf.spy_oSharpe).sum())} of {len(wf)}")
    say(f"  picks that beat FROZEN static 0.75 OOS:      {int((wf.oSharpe > wf.frozen075_oSharpe).sum())} of {len(wf)}")
    say(f"  picks that beat FROZEN static 1.00 OOS:      {int((wf.oSharpe > wf.frozen100_oSharpe).sum())} of {len(wf)}")
    say(f"  picks passing 4b OOS: {int(wf.p4b_oos.sum())} of {len(wf)};  full 4b: {int(wf.p4b.sum())};  4a: {int(wf.p4a.sum())}")

    # ------------------------------------------------- headline D: answer -----
    say(); say("=" * 118)
    say("D) DOES THE SLACK BUY THE FLOOR?  (live 10 bps rung)")
    say("=" * 118)
    for nm in panels:
        spy = ex[nm]["spy"]; floor = 0.70 * spy["CAGR"]; cap = 0.60 * spy["MaxDD"]
        s = df[(df.panel == nm) & (df.cost == LIVE_COST)]
        d = s[s.kind != "STATIC"]
        say(f"  {nm}: 4b CAGR floor {floor:.4%}, DD cap {cap:.4%}")
        say(f"    dynamic cells clearing the CAGR floor: {int((d.CAGR >= floor).sum())}/{len(d)}; "
            f"clearing the DD cap: {int((d.MaxDD >= cap).sum())}/{len(d)}; clearing BOTH: "
            f"{int(((d.CAGR >= floor) & (d.MaxDD >= cap)).sum())}/{len(d)}")
        best = d.loc[d.CAGR.idxmax()]
        say(f"    highest-CAGR dynamic cell: {best['kind']}/{best['alloc']}/B{best['B']}/L{int(best['L'])} "
            f"CAGR {best['CAGR']:.4%} Sharpe {best['Sharpe']:.4f} MaxDD {best['MaxDD']:.4%} "
            f"halves {best['H1']:.4f}/{best['H2']:.4f} OOS {best['oCAGR']:.4%}/{best['oSharpe']:.4f}/"
            f"{best['oMaxDD']:.4%} 4b {bool(best['p4b'])} fail:{best['fail4b']}")
        for alloc in ALLOCS:
            for g in STATIC_LADDER:
                t = s[(s.kind == "STATIC") & (s.alloc == alloc) & (s.label == f"STATIC{g:.2f}")].iloc[0]
                say(f"    STATIC {alloc:<5} g={g:.2f} meanG {t['Gmean']:.4f}: CAGR {t['CAGR']:.4%} "
                    f"Sharpe {t['Sharpe']:.4f} MaxDD {t['MaxDD']:.4%} halves {t['H1']:.4f}/{t['H2']:.4f} "
                    f"OOS {t['oCAGR']:.4%}/{t['oSharpe']:.4f}/{t['oMaxDD']:.4%} 4b {bool(t['p4b'])} "
                    f"fail:{t['fail4b']}")

    # 4b passers, if any
    say(); say("=" * 118)
    say("E) EVERY 4b PASS IN THE RUN (FULL + OOS), dynamic and static alike")
    say("=" * 118)
    pas = df[df.p4b]
    if pas.empty:
        say("  NONE.  0 of %d book-rungs clears 4b." % len(df))
    else:
        p = pas[["panel", "cost", "kind", "alloc", "B", "L", "Gmean", "CAGR", "Sharpe", "MaxDD",
                 "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "turnover"]].copy()
        for c in ["CAGR", "MaxDD", "oCAGR", "oMaxDD"]: p[c] = (p[c] * 100).round(3)
        for c in ["Sharpe", "H1", "H2", "oSharpe", "turnover", "Gmean"]: p[c] = p[c].round(4)
        say(p.to_string(index=False))
    pa = df[df.p4a]
    say(); say(f"F) 4a PASSES: {len(pa)} of {len(df)} book-rungs")
    if not pa.empty:
        p = pa[["panel", "cost", "kind", "alloc", "B", "L", "Gmean", "CAGR", "Sharpe", "MaxDD",
                "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]].copy()
        for c in ["CAGR", "MaxDD", "oCAGR", "oMaxDD"]: p[c] = (p[c] * 100).round(3)
        for c in ["Sharpe", "H1", "H2", "oSharpe", "Gmean"]: p[c] = p[c].round(4)
        say(p.to_string(index=False))

    # ------------------------------- headline G: the zero-parameter ladder ----
    say(); say("=" * 118)
    say("G) THE ZERO-PARAMETER COMPARAND UNDER RULE 8 — gross g chosen on 2009-2016 ONLY by the")
    say("   PRE-STATED Sep-3 memo rule ('smallest G whose MaxDD <= 60% of SPY and CAGR >= 70% of")
    say("   SPY'), 2017-2026 read ONCE.  This is the control the dynamic device must beat.")
    say("=" * 118)
    grows = []
    for nm, px in panels.items():
        e = ex[nm]; start = e["start"]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        i_spy, o_spy = metrics(spy_r.loc[:IS_END]), metrics(spy_r.loc[OOS_START:])
        for alloc in ALLOCS:
            for cost in COSTS:
                pick = None
                for g in STATIC_LADDER:
                    gr, tn, _ = e["static_cell"](alloc, g)
                    r = rets_at(gr, tn, cost).loc[start:]
                    im = metrics(r.loc[:IS_END])
                    ok = (im["MaxDD"] >= 0.60 * i_spy["MaxDD"]
                          and im["CAGR"] >= 0.70 * i_spy["CAGR"])
                    if ok and pick is None:
                        pick = (g, im)
                g, im = pick if pick else (GROSS, None)      # memo fallback: 'if none, keep 75%'
                gr, tn, _ = e["static_cell"](alloc, g)
                r = rets_at(gr, tn, cost).loc[start:]
                c = legs(r)
                grows.append(dict(panel=nm, alloc=alloc, cost=cost, g_IS_pick=g,
                                  fallback=pick is None,
                                  is_CAGR=im["CAGR"] if im else float("nan"),
                                  is_floor=0.70 * i_spy["CAGR"], is_cap=0.60 * i_spy["MaxDD"],
                                  oCAGR=c["oCAGR"], oSharpe=c["oSharpe"], oMaxDD=c["oMaxDD"],
                                  spy_oCAGR=o_spy["CAGR"], spy_oSharpe=o_spy["Sharpe"],
                                  spy_oMaxDD=o_spy["MaxDD"],
                                  base_oSharpe=e["base"][cost]["oSharpe"],
                                  CAGR=c["CAGR"], Sharpe=c["Sharpe"], MaxDD=c["MaxDD"],
                                  H1=c["H1"], H2=c["H2"],
                                  p4b_full=path4b_full(c, e["spy"]),
                                  p4b_oos=path4b_oos(c, e["spy"]), p4b=path4b(c, e["spy"]),
                                  p4a=path4a(c, e["base"][cost])))
    gl = pd.DataFrame(grows); gl.to_csv(str(OUT) + ".zeroparam.csv", index=False)
    z = gl.copy()
    for cc in ["is_CAGR", "is_floor", "is_cap", "oCAGR", "oMaxDD", "spy_oCAGR", "spy_oMaxDD",
               "CAGR", "MaxDD"]:
        z[cc] = (z[cc] * 100).round(3)
    for cc in ["oSharpe", "spy_oSharpe", "base_oSharpe", "Sharpe", "H1", "H2"]:
        z[cc] = z[cc].round(4)
    say(z.to_string(index=False))
    say()
    say(f"  IS-only pick passes 4b FULL at {int(gl.p4b_full.sum())} of {len(gl)} (panel x alloc x rung); "
        f"4b OOS at {int(gl.p4b_oos.sum())}; full 4b at {int(gl.p4b.sum())}; 4a at {int(gl.p4a.sum())}")
    say(f"  the dynamic device's rule-8 picks pass full 4b at {int(wf.p4b.sum())} of {len(wf)} "
        f"and beat FROZEN static 1.00 OOS on Sharpe at "
        f"{int((wf.oSharpe > wf.frozen100_oSharpe).sum())} of {len(wf)}")

    Path(str(OUT) + ".console.txt").write_text("\n".join(report) + "\n")
    say(); say(f"written: {OUT.name}.grid.csv .matched.csv .gates.csv .walkforward.csv .zeroparam.csv .console.txt")


if __name__ == "__main__":
    main()
