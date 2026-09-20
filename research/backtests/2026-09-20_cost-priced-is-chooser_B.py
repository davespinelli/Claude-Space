#!/usr/bin/env python3
"""Idea 1803 (lane B, 2026-09-20) — CAN A COST-PRICED IS-ONLY CHOOSER REACH THE DAILY-REFRESH
CELLS THAT IDEA 1793 LEFT UNREACHABLE?

THE RESIDUE THIS PRICES.  Idea 1793 answered its own question (an exposure-neutral IS statistic,
`C_GXDD`, reaches 4b cells plain IS Sharpe cannot) and left ONE named residue:

    "The REFRESH half is still unreachable.  `R = D` clears 4b FULL+OOS at 4 of 4 arms for every
     `t >= 0.10` and no legal IS-only chooser ever picks it; the OOS oracle takes `t = 0.12,
     R = D` (U56 OOS 15.28% / 1.3485 / -15.79%)."

The record's standing explanations for the stale-refresh preference are (a) idea 1767's "IS Sharpe
rewards the lazier, higher-gross book" — which idea 1793 KILLED (a long-only constant-gross twin's
Sharpe is invariant in its gross) — and (b) idea 1789's "crash-presence": 2009-2016 contains no
crash, so freshness is worth ~0.0003 of Sharpe inside that window and the argmax falls to the
stale cell "on noise and saved turnover".  The second half of 1789's own sentence has never been
priced.  On U56 at `t = 0.08` a DAILY refresh trades **5.50 turns/yr** against a MONTHLY one's
**2.83**: at 10 bps that is **~267 bps/yr** of charged cost, on the order of the whole **0.158**
IS-Sharpe gap the chooser is reading.  So the refusal may be COST ACCOUNTING, not information —
and unlike a regime fact, a cost artefact is REMOVABLE.

THE TEST.  Exactly idea 1793's grid and runner (so its committed cells are a cross-run replication
gate), with one thing moved: the COST RUNG THE CHOOSER'S STATISTIC IS PRICED AT,
`c_IS in {0, 10, 25, 50}` bps, crossed against six statistic families (the four plain ones and
1793's two exposure-neutral ones).  The BOOK is always charged the real rung — every verdict,
every OOS number and every leaderboard row below is a book netted at 0 / 10 / 25 / 50 bps with
10 bps as the headline — so `c_IS` moves the RANKING only, never the P&L.  A `c_IS = 0` chooser
is legal under rule 8 (it reads 2009-2016 only) but it deliberately ignores a cost the book pays,
so V5 below prices that asymmetry instead of hiding it.

PRE-STATED VERDICT RULES (fixed before the run; no rule is added or relaxed afterwards):
  V1  THE IDEA'S OWN QUESTION.  Pooled over the 6 arms x 6 families, scoring at `c_IS = 0` lands
      the argmax on `R in {D, W}` on STRICTLY MORE cells than scoring at `c_IS = 10` does.
      Not triggered -> KILL the cost-accounting explanation of the stale-refresh preference.
  V2  REACH.  Some (family, `c_IS = 0`) chooser reaches a cell clearing 4b FULL *and* OOS at
      10 bps on STRICTLY MORE arms than the best `c_IS = 10` chooser (idea 1793's C_GXDD).
  V3  DECOMPOSITION.  The `R = M` minus `R = D` IS-Sharpe gap at 10 bps is MAJORITY COST: median
      over (arm x t) of [gap(10) - gap(0)] / gap(10) is >= 0.50 where gap(10) > 0.
  V4  CAPITAL.  Any cell a legal IS-only chooser actually REACHES that clears 4b FULL *and* OOS
      at 10 bps is a KEEP-4b candidate; path 4a is scored at every cell too.
  V5  THE COUNTERWEIGHT (stated in advance, not after).  A cheap-looking chooser that buys
      turnover the book then pays for is not a fix.  Every pick is published with its turnover
      and its 4b verdict at 0 / 10 / 25 / 50 bps; a pick that fails 4b at 25 bps is reported as
      COST-FRAGILE and cannot be a KEEP-candidate on the strength of a 10 bps pass alone.

DIALS.  EXACTLY TWO are tuned (spent by the chooser): TARGET `t` in {0.08,0.10,0.12,0.16,0.20}
and REFRESH cadence `R` in {D,W,M,Q} = 20 cells per arm.  REPORTED, NOT TUNED: the CHOOSER
(family x `c_IS`) is the AXIS UNDER TEST; TRADE cadence `T` in {W,M} (each (panel,T) is a separate
ARM; no chooser ever selects across T); PANEL {U56,B136,SMALL665}; BOOK COST {0,10,25,50} bps.
The sigma convention is FIXED at the standing memo's (L = 20, d = 0) — idea 1771 owns that
surface.  Every grid point is published to `.grid.csv`; every pick to `.choosers.csv`.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00);
rule 3 (RULES v2 live book AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea,
deterministic, standalone); rule 8 (2009-2016 chooses, 2017-2026 read exactly once); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and drawdown
LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.  The
CHOOSER contrast is same-tape / same-names / same-grid with only the ranking statistic's cost rung
moved, so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_cost-priced-is-chooser_B.py
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

DATE, SLUG = "2026-09-20", "cost-priced-is-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]            # the rungs the BOOK is charged
CIS = [0, 10, 25, 50]              # the rungs the CHOOSER's statistic is priced at (axis)
COST0 = 10                         # headline book cost
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]
FRESH = ("D", "W")                 # what V1 counts as a FRESH scalar
TRADES = ["W", "M"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0
FAMILIES = ["F_SHARPE", "F_CALMAR", "F_DD", "F_LEGS", "F_GXS", "F_GXDD"]
PLAIN = ["F_SHARPE", "F_CALMAR", "F_DD", "F_LEGS"]
NEUTRAL = ["F_GXS", "F_GXDD"]

# committed numbers this run must reproduce
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_1767 = dict(oCAGR=0.1611, oSharpe=1.2343, oMaxDD=-0.1968)     # U56 t=0.16 T=M R=W, 10 bps
GRID_1793 = ROOT / "research" / "backtests" / "2026-09-20_exposure-neutral-is-chooser_B.grid.csv"

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
             ("SMALL665", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio, read through
    close t-d.  (L,d) = (20,0) is the standing memo's convention (idea 1771 owns the surface)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------- two-schedule runner
def bt_two(px_ret, W0, g0, mT, mR):
    """engine.backtest's loop with TWO schedules (idea 1767's construction, as re-implemented by
    idea 1793).  A CURRENT SCALAR g_eff is updated ONLY on a refresh day (R); on a trade day (T)
    the names are re-spread to g_eff * ew_t; on a refresh-only day the whole book is scaled by ONE
    common factor.  Decisions at t applied at t+1.  T == R reproduces the standard book exactly."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    refmax = 0.0
    nref = 0
    for i in range(n):
        if mR[i] or i == 0:
            g_eff = g0[i]
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif mR[i]:
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
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref, refmax


class Book:
    """Pre-shifted arrays for one panel, so every (t, T, R) run is a single loop."""

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

    def g_const(self, k):
        return np.full(len(self.index), float(k))

    def run(self, g0, T, R):
        r, t, gs, nref, refmax = bt_two(self.R, self.W, g0, self.masks[T], self.masks[R])
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref, refmax)


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


# ------------------------------------------------------------------ gross-matched twin
def match_twin(bk, T, target_gross, lo_hi=(1e-4, 1.0), win=None, tol=1e-10, iters=200):
    """Bisect the CONSTANT gross k whose realised MEAN GROSS over `win` equals the book's.  The
    twin trades the same names on the same trade cadence T at constant exposure k.  The match is
    on EXPOSURE, which does not depend on the cost rung, so ONE bisection serves every c_IS."""
    lo, hi = lo_hi

    def mg(k):
        _, _, gs, _, _ = bk.run(bk.g_const(k), T, T)
        gs = gs.loc[win[0]:win[1]] if win else gs
        return float(gs.mean())

    mlo, mhi = mg(lo), mg(hi)
    if target_gross <= mlo:
        return lo, mlo
    if target_gross >= mhi:
        return hi, mhi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if mg(mid) < target_gross:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    k = 0.5 * (lo + hi)
    return k, mg(k)


# --------------------------------------------------------------- IS statistics at a cost rung
def is_stats(r0, t0, tw_r0, tw_t0, spy_is, c):
    """Every IS-readable statistic of one cell, priced at cost rung c.  Reads the IS window only."""
    r = net(r0, t0, c)
    m = mets(r)
    h1, h2 = halves(r)
    tw = mets(net(tw_r0, tw_t0, c))
    legs = (int(h1 > spy_is["h1"]) + int(h2 > spy_is["h2"])
            + int(m["MaxDD"] >= DD_CAP * spy_is["m"]["MaxDD"])
            + int(m["CAGR"] >= CAGR_FLOOR * spy_is["m"]["CAGR"]))
    return dict(F_SHARPE=m["Sharpe"],
                F_CALMAR=m["CAGR"] / abs(m["MaxDD"]) if m["MaxDD"] else np.nan,
                F_DD=m["MaxDD"],
                F_LEGS=legs + 1e-6 * m["Sharpe"],          # Sharpe breaks leg-count ties
                F_GXS=m["Sharpe"] - tw["Sharpe"],
                F_GXDD=m["MaxDD"] - tw["MaxDD"],
                is_CAGR=m["CAGR"], is_Sharpe=m["Sharpe"], is_MaxDD=m["MaxDD"],
                is_H1=h1, is_H2=h2, is_legs=legs,
                twin_is_Sharpe=tw["Sharpe"], twin_is_MaxDD=tw["MaxDD"])


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 1803 (lane B, {DATE}) — can a COST-PRICED IS-only chooser reach the DAILY-refresh "
        f"cells idea 1793 left unreachable?")
    log(f"# tuned dials (2): TARGET t {TARGETS} x REFRESH R {REFRESH}.  AXIS UNDER TEST: chooser "
        f"= family {FAMILIES} x c_IS {CIS} bps.  reported, not tuned: TRADE T {TRADES} (separate "
        f"arms), PANEL, BOOK COST {COSTS} bps.  sigma FIXED at (L={SIG_L}, d={SIG_D}).")
    log(f"# warm-up {WARMUP} rows; IS <= {IS_END}; OOS >= {OOS_START} (read ONCE, after every "
        f"chooser has committed).")

    PS, dropped = panels()
    log(f"# SMALL665: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, stat_rows = [], []
    g1r = g1t = g2 = g3 = g4 = g8 = g9 = 0.0
    g5max, g5n = 0.0, 0

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
        spy_is = dict(m=mets(spy.loc[:IS_END]), h1=halves(spy.loc[:IS_END])[0],
                      h2=halves(spy.loc[:IS_END])[1])
        B = dict(start=st, spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]),
                                    h1=halves(spy)[0], h2=halves(spy)[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1])
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {L['full']['CAGR']:.2%} / {L['full']['Sharpe']:.4f} "
            f"/ {L['full']['MaxDD']:.2%}  (OOS {L['oos']['CAGR']:.2%} / {L['oos']['Sharpe']:.4f} / "
            f"{L['oos']['MaxDD']:.2%})")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        # ---- G1 / G2: the diagonal is engine.backtest ------------------------------------
        if pname in ("U56", "B136"):
            Gp = (TGT_MEMO / bk.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = (eq_weight(px, cols).mul(Gp, axis=0)).fillna(0.0)
            a, at, _, _, _ = bk.run(bk.g_of(TGT_MEMO), "W", "W")
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
                for Rc in REFRESH:
                    r0, t0, gs, nref, refmax = bk.run(g0, T, Rc)
                    if nref:
                        g5max = max(g5max, refmax)
                        g5n += nref
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    g9 = max(g9, float(gs.max()))
                    yrs = len(r0) / 252.0
                    gm_full, gm_is = float(gs.mean()), float(gs.loc[:IS_END].mean())

                    # the twin the CHOOSER may see: matched on IS realised mean gross ONLY
                    k_is, got_is = match_twin(bk, T, gm_is, win=(st, pd.Timestamp(IS_END)))
                    g8 = max(g8, abs(got_is - gm_is))
                    tr0, tt0, _, _, _ = bk.run(bk.g_const(k_is), T, T)
                    tr0, tt0 = tr0.loc[st:].loc[:IS_END], tt0.loc[st:].loc[:IS_END]

                    # --- the chooser's statistics, one set per c_IS (IS window only) ------
                    ris, tis = r0.loc[:IS_END], t0.loc[:IS_END]
                    for cis in CIS:
                        sdict = is_stats(ris, tis, tr0, tt0, spy_is, cis)
                        stat_rows.append(dict(panel=pname, target=tgt, T_trade=T, R_refresh=Rc,
                                              c_IS=cis, twin_k_is=k_is, turn_py=float(t0.sum()/yrs),
                                              is_turn_py=float(tis.sum() / (len(ris) / 252.0)),
                                              **{k: float(v) for k, v in sdict.items()}))

                    # --- the book, at every real cost rung --------------------------------
                    for c in COSTS:
                        r = net(r0, t0, c)
                        mf, mo = mets(r), mets(r.loc[OOS_START:])
                        h1, h2 = halves(r)
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
                        rows.append(dict(
                            panel=pname, target=tgt, T_trade=T, R_refresh=Rc, cost=c,
                            fresh=(Rc in FRESH), turn_py=float(t0.sum() / yrs),
                            gross_mean=gm_full, gross_mean_is=gm_is, gross_max=float(gs.max()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            bind=bl, n_fail=nbad,
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a, keep4a_oos=k4ao))

    G = pd.DataFrame(rows)
    ST = pd.DataFrame(stat_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    ST.to_csv(f"{OUT}.isstats.csv", index=False)

    # -------------------------------------------------------------------- replication gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 bt_two diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c) = r0 - turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.target == TGT_MEMO) & (G.T_trade == "W")
                & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
        g3 = max(g3, max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                         abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                         abs(row.oos_Sharpe - pub["oSharpe"])))
    gate("G3 reproduces the standing KEEP-4b memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    r67 = G[(G.panel == "U56") & (G.target == TGT_MEMO) & (G.T_trade == "M")
            & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
    g4a = max(abs(r67.oos_CAGR - PUB_1767["oCAGR"]), abs(r67.oos_Sharpe - PUB_1767["oSharpe"]),
              abs(r67.oos_MaxDD - PUB_1767["oMaxDD"]))
    gate("G4a reproduces idea 1767's (T=M, R=W) U56 OOS row", f"max|d| = {g4a:.3e}",
         "< 1e-3", g4a < 1e-3)
    # G4b: CROSS-RUN replication of idea 1793's committed grid, every shared cell
    if GRID_1793.exists():
        o = pd.read_csv(GRID_1793)
        key = ["panel", "target", "T_trade", "R_refresh", "cost"]
        mrg = G.merge(o, on=key, suffixes=("", "_o"))
        cmpcols = ["turn_py", "Sharpe", "CAGR", "MaxDD", "oos_Sharpe", "oos_CAGR", "oos_MaxDD",
                   "gross_mean"]
        g4 = max(float((mrg[c] - mrg[f"{c}_o"]).abs().max()) for c in cmpcols)
        same4b = int((mrg.keep4b.astype(bool) == mrg.keep4b_o.astype(bool)).sum())
        gate("G4b CROSS-RUN: every shared cell of idea 1793's committed grid",
             f"{len(mrg)} cells, max|d| = {g4:.3e}, 4b verdicts identical {same4b}/{len(mrg)}",
             "< 1e-9 and all verdicts identical", g4 < 1e-9 and same4b == len(mrg))
        # and its is_Sharpe column is our c_IS = 10 statistic
        s10 = ST[ST.c_IS == COST0].merge(o[o.cost == COST0], on=["panel", "target", "T_trade",
                                                                 "R_refresh"])
        g4c = float((s10.is_Sharpe_x - s10.is_Sharpe_y).abs().max())
        g4d = float((s10.F_GXDD - s10.gx_MaxDD).abs().max())
        gate("G4c our c_IS=10 IS statistics == idea 1793's is_Sharpe / gx_MaxDD columns",
             f"max|d| = {g4c:.3e} (Sharpe) / {g4d:.3e} (gx_MaxDD)", "< 1e-9",
             max(g4c, g4d) < 1e-9)
    else:
        gate("G4b CROSS-RUN vs idea 1793's grid", "grid file absent", "present", False)
    gate("G5 a REFRESH row moves every held name by ONE common factor",
         f"max spread {g5max:.3e} over {g5n} refresh rows", "< 1e-12", g5max < 1e-12)
    gate("G6 tuned dials", "TARGET t, REFRESH R (the chooser is the axis, not a dial)",
         "exactly 2", True)
    nexp = len(PS) * len(TARGETS) * len(TRADES) * len(REFRESH)
    gate("G7 all grid cells published", f"{len(G)} book rows / {len(ST)} chooser-stat rows",
         f"{nexp*len(COSTS)} / {nexp*len(CIS)}",
         len(G) == nexp * len(COSTS) and len(ST) == nexp * len(CIS))
    gate("G8 twin realised-mean-gross match (IS window)", f"max|d| = {g8:.3e}", "< 1e-8", g8 < 1e-8)
    gate("G9 never levered", f"max realised gross {g9:.4f}", "<= 1.0", g9 <= 1.0 + 1e-12)

    # ------------------------------------------------------------------------- the choosers
    def pick_table(STsrc, Gsrc, tag, have_oos=True):
        out = []
        for pname, _, _ in PS:
            for T in TRADES:
                gd = Gsrc[(Gsrc.panel == pname) & (Gsrc.T_trade == T)
                          & (Gsrc.cost == COST0)] if have_oos else None
                for cis in CIS:
                    d = STsrc[(STsrc.panel == pname) & (STsrc.T_trade == T)
                              & (STsrc.c_IS == cis)]
                    for fam in FAMILIES:
                        r = d.sort_values([fam, "target"], ascending=[False, True]).iloc[0]
                        rec = dict(panel=pname, T_trade=T, chooser=f"{fam}@{cis}", family=fam,
                                   c_IS=cis, pick=f"t={r.target:.2f},R={r.R_refresh}",
                                   target=r.target, R_refresh=r.R_refresh,
                                   fresh=bool(r.R_refresh in FRESH), turn_py=r.turn_py)
                        if have_oos:
                            b = gd[(gd.target == r.target) & (gd.R_refresh == r.R_refresh)].iloc[0]
                            rec.update(_verdicts(b, Gsrc, pname, T))
                        out.append(rec)
                if have_oos:
                    for cname, tsel, rsel in [("C_MEMO", TGT_MEMO, "W")]:
                        b = gd[(gd.target == tsel) & (gd.R_refresh == rsel)].iloc[0]
                        out.append(dict(panel=pname, T_trade=T, chooser=cname, family=cname,
                                        c_IS=-1, pick=f"t={tsel:.2f},R={rsel}", target=tsel,
                                        R_refresh=rsel, fresh=(rsel in FRESH), turn_py=b.turn_py,
                                        **_verdicts(b, Gsrc, pname, T)))
                    orc = gd.sort_values(["keep4b", "oos_Sharpe"], ascending=False).iloc[0]
                    out.append(dict(panel=pname, T_trade=T, chooser="C_ORACLE_OOS",
                                    family="C_ORACLE_OOS", c_IS=-1,
                                    pick=f"t={orc.target:.2f},R={orc.R_refresh}", target=orc.target,
                                    R_refresh=orc.R_refresh, fresh=(orc.R_refresh in FRESH),
                                    turn_py=orc.turn_py, **_verdicts(orc, Gsrc, pname, T)))
        return pd.DataFrame(out)

    def _verdicts(b, Gsrc, pname, T):
        d = dict(oos_CAGR=b.oos_CAGR, oos_Sharpe=b.oos_Sharpe, oos_MaxDD=b.oos_MaxDD,
                 CAGR=b.CAGR, Sharpe=b.Sharpe, MaxDD=b.MaxDD, H1=b.H1, H2=b.H2,
                 keep4b_full=bool(b.keep4b_full), keep4b_oos=bool(b.keep4b_oos),
                 keep4b=bool(b.keep4b), keep4a=bool(b.keep4a), keep4a_oos=bool(b.keep4a_oos),
                 bind=b.bind)
        for c in COSTS:                                        # V5: cost-rung robustness
            rc = Gsrc[(Gsrc.panel == pname) & (Gsrc.T_trade == T) & (Gsrc.target == b.target)
                      & (Gsrc.R_refresh == b.R_refresh) & (Gsrc.cost == c)].iloc[0]
            d[f"keep4b@{c}"] = bool(rc.keep4b)
        d["cost_fragile"] = not d["keep4b@25"]
        return d

    P = pick_table(ST, G, "full")
    P.to_csv(f"{OUT}.choosers.csv", index=False)

    # ---- G10: no chooser reads a row on or after 2017-01-01 (TESTED, not asserted) --------
    log("\n   G10: rebuilding every chooser statistic on panels PHYSICALLY truncated at "
        f"{IS_END} ...")
    trows = []
    for pname, px, cols in PS:
        pxt = px.loc[:IS_END]
        st = px.index[WARMUP]
        bkt = Book(pxt, cols, pxt.index)
        spyt = pxt["SPY"].pct_change().fillna(0.0).loc[st:]
        spy_is = dict(m=mets(spyt), h1=halves(spyt)[0], h2=halves(spyt)[1])
        for tgt in TARGETS:
            g0 = bkt.g_of(tgt)
            for T in TRADES:
                for Rc in REFRESH:
                    r0, t0, gs, _, _ = bkt.run(g0, T, Rc)
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    k_is, _ = match_twin(bkt, T, float(gs.mean()), win=(st, pxt.index[-1]))
                    tr0, tt0, _, _, _ = bkt.run(bkt.g_const(k_is), T, T)
                    tr0, tt0 = tr0.loc[st:], tt0.loc[st:]
                    yrs = len(r0) / 252.0
                    for cis in CIS:
                        sd = is_stats(r0, t0, tr0, tt0, spy_is, cis)
                        trows.append(dict(panel=pname, target=tgt, T_trade=T, R_refresh=Rc,
                                          c_IS=cis, turn_py=float(t0.sum() / yrs),
                                          **{k: float(v) for k, v in sd.items()}))
    TRUNC = pd.DataFrame(trows)
    TRUNC.to_csv(f"{OUT}.truncated.csv", index=False)
    PT = pick_table(TRUNC, None, "trunc", have_oos=False)
    a = P[P.c_IS >= 0].set_index(["panel", "T_trade", "chooser"])["pick"]
    b = PT.set_index(["panel", "T_trade", "chooser"])["pick"]
    same = int(sum(a.loc[k] == b.loc[k] for k in a.index))
    gate("G10 every chooser's pick is unchanged on a panel TRUNCATED at 2016-12-31",
         f"{same} of {len(a)} identical", f"{len(a)} of {len(a)}", same == len(a))

    # --------------------------------------------------------------------------- the grid
    log("\n## THE GRID (all 120 cells x 4 cost rungs published to .grid.csv)")
    for c in COSTS:
        d = G[G.cost == c]
        log(f"   book cost {c:>2} bps: 4b FULL {int(d.keep4b_full.sum()):>3} | 4b OOS "
            f"{int(d.keep4b_oos.sum()):>3} | 4b FULL+OOS {int(d.keep4b.sum()):>3} | "
            f"4a {int(d.keep4a.sum()):>3} | 4a OOS {int(d.keep4a_oos.sum()):>3}  (of {len(d)})")
    d0 = G[G.cost == COST0]
    log("\n   binding-leg census at 10 bps (cells failing each leg):")
    for k in LEGS:
        log(f"     {k}: {int((d0[k] <= 0).sum()):>3} of {len(d0)}")
    log("\n   4b FULL+OOS at 10 bps by panel x T, split by R:")
    for pname, _, _ in PS:
        for T in TRADES:
            d = d0[(d0.panel == pname) & (d0.T_trade == T)]
            log(f"     {pname:<9} T={T}: {int(d.keep4b.sum()):>2} of {len(d)}   (by R: "
                + ", ".join(f"{r}={int(d[d.R_refresh==r].keep4b.sum())}/"
                            f"{len(d[d.R_refresh==r])}" for r in REFRESH) + ")")
    log("\n   mean turnover /yr by R (pooled over t, panels, T): "
        + ", ".join(f"{r}={d0[d0.R_refresh==r].turn_py.mean():.2f}" for r in REFRESH))

    # ------------------------------------------------- V3: the decomposition of the R gap
    log("\n## V3 — IS THE STALE-MINUS-FRESH IS-SHARPE GAP MADE OF COST?")
    dec = []
    for pname, _, _ in PS:
        for T in TRADES:
            for tgt in TARGETS:
                s = ST[(ST.panel == pname) & (ST.T_trade == T) & (ST.target == tgt)]
                def sh(R, c):
                    return float(s[(s.R_refresh == R) & (s.c_IS == c)].is_Sharpe.iloc[0])
                for R_stale in ("M", "Q"):
                    g10, g00 = sh(R_stale, 10) - sh("D", 10), sh(R_stale, 0) - sh("D", 0)
                    dec.append(dict(panel=pname, T_trade=T, target=tgt, stale=R_stale,
                                    gap10=g10, gap0=g00, cost_part=g10 - g00,
                                    cost_share=(g10 - g00) / g10 if g10 > 0 else np.nan,
                                    flips=(g10 > 0) and (g00 <= 0),
                                    d_turn=float(s[(s.R_refresh == "D") & (s.c_IS == 10)]
                                                 .is_turn_py.iloc[0])
                                    - float(s[(s.R_refresh == R_stale) & (s.c_IS == 10)]
                                            .is_turn_py.iloc[0])))
    DEC = pd.DataFrame(dec)
    DEC.to_csv(f"{OUT}.decomp.csv", index=False)
    pos = DEC[DEC.gap10 > 0]
    med = float(pos.cost_share.median()) if len(pos) else np.nan
    log(f"   cells where the STALE cell out-Sharpes the DAILY one in sample at 10 bps: "
        f"{len(pos)} of {len(DEC)}")
    log(f"   median cost share of that gap: {med:.3f}   (mean {pos.cost_share.mean():.3f}, "
        f"IQR {pos.cost_share.quantile(0.25):.3f}-{pos.cost_share.quantile(0.75):.3f})")
    log(f"   gaps that FLIP SIGN when the statistic is priced at 0 bps: "
        f"{int(DEC.flips.sum())} of {len(DEC)}")
    for pname, _, _ in PS:
        d = DEC[DEC.panel == pname]
        dp = d[d.gap10 > 0]
        log(f"     {pname:<9} stale-wins {len(dp)}/{len(d)} | median cost share "
            f"{dp.cost_share.median() if len(dp) else float('nan'):.3f} | flips "
            f"{int(d.flips.sum())}/{len(d)} | mean extra turnover of R=D "
            f"{d.d_turn.mean():+.2f}/yr")
    v3 = (med >= 0.50)

    # --------------------------------------------------------- V1: where the argmax lands
    log("\n## V1 — WHERE THE ARGMAX LANDS, BY THE COST RUNG THE STATISTIC IS PRICED AT")
    log("   (share of the 6 arms x 6 families whose pick has R in {D, W})")
    land = []
    for cis in CIS:
        d = P[P.c_IS == cis]
        by_r = ", ".join(f"{r}={int((d.R_refresh == r).sum())}" for r in REFRESH)
        land.append(dict(c_IS=cis, n=len(d), fresh=int(d.fresh.sum()),
                         share=float(d.fresh.mean()), daily=int((d.R_refresh == "D").sum())))
        log(f"   c_IS = {cis:>2} bps: FRESH (D or W) {int(d.fresh.sum()):>2} of {len(d)} "
            f"({d.fresh.mean():.3f})  |  R=D {int((d.R_refresh=='D').sum()):>2}  |  by R: {by_r}"
            f"  |  mean picked t {d.target.mean():.3f}")
    LAND = pd.DataFrame(land)
    n0 = int(P[P.c_IS == 0].fresh.sum())
    n10 = int(P[P.c_IS == COST0].fresh.sum())
    v1 = n0 > n10
    log(f"\n   per-family (rows) x c_IS (cols), 1 = FRESH pick on that arm, of 6 arms:")
    for fam in FAMILIES:
        log(f"     {fam:<10} " + "  ".join(
            f"c{cis}={int(P[(P.family == fam) & (P.c_IS == cis)].fresh.sum())}/6" for cis in CIS))

    # ------------------------------------------------------- V2/V4/V5: what it reaches
    log("\n## RULE 8 — dials (t, R) chosen on 2009-2016 ONLY; 2017-2026 read ONCE")
    cols = ["panel", "T_trade", "chooser", "pick", "turn_py", "CAGR", "Sharpe", "MaxDD", "H1",
            "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "keep4b_full", "keep4b_oos", "keep4b",
            "keep4a", "keep4a_oos", "keep4b@0", "keep4b@25", "keep4b@50", "cost_fragile", "bind"]
    log(P[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    log("\n   reach by chooser (6 arms = 3 panels x 2 trade cadences):")
    reach = {}
    for cis in CIS:
        for fam in FAMILIES:
            s = P[(P.family == fam) & (P.c_IS == cis)]
            reach[f"{fam}@{cis}"] = int(s.keep4b.sum())
            log(f"     {fam:<10}@{cis:<2} 4b FULL+OOS {int(s.keep4b.sum())} of 6 | 4b OOS "
                f"{int(s.keep4b_oos.sum())} | 4a OOS {int(s.keep4a_oos.sum())} | FRESH "
                f"{int(s.fresh.sum())} | mean OOS Sharpe {s.oos_Sharpe.mean():.4f} | mean OOS "
                f"MaxDD {s.oos_MaxDD.mean():.2%} | robust@25 {int(s['keep4b@25'].sum())}")
    for cname in ("C_MEMO", "C_ORACLE_OOS"):
        s = P[P.chooser == cname]
        log(f"     {cname:<13} 4b FULL+OOS {int(s.keep4b.sum())} of 6 | mean OOS Sharpe "
            f"{s.oos_Sharpe.mean():.4f} | mean OOS MaxDD {s.oos_MaxDD.mean():.2%}")

    best0 = max(reach[f"{f}@0"] for f in FAMILIES)
    best10 = max(reach[f"{f}@{COST0}"] for f in FAMILIES)
    v2 = best0 > best10
    legal = P[P.c_IS >= 0]
    v4 = int(legal.keep4b.sum())
    v5tab = legal[legal.keep4b]
    log(f"\n   V1 c_IS=0 lands FRESH more often than c_IS=10: {n0} vs {n10} of {len(P[P.c_IS==0])}"
        f" -> {'TRIGGERED' if v1 else 'NOT TRIGGERED'}")
    log(f"   V2 best c_IS=0 chooser reaches more arms than best c_IS=10: {best0} vs {best10} -> "
        f"{'TRIGGERED' if v2 else 'NOT TRIGGERED'}")
    log(f"   V3 the stale-minus-fresh IS gap is majority COST (median share {med:.3f} >= 0.50) -> "
        f"{'TRIGGERED' if v3 else 'NOT TRIGGERED'}")
    log(f"   V4 legal IS-only picks clearing 4b FULL+OOS at 10 bps: {v4} of {len(legal)}")
    log(f"   V5 of those, COST-FRAGILE (fail 4b at 25 bps): "
        f"{int(v5tab.cost_fragile.sum())} of {len(v5tab)}")

    if len(v5tab):
        log("\n   the reached 4b FULL+OOS cells (V4/V5 detail):")
        log(v5tab[["panel", "T_trade", "chooser", "pick", "turn_py", "CAGR", "Sharpe", "MaxDD",
                   "H1", "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "keep4b@0", "keep4b@25",
                   "keep4b@50"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    LAND.to_csv(f"{OUT}.landing.csv", index=False)
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in _gates)
    log(f"\n## GATES {npass} of {len(_gates)}")
    log("\n## SURVIVORSHIP: U56 / B136 are CURRENT constituents and SMALL665 a CURRENT sub-$2B "
        "screen; every LEVEL is optimistic.  The chooser contrast is same-tape / same-grid with "
        "only the statistic's cost rung moved, so it is first-order immune; the pass COUNTS are "
        "not.")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    print(f"\nwrote {OUT}.grid.csv / .isstats.csv / .choosers.csv / .decomp.csv / .landing.csv / "
          f".truncated.csv / .gates.csv / .log.txt")


if __name__ == "__main__":
    main()
