#!/usr/bin/env python3
"""
Idea 1276 (lane C, 2026-09-18) — does the STITCHED vs SLICED gap change the SIGN of any
COMMITTED CHOOSER RESULT?

THE PREMISE, READ FROM THE RECORD.  Idea 1236 (lane C, 2026-09-18, ARM D) built 12 REALISED
STITCHED books — fold f's IS argmax held through fold f, re-booked on the switch day — and
found the anchor's edge over them runs +0.0331 / +0.0348 / +0.0374 / +0.0417 of Sharpe at
0 / 10 / 25 / 50 bps, against the +0.0209 / +0.0213 / +0.0219 / +0.0230 the record's
FOLD-SLICED accounting publishes.  It concluded that every committed chooser-minus-anchor
figure on this record is a FLOOR.  The queue asks the sharper question: does charging the
switch change any committed chooser VERDICT — its sign, or its own SE?

WHAT 1236 LEFT CONFLATED, AND WHAT THIS RUN SEPARATES.  1236 compared a WHOLE-SPAN Sharpe
(the stitched book) against a MEAN-OF-FOLD-SHARPES (the sliced accounting).  Those two
differ for two unrelated reasons, and only one of them is the switch:

  S1  SLICED       mean over folds of [ S_oos(anchor, fold f, c) - S_oos(pick_f, fold f, c) ]
                   read off CONTINUOUSLY-run books.  This is the record's committed object.
  S2  STITCHED_FREE  one whole-span Sharpe of the REALISED moving book, minus the anchor's,
                   with the INCREMENTAL re-booking turnover at each switch row REBATED.
  S3  STITCHED_PAID  the same realised book paying its own switch turnover.  1236's ARM D.

    AGGREGATION GAP = S2 - S1     mean-of-fold-Sharpes vs whole-span Sharpe.  Not the switch.
    SWITCH CHARGE   = S3 - S2     the re-booking cost, and nothing else.  The queue's object.
    TOTAL GAP       = S3 - S1     what 1236 measured.

  By construction SWITCH CHARGE is EXACTLY 0 at c = 0 bps (gate G5) and EXACTLY 0 for a cell
  that never switches (gate G6).  So any part of 1236's +0.0331 that is present at 0 bps is
  the AGGREGATION gap, not the re-booking cost — and +0.0331 of its +0.0417 is at 0 bps.
  This run states which of the two moves a verdict.

  INCREMENTAL, not gross, re-booking turnover: at a switch row o0 the stitched book turns
  over |w_new - w_held|, but a continuously-run incoming book would itself have turned over
  t_cont(o0) there (0 if o0 is not one of its rebalance days).  The charge rebated in S2 is
  t_stitched(o0) - t_cont_new(o0), so S2 charges the moving book everything a continuous
  book of the same rung would have paid and not one basis point more.

THE VERDICT TEST, STATED BEFORE ANY NUMBER IS READ.  For each cell, SE is the cell's OWN
fold-clustered SE of the sliced per-fold deltas (1214/1224's estimator: SD of the fold
values / sqrt(G)) — "its own SE" in the queue's wording.

    SIGN FLIP (switch)   sign(S3) != sign(S2)          the switch alone flips the verdict
    SIGN FLIP (total)    sign(S3) != sign(S1)          1236's comparison flips the verdict
    SE CROSS (switch)    |S3 - S2| > SE                the switch alone moves it by > 1 SE
    SE CROSS (total)     |S3 - S1| > SE

  PRE-DECLARED OUTCOMES.  (A) THE SWITCH CHANGES VERDICTS — >= 1 cell with SIGN FLIP (switch)
  at the reference rung.  (B) THE SWITCH MOVES BUT DOES NOT FLIP — 0 such flips, >= 1 SE
  CROSS (switch).  (C) THE SWITCH IS IMMATERIAL — neither.  Under (B) or (C) the TOTAL
  column is reported at equal prominence and named for what it is: an ACCOUNTING-SHAPE
  effect, not a cost.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  VERDICT SET  {V_AXIS, V_WIDE, V_POOL}   the record's three committed chooser families
                 V_AXIS  per-ladder IS argmax          3 panels x 4 ladders = 12 cells
                 V_WIDE  1214's widest-IS-spread ladder, then its argmax     3 cells
                 V_POOL  IS argmax over the union of all 19 distinct rungs   3 cells
  COST RUNG    {0, 10, 25, 50} bps        1236's / 931's ladder

  18 cells x 4 rungs = 72 grid points, EVERY ONE published in `.cells.csv`.  No verdict is
  read at a rung other than 10 bps (PROTOCOL rule 2's rung).

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the four ladders; the
folds; the 4a and 4b legs; the IS and OOS windows.  TIE-BREAK in every argmax is FIRST-WINS
in a fixed key order (idea 1202's open question) and is reported, not hidden: `.cells.csv`
carries the count of folds whose argmax was a tie.

PICK CONVENTION — REPORTED AT BOTH VALUES, NOT A THIRD DIAL.  Every one of the 72 grid points
is computed twice and both are published in `.cells.csv`:

  CA  COST-AWARE   the chooser sees the same rung c the book pays.  The realised object: a
                   book that pays its own switch turnover is also chosen knowing its costs.
                   This is the PRIMARY reading and the one the OUTCOME is taken on.
  FZ  FROZEN       the picks are made once at 10 bps and then re-priced at each rung.  This
                   is idea 1224's / 1236's main-grid convention, kept so the record's own
                   committed tables replay exactly (gates G7/G8).

  Nothing is selected on the convention: both censuses are reported side by side, and at the
  reference rung (10 bps) the two are IDENTICAL by construction (gate G8c).  1236's §5 arm
  is the CA row of this grid and replays to 1e-4 at all four rungs (gate G7c).

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W, decide-at-t /
apply-at-t+1 (rule 2), warm-up 260 rows, folds 2013..2026.

PROTOCOL: rule 2 execution; rule 3 baseline (live RULES v2) AND SPY on every book; BOTH KEEP
paths on every stitched curve, every anchor and every rule-8 row; rule 8 walk-forward with
the frozen arm chosen on warm-up..2016-12-31 ONLY and 2017-2026 read once; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_does-the-STITCHED-vs-SLICED-GAP-change-the-SIGN-of-any-COMMITTED-CHOOSER-RESULT_C.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-the-STITCHED-vs-SLICED-GAP-change-the-SIGN-of-any-COMMITTED-CHOOSER-RESULT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
REF_COST = 10.0
COSTS = [0.0, 10.0, 25.0, 50.0]                 # DIAL 2
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
ANCHOR_RUNG = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}
LADS = ["N", "H", "GROSS", "CADENCE"]
FAMILIES = ["V_AXIS", "V_WIDE", "V_POOL"]       # DIAL 1
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
# Idea 1236's committed ARM D table (12 stitched books), replayed by gate G7.
C1236_ARMD = {0.0: 0.0331, 10.0: 0.0348, 25.0: 0.0374, 50.0: 0.0417}
C1236_SWITCHES = 43
C1236_AXIS_SLICED = {0.0: 0.0209, 10.0: 0.0213, 25.0: 0.0219, 50.0: 0.0230}   # FROZEN picks
# Idea 1236 §5, the cost-aware chooser: sliced delta at 0/10/25/50 bps.
C1236_AXIS_CA = {0.0: 0.0157, 10.0: 0.0213, 25.0: 0.0159, 50.0: 0.0052}
DRIFT_TOL = 3e-3     # 1236 G10: one extra nightly trading day moves a committed level 2.6e-3

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ==================================================================== panels / runner (1224/1236's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


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


def build1(pan, N, H, freq, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; row t is the APPLICATION-time weight."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, reb):
    """1224's fast runner.  Returns (GROSS daily returns, one-way turnover at each row).
    Costs are applied afterwards as r(c) = gross - turn * c / 1e4 (gates G1/G2)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


def at_cost(gr, tu, c):
    return gr - tu * c / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def cluster_se(vals):
    """One value per fold -> SD / sqrt(G), 1214/1224's fold-clustered estimator."""
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if len(v) < 2:
        return float(v.mean()) if len(v) else np.nan, np.nan, len(v)
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v))), len(v)


# ==================================================================== world construction
def make_panels():
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    return panels, inv, pxU, pxB, pxS


def build_books(pan):
    frames = {}
    for N in LAD["N"]:
        frames[(N, A_H, "W")] = None
    for H in LAD["H"]:
        frames[(A_N, H, "W")] = None
    frames[(A_N, A_H, "M")] = None
    for key in list(frames):
        frames[key] = build1(pan, key[0], key[1], key[2])
    af = frames[(A_N, A_H, "W")]
    gb, tb, rb = {}, {}, {}
    for N in LAD["N"]:
        gb[("N", N)], tb[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], pan.seg["W"])
        rb[("N", N)] = ("W", (N, A_H, "W"), A_G)
    for H in LAD["H"]:
        gb[("H", H)], tb[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], pan.seg["W"])
        rb[("H", H)] = ("W", (A_N, H, "W"), A_G)
    for f in LAD["CADENCE"]:
        fr = af if f == "W" else frames[(A_N, A_H, "M")]
        gb[("CADENCE", f)], tb[("CADENCE", f)] = nrun(pan, A_G * fr, pan.seg[f])
        rb[("CADENCE", f)] = (f, (A_N, A_H, f), A_G)
    for g in LAD["GROSS"]:
        gb[("GROSS", g)], tb[("GROSS", g)] = nrun(pan, g * af, pan.seg["W"])
        rb[("GROSS", g)] = ("W", (A_N, A_H, "W"), g)
    return frames, gb, tb, rb


def make_folds(pan):
    yrs = pan.idx.year.values
    out = []
    for y in FOLD_YEARS:
        oo = np.flatnonzero(yrs == y)
        oo = oo[oo >= pan.i0]
        if len(oo) < 60:
            continue
        lo, hi = pan.i0, int(oo[0])
        if hi - lo < 252:
            continue
        out.append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
    return out


# The pooled rung set: every distinct book.  The anchor is ONE book reached by all four
# ladders (gate G4), so it is kept once, under its N-ladder key.
def pool_keys():
    ks = []
    for lad in LADS:
        for r in LAD[lad]:
            if r == ANCHOR_RUNG[lad] and lad != "N":
                continue                       # duplicate of ("N", 20)
            ks.append((lad, r))
    return ks


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1276 (lane C, 2026-09-18) — does the STITCHED vs SLICED gap change the SIGN of")
    say("any COMMITTED CHOOSER RESULT?")
    say("=" * 108)
    say("")
    say("  S1 SLICED        mean over folds of [S_oos(anchor,f,c) - S_oos(pick_f,f,c)], continuous books")
    say("  S2 STITCHED_FREE whole-span Sharpe of the REALISED moving book (incremental switch turnover")
    say("                   rebated), anchor minus book")
    say("  S3 STITCHED_PAID the same book paying its own switch turnover  (1236's ARM D)")
    say("  AGGREGATION = S2-S1   SWITCH CHARGE = S3-S2   TOTAL = S3-S1")
    say("  SE = the cell's OWN fold-clustered SE of the sliced per-fold deltas.")
    say("  OUTCOMES: (A) >=1 SIGN FLIP from the switch  (B) 0 flips, >=1 SE cross from the switch")
    say("            (C) neither — the switch is immaterial and the gap is accounting shape.")

    # ---------------------------------------------------------------- panels and rung books
    say("")
    say("=" * 108)
    say("ARM A — PANELS, RUNG BOOKS, MACHINERY GATES")
    say("=" * 108)
    panels, inv, pxU, pxB, pxS = make_panels()
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0); SPY benchmark only.")
    say(f"  TAPE: U56 ends {pxU.index[-1].date()}, B136 {pxB.index[-1].date()}, "
        f"SMALL {pxS.index[-1].date()}.")

    booked, turned, rebs, bench, frames_all, folds = {}, {}, {}, {}, {}, {}
    for pan in panels:
        frames, gb, tb, rb = build_books(pan)
        frames_all[pan.name] = frames
        booked[pan.name], turned[pan.name], rebs[pan.name] = gb, tb, rb
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        folds[pan.name] = make_folds(pan)
        say(f"    {pan.name:6s} {len(gb)} rung books, {len(folds[pan.name])} folds "
            f"({folds[pan.name][0][0]}..{folds[pan.name][-1][0]}).")

    POOL = pool_keys()
    say(f"  POOLED RUNG SET: {len(POOL)} distinct books "
        f"(6 N + 4 H + 10 GROSS + 2 CADENCE = 22 keys, 3 anchor duplicates removed).")

    # ---- machinery gates
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    gr, tu = nrun(pan, Wt, pan.seg["W"])
    g1 = max(float(np.nanmax(np.abs(
        backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=c, freq="W")["returns"].values[WARMUP:]
        - at_cost(gr, tu, c)[WARMUP:]))) for c in COSTS)
    gate("G1 fast runner == engine.backtest at EVERY cost rung", g1, 1e-10, g1 < 1e-10)
    BOOKKEY = list(booked["U56"].keys())
    gz = float(max(np.abs(at_cost(booked["U56"][k], turned["U56"][k], 0.0)
                          - booked["U56"][k]).max() for k in BOOKKEY))
    gate("G2 the 0 bps rung is the gross book exactly", gz, 0.0, gz == 0.0)
    lmv = mdd(bench["U56"]["live"][WARMUP:])
    gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", lmv,
         LIVE_MAXDD_COMMITTED, abs(lmv - LIVE_MAXDD_COMMITTED) < 5e-4)
    anc = [booked["U56"][(l, ANCHOR_RUNG[l])] for l in LADS]
    anct = [turned["U56"][(l, ANCHOR_RUNG[l])] for l in LADS]
    g4 = float(max(max(np.abs(a - anc[0]).max() for a in anc),
                   max(np.abs(a - anct[0]).max() for a in anct)))
    gate("G4 the anchor rung of all four ladders is ONE book, returns AND turnover", g4, 0.0,
         g4 == 0.0)
    nf = {p: len(folds[p]) for p in folds}
    gate("G9 folds tile all three panels", float(min(nf.values())), 10.0,
         min(nf.values()) >= 10)
    say(f"    G1 {g1:.3e}   G2 {gz:.3e}   G3 live U56 MaxDD {lmv:.4%}   G4 {g4:.3e}   "
        f"G9 folds {nf}")

    # ---------------------------------------------------------------- choosers
    def is_sharpe(p, key, lo, hi, c):
        return sharpe(at_cost(booked[p][key], turned[p][key], c)[lo:hi])

    def argmax_over(p, keys, lo, hi, c):
        """FIRST-WINS tie-break in the given fixed key order (idea 1202); also returns the
        number of keys tied at the winning IS Sharpe."""
        best, bk = -np.inf, None
        vals = []
        for k in keys:
            s = is_sharpe(p, k, lo, hi, c)
            vals.append(s)
            if np.isfinite(s) and s > best:
                best, bk = s, k
        ties = int(sum(1 for s in vals if np.isfinite(s) and abs(s - best) < 1e-12))
        return bk, ties

    def widest_ladder(p, lo, hi, c):
        spr = {}
        for lad in LADS:
            v = [is_sharpe(p, (lad, r), lo, hi, c) for r in LAD[lad]]
            v = [x for x in v if np.isfinite(x)]
            spr[lad] = (max(v) - min(v)) if len(v) > 1 else -np.inf
        return max(LADS, key=lambda k: spr[k])

    def picks_for(p, fam, lad, c):
        """Per-fold pick sequence for one cell.  Returns [(year, lo, hi, o0, o1, key, ties)]."""
        out = []
        for (y, lo, hi, o0, o1) in folds[p]:
            if fam == "V_AXIS":
                k, ties = argmax_over(p, [(lad, r) for r in LAD[lad]], lo, hi, c)
            elif fam == "V_WIDE":
                wl = widest_ladder(p, lo, hi, c)
                k, ties = argmax_over(p, [(wl, r) for r in LAD[wl]], lo, hi, c)
            else:
                k, ties = argmax_over(p, POOL, lo, hi, c)
            out.append((y, lo, hi, o0, o1, k, ties))
        return out

    def stitched(pan, seq, folds_used=None):
        """Realised moving book: fold f's pick held through fold f, re-booked on the switch
        day.  Returns (gross, turn_paid, turn_free, span, n_switch, switch_rows)."""
        p = pan.name
        use = [s for s in seq if folds_used is None or s[0] in folds_used]
        span = (use[0][3], use[-1][4])
        W = np.zeros_like(pan.rets)
        reb, prev, nsw, swrows = [], None, 0, []
        for (y, lo, hi, o0, o1, key, _ties) in use:
            freq, fkey, g = rebs[p][key]
            W[o0:o1] = g * frames_all[p][fkey][o0:o1]
            days = [d for d in pan.seg[freq] if o0 <= d < o1]
            if prev is not None and key != prev:
                nsw += 1
                if o0 not in days:
                    days = [o0] + days
                swrows.append((o0, key))
            elif prev is None and o0 not in days:
                days = [o0] + days
            reb.extend(days)
            prev = key
        reb = np.array(sorted(set(reb)), dtype=np.int64)
        reb = reb[(reb >= span[0]) & (reb < span[1])]
        gs, ts = nrun(pan, W, reb)
        # INCREMENTAL rebate: at each switch row, what a continuously-run incoming book would
        # itself have turned over there.
        tfree = ts.copy()
        for (o0, key) in swrows:
            tfree[o0] = min(ts[o0], turned[p][key][o0])
        return gs, ts, tfree, span, nsw, swrows

    say("")
    say("=" * 108)
    say("ARM B — THE 72 GRID POINTS (18 cells x 4 cost rungs), each under BOTH pick conventions")
    say("=" * 108)

    def cell_stats(pan, fam, lad, c_eval, c_choice):
        p = pan.name
        seq = picks_for(p, fam, lad, c_choice)
        gs, ts, tfree, span, nsw, swrows = stitched(pan, seq)
        lo, hi = span
        ka = ("N", A_N)
        ga, ta = booked[p][ka], turned[p][ka]
        per = []
        for (y, flo, fhi, o0, o1, key, _t) in seq:
            sp = sharpe(at_cost(booked[p][key], turned[p][key], c_eval)[o0:o1])
            sa = sharpe(at_cost(ga, ta, c_eval)[o0:o1])
            per.append(sa - sp)
        S1, SE, G = cluster_se(per)
        r_paid = at_cost(gs, ts, c_eval)[lo:hi]
        r_free = at_cost(gs, tfree, c_eval)[lo:hi]
        r_anc = at_cost(ga, ta, c_eval)[lo:hi]
        Sa = sharpe(r_anc)
        S2, S3 = Sa - sharpe(r_free), Sa - sharpe(r_paid)
        bm, lv = bmpack(pan.spy[lo:hi]), bmpack(bench[p]["live"][lo:hi])
        k4a_s, k4b_s, ms, h1s, h2s = keep_paths(r_paid, bm, lv)
        k4a_a, k4b_a, ma, h1a, h2a = keep_paths(r_anc, bm, lv)
        return dict(
            n_folds=G, n_switch=nsw, n_tie_folds=int(sum(1 for x in seq if x[6] > 1)),
            seq="|".join(f"{x[0]}:{x[5][0]}={x[5][1]}" for x in seq),
            S1_sliced=S1, SE_sliced=SE, S2_stitched_free=S2, S3_stitched_paid=S3,
            AGGREGATION=S2 - S1, SWITCH_CHARGE=S3 - S2, TOTAL=S3 - S1,
            FLIP_switch=bool(np.sign(S3) != np.sign(S2)),
            FLIP_total=bool(np.sign(S3) != np.sign(S1)),
            SEcross_switch=bool(np.isfinite(SE) and abs(S3 - S2) > SE),
            SEcross_total=bool(np.isfinite(SE) and abs(S3 - S1) > SE),
            turn_stitched=annturn(ts, lo, hi), turn_anchor=annturn(ta, lo, hi),
            switch_turn=float(sum(ts[o] - tfree[o] for o, _k in swrows)),
            CAGR_stitched=ms["CAGR"], Sharpe_stitched=ms["Sharpe"],
            MaxDD_stitched=ms["MaxDD"], H1_stitched=h1s, H2_stitched=h2s,
            CAGR_anchor=ma["CAGR"], Sharpe_anchor=ma["Sharpe"],
            MaxDD_anchor=ma["MaxDD"], H1_anchor=h1a, H2_anchor=h2a,
            SPY_CAGR=bm["CAGR"], SPY_Sharpe=bm["Sharpe"], SPY_MaxDD=bm["MaxDD"],
            SPY_H1=bm["H1"], SPY_H2=bm["H2"],
            LIVE_CAGR=lv["CAGR"], LIVE_Sharpe=lv["Sharpe"], LIVE_MaxDD=lv["MaxDD"],
            k4a_stitched=k4a_s, k4b_stitched=k4b_s, k4a_anchor=k4a_a, k4b_anchor=k4b_a)

    cells = []
    for pan in panels:
        for fam in FAMILIES:
            for lad in (LADS if fam == "V_AXIS" else [None]):
                for c in COSTS:
                    for pc, cch in (("CA", c), ("FZ", REF_COST)):
                        d = cell_stats(pan, fam, lad, c, cch)
                        d.update(panel=pan.name, FAMILY=fam, ladder=(lad or "-"),
                                 COST_BPS=c, PICKS=pc)
                        cells.append(d)
    CE_ALL = pd.DataFrame(cells)
    CE_ALL.to_csv(f"{OUT}.cells.csv", index=False)
    CE = CE_ALL[CE_ALL.PICKS == "CA"].reset_index(drop=True)
    CZ = CE_ALL[CE_ALL.PICKS == "FZ"].reset_index(drop=True)

    say("")
    say("   PRIMARY (CA — chooser sees the rung it pays).  All 72 grid points:")
    say("   panel  family  ladder    cost  sw   S1 SLICED    SE      S2 FREE     S3 PAID  "
        "  AGGREG    SWITCH     TOTAL  flipS flipT xSE")
    for _, r in CE.iterrows():
        say(f"   {r.panel:6s} {r.FAMILY:7s} {r.ladder:8s} {int(r.COST_BPS):4d} {int(r.n_switch):3d} "
            f"{r.S1_sliced:+.4f} {r.SE_sliced:7.4f}  {r.S2_stitched_free:+.4f}  "
            f"{r.S3_stitched_paid:+.4f}  {r.AGGREGATION:+.4f}  {r.SWITCH_CHARGE:+.4f}  "
            f"{r.TOTAL:+.4f}   {'Y' if r.FLIP_switch else '.'}     "
            f"{'Y' if r.FLIP_total else '.'}    {'Y' if r.SEcross_switch else '.'}")
    say("")
    say("   FROZEN (FZ — 1224/1236's convention: picks made once at 10 bps, re-priced).  "
        "All 72 grid points:")
    say("   panel  family  ladder    cost  sw   S1 SLICED    SE      S2 FREE     S3 PAID  "
        "  AGGREG    SWITCH     TOTAL  flipS flipT xSE")
    for _, r in CZ.iterrows():
        say(f"   {r.panel:6s} {r.FAMILY:7s} {r.ladder:8s} {int(r.COST_BPS):4d} {int(r.n_switch):3d} "
            f"{r.S1_sliced:+.4f} {r.SE_sliced:7.4f}  {r.S2_stitched_free:+.4f}  "
            f"{r.S3_stitched_paid:+.4f}  {r.AGGREGATION:+.4f}  {r.SWITCH_CHARGE:+.4f}  "
            f"{r.TOTAL:+.4f}   {'Y' if r.FLIP_switch else '.'}     "
            f"{'Y' if r.FLIP_total else '.'}    {'Y' if r.SEcross_switch else '.'}")

    # ---- construction gates on the decomposition (both conventions)
    z = CE_ALL[CE_ALL.COST_BPS == 0.0]
    g5 = float(np.abs(z.SWITCH_CHARGE).max())
    gate("G5 SWITCH CHARGE is EXACTLY 0 at 0 bps (by construction)", g5, 0.0, g5 == 0.0)
    ns = CE_ALL[CE_ALL.n_switch == 0]
    g6 = float(np.abs(ns.SWITCH_CHARGE).max()) if len(ns) else 0.0
    gate("G6 a cell that never switches has SWITCH CHARGE 0 at every rung", g6, 0.0, g6 == 0.0)
    g6b = float((CE_ALL.switch_turn < -1e-12).sum())
    gate("G6b the incremental switch turnover is never negative", g6b, 0.0, g6b == 0.0)
    a_ = CE[CE.COST_BPS == REF_COST].set_index(["panel", "FAMILY", "ladder"])
    b_ = CZ[CZ.COST_BPS == REF_COST].set_index(["panel", "FAMILY", "ladder"])
    g8c = float(np.abs(a_.S3_stitched_paid - b_.S3_stitched_paid).max())
    gate("G8c the two pick conventions are IDENTICAL at the reference rung", g8c, 0.0,
         g8c == 0.0)

    # ---- G7/G8: replay the record's own committed tables, each against its own convention
    axZ = CZ[CZ.FAMILY == "V_AXIS"]
    axC = CE[CE.FAMILY == "V_AXIS"]
    armd = {c: float(axZ[axZ.COST_BPS == c].S3_stitched_paid.mean()) for c in COSTS}
    slZ = {c: float(axZ[axZ.COST_BPS == c].S1_sliced.mean()) for c in COSTS}
    slC = {c: float(axC[axC.COST_BPS == c].S1_sliced.mean()) for c in COSTS}
    nsw12 = int(axZ[axZ.COST_BPS == REF_COST].n_switch.sum())
    g7 = max(abs(armd[c] - C1236_ARMD[c]) for c in COSTS)
    gate("G7 1236's ARM D mean d_Sharpe replays on the 12 V_AXIS books (FROZEN picks)", g7,
         DRIFT_TOL, g7 < DRIFT_TOL)
    gate("G7b 1236's 43 fold-boundary switches replay", float(nsw12), float(C1236_SWITCHES),
         nsw12 == C1236_SWITCHES)
    g7c = max(abs(slC[c] - C1236_AXIS_CA[c]) for c in COSTS)
    gate("G7c 1236's §5 cost-aware chooser row replays on the CA arm", g7c, DRIFT_TOL,
         g7c < DRIFT_TOL)
    g8 = max(abs(slZ[c] - C1236_AXIS_SLICED[c]) for c in COSTS)
    gate("G8 1224/1236's P_AXIS SLICED delta replays on the same 12 cells (FROZEN picks)", g8,
         DRIFT_TOL, g8 < DRIFT_TOL)
    say("")
    say("   REPLAY 1236 ARM D   (12 V_AXIS, FZ, PAID): " +
        "  ".join(f"@{int(c)} {armd[c]:+.4f} (cmt {C1236_ARMD[c]:+.4f})" for c in COSTS))
    say("   REPLAY 1224 SLICED  (12 V_AXIS, FZ):       " +
        "  ".join(f"@{int(c)} {slZ[c]:+.4f} (cmt {C1236_AXIS_SLICED[c]:+.4f})" for c in COSTS))
    say("   REPLAY 1236 §5      (12 V_AXIS, CA):       " +
        "  ".join(f"@{int(c)} {slC[c]:+.4f} (cmt {C1236_AXIS_CA[c]:+.4f})" for c in COSTS))
    say(f"   Switches across the 12 V_AXIS books: {nsw12} (1236 committed {C1236_SWITCHES}).")

    # ---------------------------------------------------------------- the census
    say("")
    say("=" * 108)
    say("ARM C — HOW MANY VERDICTS MOVE, BY RUNG AND BY PICK CONVENTION")
    say("=" * 108)
    say("")
    say("   picks cost   cells  FLIP(switch)  FLIP(total)  SEcross(switch)  SEcross(total)  "
        "mean SWITCH   mean AGGREG")
    cen = []
    for pc, D in (("CA", CE), ("FZ", CZ)):
        for c in COSTS:
            s = D[D.COST_BPS == c]
            row = dict(PICKS=pc, COST_BPS=c, n_cells=len(s),
                       flip_switch=int(s.FLIP_switch.sum()), flip_total=int(s.FLIP_total.sum()),
                       xse_switch=int(s.SEcross_switch.sum()),
                       xse_total=int(s.SEcross_total.sum()),
                       mean_switch=float(s.SWITCH_CHARGE.mean()),
                       mean_aggreg=float(s.AGGREGATION.mean()),
                       mean_S1=float(s.S1_sliced.mean()),
                       mean_S3=float(s.S3_stitched_paid.mean()))
            cen.append(row)
            say(f"   {pc:5s} {int(c):4d}   {len(s):5d}  {row['flip_switch']:12d}  "
                f"{row['flip_total']:11d}  {row['xse_switch']:15d}  {row['xse_total']:14d}  "
                f"{row['mean_switch']:+.4f}    {row['mean_aggreg']:+.4f}")
    CN = pd.DataFrame(cen)
    CN.to_csv(f"{OUT}.census.csv", index=False)

    say("")
    say("   BY FAMILY at the reference rung (10 bps; the two conventions coincide there):")
    fam_rows = []
    for fam in FAMILIES:
        s = CE[(CE.COST_BPS == REF_COST) & (CE.FAMILY == fam)]
        fam_rows.append(dict(FAMILY=fam, n_cells=len(s), switches=int(s.n_switch.sum()),
                             mean_S1=float(s.S1_sliced.mean()),
                             mean_S3=float(s.S3_stitched_paid.mean()),
                             mean_switch=float(s.SWITCH_CHARGE.mean()),
                             mean_aggreg=float(s.AGGREGATION.mean()),
                             flip_switch=int(s.FLIP_switch.sum()),
                             flip_total=int(s.FLIP_total.sum()),
                             xse_switch=int(s.SEcross_switch.sum()),
                             xse_total=int(s.SEcross_total.sum()),
                             anchor_wins_sliced=int((s.S1_sliced > 0).sum()),
                             anchor_wins_paid=int((s.S3_stitched_paid > 0).sum())))
        r = fam_rows[-1]
        say(f"     {fam:7s} {r['n_cells']:2d} cells, {r['switches']:3d} switches;  "
            f"S1 {r['mean_S1']:+.4f} -> S3 {r['mean_S3']:+.4f}  "
            f"(switch {r['mean_switch']:+.4f}, aggregation {r['mean_aggreg']:+.4f});  "
            f"anchor wins {r['anchor_wins_sliced']}/{r['n_cells']} sliced -> "
            f"{r['anchor_wins_paid']}/{r['n_cells']} paid;  flips {r['flip_switch']}/"
            f"{r['flip_total']}, SE crosses {r['xse_switch']}/{r['xse_total']}")
    pd.DataFrame(fam_rows).to_csv(f"{OUT}.byfamily.csv", index=False)

    # ---------------------------------------------------------------- KEEP paths
    say("")
    say("=" * 108)
    say("ARM D — BOTH KEEP PATHS on every realised book (PROTOCOL rule 4)")
    say("=" * 108)
    say("")
    for c in COSTS:
        s = CE[CE.COST_BPS == c]
        say(f"   @{int(c):3d} bps   STITCHED books: 4a {int(s.k4a_stitched.sum())} of {len(s)}, "
            f"4b {int(s.k4b_stitched.sum())} of {len(s)};   ANCHOR books: "
            f"4a {int(s.k4a_anchor.sum())}, 4b {int(s.k4b_anchor.sum())}.")
    say("")
    say("   Best stitched book by full-span Sharpe at 10 bps, and the anchor beside it:")
    s = CE[CE.COST_BPS == REF_COST].sort_values("Sharpe_stitched", ascending=False)
    for _, r in s.head(4).iterrows():
        say(f"     {r.panel:6s} {r.FAMILY:7s} {r.ladder:8s}  stitched {r.CAGR_stitched:7.2%} / "
            f"{r.Sharpe_stitched:6.4f} / {r.MaxDD_stitched:7.2%} (H {r.H1_stitched:.4f}/"
            f"{r.H2_stitched:.4f})  4a {'T' if r.k4a_stitched else 'F'} "
            f"4b {'T' if r.k4b_stitched else 'F'}")
    for _, r in s.head(1).iterrows():
        say(f"     {r.panel:6s} ANCHOR            {r.CAGR_anchor:7.2%} / {r.Sharpe_anchor:6.4f} / "
            f"{r.MaxDD_anchor:7.2%} (H {r.H1_anchor:.4f}/{r.H2_anchor:.4f})  "
            f"4a {'T' if r.k4a_anchor else 'F'} 4b {'T' if r.k4b_anchor else 'F'}")
        say(f"     {r.panel:6s} SPY               {r.SPY_CAGR:7.2%} / {r.SPY_Sharpe:6.4f} / "
            f"{r.SPY_MaxDD:7.2%} (H {r.SPY_H1:.4f}/{r.SPY_H2:.4f})")
        say(f"     {r.panel:6s} LIVE RULES v2     {r.LIVE_CAGR:7.2%} / {r.LIVE_Sharpe:6.4f} / "
            f"{r.LIVE_MaxDD:7.2%}")

    # ---------------------------------------------------------------- rule 8
    say("")
    say("=" * 108)
    say("ARM E — PROTOCOL RULE 8 (2017-2026 read once; the FROZEN arm chosen on <=2016 only)")
    say("=" * 108)
    say("")
    say("   Three arms over the SAME OOS span.  STITCH_OOS re-picks at each OOS fold from data")
    say("   strictly before that fold (causal).  FROZEN picks once on warm-up..2016-12-31 and")
    say("   holds.  ANCHOR is the committed 2026-09-04 book, which never moves.")
    wf = []
    for pan in panels:
        p = pan.name
        i1 = int(pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        hi = len(pan.rets)
        oosy = [y for (y, *_r) in folds[p] if y >= 2017]
        bm = bmpack(pan.spy[i1:hi])
        lv = bmpack(bench[p]["live"][i1:hi])
        bmF = bmpack(pan.spy[pan.i0:hi])
        lvF = bmpack(bench[p]["live"][pan.i0:hi])
        for fam in FAMILIES:
            for lad in (LADS if fam == "V_AXIS" else [None]):
              for c in COSTS:
                for pc, cch in (("CA", c), ("FZ", REF_COST)):
                    seq = picks_for(p, fam, lad, cch)
                    gs, ts, tfree, span, nsw, _sw = stitched(pan, seq, folds_used=set(oosy))
                    lo2, hi2 = span
                    # FROZEN: choose once on warm-up..2016-12-31
                    if fam == "V_AXIS":
                        fk, _t = argmax_over(p, [(lad, r) for r in LAD[lad]], pan.i0, i1, cch)
                    elif fam == "V_WIDE":
                        wl = widest_ladder(p, pan.i0, i1, cch)
                        fk, _t = argmax_over(p, [(wl, r) for r in LAD[wl]], pan.i0, i1, cch)
                    else:
                        fk, _t = argmax_over(p, POOL, pan.i0, i1, cch)
                    arms = {
                        "STITCH_OOS": (at_cost(gs, ts, c)[lo2:hi2], annturn(ts, lo2, hi2), "stitched", nsw),
                        "FROZEN": (at_cost(booked[p][fk], turned[p][fk], c)[lo2:hi2],
                                   annturn(turned[p][fk], lo2, hi2), f"{fk[0]}={fk[1]}", 0),
                        "ANCHOR": (at_cost(booked[p][("N", A_N)], turned[p][("N", A_N)], c)[lo2:hi2],
                                   annturn(turned[p][("N", A_N)], lo2, hi2), f"N={A_N}", 0),
                    }
                    bm2 = bmpack(pan.spy[lo2:hi2])
                    lv2 = bmpack(bench[p]["live"][lo2:hi2])
                    for arm, (r, tn, rung, nn) in arms.items():
                        k4a, k4b, m, h1, h2 = keep_paths(r, bm2, lv2)
                        if arm == "STITCH_OOS":
                            rf = at_cost(gs, tfree, c)[lo2:hi2]
                            sw_cost = sharpe(rf) - sharpe(r)
                        else:
                            sw_cost = 0.0
                        wf.append(dict(panel=p, FAMILY=fam, ladder=(lad or "-"), COST_BPS=c,
                                       PICKS=pc, arm=arm, rung=rung, n_switch=nn,
                                       ann_turnover=tn,
                                       OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                                       OOS_MaxDD=m["MaxDD"], OOS_H1=h1, OOS_H2=h2,
                                       OOS_switch_cost_Sharpe=sw_cost,
                                       SPY_OOS_CAGR=bm2["CAGR"], SPY_OOS_Sharpe=bm2["Sharpe"],
                                       SPY_OOS_MaxDD=bm2["MaxDD"],
                                       LIVE_OOS_CAGR=lv2["CAGR"], LIVE_OOS_Sharpe=lv2["Sharpe"],
                                       LIVE_OOS_MaxDD=lv2["MaxDD"],
                                       k4a_OOS=k4a, k4b_OOS=k4b))
        say(f"   BENCHMARKS {p:6s} OOS 2017-2026: SPY {bm['CAGR']:.2%} / {bm['Sharpe']:.4f} / "
            f"{bm['MaxDD']:.2%} (H {bm['H1']:.4f}/{bm['H2']:.4f});  LIVE RULES v2 "
            f"{lv['CAGR']:.2%} / {lv['Sharpe']:.4f} / {lv['MaxDD']:.2%} "
            f"(H {lv['H1']:.4f}/{lv['H2']:.4f});  FULL SPY {bmF['CAGR']:.2%} / "
            f"{bmF['Sharpe']:.4f} / {bmF['MaxDD']:.2%}, LIVE {lvF['CAGR']:.2%} / "
            f"{lvF['Sharpe']:.4f} / {lvF['MaxDD']:.2%}.")
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say(f"   RULE-8 ROWS: {len(WF)}  (3 panels x 6 cells x 4 cost rungs x 2 pick conventions"
        f" x 3 arms).")
    say("")
    say("   arm          rows   4a   4b    mean OOS CAGR / Sharpe / MaxDD    mean turnover")
    for arm in ("STITCH_OOS", "FROZEN", "ANCHOR"):
        s = WF[(WF.arm == arm) & (WF.PICKS == "CA")]
        say(f"   {arm:11s} {len(s):5d} {int(s.k4a_OOS.sum()):4d} {int(s.k4b_OOS.sum()):4d}    "
            f"{s.OOS_CAGR.mean():7.2%} / {s.OOS_Sharpe.mean():6.4f} / {s.OOS_MaxDD.mean():7.2%}"
            f"    {s.ann_turnover.mean():8.3f}")
    say("")
    say("   OOS ANCHOR-MINUS-STITCHED Sharpe by cost rung (the rule-8 form of the headline):")
    for c in COSTS:
        Q = WF[(WF.COST_BPS == c) & (WF.PICKS == "CA")]
        ix = ["panel", "FAMILY", "ladder"]
        a = Q[Q.arm == "ANCHOR"].set_index(ix).OOS_Sharpe
        st = Q[Q.arm == "STITCH_OOS"].set_index(ix).OOS_Sharpe
        fr = Q[Q.arm == "FROZEN"].set_index(ix).OOS_Sharpe
        swc = Q[Q.arm == "STITCH_OOS"].OOS_switch_cost_Sharpe.mean()
        say(f"     @{int(c):3d} bps  anchor - stitched {float((a-st).mean()):+.4f}   "
            f"anchor - frozen {float((a-fr).mean()):+.4f}   "
            f"OOS switch cost alone {swc:+.4f}")
    say("")
    say("   Every OOS 4b pass, by arm and cell:")
    pk = WF[WF.k4b_OOS & (WF.PICKS == "CA")]
    if len(pk) == 0:
        say("     NONE.")
    else:
        for _, r in pk.iterrows():
            say(f"     {r.panel:6s} {r.FAMILY:7s} {r.ladder:8s} @{int(r.COST_BPS):3d} {r.arm:11s} "
                f"{r.rung:10s} {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / {r.OOS_MaxDD:7.2%}  "
                f"vs SPY {r.SPY_OOS_CAGR:7.2%} / {r.SPY_OOS_Sharpe:6.4f} / {r.SPY_OOS_MaxDD:7.2%}")
        say(f"     DISTINCT realised books among the {len(pk)} OOS 4b passes: "
            f"{pk.groupby(['panel','arm','rung']).ngroups}.")

    # ---------------------------------------------------------------- the answer
    say("")
    say("=" * 108)
    say("THE ANSWER")
    say("=" * 108)
    ref = CE[CE.COST_BPS == REF_COST]
    fs, xs = int(ref.FLIP_switch.sum()), int(ref.SEcross_switch.sum())
    ft, xt = int(ref.FLIP_total.sum()), int(ref.SEcross_total.sum())
    if fs >= 1:
        outcome = "A_SWITCH_CHANGES_VERDICTS"
    elif xs >= 1:
        outcome = "B_SWITCH_MOVES_BUT_DOES_NOT_FLIP"
    else:
        outcome = "C_SWITCH_IMMATERIAL"
    say("")
    say(f"  OUTCOME: {outcome}")
    say(f"  At {int(REF_COST)} bps, of {len(ref)} committed chooser cells: "
        f"{fs} change SIGN from the SWITCH alone, {xs} cross their own SE from the SWITCH alone.")
    say(f"  Under 1236's TOTAL comparison (which also carries the aggregation shape): "
        f"{ft} sign changes, {xt} SE crossings.")
    zr = CZ[CZ.COST_BPS == REF_COST]
    say(f"  FROZEN-PICK convention at the same rung (identical by construction, gate G8c): "
        f"{int(zr.FLIP_switch.sum())} / {int(zr.SEcross_switch.sum())} switch, "
        f"{int(zr.FLIP_total.sum())} / {int(zr.SEcross_total.sum())} total.")
    say("  Across ALL 144 grid points (both conventions, all four rungs): "
        f"{int(CE_ALL.FLIP_switch.sum())} switch sign changes, "
        f"{int(CE_ALL.SEcross_switch.sum())} switch SE crossings, "
        f"{int(CE_ALL.FLIP_total.sum())} total sign changes, "
        f"{int(CE_ALL.SEcross_total.sum())} total SE crossings.")
    say(f"  Mean SWITCH CHARGE {float(ref.SWITCH_CHARGE.mean()):+.4f} of Sharpe; "
        f"mean AGGREGATION gap {float(ref.AGGREGATION.mean()):+.4f}; ratio "
        f"{abs(float(ref.SWITCH_CHARGE.mean()))/max(abs(float(ref.AGGREGATION.mean())),1e-12):.4f}.")
    mx = ref.loc[ref.SWITCH_CHARGE.abs().idxmax()]
    say(f"  Largest single SWITCH CHARGE: {mx.panel} {mx.FAMILY} {mx.ladder} "
        f"{mx.SWITCH_CHARGE:+.4f} on {int(mx.n_switch)} switches "
        f"({mx.switch_turn:.4f} of incremental one-way turnover over the span).")
    VD = pd.DataFrame([dict(OUTCOME=outcome, ref_cost=REF_COST, n_cells=len(ref),
                            flip_switch=fs, xse_switch=xs, flip_total=ft, xse_total=xt,
                            mean_switch=float(ref.SWITCH_CHARGE.mean()),
                            mean_aggreg=float(ref.AGGREGATION.mean()),
                            mean_S1=float(ref.S1_sliced.mean()),
                            mean_S3=float(ref.S3_stitched_paid.mean()))])
    VD.to_csv(f"{OUT}.verdict.csv", index=False)

    GT = pd.DataFrame(GATES)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say("=" * 108)
    say(f"GATES {int(GT.pass_.sum())} of {len(GT)}")
    for _, g in GT.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value {g.value}  target {g.target}")
    say("")
    say(f"Runtime {time.time()-t0:.1f}s.  Offline, deterministic.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
