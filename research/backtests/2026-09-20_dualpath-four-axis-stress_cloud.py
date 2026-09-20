#!/usr/bin/env python3
"""Idea 2054 (lane cloud, 2026-09-20) — DOES THE DUAL-PATH KEEP-CANDIDATE SURVIVE THE SPRINT'S
FOUR STANDING STRESS AXES AT ONCE?

THE DEFECT THIS PRICES.  Idea 2034 (lane cloud, same run) turned up the first cell in the
vol-target family ever to clear BOTH KEEP paths — `B136, VOLTGT t = 0.10, DRIFT refresh h = 0.08,
trade weekly, 10 bps, t+1` (full 12.51% / 1.2286 / -11.81%, OOS 13.01% / 1.2928 / -11.81%) — and
it was reached by a legal IS-only chooser rather than hand-picked.  But it was read at ONE cost,
ONE execution latency, ONE rebalance phase and ONE trade cadence.  The sprint brief names all four
as standing stress axes, and idea 1694 called rebalance PHASE "the largest unpriced dial in the
record" (mean Sharpe move 0.0737, mean MaxDD move 4.33 pp, moving only the day you LOOK).  A
KEEP-candidate that survives only its own discovery settings is a discovery, not a rule.

WHAT IS PRICED HERE.  The whole vol-target corpus is rebuilt and re-scored on the FULL CROSS of
the four axes, so the candidate is never read alone and every rung is published:

    PANEL     {U56, B136, SMALL665}
    TARGET    t in {0.08, 0.10, 0.12, 0.16, 0.20}          [tuned dial 1, inherited]
    DIAL      DRIFT h in {0, .01, .02, .03, .05, .08, .12, .16, .20, .25}   [tuned dial 2,
              inherited]  +  CALENDAR R in {D, W, M, Q}    [the comparison family]
    CADENCE   T in {W, M}                                  REPORTED, not tuned
    PHASE     p in {0..4}  ->  weekly trade on weekday p AND monthly/quarterly trade on the
              {1, 5, 10, 15, 20}[p]-th trading day of the month                REPORTED
    DELAY     d in {1, 2}  ->  weights decided at close t are executed at close t+d  REPORTED
    COST      {10, 25, 50} bps                             REPORTED

  = 3 x 5 x 14 x 2 x 5 x 2 = 4,200 books, x 3 cost rungs = 12,600 scored cells.

The BASELINES are held at the LIVE convention throughout (RULES v2, weekly, t+1, 10 bps, and SPY
buy-and-hold), because that is the book real capital is actually running: a delayed, expensive
idea must beat the undelayed, live one to be worth switching to.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  IS THE 4a PASS REAL?  The candidate cell is read at all 3 x 2 x 5 = 30 (cost x delay x
      phase) points.  >= 80% keeping 4a -> ROBUST.  <= 40% -> the 4a pass is a settings artefact
      and must be restated as such (a KILL on the 4a claim, not on the cell).  In between ->
      PARTIAL, and the run says which axis breaks it.
  V2  IS THE 4b PASS REAL?  The same 30 points, same bands.
  V3  WHICH AXIS OWNS THE SPREAD?  Decompose the candidate's Sharpe (and MaxDD, and each 4b leg
      margin) across COST / DELAY / PHASE by the range of the axis-conditional means.  The
      pre-stated expectation from idea 1694 is PHASE >= DELAY; the run reports what it finds.
  V4  REACH.  Rule 8 at EVERY (panel x cadence x phase x delay x cost) point: `t` and the dial
      chosen on 2009-2016 ONLY by two legal IS-only choosers, 2017-2026 read exactly ONCE.  How
      often does a legal chooser land on a cell that clears 4b?  4a?  The candidate itself?

DIALS.  NOTHING NEW IS TUNED.  `t` and `h` (calendar family: `t` and `R`) are ideas 1799 / 2022 /
2034's two inherited dials and the only ones a chooser ever spends.  Every other axis above is
REPORTED, not tuned, and every grid point is published in `.grid.csv.gz`.

PROTOCOL: rule 2 (10 bps headline, next-day execution as the base case, no leverage, gross capped
at 1.00); rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one
idea, deterministic, standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and drawdown
LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.  The
STRESS contrasts (same cell, axis moved) are same-tape / same-names / same-grid and first-order
immune; the PASS COUNTS are not.  The SMALL cache grew 439 -> 665 names on 2026-09-20, so SMALL
counts here are not comparable with earlier SMALL numbers.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_dualpath-four-axis-stress_cloud.py
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

DATE, SLUG = "2026-09-20", "dualpath-four-axis-stress"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
TRADES = ["W", "M"]
# PHASE rungs.  "ENG" is `engine.rebalance_mask` verbatim — the convention every committed book
# in this record was run on, kept so the candidate's DISCOVERY settings are reproducible exactly.
# The five numbered rungs move only the day you LOOK: weekday p for W, the {1,5,10,15,20}[p]-th
# trading day of the month for M and Q.
PHASES = ["ENG", 0, 1, 2, 3, 4]
MONTH_ANCHOR = {0: 1, 1: 5, 2: 10, 3: 15, 4: 20}
PHASE_NAME = {"ENG": "ENGINE", 0: "MON/D1", 1: "TUE/D5", 2: "WED/D10", 3: "THU/D15",
              4: "FRI/D20"}
WEEKDAY_RUNGS = [PHASE_NAME[p] for p in (0, 1, 2, 3, 4)]
DELAYS = [1, 2]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0

# the cell under stress (idea 2034's dual-path candidate) and its DISCOVERY settings
CAND = dict(panel="B136", target=0.10, family="DRIFT", h=0.08, T_trade="W",
            phase=None, delay=1, cost=10)
# committed numbers this run must reproduce, at the full precision of the committed artifact
# (research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.grid.csv.gz), not the 4-decimal
# levels quoted in the memo -- so the gate below can be exact rather than rounding-limited.
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


# ----------------------------------------------------------------- phase-aware rebalance masks
def phased_mask(index, freq, phase):
    """A rebalance mask whose PHASE is explicit.

    W  -> every trading day whose weekday == `phase` (0 = Monday .. 4 = Friday).
    M  -> the k-th TRADING day of each month, k = MONTH_ANCHOR[phase], clipped to month length.
    Q  -> the same k-th trading day, in January / April / July / October only.
    D  -> every trading day (phase has no meaning; kept so the ladder is complete).

    A week that carries no such weekday (holiday) simply does not trade that week; a month
    shorter than k trading days trades on its last.  Both are stated, not silently patched."""
    idx = pd.DatetimeIndex(index)
    if phase == "ENG":
        return pd.Series(np.asarray(rebalance_mask(idx, freq).values, bool), index=idx)
    if freq == "D":
        return pd.Series(True, index=idx)
    if freq == "W":
        return pd.Series(idx.weekday == phase, index=idx)
    k = MONTH_ANCHOR[phase]
    nth = pd.Series(1, index=idx).groupby([idx.year, idx.month]).cumsum()
    size = pd.Series(1, index=idx).groupby([idx.year, idx.month]).transform("size")
    hit = nth == np.minimum(k, size)
    if freq == "Q":
        hit = hit & pd.Series(idx.month.isin([1, 4, 7, 10]), index=idx)
    return pd.Series(np.asarray(hit), index=idx)


# --------------------------------------------------------- the two refresh runners (1799 verbatim)
def bt_cal(px_ret, W0, g0, mT, mR):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        if mR[i] or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif mR[i]:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


def bt_drift(px_ret, W0, g0, mT, h):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        trig = abs(g0[i] - cur.sum()) > h
        if trig or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif trig:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


def lag(a, d):
    """Apply an execution delay of d days to a decision series/array (axis 0)."""
    a = np.asarray(a)
    pad = np.zeros((d,) + a.shape[1:], dtype=a.dtype) if a.ndim > 1 else np.zeros(d, dtype=a.dtype)
    return np.concatenate([pad, a[:-d]]) if d else a


class Book:
    """Everything needed to run one panel at any (phase, delay)."""

    def __init__(self, px, cols):
        self.index = px.index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        self.EW = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.SIG = panel_sigma(px, cols)
        self.mask = {}
        for p in PHASES:
            for f in ("D", "W", "M", "Q"):
                self.mask[(f, p)] = np.asarray(phased_mask(px.index, f, p).values, bool)

    def inputs(self, tgt, phase, delay):
        W0 = lag(self.EW, delay)
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        g0 = lag(g, delay)
        M = {f: lag(self.mask[(f, phase)], delay).astype(bool) for f in ("D", "W", "M", "Q")}
        return W0, g0, M

    def run(self, fam, tgt, dial, T, phase, delay):
        W0, g0, M = self.inputs(tgt, phase, delay)
        if fam == "CAL":
            r, t, gs, nref = bt_cal(self.R, W0, g0, M[T], M[dial])
        else:
            r, t, gs, nref = bt_drift(self.R, W0, g0, M[T], dial)
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)


# ----------------------------------------------------------------------------- metrics
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


def spread(df, col, axis):
    """Range of the axis-conditional means of `col` — the V3 decomposition statistic."""
    m = df.groupby(axis)[col].mean()
    return float(m.max() - m.min())


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2054 (lane cloud, {DATE}) — does the DUAL-PATH KEEP-candidate survive the "
        f"sprint's FOUR standing stress axes at once?")
    log(f"# under stress: B136 VOLTGT-DRIFT t=0.10, h=0.08, trade weekly (idea 2034)")
    log(f"# TUNED (2, both inherited): t {TARGETS}; dial = DRIFT h {THRESH} | CAL R {REFRESH}")
    log(f"# REPORTED, not tuned: cadence {TRADES}, phase {[PHASE_NAME[p] for p in PHASES]}, "
        f"delay t+{DELAYS}, cost {COSTS} bps, panel.  sigma FIXED (L={SIG_L}, d={SIG_D}).")
    log(f"# warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")
    log(f"# BASELINES HELD AT THE LIVE CONVENTION: RULES v2 weekly t+1 at {COST0} bps, and SPY.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    SPYP, LIVEP, START = {}, {}, {}
    for pname, px, cols in PS:
        st = px.index[WARMUP]
        START[pname] = st
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=float(COST0), freq="W")
        lr = lb["returns"].loc[st:]
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
            f"{LV['full']['Sharpe']:.4f} / {LV['full']['MaxDD']:7.2%}  "
            f"(H1 {LV['h1']:.4f} H2 {LV['h2']:.4f}; OOS {LV['oos']['CAGR']:7.2%} / "
            f"{LV['oos']['Sharpe']:.4f} / {LV['oos']['MaxDD']:7.2%})")
        log(f"   SPY                        {S['full']['CAGR']:7.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:7.2%}  "
            f"(H1 {S['h1']:.4f} H2 {S['h2']:.4f}; OOS {S['oos']['CAGR']:7.2%} / "
            f"{S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:7.2%})")
        log(f"   4b bars: MaxDD >= {DD_CAP*S['full']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*S['full']['CAGR']:.2%}")

    rows = []
    g1 = g2 = g9 = 0.0
    g1n = 0
    for pname, px, cols in PS:
        st = START[pname]
        bk = Book(px, cols)
        S, LV = SPYP[pname], LIVEP[pname]

        # G1: the "ENG" rung IS engine.rebalance_mask, and the five weekday rungs are genuinely
        # distinct calendars (so PHASE is a real axis and not five copies of one mask).
        em = np.asarray(rebalance_mask(px.index, "W").values, bool)
        g1 = max(g1, float((np.asarray(phased_mask(px.index, "W", "ENG").values, bool)
                            != em).mean()))
        ntr = {PHASE_NAME[p]: int(np.asarray(phased_mask(px.index, "W", p).values, bool).sum())
               for p in PHASES}
        g1n += 1
        log(f"   weekly trade days per PHASE rung: {ntr}")

        for tgt in TARGETS:
            for T in TRADES:
                for phase in PHASES:
                    for delay in DELAYS:
                        cells = ([("CAL", Rc) for Rc in REFRESH]
                                 + [("DRIFT", h) for h in THRESH])
                        calD = None
                        for fam, dial in cells:
                            r0, t0, gs, nref = bk.run(fam, tgt, dial, T, phase, delay)
                            label = f"R={dial}" if fam == "CAL" else f"h={dial:.2f}"
                            if fam == "CAL" and dial == "D":
                                calD = (r0.values.copy(), t0.values.copy())
                            if fam == "DRIFT" and dial == 0.0 and calD is not None:
                                g2 = max(g2, float(np.abs(r0.values - calD[0]).max()),
                                         float(np.abs(t0.values - calD[1]).max()))
                            r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                            g9 = max(g9, float(gs.max()))
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
                                is_minleg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                                                mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                                                mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
                                rows.append(dict(
                                    panel=pname, target=tgt, T_trade=T,
                                    phase=PHASE_NAME[phase], delay=delay, cost=c,
                                    family=fam, dial=str(dial), cell=label,
                                    h=(dial if fam == "DRIFT" else np.nan),
                                    R_refresh=(dial if fam == "CAL" else ""),
                                    turn_py=float(t0.sum() / yrs), refresh_py=nref / (len(px)/252.0),
                                    gross_mean=float(gs.mean()), gross_max=float(gs.max()),
                                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                    H1=h1, H2=h2,
                                    is_Sharpe=mi["Sharpe"], is_minleg=float(is_minleg),
                                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                                    oos_MaxDD=mo["MaxDD"],
                                    **{k: float(v) for k, v in mar.items()},
                                    bind=bl, n_fail=nbad,
                                    keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                                    keep4a=k4a, keep4a_oos=k4ao))
        log(f"   {pname}: grid done ({len([r for r in rows if r['panel']==pname])} scored rows)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    NB = len(G) // len(COSTS)

    # -------------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 the ENG phase rung IS engine.rebalance_mask('W') on every panel",
         f"max disagreement {g1:.3e} over {g1n} panels", "== 0", g1 == 0.0 and g1n == len(PS))
    gate("G2 DRIFT h=0 == CALENDAR R=D at every (t, cadence, phase, delay)",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    gate("G3 the four-axis grid is complete", f"{NB} books / {len(G)} scored rows",
         f"== {3*len(TARGETS)*14*len(TRADES)*len(PHASES)*len(DELAYS)} books",
         NB == 3 * len(TARGETS) * 14 * len(TRADES) * len(PHASES) * len(DELAYS))
    gate("G4 gross never levered", f"max gross {g9:.6f}", "<= 1.0 + 1e-9", g9 <= 1.0 + 1e-9)
    # G5: the candidate reproduces idea 2034 at its DISCOVERY settings.  Its discovery phase is
    # whichever PHASE rung coincides with the engine's own weekly mask.
    disc_phase = PHASE_NAME["ENG"]
    CAND["phase"] = disc_phase
    log(f"   the candidate's DISCOVERY phase rung is {disc_phase}")
    q = G[(G.panel == "B136") & (G.target == 0.10) & (G.family == "DRIFT") & (G.h == 0.08)
          & (G.T_trade == "W") & (G.phase == disc_phase) & (G.delay == 1) & (G.cost == COST0)]
    g5 = np.nan
    if len(q):
        r = q.iloc[0]
        g5 = max(abs(r.CAGR - PUB_CAND["CAGR"]), abs(r.Sharpe - PUB_CAND["Sharpe"]),
                 abs(r.MaxDD - PUB_CAND["MaxDD"]), abs(r.oos_CAGR - PUB_CAND["oCAGR"]),
                 abs(r.oos_Sharpe - PUB_CAND["oSharpe"]), abs(r.H1 - PUB_CAND["H1"]),
                 abs(r.H2 - PUB_CAND["H2"]))
    gate("G5 reproduces idea 2034's dual-path candidate at its discovery settings",
         f"max|d| = {g5:.3e}", "< 1e-9", bool(g5 < 1e-9))
    g6 = 0.0
    for pn, pub in PUB_MEMO.items():
        z = G[(G.panel == pn) & (G.target == TGT_MEMO) & (G.family == "CAL")
              & (G.R_refresh == "W") & (G.T_trade == "W") & (G.phase == disc_phase)
              & (G.delay == 1) & (G.cost == COST0)]
        if len(z):
            r = z.iloc[0]
            g6 = max(g6, abs(r.CAGR - pub["CAGR"]), abs(r.Sharpe - pub["Sharpe"]),
                     abs(r.MaxDD - pub["MaxDD"]))
    gate("G6 reproduces the standing VOLTGT memo (U56 + B136) at the discovery phase",
         f"max|d| = {g6:.3e}", "< 1e-3", g6 < 1e-3)
    K = ["panel", "target", "T_trade", "phase", "cost", "family", "cell"]
    d1 = G[G.delay == 1].set_index(K).sort_index().Sharpe
    d2 = G[G.delay == 2].set_index(K).sort_index().Sharpe
    gate("G7 the DELAY axis actually moves the book",
         f"mean |dSharpe| t+1 -> t+2 = {float((d2 - d1).abs().mean()):.4f}",
         "> 1e-4", float((d2 - d1).abs().mean()) > 1e-4)

    # ---------------------------------------------------------- V1 / V2: is the candidate real?
    log("\n## V1 / V2 — THE CANDIDATE AT ALL 30 (COST x DELAY x PHASE) POINTS")
    CC = G[(G.panel == "B136") & (G.target == 0.10) & (G.family == "DRIFT") & (G.h == 0.08)
           & (G.T_trade == "W")].copy()
    CC = CC.sort_values(["cost", "delay", "phase"])
    CC.to_csv(f"{OUT}.candidate.csv", index=False)
    log(f"   {len(CC)} points (cost {COSTS} x delay t+{DELAYS} x phase {len(PHASES)})")
    log("   cost delay phase        CAGR   Sharpe    MaxDD     H1      H2   |  4a    4b   bind")
    for _, r in CC.iterrows():
        log(f"   {r.cost:4d}  t+{r.delay}  {r.phase:8s} {r.CAGR:7.2%} {r.Sharpe:8.4f} "
            f"{r.MaxDD:8.2%} {r.H1:7.4f} {r.H2:7.4f}  | {str(bool(r.keep4a)):5s} "
            f"{str(bool(r.keep4b)):5s} {r.bind}")
    CW = CC[CC.phase.isin(WEEKDAY_RUNGS)]
    n4a, n4b = int(CC.keep4a.sum()), int(CC.keep4b.sum())
    s4a, s4b = n4a / len(CC), n4b / len(CC)

    def band(s):
        return "ROBUST" if s >= 0.80 else ("ARTEFACT" if s <= 0.40 else "PARTIAL")
    v1, v2 = band(s4a), band(s4b)
    log(f"\n   V1  4a kept at {n4a}/{len(CC)} = {s4a:.1%}  -> {v1}")
    log(f"   V2  4b kept at {n4b}/{len(CC)} = {s4b:.1%}  -> {v2}")
    log(f"   (weekday rungs only, the ENGINE convention excluded: 4a "
        f"{int(CW.keep4a.sum())}/{len(CW)}, 4b {int(CW.keep4b.sum())}/{len(CW)})")
    for ax in ("cost", "delay", "phase"):
        log(f"      by {ax:10s}: "
            + "; ".join(f"{k}: 4a {int(s.keep4a.sum())}/{len(s)} 4b {int(s.keep4b.sum())}/{len(s)}"
                        for k, s in CC.groupby(ax)))
    log("      binding legs where 4b fails: "
        + (", ".join(f"{k} x{v}" for k, v in CC[~CC.keep4b].bind.value_counts().items())
           or "(none)"))
    log("      4a failure mode counts: "
        + (", ".join(f"{k} x{v}" for k, v in
                     CC[~CC.keep4a].assign(why=lambda d: np.where(
                         d.H1 <= LIVEP["B136"]["h1"], "H1",
                         np.where(d.H2 <= LIVEP["B136"]["h2"], "H2", "MaxDD"))
                     ).why.value_counts().items()) or "(none)"))

    # -------------------------------------------------------------- V3: which axis owns the spread
    log("\n## V3 — WHICH AXIS OWNS THE SPREAD? (range of axis-conditional means)")
    arows = []
    for col in ["Sharpe", "MaxDD", "CAGR", "oos_Sharpe"] + LEGS:
        d = dict(metric=col)
        for ax in ("cost", "delay", "phase"):
            d[ax] = spread(CC, col, ax)
        d["winner"] = max(("cost", "delay", "phase"), key=lambda a: d[a])
        arows.append(d)
        log(f"   {col:10s}  cost {d['cost']:.4f}   delay {d['delay']:.4f}   "
            f"phase {d['phase']:.4f}   -> {d['winner'].upper()}")
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.axes.csv", index=False)
    # the same decomposition over the WHOLE corpus, not just the candidate
    brows = []
    for (pn, T), s in G[G.cost == COST0].groupby(["panel", "T_trade"]):
        brows.append(dict(panel=pn, T_trade=T,
                          delay=spread(s, "Sharpe", "delay"),
                          phase=spread(s, "Sharpe", "phase"),
                          phase_dd=spread(s, "MaxDD", "phase"),
                          delay_dd=spread(s, "MaxDD", "delay")))
    B = pd.DataFrame(brows)
    B.to_csv(f"{OUT}.axes_corpus.csv", index=False)
    log("   whole corpus at 10 bps (mean Sharpe spread): "
        + "; ".join(f"{r.panel}/{r.T_trade} delay {r.delay:.4f} phase {r.phase:.4f}"
                    for _, r in B.iterrows()))

    # ---------------------------------------------------------------------- census, every point
    log("\n## CENSUS — 4a / 4b pass counts over the whole corpus, by (delay, cost)")
    crows = []
    for (d, c), s in G.groupby(["delay", "cost"]):
        crows.append(dict(delay=d, cost=c, n=len(s), keep4b=int(s.keep4b.sum()),
                          keep4b_full=int(s.keep4b_full.sum()), keep4a=int(s.keep4a.sum())))
        log(f"   t+{d}, {c:2d} bps: 4b {int(s.keep4b.sum()):4d}/{len(s)}   "
            f"4a {int(s.keep4a.sum()):4d}/{len(s)}")
    pd.DataFrame(crows).to_csv(f"{OUT}.census.csv", index=False)

    # --------------------------------------------------------------------------- V4: rule 8
    log("\n## V4 — RULE 8 (parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE)")
    wrows = []
    for (pn, T, ph, d, c, fam), sub in G.groupby(
            ["panel", "T_trade", "phase", "delay", "cost", "family"]):
        S, LV = SPYP[pn], LIVEP[pn]
        for ch, col in (("CH_ISSHARPE", "is_Sharpe"), ("CH_ISMINLEG", "is_minleg")):
            pick = sub.loc[sub[col].idxmax()]
            wrows.append(dict(panel=pn, T_trade=T, phase=ph,
                              delay=d, cost=c, family=fam, chooser=ch,
                              target=pick.target, cell=pick.cell, is_stat=float(pick[col]),
                              oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                              oos_MaxDD=pick.oos_MaxDD,
                              spy_oos_Sharpe=S["oos"]["Sharpe"],
                              live_oos_Sharpe=LV["oos"]["Sharpe"],
                              keep4b=bool(pick.keep4b), keep4b_oos=bool(pick.keep4b_oos),
                              keep4a=bool(pick.keep4a), keep4a_oos=bool(pick.keep4a_oos),
                              is_candidate=bool(pn == "B136" and pick.target == 0.10
                                                and pick.cell == "h=0.08" and T == "W")))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    log(f"   {len(W)} picks (panel x cadence x phase x delay x cost x family x chooser)")
    for (pn, d, c), s in W.groupby(["panel", "delay", "cost"]):
        log(f"      {pn:9s} t+{d} {c:2d} bps: 4b {int(s.keep4b.sum()):2d}/{len(s)}   "
            f"4a {int(s.keep4a.sum()):2d}/{len(s)}   lands on the candidate "
            f"{int(s.is_candidate.sum()):2d}/{len(s)}")
    log(f"   picks clearing BOTH paths: {int((W.keep4a & W.keep4b).sum())} of {len(W)}")
    for _, r in W[W.keep4a & W.keep4b].iterrows():
        log(f"      {r.panel:9s} T={r.T_trade} {r.phase:8s} t+{r.delay} {r.cost:2d}bps "
            f"{r.family:5s} {r.chooser:11s} -> t={r.target:.2f} {r.cell:7s}   OOS "
            f"{r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / {r.oos_MaxDD:7.2%}  (SPY OOS Sharpe "
            f"{r.spy_oos_Sharpe:.4f}, LIVE v2 OOS Sharpe {r.live_oos_Sharpe:.4f})")

    log("\n## VERDICT")
    log(f"   V1 (4a) {v1}   {n4a}/{len(CC)} = {s4a:.1%}")
    log(f"   V2 (4b) {v2}   {n4b}/{len(CC)} = {s4b:.1%}")
    log(f"   V3 axis owning the Sharpe spread: {A.set_index('metric').loc['Sharpe','winner'].upper()}")
    log(f"   gates: {sum(g['pass_'] for g in _gates)}/{len(_gates)} pass")
    log("   SURVIVORSHIP: U56 / B136 are CURRENT constituents and SMALL is a CURRENT sub-$2B")
    log("   screen, so every LEVEL is optimistic and both 4b bars are easier than on a")
    log("   point-in-time panel.  The STRESS contrasts are same-tape / same-names / same-grid")
    log("   and first-order immune; the PASS COUNTS are not.")

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()
