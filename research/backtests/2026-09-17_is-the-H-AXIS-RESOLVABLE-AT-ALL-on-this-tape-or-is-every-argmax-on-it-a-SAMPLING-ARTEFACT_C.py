#!/usr/bin/env python3
"""Idea 1181 (lane C, 2026-09-17) — is the H AXIS RESOLVABLE AT ALL on this tape, or is every
argmax on it a SAMPLING ARTEFACT?

QUESTION (QUEUE idea 1181, verbatim)
    idea 1174 found the Sharpe argmax over H moves at 14 of 18 (panel, N) families between a
    3-rung and a 16-rung ladder, and STILL moves at 10 of 18 between the 7-rung and the 16-rung
    one, so neither reading has converged.  Put a sampling interval on the H-argmax itself
    (block bootstrap over the tape at a frozen ladder) and report the rung count at which the
    argmax stops moving, or that no attainable count does.  Max 2 params (ladder, block length).

WHAT 1174 LEFT UNANSWERED, AND WHY A THIRD LADDER WOULD NOT ANSWER IT
    1174 compared two READINGS of the same axis and found they disagree.  That tells you the
    readings are unstable; it does NOT tell you whether the instability is a property of the
    LADDER (too few rungs) or of the TAPE (one finite sample).  Adding rungs can only ever
    answer the first.  This run puts a SAMPLING INTERVAL on the argmax itself, so the question
    becomes: is the between-rung difference the record publishes bigger than the noise on that
    difference?  The interval is the object the record has never carried.

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two — and the queue names both)
    1. LADDER (rung count)  {L3, L5, L7, L10, L16}, STRICTLY NESTED, SAME RANGE [21, 126]
       L3  ( 3) = [21, 63, 126]                                   — the record's three-point ladder
       L5  ( 5) = L3 + [42, 90]
       L7  ( 7) = [21, 42, 52, 63, 76, 90, 126]                   — 1093's ladder, UNCHANGED
       L10 (10) = L7 + [32, 57, 105]
       L16 (16) = 1174's LFINE = L7 + [26,32,37,47,57,69,83,105,115]
       The range is held FIXED at [21, 126] so RUNG COUNT is never confounded with RANGE.
    2. BLOCK LENGTH  {1, 5, 21, 63, 126} trading days (1 = IID).  The dependence the resample
       preserves.  63 is the HEADLINE rung (one quarter — the record's own default block).
    5 x 5 = 25 cells, EVERY ONE PUBLISHED in `.boot.csv` and printed.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL}; N in {5,8,10,12,15,20,25,30,40}
    (1082/1086/1093/1174's committed N ladder) = 27 families; statistics {Sharpe (headline),
    CAGR}; the 4a/4b legs at all 432 books; the five rule-8 choosers.  Everything else is FROZEN
    at 936/1071/1082/1086/1093/1174's construction: cap INF, CAND20 legs (21/252, 0/126, 0/63),
    max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1, warm-up 260, IS ends 2016-12-31.

WHY MaxDD IS NOT BOOTSTRAPPED HERE, SAID BEFORE THE RUN
    Sharpe and CAGR are ADDITIVE in the resampled blocks (sum, sum-of-squares, sum-of-logs), so
    a block bootstrap of them is exact and cheap.  MaxDD is an ORDER statistic of the path: the
    record's own 2026-09-17 lane-B run ("why does an IID RESAMPLE produce DEEPER drawdowns than
    a BLOCK one") shows a resampled drawdown is a different object from the tape's, not a
    noisier reading of it.  MaxDD is therefore reported POINT-WISE at every cell and never
    given a bootstrap interval.  It is still scored in 4a/4b at all 432 books.

THE EXACTNESS OF THE SAMPLER, AND ITS GATE
    For an additive statistic, gathering nb drawn blocks and summing them is ALGEBRAICALLY
    IDENTICAL to weighting the pre-computed per-start block sums by how many times each start
    was drawn.  This run draws the starts in the ordinary way and then applies them as a count
    matrix (three B x T @ T x R matmuls per cell instead of B x nb x R fancy-indexing), which is
    what makes 2,000 draws x 25 cells x 27 families cheap.  G8 checks this on the SAME DRAWN
    STARTS against a direct block-gathering implementation, so the gate is an exactness check to
    machine precision and not merely an agreement in law.

THE TWO CONTROLS, DECLARED BEFORE ANY NUMBER
    CTRL_CORR (FALSIFICATION).  The family's own 16 books, each affinely rescaled to the common
        mean and common sd, so every rung has EXACTLY the same full-sample Sharpe while the
        cross-rung CORRELATION STRUCTURE (adjacent H rungs share most of their holdings) is
        preserved.  On this object every argmax IS a sampling artefact by construction.  If the
        RESOLVED criterion fires here, the criterion is broken and the answer is (D).
    CTRL_POWER.  CTRL_CORR with a single rung's Sharpe lifted by delta in
        {0.05, 0.10, 0.20, 0.30, 0.60, 1.00}.  This gives the DETECTION FLOOR delta*: the
        smallest true between-rung Sharpe difference this tape can resolve.  The answer to the
        queue's question is then read by comparing delta* to the REAL ladder's observed spread.
        An independent-rung variant (CTRL_INDEP) is reported alongside as a second reading.

DECLARED BEFORE ANY NUMBER — the four outcomes, so none can be read off the numbers afterwards.
    A family is RESOLVED at (ladder, block) when BOTH legs hold on the headline statistic Sharpe:
        LEG 1  modal bootstrap argmax share >= 0.50
        LEG 2  the 90% argmax confidence set SPANS <= 21 days on the H axis
    LEG 2 is stated in DAYS, not in rungs, on purpose: a rung-count bar would reward coarsening,
    which is the exact failure this idea exists to catch.  A ladder RESOLVES THE AXIS when
    >= 14 of 27 families are RESOLVED at the headline block length 63.
    (D) MACHINERY DEGENERATE   : CTRL_CORR reads RESOLVED at >= 9 of 27 families.  CHECKED
        FIRST and OVERRIDES everything else — the criterion would be firing on an axis whose
        rungs are identical by construction.
    (A) THE AXIS IS RESOLVABLE : some ladder FINER than L3 resolves the axis.  Report the
        smallest rung count that does.
    (C) RESOLVABLE ONLY BY COARSENING : L3 resolves the axis and no finer ladder does, i.e. the
        stability is bought by deleting rungs rather than by measuring anything.
    (B) NOT RESOLVABLE AT ANY ATTAINABLE COUNT : no ladder, L3 included, resolves the axis.

    A LADDER READING IS NOT A KEEP PATH.  4a and 4b are scored at all 432 books and rule 8 picks
    (N, H) on 2009-2016 alone, reading 2017-2026 ONCE, with FIVE choosers including
    CH_FREEZE63 — H nailed to 63, never tuned.  That is the capital question this idea poses:
    if the H axis cannot be resolved, does refusing to tune it cost anything out of sample?

SURVIVORSHIP (PROTOCOL rule 9).  U56 (research/universe.json), B136
    (research/universe_broad.json) and SMALL (data/prices_small.csv) are CURRENT-CONSTITUENT
    lists.  Every CAGR and drawdown LEVEL below is optimistic and every 4a/4b count is an UPPER
    bound.  The resolution question compares one construction against itself on one tape and the
    bias very largely cancels out of it; it does NOT cancel out of the rule-8 OOS levels, and
    those are stated as upper bounds.
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

DATE = "2026-09-17"
SLUG = "is-the-H-AXIS-RESOLVABLE-AT-ALL-on-this-tape-or-is-every-argmax-on-it-a-SAMPLING-ARTEFACT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = ROOT / "research" / "backtests"

# ---- frozen construction (NOT dials) -------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
PANELS = ["U56", "B136", "SMALL"]

# ---- dial 1: the ladders, strictly nested, same range ---------------------------------------
L3 = [21, 63, 126]
L5 = sorted(set(L3) | {42, 90})
L7 = [21, 42, 52, 63, 76, 90, 126]
L10 = sorted(set(L7) | {32, 57, 105})
L16 = sorted(set(L7) | {26, 32, 37, 47, 57, 69, 83, 105, 115})
LADDERS = {"L3": L3, "L5": L5, "L7": L7, "L10": L10, "L16": L16}
HS = L16                                       # the grid is built once, on the finest rung set
HIDX = {h: i for i, h in enumerate(HS)}

# ---- dial 2: the block lengths --------------------------------------------------------------
BLOCKS = [1, 5, 21, 63, 126]
BLOCK_HEAD = 63

# ---- the pre-declared bars ------------------------------------------------------------------
MODAL_BAR = 0.50            # LEG 1
SPAN_BAR_DAYS = 21          # LEG 2 (in DAYS, so coarsening is never rewarded)
FAMILY_BAR = 14             # of 27 families, for "this ladder RESOLVES the axis"
CTRL_BAR = 9                # of 27 control families, for outcome (D)
NDRAW = 2000
SEED = 1181
DELTAS = [0.0, 0.05, 0.10, 0.20, 0.30, 0.60, 1.00]
STATS = ["Sharpe", "CAGR"]

# committed cross-run anchors (ideas 936 / 1071 / 1082 / 1086 / 1093 / 1174)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
_S1174 = "2026-09-17_how-many-committed-H-AXIS-claims-rest-on-the-THREE-POINT-LADDER-21-63-126_C"
G1174 = BT / f"{_S1174}.grid.csv"
B1174 = BT / f"{_S1174}.benchmarks.csv"

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ======================================================== the frozen book machinery (1082/1174)
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1082's build(), unmodified: MIN HOLD H, N slots, cap INF, equal weight gross/len(sel)."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb = []
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        nsel_by_reb.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.array(nsel_by_reb)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def blocks_metrics(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ============================================== the sampling interval on the argmax (the idea)
def block_sums(X, L):
    """Circular block sums of length L starting at every t in [0, T).  X is (T, R)."""
    T = X.shape[0]
    XX = np.vstack([X, X[:L]])
    C = np.vstack([np.zeros((1, XX.shape[1])), np.cumsum(XX, axis=0)])
    return C[L:L + T] - C[0:T]


def counts_from(st, T):
    """The MULTISET of block starts, as a (B, T) count matrix."""
    B = st.shape[0]
    flat = (np.arange(B)[:, None] * T + st).ravel()
    return np.bincount(flat, minlength=B * T).reshape(B, T).astype(np.float64)


def boot_moments(X, L, B, rng, want_log=True):
    """Circular block bootstrap MOMENTS for every column of X (T, R), in one matmul each.

    PAIRED: one resample of the TAPE is applied to every rung at once, so the between-rung
    comparison is made INSIDE each draw and the cross-rung correlation is preserved.
    Returns (S, Q, G, n, starts) with S = sum(r), Q = sum(r^2), G = sum(log1p(r)) per draw.
    Both Sharpe and CAGR are functions of these, so a block bootstrap of them is EXACT; the
    count-matrix form is algebraically identical to gathering the blocks (gate G8).
    """
    T = X.shape[0]
    nb = int(np.ceil(T / L))
    n = nb * L
    st = rng.integers(0, T, size=(B, nb))
    C = counts_from(st, T)
    S = C @ block_sums(X, L)
    Q = C @ block_sums(X * X, L)
    G = (C @ block_sums(np.log1p(np.clip(X, -0.999999, None)), L)) if want_log else None
    return S, Q, G, n, st


def sharpe_from(S, Q, n):
    mean = S / n
    var = np.maximum((Q - S * S / n) / (n - 1), 1e-300)
    return mean * np.sqrt(252.0) / np.sqrt(var)


def cagr_from(G, n):
    return np.expm1(G * 252.0 / n)


def shift_moments(S, Q, n, j, c):
    """EXACT moments after adding a constant c to column j of the tape.  Used by the controls so
    every separation delta reuses ONE set of draws instead of re-drawing (and so the power curve
    is paired across deltas)."""
    S2, Q2 = S.copy(), Q.copy()
    Q2[:, j] = Q[:, j] + 2.0 * c * S[:, j] + n * c * c
    S2[:, j] = S[:, j] + n * c
    return S2, Q2


def boot_direct(X, L, st):
    """The SAME bootstrap done by DIRECT block gathering, on the SAME drawn starts — G8's
    reference implementation.  Agreement must be to machine precision, not merely in law."""
    T, R = X.shape
    B, nb = st.shape
    base = np.arange(L)
    out = np.empty((B, R))
    for b in range(B):
        idx = (st[b][:, None] + base[None, :]).ravel() % T
        x = X[idx]
        out[b] = x.mean(axis=0) * np.sqrt(252.0) / x.std(axis=0, ddof=1)
    return out


def argmax_reading(hs, boot, obs):
    """The sampling interval on the argmax of a ladder.

    hs    : the ladder's rungs, ascending
    boot  : (B, len(hs)) bootstrap statistic, higher is better
    obs   : (len(hs),) the statistic on the tape itself
    """
    hs = np.asarray(hs)
    B = boot.shape[0]
    am = hs[np.argmax(boot, axis=1)]
    cnt = pd.Series(am).value_counts()
    p = np.array([cnt.get(h, 0) / B for h in hs])
    order = np.argsort(-p, kind="stable")
    csum = np.cumsum(p[order])
    k = int(np.searchsorted(csum, 0.90) + 1)
    cset = np.sort(hs[order[:k]])
    obs = np.asarray(obs, float)
    obs_am = int(hs[int(np.argmax(obs))])
    o = np.sort(obs)[::-1]
    ordr = np.argsort(-obs, kind="stable")
    i1 = int(ordr[0])
    i2 = int(ordr[1]) if len(obs) > 1 else i1
    gap = float(o[0] - o[1]) if len(o) > 1 else np.nan
    # SE of the PAIRED top-minus-second difference, taken at the observed ranking.  se_gap_unpaired
    # is what the same SE would read if the two rungs had been resampled INDEPENDENTLY; the
    # ratio is how much the pairing buys, and G12 gates it.
    dif = boot[:, i1] - boot[:, i2]
    se = float(dif.std(ddof=1))
    se_un = float(np.sqrt(boot[:, i1].var(ddof=1) + boot[:, i2].var(ddof=1)))
    return dict(n_rungs=len(hs), obs_argmax=obs_am, modal_rung=int(hs[int(np.argmax(p))]),
                modal_share=float(p.max()), p_obs_argmax=float(p[int(np.argmax(obs))]),
                cset_size=int(k), cset_lo=int(cset[0]), cset_hi=int(cset[-1]),
                cset_span_days=int(cset[-1] - cset[0]),
                obs_spread=float(o[0] - o[-1]), obs_gap_top2=gap, se_gap=se,
                se_gap_unpaired=se_un, pairing_gain=(se_un / se if se > 0 else np.nan),
                gap_over_se=(gap / se if se > 0 else np.nan),
                resolved=bool(p.max() >= MODAL_BAR and (cset[-1] - cset[0]) <= SPAN_BAR_DAYS))


def equalise(X):
    """CTRL_CORR: rescale every column of X to the COMMON mean and COMMON sd, so every rung has
    exactly the same full-sample Sharpe, while the cross-rung correlation structure survives."""
    m = X.mean(axis=0)
    s = X.std(axis=0, ddof=1)
    return (X - m) / s * s.mean() + m.mean()


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    P(f"# Idea 1181 (lane C, {DATE}) — is the H AXIS RESOLVABLE AT ALL on this tape, or is every")
    P("#   argmax on it a SAMPLING ARTEFACT?  A sampling interval is put on the argmax itself.")
    P(f"# 2 tuned dials: LADDER {list(LADDERS)} x BLOCK LENGTH {BLOCKS} = "
      f"{len(LADDERS)*len(BLOCKS)} cells, every one published.")
    for k, v in LADDERS.items():
        P(f"#   {k:4s} ({len(v):2d} rungs): {v}")
    P(f"# NOT dials: panel {PANELS}, N {NS} = {len(PANELS)*len(NS)} families, statistics {STATS},")
    P("#   the 4a/4b legs at all 432 books, the five rule-8 choosers.")
    P(f"# FROZEN: cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, "
      f"{COST:.0f} bps, LAG {LAG}, cadence {FREQ}, warm-up {WARMUP}, IS ends {IS_END}.")
    P(f"# BOOTSTRAP: circular block, {NDRAW} draws, seed {SEED}, PAIRED across rungs.")
    P("# DECLARED BEFORE ANY NUMBER — a family is RESOLVED when BOTH legs hold on Sharpe:")
    P(f"#   LEG 1  modal bootstrap argmax share >= {MODAL_BAR:.2f}")
    P(f"#   LEG 2  the 90% argmax confidence set spans <= {SPAN_BAR_DAYS} DAYS on the H axis")
    P(f"#   a ladder RESOLVES THE AXIS when >= {FAMILY_BAR} of 27 families are RESOLVED at "
      f"block {BLOCK_HEAD}.")
    P(f"#   (D) MACHINERY DEGENERATE : CTRL_CORR resolved at >= {CTRL_BAR} of 27  [FIRST, OVERRIDES]")
    P("#   (A) RESOLVABLE           : some ladder finer than L3 resolves the axis")
    P("#   (C) ONLY BY COARSENING   : L3 resolves it and no finer ladder does")
    P("#   (B) NOT RESOLVABLE       : no ladder, L3 included, resolves it")
    P("# MaxDD is NOT bootstrapped (order statistic, not additive) — point-wise only, but still")
    P("#   scored in 4a/4b at all 432 books.  Reason stated in the docstring.")
    P("")

    rows, benchrows, gaterows, picks = [], [], [], []
    gates = {}
    fam_rets = {}          # (panel, N) -> (T_warm, 16) post-warm-up daily returns per rung
    fam_is = {}            # (panel, N) -> (T_is,  16) in-sample-only daily returns per rung
    bench = {}

    # ------------------------------------------------------------------- ARM A: build the books
    P(f"## ARM A — THE BOOKS.  {len(PANELS)} panels x {len(NS)} N x {len(HS)} H = "
      f"{len(PANELS)*len(NS)*len(HS)} books, ALL published in .grid.csv")
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136"), small=(panel == "SMALL")).dropna(how="all").ffill()
        idx = px.index
        K = len(px.columns)
        T = len(idx)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks_metrics(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks_metrics(live, warm, ins, oos)
        bench[panel] = (sb, lb)
        P(f"   --- {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates, warm {int(warm.sum())} IS {int(ins.sum())} OOS {int(oos.sum())}")
        P(f"       SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"       RULES v2 full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb),
                      dict(panel=panel, series="RULESv2_live", **lb)]

        if panel == "U56":
            W20, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            g, tn = nrun(rets, lagmat(W20), mkl)
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, H=126, cap INF)"] = (d1, d1 < 1e-12)
            m = fmet(fast[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN vs 936/1071/1082/1086/1093/1174's committed W/H126 N=20 triple"] = (
                d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d4 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD == committed -12.05%"] = (d4, d4 < 5e-4)
            Wa, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            gates["G6 build() is deterministic"] = (float(np.abs(Wa - W20).max()),
                                                    float(np.abs(Wa - W20).max()) == 0.0)

        for N in NS:
            R = np.empty((int(warm.sum()), len(HS)))
            RI = np.empty((int(ins.sum()), len(HS)))
            for j, H in enumerate(HS):
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn = nrun(rets, lagmat(W), mkl)
                r = g - tn * COST / 1e4
                R[:, j] = r[warm]
                RI[:, j] = r[ins]
                b = blocks_metrics(r, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                rw = dict(panel=panel, N=N, H=H, cap=CAPNAME, mean_nsel=float(nsel.mean()),
                          turnover=float(tn[warm].sum() / (warm.sum() / 252.0)),
                          IS_turnover=float(tn[ins].sum() / (ins.sum() / 252.0)),
                          **b, **l4b, **l4a, **l4bo,
                          pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                          pass4b_oos=all(l4bo.values()),
                          in_L3=H in L3, in_L7=H in L7)
                rw["pass4b_full_and_oos"] = rw["pass4b"] and rw["pass4b_oos"]
                rows.append(rw)
            fam_rets[(panel, N)] = R
            fam_is[(panel, N)] = RI
            P(f"       N={N:2d} done ({len(HS)} rungs)  ({time.time()-t0:.0f}s)")

    grid = pd.DataFrame(rows)
    bn = pd.DataFrame(benchrows)
    FAMS = [(p, n) for p in PANELS for n in NS]

    # ------------------------------------------------------------------------ cross-run gate
    if G1174.exists():
        g74 = pd.read_csv(G1174)
        j = grid.merge(g74, on=["panel", "N", "H"], suffixes=("", "_74"))
        d5 = max(float(np.abs(j.CAGR - j.CAGR_74).max()),
                 float(np.abs(j.Sharpe - j.Sharpe_74).max()),
                 float(np.abs(j.MaxDD - j.MaxDD_74).max()),
                 float(np.abs(j.turnover - j.turnover_74).max()))
        gates[f"G5 CROSS-RUN 1174's committed grid reproduced cell-for-cell ({len(j)} shared "
              "(panel, N, H) cells, 4 statistics each)"] = (d5, d5 < 1e-9)
        gates["G5b the shared-cell count is 1174's WHOLE committed grid"] = (
            float(len(g74) - len(j)), len(j) == len(g74))
    else:
        gates["G5 CROSS-RUN 1174's committed grid (FILE MISSING — gate cannot run)"] = (
            float("nan"), False)

    # G3b DIAGNOSES G3 rather than absorbing it (1174 read the same 2.894e-03 drift on the same
    # day): if the SAME-DAY committed benchmarks reproduce exactly while the OLDER anchor drifts,
    # the drift is a TAPE VINTAGE effect (idea 1163's finding) and not a construction error here.
    if B1174.exists():
        b74 = pd.read_csv(B1174)
        j = bn.merge(b74, on=["panel", "series"], suffixes=("", "_74"))
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
        d3b = max(float(np.abs(j[c] - j[f"{c}_74"]).max()) for c in cols)
        gates[f"G3b CROSS-RUN 1174's SAME-DAY committed benchmarks reproduced ({len(j)} series x "
              f"{len(cols)} statistics) — the DIAGNOSIS of G3"] = (d3b, d3b < 1e-9)

    nested = set(L3) <= set(L5) <= set(L7) <= set(L10) <= set(L16)
    gates["G7 the five ladders are STRICTLY NESTED L3 < L5 < L7 < L10 < L16"] = (
        float(len(L16)), bool(nested and 3 < 5 < 7 < 10 < 16))
    gates["G7b all five ladders span the SAME range [21, 126] (count is not range)"] = (
        0.0, all(min(v) == 21 and max(v) == 126 for v in LADDERS.values()))
    tsp = float(grid[grid.panel == "B136"].turnover.max() - grid[grid.panel == "B136"].turnover.min())
    gates["G9 the H dial is LIVE (B136 turnover spread >= 1.0x/yr across the ladder)"] = (
        tsp, tsp >= 1.0)

    # G8: the count-matrix sampler == direct block gathering ON THE SAME DRAWN STARTS.  This is
    # an EXACTNESS check to machine precision, not an agreement-in-law check.
    gk = ("U56", 20) if ("U56", 20) in fam_rets else FAMS[0]
    Xg = fam_rets[gk]
    S_g, Q_g, _, n_g, st_g = boot_moments(Xg, BLOCK_HEAD, 600, np.random.default_rng(99),
                                          want_log=False)
    sh_m = sharpe_from(S_g, Q_g, n_g)
    sh_d = boot_direct(Xg, BLOCK_HEAD, st_g)
    d8 = float(np.abs(sh_m - sh_d).max())
    gates["G8 the count-matrix sampler == DIRECT block gathering on the SAME 600 drawn starts, "
          "cell for cell (600 draws x 16 rungs)"] = (d8, d8 < 1e-9)
    # G8b: the bootstrap is centred on the tape (no systematic bias in the resampled Sharpe)
    S_f, Q_f, _, n_f, _ = boot_moments(Xg, BLOCK_HEAD, NDRAW, np.random.default_rng(97),
                                       want_log=False)
    obs_g = np.array([fsharpe(Xg[:, j]) for j in range(len(HS))])
    db = float(np.abs(sharpe_from(S_f, Q_f, n_f).mean(axis=0) - obs_g).max())
    gates["G8b the bootstrap mean Sharpe is centred on the tape's (max |bias| < 0.05)"] = (db, db < 0.05)

    # ------------------------------------------------------- ARM B: the interval on the argmax
    P("")
    P(f"## ARM B — THE SAMPLING INTERVAL ON THE ARGMAX.  {len(FAMS)} families x "
      f"{len(BLOCKS)} block lengths x {len(LADDERS)} ladders x {len(STATS)} statistics, "
      f"{NDRAW} paired draws each.")
    boot_rows = []
    boot_cache = {}
    for (panel, N) in FAMS:
        X = fam_rets[(panel, N)]
        obs_sh = np.array([fsharpe(X[:, j]) for j in range(len(HS))])
        obs_cg = np.array([fmet(X[:, j])[0] for j in range(len(HS))])
        for L in BLOCKS:
            rg = np.random.default_rng(SEED * 1000 + L)
            S_, Q_, G_, n_, _ = boot_moments(X, L, NDRAW, rg)
            sh, cg = sharpe_from(S_, Q_, n_), cagr_from(G_, n_)
            if L == BLOCK_HEAD:
                boot_cache[(panel, N)] = sh
            for lname, lad in LADDERS.items():
                cols = [HIDX[h] for h in lad]
                for stat, bt, ob in (("Sharpe", sh, obs_sh), ("CAGR", cg, obs_cg)):
                    rd = argmax_reading(lad, bt[:, cols], ob[cols])
                    boot_rows.append(dict(panel=panel, N=N, block=L, ladder=lname, stat=stat, **rd))
        P(f"   {panel:6s} N={N:2d} done  ({time.time()-t0:.0f}s)")
    bo = pd.DataFrame(boot_rows)
    dump(bo, "boot")

    head = bo[(bo.stat == "Sharpe") & (bo.block == BLOCK_HEAD)]
    P("")
    P(f"   HEADLINE TABLE — statistic Sharpe, block length {BLOCK_HEAD}, {len(FAMS)} families")
    P("     ladder  rungs   resolved   modal share (med)   90% set span, days (med)   "
      "P(obs argmax) med   gap/SE med")
    lad_summary = {}
    for lname, lad in LADDERS.items():
        s = head[head.ladder == lname]
        nres = int(s.resolved.sum())
        lad_summary[lname] = (nres, len(s), float(s.modal_share.median()),
                              float(s.cset_span_days.median()))
        P(f"     {lname:5s} {len(lad):5d}   {nres:3d}/{len(s):<3d}   {s.modal_share.median():17.4f}"
          f"   {s.cset_span_days.median():22.1f}   {s.p_obs_argmax.median():16.4f}"
          f"   {s.gap_over_se.median():10.3f}")
    P("")
    P("     the UNIFORM-NULL modal share for a ladder of L rungs is 1/L — the bar a ladder must")
    P("     clear before its argmax carries any information at all:")
    for lname, lad in LADDERS.items():
        s = head[head.ladder == lname]
        P(f"       {lname:5s} 1/L = {1.0/len(lad):.4f}   observed median modal share "
          f"{s.modal_share.median():.4f}   ratio {s.modal_share.median()*len(lad):.2f}x   "
          f"families above 1/L: {int((s.modal_share > 1.0/len(lad)).sum())}/{len(s)}")

    P("")
    P("   EVERY ONE OF THE 25 DIAL CELLS (statistic Sharpe): resolved families of 27")
    P("     block\\ladder " + "".join(f"{l:>10s}" for l in LADDERS))
    for L in BLOCKS:
        s = bo[(bo.stat == "Sharpe") & (bo.block == L)]
        P(f"     {L:11d} " + "".join(
            f"{int(s[s.ladder==l].resolved.sum()):>7d}/27" for l in LADDERS))
    P("     median modal share:")
    for L in BLOCKS:
        s = bo[(bo.stat == "Sharpe") & (bo.block == L)]
        P(f"     {L:11d} " + "".join(
            f"{s[s.ladder==l].modal_share.median():>10.4f}" for l in LADDERS))
    P("     median 90% confidence-set SPAN in days (the coarsening-proof leg):")
    for L in BLOCKS:
        s = bo[(bo.stat == "Sharpe") & (bo.block == L)]
        P(f"     {L:11d} " + "".join(
            f"{s[s.ladder==l].cset_span_days.median():>10.1f}" for l in LADDERS))
    P("     CONTROL STATISTIC CAGR, resolved families of 27:")
    for L in BLOCKS:
        s = bo[(bo.stat == "CAGR") & (bo.block == L)]
        P(f"     {L:11d} " + "".join(
            f"{int(s[s.ladder==l].resolved.sum()):>7d}/27" for l in LADDERS))

    # ------------------------------------------------ 1174's own finding, re-read with intervals
    P("")
    P("   1174's FINDING RE-READ WITH THE INTERVAL ATTACHED.  1174 reported the L3 and L16 point")
    P("   argmaxes disagree at 14 of 18 families.  Here: how often is the L16 point argmax even")
    P("   INSIDE its own 90% bootstrap confidence set, and how wide is that set?")
    s16 = head[head.ladder == "L16"]
    P(f"     L16, block {BLOCK_HEAD}: median 90% set holds {s16.cset_size.median():.1f} of 16 rungs"
      f" and spans {s16.cset_span_days.median():.0f} days of the 105-day axis "
      f"({s16.cset_span_days.median()/105.0:.0%} of it)")
    P(f"     the point argmax carries median probability {s16.p_obs_argmax.median():.4f}; "
      f"at {int((s16.p_obs_argmax < 0.20).sum())} of {len(s16)} families it is below 0.20")
    P(f"     median observed top-minus-second Sharpe gap {s16.obs_gap_top2.median():.4f} against a "
      f"median paired SE of {s16.se_gap.median():.4f}  ->  median gap/SE {s16.gap_over_se.median():.3f}")
    P(f"     families whose top rung beats the second by 2 SE: "
      f"{int((s16.gap_over_se >= 2.0).sum())} of {len(s16)}")

    # ---------------------------------------------------------------------- ARM C: the controls
    P("")
    P("## ARM C — THE CONTROLS.  CTRL_CORR is the FALSIFICATION control (16 rungs rescaled to a")
    P("   COMMON mean and sd, so every rung has EXACTLY the same full-sample Sharpe while the")
    P("   cross-rung correlation survives).  CTRL_POWER lifts ONE rung's Sharpe by delta.")
    ctrl_rows = []
    for fi, (panel, N) in enumerate(FAMS):
        X = fam_rets[(panel, N)]
        E = equalise(X)
        sd_d = float(X.std(axis=0, ddof=1).mean())
        j63 = HIDX[63]
        # CTRL_INDEP: 16 INDEPENDENT block resamples of the family's OWN H=63 book — same DGP,
        # no cross-rung correlation.  A second reading, reported alongside, never merged.
        rgi = np.random.default_rng(SEED * 7 + fi)
        base = X[:, j63]
        Tn = len(base)
        nb = int(np.ceil(Tn / BLOCK_HEAD))
        I = np.empty((nb * BLOCK_HEAD, len(HS)))
        ar = np.arange(BLOCK_HEAD)
        for j in range(len(HS)):
            stj = rgi.integers(0, Tn, size=nb)
            I[:, j] = base[(stj[:, None] + ar[None, :]).ravel() % Tn]
        for kind, M in (("CTRL_CORR", E), ("CTRL_INDEP", I)):
            rg = np.random.default_rng(SEED * 31 + fi * 2 + (0 if kind == "CTRL_CORR" else 1))
            S_, Q_, _, n_, _ = boot_moments(M, BLOCK_HEAD, NDRAW, rg, want_log=False)
            # every delta reuses the SAME draws and shifts the moments EXACTLY, so the power
            # curve is paired across separations and costs one bootstrap, not seven.
            for d in DELTAS:
                c = d * sd_d / np.sqrt(252.0)
                S2, Q2 = shift_moments(S_, Q_, n_, j63, c)
                Z63 = M[:, j63] + c
                ob = np.array([fsharpe(M[:, j]) for j in range(len(HS))])
                ob[j63] = fsharpe(Z63)
                rd = argmax_reading(L16, sharpe_from(S2, Q2, n_), ob)
                ctrl_rows.append(dict(panel=panel, N=N, control=kind, delta=d,
                                      lifted_rung=63, **rd))
    ct = pd.DataFrame(ctrl_rows)
    dump(ct, "controls")

    P("")
    P("   THE DETECTION FLOOR — how large must a TRUE between-rung Sharpe difference be before")
    P("   this tape can see it?  (L16, block 63, one rung lifted by delta, 27 families each)")
    P("     control      delta   resolved   modal share (med)   P(lifted rung is argmax) med   span(d)")
    for kind in ("CTRL_CORR", "CTRL_INDEP"):
        for d in DELTAS:
            s = ct[(ct.control == kind) & (ct.delta == d)]
            plift = float((s.modal_rung == 63).mean())
            P(f"     {kind:11s} {d:6.2f}   {int(s.resolved.sum()):3d}/{len(s):<3d}"
              f"   {s.modal_share.median():17.4f}   {plift:28.4f}   {s.cset_span_days.median():7.1f}")
    corr0 = ct[(ct.control == "CTRL_CORR") & (ct.delta == 0.0)]
    n_ctrl_res = int(corr0.resolved.sum())
    floor = None
    for d in DELTAS:
        s = ct[(ct.control == "CTRL_CORR") & (ct.delta == d)]
        if int(s.resolved.sum()) >= FAMILY_BAR:
            floor = d
            break
    P("")
    P(f"   FALSIFICATION CONTROL CTRL_CORR at delta=0: RESOLVED at {n_ctrl_res} of {len(corr0)} "
      f"families (the (D) bar is >= {CTRL_BAR}); median modal share {corr0.modal_share.median():.4f}"
      f" vs the uniform null 1/16 = {1/16:.4f}")
    gates["G10 FALSIFICATION: CTRL_CORR (identical rungs by construction) does NOT read RESOLVED "
          f"at the (D) bar ({CTRL_BAR} of 27)"] = (float(n_ctrl_res), n_ctrl_res < CTRL_BAR)
    top = ct[(ct.control == "CTRL_CORR") & (ct.delta == DELTAS[-1])]
    gates[f"G11 POWER: CTRL_CORR at delta={DELTAS[-1]:.2f} DOES read RESOLVED at a majority "
          f"({FAMILY_BAR} of 27) — the criterion can see a real rung difference"] = (
        float(top.resolved.sum()), int(top.resolved.sum()) >= FAMILY_BAR)
    # G12: the draws really are PAIRED across rungs.  If they were not, the SE of the
    # top-minus-second difference would be the independent-resampling one; adjacent H rungs share
    # most of their holdings, so pairing must shrink it at essentially every family.
    pg = head[head.ladder == "L16"].pairing_gain
    gates["G12 the draws are PAIRED across rungs (the paired top-minus-second SE is SMALLER than "
          f"the unpaired one at >= 90% of families; median gain {pg.median():.2f}x)"] = (
        float((pg > 1.0).mean()), float((pg > 1.0).mean()) >= 0.90)

    P("")
    if floor is None:
        P(f"   DETECTION FLOOR delta*: NOT REACHED even at delta={DELTAS[-1]:.2f} Sharpe — on this")
        P("   tape a rung would have to beat its neighbours by MORE THAN A FULL SHARPE POINT")
        P(f"   before {FAMILY_BAR} of 27 families could name it.")
    else:
        P(f"   DETECTION FLOOR delta* = {floor:.2f} Sharpe — the smallest lift at which "
          f">= {FAMILY_BAR} of 27 families read RESOLVED.")
    P(f"   THE REAL LADDER'S OWN SPREAD, for comparison (L16, block {BLOCK_HEAD}):")
    P(f"     median best-minus-worst Sharpe across the 16 rungs  {s16.obs_spread.median():.4f}"
      f"   (p90 {s16.obs_spread.quantile(0.9):.4f})")
    P(f"     median best-minus-SECOND Sharpe                     {s16.obs_gap_top2.median():.4f}"
      f"   (p90 {s16.obs_gap_top2.quantile(0.9):.4f})")

    # ---------------------------------------------------------------- the pre-declared verdict
    resolves = {l: lad_summary[l][0] >= FAMILY_BAR for l in LADDERS}
    if n_ctrl_res >= CTRL_BAR:
        outcome = "(D) MACHINERY DEGENERATE"
    elif any(resolves[l] for l in ["L5", "L7", "L10", "L16"]):
        smallest = next(l for l in ["L5", "L7", "L10", "L16"] if resolves[l])
        outcome = f"(A) THE AXIS IS RESOLVABLE — smallest resolving ladder {smallest}"
    elif resolves["L3"]:
        outcome = "(C) RESOLVABLE ONLY BY COARSENING"
    else:
        outcome = "(B) NOT RESOLVABLE AT ANY ATTAINABLE RUNG COUNT"
    P("")
    P(f"## PRE-DECLARED OUTCOME: {outcome}")
    P("   resolved families of 27 by ladder at block 63: "
      + "  ".join(f"{l} {lad_summary[l][0]}" for l in LADDERS))

    # --------------------------------------------------------------- KEEP paths at all 432 books
    P("")
    P("## BOTH KEEP PATHS at all 432 books (PROTOCOL rule 4)")
    for panel in PANELS:
        s = grid[grid.panel == panel]
        P(f"   {panel:6s}: 4b full {int(s.pass4b.sum()):3d}/{len(s)}   "
          f"4b OOS {int(s.pass4b_oos.sum()):3d}/{len(s)}   "
          f"4b full AND OOS {int(s.pass4b_full_and_oos.sum()):3d}/{len(s)}   "
          f"4a {int(s.pass4a.sum()):3d}/{len(s)}")
    P(f"   TOTAL : 4b full {int(grid.pass4b.sum())}/{len(grid)}   "
      f"4b OOS {int(grid.pass4b_oos.sum())}/{len(grid)}   "
      f"4b full AND OOS {int(grid.pass4b_full_and_oos.sum())}/{len(grid)}   "
      f"4a {int(grid.pass4a.sum())}/{len(grid)}")
    both = grid[grid.pass4b_full_and_oos]
    if len(both):
        P("   books clearing 4b FULL and OOS at 10 bps (top 12 by full Sharpe):")
        for _, r_ in both.sort_values("Sharpe", ascending=False).head(12).iterrows():
            P(f"      {r_.panel:6s} N={int(r_.N):2d} H={int(r_.H):3d}  {r_.CAGR:7.2%} / "
              f"{r_.Sharpe:.4f} / {r_.MaxDD:7.2%}  halves {r_.H1:.3f}/{r_.H2:.3f}  "
              f"OOS {r_.OOS_CAGR:6.2%}/{r_.OOS_Sharpe:.4f}/{r_.OOS_MaxDD:7.2%}  "
              f"turn {r_.turnover:.2f}x")
        P(f"   DISTINCT (panel, N) families among the {len(both)} passers: "
          f"{both.groupby(['panel','N']).ngroups}; distinct panels: {both.panel.nunique()} — a")
        P("   count of PASSING CELLS is not a count of distinct books (1189's worry, priced here).")
    # IS ANY OF THIS A NEW CANDIDATE?  The record already committed 1174's passer set on the same
    # day; a passer this run shares with it is a RE-READ, not a discovery, and must not be
    # counted twice.  G13 makes that a gate rather than a claim.
    new_cells = set()
    if G1174.exists():
        g74 = pd.read_csv(G1174)
        old_pass = set(map(tuple, g74[g74.pass4b & g74.pass4b_oos][["panel", "N", "H"]].values))
        new_cells = set(map(tuple, both[["panel", "N", "H"]].values)) - old_pass
        P(f"   OF THE {len(both)} PASSERS, {len(both)-len(new_cells)} ARE CELLS 1174 ALREADY "
          f"COMMITTED TODAY and {len(new_cells)} ARE NEW: {sorted(new_cells) if new_cells else 'NONE'}")
        gates["G13 the 4b passer set is a RE-READ of 1174's committed set, not a new candidate "
              "(no cell passes here that 1174 did not already publish)"] = (
            float(len(new_cells)), len(new_cells) == 0)

    # ------------------------------------------------------------------------ RULE 8, five choosers
    P("")
    P("## RULE 8 WALK-FORWARD — (N, H) chosen on 2009-2016 ONLY, 2017-2026 read ONCE.")
    P("   CH_FREEZE63 never tunes the H axis at all; it is the chooser this idea exists to test.")
    for panel in PANELS:
        gp = grid[grid.panel == panel]
        sb, lb = bench[panel]
        # IS-only bootstrap, for the two interval-aware choosers.  IS WINDOW ONLY — no leakage.
        isboot = {}
        for N in NS:
            rg = np.random.default_rng(SEED * 17 + N)
            S_, Q_, _, n_, _ = boot_moments(fam_is[(panel, N)], BLOCK_HEAD, NDRAW, rg,
                                            want_log=False)
            sh = sharpe_from(S_, Q_, n_)
            am = np.argmax(sh, axis=1)
            isboot[N] = (sh.mean(axis=0), np.bincount(am, minlength=len(HS)) / NDRAW)
        cands = []
        for N in NS:
            bm, pa = isboot[N]
            for j, H in enumerate(HS):
                r_ = gp[(gp.N == N) & (gp.H == H)].iloc[0]
                cands.append(dict(N=N, H=H, boot_mean_IS_Sharpe=float(bm[j]),
                                  p_IS_argmax=float(pa[j]), row=r_))
        cd = pd.DataFrame(cands)

        def pick_by(df, keyfn, name, ladder):
            sub = df[df.H.isin(LADDERS[ladder])].copy()
            sub["k"] = sub.apply(keyfn, axis=1)
            sub = sub.sort_values(["k", "N", "H"], ascending=[False, True, True])
            r_ = sub.iloc[0]["row"]
            return dict(panel=panel, chooser=name, ladder=ladder,
                        N=int(r_["N"]), H=int(r_["H"]),
                        IS_Sharpe=r_["IS_Sharpe"], IS_CAGR=r_["IS_CAGR"], IS_MaxDD=r_["IS_MaxDD"],
                        OOS_CAGR=r_["OOS_CAGR"], OOS_Sharpe=r_["OOS_Sharpe"],
                        OOS_MaxDD=r_["OOS_MaxDD"], full_CAGR=r_["CAGR"], full_Sharpe=r_["Sharpe"],
                        full_MaxDD=r_["MaxDD"], H1=r_["H1"], H2=r_["H2"], turnover=r_["turnover"],
                        spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                        spy_OOS_MaxDD=sb["OOS_MaxDD"], spy_CAGR=sb["CAGR"],
                        spy_Sharpe=sb["Sharpe"], spy_MaxDD=sb["MaxDD"],
                        spy_H1=sb["H1"], spy_H2=sb["H2"],
                        live_OOS_Sharpe=lb["OOS_Sharpe"], live_OOS_MaxDD=lb["OOS_MaxDD"],
                        live_Sharpe=lb["Sharpe"], live_H1=lb["H1"], live_H2=lb["H2"],
                        pass4b_full=bool(r_["pass4b"]), pass4b_oos=bool(r_["pass4b_oos"]),
                        pass4a=bool(r_["pass4a"]))
        picks.append(pick_by(cd, lambda x: x["row"]["IS_Sharpe"], "CH_L16_IS", "L16"))
        picks.append(pick_by(cd, lambda x: x["row"]["IS_Sharpe"], "CH_L3_IS", "L3"))
        picks.append(pick_by(cd, lambda x: x["boot_mean_IS_Sharpe"], "CH_BOOTMEAN", "L16"))
        picks.append(pick_by(cd, lambda x: (x["p_IS_argmax"], x["row"]["IS_Sharpe"]),
                             "CH_MODAL", "L16"))
        picks.append(pick_by(cd[cd.H == 63], lambda x: x["row"]["IS_Sharpe"],
                             "CH_FREEZE63", "L3"))
    pk = pd.DataFrame(picks)
    dump(pk, "rule8")

    P("     panel  chooser        N   H    IS_Sharpe   OOS CAGR / Sharpe / MaxDD    SPY OOS S"
      "   beats SPY  4b  4bOOS  4a")
    for _, r_ in pk.iterrows():
        P(f"     {r_.panel:6s} {r_.chooser:13s} {int(r_.N):3d} {int(r_.H):3d}  "
          f"{r_.IS_Sharpe:9.4f}   {r_.OOS_CAGR:7.2%} / {r_.OOS_Sharpe:.4f} / "
          f"{r_.OOS_MaxDD:7.2%}    {r_.spy_OOS_Sharpe:.4f}   "
          f"{str(bool(r_.OOS_Sharpe > r_.spy_OOS_Sharpe)):5s}      {int(r_.pass4b_full)}  "
          f"{int(r_.pass4b_oos)}     {int(r_.pass4a)}")
    P("")
    P("   DOES TUNING THE H AXIS BUY OOS SHARPE, OR IS FREEZING IT FREE?  (the capital question)")
    P("     chooser       mean OOS Sharpe   mean OOS CAGR   mean OOS MaxDD   beats SPY   4b full  4a")
    for ch in ["CH_L3_IS", "CH_L16_IS", "CH_BOOTMEAN", "CH_MODAL", "CH_FREEZE63"]:
        s = pk[pk.chooser == ch]
        P(f"     {ch:13s} {s.OOS_Sharpe.mean():15.4f}   {s.OOS_CAGR.mean():13.2%}   "
          f"{s.OOS_MaxDD.mean():14.2%}   {int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum()):5d}/{len(s)}"
          f"   {int(s.pass4b_full.sum()):7d}  {int(s.pass4a.sum()):2d}   picks "
          f"{[(p, int(n), int(h)) for p, n, h in zip(s.panel, s.N, s.H)]}")
    d_free = float(pk[pk.chooser == "CH_L16_IS"].OOS_Sharpe.mean()
                   - pk[pk.chooser == "CH_FREEZE63"].OOS_Sharpe.mean())
    P(f"     CH_L16_IS - CH_FREEZE63 on mean OOS Sharpe: {d_free:+.4f}  "
      f"(positive = tuning the H axis paid; negative = the tuning cost money)")

    dump(grid, "grid")
    dump(bn, "benchmarks")

    # ------------------------------------------------------------------------------ the gates
    P("")
    P("## GATES")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))
    dump(pd.DataFrame(gaterows), "gates")
    npass = sum(1 for _, (v, ok) in gates.items() if ok)
    P(f"   {npass} of {len(gates)} gates PASS")

    # ------------------------------------------------------------------------ LEADERBOARD rows
    P("")
    P("## LEADERBOARD rows")
    lbrows = []
    for panel in PANELS:
        s = pk[(pk.panel == panel) & (pk.chooser == "CH_L16_IS")].iloc[0]
        f63 = pk[(pk.panel == panel) & (pk.chooser == "CH_FREEZE63")].iloc[0]
        b0 = bn[(bn.panel == panel) & (bn.series == "RULESv2_live")].iloc[0]
        nm = (f"1181 {panel} rule-8 CH_L16_IS pick N={int(s.N)} H={int(s.H)} "
              f"(OOS Sharpe {s.OOS_Sharpe:.4f}) vs CH_FREEZE63 N={int(f63.N)} H=63 "
              f"(OOS {f63.OOS_Sharpe:.4f}); SPY OOS {s.spy_OOS_Sharpe:.4f}")
        v = "KEEP-candidate" if (s.pass4b_full and s.pass4b_oos) else "KILL"
        lbrows.append(f"| {DATE} | {nm} | {s.full_CAGR:.1%} | {s.full_Sharpe:.2f} | "
                      f"{s.full_MaxDD:.1%} | {s.H1:.2f} / {s.H2:.2f} | "
                      f"{b0.Sharpe:.2f} ({b0.H1:.2f}/{b0.H2:.2f}) | {v} | "
                      f"{DATE}_{SLUG}_C.py |")
    nm = (f"1181 THE INTERVAL ON THE H-ARGMAX — {outcome}. Sharpe, block {BLOCK_HEAD}: resolved "
          + "/".join(f"{lad_summary[l][0]}" for l in LADDERS)
          + " of 27 families at L3/L5/L7/L10/L16 (bar 14); L16 median modal share "
          + f"{s16.modal_share.median():.4f} vs uniform null 0.0625, median 90% argmax set spans "
          + f"{s16.cset_span_days.median():.0f} of the 105-day axis; median top-minus-second "
          + f"gap {s16.obs_gap_top2.median():.4f} on a paired SE of {s16.se_gap.median():.4f} "
          + f"(gap/SE {s16.gap_over_se.median():.2f}); detection floor "
          + (f"delta* = {floor:.2f}" if floor is not None else f"delta* > {DELTAS[-1]:.2f}")
          + f" Sharpe; falsification CTRL_CORR {n_ctrl_res}/27; {npass}/{len(gates)} gates")
    nm += (f"; 4b full+OOS {int(grid.pass4b_full_and_oos.sum())}/432 and 4a 0/432, of which NEW "
           f"cells (not already committed by 1174 today) = {len(new_cells)}")
    lbrows.append(f"| {DATE} | {nm} | n/a | n/a | n/a | n/a | n/a | KILL as a capital finding | "
                  f"{DATE}_{SLUG}_C.py |")
    for l in lbrows:
        P("   " + l)

    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(lbrows) + "\n")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
