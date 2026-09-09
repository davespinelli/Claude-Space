#!/usr/bin/env python3
"""Idea 550 - "does-the-Q-CADENCE-SIGN-FLIP-replicate-off-SMALL439" (cloud, 2026-09-09).

The question
------------
Idea 307 (lane B, 2026-09-09) ran the cash-drag decomposition on the SMALL439 panel at five
cadences and found ONE exception to its own c_sd ordering.  For the matched pure-exposure
control (QUANTILE-M) the mean timing residual reads

    D  -0.0006   W  -0.0094   M  -0.0390   Q  +0.0114   A  -0.1239   (pp/yr, FULL window)

Q is the only cadence where the residual is POSITIVE, and it is positive at 9 of 9 thetas, even
though its c_sd (0.0097) is not the largest on the dial (A is, at 0.0158).  Every other cadence
is negative in the mean.  A sign that survives 9/9 thetas is not obviously noise, so the queue
asked the only two questions that can separate the candidate explanations:

    (a) PANEL FACT?   Run the identical D/W/M/Q/A design on U56 and B136.  If the positive Q
        residual shows up there too it is a property of the quarterly cadence itself.  If it
        does not, it is a property of the SMALL439 panel and idea 307's headline is a
        one-panel result that must be stamped as such.

    (b) CALENDAR ARTEFACT?  "Quarterly" in this record means the CALENDAR quarter - the last
        trading bar of Mar/Jun/Sep/Dec.  That confounds two different things: a ~63-bar
        HOLDING PERIOD, and a rebalance calendar phase-locked to quarter ends (earnings
        season, index reconstitution, the turn of the tax year).  If the flip is a holding-
        period fact it must survive when the same ~63-bar cadence is run at a different PHASE.
        If it only appears at the calendar phase it is an artefact of the 63-rebalance window.

Nothing here is a trading rule.  This is a restatement test on a published number: the outcome
is a stamp on idea 307's headline, and the KEEP columns are carried only because PROTOCOL
requires every book to be priced.

The design (max 2 tuned dials, both fully reported)
---------------------------------------------------
    PANEL   (dial 1)  U56, B136, SMALL439              - idea 307 had one, the queue asks for three
    CADENCE (dial 2)  D, W, M, Q, A                    - idea 307's dial, verbatim

    PHASE   is NOT a third dial.  It is a reported diagnostic contrast with every point printed:
            a fixed-length 63-bar cadence at offsets {0, 13, 26, 39, 52} plus the calendar-Q
            mask itself.  Nothing is selected on phase; all 6 columns are reported side by side.

    theta, family, construction and window are structural, not tuned: theta is the 9-point MA
    grid idea 298/307 published, x is a deterministic function of theta (the c_bar matching),
    and RESPREAD/DEGROSS is the pair the decomposition is DEFINED on.

The decomposition (idea 298's, verbatim)
----------------------------------------
    RESPREAD  gated names carry the whole gross:  w = GROSS/k_t on gated names
    DEGROSS   gated-out weight goes to cash:      w = GROSS/n_t on gated names
    c_t       = gross(DEGROSS)/gross(RESPREAD), the cash-drag path;  r_DG0 == c_t * r_RS0
    gap0      = CAGR0(DEGROSS) - CAGR0(RESPREAD)              (0 = costs stripped)
    pred0     = CAGR0(c_bar * r_RS0) - CAGR0(r_RS0)           (the level-only prediction)
    resid0    = gap0 - pred0                                  (the TIMING residual, pp/yr)

Rule 8 (walk-forward), required
-------------------------------
    Every decomposition is cut FULL / IS (<= 2016-12-31) / OOS (>= 2017-01-01).  The sign claim
    is CHOSEN on the IS half only - per panel, pick the cadence whose QUANTILE-M mean resid0 is
    most positive in-sample - and the untouched OOS half is then read for that choice.  A sign
    that is an IS artefact will not survive.  Book-level walk-forward is run alongside: choose
    the (family, cadence, theta, construction) book by IS Sharpe on each panel, report its OOS
    CAGR/Sharpe/MaxDD against RULES v2 (live), SPY and the cadence-matched no-gate EWall control.

KEEP paths (PROTOCOL 4), priced for all 540 + 540 books
-------------------------------------------------------
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than the live book
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's

Pre-registered gates (stated BEFORE the run; a FAIL is reported, not repaired)
------------------------------------------------------------------------------
    G1  local engine == engine.backtest at D/W/M/Q on every panel, < 1e-15
    G2  the DEGROSS/RESPREAD identity r_DG0 == c_t * r_RS0 holds, < 1e-12
    G3  idea 307's SMALL439 QUANTILE-M and MA-THRESH decomp reproduces, < 1e-6 pp/yr, 270 cells
    G4  idea 551's 3-panel x 5-cadence decomp reproduces, < 1e-6 pp/yr, 810 cells
    G5  c_bar matching: worst |frac_q - frac_ma| < 0.01 over the 27 (panel x theta) cells
    G6  RULES v2 live book reproduces (0.0866 / 1.2056 / -0.1205), < 5e-4
    G7  the 63-bar phase-0 cadence has the same number of rebalances as calendar-Q +/- 2 per
        panel (otherwise "phase" would be confounded with rebalance COUNT, not phase)

Pre-registered readings of the answer
-------------------------------------
    REPLICATES  : QUANTILE-M mean resid0 at Q > 0 on U56 AND B136 (FULL), and > 0 at a majority
                  of thetas on each.  -> the flip is a cadence fact.
    PANEL FACT  : Q resid0 <= 0 on both other panels.  -> idea 307's headline is SMALL439-only.
    CALENDAR    : on SMALL439 the sign is positive at calendar-Q and negative at a majority of
                  the 5 phase offsets.  -> artefact of the 63-rebalance window.
    HOLDING PER.: positive at calendar-Q and at a majority of phases.  -> a 63-bar fact.

Survivorship caveat: SMALL439 is the CURRENT constituents of a sub-$2B screen (data/
SMALL_PANEL_README.md); B136 is current large-cap constituents.  Both are survivorship-biased
upward in LEVEL.  resid0 is a difference of two books on the SAME names, so the bias very
largely cancels out of it; it does NOT cancel out of the CAGR/Sharpe/MaxDD or KEEP columns,
which are therefore optimistic and are reported for completeness only.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest as engine_backtest, rebalance_mask as engine_mask, metrics

COST_BPS = 10
GROSS = 0.75
CADENCES = ["D", "W", "M", "Q", "A"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
PHASES = [0, 13, 26, 39, 52]                 # trading-bar offsets inside a 63-bar block
QBARS = 63
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

BAR_ENGINE = 1e-15
BAR_IDENT = 1e-12
BAR_REPRO = 1e-6
BAR_MASK_TOL = 0.01
LIVE_PUB = (0.0866, 1.2056, -0.1205)
BAR_LIVE = 5e-4
BAR_NREB = 2

PRIOR307 = REPO / "research" / "backtests" / \
    "2026-09-09_does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence_B.decomp.csv"
PRIOR551 = REPO / "research" / "backtests" / \
    "2026-09-09_restate-idea-298s-MA-RESIDUAL-BAND-with-its-cadence-domain_C.decomp.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ cadence masks
def cad_mask(idx, cad):
    """True on the last trading bar of each cadence block.  Identical to engine.rebalance_mask
    for D/W/M/Q; adds A (calendar year).  Same function as idea 307/551."""
    if cad == "D":
        return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"),
           "Q": idx.to_period("Q"), "A": idx.to_period("Y")}[cad]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)


def bar_mask(idx, nbars=QBARS, phase=0):
    """True every `nbars` TRADING bars, offset by `phase`.  Fixed-length cadence with no
    calendar alignment - the probe that separates a holding-period fact from a calendar one."""
    pos = np.arange(len(idx))
    return pd.Series(((pos - phase) % nbars) == 0, index=idx)


def bt(prices, weights, cost_bps=COST_BPS, mask=None):
    """engine.backtest's loop with the rebalance mask passed in explicitly."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mv = mask.shift(1, fill_value=False).values
    cur = np.zeros(len(prices.columns))
    wv, rv = w_target.values, rets.values
    hv = np.zeros_like(wv)
    tv = np.zeros(len(prices.index))
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
            new = wv[i]
            tv[i] = np.abs(new - cur).sum()
            cur = new
        hv[i] = cur
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    held = pd.DataFrame(hv, index=prices.index, columns=prices.columns)
    turnover = pd.Series(tv, index=prices.index)
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "weights": held, "turnover": turnover}


# ------------------------------------------------------------------ panels / gates / books
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
    P(f"panels: U56 {out['U56'][0].shape[1]} names, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} ({len(bad)} dropped for max_1d_move >= 1.0)")
    for nm, (p, _) in out.items():
        P(f"  {nm}: {p.index[0].date()} .. {p.index[-1].date()}  ({len(p)} days)")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    live = live_mask(px)
    dist = (px / px.rolling(200).mean() - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, g, construction):
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


def decompose(rs_r0, dg_r0, c_t, lo, hi, tag):
    sl = slice(lo, hi)
    rr, rd = rs_r0.loc[sl], dg_r0.loc[sl]
    cb = float(c_t.loc[sl].mean())
    g0 = 100 * (cagr(rd) - cagr(rr))
    p0 = 100 * (cagr(cb * rr) - cagr(rr))
    return dict(window=tag, c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd))


# ------------------------------------------------------------------ main
def main():
    P("=" * 178)
    P("IDEA 550 - does-the-Q-CADENCE-SIGN-FLIP-replicate-off-SMALL439   (cloud, 2026-09-09)")
    P("=" * 178)
    P("PREMISE (idea 307, SMALL439, QUANTILE-M, FULL): mean resid0 D -0.0006  W -0.0094  "
      "M -0.0390  Q +0.0114  A -0.1239 pp/yr; Q positive at 9/9 thetas, c_sd 0.0097.")
    P("ASKS  (a) does Q > 0 replicate on U56 and B136?  (b) is it the CALENDAR quarter or a "
      "63-bar holding period?")
    P("DIALS panel (3) x cadence (5).  PHASE is a reported contrast, not a tuned dial.")
    P("")

    PX = panels()
    flush_log()

    # ---------------------------------------------------------- G6 live book
    px_u = load_universe()
    live_full = engine_backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                                freq="W")["returns"]
    lv = metrics(live_full.loc[px_u.index[260]:])
    ok_g6 = (abs(lv["CAGR"] - LIVE_PUB[0]) < BAR_LIVE and abs(lv["Sharpe"] - LIVE_PUB[1]) < BAR_LIVE
             and abs(lv["MaxDD"] - LIVE_PUB[2]) < BAR_LIVE)

    P("\n" + "=" * 178)
    P("PRE-REGISTERED GATES")
    P("=" * 178)

    # ---------------------------------------------------------- G1 engine equivalence
    g1rows, worst_g1, worst_mask = [], 0.0, 0
    for pname in PANELS:
        px = PX[pname][0]
        w = control_book(px)
        for cad in ["D", "W", "M", "Q"]:
            mine = bt(px, w, mask=cad_mask(px.index, cad))["returns"]
            ref = engine_backtest(px, w, cost_bps=COST_BPS, freq=cad)["returns"]
            d = float((mine - ref).abs().max())
            md = int((cad_mask(px.index, cad) != engine_mask(px.index, cad)).sum())
            worst_g1, worst_mask = max(worst_g1, d), max(worst_mask, md)
            g1rows.append(dict(panel=pname, cad=cad, max_abs_dret=d, mask_diff_bars=md))
    ok_g1 = worst_g1 < BAR_ENGINE and worst_mask == 0
    P(f"G1 {'PASS' if ok_g1 else 'FAIL'}  local engine vs engine.backtest: worst |dret| = "
      f"{worst_g1:.3e} (bar {BAR_ENGINE:.0e}), worst mask bar diff = {worst_mask}")
    pd.DataFrame(g1rows).to_csv(f"{OUT}.enginegate.csv", index=False)

    # ---------------------------------------------------------- G5 matching
    gates, match = {}, []
    for pname in PANELS:
        px = PX[pname][0]
        start = px.index[260]
        gates[pname] = {}
        for th in MA_THETA:
            gma = ma_gate(px, th)
            live = live_mask(px)
            frac_ma = float((gma.sum(axis=1) / live.sum(axis=1).clip(lower=1)).loc[start:].mean())
            gq = quantile_gate(px, frac_ma)
            frac_q = float((gq.sum(axis=1) / live.sum(axis=1).clip(lower=1)).loc[start:].mean())
            gates[pname][th] = {"MA-THRESH": gma, "QUANTILE-M": gq}
            match.append(dict(panel=pname, theta=th, x=frac_ma, frac_ma=frac_ma, frac_q=frac_q,
                              d_frac=frac_q - frac_ma))
    M = pd.DataFrame(match)
    M.to_csv(f"{OUT}.match.csv", index=False)
    ok_g5 = bool(M.d_frac.abs().max() < BAR_MASK_TOL)
    P(f"G5 {'PASS' if ok_g5 else 'FAIL'}  c_bar matching: worst |frac_q - frac_ma| = "
      f"{M.d_frac.abs().max():.5f} at {BAR_MASK_TOL} over {len(M)} (panel x theta) cells")

    # ---------------------------------------------------------- G7 rebalance counts
    g7rows, worst_g7 = [], 0
    for pname in PANELS:
        px = PX[pname][0]
        start = px.index[260]
        nq = int(cad_mask(px.index, "Q").loc[start:].sum())
        for ph in PHASES:
            nb = int(bar_mask(px.index, QBARS, ph).loc[start:].sum())
            worst_g7 = max(worst_g7, abs(nb - nq))
            g7rows.append(dict(panel=pname, phase=ph, n_calendarQ=nq, n_63bar=nb, d=nb - nq))
    ok_g7 = worst_g7 <= BAR_NREB
    pd.DataFrame(g7rows).to_csv(f"{OUT}.rebcount.csv", index=False)
    P(f"G7 {'PASS' if ok_g7 else 'FAIL'}  63-bar vs calendar-Q rebalance count: worst |d| = "
      f"{worst_g7} (bar {BAR_NREB}) over {len(g7rows)} (panel x phase) cells")
    P(f"G6 {'PASS' if ok_g6 else 'FAIL'}  RULES v2 live: CAGR {lv['CAGR']:.4f} / Sharpe "
      f"{lv['Sharpe']:.4f} / MaxDD {lv['MaxDD']:.4f} vs published {LIVE_PUB}")
    flush_log()

    # ---------------------------------------------------------- LEG A: the 540-book grid
    P("\n" + "=" * 178)
    P("LEG A - THE 540-BOOK GRID (3 panel x 9 theta x 5 cadence x 2 family x 2 construction)")
    P("=" * 178)
    rows, decomp = [], []
    ident_worst = 0.0
    for pname in PANELS:
        px, spy_px = PX[pname]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.loc[start:])
        ctrl = {}
        for cad in CADENCES:
            rc = bt(px, control_book(px), mask=cad_mask(px.index, cad))["returns"].loc[start:]
            ctrl[cad] = stat(rc)
        P(f"\nPANEL {pname}: from {start.date()} ({years:.2f} yrs) | "
          f"SPY {spy_s['CAGR']:.2%}/{spy_s['Sharpe']:.4f}/{spy_s['MaxDD']:.2%} | "
          f"LIVE v2 {live_s['CAGR']:.2%}/{live_s['Sharpe']:.4f}/{live_s['MaxDD']:.2%} | "
          f"EWall-W {ctrl['W']['CAGR']:.2%}/{ctrl['W']['Sharpe']:.4f}/{ctrl['W']['MaxDD']:.2%}")
        flush_log()
        for th in MA_THETA:
            for cad in CADENCES:
                for fam in FAMILIES:
                    g = gates[pname][th][fam]
                    arms = {}
                    for con in CONSTRUCTIONS:
                        res = bt(px, book(px, g, con), mask=cad_mask(px.index, cad))
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        arms[con] = dict(r0=r0, gross=grs, s=s)
                        rows.append(dict(panel=pname, theta=th,
                                         x=float(M[(M.panel == pname) & (M.theta == th)].x.iloc[0]),
                                         cad=cad, phase="calendar", family=fam, con=con, **s,
                                         CAGR0=cagr(r0), gross_mean=float(grs.mean()),
                                         turn_yr=float(turn.sum() / years),
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    ident_worst = max(ident_worst, ident)
                    base = dict(panel=pname, theta=th, cad=cad, phase="calendar", family=fam,
                                ident_max_err=ident)
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        decomp.append({**base, **decompose(rs["r0"], dg["r0"], c_t, lo, hi, tag)})
        P(f"  {pname} done ({len(rows)} book rows so far)")
        flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    ok_g2 = ident_worst < BAR_IDENT
    P(f"\nG2 {'PASS' if ok_g2 else 'FAIL'}  DEGROSS identity r_DG0 == c_t*r_RS0: worst "
      f"|d| = {ident_worst:.3e} (bar {BAR_IDENT:.0e}) over {len(D)//3} cells")

    # ---------------------------------------------------------- G3 / G4 reproduction
    p307 = pd.read_csv(PRIOR307)
    j3 = p307[["theta", "cad", "family", "window", "resid0_pp", "c_sd"]].merge(
        D[D.panel == "SMALL439"][["theta", "cad", "family", "window", "resid0_pp", "c_sd"]],
        on=["theta", "cad", "family", "window"], suffixes=("_307", "_me"))
    d3 = (j3.resid0_pp_307 - j3.resid0_pp_me).abs()
    ok_g3 = len(j3) == 270 and bool(d3.max() < BAR_REPRO)
    P(f"G3 {'PASS' if ok_g3 else 'FAIL'}  idea 307 SMALL439 decomp: matched {len(j3)}/270 cells, "
      f"worst |d resid0| = {d3.max():.3e} pp/yr, worst |d c_sd| = "
      f"{(j3.c_sd_307 - j3.c_sd_me).abs().max():.3e}")

    p551 = pd.read_csv(PRIOR551)
    j4 = p551[["panel", "theta", "cad", "family", "window", "resid0_pp"]].merge(
        D[["panel", "theta", "cad", "family", "window", "resid0_pp"]],
        on=["panel", "theta", "cad", "family", "window"], suffixes=("_551", "_me"))
    d4 = (j4.resid0_pp_551 - j4.resid0_pp_me).abs()
    ok_g4 = len(j4) == 810 and bool(d4.max() < BAR_REPRO)
    P(f"G4 {'PASS' if ok_g4 else 'FAIL'}  idea 551 3-panel decomp: matched {len(j4)}/810 cells, "
      f"worst |d resid0| = {d4.max():.3e} pp/yr")
    flush_log()

    # ---------------------------------------------------------- THE HEADLINE (a): replication
    P("\n" + "=" * 178)
    P("(a) DOES THE Q SIGN FLIP REPLICATE?  QUANTILE-M mean resid0 (pp/yr) by PANEL x CADENCE, "
      "all 3 windows, ALL grid points")
    P("=" * 178)
    head = []
    for fam in FAMILIES:
        for pname in PANELS:
            for cad in CADENCES:
                for win in ["FULL", "IS", "OOS"]:
                    v = D[(D.family == fam) & (D.panel == pname) & (D.cad == cad) &
                          (D.window == win)]
                    head.append(dict(family=fam, panel=pname, cad=cad, window=win,
                                     mean_resid0=v.resid0_pp.mean(), sd_resid0=v.resid0_pp.std(),
                                     min_resid0=v.resid0_pp.min(), max_resid0=v.resid0_pp.max(),
                                     n_pos=int((v.resid0_pp > 0).sum()), n=len(v),
                                     mean_c_bar=v.c_bar.mean(), mean_c_sd=v.c_sd.mean(),
                                     mean_gap0=v.gap0_pp.mean(), mean_pred0=v.pred0_pp.mean()))
    H = pd.DataFrame(head)
    H.to_csv(f"{OUT}.headline.csv", index=False)
    for fam in FAMILIES:
        P(f"\n--- {fam} ---")
        P(fmt(H[H.family == fam].set_index(["panel", "cad", "window"])
              [["mean_resid0", "sd_resid0", "min_resid0", "max_resid0", "n_pos", "n",
                "mean_c_bar", "mean_c_sd"]]))

    P("\nREPLICATION READING (QUANTILE-M, cadence Q):")
    rep = {}
    for pname in PANELS:
        r = H[(H.family == "QUANTILE-M") & (H.panel == pname) & (H.cad == "Q")]
        f_ = r[r.window == "FULL"].iloc[0]
        i_ = r[r.window == "IS"].iloc[0]
        o_ = r[r.window == "OOS"].iloc[0]
        rep[pname] = dict(full=f_.mean_resid0, npos=int(f_.n_pos), is_=i_.mean_resid0,
                          isnpos=int(i_.n_pos), oos=o_.mean_resid0, oosnpos=int(o_.n_pos))
        P(f"  {pname:9s} FULL {f_.mean_resid0:+.4f} ({int(f_.n_pos)}/9 pos)   "
          f"IS {i_.mean_resid0:+.4f} ({int(i_.n_pos)}/9)   OOS {o_.mean_resid0:+.4f} "
          f"({int(o_.n_pos)}/9)")
    replicates = (rep["U56"]["full"] > 0 and rep["B136"]["full"] > 0 and
                  rep["U56"]["npos"] >= 5 and rep["B136"]["npos"] >= 5)
    rep_read = ("REPLICATES off SMALL439" if replicates
                else "DOES NOT REPLICATE - it is a SMALL439 PANEL FACT")
    P(f"  => Q sign flip {rep_read}")
    flush_log()

    # ---------------------------------------------------------- LEG B: phase probe
    P("\n" + "=" * 178)
    P("(b) CALENDAR ARTEFACT OR 63-BAR HOLDING PERIOD?  Same decomposition at a fixed 63-bar "
      "cadence, 5 phases (540 extra books)")
    P("=" * 178)
    prows, pdecomp = [], []
    for pname in PANELS:
        px, spy_px = PX[pname]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.loc[start:])
        for ph in PHASES:
            msk = bar_mask(px.index, QBARS, ph)
            ctrl_s = stat(bt(px, control_book(px), mask=msk)["returns"].loc[start:])
            for th in MA_THETA:
                for fam in FAMILIES:
                    g = gates[pname][th][fam]
                    arms = {}
                    for con in CONSTRUCTIONS:
                        res = bt(px, book(px, g, con), mask=msk)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        arms[con] = dict(r0=r0, gross=grs, s=s)
                        prows.append(dict(panel=pname, theta=th, cad="63BAR", phase=ph,
                                          family=fam, con=con, **s, CAGR0=cagr(r0),
                                          gross_mean=float(grs.mean()),
                                          turn_yr=float(turn.sum() / years),
                                          dSharpe_ctrl=s["Sharpe"] - ctrl_s["Sharpe"],
                                          p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    ident_worst = max(ident_worst, ident)
                    base = dict(panel=pname, theta=th, cad="63BAR", phase=ph, family=fam,
                                ident_max_err=ident)
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        pdecomp.append({**base,
                                        **decompose(rs["r0"], dg["r0"], c_t, lo, hi, tag)})
        P(f"  {pname} phase probe done ({len(prows)} rows so far)")
        flush_log()

    GP = pd.DataFrame(prows)
    DP = pd.DataFrame(pdecomp)
    ALLG = pd.concat([G, GP], ignore_index=True)
    ALLD = pd.concat([D, DP], ignore_index=True)
    ALLG.to_csv(f"{OUT}.grid.csv", index=False)
    ALLD.to_csv(f"{OUT}.decomp.csv", index=False)

    ph_rows = []
    for fam in FAMILIES:
        for pname in PANELS:
            cal = D[(D.family == fam) & (D.panel == pname) & (D.cad == "Q")]
            for win in ["FULL", "IS", "OOS"]:
                c = cal[cal.window == win]
                ph_rows.append(dict(family=fam, panel=pname, window=win, phase="calendarQ",
                                    mean_resid0=c.resid0_pp.mean(), n_pos=int((c.resid0_pp > 0).sum()),
                                    mean_c_sd=c.c_sd.mean()))
                for ph in PHASES:
                    v = DP[(DP.family == fam) & (DP.panel == pname) & (DP.phase == ph) &
                           (DP.window == win)]
                    ph_rows.append(dict(family=fam, panel=pname, window=win, phase=f"63bar+{ph}",
                                        mean_resid0=v.resid0_pp.mean(),
                                        n_pos=int((v.resid0_pp > 0).sum()),
                                        mean_c_sd=v.c_sd.mean()))
    PH = pd.DataFrame(ph_rows)
    PH.to_csv(f"{OUT}.phase.csv", index=False)
    for fam in FAMILIES:
        P(f"\n--- {fam}: mean resid0 (pp/yr) and n_pos/9, calendar-Q vs 63-bar phases ---")
        piv = PH[PH.family == fam].pivot_table(index=["panel", "window"], columns="phase",
                                               values="mean_resid0")
        npv = PH[PH.family == fam].pivot_table(index=["panel", "window"], columns="phase",
                                               values="n_pos")
        P("mean resid0:")
        P(fmt(piv))
        P("n_pos out of 9:")
        P(npv.to_string())

    P("\nCALENDAR READING (QUANTILE-M, FULL window):")
    for pname in PANELS:
        sub = PH[(PH.family == "QUANTILE-M") & (PH.panel == pname) & (PH.window == "FULL")]
        cal = float(sub[sub.phase == "calendarQ"].mean_resid0.iloc[0])
        phv = sub[sub.phase != "calendarQ"].mean_resid0.values
        npos_ph = int((phv > 0).sum())
        P(f"  {pname:9s} calendar-Q {cal:+.4f} | 63-bar phases "
          f"{' '.join(f'{v:+.4f}' for v in phv)} | phases positive {npos_ph}/5")
    s_sub = PH[(PH.family == "QUANTILE-M") & (PH.panel == "SMALL439") & (PH.window == "FULL")]
    s_cal = float(s_sub[s_sub.phase == "calendarQ"].mean_resid0.iloc[0])
    s_ph = s_sub[s_sub.phase != "calendarQ"].mean_resid0.values
    if s_cal > 0 and (s_ph > 0).sum() >= 3:
        cal_read = "HOLDING-PERIOD FACT (positive at calendar-Q and at a majority of phases)"
    elif s_cal > 0:
        cal_read = "CALENDAR ARTEFACT of the 63-rebalance window (positive only at calendar phase)"
    else:
        cal_read = "no positive sign to explain on SMALL439 at this cadence"
    P(f"  => SMALL439 reading: {cal_read}")
    flush_log()

    # ---------------------------------------------------------- RULE 8 walk-forward
    P("\n" + "=" * 178)
    P("RULE 8 WALK-FORWARD - the SIGN claim chosen on IS only, read on the untouched OOS half")
    P("=" * 178)
    wf = []
    for fam in FAMILIES:
        for pname in PANELS:
            sub = H[(H.family == fam) & (H.panel == pname)]
            isr = sub[sub.window == "IS"].sort_values("mean_resid0", ascending=False)
            pick = isr.iloc[0]
            oos = sub[(sub.window == "OOS") & (sub.cad == pick.cad)].iloc[0]
            full = sub[(sub.window == "FULL") & (sub.cad == pick.cad)].iloc[0]
            wf.append(dict(family=fam, panel=pname, pick_cad=pick.cad,
                           IS_resid0=pick.mean_resid0, IS_npos=int(pick.n_pos),
                           OOS_resid0=oos.mean_resid0, OOS_npos=int(oos.n_pos),
                           FULL_resid0=full.mean_resid0,
                           sign_held=bool(pick.mean_resid0 > 0 and oos.mean_resid0 > 0)))
    WF = pd.DataFrame(wf)
    P("Choose per (family, panel) the cadence with the LARGEST IS mean resid0; read OOS:")
    P(fmt(WF.set_index(["family", "panel"])))
    P(f"  sign held IS->OOS in {int(WF.sign_held.sum())} of {len(WF)} (family x panel) cells")

    # book-level walk-forward
    P("\nBOOK-LEVEL WALK-FORWARD - choose the book by IS Sharpe on each panel, read OOS vs "
      "RULES v2 (live), SPY and EWall")
    bwf = []
    for pname in PANELS:
        px, spy_px = PX[pname]
        start = px.index[260]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.loc[start:])
        ctrl_s = stat(bt(px, control_book(px),
                         mask=cad_mask(px.index, "W"))["returns"].loc[start:])
        sub = ALLG[ALLG.panel == pname].sort_values("isSharpe", ascending=False)
        b = sub.iloc[0]
        bwf.append(dict(panel=pname, pick=f"{b.family}/{b.con}/cad={b.cad}/ph={b.phase}/"
                                          f"theta={b.theta}",
                        IS_Sharpe=b.isSharpe, OOS_CAGR=b.oCAGR, OOS_Sharpe=b.oSharpe,
                        OOS_MaxDD=b.oMaxDD, base_OOS_CAGR=live_s["oCAGR"],
                        base_OOS_Sharpe=live_s["oSharpe"], base_OOS_MaxDD=live_s["oMaxDD"],
                        spy_OOS_CAGR=spy_s["oCAGR"], spy_OOS_Sharpe=spy_s["oSharpe"],
                        spy_OOS_MaxDD=spy_s["oMaxDD"], ew_OOS_Sharpe=ctrl_s["oSharpe"],
                        p4a=b.p4a, f4b=b.f4b))
    BWF = pd.DataFrame(bwf)
    P(fmt(BWF.set_index("panel")))
    pd.concat([WF.assign(kind="sign"), BWF.assign(kind="book")], ignore_index=True) \
        .to_csv(f"{OUT}.walkforward.csv", index=False)
    flush_log()

    # ---------------------------------------------------------- KEEP paths
    P("\n" + "=" * 178)
    P("KEEP PATHS (PROTOCOL 4) over all 1080 books")
    P("=" * 178)
    n4a = int(ALLG.p4a.sum())
    n4b = int((ALLG.f4b == "-").sum())
    P(f"4a passers: {n4a} of {len(ALLG)}   4b passers: {n4b} of {len(ALLG)}")
    kp = ALLG.groupby(["panel", "family"]).agg(n=("p4a", "size"), n4a=("p4a", "sum"),
                                               n4b=("f4b", lambda s: int((s == "-").sum())))
    P(fmt(kp))
    fails = ALLG.f4b.str.split(",").explode().value_counts()
    P("\n4b failing legs (count over all books):")
    P(fails.to_string())
    if n4a:
        P("\n4a passers:")
        P(fmt(ALLG[ALLG.p4a][["panel", "family", "con", "cad", "phase", "theta", "CAGR",
                              "Sharpe", "MaxDD", "H1", "H2", "f4b"]]))
    if n4b:
        P("\n4b passers:")
        P(fmt(ALLG[ALLG.f4b == "-"][["panel", "family", "con", "cad", "phase", "theta", "CAGR",
                                     "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "p4a"]]))
    kp.to_csv(f"{OUT}.keeppaths.csv")

    # ---------------------------------------------------------- verdict
    P("\n" + "=" * 178)
    P("VERDICT")
    P("=" * 178)
    gates_ok = all([ok_g1, ok_g2, ok_g3, ok_g4, ok_g5, ok_g6, ok_g7])
    P(f"gates: G1 {ok_g1} G2 {ok_g2} G3 {ok_g3} G4 {ok_g4} G5 {ok_g5} G6 {ok_g6} G7 {ok_g7}")
    P(f"(a) replication: {'REPLICATES' if replicates else 'DOES NOT REPLICATE'} - "
      f"U56 Q {rep['U56']['full']:+.4f} ({rep['U56']['npos']}/9), "
      f"B136 Q {rep['B136']['full']:+.4f} ({rep['B136']['npos']}/9), "
      f"SMALL439 Q {rep['SMALL439']['full']:+.4f} ({rep['SMALL439']['npos']}/9)")
    P(f"(b) calendar: {cal_read}")
    P(f"KEEP: {n4a} books on 4a, {n4b} on 4b of {len(ALLG)} - "
      f"{'no KEEP candidate' if not (n4a or n4b) else 'see tables above'}")
    P("SURVIVORSHIP: SMALL439 and B136 are current constituents; resid0 is a same-names "
      "difference so the bias largely cancels there, but every CAGR/Sharpe/MaxDD/KEEP column "
      "is optimistic.")
    flush_log()


if __name__ == "__main__":
    main()
