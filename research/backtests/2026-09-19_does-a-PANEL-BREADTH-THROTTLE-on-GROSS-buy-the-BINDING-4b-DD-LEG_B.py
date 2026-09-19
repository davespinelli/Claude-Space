#!/usr/bin/env python3
"""
Idea 1413 (lane B, 2026-09-19) — does a PANEL-BREADTH THROTTLE on GROSS buy the BINDING 4b DD LEG,
measured against its OWN EXPOSURE-MATCHED FLAT CUT?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly,
10 bps, next-row) passes 4b on one leg's margin: MaxDD -19.13% against a cap of -20.23%, +1.10 pp.
Eight consecutive runs (1253 phase, 1254 years, 1255 names, 1256 gate length, 1257 signal legs,
1369 cluster cap, 1377 rank hysteresis, 1395 entry throttle) have found the SAME thing: every other
4b leg passes everywhere and the DRAWDOWN leg is the only one that ever binds.  Idea 1399 then
localised it: the incumbent de-grosses on only 34 of ~921 rebalance rows — the SHORT-FILL rows where
fewer than N names are eligible — and those rows carry 8.47% of the book's cumulative log-return and
32.5% of the worst drawdown's decline.

THE QUESTION THIS RUN ASKS.  Short fill is a breadth signal read at its very last moment: the pool
must fall below TWENTY names before the book holds any cash at all.  PANEL BREADTH — the share of
the whole investable panel that is above its 200d average with vol20 < 0.60 — collapses long before
the top-20 pool does, and nobody has priced de-grossing on it.  So: scale the incumbent's gross by
a power of breadth and ask whether TIMING the de-gross buys the binding leg.

WHY THE CONTROL IS THE WHOLE EXPERIMENT.  Idea 1189 established the degeneracy this run must beat:
Sharpe is essentially FLAT in gross (U56 N=20 weekly reads 1.14080 / 1.14089 / 1.14099 at g =
0.60 / 0.70 / 0.75), so ANY de-grossing slides one book along a fixed-Sharpe CAGR-versus-drawdown
line and can "buy" the DD leg while buying nothing at all.  A throttle that merely holds less equity
on average is that same slide wearing a signal's clothes.  So EVERY throttled cell here is judged
against a FLAT-GROSS book matched to the throttle's OWN realised mean target exposure, on the same
weight frame, same tape, same cost.  The reported quantity is THROTTLE minus MATCHED FLAT.  If that
difference is zero, breadth timing is worth nothing and the pass/fail flags are decoration.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  p   {0.0, 0.5, 1.0, 1.5, 2.0, 3.0}      throttle exponent; p = 0 IS the frozen incumbent
  b0  {0.30, 0.40, 0.50, 0.60, 0.70}      reference breadth below which the throttle starts biting

  Target gross on the segment applied from decision row s:  A_G * min(1, (b_s / b0) ** p),
  b_s = share of the PRICED, INVESTABLE names at row s that are eligible (above 200d & vol20 < 0.60).
  30 cells per panel, 90 in all, EVERY ONE PUBLISHED in .grid.csv, each with its own matched flat
  control (90 more books) and its own paired bootstrap.

  PANEL {U56, B136, SMALL} is a REPLICATION CONTROL, not a third dial: all three are built and
  published whole, nothing is selected on panel, and the verdict is taken on U56, the panel the
  incumbent lives on.

NOT DIALS, reported at every cell: both KEEP paths and all five 4b legs, full sample, both halves,
the rule-8 OOS window, turnover, realised mean exposure, the live RULES v2 baseline and SPY.

FROZEN at the incumbent's construction, not tuned here: N = 20, H = 126, base gross A_G = 0.75,
weekly decision rows (last trading row with weekday <= 4 in each calendar week), next-row
application, 3-leg composite (21/252, 0/126, 0/63) equal-ranked, above-200d & vol20 < 0.60, 260-row
warm-up, first-wins stable tie-break, equal weights within the book, 10 bps (PROTOCOL rule 2).

NO LOOK-AHEAD, STATED MECHANICALLY.  Breadth is read at the DECISION row s and the resulting gross
is applied from row s+1 onward, exactly like the weights themselves.  The de-gross trade is charged:
turnover is |w_new - w_carried| on the application row, so shrinking the book costs what shrinking
the book costs.

RESOLUTION.  Every difference here is between two books on ONE tape, so it is read against a PAIRED
CIRCULAR-BLOCK BOOTSTRAP (400 replicates, 63-row blocks, seed 20260919): the compared books are
resampled on IDENTICAL blocks, so the Sharpe difference keeps its pairing and its SE is the SE of
the difference.  A gap inside 2 SE of zero is NOT an effect, however the pass/fail flags read.

RULE 8, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  Per panel, (p, b0) is chosen on
warm-up..2016-12-31 ONLY by highest IS net Sharpe, ties to the LOWEST p (do nothing), then to the
LOWEST b0; 2017-2026 is then read ONCE.  A second, DD-aware chooser (highest IS Calmar) is run as a
declared control because the question is about drawdown and an IS-Sharpe chooser is known from 1189
to be blind to it.  The comparand is the frozen incumbent (p = 0) on the same panel.

PRE-DECLARED OUTCOMES, fixed here before any number is read.  Applied to U56, in this order;
whichever fires first is the report.
  (A) ANCHOR-FAILS   — the p = 0 cells do not reproduce the frozen incumbent, or disagree with each
                       other across b0.  Everything downstream is void.
  (B) THROTTLE-BUYS  — some cell has a SHALLOWER MaxDD than the incumbent, passes 4b, beats its OWN
                       exposure-matched flat control on full-sample Sharpe by more than 2 SE, AND a
                       declared rule-8 chooser reaches a cell with OOS Sharpe >= the incumbent's.
                       A real, reachable fix for the binding leg.
  (C) DEGENERATE     — the throttle's MaxDD and Sharpe are reproduced by its own exposure-matched
                       flat cut within 2 SE at the MAJORITY of biting cells.  Breadth timing is the
                       gross dial in costume; KILL for capital.
  (D) HARMFUL        — the throttle deepens MaxDD or loses the 4b pass at every biting cell.
  (E) HINDSIGHT-ONLY — a cell beats its matched control beyond 2 SE but no declared chooser reaches
                       it.  The fix exists on paper and not to an operator.
  (F) MIXED          — none of the above fires cleanly; the run says so and classifies nothing.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen, less tickers with max_1d_move >= 1.0 in
data/small_meta.csv.  Delisted, acquired and bankrupt names are absent from all three, which
flatters every momentum book here and makes breadth itself optimistic (a name that went to zero is
not in the denominator).  No absolute level below is an estimate of live expectancy, and every 4b
pass count is an UPPER bound.  The throttle-minus-control difference is between two books on the
same panel and is first-order immune.

PROTOCOL: rule 2 execution and next-row application, 10 bps; rule 4 both KEEP paths at every cell;
rule 8 walk-forward with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_does-a-PANEL-BREADTH-THROTTLE-on-GROSS-buy-the-BINDING-4b-DD-LEG_B.py
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
WARMUP, MAXVOL, COST = 260, 0.60, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75                        # the frozen 2026-09-04 book
PS = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]                  # dial 1
B0S = [0.30, 0.40, 0.50, 0.60, 0.70]                 # dial 2
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
BOOT_B, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919

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
        self.dec = decision_rows(px.index)
        pr = self.priced[:, self.iinv]
        ok = self.elig & pr
        n_pr = pr.sum(axis=1).astype(float)
        # BREADTH, read at each row from that row's own closes only.
        self.breadth = np.where(n_pr > 0, ok.sum(axis=1) / np.maximum(n_pr, 1.0), np.nan)
        self.n_elig = ok.sum(axis=1)


def build(pan, N):
    """The incumbent's min-hold top-N frame at UNIT gross, rule-2 application (decide on the
    weekly close, apply on the next row).  Kept names hold for at least A_H rows from their own
    application row; free slots go to the best-ranked eligible names at the decision row.
    Returns the frame, the application rows, and the DECISION row that produced each segment."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = pan.dec + 1
    dec = pan.dec
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
    return W, app, dec


def seg_mult(pan, dec, app, p, b0):
    """The throttle multiplier for each segment, read at that segment's own DECISION row.
    p = 0 returns all ones, i.e. exactly the frozen incumbent."""
    if p == 0.0:
        return np.ones(len(dec))
    b = pan.breadth[dec]
    b = np.where(np.isfinite(b), b, 1.0)
    return np.minimum(1.0, (b / b0) ** p)


def expand(mult, app, T):
    """Segment multipliers -> a per-row step function on the application grid."""
    out = np.ones(T)
    ends = np.append(app[1:], T)
    for m, i0, i1 in zip(mult, app, ends):
        out[i0:i1] = m
    return out


def nrun(pan, Wt, app):
    """GROSS returns (no cost) and per-row turnover for a weight frame applied on rows `app`.
    Cash earns nothing (the record's rf = 0 convention)."""
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
    return (held * rets).sum(axis=1), turn, held.sum(axis=1)


def at_cost(gr, turn, c=COST):
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
    """4b's two one-sided margins in percentage points (>= 0 passes)."""
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
    Ri = mt(r[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    f_dd, f_cg, f_J = margins(R, S)
    o_dd, o_cg, o_J = margins(Ro, So)
    isc = Ri["CAGR"] / abs(Ri["MaxDD"]) if Ri["MaxDD"] < 0 else np.nan
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"],
                IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"], IS_MaxDD=Ri["MaxDD"], IS_Calmar=isc,
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                dd_margin_pp=f_dd, cagr_margin_pp=f_cg, J_FULL=f_J,
                oos_dd_margin_pp=o_dd, oos_cagr_margin_pp=o_cg, J_OOS=o_J,
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def block_index(n, B, block, rng):
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(B, nb))
    off = np.arange(block)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(B, nb * block)[:, :n]
    return idx % n


def sharpe_mat(R, idx):
    X = R[idx]
    m = X.mean(axis=1)
    s = X.std(axis=1, ddof=1)
    return np.where(s > 0, m * np.sqrt(252) / s, np.nan)


def maxdd_mat(R, idx):
    X = R[idx]
    eq = np.cumprod(1.0 + X, axis=1)
    return (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)


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


def bench(pan):
    res = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=0.0, freq="W")
    lg, lt = res["returns"].values, res["turnover"].values
    spy_t = np.zeros(len(pan.spy)); spy_t[WARMUP] = 1.0
    return dict(live=at_cost(lg, lt)[WARMUP:], spy=at_cost(pan.spy, spy_t)[WARMUP:],
                idx=pan.idx[WARMUP:])


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1413 (lane B, 2026-09-19) — does a PANEL-BREADTH THROTTLE on GROSS buy the BINDING")
    say("4b DD LEG, against its OWN EXPOSURE-MATCHED FLAT CUT?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): p {PS} x b0 {B0S} = {len(PS) * len(B0S)} cells per panel,")
    say(f"  {len(PS) * len(B0S) * 3} in all, EVERY ONE PUBLISHED in .grid.csv, each with its own")
    say("  EXPOSURE-MATCHED FLAT-GROSS control and its own paired bootstrap.")
    say(f"  FROZEN: N={A_N}, H={A_H}, base gross={A_G}, weekly, rule-2 next-row application,")
    say(f"  above-200d & vol20<{MAXVOL}, 3-leg composite, {WARMUP}-row warm-up, {int(COST)} bps.")
    say("  PANEL {U56,B136,SMALL} is a REPLICATION CONTROL, not a third dial. VERDICT ON U56.")
    say(f"  RESOLUTION: paired circular-block bootstrap, {BOOT_B} reps x {BOOT_BLOCK}-row blocks,")
    say(f"  seed {BOOT_SEED}; compared books resampled on IDENTICAL blocks.")
    say("  OUTCOMES in order: (A) ANCHOR-FAILS (B) THROTTLE-BUYS (C) DEGENERATE (D) HARMFUL")
    say("  (E) HINDSIGHT-ONLY (F) MIXED.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY benchmark only.")
    for pan in panels:
        say(f"  TAPE {pan.name}: {pan.idx[0].date()} .. {pan.idx[-1].date()} ({len(pan.idx)} rows), "
            f"{len(pan.dec)} weekly decision rows.")
    say("")

    # ------------------------------------------------------- ARM A: what breadth actually does
    say("=" * 100)
    say("ARM A — THE SIGNAL ITSELF: does panel breadth move before the top-20 pool does?")
    say("=" * 100)
    say("")
    say("  The whole idea rests on one factual claim: breadth collapses EARLIER and MORE OFTEN than")
    say("  short fill.  If it does not, the throttle is short fill with extra steps.  Measured on")
    say("  the weekly DECISION rows, post-warm-up:")
    say("")
    say(f"  {'panel':6} {'dec rows':>9} {'mean b':>8} {'p05 b':>8} {'min b':>8} "
        f"{'rows b<0.5':>11} {'rows b<0.3':>11} {'short-fill':>11}")
    BR = {}
    for pan in panels:
        d = pan.dec[pan.dec >= WARMUP]
        b = pan.breadth[d]
        sf = int((pan.n_elig[d] < A_N).sum())
        BR[pan.name] = dict(dec=d, b=b, sf=sf)
        say(f"  {pan.name:6} {len(d):9d} {np.nanmean(b):8.3f} {np.nanpercentile(b, 5):8.3f} "
            f"{np.nanmin(b):8.3f} {int((b < 0.5).sum()):11d} {int((b < 0.3).sum()):11d} {sf:11d}")
    say("")
    for pan in panels:
        d, b = BR[pan.name]["dec"], BR[pan.name]["b"]
        yrs = pd.DatetimeIndex(pan.idx[d]).year
        low = pd.Series(b < 0.3, index=yrs).groupby(level=0).sum()
        low = low[low > 0]
        say(f"  {pan.name:6} decision rows with breadth < 0.30 by year: "
            + (", ".join(f"{y}:{int(c)}" for y, c in low.items()) if len(low) else "none"))
    say("")

    # ------------------------------------------------------- ARM B: the grid
    say("=" * 100)
    say(f"ARM B — THE GRID: {len(PS) * len(B0S) * 3} throttled books + {len(PS) * len(B0S) * 3} "
        "exposure-matched flat controls, every one published")
    say("=" * 100)
    say("")
    rows, S_THR, S_FLT = [], {}, {}
    for pan in panels:
        bb = bench(pan)
        idx = bb["idx"]
        W1, app, dec = build(pan, A_N)
        T = len(pan.idx)
        for p in PS:
            for b0 in B0S:
                m = seg_mult(pan, dec, app, p, b0)
                mrow = expand(m, app, T)
                gr, tu, held = nrun(pan, W1 * A_G * mrow[:, None], app)
                r = at_cost(gr, tu)[WARMUP:]
                # matched flat cut: the throttle's OWN mean TARGET gross, post-warm-up
                tgt_gross = A_G * mrow * (W1.sum(axis=1) > 0)
                g_flat = float(tgt_gross[WARMUP:].mean())
                gf, tf, heldf = nrun(pan, W1 * g_flat, app)
                rf = at_cost(gf, tf)[WARMUP:]
                rec = legs(r, bb["spy"], bb["live"], idx)
                cf = legs(rf, bb["spy"], bb["live"], idx)
                bite = int((m < 1.0 - 1e-12).sum())
                rec.update(panel=pan.name, p=p, b0=b0, kind="THROTTLE",
                           mean_target_gross=g_flat, matched_flat_gross=g_flat,
                           bite_rows=bite, bite_share=bite / max(len(m), 1),
                           mean_held_gross=float(held[WARMUP:].mean()),
                           turnover_yr=float(tu[WARMUP:].sum() / (len(idx) / 252.0)))
                cf.update(panel=pan.name, p=p, b0=b0, kind="FLAT_MATCHED",
                          mean_target_gross=g_flat, matched_flat_gross=g_flat,
                          bite_rows=0, bite_share=0.0,
                          mean_held_gross=float(heldf[WARMUP:].mean()),
                          turnover_yr=float(tf[WARMUP:].sum() / (len(idx) / 252.0)))
                rows += [rec, cf]
                S_THR[(pan.name, p, b0)] = r
                S_FLT[(pan.name, p, b0)] = rf
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"  Wrote {OUT.name}.grid.csv — {len(G)} rows "
        f"({int((G.kind == 'THROTTLE').sum())} throttled, {int((G.kind == 'FLAT_MATCHED').sum())} controls).")
    say("")

    # ------------------------------------------------------- ARM C: the anchor gate
    say("=" * 100)
    say("ARM C — GATES")
    say("=" * 100)
    say("")
    TH = G[G.kind == "THROTTLE"]
    a0 = TH[(TH.panel == "U56") & (TH.p == 0.0)]
    spread = float(max(a0.Sharpe.max() - a0.Sharpe.min(), a0.MaxDD.max() - a0.MaxDD.min(),
                       a0.CAGR.max() - a0.CAGR.min()))
    say(f"  G1  p = 0 is b0-INVARIANT on U56 (it must be: the multiplier is identically 1).")
    say(f"      worst spread over the {len(a0)} b0 cells = {spread:.3e}  -> "
        f"{'PASS' if spread < 1e-12 else 'FAIL'}")
    anc = a0.iloc[0]
    tgt = dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)
    say("  G2  the p = 0 cell IS the frozen 2026-09-04 incumbent:")
    say(f"      {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
    worst = 0.0
    for k, v in tgt.items():
        say(f"      {k:10} {anc[k]:12.4f} {v:12.4f} {anc[k] - v:12.2e}")
        worst = max(worst, abs(anc[k] - v))
    say(f"      worst |diff| {worst:.2e} -> EXACT (<5e-4): {'YES' if worst < 5e-4 else 'NO'}; "
        f"within tape-vintage floor (<5e-3): {'YES' if worst < 5e-3 else 'NO'}")
    f0 = G[(G.kind == "FLAT_MATCHED") & (G.panel == "U56") & (G.p == 0.0)].iloc[0]
    d0 = max(abs(f0.Sharpe - anc.Sharpe), abs(f0.MaxDD - anc.MaxDD), abs(f0.CAGR - anc.CAGR))
    say(f"  G3  at p = 0 the matched flat control IS the throttled book (g_flat must equal the")
    say(f"      mean target gross, which is A_G on held rows): worst |diff| {d0:.3e} -> "
        f"{'PASS' if d0 < 1e-9 else 'CHECK'} (flat gross {f0.matched_flat_gross:.4f})")
    say(f"  G4  no look-ahead: breadth is read at decision row s, applied from s+1. Rows read by")
    say(f"      the chooser are all < {IS_END.date()} (checked in ARM F).")
    mono = []
    for pan in panels:
        for b0 in B0S:
            s = TH[(TH.panel == pan.name) & (TH.b0 == b0)].sort_values("p")
            mono.append(bool(np.all(np.diff(s.mean_target_gross.values) <= 1e-12)))
    say(f"  G5  mean target gross is NON-INCREASING in p at {sum(mono)} of {len(mono)} (panel, b0) "
        f"ladders -> {'PASS' if all(mono) else 'FAIL'}")
    say(f"  G6  exactly two tuned parameters (p, b0); panel, N, H, gross, cadence, cost all frozen "
        "or reported at every value and never chosen on.")
    say("")

    # ------------------------------------------------------- ARM D: U56 in full
    say("=" * 100)
    say("ARM D — U56, THE PANEL THE INCUMBENT LIVES ON: every cell, throttle vs its matched flat")
    say("=" * 100)
    say("")
    for b0 in B0S:
        say(f"  b0 = {b0:.2f}")
        say(f"    {'p':>4} {'bite%':>6} {'gross':>6} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>7} "
            f"{'ddMrg':>6} {'OOS Sh':>7} {'4b':>3} | {'F CAGR':>7} {'F Sharpe':>8} {'F MaxDD':>7} "
            f"{'F ddMrg':>7} {'F 4b':>4} | {'dSh':>7} {'dDD pp':>7}")
        for p in PS:
            t = TH[(TH.panel == "U56") & (TH.p == p) & (TH.b0 == b0)].iloc[0]
            f = G[(G.kind == "FLAT_MATCHED") & (G.panel == "U56") & (G.p == p) & (G.b0 == b0)].iloc[0]
            say(f"    {p:4.1f} {t.bite_share:6.1%} {t.mean_target_gross:6.3f} | {t.CAGR:7.2%} "
                f"{t.Sharpe:7.4f} {t.MaxDD:7.2%} {t.dd_margin_pp:6.2f} {t.OOS_Sharpe:7.4f} "
                f"{'Y' if t.pass4b else '.':>3} | {f.CAGR:7.2%} {f.Sharpe:8.4f} {f.MaxDD:7.2%} "
                f"{f.dd_margin_pp:7.2f} {'Y' if f.pass4b else '.':>4} | "
                f"{t.Sharpe - f.Sharpe:7.4f} {100 * (t.MaxDD - f.MaxDD):7.2f}")
        say("")
    say("  4b PASS MAPS (rows p, cols b0).  T = throttle passes, F = matched flat passes.")
    for pan in panels:
        for kind, tag in (("THROTTLE", "T"), ("FLAT_MATCHED", "F")):
            say(f"    {pan.name:6} {tag}  " + "p/b0 " + " ".join(f"{b:>5.2f}" for b in B0S))
            for p in PS:
                cells = []
                for b0 in B0S:
                    x = G[(G.kind == kind) & (G.panel == pan.name) & (G.p == p) & (G.b0 == b0)].iloc[0]
                    cells.append("    Y" if x.pass4b else "    .")
                say(f"    {'':6} {'':2} {p:5.1f} " + " ".join(cells))
        say("")
    say("  4a PASS COUNTS (vs the live RULES v2 book): "
        + ", ".join(f"{pan.name} {int(G[(G.panel == pan.name)].pass4a.sum())} of "
                    f"{int((G.panel == pan.name).sum())}" for pan in panels))
    say("")
    say("  PER-LEG 4b FAILURE COUNTS over all 90 THROTTLED books:")
    for leg in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"):
        say(f"    {leg:8} fails {int((~TH[leg]).sum()):3d} of {len(TH)}   "
            + "  ".join(f"{pan.name}:{int((~TH[TH.panel == pan.name][leg]).sum())}" for pan in panels))
    say("")

    # ------------------------------------------------------- ARM E: the control test
    say("=" * 100)
    say("ARM E — THE CONTROL TEST: is the throttle ANYTHING its own exposure-matched flat cut is not?")
    say("=" * 100)
    say("")
    say("  Paired circular-block bootstrap on THROTTLE minus MATCHED FLAT, identical blocks.")
    say("  A cell whose |dSharpe| or |dMaxDD| sits inside 2 SE of zero is NOT an effect.")
    say("")
    rng = np.random.default_rng(BOOT_SEED)
    bidx = {}
    res_rows = []
    for pan in panels:
        n = len(S_THR[(pan.name, 0.0, B0S[0])])
        bidx[pan.name] = block_index(n, BOOT_B, BOOT_BLOCK, rng)
    for pan in panels:
        I = bidx[pan.name]
        for p in PS:
            for b0 in B0S:
                a = S_THR[(pan.name, p, b0)]
                b = S_FLT[(pan.name, p, b0)]
                ds = sharpe_mat(a, I) - sharpe_mat(b, I)
                dd = maxdd_mat(a, I) - maxdd_mat(b, I)
                res_rows.append(dict(panel=pan.name, p=p, b0=b0,
                                     dSharpe=float(mt(a)["Sharpe"] - mt(b)["Sharpe"]),
                                     dSharpe_se=float(np.nanstd(ds, ddof=1)),
                                     dMaxDD_pp=float(100 * (mt(a)["MaxDD"] - mt(b)["MaxDD"])),
                                     dMaxDD_se_pp=float(100 * np.nanstd(dd, ddof=1)),
                                     dCAGR_pp=float(100 * (mt(a)["CAGR"] - mt(b)["CAGR"]))))
    R = pd.DataFrame(res_rows)
    R["t_Sharpe"] = R.dSharpe / R.dSharpe_se.replace(0, np.nan)
    R["t_MaxDD"] = R.dMaxDD_pp / R.dMaxDD_se_pp.replace(0, np.nan)
    R.to_csv(f"{OUT}.control.csv", index=False)
    say(f"  Wrote {OUT.name}.control.csv — {len(R)} paired comparisons.")
    say("")
    say(f"  {'panel':6} {'p':>4} {'b0':>5} {'bite%':>6} {'dSharpe':>8} {'SE':>7} {'t':>7} "
        f"{'dMaxDD pp':>10} {'SE':>7} {'t':>7} {'dCAGR pp':>9}")
    for pan in panels:
        for p in PS:
            if p == 0.0:
                continue
            for b0 in B0S:
                x = R[(R.panel == pan.name) & (R.p == p) & (R.b0 == b0)].iloc[0]
                t = TH[(TH.panel == pan.name) & (TH.p == p) & (TH.b0 == b0)].iloc[0]
                if t.bite_share == 0:
                    continue
                say(f"  {pan.name:6} {p:4.1f} {b0:5.2f} {t.bite_share:6.1%} {x.dSharpe:8.4f} "
                    f"{x.dSharpe_se:7.4f} {x.t_Sharpe:7.2f} {x.dMaxDD_pp:10.3f} "
                    f"{x.dMaxDD_se_pp:7.3f} {x.t_MaxDD:7.2f} {x.dCAGR_pp:9.3f}")
    say("")
    bit = R.merge(TH[["panel", "p", "b0", "bite_share"]], on=["panel", "p", "b0"])
    bit = bit[bit.bite_share > 0]
    for pan in panels:
        s = bit[bit.panel == pan.name]
        ins_s = int((s.t_Sharpe.abs() < 2).sum())
        ins_d = int((s.t_MaxDD.abs() < 2).sum())
        say(f"  {pan.name:6}: of {len(s)} BITING cells, dSharpe inside 2 SE at {ins_s}, "
            f"dMaxDD inside 2 SE at {ins_d}; mean dSharpe {s.dSharpe.mean():+.4f}, "
            f"mean dMaxDD {s.dMaxDD_pp.mean():+.3f} pp, mean dCAGR {s.dCAGR_pp.mean():+.3f} pp")
    say("")

    # ------------------------------------------------------- ARM F: rule 8
    say("=" * 100)
    say("ARM F — RULE 8 WALK-FORWARD: parameters chosen on 2009-2016 ONLY, 2017-2026 read ONCE")
    say("=" * 100)
    say("")
    wf = []
    for pan in panels:
        idx = pan.idx[WARMUP:]
        assert idx[windows(idx)[2]].max() <= IS_END, "G4 violated: IS window leaks past 2016"
        sub = TH[TH.panel == pan.name]
        inc = sub[sub.p == 0.0].iloc[0]
        for tag, key in (("CH_ISSHARPE", "IS_Sharpe"), ("CH_ISCALMAR", "IS_Calmar")):
            s = sub.sort_values([key, "p", "b0"], ascending=[False, True, True]).iloc[0]
            wf.append(dict(panel=pan.name, chooser=tag, p=s.p, b0=s.b0,
                           IS_Sharpe=s.IS_Sharpe, IS_Calmar=s.IS_Calmar,
                           OOS_CAGR=s.OOS_CAGR, OOS_Sharpe=s.OOS_Sharpe, OOS_MaxDD=s.OOS_MaxDD,
                           inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_MaxDD=inc.OOS_MaxDD,
                           d_OOS_Sharpe=s.OOS_Sharpe - inc.OOS_Sharpe,
                           d_OOS_MaxDD_pp=100 * (s.OOS_MaxDD - inc.OOS_MaxDD),
                           moved=bool(s.p != 0.0), pass4b=bool(s.pass4b), pass4a=bool(s.pass4a)))
        wf.append(dict(panel=pan.name, chooser="R_DONOTHING", p=0.0, b0=B0S[0],
                       IS_Sharpe=inc.IS_Sharpe, IS_Calmar=inc.IS_Calmar,
                       OOS_CAGR=inc.OOS_CAGR, OOS_Sharpe=inc.OOS_Sharpe, OOS_MaxDD=inc.OOS_MaxDD,
                       inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_MaxDD=inc.OOS_MaxDD,
                       d_OOS_Sharpe=0.0, d_OOS_MaxDD_pp=0.0, moved=False,
                       pass4b=bool(inc.pass4b), pass4a=bool(inc.pass4a)))
        # ex-post best OOS, reported NOT claimed
        bo = sub.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        wf.append(dict(panel=pan.name, chooser="EXPOST_BEST_OOS(reported,not claimed)",
                       p=bo.p, b0=bo.b0, IS_Sharpe=bo.IS_Sharpe, IS_Calmar=bo.IS_Calmar,
                       OOS_CAGR=bo.OOS_CAGR, OOS_Sharpe=bo.OOS_Sharpe, OOS_MaxDD=bo.OOS_MaxDD,
                       inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_MaxDD=inc.OOS_MaxDD,
                       d_OOS_Sharpe=bo.OOS_Sharpe - inc.OOS_Sharpe,
                       d_OOS_MaxDD_pp=100 * (bo.OOS_MaxDD - inc.OOS_MaxDD),
                       moved=bool(bo.p != 0.0), pass4b=bool(bo.pass4b), pass4a=bool(bo.pass4a)))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {'panel':6} {'chooser':40} {'p':>4} {'b0':>5} {'OOS CAGR':>9} {'OOS Sh':>8} "
        f"{'OOS MaxDD':>10} {'dOOS Sh':>8} {'dOOS DD pp':>11} {'4b':>3}")
    for _, x in WF.iterrows():
        say(f"  {x.panel:6} {x.chooser:40} {x.p:4.1f} {x.b0:5.2f} {x.OOS_CAGR:9.2%} "
            f"{x.OOS_Sharpe:8.4f} {x.OOS_MaxDD:10.2%} {x.d_OOS_Sharpe:8.4f} "
            f"{x.d_OOS_MaxDD_pp:11.2f} {'Y' if x.pass4b else '.':>3}")
    say("")
    say("  BENCHMARKS on the same windows:")
    for pan in panels:
        bb = bench(pan)
        h1, h2, ins, oos = windows(bb["idx"])
        for tag, r in (("SPY", bb["spy"]), ("RULES v2 (live)", bb["live"])):
            m, mo = mt(r), mt(r[oos])
            say(f"    {pan.name:6} {tag:16} full {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / "
                f"{m['MaxDD']:7.2%}   halves {mt(r[h1])['Sharpe']:.4f} / {mt(r[h2])['Sharpe']:.4f}"
                f"   OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:7.2%}")
    say("")

    # ------------------------------------------------------- ARM G: verdict
    say("=" * 100)
    say("ARM G — THE PRE-DECLARED OUTCOME")
    say("=" * 100)
    say("")
    u = TH[TH.panel == "U56"]
    ub = bit[bit.panel == "U56"]
    inc = u[u.p == 0.0].iloc[0]
    shallower = u[(u.p > 0) & (u.MaxDD > inc.MaxDD)]
    beats = ub[(ub.dSharpe > 0) & (ub.t_Sharpe > 2)]
    wfu = WF[(WF.panel == "U56") & (WF.chooser.isin(["CH_ISSHARPE", "CH_ISCALMAR"]))]
    reach = wfu[(wfu.moved) & (wfu.d_OOS_Sharpe >= 0)]
    anchor_ok = spread < 1e-12 and worst < 5e-3
    say(f"  incumbent (p=0) U56: {inc.CAGR:.2%} / {inc.Sharpe:.4f} / {inc.MaxDD:.2%}, "
        f"4b DD margin {inc.dd_margin_pp:+.2f} pp, 4b {'PASS' if inc.pass4b else 'FAIL'}")
    say(f"  (A) anchor reproduces .................. {'no -> (A) FIRES' if not anchor_ok else 'yes'}")
    say(f"  (B) cells with SHALLOWER MaxDD than incumbent ... {len(shallower)} of {int((u.p > 0).sum())}")
    say(f"      of those, passing 4b ......................... "
        f"{int(shallower.pass4b.sum()) if len(shallower) else 0}")
    say(f"      cells beating their matched flat on Sharpe by >2 SE ... {len(beats)} of {len(ub)}")
    say(f"      declared choosers that MOVE and do not lose OOS Sharpe ... {len(reach)} of 2")
    say(f"  (C) biting U56 cells inside 2 SE of their matched flat: "
        f"Sharpe {int((ub.t_Sharpe.abs() < 2).sum())} of {len(ub)}, "
        f"MaxDD {int((ub.t_MaxDD.abs() < 2).sum())} of {len(ub)}")
    say(f"  (D) biting U56 cells with DEEPER MaxDD than incumbent: "
        f"{int(((u.p > 0) & (u.bite_share > 0) & (u.MaxDD < inc.MaxDD)).sum())} of "
        f"{int(((u.p > 0) & (u.bite_share > 0)).sum())}")
    say("")

    fired = None
    if not anchor_ok:
        fired = "(A) ANCHOR-FAILS"
    elif len(shallower) and shallower.pass4b.any() and len(beats) and len(reach):
        fired = "(B) THROTTLE-BUYS"
    elif len(ub) and (ub.t_Sharpe.abs() < 2).sum() > len(ub) / 2 and \
            (ub.t_MaxDD.abs() < 2).sum() > len(ub) / 2:
        fired = "(C) DEGENERATE"
    elif len(ub) and not len(shallower):
        fired = "(D) HARMFUL"
    elif len(beats) and not len(reach):
        fired = "(E) HINDSIGHT-ONLY"
    else:
        fired = "(F) MIXED"
    say(f"  OUTCOME FIRED: {fired}")
    say("")
    say(f"  SURVIVORSHIP (rule 9): U56/B136 are CURRENT constituents; SMALL is the current sub-$2B")
    say(f"  screen less {n_drop} tickers with max_1d_move >= 1.0.  Names that delisted, were acquired")
    say("  or went to zero are absent from every panel, which flatters the books AND the breadth")
    say("  series itself (a name that collapsed is not in breadth's denominator), so the throttle is")
    say("  measured on an OPTIMISTIC signal.  Every 4b pass count is an UPPER bound; the")
    say("  throttle-minus-matched-flat difference is between two books on one panel and is")
    say("  first-order immune.")
    say("")
    say(f"  ran in {time.time() - t0:.1f}s")
    Path(f"{OUT}.out.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nWrote {OUT.name}.out.txt / .grid.csv / .control.csv / .walkforward.csv")
    return fired


if __name__ == "__main__":
    main()
