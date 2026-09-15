#!/usr/bin/env python3
"""Idea 962 (lane C, 2026-09-15) -- does an IS-CHOSEN PHASE ever SURVIVE out of sample on ANY
book?

THE QUESTION (queue, 2026-09-15)
  Idea 942 found the in-sample phase chooser lands on the canonical phase in 0 of 12 cells and
  that every IS-chosen phase then fails OOS on `L4_DD` alone, buying 3-6 pp of OOS CAGR with
  2-5 pp of extra drawdown.  Run the chooser over all 5 books x 3 panels x BOTH cadences and
  report the OOS 4b pass rate AGAINST THE CANONICAL'S.

WHY IT MATTERS FOR CAPITAL
  The rebalance PHASE (which day of the month/quarter the identical book trades) is a free dial:
  942 measured family CAGR spreads of median 3.04 pp (M) / 4.37 pp (Q) and maxima up to 23.93 pp,
  so ANY published single-phase CAGR can be moved several points by a choice nobody registers.
  942 ran the chooser on 12 cells and jointly over books -- it could not say whether a chooser
  ever PAYS.  This run asks the capital question directly: pick the phase on 2009-2016 alone,
  read 2017-2026 ONCE, and compare the chooser's OOS 4b pass rate against the canonical phase's
  on the same cell.  If the chooser never beats the canonical, the honest convention is 'trade
  the canonical phase and publish the family spread', and phase is not a dial worth tuning.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL rule 4: max 2 tuned parameters)
  TUNED 1  CHOOSER, 6 levels, every one reported, all IS-ONLY by construction (G6):
           C_CAGR    argmax IS CAGR                      (942's chooser #1)
           C_SHARPE  argmax IS Sharpe                    (942's chooser #2)
           C_CALMAR  argmax IS CAGR / |IS MaxDD|
           C_DDMIN   argmin |IS MaxDD|                   (the leg 942 says does the killing)
           C_ISLEGS  argmax number of 4b legs passed IN SAMPLE, ties -> IS Sharpe
           C_MEDIAN  the phase whose IS CAGR is the family MEDIAN (a 'typical phase' control
                     that still only reads IS, i.e. choosing WITHOUT chasing)
  TUNED 2  BOOK SET, 5 levels, every one reported -- 942's own five:
           TOP05 / TOP10 / TOP20  composite rank, k names at gross/k, no vol scaler
           EWELIG                 equal weight over every eligible name (no ranking, no lookback)
           BAND03                 the 200d +/-3% band book == RULES v2, the LIVE rules
  CONTROLS, not tuned, computed on every family:
           CANONICAL  phase 0 (period-end) -- the thing the record actually publishes
           FAMILY     the mean/median OOS over ALL phases -- the phase-averaged honest estimator
           ORACLE     the best OOS phase, chosen WITH hindsight.  It is not a strategy; it
                      separates 'the chooser is bad' from 'no phase on this book could pass'.
  REPORTED AXES, nothing fitted on them, every point published:
           panel   U56 / B136 / SMALL          (3)
           cadence M (21 phases) / Q (63)      (2)
           gross   CORE = 0.75 / EXT = 1.00    (2)
           cost    0 / 5 / 10 / 25 / 50 bps    (5; 10 bps carries every verdict, PROTOCOL rule 2)
           4b convention  REC (the record's: OOS levels against SPY's FULL-sample DD and CAGR)
                          and OOSPURE (every leg read inside the OOS window).  The verdict is
                          read at REC for continuity with 942; the OOSPURE delta is published
                          because the record has repeatedly found this family convention-sensitive.

PRE-REGISTERED BARS (fixed before any number of this run was read; both directions reported)
  H_SURV    an IS-chosen phase SURVIVES iff the pooled chooser OOS 4b pass rate at the verdict
            rung is > 0 AND >= the canonical's on the same cells.
  H_BEAT    choosing PAYS on levels iff the chooser's OOS CAGR exceeds the canonical's in
            >= 60% of (chooser, book, panel, cadence, gross) cells at the verdict rung.
  H_PRED    the IS phase ranking PREDICTS the OOS one iff the median within-family Spearman
            correlation between IS CAGR and OOS CAGR across phases is >= 0.30.
  H_DD      942's 'fails OOS on L4_DD alone' GENERALISES iff >= 90% of failing chooser cells
            have the failing-leg string exactly `L4_DD`.
  H_ORACLE  no phase could have passed iff the ORACLE (hindsight-best phase) also fails 4b in
            >= 90% of families -- in which case the phase dial is not where the 4b failure lives.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every ticker with
  `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every CAGR/Sharpe/DD LEVEL below is
  optimistic and none is a capital claim on its own.  Direction for THIS run: the chooser-vs-
  canonical contrast is SAME-TAPE, SAME-UNIVERSE, SAME-WEIGHTS and differs only in WHICH DAY the
  identical book trades, so the pass-rate comparison is unaffected by panel composition.  The 4b
  LEVELS are read against SPY, which is not survivorship-inflated, so a survivor panel makes the
  books look BETTER and 4b failures RARER -- every 4b failure reported here is therefore, if
  anything, understated.
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
DOM_N, DOQ_N = 21, 63
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
SURV_BAR, BEAT_BAR, PRED_BAR, DD_BAR, ORACLE_BAR = 0.0, 0.60, 0.30, 0.90, 0.90
# committed levels the record publishes for the live book and the benchmark (G5)
COMMITTED = dict(v2_CAGR=0.086282, v2_Sharpe=1.2018, v2_MaxDD=-0.120549,
                 spy_CAGR=0.1516, spy_Sharpe=0.8861, spy_MaxDD=-0.3372)
SMOKE = bool(int(os.environ.get("IDEA962_SMOKE", "0")))
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# (1) phase machinery -- copied VERBATIM from idea 942/938 so this run NESTS the record
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


class Ctx:
    """Fast runner -- byte-identical to 942's.  G1 asserts it against engine.backtest."""
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
    """The RECORD's 4b convention (942's, verbatim): full-sample halves, OOS Sharpe, and the DD
    and CAGR legs read as OOS levels against SPY's FULL-sample drawdown and CAGR."""
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


def legs_is(row):
    """The same 4b alphabet read entirely INSIDE the IS window -- the C_ISLEGS chooser's input.
    Uses no OOS column (G6)."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ==========================================================================================
# (2) THE BOOK SET -- TUNED axis 2, 942's five books verbatim
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


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


# ==========================================================================================
# (3) THE CHOOSERS -- TUNED axis 1.  Every one reads IS_* columns ONLY (G6 proves it).
# ==========================================================================================
def _argmax(v, tiebreak=None):
    """Deterministic argmax: highest value, ties broken by `tiebreak` then by lowest index."""
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return 0
    best = np.nanmax(v)
    cand = np.flatnonzero(np.isclose(v, best, rtol=0, atol=0))
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


def choose(name, sub):
    """sub: one family's rows, sorted by phase.  Returns the chosen positional index."""
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    isdd = np.abs(sub.IS_MaxDD.values)
    if name == "C_CAGR":
        return _argmax(isc, iss)
    if name == "C_SHARPE":
        return _argmax(iss, isc)
    if name == "C_CALMAR":
        return _argmax(np.where(isdd > 0, isc / np.where(isdd > 0, isdd, np.nan), np.nan), iss)
    if name == "C_DDMIN":
        return _argmax(-isdd, iss)
    if name == "C_ISLEGS":
        return _argmax(sub.IS_legs_passed.values, iss)
    if name == "C_MEDIAN":
        ok = np.isfinite(isc)
        order = np.argsort(np.where(ok, isc, np.inf), kind="stable")
        n = int(ok.sum())
        return int(order[max(n // 2 - (1 - n % 2), 0)]) if n else 0
    raise KeyError(name)


CHOOSERS = ["C_CAGR", "C_SHARPE", "C_CALMAR", "C_DDMIN", "C_ISLEGS", "C_MEDIAN"]


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 962 (lane C, 2026-09-15) -- does an IS-CHOSEN PHASE ever SURVIVE out of sample on")
    P("ANY book?   6 choosers x 5 books x 3 panels x 2 cadences x 2 gross x 5 cost rungs.")
    P("PROTOCOL: 10 bps carries every verdict, next-day execution, both KEEP paths, rule 8.")
    P("=" * 100)
    P()
    P("PRE-REGISTERED BARS (printed before any number of this run is read)")
    P(f"  H_SURV    pooled chooser OOS 4b pass rate > {SURV_BAR:.0%} AND >= the canonical's")
    P(f"  H_BEAT    chooser OOS CAGR > canonical's in >= {BEAT_BAR:.0%} of verdict-rung cells")
    P(f"  H_PRED    median within-family Spearman(IS CAGR, OOS CAGR) >= {PRED_BAR:.2f}")
    P(f"  H_DD      >= {DD_BAR:.0%} of failing chooser cells fail on exactly `L4_DD`")
    P(f"  H_ORACLE  the hindsight-best phase also fails 4b in >= {ORACLE_BAR:.0%} of families")
    P()

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    if not SMOKE:
        sm, ndrop = load_small()
        panels["SMALL"] = sm
        P(f"  SMALL panel: {sm.shape[1] - 1} names + SPY benchmark ({ndrop} tickers with "
          f"max_1d_move >= 1.0 dropped per data/small_meta.csv)")
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

    bad = sum(int((offset_mask(px.index, per, 0)[0].values
                   != rebalance_mask(px.index, per).values).sum()) for per in ("W", "M", "Q"))
    gk["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q  : {bad} differing rows   "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w75 = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w75.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    gk["G2"] = g2 == 0.0
    P(f"  G2 BAND03 @0.75 == rules_v2_weights (the LIVE rules)       : {g2:.3e}   "
      f"{'PASS' if gk['G2'] else 'FAIL'}")

    g1 = 0.0
    for per in ("M", "Q"):
        ctx = Ctx(px, offset_mask(px.index, per, 0)[0])
        gr, tn = ctx.run(ctx.shift(w75))
        fast = pd.Series(gr - tn * HEAD_COST / 1e4, index=px.index)
        slow = backtest(px, w75, cost_bps=HEAD_COST, freq=per)["returns"]
        j = px.index[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
    gk["G1"] = g1 < 1e-12
    P(f"  G1 Ctx.run == engine.backtest @10 bps, worse of M and Q    : {g1:.3e}   "
      f"{'PASS' if gk['G1'] else 'FAIL'}")

    g4 = 0.0
    for _ in range(2):
        c = Ctx(px, offset_mask(px.index, "M", 3)[0])
        a = c.run(c.shift(ranked_book(px, 0.75, 20)))[0]
        b = c.run(c.shift(ranked_book(px, 0.75, 20)))[0]
        g4 = max(g4, float(np.abs(a - b).max()))
    gk["G4"] = g4 == 0.0
    P(f"  G4 determinism (TOP20 M phase 3 re-derived twice)          : {g4:.3e}   "
      f"{'PASS' if gk['G4'] else 'FAIL'}")

    bctx = Ctx(px, offset_mask(px.index, "W", 0)[0])
    bg, bt = bctx.run(bctx.shift(w75))
    mv2 = mets((bg - bt * HEAD_COST / 1e4)[WARM:])
    mspy = mets(px["SPY"].pct_change().fillna(0.0).values[WARM:])
    eng = mets(backtest(px, w75, cost_bps=HEAD_COST, freq="W")["returns"]
               .loc[px.index[WARM]:].values)
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
      f"/{mspy['MaxDD']:.4%}; the record's published RULES v2 / SPY constants "
      f"(8.6282%/1.2018/-12.0549%, 15.16%/0.8861/-33.72%) now differ by up to {drift:.3e}, a "
      f"DATA-CACHE drift: 942's own committed grid agrees with this run at 1e-15 (G3).")
    del bctx

    # --------------------------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(B) THE PHASE GRID -- 5 books x 3 panels x 2 gross x (21 M + 63 Q) phases x 5 rungs")
    P("=" * 100)
    ROWS, BASE = [], {}
    for pname, p in panels.items():
        idx = p.index
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(idx >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(idx <= pd.Timestamp(IS_END))[WARM:]
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        bw = rules_v2_weights(p, BAND0, 0.75)                 # the LIVE book, weekly (4a target)
        bc = Ctx(p, offset_mask(idx, "W", 0)[0])
        bgr, btn = bc.run(bc.shift(bw))
        for c in RUNGS:
            br = (bgr - btn * c / 1e4)[WARM:]
            BASE[(pname, c)] = mets(br[oos]) | {"full_MaxDD": maxdd(br)}
        del bc
        Wt = {(b, cs): BOOKS[b](p, g) for b in BOOKS for cs, g in CLAIM_SETS.items()}
        for per, n_ph in (("M", DOM_N), ("Q", DOQ_N)):
            for d in range(n_ph):
                ctx = Ctx(p, offset_mask(idx, per, d)[0])
                for (b, cs), W in Wt.items():
                    gr, tn = ctx.run(ctx.shift(W))
                    gr_w, tn_w = gr[WARM:], tn[WARM:]
                    for c in RUNGS:
                        r = gr_w - tn_w * c / 1e4
                        m, mi, mo = mets(r), mets(r[is_]), mets(r[oos])
                        ROWS.append(dict(
                            panel=pname, book=b, gross=cs, cadence=per, phase=d, cost_bps=c,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                            turn_per_yr=float(tn_w.sum() / (len(r) / 252.0)),
                            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                            spy_H1=ms["H1"], spy_H2=ms["H2"],
                            spy_IS_CAGR=ms_i["CAGR"], spy_IS_Sharpe=ms_i["Sharpe"],
                            spy_IS_MaxDD=ms_i["MaxDD"], spy_IS_H1=ms_i["H1"],
                            spy_IS_H2=ms_i["H2"],
                            spy_OOS_CAGR=ms_o["CAGR"], spy_OOS_Sharpe=ms_o["Sharpe"],
                            spy_OOS_MaxDD=ms_o["MaxDD"], spy_OOS_H1=ms_o["H1"],
                            spy_OOS_H2=ms_o["H2"]))
                del ctx
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(ROWS)
    grid["IS_legs_passed"] = [sum(legs_is(r).values()) for _, r in grid.iterrows()]
    lr = [legs_rec(r) for _, r in grid.iterrows()]
    lp = [legs_pure(r) for _, r in grid.iterrows()]
    grid["pass4b_REC"] = [all(x.values()) for x in lr]
    grid["fail4b_REC"] = [failstr(x) for x in lr]
    grid["pass4b_OOSPURE"] = [all(x.values()) for x in lp]
    grid["fail4b_OOSPURE"] = [failstr(x) for x in lp]
    grid["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                           and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                           and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                      for _, r in grid.iterrows()]
    dump(grid, "grid")
    P(f"  {len(grid):,} grid rows = {len(panels)} panels x {len(BOOKS)} books x "
      f"{len(CLAIM_SETS)} gross x {DOM_N + DOQ_N} phases x {len(RUNGS)} rungs")

    # ---- G3: this run's grid REBUILDS 942's committed grid.csv ------------------------------
    comm = OUT / "2026-09-15_does-the-CANONICAL-PHASE-MAXIMUM-hold-on-OTHER-BOOKS_cloud.grid.csv"
    if comm.exists():
        cg0 = pd.read_csv(comm)
        keys = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2", "turn_per_yr"]
        j = cg0.merge(grid, on=keys, suffixes=("_c", "_n"))
        dmax = max(float(np.abs(j[f"{c}_c"].values - j[f"{c}_n"].values).max()) for c in cols)
        gk["G3"] = (len(j) == len(cg0)) and dmax < 1e-10
        P(f"  G3 942's committed grid.csv replayed on {len(j)} of {len(cg0)} common rows, "
          f"max|d| over 13 columns {dmax:.3e}   {'PASS' if gk['G3'] else 'FAIL'}")
    else:
        gk["G3"] = False
        P("  G3 942's committed grid.csv NOT FOUND -- gate FAILS, nesting unproven")

    # ---- G6: no chooser reads an OOS column -------------------------------------------------
    rng = np.random.default_rng(20260915)
    perm = grid.copy()
    oos_cols = [c for c in perm.columns if c.startswith("OOS_") or c.startswith("spy_OOS")]
    for c in oos_cols:
        perm[c] = rng.permutation(perm[c].values)
    fam = ["panel", "book", "gross", "cadence", "cost_bps"]
    mism = 0
    for k, sub in grid.groupby(fam, sort=False):
        s1 = sub.sort_values("phase")
        s2 = perm.loc[s1.index]
        for ch in CHOOSERS:
            if choose(ch, s1) != choose(ch, s2):
                mism += 1
    gk["G6"] = mism == 0
    P(f"  G6 choosers are IS-ONLY (picks invariant to permuted OOS columns): {mism} mismatches "
      f"of {len(grid.groupby(fam)) * len(CHOOSERS)}   {'PASS' if gk['G6'] else 'FAIL'}")
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failing'})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) RULE 8 WALK-FORWARD -- phase chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    PICKS, FAMS = [], []
    for k, sub in grid.groupby(fam, sort=False):
        s = sub.sort_values("phase").reset_index(drop=True)
        kd = dict(zip(fam, k))
        n = len(s)
        fam_oos_mean = float(np.nanmean(s.OOS_CAGR.values))
        fam_oos_med = float(np.nanmedian(s.OOS_CAGR.values))
        canon = s.iloc[0]
        assert int(canon.phase) == 0
        orc = int(_argmax(s.pass4b_REC.values.astype(float) * 1000 + s.OOS_Sharpe.values))
        FAMS.append(kd | dict(
            n_phases=n, spread_OOS_CAGR_pp=float((np.nanmax(s.OOS_CAGR) - np.nanmin(s.OOS_CAGR))
                                                 * 100),
            spread_IS_CAGR_pp=float((np.nanmax(s.IS_CAGR) - np.nanmin(s.IS_CAGR)) * 100),
            rho_IS_OOS_CAGR=spearman(s.IS_CAGR.values, s.OOS_CAGR.values),
            rho_IS_OOS_Sharpe=spearman(s.IS_Sharpe.values, s.OOS_Sharpe.values),
            n_phases_pass4b_REC=int(s.pass4b_REC.sum()),
            n_phases_pass4b_OOSPURE=int(s.pass4b_OOSPURE.sum()),
            n_phases_pass4a=int(s.pass4a.sum()),
            fam_OOS_CAGR_mean=fam_oos_mean, fam_OOS_CAGR_med=fam_oos_med,
            canon_OOS_CAGR=float(canon.OOS_CAGR), canon_pass4b_REC=bool(canon.pass4b_REC),
            oracle_phase=int(s.phase[orc]), oracle_pass4b_REC=bool(s.pass4b_REC[orc])))
        for src in CHOOSERS + ["CANONICAL", "ORACLE"]:
            i = 0 if src == "CANONICAL" else (orc if src == "ORACLE" else choose(src, s))
            r = s.iloc[i]
            PICKS.append(kd | dict(
                source=src, phase=int(r.phase),
                IS_CAGR=r.IS_CAGR, IS_Sharpe=r.IS_Sharpe, IS_MaxDD=r.IS_MaxDD,
                OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                OOS_H1=r.OOS_H1, OOS_H2=r.OOS_H2,
                pass4b_REC=bool(r.pass4b_REC), fail4b_REC=r.fail4b_REC,
                pass4b_OOSPURE=bool(r.pass4b_OOSPURE), fail4b_OOSPURE=r.fail4b_OOSPURE,
                pass4a=bool(r.pass4a),
                spy_OOS_Sharpe=r.spy_OOS_Sharpe, spy_CAGR=r.spy_CAGR, spy_MaxDD=r.spy_MaxDD,
                base_OOS_Sharpe=BASE[(r.panel, r.cost_bps)]["Sharpe"],
                base_OOS_MaxDD=BASE[(r.panel, r.cost_bps)]["MaxDD"],
                is_canonical=bool(int(r.phase) == 0),
                regret_vs_canon_pp=float((r.OOS_CAGR - canon.OOS_CAGR) * 100),
                regret_vs_fammean_pp=float((r.OOS_CAGR - fam_oos_mean) * 100),
                dd_vs_canon_pp=float((abs(r.OOS_MaxDD) - abs(canon.OOS_MaxDD)) * 100)))
    picks = pd.DataFrame(PICKS)
    fams = pd.DataFrame(FAMS)
    dump(picks, "walkforward")
    dump(fams, "families")

    hv = picks[(picks.cost_bps == HEAD_COST) & (picks.gross == HEAD_GROSS)]
    ch = hv[hv.source.isin(CHOOSERS)]
    cn = hv[hv.source == "CANONICAL"]
    orc_h = hv[hv.source == "ORACLE"]
    P(f"  VERDICT RUNG = {HEAD_COST:.0f} bps, gross {HEAD_GROSS}: {len(ch)} chooser cells "
      f"(6 choosers x 5 books x 3 panels x 2 cadences), {len(cn)} canonical controls.")
    P()
    P("  OOS 4b PASS (record convention) and 4a PASS, by SOURCE:")
    t = (hv.groupby("source")[["pass4b_REC", "pass4b_OOSPURE", "pass4a"]].agg(["sum", "mean"]))
    P(t.to_string(float_format=lambda x: f"{x:.3f}"))
    P()
    P("  OOS 4b PASS rate by BOOK x SOURCE-CLASS (chooser pooled vs canonical vs oracle):")
    cls = hv.assign(klass=np.where(hv.source.isin(CHOOSERS), "CHOOSER", hv.source))
    P(cls.pivot_table(index="book", columns="klass", values="pass4b_REC", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P()
    P("  and by CADENCE x SOURCE-CLASS:")
    P(cls.pivot_table(index="cadence", columns="klass", values="pass4b_REC", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P()

    P("  every chooser cell at the verdict rung, MONTHLY cadence (OOS levels, pp regret):")
    show = ["panel", "book", "source", "phase", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "regret_vs_canon_pp", "dd_vs_canon_pp", "pass4b_REC", "fail4b_REC"]
    P(hv[(hv.cadence == "M") & hv.source.isin(CHOOSERS + ["CANONICAL"])][show]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P()
    P("  the same, QUARTERLY cadence:")
    P(hv[(hv.cadence == "Q") & hv.source.isin(CHOOSERS + ["CANONICAL"])][show]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P()

    # ---- did choosing PAY on levels? --------------------------------------------------------
    beat = float((ch.regret_vs_canon_pp > 0).mean())
    beat_fam = float((ch.regret_vs_fammean_pp > 0).mean())
    P("  DID CHOOSING PAY?  (chooser cell vs the canonical phase of the SAME family)")
    P(f"     chooser OOS CAGR > canonical's in {int((ch.regret_vs_canon_pp > 0).sum())} of "
      f"{len(ch)} cells ({beat:.3f}); > the family MEAN in {beat_fam:.3f}")
    P(f"     mean regret vs canonical {ch.regret_vs_canon_pp.mean():+.3f} pp "
      f"(median {ch.regret_vs_canon_pp.median():+.3f}, min {ch.regret_vs_canon_pp.min():+.3f}, "
      f"max {ch.regret_vs_canon_pp.max():+.3f})")
    P(f"     mean EXTRA OOS drawdown vs canonical {ch.dd_vs_canon_pp.mean():+.3f} pp "
      f"(median {ch.dd_vs_canon_pp.median():+.3f}, max {ch.dd_vs_canon_pp.max():+.3f})")
    P("     by chooser:")
    P(ch.groupby("source")[["regret_vs_canon_pp", "regret_vs_fammean_pp", "dd_vs_canon_pp"]]
      .mean().to_string(float_format=lambda x: f"{x:+.3f}"))
    P()
    n_canon = int((ch.phase == 0).sum())
    P(f"  the choosers land ON the canonical phase in {n_canon} of {len(ch)} cells "
      f"({n_canon / len(ch):.3f}) -- 942 measured 0 of 12 on its own 12-cell slice.")
    P()

    # ---- does IS phase rank predict OOS phase rank? -----------------------------------------
    fh = fams[(fams.cost_bps == HEAD_COST) & (fams.gross == HEAD_GROSS)]
    rho_med = float(np.nanmedian(fh.rho_IS_OOS_CAGR))
    P("  DOES THE IS PHASE RANKING PREDICT THE OOS ONE?  within-family Spearman over phases:")
    P(f"     median rho(IS CAGR, OOS CAGR) {rho_med:+.3f} over {len(fh)} families "
      f"(mean {np.nanmean(fh.rho_IS_OOS_CAGR):+.3f}, "
      f"{float((fh.rho_IS_OOS_CAGR > 0).mean()):.3f} positive); "
      f"Sharpe {np.nanmedian(fh.rho_IS_OOS_Sharpe):+.3f}")
    P(fh.groupby(["book", "cadence"])[["rho_IS_OOS_CAGR", "rho_IS_OOS_Sharpe"]].median()
      .to_string(float_format=lambda x: f"{x:+.3f}"))
    P()

    # ---- which leg binds? --------------------------------------------------------------------
    f_ch = ch[~ch.pass4b_REC]
    dd_alone = float((f_ch.fail4b_REC == "L4_DD").mean()) if len(f_ch) else np.nan
    P("  WHICH LEG KILLS THE CHOSEN PHASE?  failing-leg strings over failing chooser cells "
      f"({len(f_ch)} of {len(ch)}), record convention:")
    P(f_ch.fail4b_REC.value_counts().to_string())
    P(f"     exactly `L4_DD`: {dd_alone:.3f}   (942's claim on its 12-cell slice: all of them)")
    P("  and under the OOSPURE convention:")
    f_p = ch[~ch.pass4b_OOSPURE]
    P(f_p.fail4b_OOSPURE.value_counts().to_string())
    P()

    # ---- could ANY phase have passed? --------------------------------------------------------
    orc_fail = float((~orc_h.pass4b_REC).mean())
    P("  COULD ANY PHASE HAVE PASSED?  (the ORACLE reads OOS and is not a strategy)")
    P(f"     oracle fails 4b in {orc_fail:.3f} of {len(orc_h)} verdict-rung families; "
      f"families with >= 1 passing phase: {int((fh.n_phases_pass4b_REC > 0).sum())} of {len(fh)}")
    pos = fh[fh.n_phases_pass4b_REC > 0]
    if len(pos):
        P(pos[["panel", "book", "cadence", "n_phases", "n_phases_pass4b_REC",
               "canon_pass4b_REC", "oracle_phase"]].to_string(index=False))
    P()
    # ---- the BLIND-RANDOM-PHASE null: how many passes would a coin have found? ---------------
    key3 = ["panel", "book", "cadence"]
    fh3 = fh[key3 + ["n_phases", "n_phases_pass4b_REC"]]
    mm = ch.merge(fh3, on=key3)
    pr = (mm.n_phases_pass4b_REC / mm.n_phases).values          # P(a random phase passes 4b OOS)
    dist = np.array([1.0])
    for q in pr:
        dist = np.convolve(dist, [1 - q, q])                    # exact Poisson-binomial
    exp_blind = float(pr.sum())
    sd_blind = float(np.sqrt((dist * (np.arange(len(dist)) - exp_blind) ** 2).sum()))
    obs = int(ch.pass4b_REC.sum())
    p_le = float(dist[:obs + 1].sum())
    cnm = cn.merge(fh3, on=key3)
    exp_canon = float((cnm.n_phases_pass4b_REC / cnm.n_phases).sum())
    P("  THE BLIND-RANDOM-PHASE NULL -- how many 4b passes would a COIN have found on the same")
    P("  180 cells?  (exact Poisson-binomial over each family's own passing-phase fraction)")
    P(f"     blind expectation {exp_blind:.2f} passes (sd {sd_blind:.2f}); the six IS choosers "
      f"delivered {obs}.  P(X <= {obs} | blind) = {p_le:.4f}")
    P(f"     the CANONICAL phase delivered {int(cn.pass4b_REC.sum())} against a blind expectation "
      f"of {exp_canon:.2f} -- indistinguishable from chance")
    P(f"     inside the {int((fh.n_phases_pass4b_REC > 0).sum())} families where SOME phase "
      f"passes, the choosers hit {int(mm.pass4b_REC.sum())} of {len(mm[mm.n_phases_pass4b_REC > 0])}"
      f" ({mm[mm.n_phases_pass4b_REC > 0].pass4b_REC.mean():.3f}) against a blind rate of "
      f"{float((fh[fh.n_phases_pass4b_REC > 0].n_phases_pass4b_REC / fh[fh.n_phases_pass4b_REC > 0].n_phases).mean()):.3f}")
    P()
    P("  cost-rung robustness -- chooser vs canonical OOS 4b pass rate at every rung (CORE):")
    rr = picks[picks.gross == HEAD_GROSS].assign(
        klass=np.where(picks[picks.gross == HEAD_GROSS].source.isin(CHOOSERS), "CHOOSER",
                       picks[picks.gross == HEAD_GROSS].source))
    P(rr.pivot_table(index="cost_bps", columns="klass", values="pass4b_REC", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P("  and at EXT gross (1.00):")
    re_ = picks[picks.gross == "EXT"].assign(
        klass=np.where(picks[picks.gross == "EXT"].source.isin(CHOOSERS), "CHOOSER",
                       picks[picks.gross == "EXT"].source))
    P(re_.pivot_table(index="cost_bps", columns="klass", values="pass4b_REC", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) VERDICT -- pre-registered bars against the numbers above")
    P("=" * 100)
    r_ch = float(ch.pass4b_REC.mean())
    r_cn = float(cn.pass4b_REC.mean())
    h_surv = (r_ch > SURV_BAR) and (r_ch >= r_cn)
    h_beat = beat >= BEAT_BAR
    h_pred = rho_med >= PRED_BAR
    h_dd = (dd_alone >= DD_BAR) if len(f_ch) else False
    h_oracle = orc_fail >= ORACLE_BAR
    hyp = [("H_SURV", h_surv, f"chooser OOS 4b {r_ch:.3f} ({int(ch.pass4b_REC.sum())} of "
                              f"{len(ch)}) vs canonical {r_cn:.3f} "
                              f"({int(cn.pass4b_REC.sum())} of {len(cn)}); blind null expected "
                              f"{exp_blind:.2f}, P(X<={obs}) = {p_le:.4f}"),
           ("H_BEAT", h_beat, f"chooser OOS CAGR beats canonical in {beat:.3f} of cells, "
                              f"mean regret {ch.regret_vs_canon_pp.mean():+.3f} pp"),
           ("H_PRED", h_pred, f"median within-family Spearman(IS,OOS) CAGR {rho_med:+.3f}"),
           ("H_DD", h_dd, f"exactly `L4_DD` in {dd_alone:.3f} of {len(f_ch)} failing cells"),
           ("H_ORACLE", h_oracle, f"hindsight-best phase fails 4b in {orc_fail:.3f} of "
                                  f"{len(orc_h)} families")]
    hdf = pd.DataFrame([dict(hypothesis=h, supported=bool(v), evidence=e) for h, v, e in hyp])
    P(hdf.to_string(index=False))
    dump(hdf, "hypotheses")
    P()
    P(f"  GATES {sum(gk.values())} of {len(gk)} PASS.  done in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return grid, picks, fams


if __name__ == "__main__":
    main()
