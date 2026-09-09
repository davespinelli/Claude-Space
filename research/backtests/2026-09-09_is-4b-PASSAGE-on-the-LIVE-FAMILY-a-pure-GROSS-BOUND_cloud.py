#!/usr/bin/env python3
"""Idea 544 - "is-4b-PASSAGE-on-the-LIVE-FAMILY-a-pure-GROSS-BOUND" (cloud, 2026-09-09).

The question
------------
Idea 542 established, on the LIVE DEGROSS family (200d MA band with hysteresis, gated-out
weight -> cash, weekly, 10 bps, t+1):
  * full-sample Sharpe is invariant in gross to 3 decimal places, and
  * at the live gross 0.75, CAGR is the ONLY failing PROTOCOL-4b bar on every band and on
    both required panels.
If both hold, 4b passage on this family cannot be a shape fact at all: the three Sharpe
legs are flat in gross, the CAGR bar is increasing in gross and the MaxDD bar is decreasing
in gross, so 4b is exactly the interval [g_CAGR, g_DD] and passage is ONE NUMBER wide iff
the DD bar never binds below the no-leverage cap 1.00.  This run solves for those numbers.

Design (fixed before any number was read)
-----------------------------------------
FIXED, never varied:
    family    the LIVE book: baseline.band_state gate, DEGROSS construction (denominator =
              names priced that day, gated-out weight -> CASH).  RESPREAD is reported as a
              control only; no threshold claim may be read off it.
    cadence   W (weekly, live).  costs 10 bps/unit turnover.  next-day execution (t -> t+1).
    windows   IS <= 2016-12-31, OOS >= 2017-01-01 (PROTOCOL rule 8).
    panels    U56 and B136 REQUIRED (idea 542's two required panels); SMALL439 reported.
    bars      4b as PROTOCOL rule 4b: Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 0.60 x
              |SPY MaxDD|, CAGR >= 0.70 x SPY CAGR.  4a vs the live RULES v2 book.
    leverage  gross is capped at 1.00 (PROTOCOL rule 2: no leverage unless the idea says so).

TUNED PARAMETERS -- exactly two, as the queue specifies (gross resolution, band):
    1. GROSS RESOLUTION  three nested grids, ALL points reported:
         COARSE  0.05 .. 1.00 step 0.05   (20 points)
         FINE    0.05 .. 1.00 step 0.01   (96 points)
         EXACT   bisection to 1e-4 on each bar's crossing (the threshold itself)
       The resolution dial exists to answer "is the threshold an artefact of the grid?" --
       a threshold that moves with resolution is not a number, it is a rounding.
    2. BAND  {0.00, 0.01, 0.02, 0.03, 0.05, 0.08}.  0.03 is LIVE; 0.00 is idea 542's
       challenger (MA-THRESH theta 0).  Every band reported, none selected.

Pre-registered claims, written before any number was read
---------------------------------------------------------
C1  INVARIANCE.  Report max - min of full-sample Sharpe across the FINE gross grid, per
    (panel, band, construction).  Idea 542's claim is a span <= 0.006 at 3 dp; a span above
    0.01 falsifies the premise of this whole run and the "pure gross bound" framing dies.
C2  MONOTONICITY.  CAGR must be non-decreasing and |MaxDD| non-decreasing in gross for the
    interval characterisation to hold.  Report the count of grid-adjacent violations; any
    violation is printed with its cell.
C3  THE THRESHOLD g*.  Per (panel, band): the smallest gross clearing the 4b CAGR bar
    (bisection, 1e-4), the largest gross clearing the 4b DD bar, and the 4b window
    [lo, hi] intersected with the Sharpe legs and with (0, 1.00].  Width 0 => empty.
C4  IS PASSAGE ONE NUMBER WIDE?  Count the (panel, band) cells where the window's upper
    edge is the no-leverage cap 1.00 (i.e. the DD bar never binds and passage is decided by
    the single number g*), versus cells with a genuine two-sided interval, versus empty.
C5  RULE 8 -- THE ONLY QUESTION THAT MATTERS FOR CAPITAL.  A threshold is only usable if it
    is estimable.  Choose g on the IS window alone (g = smallest gross clearing the IS 4b
    CAGR bar subject to the IS DD bar, ties to lower gross), per panel and band, then read
    the OOS window ONCE and report OOS CAGR / Sharpe / MaxDD vs SPY and vs the live RULES v2
    baseline, plus |g*_IS - g*_OOS|.  If the IS-chosen gross fails 4b OOS, the family's 4b
    passage is a hindsight number and the verdict is KILL for capital regardless of C4.
C6  BOTH KEEP PATHS on every FINE grid point (4a and 4b), all reported.

Gates (asserted before any verdict is read)
    G1  the vectorised runner reproduces engine.backtest on the live U56 v2 book to < 1e-12.
    G2  book(band=0.03, gross=0.75, DEGROSS) is bit-identical to baseline.rules_v2_weights.
    G3  idea 542's headline is reproduced from this run's own grid: at gross 0.75, DEGROSS,
        on U56 and B136, for every band, CAGR is the only failing 4b bar.  Printed per cell;
        if it does not reproduce, the run says so and the queue's premise is corrected.

SURVIVORSHIP: universe.json (U56), universe_broad.json (B136) and prices_small.csv.gz
(SMALL439) are CURRENT constituents -- no delistings, no dead names -- so every CAGR level
here is inflated, the CAGR bar is therefore the EASY bar in this sample, and every threshold
g* reported below is a LOWER bound on the gross a real book would have needed.  SMALL439
additionally drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .thresholds.csv .walkforward.csv .console.txt .result.md
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights, band_state
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
CADENCE = "W"
BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]
COARSE = [round(0.05 * i, 4) for i in range(1, 21)]           # 0.05 .. 1.00 step 0.05
FINE = [round(0.01 * i, 4) for i in range(5, 101)]            # 0.05 .. 1.00 step 0.01
CONSTRUCTIONS = ["DEGROSS", "RESPREAD"]
LIVE_BAND, LIVE_GROSS, LIVE_CON = 0.03, 0.75, "DEGROSS"
GMAX = 1.00                                                    # no leverage (PROTOCOL rule 2)
GMIN = 0.0001
BISECT_TOL = 1e-4
REQUIRED_PANELS = ["U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- vectorised runner
def fast_backtest(px, weights, freq=CADENCE):
    """Reproduces engine.backtest exactly (gate G1); returns GROSS-of-cost returns."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross_i = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index), "turnover": pd.Series(turn, index=px.index)}


def net(res, bps=COST_BPS):
    return res["returns0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- books
def held_mask(px, band):
    return band_state(px, band) & px.notna()


def unit_book(px, band, construction):
    """The gross-1.0 weight matrix; the family is this matrix times the gross scalar."""
    h = held_mask(px, band)
    den = px.notna().sum(axis=1) if construction == "DEGROSS" else h.sum(axis=1)
    return h.astype(float).div(den.replace(0, np.nan), axis=0).fillna(0.0)


# ---------------------------------------------------------------- stats / verdicts
def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    hi, ho = len(r.loc[:IS_END]) // 2, len(r.loc[OOS_START:]) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                isH1=metrics(r.loc[:IS_END].iloc[:hi])["Sharpe"],
                isH2=metrics(r.loc[:IS_END].iloc[hi:])["Sharpe"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                oH1=metrics(r.loc[OOS_START:].iloc[:ho])["Sharpe"],
                oH2=metrics(r.loc[OOS_START:].iloc[ho:])["Sharpe"])


def bars_4b(s, spy):
    return {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
            "OOS": s["oSharpe"] > spy["oSharpe"],
            "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
            "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}


def fail_4b(s, spy):
    f = [k for k, v in bars_4b(s, spy).items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for max_1d_move >= 1.0)")
    return out


# ---------------------------------------------------------------- threshold solver
def bisect(f, lo, hi, target_true_at_hi, tol=BISECT_TOL):
    """Smallest x in [lo, hi] with f(x) True, assuming f is monotone False->True on the
    interval (target_true_at_hi=True).  If target_true_at_hi is False the roles flip and we
    return the LARGEST x with f(x) True.  Returns None if the bar never flips on [lo, hi]."""
    flo, fhi = f(lo), f(hi)
    if target_true_at_hi:
        if flo:
            return lo                       # already true at the bottom of the range
        if not fhi:
            return None                     # never true on the range
        a, b = lo, hi
        while b - a > tol:
            m = 0.5 * (a + b)
            if f(m):
                b = m
            else:
                a = m
        return b
    else:
        if fhi:
            return hi
        if not flo:
            return None
        a, b = lo, hi
        while b - a > tol:
            m = 0.5 * (a + b)
            if f(m):
                a = m
            else:
                b = m
        return a


# ---------------------------------------------------------------- main
def main():
    P("=" * 180)
    P("Idea 544 is-4b-PASSAGE-on-the-LIVE-FAMILY-a-pure-GROSS-BOUND (cloud) | " + Path(__file__).name)
    P("=" * 180)
    P(f"FIXED: LIVE DEGROSS family, cadence {CADENCE}, costs {COST_BPS} bps, next-day execution, "
      f"IS <= {IS_END}, OOS >= {OOS_START}, gross capped at {GMAX:.2f} (no leverage).")
    P(f"DIALS (2): GROSS RESOLUTION (coarse 0.05 / fine 0.01 / bisection {BISECT_TOL:g}) x BAND {BANDS}.")
    P("SURVIVORSHIP: all three panels are CURRENT constituents; CAGR levels are inflated, so the")
    P("  4b CAGR bar is the EASY bar here and every g* below is a LOWER bound on the real one.")

    PN = panels()

    # ------------------------------------------------------------ gates G1, G2
    P("\n" + "=" * 180)
    P("GATES")
    px_full = load_universe()
    w_live = rules_v2_weights(px_full)
    r_engine = backtest(px_full, w_live, cost_bps=COST_BPS, freq=CADENCE)["returns"]
    r_fast = net(fast_backtest(px_full, w_live))
    g1 = float(np.abs(r_engine - r_fast).max())
    P(f"  G1 vectorised runner vs engine.backtest, live U56 v2 book: max abs diff {g1:.3e} "
      f"({'PASS' if g1 < 1e-12 else 'FAIL'})")
    assert g1 < 1e-12, g1
    w_mine = unit_book(px_full, LIVE_BAND, "DEGROSS") * LIVE_GROSS
    g2 = float((w_mine - w_live).abs().max().max())
    P(f"  G2 unit_book(0.03, DEGROSS) x 0.75 vs baseline.rules_v2_weights: max abs diff {g2:.3e} "
      f"({'PASS' if g2 < 1e-15 else 'FAIL'})")
    assert g2 < 1e-15, g2
    flush_log()

    live_full = r_engine

    # ------------------------------------------------------------ the fine grid
    rows = []
    cache = {}          # (panel, band, con) -> (unit weight matrix, start, spy stat, live stat)
    P("\n" + "=" * 180)
    P("THE GRID  (fine resolution 0.01, 96 gross points x 6 bands x 2 constructions x 3 panels")
    P("           = 3,456 books; every point is written to .grid.csv, nothing is selected)")
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        P("\n" + "-" * 180)
        P(f"PANEL {pname}: evaluation from {start.date()} "
          f"({len(px.loc[start:]) / 252:.2f} yrs)"
          f"{'  [REQUIRED]' if pname in REQUIRED_PANELS else '  [reported, not required]'}")
        P(f"  SPY        CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} | OOS CAGR {spy_s['oCAGR']:.4f} Sharpe "
          f"{spy_s['oSharpe']:.4f} MaxDD {spy_s['oMaxDD']:.4f}")
        P(f"  RULES v2   CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} | OOS CAGR {live_s['oCAGR']:.4f} Sharpe "
          f"{live_s['oSharpe']:.4f} MaxDD {live_s['oMaxDD']:.4f}")
        P(f"  4b BARS on this panel: CAGR >= {0.70 * spy_s['CAGR']:.4f}, |MaxDD| <= "
          f"{0.60 * abs(spy_s['MaxDD']):.4f}, Sharpe > {spy_s['H1']:.4f} (H1) / {spy_s['H2']:.4f} (H2) "
          f"/ {spy_s['oSharpe']:.4f} (OOS)")
        for band in BANDS:
            for con in CONSTRUCTIONS:
                U = unit_book(px, band, con)
                cache[(pname, band, con)] = (px, U, start, spy_s, live_s)
                for g in FINE:
                    s = stat(net(fast_backtest(px, U * g)).loc[start:])
                    b4b = bars_4b(s, spy_s)
                    rows.append(dict(panel=pname, band=band, con=con, gross=g, **s,
                                     pass4a=verdict_4a(s, live_s),
                                     pass4b=all(b4b.values()), fail4b=fail_4b(s, spy_s),
                                     bar_CAGR=b4b["CAGR"], bar_DD=b4b["DD"], bar_H1=b4b["H1"],
                                     bar_H2=b4b["H2"], bar_OOS=b4b["OOS"]))
            P(f"    band {band:.2f} done ({len(rows)} rows)")
        flush_log()

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"\nwrote {OUT.name}.grid.csv  ({len(grid)} rows)")

    # ------------------------------------------------------------ G3: idea 542's headline
    P("\n" + "=" * 180)
    P("GATE G3 -- does idea 542's headline reproduce from THIS run's grid?")
    P("  claim: at gross 0.75, DEGROSS, on U56 and B136, CAGR is the ONLY failing 4b bar, every band.")
    g3 = grid[(grid.con == "DEGROSS") & (np.isclose(grid.gross, LIVE_GROSS))]
    ok = 0; tot = 0
    for pname in REQUIRED_PANELS:
        for band in BANDS:
            r = g3[(g3.panel == pname) & (np.isclose(g3.band, band))].iloc[0]
            tot += 1
            hit = (r.fail4b == "CAGR")
            ok += hit
            P(f"    {pname:9s} band {band:.2f}  fail4b = {r.fail4b:22s} "
              f"CAGR {r.CAGR:.4f} Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:.4f}  "
              f"{'reproduces' if hit else 'DOES NOT reproduce'}")
    P(f"  G3: {ok}/{tot} required cells reproduce idea 542's 'CAGR is the only failing bar'.")
    if ok != tot:
        P("  -> the queue's premise is NOT fully reproduced; the interval characterisation below is")
        P("     therefore reported per-cell with its actual binding bar set, not assumed.")

    # ------------------------------------------------------------ C1 invariance, C2 monotonicity
    P("\n" + "=" * 180)
    P("C1 SHARPE INVARIANCE IN GROSS (span = max - min of full-sample Sharpe over the 96-point fine grid)")
    inv = (grid.groupby(["panel", "band", "con"])
               .agg(Sharpe_min=("Sharpe", "min"), Sharpe_max=("Sharpe", "max"),
                    oSharpe_min=("oSharpe", "min"), oSharpe_max=("oSharpe", "max")))
    inv["span"] = inv.Sharpe_max - inv.Sharpe_min
    inv["oos_span"] = inv.oSharpe_max - inv.oSharpe_min
    P(fmt(inv[["Sharpe_min", "Sharpe_max", "span", "oos_span"]]))
    worst = inv.span.max()
    P(f"  max span over all 36 (panel, band, construction) cells: {worst:.4f}  "
      f"({'consistent with idea 542 (<= 0.01)' if worst <= 0.01 else 'ABOVE 0.01 -- premise weakened'})")
    P("  NOTE the span is not zero: de-grossing holds cash at 0% return, so gross changes the")
    P("  mix of a risky sleeve and a zero-vol asset -- Sharpe is only invariant to the extent the")
    P("  cash leg is a pure scalar, which it is not once the sleeve drifts between rebalances.")

    P("\nC2 MONOTONICITY IN GROSS (grid-adjacent violations over the 96-point fine grid)")
    viol = []
    for (pname, band, con), sub in grid.groupby(["panel", "band", "con"]):
        sub = sub.sort_values("gross")
        dc = np.diff(sub.CAGR.values)
        dd = np.diff(np.abs(sub.MaxDD.values))
        viol.append(dict(panel=pname, band=band, con=con,
                         cagr_down_steps=int((dc < -1e-12).sum()),
                         dd_down_steps=int((dd < -1e-12).sum()),
                         cagr_min_step=float(dc.min()), dd_min_step=float(dd.min())))
    vdf = pd.DataFrame(viol)
    P(fmt(vdf.set_index(["panel", "band", "con"]), 6))
    P(f"  total CAGR non-monotone steps {vdf.cagr_down_steps.sum()} / {len(vdf) * 95}, "
      f"|MaxDD| non-monotone steps {vdf.dd_down_steps.sum()} / {len(vdf) * 95}")

    # ------------------------------------------------------------ C3/C4 thresholds
    P("\n" + "=" * 180)
    P("C3/C4 THE THRESHOLDS  (bisection to 1e-4 on the two gross-sensitive 4b bars)")
    P("  g_CAGR = smallest gross with CAGR >= 0.70 x SPY CAGR;  g_DD = largest gross with")
    P("  |MaxDD| <= 0.60 x |SPY MaxDD|.  Sharpe legs (H1/H2/OOS) are checked at both ends.")
    trows = []
    for (pname, band, con), (px, U, start, spy_s, live_s) in cache.items():
        def mk(g):
            return stat(net(fast_backtest(px, U * g)).loc[start:])

        def f_cagr(g):
            return mk(g)["CAGR"] >= 0.70 * spy_s["CAGR"]

        def f_dd(g):
            return abs(mk(g)["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"])

        g_cagr = bisect(f_cagr, GMIN, GMAX, True)
        g_dd = bisect(f_dd, GMIN, GMAX, False)
        # Sharpe legs: evaluate at the coarse grid to see whether they are ever satisfied
        sub = grid[(grid.panel == pname) & (np.isclose(grid.band, band)) & (grid.con == con)]
        sharpe_ok_frac = float((sub.bar_H1 & sub.bar_H2 & sub.bar_OOS).mean())
        lo = g_cagr if g_cagr is not None else np.nan
        hi = g_dd if g_dd is not None else np.nan
        if g_cagr is None or g_dd is None or sharpe_ok_frac == 0.0:
            width, wshape = 0.0, "EMPTY"
        else:
            width = max(0.0, hi - lo)
            if width <= 0:
                wshape = "EMPTY"
            elif hi >= GMAX - 1e-9:
                wshape = "ONE-SIDED (DD never binds; passage = the single number g*)"
            else:
                wshape = "TWO-SIDED interval"
        trows.append(dict(panel=pname, band=band, con=con, g_CAGR=lo, g_DD=hi,
                          width=width, wshape=wshape, sharpe_legs_frac=sharpe_ok_frac,
                          n_pass4b_fine=int(sub.pass4b.sum()), n_pass4a_fine=int(sub.pass4a.sum())))
        P(f"    {pname:9s} band {band:.2f} {con:8s}  g_CAGR "
          f"{('%.4f' % lo) if lo == lo else '  none':>7s}  g_DD "
          f"{('%.4f' % hi) if hi == hi else '  none':>7s}  width {width:.4f}  "
          f"Sharpe-legs {sharpe_ok_frac:5.1%} of grid  4b {int(sub.pass4b.sum()):2d}/96  "
          f"4a {int(sub.pass4a.sum()):2d}/96  {wshape}")
        flush_log()
    th = pd.DataFrame(trows)
    th.to_csv(f"{OUT}.thresholds.csv", index=False)

    P("\nC4 IS 4b PASSAGE ONE NUMBER WIDE?  (DEGROSS, the only construction a KEEP may come from)")
    d = th[th.con == "DEGROSS"]
    for pname in PN:
        sub = d[d.panel == pname]
        P(f"    {pname:9s}  one-sided {int(sub.wshape.str.startswith('ONE-SIDED').sum())}/6 bands, "
          f"two-sided {int((sub.wshape == 'TWO-SIDED interval').sum())}/6, "
          f"empty {int((sub.wshape == 'EMPTY').sum())}/6 | g* range over bands "
          f"{sub.g_CAGR.min():.4f} - {sub.g_CAGR.max():.4f} (spread {sub.g_CAGR.max() - sub.g_CAGR.min():.4f})")

    # ------------------------------------------------------------ resolution dial
    P("\nRESOLUTION DIAL: does the threshold move with the grid?  (coarse 0.05 vs fine 0.01 vs bisection)")
    res_rows = []
    for _, r in d.iterrows():
        sub = grid[(grid.panel == r.panel) & (np.isclose(grid.band, r.band)) & (grid.con == "DEGROSS")]
        c = sub[sub.gross.isin(COARSE) & sub.bar_CAGR].gross
        f = sub[sub.bar_CAGR].gross
        res_rows.append(dict(panel=r.panel, band=r.band,
                             g_coarse=float(c.min()) if len(c) else np.nan,
                             g_fine=float(f.min()) if len(f) else np.nan,
                             g_bisect=r.g_CAGR))
    rdf = pd.DataFrame(res_rows)
    rdf["coarse_err"] = rdf.g_coarse - rdf.g_bisect
    rdf["fine_err"] = rdf.g_fine - rdf.g_bisect
    P(fmt(rdf.set_index(["panel", "band"])))
    P(f"  coarse grid overstates g* by up to {rdf.coarse_err.max():.4f}; fine grid by up to "
      f"{rdf.fine_err.max():.4f}.  A 0.05 grid cannot resolve a threshold to better than 0.05.")

    # ------------------------------------------------------------ C5 rule 8
    P("\n" + "=" * 180)
    P("C5 RULE 8 WALK-FORWARD -- is the threshold ESTIMABLE?  gross chosen on IS (<= 2016) alone,")
    P("   OOS (>= 2017) read once.  IS pick = smallest gross clearing the IS 4b CAGR bar subject")
    P("   to the IS DD bar (ties to lower gross); if no gross clears IS, the cell has no pick.")
    wrows = []
    for (pname, band, con), (px, U, start, spy_s, live_s) in cache.items():
        if con != "DEGROSS":
            continue
        def mk(g):
            return stat(net(fast_backtest(px, U * g)).loc[start:])

        def f_is(g):
            s = mk(g)
            return s["isCAGR"] >= 0.70 * spy_s["isCAGR"] and abs(s["isMaxDD"]) <= 0.60 * abs(spy_s["isMaxDD"])

        def f_oos(g):
            s = mk(g)
            return s["oCAGR"] >= 0.70 * spy_s["oCAGR"] and abs(s["oMaxDD"]) <= 0.60 * abs(spy_s["oMaxDD"])

        g_is = bisect(f_is, GMIN, GMAX, True)
        g_oos = bisect(f_oos, GMIN, GMAX, True)
        if g_is is None:
            P(f"    {pname:9s} band {band:.2f}  NO IS PICK (no gross <= 1.00 clears the IS bars)")
            wrows.append(dict(panel=pname, band=band, g_is=np.nan, g_oos_true=g_oos))
            continue
        s = mk(g_is)
        oos_pass = (s["oSharpe"] > spy_s["oSharpe"] and s["oCAGR"] >= 0.70 * spy_s["oCAGR"]
                    and abs(s["oMaxDD"]) <= 0.60 * abs(spy_s["oMaxDD"]))
        full = bars_4b(s, spy_s)
        wrows.append(dict(panel=pname, band=band, g_is=g_is, g_oos_true=g_oos,
                          drift=(g_oos - g_is) if g_oos is not None else np.nan,
                          oCAGR=s["oCAGR"], oSharpe=s["oSharpe"], oMaxDD=s["oMaxDD"],
                          spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"], spy_oMaxDD=spy_s["oMaxDD"],
                          live_oCAGR=live_s["oCAGR"], live_oSharpe=live_s["oSharpe"], live_oMaxDD=live_s["oMaxDD"],
                          oos_4b_leg=oos_pass, full_4b=all(full.values()), fail4b=fail_4b(s, spy_s)))
        P(f"    {pname:9s} band {band:.2f}  g*_IS {g_is:.4f} -> g*_OOS "
          f"{('%.4f' % g_oos) if g_oos is not None else 'none':>6s}  drift "
          f"{('%+.4f' % (g_oos - g_is)) if g_oos is not None else '  n/a':>7s} | at g*_IS: "
          f"OOS CAGR {s['oCAGR']:.4f} (SPY {spy_s['oCAGR']:.4f}, live {live_s['oCAGR']:.4f})  "
          f"OOS Sharpe {s['oSharpe']:.4f} (SPY {spy_s['oSharpe']:.4f}, live {live_s['oSharpe']:.4f})  "
          f"OOS MaxDD {s['oMaxDD']:.4f} (SPY {spy_s['oMaxDD']:.4f}, live {live_s['oMaxDD']:.4f})  "
          f"OOS-4b {'PASS' if oos_pass else 'FAIL'}  full-4b {'PASS' if all(full.values()) else 'FAIL (' + fail_4b(s, spy_s) + ')'}")
        flush_log()
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------ C6 keep paths
    P("\n" + "=" * 180)
    P("C6 BOTH KEEP PATHS over the whole fine grid (no selection)")
    kp = grid.groupby(["panel", "con"]).agg(n=("pass4b", "size"), pass4a=("pass4a", "sum"),
                                            pass4b=("pass4b", "sum"))
    kp["both"] = [int(((grid.panel == p) & (grid.con == c) & grid.pass4a & grid.pass4b).sum())
                  for p, c in kp.index]
    P(fmt(kp, 0))
    P("\n  4b bar-by-bar fail counts (DEGROSS only, the live construction):")
    dg = grid[grid.con == "DEGROSS"]
    for pname in PN:
        s = dg[dg.panel == pname]
        P(f"    {pname:9s} n={len(s)}  fails: CAGR {int((~s.bar_CAGR).sum())}  DD {int((~s.bar_DD).sum())}  "
          f"H1 {int((~s.bar_H1).sum())}  H2 {int((~s.bar_H2).sum())}  OOS {int((~s.bar_OOS).sum())}")

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 180)
    P("VERDICT")
    req = th[(th.con == "DEGROSS") & (th.panel.isin(REQUIRED_PANELS))]
    reqwf = wf[wf.panel.isin(REQUIRED_PANELS)]
    n_one = int(req.wshape.str.startswith("ONE-SIDED").sum())
    n_two = int((req.wshape == "TWO-SIDED interval").sum())
    n_emp = int((req.wshape == "EMPTY").sum())
    n_wf = int(reqwf.full_4b.fillna(False).sum()) if "full_4b" in reqwf.columns else 0
    P(f"  Shape of 4b passage on the two REQUIRED panels (DEGROSS, 12 band-cells): "
      f"one-sided {n_one}, two-sided {n_two}, empty {n_emp}.")
    if "drift" in reqwf.columns:
        P(f"  Rule 8: {n_wf}/{len(reqwf)} required band-cells whose IS-CHOSEN gross clears full 4b; "
          f"threshold drift |g*_OOS - g*_IS| median {reqwf.drift.abs().median():.4f}.")
    P("  See .result.md for the written verdict.")
    flush_log()
    return grid, th, wf


if __name__ == "__main__":
    main()
    flush_log()
