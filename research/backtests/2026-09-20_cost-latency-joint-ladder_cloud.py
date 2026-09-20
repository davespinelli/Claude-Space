#!/usr/bin/env python3
"""Idea 2046 (lane cloud, 2026-09-20) — DOES THE DUAL-PATH 4a PASS SURVIVE THE COST AND
LATENCY LADDERS JOINTLY?

THE DEFECT THIS PRICES.  Idea 2034 turned up the first cell in the vol-target family ever to
clear BOTH KEEP paths — `B136, VOLTGT t = 0.10, DRIFT refresh h = 0.08, trade weekly` — and the
record has since moved cost and latency on it only SEPARATELY: idea 2034 priced COST {0, 10, 25,
50} at t+1 (4a holds to 25, dies at 50) and idea 2054 priced DELAY {t+1, t+2} inside a wider
four-axis cross (4a 8/18 -> 0/18).  Neither walked the two ladders TOGETHER, and neither went
past t+2.  A rule you cannot execute same-week is not a rule you can run, so the honest question
is where in the JOINT (cost x latency) plane the 4a pass actually dies — and whether the joint
move is the sum of the two separate moves or worse.

WHAT IS PRICED HERE.  The full joint cross, on the whole vol-target corpus so the candidate is
never read alone:

    PANEL     {U56, B136, SMALL}            REPORTED
    TARGET    t in {0.08, 0.10, 0.12, 0.16, 0.20}                      [tuned dial 1, inherited]
    DIAL      DRIFT h in {0, .01, .02, .03, .05, .08, .12, .16, .20, .25}   [tuned dial 2,
              inherited]  +  CALENDAR R in {D, W, M, Q}   (the comparison family)
    CADENCE   W  (the candidate's own; held fixed — idea 2054 owns the cadence axis)
    PHASE     ENGINE (`engine.rebalance_mask`, the discovery convention; idea 2054 owns phase)
    DELAY     d in {1, 2, 3}   -> weights decided at close t are executed at close t+d  REPORTED
    COST      c in {10, 25, 50} bps                                                     REPORTED

  = 3 x 5 x 14 x 3 = 630 books, x 3 cost rungs = 1,890 scored cells.  t+3 has never been priced
  in this record at all.

EXACTLY TWO TUNED PARAMETERS (`t` and the dial), both inherited from ideas 1799 / 2034.  Delay,
cost, panel and family are REPORTED at every rung, never chosen.

THE BASELINES ARE HELD AT THE LIVE CONVENTION throughout (RULES v2 weekly t+1 at 10 bps, and SPY
buy-and-hold), because that is the book real capital is running: a slower, dearer idea must beat
the undelayed, cheap live book to be worth switching to.  Every 4b bar is SPY's.

PRE-STATED VERDICT RULES (fixed before the run):
  V1  WHERE DOES 4a DIE?  The candidate at all 3 x 3 = 9 joint points.  >= 80% keeping 4a ->
      ROBUST; <= 40% -> the joint ladder KILLS the 4a claim; in between -> PARTIAL.  The run
      names the binding leg and the failure mode at every one of the 9.
  V2  WHERE DOES 4b DIE?  Same 9 points, same bands.
  V3  IS THE JOINT MOVE ADDITIVE?  For each (c, d) the observed Sharpe move from the (10 bps,
      t+1) corner is compared with the additive prediction [move(c, t+1) + move(10, d)].  The
      INTERACTION is the residual.  Pre-stated: if |interaction| stays under 20% of the larger
      single-axis move, the two ladders can go on being priced separately; if it exceeds that,
      the record's separate ladders are not a substitute for the joint one.
  V4  RULE 8, 2017-2026 READ ONCE.  `t` and the dial chosen on 2009-2016 only by two legal
      IS-only choosers at every (panel x delay x cost x family) point; the OOS half is scored
      once.  How many legal picks clear 4b?  4a?  Land on the candidate?

PROTOCOL: rule 2 (10 bps headline, t+1 base case, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths and the binding leg at every cell); rule 5 (one
idea, deterministic, standalone); rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  The (cost x delay) CONTRASTS are same-tape / same-names / same-grid and first-order
immune to it; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_cost-latency-joint-ladder_cloud.py
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

DATE, SLUG = "2026-09-20", "cost-latency-joint-ladder"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [10, 25, 50]
COST0 = 10
DELAYS = [1, 2, 3]
DELAY0 = 1
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
REFRESH = ["D", "W", "M", "Q"]
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
T_TRADE = "W"
TGT_MEMO = 0.16
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0
V3_BAR = 0.20                       # pre-stated interaction tolerance (share of larger main move)

# the cell under stress: idea 2034's dual-path candidate, at its discovery settings
CAND = dict(panel="B136", target=0.10, family="DRIFT", h=0.08, T_trade="W")
# committed numbers this run must reproduce, at the precision of the committed artifact
PUB_CAND = dict(CAGR=0.1250962195302867, Sharpe=1.228631477106311,
                MaxDD=-0.1180752235695585, oCAGR=0.1300721924289238,
                oSharpe=1.2927878651902318, H1=1.3171143618077108, H2=1.1414896569837694)
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876)}

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


# ----------------------------------------------------------------------------- panels
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in pxs.columns if c in bad])
    return ([("U56", px56, list(px56.columns)),
             ("B136", px136, list(px136.columns)),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------- the two refresh runners (idea 1799 verbatim)
def bt_cal(px_ret, W0, g0, mT, mR):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1]); held = np.empty_like(px_ret); turn = np.zeros(n)
    g_eff = g0[0]; nref = 0
    for i in range(n):
        if mR[i] or i == 0:
            g_eff = g0[i]; nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff; turn[i] = np.abs(new - cur).sum(); cur = new
        elif mR[i]:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s); turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i]); tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


def bt_drift(px_ret, W0, g0, mT, h):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1]); held = np.empty_like(px_ret); turn = np.zeros(n)
    g_eff = g0[0]; nref = 0
    for i in range(n):
        trig = abs(g0[i] - cur.sum()) > h
        if trig or i == 0:
            g_eff = g0[i]; nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff; turn[i] = np.abs(new - cur).sum(); cur = new
        elif trig:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s); turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i]); tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


def lag(a, d):
    """Execution delay of d days on a decision series/array (axis 0)."""
    a = np.asarray(a)
    if not d:
        return a
    pad = np.zeros((d,) + a.shape[1:], dtype=a.dtype) if a.ndim > 1 else np.zeros(d, dtype=a.dtype)
    return np.concatenate([pad, a[:-d]])


class Book:
    """One panel, runnable at any (target, dial, delay)."""

    def __init__(self, px, cols):
        self.index = px.index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        self.EW = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.SIG = panel_sigma(px, cols)
        self.mask = {f: np.asarray(rebalance_mask(px.index, f).values, bool)
                     for f in ("D", "W", "M", "Q")}
        self.mask["D"] = np.ones(len(px.index), bool)

    def inputs(self, tgt, delay):
        W0 = lag(self.EW, delay)
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        g0 = lag(g, delay)
        M = {f: lag(self.mask[f], delay).astype(bool) for f in ("D", "W", "M", "Q")}
        return W0, g0, M

    def run(self, fam, tgt, dial, delay):
        W0, g0, M = self.inputs(tgt, delay)
        if fam == "CAL":
            r, t, gs, nref = bt_cal(self.R, W0, g0, M[T_TRADE], M[dial])
        else:
            r, t, gs, nref = bt_drift(self.R, W0, g0, M[T_TRADE], dial)
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)


# ----------------------------------------------------------------------------- metrics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna(); eq = (1 + r).cumprod(); yrs = len(r) / 252.0
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


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2046 (lane cloud, {DATE}) — does the DUAL-PATH 4a pass survive the COST and "
        f"LATENCY ladders JOINTLY?")
    log(f"# under stress: B136 VOLTGT-DRIFT t=0.10, h=0.08, trade weekly, ENGINE phase (idea 2034)")
    log(f"# TUNED (2, both inherited): t {TARGETS}; dial = DRIFT h {THRESH} | CAL R {REFRESH}")
    log(f"# REPORTED, not tuned: delay t+{DELAYS} (t+3 never priced in this record), "
        f"cost {COSTS} bps, panel, family.  cadence FIXED {T_TRADE}, phase FIXED = engine mask, "
        f"sigma FIXED (L={SIG_L}, d={SIG_D}).")
    log(f"# warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")
    log(f"# BASELINES HELD AT THE LIVE CONVENTION: RULES v2 weekly t+1 at {COST0} bps, and SPY.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    SPYP, LIVEP, START = {}, {}, {}
    for pname, px, cols in PS:
        st = px.index[WARMUP]; START[pname] = st
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lr = engine_backtest(px, lw, cost_bps=float(COST0), freq="W")["returns"].loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        SPYP[pname] = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]),
                           is_=mets(spy.loc[:IS_END]), h1=halves(spy)[0], h2=halves(spy)[1],
                           ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1])
        LIVEP[pname] = dict(full=mets(lr), oos=mets(lr.loc[OOS_START:]),
                            h1=halves(lr)[0], h2=halves(lr)[1])
        S, LV = SPYP[pname], LIVEP[pname]
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")
        log(f"   LIVE v2 (W, t+1, {COST0}bps) {LV['full']['CAGR']:7.2%} / "
            f"{LV['full']['Sharpe']:.4f} / {LV['full']['MaxDD']:7.2%}  (H1 {LV['h1']:.4f} "
            f"H2 {LV['h2']:.4f}; OOS {LV['oos']['CAGR']:7.2%} / {LV['oos']['Sharpe']:.4f} / "
            f"{LV['oos']['MaxDD']:7.2%})")
        log(f"   SPY                        {S['full']['CAGR']:7.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:7.2%}  (H1 {S['h1']:.4f} "
            f"H2 {S['h2']:.4f}; OOS {S['oos']['CAGR']:7.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:7.2%})")
        log(f"   4b bars: MaxDD >= {DD_CAP*S['full']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*S['full']['CAGR']:.2%}")

    rows = []
    gD0 = 0.0     # DRIFT h=0 vs CAL R=D agreement
    gGR = 0.0     # max gross
    for pname, px, cols in PS:
        st = START[pname]; bk = Book(px, cols)
        S, LV = SPYP[pname], LIVEP[pname]
        for tgt in TARGETS:
            for delay in DELAYS:
                calD = None
                for fam, dial in ([("CAL", Rc) for Rc in REFRESH]
                                  + [("DRIFT", h) for h in THRESH]):
                    r0, t0, gs, nref = bk.run(fam, tgt, dial, delay)
                    label = f"R={dial}" if fam == "CAL" else f"h={dial:.2f}"
                    if fam == "CAL" and dial == "D":
                        calD = (r0.values.copy(), t0.values.copy())
                    if fam == "DRIFT" and dial == 0.0 and calD is not None:
                        gD0 = max(gD0, float(np.abs(r0.values - calD[0]).max()),
                                  float(np.abs(t0.values - calD[1]).max()))
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    gGR = max(gGR, float(gs.max()))
                    yrs = len(r0) / 252.0
                    for c in COSTS:
                        r = net(r0, t0, c)
                        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                        h1, h2 = halves(r)
                        ih1, ih2 = halves(r.loc[:IS_END])
                        mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
                               "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
                               "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
                               "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
                        bl, nbad = binding(mar)
                        k4bf = all(mar[k] > 0 for k in LEGS)
                        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                        k4a = (h1 > LV["h1"] and h2 > LV["h2"]
                               and mf["MaxDD"] >= LV["full"]["MaxDD"])
                        k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"]
                                and mo["MaxDD"] >= LV["oos"]["MaxDD"])
                        why4a = ("none" if k4a else
                                 ("H1" if h1 <= LV["h1"] else
                                  ("H2" if h2 <= LV["h2"] else "MaxDD")))
                        is_minleg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                                        mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                                        mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
                        rows.append(dict(
                            panel=pname, target=tgt, delay=delay, cost=c, family=fam,
                            dial=str(dial), cell=label,
                            h=(dial if fam == "DRIFT" else np.nan),
                            R_refresh=(dial if fam == "CAL" else ""),
                            turn_py=float(t0.sum() / yrs), refresh_py=nref / (len(px) / 252.0),
                            gross_mean=float(gs.mean()), gross_max=float(gs.max()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            H1=h1, H2=h2, is_Sharpe=mi["Sharpe"], is_minleg=float(is_minleg),
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            bind=bl, n_fail=nbad, why4a=why4a,
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a, keep4a_oos=k4ao))
        log(f"   {pname}: grid done ({len([r for r in rows if r['panel']==pname])} scored rows)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    NB = len(G) // len(COSTS)

    # -------------------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 DRIFT h=0 == CALENDAR R=D at every (panel, t, delay)", f"{gD0:.3e}", "< 1e-12",
         gD0 < 1e-12)
    want = 3 * len(TARGETS) * 14 * len(DELAYS)
    gate("G2 the joint grid is complete", f"{NB} books / {len(G)} scored rows",
         f"== {want} books", NB == want)
    gate("G3 gross never levered", f"max gross {gGR:.6f}", "<= 1.0 + 1e-9", gGR <= 1.0 + 1e-9)
    q = G[(G.panel == "B136") & (G.target == 0.10) & (G.family == "DRIFT") & (G.h == 0.08)
          & (G.delay == DELAY0) & (G.cost == COST0)]
    g4 = np.nan
    if len(q):
        r = q.iloc[0]
        g4 = max(abs(r.CAGR - PUB_CAND["CAGR"]), abs(r.Sharpe - PUB_CAND["Sharpe"]),
                 abs(r.MaxDD - PUB_CAND["MaxDD"]), abs(r.oos_CAGR - PUB_CAND["oCAGR"]),
                 abs(r.oos_Sharpe - PUB_CAND["oSharpe"]), abs(r.H1 - PUB_CAND["H1"]),
                 abs(r.H2 - PUB_CAND["H2"]))
    gate("G4 reproduces idea 2034's dual-path candidate at (10 bps, t+1)",
         f"max|d| = {g4:.3e}", "< 1e-9", bool(g4 < 1e-9))
    g5 = 0.0
    for pn, pub in PUB_MEMO.items():
        z = G[(G.panel == pn) & (G.target == TGT_MEMO) & (G.family == "CAL")
              & (G.R_refresh == "W") & (G.delay == DELAY0) & (G.cost == COST0)]
        if len(z):
            r = z.iloc[0]
            g5 = max(g5, abs(r.CAGR - pub["CAGR"]), abs(r.Sharpe - pub["Sharpe"]),
                     abs(r.MaxDD - pub["MaxDD"]))
    gate("G5 reproduces the standing VOLTGT memo (U56 + B136)", f"max|d| = {g5:.3e}", "< 1e-3",
         g5 < 1e-3)
    K = ["panel", "target", "cost", "family", "cell"]
    s1 = G[G.delay == 1].set_index(K).sort_index().Sharpe
    s3 = G[G.delay == 3].set_index(K).sort_index().Sharpe
    gate("G6 the DELAY axis reaches t+3 and moves the book",
         f"mean |dSharpe| t+1 -> t+3 = {float((s3 - s1).abs().mean()):.4f}", "> 1e-4",
         float((s3 - s1).abs().mean()) > 1e-4)
    KB = ["panel", "target", "delay", "family", "cell"]            # one BOOK; cost varies inside
    mono = G.sort_values("cost").groupby(KB).CAGR.apply(
        lambda s: bool(np.all(np.diff(s.values) <= 1e-12)))
    gate("G7 net CAGR is monotone non-increasing in cost at every book",
         f"{int(mono.sum())}/{len(mono)} books", f"== {len(mono)}", int(mono.sum()) == len(mono))

    # ------------------------------------------------ V1 / V2: the candidate on the joint plane
    log("\n## V1 / V2 — THE CANDIDATE ON THE FULL JOINT (COST x DELAY) PLANE")
    CC = G[(G.panel == "B136") & (G.target == 0.10) & (G.family == "DRIFT")
           & (G.h == 0.08)].sort_values(["delay", "cost"]).copy()
    CC.to_csv(f"{OUT}.candidate.csv", index=False)
    LV = LIVEP["B136"]
    log(f"   {len(CC)} points = cost {COSTS} bps x delay t+{DELAYS}")
    log("   delay cost      CAGR   Sharpe    MaxDD      H1      H2   turn/y | 4a   why   4b   bind")
    for _, r in CC.iterrows():
        log(f"   t+{r.delay}  {r.cost:4d} {r.CAGR:8.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} "
            f"{r.H1:7.4f} {r.H2:7.4f} {r.turn_py:6.2f}  | {str(bool(r.keep4a)):5s} "
            f"{r.why4a:5s} {str(bool(r.keep4b)):5s} {r.bind}")
    n4a, n4b = int(CC.keep4a.sum()), int(CC.keep4b.sum())
    s4a, s4b = n4a / len(CC), n4b / len(CC)

    def band(s):
        return "ROBUST" if s >= 0.80 else ("ARTEFACT" if s <= 0.40 else "PARTIAL")

    v1, v2 = band(s4a), band(s4b)
    log(f"\n   V1  4a kept at {n4a}/{len(CC)} = {s4a:.1%}  -> {v1}")
    log(f"   V2  4b kept at {n4b}/{len(CC)} = {s4b:.1%}  -> {v2}")
    for ax in ("cost", "delay"):
        log(f"      by {ax:6s}: "
            + "; ".join(f"{k}: 4a {int(s.keep4a.sum())}/{len(s)} 4b {int(s.keep4b.sum())}/{len(s)}"
                        for k, s in CC.groupby(ax)))
    log("      4a failure modes: "
        + (", ".join(f"{k} x{v}" for k, v in CC[~CC.keep4a].why4a.value_counts().items())
           or "(none)"))
    log("      binding legs where 4b fails: "
        + (", ".join(f"{k} x{v}" for k, v in CC[~CC.keep4b].bind.value_counts().items())
           or "(none)"))
    # where exactly does 4a die: the frontier, per delay, of the dearest surviving cost
    fr = []
    for d, s in CC.groupby("delay"):
        ok = sorted(s[s.keep4a].cost.tolist())
        ok_b = sorted(s[s.keep4b].cost.tolist())
        fr.append(dict(delay=d, max_cost_keeping_4a=(max(ok) if ok else None),
                       max_cost_keeping_4b=(max(ok_b) if ok_b else None)))
        log(f"      t+{d}: dearest cost still clearing 4a = "
            f"{(str(max(ok)) + ' bps') if ok else 'NONE'};  4b = "
            f"{(str(max(ok_b)) + ' bps') if ok_b else 'NONE'}")
    pd.DataFrame(fr).to_csv(f"{OUT}.frontier.csv", index=False)

    # ------------------------------------------------------- V3: is the joint move additive?
    log("\n## V3 — IS THE JOINT MOVE ADDITIVE?  (Sharpe move from the (10 bps, t+1) corner)")
    piv = CC.pivot_table(index="delay", columns="cost", values="Sharpe")
    base = piv.loc[DELAY0, COST0]
    irows = []
    for d in DELAYS:
        for c in COSTS:
            obs = piv.loc[d, c] - base
            mc = piv.loc[DELAY0, c] - base                     # cost-only move
            md = piv.loc[d, COST0] - base                      # delay-only move
            inter = obs - (mc + md)
            big = max(abs(mc), abs(md))
            irows.append(dict(delay=d, cost=c, Sharpe=piv.loc[d, c], observed_move=obs,
                              cost_only=mc, delay_only=md, interaction=inter,
                              larger_main=big,
                              inter_share=(abs(inter) / big if big > 0 else np.nan)))
            log(f"   t+{d}, {c:2d} bps: Sharpe {piv.loc[d,c]:.4f}  observed {obs:+.4f}  "
                f"= cost {mc:+.4f} + delay {md:+.4f} + INTERACTION {inter:+.4f}"
                + (f"  ({abs(inter)/big:.1%} of the larger main move)" if big > 0 else ""))
    I = pd.DataFrame(irows)
    I.to_csv(f"{OUT}.interaction.csv", index=False)
    off = I[(I.delay != DELAY0) & (I.cost != COST0)]
    worst = float(off.inter_share.max())
    v3 = "ADDITIVE" if worst <= V3_BAR else "NON-ADDITIVE"
    log(f"   worst interaction over the {len(off)} genuinely joint points: "
        f"{off.interaction.abs().max():.4f} Sharpe = {worst:.1%} of the larger main move "
        f"-> {v3} (pre-stated bar {V3_BAR:.0%})")
    # the same additivity read on MaxDD, the leg that kills 4a
    pdd = CC.pivot_table(index="delay", columns="cost", values="MaxDD")
    bdd = pdd.loc[DELAY0, COST0]
    dd_int = max(abs((pdd.loc[d, c] - bdd) - ((pdd.loc[DELAY0, c] - bdd) + (pdd.loc[d, COST0] - bdd)))
                 for d in DELAYS for c in COSTS if d != DELAY0 and c != COST0)
    log(f"   MaxDD worst interaction: {dd_int:.4f} ({dd_int*100:.2f} pp)")

    # ------------------------------------------------------ corpus census on the joint plane
    log("\n## CENSUS — 4a / 4b pass counts over the whole corpus, by (delay, cost)")
    crows = []
    for (d, c), s in G.groupby(["delay", "cost"]):
        crows.append(dict(delay=d, cost=c, n=len(s), keep4a=int(s.keep4a.sum()),
                          keep4b_full=int(s.keep4b_full.sum()), keep4b=int(s.keep4b.sum())))
        log(f"   t+{d}, {c:2d} bps: 4b {int(s.keep4b.sum()):4d}/{len(s)}   "
            f"4a {int(s.keep4a.sum()):4d}/{len(s)}")
    pd.DataFrame(crows).to_csv(f"{OUT}.census.csv", index=False)
    for pn, s in G.groupby("panel"):
        log(f"   by panel: {pn:9s} 4b {int(s.keep4b.sum()):4d}/{len(s)}   "
            f"4a {int(s.keep4a.sum()):4d}/{len(s)}")

    # ------------------------------------------------------------------------ V4: rule 8
    log("\n## V4 — RULE 8 (parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE)")
    wrows = []
    for (pn, d, c, fam), sub in G.groupby(["panel", "delay", "cost", "family"]):
        S, LV2 = SPYP[pn], LIVEP[pn]
        for ch, col in (("CH_ISSHARPE", "is_Sharpe"), ("CH_ISMINLEG", "is_minleg")):
            pick = sub.loc[sub[col].idxmax()]
            wrows.append(dict(panel=pn, delay=d, cost=c, family=fam, chooser=ch,
                              target=pick.target, cell=pick.cell, is_stat=float(pick[col]),
                              oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                              oos_MaxDD=pick.oos_MaxDD,
                              spy_oos_CAGR=S["oos"]["CAGR"], spy_oos_Sharpe=S["oos"]["Sharpe"],
                              spy_oos_MaxDD=S["oos"]["MaxDD"],
                              live_oos_Sharpe=LV2["oos"]["Sharpe"],
                              keep4b=bool(pick.keep4b), keep4b_oos=bool(pick.keep4b_oos),
                              keep4a=bool(pick.keep4a), keep4a_oos=bool(pick.keep4a_oos),
                              is_candidate=bool(pn == "B136" and pick.target == 0.10
                                                and pick.cell == "h=0.08")))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    log(f"   {len(W)} picks (panel x delay x cost x family x chooser)")
    for (pn, d), s in W.groupby(["panel", "delay"]):
        log(f"      {pn:9s} t+{d}: 4b {int(s.keep4b.sum()):2d}/{len(s)}   "
            f"4a {int(s.keep4a.sum()):2d}/{len(s)}   lands on the candidate "
            f"{int(s.is_candidate.sum()):2d}/{len(s)}")
    log(f"   picks clearing BOTH paths: {int((W.keep4a & W.keep4b).sum())} of {len(W)}")
    for _, r in W[W.keep4a & W.keep4b].iterrows():
        log(f"      {r.panel:9s} t+{r.delay} {r.cost:2d}bps {r.family:5s} {r.chooser:11s} -> "
            f"t={r.target:.2f} {r.cell:7s}  OOS {r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / "
            f"{r.oos_MaxDD:7.2%}")
    log(f"   picks clearing 4b only: {int((W.keep4b & ~W.keep4a).sum())} of {len(W)}")
    for _, r in W[W.keep4b & ~W.keep4a].iterrows():
        log(f"      {r.panel:9s} t+{r.delay} {r.cost:2d}bps {r.family:5s} {r.chooser:11s} -> "
            f"t={r.target:.2f} {r.cell:7s}  OOS {r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / "
            f"{r.oos_MaxDD:7.2%}  (SPY OOS {r.spy_oos_CAGR:7.2%} / {r.spy_oos_Sharpe:.4f} / "
            f"{r.spy_oos_MaxDD:7.2%}; LIVE v2 OOS Sharpe {r.live_oos_Sharpe:.4f})")

    log("\n## VERDICT")
    log(f"   V1 (4a on the joint plane)  {v1}   {n4a}/{len(CC)} = {s4a:.1%}")
    log(f"   V2 (4b on the joint plane)  {v2}   {n4b}/{len(CC)} = {s4b:.1%}")
    log(f"   V3 (additivity)             {v3}   worst interaction {worst:.1%} of the larger "
        f"main move")
    log(f"   gates: {sum(g['pass_'] for g in _gates)}/{len(_gates)} pass")
    log("   SURVIVORSHIP: U56 / B136 are CURRENT constituents and SMALL a CURRENT sub-$2B screen,")
    log("   so every LEVEL is optimistic and both 4b bars are easier than on a point-in-time")
    log("   panel.  The (cost x delay) CONTRASTS are same-tape / same-names / same-grid and")
    log("   first-order immune; the PASS COUNTS are not.")

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()
