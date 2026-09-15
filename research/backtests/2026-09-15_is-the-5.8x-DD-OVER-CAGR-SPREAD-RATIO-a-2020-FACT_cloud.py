#!/usr/bin/env python3
"""IDEA 892 - is the 5.80x DD-OVER-CAGR SPREAD RATIO a 2020 FACT?
Cloud lane, idea 1 of 2, 2026-09-15.

THE CLAIM UNDER TEST
--------------------
Idea 879 (committed today, `..._is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-
CENTRED_cloud`) walked the MONTHLY rebalance calendar over k = 0..20 trading-day offsets on a
population of 71 books and published, as the median over those books of the per-book spread
(max over k minus min over k) of each 4b leg:

    CAGR  1.413 pp        DD  8.201 pp        ratio 5.80x

and read that ratio as the reason the DD leg flips its verdict far more often than the CAGR leg
under a calendar perturbation that changes nothing about the rule.  The queue's question is
whether that 5.80x is a statement about the DD LEG or a statement about ONE EPISODE: MaxDD is a
single-point functional (the worst peak-to-trough of one path), so a single violent month can
own the whole leg, and 2020 is the obvious candidate on a 2009-2026 window.  If stripping 2020
collapses the ratio toward 1, the record's "DD flips more" is an episode fact and should be
quoted as such; if the ratio survives, it is a property of the functional and the record's
reading stands.

WHY THIS IS TESTABLE AT ALL, AND WHAT WOULD FALSIFY EACH READING
-----------------------------------------------------------------
Both legs are computed from the SAME daily return path, so the only thing that differs between
them is the functional applied to it.  Removing a contiguous block of trading days from that
path and recomputing both legs holds the book, the calendar walk, the costs and the window
convention fixed and moves exactly one thing.  Pre-registered readings:

    H_EPISODE   the 5.80x is carried by 2020.  Prediction: stripping the 2020 episode drives
                the ratio materially toward 1 (pre-registered bar: ratio < 3.00 at the headline
                cell), and stripping a PLACEBO year of equal length does not.
    H_FUNCTIONAL the 5.80x is a property of MaxDD as an extremum statistic.  Prediction: the
                ratio survives stripping 2020 (stays >= 3.00), because whichever episode is
                deepest after 2020 inherits the same one-point sensitivity.

These are not exhaustive - a third outcome is that BOTH legs shrink together (2020 is simply the
largest source of calendar dispersion in the whole path, for CAGR as well as DD), which would
make the ratio survive for a reason neither reading names.  That outcome is reported explicitly
as H_BOTH and is distinguished by the LEVELS, not the ratio: it requires the CAGR spread to fall
by a comparable proportion.  All three are scored on the same unchanged grid.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4: no more than two; ALL grid points reported)
---------------------------------------------------------------------------------------
  1. EPISODE DEFINITION  {NONE, CRASH, HALF1, YEAR}   how much of 2020 is removed
       NONE   control: nothing removed (this cell must reproduce 879's published numbers)
       CRASH  the SPY peak-to-trough of 2020, RESOLVED FROM THE DATA, not typed in
       HALF1  2020-01-01 .. 2020-06-30   (crash plus the whole recovery leg)
       YEAR   2020-01-01 .. 2020-12-31   (the calendar year)
  2. BOOK SET            {ALL71, CAGRCENTRED, FAR}    which of 879's books are read
       ALL71        879's whole selected population (the set its 5.80x was measured on)
       CAGRCENTRED  the sub-population within 879's margin band of the 4b CAGR floor
       FAR          879's far control (|m_CAGR| > 4pp), i.e. books nowhere near the floor

Everything else is a REPORTED CONTROL, never selected on: cost rung {10, 25} bps, cadence family
{MONTHLY 21 offsets, WEEKLY 5 offsets}, panel {U56, B136}, execution lag 1 (PROTOCOL rule 2),
and two PLACEBO episodes of the same shape in 2018 and 2022 that test whether any equally long
removal would do the same thing.

METHOD FOR STRIPPING AN EPISODE
--------------------------------
The episode's trading days are DELETED from the daily return series and the remaining days are
stitched end to end; both legs are then recomputed on the stitched path with the record's own
`engine.metrics` (CAGR annualised by len(r)/252, so the shorter path is annualised over its own
shorter length; MaxDD recomputed on the stitched equity curve).  This is the only stripping that
leaves both legs defined and comparable.  It is NOT a claim that an investor could have skipped
those days - it is a sensitivity measurement, and the LEVELS it produces are counterfactual, not
tradeable.  Every level below inherits that caveat.

SURVIVORSHIP: U56 and B136 are current-constituent panels (PROTOCOL rule 9).  Every CAGR, DD and
Sharpe LEVEL printed here is optimistic.  The reported quantity is a WITHIN-BOOK spread across
calendar offsets, which is a difference of two numbers carrying the same bias, so the spreads and
their ratio are far less exposed than the levels - but the rule-8 section at the end reads LEVELS
and is exposed in full.

PROTOCOL: 10 bps costs, next-day execution (lag 1), no shorting, no leverage.  Rule 8
walk-forward is run at the end on BOTH KEEP paths.  Rules files are not touched.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402

DATE = "2026-09-15"
SLUG = "is-the-5.8x-DD-OVER-CAGR-SPREAD-RATIO-a-2020-FACT"
STAMP = f"{DATE}_{SLUG}_cloud"
OUT = ROOT / "research" / "backtests"

# idea 879's own committed script: FORMS, fast_run, shifted_mask and the ladder constants are
# IMPORTED, never re-typed, so the population this run measures is the population 879 measured.
SRC879 = OUT / f"{DATE}_is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-CENTRED_cloud.py"

COST_MAIN, LAG_MAIN = 10.0, 1
CGRID = [10.0, 25.0]
FAMILY = {"MONTHLY": ("M", list(range(21))), "WEEKLY": ("W", list(range(5)))}
FAM_HEAD = "MONTHLY"                      # 879's own "21-calendar" family
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70

# tuned dial 1
EPISODES = {
    "NONE":  None,
    "CRASH": "RESOLVE",                              # SPY 2020 peak->trough, from the data
    "HALF1": ("2020-01-01", "2020-06-30"),
    "YEAR":  ("2020-01-01", "2020-12-31"),
}
EP_HEAD = "YEAR"
# reported controls, NOT levels of the dial: same-shape removals away from 2020
PLACEBOS = {"PLA2018_YEAR": ("2018-01-01", "2018-12-31"),
            "PLA2022_YEAR": ("2022-01-01", "2022-12-31")}
# tuned dial 2
BOOKSETS = ["ALL71", "CAGRCENTRED", "FAR"]
BS_HEAD = "ALL71"

RATIO_BAR = 3.00                                     # pre-registered H_EPISODE bar
PUB879 = dict(median_CAGR=1.413, median_DD=8.201, ratio=5.80, n_books=71)

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M879 = _load(SRC879, "idea879_cloud")
FORMS, fast_run, shifted_mask = M879.FORMS, M879.fast_run, M879.shifted_mask
GROSSES, WARMUP, BANDS, FAR_PP = M879.GROSSES, M879.WARMUP, M879.BANDS, M879.FAR_PP
margins879 = M879.margins


# ------------------------------------------------------------------ episode machinery
def resolve_crash(spy):
    """The 2020 SPY peak-to-trough, resolved from the panel: argmax of the running peak before
    the 2020 trough, to the trough itself.  Nothing about 2020 is typed in except the year."""
    s = spy.loc["2020-01-01":"2020-12-31"]
    eq = (1 + s).cumprod()
    dd = eq / eq.cummax() - 1
    trough = dd.idxmin()
    peak = eq.loc[:trough].idxmax()
    return peak, trough


def strip(r, span):
    """Delete the episode's trading days and stitch the rest end to end."""
    if span is None:
        return r
    a, b = pd.Timestamp(span[0]), pd.Timestamp(span[1])
    keep = ~((r.index >= a) & (r.index <= b))
    return r[keep]


def legs(r):
    """The two LEVEL legs of PROTOCOL 4b, in pp, plus Sharpe for the control columns."""
    m = metrics(r)
    return 100.0 * m["CAGR"], 100.0 * m["MaxDD"], m["Sharpe"]


def spread(vals):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    return float(v.max() - v.min()) if len(v) > 1 else float("nan")


def halves_sharpe(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")
    P("# idea 892, cloud lane, idea 1 of 2.  PROTOCOL: 10 bps, next-day (lag 1), no shorting.")
    P(f"# 2 tuned dials: EPISODE {list(EPISODES)} x BOOK SET {BOOKSETS} = "
      f"{len(EPISODES)*len(BOOKSETS)} cells, ALL reported.")
    P(f"# HEADLINE cell declared before any number is read: EPISODE={EP_HEAD}, SET={BS_HEAD}, "
      f"family={FAM_HEAD}, rung={COST_MAIN:.0f} bps.")
    P(f"# pre-registered bar: H_EPISODE requires the headline ratio < {RATIO_BAR:.2f} "
      f"(879 published {PUB879['ratio']:.2f}).")
    P("# controls, never selected on: rungs 10/25 bps, families MONTHLY/WEEKLY, panels "
      "U56/B136, placebo removals in 2018 and 2022.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels; every LEVEL is optimistic.")
    P("# The stripped series is a SENSITIVITY construct, not a tradeable path.")
    P("")

    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill()}
    ctx = {}
    for nm, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN,
                        freq="W")["returns"].loc[start:]
        ctx[nm] = dict(px=px, start=start, spy=spy, base=base)
        ms = metrics(spy)
        P(f"PANEL {nm}: {px.shape[1]} names x {len(px)} days, "
          f"{px.index[0].date()}..{px.index[-1].date()};  scored {start.date()}.."
          f"{px.index[-1].date()}  SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} "
          f"MaxDD {ms['MaxDD']:.2%}")

    # resolve CRASH from the U56 SPY column (the headline panel's own benchmark)
    pk, tr = resolve_crash(ctx["U56"]["spy"])
    EPD = dict(EPISODES)
    EPD["CRASH"] = (pk.strftime("%Y-%m-%d"), tr.strftime("%Y-%m-%d"))
    P(f"\nEPISODE CRASH resolved from the data: SPY 2020 peak {pk.date()} -> trough {tr.date()} "
      f"({(ctx['U56']['spy'].index >= pk).sum() - (ctx['U56']['spy'].index > tr).sum()} "
      f"trading days)")
    for k, v in EPD.items():
        if v is None:
            P(f"  EPISODE {k:<6} (control: nothing removed)")
        else:
            n = int(((ctx['U56']['spy'].index >= pd.Timestamp(v[0]))
                     & (ctx['U56']['spy'].index <= pd.Timestamp(v[1]))).sum())
            P(f"  EPISODE {k:<6} {v[0]} .. {v[1]}   {n} trading days removed")
    for k, v in PLACEBOS.items():
        n = int(((ctx['U56']['spy'].index >= pd.Timestamp(v[0]))
                 & (ctx['U56']['spy'].index <= pd.Timestamp(v[1]))).sum())
        P(f"  CONTROL {k:<12} {v[0]} .. {v[1]}   {n} trading days removed")
    ALLEP = {**EPD, **PLACEBOS}

    # ---------------------------------------------------------------- G1 engine identity
    c = ctx["U56"]
    w = FORMS["MADG"](c["px"], 1.00)
    rg, tn, _ = fast_run(c["px"], w, shifted_mask(c["px"].index, "M", 0), LAG_MAIN)
    r_fast = (rg - tn * COST_MAIN / 1e4).loc[c["start"]:]
    r_eng = backtest(c["px"], w, cost_bps=COST_MAIN, freq="M")["returns"].loc[c["start"]:]
    g1 = float(np.nanmax(np.abs(r_fast.values - r_eng.values)))
    P(f"\nG1 engine    max|fast_run - engine.backtest| = {g1:.3e}  bar 1e-9  "
      f"{'PASS' if g1 < 1e-9 else 'FAIL'}")

    # ---------------------------------------------------------------- rebuild 879's population
    rows = []
    for pn, c in ctx.items():
        px, start, spy = c["px"], c["start"], c["spy"]
        mk0 = shifted_mask(px.index, "M", 0)
        for fm, fn in FORMS.items():
            for g in GROSSES:
                rg, tn, gr = fast_run(px, fn(px, g), mk0, LAG_MAIN)
                r = (rg - tn * COST_MAIN / 1e4).loc[start:]
                mg = margins879(r, spy)
                rows.append(dict(panel=pn, form=fm, gross=g, m_CAGR=mg["CAGR"], m_DD=mg["DD"],
                                 CAGR=mg["_CAGR"], Sharpe=mg["_Sharpe"], MaxDD=mg["_MaxDD"],
                                 realised_gross=float(gr.loc[start:].mean())))
    ladder = pd.DataFrame(rows)
    maxband = max(BANDS)
    sel = ladder[(ladder.m_CAGR.abs() <= maxband) | (ladder.m_DD.abs() <= maxband)
                 | (ladder.m_CAGR.abs() > FAR_PP)].copy()
    far = sel[sel.m_CAGR.abs() > FAR_PP]
    near = sel[sel.m_CAGR.abs() <= maxband]
    nearDD = sel[(sel.m_DD.abs() <= maxband) & (sel.m_CAGR.abs() > maxband)]
    far = far[far.gross.isin(GROSSES[::3])]
    sel = pd.concat([near, nearDD, far]).drop_duplicates(subset=["panel", "form", "gross"])
    sel["bookset_near"] = sel.index.isin(near.index)
    sel["bookset_far"] = sel.index.isin(far.index)
    P(f"G2 popn      879's stage-B selection rebuilt: ladder {len(ladder)} -> selected "
      f"{len(sel)}  (879 published {PUB879['n_books']})  "
      f"{'PASS' if len(sel) == PUB879['n_books'] else 'FAIL'}")
    P(f"             composition: CAGR-centred {int(sel.bookset_near.sum())}, "
      f"DD-centred-only {len(nearDD)}, FAR control {int(sel.bookset_far.sum())}")

    # ---------------------------------------------------------------- the offset walk
    P("\n" + "=" * 100)
    P("STAGE A  WALK THE CALENDAR ON EVERY SELECTED BOOK AND RECOMPUTE BOTH LEGS UNDER EVERY "
      "EPISODE")
    P("=" * 100)
    cells = []
    for _, bk in sel.iterrows():
        c = ctx[bk.panel]
        px, start = c["px"], c["start"]
        wts = FORMS[bk.form](px, bk.gross)
        for fam, (freq, offs) in FAMILY.items():
            for k in offs:
                rg, tn, _ = fast_run(px, wts, shifted_mask(px.index, freq, k), LAG_MAIN)
                rg, tn = rg.loc[start:], tn.loc[start:]
                for cost in CGRID:
                    r = rg - tn * cost / 1e4
                    for epn, span in ALLEP.items():
                        cg, dd, sh = legs(strip(r, span))
                        cells.append(dict(panel=bk.panel, form=bk.form, gross=bk.gross,
                                          book=f"{bk.panel}-{bk.form}-g{bk.gross:.2f}",
                                          near=bool(bk.bookset_near), far=bool(bk.bookset_far),
                                          family=fam, k=k, cost=cost, episode=epn,
                                          CAGR_pp=cg, DD_pp=dd, Sharpe=sh))
    cells = pd.DataFrame(cells)
    P(f"cells: {len(cells)} = {len(sel)} books x "
      f"{sum(len(o) for _, o in FAMILY.values())} offsets x {len(CGRID)} rungs x "
      f"{len(ALLEP)} episodes   ({time.time()-t0:.0f}s)")

    # per-book spreads
    sp = (cells.groupby(["book", "panel", "form", "gross", "near", "far", "family", "cost",
                         "episode"], sort=False)
          .agg(CAGR_spread=("CAGR_pp", spread), DD_spread=("DD_pp", spread),
               Sharpe_spread=("Sharpe", spread), CAGR_med=("CAGR_pp", "median"),
               DD_med=("DD_pp", "median"))
          .reset_index())
    sp["ratio"] = sp.DD_spread / sp.CAGR_spread

    # ---------------------------------------------------------------- G3 reproduce 879
    h = sp[(sp.family == FAM_HEAD) & (sp.cost == COST_MAIN) & (sp.episode == "NONE")]
    rep = dict(median_CAGR=float(h.CAGR_spread.median()), median_DD=float(h.DD_spread.median()))
    rep["ratio"] = rep["median_DD"] / rep["median_CAGR"]
    d = [abs(rep["median_CAGR"] - PUB879["median_CAGR"]), abs(rep["median_DD"] - PUB879["median_DD"]),
         abs(rep["ratio"] - PUB879["ratio"])]
    ok3 = d[0] < 0.05 and d[1] < 0.20 and d[2] < 0.15
    P(f"G3 cross-run 879's published NONE cell reproduced from this run's own arms: "
      f"CAGR {rep['median_CAGR']:.3f} vs {PUB879['median_CAGR']:.3f} (d {d[0]:.4f}), "
      f"DD {rep['median_DD']:.3f} vs {PUB879['median_DD']:.3f} (d {d[1]:.4f}), "
      f"ratio {rep['ratio']:.3f} vs {PUB879['ratio']:.2f} (d {d[2]:.4f})  "
      f"{'PASS' if ok3 else 'FAIL'}")

    # ---------------------------------------------------------------- the 4x3 grid
    P("\n" + "=" * 100)
    P("STAGE B  THE 2-DIAL GRID  (all 12 cells; headline declared above, not chosen here)")
    P("=" * 100)

    def subset(df, bs):
        return df if bs == "ALL71" else (df[df.near] if bs == "CAGRCENTRED" else df[df.far])

    grid = []
    for fam in FAMILY:
        for cost in CGRID:
            for epn in ALLEP:
                for bs in BOOKSETS:
                    q = subset(sp[(sp.family == fam) & (sp.cost == cost)
                                  & (sp.episode == epn)], bs)
                    if not len(q):
                        continue
                    mc, md = float(q.CAGR_spread.median()), float(q.DD_spread.median())
                    grid.append(dict(family=fam, cost=cost, episode=epn, bookset=bs,
                                     n=len(q), med_CAGR_spread=mc, med_DD_spread=md,
                                     ratio_of_medians=md / mc if mc else np.nan,
                                     med_of_ratios=float(q.ratio.median()),
                                     med_CAGR_level=float(q.CAGR_med.median()),
                                     med_DD_level=float(q.DD_med.median())))
    grid = pd.DataFrame(grid)

    hd = grid[(grid.family == FAM_HEAD) & (grid.cost == COST_MAIN)]
    P(f"\nHEADLINE family {FAM_HEAD}, rung {COST_MAIN:.0f} bps - the 12 tuned cells "
      f"(+{2*len(BOOKSETS)} placebo controls):")
    P(hd[["episode", "bookset", "n", "med_CAGR_spread", "med_DD_spread", "ratio_of_medians",
          "med_of_ratios", "med_CAGR_level", "med_DD_level"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P(f"\nEVERY grid point, both families and both rungs ({len(grid)} rows):")
    P(grid.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- read the hypotheses
    P("\n" + "=" * 100)
    P("STAGE C  SCORE THE PRE-REGISTERED READINGS")
    P("=" * 100)

    def cell(epn, bs=BS_HEAD, fam=FAM_HEAD, cost=COST_MAIN):
        q = grid[(grid.family == fam) & (grid.cost == cost) & (grid.episode == epn)
                 & (grid.bookset == bs)]
        return q.iloc[0]

    c0, ch = cell("NONE"), cell(EP_HEAD)
    P(f"headline cell EPISODE={EP_HEAD}, SET={BS_HEAD}: "
      f"CAGR spread {c0.med_CAGR_spread:.3f} -> {ch.med_CAGR_spread:.3f} pp "
      f"({ch.med_CAGR_spread/c0.med_CAGR_spread:.3f}x), "
      f"DD spread {c0.med_DD_spread:.3f} -> {ch.med_DD_spread:.3f} pp "
      f"({ch.med_DD_spread/c0.med_DD_spread:.3f}x), "
      f"ratio {c0.ratio_of_medians:.3f} -> {ch.ratio_of_medians:.3f}")
    h_ep = bool(ch.ratio_of_medians < RATIO_BAR)
    P(f"H_EPISODE  (headline ratio < {RATIO_BAR:.2f} after stripping 2020): "
      f"{'PASS' if h_ep else 'FAIL'}   observed {ch.ratio_of_medians:.3f}")
    P(f"H_FUNCTIONAL (ratio survives, >= {RATIO_BAR:.2f}): {'PASS' if not h_ep else 'FAIL'}")
    fall_c = 1.0 - ch.med_CAGR_spread / c0.med_CAGR_spread
    fall_d = 1.0 - ch.med_DD_spread / c0.med_DD_spread
    h_both = bool(fall_c > 0.20 and fall_d > 0.20)
    P(f"H_BOTH     (BOTH spreads fall > 20%, i.e. 2020 is the dispersion source for both legs): "
      f"{'PASS' if h_both else 'FAIL'}   CAGR falls {fall_c:+.1%}, DD falls {fall_d:+.1%}")

    P("\nunanimity of the stripping direction across ALL 12 tuned cells "
      "(does every (episode, set) pair move the ratio the same way?):")
    for bs in BOOKSETS:
        base_r = cell("NONE", bs).ratio_of_medians
        line = f"  SET {bs:<12} NONE {base_r:6.3f}"
        for epn in [e for e in EPD if e != "NONE"]:
            line += f" | {epn} {cell(epn, bs).ratio_of_medians:6.3f}"
        for epn in PLACEBOS:
            line += f" | {epn} {cell(epn, bs).ratio_of_medians:6.3f}"
        P(line)
    P("\nsame, at the 25 bps rung and on the WEEKLY family (controls):")
    for fam in FAMILY:
        for cost in CGRID:
            if fam == FAM_HEAD and cost == COST_MAIN:
                continue
            line = f"  {fam:<8} {cost:5.1f}bps  "
            for epn in ALLEP:
                line += f"{epn} {cell(epn, BS_HEAD, fam, cost).ratio_of_medians:6.3f}  "
            P(line)

    # placebo comparison: is the 2020 removal special?
    P("\nPLACEBO test - a same-shape calendar-year removal away from 2020 (headline set/family/"
      "rung):")
    for epn in ["YEAR"] + list(PLACEBOS):
        q = cell(epn)
        P(f"  {epn:<12} CAGR spread {q.med_CAGR_spread:6.3f}  DD spread {q.med_DD_spread:7.3f}  "
          f"ratio {q.ratio_of_medians:6.3f}  (vs NONE ratio {c0.ratio_of_medians:.3f})")

    # where does each book's MaxDD actually sit?
    P("\nWHERE THE DD LEG LIVES - share of books whose max drawdown TROUGH falls inside 2020, "
      "at k=0, headline family/rung:")
    for pn, c in ctx.items():
        inside = tot = 0
        for _, bk in sel[sel.panel == pn].iterrows():
            px, start = c["px"], c["start"]
            rg, tn, _ = fast_run(px, FORMS[bk.form](px, bk.gross),
                                 shifted_mask(px.index, "M", 0), LAG_MAIN)
            r = (rg - tn * COST_MAIN / 1e4).loc[start:]
            eq = (1 + r).cumprod()
            t_ = (eq / eq.cummax() - 1).idxmin()
            tot += 1
            inside += int(t_.year == 2020)
        P(f"  {pn:>5}: {inside}/{tot} books trough inside 2020")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("STAGE D  RULE 8 WALK-FORWARD")
    P("=" * 100)
    P(f"IS = ..{IS_END}   OOS = {OOS_START}..   NOTE, and it decides the clause-level answer:")
    P("  the 2020 episode lies ENTIRELY inside the OOS window, so an IS-only measurement of this")
    P("  run's dial cannot see the thing the dial removes.  The IS ratio is, by construction, an")
    P("  already-episode-free ratio.  That is reported, not worked around.")

    # D1 clause-level: per-book spreads measured inside IS only and inside OOS only
    wf = []
    for _, bk in sel.iterrows():
        c = ctx[bk.panel]
        px, start = c["px"], c["start"]
        wts = FORMS[bk.form](px, bk.gross)
        rec = {"book": f"{bk.panel}-{bk.form}-g{bk.gross:.2f}", "panel": bk.panel}
        for win, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
            cg, dd = [], []
            for k in FAMILY[FAM_HEAD][1]:
                rg, tn, _ = fast_run(px, wts, shifted_mask(px.index, FAMILY[FAM_HEAD][0], k),
                                     LAG_MAIN)
                r = (rg - tn * COST_MAIN / 1e4).loc[start:].loc[sl]
                a, b, _ = legs(r)
                cg.append(a)
                dd.append(b)
            rec[f"{win}_CAGR_spread"] = spread(cg)
            rec[f"{win}_DD_spread"] = spread(dd)
            rec[f"{win}_ratio"] = spread(dd) / spread(cg) if spread(cg) else np.nan
        wf.append(rec)
    wf = pd.DataFrame(wf)
    P(f"\nIS-only median: CAGR spread {wf.IS_CAGR_spread.median():.3f} pp, "
      f"DD spread {wf.IS_DD_spread.median():.3f} pp, ratio "
      f"{wf.IS_DD_spread.median()/wf.IS_CAGR_spread.median():.3f}")
    P(f"OOS-only median: CAGR spread {wf.OOS_CAGR_spread.median():.3f} pp, "
      f"DD spread {wf.OOS_DD_spread.median():.3f} pp, ratio "
      f"{wf.OOS_DD_spread.median()/wf.OOS_CAGR_spread.median():.3f}")
    rho = float(pd.Series(wf.IS_ratio).rank().corr(pd.Series(wf.OOS_ratio).rank()))
    P(f"rho(IS per-book ratio, OOS per-book ratio) = {rho:+.3f}  "
      f"(n = {int(wf.IS_ratio.notna().sum())})")
    agree = int(((wf.IS_ratio > RATIO_BAR) == (wf.OOS_ratio > RATIO_BAR)).sum())
    P(f"IS and OOS agree on the '> {RATIO_BAR:.2f}' verdict for {agree}/{len(wf)} books "
      f"({agree/len(wf):.1%})")

    # D2 book-level: IS-only pick, OOS read once, both KEEP paths
    P("\nD2  IS-ONLY SELECTOR (highest IS Sharpe per panel at k=0, headline rung), OOS READ ONCE:")
    lb_rows, memo_rows = [], []
    for pn, c in ctx.items():
        px, start, spy, base = c["px"], c["start"], c["spy"], c["base"]
        best, bestsh = None, -np.inf
        for _, bk in sel[sel.panel == pn].iterrows():
            rg, tn, _ = fast_run(px, FORMS[bk.form](px, bk.gross),
                                 shifted_mask(px.index, "M", 0), LAG_MAIN)
            r = (rg - tn * COST_MAIN / 1e4).loc[start:].loc[:IS_END]
            s = metrics(r)["Sharpe"]
            if s > bestsh:
                best, bestsh = bk, s
        rg, tn, _ = fast_run(px, FORMS[best.form](px, best.gross),
                             shifted_mask(px.index, "M", 0), LAG_MAIN)
        full = (rg - tn * COST_MAIN / 1e4).loc[start:]
        oos, bo, so = full.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:]
        mo, mb, msp = metrics(oos), metrics(bo), metrics(so)
        h1, h2 = halves_sharpe(oos)
        b1, b2 = halves_sharpe(bo)
        s1, s2 = halves_sharpe(so)
        k4a = bool(h1 > b1 and h2 > b2 and mo["MaxDD"] >= mb["MaxDD"])
        k4b = bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > msp["Sharpe"]
                   and mo["MaxDD"] >= DDCAP_FRAC * msp["MaxDD"]
                   and mo["CAGR"] >= CAGRFLOOR_FRAC * msp["CAGR"])
        name = f"{pn}-{best.form}-g{best.gross:.2f}"
        P(f"  {pn} pick {name}  (IS Sharpe {bestsh:.3f})")
        P(f"    OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.3f} / {mo['MaxDD']:7.2%}   "
          f"halves {h1:.3f} / {h2:.3f}")
        P(f"    SPY {msp['CAGR']:7.2%} / {msp['Sharpe']:.3f} / {msp['MaxDD']:7.2%}   "
          f"halves {s1:.3f} / {s2:.3f}   "
          f"(4b bars: CAGR >= {CAGRFLOOR_FRAC*msp['CAGR']:.2%}, "
          f"DD >= {DDCAP_FRAC*msp['MaxDD']:.2%})")
        P(f"    RULES v2 (live) {mb['CAGR']:7.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:7.2%}   "
          f"halves {b1:.3f} / {b2:.3f}")
        P(f"    KEEP 4a {'PASS' if k4a else 'FAIL'}   KEEP 4b {'PASS' if k4b else 'FAIL'}")
        # the same pick, read with 2020 stripped - the run's own dial applied to its own pick
        st = strip(oos, EPD[EP_HEAD])
        mst = metrics(st)
        P(f"    same pick, {EP_HEAD} stripped: {mst['CAGR']:7.2%} / {mst['Sharpe']:.3f} / "
          f"{mst['MaxDD']:7.2%}  (MaxDD moves {100*(mst['MaxDD']-mo['MaxDD']):+.2f} pp)")
        memo_rows.append(dict(panel=pn, pick=name, IS_Sharpe=bestsh, OOS_CAGR=mo["CAGR"],
                              OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"], OOS_H1=h1,
                              OOS_H2=h2, keep_4a=k4a, keep_4b=k4b,
                              SPY_CAGR=msp["CAGR"], SPY_Sharpe=msp["Sharpe"],
                              SPY_MaxDD=msp["MaxDD"], V2_CAGR=mb["CAGR"],
                              V2_Sharpe=mb["Sharpe"], V2_MaxDD=mb["MaxDD"],
                              stripped_MaxDD=mst["MaxDD"], stripped_CAGR=mst["CAGR"],
                              stripped_Sharpe=mst["Sharpe"]))
        lb_rows.append((pn, name, mo, h1, h2, mb, b1, b2, msp, k4a, k4b))

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 100)
    answer = ("YES - CARRIED BY 2020" if h_ep else "NO - THE RATIO SURVIVES 2020")
    P(f"ANSWER: {answer}")
    P(f"  headline ratio {c0.ratio_of_medians:.3f} (NONE) -> {ch.ratio_of_medians:.3f} "
      f"({EP_HEAD} stripped); bar {RATIO_BAR:.2f}")
    P("VERDICT for capital: KILL - this run prices a MEASUREMENT CONVENTION, not a book. "
      "Nothing is promoted; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched "
      "(PROTOCOL rule 6: a clause change is a Sunday-review act).")
    P(f"total runtime {time.time()-t0:.0f}s")

    # ---------------------------------------------------------------- artifacts
    cells.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    sp.to_csv(OUT / f"{STAMP}.spreads.csv", index=False)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    pd.DataFrame(memo_rows).to_csv(OUT / f"{STAMP}.picks.csv", index=False)
    ladder.to_csv(OUT / f"{STAMP}.ladder.csv", index=False)
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
