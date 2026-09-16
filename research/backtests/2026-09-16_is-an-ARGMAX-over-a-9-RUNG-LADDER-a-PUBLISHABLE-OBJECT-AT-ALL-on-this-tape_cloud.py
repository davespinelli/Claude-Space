#!/usr/bin/env python3
"""Idea 1098 (cloud lane, 2026-09-16) — is an ARGMAX over a 9-RUNG LADDER a PUBLISHABLE OBJECT
AT ALL on this tape?

QUESTION (QUEUE idea 1098, verbatim; QUEUE carries TWO lines numbered 1098 — defect 932 — and
this is the argmax-resolution one)
    idea 1085's U56 EDGE argmax reads 12 (uniform null), 5 (rank-matched null) and 5/12/12 across
    seed counts, while 1086's reads 12/8/12 across holds; four ways of asking the same question
    give three answers.  Bootstrap the argmax's own sampling distribution at this seed count and
    ladder spacing and report the width, then state a resolution floor below which no argmax in
    this family should be published.  Max 2 params (seeds, ladder spacing).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: SEEDS S {5, 10, 20, 40} (nested — the first S of the same 40 draws, so the
    seed dial moves PRECISION of the null median and nothing else) x LADDER SPACING {FULL9 =
    1082's nine rungs, ALT5 = {5,10,15,25,40}, COARSE3 = {5,15,40}} — every spacing a SUBSET of
    FULL9, so all three read the same paths and differ only in which rungs the argmax may land
    on.  12 cells per panel, 24 in total, ALL published.  Everything else is 1082/1086's
    construction frozen: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, W cadence, min hold 126,
    10 bps, LAG 1, warm-up 260, IS end 2016-12-31.  BLOCK LENGTH is not a dial: the headline is
    L = 63 and L in {21, 126} is reported beside it as a labelled robustness axis, never selected
    on.

WHAT IS BOOTSTRAPPED, AND WHAT THAT PRICES
    EDGE(n) = 100 * (CAGR_book(n) - median_seeds CAGR_null(n)) in pp, with 1082's REBUILT
    convention: every null path is re-run at the gross lam*0.75 that equalises its realised
    |MaxDD| with the book's, lam in (0, 1], found by 34-step bisection.  The bootstrap draws
    CIRCULAR BLOCKS of trading days and applies ONE index JOINTLY to the book path, all 40 null
    paths and every rung, because book and null are drawn from the same pool over the same tape
    and an independent resample would destroy the dependence that makes EDGE a paired quantity.
    CAGR over a block-resampled path is exact from block sums of log1p (order does not matter for
    a product), which is what makes 1,000 draws x 3 block lengths x 2 panels cheap.

    LIMITATION, DECLARED IN ADVANCE AND NOT DISCOVERED AFTERWARDS: lam is matched ONCE on the
    real tape and held fixed inside the bootstrap.  A per-replicate rematch would add variance,
    so every width published here is a LOWER bound on the argmax's true sampling width — the
    conservative direction for a conclusion of the form "this argmax is not resolved".

DECLARED BEFORE ANY NUMBER
    (a) H_STABLE, the bar for "publishable as a point": P(bootstrap argmax == the full-sample
        argmax) >= 0.50 at S = 40 on FULL9.  The RIVAL, named in advance: it is well below 0.5,
        in which case 1085's three answers (5 / 12 / 12) and 1086's (12 / 8 / 12) are ONE
        measurement seen four times, not four disagreeing measurements.
    (b) H_WIDTH: the smallest set of rungs carrying 90% of the argmax mass spans >= 3 rungs.
    (c) H_FLOOR: the full-sample peak-minus-runner-up EDGE gap is BELOW this tape's own 90%
        sign-resolution floor — i.e. the record's argmax is below the resolution of the ladder it
        is read off.  The floor is measured, not assumed: over all rung pairs, the smallest
        |dEDGE| above which the bootstrap agrees with the full-sample sign at least 90% of the
        time.
    (d) H_SEED: the width is a TAPE fact, not a seed-count fact (width at S=40 >= 0.8x width at
        S=5).  If it is a seed fact instead, the record can fix it by buying seeds; if it is a
        tape fact, it cannot be fixed at all on 17.6 years.
    (e) H_SPACE: coarsening the ladder RAISES apparent stability without adding information
        (P(stable) on COARSE3 > on FULL9).  A spacing dial that buys stability is a warning about
        every coarse ladder in the record, not a way to publish an argmax.
    (f) EDGE IS NOT A KEEP PATH, exactly as 1082 declared.  4a and 4b are scored at every rung
        and rule 8 picks n on 2009-2016 alone, inside each spacing, separately.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels.  Book and null are
    drawn from the same pool over the same tape, so the bias very largely cancels out of EDGE and
    out of the argmax; it does NOT cancel out of the 4b legs, which are measured against SPY.
"""
from __future__ import annotations

import hashlib
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

DATE = "2026-09-16"
SLUG = "is-an-ARGMAX-over-a-9-RUNG-LADDER-a-PUBLISHABLE-OBJECT-AT-ALL-on-this-tape"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
HOLD = 126
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
BISECT = 34

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]              # 1082's ladder verbatim
SEEDGRID = [5, 10, 20, 40]                            # dial 1 (nested)
NSEED_MAX = max(SEEDGRID)
SPACINGS = {"FULL9": NS, "ALT5": [5, 10, 15, 25, 40], "COARSE3": [5, 15, 40]}   # dial 2
BDRAWS = 1000
BLOCKS_L = [21, 63, 126]
L_HEAD = 63
PANELS = ["U56", "B136"]
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR", "C_ISEDGE"]

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1082_EDGE = {"U56": [5.95, 5.35, 6.21, 6.82, 5.22, 5.12, 2.95, 1.55, 0.41],
              "B136": [5.72, 5.24, 8.32, 6.52, 6.83, 4.93, 4.27, 2.81, 1.85]}   # 1082 CHANGELOG
A1085_U56_ARGMAX = {5: 12, 10: 5, 20: 12, 40: 12}     # 1085/1082's seed-dial argmax on U56
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
    """1082/1086/1094's recipe verbatim, so the null draws are the SAME objects."""
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ------------------------------------------------- 1082's runner and rescaler, copied verbatim
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


# ---------------------------------------------------------------- the bootstrap machinery
def block_starts(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    return rng.integers(0, T, size=(ndraws, nb)), nb


def boot_cagr(LOGR, starts, L, nb, chunk=100):
    """CAGR of every row of LOGR under CIRCULAR block resampling, exactly (a product does not
    care about order, so block sums of log1p suffice).  LOGR is (paths, T).  Chunked over draws
    so peak memory stays near (paths x chunk x nb) floats."""
    D = np.concatenate([LOGR, LOGR], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    out = np.empty((LOGR.shape[0], starts.shape[0]))
    for a in range(0, starts.shape[0], chunk):
        st = starts[a:a + chunk]
        out[:, a:a + chunk] = (CS[:, st + L] - CS[:, st]).sum(axis=2)
    return np.expm1(out * (252.0 / (nb * L)))


def widest_mass(counts, rungs, q=0.90):
    """Smallest contiguous-in-RANK set of rungs carrying >= q of the argmax mass, returned as
    (n_rungs, [rungs], mass).  Rungs are ordered as the ladder is."""
    k = len(rungs)
    best = None
    for w in range(1, k + 1):
        for i in range(0, k - w + 1):
            m = counts[i:i + w].sum()
            if m >= q:
                cand = (w, [rungs[j] for j in range(i, i + w)], float(m))
                if best is None or cand[0] < best[0]:
                    best = cand
        if best is not None:
            break
    if best is None:
        best = (k, list(rungs), float(counts.sum()))
    return best


def main():
    t0 = time.time()
    P(f"# Idea 1098 (cloud lane, {DATE}) — is an ARGMAX over a 9-RUNG LADDER a PUBLISHABLE")
    P("#   OBJECT AT ALL on this tape?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): SEEDS {SEEDGRID} (nested) x SPACING "
      f"{ {k: v for k, v in SPACINGS.items()} } = 12 cells per panel, 24 total, ALL published.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap {CAPNAME}, max_vol {MAXVOL}, gross {GROSS0}, cadence")
    P(f"#   {FREQ}, min hold {HOLD}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}.")
    P(f"#   BLOCK LENGTH is NOT a dial: headline L={L_HEAD}, L in {BLOCKS_L} reported beside it.")
    P(f"# BOOTSTRAP: {BDRAWS} circular-block draws, ONE index applied JOINTLY to the book, all")
    P(f"#   {NSEED_MAX} null paths and every rung.  lam is matched ONCE on the real tape and held")
    P("#   fixed inside the bootstrap, so every width here is a LOWER bound — declared in")
    P("#   advance, and the conservative direction for a 'not resolved' conclusion.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_STABLE — P(bootstrap argmax == full-sample argmax) >= 0.50 at S=40 on FULL9 is")
    P("#       the bar for publishing an argmax as a point.  RIVAL: it is well below 0.5, and")
    P("#       1085's 5/12/12 and 1086's 12/8/12 are ONE measurement seen four times.")
    P("#   (b) H_WIDTH — the 90% argmax set spans >= 3 rungs.")
    P("#   (c) H_FLOOR — the peak-minus-runner-up gap is BELOW this tape's own 90% sign-")
    P("#       resolution floor, measured over all rung pairs rather than assumed.")
    P("#   (d) H_SEED — the width is a TAPE fact, not a seed-count fact (S=40 width >= 0.8x S=5).")
    P("#   (e) H_SPACE — coarsening RAISES apparent stability without adding information.")
    P("#   (f) EDGE IS NOT A KEEP PATH: 4a/4b are scored at every rung and rule 8 picks n on")
    P("#       2009-2016 alone, inside each spacing, separately.")
    P("")

    gates, gaterows = {}, []
    edgerows, bootrows, pairrows, floorrows, pickrows, gridrows, benchrows = [], [], [], [], [], [], []

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        reb = np.flatnonzero(mk)
        warm, ins, oos = windows(idx)
        yrs = warm.sum() / 252.0
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks_m(live, warm, ins, oos)
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        benchrows.append(dict(panel=panel, series="RULESv2", **lb))
        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{yrs:.2f} scored years")
        P(f"   SPY full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2 live full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  OOS "
          f"{lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        P(f"   4b bars: DD cap {DD_CAP*abs(sb['MaxDD']):.2%} full / "
          f"{DD_CAP*abs(sb['OOS_MaxDD']):.2%} OOS;  CAGR floor {CAGR_FLOOR*sb['CAGR']:.2%} full")

        # ---- gates that do not need the ladder ------------------------------------------
        if panel == "U56":
            W20 = build(rank_key, elig, priced, reb, 20, HOLD, T, K, GROSS0)
            g20, t20 = nrun(rets, lagmat(W20), mkl)
            r20 = g20 - t20 * COST / 1e4
            eng = backtest(px, pd.DataFrame(W20, index=idx, columns=px.columns),
                           cost_bps=COST, freq=FREQ)["returns"].values
            d = float(np.abs(r20[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56 N=20 H=126 @ 10 bps)"] = (d, d < 1e-12)
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            d1b = float(np.abs(f20(1.0) - r20).max())
            gates["G1b gross_rescaler(1.0) == nrun (the bisection kernel is the same book)"] = (
                d1b, d1b < 1e-12)
            m = fmet(r20[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082's committed U56 W/H126 N=20 triple"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d5 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G5 live RULES v2 MaxDD == committed -12.05%"] = (d5, d5 < 5e-4)
            a = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0)).random(6)
            b_ = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0)).random(6)
            gates["G7 determinism of 1082's seed recipe"] = (float(np.abs(a - b_).max()), True)

        # ---- the ladder: book + 40 DD-matched nulls at every rung ------------------------
        BOOKR = {}        # n -> book net returns over the warm window
        NULLR = {}        # n -> (40, T_warm) matched null net returns
        for N in NS:
            W = build(rank_key, elig, priced, reb, N, HOLD, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(W), mkl)
            r = g - tn * COST / 1e4
            b = blocks_m(r, warm, ins, oos)
            BOOKR[N] = r[warm]
            nulls, lams, drier, nis = [], [], 0, []
            for s in range(NSEED_MAX):
                rng = np.random.default_rng(mdseed(panel, N, CAPNAME, s))
                Wn = build_null(rng, priced, reb, N, HOLD, T, K, GROSS0)
                fn = gross_rescaler(rets, lagmat(Wn), mkl)
                lr = lam_rebuilt(fn, warm, b["MaxDD"])
                if lr is None:
                    drier += 1
                    lr = 1.0
                nulls.append(fn(lr)[warm])
                lams.append(lr)
                lri = lam_rebuilt(fn, ins, b["IS_MaxDD"])          # 1082's IS arm, for C_ISEDGE
                nis.append(fmet(fn(1.0)[ins] if lri is None else fn(lri)[ins])[0])
            NULLR[N] = np.array(nulls)
            ncagr = np.array([fmet(x)[0] for x in NULLR[N]])
            nis = np.array(nis)
            l4b, l4a, l4o = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
            row = dict(panel=panel, N=N, turnover=float(tn[warm].sum() / yrs), **b, **l4b, **l4a,
                       **l4o, pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                       pass4b_oos=all(l4o.values()), lam_median=float(np.median(lams)),
                       n_already_drier=drier)
            for S in SEEDGRID:
                e = 100.0 * (b["CAGR"] - float(np.median(ncagr[:S])))
                row[f"EDGE_S{S}"] = e
                row[f"EDGE_se_S{S}"] = (100.0 * 1.2533 * float(ncagr[:S].std(ddof=1)) /
                                        np.sqrt(S)) if S > 1 else np.nan
                edgerows.append(dict(panel=panel, N=N, seeds=S, EDGE_pp=e,
                                     EDGE_IS_pp=100.0 * (b["IS_CAGR"] -
                                                         float(np.median(nis[:S]))),
                                     book_CAGR=b["CAGR"],
                                     null_CAGR_med=float(np.median(ncagr[:S])),
                                     null_CAGR_sd=float(ncagr[:S].std(ddof=1)),
                                     EDGE_se_pp=row[f"EDGE_se_S{S}"],
                                     lam_median=float(np.median(lams[:S])),
                                     book_pct_of_null=float((ncagr[:S] < b["CAGR"]).mean())))
            gridrows.append(row)
            P(f"   N={N:2d}  book {b['CAGR']:7.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:7.2%}  "
              f"EDGE(S=40) {row['EDGE_S40']:+6.2f} pp (SE {row['EDGE_se_S40']:.2f})  lam~"
              f"{np.median(lams):.3f}  drier {drier}/40  ({time.time()-t0:.0f}s)")

        # ---- CROSS-RUN gate on 1082's committed EDGE ladder ------------------------------
        mine = [next(r for r in edgerows if r["panel"] == panel and r["N"] == N
                     and r["seeds"] == 40)["EDGE_pp"] for N in NS]
        dx = float(np.abs(np.array(mine) - np.array(A1082_EDGE[panel])).max())
        gates[f"G_XRUN {panel}: 1082's nine committed EDGE figures reproduce"] = (dx, dx < 5.1e-3)

        # ---- the bootstrap ---------------------------------------------------------------
        Tw = int(warm.sum())
        paths = [BOOKR[N] for N in NS] + [NULLR[N][s] for N in NS for s in range(NSEED_MAX)]
        LOGR = np.log1p(np.array(paths))
        nb_book = len(NS)
        for L in BLOCKS_L:
            rng = np.random.default_rng(mdseed("boot", panel, L))
            starts, nb = block_starts(rng, Tw, L, BDRAWS)
            C = boot_cagr(LOGR, starts, L, nb)                   # (paths, draws)
            BK = C[:nb_book]                                      # (rungs, draws)
            NU = C[nb_book:].reshape(len(NS), NSEED_MAX, BDRAWS)
            for S in SEEDGRID:
                E = 100.0 * (BK - np.median(NU[:, :S, :], axis=1))    # (rungs, draws)
                for sp, rungs in SPACINGS.items():
                    ii = [NS.index(n) for n in rungs]
                    Es = E[ii]
                    am = np.array(rungs)[np.argmax(Es, axis=0)]
                    full = [next(r for r in edgerows if r["panel"] == panel and r["N"] == n
                                 and r["seeds"] == S)["EDGE_pp"] for n in rungs]
                    fa = rungs[int(np.argmax(full))]
                    cnt = np.array([(am == n).mean() for n in rungs])
                    w, wset, mass = widest_mass(cnt, rungs)
                    order = np.argsort(full)[::-1]
                    gap = float(full[order[0]] - full[order[1]])
                    bootrows.append(dict(panel=panel, block_L=L, seeds=S, spacing=sp,
                                         n_rungs=len(rungs), full_argmax=fa,
                                         P_argmax_equals_full=float((am == fa).mean()),
                                         modal_argmax=int(rungs[int(np.argmax(cnt))]),
                                         P_modal=float(cnt.max()),
                                         width90_rungs=w, width90_set=";".join(str(x) for x in wset),
                                         width90_mass=mass,
                                         peak_minus_runnerup_pp=gap,
                                         runner_up=int(rungs[order[1]]),
                                         P_argmax_5=float((am == 5).mean()),
                                         P_argmax_12=float((am == 12).mean())
                                         if 12 in rungs else np.nan,
                                         dist=";".join(f"{n}:{c:.3f}" for n, c in zip(rungs, cnt))))
                # pair table + resolution floor, headline block length and FULL9 only
                if L == L_HEAD and S == NSEED_MAX:
                    fullE = np.array([next(r for r in edgerows if r["panel"] == panel
                                           and r["N"] == n and r["seeds"] == S)["EDGE_pp"]
                                      for n in NS])
                    for i in range(len(NS)):
                        for j in range(i + 1, len(NS)):
                            d0 = fullE[i] - fullE[j]
                            db = E[i] - E[j]
                            agree = float((np.sign(db) == np.sign(d0)).mean())
                            pairrows.append(dict(panel=panel, n_i=NS[i], n_j=NS[j],
                                                 dEDGE_pp=d0, abs_dEDGE_pp=abs(d0),
                                                 boot_sd_pp=float(db.std(ddof=1)),
                                                 sign_agreement=agree))
            P(f"   bootstrap L={L} done ({time.time()-t0:.0f}s)")

        # ---- rule 8 inside each spacing ---------------------------------------------------
        gp = pd.DataFrame([r for r in gridrows if r["panel"] == panel])
        for sp, rungs in SPACINGS.items():
            g_ = gp[gp.N.isin(rungs)]
            for S in SEEDGRID:
                for ch in CHOOSERS:
                    if ch == "C_ISEDGE":
                        key = None
                        isedge = {n: next(r for r in edgerows if r["panel"] == panel
                                          and r["N"] == n and r["seeds"] == S)["EDGE_IS_pp"]
                                  for n in rungs}   # IS window ONLY — rule 8
                        pick = int(max(isedge, key=isedge.get))
                    else:
                        key = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD",
                               "C_ISCAGR": "IS_CAGR"}[ch]
                        pick = int(g_.sort_values(key, ascending=False).iloc[0]["N"])
                    r = g_[g_.N == pick].iloc[0]
                    pickrows.append(dict(panel=panel, spacing=sp, seeds=S, chooser=ch, pick=pick,
                                         OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                         OOS_MaxDD=r.OOS_MaxDD, CAGR=r.CAGR, Sharpe=r.Sharpe,
                                         MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                                         pass4b=bool(r.pass4b), pass4b_oos=bool(r.pass4b_oos),
                                         pass4a=bool(r.pass4a),
                                         spy_OOS_CAGR=sb["OOS_CAGR"],
                                         spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                         spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                         live_OOS_Sharpe=lb["OOS_Sharpe"]))

    ed = pd.DataFrame(edgerows)
    bt = pd.DataFrame(bootrows)
    pr = pd.DataFrame(pairrows)
    pk = pd.DataFrame(pickrows)
    gd = pd.DataFrame(gridrows)

    P("")
    P("# ---- GATES (printed before any result number) ----")
    ok = 0
    for k, (d, good) in gates.items():
        P(f"   {'PASS' if good else 'FAIL'}  {k}: {d:.3e}")
        gaterows.append(dict(gate=k, value=d, passed=bool(good)))
        ok += bool(good)
    P(f"   {ok} of {len(gates)} gates pass")

    P("")
    P("# ---- THE ARGMAX'S OWN SAMPLING DISTRIBUTION (headline L=63) ----")
    for panel in PANELS:
        for sp in SPACINGS:
            for S in SEEDGRID:
                r = bt[(bt.panel == panel) & (bt.block_L == L_HEAD) & (bt.spacing == sp)
                       & (bt.seeds == S)].iloc[0]
                P(f"   {panel:4s} {sp:7s} S={S:2d}: full argmax {r.full_argmax:2d}, "
                  f"P(argmax==full) {r.P_argmax_equals_full:.3f}, modal {r.modal_argmax:2d} "
                  f"(P {r.P_modal:.3f}), 90% set {{{r.width90_set}}} = {r.width90_rungs} rungs, "
                  f"peak-runner-up {r.peak_minus_runnerup_pp:+.2f} pp (vs n={r.runner_up})")
    P("")
    P("   BLOCK-LENGTH robustness (reported, never selected on), FULL9 / S=40:")
    for panel in PANELS:
        for L in BLOCKS_L:
            r = bt[(bt.panel == panel) & (bt.block_L == L) & (bt.spacing == "FULL9")
                   & (bt.seeds == 40)].iloc[0]
            P(f"     {panel:4s} L={L:3d}: P(argmax==full) {r.P_argmax_equals_full:.3f}, 90% set "
              f"{{{r.width90_set}}}, full distribution {r.dist}")

    P("")
    P("# ---- THE RESOLUTION FLOOR (measured, not assumed) ----")
    hyp = []
    for panel in PANELS:
        s = pr[pr.panel == panel].sort_values("abs_dEDGE_pp")
        floor = np.nan
        for i in range(len(s)):
            if (s.iloc[i:].sign_agreement >= 0.90).all():
                floor = float(s.iloc[i].abs_dEDGE_pp)
                break
        floor95 = np.nan
        for i in range(len(s)):
            if (s.iloc[i:].sign_agreement >= 0.95).all():
                floor95 = float(s.iloc[i].abs_dEDGE_pp)
                break
        pk40 = bt[(bt.panel == panel) & (bt.block_L == L_HEAD) & (bt.spacing == "FULL9")
                  & (bt.seeds == 40)].iloc[0]
        P(f"   {panel}: 90% sign-resolution floor {floor:.2f} pp of CAGR (95%: {floor95:.2f} pp) "
          f"over {len(s)} rung pairs; the published peak beats its runner-up by "
          f"{pk40.peak_minus_runnerup_pp:.2f} pp -> "
          f"{'ABOVE' if pk40.peak_minus_runnerup_pp >= floor else 'BELOW'} the floor")
        nres = int((s.sign_agreement < 0.90).sum())
        P(f"      {nres} of {len(s)} rung pairs are NOT sign-resolved at 90%; the largest "
          f"unresolved gap is {s[s.sign_agreement < 0.90].abs_dEDGE_pp.max():.2f} pp")
        floorrows.append(dict(panel=panel, floor90_pp=floor, floor95_pp=floor95,
                              peak_minus_runnerup_pp=float(pk40.peak_minus_runnerup_pp),
                              peak_above_floor=bool(pk40.peak_minus_runnerup_pp >= floor),
                              pairs=len(s), pairs_unresolved90=nres,
                              largest_unresolved_gap_pp=float(
                                  s[s.sign_agreement < 0.90].abs_dEDGE_pp.max())
                              if nres else 0.0))
        hyp.append(dict(hypothesis=f"H_FLOOR ({panel}): the peak-minus-runner-up gap is BELOW the "
                                   f"90% sign-resolution floor", declared="below",
                        observed=f"{pk40.peak_minus_runnerup_pp:.2f} vs floor {floor:.2f} pp",
                        passed=bool(pk40.peak_minus_runnerup_pp < floor)))

    for panel in PANELS:
        r40 = bt[(bt.panel == panel) & (bt.block_L == L_HEAD) & (bt.spacing == "FULL9")
                 & (bt.seeds == 40)].iloc[0]
        r5 = bt[(bt.panel == panel) & (bt.block_L == L_HEAD) & (bt.spacing == "FULL9")
                & (bt.seeds == 5)].iloc[0]
        rc = bt[(bt.panel == panel) & (bt.block_L == L_HEAD) & (bt.spacing == "COARSE3")
                & (bt.seeds == 40)].iloc[0]
        hyp += [dict(hypothesis=f"H_STABLE ({panel}): P(argmax == full-sample argmax) >= 0.50 at "
                                f"S=40 on FULL9", declared=">=0.50",
                     observed=f"{r40.P_argmax_equals_full:.3f}",
                     passed=bool(r40.P_argmax_equals_full >= 0.50)),
                dict(hypothesis=f"H_WIDTH ({panel}): the 90% argmax set spans >= 3 rungs",
                     declared=">=3", observed=f"{r40.width90_rungs} ({r40.width90_set})",
                     passed=bool(r40.width90_rungs >= 3)),
                dict(hypothesis=f"H_SEED ({panel}): width(S=40) >= 0.8 x width(S=5) — a TAPE "
                                f"fact, not a seed fact", declared=">=0.8x",
                     observed=f"{r40.width90_rungs} vs {r5.width90_rungs}",
                     passed=bool(r40.width90_rungs >= 0.8 * r5.width90_rungs)),
                dict(hypothesis=f"H_SPACE ({panel}): coarsening RAISES apparent stability "
                                f"(COARSE3 > FULL9)", declared="higher",
                     observed=f"{rc.P_argmax_equals_full:.3f} vs {r40.P_argmax_equals_full:.3f}",
                     passed=bool(rc.P_argmax_equals_full > r40.P_argmax_equals_full))]

    # H_1085: are 1085/1082's three answers inside the bootstrap's own width?
    u = bt[(bt.panel == "U56") & (bt.block_L == L_HEAD) & (bt.spacing == "FULL9")]
    seen = sorted(set(A1085_U56_ARGMAX.values()) | {5})
    mass = {}
    for S in SEEDGRID:
        r = u[u.seeds == S].iloc[0]
        d = dict(x.split(":") for x in r.dist.split(";"))
        mass[S] = {n: float(d[str(n)]) for n in seen}
    P("")
    P("# ---- H_1085: 1085/1082 reported the U56 argmax as 12 / 5 / 12 / 12 across S = 5/10/20/40")
    for S in SEEDGRID:
        P(f"   S={S:2d}: committed argmax {A1085_U56_ARGMAX[S]:2d}; this run's bootstrap mass on "
          f"n=5 {mass[S][5]:.3f}, on n=12 {mass[S][12]:.3f}")
    inside = all(mass[S][A1085_U56_ARGMAX[S]] > 0.02 for S in SEEDGRID)
    hyp.append(dict(hypothesis="H_1085: every committed U56 argmax in the seed dial carries "
                               "non-trivial bootstrap mass (>2%), i.e. the four answers are ONE "
                               "measurement", declared="all four",
                    observed=";".join(f"S{S}:{mass[S][A1085_U56_ARGMAX[S]]:.3f}"
                                      for S in SEEDGRID), passed=bool(inside)))

    P("")
    P("# ---- RULE 8 WALK-FORWARD AND BOTH KEEP PATHS ----")
    for panel in PANELS:
        sbq = [r for r in benchrows if r["panel"] == panel and r["series"] == "SPY"][0]
        P(f"   {panel} SPY OOS {sbq['OOS_CAGR']:.2%} / {sbq['OOS_Sharpe']:.4f} / "
          f"{sbq['OOS_MaxDD']:.2%};  RULES v2 OOS "
          f"{[r for r in benchrows if r['panel']==panel and r['series']=='RULESv2'][0]['OOS_CAGR']:.2%}")
        s = pk[pk.panel == panel]
        P(f"     picks (spacing x seeds x chooser = {len(s)}): 4b full {int(s.pass4b.sum())}/"
          f"{len(s)}, 4b OOS {int(s.pass4b_oos.sum())}/{len(s)}, 4a {int(s.pass4a.sum())}/{len(s)}")
        for _, r in s[s.pass4b_oos].drop_duplicates("pick").iterrows():
            P(f"       4b-OOS PASS  pick n={r['pick']}  OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f}"
              f" / {r.OOS_MaxDD:.2%}  full {r.CAGR:.2%} / {r.Sharpe:.4f} / {r.MaxDD:.2%} halves "
              f"{r.H1:.3f}/{r.H2:.3f}  4b-full {r.pass4b}")
        g = gd[gd.panel == panel]
        P(f"     whole ladder (9 rungs): 4b full {int(g.pass4b.sum())}/9, 4b OOS "
          f"{int(g.pass4b_oos.sum())}/9, 4a {int(g.pass4a.sum())}/9")

    P("")
    P("# ---- HYPOTHESES ----")
    for h in hyp:
        P(f"   {'PASS' if h['passed'] else 'FAIL'}  {h['hypothesis']}  [declared {h['declared']};"
          f" observed {h['observed']}]")

    dump(ed, "edge")
    dump(bt, "argmax")
    dump(pr, "pairs")
    dump(pd.DataFrame(floorrows), "floor")
    dump(pk, "picks")
    dump(gd, "grid")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
