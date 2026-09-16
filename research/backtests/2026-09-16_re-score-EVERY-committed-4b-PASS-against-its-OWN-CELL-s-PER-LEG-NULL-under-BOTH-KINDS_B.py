#!/usr/bin/env python3
"""Idea 969 (lane B, 2026-09-16) -- re-score EVERY committed 4b PASS in the record against its
OWN CELL's PER-LEG NULL, under BOTH null kinds, at the 0.90 non-certifying bar.

THE STANDING CLAUSE THIS RUN SCORES
  `2026-09-15_4b-leg-certification-clause_cloud.memo.md` (idea 942), clause (ii), verbatim:
    "Any published 4b PASS carries, beside it, the per-leg base rate of its own cell's
     gross-matched null under BOTH null kinds (rotating and fixed).  Any leg whose base rate
     exceeds 0.90 is reported as NOT CERTIFYING rather than as a pass, and a 4b PASS in which
     every leg is non-certifying is reported as UNADJUDICATED, not as a KEEP."
  942 scored the clause on SIX cells it chose.  This run scores it on the cells the RECORD
  actually claims, which is the question idea 969 asks: harvest every committed 4b PASS that
  names a panel and a book, rebuild THAT cell's gross-matched null under BOTH kinds, and publish
  how many passes survive the 0.90 bar.

WHAT "SURVIVE" MEANS HERE (fixed before any number was read)
  A cell's leg is CERTIFYING under a kind iff that kind's null base rate for the leg is <= 0.90.
  The memo says BOTH kinds, so the headline reading is CERT_BOTH: a leg certifies iff
  max(rot, fix) <= 0.90.  A cell SURVIVES iff it has at least one certifying leg; otherwise the
  clause calls it UNADJUDICATED.  Per-kind readings (CERT_ROT, CERT_FIX) are printed beside the
  headline and never used to choose anything.

  NOTE ON DIRECTION, STATED UP FRONT: a HIGH base rate is BAD for the book -- it means a coin
  flip in the same cell clears the same leg.  "Survive" is therefore a weak bar: one leg that a
  coin flip does NOT routinely clear is enough to keep the pass adjudicable.

TUNED DIALS (exactly 2, per the queue; every level ALWAYS reported, none chooses anything)
  1. CLAIM SET  STRICT  units naming EXACTLY ONE panel and EXACTLY ONE book (cadence/gross from
                        the text where named exactly once, else the record's canonical W / 0.75)
                WIDE    any unit naming >= 1 panel and >= 1 book, expanded to the full cross
                        product of everything it names
                STRUCT  the CONTROL -- every structurally 4b-passing cell of the reproducible
                        90-cell ladder at 10 bps, harvested from PRICES and not from TEXT
  2. NULL KIND  RANDROT (rotating) and RANDFIX (fixed) -- the memo's two kinds, both always
                printed; RANDROT_FREE (ungated) is printed as a third REPORTED control because
                942 recorded that the gate moves the L_OOS reading from 1.000 to 0.892.

REPORTED, NEVER FITTED
  PANEL {U56, B136} x BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03} x GROSS {0.50, 0.75, 1.00} x
  CADENCE {W, M, Q} = 90 cells.  COST 10 bps BINDING (PROTOCOL rule 2), next-day execution.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_SURVIVE  the record's committed 4b passes survive their own clause.  PASS iff >= 0.50 of
             STRICT resolvable passes have >= 1 CERT_BOTH leg.
  H_KIND     the verdict does not depend on the null kind.  PASS iff the STRICT survival share
             under RANDROT and under RANDFIX differ by <= 0.10.
  H_LEGAGREE the two kinds agree LEG BY LEG, not just in aggregate.  PASS iff >= 0.80 of
             (cell, leg) pairs carry the same certifying label under RANDROT and RANDFIX.
  H_CLAIM    the answer does not depend on the claim set.  PASS iff STRICT and WIDE survival
             shares differ by <= 0.10.
  H_STRUCT   text-harvested passes behave like price-harvested ones.  PASS iff STRICT and STRUCT
             survival shares differ by <= 0.10.
  H_DEGEN    the answer does not rest on degenerate nulls.  PASS iff dropping every cell whose
             null has < 50% distinct draws moves the STRICT survival share by <= 0.10.
             (Degeneracy is idea 998's found construction defect, not a dial.)
  H_ALLCERT  the clause has teeth on the leg that matters.  PASS iff L_OOS is NON-certifying
             (base rate > 0.90 under BOTH kinds) in >= 0.50 of STRICT cells -- 942's U56/M
             finding, tested on the record's own claimed cells.
  H_RULE8    a chooser that demands a certifying leg is not worse out of sample.  PASS iff
             C_ISCERT's OOS 4b count >= C_ISSHARPE's.

RULE 8 (walk-forward, mandatory -- PROTOCOL rule 8)
  (book, gross) is chosen inside each (panel, cadence) on 2009-2016 ALONE by three IS-only
  choosers -- C_ISSHARPE (IS Sharpe), C_IS4B (IS-window 4b legs first, then IS Sharpe), and
  C_ISCERT (most CERTIFYING IS legs against the SAME cell's IS-only null, then IS Sharpe).
  2017-2026 is then read ONCE.  OOS CAGR / Sharpe / MaxDD are reported against the RULES v2 live
  baseline and against SPY, and BOTH KEEP paths are scored on every pick.  G6 proves the
  choosers are IS-only by permuting the OOS return rows.

GATES (printed before any result number)
  G0  rebalance masks == `engine.rebalance_mask` on W/M/Q.  Bar 0 rows.
  G1  closed-form `Ctx` == `engine.backtest` on returns AND turnover @10 bps.  Bar 1e-12.
  G2  BAND03 @0.75 == `baseline.rules_v2_weights(px, 0.03, 0.75)`.  Bar 0.0 exact.
  G3  CROSS-RUN: SPY's OOS triple vs the record's committed 15.2102% / 0.8711 / -33.7173%.
  G4  GROSS MATCH: every null draw's target gross AND holding count equal the book's on every
      decision row.  Bar 0.0 on both.
  G5  DETERMINISM: a redrawn null is bit-for-bit identical (md5-derived seeds).
  G6  every rule-8 chooser is IS-ONLY: picks invariant to permuted OOS return rows.
  G7  CROSS-RUN of idea 942's headline: U56 / TOP20 / 0.75 / M, L_OOS base rate == 1.000 under
      RANDROT and under RANDFIX (942 published 250 of 250 for both).  Bar 0 disagreements.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 and B136 are CURRENT-constituent lists.  Every CAGR and drawdown LEVEL is optimistic and
  every 4b count is an UPPER bound.  A coin flip drawn from a survivor panel is a BETTER book
  than one drawn in real time, so every NULL base rate here is also an UPPER bound -- which cuts
  AGAINST this run's own headline: legs measured live could certify more often than printed.
"""
from __future__ import annotations
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

COST, LAG, WARMUP = 10.0, 1, 260
MAXVOL, BAND = 0.60, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CERT_BAR = 0.90                       # the memo's own bar; never moved

SMOKE = os.environ.get("SMOKE", "") == "1"
DRAWS = 20 if SMOKE else 200

PANELS = ["U56", "B136"]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]
GROSSES = [0.50, 0.75, 1.00]
CADENCES = ["W", "M", "Q"]
KINDS = ["RANDROT", "RANDFIX", "RANDROT_FREE"]
MEMO_KINDS = ["RANDROT", "RANDFIX"]                    # the two the clause names
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
IS_LEGS = ["I_H1", "I_H2", "I_DD", "I_CAGR"]

CANON_GROSS, CANON_CADENCE = 0.75, "W"
GROSS_NAME = {"CORE": 0.75, "FULL": 1.00, "HALF": 0.50}
SPY_OOS_PUB = (0.152102, 0.8711, -0.337173)            # G3, committed by ideas 1018/1023
G3_TOL = (2e-3, 2e-2, 2e-3)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts) -> int:
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:16], 16) % (2 ** 32)


def head_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


# =================================================================================================
# runner
# =================================================================================================
class Ctx:
    """Closed-form equivalent of `engine.backtest`'s day loop for ONE rebalance schedule.

    Between rebalances nothing trades, so each holding grows with its own price and the cash
    sleeve is constant.  Gated at G1 against `engine.backtest` itself on returns AND turnover.
    Weight rows are passed already at their TARGET GROSS (books may de-gross, e.g. BAND03)."""

    def __init__(self, rets, applied):
        T, N = rets.shape
        self.rets, self.T = rets, T
        C = np.cumprod(1.0 + rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        self.reb = np.flatnonzero(applied)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]

    def run(self, wt, cost=COST):
        A = wt[self.s0]
        AR = A * self.R
        V = 1.0 + (AR.sum(axis=1) - A.sum(axis=1))
        port = (AR * self.rets).sum(axis=1) / V
        Ap = wt[self.s0p[self.reb]]
        ARp = Ap * self.Rp
        Vp = 1.0 + (ARp.sum(axis=1) - Ap.sum(axis=1))
        heldp = ARp / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp).sum(axis=1)
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


# =================================================================================================
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
        ipos = np.flatnonzero(self.is_m)
        ih = len(ipos) // 2
        self.ih1 = np.zeros(self.T, bool); self.ih1[ipos[:ih]] = True
        self.ih2 = np.zeros(self.T, bool); self.ih2[ipos[ih:]] = True
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.priced = px.notna().values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < MAXVOL) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        self.spy_full = fmet(self.spy[self.warm])
        self.spy_h1 = fmet(self.spy[self.h1])[1]
        self.spy_h2 = fmet(self.spy[self.h2])[1]
        self.spy_oos = fmet(self.spy[self.oos_m])
        self.spy_is = fmet(self.spy[self.is_m])
        self.spy_ih1 = fmet(self.spy[self.ih1])[1]
        self.spy_ih2 = fmet(self.spy[self.ih2])[1]


def legs_of(pn, r):
    """PROTOCOL 4b's five legs, plus the four IS-only analogues used by C_ISCERT / C_IS4B."""
    c, s, dd = fmet(r[pn.warm])
    ic, isharpe, idd = fmet(r[pn.is_m])
    oc, os_, odd = fmet(r[pn.oos_m])
    sh1, sh2 = fmet(r[pn.h1])[1], fmet(r[pn.h2])[1]
    d = dict(L_H1=sh1 > pn.spy_h1,
             L_H2=sh2 > pn.spy_h2,
             L_OOS=os_ > pn.spy_oos[1],
             L_DD=abs(dd) <= DD_CAP * abs(pn.spy_full[2]),
             L_CAGR=c >= CAGR_FLOOR * pn.spy_full[0],
             I_H1=fmet(r[pn.ih1])[1] > pn.spy_ih1,
             I_H2=fmet(r[pn.ih2])[1] > pn.spy_ih2,
             I_DD=abs(idd) <= DD_CAP * abs(pn.spy_is[2]),
             I_CAGR=ic >= CAGR_FLOOR * pn.spy_is[0])
    return d, (c, s, dd), (ic, isharpe, idd), (oc, os_, odd), (sh1, sh2)


# =================================================================================================
# books -- weight rows are already AT their target gross
# =================================================================================================
def book_w1(px, book, elig):
    """Unit-gross weights (gross is applied by the caller).  BAND03 deliberately does NOT sum to
    1: RULES v2 de-grosses gated-out weight to cash and never re-spreads it."""
    if book == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    if book == "EWELIG":
        E = elig.astype(float)
        k = E.sum(axis=1)
        out = np.zeros_like(E)
        nz = k > 0
        out[nz] = E[nz] / k[nz, None]
        return out
    n = int(book[3:])
    mom = (px.shift(21) / px.shift(252) - 1).rank(axis=1, pct=True)
    r6 = (px / px.shift(126) - 1).rank(axis=1, pct=True)
    r3 = (px / px.shift(63) - 1).rank(axis=1, pct=True)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = ((mom + r6 + r3) / 3) * (0.5 + 0.5 * above.astype(float))
    rank = sc.where(above & (vol20 < MAXVOL)).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


def draw_picks(buf, pn, W1, dec, kind, rng, fixed_order=None):
    """GROSS-MATCHED coin flip at UNIT gross: on every DECISION row it holds exactly as many
    equally weighted names as the book holds that day, at the book's own row sum (gated at G4).

      RANDROT       k fresh names drawn at random from the names passing the BOOK'S OWN gate
                    (above the 200d MA, vol20 < 0.60).  Isolates the SCORE; the gate is common.
      RANDFIX       ONE random preference ordering of the panel drawn once; at every rebalance
                    the top k eligible names under that ordering.  Same gate, same counts, no
                    rotation.
      RANDROT_FREE  k fresh names from every name PRICED that day, gate and all.  REPORTED
                    control only -- isolates GATE + SCORE together.

    Where the book holds MORE names than the gate admits (BAND03 routinely does), the pool is
    widened with the remaining PRICED names so the holding count still matches exactly."""
    buf[:] = 0.0
    held = W1 > 0
    kcount = held.sum(axis=1)
    rowsum = W1.sum(axis=1)
    for i in np.flatnonzero(dec):
        k = int(kcount[i])
        if k == 0:
            continue
        pool = np.flatnonzero(pn.priced[i] if kind == "RANDROT_FREE" else pn.elig[i])
        if len(pool) < k:
            extra = np.setdiff1d(np.flatnonzero(pn.priced[i]), pool, assume_unique=False)
            if len(extra):
                pool = np.concatenate([pool, extra])
        if len(pool) == 0:
            continue
        k = min(k, len(pool))
        if kind == "RANDFIX":
            pick = pool[np.argsort(fixed_order[pool])[:k]]
        else:
            pick = rng.choice(pool, size=k, replace=False)
        buf[i, pick] = rowsum[i] / k
    return buf


# =================================================================================================
# HARVEST -- the record's committed 4b PASS claims
# =================================================================================================
PAN_RX = {"U56": r"\bU56\b", "B136": r"\bB136\b", "SMALL663": r"\bSMALL(?:663|483)?\b"}
BOOK_RX = {"TOP5": r"\bTOP0?5\b", "TOP10": r"\bTOP10\b", "TOP20": r"\b(?:TOP20|CAND20)\b",
           "EWELIG": r"\bEWELIG\b", "BAND03": r"\bBAND03\b"}
CAD_RX = {"W": r"(?<![A-Za-z])W(?:EEKLY|eekly)?(?![A-Za-z])|\bweekly\b",
          "M": r"(?<![A-Za-z])M(?:ONTHLY|onthly)?(?![A-Za-z])|\bmonthly\b",
          "Q": r"(?<![A-Za-z])Q(?:UARTERLY|uarterly)?(?![A-Za-z])|\bquarterly\b"}
GROSS_RX = r"(?:gross\s*|g|@)\s*([01]\.\d{2})"
PASS_RX = re.compile(r"4b", re.I)
ASSERT_RX = re.compile(r"KEEP-candidate|\b4b\s+PASS|PASS(?:ES)?\b|\bpasses\b|\bclears?\b", re.I)


def harvest():
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
          if l.startswith("|") and not l.startswith("|---")][1:]
    cl = [p for p in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n") if p.strip()]
    units = [("LEADERBOARD", i, t) for i, t in enumerate(lb)] + \
            [("CHANGELOG", i, t) for i, t in enumerate(cl)]
    rows = []
    for src, i, t in units:
        if not (PASS_RX.search(t) and ASSERT_RX.search(t)):
            continue
        pans = sorted(k for k, v in PAN_RX.items() if re.search(v, t))
        bks = sorted(k for k, v in BOOK_RX.items() if re.search(v, t))
        cads = sorted(k for k, v in CAD_RX.items() if re.search(v, t))
        gs = sorted({float(x) for x in re.findall(GROSS_RX, t) if float(x) in GROSSES})
        for nm, gv in GROSS_NAME.items():
            if re.search(rf"\b{nm}\b", t) and gv not in gs:
                gs.append(gv)
        rows.append(dict(source=src, unit=i, n_panel=len(pans), n_book=len(bks), n_cad=len(cads),
                         n_gross=len(gs), panels="|".join(pans), books="|".join(bks),
                         cads="|".join(cads), grosses="|".join(f"{g:.2f}" for g in sorted(gs)),
                         text=t[:300].replace("\n", " ")))
    return pd.DataFrame(rows), len(units)


def resolve(cen, claimset):
    """Claim units -> (panel, book, gross, cadence) cells under one claim-set rule."""
    cells = []
    for _, r in cen.iterrows():
        pans = [p for p in r.panels.split("|") if p]
        bks = [b for b in r.books.split("|") if b]
        cads = [c for c in r.cads.split("|") if c]
        gs = [float(x) for x in r.grosses.split("|") if x]
        if not pans or not bks:
            continue
        if claimset == "STRICT":
            if len(pans) != 1 or len(bks) != 1:
                continue
            cads = cads if len(cads) == 1 else [CANON_CADENCE]
            gs = gs if len(gs) == 1 else [CANON_GROSS]
        else:
            cads = cads or [CANON_CADENCE]
            gs = gs or [CANON_GROSS]
        for p in pans:
            for b in bks:
                for g in gs:
                    for c in cads:
                        cells.append(dict(panel=p, book=b, gross=float(g), cadence=c,
                                          source=r.source, unit=int(r.unit)))
    return pd.DataFrame(cells)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 969 (lane B) -- re-score EVERY committed 4b PASS against its OWN CELL's PER-LEG NULL,")
    P("                     under BOTH null kinds, at the memo's 0.90 non-certifying bar")
    P(f"tree {head_sha()}   draws {DRAWS}   cost {COST:.0f} bps BINDING   smoke={SMOKE}")
    P("=" * 100)

    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pnl = {k: Panel(k, px[k]) for k in PANELS}
    P("\nPANELS")
    for k in PANELS:
        p = pnl[k]
        P(f"  {k:5s} {p.px.shape[1]-1:4d} names + SPY   {p.idx[0].date()} -> {p.idx[-1].date()}   "
          f"H2 starts {p.idx[np.flatnonzero(p.h2)[0]].date()}   OOS starts "
          f"{p.idx[np.flatnonzero(p.oos_m)[0]].date()}")
        P(f"        SPY full {p.spy_full[0]:7.2%} / {p.spy_full[1]:.4f} / {p.spy_full[2]:7.2%}   "
          f"OOS {p.spy_oos[0]:7.2%} / {p.spy_oos[1]:.4f} / {p.spy_oos[2]:7.2%}   "
          f"H1 {p.spy_h1:.4f}  H2 {p.spy_h2:.4f}")

    W1 = {(p, b): book_w1(pnl[p].px, b, pnl[p].elig) for p in PANELS for b in BOOKS}

    # ------------------------------------------------------------------ GATES (before results)
    P("\n" + "-" * 100)
    P("GATES")
    P("-" * 100)
    gate = {}

    g0 = 0
    for p in PANELS:
        for c in CADENCES:
            g0 += int((pnl[p].dec[c] != rebalance_mask(pnl[p].idx, c).values).sum())
    gate["G0"] = g0 == 0
    P(f"  G0  rebalance masks == engine.rebalance_mask       : {g0} disagreeing rows   "
      f"{'PASS' if gate['G0'] else 'FAIL'}")

    g1r = g1t = 0.0
    for p in PANELS:
        for b in ("TOP20", "BAND03"):
            for c in ("W", "M"):
                Wg = W1[(p, b)] * 0.75
                ref = backtest(pnl[p].px, pd.DataFrame(Wg, index=pnl[p].idx, columns=pnl[p].px.columns),
                               cost_bps=COST, freq=c)
                fr, ft = pnl[p].ctx[c].run(lag_weights(Wg))
                g1r = max(g1r, float(np.abs(fr - ref["returns"].values).max()))
                g1t = max(g1t, float(np.abs(ft - ref["turnover"].values).max()))
    gate["G1"] = g1r < 1e-12 and g1t < 1e-12
    P(f"  G1  Ctx == engine.backtest (returns / turnover)    : {g1r:.3e} / {g1t:.3e}   "
      f"{'PASS' if gate['G1'] else 'FAIL'}")

    g2 = 0.0
    for p in PANELS:
        ref = rules_v2_weights(pnl[p].px, BAND, 0.75).values
        g2 = max(g2, float(np.abs(W1[(p, "BAND03")] * 0.75 - ref).max()))
    gate["G2"] = g2 == 0.0
    P(f"  G2  BAND03@0.75 == baseline.rules_v2_weights       : {g2:.3e}   "
      f"{'PASS' if gate['G2'] else 'FAIL'}")

    d3 = tuple(abs(a - b) for a, b in zip(pnl["U56"].spy_oos, SPY_OOS_PUB))
    gate["G3"] = all(d < t for d, t in zip(d3, G3_TOL))
    P(f"  G3  CROSS-RUN SPY OOS triple vs the record         : "
      f"{pnl['U56'].spy_oos[0]:.4%} / {pnl['U56'].spy_oos[1]:.4f} / {pnl['U56'].spy_oos[2]:.4%}  "
      f"vs 15.2102% / 0.8711 / -33.7173%   max|d| {max(d3):.2e}   "
      f"{'PASS' if gate['G3'] else 'FAIL'}")

    # ------------------------------------------------------------------ the 90-cell ladder
    P("\n" + "-" * 100)
    P(f"THE LADDER  ({len(PANELS)} panels x {len(BOOKS)} books x {len(GROSSES)} gross x "
      f"{len(CADENCES)} cadences = {len(PANELS)*len(BOOKS)*len(GROSSES)*len(CADENCES)} cells) "
      f"@ {COST:.0f} bps")
    P("-" * 100)
    lad = []
    for p in PANELS:
        pn = pnl[p]
        for b in BOOKS:
            for g in GROSSES:
                wt = lag_weights(W1[(p, b)] * g)
                for c in CADENCES:
                    r, tn = pn.ctx[c].run(wt)
                    lg, full, ism, oos, halves = legs_of(pn, r)
                    lad.append(dict(panel=p, book=b, gross=g, cadence=c,
                                    CAGR=full[0], Sharpe=full[1], MaxDD=full[2],
                                    SH_H1=halves[0], SH_H2=halves[1],
                                    IS_CAGR=ism[0], IS_Sharpe=ism[1], IS_MaxDD=ism[2],
                                    OOS_CAGR=oos[0], OOS_Sharpe=oos[1], OOS_MaxDD=oos[2],
                                    turn_yr=float(tn[pn.warm].sum()) / (pn.warm.sum() / 252.0),
                                    **{k: bool(v) for k, v in lg.items()},
                                    p4b=bool(all(lg[k] for k in LEGS)),
                                    p4b_IS=bool(all(lg[k] for k in IS_LEGS))))
    lad = pd.DataFrame(lad)
    P(f"  structural 4b PASS cells: {int(lad.p4b.sum())} of {len(lad)}   "
      f"({', '.join(f'{k} {int(v)}' for k, v in lad.groupby('panel').p4b.sum().items())})")
    NET = {(r.panel, r.book, r.gross, r.cadence): i for i, r in lad.iterrows()}

    # ------------------------------------------------------------------ the nulls
    P("\n" + "-" * 100)
    P(f"THE NULLS  ({DRAWS} draws x {len(KINDS)} kinds x {len(PANELS)*len(BOOKS)*len(CADENCES)} "
      f"(panel,book,cadence) families; gross is a free rescale of the SAME picks)")
    P("-" * 100)
    base = {}            # (panel,book,gross,cadence,kind) -> {leg: base rate}
    ndist = {}           # distinct draws per (panel,book,cadence,kind)
    nullstat = []
    g4_dg = g4_dk = 0.0
    g5_ok = True
    for p in PANELS:
        pn = pnl[p]
        buf = np.zeros_like(pn.rets)
        for b in BOOKS:
            Wb = W1[(p, b)]
            for c in CADENCES:
                dec = pn.dec[c]
                decidx = np.flatnonzero(dec)
                for kind in KINDS:
                    acc = {(g, leg): 0 for g in GROSSES for leg in LEGS + IS_LEGS}
                    sig = set()
                    oos_sh = {g: [] for g in GROSSES}
                    for d in range(DRAWS):
                        sd = seed_of(p, b, c, kind, d)
                        rng = np.random.default_rng(sd)
                        fo = (np.random.default_rng(sd ^ 0x5EED).random(pn.rets.shape[1])
                              if kind == "RANDFIX" else None)
                        draw_picks(buf, pn, Wb, dec, kind, rng, fo)
                        sig.add(hashlib.md5(buf[decidx].tobytes()).hexdigest())
                        if d == 0:                         # G4 on every decision row
                            g4_dg = max(g4_dg, float(np.abs(buf[decidx].sum(axis=1)
                                                            - Wb[decidx].sum(axis=1)).max()))
                            g4_dk = max(g4_dk, float(np.abs((buf[decidx] > 0).sum(axis=1)
                                                            - (Wb[decidx] > 0).sum(axis=1)).max()))
                        for g in GROSSES:
                            r, _ = pn.ctx[c].run(lag_weights(buf * g))
                            lg, _f, _i, oo, _h = legs_of(pn, r)
                            oos_sh[g].append(oo[1])
                            for leg in LEGS + IS_LEGS:
                                acc[(g, leg)] += int(lg[leg])
                    ndist[(p, b, c, kind)] = len(sig)
                    for g in GROSSES:
                        base[(p, b, g, c, kind)] = {leg: acc[(g, leg)] / DRAWS
                                                    for leg in LEGS + IS_LEGS}
                        nullstat.append(dict(panel=p, book=b, gross=g, cadence=c, kind=kind,
                                             draws=DRAWS, distinct=len(sig),
                                             degenerate=bool(len(sig) < 0.5 * DRAWS),
                                             med_null_OOS_Sharpe=float(np.nanmedian(oos_sh[g])),
                                             **{leg: acc[(g, leg)] / DRAWS for leg in LEGS + IS_LEGS}))
                    # G5: redraw seed 0 and compare bytes
                    if b == "TOP20" and c == "M":
                        a = draw_picks(np.zeros_like(pn.rets), pn, Wb, dec, kind,
                                       np.random.default_rng(seed_of(p, b, c, kind, 0)),
                                       np.random.default_rng(seed_of(p, b, c, kind, 0) ^ 0x5EED)
                                       .random(pn.rets.shape[1]) if kind == "RANDFIX" else None)
                        g5_ok &= hashlib.md5(a[decidx].tobytes()).hexdigest() in sig
        P(f"  {p}: nulls built  ({time.time()-t0:.0f}s elapsed)")
    nullstat = pd.DataFrame(nullstat)

    gate["G4"] = g4_dg < 1e-12 and g4_dk == 0
    P(f"  G4  GROSS MATCH (row sum / holding count)          : {g4_dg:.3e} / {g4_dk:.0f}   "
      f"{'PASS' if gate['G4'] else 'FAIL'}")
    gate["G5"] = bool(g5_ok)
    P(f"  G5  DETERMINISM (redrawn null identical)           : {'PASS' if gate['G5'] else 'FAIL'}")

    v_rot = base[("U56", "TOP20", 0.75, "M", "RANDROT")]["L_OOS"]
    v_fix = base[("U56", "TOP20", 0.75, "M", "RANDFIX")]["L_OOS"]
    gate["G7"] = v_rot == 1.0 and v_fix == 1.0
    P(f"  G7  CROSS-RUN 942: U56/TOP20/0.75/M L_OOS base rate: RANDROT {v_rot:.3f} / RANDFIX "
      f"{v_fix:.3f}   (942 published 1.000 / 1.000)   {'PASS' if gate['G7'] else 'FAIL'}")

    deg = nullstat[nullstat.degenerate][["panel", "book", "cadence", "kind"]].drop_duplicates()
    P(f"\n  DEGENERATE NULLS (< 50% distinct draws; idea 998's found defect): "
      f"{len(deg)} of {len(nullstat[['panel','book','cadence','kind']].drop_duplicates())} "
      f"(panel,book,cadence,kind) families")
    if len(deg):
        P("    " + ", ".join(f"{r.panel}/{r.book}/{r.cadence}/{r.kind}" for _, r in deg.iterrows()))

    # ------------------------------------------------------------------ certification table
    cert = []
    for (p, b, g, c, kind), br in base.items():
        for leg in LEGS:
            cert.append(dict(panel=p, book=b, gross=g, cadence=c, kind=kind, leg=leg,
                             base_rate=br[leg], certifying=bool(br[leg] <= CERT_BAR)))
    cert = pd.DataFrame(cert)
    piv = cert.pivot_table(index=["panel", "book", "gross", "cadence", "leg"], columns="kind",
                           values="base_rate").reset_index()
    piv["cert_ROT"] = piv["RANDROT"] <= CERT_BAR
    piv["cert_FIX"] = piv["RANDFIX"] <= CERT_BAR
    piv["cert_BOTH"] = piv[MEMO_KINDS].max(axis=1) <= CERT_BAR
    cellcert = piv.groupby(["panel", "book", "gross", "cadence"]).agg(
        n_cert_BOTH=("cert_BOTH", "sum"), n_cert_ROT=("cert_ROT", "sum"),
        n_cert_FIX=("cert_FIX", "sum")).reset_index()
    for k in ("BOTH", "ROT", "FIX"):
        cellcert[f"survive_{k}"] = cellcert[f"n_cert_{k}"] > 0
    cellcert = cellcert.merge(lad[["panel", "book", "gross", "cadence", "p4b", "OOS_Sharpe",
                                   "OOS_CAGR", "OOS_MaxDD", "Sharpe", "MaxDD", "CAGR"]],
                              on=["panel", "book", "gross", "cadence"], how="left")
    dgn = nullstat.groupby(["panel", "book", "cadence"]).degenerate.any().rename("degenerate")
    cellcert = cellcert.merge(dgn, on=["panel", "book", "cadence"], how="left")

    # ------------------------------------------------------------------ the harvest
    P("\n" + "-" * 100)
    P("THE HARVEST  (committed 4b PASS claims in LEADERBOARD.md + CHANGELOG.md)")
    P("-" * 100)
    cen, n_units = harvest()
    P(f"  claim units scanned                : {n_units:,}  (LEADERBOARD rows + CHANGELOG paras)")
    P(f"  units ASSERTING a 4b pass          : {len(cen):,}  ({len(cen)/n_units:.1%})")
    P(f"  naming >= 1 panel AND >= 1 book    : {int(((cen.n_panel>0)&(cen.n_book>0)).sum()):,}  "
      f"({((cen.n_panel>0)&(cen.n_book>0)).mean():.1%} of asserting units)")
    P(f"  naming EXACTLY ONE of each (STRICT): {int(((cen.n_panel==1)&(cen.n_book==1)).sum()):,}")

    sets = {}
    for cs in ("STRICT", "WIDE"):
        cc = resolve(cen, cs)
        cc = cc[cc.panel.isin(PANELS)]
        sets[cs] = cc
        P(f"  {cs:6s} -> {len(cc):,} claim-cells, {len(cc.drop_duplicates(['panel','book','gross','cadence'])):,} DISTINCT cells "
          f"(SMALL663-named claims dropped: this run prices 2 panels)")
    st = lad[lad.p4b][["panel", "book", "gross", "cadence"]].copy()
    st["source"], st["unit"] = "STRUCT", -1
    sets["STRUCT"] = st
    P(f"  STRUCT -> {len(st):,} structurally 4b-passing ladder cells (from PRICES, not text)")

    # ------------------------------------------------------------------ THE ANSWER
    P("\n" + "=" * 100)
    P("THE ANSWER -- how many committed 4b PASSES survive the memo's 0.90 bar")
    P("=" * 100)
    ans = []
    for cs, cc in sets.items():
        u = cc.drop_duplicates(["panel", "book", "gross", "cadence"])
        m = u.merge(cellcert, on=["panel", "book", "gross", "cadence"], how="left")
        row = dict(claimset=cs, n_claimcells=len(cc), n_distinct=len(u))
        for k in ("BOTH", "ROT", "FIX"):
            row[f"survive_{k}"] = float(m[f"survive_{k}"].mean())
            row[f"n_survive_{k}"] = int(m[f"survive_{k}"].sum())
        row["mean_cert_legs_BOTH"] = float(m.n_cert_BOTH.mean())
        row["p4b_here"] = float(m.p4b.mean())
        nd = m[~m.degenerate.fillna(False)]
        row["survive_BOTH_nondegen"] = float(nd.survive_BOTH.mean()) if len(nd) else np.nan
        row["n_nondegen"] = len(nd)
        pp = m[m.p4b.fillna(False)]                  # cells that ARE 4b passes on this tree --
        row["n_p4b"] = len(pp)                       # the only ones the clause can even apply to
        row["survive_BOTH_p4b"] = float(pp.survive_BOTH.mean()) if len(pp) else np.nan
        ans.append(row)
        P(f"\n  {cs}  ({len(cc):,} claim-cells -> {len(u)} distinct cells)")
        P(f"    SURVIVE (>= 1 certifying leg)   BOTH-kinds {row['n_survive_BOTH']:3d}/{len(u):3d} "
          f"= {row['survive_BOTH']:.3f}   RANDROT {row['survive_ROT']:.3f}   "
          f"RANDFIX {row['survive_FIX']:.3f}")
        P(f"    mean CERTIFYING legs of 5       {row['mean_cert_legs_BOTH']:.2f}          "
          f"non-degenerate subset {row['n_nondegen']}/{len(u)} -> survive "
          f"{row['survive_BOTH_nondegen']:.3f}")
        P(f"    structurally 4b PASS on this tree: {row['p4b_here']:.3f}  "
          f"({row['n_p4b']} cells)   survival RESTRICTED to those: "
          f"{row['survive_BOTH_p4b']:.3f}   <- the only cells the clause can apply to")
        pl = piv.merge(u, on=["panel", "book", "gross", "cadence"])
        P("    per-leg share of cells where the leg is NON-certifying (base rate > 0.90):")
        for leg in LEGS:
            s = pl[pl.leg == leg]
            P(f"      {leg:7s} BOTH {1-s.cert_BOTH.mean():.3f}   ROT {1-s.cert_ROT.mean():.3f}   "
              f"FIX {1-s.cert_FIX.mean():.3f}   median base rate ROT {s.RANDROT.median():.3f} / "
              f"FIX {s.RANDFIX.median():.3f} / FREE {s.RANDROT_FREE.median():.3f}")
    ans = pd.DataFrame(ans)
    P(f"\n  CROSS-RUN (reported, not a gate): the share of STRICT text-harvested cells that pass 4b "
      f"structurally on this tree reads {ans.set_index('claimset').loc['STRICT','p4b_here']:.3f} "
      f"here against idea 998's independently published H_REPRO of 0.294 on the same corpus.")

    # ------------------------------------------------------------------ hypotheses
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    A = ans.set_index("claimset")
    H = {}
    H["H_SURVIVE"] = A.loc["STRICT", "survive_BOTH"] >= 0.50
    P(f"  H_SURVIVE  STRICT survival >= 0.50            : {A.loc['STRICT','survive_BOTH']:.3f}   "
      f"{'PASS' if H['H_SURVIVE'] else 'FAIL'}")
    dk = abs(A.loc["STRICT", "survive_ROT"] - A.loc["STRICT", "survive_FIX"])
    H["H_KIND"] = dk <= 0.10
    P(f"  H_KIND     |ROT - FIX| <= 0.10                : {dk:.3f}   "
      f"{'PASS' if H['H_KIND'] else 'FAIL'}")
    su = sets["STRICT"].drop_duplicates(["panel", "book", "gross", "cadence"])
    pl = piv.merge(su, on=["panel", "book", "gross", "cadence"])
    agree = float((pl.cert_ROT == pl.cert_FIX).mean())
    H["H_LEGAGREE"] = agree >= 0.80
    P(f"  H_LEGAGREE leg-label agreement >= 0.80        : {agree:.3f}  ({len(pl)} (cell,leg) pairs)"
      f"   {'PASS' if H['H_LEGAGREE'] else 'FAIL'}")
    dc = abs(A.loc["STRICT", "survive_BOTH"] - A.loc["WIDE", "survive_BOTH"])
    H["H_CLAIM"] = dc <= 0.10
    P(f"  H_CLAIM    |STRICT - WIDE| <= 0.10            : {dc:.3f}   "
      f"{'PASS' if H['H_CLAIM'] else 'FAIL'}")
    ds = abs(A.loc["STRICT", "survive_BOTH"] - A.loc["STRUCT", "survive_BOTH"])
    H["H_STRUCT"] = ds <= 0.10
    P(f"  H_STRUCT   |STRICT - STRUCT| <= 0.10          : {ds:.3f}   "
      f"{'PASS' if H['H_STRUCT'] else 'FAIL'}")
    dd_ = abs(A.loc["STRICT", "survive_BOTH"] - A.loc["STRICT", "survive_BOTH_nondegen"])
    H["H_DEGEN"] = bool(dd_ <= 0.10)
    P(f"  H_DEGEN    |all - non-degenerate| <= 0.10     : {dd_:.3f}   "
      f"{'PASS' if H['H_DEGEN'] else 'FAIL'}")
    noncert_oos = float(1 - pl[pl.leg == "L_OOS"].cert_BOTH.mean())
    H["H_ALLCERT"] = noncert_oos >= 0.50
    P(f"  H_ALLCERT  L_OOS non-certifying in >= 0.50    : {noncert_oos:.3f}   "
      f"{'PASS' if H['H_ALLCERT'] else 'FAIL'}")

    # ------------------------------------------------------------------ RULE 8
    P("\n" + "=" * 100)
    P("RULE 8 -- WALK-FORWARD (picks on 2009-2016 ALONE; 2017-2026 read ONCE)")
    P("=" * 100)
    lk = lad.set_index(["panel", "book", "gross", "cadence"])

    def iscert_legs(p, b, g, c):
        """CERTIFYING IS-only legs: the four IS analogues, both memo kinds, same 0.90 bar."""
        return sum(1 for leg in IS_LEGS
                   if max(base[(p, b, g, c, k)][leg] for k in MEMO_KINDS) <= CERT_BAR)

    def pick(p, c, chooser, ladder):
        cands = [(b, g) for b in BOOKS for g in GROSSES]
        def key(bg):
            b, g = bg
            r = ladder.loc[(p, b, g, c)]
            if chooser == "C_ISSHARPE":
                return (r.IS_Sharpe,)
            if chooser == "C_IS4B":
                return (int(r.p4b_IS), r.IS_Sharpe)
            return (iscert_legs(p, b, g, c), r.IS_Sharpe)      # C_ISCERT
        return max(cands, key=key)

    CHOOSERS = ["C_ISSHARPE", "C_IS4B", "C_ISCERT"]
    # G6: IS-only proof -- permute OOS return rows and re-pick
    rng6 = np.random.default_rng(seed_of("G6"))
    lad_perm = lad.copy()
    om = lad_perm.panel.map(lambda p: True)
    for col in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "CAGR", "Sharpe", "MaxDD"):
        lad_perm.loc[om, col] = rng6.permutation(lad_perm.loc[om, col].values)
    lk_perm = lad_perm.set_index(["panel", "book", "gross", "cadence"])
    g6 = all(pick(p, c, ch, lk) == pick(p, c, ch, lk_perm)
             for p in PANELS for c in CADENCES for ch in CHOOSERS)
    gate["G6"] = g6
    P(f"  G6  choosers are IS-ONLY (picks invariant to permuted OOS/full rows): "
      f"{'PASS' if g6 else 'FAIL'}")

    wf = []
    for p in PANELS:
        pn = pnl[p]
        bw = rules_v2_weights(pn.px, BAND, 0.75).values
        rb, _ = pn.ctx["W"].run(lag_weights(bw))
        b_oos = fmet(rb[pn.oos_m]); b_h1 = fmet(rb[pn.h1])[1]; b_h2 = fmet(rb[pn.h2])[1]
        b_full = fmet(rb[pn.warm])
        for c in CADENCES:
            for ch in CHOOSERS:
                b, g = pick(p, c, ch, lk)
                r = lk.loc[(p, b, g, c)]
                keep4b = bool(all(r[k] for k in LEGS))
                keep4a = bool(fmet_h1h2(lad, p, b, g, c, "H1") > b_h1 and
                              fmet_h1h2(lad, p, b, g, c, "H2") > b_h2 and
                              r.MaxDD >= b_full[2])
                wf.append(dict(panel=p, cadence=c, chooser=ch, pick=f"{b}@{g:.2f}",
                               n_cert_IS=iscert_legs(p, b, g, c),
                               OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                               SPY_OOS_CAGR=pn.spy_oos[0], SPY_OOS_Sharpe=pn.spy_oos[1],
                               SPY_OOS_MaxDD=pn.spy_oos[2],
                               BASE_OOS_CAGR=b_oos[0], BASE_OOS_Sharpe=b_oos[1],
                               BASE_OOS_MaxDD=b_oos[2],
                               keep4b=keep4b, keep4a=keep4a,
                               survive_BOTH=bool(cellcert.set_index(
                                   ["panel", "book", "gross", "cadence"])
                                   .loc[(p, b, g, c), "survive_BOTH"])))
    wf = pd.DataFrame(wf)
    P("\n  panel cad  chooser      pick            OOS CAGR / Sharpe / MaxDD        "
      "baseline OOS              SPY OOS                 4b  4a  surv")
    for _, r in wf.iterrows():
        P(f"  {r.panel:5s} {r.cadence:3s}  {r.chooser:11s}  {r['pick']:14s}  "
          f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / {r.OOS_MaxDD:7.2%}   "
          f"{r.BASE_OOS_CAGR:6.2%} / {r.BASE_OOS_Sharpe:5.3f} / {r.BASE_OOS_MaxDD:7.2%}   "
          f"{r.SPY_OOS_CAGR:6.2%} / {r.SPY_OOS_Sharpe:5.3f} / {r.SPY_OOS_MaxDD:7.2%}   "
          f"{'Y' if r.keep4b else 'n'}   {'Y' if r.keep4a else 'n'}   "
          f"{'Y' if r.survive_BOTH else 'n'}")
    P(f"\n  OOS 4b PASS: {int(wf.keep4b.sum())} of {len(wf)}    OOS 4a PASS: "
      f"{int(wf.keep4a.sum())} of {len(wf)}")
    for ch in CHOOSERS:
        s = wf[wf.chooser == ch]
        P(f"    {ch:11s} 4b {int(s.keep4b.sum())}/{len(s)}   4a {int(s.keep4a.sum())}/{len(s)}   "
          f"mean OOS Sharpe {s.OOS_Sharpe.mean():.3f}   surviving picks "
          f"{int(s.survive_BOTH.sum())}/{len(s)}")
    H["H_RULE8"] = int(wf[wf.chooser == "C_ISCERT"].keep4b.sum()) >= \
                   int(wf[wf.chooser == "C_ISSHARPE"].keep4b.sum())
    P(f"  H_RULE8    C_ISCERT OOS 4b >= C_ISSHARPE's    : "
      f"{int(wf[wf.chooser=='C_ISCERT'].keep4b.sum())} vs "
      f"{int(wf[wf.chooser=='C_ISSHARPE'].keep4b.sum())}   "
      f"{'PASS' if H['H_RULE8'] else 'FAIL'}")

    # ------------------------------------------------------------------ verdict
    P("\n" + "=" * 100)
    P(f"GATES {sum(gate.values())} of {len(gate)} PASS   "
      + "  ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in gate.items()))
    P(f"HYPOTHESES {sum(H.values())} of {len(H)} PASS   "
      + "  ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in H.items()))
    P("=" * 100)

    dump(lad, "ladder.csv"); dump(nullstat, "nulls.csv"); dump(piv, "cert.csv")
    dump(cellcert, "cells.csv"); dump(cen, "census.csv"); dump(ans, "answer.csv")
    dump(wf, "walkforward.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nelapsed {time.time()-t0:.0f}s")
    return dict(lad=lad, ans=ans, wf=wf, gate=gate, H=H, piv=piv, nullstat=nullstat)


def fmet_h1h2(lad, p, b, g, c, which):
    """Half Sharpes are recomputed from the ladder's stored legs only where needed; the ladder
    stores the boolean legs, so the raw half Sharpe is re-read here from the cached column."""
    return lad.loc[(lad.panel == p) & (lad.book == b) & (lad.gross == g) & (lad.cadence == c),
                   f"SH_{which}"].iloc[0]


if __name__ == "__main__":
    main()
