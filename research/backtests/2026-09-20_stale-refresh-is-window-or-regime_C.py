#!/usr/bin/env python3
"""Idea 1789 (lane C, 2026-09-20): IS THE STALE-REFRESH PREFERENCE AN IS-WINDOW FACT OR A
REGIME FACT?

THE DEFECT THIS CLOSES.  Idea 1767 separated the VOLTGT book's TRADE cadence T (how often the
names are re-spread) from its REFRESH cadence R (how old the gross scalar g = clip(t/sigma20,0,1)
is when applied), and found something uncomfortable: on the rule-8 window every one of four legal
IS-only choosers picked a STALE scalar -- R = M or Q -- on 2009-2016, and the picks then failed
the 4b drawdown cap out of sample (U56 t=0.16: C_ISSHARPE/C_ISCALMAR/C_ISDD/C_ISLEGS all pick
T=Q,R=M, OOS MaxDD -23.96% vs the memo's weekly -19.86%).  The record read that as "IS-only
choosers cannot find the fresh scalar".  But there is a cheaper explanation that has never been
tested: 2009-2016 contains NO deep equity drawdown (post-GFC recovery, the 2011 and 2015-16
corrections and nothing worse), and a stale exposure scalar only costs money WHEN VOL SPIKES.  If
so the chooser is not blind -- rule 8's FIXED window simply never shows it the event that prices
staleness, and the same chooser on a window containing a real drawdown would prefer a FRESH
scalar.

THE CONSTRUCTION.  The T x R cross of idea 1767 is reproduced EXACTLY (same two-schedule runner,
same panels, same targets, same costs); nothing about the book moves.  The axis under test is the
IS WINDOW the chooser is allowed to see:
  CONTROL 2x2 (lengths differ by construction, never pooled with SLID): the slid family moves
      TWO things at once -- as it slides forward it ACQUIRES the 2020 crash and DROPS 2009-2012 --
      so X1 2009-2019 (early, no crash), X2 2009-2020 (early, crash), X3 2013-2019 (late, no
      crash), X4 2017-2020 (late, crash) separate CRASH-PRESENCE from RECENCY.
  SLID FAMILY, IS LENGTH HELD FIXED AT 8 YEARS (so window LENGTH cannot confound the comparison):
      W0 2009-2016 (rule 8's own window), W1 2010-2017, W2 2011-2018, W3 2012-2019,
      W4 2013-2020, W5 2014-2021.
  AS NAMED in the idea text (9-year windows, reported separately and NOT pooled with the slid
      family because their length differs): N1 2010-2018, N2 2012-2020.
  Each window's OOS is everything strictly after its IS end, read ONCE per window.
W4 / W5 / N2 contain the Feb-Mar 2020 crash; W0 / W1 / N1 contain no drawdown deeper than the
2015-16 correction.  If the stale preference is an IS-WINDOW fact it inverts across that line.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  TRADE cadence     T in {D, W, M, Q}
  DIAL 2  REFRESH cadence   R in {D, W, M, Q}
REPORTED AXES, not tuned, every point published to `.grid.csv`:
  PANEL {U56, B136, SMALL}, TARGET t {0.12, 0.16}, COST {0, 10, 25, 50} bps reconstructed off the
  cost-0 leg, IS WINDOW {W0..W5, N1, N2}.  4 x 4 x 3 x 2 x 4 = 384 scored books, all published;
  8 windows x 3 panels x 2 targets x 4 choosers = 192 chooser picks, all published.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) WINDOW FACT: the stale share of IS-only picks falls materially on the drawdown-containing
      windows (W4/W5/N2) relative to W0/W1/N1 -> rule 8's fixed window is what makes staleness
      look free, and the record's "choosers cannot find the fresh scalar" wording is wrong.
  (b) REGIME FACT / chooser fact: the stale share does NOT move with the window's drawdown ->
      the preference is a property of the IS statistic, not of the sample it is computed on, and
      1767's reading stands.
  (c) The T-CONDITIONAL read (for each panel x target x T, which R maximises IS Sharpe) is
      reported alongside the joint pick as the larger-sample version of the same question
      (24 picks per window instead of 8).
  (d) Whatever the preference does, the SIGN OF THE TRUTH is reported too: the fresh-minus-stale
      Sharpe and MaxDD difference measured INSIDE each window and AFTER it, so a chooser that is
      "wrong" can be told apart from a chooser that is right about its own window.
All are reported; the 8 windows overlap heavily, so any rank correlation between window drawdown
depth and stale share is quoted DESCRIPTIVELY with no p-value -- overlapping samples make an
independence test invalid and none is claimed.

GATES.  G0 sigma20(t) is a TRAILING window closing at t (no look-ahead).  G1 the two-schedule
runner == `engine.backtest` on returns AND turnover whenever T == R.  G2 the cost identity
r(c) = r0 - turnover*c/1e4 == the engine at 10 and 25 bps.  G3 CROSS-RUN: window W0 reproduces
idea 1767's published chooser picks and OOS numbers exactly (that IS rule 8's window).  G4 a
REFRESH row moves every held name by ONE common factor.  G5 SMALL's `max_1d_move >= 1.0` drop
applied and counted.  G6 exactly two tuned dials.  G7 every chooser statistic for window Wk reads
ONLY rows inside Wk (asserted by date, per window).  G8 every cell and every pick published.
G9 no RNG.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps headline, no leverage -- g capped at 1.00 -- no
shorting); rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, 2 dials); rule 8
(walk-forward -- W0 IS 2009-2016 chooses, 2017-2026 read once -- reported in full as the headline
walk-forward); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL is a CURRENT sub-$2B screen
(every ticker with `max_1d_move >= 1.0` in `data/small_meta.csv` dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The window-to-window contrasts are same-tape, same-names, same-book comparisons with only the
chooser's visible window moved, and are first-order immune; the pass COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_stale-refresh-is-window-or-regime_C.py
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-20", "stale-refresh-is-window-or-regime"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.12, 0.16]
TGT0 = 0.16
CADS = ["D", "W", "M", "Q"]
FRESH, STALE = {"D", "W"}, {"M", "Q"}
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

# IS windows.  family "SLID" holds length fixed at 8 calendar years; "NAMED" are the idea's own
# two 9-year windows, reported but never pooled with SLID.
WINDOWS = [("W0", "2009-01-01", "2016-12-31", "SLID"),
           ("W1", "2010-01-01", "2017-12-31", "SLID"),
           ("W2", "2011-01-01", "2018-12-31", "SLID"),
           ("W3", "2012-01-01", "2019-12-31", "SLID"),
           ("W4", "2013-01-01", "2020-12-31", "SLID"),
           ("W5", "2014-01-01", "2021-12-31", "SLID"),
           ("N1", "2010-01-01", "2018-12-31", "NAMED"),
           ("N2", "2012-01-01", "2020-12-31", "NAMED"),
           # CONTROL 2x2: does the preference follow the CRASH or merely the RECENCY of the
           # window?  The slid family confounds them (as it slides forward it both ACQUIRES the
           # 2020 crash and DROPS 2009-2012).  These four break the confound; their lengths
           # differ by construction, so they are never pooled with SLID.
           ("X1", "2009-01-01", "2019-12-31", "CTRL_early_nocrash"),
           ("X2", "2009-01-01", "2020-12-31", "CTRL_early_crash"),
           ("X3", "2013-01-01", "2019-12-31", "CTRL_late_nocrash"),
           ("X4", "2017-01-01", "2020-12-31", "CTRL_late_crash")]
IS_END, OOS_START = "2016-12-31", "2017-01-01"        # rule 8's own window (== W0)

# idea 1767's published W0 chooser picks and OOS numbers (its `_choosers.csv`), for G3
PUB_PICKS = {("U56", 0.16, "C_ISSHARPE"): ("T=Q,R=M", 0.1681, 1.2184, -0.2396),
             ("U56", 0.12, "C_ISSHARPE"): ("T=Q,R=M", 0.1566, 1.2979, -0.2083),
             ("B136", 0.16, "C_ISDD"): ("T=Q,R=W", 0.1563, 1.2020, -0.1862),
             ("B136", 0.12, "C_ISLEGS"): ("T=W,R=W", 0.1386, 1.2217, -0.1601),
             ("SMALL", 0.16, "C_ISSHARPE"): ("T=D,R=M", 0.0648, 0.4539, -0.4018)}

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------- panels
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in pxs.columns if c in bad])
    return ([("U56", px56, list(px56.columns)),        # live convention: SPY IS a constituent
             ("B136", px136, list(px136.columns)),
             ("SMALL", pxs, small_cols)],              # SPY is the benchmark only
            dropped)


def panel_sigma20(px, cols):
    """Annualised 20d realised vol of the UNLEVERED equal-weight panel portfolio, through t's
    close (idea 1767's and the standing memo's convention; the engine applies at t+1)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    return pr.rolling(20).std() * np.sqrt(252)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


# ----------------------------------------------------------------------- two-schedule runner
def bt_two(px, EW, G, mT, mR):
    """idea 1767's runner verbatim: the book carries a CURRENT SCALAR g_eff read off g_t ONLY on a
    REFRESH day (schedule R); on a TRADE day (schedule T) the names are re-spread to g_eff * ew_t;
    on a refresh-only day the book is scaled by ONE common factor.  Decisions at t applied at t+1.
    T == R reproduces the standard book exactly (G1)."""
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    W = np.nan_to_num(EW.values, nan=0.0)
    g = np.nan_to_num(G.values, nan=0.0)
    W = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])
    g = np.concatenate([[0.0], g[:-1]])
    aT = np.concatenate([[False], np.asarray(mT, bool)[:-1]])
    aR = np.concatenate([[False], np.asarray(mR, bool)[:-1]])
    n = len(R)
    cur = np.zeros(R.shape[1])
    held = np.empty_like(R)
    turn = np.zeros(n)
    g_eff = g[0]
    nref = 0
    refmax = 0.0
    for i in range(n):
        if aR[i] or i == 0:
            g_eff = g[i]
        if aT[i] or i == 0:
            new = W[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif aR[i]:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                nz = cur > 0
                if nz.any():
                    f = new[nz] / cur[nz]
                    refmax = max(refmax, float(f.max() - f.min()))
                nref += 1
                cur = new
        held[i] = cur
        gr = cur * (1.0 + R[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (pd.Series((held * R).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index), nref, refmax)


def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    if not len(r):
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


def spearman(a, b):
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    return float(np.corrcoef(ra, rb)[0, 1])


# ----------------------------------------------------------------------- run
def main():
    log(f"# Idea 1789 (lane C, {DATE}) — is the STALE-REFRESH PREFERENCE an IS-WINDOW fact or a "
        f"REGIME fact?")
    log(f"# dials: TRADE cadence T {CADS} x REFRESH cadence R {CADS} | reported: panel "
        f"{{U56,B136,SMALL}}, target {TARGETS}, cost {COSTS} bps, IS window "
        f"{[w[0] for w in WINDOWS]} | warm-up {WARMUP}")
    log("# no RNG is used anywhere in this script (G9)")

    PS, dropped = panels()
    gate("G5 SMALL max_1d_move>=1.0 drop", f"{dropped} tickers dropped", "drop applied", dropped > 0)
    gate("G6 tuned dials", "TRADE cadence T, REFRESH cadence R (the IS WINDOW is the reported "
                           "axis under test, not a dial)", "exactly 2", True)
    for nm, px, cols in PS:
        log(f"# panel {nm}: {len(cols)} held names ({px.shape[1]} columns), "
            f"{px.index[0].date()} -> {px.index[-1].date()} ({len(px)} rows, {len(px)/252:.1f}y)")

    rows, BASE, RET = [], {}, {}
    g1r = g1t = g2 = g0 = 0.0
    g4max, g4n = 0.0, 0

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        EW = eq_weight(px, cols)
        SIG = panel_sigma20(px, cols)

        # ---- G0: sigma20(t) is a trailing window closing at t ------------------------
        if pname == "U56":
            sub = px[cols]
            e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
            ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            pr = (ew.shift(1) * sub.pct_change()).sum(axis=1).values
            k = 800
            g0 = abs(float(np.std(pr[k - 19:k + 1], ddof=1) * np.sqrt(252)) - float(SIG.iloc[k]))
            gate("G0 sigma20(t) == trailing std(r[t-19..t])", f"|d| = {g0:.3e} at t=800",
                 "< 1e-12", g0 < 1e-12)

        # ---- baselines: live RULES v2 (weekly) and SPY --------------------------------
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        mw_ = rebalance_mask(px.index, "W").values
        lr, lt, _, _, _ = bt_two(px, lw, pd.Series(1.0, index=px.index), mw_, mw_)
        lr, lt = lr.loc[st:], lt.loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st, spy_r=spy, live_r={c: net(lr, lt, c) for c in COSTS},
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1])
        BASE[pname] = B
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"# {pname}: LIVE RULES v2 (W, {COST0}bps) {L['full']['CAGR']:.2%} / "
            f"{L['full']['Sharpe']:.4f} / {L['full']['MaxDD']:.2%} (rule-8 OOS "
            f"{L['oos']['CAGR']:.2%} / {L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:.2%}) | SPY "
            f"{S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:.2%} "
            f"(rule-8 OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        # ---- G1 / G2 on the diagonal ---------------------------------------------------
        if pname in ("U56", "B136"):
            Gp = (TGT0 / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = EW.mul(Gp, axis=0).fillna(0.0)
            a, at, _, _, _ = bt_two(px, EW, Gp, mw_, mw_)
            b = engine_backtest(px, Wfull, cost_bps=0.0, freq="W")
            g1r = max(g1r, float(np.abs(a.values - b["returns"].values).max()))
            g1t = max(g1t, float(np.abs(at.values - b["turnover"].values).max()))
            for c in (10, 25):
                eb = engine_backtest(px, Wfull, cost_bps=float(c), freq="W")["returns"]
                g2 = max(g2, float(np.abs(net(a, at, c).values - eb.values).max()))

        # ---- the grid -------------------------------------------------------------------
        for tgt in TARGETS:
            Gp = (tgt / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            for T in CADS:
                mT = rebalance_mask(px.index, T).values
                for Rc in CADS:
                    mR = rebalance_mask(px.index, Rc).values
                    r0, t0, gs, nref, refmax = bt_two(px, EW, Gp, mT, mR)
                    if nref:
                        g4max = max(g4max, refmax)
                        g4n += nref
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    yrs = len(r0) / 252.0
                    for c in COSTS:
                        r = net(r0, t0, c)
                        RET[(pname, tgt, T, Rc, c)] = r
                        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                        h1, h2 = halves(r)
                        S = B["spy"]
                        mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
                               "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
                               "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
                               "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
                        bl, nbad = binding(mar)
                        LV = B[f"live{c}"]
                        k4bf = (h1 > S["h1"] and h2 > S["h2"]
                                and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                        rows.append(dict(
                            panel=pname, target=tgt, T_trade=T, R_refresh=Rc, cost=c,
                            refresh_class=("FRESH" if Rc in FRESH else "STALE"),
                            diag=(T == Rc), n_refresh=nref,
                            turn_py=float(t0.sum() / yrs), gross_mean=float(gs.mean()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **mar, bind=bl, n_fail=nbad,
                            keep4b_full=bool(k4bf), keep4b_oos=bool(k4bo),
                            keep4b=bool(k4bf and mar["L3_OOS"] > 0 and k4bo),
                            keep4a=bool(h1 > LV["h1"] and h2 > LV["h2"]
                                        and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                            keep4a_oos=bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                            and mo["MaxDD"] >= LV["oos"]["MaxDD"]),
                        ))

    gate("G1 two-schedule runner == engine.backtest on the diagonal",
         f"returns {g1r:.3e}, turnover {g1t:.3e}", "< 1e-12", g1r < 1e-12 and g1t < 1e-12)
    gate("G2 cost identity r(c)=r0-turn*c/1e4", f"max|d| = {g2:.3e}", "< 1e-15", g2 < 1e-15)
    gate("G4 a REFRESH row moves every held name by ONE common factor",
         f"{g4n} refresh rows, max spread of per-name factors {g4max:.3e}", "< 1e-12",
         g4max < 1e-12 and g4n > 0)

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G8a every book cell published", f"{len(df)} rows -> {Path(OUT).name}.grid.csv", "384",
         len(df) == 384)

    # ================================================================ THE WINDOW AXIS
    log("")
    log("## WINDOW DESCRIPTION — what each IS window actually contains (SPY and the unlevered "
        "equal-weight panel, inside the window)")
    WDESC = {}
    for wl, ws, we, fam in WINDOWS:
        d = {}
        for pname, _, _ in PS:
            B = BASE[pname]
            sr = B["spy_r"].loc[ws:we]
            d[pname] = dict(n=len(sr), spy_dd=mets(sr)["MaxDD"], spy_sh=mets(sr)["Sharpe"],
                            oos_n=len(B["spy_r"].loc[pd.Timestamp(we) + pd.Timedelta(days=1):]))
        WDESC[wl] = d
        u = d["U56"]
        log(f"  {wl} [{fam}] {ws[:7]}..{we[:7]}  IS {u['n']:5d} rows ({u['n']/252:.1f}y)  "
            f"SPY IS MaxDD {u['spy_dd']:7.2%}  SPY IS Sharpe {u['spy_sh']:6.3f}  |  OOS "
            f"{u['oos_n']:5d} rows ({u['oos_n']/252:.1f}y)")

    # ---- G7: per-window date containment -------------------------------------------------
    g7ok, g7msg = True, []
    for wl, ws, we, fam in WINDOWS:
        r = RET[("U56", TGT0, "W", "W", COST0)].loc[ws:we]
        if not (r.index[0] >= pd.Timestamp(ws) and r.index[-1] <= pd.Timestamp(we)):
            g7ok = False
        g7msg.append(f"{wl}:{r.index[0].date()}..{r.index[-1].date()}")
    gate("G7 every chooser statistic for window Wk reads ONLY rows inside Wk",
         " ".join(g7msg), "each slice inside its own window", g7ok)

    # ---- choosers, per window ------------------------------------------------------------
    CHN = ["C_ISSHARPE", "C_ISCALMAR", "C_ISDD", "C_ISLEGS"]
    ch_rows = []
    for wl, ws, we, fam in WINDOWS:
        oos_start = (pd.Timestamp(we) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        for pname, _, _ in PS:
            B = BASE[pname]
            spy_is = B["spy_r"].loc[ws:we]
            spy_oo = B["spy_r"].loc[oos_start:]
            SI, SO = mets(spy_is), mets(spy_oo)
            sh1, sh2 = halves(spy_is)
            liv_oo = mets(B["live_r"][COST0].loc[oos_start:])
            cells = [(T, Rc) for T in CADS for Rc in CADS]
            for tgt in TARGETS:
                stats = {}
                for T, Rc in cells:
                    r = RET[(pname, tgt, T, Rc, COST0)]
                    ri, ro = r.loc[ws:we], r.loc[oos_start:]
                    mi, mo = mets(ri), mets(ro)
                    ih1, ih2 = halves(ri)
                    legs = (int(ih1 > sh1) + int(ih2 > sh2) + int(mi["Sharpe"] > SI["Sharpe"])
                            + int(mi["MaxDD"] >= DD_CAP * SI["MaxDD"])
                            + int(mi["CAGR"] >= CAGR_FLOOR * SI["CAGR"]) + mi["Sharpe"] / 1e6)
                    stats[(T, Rc)] = dict(
                        is_Sharpe=mi["Sharpe"], is_CAGR=mi["CAGR"], is_MaxDD=mi["MaxDD"],
                        is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
                        is_legs=legs, oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                        oos_MaxDD=mo["MaxDD"],
                        k4b_oos=bool(mo["Sharpe"] > SO["Sharpe"]
                                     and mo["MaxDD"] >= DD_CAP * SO["MaxDD"]
                                     and mo["CAGR"] >= CAGR_FLOOR * SO["CAGR"]),
                        k4a_oos=bool(mo["Sharpe"] > liv_oo["Sharpe"]
                                     and mo["MaxDD"] >= liv_oo["MaxDD"]))
                key = {"C_ISSHARPE": lambda s: s["is_Sharpe"],
                       "C_ISCALMAR": lambda s: s["is_Calmar"],
                       "C_ISDD": lambda s: s["is_MaxDD"],
                       "C_ISLEGS": lambda s: s["is_legs"]}
                # joint (T,R) pick
                for cn in CHN:
                    pk = max(cells, key=lambda k: key[cn](stats[k]))
                    s = stats[pk]
                    ch_rows.append(dict(window=wl, family=fam, is_start=ws, is_end=we,
                                        oos_start=oos_start, panel=pname, target=tgt, chooser=cn,
                                        scope="JOINT", T_pick=pk[0], R_pick=pk[1],
                                        refresh_class="FRESH" if pk[1] in FRESH else "STALE",
                                        oos_CAGR=s["oos_CAGR"], oos_Sharpe=s["oos_Sharpe"],
                                        oos_MaxDD=s["oos_MaxDD"], keep4b_oos=s["k4b_oos"],
                                        keep4a_oos=s["k4a_oos"],
                                        spy_oos_Sharpe=SO["Sharpe"], spy_oos_MaxDD=SO["MaxDD"],
                                        spy_oos_CAGR=SO["CAGR"]))
                # T-conditional pick over R only (the larger-sample version, finding (c))
                for T in CADS:
                    for cn in CHN:
                        pk = max([(T, Rc) for Rc in CADS], key=lambda k: key[cn](stats[k]))
                        s = stats[pk]
                        ch_rows.append(dict(window=wl, family=fam, is_start=ws, is_end=we,
                                            oos_start=oos_start, panel=pname, target=tgt,
                                            chooser=cn, scope=f"T={T}", T_pick=pk[0],
                                            R_pick=pk[1],
                                            refresh_class="FRESH" if pk[1] in FRESH else "STALE",
                                            oos_CAGR=s["oos_CAGR"], oos_Sharpe=s["oos_Sharpe"],
                                            oos_MaxDD=s["oos_MaxDD"], keep4b_oos=s["k4b_oos"],
                                            keep4a_oos=s["k4a_oos"],
                                            spy_oos_Sharpe=SO["Sharpe"],
                                            spy_oos_MaxDD=SO["MaxDD"], spy_oos_CAGR=SO["CAGR"]))
                # fresh-minus-stale truth, inside the window and after it (finding (d))
                for T in CADS:
                    fr = [stats[(T, Rc)] for Rc in sorted(FRESH)]
                    stl = [stats[(T, Rc)] for Rc in sorted(STALE)]
                    ch_rows.append(dict(window=wl, family=fam, is_start=ws, is_end=we,
                                        oos_start=oos_start, panel=pname, target=tgt,
                                        chooser="TRUTH_FRESH_minus_STALE", scope=f"T={T}",
                                        T_pick=T, R_pick="-", refresh_class="-",
                                        d_is_Sharpe=np.mean([s["is_Sharpe"] for s in fr])
                                                    - np.mean([s["is_Sharpe"] for s in stl]),
                                        d_is_MaxDD=np.mean([s["is_MaxDD"] for s in fr])
                                                   - np.mean([s["is_MaxDD"] for s in stl]),
                                        d_oos_Sharpe=np.mean([s["oos_Sharpe"] for s in fr])
                                                     - np.mean([s["oos_Sharpe"] for s in stl]),
                                        d_oos_MaxDD=np.mean([s["oos_MaxDD"] for s in fr])
                                                    - np.mean([s["oos_MaxDD"] for s in stl])))
    ch = pd.DataFrame(ch_rows)
    ch.to_csv(f"{OUT}.choosers.csv", index=False)
    J = ch[(ch.scope == "JOINT") & (ch.chooser != "TRUTH_FRESH_minus_STALE")]
    TC = ch[(ch.scope.str.startswith("T=")) & (ch.chooser != "TRUTH_FRESH_minus_STALE")]
    TR = ch[ch.chooser == "TRUTH_FRESH_minus_STALE"]
    gate("G8b every chooser pick published",
         f"{len(J)} joint + {len(TC)} T-conditional + {len(TR)} truth rows -> "
         f"{Path(OUT).name}.choosers.csv",
         f"{len(WINDOWS)*24} joint, {len(WINDOWS)*96} T-conditional",
         len(J) == len(WINDOWS) * 24 and len(TC) == len(WINDOWS) * 96)

    # ---- G3 cross-run against idea 1767's published W0 picks -----------------------------
    mx, bad = 0.0, []
    for (pn, tg, cn), (pick, oc, os_, od) in PUB_PICKS.items():
        q = J[(J.window == "W0") & (J.panel == pn) & (J.target == tg) & (J.chooser == cn)].iloc[0]
        got = f"T={q.T_pick},R={q.R_pick}"
        if got != pick:
            bad.append(f"{pn}/{tg}/{cn}: {got} != {pick}")
        mx = max(mx, abs(oc - q.oos_CAGR), abs(os_ - q.oos_Sharpe), abs(od - q.oos_MaxDD))
    gate("G3 cross-run: window W0 reproduces idea 1767's published picks and OOS numbers",
         f"pick mismatches {bad if bad else 0}; max|d| on OOS stats = {mx:.3e}",
         "0 mismatches, < 5e-4 (1767 quotes 4 dp)", not bad and mx < 5e-4)

    # ================================================================ THE ANSWER
    log("")
    log("## THE HEADLINE — STALE share of legal IS-only picks by IS WINDOW "
        f"({COST0} bps; JOINT = argmax over all 16 (T,R) cells, 8 picks per window; "
        "T-COND = argmax over R holding T, 32 picks per window)")
    log("   window  IS span            SPY IS MaxDD   JOINT stale   T-COND stale   "
        "picks' OOS 4b pass")
    hl = []
    for wl, ws, we, fam in WINDOWS:
        j = J[J.window == wl]
        t = TC[TC.window == wl]
        js = (j.refresh_class == "STALE").mean()
        ts = (t.refresh_class == "STALE").mean()
        dd = WDESC[wl]["U56"]["spy_dd"]
        hl.append(dict(window=wl, family=fam, is_start=ws, is_end=we, spy_is_MaxDD=dd,
                       joint_stale=js, tcond_stale=ts,
                       joint_n=len(j), tcond_n=len(t),
                       joint_4b_oos=float(j.keep4b_oos.mean()),
                       joint_4a_oos=float(j.keep4a_oos.mean()),
                       oos_years=WDESC[wl]["U56"]["oos_n"] / 252.0))
        log(f"   {wl} [{fam[:4]}] {ws[:7]}..{we[:7]}     {dd:7.2%}      "
            f"{int((j.refresh_class=='STALE').sum()):2d}/{len(j)} = {js:5.1%}   "
            f"{int((t.refresh_class=='STALE').sum()):3d}/{len(t)} = {ts:5.1%}      "
            f"{int(j.keep4b_oos.sum())}/{len(j)}")
    H = pd.DataFrame(hl)
    H.to_csv(f"{OUT}.windows.csv", index=False)

    sl = H[H.family == "SLID"]
    log("")
    log(f"  SLID family only (8y IS length held fixed, n = {len(sl)} windows, HEAVILY OVERLAPPING "
        f"— no p-value is quoted or claimed):")
    log(f"    rank corr( SPY IS MaxDD , JOINT stale share )  = "
        f"{spearman(sl.spy_is_MaxDD, sl.joint_stale):+.3f}   "
        f"(a POSITIVE value means a SHALLOWER IS drawdown goes with MORE stale picks)")
    log(f"    rank corr( SPY IS MaxDD , T-COND stale share ) = "
        f"{spearman(sl.spy_is_MaxDD, sl.tcond_stale):+.3f}")
    pre = sl[sl.window.isin(["W0", "W1", "W2", "W3"])]      # no COVID inside IS
    post = sl[sl.window.isin(["W4", "W5"])]                 # COVID inside IS
    log(f"    NO-CRASH windows W0-W3  JOINT stale {pre.joint_stale.mean():5.1%}   "
        f"T-COND stale {pre.tcond_stale.mean():5.1%}")
    log(f"    CRASH windows   W4-W5   JOINT stale {post.joint_stale.mean():5.1%}   "
        f"T-COND stale {post.tcond_stale.mean():5.1%}")
    log(f"    NAMED N1 (no crash) JOINT {float(H[H.window=='N1'].joint_stale.iloc[0]):5.1%} | "
        f"NAMED N2 (crash)    JOINT {float(H[H.window=='N2'].joint_stale.iloc[0]):5.1%}")

    log("")
    log("## THE CONTROL 2x2 — is the carrier the CRASH or merely the RECENCY of the window?")
    log("   (the slid family confounds the two; these four do not.  lengths differ and are "
        "printed, so read the 2x2, not the levels)")
    log("              NO CRASH in IS                          CRASH in IS")
    def _c(w):
        r = H[H.window == w].iloc[0]
        return (f"{w} {r.is_start[:4]}-{r.is_end[:4]} ({(pd.Timestamp(r.is_end)-pd.Timestamp(r.is_start)).days/365.25:.0f}y) "
                f"IS_DD {r.spy_is_MaxDD:6.1%} stale {r.joint_stale:5.1%}")
    log(f"   EARLY  {_c('X1'):48s}  {_c('X2')}")
    log(f"   LATE   {_c('X3'):48s}  {_c('X4')}")
    xc = H[H.family.str.startswith('CTRL')]
    crash = xc[xc.family.str.endswith('crash') & ~xc.family.str.endswith('nocrash')]
    nocrash = xc[xc.family.str.endswith('nocrash')]
    early = xc[xc.family.str.contains('early')]
    late = xc[xc.family.str.contains('late')]
    log(f"   MAIN EFFECT of CRASH-PRESENCE  {crash.joint_stale.mean():5.1%} (crash) vs "
        f"{nocrash.joint_stale.mean():5.1%} (no crash)   -> {100*(crash.joint_stale.mean()-nocrash.joint_stale.mean()):+.1f} pp")
    log(f"   MAIN EFFECT of RECENCY         {late.joint_stale.mean():5.1%} (late)  vs "
        f"{early.joint_stale.mean():5.1%} (early)      -> {100*(late.joint_stale.mean()-early.joint_stale.mean()):+.1f} pp")

    log("")
    log("## THE TRUTH THE CHOOSER IS TRYING TO SEE — FRESH minus STALE, measured INSIDE each "
        f"window and AFTER it (mean over panel x target x T, {COST0} bps)")
    log("   window   d(IS Sharpe)  d(IS MaxDD)   d(post Sharpe)  d(post MaxDD)")
    tr_rows = []
    for wl, ws, we, fam in WINDOWS:
        t = TR[TR.window == wl]
        r = dict(window=wl, family=fam, d_is_Sharpe=t.d_is_Sharpe.mean(),
                 d_is_MaxDD=t.d_is_MaxDD.mean(), d_oos_Sharpe=t.d_oos_Sharpe.mean(),
                 d_oos_MaxDD=t.d_oos_MaxDD.mean())
        tr_rows.append(r)
        log(f"   {wl} [{fam[:4]}]  {r['d_is_Sharpe']:+8.4f}     {r['d_is_MaxDD']:+7.2%}      "
            f"{r['d_oos_Sharpe']:+8.4f}       {r['d_oos_MaxDD']:+7.2%}")
    pd.DataFrame(tr_rows).to_csv(f"{OUT}.truth.csv", index=False)
    log("   (a NEGATIVE d(IS Sharpe) with a POSITIVE d(IS MaxDD) is exactly the trade the stale "
        "scalar offers: slightly better Sharpe, worse drawdown — so a Sharpe chooser picks STALE)")

    log("")
    log("## BOTH KEEP PATHS over all 384 book cells (full sample, rule-8 OOS)")
    log(f"  4b FULL {int(df.keep4b_full.sum())} | 4b OOS {int(df.keep4b_oos.sum())} | "
        f"4b (all five legs) {int(df.keep4b.sum())} | 4a {int(df.keep4a.sum())} | "
        f"4a OOS {int(df.keep4a_oos.sum())}  of {len(df)}")
    for pname, _, _ in PS:
        for tgt in TARGETS:
            q = df[(df.panel == pname) & (df.target == tgt)]
            log(f"  {pname:6s} t={tgt:.2f}  4b {int(q.keep4b.sum()):2d}/{len(q)}   "
                f"4a {int(q.keep4a.sum()):2d}/{len(q)}   binding: "
                + "  ".join(f"{k} {int((~(q[k]>0)).sum()):2d}" for k in LEGS))
    log("  4b pass share by REFRESH class at 10 bps (pooled over panels, targets, T):")
    for cls, cads in (("FRESH", sorted(FRESH)), ("STALE", sorted(STALE))):
        q = df[(df.cost == COST0) & (df.R_refresh.isin(cads))]
        log(f"    R {cls:5s} ({'/'.join(cads)})  4b {int(q.keep4b.sum()):2d}/{len(q)}   "
            f"4b OOS {int(q.keep4b_oos.sum()):2d}/{len(q)}   4a {int(q.keep4a.sum()):2d}/{len(q)}"
            f"   mean OOS MaxDD {q.oos_MaxDD.mean():7.2%}")

    # ---- RULE 8, the protocol's own walk-forward ------------------------------------------
    log("")
    log("## RULE 8 WALK-FORWARD (the protocol's own window W0: parameters chosen on 2009-2016 "
        "ONLY, 2017-2026 read once) — the headline table")
    wf = []
    for pname, _, _ in PS:
        B = BASE[pname]
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"\n  {pname}   LIVE RULES v2 OOS {L['oos']['CAGR']:7.2%} / {L['oos']['Sharpe']:7.4f} "
            f"/ {L['oos']['MaxDD']:8.2%}   SPY OOS {S['oos']['CAGR']:7.2%} / "
            f"{S['oos']['Sharpe']:7.4f} / {S['oos']['MaxDD']:8.2%}")
        for tgt in TARGETS:
            for cn in CHN:
                q = J[(J.window == "W0") & (J.panel == pname) & (J.target == tgt)
                      & (J.chooser == cn)].iloc[0]
                wf.append(dict(panel=pname, target=tgt, chooser=cn,
                               pick=f"T={q.T_pick},R={q.R_pick}",
                               refresh_class=q.refresh_class, oos_CAGR=q.oos_CAGR,
                               oos_Sharpe=q.oos_Sharpe, oos_MaxDD=q.oos_MaxDD,
                               keep4b_oos=q.keep4b_oos, keep4a_oos=q.keep4a_oos,
                               base_oos_Sharpe=L["oos"]["Sharpe"], base_oos_CAGR=L["oos"]["CAGR"],
                               base_oos_MaxDD=L["oos"]["MaxDD"], spy_oos_Sharpe=S["oos"]["Sharpe"],
                               spy_oos_CAGR=S["oos"]["CAGR"], spy_oos_MaxDD=S["oos"]["MaxDD"]))
                log(f"    t={tgt:.2f} {cn:11s} -> T={q.T_pick},R={q.R_pick} [{q.refresh_class}] "
                    f"OOS {q.oos_CAGR:7.2%} / {q.oos_Sharpe:7.4f} / {q.oos_MaxDD:8.2%}   "
                    f"4bOOS {'Y' if q.keep4b_oos else '.'}  4aOOS {'Y' if q.keep4a_oos else '.'}")
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- the same walk-forward at every OTHER window (the axis under test) ---------------
    log("")
    log("## THE SAME WALK-FORWARD AT EVERY OTHER IS WINDOW (each window's OOS read once; note "
        "later windows have SHORTER and EASIER OOS spans — lengths are printed)")
    for wl, ws, we, fam in WINDOWS:
        if wl == "W0":
            continue
        j = J[J.window == wl]
        log(f"\n  {wl} [{fam}] IS {ws[:7]}..{we[:7]} -> OOS {j.oos_start.iloc[0][:7]}.. "
            f"({WDESC[wl]['U56']['oos_n']/252:.1f}y)")
        for pname, _, _ in PS:
            q = j[j.panel == pname]
            so = q.spy_oos_Sharpe.iloc[0]
            log(f"    {pname:6s} SPY OOS Sharpe {so:6.4f} / MaxDD {q.spy_oos_MaxDD.iloc[0]:7.2%}"
                f"   picks: " + "  ".join(
                    f"{r.chooser[5:]}@t{r.target:.2f}=R{r.R_pick}({'F' if r.refresh_class=='FRESH' else 'S'},"
                    f"{r.oos_Sharpe:.2f},{r.oos_MaxDD:.1%})" for _, r in q.iterrows()))

    ok = sum(1 for g in _gates if g["pass_"])
    log(f"\n# GATES {ok} of {len(_gates)} PASS")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
