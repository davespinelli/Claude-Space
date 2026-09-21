#!/usr/bin/env python3
"""Idea 2030 (lane C, 2026-09-21) — DOES THE ASYMMETRY OF THE DRIFT TRIGGER CARRY THE WHOLE EFFECT?

THE QUESTION.  Idea 1799 found a DRIFT-THRESHOLD refresh beating the turnover-MATCHED point on its
own arm's CALENDAR ladder at 263 of 263 cells at 10 bps, mean **+0.0596** OOS Sharpe and **+4.07
pp** OOS MaxDD for +0.31 pp CAGR, and its mechanism table put the whole credit in the 2020 crash
(gross 1.000 -> 0.254).  But the trigger `|g_t - gross_held| > h` is SYMMETRIC: it also delays
RE-grossing on the way out, and the 4b CAGR floor `L5_CAGR` is the binding leg at 38 of 420 cells.
This run separates the two sides at the SAME `h` and says which one owns the +0.0596 and which one
owns the CAGR cost.

THE CONSTRUCTION, AND WHY IT IS NOT 2075's.  Today's earlier lane C run (idea 2075) found the PURE
down-only rung DEGENERATE: on the 1799 construction the drift trigger is the book's ONLY channel
for re-reading `g_t`, the shifted scalar starts at `g_0 = 0` (the t+1 convention), and a down-side
trigger can never lift a zero book off zero — mean gross 0 and turnover 0 at 360 of 360 cells.
2075 repaired this POST-HOC with a trade-day re-read (`_TD`) and re-read its verdict on a single
pre-stated `t = 0.16` against a matched `_TD` twin.  THIS run PRE-STATES the `_TD` construction
(declared here, before any compute), ladders BOTH dials, and scores the halves against the ruler
that produced the +0.0596 in the first place — the turnover-matched CALENDAR ladder — which 2075
never did.  The pure rungs are kept as REPLICATION GATES (G8/G9) of 2075's structural facts, not
as candidates.

    SYM      h_dn = h_up = h, trade day does NOT re-read      <- idea 1799's incumbent, verbatim
    SYM_TD   h_dn = h_up = h, trade day re-reads `g_t`        <- the matched two-sided control
    DOWN_TD  h_dn = h, up side DELETED, trade day re-reads    <- de-gross intraperiod only
    UP_TD    down side DELETED, h_up = h, trade day re-reads  <- re-gross intraperiod only
    CAL      calendar refresh on R in {D,W,M,Q}               <- the comparand and the zero point

THE ZERO POINT IS EXACT, WHICH IS WHAT MAKES THIS AN ATTRIBUTION AND NOT A COMPARISON.  With the
trade-day re-read on, a threshold that never fires IS the calendar book refreshed at the trade
cadence: `SYM_TD/DOWN_TD/UP_TD (h -> inf) == CAL(R = T)`, gated to 0 (G6).  So relative to that one
book, DOWN_TD adds exactly the intra-period DE-grossing, UP_TD adds exactly the intra-period
RE-grossing, SYM_TD adds both, and the interaction residual is published rather than assumed away.

PRE-STATED VERDICT RULES (fixed before the run; not adjusted afterwards):
  V1  DOWN OWNS THE SHARPE.  At 10 bps, over drift cells inside the calendar ladder's turnover
      range, mean(DOWN_TD - turnover-matched calendar) OOS Sharpe >= 0.5 x mean(SYM - matched)
      AND mean(UP_TD - matched) < 0.5 x mean(SYM - matched).
  V2  UP OWNS THE CAGR COST.  Pooled at 10 bps, the 4b CAGR margin `L5_CAGR` orders strictly
      UP_TD > SYM_TD > DOWN_TD, i.e. deleting the up side costs CAGR and deleting the down side
      buys it back.
  V3  THE HALF-RULE REACHES.  DOWN_TD clears 4b FULL *and* OOS on at least as many cells at 10 bps
      as SYM_TD, AND at least one such cell is reached by a legal IS-only chooser.  Not triggered
      -> the half-rule is KILLED as a replacement for the two-sided trigger.
  V4  CAPITAL.  Both KEEP paths are scored at every cell.  Any cell clearing 4b FULL *and* OOS
      that a legal IS-only chooser actually reaches is a KEEP-4b candidate.

DIALS.  EXACTLY TWO are tuned and only ever within one family: TARGET `t` and THRESHOLD `h` (the
CALENDAR family spends `t` and `R`).  No chooser ever selects across families, panels, trade
cadence or cost.  REPORTED, NOT TUNED: TRIGGER SIDE (the axis under test), TRADE cadence
`T in {W, M}` (separate arms), PANEL {U56, B136, SMALL}, COST {0, 10, 25, 50} bps.  The sigma
convention is FIXED at the standing memo's (L=20, d=0).  Every grid point is published.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and drawdown
LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.  The
SIDE contrast is same-tape / same-names / same-grid with only the trigger's sign condition moved,
so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-21_drift-trigger-side-attribution_C.py
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

DATE, SLUG = "2026-09-21", "drift-trigger-side-attribution"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]
H_GRID = [0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
H_GATE = [0.03, 0.08, 0.16]          # pure-rung replication gates (2075's structural KILLs)
H_BIG = 10.0                         # "never fires" limit, for the G6 identity
TRADES = ["W", "M"]
SIDES = ["SYM", "SYM_TD", "DOWN_TD", "UP_TD"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0
CRASH0, CRASH1 = "2020-02-19", "2020-04-30"
INF = float("inf")

# committed numbers this run must reproduce
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
GRID_1799 = Path(__file__).resolve().parent / "2026-09-20_drift-threshold-refresh_C.grid.csv"
PUB_1799_V2 = 0.0596      # mean OOS-Sharpe gain of DRIFT over turnover-matched CALENDAR, 10 bps

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
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio through close
    t-d.  (L, d) = (20, 0) is the standing memo's convention."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------ the two refresh runners
def bt_cal(px_ret, W0, g0, mT, mR):
    """CALENDAR refresh (idea 1767 / 1799's two-schedule construction, verbatim)."""
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


def bt_drift(px_ret, W0, g0, mT, h_dn, h_up, td_read):
    """SIDED drift-threshold refresh.  The scalar is re-read on day i iff

        DOWN:  g0[i] <  gross_held - h_dn      (the book is carrying MORE than the target)
        UP:    g0[i] >  gross_held + h_up      (the book is carrying LESS than the target)

    `h_dn = inf` deletes the down side, `h_up = inf` deletes the up side.  `td_read=True` also
    re-reads the scalar on a scheduled TRADE day, which is what makes a one-sided trigger a
    well-defined book (idea 2075's structural finding; here PRE-STATED).  With td_read=False and
    h_dn = h_up = h this is idea 1799's `bt_drift` verbatim (gate G5)."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        gh = cur.sum()
        trig = (g0[i] < gh - h_dn) or (g0[i] > gh + h_up)
        if trig or i == 0 or (td_read and mT[i]):
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


def sided(side, h):
    """(h_dn, h_up, td_read) for a named trigger side at threshold h."""
    return {"SYM":       (h, h, False),
            "SYM_TD":    (h, h, True),
            "DOWN_TD":   (h, INF, True),
            "UP_TD":     (INF, h, True),
            "PURE_DOWN": (h, INF, False),
            "PURE_UP":   (INF, h, False)}[side]


class Book:
    """Pre-shifted arrays for one panel, so every (t, T, side) run is a single loop."""

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

    def g_of(self, tgt):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])

    def _wrap(self, out):
        r, t, gs, nref = out
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)

    def run_cal(self, g0, T, R):
        return self._wrap(bt_cal(self.R, self.W, g0, self.masks[T], self.masks[R]))

    def run_side(self, g0, T, side, h):
        h_dn, h_up, td = sided(side, h)
        return self._wrap(bt_drift(self.R, self.W, g0, self.masks[T], h_dn, h_up, td))


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


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2030 (lane C, {DATE}) — does the ASYMMETRY of the DRIFT TRIGGER carry the whole "
        f"effect?")
    log(f"# tuned dials (2): TARGET t {TARGETS} x THRESHOLD h {H_GRID}   [CALENDAR family spends "
        f"t x R {REFRESH}].  reported, not tuned: SIDE {SIDES} (the axis under test), TRADE T "
        f"{TRADES}, PANEL, COST {COSTS} bps.  sigma FIXED at (L={SIG_L}, d={SIG_D}); warm-up "
        f"{WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, crash_rows = [], []
    BASE = {}
    g1r = g1t = g2 = g3 = g4 = g6 = 0.0
    g7 = 0.0
    g4n = g6n = 0
    pure_dn_gross, pure_up_crash, sym_crash = [], [], []

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")

        # ---- baselines: live RULES v2 (weekly) and SPY ---------------------------------
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1],
                          ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1],
                                 turn=float(lt.sum() / (len(lr) / 252.0)))
        BASE[pname] = B
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {L['full']['CAGR']:.2%} / {L['full']['Sharpe']:.4f}"
            f" / {L['full']['MaxDD']:.2%}  (OOS {L['oos']['CAGR']:.2%} / {L['oos']['Sharpe']:.4f}"
            f" / {L['oos']['MaxDD']:.2%}), {L['turn']:.2f} turns/yr")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        # ---- G1 / G2: the calendar diagonal is engine.backtest ---------------------------
        if pname in ("U56", "B136"):
            Gp = (TGT_MEMO / bk.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = (eq_weight(px, cols).mul(Gp, axis=0)).fillna(0.0)
            a, at, _, _ = bk.run_cal(bk.g_of(TGT_MEMO), "W", "W")
            b = engine_backtest(px, Wfull, cost_bps=0.0, freq="W")
            g1r = max(g1r, float(np.abs(a.values - b["returns"].values).max()))
            g1t = max(g1t, float(np.abs(at.values - b["turnover"].values).max()))
            for c in (10, 25):
                eb = engine_backtest(px, Wfull, cost_bps=float(c), freq="W")["returns"]
                g2 = max(g2, float(np.abs(net(a, at, c).values - eb.values).max()))

        # ---- the grid --------------------------------------------------------------------
        for tgt in TARGETS:
            g0 = bk.g_of(tgt)
            for T in TRADES:
                cal_ref = {}
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [(sd, "h", h) for sd in SIDES for h in H_GRID]
                         + [("SYM", "h", 0.0)]                    # G4 cell: h=0 == R=D
                         + [(sd, "h", H_BIG) for sd in ("SYM_TD", "DOWN_TD", "UP_TD")]
                         + [(sd, "h", h) for sd in ("PURE_DOWN", "PURE_UP") for h in H_GATE])
                for fam, Rc, h in cells:
                    if fam == "CAL":
                        r0, t0, gs, nref = bk.run_cal(g0, T, Rc)
                        label = f"R={Rc}"
                        cal_ref[Rc] = (r0.copy(), t0.copy())
                    else:
                        r0, t0, gs, nref = bk.run_side(g0, T, fam, h)
                        label = f"{fam} h={h:.2f}"

                    # ---- identity gates on the fly
                    if fam == "SYM" and h == 0.0 and "D" in cal_ref:
                        cr, ct = cal_ref["D"]
                        g4 = max(g4, float(np.abs(r0.values - cr.values).max()),
                                 float(np.abs(t0.values - ct.values).max()))
                        g4n += 1
                    if h == H_BIG and T in cal_ref:
                        cr, ct = cal_ref[T]
                        g6 = max(g6, float(np.abs(r0.values - cr.values).max()),
                                 float(np.abs(t0.values - ct.values).max()))
                        g6n += 1
                    if fam == "PURE_DOWN":
                        pure_dn_gross.append(float(np.abs(gs.values).max()))

                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    g7 = max(g7, float(gs.max()))
                    crash = gs.loc[CRASH0:CRASH1]
                    cmin = float(crash.min()) if len(crash) else np.nan
                    if fam == "PURE_UP":
                        pure_up_crash.append(cmin)
                    if fam == "SYM" and h in H_GATE:
                        sym_crash.append(cmin)
                    yrs = len(r0) / 252.0

                    if fam in ("SYM", "SYM_TD", "DOWN_TD", "UP_TD") and h in H_GRID:
                        crash_rows.append(dict(panel=pname, target=tgt, T_trade=T, side=fam, h=h,
                                               gross_pre=float(gs.loc[:CRASH0].iloc[-1]),
                                               gross_min=cmin,
                                               gross_end=float(gs.loc[CRASH1:].iloc[0]),
                                               refresh_py=nref / (len(px) / 252.0)))

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
                        LV = B[f"live{c}"]
                        k4bf = (h1 > S["h1"] and h2 > S["h2"]
                                and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                        k4a = (h1 > LV["h1"] and h2 > LV["h2"]
                               and mf["MaxDD"] >= LV["full"]["MaxDD"])
                        k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"]
                                and mo["MaxDD"] >= LV["oos"]["MaxDD"])
                        is_legs = int(ih1 > S["ish1"]) + int(ih2 > S["ish2"]) \
                            + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"]) \
                            + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"])
                        rows.append(dict(
                            panel=pname, target=tgt, T_trade=T, family=fam, R_refresh=Rc,
                            h=h, cell=label, cost=c,
                            turn_py=float(t0.sum() / yrs),
                            is_turn_py=float(t0.loc[:IS_END].sum()
                                             / (len(r0.loc[:IS_END]) / 252.)),
                            refresh_py=nref / (len(px) / 252.0),
                            gross_mean=float(gs.mean()), gross_mean_is=float(gs.loc[:IS_END].mean()),
                            gross_max=float(gs.max()), gross_crash_min=cmin,
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            is_H1=ih1, is_H2=ih2, is_legs=is_legs,
                            is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            bind=bl, n_fail=nbad,
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a, keep4a_oos=k4ao))
        log(f"   grid done ({len([r for r in rows if r['panel'] == pname])} scored rows)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    pd.DataFrame(crash_rows).to_csv(f"{OUT}.crash.csv", index=False)

    # -------------------------------------------------------------------- replication gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 bt_cal diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c) = r0 - turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.target == TGT_MEMO) & (G.T_trade == "W")
                & (G.family == "CAL") & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
        g3 = max(g3, max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                         abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                         abs(row.oos_Sharpe - pub["oSharpe"])))
    gate("G3 reproduces the standing VOLTGT memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    gate(f"G4 SYM h=0 == CALENDAR R=D, cell by cell ({g4n} cells)",
         f"{g4:.3e}", "< 1e-12", g4 < 1e-12 and g4n == len(TARGETS) * len(TRADES) * len(PS))
    gate(f"G6 the h -> inf limit of every TD side IS the calendar book at the trade cadence, "
         f"CAL(R=T) ({g6n} cells)", f"{g6:.3e}", "< 1e-12",
         g6 < 1e-12 and g6n == 3 * len(TARGETS) * len(TRADES) * len(PS))

    # G5: the SYM family reproduces idea 1799's committed grid EXACTLY
    g5 = np.nan
    if GRID_1799.exists():
        old = pd.read_csv(GRID_1799)
        old = old[(old.family == "DRIFT") & (old.h > 0)].copy()
        new = G[(G.family == "SYM") & (G.h.isin(H_GRID))].copy()
        k = ["panel", "target", "T_trade", "h", "cost"]
        m = old.merge(new, on=k, suffixes=("_o", "_n"))
        cmpcols = ["CAGR", "Sharpe", "MaxDD", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "turn_py",
                   "H1", "H2"]
        g5 = max(float(np.abs(m[f"{c}_o"] - m[f"{c}_n"]).max()) for c in cmpcols)
        gate(f"G5 SYM reproduces idea 1799's committed DRIFT grid ({len(m)} rows x "
             f"{len(cmpcols)} cols)", f"max|d| = {g5:.3e}", "< 1e-12",
             g5 < 1e-12 and len(m) == len(H_GRID) * len(TARGETS) * len(TRADES) * len(PS)
             * len(COSTS))
    else:
        gate("G5 SYM reproduces idea 1799's committed DRIFT grid", "file missing", "present", False)

    gate("G7 gross never levered", f"max gross {g7:.6f}", "<= 1.0 + 1e-9", g7 <= 1.0 + 1e-9)
    gate(f"G8 replicates idea 2075's structural KILL: a PURE down-only trigger never leaves zero "
         f"({len(pure_dn_gross)} cells)", f"max gross {max(pure_dn_gross):.3e}", "== 0",
         max(pure_dn_gross) == 0.0)
    gate(f"G9 replicates idea 2075's mirror: PURE up-only never de-grosses in the 2020 crash "
         f"(min gross {min(pure_up_crash):.3f} vs SYM's {max(sym_crash):.3f})",
         f"{min(pure_up_crash):.3f}", "> SYM max", min(pure_up_crash) > max(sym_crash))
    nz = G[(G.family.isin(SIDES)) & (G.h.isin(H_GRID))]
    gate("G10 the h ladder actually moves refresh frequency",
         f"refresh/yr {nz.refresh_py.min():.1f} .. {nz.refresh_py.max():.1f}",
         "min < 52 < max", nz.refresh_py.min() < 52 < nz.refresh_py.max())

    # --------------------------------------------- V1: each side vs the TURNOVER-MATCHED calendar
    log("\n## V1 — each SIDE vs its own arm's TURNOVER-MATCHED point on the CALENDAR ladder")
    log("   (this is idea 1799's own ruler; its published SYM mean at 10 bps is "
        f"+{PUB_1799_V2:.4f})")
    mrows = []
    for (pn, tg, T, c), sub in G.groupby(["panel", "target", "T_trade", "cost"]):
        cal = sub[sub.family == "CAL"].sort_values("turn_py")
        x = cal.turn_py.values
        for _, d in sub[sub.family.isin(SIDES) & sub.h.isin(H_GRID)].iterrows():
            mrows.append(dict(
                panel=pn, target=tg, T_trade=T, cost=c, side=d.family, h=d.h, turn_py=d.turn_py,
                cal_turn_lo=x.min(), cal_turn_hi=x.max(),
                inside_ladder=bool(x.min() <= d.turn_py <= x.max()),
                d_oos_Sharpe=d.oos_Sharpe - float(np.interp(d.turn_py, x, cal.oos_Sharpe.values)),
                d_oos_MaxDD=d.oos_MaxDD - float(np.interp(d.turn_py, x, cal.oos_MaxDD.values)),
                d_oos_CAGR=d.oos_CAGR - float(np.interp(d.turn_py, x, cal.oos_CAGR.values)),
                d_full_Sharpe=d.Sharpe - float(np.interp(d.turn_py, x, cal.Sharpe.values)),
                d_full_MaxDD=d.MaxDD - float(np.interp(d.turn_py, x, cal.MaxDD.values))))
    M = pd.DataFrame(mrows)
    M.to_csv(f"{OUT}.matched.csv", index=False)
    M0 = M[(M.cost == COST0) & M.inside_ladder]
    v1 = {}
    log(f"   {'side':8s} {'n':>4s} {'dOOS Sharpe':>12s} {'win':>6s} {'dOOS MaxDD':>11s} "
        f"{'dOOS CAGR':>10s} {'turn/yr':>8s}")
    for sd in SIDES:
        s = M0[M0.side == sd]
        v1[sd] = float(s.d_oos_Sharpe.mean())
        log(f"   {sd:8s} {len(s):4d} {s.d_oos_Sharpe.mean():+12.4f} "
            f"{(s.d_oos_Sharpe > 0).mean():6.3f} {s.d_oos_MaxDD.mean()*100:+10.2f}pp "
            f"{s.d_oos_CAGR.mean()*100:+9.2f}pp {s.turn_py.mean():8.2f}")
    V1 = (v1["DOWN_TD"] >= 0.5 * v1["SYM"]) and (v1["UP_TD"] < 0.5 * v1["SYM"])
    log(f"   V1 (DOWN owns the Sharpe): DOWN_TD {v1['DOWN_TD']:+.4f} >= 0.5 x SYM "
        f"{0.5*v1['SYM']:+.4f} AND UP_TD {v1['UP_TD']:+.4f} < that  ->  "
        f"{'TRIGGERED' if V1 else 'NOT TRIGGERED'}")

    # ------------------------------------------------- the EXACT attribution against CAL(R = T)
    log("\n## ATTRIBUTION — each side minus the CAL(R=T) zero point (its own h -> inf limit)")
    zero = G[(G.family == "CAL")].set_index(["panel", "target", "T_trade", "R_refresh", "cost"])
    arows = []
    for _, d in G[G.family.isin(SIDES) & G.h.isin(H_GRID)].iterrows():
        z = zero.loc[(d.panel, d.target, d.T_trade, d.T_trade, d.cost)]
        arows.append(dict(panel=d.panel, target=d.target, T_trade=d.T_trade, cost=d.cost,
                          side=d.family, h=d.h,
                          d_oos_Sharpe=d.oos_Sharpe - z.oos_Sharpe,
                          d_oos_MaxDD=d.oos_MaxDD - z.oos_MaxDD,
                          d_oos_CAGR=d.oos_CAGR - z.oos_CAGR,
                          d_L5=d.L5_CAGR - z.L5_CAGR, d_L4=d.L4_DD - z.L4_DD,
                          d_turn=d.turn_py - z.turn_py))
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.attribution.csv", index=False)
    A0 = A[A.cost == COST0]
    piv = A0.pivot_table(index=["panel", "target", "T_trade", "h"], columns="side",
                         values=["d_oos_Sharpe", "d_oos_MaxDD", "d_oos_CAGR", "d_turn"])
    log(f"   {'side':8s} {'dOOS Sharpe':>12s} {'dOOS MaxDD':>12s} {'dOOS CAGR':>11s} "
        f"{'dturn/yr':>9s}   (vs CAL(R=T), {len(A0)//len(SIDES)} cells each, 10 bps)")
    for sd in SIDES:
        s = A0[A0.side == sd]
        log(f"   {sd:8s} {s.d_oos_Sharpe.mean():+12.4f} {s.d_oos_MaxDD.mean()*100:+11.2f}pp "
            f"{s.d_oos_CAGR.mean()*100:+10.2f}pp {s.d_turn.mean():+9.2f}")
    inter = {}
    for m_ in ("d_oos_Sharpe", "d_oos_MaxDD", "d_oos_CAGR", "d_turn"):
        both = piv[m_]["SYM_TD"]
        add = piv[m_]["DOWN_TD"] + piv[m_]["UP_TD"]
        inter[m_] = float((both - add).mean())
        log(f"   interaction residual  {m_:14s} SYM_TD - (DOWN_TD + UP_TD) = "
            f"{(both - add).mean():+.5f}  (|resid| / |SYM_TD| = "
            f"{abs((both-add).mean()) / max(abs(both.mean()), 1e-12):.3f})")

    # ----------------------------------------------------------------- V2: who owns the CAGR cost
    log("\n## V2 — who owns the CAGR cost (4b CAGR margin L5_CAGR, 10 bps, all cells)")
    G0 = G[(G.cost == COST0) & G.family.isin(SIDES) & G.h.isin(H_GRID)]
    l5 = {sd: float(G0[G0.family == sd].L5_CAGR.mean()) for sd in SIDES}
    l5bind = {sd: int((G0[G0.family == sd].L5_CAGR <= 0).sum()) for sd in SIDES}
    for sd in SIDES:
        s = G0[G0.family == sd]
        log(f"   {sd:8s} L5_CAGR mean {l5[sd]*100:+7.2f}pp   binds at {l5bind[sd]:4d} of {len(s)}"
            f"   OOS CAGR {s.oos_CAGR.mean():7.2%}   OOS Sharpe {s.oos_Sharpe.mean():.4f}"
            f"   OOS MaxDD {s.oos_MaxDD.mean():7.2%}")
    V2 = l5["UP_TD"] > l5["SYM_TD"] > l5["DOWN_TD"]
    log(f"   V2 (UP owns the CAGR cost): UP_TD {l5['UP_TD']*100:+.2f} > SYM_TD "
        f"{l5['SYM_TD']*100:+.2f} > DOWN_TD {l5['DOWN_TD']*100:+.2f}  ->  "
        f"{'TRIGGERED' if V2 else 'NOT TRIGGERED'}")

    # ----------------------------------------------------------------------- KEEP paths by side
    log("\n## BOTH KEEP PATHS, by side and cost (all cells; SIDES x h ladder)")
    for c in COSTS:
        sub = G[(G.cost == c) & G.family.isin(SIDES) & G.h.isin(H_GRID)]
        log(f"   {c:2d} bps: " + "; ".join(
            f"{sd} 4b {int(s.keep4b.sum())}/{len(s)} (full {int(s.keep4b_full.sum())}) "
            f"4a {int(s.keep4a.sum())}"
            for sd, s in sub.groupby("family")))
    log("   binding leg (10 bps, 4b failures): " + "; ".join(
        f"{sd}: " + ", ".join(f"{k} {v}" for k, v in
                              G0[(G0.family == sd) & ~G0.keep4b].bind.value_counts()
                              .head(3).items())
        for sd in SIDES))
    log("   by panel (10 bps, 4b FULL+OOS): " + "; ".join(
        f"{pn}/{sd} {int(s.keep4b.sum())}/{len(s)}"
        for (pn, sd), s in G0.groupby(["panel", "family"])))

    # ------------------------------------------------------------------- rule 8: the choosers
    log("\n## RULE 8 — (t, h) or (t, R) chosen on 2009-2016 ONLY; 2017-2026 read exactly once")
    log("   C_ISDD is REPORTED BUT ILLEGAL (idea 2075: it selects the degenerate low-exposure "
        "cell on any corpus admitting a cash cell); it is excluded from every verdict.")
    CH = {"C_ISSHARPE": lambda d: d.is_Sharpe,
          "C_ISCALMAR": lambda d: d.is_Calmar,
          "C_ISLEGS": lambda d: d.is_legs * 1e6 + d.is_Sharpe,
          "C_ISDD": lambda d: d.is_MaxDD}
    LEGAL = ["C_ISSHARPE", "C_ISCALMAR", "C_ISLEGS"]
    ch_rows = []
    for (pn, T, c), arm in G.groupby(["panel", "T_trade", "cost"]):
        Bp = BASE[pn]
        for fam in ["CAL"] + SIDES:
            sub = arm[(arm.family == fam)
                      & ((arm.family == "CAL") | arm.h.isin(H_GRID))]
            sub = sub.sort_values(["target", "h", "R_refresh"], kind="mergesort")
            if not len(sub):
                continue
            for cname, f in CH.items():
                pick = sub.loc[f(sub).astype(float).idxmax()]
                ch_rows.append(dict(
                    panel=pn, T_trade=T, cost=c, family=fam, chooser=cname, legal=cname in LEGAL,
                    target=pick.target, h=pick.h, R_refresh=pick.R_refresh, cell=pick.cell,
                    is_Sharpe=pick.is_Sharpe, is_MaxDD=pick.is_MaxDD,
                    oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe, oos_MaxDD=pick.oos_MaxDD,
                    turn_py=pick.turn_py, gross_mean=pick.gross_mean,
                    keep4b_full=pick.keep4b_full, keep4b_oos=pick.keep4b_oos, keep4b=pick.keep4b,
                    keep4a=pick.keep4a, keep4a_oos=pick.keep4a_oos, bind=pick.bind,
                    base_oos_Sharpe=Bp[f"live{c}"]["oos"]["Sharpe"],
                    base_oos_CAGR=Bp[f"live{c}"]["oos"]["CAGR"],
                    base_oos_MaxDD=Bp[f"live{c}"]["oos"]["MaxDD"],
                    spy_oos_Sharpe=Bp["spy"]["oos"]["Sharpe"],
                    spy_oos_CAGR=Bp["spy"]["oos"]["CAGR"],
                    spy_oos_MaxDD=Bp["spy"]["oos"]["MaxDD"]))
    C = pd.DataFrame(ch_rows)
    C.to_csv(f"{OUT}.walkforward.csv", index=False)
    C0 = C[(C.cost == COST0) & C.legal]
    log(f"   {'family':8s} {'n':>3s} {'4b FULL+OOS':>12s} {'4a':>4s}  mean OOS "
        f"CAGR / Sharpe / MaxDD   (10 bps, legal choosers only)")
    for fam, s in C0.groupby("family"):
        log(f"   {fam:8s} {len(s):3d} {int(s.keep4b.sum()):12d} {int(s.keep4a.sum()):4d}  "
            f"{s.oos_CAGR.mean():7.2%} / {s.oos_Sharpe.mean():.4f} / {s.oos_MaxDD.mean():7.2%}")
    log("   picks (10 bps, legal): " + "; ".join(
        f"{fam}: " + ", ".join(f"{k} x{v}" for k, v in s.cell.value_counts().head(4).items())
        for fam, s in C0.groupby("family")))

    reached = C0[C0.keep4b & C0.family.isin(SIDES)]
    V3_counts = {sd: int(G0[G0.family == sd].keep4b.sum()) for sd in SIDES}
    V3 = (V3_counts["DOWN_TD"] >= V3_counts["SYM_TD"]) and bool(
        (reached.family == "DOWN_TD").any())
    log(f"   V3 (the half-rule reaches): DOWN_TD 4b cells {V3_counts['DOWN_TD']} >= SYM_TD "
        f"{V3_counts['SYM_TD']} AND an IS-only chooser reaches one "
        f"({int((reached.family == 'DOWN_TD').sum())} picks)  ->  "
        f"{'TRIGGERED' if V3 else 'NOT TRIGGERED'}")

    log(f"\n   RULE-8 CELLS CLEARING 4b FULL *AND* OOS, reached by a LEGAL chooser "
        f"({len(reached)} of {len(C0[C0.family.isin(SIDES)])} side picks at 10 bps):")
    for _, d in reached.iterrows():
        log(f"     {d.panel:9s} T={d.T_trade} {d.family:8s} {d.cell:18s} by {d.chooser:11s} "
            f"OOS {d.oos_CAGR:7.2%} / {d.oos_Sharpe:.4f} / {d.oos_MaxDD:7.2%}   "
            f"(live v2 OOS {d.base_oos_Sharpe:.4f}, SPY OOS {d.spy_oos_Sharpe:.4f}), "
            f"4a {'PASS' if d.keep4a else 'fail'}")
    V4 = len(reached) > 0

    # ------------------------------------------------------------------------ crash mechanism
    log("\n## MECHANISM — gross through the 2020 crash window "
        f"({CRASH0} -> {CRASH1}), 10 bps grid cells")
    CR = pd.DataFrame(crash_rows)
    for sd in SIDES:
        s = CR[CR.side == sd]
        log(f"   {sd:8s} pre {s.gross_pre.mean():.3f} -> trough {s.gross_min.mean():.3f} "
            f"-> out {s.gross_end.mean():.3f}   ({s.refresh_py.mean():5.1f} refreshes/yr)")
    u = CR[(CR.panel == "U56") & (CR.T_trade == "M") & (CR.target == 0.16) & (CR.h == 0.12)]
    for _, d in u.iterrows():
        log(f"   U56 T=M t=0.16 h=0.12  {d.side:8s} {d.gross_pre:.3f} -> {d.gross_min:.3f} "
            f"-> {d.gross_end:.3f}")

    # ------------------------------------------------------------------------------- verdict
    log("\n## PRE-STATED VERDICTS")
    for k, v in (("V1 DOWN owns the Sharpe", V1), ("V2 UP owns the CAGR cost", V2),
                 ("V3 the half-rule reaches", V3), ("V4 a reached 4b cell exists", V4)):
        log(f"   {k:32s} {'TRIGGERED' if v else 'NOT TRIGGERED'}")
    npass = sum(g["pass_"] for g in _gates)
    log(f"\n## GATES {npass}/{len(_gates)} passed;  {len(G)} scored rows written to "
        f"{OUT.name}.grid.csv.gz")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
