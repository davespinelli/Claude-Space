#!/usr/bin/env python3
"""Idea 2056 (lane cloud, 2026-09-21) — CAN THE DRIFT THRESHOLD `h` BE REMOVED ENTIRELY FROM THE
STANDING KEEP-4b CELL?  I.E. DOES A PLAIN CALENDAR REFRESH CLEAR 4b AT THE SAME TARGET?

THE QUESTION.  The standing KEEP-4b candidate (memo
`research/backtests/2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`) carries TWO tuned dials: the vol
target `t = 0.10` and a DRIFT REFRESH THRESHOLD `h = 0.08` (memo clause 5).  Two findings put `h`
under suspicion: idea 2050's rule-8 chooser keeps `t = 0.10` at 57 of 60 deleted draws but lands on
`h = 0.08` at only 17 of 60, and idea 2022 showed the drift trigger's whole matched edge over the
calendar ladder is ONE 24-day episode (+0.0596 -> +0.0066 once excised).  This run asks the VERDICT
question rather than the contrast question idea 1799 already answered: if a plain CALENDAR refresh
clears 4b at the same target, memo clause 5 is REMOVABLE MACHINERY and the book drops a dial.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  REFRESH RULE  {DRIFT h=0.08 (the incumbent), D, W, M, Q}     -- when the gross scalar is re-read
    P2  TARGET        {0.08, 0.10, 0.12, 0.16, 0.20, MEDMULT_1.00}   -- what the gross scalar aims at

`MEDMULT_1.00` is the ZERO-IS target this lane's idea 2071 established earlier today (`t_t` = the
EXPANDING point-in-time MEDIAN of the panel's own 20-day realised sigma; it reads no 2009-2016
statistic and was pre-stated there before compute).  It is a RUNG OF THE TARGET AXIS, not a third
dial: if it clears 4b under a CALENDAR refresh, the resulting rule has NO tuned dial anywhere.

REPORTED, NOT TUNED: panel {B136, U56, SMALL665}, cost {0, 10, 25, 50} bps, window {FULL, IS, OOS}.
INHERITED AND NOT TOUCHED: trade cadence W, t+1 execution, gross cap 1.00, sigma convention (20-day
realised vol of the unlevered equal-weight panel portfolio, no lag), warm-up 260.

THE REFRESH / TRADE DISTINCTION (stated because it is the whole mechanism).  The book has two
clocks.  NAME weights are rebalanced to `G / N` on the WEEKLY trade date, always.  The GROSS SCALAR
`G` is re-read on the REFRESH clock: under DRIFT when `|g_t - deployed gross| > h`, under a CALENDAR
rule on the last trading day of each D/W/M/Q period.  On a refresh that is not a trade day the book
rescales existing holdings PRO RATA and trades nothing else.  Setting the refresh clock to W makes
the two clocks identical — that is the "one-clock" book the idea asks about.

PROTOCOL: rule 2 (10 bps headline, t+1, gross <= 1.00, no shorting/leverage); rule 3 (live RULES v2
AND SPY); rule 4 (BOTH KEEP paths at every cell, <= 2 tuned parameters, ALL grid points reported);
rule 5 (one idea, one script, deterministic, standalone); rule 8 (walk-forward: BOTH dials chosen on
2009-2016 only, 2017-2026 read exactly once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified by this run.

SURVIVORSHIP.  B136 and U56 are CURRENT-constituent lists; SMALL665 is a current sub-$2B screen with
tickers whose `max_1d_move >= 1.0` in `data/small_meta.csv` dropped first.  Every CAGR / MaxDD LEVEL
is optimistic and both 4b bars are EASIER than on a point-in-time panel.  The REFRESH-RULE CONTRAST
is a same-tape, same-names comparison and is first-order immune to that; the pass LEVELS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-21_calendar-vs-drift-refresh-removal_cloud.py
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

DATE, SLUG, LANE = "2026-09-21", "calendar-vs-drift-refresh-removal", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

# ---------------------------------------------------------------- inherited, NOT tuned
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SIG_L, SIG_D = 20, 0
SELF_MINP = 126
H_INC = 0.08                      # the incumbent drift threshold
T_TRADE = "W"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST0 = 10
COSTS = [0, 10, 25, 50]
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

# ---------------------------------------------------------------- the two tuned parameters
REFRESH = ["DRIFT", "D", "W", "M", "Q"]                      # DRIFT = the incumbent, h = 0.08
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20, "MEDMULT_1.00"]     # last rung reads NO IS window
CELL = ("DRIFT", 0.10)                                       # the standing KEEP-4b cell

PUB = dict(CAGR=0.1251, Sharpe=1.2286, MaxDD=-0.1181, H1=1.3171, H2=1.1415,
           oCAGR=0.1301, oSharpe=1.2928, spy_CAGR=0.1512, spy_Sharpe=0.8844, spy_MaxDD=-0.3372,
           # idea 2071, same lane, earlier today: MEDMULT m=1.00 + DRIFT h=0.08 on B136 @10bps
           med_CAGR=0.1598, med_Sharpe=1.2464, med_MaxDD=-0.1679)

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


# ---------------------------------------------------------------- book machinery
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


def bt_book(px_ret, W0, g0, mT, mode, h=H_INC, mR=None):
    """One book.  NAME weights trade on mT (weekly, always).  The GROSS SCALAR is re-read when the
    REFRESH clock fires: DRIFT -> |g_t - deployed| > h; calendar -> mR[i].  Identical to idea
    1799/2034's loop except for the trigger expression."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        trig = (abs(g0[i] - cur.sum()) > h) if mode == "DRIFT" else bool(mR[i])
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
    def __init__(self, px, cols):
        self.index = px.index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])
        self.SIG = panel_sigma(px, cols)
        m = np.asarray(rebalance_mask(px.index, T_TRADE).values, bool)
        self.mT = np.concatenate([[False], m[:-1]])
        self.mR = {}
        for R in ("D", "W", "M", "Q"):
            mm = np.asarray(rebalance_mask(px.index, R).values, bool)
            self.mR[R] = np.concatenate([[False], mm[:-1]])

    def g_of(self, target):
        sig = self.SIG
        if isinstance(target, str) and target.startswith("MEDMULT"):
            mult = float(target.split("_")[1])
            tgt = mult * sig.expanding(min_periods=SELF_MINP).median()
        else:
            tgt = pd.Series(float(target), index=sig.index).where(sig.notna())
        g = (tgt / sig.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])        # decided at close t, applied at t+1

    def run(self, refresh, target):
        g0 = self.g_of(target)
        mode = "DRIFT" if refresh == "DRIFT" else "CAL"
        mR = None if refresh == "DRIFT" else self.mR[refresh]
        r, t, gs, nref = bt_book(self.R, self.W, g0, self.mT, mode, H_INC, mR)
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)


def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = pd.Series(r).dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1) if yrs else np.nan,
                Sharpe=float((r.mean() * 252.0) / vol) if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def legs_4b(rb, spy):
    mb, ms = mets(rb), mets(spy)
    bh1, bh2 = halves(rb)
    sh1, sh2 = halves(spy)
    ob, os_ = mets(rb.loc[OOS_START:]), mets(spy.loc[OOS_START:])
    return dict(L1_H1=bh1 - sh1, L2_H2=bh2 - sh2, L3_OOS=ob["Sharpe"] - os_["Sharpe"],
                L4_DD=mb["MaxDD"] - DD_CAP * ms["MaxDD"],
                L5_CAGR=mb["CAGR"] - CAGR_FLOOR * ms["CAGR"],
                CAGR=mb["CAGR"], Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"], H1=bh1, H2=bh2,
                oCAGR=ob["CAGR"], oSharpe=ob["Sharpe"], oMaxDD=ob["MaxDD"])


def verdict_4b(L):
    binding = [k for k in LEGS if not (L[k] > 0)]
    return (len(binding) == 0), (",".join(binding) if binding else "none")


def verdict_4a(rb, lb):
    bh1, bh2 = halves(rb)
    lh1, lh2 = halves(lb)
    mb, ml = mets(rb), mets(lb)
    fails = []
    if not bh1 > lh1: fails.append("H1")
    if not bh2 > lh2: fails.append("H2")
    if not mb["MaxDD"] >= ml["MaxDD"]: fails.append("MaxDD")
    return (len(fails) == 0), (",".join(fails) if fails else "none")


def small_panel():
    raw = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px = raw[[c for c in raw.columns if c not in bad]].dropna(how="all").ffill()
    return px, [c for c in px.columns if c != "SPY"], len(bad & set(raw.columns))


def tlabel(t):
    return t if isinstance(t, str) else f"{t:.2f}"


def main():
    log(f"# Idea 2056 (lane {LANE}, {DATE}) — CAN THE DRIFT THRESHOLD `h` BE REMOVED FROM THE "
        f"STANDING KEEP-4b CELL?")
    log(f"# BOOK (inherited, NOT tuned): equal-weight panel, gross scalar capped at 1.00, trade "
        f"{T_TRADE}, t+1, sigma (L={SIG_L}, d={SIG_D}), warm-up {WARMUP}.")
    log(f"# TUNED (2): REFRESH RULE {REFRESH} (DRIFT uses the incumbent h={H_INC}) x TARGET "
        f"{[tlabel(t) for t in TARGETS]}.  ALL {len(REFRESH)*len(TARGETS)} cells reported per panel.")
    log(f"# MEDMULT_1.00 is idea 2071's ZERO-IS target rung (expanding point-in-time median sigma), "
        f"a rung of the TARGET axis, not a third dial.")
    log(f"# REPORTED, not tuned: panel [B136, U56, SMALL665], cost {COSTS} bps, window [FULL, IS, OOS].")

    px136 = load_universe(broad=True).dropna(how="all").ffill()
    px56 = load_universe().dropna(how="all").ffill()
    pxs, cols_s, n_drop = small_panel()
    PANELS = [("B136", px136, list(px136.columns)),
              ("U56", px56, list(px56.columns)),
              (f"SMALL{len(cols_s)}", pxs, cols_s)]
    log(f"# SMALL panel: {n_drop} tickers with max_1d_move >= 1.0 dropped; {len(cols_s)} held names.")

    STATE = {}
    for pname, px, cols in PANELS:
        st = px.index[WARMUP]
        bk = Book(px, cols)
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        STATE[pname] = dict(px=px, cols=cols, bk=bk, st=st, spy=spy,
                            lr=lb["returns"].loc[st:], lt=lb["turnover"].loc[st:])
        ms, mo = mets(spy), mets(spy.loc[OOS_START:])
        lbn = net(STATE[pname]["lr"], STATE[pname]["lt"], COST0)
        ml = mets(lbn)
        log(f"\n## {pname}: {len(cols)} held names, {st.date()} -> {px.index[-1].date()} "
            f"({len(spy)} days, {len(spy)/252:.1f}y)")
        log(f"   SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%} -> bars: CAGR floor "
            f"{CAGR_FLOOR*ms['CAGR']:.2%}, DD cap {DD_CAP*ms['MaxDD']:.2%}; OOS SPY {mo['CAGR']:.2%} / {mo['Sharpe']:.4f}")
        log(f"   live RULES v2 {ml['CAGR']:.2%} / {ml['Sharpe']:.4f} / {ml['MaxDD']:.2%} halves "
            f"{halves(lbn)[0]:.4f} / {halves(lbn)[1]:.4f}")

    # ------------------------------------------------------------------ GATES
    log("\n## GATES (printed before any new number is read)")
    S = STATE["B136"]
    r0, t0, gs, nref = S["bk"].run(*CELL)
    rb = net(r0.loc[S["st"]:], t0.loc[S["st"]:], COST0)
    L = legs_4b(rb, S["spy"])
    ms = mets(S["spy"])
    g1 = max(abs(L["CAGR"] - PUB["CAGR"]), abs(L["Sharpe"] - PUB["Sharpe"]), abs(L["MaxDD"] - PUB["MaxDD"]))
    gate("G1 the standing cell (DRIFT h=0.08, t=0.10, B136) reproduces memo point 2",
         f"max|d| {g1:.2e}", "<= 5e-4", g1 <= 5e-4)
    g2 = max(abs(L["H1"] - PUB["H1"]), abs(L["H2"] - PUB["H2"]))
    gate("G2 halves reproduce (1.3171 / 1.1415)", f"max|d| {g2:.2e}", "<= 5e-4", g2 <= 5e-4)
    g3 = max(abs(L["oCAGR"] - PUB["oCAGR"]), abs(L["oSharpe"] - PUB["oSharpe"]))
    gate("G3 memo point 5 OOS reproduces (13.01% / 1.2928)", f"max|d| {g3:.2e}", "<= 5e-4", g3 <= 5e-4)
    g4 = max(abs(ms["CAGR"] - PUB["spy_CAGR"]), abs(ms["Sharpe"] - PUB["spy_Sharpe"]),
             abs(ms["MaxDD"] - PUB["spy_MaxDD"]))
    gate("G4 SPY comparand reproduces (15.12% / 0.8844 / -33.72%)", f"max|d| {g4:.2e}", "<= 5e-4", g4 <= 5e-4)
    rm, tm, _, _ = S["bk"].run("DRIFT", "MEDMULT_1.00")
    Lm = legs_4b(net(rm.loc[S["st"]:], tm.loc[S["st"]:], COST0), S["spy"])
    g5 = max(abs(Lm["CAGR"] - PUB["med_CAGR"]), abs(Lm["Sharpe"] - PUB["med_Sharpe"]),
             abs(Lm["MaxDD"] - PUB["med_MaxDD"]))
    gate("G5 idea 2071's zero-IS MEDMULT rung reproduces cross-run (15.98% / 1.2464 / -16.79%)",
         f"max|d| {g5:.2e}", "<= 5e-4", g5 <= 5e-4)
    # a CALENDAR refresh at W must coincide with the trade clock: one clock, so refreshes == trades
    rW, tW, gW, nW = S["bk"].run("W", 0.10)
    ntrade = int(S["bk"].mT.sum()) + 1
    gate("G6 refresh=W fires exactly on the weekly trade dates (one clock)",
         f"{nW} refreshes vs {ntrade} trade days", "equal", nW == ntrade)

    # ------------------------------------------------------------------ GRID
    log(f"\n## GRID — {len(PANELS)} panels x {len(REFRESH)} refresh rules x {len(TARGETS)} targets "
        f"x {len(COSTS)} cost rungs = {len(PANELS)*len(REFRESH)*len(TARGETS)*len(COSTS)} rows, all published.")
    rows, BOOKS = [], {}
    for pname, _, _ in PANELS:
        S = STATE[pname]
        for R in REFRESH:
            for T in TARGETS:
                r0, t0, gs, nref = S["bk"].run(R, T)
                r0, t0, gs = r0.loc[S["st"]:], t0.loc[S["st"]:], gs.loc[S["st"]:]
                BOOKS[(pname, R, T)] = (r0, t0)
                yrs = len(r0) / 252.0
                for c in COSTS:
                    rbk = net(r0, t0, c)
                    lbn = net(S["lr"], S["lt"], c)
                    Lg = legs_4b(rbk, S["spy"])
                    p4b, b4b = verdict_4b(Lg)
                    p4a, b4a = verdict_4a(rbk, lbn)
                    rows.append(dict(panel=pname, refresh=R, target=tlabel(T), cost_bps=c,
                                     zero_IS=isinstance(T, str), n_dials=(0 if isinstance(T, str) and R != "DRIFT"
                                                                          else (1 if isinstance(T, str) or R != "DRIFT" else 2)),
                                     CAGR=Lg["CAGR"], Sharpe=Lg["Sharpe"], MaxDD=Lg["MaxDD"],
                                     H1=Lg["H1"], H2=Lg["H2"], oCAGR=Lg["oCAGR"], oSharpe=Lg["oSharpe"],
                                     oMaxDD=Lg["oMaxDD"], **{k: Lg[k] for k in LEGS},
                                     keep4b=p4b, binding4b=b4b, keep4a=p4a, binding4a=b4a,
                                     turnover_yr=float(t0.sum() / yrs), refresh_yr=float(nref / yrs),
                                     mean_gross=float(gs.mean())))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    for pname, _, _ in PANELS:
        sub = G[(G.panel == pname) & (G.cost_bps == COST0)]
        log(f"\n### {pname} @ {COST0} bps, full sample — 4b verdict by (refresh x target)")
        log(f"{'refresh':<9}" + "".join(f"{tlabel(t):>14}" for t in TARGETS))
        for R in REFRESH:
            cells = []
            for T in TARGETS:
                r = sub[(sub.refresh == R) & (sub.target == tlabel(T))].iloc[0]
                cells.append(("PASS" if r.keep4b else "fail") + f"/{'4a' if r.keep4a else '--'}")
            log(f"{R:<9}" + "".join(f"{c:>14}" for c in cells))
        log(f"\n### {pname} @ {COST0} bps, full sample — CAGR / Sharpe / MaxDD / turnover per year")
        log(f"{'refresh':<9}{'target':>13}  {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOSShp':>7} {'trn/yr':>7} {'ref/yr':>7} {'gross':>6}  {'4b':>4} {'4a':>4}  binding4b")
        for R in REFRESH:
            for T in TARGETS:
                r = sub[(sub.refresh == R) & (sub.target == tlabel(T))].iloc[0]
                log(f"{R:<9}{r.target:>13}  {r.CAGR:>7.2%} {r.Sharpe:>7.4f} {r.MaxDD:>8.2%} "
                    f"{r.H1:>7.4f} {r.H2:>7.4f} {r.oSharpe:>7.4f} {r.turnover_yr:>7.2f} "
                    f"{r.refresh_yr:>7.1f} {r.mean_gross:>6.3f}  {'PASS' if r.keep4b else 'fail':>4} "
                    f"{'PASS' if r.keep4a else 'fail':>4}  {r.binding4b}")

    log("\n### 4b PASS COUNTS by refresh rule x cost (all panels x targets pooled; "
        f"{len(PANELS)*len(TARGETS)} cells per rule)")
    n = len(PANELS) * len(TARGETS)
    log(f"{'refresh':<9}" + "".join(f"{'4b@'+str(c):>10}" for c in COSTS)
        + "".join(f"{'4a@'+str(c):>10}" for c in COSTS) + f"{'mean turn/yr':>14}")
    for R in REFRESH:
        s = G[G.refresh == R]
        log(f"{R:<9}"
            + "".join(f"{str(int(s[s.cost_bps==c].keep4b.sum()))+'/'+str(n):>10}" for c in COSTS)
            + "".join(f"{str(int(s[s.cost_bps==c].keep4a.sum()))+'/'+str(n):>10}" for c in COSTS)
            + f"{s[s.cost_bps==COST0].turnover_yr.mean():>14.2f}")

    # ------------------------------------------------------------------ THE DIRECT COMPARISON
    log("\n## THE DIRECT QUESTION — at the SAME target, does the CALENDAR refresh clear 4b where "
        "the incumbent DRIFT trigger does?  (10 bps; dS = calendar Sharpe - DRIFT Sharpe)")
    cmp_rows = []
    for pname, _, _ in PANELS:
        for T in TARGETS:
            d = G[(G.panel == pname) & (G.refresh == "DRIFT") & (G.target == tlabel(T)) & (G.cost_bps == COST0)].iloc[0]
            for R in ("D", "W", "M", "Q"):
                c = G[(G.panel == pname) & (G.refresh == R) & (G.target == tlabel(T)) & (G.cost_bps == COST0)].iloc[0]
                cmp_rows.append(dict(panel=pname, target=tlabel(T), refresh=R,
                                     drift_4b=bool(d.keep4b), cal_4b=bool(c.keep4b),
                                     dSharpe=c.Sharpe - d.Sharpe, dCAGR=c.CAGR - d.CAGR,
                                     dMaxDD=c.MaxDD - d.MaxDD, dTurn=c.turnover_yr - d.turnover_yr,
                                     survives=bool(d.keep4b and c.keep4b),
                                     lost=bool(d.keep4b and not c.keep4b),
                                     gained=bool((not d.keep4b) and c.keep4b),
                                     cal_binding=c.binding4b))
    C = pd.DataFrame(cmp_rows)
    C.to_csv(f"{OUT}.calendar_vs_drift.csv", index=False)
    log(f"{'refresh':<9}{'drift-4b cells':>16}{'kept by cal':>13}{'lost':>7}{'gained':>8}"
        f"{'mean dSharpe':>14}{'mean dTurn':>12}")
    for R in ("D", "W", "M", "Q"):
        s = C[C.refresh == R]
        nd = int(s.drift_4b.sum())
        log(f"{R:<9}{nd:>16}{int(s.survives.sum()):>13}{int(s.lost.sum()):>7}"
            f"{int(s.gained.sum()):>8}{s.dSharpe.mean():>+14.4f}{s.dTurn.mean():>+12.2f}")
    log("\n  cell-by-cell where DRIFT passes 4b (10 bps):")
    for _, r in C[C.drift_4b].iterrows():
        log(f"    {r.panel:<9} target {r.target:<13} refresh {r.refresh:<2} -> "
            f"{'KEEPS 4b' if r.cal_4b else 'LOSES 4b (' + r.cal_binding + ')':<28} "
            f"dSharpe {r.dSharpe:+.4f}  dCAGR {r.dCAGR:+.2%}  dMaxDD {r.dMaxDD:+.2%}  dTurn {r.dTurn:+.2f}/yr")

    # ------------------------------------------------------------------ RULE 8
    log("\n## RULE 8 WALK-FORWARD — BOTH dials (refresh rule, target) chosen on 2009-2016 ONLY "
        "(argmax min IS 4b-leg slack), 2017-2026 read exactly ONCE.  Every grid point reported.")
    wf = []
    for pname, _, _ in PANELS:
        S = STATE[pname]
        spy_is, spy_oos = S["spy"].loc[:IS_END], S["spy"].loc[OOS_START:]
        sis, soos = mets(spy_is), mets(spy_oos)
        sis_h1, sis_h2 = halves(spy_is)
        soos_h1, soos_h2 = halves(spy_oos)
        lbn = net(S["lr"], S["lt"], COST0)
        lo = mets(lbn.loc[OOS_START:])
        lh1, lh2 = halves(lbn.loc[OOS_START:])
        for R in REFRESH:
            for T in TARGETS:
                r0, t0 = BOOKS[(pname, R, T)]
                rbk = net(r0, t0, COST0)
                ris, roos = rbk.loc[:IS_END], rbk.loc[OOS_START:]
                mi, mo = mets(ris), mets(roos)
                ih1, ih2 = halves(ris)
                oh1, oh2 = halves(roos)
                sl = dict(L1=ih1 - sis_h1, L2=ih2 - sis_h2,
                          L4=mi["MaxDD"] - DD_CAP * sis["MaxDD"],
                          L5=mi["CAGR"] - CAGR_FLOOR * sis["CAGR"])
                oos_4b = (oh1 > soos_h1 and oh2 > soos_h2 and mo["Sharpe"] > soos["Sharpe"]
                          and mo["MaxDD"] >= DD_CAP * soos["MaxDD"]
                          and mo["CAGR"] >= CAGR_FLOOR * soos["CAGR"])
                oos_4a = (oh1 > lh1 and oh2 > lh2 and mo["MaxDD"] >= lo["MaxDD"])
                wf.append(dict(panel=pname, refresh=R, target=tlabel(T),
                               is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                               is_minslack=min(sl.values()), **{f"is_{k}": v for k, v in sl.items()},
                               oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                               oos_L3=mo["Sharpe"] - soos["Sharpe"],
                               oos_L4=mo["MaxDD"] - DD_CAP * soos["MaxDD"],
                               oos_L5=mo["CAGR"] - CAGR_FLOOR * soos["CAGR"],
                               oos_keep4b=oos_4b, oos_keep4a=oos_4a))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pname, _, _ in PANELS:
        S = STATE[pname]
        soos = mets(S["spy"].loc[OOS_START:])
        lo = mets(net(S["lr"], S["lt"], COST0).loc[OOS_START:])
        sub = W[W.panel == pname]
        log(f"\n### {pname} — OOS 2017-2026 comparands: SPY {soos['CAGR']:.2%} / {soos['Sharpe']:.4f} "
            f"/ {soos['MaxDD']:.2%};  live RULES v2 {lo['CAGR']:.2%} / {lo['Sharpe']:.4f} / {lo['MaxDD']:.2%}")
        log(f"{'refresh':<9}{'target':>13} {'IS slack':>9}  {'OOS CAGR':>9} {'OOSShp':>7} {'OOS DD':>8} "
            f"{'4bOOS':>6} {'4aOOS':>6}")
        for _, r in sub.iterrows():
            log(f"{r.refresh:<9}{r.target:>13} {r.is_minslack:>+9.4f}  {r.oos_CAGR:>9.2%} "
                f"{r.oos_Sharpe:>7.4f} {r.oos_MaxDD:>8.2%} {'PASS' if r.oos_keep4b else 'fail':>6} "
                f"{'PASS' if r.oos_keep4a else 'fail':>6}")
        pick = sub.loc[sub.is_minslack.idxmax()]
        log(f"  -> IS PICK (both dials, 2009-2016 only): refresh={pick.refresh}, target={pick.target} "
            f"[min IS slack {pick.is_minslack:+.4f}];  OOS read ONCE {pick.oos_CAGR:.2%} / "
            f"{pick.oos_Sharpe:.4f} / {pick.oos_MaxDD:.2%}, 4b {'PASS' if pick.oos_keep4b else 'fail'}, "
            f"4a {'PASS' if pick.oos_keep4a else 'fail'}")
        cal = sub[sub.refresh != "DRIFT"]
        cpick = cal.loc[cal.is_minslack.idxmax()]
        log(f"  -> IS PICK RESTRICTED TO CALENDAR REFRESHES (h removed by construction): "
            f"refresh={cpick.refresh}, target={cpick.target}; OOS {cpick.oos_CAGR:.2%} / "
            f"{cpick.oos_Sharpe:.4f} / {cpick.oos_MaxDD:.2%}, 4b "
            f"{'PASS' if cpick.oos_keep4b else 'fail'}, 4a {'PASS' if cpick.oos_keep4a else 'fail'}")

    # ------------------------------------------------------------------ ZERO-DIAL CORNER
    log("\n## THE ZERO-DIAL CORNER — CALENDAR refresh x the ZERO-IS target: a book with NO tuned "
        "dial anywhere (no `t` off a ladder, no `h`, refresh clock = the trade clock).")
    log(f"{'panel':<10}{'refresh':<9}{'cost':>5}  {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} "
        f"{'OOS CAGR':>9} {'OOSShp':>7}  {'4b':>4} {'4a':>4}  binding4b")
    zrows = []
    for pname, _, _ in PANELS:
        for R in ("D", "W", "M", "Q"):
            for c in COSTS:
                r = G[(G.panel == pname) & (G.refresh == R) & (G.target == "MEDMULT_1.00")
                      & (G.cost_bps == c)].iloc[0]
                zrows.append(r)
                if c in (COST0, 50):
                    log(f"{pname:<10}{R:<9}{c:>5}  {r.CAGR:>7.2%} {r.Sharpe:>7.4f} {r.MaxDD:>8.2%} "
                        f"{r.oCAGR:>9.2%} {r.oSharpe:>7.4f}  {'PASS' if r.keep4b else 'fail':>4} "
                        f"{'PASS' if r.keep4a else 'fail':>4}  {r.binding4b}")
    Z = pd.DataFrame(zrows)
    Z.to_csv(f"{OUT}.zerodial.csv", index=False)
    zl = Z[Z.panel != "SMALL665"] if "SMALL665" in set(Z.panel) else Z[~Z.panel.str.startswith("SMALL")]
    log(f"  zero-dial 4b pass: {int(Z.keep4b.sum())} of {len(Z)} across all panels and cost rungs; "
        f"{int(zl.keep4b.sum())} of {len(zl)} on the two large panels.")

    # ------------------------------------------------------------------ SUMMARY
    log("\n## SUMMARY")
    d10 = G[(G.cost_bps == COST0)]
    log(f"  full-sample 4b @ {COST0} bps: {int(d10.keep4b.sum())} of {len(d10)} cells; "
        f"4a: {int(d10.keep4a.sum())} of {len(d10)}")
    for R in REFRESH:
        s = d10[d10.refresh == R]
        log(f"    refresh {R:<6} 4b {int(s.keep4b.sum())}/{len(s)}  4a {int(s.keep4a.sum())}/{len(s)}  "
            f"mean Sharpe {s.Sharpe.mean():.4f}  mean turnover {s.turnover_yr.mean():.2f}/yr")
    lost = C[C.lost]
    log(f"  cells where DRIFT passes 4b and the CALENDAR refresh does NOT: {len(lost)} of "
        f"{int(C.drift_4b.sum())} (by binding leg: "
        + ", ".join(f"{k} x{v}" for k, v in lost.cal_binding.value_counts().items()) + ")")
    log(f"  cells where the CALENDAR refresh passes 4b and DRIFT does not: {int(C.gained.sum())}")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\nGATES {sum(g['pass_'] for g in _gates)}/{len(_gates)} passed.")
    log(f"wrote {OUT}.grid.csv / .calendar_vs_drift.csv / .walkforward.csv / .zerodial.csv / "
        f".gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
