#!/usr/bin/env python3
"""Idea 800 (lane C, 2026-09-12) - is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law.

QUESTION
--------
Idea 569/571/796's machinery matches two arms - BONLY (names sourced from the broad large-cap
panel) and SONLY (names from the sub-$2B panel) - at a target LEVEL L of a per-name characteristic
by a Gaussian kernel draw of k=36 names without replacement.  The MATCH RESIDUAL is what is left
over: |achieved_B - achieved_S| at the rung.  Everything the record calls a "matched-level gap"
is only as trustworthy as that residual.

Idea 796 tried to shrink it with the obvious dial and FAILED: narrowing the bandwidth made the
match WORSE (|resid| 0.0027 -> 0.0129 -> 0.0147 at BW 0.500/0.250/0.125).  What did move it, with
no tuning at all, was the PANEL: idea 571's 430-name small panel read 0.0133 where today's 663-name
panel reads 0.0027, a 5x improvement.  The queue's diagnosis is that the residual is a POOL DENSITY
law - specifically that it is governed by the THIN arm, min(n_BONLY, n_SONLY).

That diagnosis is not yet established, because idea 796's two vintages differ in THREE ways at once:
the small arm's size (428 -> 657 usable), the characteristic values themselves (re-estimated on a
different pool - momac's per-name value is a WITHIN-POOL cross-sectional rank autocorrelation, so it
moves when the pool moves), and therefore every rung LEVEL (the rungs are pooled quantiles).  And
the thin arm was 134 names in BOTH vintages, so idea 796's own 5x was produced by changing the FAT
arm - which is the opposite of what "governed by the thin arm" predicts.

This run isolates density.  The characteristic values, the rung levels and the bandwidth are FROZEN
at the full LIVE pool (per window), and the only thing that changes is HOW MANY names each arm may
draw from.  Then |resid| is measured as a function of pool size at fixed k, and the law is published
as an entitlement table any future matched-level claim can quote.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: pool size, k)
    1. N     in {36, 48, 64, 84, 110, 134}   the sub-sample size of each arm (134 = the full B arm)
    2. K     in {12, 24, 36}                 draw size; 36 = idea 569/571/796's value, the anchor
All 6 x 3 = 18 grid points are reported, for the law AND for both KEEP paths.

REPORTED-NEVER-SELECTED axes (nothing is picked on any of them):
    leg       SYM     n_B = n_S = N                     - the tuned axis; min(n_B,n_S) = N exactly
              ASYM_S  n_B = 134 (full), n_S = N'        - N' in NGRID + {200, 330, 500, 663}
              ASYM_B  n_S = 663 (full), n_B = N
              ANCHOR  both arms full, idea 796's own cell, drawn with its VERBATIM seed keys
              REEST   SYM pools with the characteristic, rungs and bandwidth RE-ESTIMATED on the
                      sub-sample (this is what idea 796's vintage change actually did)
    char      momac (the question), tpers (idea 571/796's reference control)
    rep       0..5, six deterministic sub-sample replicates per cell
    seed      0..5, the machinery's six draw seeds
    window    FULL, IS, OOS
    flavour   BONLY, SONLY (+ POOL in the book leg), gross {0.50,0.75,1.00}, cadence {W, M}

PRE-REGISTERED HYPOTHESES (written before any number in this file was read)
    H_LAW    : |resid| is a pool-size law - on the SYM leg at fixed k it is monotone DECREASING in
               N for momac on the anchor rung set, in every window.
    H_RATIO  : the governing variable is the DRAW FRACTION k/N, not N alone - a single pooled
               log-log fit of |resid| on k/N over all 18 cells has R2 >= 0.70 and a positive slope,
               and the three per-k curves collapse onto it.
    H_THIN   : the queue's own framing - |resid| is set by min(n_B, n_S).  Concretely, on ASYM_S
               past the thin arm's size (n_S > 134 with n_B = 134 fixed) |resid| is FLAT: the change
               from n_S = 134 to n_S = 663 is inside the replicate band (<= 1 sd of the replicate
               spread at n_S = 134).
    H_FAT    : the alternative that idea 796's own 5x actually suggests - raising the FAT arm alone
               still moves |resid| materially (> 1 replicate sd).  H_FAT = not H_THIN.
    H_PARENT : the ANCHOR leg reproduces idea 796's committed LIVE/momac/BW0.500/Q5 residual
               0.0027 and its tpers 0.0011 to 1e-4 (same data, same estimator, verbatim seed keys).
    H_REEST  : idea 796's 5x was NOT density - the REEST leg (re-estimating the characteristic on
               the sub-sample, as its vintage change did) moves |resid| by more, at the same N, than
               the frozen-characteristic SYM leg does.
    H_ENTITLE: the payoff.  At the record's own working cell (n_B = 134, k = 36) the entitled
               residual is LARGER than the tightest residuals the record has published (tpers
               0.0017, volpers 0.0007), i.e. those readings are lucky cells, not tight matches.

GATES (run and printed before any new number is read)
    G0 determinism : every draw rebuilt twice gives identical name sets.                     bar 0
    G1 chars       : this file's fast panel-characteristic estimator vs idea 796's verbatim
                     panel_chars() on 12 panels.                                          bar 1e-12
    G2 identity    : fast_backtest vs engine.backtest on one book per real panel.           bar 1e-9
    G3 ANCHOR      : the ANCHOR leg vs idea 796's committed .summary.csv residuals.         bar 1e-4

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: the whole law is rebuilt inside each window (characteristics, rungs,
       bandwidth and draws all re-estimated on that window's bars only).  The exponent of the
       k/N fit is chosen on IS and used to PREDICT the OOS residual at every cell; the OOS
       prediction error is reported, as is whether H_LAW / H_THIN hold in each window separately.
    WF-B on a BOOK: the ladder read as a trading instruction - "at matched level the panel of
       origin does not matter, hold whichever flavour is available".  At every one of the 18 tuned
       cells, (flavour, level, seed, gross, cadence) is chosen by IS Sharpe ALONE, then OOS
       CAGR/Sharpe/MaxDD are read ONCE against live RULES v2 (on the drawn panel AND on U56) and
       against SPY.  A global pick over all 18 cells is reported beside the per-cell picks.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY book
    and the counts reported per cell.  Stated up front: every panel here is a kernel-weighted seeded
    draw from a randomly sub-sampled pool, i.e. two layers of randomisation away from anything a
    person could trade, so a 4b pass here is a diagnostic and NONE is claimed as a capital
    candidate.

SURVIVORSHIP: the pool is the broad panel (current constituents of universe_broad.json) plus the
    sub-$2B panel (current constituents of its screen, every ticker with max_1d_move >= 1.0 in
    data/small_meta.csv dropped first, per PROTOCOL).  Dead small names are absent.  For THIS
    question the bias is second-order: the residual is a matching diagnostic, not a return, and it
    is measured between two arms that are both drawn from survivor pools.  Any absolute residual
    quoted here is therefore an estimate for a survivor pool of that size - said again beside the
    entitlement table.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and idea 796's committed
artefacts; modifies nothing but its own outputs:
    .law.csv .rungs.csv .commonrung.csv .fits.csv .reest.csv .entitle.csv .anchres.csv
    .grid.csv .keeppaths.csv .walkforward.csv .summary.csv .console.txt

ONE CONTROL ADDED AFTER A PILOT RUN, STATED PLAINLY: the pilot showed that the number of
OVERLAPPING rungs itself grows with N (a bigger pool has a wider k-name reach band, so it can
address harder rungs).  The pre-registered all-rung mean is therefore taken over a different rung
set at each N.  A COMMON-RUNG ladder - the same rungs at every N on a curve - is reported beside it.
The pre-registered hypotheses are judged as written, on the all-rung mean; the common-rung ladder
is published as the mechanism, not as a second bite at the verdict.

TWO MORE READS ADDED AFTER THE PILOT, BOTH LABELLED AS SUCH IN THE OUTPUT.  Neither adds a dial,
a cell or a data series - each re-reads cells this file already measures:
  * a THIN-ARM test symmetric to the fat-arm test H_THIN specifies (n_B moves, n_S full).  H_THIN
    as written only says the residual is FLAT past the thin arm; it never states the other half of
    its own claim, that moving the THIN arm moves the residual.  Both halves are now reported.
  * the ANCHOR'S OWN SAMPLING DISTRIBUTION.  At n_S >= the usable small arm the "sub-sample" is
    the whole pool, so those replicates differ only in the draw's seed key - a resampling
    distribution of idea 796's committed statistic on idea 796's own data.  40 further re-draws of
    that one cell are run so the committed value's position is a RANK in a real distribution rather
    than an sd distance estimated off six points.  This costs ~1 minute and adds no dial: the pool,
    the characteristic, the rungs, the bandwidth, k and the number of seeds are all unchanged, and
    the pre-registered hypotheses are not re-judged on it.
Run with --smoke for a reduced grid (development only; the committed numbers are the full run).
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
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
SMOKE = "--smoke" in sys.argv

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
ARMS = ["EWall", "MA-RS"]
MA_WIN = 200
MOM_LAG, MOM_LOOK = 21, 252
AC_LAG = 21
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"             # idea 796's last bar, kept so G3 can be exact
BW = 0.500                            # idea 569/571/796's anchor bandwidth - NOT tuned here
LEVEL_Q5 = [0.10, 0.30, 0.50, 0.70, 0.90]      # idea 571's pre-registered rung set
SEEDS = [0, 1, 2, 3, 4, 5]
REPS = [0, 1, 2, 3, 4, 5]
BOOK_REPS = [0, 1]                    # the book leg is 12x costlier per draw; 2 replicates of 6
FLAVOURS = ["BONLY", "SONLY"]
BOOK_FLAVOURS = ["POOL", "BONLY", "SONLY"]
CHARS = ["momac", "tpers"]
NGRID = [36, 48, 64, 84, 110, 134]              # TUNED 1
KGRID = [12, 24, 36]                            # TUNED 2
K_ANCHOR = 36
NS_EXTRA = [200, 330, 500, 663]                 # ASYM_S reach past the thin arm
WINDOWS = ["FULL", "IS", "OOS"]
ANCH_R = list(range(100, 140))        # 40 pure re-draws of idea 796's own anchor cell
PARENT796 = OUT / "2026-09-11_is-momac-s-0.0549-MATCHED-LEVEL-GAP-real-or-a-MATCHING-RESIDUAL_cloud"
P796_RESID = {"momac": 0.0027111023034787074, "tpers": 0.0010633}   # its LIVE BW0.500/Q5 cells
TPERS571_RESID = 0.0017               # the record's tightest published residual (idea 571)
VOLPERS798_RESID = 0.0007             # idea 798's, the tightest on this machinery
TOL_BT = 1e-9
TOL_CH = 1e-12
TOL_ANCHOR = 1e-4

if SMOKE:
    NGRID = [36, 84, 134]
    KGRID = [12, 36]
    REPS = [0, 1]
    BOOK_REPS = [0]
    NS_EXTRA = [330, 663]
    WINDOWS = ["FULL", "IS", "OOS"]
    ANCH_R = list(range(100, 106))

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner (idea 796)
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def make_books(px, tradable, g):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    e = e > 0
    ma = (px > px.rolling(MA_WIN).mean()) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------ per-NAME characteristics (idea 571/796, verbatim)
def _flip_persistence(state, valid):
    st = state.where(valid)
    flips = st.astype(float).diff().abs().where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    return (1.0 - flips.sum() / denom).astype(float)


def pers_name_chars(pool):
    """Idea 571/796's tpers and momac, verbatim.  momac's rank is cross-sectional WITHIN the pool,
    so it is a property of the pool as well as of the name."""
    ma = pool.rolling(MA_WIN).mean()
    v_ma = pool.notna() & ma.notna()
    tpers = _flip_persistence(pool > ma, v_ma)
    mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    v_mom = pool.notna() & mom.notna()
    ac = {}
    for c in pool.columns:
        s = rk[c].where(v_mom[c]).dropna()
        ac[c] = float(s.corr(s.shift(AC_LAG))) if len(s) > 3 * AC_LAG else np.nan
    return pd.DataFrame(dict(tpers=tpers, momac=pd.Series(ac, dtype=float)))


def panel_chars_ref(px, tradable):
    """Idea 796's panel-level estimator, verbatim - the reference G1 gates against."""
    cols = [c for c in px.columns if c in tradable]
    sub = px[cols]
    r = sub.pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    ma = sub.rolling(MA_WIN).mean()
    v_ma = sub.notna() & ma.notna()
    tpers = float(_flip_persistence(sub > ma, v_ma).mean())
    mom = sub.shift(MOM_LAG) / sub.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    v_mom = sub.notna() & mom.notna()
    acs = []
    for c in sub.columns:
        s = rk[c].where(v_mom[c]).dropna()
        if len(s) > 3 * AC_LAG:
            acs.append(float(s.corr(s.shift(AC_LAG))))
    return dict(cvol=vol, tpers=tpers, momac=float(np.nanmean(acs)) if acs else np.nan)


class FastChars:
    """Same numbers as panel_chars_ref, ~11x cheaper.

    tpers and cvol are PER-NAME quantities (each column's own 200d MA and own vol), so the panel
    value is the mean of pre-computed per-name values - exactly, not approximately.  momac is NOT:
    its rank is cross-sectional inside the panel, so it is recomputed per panel, with the
    per-name autocorrelation done in numpy instead of a pandas loop.
    """

    def __init__(self, pool):
        self.cols = list(pool.columns)
        self.ci = {c: i for i, c in enumerate(self.cols)}
        ma = pool.rolling(MA_WIN).mean()
        v_ma = pool.notna() & ma.notna()
        self.tpers_name = _flip_persistence(pool > ma, v_ma).to_numpy(float)
        self.vol_name = (pool.pct_change().std() * np.sqrt(252)).to_numpy(float)
        self.mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
        self.valid = (pool.notna() & self.mom.notna()).to_numpy()

    def panel(self, names):
        j = np.array([self.ci[c] for c in names])
        rk = self.mom.iloc[:, j].rank(axis=1, pct=True).to_numpy()
        rk = np.where(self.valid[:, j], rk, np.nan)
        acs = []
        for q in range(rk.shape[1]):
            s = rk[:, q]
            s = s[~np.isnan(s)]
            if len(s) > 3 * AC_LAG:
                x, y = s[AC_LAG:], s[:-AC_LAG]
                xc, yc = x - x.mean(), y - y.mean()
                den = np.sqrt((xc * xc).sum() * (yc * yc).sum())
                acs.append(float((xc * yc).sum() / den) if den > 0 else np.nan)
        return dict(cvol=float(np.nanmean(self.vol_name[j])),
                    tpers=float(np.nanmean(self.tpers_name[j])),
                    momac=float(np.nanmean(acs)) if acs else np.nan)


# ------------------------------------------------------------------------------- the draw
def reach(x, k):
    v = np.sort(np.asarray(x, float))
    return float(v[:k].mean()), float(v[-k:].mean())


def kdraw(names, x, L, h, k, seed_key):
    """Idea 569/571/796's kernel-weighted draw of k names without replacement."""
    rng = np.random.default_rng(zlib.crc32(seed_key.encode()) % (2 ** 32))
    w = np.exp(-0.5 * ((x - L) / h) ** 2)
    w = w / w.sum()
    return sorted(rng.choice(names, size=k, replace=False, p=w).tolist())


def subsample(names, n, key):
    if n >= len(names):
        return sorted(names)
    rng = np.random.default_rng(zlib.crc32(key.encode()) % (2 ** 32))
    return sorted(rng.choice(np.array(names), size=n, replace=False).tolist())


def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 800 - is the kernel draw's MATCH RESIDUAL a POOL-SIZE law?  Freeze the characteristic,")
    P("#            the rungs and the bandwidth; vary only how many names each arm may draw from.")
    P("=" * 118)
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}, "
      f"sample truncated at {PARENT_END} (idea 796's last bar, so G3 can be exact)")
    P(f"# TUNED (2): N in {NGRID} x K in {KGRID} = {len(NGRID)*len(KGRID)} cells, all reported.")
    P("# REPORTED-NOT-SELECTED: leg (SYM/ASYM_S/ASYM_B/ANCHOR/REEST), char (momac + tpers control),")
    P(f"#   rep 0..{REPS[-1]}, seed 0..{SEEDS[-1]}, window (FULL/IS/OOS), flavour, gross, cadence.")
    P(f"# BW fixed at {BW:.3f} and rungs at idea 571's Q5 {LEVEL_Q5} - idea 796 already tuned those.")
    if SMOKE:
        P("# *** SMOKE RUN - reduced grid, NOT the committed numbers ***")
    P("")
    P("PRE-REGISTERED: H_LAW (|resid| monotone decreasing in N at fixed k), H_RATIO (pooled log-log")
    P("  fit on k/N has R2 >= 0.70, positive slope), H_THIN (ASYM_S flat past n_S=134, inside 1")
    P("  replicate sd), H_FAT (= not H_THIN), H_PARENT (ANCHOR reproduces idea 796 to 1e-4),")
    P("  H_REEST (re-estimating the char on the sub-sample moves |resid| MORE than density does),")
    P(f"  H_ENTITLE (entitled |resid| at n=134/k=36 exceeds the record's tightest published")
    P(f"  {TPERS571_RESID:.4f} / {VOLPERS798_RESID:.4f}).")
    P("")

    # ------------------------------------------------------------------ panels and the pool
    px56 = load_universe().dropna(how="all").ffill().loc[:PARENT_END]
    px136 = load_universe(broad=True).dropna(how="all").ffill().loc[:PARENT_END]
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END]
    ix = px136.index.intersection(pxs.index)
    bn_all = sorted([c for c in px136.columns if c != "SPY"])
    sn_all = sorted(s_stk)
    POOL = pd.concat([px136.loc[ix, bn_all], pxs.loc[ix, sn_all]], axis=1).ffill()
    SPY = px136.loc[ix, "SPY"]
    P(f"POOL: {ix.min().date()}..{ix.max().date()} ({len(ix)} bars); B {len(bn_all)} + "
      f"SMALL {len(sn_all)} = {POOL.shape[1]} names; {len(bad)} small tickers dropped "
      f"(max_1d_move >= 1.0, per PROTOCOL)")
    P("SURVIVORSHIP: both arms are CURRENT constituents; dead small names are absent.  The residual")
    P("  is a matching diagnostic, not a return, and both arms are drawn from survivor pools, so any")
    P("  absolute residual here is an estimate FOR A SURVIVOR POOL OF THAT SIZE.")
    P("")

    # ------------------------------------------------------------------ per-window frozen setup
    W: dict[str, dict] = {}
    for w in WINDOWS:
        pl = POOL if w == "FULL" else (POOL.loc[:IS_END] if w == "IS" else POOL.loc[OOS_START:])
        nc = pers_name_chars(pl)
        fc = FastChars(pl)
        d = dict(pool=pl, nc=nc, fc=fc, spy=SPY.reindex(pl.index))
        d["B"] = {c: sorted([n for n in bn_all if pd.notna(nc[c].get(n, np.nan))]) for c in CHARS}
        d["S"] = {c: sorted([n for n in sn_all if pd.notna(nc[c].get(n, np.nan))]) for c in CHARS}
        d["sd"] = {c: float(nc[c].std()) for c in CHARS}
        d["h"] = {c: BW * d["sd"][c] for c in CHARS}
        d["lv"] = {c: [round(float(nc[c].quantile(q)), 6) for q in LEVEL_Q5] for c in CHARS}
        W[w] = d
        P(f"WINDOW {w:4s}: {pl.index.min().date()}..{pl.index.max().date()} ({len(pl)} bars)")
        for c in CHARS:
            P(f"   {c:6s} usable B {len(d['B'][c]):3d} / S {len(d['S'][c]):3d}; sd "
              f"{d['sd'][c]:.4f}; h {d['h'][c]:.4f}; rungs " +
              " ".join(f"{x:.4f}" for x in d["lv"][c]))
    P("   The characteristic, the rungs and the bandwidth are FROZEN at the full pool inside each")
    P("   window.  Sub-sampling changes ONLY which names an arm may draw from - that is what")
    P("   isolates density from the re-estimation idea 796's vintage change also performed.")
    P("")

    # ------------------------------------------------------------------------------ gates
    P("=" * 118)
    P("GATES (printed before any new number is read)")
    P("=" * 118)
    fc = W["FULL"]["fc"]
    nc = W["FULL"]["nc"]
    g1 = 0.0
    for t_ in range(12):
        nm = subsample(list(POOL.columns), 36, f"G1|{t_}")
        a = fc.panel(nm)
        b = panel_chars_ref(POOL[nm], set(nm))
        g1 = max(g1, max(abs(a[q] - b[q]) for q in ("cvol", "tpers", "momac")))
    P(f"G1 chars       : fast vs idea 796's panel_chars max |d| = {g1:.3e} (bar {TOL_CH:.0e}) -> "
      f"{'PASS' if g1 <= TOL_CH else 'FAIL'}")
    g2 = 0.0
    for nm_, px_ in (("U56", px56), ("B136", px136), (f"SMALL{len(sn_all)}", pxs)):
        tr = {c for c in px_.columns if c != "SPY"}
        wts = make_books(px_, tr, 0.75)["MA-RS"]
        g2 = max(g2, float((fast_backtest(px_, wts, COST, "W")["returns"]
                            - backtest(px_, wts, cost_bps=COST, freq="W")["returns"]).abs().max()))
    P(f"G2 identity    : fast_backtest vs engine.backtest max |dret| = {g2:.3e} "
      f"(bar {TOL_BT:.0e}) -> {'PASS' if g2 <= TOL_BT else 'FAIL'}")
    g0 = nd = 0
    for c in CHARS:
        for k in KGRID:
            for n in NGRID:
                for fl, base in (("BONLY", W["FULL"]["B"][c]), ("SONLY", W["FULL"]["S"][c])):
                    nmz = subsample(base, n, f"SUB|{fl}|{c}|FULL|{n}|0")
                    x = nc.loc[nmz, c].to_numpy()
                    key = f"CHAR|{c}|{W['FULL']['lv'][c][2]:.6f}|{fl}|0|FULL|n{n}|r0|k{k}"
                    a = kdraw(np.array(nmz), x, W["FULL"]["lv"][c][2], W["FULL"]["h"][c], k, key)
                    b = kdraw(np.array(nmz), x, W["FULL"]["lv"][c][2], W["FULL"]["h"][c], k, key)
                    nd += 1
                    g0 += 0 if a == b else 1
    P(f"G0 determinism : {g0} of {nd} draws differ on rebuild (bar 0) -> "
      f"{'PASS' if g0 == 0 else 'FAIL'}")
    P("")

    # ----------------------------------------------------------------------- the residual law
    P("=" * 118)
    P("THE LAW - |match residual| by pool size, at fixed k, frozen characteristic")
    P("=" * 118)

    def cell_resid(w, char, nB, nS, k, rep, leg, ncx=None, lvx=None, hx=None, verbatim=False):
        """mean over overlapping rungs of |mean_seed achieved_B - mean_seed achieved_S|.

        Returns (cell_row, per_rung_rows).  A cell with no overlapping rung is still returned,
        with abs_resid = NaN and n_overlap = 0, so every grid point appears in .law.csv.
        """
        d = W[w]
        ncu = d["nc"] if ncx is None else ncx
        lv = d["lv"][char] if lvx is None else lvx
        h = d["h"][char] if hx is None else hx
        pools = {}
        for fl, base, n in (("BONLY", d["B"][char], nB), ("SONLY", d["S"][char], nS)):
            nm = subsample(base, n, f"SUB|{fl}|{char}|{w}|{n}|{rep}")
            if ncx is not None:
                nm = [q for q in nm if pd.notna(ncu[char].get(q, np.nan))]
            pools[fl] = (np.array(nm), ncu.loc[nm, char].to_numpy(float))
        out, nov, rr_ = [], 0, []
        reaches = {}
        for fl in FLAVOURS:
            nm, x = pools[fl]
            reaches[fl] = reach(x, k) if len(nm) >= k else (np.nan, np.nan)
        for L in lv:
            ach = {}
            for fl in FLAVOURS:
                nm, x = pools[fl]
                if len(nm) < k:
                    ach[fl] = None
                    continue
                lo, hi = reaches[fl]
                if not (lo <= L <= hi):
                    ach[fl] = None
                    continue
                vals = []
                for sd in SEEDS:
                    key = (f"CHAR|{char}|{L:.6f}|{fl}|{sd}" if verbatim else
                           f"CHAR|{char}|{L:.6f}|{fl}|{sd}|{w}|n{len(nm)}|r{rep}|k{k}|{leg}")
                    vals.append(d["fc"].panel(kdraw(nm, x, L, h, k, key))[char])
                ach[fl] = float(np.mean(vals))
            if ach["BONLY"] is None or ach["SONLY"] is None:
                continue
            nov += 1
            out.append(dict(level=L, achieved_B=ach["BONLY"], achieved_S=ach["SONLY"],
                            resid=ach["BONLY"] - ach["SONLY"]))
            rr_.append(dict(leg=leg, window=w, char=char, k=k, n_B=nB, n_S=nS, n_min=min(nB, nS),
                            rep=rep, level=L, achieved_B=ach["BONLY"], achieved_S=ach["SONLY"],
                            resid=ach["BONLY"] - ach["SONLY"]))
        cell = dict(leg=leg, window=w, char=char, k=k, n_B=nB, n_S=nS, n_min=min(nB, nS), rep=rep,
                    n_overlap=nov, reach_lo_B=reaches["BONLY"][0], reach_hi_B=reaches["BONLY"][1],
                    reach_lo_S=reaches["SONLY"][0], reach_hi_S=reaches["SONLY"][1],
                    reach_w_B=reaches["BONLY"][1] - reaches["BONLY"][0],
                    reach_w_S=reaches["SONLY"][1] - reaches["SONLY"][0])
        if not out:
            cell.update(abs_resid=np.nan, mean_resid=np.nan, abs_resid_sd_units=np.nan,
                        worst_rung=np.nan)
            return cell, rr_
        r = pd.DataFrame(out)
        cell.update(abs_resid=float(r.resid.abs().mean()), mean_resid=float(r.resid.mean()),
                    abs_resid_sd_units=float(r.resid.abs().mean()) / d["sd"][char],
                    worst_rung=float(r.resid.abs().max()))
        return cell, rr_

    rows, rungrows = [], []
    specs = []
    for w in WINDOWS:
        for char in CHARS:
            nBf, nSf = len(W[w]["B"][char]), len(W[w]["S"][char])
            for k in KGRID:
                for rep in REPS:
                    for n in NGRID:
                        specs.append((w, char, n, n, k, rep, "SYM"))
                    for n in NGRID + NS_EXTRA:
                        specs.append((w, char, nBf, min(n, nSf), k, rep, "ASYM_S"))
                    for n in NGRID:
                        # capped at the usable big arm: a spec above nBf would be the FULL arm
                        # wearing a bigger label, which is not a measurement of n_B at all
                        specs.append((w, char, min(n, nBf), nSf, k, rep, "ASYM_B"))
                specs.append((w, char, nBf, nSf, K_ANCHOR, -1, "ANCHOR"))
    seen = set()
    specs = [s for s in specs if not (s in seen or seen.add(s))]
    P(f"  {len(specs)} (leg, window, char, n_B, n_S, k, rep) cells x up to {len(LEVEL_Q5)} rungs x "
      f"{len(SEEDS)} seeds x 2 arms")
    for i, (w, char, nB, nS, k, rep, leg) in enumerate(specs):
        r, rr = cell_resid(w, char, nB, nS, k, rep, leg, verbatim=(leg == "ANCHOR"))
        rows.append(r)
        rungrows.extend(rr)
        if (i + 1) % 400 == 0:
            P(f"    {i+1}/{len(specs)} cells ({time.time()-t0:.0f}s)")
    LAW = pd.DataFrame(rows)
    RUNG = pd.DataFrame(rungrows)
    LAW.to_csv(f"{OUT/STAMP}.law.csv", index=False)
    RUNG.to_csv(f"{OUT/STAMP}.rungs.csv", index=False)
    nempty = int(LAW.abs_resid.isna().sum())
    P(f"  {len(LAW)} cells measured, {len(RUNG)} rung readings ({time.time()-t0:.0f}s)")
    P(f"  {nempty} cells have NO overlapping rung (both arms' k-name reach bands never bracket a")
    P("  rung): these are reported as NaN, never dropped.  At N = k the reach band collapses to a")
    P("  point (the draw must take the whole pool), which is what empties those cells.")
    for _, r in LAW[LAW.abs_resid.isna()].groupby(["leg", "char", "k", "n_min"]).size(
    ).reset_index(name="cells").iterrows():
        P(f"    empty: {r.leg:7s} {r.char:6s} k {int(r.k):2d} N {int(r.n_min):4d} "
          f"({int(r.cells)} window/rep cells)")
    LAW = LAW.dropna(subset=["abs_resid"])
    P("")

    # ------------------------------------------------------------------ G3 anchor reproduction
    P("=" * 118)
    P("G3 ANCHOR - this run's full-pool cell vs idea 796's committed LIVE / BW0.500 / Q5 residual")
    P("=" * 118)
    g3 = 0.0
    for char in CHARS:
        a = LAW[(LAW.leg == "ANCHOR") & (LAW.window == "FULL") & (LAW.char == char)]
        if a.empty:
            continue
        got = float(a.abs_resid.iloc[0])
        want = P796_RESID[char]
        g3 = max(g3, abs(got - want))
        P(f"  {char:6s} n_B {int(a.n_B.iloc[0])} n_S {int(a.n_S.iloc[0])} k {K_ANCHOR} -> "
          f"|resid| {got:.6f}  vs idea 796's {want:.6f}  |d| {abs(got-want):.2e}")
    P(f"G3 ANCHOR      : max |d| {g3:.2e} (bar {TOL_ANCHOR:.0e}) -> "
      f"{'PASS' if g3 <= TOL_ANCHOR else 'FAIL'}")
    P(f"H_PARENT -> {'PASS' if g3 <= TOL_ANCHOR else 'FAIL'}")
    P("")

    # ----------------------------------------------------------------------------- SYM ladder
    def agg(df, keys):
        return df.groupby(keys).agg(cells=("abs_resid", "size"), resid=("abs_resid", "mean"),
                                    sd=("abs_resid", "std"), worst=("worst_rung", "mean"),
                                    sdu=("abs_resid_sd_units", "mean"),
                                    ov=("n_overlap", "mean")).reset_index()

    SY = agg(LAW[LAW.leg == "SYM"], ["window", "char", "k", "n_min"])
    P("=" * 118)
    P("SYM leg - the tuned grid.  n_B = n_S = N, so min(n_B,n_S) = N.  All 18 cells per")
    P(f"          (window, char); mean over {len(REPS)} sub-sample replicates, sd across them.")
    P("=" * 118)
    P(f"  {'win':4s} {'char':6s} {'k':>3s} {'N':>4s} {'k/N':>6s} {'|resid|':>9s} {'sd_rep':>9s} "
      f"{'worst':>9s} {'/sd(ch)':>8s} {'rungs':>6s}")
    for _, r in SY.sort_values(["window", "char", "k", "n_min"]).iterrows():
        P(f"  {r.window:4s} {r.char:6s} {int(r.k):3d} {int(r.n_min):4d} {r.k/r.n_min:6.3f} "
          f"{r.resid:9.5f} {r.sd:9.5f} {r.worst:9.5f} {r.sdu:8.4f} {r.ov:6.2f}")
    P("")

    mono = {}
    for (w, char, k), d in SY.groupby(["window", "char", "k"]):
        v = d.sort_values("n_min").resid.to_numpy()
        mono[(w, char, k)] = bool(np.all(np.diff(v) <= 0))
    nm_ok = sum(1 for kk, v in mono.items() if v)
    mo_ma = sum(1 for kk, v in mono.items() if v and kk[1] == "momac")
    tot_ma = sum(1 for kk in mono if kk[1] == "momac")
    P(f"  H_LAW - |resid| monotone decreasing in N: {nm_ok}/{len(mono)} (window,char,k) curves; "
      f"momac alone {mo_ma}/{tot_ma}")
    for kk in sorted(mono):
        if not mono[kk]:
            d = SY[(SY.window == kk[0]) & (SY.char == kk[1]) & (SY.k == kk[2])].sort_values("n_min")
            P(f"    NOT monotone {kk}: " + " ".join(f"{x:.5f}" for x in d.resid))
    endpt = []
    for (w, char, k), d in SY.groupby(["window", "char", "k"]):
        d = d.sort_values("n_min")
        endpt.append(dict(window=w, char=char, k=k, lo_N=int(d.n_min.iloc[0]),
                          hi_N=int(d.n_min.iloc[-1]), lo=float(d.resid.iloc[0]),
                          hi=float(d.resid.iloc[-1]),
                          ratio=float(d.resid.iloc[0] / d.resid.iloc[-1])
                          if d.resid.iloc[-1] > 0 else np.nan))
    EP = pd.DataFrame(endpt)
    P("  endpoint ratio |resid|(N=min) / |resid|(N=max) per curve:")
    for _, r in EP.sort_values(["window", "char", "k"]).iterrows():
        P(f"    {r.window:4s} {r.char:6s} k {int(r.k):2d}: {r.lo:.5f} (N={r.lo_N}) -> "
          f"{r.hi:.5f} (N={r.hi_N}) = {r.ratio:6.2f}x")
    h_law = bool(mo_ma == tot_ma)
    P(f"  H_LAW -> {'PASS' if h_law else 'FAIL'} (judged as pre-registered: momac, the question")
    P("    variable, mean over EVERY overlapping rung)")
    P("")

    # ---------------------------------------------------- REACH, and the common-rung control
    P("-" * 118)
    P("WHY the rung count moves with N (added AFTER the pilot exposed it; reported, not re-judged):")
    P("  the k-name REACH band [mean of k lowest, mean of k highest] WIDENS as the pool grows, so a")
    P("  bigger pool unlocks HARDER rungs.  The all-rung mean above is therefore taken over a")
    P("  DIFFERENT rung set at each N.  The COMMON-RUNG ladder below fixes the rung set to those")
    P("  feasible at EVERY N on the curve, which is the like-for-like density comparison.")
    RCH = LAW[LAW.leg == "SYM"].groupby(["window", "char", "k", "n_min"]).agg(
        reach_w_B=("reach_w_B", "mean"), reach_w_S=("reach_w_S", "mean"),
        ov=("n_overlap", "mean")).reset_index()
    P(f"  {'win':4s} {'char':6s} {'k':>3s} {'N':>4s} {'reachW_B':>9s} {'reachW_S':>9s} "
      f"{'rungs':>6s}")
    for _, r in RCH[RCH.window == "FULL"].sort_values(["char", "k", "n_min"]).iterrows():
        P(f"  {r.window:4s} {r.char:6s} {int(r.k):3d} {int(r.n_min):4d} {r.reach_w_B:9.4f} "
          f"{r.reach_w_S:9.4f} {r.ov:6.2f}")
    P("")
    SR = RUNG[RUNG.leg == "SYM"].copy()
    SR["abs_resid"] = SR.resid.abs()
    com_rows, com_mono = [], {}
    for (w, char, k), d in SR.groupby(["window", "char", "k"]):
        ns = sorted(d.n_min.unique())
        common = None
        for n in ns:
            lv = set(d[d.n_min == n].level.unique())
            common = lv if common is None else (common & lv)
        if not common:
            P(f"  {w:4s} {char:6s} k {int(k):2d}: NO rung feasible at every N -> common-rung "
              f"ladder empty (N range {ns[0]}..{ns[-1]})")
            continue
        sub = d[d.level.isin(common)]
        g = sub.groupby("n_min").abs_resid.agg(["mean", "std", "size"]).reset_index()
        v = g.sort_values("n_min")["mean"].to_numpy()
        com_mono[(w, char, k)] = bool(np.all(np.diff(v) <= 0))
        for _, rr_ in g.iterrows():
            com_rows.append(dict(window=w, char=char, k=k, n_min=int(rr_.n_min),
                                 n_common_rungs=len(common), resid=float(rr_["mean"]),
                                 sd=float(rr_["std"]), obs=int(rr_["size"])))
        P(f"  {w:4s} {char:6s} k {int(k):2d}: {len(common)} common rung(s) " +
          " ".join(f"{x:.4f}" for x in sorted(common)) + "  ->  |resid| by N " +
          " ".join(f"N{int(a)}:{b:.5f}" for a, b in zip(g.n_min, g["mean"])) +
          f"  monotone {com_mono[(w,char,k)]}")
    CM = pd.DataFrame(com_rows)
    CM.to_csv(f"{OUT/STAMP}.commonrung.csv", index=False)
    cm_ma = [v for kk, v in com_mono.items() if kk[1] == "momac"]
    P(f"  COMMON-RUNG monotonicity: {sum(com_mono.values())}/{len(com_mono)} curves; momac "
      f"{sum(cm_ma)}/{len(cm_ma)}")
    cmf = {}
    for (w, char, k), d in CM.groupby(["window", "char", "k"]):
        d = d.sort_values("n_min")
        cmf[(w, char, k)] = (float(d.resid.iloc[0]), float(d.resid.iloc[-1]),
                             int(d.n_min.iloc[0]), int(d.n_min.iloc[-1]))
        P(f"    endpoint {w:4s} {char:6s} k {int(k):2d}: {d.resid.iloc[0]:.5f} "
          f"(N={int(d.n_min.iloc[0])}) -> {d.resid.iloc[-1]:.5f} (N={int(d.n_min.iloc[-1])}) = "
          f"{d.resid.iloc[0]/d.resid.iloc[-1] if d.resid.iloc[-1]>0 else np.nan:.2f}x")
    h_law_common = bool(len(cm_ma) and sum(cm_ma) == len(cm_ma))
    P(f"  H_LAW on the common-rung ladder (momac) -> {'PASS' if h_law_common else 'FAIL'}")
    P("")

    # ------------------------------------------------------------------------- H_RATIO fits
    def loglog(d, xcol):
        d = d[(d.resid > 0) & (d[xcol] > 0)]
        if len(d) < 3:
            return None
        x = np.log(d[xcol].to_numpy())
        y = np.log(d.resid.to_numpy())
        b, a = np.polyfit(x, y, 1)
        yh = a + b * x
        ss = float(((y - y.mean()) ** 2).sum())
        r2 = 1.0 - float(((y - yh) ** 2).sum()) / ss if ss > 0 else np.nan
        return dict(n=len(d), slope=float(b), intercept=float(a), R2=float(r2))

    fits = []
    P("=" * 118)
    P("H_RATIO - is the governing variable the DRAW FRACTION k/N?  log|resid| = a + b log(k/N)")
    P("=" * 118)
    SY = SY.assign(frac=SY.k / SY.n_min)
    for (w, char), d in SY.groupby(["window", "char"]):
        f_all = loglog(d, "frac")
        f_n = loglog(d.assign(frac=1.0 / d.n_min), "frac")
        if f_all:
            fits.append(dict(leg="SYM", window=w, char=char, k="pooled", x="k/N", **f_all))
            fits.append(dict(leg="SYM", window=w, char=char, k="pooled", x="1/N", **f_n))
            P(f"  {w:4s} {char:6s} pooled(18) on k/N: slope {f_all['slope']:+.3f} "
              f"R2 {f_all['R2']:.3f}   |   on 1/N alone: slope {f_n['slope']:+.3f} "
              f"R2 {f_n['R2']:.3f}")
        for k, dk in d.groupby("k"):
            f = loglog(dk, "frac")
            if f:
                fits.append(dict(leg="SYM", window=w, char=char, k=str(int(k)), x="k/N", **f))
                P(f"       k={int(k):2d} only ({f['n']} pts): slope {f['slope']:+.3f} "
                  f"R2 {f['R2']:.3f}  C={np.exp(f['intercept']):.4f}")
    FI = pd.DataFrame(fits)
    FI.to_csv(f"{OUT/STAMP}.fits.csv", index=False)
    pm = FI[(FI.leg == "SYM") & (FI.char == "momac") & (FI.k == "pooled") & (FI.x == "k/N")
            & (FI.window == "FULL")]
    h_ratio = bool(len(pm) and pm.R2.iloc[0] >= 0.70 and pm.slope.iloc[0] > 0)
    P(f"  H_RATIO -> {'PASS' if h_ratio else 'FAIL'} (momac/FULL pooled fit on k/N: "
      f"slope {pm.slope.iloc[0]:+.3f}, R2 {pm.R2.iloc[0]:.3f}; bar R2>=0.70 and slope>0)"
      if len(pm) else "  H_RATIO -> not measurable")
    P("")

    # -------------------------------------------------------------------- H_THIN vs H_FAT
    P("=" * 118)
    P("H_THIN vs H_FAT - which arm's size moves the residual?")
    P("=" * 118)
    AS = agg(LAW[LAW.leg == "ASYM_S"], ["window", "char", "k", "n_S"])
    AB = agg(LAW[LAW.leg == "ASYM_B"], ["window", "char", "k", "n_B"])
    P("  ASYM_S: n_B held at the FULL big arm, only the (already fat) small arm moves")
    P("  (columns are the requested n_S, each capped at that window/char's usable small arm, so the")
    P("   last column is the FULL arm and a request above it never appears under a bigger label)")
    for (w, char, k), d in AS.groupby(["window", "char", "k"]):
        d = d.set_index("n_S").sort_index()
        P(f"  {w:4s} {char:6s} {int(k):3d} " +
          " ".join(f"n{int(n)}:{v:.5f}" for n, v in d.resid.items()))
    P("")
    P("  ASYM_B: n_S held at the FULL small arm, only the thin big arm moves")
    P("  (n_B capped at that window/char's usable big arm - 134 on FULL, 130/131 on IS)")
    for (w, char, k), d in AB.groupby(["window", "char", "k"]):
        d = d.set_index("n_B").sort_index()
        P(f"  {w:4s} {char:6s} {int(k):3d} " +
          " ".join(f"n{int(n)}:{v:.5f}" for n, v in d.resid.items()))
    P("")
    thin_rows = []
    for (w, char, k), d in AS.groupby(["window", "char", "k"]):
        d = d.set_index("n_S")
        lo_n = max(x for x in d.index if x <= 134)
        hi_n = max(d.index)
        if lo_n == hi_n:
            continue
        band = float(d.sd.get(lo_n, np.nan))
        move = abs(float(d.resid[hi_n]) - float(d.resid[lo_n]))
        thin_rows.append(dict(window=w, char=char, k=k, lo_n=lo_n, hi_n=hi_n,
                              resid_lo=float(d.resid[lo_n]), resid_hi=float(d.resid[hi_n]),
                              move=move, rep_sd=band, flat=bool(move <= band)))
    TH = pd.DataFrame(thin_rows)
    P("  fat-arm test: n_S from the thin arm's size to the full small arm, n_B fixed")
    for _, r in TH.sort_values(["window", "char", "k"]).iterrows():
        P(f"    {r.window:4s} {r.char:6s} k {int(r.k):2d}: n_S {int(r.lo_n)} -> {int(r.hi_n)} moves "
          f"|resid| {r.resid_lo:.5f} -> {r.resid_hi:.5f} ({r.move:.5f}); replicate sd "
          f"{r.rep_sd:.5f} -> {'FLAT' if r.flat else 'MOVES'}")
    nflat = int(TH.flat.sum())
    h_thin = bool(nflat == len(TH))
    P(f"  H_THIN -> {'PASS' if h_thin else 'FAIL'} ({nflat}/{len(TH)} curves flat past the thin "
      f"arm);  H_FAT -> {'PASS' if not h_thin else 'FAIL'}")
    P("")
    thin2 = []
    for (w, char, k), d in AB.groupby(["window", "char", "k"]):
        d = d.set_index("n_B")
        lo_n, hi_n = min(d.index), max(d.index)
        if lo_n == hi_n:
            continue
        band = float(d.sd.get(lo_n, np.nan))
        move = abs(float(d.resid[hi_n]) - float(d.resid[lo_n]))
        thin2.append(dict(window=w, char=char, k=k, lo_n=lo_n, hi_n=hi_n,
                          resid_lo=float(d.resid[lo_n]), resid_hi=float(d.resid[hi_n]),
                          move=move, rep_sd=band, flat=bool(move <= band)))
    T2 = pd.DataFrame(thin2)
    P("  THIN-ARM test (the symmetric leg H_THIN needs but did not state): n_B moves, n_S full")
    for _, r in T2.sort_values(["window", "char", "k"]).iterrows():
        P(f"    {r.window:4s} {r.char:6s} k {int(r.k):2d}: n_B {int(r.lo_n)} -> {int(r.hi_n)} moves "
          f"|resid| {r.resid_lo:.5f} -> {r.resid_hi:.5f} ({r.move:.5f}); replicate sd "
          f"{r.rep_sd:.5f} -> {'FLAT' if r.flat else 'MOVES'}")
    n2flat = int(T2.flat.sum())
    no_law = bool(n2flat >= len(T2) - 2 and nflat >= len(TH) - 2)
    P(f"  thin arm FLAT in {n2flat}/{len(T2)} curves, fat arm FLAT in {nflat}/{len(TH)}")
    P("  STATED AFTER THE FACT, not pre-registered: if the residual is flat in BOTH arms over this")
    P("  range then there is no pool-size law of either kind - min(n_B,n_S) does not govern it and")
    P(f"  neither does max.  -> {'THAT IS WHAT IS MEASURED' if no_law else 'not what is measured'}")
    P("")
    sym = LAW[LAW.leg == "SYM"]
    noise = (SY.sd / SY.resid).replace([np.inf, -np.inf], np.nan)
    P(f"  NOISE DOMINANCE: median replicate sd / |resid| over the {len(SY)} SYM cells = "
      f"{float(noise.median()):.2f}")
    for (w, char), d in SY.groupby(["window", "char"]):
        rng = float(d.resid.max() - d.resid.min())
        P(f"    {w:4s} {char:6s}: |resid| spans {d.resid.min():.5f}..{d.resid.max():.5f} "
          f"(range {rng:.5f}) across the whole N x k grid; mean replicate sd {d.sd.mean():.5f} "
          f"= {d.sd.mean()/rng if rng > 0 else np.nan:.2f}x the range")
    P("")
    P("-" * 118)
    P("THE ANCHOR IN ITS OWN SAMPLING DISTRIBUTION")
    P("  At n_S >= the usable small arm the sub-sample IS the full pool, so the replicates at that")
    P("  column differ ONLY in the draw's seed key: they are a resampling distribution of idea")
    P("  796's own statistic, on its own data, with nothing changed but the random draw.")
    anch = []
    for char in CHARS:
        nSf = len(W["FULL"]["S"][char])
        d = LAW[(LAW.leg == "ASYM_S") & (LAW.window == "FULL") & (LAW.char == char)
                & (LAW.k == K_ANCHOR) & (LAW.n_S == nSf)]
        if d.empty:
            continue
        v = np.sort(d.abs_resid.to_numpy())
        want = P796_RESID[char]
        below = int((v < want).sum())
        anch.append(dict(char=char, n=len(v), committed=want, mean=float(v.mean()),
                         sd=float(v.std(ddof=1)), lo=float(v.min()), hi=float(v.max()),
                         n_below_committed=below))
        P(f"  {char:6s} k=36, n_B=134, n_S={nSf}: committed {want:.5f}; {len(v)} re-draws give "
          f"mean {v.mean():.5f} sd {v.std(ddof=1):.5f}, range {v.min():.5f}..{v.max():.5f}; "
          f"{below}/{len(v)} re-draws land below the committed value")
        P(f"  {'':6s} -> the committed value is {want/v.mean():.2f}x the mean of its own "
          f"resampling distribution, i.e. "
          f"{(v.mean()-want)/v.std(ddof=1) if v.std(ddof=1) > 0 else np.nan:+.2f} sd from it")
    AN = pd.DataFrame(anch)
    P(f"  The six ASYM_S replicates above are only six.  {len(ANCH_R)} more re-draws of the SAME")
    P("  cell follow, so the committed value's position is a rank in a real distribution and not an")
    P("  sd distance estimated off six points.  Nothing changes between them but the draw key.")
    arows = []
    for char in CHARS:
        nBf, nSf = len(W["FULL"]["B"][char]), len(W["FULL"]["S"][char])
        for rep in ANCH_R:
            r, _ = cell_resid("FULL", char, nBf, nSf, K_ANCHOR, rep, "ANCHRS")
            if not np.isnan(r["abs_resid"]):
                arows.append(r)
    AR = pd.DataFrame(arows)
    AR.to_csv(f"{OUT/STAMP}.anchres.csv", index=False)
    anchres = []
    for char in CHARS:
        v = np.sort(AR[AR.char == char].abs_resid.to_numpy())
        if not len(v):
            continue
        want = P796_RESID[char]
        below = int((v < want).sum())
        anchres.append(dict(char=char, n=len(v), committed=want, mean=float(v.mean()),
                            sd=float(v.std(ddof=1)), p05=float(np.quantile(v, 0.05)),
                            median=float(np.median(v)), lo=float(v.min()), hi=float(v.max()),
                            n_below=below, frac_below=below / len(v)))
        P(f"  {char:6s} {len(v)} re-draws: mean {v.mean():.5f} sd {v.std(ddof=1):.5f} "
          f"median {np.median(v):.5f} p05 {np.quantile(v, 0.05):.5f} "
          f"range {v.min():.5f}..{v.max():.5f}")
        P(f"  {'':6s} committed {want:.5f} -> {below}/{len(v)} re-draws below it "
          f"({below/len(v):.1%}), {want/v.mean():.2f}x the mean, "
          f"{(want-v.mean())/v.std(ddof=1):+.2f} sd")
    ANR = pd.DataFrame(anchres)
    mo = ANR[ANR.char == "momac"]
    P("")

    # ------------------------------------------------------------------------------ REEST leg
    P("=" * 118)
    P("H_REEST - was idea 796's 5x DENSITY, or CHARACTERISTIC RE-ESTIMATION?")
    P("=" * 118)
    P("  REEST repeats the SYM leg with the characteristic, the rungs and the bandwidth recomputed")
    P("  ON THE SUB-SAMPLED POOL - which is what idea 796's 430->663 vintage change actually did.")
    rr = []
    for w in WINDOWS:
        for char in ["momac"]:
            for n in NGRID:
                for rep in REPS:
                    d = W[w]
                    nmB = subsample(d["B"][char], n, f"SUB|BONLY|{char}|{w}|{n}|{rep}")
                    nmS = subsample(d["S"][char], n, f"SUB|SONLY|{char}|{w}|{n}|{rep}")
                    sub = d["pool"][nmB + nmS]
                    ncx = pers_name_chars(sub)
                    lvx = [round(float(ncx[char].quantile(q)), 6) for q in LEVEL_Q5]
                    hx = BW * float(ncx[char].std())
                    r, _ = cell_resid(w, char, n, n, K_ANCHOR, rep, "REEST",
                                      ncx=ncx, lvx=lvx, hx=hx)
                    r["sd_sub"] = float(ncx[char].std())
                    rr.append(r)
    RE = pd.DataFrame(rr).dropna(subset=["abs_resid"])
    RE.to_csv(f"{OUT/STAMP}.reest.csv", index=False)
    P(f"  {'win':4s} {'N':>4s} {'|resid| FROZEN':>15s} {'|resid| REEST':>14s} {'ratio':>7s} "
      f"{'sd(ch) full':>12s} {'sd(ch) sub':>11s}")
    reest_rows = []
    for (w, n), d in RE.groupby(["window", "n_min"]):
        fz = LAW[(LAW.leg == "SYM") & (LAW.window == w) & (LAW.char == "momac")
                 & (LAW.k == K_ANCHOR) & (LAW.n_min == n)].abs_resid.mean()
        re_ = float(d.abs_resid.mean())
        reest_rows.append(dict(window=w, n=n, frozen=float(fz), reest=re_,
                               ratio=re_ / fz if fz > 0 else np.nan))
        P(f"  {w:4s} {int(n):4d} {fz:15.5f} {re_:14.5f} {re_/fz if fz>0 else np.nan:7.2f} "
          f"{W[w]['sd']['momac']:12.4f} {float(d.sd_sub.mean()):11.4f}")
    RR = pd.DataFrame(reest_rows)
    fz_span = LAW[(LAW.leg == "SYM") & (LAW.char == "momac") & (LAW.k == K_ANCHOR)
                  & (LAW.window == "FULL")].groupby("n_min").abs_resid.mean()
    re_span = RE[RE.window == "FULL"].groupby("n_min").abs_resid.mean()
    sp_fz = float(fz_span.max() / fz_span.min()) if fz_span.min() > 0 else np.nan
    sp_re = float(re_span.max() / re_span.min()) if re_span.min() > 0 else np.nan
    h_reest = bool(sp_re > sp_fz)
    P(f"  FULL window, momac, k=36: span across N is {sp_fz:.2f}x with the characteristic FROZEN "
      f"and {sp_re:.2f}x when it is RE-ESTIMATED")
    P(f"  H_REEST -> {'PASS' if h_reest else 'FAIL'} (re-estimation moves |resid| "
      f"{'MORE' if h_reest else 'LESS'} than density alone)")
    P("")

    # -------------------------------------------------------------------- entitlement table
    P("=" * 118)
    P("H_ENTITLE - the entitlement table.  What |resid| is a matched-level claim ENTITLED to?")
    P("=" * 118)
    ent = []
    for (char, k, n), d in LAW[(LAW.leg == "SYM") & (LAW.window == "FULL")].groupby(
            ["char", "k", "n_min"]):
        ent.append(dict(char=char, k=k, n_min=n, cells=len(d),
                        mean=float(d.abs_resid.mean()), sd=float(d.abs_resid.std()),
                        p90=float(d.abs_resid.quantile(0.90)),
                        max=float(d.abs_resid.max()),
                        worst_rung=float(d.worst_rung.max())))
    EN = pd.DataFrame(ent)
    EN.to_csv(f"{OUT/STAMP}.entitle.csv", index=False)
    P("  FULL window, SYM leg, frozen characteristic; mean / p90 / max over "
      f"{len(REPS)} replicates")
    P(f"  {'char':6s} {'k':>3s} {'N':>4s} {'mean':>9s} {'p90':>9s} {'max':>9s} {'worstRung':>10s}")
    for _, r in EN.sort_values(["char", "k", "n_min"]).iterrows():
        P(f"  {r.char:6s} {int(r.k):3d} {int(r.n_min):4d} {r['mean']:9.5f} {r.p90:9.5f} "
          f"{r['max']:9.5f} {r.worst_rung:10.5f}")
    work = EN[(EN.char == "momac") & (EN.k == K_ANCHOR) & (EN.n_min == max(NGRID))]
    ent_mean = float(work["mean"].iloc[0]) if len(work) else np.nan
    ent_p90 = float(work.p90.iloc[0]) if len(work) else np.nan
    h_ent = bool(ent_p90 > TPERS571_RESID and ent_p90 > VOLPERS798_RESID)
    P(f"  the record's working cell (momac, k=36, N={max(NGRID)}): entitled |resid| mean "
      f"{ent_mean:.5f}, p90 {ent_p90:.5f}")
    P(f"  the record's tightest published residuals: tpers {TPERS571_RESID:.4f} (idea 571), "
      f"volpers {VOLPERS798_RESID:.4f} (idea 798)")
    P(f"  H_ENTITLE -> {'PASS' if h_ent else 'FAIL'}")
    P("")

    # ----------------------------------------------------------------- WF-A: the law out of sample
    P("=" * 118)
    P("RULE 8 / WF-A - the law rebuilt inside each window; the IS exponent PREDICTS the OOS cells")
    P("=" * 118)
    wf = []
    for char in CHARS:
        fi = FI[(FI.char == char) & (FI.k == "pooled") & (FI.x == "k/N")].set_index("window")
        if not {"IS", "OOS"} <= set(fi.index):
            continue
        a, b = float(fi.loc["IS", "intercept"]), float(fi.loc["IS", "slope"])
        d = SY[(SY.char == char) & (SY.window == "OOS")].copy()
        d["pred"] = np.exp(a + b * np.log(d.frac))
        err = float((np.log(d.resid) - np.log(d["pred"])).abs().mean())
        med = float((d["pred"] / d.resid).median())
        P(f"  {char:6s} IS fit  slope {b:+.3f} R2 {float(fi.loc['IS','R2']):.3f}   ->  OOS cells: "
          f"mean |log ratio| {err:.3f}, median pred/actual {med:.2f}x")
        P(f"  {char:6s} OOS own slope {float(fi.loc['OOS','slope']):+.3f} "
          f"R2 {float(fi.loc['OOS','R2']):.3f};  FULL slope "
          f"{float(fi.loc['FULL','slope']):+.3f} R2 {float(fi.loc['FULL','R2']):.3f}")
        wf.append(dict(leg="WF-A", char=char, IS_slope=b, IS_R2=float(fi.loc["IS", "R2"]),
                       OOS_slope=float(fi.loc["OOS", "slope"]), OOS_R2=float(fi.loc["OOS", "R2"]),
                       FULL_slope=float(fi.loc["FULL", "slope"]),
                       OOS_mean_abs_log_err=err, OOS_median_pred_over_actual=med))
    P("  H_LAW / H_THIN by window (momac):")
    for w in WINDOWS:
        mk = [mono[(w, "momac", k)] for k in KGRID if (w, "momac", k) in mono]
        tk = TH[(TH.window == w) & (TH.char == "momac")]
        P(f"    {w:4s}: monotone in N {sum(mk)}/{len(mk)} k-curves; fat-arm FLAT "
          f"{int(tk.flat.sum())}/{len(tk)}")
    P("")

    # ------------------------------------------------------------------------- the book leg
    P("=" * 118)
    P("BOOKS - the ladder read as a trading instruction, at every one of the 18 tuned cells")
    P("=" * 118)
    v2_56 = fast_backtest(px56, rules_v2_weights(px56), COST, "W")["returns"]
    rows = []
    draws = []
    for k in KGRID:
        for n in NGRID:
            for rep in BOOK_REPS:
                d = W["FULL"]
                char = "momac"
                pools = {}
                nmB = subsample(d["B"][char], n, f"SUB|BONLY|{char}|FULL|{n}|{rep}")
                nmS = subsample(d["S"][char], n, f"SUB|SONLY|{char}|FULL|{n}|{rep}")
                pools["BONLY"] = nmB
                pools["SONLY"] = nmS
                pools["POOL"] = sorted(nmB + nmS)
                for fl in BOOK_FLAVOURS:
                    nm = np.array(pools[fl])
                    x = d["nc"].loc[list(nm), char].to_numpy(float)
                    lo, hi = reach(x, k)
                    for L in d["lv"][char]:
                        if not (lo <= L <= hi):
                            continue
                        for sd in SEEDS:
                            key = f"CHAR|{char}|{L:.6f}|{fl}|{sd}|FULL|n{len(nm)}|r{rep}|k{k}|BOOK"
                            draws.append(dict(k=k, n=n, rep=rep, flavour=fl, level=L, seed=sd,
                                              names=kdraw(nm, x, L, d["h"][char], k, key)))
    P(f"  {len(draws)} draws x {len(ARMS)} arms x {len(GROSS)} gross x {len(CADENCE)} cadence = "
      f"{len(draws)*len(ARMS)*len(GROSS)*len(CADENCE)} books")
    pool_full = W["FULL"]["pool"]
    for i, dr in enumerate(draws):
        pxd = pd.concat([pool_full[dr["names"]], SPY.rename("SPY")], axis=1).dropna(
            how="all").ffill()
        tr = set(dr["names"])
        st = pxd.index[260]
        spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
        ach = W["FULL"]["fc"].panel(dr["names"])
        for g in GROSS:
            books = make_books(pxd, tr, g)
            for freq in CADENCE:
                for a in ARMS:
                    res = fast_backtest(pxd, books[a], COST, freq)
                    r = res["returns"].loc[st:]
                    row = dict(k=dr["k"], n=dr["n"], rep=dr["rep"], flavour=dr["flavour"],
                               level=dr["level"], seed=dr["seed"], arm=a, gross=g, cadence=freq,
                               achieved=ach["momac"], ach_tpers=ach["tpers"], ach_cvol=ach["cvol"])
                    row.update(rowify(r, res["turnover"].loc[st:]))
                    row["keep4a"] = keep_4a(r, v2)
                    row["fail4b"] = fail_4b(r, spy)
                    row["keep4b"] = row["fail4b"] == "-"
                    rows.append(row)
        if (i + 1) % 300 == 0:
            P(f"    {i+1}/{len(draws)} draws ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT/STAMP}.grid.csv", index=False)
    st = W["FULL"]["pool"].index[260]
    spy_full = SPY.pct_change().fillna(0.0).loc[st:]
    v2_56s = v2_56.loc[st:]
    P(f"  {len(G)} books ({time.time()-t0:.0f}s)")
    P("")
    P("  KEEP paths per tuned cell (4a vs RULES v2 on the drawn panel; 4b vs SPY)")
    P(f"  {'k':>3s} {'N':>4s} {'books':>6s} {'4a':>5s} {'4b':>5s} {'BOTH':>5s} {'bestSh':>7s} "
      f"{'top fail4b legs':<28s}")
    kp = []
    for (k, n), d in G.groupby(["k", "n"]):
        both = int((d.keep4a & d.keep4b).sum())
        legs = d.loc[~d.keep4b, "fail4b"].value_counts().head(3)
        kp.append(dict(k=k, n=n, books=len(d), keep4a=int(d.keep4a.sum()),
                       keep4b=int(d.keep4b.sum()), both=both, best_Sharpe=float(d.Sharpe.max())))
        P(f"  {int(k):3d} {int(n):4d} {len(d):6d} {int(d.keep4a.sum()):5d} "
          f"{int(d.keep4b.sum()):5d} {both:5d} {float(d.Sharpe.max()):7.3f} "
          + " ".join(f"{a}:{b}" for a, b in legs.items()))
    KP = pd.DataFrame(kp)
    KP.to_csv(f"{OUT/STAMP}.keeppaths.csv", index=False)
    P(f"  TOTAL: {len(G)} books, 4a {int(G.keep4a.sum())}, 4b {int(G.keep4b.sum())}, "
      f"BOTH {int((G.keep4a & G.keep4b).sum())}")
    P("")

    # ------------------------------------------------------------------------------ WF-B
    P("=" * 118)
    P("RULE 8 / WF-B - (flavour, level, seed, gross, cadence, arm) chosen by IS Sharpe ALONE at")
    P("                every tuned cell; OOS read ONCE against RULES v2 (U56) and SPY")
    P("=" * 118)
    mv2 = metrics(v2_56s.loc[OOS_START:])
    msp = metrics(spy_full.loc[OOS_START:])
    P(f"  OOS comparands: RULES v2 on U56  CAGR {mv2['CAGR']:.2%} Sharpe {mv2['Sharpe']:.3f} "
      f"MaxDD {mv2['MaxDD']:.2%}")
    P(f"                  SPY               CAGR {msp['CAGR']:.2%} Sharpe {msp['Sharpe']:.3f} "
      f"MaxDD {msp['MaxDD']:.2%}")
    P(f"  {'k':>3s} {'N':>4s} {'pick':<34s} {'IS_Sh':>6s} {'OOS_Sh':>7s} {'OOS_CAGR':>9s} "
      f"{'OOS_DD':>8s} {'>v2':>4s} {'>SPY':>5s} {'4a':>3s} {'4b':>12s}")
    for (k, n), d in G.groupby(["k", "n"]):
        b = d.loc[d.IS_Sharpe.idxmax()]
        pick = (f"{b.flavour}/L{b.level:.3f}/s{int(b.seed)}/{b.arm}/g{b.gross:.2f}/{b.cadence}")
        wf.append(dict(leg="WF-B", k=k, n=n, pick=pick, IS_Sharpe=b.IS_Sharpe,
                       OOS_Sharpe=b.OOS_Sharpe, OOS_CAGR=b.OOS_CAGR, OOS_MaxDD=b.OOS_MaxDD,
                       beats_v2_OOS=bool(b.OOS_Sharpe > mv2["Sharpe"]),
                       beats_SPY_OOS=bool(b.OOS_Sharpe > msp["Sharpe"]),
                       keep4a=bool(b.keep4a), fail4b=b.fail4b))
        P(f"  {int(k):3d} {int(n):4d} {pick:<34s} {b.IS_Sharpe:6.3f} {b.OOS_Sharpe:7.3f} "
          f"{b.OOS_CAGR:9.2%} {b.OOS_MaxDD:8.2%} "
          f"{'Y' if b.OOS_Sharpe > mv2['Sharpe'] else 'n':>4s} "
          f"{'Y' if b.OOS_Sharpe > msp['Sharpe'] else 'n':>5s} "
          f"{'Y' if b.keep4a else 'n':>3s} {b.fail4b:>12s}")
    gb = G.loc[G.IS_Sharpe.idxmax()]
    P(f"  GLOBAL pick over all {len(KP)} cells: k={int(gb.k)} N={int(gb.n)} {gb.flavour}/"
      f"L{gb.level:.3f}/s{int(gb.seed)}/{gb.arm}/g{gb.gross:.2f}/{gb.cadence}  IS Sharpe "
      f"{gb.IS_Sharpe:.3f} -> OOS Sharpe {gb.OOS_Sharpe:.3f} CAGR {gb.OOS_CAGR:.2%} "
      f"MaxDD {gb.OOS_MaxDD:.2%}; 4a {gb.keep4a}, 4b fails [{gb.fail4b}]")
    wf.append(dict(leg="WF-B-global", k=int(gb.k), n=int(gb.n),
                   pick=f"{gb.flavour}/L{gb.level:.3f}/s{int(gb.seed)}/{gb.arm}/"
                        f"g{gb.gross:.2f}/{gb.cadence}",
                   IS_Sharpe=gb.IS_Sharpe, OOS_Sharpe=gb.OOS_Sharpe, OOS_CAGR=gb.OOS_CAGR,
                   OOS_MaxDD=gb.OOS_MaxDD, beats_v2_OOS=bool(gb.OOS_Sharpe > mv2["Sharpe"]),
                   beats_SPY_OOS=bool(gb.OOS_Sharpe > msp["Sharpe"]), keep4a=bool(gb.keep4a),
                   fail4b=gb.fail4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT/STAMP}.walkforward.csv", index=False)
    nb = WF[WF.leg == "WF-B"]
    P(f"  WF-B: {int(nb.beats_v2_OOS.sum())}/{len(nb)} picks beat RULES v2 OOS Sharpe, "
      f"{int(nb.beats_SPY_OOS.sum())}/{len(nb)} beat SPY, 4a {int(nb.keep4a.sum())}/{len(nb)}, "
      f"4b {int((nb.fail4b == '-').sum())}/{len(nb)}")
    P("")

    # --------------------------------------------------------------------------- summary
    SUM = pd.DataFrame([
        dict(key="G0_draws_differ", value=g0),
        dict(key="G1_chars_max_d", value=g1),
        dict(key="G2_backtest_max_d", value=g2),
        dict(key="G3_anchor_max_d", value=g3),
        dict(key="H_PARENT", value="PASS" if g3 <= TOL_ANCHOR else "FAIL"),
        dict(key="H_LAW", value="PASS" if h_law else "FAIL"),
        dict(key="H_LAW_monotone_curves", value=f"{nm_ok}/{len(mono)}"),
        dict(key="H_LAW_common_rung", value="PASS" if h_law_common else "FAIL"),
        dict(key="H_LAW_common_rung_curves", value=f"{sum(com_mono.values())}/{len(com_mono)}"),
        dict(key="H_RATIO", value="PASS" if h_ratio else "FAIL"),
        dict(key="H_RATIO_slope_R2", value=(f"{pm.slope.iloc[0]:+.4f}/{pm.R2.iloc[0]:.4f}"
                                           if len(pm) else "NA")),
        dict(key="H_THIN", value="PASS" if h_thin else "FAIL"),
        dict(key="H_FAT", value="PASS" if not h_thin else "FAIL"),
        dict(key="H_THIN_fat_arm_flat_curves", value=f"{nflat}/{len(TH)}"),
        dict(key="thin_arm_flat_curves", value=f"{n2flat}/{len(T2)}"),
        dict(key="NO_LAW_both_arms_flat", value="YES" if no_law else "NO"),
        dict(key="median_rep_sd_over_resid", value=round(float(noise.median()), 4)),
        dict(key="anchor_resampled_mean_momac",
             value=(float(AN[AN.char == "momac"]["mean"].iloc[0])
                    if len(AN[AN.char == "momac"]) else np.nan)),
        dict(key="anchor_committed_momac", value=P796_RESID["momac"]),
        dict(key="anchor_redraws_n", value=(int(mo.n.iloc[0]) if len(mo) else 0)),
        dict(key="anchor_redraw_mean_momac", value=(float(mo["mean"].iloc[0]) if len(mo) else np.nan)),
        dict(key="anchor_redraw_sd_momac", value=(float(mo.sd.iloc[0]) if len(mo) else np.nan)),
        dict(key="anchor_redraws_below_committed_momac",
             value=(f"{int(mo.n_below.iloc[0])}/{int(mo.n.iloc[0])}" if len(mo) else "NA")),
        dict(key="H_REEST", value="PASS" if h_reest else "FAIL"),
        dict(key="H_REEST_span_frozen_vs_reest", value=f"{sp_fz:.3f}/{sp_re:.3f}"),
        dict(key="H_ENTITLE", value="PASS" if h_ent else "FAIL"),
        dict(key="entitled_resid_mean_n134_k36", value=ent_mean),
        dict(key="entitled_resid_p90_n134_k36", value=ent_p90),
        dict(key="books", value=len(G)),
        dict(key="keep4a", value=int(G.keep4a.sum())),
        dict(key="keep4b", value=int(G.keep4b.sum())),
        dict(key="keep_both", value=int((G.keep4a & G.keep4b).sum())),
        dict(key="wfb_beat_v2_oos", value=f"{int(nb.beats_v2_OOS.sum())}/{len(nb)}"),
        dict(key="wfb_beat_spy_oos", value=f"{int(nb.beats_SPY_OOS.sum())}/{len(nb)}"),
        dict(key="runtime_s", value=round(time.time() - t0, 1)),
    ])
    SUM.to_csv(f"{OUT/STAMP}.summary.csv", index=False)
    P("=" * 118)
    P("SUMMARY")
    P("=" * 118)
    for _, r in SUM.iterrows():
        P(f"  {r.key:34s} {r.value}")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
