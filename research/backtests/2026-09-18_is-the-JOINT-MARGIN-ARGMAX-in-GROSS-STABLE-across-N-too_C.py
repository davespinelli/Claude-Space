#!/usr/bin/env python3
"""
Idea 1294 (lane C, 2026-09-18) — is the JOINT-MARGIN ARGMAX in GROSS STABLE ACROSS N TOO?

THE PREMISE.  Idea 1290 froze N = 20 and solved the gross ladder for the argmax of the joint
4b margin J = min(DD margin, CAGR margin), finding g* = 0.65 on U56 and 0.60 on B136, identical
in sample and out.  Idea 1295 then certified a U56 book at that g and idea 1291 warned that H is
a third, unpriced dial in the same family.  Every one of those results was read at ONE breadth.

If g* moves with N, then gross and breadth are NOT separable dials: the record's committed
per-cell grosses (0.65, 0.60, 0.55 ...) are each conditional on the N they were solved at, and
transplanting one to another breadth is unwarranted.  If g* does not move, gross can be solved
once and reused, and 1290's number is a property of the family rather than of its cell.

This run walks the full (N x gross) surface and solves g*(N) on each window separately.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHORS.  (U56, N=20, g=0.75) must reproduce the 2026-09-04 incumbent
      (15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837) and (U56, N=20, g=0.65) must reproduce
      1290's certified book (13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833).  Reported as a
      check, not a result; a failure to reproduce invalidates everything below and is said so.
  (2) THE GRID.  Every (N, gross) cell on every panel, with BOTH KEEP paths (rule 4) and the
      three windows.  All 306 rows published in `.grid.csv`.
  (3) g*(N) PER WINDOW.  For each panel and each of IS / OOS / FULL, the gross that maximises
      J on that window, at every N.  Ties to the LOWER gross (declared, not chosen on a result).
  (4) THE SURFACE SHAPE, classified by a rule fixed here:
        RIDGE        iff max(g*) - min(g*) over the six N <= 0.05 (one rung).
        DIAGONAL     iff that spread >= 0.15 (three rungs) AND |Spearman(N, g*)| >= 0.80.
        UNSTRUCTURED otherwise.
  (5) RULE 8.  Both dials chosen on warm-up..2016-12-31 ONLY under the chooser declared below,
      2017-2026 read ONCE, against a FROZEN-N chooser and the two anchors.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) RIDGE on the IS window on every panel — gross and N separable; 1290's g* is a family
        fact and the record's per-cell grosses transfer.
    (B) DIAGONAL — not separable; every committed per-cell gross is conditional on its own N,
        and that is a standing caveat on the certified book.
    (C) UNSTRUCTURED or panel-disagreeing — the surface has no stable argmax at all and neither
        claim is supportable from one cell.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  N      {5, 10, 15, 20, 25, 30}                     (20 = the incumbent's breadth)
  GROSS  17 rungs, 0.20 .. 1.00 step 0.05            (0.65 = certified, 0.75 = 2026-09-04)

  102 cells per panel, 306 in all, EVERY ONE PUBLISHED.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); the 4a and 4b legs; full
sample, both halves, and the rule-8 OOS window; the live RULES v2 baseline and SPY.

FROZEN at the incumbent's construction: H = 126 min hold, weekly cadence (last trading row of
each calendar week), PROTOCOL rule 2's decide-at-t / apply-at-t+1, 3-leg composite (21/252,
0/126, 0/63) equal-ranked, above-200d + vol20 < 0.60 eligibility, 10 bps per unit turnover,
260-row warm-up, first-wins stable tie-break, equal weights within the book.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(warm-up .. 2016-12-31) only, per panel: among cells clearing the IS analogues of 4b's three
non-half legs (Sharpe > SPY, MaxDD >= 0.60 x SPY MaxDD, CAGR >= 0.70 x SPY CAGR), take the
highest IS joint margin J_IS = min(IS DD margin, IS CAGR margin); ties to the LOWER gross, then
to the LOWER N.  J rather than IS Sharpe because idea 1290 showed IS Sharpe cannot size a book.
If that set is empty the declared fallback is the highest J_IS over the whole grid, and the run
says the strict set was empty.  The FROZEN-N comparand runs the same chooser with N pinned at
20.  Then 2017-2026 is read ONCE.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists and SMALL is
the current constituent list of a sub-$2B screen; delisted, acquired and bankrupt names are
absent from all three, which flatters every momentum book here.  Tickers with max_1d_move >= 1.0
in data/small_meta.csv are dropped from SMALL before anything is built.  Nothing here estimates
live expectancy; all readings are relative, across cells, on fixed panels.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_is-the-JOINT-MARGIN-ARGMAX-in-GROSS-STABLE-across-N-too_C.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest  # noqa: E402

OUT = Path(__file__).with_suffix("")
WARMUP, MAXVOL, REF_COST = 260, 0.60, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H = 126                                            # frozen min hold
NS = [5, 10, 15, 20, 25, 30]                         # dial 1
GROSSES = [round(0.20 + 0.05 * i, 2) for i in range(17)]   # dial 2 — 17 rungs 0.20..1.00
DELAY = 1                                            # PROTOCOL rule 2
OOS_START = pd.Timestamp("2017-01-01")
WINDOWS = ["IS", "OOS", "FULL"]

_LOG: list[str] = []


def say(s=""):
    print(s)
    _LOG.append(s)


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


def decision_rows(idx, w=4):
    """One decision row per calendar week: the LAST trading row whose weekday is <= w.
    w = 4 (Fri) is exactly `rebalance_mask(idx, 'W')`, the incumbent's convention."""
    pos = np.arange(len(idx))
    ok = idx.weekday <= w
    s = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(s.groupby(level=0).max().values)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        self.dec = {w: decision_rows(px.index, w) for w in range(5)}


def build(pan, N, w=4, d=DELAY):
    """The incumbent's min-hold top-N frame at UNIT gross.  Kept names hold for at least A_H
    rows from their own application row; free slots go to the best-ranked eligible names read
    at the DECISION row and applied d rows later."""
    dec = pan.dec[w]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keep = app < T
    dec, app = dec[keep], app[keep]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        ks = set(int(c) for c in young)
        need = N - len(ks)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                take.append(int(c))
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app


def nrun(pan, Wt, app):
    """Gross returns and per-row turnover for a weight frame applied on rows `app`."""
    rets, Cp = pan.rets, pan.Cp
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    app = np.asarray(app, dtype=np.int64)
    ends = np.append(app[1:], T)
    for i0, i1 in zip(app, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    return (held * rets).sum(axis=1), turn


def at_cost(gr, turn, c):
    return gr - turn * c / 1e4


# ------------------------------------------------------------------ metrics
def mt(r):
    r = np.asarray(r, dtype=float)
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd)


def windows(idx):
    n = len(idx)
    h = n // 2
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS_START)
    return h1, h2, ~oos, oos


def margins(R, S):
    """4b's two one-sided margins in percentage points, on whatever window R and S are cut to."""
    dd = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"])
    cg = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    return dd, cg, min(dd, cg)


def legs(r, spy, live, idx):
    h1, h2, ins, oos = windows(idx)
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[h1]), mt(r[h2])
    s1, s2 = mt(spy[h1]), mt(spy[h2])
    l1, l2 = mt(live[h1]), mt(live[h2])
    Ro, So = mt(r[oos]), mt(spy[oos])
    Ri, Si = mt(r[ins]), mt(spy[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    f_dd, f_cg, f_J = margins(R, S)
    i_dd, i_cg, i_J = margins(Ri, Si)
    o_dd, o_cg, o_J = margins(Ro, So)
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"],
                IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"], IS_MaxDD=Ri["MaxDD"],
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                dd_margin_pp=f_dd, cagr_margin_pp=f_cg, J_FULL=f_J,
                is_dd_margin_pp=i_dd, is_cagr_margin_pp=i_cg, J_IS=i_J,
                oos_dd_margin_pp=o_dd, oos_cagr_margin_pp=o_cg, J_OOS=o_J,
                is_b_sh=Ri["Sharpe"] > Si["Sharpe"], is_b_dd=i_dd >= 0.0, is_b_cagr=i_cg >= 0.0,
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or np.ptp(y) == 0:
        return float("nan")
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return float("nan")
    return float(((rx - rx.mean()) * (ry - ry.mean())).mean() / (sx * sy))


def classify(gstars):
    """(4)'s rule, fixed in the header and not changed after reading anything."""
    spread = max(gstars) - min(gstars)
    rho = spearman(NS, gstars)
    if spread <= 0.05 + 1e-9:
        return "RIDGE", spread, rho
    if spread >= 0.15 - 1e-9 and np.isfinite(rho) and abs(rho) >= 0.80:
        return "DIAGONAL", spread, rho
    return "UNSTRUCTURED", spread, rho


# ------------------------------------------------------------------ world
def make_panels():
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    return ([Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
             Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
             Panel("SMALL", pxS, inv)], n_drop)


def bench_for(pan):
    live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")["returns"].values
    return pan.spy[WARMUP:], live[WARMUP:]


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1294 (lane C, 2026-09-18) — is the JOINT-MARGIN ARGMAX in GROSS STABLE ACROSS N TOO?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): N {NS} x GROSS {GROSSES[0]}..{GROSSES[-1]} in {len(GROSSES)} rungs")
    say(f"  = {len(NS) * len(GROSSES)} cells/panel, {len(NS) * len(GROSSES) * 3} published.")
    say("  FROZEN: H=126, weekly, t+1, 10 bps, above-200d & vol20<0.60, equal weights, 260-row warm-up.")
    say("  J = min(DD margin, CAGR margin) in pp, solved SEPARATELY on IS / OOS / FULL.")
    say("  SHAPE RULE (fixed here): RIDGE if spread(g*) <= 0.05; DIAGONAL if spread >= 0.15 and")
    say("  |Spearman(N, g*)| >= 0.80; else UNSTRUCTURED. Ties in the argmax go to the LOWER gross.")
    say("  OUTCOMES: (A) RIDGE everywhere (B) DIAGONAL (C) UNSTRUCTURED / panels disagree.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY benchmark only.")
    say("")

    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up, 10 bps, weekly for the live book)")
    say("=" * 100)
    say("")
    B = {}
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8}")
    for pan in panels:
        spy, live = bench_for(pan)
        idx = pan.idx[WARMUP:]
        B[pan.name] = dict(spy=spy, live=live, idx=idx)
        h1, h2, ins, oos = windows(idx)
        for tag, ser in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(ser), mt(ser[oos])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(ser[h1])['Sharpe']:7.4f} {mt(ser[h2])['Sharpe']:7.4f} {mo['CAGR']:9.2%} "
                f"{mo['Sharpe']:8.4f}")
    say("")

    # ---------------------------------------------------------- the grid
    rows = []
    for pan in panels:
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        for N in NS:
            W1, app = build(pan, N)
            nh = float((W1[WARMUP:][:, pan.iinv] > 0).sum(axis=1).mean())
            for g in GROSSES:
                gr, tu = nrun(pan, W1 * g, app)
                r = at_cost(gr, tu, REF_COST)[WARMUP:]
                rec = legs(r, spy, live, idx)
                rec.update(panel=pan.name, N=N, gross=g, avg_names=nh,
                           turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
                rows.append(rec)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------- anchors
    say("=" * 100)
    say("ARM B — THE ANCHOR CHECK: two committed U56 books at N=20")
    say("=" * 100)
    say("")
    anchors = [("2026-09-04 incumbent  g=0.75", 0.75,
                dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)),
               ("1290 certified       g=0.65", 0.65,
                dict(CAGR=0.1366, Sharpe=1.1526, MaxDD=-0.1673, OOS_CAGR=0.1495, OOS_Sharpe=1.1833))]
    allok = True
    for tag, g, tgt in anchors:
        a = G[(G.panel == "U56") & (G.N == 20) & (G.gross == g)].iloc[0]
        say(f"  {tag}")
        say(f"    {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
        ok = True
        for k, v in tgt.items():
            say(f"    {k:10} {a[k]:12.4f} {v:12.4f} {a[k] - v:12.2e}")
            ok &= abs(a[k] - v) < 5e-4
        say(f"    REPRODUCES: {'YES' if ok else 'NO'} (all five within 5e-4). "
            f"4b {'PASS' if a.pass4b else 'FAIL'}; 4a {'PASS' if a.pass4a else 'FAIL'}; "
            f"J_FULL {a.J_FULL:+.2f} pp, J_IS {a.J_IS:+.2f} pp.")
        say("")
        allok &= ok
    if not allok:
        say("  *** An anchor does NOT reproduce. Every number below is therefore about a book")
        say("  *** that is not the committed one, and no verdict may be taken on it.")
        say("")

    # ---------------------------------------------------------- the surface
    say("=" * 100)
    say("ARM C — THE J SURFACE (J_IS in pp; every one of the 306 cells is in .grid.csv)")
    say("=" * 100)
    say("")
    for pan in panels:
        sub = G[G.panel == pan.name]
        say(f"  --- {pan.name}: J_IS (pp) by N (rows) x gross (cols); '*' = row argmax "
            f"{'-' * 12}")
        say("   N  " + " ".join(f"{g:>6.2f}" for g in GROSSES))
        for N in NS:
            s = sub[sub.N == N].set_index("gross")["J_IS"]
            gstar = float(s.idxmax())
            say(f"  {N:3d}  " + " ".join(
                f"{s[g]:6.2f}" + ("*" if abs(g - gstar) < 1e-9 else " ") for g in GROSSES))
        say("")

    shape_rows = []
    for pan in panels:
        sub = G[G.panel == pan.name]
        for wtag, col in (("IS", "J_IS"), ("OOS", "J_OOS"), ("FULL", "J_FULL")):
            gs, Js = [], []
            for N in NS:
                s = sub[sub.N == N].set_index("gross")[col]
                gs.append(float(s.idxmax()))
                Js.append(float(s.max()))
            shape, spread, rho = classify(gs)
            shape_rows.append(dict(panel=pan.name, window=wtag, shape=shape, spread=spread,
                                   rho=rho, **{f"gstar_N{n}": v for n, v in zip(NS, gs)},
                                   **{f"J_N{n}": v for n, v in zip(NS, Js)}))
    SH = pd.DataFrame(shape_rows)
    SH.to_csv(f"{OUT}.shape.csv", index=False)

    say("=" * 100)
    say("ARM D — g*(N) PER WINDOW AND THE SHAPE VERDICT")
    say("=" * 100)
    say("")
    say(f"  {'panel':6} {'window':6} " + " ".join(f"{'N=' + str(n):>7}" for n in NS) +
        f" {'spread':>7} {'rho':>7}  shape")
    for _, x in SH.iterrows():
        say(f"  {x.panel:6} {x.window:6} " +
            " ".join(f"{x['gstar_N' + str(n)]:7.2f}" for n in NS) +
            f" {x.spread:7.2f} {x.rho:7.3f}  {x['shape']}")
    say("")
    say("  Best J at that g* (pp), same layout:")
    for _, x in SH.iterrows():
        say(f"  {x.panel:6} {x.window:6} " + " ".join(f"{x['J_N' + str(n)]:7.2f}" for n in NS))
    say("")

    # -------------------------------------------- the cost of transplanting a gross
    say("=" * 100)
    say("ARM E — WHAT A TRANSPLANTED GROSS COSTS: J_IS at the certified g=0.65 and at g*(20),")
    say("against J_IS at each N's OWN argmax")
    say("=" * 100)
    say("")
    tr = []
    for pan in panels:
        sub = G[G.panel == pan.name]
        g20 = float(sub[sub.N == 20].set_index("gross")["J_IS"].idxmax())
        for N in NS:
            s = sub[sub.N == N].set_index("gross")["J_IS"]
            own = float(s.max()); gown = float(s.idxmax())
            tr.append(dict(panel=pan.name, N=N, g_own=gown, J_own=own,
                           g_frozen20=g20, J_at_g20=float(s[g20]),
                           cost_g20_pp=float(s[g20]) - own,
                           J_at_065=float(s[0.65]), cost_065_pp=float(s[0.65]) - own,
                           rungs_from_065=int(round((gown - 0.65) / 0.05))))
    TR = pd.DataFrame(tr)
    TR.to_csv(f"{OUT}.transplant.csv", index=False)
    say(f"  {'panel':6} {'N':>3} {'g*(N)':>6} {'J own':>7} {'g*(20)':>7} {'J@g*(20)':>9} "
        f"{'cost':>7} {'J@0.65':>8} {'cost':>7} {'rungs from 0.65':>16}")
    for _, x in TR.iterrows():
        say(f"  {x.panel:6} {x.N:3d} {x.g_own:6.2f} {x.J_own:7.2f} {x.g_frozen20:7.2f} "
            f"{x.J_at_g20:9.2f} {x.cost_g20_pp:7.2f} {x.J_at_065:8.2f} {x.cost_065_pp:7.2f} "
            f"{x.rungs_from_065:16d}")
    say("")
    say(f"  Mean cost of freezing gross at g*(20): {TR.cost_g20_pp.mean():+.2f} pp of J_IS; "
        f"worst {TR.cost_g20_pp.min():+.2f} pp.")
    say(f"  Mean cost of freezing gross at the certified 0.65: {TR.cost_065_pp.mean():+.2f} pp; "
        f"worst {TR.cost_065_pp.min():+.2f} pp.")
    say("")

    # ---------------------------------------------------------- 4b / 4a census
    say("=" * 100)
    say("ARM F — BOTH KEEP PATHS AT EVERY CELL, AND WHICH LEG BINDS")
    say("=" * 100)
    say("")
    say(f"  4b passes {int(G.pass4b.sum())} of {len(G)} cells; 4a passes {int(G.pass4a.sum())}.")
    say("  by panel: " + ", ".join(
        f"{p} {int(G[G.panel == p].pass4b.sum())}/{len(G[G.panel == p])}"
        for p in ["U56", "B136", "SMALL"]) + " (4b); " + ", ".join(
        f"{p} {int(G[G.panel == p].pass4a.sum())}/{len(G[G.panel == p])}"
        for p in ["U56", "B136", "SMALL"]) + " (4a).")
    say("  4b by N: " + ", ".join(
        f"N={n} {int(G[G.N == n].pass4b.sum())}/{len(G[G.N == n])}" for n in NS) + ".")
    say("")
    say("  Per panel, the 4b-passing gross BAND at each N (contiguity is not assumed):")
    band = []
    for pan in panels:
        sub = G[G.panel == pan.name]
        for N in NS:
            ok = sorted(sub[(sub.N == N) & sub.pass4b].gross.tolist())
            band.append(dict(panel=pan.name, N=N, n_pass=len(ok),
                             lo=ok[0] if ok else np.nan, hi=ok[-1] if ok else np.nan,
                             contiguous=bool(ok) and len(ok) == int(round((ok[-1] - ok[0]) / 0.05)) + 1))
            say(f"  {pan.name:6} N={N:<3d} {len(ok):2d} rungs  " +
                (f"[{ok[0]:.2f} .. {ok[-1]:.2f}]" + ("" if band[-1]['contiguous'] else "  NOT CONTIGUOUS")
                 if ok else "none"))
    pd.DataFrame(band).to_csv(f"{OUT}.bands.csv", index=False)
    say("")
    nm = dict(b_h1="H1 Sharpe", b_h2="H2 Sharpe", b_oos="OOS Sharpe", b_dd="MaxDD cap",
              b_cagr="CAGR floor")
    F = G[~G.pass4b]
    say(f"  {len(F)} failing cells of {len(G)}.")
    say(f"  {'leg':12} {'fails':>7} {'share':>8} {'SOLE binder':>12}")
    for k, v in nm.items():
        f = ~F[k]
        sole = f & (F[[c for c in nm if c != k]].all(axis=1))
        say(f"  {v:12} {int(f.sum()):7d} {f.mean():8.4f} {int(sole.sum()):12d}")
    say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM G — RULE 8 WALK-FORWARD: dials chosen on warm-up..2016 ONLY, 2017-2026 read ONCE")
    say("=" * 100)
    say("")
    say("  CHOOSER (declared in the header, unchanged): among cells clearing the IS analogues of")
    say("  4b's Sharpe / MaxDD / CAGR legs, highest J_IS; ties to the LOWER gross then LOWER N.")
    say("  FROZEN-N comparand: the same chooser with N pinned at 20.")
    say("")

    def choose(sub):
        strict = sub[sub.is_b_sh & sub.is_b_dd & sub.is_b_cagr]
        empty = len(strict) == 0
        pool = sub if empty else strict
        pool = pool.sort_values(["J_IS", "gross", "N"], ascending=[False, True, True])
        return pool.iloc[0], empty, len(pool)

    wf = []
    for pan in panels:
        sub = G[G.panel == pan.name]
        pick, empty, npool = choose(sub)
        fpick, fempty, _ = choose(sub[sub.N == 20])
        idx = B[pan.name]["idx"]
        oos = windows(idx)[3]
        bspy, blive = mt(B[pan.name]["spy"][oos]), mt(B[pan.name]["live"][oos])
        cert = sub[(sub.N == 20) & (sub.gross == 0.65)].iloc[0]
        inc = sub[(sub.N == 20) & (sub.gross == 0.75)].iloc[0]
        # the OOS-optimal cell, read AFTER the pick, reported as regret only
        best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf.append(dict(panel=pan.name, strict_empty=empty, pool=npool,
                       pick_N=int(pick.N), pick_gross=float(pick.gross), pick_J_IS=float(pick.J_IS),
                       pick_OOS_CAGR=float(pick.OOS_CAGR), pick_OOS_Sharpe=float(pick.OOS_Sharpe),
                       pick_OOS_MaxDD=float(pick.OOS_MaxDD), pick_pass4b=bool(pick.pass4b),
                       pick_pass4a=bool(pick.pass4a),
                       pick_CAGR=float(pick.CAGR), pick_Sharpe=float(pick.Sharpe),
                       pick_MaxDD=float(pick.MaxDD), pick_H1=float(pick.H1), pick_H2=float(pick.H2),
                       froz_gross=float(fpick.gross), froz_OOS_Sharpe=float(fpick.OOS_Sharpe),
                       froz_OOS_CAGR=float(fpick.OOS_CAGR), froz_OOS_MaxDD=float(fpick.OOS_MaxDD),
                       froz_pass4b=bool(fpick.pass4b),
                       cert_OOS_Sharpe=float(cert.OOS_Sharpe), cert_OOS_CAGR=float(cert.OOS_CAGR),
                       inc_OOS_Sharpe=float(inc.OOS_Sharpe), inc_OOS_CAGR=float(inc.OOS_CAGR),
                       bestoos_N=int(best_oos.N), bestoos_gross=float(best_oos.gross),
                       bestoos_OOS_Sharpe=float(best_oos.OOS_Sharpe),
                       spy_OOS_CAGR=bspy["CAGR"], spy_OOS_Sharpe=bspy["Sharpe"],
                       spy_OOS_MaxDD=bspy["MaxDD"], live_OOS_CAGR=blive["CAGR"],
                       live_OOS_Sharpe=blive["Sharpe"], live_OOS_MaxDD=blive["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    say(f"  {'panel':6} {'FLOAT pick':>13} {'strict?':>8} {'J_IS':>7} {'OOS CAGR':>9} {'OOS Sh':>8} "
        f"{'OOS DD':>8} {'4b':>4} | {'FROZEN N=20 g':>14} {'OOS Sh':>8} {'4b':>4}")
    for _, x in WF.iterrows():
        say(f"  {x.panel:6} {f'N={x.pick_N},g={x.pick_gross}':>13} "
            f"{'EMPTY' if x.strict_empty else 'ok':>8} {x.pick_J_IS:7.2f} {x.pick_OOS_CAGR:9.2%} "
            f"{x.pick_OOS_Sharpe:8.4f} {x.pick_OOS_MaxDD:8.2%} "
            f"{'Y' if x.pick_pass4b else '.':>4} | {x.froz_gross:14.2f} {x.froz_OOS_Sharpe:8.4f} "
            f"{'Y' if x.froz_pass4b else '.':>4}")
    say("")
    say("  OOS windows in full (2017-01-01 .. end):")
    say(f"  {'panel':6} {'series':28} {'CAGR':>9} {'Sharpe':>9} {'MaxDD':>9}")
    for _, x in WF.iterrows():
        say(f"  {x.panel:6} {f'FLOAT pick N={x.pick_N} g={x.pick_gross}':28} {x.pick_OOS_CAGR:9.2%} "
            f"{x.pick_OOS_Sharpe:9.4f} {x.pick_OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {f'FROZEN N=20 g={x.froz_gross}':28} {x.froz_OOS_CAGR:9.2%} "
            f"{x.froz_OOS_Sharpe:9.4f} {x.froz_OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {'CERTIFIED N=20 g=0.65':28} {x.cert_OOS_CAGR:9.2%} "
            f"{x.cert_OOS_Sharpe:9.4f}")
        say(f"  {x.panel:6} {'INCUMBENT N=20 g=0.75':28} {x.inc_OOS_CAGR:9.2%} "
            f"{x.inc_OOS_Sharpe:9.4f}")
        say(f"  {x.panel:6} {'RULES v2 (live)':28} {x.live_OOS_CAGR:9.2%} {x.live_OOS_Sharpe:9.4f} "
            f"{x.live_OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {'SPY':28} {x.spy_OOS_CAGR:9.2%} {x.spy_OOS_Sharpe:9.4f} "
            f"{x.spy_OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {'(regret) best OOS cell':28} {'':9} {x.bestoos_OOS_Sharpe:9.4f}  "
            f"N={x.bestoos_N} g={x.bestoos_gross}")
    say("")
    say("  FULL-sample rows for the FLOAT picks (halves in the leaderboard row):")
    say(f"  {'panel':6} {'pick':>13} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'4b':>4} {'4a':>4}")
    for _, x in WF.iterrows():
        say(f"  {x.panel:6} {f'N={x.pick_N},g={x.pick_gross}':>13} {x.pick_CAGR:8.2%} "
            f"{x.pick_Sharpe:8.4f} {x.pick_MaxDD:8.2%} {x.pick_H1:7.4f} {x.pick_H2:7.4f} "
            f"{'Y' if x.pick_pass4b else '.':>4} {'Y' if x.pick_pass4a else '.':>4}")
    say("")

    # -------------------------------------------- does IS g* predict OOS g*
    say("=" * 100)
    say("ARM H — DOES THE IS ARGMAX PREDICT THE OOS ARGMAX?")
    say("=" * 100)
    say("")
    say(f"  {'panel':6} {'N':>3} {'g*_IS':>6} {'g*_OOS':>7} {'rungs apart':>12}")
    dist = []
    for pan in panels:
        for N in NS:
            i = SH[(SH.panel == pan.name) & (SH.window == "IS")].iloc[0][f"gstar_N{N}"]
            o = SH[(SH.panel == pan.name) & (SH.window == "OOS")].iloc[0][f"gstar_N{N}"]
            d = int(round((o - i) / 0.05))
            dist.append(d)
            say(f"  {pan.name:6} {N:3d} {i:6.2f} {o:7.2f} {d:12d}")
    say("")
    say(f"  Mean signed rung distance IS -> OOS: {np.mean(dist):+.2f}; "
        f"mean |distance| {np.mean(np.abs(dist)):.2f}; exact hits {sum(d == 0 for d in dist)} "
        f"of {len(dist)}.")
    say("")


    # ---------------------------------------------------------- post-hoc stress arm
    say("=" * 100)
    say("ARM J — ADDED AFTER THE MAIN GRID WAS READ, AND LABELLED AS SUCH: the rule-8 picks")
    say("through IDEA 1292's 15-POINT PHASE x DELAY ENSEMBLE")
    say("=" * 100)
    say("")
    say("  NOT pre-registered in this header. It is added because the FLOAT pick clears 4b at the")
    say("  anchor point, and the record's standing bar for a 4b candidate (ideas 1253 / 1287 /")
    say("  1292 / 1295) is 4b at ALL 15 points of the phase x delay ensemble, not at one point.")
    say("  The ROBUST rule is 1292's, inherited verbatim and NOT re-tuned here: 5 decision")
    say("  weekdays x delays {1,2,3}; ROBUST-4b := clears 4b at all 15. Comparands are declared")
    say("  by role (this run's FLOAT pick, its FROZEN-N=20 pick, and the 1290/1295 certified")
    say("  N=20 g=0.65 book), not chosen on a result.")
    say("")
    ens = []
    for _, x in WF.iterrows():
        pan = [p for p in panels if p.name == x.panel][0]
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        cand = [("FLOAT pick", int(x.pick_N), float(x.pick_gross)),
                ("FROZEN N=20", 20, float(x.froz_gross)),
                ("CERTIFIED N=20 g=0.65", 20, 0.65)]
        seen = set()
        for tag, N, g in cand:
            if (N, g) in seen:
                tag = tag + " (= same cell)"
            seen.add((N, g))
            pts = []
            for w in range(5):
                for d in (1, 2, 3):
                    W1, app = build(pan, N, w, d)
                    gr, tu = nrun(pan, W1 * g, app)
                    r = at_cost(gr, tu, REF_COST)[WARMUP:]
                    rec = legs(r, spy, live, idx)
                    rec.update(panel=pan.name, role=tag, N=N, gross=g,
                               phase=["Mon", "Tue", "Wed", "Thu", "Fri"][w], delay=d,
                               anchor=(w == 4 and d == 1))
                    pts.append(rec)
            P = pd.DataFrame(pts)
            ens.append(dict(panel=pan.name, role=tag, N=N, gross=g,
                            pass4b_points=int(P.pass4b.sum()), robust4b=bool(P.pass4b.all()),
                            worst_dd_margin_pp=float(P.dd_margin_pp.min()),
                            worst_cagr_margin_pp=float(P.cagr_margin_pp.min()),
                            worst_J=float(P[["dd_margin_pp", "cagr_margin_pp"]].min(axis=1).min()),
                            worst_OOS_Sharpe=float(P.OOS_Sharpe.min()),
                            spread_MaxDD_pp=float(100.0 * (P.MaxDD.max() - P.MaxDD.min())),
                            anchor_Sharpe=float(P[P.anchor].iloc[0].Sharpe)))
    ENS = pd.DataFrame(ens)
    ENS.to_csv(f"{OUT}.ensemble.csv", index=False)
    say(f"  {'panel':6} {'role':24} {'cell':>13} {'4b pts':>7} {'worstDDmar':>11} "
        f"{'worstCGmar':>11} {'worst OOS Sh':>13} {'DD spread':>10} {'ROBUST':>7}")
    for _, y in ENS.iterrows():
        say(f"  {y.panel:6} {y.role:24} {f'N={y.N},g={y.gross}':>13} {y.pass4b_points:4d}/15 "
            f"{y.worst_dd_margin_pp:11.2f} {y.worst_cagr_margin_pp:11.2f} "
            f"{y.worst_OOS_Sharpe:13.4f} {y.spread_MaxDD_pp:10.2f} "
            f"{'YES' if y.robust4b else '.':>7}")
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM I — THE ANSWER")
    say("=" * 100)
    say("")
    is_shapes = SH[SH.window == "IS"]["shape"].tolist()
    oos_shapes = SH[SH.window == "OOS"]["shape"].tolist()
    if all(s == "RIDGE" for s in is_shapes):
        outcome = ("(A) RIDGE on the IS window on every panel — gross and N are SEPARABLE and "
                   "1290's g* is a family fact, not a cell fact")
    elif all(s == "DIAGONAL" for s in is_shapes):
        outcome = ("(B) DIAGONAL on every panel — gross and N are NOT separable; every committed "
                   "per-cell gross is conditional on its own N")
    else:
        outcome = ("(C) MIXED / UNSTRUCTURED — IS shapes " + " / ".join(
            f"{p}:{s}" for p, s in zip(SH[SH.window == 'IS'].panel, is_shapes)))
    say(f"  OUTCOME {outcome}.")
    say(f"  OOS shapes: " + " / ".join(
        f"{p}:{s}" for p, s in zip(SH[SH.window == 'OOS'].panel, oos_shapes)) + ".")
    say("")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT constituents; delisted and")
    say("  bankrupt names are absent from all three, which flatters every momentum book here.")
    say("  No RULES change is proposed by this run (rule 6).")
    say("")
    say("  ARM J (post-hoc, labelled): stress-robust cells among the picks and comparands: "
        + ", ".join(f"{y.panel}/{y.role}: {y.pass4b_points}/15"
                    for _, y in ENS.iterrows() if y.panel != "SMALL") + ".")
    say("")
    say(f"  Runtime {time.time() - t0:.1f}s. Files: .grid.csv (306 cells), .shape.csv, "
        f".transplant.csv, .bands.csv, .walkforward.csv, .ensemble.csv, .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
