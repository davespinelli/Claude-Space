#!/usr/bin/env python3
"""Idea 2075 (lane C, 2026-09-21) — DOES THE 4:1 ASYMMETRY RATIO MATTER, OR IS ANY TIGHT
DOWN-TRIGGER THE SAME?

THE DEFECT THIS PRICES.  Idea 2026 priced a TWO-SIDED drift trigger on the standing VOLTGT book
(`g_t = clip(t / sigma20_panel, 0, 1)`, re-read only when held gross has drifted from `g_t`) and
found the asymmetric version — TIGHT on the way DOWN, LOOSE on the way UP — worth +1.01 pp (fixed
base) / +0.61 pp (`f*g_t` base) of OOS MaxDD for -0.33 / -0.16 pp of OOS CAGR at +0.26 / +0.23
turns/yr.  But the down/up ratio was PRE-STATED at 4:1 and NEVER LADDERED.  A pre-stated constant
that is never laddered is not a finding: it could be the argmax of a sharp profile (in which case
4 is information the record does not own) or a point on a flat one (in which case ANY tight down
trigger buys the same drawdown and the 4 is decoration).

WHAT IS LADDERED.  The trigger re-reads the scalar on day i iff

    g_t[i] - gross_held > h_up[i]        (the book must gross UP)     or
    gross_held - g_t[i] > h_dn[i]        (the book must gross DOWN)

and the ratio dial `A` sets the two sides from ONE base threshold `b`:

    A in {1, 2, 4, 8, 16}    h_up = b,      h_dn = b / A        (A = 1 is the SYMMETRIC twin)
    A = DOWNONLY             h_up = +inf,   h_dn = b            (the up-side trigger REMOVED,
                                                                 down side at the UNCHANGED base)
    A = UPONLY               h_up = b,      h_dn = +inf         (reported CONTROL, the mirror)
    A = DOWNONLY_TD          h_up = +inf,   h_dn = b, AND the scheduled TRADE day re-reads `g_t`
    A = A1_TD                h_up = h_dn = b, same trade-day re-read (DOWNONLY_TD's MATCHED twin)

STRUCTURAL NOTE, AND A POST-HOC REPAIR DECLARED AS SUCH.  The two `_TD` rungs were ADDED AFTER the
first run of this script, once the PURE `DOWNONLY` rung came back degenerate, and the finding that
forced them is reported as a result rather than patched away.  In ideas 1799 / 2026 the drift
trigger is the book's ONLY channel for re-reading the exposure scalar `g_t`: the scheduled trade
day re-spreads the NAMES at the scalar already in force but never re-reads it.  Deleting the
up-side threshold therefore deletes the book's only RE-ENTRY channel, and the book is ABSORBING at
whatever gross it first held (here 0, since `g_0` is the pre-shift sentinel) for the whole tape —
zero return, zero turnover, on 100% of cells.  A pure down-only trigger is not a strategy on this
construction, it is a one-way ratchet.  The `_TD` pair restores re-entry through the trade cadence
and is the nearest WELL-DEFINED "no up-side threshold" book; V3 is judged on that matched pair and
is flagged POST-HOC throughout.  V1, V2 and V4 are unchanged and remain pre-stated.

DOWNONLY is deliberately NOT the A -> inf limit: it holds the down side at the base and deletes the
up side, so DOWNONLY vs A=1 isolates REMOVING THE UP TRIGGER while A > 1 isolates TIGHTENING THE
DOWN TRIGGER.  Both are read, at BOTH bases the record owns:

    FIXH   b = h            (a constant, idea 1799's incumbent)
    FRACG  b = f * g_t      (a fixed fraction of the scalar in force, idea 2026's KEEP-4b base)

DIALS.  EXACTLY TWO are tuned: the RATIO `A` x the family's own BASE rung.  REPORTED, NOT TUNED:
TARGET `t` (PRE-STATED at the inherited 0.16 for every headline; the whole `t` ladder is published
but no chooser ever reads it), TRADE cadence `T in {W, M}`, PANEL {U56, B136, SMALL}, COST
{0, 10, 25, 50} bps.  The sigma convention is FIXED at the standing memo's (L = 20, d = 0).  The
CALENDAR ladder `R in {D,W,M,Q}` is priced as a REPORTED comparand, never chosen over.

PRE-STATED VERDICT RULES (fixed HERE, before the run, never adjusted afterwards).  All are read at
t* = 0.16, 10 bps, on the four LARGE-panel arms (U56/B136 x W/M), pooled over base rungs:
  V1  SATURATION.  The pooled mean OOS MaxDD credit over A=1 is NON-DECREASING in A across
      {1,2,4,8,16} AND the last step (8 -> 16) contributes LESS THAN 25% of the whole 1 -> 16
      credit.  Triggered -> the drawdown credit SATURATES at or before A = 8 and the 4:1 choice is
      a point on a saturating profile, not an argmax.
  V2  THE CAGR COST IS REAL.  The pooled mean OOS CAGR cost is MONOTONE NON-INCREASING in A (i.e.
      tightening the down side only ever costs return).  Reported with the first A at which the 4b
      CAGR floor leg `L5_CAGR` goes NEGATIVE at the pre-stated base on any large-panel arm.
  V3  DOMINANCE (the idea's own question).  DOWNONLY WEAKLY dominates its symmetric twin A=1 at the
      SAME base on ALL FOUR of {OOS Sharpe, OOS MaxDD, OOS CAGR, turnover (lower is better)} on at
      least 50% of (arm x base) pairs, AND strictly on at least one axis at the pooled mean.  Not
      triggered -> DOWN-ONLY does NOT dominate and the up-side threshold is earning something.
      READ TWICE: (V3-pure) on the pre-stated DOWNONLY vs A=1, which is decided by the absorbing
      structure above and not by returns, and (V3-TD, POST-HOC) on DOWNONLY_TD vs its matched
      A1_TD twin, which is the version with economic content.
  V4  DOES THE RATIO MATTER AT ALL.  Over the whole (base x arm) grid the OOS 4b FULL+OOS pass
      COUNT differs between the best and the worst A rung by MORE THAN 10% of the best.  Not
      triggered -> ANY tight down trigger is the same and the pre-stated 4 carries no information.
  V5  CAPITAL.  Both KEEP paths are scored at EVERY cell.  Any cell clearing 4b FULL *and* OOS that
      is PRE-STATED (A* = 4, the record's own constant) or reached by a LEGAL IS-only chooser is a
      KEEP-4b candidate and is reported with its binding leg and its margins.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The RATIO contrast is same-tape / same-names / same-grid with only the trigger's two sides moved,
so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-21_asymmetry-ratio-ladder_C.py
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

DATE, SLUG = "2026-09-21", "asymmetry-ratio-ladder"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.10, 0.12, 0.16, 0.20]
TGT_STAR = 0.16                      # INHERITED from the standing VOLTGT memo; not chosen here
TRADES = ["W", "M"]
REFRESH = ["D", "W", "M", "Q"]

A_NUM = [1.0, 2.0, 4.0, 8.0, 16.0]
A_RUNGS = [1.0, 2.0, 4.0, 8.0, 16.0, "DOWNONLY", "UPONLY", "DOWNONLY_TD", "A1_TD"]
TD_RUNGS = {"DOWNONLY_TD", "A1_TD"}      # the only rungs that re-read on trade days
A_STAR = 4.0                         # the record's PRE-STATED ratio, the object under test
BASE_H = [0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
BASE_F = [0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
H_STAR, F_STAR = 0.12, 0.10          # the record's PRE-STATED bases
BASES = {"FIXH": BASE_H, "FRACG": BASE_F}

SIG_L, SIG_D = 20, 0
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
CRASH = ("2020-02-19", "2020-03-23")          # idea 2022's window, quoted not re-derived
BIG = ["U56", "B136"]

# committed numbers this run must reproduce (gates G1 / G2)
PUB_1799 = dict(CAGR=0.156208, Sharpe=1.24509, MaxDD=-0.181592,        # U56 t=.16 h=.12 T=M 10bps
                oCAGR=0.16359, oSharpe=1.28099, oMaxDD=-0.181592)
PUB_2026 = dict(CAGR=0.1581, Sharpe=1.2470, MaxDD=-0.1912,             # U56 t=.16 f=.10 T=M 10bps
                oCAGR=0.1655, oSharpe=1.2928, oMaxDD=-0.1912)

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
    return ([("U56", px56, [c for c in px56.columns]),
             ("B136", px136, [c for c in px136.columns]),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio through close
    t-d.  (L, d) = (20, 0) is the standing memo's convention (idea 1771 owns that surface)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------ the two refresh runners
def bt_cal(px_ret, W0, g0, mT, mR):
    """CALENDAR refresh (idea 1767's two-schedule construction, verbatim)."""
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


def bt_var(px_ret, W0, g0, mT, hup, hdn, td_read=False):
    """DRIFT refresh with a TWO-SIDED, possibly TIME-VARYING threshold (idea 2026's runner,
    verbatim at `td_read=False`).  `hup = +inf` deletes the gross-UP trigger; `hdn = +inf` deletes
    the gross-DOWN trigger; `hup == hdn == h` is idea 1799's symmetric `bt_drift`.

    `td_read=True` adds a SECOND refresh channel: the scheduled TRADE day also re-reads the
    scalar.  This is OFF for every rung of the pre-stated A ladder (which is 2026's construction
    exactly) and ON only for the two `_TD` rungs, where it is the RE-ENTRY channel a down-only
    trigger has to borrow from somewhere — see the structural note on DOWNONLY in the memo."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        gh = cur.sum()
        trig = (g0[i] - gh > hup[i]) or (gh - g0[i] > hdn[i])
        tday = mT[i] or i == 0
        if trig or i == 0 or (td_read and tday):
            g_eff = g0[i]
            nref += 1
        if tday:
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


class Book:
    """Pre-shifted arrays for one panel, so every (t, T, base, A) run is a single loop."""

    def __init__(self, px, cols, index):
        self.index = index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])       # decided t, applied t+1
        self.SIG = panel_sigma(px, cols)
        self.masks = {}
        for f in ("D", "W", "M", "Q"):
            m = np.asarray(rebalance_mask(index, f).values, bool)
            self.masks[f] = np.concatenate([[False], m[:-1]])
        self._g = {}

    def g_of(self, tgt):
        if tgt not in self._g:
            g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
            self._g[tgt] = np.concatenate([[0.0], g[:-1]])
        return self._g[tgt]

    def thresholds(self, tgt, fam, base, A):
        """ONE base vector, TWO sides set by the ratio dial A."""
        g0, n = self.g_of(tgt), len(self.R)
        b = np.full(n, float(base)) if fam == "FIXH" else float(base) * g0
        inf = np.full(n, np.inf)
        if A in ("DOWNONLY", "DOWNONLY_TD"):
            return inf, b
        if A == "UPONLY":
            return b, inf
        if A == "A1_TD":
            return b, b
        return b, b / float(A)

    def run(self, tgt, T, fam, base, A=None):
        g0 = self.g_of(tgt)
        if fam == "CAL":
            r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[base])
        else:
            hu, hd = self.thresholds(tgt, fam, base, A)
            r, t, gs, nref = bt_var(self.R, self.W, g0, self.masks[T], hu, hd,
                                    td_read=(A in TD_RUNGS))
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


def score_cell(r0, t0, gs, nref, c, S, LV, nyears):
    r = net(r0, t0, c)
    mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
    h1, h2 = halves(r)
    ih1, ih2 = halves(r.loc[:IS_END])
    mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
           "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
           "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
           "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
    bl, nbad = binding(mar)
    k4bf = (h1 > S["h1"] and h2 > S["h2"]
            and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
            and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
    k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
            and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
            and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
    k4a = (h1 > LV["h1"] and h2 > LV["h2"] and mf["MaxDD"] >= LV["full"]["MaxDD"])
    k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"] and mo["MaxDD"] >= LV["oos"]["MaxDD"])
    is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
               + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
               + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
    isr = r.loc[:IS_END]
    return dict(
        cost=c, turn_py=float(t0.sum() / nyears),
        is_turn_py=float(t0.loc[:IS_END].sum() / (len(isr) / 252.0)),
        refresh_py=nref / (len(r0) / 252.0),
        gross_mean=float(gs.mean()), gross_min=float(gs.min()), gross_max=float(gs.max()),
        gross_crash_min=float(gs.loc[CRASH[0]:CRASH[1]].min())
        if len(gs.loc[CRASH[0]:CRASH[1]]) else np.nan,
        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
        is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
        is_H1=ih1, is_H2=ih2, is_legs=is_legs,
        is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
        **{k: float(v) for k, v in mar.items()},
        bind=bl, n_fail=nbad,
        keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
        keep4a=k4a, keep4a_oos=k4ao)


def alab(A):
    return A if isinstance(A, str) else f"A={A:g}"


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2075 (lane C, {DATE}) — does the 4:1 ASYMMETRY RATIO matter, or is ANY tight "
        f"DOWN-trigger the same?")
    log(f"# tuned dials (2): RATIO A {[alab(a) for a in A_RUNGS]} x the family's own BASE rung "
        f"(FIXH h {BASE_H} | FRACG f {BASE_F}).")
    log(f"# reported, NOT tuned: TARGET t {TARGETS} (pre-stated t*={TGT_STAR}, inherited), TRADE "
        f"{TRADES}, PANEL, COST {COSTS} bps, CAL comparand R {REFRESH}.  sigma FIXED (L={SIG_L}, "
        f"d={SIG_D}).")
    log(f"# PRE-STATED cell under test: A*={A_STAR:g} at h*={H_STAR} / f*={F_STAR}, t*={TGT_STAR}."
        f"  warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, BASE, BOOKS = [], {}, {}
    g_cost = 0.0
    g_zero = 0.0
    g_zero_n = 0
    gross_max = 0.0

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        BOOKS[pname] = (bk, px, cols, st)
        nyears = len(px.loc[st:]) / 252.0
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()} ({nyears:.1f}y)")

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st, nyears=nyears,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1],
                          ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1],
                                 turn=float(lt.sum() / nyears))
        BASE[pname] = B
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {L['full']['CAGR']:.2%} / {L['full']['Sharpe']:.4f}"
            f" / {L['full']['MaxDD']:.2%}  (OOS {L['oos']['CAGR']:.2%} / {L['oos']['Sharpe']:.4f}"
            f" / {L['oos']['MaxDD']:.2%}), {L['turn']:.2f} turns/yr")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        # ---- G4 cost identity + G5 zero-base gate on the large panels -------------------
        if pname in BIG:
            Gp = (TGT_STAR / bk.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = (eq_weight(px, cols).mul(Gp, axis=0)).fillna(0.0)
            a, at, _, _ = bk.run(TGT_STAR, "W", "CAL", "W")
            for c in (10, 25):
                eb = engine_backtest(px, Wfull, cost_bps=float(c), freq="W")["returns"]
                g_cost = max(g_cost, float(np.abs(net(a, at, c).values - eb.values).max()))
            for T in TRADES:
                z, _, _, _ = bk.run(TGT_STAR, T, "FIXH", 0.0, 1.0)
                d, _, _, _ = bk.run(TGT_STAR, T, "CAL", "D")
                g_zero = max(g_zero, float(np.abs(z.values - d.values).max()))
                g_zero_n += 1

        # ---- the grid -------------------------------------------------------------------
        for tgt in TARGETS:
            for T in TRADES:
                for rung in REFRESH:                                  # reported comparand
                    r0, t0, gs, nref = bk.run(tgt, T, "CAL", rung)
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    gross_max = max(gross_max, float(gs.max()))
                    for c in COSTS:
                        rows.append(dict(panel=pname, target=tgt, T_trade=T, family="CAL",
                                         base=np.nan, A="CAL", A_num=np.nan,
                                         cell=f"R={rung}", rung=rung,
                                         **score_cell(r0, t0, gs, nref, c, B["spy"],
                                                      B[f"live{c}"], nyears)))
                for fam, grid in BASES.items():
                    for base in grid:
                        for A in A_RUNGS:
                            r0, t0, gs, nref = bk.run(tgt, T, fam, base, A)
                            r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                            gross_max = max(gross_max, float(gs.max()))
                            lab = ("h" if fam == "FIXH" else "f") + f"={base:g} {alab(A)}"
                            for c in COSTS:
                                rows.append(dict(
                                    panel=pname, target=tgt, T_trade=T, family=fam, base=base,
                                    A=(A if isinstance(A, str) else f"{A:g}"),
                                    A_num=(np.nan if isinstance(A, str) else float(A)),
                                    cell=lab, rung=base,
                                    **score_cell(r0, t0, gs, nref, c, B["spy"],
                                                 B[f"live{c}"], nyears)))
        log(f"   ...{len(rows)} scored rows so far")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    log(f"\n# grid: {len(G)} scored rows "
        f"({len(G)//len(COSTS)} cells x {len(COSTS)} cost rungs) -> {OUT.name}.grid.csv.gz")

    # ----------------------------------------------------------------------------- gates
    log("\n## GATES")
    ok = []
    minyrs = min(BASE[p]["nyears"] for p in BASE)
    ok.append(gate("G0 sample length (yrs, min over panels)", f"{minyrs:.1f}", ">= 10", minyrs >= 10))
    ok.append(gate("G4 cost identity |net - engine(cost)|", f"{g_cost:.3e}", "< 1e-12",
                   g_cost < 1e-12))
    ok.append(gate(f"G5 zero base (FIXH b=0, A=1) == CAL R=D on {g_zero_n} cells",
                   f"{g_zero:.3e}", "== 0", g_zero == 0.0))
    ok.append(gate("G6 gross never levered (max held gross)", f"{gross_max:.6f}", "<= 1.0",
                   gross_max <= 1.0 + 1e-12))

    def cell_at(panel, tgt, T, fam, base, A, c=COST0):
        m = G[(G.panel == panel) & (G.target == tgt) & (G.T_trade == T) & (G.family == fam)
              & (G.base == base) & (G.A == A) & (G.cost == c)]
        return m.iloc[0] if len(m) else None

    r1799 = cell_at("U56", TGT_STAR, "M", "FIXH", H_STAR, "1")
    d1 = max(abs(r1799.CAGR - PUB_1799["CAGR"]), abs(r1799.Sharpe - PUB_1799["Sharpe"]),
             abs(r1799.MaxDD - PUB_1799["MaxDD"]), abs(r1799.oos_Sharpe - PUB_1799["oSharpe"]))
    ok.append(gate("G1 idea 1799 U56 t=.16 h=.12 T=M 10bps (A=1)", f"{d1:.3e}", "< 1e-4",
                   d1 < 1e-4))
    r2026 = cell_at("U56", TGT_STAR, "M", "FRACG", F_STAR, "1")
    d2 = max(abs(r2026.CAGR - PUB_2026["CAGR"]), abs(r2026.Sharpe - PUB_2026["Sharpe"]),
             abs(r2026.MaxDD - PUB_2026["MaxDD"]), abs(r2026.oos_Sharpe - PUB_2026["oSharpe"]))
    ok.append(gate("G2 idea 2026 U56 t=.16 f=.10 T=M 10bps (A=1, the standing KEEP-4b cell)",
                   f"{d2:.3e}", "< 1e-3", d2 < 1e-3))

    # refresh-count monotonicity in A, and the two deleted-side gates
    R0 = G[G.cost == COST0]
    piv = R0[R0.family.isin(BASES)].pivot_table(
        index=["panel", "target", "T_trade", "family", "base"], columns="A", values="refresh_py")
    mono = int(((piv[["1", "2", "4", "8", "16"]].diff(axis=1).iloc[:, 1:] >= -1e-9)
                .all(axis=1)).sum())
    ok.append(gate("G3 refresh rate non-decreasing in A", f"{mono} of {len(piv)}",
                   f"== {len(piv)}", mono == len(piv)))
    ndn = int((piv["DOWNONLY"] <= piv["1"] + 1e-9).sum())
    ok.append(gate("G7 DOWNONLY refreshes <= its symmetric twin A=1", f"{ndn} of {len(piv)}",
                   f"== {len(piv)}", ndn == len(piv)))
    nup = int((piv["UPONLY"] <= piv["1"] + 1e-9).sum())
    ok.append(gate("G8 UPONLY refreshes <= its symmetric twin A=1", f"{nup} of {len(piv)}",
                   f"== {len(piv)}", nup == len(piv)))
    n4 = int((piv["4"] >= piv["1"] - 1e-9).sum())
    ok.append(gate("G9 the 4:1 trigger refreshes >= its symmetric twin (idea 2026 G8 restated)",
                   f"{n4} of {len(piv)}", f"== {len(piv)}", n4 == len(piv)))
    dn = R0[(R0.A == "DOWNONLY") & (R0.family.isin(BASES))]
    nabs = int(((dn.gross_mean.abs() < 1e-12) & (dn.turn_py.abs() < 1e-12)).sum())
    ok.append(gate("G10 pure DOWNONLY is ABSORBING (no re-entry channel): gross==0 and turn==0",
                   f"{nabs} of {len(dn)}", f"== {len(dn)}", nabs == len(dn)))
    ntd = int((piv["DOWNONLY_TD"] <= piv["A1_TD"] + 1e-9).sum())
    ok.append(gate("G11 DOWNONLY_TD refreshes <= its matched twin A1_TD",
                   f"{ntd} of {len(piv)}", f"== {len(piv)}", ntd == len(piv)))
    ntd2 = int((piv["A1_TD"] >= piv["1"] - 1e-9).sum())
    ok.append(gate("G12 the trade-day re-read only ADDS refreshes (A1_TD >= A=1)",
                   f"{ntd2} of {len(piv)}", f"== {len(piv)}", ntd2 == len(piv)))
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log(f"   GATES {sum(ok)}/{len(ok)}")

    # ------------------------------------------------------- V1/V2: the A profile, paired vs A=1
    log(f"\n## V1 / V2 — the A PROFILE, paired against each base's OWN symmetric twin (A=1)")
    log(f"   t*={TGT_STAR}, {COST0} bps, large panels {BIG} x trade {TRADES}, pooled over "
        f"{len(BASE_H)} h and {len(BASE_F)} f rungs")
    prof_rows = []
    sel = R0[(R0.target == TGT_STAR) & (R0.panel.isin(BIG)) & (R0.family.isin(BASES))]
    key = ["panel", "T_trade", "family", "base"]
    sym = sel[sel.A == "1"].set_index(key)
    for A in ["2", "4", "8", "16", "DOWNONLY", "UPONLY", "DOWNONLY_TD", "A1_TD"]:
        s = sel[sel.A == A].set_index(key)
        j = s.join(sym, rsuffix="_sym", how="inner")
        prof_rows.append(dict(
            A=A, n_pairs=len(j),
            d_oosMaxDD_pp=100 * (j.oos_MaxDD - j.oos_MaxDD_sym).mean(),
            d_oosCAGR_pp=100 * (j.oos_CAGR - j.oos_CAGR_sym).mean(),
            d_oosSharpe=(j.oos_Sharpe - j.oos_Sharpe_sym).mean(),
            d_fullMaxDD_pp=100 * (j.MaxDD - j.MaxDD_sym).mean(),
            d_turn_py=(j.turn_py - j.turn_py_sym).mean(),
            d_refresh_py=(j.refresh_py - j.refresh_py_sym).mean(),
            d_crashgross=(j.gross_crash_min - j.gross_crash_min_sym).mean(),
            keep4b=int(j.keep4b.sum()), keep4b_sym=int(j.keep4b_sym.sum()),
            L5_neg=int((j.L5_CAGR <= 0).sum()), L5_neg_sym=int((j.L5_CAGR_sym <= 0).sum())))
    PR = pd.DataFrame([dict(A="1", n_pairs=len(sym), d_oosMaxDD_pp=0.0, d_oosCAGR_pp=0.0,
                            d_oosSharpe=0.0, d_fullMaxDD_pp=0.0, d_turn_py=0.0, d_refresh_py=0.0,
                            d_crashgross=0.0, keep4b=int(sym.keep4b.sum()),
                            keep4b_sym=int(sym.keep4b.sum()),
                            L5_neg=int((sym.L5_CAGR <= 0).sum()),
                            L5_neg_sym=int((sym.L5_CAGR <= 0).sum()))] + prof_rows)
    PR["dd_per_cagr"] = PR.d_oosMaxDD_pp / PR.d_oosCAGR_pp.where(PR.d_oosCAGR_pp < 0).abs()
    PR.to_csv(f"{OUT}.profile.csv", index=False)
    log(PR.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    num = PR[PR.A.isin(["1", "2", "4", "8", "16"])].set_index("A")
    dd = num.d_oosMaxDD_pp
    nondec = all(dd[b] >= dd[a] - 1e-9 for a, b in zip(["1", "2", "4", "8"], ["2", "4", "8", "16"]))
    tot = dd["16"] - dd["1"]
    last = dd["16"] - dd["8"]
    share = (last / tot) if abs(tot) > 1e-12 else np.nan
    v1 = bool(nondec and np.isfinite(share) and share < 0.25)
    log(f"   V1 SATURATION: OOS MaxDD credit non-decreasing in A = {nondec}; total 1->16 "
        f"{tot:+.3f} pp, last step 8->16 {last:+.3f} pp = {share:.1%} of it.  "
        f"V1 {'TRIGGERED' if v1 else 'NOT TRIGGERED'}")
    cg = num.d_oosCAGR_pp
    v2 = all(cg[b] <= cg[a] + 1e-9 for a, b in zip(["1", "2", "4", "8"], ["2", "4", "8", "16"]))
    firstneg = [A for A in ["1", "2", "4", "8", "16"]
                if len(sel[(sel.A == A) & (sel.base.isin([H_STAR, F_STAR]))
                           & (sel.L5_CAGR <= 0)])]
    xr = PR[PR.A.isin(["2", "4", "8", "16"])].set_index("A").dd_per_cagr
    log(f"   EXCHANGE RATE (pp of OOS MaxDD bought per pp of OOS CAGR given up): "
        f"{' '.join(f'{A}:{xr[A]:.2f}' for A in ['2','4','8','16'])} -> best rung "
        f"A={xr.idxmax()}")
    log(f"   V2 CAGR COST: pooled mean OOS CAGR delta monotone non-increasing in A = {v2}; "
        f"profile {' '.join(f'{A}:{cg[A]:+.3f}pp' for A in ['1','2','4','8','16'])}; "
        f"first A with L5_CAGR <= 0 at a PRE-STATED base: "
        f"{firstneg[0] if firstneg else 'none over the ladder'}.  "
        f"V2 {'TRIGGERED' if v2 else 'NOT TRIGGERED'}")

    # ------------------------------------------------------------------ V3: DOWNONLY dominance
    log(f"\n## V3 — does DOWN-ONLY DOMINATE its symmetric twin?  (paired, same base, same arm)")
    dom_rows = []
    for A in ["DOWNONLY", "DOWNONLY_TD", "UPONLY", "4"]:
        s = sel[sel.A == A].set_index(key)
        tw = sel[sel.A == ("A1_TD" if A == "DOWNONLY_TD" else "1")].set_index(key)
        j = s.join(tw, rsuffix="_sym", how="inner")
        wS = j.oos_Sharpe >= j.oos_Sharpe_sym - 1e-12
        wD = j.oos_MaxDD >= j.oos_MaxDD_sym - 1e-12
        wC = j.oos_CAGR >= j.oos_CAGR_sym - 1e-12
        wT = j.turn_py <= j.turn_py_sym + 1e-12
        allw = wS & wD & wC & wT
        dom_rows.append(dict(A=A, twin=("A1_TD" if A == "DOWNONLY_TD" else "1"), n=len(j), win_oosSharpe=int(wS.sum()), win_oosMaxDD=int(wD.sum()),
                             win_oosCAGR=int(wC.sum()), win_turnover=int(wT.sum()),
                             weak_dominates_all4=int(allw.sum()),
                             share_all4=float(allw.mean())))
    DM = pd.DataFrame(dom_rows)
    DM.to_csv(f"{OUT}.dominance.csv", index=False)
    log(DM.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    absorb = sel[sel.A == "DOWNONLY"]
    n_abs = int(((absorb.gross_mean.abs() < 1e-12) & (absorb.turn_py.abs() < 1e-12)).sum())
    log(f"   V3-pure: the PRE-STATED DOWNONLY rung is ABSORBING (mean gross 0, turnover 0) on "
        f"{n_abs} of {len(absorb)} cells — deleting the up-side threshold deletes the book's ONLY "
        f"re-entry channel.  It fails 4b on 4 legs at once everywhere.  V3-pure NOT TRIGGERED "
        f"BY CONSTRUCTION, not by returns.")

    dnrow = DM[DM.A == "DOWNONLY_TD"].iloc[0]
    tdj = sel[sel.A == "DOWNONLY_TD"].set_index(key).join(
        sel[sel.A == "A1_TD"].set_index(key), rsuffix="_sym", how="inner")
    dnp = dict(d_oosSharpe=(tdj.oos_Sharpe - tdj.oos_Sharpe_sym).mean(),
               d_oosMaxDD_pp=100 * (tdj.oos_MaxDD - tdj.oos_MaxDD_sym).mean(),
               d_oosCAGR_pp=100 * (tdj.oos_CAGR - tdj.oos_CAGR_sym).mean(),
               d_turn_py=(tdj.turn_py - tdj.turn_py_sym).mean(),
               keep4b=int(tdj.keep4b.sum()), keep4b_sym=int(tdj.keep4b_sym.sum()))
    strict = (dnp["d_oosSharpe"] > 0) or (dnp["d_oosMaxDD_pp"] > 0) or (dnp["d_oosCAGR_pp"] > 0) \
        or (dnp["d_turn_py"] < 0)
    v3 = bool(dnrow.share_all4 >= 0.50 and strict)
    log(f"   V3-TD (POST-HOC): DOWNONLY_TD weakly dominates its MATCHED twin A1_TD on all four "
        f"axes at {dnrow.share_all4:.1%} of {int(dnrow.n)} (arm x base) pairs; pooled means "
        f"dSharpe {dnp['d_oosSharpe']:+.4f}, dMaxDD {dnp['d_oosMaxDD_pp']:+.3f} pp, "
        f"dCAGR {dnp['d_oosCAGR_pp']:+.3f} pp, dturn {dnp['d_turn_py']:+.3f}/yr; 4b "
        f"{dnp['keep4b']} vs {dnp['keep4b_sym']} of {len(tdj)}.  "
        f"V3 {'TRIGGERED' if v3 else 'NOT TRIGGERED'}")

    # ------------------------------------------------------------- V4: does the ratio matter
    log(f"\n## V4 — does the RATIO MATTER at all?  4b FULL+OOS pass counts by A rung "
        f"(t*, {COST0} bps, large panels, all bases)")
    cnt = sel.groupby("A").agg(cells=("keep4b", "size"), keep4b=("keep4b", "sum"),
                               keep4b_full=("keep4b_full", "sum"), keep4a=("keep4a", "sum"),
                               mean_oosSharpe=("oos_Sharpe", "mean"),
                               mean_oosMaxDD=("oos_MaxDD", "mean"),
                               mean_oosCAGR=("oos_CAGR", "mean"),
                               mean_turn=("turn_py", "mean"))
    order = ["1", "2", "4", "8", "16", "DOWNONLY", "UPONLY", "DOWNONLY_TD", "A1_TD"]
    cnt = cnt.reindex([a for a in order if a in cnt.index])
    cnt.to_csv(f"{OUT}.ratio_counts.csv")
    log(cnt.to_string(float_format=lambda x: f"{x:.4f}"))
    lad = cnt.loc[[a for a in ["1", "2", "4", "8", "16"] if a in cnt.index], "keep4b"]
    spread = (lad.max() - lad.min()) / lad.max() if lad.max() else np.nan
    v4 = bool(np.isfinite(spread) and spread > 0.10)
    log(f"   V4: 4b pass count over the A ladder runs {lad.min()}..{lad.max()} of "
        f"{int(cnt.cells.iloc[0])} cells, spread {spread:.1%} of the best.  "
        f"V4 {'TRIGGERED' if v4 else 'NOT TRIGGERED'} "
        f"({'the ratio MOVES the verdict' if v4 else 'ANY tight down trigger is the same'})")

    # ---------------------------------------------- the PRE-STATED cells, side by side
    log(f"\n## THE PRE-STATED CELLS (t*={TGT_STAR}, {COST0} bps) — A* = {A_STAR:g} vs its twin "
        f"and vs DOWNONLY")
    ps_rows = []
    for pname in BASE:
        for T in TRADES:
            for fam, b in (("FIXH", H_STAR), ("FRACG", F_STAR)):
                for A in ["1", "4", "16", "DOWNONLY", "DOWNONLY_TD", "A1_TD",
                          "UPONLY"]:
                    r = cell_at(pname, TGT_STAR, T, fam, b, A)
                    if r is None:
                        continue
                    ps_rows.append(dict(panel=pname, T_trade=T, family=fam, base=b, A=A,
                                        CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                        H1=r.H1, H2=r.H2, oos_CAGR=r.oos_CAGR,
                                        oos_Sharpe=r.oos_Sharpe, oos_MaxDD=r.oos_MaxDD,
                                        turn_py=r.turn_py, refresh_py=r.refresh_py,
                                        gross_crash_min=r.gross_crash_min,
                                        bind=r.bind, keep4b_full=r.keep4b_full,
                                        keep4b_oos=r.keep4b_oos, keep4b=r.keep4b, keep4a=r.keep4a))
    PSD = pd.DataFrame(ps_rows)
    PSD.to_csv(f"{OUT}.prestated.csv", index=False)
    log(PSD[PSD.panel.isin(BIG)].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"   SMALL panel: 4b {int(PSD[~PSD.panel.isin(BIG)].keep4b.sum())} of "
        f"{len(PSD[~PSD.panel.isin(BIG)])} pre-stated cells, 4a "
        f"{int(PSD[~PSD.panel.isin(BIG)].keep4a.sum())}")

    # ------------------------------------------------------------------- rule 8: the choosers
    log(f"\n## RULE 8 — (A, base) chosen on 2009-{IS_END[:4]} ONLY; {OOS_START[:4]}-2026 read once")
    CH = {"C_ISSHARPE": lambda d: d.is_Sharpe,
          "C_ISCALMAR": lambda d: d.is_Calmar,
          "C_ISDD": lambda d: d.is_MaxDD,
          "C_ISLEGS": lambda d: d.is_legs * 1e6 + d.is_Sharpe}
    ch_rows = []
    GT = G[(G.target == TGT_STAR) & (G.family.isin(BASES))]
    for (pn, T, c, fam), arm in GT.groupby(["panel", "T_trade", "cost", "family"]):
        arm = arm.sort_values(["base", "A"], kind="mergesort")
        for cname, f in CH.items():
            pick = arm.loc[f(arm).idxmax()]
            ch_rows.append(dict(panel=pn, T_trade=T, cost=c, family=fam, chooser=cname,
                                A=pick.A, base=pick.base, cell=pick.cell,
                                turn_py=pick.turn_py, refresh_py=pick.refresh_py,
                                CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                                H1=pick.H1, H2=pick.H2, oos_CAGR=pick.oos_CAGR,
                                oos_Sharpe=pick.oos_Sharpe, oos_MaxDD=pick.oos_MaxDD,
                                bind=pick.bind, keep4b_full=pick.keep4b_full,
                                keep4b_oos=pick.keep4b_oos, keep4b=pick.keep4b, keep4a=pick.keep4a))
    C = pd.DataFrame(ch_rows)
    C.to_csv(f"{OUT}.choosers.csv", index=False)
    C0 = C[C.cost == COST0]
    log(f"   picks at {COST0} bps ({len(C0)} = {len(BASE)} panels x {len(TRADES)} cadences x "
        f"{len(BASES)} bases x {len(CH)} choosers):")
    log(C0[C0.panel.isin(BIG)][["panel", "T_trade", "family", "chooser", "cell", "oos_CAGR",
                                "oos_Sharpe", "oos_MaxDD", "turn_py", "bind", "keep4b",
                                "keep4a"]].to_string(index=False,
                                                     float_format=lambda x: f"{x:.4f}"))
    apick = C0.A.value_counts()
    log(f"   which A rung the LEGAL IS-only choosers land on: "
        f"{', '.join(f'{k}:{v}' for k, v in apick.items())}")
    deg = C0[C0.A == "DOWNONLY"]
    if len(deg):
        log(f"   CHOOSER DEGENERACY (incidental KILL): the absorbing DOWNONLY book is picked on "
            f"{len(deg)} of {len(C0)} (arm x base x chooser) cells, and "
            f"{int((deg.chooser == 'C_ISDD').sum())} of them are C_ISDD.  C_ISDD maximises IS "
            f"MaxDD, and a book that holds NOTHING has MaxDD exactly 0, so C_ISDD picks cash "
            f"whenever the corpus contains a cash book: it is picked at "
            f"{(C0[C0.chooser == 'C_ISDD'].A == 'DOWNONLY').mean():.0%} of C_ISDD cells here.  "
            f"C_ISDD is NOT a legal chooser on any corpus that admits a zero-gross cell.")
    log(f"   IS-chosen cells clearing 4b FULL+OOS: {int(C0.keep4b.sum())} of {len(C0)} "
        f"(4a {int(C0.keep4a.sum())})")
    ps4b = int(PSD[(PSD.A == "4")].keep4b.sum())
    sym4b = int(PSD[(PSD.A == "1")].keep4b.sum())
    log(f"   PRE-STATED A*=4 clears 4b on {ps4b} of {len(PSD[PSD.A == '4'])} pre-stated cells; "
        f"its symmetric twin A=1 on {sym4b}; DOWNONLY on "
        f"{int(PSD[PSD.A == 'DOWNONLY'].keep4b.sum())}")

    # -------------------------------------------------------------------- V5: capital
    log(f"\n## V5 — KEEP-4b candidates (4b FULL *and* OOS) at {COST0} bps, t*, large panels")
    P4 = sel[sel.keep4b]
    log(f"   {len(P4)} of {len(sel)} cells clear 4b FULL+OOS; 4a {int(sel.keep4a.sum())}")
    best = None
    if len(P4):
        top = P4.sort_values("oos_Sharpe", ascending=False).head(12)
        log(top[["panel", "T_trade", "family", "cell", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "turn_py"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
        # the KEEP-candidate this run puts forward: PRE-STATED only (zero IS spend)
        cand = P4[(P4.A == f"{A_STAR:g}") & (P4.base.isin([H_STAR, F_STAR]))]
        if len(cand):
            best = cand.sort_values("oos_Sharpe", ascending=False).iloc[0]
            log(f"   PRE-STATED KEEP-4b candidate: {best.panel} T={best.T_trade} {best.family} "
                f"{best.cell} t={TGT_STAR}  full {best.CAGR:.2%} / {best.Sharpe:.4f} / "
                f"{best.MaxDD:.2%}, halves {best.H1:.4f} / {best.H2:.4f}; OOS "
                f"{best.oos_CAGR:.2%} / {best.oos_Sharpe:.4f} / {best.oos_MaxDD:.2%}; "
                f"{best.turn_py:.2f} turns/yr, {best.refresh_py:.1f} refreshes/yr")
            for c in COSTS:
                rr = G[(G.panel == best.panel) & (G.target == TGT_STAR)
                       & (G.T_trade == best.T_trade) & (G.family == best.family)
                       & (G.base == best.base) & (G.A == best.A) & (G.cost == c)].iloc[0]
                log(f"      {c:2d} bps: full 4b={bool(rr.keep4b_full)} OOS 4b={bool(rr.keep4b_oos)}"
                    f"  {rr.CAGR:.2%} / {rr.Sharpe:.4f} / {rr.MaxDD:.2%}  "
                    f"(OOS {rr.oos_CAGR:.2%} / {rr.oos_Sharpe:.4f} / {rr.oos_MaxDD:.2%})"
                    f"  bind={rr.bind}")

    # ------------------------------------------------------------- leaderboard + verdict
    S56 = BASE["U56"]["spy"]
    L56 = BASE["U56"][f"live{COST0}"]
    log(f"\n## VERDICT")
    log(f"   V1 {'TRIGGERED' if v1 else 'NOT TRIGGERED'} | V2 {'TRIGGERED' if v2 else 'NOT'} | "
        f"V3 {'TRIGGERED' if v3 else 'NOT TRIGGERED'} | V4 "
        f"{'TRIGGERED' if v4 else 'NOT TRIGGERED'} | gates {sum(ok)}/{len(ok)}")
    log(f"   U56 SPY {S56['full']['CAGR']:.2%} / {S56['full']['Sharpe']:.4f} / "
        f"{S56['full']['MaxDD']:.2%} | live RULES v2 {L56['full']['CAGR']:.2%} / "
        f"{L56['full']['Sharpe']:.4f} / {L56['full']['MaxDD']:.2%}")

    lb = []
    for tag, r in (("A1-symmetric", cell_at("U56", TGT_STAR, "M", "FRACG", F_STAR, "1")),
                   ("A4-prestated", cell_at("U56", TGT_STAR, "M", "FRACG", F_STAR, "4")),
                   ("A16", cell_at("U56", TGT_STAR, "M", "FRACG", F_STAR, "16")),
                   ("A1TD-symmetric", cell_at("U56", TGT_STAR, "M", "FRACG", F_STAR, "A1_TD")),
                   ("DOWNONLY-TD", cell_at("U56", TGT_STAR, "M", "FRACG", F_STAR,
                                           "DOWNONLY_TD"))):
        if r is None:
            continue
        v = "KEEP-4b" if r.keep4b else ("KEEP-4a" if r.keep4a else "KILL")
        lb.append(f"| {DATE} | 2075-asym-ratio {tag} (U56 FRACG f=.10 t=.16 M 10bps) | "
                  f"{r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | {r.H1:.2f} / {r.H2:.2f} | "
                  f"{L56['full']['Sharpe']:.2f} ({L56['h1']:.2f}/{L56['h2']:.2f}) | {v} | "
                  f"{DATE}_{SLUG}_C.py |")
    log("\nLEADERBOARD rows:\n" + "\n".join(lb))

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    print(f"\nwrote {OUT.name}.{{grid.csv.gz,profile.csv,dominance.csv,ratio_counts.csv,"
          f"prestated.csv,choosers.csv,gates.csv,log.txt}}")


if __name__ == "__main__":
    main()
