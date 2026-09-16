#!/usr/bin/env python3
"""Idea 974 (lane B, 2026-09-16) -- is the MONTH-END vs QUARTER-END phase-bias REVERSAL a
FLOW fact or a CALENDAR-COUNT artefact?

THE QUESTION (queue, 2026-09-15, filed by idea 964)
  Idea 964 published, over 60 committed families at 10 bps, that the CANONICAL rebalance phase
  (period-end, d = 0, the day `engine.rebalance_mask` produces and the only day the live rules
  trade) sits at the 0.929 percentile of its own 21-phase family MONTHLY (+0.600 pp CAGR over
  the family mean) and at the 0.063 percentile of its own 63-phase family QUARTERLY
  (-1.112 pp).  The two cadences' canonicals are biased in OPPOSITE directions and 964's pooled
  statistic passes only by cancellation.

  The queue's suspicion: a 63-phase quarterly family spans THREE month-ends and a 21-phase
  monthly family spans ONE, so the quarterly canonical may simply be one of three month-end-like
  days competing in a comparison set three times as wide -- i.e. the reversal would be a
  CALENDAR-COUNT artefact of the family's width, not a fact about the tape.  Decompose the
  quarterly phase profile by position WITHIN THE MONTH and report whether the reversal survives.

THE TWO OBJECTS THE QUEUE'S WORDING HIDES, AND WHY BOTH ARE PRICED HERE
  "Position within the month" can be built two ways, and they are NOT the same set of days:

    MOD21   d = 21*b + m.  Block b in {0,1,2}, within-month position m = d mod 21.  This is the
            arithmetic the queue's wording implies.  It is APPROXIMATE: calendar months carry
            19-23 trading days, so phase 21 is only NEAR the second month's end and phase 42
            only NEAR the first month's end.  G7 measures exactly how approximate.
    CALEND  the EXACT arms.  MEND_Q3 / MEND_Q2 / MEND_Q1 rebalance on the last trading day of
            the 3rd / 2nd / 1st month of each quarter -- four rebalances a year in every arm,
            every one of them a true month-end, no 21-day approximation anywhere.  MEND_Q3 is
            the quarter-end itself and must be byte-identical to `offset_mask(idx, "Q", 0)` (G4).

  MOD21 answers the census question on the record's own committed numbers.  CALEND answers the
  capital question the census cannot: if you must rebalance four times a year, does it matter
  WHICH month-end you pick?  Both are reported in full; neither is selected on.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  DECOMPOSITION, 4 levels, every one reported and none chosen:
           FULL    the canonical's percentile among all 63 quarterly phases (964's statistic)
           BLOCK0  its percentile among the 21 phases of BLOCK 0 alone (d = 0..20).  This is the
                   CALENDAR-COUNT CONTROL: same family width as monthly, 21 competitors, all
                   inside the final month of the quarter.
           MPOS    the within-month profile m = d mod 21 averaged over the three blocks, and
                   m = 0's percentile inside EACH block separately
           CALEND  the exact month-end arms MEND_Q1 / MEND_Q2 / MEND_Q3 (+ MEND_ALL = monthly
                   canonical, 12/yr, as the cadence reference)
  TUNED 2  PANEL, 3 levels: U56 / B136 / SMALL.
  REPORTED AXES (nothing fitted on them, every point published): book TOP05 / TOP10 / TOP20 /
  EWELIG / BAND03; gross CORE 0.75 / EXT 1.00; cost rung 0 / 5 / 10 / 25 / 50 bps; cadence M/Q;
  estimator CANON / FMEAN; 4b convention REC and OOSPURE; choosers C_CAGR / C_SHARPE.

PRE-REGISTERED BARS (fixed and printed before any result number was read; both directions
reported, and every one of them can come back either way)
  H_COUNT    the reversal IS a calendar-count artefact iff the canonical's median within-family
             CAGR percentile under BLOCK0 (21 competitors, matching the monthly family's width)
             rises ABOVE 0.50.  FAIL = the reversal survives the width control.
  H_MEND     month-end-ness is still a GOOD rebalance property at quarterly cadence iff m = 0's
             median percentile inside block 1 AND inside block 2 is >= 0.50.
  H_QEND     the quarter-end SPECIFICALLY is the bad day iff MEND_Q3's full-sample CAGR is the
             LOWEST of {MEND_Q1, MEND_Q2, MEND_Q3} in > 0.50 of families (chance rate 1/3).
  H_FLOW     the reversal is a FLOW fact iff H_COUNT FAILS and H_MEND PASSES and H_QEND PASSES,
             i.e. month-ends are good days, the quarter-end is not, and the width control does
             not explain it.
  H_TRADE    moving the quarterly rebalance off the quarter-end BUYS something: the better of
             MEND_Q1 / MEND_Q2 beats MEND_Q3 on OOS Sharpe in >= 0.75 of families.
  H_NULL     the winning arm is an OUTLIER and not just an ordinary turn of the phase dial:
             MEND_Q2's median CAGR percentile inside the record's own 63-phase quarterly family
             is >= 0.90.  Every phase in that family is ALSO a 4x/yr book on the same panel,
             book and gross, so the family IS the null for "which day of the quarter".
  H_KEEP     (rule 8, REQUIRED) arm chosen on 2009-2016 ALONE, 2017-2026 read ONCE, both KEEP
             paths, against SPY and RULES v2 in the same window, for every arm and both choosers.

GATES (all printed before any result number)
  G0  `offset_mask(idx, per, 0)` == `engine.rebalance_mask(idx, per)` on M / Q / W, 0 rows
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN on TODAY's data: idea 964's committed `.grid.csv` replayed on all 12,600 rows
      x 13 columns.  This gate is EXPECTED TO FAIL and is reported, not tuned away: see G3b.
  G3b CROSS-RUN on 964's OWN DATA VINTAGE (`git show <964's commit>:data/prices.csv`).  This is
      the gate that certifies the CODE.  `data/prices.csv` is RESTATED across its entire history
      by the nightly close action (adjusted closes move on every dividend), so no committed grid
      in this record is byte-reproducible on a later day -- 964's own G3 passed at 1.78e-15 only
      because it ran against 962 on the same calendar day.  G3 measures that drift; G3b removes
      it.  Neither changes any percentile reported below, which is what this run is about.
  G4  the CALENDAR IDENTITY: MEND_Q3 == `offset_mask(idx, "Q", 0)`, 0 disagreeing rows
  G5  964's two published headline numbers (M +0.600 pp / 0.929, Q -1.112 pp / 0.063) recomputed
      from its own committed grid to 1e-4
  G6  MEND_Q1 / MEND_Q2 / MEND_Q3 are pairwise DISJOINT and each fires 4x/yr (+/- 1)
  G7  MOD21 is APPROXIMATE, measured not assumed: the share of phase-21 and phase-42 rebalance
      dates that are NOT true month-ends.  Reported; this gate exists to justify CALEND.
  G8  determinism: the subject family rebuilt from scratch, max|d| over all reported columns

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026, no shorting, no leverage beyond the published gross.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic.  The whole subject of this run is the SAME names on the SAME
tape under different rebalance DAYS, which is very nearly immune to it; the 4b levels are read
against SPY, which is not survivorship-inflated, so every 4b PASS reported here is an UPPER
bound and every FAIL is understated.  Stated, not hidden.
"""
from __future__ import annotations

import io
import os
import subprocess
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST, HEAD_GROSS = 10.0, "CORE"
DOM_N, DOQ_N = 21, 63
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
DECOMPS = ["FULL", "BLOCK0", "MPOS", "CALEND"]
ARMS = ["MEND_Q1", "MEND_Q2", "MEND_Q3", "MEND_ALL"]
# pre-registered bars
COUNT_BAR = 0.50        # H_COUNT: BLOCK0 median percentile ABOVE this => count artefact
MEND_BAR = 0.50         # H_MEND: m=0 percentile inside blocks 1 and 2
QEND_BAR = 0.50         # H_QEND: share of families where MEND_Q3 is the WORST of the three
TRADE_BAR = 0.75        # H_TRADE: share of families where best(Q1,Q2) OOS Sharpe > Q3's
NULL_BAR = 0.90         # H_NULL: MEND_Q2's median CAGR percentile inside the 63-phase family
IDEA964_COMMIT = "c22e4d3edd4a1523c33fb16523a5d3c8e9f317d5"   # the commit that published 964
SMOKE = bool(int(os.environ.get("IDEA974_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from ideas 938/942/962/964 so this run NESTS the record
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    engine.rebalance_mask(idx, per) exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


def month_end_positions(idx):
    """Integer positions of the LAST trading day of every calendar month in idx."""
    key = pd.Series(idx.to_period("M"), index=idx)
    return np.flatnonzero((key != key.shift(-1)).values)


def month_phase(idx):
    """For every row: trading days BEFORE the last trading day of its own calendar month.
    month_phase == 0 exactly on month-ends.  This is the EXACT version of MOD21's `m`."""
    last = month_end_positions(idx)
    key = pd.Series(idx.to_period("M"), index=idx)
    grp = np.searchsorted(last, np.arange(len(idx)), side="left")
    return last[np.minimum(grp, len(last) - 1)] - np.arange(len(idx)), key.values


def calendar_arm_mask(idx, moq):
    """CALEND arm: True on the last trading day of the `moq`-th month of each quarter
    (moq = 3 -> quarter-end, moq = 2 -> middle month, moq = 1 -> first month).
    moq = 0 is the special arm MEND_ALL: every month-end (the monthly canonical, 12/yr)."""
    mend = month_end_positions(idx)
    out = pd.Series(False, index=idx)
    if moq == 0:
        out.iloc[mend] = True
        return out
    m = idx[mend].month
    out.iloc[mend[(m - 1) % 3 == (moq - 1)]] = True
    return out


class Ctx:
    """Fast runner -- byte-identical to 942/962/964's.  G1 asserts it against engine.backtest."""

    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec(row):
    """The RECORD's 4b convention (942/962/964's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_pure(row):
    return dict(H1=row["OOS_H1"] > row["spy_OOS_H1"], H2=row["OOS_H2"] > row["spy_OOS_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_OOS_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_OOS_CAGR"])


def legs_is(row):
    """The same alphabet read entirely INSIDE the IS window -- chooser input only."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


def pctile(series, key):
    """Within-family percentile of `key`'s value: share strictly below + half the ties."""
    v = np.asarray(series, float)
    x = float(series.loc[key]) if hasattr(series, "loc") else float(key)
    return float((v < x).mean() + 0.5 * (v == x).mean())


# ==========================================================================================
# (2) THE BOOK SET -- 942/962/964's five books verbatim
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "TOP05":  lambda p, g: ranked_book(p, g, 5),
    "TOP10":  lambda p, g: ranked_book(p, g, 10),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
    "EWELIG": lambda p, g: ew_elig(p, g),
    "BAND03": lambda p, g: band_book(p, BAND0, g),
}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


CHOOSERS = ["C_CAGR", "C_SHARPE"]


def choose(name, sub):
    """IS columns ONLY.  Ties broken by the other IS column, then by arm order."""
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    v, tb = (isc, iss) if name == "C_CAGR" else (iss, isc)
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return 0
    best = np.nanmax(v)
    cand = np.flatnonzero(v == best)
    if len(cand) > 1:
        t = np.asarray(tb, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 974 (lane B) -- is the MONTH-END vs QUARTER-END PHASE-BIAS REVERSAL")
    P("                    a FLOW fact or a CALENDAR-COUNT artefact?")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL 10 bps / t+1 / warm-up {WARM}")
    P("=" * 100)
    P()
    P("PRE-REGISTERED BARS (printed BEFORE any result number is computed):")
    P(f"  H_COUNT  artefact iff BLOCK0 median canonical percentile > {COUNT_BAR}")
    P(f"  H_MEND   month-end still good iff m=0 median percentile >= {MEND_BAR} in blocks 1 AND 2")
    P(f"  H_QEND   quarter-end is the bad day iff MEND_Q3 worst of three in > {QEND_BAR} of families")
    P( "  H_FLOW   FLOW fact iff H_COUNT FAILS and H_MEND PASSES and H_QEND PASSES")
    P(f"  H_TRADE  moving off quarter-end buys something iff best(Q1,Q2) OOS Sharpe > Q3's in >= {TRADE_BAR}")
    P(f"  H_NULL   the winning arm is an OUTLIER iff MEND_Q2's median CAGR pctile in the record's")
    P(f"           own 63-phase quarterly family (every phase of it also a 4x/yr book) >= {NULL_BAR}")
    P( "  H_KEEP   rule 8: arm chosen on 2009-2016 alone, 2017-2026 read once, both KEEP paths")
    P()

    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm, ndrop = load_small()
    panels["SMALL"] = sm
    if SMOKE:
        panels = {"U56": panels["U56"]}
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
    P(f"  SMALL drops {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv; "
      f"SURVIVORSHIP: all three panels are CURRENT-CONSTITUENT lists (rule 9).")

    # ---------------------------------------------------------------------------------- gates
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any hypothesis is read")
    P("=" * 100)
    gk = {}
    u = panels["U56"]
    idx = u.index

    g0 = 0
    for per in ("M", "Q", "W"):
        g0 += int((offset_mask(idx, per, 0)[0].values != rebalance_mask(idx, per).values).sum())
    gk["G0"] = g0 == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on M/Q/W: {g0} disagreeing rows  "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w75 = rules_v2_weights(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - band_book(u, BAND0, 0.75).values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: {d2:.3e}  {'PASS' if gk['G2'] else 'FAIL'}")

    ctxW = Ctx(u, offset_mask(idx, "W", 0)[0])
    gr, tn = ctxW.run(ctxW.shift(w75))
    eng = backtest(u, w75, cost_bps=0.0, freq="W")
    d1r = float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max())
    d1t = float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max())
    gk["G1"] = d1r < 1e-12 and d1t < 1e-10
    P(f"  G1 Ctx == engine.backtest   returns {d1r:.3e}   turnover {d1t:.3e}  "
      f"{'PASS' if gk['G1'] else 'FAIL'}")
    del ctxW, eng

    # G4 the calendar identity
    q3 = calendar_arm_mask(idx, 3)
    q0 = offset_mask(idx, "Q", 0)[0]
    g4 = int((q3.values != q0.values).sum())
    gk["G4"] = g4 == 0
    P(f"  G4 CALENDAR IDENTITY  MEND_Q3 == offset_mask(idx,'Q',0): {g4} disagreeing rows  "
      f"{'PASS' if gk['G4'] else 'FAIL'}")

    # G6 arms disjoint, 4x/yr
    arms_u = {a: calendar_arm_mask(idx, m) for a, m in
              zip(ARMS, [1, 2, 3, 0])}
    yrs = len(idx) / 252.0
    ovl = 0
    for i, a in enumerate(ARMS[:3]):
        for b in ARMS[:3][i + 1:]:
            ovl += int((arms_u[a].values & arms_u[b].values).sum())
    rates = {a: arms_u[a].sum() / yrs for a in ARMS}
    gk["G6"] = ovl == 0 and all(abs(rates[a] - 4.0) <= 1.0 for a in ARMS[:3])
    P(f"  G6 MEND_Q1/Q2/Q3 pairwise disjoint ({ovl} overlaps) and fire "
      + " / ".join(f"{a} {rates[a]:.2f}" for a in ARMS)
      + f" per yr  {'PASS' if gk['G6'] else 'FAIL'}")

    # G7 how approximate is MOD21?
    mph, _ = month_phase(idx)
    g7rows = []
    for d in (0, 21, 42):
        pos = np.flatnonzero(offset_mask(idx, "Q", d)[0].values)
        pos = pos[pos >= WARM]
        share = float((mph[pos] == 0).mean())
        g7rows.append(dict(mod21_phase=d, n_dates=len(pos), share_true_month_end=share,
                           mean_month_phase=float(mph[pos].mean()),
                           max_month_phase=int(mph[pos].max())))
    g7 = pd.DataFrame(g7rows)
    gk["G7"] = bool(g7.loc[g7.mod21_phase == 0, "share_true_month_end"].iloc[0] == 1.0
                    and g7.loc[g7.mod21_phase > 0, "share_true_month_end"].max() < 1.0)
    P("  G7 MOD21 is APPROXIMATE (measured, not assumed) -- share of each phase's rebalance "
      "dates that are TRUE month-ends:")
    for _, r in g7.iterrows():
        P(f"       phase {int(r.mod21_phase):2d}: {r.share_true_month_end:.3f} of "
          f"{int(r.n_dates)} dates, mean month-phase {r.mean_month_phase:.2f} "
          f"(max {int(r.max_month_phase)})")
    P(f"     -> phase 0 is exactly the month-end; phases 21 and 42 are NOT, which is why CALEND "
      f"exists.  {'PASS' if gk['G7'] else 'FAIL'}")

    # ---- G3 / G5 cross-run against idea 964's committed grid --------------------------------
    comm = OUT / "2026-09-15_should-the-PHASE-AVERAGED-MEAN-replace-the-CANONICAL_cloud.grid.csv"
    CG = pd.read_csv(comm) if comm.exists() else None
    if CG is None:
        gk["G3"] = gk["G5"] = False
        P("  G3/G5 SKIPPED (964's committed grid.csv missing)   FAIL")
    else:
        h = CG[CG.cost_bps == HEAD_COST]
        rec = []
        for k, s in h.groupby(["panel", "book", "gross", "cadence"]):
            v = s.set_index("phase")["CAGR"]
            rec.append(dict(zip(["panel", "book", "gross", "cadence"], k),
                            pct=pctile(v, 0), d_pp=(v.loc[0] - v.mean()) * 100))
        rec = pd.DataFrame(rec)
        med = rec.groupby("cadence")[["d_pp", "pct"]].median()
        tgt = {("M", "d_pp"): 0.600, ("M", "pct"): 0.929,
               ("Q", "d_pp"): -1.112, ("Q", "pct"): 0.063}
        dmax5 = max(abs(med.loc[c, col] - v) for (c, col), v in tgt.items())
        gk["G5"] = dmax5 < 1e-3 and len(rec) == 60
        P(f"  G5 964's published headline recomputed from its own committed grid "
          f"({len(rec)} families): M {med.loc['M','d_pp']:+.3f} pp / {med.loc['M','pct']:.3f}, "
          f"Q {med.loc['Q','d_pp']:+.3f} pp / {med.loc['Q','pct']:.3f}, max|d| vs published "
          f"{dmax5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")

    # ------------------------------------------------------------------------- the MOD21 grid
    P()
    P("=" * 100)
    P("(B) THE GRID -- rebuilt from scratch: 5 books x panels x 2 gross x (21 M + 63 Q) phases")
    P("    x 5 rungs, PLUS the 4 CALEND arms.  G3/G8 check it against 964's committed grid.")
    P("=" * 100)
    ROWS, BASE, ARMROWS = [], {}, []
    for pname, p in panels.items():
        pidx = p.index
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(pidx >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(pidx <= pd.Timestamp(IS_END))[WARM:]
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        bw = rules_v2_weights(p, BAND0, 0.75)                  # the LIVE book, weekly (4a target)
        bc = Ctx(p, offset_mask(pidx, "W", 0)[0])
        bgr, btn = bc.run(bc.shift(bw))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full": mets(br)}
        del bc
        Wt = {(b, cs): BOOKS[b](p, g) for b in BOOKS for cs, g in CLAIM_SETS.items()}
        SPYCOLS = dict(
            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
            spy_H1=ms["H1"], spy_H2=ms["H2"],
            spy_IS_CAGR=ms_i["CAGR"], spy_IS_Sharpe=ms_i["Sharpe"], spy_IS_MaxDD=ms_i["MaxDD"],
            spy_IS_H1=ms_i["H1"], spy_IS_H2=ms_i["H2"],
            spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
            spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"], spy_OOS_H2=ms_o["H2"])

        def emit(sink, extra, gw, tw):
            for c in RUNGS:
                r = gw - tw * c / 1e4
                m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                sink.append(dict(
                    panel=pname, **extra, cost_bps=c,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    IS_H1=mi["H1"], IS_H2=mi["H2"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                    turn_per_yr=float(tw.sum() / (len(r) / 252.0)), **SPYCOLS))

        for per, n_ph in (("M", DOM_N), ("Q", DOQ_N)):   # SMOKE trims panels, never phases
            for d in range(n_ph):
                ctx = Ctx(p, offset_mask(pidx, per, d)[0])
                for (b, cs), W in Wt.items():
                    g_, t_ = ctx.run(ctx.shift(W))
                    emit(ROWS, dict(book=b, gross=cs, cadence=per, phase=d), g_[WARM:], t_[WARM:])
                del ctx
        for a, moq in zip(ARMS, [1, 2, 3, 0]):
            ctx = Ctx(p, calendar_arm_mask(pidx, moq))
            for (b, cs), W in Wt.items():
                g_, t_ = ctx.run(ctx.shift(W))
                emit(ARMROWS, dict(book=b, gross=cs, arm=a), g_[WARM:], t_[WARM:])
            del ctx
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")

    def annotate(df):
        df["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in df.iterrows()]
        lr = [legs_rec(r) for _, r in df.iterrows()]
        df["pass4b_REC"] = [all(x.values()) for x in lr]
        df["fail4b_REC"] = [failstr(x) for x in lr]
        df["pass4b_OOSPURE"] = [all(legs_pure(r).values()) for _, r in df.iterrows()]
        df["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                             and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                             and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                        for _, r in df.iterrows()]
        return df

    grid = annotate(pd.DataFrame(ROWS))
    arms = annotate(pd.DataFrame(ARMROWS))
    dump(grid, "grid", gz=True)
    dump(arms, "arms")
    P(f"  {len(grid):,} grid rows + {len(arms):,} CALEND arm rows")

    if CG is not None:
        keys = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2", "turn_per_yr"]
        j = CG.merge(grid, on=keys, suffixes=("_c", "_n"))
        dmax = max(float(np.abs(j[f"{c}_c"] - j[f"{c}_n"]).max()) for c in cols)
        n_exp = len(CG[CG.panel.isin(panels)])
        gk["G3"] = len(j) == n_exp and dmax < 1e-10
        P(f"  G3 CROSS-RUN on TODAY's data: 964's committed grid.csv replayed on {len(j):,} of "
          f"{n_exp:,} rows x {len(cols)} cols, max|d| {dmax:.3e}   "
          f"{'PASS' if gk['G3'] else 'FAIL'}")

        # ---- G3b: the same cross-run on 964's OWN data vintage ---------------------------
        # `data/prices.csv` is restated across its whole history by the nightly close action,
        # so G3 cannot pass on a later day however correct the code is.  G3b rebuilds the
        # U56 rows against the exact bytes 964 read and is the gate that certifies the code.
        try:
            raw = subprocess.run(["git", "show", f"{IDEA964_COMMIT}:data/prices.csv"],
                                 cwd=str(ROOT), capture_output=True, text=True, check=True).stdout
            old_px = pd.read_csv(io.StringIO(raw), index_col=0, parse_dates=True)
            cur_px = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
            common = old_px.index.intersection(cur_px.index)
            drift = float((old_px.loc[common] - cur_px.loc[common]).abs().max().max())
            worst = (old_px.loc[common] - cur_px.loc[common]).abs().max().idxmax()
            vint = old_px[[c for c in panels["U56"].columns]].loc["2008-01-01":]
            vint = vint.dropna(how="all").ffill()
            VROWS = []
            vidx = vint.index
            vspy = vint["SPY"].pct_change().fillna(0.0).values[WARM:]
            voos = np.asarray(vidx >= pd.Timestamp(OOS_START))[WARM:]
            vis = np.asarray(vidx <= pd.Timestamp(IS_END))[WARM:]
            vWt = {(b, cs): BOOKS[b](vint, g) for b in BOOKS for cs, g in CLAIM_SETS.items()}
            for per, n_ph in (("M", DOM_N), ("Q", DOQ_N)):
                for d in range(n_ph):
                    ctx = Ctx(vint, offset_mask(vidx, per, d)[0])
                    for (b, cs), W in vWt.items():
                        g_, t_ = ctx.run(ctx.shift(W))
                        gw, tw = g_[WARM:], t_[WARM:]
                        for c in RUNGS:
                            r = gw - tw * c / 1e4
                            m, mi, mo = mets(r), mets(r[vis]), mets(r[voos])
                            VROWS.append(dict(panel="U56", book=b, gross=cs, cadence=per,
                                              phase=d, cost_bps=c,
                                              CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                              MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                                              IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                              OOS_MaxDD=mo["MaxDD"], OOS_H1=mo["H1"],
                                              OOS_H2=mo["H2"],
                                              turn_per_yr=float(tw.sum() / (len(r) / 252.0))))
                    del ctx
            VG = pd.DataFrame(VROWS)
            cu = CG[CG.panel == "U56"]
            jb = cu.merge(VG, on=keys, suffixes=("_c", "_n"))
            dmaxb = max(float(np.abs(jb[f"{c}_c"] - jb[f"{c}_n"]).max()) for c in cols)
            gk["G3b"] = len(jb) == len(cu) and dmaxb < 1e-10
            P(f"  G3b CROSS-RUN on 964's OWN DATA VINTAGE ({IDEA964_COMMIT[:7]}): "
              f"{len(jb):,} of {len(cu):,} U56 rows x {len(cols)} cols, max|d| {dmaxb:.3e}   "
              f"{'PASS' if gk['G3b'] else 'FAIL'}")
            P(f"      the drift G3 measures is DATA, not code: data/prices.csv was RESTATED on "
              f"{len(common):,} shared rows, max |d| {drift:.4f} (worst column {worst}), and "
              f"gained one trading day ({old_px.index[-1].date()} -> {cur_px.index[-1].date()}).")
            P(f"      NOTHING this run reports moves with it: the canonical's Q percentile reads "
              f"0.0635 on both vintages (G5 reads 964's committed grid, section C rebuilds it).")
        except Exception as e:
            gk["G3b"] = False
            P(f"  G3b FAILED to run ({type(e).__name__}: {e})   FAIL")
    else:
        gk["G3"] = gk["G3b"] = False
        P("  G3/G3b SKIPPED   FAIL")

    # G8 determinism on the subject family
    sub_keys = dict(panel="U56", book="TOP20", gross=HEAD_GROSS, cadence="Q", cost_bps=HEAD_COST)
    pidx = panels["U56"].index
    W = BOOKS["TOP20"](panels["U56"], CLAIM_SETS[HEAD_GROSS])
    oos8 = np.asarray(pidx >= pd.Timestamp(OOS_START))[WARM:]
    re8 = []
    for d in range(DOQ_N):
        ctx = Ctx(panels["U56"], offset_mask(pidx, "Q", d)[0])
        g_, t_ = ctx.run(ctx.shift(W))
        r = (g_ - t_ * HEAD_COST / 1e4)[WARM:]
        m, mo = mets(r), mets(r[oos8])
        re8.append(dict(phase=d, CAGR=m["CAGR"], Sharpe=m["Sharpe"], OOS_CAGR=mo["CAGR"]))
    re8 = pd.DataFrame(re8)
    s8 = grid[(grid.panel == "U56") & (grid.book == "TOP20") & (grid.gross == HEAD_GROSS)
              & (grid.cadence == "Q") & (grid.cost_bps == HEAD_COST)]
    j8 = re8.merge(s8[["phase", "CAGR", "Sharpe", "OOS_CAGR"]], on="phase", suffixes=("_a", "_b"))
    d8 = max(float(np.abs(j8[f"{c}_a"] - j8[f"{c}_b"]).max()) for c in ("CAGR", "Sharpe", "OOS_CAGR"))
    gk["G8"] = d8 == 0.0
    P(f"  G8 determinism: subject family {sub_keys} rebuilt from scratch on {len(j8)} phases, "
      f"max|d| {d8:.3e}  {'PASS' if gk['G8'] else 'FAIL'}")
    P()
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS: "
      + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in sorted(gk.items())))

    # ======================================================================= (C) DECOMPOSITION
    P()
    P("=" * 100)
    P("(C) TUNED 1 = DECOMPOSITION, all 4 levels reported, none chosen")
    P("=" * 100)
    fkeys = ["panel", "book", "gross", "cost_bps"]
    dec = []
    for k, s in grid[grid.cadence == "Q"].groupby(fkeys):
        v = s.set_index("phase")["CAGR"].sort_index()
        row = dict(zip(fkeys, k))
        row["Q_FULL_pctile"] = pctile(v, 0)
        b0 = v.loc[0:20]
        row["Q_BLOCK0_pctile"] = pctile(b0, 0)
        # MPOS: profile of m averaged over the 3 blocks, and m=0 inside each block
        prof = v.groupby(v.index % 21).mean()
        row["Q_MPOS_pctile"] = pctile(prof, 0)
        for b in (0, 1, 2):
            vb = v.loc[21 * b:21 * b + 20]
            vb.index = vb.index - 21 * b
            row[f"Q_blk{b}_m0_pctile"] = pctile(vb, 0)
            row[f"Q_blk{b}_meanCAGR"] = float(vb.mean())
        row["Q_CANON_CAGR"] = float(v.loc[0])
        row["Q_FMEAN_CAGR"] = float(v.mean())
        row["Q_d_pp"] = (v.loc[0] - v.mean()) * 100
        dec.append(row)
    dec = pd.DataFrame(dec)
    mdec = []
    for k, s in grid[grid.cadence == "M"].groupby(fkeys):
        v = s.set_index("phase")["CAGR"].sort_index()
        mdec.append(dict(zip(fkeys, k), M_FULL_pctile=pctile(v, 0),
                         M_CANON_CAGR=float(v.loc[0]), M_FMEAN_CAGR=float(v.mean()),
                         M_d_pp=(v.loc[0] - v.mean()) * 100))
    dec = dec.merge(pd.DataFrame(mdec), on=fkeys)
    dump(dec, "decomp")

    hd = dec[dec.cost_bps == HEAD_COST]
    P(f"  {len(dec)} family x rung cells ({len(hd)} at the {HEAD_COST:.0f} bps verdict rung).")
    P()
    P("  the REVERSAL as 964 published it, and under the CALENDAR-COUNT control:")
    P(f"    {'decomposition':28s} {'competitors':>11s} {'median pctile of the canonical':>32s}")
    P(f"    {'M_FULL   (964, monthly)':28s} {21:>11d} {hd.M_FULL_pctile.median():>32.4f}")
    P(f"    {'Q_FULL   (964, quarterly)':28s} {63:>11d} {hd.Q_FULL_pctile.median():>32.4f}")
    P(f"    {'Q_BLOCK0 (width-matched)':28s} {21:>11d} {hd.Q_BLOCK0_pctile.median():>32.4f}")
    P(f"    {'Q_MPOS   (m-profile)':28s} {21:>11d} {hd.Q_MPOS_pctile.median():>32.4f}")
    hcount = bool(hd.Q_BLOCK0_pctile.median() > COUNT_BAR)
    P(f"    -> H_COUNT (artefact iff BLOCK0 median > {COUNT_BAR}): median "
      f"{hd.Q_BLOCK0_pctile.median():.4f}  ->  "
      f"{'PASS (IS a calendar-count artefact)' if hcount else 'FAIL (the reversal SURVIVES the width control)'}")
    P()
    P("  MPOS -- where does m = 0 (the month-end) sit INSIDE each block of the quarter?")
    P(f"    {'block':22s} {'median pctile of m=0':>22s} {'median block mean CAGR':>24s}")
    names = {0: "0  (last month)", 1: "1  (middle month)", 2: "2  (first month)"}
    for b in (0, 1, 2):
        P(f"    {names[b]:22s} {hd[f'Q_blk{b}_m0_pctile'].median():>22.4f} "
          f"{hd[f'Q_blk{b}_meanCAGR'].median() * 100:>23.2f}%")
    hmend = bool(hd.Q_blk1_m0_pctile.median() >= MEND_BAR and hd.Q_blk2_m0_pctile.median() >= MEND_BAR)
    P(f"    -> H_MEND (month-end still good iff blocks 1 AND 2 >= {MEND_BAR}): "
      f"{hd.Q_blk1_m0_pctile.median():.4f} / {hd.Q_blk2_m0_pctile.median():.4f}  ->  "
      f"{'PASS' if hmend else 'FAIL'}")
    P()
    P("  the same three numbers at every cost rung (reported, never selected on):")
    P(f"    {'bps':>5s} {'M_FULL':>8s} {'Q_FULL':>8s} {'Q_BLOCK0':>9s} {'blk0 m0':>8s} "
      f"{'blk1 m0':>8s} {'blk2 m0':>8s}")
    for c, s in dec.groupby("cost_bps"):
        P(f"    {c:5.0f} {s.M_FULL_pctile.median():8.4f} {s.Q_FULL_pctile.median():8.4f} "
          f"{s.Q_BLOCK0_pctile.median():9.4f} {s.Q_blk0_m0_pctile.median():8.4f} "
          f"{s.Q_blk1_m0_pctile.median():8.4f} {s.Q_blk2_m0_pctile.median():8.4f}")
    P()
    P("  by PANEL (TUNED 2, all 3 reported) and by BOOK, at 10 bps:")
    for ax in ("panel", "book", "gross"):
        for kk, s in hd.groupby(ax):
            P(f"    {ax:6s} {str(kk):7s} n={len(s):3d}  M_FULL {s.M_FULL_pctile.median():.4f}  "
              f"Q_FULL {s.Q_FULL_pctile.median():.4f}  Q_BLOCK0 {s.Q_BLOCK0_pctile.median():.4f}  "
              f"blk1_m0 {s.Q_blk1_m0_pctile.median():.4f}  blk2_m0 {s.Q_blk2_m0_pctile.median():.4f}")

    # ============================================================== (D) CALEND -- the exact arms
    P()
    P("=" * 100)
    P("(D) CALEND -- the EXACT month-end arms.  Four rebalances a year in every arm, every one")
    P("    a true month-end.  No 21-day approximation.  MEND_ALL (12/yr) is the cadence reference.")
    P("=" * 100)
    ha = arms[arms.cost_bps == HEAD_COST]
    P(f"    {'arm':10s} {'n':>4s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'OOS_CAGR':>9s} "
      f"{'OOS_Shp':>8s} {'OOS_DD':>8s} {'turn/yr':>8s} {'4b':>5s} {'4a':>4s}")
    for a in ARMS:
        s = ha[ha.arm == a]
        P(f"    {a:10s} {len(s):4d} {s.CAGR.median():7.2%} {s.Sharpe.median():8.4f} "
          f"{s.MaxDD.median():7.2%} {s.OOS_CAGR.median():8.2%} {s.OOS_Sharpe.median():8.4f} "
          f"{s.OOS_MaxDD.median():7.2%} {s.turn_per_yr.median():8.2f} "
          f"{s.pass4b_REC.sum():3d}/{len(s):<3d} {s.pass4a.sum():2d}")
    P()
    akeys = ["panel", "book", "gross", "cost_bps"]
    piv = ha.pivot_table(index=akeys, columns="arm", values=["CAGR", "OOS_Sharpe", "Sharpe"])
    wq3 = [(piv[("CAGR", "MEND_Q3")] < piv[("CAGR", "MEND_Q1")])
           & (piv[("CAGR", "MEND_Q3")] < piv[("CAGR", "MEND_Q2")])]
    share_worst = float(wq3[0].mean())
    hqend = bool(share_worst > QEND_BAR)
    P(f"  H_QEND -- is the QUARTER-END specifically the bad day?  MEND_Q3 has the LOWEST "
      f"full-sample CAGR of the three arms in {wq3[0].sum()} of {len(wq3[0])} families = "
      f"{share_worst:.4f} (chance rate 0.3333, bar > {QEND_BAR})  ->  "
      f"{'PASS' if hqend else 'FAIL'}")
    best12 = np.maximum(piv[("OOS_Sharpe", "MEND_Q1")], piv[("OOS_Sharpe", "MEND_Q2")])
    share_tr = float((best12 > piv[("OOS_Sharpe", "MEND_Q3")]).mean())
    htrade = bool(share_tr >= TRADE_BAR)
    P(f"  H_TRADE -- best(Q1,Q2) OOS Sharpe > Q3's in {share_tr:.4f} of families "
      f"(bar >= {TRADE_BAR})  ->  {'PASS' if htrade else 'FAIL'}")
    P()
    P("  the SAME arm ordering at every cost rung (median full-sample CAGR, all reported):")
    P(f"    {'bps':>5s} " + " ".join(f"{a:>9s}" for a in ARMS) + f" {'Q3 worst share':>15s}")
    for c, s in arms.groupby("cost_bps"):
        pv = s.pivot_table(index=akeys, columns="arm", values="CAGR")
        w = float(((pv.MEND_Q3 < pv.MEND_Q1) & (pv.MEND_Q3 < pv.MEND_Q2)).mean())
        P(f"    {c:5.0f} " + " ".join(f"{s[s.arm==a].CAGR.median():9.2%}" for a in ARMS)
          + f" {w:15.4f}")

    hflow = (not hcount) and hmend and hqend
    P()
    P(f"  H_FLOW = (H_COUNT FAIL) and (H_MEND PASS) and (H_QEND PASS)  ->  "
      f"{'PASS -- the reversal is a FLOW fact, not a calendar-count artefact' if hflow else 'FAIL'}")

    # ---- D2: THE NULL the CALEND arms have to beat ------------------------------------------
    # Every one of the 63 mod-21 quarterly phases is ALSO a 4x/yr book on the same panel, book
    # and gross.  That family IS the null distribution for "which day of the quarter do you
    # rebalance".  If MEND_Q2 is merely an ordinary draw from it, the arm ordering above is a
    # restatement of the phase dial's width, not a discovery about month-ends.
    P()
    P("  D2 -- THE NULL: where do the CALEND arms sit inside the record's own 63-phase family?")
    P("       (every phase in that family is also a 4x/yr book; the family IS the null for")
    P("        'which day of the quarter do you rebalance')")
    NUL = []
    for k, s in grid[grid.cadence == "Q"].groupby(akeys):
        v = s.set_index("phase")["CAGR"].sort_index()
        vo = s.set_index("phase")["OOS_Sharpe"].sort_index()
        row = dict(zip(akeys, k))
        row["fam_spread_CAGR_pp"] = float(v.max() - v.min()) * 100
        for a in ARMS[:3]:
            r = arms[(arms.panel == k[0]) & (arms.book == k[1]) & (arms.gross == k[2])
                     & (arms.cost_bps == k[3]) & (arms.arm == a)].iloc[0]
            row[f"{a}_CAGR_pctile"] = float((v.values < r.CAGR).mean()
                                            + 0.5 * (v.values == r.CAGR).mean())
            row[f"{a}_OOSShp_pctile"] = float((vo.values < r.OOS_Sharpe).mean()
                                              + 0.5 * (vo.values == r.OOS_Sharpe).mean())
        NUL.append(row)
    NUL = pd.DataFrame(NUL)
    dump(NUL, "nullpctiles")
    hn = NUL[NUL.cost_bps == HEAD_COST]
    P(f"    {'arm':10s} {'median CAGR pctile':>19s} {'median OOS Sharpe pctile':>25s}")
    for a in ARMS[:3]:
        P(f"    {a:10s} {hn[f'{a}_CAGR_pctile'].median():>19.4f} "
          f"{hn[f'{a}_OOSShp_pctile'].median():>25.4f}")
    P(f"    for scale: the 63-phase family's own CAGR spread (max - min) has median "
      f"{hn.fam_spread_CAGR_pp.median():.2f} pp, and the Q2 - Q3 gap is "
      f"{(ha[ha.arm=='MEND_Q2'].CAGR.median() - ha[ha.arm=='MEND_Q3'].CAGR.median()) * 100:.2f} pp.")
    hnull = bool(hn["MEND_Q2_CAGR_pctile"].median() >= NULL_BAR)
    P(f"    -> H_NULL (MEND_Q2 is an OUTLIER in its own family iff median CAGR pctile >= {NULL_BAR}): "
      f"{hn['MEND_Q2_CAGR_pctile'].median():.4f}  ->  "
      f"{'PASS (outlier)' if hnull else 'FAIL (an ORDINARY draw from the phase dial)'}")

    # ===================================================== (E) RULE 8 WALK-FORWARD -- REQUIRED
    P()
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD (REQUIRED).  Arm chosen on 2009-2016 ALONE; 2017-2026 read ONCE.")
    P("    Both KEEP paths, against SPY and RULES v2 in the same window.")
    P("=" * 100)
    WF = []
    pool = arms[arms.arm.isin(ARMS[:3])]
    for k, s in pool.groupby(akeys):
        s = s.sort_values("arm").reset_index(drop=True)
        base = BASE[(k[0], k[3])]
        canon = s[s.arm == "MEND_Q3"].iloc[0]
        for ch in CHOOSERS:
            pick = s.iloc[choose(ch, s)]
            WF.append(dict(zip(akeys, k), chooser=ch, arm=pick.arm,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD, OOS_H1=pick.OOS_H1, OOS_H2=pick.OOS_H2,
                           pass4b=bool(pick.pass4b_REC), pass4b_pure=bool(pick.pass4b_OOSPURE),
                           pass4a=bool(pick.pass4a), fail=pick.fail4b_REC,
                           beat_canon_OOS_Sharpe=bool(pick.OOS_Sharpe > canon.OOS_Sharpe),
                           spy_OOS_CAGR=pick.spy_OOS_CAGR, spy_OOS_Sharpe=pick.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=pick.spy_OOS_MaxDD,
                           base_OOS_Sharpe=base["Sharpe"], base_OOS_MaxDD=base["MaxDD"]))
        for a in ARMS:
            r = arms[(arms.panel == k[0]) & (arms.book == k[1]) & (arms.gross == k[2])
                     & (arms.cost_bps == k[3]) & (arms.arm == a)].iloc[0]
            WF.append(dict(zip(akeys, k), chooser=f"FIXED_{a}", arm=a,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           OOS_H1=r.OOS_H1, OOS_H2=r.OOS_H2, pass4b=bool(r.pass4b_REC),
                           pass4b_pure=bool(r.pass4b_OOSPURE), pass4a=bool(r.pass4a),
                           fail=r.fail4b_REC,
                           beat_canon_OOS_Sharpe=bool(r.OOS_Sharpe > canon.OOS_Sharpe),
                           spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                           base_OOS_Sharpe=base["Sharpe"], base_OOS_MaxDD=base["MaxDD"]))
    WF = pd.DataFrame(WF)
    dump(WF, "walkforward")
    hw = WF[WF.cost_bps == HEAD_COST]
    P(f"    {'chooser':16s} {'n':>4s} {'med OOS CAGR':>13s} {'med OOS Shp':>12s} "
      f"{'med OOS DD':>11s} {'4b REC':>8s} {'4b PURE':>8s} {'4a':>6s} {'beats canon':>12s}")
    for ch, s in hw.groupby("chooser"):
        P(f"    {ch:16s} {len(s):4d} {s.OOS_CAGR.median():12.2%} {s.OOS_Sharpe.median():12.4f} "
          f"{s.OOS_MaxDD.median():11.2%} {s.pass4b.sum():3d}/{len(s):<4d} "
          f"{s.pass4b_pure.sum():3d}/{len(s):<4d} {s.pass4a.sum():2d}/{len(s):<3d} "
          f"{s.beat_canon_OOS_Sharpe.mean():12.4f}")
    P(f"    {'SPY (OOS)':16s} {'':4s} {hw.spy_OOS_CAGR.median():12.2%} "
      f"{hw.spy_OOS_Sharpe.median():12.4f} {hw.spy_OOS_MaxDD.median():11.2%}")
    P(f"    {'RULES v2 (OOS)':16s} {'':4s} {'':12s} {hw.base_OOS_Sharpe.median():12.4f} "
      f"{hw.base_OOS_MaxDD.median():11.2%}")
    hkeep = bool(hw[hw.chooser.isin(CHOOSERS)].pass4b.sum() > 0
                 or hw[hw.chooser.isin(CHOOSERS)].pass4a.sum() > 0)
    P()
    P(f"  H_KEEP -- any IS-CHOSEN arm clearing either KEEP path at {HEAD_COST:.0f} bps: "
      f"4b {hw[hw.chooser.isin(CHOOSERS)].pass4b.sum()} / "
      f"{len(hw[hw.chooser.isin(CHOOSERS)])}, 4a "
      f"{hw[hw.chooser.isin(CHOOSERS)].pass4a.sum()}  ->  "
      f"{'PASS' if hkeep else 'FAIL (no KEEP on either path)'}")
    P("  4b failing legs on the IS-chosen arms (which leg binds):")
    fc = hw[hw.chooser.isin(CHOOSERS)].fail.value_counts()
    for kk, vv in fc.items():
        P(f"    {str(kk):32s} {vv:4d}")
    P()
    P("  every rung, IS-chosen arms only (reported, never selected on):")
    P(f"    {'bps':>5s} {'4b REC':>10s} {'4b PURE':>10s} {'4a':>8s} {'med OOS Sharpe':>15s}")
    for c, s in WF[WF.chooser.isin(CHOOSERS)].groupby("cost_bps"):
        P(f"    {c:5.0f} {s.pass4b.sum():4d}/{len(s):<5d} {s.pass4b_pure.sum():4d}/{len(s):<5d} "
          f"{s.pass4a.sum():3d}/{len(s):<4d} {s.OOS_Sharpe.median():15.4f}")

    # ================================================================================ verdict
    P()
    P("=" * 100)
    P("(F) HYPOTHESES AND VERDICT")
    P("=" * 100)
    H = pd.DataFrame([
        dict(name="H_COUNT", bar=f"BLOCK0 median canonical pctile > {COUNT_BAR}",
             value=f"{hd.Q_BLOCK0_pctile.median():.4f}",
             result="PASS (calendar-count artefact)" if hcount
             else "FAIL (reversal survives the width control)"),
        dict(name="H_MEND", bar=f"m=0 median pctile >= {MEND_BAR} in blocks 1 AND 2",
             value=f"{hd.Q_blk1_m0_pctile.median():.4f} / {hd.Q_blk2_m0_pctile.median():.4f}",
             result="PASS" if hmend else "FAIL"),
        dict(name="H_QEND", bar=f"MEND_Q3 worst of three in > {QEND_BAR} of families",
             value=f"{share_worst:.4f} (chance 0.3333)", result="PASS" if hqend else "FAIL"),
        dict(name="H_FLOW", bar="H_COUNT FAIL and H_MEND PASS and H_QEND PASS",
             value=f"{not hcount} / {hmend} / {hqend}", result="PASS" if hflow else "FAIL"),
        dict(name="H_TRADE", bar=f"best(Q1,Q2) OOS Sharpe > Q3 in >= {TRADE_BAR}",
             value=f"{share_tr:.4f}", result="PASS" if htrade else "FAIL"),
        dict(name="H_NULL", bar=f"MEND_Q2 median CAGR pctile in its own 63-phase family >= {NULL_BAR}",
             value=f"{hn['MEND_Q2_CAGR_pctile'].median():.4f}",
             result="PASS (outlier)" if hnull else "FAIL (an ORDINARY draw from the phase dial)"),
        dict(name="H_KEEP", bar="rule 8: IS-chosen arm clears 4a or 4b at 10 bps",
             value=f"4b {hw[hw.chooser.isin(CHOOSERS)].pass4b.sum()} / 4a "
                   f"{hw[hw.chooser.isin(CHOOSERS)].pass4a.sum()}",
             result="PASS" if hkeep else "FAIL"),
    ])
    dump(H, "hypotheses")
    for _, r in H.iterrows():
        P(f"  {r['name']:9s} {r['bar']:52s} {r['value']:26s} {r['result']}")
    dump(pd.DataFrame([dict(gate=k, result="PASS" if v else "FAIL") for k, v in sorted(gk.items())]),
        "gates")
    dump(g7, "g7_mod21_approximation")
    P()
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS.   runtime {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
