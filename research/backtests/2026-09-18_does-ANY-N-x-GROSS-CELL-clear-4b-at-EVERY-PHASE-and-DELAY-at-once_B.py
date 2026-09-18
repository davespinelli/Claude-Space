#!/usr/bin/env python3
"""
Idea 1292 (lane B, 2026-09-18) — does ANY N x GROSS CELL clear 4b at EVERY REBALANCE PHASE
AND EXECUTION DELAY AT ONCE?

THE PREMISE.  Two runs on 2026-09-17/18 perturbed the standing 2026-09-04 KEEP-4b book
(U56 / N=20 / H=126 / gross 0.75 / weekly / 10 bps) along ONE axis each and killed it the same
way.  Idea 1253 moved the REBALANCE PHASE: 4b passes at 2 of 31 phase books, the drawdown cap
failing at 29 of 31 while every Sharpe leg passes at 31 of 31.  Idea 1287 moved the EXECUTION
DELAY: 4b fails at d=2, 3 and 10, every failure binding on the MaxDD cap ALONE while all three
Sharpe legs pass at 5 of 5 lags.  Both verdicts are the same sentence: the committed -19.13%
MaxDD clears its -20.23% cap by 1.10 pp, and one weekday of slippage is worth up to 2.18 pp.

Neither run asked the question that decides whether any of this family deserves capital: is the
fragility a property of THAT CELL, or of the WHOLE (N, gross) FAMILY?  Gross is the one dial in
the frozen recipe that moves drawdown close to proportionally while leaving the Sharpe legs
roughly alone — and it is also the dial that pulls against 4b's CAGR floor, which is quoted
against a SPY that pays no turnover.  So a cell at lower gross may hold a DD margin several
times the incumbent's and still clear the floor, or may lose the floor before it buys the
margin.  This run prices that trade-off across the family, and it holds every cell to the WHOLE
stress ensemble at once rather than one axis at a time.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHOR.  (U56, N=20, gross 0.75, phase Fri, delay 1) must reproduce the committed
      incumbent (15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837).  Reported as a check, not a
      result; a failure to reproduce invalidates everything below and is said so.
  (2) THE GRID.  Every (N, gross) cell, at every point of the stress ensemble, with both KEEP
      paths (rule 4) evaluated at every point.  All 720 rows published.
  (3) ROBUST-4b.  A cell is STRESS-ROBUST iff it clears 4b at ALL 15 ensemble points.  This is
      the object the question asks about; the anchor point's own pass is reported beside it.
  (4) RULE 8.  Both dials chosen on warm-up..2016-12-31 ONLY under a chooser declared below,
      2017-2026 read ONCE, OOS CAGR / Sharpe / MaxDD reported against the live baseline and SPY.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) ROBUST CELL EXISTS AND RULE 8 REACHES IT — a stress-robust 4b book the IS chooser
        lands on.  KEEP-4b candidate, memo with exact RULES wording.
    (B) ROBUST CELL EXISTS, CHOOSER MISSES IT — PARK, documented, not promoted.
    (C) NO CELL IS STRESS-ROBUST — KILL (capital): the 4b pass is a timing artefact of the
        FAMILY, not a property of the incumbent, and nothing in this family should be funded
        on a committed number read at one phase and one lag.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  N      {10, 15, 20, 25}          (20 = the incumbent)
  GROSS  {0.45, 0.55, 0.65, 0.75}  (0.75 = the incumbent)

  16 cells per panel, 48 in all, EVERY ONE PUBLISHED at EVERY ensemble point in `.grid.csv`.

THE STRESS ENSEMBLE IS CONSTRUCTION, NOT A DIAL.  It is not chosen, not tuned, and every one
of its points is reported for every cell:

  PHASE w in {Mon, Tue, Wed, Thu, Fri} — the weekday an implementer actually decides.  Within
      each calendar week the decision row is the LAST trading row whose weekday is <= w, so
      w=Fri is exactly the incumbent's "last trading day of the week" and reproduces it.
  DELAY d in {1, 2, 3} rows — d=1 is PROTOCOL rule 2's decide-at-t / apply-at-t+1.

  5 x 3 = 15 points per cell.  The ANCHOR point is (Fri, 1).

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); the 4a and 4b legs;
full sample, both halves, and the rule-8 OOS window; the live RULES v2 baseline and SPY.

FROZEN at the incumbent's construction: H = 126 min hold, weekly cadence, 3-leg composite
(21/252, 0/126, 0/63) equal-ranked, above-200d + vol20 < 0.60 eligibility, 10 bps per unit
turnover (rule 2), 260-row warm-up, first-wins stable tie-break, equal weights within the book.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(warm-up .. 2016-12-31) only, for each cell compute at each of the 15 ensemble points the IS
Sharpe, IS MaxDD and IS CAGR, and the IS-window analogues of 4b's three non-half legs
(Sharpe > SPY, MaxDD >= 0.60 x SPY MaxDD, CAGR >= 0.70 x SPY CAGR).  Among cells clearing those
three legs at ALL 15 points, pick the one with the highest WORST-CASE IS Sharpe over the
ensemble.  If no cell clears them at all 15 points, the fallback (declared, not chosen on a
result) is the highest worst-case IS Sharpe over the whole grid, and the run says the strict
chooser was empty.  Then 2017-2026 is read once, at the anchor point and at the ensemble worst.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists and SMALL is
the current constituent list of a sub-$2B screen; delisted, acquired and bankrupt names are
absent from all three, which flatters every momentum book here.  Tickers with max_1d_move >= 1.0
in data/small_meta.csv are dropped from SMALL before anything is built.  Nothing here estimates
live expectancy; all readings are relative, across cells, on fixed panels.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell and point; rule 8
walk-forward with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_does-ANY-N-x-GROSS-CELL-clear-4b-at-EVERY-PHASE-and-DELAY-at-once_B.py
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
A_H = 126                                  # frozen min hold
NS = [10, 15, 20, 25]                      # dial 1
GROSSES = [0.45, 0.55, 0.65, 0.75]         # dial 2
PHASES = [0, 1, 2, 3, 4]                   # Mon..Fri decision weekday (construction)
DELAYS = [1, 2, 3]                         # rows between decision and application
WDNAME = ["Mon", "Tue", "Wed", "Thu", "Fri"]
ANCHOR = (4, 1)                            # Fri / t+1 = the incumbent
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")

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
        self.dec = {w: decision_rows(px.index, w) for w in PHASES}


def decision_rows(idx, w):
    """One decision row per calendar week: the LAST trading row whose weekday is <= w.
    w = 4 (Fri) is exactly `rebalance_mask(idx, 'W')`, the incumbent's convention."""
    pos = np.arange(len(idx))
    ok = idx.weekday <= w
    s = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(s.groupby(level=0).max().values)


def build(pan, N, w, d):
    """The incumbent's min-hold top-N frame at UNIT gross, deciding on phase w and applying
    d rows later.  Kept names hold for at least A_H rows from their own application row; free
    slots go to the best-ranked eligible names read at the DECISION row."""
    dec = pan.dec[w]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keepmask = app < T
    dec, app = dec[keepmask], app[keepmask]
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


def legs(r, spy, live, idx):
    h1, h2, ins, oos = windows(idx)
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[h1]), mt(r[h2])
    s1, s2 = mt(spy[h1]), mt(spy[h2])
    l1, l2 = mt(live[h1]), mt(live[h2])
    Ro, So, Ri = mt(r[oos]), mt(spy[oos]), mt(r[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_Sharpe=Ri["Sharpe"], IS_CAGR=Ri["CAGR"],
                IS_MaxDD=Ri["MaxDD"], OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"],
                OOS_MaxDD=Ro["MaxDD"], dd_margin_pp=100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"]),
                cagr_margin_pp=100.0 * (R["CAGR"] - 0.70 * S["CAGR"]),
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def is_legs(r, spy, idx):
    """The IS-window analogues of 4b's three non-half legs — the rule-8 chooser's inputs."""
    _, _, ins, _ = windows(idx)
    R, S = mt(r[ins]), mt(spy[ins])
    return dict(is_sh=R["Sharpe"], is_cagr=R["CAGR"], is_dd=R["MaxDD"],
                is_b_sh=R["Sharpe"] > S["Sharpe"], is_b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
                is_b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])


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
    say("IDEA 1292 (lane B, 2026-09-18) — does ANY N x GROSS CELL clear 4b at EVERY PHASE and")
    say("DELAY at once?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): N {NS} x GROSS {GROSSES} = 16 cells/panel, 48 published.")
    say(f"  ENSEMBLE (construction, not a dial): PHASE {WDNAME} x DELAY {DELAYS} = 15 points/cell,")
    say("  every point published. ANCHOR = (Fri, d=1) = PROTOCOL rule 2 = the incumbent.")
    say("  FROZEN: H=126, weekly, 10 bps, above-200d & vol20<0.60, equal weights, 260-row warm-up.")
    say("  ROBUST-4b := clears 4b at ALL 15 ensemble points.")
    say("  OUTCOMES: (A) ROBUST + RULE 8 REACHES IT (B) ROBUST BUT MISSED (C) NONE ROBUST.")
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
            for w in PHASES:
                for d in DELAYS:
                    W1, app = build(pan, N, w, d)
                    for g in GROSSES:
                        gr, tu = nrun(pan, W1 * g, app)
                        r = at_cost(gr, tu, REF_COST)[WARMUP:]
                        nh = (W1[WARMUP:][:, pan.iinv] > 0).sum(axis=1)
                        rec = legs(r, spy, live, idx)
                        rec.update(is_legs(r, spy, idx))
                        rec.update(panel=pan.name, N=N, gross=g, phase=WDNAME[w], delay=d,
                                   anchor=(w, d) == ANCHOR, avg_names=float(nh.mean()),
                                   turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
                        rows.append(rec)
    G = pd.DataFrame(rows)

    say("=" * 100)
    say("ARM B — THE ANCHOR CHECK: (U56, N=20, gross 0.75, Fri, d=1) against the committed")
    say("incumbent 15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837 (idea 1287)")
    say("=" * 100)
    say("")
    a = G[(G.panel == "U56") & (G.N == 20) & (G.gross == 0.75) & G.anchor].iloc[0]
    tgt = dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)
    say(f"  {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
    ok = True
    for k, v in tgt.items():
        say(f"  {k:10} {a[k]:12.4f} {v:12.4f} {a[k] - v:12.2e}")
        ok &= abs(a[k] - v) < 5e-4
    say("")
    say(f"  ANCHOR REPRODUCES: {'YES' if ok else 'NO'} (all five within 5e-4). "
        f"4b at the anchor: {'PASS' if a.pass4b else 'FAIL'}; 4a: {'PASS' if a.pass4a else 'FAIL'}.")
    if not ok:
        say("  *** The anchor does NOT reproduce. Every number below is therefore about a book")
        say("  *** that is not the committed one, and no verdict may be taken on it.")
    say("")

    # ---------------------------------------------------------- robustness
    say("=" * 100)
    say("ARM C — THE 48-CELL GRID over the 15-POINT ENSEMBLE (every point in .grid.csv)")
    say("=" * 100)
    say("")
    cells = []
    for (p, N, g), sub in G.groupby(["panel", "N", "gross"], sort=False):
        anc = sub[sub.anchor].iloc[0]
        cells.append(dict(panel=p, N=N, gross=g, n_points=len(sub),
                          pass4b_points=int(sub.pass4b.sum()), pass4a_points=int(sub.pass4a.sum()),
                          robust4b=bool(sub.pass4b.all()), robust4a=bool(sub.pass4a.all()),
                          anchor_4b=bool(anc.pass4b), anchor_4a=bool(anc.pass4a),
                          anchor_CAGR=anc.CAGR, anchor_Sharpe=anc.Sharpe, anchor_MaxDD=anc.MaxDD,
                          worst_Sharpe=sub.Sharpe.min(), worst_MaxDD=sub.MaxDD.min(),
                          worst_dd_margin_pp=sub.dd_margin_pp.min(),
                          worst_cagr_margin_pp=sub.cagr_margin_pp.min(),
                          worst_IS_Sharpe=sub.IS_Sharpe.min(),
                          spread_Sharpe=sub.Sharpe.max() - sub.Sharpe.min(),
                          spread_MaxDD_pp=100.0 * (sub.MaxDD.max() - sub.MaxDD.min()),
                          turnover_yr=float(sub.turnover_yr.mean()),
                          is_strict=bool(sub.is_b_sh.all() and sub.is_b_dd.all()
                                         and sub.is_b_cagr.all())))
    CELLS = pd.DataFrame(cells)

    for pan in panels:
        say(f"  --- {pan.name} " + "-" * 82)
        say(f"  {'N':>3} {'gross':>6} {'anchor CAGR':>11} {'anchSh':>7} {'anchDD':>8} {'anch4b':>7} "
            f"{'4b pts':>7} {'4a pts':>7} {'worstDDmar':>11} {'worstCGmar':>11} {'DDspread':>9} "
            f"{'ROBUST':>7}")
        for _, x in CELLS[CELLS.panel == pan.name].iterrows():
            say(f"  {x.N:3d} {x.gross:6.2f} {x.anchor_CAGR:11.2%} {x.anchor_Sharpe:7.4f} "
                f"{x.anchor_MaxDD:8.2%} {'Y' if x.anchor_4b else '.':>7} "
                f"{x.pass4b_points:4d}/15 {x.pass4a_points:4d}/15 {x.worst_dd_margin_pp:11.2f} "
                f"{x.worst_cagr_margin_pp:11.2f} {x.spread_MaxDD_pp:9.2f} "
                f"{'YES' if x.robust4b else '.':>7}")
        say("")

    say(f"  GRID-WIDE: 4b passes {int(G.pass4b.sum())} of {len(G)} (cell, point) rows; "
        f"4a passes {int(G.pass4a.sum())} of {len(G)}.")
    say(f"  STRESS-ROBUST cells (4b at all 15 points): {int(CELLS.robust4b.sum())} of {len(CELLS)}; "
        f"cells clearing 4b at the ANCHOR ONLY: {int((CELLS.anchor_4b & ~CELLS.robust4b).sum())}.")
    say("  4b points by panel: " + ", ".join(
        f"{p}: {int(G[G.panel == p].pass4b.sum())}/{len(G[G.panel == p])}"
        for p in ["U56", "B136", "SMALL"]) + ".")
    say("  4b points by gross: " + ", ".join(
        f"g={g}: {int(G[G.gross == g].pass4b.sum())}/{len(G[G.gross == g])}" for g in GROSSES) + ".")
    say("  4b points by N: " + ", ".join(
        f"N={n}: {int(G[G.N == n].pass4b.sum())}/{len(G[G.N == n])}" for n in NS) + ".")
    say("")

    # ---------------------------------------------------------- binding legs
    say("=" * 100)
    say("ARM D — WHICH LEG BINDS, over every FAILING (cell, point) row in the grid")
    say("=" * 100)
    say("")
    nm = dict(b_h1="H1 Sharpe", b_h2="H2 Sharpe", b_oos="OOS Sharpe", b_dd="MaxDD cap",
              b_cagr="CAGR floor")
    F = G[~G.pass4b]
    say(f"  {len(F)} failing rows of {len(G)}.")
    say(f"  {'leg':12} {'fails':>7} {'share of failures':>18} {'SOLE binder':>12}")
    for k, v in nm.items():
        f = ~F[k]
        sole = f & (F[[c for c in nm if c != k]].all(axis=1))
        say(f"  {v:12} {int(f.sum()):7d} {f.mean():18.4f} {int(sole.sum()):12d}")
    say("")
    say("  Read: a leg that is the SOLE binder on most failures is the leg the family dies on.")
    say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM E — RULE 8 WALK-FORWARD: BOTH dials chosen on warm-up..2016 ONLY, 2017-2026 ONCE")
    say("=" * 100)
    say("")
    say("  CHOOSER (declared in the header, unchanged): among cells clearing the IS analogues of")
    say("  4b's Sharpe / MaxDD / CAGR legs at ALL 15 ensemble points, the highest WORST-CASE IS")
    say("  Sharpe. Fallback if that set is empty: highest worst-case IS Sharpe over the grid.")
    say("")
    wf = []
    for pan in panels:
        sub = CELLS[CELLS.panel == pan.name]
        strict = sub[sub.is_strict]
        empty = len(strict) == 0
        pool = sub if empty else strict
        pick = pool.loc[pool.worst_IS_Sharpe.idxmax()]
        rows_pick = G[(G.panel == pan.name) & (G.N == pick.N) & (G.gross == pick.gross)]
        panc = rows_pick[rows_pick.anchor].iloc[0]
        pworst = rows_pick.loc[rows_pick.OOS_Sharpe.idxmin()]
        inc = G[(G.panel == pan.name) & (G.N == 20) & (G.gross == 0.75) & G.anchor].iloc[0]
        bspy = mt(B[pan.name]["spy"][windows(B[pan.name]["idx"])[3]])
        blive = mt(B[pan.name]["live"][windows(B[pan.name]["idx"])[3]])
        wf.append(dict(panel=pan.name, strict_set_empty=empty, pool_size=len(pool),
                       pick_N=int(pick.N), pick_gross=float(pick.gross),
                       worst_IS_Sharpe=float(pick.worst_IS_Sharpe),
                       OOS_CAGR=float(panc.OOS_CAGR), OOS_Sharpe=float(panc.OOS_Sharpe),
                       OOS_MaxDD=float(panc.OOS_MaxDD),
                       OOS_Sharpe_ens_worst=float(pworst.OOS_Sharpe),
                       OOS_CAGR_ens_worst=float(pworst.OOS_CAGR),
                       OOS_MaxDD_ens_worst=float(pworst.OOS_MaxDD),
                       ens_worst_point=f"{pworst.phase}/d{int(pworst.delay)}",
                       robust4b_pick=bool(pick.robust4b), pass4b_anchor_pick=bool(panc.pass4b),
                       inc_OOS_Sharpe=float(inc.OOS_Sharpe), inc_OOS_CAGR=float(inc.OOS_CAGR),
                       spy_OOS_Sharpe=bspy["Sharpe"], spy_OOS_CAGR=bspy["CAGR"],
                       spy_OOS_MaxDD=bspy["MaxDD"], live_OOS_Sharpe=blive["Sharpe"],
                       live_OOS_CAGR=blive["CAGR"], live_OOS_MaxDD=blive["MaxDD"]))
    WF = pd.DataFrame(wf)
    say(f"  {'panel':6} {'pick':>12} {'strict?':>8} {'wIS Sh':>7} {'OOS CAGR':>9} {'OOS Sh':>8} "
        f"{'OOS DD':>8} {'ensWorst OOS Sh':>16} {'SPY OOS Sh':>11} {'live OOS Sh':>12} {'ROB':>4}")
    for _, x in WF.iterrows():
        say(f"  {x.panel:6} {f'N={x.pick_N},g={x.pick_gross}':>12} "
            f"{'EMPTY' if x.strict_set_empty else 'ok':>8} {x.worst_IS_Sharpe:7.4f} "
            f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:8.4f} {x.OOS_MaxDD:8.2%} "
            f"{x.OOS_Sharpe_ens_worst:16.4f} {x.spy_OOS_Sharpe:11.4f} {x.live_OOS_Sharpe:12.4f} "
            f"{'YES' if x.robust4b_pick else '.':>4}")
    say("")
    say("  OOS windows in full (2017-01-01 .. end), pick vs incumbent vs live baseline vs SPY:")
    say(f"  {'panel':6} {'series':22} {'CAGR':>9} {'Sharpe':>9} {'MaxDD':>9}")
    for _, x in WF.iterrows():
        say(f"  {x.panel:6} {f'PICK N={x.pick_N} g={x.pick_gross} (anchor pt)':22} "
            f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:9.4f} {x.OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {'  same, ensemble worst':22} {x.OOS_CAGR_ens_worst:9.2%} "
            f"{x.OOS_Sharpe_ens_worst:9.4f} {x.OOS_MaxDD_ens_worst:9.2%}   "
            f"[{x.ens_worst_point}]")
        say(f"  {x.panel:6} {'  INCUMBENT N=20 g=.75':22} {x.inc_OOS_CAGR:9.2%} "
            f"{x.inc_OOS_Sharpe:9.4f}")
        say(f"  {x.panel:6} {'  RULES v2 (live)':22} {x.live_OOS_CAGR:9.2%} {x.live_OOS_Sharpe:9.4f} "
            f"{x.live_OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {'  SPY':22} {x.spy_OOS_CAGR:9.2%} {x.spy_OOS_Sharpe:9.4f} "
            f"{x.spy_OOS_MaxDD:9.2%}")
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM F — THE ANSWER")
    say("=" * 100)
    say("")
    rob = CELLS[CELLS.robust4b]
    reached = [r for _, r in WF.iterrows() if r.robust4b_pick]
    if len(rob) == 0:
        outcome = ("(C) NO CELL IS STRESS-ROBUST — no (N, gross) cell on any panel clears 4b at "
                   "all 15 ensemble points")
    elif reached:
        outcome = ("(A) ROBUST CELL EXISTS AND RULE 8 REACHES IT on " +
                   ", ".join(r.panel for r in reached))
    else:
        outcome = ("(B) ROBUST CELL(S) EXIST BUT THE RULE-8 CHOOSER MISSES THEM — " +
                   ", ".join(f"{r.panel} N={int(r.N)} g={r.gross}" for _, r in rob.iterrows()))
    say(f"  PRE-DECLARED OUTCOME REACHED: {outcome}.")
    say("")
    if len(rob):
        say(f"  {'panel':6} {'N':>3} {'gross':>6} {'anchCAGR':>9} {'anchSh':>8} {'anchDD':>8} "
            f"{'worstDDmar':>11} {'worstCGmar':>11} {'worstSh':>8}")
        for _, x in rob.iterrows():
            say(f"  {x.panel:6} {x.N:3d} {x.gross:6.2f} {x.anchor_CAGR:9.2%} "
                f"{x.anchor_Sharpe:8.4f} {x.anchor_MaxDD:8.2%} {x.worst_dd_margin_pp:11.2f} "
                f"{x.worst_cagr_margin_pp:11.2f} {x.worst_Sharpe:8.4f}")
        say("")
    inc_cell = CELLS[(CELLS.panel == "U56") & (CELLS.N == 20) & (CELLS.gross == 0.75)].iloc[0]
    say(f"  THE INCUMBENT'S OWN CELL (U56, N=20, g=0.75): 4b at {inc_cell.pass4b_points} of 15 "
        f"ensemble points, worst DD margin {inc_cell.worst_dd_margin_pp:.2f} pp, MaxDD spread "
        f"over the ensemble {inc_cell.spread_MaxDD_pp:.2f} pp.")
    say("")
    say("  SURVIVORSHIP (rule 9): all three panels are CURRENT-constituent lists; dead and")
    say("  acquired names are absent, which flatters every book here. Readings are relative,")
    say("  across cells and ensemble points on fixed panels; none is live expectancy.")

    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    CELLS.to_csv(OUT.with_suffix(".cells.csv"), index=False)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    say("")
    say(f"  Wrote .grid.csv ({len(G)}), .cells.csv ({len(CELLS)}), .walkforward.csv ({len(WF)}), "
        f".log.txt")
    say(f"  Runtime {time.time() - t0:.1f}s, offline, deterministic.")
    OUT.with_suffix(".log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
