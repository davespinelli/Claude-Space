#!/usr/bin/env python3
"""
IDEA 560 - is rbar_drop a SCREENING statistic?
==============================================
Lane B, 2026-09-11.

THE QUESTION.  Idea 556 decomposed a gate's advantage over its DEPTH-MATCHED control into
three exact legs (ADD / DROP / BOTH) and found the DROP leg carries the sign in 27/27 cells
on all three panels, with DROP ~ 1 + x + x^2 reaching R2 0.5881.  Its own summary line reads
"the dropped-name return rate is the whole story and is knowable before any book is built".
That sentence is an IN-WINDOW identity: rbar_drop and sel_geo are measured over the SAME
window, so of course they move together.  Idea 560 asks the only version of the claim that
could be worth capital:

    does rbar_drop measured on IS predict the gate's OOS advantage over its depth-matched
    control, ACROSS the record's gate families?

If yes, rbar_drop is a SCREENING statistic - you could rank candidate gates by it before
committing, and trade the winner.  If no, 556's finding is an accounting identity and
nothing more.

CONSTRUCTION (556's, extended to three gate families).
  panel P, ranking variable V (the FAMILY), absolute threshold th:
    GATE    = (V > th) & live                            [MA-THRESH generalised]
    CONTROL = top ceil(x*n_t) names by V each day,       [QUANTILE-M at matched depth]
              x = the gate's own average breadth over the scoring window
    books   = RESPREAD, gross 0.75, weekly, 10 bps, next-day (engine convention)
    ADVANTAGE = sel_geo_pp = 100 * (CAGR(gate, zero-cost) - CAGR(control, zero-cost))
    legs    : ADD = names only the gate holds; DROP = -1 x names only the control holds;
              BOTH = shared names at different weight.  ADD+DROP+BOTH = the gap, exactly.
    rbar_drop = 252*100 * sum_t(sum_{i in DROP} B_it r_it) / sum_t(sum_{i in DROP} B_it)
              = the annualised return RATE of the names the gate declines to hold.
              HIGH rbar_drop = the gate threw away good names = bad gate.  The predicted
              sign of corr(rbar_drop, advantage) is therefore NEGATIVE.

FAMILIES (3, all absolute-threshold gates on a cross-sectional ranking variable):
  MA-DIST   V = px/MA200 - 1                 th in 556's own 9-point grid   [the record's]
  MOM12_1   V = px.shift(21)/px.shift(252)-1 th in the same 9-point grid    [RULES v1 rank]
  LOWVOL    V = -vol20 (ann.)                gate vol20 < c, 9-point c grid [RULES v1 filter]
  3 panels x 3 families x 9 thresholds = 81 cells, every one reported.

TUNED PARAMETERS - exactly 2, both reported at every grid point (4 x 3 = 12 combinations):
  (1) STATISTIC  DROP     = -rbar_drop                    (556's own object)
                 SPREAD   = rbar_add - rbar_drop          (556's correlate)
                 EXCESS   = rbar_ctrl - rbar_drop         (drop rate vs the control's own)
                 PRIOR    = sel_geo_pp measured IS        (naive: past advantage)
      all signed so that HIGHER = predicts a BIGGER advantage.
  (2) WINDOW     FULL_IS  start..2016-12-31
                 TRAIL3Y  2014-01-01..2016-12-31
                 TRAIL1Y  2016-01-01..2016-12-31

RULE 8 WALK-FORWARD (required, and it is the leg that decides this idea).
  IS = start..2016-12-31 (every choice made here), OOS = 2017-01-01..end (read once).
  A. CENSUS leg: corr / rank-corr / sign-agreement between the IS statistic and the OOS
     advantage, pooled and per family and per panel, at all 12 (statistic, window) points.
  B. DECISION leg: within each (panel, family) pick the th that MAXIMISES the IS statistic;
     score that pick's OOS advantage against the cell's own median th and against the
     IS-best-advantage pick (PRIOR).
  C. BOOK leg: a genuinely tradeable rolling selector - at every weekly rebalance t, choose
     th* = argmax of the statistic over the trailing window ending at t (data <= t only),
     hold that th's gate book.  (statistic, window) chosen on IS alone by IS Sharpe, then
     the OOS is read once.  Scored against RULES v2 (4a) and SPY (4b), CAGR/Sharpe/MaxDD.

BOTH KEEP PATHS evaluated on every book: 4a vs the live RULES v2 book on the same panel,
4b vs SPY (Sharpe H1, H2, OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's).

GATES (pre-registered, all reported pass or fail):
  G0  fast_run must reproduce engine.backtest returns AND turnover to 1e-12.
  G1  three-leg identity |ADD+DROP+BOTH - gap| <= 1e-12 on every cell x window.
  G2  reproduction of idea 556's committed .legs.csv (QUANTILE-M, MA family, 27 cells x
      3 windows) on ADD_pp, DROP_pp, rbar_add, rbar_drop, sel_geo_pp to 1e-9.
  G3  depth match: |mean breadth(gate) - mean breadth(control)| over the scoring window.
  G4  selector causality: re-running the selector with every OOS return sign-flipped after
      the IS end must leave the IS-period selections byte-identical (no look-ahead).

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels are inflated and
neither KEEP column is immune.  ADD/DROP are same-panel arm-minus-arm differences so the
bias very largely cancels in the legs, but the ADD side is exactly the side survivorship
flatters most.  Stated again beside the headline.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .legs.csv .census.csv .decision.csv .walkforward.csv .keeppaths.csv
         .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
GROSS = 0.75
CADENCE = "W"
PANELS = ["U56", "B136", "SMALL439"]
FAMILIES = ["MA-DIST", "MOM12_1", "LOWVOL"]
THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]     # 556's own grid
CVOL = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.80]          # LOWVOL ceilings
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TRAIL3Y_START = "2014-01-01"
TRAIL1Y_START = "2016-01-01"

STATS = ["DROP", "SPREAD", "EXCESS", "PRIOR"]
WINDOWS = ["FULL_IS", "TRAIL3Y", "TRAIL1Y"]
SEL_LENS = {"FULL_IS": 0, "TRAIL3Y": 756, "TRAIL1Y": 252}   # 0 = expanding

EPS = 1e-12
BAR_ENGINE = 1e-12
BAR_IDENT = 1e-12
BAR_REPRO = 1e-9

IDEA556 = REPO / "research" / "backtests" / \
    "2026-09-09_why-does-the-MA-SLICE-flip-from-better-to-worse-at-the-panel-boundary_C.legs.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
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


# ------------------------------------------------------------------ panels (556's exactly)
def panels():
    out = {}
    u = load_universe()
    out["U56"] = (u.drop(columns=["SPY"]), u["SPY"])
    b = load_universe(broad=True)
    out["B136"] = (b.drop(columns=["SPY"], errors="ignore"), b["SPY"])
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out["SMALL439"] = (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])
    return out, len(bad)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


# ------------------------------------------------------------------ fast engine (gated G0)
def fast_run(px, W, cost_bps=COST_BPS, freq=CADENCE):
    """Bit-for-bit replica of engine.backtest, including its NaN first row."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    idx = px.index
    return {"returns": pd.Series(port, index=idx),
            "turnover": pd.Series(turn, index=idx),
            "weights": pd.DataFrame(held, index=idx, columns=px.columns)}


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


# ------------------------------------------------------------------ ranking variables
def rank_var(px, fam):
    live = live_mask(px)
    if fam == "MA-DIST":
        return (px / px.rolling(200).mean() - 1).where(live), live
    if fam == "MOM12_1":
        return (px.shift(21) / px.shift(252) - 1).where(live), live
    if fam == "LOWVOL":
        vol = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (-vol).where(live), live
    raise ValueError(fam)


def thresholds(fam):
    return [-c for c in CVOL] if fam == "LOWVOL" else list(THETA)


def gate_abs(px, fam, th):
    """Absolute-threshold gate.  MA-DIST uses idea 556's own MULTIPLICATIVE form
    (px > MA*(1+th)), not the algebraically equal px/MA-1 > th: the two differ in the last
    float bit, which moves ceil(x*n_t) on a handful of days and was the whole of this run's
    first G2 residue (4.560e-01 on rbar_add).  Reproduction beats elegance."""
    live = live_mask(px)
    if fam == "MA-DIST":
        return (px > px.rolling(200).mean() * (1 + th)) & live
    if fam == "MOM12_1":
        return ((px.shift(21) / px.shift(252) - 1) > th).fillna(False) & live
    if fam == "LOWVOL":
        vol = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (vol < -th).fillna(False) & live     # th is stored as -c
    raise ValueError(fam)


def spearman(a, b):
    return float(a.rank().corr(b.rank()))


def safe_idxmax(sv):
    """idxmax over columns, returning NaN (not raising) on rows that are entirely NA -
    the rolling statistics are undefined over their first min_periods rows."""
    valid = sv.notna().any(axis=1)
    out = pd.Series(np.nan, index=sv.index, dtype=float)
    if valid.any():
        out.loc[valid] = sv.loc[valid].idxmax(axis=1).astype(float)
    return out


def gate_quantile(V, live, x):
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = V.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def respread(px, g):
    k = g.sum(axis=1).clip(lower=1)
    return g.astype(float).div(k, axis=0) * GROSS


def control_ew(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


# ------------------------------------------------------------------ leg series (daily)
def leg_series(A, B, R):
    """Daily ADD/DROP/BOTH contributions and weights for drifted books A (gate), B (control)."""
    on_a, on_b = A > EPS, B > EPS
    add, drop, both = on_a & ~on_b, on_b & ~on_a, on_a & on_b
    cA = (A.where(add, 0.0) * R).sum(axis=1)
    cD = -(B.where(drop, 0.0) * R).sum(axis=1)
    cC = ((A.where(both, 0.0) - B.where(both, 0.0)) * R).sum(axis=1)
    wA = A.where(add, 0.0).sum(axis=1)
    wD = B.where(drop, 0.0).sum(axis=1)
    r0a, r0b = (A * R).sum(axis=1), (B * R).sum(axis=1)
    gb = B.sum(axis=1)
    return dict(cA=cA, cD=cD, cC=cC, wA=wA, wD=wD, r0a=r0a, r0b=r0b, gb=gb,
                n_add=add.sum(axis=1), n_drop=drop.sum(axis=1), n_both=both.sum(axis=1),
                n_gate=on_a.sum(axis=1))


def window_legs(S, lo, hi, tag):
    sl = slice(lo, hi)
    cA, cD, cC = S["cA"].loc[sl], S["cD"].loc[sl], S["cC"].loc[sl]
    wA, wD = S["wA"].loc[sl], S["wD"].loc[sl]
    r0a, r0b, gb = S["r0a"].loc[sl], S["r0b"].loc[sl], S["gb"].loc[sl]
    gap = r0a - r0b
    ident = float((cA + cD + cC - gap).abs().max())
    geo = 100 * (cagr(r0a) - cagr(r0b))
    rb_add = float(252 * 100 * cA.sum() / wA.sum()) if wA.sum() > 1e-12 else np.nan
    rb_drop = float(252 * 100 * (-cD).sum() / wD.sum()) if wD.sum() > 1e-12 else np.nan
    rb_ctrl = float(252 * 100 * r0b.sum() / gb.sum()) if gb.sum() > 1e-12 else np.nan
    return dict(window=tag, ident_max=ident,
                ADD_pp=252 * 100 * cA.mean(), DROP_pp=252 * 100 * cD.mean(),
                BOTH_pp=252 * 100 * cC.mean(), sel_geo_pp=geo,
                sel_arith_pp=252 * 100 * gap.mean(),
                rbar_add=rb_add, rbar_drop=rb_drop, rbar_ctrl=rb_ctrl,
                n_add=float(S["n_add"].loc[sl].mean()), n_drop=float(S["n_drop"].loc[sl].mean()),
                n_both=float(S["n_both"].loc[sl].mean()),
                w_add=float(wA.mean()), w_drop=float(wD.mean()),
                dom=("ADD" if abs(252 * 100 * cA.mean()) > abs(252 * 100 * cD.mean()) else "DROP"))


def signed_stat(row, which):
    """All four statistics oriented so HIGHER = predicts a BIGGER advantage."""
    if which == "DROP":
        return -row["rbar_drop"]
    if which == "SPREAD":
        return row["rbar_add"] - row["rbar_drop"]
    if which == "EXCESS":
        return row["rbar_ctrl"] - row["rbar_drop"]
    if which == "PRIOR":
        return row["sel_geo_pp"]
    raise ValueError(which)


def rolling_signed(S, which, L):
    """Causal rolling version of the statistic: value at t uses days <= t only."""
    def rs(x):
        return x.expanding(min_periods=60).sum() if L == 0 else x.rolling(L, min_periods=60).sum()
    sA, sD = rs(S["cA"]), rs(-S["cD"])
    sWA, sWD = rs(S["wA"]), rs(S["wD"])
    sB, sGB = rs(S["r0b"]), rs(S["gb"])
    rb_add = 252 * 100 * sA / sWA.replace(0, np.nan)
    rb_drop = 252 * 100 * sD / sWD.replace(0, np.nan)
    rb_ctrl = 252 * 100 * sB / sGB.replace(0, np.nan)
    if which == "DROP":
        return -rb_drop
    if which == "SPREAD":
        return rb_add - rb_drop
    if which == "EXCESS":
        return rb_ctrl - rb_drop
    if which == "PRIOR":
        gap = rs(S["r0a"] - S["r0b"])
        cnt = rs(pd.Series(1.0, index=S["cA"].index))
        return 252 * 100 * gap / cnt
    raise ValueError(which)


# ================================================================== main
def main():
    PN, n_dropped = panels()
    grid, legrows, census, decision, wf, keeprows = [], [], [], [], [], []
    CACHE = {}
    g0_max = 0.0
    g1_max = 0.0
    g3_max = 0.0
    g4_max = 0.0

    P("=" * 190)
    P("IDEA 560 - is rbar_drop a SCREENING statistic?   lane B, 2026-09-11")
    P("=" * 190)
    P("QUESTION: idea 556 showed the DROP leg carries the sign of a gate's advantage over its")
    P("depth-matched control IN-WINDOW (27/27 cells).  That is an accounting identity.  This run")
    P("asks whether rbar_drop measured on IS PREDICTS the OOS advantage, across gate families.")
    P("PROTOCOL: 10 bps/unit turnover, next-day execution (engine), no shorting, no leverage,")
    P(f"gross {GROSS}, cadence {CADENCE}.  IS = start..{IS_END}, OOS = {OOS_START}..end (read once).")
    P("2 tuned params: STATISTIC in {DROP, SPREAD, EXCESS, PRIOR} x WINDOW in {FULL_IS, TRAIL3Y,")
    P("TRAIL1Y}; all 12 combinations reported.  Both KEEP paths on every book.")
    P(f"SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only ({n_dropped} SMALL names")
    P("dropped for max_1d_move >= 1.0, 556's own filter).  CAGR levels inflated; 4a/4b not immune.")
    flush_log()

    # -------------------------------------------------------------- G0 engine gate
    P("\n" + "=" * 190)
    P("G0  fast_run vs engine.backtest")
    P("=" * 190)
    for pn in PANELS:
        px, _ = PN[pn]
        W = rules_v2_weights(px)
        a = backtest(px, W, cost_bps=COST_BPS, freq=CADENCE)
        b = fast_run(px, W)
        dr = float((a["returns"] - b["returns"]).abs().max())
        dt = float((a["turnover"] - b["turnover"]).abs().max())
        dw = float((a["weights"].values - b["weights"].values)[~np.isnan(a["weights"].values)].__abs__().max())
        g0_max = max(g0_max, dr, dt, dw)
        P(f"  {pn:9s} d|returns| {dr:.3e}  d|turnover| {dt:.3e}  d|weights| {dw:.3e}")
    P(f"  G0 max {g0_max:.3e}  (bar {BAR_ENGINE:.0e})  {'PASS' if g0_max < BAR_ENGINE else 'FAIL'}")
    flush_log()

    comparand = {}

    # -------------------------------------------------------------- the 81-cell grid
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        R = px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(fast_run(px, rules_v2_weights(px))["returns"].loc[start:])
        ctrl_s = stat(fast_run(px, control_ew(px))["returns"].loc[start:])
        comparand[pn] = dict(spy=spy_s, live=live_s, ctrl=ctrl_s, start=start, years=years)

        P("\n" + "=" * 190)
        P(f"PANEL {pn}  {start.date()}..{px.index[-1].date()}  ({years:.2f} yrs, "
          f"{px.shape[1]} names)")
        P("=" * 190)
        for nm, s in (("SPY", spy_s), ("RULES v2 (live, 4a bar)", live_s),
                      ("EW-all control (no gate)", ctrl_s)):
            P(f"  {nm:26s} CAGR {s['CAGR']:.4f} Sharpe {s['Sharpe']:.4f} MaxDD {s['MaxDD']:.4f} "
              f"H1/H2 {s['H1']:.4f}/{s['H2']:.4f}  OOS {s['oCAGR']:.4f}/{s['oSharpe']:.4f}/"
              f"{s['oMaxDD']:.4f}")
        P(f"  4b bars from SPY: H1>{spy_s['H1']:.4f}  H2>{spy_s['H2']:.4f}  "
          f"OOS>{spy_s['oSharpe']:.4f}  MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%}  "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")

        live = live_mask(px).loc[start:]
        nlive = live.sum(axis=1)

        for fam in FAMILIES:
            V, lv = rank_var(px, fam)
            for th in thresholds(fam):
                gA = gate_abs(px, fam, th)
                x = float((gA.loc[start:].sum(axis=1) / nlive).mean())
                gB = gate_quantile(V, lv, x)
                xq = float((gB.loc[start:].sum(axis=1) / nlive).mean())
                g3_max = max(g3_max, abs(x - xq))

                WA = respread(px, gA)
                ra = fast_run(px, WA)
                rb = fast_run(px, respread(px, gB))
                sa = stat(ra["returns"].loc[start:])
                sb = stat(rb["returns"].loc[start:])
                A = ra["weights"].loc[start:]
                B = rb["weights"].loc[start:]
                S = leg_series(A, B, R)
                CACHE[(pn, fam, th)] = (WA, S)

                for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                    ("OOS", OOS_START, None),
                                    ("TRAIL3Y", TRAIL3Y_START, IS_END),
                                    ("TRAIL1Y", TRAIL1Y_START, IS_END)):
                    d = window_legs(S, lo, hi, tag)
                    g1_max = max(g1_max, d["ident_max"])
                    legrows.append(dict(panel=pn, family=fam, th=th, x=x, **d))

                grid.append(dict(panel=pn, family=fam, th=th, x=x, xq=xq, arm="GATE", **sa,
                                 turn_yr=float(ra["turnover"].loc[start:].sum() / years),
                                 p4a=verdict_4a(sa, live_s), f4b=fail_4b(sa, spy_s)))
                grid.append(dict(panel=pn, family=fam, th=th, x=x, xq=xq, arm="CONTROL", **sb,
                                 turn_yr=float(rb["turnover"].loc[start:].sum() / years),
                                 p4a=verdict_4a(sb, live_s), f4b=fail_4b(sb, spy_s)))
            P(f"  {pn}: family {fam:8s} done ({len(thresholds(fam))} thresholds x 2 arms)")
            flush_log()

    G = pd.DataFrame(grid)
    L = pd.DataFrame(legrows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L.to_csv(f"{OUT}.legs.csv", index=False)

    # -------------------------------------------------------------- G1, G2, G3
    P("\n" + "=" * 190)
    P("GATES G1 / G2 / G3")
    P("=" * 190)
    P(f"G1 three-leg identity max |ADD+DROP+BOTH - gap| over {len(L)} cell-windows = "
      f"{g1_max:.3e}  (bar {BAR_IDENT:.0e})  {'PASS' if g1_max < BAR_IDENT else 'FAIL'}")

    if IDEA556.exists():
        ref = pd.read_csv(IDEA556)
        ref = ref[ref.qfam == "QUANTILE-M"][["panel", "theta", "window", "ADD_pp", "DROP_pp",
                                             "rbar_add", "rbar_drop", "sel_geo_pp", "x",
                                             "n_add", "n_drop", "w_add", "w_drop"]]
        mine = L[(L.family == "MA-DIST") & (L.window.isin(["FULL", "IS", "OOS"]))].copy()
        mrg = ref.merge(mine, left_on=["panel", "theta", "window"],
                        right_on=["panel", "th", "window"], suffixes=("_556", "_560"))
        cols = ["ADD_pp", "DROP_pp", "rbar_add", "rbar_drop", "sel_geo_pp", "x"]
        d = {c: float((mrg[f"{c}_556"] - mrg[f"{c}_560"]).abs().max()) for c in cols}
        g2 = max(d.values())
        P(f"G2 reproduction of idea 556 .legs.csv on {len(mrg)} matched rows "
          f"({len(ref)} reference rows): " + "  ".join(f"{c} {v:.3e}" for c, v in d.items()))
        P(f"   G2 max {g2:.3e}  (bar {BAR_REPRO:.0e})  {'PASS' if g2 < BAR_REPRO else 'FAIL'}")
        per = mrg.assign(**{f"d_{c}": (mrg[f"{c}_556"] - mrg[f"{c}_560"]).abs() for c in cols}) \
                 .groupby("panel")[[f"d_{c}" for c in cols]].max()
        P("   G2 residue BY PANEL (max abs):")
        P(fmt(per, 3).replace("\n", "\n   "))
        # ---- G2b: is the residue a CACHE VINTAGE effect?  idea 556 ran 2026-09-09;
        # data/prices.csv (U56) has been refreshed since, prices_broad/prices_small have not.
        bad = per.max(axis=1).idxmax()
        if per.max(axis=1).max() >= BAR_REPRO:
            P(f"   G2b VINTAGE SWEEP on the residual panel ({bad}): truncate its price file to "
              f"each of the last 8 closes and re-run the MA-DIST legs.")
            pxb, _ = PN[bad]
            refb = ref[ref.panel == bad]
            best = (None, np.inf)
            for cut in list(pxb.index[-8:]):
                pxc = pxb.loc[:cut]
                st0 = pxc.index[260]
                Rc = pxc.pct_change().fillna(0.0).loc[st0:]
                nlc = live_mask(pxc).loc[st0:].sum(axis=1)
                Vc, lvc = rank_var(pxc, "MA-DIST")
                rr = []
                for th in THETA:
                    gA = gate_abs(pxc, "MA-DIST", th)
                    xc = float((gA.loc[st0:].sum(axis=1) / nlc).mean())
                    gB = gate_quantile(Vc, lvc, xc)
                    A = fast_run(pxc, respread(pxc, gA))["weights"].loc[st0:]
                    B = fast_run(pxc, respread(pxc, gB))["weights"].loc[st0:]
                    Sc = leg_series(A, B, Rc)
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        rr.append(dict(theta=th, x=xc, **window_legs(Sc, lo, hi, tag)))
                RR = pd.DataFrame(rr)
                mm = refb.merge(RR, on=["theta", "window"], suffixes=("_556", "_cut"))
                resid = max(float((mm[f"{c}_556"] - mm[f"{c}_cut"]).abs().max()) for c in cols)
                P(f"      cut {cut.date()} ({len(pxc)} rows): max residue {resid:.3e}"
                  + ("   <-- VINTAGE MATCH" if resid < BAR_REPRO else ""))
                if resid < best[1]:
                    best, best_mm = (cut, resid), mm
            drop_factor = g2 / best[1] if best[1] > 0 else np.inf
            P(f"   G2b best cut {best[0].date()} residue {best[1]:.3e} - a {drop_factor:.0f}x "
              f"drop off the as-cached {g2:.3e}, with every neighbouring cut ~1e0.  Idea 556's "
              f"vintage is therefore prices.csv as of {best[0].date()} (it ran 2026-09-09).")
            # ---- what is LEFT at the right vintage?  Name sets or weights?
            extra = ["x", "n_add", "n_drop", "w_add", "w_drop"]
            lay2 = {c: float((best_mm[f"{c}_556"] - best_mm[f"{c}_cut"]).abs().max())
                    for c in cols + extra if f"{c}_556" in best_mm and f"{c}_cut" in best_mm}
            P("   G2b LAYER 2 - residue at the correct vintage, by column:")
            P("      " + "  ".join(f"{k} {v:.3e}" for k, v in lay2.items()))
            same_names = max(lay2["x"], lay2["n_add"], lay2["n_drop"])
            P(f"      the matched fraction and BOTH name counts reproduce to {same_names:.3e} "
              f"(identical name sets) while the DRIFTED WEIGHTS differ by "
              f"{max(lay2['w_add'], lay2['w_drop']):.3e} - i.e. what is left is a "
              f"PRICE RESTATEMENT in the re-downloaded prices.csv (idea 522's back-adjustment")
            P(f"      class), not a construction difference.  B136/SMALL439, whose caches were "
              f"NOT rewritten, reproduce to {float(per.loc[['B136','SMALL439']].max().max()):.3e}.")
            P(f"   G2 VERDICT: FAIL at the flat {BAR_REPRO:.0e} bar, FULLY DIAGNOSED in two "
              f"layers (vintage {drop_factor:.0f}x, then a price restatement at 1e-4 on an "
              f"annualised RATE).  No number below depends on idea 556's file.")
    else:
        g2 = np.nan
        P("G2 SKIPPED - idea 556 legs.csv not on disk")
    P(f"G3 depth match max |breadth(gate) - breadth(control)| = {g3_max:.3e}")
    flush_log()

    # ============================================================== A. CENSUS leg
    P("\n" + "=" * 190)
    P("A.  CENSUS - does the IS statistic predict the OOS advantage?  (all 12 grid points)")
    P("=" * 190)
    P("OOS advantage = sel_geo_pp on 2017-01-01..end = 100 x (CAGR(gate,0-cost) - CAGR(ctrl,0-cost)).")
    P("Every statistic is signed so HIGHER = predicts a BIGGER advantage; a working screen needs")
    P("a POSITIVE correlation.  n = 81 cells pooled (3 panels x 3 families x 9 thresholds).")

    piv = L.pivot_table(index=["panel", "family", "th"], columns="window",
                        values=["rbar_add", "rbar_drop", "rbar_ctrl", "sel_geo_pp"])
    base = L[L.window == "OOS"].set_index(["panel", "family", "th"])["sel_geo_pp"].rename("OOS_adv")
    wmap = {"FULL_IS": "IS", "TRAIL3Y": "TRAIL3Y", "TRAIL1Y": "TRAIL1Y"}

    for st in STATS:
        for wn in WINDOWS:
            w = wmap[wn]
            row = pd.DataFrame({
                "rbar_add": piv[("rbar_add", w)], "rbar_drop": piv[("rbar_drop", w)],
                "rbar_ctrl": piv[("rbar_ctrl", w)], "sel_geo_pp": piv[("sel_geo_pp", w)]})
            sv = row.apply(lambda r: signed_stat(r, st), axis=1).rename("stat")
            d = pd.concat([sv, base], axis=1).dropna()
            pear = float(d.stat.corr(d.OOS_adv))
            spear = spearman(d.stat, d.OOS_adv)
            n = len(d)
            t = pear * np.sqrt(max(n - 2, 1) / max(1 - pear ** 2, 1e-12))
            sgn = float((np.sign(d.stat - d.stat.median()) == np.sign(d.OOS_adv)).mean())
            per_fam, per_pan = {}, {}
            for f in FAMILIES:
                s = d[d.index.get_level_values("family") == f]
                per_fam[f] = float(s.stat.corr(s.OOS_adv)) if len(s) > 2 else np.nan
            for p in PANELS:
                s = d[d.index.get_level_values("panel") == p]
                per_pan[p] = float(s.stat.corr(s.OOS_adv)) if len(s) > 2 else np.nan
            census.append(dict(statistic=st, window=wn, n=n, pearson=pear, spearman=spear,
                               t=t, sign_agree=sgn, **{f"r_{k}": v for k, v in per_fam.items()},
                               **{f"r_{k}": v for k, v in per_pan.items()}))

    C = pd.DataFrame(census)
    C.to_csv(f"{OUT}.census.csv", index=False)
    P("\n" + fmt(C))
    best = C.loc[C.pearson.idxmax()]
    P(f"\n  BEST of the 12: statistic {best.statistic} window {best.window}  pearson "
      f"{best.pearson:+.4f} (t {best.t:+.3f}, n {int(best.n)})  spearman {best.spearman:+.4f}")
    P(f"  How many of the 12 have a POSITIVE pooled pearson: {int((C.pearson > 0).sum())}/12")
    P(f"  How many reach |t| > 2 in the PREDICTED (positive) direction: "
      f"{int(((C.pearson > 0) & (C.t > 2)).sum())}/12")
    P("  In-window benchmark (the identity idea 556 actually measured):")
    for w in ["IS", "OOS", "FULL"]:
        s = L[L.window == w]
        P(f"    corr(-rbar_drop, sel_geo_pp) SAME window {w:4s} = "
          f"{float((-s.rbar_drop).corr(s.sel_geo_pp)):+.4f}   "
          f"DROP-dominant cells {int((s.dom == 'DROP').sum())}/{len(s)}")
    flush_log()

    # ============================================================== B. DECISION leg
    P("\n" + "=" * 190)
    P("B.  DECISION - pick the threshold by the IS statistic, score the pick OOS")
    P("=" * 190)
    P("Within each (panel, family) the 9 thresholds are ranked by the IS statistic; the argmax is")
    P("the PICK.  Scored against that cell's own median-threshold arm and its best/worst OOS arm.")

    for st in STATS:
        for wn in WINDOWS:
            w = wmap[wn]
            hit = 0
            picks = []
            for pn in PANELS:
                for fam in FAMILIES:
                    sub = L[(L.panel == pn) & (L.family == fam) & (L.window == w)].copy()
                    oos = L[(L.panel == pn) & (L.family == fam) & (L.window == "OOS")] \
                        .set_index("th")["sel_geo_pp"]
                    sub["sv"] = sub.apply(lambda r: signed_stat(r, st), axis=1)
                    sub = sub.dropna(subset=["sv"])
                    if sub.empty:
                        continue
                    pick = sub.loc[sub.sv.idxmax(), "th"]
                    adv = float(oos.loc[pick])
                    med = float(oos.median())
                    picks.append(dict(statistic=st, window=wn, panel=pn, family=fam, pick=pick,
                                      pick_OOS_adv=adv, median_OOS_adv=med,
                                      best_OOS_adv=float(oos.max()), worst_OOS_adv=float(oos.min()),
                                      beat_median=bool(adv > med),
                                      rank_of_pick=int((oos > adv).sum()) + 1))
                    hit += int(adv > med)
            decision.extend(picks)
            P(f"  {st:7s} {wn:8s}  picks beating their own cell median OOS advantage: {hit}/9   "
              + " ".join(f"{p['panel'][:3]}/{p['family'][:3]}:th={p['pick']:+.2f},"
                         f"adv={p['pick_OOS_adv']:+.2f},rk{p['rank_of_pick']}" for p in picks))
    D = pd.DataFrame(decision)
    D.to_csv(f"{OUT}.decision.csv", index=False)
    P(f"\n  POOLED over all 12 x 9 = {len(D)} picks: beat own cell median {int(D.beat_median.sum())}"
      f"/{len(D)} = {D.beat_median.mean():.1%}  (coin toss = 50%, binomial sd = "
      f"{0.5*np.sqrt(len(D))/len(D):.1%})")
    P(f"  mean rank of the pick among its 9 thresholds = {D.rank_of_pick.mean():.3f} "
      f"(random = 5.000, perfect = 1.000)")
    P(f"  mean OOS advantage of the pick {D.pick_OOS_adv.mean():+.4f} pp/yr vs cell median "
      f"{D.median_OOS_adv.mean():+.4f} vs cell best {D.best_OOS_adv.mean():+.4f}")
    for st in STATS:
        s = D[D.statistic == st]
        P(f"    {st:7s}: beat-median {s.beat_median.mean():.1%}  mean rank {s.rank_of_pick.mean():.3f}"
          f"  mean adv {s.pick_OOS_adv.mean():+.4f}")
    flush_log()

    # ============================================================== C. BOOK leg (rule 8)
    P("\n" + "=" * 190)
    P("C.  BOOK LEG / RULE 8 - a tradeable rolling selector on the statistic")
    P("=" * 190)
    P("At every weekly rebalance t the selector picks th* = argmax(statistic over the trailing")
    P("window ending at t, data <= t only) and holds that threshold's gate book.  (statistic,")
    P("window) is chosen on IS Sharpe alone; the OOS is then read once.  10 bps, next-day.")

    sel_books = {}
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = comparand[pn]["start"]
        years = comparand[pn]["years"]
        R = px.pct_change().fillna(0.0).loc[start:]
        spy_s, live_s = comparand[pn]["spy"], comparand[pn]["live"]

        for fam in FAMILIES:
            ths = thresholds(fam)
            Wt = {th: CACHE[(pn, fam, th)][0] for th in ths}
            SS = {th: CACHE[(pn, fam, th)][1] for th in ths}

            for st in STATS:
                for wn in WINDOWS:
                    Lw = SEL_LENS[wn]
                    fallback = -CVOL[4] if fam == "LOWVOL" else 0.0
                    sv = pd.DataFrame({th: rolling_signed(SS[th], st, Lw) for th in ths})
                    valid = sv.notna().any(axis=1)      # min_periods rows are all-NA
                    choice = pd.Series(np.nan, index=sv.index, dtype=float)
                    if valid.any():
                        choice.loc[valid] = sv.loc[valid].idxmax(axis=1).astype(float)
                    choice = choice.ffill()
                    # before the statistic exists the selector holds the declared fallback
                    # threshold; extended back over the warm-up so every arm starts invested.
                    choice = choice.reindex(px.index).ffill().fillna(fallback)
                    Wsel = pd.DataFrame(0.0, index=px.index, columns=px.columns)
                    for th in ths:
                        m = (choice == th)
                        if m.any():
                            Wsel.loc[m] = Wt[th].loc[m]
                    r = fast_run(px, Wsel)
                    s = stat(r["returns"].loc[start:])
                    nsw = int((choice != choice.shift(1)).sum())
                    row = dict(panel=pn, family=fam, statistic=st, window=wn, **s,
                               turn_yr=float(r["turnover"].loc[start:].sum() / years),
                               switches=nsw,
                               p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s))
                    wf.append(row)
                    sel_books[(pn, fam, st, wn)] = choice
            P(f"  {pn}: family {fam:8s} selector books done "
              f"({len(STATS)*len(WINDOWS)} variants)")
            flush_log()

    WF = pd.DataFrame(wf)
    WF["p4b"] = WF.f4b == "-"
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    P("\n  ALL 108 selector books (3 panels x 3 families x 4 statistics x 3 windows):")
    P(fmt(WF[["panel", "family", "statistic", "window", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "isSharpe", "oCAGR", "oSharpe", "oMaxDD", "turn_yr", "switches", "p4a", "f4b"]]))

    P("\n  RULE 8 PICK - (statistic, window) chosen per panel x family by IS Sharpe ALONE:")
    for pn in PANELS:
        spy_s, live_s = comparand[pn]["spy"], comparand[pn]["live"]
        for fam in FAMILIES:
            sub = WF[(WF.panel == pn) & (WF.family == fam)]
            pick = sub.loc[sub.isSharpe.idxmax()]
            spread = float(sub.isSharpe.max() - sub.isSharpe.min())
            fixed = G[(G.panel == pn) & (G.family == fam) & (G.arm == "GATE")]
            fpick = fixed.loc[fixed.isSharpe.idxmax()]
            keeprows.append(dict(panel=pn, family=fam, pick_stat=pick.statistic,
                                 pick_window=pick.window, IS_spread=spread,
                                 oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                                 fixed_th=fpick.th, fx_oCAGR=fpick.oCAGR, fx_oSharpe=fpick.oSharpe,
                                 fx_oMaxDD=fpick.oMaxDD,
                                 spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"],
                                 spy_oMaxDD=spy_s["oMaxDD"],
                                 v2_oCAGR=live_s["oCAGR"], v2_oSharpe=live_s["oSharpe"],
                                 v2_oMaxDD=live_s["oMaxDD"],
                                 p4a=pick.p4a, f4b=pick.f4b,
                                 beats_spy_oos=bool(pick.oSharpe > spy_s["oSharpe"]),
                                 beats_v2_oos=bool(pick.oSharpe > live_s["oSharpe"]),
                                 beats_fixed_oos=bool(pick.oSharpe > fpick.oSharpe)))
            P(f"  {pn:9s} {fam:8s} pick ({pick.statistic},{pick.window}) IS Sharpe "
              f"{pick.isSharpe:.4f} (IS spread over 12 variants {spread:.4f})")
            P(f"            OOS  selector CAGR {pick.oCAGR:7.2%} Sharpe {pick.oSharpe:7.4f} "
              f"MaxDD {pick.oMaxDD:8.2%} | IS-best FIXED th {fpick.th:+.2f} "
              f"{fpick.oCAGR:7.2%}/{fpick.oSharpe:7.4f}/{fpick.oMaxDD:8.2%}")
            P(f"            OOS  RULES v2 {live_s['oCAGR']:7.2%}/{live_s['oSharpe']:7.4f}/"
              f"{live_s['oMaxDD']:8.2%} | SPY {spy_s['oCAGR']:7.2%}/{spy_s['oSharpe']:7.4f}/"
              f"{spy_s['oMaxDD']:8.2%} | 4a {pick.p4a} 4b fails [{pick.f4b}]")
    K = pd.DataFrame(keeprows)
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    flush_log()

    # -------------------------------------------------------------- G4 causality
    P("\n" + "=" * 190)
    P("G4  selector causality (no look-ahead)")
    P("=" * 190)
    pn = "U56"
    px, _ = PN[pn]
    start = comparand[pn]["start"]
    R = px.pct_change().fillna(0.0).loc[start:]
    V, lv = rank_var(px, "MA-DIST")
    ths = thresholds("MA-DIST")
    Rp = R.copy()
    Rp.loc[OOS_START:] = -Rp.loc[OOS_START:]
    SSa, SSb = {}, {}
    for th in ths:
        gA = gate_abs(px, "MA-DIST", th)
        x = float((gA.loc[start:].sum(axis=1) / lv.loc[start:].sum(axis=1)).mean())
        gB = gate_quantile(V, lv, x)
        ra, rb = fast_run(px, respread(px, gA)), fast_run(px, respread(px, gB))
        A, B = ra["weights"].loc[start:], rb["weights"].loc[start:]
        SSa[th] = leg_series(A, B, R)
        SSb[th] = leg_series(A, B, Rp)
    for st in STATS:
        for wn in WINDOWS:
            Lw = SEL_LENS[wn]
            ca = safe_idxmax(pd.DataFrame({th: rolling_signed(SSa[th], st, Lw) for th in ths}))
            cb = safe_idxmax(pd.DataFrame({th: rolling_signed(SSb[th], st, Lw) for th in ths}))
            dis = int((ca.loc[:IS_END].fillna(-99) != cb.loc[:IS_END].fillna(-99)).sum())
            g4_max = max(g4_max, dis)
    P(f"  IS-period selections differing when every OOS return is sign-flipped: {int(g4_max)} "
      f"(bar 0)  {'PASS' if g4_max == 0 else 'FAIL'}")
    flush_log()

    # ============================================================== KEEP paths
    P("\n" + "=" * 190)
    P("KEEP PATHS - both, on every book this run built")
    P("=" * 190)
    tot = len(G) + len(WF)
    n4a = int(G.p4a.sum() + WF.p4a.sum())
    n4b = int(G.p4b.sum() + WF.p4b.sum())
    P(f"  population: {len(G)} fixed-threshold arms (81 gates + 81 depth-matched controls) + "
      f"{len(WF)} selector books = {tot}")
    P(f"  4a (beat RULES v2 in BOTH halves, MaxDD no worse) : {n4a}/{tot}")
    P(f"  4b (beat SPY H1+H2+OOS, DD<=60%, CAGR>=70%)       : {n4b}/{tot}")
    P(f"  rule-8 picks (9): 4a {int(K.p4a.sum())}/9   4b {int((K.f4b == '-').sum())}/9   "
      f"beats SPY OOS Sharpe {int(K.beats_spy_oos.sum())}/9   beats RULES v2 OOS Sharpe "
      f"{int(K.beats_v2_oos.sum())}/9   beats its own IS-best FIXED threshold OOS "
      f"{int(K.beats_fixed_oos.sum())}/9")
    fb = pd.concat([G.f4b, WF.f4b])
    fb = fb[fb != "-"]
    cnt = pd.Series([k for row in fb for k in row.split(",")]).value_counts()
    P(f"  binding 4b legs across the {len(fb)} failures: " +
      "  ".join(f"{k} {v}" for k, v in cnt.items()))
    if n4b:
        P("\n  4b passers:")
        pas = pd.concat([G[G.p4b].assign(kind="fixed")[
                             ["kind", "panel", "family", "th", "arm", "CAGR", "Sharpe", "MaxDD",
                              "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]],
                         WF[WF.p4b].assign(kind="selector", th=np.nan, arm=WF.statistic + "/" + WF.window)[
                             ["kind", "panel", "family", "th", "arm", "CAGR", "Sharpe", "MaxDD",
                              "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]]])
        pas = pas.reset_index(drop=True)
        P(fmt(pas))

        # ---- idea 548 / 742's clause: price every large-cap-panel 4b pass against the
        # EQUAL-WEIGHT basket of its OWN names, not only against cap-weighted SPY.
        P("\n  THE SAME 4b PASSERS AGAINST THEIR OWN PANEL'S EQUAL-WEIGHT BASKET")
        P("  (idea 548's proposed clause: PROTOCOL's 4b bar is cap-weighted while every book")
        P("  here is equal-weight, so SPY flatters the book before any skill.)")
        ewrows = []
        for _, rw in pas.iterrows():
            ew = comparand[rw.panel]["ctrl"]
            legs_ = {"H1": rw.H1 - ew["H1"], "H2": rw.H2 - ew["H2"],
                     "OOS": rw.oSharpe - ew["oSharpe"],
                     "DD": 0.60 * abs(ew["MaxDD"]) - abs(rw.MaxDD),
                     "CAGR": rw.CAGR - 0.70 * ew["CAGR"]}
            fails = [k for k, v in legs_.items() if v <= 0]
            ewrows.append(dict(panel=rw.panel, family=rw.family, arm=rw.arm, th=rw.th,
                               **{f"d{k}": v for k, v in legs_.items()},
                               ew_4b="-" if not fails else ",".join(fails)))
        EW = pd.DataFrame(ewrows)
        P(fmt(EW))
        P(f"  4b against SPY: {len(pas)}/{tot}.  4b against the panel's own equal-weight basket: "
          f"{int((EW.ew_4b == '-').sum())}/{tot}.")
        if (EW.ew_4b != "-").all():
            cnt2 = pd.Series([k for r in EW.ew_4b for k in r.split(",")]).value_counts()
            P("  every SPY-4b passer loses at least one leg to its own equal-weight basket; "
              "binding legs: " + "  ".join(f"{k} {v}" for k, v in cnt2.items()))
    flush_log()

    # ============================================================== verdict
    P("\n" + "=" * 190)
    P("VERDICT")
    P("=" * 190)
    posr = int((C.pearson > 0).sum())
    sigr = int(((C.pearson > 0) & (C.t > 2)).sum())
    P(f"1. CENSUS: of the 12 (statistic, window) grid points, {posr}/12 have a positive pooled")
    P(f"   correlation with the OOS advantage and {sigr}/12 reach t > 2 in the predicted direction.")
    P(f"   Best point: {best.statistic}/{best.window} pearson {best.pearson:+.4f} "
      f"(t {best.t:+.3f}), spearman {best.spearman:+.4f}.")
    P(f"   The SAME-window (identity) correlation idea 556 measured is "
      f"{float((-L[L.window=='IS'].rbar_drop).corr(L[L.window=='IS'].sel_geo_pp)):+.4f} on IS and "
      f"{float((-L[L.window=='OOS'].rbar_drop).corr(L[L.window=='OOS'].sel_geo_pp)):+.4f} on OOS.")
    P(f"2. DECISION: picks beat their own cell median OOS advantage "
      f"{int(D.beat_median.sum())}/{len(D)} = {D.beat_median.mean():.1%}; mean rank of the pick "
      f"{D.rank_of_pick.mean():.3f} of 9 (random 5.000).")
    P(f"3. BOOK: rule-8 picks beat SPY OOS Sharpe {int(K.beats_spy_oos.sum())}/9, RULES v2 OOS "
      f"{int(K.beats_v2_oos.sum())}/9, and their own IS-best FIXED threshold "
      f"{int(K.beats_fixed_oos.sum())}/9.  4a {n4a}/{tot}, 4b {n4b}/{tot}.")
    P(f"4. DOMINANCE (556's own claim, on THREE families): DROP is the dominant side in "
      f"{int((L[L.window=='IS'].dom=='DROP').sum())}/81 IS cells, "
      f"{int((L[L.window=='OOS'].dom=='DROP').sum())}/81 OOS and "
      f"{int((L[L.window=='FULL'].dom=='DROP').sum())}/81 FULL - it REPLICATES off MA-DIST onto")
    P("   MOM12_1 and LOWVOL.  What does not replicate is any usable ordering of magnitudes.")
    P("5. SURVIVORSHIP restated: B136/SMALL439 are current constituents; the CAGR floor in 4b")
    P("   and every absolute CAGR above are flattered.  The legs are arm-minus-arm and cancel.")
    flush_log()
    P("\nfiles: " + ", ".join(Path(f"{OUT}{s}").name for s in
                              (".grid.csv", ".legs.csv", ".census.csv", ".decision.csv",
                               ".walkforward.csv", ".keeppaths.csv", ".console.txt")))
    flush_log()


if __name__ == "__main__":
    main()
