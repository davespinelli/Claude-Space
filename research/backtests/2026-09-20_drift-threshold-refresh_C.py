#!/usr/bin/env python3
"""Idea 1799 (lane C, 2026-09-20) — DOES A DRIFT-THRESHOLD REFRESH DOMINATE A CALENDAR REFRESH?

THE DEFECT THIS PRICES.  The record's REFRESH axis `R` is a CALENDAR axis: `g = clip(t/sigma20,
0, 1)` is re-read on the last trading day of each D / W / M / Q period whether or not anything
has moved.  Three runs on 2026-09-20 converged on the same residue.  Idea 1767: the 4b verdict is
a function of `R` alone (`R in {D,W}` clears 4b in 4 of 6 cells at EVERY trade cadence, `R in
{M,Q}` 0 of 6), and 23 of 24 legal IS-only picks land on a STALE scalar.  Idea 1793: `R = D`
clears 4b FULL *and* OOS at 4 of 4 large-panel arms for every `t >= 0.10`, the OOS oracle takes
`t = 0.12, R = D` (U56 OOS 15.28% / 1.3485 / -15.79%), and NO legal IS-only chooser ever reaches
it.  Idea 1789: the stale preference is an IS-WINDOW fact (79.2% stale on 2009-2016, 0.0% on any
window containing the 2020 crash), and the FRESH scalar clears 4b at 32 of 48 cells against the
stale scalar's 0 of 48.  So freshness is worth a lot and the calendar is the only way the record
has ever bought it — at a flat price of one full re-read per period.

THE FIX TESTED HERE.  The only thing the exposure scalar cares about is how far the book's HELD
gross has drifted from the scalar it should be running.  Re-read `g` only when

    | g_t  -  gross_held_t |  >  h

("DRIFT"), which is CADENCE-FREE: turnover becomes endogenous, quiet tapes cost nothing and a vol
spike is answered the day it happens rather than on Friday.  `h -> 0` reproduces `R = D` exactly
(gate G4); `h` large never refreshes at all.  The calendar ladder `R in {D,W,M,Q}` is the
comparand, priced on the same tape, the same names and the same trade cadence.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION (REACHABILITY).  At 10 bps, over the 6 arms (panel x trade cadence),
      the DRIFT family's legal IS-only picks clear 4b FULL *and* OOS on STRICTLY MORE arms than
      the CALENDAR family's.  Not triggered -> the drift threshold is KILLED as a fix to idea
      1793's reachability residue.
  V2  TURNOVER EFFICIENCY.  Pooled over cells at 10 bps, a drift book beats the turnover-MATCHED
      point on its own arm's calendar ladder (linear interpolation of the ladder's OOS Sharpe at
      the drift book's realised turnover) in MORE THAN HALF of cells AND on the mean.  This is the
      idea's own "buys freshness only where freshness is worth paying for".
  V3  FRESHNESS REACH.  The drift picks land on books at least as fresh as a WEEKLY calendar
      re-read (realised refreshes/yr >= 52) on more arms than the calendar picks do.
  V4  CAPITAL.  Any cell clearing 4b FULL *and* OOS that a legal IS-only chooser actually REACHES
      is a KEEP-4b candidate; path 4a is scored at every cell too.

DIALS.  EXACTLY TWO are tuned, and only ever within one family: the DRIFT family spends TARGET `t`
and THRESHOLD `h`; the CALENDAR family spends TARGET `t` and REFRESH `R`.  No chooser ever selects
across families, across panels, across trade cadence or across cost.  REPORTED, NOT TUNED: TRADE
cadence `T in {W,M}` (separate arms), PANEL {U56, B136, SMALL}, COST {0,10,25,50} bps.  The sigma
convention is FIXED at the standing memo's (L=20, d=0).  Every grid point is published
(`.grid.csv`).

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The DRIFT-vs-CALENDAR contrast is same-tape / same-names / same-grid with only the refresh TRIGGER
moved, so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_drift-threshold-refresh_C.py
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

DATE, SLUG = "2026-09-20", "drift-threshold-refresh"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]                       # calendar family
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]  # h=0 is the G4 gate cell
H_GRID = [h for h in THRESH if h > 0]                # the tuned drift ladder (h = 0 is not a dial)
TRADES = ["W", "M"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0

# committed numbers this run must reproduce (standing VOLTGT memo, points 2-4; idea 1793 G3)
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_1793_ORACLE = dict(oCAGR=0.1528, oSharpe=1.3485, oMaxDD=-0.1579)   # U56 t=0.12 R=D, 10bps
ORACLE_T = "M"      # idea 1793 published this cell on the MONTHLY-trade arm (see G5 note)

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
    t-d.  (L,d) = (20,0) is the standing memo's convention (idea 1771 owns that surface)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------ the two refresh runners
def bt_cal(px_ret, W0, g0, mT, mR):
    """CALENDAR refresh (idea 1767's two-schedule construction).  `g_eff` is re-read on refresh
    days only; trade days re-spread the names to the scalar in force.  T == R reproduces the
    standard single-schedule book exactly (gate G1)."""
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
    """DRIFT-THRESHOLD refresh.  Identical to bt_cal except the refresh TRIGGER: the scalar is
    re-read on day i iff |g0[i] - gross_held| > h, gross_held being the book's actual total
    exposure entering day i.  h = 0 makes the trigger fire every day, i.e. R = D (gate G4)."""
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


class Book:
    """Pre-shifted arrays for one panel, so every (t, T, scheme) run is a single loop."""

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

    def run_cal(self, g0, T, R):
        r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[R])
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)

    def run_drift(self, g0, T, h):
        r, t, gs, nref = bt_drift(self.R, self.W, g0, self.masks[T], h)
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


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 1799 (lane C, {DATE}) — does a DRIFT-THRESHOLD refresh dominate a CALENDAR "
        f"refresh?")
    log(f"# tuned dials (2, within a family): TARGET t {TARGETS} x [ DRIFT h {H_GRID} | CALENDAR "
        f"R {REFRESH} ].  reported, not tuned: TRADE T {TRADES} (separate arms), PANEL, COST "
        f"{COSTS} bps.  sigma FIXED at (L={SIG_L}, d={SIG_D}).  warm-up {WARMUP}; "
        f"IS <= {IS_END}; OOS >= {OOS_START}.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows = []
    BASE = {}
    g1r = g1t = g2 = g3 = g4 = 0.0
    g9 = 0.0
    g4n = 0

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        yrs_all = None
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
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [("DRIFT", "h", h) for h in THRESH])
                cal_ref = {}
                for fam, Rc, h in cells:
                    if fam == "CAL":
                        r0, t0, gs, nref = bk.run_cal(g0, T, Rc)
                        label = f"R={Rc}"
                    else:
                        r0, t0, gs, nref = bk.run_drift(g0, T, h)
                        label = f"h={h:.2f}"
                    if fam == "CAL":
                        cal_ref[Rc] = (r0.copy(), t0.copy())
                    if fam == "DRIFT" and h == 0.0 and "D" in cal_ref:
                        cr, ct = cal_ref["D"]
                        g4 = max(g4, float(np.abs(r0.values - cr.values).max()),
                                 float(np.abs(t0.values - ct.values).max()))
                        g4n += 1
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    g9 = max(g9, float(gs.max()))
                    yrs = len(r0) / 252.0
                    yrs_all = yrs
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
                            is_turn_py=float(t0.loc[:IS_END].sum() / (len(r0.loc[:IS_END]) / 252.)),
                            refresh_py=nref / (len(px) / 252.0),
                            gross_mean=float(gs.mean()), gross_mean_is=float(gs.loc[:IS_END].mean()),
                            gross_max=float(gs.max()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            is_H1=ih1, is_H2=ih2, is_legs=is_legs,
                            is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            bind=bl, n_fail=nbad,
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a, keep4a_oos=k4ao))
        log(f"   grid done ({len([r for r in rows if r['panel'] == pname])} scored rows, "
            f"{yrs_all:.1f}y book window)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

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
    gate(f"G4 DRIFT h=0 == CALENDAR R=D, cell by cell ({g4n} cells)",
         f"{g4:.3e}", "< 1e-12", g4 < 1e-12 and g4n == len(TARGETS) * len(TRADES) * len(PS))
    orow = G[(G.panel == "U56") & (G.target == 0.12) & (G.T_trade == ORACLE_T)
             & (G.family == "CAL")
             & (G.R_refresh == "D") & (G.cost == COST0)].iloc[0]
    g5 = max(abs(orow.oos_CAGR - PUB_1793_ORACLE["oCAGR"]),
             abs(orow.oos_Sharpe - PUB_1793_ORACLE["oSharpe"]),
             abs(orow.oos_MaxDD - PUB_1793_ORACLE["oMaxDD"]))
    gate(f"G5 reproduces idea 1793's OOS oracle cell (U56 t=0.12 R=D, T={ORACLE_T})",
         f"max|d| = {g5:.3e}", "< 1e-3", g5 < 1e-3)
    gate("G6 gross never levered", f"max gross {g9:.6f}", "<= 1.0 + 1e-9", g9 <= 1.0 + 1e-9)
    nz = G[(G.family == "DRIFT") & (G.h > 0)]
    gate("G7 the drift ladder actually moves refresh frequency",
         f"refresh/yr {nz.refresh_py.min():.1f} .. {nz.refresh_py.max():.1f}",
         "min < 52 < max", nz.refresh_py.min() < 52 < nz.refresh_py.max())

    # ------------------------------------------------------- V2: turnover-matched comparison
    log("\n## V2 — DRIFT vs its own arm's TURNOVER-MATCHED point on the CALENDAR ladder")
    mrows = []
    for (pn, tg, T, c), sub in G.groupby(["panel", "target", "T_trade", "cost"]):
        cal = sub[sub.family == "CAL"].sort_values("turn_py")
        x = cal.turn_py.values
        for _, d in sub[(sub.family == "DRIFT") & (sub.h > 0)].iterrows():
            inside = x.min() <= d.turn_py <= x.max()
            mrows.append(dict(
                panel=pn, target=tg, T_trade=T, cost=c, h=d.h, turn_py=d.turn_py,
                cal_turn_lo=x.min(), cal_turn_hi=x.max(), inside_ladder=inside,
                d_oos_Sharpe=d.oos_Sharpe - float(np.interp(d.turn_py, x, cal.oos_Sharpe.values)),
                d_oos_MaxDD=d.oos_MaxDD - float(np.interp(d.turn_py, x, cal.oos_MaxDD.values)),
                d_oos_CAGR=d.oos_CAGR - float(np.interp(d.turn_py, x, cal.oos_CAGR.values)),
                d_full_Sharpe=d.Sharpe - float(np.interp(d.turn_py, x, cal.Sharpe.values)),
                d_full_MaxDD=d.MaxDD - float(np.interp(d.turn_py, x, cal.MaxDD.values))))
    M = pd.DataFrame(mrows)
    M.to_csv(f"{OUT}.matched.csv", index=False)
    M0 = M[(M.cost == COST0) & M.inside_ladder]
    v2_share = float((M0.d_oos_Sharpe > 0).mean())
    v2_mean = float(M0.d_oos_Sharpe.mean())
    log(f"   {len(M0)} drift cells at {COST0} bps inside the calendar turnover range "
        f"({len(M) // len(COSTS) - len(M0)} outside)")
    log(f"   OOS Sharpe vs turnover-matched calendar: mean {v2_mean:+.4f}, "
        f"win share {v2_share:.3f}; MaxDD mean {M0.d_oos_MaxDD.mean()*100:+.2f} pp; "
        f"CAGR mean {M0.d_oos_CAGR.mean()*100:+.2f} pp")
    log("   by panel: " + "; ".join(
        f"{p} mean {s.d_oos_Sharpe.mean():+.4f} win {(s.d_oos_Sharpe > 0).mean():.2f}"
        for p, s in M0.groupby("panel")))

    # ------------------------------------------------------------------- rule 8: the choosers
    log("\n## RULE 8 — (t, h) or (t, R) chosen on 2009-2016 ONLY; 2017-2026 read exactly once")
    CH = {"C_ISSHARPE": lambda d: d.is_Sharpe,
          "C_ISCALMAR": lambda d: d.is_Calmar,
          "C_ISDD": lambda d: d.is_MaxDD,
          "C_ISLEGS": lambda d: d.is_legs * 1e6 + d.is_Sharpe}
    ch_rows = []
    for (pn, T, c), arm in G.groupby(["panel", "T_trade", "cost"]):
        for fam in ("CAL", "DRIFT"):
            sub = arm[(arm.family == fam) & ((arm.family == "CAL") | (arm.h > 0))]
            sub = sub.sort_values(["target", "h", "R_refresh"], kind="mergesort")
            for cname, f in CH.items():
                pick = sub.loc[f(sub).astype(float).idxmax()]
                ch_rows.append(dict(panel=pn, T_trade=T, cost=c, family=fam, chooser=cname,
                                    cell=pick.cell, target=pick.target,
                                    turn_py=pick.turn_py, refresh_py=pick.refresh_py,
                                    oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                                    oos_MaxDD=pick.oos_MaxDD,
                                    keep4b_full=pick.keep4b_full, keep4b_oos=pick.keep4b_oos,
                                    keep4b=pick.keep4b, keep4a=pick.keep4a,
                                    keep4a_oos=pick.keep4a_oos, bind=pick.bind))
            orc = sub.loc[sub.oos_Sharpe.astype(float).idxmax()]      # OOS ORACLE: not a pick
            ch_rows.append(dict(panel=pn, T_trade=T, cost=c, family=fam, chooser="ORACLE_OOS",
                                cell=orc.cell, target=orc.target, turn_py=orc.turn_py,
                                refresh_py=orc.refresh_py, oos_CAGR=orc.oos_CAGR,
                                oos_Sharpe=orc.oos_Sharpe, oos_MaxDD=orc.oos_MaxDD,
                                keep4b_full=orc.keep4b_full, keep4b_oos=orc.keep4b_oos,
                                keep4b=orc.keep4b, keep4a=orc.keep4a, keep4a_oos=orc.keep4a_oos,
                                bind=orc.bind))
    C = pd.DataFrame(ch_rows)
    C.to_csv(f"{OUT}.choosers.csv", index=False)

    C0 = C[(C.cost == COST0) & (C.chooser != "ORACLE_OOS")]
    arms_big = C0[C0.panel.isin(["U56", "B136"])]
    log(f"   legal IS-only picks at {COST0} bps: {len(C0)} "
        f"({len(CH)} choosers x 2 families x 6 arms)")
    for fam in ("CAL", "DRIFT"):
        s = C0[C0.family == fam]
        log(f"   {fam:5s}: 4b FULL+OOS {int(s.keep4b.sum())}/{len(s)}, "
            f"4a {int(s.keep4a.sum())}/{len(s)}, 4a OOS {int(s.keep4a_oos.sum())}/{len(s)}, "
            f"mean OOS Sharpe {s.oos_Sharpe.mean():.4f}, mean OOS MaxDD {s.oos_MaxDD.mean():.2%}, "
            f"mean turns/yr {s.turn_py.mean():.2f}")
    # V1: arms (panel x T) on which SOME legal chooser in the family reaches a 4b FULL+OOS cell
    v1 = {}
    for fam in ("CAL", "DRIFT"):
        s = C0[C0.family == fam]
        v1[fam] = int(s.groupby(["panel", "T_trade"]).keep4b.any().sum())
    log(f"   V1 arms reached (any chooser): CAL {v1['CAL']}/6, DRIFT {v1['DRIFT']}/6")
    # per-chooser arm counts
    for cname in CH:
        line = []
        for fam in ("CAL", "DRIFT"):
            s = C0[(C0.family == fam) & (C0.chooser == cname)]
            line.append(f"{fam} {int(s.keep4b.sum())}/{len(s)}")
        log(f"     {cname:12s} 4b FULL+OOS arms: " + ", ".join(line))
    fresh = C0.assign(fresh=C0.refresh_py >= 52.0)
    v3 = {f: int(fresh[fresh.family == f].groupby(["panel", "T_trade"]).fresh.any().sum())
          for f in ("CAL", "DRIFT")}
    log(f"   V3 arms whose picks are at least weekly-fresh: CAL {v3['CAL']}/6, "
        f"DRIFT {v3['DRIFT']}/6 (mean refresh/yr CAL "
        f"{C0[C0.family=='CAL'].refresh_py.mean():.1f}, DRIFT "
        f"{C0[C0.family=='DRIFT'].refresh_py.mean():.1f})")
    dp = C0[C0.family == "DRIFT"]
    log("   DRIFT picks by h rung: " + "; ".join(
        f"{k} x{v}" for k, v in dp.cell.value_counts().sort_index().items())
        + f"   (top rung of the ladder is h={max(THRESH):.2f})")
    log("   CAL picks by R rung: " + "; ".join(
        f"{k} x{v}" for k, v in C0[C0.family == 'CAL'].cell.value_counts().sort_index().items()))
    orc = C[(C.cost == COST0) & (C.chooser == "ORACLE_OOS")]
    log("   OOS ORACLE (reported, NOT a pick): " + "; ".join(
        f"{r.panel}/{r.T_trade}/{r.family} {r.cell} t={r.target} "
        f"{r.oos_Sharpe:.4f}{' 4b' if r.keep4b else ''}"
        for _, r in orc[orc.panel.isin(['U56', 'B136'])].iterrows()))

    # ---------------------------------------------------------------- the verdicts
    log("\n## PRE-STATED VERDICTS")
    V1 = v1["DRIFT"] > v1["CAL"]
    V2 = (v2_share > 0.5) and (v2_mean > 0)
    V3 = v3["DRIFT"] > v3["CAL"]
    reach = C0[C0.keep4b]
    V4 = len(reach) > 0
    log(f"   V1 REACHABILITY   {'PASS' if V1 else 'FAIL'} — DRIFT reaches 4b FULL+OOS on "
        f"{v1['DRIFT']} arms vs CALENDAR's {v1['CAL']} (strictly more required)")
    log(f"   V2 TURNOVER EFF.  {'PASS' if V2 else 'FAIL'} — win share {v2_share:.3f}, "
        f"mean dOOS Sharpe {v2_mean:+.4f} (both must be > 0.5 / > 0)")
    log(f"   V3 FRESHNESS      {'PASS' if V3 else 'FAIL'} — DRIFT picks weekly-fresh on "
        f"{v3['DRIFT']} arms vs CALENDAR's {v3['CAL']}")
    log(f"   V4 CAPITAL        {'PASS' if V4 else 'FAIL'} — {len(reach)} legal picks at "
        f"{COST0} bps clear 4b FULL+OOS "
        f"({int(reach.family.eq('DRIFT').sum())} DRIFT / {int(reach.family.eq('CAL').sum())} CAL)")
    if V4:
        for _, r in reach.iterrows():
            f = G[(G.panel == r.panel) & (G.T_trade == r.T_trade) & (G.cost == COST0)
                  & (G.cell == r.cell) & (G.target == r.target)].iloc[0]
            log(f"      REACHED {r.panel}/{r.T_trade}/{r.family}/{r.chooser}: {r.cell} "
                f"t={r.target}  OOS {r.oos_CAGR:.2%} / {r.oos_Sharpe:.4f} / {r.oos_MaxDD:.2%}, "
                f"FULL {f.CAGR:.2%} / {f.Sharpe:.4f} / {f.MaxDD:.2%} (halves {f.H1:.4f} / "
                f"{f.H2:.4f}), {r.turn_py:.2f} turns/yr, refresh {r.refresh_py:.0f}/yr, "
                f"mean gross {f.gross_mean:.3f}, 4a {bool(f.keep4a)}")
        log("   cost-rung robustness of the reached picks (same cell, all rungs):")
        for (pn, T, fam, cell, tg), _ in reach.groupby(
                ["panel", "T_trade", "family", "cell", "target"]):
            ss = G[(G.panel == pn) & (G.T_trade == T) & (G.cell == cell) & (G.target == tg)]
            ok = "/".join(f"{int(ss[ss.cost == c].keep4b.iloc[0])}" for c in COSTS)
            log(f"      {pn}/{T}/{fam} {cell} t={tg}: 4b FULL+OOS at "
                f"{'/'.join(str(c) for c in COSTS)} bps = {ok}")

    # ---------------------------------------------------------------- headline census
    log("\n## CENSUS (every grid point published in .grid.csv)")
    for c in COSTS:
        s = G[G.cost == c]
        log(f"   {c:2d} bps: cells {len(s)}; 4b FULL {int(s.keep4b_full.sum())}, "
            f"4b OOS {int(s.keep4b_oos.sum())}, 4b FULL+OOS {int(s.keep4b.sum())} "
            f"(CAL {int(s[s.family=='CAL'].keep4b.sum())} / "
            f"DRIFT {int(s[s.family=='DRIFT'].keep4b.sum())}); "
            f"4a {int(s.keep4a.sum())}, 4a OOS {int(s.keep4a_oos.sum())}")
    s0 = G[G.cost == COST0]
    log("   binding 4b leg at 10 bps (whole grid): " + "; ".join(
        f"{k} {v}" for k, v in s0.bind.value_counts().head(8).items()))
    log("   4b FULL+OOS by cell (10 bps, large panels):")
    for cell, s in s0[s0.panel.isin(["U56", "B136"])].groupby("cell"):
        log(f"      {cell:8s} {int(s.keep4b.sum())}/{len(s)}  mean OOS Sharpe "
            f"{s.oos_Sharpe.mean():.4f}, turns/yr {s.turn_py.mean():.2f}, "
            f"refresh/yr {s.refresh_py.mean():.0f}")

    # ------------------------------------------------- MECHANISM: the 2020 crash, gross paths
    log("\n## MECHANISM — gross path through the 2020 crash (2020-02-19 -> 2020-03-23), "
        "U56 / T=M / t=0.16")
    px56 = PS[0][1]
    bk = Book(px56, PS[0][2], px56.index)
    g0 = bk.g_of(0.16)
    crow = []
    for lbl, runner in ([(f"R={Rc}", ("cal", Rc)) for Rc in REFRESH]
                        + [(f"h={hh:.2f}", ("drift", hh)) for hh in (0.05, 0.12, 0.25)]):
        kind, arg = runner
        _, _, gs, _ = (bk.run_cal(g0, "M", arg) if kind == "cal" else bk.run_drift(g0, "M", arg))
        w = gs.loc["2020-02-19":"2020-03-23"]
        crow.append(dict(cell=lbl, gross_0219=float(gs.loc["2020-02-19"]),
                         gross_min=float(w.min()), min_date=str(w.idxmin().date()),
                         days_to_half=int((w > 0.5 * gs.loc["2020-02-19"]).sum()),
                         gross_mean_window=float(w.mean())))
        log(f"   {lbl:8s} gross 2020-02-19 {crow[-1]['gross_0219']:.3f} -> min "
            f"{crow[-1]['gross_min']:.3f} on {crow[-1]['min_date']}; window mean "
            f"{crow[-1]['gross_mean_window']:.3f}; sessions above half the pre-crash gross "
            f"{crow[-1]['days_to_half']}")
    pd.DataFrame(crow).to_csv(f"{OUT}.crash.csv", index=False)

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in _gates)
    log(f"\n## gates {npass}/{len(_gates)} pass")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
