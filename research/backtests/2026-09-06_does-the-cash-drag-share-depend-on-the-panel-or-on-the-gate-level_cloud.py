#!/usr/bin/env python3
"""Idea 298 - "does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level" (cloud, 2026-09-06).

The question
------------
Idea 290 proved that a DE-GROSSING gate book is ALGEBRAICALLY the RESPREAD book at time-varying
leverage (max |r_dg,t - c_t*r_rs,t| = 2.08e-17), and decomposed the DEGROSS-minus-RESPREAD CAGR
gap into

    gap0 = pred0  +  resid0
           ^ constant-leverage cash drag at the cell's own mean leverage c_bar (pure exposure)
                     ^ the TIMING of c_t (the gate's own content)

It measured exposure_share = pred0/gap0 = 0.914 (0.798..1.000) over 36 band x cadence x gate
cells, all at c_bar 0.42..0.52, on SMALL439 only.  The QUEUE's objection is mechanical:

    the share is a function of how far c_bar sits from 1, so a gate that de-grosses LIGHTLY
    should look almost purely like drag - and idea 290's 0.914 would then be a readout of its
    own c_bar rather than a fact about gates.

Sweep the gate's strictness so c_bar runs 0.2..0.95 and report the exposure-share curve, so any
future de-gross claim can be discounted from its own c_bar.  And - the title's second half -
say whether the share is a PANEL property or a GATE-LEVEL property.

Two rival hypotheses, both pre-registered with bars, before any number was read
------------------------------------------------------------------------------
Write c_t = 1 - eps*u_t with E[u] = 1, so (1 - c_bar) = eps.  To second order in the return,

    gap0    ~  -eps*mu  -  (1/2)*sigma^2*(c_bar^2 - 1)  -  252*Cov(c_t, r_rs,t)  + O(eps^2)
    pred0   ~  -eps*mu  -  (1/2)*sigma^2*(c_bar^2 - 1)                           + O(eps^2)
    resid0  ~                                           -  252*Cov(c_t, r_rs,t)  + O(eps^2)

H_QUEUE (the queue's mechanical story).  The share is driven by distance from 1: as c_bar -> 1
    the gate barely de-grosses, gap0 -> 0 through the drag term, and the share -> 1.
    BAR: exposure_share rises monotonically toward 1 in c_bar, and every arm's mean share at
    c_bar >= 0.85 is within 0.03 of 1.000, in at least 5 of the 6 panel x family arms.

H_RATIO (the expansion above).  BOTH the drag and the timing residual are FIRST order in eps,
    because Cov(c_t, r_t) = -eps*Cov(u_t, r_t).  The eps cancels in the ratio, so the share is
    approximately INVARIANT to c_bar and measures the gate's timing-to-drag ratio - a property
    of how the gate's exposure covaries with the panel's returns, not of its level.
    BAR: |t| of the OLS slope of share on c_bar < 2.0 within an arm in a majority of the 6
    arms, AND the within-arm sd of share <= 0.10 in a majority of arms.

The two are mutually exclusive on the c_bar >= 0.85 rungs, which is exactly where idea 290 had
no data.  Whichever fails, the answer to "panel or gate level" is then read off a two-way fit:

    B3  share ~ 1 + c_bar + panel dummies + family dummies (on all cells), plus each term's
        partial R2.  "PANEL" wins if the panel dummies' partial R2 exceeds c_bar's; "LEVEL"
        wins if c_bar's does.  Reported either way; no bar, it is the answer itself.

    B4  REPRODUCTION GATE, asserted before any new number is read.  On SMALL439, gate family
        MA-THRESH at theta = 0.00 (which is idea 290's MA gate at band 0.00 up to exact ties),
        the run must reproduce idea 290's published cells:
             cad W : c_bar 0.5040  gap0 -3.6342 pp  pred0 -3.5470 pp  share 0.9760
             cad M : c_bar 0.5087  gap0 -4.5151 pp  pred0 -4.2803 pp  share 0.9480
             cad Q : c_bar 0.5106  gap0 -5.2626 pp  pred0 -4.3481 pp  share 0.8262
        BAR: |dc_bar| < 0.005 and |dshare| < 0.02 on all three.

Design
------
GATE FAMILIES (a REPORTED dimension, not a tuned parameter - the point is the contrast):
  QUANTILE   gate IN the top ceil(x * n_t) live names by (px / ma200 - 1), so c_t == x BY
             CONSTRUCTION and c_bar lands exactly on the requested 0.20..0.95 grid.  This is
             the only construction that can pin c_bar where the queue asks for it.
  MA-THRESH  gate IN where px > ma200 * (1 + theta): the record's OWN gate form, shifted.
             theta = 0.00 reproduces idea 290's band-0.00 MA gate; c_bar is an OUTCOME here,
             which is why the QUANTILE family is carried beside it.

PANELS (a REPORTED dimension, 3 values - the title's "panel or gate level" needs more than one):
  SMALL439   idea 290's panel: sub-$2B names, the 44 with max_1d_move >= 1.0 dropped.
  U56        research/universe.json (ETF + mega-cap).
  B136       research/universe_broad.json (~100 large caps + 36 ETFs).

CONSTRUCTIONS: RESPREAD (w = g/k_t * G) and DEGROSS (w = g/n_t * G), idea 290's definitions
verbatim; the whole object under test is the contrast between them.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. strictness level   (9 values: x for QUANTILE, theta for MA-THRESH)
    2. cadence            (3 values: W, M, Q)
Reported at every value; selected at none except inside the rule-8 walk-forward.
Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps rung is DERIVED
exactly (r0 = r10 + turnover * cost_bps / 1e4), not re-run, so it is the same book.

Grid: 3 panels x 2 families x 9 levels x 3 cadences x 2 constructions = 324 books.
Decomposition cells: 3 x 2 x 9 x 3 = 162, every one reported.

Rule 8 walk-forward (required; two of them, directions fixed before any OOS number was read)
  WF-A (the book).  Inside each panel x family x construction arm, (level, cadence) is chosen
        on 2010-01-01..2016-12-31 by IS Sharpe; 2017-01-01..end is read ONCE.  OOS CAGR /
        Sharpe / MaxDD reported against the LIVE book (RULES v2 on universe.json), SPY, and the
        cadence-matched no-filter control.
  WF-B (the deliverable).  The exposure-share curve is the product this idea ships, so it gets
        its own walk-forward: fit share ~ 1 + c_bar on the IS window's cells ONLY, then predict
        each cell's OOS share and report mean |error| against two naive predictors read once -
        (i) idea 290's constant 0.914 and (ii) the IS mean share.  A curve that cannot beat a
        constant out of sample is not a discount rule.

Verdicts (both KEEP paths, on every one of the 324 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents - no delistings - so the LEVEL of every CAGR here is inflated and the 4a/4b
columns inherit that whole.  The headline is an arm-minus-arm contrast on the SAME names and
days (DEGROSS and RESPREAD share one gate mask g), so the bias very largely cancels out of
gap0 / pred0 / resid0 and out of the share; it does NOT cancel out of the KEEP columns.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .walkforward.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, band_state, rules_v2_weights
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
TINY_GAP_PP = 0.10          # cells whose |gap0| is below this are flagged: share is 0/0-unstable

# pre-registered bars
BAR_QUEUE_TOL, BAR_QUEUE_CBAR, BAR_QUEUE_ARMS = 0.03, 0.85, 5
BAR_RATIO_T, BAR_RATIO_SD = 2.0, 0.10
REPRO_290 = {"W": dict(c_bar=0.5040, gap0_pp=-3.6342, pred0_pp=-3.5470, share=0.9760),
             "M": dict(c_bar=0.5087, gap0_pp=-4.5151, pred0_pp=-4.2803, share=0.9480),
             "Q": dict(c_bar=0.5106, gap0_pp=-5.2626, pred0_pp=-4.3481, share=0.8262)}
REPRO_CBAR_TOL, REPRO_SHARE_TOL = 0.005, 0.02
IDEA290_SHARE = 0.914

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def ols(X, y, names):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ssr = float(e @ e)
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ssr / sst if sst > 0 else np.nan
    dof = max(1, n - p)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ssr / dof)), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    return dict(names=names, b=b, t=t, R2=r2, n=n, ssr=ssr, sst=sst)


def partial_r2(X, y, cols, names):
    """Drop the given column block, refit, report the R2 lost."""
    full = ols(X, y, names)
    keep = [i for i in range(X.shape[1]) if i not in cols]
    red = ols(X[:, keep], y, [names[i] for i in keep])
    return full["R2"] - red["R2"]


# ---------------------------------------------------------------- panels
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
    for nm, (p, _) in out.items():
        P(f"  {nm}: {p.index[0].date()} .. {p.index[-1].date()}  ({len(p)} days)")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    """QUANTILE: top ceil(level * n_t) live names by px/ma200-1, so c_t == level exactly.
    MA-THRESH: px > ma200 * (1 + level)."""
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


# ---------------------------------------------------------------- main
def main():
    PN = panels()
    P("=" * 170)
    P("Idea 298 does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level (cloud) | "
      + Path(__file__).name)
    P("=" * 170)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), "
      f"gross {GROSS}, next-day execution.")
    P(f"tuned dials: strictness level (9) x cadence {CADENCES}.  Reported dimensions: "
      f"panel (3) x family {FAMILIES} x construction {CONSTRUCTIONS}.")
    P("pre-registered bars:")
    P(f"  H_QUEUE : share -> 1 in c_bar; mean share at c_bar >= {BAR_QUEUE_CBAR} within "
      f"{BAR_QUEUE_TOL} of 1.000 in >= {BAR_QUEUE_ARMS}/6 arms")
    P(f"  H_RATIO : |t| of slope(share ~ c_bar) < {BAR_RATIO_T} in a majority of arms AND "
      f"within-arm sd(share) <= {BAR_RATIO_SD} in a majority")
    P(f"  B4 repro: SMALL439 / MA-THRESH theta=0.00 must match idea 290 to "
      f"|dc_bar| < {REPRO_CBAR_TOL}, |dshare| < {REPRO_SHARE_TOL}")

    # live 4a comparand, computed once
    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp = [], []
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_r)
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        ctrl, ctrl0 = {}, {}
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
            r10 = rc["returns"].loc[start:]
            ctrl[cad] = stat(r10)
            ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
        P("\n" + "-" * 170)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs).  "
          f"SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS {spy_s['oSharpe']:.4f}")
        P(f"  RULES v2 (live, 4a comparand) on this window: CAGR {live_s['CAGR']:.4f} "
          f"Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS {live_s['oSharpe']:.4f}")
        for cad in CADENCES:
            P(f"  CONTROL EWall {cad} (no gate): CAGR {ctrl[cad]['CAGR']:.4f} "
              f"Sharpe {ctrl[cad]['Sharpe']:.4f} MaxDD {ctrl[cad]['MaxDD']:.4f} "
              f"| 0 bps CAGR {ctrl0[cad]:.4f}")
        P(f"  4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70 * spy_s['CAGR']:.2%}")
        flush_log()

        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                for cad in CADENCES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, book(px, family, level, con), cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        got[con] = dict(r10=r10, r0=r0, gross=grs, s=s)
                        rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                         con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=grs.mean(), gross_min=grs.min(),
                                         turn_yr=turn.sum() / years,
                                         dCAGR_ctrl=s["CAGR"] - ctrl[cad]["CAGR"],
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s),
                                         spy_CAGR=spy_s["CAGR"], spy_Sharpe=spy_s["Sharpe"],
                                         spy_MaxDD=spy_s["MaxDD"], spy_oSharpe=spy_s["oSharpe"]))
                    dg, rs = got["DEGROSS"], got["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident_err = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    def dec_window(lo, hi, tag):
                        sl = slice(lo, hi)
                        rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                        cb = float(c_t.loc[sl].mean())
                        g0 = 100 * (cagr(rd) - cagr(rr))
                        p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        return dict(window=tag, c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                    gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                    share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                                    CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd),
                                    cov_c_r=float(np.cov(c_t.loc[sl], rr)[0, 1] * 252))
                    base = dict(panel=pname, family=family, level=level, cad=cad,
                                ident_max_err=ident_err,
                                gap_pp=100 * (dg["s"]["CAGR"] - rs["s"]["CAGR"]))
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        decomp.append({**base, **dec_window(lo, hi, tag)})
            P(f"  ... {pname} / {family} done ({len(levels) * len(CADENCES) * 2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    F = D[D.window == "FULL"].copy()
    F["tiny"] = F.gap0_pp.abs() < TINY_GAP_PP

    # ---------------- identity check (idea 290's P1, re-asserted here)
    P("\n" + "=" * 170)
    P("IDENTITY CHECK (idea 290's P1 re-asserted on this grid): max |r_dg,t - c_t * r_rs,t| at 0 bps")
    P("=" * 170)
    P(fmt(F.groupby(["panel", "family"]).ident_max_err.agg(["max", "mean"]), 3))
    P(f"worst over all {len(F)} cells: {F.ident_max_err.max():.3e}  "
      f"({'HOLDS' if F.ident_max_err.max() < 1e-12 else 'FAILS'} at 1e-12)")

    # ---------------- B4 reproduction gate
    P("\n" + "=" * 170)
    P("B4 REPRODUCTION GATE vs idea 290 (SMALL439, MA-THRESH theta = 0.00)")
    P("=" * 170)
    ok = True
    for cad in CADENCES:
        r = F[(F.panel == "SMALL439") & (F.family == "MA-THRESH") & (F.level == 0.00) &
              (F.cad == cad)].iloc[0]
        e = REPRO_290[cad]
        dc, ds = abs(r.c_bar - e["c_bar"]), abs(r.share - e["share"])
        good = dc < REPRO_CBAR_TOL and ds < REPRO_SHARE_TOL
        ok &= good
        P(f"  cad {cad}: c_bar {r.c_bar:.4f} vs {e['c_bar']:.4f} (d {dc:.5f}) | "
          f"gap0 {r.gap0_pp:+.4f} vs {e['gap0_pp']:+.4f} | pred0 {r.pred0_pp:+.4f} vs "
          f"{e['pred0_pp']:+.4f} | share {r.share:.4f} vs {e['share']:.4f} (d {ds:.5f})  "
          f"{'OK' if good else 'MISMATCH'}")
    P(f"  B4: {'PASS' if ok else 'FAIL'}")
    flush_log()

    # ---------------- the exposure-share curve
    P("\n" + "=" * 170)
    P("THE EXPOSURE-SHARE CURVE - every one of the 162 decomposition cells, full sample")
    P("=" * 170)
    for pname in PN:
        for family in FAMILIES:
            sub = F[(F.panel == pname) & (F.family == family)]
            P(f"\n--- {pname} / {family} ---")
            P(fmt(sub.set_index(["level", "cad"])[
                ["c_bar", "c_sd", "CAGR_rs0", "CAGR_dg0", "gap0_pp", "pred0_pp", "resid0_pp",
                 "share", "cov_c_r", "tiny"]]))
    P("\nQUANTILE family sanity: c_bar should sit at the requested x (drift between rebalances "
      "moves it slightly).")
    P(fmt(F[F.family == "QUANTILE"].pivot_table(index="level", columns="panel", values="c_bar")))

    P("\n" + "=" * 170)
    P("THE CURVE, COLLAPSED: mean share by c_bar decile-ish rung (this is the discount table)")
    P("=" * 170)
    F["cbin"] = pd.cut(F.c_bar, [0, .25, .35, .45, .55, .65, .75, .85, .92, 1.001])
    tab = F[~F.tiny].groupby("cbin", observed=True).agg(
        n=("share", "size"), c_bar=("c_bar", "mean"), share_mean=("share", "mean"),
        share_sd=("share", "std"), share_min=("share", "min"), share_max=("share", "max"),
        gap0_pp=("gap0_pp", "mean"), resid0_pp=("resid0_pp", "mean"))
    P(fmt(tab))
    P(f"\n(cells with |gap0| < {TINY_GAP_PP} pp excluded from the collapse as 0/0-unstable: "
      f"{int(F.tiny.sum())} of {len(F)})")

    # ---------------- H_QUEUE vs H_RATIO
    P("\n" + "=" * 170)
    P("H_QUEUE vs H_RATIO - graded on the pre-registered bars")
    P("=" * 170)
    arms, nq, nt, nsd = [], 0, 0, 0
    for pname in PN:
        for family in FAMILIES:
            sub = F[(F.panel == pname) & (F.family == family) & (~F.tiny)]
            X = np.column_stack([np.ones(len(sub)), sub.c_bar.to_numpy()])
            f = ols(X, sub.share.to_numpy(), ["const", "c_bar"])
            hi = sub[sub.c_bar >= BAR_QUEUE_CBAR]
            hi_mean = hi.share.mean() if len(hi) else np.nan
            q_ok = bool(np.isfinite(hi_mean) and abs(hi_mean - 1.0) <= BAR_QUEUE_TOL)
            t_ok = bool(abs(f["t"][1]) < BAR_RATIO_T)
            sd_ok = bool(sub.share.std() <= BAR_RATIO_SD)
            nq += q_ok; nt += t_ok; nsd += sd_ok
            arms.append(dict(panel=pname, family=family, n=len(sub),
                             slope=f["b"][1], t_slope=f["t"][1], R2=f["R2"],
                             share_mean=sub.share.mean(), share_sd=sub.share.std(),
                             share_min=sub.share.min(), share_max=sub.share.max(),
                             n_hi=len(hi), share_at_cbar_hi=hi_mean,
                             H_QUEUE_ok=q_ok, H_RATIO_t_ok=t_ok, H_RATIO_sd_ok=sd_ok))
    A = pd.DataFrame(arms)
    P(fmt(A.set_index(["panel", "family"])))
    P(f"\nH_QUEUE bar: mean share at c_bar >= {BAR_QUEUE_CBAR} within {BAR_QUEUE_TOL} of 1.000 "
      f"in >= {BAR_QUEUE_ARMS}/6 arms -> {nq}/6 -> "
      f"{'HOLDS' if nq >= BAR_QUEUE_ARMS else 'FAILS'}")
    P(f"H_RATIO bar: |t(slope)| < {BAR_RATIO_T} in a majority -> {nt}/6; "
      f"sd(share) <= {BAR_RATIO_SD} in a majority -> {nsd}/6 -> "
      f"{'HOLDS' if (nt >= 4 and nsd >= 4) else 'FAILS'}")
    P("\nWhat the first-order expansion predicts, checked directly: resid0 should be "
      "PROPORTIONAL to (1 - c_bar) if the eps cancels in the ratio.")
    for pname in PN:
        for family in FAMILIES:
            sub = F[(F.panel == pname) & (F.family == family) & (~F.tiny)]
            eps = 1 - sub.c_bar.to_numpy()
            for lbl, y in (("resid0", sub.resid0_pp.to_numpy()), ("gap0", sub.gap0_pp.to_numpy()),
                           ("pred0", sub.pred0_pp.to_numpy())):
                f = ols(np.column_stack([np.ones(len(sub)), eps]), y, ["const", "eps"])
                P(f"  {pname:9s} {family:10s} {lbl:6s} ~ 1 + (1-c_bar): "
                  f"const {f['b'][0]:+.4f} (t {f['t'][0]:+.2f})  "
                  f"slope {f['b'][1]:+.4f} (t {f['t'][1]:+.2f})  R2 {f['R2']:.4f}")
    flush_log()

    # ---------------- B3 panel vs level
    P("\n" + "=" * 170)
    P("B3 - PANEL or GATE LEVEL?  share ~ 1 + c_bar + panel dummies + family dummy + cadence dummies")
    P("=" * 170)
    S = F[~F.tiny].copy()
    pd_d = pd.get_dummies(S.panel, prefix="P", drop_first=True).astype(float)
    fd_d = pd.get_dummies(S.family, prefix="F", drop_first=True).astype(float)
    cd_d = pd.get_dummies(S.cad, prefix="C", drop_first=True).astype(float)
    blocks = [("const", np.ones((len(S), 1))), ("c_bar", S[["c_bar"]].to_numpy(float)),
              ("panel", pd_d.to_numpy()), ("family", fd_d.to_numpy()), ("cadence", cd_d.to_numpy())]
    names, cols, idx = [], {}, 0
    Xs = []
    for lbl, blk in blocks:
        Xs.append(blk)
        cols[lbl] = list(range(idx, idx + blk.shape[1]))
        names += ([lbl] if blk.shape[1] == 1 else
                  [f"{lbl}[{c}]" for c in (pd_d.columns if lbl == "panel" else
                                           fd_d.columns if lbl == "family" else cd_d.columns)])
        idx += blk.shape[1]
    X = np.column_stack(Xs)
    full = ols(X, S.share.to_numpy(), names)
    P(f"  n={full['n']}  R2={full['R2']:.4f}")
    for nm, bb, tt in zip(names, full["b"], full["t"]):
        P(f"    {nm:16s} b {bb:+.4f}  t {tt:+.2f}")
    P("\n  partial R2 (R2 lost by dropping the block):")
    pr = {}
    for lbl in ("c_bar", "panel", "family", "cadence"):
        pr[lbl] = partial_r2(X, S.share.to_numpy(), cols[lbl], names)
        P(f"    {lbl:10s} {pr[lbl]:.4f}")
    win = max(pr, key=lambda k: pr[k])
    P(f"\n  B3 ANSWER: largest partial R2 is {win} ({pr[win]:.4f}); "
      f"c_bar {pr['c_bar']:.4f} vs panel {pr['panel']:.4f} -> "
      f"{'LEVEL' if pr['c_bar'] > pr['panel'] else 'PANEL'} explains more of the share.")
    P("\n  Share by panel (pooling levels) and by level rung (pooling panels):")
    P(fmt(S.pivot_table(index="panel", columns="family", values="share",
                        aggfunc=["mean", "std", "size"])))
    P(fmt(S.pivot_table(index="cbin", columns="panel", values="share", aggfunc="mean",
                        observed=True)))
    flush_log()

    # ---------------- WF-B: the curve's own walk-forward
    P("\n" + "=" * 170)
    P("WF-B (rule 8 on the DELIVERABLE) - fit share ~ 1 + c_bar on IS cells, predict OOS share")
    P("=" * 170)
    I = D[D.window == "IS"].copy()
    O = D[D.window == "OOS"].copy()
    key = ["panel", "family", "level", "cad"]
    M = I.merge(O, on=key, suffixes=("_IS", "_OOS"))
    M = M[(M.gap0_pp_IS.abs() >= TINY_GAP_PP) & (M.gap0_pp_OOS.abs() >= TINY_GAP_PP)]
    Xi = np.column_stack([np.ones(len(M)), M.c_bar_IS.to_numpy()])
    fit = ols(Xi, M.share_IS.to_numpy(), ["const", "c_bar"])
    pred_curve = fit["b"][0] + fit["b"][1] * M.c_bar_OOS.to_numpy()
    pred_const = np.full(len(M), M.share_IS.mean())
    pred_290 = np.full(len(M), IDEA290_SHARE)
    y = M.share_OOS.to_numpy()
    P(f"  IS fit (n={fit['n']}): share = {fit['b'][0]:+.4f} {fit['b'][1]:+.4f} * c_bar   "
      f"(t {fit['t'][1]:+.2f}, R2 {fit['R2']:.4f})")
    for lbl, p_ in (("curve fitted on IS", pred_curve),
                    ("IS mean share (constant)", pred_const),
                    (f"idea 290's {IDEA290_SHARE} (constant)", pred_290)):
        P(f"    OOS mean |err| {np.abs(y - p_).mean():.4f}   RMSE "
          f"{np.sqrt(((y - p_) ** 2).mean()):.4f}   bias {np.mean(y - p_):+.4f}   [{lbl}]")
    P(f"  OOS share itself: mean {y.mean():.4f} sd {y.std():.4f} "
      f"min {y.min():.4f} max {y.max():.4f}  (n={len(y)})")
    P("  IS->OOS share rank stability (Spearman): "
      f"{M[['share_IS', 'share_OOS']].rank().corr().iloc[0, 1]:.4f}")
    P("  per-arm OOS mean |err|, curve vs IS-mean constant:")
    M = M.assign(e_curve=np.abs(y - pred_curve), e_const=np.abs(y - pred_const))
    P(fmt(M.pivot_table(index=["panel", "family"], values=["e_curve", "e_const"], aggfunc="mean")))

    # ---------------- WF-A: the book's walk-forward
    P("\n" + "=" * 170)
    P("WF-A (rule 8 on the BOOK) - (level, cadence) chosen on IS Sharpe inside each arm; OOS read once")
    P("=" * 170)
    order = {"W": 0, "M": 1, "Q": 2}
    wf = []
    for pname in PN:
        px, spy_px = PN[pname]
        start = px.index[260]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        for family in FAMILIES:
            for con in CONSTRUCTIONS:
                arm = G[(G.panel == pname) & (G.family == family) & (G.con == con)].copy()
                arm["tc"] = arm.cad.map(order)
                pick = arm.sort_values(["isSharpe", "level", "tc"],
                                       ascending=[False, False, True]).iloc[0]
                best = arm.sort_values("oSharpe", ascending=False).iloc[0]
                wf.append(dict(panel=pname, family=family, con=con,
                               pick_level=pick.level, pick_cad=pick.cad,
                               isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                               oMaxDD=pick.oMaxDD,
                               regret=pick.oSharpe - best.oSharpe,
                               best_level=best.level, best_cad=best.cad,
                               spy_oSharpe=spy_s["oSharpe"],
                               d_vs_SPY=pick.oSharpe - spy_s["oSharpe"],
                               p4a=pick.p4a, f4b=pick.f4b))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(W.set_index(["panel", "family", "con"])))

    # ---------------- KEEP paths
    P("\n" + "=" * 170)
    P(f"KEEP PATHS over all {len(G)} books (every one reported)")
    P("=" * 170)
    kp = G.groupby(["panel", "family", "con"]).agg(
        n=("p4a", "size"), keep4a=("p4a", "sum"), keep4b=("p4b", "sum"),
        CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
        oSharpe=("oSharpe", "mean"))
    P(fmt(kp))
    P(f"\n4a passes: {int(G.p4a.sum())} of {len(G)}.   4b passes: {int(G.p4b.sum())} of {len(G)}.")
    if G.p4b.any():
        P(fmt(G[G.p4b].sort_values("oSharpe", ascending=False)
              [["panel", "family", "level", "cad", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "oSharpe", "p4a"]].head(40).reset_index(drop=True)))
    P("\nfails4b census:")
    P(fmt(G.groupby("f4b").size().sort_values(ascending=False).to_frame("books").head(20), 0))
    P("\nFull grid (all 324 books):")
    for pname in PN:
        for family in FAMILIES:
            P(f"\n--- {pname} / {family} ---")
            P(fmt(G[(G.panel == pname) & (G.family == family)]
                  .set_index(["con", "level", "cad"])
                  [["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "CAGR0",
                    "gross_mean", "turn_yr", "dCAGR_ctrl", "dSharpe_ctrl", "p4a", "f4b"]]))

    flush_log()
    P(f"\nwrote {OUT.name}.grid.csv .decomp.csv .walkforward.csv .console.txt")
    flush_log()


if __name__ == "__main__":
    main()
