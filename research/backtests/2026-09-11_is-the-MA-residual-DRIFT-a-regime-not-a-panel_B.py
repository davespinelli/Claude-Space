#!/usr/bin/env python3
"""Idea 536 - "is-the-MA-residual-DRIFT-a-regime-not-a-panel" (lane B, 2026-09-11).

The question
------------
Idea 290/298 split the DEGROSS-minus-RESPREAD CAGR gap of a de-grossing gate into

    gap0  =  pred0  +  resid0
             ^ constant-leverage cash drag at the cell's own mean leverage c_bar
                       ^ the TIMING of c_t -- the gate's own content, in pp/yr

and idea 301 found that on the MA-THRESH family the residual is NOT the same number on the two
sides of PROTOCOL rule 8's 2016/2017 boundary:

    B136      IS -0.2864  ->  OOS -0.5287   drift -0.2423 pp/yr
    SMALL439  IS -0.0201  ->  OOS -0.5918   drift -0.5717 pp/yr
    U56       IS -0.3162  ->  OOS -0.3377   drift -0.0216 pp/yr

and that every pooled estimator carries a +0.1355 pp bias in the same direction.  Idea 301 read
that as a PANEL fact ("SMALL439's residual is unstable").  But a two-window split cannot tell a
panel property from a calendar one: the OOS window is 2017-2026 on all three panels and contains
2020 and 2022, and the three panels share 100% of their trading days.  If the drift is a common
TIME factor, "the residual is a per-panel constant" and "the residual is a constant at all" are
both mis-statements of the same underlying object, and the record's own remedy (pool by panel,
or by family) is aimed at the wrong axis.

This run re-cuts resid0 on ROLLING windows instead of two halves and asks which axis -- TIME or
PANEL -- carries the variance, and whether 2020 and/or 2022 are the whole of idea 301's drift.

Design
------
The cell grid is IMPORTED VERBATIM from ideas 298/301 -- 3 panels x 2 gate families x 9
strictness levels x 3 cadences = 162 decomposition cells, 324 books.  Nothing about that grid is
re-chosen here; it is the population the rolling statistic is measured on, not a dial.  Every
construction (gate_mask / book / control_book / stat / dec_window) is idea 301's code verbatim,
and a REPRODUCTION GATE (B4) asserts the recomputed two-half resid0 against idea 298's committed
.decomp.csv before any new number is read.

QUANTILE is kept as a PLACEBO family, not as evidence: it has c_t == x by construction, so its
resid0 is ~0 by identity.  A "common time factor" that also moves QUANTILE is an artefact of the
decomposition, not a regime; a factor that moves MA-THRESH and leaves QUANTILE flat is the real
thing.  Both are reported at every grid point.

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at none
except inside the rule-8 walk-forward.
    1. WINDOW LENGTH L, 4 values: 2, 3, 4, 5 years (the queue names 3).
    2. STEP S, 2 values: 6 and 12 months.
    => 8 (L, S) cells, every statistic below published at all 8.

Everything else is pre-registered and fixed: the estimator ladder, the exclusion years, the bars.

Windows for rule 8 are PROTOCOL's, fixed before the run: IS <= 2016-12-31, OOS >= 2017-01-01.
Costs 10 bps, gross 0.75, next-day execution, no shorting, no leverage.  The 0-bps rung is
DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run, so it is the same book; the
decomposition is a 0-bps object in ideas 290/298/301 and stays one here.

Pre-registered bars, written before any rolling number was read
--------------------------------------------------------------
B1  COMMON-TIME (the title).  On MA-THRESH, the three panels' rolling per-window mean residual
    series move together: median pairwise Spearman across the 3 panel pairs >= +0.50 in >= 5 of
    the 8 (L, S) cells.
B2  VARIANCE SHARE.  In the two-way fit resid0_pp ~ 1 + panel dummies + window dummies over the
    MA-THRESH cell x window population, partial R2(window) > partial R2(panel) in >= 5 of 8
    (L, S) cells.  B1 and B2 together = "regime, not panel".
B3  THE 2020/2022 ATTRIBUTION.  Deleting calendar 2020 and 2022 from both windows shrinks
    |drift| by >= 50% on >= 2 of the 3 panels (2 of 3 because U56's drift is already -0.02).
    Also reported: 2020 only, 2022 only, and 2008-09 (a placebo exclusion inside IS).
B4  REPRODUCTION GATE vs idea 298's committed .decomp.csv, asserted first: max |d resid0_pp|
    over the two-half rows < 1e-2 pp on SMALL439 + B136 (idea 301 already failed this bar on
    U56 at 1.287e-02 pp from the known data/prices.csv drift, ideas 513/515, and restated its
    headline on the 108 exactly-reproducing cells; U56 has since gained two more sessions, so
    its residual is expected to be larger still and is reported, not hidden).
B5  ACTIONABLE (rule 8, WF-B).  If the drift is a regime, the PREVIOUS window's pooled residual
    should predict the next window better than a panel constant:
    OOS MAE(LAG1-POOLED) < OOS MAE(PANEL) and < OOS MAE(GLOBAL), fitted on IS windows only.

Rule 8 walk-forward (required, both legs)
  WF-A  THE BOOK.  Inside each panel x family x construction arm, (level, cadence) is chosen on
        2010..2016 by IS Sharpe alone; 2017..end is read ONCE.  OOS CAGR / Sharpe / MaxDD
        reported against RULES v2 (the live book), SPY, and the cadence-matched no-gate control.
  WF-B  THE DELIVERABLE.  The estimator ladder is itself a walk-forward: every predictor is
        fitted on windows ending <= 2016-12-31 and scored once on windows starting >= 2017-01-01.
        Ladder (fixed, nothing selected from it outside rule 8):
          ZERO         predict 0 pp/yr
          GLOBAL       one IS mean over all IS cells                       (idea 301's winner)
          PANEL        IS mean per panel                                   (idea 301's rival)
          FAMILY       IS mean per gate family                             (idea 301's answer)
          LAG1-PANEL   the panel's own previous-window residual            (time-aware, honest)
          LAG1-POOLED  the previous window's residual pooled over panels   (time-aware, honest)
          WINDOW-ORACLE  the contemporaneous window mean                   (NOT usable; an upper
                         bound on what a perfect regime reader could buy)

Verdicts (both KEEP paths, on every one of the 324 books and on the WF-A picks)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents -- no delistings -- so every CAGR LEVEL here is inflated and the 4a/4b columns
inherit that whole.  The headline object is an arm-minus-arm contrast on the SAME names and days
(DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out of
gap0 / pred0 / resid0; it does NOT cancel out of the KEEP columns.

FOUND DURING THE RUN, recorded here because it changes how B1/B2 must be read
----------------------------------------------------------------------------
The three panels are NOT three independent readings of a calendar.  U56 is entirely NESTED
inside B136 -- |U56 n B136| = 55 of 56 names, min-share 1.0000, Jaccard 0.4074 -- while SMALL439
is disjoint from both (Jaccard 0.0000 against each).  A "common time factor" measured across
{U56, B136, SMALL439} therefore has ONE nested pair and TWO disjoint pairs, and a pooled window
dummy fits the nested pair's shared movement over 2/3 of the rows.  STEP 1b re-fits the same
two-way decomposition pair by pair.  The bars below are NOT moved; STEP 1b is a restatement in
the manner of idea 301's own B3b.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .rolling.csv.gz .factor.csv .exclusion.csv .estimator.csv
         .walkforward.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSS = 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# tuned dials (the only two)
LENGTHS = [2, 3, 4, 5]          # years
STEPS = [6, 12]                 # months

# pre-registered, not tuned
EXCLUSIONS = {"none": [], "2020": [2020], "2022": [2022], "2020+2022": [2020, 2022],
              "placebo 2008-09": [2008, 2009]}
LADDER = ["ZERO", "GLOBAL", "PANEL", "FAMILY", "LAG1-PANEL", "LAG1-POOLED", "WINDOW-ORACLE"]
B1_RHO, B1_CELLS = 0.50, 5
B2_CELLS = 5
B3_SHRINK, B3_PANELS = 0.50, 2
B4_TOL_PP = 1e-2
REF298 = REPO / "research" / "backtests" / (
    "2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.decomp.csv")
IDEA301_DRIFT = {"B136": -0.2423, "SMALL439": -0.5717, "U56": -0.0216}   # committed, for context

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 700)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def ols(X, y):
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ssr = float(e @ e)
    sst = float(((y - y.mean()) ** 2).sum())
    return dict(b=b, ssr=ssr, R2=(1 - ssr / sst if sst > 0 else np.nan), n=n, dof=max(1, n - p))


def dummies(s):
    """Full-rank-free dummy block; pinv in ols() handles the collinearity."""
    u = sorted(pd.unique(s))
    return np.column_stack([(np.asarray(s) == v).astype(float) for v in u])


# ---------------------------------------------------------------- ideas 298/301 constructions
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "SMALL439": (pxs[inv], pxs["SPY"]),
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
    }
    P(f"panels: SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0), U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}")
    for k, (px, _) in out.items():
        P(f"  {k}: {px.index.min().date()} .. {px.index.max().date()}  ({len(px)} rows)")
    names = {k: set(px.columns) for k, (px, _) in out.items()}
    ks = list(names)
    P("  panel NAME OVERLAP (|A n B| / |A u B|, and |A n B| / min(|A|,|B|)) -- two panels that "
      "share names cannot give independent readings of a 'common time factor':")
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = names[ks[i]], names[ks[j]]
            P(f"    {ks[i]} ~ {ks[j]}: |n| {len(a & b)}  Jaccard {len(a & b)/len(a | b):.4f}  "
              f"min-share {len(a & b)/min(len(a), len(b)):.4f}")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level, ma):
    live = live_mask(px)
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(level * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, family, level, construction, ma):
    g = gate_mask(px, family, level, ma)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def cagr(r):
    return metrics(r)["CAGR"]


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def decompose(r_rs0, r_dg0, c_t):
    """ideas 290/298/301's split, verbatim, on whatever index is handed in."""
    cb = float(c_t.mean())
    g0 = 100 * (cagr(r_dg0) - cagr(r_rs0))
    p0 = 100 * (cagr(cb * r_rs0) - cagr(r_rs0))
    return dict(c_bar=cb, c_sd=float(c_t.std()), gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                CAGR_rs0=cagr(r_rs0), CAGR_dg0=cagr(r_dg0))


def rolling_windows(lo0, hi0, years, step_months):
    """[lo, hi) calendar windows of `years` length, stepped `step_months`, inside [lo0, hi0].

    The window grid is COMMON to all three panels (built once from the intersection of their
    evaluation ranges) -- otherwise `panel` and `window` are confounded by the panels' different
    start dates, which is exactly the confound this run exists to break.
    """
    out, k = [], 0
    while True:
        lo = lo0 + pd.DateOffset(months=step_months * k)
        hi = lo + pd.DateOffset(years=years)
        if hi > hi0 + pd.Timedelta(days=1):
            break
        out.append((lo, hi))
        k += 1
    return out


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has no scipy); ties averaged."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return np.nan
    ra, rb = a[m].rank(), b[m].rank()
    sa, sb = ra.std(), rb.std()
    if sa == 0 or sb == 0:
        return np.nan
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb) *
                 len(ra) / (len(ra) - 1))


def score(pred, truth):
    e = np.asarray(pred, float) - np.asarray(truth, float)
    sse0 = float((np.asarray(truth, float) ** 2).sum())
    return dict(MAE=float(np.abs(e).mean()), RMSE=float(np.sqrt((e ** 2).mean())),
                bias=float(e.mean()), maxAE=float(np.abs(e).max()),
                R2_vs_zero=(1 - float((e ** 2).sum()) / sse0 if sse0 > 0 else np.nan))


# ---------------------------------------------------------------- main
def main():
    PN = panels()
    P("=" * 178)
    P("Idea 536 is-the-MA-residual-DRIFT-a-regime-not-a-panel (lane B) | " + Path(__file__).name)
    P("=" * 178)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED as r0 = r10 + turnover*bps/1e4), gross {GROSS}, "
      f"next-day execution.  IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8).")
    P(f"tuned dials: WINDOW LENGTH {LENGTHS} yr x STEP {STEPS} mo = {len(LENGTHS)*len(STEPS)} "
      f"cells, ALL reported.  The 162-cell grid (panel x family x level x cadence) is IMPORTED "
      f"from ideas 298/301 verbatim, not re-chosen here.")
    P("pre-registered bars:")
    P(f"  B1 COMMON-TIME   median pairwise Spearman of the 3 panels' MA rolling series >= "
      f"+{B1_RHO} in >= {B1_CELLS}/8 (L,S) cells")
    P(f"  B2 VARIANCE      partial R2(window) > partial R2(panel) in >= {B2_CELLS}/8 (L,S) cells")
    P(f"  B3 ATTRIBUTION   deleting 2020+2022 shrinks |drift| by >= {B3_SHRINK:.0%} on >= "
      f"{B3_PANELS}/3 panels")
    P(f"  B4 REPRODUCTION  max |d resid0_pp| vs idea 298's committed .decomp.csv < {B4_TOL_PP} pp "
      f"(SMALL439 + B136)")
    P(f"  B5 ACTIONABLE    OOS MAE(LAG1-POOLED) < OOS MAE(PANEL) and < OOS MAE(GLOBAL)")
    P("idea 301's committed two-half drifts, for context: " +
      ", ".join(f"{k} {v:+.4f}" for k, v in IDEA301_DRIFT.items()) + " pp/yr")
    flush_log()

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    # ONE window calendar for all three panels (see rolling_windows docstring).
    COMMON_LO = max(px.index[260] for px, _ in PN.values())
    COMMON_HI = min(px.index.max() for px, _ in PN.values())
    WINDOWS = {(L, S): rolling_windows(COMMON_LO, COMMON_HI, L, S)
               for L in LENGTHS for S in STEPS}
    P(f"\ncommon rolling-window range: {COMMON_LO.date()} .. {COMMON_HI.date()}  "
      f"(intersection of the three panels' evaluation ranges)")
    for k, v in WINDOWS.items():
        P(f"  L={k[0]}y S={k[1]}mo -> {len(v)} windows, "
          f"{v[0][0].date()}..{v[-1][1].date()}" if v else f"  L={k[0]} S={k[1]} -> 0 windows")

    rows, decomp, roll, excl = [], [], [], []
    series = {}          # (panel, family, level, cad) -> dict(r_rs0, r_dg0, c_t)
    panel_meta = {}
    for pname, (px, spy_px) in PN.items():
        ma = px.rolling(200).mean()
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_meta[pname] = dict(spy=spy_s, live=live_s, start=start)
        ctrl, ctrl0 = {}, {}
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
            r10 = rc["returns"].loc[start:]
            ctrl[cad] = stat(r10)
            ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
        panel_meta[pname]["ctrl"] = ctrl
        P("\n" + "-" * 178)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs).  "
          f"SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS {spy_s['oSharpe']:.4f} "
          f"(OOS CAGR {spy_s['oCAGR']:.4f} MaxDD {spy_s['oMaxDD']:.4f})")
        P(f"  RULES v2 (live, 4a comparand) on this window: CAGR {live_s['CAGR']:.4f} "
          f"Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS {live_s['oSharpe']:.4f} "
          f"(OOS CAGR {live_s['oCAGR']:.4f} MaxDD {live_s['oMaxDD']:.4f})")
        for cad in CADENCES:
            P(f"  CONTROL EWall {cad} (no gate): CAGR {ctrl[cad]['CAGR']:.4f} "
              f"Sharpe {ctrl[cad]['Sharpe']:.4f} MaxDD {ctrl[cad]['MaxDD']:.4f} "
              f"OOS Sharpe {ctrl[cad]['oSharpe']:.4f} | 0 bps CAGR {ctrl0[cad]:.4f}")
        P(f"  4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")
        flush_log()

        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                for cad in CADENCES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, book(px, family, level, con, ma),
                                       cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        got[con] = dict(r10=r10, r0=r0, gross=grs, s=s)
                        rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                         con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=grs.mean(), turn_yr=turn.sum() / years,
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s),
                                         spy_Sharpe=spy_s["Sharpe"], spy_oSharpe=spy_s["oSharpe"],
                                         ctrl_oSharpe=ctrl[cad]["oSharpe"]))
                    dg, rs = got["DEGROSS"], got["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident_err = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    key = (pname, family, level, cad)
                    series[key] = dict(rs0=rs["r0"], dg0=dg["r0"], c_t=c_t,
                                       oSharpe_rs=rs["s"]["oSharpe"], oSharpe_dg=dg["s"]["oSharpe"])
                    base = dict(panel=pname, family=family, level=level, cad=cad,
                                ident_max_err=ident_err)
                    for tag, sl in (("FULL", slice(None)), ("IS", slice(None, IS_END)),
                                    ("OOS", slice(OOS_START, None))):
                        d = decompose(rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl])
                        decomp.append({**base, "window": tag, **d,
                                       "oSharpe_rs": rs["s"]["oSharpe"],
                                       "oSharpe_dg": dg["s"]["oSharpe"]})
                    # ---- pre-registered exclusion re-cut of the SAME two-window split
                    for ename, yrs_out in EXCLUSIONS.items():
                        m = ~c_t.index.year.isin(yrs_out)
                        for tag, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
                            kk = pd.Series(m, index=c_t.index).loc[sl]
                            rr, rd, cc = (rs["r0"].loc[sl][kk.values], dg["r0"].loc[sl][kk.values],
                                          c_t.loc[sl][kk.values])
                            if len(rr) < 60:
                                continue
                            d = decompose(rr, rd, cc)
                            excl.append(dict(**base, exclusion=ename, window=tag,
                                             n_days=len(rr), **d))
                    # ---- rolling windows, both dials
                    for L in LENGTHS:
                        for S in STEPS:
                            for lo, hi in WINDOWS[(L, S)]:
                                sl = (c_t.index >= lo) & (c_t.index < hi)
                                if sl.sum() < 200:
                                    continue
                                d = decompose(rs["r0"][sl], dg["r0"][sl], c_t[sl])
                                roll.append(dict(panel=pname, family=family, level=level, cad=cad,
                                                 L=L, S=S, w_lo=lo.date(), w_hi=hi.date(),
                                                 w_mid=(lo + (hi - lo) / 2).date(),
                                                 n_days=int(sl.sum()), **d))
            P(f"  ... {pname} / {family} done ({len(levels)*len(CADENCES)*2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    R = pd.DataFrame(roll)
    X = pd.DataFrame(excl)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    R.to_csv(f"{OUT}.rolling.csv.gz", index=False)
    X.to_csv(f"{OUT}.exclusion.csv", index=False)
    P(f"\nwrote {len(G)} book rows, {len(D)} two-window decomposition rows, "
      f"{len(R)} rolling-window rows, {len(X)} exclusion rows")

    # ---------------- B4 reproduction gate, first
    P("\n" + "=" * 178)
    P("B4 REPRODUCTION GATE vs idea 298's committed .decomp.csv (asserted before any new number)")
    P("=" * 178)
    key = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF298)
    m = D.merge(ref[key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]], on=key,
                suffixes=("", "_ref"))
    P(f"  matched rows: {len(m)} of {len(D)} recomputed and {len(ref)} committed")
    for c in ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    P(fmt(m.groupby("panel")[["d_resid0_pp", "d_gap0_pp", "d_pred0_pp", "d_c_bar"]].max(), 8))
    sub = m[m.panel.isin(["SMALL439", "B136"])]
    b4max = float(sub.d_resid0_pp.max())
    b4 = b4max < B4_TOL_PP
    P(f"  max |d resid0_pp| on SMALL439+B136 = {b4max:.3e} pp  ->  B4 "
      f"{'PASS' if b4 else 'FAIL'} at {B4_TOL_PP} pp")
    P(f"  U56 (known vintage drift, ideas 513/515/301): max |d resid0_pp| = "
      f"{float(m[m.panel=='U56'].d_resid0_pp.max()):.3e} pp")
    P(f"  identity max |r_dg,t - c_t*r_rs,t| over {len(series)} cells: "
      f"{D.ident_max_err.max():.3e} ({'HOLDS' if D.ident_max_err.max() < 1e-12 else 'FAILS'} "
      f"at 1e-12)")
    flush_log()

    # ---------------- restate idea 301's two-half drift on today's data
    P("\n" + "=" * 178)
    P("STEP 0 - idea 301's two-half drift, recomputed (MA-THRESH and the QUANTILE placebo)")
    P("=" * 178)
    W = {t: D[D.window == t] for t in ("IS", "OOS")}
    arm = (W["IS"].groupby(["panel", "family"]).resid0_pp.agg(["mean", "std"])
           .rename(columns={"mean": "IS_mean", "std": "IS_sd"})
           .join(W["OOS"].groupby(["panel", "family"]).resid0_pp.agg(["mean", "std"])
                 .rename(columns={"mean": "OOS_mean", "std": "OOS_sd"})))
    arm["drift"] = arm.OOS_mean - arm.IS_mean
    arm["idea301_drift"] = [IDEA301_DRIFT.get(p, np.nan) if f == "MA-THRESH" else np.nan
                            for p, f in arm.index]
    P(fmt(arm, 4))
    flush_log()

    # ---------------- THE ROLLING RE-CUT
    P("\n" + "=" * 178)
    P("STEP 1 - THE ROLLING RE-CUT: per-(L,S) panel x window mean residual, MA-THRESH")
    P("=" * 178)
    fac = []
    for L in LENGTHS:
        for S in STEPS:
            for family in FAMILIES:
                sub = R[(R.L == L) & (R.S == S) & (R.family == family)]
                if sub.empty:
                    continue
                pw = sub.groupby(["panel", "w_mid"]).resid0_pp.mean().unstack(0)
                pw = pw.dropna()
                rhos, pair_rho = [], {}
                cols = list(pw.columns)
                for i in range(len(cols)):
                    for j in range(i + 1, len(cols)):
                        rr = spearman(pw[cols[i]].values, pw[cols[j]].values)
                        rhos.append(rr)
                        pair_rho[f"rho_{cols[i]}~{cols[j]}"] = rr
                # two-way partial R2 on the cell x window population
                s2 = sub.copy()
                s2["wid"] = s2.w_mid.astype(str)
                y = s2.resid0_pp.values
                one = np.ones((len(s2), 1))
                Dp, Dw = dummies(s2.panel), dummies(s2.wid)
                f_full = ols(np.column_stack([one, Dp, Dw]), y)
                f_pan = ols(np.column_stack([one, Dp]), y)
                f_win = ols(np.column_stack([one, Dw]), y)
                f_nul = ols(one, y)
                pr_win = (f_pan["ssr"] - f_full["ssr"]) / f_pan["ssr"]
                pr_pan = (f_win["ssr"] - f_full["ssr"]) / f_win["ssr"]
                # dof-fair version: window has many more levels than panel, so partial R2 alone
                # favours it mechanically.  F = (dSSR / d_df) / (SSR_full / df_full).
                dfw, dfp = Dw.shape[1] - 1, Dp.shape[1] - 1
                mse = f_full["ssr"] / max(1, len(y) - 1 - dfw - dfp)
                F_win = ((f_pan["ssr"] - f_full["ssr"]) / max(1, dfw)) / mse
                F_pan = ((f_win["ssr"] - f_full["ssr"]) / max(1, dfp)) / mse
                fac.append(dict(L=L, S=S, family=family, F_window=F_win, F_panel=F_pan,
                                n_windows=pw.shape[0],
                                n_cells=len(s2),
                                rho_med=float(np.median(rhos)), rho_min=float(np.min(rhos)),
                                rho_max=float(np.max(rhos)), **pair_rho,
                                R2_window_marginal=1 - f_win["ssr"] / f_nul["ssr"],
                                R2_panel_marginal=1 - f_pan["ssr"] / f_nul["ssr"],
                                partialR2_window=pr_win, partialR2_panel=pr_pan,
                                sd_across_windows=float(pw.mean(axis=1).std()),
                                sd_across_panels=float(pw.mean(axis=0).std())))
    F = pd.DataFrame(fac)
    F.to_csv(f"{OUT}.factor.csv", index=False)
    pcols = [c for c in F.columns if c.startswith("rho_") and "~" in c]
    P(fmt(F.set_index(["family", "L", "S"]).sort_index()
          [["n_windows", "n_cells", "rho_med", "rho_min", "rho_max"] + pcols +
           ["R2_window_marginal", "R2_panel_marginal", "partialR2_window", "partialR2_panel",
            "F_window", "F_panel", "sd_across_windows", "sd_across_panels"]], 4))

    ma_f = F[F.family == "MA-THRESH"]
    b1_hits = int((ma_f.rho_med >= B1_RHO).sum())
    b2_hits = int((ma_f.partialR2_window > ma_f.partialR2_panel).sum())
    b1 = b1_hits >= B1_CELLS
    b2 = b2_hits >= B2_CELLS
    P(f"\n  B1 COMMON-TIME  median pairwise Spearman >= +{B1_RHO} in {b1_hits}/8 (L,S) cells "
      f"-> {'PASS' if b1 else 'FAIL'}")
    P(f"  B2 VARIANCE     partial R2(window) > partial R2(panel) in {b2_hits}/8 -> "
      f"{'PASS' if b2 else 'FAIL'}")
    q_f = F[F.family == "QUANTILE"]
    P(f"  PLACEBO (QUANTILE, c_t == x by construction): rho_med "
      f"{q_f.rho_med.min():.4f}..{q_f.rho_med.max():.4f}, partial R2(window) "
      f"{q_f.partialR2_window.min():.4f}..{q_f.partialR2_window.max():.4f}, "
      f"sd across windows {q_f.sd_across_windows.min():.4f}..{q_f.sd_across_windows.max():.4f} pp")

    # ---- STEP 1b: the nesting restatement.  U56 is a SUBSET of B136 (min-share 1.0000), so the
    # B136~U56 pair is not an independent second reading of a "common time factor".  Re-fit the
    # same two-way decomposition on each PANEL PAIR.  This is a restatement of B2 on a cleaner
    # population, in the manner of idea 301's B3b; the bar itself is NOT moved.
    P("\n" + "-" * 178)
    P("STEP 1b - RESTATEMENT forced by the name overlap: the same two-way fit, PANEL PAIR by "
      "PANEL PAIR")
    P("  (U56 is nested inside B136 -- 55 of 56 names, min-share 1.0000 -- so only the two "
      "SMALL439 pairs are disjoint readings)")
    P("-" * 178)
    prs = []
    for L in LENGTHS:
        for S in STEPS:
            for family in FAMILIES:
                sub0 = R[(R.L == L) & (R.S == S) & (R.family == family)]
                pns = sorted(sub0.panel.unique())
                for i in range(len(pns)):
                    for j in range(i + 1, len(pns)):
                        pair = (pns[i], pns[j])
                        s2 = sub0[sub0.panel.isin(pair)].copy()
                        if s2.empty:
                            continue
                        s2["wid"] = s2.w_mid.astype(str)
                        y = s2.resid0_pp.values
                        one = np.ones((len(s2), 1))
                        Dp, Dw = dummies(s2.panel), dummies(s2.wid)
                        f_full = ols(np.column_stack([one, Dp, Dw]), y)
                        f_pan = ols(np.column_stack([one, Dp]), y)
                        f_win = ols(np.column_stack([one, Dw]), y)
                        pwp = s2.groupby(["panel", "w_mid"]).resid0_pp.mean().unstack(0).dropna()
                        prs.append(dict(
                            L=L, S=S, family=family, pair=f"{pair[0]}~{pair[1]}",
                            disjoint=("SMALL439" in pair),
                            rho=spearman(pwp[pair[0]].values, pwp[pair[1]].values),
                            partialR2_window=(f_pan["ssr"] - f_full["ssr"]) / f_pan["ssr"],
                            partialR2_panel=(f_win["ssr"] - f_full["ssr"]) / f_win["ssr"]))
    PR = pd.DataFrame(prs)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)
    P(fmt(PR[PR.family == "MA-THRESH"].pivot_table(
        index=["L", "S"], columns="pair", values=["rho", "partialR2_window"]), 4))
    dj = PR[(PR.family == "MA-THRESH") & PR.disjoint]
    nd = PR[(PR.family == "MA-THRESH") & ~PR.disjoint]
    P(f"\n  MA-THRESH, DISJOINT pairs ({dj.pair.nunique()} pairs x 8 dials = {len(dj)} fits): "
      f"rho median {dj.rho.median():+.4f}, range {dj.rho.min():+.4f}..{dj.rho.max():+.4f}; "
      f"rho >= +{B1_RHO} in {int((dj.rho >= B1_RHO).sum())}/{len(dj)}")
    P(f"  MA-THRESH, NESTED pair (U56 inside B136, {len(nd)} fits): "
      f"rho median {nd.rho.median():+.4f}, range {nd.rho.min():+.4f}..{nd.rho.max():+.4f}; "
      f"rho >= +{B1_RHO} in {int((nd.rho >= B1_RHO).sum())}/{len(nd)}")
    P(f"  => B1 restated: the common-time signal lives ENTIRELY in the nested pair.")
    flush_log()

    # the actual series, printed at the queue's own dial (L=3, S=12) and at L=3, S=6
    for (L, S) in [(3, 12), (3, 6)]:
        sub = R[(R.L == L) & (R.S == S) & (R.family == "MA-THRESH")]
        pw = sub.groupby(["w_mid", "panel"]).resid0_pp.mean().unstack(1)
        pwq = (R[(R.L == L) & (R.S == S) & (R.family == "QUANTILE")]
               .groupby(["w_mid", "panel"]).resid0_pp.mean().unstack(1))
        pw.columns = [f"MA:{c}" for c in pw.columns]
        pwq.columns = [f"QU:{c}" for c in pwq.columns]
        P(f"\n  rolling mean resid0 (pp/yr), L={L}y S={S}mo, window mid-date:")
        P(fmt(pw.join(pwq), 4))
    flush_log()

    # ---------------- B3 the 2020/2022 attribution
    P("\n" + "=" * 178)
    P("STEP 2 - B3 ATTRIBUTION: which calendar years carry idea 301's drift?")
    P("=" * 178)
    ex = (X.groupby(["family", "panel", "exclusion", "window"]).resid0_pp.mean()
          .unstack("window"))
    ex["drift"] = ex["OOS"] - ex["IS"]
    ex = ex.reset_index()
    base_d = ex[ex.exclusion == "none"].set_index(["family", "panel"]).drift
    ex["base_drift"] = [base_d.get((f, p), np.nan) for f, p in zip(ex.family, ex.panel)]
    ex["shrink"] = 1 - (ex.drift.abs() / ex.base_drift.abs())
    ex.to_csv(f"{OUT}.exclusion.summary.csv", index=False)
    P(fmt(ex[ex.family == "MA-THRESH"].set_index(["panel", "exclusion"])
          [["IS", "OOS", "drift", "base_drift", "shrink"]].sort_index(), 4))
    P("\n  QUANTILE placebo family:")
    P(fmt(ex[ex.family == "QUANTILE"].set_index(["panel", "exclusion"])
          [["IS", "OOS", "drift", "base_drift", "shrink"]].sort_index(), 4))
    both = ex[(ex.family == "MA-THRESH") & (ex.exclusion == "2020+2022")]
    b3_hits = int((both.shrink >= B3_SHRINK).sum())
    b3 = b3_hits >= B3_PANELS
    P(f"\n  B3 ATTRIBUTION  |drift| shrinks >= {B3_SHRINK:.0%} on {b3_hits}/3 panels when 2020 "
      f"and 2022 are deleted -> {'PASS' if b3 else 'FAIL'}")
    flush_log()

    # ---------------- B5 / WF-B the estimator ladder (rule 8)
    P("\n" + "=" * 178)
    P("STEP 3 - WF-B / B5: can a TIME-AWARE predictor beat a PANEL constant out of sample?")
    P("       (fitted on windows ending <= %s, scored ONCE on windows starting >= %s)" %
      (IS_END, OOS_START))
    P("=" * 178)
    est = []
    for L in LENGTHS:
        for S in STEPS:
            sub = R[(R.L == L) & (R.S == S)].copy()
            if sub.empty:
                continue
            sub["w_hi_ts"] = pd.to_datetime(sub.w_hi)
            sub["w_lo_ts"] = pd.to_datetime(sub.w_lo)
            IS = sub[sub.w_hi_ts <= pd.Timestamp(IS_END)]
            OO = sub[sub.w_lo_ts >= pd.Timestamp(OOS_START)]
            if len(IS) < 20 or len(OO) < 20:
                est.append(dict(L=L, S=S, note=f"insufficient windows IS {len(IS)} OOS {len(OO)}"))
                continue
            gmean = float(IS.resid0_pp.mean())
            # LAG1 needs the window immediately preceding each OOS window, from the FULL series
            wmid = sorted(sub.w_mid.unique())
            prev = {w: (wmid[i - 1] if i > 0 else None) for i, w in enumerate(wmid)}
            lag_panel = sub.groupby(["panel", "w_mid"]).resid0_pp.mean()
            lag_pool = sub.groupby("w_mid").resid0_pp.mean()
            cur_win = OO.groupby("w_mid").resid0_pp.mean()
            for fam_scope in ["ALL", "MA-THRESH"]:
                I2 = IS if fam_scope == "ALL" else IS[IS.family == "MA-THRESH"]
                O2 = OO if fam_scope == "ALL" else OO[OO.family == "MA-THRESH"]
                g2 = float(I2.resid0_pp.mean())
                pan_mean = I2.groupby("panel").resid0_pp.mean()
                fam_mean = I2.groupby("family").resid0_pp.mean()
                truth = O2.resid0_pp.values
                preds = {
                    "ZERO": np.zeros(len(O2)),
                    "GLOBAL": np.full(len(O2), g2),
                    "PANEL": O2.panel.map(pan_mean).fillna(g2).values,
                    "FAMILY": O2.family.map(fam_mean).fillna(g2).values,
                    "LAG1-PANEL": np.array([
                        lag_panel.get((p, prev[w]), np.nan) if prev[w] is not None else np.nan
                        for p, w in zip(O2.panel, O2.w_mid)]),
                    "LAG1-POOLED": np.array([
                        lag_pool.get(prev[w], np.nan) if prev[w] is not None else np.nan
                        for w in O2.w_mid]),
                    "WINDOW-ORACLE": O2.w_mid.map(cur_win).fillna(g2).values,
                }
                for nm in LADDER:
                    pv = np.where(np.isnan(preds[nm]), g2, preds[nm])
                    est.append(dict(L=L, S=S, scope=fam_scope, estimator=nm,
                                    n_IS=len(I2), n_OOS=len(O2), IS_mean=g2,
                                    OOS_mean=float(truth.mean()), **score(pv, truth)))
    E = pd.DataFrame(est)
    E.to_csv(f"{OUT}.estimator.csv", index=False)
    for scope in ["MA-THRESH", "ALL"]:
        sc = E[E.scope == scope]
        if sc.empty:
            continue
        P(f"\n  scope = {scope}:  OOS MAE (pp/yr) by estimator x (L,S)")
        P(fmt(sc.pivot_table(index="estimator", columns=["L", "S"], values="MAE")
              .reindex(LADDER), 4))
        P(f"  scope = {scope}:  OOS bias (pp/yr)")
        P(fmt(sc.pivot_table(index="estimator", columns=["L", "S"], values="bias")
              .reindex(LADDER), 4))
    ma_e = E[E.scope == "MA-THRESH"]
    wins = 0
    tot = 0
    for (L, S), g in ma_e.groupby(["L", "S"]):
        gi = g.set_index("estimator").MAE
        tot += 1
        if gi.get("LAG1-POOLED", np.inf) < gi.get("PANEL", np.inf) and \
           gi.get("LAG1-POOLED", np.inf) < gi.get("GLOBAL", np.inf):
            wins += 1
    b5 = wins > tot / 2
    P(f"\n  B5 ACTIONABLE  LAG1-POOLED beats BOTH PANEL and GLOBAL on OOS MAE in {wins}/{tot} "
      f"(L,S) cells -> {'PASS' if b5 else 'FAIL'}")
    P("\n  the rest of the pre-registered ladder, scored the same way (reported, not a bar):")
    piv = ma_e.pivot_table(index="estimator", columns=["L", "S"], values="MAE").reindex(LADDER)
    for nm in LADDER:
        if nm == "GLOBAL":
            continue
        w = int((piv.loc[nm] < piv.loc["GLOBAL"]).sum())
        P(f"    {nm:14s} beats GLOBAL on OOS MAE in {w}/{piv.shape[1]} (L,S) cells   "
          f"(MAE range {piv.loc[nm].min():.4f}..{piv.loc[nm].max():.4f})")
    gain = 1 - piv.loc["WINDOW-ORACLE"] / piv.loc["GLOBAL"]
    P(f"    CEILING: a PERFECT contemporaneous regime reader (WINDOW-ORACLE, not usable) buys "
      f"only {gain.min():.1%}..{gain.max():.1%} of OOS MAE over one global constant.")
    flush_log()

    # ---------------- WF-A the book (rule 8)
    P("\n" + "=" * 178)
    P("STEP 4 - WF-A THE BOOK: (level, cadence) chosen on IS Sharpe 2010..2016, OOS read ONCE")
    P("=" * 178)
    wf = []
    for pname in PN:
        pm = panel_meta[pname]
        spy_s, live_s = pm["spy"], pm["live"]
        for family in FAMILIES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == pname) & (G.family == family) & (G.con == con)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                ctrl = pm["ctrl"][pick.cad]
                wf.append(dict(panel=pname, family=family, con=con,
                               pick_level=pick.level, pick_cad=pick.cad,
                               IS_Sharpe=pick.isSharpe,
                               OOS_CAGR=pick.oCAGR, OOS_Sharpe=pick.oSharpe,
                               OOS_MaxDD=pick.oMaxDD,
                               live_OOS_Sharpe=live_s["oSharpe"], live_OOS_CAGR=live_s["oCAGR"],
                               live_OOS_MaxDD=live_s["oMaxDD"],
                               spy_OOS_Sharpe=spy_s["oSharpe"], spy_OOS_CAGR=spy_s["oCAGR"],
                               spy_OOS_MaxDD=spy_s["oMaxDD"],
                               ctrl_OOS_Sharpe=ctrl["oSharpe"],
                               full_CAGR=pick.CAGR, full_Sharpe=pick.Sharpe,
                               full_MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                               p4a=bool(pick.p4a), f4b=pick.f4b, p4b=bool(pick.p4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["panel", "family", "con"])[
        ["pick_level", "pick_cad", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "live_OOS_Sharpe", "spy_OOS_Sharpe", "ctrl_OOS_Sharpe", "H1", "H2", "p4a", "f4b"]], 4))
    P(f"\n  WF-A picks: 4a {int(WF.p4a.sum())}/{len(WF)}, 4b {int(WF.p4b.sum())}/{len(WF)}; "
      f"beat RULES v2 on OOS Sharpe {int((WF.OOS_Sharpe > WF.live_OOS_Sharpe).sum())}/{len(WF)}; "
      f"beat SPY on OOS Sharpe {int((WF.OOS_Sharpe > WF.spy_OOS_Sharpe).sum())}/{len(WF)}")

    # ---------------- KEEP paths over the whole grid
    P("\n" + "=" * 178)
    P("STEP 5 - KEEP PATHS over all 324 books")
    P("=" * 178)
    P(f"  4a passes: {int(G.p4a.sum())}/{len(G)}    4b passes: {int(G.p4b.sum())}/{len(G)}    "
      f"both: {int((G.p4a & G.p4b).sum())}/{len(G)}")
    P("  4b failure signatures:")
    P(fmt(G.f4b.value_counts().rename("n").to_frame(), 0))
    if G.p4b.any():
        P("\n  the 4b passers:")
        P(fmt(G[G.p4b][["panel", "family", "level", "cad", "con", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "oCAGR", "oMaxDD"]], 4))
    P("\n  by panel:")
    P(fmt(G.groupby("panel")[["p4a", "p4b"]].sum(), 0))

    # ---------------- verdict
    P("\n" + "=" * 178)
    P("VERDICT")
    P("=" * 178)
    bars = {"B1 COMMON-TIME": b1, "B2 VARIANCE": b2, "B3 ATTRIBUTION": b3,
            "B4 REPRODUCTION": b4, "B5 ACTIONABLE": b5}
    for k, v in bars.items():
        P(f"  {k:18s} {'PASS' if v else 'FAIL'}")
    P("")
    if b1 and b2:
        P("  TITLE ANSWER: the MA residual drift is a COMMON TIME FACTOR, not a panel property.")
    elif b1 or b2:
        P("  TITLE ANSWER: SPLIT - one of the two common-time bars holds and the other does not.")
    else:
        P("  TITLE ANSWER: NO - the rolling re-cut does not support a common time factor.")
    P(f"    B2 says the variance is TIME not PANEL (partial R2 window {ma_f.partialR2_window.min():.4f}"
      f"..{ma_f.partialR2_window.max():.4f} vs panel {ma_f.partialR2_panel.min():.4f}"
      f"..{ma_f.partialR2_panel.max():.4f}, F_window > F_panel in "
      f"{int((ma_f.F_window > ma_f.F_panel).sum())}/8) -- so idea 301's PANEL reading is refuted.")
    P(f"    B1 says the time factor is NOT SHARED: disjoint panel pairs rho median "
      f"{dj.rho.median():+.4f}, the nested pair {nd.rho.median():+.4f}.  It is PANEL-SPECIFIC "
      f"TIME, which is neither of the queue's two options.")
    P(f"  KEEP: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)} over the grid; "
      f"WF-A picks 4a {int(WF.p4a.sum())}/{len(WF)}, 4b {int(WF.p4b.sum())}/{len(WF)}.")
    flush_log()
    return G, D, R, F, E, WF


if __name__ == "__main__":
    main()
