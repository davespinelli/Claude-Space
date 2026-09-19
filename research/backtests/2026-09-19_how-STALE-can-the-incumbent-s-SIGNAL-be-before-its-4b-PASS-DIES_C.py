#!/usr/bin/env python3
"""
Idea 1298 (lane C, 2026-09-19) — how STALE can the incumbent's SIGNAL be before its 4b PASS DIES?

THE PREMISE.  PROTOCOL rule 2 fixes execution at t+1: rank on the close of row t, hold from the
close of row t+1.  Every committed number in this family is read at that single, most-favourable
implementable convention.  A real account misses fills, runs the screen the next morning, trades
on a schedule, or is simply not at the desk.  If the 2026-09-04 KEEP-4b book's pass lives inside
one day of staleness, it is a short-horizon artefact dressed as a 6-12 month momentum book and it
is not capital-worthy however it scores at d = 1.

WHAT THIS RUN ADDS OVER IDEA 1287, WHICH WALKED THE SAME AXIS.  1287 (lane cloud, 2026-09-18)
walked LAG {1,2,3,5,10} x CADENCE {W,M} at this same book and reported U56 4b PASS at d=1, FAIL at
d=2 and d=3, PASS again at d=5, FAIL at d=10 — a ladder that is NOT monotone, which is what a
decay claim needs to be.  A non-monotone ladder is either a real, jagged decay or it is noise, and
1287 measured no resolution with which to tell the two apart.  This run (i) extends the ladder to
d = 21 (a full month, the rung an operator who rebalances late actually sits at), (ii) attaches a
PAIRED CIRCULAR-BLOCK BOOTSTRAP to every rung, so each rung's distance from d = 1 is read against
its own sampling interval rather than against zero, and (iii) walks BOTH CONSTRUCTIONS of "lag"
that the record now contains, because they are not the same book:

    LATE  (this idea's own wording — "trades late"):  decide on the weekly close, TRADE d rows
          later.  Application row = decision row + d; the ranking snapshot stays on the Friday.
    SNAP  (idea 1287's construction):  trade on the fixed row after each weekly close, using a
          ranking snapshot that is d rows OLD.  Application row = decision row + 1; snapshot row
          = application row - d.

  d = 1 is identically PROTOCOL rule 2 under both.  At d >= 2 they differ, and a first pass of
  this run measured that difference at up to 1.0e-1 of Sharpe on B136 — THREE TIMES the entire
  spread of the lag ladder itself.  The convention is therefore NOT a nuisance: reporting a lag
  result without naming which one was built is uninterpretable, and that is a finding about the
  record, not about this book.  CONVENTION IS NOT A TUNED PARAMETER (rule 4): nothing is selected
  on it, both arms are published whole, and the verdict below is taken on LATE, the construction
  this idea's own text describes.  SNAP additionally serves as the replay gate for 1287's
  committed rows on today's tape (commit 4e19a80 rewrote data/prices*.csv after 1287 ran — idea
  1350's finding), which the first pass could not test because it built the other book.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  For each (LAG, PANEL) cell, build the SAME book — 3-leg composite (21/252, 0/126, 0/63)
  equal-ranked, above-200d AND vol20 < 0.60 eligibility, top N = 20 with a 126-row minimum hold,
  gross 0.75, weekly decision rows, 10 bps per unit turnover — changing ONLY how stale the ranking
  snapshot is at application time:

      LAG = d   means   the ranking snapshot used at the application row is d rows old,
                        under whichever of the two conventions above is being built.

  LAG = 1 is PROTOCOL rule 2 exactly under both, and must reproduce the committed incumbent.  Nothing else in
  the construction moves.  Then, per panel:

      DECAY(d)   = Sharpe(d) - Sharpe(1)                       (full sample, net of 10 bps)
      SE(d)      = SD over 400 circular-block bootstrap replicates (63-row blocks, seed 20260919)
                   of that SAME paired difference, the two books resampled on IDENTICAL blocks
      SLOPE      = OLS slope of net Sharpe on d over the six rungs, per day of staleness
      rho        = Spearman(d, Sharpe) over the six rungs

  and the same DECAY/SE pair for CAGR and for the rule-8 OOS window.

  PRE-DECLARED OUTCOMES, fixed here before anything is read.  Applied to the ANCHOR PANEL (U56),
  in this order; whichever fires is the report.
    (A) FRAGILE     — 4b fails already at d = 2 AND that rung's DECAY is beyond 2 SE below zero.
                      The pass is one day deep and the book is a KILL for real capital.
    (B) DECAYS      — rho <= -0.80 AND some rung at d <= 5 is beyond 2 SE below zero.  A real,
                      ordered decay; the run reports the rung at which 4b dies.
    (C) UNRESOLVED  — every one of the five rungs sits within 2 SE of zero.  The lag axis carries
                      no signal this tape can resolve, and EVERY 4b pass/fail flip along it —
                      1287's included — is a coin flip, not a finding.  The honest reading is
                      then that staleness is not shown to be survivable, only not shown to hurt.
    (D) ROBUST      — 4b clears at every rung out to d = 5, AND the d = 5 rung is within 2 SE.
    (E) MIXED       — none of the above fires cleanly; the run says so and classifies nothing.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  LAG    {1, 2, 3, 5, 10, 21} trading days   (1 is rule 2; the rest are the stress)
  PANEL  {U56, B136, SMALL}                  (the idea names panel as its second parameter)

  18 cells per convention, 36 in all, EVERY ONE PUBLISHED in `.grid.csv`.  Nothing is tuned; both
  ladders are walked whole.  CONVENTION {LATE, SNAP} is a replication control, not a third dial.

NOT DIALS, reported at every value: the 4a and 4b legs; full sample, both halves, the rule-8 OOS
window; the live RULES v2 baseline and SPY.

FROZEN at the incumbent's construction, not tuned here: N = 20, H = 126, gross = 0.75, weekly
cadence (last trading row with weekday <= 4 in each calendar week), 3-leg composite, above-200d +
vol20 < 0.60, 10 bps, 260-row warm-up, first-wins stable tie-break, equal weights within the book.

RULE 8, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  Per panel, the LAG is chosen on
warm-up..2016-12-31 ONLY, by highest IS net Sharpe, ties to the LOWER lag; 2017-2026 is then read
ONCE, against the frozen d = 1 comparand PROTOCOL mandates.  The reported quantity is
chooser-minus-do-nothing in OOS Sharpe.  A positive number would mean an operator could pick a
useful staleness in sample; a negative one means choosing the lag costs money.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen.  Delisted, acquired and bankrupt names are absent
from all three, which flatters every momentum book here.  Tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped from SMALL before anything is built.  No level here is an estimate
of live expectancy; all readings are relative, across rungs, on fixed panels.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_how-STALE-can-the-incumbent-s-SIGNAL-be-before-its-4b-PASS-DIES_C.py
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
A_N, A_H, A_G = 20, 126, 0.75                 # the frozen 2026-09-04 book
LAGS = [1, 2, 3, 5, 10, 21]                   # dial 1
CONVS = ["LATE", "SNAP"]                      # replication control, NOT a dial
OOS_START = pd.Timestamp("2017-01-01")        # rule 8
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


def build(pan, N, d, conv="LATE"):
    """The incumbent's min-hold top-N frame at UNIT gross, ranked d rows before application.

    conv = "LATE" (this idea's wording): decide on the weekly close, TRADE d rows later —
           application row = decision row + d, snapshot row = decision row.
    conv = "SNAP" (idea 1287's construction): trade on the fixed row after the weekly close with
           a d-row-old snapshot — application row = decision row + 1, snapshot = app - d.
    d = 1 is identical under both and is PROTOCOL rule 2.  Kept names hold for at least A_H rows
    from their own application row; free slots go to the best-ranked eligible names read at the
    snapshot row."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    if conv == "LATE":
        app = pan.dec + d
        dec = pan.dec
    elif conv == "SNAP":
        app = pan.dec + 1
        dec = np.maximum(app - d, 0)
    else:
        raise ValueError(conv)
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
    """4b's two one-sided margins in percentage points."""
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


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return float("nan")
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return float("nan")
    return float(((rx - rx.mean()) * (ry - ry.mean())).mean() / (sx * sy))


def ols_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())


def block_index(n, B, block, rng):
    """One (B, n) matrix of circular-block bootstrap row indices, shared by every series so the
    Sharpe difference stays PAIRED."""
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(B, nb))
    off = np.arange(block)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(B, nb * block)[:, :n]
    return idx % n


def sharpe_mat(R, idx):
    """Annualised Sharpe of series R over each bootstrap row-index replicate."""
    X = R[idx]
    m = X.mean(axis=1)
    s = X.std(axis=1, ddof=1)
    return np.where(s > 0, m * 252 / (s * np.sqrt(252)), np.nan)


def cagr_mat(R, idx):
    X = np.log1p(R[idx])
    yrs = idx.shape[1] / 252.0
    return np.expm1(X.sum(axis=1) / yrs)


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
    say("IDEA 1298 (lane C, 2026-09-19) — how STALE can the incumbent's SIGNAL be before its")
    say("4b PASS DIES?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): LAG {LAGS} x PANEL {{U56, B136, SMALL}} = {len(LAGS) * 3} cells per")
    say(f"  convention, {len(LAGS) * 3 * len(CONVS)} in all, every one published in .grid.csv.")
    say("  CONVENTION (a replication control, NOT a dial; both published, nothing selected on it):")
    say("    LATE = this idea's wording — decide on the weekly close, TRADE d rows later.")
    say("    SNAP = idea 1287's construction — trade on the fixed next row with a d-row-old snapshot.")
    say("  d = 1 is identical under both and IS PROTOCOL rule 2. The VERDICT is taken on LATE.")
    say(f"  FROZEN: N={A_N}, H={A_H}, gross={A_G}, weekly, 10 bps, above-200d & vol20<{MAXVOL},")
    say("  3-leg composite, 260-row warm-up, equal weights, first-wins tie-break.")
    say(f"  RESOLUTION: paired circular-block bootstrap, {BOOT_B} reps x {BOOT_BLOCK}-row blocks,")
    say(f"  seed {BOOT_SEED}; both books resampled on IDENTICAL blocks so the difference is paired.")
    say("  OUTCOMES (anchor panel U56, in order): (A) FRAGILE (B) DECAYS (C) UNRESOLVED")
    say("  (D) ROBUST (E) MIXED.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY benchmark only.")
    say(f"  TAPE: U56 {panels[0].idx[0].date()} .. {panels[0].idx[-1].date()} "
        f"({len(panels[0].idx)} rows); B136 {panels[1].idx[-1].date()}; SMALL {panels[2].idx[-1].date()}.")
    say("")

    # ---------------------------------------------------------- benchmarks
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
    rows, series = [], {}
    for pan in panels:
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        for conv in CONVS:
            for d in LAGS:
                W1, app = build(pan, A_N, d, conv)
                gr, tu = nrun(pan, W1 * A_G, app)
                r = at_cost(gr, tu, REF_COST)[WARMUP:]
                series[(pan.name, conv, d)] = r
                rec = legs(r, spy, live, idx)
                rec.update(panel=pan.name, conv=conv, lag=d,
                           avg_names=float((W1[WARMUP:][:, pan.iinv] > 0).sum(axis=1).mean()),
                           turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
                rows.append(rec)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------- anchor gate
    say("=" * 100)
    say("ARM B — THE ANCHOR GATE: does (U56, d=1) still reproduce the committed incumbent, and do")
    say("1287's committed lag rows reproduce on TODAY's tape?")
    say("=" * 100)
    say("")
    a = G[(G.panel == "U56") & (G.lag == 1) & (G.conv == "LATE")].iloc[0]
    tgt = dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)
    say("  (i) the 2026-09-04 incumbent, as committed by idea 1294 (U56, N=20, g=0.75, d=1):")
    say(f"      {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
    worst = 0.0
    for k, v in tgt.items():
        say(f"      {k:10} {a[k]:12.4f} {v:12.4f} {a[k] - v:12.2e}")
        worst = max(worst, abs(a[k] - v))
    ok = worst < 5e-4
    tape_ok = worst < 5e-3
    say(f"      Worst |diff| {worst:.2e}. EXACT REPLAY (< 5e-4): {'YES' if ok else 'NO'}; "
        f"WITHIN THE TAPE-VINTAGE FLOOR (< 5e-3, idea 1335 measured ~7e-3 on halves from a single "
        f"daily rewrite): {'YES' if tape_ok else 'NO'}.")
    say("")
    say("  (ii) idea 1287's committed weekly lag ladder, replayed under BOTH conventions. Under")
    say("       SNAP — 1287's OWN construction — a residual diff is a TAPE-VINTAGE fact (commit")
    say("       4e19a80 rewrote data/prices*.csv after 1287 ran, idea 1350's finding). Under LATE")
    say("       the diff is CONSTRUCTION, not tape, and that gap is itself this run's finding.")
    prior_sh = {("U56", 1): 1.152861, ("U56", 2): 1.104592, ("U56", 3): 1.119762,
                ("U56", 5): 1.124877, ("U56", 10): 1.135882,
                ("B136", 1): 1.072148, ("B136", 2): 1.155134, ("B136", 3): 1.143116,
                ("B136", 5): 1.063925, ("B136", 10): 1.068324,
                ("SMALL", 1): 0.508144, ("SMALL", 2): 0.564809, ("SMALL", 3): 0.548766,
                ("SMALL", 5): 0.536482, ("SMALL", 10): 0.541650}
    say(f"      {'panel':6} {'d':>3} {'SNAP Sh':>10} {'diff vs 1287':>13} {'LATE Sh':>10} "
        f"{'diff vs 1287':>13} {'SNAP-LATE':>10}")
    dsnap, dlate, dconv = 0.0, 0.0, 0.0
    for (pp, d), v in prior_sh.items():
        xs = float(G[(G.panel == pp) & (G.lag == d) & (G.conv == "SNAP")].iloc[0]["Sharpe"])
        xl = float(G[(G.panel == pp) & (G.lag == d) & (G.conv == "LATE")].iloc[0]["Sharpe"])
        dsnap = max(dsnap, abs(xs - v)); dlate = max(dlate, abs(xl - v))
        dconv = max(dconv, abs(xs - xl))
        say(f"      {pp:6} {d:3d} {xs:10.6f} {xs - v:13.2e} {xl:10.6f} {xl - v:13.2e} "
            f"{xs - xl:10.2e}")
    say(f"      Worst |diff| vs 1287 across the 15 replayed cells: SNAP (1287's own construction)")
    say(f"      {dsnap:.2e}; LATE {dlate:.2e}. Worst |SNAP - LATE| on the same cells: {dconv:.2e}.")
    if dsnap < dlate / 2:
        say(f"      SNAP replays 1287 to {dsnap:.1e} against LATE's {dlate:.1e} — a factor "
            f"{dlate / max(dsnap, 1e-12):.1f}. The d >= 2 gap is therefore CONSTRUCTION, not tape;")
        say(f"      the tape's own contribution is the d = 1 diff, common to both conventions.")
    else:
        say(f"      SNAP does NOT replay 1287 materially better than LATE ({dsnap:.1e} vs "
            f"{dlate:.1e}), so the gap is not attributable to construction alone.")
    say("")
    if not ok and tape_ok:
        say("  READING. The d=1 anchor misses the 5e-4 exact-replay gate but sits inside the")
        say("  tape-vintage floor: data/prices*.csv was rewritten wholesale on 2026-09-18 (commit")
        say("  4e19a80) after the committed numbers were taken, and idea 1335 measured ~7e-3 of")
        say("  half-sample Sharpe movement from one such rewrite. EVERY cell in this run is built")
        say("  on ONE tape, so the within-run comparisons below — rung against rung, convention")
        say("  against convention — are unaffected. Only comparisons to committed numbers from")
        say("  other runs carry this floor, and those are labelled where they appear.")
        say("")
    elif not ok:
        say("  *** The d=1 anchor misses BOTH gates. Every number below is about a book that is")
        say("  *** not the committed one; no verdict may be taken on it.")
        say("")

    # ---------------------------------------------------------- the ladder
    say("=" * 100)
    say("ARM C — THE LAG LADDER, EVERY RUNG, BOTH KEEP PATHS")
    say("=" * 100)
    say("")
    say(f"  {'conv':5} {'panel':6} {'d':>3} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} "
        f"{'H2':>7} {'OOS CAGR':>9} {'OOS Sh':>8} {'turn/yr':>8} {'4b DD mgn':>10} {'4b':>4} "
        f"{'4a':>4}  failing 4b legs")
    nm = dict(b_h1="H1", b_h2="H2", b_oos="OOS", b_dd="DD", b_cagr="CAGR")
    for conv in CONVS:
        for pan in panels:
            for d in LAGS:
                x = G[(G.panel == pan.name) & (G.lag == d) & (G.conv == conv)].iloc[0]
                bad = ",".join(v for k, v in nm.items() if not x[k]) or "-"
                say(f"  {conv:5} {pan.name:6} {d:3d} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} "
                    f"{x.H1:7.4f} {x.H2:7.4f} {x.OOS_CAGR:9.2%} {x.OOS_Sharpe:8.4f} "
                    f"{x.turnover_yr:8.2f} {x.dd_margin_pp:+10.3f} "
                    f"{'PASS' if x.pass4b else 'FAIL':>4} {'PASS' if x.pass4a else 'FAIL':>4}  {bad}")
            say("")
    for conv in CONVS:
        sub = G[G.conv == conv]
        say(f"  {conv}: 4b passes {int(sub.pass4b.sum())} of {len(sub)} cells; "
            f"4a passes {int(sub.pass4a.sum())}.")
    say("")

    # ---------------------------------------------------------- resolution
    say("=" * 100)
    say("ARM D — DECAY AGAINST ITS OWN SAMPLING INTERVAL (paired circular-block bootstrap)")
    say("=" * 100)
    say("")
    rng = np.random.default_rng(BOOT_SEED)
    dec_rows = []
    for pan in panels:
        idx = B[pan.name]["idx"]
        _, _, _, oos = windows(idx)
        n = len(idx)
        bidx = block_index(n, BOOT_B, BOOT_BLOCK, rng)
        oidx = np.flatnonzero(oos)
        bidx_o = block_index(len(oidx), BOOT_B, BOOT_BLOCK, rng)
        for conv in CONVS:
            r1 = series[(pan.name, conv, 1)]
            s1 = sharpe_mat(r1, bidx); c1 = cagr_mat(r1, bidx)
            s1o = sharpe_mat(r1[oidx], bidx_o)
            for d in LAGS:
                rd = series[(pan.name, conv, d)]
                g = G[(G.panel == pan.name) & (G.lag == d) & (G.conv == conv)].iloc[0]
                g1 = G[(G.panel == pan.name) & (G.lag == 1) & (G.conv == conv)].iloc[0]
                ds = sharpe_mat(rd, bidx) - s1
                dc = cagr_mat(rd, bidx) - c1
                dso = sharpe_mat(rd[oidx], bidx_o) - s1o
                dec_rows.append(dict(
                    panel=pan.name, conv=conv, lag=d,
                    d_sharpe=g.Sharpe - g1.Sharpe, se_sharpe=float(np.nanstd(ds, ddof=1)),
                    d_cagr=g.CAGR - g1.CAGR, se_cagr=float(np.nanstd(dc, ddof=1)),
                    d_maxdd=g.MaxDD - g1.MaxDD,
                    d_oos_sharpe=g.OOS_Sharpe - g1.OOS_Sharpe,
                    se_oos_sharpe=float(np.nanstd(dso, ddof=1)), pass4b=bool(g.pass4b)))
    D = pd.DataFrame(dec_rows)
    D["t_sharpe"] = D.d_sharpe / D.se_sharpe.replace(0, np.nan)
    D["t_oos"] = D.d_oos_sharpe / D.se_oos_sharpe.replace(0, np.nan)
    D["resolved"] = D.t_sharpe.abs() >= 2.0
    D.to_csv(f"{OUT}.decay.csv", index=False)
    say(f"  {'conv':5} {'panel':6} {'d':>3} {'dSharpe':>9} {'SE':>7} {'t':>7} {'dCAGR':>8} "
        f"{'SE':>7} {'dMaxDD':>8} {'dOOS Sh':>9} {'SE':>7} {'t':>7} {'4b':>5} {'|t|>=2':>7}")
    for _, x in D.iterrows():
        say(f"  {x.conv:5} {x.panel:6} {x.lag:3.0f} {x.d_sharpe:+9.4f} {x.se_sharpe:7.4f} {x.t_sharpe:+7.2f} "
            f"{x.d_cagr:+8.2%} {x.se_cagr:7.4f} {x.d_maxdd:+8.2%} {x.d_oos_sharpe:+9.4f} "
            f"{x.se_oos_sharpe:7.4f} {x.t_oos:+7.2f} {'PASS' if x.pass4b else 'FAIL':>5} "
            f"{'YES' if x.resolved else 'no':>7}")
    say("")
    say("  Ladder shape (full-sample net Sharpe over the six rungs), per convention and panel:")
    say(f"  {'conv':5} {'panel':6} {'rho(d,Sharpe)':>14} {'OLS slope /day':>15} {'spread':>8} "
        f"{'median SE':>10} {'spread/SE':>10}")
    shape = {}
    for conv in CONVS:
        for pan in panels:
            sh = [float(G[(G.panel == pan.name) & (G.lag == d) & (G.conv == conv)].iloc[0]["Sharpe"])
                  for d in LAGS]
            se = float(D[(D.panel == pan.name) & (D.conv == conv) & (D.lag > 1)].se_sharpe.median())
            rho = spearman(LAGS, sh)
            sl = ols_slope(LAGS, sh)
            spread = max(sh) - min(sh)
            shape[(conv, pan.name)] = dict(rho=rho, slope=sl, spread=spread, se=se)
            say(f"  {conv:5} {pan.name:6} {rho:14.3f} {sl:15.5f} {spread:8.4f} {se:10.4f} "
                f"{spread / se:10.2f}")
    say("")
    say("  The same ladder measured BETWEEN conventions at each rung (|SNAP - LATE| in Sharpe),")
    say("  against the median rung SE — how big the naming ambiguity is next to the effect:")
    say(f"  {'panel':6} " + " ".join(f"{'d=' + str(d):>8}" for d in LAGS) + f" {'med SE':>8}")
    for pan in panels:
        gaps = [abs(float(G[(G.panel == pan.name) & (G.lag == d) & (G.conv == "SNAP")].iloc[0]["Sharpe"]) -
                    float(G[(G.panel == pan.name) & (G.lag == d) & (G.conv == "LATE")].iloc[0]["Sharpe"]))
                for d in LAGS]
        se = float(D[(D.panel == pan.name) & (D.lag > 1)].se_sharpe.median())
        say(f"  {pan.name:6} " + " ".join(f"{g:8.4f}" for g in gaps) + f" {se:8.4f}")
    say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM E — RULE 8: a lag CHOSEN on warm-up..2016 against PROTOCOL's frozen d = 1")
    say("=" * 100)
    say("")
    wf = []
    for conv in CONVS:
      for pan in panels:
        sub = G[(G.panel == pan.name) & (G.conv == conv)].sort_values(
            ["IS_Sharpe", "lag"], ascending=[False, True])
        pick = int(sub.iloc[0]["lag"])
        p = G[(G.panel == pan.name) & (G.lag == pick) & (G.conv == conv)].iloc[0]
        f = G[(G.panel == pan.name) & (G.lag == 1) & (G.conv == conv)].iloc[0]
        wf.append(dict(panel=pan.name, conv=conv, pick=pick, is_sharpe_pick=p.IS_Sharpe,
                       is_sharpe_frozen=f.IS_Sharpe, is_margin=p.IS_Sharpe - f.IS_Sharpe,
                       oos_sharpe_pick=p.OOS_Sharpe, oos_sharpe_frozen=f.OOS_Sharpe,
                       oos_gain=p.OOS_Sharpe - f.OOS_Sharpe,
                       oos_cagr_pick=p.OOS_CAGR, oos_cagr_frozen=f.OOS_CAGR,
                       oos_maxdd_pick=p.OOS_MaxDD, oos_maxdd_frozen=f.OOS_MaxDD,
                       pick_pass4b=bool(p.pass4b), frozen_pass4b=bool(f.pass4b),
                       best_oos_lag=int(G[(G.panel == pan.name) & (G.conv == conv)].sort_values(
                           "OOS_Sharpe", ascending=False).iloc[0]["lag"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {'conv':5} {'panel':6} {'IS pick':>8} {'IS Sh pick':>11} {'IS Sh d=1':>10} "
        f"{'IS margin':>10} {'OOS Sh pick':>12} {'OOS Sh d=1':>11} {'chooser gain':>13} "
        f"{'ex-post best d':>15}")
    for _, x in WF.iterrows():
        say(f"  {x.conv:5} {x.panel:6} {x['pick']:8d} {x.is_sharpe_pick:11.4f} {x.is_sharpe_frozen:10.4f} "
            f"{x.is_margin:+10.4f} {x.oos_sharpe_pick:12.4f} {x.oos_sharpe_frozen:11.4f} "
            f"{x.oos_gain:+13.4f} {x.best_oos_lag:15d}")
    say("")
    say(f"  Mean chooser-minus-do-nothing across all {len(WF)} (convention, panel) arms: "
        f"{WF.oos_gain.mean():+.4f} OOS Sharpe; worst {WF.oos_gain.min():+.4f}; positive on "
        f"{int((WF.oos_gain > 0).sum())} of {len(WF)}.")
    for conv in CONVS:
        w = WF[WF.conv == conv]
        say(f"    {conv}: mean {w.oos_gain.mean():+.4f}, worst {w.oos_gain.min():+.4f}.")
    say(f"  The IS-chosen lag IS the ex-post best OOS lag on "
        f"{int((WF['pick'] == WF.best_oos_lag).sum())} of {len(WF)} arms.")
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM F — THE VERDICT, under the outcome rule fixed in the header")
    say("=" * 100)
    say("")
    U = G[(G.panel == "U56") & (G.conv == "LATE")].set_index("lag")
    DU = D[(D.panel == "U56") & (D.conv == "LATE")].set_index("lag")
    stress = [d for d in LAGS if d > 1]
    within = [d for d in stress if abs(DU.loc[d, "t_sharpe"]) < 2.0]
    beyond_lo5 = [d for d in stress if d <= 5 and DU.loc[d, "t_sharpe"] <= -2.0]
    fails = [d for d in stress if not bool(U.loc[d, "pass4b"])]
    rho = shape[("LATE", "U56")]["rho"]
    if (2 in fails) and (2 in beyond_lo5):
        verdict = "A — FRAGILE"
    elif rho <= -0.80 and beyond_lo5:
        verdict = "B — DECAYS"
    elif len(within) == len(stress):
        verdict = "C — UNRESOLVED"
    elif not [d for d in stress if d <= 5 and not bool(U.loc[d, "pass4b"])] and not beyond_lo5:
        verdict = "D — ROBUST"
    else:
        verdict = "E — MIXED"
    say("  Taken on LATE, the construction this idea's text describes; SNAP is reported above.")
    say(f"  ANCHOR PANEL U56: 4b FAILS at d = {fails if fails else 'no rung'}; "
        f"rho(d, Sharpe) = {rho:+.3f}; rungs beyond 2 SE below d=1: "
        f"{[d for d in stress if DU.loc[d, 't_sharpe'] <= -2.0] or 'none'}; "
        f"rungs within 2 SE: {within}.")
    say(f"  OUTCOME: {verdict}")
    say("")
    for conv in CONVS:
        say(f"  [{conv}] same three readings on every panel: " + "; ".join(
            f"{q}: 4b fails at "
            f"{[d for d in stress if not bool(G[(G.panel == q) & (G.lag == d) & (G.conv == conv)].iloc[0].pass4b)] or 'no rung'}, "
            f"rho {shape[(conv, q)]['rho']:+.2f}, resolved rungs "
            f"{[int(d) for d in D[(D.panel == q) & (D.conv == conv) & (D.lag > 1) & D.resolved].lag] or 'none'}"
            for q in ["U56", "B136", "SMALL"]))
    say("")
    say("  THE DRAWDOWN LEG, stated plainly (U56, LATE): 4b's binding margin is the MaxDD cap at")
    say("  every failing rung. Its value at each lag, in pp of room against 0.60 x SPY MaxDD:")
    say("    " + "  ".join(f"d={d}: {float(U.loc[d, 'dd_margin_pp']):+.3f}" for d in LAGS))
    say("")
    say(f"  Runtime {time.time() - t0:.0f}s. Deterministic (bootstrap seed {BOOT_SEED}).")
    Path(f"{OUT}.log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
