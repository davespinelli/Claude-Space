#!/usr/bin/env python3
"""
IDEA 938 -- is-U56-M-CORE-TOP20-s-2.09pp-CAGR-edge-over-its-WEEKLY-twin-a-REBALANCE-OFFSET-artefact
    (lane B, 2026-09-15)
====================================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 926 (lane B run) found the same rule, gross and gate reads 14.69% / 1.203 / -19.51%
  MONTHLY against 12.60% / 1.088 / -18.31% WEEKLY at 45% of the turnover, and that the monthly
  cell's gross-matched null base rate is 40.5% against the weekly cell's 0.0%.  Price the
  monthly book across all 4 within-month rebalance OFFSETS and all 21 trading-day PHASES in the
  sense of ideas 922/925, and report whether the 2.09 pp survives its own offset spread.
  Max 2 params (offset grid, cost rung).

WHY IT MATTERS FOR CAPITAL
--------------------------
  U56 M/CORE/TOP20 is the record's highest-CAGR, highest-Sharpe, both-windows-4b-clearing book.
  It is PARKED on its own null (40.5% base rate), but the +2.09 pp CAGR it shows over its weekly
  twin is the ONLY reason a reader would prefer the monthly convention at all -- it is the number
  that would justify trading the book monthly with real money.  "Rebalance on the last trading
  day of the month" is a FREE PARAMETER that nobody in this record ever tuned or reported: it was
  inherited from engine.rebalance_mask.  If the +2.09 pp is inside the spread that free parameter
  buys, then the monthly convention is not a cheaper way to run TOP20, it is a luckier one, and
  every M-vs-W comparison in the record is reading a phase draw as a cadence fact.

THE MECHANISM UNDER TEST, STATED SO IT CAN FAIL
-----------------------------------------------
  H_ARTEFACT  the +2.09 pp is bought by WHICH DAY the monthly book trades on.  Predictions:
              the canonical month-end sits in the top decile of its own 21-phase CAGR
              distribution, and/or the monthly-minus-weekly gap goes NEGATIVE at one or more
              of the 25 monthly offsets, and/or the phase spread is wider than the gap.
  H_REAL      the gap is a CADENCE fact (slower trading, less cost drag, less whipsaw).
              Prediction: the gap is positive at EVERY monthly offset, the canonical is an
              ordinary member of its own family, the median gap is at least half the published
              2.09 pp, and the phase spread is narrower than the gap it is supposed to explain.
  The two are separated by the OFFSET x COST grid below, read against the WEEKLY book's OWN
  5-phase distribution so the comparison is distribution-to-distribution, not point-to-point.

DESIGN
------
  TUNED (2, and only 2 -- every grid point is reported, none is selected for a headline)
    1. OFFSET GRID  three families, 30 offsets in total, all published:
         DOM d  (21)  rebalance d trading days BEFORE the last trading day of each calendar
                      month, d = 0..20.  d = 0 IS the canonical convention (G0 asserts the mask
                      equals engine.rebalance_mask(idx,'M') bit for bit), so the grid NESTS the
                      published book rather than replacing it.  Months with <= d trading days
                      clip to the month's first trading day; the clip count is reported per
                      offset (G4), never hidden.
         4W o   (4)   the queue's "4 within-month offsets": rebalance every 4th W-end, phase
                      o = 0..3.  Calendar-free, so it separates "monthly cadence" from "month
                      boundary".  13.0 rebalances/yr against calendar-monthly's 12.0.
         DOW d  (5)   the WEEKLY twin's own phase family, d trading days before each week's
                      last trading day, d = 0..4.  d = 0 is the published weekly twin.  Without
                      this the monthly spread would be compared against a single weekly point.
    2. COST RUNG    0 / 5 / 10 / 25 bps.  10 bps is PROTOCOL rule 2 and carries every verdict;
                    0 isolates the gross-return channel from the cost channel; 5 and 25 bracket
                    the rung so the gap is read as a curve.
  NOT TUNED -- copied from idea 926 / the 2026-09-04 incumbent without change
    BOOK        TOP20: score(vol_scale=False) ranked inside the gate, rank <= 20, weight g/20.
    CLAIM SET   CORE = gross 0.75 (the record's modal convention).  EXT (g=1.00) is run as a
                labelled replication only; no verdict is taken from it.
    GATE        above the 200d MA and vol20 < 0.60.  Warm-up 260 rows.
    PANELS      U56 (BINDING -- the book's own panel) and B136 (labelled replication).
    WINDOWS     IS <= 2016-12-31, OOS >= 2017-01-01 (PROTOCOL rule 8).
    COMPARANDS  SPY buy-and-hold and RULES v2 (live) on the same tape (PROTOCOL rule 3).

  STATISTIC, NAMED WITH ITS n (idea 564's standing request).  The headline is a DIFFERENCE OF
  CAGRs in percentage points, n = 21 DOM phases (+4 4W offsets) against n = 5 DOW phases.  With
  n that small no p-value is claimed: the run reports the FULL support of both distributions
  (min, median, max, every point in the .offsets.csv), the canonical's rank inside its own
  family, and the overlap count.  A rank over 21 points has resolution 1/21 = 4.8% and that is
  stated wherever a percentile is printed.

PRE-REGISTERED BARS (printed before any new number is read; the verdict is mechanical)
---------------------------------------------------------------------------------------
  B1 SIGN        min over the 25 monthly offsets of (CAGR - weekly canonical CAGR) > 0
  B2 EXTREMITY   percentile of the canonical month-end CAGR inside its own 21 DOM phases <= 0.90
  B3 MAGNITUDE   median over the 25 monthly offsets of the gap >= 1.045 pp (half the published
                 2.09 pp)
  B4 SPREAD      DOM phase spread (max - min CAGR over the 21 phases) < 2.09 pp
  B5 DURABILITY  the 4b PASS holds at >= 90% of the 25 monthly offsets, on the FULL sample and
                 on the rule-8 OOS window separately
  VERDICT RULE   H_REAL requires B1, B2, B3 and B4 to ALL pass.  Any failure of B1 or B2 is
                 scored H_ARTEFACT.  B5 is reported for the capital decision and moves no
                 verdict on the mechanism.  All bars are at 10 bps, PROTOCOL's own rung.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G0  offset_mask(.,'M',0) == engine.rebalance_mask(.,'M') and the same on 'W'   bar 0 rows
  G1  ctx.run == engine.backtest @10 bps on W and M                              bar 1e-12
  G2  band_book(0.03,0.75) == baseline.rules_v2_weights                          bar 0.0
  G3  idea 926's two published headlines re-derived from this file's code path:
        U56 M/CORE/TOP20 @10bps 14.69% / 1.203 / -19.51%
        U56 W/CORE/TOP20 @10bps 12.60% / 1.088 / -18.31%                         bar 5e-3
  G3b the same run's published comparands: SPY 15.13% / 0.8845 / -33.72%,
        RULES v2 Sharpe 1.2013 / MaxDD -12.05% on U56                            bar 5e-3
  G4  OFFSET FAIRNESS: rebalances/yr and clipped-month count printed for all 30 offsets; no
      DOM offset may trade fewer than 11.5 or more than 12.5 times a year          bar as stated
  G5  DETERMINISM: the canonical monthly stream re-derived twice                  bar 0.0
  G6  baseline.compare() agrees with this file's fast runner on both canonical books (the
      PROTOCOL rule-3 code path, run end to end)                                  bar 5e-3

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, and idea 924 showed
  U56's `megacap` group is the 2026 top-20 held from 2009.  Every CAGR and Sharpe LEVEL below
  is therefore optimistic and none of them is a capital claim on its own.  Direction for THIS
  run: the offset contrast, the phase spread and the M-minus-W gap are SAME-TAPE, same-universe,
  same-weights comparisons that differ only in WHICH DAY the identical book trades, so they are
  unaffected by the panel's composition.  The 4b LEVELS are against SPY, which is not
  survivorship-inflated, so they are NOT protected by that argument and are reported as
  bounded, not as clean.
"""
import os, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score, compare   # noqa: E402
from engine import backtest, rebalance_mask                                        # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0.0, 5.0, 10.0, 25.0]                 # TUNED axis 2
HEAD_COST = 10.0                               # PROTOCOL rule 2 -- carries every verdict
DOM_N, NW_N, DOW_N = 21, 4, 5                  # TUNED axis 1 (three families, 30 offsets)
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
BINDING_PANEL, BINDING_SET, BINDING_BOOK = "U56", "CORE", "TOP20"
PUBLISHED_GAP_PP = 2.09                        # idea 926's committed number, in pp
B3_BAR = PUBLISHED_GAP_PP / 2.0                # 1.045 pp
B2_BAR, B5_BAR = 0.90, 0.90
PUB_M = dict(CAGR=0.1469, Sharpe=1.203, MaxDD=-0.1951)
PUB_W = dict(CAGR=0.1260, Sharpe=1.088, MaxDD=-0.1831)
PUB_SPY = dict(CAGR=0.1513, Sharpe=0.8845, MaxDD=-0.3372)
PUB_V2 = dict(Sharpe=1.2013, MaxDD=-0.1205)

SMOKE = bool(int(os.environ.get("IDEA938_SMOKE", "0")))
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# the offset machinery -- the only thing this run adds to idea 926's code path
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period (per in {'W','M'}).

    d = 0 reproduces engine.rebalance_mask(idx, per) exactly (G0), so the grid NESTS the
    published convention.  A period with <= d trading days clips to its FIRST trading day;
    the number of clipped periods is reported per offset (G4)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def nweek_mask(idx, n, o):
    """Every n-th W-end, phase o.  Calendar-free: separates 'monthly cadence' from 'month end'."""
    w = np.flatnonzero(rebalance_mask(idx, "W").values)
    keep = w[o::n]
    out = pd.Series(False, index=idx)
    out.iloc[keep] = True
    return out, 0


def offset_grid():
    """The 30 published offsets.  family, label, mask-builder.  Order is the report order."""
    g = []
    for d in range(DOM_N):
        g.append(("DOM", f"DOM{d:02d}", ("M", d)))
    for o in range(NW_N):
        g.append(("4W", f"4W{o}", ("NW", o)))
    for d in range(DOW_N):
        g.append(("DOW", f"DOW{d}", ("W", d)))
    return g


def build_mask(idx, spec):
    kind, k = spec
    if kind == "NW":
        return nweek_mask(idx, NW_N, k)
    return offset_mask(idx, kind, k)


# ==========================================================================================
# fast runner -- byte-identical to idea 926's Ctx except that the mask is passed in
# ==========================================================================================
class Ctx:
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


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252)
    dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd,
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, oos_s, ms, spy_oos):
    return dict(L1_H1=m["H1"] > ms["H1"], L2_H2=m["H2"] > ms["H2"], L3_OOS=oos_s > spy_oos,
                L4_DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                L5_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def pass4b(m, oos_s, ms, spy_oos):
    return bool(all(legs4b(m, oos_s, ms, spy_oos).values()))


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


def failstr(m, oos_s, ms, spy_oos):
    f = [k for k, v in legs4b(m, oos_s, ms, spy_oos).items() if not v]
    return "+".join(f) if f else "-"


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def top20_book(px, g, k=20):
    """The 2026-09-04 KEEP-4b incumbent's construction, copied from idea 926 unchanged."""
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


# ==========================================================================================
def panel_context(px, mask):
    ctx = Ctx(px, mask)
    idx = px.index
    i0 = WARM
    oos = np.asarray(idx >= pd.Timestamp(OOS_START))[i0:]
    is_ = np.asarray(idx <= pd.Timestamp(IS_END))[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).values[i0:]
    return dict(ctx=ctx, i0=i0, oos=oos, is_=is_, spy=mets(spy), spy_oos=mets(spy[oos]),
                spy_is=mets(spy[is_]))


def score_stream(gr, tn, pc, c):
    i0, oos, is_ = pc["i0"], pc["oos"], pc["is_"]
    r = (gr - tn * c / 1e4)[i0:]
    return mets(r), mets(r[oos]), mets(r[is_])


def pct_rank(x, arr):
    """Fraction of the family at or below x.  Resolution 1/len(arr); always printed with n."""
    arr = np.asarray(arr, float)
    return float((arr <= x).sum() / len(arr))


# ==========================================================================================
def gates_pre(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok, px = {}, panels[BINDING_PANEL]

    bad = 0
    for per in ("M", "W"):
        m0, _ = offset_mask(px.index, per, 0)
        bad += int((m0.values != rebalance_mask(px.index, per).values).sum())
    ok["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on M and W : {bad} differing rows  "
      f"{'PASS' if ok['G0'] else 'FAIL'}")

    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    ok["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights                 : {g2:.3e}  "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    g1 = 0.0
    for per in ("W", "M"):
        m0, _ = offset_mask(px.index, per, 0)
        ctx = Ctx(px, m0)
        gr, tn = ctx.run(ctx.shift(w))
        fast = pd.Series(gr - tn * 10.0 / 1e4, index=px.index)
        slow = backtest(px, w, cost_bps=10.0, freq=per)["returns"]
        j = px.index[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
    ok["G1"] = g1 < 1e-12
    P(f"  G1 ctx.run == engine.backtest @10 bps, worse of W and M     : {g1:.3e}  "
      f"{'PASS' if ok['G1'] else 'FAIL'}")

    bk = top20_book(px, 0.75)
    got = {}
    for per, pub, lbl in (("M", PUB_M, "M/CORE/TOP20"), ("W", PUB_W, "W/CORE/TOP20")):
        m0, _ = offset_mask(px.index, per, 0)
        ctx = Ctx(px, m0)
        gr, tn = ctx.run(ctx.shift(bk))
        m = mets((gr - tn * HEAD_COST / 1e4)[WARM:])
        got[per] = m
        d = max(abs(m[k] - v) for k, v in pub.items())
        ok[f"G3_{per}"] = d < 5e-3
        P(f"  G3 idea 926 {lbl:14s}: got {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / "
          f"{m['MaxDD']:7.2%}  published {pub['CAGR']:.2%} / {pub['Sharpe']:.3f} / "
          f"{pub['MaxDD']:.2%}  max|d| {d:.3e}  {'PASS' if d < 5e-3 else 'FAIL'}")
    P(f"     -> the object under test: published gap {PUBLISHED_GAP_PP:.2f} pp, "
      f"re-derived here {(got['M']['CAGR'] - got['W']['CAGR']) * 100:.2f} pp")

    m0, _ = offset_mask(px.index, "M", 0)
    pc = panel_context(px, m0)
    ds = max(abs(pc["spy"][k] - v) for k, v in PUB_SPY.items())
    ctx = Ctx(px, offset_mask(px.index, "W", 0)[0])
    gr, tn = ctx.run(ctx.shift(rules_v2_weights(px, BAND0, 0.75)))
    mv2 = mets((gr - tn * HEAD_COST / 1e4)[WARM:])
    dv = max(abs(mv2[k] - v) for k, v in PUB_V2.items())
    ok["G3b"] = ds < 5e-3 and dv < 5e-3
    P(f"  G3b comparands: SPY {pc['spy']['CAGR']:.2%}/{pc['spy']['Sharpe']:.4f}/"
      f"{pc['spy']['MaxDD']:.2%} (|d| {ds:.3e}); RULES v2 W@10bps "
      f"{mv2['Sharpe']:.4f}/{mv2['MaxDD']:.2%} (|d| {dv:.3e})  "
      f"{'PASS' if ok['G3b'] else 'FAIL'}")

    a, _ = Ctx(px, m0).run(Ctx(px, m0).shift(bk))
    b, _ = Ctx(px, m0).run(Ctx(px, m0).shift(bk))
    g5 = float(np.abs(a - b).max())
    ok["G5"] = g5 == 0.0
    P(f"  G5 determinism (canonical monthly re-derived)                : {g5:.3e}  "
      f"{'PASS' if ok['G5'] else 'FAIL'}")
    P("  G4 (offset fairness) and G6 (baseline.compare agreement) are evaluated in sections "
      "(B) and (F).")
    return ok


# ==========================================================================================
def main():
    t0 = time.time()
    P("IDEA 938  is-U56-M-CORE-TOP20-s-2.09pp-CAGR-edge-a-REBALANCE-OFFSET-artefact  (lane B)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   offsets: {DOM_N} DOM + {NW_N} 4W + "
      f"{DOW_N} DOW = {DOM_N + NW_N + DOW_N}   costs {COSTS} bps   "
      f"claim sets {list(CLAIM_SETS)}")
    P("the two tuned axes are OFFSET GRID and COST RUNG; every grid point is reported, "
      "none chosen")
    P()
    P("PRE-REGISTERED BARS (all at 10 bps, on U56/CORE/TOP20, stated before any number is read)")
    P(f"  B1 SIGN       min over the 25 monthly offsets of (CAGR - weekly canonical) > 0")
    P(f"  B2 EXTREMITY  canonical month-end percentile inside its own {DOM_N} DOM phases "
      f"<= {B2_BAR:.2f}")
    P(f"  B3 MAGNITUDE  median monthly gap >= {B3_BAR:.3f} pp (half the published "
      f"{PUBLISHED_GAP_PP:.2f} pp)")
    P(f"  B4 SPREAD     DOM phase spread (max-min CAGR) < {PUBLISHED_GAP_PP:.2f} pp")
    P(f"  B5 DURABILITY 4b PASS at >= {B5_BAR:.0%} of the 25 monthly offsets, FULL and OOS "
      f"separately")
    P("  VERDICT       H_REAL requires B1+B2+B3+B4; failure of B1 or B2 is H_ARTEFACT. "
      "B5 informs capital, moves no mechanism verdict.")
    P()

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
    gk = gates_pre(panels)
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(B) THE OFFSET GRID ITSELF (G4) -- fairness before performance")
    P("=" * 100)
    px = panels[BINDING_PANEL]
    GRID = offset_grid()
    yrs = (len(px.index) - WARM) / 252.0
    P(f"     {'offset':8s} {'family':7s} {'reb/yr':>8s} {'clipped':>8s}   (U56 tape, "
      f"{len(px.index)} rows, {yrs:.1f} yr after warm-up)")
    GRIDROWS, g4_bad = [], 0
    for fam, lab, spec in GRID:
        m, clipped = build_mask(px.index, spec)
        n = int(m.values[WARM:].sum())
        rpy = n / yrs
        if fam == "DOM" and not (11.5 <= rpy <= 12.5):
            g4_bad += 1
        GRIDROWS.append(dict(family=fam, offset=lab, reb_per_yr=rpy, clipped_periods=clipped,
                             n_rebalances=n))
        P(f"     {lab:8s} {fam:7s} {rpy:8.2f} {clipped:8d}")
    gk["G4"] = g4_bad == 0
    P(f"  G4 every DOM offset trades 11.5-12.5 times a year: {g4_bad} violations  "
      f"{'PASS' if gk['G4'] else 'FAIL'}")
    dump(pd.DataFrame(GRIDROWS), "grid")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) EVERY GRID POINT -- 30 offsets x 4 rungs x 2 claim sets x 2 panels")
    P("=" * 100)
    ROWS = []
    for pn, ppx in panels.items():
        for cs, g in CLAIM_SETS.items():
            bk = top20_book(ppx, g)
            v2 = rules_v2_weights(ppx, BAND0, 0.75)
            for fam, lab, spec in GRID:
                m, clipped = build_mask(ppx.index, spec)
                pc = panel_context(ppx, m)
                wt = pc["ctx"].shift(bk)
                gr, tn = pc["ctx"].run(wt)
                grv, tnv = pc["ctx"].run(pc["ctx"].shift(v2))
                turn_yr = float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))
                for c in COSTS:
                    mm, mo, mi = score_stream(gr, tn, pc, c)
                    mb, _, _ = score_stream(grv, tnv, pc, c)
                    ROWS.append(dict(
                        panel=pn, claim_set=cs, family=fam, offset=lab, cost=c,
                        turn_yr=turn_yr, drag_bp_yr=turn_yr * c,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                        H1=mm["H1"], H2=mm["H2"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        pass4b=pass4b(mm, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                        pass4a=pass4a(mm, mb),
                        fail4b=failstr(mm, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                        spy_CAGR=pc["spy"]["CAGR"], spy_Sharpe=pc["spy"]["Sharpe"],
                        spy_MaxDD=pc["spy"]["MaxDD"], spy_oos_Sharpe=pc["spy_oos"]["Sharpe"],
                        spy_oos_CAGR=pc["spy_oos"]["CAGR"],
                        v2_Sharpe=mb["Sharpe"], v2_MaxDD=mb["MaxDD"]))
    off = pd.DataFrame(ROWS)
    dump(off, "offsets")

    B = off[(off.panel == BINDING_PANEL) & (off.claim_set == BINDING_SET)]
    for c in COSTS:
        s = B[B.cost == c]
        dom = s[s.family == "DOM"]
        nw = s[s.family == "4W"]
        dow = s[s.family == "DOW"]
        P(f"  @{c:5.1f} bps  CAGR   DOM[{len(dom)}] {dom.CAGR.min():.2%} .. "
          f"{dom.CAGR.median():.2%} .. {dom.CAGR.max():.2%}   "
          f"4W[{len(nw)}] {nw.CAGR.min():.2%} .. {nw.CAGR.max():.2%}   "
          f"DOW[{len(dow)}] {dow.CAGR.min():.2%} .. {dow.CAGR.max():.2%}")
    P()
    P(f"  the {DOM_N} DOM phases at {HEAD_COST:.0f} bps, in full (d=0 is the published book):")
    s = B[(B.cost == HEAD_COST) & (B.family == "DOM")].sort_values("offset")
    P(f"     {'phase':7s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
      f"{'turn/yr':>8s} {'OOS CAGR':>9s} {'OOS Sh':>7s}  4b  4a  fail")
    for _, r in s.iterrows():
        P(f"     {r.offset:7s} {r.CAGR:8.2%} {r.Sharpe:8.3f} {r.MaxDD:8.2%} {r.H1:7.3f} "
          f"{r.H2:7.3f} {r.turn_yr:8.2f} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f}  "
          f"{'Y' if r.pass4b else 'n'}   {'Y' if r.pass4a else 'n'}  {r.fail4b}")
    P()
    P(f"  the {NW_N} 4W offsets and the {DOW_N} DOW phases at {HEAD_COST:.0f} bps:")
    s2 = B[(B.cost == HEAD_COST) & (B.family != "DOM")].sort_values(["family", "offset"])
    for _, r in s2.iterrows():
        P(f"     {r.offset:7s} {r.CAGR:8.2%} {r.Sharpe:8.3f} {r.MaxDD:8.2%} {r.H1:7.3f} "
          f"{r.H2:7.3f} {r.turn_yr:8.2f} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f}  "
          f"{'Y' if r.pass4b else 'n'}   {'Y' if r.pass4a else 'n'}  {r.fail4b}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE OBJECT UNDER TEST -- does 2.09 pp survive its own offset spread?")
    P("=" * 100)
    GAPS = []
    for pn in panels:
        for cs in CLAIM_SETS:
            for c in COSTS:
                s = off[(off.panel == pn) & (off.claim_set == cs) & (off.cost == c)]
                dom = s[s.family == "DOM"].set_index("offset")
                nw = s[s.family == "4W"]
                dow = s[s.family == "DOW"].set_index("offset")
                mon = pd.concat([dom.CAGR, nw.set_index("offset").CAGR])
                wcan = float(dow.loc["DOW0", "CAGR"])
                mcan = float(dom.loc["DOM00", "CAGR"])
                gaps = (mon - wcan) * 100.0
                gaps_med = (mon.median() - dow.CAGR.median()) * 100.0
                GAPS.append(dict(
                    panel=pn, claim_set=cs, cost=c,
                    canon_M_CAGR=mcan, canon_W_CAGR=wcan,
                    canon_gap_pp=(mcan - wcan) * 100.0,
                    gap_min_pp=float(gaps.min()), gap_med_pp=float(gaps.median()),
                    gap_max_pp=float(gaps.max()),
                    n_monthly_offsets=int(len(mon)),
                    n_gap_negative=int((gaps <= 0).sum()),
                    dom_spread_pp=float((dom.CAGR.max() - dom.CAGR.min()) * 100.0),
                    dow_spread_pp=float((dow.CAGR.max() - dow.CAGR.min()) * 100.0),
                    canon_M_pctile=pct_rank(mcan, dom.CAGR.values),
                    canon_W_pctile=pct_rank(wcan, dow.CAGR.values),
                    medians_gap_pp=gaps_med,
                    n_monthly_below_best_weekly=int((mon < dow.CAGR.max()).sum()),
                    overlap=bool(mon.min() < dow.CAGR.max()),
                    sharpe_canon_gap=mcan * 0 + float(dom.loc["DOM00", "Sharpe"] -
                                                      dow.loc["DOW0", "Sharpe"]),
                    sharpe_gap_min=float((pd.concat([dom.Sharpe,
                                                     nw.set_index("offset").Sharpe])
                                          - float(dow.loc["DOW0", "Sharpe"])).min()),
                    dom_sharpe_spread=float(dom.Sharpe.max() - dom.Sharpe.min()),
                    pass4b_frac_full=float(pd.concat([dom.pass4b,
                                                      nw.set_index("offset").pass4b]).mean()),
                ))
    gaps_df = pd.DataFrame(GAPS)
    dump(gaps_df, "gaps")
    P(f"  U56/CORE, the binding cell -- gap = monthly offset CAGR minus the WEEKLY CANONICAL:")
    P(f"     {'rung':>6s} {'canon gap':>10s} {'gap min':>9s} {'gap med':>9s} {'gap max':>9s} "
      f"{'neg':>4s} {'DOM spread':>11s} {'DOW spread':>11s} {'canon pctile':>13s}")
    for _, r in gaps_df[(gaps_df.panel == BINDING_PANEL) &
                        (gaps_df.claim_set == BINDING_SET)].iterrows():
        P(f"     {r.cost:6.1f} {r.canon_gap_pp:10.2f} {r.gap_min_pp:9.2f} "
          f"{r.gap_med_pp:9.2f} {r.gap_max_pp:9.2f} {r.n_gap_negative:4d} "
          f"{r.dom_spread_pp:11.2f} {r.dow_spread_pp:11.2f} {r.canon_M_pctile:13.3f}")
    P("     (all figures in percentage points of CAGR; 'neg' counts monthly offsets whose gap "
      "over the weekly canonical is <= 0, out of 25; canon pctile has resolution 1/21 = 0.048)")
    P()
    P("  labelled replications (no verdict is taken from them):")
    for _, r in gaps_df[(gaps_df.cost == HEAD_COST) &
                        ~((gaps_df.panel == BINDING_PANEL) &
                          (gaps_df.claim_set == BINDING_SET))].iterrows():
        P(f"     {r.panel}/{r.claim_set:5s} @10bps  canon gap {r.canon_gap_pp:6.2f} pp   "
          f"min {r.gap_min_pp:6.2f}   med {r.gap_med_pp:6.2f}   max {r.gap_max_pp:6.2f}   "
          f"neg {r.n_gap_negative:2d}/25   DOM spread {r.dom_spread_pp:5.2f} pp   "
          f"canon pctile {r.canon_M_pctile:.3f}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) THE PRE-REGISTERED BARS, SCORED MECHANICALLY (U56/CORE @10 bps)")
    P("=" * 100)
    r = gaps_df[(gaps_df.panel == BINDING_PANEL) & (gaps_df.claim_set == BINDING_SET) &
                (gaps_df.cost == HEAD_COST)].iloc[0]
    s10 = B[B.cost == HEAD_COST]
    mon10 = s10[s10.family != "DOW"]
    b5_full = float(mon10.pass4b.mean())
    spy_oos_sh = float(s10.spy_oos_Sharpe.iloc[0])
    b5_oos = float((mon10.OOS_Sharpe > spy_oos_sh).mean())
    HYP = []
    def bar(name, val, ok, detail):
        HYP.append(dict(bar=name, value=val, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"  {name:14s} {'PASS' if ok else 'FAIL'}   {detail}")
        return ok
    b1 = bar("B1 SIGN", r.gap_min_pp, r.gap_min_pp > 0,
             f"min gap over 25 monthly offsets = {r.gap_min_pp:+.2f} pp "
             f"({r.n_gap_negative} of 25 are <= 0); bar > 0")
    b2 = bar("B2 EXTREMITY", r.canon_M_pctile, r.canon_M_pctile <= B2_BAR,
             f"canonical month-end is at percentile {r.canon_M_pctile:.3f} of its own "
             f"{DOM_N} DOM phases (resolution 0.048); bar <= {B2_BAR:.2f}")
    b3 = bar("B3 MAGNITUDE", r.gap_med_pp, r.gap_med_pp >= B3_BAR,
             f"median monthly gap = {r.gap_med_pp:+.2f} pp; bar >= {B3_BAR:.3f} pp")
    b4 = bar("B4 SPREAD", r.dom_spread_pp, r.dom_spread_pp < PUBLISHED_GAP_PP,
             f"DOM phase spread = {r.dom_spread_pp:.2f} pp against the "
             f"{PUBLISHED_GAP_PP:.2f} pp it must explain "
             f"({r.dom_spread_pp / PUBLISHED_GAP_PP:.2f}x); bar < {PUBLISHED_GAP_PP:.2f}")
    b5 = bar("B5 DURABILITY", b5_full, b5_full >= B5_BAR and b5_oos >= B5_BAR,
             f"4b PASS on the FULL sample at {b5_full:.1%} of 25 monthly offsets; the OOS "
             f"Sharpe leg alone clears SPY at {b5_oos:.1%}; bar >= {B5_BAR:.0%} on both")
    mech = "H_REAL" if (b1 and b2 and b3 and b4) else "H_ARTEFACT"
    HYP.append(dict(bar="MECHANISM", value=np.nan, verdict=mech,
                    detail="H_REAL requires B1+B2+B3+B4; B1 or B2 failing forces H_ARTEFACT"))
    P()
    P(f"  MECHANISM VERDICT: {mech}")
    P()
    P("  the same bars at the other three rungs (reported, not used for the verdict):")
    for _, q in gaps_df[(gaps_df.panel == BINDING_PANEL) &
                        (gaps_df.claim_set == BINDING_SET) &
                        (gaps_df.cost != HEAD_COST)].iterrows():
        P(f"     @{q.cost:5.1f} bps  B1 {'PASS' if q.gap_min_pp > 0 else 'FAIL'} "
          f"({q.gap_min_pp:+.2f} pp)   B2 {'PASS' if q.canon_M_pctile <= B2_BAR else 'FAIL'} "
          f"({q.canon_M_pctile:.3f})   B3 "
          f"{'PASS' if q.gap_med_pp >= B3_BAR else 'FAIL'} ({q.gap_med_pp:+.2f} pp)   "
          f"B4 {'PASS' if q.dom_spread_pp < PUBLISHED_GAP_PP else 'FAIL'} "
          f"({q.dom_spread_pp:.2f} pp)")
    dump(pd.DataFrame(HYP), "hypotheses")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) PROTOCOL RULE 8 -- WALK-FORWARD: the offset chosen on 2009-2016 ONLY, 2017-2026 "
      "read once")
    P("=" * 100)
    WF = []
    for pn in panels:
        for cs in CLAIM_SETS:
            for c in COSTS:
                s = off[(off.panel == pn) & (off.claim_set == cs) & (off.cost == c)]
                mon = s[s.family != "DOW"]
                allo = s
                spy_o = dict(CAGR=float(s.spy_oos_CAGR.iloc[0]),
                             Sharpe=float(s.spy_oos_Sharpe.iloc[0]))
                choosers = {
                    "CH_CANON": s[s.offset == "DOM00"].iloc[0],
                    "CH_IS_SHARPE_DOM": s[s.family == "DOM"].sort_values(
                        "IS_Sharpe", ascending=False).iloc[0],
                    "CH_IS_SHARPE_MONTHLY": mon.sort_values(
                        "IS_Sharpe", ascending=False).iloc[0],
                    "CH_IS_CAGR_MONTHLY": mon.sort_values(
                        "IS_CAGR", ascending=False).iloc[0],
                    "CH_IS_SHARPE_ANYFAM": allo.sort_values(
                        "IS_Sharpe", ascending=False).iloc[0],
                    "CH_WEEKLY_CANON": s[s.offset == "DOW0"].iloc[0],
                }
                oos_sorted = mon.OOS_Sharpe.sort_values(ascending=False).values
                for nm, pick in choosers.items():
                    rank = int((oos_sorted > pick.OOS_Sharpe).sum() + 1)
                    WF.append(dict(panel=pn, claim_set=cs, cost=c, chooser=nm,
                                   picked=pick.offset, family=pick.family,
                                   IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                   OOS_MaxDD=pick.OOS_MaxDD,
                                   oos_rank_among_monthly=rank, n_monthly=int(len(mon)),
                                   spy_oos_CAGR=spy_o["CAGR"],
                                   spy_oos_Sharpe=spy_o["Sharpe"],
                                   beats_spy_oos=bool(pick.OOS_Sharpe > spy_o["Sharpe"]),
                                   pass4b=bool(pick.pass4b), pass4a=bool(pick.pass4a)))
                # the offset-blind investor: the mean over the whole monthly family
                WF.append(dict(panel=pn, claim_set=cs, cost=c, chooser="MEAN_ALL_MONTHLY",
                               picked="(mean of 25)", family="MON",
                               IS_Sharpe=float(mon.IS_Sharpe.mean()),
                               IS_CAGR=float(mon.IS_CAGR.mean()),
                               OOS_CAGR=float(mon.OOS_CAGR.mean()),
                               OOS_Sharpe=float(mon.OOS_Sharpe.mean()),
                               OOS_MaxDD=float(mon.OOS_MaxDD.mean()),
                               oos_rank_among_monthly=-1, n_monthly=int(len(mon)),
                               spy_oos_CAGR=spy_o["CAGR"], spy_oos_Sharpe=spy_o["Sharpe"],
                               beats_spy_oos=bool(mon.OOS_Sharpe.mean() > spy_o["Sharpe"]),
                               pass4b=bool(mon.pass4b.mean() >= 0.5),
                               pass4a=bool(mon.pass4a.mean() >= 0.5)))
    wf = pd.DataFrame(WF)
    dump(wf, "walkforward")
    sub = wf[(wf.panel == BINDING_PANEL) & (wf.claim_set == BINDING_SET) &
             (wf.cost == HEAD_COST)]
    P(f"  U56/CORE @{HEAD_COST:.0f} bps, IS = 2009..2016, OOS = 2017..2026 read once:")
    P(f"     {'chooser':22s} {'picked':11s} {'IS Sh':>7s} {'OOS CAGR':>9s} {'OOS Sh':>7s} "
      f"{'OOS MaxDD':>10s} {'OOS rank':>9s}  4b 4a")
    for _, q in sub.iterrows():
        rk = "n/a" if q.oos_rank_among_monthly < 0 else f"{q.oos_rank_among_monthly}/{q.n_monthly}"
        P(f"     {q.chooser:22s} {q.picked:11s} {q.IS_Sharpe:7.3f} {q.OOS_CAGR:9.2%} "
          f"{q.OOS_Sharpe:7.3f} {q.OOS_MaxDD:10.2%} {rk:>9s}  "
          f"{'Y' if q.pass4b else 'n'}  {'Y' if q.pass4a else 'n'}")
    sp = sub.iloc[0]
    P(f"     {'SPY (OOS)':22s} {'-':11s} {'-':>7s} {sp.spy_oos_CAGR:9.2%} "
      f"{sp.spy_oos_Sharpe:7.3f}")
    monall = off[(off.panel == BINDING_PANEL) & (off.claim_set == BINDING_SET) &
                 (off.cost == HEAD_COST) & (off.family != "DOW")]
    dow10 = off[(off.panel == BINDING_PANEL) & (off.claim_set == BINDING_SET) &
                (off.cost == HEAD_COST) & (off.family == "DOW")]
    P(f"     OOS CAGR support: monthly {monall.OOS_CAGR.min():.2%} .. "
      f"{monall.OOS_CAGR.median():.2%} .. {monall.OOS_CAGR.max():.2%} (n={len(monall)});  "
      f"weekly {dow10.OOS_CAGR.min():.2%} .. {dow10.OOS_CAGR.max():.2%} (n={len(dow10)})")
    P(f"     OOS gap (monthly offset minus weekly canonical): min "
      f"{(monall.OOS_CAGR.min() - float(dow10[dow10.offset == 'DOW0'].OOS_CAGR.iloc[0])) * 100:+.2f} pp"
      f"   med "
      f"{(monall.OOS_CAGR.median() - float(dow10[dow10.offset == 'DOW0'].OOS_CAGR.iloc[0])) * 100:+.2f} pp"
      f"   max "
      f"{(monall.OOS_CAGR.max() - float(dow10[dow10.offset == 'DOW0'].OOS_CAGR.iloc[0])) * 100:+.2f} pp")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(G) PROTOCOL RULE 3 CODE PATH -- baseline.compare() on both canonical books (G6)")
    P("=" * 100)
    cmpres = {}
    for per, lbl in (("M", "938 U56 CORE/TOP20 monthly canonical (DOM00)"),
                     ("W", "938 U56 CORE/TOP20 weekly canonical (DOW0)")):
        d = compare(lbl, lambda p: top20_book(p, 0.75), panels[BINDING_PANEL], freq=per,
                    cost_bps=HEAD_COST)
        cmpres[per] = d
        P(d["table"].to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"  compare() verdict (4a, vs RULES v2): {d['verdict']}")
        P(d["row"])
        P()
    g6 = 0.0
    for per, pub in (("M", PUB_M), ("W", PUB_W)):
        t = cmpres[per]["table"].iloc[0]
        fast = B[(B.cost == HEAD_COST) &
                 (B.offset == ("DOM00" if per == "M" else "DOW0"))].iloc[0]
        g6 = max(g6, abs(float(t["CAGR"]) - float(fast.CAGR)),
                 abs(float(t["Sharpe"]) - float(fast.Sharpe)))
    gk["G6"] = g6 < 5e-3
    P(f"  G6 baseline.compare() == this file's fast runner on both canonical books: "
      f"max|d| {g6:.3e}  {'PASS' if gk['G6'] else 'FAIL'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(H) SUMMARY")
    P("=" * 100)
    P(f"  gates: {sum(bool(v) for v in gk.values())} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failed'})")
    P(f"  MECHANISM: {mech}")
    P(f"  the published 2.09 pp: canonical gap re-derived {r.canon_gap_pp:+.2f} pp; "
      f"support over 25 monthly offsets [{r.gap_min_pp:+.2f}, {r.gap_max_pp:+.2f}] pp, "
      f"median {r.gap_med_pp:+.2f} pp, {r.n_gap_negative} of 25 <= 0")
    P(f"  the free parameter's own spread: DOM {r.dom_spread_pp:.2f} pp of CAGR and "
      f"{r.dom_sharpe_spread:.3f} of Sharpe over {DOM_N} phases; DOW {r.dow_spread_pp:.2f} pp "
      f"over {DOW_N}")
    P(f"  4b at 10 bps: {int(mon10.pass4b.sum())} of {len(mon10)} monthly offsets, "
      f"{int(s10[s10.family == 'DOW'].pass4b.sum())} of {DOW_N} weekly; "
      f"4a: {int(s10.pass4a.sum())} of {len(s10)} offsets in total")
    P(f"  NOTHING PROMOTED: no RULES change, no PROTOCOL edit, no version bump (rule 6).")
    P(f"  elapsed {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
