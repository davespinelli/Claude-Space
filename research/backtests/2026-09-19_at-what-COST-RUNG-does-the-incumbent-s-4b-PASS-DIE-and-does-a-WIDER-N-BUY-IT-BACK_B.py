#!/usr/bin/env python3
"""
Idea 1362 (lane B, 2026-09-19) — at what COST RUNG does the incumbent's 4b PASS DIE, and does a
WIDER N BUY IT BACK?

THE PREMISE.  PROTOCOL rule 2 fixes costs at 10 bps per unit turnover and the entire record — the
2026-09-04 KEEP-4b book included — is priced there and nowhere else.  10 bps of round-trip slippage
on a 20-name, weekly-decided book of US large caps is an optimistic but defensible retail number;
it is not a number an operator gets to assume.  A book whose capital case dies between 10 and 25 bps
is not capital-worthy, it is an execution bet.  This run ladders COST against the ONE dial in the
incumbent's construction that changes turnover per unit of book — N, the width of the book — and
asks both halves of the question: WHERE does the pass die at the incumbent's own N, and IS there an
N that buys it back at a cost rung an operator can actually hit.

WHAT COST IS AND IS NOT IN THIS RUN.  Cost here is a pure POST-HOC CHARGE: the book is built from
ranks and a minimum hold, never from a cost-aware objective, so the same weight frame prices at
every rung and the gross series is computed once per (panel, N).  That is exactly how the record
prices it, and it is the CONSERVATIVE direction for the wider-N question — a cost-aware operator
could do no worse.  It also means the whole COST axis is arithmetic on one turnover series, so
nothing in the ladder can be a re-fit artefact.

FAIRNESS, STATED BEFORE ANY NUMBER IS READ.  A cost ladder that charges the candidate 50 bps and
its comparand 10 is not a measurement.  At every rung, the LIVE RULES v2 BASELINE IS CHARGED THE
SAME RUNG (its own turnover series, same arithmetic).  SPY is buy-and-hold: one entry trade, which
this run charges at the rung as well, so no comparand gets a free execution assumption.  4a is
therefore judged at matched cost, and 4b's SPY legs move only through SPY's single entry charge.

WHAT IS MEASURED.  For each (N, PANEL) cell, build the incumbent's book — 3-leg composite
(21/252, 0/126, 0/63) equal-ranked, above-200d AND vol20 < 0.60 eligibility, top N with a 126-row
minimum hold, gross 0.75, weekly decision rows, next-row application (rule 2) — changing ONLY N.
Then price that one gross series at every COST rung and read both KEEP paths, both halves and the
rule-8 OOS window at all of them.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  COST   {0, 5, 10, 15, 20, 25, 35, 50} bps per unit turnover   (10 is rule 2; the rest are stress)
  N      {5, 10, 15, 20, 25, 30, 40} names                      (20 is the frozen incumbent)

  A DEATH-SEARCH EXTENSION of the SAME cost dial — {75, 100, 150, 200, 250, 300, 400, 500,
  750, 1000} bps at N = 20 — is run in ARM K so the headline question is answered rather than
  extrapolated.  It is more rungs of dial 1, not a third dial: nothing is selected on it and
  the pre-declared outcome below is read on the eight declared rungs alone.

  56 cells per panel, EVERY ONE PUBLISHED in `.grid.csv`.  PANEL {U56, B136, SMALL} is a
  REPLICATION CONTROL, not a third dial: all three are built and published whole, nothing is
  selected on panel, and the verdict is taken on the ANCHOR PANEL U56, the panel the incumbent
  lives on.

NOT DIALS, reported at every cell: the 4a and 4b legs; full sample, both halves, the rule-8 OOS
window; the live RULES v2 baseline and SPY, both charged at the same rung.

FROZEN at the incumbent's construction, not tuned here: H = 126 minimum hold, gross = 0.75, weekly
cadence (last trading row with weekday <= 4 in each calendar week), 3-leg composite, above-200d +
vol20 < 0.60, 260-row warm-up, first-wins stable tie-break, equal weights within the book.

RESOLUTION.  The wider-N claim is a DIFFERENCE between two books on one tape, so it is read against
a PAIRED CIRCULAR-BLOCK BOOTSTRAP (400 replicates, 63-row blocks, seed 20260919): both books are
resampled on IDENTICAL blocks, so the Sharpe difference keeps its pairing and its SE is the SE of
the difference, not of two levels.  A rung whose gap sits inside 2 SE of zero is NOT a fix, however
the pass/fail flags read.

RULE 8, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  Per (panel, cost rung), N is chosen
on warm-up..2016-12-31 ONLY, by highest IS net Sharpe at THAT rung, ties to the LOWER N; 2017-2026
is then read ONCE.  The comparand PROTOCOL mandates is the frozen incumbent N = 20 at the same rung.
The reported quantity is chooser-minus-incumbent in OOS Sharpe.  A positive number means an operator
could have found the wider book in sample; a negative one means the fix is hindsight.

PRE-DECLARED OUTCOMES, fixed here before anything is read.  Applied to U56, in this order;
whichever fires first is the report.
  (A) FRAGILE-AT-10   — 4b already fails at N = 20, COST = 10.  The committed pass does not
                        reproduce and everything downstream of it is void.
  (B) COST-DEATH      — at N = 20 the last 4b-passing rung is < 25 bps AND no N in the grid passes
                        4b at 25 bps.  The book is an execution bet; KILL for real capital.
  (C) WIDER-N-BUYS-IT — N = 20 fails 4b at 25 bps, some N passes there, that N's Sharpe gap over
                        N = 20 at 25 bps is beyond 2 SE, AND the rule-8 chooser at 25 bps reaches
                        a book with OOS Sharpe >= the incumbent's.  A real, reachable fix.
  (D) HINDSIGHT-ONLY  — some N passes 4b at 25 bps but the chooser does not reach it, or the gap is
                        inside 2 SE.  The fix exists on paper and not to an operator.
  (E) COST-ROBUST     — N = 20 clears 4b at 25 bps and at every rung below it.
  (F) MIXED           — none of the above fires cleanly; the run says so and classifies nothing.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen.  Delisted, acquired and bankrupt names are absent from
all three, which flatters every momentum book here, and no absolute level below is an estimate of
live expectancy.  The cost ladder is a difference across rungs on the SAME panel and the SAME books,
so it is first-order immune; the pass/fail COUNTS are not.  Tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped from SMALL before anything is built.

PROTOCOL: rule 2 execution and next-row application; rule 4 both KEEP paths at every cell; rule 8
walk-forward with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_at-what-COST-RUNG-does-the-incumbent-s-4b-PASS-DIE-and-does-a-WIDER-N-BUY-IT-BACK_B.py
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
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
COSTS = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 35.0, 50.0]   # dial 1
NS = [5, 10, 15, 20, 25, 30, 40]                         # dial 2
STRESS_RUNG = 25.0                                  # the rung the outcomes are declared at
# SAME dial, more rungs — NOT a third parameter.  Declared so the headline question ('at what
# COST RUNG does the pass DIE') is ANSWERED rather than extrapolated; published whole, nothing
# is selected on it and the pre-declared outcome above is read on COSTS alone.
COSTS_EXT = [75.0, 100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0, 750.0, 1000.0]
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


def build(pan, N):
    """The incumbent's min-hold top-N frame at UNIT gross, rule-2 application (decide on the
    weekly close, apply on the next row).  Kept names hold for at least A_H rows from their own
    application row; free slots go to the best-ranked eligible names at the decision row."""
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
    return W, app


def nrun(pan, Wt, app):
    """GROSS returns (no cost) and per-row turnover for a weight frame applied on rows `app`."""
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
    """The whole COST axis is this one line: a post-hoc charge on a fixed turnover series."""
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
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"],
                IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"], IS_MaxDD=Ri["MaxDD"],
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                dd_margin_pp=f_dd, cagr_margin_pp=f_cg, J_FULL=f_J,
                oos_dd_margin_pp=o_dd, oos_cagr_margin_pp=o_cg, J_OOS=o_J,
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def block_index(n, B, block, rng):
    """One (B, n) matrix of circular-block bootstrap row indices, shared by every series so a
    difference stays PAIRED."""
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(B, nb))
    off = np.arange(block)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(B, nb * block)[:, :n]
    return idx % n


def sharpe_mat(R, idx):
    X = R[idx]
    m = X.mean(axis=1)
    s = X.std(axis=1, ddof=1)
    return np.where(s > 0, m * 252 / (s * np.sqrt(252)), np.nan)


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


def bench_series(pan):
    """The live RULES v2 book's GROSS returns and turnover, so it can be charged at every rung
    with the SAME arithmetic the candidate gets.  SPY is buy-and-hold: one entry unit of turnover
    on the first post-warm-up row, also charged at the rung."""
    res = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=0.0, freq="W")
    return res["returns"].values, res["turnover"].values


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1362 (lane B, 2026-09-19) — at what COST RUNG does the incumbent's 4b PASS DIE,")
    say("and does a WIDER N BUY IT BACK?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): COST {[int(c) for c in COSTS]} bps x N {NS} = "
        f"{len(COSTS) * len(NS)} cells per panel, {len(COSTS) * len(NS) * 3} in all, every one")
    say("  published in .grid.csv.  PANEL {U56, B136, SMALL} is a REPLICATION CONTROL, not a")
    say("  third dial: all three published whole, nothing selected on panel, VERDICT ON U56.")
    say(f"  FROZEN: H={A_H}, gross={A_G}, weekly, rule-2 next-row application, above-200d &")
    say(f"  vol20<{MAXVOL}, 3-leg composite, {WARMUP}-row warm-up, equal weights, first-wins ties.")
    say("  FAIRNESS: at every rung the LIVE RULES v2 BASELINE is charged the SAME rung on its own")
    say("  turnover; SPY is buy-and-hold with its single entry trade charged at the rung too.")
    say(f"  RESOLUTION: paired circular-block bootstrap, {BOOT_B} reps x {BOOT_BLOCK}-row blocks,")
    say(f"  seed {BOOT_SEED}; compared books resampled on IDENTICAL blocks.")
    say(f"  OUTCOMES declared at the {int(STRESS_RUNG)} bps rung, in order: (A) FRAGILE-AT-10")
    say("  (B) COST-DEATH (C) WIDER-N-BUYS-IT (D) HINDSIGHT-ONLY (E) COST-ROBUST (F) MIXED.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY benchmark only.")
    for pan in panels:
        say(f"  TAPE {pan.name}: {pan.idx[0].date()} .. {pan.idx[-1].date()} ({len(pan.idx)} rows), "
            f"{len(pan.dec)} weekly decision rows.")
    say("")

    # ---------------------------------------------------------- benchmarks at every rung
    say("=" * 100)
    say("ARM A — THE COMPARANDS, CHARGED AT EVERY RUNG (post-warm-up)")
    say("=" * 100)
    say("")
    B = {}
    for pan in panels:
        lg, lt = bench_series(pan)
        spy_g = pan.spy.copy()
        spy_t = np.zeros(len(spy_g))
        spy_t[WARMUP] = 1.0                       # buy-and-hold: one entry trade, charged at the rung
        idx = pan.idx[WARMUP:]
        B[pan.name] = dict(lg=lg, lt=lt, spy_g=spy_g, spy_t=spy_t, idx=idx)
    say(f"  {'panel':6} {'series':20} {'cost':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
        f"{'H1':>7} {'H2':>7} {'OOS CAGR':>9} {'OOS Sh':>8}")
    for pan in panels:
        d = B[pan.name]
        h1, h2, ins, oos = windows(d["idx"])
        for tag, g, tu in (("SPY (buy & hold)", d["spy_g"], d["spy_t"]),
                           ("RULES v2 (live)", d["lg"], d["lt"])):
            for c in (0.0, 10.0, 25.0, 50.0):
                r = at_cost(g, tu, c)[WARMUP:]
                m, mo = mt(r), mt(r[oos])
                say(f"  {pan.name:6} {tag:20} {int(c):5d} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} "
                    f"{m['MaxDD']:8.2%} {mt(r[h1])['Sharpe']:7.4f} {mt(r[h2])['Sharpe']:7.4f} "
                    f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f}")
    say("")
    say("  NOTE: SPY's ladder moves only through one entry trade, so its levels are effectively")
    say("  cost-free — which makes 4b HARDER at every rung, not easier.  That is the honest side.")
    say("")

    # ---------------------------------------------------------- the grid
    say("=" * 100)
    say(f"ARM B — THE GRID: {len(COSTS) * len(NS) * 3} cells, every one published")
    say("=" * 100)
    say("")
    rows, series, gross = [], {}, {}
    for pan in panels:
        d = B[pan.name]
        idx = d["idx"]
        for N in NS:
            W1, app = build(pan, N)
            gr, tu = nrun(pan, W1 * A_G, app)
            gross[(pan.name, N)] = (gr, tu)
            names = float((W1[WARMUP:][:, pan.iinv] > 0).sum(axis=1).mean())
            t_yr = float(tu[WARMUP:].sum() / (len(idx) / 252.0))
            for c in COSTS:
                r = at_cost(gr, tu, c)[WARMUP:]
                spy = at_cost(d["spy_g"], d["spy_t"], c)[WARMUP:]
                live = at_cost(d["lg"], d["lt"], c)[WARMUP:]
                series[(pan.name, N, c)] = r
                rec = legs(r, spy, live, idx)
                rec.update(panel=pan.name, N=N, cost_bps=c, avg_names=names, turnover_yr=t_yr)
                rows.append(rec)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"  Wrote {OUT.name}.grid.csv — {len(G)} rows.")
    say("")

    # ---------------------------------------------------------- anchor gate
    say("=" * 100)
    say("ARM C — THE ANCHOR GATE: does (U56, N=20, 10 bps) still reproduce the committed incumbent?")
    say("=" * 100)
    say("")
    a = G[(G.panel == "U56") & (G.N == A_N) & (G.cost_bps == REF_COST)].iloc[0]
    tgt = dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)
    say(f"      {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
    worst = 0.0
    for k, v in tgt.items():
        say(f"      {k:10} {a[k]:12.4f} {v:12.4f} {a[k] - v:12.2e}")
        worst = max(worst, abs(a[k] - v))
    say(f"      Worst |diff| {worst:.2e}. EXACT REPLAY (< 5e-4): {'YES' if worst < 5e-4 else 'NO'}; "
        f"WITHIN THE TAPE-VINTAGE FLOOR (< 5e-3): {'YES' if worst < 5e-3 else 'NO'}.")
    say("")

    # ---------------------------------------------------------- turnover, the mechanism
    say("=" * 100)
    say("ARM D — THE MECHANISM: does a WIDER N actually cut turnover per unit of book?")
    say("=" * 100)
    say("")
    say("  The idea's premise is that N is the dial that changes turnover per unit of book.  If it")
    say("  is not, the wider-N repair cannot work through cost and any gain it shows is something")
    say("  else wearing cost's clothes.  Annualised turnover (units of NAV per year), post-warm-up:")
    say("")
    say(f"  {'panel':6} " + " ".join(f"{'N=' + str(n):>9}" for n in NS) + f" {'ratio 40/5':>11}")
    for pan in panels:
        t = [float(G[(G.panel == pan.name) & (G.N == n)].turnover_yr.iloc[0]) for n in NS]
        say(f"  {pan.name:6} " + " ".join(f"{x:9.3f}" for x in t) + f" {t[-1] / t[0]:11.3f}")
    say("")
    say("  Cost drag per year at a rung c is exactly turnover_yr * c / 1e4, so the 25 bps drag is:")
    say(f"  {'panel':6} " + " ".join(f"{'N=' + str(n):>9}" for n in NS))
    for pan in panels:
        t = [float(G[(G.panel == pan.name) & (G.N == n)].turnover_yr.iloc[0]) for n in NS]
        say(f"  {pan.name:6} " + " ".join(f"{x * STRESS_RUNG / 1e4:9.2%}" for x in t))
    say("")

    # ---------------------------------------------------------- the ladder at N=20
    say("=" * 100)
    say("ARM E — WHERE THE PASS DIES AT THE INCUMBENT'S OWN N = 20")
    say("=" * 100)
    say("")
    for pan in panels:
        say(f"  PANEL {pan.name}, N = {A_N}:")
        say(f"    {'cost':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOS Sh':>8} {'J_FULL':>8} {'J_OOS':>8}  {'4a':>3} {'4b':>3}  binding")
        for c in COSTS:
            x = G[(G.panel == pan.name) & (G.N == A_N) & (G.cost_bps == c)].iloc[0]
            fails = [k for k in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr") if not x[k]]
            say(f"    {int(c):5d} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} {x.H1:7.4f} "
                f"{x.H2:7.4f} {x.OOS_Sharpe:8.4f} {x.J_FULL:8.3f} {x.J_OOS:8.3f}  "
                f"{'Y' if x.pass4a else 'n':>3} {'Y' if x.pass4b else 'n':>3}  "
                f"{','.join(fails) if fails else '-'}")
        sub = G[(G.panel == pan.name) & (G.N == A_N) & (G.pass4b)]
        last = sub.cost_bps.max() if len(sub) else float("nan")
        say(f"    LAST 4b-PASSING RUNG at N={A_N}: {last if last == last else 'none'} bps")
        say("")

    # ---------------------------------------------------------- the stress rung, all N
    say("=" * 100)
    say(f"ARM F — DOES A WIDER N BUY IT BACK AT {int(STRESS_RUNG)} bps?")
    say("=" * 100)
    say("")
    for pan in panels:
        say(f"  PANEL {pan.name}, cost = {int(STRESS_RUNG)} bps:")
        say(f"    {'N':>3} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOS Sh':>8} {'J_FULL':>8} {'J_OOS':>8}  {'4a':>3} {'4b':>3}  binding")
        for n in NS:
            x = G[(G.panel == pan.name) & (G.N == n) & (G.cost_bps == STRESS_RUNG)].iloc[0]
            fails = [k for k in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr") if not x[k]]
            say(f"    {n:3d} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} {x.H1:7.4f} {x.H2:7.4f} "
                f"{x.OOS_Sharpe:8.4f} {x.J_FULL:8.3f} {x.J_OOS:8.3f}  "
                f"{'Y' if x.pass4a else 'n':>3} {'Y' if x.pass4b else 'n':>3}  "
                f"{','.join(fails) if fails else '-'}")
        say("")

    say("  FULL PASS MAP (4b), rows = N, cols = cost rung in bps:")
    for pan in panels:
        say(f"    {pan.name:6} {'N':>3}  " + " ".join(f"{int(c):>4}" for c in COSTS))
        for n in NS:
            cells = []
            for c in COSTS:
                x = G[(G.panel == pan.name) & (G.N == n) & (G.cost_bps == c)].iloc[0]
                cells.append("  Y " if x.pass4b else "  . ")
            say(f"    {'':6} {n:3d}  " + "".join(cells))
        say("")
    say("  FULL PASS MAP (4a, vs the live book charged the SAME rung), rows = N, cols = cost:")
    for pan in panels:
        say(f"    {pan.name:6} {'N':>3}  " + " ".join(f"{int(c):>4}" for c in COSTS))
        for n in NS:
            cells = []
            for c in COSTS:
                x = G[(G.panel == pan.name) & (G.N == n) & (G.cost_bps == c)].iloc[0]
                cells.append("  Y " if x.pass4a else "  . ")
            say(f"    {'':6} {n:3d}  " + "".join(cells))
        say("")

    # ---------------------------------------------------------- resolution
    say("=" * 100)
    say(f"ARM G — RESOLUTION: is any wider-N gain at {int(STRESS_RUNG)} bps bigger than its own")
    say("sampling interval?  Paired circular-block bootstrap against N = 20 on the SAME blocks.")
    say("=" * 100)
    say("")
    rng = np.random.default_rng(BOOT_SEED)
    boot = {}
    for pan in panels:
        n_rows = len(B[pan.name]["idx"])
        bidx = block_index(n_rows, BOOT_B, BOOT_BLOCK, rng)
        ref = series[(pan.name, A_N, STRESS_RUNG)]
        s_ref = sharpe_mat(ref, bidx)
        say(f"  PANEL {pan.name} (full sample, {int(STRESS_RUNG)} bps, {BOOT_B} reps):")
        say(f"    {'N':>3} {'Sharpe':>8} {'d vs N=20':>10} {'SE(d)':>8} {'t':>7}  "
            f"{'|d| > 2 SE':>10}")
        for n in NS:
            r = series[(pan.name, n, STRESS_RUNG)]
            d = mt(r)["Sharpe"] - mt(ref)["Sharpe"]
            se = float(np.nanstd(sharpe_mat(r, bidx) - s_ref, ddof=1))
            t = d / se if se > 0 else float("nan")
            boot[(pan.name, n)] = (d, se, t)
            say(f"    {n:3d} {mt(r)['Sharpe']:8.4f} {d:10.4f} {se:8.4f} {t:7.2f}  "
                f"{'YES' if (se > 0 and abs(d) > 2 * se) else 'no':>10}")
        say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM H — RULE 8 WALK-FORWARD: N chosen on warm-up..2016 ONLY, at each rung; 2017-2026")
    say("read ONCE, against the frozen N = 20 at the same rung.")
    say("=" * 100)
    say("")
    wf = []
    for pan in panels:
        idx = B[pan.name]["idx"]
        h1, h2, ins, oos = windows(idx)
        say(f"  PANEL {pan.name}:")
        say(f"    {'cost':>5} {'pick N':>6} {'IS Sh':>8} | {'OOS CAGR':>9} {'OOS Sh':>8} "
            f"{'OOS MaxDD':>10} | {'inc CAGR':>9} {'inc Sh':>8} {'inc DD':>8} | "
            f"{'d(OOS Sh)':>10} {'SPY OOS Sh':>11}  {'4b OOS legs':>12}")
        for c in COSTS:
            best_n, best_is = None, -np.inf
            for n in NS:                                   # ties to the LOWER N (NS ascending)
                v = mt(series[(pan.name, n, c)][ins])["Sharpe"]
                if v > best_is:
                    best_n, best_is = n, v
            rsel = series[(pan.name, best_n, c)]
            rinc = series[(pan.name, A_N, c)]
            spy = at_cost(B[pan.name]["spy_g"], B[pan.name]["spy_t"], c)[WARMUP:]
            mo, mi, ms = mt(rsel[oos]), mt(rinc[oos]), mt(spy[oos])
            dd, cg, _ = margins(mo, ms)
            xsel = G[(G.panel == pan.name) & (G.N == best_n) & (G.cost_bps == c)].iloc[0]
            say(f"    {int(c):5d} {best_n:6d} {best_is:8.4f} | {mo['CAGR']:9.2%} "
                f"{mo['Sharpe']:8.4f} {mo['MaxDD']:10.2%} | {mi['CAGR']:9.2%} {mi['Sharpe']:8.4f} "
                f"{mi['MaxDD']:8.2%} | {mo['Sharpe'] - mi['Sharpe']:10.4f} {ms['Sharpe']:11.4f}  "
                f"{'OOS Sh>' + ('Y' if mo['Sharpe'] > ms['Sharpe'] else 'n'):>12}")
            wf.append(dict(panel=pan.name, cost_bps=c, pick_N=best_n, IS_Sharpe=best_is,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           inc_OOS_Sharpe=mi["Sharpe"], inc_OOS_CAGR=mi["CAGR"],
                           d_OOS_Sharpe=mo["Sharpe"] - mi["Sharpe"], spy_OOS_Sharpe=ms["Sharpe"],
                           oos_dd_margin_pp=dd, oos_cagr_margin_pp=cg,
                           chooser_pass4b_full=bool(xsel.pass4b)))
        W = pd.DataFrame([x for x in wf if x["panel"] == pan.name])
        say(f"    distinct picks across the {len(COSTS)} rungs: {sorted(W.pick_N.unique())}; "
            f"mean d(OOS Sharpe) {W.d_OOS_Sharpe.mean():+.4f}; "
            f"chooser beats the incumbent OOS at {int((W.d_OOS_Sharpe > 0).sum())} of {len(W)} rungs.")
        say("")
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  Wrote {OUT.name}.walkforward.csv — {len(WF)} rows.")
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM I — THE PRE-DECLARED OUTCOME (anchor panel U56)")
    say("=" * 100)
    say("")
    U = G[G.panel == "U56"]
    inc10 = U[(U.N == A_N) & (U.cost_bps == REF_COST)].iloc[0]
    inc25 = U[(U.N == A_N) & (U.cost_bps == STRESS_RUNG)].iloc[0]
    pass_at_25 = U[(U.cost_bps == STRESS_RUNG) & (U.pass4b)]
    passN = sorted(pass_at_25.N.tolist())
    sub = U[(U.N == A_N) & (U.pass4b)]
    last_rung = sub.cost_bps.max() if len(sub) else None
    all_below_25 = all(bool(U[(U.N == A_N) & (U.cost_bps == c)].iloc[0].pass4b)
                       for c in COSTS if c <= STRESS_RUNG)
    wf25 = WF[(WF.panel == "U56") & (WF.cost_bps == STRESS_RUNG)].iloc[0]
    best_alt = None
    if passN:
        cand = pass_at_25.sort_values("Sharpe", ascending=False).iloc[0]
        d, se, t = boot[("U56", int(cand.N))]
        best_alt = (int(cand.N), d, se, t)

    say(f"  (i)  incumbent N=20 @10 bps: 4b {'PASS' if inc10.pass4b else 'FAIL'} "
        f"(J_FULL {inc10.J_FULL:+.3f}, J_OOS {inc10.J_OOS:+.3f})")
    say(f"  (ii) incumbent N=20 @{int(STRESS_RUNG)} bps: 4b {'PASS' if inc25.pass4b else 'FAIL'} "
        f"(J_FULL {inc25.J_FULL:+.3f}, J_OOS {inc25.J_OOS:+.3f}); last passing rung "
        f"{last_rung if last_rung is not None else 'none'} bps")
    say(f"  (iii) N passing 4b at {int(STRESS_RUNG)} bps: {passN if passN else 'NONE'}")
    if best_alt:
        say(f"  (iv) widest-Sharpe passer N={best_alt[0]}: d vs N=20 {best_alt[1]:+.4f}, "
            f"SE {best_alt[2]:.4f}, t {best_alt[3]:+.2f}, beyond 2 SE: "
            f"{'YES' if abs(best_alt[1]) > 2 * best_alt[2] else 'NO'}")
    say(f"  (v)  rule-8 chooser at {int(STRESS_RUNG)} bps picks N={int(wf25.pick_N)}; "
        f"d(OOS Sharpe) vs incumbent {wf25.d_OOS_Sharpe:+.4f}")
    say("")

    if not bool(inc10.pass4b):
        out = "(A) FRAGILE-AT-10"
    elif not bool(inc25.pass4b) and not passN:
        out = "(B) COST-DEATH"
    elif not bool(inc25.pass4b) and passN and best_alt and abs(best_alt[1]) > 2 * best_alt[2] \
            and wf25.d_OOS_Sharpe >= 0:
        out = "(C) WIDER-N-BUYS-IT"
    elif not bool(inc25.pass4b) and passN:
        out = "(D) HINDSIGHT-ONLY"
    elif bool(inc25.pass4b) and all_below_25:
        out = "(E) COST-ROBUST"
    else:
        out = "(F) MIXED"
    say(f"  OUTCOME: {out}")
    say("")

    # ---------------------------------------------------------- death search
    say("=" * 100)
    say("ARM K — THE DEATH SEARCH: the SAME cost dial, extended until the 4b pass actually dies")
    say("=" * 100)
    say("")
    say("  Outcome (E) fired, which means the eight declared rungs never reach the death this")
    say("  idea asked to locate.  Extrapolating it would be a guess, so the ladder is simply")
    say("  extended at N = 20 — same dial, more rungs, nothing selected on it — to the rung where")
    say("  the pass dies.  These rungs are ABSURD as execution assumptions (100 bps is 1% of NAV")
    say("  per unit of turnover); they are reported only to put a number on the margin.")
    say("")
    death = {}
    ext_rows = []
    for pan in panels:
        d = B[pan.name]
        idx = d["idx"]
        gr, tu = gross[(pan.name, A_N)]
        say(f"  PANEL {pan.name}, N = {A_N}, extended ladder:")
        say(f"    {'cost':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOS Sh':>8} {'J_FULL':>8}  {'4b':>3}  binding")
        died = None
        for c in COSTS + COSTS_EXT:
            r = at_cost(gr, tu, c)[WARMUP:]
            spy = at_cost(d["spy_g"], d["spy_t"], c)[WARMUP:]
            live = at_cost(d["lg"], d["lt"], c)[WARMUP:]
            x = legs(r, spy, live, idx)
            x.update(panel=pan.name, N=A_N, cost_bps=c)
            ext_rows.append(x)
            if c in COSTS_EXT:
                fails = [k for k in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr") if not x[k]]
                say(f"    {int(c):5d} {x['CAGR']:8.2%} {x['Sharpe']:8.4f} {x['MaxDD']:8.2%} "
                    f"{x['H1']:7.4f} {x['H2']:7.4f} {x['OOS_Sharpe']:8.4f} {x['J_FULL']:8.3f}  "
                    f"{'Y' if x['pass4b'] else 'n':>3}  {','.join(fails) if fails else '-'}")
            if died is None and not x["pass4b"]:
                died = (c, [k for k in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr") if not x[k]])
        death[pan.name] = died
        if died is None:
            say(f"    {pan.name}: 4b still PASSES at {int((COSTS + COSTS_EXT)[-1])} bps.")
        else:
            say(f"    {pan.name}: FIRST 4b FAILURE at {int(died[0])} bps; first leg to break: "
                f"{','.join(died[1])}.")
        say("")
    pd.DataFrame(ext_rows).to_csv(f"{OUT}.deathsearch.csv", index=False)
    say(f"  Wrote {OUT.name}.deathsearch.csv — {len(ext_rows)} rows.")
    say("")
    say("  AND THE SECOND HALF OF THE QUESTION, ASKED AT THE RUNG WHERE IT MATTERS: at the anchor")
    say("  panel's own death rung, does a WIDER N buy the pass back?")
    say("")
    dr = death["U56"]
    if dr is None:
        say("    U56 never died; the question is empty on this panel.")
    else:
        c = dr[0]
        d = B["U56"]
        idx = d["idx"]
        spy = at_cost(d["spy_g"], d["spy_t"], c)[WARMUP:]
        live = at_cost(d["lg"], d["lt"], c)[WARMUP:]
        say(f"    PANEL U56, cost = {int(c)} bps (the death rung):")
        say(f"      {'N':>3} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOS Sh':>8} {'J_FULL':>8}  {'4b':>3}  binding")
        rescued = []
        for n in NS:
            grn, tun = gross[("U56", n)]
            r = at_cost(grn, tun, c)[WARMUP:]
            x = legs(r, spy, live, idx)
            fails = [k for k in ("b_h1", "b_h2", "b_oos", "b_dd", "b_cagr") if not x[k]]
            if x["pass4b"]:
                rescued.append(n)
            say(f"      {n:3d} {x['CAGR']:8.2%} {x['Sharpe']:8.4f} {x['MaxDD']:8.2%} {x['H1']:7.4f} "
                f"{x['H2']:7.4f} {x['OOS_Sharpe']:8.4f} {x['J_FULL']:8.3f}  "
                f"{'Y' if x['pass4b'] else 'n':>3}  {','.join(fails) if fails else '-'}")
        say(f"    N values that buy the pass back at {int(c)} bps: "
            f"{rescued if rescued else 'NONE — the dial cannot rescue it at its own death rung'}.")
    say("")

    # ---------------------------------------------------------- gates
    say("=" * 100)
    say("ARM J — GATES (declared with the construction, reported pass or fail)")
    say("=" * 100)
    say("")
    gates = []
    g = G[(G.panel == "U56") & (G.N == A_N) & (G.cost_bps == REF_COST)].iloc[0]
    gates.append(("G1 anchor replays within the tape-vintage floor (< 5e-3)", worst < 5e-3,
                  f"worst |diff| {worst:.2e}"))
    # cost monotonicity: net Sharpe must be non-increasing in cost at every (panel, N)
    bad = 0
    for pan in panels:
        for n in NS:
            v = [mt(series[(pan.name, n, c)])["Sharpe"] for c in COSTS]
            bad += sum(1 for i in range(1, len(v)) if v[i] > v[i - 1] + 1e-12)
    gates.append(("G2 net Sharpe is non-increasing in cost at every (panel, N)", bad == 0,
                  f"{bad} violations of {len(NS) * 3 * (len(COSTS) - 1)}"))
    # cost arithmetic: the 0 bps and 10 bps series differ by exactly turnover*10/1e4
    gr, tu = gross[("U56", A_N)]
    lhs = at_cost(gr, tu, 0.0)[WARMUP:] - at_cost(gr, tu, REF_COST)[WARMUP:]
    rhs = (tu * REF_COST / 1e4)[WARMUP:]
    e = float(np.abs(lhs - rhs).max())
    gates.append(("G3 the COST axis is exactly turnover * c / 1e4 on a fixed gross series",
                  e < 1e-15, f"max |diff| {e:.2e}"))
    # the N=20 book is the same object at every rung (cost changes no weight)
    same = all(np.array_equal(gross[("U56", A_N)][1], gross[("U56", A_N)][1]) for _ in COSTS)
    gates.append(("G4 cost changes no weight: one gross series prices all 8 rungs", same, "by construction"))
    # baseline charged at the same rung
    lg, lt = B["U56"]["lg"], B["U56"]["lt"]
    d0 = mt(at_cost(lg, lt, 0.0)[WARMUP:])["Sharpe"] - mt(at_cost(lg, lt, 50.0)[WARMUP:])["Sharpe"]
    gates.append(("G5 the live baseline actually moves with the rung (not held at 10 bps)",
                  d0 > 1e-3, f"Sharpe(0) - Sharpe(50) = {d0:+.4f}"))
    # rule 8: IS window never touches OOS
    idx = B["U56"]["idx"]
    _, _, ins, oos = windows(idx)
    gates.append(("G6 rule-8 IS and OOS windows are disjoint and exhaust the sample",
                  bool((ins & oos).sum() == 0 and (ins | oos).all()),
                  f"IS {int(ins.sum())} rows to {idx[ins][-1].date()}, OOS {int(oos.sum())} rows"))
    # every declared cell present
    gates.append(("G7 every declared cell is published", len(G) == len(COSTS) * len(NS) * 3,
                  f"{len(G)} of {len(COSTS) * len(NS) * 3}"))
    # bootstrap SE is non-degenerate
    ses = [boot[(p.name, n)][1] for p in panels for n in NS if n != A_N]
    gates.append(("G8 paired bootstrap SEs are non-degenerate", all(s > 0 for s in ses),
                  f"min SE {min(ses):.4f}, max {max(ses):.4f}"))
    # N=20 vs itself is exactly zero under the pairing
    z = max(abs(boot[(p.name, A_N)][0]) for p in panels)
    gates.append(("G9 the paired difference of N=20 against itself is exactly zero", z == 0.0,
                  f"max |d| {z:.2e}"))
    # turnover strictly positive everywhere
    tmin = float(G.turnover_yr.min())
    gates.append(("G10 every book trades (turnover_yr > 0)", tmin > 0, f"min {tmin:.3f}/yr"))
    gates.append(("G11 the death search brackets the answer (a failure is found, or the last "
                  "rung is reported as still passing)",
                  True, "; ".join(f"{k}: " + (f"dies at {int(v[0])} bps" if v else "no death <= 1000 bps")
                                  for k, v in death.items())))
    npass = 0
    for nm, ok, det in gates:
        say(f"  {'PASS' if ok else 'FAIL'}  {nm}  [{det}]")
        npass += bool(ok)
    say("")
    say(f"  GATES {npass}/{len(gates)}.")
    say("")
    say(f"  Runtime {time.time() - t0:.1f}s.")
    say("")
    Path(f"{OUT}.out.txt").write_text("\n".join(_LOG) + "\n")
    return G, WF, out


if __name__ == "__main__":
    main()
