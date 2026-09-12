#!/usr/bin/env python3
"""Idea 796 (cloud, 2026-09-11) - is-momac-s-0.0549-MATCHED-LEVEL-GAP-real-or-a-MATCHING-RESIDUAL.

QUESTION
--------
Idea 571 ran four PERSISTENCE characteristics through idea 569's kernel-matched k=36 draw ladder
and measured, at each matched rung, the premium a BONLY-sourced sub-panel earns over a SONLY-sourced
one.  `momac` (lag-21 autocorrelation of a name's 12-1 momentum rank_pct) produced the SMALLEST
matched-level gap on this machinery to date: mean |B-S| **0.0549 = 0.28x idea 568's ORIGIN568
0.1961**, with 3 of its 4 overlapping rungs inside the within-rung seed floor.

But momac's rungs are also the LOOSEST-matched of the four.  Idea 571's committed `.origin.csv`
reads a mean |achieved_B - achieved_S| of **0.0152** on momac against **0.0017** on tpers - a factor
of 9.1.  A small premium gap between two arms that are not actually at the same level of the
characteristic is not absorption; it is a matching residual.  Idea 798 sharpened the lead from the
other side: `volpers`, the tightest-matched reading on this machinery (residual 0.0007, 22x tighter
than momac's), lands at a LARGER gap (0.0655) - which is what one expects if loose matching biases
the gap DOWNWARD here.

This run re-opens momac's match.  The kernel bandwidth h = BW * sd(char) is what decides how far a
draw's achieved level may wander from its target, so SHRINKING BW tightens the match directly; and
adding RUNGS both tests more of the level axis and stops a 4-rung mean from being an accident of
which 4 rungs the k=36 reach happened to admit.

A VINTAGE PROBLEM, STATED BEFORE ANY RESULT
-------------------------------------------
Idea 571's exact numbers are NOT reproducible from today's repository, and not because of anything
this run does.  Its pooled name set (committed in its `.namechars.csv`, 573 names: B 134 + SMALL
439) no longer exists as such:
  * 9 of its 573 names are absent from today's `data/prices_small.csv` / `prices_broad.csv`;
  * the surviving names' own characteristics have moved on re-stated adjusted closes - a pilot of
    this file's code measured max |d tpers| 1.0e-03 and max |d momac| 1.1e-02 against idea 571's
    committed per-name values, on the SAME estimator;
  * `data/prices_small.csv` now carries 715 columns (663 tradable after PROTOCOL's max_1d_move
    filter) against idea 571's 440/439, so every pooled quantile - i.e. every rung LEVEL - moves.
This is idea 565's nightly-rewritten-input pathology reaching the price panel itself.  A 1e-9
reproduction gate on idea 571's rows would therefore fail for a reason that has nothing to do with
momac, so this run does NOT pretend to one.  Instead:
  * G2/G3 MEASURE the vintage drift (per-name and at idea 571's own anchor cell) and publish it;
  * the bandwidth ladder is anchored on THIS RUN'S OWN BW=0.500 / Q5 cell, rebuilt here on today's
    data with idea 571's estimator, seed key and draw size, so every comparison inside this file
    is within one internally consistent vintage;
  * the FROZEN survivors of idea 571's committed name set are run as a SECOND vintage, so the
    answer can be read as panel-dependent or not.
This departure was decided after the anchor cell was rebuilt and BEFORE any narrowed-bandwidth
number was read.  Said plainly: the number under test is re-measured here, not taken on trust.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: bandwidth, rungs)
    1. BW      in {0.500, 0.250, 0.125}      0.500 = idea 569/571's value, kept as the anchor
    2. RUNGS   in {Q5, Q9, Q19}
         Q5  = idea 571's pre-registered {0.10, 0.30, 0.50, 0.70, 0.90}        (the anchor)
         Q9  = {0.10, 0.20, ..., 0.90}
         Q19 = {0.05, 0.10, ..., 0.95}
       Q5 subset Q9 subset Q19, so the three rung sets read the same draws and the wider ones cost
       no extra backtest - stated, not hidden.
All 3 x 3 = 9 grid points are reported.  REPORTED-NEVER-SELECTED axes: panel vintage (LIVE, FROZEN),
characteristic (momac, plus `tpers` as idea 571's REFERENCE control - the variable whose 0.0017
residual is the queue's target - run at the same three bandwidths so a bandwidth effect can be told
apart from a momac-specific one), flavour in {POOL, BONLY, SONLY}, seed in 0..5, gross in
{0.50, 0.75, 1.00}, cadence in {W, M}, window in {FULL, IS, OOS}.  Nothing is picked on any of them.

PRE-REGISTERED HYPOTHESES (written before any narrowed-bandwidth number was read)
    H_TIGHTEN: the premise.  Narrowing the bandwidth tightens the match - momac's mean |resid| over
               the anchor rung set is monotone DECREASING in BW, and at BW=0.125 it is at or below
               tpers's committed 0.0017 (the queue's own target).
    H_SMALL  : the charitable reading.  At the TIGHTEST-MATCHED cell (chosen on |resid| ALONE, never
               on the gap) momac's mean |B-S| gap stays below idea 569/571's carrier bar
               0.5 x ORIGIN568 = 0.0981.
    H_RUNGS  : the smallness is not a 4-rung accident - momac's mean |B-S| on the FULL Q19 rung set
               is also below 0.0981.
    H_FLOOR  : the smallness survives in FLOOR units - |gap| / mean sd_pair at the tightest cell is
               no more than 1.25x its value at this run's BW=0.500 / Q5 anchor.  (A narrower kernel
               draws from fewer effective names, so the seed floor can grow; without this leg a gap
               could look "inside the floor" merely because the floor moved.)
    H_GROW   : idea 798's directional lead - momac's mean |gap| at the tightest cell EXCEEDS this
               run's own BW=0.500 / Q5 anchor, i.e. loose matching was biasing the gap downward.
    H_RESID  : the queue's alternative (the small gap is a matching residual, not absorption).
               CONFIRMED exactly when H_SMALL fails.

GATES (run and printed BEFORE any new number is read)
    G0 determinism : every draw rebuilt twice gives identical name sets at every BW.        bar 0
    G1 identity    : fast_backtest vs engine.backtest on one book per real panel.        bar 1e-9
    G2 VINTAGE     : idea 571's committed per-name tpers/momac vs the same estimator on today's
                     prices - MEASURED and published, no bar (see above).
    G3 ANCHOR      : idea 571's committed momac/tpers origin rows vs this run's BW=0.500 / Q5 cell
                     on both vintages - MEASURED and published, no bar.

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: the matched-level gap is recomputed on IS and on OOS separately at every
       (vintage, char, BW, rung set), so "is the gap small once matched" is answered in each window
       and the IS->OOS drift of the verdict is reported.
    WF-B on a BOOK: the absorption claim taken as a trading instruction - "at matched momac the
       panel of origin does not matter, so hold whichever flavour is available".  Among the
       overlapping rungs only, (flavour, level, seed, gross, cadence) is chosen by IS Sharpe ALONE,
       then OOS CAGR / Sharpe / MaxDD are read ONCE against live RULES v2 on U56 and against SPY.
       The BONLY-vs-SONLY OOS head-to-head over the same rungs is reported beside it, because that
       is the contrast the claim is actually about.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY book
    and the counts reported.  Stated up front: every panel here is a kernel-weighted seeded draw,
    not a rule anyone can trade, so a 4b pass on this ladder is a diagnostic, never a capital
    candidate, and none is claimed as one.

SURVIVORSHIP: the pool is B136 (current constituents of universe_broad.json) plus the sub-$2B panel
    (current constituents of its screen, every ticker with max_1d_move >= 1.0 in data/small_meta.csv
    dropped first, per PROTOCOL).  SMALL names that died are absent, so the S-sourced premium is
    biased UPWARD, which SHRINKS the B-S gap this run measures - the bias works in favour of
    H_SMALL and AGAINST the queue's matching-residual reading.  The FROZEN vintage is worse, not
    better, on this axis: it is idea 571's already-survivorship-screened set minus 9 more names that
    have since left the data.  Said again beside the result.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and idea 571's committed
artefacts; modifies nothing but its own outputs:
    .grid.csv .rungs.csv .origin.csv .summary.csv .feas.csv .walkforward.csv .keeppaths.csv
    .chars.csv .vintage.csv .console.txt
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

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
MOM_LAG, MOM_LOOK = 21, 252          # 12-1 momentum, scan.py's definition
AC_LAG = 21                          # momac: lag-21 autocorrelation of the momentum rank
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"            # idea 571's last bar
K = 36                               # idea 569/571's draw size, NOT re-tuned (that was idea 572)
SEEDS = [0, 1, 2, 3, 4, 5]
FLAVOURS = ["POOL", "BONLY", "SONLY"]
CHARS = ["momac", "tpers"]           # momac = the question; tpers = idea 571 REFERENCE control
BW_SET = [0.500, 0.250, 0.125]       # TUNED 1
BW_ANCHOR = 0.500
LEVEL_Q5 = [0.10, 0.30, 0.50, 0.70, 0.90]
LEVEL_Q9 = [round(0.10 * i, 2) for i in range(1, 10)]
LEVEL_Q19 = [round(0.05 * i, 2) for i in range(1, 20)]
LEVELSETS = {"Q5": LEVEL_Q5, "Q9": LEVEL_Q9, "Q19": LEVEL_Q19}
# what is actually DRAWN, per vintage and characteristic (kept bounded; supersets are free)
DRAWN_Q = {"LIVE": {"momac": LEVEL_Q19, "tpers": LEVEL_Q9},
           "FROZEN": {"momac": LEVEL_Q5}}
ANCHOR_LS = "Q5"                     # idea 571's rung set - the within-vintage anchor
ORIGIN568 = 0.1961                   # idea 568's mean matched-level B-S gap
GAP = 0.0978                         # idea 51's published U56 - SMALL439 premium gap
CARRIER_BAR = 0.5 * ORIGIN568        # idea 569/571's carrier bar, re-used verbatim
MOMAC571_ABSGAP = 0.0549             # idea 571's committed momac mean |B-S| (the object of this run)
MOMAC571_RESID = 0.0152              # idea 571's committed momac mean |match residual|
TPERS571_RESID = 0.0017              # idea 571's committed tpers mean |match residual| - the target
PARENT571 = OUT / "2026-09-11_is-tpers-INFORMATION-or-TAUTOLOGY_B"
TOL = 1e-9

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
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


# ------------------------------------------------------------------------- panels / pool
def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }, len(bad)


# ------------------------------------------------ per-NAME characteristics (idea 571, verbatim)
def _flip_persistence(state, valid):
    st = state.where(valid)
    flips = st.astype(float).diff().abs().where(valid & valid.shift(1))
    denom = (valid & valid.shift(1)).sum().replace(0, np.nan)
    return (1.0 - flips.sum() / denom).astype(float)


def mom_frame(pool):
    mom = pool.shift(MOM_LAG) / pool.shift(MOM_LOOK) - 1.0
    return mom, mom.rank(axis=1, pct=True)


def pers_name_chars(pool):
    """Idea 571's tpers and momac, verbatim.  momac's rank is cross-sectional WITHIN the pool, so
    it is a property of the pool as well as of the name - which is why the vintage matters."""
    ma = pool.rolling(MA_WIN).mean()
    v_ma = pool.notna() & ma.notna()
    tpers = _flip_persistence(pool > ma, v_ma)
    mom, rk = mom_frame(pool)
    v_mom = pool.notna() & mom.notna()
    ac = {}
    for c in pool.columns:
        s = rk[c].where(v_mom[c]).dropna()
        ac[c] = float(s.corr(s.shift(AC_LAG))) if len(s) > 3 * AC_LAG else np.nan
    return pd.DataFrame(dict(tpers=tpers, momac=pd.Series(ac, dtype=float)))


def panel_chars(px, tradable):
    """Panel-level momac and tpers (equal-weight over constituents), idea 571's estimator."""
    cols = [c for c in px.columns if c in tradable]
    sub = px[cols]
    r = sub.pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    ma = sub.rolling(MA_WIN).mean()
    v_ma = sub.notna() & ma.notna()
    tpers = float(_flip_persistence(sub > ma, v_ma).mean())
    mom, rk = mom_frame(sub)
    v_mom = sub.notna() & mom.notna()
    acs = []
    for c in sub.columns:
        s = rk[c].where(v_mom[c]).dropna()
        if len(s) > 3 * AC_LAG:
            acs.append(float(s.corr(s.shift(AC_LAG))))
    return dict(cvol=vol, tpers=tpers, momac=float(np.nanmean(acs)) if acs else np.nan)


def feasible_band(x):
    v = np.sort(np.asarray(x, float))
    return float(v[:K].mean()), float(v[-K:].mean())


def draw_panels(vint, nc, bnames, snames, levels, bw):
    """Idea 571's kernel-weighted k=36 draw scheme, with the BANDWIDTH as the free dial and its
    seed key kept verbatim."""
    out, feas = {}, []
    for char, lv in levels.items():
        ok_names = nc.index[nc[char].notna()]
        pools = {"POOL": list(ok_names),
                 "BONLY": [c for c in ok_names if c in bnames],
                 "SONLY": [c for c in ok_names if c in snames]}
        h = bw * float(nc[char].std())
        for fl in FLAVOURS:
            names = np.array(pools[fl])
            x = nc.loc[names, char].to_numpy()
            lo, hi = feasible_band(x)
            for L in lv:
                ok = bool(lo <= L <= hi)
                feas.append(dict(vint=vint, char=char, BW=bw, flavour=fl, level=L, reach_lo=lo,
                                 reach_hi=hi, feasible=ok, bandwidth=h, n_pool=len(names)))
                if not ok:
                    continue
                for sd in SEEDS:
                    seed = zlib.crc32(f"CHAR|{char}|{L:.6f}|{fl}|{sd}".encode()) % (2 ** 32)
                    rng = np.random.default_rng(seed)
                    w = np.exp(-0.5 * ((x - L) / h) ** 2)
                    w = w / w.sum()
                    pick = sorted(rng.choice(names, size=K, replace=False, p=w).tolist())
                    out[f"{vint}~{char}~{fl}~L{L:.6f}~{sd}~bw{bw:.3f}"] = dict(
                        names=pick, vint=vint, char=char, flavour=fl, level=L, seed=sd, BW=bw)
    return out, pd.DataFrame(feas)


def main():
    t0 = time.time()
    P("=" * 120)
    P(f"# {STAMP}")
    P("# IDEA 796 - is momac's +0.0549 matched-level B-S gap real absorption, or the residual of a")
    P("#            loose match?  Tighten the kernel (bandwidth), add rungs, then re-read it.")
    P("=" * 120)
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}, "
      f"sample truncated at {PARENT_END} (idea 571's last bar)")
    P("# TUNED (2): BW in {0.500, 0.250, 0.125} x RUNGS in {Q5, Q9, Q19}.  Q5 c Q9 c Q19, so the")
    P("#            three rung sets read the same draws.  REPORTED-NOT-SELECTED: panel vintage,")
    P("#            characteristic (momac + tpers control), flavour, seed, gross, cadence, window.")
    P("")
    P("# VINTAGE WARNING (stated before any result): idea 571's exact rows are NOT reproducible")
    P("#   from today's repository - 9 of its 573 pooled names have left the data, the survivors'")
    P("#   characteristics have moved on re-stated adjusted closes, and data/prices_small.csv now")
    P("#   carries 715 columns against its 440, which moves every pooled quantile (= every rung).")
    P("#   G2/G3 therefore MEASURE that drift instead of gating on it, and the bandwidth ladder is")
    P("#   anchored on THIS RUN'S OWN BW=0.500 / Q5 cell so every comparison is within one vintage.")
    P("")
    P(f"PRE-REGISTERED: H_TIGHTEN (momac |resid| monotone decreasing in BW and <= "
      f"{TPERS571_RESID:.4f} at BW=0.125), H_SMALL (|gap| at the tightest-matched cell < carrier")
    P(f"  bar {CARRIER_BAR:.4f}), H_RUNGS (|gap| on the full Q19 rung set also < {CARRIER_BAR:.4f}),")
    P("  H_FLOOR (|gap|/floor there <= 1.25x the anchor's), H_GROW (idea 798's lead: |gap| there")
    P("  EXCEEDS the anchor's), H_RESID (= not H_SMALL).")
    P("")

    panels, n_bad = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    P("PANELS: " + ", ".join(f"{k} ({len([c for c in v[0].columns if c in v[1] and c!='SPY'])} "
                            f"tradable, ..{v[0].index[-1].date()})" for k, v in panels.items()))
    P(f"  small panel: {n_bad} tickers with max_1d_move >= 1.0 dropped per PROTOCOL")
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; dead SMALL names are")
    P("  absent, so the S-sourced premium is biased UPWARD and the B-S gap measured here is biased")
    P("  DOWNWARD - the bias favours H_SMALL and works AGAINST the matching-residual reading.")
    P("")

    # ---------------------------------------------------------------- the pools (two vintages)
    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn_all = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn_all = sorted([c for c in pxS.columns if c in trS])
    pool_all = pd.concat([pxB.loc[ix, bn_all], pxS.loc[ix, sn_all]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]

    nc571 = pd.read_csv(f"{PARENT571}.namechars.csv", index_col=0)
    keep571 = [n for n in nc571.index if n in pool_all.columns]
    gone571 = [n for n in nc571.index if n not in pool_all.columns]

    POOLS = {}
    for vint, cols in (("LIVE", bn_all + sn_all), ("FROZEN", keep571)):
        pl = pool_all[[c for c in cols]]
        nc = pers_name_chars(pl)
        bnames = set(bn_all) & set(nc.index)
        snames = set(sn_all) & set(nc.index)
        POOLS[vint] = dict(pool=pl, nc=nc, bnames=bnames, snames=snames)
        P(f"POOL {vint:6s}: {ix.min().date()}..{ix.max().date()} ({len(ix)} bars); "
          f"B {len(bnames)} + SMALL {len(snames)} = {len(nc)} names (usable: "
          + ", ".join(f"{c} {int(nc[c].notna().sum())}" for c in CHARS) + ")")
    P(f"  FROZEN = idea 571's committed 573-name pool minus the {len(gone571)} names no longer in "
      f"the data: {' '.join(gone571)}")
    LEVELS = {v: {c: {ls: [round(float(POOLS[v]['nc'][c].quantile(q)), 6) for q in qs]
                      for ls, qs in LEVELSETS.items()} for c in CHARS} for v in POOLS}
    DRAWLEV = {v: {c: [round(float(POOLS[v]['nc'][c].quantile(q)), 6) for q in qs]
                   for c, qs in DRAWN_Q[v].items()} for v in POOLS}
    for v in POOLS:
        for c in DRAWLEV[v]:
            sd_ = float(POOLS[v]["nc"][c].std())
            P(f"  {v:6s} {c:6s} sd {sd_:.4f}; bandwidths " +
              " ".join(f"{bw:.3f}->{bw*sd_:.4f}" for bw in BW_SET))
            P(f"  {'':6s} {'':6s} drawn rungs ({len(DRAWLEV[v][c])}): " +
              " ".join(f"{x:.4f}" for x in DRAWLEV[v][c]))
    P("")

    # ---------------------------------------------------------------- gates G0/G1/G2
    P("=" * 120)
    P("GATES (printed before any new number is read)")
    P("=" * 120)
    g0 = nd = 0
    for v in POOLS:
        for bw in BW_SET:
            a, _ = draw_panels(v, POOLS[v]["nc"], POOLS[v]["bnames"], POOLS[v]["snames"],
                               DRAWLEV[v], bw)
            b, _ = draw_panels(v, POOLS[v]["nc"], POOLS[v]["bnames"], POOLS[v]["snames"],
                               DRAWLEV[v], bw)
            nd += len(a)
            g0 += sum(0 if set(a[k]["names"]) == set(b[k]["names"]) else 1 for k in a)
    P(f"G0 determinism : {g0} of {nd} draws differ on rebuild (bar 0) -> "
      f"{'PASS' if g0 == 0 else 'FAIL'}")
    g1 = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float((a - b).abs().max()))
    P(f"G1 identity    : fast_backtest vs engine.backtest max |dret| = {g1:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1 <= TOL else 'FAIL'}")

    vrows = []
    P(f"G2 VINTAGE     : idea 571's committed per-name values vs the same estimator today "
      f"({len(keep571)} survivors of {len(nc571)})")
    for v in POOLS:
        nc = POOLS[v]["nc"]
        for c in CHARS:
            a = nc[c].reindex(keep571)
            b = nc571[c].reindex(keep571)
            d = (a - b).abs()
            vrows.append(dict(leg="per-name", vint=v, char=c, n=int(d.notna().sum()),
                              max_abs_d=float(d.max()), mean_abs_d=float(d.mean()),
                              rho=float(pd.concat([a, b], axis=1).dropna().corr().iloc[0, 1])))
            P(f"   {v:6s} {c:6s} max |d| {float(d.max()):.3e}  mean |d| {float(d.mean()):.3e}  "
              f"rho {vrows[-1]['rho']:.6f}")
    P("   -> exact reproduction of idea 571 is UNREACHABLE on today's data; the ladder below is")
    P("      anchored within vintage instead.  (G3 reads the anchor cell itself, after the ladder.)")
    P("")

    # ---------------------------------------------------------------- reach / feasibility
    P("=" * 120)
    P("REACH AND FEASIBILITY (the k=36 reach band does not move with BW - only the match does)")
    P("=" * 120)
    DR, allfeas = {}, []
    for v in POOLS:
        for bw in BW_SET:
            d, f = draw_panels(v, POOLS[v]["nc"], POOLS[v]["bnames"], POOLS[v]["snames"],
                               DRAWLEV[v], bw)
            DR[(v, bw)] = d
            allfeas.append(f)
    FE = pd.concat(allfeas, ignore_index=True)
    P(f"  {'vint':6s} {'char':6s} {'flavour':7s} {'reach_lo':>9s} {'reach_hi':>9s} {'drawn':>6s} "
      f"{'feasible':>9s}")
    for v in POOLS:
        for c in DRAWLEV[v]:
            for fl in FLAVOURS:
                r = FE[(FE.vint == v) & (FE.char == c) & (FE.flavour == fl) & (FE.BW == BW_ANCHOR)]
                P(f"  {v:6s} {c:6s} {fl:7s} {r.reach_lo.iloc[0]:9.4f} {r.reach_hi.iloc[0]:9.4f} "
                  f"{len(r):6d} {int(r.feasible.sum()):9d}")
    P("")
    P("  OVERLAPPING RUNGS (both BONLY and SONLY feasible) per tuned rung set")
    for v in POOLS:
        for c in DRAWLEV[v]:
            for ls in LEVELSETS:
                lv = LEVELS[v][c][ls]
                if not set(lv) <= set(DRAWLEV[v][c]):
                    P(f"    {v:6s} {c:6s} {ls:4s} {len(lv):3d} levels -> NOT DRAWN")
                    continue
                r = FE[(FE.vint == v) & (FE.char == c) & (FE.BW == BW_ANCHOR) & FE.level.isin(lv)]
                ok = {fl: set(r[(r.flavour == fl) & r.feasible].level) for fl in FLAVOURS}
                P(f"    {v:6s} {c:6s} {ls:4s} {len(lv):3d} levels -> overlap "
                  f"{len(ok['BONLY'] & ok['SONLY'])}")
    P("")

    # ---------------------------------------------------------------- the ladder
    P("=" * 120)
    P("THE LADDER - premium on kernel-matched k=36 draws, every (vint, char, BW, level, flavour, seed)")
    P("=" * 120)
    rows, chrows = [], []
    total = sum(len(v) for v in DR.values())
    done = 0
    for (v, bw), draws in DR.items():
        pool = POOLS[v]["pool"]
        bnames = POOLS[v]["bnames"]
        for key, d in draws.items():
            pxd = pd.concat([pool[d["names"]], spy_pool.rename("SPY")],
                            axis=1).dropna(how="all").ffill()
            tr = set(d["names"])
            st = pxd.index[260]
            spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
            v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
            ch = panel_chars(pxd, tr)
            nb = sum(1 for c in d["names"] if c in bnames)
            chrows.append(dict(panel=key, **{q: d[q] for q in
                                             ("vint", "char", "flavour", "level", "seed", "BW")},
                               n_from_B=nb, n_from_S=K - nb, **ch))
            for g in GROSS:
                books = make_books(pxd, tr, g)
                for freq in CADENCE:
                    res = {a: fast_backtest(pxd, w, COST, freq) for a, w in books.items()}
                    rets = {a: x["returns"].loc[st:] for a, x in res.items()}
                    mc = metrics(rets["EWall"])
                    mci = metrics(rets["EWall"].loc[:IS_END])["Sharpe"]
                    mco = metrics(rets["EWall"].loc[OOS_START:])["Sharpe"]
                    for a in books:
                        r = rets[a]
                        row = dict(panel=key, arm=a, gross=g, cadence=freq, vint=v, BW=bw,
                                   char=d["char"], flavour=d["flavour"], level=d["level"],
                                   seed=d["seed"], achieved=ch[d["char"]], n_from_B=nb,
                                   ach_momac=ch["momac"], ach_tpers=ch["tpers"],
                                   ach_cvol=ch["cvol"])
                        row.update(rowify(r, res[a]["turnover"].loc[st:]))
                        row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                        row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                        row["dIS_Sharpe_vs_EWall"] = row["IS_Sharpe"] - mci
                        row["dOOS_Sharpe_vs_EWall"] = row["OOS_Sharpe"] - mco
                        row["keep4a"] = keep_4a(r, v2)
                        row["fail4b"] = fail_4b(r, spy)
                        row["keep4b"] = row["fail4b"] == "-"
                        rows.append(row)
            done += 1
            if done % 200 == 0:
                P(f"  {done}/{total} draws done ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    CH = pd.DataFrame(chrows)
    P(f"  {total} draws x 2 arms x {len(GROSS)} gross x {len(CADENCE)} cadence = {len(G)} books "
      f"({time.time()-t0:.0f}s)")
    P("")

    T = G[G.arm == "MA-RS"]
    dp = T.groupby(["panel", "vint", "char", "BW", "flavour", "level", "seed"]).agg(
        premium=("dSharpe_vs_EWall", "mean"), prem_IS=("dIS_Sharpe_vs_EWall", "mean"),
        prem_OOS=("dOOS_Sharpe_vs_EWall", "mean"), achieved=("achieved", "first"),
        n_from_B=("n_from_B", "first")).reset_index()
    rung = dp.groupby(["vint", "char", "BW", "flavour", "level"]).agg(
        n=("premium", "size"), achieved=("achieved", "mean"), n_from_B=("n_from_B", "mean"),
        premium=("premium", "mean"), sd=("premium", "std"),
        prem_IS=("prem_IS", "mean"), prem_OOS=("prem_OOS", "mean")).reset_index()

    def origin_rows(vint, char, bw, levels):
        o = []
        for L in levels:
            d = rung[(rung.vint == vint) & (rung.char == char) & (rung.BW == bw)
                     & (np.abs(rung.level - L) < 1e-9)].set_index("flavour")
            if not {"BONLY", "SONLY"} <= set(d.index):
                continue
            db, ds = d.loc["BONLY"], d.loc["SONLY"]
            sd_pair = float(np.sqrt((db["sd"] ** 2 + ds["sd"] ** 2) / 2))
            gap = float(db["premium"] - ds["premium"])
            o.append(dict(vint=vint, char=char, BW=bw, level=L, achieved_B=db["achieved"],
                          achieved_S=ds["achieved"],
                          match_resid=float(db["achieved"] - ds["achieved"]),
                          prem_B=db["premium"], prem_S=ds["premium"], gap=gap,
                          gap_IS=float(db["prem_IS"] - ds["prem_IS"]),
                          gap_OOS=float(db["prem_OOS"] - ds["prem_OOS"]), sd_pair=sd_pair,
                          t=gap / (sd_pair / np.sqrt(len(SEEDS))) if sd_pair > 0 else np.nan,
                          within_floor=abs(gap) <= sd_pair, ratio_to_568=gap / ORIGIN568))
        return pd.DataFrame(o)

    OR = pd.concat([origin_rows(v, c, bw, DRAWLEV[v][c])
                    for v in POOLS for c in DRAWLEV[v] for bw in BW_SET], ignore_index=True)

    # ---------------------------------------------------------------- G3 anchor drift
    P("=" * 120)
    P("G3 ANCHOR - idea 571's committed BW=0.500 / Q5 origin rows vs this run's, both vintages")
    P("=" * 120)
    o571 = pd.read_csv(f"{PARENT571}.origin.csv")
    o571 = o571[o571.char.isin(CHARS)]
    P(f"  committed (idea 571): momac {len(o571[o571.char=='momac'])} rungs, mean |gap| "
      f"{float(o571[o571.char=='momac'].gap.abs().mean()):.4f} "
      f"(quoted {MOMAC571_ABSGAP:.4f}), mean |resid| "
      f"{float(o571[o571.char=='momac'].match_resid.abs().mean()):.4f} "
      f"(quoted {MOMAC571_RESID:.4f});  tpers mean |resid| "
      f"{float(o571[o571.char=='tpers'].match_resid.abs().mean()):.4f} "
      f"(quoted {TPERS571_RESID:.4f})")
    for v in POOLS:
        for c in DRAWLEV[v]:
            lv = LEVELS[v][c][ANCHOR_LS]
            if not set(lv) <= set(DRAWLEV[v][c]):
                continue
            d = OR[(OR.vint == v) & (OR.char == c) & (OR.BW == BW_ANCHOR) & OR.level.isin(lv)]
            if not len(d):
                continue
            vrows.append(dict(leg="anchor", vint=v, char=c, n=len(d),
                              abs_gap=float(d.gap.abs().mean()),
                              abs_resid=float(d.match_resid.abs().mean()),
                              committed_abs_gap=float(o571[o571.char == c].gap.abs().mean()),
                              committed_abs_resid=float(
                                  o571[o571.char == c].match_resid.abs().mean())))
            P(f"  this run {v:6s} {c:6s} BW=0.500/{ANCHOR_LS}: {len(d)} rungs, mean |gap| "
              f"{float(d.gap.abs().mean()):.4f}, mean |resid| "
              f"{float(d.match_resid.abs().mean()):.4f}")
    VD = pd.DataFrame(vrows)
    P("  -> the anchor MOVED with the vintage; every comparison below is within-vintage.")
    P("")

    # ---------------------------------------------------------------- the answer
    P("=" * 120)
    P("THE MATCHED-LEVEL B-S GAP AT EVERY BANDWIDTH - every rung, every tuned point")
    P("=" * 120)
    P(f"  {'vint':6s} {'char':6s} {'BW':>5s} {'L':>8s} {'achB':>8s} {'achS':>8s} {'resid':>8s} "
      f"{'premB':>8s} {'premS':>8s} {'B-S':>8s} {'sd':>7s} {'t':>7s} {'/568':>6s} {'inFlr':>6s}")
    for _, r in OR.iterrows():
        P(f"  {r['vint']:6s} {r['char']:6s} {r['BW']:5.3f} {r['level']:8.4f} "
          f"{r['achieved_B']:8.4f} {r['achieved_S']:8.4f} {r['match_resid']:+8.4f} "
          f"{r['prem_B']:+8.4f} {r['prem_S']:+8.4f} {r['gap']:+8.4f} {r['sd_pair']:7.4f} "
          f"{r['t']:+7.2f} {r['ratio_to_568']:+6.2f} {str(r['within_floor']):>6s}")
    P("")
    summ = []
    for v in POOLS:
        for c in DRAWLEV[v]:
            for bw in BW_SET:
                for ls in LEVELSETS:
                    lv = LEVELS[v][c][ls]
                    if not set(lv) <= set(DRAWLEV[v][c]):
                        continue
                    d = OR[(OR.vint == v) & (OR.char == c) & (OR.BW == bw) & OR.level.isin(lv)]
                    if not len(d):
                        summ.append(dict(vint=v, char=c, BW=bw, levelset=ls, n_overlap=0))
                        continue
                    summ.append(dict(vint=v, char=c, BW=bw, levelset=ls, n_overlap=len(d),
                                     mean_gap=float(d.gap.mean()),
                                     mean_abs_gap=float(d.gap.abs().mean()),
                                     mean_sd=float(d.sd_pair.mean()),
                                     gap_over_floor=float(d.gap.abs().mean() / d.sd_pair.mean()),
                                     mean_abs_resid=float(d.match_resid.abs().mean()),
                                     ratio_568=float(d.gap.abs().mean() / ORIGIN568),
                                     n_within_floor=int(d.within_floor.sum()),
                                     mean_gap_IS=float(d.gap_IS.mean()),
                                     mean_gap_OOS=float(d.gap_OOS.mean()),
                                     mean_abs_gap_IS=float(d.gap_IS.abs().mean()),
                                     mean_abs_gap_OOS=float(d.gap_OOS.abs().mean())))
    SU = pd.DataFrame(summ)
    P("  SUMMARY - EVERY tuned grid point reported (9 for momac/LIVE; the rest are controls)")
    P(f"  {'vint':6s} {'char':6s} {'BW':>5s} {'lset':4s} {'ovl':>4s} {'meanGap':>8s} {'|gap|':>7s} "
      f"{'floor':>7s} {'|g|/flr':>8s} {'|resid|':>8s} {'|g|/568':>8s} {'inFlr':>8s} "
      f"{'gapIS':>8s} {'gapOOS':>8s}")
    for _, r in SU.iterrows():
        if not r["n_overlap"]:
            P(f"  {r['vint']:6s} {r['char']:6s} {r['BW']:5.3f} {r['levelset']:4s}    0   "
              f"NO OVERLAPPING RUNG")
            continue
        P(f"  {r['vint']:6s} {r['char']:6s} {r['BW']:5.3f} {r['levelset']:4s} {r['n_overlap']:4d} "
          f"{r['mean_gap']:+8.4f} {r['mean_abs_gap']:7.4f} {r['mean_sd']:7.4f} "
          f"{r['gap_over_floor']:8.2f} {r['mean_abs_resid']:8.4f} {r['ratio_568']:8.2f} "
          f"{r['n_within_floor']:3d}/{r['n_overlap']:<4d} {r['mean_gap_IS']:+8.4f} "
          f"{r['mean_gap_OOS']:+8.4f}")
    P("")

    def su(v, c, bw, ls, col):
        d = SU[(SU.vint == v) & (SU.char == c) & (SU.BW == bw) & (SU.levelset == ls)]
        return float(d[col].iloc[0]) if len(d) and d.n_overlap.iloc[0] else float("nan")

    # H_TIGHTEN, read on the ANCHOR rung set so the comparison is like-for-like with idea 571
    res_bw = {bw: su("LIVE", "momac", bw, ANCHOR_LS, "mean_abs_resid") for bw in BW_SET}
    res19 = {bw: su("LIVE", "momac", bw, "Q19", "mean_abs_resid") for bw in BW_SET}
    mono = all(res_bw[BW_SET[i]] >= res_bw[BW_SET[i + 1]] for i in range(len(BW_SET) - 1))
    H_TIGHTEN = bool(mono and res_bw[BW_SET[-1]] <= TPERS571_RESID)
    P("  H_TIGHTEN - momac mean |match residual| by bandwidth (LIVE)")
    for bw in BW_SET:
        P(f"    BW {bw:.3f}: {ANCHOR_LS} {res_bw[bw]:.4f}   Q19 {res19[bw]:.4f}   "
          f"FROZEN {ANCHOR_LS} {su('FROZEN','momac',bw,ANCHOR_LS,'mean_abs_resid'):.4f}")
    P(f"    monotone decreasing in BW {mono};  BW=0.125 residual {res_bw[BW_SET[-1]]:.4f} vs the "
      f"queue's target {TPERS571_RESID:.4f} -> {'PASS' if H_TIGHTEN else 'FAIL'}")
    P("")

    cand = SU[(SU.vint == "LIVE") & (SU.char == "momac") & (SU.n_overlap > 0)]
    tight = cand.sort_values("mean_abs_resid").iloc[0]
    a_gap = su("LIVE", "momac", BW_ANCHOR, ANCHOR_LS, "mean_abs_gap")
    a_flr = su("LIVE", "momac", BW_ANCHOR, ANCHOR_LS, "gap_over_floor")
    q19_gap = su("LIVE", "momac", tight.BW, "Q19", "mean_abs_gap")
    H_SMALL = bool(tight.mean_abs_gap < CARRIER_BAR)
    H_RUNGS = bool(q19_gap < CARRIER_BAR)
    H_FLOOR = bool(tight.gap_over_floor <= 1.25 * a_flr)
    H_GROW = bool(tight.mean_abs_gap > a_gap)
    H_RESID = not H_SMALL
    P(f"  TIGHTEST-MATCHED momac cell (chosen on |resid| ALONE, never on the gap): BW "
      f"{tight.BW:.3f} / {tight.levelset} on {int(tight.n_overlap)} rungs, |resid| "
      f"{tight.mean_abs_resid:.4f}")
    P(f"    |gap| there {tight.mean_abs_gap:.4f} ({tight.ratio_568:.2f}x ORIGIN568) vs this run's "
      f"anchor {a_gap:.4f} and idea 571's committed {MOMAC571_ABSGAP:.4f}")
    P(f"  H_SMALL  (|gap| {tight.mean_abs_gap:.4f} < carrier bar {CARRIER_BAR:.4f}) -> "
      f"{'PASS' if H_SMALL else 'FAIL'}")
    P(f"  H_RUNGS  (|gap| on Q19 at BW={tight.BW:.3f} {q19_gap:.4f} < {CARRIER_BAR:.4f}) -> "
      f"{'PASS' if H_RUNGS else 'FAIL'}")
    P(f"  H_FLOOR  (|gap|/floor {tight.gap_over_floor:.2f} <= 1.25 x {a_flr:.2f} = "
      f"{1.25*a_flr:.2f}) -> {'PASS' if H_FLOOR else 'FAIL'}")
    P(f"  H_GROW   (|gap| {tight.mean_abs_gap:.4f} > anchor {a_gap:.4f}) -> "
      f"{'PASS' if H_GROW else 'FAIL'}")
    P(f"  H_RESID  (the queue's alternative: the small gap is a matching residual) -> "
      f"{'CONFIRMED' if H_RESID else 'REFUTED'}")
    P("")
    P("  CONTROL - tpers at the same three bandwidths (it was ALREADY tightly matched, so a")
    P("  bandwidth effect on ITS gap is a machinery effect, not a momac one):")
    for bw in BW_SET:
        for ls in (ANCHOR_LS, "Q9"):
            d = SU[(SU.vint == "LIVE") & (SU.char == "tpers") & (SU.BW == bw)
                   & (SU.levelset == ls)]
            if len(d) and d.n_overlap.iloc[0]:
                r = d.iloc[0]
                P(f"    tpers BW {bw:.3f} {ls:3s}: overlap {int(r.n_overlap):2d}, |gap| "
                  f"{r.mean_abs_gap:.4f} ({r.ratio_568:.2f}x 568), |gap|/floor "
                  f"{r.gap_over_floor:.2f}, |resid| {r.mean_abs_resid:.4f}")
    P("")

    # ---------------------------------------------------------------- WF-A
    P("=" * 120)
    P("RULE 8 WF-A - the same gap recomputed on IS and on OOS separately, OOS read ONCE")
    P("=" * 120)
    P(f"  {'vint':6s} {'char':6s} {'BW':>5s} {'lset':4s} {'ovl':>4s} {'gapFULL':>8s} "
      f"{'gapIS':>8s} {'gapOOS':>8s} {'|g|IS':>7s} {'|g|OOS':>7s} {'smlIS':>6s} {'smlOOS':>7s}")
    wfa = []
    for _, r in SU.iterrows():
        if not r["n_overlap"]:
            continue
        sis = bool(r["mean_abs_gap_IS"] < CARRIER_BAR)
        sos = bool(r["mean_abs_gap_OOS"] < CARRIER_BAR)
        wfa.append(dict(leg="WF-A", vint=r["vint"], char=r["char"], BW=r["BW"],
                        levelset=r["levelset"], n_overlap=r["n_overlap"], gap_FULL=r["mean_gap"],
                        gap_IS=r["mean_gap_IS"], gap_OOS=r["mean_gap_OOS"],
                        abs_IS=r["mean_abs_gap_IS"], abs_OOS=r["mean_abs_gap_OOS"],
                        small_IS=sis, small_OOS=sos, resid=r["mean_abs_resid"]))
        P(f"  {r['vint']:6s} {r['char']:6s} {r['BW']:5.3f} {r['levelset']:4s} {r['n_overlap']:4d} "
          f"{r['mean_gap']:+8.4f} {r['mean_gap_IS']:+8.4f} {r['mean_gap_OOS']:+8.4f} "
          f"{r['mean_abs_gap_IS']:7.4f} {r['mean_abs_gap_OOS']:7.4f} {str(sis):>6s} "
          f"{str(sos):>7s}")
    WFA = pd.DataFrame(wfa)
    nm = WFA[(WFA.char == "momac") & (WFA.vint == "LIVE")]
    P(f"  momac/LIVE: verdict 'gap is small' holds IS in {int(nm.small_IS.sum())}/{len(nm)} tuned "
      f"cells and OOS in {int(nm.small_OOS.sum())}/{len(nm)}")
    P("")

    # ---------------------------------------------------------------- WF-B
    P("=" * 120)
    P("RULE 8 WF-B - the absorption claim as a trading instruction, OOS read ONCE")
    P("=" * 120)
    P("  'At matched momac the panel of origin does not matter, so hold whichever flavour is")
    P("  available.'  Among the OVERLAPPING rungs only, (flavour, level, seed, gross, cadence) is")
    P("  chosen by IS Sharpe ALONE; OOS is then read once against live RULES v2 on U56 and SPY.")
    pxU, trU = panels["U56"]
    stU = pxU.index[260]
    v2U = fast_backtest(pxU, rules_v2_weights(pxU), COST, "W")["returns"].loc[stU:]
    spyU = pxU["SPY"].pct_change().fillna(0.0).loc[stU:]
    mv2f, mspf = metrics(v2U), metrics(spyU)
    mv2, msp = metrics(v2U.loc[OOS_START:]), metrics(spyU.loc[OOS_START:])
    v2h, spyh = halves(v2U), halves(spyU)
    P(f"  comparands FULL: RULES v2 on U56 {mv2f['CAGR']:.2%} / {mv2f['Sharpe']:.4f} / "
      f"{mv2f['MaxDD']:.2%} (halves {v2h[0]:.4f} / {v2h[1]:.4f});  SPY {mspf['CAGR']:.2%} / "
      f"{mspf['Sharpe']:.4f} / {mspf['MaxDD']:.2%} (halves {spyh[0]:.4f} / {spyh[1]:.4f})")
    P(f"  comparands OOS : RULES v2 {mv2['CAGR']:.2%} / {mv2['Sharpe']:.4f} / {mv2['MaxDD']:.2%};  "
      f"SPY {msp['CAGR']:.2%} / {msp['Sharpe']:.4f} / {msp['MaxDD']:.2%}")
    P("")
    wfb = []
    for v in POOLS:
        for c in DRAWLEV[v]:
            for bw in BW_SET:
                o = OR[(OR.vint == v) & (OR.char == c) & (OR.BW == bw)]
                if not len(o):
                    continue
                lv = set(np.round(o.level.to_numpy(), 6))
                sel = T[(T.vint == v) & (T.char == c) & (T.BW == bw)
                        & T.flavour.isin(["BONLY", "SONLY"]) & T.level.round(6).isin(lv)]
                if not len(sel):
                    continue
                pick = sel.sort_values("IS_Sharpe", ascending=False).iloc[0]
                hh = sel.groupby("flavour").OOS_Sharpe.mean()
                wfb.append(dict(leg="WF-B", vint=v, char=c, BW=bw, n_overlap=len(o),
                                sel_flavour=pick.flavour, sel_level=pick.level,
                                sel_seed=pick.seed, sel_gross=pick.gross,
                                sel_cadence=pick.cadence, IS_Sharpe=pick.IS_Sharpe,
                                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                OOS_MaxDD=pick.OOS_MaxDD, v2_OOS_CAGR=mv2["CAGR"],
                                v2_OOS_Sharpe=mv2["Sharpe"], v2_OOS_MaxDD=mv2["MaxDD"],
                                spy_OOS_CAGR=msp["CAGR"], spy_OOS_Sharpe=msp["Sharpe"],
                                spy_OOS_MaxDD=msp["MaxDD"],
                                beat_v2=bool(pick.OOS_Sharpe > mv2["Sharpe"]),
                                beat_spy=bool(pick.OOS_Sharpe > msp["Sharpe"]),
                                keep4a=bool(pick.keep4a), keep4b=bool(pick.keep4b),
                                fail4b=pick.fail4b, hh_BONLY=float(hh.get("BONLY", np.nan)),
                                hh_SONLY=float(hh.get("SONLY", np.nan))))
    WFB = pd.DataFrame(wfb)
    P(f"  {'vint':6s} {'char':6s} {'BW':>5s} {'ovl':>4s} {'held':29s} {'IS Shp':>7s} "
      f"{'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} {'>v2':>5s} {'>SPY':>5s} {'4b fail':>10s} "
      f"{'hhB':>7s} {'hhS':>7s}")
    for _, r in WFB.iterrows():
        held = (f"{r['sel_flavour']} L{r['sel_level']:.3f} s{int(r['sel_seed'])} "
                f"g{r['sel_gross']:.2f} {r['sel_cadence']}")
        P(f"  {r['vint']:6s} {r['char']:6s} {r['BW']:5.3f} {r['n_overlap']:4d} {held:29s} "
          f"{r['IS_Sharpe']:7.4f} {r['OOS_CAGR']:9.2%} {r['OOS_Sharpe']:7.4f} "
          f"{r['OOS_MaxDD']:8.2%} {str(r['beat_v2']):>5s} {str(r['beat_spy']):>5s} "
          f"{r['fail4b']:>10s} {r['hh_BONLY']:7.4f} {r['hh_SONLY']:7.4f}")
    P("")
    P(f"  beat RULES v2 on OOS Sharpe: {int(WFB.beat_v2.sum())}/{len(WFB)};  "
      f"beat SPY on OOS Sharpe: {int(WFB.beat_spy.sum())}/{len(WFB)};  "
      f"4a {int(WFB.keep4a.sum())}/{len(WFB)};  4b {int(WFB.keep4b.sum())}/{len(WFB)}")
    P("  hhB/hhS = mean OOS Sharpe of the BONLY / SONLY arms over the overlapping rungs - the")
    P("  head-to-head the absorption claim is actually about.")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 120)
    P("KEEP PATHS 4a / 4b - every book on the ladder")
    P("=" * 120)
    kp = G[["panel", "vint", "char", "BW", "flavour", "level", "seed", "arm", "gross", "cadence",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "keep4a", "fail4b", "keep4b"]]
    P(f"  all {len(kp)} books: 4a {int(kp.keep4a.sum())}, 4b {int(kp.keep4b.sum())}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}")
    for bw in BW_SET:
        d = kp[kp.BW == bw]
        P(f"  BW={bw:.3f} ({len(d):5d} books): 4a {int(d.keep4a.sum()):4d}, "
          f"4b {int(d.keep4b.sum()):4d}, BOTH {int((d.keep4a & d.keep4b).sum()):3d}")
    for fl in FLAVOURS:
        d = kp[kp.flavour == fl]
        P(f"  {fl:6s} ({len(d):5d} books): 4a {int(d.keep4a.sum()):4d}, "
          f"4b {int(d.keep4b.sum()):4d}")
    fb = kp[~kp.keep4b].fail4b.str.split(",").explode().value_counts()
    P("  binding 4b legs: " + ", ".join(f"{a} {b}" for a, b in fb.items()))
    P("  EVERY panel here is a kernel-weighted seeded draw, not a tradable rule: no 4b pass on")
    P("  this ladder is a capital candidate, and none is claimed.")
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 120)
    P("VERDICT")
    P("=" * 120)
    for a, b in dict(H_TIGHTEN=H_TIGHTEN, H_SMALL=H_SMALL, H_RUNGS=H_RUNGS, H_FLOOR=H_FLOOR,
                     H_GROW=H_GROW).items():
        P(f"  {a:10s} {'PASS' if b else 'FAIL'}")
    P(f"  H_RESID    {'CONFIRMED' if H_RESID else 'REFUTED'}")
    P("")
    P("  momac matched-level |B-S| (LIVE vintage, within-vintage anchor in bold position first):")
    for _, r in SU[(SU.vint == "LIVE") & (SU.char == "momac") & (SU.n_overlap > 0)].iterrows():
        P(f"    BW={r.BW:.3f}/{r.levelset:3s} |gap| {r.mean_abs_gap:.4f} on {int(r.n_overlap):2d} "
          f"rungs ({r.ratio_568:.2f}x 568, |gap|/floor {r.gap_over_floor:.2f}, |resid| "
          f"{r.mean_abs_resid:.4f})")
    P("")

    G.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    rung.to_csv(f"{OUT}/{STAMP}.rungs.csv", index=False)
    OR.to_csv(f"{OUT}/{STAMP}.origin.csv", index=False)
    SU.to_csv(f"{OUT}/{STAMP}.summary.csv", index=False)
    FE.to_csv(f"{OUT}/{STAMP}.feas.csv", index=False)
    VD.to_csv(f"{OUT}/{STAMP}.vintage.csv", index=False)
    pd.concat([WFA, WFB], ignore_index=True).to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)
    kp.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    CH.to_csv(f"{OUT}/{STAMP}.chars.csv", index=False)
    P(f"wrote grid {len(G)}, rungs {len(rung)}, origin {len(OR)}, summary {len(SU)}, "
      f"feas {len(FE)}, vintage {len(VD)}, wf {len(WFA)+len(WFB)}, keeppaths {len(kp)}, "
      f"chars {len(CH)} rows in {time.time()-t0:.0f}s")
    Path(f"{OUT}/{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
