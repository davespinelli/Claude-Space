#!/usr/bin/env python3
"""Idea 2227 (lane C, 2026-09-22) — is the SHY LEG's +0.50 pp ACCOUNTING GAIN a RATE-REGIME
ARTEFACT?

WHERE THIS COMES FROM.  `engine.backtest` pays exactly 0% on the uninvested residual
`1 - sum(w)`, and on the live RULES v2 band book that residual averages ~47% of NAV while its
4b comparand SPY is fully invested.  Idea 2213 swept the idle NAV into SHY at phi = 0 (a pure
T-bill proxy, no beta added) and credited the fix **+0.50 pp CAGR / +0.067 Sharpe**; idea 2231
made it lazy (tolerance h on the sleeve leg) and turned it into the record's only robust 4a
candidate, the rule-8 pick being phi = 0.00 / h = 0.10 on BOTH panels.  But 2213 also states
SHY's own CAGR is **0.81% IS against 1.72% OOS** — the credit is larger in exactly the window
the record reads last, and SHY's whole 2009-2026 path is one ZIRP-dominated realisation that
the future need not repeat in either direction.

THE QUESTION.  Re-price the sweep against a FLAT-RATE counterfactual sleeve: the idle NAV earns
a CONSTANT annual y instead of SHY's realised path, y on a ladder.  How much of the gain
survives a rate path the future need not repeat, and at what y does the fix stop being 4a?

TWO TUNED DIALS AND NO MORE: **FLAT RATE y** and **PANEL**.  Published-not-tuned: sleeve
tolerance h in {0.00, 0.05, 0.10}, cost {0, 5, 10, 25, 50} bps, window {FULL, IS, OOS}.
phi = 0.00 throughout (the accounting fix itself — no beta is added; a beta sleeve is idea
2221's object, not this one), band c = the live 0.03, gross = the live 0.75, weekly cadence,
t+1 execution.  Every grid point is written to .grid.csv.

HONEST CONSTRUCTION NOTES, stated not repaired.
 * The FLAT and TRAIL sleeves are SYNTHETIC lines, not tradeable instruments: no duration, no
   credit, no bid-ask.  They are counterfactual accounting, deliberately.  The only ex-ante
   IMPLEMENTABLE arm in the run is TRAIL (the sleeve earns the trailing 252-day realised SHY
   return, lagged one day, so it is known at the decision close); a rule-8 chooser over y is a
   SENSITIVITY, not a strategy, because nobody chooses next decade's cash rate.  Both facts are
   printed with the numbers, not buried.
 * The SHY arm carries its sleeve as a line SEPARATE from any core holding of SHY, so a core
   sale against a sleeve purchase is charged twice rather than netted (turnover is an upper
   bound).  The FLAT/TRAIL arms cannot double-charge because cash is not a universe member.
   Section H quantifies that asymmetry (core SHY mean weight) instead of assuming it away.
 * SURVIVORSHIP (rule 9): U56 and B136 are current-constituent lists, so every absolute level
   is optimistic.  The rate-path contrast is within-tape and does not repair the level.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights          # noqa
from engine import backtest, metrics, rebalance_mask                            # noqa

OUT = Path(__file__).with_suffix("")
BAND, GROSS, FREQ, PHI = 0.03, 0.75, "W", 0.00
Y_LADDER  = [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.040, 0.050]
H_LADDER  = [0.00, 0.05, 0.10]
COSTS     = [0, 5, 10, 25, 50]
IS_END    = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
WINDOWS   = ["FULL", "IS", "OOS"]
log_lines = []

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); log_lines.append(s)

# ---------------------------------------------------------------- sleeve return paths
def flat_ret(idx, y):
    """Constant daily rate whose 252-day compounding is exactly y per year."""
    return pd.Series((1.0 + y) ** (1.0 / 252.0) - 1.0, index=idx)

def trail_ret(shy, win=252):
    """Trailing `win`-day realised SHY return, annualised then spread flat over the next day
    and LAGGED ONE DAY -> known at the decision close.  Zero before the window exists."""
    ann = (shy / shy.shift(win)) ** (252.0 / win) - 1.0
    ann = ann.shift(1).fillna(0.0).clip(lower=-0.05, upper=0.20)
    return (1.0 + ann) ** (1.0 / 252.0) - 1.0

# ---------------------------------------------------------------- runner
def run_sleeve(px, core_w, sleeve_ret, phi=PHI, h=0.10, freq=FREQ):
    """engine.backtest semantics, plus two sleeve lines (BENCH_SPY, BENCH_CASH) and a no-trade
    tolerance h on the sleeve.  `sleeve_ret` is the daily return of the CASH leg (SHY's realised
    path, a flat rate, or the trailing-rate path).  Returns GROSS (cost-free) returns and
    turnover; costs are applied afterwards, exactly, since weights never depend on the rung."""
    idx  = px.index
    rets = px.pct_change().fillna(0.0).values
    cash = sleeve_ret.reindex(idx).fillna(0.0).values
    spy_i = px.columns.get_loc("SPY")
    n = px.shape[1]
    wt   = core_w.reindex(idx).fillna(0.0).shift(1).values          # decided t, applied t+1
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values

    cur  = np.zeros(n + 2)                       # [core cols..., BENCH_SPY, BENCH_CASH]
    held = np.zeros((len(idx), n + 2))
    turn = np.zeros(len(idx))
    for i in range(len(idx)):
        if mask[i] or i == 0:
            new = np.empty(n + 2)
            new[:n] = wt[i]
            tgt = max(0.0, 1.0 - new[:n].sum())
            cur_sleeve = cur[n] + cur[n + 1]
            if abs(tgt - cur_sleeve) <= h and cur_sleeve <= tgt + 1e-12:
                new[n], new[n + 1] = cur[n], cur[n + 1]             # leave it alone
            else:
                new[n], new[n + 1] = phi * tgt, (1.0 - phi) * tgt
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        r_aug = np.empty(n + 2)
        r_aug[:n] = rets[i]; r_aug[n] = rets[i][spy_i]; r_aug[n + 1] = cash[i]
        growth = cur * (1 + r_aug)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    aug_r = np.concatenate([rets, rets[:, [spy_i]], cash.reshape(-1, 1)], axis=1)
    return dict(gross=pd.Series((held * aug_r).sum(axis=1), index=idx),
                turnover=pd.Series(turn, index=idx),
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
                and cand["MaxDD"] >= 0.60 * spy["MaxDD"]           # both negative
                and cand["CAGR"] >= 0.70 * spy["CAGR"])

def cut(s, w, start):
    s = s.loc[start:]
    return s if w == "FULL" else (s.loc[:IS_END] if w == "IS" else s.loc[OOS_START:])

# ---------------------------------------------------------------- main
rows, wf_rows, gates = [], [], []
panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
store  = {}

for pname, px in panels.items():
    start   = px.index[260]
    core    = rules_v2_weights(px, BAND, GROSS)
    live_eng = backtest(px, core, cost_bps=0, freq=FREQ)           # gross; costs applied below
    spy_r   = px["SPY"].pct_change().fillna(0.0)
    shy_r   = px["SHY"].pct_change().fillna(0.0)
    trail   = trail_ret(px["SHY"])

    nosleeve = dict(gross=live_eng["returns"], turnover=live_eng["turnover"],
                    sleeve=pd.Series(0.0, index=px.index),
                    total=core.reindex(px.index).fillna(0.0).shift(1).sum(axis=1))

    # ---- GATES, printed before any hypothesis is read ----------------
    eager_shy = run_sleeve(px, core, shy_r, h=0.00)
    aug_px = px.copy(); aug_px["BENCH_SPY"] = px["SPY"]; aug_px["BENCH_CASH"] = px["SHY"]
    aug_w  = core.reindex(px.index).fillna(0.0).copy()
    idle   = (1.0 - aug_w.sum(axis=1)).clip(lower=0.0)
    aug_w  = aug_w.reindex(columns=aug_px.columns).fillna(0.0)
    aug_w["BENCH_SPY"] = 0.0 * idle; aug_w["BENCH_CASH"] = 1.0 * idle
    eng_eager = backtest(aug_px, aug_w, cost_bps=0, freq=FREQ)
    g1r = float(np.abs(eager_shy["gross"] - eng_eager["returns"]).max())
    g1t = float(np.abs(eager_shy["turnover"] - eng_eager["turnover"]).max())
    eng25 = backtest(aug_px, aug_w, cost_bps=25, freq=FREQ)
    g2 = float(np.abs(net(eager_shy, 25) - eng25["returns"]).max())
    g3 = float(np.abs(nosleeve["gross"] - live_eng["returns"]).max())
    g4 = float(max(run_sleeve(px, core, flat_ret(px.index, y), h=h)["total"].max()
                   for y in (0.0, 0.05) for h in H_LADDER))
    # G5: a ZERO-RATE sleeve earns nothing, so its GROSS returns must equal the live book's
    flat0 = run_sleeve(px, core, flat_ret(px.index, 0.0), h=0.00)
    g5 = float(np.abs(flat0["gross"] - live_eng["returns"]).max())
    # G6: the synthetic flat line compounds to exactly y
    g6 = max(abs(metrics(flat_ret(px.index, y).loc[start:])["CAGR"] - y) for y in Y_LADDER)
    g7 = len(px.loc[start:]) / 252
    # G8: TRAIL is strictly lagged -> no same-day information
    g8 = float(np.corrcoef(trail.loc[start:].values, shy_r.loc[start:].values)[0, 1])
    for k, v, ok in [("G1 SHY runner == engine.backtest (returns)", g1r, g1r < 1e-12),
                     ("G1b SHY runner == engine.backtest (turnover)", g1t, g1t < 1e-12),
                     ("G2 derived 25 bps == fresh engine 25 bps", g2, g2 < 1e-12),
                     ("G3 NOSLEEVE == baseline.rules_v2_weights", g3, g3 == 0.0),
                     ("G4 max total weight (no leverage)", g4, g4 <= 1.0 + 1e-9),
                     ("G5 zero-rate sleeve gross == live book gross", g5, g5 < 1e-12),
                     ("G6 flat line compounds to y (max abs err)", g6, g6 < 1e-9),
                     ("G7 years of sample", g7, g7 >= 10.0),
                     ("G8 corr(TRAIL rate, same-day SHY ret) ~ 0", g8, abs(g8) < 0.10)]:
        gates.append(dict(panel=pname, gate=k, value=v, pass_=bool(ok)))
        log(f"GATE [{pname}] {k}: {v:.6g} -> {'PASS' if ok else 'FAIL'}")

    # ---- the book shelf -------------------------------------------
    books = {("NOSLEEVE", np.nan, np.nan): nosleeve}
    for h in H_LADDER:
        books[("SHY", np.nan, h)]   = run_sleeve(px, core, shy_r, h=h)
        books[("TRAIL", np.nan, h)] = run_sleeve(px, core, trail, h=h)
        for y in Y_LADDER:
            books[("FLAT", y, h)]   = run_sleeve(px, core, flat_ret(px.index, y), h=h)
    store[pname] = (px, start, spy_r, shy_r, trail, books, live_eng, core)

    for (kind, y, h), res in books.items():
        for c in COSTS:
            r    = net(res, c).loc[start:]
            live = net(dict(gross=live_eng["returns"], turnover=live_eng["turnover"]), c).loc[start:]
            for w in WINDOWS:
                rr, ll, ss = cut(r, w, start), cut(live, w, start), cut(spy_r, w, start)
                L, Lv, S = legs(rr), legs(ll), legs(ss)
                rows.append(dict(panel=pname, kind=kind, y=y, h=h, cost_bps=c, window=w,
                                 CAGR=L["CAGR"], Sharpe=L["Sharpe"], MaxDD=L["MaxDD"],
                                 H1=L["H1"], H2=L["H2"],
                                 turnover_per_yr=res["turnover"].loc[rr.index[0]:rr.index[-1]].sum() / (len(rr) / 252),
                                 mean_sleeve=res["sleeve"].loc[rr.index[0]:rr.index[-1]].mean(),
                                 live_CAGR=Lv["CAGR"], live_Sharpe=Lv["Sharpe"], live_MaxDD=Lv["MaxDD"],
                                 live_H1=Lv["H1"], live_H2=Lv["H2"],
                                 spy_CAGR=S["CAGR"], spy_Sharpe=S["Sharpe"], spy_MaxDD=S["MaxDD"],
                                 pass4a=pass4a(L, Lv), pass4b=pass4b(L, S),
                                 dCAGR=L["CAGR"]-Lv["CAGR"], dSharpe=L["Sharpe"]-Lv["Sharpe"],
                                 dH1=L["H1"]-Lv["H1"], dH2=L["H2"]-Lv["H2"], dDD=L["MaxDD"]-Lv["MaxDD"],
                                 cagr_floor=0.70*S["CAGR"], dd_cap=0.60*S["MaxDD"]))

grid = pd.DataFrame(rows)
grid.to_csv(str(OUT) + ".grid.csv", index=False)
pd.DataFrame(gates).to_csv(str(OUT) + ".gates.csv", index=False)
log(f"\npublished rows: {len(grid)}   gates: {sum(g['pass_'] for g in gates)} of {len(gates)} PASS")

def pick(pname, kind, y, h, c=10, w="FULL"):
    q = grid[(grid.panel == pname) & (grid.kind == kind) & (grid.h == h)
             & (grid.cost_bps == c) & (grid.window == w)]
    q = q[q.y.isna()] if (isinstance(y, float) and np.isnan(y)) else q[q.y == y]
    return q.iloc[0]
def ns(pname, c=10, w="FULL"):
    return grid[(grid.panel == pname) & (grid.kind == "NOSLEEVE") & (grid.cost_bps == c)
                & (grid.window == w)].iloc[0]

# ---------------------------------------------------------------- A. SHY's own rate path
log("\n" + "=" * 104)
log("A. WHAT THE RECORD IS CREDITING: SHY's OWN REALISED PATH (the thing 2227 calls a regime)")
for pname, (px, start, spy_r, shy_r, trail, *_ ) in store.items():
    s = shy_r.loc[start:]
    mF, mI, mO = metrics(s), metrics(s.loc[:IS_END]), metrics(s.loc[OOS_START:])
    yr = s.groupby(s.index.year).apply(lambda x: (1 + x).prod() - 1)
    log(f"  [{pname}] SHY CAGR FULL {mF['CAGR']:.2%}  IS {mI['CAGR']:.2%}  OOS {mO['CAGR']:.2%}   "
        f"MaxDD {mF['MaxDD']:.2%}   worst yr {yr.min():.2%} ({int(yr.idxmin())})  best {yr.max():.2%} ({int(yr.idxmax())})")
    log("    per-year: " + "  ".join(f"{int(k)}:{v:+.2%}" for k, v in yr.items()))
    t = trail.loc[start:]
    ta = ((1 + t) ** 252 - 1)
    log(f"    TRAIL implied annual rate: mean {ta.mean():.2%}  IS {ta.loc[:IS_END].mean():.2%}  "
        f"OOS {ta.loc[OOS_START:].mean():.2%}  min {ta.min():.2%}  max {ta.max():.2%}")

# ---------------------------------------------------------------- B. the gain as a function of y
log("\nB. THE GAIN AS A FUNCTION OF THE FLAT RATE y (h = 0.10, 10 bps) — vs the live RULES v2 book")
for pname in panels:
    b = ns(pname)
    log(f"  [{pname}] NOSLEEVE (live RULES v2): CAGR {b.CAGR:7.2%}  Sharpe {b.Sharpe:.4f}  "
        f"MaxDD {b.MaxDD:7.2%}  turn {b.turnover_per_yr:.2f}x")
    for y in Y_LADDER:
        r = pick(pname, "FLAT", y, 0.10)
        log(f"    FLAT y={y:5.1%}  CAGR {r.CAGR:7.2%} ({100*r.dCAGR:+.2f} pp)  Sharpe {r.Sharpe:.4f} "
            f"({r.dSharpe:+.4f})  MaxDD {r.MaxDD:7.2%} ({100*r.dDD:+.2f} pp)  turn {r.turnover_per_yr:.2f}x  "
            f"sleeve {r.mean_sleeve:.1%}  4a {str(r.pass4a):5} 4b {r.pass4b}")
    for k in ("SHY", "TRAIL"):
        r = pick(pname, k, np.nan, 0.10)
        log(f"    {k:<5} (realised) CAGR {r.CAGR:7.2%} ({100*r.dCAGR:+.2f} pp)  Sharpe {r.Sharpe:.4f} "
            f"({r.dSharpe:+.4f})  MaxDD {r.MaxDD:7.2%} ({100*r.dDD:+.2f} pp)  turn {r.turnover_per_yr:.2f}x  "
            f"sleeve {r.mean_sleeve:.1%}  4a {str(r.pass4a):5} 4b {r.pass4b}")

# ---------------------------------------------------------------- C. linearity + equivalent y
log("\nC. IS THE GAIN MECHANICAL?  dCAGR vs (mean sleeve share x y), and the y THAT REPRODUCES SHY")
for pname in panels:
    for w in WINDOWS:
        xs = np.array(Y_LADDER); dd = []
        for y in Y_LADDER:
            dd.append(pick(pname, "FLAT", y, 0.10, w=w).dCAGR)
        dd = np.array(dd)
        sl, ic = np.polyfit(xs, dd, 1)
        ms = pick(pname, "FLAT", 0.010, 0.10, w=w).mean_sleeve
        r2 = 1 - ((dd - (sl * xs + ic)) ** 2).sum() / ((dd - dd.mean()) ** 2).sum()
        shy = pick(pname, "SHY", np.nan, 0.10, w=w)
        y_eq = (shy.dCAGR - ic) / sl
        log(f"  [{pname}] {w:4} d(dCAGR)/dy {sl:+.4f} (mean sleeve share {ms:.4f}, ratio "
            f"{sl/ms:+.4f})  intercept {100*ic:+.3f} pp  R2 {r2:.6f}   "
            f"SHY dCAGR {100*shy.dCAGR:+.2f} pp -> EQUIVALENT FLAT y = {y_eq:.3%}")

# ---------------------------------------------------------------- D. the window asymmetry
log("\nD. THE ASYMMETRY 2227 POINTS AT: IS vs OOS GAIN, REALISED PATH vs FLAT RATE (h=0.10, 10 bps)")
for pname in panels:
    for k, y in [("SHY", np.nan), ("TRAIL", np.nan)] + [("FLAT", y) for y in (0.010, 0.015, 0.020)]:
        d = {w: pick(pname, k, y, 0.10, w=w) for w in WINDOWS}
        lbl = k if not (isinstance(y, float) and y == y) else f"FLAT {y:.1%}"
        log(f"  [{pname}] {lbl:<10} dCAGR IS {100*d['IS'].dCAGR:+.2f} pp  OOS {100*d['OOS'].dCAGR:+.2f} pp  "
            f"(OOS-IS {100*(d['OOS'].dCAGR-d['IS'].dCAGR):+.2f} pp)   dSharpe IS {d['IS'].dSharpe:+.4f}  "
            f"OOS {d['OOS'].dSharpe:+.4f}")

# ---------------------------------------------------------------- E. duration contribution
log("\nE. RATE LEVEL vs DURATION PATH: SHY against the FLAT arm INTERPOLATED to SHY's own CAGR")
for pname in panels:
    for w in WINDOWS:
        shy = pick(pname, "SHY", np.nan, 0.10, w=w)
        xs = np.array(Y_LADDER)
        sh = np.array([pick(pname, "FLAT", y, 0.10, w=w).Sharpe for y in Y_LADDER])
        dd = np.array([pick(pname, "FLAT", y, 0.10, w=w).MaxDD for y in Y_LADDER])
        cg = np.array([pick(pname, "FLAT", y, 0.10, w=w).CAGR for y in Y_LADDER])
        y_eq = float(np.interp(shy.CAGR, cg, xs))
        log(f"  [{pname}] {w:4} SHY CAGR {shy.CAGR:7.2%} == FLAT y {y_eq:.3%};  Sharpe SHY {shy.Sharpe:.4f} "
            f"vs matched FLAT {np.interp(y_eq, xs, sh):.4f} ({shy.Sharpe-np.interp(y_eq, xs, sh):+.4f})  "
            f"MaxDD SHY {shy.MaxDD:.2%} vs matched FLAT {np.interp(y_eq, xs, dd):.2%} "
            f"({100*(shy.MaxDD-np.interp(y_eq, xs, dd)):+.2f} pp)")

# ---------------------------------------------------------------- F. the 4a frontier in y
log("\nF. THE 4a FRONTIER IN y — the lowest flat rate at which the accounting fix still beats the book")
for pname in panels:
    for w in WINDOWS:
        for h in H_LADDER:
            line = []
            for c in COSTS:
                ok = [y for y in Y_LADDER if pick(pname, "FLAT", y, h, c=c, w=w).pass4a]
                line.append(f"{c}bps:" + (f"y>={min(ok):.1%}" if ok else "none"))
            log(f"  [{pname}] {w:4} h={h:4.2f}  4a frontier  " + "  ".join(line))
log("  (4a legs are cost-MATCHED: the live book pays the same bps as the candidate at every rung)")
n4a = int(grid.pass4a.sum()); n4b = int(grid.pass4b.sum())
log(f"  totals over all {len(grid)} rows: 4a {n4a}, 4b {n4b}")

log("\nG. 4b — WHICH LEG BINDS, AND WHETHER ANY FLAT RATE CAN REACH IT (h=0.10, 10 bps)")
for pname in panels:
    for w in WINDOWS:
        for y in (0.010, 0.020, 0.030, 0.050):
            r = pick(pname, "FLAT", y, 0.10, w=w)
            binding = [nm for nm, ok in [("H1", r.H1 > r.spy_Sharpe), ("H2", r.H2 > r.spy_Sharpe),
                                         ("DD", r.MaxDD >= r.dd_cap), ("CAGR", r.CAGR >= r.cagr_floor)] if not ok]
            log(f"  [{pname}] {w:4} y={y:4.1%} CAGR {r.CAGR:7.2%} vs floor {r.cagr_floor:6.2%} "
                f"({100*(r.CAGR-r.cagr_floor):+.2f} pp)  MaxDD {r.MaxDD:7.2%} vs cap {r.dd_cap:7.2%}  "
                f"halves {r.H1:.3f}/{r.H2:.3f} vs SPY {r.spy_Sharpe:.3f}  4b {str(r.pass4b):5} "
                f"binding {','.join(binding) if binding else '-'}")
# the flat rate that would be needed to clear the CAGR floor, by linear extrapolation in y
log("  y REQUIRED to clear the 4b CAGR FLOOR (linear in y, extrapolated beyond the ladder):")
for pname in panels:
    for w in WINDOWS:
        xs = np.array(Y_LADDER)
        cg = np.array([pick(pname, "FLAT", y, 0.10, w=w).CAGR for y in Y_LADDER])
        fl = pick(pname, "FLAT", 0.010, 0.10, w=w).cagr_floor
        sl, ic = np.polyfit(xs, cg, 1)
        log(f"    [{pname}] {w:4} floor {fl:.2%}  dCAGR/dy {sl:+.4f}  ->  y* = {(fl-ic)/sl:.2%}")

log("\nH. THE TURNOVER ASYMMETRY, QUANTIFIED NOT ASSUMED (core SHY/SPY weight the sleeve cannot net)")
for pname, (px, start, spy_r, shy_r, trail, books, live_eng, core) in store.items():
    cw = core.reindex(px.index).fillna(0.0).shift(1).loc[start:]
    log(f"  [{pname}] core SHY mean weight {cw['SHY'].mean():.4%} (nonzero on {(cw['SHY']>0).mean():.1%} of days); "
        f"core SPY {cw['SPY'].mean():.4%} ({(cw['SPY']>0).mean():.1%}); "
        f"SHY-arm turn {pick(pname,'SHY',np.nan,0.10).turnover_per_yr:.3f}x vs "
        f"FLAT-arm {pick(pname,'FLAT',0.010,0.10).turnover_per_yr:.3f}x")

# ---------------------------------------------------------------- rule 8
log("\nI. RULE 8 WALK-FORWARD — dials (y, h) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE")
log("   HONEST NOTE: C_SHARPE / C_4aIS choose y from IS data, which is a SENSITIVITY, not a")
log("   strategy — nobody picks next decade's cash rate.  C_TRAIL (h=0.10, trailing realised")
log("   rate, lagged) and C_ANCHOR (change nothing) are the only ARM-LEVEL implementable rules.")
CH = ["C_SHARPE", "C_4aIS", "C_TRAIL", "C_SHY", "C_ANCHOR"]
for pname in panels:
    for c in COSTS:
        isg = grid[(grid.panel == pname) & (grid.window == "IS") & (grid.cost_bps == c)
                   & (grid.kind == "FLAT")]
        oos = grid[(grid.panel == pname) & (grid.window == "OOS") & (grid.cost_bps == c)]
        picks = {"C_SHARPE": isg.sort_values("Sharpe", ascending=False).iloc[0]}
        a = isg[isg.pass4a]
        picks["C_4aIS"] = a.sort_values("Sharpe", ascending=False).iloc[0] if len(a) else None
        for ch in CH:
            if ch == "C_ANCHOR":
                o = oos[oos.kind == "NOSLEEVE"].iloc[0]; ky, kh, kk = np.nan, np.nan, "NOSLEEVE"
            elif ch == "C_TRAIL":
                o = oos[(oos.kind == "TRAIL") & (oos.h == 0.10)].iloc[0]; ky, kh, kk = np.nan, 0.10, "TRAIL"
            elif ch == "C_SHY":
                o = oos[(oos.kind == "SHY") & (oos.h == 0.10)].iloc[0]; ky, kh, kk = np.nan, 0.10, "SHY"
            else:
                p = picks[ch]
                if p is None:
                    wf_rows.append(dict(panel=pname, cost_bps=c, chooser=ch, note="IS admitted set EMPTY")); continue
                ky, kh, kk = p.y, p.h, "FLAT"
                o = oos[(oos.kind == "FLAT") & (oos.y == ky) & (oos.h == kh)].iloc[0]
            wf_rows.append(dict(panel=pname, cost_bps=c, chooser=ch, kind=kk, y=ky, h=kh,
                                OOS_CAGR=o.CAGR, OOS_Sharpe=o.Sharpe, OOS_MaxDD=o.MaxDD,
                                OOS_H1=o.H1, OOS_H2=o.H2, OOS_turn=o.turnover_per_yr,
                                OOS_4a=o.pass4a, OOS_4b=o.pass4b,
                                live_OOS_CAGR=o.live_CAGR, live_OOS_Sharpe=o.live_Sharpe,
                                live_OOS_MaxDD=o.live_MaxDD,
                                spy_OOS_CAGR=o.spy_CAGR, spy_OOS_Sharpe=o.spy_Sharpe,
                                spy_OOS_MaxDD=o.spy_MaxDD))
wf = pd.DataFrame(wf_rows); wf.to_csv(str(OUT) + ".walkforward.csv", index=False)
for pname in panels:
    for c in (10, 50):
        for _, r in wf[(wf.panel == pname) & (wf.cost_bps == c)].iterrows():
            if pd.isna(r.get("OOS_CAGR", np.nan)):
                log(f"  [{pname}] {c}bps {r.chooser}: {r.get('note','')}"); continue
            yl = "n/a" if pd.isna(r.y) else f"{r.y:.1%}"
            log(f"  [{pname}] {c}bps {r.chooser:9} pick {r['kind']:<8} y={yl:<5} h={r.h}  "
                f"OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  turn {r.OOS_turn:.2f}x  "
                f"halves {r.OOS_H1:.3f}/{r.OOS_H2:.3f}  4a {str(r.OOS_4a):5} 4b {r.OOS_4b}   "
                f"[live OOS {r.live_OOS_CAGR:6.2%}/{r.live_OOS_Sharpe:.4f}/{r.live_OOS_MaxDD:.2%}; "
                f"SPY OOS {r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:.2%}]")

log("\nJ. RULE 8, THE ONLY IMPLEMENTABLE ARM, AT EVERY COST RUNG (C_TRAIL vs C_ANCHOR)")
for pname in panels:
    for c in COSTS:
        t = wf[(wf.panel == pname) & (wf.cost_bps == c) & (wf.chooser == "C_TRAIL")].iloc[0]
        a = wf[(wf.panel == pname) & (wf.cost_bps == c) & (wf.chooser == "C_ANCHOR")].iloc[0]
        log(f"  [{pname}] {c:2}bps TRAIL OOS {t.OOS_CAGR:7.2%}/{t.OOS_Sharpe:.4f}/{t.OOS_MaxDD:7.2%} "
            f"vs ANCHOR {a.OOS_CAGR:7.2%}/{a.OOS_Sharpe:.4f}/{a.OOS_MaxDD:7.2%}  "
            f"d {100*(t.OOS_CAGR-a.OOS_CAGR):+.2f} pp / {t.OOS_Sharpe-a.OOS_Sharpe:+.4f} / "
            f"{100*(t.OOS_MaxDD-a.OOS_MaxDD):+.2f} pp  4a {t.OOS_4a}")

log("\nK. THE HEADLINE CAPITAL NUMBER: THE EXACT FLAT RATE AT WHICH 4a FLIPS (bisection on y,")
log("   h = 0.10, 60 iterations, each y a FULL fresh pricing of the book — not an interpolation)")
def flips(pname, c, w, h=0.10, lo=0.0, hi=0.08, iters=60):
    px, start, spy_r, shy_r, trail, books, live_eng, core = store[pname]
    live = net(dict(gross=live_eng["returns"], turnover=live_eng["turnover"]), c).loc[start:]
    Lv = legs(cut(live, w, start))
    def ok(y):
        r = net(run_sleeve(px, core, flat_ret(px.index, y), h=h), c).loc[start:]
        return pass4a(legs(cut(r, w, start)), Lv)
    if ok(lo): return lo, "passes at y=0"
    if not ok(hi): return float("nan"), "fails at y=8%"
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if ok(mid): hi = mid
        else: lo = mid
    return hi, ""
for pname in panels:
    for w in ("FULL", "OOS"):
        for c in COSTS:
            y0, note = flips(pname, c, w, iters=18)
            log(f"  [{pname}] {w:4} {c:2}bps  4a holds for y >= {y0:.3%}   {note}")
log("  SHY's realised path is EQUIVALENT to a flat y of 1.216% (U56 FULL) / 1.600% (U56 OOS) /")
log("  1.290% (B136 FULL) / 1.722% (B136 OOS) — section E.  Compare those to the frontiers above.")

Path(str(OUT) + ".log.txt").write_text("\n".join(log_lines) + "\n")
print("\nwrote", OUT.name + ".grid.csv/.gates.csv/.walkforward.csv/.log.txt")
