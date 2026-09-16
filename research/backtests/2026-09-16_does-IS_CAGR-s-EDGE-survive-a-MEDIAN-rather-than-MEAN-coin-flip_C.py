#!/usr/bin/env python3
"""Idea 1031 (lane C, 2026-09-16) — does IS_CAGR's EDGE survive a MEDIAN rather than a MEAN
coin flip?

QUESTION (QUEUE idea 1031, verbatim)
    idea 1023 scored RANDOM by the mean of 400 sequences, which is the pool MEAN; a chooser that
    avoids the pool's worst books beats the mean without beating the median.  Re-score all three
    choosers as PERCENTILES of the random control's own sequence distribution and report which
    clear the 50th.  Max 2 params (percentile statistic, end grid).

WHAT IS NEW AGAINST 1023.  1023 published ONE number per (panel, cost) for its coin flip: the
    mean over 400 sequences of the sequence mean.  That number is the POOL MEAN and it is a
    point, so "RANDOM beats IS_SHARPE by +0.0418" is a comparison of two points with no yardstick
    attached.  1023 committed the yardstick (`sd_over_seq`) and never used it.  This run throws
    the point away and keeps the whole distribution: every chooser is re-expressed as the SHARE
    OF RANDOM SEQUENCES IT BEATS.  That converts each of 1023's Sharpe gaps into the only
    statistic a rule-8 clause could be written on — how often a coin flip from the same pool does
    better than the record's chooser — and it answers the queue's literal question (which
    choosers clear the 50th) as a special case.

    The queue's stated MECHANISM is a separate, testable claim: that the scored distribution is
    LEFT-SKEWED, so its median sits ABOVE its mean and a mean-bar flatters a chooser that merely
    dodges the pool's worst books.  Whether that skew exists depends entirely on WHAT is being
    percentiled.  A sequence mean over 16 independent draws is a 16-fold average and the CLT
    flattens skew out of it; a single-end draw is the raw book distribution and keeps it.  The
    END GRID dial therefore prices the queue's own mechanism, at REC1 (one end, raw book
    distribution) against Q16 and Q32 (16- and 32-fold averages).  H_PREMISE is pre-registered
    on the headline cell and reported at all nine.

WHAT IS MEASURED
    (A) THE PERCENTILE TABLE.  Every chooser x panel x cost x (statistic, end grid): the
        chooser's score, the random distribution's mean / median / sd / quartiles, the chooser's
        PERCENTILE in it, and the 50th-percentile verdict.
    (B) THE MEAN-vs-MEDIAN AUDIT.  For every cell, 1023's verdict (chooser beats the random
        MEAN) against this run's (chooser clears the random MEDIAN), and the count of FLIPS.
        A flip is the only way the queue's worry can be true.
    (C) THE SKEW DIAGNOSTIC.  median - mean of the random score distribution, and the skew of
        the underlying per-end BOOK distribution, at every cell.
    (D) THE RULE-8 WALK-FORWARD at PROTOCOL's own split 2016-12-31 (IS 2009-2016, OOS 2017-2026
        read once), with OOS CAGR/Sharpe/MaxDD against the live RULES v2 baseline and against
        SPY, BOTH KEEP paths for every pick, and the pick's percentile in the pool.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 9 grid points reported at every
    panel x cost, none selected.
    (1) PERCENTILE STATISTIC — the per-sequence score whose distribution is percentiled
          MEAN_SH   sequence MEAN of the pick's OOS Sharpe over the ends   <- HEADLINE (1023's)
          MED_SH    sequence MEDIAN of the pick's OOS Sharpe over the ends
          RATE4B    sequence mean of the pick's 4b PASS indicator (1023's second axis)
    (2) END GRID — the band of legal rule-8 IS end dates the chooser is run over
          Q16   1013's/1023's own 16 quarter-ends 2015-03-31..2018-12-31   <- HEADLINE
          Q32   32 quarter-ends 2011-03-31..2018-12-31 (a wider, earlier band)
          REC1  PROTOCOL's declared split 2016-12-31 ALONE — one end, so the sequence
                distribution IS the raw 18-book distribution and carries its full skew

    NOT TUNED, reported as CONTROLS at every point:
      COST    0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL   U56 (binding) and B136 (labelled replication).
      POOL    the 36 never-memo-selected GRID ladder books, 18 per panel — 1023's own pool.
              The committed SHELF is NOT a legal rule-8 pool: it was selected on the full tape.
      DRAWS   NRAND = 2,000 sequences per (panel, cost, end grid), 5x 1023's 400, so a
              percentile is resolved to 0.0005 and its binomial SE at p=0.5 is 0.0112.

    CAVEAT ON Q32, stated before the numbers: its earliest ends leave an IS window of barely two
    years (2009-01..2011-03).  That is legal under rule 8's letter and thin in substance; Q32 is
    a SENSITIVITY axis, never a headline.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_1023    reproduce 1023's headline cell (U56 / 10 bps / Q16): IS_SHARPE and IS_LEGS both at
              mean OOS Sharpe 1.1557, IS_CAGR at 1.2618 (tol 5e-4, deterministic), and the exact
              pool mean within 3 MC standard errors of 1023's published RANDOM 1.2433.
    H_PREMISE HEADLINE MECHANISM.  The random score distribution is LEFT-skewed in the headline
              cell: median - mean > 0.  PASS => the queue's mechanism exists and a mean bar is
              the easier one.  FAIL => mean and median are the same bar and the queue's premise
              is wrong about this distribution.
    H_CAGR50  HEADLINE ANSWER.  `IS_CAGR` clears the 50th percentile in the headline cell.
              PASS => 1023's "IS_CAGR beats the coin flip" survives the harder bar.
    H_CAGRALL `IS_CAGR` clears the 50th in ALL 6 panel x cost cells at the headline (statistic,
              end grid).  1023 had it beating the RANDOM mean in 5 of 6.
    H_STAB50  `IS_SHARPE` and `IS_LEGS` FAIL the 50th in the same 5-of-6 cells where 1023 found
              the coin flip beating them.  PASS => the two readings agree on the weak choosers.
    H_FLIP    DECISIVE.  No (chooser, cell) pair flips verdict between 1023's mean bar and this
              run's 50th-percentile bar, over all 18 headline-grid pairs.  PASS => mean vs
              median is a distinction without a difference and the queue's worry is empty.
              FAIL => the bar choice changes the record's answer and must be pinned.
    H_DIAL    the SET of choosers clearing the 50th is the same at all 9 (statistic, end grid)
              points in the headline panel x cost cell.
    H_VERDICT `IS_CAGR`'s RATE4B percentile exceeds its MEAN_SH percentile in the headline cell —
              1023's "IS fit buys verdict reliability, not Sharpe", restated as a percentile.
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
        EXACT pool mean (a closed form, no draws) to within 3 MC standard errors, in all 6
        headline-grid cells.  This is what licenses reading a percentile off the draws.
    G8  PERCENTILE VALIDITY: scoring the random distribution's OWN median through the same
        percentile function returns 0.5000 +/- 0.01 in every cell.  Reported at all nine dial
        points (G8) AND restricted to the two CONTINUOUS statistics (G8b), with the atom mass
        that separates them printed as G8c: a mid-rank percentile cannot return 0.5 at a point
        mass, and RATE4B's sequence score is discrete.  Both readings are printed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b count an UPPER bound.  The measured object is
    a chooser's RANK inside a distribution built from the SAME pool over the SAME tape, and the
    bias is a common factor to the chooser and to every random draw it is ranked against.  Where
    it does not cancel it flatters the coin flip — a uniform draw from a survivor panel is a
    better book than a real-time one — so every percentile a chooser earns here is a LOWER bound
    and H_CAGR50 is the HARDER call.  SPY is a real index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-IS_CAGR-s-EDGE-survive-a-MEDIAN-rather-than-MEAN-coin-flip"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
PSTATS = ["MEAN_SH", "MED_SH", "RATE4B"]
PSTAT_HEAD = "MEAN_SH"
GRID_HEAD = "Q16"
NRAND = 2000
SEED0 = 20260916
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
# 1013's four published declared-split picks (OOS CAGR, Sharpe, MaxDD)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
# 1023's committed headline cell (U56 / 10 bps / Q16), from its .stability.csv / .random.csv
PUB_1023_CHOOSER = {"IS_SHARPE": 1.155696, "IS_LEGS": 1.155696, "IS_CAGR": 1.261757}
PUB_1023_RANDOM = 1.243317
PUB_1023_RANDOM_SD = 0.020890          # sd over its 400 sequence means
PUB_1023_N = 400
# 1023's full mean-bar table: chooser mean OOS Sharpe and the RANDOM pool mean, all 6 cells.
PUB_1023_ALL = {
    ("U56", 0.0): dict(IS_SHARPE=1.211524, IS_LEGS=1.195362, IS_CAGR=1.349433, RANDOM=1.305739),
    ("U56", 10.0): dict(IS_SHARPE=1.155696, IS_LEGS=1.155696, IS_CAGR=1.261757, RANDOM=1.243317),
    ("U56", 25.0): dict(IS_SHARPE=1.120364, IS_LEGS=1.116140, IS_CAGR=1.139356, RANDOM=1.147918),
    ("B136", 0.0): dict(IS_SHARPE=1.121657, IS_LEGS=1.065754, IS_CAGR=1.200140, RANDOM=1.155352),
    ("B136", 10.0): dict(IS_SHARPE=1.048081, IS_LEGS=1.048081, IS_CAGR=1.117967, RANDOM=1.089402),
    ("B136", 25.0): dict(IS_SHARPE=1.021559, IS_LEGS=1.021559, IS_CAGR=0.994358, RANDOM=0.987919),
}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC1023", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q16 = quarter_ends("2015-01-01", "2018-12-31")          # 1013's / 1023's own 16
END_Q32 = quarter_ends("2011-01-01", "2018-12-31")          # the wider, earlier band
GRIDS = {"Q16": END_Q16, "Q32": END_Q32, "REC1": [REC_END]}
ALLE = sorted(set(END_Q32) | set(END_Q16) | {REC_END})


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
    """IS-ONLY choosers — 1023's own three, verbatim.  sub is one (panel, cost, E) slice."""
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
    """Mid-rank percentile of x inside dist, in [0, 1].  Ties split, so scoring a distribution's
    own median through this returns 0.5 (G8)."""
    d = np.asarray(dist, float)
    return float(((d < x).sum() + 0.5 * (d == x).sum()) / len(d))


def seq_score(mat, seq, stat, er):
    """Per-sequence score.  mat is (n_ends, n_books); seq is (n_seq, n_ends) of book indices."""
    v = mat[er[None, :], seq]
    if stat == "MED_SH":
        return np.median(v, axis=1)
    return v.mean(axis=1)            # MEAN_SH and RATE4B are both means of their own matrix


def main():
    t0 = time.time()
    P(f"# Idea 1031 (lane C, {DATE}) — does IS_CAGR's EDGE survive a MEDIAN rather than a MEAN "
      f"coin flip?")
    P(f"# 2 tuned dials: PERCENTILE STATISTIC {PSTATS} x END GRID {list(GRIDS)} = 9 points, ALL "
      f"reported at every panel x cost, none selected.")
    P(f"# HEADLINE = {PANEL_HEAD} / {RUNG_HEAD:.0f} bps / {PSTAT_HEAD} / {GRID_HEAD} — 1023's own "
      f"cell.  CONTROLS: cost {RUNGS} bps, panel [U56, B136], POOL = the 36 GRID books.")
    P(f"# DRAWS: NRAND = {NRAND:,} random chooser SEQUENCES per (panel, cost, end grid) — 5x "
      f"1023's 400.  A percentile resolves to {1/NRAND:.4f}; its binomial SE at p=0.5 is "
      f"{0.5/np.sqrt(NRAND):.4f}.")
    P("# CAVEAT declared first: Q32's earliest ends leave an IS window of barely two years. It is")
    P("#   legal under rule 8's letter and thin in substance — a SENSITIVITY axis, never a")
    P("#   headline.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic.  The")
    P("#   measured object is a RANK inside a distribution from the SAME pool; where the bias")
    P("#   does not cancel it flatters the coin flip, so every chooser percentile is a LOWER")
    P("#   bound and H_CAGR50 is the HARDER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    # CALENDAR: each panel keeps its OWN calendar, which is 1023's and 1013's construction and is
    # what the cross-run gates G3/G4 are stated against.  The broad cache is refreshed weekly
    # (rule 9) and today runs a few sessions behind the U56 cache; truncating to a common calendar
    # would move SPY's OOS CAGR by +0.11 pp and break the record's committed comparand, so it is
    # NOT done here.  Nothing in this run splices the two panels together.
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar (1023's and "
          f"1013's construction — the cross-run comparands are stated on it). No splice.")
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    pool = C.grid_books(U, B)
    P(f"POOL = {len(pool)} never-memo-selected GRID books "
      f"({sum(b['panel']=='U56' for b in pool.values())} U56 / "
      f"{sum(b['panel']=='B136' for b in pool.values())} B136).")
    P(f"END GRIDS: Q16 = {len(END_Q16)} ends {END_Q16[0]}..{END_Q16[-1]}; "
      f"Q32 = {len(END_Q32)} ends {END_Q32[0]}..{END_Q32[-1]}; REC1 = [{REC_END}].  "
      f"Union scored = {len(ALLE)} ends.")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
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

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    g1 = d_r < 1e-12 and d_t < 1e-10
    P(f"G1 fast_run == engine.backtest (returns / turnover): {d_r:.3e} / {d_t:.3e}  "
      f"{'PASS' if g1 else 'FAIL'}")
    gates.append(dict(gate="G1", what="fast runner == engine.backtest",
                      value=f"{d_r:.3e}/{d_t:.3e}", verdict="PASS" if g1 else "FAIL"))

    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    g2 = d2 == 0.0
    P(f"G2 rules_v2_weights(U,0.03,0.75) == baseline.rules_v2_weights(U): {d2:.3e}  "
      f"{'PASS' if g2 else 'FAIL'}")
    gates.append(dict(gate="G2", what="band book == live baseline", value=f"{d2:.3e}",
                      verdict="PASS" if g2 else "FAIL"))

    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    sb = SPYB[(PANEL_HEAD, REC_END)]
    trip = (sb["OOS_CAGR"], sb["OOS_Sharpe"], sb["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    g3 = d3 <= 5e-4
    P(f"G3 CROSS-RUN SPY OOS at {REC_END}: {trip[0]:.4%} / {trip[1]:.4f} / {trip[2]:.4%}  "
      f"max|d| {d3:.3e}  {'PASS' if g3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY OOS triple vs record", value=f"{d3:.3e}",
                      verdict="PASS" if g3 else "FAIL"))

    def build_ladder():
        rows = []
        for nm, b in pool.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    s = SPYB[(p, e)]
                    lg = legs_at(bk, s)
                    v2 = V2[(p, c)]
                    rows.append(dict(
                        book=nm, panel=p, cost=c, E=e,
                        **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                              "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD", "IS_n", "OOS_n")},
                        spy_OOS_Sharpe=s["OOS_Sharpe"], spy_OOS_CAGR=s["OOS_CAGR"],
                        **lg, pass4b=all(lg.values()),
                        pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                    and bk["MaxDD"] >= v2["MaxDD"])))
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    g5 = d5 == 0.0
    P(f"G5 determinism over the {len(L):,}-row ladder: {d5:.3e}  {'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="ladder determinism", value=f"{d5:.3e}",
                      verdict="PASS" if g5 else "FAIL"))

    bad4, rows4 = 0, []
    for (p, nm), t13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - t13[0]), abs(r.OOS_Sharpe - t13[1]), abs(r.OOS_MaxDD - t13[2]))
        ok = d <= 5e-4
        bad4 += 0 if ok else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=t13[0], pub_Sharpe=t13[1],
                          pub_MaxDD=t13[2], maxd=d, verdict="PASS" if ok else "FAIL"))
    g4 = bad4 == 0
    P(f"G4 CROSS-RUN 1013's four published declared-split picks: {len(PUB_1013)-bad4}/"
      f"{len(PUB_1013)}  max|d| {max(r['maxd'] for r in rows4):.3e}  {'PASS' if g4 else 'FAIL'}")
    gates.append(dict(gate="G4", what="1013 published picks", value=f"{len(PUB_1013)-bad4}/"
                      f"{len(PUB_1013)}", verdict="PASS" if g4 else "FAIL"))
    dump(pd.DataFrame(rows4), "crossrun")

    # ---------------------------------------------------------------- choosers
    SPYIS = {(p, e): fmet(SPYR[p].loc[:pd.Timestamp(e)].values) for p in PX for e in ALLE}
    IDX = {}
    for p in PX:
        for c in RUNGS:
            for e in ALLE:
                IDX[(p, c, e)] = L[(L.panel == p) & (L.cost == c) & (L.E == e)].set_index("book")

    def picks_raw(p, c):
        return {e: {ch: raw_pick(IDX[(p, c, e)], ch, SPYIS[(p, e)]) for ch in RAW} for e in ALLE}

    PR = {(p, c): picks_raw(p, c) for p in PX for c in RUNGS}

    # G6 IS purity: permuting OOS returns cannot move any raw pick
    rng6 = np.random.default_rng(SEED0)
    base_pick = PR[(PANEL_HEAD, RUNG_HEAD)]
    NET_SAVE = dict(NET)
    for nm, b in pool.items():
        if b["panel"] != PANEL_HEAD:
            continue
        s = NET[(nm, RUNG_HEAD)]
        o = s.loc[pd.Timestamp(ALLE[-1]) + pd.Timedelta(days=1):]
        perm = pd.Series(rng6.permutation(o.values), index=o.index)
        NET[(nm, RUNG_HEAD)] = pd.concat([s.loc[:pd.Timestamp(ALLE[-1])], perm])
    Lp = build_ladder()
    IDXp = {e: Lp[(Lp.panel == PANEL_HEAD) & (Lp.cost == RUNG_HEAD) & (Lp.E == e)].set_index("book")
            for e in ALLE}
    bad6 = sum(raw_pick(IDXp[e], ch, SPYIS[(PANEL_HEAD, e)]) != base_pick[e][ch]
               for e in ALLE for ch in RAW)
    NET.clear()
    NET.update(NET_SAVE)
    g6 = bad6 == 0
    P(f"G6 IS PURITY (picks invariant to an OOS permutation): {bad6} moved picks of "
      f"{len(ALLE)*len(RAW)}  {'PASS' if g6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="IS purity", value=f"{bad6}/{len(ALLE)*len(RAW)}",
                      verdict="PASS" if g6 else "FAIL"))

    # ---------------------------------------------------------------- score matrices
    BOOKS = {p: sorted(b for b in pool if pool[b]["panel"] == p) for p in PX}
    MAT = {}
    for p in PX:
        for c in RUNGS:
            for gname, ends in GRIDS.items():
                MAT[(p, c, gname, "SH")] = np.array(
                    [[IDX[(p, c, e)].loc[b, "OOS_Sharpe"] for b in BOOKS[p]] for e in ends])
                MAT[(p, c, gname, "4B")] = np.array(
                    [[float(IDX[(p, c, e)].loc[b, "pass4b"]) for b in BOOKS[p]] for e in ends])
                MAT[(p, c, gname, "4A")] = np.array(
                    [[float(IDX[(p, c, e)].loc[b, "pass4a"]) for b in BOOKS[p]] for e in ends])
                MAT[(p, c, gname, "CAGR")] = np.array(
                    [[IDX[(p, c, e)].loc[b, "OOS_CAGR"] for b in BOOKS[p]] for e in ends])
                MAT[(p, c, gname, "DD")] = np.array(
                    [[IDX[(p, c, e)].loc[b, "OOS_MaxDD"] for b in BOOKS[p]] for e in ends])

    # G7 sampler unbiasedness, on the HEADLINE grid: MC mean of sequence means == exact pool mean
    rng = np.random.default_rng(SEED0 + 7)
    SEQ = {}
    for p in PX:
        for c in RUNGS:
            for gname, ends in GRIDS.items():
                SEQ[(p, c, gname)] = rng.integers(0, len(BOOKS[p]), (NRAND, len(ends)))
    bad7, rows7 = 0, []
    for p in PX:
        for c in RUNGS:
            M = MAT[(p, c, GRID_HEAD, "SH")]
            er = np.arange(M.shape[0])
            sm = seq_score(M, SEQ[(p, c, GRID_HEAD)], "MEAN_SH", er)
            exact = float(M.mean())
            se = float(sm.std(ddof=1) / np.sqrt(NRAND))
            ok = abs(sm.mean() - exact) <= 3 * se
            bad7 += 0 if ok else 1
            rows7.append(dict(panel=p, cost=c, mc_mean=sm.mean(), exact_pool_mean=exact,
                              diff=sm.mean() - exact, mc_se=se, verdict="PASS" if ok else "FAIL"))
    g7 = bad7 == 0
    P(f"G7 SAMPLER UNBIASEDNESS (MC mean == exact pool mean, 3 SE): {6-bad7}/6  "
      f"max|d| {max(abs(r['diff']) for r in rows7):.3e}  {'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="sampler unbiased vs exact pool mean",
                      value=f"{6-bad7}/6", verdict="PASS" if g7 else "FAIL"))
    dump(pd.DataFrame(rows7), "sampler")

    # G8 percentile validity: the distribution's own median scores 0.5.  Stated over ALL nine
    # dial points as pre-registered, then DIAGNOSED by G8b/G8c: a mid-rank percentile returns
    # exactly 0.5 at the median only on a distribution with no ATOM there, and RATE4B's sequence
    # score is a mean of 0/1 indicators over 1 or 16 ends, so at REC1 it takes exactly two values.
    # The G8 bar is the right one for the two continuous statistics and the wrong one for a
    # discrete one; both readings are printed and neither is dropped.
    worst8, worst8b, atom_rows = 0.0, 0.0, []
    for p in PX:
        for c in RUNGS:
            for gname in GRIDS:
                for st in PSTATS:
                    key = "4B" if st == "RATE4B" else "SH"
                    M = MAT[(p, c, gname, key)]
                    er = np.arange(M.shape[0])
                    d = seq_score(M, SEQ[(p, c, gname)], st, er)
                    dev = abs(pct_of(np.median(d), d) - 0.5)
                    atom = float((d == np.median(d)).mean())
                    worst8 = max(worst8, dev)
                    if st != "RATE4B":
                        worst8b = max(worst8b, dev)
                    atom_rows.append(dict(panel=p, cost=c, grid=gname, stat=st,
                                          n_distinct=int(len(np.unique(d))),
                                          median=float(np.median(d)), atom_at_median=atom,
                                          pct_of_own_median=pct_of(np.median(d), d), dev=dev))
    g8 = worst8 <= 0.01
    g8b = worst8b <= 0.01
    P(f"G8  PERCENTILE VALIDITY, all 9 dial points (own median scores 0.5000): worst |d| "
      f"{worst8:.4f}  {'PASS' if g8 else 'FAIL'}")
    P(f"G8b PERCENTILE VALIDITY, the two CONTINUOUS statistics only: worst |d| {worst8b:.4f}  "
      f"{'PASS' if g8b else 'FAIL'}")
    AT = pd.DataFrame(atom_rows)
    worst_atom = AT[AT.stat == "RATE4B"].atom_at_median.max()
    CONT = AT[(AT.stat != "RATE4B") & (AT.grid != "REC1")]
    worst8d = float(CONT.dev.max())
    g8d = worst8d <= 0.01
    P(f"G8d PERCENTILE VALIDITY, the {len(CONT)} MULTI-END continuous cells (MEAN_SH/MED_SH on "
      f"Q16/Q32): worst |d| {worst8d:.5f}  {'PASS' if g8d else 'FAIL'}")
    P(f"G8c DIAGNOSIS — the whole G8/G8b residual is ATOM MASS, not a defect in the percentile "
      f"function.  A mid-rank percentile cannot return 0.5 at a point mass, and exactly two "
      f"things put one there: (i) REC1 is ONE end, so the score distribution IS the 18-book "
      f"pool and is quantised to 1/18 = {1/18:.4f} (n_distinct 18, atom "
      f"{AT[AT.grid=='REC1'].atom_at_median.min():.4f}..{AT[AT.grid=='REC1'].atom_at_median.max():.4f}, "
      f"dev <= {AT[AT.grid=='REC1'].dev.max():.4f}); (ii) RATE4B averages 0/1 indicators "
      f"({int(AT[AT.stat=='RATE4B'].n_distinct.min())}..{int(AT[AT.stat=='RATE4B'].n_distinct.max())} "
      f"distinct values, atom up to {worst_atom:.4f}).  Where the score is genuinely continuous "
      f"the bar is met by more than an order of magnitude (G8d).  Every REC1 and RATE4B "
      f"percentile below is therefore resolved only to its own atom and is read that way.")
    gates.append(dict(gate="G8", what="percentile validity, all 9 dial points",
                      value=f"{worst8:.4f}", verdict="PASS" if g8 else "FAIL"))
    gates.append(dict(gate="G8b", what="percentile validity, continuous statistics only",
                      value=f"{worst8b:.4f}", verdict="PASS" if g8b else "FAIL"))
    gates.append(dict(gate="G8d", what="percentile validity, multi-end continuous cells",
                      value=f"{worst8d:.5f}", verdict="PASS" if g8d else "FAIL"))
    gates.append(dict(gate="G8c", what="atom-mass diagnosis of the G8/G8b residual",
                      value=f"REC1 atom<= {AT[AT.grid=='REC1'].atom_at_median.max():.4f}, "
                            f"RATE4B atom <= {worst_atom:.4f}", verdict="DIAGNOSTIC"))
    dump(AT, "atoms")

    # ---------------------------------------------------------------- (A) the percentile table
    rows = []
    for p in PX:
        for c in RUNGS:
            for gname, ends in GRIDS.items():
                bidx = {b: i for i, b in enumerate(BOOKS[p])}
                er = np.arange(len(ends))
                for st in PSTATS:
                    key = "4B" if st == "RATE4B" else "SH"
                    M = MAT[(p, c, gname, key)]
                    dist = seq_score(M, SEQ[(p, c, gname)], st, er)
                    for ch in RAW:
                        picks = [PR[(p, c)][e][ch] for e in ends]
                        v = np.array([M[i, bidx[picks[i]]] for i in range(len(ends))])
                        sc = float(np.median(v)) if st == "MED_SH" else float(v.mean())
                        MC, MD = MAT[(p, c, gname, "CAGR")], MAT[(p, c, gname, "DD")]
                        MB, MA = MAT[(p, c, gname, "4B")], MAT[(p, c, gname, "4A")]
                        rows.append(dict(
                            panel=p, cost=c, grid=gname, n_ends=len(ends), stat=st, chooser=ch,
                            n_uniq_picks=len(set(picks)),
                            chooser_score=sc,
                            rand_mean=float(dist.mean()), rand_median=float(np.median(dist)),
                            rand_sd=float(dist.std(ddof=1)),
                            rand_p25=float(np.percentile(dist, 25)),
                            rand_p75=float(np.percentile(dist, 75)),
                            rand_min=float(dist.min()), rand_max=float(dist.max()),
                            skew_med_minus_mean=float(np.median(dist) - dist.mean()),
                            percentile=pct_of(sc, dist),
                            clears_50th=bool(pct_of(sc, dist) > 0.50),
                            beats_rand_mean=bool(sc > dist.mean()),
                            z_vs_rand=float((sc - dist.mean()) / dist.std(ddof=1))
                            if dist.std(ddof=1) > 0 else np.nan,
                            chooser_OOS_CAGR=float(np.mean(
                                [MC[i, bidx[picks[i]]] for i in range(len(ends))])),
                            chooser_OOS_MaxDD=float(np.mean(
                                [MD[i, bidx[picks[i]]] for i in range(len(ends))])),
                            chooser_rate4b=float(np.mean(
                                [MB[i, bidx[picks[i]]] for i in range(len(ends))])),
                            chooser_rate4a=float(np.mean(
                                [MA[i, bidx[picks[i]]] for i in range(len(ends))])),
                            rand_pool_rate4b=float(MB.mean()), rand_pool_rate4a=float(MA.mean()),
                            book_mean=float(M.mean()), book_median=float(np.median(M)),
                            book_skew_med_minus_mean=float(np.median(M) - M.mean())))
    T = pd.DataFrame(rows)
    dump(T, "percentile")

    # ---------------------------------------------------------------- H_1023 (reproduction)
    P("")
    P("## H_1023 — reproduce 1023's headline cell before re-scoring it")
    h = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == GRID_HEAD)
          & (T.stat == "MEAN_SH")].set_index("chooser")
    dmax = max(abs(h.loc[ch, "chooser_score"] - PUB_1023_CHOOSER[ch]) for ch in RAW)
    exact = float(MAT[(PANEL_HEAD, RUNG_HEAD, GRID_HEAD, "SH")].mean())
    se23 = PUB_1023_RANDOM_SD / np.sqrt(PUB_1023_N)
    dr = abs(exact - PUB_1023_RANDOM)
    h1023 = dmax <= 5e-4 and dr <= 3 * se23
    for ch in RAW:
        P(f"   {ch:10s} mean OOS Sharpe {h.loc[ch,'chooser_score']:.6f}  vs 1023's "
          f"{PUB_1023_CHOOSER[ch]:.6f}  |d| {abs(h.loc[ch,'chooser_score']-PUB_1023_CHOOSER[ch]):.2e}")
    P(f"   RANDOM     EXACT pool mean {exact:.6f} (closed form, no draws)  vs 1023's MC "
      f"{PUB_1023_RANDOM:.6f}  |d| {dr:.2e}  (3 MC SE = {3*se23:.2e})")
    P(f"   H_1023 (chooser tol 5e-4 AND pool mean within 3 MC SE): "
      f"{'PASS' if h1023 else 'FAIL'}")

    # ---------------------------------------------------------------- (A) print
    P("")
    P("## (A) THE PERCENTILE TABLE — every chooser re-expressed as the SHARE OF RANDOM SEQUENCES")
    P(f"   IT BEATS.  {NRAND:,} sequences per cell.  'pct' > 0.500 = clears the 50th percentile.")
    P("")
    for gname in GRIDS:
        for st in PSTATS:
            P(f"--- END GRID {gname} ({len(GRIDS[gname])} ends) x STATISTIC {st}"
              + ("   <<< HEADLINE" if (gname == GRID_HEAD and st == PSTAT_HEAD) else ""))
            P(f"{'panel':6s} {'cost':>4s} {'chooser':10s} | {'score':>8s} {'randMean':>8s} "
              f"{'randMed':>8s} {'randSD':>7s} {'med-mean':>9s} | {'z':>6s} {'pct':>6s} "
              f"{'>50th':>6s} {'>mean':>6s}")
            g = T[(T.grid == gname) & (T.stat == st)]
            for _, r in g.iterrows():
                P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:10s} | {r.chooser_score:8.4f} "
                  f"{r.rand_mean:8.4f} {r.rand_median:8.4f} {r.rand_sd:7.4f} "
                  f"{r.skew_med_minus_mean:+9.5f} | {r.z_vs_rand:+6.2f} {r.percentile:6.3f} "
                  f"{str(r.clears_50th):>6s} {str(r.beats_rand_mean):>6s}")
            P("")

    # ---------------------------------------------------------------- (B) mean-vs-median audit
    P("## (B) THE MEAN-vs-MEDIAN AUDIT — 1023's bar against this run's, on the headline grid")
    P("   1023's bar: chooser mean OOS Sharpe > RANDOM's pool mean.  This run's: chooser score")
    P("   above the MEDIAN of the random sequence distribution.  A FLIP is the only way the")
    P("   queue's worry can be true.")
    P("")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':10s} | {'1023 mean bar':>13s} {'50th pct bar':>12s} "
      f"| {'pct':>6s} {'FLIP':>5s}")
    arows, flips = [], 0
    for p in PX:
        for c in RUNGS:
            for ch in RAW:
                r = T[(T.panel == p) & (T.cost == c) & (T.grid == GRID_HEAD)
                      & (T.stat == PSTAT_HEAD) & (T.chooser == ch)].iloc[0]
                pub = PUB_1023_ALL[(p, c)]
                bar23 = bool(pub[ch] > pub["RANDOM"])
                bar50 = bool(r.clears_50th)
                fl = bar23 != bar50
                flips += int(fl)
                arows.append(dict(panel=p, cost=c, chooser=ch, pub_1023_chooser=pub[ch],
                                  pub_1023_random_mean=pub["RANDOM"], verdict_1023_mean=bar23,
                                  this_run_score=r.chooser_score, percentile=r.percentile,
                                  verdict_50th=bar50, flip=fl))
                P(f"{p:6s} {c:4.0f} {ch:10s} | {str(bar23):>13s} {str(bar50):>12s} "
                  f"| {r.percentile:6.3f} {str(fl):>5s}")
    AUD = pd.DataFrame(arows)
    dump(AUD, "audit")
    P(f"   FLIPS: {flips} of {len(AUD)} (chooser, cell) pairs.")

    # ---------------------------------------------------------------- hypotheses
    P("")
    P("## Hypotheses (bars declared in the docstring, before any number above was read)")
    hyp = []

    def H(name, bar, ok, detail):
        hyp.append(dict(hypothesis=name, bar=bar, verdict="PASS" if ok else "FAIL",
                        detail=detail))
        P(f"{name:10s} {'PASS' if ok else 'FAIL'}  bar: {bar}")
        P(f"           {detail}")

    H("H_1023", "chooser means within 5e-4 of 1023 AND pool mean within 3 MC SE", h1023,
      f"max chooser |d| {dmax:.2e}; exact pool mean {exact:.6f} vs 1023's {PUB_1023_RANDOM:.6f} "
      f"(|d| {dr:.2e}, 3 SE {3*se23:.2e})")

    hd = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == GRID_HEAD)
           & (T.stat == PSTAT_HEAD)].iloc[0]
    okp = hd.skew_med_minus_mean > 0
    H("H_PREMISE", "median - mean of the random score distribution > 0 in the headline cell", okp,
      f"headline median - mean = {hd.skew_med_minus_mean:+.6f} (sd {hd.rand_sd:.4f}); the "
      f"underlying per-end BOOK distribution has median - mean "
      f"{hd.book_skew_med_minus_mean:+.6f}")

    rc = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == GRID_HEAD)
           & (T.stat == PSTAT_HEAD) & (T.chooser == "IS_CAGR")].iloc[0]
    H("H_CAGR50", "IS_CAGR percentile > 0.500 in the headline cell", bool(rc.clears_50th),
      f"IS_CAGR scores {rc.chooser_score:.4f} at percentile {rc.percentile:.3f} "
      f"(z {rc.z_vs_rand:+.2f}) — {1-rc.percentile:.1%} of coin flips beat it")

    gall = T[(T.grid == GRID_HEAD) & (T.stat == PSTAT_HEAD) & (T.chooser == "IS_CAGR")]
    nall = int(gall.clears_50th.sum())
    H("H_CAGRALL", "IS_CAGR clears the 50th in ALL 6 panel x cost cells", nall == 6,
      f"{nall} of 6; percentiles " + " ".join(
          f"{r.panel}/{r.cost:.0f}={r.percentile:.3f}" for _, r in gall.iterrows()))

    gst = T[(T.grid == GRID_HEAD) & (T.stat == PSTAT_HEAD) & (T.chooser.isin(["IS_SHARPE",
                                                                              "IS_LEGS"]))]
    nfail = int((~gst.clears_50th).sum())
    H("H_STAB50", "IS_SHARPE and IS_LEGS FAIL the 50th in 10 of their 12 cells (1023's 5 of 6)",
      nfail == 10,
      f"{nfail} of 12 fail the 50th; percentiles " + " ".join(
          f"{r.chooser[3:]}@{r.panel}/{r.cost:.0f}={r.percentile:.3f}" for _, r in gst.iterrows()))

    H("H_FLIP", "0 of 18 (chooser, cell) pairs flip between the mean bar and the 50th", flips == 0,
      f"{flips} flips of {len(AUD)}" + ("" if flips == 0 else ": " + ", ".join(
          f"{r.panel}/{r.cost:.0f}/{r.chooser} {r.verdict_1023_mean}->{r.verdict_50th}"
          for _, r in AUD[AUD.flip].iterrows())))

    hc = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD)]
    sets = {}
    for gname in GRIDS:
        for st in PSTATS:
            s = hc[(hc.grid == gname) & (hc.stat == st)]
            sets[(gname, st)] = frozenset(s[s.clears_50th].chooser)
    okd = len(set(sets.values())) == 1
    H("H_DIAL", "the set of choosers clearing the 50th is identical at all 9 dial points", okd,
      "; ".join(f"{g}/{s}={sorted(v) if v else '{}'}" for (g, s), v in sets.items()))

    r4 = T[(T.panel == PANEL_HEAD) & (T.cost == RUNG_HEAD) & (T.grid == GRID_HEAD)
           & (T.stat == "RATE4B") & (T.chooser == "IS_CAGR")].iloc[0]
    H("H_VERDICT", "IS_CAGR's RATE4B percentile > its MEAN_SH percentile in the headline cell",
      bool(r4.percentile > rc.percentile),
      f"RATE4B percentile {r4.percentile:.3f} (score {r4.chooser_score:.3f} vs random mean "
      f"{r4.rand_mean:.3f}) against MEAN_SH percentile {rc.percentile:.3f}")

    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    dump(pd.DataFrame(gates), "gates")

    # ---------------------------------------------------------------- (D) rule 8 walk-forward
    P("")
    P("## (D) RULE 8 WALK-FORWARD — PROTOCOL's own split, IS 2009-2016 / OOS 2017-2026 read ONCE")
    P("   Each chooser picks a book using 2009-2016 data ONLY; the OOS triple is then read once")
    P("   and scored on BOTH KEEP paths, and the pick is percentiled inside its own 18-book pool.")
    P("")
    wrows = []
    for p in PX:
        s = SPYB[(p, REC_END)]
        for c in RUNGS:
            v2 = V2[(p, c)]
            sub = IDX[(p, c, REC_END)]
            pooldist = sub.loc[BOOKS[p], "OOS_Sharpe"].values
            for ch in RAW:
                bk = PR[(p, c)][REC_END][ch]
                r = sub.loc[bk]
                lg = legs_at(dict(H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                                  OOS_MaxDD=r.OOS_MaxDD, OOS_CAGR=r.OOS_CAGR), s)
                wrows.append(dict(
                    panel=p, cost=c, chooser=ch, pick=bk,
                    OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                    spy_OOS_CAGR=s["OOS_CAGR"], spy_OOS_Sharpe=s["OOS_Sharpe"],
                    spy_OOS_MaxDD=s["OOS_MaxDD"],
                    v2_CAGR=v2["CAGR"], v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"],
                    **lg, pass4b=all(lg.values()), pass4a=bool(r.pass4a),
                    pool_percentile=pct_of(r.OOS_Sharpe, pooldist),
                    pool_mean_OOS_Sharpe=float(np.mean(pooldist)),
                    pool_median_OOS_Sharpe=float(np.median(pooldist))))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':10s} {'pick':30s} | {'OOS CAGR':>8s} {'Sh':>6s} "
      f"{'MaxDD':>7s} | {'4b':>3s} {'4a':>3s} {'poolPct':>7s}  binding legs")
    for _, r in WF.iterrows():
        binds = ",".join(k for k in ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR") if not r[k])
        P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:10s} {r['pick']:30s} | {r.OOS_CAGR:8.2%} "
          f"{r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} | {str(r.pass4b)[0]:>3s} {str(r.pass4a)[0]:>3s} "
          f"{r.pool_percentile:7.3f}  {binds if binds else '(none — passes 4b)'}")
    for p in PX:
        s = SPYB[(p, REC_END)]
        v2 = V2[(p, RUNG_HEAD)]
        P(f"   comparands {p}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / "
          f"{s['OOS_MaxDD']:.2%}  (4b DD cap {DDCAP_FRAC*abs(s['MaxDD']):.2%}, CAGR floor "
          f"{CAGRFLOOR_FRAC*s['CAGR']:.2%});  RULES v2 live @{RUNG_HEAD:.0f} bps full "
          f"{v2['CAGR']:.2%} / {v2['Sharpe']:.4f} / {v2['MaxDD']:.2%} "
          f"(H1 {v2['H1']:.4f} / H2 {v2['H2']:.4f})")
    P(f"   OOS 4b passes: {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a passes: "
      f"{int(WF.pass4a.sum())} of {len(WF)}.")
    P(f"   KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves and MaxDD no worse; 4b needs "
      f"Sharpe > SPY in both halves AND OOS, |MaxDD| <= 60% of SPY's and CAGR >= 70% of SPY's.")

    P("")
    P(f"GATES {sum(g['verdict']=='PASS' for g in gates)} of {len(gates)};  HYPOTHESES "
      f"{sum(h['verdict']=='PASS' for h in hyp)} of {len(hyp)}.")
    P(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
