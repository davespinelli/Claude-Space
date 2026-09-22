#!/usr/bin/env python3
"""Idea 1775 (lane C, 2026-09-22): does the NAME-SET CHOOSER LIFT REPLICATE on B136 and SMALL,
or is it a U56 fact?

THE DEFECT THIS CLOSES.  Idea 1749 (lane cloud, 2026-09-20) widened idea 1632's 24 seeded
20-name draws to 480 on U56 and found the NAME SET to be a REACHABLE axis, not a lottery: the
4b FULL-and-OOS base rate over the 480 draws is 43/480 = 8.96%, while ranking the draws on an
IN-SAMPLE-ONLY statistic read on 2009-2016 lifts the TOP DECILE to 25/48 = 52.08% (IS_CAGRSLACK
and IS_MINMARG), exact hypergeometric p < 1e-4.  That whole measurement was taken on ONE panel
with 56 columns, 20 of them drawn — a 35.7% cut of a CURRENT-constituent list.  If the lift is
NAME-SET INFORMATION it must appear wherever the pool is wide enough to draw from.  If it is a
56-name artefact (the draw covers a third of the pool, so two draws share ~7 names on average
and every draw inherits most of the panel's own factor structure) it will not.  The record
currently quotes 1749's lift as a property of the name-set AXIS, not of U56.

THE TEST.  Re-run 1749's construction UNCHANGED — band c = 0.03, gross 0.75, weekly cadence,
t+1 execution, 10 bps binding, the same `default_rng(16320000 + 1009*N + d)` seed stream, the
same four IS-only ranking statistics, the same ceil(D/10) top decile, the same exact
hypergeometric tail — on THREE panels at TWO draw widths, and compare each cell's top-decile
OOS-4b rate against that cell's OWN base rate.  U56 at N = 20 is 1749's own cell and is carried
as a bit-for-bit replication gate (G3), not as a new measurement.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  PANEL  {U56, B136, SMALL} — SMALL drops the max_1d_move >= 1.0 tickers of
          data/small_meta.csv first (the convention of every small-panel run in this record) and
          never draws the joined SPY benchmark column.
  DIAL 2  N (names drawn) {20, 40}.
EVERYTHING ELSE IS INHERITED FROM 1749, NOT TUNED: the band rung c = 0.03, gross 0.75, cadence
W, the decile width D/10, the seed stream, the statistic set {IS_SHARPE, IS_LEGS, IS_CAGRSLACK,
IS_MINMARG}, the IS/OOS split at 2016-12-31 / 2017-01-01.
REPORTED AXES, not tuned, every cell published to `.grid.csv`:
  DRAW COUNT D in {24, 96, 240, 480} (nested: the D = 24 population is the first 24 draws of the
  480, exactly as 1749 nested 1632's), and COST {0, 10, 25, 50} bps reconstructed exactly off the
  cost-0 leg (weights are cost-independent; G2).  Every verdict is read at the protocol's 10 bps.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) the lift appears with p < 0.05 on B136 AND on SMALL at both N -> the chooser carries NAME
      SET information and 1749's headline is a property of the axis, as the record now reads it.
  (b) the lift is confined to U56 (absent or negative on the other two panels) -> 1749's headline
      is a U56 fact, the record's wording must be narrowed, and the name-set axis is NOT
      established as reachable on a wide pool.
  (c) the lift survives on some panels and dies on others -> the reachability of the name set is
      itself a PANEL property, i.e. one more universe-by-universe pricing job and not a law.
  (d) rule 8, answered separately at every cell: the argmax draw of each statistic chosen on
      2009-2016 ONLY, its 2017-2026 numbers read ONCE against live RULES v2 and SPY, both KEEP
      paths.

GATES.  G1 this runner == `engine.backtest` on returns AND turnover for the full-pool band book
on each panel.  G2 the cost identity r(c) = r0 - turnover*c/1e4 == the engine at 10 and 25 bps.
G3 CROSS-RUN REPLICATION of idea 1749 / 1632: U56 N=20 draws 3 and 18 reproduce 1632's published
cells, and the U56 N=20 D=480 base rate and top-decile counts reproduce 1749's published
43/480 and 25/48.  G4 no chooser statistic reads a row on or after 2017-01-01.  G5 exactly two
tuned dials.  G6 every cell published.  G7 the ONLY RNG is the draw index selection, seeded with
1749's formula unchanged.  G8 no leverage / no shorting: max realised TARGET gross <= 0.75.
G9 SMALL's trading days are a SUBSET of U56's, so the live RULES v2 4a anchor can be read on
SMALL's own calendar without interpolation.

PROTOCOL: rule 1 (>= 10y on every panel); rule 2 (t+1, 10 bps binding, no leverage/shorting);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, two dials); rule 8
(walk-forward, IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  All three panels are CURRENT-constituent lists (U56 and B136 are names that exist
today; SMALL is today's sub-$2B screen), so every CAGR and drawdown LEVEL below is optimistic and
both 4b bars are easier here than on a point-in-time panel.  The lift is a WITHIN-PANEL contrast
— same tape, same bars, same seed stream, only the drawn names move — and is first-order immune
to that bias; the absolute pass COUNTS are not, and are quoted as upper bounds.  The CROSS-PANEL
comparison that is this idea's object additionally assumes the three panels' survivorship
exposures are comparable, which they are not identically: the draw is a 35.7% cut of U56, a
14.7% cut of B136 and a ~3% cut of SMALL at N = 20, and that difference in cut depth is itself a
candidate explanation for any panel dependence found.  It is reported, not controlled away.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-22_name-set-chooser-lift-replication_C.py
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

DATE, SLUG = "2026-09-22", "name-set-chooser-lift-replication"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
GROSS = 0.75                       # live RULES v2
BAND_C = 0.03                      # live RULES v2 clause 2
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

NLIST = [20, 40]                   # DIAL 2
DCOUNTS = [24, 96, 240, 480]       # reported, nested
DMAX = max(DCOUNTS)
SEED0 = 16320000                   # idea 1632's / 1749's seed base, unchanged (G7)
STATS = ["IS_SHARPE", "IS_LEGS", "IS_CAGRSLACK", "IS_MINMARG"]
IS_LEGS4 = ["I1_H1", "I2_H2", "I4_DD", "I5_CAGR"]

# idea 1632's published U56 N=20 passers (band c=0.03, gross 0.75, W, 10 bps), re-quoted by 1749
PUB_1632 = {3:  dict(CAGR=0.1060, Sharpe=1.2062, MaxDD=-0.1425, oCAGR=0.1195, oSharpe=1.2657),
            18: dict(CAGR=0.1107, Sharpe=1.2355, MaxDD=-0.1475, oCAGR=0.1085, oSharpe=1.1995)}
# idea 1749's published U56 N=20 D=480 counts on the "4b BOTH" target
PUB_1749 = dict(base_K=43, D=480, n_top=48, top_k=25)

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
# (identical semantics to idea 1749's runner; gated against engine.backtest at G1/G2)
class Panel:
    def __init__(self, px, pool):
        self.px = px
        self.cols = list(px.columns)
        self.pool = list(pool)                       # columns a draw may select from
        self.pool_j = np.array([self.cols.index(c) for c in self.pool])
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
    """Target weights at gross 1.0 for the sub-book on column indices `j`, shifted one row so
    row t carries the close-(t-1) decision -- exactly engine.backtest's `weights.shift(1)`.
    N = names PRICED in the sub-book (the live RULES v2 convention); gated-out weight goes to
    CASH and is NEVER re-spread."""
    pr = pan.priced[:, j]
    e = (pr & pan.band[:, j]).astype(float)
    n = pr.sum(axis=1).astype(float)
    w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
    w = np.nan_to_num(w, nan=0.0)
    return np.vstack([np.zeros((1, w.shape[1])), w[:-1]])


def run_cell(pan: Panel, j, frame, g=GROSS):
    """Hold g*frame on the weekly schedule, drift between rebalances, de-gross to 0%-yielding
    cash.  Returns gross-of-cost daily returns, the turnover path and max realised target
    gross."""
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


# --------------------------------------------------------------------------- panels
def build_panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_pool = [c for c in pxs.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxs.columns if c in bad])
    return [("U56", px56, list(px56.columns), 0),          # 1749's own pool: SPY drawable
            ("B136", px136, list(px136.columns), 0),
            (f"SMALL{len(small_pool)}", pxs, small_pool, n_drop)]


# --------------------------------------------------------------------------- run
def main():
    t0_wall = time.time()
    say("=" * 118)
    say(f"IDEA 1775 (lane C, {DATE}) — does the NAME-SET CHOOSER LIFT REPLICATE on B136 and")
    say("SMALL, or is it a U56 fact?")
    say("=" * 118)
    say(f"# dials: PANEL {{U56, B136, SMALL}} x N {NLIST}")
    say(f"# inherited from 1749, NOT tuned: band c={BAND_C}, gross {GROSS}, cadence {CADENCE}, "
        f"t+1, decile = ceil(D/10), statistics {STATS}, split {IS_END}/{OOS_START}")
    say(f"# reported axes: draw count D {DCOUNTS} (nested), cost {COSTS} bps "
        f"(binding {BIND:.0f})")
    say(f"# the ONLY RNG is the draw index selection, seeded default_rng({SEED0} + 1009*N + d) "
        "— idea 1632's / 1749's formula unchanged (G7)")
    say("")
    gate("G5 tuned dials", "PANEL, N", "exactly 2", True)
    gate("G7 seed stream", f"default_rng({SEED0} + 1009*N + d), d = 0..{DMAX-1}",
         "1749's formula unchanged", True)

    PANELS = build_panels()

    # --- the live RULES v2 book on U56: the protocol rule-3 4a anchor for EVERY panel -------
    px56 = PANELS[0][1]
    lw56 = rules_v2_weights(px56, band=BAND_C, gross=GROSS)
    lb56 = engine_backtest(px56, lw56, cost_bps=0.0, freq=CADENCE)
    live56_r0 = pd.Series(np.nan_to_num(lb56["returns"].values, nan=0.0), index=px56.index)
    live56_t0 = pd.Series(np.nan_to_num(lb56["turnover"].values, nan=0.0), index=px56.index)
    small_idx = PANELS[2][1].index
    sub_ok = bool(small_idx.isin(px56.index).all())
    gate("G9 SMALL trading days subset of U56's",
         f"{int(small_idx.isin(px56.index).sum())} / {len(small_idx)} rows found in U56",
         "all", sub_ok)

    all_rows: list[dict] = []
    q1: list[dict] = []
    r8: list[dict] = []
    panel_ref: list[dict] = []
    gmax_global = 0.0
    g1_worst = 0.0
    g2_worst = 0.0

    for pname, px, pool, n_drop in PANELS:
        pan = Panel(px, pool)
        st = WARMUP
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END), side="right"))
        say("")
        say("-" * 118)
        say(f"## PANEL {pname}: {len(pan.cols)} columns, draw pool {len(pool)}"
            + (f" ({n_drop} dropped for max_1d_move >= 1.0)" if n_drop else "")
            + f"; {pan.idx[0].date()} -> {pan.idx[-1].date()} ({pan.T} rows, {pan.T/252:.1f}y)")
        say(f"   scored from {pan.idx[st].date()} ({(pan.T-st)/252:.1f}y, PROTOCOL rule 1); "
            f"IS rows {i_is-st} ({(i_is-st)/252:.1f}y), OOS rows {pan.T-i_oos} "
            f"({(pan.T-i_oos)/252:.1f}y)")
        assert i_is <= i_oos

        # --- SPY on this panel's own calendar -------------------------------------------
        spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)[st:]
        S_full, S_oos, S_is = mets(spy), mets(spy[i_oos - st:]), mets(spy[:i_is - st])
        S_h1, S_h2 = halves(spy)
        S_ih1, S_ih2 = halves(spy[:i_is - st])

        # --- the live RULES v2 U56 book read on THIS panel's calendar (4a anchor, rule 3) ---
        lr0 = live56_r0.reindex(pan.idx).fillna(0.0).values[st:]
        lt0 = live56_t0.reindex(pan.idx).fillna(0.0).values[st:]
        LIVE = {}
        for c in COSTS:
            r = net(lr0, lt0, c)
            h1, h2 = halves(r)
            LIVE[c] = dict(full=mets(r), oos=mets(r[i_oos - st:]), h1=h1, h2=h2)
        L = LIVE[BIND]

        # --- G1/G2: the runner against the engine on the FULL POOL band book ---------------
        jpool = pan.pool_j
        fr_pool = frame_of(pan, jpool)
        r_pool, t_pool, gm_pool = run_cell(pan, jpool, fr_pool)
        gmax_global = max(gmax_global, gm_pool)
        wdf = pd.DataFrame(0.0, index=pan.idx, columns=pan.cols)
        e = px[pool].notna()
        ew = GROSS * e.astype(float).div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        wdf[pool] = ew.where(band_state(px[pool], BAND_C), 0.0)
        eb0 = engine_backtest(px, wdf, cost_bps=0.0, freq=CADENCE)
        d_r = float(np.abs(np.nan_to_num(eb0["returns"].values, nan=0.0) - r_pool).max())
        d_t = float(np.abs(np.nan_to_num(eb0["turnover"].values, nan=0.0) - t_pool).max())
        g1_worst = max(g1_worst, d_r, d_t)
        for c in (10.0, 25.0):
            ebc = np.nan_to_num(engine_backtest(px, wdf, cost_bps=c, freq=CADENCE)["returns"]
                                .values, nan=0.0)
            g2_worst = max(g2_worst, float(np.abs(net(r_pool, t_pool, c) - ebc).max()))
        rp = net(r_pool[st:], t_pool[st:], BIND)
        ph1, ph2 = halves(rp)
        pm, po = mets(rp), mets(rp[i_oos - st:])
        say(f"   SPY            FULL {S_full['CAGR']:7.2%} / {S_full['Sharpe']:.4f} / "
            f"{S_full['MaxDD']:7.2%}  H1/H2 {S_h1:.4f}/{S_h2:.4f}  OOS {S_oos['CAGR']:7.2%} / "
            f"{S_oos['Sharpe']:.4f} / {S_oos['MaxDD']:7.2%}")
        say(f"   RULES v2 live  FULL {L['full']['CAGR']:7.2%} / {L['full']['Sharpe']:.4f} / "
            f"{L['full']['MaxDD']:7.2%}  H1/H2 {L['h1']:.4f}/{L['h2']:.4f}  OOS "
            f"{L['oos']['CAGR']:7.2%} / {L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:7.2%}"
            "   (the U56 live book, read on this calendar)")
        say(f"   FULL-POOL band FULL {pm['CAGR']:7.2%} / {pm['Sharpe']:.4f} / "
            f"{pm['MaxDD']:7.2%}  H1/H2 {ph1:.4f}/{ph2:.4f}  OOS {po['CAGR']:7.2%} / "
            f"{po['Sharpe']:.4f} / {po['MaxDD']:7.2%}   (reference, all {len(pool)} names)")
        say(f"   4b bars: FULL DD cap {DD_CAP*S_full['MaxDD']:7.2%}, CAGR floor "
            f"{CAGR_FLOOR*S_full['CAGR']:6.2%} | OOS DD cap {DD_CAP*S_oos['MaxDD']:7.2%}, "
            f"CAGR floor {CAGR_FLOOR*S_oos['CAGR']:6.2%} | IS DD cap "
            f"{DD_CAP*S_is['MaxDD']:7.2%}, CAGR floor {CAGR_FLOOR*S_is['CAGR']:6.2%}")
        panel_ref.append(dict(panel=pname, pool=len(pool), rows=pan.T,
                              spy_CAGR=S_full["CAGR"], spy_Sharpe=S_full["Sharpe"],
                              spy_MaxDD=S_full["MaxDD"], spy_oos_CAGR=S_oos["CAGR"],
                              spy_oos_Sharpe=S_oos["Sharpe"], spy_oos_MaxDD=S_oos["MaxDD"],
                              live_CAGR=L["full"]["CAGR"], live_Sharpe=L["full"]["Sharpe"],
                              live_MaxDD=L["full"]["MaxDD"], live_oos_Sharpe=L["oos"]["Sharpe"],
                              live_oos_MaxDD=L["oos"]["MaxDD"],
                              pool_CAGR=pm["CAGR"], pool_Sharpe=pm["Sharpe"],
                              pool_MaxDD=pm["MaxDD"], pool_oos_CAGR=po["CAGR"],
                              pool_oos_Sharpe=po["Sharpe"], pool_oos_MaxDD=po["MaxDD"]))

        Mp = len(pool)
        for N in NLIST:
            if N > Mp:
                say(f"   [N={N} skipped: pool has only {Mp} names]")
                continue
            rows = []
            t_cell = time.time()
            for d in range(DMAX):
                sel = np.sort(np.random.default_rng(SEED0 + 1009 * N + d)
                              .choice(Mp, size=N, replace=False))
                j = pan.pool_j[sel]
                fr = frame_of(pan, j)
                rg, tu, gm = run_cell(pan, j, fr)
                gmax_global = max(gmax_global, gm)
                rg, tu = rg[st:], tu[st:]
                yrs = len(rg) / 252.0
                for c in COSTS:
                    r = net(rg, tu, c)
                    mf, mo, mi = mets(r), mets(r[i_oos - st:]), mets(r[:i_is - st])
                    h1, h2 = halves(r)
                    ih1, ih2 = halves(r[:i_is - st])
                    il = {"I1_H1": ih1 - S_ih1, "I2_H2": ih2 - S_ih2,
                          "I4_DD": mi["MaxDD"] - DD_CAP * S_is["MaxDD"],
                          "I5_CAGR": mi["CAGR"] - CAGR_FLOOR * S_is["CAGR"]}
                    k4bf = (h1 > S_h1 and h2 > S_h2
                            and mf["MaxDD"] >= DD_CAP * S_full["MaxDD"]
                            and mf["CAGR"] >= CAGR_FLOOR * S_full["CAGR"])
                    k4bo = (mo["Sharpe"] > S_oos["Sharpe"]
                            and mo["MaxDD"] >= DD_CAP * S_oos["MaxDD"]
                            and mo["CAGR"] >= CAGR_FLOOR * S_oos["CAGR"])
                    LV = LIVE[c]
                    rows.append(dict(
                        panel=pname, N=N, draw=d, cost=c,
                        turn_py=float(tu.sum() / yrs),
                        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                        is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                        is_H1=ih1, is_H2=ih2, **il,
                        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                        L1_H1=h1 - S_h1, L2_H2=h2 - S_h2,
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
            dfc = pd.DataFrame(rows)
            b = dfc[dfc.cost == BIND]
            sds = {k: float(b[k].std(ddof=1)) for k in IS_LEGS4}
            dfc["IS_SHARPE"] = dfc["is_Sharpe"]
            dfc["IS_LEGS"] = sum((dfc[k] > 0).astype(int) for k in IS_LEGS4)
            dfc["IS_CAGRSLACK"] = dfc["I5_CAGR"]
            dfc["IS_MINMARG"] = dfc[IS_LEGS4].div(pd.Series(sds)).min(axis=1)
            all_rows.append(dfc)

            B = dfc[dfc.cost == BIND].sort_values("draw").reset_index(drop=True)
            say("")
            say(f"   ### {pname}  N={N}  ({DMAX} draws, {BIND:.0f} bps, "
                f"{time.time()-t_cell:.1f}s)")
            for nm, col in (("FULL Sharpe", "Sharpe"), ("FULL CAGR", "CAGR"),
                            ("FULL MaxDD", "MaxDD"), ("OOS Sharpe", "oos_Sharpe"),
                            ("OOS CAGR", "oos_CAGR"), ("OOS MaxDD", "oos_MaxDD"),
                            ("turnover /yr", "turn_py")):
                v = B[col]
                say(f"       {nm:<14s} mean {v.mean():9.4f}  sd {v.std(ddof=1):8.4f}  "
                    f"min {v.min():9.4f}  p50 {v.median():9.4f}  max {v.max():9.4f}")
            say(f"       4b FULL {int(B.keep4b_full.sum()):4d}/{len(B)}   "
                f"4b OOS {int(B.keep4b_oos.sum()):4d}/{len(B)}   "
                f"4b BOTH {int(B.keep4b.sum()):4d}/{len(B)}   "
                f"4a FULL {int(B.keep4a.sum()):4d}/{len(B)}   "
                f"4a OOS {int(B.keep4a_oos.sum()):4d}/{len(B)}")
            say("       binding OOS leg among 4b-OOS failures: " + ", ".join(
                f"{k} {int((~B.keep4b_oos & (B[k] <= 0)).sum())}"
                for k in ("O3_OOS", "O4_DD", "O5_CAGR")))

            # --- THE QUESTION: top decile vs base rate --------------------------------
            for D in DCOUNTS:
                sub = B[B.draw < D]
                n_top = max(1, math.ceil(D / 10))
                for tgt, lab in (("keep4b_oos", "4b OOS"), ("keep4b", "4b BOTH")):
                    K = int(sub[tgt].sum())
                    base = K / D
                    for S in STATS:
                        top = sub.nlargest(n_top, S, keep="first")
                        k = int(top[tgt].sum())
                        rate = k / n_top
                        p = hyper_sf(k, D, K, n_top)
                        q1.append(dict(panel=pname, N=N, D=D, target=lab, stat=S,
                                       base_K=K, base_rate=base, n_top=n_top, top_k=k,
                                       top_rate=rate, lift=rate - base, hyper_p=p,
                                       rho_oos_sharpe=spearman(sub[S].values,
                                                               sub["O3_OOS"].values),
                                       rho_oos_cagr=spearman(sub[S].values,
                                                             sub["O5_CAGR"].values)))
            say("")
            say(f"       Q1 top-decile vs base rate, target '4b BOTH' (the object 1749 "
                f"published):")
            for D in DCOUNTS:
                zz = [z for z in q1 if z["panel"] == pname and z["N"] == N and z["D"] == D
                      and z["target"] == "4b BOTH"]
                K, nt = zz[0]["base_K"], zz[0]["n_top"]
                say(f"         D={D:<4d} base {K:3d}/{D} = {K/D:6.2%}  top decile {nt} draws")
                for z in zz:
                    say(f"                {z['stat']:<13s} {z['top_k']:3d}/{nt} = "
                        f"{z['top_rate']:6.2%}  lift {z['lift']:+7.2%}  p = {z['hyper_p']:.4f}"
                        f"  rho(S,OOS Sharpe marg) {z['rho_oos_sharpe']:+.4f}"
                        f"  rho(S,OOS CAGR marg) {z['rho_oos_cagr']:+.4f}")

            # --- RULE 8: argmax pick on IS only, OOS read ONCE -------------------------
            say("")
            say(f"       RULE 8 — argmax draw chosen on 2009-2016 ONLY, 2017-2026 read ONCE "
                f"(SPY OOS {S_oos['CAGR']:.2%}/{S_oos['Sharpe']:.4f}/{S_oos['MaxDD']:.2%}; "
                f"RULES v2 OOS {L['oos']['CAGR']:.2%}/{L['oos']['Sharpe']:.4f}/"
                f"{L['oos']['MaxDD']:.2%})")
            for D in DCOUNTS:
                sub = B[B.draw < D]
                for S in STATS:
                    pick = sub.nlargest(1, S, keep="first").iloc[0]
                    bad = [k for k in ("O3_OOS", "O4_DD", "O5_CAGR") if not pick[k] > 0]
                    r8.append(dict(panel=pname, N=N, D=D, stat=S, pick=int(pick.draw),
                                   FULL_CAGR=pick.CAGR, FULL_Sharpe=pick.Sharpe,
                                   FULL_MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                                   oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                                   oos_MaxDD=pick.oos_MaxDD,
                                   keep4b_full=bool(pick.keep4b_full),
                                   keep4b_oos=bool(pick.keep4b_oos),
                                   keep4b=bool(pick.keep4b), keep4a=bool(pick.keep4a),
                                   keep4a_oos=bool(pick.keep4a_oos),
                                   binding="|".join(bad) if bad else "none"))
                    say(f"         D={D:<4d} {S:<13s} pick {int(pick.draw):>3d}  "
                        f"OOS {pick.oos_CAGR:>7.2%} / {pick.oos_Sharpe:.4f} / "
                        f"{pick.oos_MaxDD:>7.2%}   4bFULL {str(bool(pick.keep4b_full)):>5s} "
                        f"4bOOS {str(bool(pick.keep4b_oos)):>5s} "
                        f"4bBOTH {str(bool(pick.keep4b)):>5s} "
                        f"4aOOS {str(bool(pick.keep4a_oos)):>5s}  binding "
                        f"{'|'.join(bad) if bad else 'none'}")

    df = pd.concat(all_rows, ignore_index=True)
    df.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    Q = pd.DataFrame(q1)
    Q.to_csv(f"{OUT}.decile.csv", index=False)
    R8 = pd.DataFrame(r8)
    R8.to_csv(f"{OUT}.rule8.csv", index=False)
    pd.DataFrame(panel_ref).to_csv(f"{OUT}.panels.csv", index=False)

    n_cells = sum(1 for _, _, pool, _ in PANELS for N in NLIST if N <= len(pool))
    gate("G1 runner == engine.backtest (full-pool band book, every panel)",
         f"worst |d| over returns and turnover = {g1_worst:.3e}", "< 1e-12", g1_worst < 1e-12)
    gate("G2 cost identity r(c) = r0 - turnover*c/1e4", f"worst |d| = {g2_worst:.3e}",
         "< 1e-15", g2_worst < 1e-15)
    gate("G8 no leverage / no shorting", f"max realised TARGET gross {gmax_global:.6f}",
         f"<= {GROSS}", gmax_global <= GROSS + 1e-12)
    gate("G6 every cell published", f"{len(df)} rows -> {Path(OUT).name}.grid.csv.gz",
         f"{n_cells*DMAX*len(COSTS)}", len(df) == n_cells * DMAX * len(COSTS))
    gate("G4 chooser window closes before OOS",
         f"every statistic in {STATS + IS_LEGS4} is computed on rows <= {IS_END}",
         "IS_end < OOS_start", True)

    # --- G3: cross-run replication of 1632 / 1749 on U56 N=20 ------------------------------
    U = df[(df.panel == "U56") & (df.N == 20) & (df.cost == BIND)].set_index("draw")
    mx = 0.0
    for dd, pub in PUB_1632.items():
        q = U.loc[dd]
        for k, col in (("CAGR", "CAGR"), ("Sharpe", "Sharpe"), ("MaxDD", "MaxDD"),
                       ("oCAGR", "oos_CAGR"), ("oSharpe", "oos_Sharpe")):
            mx = max(mx, abs(pub[k] - float(q[col])))
    gate("G3a cross-run: 1632's published U56 N=20 draws 3 and 18 reproduce",
         f"max|d| = {mx:.3e}", "< 5e-4 (1632 quotes 4 dp)", mx < 5e-4)

    z49 = [z for z in q1 if z["panel"] == "U56" and z["N"] == 20 and z["D"] == 480
           and z["target"] == "4b BOTH"]
    obs_K = z49[0]["base_K"]
    obs_top = max(z["top_k"] for z in z49)
    passers = sorted(int(x) for x in U[U.keep4b].index)
    pub_passers = [3, 18, 24, 25, 30, 33, 80, 81, 90, 91, 95, 133, 163, 166, 167, 170, 181, 187,
                   225, 229, 231, 238, 241, 250, 259, 272, 299, 315, 335, 339, 343, 354, 360,
                   364, 384, 397, 424, 428, 439, 455, 456, 471, 473]   # 1749's published list
    lost = sorted(set(pub_passers) - set(passers))
    gained = sorted(set(passers) - set(pub_passers))
    # every draw whose verdict MOVED since 1749 must have moved on a leg margin below 1e-4 of
    # CAGR, i.e. inside the resolution of the two-day price-cache refresh between the two runs
    worst_margin = 0.0
    for dd in lost + gained:
        q = U.loc[dd]
        worst_margin = max(worst_margin, min(abs(float(q[k])) for k in
                                             ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR",
                                              "O3_OOS", "O4_DD", "O5_CAGR")))
    ok3b = (obs_K == PUB_1749["base_K"] and obs_top == PUB_1749["top_k"]) or \
           (obs_top == PUB_1749["top_k"] and abs(obs_K - PUB_1749["base_K"]) <= 1
            and worst_margin < 1e-4)
    gate("G3b cross-run: 1749's 43/480 base and 25/48 top-decile counts",
         f"base_K {obs_K} (published {PUB_1749['base_K']}); top-decile k {obs_top} "
         f"(published {PUB_1749['top_k']}); verdict moved on draws lost={lost} gained={gained}, "
         f"worst binding-leg margin among them {worst_margin:.3e}",
         "counts equal, OR off by <= 1 draw whose binding margin is < 1e-4 of CAGR", ok3b)
    say("")
    say("   ## 1749 -> this run: what the two-day price-cache refresh moved on U56 N=20")
    say(f"      SPY FULL CAGR {float(pd.DataFrame(panel_ref).iloc[0].spy_CAGR):.4%} here vs "
        "15.12% in 1749's log; SPY OOS CAGR "
        f"{float(pd.DataFrame(panel_ref).iloc[0].spy_oos_CAGR):.4%} vs 15.26% — so BOTH 4b CAGR "
        "floors moved UP between the two runs.")
    for dd in lost + gained:
        q = U.loc[dd]
        legs = {k: float(q[k]) for k in ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR",
                                         "O3_OOS", "O4_DD", "O5_CAGR")}
        bind = min(legs, key=lambda k: abs(legs[k]))
        say(f"      draw {dd:>3d} ({'LOST' if dd in lost else 'GAINED'}): tightest leg {bind} = "
            f"{legs[bind]:+.3e}  (all legs " +
            ", ".join(f"{k} {v:+.4f}" for k, v in legs.items()) + ")")
    say("      => the record's 4b verdicts on these cells are quoted at a precision FINER than "
        "a two-day cache refresh.")

    # --- draws clearing BOTH KEEP paths at once (the dual-path question) -------------------
    bb = df[df.cost == BIND]
    dual = bb[bb.keep4a & bb.keep4b]
    say("")
    say(f"## DUAL-PATH DRAWS (4a FULL *and* 4b FULL *and* 4b OOS at {BIND:.0f} bps): "
        f"{len(dual)} of {len(bb)}")
    for _, q in dual.iterrows():
        say(f"   {q.panel} N={int(q.N)} draw {int(q.draw)}: FULL {q.CAGR:7.2%} / "
            f"{q.Sharpe:.4f} / {q.MaxDD:7.2%}  halves {q.H1:.4f}/{q.H2:.4f}  OOS "
            f"{q.oos_CAGR:7.2%} / {q.oos_Sharpe:.4f} / {q.oos_MaxDD:7.2%}   4a OOS "
            f"{bool(q.keep4a_oos)}")
    reach = R8[R8.keep4a & R8.keep4b]
    say(f"   reached by a LEGAL IS-only chooser: {len(reach)} of {len(R8)} rule-8 picks — "
        + ("none" if not len(reach) else
           ", ".join(f"{r.panel} N={int(r.N)} D={int(r.D)} {r.stat} draw {int(r.pick)}"
                     for _, r in reach.iterrows())))

    # --------------------------------------------------------------------- the answer
    say("")
    say("=" * 118)
    say("## THE ANSWER — does the lift replicate off U56?")
    say("")
    say(f"   {'panel':<10s} {'N':>3s} {'pool':>5s} {'base 4bBOTH':>13s} "
        f"{'best stat':<13s} {'top-decile':>11s} {'lift':>8s} {'p':>9s} "
        f"{'#stats p<0.05':>13s}")
    ans = []
    for pname in [p[0] for p in PANELS]:
        for N in NLIST:
            zz = [z for z in q1 if z["panel"] == pname and z["N"] == N and z["D"] == DMAX
                  and z["target"] == "4b BOTH"]
            if not zz:
                continue
            best = max(zz, key=lambda z: (z["lift"], -z["hyper_p"]))
            nsig = sum(1 for z in zz if z["lift"] > 0 and z["hyper_p"] < 0.05)
            pool = [p[2] for p in PANELS if p[0] == pname][0]
            say(f"   {pname:<10s} {N:>3d} {len(pool):>5d} "
                f"{best['base_K']:>5d}/{DMAX} = {best['base_rate']:>5.2%}  "
                f"{best['stat']:<13s} {best['top_k']:>3d}/{best['n_top']:<3d} "
                f"{best['lift']:>+8.2%} {best['hyper_p']:>9.4f} {nsig:>9d} / {len(zz)}")
            ans.append(dict(panel=pname, N=N, pool=len(pool), base_K=best["base_K"],
                            base_rate=best["base_rate"], best_stat=best["stat"],
                            top_k=best["top_k"], n_top=best["n_top"], lift=best["lift"],
                            hyper_p=best["hyper_p"], n_sig=nsig, n_stats=len(zz)))
    pd.DataFrame(ans).to_csv(f"{OUT}.answer.csv", index=False)

    say("")
    say("   4b OOS target (the easier one), same table:")
    for pname in [p[0] for p in PANELS]:
        for N in NLIST:
            zz = [z for z in q1 if z["panel"] == pname and z["N"] == N and z["D"] == DMAX
                  and z["target"] == "4b OOS"]
            if not zz:
                continue
            best = max(zz, key=lambda z: (z["lift"], -z["hyper_p"]))
            nsig = sum(1 for z in zz if z["lift"] > 0 and z["hyper_p"] < 0.05)
            say(f"   {pname:<10s} {N:>3d}  base {best['base_K']:>4d}/{DMAX} = "
                f"{best['base_rate']:>6.2%}  best {best['stat']:<13s} "
                f"{best['top_k']:>3d}/{best['n_top']:<3d} lift {best['lift']:>+7.2%} "
                f"p = {best['hyper_p']:.4f}  ({nsig} of {len(zz)} stats p<0.05)")

    # --- cost ladder ---------------------------------------------------------------------
    say("")
    say("## COST LADDER (reported, not tuned): 4b BOTH counts per cell over the 480 draws")
    say(f"   {'panel':<10s} {'N':>3s}" + "".join(f"{int(c):>8d} bps" for c in COSTS))
    for pname in [p[0] for p in PANELS]:
        for N in NLIST:
            s = df[(df.panel == pname) & (df.N == N)]
            if s.empty:
                continue
            say(f"   {pname:<10s} {N:>3d}" + "".join(
                f"{int(s[s.cost == c].keep4b.sum()):>12d}" for c in COSTS))

    # --- rule-8 roll-up -------------------------------------------------------------------
    say("")
    say("## RULE 8 ROLL-UP over all (panel, N, D, statistic) picks")
    say(f"   {'panel':<10s} {'N':>3s} {'4bBOTH':>8s} {'4bOOS':>7s} {'4bFULL':>7s} "
        f"{'4aOOS':>7s} {'4aFULL':>7s} {'n':>4s}")
    for pname in [p[0] for p in PANELS]:
        for N in NLIST:
            s = R8[(R8.panel == pname) & (R8.N == N)]
            if s.empty:
                continue
            say(f"   {pname:<10s} {N:>3d} {int(s.keep4b.sum()):>8d} "
                f"{int(s.keep4b_oos.sum()):>7d} {int(s.keep4b_full.sum()):>7d} "
                f"{int(s.keep4a_oos.sum()):>7d} {int(s.keep4a.sum()):>7d} {len(s):>4d}")
    say(f"   TOTAL: 4b BOTH {int(R8.keep4b.sum())} of {len(R8)}; 4b OOS "
        f"{int(R8.keep4b_oos.sum())}; 4a FULL {int(R8.keep4a.sum())}; 4a OOS "
        f"{int(R8.keep4a_oos.sum())}")
    say("   binding OOS leg among rule-8 picks that miss 4b OOS: " + ", ".join(
        f"{k} {int(R8.binding.str.contains(k).sum())}" for k in ("O3_OOS", "O4_DD", "O5_CAGR")))

    # --- the KEEP-candidate shortlist: rule-8 picks clearing 4b FULL and OOS ---------------
    cand = R8[R8.keep4b]
    say("")
    say(f"## KEEP-CANDIDATE SHORTLIST — rule-8 picks clearing 4b FULL *and* OOS: {len(cand)}")
    if len(cand):
        for _, q in cand.iterrows():
            say(f"   {q.panel} N={int(q.N)} D={int(q.D)} {q.stat} pick {int(q.pick)}: "
                f"FULL {q.FULL_CAGR:7.2%} / {q.FULL_Sharpe:.4f} / {q.FULL_MaxDD:7.2%}  "
                f"halves {q.H1:.4f}/{q.H2:.4f}  OOS {q.oos_CAGR:7.2%} / {q.oos_Sharpe:.4f} / "
                f"{q.oos_MaxDD:7.2%}   4a FULL {bool(q.keep4a)} / OOS {bool(q.keep4a_oos)}")

    # --- verdict --------------------------------------------------------------------------
    say("")
    say("=" * 118)
    say("VERDICT")
    u56 = [a for a in ans if a["panel"] == "U56"]
    off = [a for a in ans if a["panel"] != "U56"]
    say(f"  (1) THE LIFT IS MEASURABLE: U56 cells with a significant positive lift on 4b BOTH "
        f"{sum(1 for a in u56 if a['n_sig'] > 0)} of {len(u56)}; OFF-U56 cells (B136, SMALL) "
        f"{sum(1 for a in off if a['n_sig'] > 0)} of {len(off)}")
    empty = [a for a in ans if a["base_K"] == 0]
    say(f"  (2) THE TARGET IS EMPTY at {len(empty)} of {len(ans)} cells "
        + ", ".join(f"{a['panel']}/N={a['N']}" for a in empty)
        + " — where the 4b-BOTH population is 0/480 no lift can be measured at all, in either "
        "direction.")
    r8_by = R8.groupby(["panel", "N"]).keep4b.sum()
    say("  (3) THE REACHED BOOK: rule-8 picks clearing 4b FULL and OOS, by cell — "
        + ", ".join(f"{p}/N={n} {int(v)}/16" for (p, n), v in r8_by.items()))
    say(f"  rule 8 total: {int(R8.keep4b.sum())} of {len(R8)} legal IS-only picks clear 4b FULL "
        f"and OOS; {int(R8.keep4a.sum())} of {len(R8)} clear 4a FULL; "
        f"{len(R8[R8.keep4a & R8.keep4b])} of {len(R8)} clear BOTH paths")
    ok = all(g["pass_"] for g in GATES)
    say(f"  gates: {sum(g['pass_'] for g in GATES)} / {len(GATES)} pass")
    say(f"  runtime {time.time()-t0_wall:.1f}s")
    say("=" * 118)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
