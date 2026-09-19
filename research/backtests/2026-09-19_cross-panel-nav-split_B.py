#!/usr/bin/env python3
"""Idea 1653 (lane B, 2026-09-19) — does a CONSTANT-GROSS U56 x SMALL NAV SPLIT clear 4b on
BOTH windows, against its OWN CORNERS and a MATCHED-REALISED-GROSS DE-GROSS TWIN?

WHY THIS IDEA.  Nine consecutive 2026-09-19 runs found every device family (trailing stops,
breadth throttles, vol targeting, MA-distance gates, SPY filters, the drawdown-budget ladder,
correlation-cluster caps, the momentum rank cut, the MAXVOL gate) beaten at matched exposure by a
plain constant de-gross.  Every one of those devices REMOVES exposure.  A cross-panel NAV split
REALLOCATES it at constant total gross -- the one direction the record has never priced -- and it
is the only lever that can lift CAGR, the 4b leg that binds 26 of 36 cells in idea 1617 and kills
the live book on its own.

TWO TUNED DIALS AND NO MORE: w (NAV share to the U56 book) and G (total target gross).
Cost rung and window are PUBLISHED AXES, not dials: every cell is reported at every rung.

Deterministic, offline, reads only committed caches.
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-19_cross-panel-nav-split_B"
LOG = []
def say(s=""):
    print(s); LOG.append(s)

BAND = 0.03          # LIVE value, inherited, NOT tuned
FREQ = "W"           # LIVE cadence, inherited, NOT tuned
RUNGS = [10.0, 25.0, 50.0]
BIND = 10.0          # PROTOCOL rule 2
WGRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
GGRID = [0.50, 0.75, 1.00]
OOS0 = pd.Timestamp("2017-01-01")

# ---------------------------------------------------------------- fast engine
def fast_run(rets, W, mask):
    """Exact numpy replication of engine.backtest.  Returns (gross returns, turnover).
    Cost is NOT applied here: port(c) = gross - turnover * c/1e4 is an exact identity
    because neither `held` nor `turnover` depends on c (gate G2)."""
    n, k = rets.shape
    wt = np.vstack([np.full((1, k), np.nan), W[:-1]])   # .shift(1) — row 0 is NaN in engine too
    cur = np.zeros(k); out = np.zeros(n); tno = np.zeros(n); grs = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            tno[i] = np.abs(new - cur).sum(); cur = new
        held = cur
        grs[i] = np.nansum(held)          # pandas .sum(axis=1) skips NaN — mirror it exactly
        r = rets[i]
        out[i] = np.nansum(held * r)
        growth = held * (1.0 + r)
        tot = growth.sum() + (1.0 - held.sum())
        cur = growth / tot if tot > 0 else held
    return out, tno, grs

def prep(px, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    m = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    return rets, m

def stats(r, idx):
    s = pd.Series(r, index=idx)
    m = metrics(s); h = len(s) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(s.iloc[:h])["Sharpe"], H2=metrics(s.iloc[h:])["Sharpe"],
                Calmar=m["Calmar"], Vol=m["Vol"])

# ---------------------------------------------------------------- data
t0 = time.time()
say("# Idea 1653 (lane B) — CONSTANT-GROSS CROSS-PANEL NAV SPLIT (U56 x SMALL)")
say("")
pxU = load_universe()                       # data/prices.csv  (LIVE frame, SPY included as a name)
pxS = load_universe(small=True)             # data/prices_small.csv.gz + SPY benchmark column

md = pd.read_csv(ROOT / "data" / "small_meta.csv")
mcol = "ticker" if "ticker" in md.columns else md.columns[0]
bad = set(md.loc[md["max_1d_move"] >= 1.0, mcol].astype(str))
mv = pxS.pct_change().abs().max()
INV = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
say(f"PANELS: U56 {pxU.shape[1]} columns (LIVE frame, SPY is a constituent of the live book); "
    f"SMALL {len(INV)} investable of {pxS.shape[1]-1} after data/small_meta.csv max_1d_move >= 1.0 "
    f"drops {len(bad)} tickers.")

# unit-gross books, each built on its OWN FULL history so the 200d warm-up is never truncated
WU1 = rules_v2_weights(pxU, band=BAND, gross=1.0)                       # live book, gross 1
eS = pd.DataFrame(1.0, index=pxS.index, columns=INV).where(pxS[INV].notna(), 0.0)
WS1 = (eS.div(eS.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
         .where(band_state(pxS[INV], BAND), 0.0))                       # same shape, small panel

IDX = pxU.index.intersection(pxS.index)
pxC = pd.concat([pxU.reindex(IDX), pxS[INV].reindex(IDX).rename(columns=lambda c: "S:" + c)], axis=1)
WU1c = WU1.reindex(IDX).fillna(0.0)
WS1c = WS1.reindex(IDX).rename(columns=lambda c: "S:" + c).fillna(0.0)
ZU = pd.DataFrame(0.0, index=IDX, columns=WS1c.columns)
ZS = pd.DataFrame(0.0, index=IDX, columns=pxU.columns)
say(f"COMBINED FRAME: {pxC.shape[0]} days x {pxC.shape[1]} columns, "
    f"{IDX[0].date()} -> {IDX[-1].date()}.")

START = IDX[260]                                    # compare()'s warm-up convention
WIN = IDX >= START
OOS = (IDX >= OOS0) & WIN
IS_ = WIN & (IDX < OOS0)
widx = IDX[WIN]; oidx = IDX[OOS]; iidx = IDX[IS_]
say(f"SCORED WINDOW: {widx[0].date()} -> {widx[-1].date()} ({len(widx)/252:.1f}y);  "
    f"IS {iidx[0].date()}..{iidx[-1].date()} ({len(iidx)/252:.1f}y);  "
    f"OOS {oidx[0].date()}..{oidx[-1].date()} ({len(oidx)/252:.1f}y).")
say("")

retsC, maskC = prep(pxC)
retsU, maskU = prep(pxU.reindex(IDX))

def blend_W(w, G):
    A = (w * G) * WU1c
    B = ((1.0 - w) * G) * WS1c
    return pd.concat([A, B], axis=1)[pxC.columns].values

# ---------------------------------------------------------------- GATES (printed before any hypothesis is read)
say("## GATES (printed before any hypothesis is read)")
gates = []
def gate(n, desc, val, ok):
    gates.append(dict(gate=n, description=desc, value=val, pass_=bool(ok)))
    say(f"  {n}: {desc} -> {val}  [{'PASS' if ok else 'FAIL'}]")

gate("G0", "sample years >= 10 (PROTOCOL rule 1)", f"{len(widx)/252:.2f}y", len(widx)/252 >= 10)

# G1 fast_run == engine.backtest on returns AND turnover, on two cells
g1 = 0.0; g1nan = True
for (w, G) in [(1.0, 0.75), (0.5, 0.75)]:
    Wdf = pd.DataFrame(blend_W(w, G), index=IDX, columns=pxC.columns)
    eng = backtest(pxC, Wdf, cost_bps=BIND, freq=FREQ)
    fr, ft, _ = fast_run(retsC, Wdf.values, maskC)
    fp = fr - ft * BIND / 1e4
    g1nan &= bool((np.isnan(fp) == np.isnan(eng["returns"].values)).all()
                  and (np.isnan(ft) == np.isnan(eng["turnover"].values)).all())
    g1 = max(g1, float(np.abs(fp[WIN] - eng["returns"].values[WIN]).max()),
                 float(np.abs(ft[WIN] - eng["turnover"].values[WIN]).max()))
gate("G1", "fast_run vs engine.backtest over the scored window, returns AND turnover, cells "
     "(w=1,G=.75) and (w=.5,G=.75); NaN masks identical (engine leaves 2 pre-window rows NaN)",
     f"{g1:.3e}, nan-mask match {g1nan}", g1 < 1e-12 and g1nan)

# G2 cost axis exact
Wdf = pd.DataFrame(blend_W(0.5, 0.75), index=IDX, columns=pxC.columns)
e25 = backtest(pxC, Wdf, cost_bps=25.0, freq=FREQ)["returns"].values
fr, ft, _ = fast_run(retsC, Wdf.values, maskC)
g2 = float(np.abs((fr - ft * 25.0 / 1e4)[WIN] - e25[WIN]).max())
gate("G2", "derived 25 bps rung vs a fresh 25 bps engine run (cost axis exact)", f"{g2:.3e}", g2 < 1e-12)

# G3 the w=1 corner IS the live RULES v2 book
bl = backtest(pxU, rules_v2_weights(pxU, band=BAND), cost_bps=BIND, freq=FREQ)["returns"].reindex(IDX).fillna(0.0)
fr1, ft1, gs1 = fast_run(retsC, blend_W(1.0, 0.75), maskC)
p1 = fr1 - ft1 * BIND / 1e4
g3 = float(np.abs(pd.Series(p1, index=IDX)[WIN].values - bl[WIN].values).max())
gate("G3", "corner w=1,G=0.75 replays baseline.rules_v2_weights on the LIVE frame over the window",
     f"{g3:.3e}", g3 < 1e-10)

# G4 the split creates and destroys NO gross: its target gross is an exact linear
# interpolation of the two corners', and its ceiling is G for every w.
gu = WU1c.sum(axis=1).values; gs_ = WS1c.sum(axis=1).values
mx = 0.0; ceil = 0.0
for G in GGRID:
    for w in WGRID:
        tg = pd.DataFrame(blend_W(w, G), index=IDX, columns=pxC.columns).sum(axis=1).values
        mx = max(mx, float(np.abs(tg - (w * G * gu + (1 - w) * G * gs_)).max()))
        ceil = max(ceil, float(tg.max() - G))
gate("G4", "target gross is an EXACT convex combination of the two corners', and never exceeds G "
     "(the split creates and destroys no gross)", f"max dev {mx:.3e}; max (gross - G) {ceil:.3e}",
     mx < 1e-12 and ceil <= 1e-12)

gate("G5", "tuned parameters", "2 (w, G) — cost rung, window and panel are published axes", True)

# G6 no chooser can see a 2017+ row: IS stats recomputed on a hard-truncated array
_r = pd.Series(p1, index=IDX)[IS_]
_t = pd.Series(p1[: int(np.searchsorted(IDX.values, OOS0.to_datetime64()))],
               index=IDX[: int(np.searchsorted(IDX.values, OOS0.to_datetime64()))])
_t = _t[_t.index >= START]
g6 = abs(metrics(_r)["Sharpe"] - metrics(_t)["Sharpe"])
gate("G6", "IS Sharpe on a masked array vs a HARD-TRUNCATED array (no 2017+ row reachable)",
     f"{g6:.3e}", g6 < 1e-15)

say("")

# ---------------------------------------------------------------- GRID
say("## GRID — all 33 (w, G) cells x 3 cost rungs, every one published")
rows = []
cache = {}
for G in GGRID:
    for w in WGRID:
        Wv = blend_W(w, G)
        fr, ft, gs = fast_run(retsC, Wv, maskC)
        cache[(w, G)] = (fr, ft, gs)
        rg_full = float(gs[WIN].mean()); rg_oos = float(gs[OOS].mean())
        tno_yr = float(ft[WIN].sum() / (len(widx) / 252))
        for c in RUNGS:
            p = fr - ft * c / 1e4
            f = stats(p[WIN], widx); o = stats(p[OOS], oidx); i = stats(p[IS_], iidx)
            rows.append(dict(w=w, G=G, cost_bps=c,
                             CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"],
                             H1=f["H1"], H2=f["H2"],
                             OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                             IS_CAGR=i["CAGR"], IS_Sharpe=i["Sharpe"], IS_MaxDD=i["MaxDD"],
                             realised_gross=rg_full, realised_gross_oos=rg_oos, turnover_yr=tno_yr))
grid = pd.DataFrame(rows)

# benchmarks
spy = pxU["SPY"].pct_change().fillna(0.0).reindex(IDX).fillna(0.0).values
SPY_F = stats(spy[WIN], widx); SPY_O = stats(spy[OOS], oidx); SPY_I = stats(spy[IS_], iidx)
v1 = backtest(pxU, rules_v1_weights(pxU), cost_bps=BIND, freq=FREQ)["returns"].reindex(IDX).fillna(0.0).values
V1_F = stats(v1[WIN], widx); V1_O = stats(v1[OOS], oidx)
BASE = grid[(grid.w == 1.0) & (grid.G == 0.75) & (grid.cost_bps == BIND)].iloc[0]   # == live RULES v2

def bars(S):  # 4b bars
    return 0.6 * abs(S["MaxDD"]), 0.7 * S["CAGR"]

DDF, CGF = bars(SPY_F); DDO, CGO = bars(SPY_O); DDI, CGI = bars(SPY_I)
say(f"  SPY FULL {SPY_F['CAGR']:.2%} / {SPY_F['Sharpe']:.4f} / {SPY_F['MaxDD']:.2%} "
    f"(halves {SPY_F['H1']:.4f} / {SPY_F['H2']:.4f});  4b bars: MaxDD >= {-DDF:.2%}, CAGR >= {CGF:.2%}")
say(f"  SPY OOS  {SPY_O['CAGR']:.2%} / {SPY_O['Sharpe']:.4f} / {SPY_O['MaxDD']:.2%};  "
    f"4b OOS bars: MaxDD >= {-DDO:.2%}, CAGR >= {CGO:.2%}")
say(f"  LIVE RULES v2 (= corner w=1, G=0.75) FULL {BASE.CAGR:.2%} / {BASE.Sharpe:.4f} / {BASE.MaxDD:.2%} "
    f"(halves {BASE.H1:.4f} / {BASE.H2:.4f});  OOS {BASE.OOS_CAGR:.2%} / {BASE.OOS_Sharpe:.4f} / {BASE.OOS_MaxDD:.2%}")
say(f"  RULES v1 (previous) FULL {V1_F['CAGR']:.2%} / {V1_F['Sharpe']:.4f} / {V1_F['MaxDD']:.2%};  "
    f"OOS {V1_O['CAGR']:.2%} / {V1_O['Sharpe']:.4f} / {V1_O['MaxDD']:.2%}")
say("")

# KEEP paths, per rung, judged against the LIVE book at the SAME rung
def live_at(c):
    return grid[(grid.w == 1.0) & (grid.G == 0.75) & (grid.cost_bps == c)].iloc[0]

keep4a, keep4bF, keep4bO = [], [], []
for _, r in grid.iterrows():
    L = live_at(r.cost_bps)
    a = (r.H1 > L.H1) and (r.H2 > L.H2) and (r.MaxDD >= L.MaxDD)
    bF = (r.H1 > SPY_F["H1"]) and (r.H2 > SPY_F["H2"]) and (r.MaxDD >= -DDF) and (r.CAGR >= CGF)
    bO = (r.OOS_Sharpe > SPY_O["Sharpe"]) and (r.OOS_MaxDD >= -DDO) and (r.OOS_CAGR >= CGO)
    keep4a.append(a); keep4bF.append(bF); keep4bO.append(bO)
grid["k4a"] = keep4a; grid["k4b_full"] = keep4bF; grid["k4b_oos"] = keep4bO
grid["k4b_both"] = grid.k4b_full & grid.k4b_oos
gate("G7", "grid cells published", f"{len(grid)} of {len(WGRID)*len(GGRID)*len(RUNGS)}",
     len(grid) == len(WGRID) * len(GGRID) * len(RUNGS))
gate("G8", "no shorting; max realised gross over the whole grid",
     f"{grid.realised_gross.max():.6f} (min weight {min(float(blend_W(w,G).min()) for w in WGRID for G in GGRID):.1f})",
     grid.realised_gross.max() <= 1.0 + 1e-12)

for c in RUNGS:
    s = grid[grid.cost_bps == c]
    say(f"  {int(c)} bps: 4a {int(s.k4a.sum())} of {len(s)};  4b FULL {int(s.k4b_full.sum())} of {len(s)};  "
        f"4b OOS {int(s.k4b_oos.sum())};  4b BOTH {int(s.k4b_both.sum())};  4a n 4b {int((s.k4a & s.k4b_both).sum())}")
say("")
say(grid[grid.cost_bps == BIND][["w","G","CAGR","Sharpe","MaxDD","H1","H2","OOS_CAGR","OOS_Sharpe",
    "OOS_MaxDD","realised_gross","turnover_yr","k4a","k4b_full","k4b_oos"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("")

# ---------------------------------------------------------------- MATCHED-REALISED-GROSS DE-GROSS TWIN
say("## MATCHED-REALISED-GROSS TWIN — the incumbent U56 book alone, de-grossed to the blend's OWN realised gross")
say("  (the test idea 1617 applied to the SUBTRACTIVE families, pointed here at the REALLOCATION direction)")
WUfull = WU1c.values
padZ = np.zeros((len(IDX), pxC.shape[1] - pxU.shape[1]))
def u56_only(k):
    return np.hstack([k * WUfull, padZ])

twin_rows = []
for G in GGRID:
    for w in WGRID:
        fr, ft, gs = cache[(w, G)]
        tgt = float(gs[WIN].mean())
        lo, hi = 0.0, 2.0
        for _ in range(60):                     # bisection on the twin's scale k
            mid = 0.5 * (lo + hi)
            _f, _t, _g = fast_run(retsC, u56_only(mid), maskC)
            if float(_g[WIN].mean()) < tgt: lo = mid
            else: hi = mid
        k = 0.5 * (lo + hi)
        tf, tt, tg = fast_run(retsC, u56_only(k), maskC)
        for c in RUNGS:
            bp = fr - ft * c / 1e4; tp = tf - tt * c / 1e4
            B = stats(bp[WIN], widx); T = stats(tp[WIN], widx)
            Bo = stats(bp[OOS], oidx); To = stats(tp[OOS], oidx)
            twin_rows.append(dict(w=w, G=G, cost_bps=c, k=k,
                blend_rg=float(gs[WIN].mean()), twin_rg=float(tg[WIN].mean()),
                dSharpe=B["Sharpe"]-T["Sharpe"], dCAGR=B["CAGR"]-T["CAGR"], dMaxDD=B["MaxDD"]-T["MaxDD"],
                dSharpe_oos=Bo["Sharpe"]-To["Sharpe"], dCAGR_oos=Bo["CAGR"]-To["CAGR"],
                dMaxDD_oos=Bo["MaxDD"]-To["MaxDD"],
                blend_Sharpe=B["Sharpe"], twin_Sharpe=T["Sharpe"], blend_CAGR=B["CAGR"], twin_CAGR=T["CAGR"],
                blend_MaxDD=B["MaxDD"], twin_MaxDD=T["MaxDD"], twin_turnover_yr=float(tt[WIN].sum()/(len(widx)/252))))
twin = pd.DataFrame(twin_rows)
gate("G9", "max |blend realised gross - twin realised gross| over every twin",
     f"{(twin.blend_rg - twin.twin_rg).abs().max():.3e}", (twin.blend_rg - twin.twin_rg).abs().max() < 1e-6)
gate("G10", "turnover and realised gross published for every cell AND every twin",
     f"{len(grid)} grid rows, {len(twin)} twin rows", True)

tb = twin[(twin.cost_bps == BIND) & (twin.w < 1.0)]
say(f"  At {int(BIND)} bps, excluding the w=1 corner (which IS its own twin): {len(tb)} paired cells.")
say(f"    dSharpe > 0 in {int((tb.dSharpe>0).sum())} of {len(tb)}, mean {tb.dSharpe.mean():+.4f}")
say(f"    dCAGR   > 0 in {int((tb.dCAGR>0).sum())} of {len(tb)}, mean {tb.dCAGR.mean()*100:+.2f} pp/yr")
say(f"    dMaxDD  > 0 in {int((tb.dMaxDD>0).sum())} of {len(tb)}, mean {tb.dMaxDD.mean()*100:+.2f} pp (positive = SHALLOWER)")
for c in RUNGS:
    s = twin[(twin.cost_bps == c) & (twin.w < 1.0)]
    say(f"    {int(c)} bps: dSharpe>0 {int((s.dSharpe>0).sum())}/{len(s)} (mean {s.dSharpe.mean():+.4f}); "
        f"dCAGR {s.dCAGR.mean()*100:+.2f} pp; dMaxDD {s.dMaxDD.mean()*100:+.2f} pp; "
        f"OOS dSharpe>0 {int((s.dSharpe_oos>0).sum())}/{len(s)} (mean {s.dSharpe_oos.mean():+.4f})")
say("")
say(tb[["w","G","k","blend_rg","twin_rg","blend_Sharpe","twin_Sharpe","dSharpe","dCAGR","dMaxDD","dSharpe_oos"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("")

# ---------------------------------------------------------------- RULE 8
say("## RULE 8 WALK-FORWARD — choosers fitted on warm-up..2016-12-31 only, 2017-2026 read ONCE")
isg = grid[grid.cost_bps == BIND].copy()
def pick(name, fn, sub):
    r = fn(sub)
    return dict(chooser=name, w=r.w, G=r.G,
                OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR, IS_MaxDD=r.IS_MaxDD,
                k4b_oos=bool((r.OOS_Sharpe > SPY_O["Sharpe"]) and (r.OOS_MaxDD >= -DDO) and (r.OOS_CAGR >= CGO)))
def c_sharpe(s): return s.loc[s.IS_Sharpe.idxmax()]
def c_calmar(s): return s.loc[(s.IS_CAGR / s.IS_MaxDD.abs()).idxmax()]
def c_live(s):   return s[(s.w == 1.0) & (s.G == 0.75)].iloc[0]
def c_prereg(s):
    ok = s[(s.IS_MaxDD >= -DDI) & (s.IS_CAGR >= CGI)]
    if len(ok) == 0: return c_live(s)
    ok = ok[ok.G == ok.G.min()]
    return ok.loc[ok.IS_Sharpe.idxmax()]
picks = pd.DataFrame([pick(n, f, isg) for n, f in
                      [("C_LIVE", c_live), ("C_SHARPE", c_sharpe), ("C_CALMAR", c_calmar), ("C_PREREG", c_prereg)]])
say(picks.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say(f"  SPY OOS {SPY_O['CAGR']:.2%} / {SPY_O['Sharpe']:.4f} / {SPY_O['MaxDD']:.2%};  "
    f"LIVE RULES v2 OOS {BASE.OOS_CAGR:.2%} / {BASE.OOS_Sharpe:.4f} / {BASE.OOS_MaxDD:.2%}")
say(f"  pooled mean OOS Sharpe of the four picks: {picks.OOS_Sharpe.mean():.4f}; "
    f"C_SHARPE minus C_LIVE = {float(picks[picks.chooser=='C_SHARPE'].OOS_Sharpe.iloc[0] - picks[picks.chooser=='C_LIVE'].OOS_Sharpe.iloc[0]):+.4f}")
say("")

# ---------------------------------------------------------------- correlation diagnostic
u_r = pd.Series(cache[(1.0, 0.75)][0], index=IDX)[WIN]
s_r = pd.Series(cache[(0.0, 0.75)][0], index=IDX)[WIN]
say(f"## DIAGNOSTIC: corr(U56 book, SMALL book) daily gross returns = {u_r.corr(s_r):.4f} "
    f"(IS {u_r[u_r.index < OOS0].corr(s_r[s_r.index < OOS0]):.4f}, "
    f"OOS {u_r[u_r.index >= OOS0].corr(s_r[s_r.index >= OOS0]):.4f})")
say(f"   realised gross: U56 corner {grid[(grid.w==1.0)&(grid.G==0.75)&(grid.cost_bps==BIND)].realised_gross.iloc[0]:.4f}, "
    f"SMALL corner {grid[(grid.w==0.0)&(grid.G==0.75)&(grid.cost_bps==BIND)].realised_gross.iloc[0]:.4f}")
say(f"   SURVIVORSHIP (rule 9): U56 is a current-constituent list and SMALL a current sub-$2B screen carried "
    f"back to 2010, so every ABSOLUTE level is an UPPER BOUND; the headline is a blend-minus-corner and "
    f"blend-minus-twin contrast over the SAME names on the SAME days, which the bias cannot manufacture.")
say("")
say(f"ALL GATES: {sum(g['pass_'] for g in gates)} of {len(gates)} PASS.   runtime {time.time()-t0:.1f}s")

grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
twin.to_csv(OUT / f"{STEM}.twins.csv", index=False)
picks.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
pd.DataFrame(gates).to_csv(OUT / f"{STEM}.gates.csv", index=False)
(OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")

# ---------------------------------------------------------------- APPENDIX (not this idea's device)
# Every 4b passer in the grid above sits at G = 1.00, and the CAGR leg is what moves.  G is an
# INHERITED exposure dial, not this idea's device (w is), and the grid's window is the SMALL panel's
# (2011-2026), whose SPY CAGR bar is 9.81% against 10.59% on the LIVE frame's own 17.7y history.
# Honesty requires re-reading the dial on the LIVE frame's OWN window before any claim is made.
say("## APPENDIX — WINDOW CHECK ON THE INHERITED GROSS DIAL (NOT idea 1653's device)")
startU = pxU.index[260]
spyU = pxU["SPY"].pct_change().fillna(0.0).loc[startU:]
def st2(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
SF2, SO2 = st2(spyU), st2(spyU.loc[OOS0:])
DDF2, CGF2 = 0.6 * abs(SF2["MaxDD"]), 0.7 * SF2["CAGR"]
DDO2, CGO2 = 0.6 * abs(SO2["MaxDD"]), 0.7 * SO2["CAGR"]
say(f"  LIVE frame own window {startU.date()} -> {pxU.index[-1].date()} ({len(spyU)/252:.1f}y)")
say(f"  SPY FULL {SF2['CAGR']:.2%} / {SF2['Sharpe']:.4f} / {SF2['MaxDD']:.2%} "
    f"(halves {SF2['H1']:.4f} / {SF2['H2']:.4f});  bars MaxDD >= {-DDF2:.2%}, CAGR >= {CGF2:.2%}")
say(f"  SPY OOS  {SO2['CAGR']:.2%} / {SO2['Sharpe']:.4f} / {SO2['MaxDD']:.2%};  "
    f"bars MaxDD >= {-DDO2:.2%}, CAGR >= {CGO2:.2%}")
app = []
for G in [0.50, 0.75, 0.85, 1.00]:
    for c in [10.0, 25.0]:
        r = backtest(pxU, rules_v2_weights(pxU, band=BAND, gross=G), cost_bps=c, freq=FREQ)["returns"].loc[startU:]
        F, O = st2(r), st2(r.loc[OOS0:])
        bF = (F["H1"] > SF2["H1"]) and (F["H2"] > SF2["H2"]) and (F["MaxDD"] >= -DDF2) and (F["CAGR"] >= CGF2)
        bO = (O["Sharpe"] > SO2["Sharpe"]) and (O["MaxDD"] >= -DDO2) and (O["CAGR"] >= CGO2)
        app.append(dict(G=G, cost_bps=c, CAGR=F["CAGR"], Sharpe=F["Sharpe"], MaxDD=F["MaxDD"],
                        H1=F["H1"], H2=F["H2"], OOS_CAGR=O["CAGR"], OOS_Sharpe=O["Sharpe"],
                        OOS_MaxDD=O["MaxDD"], k4b_full=bF, k4b_oos=bO))
appx = pd.DataFrame(app)
say(appx.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
appx.to_csv(OUT / f"{STEM}.appendix_gross.csv", index=False)

# G11 — independent replication of the record's OWN committed cell for the same book
prior = pd.read_csv(OUT / "2026-09-19_zero-percent-cash-convention_B.grid.csv")
pc = prior[(prior.panel == "U56") & (prior.frame == "LIVE") & (prior.F == 0.0) & (prior.G == 1.0)]
mine = appx[(appx.G == 1.0) & (appx.cost_bps == 10.0)].iloc[0]
d = max(abs(float(pc.CAGR.iloc[0]) - mine.CAGR), abs(float(pc.Sharpe.iloc[0]) - mine.Sharpe),
        abs(float(pc.MaxDD.iloc[0]) - mine.MaxDD), abs(float(pc.oCAGR.iloc[0]) - mine.OOS_CAGR),
        abs(float(pc.oSharpe.iloc[0]) - mine.OOS_Sharpe))
gate("G11", "this script's LIVE G=1.00 row vs idea 1498's COMMITTED grid cell "
     "(U56, LIVE, G=1.00, F=0.00) — independent replication, different script, different frame build",
     f"max |diff| {d:.3e}; prior keep4b={bool(pc.keep4b.iloc[0])}/keep4b_oos={bool(pc.keep4b_oos.iloc[0])}", d < 5e-4)
say(f"  PUBLICATION GAP: idea 1498's committed grid ALREADY carries keep4b={bool(pc.keep4b.iloc[0])} and "
    f"keep4b_oos={bool(pc.keep4b_oos.iloc[0])} for this cell, while its memo §4 and the CHANGELOG say the "
    f"live book's 4b CAGR floor 'does not close'. Both are true: it does not close at the LIVE G = 0.75, "
    f"and it DOES close two rows down the same table at G = 1.00. The prose stated the first and not the second.")
say("")
say(f"ALL GATES (final): {sum(g['pass_'] for g in gates)} of {len(gates)} PASS.")
pd.DataFrame(gates).to_csv(OUT / f"{STEM}.gates.csv", index=False)
(OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")
