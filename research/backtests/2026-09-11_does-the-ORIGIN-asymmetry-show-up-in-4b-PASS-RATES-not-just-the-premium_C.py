#!/usr/bin/env python3
"""Idea 784 (lane C, 2026-09-11) - does-the-ORIGIN-asymmetry-show-up-in-4b-PASS-RATES-not-just-the-premium.

QUESTION
--------
Idea 570 matched B136-sourced and SMALL439-sourced panels ONE-TO-ONE on a characteristic and
found the MA-gate selection premium still separates by origin (+0.1649 .. +0.3021).  In the
same run's KEEP-path census the two sides also separate on something nobody priced: of the
2592 books on each side, **225 B-side books pass PROTOCOL 4b against 19 S-side books** at
identical characteristic, identical width k and identical (gross, cadence).  An 11.8x
asymmetry.  Is that pass-rate gap the premium gap re-expressed - the same selection edge,
read through a pass/fail bar - or an independent DRAWDOWN fact about where the names came
from?

WHY IT IS NOT OBVIOUSLY THE SAME STATEMENT
------------------------------------------
The premium is a WITHIN-panel arm difference, Sharpe(MA-RS) - Sharpe(EWall), and is invariant
to the exposure dial.  4b is an ABSOLUTE bar on a single book against SPY with five legs -
three Sharpe legs (H1, H2, OOS) and two LEVEL legs (a MaxDD cap at 60% of SPY's and a CAGR
floor at 70% of SPY's).  A panel can carry a large selection premium and still fail 4b on
drawdown, and a panel with no premium at all can pass on level alone: the EWall arm carries
no selection whatsoever, yet idea 570's census shows 115 of its 244 4b passers are EWall
books.  So "the origin asymmetry" could live in either object, and the two answers point
different ways: a premium-carried gap is a statement about the MA gate, a drawdown-carried
gap is a statement about the panels themselves and would survive any gate put on them.

DESIGN
------
Rebuild idea 570's matched grid from prices - the same pool (573 names, 2010-01-04 ..
2026-09-04), the same seeded greedy one-to-one nearest-neighbour match, the same two arms
(EWall = gross g over every priced name; MA-RS = gross g respread over names above their 200d
MA), the same 5184 books - and then take each book apart LEG BY LEG instead of reading one
pass/fail bit.  Every B book has exactly one S twin at the same (char, tau, k, seed, arm,
gross, cadence), so the whole census is 2592 matched PAIRS and every comparison below is
paired.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. BAR lambda in {0.60, 0.80, 1.00, 1.25} - a single strictness knob on 4b, lambda = 1.00 IS
       PROTOCOL 4b verbatim:  Sharpe > lambda * SPY (H1, H2, OOS),
       MaxDD >= (0.60 / lambda) * SPY MaxDD,  CAGR >= lambda * 0.70 * SPY CAGR.
       Larger lambda is stricter on every leg.
    2. k in {18, 36, 72} pairs
All 4 x 3 = 12 grid points are reported.  REPORTED (never selected) axes: characteristic
{cvol, breadth}, tau {0.01, 0.02, 0.05, inf}, gross {0.50, 0.75, 1.00}, cadence {W, M},
arm {EWall, MA-RS}, seed (12), period (FULL / IS / OOS).
NOTE on the k dial's support, stated up front: idea 570's match is INFEASIBLE at k=72 for
every finite tau (the S pool runs out of partners), so k=72 exists only at tau=inf.  The k
column is therefore 4 tau x 12 seeds at k=18 and k=36 and 1 tau x 12 seeds at k=72; every
table below prints its own n.

PRE-REGISTERED HYPOTHESES (written before any leg was read)
-----------------------------------------------------------
PUB_B, PUB_S = 225, 19 of 2592 (idea 570's committed counts); PUB_RATIO = 11.84.
H_PREM : the pass-rate gap is the premium gap re-expressed.  Predicts (i) the asymmetry is
         carried by the three SHARPE legs - the block the premium lives in - so the B/S ratio
         of the Sharpe-only sub-criterion {H1, H2, OOS} is at least half the full-4b ratio
         (>= 5.9x), and (ii) it is an MA-RS phenomenon: the EWall arm, which has no selection
         at all, shows a materially smaller ratio than MA-RS.
H_DD   : the gap is an independent LEVEL fact.  Predicts dropping the DD leg collapses the
         B/S ratio while dropping any Sharpe leg leaves it intact - operationally, the
         drop-DD ratio is below HALF the full-4b ratio AND every drop-Sharpe-leg ratio is
         above 0.8x of it.  Both sides of that bar are printed as multiples of the full
         ratio, so a reader can apply their own.
H_COND : if the gap is return-carried, conditioning each pair on the book's own full-sample
         Sharpe removes it - the Mantel-Haenszel odds ratio across Sharpe deciles falls below
         half the crude odds ratio.  (Conditioning on MaxDD deciles is reported beside it as
         a TAUTOLOGY CHECK, not as evidence: the DD leg is part of the outcome.)
H_LINK : if the two objects are one object, the per-draw premium gap predicts the per-draw
         pass gap across the 216 (char, tau, k, seed) draws.  Falsified if |rho| < 0.30.

GATES (pre-registered, run and printed before any new number is read)
    G0 metrics    : this run's numpy `mstats` vs engine.metrics on a real book.      bar 1e-12
    G1 identity   : fast_backtest vs engine.backtest on one book per real panel.     bar 1e-12
    G2 pool       : 573 names (B 134 + SMALL 439), 2010-01-04 .. 2026-09-04, 4194 bars. exact
    G3 grid repro : idea 570's committed `.grid.csv`, ALL 5184 rows x 11 numeric columns
                    rebuilt here from prices and its own seeding scheme.              bar 1e-9
    G4 headline   : its committed KEEP-path counts re-derived exactly - 4a 21/5184, 4b
                    244/5184, BOTH 1/5184, by side B 225/2592 S 19/2592, by arm EWall 115
                    MA-RS 129, and its six binding-failure-leg counts.                 exact
    G5 comparand  : every matched panel frame shares the pool index and the same warm-up
                    start, so ONE SPY series is the comparand for all 5184 books.      exact

RULE 8 WALK-FORWARD (required, run whatever the census says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: re-read the pass-rate asymmetry AND its leg decomposition with every
       leg computed inside IS only and inside OOS only (a period-local 4-leg 4b: both halves
       of the period, the period's DD cap, the period's CAGR floor), at all 12 tuned points.
       An asymmetry that is IS-only, or whose CARRIER leg changes between IS and OOS, is not
       a fact about the panels.
    WF-B on a BOOK: the census is a decision rule - "at matched characteristic, trade the
       B-sourced panel".  Pick (char, tau, k) on IS 4b pass rate of the B side (this idea's
       own statistic), tie-broken by IS Sharpe; read OOS ONCE for the seed-pooled B-side book
       against its S-side twin, an ORIGIN-BLIND control, the incumbent whole-B136 gate,
       RULES v2 on U56 and SPY.
    KEEP paths 4a and 4b are evaluated for EVERY book.  Stated up front, as idea 570 stated
    it: a matched draw is a DIAGNOSTIC panel, not a rule anyone can trade, so a 4b pass on
    this grid is a diagnostic and never a capital candidate.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents; the small end
    carries more survivorship premium than B136, and a differential survivorship premium
    between the two panels is an alternative explanation this design cannot exclude - it is
    idea 782's question and is restated beside every headline here.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and committed artefacts of
idea 570; modifies nothing but its own outputs:
    .grid.csv .legs.csv .census.csv .walkforward.csv .keeppaths.csv .console.txt
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
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"
CHARS = ["cvol", "breadth"]
TAUS = [0.01, 0.02, 0.05, np.inf]
KS = [18, 36, 72]
SEEDS = list(range(12))
LAMBDAS = [0.60, 0.80, 1.00, 1.25]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
SHARPE_LEGS = ["H1", "H2", "OOS"]
LEVEL_LEGS = ["DD", "CAGR"]
NPERM = 20000

# idea 570's committed numbers (pre-registered comparands)
P570 = OUT / "2026-09-11_is-the-ORIGIN-gap-a-MATCHING-RESIDUAL-or-a-real-panel-effect_cloud"
PUB_B, PUB_S, PUB_N = 225, 19, 2592
PUB_RATIO = PUB_B / PUB_S
PUB_COUNTS = dict(a4=21, b4=244, both=1, ewall=115, mars=129)
PUB_LEGS = {"DD": 1728, "H1,H2,OOS,DD,CAGR": 997, "CAGR": 460, "H2,OOS,DD": 320,
            "H1,H2,OOS,CAGR": 254, "-": 244}
TOL, TOL_ID = 1e-9, 1e-12

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1).  Idea 312/568/570's runner."""
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


def mstats(a):
    """engine.metrics' CAGR / Sharpe / MaxDD on a numpy array (asserted in G0)."""
    eq = np.cumprod(1.0 + a)
    yrs = len(a) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = eq / np.maximum.accumulate(eq) - 1.0
    vol = a.std(ddof=1) * np.sqrt(252.0)
    return (float(cagr), float(a.mean() * 252.0 / vol) if vol else np.nan, float(dd.min()))


def periodstats(a):
    """CAGR / Sharpe / MaxDD of a period and the Sharpe of each of its two halves."""
    c, s, d = mstats(a)
    h = len(a) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=mstats(a[:h])[1], H2=mstats(a[h:])[1])


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


def keep_4a(r, b):
    """PROTOCOL 4a against the live book, idea 570's function verbatim."""
    h = len(r) // 2
    a1, a2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    hb = len(b) // 2
    b1, b2 = metrics(b.iloc[:hb])["Sharpe"], metrics(b.iloc[hb:])["Sharpe"]
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def leg_margins(bk, sp, lam=1.0, full=True):
    """Signed slack on every 4b leg: positive = leg passes.  lambda scales strictness.

    FULL form is PROTOCOL 4b verbatim at lambda=1 (five legs).  Period-local form (full=False)
    drops the OOS leg because inside a single period there is no out-of-sample half; the four
    remaining legs are computed entirely within that period."""
    m = {"H1": bk["H1"] - lam * sp["H1"],
         "H2": bk["H2"] - lam * sp["H2"],
         "DD": bk["MaxDD"] - (0.60 / lam) * sp["MaxDD"],
         "CAGR": bk["CAGR"] - lam * 0.70 * sp["CAGR"]}
    if full:
        m["OOS"] = bk["OOS_Sharpe"] - lam * sp["OOS_Sharpe"]
    return m


def fails_of(m, legs):
    return [L for L in legs if not m[L] > 0] if legs else []


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


def name_chars(pool):
    """idea 568/570's per-NAME characteristic, verbatim: annualised vol and MA breadth."""
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)
    on = above_ma(pool) & pool.notna()
    br = (on.sum() / pool.notna().sum().replace(0, np.nan)).astype(float)
    return pd.DataFrame(dict(cvol=vol, breadth=br)).dropna()


def greedy_match(nc, bnames, snames, char, tau, k, seed):
    """idea 570's matcher, verbatim: seeded visit order, nearest UNUSED S partner, |d| <= tau,
    first k accepted pairs, no name reused on either side."""
    rng = np.random.default_rng(zlib.crc32(f"MATCH|{char}|{tau}|{k}|{seed}".encode()) % (2 ** 32))
    xb = nc.loc[sorted(bnames), char]
    xs = nc.loc[sorted(snames), char].sort_values()
    s_names = xs.index.to_numpy()
    s_vals = xs.to_numpy(float)
    used = np.zeros(len(s_vals), bool)
    order = rng.permutation(xb.index.to_numpy())
    pairs = []
    for b in order:
        if len(pairs) >= k:
            break
        v = float(xb.loc[b])
        d = np.abs(s_vals - v)
        d[used] = np.inf
        j = int(np.argmin(d))
        if not np.isfinite(d[j]) or d[j] > tau:
            continue
        used[j] = True
        pairs.append((b, str(s_names[j]), float(v), float(s_vals[j]), float(d[j])))
    return pairs


# ------------------------------------------------------------------------- census helpers
def ratio(nb, ns, n_b, n_s):
    """B/S pass-RATE ratio.  Undefined (NaN) when NEITHER side passes; a +0.5 continuity
    correction on the S side when only it is empty (that value is flagged `capped`)."""
    if ns == 0 and nb == 0:
        return np.nan, True
    if ns == 0:
        return ((nb + 0.5) / n_b) / (0.5 / n_s), True
    return (nb / n_b) / (ns / n_s), False


def mcnemar(pb, ps):
    """Paired discordance on the SAME matched pairs.  Returns (b, c, chi2)."""
    b = int(np.sum(pb & ~ps))
    c = int(np.sum(~pb & ps))
    chi = (abs(b - c) - 1) ** 2 / (b + c) if (b + c) > 0 else np.nan
    return b, c, float(chi)


def mh_odds(pb, sb, ps, ss):
    """Mantel-Haenszel common odds ratio and standardised rate difference across strata.

    pb/ps are the pass flags of the two sides; sb/ss the stratum of each book on ITS OWN side
    (the strata are common deciles of the pooled distribution, so 'stratum 3' means the same
    thing on both sides)."""
    num = den = 0.0
    wsum = wdiff = 0.0
    for s in np.unique(np.concatenate([sb, ss])):
        mb, ms = sb == s, ss == s
        a, b = int(pb[mb].sum()), int((~pb[mb]).sum())
        c, d = int(ps[ms].sum()), int((~ps[ms]).sum())
        n = a + b + c + d
        if n == 0:
            continue
        num += a * d / n
        den += b * c / n
        if (a + b) and (c + d):
            wsum += n
            wdiff += n * (a / (a + b) - c / (c + d))
    return (num / den if den > 0 else np.inf), (wdiff / wsum if wsum else np.nan)


def crude_odds(pb, ps):
    a, b = int(pb.sum()), int((~pb).sum())
    c, d = int(ps.sum()), int((~ps).sum())
    return (a * d) / (b * c) if b * c > 0 else np.inf


def perm_p(diff, nperm=NPERM, seed=784):
    """Two-sided permutation p for a PAIRED mean difference: permuting the side label within a
    pair is a sign flip on that pair's difference."""
    d = np.asarray(diff, float)
    d = d[np.isfinite(d)]
    if len(d) == 0:
        return np.nan
    obs = abs(d.mean())
    rng = np.random.default_rng(seed)
    hit = 0
    done = 0
    while done < nperm:
        m = min(1000, nperm - done)
        sg = rng.choice([-1.0, 1.0], size=(m, len(d)))
        hit += int(np.sum(np.abs((sg * d).mean(axis=1)) >= obs - 1e-15))
        done += m
    return float((1 + hit) / (nperm + 1))


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 784  does-the-ORIGIN-asymmetry-show-up-in-4b-PASS-RATES-not-just-the-premium  (lane C, 2026-09-11)")
    P("=" * 112)
    P(f"PROTOCOL: {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START} read once.")
    P(f"TUNED (2): BAR lambda in {LAMBDAS} x k in {KS} -- all {len(LAMBDAS)*len(KS)} points reported.")
    P(f"Pre-registered: idea 570's committed asymmetry B {PUB_B}/{PUB_N} vs S {PUB_S}/{PUB_N} "
      f"= {PUB_RATIO:.2f}x.")
    P("")

    # ---------------------------------------------------------------- gates part 1
    P("=" * 112)
    P("GATES (pre-registered; printed before any leg is read)")
    P("=" * 112)
    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]

    g0 = g1 = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        fr = fast_backtest(px, w, COST, "W")["returns"]
        er = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float((fr - er).abs().max()))
        st = px.index[260]
        a = fr.loc[st:]
        mm, me = mstats(a.to_numpy(float)), metrics(a)
        g0 = max(g0, max(abs(mm[0] - me["CAGR"]), abs(mm[1] - me["Sharpe"]),
                         abs(mm[2] - me["MaxDD"])))
    P(f"G0 metrics      : numpy mstats vs engine.metrics, 3 real books x 3 statistics, "
      f"max |d| = {g0:.3e} (bar {TOL_ID:.0e}) -> {'PASS' if g0 < TOL_ID else 'FAIL'}")
    P(f"G1 identity     : fast_backtest vs engine.backtest, max |dret| = {g1:.3e} "
      f"(bar {TOL_ID:.0e}) -> {'PASS' if g1 < TOL_ID else 'FAIL'}")

    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]
    nc = name_chars(pool)
    bnames = sorted(set(bn) & set(nc.index))
    snames = sorted(set(sn) & set(nc.index))
    g2 = (len(nc) == 573 and len(bnames) == 134 and len(snames) == 439 and len(ix) == 4194
          and str(ix.min().date()) == "2010-01-04" and str(ix.max().date()) == "2026-09-04")
    P(f"G2 pool         : {ix.min().date()}..{ix.max().date()} ({len(ix)} bars), B {len(bnames)}"
      f" + SMALL {len(snames)} = {len(nc)} names -> {'PASS' if g2 else 'FAIL'} (idea 568/570)")

    # one SPY comparand for the whole matched grid (G5 asserts every frame agrees)
    start_i = 260
    spy_full = spy_pool.pct_change().fillna(0.0).to_numpy(float)[start_i:]
    ix_run = ix[start_i:]
    is_m = np.asarray(ix_run <= pd.Timestamp(IS_END))
    oos_m = np.asarray(ix_run >= pd.Timestamp(OOS_START))
    SPY = periodstats(spy_full)
    SPY["OOS_Sharpe"] = periodstats(spy_full[oos_m])["Sharpe"]
    SPY_IS = periodstats(spy_full[is_m])
    SPY_OOS = periodstats(spy_full[oos_m])
    P(f"                  SPY comparand over the pooled window: CAGR {SPY['CAGR']:.2%} Sharpe "
      f"{SPY['Sharpe']:.4f} MaxDD {SPY['MaxDD']:.2%} | H1 {SPY['H1']:.4f} H2 {SPY['H2']:.4f} "
      f"OOS Sharpe {SPY['OOS_Sharpe']:.4f}")
    P(f"                  4b bars at lambda=1: Sharpe > {SPY['H1']:.4f}/{SPY['H2']:.4f}/"
      f"{SPY['OOS_Sharpe']:.4f}, MaxDD >= {0.60*SPY['MaxDD']:.2%}, CAGR >= "
      f"{0.70*SPY['CAGR']:.2%}")

    # ---------------------------------------------------------------- the grid
    P("")
    P("=" * 112)
    P("REBUILDING IDEA 570'S MATCHED GRID FROM PRICES (5184 books; G3/G4 gate it)")
    P("=" * 112)
    rows, prows = [], []
    starts = set()
    for ch in CHARS:
        for tau in TAUS:
            for k in KS:
                for sd in SEEDS:
                    pr = greedy_match(nc, bnames, snames, ch, tau, k, sd)
                    if len(pr) < k:
                        continue
                    sides = {"B": [p[0] for p in pr], "S": [p[1] for p in pr]}
                    prow = dict(char=ch, tau=tau, k=k, seed=sd)
                    for side, names in sides.items():
                        cols = list(dict.fromkeys(list(names) + ["SPY"]))
                        pxd = pd.concat([pool[list(names)], spy_pool.rename("SPY")],
                                        axis=1)[cols].dropna(how="all").ffill()
                        starts.add(str(pxd.index[start_i].date()))
                        tr = set(names)
                        v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"] \
                            .iloc[start_i:]
                        prem = []
                        for g in GROSS:
                            books = make_books(pxd, tr, g)
                            for freq in CADENCE:
                                res = {a: fast_backtest(pxd, w, COST, freq)
                                       for a, w in books.items()}
                                sh = {}
                                for a in books:
                                    r = res[a]["returns"].iloc[start_i:]
                                    arr = r.to_numpy(float)
                                    st_f = periodstats(arr)
                                    st_i = periodstats(arr[is_m])
                                    st_o = periodstats(arr[oos_m])
                                    sh[a] = st_f["Sharpe"]
                                    tn = float(res[a]["turnover"].iloc[start_i:].sum()
                                               / (len(arr) / 252.0))
                                    row = dict(char=ch, tau=tau, k=k, seed=sd, side=side, arm=a,
                                               gross=g, cadence=freq,
                                               CAGR=st_f["CAGR"], Sharpe=st_f["Sharpe"],
                                               MaxDD=st_f["MaxDD"], H1=st_f["H1"], H2=st_f["H2"],
                                               IS_Sharpe=st_i["Sharpe"], IS_CAGR=st_i["CAGR"],
                                               IS_MaxDD=st_i["MaxDD"], IS_H1=st_i["H1"],
                                               IS_H2=st_i["H2"],
                                               OOS_CAGR=st_o["CAGR"], OOS_Sharpe=st_o["Sharpe"],
                                               OOS_MaxDD=st_o["MaxDD"], OOS_H1=st_o["H1"],
                                               OOS_H2=st_o["H2"], turnover=tn,
                                               keep4a=keep_4a(r, v2))
                                    rows.append(row)
                                prem.append(sh["MA-RS"] - sh["EWall"])
                        prow[f"prem_{side}"] = float(np.mean(prem))
                    prows.append(prow)
        P(f"  {ch}: matched and priced ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    PR = pd.DataFrame(prows)
    P(f"  grid {len(G)} books, {len(PR)} feasible draws x 2 sides")

    # leg margins at every lambda (FULL = PROTOCOL 4b; period-local for WF-A)
    for lam in LAMBDAS:
        for per, sp, pref in (("FULL", SPY, ""), ("IS", SPY_IS, "IS_"), ("OOS", SPY_OOS, "OOS_")):
            full = per == "FULL"
            bk = dict(H1=G[pref + "H1"], H2=G[pref + "H2"], MaxDD=G[pref + "MaxDD"],
                      CAGR=G[pref + "CAGR"], OOS_Sharpe=G["OOS_Sharpe"])
            mg = leg_margins(bk, sp, lam, full=full)
            legs = LEGS if full else ["H1", "H2", "DD", "CAGR"]
            ok = pd.Series(True, index=G.index)
            for L in legs:
                G[f"m_{per}_{lam}_{L}"] = mg[L]
                G[f"p_{per}_{lam}_{L}"] = mg[L] > 0
                ok &= mg[L] > 0
            G[f"keep4b_{per}_{lam}"] = ok
    G["keep4b"] = G["keep4b_FULL_1.0"]
    _pm = G[[f"p_FULL_1.0_{L}" for L in LEGS]].to_numpy(bool)
    G["fail4b"] = [",".join([L for L, ok in zip(LEGS, row) if not ok]) or "-" for row in _pm]

    # ---------------------------------------------------------------- gates part 2
    P("")
    g5 = len(starts) == 1
    P(f"G5 comparand    : {len(starts)} distinct warm-up start date across all matched frames "
      f"({sorted(starts)[0]}) -> {'PASS' if g5 else 'FAIL'} (one SPY comparand is valid)")
    old = pd.read_csv(f"{P570}.grid.csv")
    key = ["char", "tau", "k", "seed", "side", "arm", "gross", "cadence"]
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "turnover"]
    mg = G.merge(old, on=key, suffixes=("", "_p"))
    g3 = float(np.abs(mg[cmpcols].to_numpy(float)
                      - mg[[c + "_p" for c in cmpcols]].to_numpy(float)).max())
    g3b = int((mg.keep4a.astype(bool) != mg.keep4a_p.astype(bool)).sum()
              + (mg.fail4b != mg.fail4b_p).sum())
    P(f"G3 grid repro   : {len(mg)} of {len(old)} committed rows matched on {len(key)} keys; "
      f"max |d| over {len(cmpcols)} numeric columns = {g3:.3e} (bar {TOL:.0e}); "
      f"{g3b} verdict-string mismatches -> "
      f"{'PASS' if (len(mg) == len(old) and g3 < TOL and g3b == 0) else 'FAIL'}")
    cnt = dict(a4=int(G.keep4a.sum()), b4=int(G.keep4b.sum()),
               both=int((G.keep4a & G.keep4b).sum()),
               ewall=int(G[G.arm == "EWall"].keep4b.sum()),
               mars=int(G[G.arm == "MA-RS"].keep4b.sum()))
    side_c = {s: int(v.keep4b.sum()) for s, v in G.groupby("side")}
    legc = G.fail4b.value_counts()
    g4 = (cnt == PUB_COUNTS and side_c["B"] == PUB_B and side_c["S"] == PUB_S
          and all(int(legc.get(a, 0)) == b for a, b in PUB_LEGS.items()))
    P(f"G4 headline     : 4a {cnt['a4']}/{len(G)}, 4b {cnt['b4']}/{len(G)}, BOTH {cnt['both']}, "
      f"by side B {side_c['B']}/{PUB_N} S {side_c['S']}/{PUB_N}, by arm EWall {cnt['ewall']} "
      f"MA-RS {cnt['mars']}; 6 binding-leg counts "
      f"{[int(legc.get(a,0)) for a in PUB_LEGS]} vs committed {list(PUB_LEGS.values())} -> "
      f"{'PASS' if g4 else 'FAIL'}")
    P("")
    P("  ALL GATES: " + ("PASS" if (g0 < TOL_ID and g1 < TOL_ID and g2 and g5 and g3 < TOL
                                    and g3b == 0 and len(mg) == len(old) and g4) else "FAIL"))

    # ---------------------------------------------------------------- the levels
    P("")
    P("=" * 112)
    P("WHAT THE TWO SIDES ACTUALLY LOOK LIKE (means over each side's 2592 books)")
    P("=" * 112)
    lv = G.groupby("side")[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_MaxDD",
                            "turnover"]].mean()
    P(fmt(lv, 4))
    prem_b, prem_s = float(PR.prem_B.mean()), float(PR.prem_S.mean())
    P(f"  selection premium (mean over {len(PR)} matched draws): B {prem_b:+.4f}  S "
      f"{prem_s:+.4f}  gap {prem_b-prem_s:+.4f}  (idea 570's headline gap range +0.1649..+0.3021)")

    # ---------------------------------------------------------------- leg census
    P("")
    P("=" * 112)
    P("LEG CENSUS - which of the five 4b legs the two sides fail (lambda = 1.00, PROTOCOL 4b)")
    P("=" * 112)
    fl = []
    for s, v in G.groupby("side"):
        d = dict(side=s, n=len(v))
        for L in LEGS:
            d[f"fail_{L}"] = int((~v[f"p_FULL_1.0_{L}"]).sum())
        d["pass4b"] = int(v.keep4b.sum())
        fl.append(d)
    FL = pd.DataFrame(fl).set_index("side")
    P(fmt(FL, 0))
    nf = G[[f"p_FULL_1.0_{L}" for L in LEGS]].to_numpy(bool)
    G["n_fail"] = (~nf).sum(axis=1)
    P("  how many of the five legs each book fails (count of books):")
    P(fmt(G.pivot_table(index="side", columns="n_fail", values="CAGR", aggfunc="size",
                        fill_value=0), 0))
    P("  and, for the books that fail EXACTLY ONE leg, which leg it is:")
    one = G[G.n_fail == 1].copy()
    P(fmt(one.pivot_table(index="side", columns="fail4b", values="CAGR", aggfunc="size",
                          fill_value=0), 0))
    P("  per-leg FAILURE RATE and the B-minus-S difference:")
    fr = FL[[f"fail_{L}" for L in LEGS]].div(FL.n, axis=0)
    fr.loc["B-S"] = fr.loc["B"] - fr.loc["S"]
    P(fmt(fr, 4))
    P("")

    # ---------------------------------------------------------------- the 9 tuned points
    P("=" * 112)
    P("THE ASYMMETRY AT EVERY TUNED POINT (BAR lambda x k), and the LEAVE-ONE-LEG-OUT test")
    P("=" * 112)
    P("  drop_L = pass rate of 4b WITHOUT leg L.  If the asymmetry is carried by leg L, the")
    P("  B/S ratio collapses toward 1 when L is dropped and survives when any other is.")
    crows = []
    for lam in LAMBDAS:
        for k in KS:
            sub = G[G.k == k]
            b, s = sub[sub.side == "B"], sub[sub.side == "S"]
            nb, ns = len(b), len(s)
            pb = b[f"keep4b_FULL_{lam}"].to_numpy(bool)
            ps = s[f"keep4b_FULL_{lam}"].to_numpy(bool)
            r, capped = ratio(int(pb.sum()), int(ps.sum()), nb, ns)
            row = dict(bar=lam, k=k, n_side=nb, pass_B=int(pb.sum()), pass_S=int(ps.sum()),
                       ratio=r, ratio_capped=capped)
            for L in LEGS:
                keep_b = np.ones(nb, bool)
                keep_s = np.ones(ns, bool)
                for L2 in LEGS:
                    if L2 == L:
                        continue
                    keep_b &= b[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
                    keep_s &= s[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
                rr, _ = ratio(int(keep_b.sum()), int(keep_s.sum()), nb, ns)
                row[f"drop{L}_B"] = int(keep_b.sum())
                row[f"drop{L}_S"] = int(keep_s.sum())
                row[f"drop{L}_ratio"] = rr
            # block sub-criteria
            for bl, nmb in ((SHARPE_LEGS, "SHARPEonly"), (LEVEL_LEGS, "LEVELonly")):
                kb = np.ones(nb, bool)
                ks_ = np.ones(ns, bool)
                for L2 in bl:
                    kb &= b[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
                    ks_ &= s[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
                rr, _ = ratio(int(kb.sum()), int(ks_.sum()), nb, ns)
                row[f"{nmb}_B"] = int(kb.sum())
                row[f"{nmb}_S"] = int(ks_.sum())
                row[f"{nmb}_ratio"] = rr
            bb, cc, chi = mcnemar(pb, ps)
            row.update(mcn_Bonly=bb, mcn_Sonly=cc, mcn_chi2=chi)
            crows.append(row)
    CEN = pd.DataFrame(crows)
    P(fmt(CEN.set_index(["bar", "k"])[["n_side", "pass_B", "pass_S", "ratio", "mcn_Bonly",
                                       "mcn_Sonly", "mcn_chi2"]], 3))
    P("")
    P("  LEAVE-ONE-LEG-OUT pass counts (B / S) and the resulting B/S rate ratio:")
    show = ["ratio"] + [f"drop{L}_ratio" for L in LEGS] + ["SHARPEonly_ratio", "LEVELonly_ratio"]
    P(fmt(CEN.set_index(["bar", "k"])[show], 2))
    P("  the same as counts:")
    show2 = ["pass_B", "pass_S"] + [f"drop{L}_{s}" for L in LEGS for s in ("B", "S")] + \
            ["SHARPEonly_B", "SHARPEonly_S", "LEVELonly_B", "LEVELonly_S"]
    P(fmt(CEN.set_index(["bar", "k"])[show2], 0))
    P("")

    # pooled (all k) at each lambda, for the hypothesis lines
    pool_rows = []
    for lam in LAMBDAS:
        b, s = G[G.side == "B"], G[G.side == "S"]
        pb = b[f"keep4b_FULL_{lam}"].to_numpy(bool)
        ps = s[f"keep4b_FULL_{lam}"].to_numpy(bool)
        r, _ = ratio(int(pb.sum()), int(ps.sum()), len(b), len(s))
        d = dict(bar=lam, pass_B=int(pb.sum()), pass_S=int(ps.sum()), ratio=r)
        for L in LEGS:
            kb = np.ones(len(b), bool)
            ks_ = np.ones(len(s), bool)
            for L2 in LEGS:
                if L2 == L:
                    continue
                kb &= b[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
                ks_ &= s[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
            d[f"drop{L}_ratio"] = ratio(int(kb.sum()), int(ks_.sum()), len(b), len(s))[0]
        for bl, nmb in ((SHARPE_LEGS, "SHARPEonly"), (LEVEL_LEGS, "LEVELonly")):
            kb = np.ones(len(b), bool)
            ks_ = np.ones(len(s), bool)
            for L2 in bl:
                kb &= b[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
                ks_ &= s[f"p_FULL_{lam}_{L2}"].to_numpy(bool)
            d[f"{nmb}_B"] = int(kb.sum())
            d[f"{nmb}_S"] = int(ks_.sum())
            d[f"{nmb}_ratio"] = ratio(int(kb.sum()), int(ks_.sum()), len(b), len(s))[0]
        pool_rows.append(d)
    POOL = pd.DataFrame(pool_rows)
    P("  POOLED over k (2592 books per side at every lambda):")
    P(fmt(POOL.set_index("bar"), 2))
    P("")

    # ---------------------------------------------------------------- arm split
    P("=" * 112)
    P("H_PREM's SECOND PREDICTION: is the asymmetry an MA-GATE phenomenon? (arm split)")
    P("=" * 112)
    arows = []
    for lam in LAMBDAS:
        for arm, v in G.groupby("arm"):
            b, s = v[v.side == "B"], v[v.side == "S"]
            pb, ps = b[f"keep4b_FULL_{lam}"], s[f"keep4b_FULL_{lam}"]
            r, capped = ratio(int(pb.sum()), int(ps.sum()), len(b), len(s))
            arows.append(dict(bar=lam, arm=arm, n_side=len(b), pass_B=int(pb.sum()),
                              pass_S=int(ps.sum()), ratio=r, capped=capped))
    AR = pd.DataFrame(arows)
    P(fmt(AR.set_index(["bar", "arm"]), 2))
    a1 = AR[(AR.bar == 1.0)].set_index("arm")
    P(f"  EWall carries NO selection at all, and its books are {int(a1.loc['EWall','pass_B'])} B "
      f"vs {int(a1.loc['EWall','pass_S'])} S; MA-RS {int(a1.loc['MA-RS','pass_B'])} vs "
      f"{int(a1.loc['MA-RS','pass_S'])}.")
    P("")

    # ---------------------------------------------------------------- conditioning
    P("=" * 112)
    P("H_COND: does conditioning on the book's OWN return statistic remove the asymmetry?")
    P("=" * 112)
    P("  Strata = deciles of the pooled (B+S) distribution of the conditioning variable.")
    P("  MH_OR = Mantel-Haenszel common odds ratio; STD_DIFF = stratum-size-weighted B-S rate.")
    cond_rows = []
    for lam in LAMBDAS:
        b = G[G.side == "B"].sort_values(key).reset_index(drop=True)
        s = G[G.side == "S"].sort_values(key).reset_index(drop=True)
        pb = b[f"keep4b_FULL_{lam}"].to_numpy(bool)
        ps = s[f"keep4b_FULL_{lam}"].to_numpy(bool)
        crude = crude_odds(pb, ps)
        for var, tag in (("Sharpe", "Sharpe (the premium's own unit)"),
                         ("CAGR", "CAGR"),
                         ("MaxDD", "MaxDD  [TAUTOLOGY CHECK - the DD leg is in the outcome]")):
            allv = np.concatenate([b[var].to_numpy(float), s[var].to_numpy(float)])
            edges = np.quantile(allv, np.linspace(0, 1, 11))
            edges[0], edges[-1] = -np.inf, np.inf
            sb = np.digitize(b[var].to_numpy(float), edges[1:-1])
            ss = np.digitize(s[var].to_numpy(float), edges[1:-1])
            mh, sd_ = mh_odds(pb, sb, ps, ss)
            # tighter still: keep only the PAIRS whose two books land in the same decile
            same = sb == ss
            mh2, sd2 = mh_odds(pb[same], sb[same], ps[same], ss[same])
            cond_rows.append(dict(bar=lam, cond=tag, crude_OR=crude, MH_OR=mh, STD_DIFF=sd_,
                                  n_same_decile=int((sb == ss).sum()),
                                  MH_OR_samedecile=mh2, STD_DIFF_samedecile=sd2))
    CO = pd.DataFrame(cond_rows)
    P(fmt(CO.set_index(["bar", "cond"]), 3))
    P("")

    # ---------------------------------------------------------------- margins
    P("=" * 112)
    P("WHERE THE TWO SIDES SEPARATE: paired per-leg MARGIN (positive = leg passes), lambda=1")
    P("=" * 112)
    b = G[G.side == "B"].sort_values(key).reset_index(drop=True)
    s = G[G.side == "S"].sort_values(key).reset_index(drop=True)
    assert (b[[c for c in key if c != "side"]].to_numpy()
            == s[[c for c in key if c != "side"]].to_numpy()).all(), "pairing broken"
    mrows = []
    for L in LEGS:
        db = b[f"m_FULL_1.0_{L}"].to_numpy(float)
        ds = s[f"m_FULL_1.0_{L}"].to_numpy(float)
        d = db - ds
        sd_all = float(np.std(np.concatenate([db, ds]), ddof=1))
        mrows.append(dict(leg=L, margin_B=float(db.mean()), margin_S=float(ds.mean()),
                          diff=float(d.mean()), sd_pairdiff=float(d.std(ddof=1)),
                          t=float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))),
                          cohens_d=float(d.mean() / sd_all),
                          share_B_passes=float((db > 0).mean()),
                          share_S_passes=float((ds > 0).mean()),
                          perm_p=perm_p(d)))
    MG = pd.DataFrame(mrows).set_index("leg")
    P(fmt(MG, 4))
    P(f"  permutation: {NPERM} sign-flips of the matched-pair label, seed 784, two-sided.")
    P("")

    # ---------------------------------------------------------------- H_LINK
    P("=" * 112)
    P("H_LINK: does the per-draw PREMIUM gap predict the per-draw PASS gap? (216 draws)")
    P("=" * 112)
    pg = G.groupby(["char", "tau", "k", "seed", "side"]).keep4b.sum().unstack("side")
    pg.columns = ["pass_B", "pass_S"]
    LK = PR.set_index(["char", "tau", "k", "seed"]).join(pg)
    LK["prem_gap"] = LK.prem_B - LK.prem_S
    LK["pass_gap"] = LK.pass_B - LK.pass_S
    x, y = LK.prem_gap.to_numpy(float), LK.pass_gap.to_numpy(float)
    pear = float(np.corrcoef(x, y)[0, 1])
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    spear = float(np.corrcoef(rx, ry)[0, 1])
    rng = np.random.default_rng(7841)
    null = np.array([abs(np.corrcoef(x, rng.permutation(y))[0, 1]) for _ in range(2000)])
    plink = float((1 + np.sum(null >= abs(pear) - 1e-15)) / 2001)
    P(f"  n = {len(LK)} draws; premium gap mean {x.mean():+.4f} (sd {x.std(ddof=1):.4f}); "
      f"pass gap mean {y.mean():+.3f} of 12 books per side (sd {y.std(ddof=1):.3f})")
    P(f"  Pearson rho {pear:+.4f}  Spearman {spear:+.4f}  permutation p {plink:.4f} "
      f"(2000 draws) -> H_LINK {'HOLDS' if abs(spear) >= 0.30 else 'FALSIFIED'} (bar |rho| 0.30)")
    P("  pass gap by premium-gap quartile (does more premium buy more passes?):")
    LK["q"] = pd.qcut(LK.prem_gap, 4, labels=["Q1 low", "Q2", "Q3", "Q4 high"])
    P(fmt(LK.groupby("q", observed=True)[["prem_gap", "pass_B", "pass_S", "pass_gap"]].mean(), 3))
    P("")

    # ---------------------------------------------------------------- rule 8 WF-A
    P("=" * 112)
    P("RULE 8 WF-A: the same census with every leg computed INSIDE IS only and INSIDE OOS only")
    P("=" * 112)
    P("  period-local 4b (4 legs): both halves of the period vs SPY, the period's DD cap, the")
    P("  period's CAGR floor.  FULL is shown in the same 4-leg form so the three are comparable.")
    wrows = []
    for per in ("FULL", "IS", "OOS"):
        for lam in LAMBDAS:
            for k in KS:
                sub = G[G.k == k]
                bb, ss = sub[sub.side == "B"], sub[sub.side == "S"]
                legs4 = ["H1", "H2", "DD", "CAGR"]
                kb = np.ones(len(bb), bool)
                ks_ = np.ones(len(ss), bool)
                for L in legs4:
                    kb &= bb[f"p_{per}_{lam}_{L}"].to_numpy(bool)
                    ks_ &= ss[f"p_{per}_{lam}_{L}"].to_numpy(bool)
                r, capped = ratio(int(kb.sum()), int(ks_.sum()), len(bb), len(ss))
                row = dict(period=per, bar=lam, k=k, n_side=len(bb), pass_B=int(kb.sum()),
                           pass_S=int(ks_.sum()), ratio=r, capped=capped)
                for L in legs4:
                    db = np.ones(len(bb), bool)
                    ds = np.ones(len(ss), bool)
                    for L2 in legs4:
                        if L2 == L:
                            continue
                        db &= bb[f"p_{per}_{lam}_{L2}"].to_numpy(bool)
                        ds &= ss[f"p_{per}_{lam}_{L2}"].to_numpy(bool)
                    row[f"drop{L}_ratio"] = ratio(int(db.sum()), int(ds.sum()),
                                                  len(bb), len(ss))[0]
                    row[f"fail{L}_B"] = float((~bb[f"p_{per}_{lam}_{L}"]).mean())
                    row[f"fail{L}_S"] = float((~ss[f"p_{per}_{lam}_{L}"]).mean())
                wrows.append(row)
    WFA = pd.DataFrame(wrows)
    P(fmt(WFA.set_index(["period", "bar", "k"])[
        ["pass_B", "pass_S", "ratio"] + [f"drop{L}_ratio" for L in ["H1", "H2", "DD", "CAGR"]]], 2))
    P("")
    P("  per-leg FAILURE RATE by period and side (lambda = 1.00, pooled over k):")
    frs = []
    for per in ("FULL", "IS", "OOS"):
        for side, v in G.groupby("side"):
            d = dict(period=per, side=side)
            for L in ["H1", "H2", "DD", "CAGR"]:
                d[f"fail_{L}"] = float((~v[f"p_{per}_1.0_{L}"]).mean())
            frs.append(d)
    P(fmt(pd.DataFrame(frs).set_index(["period", "side"]), 4))
    sgn = WFA.pivot_table(index=["bar", "k"], columns="period", values="ratio", dropna=False)
    defined = sgn["IS"].notna() & sgn["OOS"].notna()
    agree = int(((sgn["IS"] > 1) & (sgn["OOS"] > 1) & defined).sum())
    P("")
    P(f"  the asymmetry points the same way (B > S) in IS and OOS at {agree} of "
      f"{int(defined.sum())} tuned points where both are defined ({len(sgn)-int(defined.sum())} "
      f"points have no passer on EITHER side in one period); ratio IS "
      f"{sgn['IS'].min():.2f}-{sgn['IS'].max():.2f}, OOS "
      f"{sgn['OOS'].min():.2f}-{sgn['OOS'].max():.2f}")
    P("")

    # ---------------------------------------------------------------- rule 8 WF-B
    P("=" * 112)
    P("RULE 8 WF-B: the census priced as a BOOK - pick (char, tau, k) on IS 4b pass rate of the")
    P("             B side (tie-break IS Sharpe); OOS read ONCE.")
    P("=" * 112)
    sel = G[(G.side == "B")].groupby(["char", "tau", "k"]).agg(
        IS_pass=(f"keep4b_IS_1.0", "mean"), IS_Sharpe=("IS_Sharpe", "mean")).reset_index()
    P(fmt(sel.set_index(["char", "tau", "k"]), 4))
    sel = sel.sort_values(["IS_pass", "IS_Sharpe"], ascending=False)
    best = (sel.iloc[0]["char"], float(sel.iloc[0]["tau"]), int(sel.iloc[0]["k"]))
    P(f"  IS-best point: char={best[0]}, tau={best[1]}, k={best[2]}  (IS 4b pass rate "
      f"{sel.iloc[0]['IS_pass']:.4f}, IS Sharpe {sel.iloc[0]['IS_Sharpe']:.4f})")

    MATCH = {}
    for ch in CHARS:
        for tau in TAUS:
            for k in KS:
                for sd in SEEDS:
                    pr = greedy_match(nc, bnames, snames, ch, tau, k, sd)
                    if len(pr) == k:
                        MATCH[(ch, tau, k, sd)] = ([p[0] for p in pr], [p[1] for p in pr])

    def pooled_book(char, tau, k, which):
        segs = []
        for sd in SEEDS:
            got = MATCH.get((char, tau, k, sd))
            if got is None:
                continue
            B_, S_ = got
            names = {"B": B_, "S": S_, "BLIND": B_ + S_}[which]
            cols = list(dict.fromkeys(list(names) + ["SPY"]))
            pxd = pd.concat([pool[list(names)], spy_pool.rename("SPY")], axis=1)[cols] \
                .dropna(how="all").ffill()
            w = make_books(pxd, set(names), 0.75)["MA-RS"]
            segs.append(fast_backtest(pxd, w, COST, "W")["returns"].iloc[start_i:])
        idx = segs[0].index
        return pd.concat([x.reindex(idx).fillna(0.0) for x in segs], axis=1).mean(axis=1)

    u56px, u56tr = panels["U56"]
    st56 = u56px.index[260]
    v2_56 = fast_backtest(u56px, rules_v2_weights(u56px), COST, "W")["returns"].loc[st56:]
    spy56 = u56px["SPY"].pct_change().fillna(0.0).loc[st56:]
    pxB_pool = pd.concat([pool[bnames], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    b136_full = fast_backtest(pxB_pool, make_books(pxB_pool, set(bnames), 0.75)["MA-RS"],
                              COST, "W")["returns"].iloc[start_i:]
    pxS_pool = pd.concat([pool[snames], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    small_full = fast_backtest(pxS_pool, make_books(pxS_pool, set(snames), 0.75)["MA-RS"],
                               COST, "W")["returns"].iloc[start_i:]

    wf_rows = []
    for nm, r in (("B-side (IS pick)", pooled_book(*best, "B")),
                  ("S-side twin", pooled_book(*best, "S")),
                  ("ORIGIN-BLIND control", pooled_book(*best, "BLIND")),
                  ("INCUMBENT B136 MA-RS g0.75 W", b136_full),
                  ("SMALL439 MA-RS g0.75 W", small_full),
                  ("RULES v2 U56 (live book)", v2_56),
                  ("SPY", spy56)):
        arr = r.to_numpy(float)
        if len(arr) == len(spy_full):
            bk = periodstats(arr)
            bk["OOS_Sharpe"] = periodstats(arr[oos_m])["Sharpe"]
            mo = periodstats(arr[oos_m])
            mrg = leg_margins(bk, SPY, 1.0, full=True)
        else:                                   # U56 frame: its own SPY window
            s56 = spy56.reindex(r.index).fillna(0.0).to_numpy(float)
            om = np.asarray(r.index >= pd.Timestamp(OOS_START))
            bk = periodstats(arr)
            bk["OOS_Sharpe"] = periodstats(arr[om])["Sharpe"]
            sp = periodstats(s56)
            sp["OOS_Sharpe"] = periodstats(s56[om])["Sharpe"]
            mo = periodstats(arr[om])
            mrg = leg_margins(bk, sp, 1.0, full=True)
        f = fails_of(mrg, LEGS)
        wf_rows.append(dict(book=nm, CAGR=bk["CAGR"], Sharpe=bk["Sharpe"], MaxDD=bk["MaxDD"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            keep4a=keep_4a(r, v2_56.reindex(r.index).fillna(0.0)),
                            fail4b=",".join(f) or "-", keep4b=not f))
    WF = pd.DataFrame(wf_rows)
    P(fmt(WF.set_index("book"), 4))
    bs = float(WF[WF.book == "RULES v2 U56 (live book)"].OOS_Sharpe.iloc[0])
    ss = float(WF[WF.book == "SPY"].OOS_Sharpe.iloc[0])
    cand = WF[WF.book.isin(["B-side (IS pick)", "S-side twin", "ORIGIN-BLIND control"])]
    P(f"  decision books beating RULES v2 U56 OOS Sharpe ({bs:.4f}): "
      f"{int((cand.OOS_Sharpe > bs).sum())}/3; beating SPY ({ss:.4f}): "
      f"{int((cand.OOS_Sharpe > ss).sum())}/3")
    P(f"  decision books: 4a {int(cand.keep4a.sum())}/3, 4b {int(cand.keep4b.sum())}/3, "
      f"BOTH {int((cand.keep4a & cand.keep4b).sum())}/3")
    bside = pooled_book(*best, "B")
    ix2 = bside.index.intersection(b136_full.index)
    corr = float(np.corrcoef(bside.reindex(ix2).fillna(0.0),
                             b136_full.reindex(ix2).fillna(0.0))[0, 1])
    P(f"  B-side book vs the incumbent whole-B136 MA-RS gate, daily-return correlation: "
      f"{corr:.4f}")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 112)
    P("KEEP PATHS (PROTOCOL 4a and 4b, every book on the grid and every decision book)")
    P("=" * 112)
    P(f"  matched grid ({len(G)} books): 4a {int(G.keep4a.sum())}, 4b {int(G.keep4b.sum())}, "
      f"BOTH {int((G.keep4a & G.keep4b).sum())}  [G4 reproduction of idea 570: "
      f"{'EXACT' if g4 else 'MISMATCH'}]")
    P(f"  by side: B 4a {int(G[G.side=='B'].keep4a.sum())} 4b {int(G[G.side=='B'].keep4b.sum())}"
      f" | S 4a {int(G[G.side=='S'].keep4a.sum())} 4b {int(G[G.side=='S'].keep4b.sum())}")
    P(f"  decision books (WF-B): 4a {int(cand.keep4a.sum())}/3, 4b {int(cand.keep4b.sum())}/3, "
      f"BOTH {int((cand.keep4a & cand.keep4b).sum())}/3")
    P("  A matched draw is a DIAGNOSTIC panel, not a tradable rule: no book on this grid is a")
    P("  capital candidate whatever it passes, as idea 570 stated when it built the grid.")
    P("")

    # ---------------------------------------------------------------- verdicts
    P("=" * 112)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 112)
    p1 = POOL[POOL.bar == 1.0].iloc[0]
    sh_ratio = float(p1.SHARPEonly_ratio)
    lv_ratio = float(p1.LEVELonly_ratio)
    full_ratio = float(p1.ratio)
    dropDD = float(p1.dropDD_ratio)
    dropSh = max(float(p1[f"drop{L}_ratio"]) for L in SHARPE_LEGS)
    minSh = min(float(p1[f"drop{L}_ratio"]) for L in SHARPE_LEGS)
    P(f"H_PREM (i)  : SHARPE-only sub-criterion B/S ratio {sh_ratio:.2f} vs full-4b "
      f"{full_ratio:.2f} (bar: half, {full_ratio/2:.2f}) -> "
      f"{'HOLDS' if sh_ratio >= full_ratio / 2 else 'FALSIFIED'}")
    ew = AR[(AR.bar == 1.0) & (AR.arm == "EWall")].iloc[0]
    ma = AR[(AR.bar == 1.0) & (AR.arm == "MA-RS")].iloc[0]
    P(f"H_PREM (ii) : EWall (no selection) ratio {ew.ratio:.2f}"
      f"{' [S side empty, continuity-corrected]' if bool(ew.capped) else ''} vs MA-RS "
      f"{ma.ratio:.2f}{' [S side empty, continuity-corrected]' if bool(ma.capped) else ''} -> "
      f"{'HOLDS' if ma.ratio > 2 * ew.ratio else 'FALSIFIED - the arm WITHOUT a gate is as asymmetric'}")
    P(f"H_DD        : dropping DD moves the ratio to {dropDD:.2f} = {dropDD/full_ratio:.2f}x of "
      f"full (bar 0.50x); dropping a SHARPE leg leaves it at {minSh:.2f}-{dropSh:.2f} = "
      f"{minSh/full_ratio:.2f}x-{dropSh/full_ratio:.2f}x (bar 0.80x); LEVEL-only ratio "
      f"{lv_ratio:.2f} -> "
      f"{'HOLDS' if (dropDD < 0.5 * full_ratio and minSh > 0.8 * full_ratio) else 'FALSIFIED'}")
    c1 = CO[(CO.bar == 1.0)].set_index("cond")
    shr = c1.loc["Sharpe (the premium's own unit)"]
    P(f"H_COND      : crude OR {shr.crude_OR:.2f} -> Sharpe-decile MH OR {shr.MH_OR:.2f} "
      f"({shr.MH_OR/shr.crude_OR:.2f}x of crude) -> "
      f"{'HOLDS - return-carried' if shr.MH_OR < 0.5 * shr.crude_OR else 'FALSIFIED - conditioning on return does NOT remove it'}")
    P(f"H_LINK      : Spearman {spear:+.4f} (bar 0.30) -> "
      f"{'HOLDS' if abs(spear) >= 0.30 else 'FALSIFIED'}")
    P("")
    P("SURVIVORSHIP: both panels are CURRENT constituents; SMALL439 is the heavier screen, and a")
    P("  differential survivorship premium would push the SAME way as every number above. This")
    P("  design controls the characteristic and the width, NOT the listing history - idea 782.")
    P("")

    # ---------------------------------------------------------------- write
    keep_cols = [c for c in G.columns if not c.startswith(("m_", "p_"))]
    G[keep_cols].to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    MG.reset_index().to_csv(OUT / f"{STAMP}.legs.csv", index=False)
    CEN.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    pd.concat([WFA.assign(leg="WF-A"), WF.assign(leg="WF-B"), CO.assign(leg="COND"),
               POOL.assign(leg="POOLED"), AR.assign(leg="ARM")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    G[["char", "tau", "k", "seed", "side", "arm", "gross", "cadence", "keep4a", "fail4b",
       "keep4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    LK.reset_index().to_csv(OUT / f"{STAMP}.link.csv", index=False)
    P(f"wrote grid {len(G)}, census {len(CEN)}, WF-A {len(WFA)}, link {len(LK)} in "
      f"{time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
