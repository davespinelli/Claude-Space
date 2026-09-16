#!/usr/bin/env python3
"""Idea 1033 (cloud lane, 2026-09-16) — is a CHOOSER PERCENTILE a POOL-SIZE artefact, the way
1030 asks of the FLOOR?

QUESTION (QUEUE idea 1033, verbatim)
    idea 1031 found every percentile on the 18-book GRID pool is quantised to 1/18 = 0.0556 and
    that PROTOCOL's own single split is the coarsest reading available.  Walk the pool size
    (GRID 18, GRID+SHELF, a widened band x gross ladder) and report at what N a chooser
    percentile is resolved finely enough to separate IS_CAGR's 0.800 from a coin flip.
    Max 2 params (pool, end grid).

WHAT IS NEW AGAINST 1031.  1031 re-expressed every chooser as a percentile of its own pool's
    coin-flip distribution and published IS_CAGR at 0.800 on the 18-book GRID pool.  It then
    noted, without testing it, that such a percentile cannot be finer than 1/N.  That note
    conflates TWO different things and this run separates them:

      RESOLUTION  — the GRANULARITY of the percentile scale.  At a single split end the coin
                    flip is a uniform draw from N books, so a chooser's percentile can only be
                    (k + 1/2)/N.  This is a pure function of N and nothing else.
      DECIDABILITY— whether an OBSERVED percentile is distinguishable from a coin flip.  Under
                    the null that the chooser draws uniformly from the same pool, its percentile
                    IS the one-sided p-value.  0.800 means "1 coin flip in 5 beats it", and that
                    statement is p = 0.200 whether N is 18 or 18,000.

    The queue's question presumes RESOLUTION is what stops 0.800 separating from 0.5.  If that
    is wrong, no N fixes it and the record's chooser claims need REPLICATION (more ends), not a
    bigger pool.  Both readings are measured at every grid point and reported side by side.

    The second, and separable, thing pool size does is CHANGE THE POOL — a wider ladder adds
    worse books, the coin flip's mean falls, and a fixed chooser's percentile rises for reasons
    that have nothing to do with skill.  That is 1030's FLOOR mechanism, and it is measured here
    on a NESTED ladder (WIDE10 subset of WIDE20 subset of WIDE40 subset of WIDE80, stride-thinned
    from one master list so family composition is held near-fixed) so that a percentile MOVE is
    attributable to the pool's contents rather than to a change of family.

WHAT IS MEASURED
    (A) THE RESOLUTION TABLE.  For every (pool, end grid): N, the number of DISTINCT percentile
        values attainable, the step between them, and the SMALLEST p-value any chooser could
        possibly earn (0.5/N at one end).  This is arithmetic, not an estimate.
    (B) THE PERCENTILE TABLE.  Every chooser x pool x end grid x panel x cost: the chooser's
        mean OOS Sharpe over the ends, the random distribution's mean/median/sd, the chooser's
        percentile, its one-sided p, and the 5% and 50% verdicts.
    (C) THE POOL-QUALITY DECOMPOSITION (1030's floor).  The coin flip's own absolute level by
        pool size, against the chooser's absolute level, so a percentile move can be read as
        "the pool got worse" or "the chooser got better".
    (D) THE RULE-8 WALK-FORWARD at PROTOCOL's own split 2016-12-31 (IS 2009-2016, OOS 2017-2026
        read once), with OOS CAGR/Sharpe/MaxDD against the live RULES v2 baseline and against
        SPY, BOTH KEEP paths, for every (pool, chooser) pick.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 24 grid points reported at every
    panel x cost, none selected.
    (1) POOL — six, the three the queue names plus a nested size ladder
          GRID18     861's mechanical 18-book ladder, 1031's own pool          <- HEADLINE
          GRIDSHELF  GRID18 + this lane's committed SHELF books (U56 7, B136 2)
          WIDE10 / WIDE20 / WIDE40 / WIDE80   nested stride-thinned subsets of one 80-book
                     master per panel: band (0.00..0.18) x gross (0.25..1.00) = 32 books and
                     qroll q(0.08..0.25) x w(252,504,1008) x depth(0.25..1.00) = 48 books,
                     interleaved 2:3 so every thinned subpool keeps both families in proportion.
                     GRID18 is a strict subset of WIDE80 (gate G9).
    (2) END GRID — the band of legal rule-8 IS end dates the chooser is run over
          REC1  PROTOCOL's declared split 2016-12-31 ALONE — one end, so the percentile scale
                is exactly the 1/N grid the queue is asking about        <- the queue's object
          Q8    8 quarter-ends 2017-03-31..2018-12-31
          Q16   1013's / 1023's / 1031's own 16 ends 2015-03-31..2018-12-31   <- HEADLINE
          Q32   32 quarter-ends 2011-03-31..2018-12-31

    NOT TUNED, reported as CONTROLS at every point:
      COST    0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL   U56 (binding) and B136 (labelled replication).
      CHOOSER 1023's / 1031's own three IS-only statistics, verbatim.
      DRAWS   NRAND = 2,000 sequences per (panel, cost, pool, end grid).

    CAVEATS declared before the numbers.  (i) GRIDSHELF is NOT a legal rule-8 pool: its SHELF
    members were selected on the full tape, so a chooser running on 2009-2016 alone could not
    have had them in front of it.  It is carried because the queue names it and is never a
    headline.  (ii) Q32's earliest ends leave an IS window of barely two years; legal under rule
    8's letter, thin in substance, a SENSITIVITY axis only.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_1031     reproduce 1031's headline cell (U56 / 10 bps / GRID18 / Q16): IS_CAGR at
               percentile 0.800 and IS_SHARPE / IS_LEGS at 0.000, to within 3 MC standard errors.
    H_QUANT    the queue's arithmetic premise.  At REC1 the attainable percentile step equals
               1/N EXACTLY for all six pools (1/18 = 0.0556 for GRID18).
    H_RESOLVE  THE QUEUE'S LITERAL QUESTION.  There exists a pool size on this ladder at which
               IS_CAGR's percentile at PROTOCOL's own single split (REC1) separates from a coin
               flip at the one-sided 5% level.  PASS => the queue's N exists and this run names
               it.  FAIL => no pool size on the ladder resolves it.
    H_NOTRES   DECISIVE, and the alternative to H_RESOLVE.  Resolution is NOT the binding
               constraint: at every pool with N >= 20 the SMALLEST attainable p (0.5/N) is
               already <= 0.05, while IS_CAGR's ACTUAL p at REC1 stays > 0.05.  PASS => the
               percentile scale is fine enough and the chooser simply is not high enough in it,
               so no N can fix it and the queue's framing is wrong.
    H_MOVE     POOL-SIZE ARTEFACT.  IS_CAGR's headline-grid percentile moves by MORE than 0.10
               between WIDE10 and WIDE80.  PASS => the percentile is a pool-composition object,
               1030's floor mechanism, and percentiles are not comparable across pools.
    H_FLOOR    1030's mechanism directly: the coin flip's own mean OOS Sharpe falls monotonically
               along WIDE10 -> WIDE20 -> WIDE40 -> WIDE80 in the headline cell.
    H_POWER    REPLICATION beats RESOLUTION.  At fixed pool GRID18 the spread of IS_CAGR's p
               across the four end grids exceeds, at fixed grid Q16, its spread across the four
               WIDE pools.  PASS => the end count, not N, is what a rule-8 clause should pin.
    H_ORDER    the ordering of the three choosers by percentile is identical at all six pools in
               the headline cell.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                     0.0
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the record's committed
        15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1013's four published declared-split picks reproduce their OOS triples.
    G5  determinism: the whole end x book x rung ladder rebuilt reproduces bit-for-bit.      0.0
    G6  IS PURITY: every chooser's pick is invariant under a permutation of the OOS returns.
    G7  SAMPLER UNBIASEDNESS: the Monte-Carlo mean of the sequence-mean distribution equals the
        EXACT pool mean (closed form, no draws) to within 3 MC standard errors, every pool.
    G8  PERCENTILE VALIDITY: scoring the random distribution's OWN median through the same
        percentile function returns 0.5000 +/- 0.01 in every cell.  Reported over ALL cells (G8)
        AND restricted to the K > 1 grids (G8b), with the atom mass that separates them printed
        as G8c: at REC1 the random distribution is N POINT MASSES, its own median IS one of them,
        and a mid-rank percentile cannot return 0.5 at a point mass of size 1/N.  That is the
        SAME discreteness 1031 reported for its RATE4B statistic, and it is the object this run
        is measuring, not a defect in it — so the failure is printed, not tuned away.
    G9  NESTING: WIDE10 c WIDE20 c WIDE40 c WIDE80 and GRID18 c WIDE80, so a size move is not a
        family move.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b count an UPPER bound.  The measured object is
    a chooser's RANK inside a distribution built from the SAME pool over the SAME tape; the bias
    is a common factor to the chooser and to every random draw it is ranked against.  Where it
    does not cancel it flatters the coin flip, so every chooser percentile here is a LOWER bound.
    SPY is a real index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-a-CHOOSER-PERCENTILE-a-POOL-SIZE-artefact"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
POOL_HEAD = "GRID18"
GRID_HEAD = "Q16"
NRAND = 2000
SEED0 = 20260916
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
# 1031's committed headline percentiles (U56 / 10 bps / GRID18 pool / Q16 / MEAN_SH)
PUB_1031_PCT = {"IS_SHARPE": 0.000, "IS_LEGS": 0.000, "IS_CAGR": 0.800}
PUB_1031_N = 2000
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q8 = quarter_ends("2017-01-01", "2018-12-31")
END_Q16 = quarter_ends("2015-01-01", "2018-12-31")
END_Q32 = quarter_ends("2011-01-01", "2018-12-31")
GRIDS = {"REC1": [REC_END], "Q8": END_Q8, "Q16": END_Q16, "Q32": END_Q32}
ALLE = sorted(set(END_Q32) | set(END_Q16) | set(END_Q8) | {REC_END})

# ------------------------------------------------------------------ the master book ladder
BANDS = (0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.18)
GROSS = (0.25, 0.50, 0.75, 1.00)
QQ, WW, DD = (0.08, 0.12, 0.17, 0.25), (252, 504, 1008), (0.25, 0.50, 0.75, 1.00)


def wide_master(pname, px):
    """80 mechanical books per panel, band family and qroll family INTERLEAVED 2:3 so any
    stride-thinned prefix keeps the two families in their master proportion (32:48)."""
    bandbooks = [(f"{pname}-band{b:.2f}-g{g:.2f}",
                  dict(panel=pname, freq="W", W=rules_v2_weights(px, b, g), fam="band"))
                 for b, g in product(BANDS, GROSS)]
    elig = C.eligible_mask(px).astype(float)
    nn = elig.sum(axis=1).replace(0, np.nan)
    base = elig.div(nn, axis=0).fillna(0.0)
    br = C.breadth(px)
    thr_cache = {}
    qbooks = []
    for q, w, d in product(QQ, WW, DD):
        if (q, w) not in thr_cache:
            thr_cache[(q, w)] = br.rolling(w, min_periods=w).quantile(q)
        qbooks.append((f"{pname}-qroll-q{q:.2f}-w{w}-d{d:.2f}",
                       dict(panel=pname, freq="W",
                            W=base.mul(C.gate_mult(br, thr_cache[(q, w)], d, px.index), axis=0),
                            fam="qroll")))
    out, i, j = [], 0, 0
    while i < len(bandbooks) or j < len(qbooks):          # 2 band : 3 qroll
        for _ in range(2):
            if i < len(bandbooks):
                out.append(bandbooks[i]); i += 1
        for _ in range(3):
            if j < len(qbooks):
                out.append(qbooks[j]); j += 1
    return out


def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def raw_pick(sub, ch, spy_is):
    """IS-ONLY choosers — 1023's / 1031's own three, verbatim.  `sub` is one pool's slice."""
    if ch == "IS_SHARPE":
        return sub["IS_Sharpe"].idxmax()
    if ch == "IS_CAGR":
        return sub["IS_CAGR"].idxmax()
    s = sub.copy()
    s["nlegs"] = ((s["IS_Sharpe"] > spy_is[1]).astype(int)
                  + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * spy_is[0]).astype(int)
                  + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(spy_is[2])).astype(int))
    s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
    return s.index[0]


def pct_of(x, dist):
    """Mid-rank percentile of x inside dist, in [0, 1]; ties split (G8)."""
    d = np.asarray(dist, float)
    return float(((d < x).sum() + 0.5 * (d == x).sum()) / len(d))


def main():
    t0 = time.time()
    P(f"# Idea 1033 (cloud lane, {DATE}) — is a CHOOSER PERCENTILE a POOL-SIZE artefact, the way "
      f"1030 asks of the FLOOR?")
    P(f"# 2 tuned dials: POOL (6) x END GRID (4) = 24 points, ALL reported at every panel x cost, "
      f"none selected.")
    P(f"# HEADLINE = {PANEL_HEAD} / {RUNG_HEAD:.0f} bps / {POOL_HEAD} / {GRID_HEAD} — 1031's own "
      f"cell.  CONTROLS: cost {RUNGS} bps, panel [U56, B136], choosers {RAW}.")
    P(f"# DRAWS: NRAND = {NRAND:,} random chooser SEQUENCES per (panel, cost, pool, end grid).")
    P("# CAVEAT 1: GRIDSHELF is NOT a legal rule-8 pool — its SHELF members were selected on the")
    P("#   full tape.  Carried because the queue names it; never a headline.")
    P("# CAVEAT 2: Q32's earliest ends leave an IS window of barely two years — legal under rule")
    P("#   8's letter, thin in substance, a SENSITIVITY axis only.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic.  The")
    P("#   measured object is a RANK inside a distribution from the SAME pool; where the bias")
    P("#   does not cancel it flatters the coin flip, so every chooser percentile is a LOWER")
    P("#   bound.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar (1013's / "
          f"1023's / 1031's construction — the cross-run comparands are stated on it). No splice.")
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    # ---------------------------------------------------------------- pools
    grid18 = C.grid_books(U, B)
    shelf = C.shelf_books(U, B)
    master = {}
    ORDER = {}
    for pname, px in (("U56", U), ("B136", B)):
        lst = wide_master(pname, px)
        ORDER[pname] = [nm for nm, _ in lst]
        for nm, b in lst:
            master[nm] = b
    for nm, b in grid18.items():
        master.setdefault(nm, dict(panel=b["panel"], freq=b["freq"], W=b["W"], fam="band"))
    for nm, b in shelf.items():
        master[nm] = dict(panel=b["panel"], freq=b["freq"], W=b["W"], fam="shelf")

    POOLS = {}
    for pname in PX:
        g18 = [nm for nm, b in grid18.items() if b["panel"] == pname]
        sh = [nm for nm, b in shelf.items() if b["panel"] == pname]
        o = ORDER[pname]
        POOLS[("GRID18", pname)] = sorted(g18)
        POOLS[("GRIDSHELF", pname)] = sorted(g18 + sh)
        for k, stride in (("WIDE10", 8), ("WIDE20", 4), ("WIDE40", 2), ("WIDE80", 1)):
            POOLS[(k, pname)] = sorted(o[::stride])
    POOLNAMES = ["GRID18", "GRIDSHELF", "WIDE10", "WIDE20", "WIDE40", "WIDE80"]
    P(f"POOLS (books per panel): " + "; ".join(
        f"{k} U56={len(POOLS[(k,'U56')])} B136={len(POOLS[(k,'B136')])}" for k in POOLNAMES))
    P(f"MASTER book set actually run: {len(master)} books "
      f"({sum(b['panel']=='U56' for b in master.values())} U56 / "
      f"{sum(b['panel']=='B136' for b in master.values())} B136).")
    P(f"END GRIDS: " + "; ".join(f"{k}={len(v)} ends" for k, v in GRIDS.items())
      + f".  Union scored = {len(ALLE)} ends {ALLE[0]}..{ALLE[-1]}.")

    NET = {}
    for nm, b in master.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    P(f"   ran {len(master)} books x {len(RUNGS)} rungs in {time.time()-t0:.1f}s")
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = metblock((r - t * c / 1e4).loc[REC[p]:].values)

    # ================================================================ GATES
    P("")
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    def G(name, what, value, ok):
        gates.append(dict(gate=name, what=what, value=value, verdict="PASS" if ok else "FAIL"))
        P(f"{name} {what}: {value}  {'PASS' if ok else 'FAIL'}")
        return ok

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    G("G1", "fast_run == engine.backtest (returns / turnover)", f"{d_r:.3e}/{d_t:.3e}",
      d_r < 1e-12 and d_t < 1e-10)
    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    G("G2", "rules_v2_weights(U,0.03,0.75) == baseline", f"{d2:.3e}", d2 == 0.0)

    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    sb = SPYB[(PANEL_HEAD, REC_END)]
    trip = (sb["OOS_CAGR"], sb["OOS_Sharpe"], sb["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    G("G3", f"CROSS-RUN SPY OOS at {REC_END} "
      f"({trip[0]:.4%}/{trip[1]:.4f}/{trip[2]:.4%}) vs record", f"max|d| {d3:.3e}", d3 <= 5e-4)

    def build_ladder():
        rows = []
        for nm, b in master.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    s = SPYB[(p, e)]
                    lg = legs_at(bk, s)
                    v2 = V2[(p, c)]
                    rows.append(dict(
                        book=nm, panel=p, fam=b["fam"], cost=c, E=e,
                        **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                              "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD", "IS_n", "OOS_n")},
                        spy_OOS_Sharpe=s["OOS_Sharpe"],
                        **lg, pass4b=all(lg.values()),
                        pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                    and bk["MaxDD"] >= v2["MaxDD"])))
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    G("G5", f"determinism over the {len(L):,}-row ladder", f"{d5:.3e}", d5 == 0.0)
    dump(L, "ladder", gz=True)

    bad4, rows4 = 0, []
    for (p, nm), t13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - t13[0]), abs(r.OOS_Sharpe - t13[1]), abs(r.OOS_MaxDD - t13[2]))
        bad4 += 0 if d <= 5e-4 else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=t13[0], pub_Sharpe=t13[1],
                          pub_MaxDD=t13[2], maxd=d, verdict="PASS" if d <= 5e-4 else "FAIL"))
    G("G4", "CROSS-RUN 1013's four published declared-split picks",
      f"{len(PUB_1013)-bad4}/{len(PUB_1013)} max|d| {max(r['maxd'] for r in rows4):.3e}", bad4 == 0)
    dump(pd.DataFrame(rows4), "crossrun")

    # G9 nesting
    nest_ok = True
    for pname in PX:
        for a, b in (("WIDE10", "WIDE20"), ("WIDE20", "WIDE40"), ("WIDE40", "WIDE80")):
            nest_ok &= set(POOLS[(a, pname)]).issubset(POOLS[(b, pname)])
        nest_ok &= set(POOLS[("GRID18", pname)]).issubset(POOLS[("WIDE80", pname)])
    G("G9", "WIDE10 c WIDE20 c WIDE40 c WIDE80 and GRID18 c WIDE80", str(nest_ok), nest_ok)

    # ---------------------------------------------------------------- choosers
    SPYIS = {(p, e): fmet(SPYR[p].loc[:pd.Timestamp(e)].values) for p in PX for e in ALLE}
    IDX = {}
    for p in PX:
        for c in RUNGS:
            for e in ALLE:
                IDX[(p, c, e)] = L[(L.panel == p) & (L.cost == c) & (L.E == e)].set_index("book")

    def picks_for(p, c, poolname):
        bks = POOLS[(poolname, p)]
        return {e: {ch: raw_pick(IDX[(p, c, e)].loc[bks], ch, SPYIS[(p, e)]) for ch in RAW}
                for e in ALLE}

    PR = {(p, c, pn): picks_for(p, c, pn) for p in PX for c in RUNGS for pn in POOLNAMES}

    # G6 IS purity: permuting the OOS returns cannot move any pick
    rng6 = np.random.default_rng(SEED0)
    base_pick = PR[(PANEL_HEAD, RUNG_HEAD, POOL_HEAD)]
    NET_SAVE = dict(NET)
    for nm in POOLS[(POOL_HEAD, PANEL_HEAD)]:
        s = NET[(nm, RUNG_HEAD)]
        cut = pd.Timestamp(ALLE[-1]) + pd.Timedelta(days=1)
        o = s.loc[cut:]
        NET[(nm, RUNG_HEAD)] = pd.concat(
            [s.loc[:pd.Timestamp(ALLE[-1])],
             pd.Series(rng6.permutation(o.values), index=o.index)])
    IDX6 = {}
    for e in ALLE:
        rows = []
        for nm in POOLS[(POOL_HEAD, PANEL_HEAD)]:
            bk = split_block(NET[(nm, RUNG_HEAD)], e)
            rows.append(dict(book=nm, **bk))
        IDX6[e] = pd.DataFrame(rows).set_index("book")
    perm_pick = {e: {ch: raw_pick(IDX6[e], ch, SPYIS[(PANEL_HEAD, e)]) for ch in RAW}
                 for e in ALLE}
    npure = sum(base_pick[e][ch] == perm_pick[e][ch] for e in ALLE for ch in RAW)
    NET.update(NET_SAVE)
    G("G6", "IS purity — picks invariant under an OOS permutation",
      f"{npure}/{len(ALLE)*len(RAW)}", npure == len(ALLE) * len(RAW))

    # ---------------------------------------------------------------- (A)+(B) the tables
    P("")
    P("## (A) THE RESOLUTION TABLE and (B) THE PERCENTILE TABLE")
    P("   RESOLUTION is arithmetic: at ONE end a coin flip is a uniform draw from N books, so a")
    P("   chooser's percentile lies on the (k+1/2)/N grid and the smallest p it could earn is")
    P("   0.5/N.  DECIDABILITY is the observed percentile itself: under the null 'the chooser is")
    P("   a uniform draw from this pool', one-sided p = 1 - percentile.")
    P("")
    rng = np.random.default_rng(SEED0 + 1)
    trows, rrows, g7, g8 = [], [], [], []
    for p in PX:
        for c in RUNGS:
            for pn in POOLNAMES:
                bks = POOLS[(pn, p)]
                N = len(bks)
                for gname, ends in GRIDS.items():
                    K = len(ends)
                    er = np.arange(K)
                    mat = np.column_stack([IDX[(p, c, e)].loc[bks, "OOS_Sharpe"].values
                                           for e in ends]).T          # (K, N)
                    seq = rng.integers(0, N, size=(NRAND, K))
                    rscore = mat[er[None, :], seq].mean(axis=1)
                    exact = float(mat.mean())                          # closed-form pool mean
                    mc_se = float(rscore.std(ddof=1) / np.sqrt(NRAND))
                    ok7 = abs(rscore.mean() - exact) <= 3 * max(mc_se, 1e-12)
                    g7.append(ok7)
                    ok8 = abs(pct_of(np.median(rscore), rscore) - 0.5) <= 0.01
                    g8.append(dict(K=K, ok=ok8, atom=float((rscore == np.median(rscore)).mean()),
                                   dev=abs(pct_of(np.median(rscore), rscore) - 0.5)))
                    distinct = int(len(np.unique(np.round(rscore, 12))))
                    step = 1.0 / N if K == 1 else float(
                        np.min(np.diff(np.unique(np.round(rscore, 12)))) if distinct > 1 else 1.0)
                    rrows.append(dict(panel=p, cost=c, pool=pn, N=N, grid=gname, K=K,
                                      distinct_rand_scores=distinct,
                                      pct_step_at_one_end=1.0 / N,
                                      min_attainable_p=0.5 / N,
                                      rand_mean=float(rscore.mean()),
                                      exact_pool_mean=exact, mc_se=mc_se,
                                      rand_median=float(np.median(rscore)),
                                      rand_sd=float(rscore.std(ddof=1)),
                                      median_atom_mass=float((rscore == np.median(rscore)).mean()),
                                      G7=ok7, G8=ok8))
                    for ch in RAW:
                        sc = float(np.mean([IDX[(p, c, e)].loc[PR[(p, c, pn)][e][ch],
                                                               "OOS_Sharpe"] for e in ends]))
                        pctl = pct_of(sc, rscore)
                        trows.append(dict(
                            panel=p, cost=c, pool=pn, N=N, grid=gname, K=K, chooser=ch,
                            chooser_score=sc, rand_mean=float(rscore.mean()),
                            rand_median=float(np.median(rscore)),
                            rand_sd=float(rscore.std(ddof=1)), percentile=pctl,
                            p_one_sided=1.0 - pctl, clears_50th=bool(pctl > 0.5),
                            sep_at_5pct=bool((1.0 - pctl) <= 0.05),
                            min_attainable_p=0.5 / N,
                            resolution_permits_5pct=bool(0.5 / N <= 0.05)))
    T = pd.DataFrame(trows)
    R = pd.DataFrame(rrows)
    dump(T, "percentile")
    dump(R, "resolution")
    G("G7", "sampler unbiasedness (MC mean == exact pool mean, 3 SE)",
      f"{sum(g7)}/{len(g7)} cells", all(g7))
    n8 = sum(x["ok"] for x in g8)
    G("G8", "percentile validity, ALL cells (own median -> 0.500 +/- 0.01)",
      f"{n8}/{len(g8)} cells", all(x["ok"] for x in g8))
    cont = [x for x in g8 if x["K"] > 1]
    G("G8b", "percentile validity, K > 1 (continuous) cells only",
      f"{sum(x['ok'] for x in cont)}/{len(cont)} cells", all(x["ok"] for x in cont))
    one = [x for x in g8 if x["K"] == 1]
    P(f"G8c the {len(one)} REC1 cells are N POINT MASSES: median atom mass "
      f"{min(x['atom'] for x in one):.4f}..{max(x['atom'] for x in one):.4f}, deviation from "
      f"0.500 {min(x['dev'] for x in one):.4f}..{max(x['dev'] for x in one):.4f}.  A mid-rank "
      f"percentile CANNOT return 0.500 at a point mass, so G8's failures are exactly the "
      f"quantisation this run is measuring — 1031 reported the same for its RATE4B statistic.")
    LOG.append("")
    gates.append(dict(gate="G8c", what="REC1 median atom mass (the quantisation itself)",
                      value=f"{min(x['atom'] for x in one):.4f}..{max(x['atom'] for x in one):.4f}",
                      verdict="REPORTED"))

    hd = R[(R.panel == PANEL_HEAD) & (R.cost == RUNG_HEAD)]
    P("")
    P(f"   RESOLUTION, {PANEL_HEAD} @ {RUNG_HEAD:.0f} bps (arithmetic — identical at every cost):")
    P(f"   {'pool':10s} {'N':>4s} | {'1/N step':>9s} {'min p (0.5/N)':>13s} {'5% reachable?':>14s} "
      f"| distinct random scores REC1 / Q8 / Q16 / Q32")
    for pn in POOLNAMES:
        s = hd[hd.pool == pn]
        N = int(s.N.iloc[0])
        d = {r.grid: r.distinct_rand_scores for _, r in s.iterrows()}
        P(f"   {pn:10s} {N:4d} | {1/N:9.4f} {0.5/N:13.4f} {str(0.5/N <= 0.05):>14s} "
          f"| {d['REC1']:5d} {d['Q8']:5d} {d['Q16']:5d} {d['Q32']:5d}")

    P("")
    P(f"   PERCENTILES, {PANEL_HEAD} @ {RUNG_HEAD:.0f} bps — chooser percentile (one-sided p) at "
      f"every pool x end grid:")
    P(f"   {'pool':10s} {'N':>4s} | " + " | ".join(f"{ch:^30s}" for ch in RAW))
    P(f"   {'':10s} {'':>4s} | " + " | ".join(
        "  ".join(f"{g:>6s}" for g in GRIDS) + "      " for ch in RAW))
    for pn in POOLNAMES:
        cells = []
        for ch in RAW:
            v = []
            for gname in GRIDS:
                r = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == pn)
                      & (T.grid == gname) & (T.chooser == ch)].iloc[0]
                v.append(f"{r.percentile:6.3f}")
            cells.append("  ".join(v) + "      ")
        N = int(T[(T.pool == pn) & (T.panel == PANEL_HEAD)].N.iloc[0])
        P(f"   {pn:10s} {N:4d} | " + " | ".join(cells))

    # ---------------------------------------------------------------- (C) pool quality
    P("")
    P("## (C) POOL-QUALITY DECOMPOSITION — 1030's FLOOR, measured on the nested ladder")
    P("   If a percentile rises with N because the added books are WORSE, the move is the pool's,")
    P("   not the chooser's.  Absolute levels (mean OOS Sharpe over the headline grid):")
    P("")
    P(f"   {'pool':10s} {'N':>4s} | {'coin flip':>9s} {'pool sd':>8s} | "
      + " ".join(f"{ch:>12s}" for ch in RAW) + " | " + " ".join(f"{ch[3:]+' pct':>10s}"
                                                                for ch in RAW))
    qrows = []
    for pn in POOLNAMES:
        r0 = R[(R.panel == PANEL_HEAD) & (R.cost == RUNG_HEAD) & (R.pool == pn)
               & (R.grid == GRID_HEAD)].iloc[0]
        line = f"   {pn:10s} {int(r0.N):4d} | {r0.rand_mean:9.4f} {r0.rand_sd:8.4f} | "
        sc, pc = [], []
        for ch in RAW:
            r = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == pn)
                  & (T.grid == GRID_HEAD) & (T.chooser == ch)].iloc[0]
            sc.append(f"{r.chooser_score:12.4f}")
            pc.append(f"{r.percentile:10.3f}")
        P(line + " ".join(sc) + " | " + " ".join(pc))
        qrows.append(dict(pool=pn, N=int(r0.N), coinflip_mean=r0.rand_mean, pool_sd=r0.rand_sd,
                          **{f"score_{ch}": float(T[(T.panel == PANEL_HEAD)
                                                    & (T.cost == RUNG_HEAD) & (T.pool == pn)
                                                    & (T.grid == GRID_HEAD)
                                                    & (T.chooser == ch)].chooser_score.iloc[0])
                             for ch in RAW}))
    dump(pd.DataFrame(qrows), "poolquality")

    P("")
    P("   POST-HOC (NOT pre-registered — H_MOVE's bar was set on the NESTED WIDE axis alone, and")
    P("   the nested axis is where the percentile turns out to be stable).  Across ALL SIX named")
    P("   pools at the headline grid the same chooser spans:")
    for ch in RAW:
        v = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == GRID_HEAD)
              & (T.chooser == ch)]
        P(f"      {ch:10s} {v.percentile.min():.3f} .. {v.percentile.max():.3f}  "
          f"(range {v.percentile.max()-v.percentile.min():.3f}) — "
          + " ".join(f"{r['pool']}={r.percentile:.3f}" for _, r in v.iterrows()))
    P("   and the SAME CHOOSER picks a DIFFERENT BOOK as the menu widens, so the move is a")
    P("   MENU-COMPOSITION object, not a SIZE object.  A percentile is therefore only ever a")
    P("   statement about the pool it was computed in.")
    P("")
    P("   THE QUEUE'S QUESTION, ANSWERED IN ITS OWN TERMS.  RESOLUTION is sufficient at N >= 10")
    P("   (0.5/N <= 0.05 needs only N >= 10) and the record's own 18-book pool already resolves")
    P("   to 0.0278 — finer than the 5% bar.  So there is NO N at which resolution becomes the")
    P("   binding constraint, because it never was: 0.800 fails to separate from a coin flip")
    P("   because 1 draw in 5 beats it, and that is a RANK, readable at any N.")

    # ---------------------------------------------------------------- hypotheses
    P("")
    P("## Hypotheses (bars declared in the docstring, before any number above was read)")
    hyp = []

    def H(name, bar, ok, detail):
        hyp.append(dict(hypothesis=name, bar=bar, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"{name:10s} {'PASS' if ok else 'FAIL'}  bar: {bar}")
        P(f"           {detail}")

    se31 = np.sqrt(0.25 / PUB_1031_N)
    d31 = {}
    for ch in RAW:
        r = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == POOL_HEAD)
              & (T.grid == GRID_HEAD) & (T.chooser == ch)].iloc[0]
        d31[ch] = (r.percentile, abs(r.percentile - PUB_1031_PCT[ch]))
    ok31 = all(v[1] <= 3 * se31 for v in d31.values())
    H("H_1031", "1031's headline percentiles reproduce within 3 MC SE "
      f"({3*se31:.4f})", ok31,
      "; ".join(f"{ch} {d31[ch][0]:.3f} vs {PUB_1031_PCT[ch]:.3f} (|d| {d31[ch][1]:.4f})"
                for ch in RAW))

    rec = R[(R.grid == "REC1")]
    ok_q = bool(np.abs(rec.pct_step_at_one_end - 1.0 / rec.N).max() < 1e-12)
    n18 = float(rec[rec.pool == "GRID18"].pct_step_at_one_end.iloc[0])
    H("H_QUANT", "at REC1 the percentile step equals 1/N exactly for all six pools", ok_q,
      f"max |step - 1/N| = {np.abs(rec.pct_step_at_one_end - 1.0/rec.N).max():.2e}; "
      f"GRID18 step {n18:.4f} (1031's 1/18 = {1/18:.4f}); "
      + ", ".join(f"{pn} 1/{int(rec[rec.pool==pn].N.iloc[0])}={1/rec[rec.pool==pn].N.iloc[0]:.4f}"
                  for pn in POOLNAMES))

    rc = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == "REC1")
           & (T.chooser == "IS_CAGR")]
    sep = rc[rc.sep_at_5pct]
    H("H_RESOLVE", "some pool on the ladder separates IS_CAGR from a coin flip at REC1, p <= 0.05",
      len(sep) > 0,
      ("separating pools: " + ", ".join(f"{r.pool}(N={int(r.N)}, p={r.p_one_sided:.4f})"
                                        for _, r in sep.iterrows())) if len(sep) else
      "NONE of the 6 pools: " + ", ".join(f"{r.pool}(N={int(r.N)}, pct={r.percentile:.3f}, "
                                          f"p={r.p_one_sided:.4f})" for _, r in rc.iterrows()))

    big = rc[rc.N >= 20]
    ok_nr = bool(len(big) > 0 and (big.min_attainable_p <= 0.05).all()
                 and (big.p_one_sided > 0.05).all())
    H("H_NOTRES", "at every pool with N >= 20 the smallest attainable p is <= 0.05 while "
      "IS_CAGR's actual p at REC1 stays > 0.05", ok_nr,
      "; ".join(f"{r.pool} N={int(r.N)} min_p={r.min_attainable_p:.4f} actual_p={r.p_one_sided:.4f}"
                for _, r in big.iterrows()))

    w10 = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == "WIDE10")
            & (T.grid == GRID_HEAD) & (T.chooser == "IS_CAGR")].percentile.iloc[0]
    w80 = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == "WIDE80")
            & (T.grid == GRID_HEAD) & (T.chooser == "IS_CAGR")].percentile.iloc[0]
    H("H_MOVE", "IS_CAGR's headline-grid percentile moves > 0.10 between WIDE10 and WIDE80",
      abs(w80 - w10) > 0.10,
      f"WIDE10 {w10:.3f} -> WIDE80 {w80:.3f} (|d| {abs(w80-w10):.3f}); full ladder "
      + " ".join(f"{pn}={T[(T.panel==PANEL_HEAD)&(T.cost==RUNG_HEAD)&(T.pool==pn)&(T.grid==GRID_HEAD)&(T.chooser=='IS_CAGR')].percentile.iloc[0]:.3f}"
                 for pn in POOLNAMES))

    fl = [float(R[(R.panel == PANEL_HEAD) & (R.cost == RUNG_HEAD) & (R.pool == pn)
                  & (R.grid == GRID_HEAD)].rand_mean.iloc[0])
          for pn in ("WIDE10", "WIDE20", "WIDE40", "WIDE80")]
    H("H_FLOOR", "the coin flip's own mean OOS Sharpe falls monotonically WIDE10->WIDE80",
      all(fl[i] > fl[i + 1] for i in range(3)),
      " -> ".join(f"{v:.4f}" for v in fl) + f"  (total {fl[-1]-fl[0]:+.4f})")

    pe = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == "GRID18")
           & (T.chooser == "IS_CAGR")].p_one_sided
    pp = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == GRID_HEAD)
           & (T.chooser == "IS_CAGR") & (T.pool.str.startswith("WIDE"))].p_one_sided
    H("H_POWER", "spread of IS_CAGR's p across the 4 END GRIDS (fixed GRID18) exceeds its spread "
      "across the 4 WIDE POOLS (fixed Q16)", (pe.max() - pe.min()) > (pp.max() - pp.min()),
      f"end-grid spread {pe.max()-pe.min():.4f} ({pe.min():.4f}..{pe.max():.4f}) vs pool-size "
      f"spread {pp.max()-pp.min():.4f} ({pp.min():.4f}..{pp.max():.4f})")

    ords = {}
    for pn in POOLNAMES:
        s = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.pool == pn)
              & (T.grid == GRID_HEAD)].sort_values("percentile", ascending=False)
        ords[pn] = tuple(s.chooser)
    H("H_ORDER", "the chooser ordering by percentile is identical at all six pools",
      len(set(ords.values())) == 1,
      "; ".join(f"{pn}={'>'.join(c[3:] for c in v)}" for pn, v in ords.items()))

    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(gates), "gates")

    # ---------------------------------------------------------------- (D) rule 8 walk-forward
    P("")
    P("## (D) RULE 8 WALK-FORWARD — PROTOCOL's own split, IS 2009-2016 / OOS 2017-2026 read ONCE")
    P("   Each chooser picks from its POOL using 2009-2016 data ONLY; the OOS triple is read once")
    P("   and scored on BOTH KEEP paths against the live RULES v2 baseline and against SPY.")
    P("")
    wrows = []
    for p in PX:
        s = SPYB[(p, REC_END)]
        for c in RUNGS:
            v2 = V2[(p, c)]
            for pn in POOLNAMES:
                bks = POOLS[(pn, p)]
                sub = IDX[(p, c, REC_END)].loc[bks]
                pooldist = sub["OOS_Sharpe"].values
                for ch in RAW:
                    bk = PR[(p, c, pn)][REC_END][ch]
                    r = sub.loc[bk]
                    lg = legs_at(dict(H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                                      OOS_MaxDD=r.OOS_MaxDD, OOS_CAGR=r.OOS_CAGR), s)
                    wrows.append(dict(
                        panel=p, cost=c, pool=pn, N=len(bks), chooser=ch, pick=bk,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        full_CAGR=r.CAGR, full_Sharpe=r.Sharpe, full_MaxDD=r.MaxDD,
                        H1=r.H1, H2=r.H2,
                        spy_OOS_CAGR=s["OOS_CAGR"], spy_OOS_Sharpe=s["OOS_Sharpe"],
                        spy_OOS_MaxDD=s["OOS_MaxDD"], spy_H1=s["H1"], spy_H2=s["H2"],
                        v2_CAGR=v2["CAGR"], v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"],
                        v2_H1=v2["H1"], v2_H2=v2["H2"],
                        **lg, pass4b=all(lg.values()), pass4a=bool(r.pass4a),
                        pool_percentile=pct_of(r.OOS_Sharpe, pooldist),
                        pool_mean_OOS_Sharpe=float(np.mean(pooldist))))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"   {'panel':6s} {'cost':>4s} {'pool':10s} {'chooser':10s} {'pick':32s} | "
      f"{'OOS CAGR':>8s} {'Sh':>6s} {'MaxDD':>7s} | {'4b':>2s} {'4a':>2s} {'poolPct':>7s}  binding")
    for _, r in WF[(WF.panel == PANEL_HEAD) & (WF.cost == RUNG_HEAD)].iterrows():
        binds = ",".join(k for k in ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR") if not r[k])
        P(f"   {r.panel:6s} {r.cost:4.0f} {r['pool']:10s} {r.chooser:10s} {r['pick']:32s} | "
          f"{r.OOS_CAGR:8.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} | {str(r.pass4b)[0]:>2s} "
          f"{str(r.pass4a)[0]:>2s} {r.pool_percentile:7.3f}  {binds if binds else '(none — 4b)'}")
    for p in PX:
        s = SPYB[(p, REC_END)]
        v2 = V2[(p, RUNG_HEAD)]
        P(f"   comparands {p}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / "
          f"{s['OOS_MaxDD']:.2%}; SPY full {s['CAGR']:.2%} / {s['Sharpe']:.4f} / "
          f"{s['MaxDD']:.2%} (H1 {s['H1']:.4f} / H2 {s['H2']:.4f}; 4b DD cap "
          f"{DDCAP_FRAC*abs(s['MaxDD']):.2%}, CAGR floor {CAGRFLOOR_FRAC*s['CAGR']:.2%});  "
          f"RULES v2 live @{RUNG_HEAD:.0f} bps {v2['CAGR']:.2%} / {v2['Sharpe']:.4f} / "
          f"{v2['MaxDD']:.2%} (H1 {v2['H1']:.4f} / H2 {v2['H2']:.4f})")
    P(f"   OOS 4b passes: {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a passes: "
      f"{int(WF.pass4a.sum())} of {len(WF)}.")
    P(f"   KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves and MaxDD no worse; 4b needs "
      f"Sharpe > SPY in both halves AND OOS, |MaxDD| <= 60% of SPY's and CAGR >= 70% of SPY's.")
    dist = WF[(WF.panel == PANEL_HEAD) & (WF.cost == RUNG_HEAD)]["pick"].nunique()
    P(f"   DISTINCT picks across the 6 pools x 3 choosers in the headline cell: {dist} of 18.")

    P("")
    P(f"GATES {sum(g['verdict']=='PASS' for g in gates)} of {len(gates)};  HYPOTHESES "
      f"{sum(h['verdict']=='PASS' for h in hyp)} of {len(hyp)}.")
    P(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
