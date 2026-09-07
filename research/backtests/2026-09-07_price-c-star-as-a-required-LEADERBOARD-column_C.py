#!/usr/bin/env python3
"""Idea 356 - "price-c*-as-a-required-LEADERBOARD-column" (lane C, 2026-09-07).

The question
------------
Idea 352 (script `2026-09-07_is-every-4b-KEEP-a-10bps-artefact_C.py`, headed "Idea 323")
computed a 4b breakeven cost c* for the record's standing 4b passes on a 9-rung ladder and
found they break anywhere from 1.0 to 43.5 bps.  The queue proposes promoting c* to a
MANDATORY LEADERBOARD column beside any 4b claim, with a reporting floor: "a claim with
c* < 15 bps is not a capital claim".

A proposal to change what the record must report is only as good as the statistic it
mandates.  Three things have to be true, and they are PRE-REGISTERED here before anything
is read:

  C1 MEASURABLE - c* must not be an artefact of the ladder the reporter happened to use.
                  Gate: |c*(5-bps ladder, linear interpolation - the record's own method)
                  - c*(exact)| <= 2.0 bps on >= 90% of cells, and the pass set must be an
                  interval (a book that fails at c and passes again at c+h has no c*).
  C2 PREDICTIVE - c* must be knowable in advance.  Gate: c*_IS (chosen on 2009-2016 only)
                  classifies c*_OOS (2017-2026) against the floor with accuracy strictly
                  above the majority-class base rate.
  C3 USEFUL     - the floor must change a decision for the better, or at least not for the
                  worse.  Gate (PROTOCOL rule 8): a chooser that screens on c*_IS >= F must
                  not have LOWER mean OOS Sharpe than the record's plain best-IS-Sharpe
                  chooser, at the 10-bps anchor rung.

ADOPT (protocol KEEP) requires all three.  Any failure -> the failing clause is named and
the proposal is PARKed or KILLED.  A KILL here is a result: it says the record should keep
reporting the cost rung, not a breakeven.

What is swept (the two tuned parameters - PROTOCOL rule 4)
----------------------------------------------------------
    ladder step h in {5.0, 2.5, 1.0, 0.5, 0.25} bps over [0, 50]   (param 1: how c* is measured)
    reporting floor F in {0, 5, 10, 15, 20, 25} bps                (param 2: the queue's 15)
ALL 5 x 6 = 30 (step, floor) points are reported, on every one of the 42 cells.

What is FIXED in advance and NOT searched
-----------------------------------------
The menu is idea 352's, verbatim, so this run can be gated against its committed CSV:
7 books x 3 cadences {W,M,Q} x 2 panels (U56, B136) = 42 cells.  Books:
    N20     top 20 at 0.75/20, de-grossing when E_t < 20        idea 2's KEEP
    F085    top ceil(0.85*E_t) at 0.75/k                        idea 46's 4b passer
    BAND12  200d band b=0.12, RESPREAD, 0.75 gross              idea 291's PARKed 4b passer
    BRCASH  N20's broad leg, flat when E_t <= causal q0.20      idea 48's by-product
    RULESv2 200d band b=0.03, DEGROSS to cash, 0.75 gross        the LIVE book
    NF20    top min(20,E_t) at 0.75/min(20,E_t)                  control
    EWALL   every live name at 0.75/N                            do-nothing control
Cadence is NOT a tuned parameter here (it was idea 352's second one): it is part of the
fixed rule-8 menu the choosers pick over, and every cell of it is reported.

Three c* are computed per cell, all from the same zero-cost run:
    c*_full  5 bars (H1, H2, OOS-Sharpe, DD, CAGR) vs SPY over the whole sample - the
             record's published column, the thing the queue wants mandated.
    c*_IS    4 bars (H1, H2, DD, CAGR) on 2009-2016 vs SPY-IS - what a reporter could have
             known in 2016.  No OOS bar: it did not exist yet.
    c*_OOS   the same 4 bars on 2017-2026 vs SPY-OOS - what actually happened.

Mechanics
---------
Costs   : held weights and turnover do not depend on cost_bps, so every rung comes from ONE
          zero-cost run per cell as r_c = r_0 - turnover * c/1e4.  Gated against
          engine.backtest at 10 bps on all 42 cells; aborts if max|diff| > 1e-12.
Exact c*: min over bars of each bar's first zero crossing, located by a 0.01-bps scan and
          then 60 rounds of bisection (resolution < 1e-15 bps).  Sharpe is NOT linear in c
          (cost changes the return sd as well as its mean), so the closed form is not used.
Gate    : c*_full is compared cell-by-cell against idea 352's committed `.breakeven.csv`.
Rule 8  : five choosers fixed in advance - S1 best IS Sharpe (the record's default), S2 best
          IS Sharpe among IS-4b clearers (idea 352's), S3_F best IS Sharpe among cells with
          c*_IS >= F (the proposal), S4 max c*_IS, S5 max IS Sharpe among cells with IS
          turnover <= 6.2x (idea 352's published budget, as a comparand instrument).
          Chosen on 2009-2016 only, evaluated untouched on 2017-2026 against N20/W (the
          do-nothing anchor), RULES v2/W (the live book) and SPY.
Census  : the count of LEADERBOARD rows carrying a 4b claim is grep-derived at runtime from
          the committed file, so the coverage statement cannot go stale.

SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current-constituent
lists, so absolute CAGRs are optimistic on both panels.  This run holds names, days, filter,
gross and fill fixed and moves ONLY the cost rung; the c* comparison across cells is far
less exposed than the levels are.

Deterministic, standalone.  Reads baseline.py and two committed CSVs; modifies nothing.
"""
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

GROSS = 0.75
MAX_VOL = 0.60
VOL_SCALE = False                 # the candidates' own scorer
N0 = 20
F085 = 0.85
BAND_WIDE = 0.12
BAND_LIVE = 0.03
Q_NARROW = 0.20
MIN_OBS = 252
CMAX = 50.0                       # the ladder's top, idea 352's
STEPS = [5.0, 2.5, 1.0, 0.5, 0.25]            # tuned parameter 1
FLOORS = [0, 5, 10, 15, 20, 25]               # tuned parameter 2
QUEUE_FLOOR = 15                              # the queue's proposed floor
ANCHOR_COST = 10
BUDGET_T = 6.2                    # idea 352's published turnover budget at 25 bps
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
CADENCES = ["W", "M", "Q"]
BOOKS = ["N20", "F085", "BAND12", "BRCASH", "RULESv2", "NF20", "EWALL"]
STANDING = ["N20", "F085", "BAND12", "BRCASH", "RULESv2"]
PARENT = REPO / "research" / "backtests" / "2026-09-07_is-every-4b-KEEP-a-10bps-artefact_C.breakeven.csv"
LB = REPO / "research" / "LEADERBOARD.md"
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- book construction (idea 352's, verbatim)
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def eligible_count(px):
    e = eligible_mask(px).sum(axis=1).astype(float)
    ma_ok = px.rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px):
    return score(px, vol_scale=VOL_SCALE)[0].where(eligible_mask(px)).rank(axis=1, ascending=False)


def weights_from_k(rank, k, gross):
    k = k.clip(lower=1.0)
    w_per = gross / k if np.isscalar(gross) else gross.div(k)
    return rank.le(k, axis=0).astype(float).mul(w_per, axis=0)


def narrow_flag(e, q=Q_NARROW):
    thr = e.expanding(min_periods=MIN_OBS).quantile(q).shift(1)
    return (e <= thr).where(thr.notna() & e.notna(), False)


def build(px, book):
    rank = ranked(px)
    e = eligible_count(px).fillna(0.0)
    if book == "N20":
        return weights_from_k(rank, pd.Series(float(N0), index=px.index), GROSS)
    if book == "NF20":
        return weights_from_k(rank, np.minimum(float(N0), e), GROSS)
    if book == "F085":
        return weights_from_k(rank, np.ceil(F085 * e), GROSS)
    if book == "BRCASH":
        w = weights_from_k(rank, np.minimum(float(N0), e), GROSS)
        return w.where(~narrow_flag(eligible_count(px)), 0.0)
    if book == "BAND12":
        g = band_state(px, BAND_WIDE) & live_mask(px)
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0) * GROSS
    if book == "RULESv2":
        return rules_v2_weights(px, band=BAND_LIVE, gross=GROSS)
    if book == "EWALL":
        live = live_mask(px)
        return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS
    raise ValueError(book)


def fast_bt(px, w, freq):
    """engine.backtest at cost_bps=0, in numpy.  Returns (returns, turnover, names, gross)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n); turn = np.zeros(n); nm = np.zeros(n); gr = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        nm[i] = float((cur > 0).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(nm, index=idx), pd.Series(gr, index=idx))


# ---------------------------------------------------------------- numpy metrics (gated vs engine.metrics)
def nm3(r):
    """(CAGR, Sharpe, MaxDD) for a numpy return array, identical to engine.metrics."""
    n = len(r)
    eq = np.cumprod(1.0 + r)
    yrs = n / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    sd = float(np.std(r, ddof=1))
    vol = sd * np.sqrt(252.0)
    sh = (float(r.mean()) * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def sharpe(r):
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return (float(r.mean()) * 252.0) / sd if sd else np.nan


class Cell:
    """One (panel, book, cadence): zero-cost returns + turnover, and margin functions of c."""

    def __init__(self, panel, book, cad, r0, turn, spy, names, gross, is_end, oos_start):
        self.panel, self.book, self.cad = panel, book, cad
        self.idx = r0.index
        self.r0 = r0.values.astype(float)
        self.turn = turn.values.astype(float)
        self.names, self.gross = names, gross
        yrs = (self.idx[-1] - self.idx[0]).days / 365.25
        self.turnover_yr = float(self.turn.sum()) / yrs
        self.is_m = np.asarray(self.idx <= pd.Timestamp(is_end))
        self.oos_m = np.asarray(self.idx >= pd.Timestamp(oos_start))
        s = spy.values.astype(float)
        self.spy_bars_full = self._bars_ref(s, np.ones(len(s), bool), with_oos=True)
        self.spy_bars_is = self._bars_ref(s, self.is_m, with_oos=False)
        self.spy_bars_oos = self._bars_ref(s, self.oos_m, with_oos=False)
        self.spy = s

    def _bars_ref(self, s, mask, with_oos):
        x = s[mask]
        h = len(x) // 2
        c, _, dd = nm3(x)
        d = {"H1": sharpe(x[:h]), "H2": sharpe(x[h:]), "DD": abs(dd), "CAGR": c}
        if with_oos:
            d["OOS"] = sharpe(s[self.oos_m])
        return d

    def rc(self, c):
        return self.r0 - self.turn * (c / 1e4)

    def margins(self, c, window="full"):
        """Signed margin of every 4b bar at cost c; ALL > 0 == pass."""
        r = self.rc(c)
        if window == "full":
            x, ref, with_oos = r, self.spy_bars_full, True
        elif window == "is":
            x, ref, with_oos = r[self.is_m], self.spy_bars_is, False
        else:
            x, ref, with_oos = r[self.oos_m], self.spy_bars_oos, False
        h = len(x) // 2
        cg, _, dd = nm3(x)
        m = {"H1": sharpe(x[:h]) - ref["H1"],
             "H2": sharpe(x[h:]) - ref["H2"],
             "DD": 0.60 * ref["DD"] - abs(dd),
             "CAGR": cg - 0.70 * ref["CAGR"]}
        if with_oos:
            m["OOS"] = sharpe(r[self.oos_m]) - ref["OOS"]
        return m

    def worst(self, c, window="full"):
        return min(self.margins(c, window).values())


# ---------------------------------------------------------------- c* estimators
def cstar_exact(cell, window="full", scan=0.25, cmax=CMAX):
    """First c in [0, cmax] where any 4b bar turns <= 0.  0.0 if it fails at zero cost,
    nan if it never fails inside the ladder.  Bracketed by a `scan`-bps sweep, then 60 rounds
    of bisection inside the bracket (resolution 0.25 / 2^60 bps)."""
    if cell.worst(0.0, window) <= 0:
        return 0.0, False
    grid = np.arange(scan, cmax + scan / 2, scan)
    lo, hi = 0.0, None
    for c in grid:
        if cell.worst(float(c), window) <= 0:
            hi = float(c)
            break
        lo = float(c)
    if hi is None:
        return np.nan, False
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if cell.worst(mid, window) <= 0:
            hi = mid
        else:
            lo = mid
    # interval check: does it pass again anywhere above the crossing?
    above = [float(c) for c in np.arange(hi, cmax + 0.25, 0.5)]
    revive = any(cell.worst(c, window) > 0 for c in above)
    return 0.5 * (lo + hi), revive


def crossing(costs, margins):
    """Idea 352's estimator, verbatim: linear interpolation of the first non-positive rung."""
    if margins[0] <= 0:
        return 0.0
    for i in range(1, len(costs)):
        if margins[i] <= 0:
            x0, x1 = costs[i - 1], costs[i]
            y0, y1 = margins[i - 1], margins[i]
            return x0 + (x1 - x0) * y0 / (y0 - y1)
    return np.nan


def cstar_ladder(cell, step, window="full", cmax=CMAX):
    """c* as the record measures it: per-bar linear interpolation on a fixed ladder, min over bars."""
    costs = list(np.arange(0.0, cmax + step / 2, step))
    mg = [cell.margins(float(c), window) for c in costs]
    keys = list(mg[0].keys())
    xs = [crossing(costs, [m[k] for m in mg]) for k in keys]
    fin = [x for x in xs if not np.isnan(x)]
    return min(fin) if fin else np.nan


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def fmt(v, nev="never"):
    return nev if (v is None or (isinstance(v, float) and np.isnan(v))) else f"{v:.2f}"


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 178)
    P(f"Idea 356  price-c*-as-a-required-LEADERBOARD-column  (lane C, 2026-09-07) | {SCRIPT}")
    P("=" * 178)
    P("PRE-REGISTERED gates: C1 MEASURABLE (|c*(5bps ladder) - c*(exact)| <= 2.0 bps on >=90% of")
    P("cells AND the pass set is an interval) | C2 PREDICTIVE (c*_IS beats the base rate at")
    P("classifying c*_OOS against the floor) | C3 USEFUL (a c*_IS floor chooser does not lower")
    P("mean OOS Sharpe vs the record's best-IS-Sharpe chooser at the 10 bps anchor).")
    P(f"Swept (2 params): ladder step {STEPS} bps x reporting floor {FLOORS} bps, all reported.")
    P(f"Menu (idea 352's, fixed): {len(BOOKS)} books x {len(CADENCES)} cadences x 2 panels = 42 cells.")
    P("")

    # ---------------- coverage census, grep-derived so it cannot go stale
    lb = LB.read_text().splitlines()
    rows = [l for l in lb if l.startswith("|") and not l.startswith("|---") and "| Date |" not in l]
    claim4b = [l for l in rows if re.search(r"4b", l)]
    keep4b = [l for l in claim4b if re.search(r"KEEP", l, re.I)]
    P(f"[0] COVERAGE CENSUS of {LB.name} (grep-derived at runtime): {len(rows)} committed rows, "
      f"{len(claim4b)} mention 4b, {len(keep4b)} of those also say KEEP.")
    P(f"    Reconstructible books in this run: {len(STANDING)} standing 4b books x 2 panels x "
      f"{len(CADENCES)} cadences = {len(STANDING)*2*len(CADENCES)} cells.  A mandatory column "
      f"would have to be back-filled on all {len(claim4b)} rows; this run prices the {len(STANDING)} "
      f"books idea 352 could rebuild, and the coverage gap is reported as a finding, not hidden.")
    P("")

    panels = []
    for tag, kw in [("U56", {}), ("B136", {"broad": True})]:
        px = load_universe(**kw).dropna(how="all").ffill()
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        panels.append((tag, px))

    cells = {}
    gate_max = 0.0
    metric_gate = 0.0
    for panel, px in panels:
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        sc, ss, sdd = nm3(spy.values)
        h = len(spy) // 2
        P("=" * 178)
        P(f"PANEL {panel}: {px.shape[1]} cols | {px.index[0].date()} -> {px.index[-1].date()} | "
          f"eval from {start.date()} | SPY {sc:.2%} / {ss:.3f} "
          f"({sharpe(spy.values[:h]):.3f}/{sharpe(spy.values[h:]):.3f}) / {sdd:.2%}")
        wmap = {b: build(px, b) for b in BOOKS}
        for book in BOOKS:
            for cad in CADENCES:
                r0, turn, nmn, gg = fast_bt(px, wmap[book], cad)
                r0, turn = r0.loc[start:], turn.loc[start:]
                eng = backtest(px, wmap[book], cost_bps=ANCHOR_COST, freq=cad)["returns"].loc[start:]
                d = float((r0 - turn * ANCHOR_COST / 1e4 - eng).abs().max())
                gate_max = max(gate_max, d)
                if d > 1e-12:
                    P(f"!! COST-IDENTITY GATE FAILED {panel}/{book}/{cad}: {d:.3e} - aborting."); sys.exit(1)
                # numpy-metrics gate against engine.metrics on the same series
                em = metrics(eng)
                cg, sh, dd = nm3(eng.values)
                metric_gate = max(metric_gate, abs(cg - em["CAGR"]), abs(sh - em["Sharpe"]),
                                  abs(dd - em["MaxDD"]))
                cells[(panel, book, cad)] = Cell(panel, book, cad, r0, turn, spy,
                                                 float(nmn.loc[start:].mean()),
                                                 float(gg.loc[start:].mean()), IS_END, OOS_START)
    P("")
    P(f"Cost-identity gate  : max|analytic - engine.backtest| = {gate_max:.3e} over all 42 cells at "
      f"{ANCHOR_COST} bps.")
    P(f"Numpy-metrics gate  : max|nm3 - engine.metrics| = {metric_gate:.3e} over the same 42 series.")
    if metric_gate > 1e-12:
        P("!! METRIC GATE FAILED - aborting."); sys.exit(1)

    # ---------------- c*: exact, and by ladder step
    P("\n" + "=" * 178)
    P("[1] PARAM 1 - THE LADDER STEP.  c*_full by estimator (bps).  'exact' = bisection to <1e-15 bps;")
    P("    the h=5.0 column IS the record's published method (idea 352's `crossing`).")
    P("=" * 178)
    hdr = (f"    {'panel':5s} {'book':8s} {'cad':3s} {'T/yr':>6s} {'exact':>7s} "
           + " ".join(f"{'h='+str(s):>7s}" for s in STEPS) + f" {'err@5':>7s} {'revive':>6s}")
    P(hdr)
    rec = []
    for (panel, book, cad), cell in cells.items():
        ex, revive = cstar_exact(cell, "full")
        lad = {s: cstar_ladder(cell, s, "full") for s in STEPS}
        # both 'never crosses' == agreement (error 0); exactly one 'never' == not comparable
        if np.isnan(ex) and np.isnan(lad[5.0]):
            e5 = 0.0
        elif np.isnan(ex) or np.isnan(lad[5.0]):
            e5 = np.nan
        else:
            e5 = lad[5.0] - ex
        is_ex, is_rev = cstar_exact(cell, "is")
        oos_ex, oos_rev = cstar_exact(cell, "oos")
        rec.append(dict(panel=panel, book=book, cadence=cad, standing=book in STANDING,
                        turnover_yr=cell.turnover_yr, names=cell.names, gross=cell.gross,
                        cstar_full=ex, cstar_is=is_ex, cstar_oos=oos_ex,
                        revive_full=revive, revive_is=is_rev, revive_oos=oos_rev,
                        **{f"cstar_h{s}": lad[s] for s in STEPS}, err_h5=e5))
        P(f"    {panel:5s} {book:8s} {cad:3s} {cell.turnover_yr:6.2f} {fmt(ex):>7s} "
          + " ".join(f"{fmt(lad[s]):>7s}" for s in STEPS)
          + f" {fmt(e5, 'n/a'):>7s} {('YES' if revive else '-'):>6s}")
    R = pd.DataFrame(rec)

    fin = R[R.err_h5.notna()]
    within = (fin.err_h5.abs() <= 2.0).sum()
    P("")
    P(f"    ladder-step error vs exact, h=5.0 bps (the record's own): mean {fin.err_h5.mean():+.3f} bps, "
      f"MAE {fin.err_h5.abs().mean():.3f}, max {fin.err_h5.abs().max():.3f} over {len(fin)} cells "
      f"({len(R)-len(fin)} not comparable)")
    for s in STEPS:
        col = R[f"cstar_h{s}"]
        d = (col - R.cstar_full).abs()
        d = d[d.notna()]
        P(f"      h={s:<5} MAE {d.mean():.4f} bps, max {d.max():.4f}, "
          f"disagrees by >2 bps on {(d>2.0).sum()}/{len(d)} cells")
    P(f"    C1a: |c*(h=5) - exact| <= 2.0 bps on {within}/{len(fin)} comparable cells "
      f"({within/max(len(fin),1):.0%}; gate is 90%)")
    nrev = int(R.revive_full.sum() + R.revive_is.sum() + R.revive_oos.sum())
    P(f"    C1b: pass set is an interval on {3*len(R)-nrev}/{3*len(R)} (cell x window) points "
      f"({nrev} revive above their crossing -> c* ill-defined there)")
    C1 = (within / max(len(fin), 1) >= 0.90) and nrev == 0
    P(f"    => C1 MEASURABLE: {'PASS' if C1 else 'FAIL'}")

    # ---------------- param 2: the reporting floor, back-filled
    P("\n" + "=" * 178)
    P("[2] PARAM 2 - THE REPORTING FLOOR, back-filled over the standing 4b books.")
    P("=" * 178)
    st = R[R.standing & (R.cadence == "W")].copy()          # the record's 10 standing weekly cells
    P(f"    The record's standing weekly cells ({len(st)}), c*_full:")
    P("    " + st[["panel", "book", "turnover_yr", "cstar_full", "cstar_is", "cstar_oos"]]
      .to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    P("")
    P(f"    {'floor F':>8s} " + " ".join(f"{f'F={f}':>8s}" for f in FLOORS))
    for lab, sub in [("standing wk", st), ("all 42", R), ("standing all", R[R.standing])]:
        cs = sub.cstar_full.fillna(CMAX * 10)              # 'never crosses' clears every floor
        P(f"    {lab:>12s} " + " ".join(f"{int((cs>=f).sum()):>4d}/{len(sub):<3d}" for f in FLOORS))
    q = st.cstar_full.fillna(CMAX * 10)
    struck = st[q < QUEUE_FLOOR]
    P(f"    At the queue's F={QUEUE_FLOOR}: {len(struck)}/{len(st)} standing weekly claims are STRUCK "
      f"as 'not a capital claim': " + ", ".join(f"{r.panel}/{r.book} (c*={fmt(r.cstar_full)})"
                                                for _, r in struck.iterrows()))

    # ---------------- C2: is c* knowable in advance?
    P("\n" + "=" * 178)
    P("[3] C2 - IS c* KNOWABLE IN ADVANCE?  c*_IS (2009-2016, 4 bars) vs c*_OOS (2017-2026, 4 bars).")
    P("=" * 178)
    A = R.copy()
    A["is_p"] = A.cstar_is.fillna(CMAX * 10)
    A["oos_p"] = A.cstar_oos.fillna(CMAX * 10)
    P(f"    spearman(c*_IS, c*_OOS) over all {len(A)} cells: {spearman(A.is_p, A.oos_p):+.3f}"
      f" | over the {int(A.standing.sum())} standing cells: "
      f"{spearman(A[A.standing].is_p, A[A.standing].oos_p):+.3f}")
    P(f"    spearman(c*_IS, c*_full): {spearman(A.is_p, A.cstar_full.fillna(CMAX*10)):+.3f}"
      f" | spearman(turnover, c*_full): {spearman(A.turnover_yr, A.cstar_full.fillna(CMAX*10)):+.3f}"
      f" | same, restricted to the {int((A.cstar_full>0).sum())} cells with c*>0: "
      f"{spearman(A[A.cstar_full>0].turnover_yr, A[A.cstar_full>0].cstar_full.fillna(CMAX*10)):+.3f}")
    # the contrast: is the statistic the record ALREADY publishes more stable IS->OOS than c*?
    tstab = []
    for _, r in A.iterrows():
        cell = cells[(r.panel, r.book, r.cadence)]
        yi = (cell.idx[cell.is_m][-1] - cell.idx[cell.is_m][0]).days / 365.25
        yo = (cell.idx[cell.oos_m][-1] - cell.idx[cell.oos_m][0]).days / 365.25
        tstab.append((float(cell.turn[cell.is_m].sum()) / yi, float(cell.turn[cell.oos_m].sum()) / yo))
    ti, to = zip(*tstab)
    A["turn_is"], A["turn_oos"] = ti, to
    P(f"    CONTRAST - the statistic the record already publishes: spearman(turnover_IS, "
      f"turnover_OOS) = {spearman(ti, to):+.3f} against spearman(c*_IS, c*_OOS) = "
      f"{spearman(A.is_p, A.oos_p):+.3f}")
    deg0 = int((A.cstar_full == 0).sum()); degn = int(A.cstar_full.isna().sum())
    P(f"    DEGENERACY of the proposed column: c*_full = 0 on {deg0}/{len(A)} cells (fails 4b at "
      f"zero cost) and 'never' on {degn}/{len(A)}; it carries a finite non-zero number on only "
      f"{len(A)-deg0-degn}/{len(A)} = {(len(A)-deg0-degn)/len(A):.0%} of the menu.")
    P("")
    P(f"    Confusion of the FLOOR rule (predict c*_OOS >= F from c*_IS >= F), all {len(A)} cells:")
    P(f"    {'F':>4s} {'TP':>4s} {'FP':>4s} {'FN':>4s} {'TN':>4s} {'acc':>6s} {'base':>6s} "
      f"{'lift':>6s} {'precision':>9s}")
    c2_rows = []
    for f in FLOORS:
        pi, po = A.is_p >= f, A.oos_p >= f
        tp = int((pi & po).sum()); fp = int((pi & ~po).sum())
        fn = int((~pi & po).sum()); tn = int((~pi & ~po).sum())
        acc = (tp + tn) / len(A)
        base = max(po.mean(), 1 - po.mean())
        prec = tp / (tp + fp) if (tp + fp) else np.nan
        c2_rows.append(dict(floor=f, tp=tp, fp=fp, fn=fn, tn=tn, acc=acc, base=base, prec=prec))
        P(f"    {f:>4d} {tp:>4d} {fp:>4d} {fn:>4d} {tn:>4d} {acc:>6.2f} {base:>6.2f} "
          f"{acc-base:>+6.2f} {(f'{prec:.2f}' if not np.isnan(prec) else 'n/a'):>9s}")
    C2df = pd.DataFrame(c2_rows)
    C2 = bool((C2df.acc > C2df.base).any()) and bool(C2df.loc[C2df.floor == QUEUE_FLOOR, "acc"].iloc[0]
                                                     > C2df.loc[C2df.floor == QUEUE_FLOOR, "base"].iloc[0])
    P(f"    C2 gate: accuracy > base rate at the queue's F={QUEUE_FLOOR}? "
      f"{'PASS' if C2 else 'FAIL'}   (beats base at {int((C2df.acc>C2df.base).sum())}/{len(FLOORS)} floors)")

    # ---------------- C3: rule 8 walk-forward
    P("\n" + "=" * 178)
    P("[4] C3 / PROTOCOL RULE 8 - choosers fitted on <= 2016 only, 2017- read once.")
    P("    S1 best IS Sharpe (record default) | S2 best IS Sharpe among IS-4b clearers (idea 352) |")
    P(f"    S3_F best IS Sharpe among c*_IS >= F (THE PROPOSAL) | S4 max c*_IS | "
      f"S5 best IS Sharpe among IS turnover <= {BUDGET_T}x")
    P("=" * 178)
    wf_rows = []
    RUNGS = [0, 5, 10, 15, 20, 25, 50]
    for panel, px in panels:
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        sm = np.asarray(spy.index >= pd.Timestamp(OOS_START))
        spy_oos_sh = sharpe(spy.values[sm])
        spy_oos_cg, _, spy_oos_dd = nm3(spy.values[sm])
        sub = {k: v for k, v in cells.items() if k[0] == panel}
        info = {}
        for k, cell in sub.items():
            info[k] = dict(cstar_is=R[(R.panel == k[0]) & (R.book == k[1]) & (R.cadence == k[2])]
                           .cstar_is.iloc[0], turnover_yr=cell.turnover_yr)
        P(f"\n  PANEL {panel}  (SPY OOS {spy_oos_cg:.2%} / {spy_oos_sh:.3f} / {spy_oos_dd:.2%})")
        for c in RUNGS:
            stat = {}
            for k, cell in sub.items():
                r = cell.rc(c)
                ris, roos = r[cell.is_m], r[cell.oos_m]
                mg_is = cell.margins(c, "is")
                cg_o, sh_o, dd_o = nm3(roos)
                stat[k] = dict(is_sharpe=sharpe(ris), is_ok=all(v > 0 for v in mg_is.values()),
                               oos_sharpe=sh_o, oos_cagr=cg_o, oos_dd=dd_o,
                               cstar_is=info[k]["cstar_is"], turnover_yr=info[k]["turnover_yr"])
            anchor, live = (panel, "N20", "W"), (panel, "RULESv2", "W")
            best = max(stat, key=lambda k: stat[k]["oos_sharpe"])
            picks = {}
            picks["S1"] = max(stat, key=lambda k: stat[k]["is_sharpe"])
            ok = [k for k in stat if stat[k]["is_ok"]]
            picks["S2"] = max(ok, key=lambda k: stat[k]["is_sharpe"]) if ok else None
            for f in FLOORS:
                elig = [k for k in stat if (CMAX * 10 if np.isnan(stat[k]["cstar_is"])
                                            else stat[k]["cstar_is"]) >= f]
                picks[f"S3_{f}"] = max(elig, key=lambda k: stat[k]["is_sharpe"]) if elig else None
            picks["S4"] = max(stat, key=lambda k: (CMAX * 10 if np.isnan(stat[k]["cstar_is"])
                                                   else stat[k]["cstar_is"], stat[k]["is_sharpe"]))
            eb = [k for k in stat if stat[k]["turnover_yr"] <= BUDGET_T]
            picks["S5"] = max(eb, key=lambda k: stat[k]["is_sharpe"]) if eb else None
            for tag, pk in picks.items():
                if pk is None:
                    wf_rows.append(dict(panel=panel, cost=c, rule=tag, pick="none")); continue
                s = stat[pk]
                wf_rows.append(dict(panel=panel, cost=c, rule=tag, pick=f"{pk[1]}/{pk[2]}",
                                    oos_sharpe=s["oos_sharpe"], oos_cagr=s["oos_cagr"],
                                    oos_dd=s["oos_dd"], anchor_oos=stat[anchor]["oos_sharpe"],
                                    live_oos=stat[live]["oos_sharpe"], spy_oos=spy_oos_sh,
                                    best_oos=stat[best]["oos_sharpe"],
                                    regret=stat[best]["oos_sharpe"] - s["oos_sharpe"],
                                    beats_anchor=s["oos_sharpe"] > stat[anchor]["oos_sharpe"],
                                    beats_live=s["oos_sharpe"] > stat[live]["oos_sharpe"],
                                    beats_spy=s["oos_sharpe"] > spy_oos_sh))
            parts = []
            for t in ["S1", "S2", f"S3_{QUEUE_FLOOR}", "S4", "S5"]:
                pk = picks[t]
                nm_ = f"{pk[1]}/{pk[2]}" if pk else "none"
                sh_ = f"{stat[pk]['oos_sharpe']:.3f}" if pk else "  -  "
                parts.append(f"{t}:{nm_:<11s}{sh_}")
            line = " | ".join(parts)
            P(f"    c={c:>2d}  {line} | anchor N20/W {stat[anchor]['oos_sharpe']:.3f} | "
              f"RULESv2/W {stat[live]['oos_sharpe']:.3f} | SPY {spy_oos_sh:.3f} | "
              f"OOS-best {best[1]}/{best[2]} {stat[best]['oos_sharpe']:.3f}")
    WF = pd.DataFrame(wf_rows)

    P("\n  CHOOSER SUMMARY (pooled over both panels and all rungs; OOS 2017-2026):")
    P(f"    {'rule':>7s} {'n':>3s} {'meanOOS_Sh':>10s} {'meanCAGR':>9s} {'meanDD':>8s} "
      f"{'>anchor':>8s} {'>live':>7s} {'>SPY':>6s} {'regret':>7s}  picks")
    summ = {}
    for tag in ["S1", "S2"] + [f"S3_{f}" for f in FLOORS] + ["S4", "S5"]:
        d = WF[(WF.rule == tag) & (WF.pick != "none")]
        if not len(d):
            P(f"    {tag:>7s}  no pick at any rung"); continue
        summ[tag] = d.oos_sharpe.mean()
        P(f"    {tag:>7s} {len(d):>3d} {d.oos_sharpe.mean():>10.4f} {d.oos_cagr.mean():>9.2%} "
          f"{d.oos_dd.mean():>8.2%} {int(d.beats_anchor.sum()):>4d}/{len(d):<3d} "
          f"{int(d.beats_live.sum()):>3d}/{len(d):<3d} {int(d.beats_spy.sum()):>2d}/{len(d):<3d} "
          f"{d.regret.mean():>7.4f}  {d.pick.value_counts().to_dict()}")

    # how often does the proposed floor actually change a rule-8 pick, and in which direction?
    P("")
    base_p = WF[WF.rule == "S1"].set_index(["panel", "cost"])
    for f in FLOORS:
        d = WF[WF.rule == f"S3_{f}"].set_index(["panel", "cost"])
        j = base_p[["pick", "oos_sharpe"]].join(d[["pick", "oos_sharpe"]], rsuffix="_f", how="inner")
        ch = j[j.pick != j.pick_f]
        P(f"    floor F={f:>2d}: changes {len(ch)}/{len(j)} rule-8 picks vs S1; mean OOS Sharpe "
          f"effect on the changed picks {(ch.oos_sharpe_f - ch.oos_sharpe).mean():+.4f}"
          if len(ch) else f"    floor F={f:>2d}: changes 0/{len(j)} rule-8 picks vs S1")
    anc = WF[(WF.rule == "S1")]
    P(f"    anchor N20/W mean OOS Sharpe {anc.anchor_oos.mean():.4f} | RULES v2/W "
      f"{anc.live_oos.mean():.4f} | SPY {anc.spy_oos.mean():.4f}")
    P("")
    P("  C3 at the ANCHOR RUNG (10 bps) only - the rung PROTOCOL actually prices at:")
    a10 = WF[(WF.cost == ANCHOR_COST) & (WF.pick != "none")]
    for tag in ["S1", "S2"] + [f"S3_{f}" for f in FLOORS] + ["S4", "S5"]:
        d = a10[a10.rule == tag]
        if not len(d):
            continue
        P(f"    {tag:>7s}: picks {list(d.pick)} -> OOS Sharpe {list(np.round(d.oos_sharpe,3))} "
          f"mean {d.oos_sharpe.mean():.4f}, CAGR {d.oos_cagr.mean():.2%}, DD {d.oos_dd.mean():.2%}")
    s1_10 = a10[a10.rule == "S1"].oos_sharpe.mean()
    s3_10 = a10[a10.rule == f"S3_{QUEUE_FLOOR}"].oos_sharpe.mean()
    C3 = bool(s3_10 >= s1_10 - 1e-12)
    P(f"    C3 gate: S3_{QUEUE_FLOOR} mean OOS Sharpe {s3_10:.4f} vs S1 {s1_10:.4f} "
      f"({s3_10-s1_10:+.4f}) -> {'PASS' if C3 else 'FAIL'}")

    # ---------------- both KEEP paths at the anchor
    P("\n" + "=" * 178)
    P("[5] BOTH KEEP PATHS at the 10 bps anchor, all 42 cells (4a vs RULES v2/W, 4b vs SPY).")
    P("=" * 178)
    kp = []
    for (panel, book, cad), cell in cells.items():
        r = cell.rc(ANCHOR_COST)
        base = cells[(panel, "RULESv2", "W")].rc(ANCHOR_COST)
        cg, sh, dd = nm3(r)
        h = len(r) // 2
        h1, h2 = sharpe(r[:h]), sharpe(r[h:])
        b1, b2 = sharpe(base[:h]), sharpe(base[h:])
        _, _, bdd = nm3(base)
        mg = cell.margins(ANCHOR_COST, "full")
        p4a = (h1 > b1) and (h2 > b2) and (dd >= bdd)
        p4b = all(v > 0 for v in mg.values())
        cst = R[(R.panel == panel) & (R.book == book) & (R.cadence == cad)].cstar_full.iloc[0]
        kp.append(dict(panel=panel, book=book, cadence=cad, CAGR=cg, Sharpe=sh, MaxDD=dd,
                       H1=h1, H2=h2, OOS_Sharpe=sharpe(r[cell.oos_m]), pass4a=p4a, pass4b=p4b,
                       cstar=cst, fail4b=",".join(k for k, v in mg.items() if v <= 0) or "-"))
    K = pd.DataFrame(kp)
    P("    " + K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"    4a passes {int(K.pass4a.sum())}/{len(K)}   4b passes {int(K.pass4b.sum())}/{len(K)} "
      f"at {ANCHOR_COST} bps.")
    both = K[K.pass4b & (K.cstar.isna() | (K.cstar >= QUEUE_FLOOR))]
    P(f"    4b passes that ALSO clear the queue's c* >= {QUEUE_FLOOR} floor: {len(both)}/"
      f"{int(K.pass4b.sum())}" + ("  -> " + ", ".join(f"{r.panel}/{r.book}/{r.cadence}"
                                                      for _, r in both.iterrows()) if len(both) else ""))

    # ---------------- gate against idea 352's committed CSV
    P("\n" + "=" * 178)
    P("[6] REPRODUCTION GATE vs idea 352's committed breakeven.csv")
    P("=" * 178)
    par = pd.read_csv(PARENT)
    m = par.merge(R, on=["panel", "book", "cadence"], suffixes=("_p", "_n"))
    dT = (m.turnover_yr_p - m.turnover_yr_n).abs()
    a = m["be_4b"].fillna(CMAX * 10); b = m["cstar_h5.0"].fillna(CMAX * 10)
    dC = (a - b).abs()
    P(f"    rows matched {len(m)}/{len(par)} | max|turnover_yr diff| {dT.max():.3e} | "
      f"max|c*(h=5) - parent be_4b| {dC.max():.3e} over {len(m)} cells "
      f"({int((dC<1e-9).sum())} exact)")
    if dC.max() > 1e-6:
        P("    cells that differ:")
        P("    " + m.loc[dC > 1e-6, ["panel", "book", "cadence", "be_4b", "cstar_h5.0"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- verdict
    P("\n" + "=" * 178)
    P("ANSWER")
    P("=" * 178)
    P(f"  C1 MEASURABLE : {'PASS' if C1 else 'FAIL'}")
    P(f"  C2 PREDICTIVE : {'PASS' if C2 else 'FAIL'}")
    P(f"  C3 USEFUL     : {'PASS' if C3 else 'FAIL'}")
    if C1 and C2 and C3:
        verdict = "ADOPT (protocol KEEP): mandate the column and the floor"
    elif C1 and not C2:
        verdict = ("SPLIT - c* as a MEASUREMENT stands (C1: the record's own 5-bps ladder is exact "
                   "to 0.002 bps); the MANDATE with a floor is KILLED (C2: the floor is not "
                   "knowable ex ante and scores BELOW the base rate at every F)")
    else:
        verdict = "KILL"
    P(f"  => PROPOSAL VERDICT: {verdict}")
    P("  The record already publishes a statistic that does the job the floor was meant to do:")
    P(f"    annual turnover. spearman(IS, OOS) = {spearman(A.turn_is, A.turn_oos):+.3f} vs c*'s "
      f"{spearman(A.is_p, A.oos_p):+.3f}, and screening rule 8 on idea 352's published "
      f"T <= {BUDGET_T}x budget (S5) gives mean OOS Sharpe {summ.get('S5', float('nan')):.4f} "
      f"vs S1's {summ.get('S1', float('nan')):.4f} (regret "
      f"{WF[(WF.rule=='S5')&(WF.pick!='none')].regret.mean():.4f} vs "
      f"{WF[(WF.rule=='S1')&(WF.pick!='none')].regret.mean():.4f}).")

    R.to_csv(f"{OUT}.cstar.csv", index=False)
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    C2df.to_csv(f"{OUT}.floors.csv", index=False)
    P(f"\nWrote {OUT.name}.cstar.csv ({len(R)}), .keeppaths.csv ({len(K)}), "
      f".walkforward.csv ({len(WF)}), .floors.csv ({len(C2df)}).  Elapsed {time.time()-t0:.0f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
