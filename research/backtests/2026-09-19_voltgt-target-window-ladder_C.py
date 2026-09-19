#!/usr/bin/env python3
"""idea 1678 (lane C, 2026-09-19) — DOES THE VOLTGT 4b CANDIDATE SURVIVE A RULE-8 LADDER OF
ITS OWN TWO INHERITED DIALS?

Idea 1656 (lane cloud, this day) published an INCIDENTAL, CONDITIONAL KEEP-4b candidate: equal
weight every priced name, scale the sleeve to a 15% trailing-20d realised vol, cap at gross 1.00,
weekly, 10 bps.  It clears 4b FULL and OOS on U56 and B136 at every cost rung and is picked from
IS rows alone by C_SHARPE and C_CALMAR.  But its **vol target 0.15 and its 20-day window were
INHERITED from the record and never laddered** — so of the candidate's three dials only gross had
ever been walk-forwarded, and the memo filed the gap as this idea.

THIS RUN LADDERS THE TWO INHERITED DIALS AND NOTHING ELSE.
  target  T in {0.10, 0.125, 0.15, 0.20, 0.25}      (5 rungs)
  window  W in {10, 20, 40, 60} trading days        (4 rungs)
  gross   PINNED at 1.00 (idea 1656's certified rung; not a dial here)
  -> 20 cells per panel x 3 panels x 4 cost rungs = 240 published rows.  MAX 2 TUNED PARAMS.

Every cell is also priced against its OWN realised-gross-matched constant-gross EW twin, so the
report can say whether the vol-target DIAL buys anything a plain de-gross does not — the question
every 2026-09-19 lane has had to answer.

PROTOCOL: costs 10 bps is the live rung (0/25/50 also published); weights decided at t applied at
t+1 (engine); both KEEP paths at every cell; rule 8 with choosers fitted on rows <= 2016-12-31
ONLY and 2017-2026 read once.  Survivorship (rule 9): U56/B136/SMALL are current-constituent
lists, so absolute levels are UPPER BOUNDS; the cell-vs-twin contrast is first-order immune.

Deterministic, offline, no network.  Writes .grid.csv .twin.csv .walkforward.csv .gates.csv .log.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                      # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                      # noqa: E402

OUT = Path(__file__).with_suffix("")
TARGETS = [0.10, 0.125, 0.15, 0.20, 0.25]
WINDOWS = [10, 20, 40, 60]
GROSS = 1.00                 # pinned: idea 1656's certified rung
COSTS = [0, 10, 25, 50]
IS_END = "2016-12-31"
INHERITED = (0.15, 20)       # the dials 1656 inherited; the incumbent cell
LOG, GATES = [], []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def gate(name, val, ok, note=""):
    GATES.append(dict(gate=name, value=str(val), pass_=bool(ok), note=note))
    say(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")


# ---------------------------------------------------------------- books
def ew_weights(px, g, trad):
    e = px[trad].notna().astype(float)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def voltgt_weights(px, trad, target, window, g=GROSS):
    """idea 1656's construction, with the target and the window made EXPLICIT dials.
    Equal-weight every priced name, scale so the sleeve's trailing `window`-day realised vol
    hits `target`, cap the scale at 1.0 (no leverage) and at gross g.  Uses only info <= t."""
    base = ew_weights(px, 1.0, trad)
    sleeve = (base.shift(1) * px[trad].pct_change().reindex(columns=base.columns).fillna(0.0)).sum(axis=1)
    rv = sleeve.rolling(window).std() * np.sqrt(252)
    k = (target / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return base.mul(k * g, axis=0)


def run(px, wfn, freq="W"):
    res = backtest(px, wfn(px), cost_bps=0.0, freq=freq)
    return dict(gross=res["returns"], turnover=res["turnover"], rg=res["weights"].sum(axis=1))


def net(r, c):
    """Exact cost axis off the 0 bps run: r_net(c) = r_gross - turnover * c / 1e4 (gated below)."""
    return r["gross"] - r["turnover"] * c / 1e4


def legs(ret, start):
    r = ret.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins = metrics(r.loc[:IS_END])
    oos = metrics(r.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=ins["Sharpe"], IS_CAGR=ins["CAGR"], IS_MaxDD=ins["MaxDD"],
                OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"])


# ---------------------------------------------------------------- panels
PANELS = {}
u = load_universe();                PANELS["U56"] = (u, [c for c in u.columns])
b = load_universe(broad=True);      PANELS["B136"] = (b, [c for c in b.columns])
sm = load_universe(small=True)
meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
PANELS["SMALL"] = (sm, [c for c in sm.columns if c != "SPY" and c not in bad])
say("# idea 1678 — VOLTGT target x window ladder, gross pinned 1.00, weekly, 3 panels")
say(f"  panels: U56 {u.shape[1]} cols, B136 {b.shape[1]} cols, SMALL {sm.shape[1]} cols "
    f"({len(bad)} max_1d_move>=1.0 names dropped -> {len(PANELS['SMALL'][1])} tradable, SPY benchmark-only)")
gate("G1 small-panel screen applied", f"{len(bad)} dropped, {len(PANELS['SMALL'][1])} tradable",
     len(bad) > 0 and "SPY" not in PANELS["SMALL"][1], "data/small_meta.csv max_1d_move >= 1.0")

GRID, TWIN, WF_STORE = [], [], {}
EW_LADDER = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]

for pname, (px, trad) in PANELS.items():
    START = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0)
    spy_f = metrics(spy.loc[START:]); _h = len(spy.loc[START:]) // 2
    spy_h1 = metrics(spy.loc[START:].iloc[:_h]); spy_h2 = metrics(spy.loc[START:].iloc[_h:])
    spy_is = metrics(spy.loc[START:IS_END])
    spy_o = metrics(spy.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    base_r = run(px, rules_v2_weights)
    say(f"\n## PANEL {pname}  {START.date()} -> {px.index[-1].date()}  "
        f"({(px.index[-1]-START).days/365.25:.2f} y)")
    say(f"   SPY   FULL {spy_f['CAGR']:.2%} / {spy_f['Sharpe']:.4f} / {spy_f['MaxDD']:.2%}   halves "
        f"{spy_h1['Sharpe']:.4f} / {spy_h2['Sharpe']:.4f}   OOS {spy_o['CAGR']:.2%} / "
        f"{spy_o['Sharpe']:.4f} / {spy_o['MaxDD']:.2%}")
    LB = legs(net(base_r, 10), START)
    say(f"   RULES v2 (live) @10bps FULL {LB['CAGR']:.2%} / {LB['Sharpe']:.4f} / {LB['MaxDD']:.2%}   halves "
        f"{LB['H1']:.4f} / {LB['H2']:.4f}   OOS {LB['OOS_CAGR']:.2%} / {LB['OOS_Sharpe']:.4f} / {LB['OOS_MaxDD']:.2%}")
    say(f"   4b FULL bars: DD cap {0.6*spy_f['MaxDD']:.2%}, CAGR floor {0.7*spy_f['CAGR']:.2%};  "
        f"4b OOS bars: DD cap {0.6*spy_o['MaxDD']:.2%}, CAGR floor {0.7*spy_o['CAGR']:.2%}")

    def keep4a(d, c):
        L = legs(net(base_r, c), START)
        return bool(d["H1"] > L["H1"] and d["H2"] > L["H2"] and d["MaxDD"] >= L["MaxDD"])

    def keep4b(d, oos=False):
        if oos:
            return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                        and d["OOS_Sharpe"] > spy_o["Sharpe"]
                        and d["OOS_MaxDD"] >= 0.6 * spy_o["MaxDD"] and d["OOS_CAGR"] >= 0.7 * spy_o["CAGR"])
        return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                    and d["MaxDD"] >= 0.6 * spy_f["MaxDD"] and d["CAGR"] >= 0.7 * spy_f["CAGR"])

    # ---- constant-gross EW curve, for the realised-gross-matched twin of every cell
    ew_runs = {g: run(px, lambda p, g=g: ew_weights(p, g, trad)) for g in EW_LADDER}
    curve = [float(ew_runs[g]["rg"].loc[START:].mean()) for g in EW_LADDER]
    gate(f"G2 {pname} EW realised-gross curve monotone", f"{np.all(np.diff(curve) > 0)}",
         bool(np.all(np.diff(curve) > 0)), "twin gross inverted by interpolation on this curve")

    arms, cells = {}, {}
    for T in TARGETS:
        for W in WINDOWS:
            r = run(px, lambda p, T=T, W=W: voltgt_weights(p, trad, T, W))
            arms[(T, W)] = r
            R = float(r["rg"].loc[START:].mean())
            g_tw = float(np.interp(R, curve, EW_LADDER))
            tw = run(px, lambda p, g=g_tw: ew_weights(p, g, trad))
            arms[("TWIN", T, W)] = tw
            cells[(T, W)] = (R, g_tw, float(tw["rg"].loc[START:].mean()))

    for (T, W), (R, g_tw, R_tw) in cells.items():
        for c in COSTS:
            d = legs(net(arms[(T, W)], c), START)
            t = legs(net(arms[("TWIN", T, W)], c), START)
            GRID.append(dict(panel=pname, target=T, window=W, gross=GROSS, cost_bps=c,
                             CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"], H1=d["H1"], H2=d["H2"],
                             OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"], OOS_MaxDD=d["OOS_MaxDD"],
                             IS_Sharpe=d["IS_Sharpe"], IS_CAGR=d["IS_CAGR"], IS_MaxDD=d["IS_MaxDD"],
                             realised_gross=R, turnover_yr=float(arms[(T, W)]["turnover"].loc[START:].sum()
                                                                 / ((px.index[-1] - START).days / 365.25)),
                             keep4a=keep4a(d, c), keep4b_full=keep4b(d), keep4b_oos=keep4b(d, oos=True)))
            TWIN.append(dict(panel=pname, target=T, window=W, cost_bps=c, twin_gross=g_tw,
                             cell_realised_gross=R, twin_realised_gross=R_tw,
                             dSharpe=d["Sharpe"] - t["Sharpe"], dSharpe_OOS=d["OOS_Sharpe"] - t["OOS_Sharpe"],
                             dCAGR_pp=(d["CAGR"] - t["CAGR"]) * 100, dMaxDD_pp=(d["MaxDD"] - t["MaxDD"]) * 100,
                             twin_keep4b_full=keep4b(t), twin_keep4b_oos=keep4b(t, oos=True)))

    WF_STORE[pname] = dict(px=px, START=START, arms=arms, keep4a=keep4a, keep4b=keep4b,
                           spy_is=spy_is, spy_o=spy_o, base_r=base_r)

    sub = pd.DataFrame([g for g in GRID if g["panel"] == pname and g["cost_bps"] == 10])
    say(f"\n   --- all 20 cells @10bps, gross {GROSS:.2f} (FULL / OOS) ---")
    say(sub[["target", "window", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
             "OOS_MaxDD", "realised_gross", "turnover_yr", "keep4a", "keep4b_full", "keep4b_oos"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

grid = pd.DataFrame(GRID); grid.to_csv(f"{OUT}.grid.csv", index=False)
twin = pd.DataFrame(TWIN); twin.to_csv(f"{OUT}.twin.csv", index=False)
say(f"\n{len(grid)} published grid rows -> {Path(OUT).name}.grid.csv ; {len(twin)} twin rows -> .twin.csv")

# ---------------------------------------------------------------- gates
u_arms = WF_STORE["U56"]["arms"]; u_start = WF_STORE["U56"]["START"]
inc = legs(net(u_arms[INHERITED], 10), u_start)
say(f"\n# INCUMBENT CELL (U56, target 0.15, window 20, gross 1.00, 10 bps): "
    f"FULL {inc['CAGR']:.2%} / {inc['Sharpe']:.4f} / {inc['MaxDD']:.2%}  halves {inc['H1']:.4f}/{inc['H2']:.4f}  "
    f"OOS {inc['OOS_CAGR']:.2%} / {inc['OOS_Sharpe']:.4f} / {inc['OOS_MaxDD']:.2%}")
dev = max(abs(inc["CAGR"] - 0.1527), abs(inc["Sharpe"] - 1.2075), abs(inc["MaxDD"] + 0.1929))
gate("G3 incumbent reproduces idea 1656", f"max |dev| {dev:.2e}", dev < 5e-4,
     "1656 published U56 @10bps FULL 15.27% / 1.2075 / -19.29%")

chk_w = voltgt_weights(PANELS["U56"][0], PANELS["U56"][1], *INHERITED)
exact = backtest(PANELS["U56"][0], chk_w, cost_bps=25.0, freq="W")["returns"]
d_cost = float((exact - net(u_arms[INHERITED], 25)).abs().max())
gate("G4 cost axis exact off the 0 bps run", f"{d_cost:.3e}", d_cost < 1e-12,
     "r_net(c) = r_gross - turnover*c/1e4 vs engine.backtest(cost_bps=25)")

maxg = max(float(WF_STORE[p]["arms"][(T, W)]["rg"].loc[WF_STORE[p]["START"]:].max())
           for p in PANELS for T in TARGETS for W in WINDOWS)
gate("G5 no leverage anywhere", f"max realised gross {maxg:.6f}", maxg <= 1.0 + 1e-9, "scale capped at 1.0")

mg = twin.groupby(["panel", "target", "window"])[["cell_realised_gross", "twin_realised_gross"]].first()
gate("G6 twin realised-gross match", f"max |dev| {float((mg.cell_realised_gross-mg.twin_realised_gross).abs().max()):.3e}",
     float((mg.cell_realised_gross - mg.twin_realised_gross).abs().max()) < 5e-3,
     "interpolated constant-gross EW twin, 60 pairs")

# ---------------------------------------------------------------- rule 8
say("\n## RULE 8 WALK-FORWARD — choosers fitted on rows <= 2016-12-31 ONLY; 2017-2026 read once")
WF = []
CELLS = [(T, W) for T in TARGETS for W in WINDOWS]
for pname, S in WF_STORE.items():
    START, spy_is, spy_o = S["START"], S["spy_is"], S["spy_o"]
    for c in COSTS:
        isd = {k: legs(net(S["arms"][k], c), START) for k in CELLS}

        def memo(default):
            """the record's own pre-stated 2026-09-03 rule, read on IS rows only: among cells
            clearing the 4b bars IN-SAMPLE, take the lowest target then the shortest window."""
            ok = [k for k in CELLS if isd[k]["IS_MaxDD"] >= 0.6 * spy_is["MaxDD"]
                  and isd[k]["IS_CAGR"] >= 0.7 * spy_is["CAGR"]]
            return min(ok) if ok else default

        choosers = {
            "C_SHARPE": max(CELLS, key=lambda k: isd[k]["IS_Sharpe"]),
            "C_CAGR": max(CELLS, key=lambda k: isd[k]["IS_CAGR"]),
            "C_CALMAR": max(CELLS, key=lambda k: isd[k]["IS_CAGR"] / abs(isd[k]["IS_MaxDD"])),
            "C_MEMO": memo(INHERITED),
            "C_INHERITED (incumbent, NOT a chooser)": INHERITED,
        }
        for nm, k in choosers.items():
            d = legs(net(S["arms"][k], c), START)
            t = legs(net(S["arms"][("TWIN",) + k], c), START)
            WF.append(dict(panel=pname, cost_bps=c, chooser=nm, pick_target=k[0], pick_window=k[1],
                           picks_inherited=(k == INHERITED),
                           OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"], OOS_MaxDD=d["OOS_MaxDD"],
                           keep4b_oos=S["keep4b"](d, oos=True), keep4b_full=S["keep4b"](d),
                           keep4a=S["keep4a"](d, c), dSharpe_OOS_vs_twin=d["OOS_Sharpe"] - t["OOS_Sharpe"]))
wf = pd.DataFrame(WF); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# ---------------------------------------------------------------- headlines
say("\n# HEADLINES")
for pname in PANELS:
    g10 = grid[(grid.panel == pname) & (grid.cost_bps == 10)]
    say(f"  {pname} @10bps: 4a {int(g10.keep4a.sum())}/20, 4b FULL {int(g10.keep4b_full.sum())}/20, "
        f"4b OOS {int(g10.keep4b_oos.sum())}/20")
say(f"  ALL {len(grid)} rows: 4a {int(grid.keep4a.sum())}, 4b FULL {int(grid.keep4b_full.sum())}, "
    f"4b OOS {int(grid.keep4b_oos.sum())}, 4b FULL&OOS {int((grid.keep4b_full & grid.keep4b_oos).sum())}")
real = wf[~wf.chooser.str.startswith("C_INHERITED")]
say(f"  IS-only choosers: {int(real.picks_inherited.sum())} of {len(real)} pick the INHERITED "
    f"(0.15, 20) cell; 4b OOS cleared by {int(real.keep4b_oos.sum())} of {len(real)}")
say("  chooser picks by panel/cost:")
say(real.pivot_table(index=["panel", "cost_bps"], columns="chooser",
                     values="pick_target", aggfunc="first").to_string())
say(real.pivot_table(index=["panel", "cost_bps"], columns="chooser",
                     values="pick_window", aggfunc="first").to_string())
t10 = twin[twin.cost_bps == 10]
say(f"  vs own realised-gross-matched twin @10bps: dSharpe > 0 in {int((t10.dSharpe > 0).sum())} of {len(t10)} "
    f"(mean {t10.dSharpe.mean():+.4f}); OOS {int((t10.dSharpe_OOS > 0).sum())} of {len(t10)} "
    f"(mean {t10.dSharpe_OOS.mean():+.4f}); dMaxDD mean {t10.dMaxDD_pp.mean():+.2f} pp; "
    f"twin 4b FULL&OOS {int((t10.twin_keep4b_full & t10.twin_keep4b_oos).sum())} of {len(t10)}")

pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
say(f"\nGATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
print(f"log -> {Path(OUT).name}.log.txt")
