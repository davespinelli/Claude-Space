#!/usr/bin/env python3
"""Idea 571 (lane B, 2026-09-11) - is-tpers-INFORMATION-or-TAUTOLOGY.

QUESTION
--------
Idea 569 measured the MA-gate SELECTION premium `Sharpe(MA-RS) - Sharpe(EWall)` on
kernel-matched k=36 draws and found ONE characteristic that orders it monotonically:

    tpers  = 1 - daily flip rate of the name's own above-200d-MA state
    POOL slope +33.381187, R2 0.847210, slope*span +0.707607 = 7.24x the published GAP,
    monotone up on all three flavours, premium changes SIGN over the rungs, and the slope
    STRENGTHENS out of sample (IS +21.37 -> OOS +39.08).

But tpers IS the gate's own state variable.  "The gate pays where its state is persistent"
may be an identity: the MA-RS arm differs from EWall only by that state, so a name whose
state never flips is a name the gate holds (or drops) for the whole sample, and the premium
could be reading its own construction rather than a property of the names.

THE TEST (the queue's wording): re-run the SAME kernel-draw ranking on the persistence of a
DIFFERENT signal and report whether the R2 survives when the persistence variable is not the
gate's.  Three non-gate persistence variables are run beside tpers as the REFERENCE:

    tpers    REFERENCE   1 - flip rate of the above-200d-MA state      (the GATE's own variable)
    mompers  PRIMARY     1 - flip rate of the state "12-1 momentum rank_pct > 0.5" over the
                         pooled cross-section.  This is the queue's named variable: 12-1
                         momentum RANK persistence.
    momsgn   ROBUSTNESS  1 - flip rate of the state "12-1 momentum > 0".  Name-local (no
                         cross-sectional reference), so it is the closest structural twin of
                         tpers that is not the gate's variable.
    momac    ROBUSTNESS  lag-21 autocorrelation of the name's 12-1 momentum rank_pct.  A
                         CONTINUOUS reading of the same persistence, in case the binary
                         flip-rate form is what carries tpers.

Every one of the four is a persistence statistic of the same functional family; only the
first is the gate's.  If the R2 is about PERSISTENCE, the non-gate variables should order the
premium too.  If it is about the GATE, only tpers will.

DESIGN (idea 569's machinery, verbatim where it can be)
-------------------------------------------------------
Pool  = 135 B136 tradables + SMALL tradables on the COMMON trading index.  SMALL names with
        max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST.  SPY benchmark only.
        The per-name frame is built with idea 569's FIVE original characteristics and
        dropna()'d exactly as it was, THEN the four persistence columns are joined on that
        same index, so the pooled name set - and therefore every pre-registered rung level
        and every tpers draw - is bit-identical to idea 569's.  That is what makes G1 a real
        reproduction gate rather than a re-estimate.
        SURVIVORSHIP: B136 and the small panel are CURRENT constituents.  Every number below
        inherits that bias and is a statement about surviving names, not a tradable 2010 list.
Draw  = k = 36 names without replacement, probability proportional to a Gaussian kernel on
        the name's own characteristic, w_i = exp(-0.5*((x_i-L)/h)^2), h = 0.5*sd(x) over the
        pooled names (idea 569's BW_MULT, NOT re-tuned).  Seeded
        crc32("CHAR|{char}|{L:.6f}|{flavour}|{seed}"), 6 seeds per rung.  k is 36 at every
        rung, so panel WIDTH is never confounded with composition.
Levels= PRE-REGISTERED as the pooled 10/30/50/70/90th percentiles of that characteristic.
Arms  = EWall (gross g over every priced tradable, CONTROL) and MA-RS (gross g over names
        above their 200d MA, RESPREAD, TREATMENT).  premium = Sharpe(MA-RS) - Sharpe(EWall)
        at the SAME (panel, g, cadence).  RESPREAD holds gross fixed: pure selection.
Flavours POOL / BONLY / SONLY, as idea 569, so H_CARRIER is re-measurable on the new
        variables.  A rung runs only where the flavour can reach the level (feasible band =
        mean of its 36 lowest / 36 highest names); infeasible rungs are reported, never
        silently dropped.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the SIGNAL (which persistence variable) and
the target LEVEL.  Gross g in {0.50, 0.75, 1.00} and cadence {W, M} are REPORTED axes averaged
over for the headline premium (idea 51's convention); seed is replication; flavour is a
reported contrast.  EVERY grid point is written to .grid.csv.

PRE-REGISTERED HYPOTHESES (fixed before any premium on a NEW variable was read)
------------------------------------------------------------------------------
GAP         = 0.0978    idea 51's published U56 - SMALL439 premium gap.
ORIGIN568   = 0.1961    idea 568's mean matched-level B-S gap.
R2_TPERS    = 0.847210  idea 569's committed tpers POOL R2   (the number under test).
SLOPE_TPERS = 33.381187 idea 569's committed tpers POOL slope.
EFF_TPERS   = 0.707607  idea 569's committed tpers POOL slope*span.

H_INFO(char)  : the POOL premium is monotone in `char` in the required direction (sign fixed
                in advance by the three REAL panels' own values of `char`, computed before any
                premium is read), |slope*span| >= 0.5*GAP, AND R2 >= 0.5*R2_TPERS.  A NON-GATE
                variable that passes this makes tpers INFORMATION about persistence.
H_TAUT        : tpers passes H_INFO and NO non-gate persistence variable does.  Then the
                ranking is the gate reading its own state: TAUTOLOGY.
H_INDEP(char) : |Spearman(char, tpers)| over the pooled names < 0.50.  Reported for every
                variable: a non-gate variable that passes H_INFO while being a near-copy of
                tpers is not independent evidence.
H_CARRIER(char): idea 569's bar - at EVERY overlapping matched rung |premium(BONLY) -
                premium(SONLY)| inside the within-rung seed sd AND mean |B-S| < 0.5*ORIGIN568.
                (No variable has ever passed it; re-measured here for the record.)

RULE 8 (walk-forward, required): WF-A refits every slope inside 2010-2016 and again in
2017-2026, read once, and reports whether the sign holds and whether the R2 ordering of the
four variables survives.  WF-B picks (char, level) by IS Sharpe ALONE at g=0.75/W on the POOL
flavour, then reads the OOS window once against RULES v2 on B136 and against SPY.  BOTH KEEP
paths (4a vs RULES v2 on the same panel, 4b vs SPY) are evaluated on EVERY book and counted.

Costs 10 bps per unit turnover, weights at close t applied t+1 (engine convention), no
shorting, no leverage.

GATES
-----
G1  idea 569's committed tpers POOL/BONLY/SONLY slopes, R2s and rung premia reproduce from
    this run's draws (the pooled name set, levels and seeds are built to be identical).
G2  fast_backtest == engine.backtest on a real book.
G3  idea 569's committed tpers matched-level B-S origin gaps reproduce.
"""
import sys, time, zlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
MOM_LAG, MOM_LOOK = 21, 252         # 12-1 momentum: px.shift(21)/px.shift(252)-1 (scan.py)
AC_LAG = 21                         # momac: lag-21 autocorrelation of the momentum rank
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K = 36
SEEDS = [0, 1, 2, 3, 4, 5]
FLAVOURS = ["POOL", "BONLY", "SONLY"]
OLD_CHARS = ["cvol", "mrho", "beta", "tpers", "plevel"]   # idea 569's frame, for index parity
CHARS = ["tpers", "mompers", "momsgn", "momac"]
NEW_CHARS = ["mompers", "momsgn", "momac"]                # the NON-GATE persistence variables
LEVEL_Q = [0.10, 0.30, 0.50, 0.70, 0.90]
BW_MULT = 0.5
GAP = 0.0978
ORIGIN568 = 0.1961
R2_TPERS = 0.847210
SLOPE_TPERS = 33.381187
EFF_TPERS = 0.707607
PARENT = "2026-09-09_name-the-CARRIER-that-survives-a-CHARACTERISTIC-MATCH_cloud"
PARENT_END = "2026-09-04"
G1_TOL, G2_TOL, G3_TOL = 1e-6, 1e-12, 1e-6
INDEP_BAR = 0.50

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G2).  Idea 312/568/569's runner."""
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


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
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
    if not a1 > s1: f.append("H1")
    if not a2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]: f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float((resid ** 2).sum()) / ss if ss > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2


def spearman(a, b):
    d = pd.concat([pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))],
                  axis=1).dropna()
    return float(np.corrcoef(d.iloc[:, 0].rank().values, d.iloc[:, 1].rank().values)[0, 1])


def pearson(a, b):
    d = pd.concat([pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))],
                  axis=1).dropna()
    return float(np.corrcoef(d.iloc[:, 0].values, d.iloc[:, 1].values)[0, 1])


# ------------------------------------------------------------------------- panels
def small_tradables(pxs):
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return [c for c in pxs.columns if c != "SPY" and c not in bad]


def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    s_stk = small_tradables(pxs)
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }


# ------------------------------------------------ per-NAME characteristics
def _flip_persistence(state, valid):
    """1 - daily flip rate of a binary state, over days where the state is defined."""
    st = state.where(valid)
    flips = st.astype(float).diff().abs().where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    return (1.0 - flips.sum() / denom).astype(float)


def mom_frame(pool):
    """12-1 momentum level and its pooled cross-sectional percentile rank, per day."""
    mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    rk = mom.rank(axis=1, pct=True)
    return mom, rk


def old_name_chars(pool, spy_px):
    """Idea 569's FIVE characteristics, verbatim, so the dropna()'d index matches exactly."""
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)
    C = r.corr()
    n = C.shape[0]
    mrho = ((C.sum(axis=0) - 1.0) / (n - 1)).astype(float)
    sr = spy_px.pct_change().reindex(r.index)
    var_s = float(sr.var())
    beta = r.apply(lambda c: float(c.cov(sr)) / var_s if var_s > 0 else np.nan).astype(float)
    ma = pool.rolling(MA_WIN).mean()
    valid = pool.notna() & ma.notna()
    tpers = _flip_persistence(pool > ma, valid)
    plevel = np.log10(pool.median().astype(float).clip(lower=1e-6))
    return pd.DataFrame(dict(cvol=vol, mrho=mrho, beta=beta, tpers=tpers, plevel=plevel)).dropna()


def pers_name_chars(pool):
    """The three NON-GATE persistence variables (plus tpers, recomputed identically)."""
    ma = pool.rolling(MA_WIN).mean()
    v_ma = pool.notna() & ma.notna()
    tpers = _flip_persistence(pool > ma, v_ma)

    mom, rk = mom_frame(pool)
    v_mom = pool.notna() & mom.notna()
    mompers = _flip_persistence(rk > 0.5, v_mom)          # queue's variable: RANK persistence
    momsgn = _flip_persistence(mom > 0.0, v_mom)          # name-local twin of tpers

    ac = {}
    for c in pool.columns:
        s = rk[c].where(v_mom[c]).dropna()
        ac[c] = float(s.corr(s.shift(AC_LAG))) if len(s) > 3 * AC_LAG else np.nan
    momac = pd.Series(ac, dtype=float)
    return pd.DataFrame(dict(tpers=tpers, mompers=mompers, momsgn=momsgn, momac=momac))


def panel_chars(px, tradable, spy_r):
    """Panel-level values of every characteristic used here (equal-weight over constituents)."""
    cols = [c for c in px.columns if c in tradable]
    sub = px[cols]
    r = sub.pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    on = above_ma(sub) & sub.notna()
    breadth = float(on.sum(axis=1).div(sub.notna().sum(axis=1).replace(0, np.nan)).mean())
    ma = sub.rolling(MA_WIN).mean()
    v_ma = sub.notna() & ma.notna()
    tpers = float(_flip_persistence(sub > ma, v_ma).mean())
    mom, rk = mom_frame(sub)
    v_mom = sub.notna() & mom.notna()
    mompers = float(_flip_persistence(rk > 0.5, v_mom).mean())
    momsgn = float(_flip_persistence(mom > 0.0, v_mom).mean())
    acs = []
    for c in sub.columns:
        s = rk[c].where(v_mom[c]).dropna()
        if len(s) > 3 * AC_LAG:
            acs.append(float(s.corr(s.shift(AC_LAG))))
    momac = float(np.nanmean(acs)) if acs else np.nan
    return dict(cvol=vol, breadth=breadth, tpers=tpers, mompers=mompers, momsgn=momsgn,
                momac=momac)


def feasible_band(x):
    v = np.sort(np.asarray(x, float))
    return float(v[:K].mean()), float(v[-K:].mean())


def draw_panels(nc, bnames, snames, levels):
    """Kernel-weighted k=36 draws at each (characteristic, level, flavour, seed).  Idea 569's
    seed key, so the tpers draws are bit-identical to its committed ones."""
    out, feas = {}, []
    for char, lv in levels.items():
        ok_names = nc.index[nc[char].notna()]
        pools = {"POOL": list(ok_names),
                 "BONLY": [c for c in ok_names if c in bnames],
                 "SONLY": [c for c in ok_names if c in snames]}
        h = BW_MULT * float(nc[char].std())
        for fl in FLAVOURS:
            names = np.array(pools[fl])
            x = nc.loc[names, char].to_numpy()
            lo, hi = feasible_band(x)
            for L in lv:
                ok = lo <= L <= hi
                feas.append(dict(char=char, flavour=fl, level=L, reach_lo=lo, reach_hi=hi,
                                 feasible=ok, bandwidth=h, n_pool=len(names)))
                if not ok:
                    continue
                for sd in SEEDS:
                    seed = zlib.crc32(f"CHAR|{char}|{L:.6f}|{fl}|{sd}".encode()) % (2 ** 32)
                    rng = np.random.default_rng(seed)
                    w = np.exp(-0.5 * ((x - L) / h) ** 2)
                    w = w / w.sum()
                    pick = sorted(rng.choice(names, size=K, replace=False, p=w).tolist())
                    out[f"{char}~{fl}~L{L:.6f}~{sd}"] = dict(
                        names=pick, char=char, flavour=fl, level=L, seed=sd)
    return out, pd.DataFrame(feas)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 571  is-tpers-INFORMATION-or-TAUTOLOGY  (lane B, 2026-09-11)")
    P("=" * 118)
    P("Treatment = idea 51's MA-gate SELECTION premium, Sharpe(MA-RS) - Sharpe(EWall) at matched")
    P("(gross, cadence), on kernel-matched k=36 draws, k pinned.  10 bps, t+1 fills, no leverage.")
    P(f"Variables: tpers = the GATE'S OWN state persistence (REFERENCE, idea 569's winner);")
    P(f"           {NEW_CHARS} = persistence of the 12-1 MOMENTUM signal (NOT the gate's).")
    P(f"Pre-registered: GAP {GAP:.4f}  ORIGIN568 {ORIGIN568:.4f}  tpers POOL R2 {R2_TPERS:.6f} "
      f"slope {SLOPE_TPERS:+.6f} effect {EFF_TPERS:+.6f}")
    P(f"H_INFO bar for ANY variable: required sign AND |slope*span| >= {0.5*GAP:.4f} AND "
      f"R2 >= {0.5*R2_TPERS:.4f}.")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; every number below")
    P("inherits that bias and is a statement about surviving names, not a tradable 2010 list.")
    P("")

    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    for nm, (px, tr) in panels.items():
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, last bar {px.index.max().date()}")

    # ---------------------------------------------------------------- G2 identity
    P("")
    P("=" * 118)
    P("G2  IDENTITY GATE - fast_backtest vs engine.backtest")
    P("=" * 118)
    worst = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        d = float((a - b).abs().max())
        worst = max(worst, d)
        P(f"  {nm:9s} max |dreturn| {d:.3e}")
    assert worst < G2_TOL, f"G2 FAILED at {worst:.3e}"
    P(f"  G2 PASS ({worst:.3e} < {G2_TOL:.0e})")

    # ---------------------------------------------------------------- pooled frame
    P("")
    P("=" * 118)
    P("THE POOL - B136 + SMALL on the common index, four PERSISTENCE characteristics")
    P("=" * 118)
    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]

    old = old_name_chars(pool, spy_pool)          # idea 569's frame -> its exact name set
    pers = pers_name_chars(pool)
    nc = pers.reindex(old.index)
    P(f"  pooled index {ix.min().date()} .. {ix.max().date()}  ({len(ix)} bars)")
    P(f"  idea 569's pooled name set: {len(old)} names (index parity for G1)")
    # NaNs are kept in place and handled PER CHARACTERISTIC (a name with too little history for
    # one variable is simply not drawable on that variable's rungs).  Dropping them globally
    # would shift the pooled tpers quantiles and break G1's bit-for-bit parity with idea 569.
    for ch_ in CHARS:
        miss = sorted(nc.index[nc[ch_].isna()])
        if miss:
            P(f"  {ch_:9s} undefined on {len(miss)} name(s) - excluded from ITS rungs only: "
              + " ".join(miss))
    assert float((nc.tpers - old.tpers).abs().max()) < 1e-12, "tpers recompute differs"
    bnames, snames = set(bn) & set(nc.index), set(sn) & set(nc.index)
    P(f"  names used: B {len(bnames)}  SMALL {len(snames)}  total {len(nc)} "
      f"(per-char usable: " + ", ".join(f"{c} {int(nc[c].notna().sum())}" for c in CHARS) + ")")
    P("")
    P("  per-name characteristic distributions and k=36 REACH")
    P("  " + f"{'char':9s} {'B mean':>8s} {'S mean':>8s} {'sd':>8s} {'bw':>8s} "
        f"{'BONLY reach':>20s} {'SONLY reach':>20s} {'POOL reach':>20s}")
    LEVELS = {}
    for ch_ in CHARS:
        b_lo, b_hi = feasible_band(nc.loc[sorted(bnames), ch_].dropna())
        s_lo, s_hi = feasible_band(nc.loc[sorted(snames), ch_].dropna())
        p_lo, p_hi = feasible_band(nc[ch_].dropna())
        LEVELS[ch_] = [round(float(nc[ch_].quantile(q)), 6) for q in LEVEL_Q]
        P("  " + f"{ch_:9s} {nc.loc[sorted(bnames), ch_].mean():8.4f} "
            f"{nc.loc[sorted(snames), ch_].mean():8.4f} {nc[ch_].std():8.4f} "
            f"{BW_MULT*float(nc[ch_].std()):8.4f} [{b_lo:8.4f},{b_hi:8.4f}] "
            f"[{s_lo:8.4f},{s_hi:8.4f}] [{p_lo:8.4f},{p_hi:8.4f}]")
    P("")
    P("  PRE-REGISTERED rung levels (pooled 10/30/50/70/90th percentiles):")
    for ch_ in CHARS:
        P(f"    {ch_:9s} " + "  ".join(f"{v:.4f}" for v in LEVELS[ch_]))

    # H_INDEP: is a non-gate variable actually a different variable?
    P("")
    P("  H_INDEP - cross-name Spearman against tpers (bar: |rho| < %.2f to be independent)" % INDEP_BAR)
    indep, H_INDEP = [], {}
    for ch_ in CHARS:
        rho = spearman(nc[ch_], nc["tpers"])
        pear = pearson(nc[ch_], nc["tpers"])
        H_INDEP[ch_] = bool(abs(rho) < INDEP_BAR) if ch_ != "tpers" else False
        indep.append(dict(char=ch_, spearman_vs_tpers=rho, pearson_vs_tpers=pear,
                          independent=H_INDEP[ch_]))
        P(f"    {ch_:9s} Spearman {rho:+.4f}   Pearson {pear:+.4f}   independent "
          f"{str(H_INDEP[ch_]) if ch_ != 'tpers' else '(self)'}")
    IND = pd.DataFrame(indep)

    # ---------------------------------------------------- REAL panels on the common window
    P("")
    P("  REAL panels restated on the pooled window (premium re-measured there too):")
    pub = {}
    real_common = {}
    for nm, (px, tr) in panels.items():
        st0 = px.index[260]
        prem_full = []
        for g in GROSS:
            books = make_books(px, tr, g)
            for freq in CADENCE:
                rr = {k: fast_backtest(px, w, COST, freq)["returns"].loc[st0:] for k, w in books.items()}
                prem_full.append(metrics(rr["MA-RS"])["Sharpe"] - metrics(rr["EWall"])["Sharpe"])
        pub[nm] = float(np.mean(prem_full))
        pxc = px.reindex(ix).ffill()
        st = pxc.index[260]
        spy = pxc["SPY"].pct_change().fillna(0.0).loc[st:]
        ch = panel_chars(pxc, tr, spy)
        prem = []
        for g in GROSS:
            books = make_books(pxc, tr, g)
            for freq in CADENCE:
                rr = {k: fast_backtest(pxc, w, COST, freq)["returns"].loc[st:] for k, w in books.items()}
                prem.append(metrics(rr["MA-RS"])["Sharpe"] - metrics(rr["EWall"])["Sharpe"])
        real_common[nm] = dict(prem_common=float(np.mean(prem)), prem_full=pub[nm], **ch)
        P(f"    {nm:9s} tpers {ch['tpers']:.4f}  mompers {ch['mompers']:.4f}  "
          f"momsgn {ch['momsgn']:.4f}  momac {ch['momac']:+.4f}  "
          f"premium(full) {pub[nm]:+.4f}  premium(common) {np.mean(prem):+.4f}")
    gap_reread = float(pub["U56"] - pub[SMALLK])
    P(f"    U56 - {SMALLK} premium gap re-read (full): {gap_reread:+.4f}  (published GAP {GAP:.4f})")
    P(f"    U56 - {SMALLK} premium gap on the common window: "
      f"{real_common['U56']['prem_common'] - real_common[SMALLK]['prem_common']:+.4f}")

    P("")
    P("  REQUIRED SLOPE SIGN per characteristic (fixed by the three panels' OWN values, so that")
    P("  a monotone fit would reproduce the published U56 > B136 > SMALL premium ordering):")
    req_sign, panel_mono = {}, {}
    for ch_ in CHARS:
        u, b_, s_ = (real_common["U56"][ch_], real_common["B136"][ch_], real_common[SMALLK][ch_])
        mono = (u > b_ > s_) or (u < b_ < s_)
        req_sign[ch_] = float(np.sign(u - s_)) if u != s_ else 0.0
        panel_mono[ch_] = bool(mono)
        P(f"    {ch_:9s} U56 {u:+8.4f}  B136 {b_:+8.4f}  {SMALLK} {s_:+8.4f}   "
          f"panel-monotone {str(mono):5s}   required slope sign {req_sign[ch_]:+.0f}")

    # ---------------------------------------------------------------- draws
    P("")
    P("=" * 118)
    P("DRAWS - kernel-matched k=36 sub-panels")
    P("=" * 118)
    dr, FEAS = draw_panels(nc, bnames, snames, LEVELS)
    P(f"  rungs planned {len(FEAS)}, feasible {int(FEAS.feasible.sum())}, draws {len(dr)}")
    infeas = FEAS[~FEAS.feasible]
    if len(infeas):
        P("  INFEASIBLE rungs (flavour cannot reach the level with k=36):")
        for _, r in infeas.iterrows():
            P(f"    {r['char']:9s} {r['flavour']:6s} L={r['level']:9.4f}  "
              f"reach [{r['reach_lo']:.4f}, {r['reach_hi']:.4f}]")

    # ---------------------------------------------------------------- the ladder
    P("")
    P("=" * 118)
    P("THE LADDER - premium on kernel-matched k=36 draws (EVERY grid point in .grid.csv)")
    P("=" * 118)
    grid, chars = [], []
    for key, d in dr.items():
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
        tr = set(d["names"])
        st = pxd.index[260]
        spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
        ch = panel_chars(pxd, tr, spy)
        nb = sum(1 for c in d["names"] if c in bnames)
        chars.append(dict(panel=key, **{k: d[k] for k in ("char", "flavour", "level", "seed")},
                          n_from_B=nb, n_from_S=K - nb, **ch))
        for g in GROSS:
            books = make_books(pxd, tr, g)
            for freq in CADENCE:
                res = {k: fast_backtest(pxd, w, COST, freq) for k, w in books.items()}
                rets = {k: v["returns"].loc[st:] for k, v in res.items()}
                mc = metrics(rets["EWall"])
                mci = metrics(rets["EWall"].loc[:IS_END])["Sharpe"]
                mco = metrics(rets["EWall"].loc[OOS_START:])["Sharpe"]
                for k in books:
                    r = rets[k]
                    row = dict(panel=key, kind="DRAW", arm=k, gross=g, cadence=freq,
                               char=d["char"], flavour=d["flavour"], level=d["level"],
                               seed=d["seed"], achieved=ch[d["char"]], n_from_B=nb,
                               **{f"ach_{c}": ch[c] for c in CHARS})
                    row.update(rowify(r, res[k]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    row["dIS_Sharpe_vs_EWall"] = row["IS_Sharpe"] - mci
                    row["dOOS_Sharpe_vs_EWall"] = row["OOS_Sharpe"] - mco
                    row["keep4a"] = keep_4a(r, v2)
                    row["fail4b"] = fail_4b(r, spy)
                    row["keep4b"] = row["fail4b"] == "-"
                    grid.append(row)
    G = pd.DataFrame(grid)
    CH = pd.DataFrame(chars)
    P(f"  {len(dr)} draws x 2 arms x {len(GROSS)} gross x {len(CADENCE)} cadence = {len(G)} books "
      f"({time.time()-t0:.0f}s)")

    T = G[G.arm == "MA-RS"]
    draw_prem = T.groupby(["panel", "char", "flavour", "level", "seed"]).agg(
        premium=("dSharpe_vs_EWall", "mean"),
        prem_IS=("dIS_Sharpe_vs_EWall", "mean"),
        prem_OOS=("dOOS_Sharpe_vs_EWall", "mean"),
        achieved=("achieved", "first"), n_from_B=("n_from_B", "first")).reset_index()
    rung = draw_prem.groupby(["char", "flavour", "level"]).agg(
        n=("premium", "size"), achieved=("achieved", "mean"), n_from_B=("n_from_B", "mean"),
        premium=("premium", "mean"), sd=("premium", "std"),
        prem_IS=("prem_IS", "mean"), prem_OOS=("prem_OOS", "mean")).reset_index()
    P("")
    P("  RUNGS (premium = mean over 6 seeds x 3 gross x 2 cadence; sd = across seeds)")
    P("  " + f"{'char':9s} {'flavour':7s} {'L':>9s} {'achieved':>9s} {'nB/36':>6s} "
        f"{'premium':>9s} {'sd':>7s} {'IS':>8s} {'OOS':>8s}")
    for _, r in rung.iterrows():
        P("  " + f"{r['char']:9s} {r['flavour']:7s} {r['level']:9.4f} {r['achieved']:9.4f} "
            f"{r['n_from_B']:6.1f} {r['premium']:+9.4f} {r['sd']:7.4f} {r['prem_IS']:+8.4f} "
            f"{r['prem_OOS']:+8.4f}")
    floor_here = float(rung.sd.mean())
    P("")
    P(f"  NOISE FLOOR recomputed here: mean within-rung seed sd = {floor_here:.4f} "
      f"({floor_here/GAP:.2f}x the published GAP)")

    # ---------------------------------------------------------------- the fits
    P("")
    P("=" * 118)
    P("H_INFO  - does the premium order in the characteristic, and does the R2 SURVIVE off-gate?")
    P("=" * 118)
    slopes = []
    for ch_ in CHARS:
        for fl in FLAVOURS:
            d = draw_prem[(draw_prem.char == ch_) & (draw_prem.flavour == fl)]
            if d.level.nunique() < 3:
                continue
            a, b, r2 = ols(d.achieved, d.premium)
            span = float(d.achieved.max() - d.achieved.min())
            rr = rung[(rung.char == ch_) & (rung.flavour == fl)].sort_values("achieved")
            mono_dn = bool((rr.premium.diff().dropna() <= 0).all())
            mono_up = bool((rr.premium.diff().dropna() >= 0).all())
            eff = b * span
            slopes.append(dict(char=ch_, flavour=fl, n=len(d), intercept=a, slope=b, r2=r2,
                               span=span, effect=eff, sd_within=float(rr.sd.mean()),
                               ratio_to_GAP=abs(eff) / GAP, r2_vs_tpers=r2 / R2_TPERS,
                               mono_down=mono_dn, mono_up=mono_up, req_sign=req_sign[ch_],
                               sign_ok=bool(np.sign(b) == req_sign[ch_] and req_sign[ch_] != 0)))
    SL = pd.DataFrame(slopes)
    P("  " + f"{'char':9s} {'flavour':7s} {'n':>4s} {'slope':>10s} {'R2':>7s} {'R2/569':>7s} "
        f"{'span':>8s} {'slope*span':>11s} {'|eff|/GAP':>10s} {'sd_within':>10s} {'signOK':>7s} {'mono':>6s}")
    for _, r in SL.iterrows():
        mono = "down" if r["mono_down"] else ("up" if r["mono_up"] else "-")
        P("  " + f"{r['char']:9s} {r['flavour']:7s} {r['n']:4.0f} {r['slope']:+10.4f} "
            f"{r['r2']:7.4f} {r['r2_vs_tpers']:7.3f} {r['span']:8.4f} {r['effect']:+11.4f} "
            f"{r['ratio_to_GAP']:10.2f} {r['sd_within']:10.4f} {str(r['sign_ok']):>7s} {mono:>6s}")

    H_INFO, H_NOISE = {}, {}
    for ch_ in CHARS:
        row = SL[(SL.char == ch_) & (SL.flavour == "POOL")]
        if not len(row):
            H_INFO[ch_] = H_NOISE[ch_] = None
            continue
        row = row.iloc[0]
        H_INFO[ch_] = bool(row["sign_ok"] and abs(row["effect"]) >= 0.5 * GAP
                           and row["r2"] >= 0.5 * R2_TPERS)
        H_NOISE[ch_] = bool(abs(row["effect"]) > row["sd_within"])
    P("")
    for ch_ in CHARS:
        tag = "GATE'S OWN" if ch_ == "tpers" else "non-gate"
        P(f"  {ch_:9s} [{tag:10s}] H_INFO {str(H_INFO[ch_]):5s}   H_NOISE {str(H_NOISE[ch_]):5s}")
    H_TAUT = bool(H_INFO.get("tpers") is True
                  and not any(H_INFO.get(c) is True for c in NEW_CHARS))
    H_ANY_NEW = any(H_INFO.get(c) is True for c in NEW_CHARS)
    P("")
    P(f"  H_ANY_NEW (a NON-GATE persistence variable clears the same bar): "
      f"{'PASS' if H_ANY_NEW else 'FAIL'}")
    P(f"  H_TAUT (tpers clears it and no non-gate variable does): {'PASS' if H_TAUT else 'FAIL'}")

    # ---------------------------------------------------------------- G1 / G3
    P("")
    P("=" * 118)
    P("G1 / G3  REPRODUCTION GATES - idea 569's committed tpers ladder and origin gaps")
    P("=" * 118)
    pr = OUT / f"{PARENT}.rungs.csv"
    if pr.exists():
        p569 = pd.read_csv(pr)
        p569 = p569[p569.char == "tpers"]
        mine = rung[rung.char == "tpers"].merge(
            SL[SL.char == "tpers"], on=["char", "flavour"], suffixes=("", "_fit"))
        m = mine.merge(p569, on=["char", "flavour", "level"], suffixes=("", "_p"))
        cols = ["achieved", "premium", "sd", "slope", "r2", "span", "effect"]
        dmax = float(np.abs(m[cols].to_numpy(float) - m[[c + "_p" for c in cols]].to_numpy(float)).max())
        P(f"  tpers rungs matched {len(m)}/{len(p569)}   max |delta| over {cols} = {dmax:.3e}")
        for _, r in m.iterrows():
            P(f"    {r['flavour']:7s} L={r['level']:.6f}  premium here {r['premium']:+.6f} "
              f"vs committed {r['premium_p']:+.6f}   R2 {r['r2']:.6f} vs {r['r2_p']:.6f}")
        assert len(m) == len(p569), f"G1 FAILED: {len(m)}/{len(p569)} tpers rungs matched"
        assert dmax < G1_TOL, f"G1 FAILED at {dmax:.3e} (bar {G1_TOL:.0e})"
        sl_pool = SL[(SL.char == "tpers") & (SL.flavour == "POOL")].iloc[0]
        P(f"  tpers POOL slope {sl_pool['slope']:+.6f} (pre-registered {SLOPE_TPERS:+.6f}), "
          f"R2 {sl_pool['r2']:.6f} ({R2_TPERS:.6f}), effect {sl_pool['effect']:+.6f} ({EFF_TPERS:+.6f})")
        assert abs(sl_pool["slope"] - SLOPE_TPERS) < G1_TOL, "G1: tpers POOL slope moved"
        assert abs(sl_pool["r2"] - R2_TPERS) < G1_TOL, "G1: tpers POOL R2 moved"
        assert abs(sl_pool["effect"] - EFF_TPERS) < G1_TOL, "G1: tpers POOL effect moved"
        P("  G1 PASS - the reference ladder is idea 569's, bit-for-bit.")
    else:
        P("  G1 SKIPPED - idea 569's rungs.csv not present.")

    # ---------------------------------------------------------------- H_CARRIER
    P("")
    P("=" * 118)
    P("H_CARRIER  - at a MATCHED level, does the panel of ORIGIN stop mattering?")
    P("=" * 118)
    orig = []
    for ch_ in CHARS:
        for L in LEVELS[ch_]:
            d = rung[(rung.char == ch_) & (np.abs(rung.level - L) < 1e-9)].set_index("flavour")
            if not {"BONLY", "SONLY"} <= set(d.index):
                continue
            db, ds = d.loc["BONLY"], d.loc["SONLY"]
            sd_pair = float(np.sqrt((db["sd"] ** 2 + ds["sd"] ** 2) / 2))
            gap_bs = float(db["premium"] - ds["premium"])
            orig.append(dict(char=ch_, level=L, achieved_B=db["achieved"], achieved_S=ds["achieved"],
                             match_resid=float(db["achieved"] - ds["achieved"]),
                             prem_B=db["premium"], prem_S=ds["premium"], gap=gap_bs, sd_pair=sd_pair,
                             t=gap_bs / (sd_pair / np.sqrt(len(SEEDS))) if sd_pair > 0 else np.nan,
                             within_floor=abs(gap_bs) <= sd_pair,
                             ratio_to_GAP=gap_bs / GAP, ratio_to_568=gap_bs / ORIGIN568))
    OR = pd.DataFrame(orig)
    H_CARRIER = {}
    if len(OR):
        P("  " + f"{'char':9s} {'L':>9s} {'achB':>8s} {'achS':>8s} {'resid':>8s} {'premB':>8s} "
            f"{'premS':>8s} {'B-S':>8s} {'sd':>7s} {'t':>7s} {'/GAP':>7s} {'/568':>7s}")
        for _, r in OR.iterrows():
            P("  " + f"{r['char']:9s} {r['level']:9.4f} {r['achieved_B']:8.4f} {r['achieved_S']:8.4f} "
                f"{r['match_resid']:+8.4f} {r['prem_B']:+8.4f} {r['prem_S']:+8.4f} {r['gap']:+8.4f} "
                f"{r['sd_pair']:7.4f} {r['t']:+7.2f} {r['ratio_to_GAP']:+7.2f} {r['ratio_to_568']:+7.2f}")
        P("")
        for ch_ in CHARS:
            d = OR[OR.char == ch_]
            if not len(d):
                H_CARRIER[ch_] = None
                P(f"  {ch_:9s} NO OVERLAPPING RUNG - BONLY and SONLY reach disjoint level sets at k=36.")
                continue
            mg = float(d.gap.mean())
            H_CARRIER[ch_] = bool(d.within_floor.all() and abs(mg) < 0.5 * ORIGIN568)
            P(f"  {ch_:9s} H_CARRIER {str(H_CARRIER[ch_]):5s}   {int(d.within_floor.sum())}/{len(d)} "
              f"rungs inside the seed sd   mean B-S {mg:+.4f} = {mg/GAP:+.2f}x GAP = "
              f"{mg/ORIGIN568:+.2f}x idea 568")
        po = OUT / f"{PARENT}.origin.csv"
        if po.exists():
            o5 = pd.read_csv(po)
            o5 = o5[o5.char == "tpers"]
            mm = OR[OR.char == "tpers"].merge(o5, on=["char", "level"], suffixes=("", "_p"))
            gcols = ["prem_B", "prem_S", "gap", "sd_pair"]
            g3 = float(np.abs(mm[gcols].to_numpy(float) - mm[[c + "_p" for c in gcols]].to_numpy(float)).max()) \
                if len(mm) else np.nan
            P("")
            P(f"  G3  idea 569's committed tpers origin rows: matched {len(mm)}/{len(o5)}, "
              f"max |delta| {g3:.3e}")
            assert len(mm) == len(o5) and g3 < G3_TOL, f"G3 FAILED ({len(mm)}/{len(o5)}, {g3:.3e})"
            P("  G3 PASS.")
    else:
        for ch_ in CHARS:
            H_CARRIER[ch_] = None
        P("  NO OVERLAPPING RUNG on any characteristic.")

    # ---------------------------------------------------------------- RULE 8
    P("")
    P("=" * 118)
    P("RULE 8 WALK-FORWARD   IS <= %s, OOS >= %s (read once)" % (IS_END, OOS_START))
    P("=" * 118)
    wf = []
    P("  WF-A  every slope refit inside each window")
    P("  " + f"{'char':9s} {'flavour':7s} {'slope_IS':>10s} {'R2_IS':>7s} {'slope_OOS':>10s} "
        f"{'R2_OOS':>7s} {'slope_full':>11s} {'sign holds':>11s}")
    for ch_ in CHARS:
        for fl in FLAVOURS:
            d = draw_prem[(draw_prem.char == ch_) & (draw_prem.flavour == fl)]
            if d.level.nunique() < 3:
                continue
            _, b_is, r2_is = ols(d.achieved, d.prem_IS)
            _, b_oos, r2_oos = ols(d.achieved, d.prem_OOS)
            _, b_full, r2_full = ols(d.achieved, d.premium)
            hold = bool(np.sign(b_is) == np.sign(b_oos))
            wf.append(dict(leg="WF-A", char=ch_, flavour=fl, slope_IS=b_is, r2_IS=r2_is,
                           slope_OOS=b_oos, r2_OOS=r2_oos, slope_full=b_full, sign_hold=hold))
            P("  " + f"{ch_:9s} {fl:7s} {b_is:+10.4f} {r2_is:7.3f} {b_oos:+10.4f} {r2_oos:7.3f} "
                f"{b_full:+11.4f} {str(hold):>11s}")
    WFA = pd.DataFrame([w for w in wf if w["leg"] == "WF-A"])
    P(f"  sign holds IS -> OOS in {int(WFA.sign_hold.sum())}/{len(WFA)} (char, flavour) cells")
    pw = WFA[WFA.flavour == "POOL"].set_index("char")
    P("  POOL R2 ordering of the four variables:")
    P("    IS  : " + "  ".join(f"{c} {pw.loc[c, 'r2_IS']:.3f}" for c in CHARS if c in pw.index))
    P("    OOS : " + "  ".join(f"{c} {pw.loc[c, 'r2_OOS']:.3f}" for c in CHARS if c in pw.index))
    tpers_top_is = bool(all(pw.loc["tpers", "r2_IS"] >= pw.loc[c, "r2_IS"]
                            for c in NEW_CHARS if c in pw.index))
    tpers_top_oos = bool(all(pw.loc["tpers", "r2_OOS"] >= pw.loc[c, "r2_OOS"]
                             for c in NEW_CHARS if c in pw.index))
    P(f"    tpers has the highest POOL R2: IS {tpers_top_is}, OOS {tpers_top_oos}")

    P("")
    P("  WF-B  a BOOK: pick (char, level) by IS Sharpe of the seed-pooled MA-RS book at g=0.75/W, POOL")
    sel = G[(G.arm == "MA-RS") & (G.gross == 0.75) & (G.cadence == "W") & (G.flavour == "POOL")]
    pick_tbl = sel.groupby(["char", "level"]).agg(IS_Sharpe=("IS_Sharpe", "mean"),
                                                  OOS_Sharpe=("OOS_Sharpe", "mean")).reset_index()
    for _, r in pick_tbl.sort_values("IS_Sharpe", ascending=False).iterrows():
        P(f"    {r['char']:9s} L={r['level']:9.4f}  IS {r['IS_Sharpe']:+.4f}   (OOS {r['OOS_Sharpe']:+.4f})")
    best = pick_tbl.sort_values("IS_Sharpe", ascending=False).iloc[0]
    oos_best = pick_tbl.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P(f"    PICK (IS only): {best['char']} L={best['level']:.4f}   "
      f"| OOS winner was {oos_best['char']} L={oos_best['level']:.4f} "
      f"(OOS {oos_best['OOS_Sharpe']:+.4f})")

    keys_pick = [k for k, d in dr.items()
                 if d["char"] == best["char"] and abs(d["level"] - best["level"]) < 1e-9
                 and d["flavour"] == "POOL"]
    rets_pick = []
    for key in keys_pick:
        d = dr[key]
        pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
        st = pxd.index[260]
        w = make_books(pxd, set(d["names"]), 0.75)["MA-RS"]
        rets_pick.append(fast_backtest(pxd, w, COST, "W")["returns"].loc[st:])
    RP = pd.concat(rets_pick, axis=1).fillna(0.0).mean(axis=1)
    st_b = pxB.index[260]
    b136_v2 = backtest(pxB, rules_v2_weights(pxB), cost_bps=COST, freq="W")["returns"].loc[st_b:] \
        .reindex(RP.index).fillna(0.0)
    spy_r = spy_pool.pct_change().fillna(0.0).reindex(RP.index).fillna(0.0)
    P("")
    P("  " + f"{'book':28s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
        f"{'OOS_CAGR':>9s} {'OOS_Sh':>8s} {'OOS_DD':>8s}")
    wfb = []
    for nm, r in (("WF-B pick (seed-pooled)", RP), ("RULES v2 (B136)", b136_v2), ("SPY", spy_r)):
        d = rowify(r)
        wfb.append(dict(leg="WF-B", book=nm, **d))
        P("  " + f"{nm:28s} {d['CAGR']:8.2%} {d['Sharpe']:8.3f} {d['MaxDD']:8.2%} {d['H1']:7.3f} "
            f"{d['H2']:7.3f} {d['OOS_CAGR']:9.2%} {d['OOS_Sharpe']:8.3f} {d['OOS_MaxDD']:8.2%}")
    wfb_4a = keep_4a(RP, b136_v2)
    wfb_4b = fail_4b(RP, spy_r)
    P(f"  WF-B 4a vs RULES v2 (B136): {wfb_4a}    4b fail legs vs SPY: {wfb_4b}")

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 118)
    P("KEEP PATHS over every book (4a vs RULES v2 on the SAME panel, 4b vs SPY)")
    P("=" * 118)
    P(f"  books: {len(G)} DRAW books")
    P(f"  4a passes {int(G.keep4a.sum())}/{len(G)}   4b passes {int(G.keep4b.sum())}/{len(G)}   "
      f"BOTH {int((G.keep4a & G.keep4b).sum())}/{len(G)}")
    legs = pd.Series([x for s in G.loc[~G.keep4b, "fail4b"] for x in s.split(",")]).value_counts()
    P("  binding 4b legs: " + "  ".join(f"{k} {v}" for k, v in legs.items()))
    if int(G.keep4b.sum()):
        P("  4b passers by arm: " + "  ".join(f"{k} {v}" for k, v in G[G.keep4b].arm.value_counts().items()))
        P("  4b passers by char: " + "  ".join(f"{k} {v}" for k, v in G[G.keep4b].char.value_counts().items()))
        bb = G[G.keep4b].sort_values("Sharpe", ascending=False).head(5)
        P("  top 4b passers (DIAGNOSTIC ONLY - a kernel draw is not a tradable rule):")
        for _, r in bb.iterrows():
            P(f"    {str(r['panel'])[:38]:38s} {r['arm']:6s} g={r['gross']:.2f} {r['cadence']}  "
              f"CAGR {r['CAGR']:6.2%}  Sh {r['Sharpe']:.3f}  DD {r['MaxDD']:7.2%}  "
              f"H1/H2 {r['H1']:.2f}/{r['H2']:.2f}  OOS {r['OOS_Sharpe']:.3f}")
    KP = G[["panel", "kind", "arm", "gross", "cadence", "char", "flavour", "level", "seed",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "keep4a", "fail4b", "keep4b"]]

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    P("  " + f"{'char':9s} {'gate?':6s} {'R2':>7s} {'R2/569':>7s} {'|eff|/GAP':>10s} {'signOK':>7s} "
        f"{'H_INFO':>7s} {'H_INDEP':>8s} {'H_CARRIER':>10s}")
    for ch_ in CHARS:
        row = SL[(SL.char == ch_) & (SL.flavour == "POOL")]
        if not len(row):
            P(f"  {ch_:9s} no POOL fit")
            continue
        row = row.iloc[0]
        P("  " + f"{ch_:9s} {'YES' if ch_ == 'tpers' else 'no':6s} {row['r2']:7.4f} "
            f"{row['r2_vs_tpers']:7.3f} {row['ratio_to_GAP']:10.2f} {str(row['sign_ok']):>7s} "
            f"{str(H_INFO.get(ch_)):>7s} "
            f"{('(self)' if ch_ == 'tpers' else str(H_INDEP.get(ch_))):>8s} "
            f"{str(H_CARRIER.get(ch_)):>10s}")
    P("")
    if H_TAUT:
        P("  ANSWER: TAUTOLOGY.  The R2 does NOT survive when the persistence variable is not the")
        P("  gate's own state: tpers clears the bar and no non-gate persistence variable does.")
    elif H_ANY_NEW:
        passers = [c for c in NEW_CHARS if H_INFO.get(c) is True]
        P(f"  ANSWER: INFORMATION (at least partly).  {passers} clear the same bar off-gate.")
        P("  Check H_INDEP above before reading that as independent evidence.")
    else:
        P("  ANSWER: NEITHER CLEARS THE BAR on this run's draws - tpers itself failed to "
          "reproduce its own H_INFO, which would be a G1 failure; read the gates above.")

    # ---------------------------------------------------------------- outputs
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    rung.merge(SL, on=["char", "flavour"], how="left", suffixes=("", "_fit")).to_csv(
        OUT / f"{STAMP}.rungs.csv", index=False)
    (OR if len(OR) else pd.DataFrame(columns=["char"])).to_csv(OUT / f"{STAMP}.origin.csv", index=False)
    pd.concat([pd.DataFrame(wf), pd.DataFrame(wfb)], ignore_index=True, sort=False).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    CH.merge(FEAS, on=["char", "flavour", "level"], how="left").to_csv(OUT / f"{STAMP}.chars.csv", index=False)
    IND.to_csv(OUT / f"{STAMP}.independence.csv", index=False)
    nc.to_csv(OUT / f"{STAMP}.namechars.csv")
    P("")
    P(f"  wrote {STAMP}.{{grid,rungs,origin,walkforward,keeppaths,chars,independence,namechars}}.csv "
      f"({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
