#!/usr/bin/env python3
"""Idea 1103 (cloud lane, 2026-09-16) — is the RESOLUTION FLOOR a property of EDGE or of
every LADDERED STATISTIC?

QUESTION (QUEUE idea 1103, verbatim)
    idea 1098's floor was measured on EDGE, whose null median carries its own sampling error.
    Re-measure the same block-bootstrap floor for argmaxes over OOS Sharpe, full-sample Sharpe
    and MaxDD on the identical 9-rung n ladder, and report whether a statistic with no null
    attached resolves any better.  Max 2 params (statistic, block length).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: STATISTIC {EDGE, EDGE_FIXNULL, CAGR, S_FULL, S_OOS, DD} x BLOCK LENGTH
    L {21, 63, 126} = 18 points, ALL published, on BOTH panels (36 rows).  PANEL is NOT a dial
    — U56 and B136 are 1098's own two panels and every number is reported on both.  The LADDER
    is not a dial: 1082/1098's nine rungs n = [5,8,10,12,15,20,25,30,40] verbatim, nothing
    added and nothing dropped.  q is not a dial: q=0.90 headline (1098's own), q=0.95 printed
    beside it and never selected on.  Everything else frozen at 1082/1094/1098/1102/1104's
    construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, W cadence, min hold 126,
    10 bps, LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws, S=40 nulls, 34-step bisection.

THE SIX STATISTICS (dial 1) — all measured on the SAME block draws within a window
    EDGE          100 x (CAGR_book(n) - median_s CAGR_null(n,s)), book AND nulls both resampled
                  on the draw.  1098/1104's construction verbatim.  This is the incumbent.
    EDGE_FIXNULL  100 x (CAGR_book(n)_draw - median_s CAGR_null(n,s)_FULL-SAMPLE).  The null
                  median is held at its point value, so the only resampling noise is the book's.
                  A DECOMPOSITION CONTROL, not a proposal: it isolates exactly the term the
                  idea names (the null median's own sampling error).
    CAGR          100 x CAGR_book(n).  No null attached at all.
    S_FULL        annualised Sharpe of the book on the warm window.
    S_OOS         annualised Sharpe of the book on 2017-2026 (resampled WITHIN that window).
    DD            100 x MaxDD of the book on the warm window.  A PATH functional: the resampled
                  ORDER decides it, so it is drawn path-by-path, not from block sums.

THE COMPARISON IS UNIT-FREE, DECLARED BEFORE ANY NUMBER
    A floor lives in its statistic's own units, so RAW floors across statistics are MEANINGLESS
    (3.25 pp of CAGR against 0.04 of Sharpe compares nothing).  Every cross-statistic reading
    below is one of exactly three unit-free quantities, all three always published:
      (1) REL_FLOOR      min(floor, spread) / spread — the floor as a share of what the ladder
                         itself spans.  1.0 means the ladder's LARGEST gap is un-resolved.
      (2) UNRES_SHARE    unresolved rung pairs / 36, at q.
      (3) W90            the smallest contiguous-in-rank set of rungs carrying >= 0.90 of the
                         bootstrap argmax mass, in RUNGS (1..9).  9 means the argmax is free.
    PRE-REGISTERED DECISION RULE: statistic X RESOLVES BETTER than Y at a (panel, L) point iff
    X wins a MAJORITY (>= 2) of those three.  Exact ties count for neither.

DECLARED BEFORE ANY NUMBER
    (a) H_NULL_COSTS   — the idea's own premise: EDGE resolves WORSE than CAGR (the same book
                         statistic with the null removed) at a MAJORITY of the 6 (panel, L)
                         points, by the majority-of-three rule above.
    (b) H_FIXNULL_MID  — EDGE_FIXNULL sits BETWEEN EDGE and CAGR on REL_FLOOR at a majority of
                         the 6 points.  If it does not, the null median's sampling error is not
                         what separates EDGE from CAGR and the idea's stated mechanism is wrong.
    (c) H_SOME_DECIDES — at least one null-free statistic DECIDES the nine-rung ladder (tie set
                         = {peak} at q=0.90) on at least one panel at the headline L=63.
    (d) H_DD_WORST     — DD resolves worst of the six (median REL_FLOOR over the 6 points),
                         because a path functional carries the resampled ORDER as extra noise.
    (e) H_OOS_WORSE    — S_OOS resolves worse than S_FULL (shorter window, ~40% of the days).
    (f) H_L_RISES      — REL_FLOOR rises with block length L at a majority of the 12
                         (panel, statistic) cells: longer blocks, fewer of them, more noise.
    (g) THE FLOOR IS NOT A KEEP PATH.  4a and 4b are scored at every rung of the ladder on both
        panels, and rule 8 picks n on IS 2009-2016 ALONE under four choosers with OOS read once.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels, so every level is
    optimistic.  A GAP between two rungs of the same ladder, and the agreement of a resample
    with that gap's sign, both contrast two books over the same inflated tape and the bias very
    largely cancels out of them — which is why this run's headline is a RESOLVABILITY claim and
    not a capital claim.  It does NOT cancel out of the 4b legs, which are measured against SPY.
"""
from __future__ import annotations

import hashlib
import sys
import time
import zlib
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-RESOLUTION-FLOOR-a-property-of-EDGE-or-of-every-LADDERED-STATISTIC"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ, HOLD = 10.0, 0.75, "W", 126
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME, BISECT = "INF", 34

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]          # 1082/1098's ladder, verbatim
NSEED = 40                                        # 1098's headline seed count
BDRAWS = 1000
BLOCKS_L = [21, 63, 126]                          # dial 2
L_HEAD = 63
QHEAD, QALT = 0.90, 0.95
PANELS = ["U56", "B136"]                          # 1098's own two panels; NOT a dial
STATS = ["EDGE", "EDGE_FIXNULL", "CAGR", "S_FULL", "S_OOS", "DD"]     # dial 1
NULLFREE = ["CAGR", "S_FULL", "S_OOS", "DD"]
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR", "C_ISEDGE"]

# committed cross-run anchors (gates only, never selection)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1082_EDGE_U56 = [5.95, 5.35, 6.21, 6.82, 5.22, 5.12, 2.95, 1.55, 0.41]
A1098_U56 = dict(floor90=3.25, floor95=4.66, peak=12, gap=0.61, collapse=6.41)
A1098_B136 = dict(floor90=4.02, collapse=6.47)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    """1082/1086/1094/1098/1104's recipe verbatim, so the NULL DRAWS are the SAME objects."""
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


def bseed(*parts):
    """Process-stable seed for the BOOTSTRAP draws (1108's repair of 1102's hash())."""
    return 11031103 + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# --------------------------------- 1082/1098/1104's runner and rescaler, copied verbatim
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


def gross_rescaler(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        return out

    return f


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


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


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


def build_null(rng, priced, reb, N, H, T, K, gross):
    """1082's convention: random ranks, NO eligibility gate."""
    return build(rng.random((T, K)), np.ones((T, K), dtype=bool), priced, reb, N, H, T, K, gross)


def lam_rebuilt(f, sl, target_dd):
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(BISECT):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


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


# ------------------------------------------------------------- the bootstrap machinery
def block_starts(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    return rng.integers(0, T, size=(ndraws, nb)), nb


def boot_cagr(LOGR, starts, L, nb, chunk=100):
    """CAGR of every row under CIRCULAR block resampling — exact (a product ignores order)."""
    D = np.concatenate([LOGR, LOGR], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    out = np.empty((LOGR.shape[0], starts.shape[0]))
    for a in range(0, starts.shape[0], chunk):
        st = starts[a:a + chunk]
        out[:, a:a + chunk] = (CS[:, st + L] - CS[:, st]).sum(axis=2)
    return np.expm1(out * (252.0 / (nb * L)))


def boot_sharpe(R, starts, L, nb, chunk=100):
    """Annualised Sharpe of every row under the SAME draws — exact (mean/SD ignore order)."""
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    n = nb * L
    out = np.empty((R.shape[0], starts.shape[0]))
    for a in range(0, starts.shape[0], chunk):
        st = starts[a:a + chunk]
        s1 = (CS1[:, st + L] - CS1[:, st]).sum(axis=2)
        s2 = (CS2[:, st + L] - CS2[:, st]).sum(axis=2)
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        out[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return out


def boot_maxdd(R, starts, L, chunk=25):
    """MaxDD under the SAME draws — a PATH functional, so the resampled ORDER is rebuilt."""
    nr = R.shape[0]
    nd = starts.shape[0]
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    off = np.arange(L)
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        st = starts[a:a + chunk]
        idx = (st[:, :, None] + off[None, None, :]).reshape(st.shape[0], -1)
        for j in range(nr):
            cum = np.cumsum(D[j][idx], axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def widest_mass(counts, rungs, q=0.90):
    """Smallest contiguous-in-RANK set of rungs carrying >= q of the argmax mass (1104's)."""
    k = len(rungs)
    for w in range(1, k + 1):
        best = None
        for i in range(0, k - w + 1):
            m = counts[i:i + w].sum()
            if m >= q and (best is None or m > best[2]):
                best = (w, [rungs[j] for j in range(i, i + w)], float(m))
        if best is not None:
            return best
    return (k, list(rungs), float(counts.sum()))


def measure_floor(gaps, agree, q):
    """1098's definition verbatim: the smallest |gap| above which EVERY pair agrees in sign
    with the full sample at least q of the time."""
    o = np.argsort(gaps)
    g, a = np.asarray(gaps)[o], np.asarray(agree)[o]
    for i in range(len(g)):
        if (a[i:] >= q).all():
            return float(g[i])
    return float("inf")


def load_panel(name):
    px = load_universe(broad=(name == "B136")).dropna(how="all").ffill()
    return px


# ------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1103 (cloud lane, {DATE}) — is the RESOLUTION FLOOR a property of EDGE or of")
    P("#   every LADDERED STATISTIC?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): STATISTIC {STATS} x BLOCK LENGTH {BLOCKS_L}")
    P(f"#   = {len(STATS)*len(BLOCKS_L)} points, ALL published, on BOTH panels {PANELS}.")
    P("#   PANEL is NOT a dial (1098's own two, both reported everywhere).  The LADDER is NOT a")
    P(f"#   dial: 1082/1098's nine rungs {NS} verbatim.  q is NOT a dial: q={QHEAD} headline,")
    P(f"#   q={QALT} printed beside it, never selected on.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap {CAPNAME}, max_vol {MAXVOL}, gross {GROSS0}, cadence")
    P(f"#   {FREQ}, min hold {HOLD}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end "
      f"{IS_END}, S={NSEED} nulls, {BDRAWS} draws, {BISECT}-step bisection.")
    P("# THE COMPARISON IS UNIT-FREE: a floor lives in its own statistic's units, so raw floors")
    P("#   across statistics compare NOTHING.  Three unit-free readings, all always published:")
    P("#   (1) REL_FLOOR min(floor,spread)/spread  (2) UNRES_SHARE unresolved pairs / 36")
    P("#   (3) W90 rungs carrying >= 0.90 of the bootstrap argmax mass.")
    P("#   DECISION RULE (pre-registered): X resolves better than Y iff X wins >= 2 of the 3.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_NULL_COSTS   EDGE resolves WORSE than CAGR at a majority of the 6 (panel, L).")
    P("#   (b) H_FIXNULL_MID  EDGE_FIXNULL's REL_FLOOR sits BETWEEN EDGE's and CAGR's, majority.")
    P("#   (c) H_SOME_DECIDES some null-free statistic DECIDES the ladder on some panel at L=63.")
    P("#   (d) H_DD_WORST     DD resolves worst of the six (median REL_FLOOR).")
    P("#   (e) H_OOS_WORSE    S_OOS resolves worse than S_FULL.")
    P("#   (f) H_L_RISES      REL_FLOOR rises with L at a majority of the 12 (panel, stat) cells.")
    P("#   (g) THE FLOOR IS NOT A KEEP PATH: 4a/4b at every rung, rule 8 picks n on IS alone.")
    P("")

    gates, gaterows = {}, []
    gridrows, edgerows, benchrows, pairrows, floorrows, pickrows, varrows = [], [], [], [], [], [], []
    BOOT = {}

    for panel in PANELS:
        px = load_panel(panel)
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        yrs = warm.sum() / 252.0
        sc, elig = mech(px)
        rank_key = -sc
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks_m(live, warm, ins, oos)
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        benchrows.append(dict(panel=panel, series="RULESv2_live", **lb))
        P(f"## {panel}: {K} columns, {T:,} days {idx[0].date()}..{idx[-1].date()}, "
          f"{yrs:.2f} scored years;  IS {int(ins.sum()):,} / OOS {int(oos.sum()):,} days")
        P(f"   SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2  full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  OOS "
          f"{lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        P(f"   4b bars: DD cap {DD_CAP*abs(sb['MaxDD']):.2%} full / "
          f"{DD_CAP*abs(sb['OOS_MaxDD']):.2%} OOS;  CAGR floor {CAGR_FLOOR*sb['CAGR']:.2%} full")

        # ---- gates that need only the anchor books ----------------------------------------
        W20 = build(rank_key, elig, priced, reb, 20, HOLD, T, K, GROSS0)
        g20, t20 = nrun(rets, lagmat(W20), mkl)
        r20 = g20 - t20 * COST / 1e4
        eng = backtest(px, pd.DataFrame(W20, index=idx, columns=px.columns),
                       cost_bps=COST, freq=FREQ)["returns"].values
        d = float(np.abs(r20[WARMUP:] - eng[WARMUP:]).max())
        gates[f"G1  fast runner == engine.backtest ({panel} N=20 H=126 @ 10 bps)"] = (d, d < 1e-12)
        f20 = gross_rescaler(rets, lagmat(W20), mkl)
        d1b = float(np.abs(f20(1.0) - r20).max())
        gates[f"G1b gross_rescaler(1.0) == nrun ({panel})"] = (d1b, d1b < 1e-12)
        if panel == "U56":
            m = fmet(r20[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2  CROSS-RUN 936/1071/1082/1098's committed U56 W/H126/N=20 triple"] = (
                d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3  CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d5 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G5  live RULES v2 MaxDD == committed -12.05%"] = (d5, d5 < 5e-4)
            a_ = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0)).random(6)
            b_ = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0)).random(6)
            gates["G6  determinism of 1082/1098's null-seed recipe"] = (
                float(np.abs(a_ - b_).max()), float(np.abs(a_ - b_).max()) == 0.0)

        # ---- the ladder: book + S=40 DD-matched nulls at every rung -----------------------
        BOOKR, NULLR, NULLC = {}, {}, {}
        for N in NS:
            W = build(rank_key, elig, priced, reb, N, HOLD, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(W), mkl)
            r = g - tn * COST / 1e4
            b = blocks_m(r, warm, ins, oos)
            BOOKR[N] = r
            nulls, lams, drier, nis = [], [], 0, []
            for s in range(NSEED):
                rng = np.random.default_rng(mdseed(panel, N, CAPNAME, s))
                Wn = build_null(rng, priced, reb, N, HOLD, T, K, GROSS0)
                fn = gross_rescaler(rets, lagmat(Wn), mkl)
                lr = lam_rebuilt(fn, warm, b["MaxDD"])
                if lr is None:
                    drier += 1
                    lr = 1.0
                nulls.append(fn(lr)[warm])
                lams.append(lr)
                lri = lam_rebuilt(fn, ins, b["IS_MaxDD"])         # 1082's IS arm, for C_ISEDGE
                nis.append(fmet(fn(1.0)[ins] if lri is None else fn(lri)[ins])[0])
            NULLR[N] = np.array(nulls)
            ncagr = np.array([fmet(x)[0] for x in NULLR[N]])
            NULLC[N] = ncagr
            nis = np.array(nis)
            l4b, l4a, l4o = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
            e = 100.0 * (b["CAGR"] - float(np.median(ncagr)))
            se = 100.0 * 1.2533 * float(ncagr.std(ddof=1)) / np.sqrt(NSEED)
            gridrows.append(dict(panel=panel, N=N, turnover=float(tn[warm].sum() / yrs), **b,
                                 **l4b, **l4a, **l4o, pass4b=all(l4b.values()),
                                 pass4a=all(l4a.values()), pass4b_oos=all(l4o.values()),
                                 lam_median=float(np.median(lams)), n_already_drier=drier,
                                 EDGE_pp=e, EDGE_se_pp=se))
            edgerows.append(dict(panel=panel, N=N, seeds=NSEED, EDGE_pp=e,
                                 EDGE_IS_pp=100.0 * (b["IS_CAGR"] - float(np.median(nis))),
                                 book_CAGR=b["CAGR"], null_CAGR_med=float(np.median(ncagr)),
                                 null_CAGR_sd=float(ncagr.std(ddof=1)), EDGE_se_pp=se,
                                 lam_median=float(np.median(lams)),
                                 book_pct_of_null=float((ncagr < b["CAGR"]).mean())))
            P(f"   N={N:2d}  book {b['CAGR']:7.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:7.2%}  "
              f"S_OOS {b['OOS_Sharpe']:.4f}  EDGE {e:+6.2f} pp (SE {se:.2f})  "
              f"lam~{np.median(lams):.3f}  drier {drier}/{NSEED}  ({time.time()-t0:.0f}s)")

        if panel == "U56":
            mine = [next(r for r in edgerows if r["panel"] == "U56" and r["N"] == N)["EDGE_pp"]
                    for N in NS]
            dx = float(np.abs(np.array(mine) - np.array(A1082_EDGE_U56)).max())
            gates["G7  CROSS-RUN 1082/1098's nine committed U56 EDGE figures reproduce"] = (
                dx, dx < 5.1e-3)
            g12 = next(r for r in gridrows if r["panel"] == "U56" and r["N"] == 12)
            d4 = max(abs(g12["CAGR"] - A1098_U56_N12[0]), abs(g12["Sharpe"] - A1098_U56_N12[1]),
                     abs(g12["MaxDD"] - A1098_U56_N12[2]))
            gates["G4  CROSS-RUN 1098/1102's committed U56 n=12 triple"] = (d4, d4 < 5e-4)
        if panel == "B136":
            g15 = next(r for r in gridrows if r["panel"] == "B136" and r["N"] == 15)
            d4b = max(abs(g15["CAGR"] - A1098_B136_N15[0]),
                      abs(g15["Sharpe"] - A1098_B136_N15[1]),
                      abs(g15["MaxDD"] - A1098_B136_N15[2]))
            gates["G4b CROSS-RUN 1098/1102's committed B136 n=15 triple"] = (d4b, d4b < 5e-4)

        # ---- the bootstrap, SIX statistics on the SAME draws -------------------------------
        Tw, To = int(warm.sum()), int(oos.sum())
        BOOKW = np.array([BOOKR[N][warm] for N in NS])
        BOOKO = np.array([BOOKR[N][oos] for N in NS])
        NULLW = np.array([NULLR[N][s] for N in NS for s in range(NSEED)])
        LOGR = np.log1p(np.vstack([BOOKW, NULLW]))
        full_null_med = np.array([float(np.median(NULLC[N])) for N in NS])
        FULL = {
            "EDGE": np.array([next(r for r in edgerows if r["panel"] == panel
                                   and r["N"] == n)["EDGE_pp"] for n in NS]),
            "CAGR": 100.0 * np.array([next(r for r in gridrows if r["panel"] == panel
                                           and r["N"] == n)["CAGR"] for n in NS]),
            "S_FULL": np.array([next(r for r in gridrows if r["panel"] == panel
                                     and r["N"] == n)["Sharpe"] for n in NS]),
            "S_OOS": np.array([next(r for r in gridrows if r["panel"] == panel
                                    and r["N"] == n)["OOS_Sharpe"] for n in NS]),
            "DD": 100.0 * np.array([next(r for r in gridrows if r["panel"] == panel
                                         and r["N"] == n)["MaxDD"] for n in NS]),
        }
        FULL["EDGE_FIXNULL"] = FULL["EDGE"].copy()      # identical point values, by construction

        for L in BLOCKS_L:
            rngw = np.random.default_rng(bseed("warm", panel, L))
            rngo = np.random.default_rng(bseed("oos", panel, L))
            stw, nbw = block_starts(rngw, Tw, L, BDRAWS)
            sto, nbo = block_starts(rngo, To, L, BDRAWS)
            C = boot_cagr(LOGR, stw, L, nbw)                       # (9 + 9*40, draws)
            BK, NU = C[:len(NS)], C[len(NS):].reshape(len(NS), NSEED, BDRAWS)
            B = {}
            B["EDGE"] = 100.0 * (BK - np.median(NU, axis=1))
            B["EDGE_FIXNULL"] = 100.0 * (BK - full_null_med[:, None])
            B["CAGR"] = 100.0 * BK
            B["S_FULL"] = boot_sharpe(BOOKW, stw, L, nbw)
            B["S_OOS"] = boot_sharpe(BOOKO, sto, L, nbo)
            B["DD"] = 100.0 * boot_maxdd(BOOKW, stw, L)
            BOOT[(panel, L)] = B

            # the null's own contribution to the pair-gap variance (the idea's mechanism)
            for i, j in combinations(range(len(NS)), 2):
                dbook = 100.0 * (BK[i] - BK[j])
                dnull = 100.0 * (np.median(NU[i], axis=0) - np.median(NU[j], axis=0))
                vb, vn = float(dbook.var(ddof=1)), float(dnull.var(ddof=1))
                cv = float(np.cov(dbook, dnull, ddof=1)[0, 1])
                varrows.append(dict(panel=panel, block_L=L, n_i=NS[i], n_j=NS[j],
                                    var_dEDGE=float((dbook - dnull).var(ddof=1)),
                                    var_dbook=vb, var_dnullmed=vn, cov=cv,
                                    null_var_share=vn / (vb + vn - 2 * cv) if (vb + vn - 2 * cv) > 0
                                    else np.nan))

            for stat in STATS:
                v, bm = FULL[stat], B[stat]
                spread = float(v.max() - v.min())
                gaps, agr, sds = [], [], []
                for i, j in combinations(range(len(NS)), 2):
                    g0 = v[i] - v[j]
                    db = bm[i] - bm[j]
                    db = db[np.isfinite(db)]
                    gaps.append(abs(g0))
                    agr.append(float((np.sign(db) == np.sign(g0)).mean()) if len(db) else np.nan)
                    sds.append(float(db.std(ddof=1)) if len(db) > 1 else np.nan)
                    if L == L_HEAD:
                        pairrows.append(dict(panel=panel, stat=stat, n_i=NS[i], n_j=NS[j],
                                             gap=g0, abs_gap=abs(g0), boot_sd=sds[-1],
                                             sign_agreement=agr[-1],
                                             resolved90=bool(agr[-1] >= QHEAD)))
                gaps, agr = np.array(gaps), np.array(agr)
                f90, f95 = measure_floor(gaps, agr, QHEAD), measure_floor(gaps, agr, QALT)
                order = np.argsort(-v, kind="stable")
                peak, runner = int(order[0]), int(order[1])
                pgap = float(v[peak] - v[runner])
                # TIE SET at q: the peak plus every rung the bootstrap cannot separate from it
                tie = [NS[peak]]
                for j in range(len(NS)):
                    if j == peak:
                        continue
                    db = bm[peak] - bm[j]
                    db = db[np.isfinite(db)]
                    a_ = float((np.sign(db) == np.sign(v[peak] - v[j])).mean()) if len(db) else 0.0
                    if a_ < QHEAD:
                        tie.append(NS[j])
                am = np.array(NS)[np.argmax(bm, axis=0)]
                cnt = np.array([(am == n).mean() for n in NS])
                w90, w90set, w90mass = widest_mass(cnt, NS, 0.90)
                floorrows.append(dict(
                    panel=panel, stat=stat, block_L=L, rungs=len(NS), units=(
                        "pp of CAGR" if stat in ("EDGE", "EDGE_FIXNULL", "CAGR") else
                        ("pp of MaxDD" if stat == "DD" else "Sharpe")),
                    peak=NS[peak], runner_up=NS[runner], peak_gap=pgap, spread=spread,
                    floor90=f90, floor95=f95, floor90_capped=min(f90, spread),
                    rel_floor=min(f90, spread) / spread if spread > 0 else np.nan,
                    rel_floor95=min(f95, spread) / spread if spread > 0 else np.nan,
                    n_unresolved90=int((agr < QHEAD).sum()), n_pairs=len(gaps),
                    unres_share=float((agr < QHEAD).mean()),
                    largest_unresolved=float(gaps[agr < QHEAD].max()) if (agr < QHEAD).any() else 0.0,
                    decided=bool(len(tie) == 1), tie_set=";".join(str(x) for x in sorted(tie)),
                    tie_size=len(tie), W90=w90, W90_set=";".join(str(x) for x in w90set),
                    W90_mass=w90mass, P_argmax_equals_full=float((am == NS[peak]).mean()),
                    modal_argmax=int(NS[int(np.argmax(cnt))]), P_modal=float(cnt.max()),
                    dist=";".join(f"{n}:{c:.3f}" for n, c in zip(NS, cnt))))
            P(f"   bootstrap L={L} done, 6 statistics x 36 pairs  ({time.time()-t0:.0f}s)")

        # ---- rule 8 on this panel ---------------------------------------------------------
        gp = pd.DataFrame([r for r in gridrows if r["panel"] == panel])
        for ch in CHOOSERS:
            if ch == "C_ISEDGE":
                ise = {n: next(r for r in edgerows if r["panel"] == panel
                               and r["N"] == n)["EDGE_IS_pp"] for n in NS}
                pick = int(max(ise, key=ise.get))
            else:
                key = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD", "C_ISCAGR": "IS_CAGR"}[ch]
                pick = int(gp.sort_values(key, ascending=False).iloc[0]["N"])
            r_ = gp[gp.N == pick].iloc[0]
            pickrows.append(dict(panel=panel, chooser=ch, pick=pick, CAGR=r_.CAGR,
                                 Sharpe=r_.Sharpe, MaxDD=r_.MaxDD, H1=r_.H1, H2=r_.H2,
                                 OOS_CAGR=r_.OOS_CAGR, OOS_Sharpe=r_.OOS_Sharpe,
                                 OOS_MaxDD=r_.OOS_MaxDD, pass4b=bool(r_.pass4b),
                                 pass4b_oos=bool(r_.pass4b_oos), pass4a=bool(r_.pass4a),
                                 spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                                 spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_Sharpe=lb["OOS_Sharpe"],
                                 best_possible_OOS_Sharpe=float(gp.OOS_Sharpe.max()),
                                 regret=float(gp.OOS_Sharpe.max() - r_.OOS_Sharpe)))

    gd, ed = pd.DataFrame(gridrows), pd.DataFrame(edgerows)
    fl, pr = pd.DataFrame(floorrows), pd.DataFrame(pairrows)
    pk, vr = pd.DataFrame(pickrows), pd.DataFrame(varrows)
    bn = pd.DataFrame(benchrows)

    # ------------------------------------------------------------------------------ GATES
    P("")
    P("# ---- GATES (printed before any result number) ----")
    # G8: 1098's own committed U56 EDGE floor / peak / gap / collapse reproduce
    u = fl[(fl.panel == "U56") & (fl.stat == "EDGE") & (fl.block_L == L_HEAD)].iloc[0]
    eU = np.array([float(ed[(ed.panel == "U56") & (ed.N == n)].EDGE_pp.iloc[0]) for n in NS])
    coll = float(eU.max() - eU[-1])
    d8 = max(abs(float(u.floor90) - A1098_U56["floor90"]) / A1098_U56["floor90"],
             abs(float(u.peak_gap) - A1098_U56["gap"]) / A1098_U56["gap"],
             abs(coll - A1098_U56["collapse"]) / A1098_U56["collapse"])
    gates["G8  CROSS-RUN 1098's committed U56 EDGE floor90 / peak gap / collapse"] = (
        d8, d8 < 0.05 and int(u.peak) == A1098_U56["peak"])
    b_ = fl[(fl.panel == "B136") & (fl.stat == "EDGE") & (fl.block_L == L_HEAD)].iloc[0]
    eB = np.array([float(ed[(ed.panel == "B136") & (ed.N == n)].EDGE_pp.iloc[0]) for n in NS])
    d8b = abs(float(eB.max() - eB[-1]) - A1098_B136["collapse"]) / A1098_B136["collapse"]
    gates["G8b CROSS-RUN 1098's committed B136 EDGE collapse"] = (d8b, d8b < 0.08)
    # G9: EDGE and EDGE_FIXNULL carry IDENTICAL point values (the control is a variance-only change)
    d9 = float(np.abs(fl[fl.stat == "EDGE"].sort_values(["panel", "block_L"]).peak_gap.values -
                      fl[fl.stat == "EDGE_FIXNULL"].sort_values(["panel", "block_L"]).peak_gap.values
                      ).max())
    gates["G9  EDGE_FIXNULL is a VARIANCE-only control (identical point gaps)"] = (d9, d9 == 0.0)
    # G10: every statistic's ladder is live
    sprmin = float(fl.spread.min())
    gates["G10 every statistic's ladder is live (min spread over 36 rows)"] = (sprmin, sprmin > 0)
    # G11: the three resamplers are EXACT on the identity draw (one block = the whole window)
    Rg = np.vstack([np.random.default_rng(bseed("G11")).normal(0.0004, 0.01, 1500),
                    np.random.default_rng(bseed("G11b")).normal(0.0002, 0.013, 1500)])
    st1 = np.zeros((1, 1), dtype=np.int64)
    d11 = max(
        float(np.abs(boot_cagr(np.log1p(Rg), st1, Rg.shape[1], 1)[:, 0] -
                     np.array([fmet(x)[0] for x in Rg])).max()),
        float(np.abs(boot_sharpe(Rg, st1, Rg.shape[1], 1)[:, 0] -
                     np.array([fsharpe(x) for x in Rg])).max()),
        float(np.abs(boot_maxdd(Rg, st1, Rg.shape[1])[:, 0] -
                     np.array([maxdd(x) for x in Rg])).max()))
    gates["G11 all three resamplers exact on the identity draw (CAGR / Sharpe / MaxDD)"] = (
        d11, d11 < 1e-12)
    ok = 0
    for k, (dv, good) in gates.items():
        P(f"   {'PASS' if good else 'FAIL'}  {k}: {dv:.3e}")
        gaterows.append(dict(gate=k, value=dv, passed=bool(good)))
        ok += bool(good)
    P(f"   {ok} of {len(gates)} gates pass")
    dump(pd.DataFrame(gaterows), "gates")
    dump(gd, "grid")
    dump(ed, "edge")
    dump(bn, "benchmarks")
    dump(fl, "floor")
    dump(pr, "pairs")
    dump(vr, "nullvar")

    # ------------------------------------------------------- THE LADDER, EVERY STATISTIC
    P("")
    P("# ---- THE NINE-RUNG LADDER, ALL SIX STATISTICS, BOTH PANELS (full-sample values) ----")
    P("   panel  statistic       " + "".join(f"{n:>9d}" for n in NS) + "   spread   argmax")
    for panel in PANELS:
        for stat in STATS:
            row = fl[(fl.panel == panel) & (fl.stat == stat) & (fl.block_L == L_HEAD)].iloc[0]
            if stat == "EDGE_FIXNULL":
                v = [float(ed[(ed.panel == panel) & (ed.N == n)].EDGE_pp.iloc[0]) for n in NS]
            elif stat == "EDGE":
                v = [float(ed[(ed.panel == panel) & (ed.N == n)].EDGE_pp.iloc[0]) for n in NS]
            elif stat == "CAGR":
                v = [100.0 * float(gd[(gd.panel == panel) & (gd.N == n)].CAGR.iloc[0]) for n in NS]
            elif stat == "S_FULL":
                v = [float(gd[(gd.panel == panel) & (gd.N == n)].Sharpe.iloc[0]) for n in NS]
            elif stat == "S_OOS":
                v = [float(gd[(gd.panel == panel) & (gd.N == n)].OOS_Sharpe.iloc[0]) for n in NS]
            else:
                v = [100.0 * float(gd[(gd.panel == panel) & (gd.N == n)].MaxDD.iloc[0]) for n in NS]
            P(f"   {panel:<6} {stat:<14} " + "".join(f"{x:+9.3f}" for x in v) +
              f"  {row.spread:7.3f}   n={row.peak}")

    # --------------------------------------------- THE ANSWER: THE THREE UNIT-FREE READINGS
    P("")
    P("# ---- THE ANSWER — THREE UNIT-FREE READINGS, ALL 36 (panel x statistic x L) ROWS ----")
    P("   panel  statistic     L    REL_FLOOR  UNRES/36   W90   tie set (q=0.90)          verdict")
    for panel in PANELS:
        for L in BLOCKS_L:
            for stat in STATS:
                r_ = fl[(fl.panel == panel) & (fl.stat == stat) & (fl.block_L == L)].iloc[0]
                P(f"   {panel:<6} {stat:<13} {L:<4} {r_.rel_floor:9.4f}  {r_.n_unresolved90:3d}/36"
                  f"   {r_.W90:3d}   {r_.tie_set:<24}  "
                  f"{'DECIDED' if r_.decided else 'TIE SET'}")

    # pairwise decision rule
    P("")
    P("# ---- PRE-REGISTERED DECISION RULE: X beats Y iff X wins >= 2 of "
      "{REL_FLOOR, UNRES, W90} ----")
    def beats(x, y, panel, L):
        a = fl[(fl.panel == panel) & (fl.stat == x) & (fl.block_L == L)].iloc[0]
        b = fl[(fl.panel == panel) & (fl.stat == y) & (fl.block_L == L)].iloc[0]
        w = int(a.rel_floor < b.rel_floor) + int(a.n_unresolved90 < b.n_unresolved90) + \
            int(a.W90 < b.W90)
        l = int(a.rel_floor > b.rel_floor) + int(a.n_unresolved90 > b.n_unresolved90) + \
            int(a.W90 > b.W90)
        return w, l, w >= 2

    cmprows = []
    for panel in PANELS:
        for L in BLOCKS_L:
            for x, y in combinations(STATS, 2):
                w, l, v = beats(x, y, panel, L)
                cmprows.append(dict(panel=panel, block_L=L, X=x, Y=y, X_wins=w, Y_wins=l,
                                    X_better=bool(v), Y_better=bool(l >= 2)))
    cmp_ = pd.DataFrame(cmprows)
    dump(cmp_, "compare")

    # (a) H_NULL_COSTS
    s = cmp_[(cmp_.X == "EDGE") & (cmp_.Y == "CAGR")]
    n_cagr_better = int(s.Y_better.sum())
    n_edge_better = int(s.X_better.sum())
    H_NULL_COSTS = bool(n_cagr_better > len(s) / 2)
    P(f"   (a) H_NULL_COSTS  CAGR (no null) beats EDGE at {n_cagr_better} of {len(s)} "
      f"(panel, L) points; EDGE beats CAGR at {n_edge_better}  -> "
      f"{'SUPPORTED' if H_NULL_COSTS else 'REFUTED'}")
    for _, r_ in s.iterrows():
        a = fl[(fl.panel == r_.panel) & (fl.stat == "EDGE") & (fl.block_L == r_.block_L)].iloc[0]
        b = fl[(fl.panel == r_.panel) & (fl.stat == "CAGR") & (fl.block_L == r_.block_L)].iloc[0]
        P(f"       {r_.panel:<6} L={r_.block_L:<4} EDGE rel {a.rel_floor:.4f} / unres "
          f"{a.n_unresolved90:2d} / W90 {a.W90}    CAGR rel {b.rel_floor:.4f} / unres "
          f"{b.n_unresolved90:2d} / W90 {b.W90}")

    # (b) H_FIXNULL_MID
    mid = 0
    for panel in PANELS:
        for L in BLOCKS_L:
            e = float(fl[(fl.panel == panel) & (fl.stat == "EDGE") & (fl.block_L == L)].rel_floor.iloc[0])
            f_ = float(fl[(fl.panel == panel) & (fl.stat == "EDGE_FIXNULL") & (fl.block_L == L)].rel_floor.iloc[0])
            c = float(fl[(fl.panel == panel) & (fl.stat == "CAGR") & (fl.block_L == L)].rel_floor.iloc[0])
            mid += int(min(e, c) <= f_ <= max(e, c))
    H_FIXNULL_MID = bool(mid > 6 / 2)
    P(f"   (b) H_FIXNULL_MID EDGE_FIXNULL's REL_FLOOR lies between EDGE's and CAGR's at "
      f"{mid} of 6 points -> {'SUPPORTED' if H_FIXNULL_MID else 'REFUTED'}")

    # (c) H_SOME_DECIDES
    dec = fl[(fl.block_L == L_HEAD) & (fl.stat.isin(NULLFREE)) & (fl.decided)]
    H_SOME_DECIDES = bool(len(dec) > 0)
    P(f"   (c) H_SOME_DECIDES null-free statistics that DECIDE the ladder at L=63: {len(dec)} "
      f"of {2*len(NULLFREE)} -> {'SUPPORTED' if H_SOME_DECIDES else 'REFUTED'}"
      + ("  [" + ", ".join(f"{r.panel} {r.stat} n={r.peak}" for _, r in dec.iterrows()) + "]"
         if len(dec) else ""))

    # (d) H_DD_WORST  (e) H_OOS_WORSE
    med = fl.groupby("stat").rel_floor.median().sort_values(ascending=False)
    H_DD_WORST = bool(med.index[0] == "DD")
    P("   (d) H_DD_WORST    median REL_FLOOR over the 6 (panel, L) points, worst first:")
    for k, v in med.items():
        P(f"       {k:<14} {v:.4f}   (median UNRES/36 "
          f"{fl[fl.stat==k].n_unresolved90.median():.1f}, median W90 {fl[fl.stat==k].W90.median():.1f})")
    P(f"       -> {'SUPPORTED' if H_DD_WORST else 'REFUTED'}")
    s2 = cmp_[(cmp_.X == "S_FULL") & (cmp_.Y == "S_OOS")]
    H_OOS_WORSE = bool(int(s2.X_better.sum()) > len(s2) / 2)
    P(f"   (e) H_OOS_WORSE   S_FULL beats S_OOS at {int(s2.X_better.sum())} of {len(s2)} "
      f"points (S_OOS beats S_FULL at {int(s2.Y_better.sum())}) -> "
      f"{'SUPPORTED' if H_OOS_WORSE else 'REFUTED'}")

    # (f) H_L_RISES
    rises = 0
    for panel in PANELS:
        for stat in STATS:
            v = [float(fl[(fl.panel == panel) & (fl.stat == stat) & (fl.block_L == L)].rel_floor.iloc[0])
                 for L in BLOCKS_L]
            rises += int(v[-1] > v[0])
    H_L_RISES = bool(rises > 12 / 2)
    P(f"   (f) H_L_RISES     REL_FLOOR(L=126) > REL_FLOOR(L=21) at {rises} of 12 "
      f"(panel, statistic) cells -> {'SUPPORTED' if H_L_RISES else 'REFUTED'}")

    # ---------------------------------------- THE MECHANISM: what the null median contributes
    P("")
    P("# ---- THE MECHANISM — the null median's share of the EDGE pair-gap variance ----")
    P("   Var(dEDGE) = Var(dBOOK) + Var(dNULLMED) - 2 Cov.  If the idea's premise is right,")
    P("   the null term is a material share; if it is small, EDGE and CAGR must resolve alike.")
    for panel in PANELS:
        for L in BLOCKS_L:
            s3 = vr[(vr.panel == panel) & (vr.block_L == L)]
            P(f"   {panel:<6} L={L:<4} median null-var share {s3.null_var_share.median():+.4f}  "
              f"(min {s3.null_var_share.min():+.4f}, max {s3.null_var_share.max():+.4f});  median "
              f"sd(dBOOK) {np.sqrt(s3.var_dbook).median():.4f} pp vs sd(dNULLMED) "
              f"{np.sqrt(s3.var_dnullmed).median():.4f} pp vs sd(dEDGE) "
              f"{np.sqrt(s3.var_dEDGE).median():.4f} pp")

    # -------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("")
    P("# ---- RULE 8 (walk-forward) AND BOTH KEEP PATHS — the floor is NOT a keep path ----")
    dump(pk, "picks")
    P("   n chosen on IS 2009-2016 ALONE, four choosers, OOS 2017-2026 read ONCE:")
    for _, r_ in pk.iterrows():
        P(f"   {r_.panel:<6} {r_.chooser:<12} pick n={r_.pick:<3} full {r_.CAGR:7.2%} / "
          f"{r_.Sharpe:.4f} / {r_.MaxDD:7.2%}  halves {r_.H1:.4f}/{r_.H2:.4f}  OOS "
          f"{r_.OOS_CAGR:7.2%} / {r_.OOS_Sharpe:.4f} / {r_.OOS_MaxDD:7.2%}   4b full "
          f"{'Y' if r_.pass4b else 'n'}  4b OOS {'Y' if r_.pass4b_oos else 'n'}  4a "
          f"{'Y' if r_.pass4a else 'n'}   regret {r_.regret:+.4f}")
    P(f"   {len(pk)} IS picks: 4b full {int(pk.pass4b.sum())}, 4b OOS {int(pk.pass4b_oos.sum())}, "
      f"4a {int(pk.pass4a.sum())}, median OOS Sharpe {pk.OOS_Sharpe.median():.4f}, median regret "
      f"{pk.regret.median():+.4f}")
    P(f"   whole grid, {len(gd)} rungs: 4b full {int(gd.pass4b.sum())}, 4b OOS "
      f"{int(gd.pass4b_oos.sum())}, 4a {int(gd.pass4a.sum())}")
    P("   every rung, both panels:")
    for _, r_ in gd.iterrows():
        P(f"   {r_.panel:<6} n={r_.N:<3} full {r_.CAGR:7.2%} / {r_.Sharpe:.4f} / {r_.MaxDD:7.2%}  "
          f"halves {r_.H1:.4f}/{r_.H2:.4f}  OOS {r_.OOS_CAGR:7.2%} / {r_.OOS_Sharpe:.4f} / "
          f"{r_.OOS_MaxDD:7.2%}  turn {r_.turnover:.2f}x/yr   4b full "
          f"{'Y' if r_.pass4b else 'n'}  4b OOS {'Y' if r_.pass4b_oos else 'n'}  4a "
          f"{'Y' if r_.pass4a else 'n'}")
    for _, r_ in bn.iterrows():
        P(f"   BENCH {r_.panel:<6} {r_.series:<14} full {r_.CAGR:7.2%} / {r_.Sharpe:.4f} / "
          f"{r_.MaxDD:7.2%}  halves {r_.H1:.4f}/{r_.H2:.4f}  OOS {r_.OOS_CAGR:7.2%} / "
          f"{r_.OOS_Sharpe:.4f} / {r_.OOS_MaxDD:7.2%}")

    hyp = pd.DataFrame([
        dict(hypothesis="H_NULL_COSTS", declared="EDGE resolves worse than CAGR, majority of 6",
             result="SUPPORTED" if H_NULL_COSTS else "REFUTED",
             detail=f"CAGR better at {n_cagr_better}/6, EDGE better at {n_edge_better}/6"),
        dict(hypothesis="H_FIXNULL_MID", declared="EDGE_FIXNULL rel_floor between EDGE and CAGR",
             result="SUPPORTED" if H_FIXNULL_MID else "REFUTED", detail=f"{mid}/6"),
        dict(hypothesis="H_SOME_DECIDES", declared="some null-free statistic decides at L=63",
             result="SUPPORTED" if H_SOME_DECIDES else "REFUTED",
             detail=f"{len(dec)} of {2*len(NULLFREE)} null-free cells decided"),
        dict(hypothesis="H_DD_WORST", declared="DD resolves worst of the six",
             result="SUPPORTED" if H_DD_WORST else "REFUTED",
             detail="worst median rel_floor = " + str(med.index[0])),
        dict(hypothesis="H_OOS_WORSE", declared="S_OOS resolves worse than S_FULL",
             result="SUPPORTED" if H_OOS_WORSE else "REFUTED",
             detail=f"S_FULL better at {int(s2.X_better.sum())}/6"),
        dict(hypothesis="H_L_RISES", declared="rel_floor rises with L, majority of 12",
             result="SUPPORTED" if H_L_RISES else "REFUTED", detail=f"{rises}/12"),
    ])
    dump(hyp, "hypotheses")
    P("")
    P("# ---- HYPOTHESES ----")
    for _, r_ in hyp.iterrows():
        P(f"   {r_.hypothesis:<16} {r_.result:<10} {r_.detail}")
    P(f"   {int((hyp.result == 'SUPPORTED').sum())} of {len(hyp)} supported")
    P("")
    P(f"# SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels, so every level is")
    P("#   optimistic.  Rung-pair gaps and their sign agreement contrast two books over the same")
    P("#   inflated tape and the bias very largely cancels out of them; it does NOT cancel out")
    P("#   of the 4b legs above, which are measured against SPY.")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
