#!/usr/bin/env python3
"""Idea 1694 (lane cloud, 2026-09-19) — is the KEEP-4b pass a REBALANCE-CALENDAR-PHASE artefact?

Every book in this record rebalances on the LAST trading day of the period, because that is
what `engine.rebalance_mask` does.  Nobody chose that anchor and no run has priced it.  Idea
1590 found that ONE trading day of execution LATENCY (trade at t+2 instead of t+1) kills the
standing 4b pass, which says the book's margins are thin in the calendar.  The neighbouring
question is different and unasked: hold the latency fixed at t+1 and move the day you LOOK.

DIALS (two, and no more):
  1. CADENCE  in {W, M}
  2. PHASE    W: the weekday anchor, Mon..Fri -- rebalance on the LAST trading day of the week
                 whose weekday <= p.  p = FRI is exactly `engine.rebalance_mask(idx, 'W')`.
              M: the k-th trading day of the month, k in {1, 5, 10, 15, 20, L}.  k = L is
                 exactly `engine.rebalance_mask(idx, 'M')`.

NOT dials, published at every cell: PANEL {U56, B136, SMALL} and GROSS {0.75, 1.00}.  Both
gross values are PRE-REGISTERED FROM THE COMMITTED RECORD, not chosen here: 0.75 is live RULES
v2, and 1.00 is the only gross at which the band book clears 4b FULL-and-OOS in the record
(ideas 1498 / 1649).  Neither is tuned by this run's results.

Book at every cell: live RULES v2 band 0.03, equal weight gross/N over in-band priced names,
gated-out weight to 0%-yielding cash, t+1 execution, 10 bps (PROTOCOL rules 1-2).  The only
thing that moves across cells is WHICH DAY the weights are recomputed and traded on.

Outputs: .console.txt, .grid.csv, .keeppaths.csv, .walkforward.csv
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights          # noqa
from engine import backtest, rebalance_mask, metrics          # noqa

STAMP, SLUG = "2026-09-19", "rebalance-calendar-phase_cloud"
OUT = ROOT / "research" / "backtests"
COST, BAND, WARM = 10, 0.03, 260
GROSSES = [0.75, 1.00]
WPHASES = [("MON", 0), ("TUE", 1), ("WED", 2), ("THU", 3), ("FRI", 4)]
MPHASES = [("D1", 1), ("D5", 5), ("D10", 10), ("D15", 15), ("D20", 20), ("L", None)]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_log = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); _log.append(s)

# ----------------------------------------------------------------- phase masks
def phase_mask(idx, cadence, p):
    """True on the chosen rebalance day of each period. Same shape/semantics as
    engine.rebalance_mask, with the anchor moved off the period's last trading day."""
    if cadence == "W":
        key = idx.to_period("W")
        ok = pd.Series(idx.weekday <= p, index=idx)
        s = pd.Series(key, index=idx)
        m = pd.Series(False, index=idx)
        for _, g in ok.groupby(s, sort=False):
            cand = g[g].index
            m.loc[cand[-1] if len(cand) else g.index[0]] = True   # fall back if the week has none
        return m
    key = idx.to_period("M")
    s = pd.Series(key, index=idx)
    m = pd.Series(False, index=idx)
    for _, g in s.groupby(s, sort=False):
        days = g.index
        m.loc[days[-1] if p is None else days[min(p, len(days)) - 1]] = True
    return m

def bt(prices, weights, mask, cost_bps=COST):
    """engine.backtest verbatim, with the schedule supplied instead of derived from freq."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mk = mask.reindex(prices.index).fillna(False).shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns)); turnover = pd.Series(0.0, index=prices.index)
    for i, d in enumerate(prices.index):
        if mk.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum(); cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "turnover": turnover}

# ----------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"SMALL: dropped {px.shape[1]-len(keep)} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv); {len(keep)-1} names remain + SPY. SURVIVORSHIP: current "
        f"constituents of a sub-$2B screen carried back to 2010 (rule 9).")
    return px[keep]

PANELS = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
for k, v in PANELS.items():
    say(f"panel {k}: {v.shape[1]-1} names + SPY, {v.index[0].date()}..{v.index[-1].date()}, {len(v)} rows")

# ----------------------------------------------------------------- gates FIRST
say("\n=== GATES (run before any new number is read) ===")
u = PANELS["U56"]; wts = rules_v2_weights(u, band=BAND, gross=0.75)
g1 = bool((phase_mask(u.index, "W", 4) == rebalance_mask(u.index, "W")).all())
g2 = bool((phase_mask(u.index, "M", None) == rebalance_mask(u.index, "M")).all())
ref = backtest(u, wts, cost_bps=COST, freq="W")["returns"]
mine = bt(u, wts, phase_mask(u.index, "W", 4))["returns"]
g3 = float((ref - mine).abs().max())
refm = backtest(u, wts, cost_bps=COST, freq="M")["returns"]
minem = bt(u, wts, phase_mask(u.index, "M", None))["returns"]
g4 = float((refm - minem).abs().max())
say(f"  G1 phase_mask(W, FRI) == engine.rebalance_mask(idx,'W'): {g1}")
say(f"  G2 phase_mask(M, L)   == engine.rebalance_mask(idx,'M'): {g2}")
say(f"  G3 local bt() replays engine.backtest at freq='W' bit-for-bit: max|d| {g3:.3e}")
say(f"  G4 local bt() replays engine.backtest at freq='M' bit-for-bit: max|d| {g4:.3e}")
cnt = {f"W/{n}": int(phase_mask(u.index, "W", p).sum()) for n, p in WPHASES}
cnt.update({f"M/{n}": int(phase_mask(u.index, "M", p).sum()) for n, p in MPHASES})
say(f"  G5 rebalance-day counts on U56's calendar (must be ~equal within a cadence): {cnt}")
assert g1 and g2 and g3 < 1e-15 and g4 < 1e-15, "gate failure"

# ----------------------------------------------------------------- grid
def legs(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:]); i = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"], IS_MaxDD=i["MaxDD"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])

rows, series = [], {}
for pan, px in PANELS.items():
    spy = px["SPY"].pct_change().fillna(0.0)
    live_full = bt(px, rules_v2_weights(px, band=BAND, gross=0.75),
                   phase_mask(px.index, "W", 4))["returns"]
    for G in GROSSES:
        w = rules_v2_weights(px, band=BAND, gross=G)
        for cad, phases in (("W", WPHASES), ("M", MPHASES)):
            for pname, p in phases:
                res = bt(px, w, phase_mask(px.index, cad, p))
                r = res["returns"].iloc[WARM:]
                series[(pan, G, cad, pname)] = r
                L = legs(r); Ls = legs(spy.loc[r.index]); Ll = legs(live_full.loc[r.index])
                p4a = (L["H1"] > Ll["H1"]) and (L["H2"] > Ll["H2"]) and (L["MaxDD"] >= Ll["MaxDD"])
                p4b_f = (L["H1"] > Ls["H1"]) and (L["H2"] > Ls["H2"]) and \
                        (L["MaxDD"] >= 0.60 * Ls["MaxDD"]) and (L["CAGR"] >= 0.70 * Ls["CAGR"])
                p4b_o = (L["OOS_Sharpe"] > Ls["OOS_Sharpe"]) and \
                        (L["OOS_MaxDD"] >= 0.60 * Ls["OOS_MaxDD"]) and \
                        (L["OOS_CAGR"] >= 0.70 * Ls["OOS_CAGR"])
                rows.append(dict(panel=pan, G=G, cadence=cad, phase=pname, **L,
                                 turn_yr=res["turnover"].iloc[WARM:].sum() / (len(r) / 252),
                                 pass4a=p4a, pass4b_FULL=p4b_f, pass4b_OOS=p4b_o,
                                 spy_Sharpe=Ls["Sharpe"], spy_CAGR=Ls["CAGR"], spy_MaxDD=Ls["MaxDD"],
                                 spy_OOS_Sharpe=Ls["OOS_Sharpe"], spy_OOS_CAGR=Ls["OOS_CAGR"],
                                 spy_OOS_MaxDD=Ls["OOS_MaxDD"],
                                 base_Sharpe=Ll["Sharpe"], base_MaxDD=Ll["MaxDD"],
                                 base_OOS_Sharpe=Ll["OOS_Sharpe"]))
    say(f"  {pan}: {len(GROSSES)*(len(WPHASES)+len(MPHASES))} cells done")
grid = pd.DataFrame(rows)
grid.to_csv(OUT / f"{STAMP}_{SLUG}.grid.csv", index=False)
grid.to_csv(OUT / f"{STAMP}_{SLUG}.keeppaths.csv", index=False)

say(f"\n=== EVERY CELL ({len(grid)} of them, all published) ===")
cols = ["panel","G","cadence","phase","CAGR","Sharpe","MaxDD","H1","H2","OOS_CAGR","OOS_Sharpe",
        "OOS_MaxDD","turn_yr","pass4a","pass4b_FULL","pass4b_OOS"]
say(grid[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

say("\n=== BENCHMARKS on each panel's own calendar ===")
for pan in PANELS:
    g = grid[grid.panel == pan].iloc[0]
    say(f"  {pan:6s} SPY FULL {g.spy_CAGR:.2%} / {g.spy_Sharpe:.4f} / {g.spy_MaxDD:.2%} | "
        f"SPY OOS {g.spy_OOS_CAGR:.2%} / {g.spy_OOS_Sharpe:.4f} / {g.spy_OOS_MaxDD:.2%} | "
        f"live RULES v2 (W/FRI, G 0.75) FULL {g.base_Sharpe:.4f} / {g.base_MaxDD:.2%}, "
        f"OOS Sharpe {g.base_OOS_Sharpe:.4f}")

say("\n=== THE QUESTION: how far does one panel-gross-cadence cell move when ONLY the phase moves? ===")
sp = []
for (pan, G, cad), g in grid.groupby(["panel", "G", "cadence"]):
    anch = g[g.phase.isin(["FRI", "L"])].iloc[0]
    sp.append(dict(panel=pan, G=G, cadence=cad, n_phase=len(g),
                   Sharpe_min=g.Sharpe.min(), Sharpe_max=g.Sharpe.max(),
                   Sharpe_spread=g.Sharpe.max() - g.Sharpe.min(), Sharpe_anchor=anch.Sharpe,
                   MaxDD_spread=g.MaxDD.max() - g.MaxDD.min(), MaxDD_anchor=anch.MaxDD,
                   CAGR_spread=g.CAGR.max() - g.CAGR.min(), CAGR_anchor=anch.CAGR,
                   OOS_Sharpe_spread=g.OOS_Sharpe.max() - g.OOS_Sharpe.min(),
                   OOS_Sharpe_anchor=anch.OOS_Sharpe,
                   n4a=int(g.pass4a.sum()), n4b_FULL=int(g.pass4b_FULL.sum()),
                   n4b_OOS=int(g.pass4b_OOS.sum()),
                   n4b_BOTH=int((g.pass4b_FULL & g.pass4b_OOS).sum()),
                   anchor_4b_BOTH=bool(anch.pass4b_FULL and anch.pass4b_OOS)))
spread = pd.DataFrame(sp)
say(spread.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

say("\n  -- verdict UNANIMITY per (panel, gross, cadence) group: does the phase change the ANSWER? --")
flip = spread[(spread.n4b_BOTH > 0) & (spread.n4b_BOTH < spread.n_phase)]
say(f"  groups where 4b FULL-and-OOS is NOT unanimous across phases: {len(flip)} of {len(spread)}")
if len(flip): say(flip[["panel","G","cadence","n_phase","n4b_BOTH","anchor_4b_BOTH"]].to_string(index=False))
flipa = spread[(spread.n4a > 0) & (spread.n4a < spread.n_phase)]
say(f"  groups where 4a is NOT unanimous across phases: {len(flipa)} of {len(spread)}")
say(f"  TOTALS over all {len(grid)} cells: 4a {int(grid.pass4a.sum())}, 4b FULL "
    f"{int(grid.pass4b_FULL.sum())}, 4b OOS {int(grid.pass4b_OOS.sum())}, 4b FULL-and-OOS "
    f"{int((grid.pass4b_FULL & grid.pass4b_OOS).sum())}")

say("\n  -- the 1.10 pp / 0.0089 yardsticks the record already owns --")
say(f"  mean phase spread of Sharpe  {spread.Sharpe_spread.mean():.4f} "
    f"(max {spread.Sharpe_spread.max():.4f}); the standing 4b candidate's own Sharpe edge over its "
    f"matched twin is 0.0089 (idea 1617)")
say(f"  mean phase spread of MaxDD   {100*spread.MaxDD_spread.mean():.2f} pp "
    f"(max {100*spread.MaxDD_spread.max():.2f} pp); the anchor's whole 4b drawdown margin is "
    f"1.10 pp (idea 1511) and the paired DD-contrast SE is 2.93 pp")
say(f"  mean phase spread of CAGR    {100*spread.CAGR_spread.mean():.2f} pp/yr")
say(f"  mean phase spread of OOS Sharpe {spread.OOS_Sharpe_spread.mean():.4f}")

say("\n  -- is the anchor (FRI / L) SPECIAL, or just one draw from the phase set? --")
rk = []
for (pan, G, cad), g in grid.groupby(["panel", "G", "cadence"]):
    g = g.sort_values("Sharpe", ascending=False).reset_index(drop=True)
    i = int(g.index[g.phase.isin(["FRI", "L"])][0])
    rk.append(dict(panel=pan, G=G, cadence=cad, anchor_rank=i + 1, of=len(g)))
rkd = pd.DataFrame(rk)
say(rkd.to_string(index=False))
_exp = (rkd["of"].mean() + 1) / 2
say(f"  anchor's mean rank {rkd.anchor_rank.mean():.2f} of a mean {rkd['of'].mean():.1f} phases "
    f"(uniform expectation {_exp:.2f}); rank 1 or 2 in {int((rkd.anchor_rank<=2).sum())} of "
    f"{len(rkd)} groups. A mean rank BELOW the uniform expectation means the committed "
    f"last-trading-day anchor is not a neutral draw -- it is systematically one of the BETTER "
    f"phases, so every Sharpe the record has published on it is quoted at a favourable point of "
    f"a dial nobody declared.")

# ----------------------------------------------------------------- rule 8
say("\n=== RULE 8: (cadence, phase) chosen on 2010-2016 rows ONLY; 2017-2026 read ONCE ===")
wf = []
for (pan, G), g in grid.groupby(["panel", "G"]):
    spyL = legs(PANELS[pan]["SPY"].pct_change().fillna(0.0).loc[
        series[(pan, G, "W", "FRI")].index])
    anch = g[(g.cadence == "W") & (g.phase == "FRI")].iloc[0]
    for cname, col, asc in [("C_SHARPE", "IS_Sharpe", False), ("C_CAGR", "IS_CAGR", False),
                            ("C_MINDD", "IS_MaxDD", False)]:
        pick = g.sort_values(col, ascending=asc).iloc[0]
        wf.append(dict(panel=pan, G=G, chooser=cname, pick=f"{pick.cadence}/{pick.phase}",
                       IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                       OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                       anchor_OOS_Sharpe=anch.OOS_Sharpe, anchor_OOS_CAGR=anch.OOS_CAGR,
                       anchor_OOS_MaxDD=anch.OOS_MaxDD, d_OOS_Sharpe=pick.OOS_Sharpe - anch.OOS_Sharpe,
                       spy_OOS_Sharpe=spyL["OOS_Sharpe"], pass4b_OOS=bool(pick.pass4b_OOS),
                       pass4a=bool(pick.pass4a), picked_anchor=(pick.cadence == "W" and pick.phase == "FRI")))
wfd = pd.DataFrame(wf)
wfd.to_csv(OUT / f"{STAMP}_{SLUG}.walkforward.csv", index=False)
say(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say(f"\n  IS-only choosers that land back on the committed anchor (W/FRI): "
    f"{int(wfd.picked_anchor.sum())} of {len(wfd)}")
say(f"  mean OOS Sharpe of the picks {wfd.OOS_Sharpe.mean():.4f} vs the anchor's "
    f"{wfd.anchor_OOS_Sharpe.mean():.4f} on the same cells ({wfd.d_OOS_Sharpe.mean():+.4f})")
say(f"  picks clearing 4b OOS {int(wfd.pass4b_OOS.sum())} of {len(wfd)}; 4a "
    f"{int(wfd.pass4a.sum())} of {len(wfd)}")

(OUT / f"{STAMP}_{SLUG}.console.txt").write_text("\n".join(_log) + "\n")
print("\nwrote", OUT / f"{STAMP}_{SLUG}.console.txt")
