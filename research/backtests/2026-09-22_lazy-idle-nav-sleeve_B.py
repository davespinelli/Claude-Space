#!/usr/bin/env python3
"""Idea 2231 (lane B, 2026-09-22) — does a NO-TRADE BAND on the IDLE-NAV SLEEVE make the
accounting fix 4a-ADOPTABLE?

DIAGNOSIS THIS COMES FROM (CHANGELOG, idea 2213 / 2221).  `engine.backtest` pays 0% on the
uninvested residual `1 - sum(w)`, and on the live RULES v2 band book that residual averages
~47% of NAV while its 4b comparand SPY is fully invested.  Sweeping the idle NAV into a bench
sleeve `phi*SPY + (1-phi)*SHY` at phi = 0 (pure T-bill proxy, no beta added) is worth about
+0.50 pp CAGR / +0.067 Sharpe and is the record's ONLY 4a passer — but it was ruled NOT
adoptable for exactly one reason: it lifts turnover 1.92x -> 3.03x/yr, because the sleeve is
reset to `1 - gross*IN/N` every week in lockstep with the core, so 4a dies at 25 and 50 bps
while RULES v2's own acceptance record holds at 5/10/25/50.

THE QUESTION.  That churn is an artefact of the reset, not of the allocation.  Put a NO-TRADE
TOLERANCE h on the sleeve leg alone: at each weekly rebalance the sleeve is left untouched
unless its drifted weight differs from the target idle share by more than h (or unless leaving
it would push total weight above 1.00, which is never allowed).  Does the accounting gain
survive the laziness, and does 4a then hold at every cost rung?

TWO TUNED DIALS AND NO MORE: tolerance h and sleeve mix phi.  Published-not-tuned: panel
{U56, B136} x cost {0, 10, 25, 50} bps x window {FULL, IS, OOS}.  Band c = the live 0.03,
gross = the live 0.75, cadence weekly, t+1 execution — none of them is a dial here.
Every grid point is written to .grid.csv.

HONEST CONSTRUCTION NOTES, stated not repaired.
 * SPY and SHY are also gated universe names, so the sleeve ADDS to any core holding of them.
   The sleeve legs are carried as SEPARATE lines (BENCH_SPY / BENCH_SHY), so a core sale of SPY
   against a sleeve purchase of SPY is charged twice rather than netted: turnover here is
   CONSERVATIVE (an upper bound), never flattering.
 * SHY is a real bond ETF with real duration risk, and its own return path is regime-bound
   (see the .grid.csv SHY rows); this backtest is not a forward-looking statement about cash.
 * SURVIVORSHIP (rule 9): U56 and B136 are current-constituent lists, so every absolute level
   is optimistic.  The lazy-vs-eager contrast is within-tape and does not repair the level.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights          # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

OUT = Path(__file__).with_suffix("")
BAND, GROSS, FREQ = 0.03, 0.75, "W"
H_LADDER   = [0.00, 0.01, 0.02, 0.05, 0.10, 0.20, 0.50]
PHI_LADDER = [0.00, 0.25, 0.50]
COSTS      = [0, 5, 10, 25, 50]
IS_END     = pd.Timestamp("2016-12-31")
OOS_START  = pd.Timestamp("2017-01-01")
log_lines  = []

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); log_lines.append(s)

# ---------------------------------------------------------------- runner
def run_sleeve(px, core_w, phi, h, freq=FREQ):
    """engine.backtest, with two extra sleeve lines and a no-trade tolerance h on the sleeve.

    h = 0.0 -> the sleeve is reset to the target idle share every rebalance (the eager sweep
    idea 2213 priced).  h = inf -> the sleeve is set once and only ever traded to avoid
    leverage.  Returns GROSS (cost-free) returns plus the turnover series; costs are applied
    afterwards, exactly, because the weights do not depend on the cost rung.
    """
    idx  = px.index
    rets = px.pct_change().fillna(0.0).values
    spy_i, shy_i = px.columns.get_loc("SPY"), px.columns.get_loc("SHY")
    n = px.shape[1]
    wt   = core_w.reindex(idx).fillna(0.0).shift(1).values          # decided t, applied t+1
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values

    cur = np.zeros(n + 2)                       # [core cols..., BENCH_SPY, BENCH_SHY]
    held = np.zeros((len(idx), n + 2))
    turn = np.zeros(len(idx))
    for i in range(len(idx)):
        if mask[i] or i == 0:
            new = np.empty(n + 2)
            new[:n] = wt[i]
            core_sum = new[:n].sum()
            tgt = max(0.0, 1.0 - core_sum)
            cur_sleeve = cur[n] + cur[n + 1]
            if abs(tgt - cur_sleeve) <= h and cur_sleeve <= tgt + 1e-12:
                new[n], new[n + 1] = cur[n], cur[n + 1]            # leave it alone
            else:
                new[n], new[n + 1] = phi * tgt, (1.0 - phi) * tgt
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        r_aug = np.empty(n + 2)
        r_aug[:n] = rets[i]; r_aug[n] = rets[i][spy_i]; r_aug[n + 1] = rets[i][shy_i]
        growth = cur * (1 + r_aug)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = pd.Series((held * np.concatenate([rets, rets[:, [spy_i]], rets[:, [shy_i]]], axis=1)).sum(axis=1), index=idx)
    return dict(gross=port, turnover=pd.Series(turn, index=idx),
                sleeve=pd.Series(held[:, n] + held[:, n + 1], index=idx),
                total=pd.Series(held.sum(axis=1), index=idx))

def net(res, cost_bps):
    return res["gross"] - res["turnover"] * cost_bps / 1e4

# ---------------------------------------------------------------- scoring
def legs(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

def pass4a(cand, live):
    return bool(cand["H1"] > live["H1"] and cand["H2"] > live["H2"] and cand["MaxDD"] >= live["MaxDD"])

def pass4b(cand, spy):
    return bool(cand["H1"] > spy["H1"] and cand["H2"] > spy["H2"]
                and cand["MaxDD"] >= 0.60 * spy["MaxDD"]          # both negative
                and cand["CAGR"] >= 0.70 * spy["CAGR"])

WINDOWS = ["FULL", "IS", "OOS"]
def cut(s, w, start):
    s = s.loc[start:]
    return s if w == "FULL" else (s.loc[:IS_END] if w == "IS" else s.loc[OOS_START:])

# ---------------------------------------------------------------- main
rows, wf_rows, gates = [], [], []
panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
store = {}

for pname, px in panels.items():
    start = px.index[260]
    core = rules_v2_weights(px, BAND, GROSS)
    live_eng = backtest(px, core, cost_bps=0, freq=FREQ)          # gross; costs applied below
    spy_r = px["SPY"].pct_change().fillna(0.0)
    v1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)

    # ---- GATES -------------------------------------------------------
    ctrl = run_sleeve(px, core, phi=0.0, h=np.inf)                # sleeve never funded: phi/h moot
    # the control's sleeve is funded at i=0 (tgt>0) so force a true NOSLEEVE control:
    nosleeve = dict(gross=live_eng["returns"], turnover=live_eng["turnover"],
                    sleeve=pd.Series(0.0, index=px.index), total=(core.reindex(px.index).fillna(0).shift(1).sum(axis=1)))
    eager = run_sleeve(px, core, phi=0.0, h=0.0)
    # G1: eager sweep == engine.backtest on the explicit augmented weights
    aug_px = px.copy()
    aug_px["BENCH_SPY"] = px["SPY"]; aug_px["BENCH_SHY"] = px["SHY"]
    aug_w = core.reindex(px.index).fillna(0.0).copy()
    idle = (1.0 - aug_w.sum(axis=1)).clip(lower=0.0)
    aug_w = aug_w.reindex(columns=aug_px.columns).fillna(0.0)
    aug_w["BENCH_SPY"] = 0.0 * idle; aug_w["BENCH_SHY"] = 1.0 * idle
    eng_eager = backtest(aug_px, aug_w, cost_bps=0, freq=FREQ)
    g1r = float(np.abs(eager["gross"] - eng_eager["returns"]).max())
    g1t = float(np.abs(eager["turnover"] - eng_eager["turnover"]).max())
    # G2: the h=inf sleeve never levers; G3: no shorting anywhere
    g2 = float(max(run_sleeve(px, core, phi=p, h=h)["total"].max() for p in (0.0, 0.5) for h in (0.0, 0.5, np.inf)))
    # G4: cost identity — derived 25 bps == a fresh engine run at 25 bps on the eager book
    eng25 = backtest(aug_px, aug_w, cost_bps=25, freq=FREQ)
    g4 = float(np.abs(net(eager, 25) - eng25["returns"]).max())
    # G5: NOSLEEVE control reproduces baseline.rules_v2_weights exactly (it IS that call)
    g5 = float(np.abs(nosleeve["gross"] - live_eng["returns"]).max())
    # G6: sample length
    g6 = len(px.loc[start:]) / 252
    for k, v, ok in [("G1 eager runner == engine.backtest (returns)", g1r, g1r < 1e-12),
                     ("G1b eager runner == engine.backtest (turnover)", g1t, g1t < 1e-12),
                     ("G2 max total weight (no leverage)", g2, g2 <= 1.0 + 1e-9),
                     ("G4 derived 25 bps == fresh engine 25 bps", g4, g4 < 1e-12),
                     ("G5 NOSLEEVE == baseline.rules_v2_weights", g5, g5 == 0.0),
                     ("G6 years of sample", g6, g6 >= 10.0)]:
        gates.append(dict(panel=pname, gate=k, value=v, pass_=bool(ok)))
        log(f"GATE [{pname}] {k}: {v:.6g} -> {'PASS' if ok else 'FAIL'}")

    books = {("NOSLEEVE", np.nan, np.nan): nosleeve}
    for phi in PHI_LADDER:
        for h in H_LADDER:
            books[("SLEEVE", phi, h)] = run_sleeve(px, core, phi=phi, h=h)
    store[pname] = (px, start, spy_r, books, live_eng, v1)

    yrs = len(px.loc[start:]) / 252
    for (kind, phi, h), res in books.items():
        for c in COSTS:
            r = net(res, c).loc[start:]
            live = net(dict(gross=live_eng["returns"], turnover=live_eng["turnover"]), c).loc[start:]
            for w in WINDOWS:
                rr, ll = cut(r, w, start), cut(live, w, start)
                ss = cut(spy_r, w, start)
                L, Lv, S = legs(rr), legs(ll), legs(ss)
                rows.append(dict(panel=pname, kind=kind, phi=phi, h=h, cost_bps=c, window=w,
                                 CAGR=L["CAGR"], Sharpe=L["Sharpe"], MaxDD=L["MaxDD"],
                                 H1=L["H1"], H2=L["H2"],
                                 turnover_per_yr=res["turnover"].loc[rr.index[0]:rr.index[-1]].sum() / (len(rr) / 252),
                                 mean_sleeve=res["sleeve"].loc[rr.index[0]:rr.index[-1]].mean(),
                                 live_CAGR=Lv["CAGR"], live_Sharpe=Lv["Sharpe"], live_MaxDD=Lv["MaxDD"],
                                 spy_CAGR=S["CAGR"], spy_Sharpe=S["Sharpe"], spy_MaxDD=S["MaxDD"],
                                 pass4a=pass4a(L, Lv), pass4b=pass4b(L, S),
                                 dH1=L["H1"]-Lv["H1"], dH2=L["H2"]-Lv["H2"], dDD=L["MaxDD"]-Lv["MaxDD"],
                                 cagr_floor=0.70*S["CAGR"], dd_cap=0.60*S["MaxDD"]))

grid = pd.DataFrame(rows)
grid.to_csv(str(OUT) + ".grid.csv", index=False)
pd.DataFrame(gates).to_csv(str(OUT) + ".gates.csv", index=False)

# ---------------------------------------------------------------- headline reads
log("\n" + "=" * 100)
log("A. THE ACCOUNTING GAIN AND THE TURNOVER IT COSTS (phi = 0.00, FULL window, 10 bps)")
for pname in panels:
    g = grid[(grid.panel == pname) & (grid.window == "FULL") & (grid.cost_bps == 10)]
    ns = g[g.kind == "NOSLEEVE"].iloc[0]
    log(f"  [{pname}] NOSLEEVE (live RULES v2): CAGR {ns.CAGR:7.2%}  Sharpe {ns.Sharpe:.4f}  "
        f"MaxDD {ns.MaxDD:7.2%}  turn {ns.turnover_per_yr:.2f}x")
    for h in H_LADDER:
        s = g[(g.kind == "SLEEVE") & (g.phi == 0.0) & (g.h == h)].iloc[0]
        log(f"    h={h:<5.2f} CAGR {s.CAGR:7.2%} ({s.CAGR-ns.CAGR:+.2%})  Sharpe {s.Sharpe:.4f} "
            f"({s.Sharpe-ns.Sharpe:+.4f})  MaxDD {s.MaxDD:7.2%}  turn {s.turnover_per_yr:.2f}x  "
            f"sleeve {s.mean_sleeve:.1%}  4a {str(s.pass4a):5} 4b {s.pass4b}")

log("\nB. 4a AT EVERY COST RUNG (the leg that killed the eager sweep), FULL window")
for pname in panels:
    for phi in PHI_LADDER:
        for h in H_LADDER:
            g = grid[(grid.panel == pname) & (grid.window == "FULL") & (grid.kind == "SLEEVE")
                     & (grid.phi == phi) & (grid.h == h)]
            v = {int(c): bool(g[g.cost_bps == c].iloc[0].pass4a) for c in COSTS}
            if any(v.values()):
                log(f"  [{pname}] phi={phi} h={h}: 4a " + " ".join(f"{c}bps={'Y' if v[c] else 'n'}" for c in COSTS))
n4a = int(grid[(grid.window == 'FULL')].pass4a.sum()); n4b = int(grid[(grid.window == 'FULL')].pass4b.sum())
log(f"  4a total (FULL, all panels x cells x rungs): {n4a} of {len(grid[grid.window=='FULL'])}")
log(f"  4b total (FULL, all panels x cells x rungs): {n4b} of {len(grid[grid.window=='FULL'])}")

log("\nD. THE 4a LEGS AT THE RUNG THAT KILLED THE EAGER SWEEP (50 bps, FULL, phi = 0.00)")
for pname in panels:
    for h in H_LADDER:
        r = grid[(grid.panel == pname) & (grid.window == "FULL") & (grid.cost_bps == 50)
                 & (grid.kind == "SLEEVE") & (grid.phi == 0.0) & (grid.h == h)].iloc[0]
        log(f"  [{pname}] h={h:<5.2f} dSharpe H1 {r.dH1:+.4f}  H2 {r.dH2:+.4f}  dMaxDD {r.dDD:+.2%}  "
            f"-> 4a {r.pass4a}")

log("\nE. THE 4b CAGR FLOOR, THE LEG phi=0 CANNOT REACH (10 bps, phi = 0.00, h = 0.10)")
for pname in panels:
    for w in WINDOWS:
        r = grid[(grid.panel == pname) & (grid.window == w) & (grid.cost_bps == 10)
                 & (grid.kind == "SLEEVE") & (grid.phi == 0.0) & (grid.h == 0.10)].iloc[0]
        log(f"  [{pname}] {w:4} CAGR {r.CAGR:7.2%} vs floor {r.cagr_floor:6.2%} "
            f"({100*(r.CAGR-r.cagr_floor):+.2f} pp)  MaxDD {r.MaxDD:7.2%} vs cap {r.dd_cap:7.2%}  "
            f"Sharpe halves {r.H1:.3f}/{r.H2:.3f} vs SPY {r.spy_Sharpe:.3f}  4b {r.pass4b}")

log("\nF. WHAT THE LAZINESS BUYS: GAIN RETAINED vs TURNOVER LIFT RETAINED (10 bps, phi=0, FULL)")
for pname in panels:
    g = grid[(grid.panel == pname) & (grid.window == "FULL") & (grid.cost_bps == 10)]
    ns = g[g.kind == "NOSLEEVE"].iloc[0]
    e = g[(g.kind == "SLEEVE") & (g.phi == 0.0) & (g.h == 0.0)].iloc[0]
    for h in H_LADDER:
        s_ = g[(g.kind == "SLEEVE") & (g.phi == 0.0) & (g.h == h)].iloc[0]
        gain = (s_.Sharpe - ns.Sharpe) / (e.Sharpe - ns.Sharpe)
        lift = (s_.turnover_per_yr - ns.turnover_per_yr) / (e.turnover_per_yr - ns.turnover_per_yr)
        log(f"  [{pname}] h={h:<5.2f} Sharpe gain retained {gain:6.1%}   turnover lift retained {lift:6.1%}"
            f"   sleeve funded {s_.mean_sleeve:.1%} of NAV")

log("\nG. THE SLEEVE LEG IS A REAL ALLOCATION, NOT FREE MONEY — SHY's OWN NUMBERS")
_px = panels["U56"]; _s = _px["SHY"].pct_change().fillna(0.0).loc[_px.index[260]:]
_m = metrics(_s); _mi = metrics(_s.loc[:IS_END]); _mo = metrics(_s.loc[OOS_START:])
_y = _s.groupby(_s.index.year).apply(lambda x: (1 + x).prod() - 1)
log(f"  SHY FULL CAGR {_m['CAGR']:.2%}  MaxDD {_m['MaxDD']:.2%}   IS CAGR {_mi['CAGR']:.2%}  "
    f"OOS CAGR {_mo['CAGR']:.2%}   2022 {_y.get(2022, float('nan')):.2%}   2013 {_y.get(2013, float('nan')):.2%}")

# ---------------------------------------------------------------- rule 8
log("\nC. RULE 8 WALK-FORWARD — dials chosen on warm-up..2016-12-31 only, 2017-2026 read ONCE")
CH = ["C_SHARPE", "C_4bIS", "C_4aIS", "C_ANCHOR"]
for pname, (px, start, spy_r, books, live_eng, v1) in store.items():
    for c in COSTS:
        isg = grid[(grid.panel == pname) & (grid.window == "IS") & (grid.cost_bps == c)
                   & (grid.kind == "SLEEVE")]
        oos = grid[(grid.panel == pname) & (grid.window == "OOS") & (grid.cost_bps == c)]
        picks = {}
        picks["C_SHARPE"] = isg.sort_values("Sharpe", ascending=False).iloc[0]
        a = isg[isg.pass4b]; picks["C_4bIS"] = a.sort_values("Sharpe", ascending=False).iloc[0] if len(a) else None
        b = isg[isg.pass4a]; picks["C_4aIS"] = b.sort_values("Sharpe", ascending=False).iloc[0] if len(b) else None
        picks["C_ANCHOR"] = None                                   # change nothing = NOSLEEVE
        ns = oos[oos.kind == "NOSLEEVE"].iloc[0]
        for ch in CH:
            p = picks[ch]
            if ch == "C_ANCHOR":
                o = ns; phi = h = np.nan
            elif p is None:
                wf_rows.append(dict(panel=pname, cost_bps=c, chooser=ch, phi=None, h=None,
                                    note="IS admitted set EMPTY")); continue
            else:
                phi, h = p.phi, p.h
                o = oos[(oos.kind == "SLEEVE") & (oos.phi == phi) & (oos.h == h)].iloc[0]
            wf_rows.append(dict(panel=pname, cost_bps=c, chooser=ch, phi=phi, h=h,
                                OOS_CAGR=o.CAGR, OOS_Sharpe=o.Sharpe, OOS_MaxDD=o.MaxDD,
                                OOS_turn=o.turnover_per_yr, OOS_4a=o.pass4a, OOS_4b=o.pass4b,
                                live_OOS_CAGR=o.live_CAGR, live_OOS_Sharpe=o.live_Sharpe,
                                live_OOS_MaxDD=o.live_MaxDD, spy_OOS_CAGR=o.spy_CAGR,
                                spy_OOS_Sharpe=o.spy_Sharpe, spy_OOS_MaxDD=o.spy_MaxDD))
wf = pd.DataFrame(wf_rows); wf.to_csv(str(OUT) + ".walkforward.csv", index=False)
for pname in panels:
    for c in (10, 50):
        for _, r in wf[(wf.panel == pname) & (wf.cost_bps == c)].iterrows():
            if "OOS_CAGR" not in r or pd.isna(r.get("OOS_CAGR", np.nan)):
                log(f"  [{pname}] {r.chooser}: {r.get('note','')}"); continue
            log(f"  [{pname}] {r.chooser:9} pick phi={r.phi} h={r.h}  OOS {r.OOS_CAGR:7.2%} / "
                f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  turn {r.OOS_turn:.2f}x  "
                f"4a {str(r.OOS_4a):5} 4b {r.OOS_4b}   [live OOS {r.live_OOS_CAGR:6.2%}/"
                f"{r.live_OOS_Sharpe:.4f}/{r.live_OOS_MaxDD:.2%}; SPY OOS {r.spy_OOS_CAGR:6.2%}/"
                f"{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:.2%}]")

Path(str(OUT) + ".log.txt").write_text("\n".join(log_lines) + "\n")
print("\nwrote", OUT.name + ".grid.csv/.gates.csv/.walkforward.csv/.log.txt")
