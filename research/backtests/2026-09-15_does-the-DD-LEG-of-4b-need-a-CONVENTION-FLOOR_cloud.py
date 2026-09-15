#!/usr/bin/env python3
"""Idea 808 (cloud lane, 2026-09-15) - does-the-DD-LEG-of-PROTOCOL-4b-need-a-DECLARED-CONVENTION-FLOOR.

QUESTION
--------
Idea 805 killed the U56 / MA-DG / MONTHLY / g=1.00 book on ONE leg: shift the monthly rebalance off
month end and 4b holds at only 13 of 21 trading-day offsets, all 8 failures on the DRAWDOWN leg
alone, because that book's DD-cap margin (4.74pp) is SMALLER than its own 21-offset MaxDD spread
(8.37pp) while CAGR and all three Sharpe legs held at every offset.  That is one book.  This run
asks whether the asymmetry is a PROPERTY OF THE DD LEG across a declared book set, and prices the
PROTOCOL clause the queue proposes: a 4b DD pass must clear its cap by MORE than the book's own
offset spread.

WHAT IS MEASURED
----------------
For every book x every rebalance calendar in a declared convention family, the five 4b legs are
recorded as MARGINS in their own units (Sharpe points for H1/H2/OOS, percentage points for DD and
CAGR), not as booleans.  Per leg per book:
    margin(k=0)  the margin on PROTOCOL's own calendar (the number the record publishes)
    spread       max - min of that margin across the offsets (the convention floor, FULLSPREAD)
    sd           its standard deviation across offsets
    ratio        margin(k=0) / spread   -- unit-free WITHIN a leg, so legs are comparable
    flips        how many offsets disagree with k=0 on the leg's own pass/fail
A leg whose ratio < 1 is a leg whose published verdict is a date, not a rule.

THE BOOK SET (param 1, DECLARED IN FULL; nothing in it is chosen by anything below)
-----------------------------------------------------------------------------------
6 forms x 2 panels = 12 books.  Every form is a book the record already prices; none was picked
after seeing an offset number.  All are long-only, no leverage, cash-settled de-gross.
  MADG100   idea 805's own book: w_i = g/N over ALL priced names, zeroed below the 200d MA
            (weight to CASH, never re-spread), g = 1.00.
  MADG075   the same at g = 0.75.
  TOP20     the 2026-09-04 first KEEP 4b: top 20 eligible names by the v1 composite WITHOUT the
            /sqrt(vol20) term, equal weight 0.75/20, v1 eligibility (above 200d AND vol20 < 0.60).
  TOP40     idea 589/806's book: top 40 eligible by the same composite, g/N each at g = 1.00.
  EWELIG    the 2026-09-03 Finding 2 book: equal weight over ALL eligible names, gross 0.75.
  RULESV2   the LIVE rules: every name inside the 200d +/-3% hysteresis band at 0.75/N, cash
            otherwise (baseline.rules_v2_weights, verbatim).
  PANELS    U56 = research/universe.json via load_universe(); B136 = load_universe(broad=True).
            SPY is a tradable constituent of both AND the 4b comparand (the record's construction,
            not changed here).

THE CONVENTION FAMILY (structural, reported in full, never selected)
  MONTHLY   21 sleeves, k = 0..20 trading days after each month end (idea 805's own family;
            k = 0 is PROTOCOL's calendar).
  WEEKLY    5 sleeves, k = 0..4 trading days after each week end.
  Both families are run for every book, so "the live book is weekly" is not an escape hatch:
  the same question is asked of the calendar each book actually uses and of the other one.

THE FLOOR FORM (param 2)
  FULLSPREAD   floor = max - min of the leg margin across the family's offsets (the queue's own).
  SD1          floor = 1 standard deviation across offsets.
  SD2          floor = 2 standard deviations.
  All three are reported for every leg of every book; the clause is priced under each.

REPORTED-NEVER-SELECTED: cost rungs 10 / 25 bps, execution lag 1 / 2 days, window (FULL / IS /
OOS), path 4a against RULES v2 (live), realised gross, turnover, and every one of the 12 x 26 x 2
book-offset-lag cells, pass or fail.

GATES (printed before any hypothesis is read)
  G1 engine : fast_run vs engine.backtest on MADG100/U56, k=0 monthly, lag 1, 10 bps.   bar 1e-9
  G2 repro  : (a) MADG100/U56 at k=0 reproduces idea 804/805's published triple to the half-unit
              of its last published digit (CAGR 11.92%, Sharpe 1.21, MaxDD -15.5%).  The panel has
              gained trading days since 805 ran, so CAGR is allowed to miss and the miss is
              PRINTED rather than hidden; Sharpe and MaxDD must hold.
              (b) idea 805's H_CAL census: 13 of 21 offsets pass 4b at g=1.00 / 10 bps / lag 1,
              all 8 failures on the DD leg alone.
              (c) the two numbers the queue quotes: DD-cap margin 4.74pp, 21-offset MaxDD spread
              8.37pp, bar 0.10pp each.
              If (b) fails, this is not the phenomenon the idea is about and it is said so.
  G3 bars   : RULES v2 (live) and SPY printed on this window with all four 4b bars as numbers.

PRE-REGISTERED HYPOTHESES (written before any number below was run; the only numbers in hand are
ideas 804/805's published ones, which the queue itself quotes)
  H_DDWORST : across the 12 books, the DD leg has the LOWEST median margin/spread ratio of the five
              4b legs on the MONTHLY family.  (805's asymmetry is a leg property, not a book fact.)
  H_DDFLIP  : the DD leg accounts for a strict majority of all leg-level offset flips across the
              book set.
  H_BITE    : the clause (margin > FULLSPREAD floor) demotes at least one book that passes 4b at
              k=0, i.e. it is not vacuous.
  H_WF      : the IS-window offset spread PREDICTS the OOS-window offset spread (Spearman rho >
              +0.5 per leg across books), so the floor is knowable in sample - which is the only
              way a PROTOCOL clause can be applied before the outcome window is read.
  H_CADENCE : the WEEKLY family's spreads are SMALLER than the MONTHLY family's for the same book
              (more rebalances per year -> less calendar luck), so the clause binds mainly monthly.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
  IS = window start .. 2016-12-31 (read and fitted), OOS = 2017-01-01 .. end (read once).  The
  floor is measured on IS ONLY and used to predict the OOS calendar-stability of each leg.  Inside
  the IS window the 4b "OOS" leg collapses into that window's own second half; that is stated, not
  hidden.  OOS CAGR / Sharpe / MaxDD for every book at k=0 is reported against RULES v2 (live) OOS
  and SPY OOS.

KEEP PATHS: 4a (vs RULES v2 live) and 4b (vs SPY) evaluated at every cell.

SURVIVORSHIP: U56 and B136 are CURRENT-constituent lists.  Dead names are absent, so every CAGR is
biased upward and the 4b CAGR floor (0.70 x SPY, measured on the same survivor-free benchmark) is
easier to clear than on a point-in-time panel; the DD cap is biased the same way.  Nothing below is
corrected for it.  This run's question - the SPREAD of a leg across equally arbitrary calendars -
is a within-book quantity and is far less exposed to that bias than the levels are.

PROTOCOL: 10 bps per unit turnover, next-day fills, no shorting, no leverage.  Deterministic,
standalone, no network.  Modifies nothing but its own outputs:
    .cells.csv  .legs.csv  .clause.csv  .walkforward.csv  .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-15_does-the-DD-LEG-of-4b-need-a-CONVENTION-FLOOR_cloud"
OUT = ROOT / "research" / "backtests"

COST_MAIN, LAG_MAIN = 10.0, 1
CGRID = [10.0, 25.0]
LAGS = [1, 2]
FAMILY = {"MONTHLY": ("M", list(range(21))), "WEEKLY": ("W", list(range(5)))}
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MA_WIN, WARMUP, MAX_VOL = 200, 260, 0.60
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
SHARPE_LEGS = ["H1", "H2", "OOS"]

PUB = dict(CAGR=0.1192, Sharpe=1.21, MaxDD=-0.155)
PUB_TOL = dict(CAGR=5e-5, Sharpe=5e-3, MaxDD=5e-4)
PUB_CAL_PASS, PUB_MARGIN_PP, PUB_SPREAD_PP, PP_TOL = 13, 4.74, 8.37, 0.10

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ the books
def ma_dg_weights(px, g):
    """MA-DG (idea 805): g/N over all priced names, zeroed below the 200d MA (to cash)."""
    pm = px.notna()
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    cnt = pm.sum(axis=1).replace(0, np.nan)
    return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)


def _elig(px):
    """RULES v1 eligibility, verbatim: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def top_n_weights(px, n, g, per_name):
    """Top n eligible by the v1 composite WITHOUT the vol scaler.
    per_name=True -> w = g/n each (the 2026-09-04 KEEP's construction, cash if fewer eligible)."""
    s = score(px, vol_scale=False)[0]
    rank = s.where(_elig(px)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n if per_name else g / n)


def ew_elig_weights(px, g):
    """Equal weight over ALL eligible names at gross g (2026-09-03 Finding 2)."""
    e = _elig(px).astype(float)
    cnt = e.sum(axis=1).replace(0, np.nan)
    return (g * e.div(cnt, axis=0)).fillna(0.0)


BOOKS = {
    "MADG100": lambda px: ma_dg_weights(px, 1.00),
    "MADG075": lambda px: ma_dg_weights(px, 0.75),
    "TOP20": lambda px: top_n_weights(px, 20, 0.75, True),
    "TOP40": lambda px: top_n_weights(px, 40, 1.00, True),
    "EWELIG": lambda px: ew_elig_weights(px, 0.75),
    "RULESV2": lambda px: rules_v2_weights(px, band=0.03, gross=0.75),
}


def shifted_mask(idx, freq, k):
    """Period-end rebalance calendar moved k TRADING days later (k = 0 is PROTOCOL's own)."""
    m = rebalance_mask(idx, freq).values
    if k == 0:
        return pd.Series(m, index=idx)
    pos = np.flatnonzero(m) + k
    pos = pos[pos < len(idx)]
    out = np.zeros(len(idx), dtype=bool)
    out[pos] = True
    return pd.Series(out, index=idx)


# ------------------------------------------------------------------ vectorised runner (805's)
def fast_run(prices, weights, mask, lag):
    """(gross return path before costs, turnover path, realised gross).
    r(c) = r_gross - turn * c/1e4 exactly, because cost is a same-day subtraction."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


# ------------------------------------------------------------------ 4b arithmetic
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def margins(r, spy, window):
    """The five 4b legs as MARGINS in their own units.  window in {FULL, IS, OOS}.
    Inside IS/OOS the 'OOS' leg collapses into that window's own second half (named, not hidden)."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    if window == "FULL":
        oos = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    else:
        oos = a2 - s2
    return {"H1": a1 - s1, "H2": a2 - s2, "OOS": oos,
            "DD": (m["MaxDD"] - 0.60 * ms["MaxDD"]) * 100.0,
            "CAGR": (m["CAGR"] - 0.70 * ms["CAGR"]) * 100.0,
            "_CAGR": m["CAGR"], "_Sharpe": m["Sharpe"], "_MaxDD": m["MaxDD"]}


def spearman(a, b):
    """Rank-then-Pearson; scipy is not installed in the sandbox."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    if len(a) < 3:
        return float("nan")
    return float(a.rank().corr(b.rank()))


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")
    P("# 12 books (6 forms x 2 panels) x 26 calendars (21 monthly + 5 weekly) x 2 lags x 2 costs")

    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill()}
    for nm, px in panels.items():
        P(f"PANEL {nm}: {px.shape[1]} names x {len(px)} days, {px.index[0].date()} .. {px.index[-1].date()}")
    P("SPY is a tradable constituent of both panels AND the 4b comparand (the record's construction).")

    ctx = {}
    for nm, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]
        ctx[nm] = dict(px=px, start=start, spy=spy, base=base)
        P(f"WINDOW {nm}: {start.date()} .. {px.index[-1].date()}  IS ..{IS_END}  OOS {OOS_START}..")

    # ---------------------------------------------------------------- G1 engine gate
    px = ctx["U56"]["px"]
    w = BOOKS["MADG100"](px)
    mk = shifted_mask(px.index, "M", 0)
    rg, tn, gr = fast_run(px, w, mk, LAG_MAIN)
    r_fast = (rg - tn * COST_MAIN / 1e4).loc[ctx["U56"]["start"]:]
    r_eng = backtest(px, w, cost_bps=COST_MAIN, freq="M")["returns"].loc[ctx["U56"]["start"]:]
    g1 = float(np.nanmax(np.abs(r_fast.values - r_eng.values)))
    P(f"\nG1 engine  max|fast_run - engine.backtest| = {g1:.3e}   bar 1e-9   "
      f"{'PASS' if g1 < 1e-9 else 'FAIL'}")

    # ---------------------------------------------------------------- G3 bars
    P("\nG3 comparand bars on this window:")
    for nm in panels:
        c = ctx[nm]
        ms, mb = metrics(c["spy"]), metrics(c["base"])
        s1, s2 = halves(c["spy"])
        P(f"  {nm}: SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} halves {s1:.3f}/{s2:.3f} "
          f"MaxDD {ms['MaxDD']:.2%}  ->  4b bars: DD cap {0.60*ms['MaxDD']:.2%}, "
          f"CAGR floor {0.70*ms['CAGR']:.2%}")
        P(f"       RULES v2 (live, weekly) CAGR {mb['CAGR']:.2%} Sharpe {mb['Sharpe']:.3f} "
          f"MaxDD {mb['MaxDD']:.2%}")

    # ---------------------------------------------------------------- all cells
    P("\nrunning cells ...")
    rows = []
    for pn, c in ctx.items():
        px, start, spy, base = c["px"], c["start"], c["spy"], c["base"]
        for bn, fn in BOOKS.items():
            wts = fn(px)
            for fam, (freq, offs) in FAMILY.items():
                for k in offs:
                    mk = shifted_mask(px.index, freq, k)
                    for lag in LAGS:
                        rg, tn, gr = fast_run(px, wts, mk, lag)
                        rg, tn, gr = rg.loc[start:], tn.loc[start:], gr.loc[start:]
                        for cost in CGRID:
                            r = rg - tn * cost / 1e4
                            for win, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                                ("OOS", OOS_START, None)):
                                mg = margins(r.loc[lo:hi], spy.loc[lo:hi], win)
                                rows.append(dict(
                                    panel=pn, book=bn, family=fam, k=k, lag=lag, cost=cost,
                                    window=win, CAGR=mg["_CAGR"], Sharpe=mg["_Sharpe"],
                                    MaxDD=mg["_MaxDD"],
                                    **{f"m_{L}": mg[L] for L in LEGS},
                                    **{f"p_{L}": bool(mg[L] > 0) for L in LEGS},
                                    pass4b=bool(all(mg[L] > 0 for L in LEGS)),
                                    pass4a=keep_4a(r.loc[lo:hi], base.loc[lo:hi]),
                                    gross=float(gr.mean()),
                                    turn_yr=float(tn.sum() / (len(tn) / 252))))
    cells = pd.DataFrame(rows)
    cells.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    P(f"cells: {len(cells)} rows -> {STAMP}.cells.csv   ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------------- G2 reproduction
    ref = cells[(cells.panel == "U56") & (cells.book == "MADG100") & (cells.family == "MONTHLY")
                & (cells.lag == LAG_MAIN) & (cells.cost == COST_MAIN) & (cells.window == "FULL")]
    r0 = ref[ref.k == 0].iloc[0]
    P("\nG2 reproduction of ideas 804/805's book (U56 / MADG100 / MONTHLY / k=0 / 10bps / lag 1):")
    for fld, got in (("CAGR", r0.CAGR), ("Sharpe", r0.Sharpe), ("MaxDD", r0.MaxDD)):
        d = abs(got - PUB[fld])
        P(f"  {fld:7s} published {PUB[fld]:+.4f}  here {got:+.4f}  |d| {d:.5f}  bar {PUB_TOL[fld]:.0e}"
          f"  {'PASS' if d <= PUB_TOL[fld] else 'MISS'}")
    P("  (the panel gained trading days since 805 ran on 2026-09-12, so a CAGR miss of this size is"
      " a calendar fact about data/prices.csv, not a disagreement about the book; Sharpe and MaxDD"
      " are the fields that must hold.)")
    npass = int(ref.pass4b.sum())
    ddonly = int(((~ref.p_DD) & ref.p_H1 & ref.p_H2 & ref.p_OOS & ref.p_CAGR).sum())
    P(f"  H_CAL census: {npass} of 21 offsets pass 4b (805 published {PUB_CAL_PASS}); "
      f"{ddonly} of the {21-npass} failures are the DD leg ALONE "
      f"{'PASS' if npass == PUB_CAL_PASS and ddonly == 21 - npass else 'MISS'}")
    mgn, spr = float(r0.m_DD), float(ref.m_DD.max() - ref.m_DD.min())
    P(f"  DD-cap margin at k=0 {mgn:.2f}pp (805: {PUB_MARGIN_PP}pp, bar {PP_TOL})   "
      f"{'PASS' if abs(mgn - PUB_MARGIN_PP) <= PP_TOL else 'MISS'}")
    P(f"  21-offset MaxDD spread {spr:.2f}pp (805: {PUB_SPREAD_PP}pp, bar {PP_TOL})   "
      f"{'PASS' if abs(spr - PUB_SPREAD_PP) <= PP_TOL else 'MISS'}")

    # ---------------------------------------------------------------- per-leg spread table
    leg_rows = []
    for (pn, bn, fam, lag, cost, win), g in cells.groupby(
            ["panel", "book", "family", "lag", "cost", "window"], sort=False):
        g0 = g[g.k == 0].iloc[0]
        for L in LEGS:
            v = g[f"m_{L}"].values
            m0 = float(g0[f"m_{L}"])
            sd = float(v.std(ddof=1)) if len(v) > 1 else 0.0
            sp = float(v.max() - v.min())
            leg_rows.append(dict(panel=pn, book=bn, family=fam, lag=lag, cost=cost, window=win,
                                 leg=L, margin0=m0, spread=sp, sd=sd,
                                 ratio_spread=m0 / sp if sp > 0 else np.inf,
                                 ratio_sd=m0 / sd if sd > 0 else np.inf,
                                 pass0=bool(m0 > 0),
                                 n_pass=int((v > 0).sum()), n_off=len(v),
                                 flips=int((np.sign(v) != np.sign(m0)).sum()),
                                 clause_FULLSPREAD=bool(m0 > sp),
                                 clause_SD1=bool(m0 > sd), clause_SD2=bool(m0 > 2 * sd)))
    legs = pd.DataFrame(leg_rows)
    legs.to_csv(OUT / f"{STAMP}.legs.csv", index=False)
    P(f"legs: {len(legs)} rows -> {STAMP}.legs.csv")

    main_sel = (legs.lag == LAG_MAIN) & (legs.cost == COST_MAIN) & (legs.window == "FULL")

    # ---------------------------------------------------------------- H_DDWORST / H_DDFLIP
    P("\n" + "=" * 100)
    P("SECTION 1 - IS THE DD LEG THE CONVENTION-SENSITIVE ONE?  (FULL window, 10bps, lag 1)")
    P("=" * 100)
    for fam in FAMILY:
        sub = legs[main_sel & (legs.family == fam)]
        P(f"\n{fam} family ({len(FAMILY[fam][1])} calendars), 12 books:")
        t = sub.groupby("leg").agg(median_ratio=("ratio_spread", "median"),
                                   min_ratio=("ratio_spread", "min"),
                                   n_ratio_lt1=("ratio_spread", lambda s: int((s < 1).sum())),
                                   total_flips=("flips", "sum"),
                                   books_with_flips=("flips", lambda s: int((s > 0).sum())),
                                   mean_spread=("spread", "mean")).reindex(LEGS)
        P(t.to_string(float_format=lambda x: f"{x:.3f}"))
        tot = int(sub.flips.sum())
        ddf = int(sub[sub.leg == "DD"].flips.sum())
        P(f"  DD share of all leg-level offset flips: {ddf}/{tot} = "
          f"{(ddf/tot if tot else float('nan')):.1%}")
        if fam == "MONTHLY":
            med = t["median_ratio"]
            worst = med.idxmin()
            P(f"  H_DDWORST: lowest median margin/spread ratio is {worst} ({med.min():.3f}) -> "
              f"{'CONFIRMED' if worst == 'DD' else 'REFUTED'}")
            P(f"  H_DDFLIP : DD holds a strict majority of flips -> "
              f"{'CONFIRMED' if tot and ddf > tot/2 else 'REFUTED'}")

    P("\nPer-book DD leg, MONTHLY, FULL window, 10bps, lag 1 "
      "(margin0/spread in pp; ratio<1 = the verdict is a date):")
    dd = legs[main_sel & (legs.family == "MONTHLY") & (legs.leg == "DD")].copy()
    dd = dd.sort_values("ratio_spread")
    P(dd[["panel", "book", "margin0", "spread", "sd", "ratio_spread", "pass0", "n_pass",
          "clause_FULLSPREAD", "clause_SD2"]].to_string(index=False,
                                                        float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- H_CADENCE
    P("\n" + "=" * 100)
    P("SECTION 2 - DOES CADENCE CHANGE THE FLOOR?  (mean spread per leg, MONTHLY vs WEEKLY)")
    P("=" * 100)
    piv = (legs[main_sel].pivot_table(index="leg", columns="family", values="spread",
                                      aggfunc="mean").reindex(LEGS))
    piv["W/M ratio"] = piv["WEEKLY"] / piv["MONTHLY"]
    P(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    wsm = (legs[main_sel & (legs.family == "WEEKLY")].set_index(["panel", "book", "leg"]).spread
           < legs[main_sel & (legs.family == "MONTHLY")].set_index(["panel", "book", "leg"]).spread)
    P(f"  WEEKLY spread < MONTHLY spread in {int(wsm.sum())} of {len(wsm)} book-leg pairs -> "
      f"H_CADENCE {'CONFIRMED' if wsm.mean() > 0.5 else 'REFUTED'}")

    # ---------------------------------------------------------------- H_BITE: the clause priced
    P("\n" + "=" * 100)
    P("SECTION 3 - THE CLAUSE PRICED (MONTHLY, FULL window, 10bps, lag 1)")
    P("=" * 100)
    cl_rows = []
    for (pn, bn), g in legs[main_sel & (legs.family == "MONTHLY")].groupby(["panel", "book"]):
        gi = g.set_index("leg")
        row = dict(panel=pn, book=bn,
                   pass4b_k0=bool(all(gi.loc[L, "pass0"] for L in LEGS)),
                   unanimous=bool(all(gi.loc[L, "n_pass"] == gi.loc[L, "n_off"] for L in LEGS)))
        for form, col in (("FULLSPREAD", "clause_FULLSPREAD"), ("SD1", "clause_SD1"),
                          ("SD2", "clause_SD2")):
            row[f"survives_{form}"] = bool(row["pass4b_k0"] and all(gi.loc[L, col] for L in LEGS))
            row[f"DDonly_{form}"] = bool(row["pass4b_k0"] and gi.loc["DD", col])
        row["binding_leg"] = ",".join(L for L in LEGS if not gi.loc[L, "clause_FULLSPREAD"]) or "none"
        cl_rows.append(row)
    clause = pd.DataFrame(cl_rows)
    clause.to_csv(OUT / f"{STAMP}.clause.csv", index=False)
    P(clause.to_string(index=False))
    n4b = int(clause.pass4b_k0.sum())
    for form in ("FULLSPREAD", "SD1", "SD2"):
        surv = int(clause[f"survives_{form}"].sum())
        ddo = int(clause[f"DDonly_{form}"].sum())
        P(f"  floor {form:11s}: of the {n4b} books passing 4b at k=0, {surv} survive the "
          f"all-leg clause and {ddo} survive a DD-leg-only clause")
    P(f"  H_BITE: the FULLSPREAD clause demotes {n4b - int(clause.survives_FULLSPREAD.sum())} of "
      f"{n4b} k=0 4b passes -> "
      f"{'CONFIRMED' if n4b and int(clause.survives_FULLSPREAD.sum()) < n4b else 'REFUTED'}")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("SECTION 4 - RULE 8 WALK-FORWARD: is the floor KNOWABLE IN SAMPLE?")
    P("=" * 100)
    IS_l = legs[(legs.lag == LAG_MAIN) & (legs.cost == COST_MAIN) & (legs.window == "IS")
                & (legs.family == "MONTHLY")].set_index(["panel", "book", "leg"])
    OO_l = legs[(legs.lag == LAG_MAIN) & (legs.cost == COST_MAIN) & (legs.window == "OOS")
                & (legs.family == "MONTHLY")].set_index(["panel", "book", "leg"])
    wf = pd.DataFrame({"IS_margin": IS_l.margin0, "IS_spread": IS_l.spread,
                       "IS_clause": IS_l.clause_FULLSPREAD, "IS_pass": IS_l.pass0,
                       "OOS_margin": OO_l.margin0, "OOS_spread": OO_l.spread,
                       "OOS_pass": OO_l.pass0,
                       "OOS_unanimous": OO_l.n_pass == OO_l.n_off}).reset_index()
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P("\nSpearman rho(IS spread, OOS spread) across the 12 books, per leg:")
    for L in LEGS:
        s = wf[wf.leg == L]
        rho = spearman(s.IS_spread, s.OOS_spread)
        P(f"  {L:5s} rho {rho:+.3f}   IS mean spread {s.IS_spread.mean():.3f}  "
          f"OOS mean spread {s.OOS_spread.mean():.3f}")
    rhos = [spearman(wf[wf.leg == L].IS_spread, wf[wf.leg == L].OOS_spread) for L in LEGS]
    P(f"  H_WF: rho > +0.5 on {sum(1 for x in rhos if x > 0.5)} of 5 legs -> "
      f"{'CONFIRMED' if sum(1 for x in rhos if x > 0.5) >= 3 else 'REFUTED'}")

    P("\nDoes the IS clause PREDICT OOS calendar stability?  (rows = book-leg pairs that pass "
      "the leg in sample)")
    sel = wf[wf.IS_pass]
    for lab, mask in (("IS margin > 0 only (naive)", pd.Series(True, index=sel.index)),
                      ("IS margin > IS spread (clause)", sel.IS_clause)):
        s = sel[mask]
        if len(s):
            P(f"  {lab:32s}: n={len(s):3d}  OOS leg passes {s.OOS_pass.mean():.1%}  "
              f"OOS unanimous across 21 calendars {s.OOS_unanimous.mean():.1%}")
    for L in LEGS:
        s = sel[sel.leg == L]
        sc = s[s.IS_clause]
        if len(s):
            P(f"    {L:5s} naive n={len(s):2d} OOS-unanimous {s.OOS_unanimous.mean():5.1%} | "
              f"clause n={len(sc):2d} OOS-unanimous "
              f"{(sc.OOS_unanimous.mean() if len(sc) else float('nan')):5.1%}")

    # ---------------------------------------------------------------- OOS triples (required)
    P("\nOOS (2017-01-01..) triples at k=0, 10bps, lag 1, MONTHLY, vs RULES v2 (live) and SPY:")
    for pn, c in ctx.items():
        mb = metrics(c["base"].loc[OOS_START:])
        ms = metrics(c["spy"].loc[OOS_START:])
        P(f"  --- {pn} --- RULES v2 OOS {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}"
          f"   SPY OOS {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}")
        sub = cells[(cells.panel == pn) & (cells.family == "MONTHLY") & (cells.k == 0)
                    & (cells.lag == LAG_MAIN) & (cells.cost == COST_MAIN) & (cells.window == "OOS")]
        for _, r in sub.iterrows():
            P(f"    {r.book:8s} OOS {r.CAGR:6.2%} / {r.Sharpe:5.3f} / {r.MaxDD:7.2%}   "
              f"4b {'PASS' if r.pass4b else 'fail:' + '+'.join(L for L in LEGS if not r[f'p_{L}'])}"
              f"   4a {'PASS' if r.pass4a else 'fail'}")

    # ---------------------------------------------------------------- full-sample KEEP paths
    P("\nFULL-sample k=0 (10bps, lag 1, MONTHLY) - both KEEP paths, all 12 books:")
    sub = cells[(cells.family == "MONTHLY") & (cells.k == 0) & (cells.lag == LAG_MAIN)
                & (cells.cost == COST_MAIN) & (cells.window == "FULL")]
    P(sub[["panel", "book", "CAGR", "Sharpe", "MaxDD", "m_DD", "m_CAGR", "pass4b", "pass4a",
           "gross", "turn_yr"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P(f"\n4b passes at k=0: {int(sub.pass4b.sum())}/12   4a passes: {int(sub.pass4a.sum())}/12")

    # ---------------------------------------------------------------- cost / lag robustness
    P("\nRobustness (reported, never selected) - 4b pass count over all 21 monthly calendars:")
    for cost in CGRID:
        for lag in LAGS:
            s = cells[(cells.family == "MONTHLY") & (cells.lag == lag) & (cells.cost == cost)
                      & (cells.window == "FULL")]
            P(f"  {cost:4.0f}bps lag {lag}: {int(s.pass4b.sum())} of {len(s)} book-calendar cells "
              f"pass 4b; DD leg fails in {int((~s.p_DD).sum())}, CAGR {int((~s.p_CAGR).sum())}, "
              f"H1 {int((~s.p_H1).sum())}, H2 {int((~s.p_H2).sum())}, OOS {int((~s.p_OOS).sum())}")

    P(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
