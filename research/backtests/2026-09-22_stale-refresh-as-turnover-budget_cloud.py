#!/usr/bin/env python3
"""Idea 1795 (lane cloud, 2026-09-22) — IS THE STALE-REFRESH PREFERENCE A TURNOVER-BUDGET
FACT IN DISGUISE?

THE DEFECT THIS PRICES.  The record's exposure scalar `g = clip(t/sigma20, 0, 1)` is re-read on
a CALENDAR schedule `R in {D,W,M,Q}`.  Idea 1767 found 23 of 24 legal IS-only picks land on a
STALE scalar (`R in {M,Q}`); ideas 1789/1793 found the FRESH scalar (`R = D`) is the one that
actually clears 4b out of sample, and that no legal IS-only chooser ever reaches it.  A stale
scalar trades 1.3-1.6 turns/yr against a daily one's 1.9-5.5.  At 10 bps that is 6-42 bp/yr of
saved cost, which is the same order as the IS Sharpe gaps the chooser is deciding on.  So the
IS statistic may be buying SAVED COST, not better returns.  If it is, the fix is a TURNOVER
BUDGET, not a cadence: refresh the scalar whenever it moves, but only while the book can afford
to.

WHAT IS PRICED (two arms, both required).
  ARM A (DECOMPOSITION).  Every committed `R` gap on this grid is split exactly:
        d_net(c) = d_gross  -  (c/1e4) * d_turnover
  and the TURNOVER SHARE  (c/1e4)*d_turn / d_net  is published for every (panel, T, t, R) cell at
  10 / 25 / 50 bps, on the IS window (the window the chooser actually reads) and on the full
  sample.  A stale preference whose turnover share exceeds 1.0 is a preference bought entirely
  with saved cost; one below 0 means the stale cadence ALSO wins on gross return.
  ARM B (THE BUDGET BOOK).  `bt_budget` refreshes the scalar on ANY day it has moved (i.e. the
  R = D trigger) but executes the refresh only while trailing-252-day realised turnover plus the
  refresh's own cost stays within an annual budget `B` turns/yr.  Mandatory trade-cadence
  re-spreads always execute and are charged against the same budget.  `B = inf` reproduces
  `R = D` exactly (gate G4).  The question: does the budget reach the cells the stale calendar
  cadences reach, at the freshness the fresh cadence has?

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION.  Over the (panel, T, t, R in {W,M,Q}) cells where the STALE rung
      beats `R = D` on IS SHARPE at 10 bps, the TURNOVER TERM accounts for MORE THAN HALF of the
      gap in MORE THAN HALF of those cells.  Triggered -> the stale preference is a cost fact and
      a budget is the right fix.  Not triggered -> it is a gross-return fact and no budget can be.
  V2  REACHABILITY.  At 10 bps, over the 6 arms (panel x trade cadence), the BUDGET family's legal
      IS-only picks clear 4b FULL *and* OOS on STRICTLY MORE arms than the CALENDAR family's.
  V3  TURNOVER EFFICIENCY.  Pooled at 10 bps, a budget book beats the turnover-MATCHED point on
      its own arm's calendar ladder (linear interpolation of the ladder's OOS Sharpe at the budget
      book's realised turnover) in MORE THAN HALF of cells AND on the mean.
  V5  NOT-A-KNIFE-EDGE.  A reached 4b FULL+OOS cell also clears 4b at >= 1 neighbouring rung of
      BOTH tuned dials AND keeps its 4b verdict under ONE EXTRA DAY of execution lag.  A cell
      that fails V5 is PARK, never KEEP, however good its own numbers.
  V4  CAPITAL.  Any cell clearing 4b FULL *and* OOS that a legal IS-only chooser actually REACHES
      is a KEEP-4b candidate; path 4a is scored at every cell too.

DIALS.  EXACTLY TWO are tuned, and only ever within one family: the BUDGET family spends TARGET
`t` and BUDGET `B`; the CALENDAR family spends TARGET `t` and REFRESH `R`.  No chooser selects
across families, panels, trade cadence or cost.  REPORTED, NOT TUNED: TRADE cadence `T in {W,M}`
(separate arms), PANEL {U56, B136, SMALL}, COST {0,10,25,50} bps, and the two pre-registered
legal IS-only choosers (IS_SHARPE, IS_LEGS).  The sigma convention is FIXED at the standing
memo's (L=20, d=0).  Every grid point is published (`.grid.csv`).

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The BUDGET-vs-CALENDAR contrast is same-tape / same-names / same-grid with only the refresh
TRIGGER moved, so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-22_stale-refresh-as-turnover-budget_cloud.py
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

DATE, SLUG = "2026-09-22", "stale-refresh-as-turnover-budget"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]                       # calendar family
BUDGETS = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]             # the tuned budget ladder (turns/yr)
B_INF = 1e9                                          # gate cell only, not a dial
TRADES = ["W", "M"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0
WIN = 252                                            # budget accounting window (trading days)

# committed numbers this run must reproduce (standing VOLTGT memo, points 2-4)
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
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
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio through
    close t-d.  (L,d) = (20,0) is the standing memo's convention."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------ the two refresh runners
def bt_cal(px_ret, W0, g0, mT, mR):
    """CALENDAR refresh (idea 1767's two-schedule construction).  T == R reproduces the standard
    single-schedule book exactly (gate G1)."""
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


def bt_budget(px_ret, W0, g0, mT, B):
    """TURNOVER-BUDGETED refresh.  The refresh TRIGGER is R = D (the scalar is re-read whenever it
    has moved), but a refresh executes only while the trailing-`WIN`-day realised turnover plus
    the refresh's own cost stays within the annual budget `B` (turns/yr).  Mandatory trade-cadence
    re-spreads always execute and are charged against the same budget.  `B = inf` reproduces
    `R = D` exactly (gate G4)."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    spent = 0.0                                    # trailing-window turnover already committed
    for i in range(n):
        if i >= WIN:
            spent -= turn[i - WIN]
        if i == 0:
            g_eff = g0[i]
            nref += 1
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            spent += turn[i]
            cur = new
        else:
            if mT[i]:
                new = W0[i] * g0[i]                # trade day: re-spread AND take the fresh scalar
                c_ref = np.abs(new - cur).sum()
                if spent + c_ref <= B:
                    g_eff = g0[i]
                else:                              # cannot afford freshness: hold the old scalar
                    new = W0[i] * g_eff
                    c_ref = np.abs(new - cur).sum()
                turn[i] = c_ref
                spent += c_ref
                cur = new
            elif abs(g0[i] - cur.sum()) > 0.0:     # R = D trigger, off a trade day
                s = cur.sum()
                if s > 0:
                    new = cur * (g0[i] / s)
                    c_ref = np.abs(new - cur).sum()
                    if spent + c_ref <= B:
                        g_eff = g0[i]
                        turn[i] = c_ref
                        spent += c_ref
                        cur = new
                        nref += 1
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


class Book:
    def __init__(self, px, cols, index, delay=1):
        """`delay` is the execution lag in days.  delay=1 is PROTOCOL rule 2 (decided at close t,
        applied at t+1).  delay=2 is the stress arm's ONE EXTRA DAY of slippage."""
        self.index = index
        self.delay = delay
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((delay, ew.shape[1])), ew[:-delay]])   # decided t, applied t+delay
        self.SIG = panel_sigma(px, cols)
        self.masks = {}
        for f in ("D", "W", "M", "Q"):
            m = np.asarray(rebalance_mask(index, f).values, bool)
            self.masks[f] = np.concatenate([[False], m[:-1]])

    def g_of(self, tgt):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([np.zeros(self.delay), g[:-self.delay]])

    def run_cal(self, g0, T, R):
        r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[R])
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)

    def run_budget(self, g0, T, B):
        r, t, gs, nref = bt_budget(self.R, self.W, g0, self.masks[T], B)
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


def w_bud(w):
    """The BUDGET ladder value a walk-forward row landed on (inf cells carry B_INF)."""
    return B_INF if w.cell == "B=inf" else float(w.cell.split("=")[1])


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 1795 (lane cloud, {DATE}) — is the STALE-REFRESH PREFERENCE a TURNOVER-BUDGET "
        f"fact in disguise?")
    log(f"# tuned dials (2, within a family): TARGET t {TARGETS} x [ BUDGET B {BUDGETS} turns/yr "
        f"| CALENDAR R {REFRESH} ].  reported, not tuned: TRADE T {TRADES} (separate arms), "
        f"PANEL, COST {COSTS} bps, choosers (IS_SHARPE, IS_LEGS).  sigma FIXED at (L={SIG_L}, "
        f"d={SIG_D}); budget window {WIN}d.  warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows = []
    BASE = {}
    PXS = {}
    g1r = g1t = g2 = g3 = g4 = 0.0
    g9 = 0.0
    g4n = 0

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        PXS[pname] = (px, cols, st)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")

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
        LV, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {LV['full']['CAGR']:.2%} / "
            f"{LV['full']['Sharpe']:.4f} / {LV['full']['MaxDD']:.2%}  (OOS "
            f"{LV['oos']['CAGR']:.2%} / {LV['oos']['Sharpe']:.4f} / {LV['oos']['MaxDD']:.2%}), "
            f"{LV['turn']:.2f} turns/yr")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        # ---- G1 / G2: the calendar diagonal is engine.backtest -------------------------
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

        # ---- the grid -----------------------------------------------------------------
        for tgt in TARGETS:
            g0 = bk.g_of(tgt)
            for T in TRADES:
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [("BUDGET", "B", b) for b in BUDGETS + [B_INF]])
                cal_D = None
                for fam, Rc, bval in cells:
                    if fam == "CAL":
                        r0, t0, gs, nref = bk.run_cal(g0, T, Rc)
                        label = f"R={Rc}"
                        if Rc == "D":
                            cal_D = (r0.copy(), t0.copy())
                    else:
                        r0, t0, gs, nref = bk.run_budget(g0, T, bval)
                        label = ("B=inf" if bval >= B_INF else f"B={bval:.1f}")
                        if bval >= B_INF and cal_D is not None:
                            cr, ct = cal_D
                            g4 = max(g4, float(np.abs(r0.values - cr.values).max()),
                                     float(np.abs(t0.values - ct.values).max()))
                            g4n += 1
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    g9 = max(g9, float(gs.max()))
                    yrs = len(r0) / 252.0
                    is_r0, is_t0 = r0.loc[:IS_END], t0.loc[:IS_END]
                    is_yrs = len(is_r0) / 252.0
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
                        LVc = B[f"live{c}"]
                        k4bf = (h1 > S["h1"] and h2 > S["h2"]
                                and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                        k4a = (h1 > LVc["h1"] and h2 > LVc["h2"]
                               and mf["MaxDD"] >= LVc["full"]["MaxDD"])
                        k4ao = (mo["Sharpe"] > LVc["oos"]["Sharpe"]
                                and mo["MaxDD"] >= LVc["oos"]["MaxDD"])
                        is_legs = int(ih1 > S["ish1"]) + int(ih2 > S["ish2"]) \
                            + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"]) \
                            + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"])
                        rows.append(dict(
                            panel=pname, target=tgt, T_trade=T, family=fam, R_refresh=Rc,
                            budget=bval, cell=label, cost=c,
                            turn_py=float(t0.sum() / yrs),
                            is_turn_py=float(is_t0.sum() / is_yrs),
                            gross_ret_full=float(r0.mean() * 252.0),
                            gross_ret_is=float(is_r0.mean() * 252.0),
                            refresh_py=nref / (len(px) / 252.0),
                            gross_mean=float(gs.mean()), gross_max=float(gs.max()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            is_H1=ih1, is_H2=ih2, is_legs=is_legs,
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            bind=bl, n_fail=nbad,
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a, keep4a_oos=k4ao))
        log(f"   grid done ({len([r for r in rows if r['panel'] == pname])} scored rows)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # -------------------------------------------------------------------- gates
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
    gate(f"G4 BUDGET B=inf == CALENDAR R=D, cell by cell ({g4n} cells)",
         f"{g4:.3e}", "< 1e-12", g4 < 1e-12 and g4n == len(TARGETS) * len(TRADES) * len(PS))
    gate("G5 gross never exceeds 1.00 (no leverage)", f"{g9:.6f}", "<= 1.0", g9 <= 1.0 + 1e-9)

    # ----------------------------------------------------- ARM A: the decomposition
    log("\n## ARM A — DECOMPOSITION OF EVERY CALENDAR `R` GAP (stale rung minus R=D)")
    dec = []
    g0c = G[G.cost == 0].set_index(["panel", "target", "T_trade", "family", "R_refresh",
                                    "budget"], drop=False)
    for (pn, tgt, T), sub in G[(G.family == "CAL") & (G.cost == COST0)].groupby(
            ["panel", "target", "T_trade"]):
        d = sub.set_index("R_refresh")
        if "D" not in d.index:
            continue
        for Rc in ["W", "M", "Q"]:
            if Rc not in d.index:
                continue
            for c in [10, 25, 50]:
                s = G[(G.panel == pn) & (G.target == tgt) & (G.T_trade == T)
                      & (G.family == "CAL") & (G.cost == c)].set_index("R_refresh")
                for win, sk, gk, tk in [("IS", "is_Sharpe", "gross_ret_is", "is_turn_py"),
                                        ("FULL", "Sharpe", "gross_ret_full", "turn_py")]:
                    d_net_sharpe = s.loc[Rc, sk] - s.loc["D", sk]
                    d_gross = s.loc[Rc, gk] - s.loc["D", gk]        # arithmetic ann. gross return
                    d_turn = s.loc[Rc, tk] - s.loc["D", tk]
                    cost_term = -(c / 1e4) * d_turn                  # the stale rung's cost SAVING
                    d_net_ret = d_gross + cost_term
                    dec.append(dict(panel=pn, target=tgt, T_trade=T, R=Rc, cost=c, window=win,
                                    d_net_sharpe=d_net_sharpe, d_gross_ret=d_gross,
                                    d_turn_py=d_turn, cost_term=cost_term, d_net_ret=d_net_ret,
                                    turn_share=(cost_term / d_net_ret
                                                if abs(d_net_ret) > 1e-12 else np.nan),
                                    stale_wins_sharpe=bool(d_net_sharpe > 0),
                                    stale_wins_gross=bool(d_gross > 0)))
    D = pd.DataFrame(dec)
    D.to_csv(f"{OUT}.decomp.csv", index=False)

    sel = D[(D.cost == COST0) & (D.window == "IS") & D.stale_wins_sharpe]
    n_sel = len(sel)
    n_cost = int((sel.turn_share > 0.5).sum())
    n_gross_too = int(sel.stale_wins_gross.sum())
    v1 = (n_sel > 0) and (n_cost > n_sel / 2)
    log(f"   IS window @ {COST0} bps: the stale rung beats R=D on IS Sharpe at {n_sel} of "
        f"{len(D[(D.cost == COST0) & (D.window == 'IS')])} (panel x t x T x R) cells.")
    log(f"   of those {n_sel}: turnover term > 50% of the net-return gap at {n_cost} "
        f"({n_cost/max(n_sel,1):.1%}); the stale rung ALSO wins on GROSS return at "
        f"{n_gross_too} ({n_gross_too/max(n_sel,1):.1%}).")
    if n_sel:
        log(f"   turnover share of the gap: median {sel.turn_share.median():.3f}, "
            f"mean {sel.turn_share.mean():.3f}, "
            f"IQR [{sel.turn_share.quantile(.25):.3f}, {sel.turn_share.quantile(.75):.3f}]")
        log(f"   mean d_turnover (stale - D) = {sel.d_turn_py.mean():.3f} turns/yr; "
            f"mean cost saving = {sel.cost_term.mean()*1e4:.1f} bp/yr; "
            f"mean d_gross = {sel.d_gross_ret.mean()*1e4:.1f} bp/yr")
    log(f"   V1 (stale preference is a COST fact): {'TRIGGERED' if v1 else 'NOT TRIGGERED'}")
    for c in (25, 50):
        s2 = D[(D.cost == c) & (D.window == "IS") & D.stale_wins_sharpe]
        log(f"   [reported, not tuned] at {c} bps: {len(s2)} stale-wins cells, "
            f"turnover share > 0.5 at {int((s2.turn_share > 0.5).sum())}")

    # ----------------------------------------------------- ARM B: reachability (rule 8)
    log("\n## ARM B — RULE-8 WALK-FORWARD: legal IS-ONLY choosers, 2017-2026 read once")
    wf = []
    for (pn, T, fam), sub in G[G.cost == COST0].groupby(["panel", "T_trade", "family"]):
        for ch in ("IS_SHARPE", "IS_LEGS"):
            if ch == "IS_SHARPE":
                pick = sub.sort_values(["is_Sharpe"], ascending=False).iloc[0]
            else:
                pick = sub.sort_values(["is_legs", "is_Sharpe"], ascending=False).iloc[0]
            b = BASE[pn]
            wf.append(dict(panel=pn, T_trade=T, family=fam, chooser=ch, cell=pick.cell,
                           target=pick.target, turn_py=pick.turn_py,
                           refresh_py=pick.refresh_py,
                           is_Sharpe=pick.is_Sharpe, is_legs=pick.is_legs,
                           CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                           oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                           oos_MaxDD=pick.oos_MaxDD,
                           spy_oos_CAGR=b["spy"]["oos"]["CAGR"],
                           spy_oos_Sharpe=b["spy"]["oos"]["Sharpe"],
                           spy_oos_MaxDD=b["spy"]["oos"]["MaxDD"],
                           live_oos_CAGR=b[f"live{COST0}"]["oos"]["CAGR"],
                           live_oos_Sharpe=b[f"live{COST0}"]["oos"]["Sharpe"],
                           live_oos_MaxDD=b[f"live{COST0}"]["oos"]["MaxDD"],
                           keep4b_full=pick.keep4b_full, keep4b_oos=pick.keep4b_oos,
                           keep4b=pick.keep4b, keep4a=pick.keep4a, keep4a_oos=pick.keep4a_oos,
                           bind=pick.bind))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for _, r in W.sort_values(["panel", "T_trade", "chooser", "family"]).iterrows():
        log(f"   {r.panel:<10} T={r.T_trade} {r.chooser:<9} {r.family:<6} pick {r.cell:<7} "
            f"t={r.target:.2f}  IS S={r.is_Sharpe:.4f} legs={r.is_legs}  ->  OOS "
            f"{r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / {r.oos_MaxDD:7.2%}  "
            f"(SPY {r.spy_oos_CAGR:.2%}/{r.spy_oos_Sharpe:.4f}/{r.spy_oos_MaxDD:.2%}; "
            f"RULESv2 {r.live_oos_CAGR:.2%}/{r.live_oos_Sharpe:.4f}/{r.live_oos_MaxDD:.2%})  "
            f"4b_full={int(r.keep4b_full)} 4b_oos={int(r.keep4b_oos)} 4a={int(r.keep4a)} "
            f"bind={r.bind}  {r.turn_py:.2f} turns/yr, {r.refresh_py:.0f} refresh/yr")
    arm_bud = W[(W.family == "BUDGET") & W.keep4b].groupby(["panel", "T_trade"]).ngroups
    arm_cal = W[(W.family == "CAL") & W.keep4b].groupby(["panel", "T_trade"]).ngroups
    v2 = arm_bud > arm_cal
    log(f"   V2 REACHABILITY: BUDGET picks clear 4b FULL+OOS on {arm_bud} of 6 arms, CALENDAR on "
        f"{arm_cal} of 6  ->  {'TRIGGERED' if v2 else 'NOT TRIGGERED'}")

    # ----------------------------------------------------- V3: turnover-matched comparison
    log("\n## V3 — BUDGET BOOKS AGAINST THE TURNOVER-MATCHED POINT ON THEIR OWN CALENDAR LADDER")
    mm = []
    for (pn, tgt, T), sub in G[G.cost == COST0].groupby(["panel", "target", "T_trade"]):
        cal = sub[sub.family == "CAL"].sort_values("turn_py")
        xs, ys = cal.turn_py.values, cal.oos_Sharpe.values
        for _, r in sub[(sub.family == "BUDGET") & (sub.budget < B_INF)].iterrows():
            if r.turn_py < xs.min() or r.turn_py > xs.max():
                matched = np.nan
            else:
                matched = float(np.interp(r.turn_py, xs, ys))
            mm.append(dict(panel=pn, target=tgt, T_trade=T, cell=r.cell, turn_py=r.turn_py,
                           oos_Sharpe=r.oos_Sharpe, matched=matched,
                           lift=r.oos_Sharpe - matched))
    M = pd.DataFrame(mm)
    M.to_csv(f"{OUT}.matched.csv", index=False)
    Mv = M.dropna(subset=["lift"])
    v3 = len(Mv) > 0 and (Mv.lift > 0).mean() > 0.5 and Mv.lift.mean() > 0
    log(f"   {len(Mv)} of {len(M)} budget cells fall inside their ladder's turnover range; "
        f"lift > 0 at {(Mv.lift > 0).sum()} ({(Mv.lift > 0).mean():.1%}), "
        f"mean lift {Mv.lift.mean():+.4f}, median {Mv.lift.median():+.4f}")
    log(f"   V3: {'TRIGGERED' if v3 else 'NOT TRIGGERED'}")

    # ----------------------------------------------------- V4: capital
    log("\n## V4 — CAPITAL")
    k = G[(G.cost == COST0) & G.keep4b]
    log(f"   cells clearing 4b FULL+OOS at {COST0} bps: {len(k)} of "
        f"{len(G[G.cost == COST0])}  (BUDGET {int((k.family == 'BUDGET').sum())}, "
        f"CAL {int((k.family == 'CAL').sum())})")
    reached = W[W.keep4b]
    log(f"   cells a legal IS-only chooser REACHES and that clear 4b FULL+OOS: {len(reached)}")
    for _, r in reached.iterrows():
        log(f"     -> {r.panel} T={r.T_trade} {r.family} {r.cell} t={r.target:.2f} ({r.chooser})")
    k4a = G[(G.cost == COST0) & G.keep4a]
    log(f"   cells clearing 4a (vs live RULES v2) at {COST0} bps: {len(k4a)}")
    v4 = len(reached) > 0


    # ----------------------------------------------------- STRESS: execution lag + dial neighbours
    log("\n## STRESS S1 — ONE EXTRA DAY OF EXECUTION LAG (decided t, applied t+2), whole grid")
    srows = []
    for pname, (px, cols, st) in PXS.items():
        bkd = Book(px, cols, px.index, delay=2)
        S = BASE[pname]["spy"]
        LVd = BASE[pname][f"live{COST0}"]
        for tgt in TARGETS:
            g0 = bkd.g_of(tgt)
            for T in TRADES:
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [("BUDGET", "B", b) for b in BUDGETS + [B_INF]])
                for fam, Rc, bval in cells:
                    if fam == "CAL":
                        r0, t0, gs, nref = bkd.run_cal(g0, T, Rc)
                        label = f"R={Rc}"
                    else:
                        r0, t0, gs, nref = bkd.run_budget(g0, T, bval)
                        label = ("B=inf" if bval >= B_INF else f"B={bval:.1f}")
                    r0, t0 = r0.loc[st:], t0.loc[st:]
                    r = net(r0, t0, COST0)
                    mf, mo = mets(r), mets(r.loc[OOS_START:])
                    h1, h2 = halves(r)
                    k4bf = (h1 > S["h1"] and h2 > S["h2"]
                            and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                            and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                    k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                            and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                            and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                    k4a = (h1 > LVd["h1"] and h2 > LVd["h2"]
                           and mf["MaxDD"] >= LVd["full"]["MaxDD"])
                    srows.append(dict(panel=pname, target=tgt, T_trade=T, family=fam,
                                      R_refresh=Rc, budget=bval, cell=label, cost=COST0,
                                      CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                      H1=h1, H2=h2, oos_CAGR=mo["CAGR"],
                                      oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                      turn_py=float(t0.sum() / (len(r0) / 252.0)),
                                      keep4b_full=k4bf, keep4b_oos=k4bo,
                                      keep4b=(k4bf and k4bo), keep4a=k4a))
    SS = pd.DataFrame(srows)
    SS.to_csv(f"{OUT}.stress_delay.csv", index=False)
    key = ["panel", "target", "T_trade", "family", "R_refresh", "budget"]
    j = (G[G.cost == COST0].set_index(key)[["keep4b"]]
         .join(SS.set_index(key)[["keep4b"]], rsuffix="_d", how="inner"))
    log(f"   4b FULL+OOS cells at 10 bps: {int(j.keep4b.sum())} at t+1, "
        f"{int(j.keep4b_d.sum())} at t+2; survive the extra day: "
        f"{int((j.keep4b & j.keep4b_d).sum())} of {int(j.keep4b.sum())}")

    log("\n## STRESS S2 — DIAL-NEIGHBOUR ROBUSTNESS OF EVERY REACHED 4b CELL")
    nb = []
    for _, w in W[W.keep4b].iterrows():
        sub = G[(G.panel == w.panel) & (G.T_trade == w.T_trade)
                & (G.family == w.family) & (G.cost == COST0)]
        if w.family == "BUDGET":
            ladder = BUDGETS + [B_INF]
            i = ladder.index(w_bud(w))
            neigh_b = [ladder[k] for k in (i - 1, i + 1) if 0 <= k < len(ladder)]
            nrows = sub[(sub.target == w.target) & sub.budget.isin(neigh_b)]
        else:
            i = REFRESH.index(w.cell.split("=")[1])
            neigh_r = [REFRESH[k] for k in (i - 1, i + 1) if 0 <= k < len(REFRESH)]
            nrows = sub[(sub.target == w.target) & sub.R_refresh.isin(neigh_r)]
        it = TARGETS.index(w.target)
        neigh_t = [TARGETS[k] for k in (it - 1, it + 1) if 0 <= k < len(TARGETS)]
        if w.family == "BUDGET":
            trows = sub[(sub.budget == w_bud(w)) & sub.target.isin(neigh_t)]
        else:
            trows = sub[(sub.R_refresh == w.cell.split("=")[1]) & sub.target.isin(neigh_t)]
        dsur = SS[(SS.panel == w.panel) & (SS.T_trade == w.T_trade) & (SS.cell == w.cell)
                  & (SS.target == w.target)]
        nb.append(dict(panel=w.panel, T_trade=w.T_trade, family=w.family, cell=w.cell,
                       target=w.target, chooser=w.chooser,
                       n_dial1_neighbours=len(nrows), dial1_4b=int(nrows.keep4b.sum()),
                       n_target_neighbours=len(trows), target_4b=int(trows.keep4b.sum()),
                       survives_t2=bool(dsur.keep4b.iloc[0]) if len(dsur) else None))
        log(f"   {w.panel:<10} T={w.T_trade} {w.family:<6} {w.cell:<7} t={w.target:.2f} "
            f"({w.chooser}): 4b holds at {nb[-1]['dial1_4b']}/{nb[-1]['n_dial1_neighbours']} "
            f"neighbouring rungs of dial 1 and {nb[-1]['target_4b']}/"
            f"{nb[-1]['n_target_neighbours']} neighbouring targets; survives t+2: "
            f"{nb[-1]['survives_t2']}")
    NB = pd.DataFrame(nb)
    NB.to_csv(f"{OUT}.neighbours.csv", index=False)
    v5 = bool(len(NB) and ((NB.dial1_4b > 0) & (NB.target_4b > 0) & NB.survives_t2).any())
    log(f"   V5 (a reached 4b cell that is NOT a knife edge: 4b also holds at >=1 neighbour of "
        f"BOTH dials AND survives t+2): {'TRIGGERED' if v5 else 'NOT TRIGGERED'}")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log("\n## VERDICTS")
    log(f"   V1 stale preference is a COST fact ............ {'YES' if v1 else 'NO'}")
    log(f"   V2 budget reaches more 4b arms than calendar ... {'YES' if v2 else 'NO'}")
    log(f"   V3 budget beats turnover-matched calendar ...... {'YES' if v3 else 'NO'}")
    log(f"   V4 a reached 4b FULL+OOS cell exists ........... {'YES' if v4 else 'NO'}")
    log(f"   V5 a reached 4b cell that is not a knife edge .. {'YES' if v5 else 'NO'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
