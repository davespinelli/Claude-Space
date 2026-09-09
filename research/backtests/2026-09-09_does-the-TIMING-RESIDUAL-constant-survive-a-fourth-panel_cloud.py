#!/usr/bin/env python3
"""Idea 555 - "does-the-TIMING-RESIDUAL-constant-survive-a-fourth-panel" (cloud, 2026-09-09).

The question
------------
Idea 305 measured the MA gate's EXPOSURE-TIMING RESIDUAL

    resid0 = gap0 - pred0,
    gap0   = CAGR(DEGROSS book, 0 bps) - CAGR(RESPREAD book, 0 bps)          [pp/yr]
    pred0  = CAGR(c_bar * RESPREAD book, 0 bps) - CAGR(RESPREAD book, 0 bps) [pp/yr]

on three panels and got -0.3375 (U56) / -0.4231 (B136) / -0.3817 (SMALL439) pp/yr - a
0.086 pp/yr spread across panels differing 8x in width - while the SAME gate's PRICE in
Sharpe does not replicate across those panels at all.  The record has since been quoting
resid0 as if it were a property of the GATE FORM.  It has never been measured on a panel
the record did not already own, and with three points and three panel characteristics
moving together, nothing separates "gate-form constant" from "tracks a characteristic".

  QUEUE'S EXACT TEST: measure resid0 directly on a FOURTH cut - fresh sub-panels drawn
  from B136 at CONTROLLED ETF share - and report whether resid0 is a gate-form constant
  or tracks a panel characteristic.

Pre-registered hypotheses and bars (written before any fresh-cut number was read)
--------------------------------------------------------------------------------
Let R_p = mean resid0 over the published constant's OWN domain (MA-THRESH family, FULL
window, 9 theta x 3 cadences W/M/Q, gross 0.75, 0 bps derived).  The three anchors span
    ANCHOR_SPAN = |-0.4231 - (-0.3375)| = 0.0856 pp/yr.

H_GATEFORM.  resid0 is a property of the gate form.  BAR (both clauses, on the 36 fresh
    cuts, which are drawn from ONE parent panel and therefore have LESS characteristic
    variation than the three anchors do):
      (1) the fresh cuts' panel-level R_p range <= 2 x ANCHOR_SPAN = 0.1712 pp/yr; and
      (2) no measured panel characteristic explains more than R2 = 0.30 of the
          cross-panel variation of R_p (single-regressor OLS, 39 panels).
H_CHARACTERISTIC.  Either clause fails: resid0 moves with the panel, and the record's
    "gate-form constant" reading has to be re-quoted with the characteristic it tracks.
The two are exhaustive and mutually exclusive.  Both clauses are reported either way, and
the identity of the winning characteristic (if any) is reported whatever the verdict.

The fresh cut (the "fourth panel")
    B136 has 135 investable names, 35 of them ETFs (26% ETF share) and 100 single stocks.
    Sub-panels are drawn at ETF share q in {0.00, 0.25, 0.50} and width W in {30, 60},
    6 seeds each = 36 fresh cuts, every draw a uniform sample without replacement from
    the ETF pool and the stock pool separately, seeded by (q, W, seed) so the run is
    deterministic.  SPY rides along as the benchmark column only, never investable.
    q = 0.50 at W = 60 needs 30 of the 35 available ETFs, so the ladder stops there.
    PANEL IS ONE DIAL with 39 levels (3 anchors + 36 cuts), not three dials: nothing is
    ever chosen on width, ETF share or seed - they are the CHARACTERISTICS whose ability
    to price R_p is the question.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel  (39 levels: 3 anchors + 36 fresh cuts)
    2. theta  (9 levels, idea 298/300/305's grid verbatim)
    Cadence W/M/Q is NOT a third dial: the published constant is a mean over exactly that
    domain, so reproducing and extending it requires the same domain.  It is reported at
    every level (which is queue idea 553's separate question) and selected at none outside
    rule 8.  Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps
    rung is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run.
    Grid: 39 panels x 9 theta x 3 cadences x 2 families x 2 constructions = 4,212 books.
    ALL grid points are written to .grid.csv and .decomp.csv.

Families and constructions (idea 305's verbatim)
    MA-THRESH   IN where px > ma200*(1+theta); c_bar is an outcome.
    QUANTILE-F  same ranking (dist = px/ma200 - 1), same MEAN mask fraction x (= the MA
                arm's own mean mask fraction at that theta on that panel), marginal name
                carries the fractional weight so the mask fraction is EXACTLY x every day.
                x is a deterministic function of theta, not a dial.  Idea 305 showed the
                ceil()-rounded QUANTILE-M arm fails its own exposure-match gate on narrow
                panels (1/n_t per day = 1.8% on U56), and this run's cuts are narrower
                still (W=30), so QUANTILE-F is the matched control here.  QUANTILE-M is
                NOT run: it is the arm idea 305 showed to be mis-matched at these widths.
    RESPREAD    w = g/k_t (gross pinned);  DEGROSS  w = g/n_t (gated weight to cash).
    resid0 is a DEGROSS-vs-RESPREAD decomposition and is defined per (panel, theta,
    cadence, family); the headline constant is the MA-THRESH one.

Validity gates, read BEFORE the headline
    G0  fast_backtest reproduces engine.backtest to < 1e-12 on returns AND turnover.
    G1  DEGROSS/RESPREAD identity r_dg,t = c_t * r_rs,t closes to < 1e-12 in every cell.
    G2  |mean QUANTILE-F resid0| < 0.05 pp/yr per panel - the constant-depth arm must be
        the pure exposure control the decomposition assumes.
    G3  |d mask fraction| (QUANTILE-F minus MA-THRESH) < 0.01 in every (panel, theta).
    R1  REPRODUCTION: the three anchor panels must return idea 305's published R_p to
        within 0.02 pp/yr: U56 -0.3375, B136 -0.4231, SMALL439 -0.3817.
    A gate FAIL is reported and the affected rows are excluded from the headline, not
    silently carried.

Rule 8 walk-forward (required; every direction fixed before any OOS number was read)
    IS = start..2016-12-31 (selection), OOS = 2017-01-01..end (read once).
    WF-A  theta chosen on IS Sharpe inside each (panel, family, construction, cadence)
          arm; OOS CAGR/Sharpe/MaxDD reported against RULES v2 (live), SPY and the
          cadence-matched no-gate EWall control on the same panel.
    WF-B  DOES THE CONSTANT WALK FORWARD?  Fit nothing.  Take each panel's IS-window mean
          resid0 and score it against that panel's OOS resid0; compare MAE to (a) the
          zero baseline and (b) the POOLED IS constant (one number for all 39 panels).
          If the pooled constant beats the per-panel one out of sample, resid0 is
          gate-form; if the per-panel one wins, it tracks the panel.
    WF-C  the H_GATEFORM R2 clause re-run on IS only and on OOS only, so a characteristic
          that prices resid0 in-sample but not out of sample is visible as such.

Verdicts (both KEEP paths, on every one of the 4,212 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: B136 (research/universe_broad.json) and SMALL439 (data/prices_small.csv.gz)
are CURRENT constituents - no delistings - so every CAGR LEVEL on those panels, and on
every fresh cut drawn from B136, is inflated, and the 4a/4b columns inherit that bias
whole.  resid0 is an arm-minus-arm contrast on the SAME names, the SAME ranking and the
SAME days, so the bias very largely cancels out of it; it does NOT cancel out of the KEEP
columns, which is why no book here would be promoted on this run's evidence alone.
SMALL439: tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped first.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its own
outputs.  Outputs: .grid.csv .decomp.csv .panels.csv .constant.csv .walkforward.csv
.keeppaths.csv .console.txt
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
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-F"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
ANCHORS = ["U56", "B136", "SMALL439"]
Q_LADDER = [0.00, 0.25, 0.50]
W_LADDER = [30, 60]
SEEDS = [0, 1, 2, 3, 4, 5]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# published anchors (idea 305, .bmatch.csv column ma_resid) -- pp/yr
R1 = {"U56": -0.3375, "B136": -0.4231, "SMALL439": -0.3817}
R1_TOL = 0.02
ANCHOR_SPAN = abs(R1["B136"] - R1["U56"])       # 0.0856 pp/yr
BAR_RANGE = 2 * ANCHOR_SPAN                     # 0.1712 pp/yr
BAR_R2 = 0.30
BAR_IDENT = 1e-12
BAR_Q_RESID = 0.05                              # pp/yr
BAR_MASK = 0.01

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


# ---------------------------------------------------------------- backtest core
def fast_backtest(px, weights, freq):
    """Vectorised twin of engine.backtest at ZERO cost; gated against it in G0."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n)
    turn = np.zeros(n)
    gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(gross, index=idx))


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def dist_rank(px):
    return (px / px.rolling(200).mean() - 1).where(live_mask(px))


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate_frac(px, x):
    """Same ranking, same mean exposure x, marginal name fractionally weighted so the
    mask fraction is EXACTLY x every day (no ceil() rounding)."""
    dist = dist_rank(px)
    live = live_mask(px)
    n = live.sum(axis=1)
    kf = x * n
    kfl = np.floor(kf)
    rank = dist.rank(axis=1, ascending=False, method="first")
    full = (rank.le(kfl, axis=0).fillna(False) & live).astype(float)
    marg = (rank.eq(kfl + 1, axis=0).fillna(False) & live).astype(float)
    return full + marg.mul(kf - kfl, axis=0)


def book(px, g, construction):
    gf = g.astype(float)
    if construction == "RESPREAD":
        k = gf.sum(axis=1).clip(lower=1e-12)
        return gf.div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return gf.div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def cagr(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    return eq.iloc[-1] ** (1 / yrs) - 1


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


def ols_r2(x, y):
    """Single-regressor OLS R2 and slope; nan-safe."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return np.nan, np.nan, len(x)
    b = np.polyfit(x, y, 1)
    yh = np.polyval(b, x)
    r2 = 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return float(r2), float(b[0]), len(x)


# ---------------------------------------------------------------- panels
def build_panels():
    """{name: (investable px, SPY series, characteristics dict)}."""
    out = {}
    u = load_universe()
    out["U56"] = (u.drop(columns=["SPY"]), u["SPY"], dict(kind="anchor", etf_share=np.nan,
                                                          width=u.shape[1] - 1, seed=-1,
                                                          q_target=np.nan))
    b = load_universe(broad=True)
    b_spy = b["SPY"]
    b_inv = b.drop(columns=["SPY"], errors="ignore")
    out["B136"] = (b_inv, b_spy, dict(kind="anchor", etf_share=np.nan,
                                      width=b_inv.shape[1], seed=-1, q_target=np.nan))
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_inv = s[[c for c in s.columns if c != "SPY" and c not in bad]]
    out["SMALL439"] = (s_inv, s["SPY"], dict(kind="anchor", etf_share=0.0,
                                             width=s_inv.shape[1], seed=-1,
                                             q_target=np.nan))

    # ---- the fourth cut: ETF-share-controlled sub-panels of B136
    uni = __import__("json").loads((REPO / "research" / "universe.json").read_text())
    etf_pool = sorted(set(uni["broad"]) | set(uni["sectors"]) | set(uni["bonds_fx_commod"]))
    etfs = sorted([c for c in b_inv.columns if c in etf_pool])
    stocks = sorted([c for c in b_inv.columns if c not in etf_pool])
    out["U56"][2]["etf_share"] = len([c for c in out["U56"][0].columns if c in etf_pool]) \
        / out["U56"][0].shape[1]
    out["B136"][2]["etf_share"] = len(etfs) / b_inv.shape[1]

    for q in Q_LADDER:
        for W in W_LADDER:
            ne = int(round(q * W))
            ns = W - ne
            if ne > len(etfs) or ns > len(stocks):
                continue
            for sd in SEEDS:
                rng = np.random.default_rng(hash((int(q * 100), W, sd)) % (2 ** 32))
                pick = list(rng.choice(etfs, ne, replace=False)) if ne else []
                pick += list(rng.choice(stocks, ns, replace=False))
                pick = sorted(pick)
                nm = f"B{W}q{int(q * 100):02d}s{sd}"
                out[nm] = (b_inv[pick], b_spy,
                           dict(kind="cut", etf_share=ne / W, width=W, seed=sd, q_target=q))
    return out, len(bad), etfs, stocks


def panel_chars(px):
    """Characteristics measured on the panel itself (no book, no gate)."""
    r = px.pct_change()
    start = px.index[260]
    r = r.loc[start:]
    vol = (r.std() * np.sqrt(252)).mean()
    disp = r.std(axis=1).mean() * np.sqrt(252)
    C = r.iloc[-2520:].corr()
    iu = np.triu_indices_from(C.values, 1)
    rho = float(np.nanmean(C.values[iu]))
    live = live_mask(px).loc[start:]
    return dict(mean_vol=float(vol), xs_disp=float(disp), mean_rho=rho,
                n_live=float(live.sum(axis=1).mean()),
                yrs=len(px.loc[start:]) / 252)


# ---------------------------------------------------------------- main
def main():
    PN, n_dropped, etfs, stocks = build_panels()
    names = list(PN)

    P("=" * 180)
    P("Idea 555 does-the-TIMING-RESIDUAL-constant-survive-a-fourth-panel (cloud) | "
      + Path(__file__).name)
    P("=" * 180)
    P("QUESTION: idea 305's resid0 is -0.3375 (U56) / -0.4231 (B136) / -0.3817 (SMALL439) "
      "pp/yr.  Measured on a FOURTH cut - fresh")
    P("          ETF-share-controlled sub-panels of B136 - is it a GATE-FORM constant or "
      "does it track a panel characteristic?")
    P(f"PRE-REGISTERED  H_GATEFORM      : (1) fresh-cut R_p range <= 2 x anchor span "
      f"({BAR_RANGE:.4f} pp/yr) AND (2) no single panel")
    P(f"                                  characteristic reaches R2 {BAR_R2:.2f} on R_p "
      f"across all {len(names)} panels.")
    P("                H_CHARACTERISTIC: either clause fails -> resid0 tracks the panel, "
      "and the winning characteristic is named.")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), "
      f"gross {GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): panel ({len(names)} levels) x theta ({len(MA_THETA)} levels).  "
      f"cadence {CADENCES} is the published constant's OWN domain, reported at every")
    P("                 level and selected at none outside rule 8; x is a deterministic "
      "function of theta, not a dial.")
    P(f"grid: {len(names)} panels x {len(MA_THETA)} theta x {len(CADENCES)} cadences x "
      f"{len(FAMILIES)} families x {len(CONSTRUCTIONS)} constructions = "
      f"{len(names) * len(MA_THETA) * len(CADENCES) * len(FAMILIES) * len(CONSTRUCTIONS)} "
      f"books, ALL reported.")
    P(f"B136 pools: {len(etfs)} ETFs / {len(stocks)} single stocks.  Cuts: q "
      f"{Q_LADDER} x W {W_LADDER} x {len(SEEDS)} seeds = "
      f"{sum(1 for k in PN if PN[k][2]['kind'] == 'cut')} fresh panels.")
    P("SURVIVORSHIP: B136 / SMALL439 / every fresh cut are CURRENT constituents only - "
      "CAGR LEVELS inflated, arm-minus-arm resid0")
    P(f"              very largely immune, 4a/4b columns are NOT.  SMALL439 drops "
      f"{n_dropped} tickers with max_1d_move >= 1.0.")
    flush_log()

    # ---------------------------------------------------- G0: fast vs engine
    P("\n" + "=" * 180)
    P("G0 - fast_backtest vs engine.backtest (returns AND turnover), on the anchor "
      "panels, MA-THRESH theta 0.00 DEGROSS")
    P("=" * 180)
    g0_max = 0.0
    for pn in ANCHORS:
        px = PN[pn][0]
        w = book(px, ma_gate(px, 0.0), "DEGROSS")
        for cad in CADENCES:
            r_f, t_f, _ = fast_backtest(px, w, cad)
            eng = backtest(px, w, cost_bps=0.0, freq=cad)
            dr = float((r_f - eng["returns"]).abs().max())
            dt = float((t_f - eng["turnover"]).abs().max())
            g0_max = max(g0_max, dr, dt)
            P(f"  {pn:9s} {cad}: max|dret| {dr:.3e}  max|dturn| {dt:.3e}")
    P(f"G0 {'PASS' if g0_max < BAR_IDENT else 'FAIL'} (max {g0_max:.3e} < {BAR_IDENT:.0e})")
    flush_log()

    # ---------------------------------------------------- the live 4a comparand
    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, decomp, matched, pchars = [], [], [], []

    for pi, pn in enumerate(names):
        px, spy_px, meta = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        ch = panel_chars(px)
        pchars.append(dict(panel=pn, **meta, **ch,
                           spy_CAGR=spy_s["CAGR"], spy_Sharpe=spy_s["Sharpe"],
                           spy_MaxDD=spy_s["MaxDD"]))

        ctrl = {}
        for cad in CADENCES:
            r0c, tc, _ = fast_backtest(px, control_book(px), cad)
            r10c = (r0c - tc * COST_BPS / 1e4).loc[start:]
            ctrl[cad] = stat(r10c)

        live = live_mask(px).loc[start:]
        nlive = live.sum(axis=1)
        gates, xs = {}, {}
        for th in MA_THETA:
            gm = ma_gate(px, th)
            x = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gf = quantile_gate_frac(px, x)
            fq = float((gf.loc[start:].sum(axis=1) / nlive).mean())
            gates[th] = {"MA-THRESH": gm, "QUANTILE-F": gf}
            xs[th] = x
            matched.append(dict(panel=pn, theta=th, x=x, frac_ma=x, frac_q=fq,
                                d_frac=fq - x,
                                k_ma=float(gm.loc[start:].sum(axis=1).mean()),
                                k_q=float(gf.loc[start:].sum(axis=1).mean())))

        for th in MA_THETA:
            for cad in CADENCES:
                for fam in FAMILIES:
                    arms = {}
                    for con in CONSTRUCTIONS:
                        r0, turn, grs = fast_backtest(px, book(px, gates[th][fam], con), cad)
                        r0 = r0.loc[start:]
                        turn = turn.loc[start:]
                        grs = grs.loc[start:]
                        r10 = r0 - turn * COST_BPS / 1e4
                        s = stat(r10)
                        arms[con] = dict(r0=r0, gross=grs, s=s, turn=turn)
                        rows.append(dict(panel=pn, kind=meta["kind"],
                                         etf_share=meta["etf_share"], width=meta["width"],
                                         seed=meta["seed"], theta=th, x=xs[th], cad=cad,
                                         family=fam, con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=float(grs.mean()),
                                         turn_yr=float(turn.sum() / years),
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         dCAGR_ctrl=s["CAGR"] - ctrl[cad]["CAGR"],
                                         p4a=verdict_4a(s, live_s),
                                         f4b=fail_4b(s, spy_s)))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        sl = slice(lo, hi)
                        rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                        cb = float(c_t.loc[sl].mean())
                        g0 = 100 * (cagr(rd) - cagr(rr))
                        p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        decomp.append(dict(panel=pn, kind=meta["kind"],
                                           etf_share=meta["etf_share"],
                                           width=meta["width"], seed=meta["seed"],
                                           theta=th, cad=cad, family=fam, window=tag,
                                           ident_max_err=ident, c_bar=cb,
                                           c_sd=float(c_t.loc[sl].std()),
                                           gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                           CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd)))
        P(f"  [{pi + 1:2d}/{len(names)}] {pn:12s} width {px.shape[1]:3d} "
          f"etf_share {meta['etf_share']:.3f} done")
        if (pi + 1) % 5 == 0:
            flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    M = pd.DataFrame(matched)
    CH = pd.DataFrame(pchars)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    CH.to_csv(f"{OUT}.panels.csv", index=False)

    F = D[D.window == "FULL"]

    # ---------------------------------------------------- G1/G2/G3/R1
    P("\n" + "=" * 180)
    P("VALIDITY GATES (read before the headline)")
    P("=" * 180)
    g1 = float(F.ident_max_err.max())
    P(f"G1 DEGROSS/RESPREAD identity   : max {g1:.3e} (< {BAR_IDENT:.0e}) -> "
      f"{'PASS' if g1 < BAR_IDENT else 'FAIL'}")
    qres = F[F.family == "QUANTILE-F"].groupby("panel").resid0_pp.mean()
    g2 = float(qres.abs().max())
    G2_BAD = sorted(qres.index[qres.abs() >= BAR_Q_RESID])
    P(f"G2 |mean QUANTILE-F resid0|    : max {g2:.4f} pp/yr over {len(qres)} panels "
      f"(< {BAR_Q_RESID}) -> {'PASS' if g2 < BAR_Q_RESID else 'FAIL'}"
      f"   [worst {qres.abs().idxmax()} {qres[qres.abs().idxmax()]:+.4f}]")
    if G2_BAD:
        P(f"   G2-FAILING PANELS ({len(G2_BAD)}): "
          + ", ".join(f"{p} {qres[p]:+.4f}" for p in G2_BAD))
        P("   As pre-registered, these panels are EXCLUDED from the headline clauses and "
          "reported separately; nothing else is dropped.")
    g3 = float(M.d_frac.abs().max())
    P(f"G3 |d mask fraction| MA vs QF  : max {g3:.5f} (< {BAR_MASK}) -> "
      f"{'PASS' if g3 < BAR_MASK else 'FAIL'}")
    RP = F[F.family == "MA-THRESH"].groupby("panel").resid0_pp.mean()
    P("R1 REPRODUCTION of idea 305's published anchors (pp/yr):")
    r1_ok = True
    for pn in ANCHORS:
        d = abs(RP[pn] - R1[pn])
        r1_ok &= d < R1_TOL
        P(f"   {pn:9s} published {R1[pn]:+.4f}  this run {RP[pn]:+.4f}  |d| {d:.4f} "
          f"(< {R1_TOL}) -> {'PASS' if d < R1_TOL else 'FAIL'}")
    P(f"R1 {'PASS' if r1_ok else 'FAIL'}")
    gates_ok = (g1 < BAR_IDENT) and (g2 < BAR_Q_RESID) and (g3 < BAR_MASK) and r1_ok
    P(f"ALL GATES: {'PASS' if gates_ok else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------- the constant, per panel
    P("\n" + "=" * 180)
    P("R_p - MA-THRESH resid0 (pp/yr), FULL window, mean over 9 theta x 3 cadences, "
      "EVERY panel reported")
    P("=" * 180)
    CT = (F[F.family == "MA-THRESH"]
          .groupby(["panel"])
          .agg(R_p=("resid0_pp", "mean"), sd=("resid0_pp", "std"),
               lo=("resid0_pp", "min"), hi=("resid0_pp", "max"),
               c_bar=("c_bar", "mean"), c_sd=("c_sd", "mean"))
          .reset_index())
    CT = CT.merge(CH, on="panel")
    for cad in CADENCES:
        sub = (F[(F.family == "MA-THRESH") & (F.cad == cad)]
               .groupby("panel").resid0_pp.mean().rename(f"R_p_{cad}"))
        CT = CT.merge(sub, on="panel")
    for wtag in ("IS", "OOS"):
        sub = (D[(D.window == wtag) & (D.family == "MA-THRESH")]
               .groupby("panel").resid0_pp.mean().rename(f"R_p_{wtag}"))
        CT = CT.merge(sub, on="panel")
    CT = CT.sort_values(["kind", "q_target", "width", "seed"], na_position="first")
    CT["g2_ok"] = ~CT.panel.isin(G2_BAD)
    CT.to_csv(f"{OUT}.constant.csv", index=False)
    CTA = CT                     # all panels, reported
    CT = CT[CT.g2_ok]            # headline set (pre-registered exclusion)
    show = ["panel", "kind", "width", "etf_share", "R_p", "sd", "lo", "hi",
            "R_p_W", "R_p_M", "R_p_Q", "R_p_IS", "R_p_OOS", "c_bar", "c_sd",
            "mean_vol", "xs_disp", "mean_rho", "g2_ok"]
    P(fmt(CTA[show], 4))
    if G2_BAD:
        ex = CTA[~CTA.g2_ok]
        P(f"\n(headline set excludes {len(G2_BAD)} G2-failing panel(s): "
          + ", ".join(f"{r.panel} R_p {r.R_p:+.4f}" for r in ex.itertuples())
          + "; the exclusion is reported both ways below)")

    cuts = CT[CT.kind == "cut"]
    anc = CT[CT.kind == "anchor"]
    rng_cuts = float(cuts.R_p.max() - cuts.R_p.min())
    P("")
    P(f"ANCHORS   R_p: " + "  ".join(f"{r.panel} {r.R_p:+.4f}" for r in anc.itertuples())
      + f"   span {float(anc.R_p.max() - anc.R_p.min()):.4f} pp/yr")
    P(f"FRESH CUTS R_p: n {len(cuts)}  mean {cuts.R_p.mean():+.4f}  sd {cuts.R_p.std():.4f}  "
      f"min {cuts.R_p.min():+.4f} ({cuts.loc[cuts.R_p.idxmin(), 'panel']})  "
      f"max {cuts.R_p.max():+.4f} ({cuts.loc[cuts.R_p.idxmax(), 'panel']})")
    P(f"CLAUSE 1  fresh-cut range {rng_cuts:.4f} <= {BAR_RANGE:.4f} pp/yr -> "
      f"{'PASS' if rng_cuts <= BAR_RANGE else 'FAIL'}")
    ac = CTA[CTA.kind == "cut"]
    rng_all = float(ac.R_p.max() - ac.R_p.min())
    P(f"CLAUSE 1  (robustness, G2-failing panels INCLUDED, n {len(ac)}): range "
      f"{rng_all:.4f} -> {'PASS' if rng_all <= BAR_RANGE else 'FAIL'}")

    # per (q, W) cell
    P("\nfresh cuts by (ETF share target, width) - 6 seeds each:")
    cell = (cuts.groupby(["q_target", "width"])
            .agg(n=("R_p", "size"), mean=("R_p", "mean"), sd=("R_p", "std"),
                 lo=("R_p", "min"), hi=("R_p", "max"), c_bar=("c_bar", "mean"),
                 c_sd=("c_sd", "mean"), vol=("mean_vol", "mean"),
                 rho=("mean_rho", "mean")).reset_index())
    P(fmt(cell, 4))

    # ---------------------------------------------------- clause 2: characteristics
    P("\n" + "=" * 180)
    P(f"CLAUSE 2 - single-regressor OLS of R_p on each panel characteristic "
      f"({len(CT)} panels; anchors carry nan etf_share only where undefined)")
    P("=" * 180)
    CHARS = ["width", "etf_share", "c_bar", "c_sd", "mean_vol", "xs_disp", "mean_rho",
             "n_live", "yrs", "spy_MaxDD"]
    reg = []
    for c in CHARS:
        for scope, sub in (("ALL", CT), ("CUTS", cuts), ("ALLwG2", CTA)):
            for ycol, ytag in (("R_p", "FULL"), ("R_p_IS", "IS"), ("R_p_OOS", "OOS")):
                r2, slope, n = ols_r2(sub[c], sub[ycol])
                reg.append(dict(char=c, scope=scope, window=ytag, R2=r2, slope=slope, n=n))
    RG = pd.DataFrame(reg)
    P(fmt(RG.pivot_table(index="char", columns=["scope", "window"], values="R2"), 4))
    P("\nslopes (pp/yr per unit of characteristic):")
    P(fmt(RG.pivot_table(index="char", columns=["scope", "window"], values="slope"), 4))
    main_r2 = RG[(RG.scope == "ALL") & (RG.window == "FULL")].set_index("char").R2
    best = main_r2.idxmax()
    P(f"\nCLAUSE 2  best single characteristic (ALL panels, FULL): {best} "
      f"R2 {main_r2.max():.4f} <= {BAR_R2} -> "
      f"{'PASS' if main_r2.max() <= BAR_R2 else 'FAIL'}")
    RG.to_csv(f"{OUT}.regressions.csv", index=False)

    c1 = rng_cuts <= BAR_RANGE
    c2 = main_r2.max() <= BAR_R2
    VERDICT = "H_GATEFORM" if (c1 and c2) else "H_CHARACTERISTIC"
    P(f"\nHEADLINE: clause 1 {'PASS' if c1 else 'FAIL'}, clause 2 "
      f"{'PASS' if c2 else 'FAIL'} -> {VERDICT}")
    flush_log()

    # ---------------------------------------------------- WF-B: does it walk forward?
    P("\n" + "=" * 180)
    P("WF-B (rule 8) - does the constant walk forward?  IS = ..2016-12-31 chooses, "
      "OOS = 2017-01-01.. read once.  Nothing is fitted.")
    P("=" * 180)
    pooled_is = float(CT.R_p_IS.mean())
    wf = []
    for r in CT.itertuples():
        wf.append(dict(panel=r.panel, kind=r.kind, IS=r.R_p_IS, OOS=r.R_p_OOS,
                       err_perpanel=abs(r.R_p_OOS - r.R_p_IS),
                       err_pooled=abs(r.R_p_OOS - pooled_is),
                       err_zero=abs(r.R_p_OOS)))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"pooled IS constant = {pooled_is:+.4f} pp/yr (mean over all {len(CT)} panels)")
    for scope, sub in (("ALL", WF), ("ANCHORS", WF[WF.kind == "anchor"]),
                       ("CUTS", WF[WF.kind == "cut"])):
        P(f"  {scope:8s} n {len(sub):2d} | OOS MAE  per-panel-IS {sub.err_perpanel.mean():.4f}"
          f"  pooled-IS {sub.err_pooled.mean():.4f}  zero {sub.err_zero.mean():.4f}"
          f"  | mean IS {sub.IS.mean():+.4f} -> mean OOS {sub.OOS.mean():+.4f}"
          f"  | corr(IS,OOS) {sub[['IS', 'OOS']].corr().iloc[0, 1]:+.4f}")
    P("  reading: the estimator with the LOWEST OOS MAE is the one the record should quote.")
    P(fmt(WF, 4))
    flush_log()

    # ---------------------------------------------------- WF-A + KEEP paths
    P("\n" + "=" * 180)
    P("WF-A (rule 8) - theta chosen on IS Sharpe per (panel, family, construction, "
      "cadence); OOS read once vs RULES v2 (live), SPY and the no-gate EWall control")
    P("=" * 180)
    wfa = []
    for (pn, fam, con, cad), sub in G.groupby(["panel", "family", "con", "cad"]):
        pick = sub.loc[sub.isSharpe.idxmax()]
        px, spy_px, meta = PN[pn]
        start = px.index[260]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        r0c, tc, _ = fast_backtest(px, control_book(px), cad)
        ctl = stat((r0c - tc * COST_BPS / 1e4).loc[start:])
        wfa.append(dict(panel=pn, kind=meta["kind"], family=fam, con=con, cad=cad,
                        theta_IS=pick.theta, isSharpe=pick.isSharpe,
                        oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                        ctl_oCAGR=ctl["oCAGR"], ctl_oSharpe=ctl["oSharpe"],
                        ctl_oMaxDD=ctl["oMaxDD"],
                        spy_oCAGR=spy_s["oCAGR"], spy_oSharpe=spy_s["oSharpe"],
                        spy_oMaxDD=spy_s["oMaxDD"],
                        live_oCAGR=live_s["oCAGR"], live_oSharpe=live_s["oSharpe"],
                        live_oMaxDD=live_s["oMaxDD"],
                        beats_ctl=pick.oSharpe > ctl["oSharpe"],
                        beats_spy=pick.oSharpe > spy_s["oSharpe"],
                        beats_live=pick.oSharpe > live_s["oSharpe"],
                        p4a=pick.p4a, f4b=pick.f4b))
    WA = pd.DataFrame(wfa)
    WA.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(fmt(WA.groupby(["kind", "family", "con", "cad"])
          .agg(n=("oSharpe", "size"), oSharpe=("oSharpe", "mean"),
               ctl=("ctl_oSharpe", "mean"), spy=("spy_oSharpe", "mean"),
               live=("live_oSharpe", "mean"), beats_ctl=("beats_ctl", "mean"),
               beats_spy=("beats_spy", "mean"), beats_live=("beats_live", "mean"),
               p4a=("p4a", "sum")).reset_index(), 4))

    P("\n" + "=" * 180)
    P("KEEP PATHS over the FULL grid (both paths, every book)")
    P("=" * 180)
    P(f"4a passes: {int(G.p4a.sum())} of {len(G)}   4b passes: {int(G.p4b.sum())} of {len(G)}")
    P("4b failing-bar frequency (first-listed bars per row, SET semantics):")
    fb = G.f4b.str.split(",").explode().value_counts()
    P(fmt(fb.to_frame("rows").T, 0))
    if G.p4b.any():
        P("\n4b passers (all reported):")
        P(fmt(G[G.p4b][["panel", "kind", "theta", "cad", "family", "con", "CAGR",
                        "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]], 4))
    if G.p4a.any():
        P("\n4a passers (all reported):")
        P(fmt(G[G.p4a][["panel", "kind", "theta", "cad", "family", "con", "CAGR",
                        "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]], 4))

    # ---------------------------------------------------- verdict
    P("\n" + "=" * 180)
    P("VERDICT")
    P("=" * 180)
    P(f"GATES: G0 {'PASS' if g0_max < BAR_IDENT else 'FAIL'}  G1 "
      f"{'PASS' if g1 < BAR_IDENT else 'FAIL'}  G2 "
      f"{'PASS' if g2 < BAR_Q_RESID else 'FAIL'}  G3 "
      f"{'PASS' if g3 < BAR_MASK else 'FAIL'}  R1 {'PASS' if r1_ok else 'FAIL'}")
    P(f"CLAUSE 1 (range)  fresh-cut R_p range {rng_cuts:.4f} vs bar {BAR_RANGE:.4f} -> "
      f"{'PASS' if c1 else 'FAIL'}")
    P(f"CLAUSE 2 (R2)     best characteristic {best} R2 {main_r2.max():.4f} vs bar "
      f"{BAR_R2:.2f} -> {'PASS' if c2 else 'FAIL'}")
    P(f"=> {VERDICT}")
    P(f"WF-B  OOS MAE: per-panel-IS {WF.err_perpanel.mean():.4f} | pooled-IS "
      f"{WF.err_pooled.mean():.4f} | zero {WF.err_zero.mean():.4f}")
    P("KEEP: no book is promoted on this run - it is a decomposition study on "
      "survivorship-inflated panels; 4a/4b columns are reported for PROTOCOL compliance.")
    flush_log()


if __name__ == "__main__":
    main()
