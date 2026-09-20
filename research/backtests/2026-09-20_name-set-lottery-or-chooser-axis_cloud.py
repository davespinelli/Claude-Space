#!/usr/bin/env python3
"""Idea 1749 (lane cloud, 2026-09-20): can a 4b-PASSING BAND BOOK be REACHED by ANY LEGAL
CHOOSER on the NAME-SET axis, or is the name set a LOTTERY?

THE DEFECT THIS CLOSES.  Idea 1632 subsampled U56 down to N = 20 names and ran the live band
book (c = 0.03, gross 0.75, weekly, t+1, 10 bps) on 24 seeded draws.  Exactly TWO of the 24
cleared 4b FULL *and* 4b OOS -- draws 3 and 18 (FULL 10.60% / 1.2062 / -14.25% and 11.07% /
1.2355 / -14.75%; OOS 11.95% / 1.2657 and 10.85% / 1.1995) -- and NO in-sample-only chooser
reached either: 0 of 9 picks cleared either KEEP path out of sample, every one of them on the
4b CAGR floor.  With 24 draws and 2 passers that is an UNRESOLVED count, not a finding: a
chooser that is genuinely informative would still miss at that sample size, and a chooser that
is pure noise would look identical.  Until the draw count is widened the record cannot say
whether the NAME SET is an AXIS a rule may legally select on, or a LOTTERY whose winners are
hindsight.  1632's two passers are currently quoted in the record as if they were books.

THE TEST.  Widen the draw count at N = 20 on U56 along the SAME seed stream 1632 used (so its
24 draws are the first 24 of this run's 480 and its two passers are reproduced bit-for-bit at
G3), rank every draw by an IN-SAMPLE-ONLY statistic, and compare the OOS 4b pass RATE of the
TOP DECILE against the BASE RATE of the whole draw population.  A chooser with real information
lifts the top decile above the base rate; a lottery does not.  The comparison is published with
an EXACT hypergeometric tail probability (no RNG, no asymptotics) and with the Spearman rank
correlation between the IS statistic and the OOS 4b margin, so a lift that is real but small is
not thrown away with a lift that is zero.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  DRAW COUNT  D in {24, 96, 240, 480}.  Nested: D = 24 is 1632's own population exactly.
  DIAL 2  IS RANKING STATISTIC S in
            IS_SHARPE     Sharpe over [warm-up, 2016-12-31]
            IS_LEGS       how many of the FOUR in-sample-readable 4b legs the draw passes
                          (H1 > SPY H1, H2 > SPY H2, MaxDD >= 0.60 x SPY MaxDD,
                           CAGR >= 0.70 x SPY CAGR), all computed inside the IS window only
            IS_CAGRSLACK  IS CAGR - 0.70 x SPY IS CAGR -- the leg 1632's 9 picks all died on
            IS_MINMARG    min over those four legs of the leg's margin divided by that leg's
                          cross-draw standard deviation (a joint-margin chooser)
REPORTED AXES, not tuned, every point published to `_grid.csv`:
  COST {0, 10, 25, 50} bps, reconstructed exactly off the cost-0 leg (weights are
  cost-independent); the protocol's binding rung is 10 bps and every verdict is read there.
  The full-panel N = 56 band book is carried as a deterministic reference row.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) top-decile OOS-4b rate <= base rate at every (D, S) -> the NAME SET IS A LOTTERY and
      1632's draws 3 and 18 are hindsight; the record should say so once and for all.
  (b) some (D, S) lifts the top decile materially above the base rate, and the lift SURVIVES
      the widening from D = 24 to D = 480 -> the name set is a reachable axis and the chooser
      that reaches it is named.
  (c) a lift that appears at small D and vanishes at large D is itself the answer: the 24-draw
      population was too small to resolve the question, which is exactly the defect above.
  (d) rule 8's own question, answered separately: the argmax pick of each statistic on
      2009-2016 only, its 2017-2026 numbers read ONCE against live RULES v2 and SPY.

GATES.  G1 this runner == `engine.backtest` on returns AND turnover for the live band book on
the full U56 panel.  G2 the cost identity r(c) = r0 - turnover * c / 1e4 == the engine at 10 and
25 bps.  G3 CROSS-RUN: 1632's published draw-3 and draw-18 cells reproduce (FULL CAGR / Sharpe /
MaxDD and OOS CAGR / Sharpe).  G4 no chooser statistic reads a row on or after 2017-01-01.
G5 exactly two tuned dials.  G6 every cell published.  G7 the ONLY RNG is the draw index
selection, seeded exactly as 1632 (`default_rng(16320000 + 1009*N + d)`), so the draw stream is
reproducible and nested.  G8 no leverage / no shorting: max realised TARGET gross <= 0.75.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1 execution, 10 bps binding, no leverage, no shorting);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, two dials); rule 8
(walk-forward, IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 is a CURRENT-constituent list (56 large caps and sector/bond ETFs that exist
today), so every CAGR and drawdown LEVEL below is optimistic and BOTH 4b bars are easier here
than on a point-in-time panel.  The lottery-vs-axis comparison is a WITHIN-PANEL contrast --
same tape, same bars, same seed stream, only the 20 names moved -- and is first-order immune to
that bias; the absolute pass COUNTS are not, and are quoted as upper bounds.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_name-set-lottery-or-chooser-axis_cloud.py
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state      # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-20", "name-set-lottery-or-chooser-axis"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
GROSS = 0.75
BAND_C = 0.03                      # live RULES v2 clause 2
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

NAMES_N = 20
DCOUNTS = [24, 96, 240, 480]
DMAX = max(DCOUNTS)
SEED0 = 16320000                   # idea 1632's seed base, carried over unchanged (G7)
STATS = ["IS_SHARPE", "IS_LEGS", "IS_CAGRSLACK", "IS_MINMARG"]
IS_LEGS4 = ["I1_H1", "I2_H2", "I4_DD", "I5_CAGR"]

# idea 1632's published N=20 U56 passers (band c=0.03, gross 0.75, W, 10 bps)
PUB = {3:  dict(CAGR=0.1060, Sharpe=1.2062, MaxDD=-0.1425, oCAGR=0.1195, oSharpe=1.2657),
       18: dict(CAGR=0.1107, Sharpe=1.2355, MaxDD=-0.1475, oCAGR=0.1085, oSharpe=1.1995)}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# --------------------------------------------------------------------------- book machinery
class Panel:
    def __init__(self, px):
        self.px = px
        self.cols = list(px.columns)
        self.idx = px.index
        q = px[self.cols]
        self.rets = np.nan_to_num(q.pct_change().values, nan=0.0)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.priced = q.notna().values
        self.band = band_state(q, BAND_C).values
        m = rebalance_mask(self.idx, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(self.idx)


def frame_of(pan: Panel, j):
    """Target weights at gross 1.0 for the sub-book on columns `j`, shifted one row so row t
    carries the close-(t-1) decision -- exactly engine.backtest's `weights.shift(1)`.
    N = names PRICED in the sub-book (the live RULES v2 convention); gated-out weight goes to
    cash and is NEVER re-spread."""
    pr = pan.priced[:, j]
    e = (pr & pan.band[:, j]).astype(float)
    n = pr.sum(axis=1).astype(float)
    w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
    w = np.nan_to_num(w, nan=0.0)
    return np.vstack([np.zeros((1, w.shape[1])), w[:-1]])


def run_cell(pan: Panel, j, frame, g=GROSS):
    """Hold g*frame on the weekly schedule, drift between rebalances, de-gross to 0%-yielding
    cash.  Returns gross-of-cost daily returns, the turnover path and max realised target
    gross -- identical semantics to engine.backtest (gated at G1)."""
    rets = pan.rets[:, j]
    C, Cp = pan.C[:, j], pan.Cp[:, j]
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    reb = pan.reb
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max


def net(rg, tu, c):
    return rg - tu * c / 1e4


def mets(r):
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std(ddof=1) * math.sqrt(252.0)
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    return dict(CAGR=eq[-1] ** (1.0 / yrs) - 1.0 if yrs else float("nan"),
                Sharpe=(r.mean() * 252.0) / vol if vol else float("nan"), MaxDD=dd)


def halves(r):
    h = len(r) // 2
    return mets(r[:h])["Sharpe"], mets(r[h:])["Sharpe"]


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    def rk(v):
        o = np.argsort(v, kind="mergesort")
        r = np.empty(len(v), float)
        r[o] = np.arange(1, len(v) + 1)
        # average ties
        s = np.sort(v)
        i = 0
        while i < len(s):
            k = i
            while k + 1 < len(s) and s[k + 1] == s[i]:
                k += 1
            if k > i:
                r[o[i:k + 1]] = (i + k + 2) / 2.0
            i = k + 1
        return r
    a, b = rk(x), rk(y)
    if a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def hyper_sf(k, D, K, n):
    """Exact P(X >= k) for X ~ Hypergeometric(D, K, n).  No RNG, no asymptotics."""
    if K == 0:
        return 1.0 if k <= 0 else 0.0
    tot = math.comb(D, n)
    s = 0
    for x in range(k, min(K, n) + 1):
        s += math.comb(K, x) * math.comb(D - K, n - x)
    return s / tot


# --------------------------------------------------------------------------- run
def main():
    t_start = time.time()
    say("=" * 116)
    say("IDEA 1749 (lane cloud, 2026-09-20) — can a 4b-PASSING BAND BOOK be REACHED by ANY LEGAL")
    say("CHOOSER on the NAME-SET axis, or is the name set a LOTTERY?")
    say("=" * 116)
    say(f"# dials: DRAW COUNT D {DCOUNTS} x IS RANKING STATISTIC {STATS}")
    say(f"# fixed: U56, N={NAMES_N} names, band c={BAND_C}, gross {GROSS}, cadence {CADENCE}, "
        f"t+1; reported axis: cost {COSTS} bps (binding {BIND:.0f})")
    say(f"# warm-up {WARMUP} rows | IS <= {IS_END} | OOS >= {OOS_START}")
    say("# the ONLY RNG is the draw index selection, seeded exactly as idea 1632 (G7)")
    say("")

    px = load_universe().dropna(how="all").ffill()
    pan = Panel(px)
    st = WARMUP
    M = len(pan.cols)
    i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
    i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END), side="right"))
    say(f"# panel U56: {M} columns, {pan.idx[0].date()} -> {pan.idx[-1].date()} "
        f"({pan.T} rows, {pan.T/252:.1f}y); scored from {pan.idx[st].date()} "
        f"({(pan.T-st)/252:.1f}y, PROTOCOL rule 1)")
    say(f"# IS rows {i_is-st} ({(i_is-st)/252:.1f}y)  OOS rows {pan.T-i_oos} "
        f"({(pan.T-i_oos)/252:.1f}y)")
    gate("G5 tuned dials", "DRAW COUNT D, IS RANKING STATISTIC S", "exactly 2", True)
    gate("G4 chooser window closes before OOS", f"IS ends at row {i_is-1} "
         f"({pan.idx[i_is-1].date()}), OOS starts at row {i_oos} ({pan.idx[i_oos].date()})",
         "IS_end < OOS_start", i_is <= i_oos)

    # ---- benchmarks: SPY and live RULES v2 -------------------------------------------
    spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)[st:]
    S_full, S_oos, S_is = mets(spy), mets(spy[i_oos - st:]), mets(spy[:i_is - st])
    S_h1, S_h2 = halves(spy)
    S_ih1, S_ih2 = halves(spy[:i_is - st])

    lw = rules_v2_weights(px, band=BAND_C, gross=GROSS)
    lb = engine_backtest(px, lw, cost_bps=0.0, freq=CADENCE)
    lr0 = np.nan_to_num(lb["returns"].values, nan=0.0)[st:]
    lt0 = np.nan_to_num(lb["turnover"].values, nan=0.0)[st:]
    LIVE = {}
    for c in COSTS:
        r = net(lr0, lt0, c)
        h1, h2 = halves(r)
        LIVE[c] = dict(full=mets(r), oos=mets(r[i_oos - st:]), h1=h1, h2=h2)
    L = LIVE[BIND]
    say("")
    say(f"# SPY          FULL {S_full['CAGR']:7.2%} / {S_full['Sharpe']:.4f} / "
        f"{S_full['MaxDD']:7.2%}   H1/H2 {S_h1:.4f}/{S_h2:.4f}   OOS {S_oos['CAGR']:7.2%} / "
        f"{S_oos['Sharpe']:.4f} / {S_oos['MaxDD']:7.2%}")
    say(f"# RULES v2 live FULL {L['full']['CAGR']:7.2%} / {L['full']['Sharpe']:.4f} / "
        f"{L['full']['MaxDD']:7.2%}   H1/H2 {L['h1']:.4f}/{L['h2']:.4f}   OOS "
        f"{L['oos']['CAGR']:7.2%} / {L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:7.2%}   "
        f"(the FULL 56-name band book, {BIND:.0f} bps)")
    say(f"# 4b bars: FULL DD cap {DD_CAP*S_full['MaxDD']:7.2%}, CAGR floor "
        f"{CAGR_FLOOR*S_full['CAGR']:6.2%} | OOS DD cap {DD_CAP*S_oos['MaxDD']:7.2%}, CAGR floor "
        f"{CAGR_FLOOR*S_oos['CAGR']:6.2%} | IS DD cap {DD_CAP*S_is['MaxDD']:7.2%}, CAGR floor "
        f"{CAGR_FLOOR*S_is['CAGR']:6.2%}")

    # ---- G1 / G2: the runner against the engine on the FULL panel --------------------
    jall = np.arange(M)
    fr_all = frame_of(pan, jall)
    r_all, t_all, gmax_all = run_cell(pan, jall, fr_all)
    d_r = float(np.abs(np.nan_to_num(lb["returns"].values, nan=0.0) - r_all).max())
    d_t = float(np.abs(np.nan_to_num(lb["turnover"].values, nan=0.0) - t_all).max())
    gate("G1 runner == engine.backtest (live band book, full U56)",
         f"returns {d_r:.3e}, turnover {d_t:.3e}", "< 1e-12", d_r < 1e-12 and d_t < 1e-12)
    d2 = 0.0
    for c in (10.0, 25.0):
        eb = np.nan_to_num(engine_backtest(px, lw, cost_bps=c, freq=CADENCE)["returns"].values,
                           nan=0.0)
        d2 = max(d2, float(np.abs(net(r_all, t_all, c) - eb).max()))
    gate("G2 cost identity r(c) = r0 - turnover*c/1e4", f"max|d| = {d2:.3e}", "< 1e-15",
         d2 < 1e-15)

    # ---- the draw population ----------------------------------------------------------
    spy_j = pan.cols.index("SPY") if "SPY" in pan.cols else -1
    rows = []
    gmax = 0.0
    say("")
    say(f"# running {DMAX} seeded {NAMES_N}-name draws x {len(COSTS)} cost rungs ...")
    for d in range(DMAX):
        j = np.sort(np.random.default_rng(SEED0 + 1009 * NAMES_N + d)
                    .choice(M, size=NAMES_N, replace=False))
        fr = frame_of(pan, j)
        r0, t0, gm = run_cell(pan, j, fr)
        gmax = max(gmax, gm)
        r0, t0 = r0[st:], t0[st:]
        has_spy = bool(spy_j >= 0 and spy_j in set(j.tolist()))
        yrs = len(r0) / 252.0
        for c in COSTS:
            r = net(r0, t0, c)
            mf, mo, mi = mets(r), mets(r[i_oos - st:]), mets(r[:i_is - st])
            h1, h2 = halves(r)
            ih1, ih2 = halves(r[:i_is - st])
            # --- the FOUR in-sample-readable 4b legs (chooser inputs; G4) --------------
            il = {"I1_H1": ih1 - S_ih1, "I2_H2": ih2 - S_ih2,
                  "I4_DD": mi["MaxDD"] - DD_CAP * S_is["MaxDD"],
                  "I5_CAGR": mi["CAGR"] - CAGR_FLOOR * S_is["CAGR"]}
            # --- the 4b verdicts ------------------------------------------------------
            k4bf = (h1 > S_h1 and h2 > S_h2 and mf["MaxDD"] >= DD_CAP * S_full["MaxDD"]
                    and mf["CAGR"] >= CAGR_FLOOR * S_full["CAGR"])
            k4bo = (mo["Sharpe"] > S_oos["Sharpe"]
                    and mo["MaxDD"] >= DD_CAP * S_oos["MaxDD"]
                    and mo["CAGR"] >= CAGR_FLOOR * S_oos["CAGR"])
            LV = LIVE[c]
            rows.append(dict(
                draw=d, cost=c, has_spy=has_spy, turn_py=float(t0.sum() / yrs),
                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                is_H1=ih1, is_H2=ih2, **il,
                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                L1_H1=h1 - S_h1, L2_H2=h2 - S_h2,
                L3_OOS=mo["Sharpe"] - S_oos["Sharpe"],
                L4_DD=mf["MaxDD"] - DD_CAP * S_full["MaxDD"],
                L5_CAGR=mf["CAGR"] - CAGR_FLOOR * S_full["CAGR"],
                O3_OOS=mo["Sharpe"] - S_oos["Sharpe"],
                O4_DD=mo["MaxDD"] - DD_CAP * S_oos["MaxDD"],
                O5_CAGR=mo["CAGR"] - CAGR_FLOOR * S_oos["CAGR"],
                keep4b_full=bool(k4bf), keep4b_oos=bool(k4bo),
                keep4b=bool(k4bf and k4bo),
                keep4a=bool(h1 > LV["h1"] and h2 > LV["h2"]
                            and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                keep4a_oos=bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                and mo["MaxDD"] >= LV["oos"]["MaxDD"]),
            ))
    gate("G8 no leverage / no shorting", f"max realised TARGET gross {gmax:.6f}",
         f"<= {GROSS}", gmax <= GROSS + 1e-12)

    df = pd.DataFrame(rows)
    # the IS_MINMARG chooser needs the cross-draw sd of each leg, computed at the binding rung
    b = df[df.cost == BIND]
    sds = {k: float(b[k].std(ddof=1)) for k in IS_LEGS4}
    df["IS_SHARPE"] = df["is_Sharpe"]
    df["IS_LEGS"] = sum((df[k] > 0).astype(int) for k in IS_LEGS4)
    df["IS_CAGRSLACK"] = df["I5_CAGR"]
    df["IS_MINMARG"] = df[IS_LEGS4].div(pd.Series(sds)).min(axis=1)
    df.to_csv(f"{OUT}_grid.csv", index=False)
    gate("G6 every cell published", f"{len(df)} rows -> {Path(OUT).name}_grid.csv",
         f"{DMAX*len(COSTS)}", len(df) == DMAX * len(COSTS))

    # ---- G3 cross-run against idea 1632's published passers ---------------------------
    mx = 0.0
    for dd, pub in PUB.items():
        q = df[(df.draw == dd) & (df.cost == BIND)].iloc[0]
        for k, col in (("CAGR", "CAGR"), ("Sharpe", "Sharpe"), ("MaxDD", "MaxDD"),
                       ("oCAGR", "oos_CAGR"), ("oSharpe", "oos_Sharpe")):
            mx = max(mx, abs(pub[k] - float(q[col])))
    gate("G3 cross-run vs idea 1632's published N=20 draws 3 and 18",
         f"max|d| = {mx:.3e}", "< 5e-4 (1632 quotes 4 dp)", mx < 5e-4)

    B = df[df.cost == BIND].sort_values("draw").reset_index(drop=True)
    say("")
    say(f"## THE DRAW POPULATION at N={NAMES_N}, band c={BAND_C}, gross {GROSS}, "
        f"{BIND:.0f} bps ({DMAX} draws)")
    say(f"   SPY inclusion rate in the draw: {B.has_spy.mean():.1%} "
        f"(expected {NAMES_N}/{M} = {NAMES_N/M:.1%})")
    for nm, col in (("FULL Sharpe", "Sharpe"), ("FULL CAGR", "CAGR"), ("FULL MaxDD", "MaxDD"),
                    ("OOS Sharpe", "oos_Sharpe"), ("OOS CAGR", "oos_CAGR"),
                    ("OOS MaxDD", "oos_MaxDD"), ("turnover /yr", "turn_py")):
        v = B[col]
        say(f"   {nm:<14s} mean {v.mean():9.4f}  sd {v.std(ddof=1):8.4f}  min {v.min():9.4f}  "
            f"p50 {v.median():9.4f}  max {v.max():9.4f}")
    say(f"   4b FULL passes {int(B.keep4b_full.sum()):4d} / {len(B)}   "
        f"4b OOS passes {int(B.keep4b_oos.sum()):4d} / {len(B)}   "
        f"BOTH (the object) {int(B.keep4b.sum()):4d} / {len(B)}")
    say(f"   4a FULL passes {int(B.keep4a.sum()):4d} / {len(B)}   "
        f"4a OOS passes {int(B.keep4a_oos.sum()):4d} / {len(B)}")
    say("   binding OOS leg among 4b-OOS failures: " + ", ".join(
        f"{k} {int((~B.keep4b_oos & (B[k] <= 0)).sum())}" for k in ("O3_OOS", "O4_DD", "O5_CAGR")))
    say("   4b-BOTH passers: draws " + ", ".join(str(int(x)) for x in B[B.keep4b].draw.tolist()))

    # ---- THE QUESTION: top decile vs base rate ----------------------------------------
    say("")
    say("## Q1 — TOP-DECILE OOS-4b RATE vs the DRAW BASE RATE (the lottery test)")
    say("   'top decile' = the ceil(D/10) draws with the highest IS statistic, ranked on "
        "2009-2016 data ONLY (G4).")
    say("   p = EXACT hypergeometric P(X >= observed) for that many hits in the top decile "
        "under the lottery null.")
    say("")
    q1 = []
    for D in DCOUNTS:
        sub = B[B.draw < D]
        n_top = max(1, math.ceil(D / 10))
        for tgt, lab in (("keep4b_oos", "4b OOS"), ("keep4b", "4b BOTH")):
            K = int(sub[tgt].sum())
            base = K / D
            say(f"   D={D:<4d} target {lab:<8s} base rate {K:3d}/{D} = {base:6.2%}   "
                f"top decile = {n_top} draws")
            for S in STATS:
                top = sub.nlargest(n_top, S, keep="first")
                k = int(top[tgt].sum())
                rate = k / n_top
                p = hyper_sf(k, D, K, n_top)
                rho = spearman(sub[S].values, sub["O3_OOS"].values)
                rho5 = spearman(sub[S].values, sub["O5_CAGR"].values)
                say(f"          {S:<13s} top-decile {k:3d}/{n_top} = {rate:6.2%}   "
                    f"lift {rate-base:+7.2%}   p = {p:.4f}   "
                    f"rho(S, OOS Sharpe margin) {rho:+.4f}   rho(S, OOS CAGR margin) {rho5:+.4f}")
                q1.append(dict(D=D, target=lab, stat=S, base_K=K, base_rate=base, n_top=n_top,
                               top_k=k, top_rate=rate, lift=rate - base, hyper_p=p,
                               rho_oos_sharpe=rho, rho_oos_cagr=rho5))
            say("")
    pd.DataFrame(q1).to_csv(f"{OUT}_decile.csv", index=False)

    # ---- RULE 8: the argmax pick, read ONCE -------------------------------------------
    say("")
    say("## RULE 8 WALK-FORWARD — each statistic's ARGMAX draw is chosen on 2009-2016 ONLY and "
        "its 2017-2026 numbers are read ONCE")
    say(f"   reference OOS: SPY {S_oos['CAGR']:7.2%} / {S_oos['Sharpe']:.4f} / "
        f"{S_oos['MaxDD']:7.2%} | RULES v2 live {L['oos']['CAGR']:7.2%} / "
        f"{L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:7.2%}")
    say("")
    say(f"   {'D':>4s} {'statistic':<13s} {'pick':>5s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} "
        f"{'OOS MaxDD':>10s}  {'4bOOS':>5s} {'4aOOS':>5s}  binding OOS leg")
    r8 = []
    for D in DCOUNTS:
        sub = B[B.draw < D]
        for S in STATS:
            pick = sub.nlargest(1, S, keep="first").iloc[0]
            bad = [k for k in ("O3_OOS", "O4_DD", "O5_CAGR") if not pick[k] > 0]
            say(f"   {D:>4d} {S:<13s} {int(pick.draw):>5d} {pick.oos_CAGR:>9.2%} "
                f"{pick.oos_Sharpe:>9.4f} {pick.oos_MaxDD:>10.2%}  "
                f"{str(bool(pick.keep4b_oos)):>5s} {str(bool(pick.keep4a_oos)):>5s}  "
                f"{'|'.join(bad) if bad else 'none'}")
            r8.append(dict(D=D, stat=S, pick=int(pick.draw), oos_CAGR=pick.oos_CAGR,
                           oos_Sharpe=pick.oos_Sharpe, oos_MaxDD=pick.oos_MaxDD,
                           keep4b_oos=bool(pick.keep4b_oos), keep4a_oos=bool(pick.keep4a_oos),
                           keep4b=bool(pick.keep4b), keep4a=bool(pick.keep4a),
                           binding='|'.join(bad) if bad else 'none'))
    pd.DataFrame(r8).to_csv(f"{OUT}_rule8.csv", index=False)
    npick = len(r8)
    n4b = sum(x["keep4b_oos"] for x in r8)
    n4a = sum(x["keep4a_oos"] for x in r8)
    say(f"   -> {n4b} of {npick} legal IS-only picks clear 4b OOS; {n4a} of {npick} clear 4a OOS")

    # ---- the cost ladder ---------------------------------------------------------------
    say("")
    say("## COST LADDER (reported axis, not tuned): 4b pass counts over the full 480 draws")
    say(f"   {'cost':>5s} {'4b FULL':>9s} {'4b OOS':>8s} {'4b BOTH':>9s} {'4a FULL':>9s} "
        f"{'mean turn/yr':>13s}")
    for c in COSTS:
        s = df[df.cost == c]
        say(f"   {c:>5.0f} {int(s.keep4b_full.sum()):>9d} {int(s.keep4b_oos.sum()):>8d} "
            f"{int(s.keep4b.sum()):>9d} {int(s.keep4a.sum()):>9d} {s.turn_py.mean():>13.3f}")

    # ---- 1632's two passers, restated ---------------------------------------------------
    say("")
    say("## 1632's TWO PASSERS, restated against the widened population")
    for dd in sorted(PUB):
        q = B[B.draw == dd].iloc[0]
        pr_s = float((B.oos_Sharpe <= q.oos_Sharpe).mean())
        pr_i = float((B.IS_SHARPE <= q.IS_SHARPE).mean())
        say(f"   draw {dd:>3d}: FULL {q.CAGR:7.2%} / {q.Sharpe:.4f} / {q.MaxDD:7.2%}  "
            f"OOS {q.oos_CAGR:7.2%} / {q.oos_Sharpe:.4f} / {q.oos_MaxDD:7.2%}  "
            f"4b BOTH {bool(q.keep4b)}  | IS Sharpe percentile {pr_i:6.1%}, "
            f"OOS Sharpe percentile {pr_s:6.1%}")

    # ---- verdict -------------------------------------------------------------------------
    best = max(q1, key=lambda z: (z["target"] == "4b BOTH", z["lift"]))
    anylift = [z for z in q1 if z["lift"] > 0 and z["hyper_p"] < 0.05]
    big = [z for z in q1 if z["D"] == DMAX and z["lift"] > 0 and z["hyper_p"] < 0.05]
    say("")
    say("=" * 116)
    say("VERDICT")
    say(f"  top-decile lifts significant at p < 0.05: {len(anylift)} of {len(q1)} "
        f"(D x statistic x target) cells; at the widest D={DMAX}: {len(big)} of "
        f"{len([z for z in q1 if z['D']==DMAX])}")
    say(f"  largest lift anywhere: {best['stat']} at D={best['D']} on {best['target']} — "
        f"{best['top_rate']:.2%} vs base {best['base_rate']:.2%} "
        f"(lift {best['lift']:+.2%}, p = {best['hyper_p']:.4f})")
    say(f"  rule 8: {n4b} of {npick} legal IS-only picks clear 4b OOS, {n4a} of {npick} clear 4a OOS")
    ok = all(g["pass_"] for g in GATES)
    say(f"  gates: {sum(g['pass_'] for g in GATES)} / {len(GATES)} pass")
    say(f"  runtime {time.time()-t_start:.1f}s")
    say("=" * 116)

    pd.DataFrame(GATES).to_csv(f"{OUT}_gates.csv", index=False)
    Path(f"{OUT}_log.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
