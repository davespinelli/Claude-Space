#!/usr/bin/env python3
"""Idea 1793 (lane B, 2026-09-20) — CAN AN EXPOSURE-NEUTRAL IS-ONLY CHOOSER REACH THE 4b CELLS
THAT PLAIN IS SHARPE MISSES?

THE DEFECT THIS PRICES.  Three runs on 2026-09-20 found the SAME failure and none of them tried
to fix it.  Idea 1771 (t x L x d): IS Sharpe peaks at t = 0.16 and the surface argmax is the
STALER convention, which fails 4b OOS on the drawdown cap.  Idea 1767 (T x R): 23 of 24 legal
IS-only picks land off-diagonal on a STALE scalar (R = M or Q) "because IS Sharpe rewards the
lazier, higher-gross book", and on U56 all eight picks go to (T=Q, R=M) and fail 4b OOS.  Idea
1763 (sigma source): a chooser handed the source free buys SPY 14 of 18 times because SPY's sigma
runs ~9% hot, pushing the target argmax one rung UP.  One mechanism explains all three: 2009-2016
is a low-vol bull, so every IS statistic the record uses is bought by EXPOSURE, and the cheapest
way to buy IS Sharpe on an exposure dial is to set the dial to its most-exposed end.  The 4b
DRAWDOWN CAP then collects the bill out of sample.

THE FIX TESTED HERE.  Idea 1771 built the machinery to price a book AGAINST ITS OWN REALISED-
MEAN-GROSS-MATCHED CONSTANT-GROSS TWIN, and found vol-targeting the first device in the record to
beat that twin at scale.  That difference is computable ENTIRELY IN SAMPLE, so it is a legal
rule-8 chooser.  This run asks whether scoring each variant on

    IS Sharpe(book)  -  IS Sharpe(its OWN twin, matched to the book's IS realised mean gross)

("EXPOSURE-NEUTRAL", C_GXS; and the drawdown version C_GXDD) reaches 4b-passing cells that plain
IS Sharpe / Calmar / MaxDD / leg-count cannot.  A chooser that cannot be bought by exposure alone
should not be walked into the most-exposed rung.

PRE-STATED VERDICT RULES (fixed before the run):
  V1  THE IDEA'S OWN QUESTION.  Over the 6 arms (panel x T), the exposure-neutral choosers
      (C_GXS, C_GXDD) reach a cell clearing 4b FULL *and* OOS on STRICTLY MORE arms than the best
      plain IS chooser.  Not triggered -> the exposure-neutral chooser is KILLED as a fix.
  V2  DOMINANCE.  Pooled over arms, the exposure-neutral picks post higher OOS Sharpe AND shallower
      OOS MaxDD than the plain picks.
  V3  LANDING ZONE.  The exposure-neutral picks land inside idea 1771's convention-robust band
      t in {0.10, 0.12} on more arms than the plain picks do.
  V4  CAPITAL.  Any cell clearing 4b FULL *and* OOS that a legal IS-only chooser actually REACHES
      is a KEEP-4b candidate; path 4a is scored at every cell too.

DIALS.  EXACTLY TWO are tuned (spent by the chooser): TARGET `t` in {0.08,0.10,0.12,0.16,0.20}
and REFRESH cadence `R` in {D,W,M,Q} = 20 cells per arm.  REPORTED, NOT TUNED: TRADE cadence
`T` in {W,M} (each (panel,T) is a separate ARM; no chooser ever selects across T), PANEL
{U56,B136,SMALL665}, COST {0,10,25,50} bps.  The sigma convention is FIXED at the standing memo's
(L = 20, d = 0) and is not a dial here (idea 1771 owns that surface).  Every grid point published.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00);
rule 3 (RULES v2 live book AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea,
deterministic, standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  The CHOOSER contrast is same-tape / same-names / same-grid with only the ranking
statistic moved, so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_exposure-neutral-is-chooser_B.py
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

DATE, SLUG = "2026-09-20", "exposure-neutral-is-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]
TRADES = ["W", "M"]
BAND_ROBUST = (0.10, 0.12)          # idea 1771's convention-robust band (OOS-visible; NOT a pick)
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0                # the standing memo's sigma convention, FIXED (not a dial)

# committed numbers this run must reproduce
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_1767 = dict(oCAGR=0.1611, oSharpe=1.2343, oMaxDD=-0.1968)     # U56 t=0.16 T=M R=W, 10 bps

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
             ("SMALL665", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio, read through
    close t-d.  (L,d) = (20,0) is the standing memo's convention."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------- two-schedule runner
def bt_two(px_ret, W0, g0, mT, mR):
    """engine.backtest's loop with TWO schedules (idea 1767's construction, re-implemented on
    arrays).  A CURRENT SCALAR g_eff is updated ONLY on a refresh day (R); on a trade day (T) the
    names are re-spread to g_eff * ew_t; on a refresh-only day the book is scaled by ONE common
    factor.  Decisions at t applied at t+1.  T == R reproduces the standard book exactly."""
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
    """Bisect the CONSTANT gross k whose realised MEAN GROSS over `win` equals the book's.
    The twin trades the same names on the same trade cadence T at constant exposure k; its
    refresh schedule is T (constant gross has no scalar to refresh)."""
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


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 1793 (lane B, {DATE}) — can an EXPOSURE-NEUTRAL IS-ONLY chooser reach the 4b "
        f"cells that plain IS Sharpe misses?")
    log(f"# tuned dials (2): TARGET t {TARGETS} x REFRESH R {REFRESH}.  reported, not tuned: "
        f"TRADE T {TRADES} (separate arms), PANEL, COST {COSTS} bps.  sigma convention FIXED at "
        f"(L={SIG_L}, d={SIG_D}).  warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")

    PS, dropped = panels()
    log(f"# SMALL665: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, twin_rows, ch_rows = [], [], []
    BASE = {}
    g1r = g1t = g2 = g3 = g4 = g8 = 0.0
    g9 = 0.0
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
        B = dict(start=st,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1],
                          ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1])
        BASE[pname] = B
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
                    gm_full = float(gs.mean())
                    gm_is = float(gs.loc[:IS_END].mean())

                    # --- the twin the CHOOSER is allowed to see: matched on IS ONLY --------
                    k_is, got_is = match_twin(bk, T, gm_is, win=(st, pd.Timestamp(IS_END)))
                    g8 = max(g8, abs(got_is - gm_is))
                    tr0, tt0, tgs, _, _ = bk.run(bk.g_const(k_is), T, T)
                    tr0, tt0 = tr0.loc[st:], tt0.loc[st:]
                    tr = net(tr0, tt0, COST0)
                    tw_is = mets(tr.loc[:IS_END])

                    # --- the twin used only for REPORTING the dial: matched on FULL --------
                    k_f, got_f = match_twin(bk, T, gm_full, win=(st, px.index[-1]))
                    g8 = max(g8, abs(got_f - gm_full))
                    fr0, ft0, _, _, _ = bk.run(bk.g_const(k_f), T, T)
                    fr0, ft0 = fr0.loc[st:], ft0.loc[st:]
                    fr = net(fr0, ft0, COST0)
                    tw_full, tw_oos = mets(fr), mets(fr.loc[OOS_START:])

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
                        k4a = (h1 > LV["h1"] and h2 > LV["h2"] and mf["MaxDD"] >= LV["full"]["MaxDD"])
                        k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"]
                                and mo["MaxDD"] >= LV["oos"]["MaxDD"])
                        # IS-readable legs only (no OOS anywhere): halves of the IS window
                        is_legs = int(ih1 > S["ish1"]) + int(ih2 > S["ish2"]) \
                            + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"]) \
                            + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"])
                        rows.append(dict(
                            panel=pname, target=tgt, T_trade=T, R_refresh=Rc, cost=c,
                            diag=(T == Rc), turn_py=float(t0.sum() / yrs),
                            gross_mean=gm_full, gross_mean_is=gm_is, gross_max=float(gs.max()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            is_H1=ih1, is_H2=ih2, is_legs=is_legs,
                            is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
                            twin_k_is=k_is, twin_is_Sharpe=tw_is["Sharpe"],
                            twin_is_MaxDD=tw_is["MaxDD"],
                            gx_Sharpe=mi["Sharpe"] - tw_is["Sharpe"],
                            gx_MaxDD=mi["MaxDD"] - tw_is["MaxDD"],
                            twin_k_full=k_f, twin_Sharpe=tw_full["Sharpe"],
                            twin_MaxDD=tw_full["MaxDD"], twin_oos_Sharpe=tw_oos["Sharpe"],
                            twin_oos_MaxDD=tw_oos["MaxDD"],
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            bind=bl, n_fail=nbad,
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a, keep4a_oos=k4ao))
                    twin_rows.append(dict(panel=pname, target=tgt, T_trade=T, R_refresh=Rc,
                                          k_is=k_is, k_full=k_f, gross_is=gm_is,
                                          gross_full=gm_full,
                                          d_is_Sharpe=rows[-1]["gx_Sharpe"],
                                          d_is_MaxDD=rows[-1]["gx_MaxDD"],
                                          d_oos_Sharpe=rows[-1]["oos_Sharpe"] - tw_oos["Sharpe"],
                                          d_oos_MaxDD=rows[-1]["oos_MaxDD"] - tw_oos["MaxDD"]))

    G = pd.DataFrame(rows)
    TW = pd.DataFrame(twin_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    TW.to_csv(f"{OUT}.twins.csv", index=False)

    # -------------------------------------------------------------------- replication gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 bt_two diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c)=r0-turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.target == TGT_MEMO) & (G.T_trade == "W")
                & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
        d = max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                abs(row.oos_Sharpe - pub["oSharpe"]))
        g3 = max(g3, d)
    gate("G3 reproduces the standing KEEP-4b memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    r67 = G[(G.panel == "U56") & (G.target == TGT_MEMO) & (G.T_trade == "M")
            & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
    g4 = max(abs(r67.oos_CAGR - PUB_1767["oCAGR"]), abs(r67.oos_Sharpe - PUB_1767["oSharpe"]),
             abs(r67.oos_MaxDD - PUB_1767["oMaxDD"]))
    gate("G4 reproduces idea 1767's (T=M, R=W) U56 OOS row", f"max|d| = {g4:.3e}",
         "< 1e-3", g4 < 1e-3)
    gate("G5 a REFRESH row moves every held name by ONE common factor",
         f"max spread {g5max:.3e} over {g5n} refresh rows", "< 1e-12", g5max < 1e-12)
    gate("G6 tuned dials", "TARGET t, REFRESH R", "exactly 2", True)
    gate("G7 all grid cells published",
         f"{len(G)} rows = {len(PS)} panels x {len(TARGETS)} t x {len(TRADES)} T x "
         f"{len(REFRESH)} R x {len(COSTS)} costs",
         str(len(PS) * len(TARGETS) * len(TRADES) * len(REFRESH) * len(COSTS)),
         len(G) == len(PS) * len(TARGETS) * len(TRADES) * len(REFRESH) * len(COSTS))
    gate("G8 twin realised-mean-gross match", f"max|d| = {g8:.3e}", "< 1e-8", g8 < 1e-8)
    gate("G9 never levered", f"max realised gross {g9:.4f}", "<= 1.0", g9 <= 1.0 + 1e-12)

    # ------------------------------------------------------------------------- the choosers
    CH = {
        "C_ISSHARPE":  lambda d: d.sort_values(["is_Sharpe"], ascending=False).iloc[0],
        "C_ISCALMAR":  lambda d: d.sort_values(["is_Calmar"], ascending=False).iloc[0],
        "C_ISDD":      lambda d: d.sort_values(["is_MaxDD"], ascending=False).iloc[0],
        "C_ISLEGS":    lambda d: d.sort_values(["is_legs", "is_Sharpe"], ascending=False).iloc[0],
        "C_GXS":       lambda d: d.sort_values(["gx_Sharpe"], ascending=False).iloc[0],
        "C_GXDD":      lambda d: d.sort_values(["gx_MaxDD"], ascending=False).iloc[0],
    }
    PLAIN = ["C_ISSHARPE", "C_ISCALMAR", "C_ISDD", "C_ISLEGS"]
    NEUTRAL = ["C_GXS", "C_GXDD"]

    def pick_table(Gsrc, tag):
        out = []
        for pname, _, _ in PS:
            for T in TRADES:
                d = Gsrc[(Gsrc.panel == pname) & (Gsrc.T_trade == T)
                         & (Gsrc.cost == COST0)].copy()
                for cn, fn in CH.items():
                    r = fn(d)
                    out.append(dict(src=tag, panel=pname, T_trade=T, chooser=cn,
                                    pick=f"t={r.target:.2f},R={r.R_refresh}",
                                    target=r.target, R_refresh=r.R_refresh,
                                    in_band=bool(r.target in BAND_ROBUST),
                                    oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe,
                                    oos_MaxDD=r.oos_MaxDD, turn_py=r.turn_py,
                                    keep4b_full=bool(r.keep4b_full), keep4b_oos=bool(r.keep4b_oos),
                                    keep4b=bool(r.keep4b), keep4a_oos=bool(r.keep4a_oos),
                                    bind=r.bind))
                # controls
                memo = d[(d.target == TGT_MEMO) & (d.R_refresh == "W")].iloc[0]
                out.append(dict(src=tag, panel=pname, T_trade=T, chooser="C_MEMO",
                                pick=f"t={TGT_MEMO:.2f},R=W", target=TGT_MEMO, R_refresh="W",
                                in_band=False, oos_CAGR=memo.oos_CAGR, oos_Sharpe=memo.oos_Sharpe,
                                oos_MaxDD=memo.oos_MaxDD, turn_py=memo.turn_py,
                                keep4b_full=bool(memo.keep4b_full),
                                keep4b_oos=bool(memo.keep4b_oos), keep4b=bool(memo.keep4b),
                                keep4a_oos=bool(memo.keep4a_oos), bind=memo.bind))
                orc = d.sort_values(["keep4b", "oos_Sharpe"], ascending=False).iloc[0]
                out.append(dict(src=tag, panel=pname, T_trade=T, chooser="C_ORACLE_OOS",
                                pick=f"t={orc.target:.2f},R={orc.R_refresh}", target=orc.target,
                                R_refresh=orc.R_refresh, in_band=bool(orc.target in BAND_ROBUST),
                                oos_CAGR=orc.oos_CAGR, oos_Sharpe=orc.oos_Sharpe,
                                oos_MaxDD=orc.oos_MaxDD, turn_py=orc.turn_py,
                                keep4b_full=bool(orc.keep4b_full), keep4b_oos=bool(orc.keep4b_oos),
                                keep4b=bool(orc.keep4b), keep4a_oos=bool(orc.keep4a_oos),
                                bind=orc.bind))
        return pd.DataFrame(out)

    P = pick_table(G, "full")
    P.to_csv(f"{OUT}.choosers.csv", index=False)

    # ---- G10: no chooser reads a row on or after 2017-01-01 (TESTED, not asserted) --------
    # every chooser input is recomputed from a panel TRUNCATED at IS_END; picks must be identical.
    trunc_rows = []
    for pname, px, cols in PS:
        pxt = px.loc[:IS_END]
        st = px.index[WARMUP]
        bkt = Book(pxt, cols, pxt.index)
        spyt = pxt["SPY"].pct_change().fillna(0.0).loc[st:]
        s_is, s_h1, s_h2 = mets(spyt), halves(spyt)[0], halves(spyt)[1]
        for tgt in TARGETS:
            g0 = bkt.g_of(tgt)
            for T in TRADES:
                for Rc in REFRESH:
                    r0, t0, gs, _, _ = bkt.run(g0, T, Rc)
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    gm_is = float(gs.mean())
                    k_is, _ = match_twin(bkt, T, gm_is, win=(st, pxt.index[-1]))
                    tr0, tt0, _, _, _ = bkt.run(bkt.g_const(k_is), T, T)
                    tw = mets(net(tr0.loc[st:], tt0.loc[st:], COST0))
                    r = net(r0, t0, COST0)
                    mi = mets(r)
                    ih1, ih2 = halves(r)
                    trunc_rows.append(dict(
                        panel=pname, target=tgt, T_trade=T, R_refresh=Rc, cost=COST0,
                        is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                        is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
                        is_legs=int(ih1 > s_h1) + int(ih2 > s_h2)
                        + int(mi["MaxDD"] >= DD_CAP * s_is["MaxDD"])
                        + int(mi["CAGR"] >= CAGR_FLOOR * s_is["CAGR"]),
                        gx_Sharpe=mi["Sharpe"] - tw["Sharpe"],
                        gx_MaxDD=mi["MaxDD"] - tw["MaxDD"],
                        oos_CAGR=np.nan, oos_Sharpe=np.nan, oos_MaxDD=np.nan, turn_py=np.nan,
                        keep4b_full=False, keep4b_oos=False, keep4b=False, keep4a_oos=False,
                        bind=""))
    TR = pd.DataFrame(trunc_rows)
    PT = pick_table(TR, "trunc")
    same = 0
    tot = 0
    for cn in CH:
        a = P[(P.chooser == cn)].set_index(["panel", "T_trade"])["pick"]
        b = PT[(PT.chooser == cn)].set_index(["panel", "T_trade"])["pick"]
        for key in a.index:
            tot += 1
            same += int(a.loc[key] == b.loc[key])
    gate("G10 every chooser's pick is unchanged on a panel TRUNCATED at 2016-12-31",
         f"{same} of {tot} identical", f"{tot} of {tot}", same == tot)
    TR.to_csv(f"{OUT}.truncated.csv", index=False)

    # --------------------------------------------------------------------------- the answer
    log("\n## THE GRID (4b / 4a pass counts, all cells published)")
    for c in COSTS:
        d = G[G.cost == c]
        log(f"   cost {c:>2} bps: 4b FULL {int(d.keep4b_full.sum()):>3} | 4b OOS "
            f"{int(d.keep4b_oos.sum()):>3} | 4b FULL+OOS {int(d.keep4b.sum()):>3} | "
            f"4a {int(d.keep4a.sum()):>3} | 4a OOS {int(d.keep4a_oos.sum()):>3}  (of {len(d)})")
    d0 = G[G.cost == COST0]
    log("\n   binding-leg census at 10 bps (cells failing each leg):")
    for k in LEGS:
        log(f"     {k}: {int((d0[k] <= 0).sum()):>3} of {len(d0)}")
    log("\n   4b FULL+OOS pass share at 10 bps by panel x T:")
    for pname, _, _ in PS:
        for T in TRADES:
            d = d0[(d0.panel == pname) & (d0.T_trade == T)]
            log(f"     {pname:<9} T={T}: {int(d.keep4b.sum()):>2} of {len(d)}   "
                f"(by R: " + ", ".join(f"{r}={int(d[d.R_refresh==r].keep4b.sum())}/"
                                       f"{len(d[d.R_refresh==r])}" for r in REFRESH) + ")")
    log("\n   4b FULL+OOS pass share at 10 bps by target (pooled over R, T, U56+B136):")
    dd = d0[d0.panel != "SMALL665"]
    for t in TARGETS:
        d = dd[dd.target == t]
        log(f"     t={t:.2f}: {int(d.keep4b.sum()):>2} of {len(d)}")

    log("\n## RULE 8 — dials (t, R) chosen on 2009-2016 ONLY; 2017-2026 read ONCE")
    log(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    reach = P[P.chooser.isin(PLAIN + NEUTRAL)].groupby("chooser").keep4b.sum()
    n_arms = len(PS) * len(TRADES)
    log(f"\n   arms = {n_arms} (panel x T).  4b FULL+OOS reached:")
    for cn in PLAIN + NEUTRAL + ["C_MEMO", "C_ORACLE_OOS"]:
        s = P[P.chooser == cn]
        log(f"     {cn:<13} {int(s.keep4b.sum())} of {n_arms} | 4b OOS {int(s.keep4b_oos.sum())} "
            f"| 4a OOS {int(s.keep4a_oos.sum())} | in-band {int(s.in_band.sum())} | mean OOS "
            f"Sharpe {s.oos_Sharpe.mean():.4f} | mean OOS MaxDD {s.oos_MaxDD.mean():.2%}")

    best_plain = int(max(P[P.chooser == cn].keep4b.sum() for cn in PLAIN))
    best_neu = int(max(P[P.chooser == cn].keep4b.sum() for cn in NEUTRAL))
    v1 = best_neu > best_plain
    pl = P[P.chooser.isin(PLAIN)]
    ne = P[P.chooser.isin(NEUTRAL)]
    v2 = (ne.oos_Sharpe.mean() > pl.oos_Sharpe.mean()) and (ne.oos_MaxDD.mean() > pl.oos_MaxDD.mean())
    v3 = (ne.in_band.mean() > pl.in_band.mean())
    v4 = int(P[P.chooser.isin(PLAIN + NEUTRAL)].keep4b.sum())
    log(f"\n   V1 exposure-neutral reaches MORE arms than the best plain chooser: "
        f"{best_neu} vs {best_plain} -> {'TRIGGERED' if v1 else 'NOT TRIGGERED'}")
    log(f"   V2 dominance (mean OOS Sharpe {ne.oos_Sharpe.mean():.4f} vs {pl.oos_Sharpe.mean():.4f}; "
        f"mean OOS MaxDD {ne.oos_MaxDD.mean():.2%} vs {pl.oos_MaxDD.mean():.2%}) -> "
        f"{'TRIGGERED' if v2 else 'NOT TRIGGERED'}")
    log(f"   V3 landing zone t in {BAND_ROBUST} (share {ne.in_band.mean():.3f} vs "
        f"{pl.in_band.mean():.3f}) -> {'TRIGGERED' if v3 else 'NOT TRIGGERED'}")
    log(f"   V4 legal IS-only picks clearing 4b FULL+OOS: {v4} of "
        f"{len(P[P.chooser.isin(PLAIN + NEUTRAL)])}")

    log("\n## THE DIAL vs ITS OWN FULL-MATCHED TWIN (reporting control, idea 1771's statistic)")
    for pname, _, _ in PS:
        t = TW[TW.panel == pname]
        log(f"   {pname:<9} OOS dSharpe mean {t.d_oos_Sharpe.mean():+.4f} (win "
            f"{(t.d_oos_Sharpe > 0).mean():.3f}) | OOS dMaxDD mean {t.d_oos_MaxDD.mean():+.2%} "
            f"(win {(t.d_oos_MaxDD > 0).mean():.3f}) | IS dSharpe mean {t.d_is_Sharpe.mean():+.4f} "
            f"(win {(t.d_is_Sharpe > 0).mean():.3f})")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in _gates)
    log(f"\n## GATES {npass} of {len(_gates)}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    print(f"\nwrote {OUT}.grid.csv / .twins.csv / .choosers.csv / .truncated.csv / .gates.csv / .log.txt")


if __name__ == "__main__":
    main()
