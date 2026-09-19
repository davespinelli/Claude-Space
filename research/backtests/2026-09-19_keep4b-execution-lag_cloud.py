#!/usr/bin/env python3
"""Idea 1635 (lane cloud, 2026-09-19) — does the 2026-09-04 KEEP-4b TOP-20 BOOK survive a
1-DAY-DELAYED EXECUTION at 25 and 50 bps?

WHY THIS IDEA.  The standing KEEP-4b candidate (top-20 equal weight, NO vol scaler, 126-row min
hold, weekly) has only ever been priced at 10 bps with the engine's t+1 convention.  A real book
run from a NIGHTLY scan does not fill at tomorrow's close: the scan runs after the close of t, the
order is worked on t+1 at best and, with any human or broker step in between, later.  The
candidate's 4b drawdown margin is **1.10 pp** and idea 1511 measured the paired circular-block SE
of a MaxDD contrast at **2.93 pp**.  If the margin is thinner than one further day of slippage,
the candidate is not a capital claim -- it is a backtest convention.

TWO DIALS AND NO MORE (PROTOCOL rule 4):
  L  {1, 2, 3, 5} trading days from the Friday DECISION row to the APPLICATION row
                  (L = 1 is the engine's t+1 convention and the published anchor)
  c  {0, 10, 25, 50} bps per unit turnover (10 = PROTOCOL rule 2's binding rung)

  L AND c ARE ADVERSARIAL AXES, NOT DIALS A MANAGER OWNS.  Nobody chooses their own fill lag or
  their own spread.  Consequently NO chooser is run over L or c: the pre-registered reading is the
  FRONTIER -- for each panel and each cost rung, the LARGEST L at which every 4b leg still passes,
  and, for each failing cell, WHICH leg fails FIRST.  An IS-only chooser over L is reported at the
  end and LABELLED ILLEGITIMATE, exactly so the record cannot later quote it as a result.

PANEL  {U56, B136, SMALL} is a REPLICATION axis, reported per panel, never pooled, never tuned over.
GROSS  {0.75, 0.65} are BOTH FROZEN COMPARANDS, not a dial: 0.75 is idea 1635's own statement of
       the candidate and the live value; 0.65 is the gross the record later certified (idea 1293).
       Both are published at every cell; neither is chosen by anything.
  => 3 panels x 4 L x 4 c x 2 gross = 96 cells, EVERY ONE PUBLISHED.

FROZEN at the 2026-09-04 book's construction: N = 20, H = 126-row min hold, weekly cadence
deciding on the last trading row of the week (Fri phase), above-200d AND vol20 < 0.60 eligibility,
the 3-leg composite (21/252, 0/126, 0/63) equal-ranked and halved below the 200d average, NO vol
scaler, equal weights, 260-row warm-up, first-wins stable tie-break, cash at 0%.

GATE (printed before any hypothesis is read, and invalidating everything below if it fails).
  (U56, N = 20, g = 0.65, L = 1, c = 10) must reproduce idea 1293's certified candidate:
  FULL 13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833.

RULE 8.  The book is FROZEN, so the walk-forward question is not which dial to pick but whether
the legs that pass in-sample (warm-up .. 2016-12-31) still pass out of sample (2017-2026, read
ONCE).  Every cell publishes IS and OOS separately, and the 4b OOS legs are scored against SPY's
OWN OOS bars, never against full-sample bars.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
CURRENT constituent list of a sub-$2B screen, so its delisted, acquired and bankrupt names are
ABSENT.  Every SMALL reading is an UPPER bound.  Tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped before anything is built.

PROTOCOL: rule 2 execution and costs; rule 3 baselines (RULES v2 live AND SPY); rule 4 both KEEP
paths at every cell; rule 8 IS/OOS with 2017-2026 read once; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Deterministic, offline, committed caches only:
  python research/backtests/2026-09-19_keep4b-execution-lag_cloud.py
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
WARMUP, MAXVOL, N_FIX, A_H, A_PHASE = 260, 0.60, 20, 126, 4
LEGS = [(21, 252), (0, 126), (0, 63)]
LAGS = [1, 2, 3, 5]
RUNGS = [0.0, 10.0, 25.0, 50.0]
GROSSES = [0.75, 0.65]
BIND, L0, G0 = 10.0, 1, 0.75
IS_END, OOS0 = pd.Timestamp("2016-12-31"), pd.Timestamp("2017-01-01")
REF = dict(CAGR=0.1366, Sharpe=1.1526, MaxDD=-0.1673, OOS_CAGR=0.1495, OOS_Sharpe=1.1833)
_LOG: list[str] = []
def say(s=""):
    print(s); _LOG.append(s)

# ------------------------------------------------------------------ mechanics
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
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        self.dec = decision_rows(px.index, A_PHASE)

def build(pan, N, d):
    """2026-09-04 book at UNIT gross, decision row -> application row d trading days later."""
    T, M = pan.rets.shape; K = len(pan.iinv)
    app = pan.dec + d; keep = app < T; app, dec = app[keep], pan.dec[keep]
    W = np.zeros((T, M)); cur = np.full(K, -1, dtype=np.int64); pr = pan.priced[:, pan.iinv]
    nsel = np.zeros(T)
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
        if len(sel):
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel); nsel[t:stop] = len(sel)
    return W, app, nsel

def nrun(pan, Wt, app):
    rets, Cp = pan.rets, pan.Cp
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
    return (held * rets).sum(axis=1), turn

# ------------------------------------------------------------------ metrics
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

LEGNAMES = ["b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"]

def cell(r, spy, live, W):
    R, S, L_ = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[W["H1"]]), mt(r[W["H2"]]); s1, s2 = mt(spy[W["H1"]]), mt(spy[W["H2"]])
    l1, l2 = mt(live[W["H1"]]), mt(live[W["H2"]])
    Ri, Ro, So, Si = mt(r[W["IS"]]), mt(r[W["OOS"]]), mt(spy[W["OOS"]]), mt(spy[W["IS"]])
    a = dict(a_h1=bool(r1["Sharpe"] > l1["Sharpe"]), a_h2=bool(r2["Sharpe"] > l2["Sharpe"]),
             a_dd=bool(R["MaxDD"] >= L_["MaxDD"]))
    b = dict(b_h1=bool(r1["Sharpe"] > s1["Sharpe"]), b_h2=bool(r2["Sharpe"] > s2["Sharpe"]),
             b_oos=bool(Ro["Sharpe"] > So["Sharpe"]),
             b_dd=bool(R["MaxDD"] >= 0.60 * S["MaxDD"]),
             b_cagr=bool(R["CAGR"] >= 0.70 * S["CAGR"]))
    ddm = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"]); cgm = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    ddo = 100.0 * (Ro["MaxDD"] - 0.60 * So["MaxDD"]); cgo = 100.0 * (Ro["CAGR"] - 0.70 * So["CAGR"])
    ddi = 100.0 * (Ri["MaxDD"] - 0.60 * Si["MaxDD"]); cgi = 100.0 * (Ri["CAGR"] - 0.70 * Si["CAGR"])
    # OOS-only 4b, scored against SPY's OWN OOS bars
    o1, o2 = W["OOS"] & W["H1"], W["OOS"] & W["H2"]
    b_oos_all = bool(Ro["Sharpe"] > So["Sharpe"] and Ro["MaxDD"] >= 0.60 * So["MaxDD"]
                     and Ro["CAGR"] >= 0.70 * So["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"], H2=r2["Sharpe"],
                sh_h1_bar=s1["Sharpe"], sh_h2_bar=s2["Sharpe"],
                IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"], IS_MaxDD=Ri["MaxDD"],
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                spy_OOS_Sharpe=So["Sharpe"], dd_margin=ddm, cagr_margin=cgm,
                dd_margin_IS=ddi, cagr_margin_IS=cgi, dd_margin_OOS=ddo, cagr_margin_OOS=cgo,
                J_FULL=min(ddm, cgm), J_IS=min(ddi, cgi), J_OOS=min(ddo, cgo),
                pass4a=all(a.values()), pass4b=all(b.values()), pass4b_oosonly=b_oos_all, **a, **b)

def first_fail(row):
    f = [k for k in LEGNAMES if not row[k]]
    return ",".join(f) if f else "-"

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 116)
    say("IDEA 1635 (lane cloud, 2026-09-19) — does the 2026-09-04 KEEP-4b TOP-20 BOOK survive a")
    say("1-DAY-DELAYED EXECUTION at 25 and 50 bps?")
    say("=" * 116); say()
    say(f"  DIALS (2, rule 4): L {LAGS} trading days  x  c {RUNGS} bps.")
    say(f"  BOTH ARE ADVERSARIAL AXES, NOT DIALS A MANAGER OWNS — no chooser is run over either.")
    say(f"  PANEL {{U56, B136, SMALL}} replication axis; GROSS {GROSSES} both FROZEN comparands.")
    say(f"  => 3 x {len(LAGS)} x {len(RUNGS)} x {len(GROSSES)} = {3*len(LAGS)*len(RUNGS)*len(GROSSES)} cells, ALL published.")
    say(f"  FROZEN: N={N_FIX}, H={A_H} min hold, weekly Fri decision, above-200d & vol20<{MAXVOL}, equal weights.")
    say()

    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    invS = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, invS)]
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped, max_1d_move >= 1.0).")
    say()

    say("=" * 116); say("ARM A — BENCHMARKS (rule 3), post-warm-up, each on its own panel's trading days.")
    say("=" * 116); say()
    B = {}
    say(f"  {'panel':6} {'series':24} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8}")
    for pan in panels:
        spy, idx = pan.spy[WARMUP:], pan.idx[WARMUP:]
        W = windows(idx)
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=BIND, freq="W")["returns"].values[WARMUP:]
        B[pan.name] = dict(spy=spy, live=live, idx=idx, W=W)
        for lab, s in (("SPY (buy & hold)", spy), ("RULES v2 (live, 10bps)", live)):
            m, mo = mt(s), mt(s[W["OOS"]])
            say(f"  {pan.name:6} {lab:24} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(s[W['H1']])['Sharpe']:7.4f} {mt(s[W['H2']])['Sharpe']:7.4f} "
                f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
        ms, mso = mt(spy), mt(spy[W["OOS"]])
        say(f"  {pan.name:6} {'4b bars':24} FULL cap {0.60*ms['MaxDD']:7.2%}  floor {0.70*ms['CAGR']:6.2%}   "
            f"| OOS cap {0.60*mso['MaxDD']:7.2%}  floor {0.70*mso['CAGR']:6.2%}")
    say()

    # ---------------------------------------------------------- the grid
    rows = []
    for pan in panels:
        spy, idx, W, live = (B[pan.name][k] for k in ("spy", "idx", "W", "live"))
        for L in LAGS:
            W1, app, nsel = build(pan, N_FIX, L)
            names = float(np.mean(nsel[WARMUP:][nsel[WARMUP:] > 0])) if (nsel[WARMUP:] > 0).any() else 0.0
            for g in GROSSES:
                gr, turn = nrun(pan, W1 * g, app)
                for c in RUNGS:
                    r = (gr - turn * c / 1e4)[WARMUP:]
                    d = cell(r, spy, live, W)
                    d.update(panel=pan.name, L=L, cost=c, gross=g, names=names,
                             turns_yr=float(turn[WARMUP:].sum() / (len(r) / 252.0)))
                    rows.append(d)
    GD = pd.DataFrame(rows)
    GD["first_fail_4b"] = GD.apply(first_fail, axis=1)
    order = (["panel", "L", "gross", "cost", "names", "turns_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "sh_h1_bar", "sh_h2_bar", "IS_CAGR", "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
              "OOS_MaxDD", "spy_OOS_Sharpe", "dd_margin", "cagr_margin", "dd_margin_IS",
              "cagr_margin_IS", "dd_margin_OOS", "cagr_margin_OOS", "J_FULL", "J_IS", "J_OOS",
              "pass4a", "pass4b", "pass4b_oosonly", "first_fail_4b",
              "a_h1", "a_h2", "a_dd"] + LEGNAMES)
    GD = GD[order].sort_values(["panel", "gross", "L", "cost"]).reset_index(drop=True)
    GD.to_csv(str(STEM) + ".grid.csv", index=False)

    # ---------------------------------------------------------- GATE
    say("=" * 116); say("GATE — reproduce idea 1293's certified candidate (U56, N=20, g=0.65, L=1, c=10).")
    say("=" * 116); say()
    a = GD[(GD.panel == "U56") & (GD.gross == 0.65) & (GD.L == 1) & (GD.cost == BIND)].iloc[0]
    devs = {"CAGR": a.CAGR - REF["CAGR"], "Sharpe": a.Sharpe - REF["Sharpe"],
            "MaxDD": a.MaxDD - REF["MaxDD"], "OOS_CAGR": a.OOS_CAGR - REF["OOS_CAGR"],
            "OOS_Sharpe": a.OOS_Sharpe - REF["OOS_Sharpe"]}
    ok = max(abs(v) for v in devs.values()) < 5e-3
    for k, v in devs.items():
        say(f"    {k:12} this run { (a[k]):>10.4f}   idea 1293 {REF[k]:>10.4f}   dev {v:+.2e}")
    say(f"    GATE: {'PASS' if ok else 'FAIL'} (max |dev| {max(abs(v) for v in devs.values()):.2e}, bar 5e-03)")
    if not ok:
        say("    GATE FAILED — every comparison below is invalidated.  Stopping.")
        Path(str(STEM) + ".console.txt").write_text("\n".join(_LOG) + "\n"); return "GATE FAIL"
    say()

    # ---------------------------------------------------------- ARM B
    say("=" * 116)
    say(f"ARM B — THE FULL GRID at the ANCHOR GROSS {G0:.2f}.  (g = 0.65 and every cost rung in .grid.csv.)")
    say("=" * 116); say()
    say(f"  {'panel':6} {'L':>2} {'c':>3} {'trn/y':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'ddM':>7} {'cgM':>7} {'J_OOS':>7} {'4a':>5} {'4b':>5} {'first 4b leg to fail':>22}")
    for pan in panels:
        for L in LAGS:
            for c in RUNGS:
                r = GD[(GD.panel == pan.name) & (GD.gross == G0) & (GD.L == L) & (GD.cost == c)].iloc[0]
                say(f"  {pan.name:6} {L:2d} {c:3.0f} {r.turns_yr:6.2f} {r.CAGR:8.2%} {r.Sharpe:8.4f} "
                    f"{r.MaxDD:8.2%} {r.H1:7.4f} {r.H2:7.4f} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:8.4f} "
                    f"{r.dd_margin:7.2f} {r.cagr_margin:7.2f} {r.J_OOS:7.2f} "
                    f"{str(bool(r.pass4a)):>5} {str(bool(r.pass4b)):>5} {r.first_fail_4b:>22}")
        say()

    # ---------------------------------------------------------- ARM C — the frontier
    say("=" * 116)
    say("ARM C — THE FRONTIER.  For each (panel, gross, cost): the LARGEST L at which every 4b leg")
    say("        still passes (FULL), and the same for the OOS-only 4b reading.  '-' = fails at L = 1.")
    say("=" * 116); say()
    fr = []
    say(f"  {'panel':6} {'gross':>6} {'cost':>5} {'max L 4b FULL':>14} {'max L 4b OOS':>13} "
        f"{'ddM(L=1)':>9} {'cgM(L=1)':>9} {'d ddM per L':>12} {'d cgM per L':>12} {'binding leg':>14}")
    for pan in panels:
        for g in GROSSES:
            for c in RUNGS:
                s = GD[(GD.panel == pan.name) & (GD.gross == g) & (GD.cost == c)].sort_values("L")
                okF = [int(r.L) for _, r in s.iterrows() if r.pass4b]
                okO = [int(r.L) for _, r in s.iterrows() if r.pass4b_oosonly]
                mF = max(okF) if okF and min(okF) == 1 else ("-" if not okF else f"~{max(okF)}")
                mO = max(okO) if okO and min(okO) == 1 else ("-" if not okO else f"~{max(okO)}")
                r1 = s.iloc[0]; r5 = s.iloc[-1]
                dd_slope = (r5.dd_margin - r1.dd_margin) / (r5.L - r1.L)
                cg_slope = (r5.cagr_margin - r1.cagr_margin) / (r5.L - r1.L)
                fr.append(dict(panel=pan.name, gross=g, cost=c, maxL_4b_full=str(mF),
                               maxL_4b_oos=str(mO), ddm_L1=r1.dd_margin, cgm_L1=r1.cagr_margin,
                               dd_slope_per_L=dd_slope, cagr_slope_per_L=cg_slope,
                               binding=r1.first_fail_4b))
                say(f"  {pan.name:6} {g:6.2f} {c:5.0f} {str(mF):>14} {str(mO):>13} "
                    f"{r1.dd_margin:9.2f} {r1.cagr_margin:9.2f} {dd_slope:+12.3f} {cg_slope:+12.3f} "
                    f"{r1.first_fail_4b:>14}")
    FR = pd.DataFrame(fr); FR.to_csv(str(STEM) + ".frontier.csv", index=False)
    say()

    # ---------------------------------------------------------- ARM D — the anchor's own decay
    say("=" * 116)
    say("ARM D — THE CANDIDATE'S OWN DECAY.  U56, N = 20, at both frozen grosses, every (L, c).")
    say("        d vs the (L = 1, c = 10) anchor at the same gross.")
    say("=" * 116); say()
    dec = []
    for g in GROSSES:
        anc = GD[(GD.panel == "U56") & (GD.gross == g) & (GD.L == 1) & (GD.cost == BIND)].iloc[0]
        say(f"  gross {g:.2f}  anchor (L=1, c=10): CAGR {anc.CAGR:.2%}  Sharpe {anc.Sharpe:.4f}  "
            f"MaxDD {anc.MaxDD:.2%}  ddM {anc.dd_margin:+.2f}pp  cgM {anc.cagr_margin:+.2f}pp  "
            f"4b {bool(anc.pass4b)}")
        say(f"    {'L':>2} {'c':>3} {'dCAGR':>9} {'dSharpe':>9} {'dMaxDD':>9} {'d ddM':>8} {'d cgM':>8} "
            f"{'dOOS Sh':>9} {'4b':>5} {'4b OOS':>7}")
        for L in LAGS:
            for c in RUNGS:
                r = GD[(GD.panel == "U56") & (GD.gross == g) & (GD.L == L) & (GD.cost == c)].iloc[0]
                dec.append(dict(gross=g, L=L, cost=c, dCAGR=100*(r.CAGR-anc.CAGR),
                                dSharpe=r.Sharpe-anc.Sharpe, dMaxDD=100*(r.MaxDD-anc.MaxDD),
                                d_ddm=r.dd_margin-anc.dd_margin, d_cgm=r.cagr_margin-anc.cagr_margin,
                                dOOS_Sharpe=r.OOS_Sharpe-anc.OOS_Sharpe, pass4b=bool(r.pass4b),
                                pass4b_oos=bool(r.pass4b_oosonly)))
                d = dec[-1]
                say(f"    {L:2d} {c:3.0f} {d['dCAGR']:+8.2f}pp {d['dSharpe']:+9.4f} {d['dMaxDD']:+8.2f}pp "
                    f"{d['d_ddm']:+8.2f} {d['d_cgm']:+8.2f} {d['dOOS_Sharpe']:+9.4f} "
                    f"{str(d['pass4b']):>5} {str(d['pass4b_oos']):>7}")
        say()
    pd.DataFrame(dec).to_csv(str(STEM) + ".decay.csv", index=False)

    # ---------------------------------------------------------- ARM E — illegitimate chooser
    say("=" * 116)
    say("ARM E — AN IS-ONLY CHOOSER OVER L, REPORTED AND LABELLED **ILLEGITIMATE**.")
    say("        Nobody chooses their own fill lag; this exists so the record cannot quote it as a result.")
    say("=" * 116); say()
    wf = []
    for pan in panels:
        for g in GROSSES:
            for c in RUNGS:
                s = GD[(GD.panel == pan.name) & (GD.gross == g) & (GD.cost == c)]
                p = s.sort_values(["IS_Sharpe", "L"], ascending=[False, True]).iloc[0]
                hon = s[s.L == 1].iloc[0]
                wf.append(dict(panel=pan.name, gross=g, cost=c, IS_pick_L=int(p.L),
                               pick_OOS_Sharpe=p.OOS_Sharpe, pick_OOS_CAGR=p.OOS_CAGR,
                               L1_OOS_Sharpe=hon.OOS_Sharpe, L1_OOS_CAGR=hon.OOS_CAGR,
                               pick_pass4b=bool(p.pass4b), L1_pass4b=bool(hon.pass4b)))
    WF = pd.DataFrame(wf); WF.to_csv(str(STEM) + ".walkforward.csv", index=False)
    say(f"  IS-Sharpe chooser picks L = 1 in {int((WF.IS_pick_L==1).sum())} of {len(WF)} (panel, gross, cost) cells; "
        f"picks by L: {dict(WF.IS_pick_L.value_counts().sort_index())}")
    say(f"  Its OOS Sharpe vs the honest L = 1 reading: mean {(WF.pick_OOS_Sharpe-WF.L1_OOS_Sharpe).mean():+.4f}, "
        f"better in {int((WF.pick_OOS_Sharpe>WF.L1_OOS_Sharpe).sum())} of {len(WF)}.")
    say()

    # ---------------------------------------------------------- ARM F — verdict
    say("=" * 116); say("ARM F — VERDICT."); say("=" * 116); say()
    A = GD[(GD.panel == "U56") & (GD.gross == G0)]
    n4b = int(GD.pass4b.sum()); n4a = int(GD.pass4a.sum())
    say(f"  Over all {len(GD)} cells: 4a passes {n4a}; 4b passes {n4b}.")
    for g in GROSSES:
        u = GD[(GD.panel == "U56") & (GD.gross == g)]
        pl = sorted(set(int(x) for x in u[u.pass4b].L))
        pc = sorted(set(float(x) for x in u[u.pass4b].cost))
        say(f"  U56 g={g:.2f}: 4b passes {int(u.pass4b.sum())} of {len(u)} — at lags {pl if pl else 'none'} "
            f"and cost rungs {pc if pc else 'none'}.")
    for pan in ("B136", "SMALL"):
        u = GD[GD.panel == pan]
        say(f"  {pan}: 4b passes {int(u.pass4b.sum())} of {len(u)}.")
    a1 = GD[(GD.panel=="U56")&(GD.gross==G0)&(GD.L==1)&(GD.cost==BIND)].iloc[0]
    a2 = GD[(GD.panel=="U56")&(GD.gross==G0)&(GD.L==2)&(GD.cost==BIND)].iloc[0]
    a25 = GD[(GD.panel=="U56")&(GD.gross==G0)&(GD.L==1)&(GD.cost==25.0)].iloc[0]
    a50 = GD[(GD.panel=="U56")&(GD.gross==G0)&(GD.L==1)&(GD.cost==50.0)].iloc[0]
    say()
    say(f"  THE HEADLINE PAIR (U56, g {G0:.2f}): one further day of lag costs "
        f"{100*(a2.CAGR-a1.CAGR):+.2f} pp/yr of CAGR, {a2.Sharpe-a1.Sharpe:+.4f} of Sharpe and "
        f"{a2.dd_margin-a1.dd_margin:+.2f} pp of 4b DD margin; 4b {bool(a1.pass4b)} -> {bool(a2.pass4b)}.")
    say(f"  At L = 1, 25 bps: 4b {bool(a25.pass4b)} (ddM {a25.dd_margin:+.2f}, cgM {a25.cagr_margin:+.2f}). "
        f"At L = 1, 50 bps: 4b {bool(a50.pass4b)} (ddM {a50.dd_margin:+.2f}, cgM {a50.cagr_margin:+.2f}).")
    say()
    say("  SURVIVORSHIP (rule 9): U56/B136/SMALL are CURRENT-constituent lists; every reading, and the")
    say("  SMALL panel's above all, is an UPPER bound on what the book would have earned.")
    say(); say(f"  [{time.time()-t0:.1f}s]")
    Path(str(STEM) + ".console.txt").write_text("\n".join(_LOG) + "\n")

if __name__ == "__main__":
    main()
