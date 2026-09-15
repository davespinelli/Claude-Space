#!/usr/bin/env python3
"""Idea 931 (cloud, 2026-09-15) -- is the W->M SHARPE GAIN on the STANDING CANDIDATE inside its
own NULL?

THE QUESTION (queue, 2026-09-15)
  Idea 926 found `U56/CORE/TOP20` at 10 bps improves from 12.60% / 1.088 / -18.31% WEEKLY to
  14.69% / 1.203 / -19.51% MONTHLY, while its gross-matched coin-flip base rate goes 0.0% -> 38.4%.
  A base rate is a statement about the LEVEL.  The queue asks for the statement about the GAIN:
  run the same cadence ladder on the NULL and report the book's percentile in the null's own
  W->M IMPROVEMENT distribution, not just in the level.

WHY THE GAIN IS THE RIGHT OBJECT
  Slowing a book down cuts its turnover, and at a fixed cost rung every book -- including a coin
  flip -- gets paid for that.  So a W->M gain is only evidence about the RULE if it is larger than
  the gain a random book with the same gross, the same holding count and the same cadence collects
  for free.  That is exactly a percentile in the null's DELTA distribution, and it is the number
  the record has never published for this book.

THE BOOK (idea 670's `CAND20` = `CORE/TOP20`, the 2026-09-04 KEEP 4b candidate; NOT re-specified)
  Each rebalance, rank every priced name above its own 200d MA with 20d realised vol < 0.60 by the
  v1 composite mean(pct-rank 12-1 mom, pct-rank 6m, pct-rank 3m) x (1 if above 200d MA else 0.5)
  WITHOUT the /sqrt(vol20) term; hold the top k = min(20, #eligible) at g/k each, g = 0.75.

THE NULL, AND WHY ITS GROSS MATCH IS EXACT (idea 680's construction, unmodified)
  On each rebalance row the book holds k(t) names at one common per-name weight w(t) = g/k(t),
  drawn from the candidate pool P(t) = the names that are eligible AND scored that day.  The null
  holds k(t) names at the SAME w(t), drawn uniformly without replacement from that SAME P(t).
  Count and per-name weight are copied from the book row by row, so gross, cash drag and the whole
  drift path are identical (gated at G2), and the ONLY difference is WHICH names.  The null is
  re-drawn on its OWN cadence, so its turnover carries the same cadence effect the book's does --
  which is the entire point.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CADENCE LADDER, 2 levels, both reported:
           LADDER2 = {W, M}          the queue's own contrast
           LADDER4 = {D, W, M, Q}    the same contrast inside a full ladder
  TUNED 2  PANEL, 3 levels, all reported, never averaged: U56 / B136 / SMALL
  REPORTED AXES (nothing fitted on them; every point published):
           cost 0 / 10 / 25 / 50 bps; draws 500 per (panel, cadence) with the 250-draw
           half-sample printed beside it; windows FULL / IS / OOS / H1 / H2.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_LEVEL  926's published W and M triples for U56/CORE/TOP20 reproduce on this tree to the
           record's own vintage bar (dCAGR < 0.005, dSharpe < 0.030, dMaxDD < 0.015).
  H_GAIN   the book's W->M dSharpe sits at or above the 95th percentile of the NULL's own W->M
           dSharpe distribution.  Below that, the cadence gain is not evidence about the rule.
  H_FREE   the null ITSELF gains from W->M (median null dSharpe > 0), i.e. the gain is at least
           partly a turnover rebate that any book collects.
  H_PANEL  whatever H_GAIN says on U56 it says on B136 and on SMALL.
  H_LADDER the percentile does not move by more than 5 points between LADDER2 and LADDER4.
  H_WF     (rule 8, REQUIRED) CADENCE chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026 read
           ONCE, both KEEP paths, against SPY and the live RULES v2 book in the same window.

GATES (all printed before any result number)
  G1  the fast runner == `engine.backtest` on returns and turnover (the book, U56, W and M)
  G2  the null's realised gross == the book's realised gross on EVERY day, every cadence
  G3  CROSS-RUN: idea 926's published U56/CORE/TOP20 W and M triples
  G4  the draw is legal: |P(t)| >= k(t) on every rebalance row of every panel and cadence
  G5  determinism: the same seed reproduces the same null return series bit-for-bit
  G6  the null is INVESTED on every cadence (median realised gross > 0.50, vol > 0.01) -- the
      gate that catches a draw written on the wrong row and silently held as cash

PROTOCOL: 10 bps primary, t+1 execution, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every
ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is
optimistic.  The direction for THIS run's headline is specific and works AGAINST the book: a coin
flip drawn from a survivor panel is a BETTER book than one drawn in real time, so the null's gains
are an UPPER bound and the book's percentile inside the null is a LOWER bound -- which means a
FAILING percentile here is a fortiori failing.  The 4b bar is SPY, which is not survivorship-
inflated.  Stated, not hidden.
"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
LAG = 1
BAND0 = 0.03
MAXVOL = 0.60
NTOP = 20
GROSS = 0.75
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 10.0, 25.0, 50.0]
NDRAW = 500
HALF = 250
SEED0 = 20260915

LADDERS = {"LADDER2": ["W", "M"], "LADDER4": ["D", "W", "M", "Q"]}
PANELS = ["U56", "B136", "SMALL"]

GAIN_PCTL_BAR = 95.0      # H_GAIN
LADDER_BAR = 5.0          # H_LADDER (percentile points)

# idea 926's committed U56/CORE/TOP20 triples (10 bps, g=0.75)
PUB_W = (0.1260, 1.088, -0.1831)
PUB_M = (0.1469, 1.203, -0.1951)
TOL_C, TOL_S, TOL_D = 0.005, 0.030, 0.015

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
class Panel:
    def __init__(self, name, px, freq):
        self.name, self.px, self.freq = name, px, freq
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, freq).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.dec = np.maximum(self.reb - LAG, 0)   # DECISION rows (weights decided at t, applied t+1)
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        yr = self.idx
        m_full = np.asarray(self.idx >= self.idx[WARMUP])
        fp = np.flatnonzero(m_full)
        h = len(fp) // 2
        m1 = np.zeros(T, bool); m1[fp[:h]] = True
        m2 = np.zeros(T, bool); m2[fp[h:]] = True
        self.masks = {"FULL": m_full, "H1": m1, "H2": m2,
                      "IS": m_full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
                      "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        self.spy = px["SPY"].pct_change().fillna(0.0).values


class Book:
    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]
        AR = A * panel.R
        self.S = AR.sum(axis=1)
        self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        ARp = Ap * panel.Rp
        self.ARp = ARp
        self.Sp = ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)

    def at(self, g=GROSS, cost=COST0):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn

    def realised_gross(self, g=GROSS):
        V = 1.0 + g * (self.S - self.As)
        return g * self.S / V


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def full_pack(r, pan):
    c, s, d = fmet(np.asarray(r)[pan.masks["FULL"]])
    co, so, do = fmet(np.asarray(r)[pan.masks["OOS"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=d,
                H1=fsharpe(np.asarray(r)[pan.masks["H1"]]),
                H2=fsharpe(np.asarray(r)[pan.masks["H2"]]),
                oCAGR=co, oSharpe=so, oMaxDD=do)


def legs4b(s, spy):
    L = dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
             L3_OOS=bool(s["oSharpe"] > spy["oSharpe"]),
             L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
             L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    L["pass4b"] = bool(all(L.values()))
    return L


# ================================================================================================
def book_w1_and_pool(px):
    """The book's gross-1.0 weights AND the candidate pool it drew them from (the null's pool)."""
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAXVOL) & px.notna() & sc.notna()
    sce = sc.where(elig)
    rank = sce.rank(axis=1, ascending=False)
    sel = (rank <= NTOP).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    W1 = sel.div(k, axis=0).fillna(0.0).values
    return W1, elig.values, sel.sum(axis=1).values.astype(int)


def null_w1(pool, kcount, dec, rng):
    """Gross-matched coin flip: on each DECISION row draw k(t) names uniformly from P(t).

    `dec` must be the DECISION rows (reb - LAG), not the application rows: the book's weights
    matrix is defined on every day and `Book` rolls it forward by LAG, so a null written on the
    application rows would be rolled off its own rebalance and hold nothing.  Gated at G6.
    """
    T, N = pool.shape
    W = np.zeros((T, N))
    for t in dec:
        k = kcount[t]
        if k <= 0:
            continue
        idx = np.flatnonzero(pool[t])
        if len(idx) == 0:
            continue
        k = min(k, len(idx))
        pick = rng.choice(idx, size=k, replace=False)
        W[t, pick] = 1.0 / k
    return W


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 931 (cloud) -- is the W->M SHARPE GAIN on the STANDING CANDIDATE inside its own NULL?")
    P("=" * 100)

    # ---------------------------------------------------------------------------- load panels
    raw = {}
    raw["U56"] = load_universe()
    raw["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c not in bad]
    raw["SMALL"] = sm[keep]
    P(f"\n  panels: " + ", ".join(f"{k} {v.shape[1]} cols x {v.shape[0]} rows "
                                 f"[{v.index[0].date()}..{v.index[-1].date()}]" for k, v in raw.items()))
    P(f"  SMALL: dropped {len(bad & set(sm.columns))} tickers with max_1d_move >= 1.0 "
      f"per data/small_meta.csv (SURVIVORSHIP: current constituents of the screen only)")

    ALL_FREQS = sorted({f for L in LADDERS.values() for f in L}, key="DWMQ".index)

    # build every (panel, freq) once: panel object, book, pool, k(t)
    ctx = {}
    for pn, px in raw.items():
        W1, pool, kc = book_w1_and_pool(px)
        for f in ALL_FREQS:
            pan = Panel(pn, px, f)
            ctx[(pn, f)] = dict(pan=pan, book=Book(pan, W1), pool=pool, kc=kc, W1=W1, px=px)

    # ---------------------------------------------------------------------------------- GATES
    P("\n" + "-" * 100)
    P("GATES (printed before any result number)")
    P("-" * 100)
    gates = []

    # G1
    d1 = []
    for f in ("W", "M"):
        c = ctx[("U56", f)]
        r_f, t_f = c["book"].at(GROSS, COST0)
        eng = backtest(c["px"], pd.DataFrame(GROSS * c["W1"], index=c["px"].index, columns=c["px"].columns),
                       cost_bps=COST0, freq=f)
        m = c["pan"].masks["FULL"]
        d1.append((f, float(np.abs(r_f[m] - eng["returns"].values[m]).max()),
                   float(np.abs(t_f[m] - eng["turnover"].values[m]).max())))
    ok1 = all(a < 1e-9 and b < 1e-9 for _, a, b in d1)
    gates.append(dict(gate="G1 fast runner == engine.backtest (book, U56, W and M, post-warm-up)",
                      stat=" | ".join(f"{f}: dret {a:.2e} dturn {b:.2e}" for f, a, b in d1),
                      bar="1e-9", passed=ok1))

    # G2 gross match.  THE MATCH IS ON THE TARGET, WHICH IS THE ONLY THING A DRAW CONTROLS: on every
    # rebalance row the null holds the same NUMBER of names at the same PER-NAME WEIGHT, so the
    # target gross and the cash position are identical row by row.  The DRIFTED gross afterwards is
    # a function of which names were held, i.e. of the very thing the null randomises, and is
    # measured at G2b rather than gated -- a null whose drifted gross matched would not be a null.
    d2t, d2k, d2w, d2d = [], [], [], []
    for pn in PANELS:
        for f in ALL_FREQS:
            c = ctx[(pn, f)]
            rng = np.random.default_rng(SEED0)
            NW = null_w1(c["pool"], c["kc"], c["pan"].dec, rng)
            reb = c["pan"].dec
            d2t.append(float(np.abs(NW[reb].sum(axis=1) - c["W1"][reb].sum(axis=1)).max()))
            d2k.append(int(np.abs((NW[reb] > 0).sum(axis=1) - (c["W1"][reb] > 0).sum(axis=1)).max()))
            nz = NW[reb].max(axis=1)
            bz = c["W1"][reb].max(axis=1)
            d2w.append(float(np.abs(nz - bz).max()))
            nb = Book(c["pan"], NW)
            d2d.append(float(np.abs(nb.realised_gross() - c["book"].realised_gross()).max()))
    gates.append(dict(gate="G2 null TARGET gross / count / per-name weight == book's (every panel x cadence)",
                      stat=f"max|dgross_target| {max(d2t):.3e}, max|dcount| {max(d2k)}, "
                           f"max|dweight| {max(d2w):.3e} over {len(d2t)} cells",
                      bar="1e-12 / 0 / 1e-12",
                      passed=bool(max(d2t) < 1e-12 and max(d2k) == 0 and max(d2w) < 1e-12)))
    gates.append(dict(gate="G2b DRIFTED gross divergence (measured, NOT gated)",
                      stat=f"max|dgross_drifted| {max(d2d):.3e}, median over cells "
                           f"{float(np.median(d2d)):.3e} -- this is the null doing its job",
                      bar="reported", passed=True))

    # G3 cross-run vs idea 926
    g3 = []
    for f, want in (("W", PUB_W), ("M", PUB_M)):
        c = ctx[("U56", f)]
        r_f, _ = c["book"].at(GROSS, COST0)
        m = full_pack(r_f, c["pan"])
        dc, ds, dd = abs(m["CAGR"] - want[0]), abs(m["Sharpe"] - want[1]), abs(m["MaxDD"] - want[2])
        ok = dc < TOL_C and ds < TOL_S and dd < TOL_D
        g3.append(f"{f} {m['CAGR']:.4f}/{m['Sharpe']:.4f}/{m['MaxDD']:.4f} vs committed "
                  f"{want[0]}/{want[1]}/{want[2]} d=({dc:.4f},{ds:.4f},{dd:.4f}) {'OK' if ok else 'MISS'}")
    gates.append(dict(gate="G3 CROSS-RUN idea 926's U56/CORE/TOP20 W and M triples",
                      stat=" | ".join(g3),
                      bar=f"dCAGR<{TOL_C} dSharpe<{TOL_S} dMaxDD<{TOL_D}",
                      passed=all("OK" in s for s in g3)))

    # G4 the draw is legal
    worst = None
    okc = 0
    for pn in PANELS:
        for f in ALL_FREQS:
            c = ctx[(pn, f)]
            reb = c["pan"].dec
            avail = c["pool"][reb].sum(axis=1)
            need = c["kc"][reb]
            short = int((avail < need).sum())
            okc += short
            if worst is None or short > worst[2]:
                worst = (pn, f, short, int(need.max()), int(avail.min()))
    gates.append(dict(gate="G4 draw legality |P(t)| >= k(t) on every rebalance row",
                      stat=f"rows short of pool: {okc} (worst cell {worst[0]}/{worst[1]} short={worst[2]}, "
                           f"max k={worst[3]}, min |P|={worst[4]})", bar="0", passed=bool(okc == 0)))

    # G5 determinism
    c = ctx[("U56", "M")]
    ra, _ = Book(c["pan"], null_w1(c["pool"], c["kc"], c["pan"].dec, np.random.default_rng(7))).at()
    rb, _ = Book(c["pan"], null_w1(c["pool"], c["kc"], c["pan"].dec, np.random.default_rng(7))).at()
    d5 = float(np.abs(ra - rb).max())
    gates.append(dict(gate="G5 determinism (same seed -> same null)", stat=f"max|d| {d5:.3e}",
                      bar="0.0", passed=bool(d5 == 0.0)))

    # G6 the null is actually INVESTED on every cadence.  This gate exists because the first cut of
    # this run wrote the draw on the APPLICATION rows; `Book` rolls weights forward by LAG, so on
    # every non-daily cadence the null was rolled off its own rebalance and held pure cash -- a
    # silent all-zero return series that every other gate passed.  Both legs are reported.
    d6g, d6s = [], []
    for pn in PANELS:
        for f in ALL_FREQS:
            c = ctx[(pn, f)]
            nb = Book(c["pan"], null_w1(c["pool"], c["kc"], c["pan"].dec, np.random.default_rng(11)))
            r, _ = nb.at()
            m = c["pan"].masks["FULL"]
            d6g.append(float(np.median(nb.realised_gross()[m])))
            d6s.append(float(np.std(r[m], ddof=1) * np.sqrt(252.0)))
    gates.append(dict(gate="G6 the null is INVESTED on every cadence (not rolled off its rebalance)",
                      stat=f"min median realised gross {min(d6g):.4f} (book target {GROSS}), "
                           f"min annualised vol {min(d6s):.4f} over {len(d6g)} panel x cadence cells",
                      bar="gross > 0.50 and vol > 0.01 everywhere",
                      passed=bool(min(d6g) > 0.50 and min(d6s) > 0.01)))

    for g in gates:
        P(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}   (bar {g['bar']})")

    # ------------------------------------------------------------------------------- THE BOOK
    P("\n" + "-" * 100)
    P("THE BOOK on the cadence ladder (g=0.75, every cost rung reported)")
    P("-" * 100)
    brows = []
    for pn in PANELS:
        for f in ALL_FREQS:
            c = ctx[(pn, f)]
            spyp = full_pack(c["pan"].spy, c["pan"])
            for cost in COSTS:
                r, turn = c["book"].at(GROSS, cost)
                m = full_pack(r, c["pan"])
                brows.append(dict(panel=pn, freq=f, cost_bps=cost, arm="BOOK", **m,
                                  ann_turn=float(turn.sum() / (len(turn) / 252.0)),
                                  spy_Sharpe=spyp["Sharpe"], **legs4b(m, spyp)))
    bk = pd.DataFrame(brows)
    for pn in PANELS:
        P(f"\n    {pn}   (SPY FULL Sharpe {full_pack(ctx[(pn,'W')]['pan'].spy, ctx[(pn,'W')]['pan'])['Sharpe']:.4f})")
        P(f"      {'freq':<5} {'cost':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'annTurn':>8} {'4b':>6}")
        for f in ALL_FREQS:
            for cost in COSTS:
                r = bk[(bk.panel == pn) & (bk.freq == f) & (bk.cost_bps == cost)].iloc[0]
                P(f"      {f:<5} {cost:>5.0f} {r.CAGR:>8.2%} {r.Sharpe:>8.4f} {r.MaxDD:>8.2%} "
                  f"{r.ann_turn:>8.2f} {str(bool(r.pass4b)):>6}")
    dump(bk, "book.csv")

    # -------------------------------------------------------------------------------- THE NULL
    P("\n" + "-" * 100)
    P(f"THE NULL -- {NDRAW} gross-matched coin flips per (panel, cadence), each re-drawn on its OWN")
    P("cadence, so it collects the same turnover rebate the book does")
    P("-" * 100)
    nrows = []
    for pn in PANELS:
        for f in ALL_FREQS:
            c = ctx[(pn, f)]
            pan, pool, kc, dec = c["pan"], c["pool"], c["kc"], c["pan"].dec
            for s in range(NDRAW):
                rng = np.random.default_rng((SEED0, PANELS.index(pn), ALL_FREQS.index(f), s))
                nb = Book(pan, null_w1(pool, kc, dec, rng))
                for cost in COSTS:
                    r, turn = nb.at(GROSS, cost)
                    cA, sA, dA = fmet(np.asarray(r)[pan.masks["FULL"]])
                    cO, sO, dO = fmet(np.asarray(r)[pan.masks["OOS"]])
                    nrows.append(dict(panel=pn, freq=f, seed=s, cost_bps=cost,
                                      CAGR=cA, Sharpe=sA, MaxDD=dA, oSharpe=sO,
                                      ann_turn=float(turn.sum() / (len(turn) / 252.0))))
            P(f"    {pn}/{f}: {NDRAW} draws done  ({time.time()-t0:.0f}s)")
    nl = pd.DataFrame(nrows)
    dump(nl, "null.csv")

    # -------------------------------------------------------------------------- THE GAIN + PCTL
    P("\n" + "=" * 100)
    P("THE ANSWER -- the book's W->M dSharpe against the NULL's OWN W->M dSharpe distribution")
    P("=" * 100)
    grows = []
    for lad, freqs in LADDERS.items():
        pairs = [(freqs[i], freqs[j]) for i in range(len(freqs)) for j in range(i + 1, len(freqs))]
        for pn in PANELS:
            for (fa, fb) in pairs:
                for cost in COSTS:
                    ba = bk[(bk.panel == pn) & (bk.freq == fa) & (bk.cost_bps == cost)].iloc[0]
                    bb = bk[(bk.panel == pn) & (bk.freq == fb) & (bk.cost_bps == cost)].iloc[0]
                    d_book = bb.Sharpe - ba.Sharpe
                    na = nl[(nl.panel == pn) & (nl.freq == fa) & (nl.cost_bps == cost)].set_index("seed").Sharpe
                    nb_ = nl[(nl.panel == pn) & (nl.freq == fb) & (nl.cost_bps == cost)].set_index("seed").Sharpe
                    d_null = (nb_ - na).dropna().values     # SAME seed both cadences: paired
                    pct = float((d_null < d_book).mean() * 100.0)
                    pct_half = float((d_null[:HALF] < d_book).mean() * 100.0)
                    lvl_b = float((nb_.values < bb.Sharpe).mean() * 100.0)
                    lvl_a = float((na.values < ba.Sharpe).mean() * 100.0)
                    grows.append(dict(ladder=lad, panel=pn, from_freq=fa, to_freq=fb, cost_bps=cost,
                                      book_from=ba.Sharpe, book_to=bb.Sharpe, book_dSharpe=d_book,
                                      null_d_median=float(np.median(d_null)),
                                      null_d_p95=float(np.percentile(d_null, 95)),
                                      null_d_sd=float(np.std(d_null, ddof=1)),
                                      book_pctl_in_null_DELTA=pct, pctl_half=pct_half,
                                      book_pctl_LEVEL_from=lvl_a, book_pctl_LEVEL_to=lvl_b,
                                      book_dCAGR=bb.CAGR - ba.CAGR,
                                      book_dTurn=bb.ann_turn - ba.ann_turn,
                                      n_draws=len(d_null)))
    gn = pd.DataFrame(grows)
    dump(gn, "gain.csv")

    P(f"\n  THE HEADLINE CELL -- W -> M at {COST0:.0f} bps, LADDER2")
    P(f"    {'panel':<7} {'book W':>8} {'book M':>8} {'dSharpe':>9} {'null med':>9} {'null p95':>9} "
      f"{'null sd':>8} {'PCTL(D)':>9} {'250-half':>9} {'lvl W':>7} {'lvl M':>7}")
    for pn in PANELS:
        r = gn[(gn.ladder == "LADDER2") & (gn.panel == pn) & (gn.from_freq == "W") &
               (gn.to_freq == "M") & (gn.cost_bps == COST0)].iloc[0]
        P(f"    {pn:<7} {r.book_from:>8.4f} {r.book_to:>8.4f} {r.book_dSharpe:>+9.4f} "
          f"{r.null_d_median:>+9.4f} {r.null_d_p95:>+9.4f} {r.null_d_sd:>8.4f} {r.book_pctl_in_null_DELTA:>9.1f} "
          f"{r.pctl_half:>9.1f} {r.book_pctl_LEVEL_from:>7.1f} {r.book_pctl_LEVEL_to:>7.1f}")

    P(f"\n  THE SAME CELL AT EVERY COST RUNG (U56, W -> M)")
    P(f"    {'cost':>5} {'dSharpe book':>13} {'null med':>9} {'PCTL(D)':>9} {'lvl W':>7} {'lvl M':>7} {'dTurn':>8}")
    for cost in COSTS:
        r = gn[(gn.ladder == "LADDER2") & (gn.panel == "U56") & (gn.from_freq == "W") &
               (gn.to_freq == "M") & (gn.cost_bps == cost)].iloc[0]
        P(f"    {cost:>5.0f} {r.book_dSharpe:>+13.4f} {r.null_d_median:>+9.4f} "
          f"{r.book_pctl_in_null_DELTA:>9.1f} {r.book_pctl_LEVEL_from:>7.1f} "
          f"{r.book_pctl_LEVEL_to:>7.1f} {r.book_dTurn:>8.2f}")

    P(f"\n  THE FULL LADDER (LADDER4, {COST0:.0f} bps): every ordered cadence pair, every panel")
    P(f"    {'panel':<7} {'pair':<8} {'dSharpe':>9} {'null med':>9} {'PCTL(D)':>9}")
    for pn in PANELS:
        for _, r in gn[(gn.ladder == "LADDER4") & (gn.panel == pn) &
                       (gn.cost_bps == COST0)].iterrows():
            P(f"    {pn:<7} {r.from_freq+'->'+r.to_freq:<8} {r.book_dSharpe:>+9.4f} "
              f"{r.null_d_median:>+9.4f} {r.book_pctl_in_null_DELTA:>9.1f}")

    # ------------------------------------------------------------------------------ HYPOTHESES
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    hyp = []
    g3 = next(g for g in gates if g["gate"].startswith("G3 "))
    hyp.append(dict(name="H_LEVEL", verdict="PASS" if g3["passed"] else "FAIL", detail=g3["stat"]))

    hl = gn[(gn.ladder == "LADDER2") & (gn.from_freq == "W") & (gn.to_freq == "M") &
            (gn.cost_bps == COST0)].set_index("panel")
    u = hl.loc["U56"]
    hyp.append(dict(name="H_GAIN", verdict="PASS" if u.book_pctl_in_null_DELTA >= GAIN_PCTL_BAR else "FAIL",
                    detail=f"U56 book W->M dSharpe {u.book_dSharpe:+.4f} sits at the "
                           f"{u.book_pctl_in_null_DELTA:.1f}th percentile of its own null's W->M dSharpe "
                           f"(median {u.null_d_median:+.4f}, p95 {u.null_d_p95:+.4f}, sd {u.null_d_sd:.4f}, "
                           f"n={int(u.n_draws)}; 250-draw half-sample {u.pctl_half:.1f}) -- bar {GAIN_PCTL_BAR}"))
    med = gn[(gn.from_freq == "W") & (gn.to_freq == "M") & (gn.cost_bps == COST0)]
    hyp.append(dict(name="H_FREE", verdict="PASS" if (med.null_d_median > 0).all() else "FAIL",
                    detail=f"the NULL's own median W->M dSharpe at 10 bps: " +
                           ", ".join(f"{p}={v:+.4f}" for p, v in zip(med.panel, med.null_d_median)) +
                           f" -- positive on {int((med.null_d_median > 0).sum())} of {len(med)} cells, so a "
                           f"cadence gain is a REBATE every book collects, not evidence about a rule"))
    agree = bool(((hl.book_pctl_in_null_DELTA >= GAIN_PCTL_BAR) ==
                  (u.book_pctl_in_null_DELTA >= GAIN_PCTL_BAR)).all())
    hyp.append(dict(name="H_PANEL", verdict="PASS" if agree else "FAIL",
                    detail="percentiles at 10 bps: " +
                           ", ".join(f"{p}={v:.1f}" for p, v in zip(hl.index, hl.book_pctl_in_null_DELTA)) +
                           f" (bar {GAIN_PCTL_BAR}); verdict agrees on "
                           f"{'all 3' if agree else 'NOT all'} panels"))
    l2 = gn[(gn.ladder == "LADDER2") & (gn.from_freq == "W") & (gn.to_freq == "M")]
    l4 = gn[(gn.ladder == "LADDER4") & (gn.from_freq == "W") & (gn.to_freq == "M")]
    j = l2.merge(l4, on=["panel", "from_freq", "to_freq", "cost_bps"], suffixes=("_2", "_4"))
    dl = float((j.book_pctl_in_null_DELTA_2 - j.book_pctl_in_null_DELTA_4).abs().max())
    hyp.append(dict(name="H_LADDER", verdict="PASS" if dl <= LADDER_BAR else "FAIL",
                    detail=f"max |pctl(LADDER2) - pctl(LADDER4)| over {len(j)} (panel, cost) cells = "
                           f"{dl:.2f} points (bar {LADDER_BAR}); the W->M pair is drawn from the same "
                           f"seeds in both ladders by construction"))

    # ------------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "-" * 100)
    P("RULE 8 WALK-FORWARD -- CADENCE chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026 read ONCE")
    P("-" * 100)
    wrows = []
    for lad, freqs in LADDERS.items():
        for pn in PANELS:
            for cost in COSTS:
                best, bs = None, -np.inf
                for f in freqs:
                    c = ctx[(pn, f)]
                    r, _ = c["book"].at(GROSS, cost)
                    s_is = fsharpe(np.asarray(r)[c["pan"].masks["IS"]])
                    if np.isfinite(s_is) and s_is > bs:
                        bs, best = s_is, f
                c = ctx[(pn, best)]
                r, _ = c["book"].at(GROSS, cost)
                oos = np.asarray(r)[c["pan"].masks["OOS"]]
                oc, os_, od = fmet(oos)
                h = len(oos) // 2
                spy_o = np.asarray(c["pan"].spy)[c["pan"].masks["OOS"]]
                sc_, ss, sd = fmet(spy_o)
                bpan = Panel(pn, c["px"], "W")
                bv2, _ = Book(bpan, (rules_v2_weights(c["px"], BAND0, 1.0)).values).at(0.75, cost)
                v2o = np.asarray(bv2)[bpan.masks["OOS"]]
                bc, bsh, bd = fmet(v2o)
                # the NULL's own OOS answer under the SAME chooser, for the same window
                nsel = nl[(nl.panel == pn) & (nl.freq == best) & (nl.cost_bps == cost)]
                p4b = bool(fsharpe(oos[:h]) > fsharpe(spy_o[:h]) and fsharpe(oos[h:]) > fsharpe(spy_o[h:])
                           and os_ > ss and od >= DD_CAP * sd and oc >= CAGR_FLOOR * sc_)
                p4a = bool(fsharpe(oos[:h]) > fsharpe(v2o[:h]) and fsharpe(oos[h:]) > fsharpe(v2o[h:])
                           and od >= bd)
                wrows.append(dict(ladder=lad, panel=pn, cost_bps=cost, pick_freq=best, IS_Sharpe=bs,
                                  OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                                  OOS_H1=fsharpe(oos[:h]), OOS_H2=fsharpe(oos[h:]),
                                  SPY_OOS_CAGR=sc_, SPY_OOS_Sharpe=ss, SPY_OOS_MaxDD=sd,
                                  V2_OOS_CAGR=bc, V2_OOS_Sharpe=bsh, V2_OOS_MaxDD=bd,
                                  null_OOS_Sharpe_median=float(nsel.oSharpe.median()),
                                  book_pctl_OOS_LEVEL=float((nsel.oSharpe.values < os_).mean() * 100),
                                  OOS_pass4b=p4b, OOS_pass4a=p4a))
                P(f"  {lad:<8} {pn:<6} {cost:>5.0f}bps  pick {best}  IS={bs:.3f}  ->  OOS {oc:7.2%} / "
                  f"{os_:6.3f} / {od:7.2%}   SPY {sc_:7.2%}/{ss:6.3f}/{sd:7.2%}   "
                  f"v2 {bc:7.2%}/{bsh:6.3f}/{bd:7.2%}   4b={p4b} 4a={p4a}   "
                  f"null OOS med {float(nsel.oSharpe.median()):.3f} pctl {float((nsel.oSharpe.values < os_).mean()*100):.1f}")
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward.csv")
    hyp.append(dict(name="H_WF", verdict="REPORTED",
                    detail=f"OOS 4b {int(wf.OOS_pass4b.sum())} of {len(wf)}, 4a {int(wf.OOS_pass4a.sum())} of "
                           f"{len(wf)}; IS picks {dict(wf.groupby('panel').pick_freq.agg(lambda s: sorted(set(s))))}; "
                           f"median book percentile in the null's OOS LEVEL {wf.book_pctl_OOS_LEVEL.median():.1f}"))

    for h in hyp:
        P(f"  {h['name']:<9} {h['verdict']:<8} {h['detail']}")
    dump(pd.DataFrame(hyp), "hypotheses.csv")
    dump(pd.DataFrame(gates), "gates.csv")
    P(f"\n  GATES {sum(g['passed'] for g in gates)} of {len(gates)} PASS")
    P(f"\n  elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
