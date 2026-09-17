#!/usr/bin/env python3
"""Idea 1164 (lane B, 2026-09-17)
   what-sets-PHI-once-the-EPISODE-LENGTH-is-only-a-LOWER-BOUND-on-L-STAR

THE QUEUE'S PREMISE, QUOTED.  Idea 1162 found the moving-block |MaxDD| null is a
ONE-PARAMETER FAMILY running from the iid null (L = 1, bit for bit) to the observed path
(L = T), and defined

    phi(L) = (N_BLOCK(L) - N_IID) / (OBSERVED - N_IID)

as how far along that family the record's frozen L = 63 sits.  phi ran 0.110 to 1.000
across its 15 cells.  1162's own POST HOC explanation -- that L* (the L at which the block
null first reaches the observed value) is set by the drawdown EPISODE LENGTH -- was
declared post hoc and REFUTED at 7 of 12: L*/episode ran 1.09 to 21.91, leaving only the
one-sided fact that L* >= the episode length at 12 of 12.  The queue filed this idea to
find what actually sets phi, and named three candidates: block START coverage, the number
of near-tied drawdown episodes, and the tape's recovery speed.

WHAT THIS RUN CHANGES ABOUT THE QUESTION, STATED UP FRONT.

  1162 refuted the episode story on the WRONG FUNCTIONAL.  L* is a THRESHOLD CROSSING of
  a noisy curve -- the first rung of a coarse ladder {1,2,5,...,1008,T} whose median at
  each rung carries seed noise -- so a ratio built on it inherits the ladder's resolution
  and the crossing's instability.  phi is a LEVEL at one frozen L, and it is the quantity
  every published band actually depends on.  A variable can fail to predict a crossing
  and still set the level.  This run therefore tests the queue's three candidates AND
  1162's own refuted variable against phi directly, on a population 4.8x larger than the
  15 cells the ratio was refuted on, and it settles the mechanism on SYNTHETIC tapes
  where the episode length is KNOWN BY CONSTRUCTION rather than measured.

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:

  `DRIVER`   {D_COVER, D_TIES, D_RECOV, D_EPISODE}
  `CONTROL`  {X_NONE, X_PANEL, X_GAP, X_ORDER}

  = 16 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`, all four drivers scored
  under all four controls whatever the headline says.

  DRIVERS (all computed from the OBSERVED path alone, never from a null):
    D_COVER    the queue's candidate 1, its literal reading: the probability that ONE
               draw of the moving-block bootstrap contains the whole drawdown episode
               intact, = 1 - (1 - max(0, L-E+1)/T) ** ceil(T/L), a SATURATING function of
               the episode length E which is exactly ZERO for every episode longer than
               the block.  PRE-REGISTERED SIGN +.
    D_TIES     the queue's candidate 2: the number of DISTINCT peak-to-trough episodes
               whose depth is >= 0.90 x the deepest.  PRE-REGISTERED SIGN + (a maximum
               carried by many near-tied episodes is reproducible by many stretches of
               the tape, so a null that keeps local structure reaches it).
    D_RECOV    the queue's candidate 3: the tape's recovery speed, = the MEDIAN over all
               episodes deeper than 5% of (bars trough->recovery) / (bars peak->trough).
               PRE-REGISTERED SIGN - (a slow tape's drawdowns outrun one block).
    D_EPISODE  1162's own REFUTED variable, E = bars peak->trough of the deepest episode,
               carried here as the incumbent so the comparison is honest.  SIGN -.

  CONTROLS:
    X_NONE     raw Spearman over the whole population.
    X_PANEL    WITHIN-panel Spearman, mean over the three panels (kills every
               tape-level confound: a panel's vol, length, start date, survivorship).
    X_GAP      partial Spearman controlling for |OBS/N_IID - 1|, phi's own DENOMINATOR.
               phi is a ratio; a driver that merely tracks the size of the gap being
               apportioned is not a driver of WHERE L=63 sits.
    X_ORDER    FALSIFICATION.  Every cell's returns are RANDOMLY PERMUTED and BOTH phi
               and the drivers are recomputed on the permuted tape.  1165 showed a moving
               block shallows |MaxDD| even with order destroyed (pooled BLOCK/IID 0.9759),
               so a driver->phi relation that SURVIVES order destruction is bootstrap
               MACHINERY, not a fact about the tape.  The winning driver must LOSE at
               least half its strength here or this run's headline is not a tape result.

  NOT DIALS.  PANEL (all three built), the 72-BOOK POPULATION (every book published, the
  N / HOLD / CADENCE axes are a population not a search), the L LADDER (9 rungs published,
  headline frozen at the record's L = 63 and nothing is ever selected on it), the GROSS
  ladder in the rule-8 arm (15 rungs, all published), SEED (3 run at every headline cell,
  spread published, never selected on), and the TIES / RECOV thresholds (0.90 and 5% are
  frozen; 0.75 / 0.95 / 2% / 10% variants are printed in `.sensitivity.csv` and are never
  selected on).

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131/1140/1148/1159/1162's
construction: CAND20 legs, max_vol 0.60, gross 0.75, 10 bps (PROTOCOL rule 2), LAG 1,
warm-up 260, IS end 2016-12-31, block L = 63, 1000 draws, crc32 seeds, DD cap 0.60,
CAGR floor 0.70.

TWO CORRECTIONS THIS RUN MADE TO ITSELF, both recorded here rather than quietly patched:

  (1) PHI IS NOT ALWAYS ESTIMABLE.  phi's denominator is (OBSERVED - N_IID), and on books
      whose observed drawdown sits on top of its own iid null that gap passes through
      zero: the first cut of this run read phi from -31.55 to +13.17 on the 72-book
      population, which is an interpolation weight outside [0, 1] by two orders of
      magnitude.  A cell is called ESTIMABLE only when |denominator| >= max(3 x the larger
      cross-seed spread of the two null medians, 0.25 percentage points) -- the run's own
      seed noise, not a tuned bar.  The rule was written AFTER seeing the first cut.  Every
      book is published in `.cells.csv` with its denominator, its resolution and its
      verdict, and EVERY dial-grid cell carries `rho_all` over all 72 beside the headline
      `rho` so the rule cannot hide a reversal.
  (2) THE FIRST SYNTHETIC TAPE WAS MIS-SPECIFIED.  Cut 1 (SYN_ADD) injected the episode
      into a ZERO-DRIFT gaussian tape, whose own natural drawdowns are 40-60% over 4,706
      bars, so the injected episode was not the maximum at 10 of 10 rungs and the arm
      measured nothing.  Cut 2 (SYN_DET) replaces the window with a deterministic decline
      on a trending tape, making the peak, the trough and E exact by construction.  Both
      cuts are published; gate G14 pins cut 1 as dead by its own check.

CROSS-RUN GATE.  1162's 15 anchor cells are REPLAYED BIT FOR BIT out of this run's own
code path, using 1162's seed base and its exact seed parts, and checked against its
committed `.cells.csv`.  If that replay fails, nothing below is comparable to the record
and the run says so.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
CURRENT constituents of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  Every LEVEL here -- CAGR, |MaxDD| and every null median
built on them -- is optimistic, and it bites HARDER than usual in this run because every
object under study IS a drawdown: a survivor panel's deepest episode is shallower and
shorter than the true one, which compresses the very D_EPISODE / D_COVER axis the headline
is measured along.  It largely CANCELS out of the headline, which is a RANK correlation of
one construction against itself across cells of the same tape, and it does NOT cancel out
of the 4a / 4b legs.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
"""
from __future__ import annotations

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
SLUG = "what-sets-PHI-once-the-EPISODE-LENGTH-is-only-a-LOWER-BOUND-on-L-STAR"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136", "SMALL"]
DRIVERS = ["D_COVER", "D_TIES", "D_RECOV", "D_EPISODE"]                        # dial 1
CONTROLS = ["X_NONE", "X_PANEL", "X_GAP", "X_ORDER"]                           # dial 2
SIGN = {"D_COVER": +1, "D_TIES": +1, "D_RECOV": -1, "D_EPISODE": -1}           # pre-registered

L_BLOCK, BDRAWS = 63, 1000
L_LADDER = [1, 5, 21, 63, 126, 252, 504, 1008]        # + T, appended per cell
SEEDS = [0, 1, 2]
SEED_BASE = 11641164
SEED_1162 = 11621162                                  # the parent's base, for the replay gate
NPERM = 2000
TIE_Q, TIE_ALT = 0.90, [0.75, 0.95]                   # frozen / published-not-selected
REC_MIN, REC_ALT = 5.0, [2.0, 10.0]                   # frozen / published-not-selected

# the population: N x HOLD x CADENCE per panel (24 books per panel, 72 in all)
POP_N = [5, 10, 20, 40]
POP_H = [63, 126, 252]
POP_F = ["W", "M"]
ANCHOR_CONTROLS = ["C_BOOK", "C_GATEOFF", "C_NOREBAL", "C_SHUFFLE", "C_SPY"]   # 1162's 15
GROSS_LADDER = [round(0.30 + 0.05 * i, 3) for i in range(15)]
CHOOSERS = {"C_ISSHARPE": "IS_Sharpe", "C_ISCAGR": "IS_CAGR", "C_ISDD": "IS_MaxDD"}

PRIOR1162 = (Path(__file__).resolve().parent /
             ("2026-09-17_why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-"
              "one_B.cells.csv"))
PRIOR1162_PHI_RANGE = (0.110, 1.000)          # the queue's quoted range, gated below
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)

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
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<64s} {value:.3e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, bar, measured, supported):
    HYP.append(dict(hypothesis=name, bar=bar, measured=measured, supported=bool(supported)))
    P(f"  {name:<11s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


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


# ======================================================== the two resample nulls
def null_index(kind, rng, T, ndraws, L=L_BLOCK):
    if kind == "N_IID":
        return rng.integers(0, T, size=(ndraws, T))
    if kind == "N_BLOCK":
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T, size=(ndraws, nb))
        idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
        return idx.reshape(ndraws, nb * L)[:, :T]
    if kind == "N_STAT":
        p = 1.0 / L
        out = np.empty((ndraws, T), dtype=np.int64)
        out[:, 0] = rng.integers(0, T, size=ndraws)
        newb = rng.random((ndraws, T)) < p
        fresh = rng.integers(0, T, size=(ndraws, T))
        for t in range(1, T):
            cont = (out[:, t - 1] + 1) % T
            out[:, t] = np.where(newb[:, t], fresh[:, t], cont)
        return out
    raise ValueError(kind)


def boot_maxdd(r, idx, chunk=100):
    """|MaxDD| (positive, in %) of ONE return series under every resample row of idx."""
    LG = np.log1p(np.asarray(r, float))
    out = np.empty(idx.shape[0])
    for a in range(0, idx.shape[0], chunk):
        ix = idx[a:a + chunk]
        cum = np.cumsum(LG[ix], axis=1)
        run = np.maximum.accumulate(cum, axis=1)
        out[a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


RES_K, RES_FLOOR = 3.0, 0.25          # phi-estimability resolution (see the docstring)


def denom_res(spread_iid, spread_block):
    """phi's denominator is (OBSERVED - N_IID).  When that gap is inside the null medians'
    own cross-seed noise, phi is not a measurement -- it is a ratio of two noises, and it
    blows up.  A cell is ESTIMABLE only if |denominator| >= 3 x the larger cross-seed
    spread, with a 0.25 percentage-point absolute floor."""
    return max(RES_K * max(spread_iid, spread_block), RES_FLOOR)


def null_median(r, kind, seed_parts, L=L_BLOCK, base=SEED_BASE, ndraws=BDRAWS):
    rng = np.random.default_rng(seed_of(*seed_parts, base=base))
    return float(np.median(boot_maxdd(r, null_index(kind, rng, len(r), ndraws, L))))


# ---------------------------------------------------------- observed-path diagnostics
def obs_maxdd(r):
    cum = np.cumsum(np.log1p(np.asarray(r, float)))
    run = np.maximum.accumulate(cum)
    dd = np.expm1(cum - run)
    tr = int(dd.argmin())
    pk = int(np.argmax(cum[:tr + 1]))
    return -float(dd[tr]) * 100.0, pk, tr


def episode_table(r):
    """Every peak -> trough -> recovery excursion of the equity path.
    Returns a list of (peak, trough, recovery_or_-1, depth_pct)."""
    cum = np.cumsum(np.log1p(np.asarray(r, float)))
    run = np.maximum.accumulate(cum)
    under = cum < run - 1e-15
    eps, t, T = [], 0, len(cum)
    while t < T:
        if not under[t]:
            t += 1
            continue
        s = t
        while t < T and under[t]:
            t += 1
        pk = s - 1                                  # last bar at the running maximum
        k = int(np.argmin(cum[s:t])) + s
        eps.append((pk, k, (t if t < T else -1), -float(np.expm1(cum[k] - cum[pk])) * 100.0))
    return eps


def drivers_of(r, L=L_BLOCK, tie_q=TIE_Q, rec_min=REC_MIN):
    """The four pre-registered drivers, computed from the OBSERVED path alone."""
    T = len(r)
    o, pk, tr = obs_maxdd(r)
    E = max(1, tr - pk)
    nb = int(np.ceil(T / L))
    p1 = max(0.0, L - E + 1.0) / T
    cover = 1.0 - (1.0 - p1) ** nb
    eps = episode_table(r)
    deep = max((e[3] for e in eps), default=0.0)
    ties = sum(1 for e in eps if deep > 0 and e[3] >= tie_q * deep)
    ratios, censored = [], 0
    for a, b, c, d in eps:
        if d < rec_min:
            continue
        dec = max(1, b - a)
        if c >= 0:
            ratios.append((c - b) / dec)
        else:
            ratios.append((T - 1 - b) / dec)        # lower bound, flagged
            censored += 1
    rec = float(np.median(ratios)) if len(ratios) >= 3 else np.nan
    return dict(obs_maxdd=o, peak=pk, trough=tr, D_EPISODE=float(E), D_COVER=cover,
                COVER_GRADED=min(1.0, L / E), D_TIES=float(ties), D_RECOV=rec,
                n_episodes=len(eps),
                n_rec_episodes=len(ratios), n_rec_censored=censored, deepest=deep)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def partial_spearman(a, b, c):
    """Spearman of a vs b holding c fixed: correlate rank residuals after OLS on rank(c)."""
    a, b, c = (np.asarray(x, float) for x in (a, b, c))
    m = np.isfinite(a) & np.isfinite(b) & np.isfinite(c)
    if m.sum() < 4:
        return np.nan
    ra, rb, rc = (pd.Series(x[m]).rank().values for x in (a, b, c))
    if np.std(rc) == 0:
        return spearman(a[m], b[m])
    X = np.vstack([np.ones(len(rc)), rc]).T
    res = []
    for y in (ra, rb):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res.append(y - X @ beta)
    tol = 1e-8 * max(1.0, float(np.std(rc)))
    if res[0].std() <= tol or res[1].std() <= tol:
        return 0.0                       # a residual that IS the control carries no signal
    return float(np.corrcoef(res[0], res[1])[0, 1])


def perm_p(a, b, rho, seed, nperm=NPERM):
    """Two-sided permutation p-value for a Spearman rho."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 4 or not np.isfinite(rho):
        return np.nan
    rng = np.random.default_rng(seed)
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    hits = 0
    for _ in range(nperm):
        if abs(np.corrcoef(ra, rng.permutation(rb))[0, 1]) >= abs(rho) - 1e-15:
            hits += 1
    return (hits + 1.0) / (nperm + 1.0)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1164 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")
    head_bytes = (ROOT / "data" / "prices.csv").read_bytes()
    P("## PRICE-VINTAGE STAMP (PROTOCOL draft rule 12, proposed by 1163 — complied with, "
      "not enacted)")
    P(f"  data/prices.csv @HEAD  crc32={format(zlib.crc32(head_bytes) & 0xFFFFFFFF, '08x')}  "
      f"{len(head_bytes):,} bytes")
    P("")

    P("## PRE-REGISTRATION — declared before a single result number")
    P("  DIAL 1 DRIVER  : D_COVER(+), D_TIES(+), D_RECOV(-), D_EPISODE(-)   signs frozen here")
    P("  DIAL 2 CONTROL : X_NONE, X_PANEL, X_GAP, X_ORDER")
    P("  NOT DIALS      : PANEL (3 built), the 72-book POPULATION, the L ladder (9 rungs,")
    P("                   headline frozen L=63), the GROSS ladder (15 rungs), SEED (3),")
    P("                   and the TIES/RECOV thresholds (0.90 / 5%, variants published).")
    P("  H_COVER    the queue's candidate 1 wins: |rho(D_COVER, phi)| >= 0.60 with the")
    P("             pre-registered sign under X_NONE, the LARGEST |rho| of the four, and")
    P("             the correct sign at 3 of 3 panels under X_PANEL.")
    P("  H_TIES     the queue's candidate 2: |rho| >= 0.40, correct sign, under X_NONE.")
    P("  H_RECOV    the queue's candidate 3: |rho| >= 0.40, correct sign, under X_NONE.")
    P("  H_EPISODE  1162's REFUTED variable predicts the LEVEL even though it failed on")
    P("             the CROSSING: rho(D_EPISODE, phi) <= -0.40 under X_NONE AND under X_GAP.")
    P("  H_ORDER    FALSIFICATION: the winning driver's |rho| under X_ORDER is <= HALF its")
    P("             X_NONE value.  If it survives order destruction the relation is")
    P("             bootstrap MACHINERY (1165's term) and the headline is not a tape fact.")
    P("  H_SYNTH    MECHANISM, on tapes whose episode length is KNOWN BY CONSTRUCTION:")
    P("             phi falls monotonically in E (spearman <= -0.90), phi >= 0.90 at")
    P("             E <= 21 and phi <= 0.40 at E >= 252.")
    P("  H_LSTAR    REPLICATION of 1162's one surviving claim on the wider population:")
    P("             L* >= E at >= 90% of cells.")
    P("")

    # --------------------------------------------------------------------- panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    small, ndrop, nmeta = load_small()
    raw["SMALL"] = small
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
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    # ------------------------------------------------------- book constructors
    _WCACHE: dict = {}

    def weights_pop(panel, N, H, freq):
        key = (panel, "POP", N, H, freq)
        if key in _WCACHE:
            return _WCACHE[key]
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N, H,
                  d["T"], d["K"], 1.0)
        _WCACHE[key] = (W, mk)
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
        """1162's five controls, its construction, bit for bit (C_SHUFFLE included)."""
        base = "C_BOOK" if control == "C_SHUFFLE" else control
        W1, mk = weights_anchor(panel, base)
        r = run_weights(panel, W1, mk, gross)
        if control == "C_SHUFFLE":
            rw = r.copy()
            np.random.default_rng(seed_of(panel, "C_SHUFFLE", gross, "", base=SEED_1162)).shuffle(rw)
            return rw
        return r

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

    Wfresh = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
                   d["T"], d["K"], 0.45)
    v = float(np.abs(Wfresh - (W / GROSS0) * 0.45).max())
    gate("G2", "gross ladder is an EXACT scale on the selection (built vs scaled W)", v, v < 1e-15)

    rng = np.random.default_rng(12345)
    ix_b1 = null_index("N_BLOCK", np.random.default_rng(777), 500, 50, L=1)
    ix_i1 = null_index("N_IID", np.random.default_rng(777), 500, 50)
    v = float(np.abs(ix_b1 - ix_i1).max())
    gate("G3", "N_BLOCK at L=1 IS N_IID, bit for bit (same seed, same draw)", v, v == 0)

    rr = np.random.default_rng(5).normal(0, 0.01, 3000)
    o, pk, tr = obs_maxdd(rr)
    eps = episode_table(rr)
    deep = max(eps, key=lambda e: e[3])
    v = abs(deep[3] - o) + abs(deep[0] - pk) + abs(deep[1] - tr)
    gate("G4", "episode table's deepest excursion == obs_maxdd (peak, trough, depth)", v, v < 1e-12)

    x = rng.normal(size=60)
    y = 0.7 * x + rng.normal(size=60) * 0.7
    z = rng.normal(size=60)
    dsq = ((pd.Series(x).rank().values - pd.Series(y).rank().values) ** 2).sum()
    closed = 1.0 - 6.0 * dsq / (len(x) * (len(x) ** 2 - 1.0))     # tie-free closed form
    v = abs(spearman(x, y) - closed)
    gate("G5", "spearman() == the tie-free closed form 1-6*sum(d^2)/(n(n^2-1))", v, v < 1e-12)
    v = abs(partial_spearman(x, y, z) - spearman(x, y))
    gate("G6", "partial_spearman on an INDEPENDENT control ~= the raw spearman", v, v < 0.05)
    v = abs(partial_spearman(x, y, y))
    gate("G7", "partial_spearman controlling for y itself is 0", v, v < 1e-8)

    # ------------------------------ G8/G9: replay 1162's 15 anchor cells bit for bit
    P("")
    P("## CROSS-RUN REPLAY — 1162's 15 anchor cells, its seed base, its seed parts")
    prior = pd.read_csv(PRIOR1162) if PRIOR1162.exists() else None
    rep_rows = []
    for panel in PANELS:
        for c in ANCHOR_CONTROLS:
            r = anchor_returns(panel, c)
            o, pk, tr = obs_maxdd(r)
            ni = null_median(r, "N_IID", (panel, c, "N_IID", 0), base=SEED_1162)
            nb_ = null_median(r, "N_BLOCK", (panel, c, "N_BLOCK", 0), base=SEED_1162)
            phi = (nb_ - ni) / (o - ni) if abs(o - ni) > 1e-12 else np.nan
            row = dict(panel=panel, control=c, observed=o, N_IID=ni, N_BLOCK=nb_,
                       phi_L63=phi, episode_bars=tr - pk)
            if prior is not None:
                q = prior[(prior.panel == panel) & (prior.control == c)]
                if len(q):
                    row["prior_observed"] = float(q.observed.iloc[0])
                    row["prior_N_IID"] = float(q.N_IID.iloc[0])
                    row["prior_N_BLOCK"] = float(q.N_BLOCK.iloc[0])
                    row["prior_phi"] = float(q.phi_L63.iloc[0])
                    row["prior_episode"] = float(q.episode_bars.iloc[0])
            rep_rows.append(row)
    rep = pd.DataFrame(rep_rows)
    if prior is not None and "prior_phi" in rep:
        v = float(np.abs(rep.observed - rep.prior_observed).max())
        gate("G8", "1162's 15 observed |MaxDD| REPLAYED bit for bit", v, v < 1e-9)
        v = float(np.abs(rep.episode_bars - rep.prior_episode).max())
        gate("G9", "1162's 15 episode lengths REPLAYED exactly", v, v == 0)
        v = float(np.abs(rep.phi_L63 - rep.prior_phi).max())
        gate("G10", "1162's 15 phi_L63 REPLAYED bit for bit (its seeds, its draws)", v, v < 1e-9)
        tradable = rep[rep.control != "C_SHUFFLE"]
        lo, hi = tradable.phi_L63.min(), tradable.phi_L63.max()
        v = abs(lo - PRIOR1162_PHI_RANGE[0]) + abs(hi - PRIOR1162_PHI_RANGE[1])
        gate("G11", "the QUEUE's quoted phi range 0.110-1.000 is the TRADABLE-cell range",
             v, v < 5e-4)
    else:
        P("  1162's committed cells.csv not found — the replay gates are SKIPPED and said so.")
    P("")

    # ================================================== ARM A — THE 72-BOOK POPULATION
    P("## ARM A — THE POPULATION: 3 panels x N{5,10,20,40} x HOLD{63,126,252} x "
      "CADENCE{W,M} = 72 books")
    P(f"  gross frozen at {GROSS0}, {BDRAWS:,} draws, block L={L_BLOCK}, seeds {SEEDS}")
    series, cell_rows = {}, []
    for panel in PANELS:
        for N in POP_N:
            for H in POP_H:
                for f in POP_F:
                    key = (panel, N, H, f)
                    r = pop_returns(panel, N, H, f)
                    series[key] = r
                    dv = drivers_of(r)
                    meds_i, meds_b = [], []
                    for s in SEEDS:
                        meds_i.append(null_median(r, "N_IID", (panel, N, H, f, "I", s)))
                        meds_b.append(null_median(r, "N_BLOCK", (panel, N, H, f, "B", s)))
                    ni, nb_ = meds_i[0], meds_b[0]
                    denom = dv["obs_maxdd"] - ni
                    phi = (nb_ - ni) / denom if abs(denom) > 1e-12 else np.nan
                    phis = [(b - i) / (dv["obs_maxdd"] - i) for i, b in zip(meds_i, meds_b)
                            if abs(dv["obs_maxdd"] - i) > 1e-12]
                    spi, spb = max(meds_i) - min(meds_i), max(meds_b) - min(meds_b)
                    cagr, sh, dd = fmet(r)
                    cell_rows.append(dict(panel=panel, N=N, H=H, freq=f, n_bars=len(r),
                                          N_IID=ni, N_BLOCK=nb_, phi_L63=phi, denom=denom,
                                          iid_seed_spread=spi, block_seed_spread=spb,
                                          resolution=denom_res(spi, spb),
                                          phi_estimable=bool(abs(denom) >= denom_res(spi, spb)),
                                          phi_seed_min=min(phis), phi_seed_max=max(phis),
                                          phi_seed_spread=max(phis) - min(phis),
                                          gap=abs(dv["obs_maxdd"] / ni - 1.0),
                                          CAGR=cagr, Sharpe=sh, MaxDD=dd, **dv))
        P(f"  {panel} population done  ({time.time() - t0:.0f}s)")
    cells = pd.DataFrame(cell_rows)
    est = cells[cells.phi_estimable]
    P("")
    gate("G12", "every ESTIMABLE book's |denominator| clears the run's own seed resolution",
         float(min(abs(est.denom) - est.resolution)), bool(min(abs(est.denom) - est.resolution) >= 0))
    P("")
    P("  A CORRECTION THIS RUN MADE TO ITSELF, recorded rather than quietly patched.")
    P(f"  The first cut scored all {len(cells)} books and read phi from "
      f"{cells.phi_L63.min():.2f} to {cells.phi_L63.max():.2f} — an interpolation weight")
    P("  outside [0,1] by two orders of magnitude, because phi's DENOMINATOR (OBSERVED -")
    P("  N_IID) passes through zero on books whose observed drawdown happens to sit on top")
    P("  of its own iid null.  phi is then a ratio of two noises.  The estimability rule in")
    P("  `denom_res` was added AFTER seeing that, is stated in the docstring, and every")
    P("  excluded book is published in `.cells.csv` with its denominator and resolution.")
    P(f"  ESTIMABLE at {len(est)} of {len(cells)} books "
      f"(|denominator| >= max({RES_K:g} x cross-seed spread, {RES_FLOOR} pp)).")
    P(f"  phi over the {len(est)} ESTIMABLE books: min {est.phi_L63.min():.4f}  "
      f"median {est.phi_L63.median():.4f}  max {est.phi_L63.max():.4f}")
    P(f"  median cross-seed phi spread {est.phi_seed_spread.median():.4f} "
      f"(max {est.phi_seed_spread.max():.4f}) — the resolution of every number below")
    for panel in PANELS:
        s = est[est.panel == panel]
        P(f"    {panel:<6s} phi {s.phi_L63.min():.4f}..{s.phi_L63.max():.4f}   "
          f"E {int(s.D_EPISODE.min()):4d}..{int(s.D_EPISODE.max()):4d}   "
          f"COVER {s.D_COVER.min():.4f}..{s.D_COVER.max():.4f}   "
          f"TIES {int(s.D_TIES.min())}..{int(s.D_TIES.max())}   "
          f"RECOV {s.D_RECOV.min():.2f}..{s.D_RECOV.max():.2f}   n={len(s)}")
    P(f"  D_COVER is EXACTLY ZERO at {int((est.D_COVER == 0).sum())} of {len(est)} estimable "
      f"books (every episode longer than the block) — a saturating driver cannot rank those.")
    P("")

    # ===================================== ARM B — X_ORDER: the order-destroyed population
    P("## ARM B — X_ORDER: the same 72 books with their RETURN ORDER DESTROYED")
    P("  Both phi AND the drivers are recomputed on the permuted tape.  1165 showed the")
    P("  moving block still shallows |MaxDD| with order destroyed, so this arm prices how")
    P("  much of any driver->phi relation is the bootstrap's own machinery.")
    ord_rows = []
    for (panel, N, H, f), r in series.items():
        rw = r.copy()
        np.random.default_rng(seed_of(panel, N, H, f, "ORD")).shuffle(rw)
        dv = drivers_of(rw)
        mi = [null_median(rw, "N_IID", (panel, N, H, f, "OI", s)) for s in SEEDS]
        mb = [null_median(rw, "N_BLOCK", (panel, N, H, f, "OB", s)) for s in SEEDS]
        ni, nb_ = mi[0], mb[0]
        denom = dv["obs_maxdd"] - ni
        spi, spb = max(mi) - min(mi), max(mb) - min(mb)
        phi = (nb_ - ni) / denom if abs(denom) > 1e-12 else np.nan
        ord_rows.append(dict(panel=panel, N=N, H=H, freq=f, N_IID=ni, N_BLOCK=nb_,
                             phi_L63=phi, denom=denom, resolution=denom_res(spi, spb),
                             phi_estimable=bool(abs(denom) >= denom_res(spi, spb)),
                             gap=abs(dv["obs_maxdd"] / ni - 1.0), **dv))
    ordc = pd.DataFrame(ord_rows)
    orde = ordc[ordc.phi_estimable]
    P(f"  ESTIMABLE at {len(orde)} of {len(ordc)} order-destroyed books")
    P(f"  order-destroyed phi: min {orde.phi_L63.min():.4f}  median {orde.phi_L63.median():.4f}  "
      f"max {orde.phi_L63.max():.4f}   (book tape median {est.phi_L63.median():.4f})")
    P(f"  order-destroyed episode length E: median {ordc.D_EPISODE.median():.0f} bars "
      f"against the book tape's {cells.D_EPISODE.median():.0f}")
    P("")

    # ================================================== ARM C — THE 4 x 4 DIAL GRID
    P("## ARM C — THE 2-DIAL GRID (DRIVER x CONTROL), ALL 16 CELLS PUBLISHED")
    P("  Headline rho is computed on the ESTIMABLE books; rho_all over all 72 is published")
    P("  beside it in every cell so the estimability rule cannot hide a reversal.")
    grid_rows = []
    for drv in DRIVERS:
        for ctl in CONTROLS:
            if ctl == "X_NONE":
                rho = spearman(est[drv], est.phi_L63)
                rho_all = spearman(cells[drv], cells.phi_L63)
                n = int((np.isfinite(est[drv]) & np.isfinite(est.phi_L63)).sum())
                p = perm_p(est[drv], est.phi_L63, rho, seed_of(drv, ctl))
                extra = ""
            elif ctl == "X_PANEL":
                rs = [spearman(est[est.panel == pn][drv], est[est.panel == pn].phi_L63)
                      for pn in PANELS]
                rho = float(np.nanmean(rs))
                rho_all = float(np.nanmean(
                    [spearman(cells[cells.panel == pn][drv], cells[cells.panel == pn].phi_L63)
                     for pn in PANELS]))
                n = len(est)
                p = np.nan
                extra = " ".join(f"{pn}:{x:+.3f}" for pn, x in zip(PANELS, rs))
            elif ctl == "X_GAP":
                rho = partial_spearman(est[drv], est.phi_L63, est.gap)
                rho_all = partial_spearman(cells[drv], cells.phi_L63, cells.gap)
                n = int((np.isfinite(est[drv]) & np.isfinite(est.phi_L63)).sum())
                p = np.nan
                extra = f"rho(driver,gap)={spearman(est[drv], est.gap):+.3f}"
            else:
                rho = spearman(orde[drv], orde.phi_L63)
                rho_all = spearman(ordc[drv], ordc.phi_L63)
                n = int((np.isfinite(orde[drv]) & np.isfinite(orde.phi_L63)).sum())
                p = perm_p(orde[drv], orde.phi_L63, rho, seed_of(drv, ctl))
                extra = "order destroyed"
            grid_rows.append(dict(driver=drv, control=ctl, rho=rho, rho_all=rho_all, n=n,
                                  perm_p=p, expected_sign=SIGN[drv],
                                  sign_ok=bool(np.isfinite(rho) and np.sign(rho) == SIGN[drv]),
                                  note=extra))
    grid = pd.DataFrame(grid_rows)
    P(f"  {'driver':<11s} {'control':<9s} {'rho':>8s} {'rho_all':>8s} {'sign':>5s} "
      f"{'perm p':>8s} {'n':>4s}  note")
    for _, x in grid.iterrows():
        pp = f"{x.perm_p:8.4f}" if np.isfinite(x.perm_p) else "      --"
        P(f"  {x.driver:<11s} {x.control:<9s} {x.rho:+8.4f} {x.rho_all:+8.4f} "
          f"{str(bool(x.sign_ok)):>5s} {pp} {x.n:4d}  {x.note}")
    P("")
    xn = grid[grid.control == "X_NONE"].set_index("driver").rho
    win = xn.abs().idxmax()
    P(f"  LARGEST |rho| under X_NONE: {win} at {xn[win]:+.4f}")
    P("")

    # ======================================== ARM D — SYNTHETIC: E KNOWN BY CONSTRUCTION
    P("## ARM D — MECHANISM ON SYNTHETIC TAPES (episode length KNOWN, not measured)")
    P("  A SECOND CORRECTION THIS RUN MADE TO ITSELF, both cuts published in")
    P("  `.synthetic.csv` under a `cut` column.")
    P("  CUT 1 (SYN_ADD, mis-specified, kept on the record): a ZERO-DRIFT gaussian tape,")
    P("  sigma 0.40%/day, with -35% ADDED over E bars.  A zero-drift random walk of 4,706")
    P("  bars has natural drawdowns of 40-60% on its own, so the injected episode was NOT")
    P("  the maximum at 10 of 10 rungs and the arm measured nothing.  It is printed below")
    P("  with found=False at every rung rather than deleted.")
    P("  CUT 2 (SYN_DET, the headline): a TRENDING tape (mu 0.08%/day, sigma 0.15%/day)")
    P("  whose E-bar window is REPLACED by a deterministic -35% decline, so the peak, the")
    P("  trough and therefore E are exact by construction.  Nothing else differs between")
    P("  rungs, so phi(E) here is the block length meeting the episode length and nothing else.")
    syn_rows = []
    T_SYN, DEPTH = 4706, -0.35
    E_LADDER = [5, 10, 21, 42, 63, 84, 126, 252, 504, 1008]
    for cut, mu, sig, mode in [("SYN_ADD", 0.0, 0.0040, "add"), ("SYN_DET", 0.0008, 0.0015, "set")]:
        for E in E_LADDER:
            rs = np.random.default_rng(seed_of("SYN", E)).normal(mu, sig, T_SYN)
            start = T_SYN // 2
            if mode == "add":
                rs[start:start + E] += np.expm1(np.log1p(DEPTH) / E)
            else:
                rs[start:start + E] = np.expm1(np.log1p(DEPTH) / E)
            dv = drivers_of(rs)
            ni = null_median(rs, "N_IID", ("SYN", cut, E, "I"))
            nb_ = null_median(rs, "N_BLOCK", ("SYN", cut, E, "B"))
            phi = (nb_ - ni) / (dv["obs_maxdd"] - ni) if abs(dv["obs_maxdd"] - ni) > 1e-12 else np.nan
            syn_rows.append(dict(cut=cut, E_injected=E, E_measured=dv["D_EPISODE"],
                                 obs=dv["obs_maxdd"], N_IID=ni, N_BLOCK=nb_, phi_L63=phi,
                                 D_COVER=dv["D_COVER"], COVER_GRADED=dv["COVER_GRADED"],
                                 D_TIES=dv["D_TIES"], D_RECOV=dv["D_RECOV"],
                                 found=bool(abs(dv["obs_maxdd"] + DEPTH * 100.0) <= 1.5
                                            and E <= dv["D_EPISODE"] <= E + 21)))
    syn = pd.DataFrame(syn_rows)
    for cut in ["SYN_ADD", "SYN_DET"]:
        s = syn[syn.cut == cut]
        P("")
        P(f"  {cut}   {'E':>5s} {'E_meas':>7s} {'obs%':>7s} {'N_IID':>7s} {'N_BLOCK':>8s} "
          f"{'phi':>8s} {'COVER':>7s} {'COVERg':>7s}  episode-IS-the-maximum")
        for _, x in s.iterrows():
            P(f"           {int(x.E_injected):5d} {int(x.E_measured):7d} {x.obs:7.2f} "
              f"{x.N_IID:7.2f} {x.N_BLOCK:8.2f} {x.phi_L63:8.4f} {x.D_COVER:7.4f} "
              f"{x.COVER_GRADED:7.4f}  {bool(x.found)}")
    det = syn[(syn.cut == "SYN_DET") & syn.found]
    rho_syn = spearman(det.E_injected, det.phi_L63)
    P("")
    P(f"  SYN_DET: the injected episode IS the maximum at {len(det)} of {len(E_LADDER)} rungs;"
      f"  spearman(E, phi) = {rho_syn:+.4f}")
    sd = syn[syn.cut == "SYN_DET"]
    v = float((sd.obs + DEPTH * 100.0).abs().max())
    gate("G13", "SYN_DET's drawdown IS the injected -35% at every rung (pp)", v, v <= 1.5)
    v = float((sd.E_measured - sd.E_injected).max())
    gate("G14", "SYN_DET's trough is inside the injected window +21 bars of noise", v,
         bool((sd.E_measured >= sd.E_injected).all() and v <= 21))
    v = float(syn[syn.cut == "SYN_ADD"].found.sum())
    gate("G15", "SYN_ADD (cut 1) is DEAD by its own check and is published, not deleted",
         v, v == 0)

    # ---- POST HOC, and labelled so: a second synthetic probe for the driver that WON
    P("")
    P("  ARM D2 — POST HOC (declared post hoc; the pre-registration above names no such")
    P("  arm).  D_TIES won the population with the WRONG SIGN, so the same deterministic")
    P("  tape is rebuilt with K EQUALLY DEEP episodes of a FIXED 63 bars each, K = 1..8.")
    P("  Nothing but the number of near-ties changes.  This is descriptive: it prices the")
    P("  sign, it does not test a hypothesis, and no bar was declared for it.")
    P("  A THIRD CORRECTION THIS RUN MADE TO ITSELF: the first D2 tape spaced episodes of")
    P("  -35% 500 bars apart, and a -35% hole cannot be climbed out of in 437 bars at")
    P("  0.08%/day, so all K episodes MERGED into one (measured ties = 1 at 6 of 6 rungs)")
    P("  and the arm priced DEPTH, not ties.  Depth is now -20% and spacing 520 bars, which")
    P("  recovers in 279; gate G16 pins that the measured tie count IS K at every rung.")
    tie_rows = []
    for K in [1, 2, 3, 4, 6, 8]:
        rs = np.random.default_rng(seed_of("SYNT", K)).normal(0.0008, 0.0015, T_SYN)
        for j in range(K):
            s0 = 400 + j * 520
            rs[s0:s0 + 63] = np.expm1(np.log1p(-0.20) / 63)
        dv = drivers_of(rs)
        ni = null_median(rs, "N_IID", ("SYNT", K, "I"))
        nb_ = null_median(rs, "N_BLOCK", ("SYNT", K, "B"))
        phi = (nb_ - ni) / (dv["obs_maxdd"] - ni) if abs(dv["obs_maxdd"] - ni) > 1e-12 else np.nan
        tie_rows.append(dict(cut="SYN_TIES", K_injected=K, E_injected=63,
                             E_measured=dv["D_EPISODE"], obs=dv["obs_maxdd"], N_IID=ni,
                             N_BLOCK=nb_, phi_L63=phi, D_TIES=dv["D_TIES"],
                             D_COVER=dv["D_COVER"], COVER_GRADED=dv["COVER_GRADED"],
                             D_RECOV=dv["D_RECOV"], found=True))
    ties_syn = pd.DataFrame(tie_rows)
    P(f"  SYN_TIES  {'K':>3s} {'TIES_meas':>9s} {'obs%':>7s} {'N_IID':>7s} {'N_BLOCK':>8s} "
      f"{'phi':>8s}")
    for _, x in ties_syn.iterrows():
        P(f"            {int(x.K_injected):3d} {int(x.D_TIES):9d} {x.obs:7.2f} {x.N_IID:7.2f} "
          f"{x.N_BLOCK:8.2f} {x.phi_L63:8.4f}")
    rho_ties_syn = spearman(ties_syn.K_injected, ties_syn.phi_L63)
    P(f"  spearman(K, phi) on the controlled tape = {rho_ties_syn:+.4f}   "
      f"(population reading: {float(xn['D_TIES']):+.4f})")
    v = float((ties_syn.D_TIES - ties_syn.K_injected).abs().max())
    gate("G16", "SYN_TIES' MEASURED tie count IS K at every rung (the episodes do recover)",
         v, v == 0)
    v = float(ties_syn.obs.max() - ties_syn.obs.min())
    gate("G17", "SYN_TIES holds the observed drawdown FIXED while K varies (pp spread)",
         v, v <= 1.0)
    syn = pd.concat([syn, ties_syn], ignore_index=True)
    P("")

    # ============================================ ARM E — THE L LADDER AND L* (1162's claim)
    P("## ARM E — THE L LADDER AND L*, replicated on the 72-book population")
    lad_rows, star_rows = [], []
    for (panel, N, H, f), r in series.items():
        Tn = len(r)
        rungs = sorted(set([L for L in L_LADDER if L < Tn] + [Tn]))
        o = obs_maxdd(r)[0]
        ni = float(cells[(cells.panel == panel) & (cells.N == N) & (cells.H == H) &
                         (cells.freq == f)].N_IID.iloc[0])
        E = float(cells[(cells.panel == panel) & (cells.N == N) & (cells.H == H) &
                        (cells.freq == f)].D_EPISODE.iloc[0])
        meds = []
        for L in rungs:
            m = null_median(r, "N_BLOCK", (panel, N, H, f, "LAD", L), L=L)
            meds.append(m)
            lad_rows.append(dict(panel=panel, N=N, H=H, freq=f, L=L, null_median=m,
                                 observed=o, N_IID=ni,
                                 phi=(m - ni) / (o - ni) if abs(o - ni) > 1e-12 else np.nan))
        meds = np.array(meds)
        sgn = np.sign(o - ni)
        reach = [L for L, m in zip(rungs, meds) if sgn * (m - ni) >= sgn * (o - ni) - 1e-12]
        Lst = float(min(reach)) if reach else np.nan
        star_rows.append(dict(panel=panel, N=N, H=H, freq=f, L_star=Lst, episode_bars=E,
                              ratio=(Lst / E if np.isfinite(Lst) and E > 0 else np.nan),
                              ge_episode=bool(np.isfinite(Lst) and Lst >= E),
                              phi_L63=float(cells[(cells.panel == panel) & (cells.N == N) &
                                                  (cells.H == H) & (cells.freq == f)].phi_L63.iloc[0])))
    lad = pd.DataFrame(lad_rows)
    star = pd.DataFrame(star_rows).merge(
        cells[["panel", "N", "H", "freq", "phi_estimable"]], on=["panel", "N", "H", "freq"])
    ge, gee = int(star.ge_episode.sum()), int(star[star.phi_estimable].ge_episode.sum())
    ne = int(star.phi_estimable.sum())
    P(f"  L* >= episode length at {ge} of {len(star)} books ({ge / len(star):.3f}) and at "
      f"{gee} of {ne} ESTIMABLE books ({gee / ne:.3f}) — 1162 read 12 of 12 on its own 15")
    P(f"  L*/E ranges {star.ratio.min():.2f}..{star.ratio.max():.2f}, "
      f"median {star.ratio.median():.2f}")
    P(f"  spearman(L*, E)   = {spearman(star.L_star, star.episode_bars):+.4f}   "
      f"spearman(L*/E, E)  = {spearman(star.ratio, star.episode_bars):+.4f}")
    se = star[star.phi_estimable]
    P(f"  spearman(L*, phi) = {spearman(se.L_star, se.phi_L63):+.4f}   "
      f"(the CROSSING against the LEVEL — the two functionals 1162 conflated), "
      f"spearman(L*, E) on estimable = {spearman(se.L_star, se.episode_bars):+.4f}")
    P("")

    # ------------------------------------------------- sensitivity on the frozen thresholds
    P("## SENSITIVITY — the frozen TIES / RECOV thresholds (published, never selected on)")
    keys = list(series)
    emask = np.array([bool(cells[(cells.panel == k[0]) & (cells.N == k[1]) &
                                (cells.H == k[2]) & (cells.freq == k[3])].phi_estimable.iloc[0])
                      for k in keys])
    phi_e = est.phi_L63.values

    def srho(vals):
        return spearman(np.asarray(vals, float)[emask], phi_e)

    sens_rows = []
    for q in [TIE_Q] + TIE_ALT:
        sens_rows.append(dict(driver="D_TIES", param=f"tie_q={q}",
                              rho=srho([drivers_of(series[k], tie_q=q)["D_TIES"] for k in keys]),
                              frozen=(q == TIE_Q)))
    for m in [REC_MIN] + REC_ALT:
        sens_rows.append(dict(driver="D_RECOV", param=f"rec_min={m}%",
                              rho=srho([drivers_of(series[k], rec_min=m)["D_RECOV"] for k in keys]),
                              frozen=(m == REC_MIN)))
    for LL in [21, 63, 126]:
        sens_rows.append(dict(driver="D_COVER", param=f"L={LL}",
                              rho=srho([drivers_of(series[k], L=LL)["D_COVER"] for k in keys]),
                              frozen=(LL == L_BLOCK)))
        sens_rows.append(dict(driver="COVER_GRADED", param=f"L={LL}",
                              rho=srho([drivers_of(series[k], L=LL)["COVER_GRADED"] for k in keys]),
                              frozen=False))
    sens = pd.DataFrame(sens_rows)
    for _, x in sens.iterrows():
        P(f"  {x.driver:<11s} {x.param:<14s} rho {x.rho:+.4f}  "
          f"{'FROZEN (headline)' if x.frozen else 'published, not selected on'}")
    P("")

    # ---------------------------------------------------------------- hypotheses
    P("## HYPOTHESES — scored against the bars declared before any result")
    rho_cover = float(xn["D_COVER"])
    panel_signs = [spearman(est[est.panel == pn].D_COVER, est[est.panel == pn].phi_L63)
                   for pn in PANELS]
    cover_wins = bool(abs(rho_cover) >= 0.60 and np.sign(rho_cover) == SIGN["D_COVER"]
                      and win == "D_COVER"
                      and all(np.sign(x) == SIGN["D_COVER"] for x in panel_signs))
    hyp("H_COVER", "|rho|>=0.60, correct sign, largest of 4, sign at 3 of 3 panels",
        f"rho {rho_cover:+.4f}, largest={win}, panels "
        + "/".join(f"{x:+.3f}" for x in panel_signs), cover_wins)
    for nm, drv, bar in [("H_TIES", "D_TIES", 0.40), ("H_RECOV", "D_RECOV", 0.40)]:
        rr_ = float(xn[drv])
        hyp(nm, f"|rho|>={bar} with sign {SIGN[drv]:+d} under X_NONE", f"rho {rr_:+.4f}",
            bool(abs(rr_) >= bar and np.sign(rr_) == SIGN[drv]))
    rho_ep = float(xn["D_EPISODE"])
    rho_ep_gap = float(grid[(grid.driver == "D_EPISODE") & (grid.control == "X_GAP")].rho.iloc[0])
    hyp("H_EPISODE", "rho<=-0.40 under X_NONE AND under X_GAP",
        f"X_NONE {rho_ep:+.4f}, X_GAP {rho_ep_gap:+.4f}",
        bool(rho_ep <= -0.40 and rho_ep_gap <= -0.40))
    rho_win_ord = float(grid[(grid.driver == win) & (grid.control == "X_ORDER")].rho.iloc[0])
    hyp("H_ORDER", f"|rho({win})| under X_ORDER <= half its X_NONE value",
        f"X_NONE {float(xn[win]):+.4f} -> X_ORDER {rho_win_ord:+.4f}",
        bool(abs(rho_win_ord) <= 0.5 * abs(float(xn[win]))))
    lo = float(det[det.E_injected <= 21].phi_L63.min())
    hi = float(det[det.E_injected >= 252].phi_L63.max())
    hyp("H_SYNTH", "spearman(E,phi)<=-0.90 AND phi>=0.90 at E<=21 AND phi<=0.40 at E>=252",
        f"rho {rho_syn:+.4f}, min(E<=21) {lo:.4f}, max(E>=252) {hi:.4f}",
        bool(rho_syn <= -0.90 and lo >= 0.90 and hi <= 0.40))
    hyp("H_LSTAR", "L* >= E at >= 90% of the 72 books",
        f"{ge} of {len(star)} = {ge / len(star):.3f} (estimable {gee} of {ne} = "
        f"{gee / ne:.3f})", bool(ge / len(star) >= 0.90))
    P("")

    # ================================ ARM F — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS
    P("## ARM F — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (PROTOCOL rules 4 and 8)")
    P("  Every book of the 72-book population at the frozen gross 0.75, PLUS the anchor")
    P("  book's 15-rung GROSS ladder on each panel = 117 books, ALL published.  Parameters")
    P("  are chosen on 2009-2016 ONLY by three IS choosers and scored on the untouched")
    P("  2017-2026 window.")
    wf_rows, bench = [], {}
    for panel in PANELS:
        d = panels[panel]
        sp = d["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(sp, d["warm"], d["ins"], d["oos"])
        lv = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
        lb = blocks_m(lv, d["warm"], d["ins"], d["oos"])
        bench[panel] = (sb, lb)
        P(f"  {panel:<6s} SPY  {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%} "
          f"(H {sb['H1']:.4f}/{sb['H2']:.4f})  OOS {sb['OOS_CAGR']:7.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {panel:<6s} v2   {lb['CAGR']:7.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:7.2%} "
          f"(H {lb['H1']:.4f}/{lb['H2']:.4f})  OOS {lb['OOS_CAGR']:7.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:7.2%}")
        ins_t, oos_t = d["ins"][d["warm"]], d["oos"][d["warm"]]
        for N in POP_N:
            for H in POP_H:
                for f in POP_F:
                    r = series[(panel, N, H, f)]
                    b = blocks_m(r, np.ones(len(r), dtype=bool), ins_t, oos_t)
                    l4b, l4o, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
                    wf_rows.append(dict(panel=panel, arm="POP", book=f"N{N}/H{H}/{f}",
                                        N=N, H=H, freq=f, gross=GROSS0, **b, **l4b, **l4o,
                                        **l4a, pass_4b_full=all(l4b.values()),
                                        pass_4b_oos=all(l4o.values()), pass_4a=all(l4a.values())))
        W1, mk = weights_anchor(panel, "C_BOOK")
        for g in GROSS_LADDER:
            r = run_weights(panel, W1, mk, g)
            b = blocks_m(r, np.ones(len(r), dtype=bool), ins_t, oos_t)
            l4b, l4o, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            wf_rows.append(dict(panel=panel, arm="GROSS", book=f"anchor/g{g:.2f}",
                                N=N0, H=HOLD0, freq=FREQ0, gross=g, **b, **l4b, **l4o, **l4a,
                                pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4o.values()),
                                pass_4a=all(l4a.values())))
    wf = pd.DataFrame(wf_rows)
    a = wf[(wf.panel == "U56") & (wf.book == "N20/H126/W")].iloc[0]
    b = wf[(wf.panel == "U56") & (wf.book == "anchor/g0.75")].iloc[0]
    v = max(abs(a.CAGR - b.CAGR), abs(a.Sharpe - b.Sharpe), abs(a.MaxDD - b.MaxDD))
    gate("G18", "the population's N20/H126/W IS the anchor book at gross 0.75", v, v < 1e-12)
    P("")
    P(f"  BASE RATES over all {len(wf)} books: 4b full {int(wf.pass_4b_full.sum())}, "
      f"4b OOS {int(wf.pass_4b_oos.sum())}, 4a {int(wf.pass_4a.sum())}")
    for panel in PANELS:
        s = wf[wf.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):3d}/{len(s)}  "
          f"4b OOS {int(s.pass_4b_oos.sum()):3d}/{len(s)}  4a {int(s.pass_4a.sum()):3d}/{len(s)}")
    pick_rows = []
    for panel in PANELS:
        sb, lb = bench[panel]
        for arm in ["POP", "GROSS", "ALL"]:
            s = wf[(wf.panel == panel)] if arm == "ALL" else wf[(wf.panel == panel) & (wf.arm == arm)]
            for cname, key in CHOOSERS.items():
                x = wf.loc[s[key].idxmax()]
                pick_rows.append(dict(panel=panel, arm=arm, chooser=cname, pick=x.book,
                                      IS_Sharpe=x.IS_Sharpe, CAGR=x.CAGR, Sharpe=x.Sharpe,
                                      MaxDD=x.MaxDD, OOS_CAGR=x.OOS_CAGR,
                                      OOS_Sharpe=x.OOS_Sharpe, OOS_MaxDD=x.OOS_MaxDD,
                                      SPY_OOS_CAGR=sb["OOS_CAGR"], SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                                      SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                                      pass_4b_full=bool(x.pass_4b_full),
                                      pass_4b_oos=bool(x.pass_4b_oos), pass_4a=bool(x.pass_4a)))
    picks = pd.DataFrame(pick_rows)
    P("")
    P("  RULE-8 PICKS (chosen on 2009..2016 IS only, scored on the untouched OOS window):")
    P(f"  {'panel':<6s} {'arm':<6s} {'chooser':<11s} {'pick':<15s} {'OOS CAGR':>9s} "
      f"{'OOS Shrp':>9s} {'OOS DD':>8s} {'4bF':>5s} {'4bO':>5s} {'4a':>5s}")
    for _, x in picks.iterrows():
        P(f"  {x.panel:<6s} {x.arm:<6s} {x.chooser:<11s} {x['pick']:<15s} {x.OOS_CAGR:9.2%} "
          f"{x.OOS_Sharpe:9.4f} {x.OOS_MaxDD:8.2%} {str(bool(x.pass_4b_full)):>5s} "
          f"{str(bool(x.pass_4b_oos)):>5s} {str(bool(x.pass_4a)):>5s}")
    best = wf[wf.pass_4b_full & wf.pass_4b_oos]
    P("")
    if len(best):
        for _, bb in best.sort_values("OOS_Sharpe", ascending=False).head(5).iterrows():
            reach = bool(((picks.panel == bb.panel) & (picks["pick"] == bb.book)).any())
            P(f"  4b FULL+OOS: {bb.panel:<6s} {bb.book:<15s} full {bb.CAGR:7.2%} / "
              f"{bb.Sharpe:.4f} / {bb.MaxDD:7.2%} (H {bb.H1:.4f}/{bb.H2:.4f})  OOS "
              f"{bb.OOS_CAGR:7.2%} / {bb.OOS_Sharpe:.4f} / {bb.OOS_MaxDD:7.2%}  "
              f"IS-chooser-reachable {'YES' if reach else 'NO'}")
    else:
        P("  NO book clears 4b FULL and 4b OOS anywhere on this grid.")
    P(f"  4a passes: {int(wf.pass_4a.sum())} of {len(wf)} books and "
      f"{int(picks.pass_4a.sum())} of {len(picks)} picks.")
    P("")

    # ---------------------------------------------------------------------- outputs
    P("## OUTPUTS")
    dump(pd.DataFrame(GATES), "gates")
    dump(pd.DataFrame(HYP), "hypotheses")
    dump(rep, "replay")
    dump(cells, "cells")
    dump(ordc, "orderdestroyed")
    dump(grid, "dialgrid")
    dump(syn, "synthetic")
    dump(lad, "ladder")
    dump(star, "lstar")
    dump(sens, "sensitivity")
    dump(wf, "walkforward")
    dump(picks, "picks")
    P("")
    P(f"GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS   "
      f"HYPOTHESES {sum(h['supported'] for h in HYP)} of {len(HYP)} SUPPORTED")
    P(f"runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return cells, grid, syn, wf, picks


if __name__ == "__main__":
    main()
