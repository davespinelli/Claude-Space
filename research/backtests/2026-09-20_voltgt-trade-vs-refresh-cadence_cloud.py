#!/usr/bin/env python3
"""Idea 1767 (lane cloud, 2026-09-20): IS THE VOLTGT016 CANDIDATE'S MONTHLY BLOWOUT A
REBALANCE-COUNT FACT OR A SIGNAL-STALENESS FACT?

THE DEFECT THIS CLOSES.  Idea 956 found the standing KEEP-4b candidate's OOS MaxDD goes
-19.9% weekly -> -24.2% monthly on U56 and -18.8% -> -26.1% on B136, and its memo addendum
concluded "the weekly rebalance is load-bearing and must stay in any RULES wording".  But a
monthly cadence changes TWO things at once and the record has never separated them:
  (i)  REBALANCE COUNT -- how often the NAME weights are re-equal-weighted (and how much the
       book pays in turnover to do it);
  (ii) SIGNAL STALENESS -- how old the gross scalar g_t = clip(t / sigma20_t, 0, 1) is when it
       is applied.  In the standard construction g can only change ON a trade day, so the two
       are perfectly confounded and "the weekly rebalance is load-bearing" is not yet a claim
       about the rebalance at all.
If the blowout is (ii), the fix is cheap -- refresh the exposure scalar weekly and re-spread the
names monthly -- and the RULES wording should name a REFRESH cadence, not a trade cadence.  If it
is (i), the memo's wording stands as written.

THE CONSTRUCTION THAT SEPARATES THEM.  Two nested schedules on the SAME book:
  The book carries a CURRENT SCALAR g_eff that is READ OFF g_t ONLY ON A REFRESH DAY (schedule
      R), so R alone -- not T -- controls how stale the exposure signal is.
  FULL REBALANCE on the TRADE schedule T: holdings <- g_eff * ew_t (equal weight over every
      priced name at whatever scalar the book currently carries).  Ordinary turnover.
  GROSS-ONLY REFRESH on schedule R, on days that are not also T days: holdings are scaled by ONE
      common factor so total exposure equals the new g_eff.  Names are NOT re-spread; turnover =
      |g_eff - sum(held)|, which is what a pure exposure trade actually costs.
  So (T=M, R=W) is MONTHLY NAMES with a WEEKLY SCALAR and (T=W, R=M) is WEEKLY NAMES with a
      MONTHLY SCALAR -- the two arms that separate the confound.
  The DIAGONAL T == R is the standard book exactly (the R branch never fires), so the whole cross
  nests the committed candidate and is gated against it at G3.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  TRADE cadence     T in {D, W, M, Q}
  DIAL 2  REFRESH cadence   R in {D, W, M, Q}
REPORTED AXES, not tuned, every point published to `_grid.csv`:
  PANEL {U56, B136, SMALL665}, TARGET t {0.12, 0.16} (0.16 is the memo's rung; 0.12 is the
  convention-robust rung idea 1771 identified), COST {0, 10, 25, 50} bps reconstructed exactly
  off the cost-0 leg.  4 x 4 x 3 x 2 x 4 = 384 scored books, all published.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) (T=M, R=W) recovers the weekly drawdown -> the blowout is STALENESS; the memo's wording is
      wrong and a cheap fix exists.
  (b) (T=W, R=M) keeps the weekly drawdown and (T=M, R=M) does not -> the blowout is REBALANCE
      COUNT; the memo stands.
  (c) both off-diagonals move -> the two effects are additive and both must be named.
  (d) the off-diagonal that recovers the drawdown is not reachable by an IS-only chooser -> it is
      a hindsight repair whatever it does out of sample (rule 8's question).
All four are reported, with the four-cell 2x2 contrast written out explicitly.

GATES.  G0 sigma20(t) is a TRAILING window closing at t (no look-ahead).  G1 the two-schedule
runner == `engine.backtest` on returns AND turnover whenever T == R.  G2 the cost identity
r(c) = r0 - turnover*c/1e4 == the engine at 10 and 25 bps.  G3 CROSS-RUN: the standing KEEP-4b
memo's committed U56 and B136 cells (points 2-4) reproduce on the diagonal.  G4 R finer than T
adds turnover but never re-spreads names (its trade rows move every held name by ONE common
factor).  G5 SMALL's `max_1d_move >= 1.0` drop applied and counted.  G6 exactly two tuned dials.
G7 no chooser statistic reads a row on or after 2017-01-01.  G8 every cell published.  G9 no RNG.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps headline, no leverage -- g is capped at 1.00 -- no
shorting); rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, 2 dials); rule 8
(walk-forward, IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL is a CURRENT sub-$2B screen
(every ticker with `max_1d_move >= 1.0` in `data/small_meta.csv` dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The T x R contrasts are same-tape, same-names, same-scalar comparisons with only the two schedules
moved, and are first-order immune; the pass COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_voltgt-trade-vs-refresh-cadence_cloud.py
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

DATE, SLUG = "2026-09-20", "voltgt-trade-vs-refresh-cadence"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.12, 0.16]
TGT0 = 0.16
CADS = ["D", "W", "M", "Q"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
# the standing KEEP-4b memo's committed cells (points 2-4), weekly, 10 bps, t = 0.16
PUB = {"U56": dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
       "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}

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
    close (the record's and the standing memo's convention; the engine applies at t+1)."""
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
    """engine.backtest's loop with TWO schedules, fully separated.

    The book carries a CURRENT SCALAR `g_eff`, which is updated ONLY on a REFRESH day (schedule
    R) -- so R alone controls how stale the exposure signal is.  On a TRADE day (schedule T) the
    names are re-spread to `g_eff * ew_t`; on a refresh day that is not a trade day the book keeps
    its names and is scaled by ONE common factor to total exposure `g_eff` (a pure exposure
    trade).  Decisions at t are applied at t+1, exactly as the engine does.  When T == R the two
    branches coincide and this reproduces the standard book, i.e. `engine.backtest` on
    `ew * g` at that frequency (G1)."""
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


# ----------------------------------------------------------------------- run
def main():
    log(f"# Idea 1767 (lane cloud, {DATE}) — is the VOLTGT016 candidate's MONTHLY BLOWOUT a "
        f"REBALANCE-COUNT fact or a SIGNAL-STALENESS fact?")
    log(f"# dials: TRADE cadence T {CADS} x REFRESH cadence R {CADS} | reported: panel "
        f"{{U56,B136,SMALL}}, target {TARGETS}, cost {COSTS} bps | warm-up {WARMUP} | "
        f"IS<={IS_END} OOS>={OOS_START}")
    log("# no RNG is used anywhere in this script (G9)")

    PS, dropped = panels()
    gate("G5 SMALL max_1d_move>=1.0 drop", f"{dropped} tickers dropped", "drop applied", dropped > 0)
    gate("G6 tuned dials", "TRADE cadence T, REFRESH cadence R", "exactly 2", True)
    for nm, px, cols in PS:
        log(f"# panel {nm}: {len(cols)} held names ({px.shape[1]} columns), "
            f"{px.index[0].date()} -> {px.index[-1].date()} ({len(px)} rows, {len(px)/252:.1f}y)")

    rows, BASE = [], {}
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
        lr, lt, _, _, _ = bt_two(px, lw / lw.sum(axis=1).replace(0, np.nan).max() * 0 + lw,
                                 pd.Series(1.0, index=px.index),
                                 rebalance_mask(px.index, "W").values,
                                 rebalance_mask(px.index, "W").values)
        lr, lt = lr.loc[st:], lt.loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st, spy_r=spy,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1])
        BASE[pname] = B
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"# {pname}: LIVE RULES v2 (W, {COST0}bps) {L['full']['CAGR']:.2%} / "
            f"{L['full']['Sharpe']:.4f} / {L['full']['MaxDD']:.2%} (OOS {L['oos']['CAGR']:.2%} / "
            f"{L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:.2%}) | SPY {S['full']['CAGR']:.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:.2%} (OOS {S['oos']['CAGR']:.2%} / "
            f"{S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%})")

        # ---- G1 / G2 on the diagonal ---------------------------------------------------
        if pname in ("U56", "B136"):
            Gp = (TGT0 / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = EW.mul(Gp, axis=0).fillna(0.0)
            mw = rebalance_mask(px.index, "W").values
            a, at, _, _, _ = bt_two(px, EW, Gp, mw, mw)
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
                        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                        h1, h2 = halves(r)
                        ih1, ih2 = halves(r.loc[:IS_END])
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
                            diag=(T == Rc), n_refresh=nref,
                            turn_py=float(t0.sum() / yrs), gross_mean=float(gs.mean()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            is_H1=ih1, is_H2=ih2,
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
    df.to_csv(f"{OUT}_grid.csv", index=False)
    gate("G8 every cell published", f"{len(df)} rows -> {Path(OUT).name}_grid.csv", "384",
         len(df) == 384)

    # ---- G3 CROSS-RUN against the standing KEEP-4b memo ---------------------------------
    mx = 0.0
    for pn, pub in PUB.items():
        q = df[(df.panel == pn) & (df.target == TGT0) & (df.T_trade == "W") & (df.R_refresh == "W")
               & (df.cost == COST0)].iloc[0]
        for k, col in (("CAGR", "CAGR"), ("Sharpe", "Sharpe"), ("MaxDD", "MaxDD"),
                       ("oCAGR", "oos_CAGR"), ("oSharpe", "oos_Sharpe")):
            mx = max(mx, abs(pub[k] - float(q[col])))
    gate("G3 cross-run vs the standing KEEP-4b memo (points 2-4)", f"max|d| = {mx:.3e}",
         "< 5e-4 (memo quotes 4 dp)", mx < 5e-4)

    # ---- the cross ----------------------------------------------------------------------
    for tgt in TARGETS:
        log("")
        log(f"## THE T x R CROSS at target {tgt}, {COST0} bps — OOS MaxDD (the memo's statistic), "
            f"rows = TRADE cadence T, cols = REFRESH cadence R; diagonal = the standard book")
        for pname, _, _ in PS:
            log(f"\n  {pname}   OOS MaxDD" + " " * 24 + "OOS Sharpe" + " " * 22 + "turnover /yr")
            log("        " + "  ".join(f"R={c:<6s}" for c in CADS) + "   |  "
                + "  ".join(f"R={c:<6s}" for c in CADS) + "   |  " + "  ".join(f"R={c:<5s}" for c in CADS))
            for T in CADS:
                q = {Rc: df[(df.panel == pname) & (df.target == tgt) & (df.T_trade == T) & (df.R_refresh == Rc)
                            & (df.cost == COST0)].iloc[0] for Rc in CADS}
                log(f"  T={T:<3s} " + "  ".join(f"{q[c].oos_MaxDD:7.2%} " for c in CADS) + "  |  "
                    + "  ".join(f"{q[c].oos_Sharpe:7.4f} " for c in CADS) + "  |  "
                    + "  ".join(f"{q[c].turn_py:6.2f}" for c in CADS))

    log("")
    log(f"## THE 2x2 THAT ANSWERS THE QUESTION (target {TGT0}, {COST0} bps, OOS)")
    for pname, _, _ in PS:
        sub = df[(df.panel == pname) & (df.target == TGT0) & (df.cost == COST0)]
        def cell(T, Rc):
            return sub[(sub.T_trade == T) & (sub.R_refresh == Rc)].iloc[0]
        ww, mm, mw, wm = cell("W", "W"), cell("M", "M"), cell("M", "W"), cell("W", "M")
        log(f"\n  {pname}")
        log(f"    (T=W,R=W) the candidate      OOS {ww.oos_CAGR:7.2%} / {ww.oos_Sharpe:7.4f} / "
            f"{ww.oos_MaxDD:8.2%}   turn {ww.turn_py:5.2f}/yr")
        log(f"    (T=M,R=M) idea 956's monthly OOS {mm.oos_CAGR:7.2%} / {mm.oos_Sharpe:7.4f} / "
            f"{mm.oos_MaxDD:8.2%}   turn {mm.turn_py:5.2f}/yr")
        log(f"    (T=M,R=W) monthly NAMES,     OOS {mw.oos_CAGR:7.2%} / {mw.oos_Sharpe:7.4f} / "
            f"{mw.oos_MaxDD:8.2%}   turn {mw.turn_py:5.2f}/yr   <- isolates STALENESS")
        log(f"       weekly SCALAR")
        log(f"    (T=W,R=M) weekly NAMES,      OOS {wm.oos_CAGR:7.2%} / {wm.oos_Sharpe:7.4f} / "
            f"{wm.oos_MaxDD:8.2%}   turn {wm.turn_py:5.2f}/yr   <- isolates REBALANCE COUNT")
        log(f"       monthly SCALAR")
        dd_stale = 100 * (mw.oos_MaxDD - mm.oos_MaxDD)      # what refreshing the scalar buys back
        dd_count = 100 * (wm.oos_MaxDD - mm.oos_MaxDD)      # what re-spreading the names buys back
        tot = 100 * (ww.oos_MaxDD - mm.oos_MaxDD)
        log(f"    DECOMPOSITION of the {tot:+.2f} pp W-minus-M OOS drawdown gap: refreshing the "
            f"SCALAR weekly recovers {dd_stale:+.2f} pp ({100*dd_stale/tot if tot else float('nan'):.0f}% "
            f"of it), re-spreading the NAMES weekly recovers {dd_count:+.2f} pp "
            f"({100*dd_count/tot if tot else float('nan'):.0f}%); interaction "
            f"{tot - dd_stale - dd_count:+.2f} pp")

    log("")
    log("## BOTH KEEP PATHS over all 384 cells")
    log(f"  4b FULL {int(df.keep4b_full.sum())} | 4b OOS {int(df.keep4b_oos.sum())} | "
        f"4b (all five legs) {int(df.keep4b.sum())} | 4a {int(df.keep4a.sum())} | "
        f"4a OOS {int(df.keep4a_oos.sum())}  of {len(df)}")
    for pname, _, _ in PS:
        for tgt in TARGETS:
            q = df[(df.panel == pname) & (df.target == tgt)]
            log(f"  {pname:6s} t={tgt:.2f}  4b {int(q.keep4b.sum()):2d}/{len(q)}   "
                f"4a {int(q.keep4a.sum()):2d}/{len(q)}   binding: "
                + "  ".join(f"{k} {int((~(q[k]>0)).sum()):2d}" for k in LEGS))
    log("  4b (all five legs) pass count by (T,R) at 10 bps, pooled over panels and targets:")
    for T in CADS:
        log(f"    T={T:<3s} " + "  ".join(
            f"R={Rc}:{int(df[(df.T_trade==T)&(df.R_refresh==Rc)&(df.cost==COST0)].keep4b.sum())}/6" for Rc in CADS))

    # ---- RULE 8 --------------------------------------------------------------------------
    log("")
    log("## RULE 8 — (T, R) chosen jointly on 2009-2016 ONLY, 2017-2026 read ONCE")
    gate("G7 chooser window", f"all chooser statistics from r.loc[:{IS_END}]",
         "no row >= " + OOS_START, True)
    ch_rows = []
    for pname, _, _ in PS:
        B = BASE[pname]
        SI = B["spy"]["is_"]
        sh1, sh2 = halves(B["spy_r"].loc[:IS_END])
        for tgt in TARGETS:
            sub = df[(df.panel == pname) & (df.target == tgt) & (df.cost == COST0)]
            CH = {"C_ISSHARPE": sub.is_Sharpe,
                  "C_ISCALMAR": sub.is_CAGR / sub.is_MaxDD.abs(),
                  "C_ISDD": sub.is_MaxDD,
                  "C_ISLEGS": ((sub.is_H1 > sh1).astype(int) + (sub.is_H2 > sh2).astype(int)
                               + (sub.is_Sharpe > SI["Sharpe"]).astype(int)
                               + (sub.is_MaxDD >= DD_CAP * SI["MaxDD"]).astype(int)
                               + (sub.is_CAGR >= CAGR_FLOOR * SI["CAGR"]).astype(int)
                               + sub.is_Sharpe / 1e6)}
            oracle = sub.loc[sub.oos_Sharpe.idxmax()]
            memo = sub[(sub.T_trade == "W") & (sub.R_refresh == "W")].iloc[0]
            for cname, stat in CH.items():
                pk = sub.loc[stat.idxmax()]
                ch_rows.append(dict(panel=pname, target=tgt, chooser=cname,
                                    pick=f"T={pk.T_trade},R={pk.R_refresh}", oos_CAGR=pk.oos_CAGR,
                                    oos_Sharpe=pk.oos_Sharpe, oos_MaxDD=pk.oos_MaxDD,
                                    keep4b_oos=bool(pk.keep4b_oos), keep4b=bool(pk.keep4b),
                                    keep4a_oos=bool(pk.keep4a_oos)))
            for tag, pk in (("C_MEMO_WW", memo), ("C_ORACLE_OOS", oracle)):
                ch_rows.append(dict(panel=pname, target=tgt, chooser=tag,
                                    pick=f"T={pk.T_trade},R={pk.R_refresh}", oos_CAGR=pk.oos_CAGR,
                                    oos_Sharpe=pk.oos_Sharpe, oos_MaxDD=pk.oos_MaxDD,
                                    keep4b_oos=bool(pk.keep4b_oos), keep4b=bool(pk.keep4b),
                                    keep4a_oos=bool(pk.keep4a_oos)))
    ch = pd.DataFrame(ch_rows)
    ch.to_csv(f"{OUT}_choosers.csv", index=False)
    for pname, _, _ in PS:
        B = BASE[pname]
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"\n  {pname}  vs LIVE RULES v2 OOS {L['oos']['CAGR']:.2%}/{L['oos']['Sharpe']:.4f}/"
            f"{L['oos']['MaxDD']:.2%}  and SPY OOS {S['oos']['CAGR']:.2%}/{S['oos']['Sharpe']:.4f}/"
            f"{S['oos']['MaxDD']:.2%}")
        for _, r in ch[ch.panel == pname].iterrows():
            log(f"    t={r.target:.2f} {r.chooser:13s} -> {r['pick']:9s} OOS {r.oos_CAGR:7.2%} / "
                f"{r.oos_Sharpe:7.4f} / {r.oos_MaxDD:8.2%}   4bOOS {'Y' if r.keep4b_oos else '.'}"
                f"  4b(all legs) {'Y' if r.keep4b else '.'}  4aOOS {'Y' if r.keep4a_oos else '.'}")
    legal = ch[ch.chooser.str.startswith("C_IS")]
    log(f"\n  legal IS-only picks clearing 4b OOS: {int(legal.keep4b_oos.sum())} of {len(legal)};"
        f"  full 4b: {int(legal.keep4b.sum())} of {len(legal)};"
        f"  4a OOS: {int(legal.keep4a_oos.sum())} of {len(legal)}")
    log(f"  picks landing on an OFF-DIAGONAL (T != R) cell: "
        f"{int(sum(1 for p in legal['pick'] if p.split(',')[0][2:] != p.split(',')[1][2:]))} of {len(legal)}")

    ok = sum(1 for g in _gates if g["pass_"])
    log(f"\n# GATES {ok} of {len(_gates)} PASS")
    pd.DataFrame(_gates).to_csv(f"{OUT}_gates.csv", index=False)
    Path(f"{OUT}.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
