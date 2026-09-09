#!/usr/bin/env python3
"""Idea 305 - "does-the-uncompensated-residual-finding-replicate-off-SMALL439" (lane B, 2026-09-09).

The question
------------
Idea 300 ran, on SMALL439 ONLY, the matched experiment that separates a gate's SELECTION from
its EXPOSURE TIMING: hold the ranking fixed (dist = px/ma200 - 1), hold the mean exposure fixed
(x set to the MA arm's own mean mask fraction), and vary only whether the gate's DEPTH moves.
It found the MA threshold's extra 0.38 pp/yr of timing residual buys nothing - dSharpe -0.0092
full, -0.0256 OOS - and that from c_bar 0.5 up, where a real book lives, dSharpe was negative
at EVERY rung (-0.012..-0.047 full, -0.053..-0.076 OOS).

Idea 298 measured the same residual gap on U56 and B136 but never priced it.  So the record's
"the MA gate's extra residual is uncompensated" is a ONE-PANEL claim on the record's most
survivorship-inflated panel.  This run asks whether it replicates where the live book lives.

  QUEUE'S EXACT TEST: does dSharpe stay <= 0 at c_bar >= 0.5 on BOTH U56 and B136?

Pre-registered hypotheses and bars (written before any number was read)
----------------------------------------------------------------------
H_REPLICATES.  The uncompensated-residual finding is a property of MA gates, not of SMALL439.
    BAR (all three clauses, on the DEGROSS pair, 10 bps, restricted to cells with c_bar >= 0.5,
    on BOTH U56 and B136):
      (1) mean dSharpe = Sharpe(MA-THRESH) - Sharpe(QUANTILE-M) <= 0;
      (2) mean OOS dSharpe (2017-2026, after the rule-8 split) <= 0;
      (3) no c_bar rung (theta level) has a mean dSharpe above 0.
H_PANEL_SPECIFIC.  Any clause fails on either panel; idea 300's finding is then a SMALL439
    fact and the record must re-quote it with its panel.
The two are exhaustive and mutually exclusive.  Reported per panel, so a split verdict
(replicates on one, not the other) is reportable as such.

Validity gates, read BEFORE the headline (B_MATCH, per panel)
    (i)   |d mask fraction| < 0.01 and |d realised c_bar| < 0.02 in all 27 cells - i.e. the
          two arms really do spend the same average exposure;
    (ii)  the DEGROSS/RESPREAD identity r_dg,t = c_t * r_rs,t closes to < 1e-12;
    (iii) |mean QUANTILE-M resid0| < 0.05 pp/yr - the constant-depth arm must be the pure
          exposure control idea 298/300 says it is, on THIS panel too.
    The MA arm's resid0 is REPORTED against idea 298's [-0.70,-0.20] pp/yr band but is NOT a
    pass/fail gate here: queue idea 551 has that band under audit for cadence domain, and this
    run's W/M/Q domain is the band's own domain, so it is quoted as an observation.

Reproduction gates (this run must reproduce the record before it extends it)
    R1  SMALL439 is carried as an anchor and must reproduce idea 300's published headline:
        DEGROSS dSharpe -0.0092, OOS -0.0256; RESPREAD dSharpe +0.0476; resid0 MA -0.3817 and
        QUANTILE-M -0.0124 pp/yr; attribution -0.2917 = +1.2436 sel -1.1660 lev -0.3693 tim.
    R2  Idea 306 (2026-09-09, cloud) ran the same pair at gross 0.75 over D/W/M/Q/A with a
        verbatim copy of engine.backtest.  Every (panel, theta, cadence in W/M/Q, construction)
        cell here must match its pairs.csv dSharpe to < 1e-9.  Idea 306's DEGROSS pair means
        over its 45-cell grids (-0.0103 SMALL439, -0.1204 U56, -0.1174 B136) already imply the
        headline's SIGN; what it does not carry is c_bar per cell, the resid0 decomposition, or
        the rung-by-rung reading the queue actually asked for - which is this run.

Design (identical to idea 300 except the panel loop)
    PANELS (a reported contrast, not a dial): U56 (the live panel), B136 (broad), SMALL439
        (idea 300's own panel, as the reproduction anchor).  SPY is a benchmark column only,
        never investable.
    FAMILIES: MA-THRESH (IN where px > ma200*(1+theta); c_bar is an outcome) and QUANTILE-M
        (IN the top ceil(x*n_t) live names by dist, x = the MA arm's OWN mean mask fraction at
        that theta on that panel).  x is a deterministic function of theta, not a third dial.
        QUANTILE-F is a THIRD arm added after the first run failed its own B_MATCH gate on
        U56/B136 (below): identical ranking and identical x, but the marginal name carries the
        FRACTIONAL weight x*n_t - floor(x*n_t), so the mask fraction is exactly x every day
        instead of ceil()-rounded.  It is not a dial and nothing is chosen on it - it exists
        because ceil() rounding is worth 1/n_t of exposure per day, which is 0.23% on
        SMALL439's 439 names but 1.8% on U56's 56, i.e. the same order as the effect under
        test.  The pre-registered verdict is read on QUANTILE-M as written; QUANTILE-F is the
        exact-matched restatement of it.
    CONSTRUCTIONS (both reported): RESPREAD (w = g/k_t, gross pinned) and DEGROSS (w = g/n_t,
        gated weight to cash).  The headline is the DEGROSS pair.
    Tuned parameters (PROTOCOL rule 4: at most two)
        1. strictness theta (9 values, idea 298/300's grid verbatim)
        2. cadence          (3 values: W, M, Q - idea 300's grid verbatim)
    Reported at every one of the 27 cells per panel; selected at none except inside rule 8.
    Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps rung is
    DERIVED exactly (r0 = r10 + turnover*bps/1e4), not re-run, so it is the same book.
    Grid: 3 panels x 9 theta x 3 cadences x 3 families x 2 constructions = 486 books.

Rule 8 walk-forward (required; all directions fixed before any OOS number was read)
    IS = start..2016-12-31 (selection), OOS = 2017-01-01..end (read once).
    WF-A  (theta, cadence) chosen on IS Sharpe inside each panel x family x construction arm;
          OOS CAGR/Sharpe/MaxDD reported against RULES v2 (live), SPY and the cadence-matched
          no-gate EWall control.
    WF-B  per cell pick the family with the higher IS Sharpe (DEGROSS), read OOS once, compare
          against always-MA and always-QUANTILE-M, and report IS->OOS sign agreement.
    WF-C  does the constant-residual discount walk forward on U56/B136?  Fit nothing: OOS MAE
          of the IS-window per-arm mean resid0 against the zero baseline, per panel x family.

Verdicts (both KEEP paths, on every one of the 486 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
        SPY's.

SURVIVORSHIP: SMALL439 (data/prices_small.csv.gz) and B136 (research/universe_broad.json) are
CURRENT constituents - no delistings - so every CAGR LEVEL on those two panels is inflated and
the 4a/4b columns inherit that bias whole.  The headline is an arm-minus-arm contrast on the
SAME names, the SAME ranking and the SAME days, so the bias very largely cancels out of
dCAGR / dSharpe / resid0; it does NOT cancel out of the KEEP columns.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .matched.csv .pairs.csv .bmatch.csv .walkforward.csv .console.txt
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
FAMILIES = ["MA-THRESH", "QUANTILE-M", "QUANTILE-F"]
Q_FAMS = ["QUANTILE-M", "QUANTILE-F"]
PANELS = ["U56", "B136", "SMALL439"]          # SMALL439 last: it is the anchor, not the question
TARGET = ["U56", "B136"]                      # the queue's two panels
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# pre-registered bars
CBAR_FLOOR = 0.50            # "where a real book lives" - the queue's own condition
BAR_MASK_TOL = 0.01
BAR_CBAR_TOL = 0.02
BAR_IDENT = 1e-12
BAR_Q_RESID = 0.05           # pp/yr
BAR_MA_RESID = (-0.70, -0.20)   # idea 298's band - REPORTED, not a gate (see docstring)

# R1: idea 300's published SMALL439 headline (pp/yr where marked)
R1 = dict(dSharpe=-0.0092, dSharpe_oos=-0.0256, dSharpe_rs=+0.0476,
          resid_ma=-0.3817, resid_q=-0.0124,
          dCAGR0=-0.2917, sel=+1.2436, lev=-1.1660, tim=-0.3693)
R1_TOL_S = 0.0015            # Sharpe units
R1_TOL_PP = 0.02             # pp/yr
IDEA306 = REPO / "research" / "backtests" / \
    "2026-09-09_is-the-MA-threshold-edge-a-CONSTANT-GROSS-effect_cloud.pairs.csv"
R2_TOL = 1e-9

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- panels
def panels():
    """{name: (investable px, SPY benchmark series)}.  Same construction as ideas 300/306."""
    out, n_dropped = {}, 0
    u = load_universe()
    out["U56"] = (u.drop(columns=["SPY"]), u["SPY"])
    b = load_universe(broad=True)
    out["B136"] = (b.drop(columns=["SPY"], errors="ignore"), b["SPY"])
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    n_dropped = len(bad)
    out["SMALL439"] = (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])
    return out, n_dropped


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def dist_rank(px):
    live = live_mask(px)
    return (px / px.rolling(200).mean() - 1).where(live), live


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    dist, live = dist_rank(px)
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def quantile_gate_frac(px, x):
    """Same ranking, same x, but the marginal name carries the fractional weight so the mask
    fraction is EXACTLY x every day (no ceil() rounding).  Returns a float mask in [0,1]."""
    dist, live = dist_rank(px)
    n = live.sum(axis=1)
    kf = x * n
    kfl = np.floor(kf)
    rank = dist.rank(axis=1, ascending=False, method="first")
    full = (rank.le(kfl, axis=0).fillna(False) & live).astype(float)
    marg = (rank.eq(kfl + 1, axis=0).fillna(False) & live).astype(float)
    return full + marg.mul(kf - kfl, axis=0)


def book(px, g, construction):
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
    PN, n_dropped = panels()

    P("=" * 175)
    P("Idea 305 does-the-uncompensated-residual-finding-replicate-off-SMALL439 (lane B) | "
      + Path(__file__).name)
    P("=" * 175)
    P("QUESTION: idea 300 priced the MA gate's extra timing residual on SMALL439 only and found "
      "it buys nothing (dSharpe -0.0092,")
    P("          OOS -0.0256; negative at EVERY rung with c_bar >= 0.5).  Does that replicate on "
      "U56 and B136?")
    P(f"PRE-REGISTERED  H_REPLICATES : on BOTH {TARGET}, restricted to cells with c_bar >= "
      f"{CBAR_FLOOR}: (1) mean dSharpe <= 0,")
    P("                               (2) mean OOS dSharpe <= 0, (3) no theta rung's mean "
      "dSharpe above 0.")
    P("                H_PANEL_SPECIFIC : any clause fails on either panel -> idea 300's "
      "finding is a SMALL439 fact.")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), gross "
      f"{GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): theta {MA_THETA} x cadence {CADENCES}.  x is a deterministic function "
      f"of theta (the matching), not a dial.")
    P(f"reported contrasts: panel {PANELS} x family {FAMILIES} x construction {CONSTRUCTIONS} = "
      f"{len(PANELS) * len(MA_THETA) * len(CADENCES) * len(FAMILIES) * len(CONSTRUCTIONS)} books.")
    P("SURVIVORSHIP: SMALL439 and B136 are current constituents only; CAGR LEVELS inflated, "
      "arm-minus-arm contrasts very largely immune, 4a/4b columns are not.")
    for pn in PANELS:
        px, _ = PN[pn]
        P(f"  PANEL {pn:9s}: {px.shape[1]:3d} names, {px.index[0].date()}..{px.index[-1].date()}, "
          f"{len(px)} bars"
          + (f" ({n_dropped} dropped for max_1d_move >= 1.0)" if pn == "SMALL439" else ""))
    flush_log()

    # ------------------------------------------------- the live 4a comparand (RULES v2 on U56)
    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp, pair, matchrows = [], [], [], []
    spy_by_panel, live_by_panel, ctrl_by_panel = {}, {}, {}

    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        spy_by_panel[pn], live_by_panel[pn] = spy_s, live_s

        ctrl, ctrl0 = {}, {}
        for cad in CADENCES:
            rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=cad)
            r10 = rc["returns"].loc[start:]
            ctrl[cad] = stat(r10)
            ctrl0[cad] = cagr(r10 + rc["turnover"].loc[start:] * COST_BPS / 1e4)
        ctrl_by_panel[pn] = ctrl

        P("\n" + "=" * 175)
        P(f"PANEL {pn} - comparands over {start.date()}..{px.index[-1].date()} ({years:.2f} yrs)")
        P("=" * 175)
        P(f"SPY                          : CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} "
          f"OOS {spy_s['oSharpe']:.4f}")
        P(f"RULES v2 (live, 4a comparand): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS {live_s['oSharpe']:.4f}")
        for cad in CADENCES:
            P(f"CONTROL EWall {cad} (no gate)   : CAGR {ctrl[cad]['CAGR']:.4f} Sharpe "
              f"{ctrl[cad]['Sharpe']:.4f} MaxDD {ctrl[cad]['MaxDD']:.4f} | 0 bps CAGR "
              f"{ctrl0[cad]:.4f}")
        P(f"4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} OOS>{spy_s['oSharpe']:.3f} "
          f"MaxDD>=-{0.60 * abs(spy_s['MaxDD']):.1%} CAGR>={0.70 * spy_s['CAGR']:.2%}")

        # ------------------------------------------- the matching (theta -> x), per panel
        live = live_mask(px).loc[start:]
        nlive = live.sum(axis=1)
        gates = {}
        for th in MA_THETA:
            gm = ma_gate(px, th)
            frac_ma = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gq = quantile_gate(px, frac_ma)
            gf = quantile_gate_frac(px, frac_ma)
            frac_q = float((gq.loc[start:].sum(axis=1) / nlive).mean())
            frac_f = float((gf.loc[start:].sum(axis=1) / nlive).mean())
            gates[th] = {"MA-THRESH": gm, "QUANTILE-M": gq, "QUANTILE-F": gf}
            matchrows.append(dict(panel=pn, theta=th, x=frac_ma, frac_ma=frac_ma, frac_q=frac_q,
                                  frac_f=frac_f, d_frac=frac_q - frac_ma,
                                  d_frac_f=frac_f - frac_ma,
                                  k_ma_mean=float(gm.loc[start:].sum(axis=1).mean()),
                                  k_q_mean=float(gq.loc[start:].sum(axis=1).mean()),
                                  k_f_mean=float(gf.loc[start:].sum(axis=1).mean()),
                                  k_ma_sd=float(gm.loc[start:].sum(axis=1).std()),
                                  k_q_sd=float(gq.loc[start:].sum(axis=1).std()),
                                  k_f_sd=float(gf.loc[start:].sum(axis=1).std())))

        # ------------------------------------------- the grid
        for th in MA_THETA:
            xth = float([m["x"] for m in matchrows
                         if m["panel"] == pn and m["theta"] == th][0])
            for cad in CADENCES:
                got = {}
                for fam in FAMILIES:
                    g = gates[th][fam]
                    arms = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, book(px, g, con), cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        arms[con] = dict(r10=r10, r0=r0, gross=grs, s=s, turn=turn)
                        rows.append(dict(panel=pn, theta=th, x=xth, cad=cad, family=fam, con=con,
                                         **s, CAGR0=cagr(r0),
                                         gross_mean=float(grs.mean()),
                                         gross_min=float(grs.min()),
                                         turn_yr=float(turn.sum() / years),
                                         dCAGR_ctrl=s["CAGR"] - ctrl[cad]["CAGR"],
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())

                    def dec(lo, hi, tag, rs=rs, dg=dg, c_t=c_t):
                        sl = slice(lo, hi)
                        rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                        cb = float(c_t.loc[sl].mean())
                        g0 = 100 * (cagr(rd) - cagr(rr))
                        p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        return dict(window=tag, c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                    gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                    share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                                    CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd))

                    base = dict(panel=pn, theta=th, cad=cad, family=fam, ident_max_err=ident)
                    cells = {}
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        d = dec(lo, hi, tag)
                        cells[tag] = d
                        decomp.append({**base, **d})
                    got[fam] = dict(arms=arms, cells=cells)

                for qfam in Q_FAMS:
                  for con in CONSTRUCTIONS:
                    a = got["MA-THRESH"]["arms"][con]["s"]
                    b = got[qfam]["arms"][con]["s"]
                    cm, cq = got["MA-THRESH"]["cells"], got[qfam]["cells"]
                    pair.append(dict(
                        panel=pn, theta=th, x=xth, cad=cad, con=con, qfam=qfam,
                        c_bar_ma=cm["FULL"]["c_bar"], c_bar_q=cq["FULL"]["c_bar"],
                        d_c_bar=cq["FULL"]["c_bar"] - cm["FULL"]["c_bar"],
                        c_sd_ma=cm["FULL"]["c_sd"], c_sd_q=cq["FULL"]["c_sd"],
                        Sharpe_ma=a["Sharpe"], Sharpe_q=b["Sharpe"],
                        dSharpe=a["Sharpe"] - b["Sharpe"],
                        CAGR_ma=a["CAGR"], CAGR_q=b["CAGR"],
                        dCAGR_pp=100 * (a["CAGR"] - b["CAGR"]),
                        MaxDD_ma=a["MaxDD"], MaxDD_q=b["MaxDD"],
                        dMaxDD_pp=100 * (a["MaxDD"] - b["MaxDD"]),
                        H1_ma=a["H1"], H1_q=b["H1"], dH1=a["H1"] - b["H1"],
                        H2_ma=a["H2"], H2_q=b["H2"], dH2=a["H2"] - b["H2"],
                        isSharpe_ma=a["isSharpe"], isSharpe_q=b["isSharpe"],
                        dSharpe_is=a["isSharpe"] - b["isSharpe"],
                        oSharpe_ma=a["oSharpe"], oSharpe_q=b["oSharpe"],
                        dSharpe_oos=a["oSharpe"] - b["oSharpe"],
                        oCAGR_ma=a["oCAGR"], oCAGR_q=b["oCAGR"],
                        dCAGR_oos_pp=100 * (a["oCAGR"] - b["oCAGR"]),
                        oMaxDD_ma=a["oMaxDD"], oMaxDD_q=b["oMaxDD"],
                        turn_ma=float(got["MA-THRESH"]["arms"][con]["turn"].sum() / years),
                        turn_q=float(got[qfam]["arms"][con]["turn"].sum() / years),
                        resid_ma_pp=cm["FULL"]["resid0_pp"], resid_q_pp=cq["FULL"]["resid0_pp"],
                        d_resid_pp=cm["FULL"]["resid0_pp"] - cq["FULL"]["resid0_pp"],
                        sel_pp=100 * (cm["FULL"]["CAGR_rs0"] - cq["FULL"]["CAGR_rs0"]),
                        level_pp=cm["FULL"]["pred0_pp"] - cq["FULL"]["pred0_pp"],
                        timing_pp=cm["FULL"]["resid0_pp"] - cq["FULL"]["resid0_pp"],
                        dCAGR0_dg_pp=100 * (cm["FULL"]["CAGR_dg0"] - cq["FULL"]["CAGR_dg0"]),
                        dCAGR0_rs_pp=100 * (cm["FULL"]["CAGR_rs0"] - cq["FULL"]["CAGR_rs0"]),
                    ))
            P(f"  {pn}: theta {th:+.2f} done ({len(CADENCES) * len(FAMILIES) * 2} books)")
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    PR = pd.DataFrame(pair)
    M = pd.DataFrame(matchrows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)
    M.to_csv(f"{OUT}.matched.csv", index=False)
    F = D[D.window == "FULL"]
    QM = PR[PR.qfam == "QUANTILE-M"]
    PD_ = QM[QM.con == "DEGROSS"].copy()        # the pre-registered headline pair
    PRS = QM[QM.con == "RESPREAD"].copy()
    QF = PR[PR.qfam == "QUANTILE-F"]
    PF_ = QF[QF.con == "DEGROSS"].copy()        # the exact-matched restatement

    # --------------------------------------------- B_MATCH
    P("\n" + "=" * 175)
    P("B_MATCH - validity gates, read BEFORE the headline (per panel)")
    P("=" * 175)
    bm = []
    for qfam, dcol in (("QUANTILE-M", "d_frac"), ("QUANTILE-F", "d_frac_f")):
        Pq = PR[(PR.qfam == qfam) & (PR.con == "DEGROSS")]
        for pn in PANELS:
            dfr = M[M.panel == pn][dcol].abs().max()
            dcb = Pq[Pq.panel == pn].d_c_bar.abs().max()
            idm = F[F.panel == pn].ident_max_err.max()
            rq = F[(F.panel == pn) & (F.family == qfam)].resid0_pp
            rma = F[(F.panel == pn) & (F.family == "MA-THRESH")].resid0_pp
            ok = (dfr < BAR_MASK_TOL) and (dcb < BAR_CBAR_TOL) and (idm < BAR_IDENT) \
                and (abs(rq.mean()) < BAR_Q_RESID)
            bm.append(dict(qfam=qfam, panel=pn, d_frac=dfr, d_c_bar=dcb, ident=idm,
                           q_resid=rq.mean(), ma_resid=rma.mean(), PASS=ok))
            P(f"  {qfam} {pn:9s} |d mask frac| {dfr:.5f} (<{BAR_MASK_TOL}) | |d c_bar| "
              f"{dcb:.5f} (<{BAR_CBAR_TOL}) | identity {idm:.3e} (<{BAR_IDENT:.0e}) | "
              f"{qfam} resid0 mean {rq.mean():+.4f} pp/yr (<+/-{BAR_Q_RESID}) -> "
              f"{'PASS' if ok else 'FAIL'}")
            if qfam == "QUANTILE-M":
                P(f"                      MA-THRESH resid0 mean {rma.mean():+.4f} pp/yr "
                  f"(sd {rma.std():.4f}, range {rma.min():+.4f}..{rma.max():+.4f}); idea 298's "
                  f"band {BAR_MA_RESID} -> "
                  f"{'inside' if BAR_MA_RESID[0] <= rma.mean() <= BAR_MA_RESID[1] else 'OUTSIDE'} "
                  f"[REPORTED, not a gate]")
    BM = pd.DataFrame(bm)
    BM.to_csv(f"{OUT}.bmatch.csv", index=False)
    for qfam in Q_FAMS:
        sub = BM[BM.qfam == qfam]
        P(f"  B_MATCH ({qfam}): "
          f"{'PASS' if sub.PASS.all() else 'FAIL on ' + str(list(sub.loc[~sub.PASS, 'panel']))}")
    P("  NOTE the pre-registered arm (QUANTILE-M) fails its own matching tolerance off "
      "SMALL439: ceil(x*n_t) rounds the constant-depth arm UP by up to 1/n_t of exposure per "
      "day, which is small at n=439 and not at n=56/136.  QUANTILE-F removes exactly that.")
    flush_log()

    # --------------------------------------------- reproduction gates
    P("\n" + "=" * 175)
    P("REPRODUCTION GATES - reproduce the record before extending it")
    P("=" * 175)
    s439 = PD_[PD_.panel == "SMALL439"]
    r439 = PRS[PRS.panel == "SMALL439"]
    f439 = F[F.panel == "SMALL439"]
    got = dict(dSharpe=s439.dSharpe.mean(), dSharpe_oos=s439.dSharpe_oos.mean(),
               dSharpe_rs=r439.dSharpe.mean(),
               resid_ma=f439[f439.family == "MA-THRESH"].resid0_pp.mean(),
               resid_q=f439[f439.family == "QUANTILE-M"].resid0_pp.mean(),
               dCAGR0=s439.dCAGR0_dg_pp.mean(), sel=s439.sel_pp.mean(),
               lev=s439.level_pp.mean(), tim=s439.timing_pp.mean())
    P("R1 vs idea 300's published SMALL439 headline:")
    r1ok = True
    for k, v in R1.items():
        tol = R1_TOL_S if "Sharpe" in k else R1_TOL_PP
        ok = abs(got[k] - v) <= tol
        r1ok &= ok
        P(f"   {k:12s} published {v:+.4f}  here {got[k]:+.4f}  |d| {abs(got[k] - v):.4f} "
          f"(tol {tol})  {'PASS' if ok else 'FAIL'}")
    P(f"  R1: {'PASS' if r1ok else 'FAIL'}")

    P("\nR2 vs idea 306's pairs.csv (gross 0.75, cadences W/M/Q, cell by cell):")
    r2ok, r2n, r2max = False, 0, np.nan
    if IDEA306.exists():
        o = pd.read_csv(IDEA306)
        o = o[(o.gross == 0.75) & (o.cad.isin(CADENCES))]
        j = QM.merge(o[["panel", "cad", "theta", "con", "dSharpe", "dCAGR_pp"]],
                     on=["panel", "cad", "theta", "con"], suffixes=("", "_306"))
        r2n = len(j)
        r2max = float((j.dSharpe - j.dSharpe_306).abs().max()) if r2n else np.nan
        r2max_c = float((j.dCAGR_pp - j.dCAGR_pp_306).abs().max()) if r2n else np.nan
        r2ok = bool(r2n == len(QM) and r2max < R2_TOL)
        P(f"   matched {r2n}/{len(QM)} cells; max |d dSharpe| {r2max:.3e}, max |d dCAGR_pp| "
          f"{r2max_c:.3e} (tol {R2_TOL:.0e})  {'PASS' if r2ok else 'FAIL'}")
    else:
        P("   idea 306 pairs.csv not found - R2 NOT RUN")
    flush_log()

    # --------------------------------------------- decomposition
    P("\n" + "=" * 175)
    P("DECOMPOSITION - full-sample cells (0 bps), both families, all three panels")
    P("=" * 175)
    for pn in PANELS:
        for fam in FAMILIES:
            P(f"\n--- {pn} / {fam} ---")
            P(fmt(F[(F.panel == pn) & (F.family == fam)].set_index(["theta", "cad"])[
                ["c_bar", "c_sd", "CAGR_rs0", "CAGR_dg0", "gap0_pp", "pred0_pp", "resid0_pp",
                 "share"]]))
    P("\nresid0 (pp/yr) by panel x family, full sample:")
    P(fmt(F.groupby(["panel", "family"]).resid0_pp.agg(["mean", "std", "min", "max"])))
    flush_log()

    # --------------------------------------------- THE HEADLINE
    P("\n" + "=" * 175)
    P("HEADLINE - MA-THRESH minus matched QUANTILE-M, DEGROSS, 10 bps, 27 cells per panel")
    P("=" * 175)
    for pn in PANELS:
        P(f"\n--- {pn} ---")
        P(fmt(PD_[PD_.panel == pn].set_index(["theta", "cad"])[
            ["c_bar_ma", "c_bar_q", "Sharpe_ma", "Sharpe_q", "dSharpe", "dH1", "dH2",
             "dSharpe_oos", "dCAGR_pp", "dMaxDD_pp", "d_resid_pp", "turn_ma", "turn_q"]]))
    P("\n(dSharpe > 0 means the MA gate's time-varying depth is worth paying for; "
      "dMaxDD_pp > 0 means the MA gate drew down LESS.)")

    P("\n" + "-" * 175)
    P("SUMMARY by panel (all 27 cells):")
    agg = PD_.groupby("panel").agg(
        n=("dSharpe", "size"), dSharpe=("dSharpe", "mean"),
        pos=("dSharpe", lambda s: int((s > 0).sum())),
        dSharpe_med=("dSharpe", "median"), dSharpe_sd=("dSharpe", "std"),
        dSharpe_oos=("dSharpe_oos", "mean"),
        pos_oos=("dSharpe_oos", lambda s: int((s > 0).sum())),
        dCAGR_pp=("dCAGR_pp", "mean"), dMaxDD_pp=("dMaxDD_pp", "mean"),
        d_resid_pp=("d_resid_pp", "mean"),
        turn_ratio=("turn_ma", "mean"))
    agg["turn_ratio"] = PD_.groupby("panel").turn_ma.mean() / PD_.groupby("panel").turn_q.mean()
    P(fmt(agg.reindex(PANELS)))

    P(f"\nTHE QUEUE'S TEST - restricted to cells with c_bar >= {CBAR_FLOOR} "
      "(where a real book lives):")
    HI = PD_[PD_.c_bar_ma >= CBAR_FLOOR]
    aggh = HI.groupby("panel").agg(
        n=("dSharpe", "size"), dSharpe=("dSharpe", "mean"),
        pos=("dSharpe", lambda s: int((s > 0).sum())),
        dSharpe_min=("dSharpe", "min"), dSharpe_max=("dSharpe", "max"),
        dSharpe_oos=("dSharpe_oos", "mean"),
        pos_oos=("dSharpe_oos", lambda s: int((s > 0).sum())),
        dCAGR_pp=("dCAGR_pp", "mean"), dMaxDD_pp=("dMaxDD_pp", "mean"))
    P(fmt(aggh.reindex([p for p in PANELS if p in aggh.index])))

    P("\nby theta rung (mean over cadences), DEGROSS dSharpe:")
    rung = PD_.pivot_table(index="theta", columns="panel", values="dSharpe", aggfunc="mean")
    rungc = PD_.pivot_table(index="theta", columns="panel", values="c_bar_ma", aggfunc="mean")
    rungo = PD_.pivot_table(index="theta", columns="panel", values="dSharpe_oos", aggfunc="mean")
    tbl = pd.concat({"c_bar": rungc[PANELS], "dSharpe": rung[PANELS], "dSharpe_oos": rungo[PANELS]},
                    axis=1)
    P(fmt(tbl))
    P("\nby cadence, DEGROSS dSharpe:")
    P(fmt(PD_.pivot_table(index="cad", columns="panel", values="dSharpe", aggfunc="mean")[PANELS]))
    P("\nHOW MUCH OF THIS IS THE MATCHING ERROR?  d_c_bar = c_bar(QUANTILE) - c_bar(MA); a "
      "positive value means the constant-depth arm was handed extra exposure by ceil() rounding:")
    for pn in PANELS:
        a, b = PD_[PD_.panel == pn], PD_[(PD_.panel == pn) & (PD_.c_bar_ma >= CBAR_FLOOR)]
        f = PF_[PF_.panel == pn]
        P(f"  {pn:9s} QUANTILE-M d_c_bar mean {a.d_c_bar.mean():+.4f} (max |{a.d_c_bar.abs().max():.4f}|), "
          f"corr(dSharpe, d_c_bar) all {a.dSharpe.corr(a.d_c_bar):+.3f} / at c_bar>={CBAR_FLOOR} "
          f"{b.dSharpe.corr(b.d_c_bar):+.3f}  ||  QUANTILE-F d_c_bar mean {f.d_c_bar.mean():+.4f} "
          f"(max |{f.d_c_bar.abs().max():.4f}|)")
    P("\nQUANTILE-F pair (exactly matched exposure), DEGROSS, by panel:")
    P(fmt(PF_.groupby("panel").agg(n=("dSharpe", "size"), dSharpe=("dSharpe", "mean"),
                                   pos=("dSharpe", lambda s: int((s > 0).sum())),
                                   dSharpe_oos=("dSharpe_oos", "mean"),
                                   dCAGR_pp=("dCAGR_pp", "mean"),
                                   dMaxDD_pp=("dMaxDD_pp", "mean"),
                                   d_resid_pp=("d_resid_pp", "mean")).reindex(PANELS)))
    P("\nRESPREAD arm (exposure pinned; isolates the slice-depth SELECTION effect):")
    P(fmt(PRS.groupby("panel").agg(dSharpe=("dSharpe", "mean"),
                                   pos=("dSharpe", lambda s: int((s > 0).sum())),
                                   dCAGR_pp=("dCAGR_pp", "mean"),
                                   dMaxDD_pp=("dMaxDD_pp", "mean")).reindex(PANELS)))
    flush_log()

    # --------------------------------------------- pre-registered verdict
    P("\n" + "=" * 175)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 175)
    clauses = {}
    for pn in TARGET:
        h = HI[HI.panel == pn]
        c1 = float(h.dSharpe.mean()) <= 0
        c2 = float(h.dSharpe_oos.mean()) <= 0
        byrung = h.groupby("theta").dSharpe.mean()
        c3 = bool((byrung <= 0).all())
        clauses[pn] = (c1, c2, c3)
        P(f"  {pn:5s} n={len(h)} cells with c_bar >= {CBAR_FLOOR}: "
          f"(1) mean dSharpe {h.dSharpe.mean():+.4f} <= 0 -> {'PASS' if c1 else 'FAIL'}; "
          f"(2) mean OOS {h.dSharpe_oos.mean():+.4f} <= 0 -> {'PASS' if c2 else 'FAIL'}; "
          f"(3) rungs above 0: {int((byrung > 0).sum())}/{len(byrung)} -> "
          f"{'PASS' if c3 else 'FAIL'}")
        P(f"        rung means: " + ", ".join(f"{t:+.2f}:{v:+.4f}" for t, v in byrung.items()))
    replicates = all(all(v) for v in clauses.values())
    P(f"\n  H_REPLICATES    -> {'HOLDS' if replicates else 'FAILS'}")
    P(f"  H_PANEL_SPECIFIC -> {'FAILS' if replicates else 'HOLDS'}")
    if not replicates:
        for pn, (c1, c2, c3) in clauses.items():
            if not (c1 and c2 and c3):
                P(f"     broken on {pn}: clauses "
                  + ", ".join(n for n, ok in zip(("1 full", "2 OOS", "3 rungs"), (c1, c2, c3))
                              if not ok))

    # -- the same three clauses on the EXACTLY matched arm (the B_MATCH repair, not a re-tune)
    P("\nRESTATEMENT on QUANTILE-F (exposure matched exactly, so the ceil() bias is removed):")
    HF = PF_[PF_.c_bar_ma >= CBAR_FLOOR]
    clausesF = {}
    for pn in TARGET:
        h = HF[HF.panel == pn]
        byrung = h.groupby("theta").dSharpe.mean()
        c1, c2 = float(h.dSharpe.mean()) <= 0, float(h.dSharpe_oos.mean()) <= 0
        c3 = bool((byrung <= 0).all())
        clausesF[pn] = (c1, c2, c3)
        P(f"  {pn:5s} n={len(h)}: (1) mean dSharpe {h.dSharpe.mean():+.4f} -> "
          f"{'PASS' if c1 else 'FAIL'}; (2) mean OOS {h.dSharpe_oos.mean():+.4f} -> "
          f"{'PASS' if c2 else 'FAIL'}; (3) rungs above 0 {int((byrung > 0).sum())}/{len(byrung)}"
          f" -> {'PASS' if c3 else 'FAIL'} | worst |d c_bar| "
          f"{PF_[PF_.panel == pn].d_c_bar.abs().max():.5f}")
        P(f"        rung means: " + ", ".join(f"{t:+.2f}:{v:+.4f}" for t, v in byrung.items()))
    P(f"  all 27 cells, QUANTILE-F pair: "
      + " | ".join(f"{pn} dSharpe {PF_[PF_.panel == pn].dSharpe.mean():+.4f} "
                   f"({int((PF_[PF_.panel == pn].dSharpe > 0).sum())}/27 pos, OOS "
                   f"{PF_[PF_.panel == pn].dSharpe_oos.mean():+.4f})" for pn in PANELS))
    replicatesF = all(all(v) for v in clausesF.values())
    P(f"  H_REPLICATES on the exactly-matched arm -> {'HOLDS' if replicatesF else 'FAILS'}")
    flush_log()

    # --------------------------------------------- exact attribution
    P("\n" + "=" * 175)
    P("EXACT ATTRIBUTION of the 0-bps DEGROSS CAGR difference (identity, not a fit)")
    P("   dCAGR0_dg = SELECTION + LEVEL + TIMING   (pp/yr)")
    P("=" * 175)
    PD_["check"] = PD_.dCAGR0_dg_pp - (PD_.sel_pp + PD_.level_pp + PD_.timing_pp)
    P(fmt(PD_.groupby("panel").agg(dCAGR0_dg_pp=("dCAGR0_dg_pp", "mean"),
                                   SELECTION=("sel_pp", "mean"), LEVEL=("level_pp", "mean"),
                                   TIMING=("timing_pp", "mean"),
                                   max_check=("check", lambda s: s.abs().max())).reindex(PANELS)))
    P(f"identity closes to {PD_.check.abs().max():.3e} pp "
      f"({'PASS' if PD_.check.abs().max() < 1e-9 else 'FAIL'} at 1e-9) over {len(PD_)} cells")
    flush_log()

    # --------------------------------------------- KEEP paths
    P("\n" + "=" * 175)
    P(f"KEEP PATHS on all {len(G)} books")
    P("=" * 175)
    P(f"4a passes: {int(G.p4a.sum())}/{len(G)}    4b passes: {int(G.p4b.sum())}/{len(G)}")
    P(fmt(G.groupby("panel").agg(n=("p4a", "size"), p4a=("p4a", "sum"),
                                 p4b=("p4b", "sum")).reindex(PANELS), 0))
    P("\n4b failure reasons (count of books by failing clause set):")
    P(fmt(G.f4b.value_counts().to_frame("n"), 0))
    if G.p4b.any():
        P("\n4b PASSERS:")
        P(fmt(G[G.p4b].set_index(["panel", "family", "con", "theta", "cad"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "turn_yr"]]))
    if G.p4a.any():
        P("\n4a PASSERS:")
        P(fmt(G[G.p4a].set_index(["panel", "family", "con", "theta", "cad"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "turn_yr"]]))
    P(f"\nBOTH 4a and 4b: {int((G.p4a & G.p4b).sum())}/{len(G)}")
    P("\nbest full-sample Sharpe per panel x family x construction:")
    P(fmt(G.loc[G.groupby(["panel", "family", "con"]).Sharpe.idxmax()]
          .set_index(["panel", "family", "con"])[
              ["theta", "cad", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]]))
    flush_log()

    # --------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 175)
    P("RULE 8 WALK-FORWARD.  IS = start..2016-12-31 (selection), OOS = 2017-01-01..end (once)")
    P("=" * 175)
    wf = []
    P("\nWF-A: (theta, cadence) picked by IS Sharpe inside each panel x family x construction")
    for (pn, fam, con), sub in G.groupby(["panel", "family", "con"]):
        pick = sub.loc[sub.isSharpe.idxmax()]
        spy_s, live_s = spy_by_panel[pn], live_by_panel[pn]
        wf.append(dict(test="WF-A", panel=pn, arm=f"{fam}/{con}",
                       pick=f"theta {pick.theta:+.2f} cad {pick.cad}", isSharpe=pick.isSharpe,
                       oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                       vs_SPY=pick.oSharpe - spy_s["oSharpe"],
                       vs_RULESv2=pick.oSharpe - live_s["oSharpe"]))
        P(f"  {pn:9s} {fam:11s}/{con:8s} picks theta {pick.theta:+.2f} cad {pick.cad} "
          f"(IS Sharpe {pick.isSharpe:.4f}) -> OOS CAGR {pick.oCAGR:.4f} Sharpe "
          f"{pick.oSharpe:.4f} MaxDD {pick.oMaxDD:.4f}")
    for pn in PANELS:
        s_, l_ = spy_by_panel[pn], live_by_panel[pn]
        P(f"  comparands OOS on {pn:9s}: SPY Sharpe {s_['oSharpe']:.4f} CAGR {s_['oCAGR']:.4f} | "
          f"RULES v2 Sharpe {l_['oSharpe']:.4f} CAGR {l_['oCAGR']:.4f} | EWall "
          + " ".join(f"{c} {ctrl_by_panel[pn][c]['oSharpe']:.4f}" for c in CADENCES))

    P("\nWF-B: per cell pick the family with the higher IS Sharpe (DEGROSS), read OOS once")
    for pn in PANELS:
        h = PD_[PD_.panel == pn]
        picked_ma = h.dSharpe_is > 0
        oos_pick = np.where(picked_ma, h.oSharpe_ma, h.oSharpe_q)
        oos_pick_c = np.where(picked_ma, h.oCAGR_ma, h.oCAGR_q)
        hit = float(((h.dSharpe_is > 0) == (h.dSharpe_oos > 0)).mean())
        P(f"  {pn:9s} IS prefers MA in {int(picked_ma.sum())}/{len(h)} | OOS Sharpe PICK "
          f"{oos_pick.mean():.4f} | always-MA {h.oSharpe_ma.mean():.4f} | always-QUANTILE-M "
          f"{h.oSharpe_q.mean():.4f} | OOS CAGR PICK {oos_pick_c.mean():.4f} | "
          f"IS->OOS sign agreement {hit:.4f} ({int(round(hit * len(h)))}/{len(h)})")
        wf.append(dict(test="WF-B", panel=pn, arm="family pick (DEGROSS)",
                       pick=f"MA in {int(picked_ma.sum())}/{len(h)}", isSharpe=np.nan,
                       oCAGR=float(oos_pick_c.mean()), oSharpe=float(oos_pick.mean()),
                       oMaxDD=np.nan, vs_SPY=np.nan, vs_RULESv2=hit))

    P("\nWF-C: does the constant-residual discount walk forward on each panel?")
    for pn in PANELS:
        for fam in FAMILIES:
            di = D[(D.panel == pn) & (D.family == fam) & (D.window == "IS")] \
                .set_index(["theta", "cad"]).resid0_pp
            do = D[(D.panel == pn) & (D.family == fam) & (D.window == "OOS")] \
                .set_index(["theta", "cad"]).resid0_pp
            mae_zero = float(do.abs().mean())
            mae_const = float((do - di.mean()).abs().mean())
            mae_cell = float((do - di).abs().mean())
            P(f"  {pn:9s} {fam:11s}: IS mean resid0 {di.mean():+.4f} pp/yr, OOS mean "
              f"{do.mean():+.4f} | OOS MAE vs zero {mae_zero:.4f} | vs IS-mean constant "
              f"{mae_const:.4f} | vs own IS cell {mae_cell:.4f} -> "
              f"{'constant beats zero' if mae_const < mae_zero else 'ZERO beats the constant'}")
            wf.append(dict(test="WF-C", panel=pn, arm=fam, pick="IS-mean constant",
                           isSharpe=di.mean(), oCAGR=do.mean(), oSharpe=mae_const,
                           oMaxDD=mae_zero, vs_SPY=np.nan, vs_RULESv2=mae_cell))
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # --------------------------------------------- answer
    P("\n" + "=" * 175)
    P("ANSWER")
    P("=" * 175)
    P(f"Does idea 300's uncompensated-residual finding replicate off SMALL439?  "
      f"pre-registered arm: {'YES' if replicates else 'NO / QUALIFIED'};  "
      f"exactly-matched arm: {'YES' if replicatesF else 'NO / QUALIFIED'}")
    for pn in PANELS:
        h = HI[HI.panel == pn]
        a = PD_[PD_.panel == pn]
        hf, af = HF[HF.panel == pn], PF_[PF_.panel == pn]
        P(f"  {pn:9s} QUANTILE-F (exact match): all 27 dSharpe {af.dSharpe.mean():+.4f} "
          f"({int((af.dSharpe > 0).sum())}/27 pos, OOS {af.dSharpe_oos.mean():+.4f}); at "
          f"c_bar >= {CBAR_FLOOR} (n={len(hf)}) dSharpe {hf.dSharpe.mean():+.4f} "
          f"[{hf.dSharpe.min():+.4f}..{hf.dSharpe.max():+.4f}], OOS {hf.dSharpe_oos.mean():+.4f}")
        P(f"  {pn:9s}: all 27 cells dSharpe {a.dSharpe.mean():+.4f} ({int((a.dSharpe > 0).sum())}"
          f"/27 positive, OOS {a.dSharpe_oos.mean():+.4f}); at c_bar >= {CBAR_FLOOR} "
          f"(n={len(h)}) dSharpe {h.dSharpe.mean():+.4f} "
          f"[{h.dSharpe.min():+.4f}..{h.dSharpe.max():+.4f}], OOS {h.dSharpe_oos.mean():+.4f}; "
          f"MA resid0 {F[(F.panel == pn) & (F.family == 'MA-THRESH')].resid0_pp.mean():+.4f} vs "
          f"QM {F[(F.panel == pn) & (F.family == 'QUANTILE-M')].resid0_pp.mean():+.4f} pp/yr")
    P(f"  KEEP paths: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}, "
      f"BOTH {int((G.p4a & G.p4b).sum())}/{len(G)}.")
    P(f"  reproduction: R1 {'PASS' if r1ok else 'FAIL'}, R2 "
      f"{'PASS' if r2ok else 'FAIL/NOT RUN'} ({r2n} cells, max |d| {r2max:.2e}).")
    flush_log()
    P(f"\nwrote {OUT.name}.grid.csv .decomp.csv .matched.csv .pairs.csv .walkforward.csv "
      f".console.txt")
    flush_log()


if __name__ == "__main__":
    main()
