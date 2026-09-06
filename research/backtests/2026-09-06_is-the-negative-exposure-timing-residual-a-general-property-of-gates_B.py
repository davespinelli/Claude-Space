#!/usr/bin/env python3
"""Idea 297 - "is-the-negative-exposure-timing-residual-a-general-property-of-gates"
(lane B, 2026-09-06).

The question
------------
Idea 290 (lane B, 2026-09-06) showed that a DE-GROSSING gate book is ALGEBRAICALLY the same
gate's RESPREAD book run at time-varying leverage c_t = (names gated IN)/(names live), so its
0-bps CAGR gap splits exactly into

    gap0 = [ constant-leverage cash drag at the cell's own mean leverage c_bar ]   <- exposure
         + [ residual from the TIMING of c_t ]                                     <- gate content

On the 439-name sub-$2B panel the exposure term carried 91.4% of the gap and the residual was
NEGATIVE in 35 of 36 cells (mean -0.40 pp/yr, worst -1.24), WIDENING with band width
(-0.32 -> -0.57 pp) and with slower cadence (Q -0.75 pp).  Read literally that says de-grossing
does not merely hold less; it holds less at systematically the wrong times, and more so as the
dial slows.  Idea 298 then showed the SHARE is a property of the gate's FORM (a pure-exposure
QUANTILE gate has ~zero residual; an MA gate has a level-independent lump of 0.3-0.6 pp/yr) and
that its panel dummies were flat -- but it never tested the SIGN or the DIAL-DEPENDENCE off the
sub-$2B panel, which is what idea 297 asks.

QUEUE wording: "Re-run the same constant-leverage decomposition on the large-cap panels (U56,
B136) and on the live RULES v2 book, and report whether the sign and the dial-dependence hold
off the sub-$2B panel."

Four pre-registered hypotheses (bars fixed before any number was read)
----------------------------------------------------------------------
H1  SIGN GENERALITY.  On EACH large panel, resid0 < 0 in at least 33 of the 36
    (gate x cadence x band) cells -- the same 35/36 rate idea 290 found, minus slack for two
    cells.  Reported with an exact two-sided binomial sign test at p = 0.5.
    FAILS if either panel comes in under 33/36.

H2  BAND WIDENING.  On EACH panel the residual is more negative at the widest band than at the
    narrowest (mean resid0 at b=0.12 < mean at b=0.00) AND Spearman(band, resid0) < 0 with
    |t| >= 2 over that panel's 36 cells.  Both clauses must hold.

H3  CADENCE WIDENING.  On EACH panel the cadence means are ordered W > M > Q (i.e. the residual
    gets more negative as the dial slows), matching idea 290's Q = -0.75 pp.

H4  THE LIVE BOOK.  RULES v2 (universe.json, 200d +/-3% band, weekly, 0.75 gross) IS a DEGROSS
    construction.  Decompose the live book itself against its own RESPREAD twin and report
    c_bar, gap0, pred0, resid0 and the exposure share.  H4 holds if the live book's resid0 is
    negative -- i.e. the property the idea asks about is a property of the book we actually run.

B0  REPRODUCTION GATE, asserted before any new number is read.  The SMALL439 x MA cells of this
    script must reproduce idea 290's committed identity.csv on c_bar, gap0_pp, pred0_pp and
    resid0_pp to < 1e-6 (same panel, same start index, same construction).  If B0 fails, the
    rest of this script is measuring something else and the run is aborted.

Panels
-------
  SMALL439   idea 290's panel: data/prices_small.csv sub-$2B names, the 44 with
             max_1d_move >= 1.0 dropped.  Anchor / reproduction only.
  U56        research/universe.json (ETFs + mega-caps), SPY held out as benchmark.
  B136       research/universe_broad.json (~100 large caps + 36 ETFs), SPY held out.

Windows
--------
The three panels start on different days, so a panel contrast read on per-panel windows could be
a WINDOW contrast.  Every headline is therefore reported twice: FULL (each panel from its own
index[260], which is what reproduces idea 290) and COMMON (the latest of the three starts,
shared by all three panels).  IS = <= 2016-12-31 and OOS = 2017-01-01.. are also decomposed
separately, so the sign claim is tested across time as well as across panels.

Tuned parameters (PROTOCOL rule 4: at most two)
------------------------------------------------
    band b   in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}   (baseline.band_state, RULES v2 form)
    cadence  in {W, M, Q}
Reported at EVERY value, selected at none except inside the rule-8 walk-forward.  Panel, gate
form (MA / MAVOL) and construction (RESPREAD / DEGROSS) are REPORTED dimensions, not tuned --
the whole question is the contrast across them.

Grid: 3 panels x 2 gates x 3 cadences x 6 bands x 2 constructions = 216 cells, each at 10 bps
and 0 bps = 432 backtests, plus 9 cadence-matched no-filter controls x 2 rungs and the live
book.  Every cell printed.

Walk-forward (PROTOCOL rule 8)
-------------------------------
(band, cadence) chosen on data <= 2016-12-31 by in-sample Sharpe inside each of the 12
panel x gate x construction arms; 2017-2026 read once.  OOS CAGR/Sharpe/MaxDD reported against
the LIVE RULES v2 book, SPY and the matched no-filter control.  Both KEEP paths (4a vs the live
book, 4b vs SPY) evaluated on all 216 cells.

SURVIVORSHIP: all three panels are CURRENT constituents -- prices_small.csv is a screen of
today's sub-$2B names and universe(_broad).json are today's large caps/ETFs; no delistings.
Every headline here is an arm-minus-arm contrast on the SAME names and days (DEGROSS vs RESPREAD
share one gate mask), so the bias very largely cancels out of the residual; it does NOT cancel
out of the 4a/4b columns, which are levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import math
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
MAX_VOL = 0.60
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
CADENCES = ["W", "M", "Q"]
GATES = ["MA", "MAVOL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
PANELS = ["SMALL439", "U56", "B136"]
LARGE = ["U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

# pre-registered bars
H1_MIN_NEG = 33          # of 36 cells, per large panel
H2_MIN_T = 2.0           # |t| on Spearman(band, resid0)
B0_TOL = 1e-6            # reproduction of idea 290's identity.csv
P1_TOL = 1e-12           # algebraic exactness of the leverage identity

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


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
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, gate, band):
    g = band_state(px, band)
    if gate == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g & live_mask(px)


def book(px, gate, band, construction):
    g = gate_mask(px, gate, band)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


def cagr_of(r):
    return metrics(r)["CAGR"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def stat(r):
    m = metrics(r)
    h1, h2 = halves(r)
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def spearman(x, y):
    """Spearman rho plus the usual t = rho*sqrt((n-2)/(1-rho^2)); no scipy."""
    x = pd.Series(np.asarray(x, float)).rank()
    y = pd.Series(np.asarray(y, float)).rank()
    n = len(x)
    rho = float(np.corrcoef(x, y)[0, 1])
    t = rho * math.sqrt((n - 2) / max(1e-12, 1 - rho ** 2)) if n > 2 else np.nan
    return rho, t


def sign_p(k, n):
    """Exact two-sided binomial p for k successes of n at p=0.5."""
    tail = sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def decompose(r_dg0, r_rs0, held_dg, held_rs, window):
    """The idea-290 constant-leverage split, restricted to `window` (a slice of the index)."""
    d, r_, hd, hr = (s.loc[window] for s in (r_dg0, r_rs0, held_dg, held_rs))
    if len(d) < 60:
        return None
    c_t = (hd / hr.replace(0, np.nan)).fillna(0.0)
    c_bar = float(c_t.mean())
    cagr_rs = cagr_of(r_)
    gap0 = 100 * (cagr_of(d) - cagr_rs)
    pred0 = 100 * (cagr_of(c_bar * r_) - cagr_rs)
    return dict(c_bar=c_bar, c_sd=float(c_t.std()), gap0_pp=gap0, pred0_pp=pred0,
                resid0_pp=gap0 - pred0,
                share=(pred0 / gap0) if abs(gap0) > 1e-12 else np.nan,
                n_days=len(d))


# ---------------------------------------------------------------- main
def main():
    PX = panels()
    starts = {k: v[0].index[260] for k, v in PX.items()}
    ends = {k: v[0].index[-1] for k, v in PX.items()}
    common_start = max(starts.values())
    common_end = min(ends.values())

    P("=" * 175)
    P(f"Idea 297 is-the-negative-exposure-timing-residual-a-general-property-of-gates (lane B) | {SCRIPT}")
    P("=" * 175)
    for k in PANELS:
        yrs = len(PX[k][0].loc[starts[k]:]) / 252
        P(f"  {k}: {PX[k][0].index[0].date()} .. {ends[k].date()}; evaluated from "
          f"{starts[k].date()} ({yrs:.2f} yrs, {PX[k][0].shape[1]} names)")
    P(f"  COMMON window shared by all three panels: {common_start.date()} .. {common_end.date()} "
      f"({len(PX['SMALL439'][0].loc[common_start:common_end]) / 252:.2f} yrs)")
    P(f"Costs {COST_BPS} bps (and a 0-bps rung for the decomposition), gross {GROSS}, "
      f"next-day execution, no shorting, no leverage.")
    P(f"Pre-registered bars: H1 resid0<0 in >= {H1_MIN_NEG}/36 on EACH of U56 and B136; "
      f"H2 mean(b=0.12) < mean(b=0.00) AND |t(Spearman(band,resid0))| >= {H2_MIN_T}; "
      f"H3 cadence means ordered W > M > Q; H4 live RULES v2 resid0 < 0; "
      f"B0 repro of idea 290 identity.csv < {B0_TOL:g}.")

    for k in PANELS:
        y = PX[k][0].index.to_series().groupby(PX[k][0].index.year).count()
        if y.loc[2013:2024].max() > 300:
            P(f"!! {k} has a CALENDAR-DAY index - aborting."); sys.exit(1)
    P("Index sanity: all three panels ~252 rows/yr (trading-day index confirmed).")

    # ---------------- reference books ------------------------------------
    P("\n" + "-" * 175)
    P("REFERENCE BOOKS (per panel, own window)")
    P("-" * 175)
    ctrl, ctrl0, spy_stat = {}, {}, {}
    for k in PANELS:
        px, spy = PX[k]
        st = starts[k]
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)["returns"].loc[st:]
            ctrl[(k, cad)] = stat(rc)
            ctrl0[(k, cad)] = backtest(px, control_book(px), cost_bps=0, freq=cad)["returns"].loc[st:]
        spy_stat[k] = stat(spy.pct_change().fillna(0.0).loc[st:])

    px_u = load_universe()
    live_ret = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]
    live_s = stat(live_ret.loc[starts["U56"]:])

    ref = {f"CONTROL EWall {k} {c} (no filter)": ctrl[(k, c)] for k in PANELS for c in CADENCES}
    ref["RULES v2 on universe.json (LIVE BOOK, 4a comparand)"] = live_s
    for k in PANELS:
        ref[f"SPY on {k} window (4b comparand)"] = spy_stat[k]
    P(fmt(pd.DataFrame(ref).T))
    P(f"\nREPRODUCTION vs idea 49/52/290's SMALL439 no-filter control (weekly, 10 bps): "
      f"CAGR {ctrl[('SMALL439', 'W')]['CAGR']:.2%} (published 10.2%), "
      f"Sharpe {ctrl[('SMALL439', 'W')]['Sharpe']:.4f} (0.677-0.679), "
      f"MaxDD {ctrl[('SMALL439', 'W')]['MaxDD']:.2%} (-36.2%)")

    # ---------------- the grid --------------------------------------------
    P("\n" + "-" * 175)
    P("GRID - all 216 cells (3 panels x 2 gates x 3 cadences x 6 bands x 2 constructions), "
      "10 bps and 0 bps")
    P("-" * 175)
    rows, ret0, held = {}, {}, {}
    for k in PANELS:
        px, _ = PX[k]
        st = starts[k]
        years = len(px.loc[st:]) / 252
        for con in CONSTRUCTIONS:
            for gate in GATES:
                for cad in CADENCES:
                    for b in BANDS:
                        w = book(px, gate, b, con)
                        res = backtest(px, w, cost_bps=COST_BPS, freq=cad)
                        res0 = backtest(px, w, cost_bps=0, freq=cad)
                        key = (k, con, gate, cad, b)
                        r = res["returns"].loc[st:]
                        s = stat(r)
                        ret0[key] = res0["returns"].loc[st:]
                        held[key] = res["weights"].loc[st:].sum(axis=1)
                        rows[key] = dict(panel=k, con=con, gate=gate, cad=cad, band=b, **s,
                                         CAGR0=cagr_of(ret0[key]),
                                         gross_mean=held[key].mean(),
                                         turn_yr=res["turnover"].loc[st:].sum() / years,
                                         dCAGR_ctrl=s["CAGR"] - ctrl[(k, cad)]["CAGR"],
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[(k, cad)]["Sharpe"],
                                         p4a=verdict_4a(s, live_s),
                                         f4b=fail_4b(s, spy_stat[k]))
    G = pd.DataFrame(rows.values())
    G["p4b"] = G.f4b == "-"
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "CAGR0",
            "gross_mean", "turn_yr", "dCAGR_ctrl", "dSharpe_ctrl", "p4a", "f4b"]
    for k in PANELS:
        for con in CONSTRUCTIONS:
            for gate in GATES:
                sub = G[(G.panel == k) & (G.con == con) & (G.gate == gate)].set_index(["cad", "band"])[cols]
                P(f"\n--- {k} / {con} / gate {gate} ---")
                P(fmt(sub))
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- P1: the leverage identity, on every panel -----------
    P("\n" + "-" * 175)
    P("P1 - IS THE DE-GROSS BOOK EXACTLY THE RESPREAD BOOK AT TIME-VARYING LEVERAGE, ON EVERY PANEL?")
    P("-" * 175)
    p1 = []
    for k in PANELS:
        for gate in GATES:
            for cad in CADENCES:
                for b in BANDS:
                    kd, kr = (k, "DEGROSS", gate, cad, b), (k, "RESPREAD", gate, cad, b)
                    c_t = (held[kd] / held[kr].replace(0, np.nan)).fillna(0.0)
                    p1.append(dict(panel=k, gate=gate, cad=cad, band=b,
                                   max_abs_err=(ret0[kd] - c_t * ret0[kr]).abs().max()))
    P1 = pd.DataFrame(p1)
    worst = P1.groupby("panel").max_abs_err.max()
    P(fmt(worst.to_frame("worst_max_abs_err")))
    p1_pass = bool(P1.max_abs_err.max() < P1_TOL)
    P(f"P1: worst |r_dg,t - c_t*r_rs,t| over all 108 pairs = {P1.max_abs_err.max():.3e} "
      f"(bar {P1_TOL:g}) -> {'HOLDS' if p1_pass else 'FAILS'}")

    # ---------------- the decomposition, four windows ---------------------
    P("\n" + "-" * 175)
    P("CONSTANT-LEVERAGE DECOMPOSITION (idea 290's split) on FULL / COMMON / IS / OOS windows")
    P("-" * 175)
    wins = {"FULL": None, "COMMON": slice(common_start, common_end),
            "IS": slice(None, IS_END), "OOS": slice(OOS_START, None)}
    dec = []
    for k in PANELS:
        for gate in GATES:
            for cad in CADENCES:
                for b in BANDS:
                    kd, kr = (k, "DEGROSS", gate, cad, b), (k, "RESPREAD", gate, cad, b)
                    for wname, w in wins.items():
                        sl = slice(None) if w is None else w
                        d = decompose(ret0[kd], ret0[kr], held[kd], held[kr], sl)
                        if d is None:
                            continue
                        dec.append(dict(panel=k, window=wname, gate=gate, cad=cad, band=b, **d))
    D = pd.DataFrame(dec)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    for k in PANELS:
        sub = D[(D.panel == k) & (D.window == "FULL")].set_index(["gate", "cad", "band"])
        P(f"\n--- {k} / FULL window ---")
        P(fmt(sub[["c_bar", "c_sd", "gap0_pp", "pred0_pp", "resid0_pp", "share"]]))

    # ---------------- B0 reproduction gate --------------------------------
    P("\n" + "-" * 175)
    P("B0 REPRODUCTION GATE - SMALL439 x MA cells vs idea 290's committed identity.csv")
    P("-" * 175)
    ref_path = REPO / "research" / "backtests" / "2026-09-06_is-the-de-gross-cost-a-cash-drag-identity_B.identity.csv"
    b0_pass, b0_worst = None, np.nan
    if ref_path.exists():
        R = pd.read_csv(ref_path)
        mine = D[(D.panel == "SMALL439") & (D.window == "FULL")]
        m = R.merge(mine, on=["gate", "cad", "band"], suffixes=("_ref", "_new"))
        diffs = {c: (m[f"{c}_ref"] - m[f"{c}_new"]).abs().max()
                 for c in ["c_bar", "gap0_pp", "pred0_pp", "resid0_pp"]}
        b0_worst = max(diffs.values())
        b0_pass = bool(b0_worst < B0_TOL)
        P(f"  matched {len(m)} cells (both gates x 3 cadences x 6 bands)")
        for c, v in diffs.items():
            P(f"    max |idea290 - here| on {c:>10s} = {v:.3e}")
        P(f"  B0: worst {b0_worst:.3e} vs bar {B0_TOL:g} -> {'HOLDS' if b0_pass else 'FAILS'}")
        if not b0_pass:
            P("  !! B0 FAILED - the panel/window/construction is not idea 290's. ABORTING.")
            sys.exit(1)
    else:
        P("  !! idea 290 identity.csv not found - cannot assert B0.")

    # ---------------- H1 sign generality ----------------------------------
    P("\n" + "-" * 175)
    P("H1 - IS THE RESIDUAL NEGATIVE OFF THE SUB-$2B PANEL?  (36 cells per panel x window)")
    P("-" * 175)
    sgn = []
    for k in PANELS:
        for wname in wins:
            s = D[(D.panel == k) & (D.window == wname)]
            if s.empty:
                continue
            n, neg = len(s), int((s.resid0_pp < 0).sum())
            sgn.append(dict(panel=k, window=wname, n=n, n_neg=neg, frac_neg=neg / n,
                            mean_resid=s.resid0_pp.mean(), median_resid=s.resid0_pp.median(),
                            worst_resid=s.resid0_pp.min(), best_resid=s.resid0_pp.max(),
                            mean_gap0=s.gap0_pp.mean(), mean_share=s.share.mean(),
                            sign_p=sign_p(neg, n)))
    S = pd.DataFrame(sgn)
    P(fmt(S.set_index(["panel", "window"])))
    h1_full = {k: int(S[(S.panel == k) & (S.window == "FULL")].n_neg.iloc[0]) for k in PANELS}
    h1_common = {k: int(S[(S.panel == k) & (S.window == "COMMON")].n_neg.iloc[0]) for k in PANELS}
    h1_pass = all(h1_full[k] >= H1_MIN_NEG for k in LARGE)
    P(f"\nH1 (FULL window): SMALL439 {h1_full['SMALL439']}/36 (idea 290 published 35/36), "
      f"U56 {h1_full['U56']}/36, B136 {h1_full['B136']}/36; bar {H1_MIN_NEG}/36 on EACH large "
      f"panel -> {'HOLDS' if h1_pass else 'FAILS'}")
    P(f"H1 (COMMON window, same days for all three): SMALL439 {h1_common['SMALL439']}/36, "
      f"U56 {h1_common['U56']}/36, B136 {h1_common['B136']}/36")

    # ---------------- H2 band dial ----------------------------------------
    P("\n" + "-" * 175)
    P("H2 - DOES THE RESIDUAL WIDEN WITH BAND WIDTH?  (mean resid0_pp by band, FULL window)")
    P("-" * 175)
    band_tab = D[D.window == "FULL"].pivot_table(index="panel", columns="band", values="resid0_pp",
                                                 aggfunc="mean").reindex(PANELS)
    P(fmt(band_tab))
    h2 = []
    for k in PANELS:
        s = D[(D.panel == k) & (D.window == "FULL")]
        rho, t = spearman(s.band, s.resid0_pp)
        lo, hi = band_tab.loc[k, 0.00], band_tab.loc[k, 0.12]
        h2.append(dict(panel=k, mean_b000=lo, mean_b012=hi, delta=hi - lo, rho=rho, t=t,
                       clause_A=bool(hi < lo), clause_B=bool(rho < 0 and abs(t) >= H2_MIN_T)))
    H2 = pd.DataFrame(h2).set_index("panel")
    P("\n" + fmt(H2))
    h2_pass = bool(H2.loc[LARGE, ["clause_A", "clause_B"]].all().all())
    P(f"H2 (both clauses on BOTH large panels; idea 290 published -0.32 -> -0.57 pp on "
      f"SMALL439) -> {'HOLDS' if h2_pass else 'FAILS'}")

    # ---------------- H3 cadence dial -------------------------------------
    P("\n" + "-" * 175)
    P("H3 - DOES THE RESIDUAL WIDEN AS THE CADENCE SLOWS?  (mean resid0_pp by cadence, FULL)")
    P("-" * 175)
    cad_tab = D[D.window == "FULL"].pivot_table(index="panel", columns="cad", values="resid0_pp",
                                                aggfunc="mean").reindex(PANELS)[CADENCES]
    P(fmt(cad_tab))
    h3_rows = [dict(panel=k, W=cad_tab.loc[k, "W"], M=cad_tab.loc[k, "M"], Q=cad_tab.loc[k, "Q"],
                    ordered=bool(cad_tab.loc[k, "W"] > cad_tab.loc[k, "M"] > cad_tab.loc[k, "Q"]))
                for k in PANELS]
    H3 = pd.DataFrame(h3_rows).set_index("panel")
    P("\n" + fmt(H3))
    h3_pass = bool(H3.loc[LARGE, "ordered"].all())
    P(f"H3 (W > M > Q on BOTH large panels; idea 290 published Q = -0.75 pp on SMALL439) "
      f"-> {'HOLDS' if h3_pass else 'FAILS'}")

    # by gate form, for continuity with idea 298
    gate_tab = D[D.window == "FULL"].pivot_table(index="panel", columns="gate",
                                                 values=["resid0_pp", "share", "c_bar"],
                                                 aggfunc="mean").reindex(PANELS)
    P("\nBy gate form (continuity with idea 298's 'the share is the gate's FORM' finding):")
    P(fmt(gate_tab))

    # ---------------- H4 the live book ------------------------------------
    P("\n" + "-" * 175)
    P("H4 - THE LIVE RULES v2 BOOK DECOMPOSED AGAINST ITS OWN RESPREAD TWIN")
    P("-" * 175)
    st = px_u.index[260]
    # baseline.rules_v2_weights' own liveness convention: e = px.notna() (no shift(1) clause),
    # denominator = names PRICED that day; gated-out weight goes to cash.
    e_live = px_u.notna()
    g_live = band_state(px_u, 0.03) & e_live
    n_live = e_live.sum(axis=1).replace(0, np.nan)
    k_live = g_live.sum(axis=1).replace(0, np.nan)
    w_dg = (g_live.astype(float).div(n_live, axis=0) * GROSS).fillna(0.0)  # == rules_v2_weights
    w_rs = (g_live.astype(float).div(k_live, axis=0) * GROSS).fillna(0.0)  # the respread twin
    chk = float((w_dg - rules_v2_weights(px_u)).abs().max().max())
    P(f"  reconstruction check: max |w_dg - baseline.rules_v2_weights| = {chk:.3e} "
      f"(the live book IS the DEGROSS construction)")
    live_rows = []
    for tag, w in (("DEGROSS (live)", w_dg), ("RESPREAD twin", w_rs)):
        r10 = backtest(px_u, w, cost_bps=COST_BPS, freq="W")
        r0 = backtest(px_u, w, cost_bps=0, freq="W")
        live_rows.append((tag, r10, r0))
    ld10, ld0 = live_rows[0][1], live_rows[0][2]
    lr10, lr0 = live_rows[1][1], live_rows[1][2]
    hd, hr = ld10["weights"].loc[st:].sum(axis=1), lr10["weights"].loc[st:].sum(axis=1)
    live_dec = {}
    for wname, w in wins.items():
        sl = slice(None) if w is None else w
        d = decompose(ld0["returns"].loc[st:], lr0["returns"].loc[st:], hd, hr, sl)
        if d:
            live_dec[wname] = d
    LD = pd.DataFrame(live_dec).T
    P("\n" + fmt(LD))
    lt = pd.DataFrame({"DEGROSS (live RULES v2)": stat(ld10["returns"].loc[st:]),
                       "RESPREAD twin": stat(lr10["returns"].loc[st:]),
                       "SPY": spy_stat["U56"]}).T
    P("\n" + fmt(lt))
    h4_resid = float(LD.loc["FULL", "resid0_pp"])
    h4_pass = bool(h4_resid < 0)
    P(f"\nH4: live RULES v2 resid0 = {h4_resid:+.4f} pp/yr (exposure share "
      f"{float(LD.loc['FULL', 'share']):.4f}, c_bar {float(LD.loc['FULL', 'c_bar']):.4f}) "
      f"-> {'HOLDS' if h4_pass else 'FAILS'}")
    LD.to_csv(f"{OUT}.livebook.csv")

    # ---------------- rule 8 walk-forward ---------------------------------
    P("\n" + "-" * 175)
    P("RULE 8 WALK-FORWARD - (band, cadence) chosen on <= 2016-12-31 by IS Sharpe inside each of")
    P("the 12 panel x gate x construction arms; 2017-2026 read once.  Ties -> wider band, slower cadence.")
    P("-" * 175)
    order = {"W": 0, "M": 1, "Q": 2}
    wf = []
    for k in PANELS:
        for con in CONSTRUCTIONS:
            for gate in GATES:
                arm = G[(G.panel == k) & (G.con == con) & (G.gate == gate)].copy()
                arm["tc"] = arm.cad.map(order)
                pick = arm.sort_values(["isSharpe", "band", "tc"],
                                       ascending=[False, False, False]).iloc[0]
                best = arm.sort_values("oSharpe", ascending=False).iloc[0]
                wf.append(dict(panel=k, con=con, gate=gate, pick_band=pick.band, pick_cad=pick.cad,
                               isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                               oMaxDD=pick.oMaxDD,
                               regret=pick.oSharpe - best.oSharpe,
                               best_band=best.band, best_cad=best.cad,
                               vs_ctrl=pick.oSharpe - ctrl[(k, pick.cad)]["oSharpe"],
                               vs_SPY=pick.oSharpe - spy_stat[k]["oSharpe"],
                               vs_LIVE=pick.oSharpe - live_s["oSharpe"]))
    WF = pd.DataFrame(wf)
    P(fmt(WF.set_index(["panel", "con", "gate"])))
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\nOOS comparands: LIVE RULES v2 {live_s['oCAGR']:.2%}/{live_s['oSharpe']:.4f}/"
      f"{live_s['oMaxDD']:.1%}")
    for k in PANELS:
        P(f"   SPY on {k} window {spy_stat[k]['oCAGR']:.2%}/{spy_stat[k]['oSharpe']:.4f}/"
          f"{spy_stat[k]['oMaxDD']:.1%} | control EWall W {ctrl[(k, 'W')]['oCAGR']:.2%}/"
          f"{ctrl[(k, 'W')]['oSharpe']:.4f}/{ctrl[(k, 'W')]['oMaxDD']:.1%}")
    P(f"Picks beating SPY OOS on Sharpe: {(WF.vs_SPY > 0).sum()} of {len(WF)}; the matched "
      f"no-filter control: {(WF.vs_ctrl > 0).sum()} of {len(WF)}; the LIVE book: "
      f"{(WF.vs_LIVE > 0).sum()} of {len(WF)}")

    # WF on the RESIDUAL itself: is the IS sign predictive of the OOS sign?
    P("\nWALK-FORWARD ON THE RESIDUAL ITSELF (does the IS sign predict the OOS sign, per cell?)")
    piv = D.pivot_table(index=["panel", "gate", "cad", "band"], columns="window",
                        values="resid0_pp")
    piv = piv.dropna(subset=["IS", "OOS"])
    piv["same_sign"] = np.sign(piv.IS) == np.sign(piv.OOS)
    agree = piv.groupby(level=0).agg(n=("same_sign", "size"), same=("same_sign", "sum"),
                                     IS_mean=("IS", "mean"), OOS_mean=("OOS", "mean"),
                                     OOS_neg=("OOS", lambda s: int((s < 0).sum())))
    agree["frac_same"] = agree["same"] / agree.n
    P(fmt(agree.reindex(PANELS)))
    P("Naive OOS predictor comparison (pp/yr MAE on the 36 cells per panel):")
    mae = []
    for k in PANELS:
        s = piv.loc[k]
        mae.append(dict(panel=k, MAE_zero=s.OOS.abs().mean(),
                        MAE_IS_cell=(s.OOS - s.IS).abs().mean(),
                        MAE_IS_panel_mean=(s.OOS - s.IS.mean()).abs().mean()))
    P(fmt(pd.DataFrame(mae).set_index("panel")))

    # ---------------- KEEP paths -------------------------------------------
    P("\n" + "-" * 175)
    P("KEEP PATHS - both evaluated on all 216 cells")
    P("-" * 175)
    P(f"4a (Sharpe > LIVE RULES v2 in BOTH halves AND MaxDD no worse): {int(G.p4a.sum())} of {len(G)}")
    P(f"4b (Sharpe > SPY H1, H2 and OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's): "
      f"{int(G.p4b.sum())} of {len(G)}")
    binding = pd.Series([b for f in G.f4b for b in (f.split(",") if f != "-" else [])]).value_counts()
    P("Binding 4b bars (cells failing each):")
    P(binding.to_string())
    if G.p4b.any():
        P(fmt(G[G.p4b].set_index(["panel", "con", "gate", "cad", "band"])[cols]))
        P("(4b passers are LEVELS on a survivorship-screened panel, and none of them is a "
          "pre-registered dial of this idea - they are reported, not claimed.)")

    # ---------------- verdict ----------------------------------------------
    P("\n" + "=" * 175)
    P("VERDICT")
    P("=" * 175)
    res = [("B0 reproduction of idea 290", b0_pass), ("P1 leverage identity (all panels)", p1_pass),
           ("H1 sign generality", h1_pass), ("H2 band widening", h2_pass),
           ("H3 cadence widening", h3_pass), ("H4 live book residual negative", h4_pass)]
    for tag, ok in res:
        P(f"  {tag}: {'HOLDS' if ok else 'FAILS' if ok is not None else 'NOT ASSERTED'}")
    n_hold = sum(1 for _, ok in res[2:] if ok)
    verdict = ("GENERAL PROPERTY CONFIRMED" if n_hold == 4 else
               "PARTLY GENERAL" if n_hold >= 2 else "NOT A GENERAL PROPERTY")
    P(f"\n{verdict}  ({n_hold} of the 4 pre-registered hypotheses hold)")
    P(f"No new book proposed: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}.")

    summary = pd.DataFrame([dict(
        b0_worst=b0_worst, b0=b0_pass, p1_worst=P1.max_abs_err.max(), p1=p1_pass,
        h1_small=h1_full["SMALL439"], h1_u56=h1_full["U56"], h1_b136=h1_full["B136"], h1=h1_pass,
        h1c_small=h1_common["SMALL439"], h1c_u56=h1_common["U56"], h1c_b136=h1_common["B136"],
        h2=h2_pass, h3=h3_pass, h4_resid_pp=h4_resid, h4=h4_pass,
        mean_resid_small=float(S[(S.panel == "SMALL439") & (S.window == "FULL")].mean_resid.iloc[0]),
        mean_resid_u56=float(S[(S.panel == "U56") & (S.window == "FULL")].mean_resid.iloc[0]),
        mean_resid_b136=float(S[(S.panel == "B136") & (S.window == "FULL")].mean_resid.iloc[0]),
        pass4a=int(G.p4a.sum()), pass4b=int(G.p4b.sum()), n_cells=len(G), verdict=verdict)])
    summary.to_csv(f"{OUT}.summary.csv", index=False)
    S.to_csv(f"{OUT}.signs.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nWrote {Path(f'{OUT}.grid.csv').name}, {Path(f'{OUT}.decomp.csv').name}, "
          f"{Path(f'{OUT}.signs.csv').name}, {Path(f'{OUT}.livebook.csv').name}, "
          f"{Path(f'{OUT}.walkforward.csv').name}, {Path(f'{OUT}.summary.csv').name}, "
          f"{Path(f'{OUT}.console.txt').name}")


if __name__ == "__main__":
    main()
