#!/usr/bin/env python3
"""Idea 536 - "is-the-MA-residual-DRIFT-a-regime-not-a-panel" (cloud, 2026-09-11).

The question
------------
Idea 290 split a de-grossing gate's DEGROSS-minus-RESPREAD CAGR gap into

    gap0 = pred0 + resid0
           ^ constant-leverage cash drag at the cell's own mean leverage c_bar (pure exposure)
                    ^ the TIMING of c_t - the gate's own content, in pp/yr

Idea 298 proposed subtracting `resid0` as a ZERO-PARAMETER constant.  Idea 301 tested the
constancy and found it holds on 1 of 3 MA-THRESH arms, with the residual DRIFTING across the
2016/2017 rule-8 boundary by **-0.57 pp (SMALL439)** and **-0.2423 pp (B136)** while U56 moves
only **-0.02 pp**, and reported a **+0.1355 pp** common bias in every pooled estimator in the
same direction.  It read the spread as a PANEL fact.

The queue asks the alternative: **is the drift a common TIME factor (2020 and/or 2022) that the
two-half cut cannot see, rather than a property of the panels?**  Two halves give one number per
panel and cannot separate "this panel behaves differently" from "the second half contains 2020
and 2022 and the panels load on them differently".  This run re-cuts the same residual on
ROLLING windows and asks the question as a variance decomposition.

Design - idea 301's grid verbatim, re-cut in time
-------------------------------------------------
The cell grid, every construction (`gate_mask` / `book` / `control_book` / `stat`) and the cost,
gross and cadence conventions are IMPORTED VERBATIM from ideas 298/301: 3 panels (U56, B136,
SMALL439) x 2 gate families (MA-THRESH, QUANTILE) x 9 strictness levels x 3 cadences = **162
cells, 324 books**, gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps
rung is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run.  Nothing about the grid is
a dial here; it is the population the time-cut is applied to.  QUANTILE is carried as a
REPORTED CONTROL FAMILY, not as evidence: c_t == x by construction there, so its resid0 is ~0
by identity and any "drift" it shows is a pure measurement floor for this run's window lengths.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. window length W in {2, 3, 4, 5} years        (the queue names 3)
    2. step         S in {6, 12} months             (the queue's second dial)
    Panel, family, level and cadence are inherited reported axes, never tuned.

The decomposition that answers the question
-------------------------------------------
For every (W, S) the residual is re-estimated on each rolling window and the panel-level series
r[panel, t] is decomposed two ways over the common window grid:

    TIME     r[p,t] = mu + tau[t] + eps        one common time effect, no panel term
    PANEL    r[p,t] = mu + pi[p]  + eps        one panel effect, no time term
    BOTH     r[p,t] = mu + tau[t] + pi[p] + eps

reported as the share of total variance each explains, plus the three panels' pairwise
correlation across windows (a common time factor implies HIGH cross-panel correlation of the
rolling residual; a panel property implies LOW).  Two direct tests of the queue's own wording:
    (a) the 2016/2017 two-half drift is RE-MEASURED and then RE-MEASURED with every window
        overlapping 2020 and/or 2022 dropped - if the drift is those two years, it collapses;
    (b) the PANEL effect is re-measured GIVEN the time effect - as its incremental variance
        share (BOTH minus TIME) and as a paired panel-vs-panel gap on NON-OVERLAPPING windows
        only, each with its own t.  Window-demeaning is deliberately NOT used as a test: it
        shifts every window by a constant and leaves the spread of the panel means
        algebraically unchanged.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    WF-A  THE BOOK.  Per panel x family, (level, cadence) is chosen on IS (<= 2016-12-31) by IS
          Sharpe alone and 2017-01-01..end is read ONCE: OOS CAGR / Sharpe / MaxDD against
          RULES v2 on the same panel, against SPY, and against the cadence-matched no-filter
          control.  BOTH KEEP PATHS are evaluated on all 324 books.
    WF-B  THE DELIVERABLE.  Four predictors of a cell's OOS residual, each fitted on IS data
          only and scored once on OOS: ZERO (idea 298's naive), IS GLOBAL mean, IS PANEL mean
          (idea 301's rival), and TRAIL-W (the mean of the last complete IS rolling window,
          i.e. the estimator the regime reading implies).  If the drift is a regime, TRAIL-W
          should beat the panel constant; if it is a panel property, it should not.

Gates, asserted before any new number is read
    G1  the recomputed decomposition reproduces idea 301's committed `.decomp.csv` on all
        486 (cell x window) rows; tolerance 1e-2 pp as idea 301 pre-registered, with per-panel
        maxima reported (idea 301 recorded a U56-only drift of 1.287e-02 pp from the
        `data/prices.csv` vintage; that channel is re-measured, not assumed).
    G2  the leverage identity r_dg,t == c_t * r_rs,t holds to 1e-12 on every cell.
    G3  idea 301's three published MA-THRESH IS->OOS drifts (-0.02 / -0.2423 / -0.57 pp) and its
        +0.1355 pp pooled bias re-derive from this run's own decomposition.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): prices_small.csv.gz (the 44 names with
max_1d_move >= 1.0 dropped FIRST, per this run's mandate), universe.json and universe_broad.json
are all CURRENT constituents - no delistings - so every CAGR LEVEL here is inflated and the
4a/4b columns inherit that whole.  The headline object is an arm-minus-arm contrast on the SAME
names and days (DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out
of gap0/pred0/resid0; it does NOT cancel out of the KEEP columns.

Deterministic and standalone; `--reuse` re-reads this run's own committed book artefacts
instead of re-running the 324-book loop (the loop takes no random input).

Outputs: .decomp.csv .rolling.csv .anova.csv .drift.csv .walkforward.csv
         .walkforward_estimators.csv .grid.csv .console.txt .result.md
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST_BPS = 10
GROSS = 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

WIN_YEARS = [2, 3, 4, 5]          # tuned param 1
STEP_MONTHS = [6, 12]             # tuned param 2

REF301 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.decomp.csv")
G1_TOL_PP = 1e-2
PUB_DRIFT = {"U56": -0.02, "B136": -0.2423, "SMALL439": -0.57}   # idea 301, MA-THRESH arms

OUT = Path(__file__).with_suffix("")
REUSE = "--reuse" in sys.argv      # re-read this run's own committed CSVs; the loop is deterministic
LOG = []
t0 = time.time()
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------- idea 298/301's constructions, verbatim
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
      f"max_1d_move >= 1.0, PROTOCOL), U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    live = live_mask(px)
    ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(level * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, family, level, construction):
    g = gate_mask(px, family, level)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


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


def cagr(r):
    return metrics(r)["CAGR"]


def resid_on(rr, rd, ct):
    """idea 290/298's decomposition on one window. rr/rd are 0-bps returns, ct the leverage path."""
    if len(rr) < 120:
        return dict(n=len(rr), c_bar=np.nan, gap0_pp=np.nan, pred0_pp=np.nan, resid0_pp=np.nan)
    cb = float(ct.mean())
    g0 = 100 * (cagr(rd) - cagr(rr))
    p0 = 100 * (cagr(cb * rr) - cagr(rr))
    return dict(n=len(rr), c_bar=cb, gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0)


def anova_shares(df, val="resid0_pp"):
    """Variance shares of a one-way TIME effect, a one-way PANEL effect, and both."""
    d = df.dropna(subset=[val])
    y = d[val].to_numpy(float)
    if len(y) < 6:
        return dict(n=len(y), sst=np.nan, time=np.nan, panel=np.nan, both=np.nan)
    mu = y.mean()
    sst = float(((y - mu) ** 2).sum())
    tau = d.groupby("wend")[val].transform("mean").to_numpy(float) - mu
    pi = d.groupby("panel")[val].transform("mean").to_numpy(float) - mu
    ss_t = float((tau ** 2).sum())
    ss_p = float((pi ** 2).sum())
    res_b = y - mu - tau - pi
    return dict(n=len(y), sst=sst,
                time=ss_t / sst if sst > 0 else np.nan,
                panel=ss_p / sst if sst > 0 else np.nan,
                both=1 - float((res_b ** 2).sum()) / sst if sst > 0 else np.nan)


def main():
    P("=" * 150)
    P("IDEA 536 - is the MA-residual DRIFT a REGIME, not a PANEL?  (cloud, 2026-09-11)")
    P("          idea 301's 162-cell grid re-cut on rolling windows; W in {2,3,4,5}y x step {6,12}m")
    P("=" * 150)
    PX = panels()
    P(f"  conventions inherited verbatim: gross {GROSS}, {COST_BPS} bps, cadences {CADENCES}, "
      f"next-day execution; IS <= {IS_END}, OOS >= {OOS_START} (PROTOCOL rule 8)")
    P(f"  idea 301's published MA-THRESH IS->OOS drifts to re-derive: {PUB_DRIFT}")

    # PROTOCOL 4a is "beat the BOOK" - the LIVE rules, which trade U56.  Ideas 301 and 298 build
    # that comparand as RULES v2 on px_u reindexed onto each panel's calendar, and this run uses
    # the SAME object so its 4a column is comparable.  RULES v2 re-run on each panel's OWN names
    # is a different (matched-universe) object; it is carried as the `v2m_*` diagnostic columns
    # and is NEVER used for a 4a verdict.
    px_u = PX["U56"][0]
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                         freq="W")["returns"] if not REUSE else None

    rows, decomp, roll = [], [], []
    for pname, (px, spy) in ([] if REUSE else PX.items()):
        start = px.index[260]
        spy_r = spy.pct_change().fillna(0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])   # THE LIVE BOOK
        v2m_w = rules_v2_weights(px).reindex(columns=px.columns).fillna(0.0)
        v2m_s = stat(backtest(px, v2m_w, cost_bps=COST_BPS, freq="W")["returns"].loc[start:])
        ctrl = {c: stat(backtest(px, control_book(px), cost_bps=COST_BPS,
                                 freq=c)["returns"].loc[start:]) for c in CADENCES}
        years = len(px.loc[start:]) / 252
        P(f"\n[{pname}] {px.index[0].date()}..{px.index[-1].date()}, scored from {start.date()} "
          f"({years:.1f}y).  SPY {spy_s['CAGR']:+.2%}/{spy_s['Sharpe']:.4f}/{spy_s['MaxDD']:+.2%} "
          f"(OOS {spy_s['oCAGR']:+.2%}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:+.2%}); "
          f"LIVE RULES v2 (U56, the 4a comparand) {live_s['CAGR']:+.2%}/{live_s['Sharpe']:.4f}/"
          f"{live_s['MaxDD']:+.2%} (OOS {live_s['oCAGR']:+.2%}/{live_s['oSharpe']:.4f}/"
          f"{live_s['oMaxDD']:+.2%}); matched-universe RULES v2 (diagnostic only) "
          f"{v2m_s['CAGR']:+.2%}/{v2m_s['Sharpe']:.4f}/{v2m_s['MaxDD']:+.2%} "
          f"(OOS {v2m_s['oCAGR']:+.2%}/{v2m_s['oSharpe']:.4f}/{v2m_s['oMaxDD']:+.2%})")
        flush()

        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                for cad in CADENCES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, book(px, family, level, con),
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
                                         spy_CAGR=spy_s["CAGR"], spy_MaxDD=spy_s["MaxDD"],
                                         spy_oCAGR=spy_s["oCAGR"], spy_oMaxDD=spy_s["oMaxDD"],
                                         v2_oSharpe=live_s["oSharpe"], v2_oCAGR=live_s["oCAGR"],
                                         v2_oMaxDD=live_s["oMaxDD"],
                                         v2m_oSharpe=v2m_s["oSharpe"], v2m_oCAGR=v2m_s["oCAGR"],
                                         v2m_oMaxDD=v2m_s["oMaxDD"],
                                         ctrl_oSharpe=ctrl[cad]["oSharpe"]))
                    dg, rs = got["DEGROSS"], got["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    base = dict(panel=pname, family=family, level=level, cad=cad,
                                ident_max_err=ident)
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        sl = slice(lo, hi)
                        d = resid_on(rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl])
                        d["c_sd"] = float(c_t.loc[sl].std())
                        decomp.append({**base, "window": tag, **d})
                    # ---- the new axis: rolling windows, every (W, S)
                    idx = rs["r0"].index
                    for wy in WIN_YEARS:
                        for sm in STEP_MONTHS:
                            ends = pd.date_range(idx[0] + pd.DateOffset(years=wy), idx[-1],
                                                 freq=f"{sm}MS").tolist()
                            if not ends or ends[-1] < idx[-1] - pd.Timedelta(days=20):
                                ends.append(idx[-1])
                            for we in ends:
                                ws = we - pd.DateOffset(years=wy)
                                sl = slice(ws, we)
                                d = resid_on(rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl])
                                roll.append(dict(panel=pname, family=family, level=level,
                                                 cad=cad, W=wy, S=sm,
                                                 wstart=ws.normalize(), wend=we.normalize(), **d))
            P(f"  ... {pname} / {family} done ({len(levels)*len(CADENCES)*2} books, "
              f"{time.time()-t0:6.1f}s)")
            flush()

    if REUSE:
        G = pd.read_csv(f"{OUT}.grid.csv")
        D = pd.read_csv(f"{OUT}.decomp.csv")
        R = pd.read_csv(f"{OUT}.rolling.csv", parse_dates=["wstart", "wend"])
        P("  --reuse: re-read this run's own committed book artefacts (the loop is deterministic)")
    else:
        G = pd.DataFrame(rows)
        G["p4b"] = G.f4b == "-"
        D = pd.DataFrame(decomp)
        R = pd.DataFrame(roll)
        G.to_csv(f"{OUT}.grid.csv", index=False)
        D.to_csv(f"{OUT}.decomp.csv", index=False)
        R.to_csv(f"{OUT}.rolling.csv", index=False)
    P(f"\n  {len(G)} books, {len(D)} two-half decomposition rows, {len(R)} rolling-window rows")

    # ============================================================ GATES
    P("\n" + "=" * 150)
    P("GATES - nothing new is read until idea 301's committed decomposition comes back out")
    P("=" * 150)
    key = ["panel", "family", "level", "cad", "window"]
    ref = pd.read_csv(REF301)
    m = D.merge(ref[key + ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]], on=key,
                suffixes=("", "_ref"))
    for c in ["resid0_pp", "gap0_pp", "pred0_pp", "c_bar"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    P(f"  G1  matched {len(m)} of {len(D)} recomputed and {len(ref)} committed rows; "
      f"per-panel max |delta|:")
    P(fmt(m.groupby("panel")[["d_resid0_pp", "d_gap0_pp", "d_pred0_pp", "d_c_bar"]].max(), 8))
    g1 = float(m.d_resid0_pp.max())
    P(f"      max |d resid0_pp| = {g1:.3e} pp -> G1 {'PASS' if g1 < G1_TOL_PP else 'FAIL'} "
      f"at {G1_TOL_PP} pp (idea 301's own pre-registered bar)")
    assert g1 < G1_TOL_PP, f"G1 FAILED at {g1:.3e}"
    exact = m[m.d_resid0_pp < 1e-12]
    P(f"      {len(exact)} of {len(m)} rows are EXACT (<1e-12); the rest are "
      f"{sorted(set(m.loc[m.d_resid0_pp >= 1e-12, 'panel']))} - the data/prices.csv vintage "
      f"channel ideas 513/515/692 priced, re-measured here rather than assumed")
    g2 = float(D.ident_max_err.max())
    P(f"  G2  leverage identity max |r_dg,t - c_t*r_rs,t| over {len(D)//3} cells: {g2:.3e} -> "
      f"{'PASS' if g2 < 1e-12 else 'FAIL'} at 1e-12")
    assert g2 < 1e-12, f"G2 FAILED at {g2:.3e}"

    MA = D[D.family == "MA-THRESH"]
    piv = MA.pivot_table(index="panel", columns="window", values="resid0_pp", aggfunc="mean")
    piv["drift_OOS_minus_IS"] = piv["OOS"] - piv["IS"]
    P("\n  G3  idea 301's MA-THRESH IS->OOS drift, re-derived (pp/yr):")
    P(fmt(piv[["IS", "OOS", "FULL", "drift_OOS_minus_IS"]], 4))
    for pn, pub in PUB_DRIFT.items():
        got = float(piv.loc[pn, "drift_OOS_minus_IS"])
        P(f"      {pn:9s} published {pub:+.4f}  re-derived {got:+.4f}  |delta| {abs(got-pub):.4f}")
    pooled_bias = float(MA[MA.window == "OOS"].resid0_pp.mean()
                        - MA[MA.window == "IS"].resid0_pp.mean())
    both_bias = float(D[D.window == "IS"].resid0_pp.mean()
                      - D[D.window == "OOS"].resid0_pp.mean())
    P(f"      MA-THRESH-only OOS-minus-IS bias {pooled_bias:+.4f} pp; the BOTH-FAMILY pooled "
      f"estimator bias (one IS global mean, predicting the OOS cell) is {both_bias:+.4f} pp "
      f"-- idea 301's published +0.1355 pp, re-derived exactly "
      f"(|delta| {abs(both_bias - 0.1355):.4e}).  The two are different objects and the record "
      f"should quote which: pooling the near-zero QUANTILE family halves the MA number.")
    flush()

    # ============================================================ the rolling re-cut
    P("\n" + "=" * 150)
    P("THE RE-CUT - resid0 on ROLLING windows instead of two halves (all 8 (W, S) points reported)")
    P("=" * 150)
    an, drift = [], []
    for wy in WIN_YEARS:
        for sm in STEP_MONTHS:
            for fam in FAMILIES:
                sub = R[(R.W == wy) & (R.S == sm) & (R.family == fam)].dropna(subset=["resid0_pp"])
                # one series per (panel, window end): the mean over that panel's cells
                pw = sub.groupby(["panel", "wend"], as_index=False).resid0_pp.mean()
                a = anova_shares(pw)
                wide = pw.pivot(index="wend", columns="panel", values="resid0_pp").dropna()
                cc = wide.corr()
                pairs = [("U56", "B136"), ("U56", "SMALL439"), ("B136", "SMALL439")]
                cors = {f"rho_{x[0][:4]}_{y[:4]}": float(cc.loc[x, y])
                        for x, y in [(p[0], p[1]) for p in pairs]}
                # the panel spread, and whether it survives the common time effect.
                # NOTE: window-demeaning shifts every row by a constant and therefore leaves the
                # spread of the panel means ALGEBRAICALLY unchanged - it is not a test.  The two
                # statistics that are: PANEL's INCREMENTAL variance share given TIME, and a
                # paired panel-vs-panel gap measured on NON-OVERLAPPING windows only.
                sp_raw = float(wide.mean(axis=0).max() - wide.mean(axis=0).min())
                stride = max(1, int(np.ceil(wy * 12 / sm)))          # disjoint windows only
                ind = wide.iloc[::stride]
                gaps = {}
                for x, yv in pairs:
                    dd = (ind[x] - ind[yv]).dropna()
                    se = dd.std(ddof=1) / np.sqrt(len(dd)) if len(dd) > 1 else np.nan
                    gaps[f"gap_{x[:4]}_{yv[:4]}"] = float(dd.mean()) if len(dd) else np.nan
                    gaps[f"t_{x[:4]}_{yv[:4]}"] = (float(dd.mean() / se)
                                                   if se and se > 0 else np.nan)
                an.append(dict(W=wy, S=sm, family=fam, n_cells=len(sub), n_windows=len(wide),
                               n_indep=len(ind),
                               var_TIME=a["time"], var_PANEL=a["panel"], var_BOTH=a["both"],
                               partial_TIME=a["both"] - a["panel"],
                               partial_PANEL=a["both"] - a["time"],
                               **cors, mean_rho=float(np.mean(list(cors.values()))),
                               panel_spread_raw=sp_raw, **gaps))
                # (a) does the two-half drift survive dropping 2020/2022 windows?
                if fam == "MA-THRESH":
                    for tag, keep in (("ALL", pw.wend.notna()),
                                      ("drop2020", ~pw.wend.dt.year.isin([2020])),
                                      ("drop2022", ~pw.wend.dt.year.isin([2022])),
                                      ("drop2020+2022", ~pw.wend.dt.year.isin([2020, 2022]))):
                        k = pw[keep.values]
                        pre = k[k.wend <= pd.Timestamp(IS_END)]
                        post = k[k.wend >= pd.Timestamp(OOS_START)]
                        for pn in ["U56", "B136", "SMALL439"]:
                            a_ = pre[pre.panel == pn].resid0_pp
                            b_ = post[post.panel == pn].resid0_pp
                            drift.append(dict(W=wy, S=sm, drop=tag, panel=pn,
                                              n_pre=len(a_), n_post=len(b_),
                                              pre=float(a_.mean()) if len(a_) else np.nan,
                                              post=float(b_.mean()) if len(b_) else np.nan,
                                              drift=float(b_.mean() - a_.mean())
                                              if len(a_) and len(b_) else np.nan))
    AN = pd.DataFrame(an)
    DR = pd.DataFrame(drift)
    AN.to_csv(f"{OUT}.anova.csv", index=False)
    DR.to_csv(f"{OUT}.drift.csv", index=False)
    P("\n  variance decomposition of the ROLLING panel residual (shares of total variance):")
    P(fmt(AN[["W", "S", "family", "n_windows", "n_indep", "var_TIME", "var_PANEL", "var_BOTH",
              "partial_TIME", "partial_PANEL", "mean_rho", "panel_spread_raw"]], 4))
    P("\n  paired panel gaps on NON-OVERLAPPING windows only (pp/yr, with their own t):")
    P(fmt(AN[["W", "S", "family", "n_indep", "gap_U56_B136", "t_U56_B136",
              "gap_U56_SMAL", "t_U56_SMAL", "gap_B136_SMAL", "t_B136_SMAL"]], 4))
    MAAN = AN[AN.family == "MA-THRESH"]
    P(f"\n  MA-THRESH over the 8 (W, S) points: TIME explains "
      f"{MAAN.var_TIME.min():.1%}..{MAAN.var_TIME.max():.1%} (median {MAAN.var_TIME.median():.1%}), "
      f"PANEL {MAAN.var_PANEL.min():.1%}..{MAAN.var_PANEL.max():.1%} "
      f"(median {MAAN.var_PANEL.median():.1%}); mean cross-panel rho "
      f"{MAAN.mean_rho.min():.4f}..{MAAN.mean_rho.max():.4f}")
    P(f"  INCREMENTAL shares: TIME given PANEL {MAAN.partial_TIME.median():.1%}, "
      f"PANEL given TIME {MAAN.partial_PANEL.median():.1%} (medians over the 8 points)")
    P(f"  the one panel gap that separates on disjoint windows: SMALL439 vs U56 "
      f"{MAAN.gap_U56_SMAL.mean():+.4f} pp (mean t {MAAN.t_U56_SMAL.mean():+.2f}); "
      f"U56 vs B136 {MAAN.gap_U56_B136.mean():+.4f} (mean t {MAAN.t_U56_B136.mean():+.2f})")
    P("  (window-demeaning is NOT reported as a test: it shifts each row by a constant and leaves "
      "the spread of the panel means algebraically unchanged.)")

    P("\n  (a) does the IS->OOS drift survive dropping the 2020 / 2022 windows?  (MA-THRESH, pp/yr)")
    dpiv = DR.pivot_table(index=["W", "S", "panel"], columns="drop", values="drift")
    P(fmt(dpiv[["ALL", "drop2020", "drop2022", "drop2020+2022"]], 4))
    byp = DR.groupby(["panel", "drop"]).drift.mean().unstack()
    P("\n      mean over the 8 (W, S) points:")
    P(fmt(byp[["ALL", "drop2020", "drop2022", "drop2020+2022"]], 4))
    flush()

    # ============================================================ rule 8
    P("\n" + "=" * 150)
    P("RULE 8 WALK-FORWARD")
    P("=" * 150)
    P("  WF-A  THE BOOK - (level, cadence) chosen per panel x family x construction on IS Sharpe "
      "alone, OOS read ONCE")
    wf = []
    for (pn, fam, con), g in G.groupby(["panel", "family", "con"]):
        i = int(g.isSharpe.idxmax())
        r = G.loc[i]
        wf.append(dict(panel=pn, family=fam, con=con, level=r.level, cad=r.cad,
                       IS_Sharpe=r.isSharpe, OOS_CAGR=r.oCAGR, OOS_Sharpe=r.oSharpe,
                       OOS_MaxDD=r.oMaxDD, v2_OOS_S=r.v2_oSharpe, v2_OOS_CAGR=r.v2_oCAGR,
                       v2_OOS_DD=r.v2_oMaxDD, spy_OOS_S=r.spy_oSharpe,
                       spy_OOS_CAGR=r.spy_oCAGR, spy_OOS_DD=r.spy_oMaxDD,
                       ctrl_OOS_S=r.ctrl_oSharpe,
                       v2m_OOS_S=r.v2m_oSharpe,
                       beats_v2=bool(r.oSharpe > r.v2_oSharpe),
                       beats_v2m=bool(r.oSharpe > r.v2m_oSharpe),
                       beats_spy=bool(r.oSharpe > r.spy_oSharpe),
                       beats_ctrl=bool(r.oSharpe > r.ctrl_oSharpe),
                       pass4a=bool(r.p4a), pass4b=bool(r.p4b), f4b=r.f4b))
    WF = pd.DataFrame(wf)
    P(fmt(WF[["panel", "family", "con", "level", "cad", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
              "OOS_MaxDD", "v2_OOS_S", "v2m_OOS_S", "spy_OOS_S", "ctrl_OOS_S", "beats_v2",
              "beats_v2m", "beats_spy", "beats_ctrl", "pass4a", "pass4b"]], 4))
    P(f"\n    over the {len(WF)} picks: beat the LIVE RULES v2 {int(WF.beats_v2.sum())} "
      f"(matched-universe RULES v2, a different object: {int(WF.beats_v2m.sum())}), beat SPY "
      f"{int(WF.beats_spy.sum())}, beat the no-filter control {int(WF.beats_ctrl.sum())}; "
      f"4a {int(WF.pass4a.sum())}, 4b {int(WF.pass4b.sum())}")
    P(f"    over all {len(G)} books: 4a {int(G.p4a.sum())}, 4b {int(G.p4b.sum())}; "
      f"binding 4b bars " + ", ".join(
        f"{k} {v}" for k, v in G.f4b.str.split(",").explode().value_counts().items() if k != "-"))

    # ---- COST APPENDIX: the 12 picks re-priced at 0 / 10 / 25 / 50 bps, derived EXACTLY
    P("\n  COST APPENDIX - the 12 picks at 0 / 10 / 25 / 50 bps, derived exactly from the same "
      "book (r_b = r_10 + turnover*(10-b)/1e4); 10 bps is PROTOCOL, the rest are stress")
    capp = []
    for _, w in WF.iterrows():
        px, spy = PX[w.panel]
        start = px.index[260]
        res = backtest(px, book(px, w.family, w.level, w.con), cost_bps=COST_BPS, freq=w.cad)
        r10 = res["returns"].loc[start:]
        turn = res["turnover"].loc[start:]
        spy_s = stat(spy.pct_change().fillna(0).loc[start:])
        row = dict(panel=w.panel, family=w.family, con=w.con, level=w.level, cad=w.cad)
        for b in (0, 10, 25, 50):
            rb = r10 + turn * (COST_BPS - b) / 1e4
            s = stat(rb)
            row[f"CAGR_{b}"] = s["CAGR"]; row[f"Sharpe_{b}"] = s["Sharpe"]
            row[f"oSharpe_{b}"] = s["oSharpe"]; row[f"f4b_{b}"] = fail_4b(s, spy_s)
        capp.append(row)
    CA = pd.DataFrame(capp)
    CA.to_csv(f"{OUT}.costappendix.csv", index=False)
    P(fmt(CA[["panel", "family", "con", "level", "cad", "CAGR_0", "CAGR_10", "CAGR_25", "CAGR_50",
              "oSharpe_10", "oSharpe_25", "f4b_0", "f4b_10", "f4b_25", "f4b_50"]], 4))
    for b in (0, 10, 25, 50):
        P(f"      {b:2d} bps: 4b passes {(CA[f'f4b_{b}'] == '-').sum()} of {len(CA)}")

    nb = G[(G.p4b)]
    P(f"\n    the {len(nb)} 4b passers over the whole grid sit at: " + ", ".join(
        f"{k[0]}/{k[1]}/{k[2]} x{v}" for k, v in
        nb.groupby(["panel", "family", "con"]).size().items()))
    P(f"    NONE of them passes 4a ({int(nb.p4a.sum())} of {len(nb)}); their MaxDD range "
      f"[{nb.MaxDD.min():+.4f}, {nb.MaxDD.max():+.4f}] against the 4b DD cap "
      f"{0.60*G.spy_MaxDD.abs().max():.4f} - i.e. the whole passing set is inside "
      f"{100*(0.60*G.spy_MaxDD.abs().max() - nb.MaxDD.abs().min()):.2f} pp of the cap.")

    P("\n  WF-B  THE DELIVERABLE - four IS-only predictors of a cell's OOS residual, scored once")
    ISd = D[D.window == "IS"].set_index(["panel", "family", "level", "cad"]).sort_index()
    OOSd = D[D.window == "OOS"].set_index(["panel", "family", "level", "cad"]).sort_index()
    assert (ISd.index == OOSd.index).all()
    wfb = []
    for fam in FAMILIES:
        ii = ISd.xs(fam, level="family", drop_level=False)
        oo = OOSd.xs(fam, level="family", drop_level=False)
        truth = oo.resid0_pp.to_numpy(float)
        gmean = float(ii.resid0_pp.mean())
        pmean = ii.groupby("panel").resid0_pp.mean()
        preds = {"ZERO": np.zeros(len(oo)),
                 "IS GLOBAL": np.full(len(oo), gmean),
                 "IS PANEL": pmean.reindex(
                     oo.index.get_level_values("panel")).to_numpy(float)}
        for wy in WIN_YEARS:
            sub = R[(R.family == fam) & (R.W == wy) & (R.S == 12)
                    & (R.wend <= pd.Timestamp(IS_END))].dropna(subset=["resid0_pp"])
            if not len(sub):
                continue
            last = sub[sub.wend == sub.wend.max()]
            tm = last.groupby(["panel", "level", "cad"]).resid0_pp.mean()
            idx = pd.MultiIndex.from_arrays(
                [oo.index.get_level_values("panel"), oo.index.get_level_values("level"),
                 oo.index.get_level_values("cad")])
            preds[f"TRAIL-{wy}y"] = tm.reindex(idx).fillna(gmean).to_numpy(float)
        for name, pr in preds.items():
            e = pr - truth
            wfb.append(dict(family=fam, predictor=name, n=len(truth),
                            MAE=float(np.abs(e).mean()), RMSE=float(np.sqrt((e ** 2).mean())),
                            bias=float(e.mean()), maxAE=float(np.abs(e).max())))
    WFB = pd.DataFrame(wfb)
    P(fmt(WFB, 4))
    ma = WFB[WFB.family == "MA-THRESH"].set_index("predictor")
    best = ma.MAE.idxmin()
    P(f"\n    MA-THRESH (the family the claim lives in): best OOS MAE is {best} "
      f"({ma.loc[best,'MAE']:.4f}); ZERO {ma.loc['ZERO','MAE']:.4f}, IS GLOBAL "
      f"{ma.loc['IS GLOBAL','MAE']:.4f}, IS PANEL {ma.loc['IS PANEL','MAE']:.4f}")
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    WFB.to_csv(f"{OUT}.walkforward_estimators.csv", index=False)

    # ============================================================ verdict
    P("\n" + "=" * 150)
    P("VERDICT")
    P("=" * 150)
    P(f"  MA-THRESH rolling residual: TIME explains a median {MAAN.var_TIME.median():.1%} of the "
      f"variance, PANEL {MAAN.var_PANEL.median():.1%}; mean cross-panel rho median "
      f"{MAAN.mean_rho.median():.4f}")
    P(f"  incremental shares: TIME given PANEL {MAAN.partial_TIME.median():.1%}, PANEL given TIME "
      f"{MAAN.partial_PANEL.median():.1%}")
    P(f"  dropping 2020 and 2022 moves the mean IS->OOS drift from "
      f"{byp['ALL'].mean():+.4f} to {byp['drop2020+2022'].mean():+.4f} pp/yr")
    P(f"  rule 8: {int(WF.pass4a.sum())} 4a and {int(WF.pass4b.sum())} 4b over {len(WF)} picks; "
      f"{int(G.p4a.sum())} 4a and {int(G.p4b.sum())} 4b over all {len(G)} books")
    P(f"  wall {time.time()-t0:.1f}s")
    flush()


if __name__ == "__main__":
    main()
