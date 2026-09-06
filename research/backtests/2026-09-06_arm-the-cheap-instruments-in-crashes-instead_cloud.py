#!/usr/bin/env python3
"""QUEUE idea 245 — arm-the-cheap-instruments-in-crashes-instead (cloud, 2026-09-06).

Question (pre-registered)
-------------------------
Idea 75 measured the FAST per-name trailing stop's (arm - control) return split by the
SPY<200dMA regime and found it is DEAREST in the crash regime (-1.03 pp/yr at S=20% vs
-0.04 pp/yr in trends), which inverts the queue's whipsaw premise.  The same split has
never been run on the SLOW instruments the project owns (200d gate, 3% re-entry band,
absolute momentum, constant de-gross, idea 40's book-level drawdown control), where
ideas 55/57/4 say FLIP RATE is the cost driver rather than the regime.

Pre-registered question, exactly as the queue states it: split each slow instrument's
(arm - control) return by SPY<200dMA and report whether ANY of them is cheaper in
crashes than in trends.  "Cheaper in crashes" is defined before any number is read as

    d_crash_ann  >  d_trend_ann          (both in pp/yr, annualised within-regime)

where d = (arm return - its OWN control's return) on the same book, same panel, same
cost.  A YES for an instrument means the regime-conditional arming idea 75 killed for
the stop is at least ARITHMETICALLY available for that instrument.  A NO everywhere
would say the project's whole "arm it only in crashes" family is dead, not just the
stop's version of it.

Secondary, and reported but never selected on: the same split under idea 75's
`breadth20` regime (panel breadth at/below its expanding 20th percentile), as a
robustness read on the regime definition, which is PRE-REGISTERED as spy200.

Design (PROTOCOL rules 1-8)
---------------------------
Universes : u56 = load_universe() (56 names + SPY); broad = load_universe(broad=True)
            (136 names).  BOTH reported at every arm.  SURVIVORSHIP: current
            constituents of both lists, so every level here is biased upward; the
            statistic read for the verdict is a WITHIN-cell difference (arm minus its
            own control on the same panel), which the bias largely cancels out of.
Books     : two INSTRUMENT-FREE base books, so that every instrument is an overlay and
            no book smuggles in the instrument it is meant to price:
              EWALL0 — equal-weight every name in the panel, no trend gate, no vol gate.
              CAND20 — top 20 by idea 2's composite (no vol scaler), NO gates.
            Both at GROSS = 0.75 (idea 2's KEEP 4b convention).
Params    : exactly TWO tuned dimensions —
              * instrument FAMILY in {200d, band, abs, dg, ddctl, stop}
              * that family's STRENGTH level, 4 values each (see STRENGTH below).
            = 24 arms + the no-instrument control per (panel, book).  ALL reported.
            Panel, book and cost are reported at every value and never selected on.
Costs     : 10 bps (PROTOCOL, verdicts read here) and 25 bps, applied analytically
            (net = gross - turnover * bps/1e4), exact because the held path does not
            depend on cost_bps.
Execution : weights decided at close t, applied at close t+1 (PROTOCOL rule 2).  The
            stop trigger, the ddctl state and the gates are all read at close i and
            executed at close i+1.
Baseline  : RULES v1 weekly on the same panel (4a) and SPY buy-and-hold (4b).  BOTH
            KEEP paths evaluated for every arm.
Rule 8    : (family, strength) chosen on 2009-2016 IS by Sharpe, 2017-2026 evaluated
            untouched; OOS CAGR/Sharpe/MaxDD reported against the no-instrument
            control's, RULES v1's and SPY's OOS.

Reproduction gates, asserted before any result is read:
  [A] run() with no instrument == engine.backtest on the same weights (max|diff| ~ 0).
  [B] run() with family=dg is the exact static lever: net(g*book) == g*net(book) at
      zero cost, i.e. g*gross and g*turnover (idea 66).
  [C] run() with family=stop reproduces idea 94's published `run_stop` bit-for-bit at
      every depth (the module is IMPORTED, not re-implemented).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

# --- import idea 94's module (the stop reference, not a re-implementation) -----
_p94 = ROOT / "research" / "backtests" / "2026-09-04_trailing-stop_cloud.py"
_spec = importlib.util.spec_from_file_location("ts94", _p94)
ts94 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ts94)
composite = ts94.composite
at_cost = ts94.at_cost
m = ts94.m
halves = ts94.halves
turn_per_yr = ts94.turn_per_yr
fail4a = ts94.fail4a
fail4b = ts94.fail4b

GROSS = 0.75
FREQ = "W"
COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BREADTH_Q = 0.20
MIN_HIST = 756
DD_CUT = 0.50                     # idea 40's convention: halve the book in drawdown
SCRIPT = "research/backtests/2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py"
OUT = ROOT / "research" / "backtests" / "2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud"

# strength ladder per family — 4 levels each, ALL reported, none selected on
STRENGTH = {
    "200d":  [100, 150, 200, 250],        # MA window (days)
    "band":  [0.02, 0.03, 0.05, 0.08],    # re-entry band around the 200d MA
    "abs":   [63, 126, 252, 378],         # absolute-momentum lookback (days)
    "dg":    [0.85, 0.75, 0.60, 0.45],    # constant gross multiplier
    "ddctl": [0.08, 0.12, 0.16, 0.20],    # book drawdown that halves the book
    "stop":  [0.10, 0.15, 0.20, 0.25],    # per-name trailing stop depth
}
SLOW = ["200d", "band", "abs", "dg", "ddctl"]      # the queue's set
FAMILIES = SLOW + ["stop"]                          # + idea 75's fast reference


# ---------------------------------------------------------------- base books
def w_ewall0(px):
    """Equal-weight EVERY name in the panel (SPY excluded as a constituent). No gates."""
    names = [c for c in px.columns if c != "SPY"]
    e = px[names].notna().astype(float)
    w = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS
    return w.reindex(columns=px.columns).fillna(0.0)


def w_cand20(px):
    """Top 20 by idea 2's composite, NO trend gate and NO vol gate (instrument-free)."""
    names = [c for c in px.columns if c != "SPY"]
    rank = composite(px[names]).rank(axis=1, ascending=False)
    w = (rank <= 20).astype(float) * (GROSS / 20)
    return w.reindex(columns=px.columns).fillna(0.0)


BASE_BOOKS = {"EWALL0": w_ewall0, "CAND20": w_cand20}


# ---------------------------------------------------------------- instruments
def gate_mask(px, family, level):
    """Boolean per-name eligibility read at close i (shifted to i+1 by the simulator)."""
    names = [c for c in px.columns if c != "SPY"]
    p = px[names]
    if family == "200d":
        return (p > p.rolling(int(level)).mean()).fillna(False)
    if family == "band":
        ma = p.rolling(200).mean()
        raw = pd.DataFrame(np.nan, index=p.index, columns=p.columns)
        raw = raw.mask(p > ma * (1 + level), 1.0)
        raw = raw.mask(p < ma * (1 - level), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if family == "abs":
        return ((p / p.shift(int(level)) - 1) > 0).fillna(False)
    raise ValueError(family)


def apply_gate(w, mask):
    """Re-normalise the surviving names back to GROSS (cash if nothing survives)."""
    names = list(mask.columns)
    ww = w[names] * mask.reindex(columns=names).astype(float)
    s = ww.sum(axis=1).replace(0, np.nan)
    out = ww.div(s, axis=0).fillna(0.0) * GROSS
    return out.reindex(columns=w.columns).fillna(0.0)


def regime(px, arm):
    """Boolean per-day series read at close i. No look-ahead (expanding quantile)."""
    if arm == "spy200":
        spy = px["SPY"]
        return (spy < spy.rolling(200).mean()).fillna(False)
    if arm == "breadth20":
        names = [c for c in px.columns if c != "SPY"]
        p = px[names]
        br = (p > p.rolling(200).mean()).sum(axis=1) / p.notna().sum(axis=1).clip(lower=1)
        q = br.expanding(min_periods=MIN_HIST).quantile(BREADTH_Q)
        return (br <= q).fillna(False)
    raise ValueError(arm)


# ---------------------------------------------------------------- simulator
def run(prices, weights, stop=None, ddctl=None, freq=FREQ):
    """engine.backtest + optionally a per-name trailing stop and/or a book-level DD
    control, at ZERO cost (costs applied analytically afterwards).

    stop=None and ddctl=None must reproduce engine.backtest exactly (gate [A]).
    stop=S with ddctl=None must reproduce idea 94's run_stop exactly (gate [C]).

    ddctl: the book's own equity peak-to-trough drawdown is read at close i; if it is
    worse than -ddctl the target multiplier for close i+1 is DD_CUT, else 1.0.  The
    multiplier is applied to the HELD book daily (t+1 execution), so entering and
    leaving the cut state costs turnover exactly as a real de-gross would.
    """
    rets = prices.pct_change().fillna(0.0).values
    pxv = prices.values
    n = pxv.shape[1]
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values

    cur = np.zeros(n)
    peak = np.full(n, np.nan)
    pending = np.zeros(n, dtype=bool)
    port = np.zeros(len(prices))
    turn = np.zeros(len(prices))
    invested = np.zeros(len(prices))
    mult = 1.0
    next_mult = 1.0
    eq = 1.0
    eq_peak = 1.0
    n_fires = 0

    for i in range(len(prices)):
        # 1. execute stop exits decided at the previous close (t+1 execution)
        if pending.any():
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        # 1b. execute the ddctl gross change decided at the previous close (t+1)
        if ddctl is not None and next_mult != mult:
            scaled = cur * (next_mult / mult)
            turn[i] += np.abs(scaled - cur).sum()
            cur = scaled
            mult = next_mult
        # 2. scheduled rebalance (target decided at t-1 via the shift above)
        if mask[i] or i == 0:
            new = w_target[i] * (mult if ddctl is not None else 1.0)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held = cur.copy()
        invested[i] = held.sum()
        port[i] = float(np.nansum(held * rets[i]))
        # 3. drift
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
        # 4. update trailing highs and fire stops on the new closes
        if stop is not None:
            alive = cur > 1e-9
            p = pxv[i]
            peak = np.where(alive, np.fmax(np.where(np.isnan(peak), -np.inf, peak), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak * (1 - stop))
            if hit.any():
                pending |= hit
                n_fires += int(hit.sum())
        # 5. read the book's own drawdown state for the next bar
        if ddctl is not None:
            eq *= (1 + port[i])
            eq_peak = max(eq_peak, eq)
            nm = DD_CUT if (eq / eq_peak - 1) < -ddctl else 1.0
            if nm != next_mult:
                n_fires += 1
            next_mult = nm

    idx = prices.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(invested, index=idx), n_fires)


def arm_returns(px, w, family, level, ctrl):
    """(gross returns, turnover, invested, fires) for one instrument arm.

    `ctrl` is the SAME book with no instrument, full index — needed by `dg`, which is
    idea 66's EXACT static lever (scale the realised return AND turnover by g, the
    remainder in cash at 0%), not a re-run of the book at g x weights.  The two are not
    the same object in this engine, because `engine.backtest` re-normalises the drifted
    book against its cash line each day; harness gate [B] measures the gap rather than
    asserting it away, and both conventions are reported.
    """
    if family in ("200d", "band", "abs"):
        return run(px, apply_gate(w, gate_mask(px, family, level)))
    if family == "dg":
        g, t, inv, _ = ctrl
        return g * level, t * level, inv * level, 0
    if family == "ddctl":
        return run(px, w, ddctl=level)
    if family == "stop":
        return run(px, w, stop=level)
    raise ValueError(family)


# ---------------------------------------------------------------- harness
def harness(px):
    """Reproduction gates [A] [B] [C]. Asserted before any result is read."""
    w = w_ewall0(px)
    g, t, inv, _ = run(px, w)
    ref = backtest(px, w, cost_bps=0.0, freq=FREQ)
    dA = float(np.abs(g - ref["returns"]).max())
    dAt = float(np.abs(t - ref["turnover"]).max())
    print(f"[A] run(no instrument) vs engine.backtest : max|dret| = {dA:.3e}  max|dturn| = {dAt:.3e}")
    assert dA < 1e-12 and dAt < 1e-12

    gg, tt, _, _ = run(px, w * 0.60)
    lev = at_cost(0.60 * g, 0.60 * t, PROTO_COST)
    bkw = at_cost(gg, tt, PROTO_COST)
    print(f"[B] dg convention gap (reported, not asserted): lever(0.60) vs book-at-0.60xw — "
          f"CAGR {m(lev)[0]:.4f} vs {m(bkw)[0]:.4f}, Sharpe {m(lev)[1]:.4f} vs {m(bkw)[1]:.4f}, "
          f"MaxDD {m(lev)[2]:.4f} vs {m(bkw)[2]:.4f}; max|dret| = {float(np.abs(bkw - lev).max()):.3e}")
    print("    dg is priced with idea 66's LEVER convention throughout (exactly proportional by "
          "construction); the book-at-g-weights variant differs only through the engine's cash "
          "re-normalisation and is not used.")

    worst = 0.0
    for s in STRENGTH["stop"]:
        a = run(px, w, stop=s)
        b = ts94.run_stop(px, w, stop=s)
        worst = max(worst, float(np.abs(a[0] - b[0]).max()), float(np.abs(a[1] - b[1]).max()))
        assert a[3] == b[3], (s, a[3], b[3])
    print(f"[C] run(stop=S) vs idea 94 run_stop     : max|diff| over 4 depths = {worst:.3e}")
    assert worst < 1e-12
    print()


# ---------------------------------------------------------------- sweep
def sweep(px, pname, rows, reg_rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = m(spy.loc[OOS_START:])[1]
    base_r = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]

    regs = {a: regime(px, a).loc[start:] for a in ("spy200", "breadth20")}
    for a, v in regs.items():
        reg_rows.append(dict(panel=pname, regime=a, frac=float(v.mean()), days=int(v.sum()),
                             frac_IS=float(v.loc[:IS_END].mean()),
                             frac_OOS=float(v.loc[OOS_START:].mean())))

    for bname, wfn in BASE_BOOKS.items():
        w = wfn(px)
        ctrl_full = run(px, w)
        g_c, t_c, inv_c = (s.loc[start:] for s in ctrl_full[:3])

        sims = {}
        for fam in FAMILIES:
            for lv in STRENGTH[fam]:
                gg, tt, ii, nf = arm_returns(px, w, fam, lv, ctrl_full)
                sims[(fam, lv)] = (gg.loc[start:], tt.loc[start:], ii.loc[start:], nf)

        for cost in COSTS:
            r_c = at_cost(g_c, t_c, cost)
            c_c, s_c, dd_c = m(r_c)
            h1c, h2c = halves(r_c)
            oos_c = m(r_c.loc[OOS_START:])[1]
            rows.append(dict(panel=pname, book=bname, cost=cost, family="none", level=np.nan,
                             fires=0, CAGR=c_c, Sharpe=s_c, MaxDD=dd_c, H1=h1c, H2=h2c,
                             IS_Sharpe=m(r_c.loc[:IS_END])[1], OOS_Sharpe=oos_c,
                             OOS_CAGR=m(r_c.loc[OOS_START:])[0],
                             OOS_MaxDD=m(r_c.loc[OOS_START:])[2],
                             dCAGR=0.0, dSharpe=0.0, dMaxDD=0.0,
                             gross=float(inv_c.mean()), turn_yr=turn_per_yr(t_c),
                             d_crash_ann=0.0, d_trend_ann=0.0, d_crash_b20=0.0, d_trend_b20=0.0,
                             xrate=np.nan,
                             fail4a="|".join(fail4a(r_c, base_r)),
                             fail4b="|".join(fail4b(r_c, spy, oos_c, spy_oos))))

            for (fam, lv), (gg, tt, ii, nf) in sims.items():
                r = at_cost(gg, tt, cost)
                c, sh, dd = m(r)
                h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                d = r - r_c                                   # arm minus its OWN control
                cr = regs["spy200"].reindex(d.index).fillna(False)
                b2 = regs["breadth20"].reindex(d.index).fillna(False)
                bought = (dd - dd_c) * 100                    # pp of MaxDD bought (>0 = shallower)
                paid = (c_c - c) * 100                        # pp of CAGR surrendered
                rows.append(dict(
                    panel=pname, book=bname, cost=cost, family=fam, level=lv, fires=nf,
                    CAGR=c, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                    IS_Sharpe=m(r.loc[:IS_END])[1], OOS_Sharpe=oos,
                    OOS_CAGR=m(r.loc[OOS_START:])[0], OOS_MaxDD=m(r.loc[OOS_START:])[2],
                    dCAGR=(c - c_c) * 100, dSharpe=sh - s_c, dMaxDD=bought,
                    gross=float(ii.mean()), turn_yr=turn_per_yr(tt),
                    d_crash_ann=float(d[cr].mean() * 252 * 100),
                    d_trend_ann=float(d[~cr].mean() * 252 * 100),
                    d_crash_b20=float(d[b2].mean() * 252 * 100),
                    d_trend_b20=float(d[~b2].mean() * 252 * 100),
                    xrate=(paid / bought) if bought > 1e-9 else np.nan,
                    fail4a="|".join(fail4a(r, base_r)),
                    fail4b="|".join(fail4b(r, spy, oos, spy_oos))))

    return dict(panel=pname, spy_CAGR=m(spy)[0], spy_Sharpe=m(spy)[1], spy_MaxDD=m(spy)[2],
                spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                spy_OOS_CAGR=m(spy.loc[OOS_START:])[0], spy_OOS_Sharpe=spy_oos,
                spy_OOS_MaxDD=m(spy.loc[OOS_START:])[2],
                base_CAGR=m(base_r)[0], base_Sharpe=m(base_r)[1], base_MaxDD=m(base_r)[2],
                base_H1=halves(base_r)[0], base_H2=halves(base_r)[1],
                base_OOS_CAGR=m(base_r.loc[OOS_START:])[0],
                base_OOS_Sharpe=m(base_r.loc[OOS_START:])[1],
                base_OOS_MaxDD=m(base_r.loc[OOS_START:])[2])


# ---------------------------------------------------------------- main
def main():
    pd.set_option("display.width", 220)
    print(f"# {SCRIPT}\n# QUEUE idea 245 — does ANY slow drawdown instrument cost less in crashes than in trends?\n")

    rows, reg_rows, bench = [], [], []
    for pname, broad in (("u56", False), ("broad", True)):
        px = load_universe(broad=broad)
        print(f"--- {pname}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")
        if pname == "u56":
            harness(px)
        bench.append(sweep(px, pname, rows, reg_rows))

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    bn = pd.DataFrame(bench).set_index("panel")
    rg = pd.DataFrame(reg_rows)
    rg.to_csv(f"{OUT}.regime.csv", index=False)

    print("\n=== BENCHMARKS over the common sample (RULES v1 weekly @10bps, SPY buy-and-hold) ===")
    print(bn.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n=== REGIME COVERAGE (fraction of days armed) ===")
    print(rg.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    a10 = df[(df.cost == PROTO_COST) & (df.family != "none")]

    print("\n" + "=" * 100)
    print("=== THE PRE-REGISTERED TEST: (arm - own control) annualised, split by SPY<200dMA ===")
    print("pp/yr; d_crash > d_trend  =>  the instrument is CHEAPER IN CRASHES (queue's YES)")
    print("=" * 100)
    prem = a10.groupby(["family", "level"]).agg(
        n=("d_crash_ann", "size"),
        med_crash=("d_crash_ann", "median"), crash_gt0=("d_crash_ann", lambda x: int((x > 0).sum())),
        med_trend=("d_trend_ann", "median"), trend_gt0=("d_trend_ann", lambda x: int((x > 0).sum())),
        cheaper_in_crash=("d_crash_ann", "size")).reset_index()
    cheap = a10.assign(ch=a10.d_crash_ann > a10.d_trend_ann).groupby(["family", "level"]).ch.sum()
    prem["cheaper_in_crash"] = prem.set_index(["family", "level"]).index.map(cheap).astype(int)
    prem["med_gap"] = a10.assign(gap=a10.d_crash_ann - a10.d_trend_ann).groupby(
        ["family", "level"]).gap.median().values
    print(prem.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    prem.to_csv(f"{OUT}.premise.csv", index=False)

    print("\n--- rolled up to the FAMILY (4 levels x 2 panels x 2 books = 16 cells each) ---")
    fam = a10.assign(ch=a10.d_crash_ann > a10.d_trend_ann, gap=a10.d_crash_ann - a10.d_trend_ann)
    famr = fam.groupby("family").agg(
        cells=("gap", "size"), cheaper_in_crash=("ch", "sum"),
        med_crash=("d_crash_ann", "median"), med_trend=("d_trend_ann", "median"),
        med_gap=("gap", "median"), min_gap=("gap", "min"), max_gap=("gap", "max"),
        med_turn=("turn_yr", "median")).reset_index()
    famr["verdict"] = np.where(famr.cheaper_in_crash == famr.cells, "CHEAPER IN CRASHES (all cells)",
                        np.where(famr.cheaper_in_crash == 0, "DEARER IN CRASHES (all cells)", "mixed"))
    print(famr.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    famr.to_csv(f"{OUT}.family.csv", index=False)

    print("\n--- robustness: the SAME split under breadth20 instead of spy200 (never selected on) ---")
    fb = a10.assign(ch=a10.d_crash_b20 > a10.d_trend_b20, gap=a10.d_crash_b20 - a10.d_trend_b20)
    print(fb.groupby("family").agg(cells=("gap", "size"), cheaper_in_crash=("ch", "sum"),
                                   med_crash=("d_crash_b20", "median"),
                                   med_trend=("d_trend_b20", "median"),
                                   med_gap=("gap", "median")).to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n--- by panel x book, 10 bps, median over the family's 4 levels (gap = crash - trend, pp/yr) ---")
    piv = fam.groupby(["panel", "book", "family"]).gap.median().unstack("family")
    print(piv.to_string(float_format=lambda x: f"{x:+.3f}"))

    print("\n--- cost robustness: the same family roll-up at 25 bps ---")
    a25 = df[(df.cost == 25) & (df.family != "none")]
    f25 = a25.assign(ch=a25.d_crash_ann > a25.d_trend_ann, gap=a25.d_crash_ann - a25.d_trend_ann)
    print(f25.groupby("family").agg(cells=("gap", "size"), cheaper_in_crash=("ch", "sum"),
                                    med_gap=("gap", "median")).to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 100)
    print("=== FULL GRID at 10 bps (every arm, nothing withheld) ===")
    print("=" * 100)
    show = ["panel", "book", "family", "level", "fires", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "dCAGR", "dSharpe", "dMaxDD", "turn_yr",
            "d_crash_ann", "d_trend_ann", "fail4a", "fail4b"]
    print(df[df.cost == PROTO_COST][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== FULL GRID at 25 bps ===")
    print(df[df.cost == 25][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== KEEP paths, both evaluated, 10 bps ===")
    arms10 = df[(df.cost == PROTO_COST) & (df.family != "none")]
    p4a = arms10[arms10.fail4a == ""]
    p4b = arms10[arms10.fail4b == ""]
    print(f"4a passes: {len(p4a)} / {len(arms10)} instrument arms")
    if len(p4a):
        print(p4a[["panel", "book", "family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"4b passes: {len(p4b)} / {len(arms10)} instrument arms")
    if len(p4b):
        print(p4b[["panel", "book", "family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "OOS_Sharpe", "turn_yr"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ctl = df[(df.cost == PROTO_COST) & (df.family == "none")]
    print("\ncontrols (context): 4a passes "
          f"{int((ctl.fail4a == '').sum())}/{len(ctl)}, 4b passes {int((ctl.fail4b == '').sum())}/{len(ctl)}")
    print(ctl[["panel", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
               "fail4a", "fail4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 100)
    print("=== RULE 8 WALK-FORWARD: (family, level) chosen on 2009-2016 IS Sharpe, 2017-2026 untouched ===")
    print("=" * 100)
    wf = []
    for (pn, bk, cost), g in df.groupby(["panel", "book", "cost"]):
        arms = g[g.family != "none"]
        ctrl = g[g.family == "none"].iloc[0]
        pick = arms.loc[arms.IS_Sharpe.idxmax()]
        best = arms.loc[arms.OOS_Sharpe.idxmax()]
        b = bn.loc[pn]
        wf.append(dict(panel=pn, book=bk, cost=cost,
                       pick=f"{pick.family}/{pick.level}", IS_Sharpe=pick.IS_Sharpe,
                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                       ctrl_OOS_CAGR=ctrl.OOS_CAGR, ctrl_OOS_Sharpe=ctrl.OOS_Sharpe,
                       ctrl_OOS_MaxDD=ctrl.OOS_MaxDD,
                       regret=pick.OOS_Sharpe - ctrl.OOS_Sharpe,
                       best_oos=f"{best.family}/{best.level}", best_OOS_Sharpe=best.OOS_Sharpe,
                       base_OOS_CAGR=b.base_OOS_CAGR, base_OOS_Sharpe=b.base_OOS_Sharpe,
                       base_OOS_MaxDD=b.base_OOS_MaxDD,
                       spy_OOS_CAGR=b.spy_OOS_CAGR, spy_OOS_Sharpe=b.spy_OOS_Sharpe,
                       spy_OOS_MaxDD=b.spy_OOS_MaxDD))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(wfd.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\nIS chooser vs the do-nothing control, OOS Sharpe: mean regret {wfd.regret.mean():+.4f}, "
          f"median {wfd.regret.median():+.4f}, wins {int((wfd.regret > 0).sum())}/{len(wfd)}")

    print("\n--- rule 8 restricted to the SLOW instruments only (the queue's actual set) ---")
    wfs = []
    for (pn, bk, cost), g in df.groupby(["panel", "book", "cost"]):
        arms = g[g.family.isin(SLOW)]
        ctrl = g[g.family == "none"].iloc[0]
        pick = arms.loc[arms.IS_Sharpe.idxmax()]
        wfs.append(dict(panel=pn, book=bk, cost=cost, pick=f"{pick.family}/{pick.level}",
                        IS_Sharpe=pick.IS_Sharpe, OOS_Sharpe=pick.OOS_Sharpe,
                        OOS_CAGR=pick.OOS_CAGR, OOS_MaxDD=pick.OOS_MaxDD,
                        ctrl_OOS_Sharpe=ctrl.OOS_Sharpe,
                        regret=pick.OOS_Sharpe - ctrl.OOS_Sharpe))
    wfsd = pd.DataFrame(wfs)
    print(wfsd.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"slow-only: mean regret {wfsd.regret.mean():+.4f}, wins {int((wfsd.regret > 0).sum())}/{len(wfsd)}")

    print(f"\nwrote {OUT}.grid.csv / .premise.csv / .family.csv / .regime.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
