#!/usr/bin/env python3
"""Idea 1179 (lane B, 2026-09-17)
   what-does-a-ONE-SIDED-agreement-between-a-FREE-bar-and-a-PAID-one-buy-the-record

THE QUEUE'S PREMISE, QUOTED.  Idea 1170 found that a zero-cost one-seed t-rule (R_TSTAT)
agrees with the 5-seed incumbent (R_1164) on 0.879 of 132 cells, and that EVERY one of the
16 disagreements is ONE-SIDED: +16 admitted, -0 refused.  The free rule never refuses a
cell the paid rule admits, so it is a sound LOWER BOUND on refusals.  The queue asks two
things of that observation: (a) CENSUS the record's other paid-vs-free bar pairs for
whether any is one-sided IN THE SAME DIRECTION, and (b) PRICE publishing the free bar as a
SCREEN that only the FLAGGED cells pay to resolve.

WHAT THIS RUN CHANGES ABOUT THE QUESTION, STATED UP FRONT.

  1170's one-sidedness is reported as if it were a property of the MACHINERY (cheap
  statistic vs expensive statistic).  It is not obviously that.  R_TSTAT's bar is
  2 x median_se and R_1164's is max(3 x cross-seed spread, 0.25pp): the two differ by an
  arbitrary CONSTANT as well as by machinery, and the run's own numbers say the constant is
  doing the work -- median R_TSTAT bar 0.564 pp against a median R_1164 bar of 2.042 pp,
  i.e. the free bar sits 3.6x LOWER.  A looser bar admits a superset BY CONSTRUCTION, and a
  superset is one-sided BY CONSTRUCTION.  So this run measures one-sidedness twice for every
  pair: AS PUBLISHED, and again at a LEVEL-MATCHED free constant chosen (not searched) so
  the two bars admit the same NUMBER of cells.  If one-sidedness survives level-matching it
  is a machinery fact and the screen is sound; if it does not, 1170's headline is an
  artefact of two constants and the screen buys nothing structural.  This is H_CONSTANT and
  it is pre-registered below.

  The second thing the queue's phrasing hides: a SCREEN is only worth pricing if its two
  costs are on the same axis.  They are not.  The free bar's cost is ZERO DRAWS; the paid
  bar's is the full null.  So the screen's price is the SHARE OF CELLS FLAGGED and its
  product is the SHARE OF VERDICTS THAT STILL MATCH PAYING EVERYWHERE.  Both are published
  at every rung of the threshold ladder, and the frontier (smallest k with zero error, and
  what it costs) is the deliverable.

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:

  `BAR_PAIR`   {B_MEANP, B_SHARPE, B_PERMT, B_TSTAT}
  `SCREEN_K`   {0.00, 0.25, 0.50, 1.00, 2.00, inf}

  = 24 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`, whatever the headline says.

  BAR PAIRS.  Each is a PAID (resampling) bar and a FREE (closed-form) bar deciding the
  SAME admit/refuse verdict on the SAME cell.  The first three are the three the queue
  names; the fourth is 1170's own pair, replayed bit for bit off its committed cells.csv
  so this run's frame is anchored to the record rather than to a re-derivation.

    B_MEANP   "bootstrap p vs normal p".  Object: is the book's mean daily return
              distinguishable from zero?
              PAID  moving-block bootstrap (L=63, 1000 draws), recentred two-sided p:
                    p = share(|mean(r*) - mean(r)| >= |mean(r)|).  ADMIT at p <= 0.05.
              FREE  t = mean / (sd / sqrt(T)), normal two-sided p.  ADMIT at p <= 0.05.
              z_free = |t|,  z* = 1.96.
    B_SHARPE  "block band vs analytic SE".  Object: is the book's Sharpe distinguishable
              from zero?
              PAID  moving-block bootstrap band [q025, q975] on the Sharpe, 1000 draws.
                    ADMIT when the band excludes 0.
              FREE  Lo (2002) iid analytic SE, SE(S_pp) = sqrt((1 + S_pp^2 / 2) / T),
                    annualised by sqrt(252).  ADMIT at |S| >= 1.96 SE.
              z_free = |S| / SE_Lo,  z* = 1.96.
    B_PERMT   "permutation vs t".  Object: is the book's daily return distinguishable from
              SPY's on the same panel?  d = r_book - r_SPY, paired.
              PAID  moving-block SIGN-FLIP permutation of d (L=63, 1000 draws),
                    p = share(|mean(d*)| >= |mean(d)|).  ADMIT at p <= 0.05.
              FREE  paired t on d.  ADMIT at p <= 0.05.
              z_free = |t_d|,  z* = 1.96.
              UNDEFINED at the C_SPY anchor cells (d == 0); those 3 cells are excluded from
              every B_PERMT count and the exclusion is published, never silently dropped.
    B_TSTAT   1170's OWN pair, the record's committed one.
              PAID  R_1164: |denom| >= max(3 x larger cross-seed spread, 0.25 pp), 5 seeds
                    x 2 nulls x 1000 draws per cell.
              FREE  R_TSTAT: |denom| >= 2 x the one-seed order-statistic median SE.
              z_free = |denom| / se_iid,  z* = 2.0.
              Read straight off 1170's committed `.cells.csv`; gates G6/G7 require this
              run's recomputation to reproduce its committed verdicts EXACTLY (0 cells of
              132 differing) before a single number below is read.

  SCREEN.  Given the free statistic z and its critical value z*, the screen FLAGS a cell
  when |z - z*| <= k (k in free-SE units, which is the natural scale because every z above
  is already standardised) and PAYS the full null only there.  The screened verdict is the
  PAID verdict at flagged cells and the FREE verdict everywhere else.  k = inf is the
  status quo (pay everywhere, cost 1.000, error 0.000 by construction); k = 0 is the free
  bar alone (cost 0.000, error = the raw disagreement rate).  Gate G9 checks both
  identities; gate G10 checks that cost is non-decreasing and error non-increasing in k.

  NOT DIALS.  PANEL (all three built), the 132-CELL POPULATION (3 x [24 books + 5 anchor
  controls + 15 gross rungs], 1170's own, so that every pair is measured on the cells the
  record already published), L = 63, 1000 draws, the seeds, and the census scan, which is
  exhaustive over research/backtests/*.csv and the record's committed prose.

  A POPULATION CAVEAT THIS RUN PUBLISHES RATHER THAN BURIES.  15 of each panel's 44 cells
  are GROSS rungs of one anchor book.  Sharpe and the t on the mean are very nearly
  scale-invariant, so those 45 cells are near-duplicates for B_SHARPE and B_MEANP and they
  inflate any agreement rate computed over all 132.  Every headline below is therefore
  reported TWICE -- on all 132 and on the 87 non-GROSS cells -- and the 87 is the one that
  should be quoted.

FROZEN at 1162/1164/1170's construction: CAND20 legs, max_vol 0.60, gross 0.75, 10 bps
(PROTOCOL rule 2), LAG 1, warm-up 260, IS end 2016-12-31, block L = 63, 1000 draws, crc32
seeds, DD cap 0.60, CAGR floor 0.70.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
CURRENT constituents of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  Every LEVEL here -- CAGR, Sharpe, |MaxDD| -- is optimistic.
It largely CANCELS out of the headline, which is an AGREEMENT COUNT between two bars read
on the same cell, and it does NOT cancel out of the 4a / 4b legs in ARM F.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

import csv
import math
import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "what-does-a-ONE-SIDED-agreement-between-a-FREE-bar-and-a-PAID-one-buy-the-record"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136", "SMALL"]
POP_N = [5, 10, 20, 40]
POP_H = [63, 126, 252]
POP_F = ["W", "M"]
ANCHOR_CONTROLS = ["C_BOOK", "C_GATEOFF", "C_NOREBAL", "C_SHUFFLE", "C_SPY"]
GROSS_LADDER = [round(0.30 + 0.05 * i, 3) for i in range(15)]

BAR_PAIRS = ["B_MEANP", "B_SHARPE", "B_PERMT", "B_TSTAT"]           # dial 1
SCREEN_K = [0.00, 0.25, 0.50, 1.00, 2.00, float("inf")]             # dial 2

L_BLOCK, BDRAWS = 63, 1000
ALPHA = 0.05
ZCRIT = 1.959963984540054          # two-sided 5% normal critical value
TSTAT_K = 2.0                      # 1170's free constant, quoted not chosen
SEED_BASE = 11791179
SEED_1162 = 11621162
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}
REGIMES = ["G_FREE", "G_PAID", "G_SCREEN"]
SCREEN_K_ARMF = 1.00               # the ARM F screen rung, frozen at the ladder's middle

PRIOR1170 = BT / ("2026-09-17_is-every-published-PHI-or-BLOCK-BAND-in-the-record-"
                  "ESTIMABLE-at-all_B.cells.csv")
PRIOR1170_AGREE = BT / ("2026-09-17_is-every-published-PHI-or-BLOCK-BAND-in-the-record-"
                        "ESTIMABLE-at-all_B.agreement.csv")
COMMITTED_1170_AGREE_PHI = 0.8787878787878788
COMMITTED_1170_EXTRA, COMMITTED_1170_LOST = 16, 0

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts, base=SEED_BASE):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<68s} {value:.3e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, bar, measured, supported):
    HYP.append(dict(hypothesis=name, bar=bar, measured=measured, supported=bool(supported)))
    P(f"  {name:<12s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


def norm_p(z):
    """Two-sided normal p-value.  math.erfc, no scipy."""
    return float(math.erfc(abs(float(z)) / math.sqrt(2.0)))


# ================================================================= the record's runner
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


def windows_of(idx):
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


# ====================================================== resample machinery (the PAID side)
def block_index(rng, T, ndraws, L=L_BLOCK):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
    return idx.reshape(ndraws, nb * L)[:, :T]


def iid_index(rng, T, ndraws):
    return rng.integers(0, T, size=(ndraws, T))


def block_signs(rng, T, ndraws, L=L_BLOCK):
    """One +/-1 per block of L consecutive bars, tiled to length T.  The permutation arm's
    resample: preserves the within-block dependence of d and imposes only symmetry."""
    nb = int(np.ceil(T / L))
    s = rng.choice(np.array([-1.0, 1.0]), size=(ndraws, nb))
    return np.repeat(s, L, axis=1)[:, :T]


def boot_mean_sharpe(r, idx, chunk=200):
    """mean and annualised Sharpe of ONE series under every resample row of idx."""
    r = np.asarray(r, float)
    n = idx.shape[0]
    mu = np.empty(n)
    sh = np.empty(n)
    for a in range(0, n, chunk):
        x = r[idx[a:a + chunk]]
        m = x.mean(axis=1)
        sd = x.std(axis=1, ddof=1)
        mu[a:a + chunk] = m
        sh[a:a + chunk] = np.where(sd > 0, m * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return mu, sh


def boot_maxdd(r, idx, chunk=100):
    """|MaxDD| (positive, in %) of ONE series under every resample row of idx."""
    LG = np.log1p(np.asarray(r, float))
    out = np.empty(idx.shape[0])
    for a in range(0, idx.shape[0], chunk):
        ix = idx[a:a + chunk]
        cum = np.cumsum(LG[ix], axis=1)
        run = np.maximum.accumulate(cum, axis=1)
        out[a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


def obs_maxdd_pct(r):
    cum = np.cumsum(np.log1p(np.asarray(r, float)))
    run = np.maximum.accumulate(cum)
    return -float(np.expm1(cum - run).min()) * 100.0


def median_se(x):
    """SE of a sample median read off the draws themselves, DISTRIBUTION-FREE (1170's
    corrected form): half the spacing between the order statistics sqrt(n)/2 ranks either
    side of the middle.  Needs ONE seed -- this is what makes the free bar free."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    half = 0.5 * np.sqrt(n)
    lo = int(np.clip(np.floor(n / 2.0 - half), 0, n - 1))
    hi = int(np.clip(np.ceil(n / 2.0 + half), 0, n - 1))
    return float((x[hi] - x[lo]) / 2.0)


def lo_se_sharpe(r):
    """Lo (2002) iid analytic SE of an annualised Sharpe.  The FREE bar for B_SHARPE:
    SE(S_pp) = sqrt((1 + S_pp^2 / 2) / T), annualised by sqrt(252)."""
    r = np.asarray(r, float)
    T = len(r)
    sd = r.std(ddof=1)
    if sd <= 0:
        return np.nan, np.nan
    s_pp = r.mean() / sd
    return float(s_pp * np.sqrt(252.0)), float(np.sqrt((1.0 + 0.5 * s_pp ** 2) / T) *
                                               np.sqrt(252.0))


# ================================================== the FOUR PAIRS, on one return series
def pair_bars(pair, r, rspy, seed_parts):
    """Return dict(z_free, z_star, free_admit, paid_admit, defined, free_stat, paid_stat).
    B_TSTAT is NOT computed here -- it is read off 1170's committed cells (and recomputed
    in the replay gate) because it IS the record's committed pair."""
    r = np.asarray(r, float)
    T = len(r)
    rng = np.random.default_rng(seed_of(pair, *seed_parts))
    if pair == "B_MEANP":
        m = r.mean()
        sd = r.std(ddof=1)
        t = m / (sd / np.sqrt(T)) if sd > 0 else np.nan
        pf = norm_p(t) if np.isfinite(t) else np.nan
        mu, _ = boot_mean_sharpe(r, block_index(rng, T, BDRAWS))
        pp = float(np.mean(np.abs(mu - m) >= abs(m)))
        return dict(defined=bool(np.isfinite(t)), z_free=abs(t), z_star=ZCRIT,
                    free_stat=pf, paid_stat=pp,
                    free_admit=bool(pf <= ALPHA), paid_admit=bool(pp <= ALPHA))
    if pair == "B_SHARPE":
        s_ann, se = lo_se_sharpe(r)
        _, sh = boot_mean_sharpe(r, block_index(rng, T, BDRAWS))
        lo, hi = np.nanpercentile(sh, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
        z = abs(s_ann) / se if (se and np.isfinite(se) and se > 0) else np.nan
        return dict(defined=bool(np.isfinite(z)), z_free=z, z_star=ZCRIT,
                    free_stat=float(s_ann), paid_stat=float(lo),
                    free_admit=bool(z >= ZCRIT), paid_admit=bool(lo > 0.0 or hi < 0.0))
    if pair == "B_PERMT":
        d = r - np.asarray(rspy, float)
        sd = d.std(ddof=1)
        if not np.isfinite(sd) or sd <= 0:
            return dict(defined=False, z_free=np.nan, z_star=ZCRIT, free_stat=np.nan,
                        paid_stat=np.nan, free_admit=False, paid_admit=False)
        m = d.mean()
        t = m / (sd / np.sqrt(T))
        pf = norm_p(t)
        sg = block_signs(rng, T, BDRAWS)
        pp = float(np.mean(np.abs((sg * d[None, :]).mean(axis=1)) >= abs(m)))
        return dict(defined=True, z_free=abs(t), z_star=ZCRIT, free_stat=pf, paid_stat=pp,
                    free_admit=bool(pf <= ALPHA), paid_admit=bool(pp <= ALPHA))
    raise ValueError(pair)


# ============================================================ agreement / screen scoring
def agreement(free, paid, defined):
    """(agree, n_disagree, n_extra = free admits & paid refuses, n_lost = the reverse)."""
    f = np.asarray(free, bool)[np.asarray(defined, bool)]
    p = np.asarray(paid, bool)[np.asarray(defined, bool)]
    n = len(f)
    dis = int((f != p).sum())
    return (1.0 - dis / n if n else np.nan, dis, int((f & ~p).sum()), int((~f & p).sum()), n)


def one_sided(extra, lost):
    if extra + lost == 0:
        return "IDENTICAL", 0
    if lost == 0:
        return "ONE-SIDED +", extra
    if extra == 0:
        return "ONE-SIDED -", lost
    return "TWO-SIDED", min(extra, lost)


def matched_threshold(z, paid_admit, defined):
    """The free critical value that admits EXACTLY as many cells as the paid bar does.
    DETERMINED by the matching condition, not searched: take the n_paid-th largest z."""
    z = np.asarray(z, float)[np.asarray(defined, bool)]
    p = np.asarray(paid_admit, bool)[np.asarray(defined, bool)]
    k = int(p.sum())
    zs = np.sort(z[np.isfinite(z)])[::-1]
    if k <= 0:
        return float(np.inf)
    if k >= len(zs):
        return float(-np.inf)
    return float((zs[k - 1] + zs[k]) / 2.0)


def screen_score(z, zstar, free, paid, defined, k):
    """cost = share of DEFINED cells that pay; error = share whose screened verdict
    differs from paying everywhere; the residual error's two directions."""
    m = np.asarray(defined, bool)
    z = np.asarray(z, float)[m]
    f = np.asarray(free, bool)[m]
    p = np.asarray(paid, bool)[m]
    zs = np.asarray(zstar, float)[m]
    n = len(f)
    if n == 0:
        return dict(n=0, cost=np.nan, error=np.nan, n_err=0, err_extra=0, err_lost=0)
    flag = np.abs(z - zs) <= k if np.isfinite(k) else np.ones(n, bool)
    flag = flag & np.isfinite(z) if np.isfinite(k) else flag
    if not np.isfinite(k):
        flag = np.ones(n, bool)
    v = np.where(flag, p, f)
    err = v != p
    return dict(n=n, cost=float(flag.mean()), error=float(err.mean()), n_err=int(err.sum()),
                err_extra=int((v & ~p).sum()), err_lost=int((~v & p).sum()))


# ================================================================ ARM A — THE CENSUS
PAID_TOK = re.compile(r"(p_boot|boot_p|p_perm|perm_p|bootstrap_p|p_block|n_draws|ndraws|"
                      r"draws|null_median|seed_spread|q05|q95|q025|q975|band_lo|band_hi|"
                      r"boot_lo|boot_hi|p_bootstrap|null_p|p_null)", re.I)
FREE_TOK = re.compile(r"(t_?stat|tstat|^t$|_t$|z_?stat|zstat|p_norm|norm_p|p_t|analytic|"
                      r"^se$|_se$|se_|_sd$|^sd$|stderr|std_err)", re.I)
PAIDCTX = re.compile(r"(boot|block|perm|resample|null|draw)", re.I)

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
SENT_PAID = re.compile(r"(bootstrap|block bootstrap|permutation|resampl|P_boot|p_boot|"
                       r"block band|null median|1,000 draws|1000 draws)", re.I)
SENT_FREE = re.compile(r"(t-stat|t stat|tstat|analytic SE|analytic se|normal p|z-score|"
                       r"standard error|closed[- ]form|mean/SE|mean / SE)", re.I)
SENT_NUM = re.compile(r"\d")


def census_scan():
    """Exhaustive scan of every committed CSV in research/backtests.  A file carries a BAR
    PAIR when it publishes at least one PAID-bar column and at least one FREE-bar column,
    in a resampling context.  That is the population the record could audit for
    one-sidedness WITHOUT running anything."""
    rows = []
    files = sorted(BT.glob("*.csv"))
    for f in files:
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                hdr = next(rd)
                n = sum(1 for _ in rd)
        except Exception:
            continue
        cols = [c.strip() for c in hdr]
        paid = [c for c in cols if PAID_TOK.search(c)]
        free = [c for c in cols if FREE_TOK.search(c)]
        ctx = bool(PAIDCTX.search(f.name)) or any(PAIDCTX.search(c) for c in cols)
        if not paid and not free:
            continue
        cls = ("BOTH" if (paid and free) else ("PAID_ONLY" if paid else "FREE_ONLY"))
        rows.append(dict(file=f.name, n_rows=n, n_cols=len(cols), klass=cls,
                         resample_ctx=bool(ctx),
                         paid_cols="|".join(paid[:6]), free_cols="|".join(free[:6]),
                         n_paid_cols=len(paid), n_free_cols=len(free)))
    return pd.DataFrame(rows), len(files)


def prose_scan():
    """The reader-facing layer: committed sentences in *.result.md / *.memo.md / the
    CHANGELOG that quote a PAID bar, and how many of those also quote its FREE
    counterpart."""
    rows = []
    srcs = sorted(BT.glob("*.result.md")) + sorted(BT.glob("*.memo.md"))
    srcs += [ROOT / "research" / "CHANGELOG.md", ROOT / "research" / "LEADERBOARD.md"]
    nsent = 0
    for f in srcs:
        if not f.exists():
            continue
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for s in SENT_SPLIT.split(txt.replace("\n", " ")):
            s = s.strip()
            if not s:
                continue
            nsent += 1
            hp, hf = bool(SENT_PAID.search(s)), bool(SENT_FREE.search(s))
            if hp or hf:
                rows.append(dict(file=f.name, has_paid=hp, has_free=hf,
                                 has_number=bool(SENT_NUM.search(s)),
                                 sentence=s[:300]))
    return pd.DataFrame(rows), nsent, len([f for f in srcs if f.exists()])


# ==========================================================================  MAIN
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1179 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")
    P("## PRE-REGISTERED HYPOTHESES (bars fixed before any number below is read)")
    P("  H_ONESIDED  at least ONE of the three FRESH bar pairs is ONE-SIDED in the SAME")
    P("              direction as 1170's (free admits a superset; n_lost == 0 with")
    P("              n_extra > 0).")
    P("  H_UNIVERSAL one-sidedness is a GENERAL property of paid-vs-free: ALL FOUR pairs")
    P("              are one-sided, in any direction.")
    P("  H_CONSTANT  one-sidedness is a MACHINERY fact, not a CONSTANT one: it survives")
    P("              level-matching the free bar to admit the same COUNT as the paid bar,")
    P("              at >= half the pairs that are one-sided as published.")
    P("  H_SCREEN    some k < inf reaches ZERO screened error at < 0.50 of the cost of")
    P("              paying everywhere, at >= half the pairs.")
    P("  H_AUDITABLE the record can audit this retrospectively: >= 0.10 of committed")
    P("              bar-bearing CSVs publish BOTH a paid and a free bar column.")
    P("  H_CAPITAL   the screen has CAPITAL content: swapping an IS chooser's admitted")
    P("              pool between G_FREE, G_PAID and G_SCREEN moves OOS Sharpe by >= 0.05")
    P("              at >= half the (panel, chooser, pair) cells.")
    P("")

    # --------------------------------------------------------------------- panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    smallpx = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in smallpx.columns if c == "SPY" or c not in bad]
    raw["SMALL"] = smallpx[keep].dropna(how="all").ffill()
    ndrop, nmeta = len(bad), len(meta)
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm, ins=ins, oos=oos,
                             sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY.")
    P("")

    # ------------------------------------------------------- book constructors
    _WCACHE: dict = {}

    def weights_pop(panel, N, H, freq):
        key = (panel, "POP", N, H, freq)
        if key not in _WCACHE:
            d = panels[panel]
            mk = rebalance_mask(d["idx"], freq).values
            _WCACHE[key] = (build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N, H,
                                  d["T"], d["K"], 1.0), mk)
        return _WCACHE[key]

    def weights_anchor(panel, control):
        key = (panel, "ANC", control)
        if key in _WCACHE:
            return _WCACHE[key]
        d = panels[panel]
        T, K = d["T"], d["K"]
        if control == "C_SPY":
            mk = rebalance_mask(d["idx"], FREQ0).values
            W = np.zeros((T, K))
            W[WARMUP:, d["spy_i"]] = 1.0
        elif control == "C_NOREBAL":
            mk_full = rebalance_mask(d["idx"], FREQ0).values
            first = int(np.flatnonzero(mk_full & (np.arange(T) >= WARMUP))[0])
            mk = np.zeros(T, dtype=bool)
            mk[first] = True
            W = build(-d["sc"], d["elig"], d["priced"], np.array([first]), N0, HOLD0, T, K, 1.0)
        else:
            mk = rebalance_mask(d["idx"], FREQ0).values
            elig = d["priced"] if control == "C_GATEOFF" else d["elig"]
            if control == "C_GATEOFF" and panel == "SMALL":
                elig = elig.copy()
                elig[:, d["spy_i"]] = False
            W = build(-d["sc"], elig, d["priced"], np.flatnonzero(mk), N0, HOLD0, T, K, 1.0)
        _WCACHE[key] = (W, mk)
        return _WCACHE[key]

    def run_weights(panel, W1, mk, gross):
        d = panels[panel]
        W = W1 * gross
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return (g - tn * COST / 1e4)[d["warm"]]

    def pop_returns(panel, N, H, freq, gross=GROSS0):
        W1, mk = weights_pop(panel, N, H, freq)
        return run_weights(panel, W1, mk, gross)

    def anchor_returns(panel, control, gross=GROSS0):
        base = "C_BOOK" if control == "C_SHUFFLE" else control
        W1, mk = weights_anchor(panel, base)
        r = run_weights(panel, W1, mk, gross)
        if control == "C_SHUFFLE":
            rw = r.copy()
            np.random.default_rng(seed_of(panel, "C_SHUFFLE", gross, "",
                                          base=SEED_1162)).shuffle(rw)
            return rw
        return r

    def spy_warm(panel):
        d = panels[panel]
        return d["px"]["SPY"].pct_change().fillna(0.0).values[d["warm"]]

    # ------------------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_weights("U56", W / GROSS0, mk, GROSS0)
    v = float(np.abs(eng[d["warm"]] - rfast).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    # live RULES v2 and SPY anchors, against the record's committed values
    bl = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"]
    blm = fmet(bl.values[d["warm"]])
    v = abs(blm[0] - 0.0860) + abs(blm[2] + 0.1205)
    gate("G2", "live RULES v2 == committed 8.60% CAGR / -12.05% MaxDD", v, v < 5e-4)
    spym = fmet(spy_warm("U56"))
    v = abs(spym[0] - 0.1506) + abs(spym[1] - 0.8814) + abs(spym[2] + 0.3372)
    gate("G3", "SPY (U56 tape) == committed 15.06% / 0.8814 / -33.72%", v, v < 2e-3)

    z = np.random.default_rng(3).normal(0, 1, 20000)
    v = abs(median_se(z) - 1.2533 / np.sqrt(len(z))) / (1.2533 / np.sqrt(len(z)))
    gate("G4", "median_se (order statistics) == gaussian 1.2533*sd/sqrt(n)", v, v < 0.05)

    # the FREE bars must be CALIBRATED on data where the PAID bar's extra machinery is
    # known to be unnecessary: iid gaussian returns.  If they disagree THERE, any
    # disagreement on the books is this run's bug, not a finding.
    rr = np.random.default_rng(11).normal(0.0004, 0.01, 4000)
    s_ann, se_lo = lo_se_sharpe(rr)
    _, shb = boot_mean_sharpe(rr, iid_index(np.random.default_rng(12), len(rr), 2000))
    v = abs(np.nanstd(shb, ddof=1) - se_lo) / se_lo
    gate("G5", "Lo analytic SE == iid-bootstrap SD of the Sharpe on iid gaussian data",
         v, v < 0.10)

    dd = np.random.default_rng(13).normal(0.0, 0.01, 4000)
    tt = dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd)))
    sg = block_signs(np.random.default_rng(14), len(dd), 4000, L=1)
    pp = float(np.mean(np.abs((sg * dd[None, :]).mean(axis=1)) >= abs(dd.mean())))
    v = abs(pp - norm_p(tt))
    gate("G6", "sign-flip permutation p == normal p on iid symmetric data (L=1)", v,
         v < 0.05)

    ix_b1 = block_index(np.random.default_rng(777), 500, 50, L=1)
    ix_i1 = iid_index(np.random.default_rng(777), 500, 50)
    v = float(np.abs(ix_b1 - ix_i1).max())
    gate("G7", "block_index at L=1 IS iid_index, bit for bit (same seed, same draw)", v,
         v == 0)

    # ------------------------- G8: replay 1170's committed pair off its own cells.csv
    P("")
    P("## CROSS-RUN REPLAY — 1170's committed B_TSTAT pair, off its own .cells.csv")
    if not PRIOR1170.exists():
        P("  FATAL: 1170's committed cells.csv is missing; nothing below is comparable.")
        sys.exit(1)
    pc = pd.read_csv(PRIOR1170)
    bar_paid = np.maximum(3.0 * np.maximum(pc.iid_seed_spread.values,
                                           pc.block_seed_spread.values), 0.25)
    paid_re = np.abs(pc.denom.values) >= bar_paid
    free_re = np.abs(pc.denom.values) >= TSTAT_K * pc.se_iid.values
    v = float((paid_re != pc.phi_est_R_1164.values.astype(bool)).sum())
    gate("G8", "recomputed R_1164 verdict == 1170's committed phi_est_R_1164 (132 cells)",
         v, v == 0)
    v = float((free_re != pc.phi_est_R_TSTAT.values.astype(bool)).sum())
    gate("G9", "recomputed R_TSTAT verdict == 1170's committed phi_est_R_TSTAT", v, v == 0)
    ag = agreement(free_re, paid_re, np.ones(len(pc), bool))
    v = abs(ag[0] - COMMITTED_1170_AGREE_PHI) + abs(ag[2] - COMMITTED_1170_EXTRA) + \
        abs(ag[3] - COMMITTED_1170_LOST)
    gate("G10", "replayed agreement == 1170's committed 0.8788 / +16 / -0", v, v < 1e-12)
    P(f"  1170's pair, replayed: agree {ag[0]:.4f}, +{ag[2]} admitted, -{ag[3]} refused, "
      f"n = {ag[4]}")
    P("")

    # ===================================================================== ARM A: census
    P("## ARM A — CENSUS of the record's committed BAR PAIRS")
    cen, nfiles = census_scan()
    dump(cen, "census")
    tot = len(cen)
    by = cen.groupby("klass").agg(files=("file", "size"), rows=("n_rows", "sum"))
    P(f"  {nfiles:,} committed CSVs scanned; {tot:,} carry at least one bar column.")
    for k in ["BOTH", "PAID_ONLY", "FREE_ONLY"]:
        if k in by.index:
            P(f"    {k:<10s} {int(by.loc[k, 'files']):5d} files  "
              f"{int(by.loc[k, 'rows']):10,d} rows   share of bar-bearing files "
              f"{by.loc[k, 'files'] / tot:.4f}")
    share_both = float((cen.klass == "BOTH").mean()) if tot else 0.0
    ctx = cen[cen.resample_ctx]
    share_both_ctx = float((ctx.klass == "BOTH").mean()) if len(ctx) else np.nan
    P(f"  In a RESAMPLING context ({len(ctx):,} files): BOTH = {share_both_ctx:.4f}")
    pr, nsent, nsrc = prose_scan()
    dump(pr, "sentences")
    npaid = int(pr.has_paid.sum())
    nboth_s = int((pr.has_paid & pr.has_free).sum())
    P(f"  PROSE: {nsent:,} committed sentences in {nsrc} files; {npaid:,} quote a PAID "
      f"bar, {nboth_s:,} of those also quote a FREE one "
      f"({(nboth_s / npaid if npaid else float('nan')):.4f}).")
    cen_sum = pd.DataFrame([dict(layer="csv", n_files=nfiles, n_bar_files=tot,
                                 share_both=share_both, share_both_resample=share_both_ctx),
                            dict(layer="prose", n_files=nsrc, n_bar_files=npaid,
                                 share_both=(nboth_s / npaid if npaid else np.nan),
                                 share_both_resample=np.nan)])
    dump(cen_sum, "census_summary")
    hyp("H_AUDITABLE", ">= 0.10 of bar-bearing CSVs publish BOTH",
        f"{share_both:.4f} of {tot} CSVs ({share_both_ctx:.4f} in resample context); "
        f"prose {nboth_s}/{npaid}", share_both >= 0.10)
    P("")

    # ============================================= ARM B: build the 132-cell population
    P("## ARM B — the 132-cell population (1170's own), four bar pairs on each")
    cells = []
    for panel in PANELS:
        dpan = panels[panel]
        rspy = spy_warm(panel)
        specs = []
        for N in POP_N:
            for H in POP_H:
                for F in POP_F:
                    specs.append(("POP", f"N{N}/H{H}/{F}", lambda N=N, H=H, F=F:
                                  pop_returns(panel, N, H, F)))
        for c in ANCHOR_CONTROLS:
            specs.append(("ANCHOR", c, lambda c=c: anchor_returns(panel, c)))
        for g in GROSS_LADDER:
            specs.append(("GROSS", f"anchor/g{g:.2f}",
                          lambda g=g: anchor_returns(panel, "C_BOOK", gross=g)))
        for arm, book, fn in specs:
            r = fn()
            row = dict(cell=f"{panel}/{book}", panel=panel, arm=arm, book=book,
                       n_bars=len(r))
            c_, s_, dd_ = fmet(r)
            row.update(CAGR=c_, Sharpe=s_, MaxDD=dd_, obs_maxdd=obs_maxdd_pct(r))
            for pair in ["B_MEANP", "B_SHARPE", "B_PERMT"]:
                b = pair_bars(pair, r, rspy, (panel, book))
                row[f"{pair}_defined"] = b["defined"]
                row[f"{pair}_z"] = b["z_free"]
                row[f"{pair}_zstar"] = b["z_star"]
                row[f"{pair}_free"] = b["free_admit"]
                row[f"{pair}_paid"] = b["paid_admit"]
                row[f"{pair}_free_stat"] = b["free_stat"]
                row[f"{pair}_paid_stat"] = b["paid_stat"]
            cells.append(row)
        P(f"  {panel:<6s} {len([c for c in cells if c['panel'] == panel]):3d} cells built "
          f"({time.time() - t0:.0f}s)")
    C = pd.DataFrame(cells)

    # B_TSTAT: 1170's committed cells, joined on the same cell key
    pc2 = pc.copy()
    pc2["cell"] = pc2.panel + "/" + pc2.book
    pc2["B_TSTAT_z"] = np.abs(pc2.denom.values) / pc2.se_iid.values
    pc2["B_TSTAT_zstar"] = TSTAT_K
    pc2["B_TSTAT_free"] = free_re
    pc2["B_TSTAT_paid"] = paid_re
    pc2["B_TSTAT_defined"] = np.isfinite(pc2["B_TSTAT_z"].values)
    pc2["B_TSTAT_free_stat"] = pc2.denom.values
    pc2["B_TSTAT_paid_stat"] = bar_paid
    keepc = ["cell"] + [c for c in pc2.columns if c.startswith("B_TSTAT_")]
    C = C.merge(pc2[keepc], on="cell", how="left")
    miss = int(C.B_TSTAT_paid.isna().sum())
    gate("G11", "every one of this run's 132 cells matches a committed 1170 cell",
         float(miss), miss == 0)
    dump(C, "cells")
    P("")

    # ======================================== ARM C: agreement and one-sidedness by pair
    P("## ARM C — AGREEMENT and ONE-SIDEDNESS, per bar pair")
    P("  (ALL = 132 cells; NOGROSS = the 87 POP+ANCHOR cells, the number to quote)")
    sub = {"ALL": C, "NOGROSS": C[C.arm != "GROSS"]}
    arows = []
    for pair in BAR_PAIRS:
        for scope, Cx in sub.items():
            dfn = Cx[f"{pair}_defined"].fillna(False).values.astype(bool)
            fr = Cx[f"{pair}_free"].fillna(False).values.astype(bool)
            pa = Cx[f"{pair}_paid"].fillna(False).values.astype(bool)
            zz = Cx[f"{pair}_z"].values
            ag_, dis, ex, lo_, n = agreement(fr, pa, dfn)
            verdict, minor = one_sided(ex, lo_)
            zm = matched_threshold(zz, pa, dfn)
            frm = np.where(np.isfinite(zz), zz >= zm, False)
            ag2, dis2, ex2, lo2, _ = agreement(frm, pa, dfn)
            v2, minor2 = one_sided(ex2, lo2)
            arows.append(dict(bar_pair=pair, scope=scope, n=n,
                              n_free_admit=int(fr[dfn].sum()),
                              n_paid_admit=int(pa[dfn].sum()),
                              agree=ag_, n_disagree=dis, n_extra=ex, n_lost=lo_,
                              verdict=verdict, minority=minor,
                              z_star_published=float(np.nanmedian(
                                  Cx[f"{pair}_zstar"].values)),
                              z_star_matched=zm, agree_matched=ag2,
                              n_disagree_matched=dis2, n_extra_matched=ex2,
                              n_lost_matched=lo2, verdict_matched=v2,
                              n_undefined=int((~dfn).sum())))
            if scope == "NOGROSS":
                P(f"  {pair:<9s} n={n:3d}  free admits {int(fr[dfn].sum()):3d}  paid "
                  f"{int(pa[dfn].sum()):3d}  agree {ag_:.4f}  +{ex:3d} / -{lo_:<3d} "
                  f"{verdict:<12s} | MATCHED z*={zm:6.3f} agree {ag2:.4f} "
                  f"+{ex2:3d} / -{lo2:<3d} {v2}")
    A = pd.DataFrame(arows)
    dump(A, "agreement")

    ng = A[A.scope == "NOGROSS"].set_index("bar_pair")
    fresh = [p for p in BAR_PAIRS if p != "B_TSTAT"]
    same_dir = [p for p in fresh if ng.loc[p, "verdict"] == "ONE-SIDED +"]
    hyp("H_ONESIDED", ">= 1 fresh pair ONE-SIDED + (free admits a superset)",
        f"{len(same_dir)} of 3 fresh pairs one-sided +: {same_dir or 'none'}; "
        f"verdicts " + ", ".join(f"{p}={ng.loc[p, 'verdict']}" for p in fresh),
        len(same_dir) >= 1)
    all_os = [p for p in BAR_PAIRS if ng.loc[p, "verdict"].startswith("ONE-SIDED")]
    hyp("H_UNIVERSAL", "ALL FOUR pairs one-sided in some direction",
        f"{len(all_os)} of 4 one-sided: " + ", ".join(
            f"{p}={ng.loc[p, 'verdict']}" for p in BAR_PAIRS), len(all_os) == 4)
    surv = [p for p in all_os if ng.loc[p, "verdict_matched"].startswith("ONE-SIDED")
            or ng.loc[p, "verdict_matched"] == "IDENTICAL"]
    hyp("H_CONSTANT", ">= half of the one-sided pairs stay one-sided at a LEVEL-MATCHED "
        "free constant",
        f"{len(surv)} of {len(all_os)} survive matching: " + ", ".join(
            f"{p}: {ng.loc[p, 'verdict']} -> {ng.loc[p, 'verdict_matched']}"
            for p in all_os),
        len(all_os) > 0 and len(surv) >= len(all_os) / 2.0)
    P("")

    # ========================================== ARM D: the SCREEN — the full 24-point grid
    P("## ARM D — the SCREEN: cost (share of cells that pay) vs error (verdicts that")
    P("          differ from paying everywhere).  ALL 24 DIAL POINTS PUBLISHED.")
    drows = []
    for pair in BAR_PAIRS:
        for scope, Cx in sub.items():
            dfn = Cx[f"{pair}_defined"].fillna(False).values.astype(bool)
            fr = Cx[f"{pair}_free"].fillna(False).values.astype(bool)
            pa = Cx[f"{pair}_paid"].fillna(False).values.astype(bool)
            zz = Cx[f"{pair}_z"].values
            zs = Cx[f"{pair}_zstar"].values
            for k in SCREEN_K:
                s = screen_score(zz, zs, fr, pa, dfn, k)
                drows.append(dict(bar_pair=pair, scope=scope, screen_k=k, **s))
    D = pd.DataFrame(drows)
    dump(D, "dialgrid")
    P("")
    P(f"  {'pair':<9s} {'k':>6s} {'n':>4s} {'cost':>7s} {'error':>7s} {'n_err':>6s} "
      f"{'+err':>5s} {'-err':>5s}    (NOGROSS, the 87 cells)")
    for pair in BAR_PAIRS:
        for k in SCREEN_K:
            r = D[(D.bar_pair == pair) & (D.scope == "NOGROSS") & (D.screen_k == k)].iloc[0]
            P(f"  {pair:<9s} {k:6.2f} {int(r.n):4d} {r.cost:7.4f} {r.error:7.4f} "
              f"{int(r.n_err):6d} {int(r.err_extra):5d} {int(r.err_lost):5d}")

    # identity + monotonicity gates on the screen
    bad = 0
    for pair in BAR_PAIRS:
        for scope in sub:
            g = D[(D.bar_pair == pair) & (D.scope == scope)].sort_values("screen_k")
            inf_ = g[np.isinf(g.screen_k)].iloc[0]
            z0 = g[g.screen_k == 0.0].iloc[0]
            raw = A[(A.bar_pair == pair) & (A.scope == scope)].iloc[0]
            bad += int(abs(inf_.cost - 1.0) > 1e-12) + int(inf_.error > 1e-12)
            bad += int(abs(z0.cost) > 1e-12)
            bad += int(z0.n_err != raw.n_disagree)
            bad += int((np.diff(g.cost.values) < -1e-12).any())
            bad += int((np.diff(g.error.values) > 1e-12).any())
    gate("G12", "screen identities (k=inf -> cost 1 err 0; k=0 -> cost 0 err = raw) and "
         "monotonicity", float(bad), bad == 0)

    # the frontier: smallest ladder k with zero error, and what it costs
    frows = []
    for pair in BAR_PAIRS:
        for scope in sub:
            g = D[(D.bar_pair == pair) & (D.scope == scope)].sort_values("screen_k")
            zero = g[g.n_err == 0]
            kz = float(zero.screen_k.iloc[0]) if len(zero) else np.nan
            cz = float(zero.cost.iloc[0]) if len(zero) else np.nan
            dfn = sub[scope][f"{pair}_defined"].fillna(False).values.astype(bool)
            fr = sub[scope][f"{pair}_free"].fillna(False).values.astype(bool)
            pa = sub[scope][f"{pair}_paid"].fillna(False).values.astype(bool)
            zz = sub[scope][f"{pair}_z"].values[dfn]
            zs = sub[scope][f"{pair}_zstar"].values[dfn]
            dis = fr[dfn] != pa[dfn]
            kexact = float(np.nanmax(np.abs(zz - zs)[dis])) if dis.any() else 0.0
            cost_exact = float(np.mean(np.abs(zz - zs) <= kexact))
            frows.append(dict(bar_pair=pair, scope=scope,
                              k_zero_on_ladder=kz, cost_at_k_zero=cz,
                              k_zero_exact=kexact, cost_at_k_zero_exact=cost_exact,
                              free_only_error=float(dis.mean())))
    F = pd.DataFrame(frows)
    dump(F, "frontier")
    P("")
    P("  FRONTIER (NOGROSS): the EXACT smallest k that reproduces paying everywhere, and")
    P("  what that screen costs:")
    for _, r in F[F.scope == "NOGROSS"].iterrows():
        P(f"    {r.bar_pair:<9s} free-only error {r.free_only_error:.4f}  ->  k* "
          f"{r.k_zero_exact:7.3f}  costs {r.cost_at_k_zero_exact:.4f} of cells  "
          f"(ladder k {r.k_zero_on_ladder} at cost {r.cost_at_k_zero})")
    fng = F[F.scope == "NOGROSS"].set_index("bar_pair")
    win = [p for p in BAR_PAIRS if np.isfinite(fng.loc[p, "cost_at_k_zero_exact"])
           and fng.loc[p, "cost_at_k_zero_exact"] < 0.50]
    hyp("H_SCREEN", "zero screened error at < 0.50 cost, at >= half the pairs",
        f"{len(win)} of 4 pairs reach zero error below half cost: " + ", ".join(
            f"{p}={fng.loc[p, 'cost_at_k_zero_exact']:.4f}" for p in BAR_PAIRS),
        len(win) >= 2)
    P("")

    # ================================ ARM E/F: rule 8 walk-forward and both KEEP paths
    P("## ARM F — RULE 8 WALK-FORWARD and BOTH KEEP PATHS")
    P("  72 population books, every one published; bars for the choosers are recomputed")
    P("  on the IS window (2009-2016) ONLY, and the picks are scored on the untouched")
    P("  2017-2026 window.")
    wf = []
    ispool: dict = {}
    for panel in PANELS:
        dpan = panels[panel]
        warm, ins, oos = dpan["warm"], dpan["ins"], dpan["oos"]
        isw = ins[warm]                       # IS mask inside the warm window
        spy_full = dpan["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(spy_full, warm, ins, oos)
        lbW = backtest(dpan["px"], rules_v2_weights(dpan["px"]), cost_bps=COST,
                       freq="W")["returns"].values
        lb = blocks_m(lbW, warm, ins, oos)
        rspy_w = spy_warm(panel)
        for N in POP_N:
            for H in POP_H:
                for Fq in POP_F:
                    book = f"N{N}/H{H}/{Fq}"
                    W1, mk = weights_pop(panel, N, H, Fq)
                    rfull = np.zeros(dpan["T"])
                    rfull[warm] = run_weights(panel, W1, mk, GROSS0)
                    m = blocks_m(rfull, warm, ins, oos)
                    b4 = legs_4b(m, sb)
                    b4o = legs_4b_oos(m, sb)
                    a4 = legs_4a(m, lb)
                    row = dict(panel=panel, book=book, **m,
                               pass_4b_full=all(b4.values()),
                               pass_4b_oos=all(b4o.values()),
                               pass_4a=all(a4.values()), **b4, **b4o, **a4)
                    # IS-window bars for each pair (walk-forward: IS data only)
                    rIS = rfull[warm][isw]
                    sIS = rspy_w[isw]
                    for pair in ["B_MEANP", "B_SHARPE", "B_PERMT"]:
                        b = pair_bars(pair, rIS, sIS, (panel, book, "IS"))
                        row[f"{pair}_free"] = b["free_admit"]
                        row[f"{pair}_paid"] = b["paid_admit"]
                        row[f"{pair}_z"] = b["z_free"]
                        row[f"{pair}_zstar"] = b["z_star"]
                        row[f"{pair}_defined"] = b["defined"]
                    # B_TSTAT on the IS window: the phi denominator and its two bars
                    obs = obs_maxdd_pct(rIS)
                    meds_i, meds_b = [], []
                    for sd_ in range(5):
                        rg = np.random.default_rng(seed_of(panel, book, "IS", "IID", sd_))
                        di = boot_maxdd(rIS, iid_index(rg, len(rIS), BDRAWS))
                        rg = np.random.default_rng(seed_of(panel, book, "IS", "BLK", sd_))
                        db = boot_maxdd(rIS, block_index(rg, len(rIS), BDRAWS))
                        meds_i.append(float(np.median(di)))
                        meds_b.append(float(np.median(db)))
                        if sd_ == 0:
                            se_i = median_se(di)
                    denom = obs - meds_i[0]
                    sp_i = max(meds_i) - min(meds_i)
                    sp_b = max(meds_b) - min(meds_b)
                    barp = max(3.0 * max(sp_i, sp_b), 0.25)
                    row["B_TSTAT_free"] = bool(abs(denom) >= TSTAT_K * se_i)
                    row["B_TSTAT_paid"] = bool(abs(denom) >= barp)
                    row["B_TSTAT_z"] = abs(denom) / se_i if se_i > 0 else np.nan
                    row["B_TSTAT_zstar"] = TSTAT_K
                    row["B_TSTAT_defined"] = bool(se_i > 0)
                    wf.append(row)
        ispool[panel] = dict(sb=sb, lb=lb)
        P(f"  {panel:<6s} 24 books scored, IS bars built ({time.time() - t0:.0f}s)")
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    P(f"  BASE RATES over {len(WF)} books: 4b full {int(WF.pass_4b_full.sum())}, "
      f"4b OOS {int(WF.pass_4b_oos.sum())}, 4a {int(WF.pass_4a.sum())}.")
    for panel in PANELS:
        w = WF[WF.panel == panel]
        P(f"    {panel:<6s} 4b full {int(w.pass_4b_full.sum()):2d}/24  "
          f"4b OOS {int(w.pass_4b_oos.sum()):2d}/24  4a {int(w.pass_4a.sum()):2d}/24")

    # choosers under the three bar regimes
    P("")
    P("  PICKS: 3 panels x 3 choosers x 4 bar pairs x 3 regimes = 108, all published.")
    prows = []
    for panel in PANELS:
        w = WF[WF.panel == panel].reset_index(drop=True)
        sb, lb = ispool[panel]["sb"], ispool[panel]["lb"]
        for pair in BAR_PAIRS:
            dfn = w[f"{pair}_defined"].values.astype(bool)
            fr = w[f"{pair}_free"].values.astype(bool) & dfn
            pa = w[f"{pair}_paid"].values.astype(bool) & dfn
            zz = w[f"{pair}_z"].values
            zs = w[f"{pair}_zstar"].values
            flag = np.abs(zz - zs) <= SCREEN_K_ARMF
            scr = np.where(flag & dfn, pa, fr)
            pools = {"G_FREE": fr, "G_PAID": pa, "G_SCREEN": scr}
            for cname, col in CHOOSERS.items():
                for reg in REGIMES:
                    pool = pools[reg]
                    sel = w[pool] if pool.any() else w
                    fallback = not pool.any()
                    j = (sel[col].idxmin() if cname == "C_ISDD" else sel[col].idxmax())
                    b = w.loc[j]
                    prows.append(dict(
                        panel=panel, bar_pair=pair, chooser=cname, regime=reg,
                        pool_size=int(pool.sum()), fallback_all=fallback,
                        pick=b.book, IS_Sharpe=b.IS_Sharpe, IS_CAGR=b.IS_CAGR,
                        IS_MaxDD=b.IS_MaxDD, OOS_Sharpe=b.OOS_Sharpe,
                        OOS_CAGR=b.OOS_CAGR, OOS_MaxDD=b.OOS_MaxDD,
                        CAGR=b.CAGR, Sharpe=b.Sharpe, MaxDD=b.MaxDD, H1=b.H1, H2=b.H2,
                        pass_4b_full=bool(b.pass_4b_full), pass_4b_oos=bool(b.pass_4b_oos),
                        pass_4a=bool(b.pass_4a),
                        spy_OOS_Sharpe=sb["OOS_Sharpe"], live_OOS_Sharpe=lb["OOS_Sharpe"]))
    PK = pd.DataFrame(prows)
    dump(PK, "picks")
    for pair in BAR_PAIRS:
        g = PK[PK.bar_pair == pair]
        n4b = int((g.pass_4b_full & g.pass_4b_oos).sum())
        P(f"    {pair:<9s} picks {len(g):3d}  4b full+OOS {n4b:2d}  4a "
          f"{int(g.pass_4a.sum()):2d}  mean OOS Sharpe {g.OOS_Sharpe.mean():.4f}")

    # H_CAPITAL: does the regime move the pick, and by how much OOS?
    piv = PK.pivot_table(index=["panel", "bar_pair", "chooser"], columns="regime",
                         values="OOS_Sharpe")
    pk2 = PK.pivot_table(index=["panel", "bar_pair", "chooser"], columns="regime",
                         values="pick", aggfunc="first")
    moved_fp = int((pk2["G_FREE"] != pk2["G_PAID"]).sum())
    moved_sp = int((pk2["G_SCREEN"] != pk2["G_PAID"]).sum())
    dd_fp = (piv["G_FREE"] - piv["G_PAID"]).abs()
    dd_sp = (piv["G_SCREEN"] - piv["G_PAID"]).abs()
    big = int((dd_fp >= 0.05).sum())
    P("")
    P(f"  The bar regime moves the pick at {moved_fp} of {len(pk2)} (panel, pair, chooser) "
      f"cells for FREE vs PAID and {moved_sp} for SCREEN vs PAID.")
    P(f"  |dOOS Sharpe| FREE vs PAID: mean {dd_fp.mean():.4f}, max {dd_fp.max():.4f}, "
      f">= 0.05 at {big} of {len(dd_fp)}.")
    P(f"  |dOOS Sharpe| SCREEN vs PAID: mean {dd_sp.mean():.4f}, max {dd_sp.max():.4f}, "
      f">= 0.05 at {int((dd_sp >= 0.05).sum())} of {len(dd_sp)}.")
    hyp("H_CAPITAL", "|dOOS Sharpe| >= 0.05 at >= half the (panel, pair, chooser) cells",
        f"{big} of {len(dd_fp)} (FREE vs PAID), {int((dd_sp >= 0.05).sum())} of "
        f"{len(dd_sp)} (SCREEN vs PAID); picks move {moved_fp} and {moved_sp}",
        big >= len(dd_fp) / 2.0)

    # the best 4b book, full AND OOS, and whether a chooser reaches it
    best = WF[WF.pass_4b_full & WF.pass_4b_oos].sort_values("OOS_Sharpe", ascending=False)
    P("")
    if len(best):
        b = best.iloc[0]
        reach = PK[(PK.pick == b.book) & (PK.panel == b.panel)]
        P(f"  BEST 4b (full AND OOS) BOOK: {b.panel}/{b.book}  full "
          f"{b.CAGR:.2%} / {b.Sharpe:.4f} / {b.MaxDD:.2%} (H1 {b.H1:.4f} / H2 {b.H2:.4f}); "
          f"OOS {b.OOS_CAGR:.2%} / {b.OOS_Sharpe:.4f} / {b.OOS_MaxDD:.2%}")
        sb = ispool[b.panel]["sb"]
        lb = ispool[b.panel]["lb"]
        P(f"    SPY  ({b.panel}) full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / "
          f"{sb['MaxDD']:.2%}; OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")
        P(f"    LIVE RULES v2 full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / "
          f"{lb['MaxDD']:.2%}; OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / "
          f"{lb['OOS_MaxDD']:.2%}")
        P(f"    IS-chooser-reachable: {'YES' if len(reach) else 'NO'} "
          f"({len(reach)} of {len(PK)} picks land on it)  |  4a: "
          f"{'PASS' if b.pass_4a else 'FAIL'}")
    else:
        P("  BEST 4b BOOK: none — no book passes 4b full AND OOS on this population.")

    # ------------------------------------------------------------------- write-out
    P("")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYP).to_csv(f"{OUT}.hypotheses.csv", index=False)
    P(f"  gates {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS; hypotheses "
      f"{sum(h['supported'] for h in HYP)} of {len(HYP)} SUPPORTED.")
    P(f"  total runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
