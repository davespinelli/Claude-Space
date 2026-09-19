#!/usr/bin/env python3
"""Idea 1617 (lane C, 2026-09-19): is EVERY eligibility filter the record owns just a
CONSTANT DE-GROSS in disguise, once the twin is matched on REALISED mean gross?

WHY THIS IDEA.  Idea 1586's G10 measured what the inherited MAXVOL 0.60 gate actually does to
the live book: it lowers REALISED mean gross (U56 0.5317 -> 0.5192, SMALL 0.4124 -> 0.3670) and
buys 0.55-1.74 pp of drawdown for 0.54-1.41 pp/yr of CAGR.  That is the exact signature eight
2026-09-19 runs found beaten at matched exposure by a plain constant de-gross (trailing stops,
breadth throttles, vol targeting, MA-distance gates, SPY filters).  Every one of those was a
POSITION-SIZING device.  An ELIGIBILITY FILTER is supposed to be different in kind: it is a
selection claim, not an exposure claim.  This run tests whether the distinction survives contact
with a matched-exposure twin.

THE NULL, STATED BEFORE THE RUN.  Under the live RULES v2 weighting convention (each eligible
name gets GROSS / N_priced of NAV, gated-out weight goes to CASH and is never re-spread), any
filter that removes names MECHANICALLY lowers realised gross.  So the null hypothesis is not
"the filter does nothing" -- it plainly does something -- but:

    H0:  a filter's entire effect on (CAGR, Sharpe, MaxDD) is reproduced by scaling the
         UNFILTERED book by a constant k chosen so the two books carry the SAME REALISED
         MEAN GROSS.

Rejecting H0 for a filter means that filter is a real selection edge.  Failing to reject it for
ALL of them means the record can retire the whole eligibility-filter family in one line, as the
idea asks.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  FAMILY  {MAXVOL, BAND, RANKCUT}   which eligibility filter is switched on
  DIAL 2  RUNG    the filter's own parameter

      BASE                 no filter at all: hold EVERY priced name at GROSS / N_priced.
                           This is the common ANCHOR for all three families and the book that
                           every twin is a scaled copy of.
      MAXVOL   m in {0.45, 0.60, 0.80, 1.00}   eligible iff vol20 < m.  0.60 is the value the
                           frozen incumbent inherited from RULES v1.
      BAND     c in {0.00, 0.03, 0.06, 0.10}   eligible iff `baseline.band_state(px, c)`.
                           c = 0.00 IS the plain 200d MA gate (no hysteresis); c = 0.03 IS the
                           live RULES v2 clause 2 and reproduces `baseline.rules_v2_weights`
                           bit-for-bit (gated at G3).  So this ONE family prices BOTH the 200d
                           gate (0.00 vs BASE) and the band width (0.03/0.06/0.10 vs 0.00).
      RANKCUT  q in {0.25, 0.50, 0.75}         eligible iff the name's composite momentum rank
                           is in the top q of the names priced that day.  Composite = the mean
                           of the cross-sectional pct ranks of the three legs (21,252)/(0,126)/
                           (0,63) -- `baseline.score` without its 200d halving and without its
                           1/sqrt(vol) scaler, so the rank cut is the SCREEN'S OWN cut and
                           nothing else.

  12 cells (1 BASE + 4 + 4 + 3).  Each non-BASE cell is paired with its own DE-GROSS TWIN:
  the BASE book scaled by a constant k solved by bisection so that the twin's REALISED mean
  gross equals the filter's REALISED mean gross to 1e-12.  Matching on REALISED and not on
  TARGET gross is the whole point of the idea -- a gate that is IN 70% of days at target 0.75
  carries realised 0.52, and a twin at target 0.52 does not.

NOT DIALS, published at every value: PANEL {U56, B136, SMALL} (rule 9), COST {0, 10, 25, 50} bps.
  -> 12 cells x 3 panels x 4 cost rungs = 144 rows, each carrying BOTH the filter book and its
     own matched twin, ALL published.

COST IS NOT A DIAL.  Weights are cost-independent, so one run of a cell yields every rung
exactly: r(c) = r_gross - turnover * c / 1e4 (engine.backtest subtracts the charge from the daily
return and never feeds it back into position drift).  That linearity is GATED against a fresh
25 bps engine run (G2), not assumed.  Every KEEP verdict in this file is judged at the protocol's
binding 10 bps.

THE THREE QUESTIONS, STATED BEFORE THE RUN:
  Q1 SURVIVAL.  For each of the 10 non-BASE cells on each panel, does the filter beat its
     matched-exposure twin on FULL Sharpe?  Published as a count over all 33, with dCAGR and
     dMaxDD alongside, at every cost rung.  H0 above predicts ~0 survivors and a dSharpe
     centred on zero.
  Q2 WHICH AXIS.  A filter can lose Sharpe and still be worth holding if it buys DRAWDOWN the
     twin cannot.  So dMaxDD (filter minus twin, positive = shallower) is reported for all 33
     cells separately from dSharpe, and the joint survivor count (dSharpe > 0 AND dMaxDD >= 0)
     is published too.
  Q3 IS ANY OF IT CAPITAL-WORTHY?  Both KEEP paths at every cell, filter AND twin, full and OOS;
     and rule 8.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE  argmax IS Sharpe over all 12 cells                    (the record's usual chooser)
  C_MEMO    among cells whose IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
            the LOWEST-TURNOVER one (the cheapest admissible book); else BASE.  This is the
            2026-09-03 RECOMMENDATION memo's OWN pre-registered DD-aware admission rule, with
            its 'smallest' tie-break, carried onto this dial unchanged
  C_LIVE    the live inheritance, choosing nothing: BAND c = 0.03
  C_BASE    the no-filter anchor, choosing nothing: BASE
  Each chooser's pick is then read OOS against (a) SPY, (b) the live RULES v2 baseline and
  (c) its OWN matched twin, whose k is re-solved on IS GROSS ONLY so the twin is legal too.

WHAT WOULD MAKE THIS A FINDING.  If 0 of 33 filters beat their matched twin, the record can say
in one line that eligibility filters are exposure dials in costume and stop pricing them one at
a time.  If some family survives, it is the first selection claim in the record that is not a
de-gross, and it deserves its own memo.  Both outcomes are reported; nothing is tuned until it
works.

GATES.  G0 sample >= 10y (rule 1).  G1 fast_run vs `engine.backtest` (returns AND turnover) on
BASE and on the live BAND 0.03 book, every panel.  G2 the DERIVED 25 bps rung vs a fresh 25 bps
engine run.  G3 BAND c = 0.03 on U56 replays `baseline.compare`'s RULES v2 baseline row.  G4 the
gross match: max |mean_gross(twin) - mean_gross(filter)| over all cells.  G5 exactly two tuned
parameters (12 cells).  G6 no chooser reads a row on or after 2017-01-01 (asserted by
construction AND tested on truncated IS input).  G7 144 of 144 rows published.  G8 no leverage,
no shorting: max realised target gross <= 0.75.  G9 PUBLISHED, not asserted: turnover per cell,
filter and twin, and the drag it implies.  G10 PUBLISHED: realised mean gross and mean names
held per cell.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_is-every-eligibility-filter-a-degross-in-disguise_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "is-every-eligibility-filter-a-degross-in-disguise"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
GROSS = 0.75
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

CELLS = ([("BASE", 0.0)]
         + [("MAXVOL", m) for m in (0.45, 0.60, 0.80, 1.00)]
         + [("BAND", c) for c in (0.00, 0.03, 0.06, 0.10)]
         + [("RANKCUT", q) for q in (0.25, 0.50, 0.75)])
LIVE_CELL = ("BAND", 0.03)
BASE_CELL = ("BASE", 0.0)


def lab(cell):
    f, p = cell
    return "BASE" if f == "BASE" else f"{f} {p:.2f}"


LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- panel
class Panel:
    """One price panel plus every eligibility input, all computed on the TRADED column set."""

    def __init__(self, name, px, cols):
        self.name, self.px, self.cols = name, px, list(cols)
        allc = list(px.columns)
        self.icol = np.array([allc.index(c) for c in self.cols])
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        q = px[self.cols]
        self.priced = q.notna().values
        v = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.vol20 = np.nan_to_num(v, nan=1e9)                       # NaN vol -> never eligible
        self.bands = {c: band_state(q, c).values for c in (0.00, 0.03, 0.06, 0.10)}
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts))
        # top-q rank cut AMONG THE NAMES PRICED THAT DAY: pct rank of the composite, descending
        self.rankpct = comp.rank(axis=1, ascending=False, pct=True).values
        self.rankok = np.isfinite(self.rankpct)
        self.reb = self._reb(CADENCE)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))

    def _reb(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)

    def elig(self, cell):
        f, p = cell
        if f == "BASE":
            return self.priced
        if f == "MAXVOL":
            return self.priced & (self.vol20 < p)
        if f == "BAND":
            return self.priced & self.bands[p]
        if f == "RANKCUT":
            return self.priced & self.rankok & (np.nan_to_num(self.rankpct, nan=9.9) <= p)
        raise ValueError(f)

    def frame(self, cell):
        """Target weights at GROSS = 1.0, shifted one row so row t carries the close-(t-1)
        decision -- exactly engine.backtest's `weights.shift(1)` convention."""
        T, M = self.rets.shape
        e = self.elig(cell).astype(float)
        n = self.priced.sum(axis=1).astype(float)     # N = names PRICED, the live convention
        w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
        w = np.nan_to_num(w, nan=0.0)
        W = np.zeros((T, M))
        W[:, self.icol] = w
        return np.vstack([np.zeros((1, M)), W[:-1]])


def run_cell(pan, frame, g=GROSS):
    """Hold g * frame on the weekly schedule, drift between rebalances, de-gross to 0%-yielding
    cash.  Returns GROSS-OF-COST daily returns, the turnover path, max realised target gross and
    the realised gross path -- identical semantics to engine.backtest, gated at G1."""
    rets = pan.rets
    T, M = rets.shape
    reb = pan.reb
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


def solve_k(pan, base_frame, target_mean_gross, lo, hi, cache):
    """Bisect the constant scaler k so that the BASE book at gross k*GROSS carries the SAME
    REALISED mean gross as the filtered book over slice [lo:hi).  Realised gross is monotone
    increasing in k, so bisection is exact to machine precision in 60 halvings."""
    a, b = 0.0, 1.0
    for _ in range(60):
        k = 0.5 * (a + b)
        key = round(k, 15)
        if key not in cache:
            cache[key] = run_cell(pan, base_frame, g=k * GROSS)
        gm = float(np.mean(cache[key][3][lo:hi]))
        if gm < target_mean_gross:
            a = k
        else:
            b = k
    k = 0.5 * (a + b)
    if round(k, 15) not in cache:
        cache[round(k, 15)] = run_cell(pan, base_frame, g=k * GROSS)
    return k, cache[round(k, 15)]


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE book (rule 4a), 4b against SPY (rule 4b).  Legs published."""
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1617 (lane C, 2026-09-19) — is EVERY eligibility filter in the record a CONSTANT")
    say("DE-GROSS in disguise, once its twin is matched on REALISED (not target) mean gross?")
    say(f"DIALS: FAMILY {{MAXVOL, BAND, RANKCUT}} x RUNG  ->  {len(CELLS)} cells incl. the BASE anchor.")
    say(f"NOT DIALS, all published: PANEL [U56, B136, SMALL] x COST {COSTS} bps.  Gross {GROSS}, "
        f"weekly cadence, t+1 execution, gated-out weight to 0%-yielding CASH.")
    say("H0: a filter's whole effect is reproduced by scaling the UNFILTERED book to the same")
    say("    REALISED mean gross.  Rejecting H0 = the filter is a real selection edge.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} of {len(pxS.columns)-1} priced names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns]),
              Panel("B136", pxB, [c for c in pxB.columns]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names + SPY, B136 {len(pxB.columns)-1} + SPY, "
        f"SMALL {len(inv)} (SPY is a joined BENCHMARK there, not a constituent, so it is NOT "
        f"traded on SMALL; on U56/B136 it IS a universe constituent and the live book holds it).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND.  "
        "The headline is a FILTER-minus-TWIN contrast inside one panel, over the same names on "
        "the same days at the same realised exposure, so it is first-order immune; the 4b pass "
        "counts are not.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)  OOS starts row {p.i_oos} ({p.idx[p.i_oos].date()})")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned parameters (FAMILY x RUNG)",
         f"{len(CELLS)} cells = 1 BASE + 4 MAXVOL + 4 BAND + 3 RANKCUT", "2 dials",
         len(CELLS) == 12)

    # ------------------------------------------------ G1 / G2: fast_run vs the engine
    say("\n  [G1/G2] fast_run vs engine.backtest (returns AND turnover), BASE and live BAND 0.03")
    d1r = d1t = d2 = 0.0
    for pan in panels:
        fr = pan.frame(LIVE_CELL)
        rg, tu, _, _ = run_cell(pan, fr)
        W = (rules_v2_weights(pan.px[pan.cols], gross=GROSS)
             .reindex(pan.idx).fillna(0.0).reindex(columns=pan.px.columns).fillna(0.0))
        eng = backtest(pan.px, W, cost_bps=BIND, freq=CADENCE)
        eng25 = backtest(pan.px, W, cost_bps=25.0, freq=CADENCE)
        d1r = max(d1r, float(np.max(np.abs((rg - tu * BIND / 1e4) - eng["returns"].values))))
        d1t = max(d1t, float(np.max(np.abs(tu - eng["turnover"].values))))
        d2 = max(d2, float(np.max(np.abs((rg - tu * 25.0 / 1e4) - eng25["returns"].values))))
        # BASE: hold every priced name at GROSS/N -> build the same weights the slow way
        e = pd.DataFrame(1.0, index=pan.idx, columns=pan.cols).where(pan.px[pan.cols].notna(), 0.0)
        WB = (GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
              .reindex(columns=pan.px.columns).fillna(0.0))
        rgB, tuB, _, _ = run_cell(pan, pan.frame(BASE_CELL))
        engB = backtest(pan.px, WB, cost_bps=BIND, freq=CADENCE)
        d1r = max(d1r, float(np.max(np.abs((rgB - tuB * BIND / 1e4) - engB["returns"].values))))
        d1t = max(d1t, float(np.max(np.abs(tuB - engB["turnover"].values))))
    gate("G1 fast_run vs engine.backtest, RETURNS (max |dev| over 6 panel x book runs)",
         f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12",
         d1t < 1e-12)
    gate("G2 DERIVED 25 bps rung vs a fresh 25 bps engine run (max |dev|)", f"{d2:.3e}",
         "< 1e-12", d2 < 1e-12)

    rows, wsum_global, gapmax = [], 0.0, 0.0
    ISPK, BARS, RET = {}, {}, {}
    g3row = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = pan.i_oos
        spy = bmpack(pan.spy[WARMUP:])
        spyO = bmpack(pan.spy[i_oos:])
        spyI = bmpack(pan.spy[WARMUP:i_oos])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=BIND, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        BARS[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO)
        g3row[pan.name] = live
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}"
            f"  H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%},"
            f" CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}"
            f"  |  OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%}  H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  (OOS "
            f"{liveO['CAGR']:.2%} / {liveO['Sharpe']:.4f} / {liveO['MaxDD']:.2%})")

        base_frame = pan.frame(BASE_CELL)
        kcache: dict = {}
        rgB, tuB, wsB, gsB = run_cell(pan, base_frame)
        kcache[round(1.0, 15)] = (rgB, tuB, wsB, gsB)
        yrs = (T - WARMUP) / 252.0

        for cell in CELLS:
            fm = pan.frame(cell)
            rg, tu, ws, gs = run_cell(pan, fm)
            wsum_global = max(wsum_global, ws)
            nheld = float(np.mean((fm[WARMUP:] > 0).sum(axis=1)))
            gf_full = float(np.mean(gs[WARMUP:]))
            gf_is = float(np.mean(gs[WARMUP:i_oos]))
            if cell == BASE_CELL:
                kF, (rgT, tuT, _, gsT) = 1.0, (rgB, tuB, wsB, gsB)
                kI, twinI = 1.0, (rgB, tuB, wsB, gsB)
            else:
                kF, (rgT, tuT, _, gsT) = solve_k(pan, base_frame, gf_full, WARMUP, T, kcache)
                kI, twinI = solve_k(pan, base_frame, gf_is, WARMUP, i_oos, kcache)
            gapmax = max(gapmax, abs(float(np.mean(gsT[WARMUP:])) - gf_full),
                         abs(float(np.mean(twinI[3][WARMUP:i_oos])) - gf_is))
            nheldT = float(np.mean((base_frame[WARMUP:] > 0).sum(axis=1)))

            for c in COSTS:
                r = rg - tu * c / 1e4
                rT = rgT - tuT * c / 1e4
                rTI = twinI[0] - twinI[1] * c / 1e4
                RET[(pan.name, cell, c)] = r
                k4a, k4b, mt, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                t4a, t4b, tmt, th1, th2, _ = keep_paths(rT[WARMUP:], spy, live)
                t4aO, t4bO, tmo, _, _, _ = keep_paths(rTI[i_oos:], spyO, liveO)
                if c == BIND:
                    ISPK.setdefault(pan.name, {})[cell] = dict(
                        Sharpe=sharpe(r[WARMUP:i_oos]), CAGR=cagr(r[WARMUP:i_oos]),
                        MaxDD=mdd(r[WARMUP:i_oos]), turn=float(tu[WARMUP:i_oos].sum()),
                        kI=kI, oSharpe=sharpe(r[i_oos:]), oCAGR=cagr(r[i_oos:]),
                        oMaxDD=mdd(r[i_oos:]), tw_oSharpe=sharpe(rTI[i_oos:]),
                        tw_oCAGR=cagr(rTI[i_oos:]), tw_oMaxDD=mdd(rTI[i_oos:]),
                        tw_isSharpe=sharpe(rTI[WARMUP:i_oos]),
                        keep4b_oos=k4bO, keep4a_oos=k4aO, tw_keep4b_oos=t4bO)
                rows.append(dict(
                    panel=pan.name, family=cell[0], rung=("" if cell[0] == "BASE" else f"{cell[1]:.2f}"),
                    cell=lab(cell), cost_bps=c,
                    CAGR=mt["CAGR"], Sharpe=mt["Sharpe"], MaxDD=mt["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    isSharpe=sharpe(r[WARMUP:i_oos]), isCAGR=cagr(r[WARMUP:i_oos]),
                    isMaxDD=mdd(r[WARMUP:i_oos]),
                    k_full=kF, k_is=kI,
                    tw_CAGR=tmt["CAGR"], tw_Sharpe=tmt["Sharpe"], tw_MaxDD=tmt["MaxDD"],
                    tw_H1=th1, tw_H2=th2,
                    tw_oCAGR=tmo["CAGR"], tw_oSharpe=tmo["Sharpe"], tw_oMaxDD=tmo["MaxDD"],
                    dSharpe=mt["Sharpe"] - tmt["Sharpe"], dCAGR=mt["CAGR"] - tmt["CAGR"],
                    dMaxDD=mt["MaxDD"] - tmt["MaxDD"],
                    odSharpe=mo["Sharpe"] - tmo["Sharpe"], odCAGR=mo["CAGR"] - tmo["CAGR"],
                    odMaxDD=mo["MaxDD"] - tmo["MaxDD"],
                    mean_gross=gf_full, tw_mean_gross=float(np.mean(gsT[WARMUP:])),
                    mean_names=nheld, tw_mean_names=nheldT,
                    turnover_yr=float(tu[WARMUP:].sum() / yrs),
                    tw_turnover_yr=float(tuT[WARMUP:].sum() / yrs),
                    drag_bpyr=float(tu[WARMUP:].sum() / yrs) * c,
                    keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                    tw_keep4a=t4a, tw_keep4b=t4b, tw_keep4b_oos=t4bO,
                    leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                    oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                    oleg_CAGR=legsO["CAGR"],
                    is_base=bool(cell == BASE_CELL), is_live=bool(cell == LIVE_CELL)))
        say(f"    [{pan.name}] {len(CELLS)} cells x {len(COSTS)} cost rungs done, twins solved "
            f"({time.time()-t0:.0f}s elapsed)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G7 every cell published", f"{len(G)} rows in {Path(OUT).name}.grid.csv",
         f"{3*len(CELLS)*len(COSTS)} = 3 panels x {len(CELLS)} cells x {len(COSTS)} rungs",
         len(G) == 3 * len(CELLS) * len(COSTS))
    gate("G8 no leverage, no shorting (max realised target gross)", f"{wsum_global:.4f}",
         f"<= {GROSS:.4f}", wsum_global <= GROSS + 1e-12)
    gate("G4 REALISED-gross match |mean_gross(twin) - mean_gross(filter)|, max over all cells "
         "and both windows", f"{gapmax:.3e}", "< 1e-9", gapmax < 1e-9)

    lv = G[(G.panel == "U56") & (G.cell == lab(LIVE_CELL)) & (G.cost_bps == BIND)].iloc[0]
    b = g3row["U56"]
    d3 = max(abs(lv["CAGR"] - b["CAGR"]), abs(lv["Sharpe"] - b["Sharpe"]),
             abs(lv["MaxDD"] - b["MaxDD"]), abs(lv["H1"] - b["H1"]), abs(lv["H2"] - b["H2"]))
    gate("G3 BAND 0.03 on U56 replays baseline.compare's RULES v2 row", f"{d3:.3e}",
         "< 1e-12 (it IS the same book)", d3 < 1e-12)

    # ------------------------------------------------ Q1 / Q2: the census
    say("\n" + "=" * 118)
    say("Q1/Q2  FILTER vs ITS MATCHED-EXPOSURE TWIN — every non-BASE cell, every panel, @10 bps")
    say("=" * 118)
    say(f"  {'panel':6s} {'cell':14s} {'gross':>7s} {'twin k':>7s} {'CAGR':>8s} {'twin':>8s} "
        f"{'dCAGR':>8s} {'Sharpe':>8s} {'twin':>8s} {'dSh':>8s} {'MaxDD':>8s} {'twin':>8s} "
        f"{'dDD':>7s} {'turn':>6s} {'twin':>6s}")
    B = G[G.cost_bps == BIND]
    for pan in ["U56", "B136", "SMALL"]:
        for cell in CELLS:
            r = B[(B.panel == pan) & (B.cell == lab(cell))].iloc[0]
            mark = "  <-BASE" if r["is_base"] else ("  <-LIVE" if r["is_live"] else "")
            say(f"  {pan:6s} {r['cell']:14s} {r['mean_gross']:7.4f} {r['k_full']:7.4f} "
                f"{r['CAGR']:8.2%} {r['tw_CAGR']:8.2%} {r['dCAGR']:+8.2%} "
                f"{r['Sharpe']:8.4f} {r['tw_Sharpe']:8.4f} {r['dSharpe']:+8.4f} "
                f"{r['MaxDD']:8.2%} {r['tw_MaxDD']:8.2%} {r['dMaxDD']:+7.2%} "
                f"{r['turnover_yr']:6.2f} {r['tw_turnover_yr']:6.2f}{mark}")

    NB = B[~B.is_base]
    say("")
    for c in COSTS:
        S = G[(G.cost_bps == c) & (~G.is_base)]
        say(f"  COST {c:>4.0f} bps : FULL dSharpe > 0 in {int((S.dSharpe > 0).sum())} of {len(S)}"
            f" | dMaxDD >= 0 (shallower) in {int((S.dMaxDD >= 0).sum())} of {len(S)}"
            f" | JOINT (both) {int(((S.dSharpe > 0) & (S.dMaxDD >= 0)).sum())} of {len(S)}"
            f" | mean dSharpe {S.dSharpe.mean():+.4f}  mean dCAGR {S.dCAGR.mean():+.4%}"
            f"  mean dMaxDD {S.dMaxDD.mean():+.2%}")
    say("")
    for fam in ["MAXVOL", "BAND", "RANKCUT"]:
        S = NB[NB.family == fam]
        say(f"  FAMILY {fam:8s} @10bps: dSharpe > 0 in {int((S.dSharpe > 0).sum())} of {len(S)}"
            f"  mean {S.dSharpe.mean():+.4f}  [min {S.dSharpe.min():+.4f}, max {S.dSharpe.max():+.4f}]"
            f"  |  mean dCAGR {S.dCAGR.mean():+.4%}  mean dMaxDD {S.dMaxDD.mean():+.2%}"
            f"  |  OOS dSharpe > 0 in {int((S.odSharpe > 0).sum())} of {len(S)}")
    say("")
    say(f"  OOS (2017-2026, twin k re-solved on IS gross only): dSharpe > 0 in "
        f"{int((NB.odSharpe > 0).sum())} of {len(NB)}  mean {NB.odSharpe.mean():+.4f}")

    # ------------------------------------------------ Q3: KEEP paths
    say("\n" + "=" * 118)
    say("Q3  BOTH KEEP PATHS (rule 4), every cell, filter AND twin, @10 bps binding")
    say("=" * 118)
    say(f"  4a (beat the live book, both halves + MaxDD): FILTER {int(B.keep4a.sum())} of {len(B)}"
        f"  |  TWIN {int(B.tw_keep4a.sum())} of {len(B)}")
    say(f"  4b (beat SPY, both halves + DD cap + CAGR floor), FULL: FILTER {int(B.keep4b.sum())}"
        f" of {len(B)}  |  TWIN {int(B.tw_keep4b.sum())} of {len(B)}")
    say(f"  4b OOS: FILTER {int(B.keep4b_oos.sum())} of {len(B)}  |  TWIN "
        f"{int(B.tw_keep4b_oos.sum())} of {len(B)}")
    say(f"  4b FULL *and* OOS (the bar a capital-worthy book must clear): "
        f"{int((B.keep4b & B.keep4b_oos).sum())} of {len(B)}")
    for _, r in B[B.keep4b & B.keep4b_oos].iterrows():
        say(f"      PASS  {r['panel']:6s} {r['cell']:14s} FULL {r['CAGR']:.2%}/{r['Sharpe']:.4f}/"
            f"{r['MaxDD']:.2%} H1/H2 {r['H1']:.3f}/{r['H2']:.3f}  OOS {r['oCAGR']:.2%}/"
            f"{r['oSharpe']:.4f}/{r['oMaxDD']:.2%}  |  TWIN at the SAME realised gross "
            f"{r['tw_CAGR']:.2%}/{r['tw_Sharpe']:.4f}/{r['tw_MaxDD']:.2%} -> 4b FULL "
            f"{bool(r['tw_keep4b'])}, OOS {bool(r['tw_keep4b_oos'])}")
    for c in COSTS:
        S = G[G.cost_bps == c]
        say(f"  cost {c:>4.0f} bps: 4a {int(S.keep4a.sum())} of {len(S)} | 4b FULL "
            f"{int(S.keep4b.sum())} | 4b FULL+OOS {int((S.keep4b & S.keep4b_oos).sum())}")
    say("  4b LEG FAILURES @10bps (why the passes are not passes), counted over all "
        f"{len(B)} cells: H1 {int((~B.leg_H1).sum())}, H2 {int((~B.leg_H2).sum())}, "
        f"DD {int((~B.leg_DD).sum())}, CAGR {int((~B.leg_CAGR).sum())}")

    # ------------------------------------------------ rule 8
    say("\n" + "=" * 118)
    say("RULE 8  WALK-FORWARD — parameters chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE")
    say("=" * 118)
    wf = []
    for pan in panels:
        p = ISPK[pan.name]
        si = BARS[pan.name]["spyI"]
        ok = [c for c in CELLS if p[c]["MaxDD"] >= DD_CAP * si["MaxDD"]
              and p[c]["CAGR"] >= CAGR_FLOOR * si["CAGR"]]
        memo = min(ok, key=lambda c: (p[c]["turn"], CELLS.index(c))) if ok else BASE_CELL
        picks = dict(
            C_SHARPE=max(CELLS, key=lambda c: (p[c]["Sharpe"], -CELLS.index(c))),
            C_MEMO=memo, C_LIVE=LIVE_CELL, C_BASE=BASE_CELL)
        bo, so = BARS[pan.name]["liveO"], BARS[pan.name]["spyO"]
        say(f"    C_MEMO admissible set on IS (MaxDD >= {DD_CAP*si['MaxDD']:.2%}, CAGR >= "
            f"{CAGR_FLOOR*si['CAGR']:.2%}): "
            f"{', '.join(lab(c) for c in ok) if ok else 'EMPTY -> falls back to BASE'}")
        say(f"\n  [{pan.name}]  live RULES v2 OOS Sharpe {bo['Sharpe']:.4f} | SPY OOS Sharpe "
            f"{so['Sharpe']:.4f}")
        for nm, cell in picks.items():
            d = p[cell]
            say(f"    {nm:9s} picks {lab(cell):14s} (IS Sharpe {d['Sharpe']:.4f})  ->  OOS "
                f"{d['oCAGR']:7.2%} / {d['oSharpe']:.4f} / {d['oMaxDD']:7.2%}   vs its MATCHED "
                f"TWIN (k_IS {d['kI']:.4f}) {d['tw_oCAGR']:7.2%} / {d['tw_oSharpe']:.4f} / "
                f"{d['tw_oMaxDD']:7.2%}   dSharpe {d['oSharpe']-d['tw_oSharpe']:+.4f}"
                f"   4b OOS {'PASS' if d['keep4b_oos'] else 'fail'}"
                f" (twin {'PASS' if d['tw_keep4b_oos'] else 'fail'})")
            wf.append(dict(panel=pan.name, chooser=nm, pick=lab(cell), isSharpe=d["Sharpe"],
                           oCAGR=d["oCAGR"], oSharpe=d["oSharpe"], oMaxDD=d["oMaxDD"],
                           k_is=d["kI"], tw_oCAGR=d["tw_oCAGR"], tw_oSharpe=d["tw_oSharpe"],
                           tw_oMaxDD=d["tw_oMaxDD"], d_oSharpe=d["oSharpe"] - d["tw_oSharpe"],
                           live_oSharpe=bo["Sharpe"], spy_oSharpe=so["Sharpe"],
                           beats_live=bool(d["oSharpe"] > bo["Sharpe"]),
                           beats_spy=bool(d["oSharpe"] > so["Sharpe"]),
                           keep4b_oos=d["keep4b_oos"], keep4a_oos=d["keep4a_oos"],
                           tw_keep4b_oos=d["tw_keep4b_oos"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    for nm in ["C_SHARPE", "C_MEMO", "C_LIVE", "C_BASE"]:
        S = W[W.chooser == nm]
        say(f"  POOLED {nm:9s}: mean OOS Sharpe {S.oSharpe.mean():.4f}  | beats its matched twin "
            f"in {int((S.d_oSharpe > 0).sum())} of {len(S)} (mean {S.d_oSharpe.mean():+.4f})"
            f"  | beats live in {int(S.beats_live.sum())} of {len(S)}"
            f"  | beats SPY in {int(S.beats_spy.sum())} of {len(S)}"
            f"  | 4b OOS {int(S.keep4b_oos.sum())} of {len(S)}")
    cs, cb = W[W.chooser == "C_SHARPE"], W[W.chooser == "C_BASE"]
    say(f"  TUNING VALUE: C_SHARPE minus C_BASE pooled mean OOS Sharpe "
        f"{cs.oSharpe.mean()-cb.oSharpe.mean():+.4f} over {len(cs)} panels — i.e. choosing a "
        f"filter on IS rows is worth this much out of sample relative to choosing NO filter.")

    # G6: the choosers are IS-only, tested and not merely asserted
    say("\n  [G6] IS-only test: re-derive C_SHARPE from a TRUNCATED IS input (rows >= 2017 "
        "deleted, not masked) and check the pick is identical")
    same = True
    for pan in panels:
        p = ISPK[pan.name]
        a = max(CELLS, key=lambda c: (p[c]["Sharpe"], -CELLS.index(c)))
        trunc = {}
        for cell in CELLS:
            r = RET[(pan.name, cell, BIND)][:pan.i_oos]
            trunc[cell] = sharpe(r[WARMUP:])
        b2 = max(CELLS, key=lambda c: (trunc[c], -CELLS.index(c)))
        same = same and (a == b2)
    gate("G6 chooser reads no row on or after 2017-01-01 (tested on truncated input)",
         f"identical pick on {len(panels)} of {len(panels)} panels", "identical", same)
    publish("G9 turnover per cell (filter and twin)", "turnover_yr / tw_turnover_yr in .grid.csv")
    publish("G10 realised mean gross and mean names held per cell",
            "mean_gross / tw_mean_gross / mean_names / tw_mean_names in .grid.csv")

    gd = pd.DataFrame(GATES)
    gd.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gd.pass_.sum())
    say(f"\n  GATES {npass}/{len(gd)} pass ({int((~gd.pass_).sum())} fail)")
    say(f"\n  DONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return G, W


if __name__ == "__main__":
    main()
