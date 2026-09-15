#!/usr/bin/env python3
"""Idea 975 (lane C, 2026-09-15) -- is the WEEKLY PHASE FAMILY SPREAD small because of
AVERAGING or because WEEKDAYS ARE ALIKE?

THE QUESTION (queue, 2026-09-15)
  Idea 965 measured the median OOS CAGR spread WITHIN a rebalance-phase family at 1.75 pp on
  the WEEKLY grid against 3.09 (monthly) and 6.53 (quarterly), and W is the only grid whose
  IS->OOS rank correlation is non-negative (+0.100).  Decompose the spread by grid against the
  NUMBER OF REBALANCES each phase makes and test whether it scales as 1/sqrt(n_rebalances).

WHY IT MATTERS FOR CAPITAL
  The record publishes the family spread as the honest error bar on any single-phase claim
  (963, 965).  If the spread is 1/sqrt(n_reb) AVERAGING noise, then it is PREDICTABLE from the
  cadence alone -- a book can be quoted with an error bar nobody has to re-simulate, and the
  right capital response is to prefer the highest-rebalance cadence the cost budget allows,
  because the phase dial then carries less unpriced luck.  If instead it is a SEPARATION fact
  (two rebalance calendars differ only as much as they are far apart in trading days, and the
  weekly grid is small merely because five weekdays cannot be more than two days apart), then
  n_reb predicts nothing, the error bar must be re-measured per grid, and 965's "W is the one
  steerable dial" reads as "W is the one TRUNCATED dial".

  These two stories make OPPOSITE predictions that this run separates by construction.

THE SEPARATION OF THE TWO STORIES (the whole design in four lines)
  Let D(L, s) = how different two books are that trade the SAME weights on rebalance calendars
  of period L trading days offset by s trading days.
    AVERAGING  says D depends on L (as 1/sqrt(n_reb) ~ sqrt(L)) and is FLAT in s for s >= 1:
               each rebalance draws independent timing noise and n of them average out.
    SEPARATION says D depends on s (books drift apart as their calendars drift apart) and is
               FLAT in L: only how far apart the two calendars sit matters.
  The record's three grids confound the two (W has both the most rebalances AND the smallest
  possible separation).  This run breaks the confound with FIXED-INTERVAL grids: rebalance
  every K trading days, phase d in 0..K-1, so the MATCHED-SEPARATION ratio D(K=5,s)/D(K=21,s)
  at the same s is ~0.488 under AVERAGING and ~1.00 under SEPARATION.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL rule 4: max 2 tuned parameters)
  TUNED 1  GRID, 8 levels, ALL reported:
           CALENDAR  W (5 phases) / M (21) / Q (63)     -- 962's, 965's and the record's grids
           FIXED-K   K05 (5) / K10 (10) / K21 (21) / K42 (42) / K63 (63)  -- rebalance every K
                     trading days; K and the phase count are the SAME number, which is exactly
                     what makes the matched-separation cut possible.
  TUNED 2  BOOK SET, 2 levels, ALL reported, every book also reported on its own:
           RANKED  TOP05 / TOP10 / TOP20   (concentrated, high turnover)
           SPREAD  EWELIG / BAND03         (diffuse; BAND03 @0.75 IS the live RULES v2 book)
  REPORTED AXES, nothing fitted on them, every point published:
           panel  U56 / B136 / SMALL
           gross  CORE 0.75 / EXT 1.00
           cost   0 / 5 / 10 / 25 / 50 bps  (10 bps carries every verdict, PROTOCOL rule 2)
           window FULL / IS 2009-2016 / OOS 2017-2026

  SPREAD IS MEASURED THREE WAYS AND ALL THREE ARE PUBLISHED
           RANGE  max - min over the family   -- the record's statistic (963, 965)
           SD     standard deviation over the family -- count-free
           IQR    inter-quartile range        -- count-free and outlier-free
  This matters because the record compares a 5-draw RANGE against a 63-draw RANGE.  The
  expected range of k iid draws grows like the SPC d2 constant c_k (1.128 at k=2, 2.326 at
  k=5, ~4.2 at k=63), so 12.6x more phases inflates the RANGE ~1.8x at IDENTICAL dispersion.
  Any 1/sqrt(n_reb) test run on RANGE is testing two things at once; this run tests on SD.

PRE-REGISTERED BARS (fixed before any number of this run was read; both directions reported)
  H_SQRT   the spread IS a 1/sqrt(n_reb) averaging fact iff the OLS slope of log(SD of OOS
           CAGR) on log(n_reb per year), pooled over families at the verdict rung, lies in
           [-0.60, -0.40] (the 1/sqrt law is -0.50).
  H_COUNT  the record's RANGE statistic is COUNT-CONFOUNDED iff the median over families of
           (RANGE/SD) / c_k lies inside [0.85, 1.15] -- i.e. the RANGE is the SD times the
           phase-count factor and nothing else.
  H_SEP    the spread is a SEPARATION fact rather than an averaging one iff the median
           matched-separation ratio D(K_small, s) / D(K_big, s), pooled over the three matched
           pairs (K05/K21, K10/K42, K21/K63) and every s both grids can reach, is >= 0.85.
           AVERAGING predicts that same ratio at sqrt(K_small/K_big) = 0.488 / 0.488 / 0.577.
  H_FLAT   AVERAGING's second prediction -- D is FLAT in separation -- holds iff the median
           over families of D(K21, s=10) / D(K21, s=1) <= 1.25.
  H_TRUNC  the WEEKLY family's small spread is a TRUNCATION of the separation axis iff the
           weekly RANGE predicted from the MONTHLY grid's own D(s) curve restricted to
           s <= 2 (the most two weekdays can be apart) lands within 25% of the measured
           weekly RANGE.

  A single mechanism has to answer all five.  They are reported in both directions and the
  verdict is stated for whichever wins.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every ticker with
  `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every CAGR / Sharpe / DD LEVEL below is
  optimistic and none is a capital claim on its own.  Direction for THIS run: every contrast
  is SAME-TAPE, SAME-UNIVERSE, SAME-WEIGHTS and differs ONLY in WHICH DAY the identical book
  rebalances, so the spread, ratio and scaling statistics are unaffected by panel composition.
  The 4b LEVELS are read against SPY, which is not survivorship-inflated, so a survivor panel
  makes 4b failures RARER -- every failure reported here is, if anything, understated.
"""
import os, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

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
CAL_GRIDS = (("W", 5), ("M", 21), ("Q", 63))            # the record's calendar grids
K_GRIDS = ((5, 5), (10, 10), (21, 21), (42, 42), (63, 63))   # fixed-interval: (K, n_phases)
MATCHED = (("K05", "K21", 5, 21), ("K10", "K42", 10, 42), ("K21", "K63", 21, 63))
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
SQRT_LO, SQRT_HI, COUNT_LO, COUNT_HI, SEP_BAR, FLAT_BAR, TRUNC_BAR = \
    -0.60, -0.40, 0.85, 1.15, 0.85, 1.25, 0.25
BOOKSETS = {"RANKED": ["TOP05", "TOP10", "TOP20"], "SPREAD": ["EWELIG", "BAND03"]}
COMMITTED = dict(v2_CAGR=0.086282, v2_Sharpe=1.2018, v2_MaxDD=-0.120549,
                 spy_CAGR=0.1516, spy_Sharpe=0.8861, spy_MaxDD=-0.3372)
D2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 10: 3.078}   # SPC range constants
SMOKE = bool(int(os.environ.get("IDEA975_SMOKE", "0")))
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# (1) phase machinery -- offset_mask / Ctx / mets copied VERBATIM from idea 965/962/942 so
#     this run NESTS the record (G3 replays 965's committed grid).  kmask is NEW.
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each calendar period.  d = 0
    reproduces engine.rebalance_mask(idx, per) exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


def kmask(idx, K, d):
    """FIXED-INTERVAL grid: rebalance every K TRADING DAYS, phase d in 0..K-1.  Phase d
    rebalances on the trading days whose ordinal position i satisfies i % K == d.  The K
    phases are exact translates of one another, each makes the SAME number of rebalances
    (+/-1), and the separation between phases i and j is the cyclic distance
    min(|i-j|, K-|i-j|) trading days (G6)."""
    out = np.zeros(len(idx), bool)
    out[np.arange(d, len(idx), K)] = True
    return pd.Series(out, index=idx), 0


class Ctx:
    """Fast runner -- byte-identical to 965's.  G1 asserts it against engine.backtest."""
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values if hasattr(mask, "values") else mask, bool)
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


def shift_w(W, idx):
    """weights decided at t are applied at t+1 (PROTOCOL rule 2)."""
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    if len(r) == 0:
        return np.nan
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    if len(r) < 2:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec(row):
    """The RECORD's 4b convention (942's / 962's / 965's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_pure(row):
    """Every leg read INSIDE the OOS window against SPY's OOS statistics."""
    return dict(H1=row["OOS_H1"] > row["spy_OOS_H1"], H2=row["OOS_H2"] > row["spy_OOS_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_OOS_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_OOS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def ols(x, y):
    """slope, intercept, R^2 of y on x (finite pairs only)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3 or np.std(x[ok]) == 0:
        return np.nan, np.nan, np.nan, int(ok.sum())
    x, y = x[ok], y[ok]
    b = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
    a = y.mean() - b * x.mean()
    r2 = float(np.corrcoef(x, y)[0, 1] ** 2)
    return float(b), float(a), r2, int(len(x))


def range_factor(k, rng):
    """E[range of k iid standard normals] by Monte Carlo (deterministic seed).  G8 checks it
    against the published SPC d2 constants."""
    z = rng.standard_normal((40000, k))
    return float((z.max(axis=1) - z.min(axis=1)).mean())


# ==========================================================================================
# (2) THE BOOKS -- 942's / 962's / 965's five, verbatim
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    """== rules_v2_weights(px, band, g) -- asserted at G2."""
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def elig_mask(px):
    _, above, vol20 = score(px, vol_scale=False)
    return above & (vol20 < VOLCAP)


def ew_elig(px, g):
    e = elig_mask(px).astype(float).where(px.notna(), 0.0)
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
BOOKSET_OF = {b: s for s, bs in BOOKSETS.items() for b in bs}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


def cyclic_sep(i, j, n):
    d = abs(int(i) - int(j))
    return min(d, n - d)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 975 (lane C, 2026-09-15) -- is the WEEKLY PHASE FAMILY SPREAD small because of")
    P("AVERAGING (1/sqrt(n_rebalances)) or because WEEKDAYS ARE ALIKE (separation)?")
    P("8 grids (W/M/Q + fixed-interval K=5/10/21/42/63) x 5 books x 3 panels x 2 gross x 5 rungs.")
    P("PROTOCOL: 10 bps carries every verdict, next-day execution, both KEEP paths, rule 8.")
    P("=" * 100)
    P()
    P("PRE-REGISTERED BARS (printed before any number of this run is read)")
    P(f"  H_SQRT   OLS slope of log(SD of OOS CAGR) on log(n_reb/yr) in "
      f"[{SQRT_LO:+.2f}, {SQRT_HI:+.2f}]   (the 1/sqrt law is -0.50)")
    P(f"  H_COUNT  median (RANGE/SD)/c_k in [{COUNT_LO:.2f}, {COUNT_HI:.2f}] -- the record's "
      f"RANGE is SD x the phase-count factor")
    P(f"  H_SEP    median matched-separation ratio D(K_small,s)/D(K_big,s) >= {SEP_BAR:.2f}   "
      f"(AVERAGING predicts 0.488 / 0.488 / 0.577)")
    P(f"  H_FLAT   median D(K21, s=10) / D(K21, s=1) <= {FLAT_BAR:.2f}  (AVERAGING says D is "
      f"flat in separation)")
    P(f"  H_TRUNC  weekly RANGE predicted from the MONTHLY D(s<=2) curve within "
      f"{TRUNC_BAR:.0%} of the measured weekly RANGE")
    P()

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
        P(f"  SMALL panel: {sm.shape[1] - 1} names + SPY benchmark ({ndrop} tickers with "
          f"max_1d_move >= 1.0 dropped per data/small_meta.csv)")
    cal_grids = CAL_GRIDS if not SMOKE else (("W", 5), ("M", 21))
    k_grids = K_GRIDS if not SMOKE else ((5, 5), (21, 21))
    GRIDS = [("CAL", per, n) for per, n in cal_grids] + [("K", K, n) for K, n in k_grids]
    gname = {("CAL", p): p for p, _ in cal_grids}
    gname.update({("K", K): f"K{K:02d}" for K, _ in k_grids})
    for k, v in panels.items():
        P(f"  panel {k}: {v.shape[1]} columns, {v.index[0].date()} .. {v.index[-1].date()}, "
          f"{len(v)} rows")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(A) GATES -- run before any number of the hypothesis is read")
    P("=" * 100)
    gk = {}
    px = panels["U56"]
    idx0 = px.index

    bad = sum(int((offset_mask(idx0, per, 0)[0].values
                   != rebalance_mask(idx0, per).values).sum()) for per in ("W", "M", "Q"))
    gk["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q  : {bad} differing rows   "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w75 = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w75.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    gk["G2"] = g2 == 0.0
    P(f"  G2 BAND03 @0.75 == rules_v2_weights (the LIVE rules)       : {g2:.3e}   "
      f"{'PASS' if gk['G2'] else 'FAIL'}")

    g1 = 0.0
    wt75 = shift_w(w75, idx0)
    for per in ("W", "M", "Q"):
        ctx = Ctx(px, offset_mask(idx0, per, 0)[0])
        gr, tn = ctx.run(wt75)
        fast = pd.Series(gr - tn * HEAD_COST / 1e4, index=idx0)
        slow = backtest(px, w75, cost_bps=HEAD_COST, freq=per)["returns"]
        j = idx0[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
        del ctx
    gk["G1"] = g1 < 1e-12
    P(f"  G1 Ctx.run == engine.backtest @10 bps, worst of W/M/Q      : {g1:.3e}   "
      f"{'PASS' if gk['G1'] else 'FAIL'}")

    g4 = 0.0
    wt20 = shift_w(ranked_book(px, 0.75, 20), idx0)
    for _ in range(2):
        c = Ctx(px, kmask(idx0, 21, 3)[0])
        g4 = max(g4, float(np.abs(c.run(wt20)[0] - c.run(wt20)[0]).max()))
        del c
    gk["G4"] = g4 == 0.0
    P(f"  G4 determinism (TOP20 K21 phase 3 re-derived twice)        : {g4:.3e}   "
      f"{'PASS' if gk['G4'] else 'FAIL'}")

    bctx = Ctx(px, offset_mask(idx0, "W", 0)[0])
    bg, bt = bctx.run(wt75)
    mv2 = mets((bg - bt * HEAD_COST / 1e4)[WARM:])
    mspy = mets(px["SPY"].pct_change().fillna(0.0).values[WARM:])
    eng = mets(backtest(px, w75, cost_bps=HEAD_COST, freq="W")["returns"].loc[idx0[WARM]:].values)
    g5 = max(abs(mv2[k] - eng[k]) for k in ("CAGR", "Sharpe", "MaxDD"))
    gk["G5"] = g5 < 1e-12
    P(f"  G5 RULES v2 weekly {mv2['CAGR']:.4%}/{mv2['Sharpe']:.4f}/{mv2['MaxDD']:.4%} == "
      f"engine.backtest(freq='W'): {g5:.3e}   {'PASS' if gk['G5'] else 'FAIL'}")
    drift = max(abs(mv2["CAGR"] - COMMITTED["v2_CAGR"]), abs(mv2["Sharpe"] - COMMITTED["v2_Sharpe"]),
                abs(mv2["MaxDD"] - COMMITTED["v2_MaxDD"]),
                abs(mspy["CAGR"] - COMMITTED["spy_CAGR"]),
                abs(mspy["Sharpe"] - COMMITTED["spy_Sharpe"]),
                abs(mspy["MaxDD"] - COMMITTED["spy_MaxDD"]))
    P(f"     REPORTED, not a gate -- SPY on today's cache {mspy['CAGR']:.4%}/{mspy['Sharpe']:.4f}"
      f"/{mspy['MaxDD']:.4%}; the record's published RULES v2 / SPY constants differ by up to "
      f"{drift:.3e} (a DATA-CACHE drift; G3 pins the machinery against 965's committed grid).")
    del bctx

    # ---- G6: the fixed-interval grid is a clean translate family --------------------------
    prob = []
    for K, n in k_grids:
        ms = [kmask(idx0, K, d)[0].values for d in range(K)]
        cnt = [int(m.sum()) for m in ms]
        if max(cnt) - min(cnt) > 1:
            prob.append(f"K{K} rebalance counts span {min(cnt)}..{max(cnt)}")
        if int(np.sum(np.sum(ms, axis=0) != 1)) != 0:
            prob.append(f"K{K} phases do not partition the trading days")
        if abs(np.mean(cnt) - len(idx0) / K) > 1.0:
            prob.append(f"K{K} mean count {np.mean(cnt):.1f} != T/K {len(idx0)/K:.1f}")
        if not np.array_equal(np.roll(ms[0], 1), ms[1]):
            prob.append(f"K{K} phase 1 is not phase 0 shifted by one trading day")
    gk["G6"] = not prob
    P(f"  G6 fixed-interval grids partition the tape, equal counts, exact translates : "
      f"{'; '.join(prob) if prob else 'clean on all ' + str(len(k_grids)) + ' grids'}   "
      f"{'PASS' if gk['G6'] else 'FAIL'}")

    # ---- G7: the covariance shortcut for pairwise tracking error --------------------------
    rng = np.random.default_rng(20260915)
    A = rng.standard_normal((8, 900)) * 0.01
    Cv = np.cov(A)
    dg = np.diag(Cv)
    TEfast = np.sqrt(np.maximum(dg[:, None] + dg[None, :] - 2 * Cv, 0.0))
    TEslow = np.array([[np.std(A[i] - A[j], ddof=1) for j in range(8)] for i in range(8)])
    g7 = float(np.abs(TEfast - TEslow).max())
    gk["G7"] = g7 < 1e-12
    P(f"  G7 pairwise TE via covariance == direct std(r_i - r_j)     : {g7:.3e}   "
      f"{'PASS' if gk['G7'] else 'FAIL'}")

    # ---- G8: the phase-count range factor c_k ---------------------------------------------
    rngc = np.random.default_rng(975)
    CK = {k: range_factor(k, rngc) for k in sorted(set(list(D2) + [n for _, _, n in GRIDS]))}
    d8 = max(abs(CK[k] - v) for k, v in D2.items())
    gk["G8"] = d8 < 0.02
    P(f"  G8 Monte-Carlo c_k == published SPC d2 constants (k=2..10)  : max|d| {d8:.4f}   "
      f"{'PASS' if gk['G8'] else 'FAIL'}")
    P("     c_k used here: " + ", ".join(f"k={k}:{CK[k]:.3f}" for _, _, k in GRIDS))

    # --------------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(B) THE PHASE GRID -- every (panel, book, gross, grid, phase, rung), full/IS/OOS,")
    P("    plus the OOS daily-return covariance that prices every PAIR of phases")
    P("=" * 100)
    ROWS, BASE, PAIRS = [], {}, []
    for pname, p in panels.items():
        idx = p.index
        post = idx[WARM:]
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(post >= pd.Timestamp(OOS_START))
        is_ = np.asarray(post <= pd.Timestamp(IS_END))
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        bw = rules_v2_weights(p, BAND0, 0.75)                # the LIVE book, weekly (4a target)
        bc = Ctx(p, offset_mask(idx, "W", 0)[0])
        bgr, btn = bc.run(shift_w(bw, idx))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full_MaxDD": maxdd(br)}
        del bc
        WT = {(b, cs): shift_w(BOOKS[b](p, g), idx) for b in BOOKS for cs, g in CLAIM_SETS.items()}
        for kind, key, n_ph in GRIDS:
            gnm = gname[(kind, key)]
            RO = {b: np.empty((n_ph, int(oos.sum()))) for b in BOOKS}   # OOS daily rets @HEAD
            for d in range(n_ph):
                mk = offset_mask(idx, key, d)[0] if kind == "CAL" else kmask(idx, key, d)[0]
                n_reb_oos = float(np.asarray(mk.values)[WARM:][oos].sum())
                n_reb_yr = n_reb_oos / (int(oos.sum()) / 252.0)
                ctx = Ctx(p, mk)
                for (b, cs), W in WT.items():
                    gr, tn = ctx.run(W)
                    gr_w, tn_w = gr[WARM:], tn[WARM:]
                    for c in RUNGS:
                        r = gr_w - tn_w * c / 1e4
                        m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                        ROWS.append(dict(
                            panel=pname, book=b, bookset=BOOKSET_OF[b], gross=cs, grid=gnm,
                            gridkind=kind, n_phases=n_ph, phase=d, cost_bps=c,
                            n_reb_oos=n_reb_oos, n_reb_per_yr=n_reb_yr,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                            turn_per_yr=float(tn_w.sum() / (len(r) / 252.0)),
                            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                            spy_H1=ms["H1"], spy_H2=ms["H2"],
                            spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                            spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"],
                            spy_OOS_H2=ms_o["H2"]))
                        if cs == HEAD_GROSS and c == HEAD_COST:
                            RO[b][d] = r[oos]
                del ctx
            # ---- pairwise separation prices, verdict rung / CORE gross ------------------
            for b in BOOKS:
                R = RO[b]
                Cv = np.cov(R)
                dg = np.diag(np.atleast_2d(Cv)) if n_ph > 1 else np.array([float(Cv)])
                TE = np.sqrt(np.maximum(dg[:, None] + dg[None, :] - 2 * np.atleast_2d(Cv), 0.0)) \
                    * np.sqrt(252) * 100
                cg = np.array([mets(R[d])["CAGR"] for d in range(n_ph)]) * 100
                for i in range(n_ph):
                    for j in range(i + 1, n_ph):
                        PAIRS.append(dict(panel=pname, book=b, grid=gnm, gridkind=kind,
                                          n_phases=n_ph, i=i, j=j,
                                          sep=cyclic_sep(i, j, n_ph), sep_lin=j - i,
                                          TE_pp=float(TE[i, j]),
                                          dCAGR_pp=float(abs(cg[i] - cg[j]))))
            P(f"  panel {pname} grid {gnm} done  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(ROWS)
    lr = [legs_rec(r) for _, r in grid.iterrows()]
    lp = [legs_pure(r) for _, r in grid.iterrows()]
    grid["pass4b_REC"] = [all(x.values()) for x in lr]
    grid["fail4b_REC"] = [failstr(x) for x in lr]
    grid["pass4b_OOSPURE"] = [all(x.values()) for x in lp]
    grid["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                           and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                           and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                      for _, r in grid.iterrows()]
    dump(grid, "grid")
    pairs = pd.DataFrame(PAIRS)
    dump(pairs, "pairs")
    P(f"  {len(grid):,} grid rows = {len(panels)} panels x {len(BOOKS)} books x "
      f"{len(CLAIM_SETS)} gross x {sum(n for _, _, n in GRIDS)} phases x {len(RUNGS)} rungs; "
      f"{len(pairs):,} phase PAIRS priced at {HEAD_COST:.0f} bps / {HEAD_GROSS} gross")

    # ---- G3: this run's CALENDAR rows REBUILD 965's committed grid.csv ---------------------
    comm = OUT / ("2026-09-15_is-the-ANTI-PREDICTIVE-phase-correlation-a-SINGLE-PICK-artefact-"
                  "or-a-ROLLING-one_C.grid.csv")
    if comm.exists():
        cg0 = pd.read_csv(comm).rename(columns={"cadence": "grid"})
        cg0 = cg0[cg0.grid.isin([g for _, g in [(k, gname[(k, x)]) for k, x, _ in GRIDS
                                                if k == "CAL"]])]
        keys = ["panel", "book", "gross", "grid", "phase", "cost_bps"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2", "turn_per_yr"]
        j = cg0.merge(grid, on=keys, suffixes=("_c", "_n"))
        dmax = max(float(np.abs(j[f"{c}_c"].values - j[f"{c}_n"].values).max()) for c in cols)
        gk["G3"] = (len(j) == len(cg0)) and dmax < 1e-10
        P(f"  G3 965's committed grid.csv replayed on {len(j)} of {len(cg0)} calendar rows, "
          f"13 columns, max|d| {dmax:.3e}   {'PASS' if gk['G3'] else 'FAIL'}")
    else:
        gk["G3"] = False
        P("  G3 965's committed grid.csv NOT FOUND -- gate FAILS, nesting unproven")

    # --------------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(C) THE FAMILY SPREAD, THREE WAYS, AGAINST THE NUMBER OF REBALANCES")
    P("=" * 100)
    FAM = []
    for k, sub in grid.groupby(["panel", "book", "gross", "grid", "cost_bps"], sort=False):
        s = sub.sort_values("phase")
        row = dict(panel=k[0], book=k[1], bookset=BOOKSET_OF[k[1]], gross=k[2], grid=k[3],
                   cost_bps=k[4], gridkind=s.iloc[0].gridkind, n_phases=int(s.iloc[0].n_phases),
                   n_reb_per_yr=float(s.n_reb_per_yr.mean()), c_k=CK[int(s.iloc[0].n_phases)],
                   canon_OOS_CAGR=float(s.iloc[0].OOS_CAGR),
                   fam_OOS_CAGR_mean=float(np.nanmean(s.OOS_CAGR.values)),
                   n_phases_pass4b_REC=int(s.pass4b_REC.sum()),
                   n_phases_pass4a=int(s.pass4a.sum()),
                   rho_IS_OOS_CAGR=spearman(s.IS_CAGR.values, s.OOS_CAGR.values),
                   turn_per_yr=float(s.turn_per_yr.mean()))
        for lab, col in (("OOS_CAGR", "OOS_CAGR"), ("OOS_Sharpe", "OOS_Sharpe"),
                         ("OOS_MaxDD", "OOS_MaxDD"), ("CAGR", "CAGR")):
            v = s[col].values.astype(float)
            sc = 100.0 if lab != "OOS_Sharpe" else 1.0
            row[f"RANGE_{lab}"] = float(np.nanmax(v) - np.nanmin(v)) * sc
            row[f"SD_{lab}"] = float(np.nanstd(v, ddof=1)) * sc
            row[f"IQR_{lab}"] = float(np.nanpercentile(v, 75) - np.nanpercentile(v, 25)) * sc
        row["RANGE_over_SD"] = row["RANGE_OOS_CAGR"] / row["SD_OOS_CAGR"] \
            if row["SD_OOS_CAGR"] > 0 else np.nan
        row["RANGE_over_SD_over_ck"] = row["RANGE_over_SD"] / row["c_k"]
        FAM.append(row)
    fams = pd.DataFrame(FAM)
    dump(fams, "families")
    fh = fams[(fams.cost_bps == HEAD_COST) & (fams.gross == HEAD_GROSS)]
    P(f"  {len(fh)} families at the verdict rung ({len(panels)} panels x {len(BOOKS)} books x "
      f"{len(GRIDS)} grids); {len(fams)} over all rungs and gross")
    P()
    P("  MEDIAN family spread of OOS CAGR (pp), by grid -- three measures + the rebalance count:")
    t = fh.groupby("grid").agg(n_phases=("n_phases", "first"),
                               n_reb_per_yr=("n_reb_per_yr", "mean"),
                               RANGE_pp=("RANGE_OOS_CAGR", "median"),
                               SD_pp=("SD_OOS_CAGR", "median"),
                               IQR_pp=("IQR_OOS_CAGR", "median"),
                               c_k=("c_k", "first"),
                               RANGE_over_SD=("RANGE_over_SD", "median"),
                               turn=("turn_per_yr", "mean"),
                               families=("grid", "size")).sort_values("n_reb_per_yr")
    P(t.to_string(float_format=lambda x: f"{x:.3f}"))
    w_r = float(fh[fh.grid == "W"].RANGE_OOS_CAGR.median()) if (fh.grid == "W").any() else np.nan
    m_r = float(fh[fh.grid == "M"].RANGE_OOS_CAGR.median()) if (fh.grid == "M").any() else np.nan
    q_r = float(fh[fh.grid == "Q"].RANGE_OOS_CAGR.median()) if (fh.grid == "Q").any() else np.nan
    P(f"  965's published numbers, re-derived: W {w_r:.2f} pp / M {m_r:.2f} / Q {q_r:.2f} "
      f"(it published 1.75 / 3.09 / 6.53)")
    P()
    P("  H_SQRT -- OLS of log(SD of OOS CAGR) on log(n_reb per year), verdict rung, CORE gross:")
    rows_sq = []
    for lab, sub in [("ALL 8 grids", fh), ("CALENDAR W/M/Q", fh[fh.gridkind == "CAL"]),
                     ("FIXED-K only", fh[fh.gridkind == "K"])]:
        for meas in ("SD_OOS_CAGR", "RANGE_OOS_CAGR", "IQR_OOS_CAGR"):
            b, a, r2, n = ols(np.log(sub.n_reb_per_yr.values), np.log(sub[meas].values))
            rows_sq.append(dict(subset=lab, measure=meas, slope=b, intercept=a, R2=r2, n=n))
    sq = pd.DataFrame(rows_sq)
    P(sq.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    slope_sd = float(sq[(sq.subset == "ALL 8 grids") & (sq.measure == "SD_OOS_CAGR")].slope.iloc[0])
    slope_rg = float(sq[(sq.subset == "ALL 8 grids")
                        & (sq.measure == "RANGE_OOS_CAGR")].slope.iloc[0])
    H_SQRT = SQRT_LO <= slope_sd <= SQRT_HI
    P(f"  H_SQRT  slope on SD = {slope_sd:+.4f} (bar [{SQRT_LO:+.2f}, {SQRT_HI:+.2f}])  -> "
      f"{'PASS' if H_SQRT else 'FAIL'}   [on the record's RANGE it reads {slope_rg:+.4f}]")
    P()
    P("  H_COUNT -- is the record's RANGE just SD x the phase-count factor c_k?")
    ck_med = float(fh.RANGE_over_SD_over_ck.median())
    H_COUNT = COUNT_LO <= ck_med <= COUNT_HI
    P(fh.groupby("grid").agg(n_phases=("n_phases", "first"), c_k=("c_k", "first"),
                             RANGE_over_SD=("RANGE_over_SD", "median"),
                             ratio_to_ck=("RANGE_over_SD_over_ck", "median"))
      .sort_values("n_phases").to_string(float_format=lambda x: f"{x:.3f}"))
    P(f"  H_COUNT median (RANGE/SD)/c_k = {ck_med:.3f} (bar [{COUNT_LO:.2f}, {COUNT_HI:.2f}]) "
      f"-> {'PASS' if H_COUNT else 'FAIL'}")
    big = "Q" if (fh.grid == "Q").any() else "M"
    if (fh.grid == "W").any() and (fh.grid == big).any():
        kb = int(fh[fh.grid == big].n_phases.iloc[0])
        sd_ratio = (float(fh[fh.grid == big].SD_OOS_CAGR.median())
                    / float(fh[fh.grid == "W"].SD_OOS_CAGR.median()))
        rg_ratio = float(fh[fh.grid == big].RANGE_OOS_CAGR.median()) / w_r
        P(f"     so of the W-to-{big} RANGE ratio {rg_ratio:.2f}x, the PHASE COUNT alone accounts "
          f"for {CK[kb] / CK[5]:.2f}x and the DISPERSION for {sd_ratio:.2f}x "
          f"({CK[kb] / CK[5] * sd_ratio:.2f}x together)")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE MATCHED-SEPARATION CUT -- the one place the two stories disagree")
    P("=" * 100)
    ph = pairs.copy()
    P("  D(grid, separation): median over families of the pairwise OOS tracking error (pp/yr)")
    P("  and of |dCAGR| (pp), by grid and cyclic separation in trading days:")
    piv = ph.pivot_table(index="sep", columns="grid", values="TE_pp", aggfunc="median")
    P("  --- tracking error TE_pp ---")
    P(piv.head(12).to_string(float_format=lambda x: f"{x:.3f}"))
    pivc = ph.pivot_table(index="sep", columns="grid", values="dCAGR_pp", aggfunc="median")
    P("  --- |dCAGR| pp ---")
    P(pivc.head(12).to_string(float_format=lambda x: f"{x:.3f}"))
    P()
    P("  MATCHED SEPARATION: same s, grids whose rebalance counts differ 3-4x.")
    P("  AVERAGING predicts the ratio at sqrt(K_small/K_big); SEPARATION predicts 1.00.")
    MS = []
    for gsm, gbg, Ks, Kb in MATCHED:
        pred = np.sqrt(Ks / Kb)
        smax = min(Ks // 2, Kb // 2)
        for s in range(1, smax + 1):
            a = ph[(ph.grid == gsm) & (ph.sep == s)]
            b = ph[(ph.grid == gbg) & (ph.sep == s)]
            if not len(a) or not len(b):
                continue
            for meas in ("TE_pp", "dCAGR_pp"):
                ka = a.groupby(["panel", "book"])[meas].median()
                kb = b.groupby(["panel", "book"])[meas].median()
                jn = pd.concat([ka.rename("small"), kb.rename("big")], axis=1).dropna()
                jn = jn[jn.big > 0]
                if not len(jn):
                    continue
                MS.append(dict(pair=f"{gsm}/{gbg}", K_small=Ks, K_big=Kb, sep=s, measure=meas,
                               n_families=len(jn),
                               ratio=float((jn.small / jn.big).median()),
                               pred_averaging=float(pred),
                               small=float(jn.small.median()), big=float(jn.big.median())))
    ms_df = pd.DataFrame(MS)
    dump(ms_df, "matched")
    mt = ms_df[ms_df.measure == "TE_pp"]
    P(mt.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sep_ratio = float(mt.ratio.median())
    sep_ratio_c = float(ms_df[ms_df.measure == "dCAGR_pp"].ratio.median())
    pred_med = float(mt.pred_averaging.median())
    H_SEP = sep_ratio >= SEP_BAR
    P(f"  H_SEP  median matched-separation TE ratio = {sep_ratio:.4f} (|dCAGR| twin "
      f"{sep_ratio_c:.4f}) against the {SEP_BAR:.2f} separation bar and the AVERAGING "
      f"prediction {pred_med:.4f}  ->  {'PASS (SEPARATION)' if H_SEP else 'FAIL'}")
    P(f"     distance to each story: |obs - 1.00| = {abs(sep_ratio - 1.0):.4f}, "
      f"|obs - averaging| = {abs(sep_ratio - pred_med):.4f}")
    P()
    P("  H_FLAT -- AVERAGING also says D must be FLAT in separation.  Within one grid:")
    FL = []
    for gnm2 in sorted(ph.grid.unique()):
        sub = ph[ph.grid == gnm2]
        smax = int(sub.sep.max())
        if smax < 2:
            continue
        for meas in ("TE_pp", "dCAGR_pp"):
            lo = sub[sub.sep == 1].groupby(["panel", "book"])[meas].median()
            hi = sub[sub.sep == smax].groupby(["panel", "book"])[meas].median()
            jn = pd.concat([lo.rename("s1"), hi.rename("smax")], axis=1).dropna()
            jn = jn[jn.s1 > 0]
            if len(jn):
                FL.append(dict(grid=gnm2, measure=meas, s_max=smax, n_families=len(jn),
                               D_s1=float(jn.s1.median()), D_smax=float(jn.smax.median()),
                               ratio=float((jn.smax / jn.s1).median())))
    fl = pd.DataFrame(FL)
    P(fl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    k21 = fl[(fl.grid == "K21") & (fl.measure == "TE_pp")] if len(fl) else fl
    flat_ratio = float(k21.ratio.iloc[0]) if len(k21) else np.nan
    H_FLAT = bool(np.isfinite(flat_ratio) and flat_ratio <= FLAT_BAR)
    P(f"  H_FLAT  D(K21, s={int(k21.s_max.iloc[0]) if len(k21) else 0}) / D(K21, s=1) = "
      f"{flat_ratio:.4f} (bar <= {FLAT_BAR:.2f})  ->  "
      f"{'PASS (AVERAGING)' if H_FLAT else 'FAIL (D GROWS WITH SEPARATION)'}")
    P()
    P("  the same regression, run on the PAIRS rather than the families -- log TE on")
    P("  log(n_reb) and log(separation) one at a time, and both together:")
    pk = ph[(ph.gridkind == "K") & (ph.TE_pp > 0) & (ph.sep > 0)].copy()
    pk["n_reb"] = 252.0 / pk.n_phases
    b1, _, r1, n1 = ols(np.log(pk.n_reb.values), np.log(pk.TE_pp.values))
    b2, _, r2, n2 = ols(np.log(pk.sep.values), np.log(pk.TE_pp.values))
    X = np.column_stack([np.ones(len(pk)), np.log(pk.n_reb.values), np.log(pk.sep.values)])
    y = np.log(pk.TE_pp.values)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    r3 = float(1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum())
    P(f"     log TE ~ log(n_reb)            slope {b1:+.4f}  R2 {r1:.4f}  n {n1:,}   "
      f"(AVERAGING wants -0.50)")
    P(f"     log TE ~ log(separation)       slope {b2:+.4f}  R2 {r2:.4f}  n {n2:,}   "
      f"(SEPARATION wants > 0)")
    P(f"     log TE ~ both                  n_reb {beta[1]:+.4f} | sep {beta[2]:+.4f}  "
      f"R2 {r3:.4f}   <- the horse race")
    P()
    P("  H_TRUNC -- predict the WEEKLY family RANGE from the MONTHLY grid's own D(s) curve,")
    P("  restricted to s <= 2 (the most two weekdays can be apart):")
    H_TRUNC, tr_err = False, np.nan
    try:
        mm_ = ph[(ph.grid == "M") & (ph.sep <= 2) & (ph.sep > 0)]
        w_pairs = ph[(ph.grid == "W") & (ph.sep > 0)]
        pred_rng = float(mm_.groupby(["panel", "book"]).dCAGR_pp.max().median())
        obs_rng = float(w_pairs.groupby(["panel", "book"]).dCAGR_pp.max().median())
        tr_err = abs(pred_rng - obs_rng) / obs_rng
        H_TRUNC = tr_err <= TRUNC_BAR
        P(f"     monthly D(s<=2) predicts a weekly RANGE of {pred_rng:.3f} pp; measured weekly "
          f"RANGE {obs_rng:.3f} pp; error {tr_err:.1%} (bar {TRUNC_BAR:.0%})  ->  "
          f"{'PASS' if H_TRUNC else 'FAIL'}")
        full_m = float(ph[ph.grid == "M"].groupby(["panel", "book"]).dCAGR_pp.max().median())
        P(f"     for scale: the FULL monthly range is {full_m:.3f} pp, so restricting the "
          f"separation axis to s<=2 alone removes "
          f"{(1 - pred_rng / full_m) * 100:.1f}% of it")
    except Exception as e:                                   # pragma: no cover
        P(f"     H_TRUNC could not be evaluated: {e}")
    P()
    P("  POST-HOC, DECLARED AS POST-HOC AND NOT A PRE-REGISTERED BAR -- H_TRUNC's estimator is")
    P("  itself count-confounded (a MAX over 41 monthly pairs at s<=2 against 10 weekly ones),")
    P("  which is the very inflation H_COUNT measured.  The count-matched form of the same")
    P("  question: take every window of L CONSECUTIVE phases inside each family and measure")
    P("  the RANGE of OOS CAGR over that window.  A window of L phases has L draws and at most")
    P("  L-1 days of separation on EVERY grid, so grid differences that survive here are real.")
    WN = []
    for L in (3, 5):
        for k, sub in grid[(grid.cost_bps == HEAD_COST)
                           & (grid.gross == HEAD_GROSS)].groupby(
                               ["panel", "book", "grid"], sort=False):
            v = sub.sort_values("phase").OOS_CAGR.values.astype(float) * 100
            n = len(v)
            if n < L:
                continue
            rr = [float(np.nanmax(np.take(v, range(i, i + L), mode="wrap"))
                        - np.nanmin(np.take(v, range(i, i + L), mode="wrap"))) for i in range(n)]
            WN.append(dict(window=L, panel=k[0], book=k[1], grid=k[2], n_phases=n,
                           n_reb_per_yr=float(sub.n_reb_per_yr.mean()),
                           win_RANGE_pp=float(np.median(rr)),
                           full_RANGE_pp=float(np.nanmax(v) - np.nanmin(v))))
    wn = pd.DataFrame(WN)
    dump(wn, "windows")
    P(wn.pivot_table(index="grid", columns="window", values="win_RANGE_pp", aggfunc="median")
      .join(wn[wn.window == 3].groupby("grid")[["n_reb_per_yr", "full_RANGE_pp"]].median())
      .sort_values("n_reb_per_yr").to_string(float_format=lambda x: f"{x:.3f}"))
    for L in (3, 5):
        s3 = wn[wn.window == L]
        b3, _, r3b, n3 = ols(np.log(s3.n_reb_per_yr.values), np.log(s3.win_RANGE_pp.values))
        lo = s3.groupby("grid").win_RANGE_pp.median()
        P(f"     window L={L}: median range {lo.min():.3f}..{lo.max():.3f} pp across the 8 "
          f"grids (spread {lo.max() / lo.min():.2f}x, against {q_r / w_r:.2f}x for the record's "
          f"FULL-family statistic); OLS slope on log n_reb {b3:+.4f} (R2 {r3b:.4f}, n {n3})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- grid and phase chosen on 2009-2016 ONLY, 2017-2026 read once")
    P("=" * 100)
    PICKS = []
    for (pnl, b, cs, c), sub in grid.groupby(["panel", "book", "gross", "cost_bps"], sort=False):
        base = BASE[(pnl, c)]
        cands = {
            "CANON_W":     sub[(sub.grid == "W") & (sub.phase == 0)],          # the live cadence
            "IS_PHASE_W":  sub[sub.grid == "W"],                               # 1 free param
            "IS_GRIDPHASE": sub,                                               # 2 free params
            "IS_GRID_CANON": sub[sub.phase == 0],                              # 1 free param
            "MAXREB_CANON": sub[(sub.grid == "K05") & (sub.phase == 0)],       # this idea's rule
        }
        for nm, cd in cands.items():
            if not len(cd):
                continue
            pick = cd.loc[cd.IS_Sharpe.idxmax()] if nm.startswith("IS_") else cd.iloc[0]
            row = dict(panel=pnl, book=b, bookset=BOOKSET_OF[b], gross=cs, cost_bps=c,
                       chooser=nm, grid=pick.grid, phase=int(pick.phase),
                       n_reb_per_yr=float(pick.n_reb_per_yr),
                       IS_Sharpe=float(pick.IS_Sharpe), IS_CAGR=float(pick.IS_CAGR),
                       CAGR=float(pick.CAGR), Sharpe=float(pick.Sharpe),
                       MaxDD=float(pick.MaxDD), H1=float(pick.H1), H2=float(pick.H2),
                       OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                       OOS_MaxDD=float(pick.OOS_MaxDD), OOS_H1=float(pick.OOS_H1),
                       OOS_H2=float(pick.OOS_H2), turn_per_yr=float(pick.turn_per_yr),
                       spy_CAGR=float(pick.spy_CAGR), spy_Sharpe=float(pick.spy_Sharpe),
                       spy_MaxDD=float(pick.spy_MaxDD), spy_H1=float(pick.spy_H1),
                       spy_H2=float(pick.spy_H2), spy_OOS_CAGR=float(pick.spy_OOS_CAGR),
                       spy_OOS_Sharpe=float(pick.spy_OOS_Sharpe),
                       spy_OOS_MaxDD=float(pick.spy_OOS_MaxDD),
                       spy_OOS_H1=float(pick.spy_OOS_H1), spy_OOS_H2=float(pick.spy_OOS_H2),
                       base_OOS_CAGR=base["CAGR"], base_OOS_Sharpe=base["Sharpe"],
                       base_OOS_MaxDD=base["MaxDD"], base_OOS_H1=base["H1"],
                       base_OOS_H2=base["H2"],
                       pass4b_REC=bool(pick.pass4b_REC), fail4b_REC=pick.fail4b_REC,
                       pass4b_OOSPURE=bool(pick.pass4b_OOSPURE), pass4a=bool(pick.pass4a))
            PICKS.append(row)
    picks = pd.DataFrame(PICKS)
    dump(picks, "walkforward")
    hv = picks[(picks.cost_bps == HEAD_COST)]
    P(f"  {len(picks):,} rule-8 picks ({len(hv)} at the verdict rung); every chooser reads only")
    P("  2009-2016 statistics and is scored on 2017-2026 once.")
    P(hv.groupby("chooser").agg(cells=("OOS_CAGR", "size"), pass4b=("pass4b_REC", "sum"),
                                pass4b_pure=("pass4b_OOSPURE", "sum"), pass4a=("pass4a", "sum"),
                                OOS_CAGR=("OOS_CAGR", "mean"),
                                OOS_Sharpe=("OOS_Sharpe", "mean"),
                                OOS_MaxDD=("OOS_MaxDD", "mean"),
                                turn=("turn_per_yr", "mean"),
                                n_reb=("n_reb_per_yr", "mean"))
      .to_string(float_format=lambda x: f"{x:.4f}"))
    sp = hv.iloc[0]
    P(f"  SPY OOS {sp.spy_OOS_CAGR:.2%} / {sp.spy_OOS_Sharpe:.3f} / {sp.spy_OOS_MaxDD:.2%}   |   "
      f"live RULES v2 OOS (mean over panels) {hv.base_OOS_CAGR.mean():.2%} / "
      f"{hv.base_OOS_Sharpe.mean():.3f} / {hv.base_OOS_MaxDD.mean():.2%}")
    P()
    P("  4b/4a pass counts over the WHOLE grid at the verdict rung, by grid:")
    gh = grid[grid.cost_bps == HEAD_COST]
    P(gh.groupby("grid").agg(rows=("pass4b_REC", "size"), pass4b=("pass4b_REC", "sum"),
                             rate4b=("pass4b_REC", "mean"), pass4a=("pass4a", "sum"),
                             n_reb=("n_reb_per_yr", "mean"),
                             turn=("turn_per_yr", "mean")).sort_values("n_reb")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("  and over every rung (4b pass rate):")
    P(grid.pivot_table(index="cost_bps", columns="grid", values="pass4b_REC", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P()
    fmk = fams[(fams.cost_bps == HEAD_COST)].set_index(["panel", "book", "gross", "grid"])
    hv = hv.copy()
    hv["blind_rate"] = [float(fmk.loc[(r.panel, r.book, r.gross, r.grid), "n_phases_pass4b_REC"])
                        / float(fmk.loc[(r.panel, r.book, r.gross, r.grid), "n_phases"])
                        for _, r in hv.iterrows()]
    hv["fam_SD_pp"] = [float(fmk.loc[(r.panel, r.book, r.gross, r.grid), "SD_OOS_CAGR"])
                       for _, r in hv.iterrows()]
    P()
    P("  965's STANDING REQUIREMENT -- every 4b pass a phase-choosing rule produces is quoted")
    P("  with its own family's BLIND base rate (the share of that family's phases that pass):")
    wb = hv[hv.pass4b_REC]
    if len(wb):
        P(f"     {len(wb)} rule-8 picks clear 4b at the verdict rung: median own-family blind "
          f"rate {wb.blind_rate.median():.3f}, mean {wb.blind_rate.mean():.3f}; "
          f"{int((wb.blind_rate >= 0.25).sum())} of {len(wb)} "
          f"({(wb.blind_rate >= 0.25).mean():.3f}) sit on a family a coin clears at least a "
          f"quarter of the time")
        P(wb[["panel", "book", "gross", "chooser", "grid", "phase", "OOS_CAGR", "OOS_Sharpe",
              "OOS_MaxDD", "blind_rate", "fam_SD_pp", "pass4a"]]
          .sort_values("OOS_Sharpe", ascending=False)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("     (no rule-8 pick clears 4b)")
    both = hv[hv.pass4b_REC & hv.pass4a]
    P(f"  picks clearing BOTH KEEP paths (4a and 4b) at the verdict rung: {len(both)} of "
      f"{len(hv)}" + ("" if not len(both) else ""))
    if len(both):
        P(both[["panel", "book", "gross", "chooser", "grid", "phase", "OOS_CAGR", "OOS_Sharpe",
                "OOS_MaxDD", "blind_rate"]].to_string(index=False,
                                                      float_format=lambda x: f"{x:.4f}"))
    P()
    best = hv.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P("  RULE 8 + BOTH KEEP PATHS -- the single best rule-8 pick by OOS Sharpe, in full:")
    P(f"     {best.panel}/{best.book}/{best.gross}/{best.chooser} -> grid {best.grid} "
      f"phase {best.phase} ({best.n_reb_per_yr:.1f} rebalances/yr)")
    P(f"     OOS  CAGR {best.OOS_CAGR:.2%}  Sharpe {best.OOS_Sharpe:.3f}  "
      f"MaxDD {best.OOS_MaxDD:.2%}   |  FULL CAGR {best.CAGR:.2%}  Sharpe {best.Sharpe:.3f}  "
      f"MaxDD {best.MaxDD:.2%}  halves {best.H1:.3f} / {best.H2:.3f}")
    P(f"     SPY  OOS CAGR {best.spy_OOS_CAGR:.2%}  Sharpe {best.spy_OOS_Sharpe:.3f}  "
      f"MaxDD {best.spy_OOS_MaxDD:.2%}  (full {best.spy_CAGR:.2%} / {best.spy_Sharpe:.3f} / "
      f"{best.spy_MaxDD:.2%})")
    P(f"     LIVE RULES v2 OOS CAGR {best.base_OOS_CAGR:.2%}  Sharpe {best.base_OOS_Sharpe:.3f}  "
      f"MaxDD {best.base_OOS_MaxDD:.2%}")
    P(f"     4b {best.pass4b_REC} (fails: {best.fail4b_REC}) | 4b OOSPURE "
      f"{best.pass4b_OOSPURE} | 4a {best.pass4a}")
    fam_hit = fams[(fams.panel == best.panel) & (fams.book == best.book)
                   & (fams.grid == best.grid) & (fams.gross == best.gross)
                   & (fams.cost_bps == HEAD_COST)]
    if len(fam_hit):
        f0 = fam_hit.iloc[0]
        P(f"     ITS OWN FAMILY'S ERROR BAR: {int(f0.n_phases)} phases, OOS CAGR SD "
          f"{f0.SD_OOS_CAGR:.3f} pp, RANGE {f0.RANGE_OOS_CAGR:.3f} pp, and "
          f"{int(f0.n_phases_pass4b_REC)} of {int(f0.n_phases)} phases clear 4b "
          f"({f0.n_phases_pass4b_REC / f0.n_phases:.3f} -- a blind coin's rate on this cell)")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    H = [("H_SQRT", H_SQRT, f"slope of log SD on log n_reb = {slope_sd:+.4f} "
          f"(bar [{SQRT_LO:+.2f},{SQRT_HI:+.2f}]); on the record's RANGE {slope_rg:+.4f}"),
         ("H_COUNT", H_COUNT, f"median (RANGE/SD)/c_k = {ck_med:.3f} "
          f"(bar [{COUNT_LO:.2f},{COUNT_HI:.2f}])"),
         ("H_SEP", H_SEP, f"matched-separation TE ratio {sep_ratio:.4f} vs bar {SEP_BAR:.2f}; "
          f"AVERAGING predicted {pred_med:.4f}"),
         ("H_FLAT", H_FLAT, f"D(K21,s_max)/D(K21,s=1) = {flat_ratio:.4f} vs bar {FLAT_BAR:.2f}"),
         ("H_TRUNC", H_TRUNC, f"weekly RANGE predicted from monthly D(s<=2) within "
          f"{tr_err:.1%} (bar {TRUNC_BAR:.0%})")]
    hy = pd.DataFrame([dict(hypothesis=k, result="PASS" if v else "FAIL", detail=d)
                       for k, v, d in H])
    P(hy.to_string(index=False))
    dump(hy, "hypotheses")
    P()
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failing'})")
    P(f"  done in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
