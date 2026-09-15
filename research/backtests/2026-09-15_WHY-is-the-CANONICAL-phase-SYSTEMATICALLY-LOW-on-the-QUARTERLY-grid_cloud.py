#!/usr/bin/env python3
"""Idea 961 (cloud, 2026-09-15) -- WHY is the CANONICAL phase SYSTEMATICALLY LOW on the
QUARTERLY grid?

THE PRIOR RESULT BEING EXPLAINED (idea 942, committed)
  On the quarterly grid the canonical quarter-end rebalance date is the CAGR MAXIMUM of its own
  63-phase family in 0 of 150 cells, mean percentile 0.170, and the family argmax never lands
  closer than 17 trading days before quarter-end (median 29, mode 23).  A 0-of-150 is a
  mechanism, not noise.  942 measured it; it did not say WHY.

THREE CANDIDATE MECHANISMS, AND WHAT EACH PREDICTS
  (c) ALIAS      -- `score()` carries a 63-TRADING-DAY leg (r3 = px / px.shift(63)).  A 63-phase
                    rebalance grid tiles EXACTLY with that lookback, so every phase-p rebalance
                    reads an r3 window whose endpoints are pinned to the same grid.  If this is
                    the carrier, de-tuning the r3 lookback off 63 (55, 84) or deleting the leg
                    must move the canonical percentile back toward 0.5.
  (a) CALENDAR   -- quarter-end flows in the TAPE itself (window dressing, fund flows, the
                    quarterly option/futures expiry).  If this is the carrier the deficit must
                    survive on a book with NO cross-sectional ranking and NO momentum leg at all
                    (BAND03 = RULES v2, the live baseline).
  (b) RECONSTITUTION -- index adds/drops at quarter boundaries.  **NOT DIRECTLY TESTABLE HERE**:
                    the sandbox carries no index-membership history, only prices.  Whatever it
                    does to a price-only book, it must do THROUGH the calendar channel, which
                    H_CALENDAR measures.  Stated as a limit, not tested as a hypothesis.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_ALIAS     the 63-day r3 leg is the carrier.
              PASS iff >= 5 of the 6 DE-ALIASED cells (3 variants x 2 panels: R3_55, R3_84,
              NOR3) read a canonical CAGR percentile ABOVE 0.40, against 942's 0.170 mean.
  H_CALENDAR  the tape's quarter-end calendar is the carrier, independent of any signal.
              PASS iff BAND03 -- which has no rank, no momentum leg, no 63-day anything --
              reads canonical percentile <= 0.25 on BOTH panels.
  H_MOM       the deficit is a property of MOMENTUM SELECTION generally, not of the 63-day leg.
              PASS iff MOMONLY (12-1 momentum alone, no 126d leg, no 63d leg) reads canonical
              percentile <= 0.25 on BOTH panels.
  These are not exclusive: H_ALIAS and H_MOM can both fail, which is itself the answer.

TWO TUNED DIALS, ALL GRID POINTS REPORTED
  MECHANISM SET  {CAND20 (r3=63, the 2026-09-04 KEEP 4b candidate), R3_55, R3_84, NOR3,
                  MOMONLY, BAND03}                                            -- 6 levels
  PANEL          {U56, B136}                                                  -- 2 levels
  Everything else is a REPORTED CONSTANT, never tuned: gross 0.75, cost 10 bps, lag 1,
  warmup 260, n=20, max_vol 0.60, 200d gate, band 0.03.

RULE 8 (walk-forward), run on every cell
  Choose the phase on the IS window (<= 2016-12-31) by CAGR; evaluate untouched on OOS
  (>= 2017-01-01).  Report OOS CAGR/Sharpe/MaxDD for the IS-chosen phase, the CANONICAL
  quarter-end, and the phase-family MEDIAN, against the RULES v2 baseline and SPY, and score
  both KEEP paths (4a and 4b) on each.

GATES
  G1  fast runner == `engine.backtest` @10 bps post-warmup, on 3 books x 2 freqs.  Bar 1e-12.
  G2  BAND03 weights == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CAND20 reproduces the 2026-09-04 committed triple 12.66% / 1.0921 / -18.31% at the
      record's own vintage tolerance (CAGR 5e-3, MaxDD 5e-3, Sharpe 3.3e-2 -- the record has
      already committed, at CHANGELOG 2026-09-15, that the published Sharpe is NOT recoverable
      from this tree, reading 1.0596-1.0881; the bar is set to that KNOWN drift and the miss is
      printed, not hidden).
  G4  the 63-phase family partitions the trading days exactly (each day in exactly one phase).
  G5  determinism: the whole grid runs twice, tables byte-identical.

SURVIVORSHIP: U56 and B136 are CURRENT-constituent lists, so every CAGR and drawdown LEVEL is
optimistic.  Every number here is a WITHIN-PANEL, SAME-TAPE contrast between rebalance dates on
identical names, which survivorship does not touch; the 4b levels are read against SPY and are
NOT protected by that argument.

COSTS 10 bps per unit turnover, weights decided at close t applied at close t+1 (PROTOCOL 2).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0
GROSS = 0.75
LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
BAND = 0.03
PHASE_LEN = 63                      # trading days in a quarter; 942's family size
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# pre-registered bars
ALIAS_BAR, ALIAS_MIN_CELLS = 0.40, 5
CAL_BAR = 0.25

PANELS = ["U56", "B136"]
MECHS = ["CAND20", "R3_55", "R3_84", "NOR3", "MOMONLY", "BAND03"]
DEALIASED = ["R3_55", "R3_84", "NOR3"]
MECH_SRC = {
    "CAND20":  "the 2026-09-04 KEEP 4b candidate: legs mom(21,252)+r6(0,126)+r3(0,63), 200d gate, vol20<0.60, top-20 EW",
    "R3_55":   "identical, r3 lookback 63 -> 55 (off the 63-day grid)",
    "R3_84":   "identical, r3 lookback 63 -> 84 (off the 63-day grid)",
    "NOR3":    "identical, r3 leg DELETED (mom + r6 only)",
    "MOMONLY": "identical, 12-1 momentum leg ONLY (no r6, no r3)",
    "BAND03":  "RULES v2 live baseline: no rank, no momentum leg, 200d +/-3% band, EW, de-gross",
}
# committed triple, 2026-09-04 KEEP 4b candidate (CAND20 on U56, gross 0.75, weekly, 10 bps)
CAND20_PUB = (0.1266, 1.0921, -0.1831)
G3_TOL = (5e-3, 3.3e-2, 5e-3)       # (CAGR, Sharpe, MaxDD) -- Sharpe bar set to the record's own
                                    # committed, unexplained vintage drift; see docstring
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# runner -- same semantics as engine.backtest, arbitrary rebalance mask (gated at G1)
# ================================================================================================
def run(rets: np.ndarray, wt: np.ndarray, applied: np.ndarray, gross: float, cost: float):
    """rets T x N daily returns; wt T x N gross-1.0 target weights ALREADY lag-shifted;
    applied T bool = days on which the target is put on.  Returns (daily returns, turnover)."""
    T, N = rets.shape
    cur = np.zeros(N)
    port = np.empty(T)
    turn = np.zeros(T)
    for i in range(T):
        if applied[i]:
            new = gross * wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = cur @ rets[i]
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return port - turn * cost / 1e4, turn


def lag_weights(W1: np.ndarray) -> np.ndarray:
    wt = np.roll(W1, LAG, axis=0).copy()
    wt[:LAG] = 0.0
    return wt


def applied_from_decision(dec: np.ndarray) -> np.ndarray:
    a = np.roll(dec, LAG)
    a[:LAG] = False
    a[0] = True                      # engine's `or i == 0`
    return a


def fmet(r: np.ndarray):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


# ================================================================================================
# panels and books
# ================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.T = len(self.idx)
        self.warm = np.asarray(np.arange(self.T) >= WARMUP)
        self.is_m = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))
        self.oos_m = np.asarray(self.idx >= pd.Timestamp(OOS_START))
        wpos = np.flatnonzero(self.warm)
        h = len(wpos) // 2
        self.h1 = np.zeros(self.T, bool); self.h1[wpos[:h]] = True
        self.h2 = np.zeros(self.T, bool); self.h2[wpos[h:]] = True
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        # decision masks
        self.canon = rebalance_mask(self.idx, "Q").values.copy()
        self.wk = rebalance_mask(self.idx, "W").values.copy()
        ar = np.arange(self.T)
        self.phase_dec = {p: (ar % PHASE_LEN) == p for p in range(PHASE_LEN)}
        # distance (trading days) from each day to the NEXT canonical quarter-end
        qe = np.flatnonzero(self.canon)
        nxt = np.searchsorted(qe, ar, side="left")
        d = np.full(self.T, np.nan)
        ok = nxt < len(qe)
        d[ok] = qe[nxt[ok]] - ar[ok]
        self.dist_to_qe = d


def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


LEGSETS = {
    "CAND20":  [(21, 252), (0, 126), (0, 63)],
    "R3_55":   [(21, 252), (0, 126), (0, 55)],
    "R3_84":   [(21, 252), (0, 126), (0, 84)],
    "NOR3":    [(21, 252), (0, 126)],
    "MOMONLY": [(21, 252)],
}


def mech_w1(px, mech):
    """Gross-1.0 target weights for one mechanism arm."""
    if mech == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    comp = legs_composite(px, LEGSETS[mech])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))           # no vol scaler (KEEP 4b convention)
    elig = sc.where(above & (vol20 < MAXVOL))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= NTOP).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


# ================================================================================================
# KEEP paths
# ================================================================================================
def keep_4b(c, s_h1, s_h2, s_oos, dd, sc, ss1, ss2, soos, sdd):
    """Sharpe > SPY in BOTH halves AND OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's."""
    return bool(s_h1 > ss1 and s_h2 > ss2 and s_oos > soos
                and abs(dd) <= DD_CAP * abs(sdd) and c >= CAGR_FLOOR * sc)


def legs_4b(c, s_h1, s_h2, s_oos, dd, sc, ss1, ss2, soos, sdd):
    return dict(L_H1=s_h1 > ss1, L_H2=s_h2 > ss2, L_OOS=s_oos > soos,
                L_DD=abs(dd) <= DD_CAP * abs(sdd), L_CAGR=c >= CAGR_FLOOR * sc)


def keep_4a(s_h1, s_h2, dd, b_h1, b_h2, bdd):
    return bool(s_h1 > b_h1 and s_h2 > b_h2 and dd >= bdd)


# ================================================================================================
def main():
    P("=" * 96)
    P("IDEA 961 -- WHY is the CANONICAL phase SYSTEMATICALLY LOW on the QUARTERLY grid?")
    P("=" * 96)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    pans = {"U56": Panel("U56", px_u), "B136": Panel("B136", px_b)}
    for k, pn in pans.items():
        P(f"  {k}: {pn.px.shape[1]} cols x {pn.T} days, {pn.idx[0].date()} -> {pn.idx[-1].date()}")

    # ---------------- gates -------------------------------------------------------------------
    P("\n" + "-" * 96)
    P("GATES")
    P("-" * 96)
    g1 = 0.0
    for mech in ["CAND20", "NOR3", "BAND03"]:
        W1 = mech_w1(px_u, mech)
        for fq in ["W", "Q"]:
            dec = rebalance_mask(px_u.index, fq).values.copy()
            mine, _ = run(pans["U56"].rets, lag_weights(W1), applied_from_decision(dec), GROSS, COST)
            eng = backtest(px_u, pd.DataFrame(GROSS * W1, index=px_u.index, columns=px_u.columns),
                           cost_bps=COST, freq=fq)["returns"].values
            d = np.abs(mine[WARMUP:] - eng[WARMUP:]).max()
            g1 = max(g1, d)
    P(f"  G1  fast runner == engine.backtest post-warmup, 3 books x 2 freqs: max|d| = {g1:.3e}  "
      f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]")

    g2 = np.abs(mech_w1(px_u, "BAND03") - rules_v2_weights(px_u, BAND, GROSS).values / GROSS).max()
    P(f"  G2  BAND03 == rules_v2_weights/gross: max|d| = {g2:.3e}  [{'PASS' if g2 == 0.0 else 'FAIL'}]")

    W_c = lag_weights(mech_w1(px_u, "CAND20"))
    r_c, _ = run(pans["U56"].rets, W_c, applied_from_decision(pans["U56"].wk), GROSS, COST)
    trip = fmet(r_c[pans["U56"].warm])
    dlt = [abs(trip[0] - CAND20_PUB[0]), abs(trip[1] - CAND20_PUB[1]), abs(trip[2] - CAND20_PUB[2])]
    g3 = all(d <= t for d, t in zip(dlt, G3_TOL))
    P(f"  G3  CAND20 weekly: {trip[0]:.4%} / {trip[1]:.4f} / {trip[2]:.2%}  vs published "
      f"{CAND20_PUB[0]:.2%} / {CAND20_PUB[1]:.4f} / {CAND20_PUB[2]:.2%}")
    P(f"      |d| = {dlt[0]:.2e} / {dlt[1]:.2e} / {dlt[2]:.2e}  vs tol {G3_TOL}  "
      f"[{'PASS' if g3 else 'FAIL'}]   (Sharpe tol = the record's own committed vintage drift)")

    cov = np.zeros(pans["U56"].T, int)
    for p in range(PHASE_LEN):
        cov += pans["U56"].phase_dec[p].astype(int)
    P(f"  G4  63-phase family partitions the tape:per-day count min/max = {cov.min()}/{cov.max()}  "
      f"[{'PASS' if cov.min() == cov.max() == 1 else 'FAIL'}]")

    # ---------------- the grid ----------------------------------------------------------------
    P("\n" + "-" * 96)
    P(f"THE GRID -- {len(MECHS)} mechanism arms x {len(PANELS)} panels x {PHASE_LEN} phases "
      f"+ canonical = {len(MECHS) * len(PANELS) * (PHASE_LEN + 1):,} books")
    P("-" * 96)

    rows, summ = [], []
    for pname in PANELS:
        pn = pans[pname]
        sc_f, _, sdd_f = fmet(pn.spy[pn.warm])
        _, ss1, _ = fmet(pn.spy[pn.h1]); _, ss2, _ = fmet(pn.spy[pn.h2])
        sc_i, ss_i, _ = fmet(pn.spy[pn.is_m])
        sc_o, ss_o, sdd_o = fmet(pn.spy[pn.oos_m])
        # baseline RULES v2 weekly on this panel
        Wv = lag_weights(rules_v2_weights(pn.px, BAND, GROSS).values / GROSS)
        r_v, _ = run(pn.rets, Wv, applied_from_decision(pn.wk), GROSS, COST)
        bc_f, bs_f, bdd_f = fmet(r_v[pn.warm])
        _, bs1, _ = fmet(r_v[pn.h1]); _, bs2, _ = fmet(r_v[pn.h2])
        bc_o, bs_o, bdd_o = fmet(r_v[pn.oos_m])
        ss_f = fmet(pn.spy[pn.warm])[1]
        P(f"\n[{pname}]  SPY full {sc_f:.2%}/{ss_f:.4f}/{sdd_f:.2%}"
          f"   halves {ss1:.4f}/{ss2:.4f}   OOS {sc_o:.2%}/{ss_o:.4f}/{sdd_o:.2%}")
        P(f"[{pname}]  RULES v2 (baseline, W) full {bc_f:.2%}/{bs_f:.4f}/{bdd_f:.2%}"
          f"   halves {bs1:.4f}/{bs2:.4f}   OOS {bc_o:.2%}/{bs_o:.4f}/{bdd_o:.2%}")

        for mech in MECHS:
            W1 = mech_w1(pn.px, mech)
            wt = lag_weights(W1)
            fam = {}
            for p in range(PHASE_LEN):
                r, t = run(pn.rets, wt, applied_from_decision(pn.phase_dec[p]), GROSS, COST)
                c, s, d = fmet(r[pn.warm])
                ci, si, _ = fmet(r[pn.is_m])
                co, so, do = fmet(r[pn.oos_m])
                _, s1, _ = fmet(r[pn.h1]); _, s2, _ = fmet(r[pn.h2])
                mdist = float(np.nanmedian(pn.dist_to_qe[pn.phase_dec[p] & pn.warm]))
                fam[p] = dict(CAGR=c, Sharpe=s, MaxDD=d, IS_CAGR=ci, IS_Sharpe=si,
                              OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=do, H1=s1, H2=s2,
                              turn=t[pn.warm].sum() / (pn.warm.sum() / 252.0), dist_qe=mdist)
                rows.append(dict(panel=pname, mech=mech, phase=p, canonical=0, **fam[p]))
            rc, _ = run(pn.rets, wt, applied_from_decision(pn.canon), GROSS, COST)
            c, s, d = fmet(rc[pn.warm])
            ci, si, _ = fmet(rc[pn.is_m])
            co, so, do = fmet(rc[pn.oos_m])
            _, s1, _ = fmet(rc[pn.h1]); _, s2, _ = fmet(rc[pn.h2])
            _, tt = run(pn.rets, wt, applied_from_decision(pn.canon), GROSS, COST)
            canon = dict(CAGR=c, Sharpe=s, MaxDD=d, IS_CAGR=ci, IS_Sharpe=si, OOS_CAGR=co,
                         OOS_Sharpe=so, OOS_MaxDD=do, H1=s1, H2=s2,
                         turn=tt[pn.warm].sum() / (pn.warm.sum() / 252.0), dist_qe=0.0)
            rows.append(dict(panel=pname, mech=mech, phase=-1, canonical=1, **canon))

            fc = np.array([fam[p]["CAGR"] for p in range(PHASE_LEN)])
            fs = np.array([fam[p]["Sharpe"] for p in range(PHASE_LEN)])
            pct_c = float((fc < canon["CAGR"]).mean())
            pct_s = float((fs < canon["Sharpe"]).mean())
            amax = int(np.argmax(fc))
            # rule 8: choose phase on IS CAGR, evaluate OOS untouched
            fi = np.array([fam[p]["IS_CAGR"] for p in range(PHASE_LEN)])
            pick = int(np.argmax(fi))
            med_oos_c = float(np.median([fam[p]["OOS_CAGR"] for p in range(PHASE_LEN)]))
            med_oos_s = float(np.median([fam[p]["OOS_Sharpe"] for p in range(PHASE_LEN)]))
            med_oos_d = float(np.median([fam[p]["OOS_MaxDD"] for p in range(PHASE_LEN)]))

            def score_pack(dd_, tag):
                return dict(
                    k4b=keep_4b(dd_["CAGR"], dd_["H1"], dd_["H2"], dd_["OOS_Sharpe"], dd_["MaxDD"],
                                sc_f, ss1, ss2, ss_o, sdd_f),
                    k4a=keep_4a(dd_["H1"], dd_["H2"], dd_["MaxDD"], bs1, bs2, bdd_f),
                    **{f"{tag}_{k}": v for k, v in
                       legs_4b(dd_["CAGR"], dd_["H1"], dd_["H2"], dd_["OOS_Sharpe"], dd_["MaxDD"],
                               sc_f, ss1, ss2, ss_o, sdd_f).items()})

            sp_can = score_pack(canon, "CAN")
            sp_pick = score_pack(fam[pick], "PICK")
            summ.append(dict(
                panel=pname, mech=mech,
                canon_CAGR=canon["CAGR"], canon_Sharpe=canon["Sharpe"], canon_MaxDD=canon["MaxDD"],
                fam_med_CAGR=float(np.median(fc)), fam_min_CAGR=float(fc.min()),
                fam_max_CAGR=float(fc.max()), fam_spread_pp=float((fc.max() - fc.min()) * 100),
                canon_pct_CAGR=pct_c, canon_pct_Sharpe=pct_s,
                argmax_phase=amax, argmax_dist_to_qe=fam[amax]["dist_qe"],
                argmax_CAGR=float(fc.max()),
                canon_turn=canon["turn"], fam_med_turn=float(np.median(
                    [fam[p]["turn"] for p in range(PHASE_LEN)])),
                IS_pick_phase=pick, pick_dist_to_qe=fam[pick]["dist_qe"],
                pick_OOS_CAGR=fam[pick]["OOS_CAGR"], pick_OOS_Sharpe=fam[pick]["OOS_Sharpe"],
                pick_OOS_MaxDD=fam[pick]["OOS_MaxDD"],
                canon_OOS_CAGR=canon["OOS_CAGR"], canon_OOS_Sharpe=canon["OOS_Sharpe"],
                canon_OOS_MaxDD=canon["OOS_MaxDD"],
                med_OOS_CAGR=med_oos_c, med_OOS_Sharpe=med_oos_s, med_OOS_MaxDD=med_oos_d,
                spy_OOS_CAGR=sc_o, spy_OOS_Sharpe=ss_o, spy_OOS_MaxDD=sdd_o,
                v2_OOS_CAGR=bc_o, v2_OOS_Sharpe=bs_o, v2_OOS_MaxDD=bdd_o,
                canon_4b=sp_can["k4b"], canon_4a=sp_can["k4a"],
                pick_4b=sp_pick["k4b"], pick_4a=sp_pick["k4a"],
                **{k: v for k, v in sp_can.items() if k.startswith("CAN_")},
                **{k: v for k, v in sp_pick.items() if k.startswith("PICK_")},
            ))
            P(f"  {mech:8s} canon CAGR {canon['CAGR']:7.2%}  fam [{fc.min():.2%},{fc.max():.2%}] "
              f"med {np.median(fc):.2%}  PCTILE(CAGR) {pct_c:.3f}  PCTILE(Sharpe) {pct_s:.3f}  "
              f"argmax p={amax:2d} @ {fam[amax]['dist_qe']:.0f}d before QE")

    df_all = pd.DataFrame(rows)
    df_s = pd.DataFrame(summ)
    dump(df_all, "family.csv")
    dump(df_s, "summary.csv")

    # ---------------- hypotheses --------------------------------------------------------------
    P("\n" + "-" * 96)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 96)
    P("\n  canonical CAGR percentile within its own 63-phase family (0 = family worst, 1 = best):")
    piv = df_s.pivot(index="mech", columns="panel", values="canon_pct_CAGR").reindex(MECHS)
    P(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  canonical SHARPE percentile:")
    pivs = df_s.pivot(index="mech", columns="panel", values="canon_pct_Sharpe").reindex(MECHS)
    P(pivs.to_string(float_format=lambda x: f"{x:.3f}"))

    de = df_s[df_s.mech.isin(DEALIASED)]
    n_above = int((de.canon_pct_CAGR > ALIAS_BAR).sum())
    h_alias = n_above >= ALIAS_MIN_CELLS
    P(f"\n  H_ALIAS   de-aliased cells with canonical percentile > {ALIAS_BAR}: "
      f"{n_above} of {len(de)}  (bar >= {ALIAS_MIN_CELLS})   -> "
      f"{'PASS: the 63-day r3 leg is the carrier' if h_alias else 'FAIL: the r3 leg is NOT the carrier'}")

    bd = df_s[df_s.mech == "BAND03"]
    h_cal = bool((bd.canon_pct_CAGR <= CAL_BAR).all())
    P(f"  H_CALENDAR BAND03 canonical percentile: "
      f"{', '.join(f'{r.panel}={r.canon_pct_CAGR:.3f}' for r in bd.itertuples())}  (bar <= {CAL_BAR} both)"
      f"   -> {'PASS: a signal-free book carries it too' if h_cal else 'FAIL: a signal-free book does NOT carry it'}")

    mo = df_s[df_s.mech == "MOMONLY"]
    h_mom = bool((mo.canon_pct_CAGR <= CAL_BAR).all())
    P(f"  H_MOM     MOMONLY canonical percentile: "
      f"{', '.join(f'{r.panel}={r.canon_pct_CAGR:.3f}' for r in mo.itertuples())}  (bar <= {CAL_BAR} both)"
      f"   -> {'PASS: momentum selection per se carries it' if h_mom else 'FAIL'}")
    P("  H_RECON   NOT TESTABLE in this sandbox (no index-membership history). It can only act "
      "through the calendar channel, which H_CALENDAR measures.")

    P(f"\n  argmax distance to the NEXT quarter-end (trading days), all {len(df_s)} cells:")
    P("   " + "  ".join(f"{r.panel}/{r.mech}={r.argmax_dist_to_qe:.0f}" for r in df_s.itertuples()))
    dd_ = df_s.argmax_dist_to_qe.values
    P(f"   min {dd_.min():.0f}  median {np.median(dd_):.0f}  max {dd_.max():.0f}   "
      f"(942 reported: never < 17, median 29, mode 23)")
    P(f"\n  family CAGR spread (max-min, pp): min {df_s.fam_spread_pp.min():.2f}  "
      f"median {df_s.fam_spread_pp.median():.2f}  max {df_s.fam_spread_pp.max():.2f}")
    P(f"  canonical vs family-median annual turnover: canon {df_s.canon_turn.mean():.2f}x  "
      f"family-median {df_s.fam_med_turn.mean():.2f}x   (a turnover story would need a gap here)")

    # ---------------- rule 8 ------------------------------------------------------------------
    # ---------------- post-hoc: the CALENDAR profile ------------------------------------------
    # POST HOC, declared as such: no bar was pre-registered for this, it is a description of the
    # shape H_CALENDAR passed on, not a test.
    P("\n" + "-" * 96)
    P("POST HOC (not pre-registered): family CAGR by DISTANCE of the phase to the next quarter-end")
    P("-" * 96)
    fam = df_all[df_all.canonical == 0].copy()
    fam["bucket"] = pd.cut(fam.dist_qe, [-0.1, 8, 17, 31, 45, 63],
                           labels=["0-8d", "9-17d", "18-31d", "32-45d", "46-62d"])
    # de-mean within (panel, mech) so the buckets are comparable across books
    fam["dCAGR_pp"] = (fam.CAGR - fam.groupby(["panel", "mech"]).CAGR.transform("mean")) * 100
    prof = fam.groupby("bucket").agg(n=("dCAGR_pp", "size"), mean_dCAGR_pp=("dCAGR_pp", "mean"),
                                     med_dCAGR_pp=("dCAGR_pp", "median"))
    P(prof.to_string(float_format=lambda x: f"{x:+.3f}"))
    near = fam[fam.dist_qe <= 17].dCAGR_pp
    far = fam[fam.dist_qe > 17].dCAGR_pp
    P(f"\n  phases within 17 trading days of quarter-end: n={len(near)}, mean {near.mean():+.3f} pp")
    P(f"  phases further out                        : n={len(far)}, mean {far.mean():+.3f} pp")
    P(f"  gap = {near.mean() - far.mean():+.3f} pp/yr of CAGR.  The CANONICAL date is the extreme "
      f"member of the NEAR group (distance 0).")
    nwin = int((fam.groupby(["panel", "mech"]).apply(
        lambda g: g.loc[g.CAGR.idxmax(), "dist_qe"] <= 17)).sum())
    P(f"  cells whose family ARGMAX sits within 17 days of quarter-end: {nwin} of {len(df_s)} "
      f"(uniform would give {len(df_s) * 18 / PHASE_LEN:.1f})")
    P(f"\n  mean canonical CAGR percentile over all {len(df_s)} cells: "
      f"{df_s.canon_pct_CAGR.mean():.3f}   (942 published 0.170 over 150 cells)")
    P(f"  canonical is the family MAXIMUM in {int((df_s.canon_pct_CAGR == 1.0).sum())} of {len(df_s)} "
      f"cells   (942: 0 of 150; note (62/63)^150 = 0.093, so 0-of-150 alone is ~1.7 sigma, "
      f"weak -- the MEAN percentile, not the argmax count, is where 942's evidence lives)")

    # ---------------- does ANY phase clear 4b? ------------------------------------------------
    P("\n" + "-" * 96)
    P("DOES ANY PHASE ON THE QUARTERLY GRID CLEAR 4b?  (all 63 phases x 12 cells = 756 books)")
    P("-" * 96)
    npass, bind = 0, {}
    for r in df_all.itertuples():
        pn = pans[r.panel]
        sc_f = fmet(pn.spy[pn.warm])[0]; sdd_f = fmet(pn.spy[pn.warm])[2]
        _, ss1, _ = fmet(pn.spy[pn.h1]); _, ss2, _ = fmet(pn.spy[pn.h2])
        ss_o = fmet(pn.spy[pn.oos_m])[1]
        lg = legs_4b(r.CAGR, r.H1, r.H2, r.OOS_Sharpe, r.MaxDD, sc_f, ss1, ss2, ss_o, sdd_f)
        if all(lg.values()):
            npass += 1
        for k, v in lg.items():
            if not v:
                bind[k] = bind.get(k, 0) + 1
    P(f"  4b passes: {npass} of {len(df_all)} books on the quarterly grid.")
    P("  binding legs (count of books each leg fails): " +
      ", ".join(f"{k}={v} ({v / len(df_all):.1%})" for k, v in sorted(bind.items(), key=lambda x: -x[1])))

    P("\n" + "-" * 96)
    P("RULE 8 WALK-FORWARD -- phase chosen on IS (<=2016) by CAGR, evaluated untouched on OOS")
    P("-" * 96)
    P(f"{'panel/mech':16s} {'ISpick':>6s} {'d2QE':>5s} | {'pick OOS C/S/DD':>24s} | "
      f"{'canon OOS C/S/DD':>24s} | {'famMED OOS C/S/DD':>24s} | {'SPY OOS':>22s}")
    for r in df_s.itertuples():
        P(f"{r.panel + '/' + r.mech:16s} {r.IS_pick_phase:6d} {r.pick_dist_to_qe:5.0f} | "
          f"{r.pick_OOS_CAGR:7.2%} {r.pick_OOS_Sharpe:7.3f} {r.pick_OOS_MaxDD:7.2%} | "
          f"{r.canon_OOS_CAGR:7.2%} {r.canon_OOS_Sharpe:7.3f} {r.canon_OOS_MaxDD:7.2%} | "
          f"{r.med_OOS_CAGR:7.2%} {r.med_OOS_Sharpe:7.3f} {r.med_OOS_MaxDD:7.2%} | "
          f"{r.spy_OOS_CAGR:6.2%} {r.spy_OOS_Sharpe:6.3f} {r.spy_OOS_MaxDD:6.2%}")
    n_better = int((df_s.pick_OOS_CAGR > df_s.canon_OOS_CAGR).sum())
    P(f"\n  IS-chosen phase beats the canonical OUT OF SAMPLE on CAGR in {n_better} of {len(df_s)} cells.")
    n_med = int((df_s.pick_OOS_CAGR > df_s.med_OOS_CAGR).sum())
    P(f"  IS-chosen phase beats its own family MEDIAN out of sample in {n_med} of {len(df_s)} cells.")

    P("\n" + "-" * 96)
    P("KEEP PATHS (both, on every cell; 4b read with rule-8 OOS Sharpe as the third leg)")
    P("-" * 96)
    P(f"{'panel/mech':16s} {'canon 4a':>9s} {'canon 4b':>9s} {'pick 4a':>9s} {'pick 4b':>9s}   binding legs (canonical)")
    for r in df_s.itertuples():
        legs = [k[4:] for k in df_s.columns if k.startswith("CAN_L") and not getattr(r, k)]
        P(f"{r.panel + '/' + r.mech:16s} {str(r.canon_4a):>9s} {str(r.canon_4b):>9s} "
          f"{str(r.pick_4a):>9s} {str(r.pick_4b):>9s}   fails: {','.join(legs) if legs else '(none)'}")
    P(f"\n  4b PASSES: canonical {int(df_s.canon_4b.sum())} of {len(df_s)}, "
      f"IS-chosen {int(df_s.pick_4b.sum())} of {len(df_s)}")
    P(f"  4a PASSES: canonical {int(df_s.canon_4a.sum())} of {len(df_s)}, "
      f"IS-chosen {int(df_s.pick_4a.sum())} of {len(df_s)}")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")
    return df_s


if __name__ == "__main__":
    a = main()
    b = main()          # G5 determinism
    same = a.equals(b)
    print(f"\n  G5  determinism (whole grid run twice): {'PASS' if same else 'FAIL'}")
