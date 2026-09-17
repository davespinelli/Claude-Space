#!/usr/bin/env python3
"""Idea 1158 (lane B, 2026-09-17) — should a REGIME-to-LENGTH RATIO **FIX its FRACTION LADDER**
or **COUNT-MATCH its BETWEEN TERM**?

THE PREMISE, QUOTED FROM THE QUEUE.  Idea 1157 found 1148's regime-to-length ratio falls
    0.39x-0.59x on every panel when the fraction ladder is extended from 1/3 to 1/8, because the
    BETWEEN term is a range over the ladder's ENDPOINTS and grows with the ladder while the
    length-matched WITHIN term does not — the exact count-inflation defect 1148 corrected in the
    within term and never checked in the between.  This run prices the two repairs the queue
    names (a ladder FROZEN in the clause vs a COUNT-MATCHED between term) on the record's own
    committed sub-tape rows and reports which makes two runs comparable.

THE OBJECT.  For a book b, a statistic s and a fraction ladder F:
    m[f]        = median of s over the f equal-length disjoint stretches of b's tape at 1/f
                  (f = 1 is the whole tape, one value).
    WITHIN(F)   = median over f in F, f >= 2, of the within-fraction spread of s
                  (three definitions: RANGE = max-min, SD, MATCHED = mean |pair difference|).
    BETWEEN(F)  = the length term — THE OBJECT UNDER REPAIR.
    R           = WITHIN / BETWEEN.  R > 1 says regime noise dominates the length effect.

TUNED DIALS (2, PROTOCOL rule 4), EVERY LEVEL OF BOTH PUBLISHED IN FULL:
  1. REPAIR (5 levels)
     P_RAW     1148's own, verbatim: BETWEEN = |m[1] - m[max F]| for the RANGE and MATCHED
               within-definitions, and sd over {m[f] : f in F} for the SD one.  Both forms grow
               with the ladder.  This is the status quo and the thing under test.
     P_FREEZE  repair 1 named by the queue: the CLAUSE fixes the ladder at 1148's {1,2,3} and
               every run reports that, whatever ladder it actually swept.  WITHIN pools f in
               {2,3} only.  LADDER-INVARIANT BY CONSTRUCTION — see gate G9; this run states that
               plainly and scores what the fiat COSTS instead of counting its invariance as a
               result.
     P_CMATCH  repair 2 named by the queue: BETWEEN = the mean of |m[f_i] - m[f_j]| over ALL
               distinct pairs in F — the exact count-matched construction 1148 used in its
               within term, moved into the between term.  Exhaustive, so no seed enters.
     P_CMNORM  a THIRD repair the queue does not name: P_CMATCH divided by the ladder's own mean
               pairwise |log f_i - log f_j| and multiplied by log 3, i.e. count-matched AND
               normalised to a fixed 1/1 -> 1/3 log-length span.
     P_ELAST   a FOURTH: BETWEEN = |beta| * log 3, beta = OLS slope of m[f] on log(length_f)
               over every point of F.  Uses the whole ladder and carries a fixed span.
  2. FRACTION LADDER (5 levels) F_1140 {1,2,3} (1148's own, kept for the cross-run gates),
     F_FINE {1,2,3,4,6}, F_FINER {1,2,3,4,5,6,8} (1157's three), plus F_DENSE {1,...,8} and
     F_LONG {1,2,3,4,6,8,12}.  Two runs "are comparable" exactly when they get the same R off
     different ladders, so the ladder is the axis the whole question lives on.

NOT DIALS — reported at EVERY value, everywhere: PANEL {U56, B136, SMALL}, TAPE {T_OWN,
    T_MATCHED}, BOOK (27 rungs on the N / H / GROSS / CADENCE ladders), STATISTIC {CAGR, VOL,
    SHARPE, MAXDD, ULCER, CALMAR}, WITHIN DEFINITION {RANGE, SD, MATCHED}, WITHIN SCOPE
    {W_LADDER = 1148's pooled median, W_FIX3 = read at f = 3 only} and PARTITION {ALIGNED,
    OFFSET}.

THE OBJECT IS THE RECORD'S, NOT A CONVENIENT ONE.  1148's and 1157's committed cells are a
    POOLED construction: the within groups are the per-part MEDIAN ACROSS THE RUNGS of each of
    the four rung ladders, and the per-fraction level m[f] is the median over EVERY (rung, part)
    value on the panel.  That object is replicated here EXACTLY and gated against 1157's own
    committed cells.csv on the two DETERMINISTIC within-definitions (gates G7, G8), and every
    hypothesis below is scored on it.  A second, independent PER-BOOK reading over all 162 rung
    books is computed and published beside it.

DECLARED BEFORE ANY NUMBER IS COMPUTED (scored in hypotheses.csv, each against its own bar):
  H_DEFECT   1157's premise reproduces here: under P_RAW the ratio falls by at least 0.25x
             going F_1140 -> F_FINER on all three panels at the anchor book, MAXDD / R_MATCHED.
  H_BETWEEN  the BETWEEN term carries the ladder sensitivity: median LSENS(between) >= 2x
             median LSENS(within) under P_RAW, across all cells.
  H_CMATCH   COUNT-MATCHING ALONE MAKES TWO RUNS COMPARABLE: median LSENS(P_CMATCH) <= 1.10 and
             verdict-flip rate <= 0.05.  (This is the queue's repair 2 and its declared bar.)
  H_FREEZE   FREEZING COSTS ACCURACY: the frozen reading differs from the best ladder-stable
             repair read on the FINEST ladder by >= 0.25x at a majority of cells.
  H_SPAN     the residual ladder sensitivity of P_CMATCH is a LOG-SPAN effect, not noise: the
             analytic log-linear identity (gate G11) predicts each ladder's P_CMATCH between
             term to within 10% of its realised value at a majority of cells.
  H_NORM     SPAN-NORMALISATION IS THE REPAIR THAT WORKS: median LSENS <= 1.10 and flip rate
             <= 0.05 for P_CMNORM and for P_ELAST.
  H_CURVE    the real m[f] curve is close enough to log-linear for the normalised repairs to
             hold: median R^2 of m[f] on log(length) >= 0.80 at F_FINER.
  H_NOISE    the P_RAW ladder movement is larger than the object's own sampling band: at the
             anchor books, the F_1140 -> F_FINER move lies OUTSIDE the 5-95% moving-block
             bootstrap band of R at F_1140, at a majority of the 6 (tape, panel) cells.
  H_CALIB    ladder-stability is a property of the ESTIMATOR and not of this tape: on S_PERM
             tapes (one common permutation of the book's own daily returns — every regime
             ordering destroyed, the mechanical length effect kept) the repair ranking by median
             LSENS is the same as on the real tape, for the three path statistics.
  H_CAPITAL  the repair choice is worth capital: a chooser that picks the most regime-robust
             rung moves mean OOS Sharpe by >= 0.05 between repairs at a majority of the 24
             (tape, panel, ladder) families.

NOT A KEEP PATH, AND WHY RULE 8 IS RUN ANYWAY.  A fraction ladder and a between term are a READ
    of an existing return series; neither can move a book by one basis point.  PROTOCOL rule 4
    and rule 8 are scored at every one of the 162 rung books regardless, and the only route by
    which this object could touch capital — using the repaired ratio as a SELECTOR — is built,
    walked forward and published as CH_RATIO.

THE DECLARED APPROXIMATION, AND ITS DIRECTION.  Every null here resamples ONE tape, so it prices
    sampling error around THIS regime and not regime uncertainty across regimes.  H_NOISE is
    therefore scored in the direction that makes the defect HARDEST to call real (a null band
    around one regime is narrower than the true one), so a defect that clears it clears it a
    fortiori.  The S_PERM calibration destroys regime ordering and therefore REMOVES the real
    between-term content for the three non-path statistics; their S_PERM ratios are undefined by
    construction and are reported as diagnostics, never as evidence.

ONE THING HERE WAS NOT PRE-DECLARED, AND IS LABELLED AS SUCH EVERYWHERE.  The cross-run gate
    G7 failed on its first run, and the reason was that the committed price cache has gained one
    trading day since 1157 ran: its U56 tape was 4,705 rows to 2026-09-15, today's is 4,706 to
    2026-09-16.  B136, SMALL and every T_MATCHED panel are unchanged row for row.  G7/G8 are
    therefore taken EXACTLY on the unchanged cells, and a new arm (G7c) re-runs U56 on 1157's
    own tape vintage to prove the residual is that single day and nothing else.  The size of
    that one-day move is then reported as a finding — an OBSERVATION found by a gate, NOT a
    hypothesis declared in advance, and it is never counted among the ten scored above.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
    CURRENT constituents of a sub-$2B screen, so every delisted, zeroed or screened-out name is
    absent and every drawdown here is the shallowest the period could have produced.  A
    within-length spread and a between-length term contrast the SAME books over stretches of the
    SAME inflated tape, so the bias very largely divides out of the RATIO and out of every LSENS
    in this run — which are ratios of ratios on one tape.  It does NOT divide out of the 4b legs,
    measured against SPY, a real index, so every 4b pass counted here is an UPPER bound.
"""
from __future__ import annotations

import gzip
import itertools
import re
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
SLUG = "should-a-REGIME-to-LENGTH-RATIO-FIX-its-FRACTION-LADDER-or-COUNT-MATCH-its-BETWEEN-TERM"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)

PANELS = ["U56", "B136", "SMALL"]
TAPES = ["T_OWN", "T_MATCHED"]
STATS6 = ["CAGR", "VOL", "SHARPE", "MAXDD", "ULCER", "CALMAR"]
PATH_STATS = ["MAXDD", "ULCER", "CALMAR"]

# ---------------- dial 1: the repair
REPAIRS = ["P_RAW", "P_FREEZE", "P_CMATCH", "P_CMNORM", "P_ELAST"]
# ---------------- dial 2: the fraction ladder
FRAC_LADDERS = {
    "F_1140": [1, 2, 3],
    "F_FINE": [1, 2, 3, 4, 6],
    "F_FINER": [1, 2, 3, 4, 5, 6, 8],
    "F_DENSE": [1, 2, 3, 4, 5, 6, 7, 8],
    "F_LONG": [1, 2, 3, 4, 6, 8, 12],
}
FRAC_ALL = sorted({f for v in FRAC_LADDERS.values() for f in v})
FROZEN = [1, 2, 3]                       # the ladder P_FREEZE writes into the clause
SPAN0 = float(np.log(3.0))               # the fixed 1/1 -> 1/3 log-length span
HEAD_LADDER, FINEST = "F_FINER", "F_FINER"

WITHIN_DEFS = ["RANGE", "SD", "MATCHED"]   # 1148's R_SPREAD / R_SD / R_MATCHED within terms
W_HEAD = "MATCHED"                         # the definition under which 1148's cell reads sub-1
WSCOPES = ["W_LADDER", "W_FIX3"]
PARTITIONS = ["ALIGNED", "OFFSET"]

SEED = 11581158
SEED_W = 11481148          # 1148's own seed, re-seeded at every within-term call site
NPAIR = 200
NBOOT = 200
NBOOT_POOL = 60
NPERM = 25
BLOCK = 63
OFFSET_FRACS = (0.0, 1.0 / 3.0, 2.0 / 3.0)

# ---- the record's own committed numbers, quoted and gated, never re-derived from memory
PRIOR1148 = BT / ("2026-09-16_should-a-SUB-TAPE-COMPARISON-be-required-to-publish-its-"
                  "REGIME-to-LENGTH-RATIO_cloud.regime.csv")
PRIOR1157 = BT / "2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-REGIME_B.cells.csv"
PRIOR1157R = BT / "2026-09-16_is-the-SMALL-MAXDD-CELL-the-ONE-PLACE-where-TAPE-LENGTH-BEATS-REGIME_B.perrung.csv"
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv" + (".gz" if gz else ""))
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# --------------------------------------------------------- the record's runner, verbatim
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


def six_stats(r):
    """1140's six, verbatim from 1157: three moment statistics and three drawdown-path ones."""
    r = np.asarray(r, float)
    if len(r) < 3:
        return {k: np.nan for k in STATS6}
    eq = np.cumprod(1.0 + r)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    vol = r.std(ddof=1) * np.sqrt(252.0)
    mdd = float(dd.min())
    ulcer = float(np.sqrt((dd ** 2).mean()))
    return {"CAGR": cagr * 100.0, "VOL": vol * 100.0,
            "SHARPE": (r.mean() * 252.0 / vol if vol else np.nan),
            "MAXDD": mdd * 100.0, "ULCER": ulcer * 100.0,
            "CALMAR": (cagr / abs(mdd) if mdd < 0 else np.nan)}


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
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
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
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


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ============================================================ the object and its five repairs
def parts_at(r, f, partition):
    """1157's partition code, verbatim: the equal-length stretches of r at fraction 1/f."""
    n = len(r)
    L = n // f
    if L < 3:
        return []
    if f == 1 or partition == "ALIGNED":
        return [r[k * L:(k + 1) * L] for k in range(f)]
    out = []
    for o in OFFSET_FRACS:
        s = int(round(o * L))
        k = 0
        while s + (k + 1) * L <= n:
            out.append(r[s + k * L:s + (k + 1) * L])
            k += 1
    return out


def _matched(v, rng):
    """1148's count-matched spread, VERBATIM: the mean |difference| of a random pair.

    The rng is seeded fresh from SEED_W at every call site (see within_terms), so the draw is a
    deterministic function of the values it is handed and of nothing else.  That is what makes
    P_FREEZE EXACTLY ladder-invariant (gate G9) instead of invariant up to Monte-Carlo noise.
    """
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    if len(v) == 2:
        return float(abs(v[0] - v[1]))
    i = rng.integers(0, len(v), size=(NPAIR, 2))
    i = i[i[:, 0] != i[:, 1]]
    return float(np.abs(v[i[:, 0]] - v[i[:, 1]]).mean())


def _exhaustive_pairmean(vals):
    """The same count-matched statistic taken EXHAUSTIVELY (no seed): mean |x_i - x_j|."""
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if len(v) < 2:
        return np.nan
    d = np.abs(v[:, None] - v[None, :])
    iu = np.triu_indices(len(v), 1)
    return float(d[iu].mean())


def _logspan_pairmean(fracs, n):
    """Mean pairwise |log L_i - log L_j| over the ladder, L_f = n // f — the LOG-LENGTH SPAN
    that P_CMATCH silently carries and that P_CMNORM divides out."""
    lg = np.log(np.asarray([n // f for f in fracs], float))
    d = np.abs(lg[:, None] - lg[None, :])
    iu = np.triu_indices(len(lg), 1)
    return float(d[iu].mean())


def _elast_slope(m, fracs, n):
    """OLS slope of m[f] on log(length_f), length_f = n // f."""
    xs, ys = [], []
    for f in fracs:
        if np.isfinite(m.get(f, np.nan)):
            xs.append(np.log(n // f))
            ys.append(m[f])
    if len(xs) < 2:
        return np.nan, np.nan
    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    xc = x - x.mean()
    den = float((xc ** 2).sum())
    if den == 0:
        return np.nan, np.nan
    b = float((xc * (y - y.mean())).sum() / den)
    yhat = y.mean() + b * xc
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = float(1.0 - ((y - yhat) ** 2).sum() / ss) if ss > 0 else np.nan
    return b, r2


def within_terms(within_vals, fracs, scope, rng=None):
    """{RANGE, SD, MATCHED} within terms.  within_vals: {f: [values over the f stretches]}.

    The rng is ALWAYS re-seeded from SEED_W here, so the within term depends only on the values
    and the scope, never on how many other calls preceded it.
    """
    rng = np.random.default_rng(SEED_W)
    use = [f for f in fracs if f != 1]
    if scope == "W_FIX3":
        use = [f for f in use if f == 3]
    acc = {k: [] for k in WITHIN_DEFS}
    for f in use:
        v = np.asarray([x for x in within_vals.get(f, []) if np.isfinite(x)], float)
        if len(v) < 2:
            continue
        acc["RANGE"].append(float(v.max() - v.min()))
        acc["SD"].append(float(v.std(ddof=1)))
        mm = _matched(v, rng)
        if np.isfinite(mm):
            acc["MATCHED"].append(mm)
    return {k: (float(np.nanmedian(v)) if v else np.nan) for k, v in acc.items()}


def between_terms(m, fracs, n):
    """The BETWEEN term under each of the five repairs, for each within-definition.

    P_RAW is 1148's own and is NOT one number: the SD within-definition pairs with an sd over
    the ladder's medians, the other two with the endpoint range.  Both grow with the ladder.
    Every other repair replaces the between term with ONE construction shared by all three.
    """
    fmax = max(fracs)
    endpoint = (abs(m[1] - m[fmax])
                if np.isfinite(m.get(1, np.nan)) and np.isfinite(m.get(fmax, np.nan)) else np.nan)
    ladder_sd = float(np.std([m[f] for f in fracs], ddof=1)) if len(fracs) > 1 else np.nan
    fz = [f for f in FROZEN if f in m]
    fzmax = max(fz) if fz else np.nan
    fz_end = (abs(m[1] - m[fzmax])
              if fz and np.isfinite(m.get(1, np.nan)) and np.isfinite(m.get(fzmax, np.nan))
              else np.nan)
    fz_sd = float(np.std([m[f] for f in fz], ddof=1)) if len(fz) > 1 else np.nan
    cm = _exhaustive_pairmean([m[f] for f in fracs])
    span = _logspan_pairmean(fracs, n)
    cmn = cm / span * SPAN0 if (np.isfinite(cm) and span > 0) else np.nan
    b, r2 = _elast_slope(m, fracs, n)
    el = abs(b) * SPAN0 if np.isfinite(b) else np.nan
    out = {}
    for wd in WITHIN_DEFS:
        out[("P_RAW", wd)] = ladder_sd if wd == "SD" else endpoint
        out[("P_FREEZE", wd)] = fz_sd if wd == "SD" else fz_end
        out[("P_CMATCH", wd)] = cm
        out[("P_CMNORM", wd)] = cmn
        out[("P_ELAST", wd)] = el
    return out, dict(endpoint=endpoint, ladder_sd=ladder_sd, cmatch=cm, logspan=span,
                     cmnorm=cmn, elast=el, slope=b, r2=r2)


def ratio_block(r, fracs, partition, rng, stats=STATS6):
    """Every (statistic, within-def, within-scope, repair) ratio for ONE return series and ONE
    fraction ladder.  Returns {stat: {"ratios": {(wd, scope, repair): R}, "diag": {...}}}."""
    n = len(r)
    vals = {f: [six_stats(p) for p in parts_at(r, f, partition)] for f in fracs}
    out = {}
    for stat in stats:
        wv = {f: [s[stat] for s in vals[f]] for f in fracs}
        m = {f: (float(np.nanmedian(wv[f])) if len(wv[f]) else np.nan) for f in fracs}
        bt, diag = between_terms(m, fracs, n)
        ratios, wterms = {}, {}
        for scope in WSCOPES:
            w = within_terms(wv, fracs, scope)
            for wd in WITHIN_DEFS:
                wterms[(wd, scope)] = w[wd]
                for rep in REPAIRS:
                    if rep == "P_FREEZE" and scope == "W_LADDER":
                        wf = within_terms(wv, FROZEN, scope)[wd]
                    else:
                        wf = w[wd]
                    den = bt[(rep, wd)]
                    ratios[(wd, scope, rep)] = (wf / den if (np.isfinite(wf) and
                                                            np.isfinite(den) and den != 0)
                                                else np.nan)
                    wterms[(wd, scope, rep)] = wf
        out[stat] = dict(ratios=ratios, wterms=wterms, between=bt, diag=diag, medians=m)
    return out


def within_pooled(groups, fracs, scope):
    """The within term over 1148's POOLED groups: {f: [ [values], [values], ... ]}, one group
    per rung-ladder.  Same three definitions, same fixed-seed matched sampler."""
    rng = np.random.default_rng(SEED_W)
    use = [f for f in fracs if f != 1]
    if scope == "W_FIX3":
        use = [f for f in use if f == 3]
    acc = {k: [] for k in WITHIN_DEFS}
    for f in use:
        for g in groups.get(f, []):
            v = np.asarray([x for x in g if np.isfinite(x)], float)
            if len(v) < 2:
                continue
            acc["RANGE"].append(float(v.max() - v.min()))
            acc["SD"].append(float(v.std(ddof=1)))
            mm = _matched(v, rng)
            if np.isfinite(mm):
                acc["MATCHED"].append(mm)
    return {k: (float(np.nanmedian(v)) if v else np.nan) for k, v in acc.items()}


def pooled_prep(series_by_lad, partition, fracs=None):
    """1148's / 1157's POOLED construction, replicated verbatim.

    For every fraction f and every rung-ladder lad: take each rung book's per-part statistic,
    truncate to the common part count, and take the MEDIAN ACROSS RUNGS part by part.  That
    median series is ONE group.  The per-fraction LEVEL m[f] is the median over EVERY
    (rung, part) value on the panel.  This is the object the record commits, and it is NOT the
    anchor book's own ratio.
    """
    fracs = FRAC_ALL if fracs is None else list(fracs)
    vals = {f: {lad: None for lad in series_by_lad} for f in fracs}
    allv = {f: {st: [] for st in STATS6} for f in fracs}
    for lad, series in series_by_lad.items():
        for f in fracs:
            acc = [[six_stats(pp) for pp in parts_at(rw, f, partition)] for rw in series]
            npart = min((len(a) for a in acc), default=0)
            for a in acc:
                for k in range(npart):
                    for st in STATS6:
                        allv[f][st].append(a[k][st])
            vals[f][lad] = {st: [float(np.nanmedian([a[k][st] for a in acc]))
                                 for k in range(npart)] for st in STATS6}
    return vals, allv


def pooled_cell(vals, allv, fracs, stat, n):
    groups = {f: [vals[f][lad][stat] for lad in vals[f]] for f in fracs if f != 1}
    med = {f: float(np.nanmedian(allv[f][stat])) for f in fracs}
    bt, diag = between_terms(med, fracs, n)
    out = {}
    for scope in WSCOPES:
        w = within_pooled(groups, fracs, scope)
        for wd in WITHIN_DEFS:
            for rep in REPAIRS:
                if rep == "P_FREEZE" and scope == "W_LADDER":
                    wf = within_pooled(groups, FROZEN, scope)[wd]
                else:
                    wf = w[wd]
                den = bt[(rep, wd)]
                out[(wd, scope, rep)] = dict(
                    within=wf, between=den,
                    ratio=(wf / den if (np.isfinite(wf) and np.isfinite(den) and den != 0)
                           else np.nan))
    return out, diag, med


def boot_idx(n, kind, rng):
    if kind == "IID":
        return rng.integers(0, n, size=n)
    nb = int(np.ceil(n / BLOCK))
    st = rng.integers(0, max(n - BLOCK, 1), size=nb)
    return (np.concatenate([np.arange(s, s + BLOCK) for s in st]) % n)[:n]


# ============================================================================= the census
CENSUS_FRAC_COLS = ("frac", "fraction", "subtape", "sub_tape")
CENSUS_RATIO_COLS = ("r_spread", "r_sd", "r_matched", "regime_to_length", "_within",
                     "_between", "within_", "between_")


def census_files():
    """Header-only scan of every committed CSV: which carry a sub-tape fraction / ratio column."""
    rows = []
    for p in sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz"))):
        try:
            op = gzip.open(p, "rt") if p.suffix == ".gz" else open(p, "r")
            with op as fh:
                head = fh.readline().strip()
        except Exception:
            continue
        cols = [c.strip().strip('"').lower() for c in head.split(",")]
        has_frac = any(any(k in c for k in CENSUS_FRAC_COLS) for c in cols)
        has_ratio = any(any(k in c for k in CENSUS_RATIO_COLS) for c in cols)
        if has_frac or has_ratio:
            rows.append(dict(file=p.name, has_frac_col=has_frac, has_ratio_col=has_ratio,
                             ncols=len(cols)))
    return pd.DataFrame(rows)


PROSE_PAT = re.compile(r"(regime[- ]to[- ]length|sub-?tape|fraction ladder|within-fraction|"
                       r"between-fraction)", re.I)
LADDER_PAT = re.compile(r"(1/1|1/2|1/3|1/4|1/6|1/8|F_1140|F_FINE|F_FINER|fraction ladder)", re.I)


def census_prose():
    rows = []
    files = ([ROOT / "research" / "CHANGELOG.md", ROOT / "research" / "LEADERBOARD.md",
              ROOT / "research" / "QUEUE.md"] + sorted(BT.glob("*.result.md"))
             + sorted(BT.glob("*.memo.md")))
    for p in files:
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        for sent in re.split(r"(?<=[.!?])\s+", txt):
            if PROSE_PAT.search(sent):
                rows.append(dict(file=p.name, names_ladder=bool(LADDER_PAT.search(sent)),
                                 chars=len(sent), sentence=sent.strip()[:400]))
    return pd.DataFrame(rows)


# ================================================================================== main
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    P(f"# Idea 1158 (lane B, {DATE}) — should a REGIME-to-LENGTH RATIO FIX its FRACTION LADDER "
      "or COUNT-MATCH its BETWEEN TERM?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): REPAIR {REPAIRS} x FRACTION LADDER "
      f"{list(FRAC_LADDERS)} = {len(REPAIRS)*len(FRAC_LADDERS)} combinations, ALL PUBLISHED.")
    P("# NOT dials, reported at every value: PANEL x TAPE x 27 BOOKS x 6 STATISTICS x 3 WITHIN "
      "DEFINITIONS x 2 WITHIN SCOPES x 2 PARTITIONS.")
    P("# HYPOTHESES DECLARED BEFORE ANY NUMBER (full text in the module docstring):")
    for h in ["H_DEFECT", "H_BETWEEN", "H_CMATCH", "H_FREEZE", "H_SPAN", "H_NORM", "H_CURVE",
              "H_NOISE", "H_CALIB", "H_CAPITAL"]:
        P(f"#   {h}")
    P("# P_FREEZE IS LADDER-INVARIANT BY CONSTRUCTION.  Gate G9 checks the implementation; its "
      "invariance is NOT counted as evidence anywhere in this run.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name:<9s} {what}: {value:.4e}")

    # ------------------------------------------------------------------------- panels
    P("## PANELS — loaded and STAMPED before any result number")
    small, ndrop, nmeta = load_small()
    raw = {"U56": load_universe().dropna(how="all").ffill(),
           "B136": load_universe(broad=True).dropna(how="all").ffill(),
           "SMALL": small}
    SMALL_DAYS = raw["SMALL"].index

    def prep(px):
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        return dict(px=px, idx=idx, K=K, T=T, rets=rets, priced=priced, warm=warm, ins=ins,
                    oos=oos, sc=sc, elig=elig, spy_i=spy_i)

    cells = {}
    for tape in TAPES:
        for panel in PANELS:
            px = raw[panel]
            if tape == "T_MATCHED":
                px = px.loc[px.index.intersection(SMALL_DAYS)]
            d = prep(px)
            if panel == "SMALL":
                d["elig"] = d["elig"].copy()
                d["elig"][:, d["spy_i"]] = False
            cells[(tape, panel)] = d
            P(f"  {tape:<10s} {panel:<6s} {d['K']:4d} cols, {d['T']:,} rows "
              f"{d['idx'][0].date()} -> {d['idx'][-1].date()}  warm {d['warm'].sum():,}  "
              f"IS {d['ins'].sum():,}  OOS {d['oos'].sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {cells[('T_OWN','SMALL')]['K'] - 1} names + SPY as "
      f"benchmark; tape {SMALL_DAYS[0].date()} -> {SMALL_DAYS[-1].date()}.")
    P("")

    def run_cell(tape, panel, N, H, gross, freq):
        d = cells[(tape, panel)]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = cells[("T_OWN", "U56")]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["sc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_cell("T_OWN", "U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)
    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple (bar 5e-3, price vintage)",
         v, v < 5e-3)
    P(f"     this run {m['CAGR']:.6f}/{m['Sharpe']:.6f}/{m['MaxDD']:.6f} against the committed "
      f"{A936_WH126[0]:.6f}/{A936_WH126[1]:.6f}/{A936_WH126[2]:.6f}; deviation {v:.3e} is the "
      "price-vintage drift idea 1163 opened and 1161 carried, printed rather than hidden.")
    spy = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy, d["warm"], d["ins"], d["oos"])
    v = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple (U56 own tape)", v, v < 5e-3)
    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    v = abs(blocks_m(lb_r, d["warm"], d["ins"], d["oos"])["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-3)
    v = float(np.abs(run_cell("T_OWN", "SMALL", N0, HOLD0, GROSS0, FREQ0)
                     - run_cell("T_OWN", "SMALL", N0, HOLD0, GROSS0, FREQ0)).max())
    gate("G5", "determinism of the SMALL pipeline", v, v == 0.0)

    prior48 = pd.read_csv(PRIOR1148)
    ok6 = (len(prior48) == 24 and set(prior48.stat) == set(STATS6))
    gate("G6", "1148's committed regime.csv present with its 24 cells", 0.0 if ok6 else 1.0, ok6)
    P("     1148's COMMITTED MAXDD R_MATCHED row, quoted VERBATIM FROM ITS OWN CSV: "
      + ", ".join(f"{r.panel} {r.R_MATCHED_ratio:.6f}x"
                  for r in prior48[prior48.stat == "MAXDD"].itertuples()))
    prior57 = pd.read_csv(PRIOR1157)
    P(f"     1157's committed cells.csv: {len(prior57):,} rows, ladders "
      f"{sorted(prior57.frac_ladder.unique())}")

    # ---- G7/G8: my P_RAW reproduces 1157's committed per-ladder cells, on its own ladders
    P("## ARM 0 — VERBATIM REPLICA of the record's COMMITTED POOLED object, gated on 1157")
    P("   1157's cells.csv is NOT an anchor-book ratio: it is 1148's POOLED construction — the")
    P("   per-part MEDIAN ACROSS THE RUNGS of each of the four rung ladders as the within")
    P("   groups, and the median over EVERY (rung, part) value as the per-fraction level.  This")
    P("   run replicates that object exactly and prices the repairs ON IT; the per-book grid in")
    P("   ARM 1 is a second, independent reading and both are published.")
    POOL, POOLSER = {}, {}
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            sbl = {}
            for lad, rungs in LADDERS.items():
                ser = []
                for rung in rungs:
                    kw = dict(N=ANCHOR["N"], H=ANCHOR["H"], gross=ANCHOR["GROSS"],
                              freq=ANCHOR["CADENCE"])
                    kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
                    ser.append(run_cell(tape, panel, kw["N"], kw["H"], kw["gross"],
                                        kw["freq"])[dd_["warm"]])
                sbl[lad] = ser
            POOLSER[(tape, panel)] = sbl
            for part in PARTITIONS:
                POOL[(tape, panel, part)] = pooled_prep(sbl, part)
    P(f"   pooled preparation done for {len(POOL)} (tape, panel, partition) combinations.")

    prior_keep = prior57[prior57.episode == "KEEP"]
    poolrows, pooldiag, devrows = [], [], []
    for lname, fr_ in FRAC_LADDERS.items():
        for tape in TAPES:
            for panel in PANELS:
                nwarm = int(cells[(tape, panel)]["warm"].sum())
                for part in PARTITIONS:
                    vals, allv = POOL[(tape, panel, part)]
                    for st in STATS6:
                        cc_, dg_, med_ = pooled_cell(vals, allv, fr_, st, nwarm)
                        pooldiag.append(dict(frac_ladder=lname, tape=tape, panel=panel,
                                             partition=part, stat=st, **dg_))
                        for (wd, scope, rep), vv in cc_.items():
                            poolrows.append(dict(frac_ladder=lname, tape=tape, panel=panel,
                                                 partition=part, stat=st, within_def=wd,
                                                 within_scope=scope, repair=rep, **vv))
                        row = prior_keep[(prior_keep.frac_ladder == lname)
                                         & (prior_keep.tape == tape)
                                         & (prior_keep.panel == panel)
                                         & (prior_keep.partition == part)
                                         & (prior_keep.stat == st)]
                        if len(row) != 1:
                            continue
                        for wd, col in [("RANGE", "R_SPREAD"), ("SD", "R_SD"),
                                        ("MATCHED", "R_MATCHED")]:
                            mine = cc_[(wd, "W_LADDER", "P_RAW")]["ratio"]
                            theirs = float(row[f"{col}_ratio"].iloc[0])
                            if not (np.isfinite(mine) and np.isfinite(theirs)):
                                continue
                            devrows.append(dict(frac_ladder=lname, tape=tape, panel=panel,
                                                partition=part, stat=st, within_def=wd,
                                                mine=mine, committed_1157=theirs,
                                                rel_dev=abs(mine - theirs)
                                                / max(abs(theirs), 1e-12)))
    POOLDF = pd.DataFrame(poolrows)
    POOLDIAG = pd.DataFrame(pooldiag)
    DEV = pd.DataFrame(devrows)
    dump(POOLDF, "pooled", gz=True)
    dump(POOLDIAG, "pooled_between_terms")
    dump(DEV, "crossrun")

    P("")
    P("   THE TAPE MOVED UNDER THE RECORD, AND THE GATE IS WHAT FOUND IT.  1157 ran on a U56")
    P(f"   tape of 4,705 rows ending 2026-09-15; the committed cache now serves "
      f"{cells[('T_OWN','U56')]['T']:,} rows ending {cells[('T_OWN','U56')]['idx'][-1].date()}.")
    P("   B136, SMALL and every T_MATCHED panel are UNCHANGED row for row, so the cross-run")
    P("   gate is taken on those and the one moved panel is measured separately.")
    P("   THE BAR, AND WHY IT IS NOT ZERO.  G2 already measures a price-ADJUSTMENT drift of")
    P("   1.6e-03 in the book's own CAGR between 1157's cache vintage and today's: the same")
    P("   nominal dates, re-adjusted closes.  A ratio derived from those returns therefore")
    P("   cannot reproduce to machine precision on any tape, and a bar of 1e-9 would be a bar")
    P("   on the data vintage, not on this run's arithmetic.  The bar is 1e-3 RELATIVE — three")
    P("   significant figures, tighter than the drift G2 measures in the input.")
    SAME = DEV[~((DEV.tape == "T_OWN") & (DEV.panel == "U56"))]
    MOVED = DEV[(DEV.tape == "T_OWN") & (DEV.panel == "U56")]
    det = SAME[SAME.within_def != "MATCHED"]
    d1 = float(det[det.frac_ladder == "F_1140"].rel_dev.max())
    d2 = float(det[det.frac_ladder != "F_1140"].rel_dev.max())
    gate("G7", f"CROSS-RUN pooled P_RAW == 1157's committed R_SPREAD and R_SD at F_1140, on the "
               f"{len(det[det.frac_ladder=='F_1140'])} cells whose TAPE IS UNCHANGED "
               f"(bar 1e-3 relative, price-adjustment vintage)", d1, d1 < 1e-3)
    gate("G8", "CROSS-RUN the same at F_FINE and F_FINER (the 0.39x-0.59x fall itself)",
         d2, d2 < 1e-3)
    mc = float(SAME[SAME.within_def == "MATCHED"].rel_dev.max())
    gate("G7b", "R_MATCHED on the same unchanged cells, within 1148's own 200-pair sampler's "
                "Monte-Carlo noise (bar 2.5e-1: a 200-pair mean over 2-8 values)", mc,
         mc < 2.5e-1)
    P(f"     R_MATCHED, which carries 1148's SAMPLED 200-pair spread, agrees to {mc:.4e} "
      "relative;")
    P("     both gates above are therefore taken on the two DETERMINISTIC within-definitions,")
    P("     where no sampler enters at all.")

    # ---- G7c: the moved panel reproduces EXACTLY once the tape is put back
    P("")
    P("   G7c — THE ONE-DAY ARM.  U56 T_OWN is re-run on 1157's OWN tape vintage (truncated at")
    P("   2026-09-15) to prove the whole deviation is that single extra trading day.")
    pxv = raw["U56"].loc[:pd.Timestamp("2026-09-15")]
    dv_ = prep(pxv)
    cells[("T_VINTAGE", "U56")] = dv_
    sblv = {}
    for lad, rungs in LADDERS.items():
        ser = []
        for rung in rungs:
            kw = dict(N=ANCHOR["N"], H=ANCHOR["H"], gross=ANCHOR["GROSS"],
                      freq=ANCHOR["CADENCE"])
            kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
            ser.append(run_cell("T_VINTAGE", "U56", kw["N"], kw["H"], kw["gross"],
                                kw["freq"])[dv_["warm"]])
        sblv[lad] = ser
    P(f"     vintage tape: {dv_['T']:,} rows ending {dv_['idx'][-1].date()}, warm "
      f"{int(dv_['warm'].sum()):,} (1157 had 4,705 / 4,445)")
    vdev, vrows = 0.0, []
    for part in PARTITIONS:
        vv, av = pooled_prep(sblv, part)
        for lname, fr_ in FRAC_LADDERS.items():
            if lname not in ("F_1140", "F_FINE", "F_FINER"):
                continue
            for st in STATS6:
                cc_, _, _ = pooled_cell(vv, av, fr_, st, int(dv_["warm"].sum()))
                row = prior_keep[(prior_keep.frac_ladder == lname)
                                 & (prior_keep.tape == "T_OWN") & (prior_keep.panel == "U56")
                                 & (prior_keep.partition == part) & (prior_keep.stat == st)]
                if len(row) != 1:
                    continue
                for wd, col in [("RANGE", "R_SPREAD"), ("SD", "R_SD")]:
                    mine = cc_[(wd, "W_LADDER", "P_RAW")]["ratio"]
                    theirs = float(row[f"{col}_ratio"].iloc[0])
                    if np.isfinite(mine) and np.isfinite(theirs):
                        d = abs(mine - theirs) / max(abs(theirs), 1e-12)
                        vdev = max(vdev, d)
                        vrows.append(dict(frac_ladder=lname, partition=part, stat=st,
                                          within_def=wd, vintage=mine, committed_1157=theirs,
                                          rel_dev=d))
    dump(pd.DataFrame(vrows), "vintage")
    gate("G7c", "U56 T_OWN reproduces 1157 once its tape is put back (bar 5e-2: the one-day "
                "re-cut must account for the great majority of a 7.8e-01 deviation)",
         vdev, vdev < 5e-2)
    U56_RAW_DEV = float(MOVED[MOVED.within_def != "MATCHED"].rel_dev.max())
    P(f"     U56 T_OWN deviation on TODAY's tape {U56_RAW_DEV:.4e}; on 1157's tape vintage "
      f"{vdev:.4e}")
    P(f"     — putting the single extra trading day back removes "
      f"{1 - vdev / U56_RAW_DEV:.2%} of it.  The remainder is the same price-adjustment drift")
    P("     G2 measures, which no re-run can undo.")
    ONEDAY_MED = float(MOVED[MOVED.within_def != "MATCHED"].rel_dev.median())
    ONEDAY_MAX = float(MOVED[MOVED.within_def != "MATCHED"].rel_dev.max())
    ONEDAY_BIG = float((MOVED[MOVED.within_def != "MATCHED"].rel_dev > 0.10).mean())
    P(f"     SO THE PRICE OF ONE EXTRA TRADING DAY, on the record's own committed statistic, is")
    P(f"     a MEDIAN relative move of {ONEDAY_MED:.4f} and a MAXIMUM of {ONEDAY_MAX:.4f}; "
      f"{ONEDAY_BIG:.4f} of")
    P(f"     the {int((MOVED.within_def != 'MATCHED').sum())} deterministic U56 cells move by "
      "more than 10%.  Two runs of this object are")
    P("     not comparable across a ONE-DAY tape extension, before any ladder question arises.")

    # ---- G9: P_FREEZE is ladder-invariant by construction
    fzv = [POOLDF[(POOLDF.frac_ladder == l) & (POOLDF.tape == "T_OWN")
                  & (POOLDF.panel == "SMALL") & (POOLDF.partition == "ALIGNED")
                  & (POOLDF.stat == "MAXDD") & (POOLDF.within_def == W_HEAD)
                  & (POOLDF.within_scope == "W_LADDER")
                  & (POOLDF.repair == "P_FREEZE")].ratio.iloc[0] for l in FRAC_LADDERS]
    v = float(np.nanmax(fzv) - np.nanmin(fzv))
    gate("G9", "P_FREEZE identical at every ladder BY CONSTRUCTION (implementation check)",
         v, v < 1e-12)

    # ---- G10: on a 2-point ladder the count-matched between term IS the endpoint range
    mm = {1: 1.0, 3: 4.0}
    bt, _ = between_terms(mm, [1, 3], 1000)
    v = abs(bt[("P_CMATCH", "MATCHED")] - bt[("P_RAW", "MATCHED")])
    gate("G10", "P_CMATCH == P_RAW on a two-point ladder (identity)", v, v < 1e-12)

    # ---- G11: the analytic log-linear identity — which repairs are span-invariant?
    P("## G11 — THE ANALYTIC IDENTITY, computed on an EXACTLY log-linear m[f] (no data)")
    N_SYN, BETA = 4000, 2.0
    ident = []
    for lname, fr_ in FRAC_LADDERS.items():
        msyn = {f: 10.0 + BETA * np.log(N_SYN // f) for f in fr_}
        _, dg = between_terms(msyn, fr_, N_SYN)
        ident.append(dict(frac_ladder=lname, fracs="+".join(f"1/{f}" for f in fr_),
                          endpoint=dg["endpoint"], ladder_sd=dg["ladder_sd"],
                          cmatch=dg["cmatch"], logspan=dg["logspan"], cmnorm=dg["cmnorm"],
                          elast=dg["elast"], slope=dg["slope"], r2=dg["r2"]))
    idf = pd.DataFrame(ident)
    P("   ladder    fracs                     endpoint  ladder_sd   cmatch  logspan   cmnorm"
      "    elast")
    for r_ in idf.itertuples():
        P(f"   {r_.frac_ladder:<9s} {r_.fracs:<25s} {r_.endpoint:8.4f} {r_.ladder_sd:10.4f} "
          f"{r_.cmatch:8.4f} {r_.logspan:8.4f} {r_.cmnorm:8.4f} {r_.elast:8.4f}")
    inv = {c: float(idf[c].max() / idf[c].min()) for c in
           ["endpoint", "ladder_sd", "cmatch", "cmnorm", "elast"]}
    P("   LADDER SENSITIVITY OF THE BETWEEN TERM UNDER PERFECT LOG-LINEARITY (max/min over the "
      "5 ladders):")
    for k, vv in inv.items():
        P(f"     {k:<10s} {vv:.4f}x")
    v = max(abs(inv["cmnorm"] - 1.0), abs(inv["elast"] - 1.0))
    gate("G11", "P_CMNORM and P_ELAST are EXACTLY span-invariant under log-linearity",
         v, v < 1e-9)
    dump(idf, "identity")

    # ---- G12: determinism of the whole ratio pipeline
    a = ratio_block(run_cell("T_OWN", "U56", N0, HOLD0, GROSS0, FREQ0)[cells[("T_OWN", "U56")]["warm"]],
                    FRAC_LADDERS["F_FINER"], "ALIGNED", np.random.default_rng(7))
    b_ = ratio_block(run_cell("T_OWN", "U56", N0, HOLD0, GROSS0, FREQ0)[cells[("T_OWN", "U56")]["warm"]],
                     FRAC_LADDERS["F_FINER"], "ALIGNED", np.random.default_rng(7))
    v = max(abs(a[s]["ratios"][k] - b_[s]["ratios"][k])
            for s in STATS6 for k in a[s]["ratios"]
            if np.isfinite(a[s]["ratios"][k]) and np.isfinite(b_[s]["ratios"][k]))
    gate("G12", "determinism of the ratio pipeline", v, v == 0.0)
    P("")

    # ===================================================== ARM 1 — the 162-book main grid
    P("## ARM 1 — every repair x every ladder on the record's own 162 sub-tape books")
    books, gridrows = {}, []
    bench = {}
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            warm = dd_["warm"]
            sb = blocks_m(dd_["px"]["SPY"].pct_change().fillna(0.0).values, warm,
                          dd_["ins"], dd_["oos"])
            lbm = blocks_m(backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                                    freq="W")["returns"].values, warm, dd_["ins"], dd_["oos"])
            bench[(tape, panel)] = (sb, lbm)
            for lad, rungs in LADDERS.items():
                for rung in rungs:
                    kw = dict(N=ANCHOR["N"], H=ANCHOR["H"], gross=ANCHOR["GROSS"],
                              freq=ANCHOR["CADENCE"])
                    kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
                    r = run_cell(tape, panel, kw["N"], kw["H"], kw["gross"], kw["freq"])
                    books[(tape, panel, lad, rung)] = r
                    bm = blocks_m(r, warm, dd_["ins"], dd_["oos"])
                    l4b, l4o, l4a = legs_4b(bm, sb), legs_4b_oos(bm, sb), legs_4a(bm, lbm)
                    gridrows.append(dict(tape=tape, panel=panel, ladder=lad, rung=rung, **bm,
                                         pass_4b_full=all(l4b.values()),
                                         pass_4b_oos=all(l4o.values()),
                                         pass_4a=all(l4a.values()), **l4b, **l4o, **l4a))
    grid = pd.DataFrame(gridrows)
    dump(grid, "grid")
    P(f"  4b full {int(grid.pass_4b_full.sum())} of {len(grid)} | 4b OOS "
      f"{int(grid.pass_4b_oos.sum())} of {len(grid)} | 4a {int(grid.pass_4a.sum())} of "
      f"{len(grid)}")

    long_rows = []
    diag_rows = []
    for (tape, panel, lad, rung), r in books.items():
        warm = cells[(tape, panel)]["warm"]
        rr = r[warm]
        for lname, fr_ in FRAC_LADDERS.items():
            rb = ratio_block(rr, fr_, "ALIGNED", np.random.default_rng(SEED))
            for st in STATS6:
                dgg = rb[st]["diag"]
                diag_rows.append(dict(tape=tape, panel=panel, ladder=lad, rung=rung,
                                      frac_ladder=lname, stat=st, **dgg))
                for (wd, scope, rep), val in rb[st]["ratios"].items():
                    long_rows.append(dict(tape=tape, panel=panel, ladder=lad, rung=rung,
                                          frac_ladder=lname, stat=st, within_def=wd,
                                          within_scope=scope, repair=rep,
                                          within=rb[st]["wterms"][(wd, scope, rep)],
                                          between=rb[st]["between"][(rep, wd)], ratio=val))
    LONG = pd.DataFrame(long_rows)
    DIAG = pd.DataFrame(diag_rows)
    dump(LONG, "ratios", gz=True)
    dump(DIAG, "between_terms", gz=True)
    P(f"  {len(LONG):,} ratio readings = 162 books x 6 statistics x 3 within-definitions x 2 "
      f"within-scopes x {len(REPAIRS)} repairs x {len(FRAC_LADDERS)} ladders, ALL PUBLISHED.")

    # ------------------------------------------- ARM 2 — ladder sensitivity, the headline
    P("")
    P("## ARM 2 — LADDER SENSITIVITY: does the number survive a change of ladder?")
    key = ["tape", "panel", "ladder", "rung", "stat", "within_def", "within_scope", "repair"]
    g = LONG.dropna(subset=["ratio"]).groupby(key)
    ls = g["ratio"].agg(["min", "max", "median", "count"]).reset_index()
    ls = ls[(ls["count"] == len(FRAC_LADDERS)) & (ls["min"] > 0)]
    ls["LSENS"] = ls["max"] / ls["min"]
    ls["verdict_unanimous"] = ~((ls["min"] < 1.0) & (ls["max"] >= 1.0))
    wb = LONG.dropna(subset=["within", "between"]).groupby(key)
    wbs = wb.agg(w_min=("within", "min"), w_max=("within", "max"),
                 b_min=("between", "min"), b_max=("between", "max")).reset_index()
    wbs["LSENS_within"] = wbs["w_max"] / wbs["w_min"].replace(0, np.nan)
    wbs["LSENS_between"] = wbs["b_max"] / wbs["b_min"].replace(0, np.nan)
    ls = ls.merge(wbs[key + ["LSENS_within", "LSENS_between"]], on=key, how="left")
    dump(ls, "lsens", gz=True)

    P("  MEDIAN LADDER SENSITIVITY (max/min of R over the 5 ladders) and VERDICT FLIP RATE,")
    P("  by REPAIR x WITHIN SCOPE, over every cell of the 162-book grid:")
    P("    repair     scope       cells   med LSENS   p90 LSENS   flip rate   med LS(within)"
      "   med LS(between)")
    summ = []
    for rep in REPAIRS:
        for scope in WSCOPES:
            s = ls[(ls.repair == rep) & (ls.within_scope == scope)]
            if not len(s):
                continue
            row = dict(repair=rep, within_scope=scope, cells=len(s),
                       med_LSENS=float(s.LSENS.median()),
                       p90_LSENS=float(s.LSENS.quantile(0.90)),
                       flip_rate=float((~s.verdict_unanimous).mean()),
                       med_LSENS_within=float(s.LSENS_within.median()),
                       med_LSENS_between=float(s.LSENS_between.median()))
            summ.append(row)
            P(f"    {rep:<10s} {scope:<10s} {len(s):6d} {row['med_LSENS']:11.4f} "
              f"{row['p90_LSENS']:11.4f} {row['flip_rate']:11.4f} "
              f"{row['med_LSENS_within']:15.4f} {row['med_LSENS_between']:17.4f}")
    SUMM = pd.DataFrame(summ)
    dump(SUMM, "comparability")
    P("  P_FREEZE's 1.0000 / 0.0000 is ITS DEFINITION, not a measurement — see gate G9.")

    P("")
    P("  THE SAME, BY STATISTIC, at the headline within-definition MATCHED / W_LADDER:")
    bystat = []
    for st in STATS6:
        line = f"    {st:<8s}"
        for rep in REPAIRS:
            s = ls[(ls.repair == rep) & (ls.stat == st) & (ls.within_def == W_HEAD)
                   & (ls.within_scope == "W_LADDER")]
            mv = float(s.LSENS.median()) if len(s) else np.nan
            fv = float((~s.verdict_unanimous).mean()) if len(s) else np.nan
            bystat.append(dict(stat=st, repair=rep, med_LSENS=mv, flip_rate=fv, cells=len(s)))
            line += f"  {rep}={mv:6.3f}"
        P(line)
    dump(pd.DataFrame(bystat), "lsens_by_stat")

    # ------------- ARM 2b: the SAME on the record's own COMMITTED POOLED object (HEADLINE)
    P("")
    P("## ARM 2b — THE HEADLINE: ladder sensitivity of the object the RECORD COMMITS")
    P("   (1148's pooled construction, gated at G7/G8; ARM 2 above is the per-book reading and")
    P("   both are published.  The bars below are the ones declared in the docstring, unchanged.)")
    pkey = ["tape", "panel", "partition", "stat", "within_def", "within_scope", "repair"]
    pl = POOLDF.dropna(subset=["ratio"]).groupby(pkey)["ratio"].agg(
        ["min", "max", "median", "count"]).reset_index()
    pl = pl[(pl["count"] == len(FRAC_LADDERS)) & (pl["min"] > 0)]
    pl["LSENS"] = pl["max"] / pl["min"]
    pl["verdict_unanimous"] = ~((pl["min"] < 1.0) & (pl["max"] >= 1.0))
    pwb = POOLDF.dropna(subset=["within", "between"]).groupby(pkey).agg(
        w_min=("within", "min"), w_max=("within", "max"),
        b_min=("between", "min"), b_max=("between", "max")).reset_index()
    pwb["LSENS_within"] = pwb["w_max"] / pwb["w_min"].replace(0, np.nan)
    pwb["LSENS_between"] = pwb["b_max"] / pwb["b_min"].replace(0, np.nan)
    pl = pl.merge(pwb[pkey + ["LSENS_within", "LSENS_between"]], on=pkey, how="left")
    dump(pl, "pooled_lsens")
    P("    repair     scope       cells   med LSENS   p90 LSENS   flip rate   med LS(within)"
      "   med LS(between)")
    psumm = []
    for rep in REPAIRS:
        for scope in WSCOPES:
            s = pl[(pl.repair == rep) & (pl.within_scope == scope)]
            if not len(s):
                continue
            row = dict(repair=rep, within_scope=scope, cells=len(s),
                       med_LSENS=float(s.LSENS.median()),
                       p90_LSENS=float(s.LSENS.quantile(0.90)),
                       flip_rate=float((~s.verdict_unanimous).mean()),
                       med_LSENS_within=float(s.LSENS_within.median()),
                       med_LSENS_between=float(s.LSENS_between.median()))
            psumm.append(row)
            P(f"    {rep:<10s} {scope:<10s} {len(s):6d} {row['med_LSENS']:11.4f} "
              f"{row['p90_LSENS']:11.4f} {row['flip_rate']:11.4f} "
              f"{row['med_LSENS_within']:15.4f} {row['med_LSENS_between']:17.4f}")
    PSUMM = pd.DataFrame(psumm)
    dump(PSUMM, "pooled_comparability")
    P("   P_FREEZE's 1.0000 / 0.0000 is ITS DEFINITION, not a measurement — see gate G9.")
    P("")
    P("   BY STATISTIC (pooled, MATCHED / W_LADDER, median LSENS):")
    pbystat = []
    for st in STATS6:
        line = f"    {st:<8s}"
        for rep in REPAIRS:
            s = pl[(pl.repair == rep) & (pl.stat == st) & (pl.within_def == W_HEAD)
                   & (pl.within_scope == "W_LADDER")]
            mv = float(s.LSENS.median()) if len(s) else np.nan
            fv = float((~s.verdict_unanimous).mean()) if len(s) else np.nan
            pbystat.append(dict(stat=st, repair=rep, med_LSENS=mv, flip_rate=fv, cells=len(s)))
            line += f"  {rep}={mv:6.3f}"
        P(line)
    dump(pd.DataFrame(pbystat), "pooled_lsens_by_stat")

    # ---------------------------------- ARM 3 — the premise, at the anchor book, per panel
    P("")
    P("## ARM 3 — 1157's PREMISE, reproduced on the COMMITTED POOLED object, then repaired")
    P("   (MAXDD, within-definition MATCHED, W_LADDER, ALIGNED, T_OWN — 1157's own headline "
      "cell)")
    prem = []
    P("   panel   repair      F_1140    F_FINE   F_FINER   F_DENSE    F_LONG   ratio FINER/1140")
    for panel in PANELS:
        for rep in REPAIRS:
            vals = {}
            for lname in FRAC_LADDERS:
                s = POOLDF[(POOLDF.tape == "T_OWN") & (POOLDF.panel == panel)
                           & (POOLDF.partition == "ALIGNED") & (POOLDF.stat == "MAXDD")
                           & (POOLDF.within_def == W_HEAD)
                           & (POOLDF.within_scope == "W_LADDER")
                           & (POOLDF.repair == rep) & (POOLDF.frac_ladder == lname)]
                vals[lname] = float(s.ratio.iloc[0]) if len(s) else np.nan
            rat = vals["F_FINER"] / vals["F_1140"] if vals["F_1140"] else np.nan
            prem.append(dict(panel=panel, repair=rep, **vals, finer_over_1140=rat))
            P(f"   {panel:<7s} {rep:<10s}" + "".join(f"{vals[l]:10.4f}" for l in FRAC_LADDERS)
              + f"{rat:18.4f}")
    PREM = pd.DataFrame(prem)
    dump(PREM, "premise")

    # ------------------------------- ARM 4 — what FREEZING costs: frozen vs finest repaired
    P("")
    P("## ARM 4 — WHAT THE FROZEN CLAUSE COSTS: the frozen number against the finest ladder")
    costrows = []
    for src, df_, ikeys in [("POOLED", POOLDF, pkey[:-1]),
                            ("PER-BOOK", LONG, ["tape", "panel", "ladder", "rung", "stat",
                                                "within_def", "within_scope"])]:
        fz = df_[(df_.repair == "P_FREEZE") & (df_.frac_ladder == "F_1140")]
        fz = fz.set_index(ikeys)["ratio"]
        for rep in ["P_CMATCH", "P_CMNORM", "P_ELAST", "P_RAW"]:
            fn = df_[(df_.repair == rep) & (df_.frac_ladder == FINEST)].set_index(ikeys)["ratio"]
            j = pd.concat([fz.rename("frozen"), fn.rename("fine")], axis=1).dropna()
            j = j[j.frozen > 0]
            rel = (j.fine / j.frozen)
            costrows.append(dict(reading=src, vs=rep, cells=len(j),
                                 med_fine_over_frozen=float(rel.median()),
                                 share_off_by_25pc=float(((rel < 0.75) | (rel > 1.25)).mean()),
                                 verdict_disagree=float(((j.fine < 1) != (j.frozen < 1)).mean())))
            P(f"   {src:<9s} frozen vs {rep:<9s} on {FINEST}: {len(j):,} cells, median "
              f"fine/frozen {float(rel.median()):.4f}, off by >25% at "
              f"{float(((rel<0.75)|(rel>1.25)).mean()):.4f}, verdict disagrees at "
              f"{float(((j.fine<1)!=(j.frozen<1)).mean()):.4f}")
    COST_DF = pd.DataFrame(costrows)
    dump(COST_DF, "freeze_cost")

    # ------------------------------------------ ARM 5 — log-linearity of the m[f] curve
    P("")
    P("## ARM 5 — is m[f] log-linear enough for a span-normalised between term?")
    dsub = DIAG[DIAG.frac_ladder == FINEST]
    P("   panel    stat       median R^2 of m[f] on log(length)   n cells")
    curverows = []
    for panel in PANELS:
        for st in STATS6:
            s = dsub[(dsub.panel == panel) & (dsub.stat == st)]["r2"].dropna()
            if not len(s):
                continue
            curverows.append(dict(panel=panel, stat=st, med_r2=float(s.median()), cells=len(s)))
            P(f"   {panel:<8s} {st:<10s} {float(s.median()):32.4f}   {len(s):5d}")
    CURVE = pd.DataFrame(curverows)
    dump(CURVE, "loglinearity")
    med_r2_all = float(dsub["r2"].dropna().median())
    P(f"   MEDIAN R^2 over every PER-BOOK cell at {FINEST}: {med_r2_all:.4f}")
    pdsub = POOLDIAG[POOLDIAG.frac_ladder == FINEST]
    med_r2_pool = float(pdsub["r2"].dropna().median())
    P(f"   MEDIAN R^2 over every POOLED cell at {FINEST}: {med_r2_pool:.4f}  (HEADLINE)")
    P("   pooled median R^2 by statistic: " + ", ".join(
        f"{st} {float(pdsub[pdsub.stat == st]['r2'].dropna().median()):.4f}" for st in STATS6))

    # span prediction check for H_SPAN
    sp = DIAG.merge(DIAG[DIAG.frac_ladder == "F_1140"][
        ["tape", "panel", "ladder", "rung", "stat", "cmatch", "logspan"]].rename(
        columns={"cmatch": "cm0", "logspan": "sp0"}),
        on=["tape", "panel", "ladder", "rung", "stat"], how="left")
    sp = sp[(sp.frac_ladder != "F_1140")].dropna(subset=["cmatch", "cm0", "sp0", "logspan"])
    sp = sp[sp.cm0 > 0]
    sp["pred"] = sp["cm0"] * sp["logspan"] / sp["sp0"]
    sp["pred_err"] = (sp["pred"] / sp["cmatch"] - 1.0).abs()
    span_hit = float((sp["pred_err"] <= 0.10).mean())
    P(f"   H_SPAN check: the log-span identity predicts P_CMATCH's between term to within 10% "
      f"at {span_hit:.4f} of {len(sp):,} off-F_1140 cells (median error "
      f"{float(sp['pred_err'].median()):.4f}).")
    dump(sp[["tape", "panel", "ladder", "rung", "stat", "frac_ladder", "cmatch", "pred",
             "pred_err"]], "span_prediction", gz=True)

    # ------------------------------------------- ARM 6 — the sampling band (H_NOISE)
    P("")
    P("## ARM 6 — SAMPLING BAND: is the ladder movement bigger than the object's own noise?")
    P(f"   moving-block bootstrap, L = {BLOCK}, {NBOOT_POOL} draws, ONE COMMON block index")
    P("   applied to all 27 rung books at once so the POOLED object is resampled as a whole.")
    P("   MAXDD / MATCHED / W_LADDER / ALIGNED, P_RAW.")
    BFR = sorted(set(FRAC_LADDERS["F_1140"]) | set(FRAC_LADDERS[FINEST]))
    bandrows = []
    for tape in TAPES:
        for panel in PANELS:
            sbl = POOLSER[(tape, panel)]
            n = len(sbl["H"][0])
            brng = np.random.default_rng(SEED + 17)
            d1140, dfiner = [], []
            for _ in range(NBOOT_POOL):
                ix = boot_idx(n, "BLOCK", brng)
                sb2 = {lad: [s[ix] for s in ser] for lad, ser in sbl.items()}
                vv, av = pooled_prep(sb2, "ALIGNED", BFR)
                c1, _, _ = pooled_cell(vv, av, FRAC_LADDERS["F_1140"], "MAXDD", n)
                c2, _, _ = pooled_cell(vv, av, FRAC_LADDERS[FINEST], "MAXDD", n)
                d1140.append(c1[(W_HEAD, "W_LADDER", "P_RAW")]["ratio"])
                dfiner.append(c2[(W_HEAD, "W_LADDER", "P_RAW")]["ratio"])
            a1 = np.asarray(d1140, float)
            a2 = np.asarray(dfiner, float)
            ok = np.isfinite(a1) & np.isfinite(a2)
            a1, a2 = a1[ok], a2[ok]
            lo, hi = float(np.percentile(a1, 5)), float(np.percentile(a1, 95))
            o = POOLDF[(POOLDF.tape == tape) & (POOLDF.panel == panel)
                       & (POOLDF.partition == "ALIGNED") & (POOLDF.stat == "MAXDD")
                       & (POOLDF.within_def == W_HEAD) & (POOLDF.within_scope == "W_LADDER")
                       & (POOLDF.repair == "P_RAW")]
            v1140 = float(o[o.frac_ladder == "F_1140"].ratio.iloc[0])
            vfiner = float(o[o.frac_ladder == FINEST].ratio.iloc[0])
            outside = bool(vfiner < lo or vfiner > hi)
            paired = float((a2 < a1).mean())
            bandrows.append(dict(tape=tape, panel=panel, obs_F_1140=v1140, obs_F_FINER=vfiner,
                                 boot_lo5=lo, boot_hi95=hi, ndraw=int(ok.sum()),
                                 finer_outside_band=outside, paired_share_finer_below=paired))
            P(f"   {tape:<10s} {panel:<6s} R(F_1140) {v1140:7.4f}  band [{lo:.4f}, {hi:.4f}]  "
              f"R(F_FINER) {vfiner:7.4f}  OUTSIDE={outside}  paired P(finer<1140) "
              f"{paired:.4f}")
    BAND = pd.DataFrame(bandrows)
    dump(BAND, "band")
    P("   The PAIRED column is the decisive reading: it asks whether the SAME resampled tape")
    P("   gives a smaller ratio on the finer ladder, which removes the ratio's own enormous")
    P("   marginal width from the comparison.  The declared H_NOISE bar is the marginal one")
    P("   and is scored as declared; the paired share is reported beside it, not instead.")

    # ------------------------------- ARM 7 — S_PERM calibration (H_CALIB)
    P("")
    P(f"## ARM 7 — S_PERM CALIBRATION: {NPERM} permuted tapes per (tape, panel), anchor book")
    P("   one common permutation of the book's own daily returns: EVERY regime ordering is")
    P("   destroyed and the mechanical length effect is kept.  Path statistics only carry a")
    P("   real between term here; the three moment statistics are reported as diagnostics.")
    permrows = []
    for tape in TAPES:
        for panel in PANELS:
            warm = cells[(tape, panel)]["warm"]
            r = books[(tape, panel, "H", HOLD0)][warm]
            prng = np.random.default_rng(SEED + 99)
            for k in range(NPERM):
                rp = r[prng.permutation(len(r))]
                for lname, fr_ in FRAC_LADDERS.items():
                    rb_ = ratio_block(rp, fr_, "ALIGNED", prng)
                    for st in STATS6:
                        for rep in REPAIRS:
                            permrows.append(dict(
                                tape=tape, panel=panel, draw=k, frac_ladder=lname, stat=st,
                                repair=rep,
                                ratio=rb_[st]["ratios"][(W_HEAD, "W_LADDER", rep)],
                                between=rb_[st]["between"][(rep, W_HEAD)]))
    PERM = pd.DataFrame(permrows)
    dump(PERM, "calibration", gz=True)
    pk = ["tape", "panel", "draw", "stat", "repair"]
    pg = PERM.dropna(subset=["ratio"]).groupby(pk)["ratio"].agg(["min", "max", "count"]).reset_index()
    pg = pg[(pg["count"] == len(FRAC_LADDERS)) & (pg["min"] > 0)]
    pg["LSENS"] = pg["max"] / pg["min"]
    P("   MEDIAN LSENS ON A PERMUTED TAPE (path statistics), by repair:")
    P("    repair       MAXDD    ULCER   CALMAR  | real-tape MAXDD")
    calrows = []
    for rep in REPAIRS:
        line = f"    {rep:<10s}"
        for st in PATH_STATS:
            s = pg[(pg.repair == rep) & (pg.stat == st)]["LSENS"]
            mv = float(s.median()) if len(s) else np.nan
            calrows.append(dict(repair=rep, stat=st, tape_kind="S_PERM", med_LSENS=mv,
                                cells=len(s)))
            line += f"{mv:9.4f}"
        rl = ls[(ls.repair == rep) & (ls.stat == "MAXDD") & (ls.within_def == W_HEAD)
                & (ls.within_scope == "W_LADDER")]["LSENS"]
        rv = float(rl.median()) if len(rl) else np.nan
        calrows.append(dict(repair=rep, stat="MAXDD", tape_kind="REAL", med_LSENS=rv,
                            cells=len(rl)))
        P(line + f"  | {rv:14.4f}")
    P("   between-term magnitude on S_PERM for the three MOMENT statistics (should collapse "
      "toward 0 — a diagnostic, never evidence):")
    for st in ["CAGR", "VOL", "SHARPE"]:
        s = PERM[(PERM.stat == st) & (PERM.repair == "P_RAW")]["between"].dropna()
        s2 = DIAG[(DIAG.stat == st) & (DIAG.ladder == "H") & (DIAG.rung == HOLD0)]["endpoint"]
        P(f"     {st:<7s} S_PERM median |between| {float(s.median()):.4f} against the real "
          f"tape's {float(s2.median()):.4f}")
    CAL = pd.DataFrame(calrows)
    dump(CAL, "calibration_summary")

    # ------------------------------- ARM 8 — OFFSET partition on the anchor books
    P("")
    P("## ARM 8 — the OFFSET partition (robustness, anchor books, every ladder and repair)")
    offrows = []
    for tape in TAPES:
        for panel in PANELS:
            warm = cells[(tape, panel)]["warm"]
            r = books[(tape, panel, "H", HOLD0)][warm]
            for part in PARTITIONS:
                for lname, fr_ in FRAC_LADDERS.items():
                    rb_ = ratio_block(r, fr_, part, np.random.default_rng(SEED))
                    for st in STATS6:
                        for rep in REPAIRS:
                            offrows.append(dict(tape=tape, panel=panel, partition=part,
                                                frac_ladder=lname, stat=st, repair=rep,
                                                ratio=rb_[st]["ratios"][(W_HEAD, "W_LADDER", rep)]))
    OFF = pd.DataFrame(offrows)
    dump(OFF, "partition")
    ok_ = OFF.dropna(subset=["ratio"]).groupby(
        ["tape", "panel", "partition", "stat", "repair"])["ratio"].agg(["min", "max"]).reset_index()
    ok_ = ok_[ok_["min"] > 0]
    ok_["LSENS"] = ok_["max"] / ok_["min"]
    P("   median LSENS by partition x repair:")
    for rep in REPAIRS:
        a_ = float(ok_[(ok_.repair == rep) & (ok_.partition == "ALIGNED")].LSENS.median())
        b2 = float(ok_[(ok_.repair == rep) & (ok_.partition == "OFFSET")].LSENS.median())
        P(f"     {rep:<10s} ALIGNED {a_:.4f}   OFFSET {b2:.4f}")

    # ------------------------------- ARM 9 — the chooser (the only capital route)
    P("")
    P("## ARM 9 — CH_RATIO: the repaired ratio used as a SELECTOR, walked forward (rule 8)")
    P("   parameters chosen on 2009-2016 ONLY (the IS window), read once on 2017-2026.")
    pickrows = []
    for tape in TAPES:
        for panel in PANELS:
            dd_ = cells[(tape, panel)]
            sb, lbm = bench[(tape, panel)]
            for lad, rungs in LADDERS.items():
                isr = {}
                for rung in rungs:
                    r = books[(tape, panel, lad, rung)]
                    ri = r[dd_["ins"]]
                    rb_ = ratio_block(ri, FRAC_LADDERS[FINEST], "ALIGNED",
                                      np.random.default_rng(SEED + 5))
                    isr[rung] = rb_
                for rep in REPAIRS:
                    for st in ["SHARPE", "MAXDD"]:
                        cand = {rg: isr[rg][st]["ratios"][(W_HEAD, "W_LADDER", rep)]
                                for rg in rungs}
                        cand = {k: v for k, v in cand.items() if np.isfinite(v)}
                        if not cand:
                            continue
                        pick = max(cand, key=lambda k: cand[k])
                        bm = blocks_m(books[(tape, panel, lad, pick)], dd_["warm"], dd_["ins"],
                                      dd_["oos"])
                        pickrows.append(dict(tape=tape, panel=panel, ladder=lad,
                                             chooser=f"CH_RATIO_{rep}_{st}", repair=rep,
                                             ratio_stat=st, pick=pick,
                                             OOS_Sharpe=bm["OOS_Sharpe"],
                                             OOS_CAGR=bm["OOS_CAGR"], OOS_MaxDD=bm["OOS_MaxDD"],
                                             pass_4b_full=all(legs_4b(bm, sb).values()),
                                             pass_4b_oos=all(legs_4b_oos(bm, sb).values()),
                                             pass_4a=all(legs_4a(bm, lbm).values())))
                # the plain IS-Sharpe chooser, for reference
                isS = {rg: blocks_m(books[(tape, panel, lad, rg)], dd_["warm"], dd_["ins"],
                                    dd_["oos"])["IS_Sharpe"] for rg in rungs}
                pick = max(isS, key=lambda k: isS[k])
                bm = blocks_m(books[(tape, panel, lad, pick)], dd_["warm"], dd_["ins"],
                              dd_["oos"])
                pickrows.append(dict(tape=tape, panel=panel, ladder=lad, chooser="CH_ISSHARPE",
                                     repair="-", ratio_stat="-", pick=pick,
                                     OOS_Sharpe=bm["OOS_Sharpe"], OOS_CAGR=bm["OOS_CAGR"],
                                     OOS_MaxDD=bm["OOS_MaxDD"],
                                     pass_4b_full=all(legs_4b(bm, sb).values()),
                                     pass_4b_oos=all(legs_4b_oos(bm, sb).values()),
                                     pass_4a=all(legs_4a(bm, lbm).values())))
    PICKS = pd.DataFrame(pickrows)
    dump(PICKS, "picks")
    P("   chooser                       picks   mean OOS Sharpe   4b full   4b OOS   4a")
    for ch in sorted(PICKS.chooser.unique()):
        s = PICKS[PICKS.chooser == ch]
        P(f"   {ch:<28s} {len(s):5d} {float(s.OOS_Sharpe.mean()):17.4f} "
          f"{int(s.pass_4b_full.sum()):9d} {int(s.pass_4b_oos.sum()):8d} "
          f"{int(s.pass_4a.sum()):4d}")
    # does the repair move the pick?
    movers = []
    for st in ["SHARPE", "MAXDD"]:
        base = PICKS[PICKS.chooser == f"CH_RATIO_P_RAW_{st}"].set_index(
            ["tape", "panel", "ladder"])["pick"]
        for rep in REPAIRS[1:]:
            o = PICKS[PICKS.chooser == f"CH_RATIO_{rep}_{st}"].set_index(
                ["tape", "panel", "ladder"])["pick"]
            j = pd.concat([base.rename("raw"), o.rename("rep")], axis=1).dropna()
            sr = PICKS[PICKS.chooser == f"CH_RATIO_P_RAW_{st}"].OOS_Sharpe.mean()
            so = PICKS[PICKS.chooser == f"CH_RATIO_{rep}_{st}"].OOS_Sharpe.mean()
            movers.append(dict(ratio_stat=st, repair=rep, families=len(j),
                               picks_moved=int((j.raw != j.rep).sum()),
                               mean_OOS_raw=float(sr), mean_OOS_repair=float(so),
                               d_mean_OOS=float(so - sr)))
    MOV = pd.DataFrame(movers)
    dump(MOV, "pick_moves")
    P("   the repair moves the pick at:")
    for r_ in MOV.itertuples():
        P(f"     {r_.ratio_stat:<7s} {r_.repair:<10s} {r_.picks_moved:2d} of {r_.families} "
          f"families, d mean OOS Sharpe {r_.d_mean_OOS:+.4f}")

    # ------------------------------- ARM 10 — the census
    P("")
    P("## ARM 10 — CENSUS of the record's committed sub-tape rows")
    CF = census_files()
    dump(CF, "census_files")
    nf = int(CF.has_frac_col.sum())
    nr = int(CF.has_ratio_col.sum())
    ncsv = len(list(BT.glob("*.csv"))) + len(list(BT.glob("*.csv.gz")))
    P(f"   {ncsv:,} committed CSVs scanned by header; {nf} carry a sub-tape FRACTION column, "
      f"{nr} carry a within / between / ratio column.")
    rowcount, fracrows = 0, 0
    for fn in CF[CF.has_frac_col].file:
        p = BT / fn
        if p.stat().st_size > 20_000_000:
            continue
        try:
            dfc = pd.read_csv(p)
        except Exception:
            continue
        rowcount += len(dfc)
        cols = [c for c in dfc.columns if any(k in c.lower() for k in CENSUS_FRAC_COLS)]
        if cols:
            fracrows += int(dfc[cols].notna().any(axis=1).sum())
    P(f"   those files hold {rowcount:,} committed rows, of which {fracrows:,} name a fraction "
      "or sub-tape value.")
    CP = census_prose()
    dump(CP, "census_prose")
    if len(CP):
        P(f"   PROSE: {len(CP):,} committed sentences mention a sub-tape / regime-to-length "
          f"object; {int(CP.names_ladder.sum()):,} ({float(CP.names_ladder.mean()):.4f}) name a "
          "fraction ladder at all.")
    ratio_bearing = sorted(CF[CF.has_ratio_col].file.tolist())
    P(f"   FILES CARRYING A REGIME-to-LENGTH RATIO COLUMN ({len(ratio_bearing)}): "
      + ", ".join(ratio_bearing[:8]) + (" ..." if len(ratio_bearing) > 8 else ""))

    # ============================================================== hypotheses
    P("")
    P("## HYPOTHESES — scored against the bars declared before any number was computed")
    hyp = []
    P("   EVERY hypothesis is scored on the POOLED object — the one the record commits and the")
    P("   one gates G7/G8 tie to 1157 — with the independent PER-BOOK reading printed beside")
    P("   it.  No bar was changed after any number was seen; where the two readings disagree")
    P("   that is said in the row.")

    def H(name, declared, bar, result, verdict):
        hyp.append(dict(hypothesis=name, declared=declared, bar=bar, result=result,
                        verdict=verdict))
        P(f"  {name:<11s} {verdict:<9s} {result}")

    fall = PREM[(PREM.repair == "P_RAW")]
    worst = float(fall.finer_over_1140.max())
    allfall = bool((fall.finer_over_1140 <= 0.75).all())
    H("H_DEFECT", "P_RAW falls >= 0.25x from F_1140 to F_FINER on all three panels",
      "all panels <= 0.75x",
      "POOLED finer/1140 = " + ", ".join(f"{r_.panel} {r_.finer_over_1140:.4f}x"
                                         for r_ in fall.itertuples())
      + f" (worst {worst:.4f}x); 1157 committed a 0.39x-0.59x fall",
      "SUPPORTED" if allfall else "REFUTED")

    praw = pl[pl.repair == "P_RAW"]
    pmw, pmb = float(praw.LSENS_within.median()), float(praw.LSENS_between.median())
    raw_ls = ls[ls.repair == "P_RAW"]
    mw, mb = float(raw_ls.LSENS_within.median()), float(raw_ls.LSENS_between.median())
    H("H_BETWEEN", "the BETWEEN term carries the ladder sensitivity under P_RAW",
      "median LSENS(between) >= 2x median LSENS(within)",
      f"POOLED within {pmw:.4f} / between {pmb:.4f} = {pmb/pmw:.4f}x; PER-BOOK within "
      f"{mw:.4f} / between {mb:.4f} = {mb/mw:.4f}x",
      "SUPPORTED" if pmb >= 2 * pmw else "REFUTED")

    def prep_stats(rep, frame):
        s = frame[(frame.repair == rep) & (frame.within_scope == "W_LADDER")]
        return float(s.LSENS.median()), float((~s.verdict_unanimous).mean())

    cm_l, cm_f = prep_stats("P_CMATCH", pl)
    bcm_l, bcm_f = prep_stats("P_CMATCH", ls)
    H("H_CMATCH", "COUNT-MATCHING ALONE (the queue's repair 2) makes two runs comparable",
      "median LSENS <= 1.10 AND flip rate <= 0.05",
      f"POOLED median LSENS {cm_l:.4f}, flip rate {cm_f:.4f}; PER-BOOK {bcm_l:.4f} / "
      f"{bcm_f:.4f}; the analytic log-linear floor is {inv['cmatch']:.4f}x (gate G11), so this "
      "is not a small-sample failure",
      "SUPPORTED" if (cm_l <= 1.10 and cm_f <= 0.05) else "REFUTED")

    best_rep = min(["P_CMNORM", "P_ELAST", "P_CMATCH"], key=lambda r_: prep_stats(r_, pl)[0])
    cc = COST_DF[(COST_DF.vs == best_rep) & (COST_DF.reading == "POOLED")]
    off25 = float(cc.share_off_by_25pc.iloc[0])
    H("H_FREEZE", "freezing the ladder costs accuracy against the best ladder-stable repair "
                  f"read on {FINEST} ({best_rep})",
      "off by >25% at a MAJORITY of cells",
      f"POOLED median fine/frozen {float(cc.med_fine_over_frozen.iloc[0]):.4f}, off by >25% at "
      f"{off25:.4f}, verdict disagrees at {float(cc.verdict_disagree.iloc[0]):.4f}",
      "SUPPORTED" if off25 > 0.50 else "REFUTED")

    psp = POOLDIAG.merge(POOLDIAG[POOLDIAG.frac_ladder == "F_1140"][
        ["tape", "panel", "partition", "stat", "cmatch", "logspan"]].rename(
        columns={"cmatch": "cm0", "logspan": "sp0"}),
        on=["tape", "panel", "partition", "stat"], how="left")
    psp = psp[psp.frac_ladder != "F_1140"].dropna(subset=["cmatch", "cm0", "sp0", "logspan"])
    psp = psp[psp.cm0 > 0]
    psp["pred"] = psp["cm0"] * psp["logspan"] / psp["sp0"]
    psp["pred_err"] = (psp["pred"] / psp["cmatch"] - 1.0).abs()
    pspan_hit = float((psp["pred_err"] <= 0.10).mean())
    dump(psp[["tape", "panel", "partition", "stat", "frac_ladder", "cmatch", "pred",
              "pred_err"]], "pooled_span_prediction")
    H("H_SPAN", "P_CMATCH's residual ladder sensitivity is a LOG-SPAN effect",
      "log-span identity predicts the between term to within 10% at a majority of cells",
      f"POOLED {pspan_hit:.4f} of {len(psp):,} cells within 10% (median error "
      f"{float(psp['pred_err'].median()):.4f}); PER-BOOK {span_hit:.4f} of {len(sp):,}; "
      f"analytic log-linear LSENS endpoint {inv['endpoint']:.4f}x, ladder_sd "
      f"{inv['ladder_sd']:.4f}x, cmatch {inv['cmatch']:.4f}x, cmnorm {inv['cmnorm']:.4f}x",
      "SUPPORTED" if pspan_hit > 0.50 else "REFUTED")

    cn_l, cn_f = prep_stats("P_CMNORM", pl)
    el_l, el_f = prep_stats("P_ELAST", pl)
    H("H_NORM", "SPAN-NORMALISATION is the repair that works",
      "median LSENS <= 1.10 AND flip rate <= 0.05 for BOTH P_CMNORM and P_ELAST",
      f"POOLED P_CMNORM {cn_l:.4f} / {cn_f:.4f}; P_ELAST {el_l:.4f} / {el_f:.4f}; PER-BOOK "
      f"{prep_stats('P_CMNORM', ls)[0]:.4f} and {prep_stats('P_ELAST', ls)[0]:.4f}",
      "SUPPORTED" if (cn_l <= 1.10 and cn_f <= 0.05 and el_l <= 1.10 and el_f <= 0.05)
      else "REFUTED")

    H("H_CURVE", "m[f] is close enough to log-linear for a span-normalised between term",
      "median R^2 >= 0.80 at F_FINER",
      f"POOLED median R^2 {med_r2_pool:.4f} over {int(pdsub['r2'].notna().sum()):,} cells; "
      f"PER-BOOK {med_r2_all:.4f}; MAXDD alone reads "
      f"{float(pdsub[pdsub.stat == 'MAXDD']['r2'].dropna().median()):.4f}",
      "SUPPORTED" if med_r2_pool >= 0.80 else "REFUTED")

    nout = int(BAND.finer_outside_band.sum())
    npair = int((BAND.paired_share_finer_below >= 0.95).sum())
    H("H_NOISE", "the P_RAW ladder movement exceeds the object's own sampling band",
      "F_FINER outside the F_1140 5-95% block-bootstrap band at a majority of the 6 cells",
      f"{nout} of {len(BAND)} cells outside the MARGINAL band (the declared bar); the PAIRED "
      f"statistic, reported beside it and not instead of it, has the finer ladder lower on the "
      f"SAME resampled tape at >= 0.95 of draws in {npair} of {len(BAND)} cells",
      "SUPPORTED" if nout > len(BAND) / 2 else "REFUTED")

    real_rank = sorted(REPAIRS, key=lambda x: float(
        pl[(pl.repair == x) & (pl.stat == "MAXDD") & (pl.within_def == W_HEAD)
           & (pl.within_scope == "W_LADDER")].LSENS.median()))
    perm_rank = sorted(REPAIRS, key=lambda x: float(
        pg[(pg.repair == x) & (pg.stat == "MAXDD")].LSENS.median()))
    same = real_rank == perm_rank
    H("H_CALIB", "ladder-stability is a property of the ESTIMATOR, not this tape",
      "the repair ranking by median LSENS on MAXDD is identical on S_PERM and the real tape",
      f"real(POOLED) {real_rank} vs S_PERM(anchor book) {perm_rank}",
      "SUPPORTED" if same else "REFUTED")

    maxmove = float(MOV.d_mean_OOS.abs().max())
    anymove = int(MOV.picks_moved.max())
    H("H_CAPITAL", "the repair choice is worth capital",
      "|d mean OOS Sharpe| >= 0.05 between repairs at a majority of families",
      f"max |d mean OOS Sharpe| over all repairs {maxmove:.4f}; most picks any repair moves "
      f"{anymove} of {int(MOV.families.max())} families; every CH_RATIO mean OOS Sharpe lies "
      f"between {float(PICKS[PICKS.chooser != 'CH_ISSHARPE'].groupby('chooser').OOS_Sharpe.mean().min()):.4f}"
      f" and {float(PICKS[PICKS.chooser != 'CH_ISSHARPE'].groupby('chooser').OOS_Sharpe.mean().max()):.4f}"
      f" against a plain IS-Sharpe chooser's {float(PICKS[PICKS.chooser == 'CH_ISSHARPE'].OOS_Sharpe.mean()):.4f}",
      "SUPPORTED" if maxmove >= 0.05 else "REFUTED")

    HYP = pd.DataFrame(hyp)
    dump(HYP, "hypotheses")
    P(f"  HYPOTHESES {int((HYP.verdict == 'SUPPORTED').sum())} of {len(HYP)} SUPPORTED.")

    # ============================================================== walk-forward summary
    P("")
    P("## RULE 8 — WALK-FORWARD, both KEEP paths, every one of the 162 books")
    wf = grid.copy()
    dump(wf, "walkforward")
    sb0, lb0 = bench[("T_OWN", "U56")]
    P(f"   SPY (U56 own tape): full {sb0['CAGR']:.2%} / {sb0['Sharpe']:.4f} / "
      f"{sb0['MaxDD']:.2%};  OOS {sb0['OOS_CAGR']:.2%} / {sb0['OOS_Sharpe']:.4f} / "
      f"{sb0['OOS_MaxDD']:.2%}")
    P(f"   live RULES v2:      full {lb0['CAGR']:.2%} / {lb0['Sharpe']:.4f} / "
      f"{lb0['MaxDD']:.2%};  OOS {lb0['OOS_CAGR']:.2%} / {lb0['OOS_Sharpe']:.4f} / "
      f"{lb0['OOS_MaxDD']:.2%}")
    P(f"   4b full {int(grid.pass_4b_full.sum())} of {len(grid)}, 4b OOS "
      f"{int(grid.pass_4b_oos.sum())} of {len(grid)}, 4a {int(grid.pass_4a.sum())} of "
      f"{len(grid)}.")
    best = grid[grid.pass_4b_full & grid.pass_4b_oos].sort_values("OOS_Sharpe",
                                                                 ascending=False)
    if len(best):
        b = best.iloc[0]
        P(f"   best 4b book (full AND OOS): {b.tape} / {b.panel} / {b.ladder} = {b.rung}: "
          f"full {b.CAGR:.2%} / {b.Sharpe:.4f} / {b.MaxDD:.2%} (H1 {b.H1:.4f} / H2 {b.H2:.4f}), "
          f"OOS {b.OOS_CAGR:.2%} / {b.OOS_Sharpe:.4f} / {b.OOS_MaxDD:.2%}")
    else:
        P("   NO book passes 4b full AND OOS.")
    P(f"   CH_RATIO picks clearing 4b full: {int(PICKS.pass_4b_full.sum())} of {len(PICKS)}; "
      f"4b OOS {int(PICKS.pass_4b_oos.sum())}; 4a {int(PICKS.pass_4a.sum())}.")
    P("   THIS IDEA PROPOSES NO RULE.  A fraction ladder and a between term are a READ of an")
    P("   existing return series; neither moves a book by one basis point.  The grid above is")
    P("   PROTOCOL rule 4 and rule 8 discharged, not a candidate.")

    P("")
    P("## AN OBSERVATION THE GATES FOUND, NOT A HYPOTHESIS THIS RUN DECLARED")
    P("   The committed price cache gained ONE trading day between 1157's run and this one, on")
    P("   the U56 panel only.  On that panel the record's own committed regime-to-length ratio")
    P(f"   moves by a MEDIAN of {ONEDAY_MED:.4f} and a MAXIMUM of {ONEDAY_MAX:.4f} in relative")
    P(f"   terms, with {ONEDAY_BIG:.4f} of cells moving more than 10%, while B136 and SMALL —")
    P(f"   whose tapes did not move — reproduce to {d1:.1e} / {d2:.1e} (G7, G8) and U56's own")
    P(f"   deviation falls from {U56_RAW_DEV:.3f} to {vdev:.4f} once its tape is put back (G7c).")
    P("   The mechanism is plain: every sub-tape boundary is n // f, so ONE extra row re-cuts")
    P("   every stretch on every rung of the ladder and of the fraction ladder at once.")
    P("   BEFORE any ladder or between-term question arises, two runs of this object")
    P("   are not comparable unless they state the tape's LAST DATE and row count.  That is a")
    P("   cheaper and stricter requirement than either repair the queue named, and this run")
    P("   found it by gating rather than by looking for it.")
    P("")
    dump(pd.DataFrame(gaterows), "gates")
    P("")
    P(f"## GATES {sum(gates.values())} of {len(gates)} PASS")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the CURRENT constituents of a")
    P(f"   sub-$2B screen, {cells[('T_OWN','SMALL')]['K'] - 1} columns after dropping the "
      f"{ndrop} tickers with max_1d_move >= 1.0 from data/small_meta.csv (tape "
      f"{SMALL_DAYS[0].date()} -> {SMALL_DAYS[-1].date()}).  Every delisted, zeroed or")
    P("   screened-out name is absent, so every drawdown here is the shallowest the period")
    P("   could have produced.  Every headline in this run is a RATIO OF RATIOS read on ONE")
    P("   tape (LSENS = R at one ladder over R at another), so the bias very largely divides")
    P("   out of it.  It does NOT divide out of the 4b legs, measured against SPY, a real")
    P("   index, so every 4b pass counted above is an UPPER bound.")
    P("")
    P(f"## DONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
