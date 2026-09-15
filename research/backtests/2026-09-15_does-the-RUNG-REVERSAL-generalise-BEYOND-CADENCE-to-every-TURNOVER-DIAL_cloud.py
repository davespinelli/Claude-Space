#!/usr/bin/env python3
"""Idea 945 (cloud, 2026-09-15) -- does the RUNG REVERSAL generalise BEYOND CADENCE to every
TURNOVER DIAL?

THE QUESTION (queue, 2026-09-15)
  Idea 943 found that the gross-matched null's own median W->M CADENCE gain is NEGATIVE at 0 bps
  and POSITIVE at 10 / 25 / 50 bps, so a book that beats its null on 6 of 16 cells at one cost
  rung beats it on 0 of 16 at the next.  If that is a property of SLOWING A BOOK DOWN rather than
  of the cadence axis, then EVERY dial that removes turnover should show the same sign flip, and
  every committed claim that quotes a gain from such a dial at one rung is quoting a number whose
  sign is set by the rung.  This run sweeps the record's other four turnover dials -- GROSS, book
  WIDTH n, ELIGIBILITY tightness and the 200d-MA DRIFT BAND -- for the same reversal.

WHAT A "DIAL" IS HERE
  A dial is one parameter of an otherwise fixed book, moved from a HIGH-turnover setting A to a
  LOW-turnover setting B.  The step direction is declared BEFORE any number is read and then
  CHECKED against realised turnover at G7; a dial that does not actually cut turnover is reported
  as failing its own direction check, never silently flipped.

  D1 CADENCE  CORE/TOP20, g=0.75, max_vol 0.60:   freq   W    -> M      (943's own dial, the control)
  D2 GROSS    CORE/TOP20, freq W, max_vol 0.60:   gross  1.00 -> 0.50
  D3 WIDTH    CORE/TOPn,  freq W, g=0.75:         n      5    -> 20
  D4 ELIG     CORE/TOP20, freq W, g=0.75:         max_vol 0.60 -> 0.35
  D5 BAND     BAND (RULES v2 shape), freq W, g=0.75: band 0.00 -> 0.06

THE BOOKS (both already in the record; NEITHER is re-specified here)
  CORE/TOPn -- each rebalance, rank every priced name above its own 200d MA with 20d realised vol
    < max_vol by the v1 composite mean(pct-rank 12-1 mom, pct-rank 6m, pct-rank 3m) x (1 if above
    the 200d MA else 0.5), WITHOUT the /sqrt(vol20) term; hold the top k = min(n, #eligible) at
    g/k each.  This is idea 670's `CAND20` at n=20, the 2026-09-04 KEEP-4b candidate.
  BAND -- `baseline.rules_v2_weights`: hold every name inside the 200d +/- band hysteresis state at
    g/N of NAV, N = names priced that day; gated-out weight goes to CASH (de-gross, never
    re-spread).  Gated against `rules_v2_weights` itself at G1b.

THE NULL (idea 680's construction, unmodified, generalised to a per-row per-name weight)
  On each DECISION row the book holds k(t) names at a common per-name weight w(t), drawn from the
  candidate pool P(t).  The null holds k(t) names at the SAME w(t), drawn uniformly without
  replacement from that SAME P(t).  Count and per-name weight are copied row by row, so target
  gross, cash drag and the drift path are identical (G2) and the ONLY difference is WHICH names.
  Each side of each dial gets its own null, drawn on ITS OWN setting, so the null collects exactly
  the same turnover rebate the book does -- which is the whole point.
  D2 (GROSS) is the one dial whose two sides share a single draw set evaluated at two gross
  levels, so its null gain carries ZERO draw noise and is a pure cost object.  Stated, not hidden.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  DIAL FAMILY, 5 levels, every one reported: D1..D5 above.
  TUNED 2  COST RUNG, 4 levels, every one reported: 0 / 10 / 25 / 50 bps.
  REPORTED AXES (nothing fitted on them, every point published, none selected):
           PANEL U56 / B136 / SMALL; windows FULL / IS / OOS / H1 / H2; 250 draws per
           (panel, setting) with the 125-draw half-sample printed beside every percentile.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_CTRL   D1 reproduces 943's cadence result on U56: the null's median W->M dSharpe is < 0 at
           0 bps and > 0 at 10, 25 and 50 bps.  Without this the run says nothing about 943.
  H_SIGN   the reversal GENERALISES: on every one of D2..D5 the null's median gain is < 0 at
           0 bps and > 0 at 10 / 25 / 50 bps, on all three panels.
  H_BEAT   the count of cells where the BOOK's gain exceeds its own null's median gain falls
           monotonically as the cost rung rises (943: 6 of 16 -> 0 of 16 between two rungs).
  H_EDGE   at PROTOCOL's own 10 bps rung the book's gain sits at or above the 95th percentile of
           its null's gain distribution on at least one dial.  Below that, no dial's published
           gain is evidence about the RULE.
  H_WF     (rule 8, REQUIRED) the DIAL SETTING is chosen on 2009-2016 ALONE by IS Sharpe and
           2017-2026 is read ONCE, both KEEP paths, against SPY and the live RULES v2 book in the
           same window.

GATES (all printed before any result number)
  G1   the fast runner == `engine.backtest` on returns and turnover (CORE/TOP20, U56, W and M)
  G1b  the BAND book == `baseline.rules_v2_weights(px, band, gross)` exactly
  G2   the null's TARGET gross / holding count / per-name weight == the book's on every row of
       every (panel, setting) cell
  G3   CROSS-RUN: ideas 926 and 931's committed U56 CORE/TOP20 W and M triples
  G4   the draw is legal: |P(t)| >= k(t) on every decision row of every cell
  G5   determinism: the same seed reproduces the same null return series bit-for-bit
  G6   the null is INVESTED in every cell (median realised gross > 0.50, annualised vol > 0.01)
  G7   DIRECTION: every declared dial step actually CUTS realised annual turnover
  G8   SMALL screen: the `max_1d_move` >= 1.0 drop is applied and its count is printed

PROTOCOL: 10 bps primary, t+1 execution, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every
ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL
below is optimistic and both 4b bars are easier here than on a point-in-time panel.  The dial
contrasts are same-tape, same-pool comparisons with one parameter moved and are far less exposed.
The direction for this run's headline works AGAINST the book: a coin flip drawn from a survivor
panel is a BETTER book than one drawn in real time, so the null's gains are an UPPER bound and the
book's percentile inside its null is a LOWER bound -- a FAILING percentile here is a fortiori
failing.  The rule-8 4b levels are read against SPY, which is not survivorship-inflated.
"""
from __future__ import annotations

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
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 10.0, 25.0, 50.0]
NDRAW = 250
HALF = 125
SEED0 = 20260915
GROSS0 = 0.75
PANELS = ["U56", "B136", "SMALL"]
EDGE_PCTL_BAR = 95.0

# committed U56 CORE/TOP20 triples at 10 bps, g=0.75 (ideas 926 / 931)
PUB = {"W": (0.1260, 1.088, -0.1831), "M": (0.1469, 1.203, -0.1951)}
TOL_C, TOL_S, TOL_D = 0.005, 0.030, 0.015

# ---- the five dials: (family, freq, n, max_vol, band) is the SETTING; gross is carried beside it
#      each entry is (label, settingA, grossA, settingB, grossB) with A the HIGH-turnover side
SET = lambda fam, freq, n, mv, bd: (fam, freq, n, mv, bd)
DIALS = [
    ("D1_CADENCE", "freq W->M",        SET("CORE", "W", 20, 0.60, None), GROSS0,
                                       SET("CORE", "M", 20, 0.60, None), GROSS0),
    ("D2_GROSS",   "gross 1.00->0.50", SET("CORE", "W", 20, 0.60, None), 1.00,
                                       SET("CORE", "W", 20, 0.60, None), 0.50),
    ("D3_WIDTH",   "n 5->20",          SET("CORE", "W",  5, 0.60, None), GROSS0,
                                       SET("CORE", "W", 20, 0.60, None), GROSS0),
    ("D4_ELIG",    "max_vol 0.60->0.35", SET("CORE", "W", 20, 0.60, None), GROSS0,
                                         SET("CORE", "W", 20, 0.35, None), GROSS0),
    ("D5_BAND",    "band 0.00->0.06",  SET("BAND", "W", 0, 0.0, 0.00), GROSS0,
                                       SET("BAND", "W", 0, 0.0, 0.06), GROSS0),
]

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
    """Everything about (prices, cadence) that does not depend on which names are held."""

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
        self.dec = np.maximum(self.reb - LAG, 0)   # DECISION rows (decided at t, applied at t+1)
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
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
    """A gross-1.0 weights matrix priced on a Panel; `at(g, cost)` gives net returns + turnover."""

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
        self.ARp = Ap * panel.Rp
        self.Sp = self.ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)

    def at(self, g=GROSS0, cost=COST0):
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gross = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn

    def realised_gross(self, g=GROSS0):
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
                IS_Sharpe=fsharpe(np.asarray(r)[pan.masks["IS"]]),
                oCAGR=co, oSharpe=so, oMaxDD=do)


def legs4b(s, spy):
    L = dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
             L3_OOS=bool(s["oSharpe"] > spy["oSharpe"]),
             L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
             L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    L["pass4b"] = bool(all(L.values()))
    return L


# ================================================================================================
def build_setting(px, setting):
    """(W1, pool, k(t), per-name weight w(t)) for one book setting.  The null needs all four."""
    fam, freq, n, mv, bd = setting
    if fam == "CORE":
        sc, above, vol20 = score(px, vol_scale=False)
        elig = above & (vol20 < mv) & px.notna() & sc.notna()
        sce = sc.where(elig)
        sel = (sce.rank(axis=1, ascending=False) <= n).astype(float)
        k = sel.sum(axis=1)
        wpn = (1.0 / k.replace(0, np.nan)).fillna(0.0).values
        W1 = sel.div(k.replace(0, np.nan), axis=0).fillna(0.0).values
        return W1, elig.values, k.values.astype(int), wpn
    if fam == "BAND":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        npr = e.sum(axis=1).replace(0, np.nan)
        ew = e.div(npr, axis=0).fillna(0.0)                 # per-name weight 1/N_priced
        inb = band_state(px, bd) & px.notna()
        W1 = ew.where(inb, 0.0).values
        k = inb.sum(axis=1)
        wpn = (1.0 / npr).fillna(0.0).values
        return W1, (px.notna()).values, k.values.astype(int), wpn
    raise ValueError(fam)


def null_w1(pool, kc, wpn, dec, rng):
    """Gross-matched coin flip: on each DECISION row draw k(t) names uniformly from P(t) and give
    each the book's own per-name weight w(t).

    `dec` must be the DECISION rows (reb - LAG), not the application rows: `Book` rolls the whole
    weights matrix forward by LAG, so a null written on the application rows would be rolled off
    its own rebalance and silently held as cash.  Gated at G6.
    """
    T, N = pool.shape
    W = np.zeros((T, N))
    for t in dec:
        k = int(kc[t])
        if k <= 0 or wpn[t] <= 0:
            continue
        idx = np.flatnonzero(pool[t])
        if len(idx) == 0:
            continue
        k = min(k, len(idx))
        W[t, rng.choice(idx, size=k, replace=False)] = wpn[t]
    return W


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 945 (cloud) -- does the RUNG REVERSAL generalise BEYOND CADENCE to every TURNOVER DIAL?")
    P("=" * 100)

    # -------------------------------------------------------------------------------- panels
    raw = {}
    raw["U56"] = load_universe()
    raw["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    ndrop = len(bad & set(sm.columns))
    raw["SMALL"] = sm[[c for c in sm.columns if c not in bad]]
    P("\n  panels: " + ", ".join(f"{k} {v.shape[1]} cols x {v.shape[0]} rows "
                                f"[{v.index[0].date()}..{v.index[-1].date()}]" for k, v in raw.items()))
    P(f"  SMALL: dropped {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv "
      f"(SURVIVORSHIP: current constituents of the screen only)")

    # every distinct (panel, setting) cell that any dial touches, built once
    SETTINGS = []
    for _, _, sa, _, sb, _ in DIALS:
        for s in (sa, sb):
            if s not in SETTINGS:
                SETTINGS.append(s)
    P(f"\n  {len(DIALS)} dials over {len(SETTINGS)} distinct book settings x {len(PANELS)} panels "
      f"x {len(COSTS)} cost rungs; {NDRAW} null draws per (panel, setting)")

    ctx = {}
    for pn, px in raw.items():
        for st in SETTINGS:
            W1, pool, kc, wpn = build_setting(px, st)
            pan = Panel(pn, px, st[1])
            ctx[(pn, st)] = dict(pan=pan, book=Book(pan, W1), pool=pool, kc=kc, wpn=wpn,
                                 W1=W1, px=px)
    P(f"  built {len(ctx)} (panel, setting) contexts  ({time.time()-t0:.0f}s)")

    # --------------------------------------------------------------------------------- GATES
    P("\n" + "-" * 100)
    P("GATES (printed before any result number)")
    P("-" * 100)
    gates = []

    # G1 fast runner == engine.backtest, CORE/TOP20 on U56, W and M
    d1 = []
    for st in (SET("CORE", "W", 20, 0.60, None), SET("CORE", "M", 20, 0.60, None)):
        c = ctx[("U56", st)]
        r_f, t_f = c["book"].at(GROSS0, COST0)
        eng = backtest(c["px"], pd.DataFrame(GROSS0 * c["W1"], index=c["px"].index,
                                             columns=c["px"].columns), cost_bps=COST0, freq=st[1])
        m = c["pan"].masks["FULL"]
        d1.append((st[1], float(np.abs(r_f[m] - eng["returns"].values[m]).max()),
                   float(np.abs(t_f[m] - eng["turnover"].values[m]).max())))
    gates.append(dict(gate="G1 fast runner == engine.backtest (CORE/TOP20, U56, W and M)",
                      stat=" | ".join(f"{f}: dret {a:.2e} dturn {b:.2e}" for f, a, b in d1),
                      bar="1e-9", passed=all(a < 1e-9 and b < 1e-9 for _, a, b in d1)))

    # G1b BAND book == rules_v2_weights
    d1b = []
    for bd in (0.00, 0.06):
        c = ctx[("U56", SET("BAND", "W", 0, 0.0, bd))]
        want = rules_v2_weights(c["px"], bd, GROSS0).values
        d1b.append(float(np.abs(GROSS0 * c["W1"] - want).max()))
    gates.append(dict(gate="G1b BAND book == baseline.rules_v2_weights(px, band, 0.75)",
                      stat=f"max|dw| band0.00 {d1b[0]:.3e}, band0.06 {d1b[1]:.3e}",
                      bar="1e-12", passed=bool(max(d1b) < 1e-12)))

    # G2 null target gross / count / per-name weight
    d2t, d2k, d2w = [], [], []
    for pn in PANELS:
        for st in SETTINGS:
            c = ctx[(pn, st)]
            NW = null_w1(c["pool"], c["kc"], c["wpn"], c["pan"].dec, np.random.default_rng(SEED0))
            d = c["pan"].dec
            d2t.append(float(np.abs(NW[d].sum(axis=1) - c["W1"][d].sum(axis=1)).max()))
            d2k.append(int(np.abs((NW[d] > 0).sum(axis=1) - (c["W1"][d] > 0).sum(axis=1)).max()))
            d2w.append(float(np.abs(NW[d].max(axis=1) - c["W1"][d].max(axis=1)).max()))
    gates.append(dict(gate="G2 null TARGET gross / count / per-name weight == book's (every cell)",
                      stat=f"max|dgross| {max(d2t):.3e}, max|dcount| {max(d2k)}, "
                           f"max|dweight| {max(d2w):.3e} over {len(d2t)} cells",
                      bar="1e-12 / 0 / 1e-12",
                      passed=bool(max(d2t) < 1e-12 and max(d2k) == 0 and max(d2w) < 1e-12)))

    # G3 cross-run vs ideas 926 / 931
    g3 = []
    for f, want in PUB.items():
        c = ctx[("U56", SET("CORE", f, 20, 0.60, None))]
        r_f, _ = c["book"].at(GROSS0, COST0)
        m = full_pack(r_f, c["pan"])
        dc, ds, dd = abs(m["CAGR"] - want[0]), abs(m["Sharpe"] - want[1]), abs(m["MaxDD"] - want[2])
        ok = dc < TOL_C and ds < TOL_S and dd < TOL_D
        g3.append(f"{f} {m['CAGR']:.4f}/{m['Sharpe']:.4f}/{m['MaxDD']:.4f} vs committed "
                  f"{want[0]}/{want[1]}/{want[2]} d=({dc:.4f},{ds:.4f},{dd:.4f}) {'OK' if ok else 'MISS'}")
    gates.append(dict(gate="G3 CROSS-RUN ideas 926/931 U56 CORE/TOP20 W and M triples",
                      stat=" | ".join(g3), bar=f"dCAGR<{TOL_C} dSharpe<{TOL_S} dMaxDD<{TOL_D}",
                      passed=all("OK" in s for s in g3)))

    # G4 draw legality
    short_total, worst = 0, None
    for pn in PANELS:
        for st in SETTINGS:
            c = ctx[(pn, st)]
            d = c["pan"].dec
            sh = int((c["pool"][d].sum(axis=1) < c["kc"][d]).sum())
            short_total += sh
            if worst is None or sh > worst[2]:
                worst = (pn, st, sh)
    gates.append(dict(gate="G4 draw legality |P(t)| >= k(t) on every decision row",
                      stat=f"rows short of pool: {short_total} (worst cell {worst[0]}/{worst[1]})",
                      bar="0", passed=bool(short_total == 0)))

    # G5 determinism
    c = ctx[("U56", SET("CORE", "M", 20, 0.60, None))]
    ra, _ = Book(c["pan"], null_w1(c["pool"], c["kc"], c["wpn"], c["pan"].dec,
                                   np.random.default_rng(7))).at()
    rb, _ = Book(c["pan"], null_w1(c["pool"], c["kc"], c["wpn"], c["pan"].dec,
                                   np.random.default_rng(7))).at()
    d5 = float(np.abs(ra - rb).max())
    gates.append(dict(gate="G5 determinism (same seed -> same null)", stat=f"max|d| {d5:.3e}",
                      bar="0.0", passed=bool(d5 == 0.0)))

    # G6 the null is invested everywhere
    d6g, d6s = [], []
    for pn in PANELS:
        for st in SETTINGS:
            c = ctx[(pn, st)]
            nb = Book(c["pan"], null_w1(c["pool"], c["kc"], c["wpn"], c["pan"].dec,
                                        np.random.default_rng(11)))
            r, _ = nb.at()
            m = c["pan"].masks["FULL"]
            d6g.append(float(np.median(nb.realised_gross()[m])))
            d6s.append(float(np.std(r[m], ddof=1) * np.sqrt(252.0)))
    gates.append(dict(gate="G6 the null is INVESTED in every cell (not rolled off its rebalance)",
                      stat=f"min median realised gross {min(d6g):.4f} (book target {GROSS0}), "
                           f"min annualised vol {min(d6s):.4f} over {len(d6g)} cells",
                      bar="gross > 0.50 and vol > 0.01 everywhere",
                      passed=bool(min(d6g) > 0.50 and min(d6s) > 0.01)))

    gates.append(dict(gate="G8 SMALL screen applied", stat=f"dropped {ndrop} tickers "
                      f"(max_1d_move >= 1.0), {raw['SMALL'].shape[1]} columns kept incl. SPY benchmark",
                      bar="> 0 dropped", passed=bool(ndrop > 0)))

    # ------------------------------------------------------------------------------- THE BOOK
    P("\n(gates G7 DIRECTION is printed with the book table below, where turnover is measured)")
    brows = []
    for pn in PANELS:
        spyp = full_pack(ctx[(pn, SETTINGS[0])]["pan"].spy, ctx[(pn, SETTINGS[0])]["pan"])
        for dname, dlabel, sa, ga, sb, gb in DIALS:
            for side, st, g in (("A", sa, ga), ("B", sb, gb)):
                c = ctx[(pn, st)]
                for cost in COSTS:
                    r, turn = c["book"].at(g, cost)
                    m = full_pack(r, c["pan"])
                    brows.append(dict(panel=pn, dial=dname, dial_label=dlabel, side=side,
                                      setting=str(st), gross=g, cost_bps=cost, **m,
                                      ann_turn=float(turn.sum() / (len(turn) / 252.0)),
                                      spy_Sharpe=spyp["Sharpe"], spy_CAGR=spyp["CAGR"],
                                      spy_MaxDD=spyp["MaxDD"], **legs4b(m, spyp)))
    bk = pd.DataFrame(brows)
    dump(bk, "book.csv")

    dirrows = []
    for pn in PANELS:
        for dname, dlabel, *_ in DIALS:
            ta = bk[(bk.panel == pn) & (bk.dial == dname) & (bk.side == "A") &
                    (bk.cost_bps == 0.0)].ann_turn.iloc[0]
            tb = bk[(bk.panel == pn) & (bk.dial == dname) & (bk.side == "B") &
                    (bk.cost_bps == 0.0)].ann_turn.iloc[0]
            dirrows.append(dict(panel=pn, dial=dname, label=dlabel, turn_A=ta, turn_B=tb,
                                ratio=ta / tb if tb else np.nan, cuts=bool(tb < ta)))
    dr = pd.DataFrame(dirrows)
    gates.append(dict(gate="G7 DIRECTION: every declared dial step cuts realised annual turnover",
                      stat=f"{int(dr.cuts.sum())} of {len(dr)} (panel, dial) cells cut turnover; "
                           f"ratio A/B min {dr.ratio.min():.2f} max {dr.ratio.max():.2f}",
                      bar=f"{len(dr)} of {len(dr)}", passed=bool(dr.cuts.all())))

    for g in gates:
        P(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}   (bar {g['bar']})")
    P(f"\n  GATES {sum(g['passed'] for g in gates)} of {len(gates)} PASS")

    P("\n" + "-" * 100)
    P("THE DIALS -- realised annual turnover on each side (0 bps, so turnover is not cost-confounded)")
    P("-" * 100)
    P(f"  {'panel':<6} {'dial':<12} {'step':<22} {'turn A':>8} {'turn B':>8} {'A/B':>7} {'cuts?':>6}")
    for _, r in dr.iterrows():
        P(f"  {r.panel:<6} {r.dial:<12} {r.label:<22} {r.turn_A:>8.2f} {r.turn_B:>8.2f} "
          f"{r.ratio:>7.2f} {str(r.cuts):>6}")
    dump(dr, "direction.csv")

    P("\n" + "-" * 100)
    P(f"THE BOOK on both sides of every dial (U56, {COST0:.0f} bps shown; every rung in book.csv)")
    P("-" * 100)
    P(f"  {'dial':<12} {'side':<5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'annTurn':>8} {'4b':>6}")
    for dname, _, *_ in DIALS:
        for side in ("A", "B"):
            r = bk[(bk.panel == "U56") & (bk.dial == dname) & (bk.side == side) &
                   (bk.cost_bps == COST0)].iloc[0]
            P(f"  {dname:<12} {side:<5} {r.CAGR:>8.2%} {r.Sharpe:>8.4f} {r.MaxDD:>8.2%} "
              f"{r.ann_turn:>8.2f} {str(bool(r.pass4b)):>6}")

    # -------------------------------------------------------------------------------- THE NULL
    P("\n" + "-" * 100)
    P(f"THE NULL -- {NDRAW} gross-matched coin flips per (panel, setting), each drawn on ITS OWN")
    P("setting, so it collects the same turnover rebate the book does")
    P("-" * 100)
    nrows = []
    for pn in PANELS:
        for si, st in enumerate(SETTINGS):
            c = ctx[(pn, st)]
            pan, pool, kc, wpn, dec = c["pan"], c["pool"], c["kc"], c["wpn"], c["pan"].dec
            for s in range(NDRAW):
                rng = np.random.default_rng((SEED0, PANELS.index(pn), si, s))
                nb = Book(pan, null_w1(pool, kc, wpn, dec, rng))
                for g in sorted({ga for _, _, sa, ga, sb, gb in DIALS if sa == st} |
                                {gb for _, _, sa, ga, sb, gb in DIALS if sb == st}):
                    for cost in COSTS:
                        r, turn = nb.at(g, cost)
                        cA, sA, dA = fmet(np.asarray(r)[pan.masks["FULL"]])
                        cO, sO, dO = fmet(np.asarray(r)[pan.masks["OOS"]])
                        nrows.append(dict(panel=pn, setting=str(st), gross=g, seed=s,
                                          cost_bps=cost, CAGR=cA, Sharpe=sA, MaxDD=dA,
                                          oSharpe=sO, oCAGR=cO, oMaxDD=dO,
                                          ann_turn=float(turn.sum() / (len(turn) / 252.0))))
            P(f"    {pn}/{st}: {NDRAW} draws done  ({time.time()-t0:.0f}s)")
    nl = pd.DataFrame(nrows)
    dump(nl, "null.csv")

    # ---------------------------------------------------------------------- THE GAIN, PER RUNG
    P("\n" + "=" * 100)
    P("THE ANSWER -- each dial's BOOK gain against its own NULL's gain, at every cost rung")
    P("=" * 100)
    grows = []
    for pn in PANELS:
        for dname, dlabel, sa, ga, sb, gb in DIALS:
            for cost in COSTS:
                ba = bk[(bk.panel == pn) & (bk.dial == dname) & (bk.side == "A") &
                        (bk.cost_bps == cost)].iloc[0]
                bb = bk[(bk.panel == pn) & (bk.dial == dname) & (bk.side == "B") &
                        (bk.cost_bps == cost)].iloc[0]
                d_book = bb.Sharpe - ba.Sharpe
                na = nl[(nl.panel == pn) & (nl.setting == str(sa)) & (nl.gross == ga) &
                        (nl.cost_bps == cost)].set_index("seed").Sharpe
                nb_ = nl[(nl.panel == pn) & (nl.setting == str(sb)) & (nl.gross == gb) &
                         (nl.cost_bps == cost)].set_index("seed").Sharpe
                d_null = (nb_ - na).dropna().values          # paired by seed index
                pct = float((d_null < d_book).mean() * 100.0)
                grows.append(dict(panel=pn, dial=dname, label=dlabel, cost_bps=cost,
                                  book_A=ba.Sharpe, book_B=bb.Sharpe, book_gain=d_book,
                                  null_gain_median=float(np.median(d_null)),
                                  null_gain_p95=float(np.percentile(d_null, 95)),
                                  null_gain_sd=float(np.std(d_null, ddof=1)),
                                  book_pctl_in_null=pct,
                                  pctl_half=float((d_null[:HALF] < d_book).mean() * 100.0),
                                  excess=d_book - float(np.median(d_null)),
                                  beats_null=bool(d_book > float(np.median(d_null))),
                                  dTurn=bb.ann_turn - ba.ann_turn,
                                  turn_ratio=ba.ann_turn / bb.ann_turn if bb.ann_turn else np.nan,
                                  book_dCAGR=bb.CAGR - ba.CAGR, n_draws=len(d_null)))
    gn = pd.DataFrame(grows)
    dump(gn, "gain.csv")

    P("\n  THE NULL'S OWN MEDIAN GAIN, by dial x cost rung (the rung-reversal table)")
    for pn in PANELS:
        P(f"\n    {pn}")
        P(f"      {'dial':<12} {'step':<22} " + " ".join(f"{c:>10.0f}bps" for c in COSTS) + "   sign flip 0->10?")
        for dname, dlabel, *_ in DIALS:
            v = [gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == c)].null_gain_median.iloc[0]
                 for c in COSTS]
            flip = bool(v[0] < 0 and all(x > 0 for x in v[1:]))
            P(f"      {dname:<12} {dlabel:<22} " + " ".join(f"{x:>+13.4f}" for x in v) +
              f"   {'YES' if flip else 'no'}")

    P("\n  THE BOOK'S OWN GAIN, same cells (so the two can be read side by side)")
    for pn in PANELS:
        P(f"\n    {pn}")
        P(f"      {'dial':<12} " + " ".join(f"{c:>10.0f}bps" for c in COSTS))
        for dname, *_ in DIALS:
            v = [gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == c)].book_gain.iloc[0]
                 for c in COSTS]
            P(f"      {dname:<12} " + " ".join(f"{x:>+13.4f}" for x in v))

    P(f"\n  THE EXCESS (book gain minus null median gain) and the book's percentile in its null")
    P(f"    {'panel':<6} {'dial':<12} {'cost':>5} {'book':>9} {'null med':>9} {'excess':>9} "
      f"{'pctl':>7} {'half':>7} {'beats':>6}")
    for pn in PANELS:
        for dname, *_ in DIALS:
            for cost in COSTS:
                r = gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == cost)].iloc[0]
                P(f"    {pn:<6} {dname:<12} {cost:>5.0f} {r.book_gain:>+9.4f} "
                  f"{r.null_gain_median:>+9.4f} {r.excess:>+9.4f} {r.book_pctl_in_null:>7.1f} "
                  f"{r.pctl_half:>7.1f} {str(r.beats_null):>6}")

    P("\n  CELLS WHERE THE BOOK BEATS ITS OWN NULL, by cost rung (943's 6-of-16 -> 0-of-16 object)")
    P(f"    {'cost':>5} {'beats':>8} {'of':>4}   {'mean excess':>12} {'median pctl':>12}")
    beat_by_rung = []
    for cost in COSTS:
        sub = gn[gn.cost_bps == cost]
        beat_by_rung.append(int(sub.beats_null.sum()))
        P(f"    {cost:>5.0f} {int(sub.beats_null.sum()):>8} {len(sub):>4}   "
          f"{sub.excess.mean():>+12.4f} {sub.book_pctl_in_null.median():>12.1f}")

    # ------------------------------------------------------------------------------ HYPOTHESES
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    hyp = []

    def flips(pn, dname):
        v = [gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == c)].null_gain_median.iloc[0]
             for c in COSTS]
        return bool(v[0] < 0 and all(x > 0 for x in v[1:])), v

    ok, v = flips("U56", "D1_CADENCE")
    hyp.append(dict(name="H_CTRL", verdict="PASS" if ok else "FAIL",
                    detail=f"D1_CADENCE on U56, null median gain at 0/10/25/50 bps = " +
                           ", ".join(f"{x:+.4f}" for x in v) +
                           f" -- 943's reversal {'reproduces' if ok else 'DOES NOT reproduce'}"))

    gen = {}
    for dname, *_ in DIALS:
        if dname == "D1_CADENCE":
            continue
        gen[dname] = {pn: flips(pn, dname)[0] for pn in PANELS}
    nall = sum(all(d.values()) for d in gen.values())
    ncell = sum(sum(d.values()) for d in gen.values())
    hyp.append(dict(name="H_SIGN", verdict="PASS" if nall == len(gen) else "FAIL",
                    detail=f"the reversal holds on {nall} of {len(gen)} non-cadence dials across ALL "
                           f"three panels ({ncell} of {3*len(gen)} (dial, panel) cells): " +
                           "; ".join(f"{k} " + "/".join(f"{p}={'Y' if v else 'n'}" for p, v in d.items())
                                     for k, d in gen.items())))

    mono = all(beat_by_rung[i] >= beat_by_rung[i + 1] for i in range(len(beat_by_rung) - 1))
    hyp.append(dict(name="H_BEAT", verdict="PASS" if mono else "FAIL",
                    detail=f"cells where the book's gain beats its null's median, by rung "
                           f"0/10/25/50 bps: " + " -> ".join(f"{b} of {len(gn)//len(COSTS)}"
                                                             for b in beat_by_rung) +
                           f" -- {'monotone falling' if mono else 'NOT monotone'}"))

    at10 = gn[gn.cost_bps == COST0]
    best = at10.loc[at10.book_pctl_in_null.idxmax()]
    hyp.append(dict(name="H_EDGE", verdict="PASS" if best.book_pctl_in_null >= EDGE_PCTL_BAR else "FAIL",
                    detail=f"highest percentile at {COST0:.0f} bps over all {len(at10)} (panel, dial) "
                           f"cells: {best.panel}/{best.dial} at {best.book_pctl_in_null:.1f} "
                           f"(half-sample {best.pctl_half:.1f}, book gain {best.book_gain:+.4f} vs null "
                           f"median {best.null_gain_median:+.4f}, n={int(best.n_draws)}) -- bar "
                           f"{EDGE_PCTL_BAR}; cells at or above the bar: "
                           f"{int((at10.book_pctl_in_null >= EDGE_PCTL_BAR).sum())} of {len(at10)}"))

    # ------------------------------------------------------------------------- RESTATEMENT
    # POST-HOC, written after H_CTRL failed AS WRITTEN.  It moves no bar and selects no cell: it
    # restates 943's own aggregation (a MEDIAN OVER ITS CELL FAMILY, not a single cell) on this
    # run's dial families, so the two runs' headline statistics are read like for like.
    P("\n" + "-" * 100)
    P("RESTATEMENT (POST-HOC, selects nothing, moves no bar)")
    P("943's published headline is a MEDIAN OVER ITS 16 (panel, template, step) CELLS -- rescore.csv")
    P("gives null_med_gain_median -0.0279 / +0.4560 / +1.1241 / +2.1333 at 0/10/25/50 bps with only")
    P("2 of 16 cells positive at 0 bps.  H_CTRL was pre-registered on the SINGLE U56 W->M cell, which")
    P("is one of those 2 positive cells, so it fails as written.  Below is 943's own aggregation")
    P("computed on THIS run's 15 (panel, dial) cells.")
    P("-" * 100)
    P(f"    {'rung':>5} {'median null gain':>17} {'cells > 0':>10} {'of':>4}   "
      f"{'cadence-only median':>20} {'non-cadence median':>19}")
    for cost in COSTS:
        s = gn[gn.cost_bps == cost]
        sc_ = s[s.dial == "D1_CADENCE"].null_gain_median
        sn = s[s.dial != "D1_CADENCE"].null_gain_median
        P(f"    {cost:>5.0f} {s.null_gain_median.median():>+17.4f} "
          f"{int((s.null_gain_median > 0).sum()):>10} {len(s):>4}   {sc_.median():>+20.4f} "
          f"{sn.median():>+19.4f}")

    P("\n  WHICH WAY EACH DIAL ACTUALLY FLIPS between 0 and 10 bps (the queue asked for one shape;")
    P("  the record's dials show three)")
    P(f"    {'panel':<6} {'dial':<12} {'0 bps':>9} {'10 bps':>9}   shape")
    shapes = []
    for pn in PANELS:
        for dname, *_ in DIALS:
            v0 = gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == 0.0)].null_gain_median.iloc[0]
            v10 = gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == COST0)].null_gain_median.iloc[0]
            sh = ("NEG->POS (the queue's shape)" if v0 < 0 <= v10 else
                  "POS->NEG (the opposite flip)" if v0 > 0 > v10 else
                  "positive at both rungs" if v0 > 0 else "negative at both rungs")
            shapes.append(dict(panel=pn, dial=dname, g0=v0, g10=v10, shape=sh))
            P(f"    {pn:<6} {dname:<12} {v0:>+9.4f} {v10:>+9.4f}   {sh}")
    sh = pd.DataFrame(shapes)
    dump(sh, "shapes.csv")
    P("\n    shape counts over the 15 cells: " +
      ", ".join(f"[{k}] = {v}" for k, v in sh["shape"].value_counts().items()))

    # the mechanism: it is the NULL's OWN turnover drop, not the book's, that sets the rebate
    P("\n  THE MECHANISM -- the rebate is priced off the NULL's OWN turnover drop, not the book's")
    P(f"    {'panel':<6} {'dial':<12} {'book dTurn':>11} {'null dTurn':>11} {'predicted':>10} "
      f"{'observed':>10}   (gain at 10 bps minus gain at 0 bps)")
    mrows = []
    for pn in PANELS:
        for dname, dlabel, sa, ga, sb, gb in DIALS:
            na = nl[(nl.panel == pn) & (nl.setting == str(sa)) & (nl.gross == ga) &
                    (nl.cost_bps == 0.0)].ann_turn.median()
            nb_ = nl[(nl.panel == pn) & (nl.setting == str(sb)) & (nl.gross == gb) &
                     (nl.cost_bps == 0.0)].ann_turn.median()
            r0 = gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == 0.0)].iloc[0]
            r10 = gn[(gn.panel == pn) & (gn.dial == dname) & (gn.cost_bps == COST0)].iloc[0]
            # predicted gain shift = (null turnover drop) x cost / annualised vol of the null book
            spn = ctx[(pn, sa)]
            rr, _ = Book(spn["pan"], null_w1(spn["pool"], spn["kc"], spn["wpn"], spn["pan"].dec,
                                             np.random.default_rng((SEED0, PANELS.index(pn), 0, 0)))).at(ga, 0.0)
            volN = float(np.std(rr[spn["pan"].masks["FULL"]], ddof=1) * np.sqrt(252.0))
            pred = (na - nb_) * COST0 / 1e4 / volN
            obs = r10.null_gain_median - r0.null_gain_median
            mrows.append(dict(panel=pn, dial=dname, book_dTurn=r0.dTurn, null_dTurn=nb_ - na,
                              null_vol=volN, predicted=pred, observed=obs))
            P(f"    {pn:<6} {dname:<12} {r0.dTurn:>+11.2f} {nb_-na:>+11.2f} {pred:>+10.4f} {obs:>+10.4f}")
    mm = pd.DataFrame(mrows)
    dump(mm, "mechanism.csv")
    rho_m = float(np.corrcoef(mm.predicted, mm.observed)[0, 1])
    P(f"    corr(predicted, observed) over the {len(mm)} cells = {rho_m:+.4f}; "
      f"median |predicted - observed| = {float((mm.predicted - mm.observed).abs().median()):.4f}")

    d = gn[gn.cost_bps > 0].copy()
    d["drag_drop"] = -d.dTurn * d.cost_bps / 1e4
    rho = float(np.corrcoef(d.drag_drop, d.null_gain_median)[0, 1])
    P(f"\n  corr(null median gain, BOOK turnover drop x cost) over the {len(d)} non-zero-cost cells "
      f"= {rho:+.4f} -- the book's own turnover drop is the WRONG regressor; the null's is "
      f"{rho_m:+.4f}")

    # ------------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "-" * 100)
    P("RULE 8 WALK-FORWARD -- the DIAL SETTING chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026")
    P("read ONCE.  Both KEEP paths, against SPY and the live RULES v2 book in the same window.")
    P("-" * 100)
    wrows = []
    for pn in PANELS:
        px = raw[pn]
        bpan = Panel(pn, px, "W")
        v2 = Book(bpan, rules_v2_weights(px, 0.03, 1.0).values)
        for dname, dlabel, sa, ga, sb, gb in DIALS:
            for cost in COSTS:
                cand = []
                for side, st, g in (("A", sa, ga), ("B", sb, gb)):
                    c = ctx[(pn, st)]
                    r, _ = c["book"].at(g, cost)
                    cand.append((fsharpe(np.asarray(r)[c["pan"].masks["IS"]]), side, st, g, r, c))
                cand = [x for x in cand if np.isfinite(x[0])]
                sis, side, st, g, r, c = max(cand, key=lambda x: x[0])
                pan = c["pan"]
                oos = np.asarray(r)[pan.masks["OOS"]]
                oc, os_, od = fmet(oos)
                h = len(oos) // 2
                spy_o = np.asarray(pan.spy)[pan.masks["OOS"]]
                sc_, ss, sd = fmet(spy_o)
                rv2, _ = v2.at(GROSS0, cost)
                v2o = np.asarray(rv2)[bpan.masks["OOS"]]
                bc, bsh, bdd = fmet(v2o)
                p4b = bool(fsharpe(oos[:h]) > fsharpe(spy_o[:h]) and
                           fsharpe(oos[h:]) > fsharpe(spy_o[h:]) and os_ > ss and
                           od >= DD_CAP * sd and oc >= CAGR_FLOOR * sc_)
                p4a = bool(fsharpe(oos[:h]) > fsharpe(v2o[:h]) and
                           fsharpe(oos[h:]) > fsharpe(v2o[h:]) and od >= bdd)
                ns = nl[(nl.panel == pn) & (nl.setting == str(st)) & (nl.gross == g) &
                        (nl.cost_bps == cost)]
                wrows.append(dict(panel=pn, dial=dname, label=dlabel, cost_bps=cost,
                                  pick_side=side, pick_setting=str(st), pick_gross=g,
                                  IS_Sharpe=sis, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                                  OOS_H1=fsharpe(oos[:h]), OOS_H2=fsharpe(oos[h:]),
                                  SPY_OOS_CAGR=sc_, SPY_OOS_Sharpe=ss, SPY_OOS_MaxDD=sd,
                                  V2_OOS_CAGR=bc, V2_OOS_Sharpe=bsh, V2_OOS_MaxDD=bdd,
                                  null_OOS_Sharpe_median=float(ns.oSharpe.median()),
                                  book_pctl_OOS=float((ns.oSharpe.values < os_).mean() * 100),
                                  OOS_pass4b=p4b, OOS_pass4a=p4a))
                P(f"  {pn:<6} {dname:<12} {cost:>5.0f}bps  pick {side} ({st[1]},n={st[2]},"
                  f"mv={st[3]},bd={st[4]},g={g})  IS={sis:.3f} -> OOS {oc:7.2%} / {os_:6.3f} / "
                  f"{od:7.2%}   SPY {sc_:7.2%}/{ss:6.3f}/{sd:7.2%}   v2 {bc:7.2%}/{bsh:6.3f}/"
                  f"{bdd:7.2%}   4b={p4b} 4a={p4a}   null OOS med {float(ns.oSharpe.median()):.3f} "
                  f"pctl {float((ns.oSharpe.values < os_).mean()*100):.1f}")
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward.csv")
    hyp.append(dict(name="H_WF", verdict="REPORTED",
                    detail=f"OOS 4b {int(wf.OOS_pass4b.sum())} of {len(wf)}, 4a "
                           f"{int(wf.OOS_pass4a.sum())} of {len(wf)}; the IS chooser picks the "
                           f"LOW-turnover side B in {int((wf.pick_side=='B').sum())} of {len(wf)} "
                           f"cells; median book percentile in its null's OOS LEVEL "
                           f"{wf.book_pctl_OOS.median():.1f}"))

    P("\n  RULE 8 SUMMARY by panel (all cost rungs, all dials)")
    P(f"    {'panel':<6} {'best OOS pick':<34} {'OOS CAGR':>9} {'Sharpe':>8} {'MaxDD':>8} "
      f"{'SPY CAGR':>9} {'SPY Sh':>7} {'SPY DD':>8} {'4b':>5}")
    for pn in PANELS:
        s = wf[wf.panel == pn]
        r = s.loc[s.OOS_Sharpe.idxmax()]
        P(f"    {pn:<6} {r.dial+' @'+str(int(r.cost_bps))+'bps side '+r.pick_side:<34} "
          f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>8.3f} {r.OOS_MaxDD:>8.2%} {r.SPY_OOS_CAGR:>9.2%} "
          f"{r.SPY_OOS_Sharpe:>7.3f} {r.SPY_OOS_MaxDD:>8.2%} {str(bool(r.OOS_pass4b)):>5}")

    # ------------------------------------------------- WHICH COMMITTED CLAIMS SIT ON THE RUNG
    P("\n" + "-" * 100)
    P("WHICH COMMITTED CLAIMS SIT ON THE WRONG SIDE OF THEIR OWN RUNG")
    P("(a KEYWORD census of the committed record; its denominator and tree are stamped, and it")
    P("is a POINTER to claims that need re-scoring, not a re-scoring of them)")
    P("-" * 100)
    import subprocess
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip() or "unknown"
    KEY = {"D1_CADENCE": ["cadence", "freq", "weekly", "monthly", "quarterly", "rebalance"],
           "D2_GROSS": ["gross"], "D3_WIDTH": ["book size", "book width", "top20", "top5", "top10",
                                               "n dial", "width"],
           "D4_ELIG": ["eligib", "max_vol", "vol filter", "threshold"],
           "D5_BAND": ["band", "drift", "hysteresis"]}
    crows = []
    for fname in ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md"):
        lines = (ROOT / "research" / fname).read_text().lower().split("\n")
        for dname, keys in KEY.items():
            n = sum(1 for ln in lines if any(k in ln for k in keys))
            crows.append(dict(file=fname, dial=dname, lines_matching=n, n_lines=len(lines)))
    cen = pd.DataFrame(crows)
    dump(cen, "census.csv")
    P(f"  tree {sha}; keyword lines in the committed record (a line may match more than one dial)")
    P(f"    {'file':<16} " + " ".join(f"{d:>12}" for d, *_ in DIALS) + f" {'lines':>8}")
    for fname in ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md"):
        s = cen[cen.file == fname].set_index("dial")
        P(f"    {fname:<16} " + " ".join(f"{int(s.loc[d].lines_matching):>12}" for d, *_ in DIALS) +
          f" {int(s.iloc[0].n_lines):>8}")
    P("\n  RE-SCORING RULE implied by the table above (proposed, NOT applied -- PROTOCOL rule 6):")
    for dname, dlabel, *_ in DIALS:
        v0 = gn[(gn.panel == "U56") & (gn.dial == dname) & (gn.cost_bps == 0.0)].null_gain_median.iloc[0]
        v10 = gn[(gn.panel == "U56") & (gn.dial == dname) & (gn.cost_bps == COST0)].null_gain_median.iloc[0]
        P(f"    {dname:<12} {dlabel:<22} null median gain {v0:+.4f} at 0 bps -> {v10:+.4f} at 10 bps"
          f"  => any published {dname.split('_')[1]} gain smaller than {abs(v10):.4f} of Sharpe at "
          f"10 bps is inside the rebate a coin flip collects")

    for h in hyp:
        P(f"  {h['name']:<9} {h['verdict']:<8} {h['detail']}")
    dump(pd.DataFrame(hyp), "hypotheses.csv")
    dump(pd.DataFrame(gates), "gates.csv")
    P(f"\n  GATES {sum(g['passed'] for g in gates)} of {len(gates)} PASS")
    P(f"\n  elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
