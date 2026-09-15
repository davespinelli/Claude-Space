#!/usr/bin/env python3
"""Idea 942 (cloud, 2026-09-15) -- is the 4b OOS-SHARPE LEG DEAD on any MONTHLY U56 CELL?

THE PRIOR RESULT (idea 931, committed)
  100.0% of 500 gross-matched coin flips clear SPY's OOS Sharpe on U56 MONTHLY (null median
  1.125 against SPY's 0.874), against 8.8% on the SAME panel weekly.  A leg that every draw
  passes certifies nothing.  931 measured one cell; PROTOCOL 4b reads that leg on every
  candidate.

WHAT THIS RUN DOES
  Measures the base rate at which a gross-matched coin flip clears EACH of 4b's five legs
  SEPARATELY -- not just the joint verdict -- across a cadence x panel grid, all three null kinds,
  and asks the question the joint base rate cannot answer: WHICH LEG is doing the certifying,
  and is any of them dead?

  It also asks a question 931 did not, and the answer turns out to matter more than the cadence
  finding: **4b's three Sharpe legs are H1, H2 and OOS, but the record's H2 window and its
  rule-8 OOS window are nearly the SAME DATES.**  The full sample starts at the warm-up (2009)
  and ends 2026, so the halfway point falls in late 2017; OOS starts 2017-01-01.  If those two
  legs overlap, 4b's "both halves AND out-of-sample" is closer to a two-leg test than a
  three-leg one, and the OOS leg is redundant rather than merely weak.  Both are measured.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_DEAD        the OOS-Sharpe leg is DEAD on U56 monthly.
                PASS iff the RANDROT base rate for L_OOS on U56/M is >= 0.90 (931 read 100.0%).
  H_CADENCE     the leg's base rate rises monotonically with holding length.
                PASS iff base_rate(W) < base_rate(M) < base_rate(Q) on BOTH panels, RANDROT.
  H_REDUNDANT   the OOS leg adds < 5% of discriminating power beyond the H2 leg.
                PASS iff P(all 5 legs) / P(the other 4 legs) >= 0.95 on >= 5 of the 6 cells,
                RANDROT.  (A leg that never changes the verdict is redundant whatever its own
                base rate.)
  H_LIVE        at least one leg is genuinely discriminating everywhere.
                PASS iff some leg has base rate <= 0.25 in ALL 6 cells, RANDROT.

TWO TUNED DIALS, ALL GRID POINTS REPORTED
  CADENCE  {W, M, Q}                        -- 3 levels
  PANEL    {U56, B136}                      -- 2 levels
  NULL KIND {RANDROT, RANDFIX, RANDROT_FREE} is NOT a tuned dial: all THREE are always
  reported side by side and none is ever chosen, because the record has already committed (CHANGELOG 2026-09-15) that
  the kind moves a joint base rate from 74.8% to 0.2% on one cell -- there is no such thing as
  *the* coin-flip base rate, and a headline that picks one is not a measurement.
  Everything else is a REPORTED CONSTANT: gross 0.75, cost 10 bps, lag 1, warm-up 260, n=20,
  max_vol 0.60, 200d gate, 250 draws per (cell, kind), md5-derived seeds.
  THE FIRST TWO NULL KINDS DRAW THROUGH THE BOOK'S OWN ELIGIBILITY GATE (above the 200d MA,
  vol20 < 0.60), which is the record's convention: the gate is held in common so the null prices
  the SCORE alone.  RANDROT_FREE drops the gate and is reported beside them, because a gated
  null cannot say what the gate itself is worth and 4b is read on the whole book.

RULE 8 (walk-forward), on the real books
  CADENCE is chosen on the IS window (<= 2016-12-31) by Sharpe and evaluated untouched on OOS
  (>= 2017-01-01), for CAND20 (the 2026-09-04 KEEP 4b candidate) and BAND03 (live RULES v2), on
  both panels.  OOS CAGR/Sharpe/MaxDD are reported against the RULES v2 baseline and SPY, and
  BOTH KEEP paths are scored -- each with its own cell's null base rate printed beside it.

GATES
  G1  closed-form runner == `engine.backtest` @10 bps post-warm-up, 2 books x 3 cadences.
      Bar 1e-12.  G1b the same, against a literal transcription of the engine's day loop.
  G2  BAND03 weights == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CAND20 weekly reproduces the 2026-09-04 committed triple at the record's own vintage
      tolerance (the Sharpe bar is the record's KNOWN, committed drift; the miss is printed).
  G4  GROSS MATCH: every null's target gross and holding count equal the book's on every
      rebalance day (bar 0.0 exact) AND the null's realised annual turnover is > 0.5x.  The
      turnover leg exists because the FIRST CUT OF THIS RUN wrote the draw on the APPLICATION
      rows rather than the DECISION rows; `lag_weights` then rolled it off the rebalance days and
      every null sat in pure cash, with every other gate still passing.  The record logged the
      identical defect on 2026-09-15 and the gate is copied from it.
  G5  SEED REPRODUCIBILITY: the same md5-derived seed regenerates a draw bit-for-bit, so the
      draw streams are nested and base rates at different budgets are comparable.
  G6  determinism: the whole grid runs twice, tables identical.

SURVIVORSHIP: U56 and B136 are CURRENT-constituent lists.  A coin flip drawn from a survivor
panel is a BETTER book than one drawn in real time, so **every base rate reported here is an
UPPER bound** -- which cuts AGAINST this run's own headline (a dead leg would be even deader
in real time is the wrong direction; the honest statement is that a leg measured live could
have a LOWER base rate than printed, so "dead" claims are the ones to treat as upper bounds).
The cadence and leg contrasts are same-tape, same-names comparisons and survive it; the 4b
LEVELS are read against SPY and are not protected.

COSTS 10 bps per unit turnover, weights decided at close t applied at close t+1 (PROTOCOL 2).
"""
from __future__ import annotations

import hashlib
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

COST, GROSS, LAG, WARMUP = 10.0, 0.75, 1, 260
NTOP, MAXVOL, BAND = 20, 0.60, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
DRAWS = 250
PANELS = ["U56", "B136"]
CADENCES = ["W", "M", "Q"]
KINDS = ["RANDROT", "RANDFIX", "RANDROT_FREE"]
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
BOOKS = ["CAND20", "BAND03"]

DEAD_BAR = 0.90          # H_DEAD
REDUND_BAR, REDUND_CELLS = 0.95, 5   # H_REDUNDANT
LIVE_BAR = 0.25          # H_LIVE

CAND20_PUB = (0.1266, 1.0921, -0.1831)
G3_TOL = (5e-3, 3.3e-2, 5e-3)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts) -> int:
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:16], 16) % (2**32)


# ================================================================================================
# runner (gated at G1)
# ================================================================================================
def run_ref(rets, wt, applied, gross, cost):
    """Literal transcription of `engine.backtest`'s day loop. Kept only as G1b's reference."""
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


class Ctx:
    """Closed-form equivalent of the day loop, for ONE rebalance schedule.

    Between two rebalances nothing is traded, so each holding's dollar value grows with its own
    price and the cash sleeve is constant.  The held weight on day i is therefore
        held[i,j] = g*A[i,j]*R[i,j] / V[i],   R[i,j] = price_j(i) / price_j(s0[i]),
        V[i]     = 1 + g*(sum_j A[i,j]*R[i,j] - sum_j A[i,j]),
    where A[i] is the target set at the last rebalance s0[i].  Turnover on a rebalance day is
    read against the weights that DRIFTED in from the previous one.  Identical numbers to the
    loop, ~100x faster; the equality is gated at G1 against `engine.backtest` itself and at G1b
    against `run_ref`."""

    def __init__(self, rets, applied):
        T, N = rets.shape
        self.rets, self.T = rets, T
        C = np.cumprod(1.0 + rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])       # asset value at the START of day i
        self.reb = np.flatnonzero(applied)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]

    def run(self, wt, gross, cost):
        A = wt[self.s0]
        AR = A * self.R
        V = 1.0 + gross * (AR.sum(axis=1) - A.sum(axis=1))
        port = gross * (AR * self.rets).sum(axis=1) / V
        Ap = wt[self.s0p[self.reb]]
        ARp = Ap * self.Rp
        Vp = 1.0 + gross * (ARp.sum(axis=1) - Ap.sum(axis=1))
        heldp = gross * ARp / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(gross * wt[self.reb] - heldp).sum(axis=1)
        return port - turn * cost / 1e4, turn


def lag_weights(W1):
    wt = np.roll(W1, LAG, axis=0).copy()
    wt[:LAG] = 0.0
    return wt


def applied_from_decision(dec):
    a = np.roll(dec, LAG)
    a[:LAG] = False
    a[0] = True
    return a


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


# ================================================================================================
class Panel:
    def __init__(self, name, px):
        self.name, self.px, self.idx = name, px, px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.T = len(self.idx)
        self.warm = np.arange(self.T) >= WARMUP
        self.oos_m = np.asarray(self.idx >= pd.Timestamp(OOS_START))
        self.is_m = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))
        wpos = np.flatnonzero(self.warm)
        h = len(wpos) // 2
        self.h1 = np.zeros(self.T, bool); self.h1[wpos[:h]] = True
        self.h2 = np.zeros(self.T, bool); self.h2[wpos[h:]] = True
        self.h2_start = self.idx[wpos[h]]
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.priced = px.notna().values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < MAXVOL) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        # SPY reference legs
        self.spy_c, self.spy_s, self.spy_dd = fmet(self.spy[self.warm])
        self.spy_h1 = fmet(self.spy[self.h1])[1]
        self.spy_h2 = fmet(self.spy[self.h2])[1]
        self.spy_oos_c, self.spy_oos_s, self.spy_oos_dd = fmet(self.spy[self.oos_m])


def legs_of(pn, r):
    c, s, dd = fmet(r[pn.warm])
    return dict(L_H1=fmet(r[pn.h1])[1] > pn.spy_h1,
                L_H2=fmet(r[pn.h2])[1] > pn.spy_h2,
                L_OOS=fmet(r[pn.oos_m])[1] > pn.spy_oos_s,
                L_DD=abs(dd) <= DD_CAP * abs(pn.spy_dd),
                L_CAGR=c >= CAGR_FLOOR * pn.spy_c), (c, s, dd)


def book_w1(px, book):
    if book == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    mom = (px.shift(21) / px.shift(252) - 1).rank(axis=1, pct=True)
    r6 = (px / px.shift(126) - 1).rank(axis=1, pct=True)
    r3 = (px / px.shift(63) - 1).rank(axis=1, pct=True)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = ((mom + r6 + r3) / 3) * (0.5 + 0.5 * above.astype(float))
    rank = sc.where(above & (vol20 < MAXVOL)).rank(axis=1, ascending=False)
    sel = (rank <= NTOP).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


def draw_null(buf, pn, W1, dec, kind, rng, fixed_order=None):
    """Fill `buf` with a GROSS-MATCHED coin flip.  On every APPLIED day it holds exactly as many
    equally weighted names as the book holds that day, so target gross and holding count match
    the book exactly (gated at G4).

      RANDROT       draws k fresh names at random from the names that pass the BOOK'S OWN
                    eligibility gate that day (above the 200d MA, vol20 < 0.60).  This is the
                    record's convention and it is the null that isolates the SCORE: the gate is
                    held in common, only the ranking is randomised.
      RANDFIX       draws ONE random preference ordering of the panel at the start and, at every
                    rebalance, takes the top k eligible names under that fixed ordering.  Same
                    gate, same counts, but no rotation -- the record's RANDFIX.
      RANDROT_FREE  draws k fresh names from every name PRICED that day, gate and all.  This is
                    the null that isolates GATE + SCORE together, and it is reported because a
                    gated null cannot tell you what the gate itself is worth.
    """
    buf[:] = 0.0
    kcount = (W1 > 0).sum(axis=1)
    days = np.flatnonzero(dec)      # DECISION rows -- `lag_weights` supplies the t+1 roll.
    for i in days:                  # Writing on the APPLICATION rows instead leaves the book in
        pass                        # pure cash; that is what G4's turnover leg is there to catch.
    for i in days:
        k = int(kcount[i])
        if k == 0:
            continue
        pool = np.flatnonzero(pn.priced[i] if kind == "RANDROT_FREE" else pn.elig[i])
        if len(pool) == 0:
            pool = np.flatnonzero(pn.priced[i])
        if len(pool) == 0:
            continue
        k = min(k, len(pool))
        if kind == "RANDFIX":
            order = fixed_order[pool]
            pick = pool[np.argsort(order)[:k]]
        else:
            pick = rng.choice(pool, size=k, replace=False)
        buf[i, pick] = 1.0 / len(pick)
    return buf


def main(draws=DRAWS, verbose=True):
    LOG.clear()
    P("=" * 96)
    P("IDEA 942 -- is the 4b OOS-SHARPE LEG DEAD on any MONTHLY U56 CELL?")
    P("=" * 96)
    px_u, px_b = load_universe(), load_universe(broad=True)
    pans = {"U56": Panel("U56", px_u), "B136": Panel("B136", px_b)}
    W1 = {(p, b): book_w1(pans[p].px, b) for p in PANELS for b in BOOKS}

    # ---------------- gates -------------------------------------------------------------------
    P("\n" + "-" * 96)
    P("GATES")
    P("-" * 96)
    g1 = g1r = 0.0
    for b in BOOKS:
        for c in CADENCES:
            mine, _ = pans["U56"].ctx[c].run(lag_weights(W1[("U56", b)]), GROSS, COST)
            ref, _ = run_ref(pans["U56"].rets, lag_weights(W1[("U56", b)]), pans["U56"].app[c], GROSS, COST)
            eng = backtest(px_u, pd.DataFrame(GROSS * W1[("U56", b)], index=px_u.index,
                                              columns=px_u.columns), cost_bps=COST, freq=c)["returns"].values
            g1 = max(g1, np.abs(mine[WARMUP:] - eng[WARMUP:]).max())
            g1r = max(g1r, np.abs(mine[WARMUP:] - ref[WARMUP:]).max())
    P(f"  G1  closed-form Ctx.run == engine.backtest, 2 books x 3 cadences: max|d| = {g1:.3e}  "
      f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]")
    P(f"  G1b closed-form Ctx.run == the literal day loop `run_ref`: max|d| = {g1r:.3e}  "
      f"[{'PASS' if g1r < 1e-12 else 'FAIL'}]")
    g2 = np.abs(W1[("U56", "BAND03")] - rules_v2_weights(px_u, BAND, GROSS).values / GROSS).max()
    P(f"  G2  BAND03 == rules_v2_weights/gross: {g2:.3e}  [{'PASS' if g2 == 0.0 else 'FAIL'}]")
    rc, _ = pans["U56"].ctx["W"].run(lag_weights(W1[("U56", "CAND20")]), GROSS, COST)
    tr = fmet(rc[pans["U56"].warm])
    dl = [abs(tr[i] - CAND20_PUB[i]) for i in range(3)]
    P(f"  G3  CAND20 weekly {tr[0]:.4%} / {tr[1]:.4f} / {tr[2]:.2%} vs published "
      f"{CAND20_PUB[0]:.2%} / {CAND20_PUB[1]:.4f} / {CAND20_PUB[2]:.2%}; |d| = "
      f"{dl[0]:.2e} / {dl[1]:.2e} / {dl[2]:.2e}  "
      f"[{'PASS' if all(d <= t for d, t in zip(dl, G3_TOL)) else 'FAIL'}]  "
      f"(Sharpe tol 3.3e-2 = the record's own committed vintage drift)")

    # G4 gross match, G5 nesting
    pn = pans["U56"]; buf = np.zeros_like(pn.rets)
    w = W1[("U56", "CAND20")]; dec = pn.dec["M"]; app = pn.app["M"]
    gm = 0.0; km = 0; tmin = 1e9
    for d in range(5):
        rg = np.random.default_rng(seed_of("U56", "M", "RANDROT", d))
        n = draw_null(buf, pn, w, dec, "RANDROT", rg)
        gm = max(gm, np.abs(n[dec].sum(axis=1) - w[dec].sum(axis=1)).max())
        km = max(km, int(np.abs((n[dec] > 0).sum(axis=1) - (w[dec] > 0).sum(axis=1)).max()))
        rr, tt = pn.ctx["M"].run(lag_weights(n), GROSS, COST)
        tmin = min(tmin, tt[pn.warm].sum() / (pn.warm.sum() / 252.0))
    P(f"  G4  gross match on 5 draws: max|d gross| = {gm:.3e}, max|d holding count| = {km}, "
      f"min realised annual turnover = {tmin:.2f}x  "
      f"[{'PASS' if gm < 1e-12 and km == 0 and tmin > 0.5 else 'FAIL'}]")
    P("      (the turnover leg exists because the first cut of this run wrote the draw on the "
      "APPLICATION\n       rows; every other gate passed while the null sat in pure cash)")
    a = draw_null(buf.copy(), pn, w, dec, "RANDROT", np.random.default_rng(seed_of("U56", "M", "RANDROT", 7)))
    b_ = draw_null(np.zeros_like(pn.rets), pn, w, dec, "RANDROT",
                   np.random.default_rng(seed_of("U56", "M", "RANDROT", 7)))
    del rg
    P(f"  G5  draw nesting / seed reproducibility: max|d| = {np.abs(a - b_).max():.3e}  "
      f"[{'PASS' if np.abs(a - b_).max() == 0.0 else 'FAIL'}]")

    # ---------------- the H2 / OOS window overlap ---------------------------------------------
    P("\n" + "-" * 96)
    P("THE WINDOW OVERLAP THAT 4b's THIRD LEG SITS ON")
    P("-" * 96)
    for p in PANELS:
        pn = pans[p]
        both = int((pn.h2 & pn.oos_m).sum())
        P(f"  {p}: H2 runs {pn.h2_start.date()} -> {pn.idx[-1].date()} ({int(pn.h2.sum())} days); "
          f"OOS runs {OOS_START} -> {pn.idx[-1].date()} ({int(pn.oos_m.sum())} days); "
          f"overlap {both} days = {both / pn.oos_m.sum():.1%} of OOS and {both / pn.h2.sum():.1%} of H2")

    # ---------------- the null grid -----------------------------------------------------------
    P("\n" + "-" * 96)
    P(f"NULL GRID -- {len(PANELS)} panels x {len(CADENCES)} cadences x {len(KINDS)} null kinds x "
      f"{draws} draws = {len(PANELS) * len(CADENCES) * len(KINDS) * draws:,} coin-flip books")
    P("-" * 96)
    rows = []
    for p in PANELS:
        pn = pans[p]
        buf = np.zeros_like(pn.rets)
        w = W1[(p, "CAND20")]
        for c in CADENCES:
            app, dec = pn.app[c], pn.dec[c]
            for kind in KINDS:
                rng = np.random.default_rng(seed_of(p, c, kind, "stream"))
                for d in range(draws):
                    fo = (np.random.default_rng(seed_of(p, c, kind, "order", d))
                          .random(pn.rets.shape[1]) if kind == "RANDFIX" else None)
                    nw = draw_null(buf, pn, w, dec, kind, rng, fo)
                    r, t = pn.ctx[c].run(lag_weights(nw), GROSS, COST)
                    lg, (cg, sh, dd) = legs_of(pn, r)
                    rows.append(dict(panel=p, cadence=c, kind=kind, draw=d, CAGR=cg, Sharpe=sh,
                                     MaxDD=dd, OOS_Sharpe=fmet(r[pn.oos_m])[1],
                                     turn=t[pn.warm].sum() / (pn.warm.sum() / 252.0), **lg))
    nul = pd.DataFrame(rows)
    nul["pass4b"] = nul[LEGS].all(axis=1)
    nul["pass_no_OOS"] = nul[[l for l in LEGS if l != "L_OOS"]].all(axis=1)
    dump(nul, "nulls.csv")

    br = nul.groupby(["panel", "cadence", "kind"])[LEGS + ["pass4b", "pass_no_OOS"]].mean().reset_index()
    br["med_turn"] = nul.groupby(["panel", "cadence", "kind"]).turn.median().values
    br["med_OOS_Sharpe"] = nul.groupby(["panel", "cadence", "kind"]).OOS_Sharpe.median().values
    dump(br, "baserates.csv")

    P("\n  PER-LEG BASE RATE = fraction of gross-matched coin flips that CLEAR that 4b leg")
    P(f"  {'panel':5s} {'cad':3s} {'kind':8s} " + " ".join(f"{l:>7s}" for l in LEGS) +
      f" {'4b':>7s} {'4b-noOOS':>9s} {'turn':>6s} {'medOOSs':>8s}")
    for r in br.itertuples():
        P(f"  {r.panel:5s} {r.cadence:3s} {r.kind:8s} " +
          " ".join(f"{getattr(r, l):7.3f}" for l in LEGS) +
          f" {r.pass4b:7.3f} {r.pass_no_OOS:9.3f} {r.med_turn:6.2f} {r.med_OOS_Sharpe:8.3f}")

    # ---------------- hypotheses --------------------------------------------------------------
    P("\n" + "-" * 96)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 96)
    rot = br[br.kind == "RANDROT"].set_index(["panel", "cadence"])
    fix = br[br.kind == "RANDFIX"].set_index(["panel", "cadence"])

    v = rot.loc[("U56", "M"), "L_OOS"]
    h_dead = bool(v >= DEAD_BAR)
    P(f"  H_DEAD      U56/M RANDROT L_OOS base rate = {v:.3f}  (bar >= {DEAD_BAR}; 931 read 1.000 "
      f"at 500 draws)  -> {'PASS -- the leg is DEAD on this cell' if h_dead else 'FAIL'}")
    P(f"              same cell RANDFIX = {fix.loc[('U56','M'),'L_OOS']:.3f}  <- the kind, not the "
      f"cadence, can own the number; both are printed, neither is the headline")

    mono = []
    for p in PANELS:
        a_, b2, c2 = (rot.loc[(p, c), "L_OOS"] for c in CADENCES)
        mono.append(a_ < b2 < c2)
        P(f"  H_CADENCE   {p:5s} L_OOS  W {a_:.3f} < M {b2:.3f} < Q {c2:.3f}  -> "
          f"{'monotone' if mono[-1] else 'NOT monotone'}")
    h_cad = all(mono)
    P(f"              -> {'PASS' if h_cad else 'FAIL'}")

    ratios = []
    for p in PANELS:
        for c in CADENCES:
            num, den = rot.loc[(p, c), "pass4b"], rot.loc[(p, c), "pass_no_OOS"]
            rt = (num / den) if den > 0 else np.nan
            ratios.append((p, c, num, den, rt))
    ok = sum(1 for _, _, _, _, rt in ratios if not np.isnan(rt) and rt >= REDUND_BAR)
    nan_cells = sum(1 for _, _, _, den, rt in ratios if np.isnan(rt))
    h_red = ok >= REDUND_CELLS
    P(f"\n  H_REDUNDANT does dropping L_OOS change the joint verdict?  "
      f"P(all 5) / P(other 4), RANDROT:")
    for p, c, num, den, rt in ratios:
        P(f"              {p:5s} {c:3s}  {num:.4f} / {den:.4f} = "
          f"{'n/a (no draw clears the other four)' if np.isnan(rt) else f'{rt:.4f}'}")
    P(f"              cells at or above {REDUND_BAR}: {ok} of {len(ratios) - nan_cells} measurable "
      f"({nan_cells} undefined)  (bar >= {REDUND_CELLS})  -> "
      f"{'PASS -- the OOS leg is REDUNDANT beside H2' if h_red else 'FAIL'}")

    live = [l for l in LEGS if (rot[l] <= LIVE_BAR).all()]
    h_live = len(live) > 0
    P(f"\n  H_LIVE      legs with base rate <= {LIVE_BAR} in ALL 6 RANDROT cells: "
      f"{live if live else '(none)'}  -> {'PASS' if h_live else 'FAIL'}")
    P("              per-leg worst-cell base rate (RANDROT): " +
      ", ".join(f"{l}={rot[l].max():.3f}" for l in LEGS))

    # ---------------- the real books, rule 8, both KEEP paths ---------------------------------
    P("\n" + "-" * 96)
    P("THE REAL BOOKS -- RULE 8 (cadence chosen on IS <=2016 by Sharpe, OOS read once) + BOTH KEEP PATHS")
    P("-" * 96)
    brows = []
    for p in PANELS:
        pn = pans[p]
        base_r, _ = pn.ctx["W"].run(lag_weights(W1[(p, "BAND03")]), GROSS, COST)
        b_h1, b_h2 = fmet(base_r[pn.h1])[1], fmet(base_r[pn.h2])[1]
        b_dd = fmet(base_r[pn.warm])[2]
        b_oc, b_os, b_od = fmet(base_r[pn.oos_m])
        P(f"\n[{p}]  SPY full {pn.spy_c:.2%}/{pn.spy_s:.4f}/{pn.spy_dd:.2%}  halves "
          f"{pn.spy_h1:.4f}/{pn.spy_h2:.4f}  OOS {pn.spy_oos_c:.2%}/{pn.spy_oos_s:.4f}/{pn.spy_oos_dd:.2%}")
        P(f"[{p}]  RULES v2 baseline (W) OOS {b_oc:.2%}/{b_os:.4f}/{b_od:.2%}")
        for b in BOOKS:
            per = {}
            for c in CADENCES:
                r, t = pn.ctx[c].run(lag_weights(W1[(p, b)]), GROSS, COST)
                lg, (cg, sh, dd) = legs_of(pn, r)
                oc, os_, od = fmet(r[pn.oos_m])
                per[c] = dict(CAGR=cg, Sharpe=sh, MaxDD=dd, IS_Sharpe=fmet(r[pn.is_m])[1],
                              OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                              H1=fmet(r[pn.h1])[1], H2=fmet(r[pn.h2])[1],
                              turn=t[pn.warm].sum() / (pn.warm.sum() / 252.0), **lg)
            pick = max(CADENCES, key=lambda c: per[c]["IS_Sharpe"])
            for c in CADENCES:
                d_ = per[c]
                k4b = all(d_[l] for l in LEGS)
                k4a = bool(d_["H1"] > b_h1 and d_["H2"] > b_h2 and d_["MaxDD"] >= b_dd)
                nb = float(rot.loc[(p, c), "pass4b"])
                nl = float(rot.loc[(p, c), "L_OOS"])
                brows.append(dict(panel=p, book=b, cadence=c, is_pick=(c == pick), **d_,
                                  KEEP_4b=k4b, KEEP_4a=k4a, null_4b_baserate=nb,
                                  null_LOOS_baserate=nl,
                                  spy_OOS_CAGR=pn.spy_oos_c, spy_OOS_Sharpe=pn.spy_oos_s,
                                  spy_OOS_MaxDD=pn.spy_oos_dd, v2_OOS_CAGR=b_oc,
                                  v2_OOS_Sharpe=b_os, v2_OOS_MaxDD=b_od))
                fails = [l for l in LEGS if not d_[l]]
                P(f"  {b:7s} {c}{'*' if c == pick else ' '} full {cg if False else d_['CAGR']:7.2%}"
                  f"/{d_['Sharpe']:6.3f}/{d_['MaxDD']:7.2%}  halves {d_['H1']:.3f}/{d_['H2']:.3f}"
                  f"  OOS {d_['OOS_CAGR']:7.2%}/{d_['OOS_Sharpe']:6.3f}/{d_['OOS_MaxDD']:7.2%}"
                  f"  turn {d_['turn']:5.2f}x  4a={str(k4a):5s} 4b={str(k4b):5s}"
                  f"  fails:{','.join(fails) if fails else '-':22s}"
                  f"  null 4b {nb:.3f} / L_OOS {nl:.3f}")
            P(f"          ^ IS-chosen cadence = {pick}")
    bdf = pd.DataFrame(brows)
    dump(bdf, "books.csv")

    P("\n  KEEP verdicts on the IS-chosen cadence only (rule 8):")
    for r in bdf[bdf.is_pick].itertuples():
        P(f"    {r.panel:5s} {r.book:7s} cadence {r.cadence}: 4a={r.KEEP_4a}  4b={r.KEEP_4b}  "
          f"OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.2%}  vs SPY "
          f"{r.spy_OOS_CAGR:.2%}/{r.spy_OOS_Sharpe:.3f}/{r.spy_OOS_MaxDD:.2%}  vs RULES v2 "
          f"{r.v2_OOS_CAGR:.2%}/{r.v2_OOS_Sharpe:.3f}/{r.v2_OOS_MaxDD:.2%}   "
          f"[its cell's coin flip clears 4b {r.null_4b_baserate:.1%} of the time]")
    P(f"\n  4b PASS {int(bdf.KEEP_4b.sum())} of {len(bdf)} book x cadence cells; "
      f"4a PASS {int(bdf.KEEP_4a.sum())} of {len(bdf)}.")

    P("\n" + "-" * 96)
    P("THE GUARD THIS RUN PROPOSES (PROPOSED, NOT APPLIED -- PROTOCOL rule 6)")
    P("-" * 96)
    P("  PROTOCOL 4b currently reads THREE Sharpe legs: H1, H2 and rule-8 OOS. On this tree the")
    P("  H2 and OOS windows overlap by the percentages printed above, so the third leg is close")
    P("  to a restatement of the second rather than an independent test. Proposed amendment:")
    P("  (i) rule 8's OOS window must be DISJOINT from the second half used by 4b -- either the")
    P("      halves are taken INSIDE the IS window (2009-2016 split in two) or the 4b halves are")
    P("      dropped in favour of IS/OOS; and")
    P("  (ii) any published 4b PASS carries, beside it, the per-leg base rate of its OWN cell's")
    P("      gross-matched null under BOTH null kinds, and any leg whose base rate exceeds 0.90")
    P("      is reported as NOT CERTIFYING rather than as a pass.")
    P("  Scored on this run's grid, clause (ii) would strip the OOS leg from every cell where it")
    P("  reads >= 0.90 above, and clause (i) would make the H1/H2 split independent of rule 8.")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")
    return br, bdf


if __name__ == "__main__":
    a1, a2 = main()
    b1, b2 = main()
    print(f"\n  G6  determinism (whole grid run twice): "
          f"{'PASS' if a1.equals(b1) and a2.equals(b2) else 'FAIL'}")
