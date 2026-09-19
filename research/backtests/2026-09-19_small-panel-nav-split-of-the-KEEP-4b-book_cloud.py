#!/usr/bin/env python3
"""Idea 1645 (lane cloud, 2026-09-19) — does the SMALL-PANEL BOOK ADD ANYTHING to the U56 BOOK
at CONSTANT TOTAL GROSS?

WHY THIS IDEA, AND WHAT IS *NOT* BEING RE-RUN.  Nine consecutive 2026-09-19 runs found every
device family beaten at matched exposure by a plain constant de-gross: every device REMOVES
exposure.  A cross-panel NAV split REALLOCATES it at constant total gross, so it is the one
lever that can lift CAGR -- the 4b leg that binds 26 of 36 cells in idea 1617 -- without buying
drawdown.  Lane B's idea 1653 is 1645's full capital arm and it already KILLED the split of the
LIVE RULES v2 BAND book (dSharpe > 0 in 0 of 30 paired cells at 10/25/50 bps).  It did NOT split
the book that matters for real capital: the 2026-09-04 KEEP-4b candidate (top-N equal weight, NO
vol scaler, 126-row min hold, weekly, t+1).  This run asks 1645's question of THAT book.  If the
answer agrees with 1653 the two together retire the whole cross-panel-reallocation family.

THE CONSTRUCTION, FIXED BEFORE ANY NUMBER IS READ.
  Each sleeve is the 2026-09-04 recipe at N = 20 on its own panel, built on that panel's own full
  price history with the frozen mechanics below.  The two unit-gross HELD FRAMES are then
  reindexed onto the COMMON trading-day index and combined into ONE target weight matrix

        W(t) = w * G * W_U56(t)  +  (1 - w) * G * W_SMALL(t)

  which is run through ONE engine pass over the union of the two panels' weekly application rows,
  letting weights drift between rows exactly as the engine does.  Turnover is therefore the
  portfolio's own sum |dw| -- no sleeve-rebalancing convention is invented, and nothing is
  approximated.  Total TARGET gross is G at every w by construction, so the w = 1 corner IS the
  realised-gross-matched de-gross twin of every interior cell: any gain at w < 1 is PURE
  REALLOCATION and cannot be a re-gross.  Realised mean gross is published per cell as the check.

TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  w  {0.0, 0.1, ... 1.0}        11 rungs   (1.0 = pure U56 corner = the de-gross twin; 0.0 = pure SMALL)
  G  {0.50, 0.75, 1.00}          3 rungs   (0.75 = the 2026-09-04 anchor and the live value)
  = 33 cells, EVERY ONE PUBLISHED, each at FOUR cost rungs {0, 10, 25, 50} bps.
  Cost rung and window are PUBLISHED AXES, not dials.

FROZEN, NOT DIALS: N = 20, H = 126-row min hold, weekly cadence deciding on the last trading row
of the week (Fri phase) applying at t+1 (rule 2), above-200d AND vol20 < 0.60 eligibility, the
3-leg composite (21/252, 0/126, 0/63) equal-ranked and halved below the 200d average, NO vol
scaler, equal weights, 260-row warm-up per panel, first-wins stable tie-break, cash at 0%.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(common-index start .. 2016-12-31) ONLY, pick the (w, G) maximising IS Sharpe; ties to the LOWER
G, then the HIGHER w (i.e. ties resolve TOWARD the incumbent U56 corner).  A second, declared
chooser maximising J(IS) := min(dd_margin, cagr_margin) is reported beside it.  2017-2026 is then
read ONCE.  The pre-registered PASS for this idea is strictly harder than 4b alone: the chosen
cell must beat its OWN w = 1 corner at the same G, out of sample, on Sharpe AND CAGR.

SURVIVORSHIP (rule 9).  U56 is the CURRENT constituent list of a hand-kept mega-cap/ETF universe;
SMALL is the CURRENT constituent list of a sub-$2B screen, so its delisted, acquired and bankrupt
names are ABSENT.  That bias is WORST on the small panel, so every number the SMALL sleeve
contributes here is an UPPER bound on what it would have earned, and a KILL of the split is
therefore the STRONGER reading, not the weaker one.  Tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped before anything is built.

PROTOCOL: rule 2 execution and costs; rule 3 baselines (RULES v2 live AND SPY); rule 4 both KEEP
paths at every cell; rule 8 walk-forward with 2017-2026 read once; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Deterministic, offline, committed caches only:
  python research/backtests/2026-09-19_small-panel-nav-split-of-the-KEEP-4b-book_cloud.py
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest                                   # noqa: E402

STEM = Path(str(Path(__file__))[:-3])
WARMUP, MAXVOL, N_FIX, A_H, A_PHASE, A_DELAY = 260, 0.60, 20, 126, 4, 1
LEGS = [(21, 252), (0, 126), (0, 63)]
WGRID = [round(0.1 * i, 1) for i in range(11)]
GGRID = [0.50, 0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0                                   # PROTOCOL rule 2
IS_END, OOS0 = pd.Timestamp("2016-12-31"), pd.Timestamp("2017-01-01")
_LOG: list[str] = []
def say(s=""):
    print(s); _LOG.append(s)

# ------------------------------------------------------------------ mechanics (2026-09-04 book)
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)

def decision_rows(idx, wd):
    pos = np.arange(len(idx)); ok = idx.weekday <= wd
    s = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(s.groupby(level=0).max().values)

class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest, self.idx = name, px, invest, px.index
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.priced = px.notna().values
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.dec = decision_rows(px.index, A_PHASE)

def build(pan, N=N_FIX, d=A_DELAY):
    """Unit-gross top-N min-hold HELD FRAME of the 2026-09-04 book (gross-independent)."""
    T, M = pan.priced.shape; K = len(pan.iinv)
    app = pan.dec + d; app = app[app < T]; dec = pan.dec[:len(app)]
    W = np.zeros((T, M)); cur = np.full(K, -1, dtype=np.int64); pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young): young = young[pr[t, young]]
        ks = set(int(c) for c in young); need = N - len(ks); take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks: k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]): break
                take.append(int(c))
        new = np.full(K, -1, dtype=np.int64)
        for c in ks: new[c] = cur[c]
        for c in take: new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = app[i + 1] if i + 1 < len(app) else T
        if len(sel): W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return pd.DataFrame(W, index=pan.idx, columns=pan.px.columns), app

def run(rets, Cp, Wt, app):
    """Exact engine semantics: set target on each application row, drift in between."""
    T, M = rets.shape
    held = np.zeros((T, M)); turn = np.zeros(T); curw = np.zeros(M)
    ends = np.append(app[1:], T)
    for i0, i1 in zip(app, ends):
        w0 = Wt[i0]; turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - w0.sum())
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    return (held * rets).sum(axis=1), turn, held.sum(axis=1)

# ------------------------------------------------------------------ metrics / verdicts
def mt(r):
    r = np.asarray(r, float)
    if len(r) < 20: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd)

def windows(idx):
    n = len(idx); h = n // 2
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS0)
    return dict(FULL=np.ones(n, bool), H1=h1, H2=h2, IS=~oos, OOS=oos)

def cell(r, spy, live, W):
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[W["H1"]]), mt(r[W["H2"]]); s1, s2 = mt(spy[W["H1"]]), mt(spy[W["H2"]])
    l1, l2 = mt(live[W["H1"]]), mt(live[W["H2"]])
    Ri, Ro, So = mt(r[W["IS"]]), mt(r[W["OOS"]]), mt(spy[W["OOS"]])
    a = dict(a_h1=bool(r1["Sharpe"] > l1["Sharpe"]), a_h2=bool(r2["Sharpe"] > l2["Sharpe"]),
             a_dd=bool(R["MaxDD"] >= L["MaxDD"]))
    b = dict(b_h1=bool(r1["Sharpe"] > s1["Sharpe"]), b_h2=bool(r2["Sharpe"] > s2["Sharpe"]),
             b_oos=bool(Ro["Sharpe"] > So["Sharpe"]),
             b_dd=bool(R["MaxDD"] >= 0.60 * S["MaxDD"]),
             b_cagr=bool(R["CAGR"] >= 0.70 * S["CAGR"]))
    ddm = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"]); cgm = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    Si = mt(spy[W["IS"]])
    ddi = 100.0 * (mt(r[W["IS"]])["MaxDD"] - 0.60 * Si["MaxDD"])
    cgi = 100.0 * (Ri["CAGR"] - 0.70 * Si["CAGR"])
    ddo = 100.0 * (Ro["MaxDD"] - 0.60 * So["MaxDD"]); cgo = 100.0 * (Ro["CAGR"] - 0.70 * So["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"], H2=r2["Sharpe"],
                IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"], IS_MaxDD=Ri["MaxDD"],
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                dd_margin=ddm, cagr_margin=cgm, J_FULL=min(ddm, cgm), J_IS=min(ddi, cgi),
                J_OOS=min(ddo, cgo), pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1645 (lane cloud, 2026-09-19) — does the SMALL-PANEL BOOK ADD ANYTHING to the U56 BOOK")
    say("at CONSTANT TOTAL GROSS?   Book = the 2026-09-04 KEEP-4b candidate (top-20, no vol scaler).")
    say("=" * 108); say()
    say(f"  DIALS (2, rule 4): w {WGRID}  x  G {GGRID}  = {len(WGRID)*len(GGRID)} cells, ALL published,")
    say(f"                     each at cost rungs {RUNGS} bps (published axis, not a dial).")
    say("  FROZEN: N=20, H=126 min hold, weekly Fri decision, t+1, above-200d & vol20<0.60, equal weights.")
    say("  w = 1.0 IS the realised-gross-matched de-gross twin of every interior cell (total gross = G).")
    say()

    pxU = load_universe(); pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    invU = [c for c in pxU.columns if c != "SPY"]
    invS = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    panU, panS = Panel("U56", pxU, invU), Panel("SMALL", pxS, invS)
    WU, _ = build(panU); WS, _ = build(panS)

    # ---- common index: both panels warmed up, both trading
    startU, startS = panU.idx[WARMUP], panS.idx[WARMUP]
    idx = pxU.index.intersection(pxS.index)
    idx = idx[idx >= max(startU, startS)]
    overlap = sorted(set(invU) & set(invS))
    say(f"  PANELS: U56 {len(invU)} investable; SMALL {len(invS)} ({n_drop} dropped, max_1d_move >= 1.0).")
    say(f"          ticker overlap between the two sleeves: {len(overlap)} {overlap if overlap else ''}")
    say(f"  COMMON INDEX: {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} rows, {len(idx)/252:.1f}y);")
    say(f"          IS = start..{IS_END.date()} ({int((idx <= IS_END).sum())} rows), "
        f"OOS = {OOS0.date()}.. ({int((idx >= OOS0).sum())} rows).")
    say()

    cols = sorted(set(WU.columns) | set(WS.columns))
    FU = WU.reindex(index=idx, columns=cols).fillna(0.0).values
    FS = WS.reindex(index=idx, columns=cols).fillna(0.0).values
    PX = pd.concat([pxU.reindex(idx), pxS.reindex(idx).drop(columns=["SPY"], errors="ignore")],
                   axis=1).reindex(columns=cols)
    rets = PX.pct_change().fillna(0.0).values
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
    def app_pos(pan):
        a = pan.dec + A_DELAY
        a = a[a < len(pan.idx)]
        pos = idx.get_indexer(pan.idx[a])
        return pos[pos >= 0]
    app = np.unique(np.concatenate([app_pos(panU), app_pos(panS)]))
    if app[0] != 0: app = np.concatenate([[0], app])
    W = windows(idx)

    spy = pxU["SPY"].reindex(idx).pct_change().fillna(0.0).values
    live = backtest(pxU, rules_v2_weights(pxU), cost_bps=BIND, freq="W")["returns"].reindex(idx).fillna(0.0).values

    say("=" * 108); say("ARM A — BENCHMARKS on the COMMON index (rule 3).  4a is judged against RULES v2 (live).")
    say("=" * 108); say()
    say(f"  {'series':26} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} {'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8}")
    for lab, s in (("SPY (buy & hold)", spy), ("RULES v2 (live, 10bps)", live)):
        m, mo = mt(s), mt(s[W["OOS"]])
        say(f"  {lab:26} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
            f"{mt(s[W['H1']])['Sharpe']:7.4f} {mt(s[W['H2']])['Sharpe']:7.4f} "
            f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
    ms, mso = mt(spy), mt(spy[W["OOS"]])
    say(f"  4b bars: FULL MaxDD cap {0.60*ms['MaxDD']:7.2%}  CAGR floor {0.70*ms['CAGR']:6.2%}   "
        f"| OOS cap {0.60*mso['MaxDD']:7.2%}  floor {0.70*mso['CAGR']:6.2%}")
    say()

    # ---- grid
    rows = []
    for g in GGRID:
        for w in WGRID:
            Wt = g * (w * FU + (1.0 - w) * FS)
            gr, turn, gsum = run(rets, Cp, Wt, app)
            for c in RUNGS:
                r = gr - turn * c / 1e4
                d = cell(r, spy, live, W)
                d.update(w=w, G=g, cost=c, turns_yr=float(turn.sum() / (len(idx) / 252.0)),
                         mean_gross=float(gsum.mean()))
                rows.append(d)
    GD = pd.DataFrame(rows)
    order = ["G", "w", "cost", "mean_gross", "turns_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "IS_CAGR", "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "dd_margin", "cagr_margin", "J_FULL", "J_IS", "J_OOS", "pass4a", "pass4b",
             "a_h1", "a_h2", "a_dd", "b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"]
    GD = GD[order].sort_values(["G", "w", "cost"]).reset_index(drop=True)
    GD.to_csv(str(STEM) + ".grid.csv", index=False)

    say("=" * 108); say(f"ARM B — THE FULL {len(WGRID)*len(GGRID)} - CELL GRID at the BINDING {BIND:.0f} bps rung (all "
                        f"{len(GD)} cost readings in .grid.csv).")
    say("=" * 108); say()
    b10 = GD[GD.cost == BIND]
    say(f"  {'G':>5} {'w':>5} {'gross':>6} {'trn/y':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'J_FULL':>8} {'J_OOS':>8} {'4a':>4} {'4b':>4}")
    for _, r in b10.iterrows():
        say(f"  {r.G:5.2f} {r.w:5.1f} {r.mean_gross:6.3f} {r.turns_yr:6.2f} {r.CAGR:8.2%} {r.Sharpe:8.4f} "
            f"{r.MaxDD:8.2%} {r.H1:7.4f} {r.H2:7.4f} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:8.4f} "
            f"{r.J_FULL:8.2f} {r.J_OOS:8.2f} {str(bool(r.pass4a)):>4} {str(bool(r.pass4b)):>4}")
    say()

    # ---- ARM C: every interior cell against its OWN w=1 corner at the same G and cost
    say("=" * 108)
    say("ARM C — EVERY CELL AGAINST ITS OWN w = 1 CORNER (the realised-gross-matched twin).")
    say("        A POSITIVE dSharpe here is PURE REALLOCATION: total target gross is identical.")
    say("=" * 108); say()
    tw = []
    for (g, c), blk in GD.groupby(["G", "cost"]):
        anc = blk[blk.w == 1.0].iloc[0]
        for _, r in blk.iterrows():
            if r.w == 1.0: continue
            tw.append(dict(G=g, cost=c, w=r.w,
                           dSharpe=r.Sharpe - anc.Sharpe, dCAGR=100 * (r.CAGR - anc.CAGR),
                           dMaxDD=100 * (r.MaxDD - anc.MaxDD),
                           dOOS_Sharpe=r.OOS_Sharpe - anc.OOS_Sharpe,
                           dOOS_CAGR=100 * (r.OOS_CAGR - anc.OOS_CAGR),
                           dgross=r.mean_gross - anc.mean_gross))
    TW = pd.DataFrame(tw); TW.to_csv(str(STEM) + ".twins.csv", index=False)
    say(f"  {'cost':>5} {'n':>4} {'dSharpe>0':>10} {'mean dSh':>9} {'mean dCAGR':>11} {'mean dMaxDD':>12} "
        f"{'OOS dSh>0':>10} {'mean OOS dSh':>13} {'max |dgross|':>13}")
    for c in RUNGS:
        s = TW[TW.cost == c]
        say(f"  {c:5.0f} {len(s):4d} {int((s.dSharpe>0).sum()):>5} / {len(s):<3d} {s.dSharpe.mean():9.4f} "
            f"{s.dCAGR.mean():10.2f}pp {s.dMaxDD.mean():11.2f}pp "
            f"{int((s.dOOS_Sharpe>0).sum()):>5} / {len(s):<3d} {s.dOOS_Sharpe.mean():13.4f} "
            f"{s.dgross.abs().max():13.2e}")
    say()
    say("  Per-G breakdown at the binding rung:")
    for g in GGRID:
        s = TW[(TW.cost == BIND) & (TW.G == g)]
        say(f"    G={g:.2f}: dSharpe>0 {int((s.dSharpe>0).sum())}/{len(s)}  mean {s.dSharpe.mean():+.4f} | "
            f"dCAGR {s.dCAGR.mean():+.2f}pp | dMaxDD {s.dMaxDD.mean():+.2f}pp | "
            f"OOS dSharpe>0 {int((s.dOOS_Sharpe>0).sum())}/{len(s)} mean {s.dOOS_Sharpe.mean():+.4f}")
    say()

    # ---- ARM D: rule 8
    say("=" * 108)
    say("ARM D — RULE 8 WALK-FORWARD.  Dials chosen on IS (.. 2016-12-31) ONLY; 2017-2026 read ONCE.")
    say("=" * 108); say()
    wf = []
    for c in RUNGS:
        blk = GD[GD.cost == c]
        for nm, key in (("IS_SHARPE", "IS_Sharpe"), ("IS_J", "J_IS")):
            s = blk.sort_values([key, "G", "w"], ascending=[False, True, False]).iloc[0]
            anc = blk[(blk.G == s.G) & (blk.w == 1.0)].iloc[0]
            spyo = mt(spy[W["OOS"]])
            wf.append(dict(cost=c, chooser=nm, w=s.w, G=s.G, IS_Sharpe=s.IS_Sharpe, J_IS=s.J_IS,
                           OOS_CAGR=s.OOS_CAGR, OOS_Sharpe=s.OOS_Sharpe, OOS_MaxDD=s.OOS_MaxDD,
                           corner_OOS_CAGR=anc.OOS_CAGR, corner_OOS_Sharpe=anc.OOS_Sharpe,
                           dOOS_Sharpe=s.OOS_Sharpe - anc.OOS_Sharpe,
                           dOOS_CAGR=100 * (s.OOS_CAGR - anc.OOS_CAGR),
                           spy_OOS_Sharpe=spyo["Sharpe"], spy_OOS_CAGR=spyo["CAGR"],
                           pass4a=bool(s.pass4a), pass4b=bool(s.pass4b),
                           beats_corner_OOS=bool(s.OOS_Sharpe > anc.OOS_Sharpe and s.OOS_CAGR > anc.OOS_CAGR)))
    WF = pd.DataFrame(wf); WF.to_csv(str(STEM) + ".walkforward.csv", index=False)
    say(f"  {'cost':>5} {'chooser':>10} {'pick (w,G)':>13} {'IS Sh':>8} {'OOS CAGR':>9} {'OOS Sh':>8} "
        f"{'OOS DD':>8} {'corner OOS Sh':>14} {'dOOS Sh':>9} {'dOOS CAGR':>10} {'4a':>4} {'4b':>4} {'BEATS CORNER':>13}")
    for _, r in WF.iterrows():
        say(f"  {r.cost:5.0f} {r.chooser:>10} {f'({r.w:.1f}, {r.G:.2f})':>13} {r.IS_Sharpe:8.4f} "
            f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:8.4f} {r.OOS_MaxDD:8.2%} {r.corner_OOS_Sharpe:14.4f} "
            f"{r.dOOS_Sharpe:+9.4f} {r.dOOS_CAGR:+9.2f}pp {str(r.pass4a):>4} {str(r.pass4b):>4} "
            f"{str(r.beats_corner_OOS):>13}")
    say()

    # ---- ARM E: verdict
    say("=" * 108); say("ARM E — VERDICT."); say("=" * 108); say()
    n4a = int(b10.pass4a.sum()); n4b = int(b10.pass4b.sum())
    n4b_int = int(b10[(b10.w < 1.0) & (b10.w > 0.0)].pass4b.sum())
    s10 = TW[TW.cost == BIND]
    say(f"  4a at {BIND:.0f} bps: {n4a} of {len(b10)} cells.   4b: {n4b} of {len(b10)}   "
        f"(of which INTERIOR 0 < w < 1: {n4b_int}).")
    say(f"  Interior-vs-corner at {BIND:.0f} bps: dSharpe > 0 in {int((s10.dSharpe>0).sum())} of {len(s10)}; "
        f"OOS dSharpe > 0 in {int((s10.dOOS_Sharpe>0).sum())} of {len(s10)}.")
    say(f"  Rule-8 picks BEATING their own corner OOS on Sharpe AND CAGR: "
        f"{int(WF.beats_corner_OOS.sum())} of {len(WF)}.")
    if n4b_int == 0 and int(WF.beats_corner_OOS.sum()) == 0:
        v = "KILL"
        why = ("no interior NAV split clears 4b and no legal IS-only chooser produces a split that "
               "beats its own constant-gross U56 corner out of sample")
    elif int(WF.beats_corner_OOS.sum()) == len(WF) and n4b_int > 0:
        v = "KEEP-candidate (4b)"; why = "every chooser's split beats its own corner OOS and clears 4b"
    else:
        v = "PARK"; why = "mixed: some cells clear but no legal chooser reaches them robustly"
    say(); say(f"  VERDICT: {v} — {why}.")
    say(f"  SURVIVORSHIP (rule 9): the SMALL sleeve is a CURRENT-constituent sub-$2B screen, so its "
        f"contribution is an UPPER bound; a KILL is therefore the stronger reading.")
    say(); say(f"  [{time.time()-t0:.1f}s]")
    Path(str(STEM) + ".console.txt").write_text("\n".join(_LOG) + "\n")
    return v

if __name__ == "__main__":
    main()
