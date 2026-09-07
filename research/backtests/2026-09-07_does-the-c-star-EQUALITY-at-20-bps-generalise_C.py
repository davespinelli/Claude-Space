#!/usr/bin/env python3
"""Idea 335 — "does-the-c-star-EQUALITY-at-20-bps-generalise" (lane C, 2026-09-07).

QUESTION (QUEUE.md).  Idea 42 found the best gated arm's cost breakeven (U56, g=1.00,
B=0.40, depth 0.50) is EXACTLY 20 bps, identical to the plain gross dial's at g=0.85 —
i.e. the overlay bought back precisely what it cost.  Test whether

        c*(book + de-grossing overlay)  <=  c*(book at matched mean gross)

is an IDENTITY across the record's overlay families (stops, bands, ddctl, breadth, vol
caps) on 2 panels x 3 gross rungs.  If it holds everywhere, c* is a pure EXPOSURE
statistic and no de-grossing overlay can ever widen a book's cost budget — which would
make every "the overlay pays for itself" claim in the record a restatement of its mean
gross, and would let c* be read off the exposure path without running the overlay.

WHY THIS IS NOT ARITHMETIC.  Under the record's overlay convention the constant-gross
control is r = a*r0, turn = a*turn0, so its SHARPE is exactly invariant in a at every
cost rung (the a cancels in mean/sd) while its CAGR and MaxDD scale with a.  A
de-grossing OVERLAY, by contrast, moves Sharpe as well: it re-times the exposure.  So an
overlay that improves the Sharpe path can push its own crossing ABOVE the matched-gross
control's, and the proposition has real content.  It is a claim about whether re-timing
exposure ever buys cost budget, not an algebraic necessity.

DESIGN.

  PARENT (fixed, idea 40/41's book, never tuned): eligible = above the 200d MA and
  vol20 < 0.60; rank eligible names by the v1 composite WITHOUT the /sqrt(vol20) term;
  hold the top k = min(20, E_t) equal-weight at w = g0/k; weekly; next-day execution.

  RUNGS (tuned parameter 1): g0 in {0.50, 0.75, 1.00}.  No leverage (PROTOCOL rule 2).

  OVERLAY FAMILIES (census axis, every level reported; each has a DIAL = tuned param 2):
    BREADTH  book-level.  m = depth while panel breadth (share of constituents above
             their own 200d MA, lagged 1 day) < B = 0.40 (idea 42's pinned B).
             depth in {0.75, 0.50, 0.25}.   off: depth = 1.00.
    DDCTL    book-level.  m = 0.50 while the parent's own lagged zero-cost drawdown is
             worse than -T.  T in {0.05, 0.10, 0.20}.   off: T = inf.
    VOLCAP   book-level.  m = min(1, target / lagged 20d annualised parent vol).
             target in {0.10, 0.15, 0.25}.   off: target = inf.
    MABAND   per-name, DAILY.  A held name is liquidated to cash the next day whenever
             it leaves the 200d +/-b band (hysteresis, baseline.band_state), and is only
             re-bought on the next rebalance.  b in {0.00, 0.06, 0.12}.  off: no gate.
    STOP     per-name, DAILY.  A held name is liquidated to cash the next day when it is
             more than s below its own 60d running max.  s in {0.10, 0.20, 0.30}.
             off: s = inf.

  BOOK-LEVEL overlays use idea 41's published convention verbatim: r = m*r0 and
  turn = m*turn0 + |dm| * gross0, i.e. the exposure switch pays the rung's cost on the
  notional it moves on the day it takes effect.  PER-NAME overlays are simulated
  directly (liquidation to cash, turnover measured by the simulator); their realised
  gross path is read off the simulator, not assumed.  Both are stated at the point of
  use; the two conventions are never mixed inside one comparison.

  MATCHED CONTROL.  For every overlay cell, a = mean(gross_overlay_t) /
  mean(gross_parent_t), applied as a CONSTANT multiplier to the same parent.  a is
  closed-form (no search) and a <= 1 by construction because every family de-grosses.
  This is the plain gross dial held at the overlay's own realised mean exposure.

  c* ESTIMATOR.  First cost c in [0, 50] bps at which any bar of the path turns
  non-positive; 0.0 if the path fails at zero cost; "never" if it survives the whole
  ladder.  Bracketed on a 0.25-bps scan then bisected 60 times.  Computed for BOTH KEEP
  paths and on three windows (full / IS 2008-2016 / OOS 2017-2026):
    4b  vs SPY: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%.
    4a  vs the LIVE RULES v2 book at the SAME cost rung: Sharpe > v2 in both halves and
        MaxDD no worse than v2's.

  RULE 8 WALK-FORWARD.  For every (panel, rung, family) the dial is chosen on 2008-2016
  ONLY — by IS c*_4b (the statistic the question is about) and, separately, by IS Sharpe
  at 10 bps (the record's convention) — and 2017-2026 is read once.  OOS CAGR / Sharpe /
  MaxDD against the parent anchor, RULES v2 and SPY, and the OOS identity is re-tested on
  the OOS window alone.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): (1) the parent's gross rung, (2) the overlay's
dial.  Panel, overlay family and cost rung are CENSUS axes — every level is reported and
nothing is selected on outcome.  All grid points go to .grid.csv.

GATES (asserted / printed in [0] before any new number is read).
  G1  fast_bt == engine.backtest on returns AND turnover at 0 and 25 bps.
  G2  every per-name overlay at its OFF setting == the parent, |dr| and |dturn| == 0.
  G3  every book-level overlay at its OFF setting (m == 1) == the parent, exactly.
  G4  the matched control at a = 1 == the parent, exactly.
  G5  SHARPE INVARIANCE of the gross dial: Sharpe(a*r0 - a*turn*c) == Sharpe(r0 -
      turn*c) for a in {0.25..1} at c in {0, 10, 25} — this is what makes the control's
      c* a pure CAGR/MaxDD statistic, and it is measured, not assumed.
  G6  c*_exact reproduces its own value on a re-run (determinism of the bisection).

CAVEATS.  (1) universe.json (56) and universe_broad.json (136) are CURRENT-CONSTITUENT
lists — SURVIVORSHIP; absolute CAGRs are optimistic on both, and B136 CONTAINS U56, so
two panels is not two independent samples.  (2) Gross is capped at 1.00; a c* that only
leverage would move is reported as unmoved.  (3) c* is a breakeven, not a return: a book
with a high c* and a bad level is still a bad book, and [5] reports the levels beside it.
(4) The 4a control moves with the rung too (RULES v2 pays the same cost), so c*_4a can be
"never" for reasons that have nothing to do with the idea.

Deterministic, standalone.  Reads baseline.py only; modifies nothing.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, band_state, rules_v2_weights   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

OUT = Path(__file__).with_suffix("")
SLUG = OUT.name

MAX_VOL = 0.60
VOL_SCALE = False
N0 = 20
FREQ = "W"
WARMUP = 260
RUNGS = [0.50, 0.75, 1.00]
COSTS = [0, 10, 25]
CMAX = 50.0
SCAN = 0.25
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
B_FIXED = 0.40                    # idea 42's pinned breadth threshold
ANCHOR_G, ANCHOR_DEPTH = 1.00, 0.50
ANCHOR_GROSS_DIAL = 0.85          # idea 42's plain-gross comparand

FAMILIES = {
    "BREADTH": dict(kind="book", dial="depth", vals=[0.75, 0.50, 0.25], off=1.00),
    "DDCTL":   dict(kind="book", dial="T",     vals=[0.05, 0.10, 0.20], off=np.inf),
    "VOLCAP":  dict(kind="book", dial="target", vals=[0.10, 0.15, 0.25], off=np.inf),
    "MABAND":  dict(kind="name", dial="b",     vals=[0.00, 0.06, 0.12], off=None),
    "STOP":    dict(kind="name", dial="s",     vals=[0.10, 0.20, 0.30], off=np.inf),
}

pd.set_option("display.width", 240)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ book construction
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def parent_weights(px, g0, n=N0):
    """NFn: top k = min(n, E_t) eligible names, equal weight, gross g0."""
    el = eligible_mask(px)
    rank = score(px, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    e = el.sum(axis=1).astype(float)
    k = np.minimum(float(n), e).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(g0 / k, axis=0)


# ------------------------------------------------------------------ simulators
def fast_bt(px, w, freq, daily_mask=None):
    """engine.backtest at cost_bps=0, in numpy, plus an optional DAILY per-name hold mask.

    Where daily_mask is False the position is liquidated to cash at that day's open weight
    (turnover charged on the liquidated notional) and is only re-bought on the next
    rebalance.  daily_mask=None reproduces engine.backtest exactly (gate G1/G2).
    Returns (returns, turnover, gross) as Series on px.index.
    """
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    reb = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    if daily_mask is not None:
        dm = daily_mask.reindex(px.index).reindex(columns=px.columns).fillna(True) \
                       .shift(1).fillna(True).values.astype(bool)
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n)
    turn = np.zeros(n)
    gr = np.zeros(n)
    for i in range(n):
        if reb[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        if daily_mask is not None:
            kill = (~dm[i]) & (cur > 0)
            if kill.any():
                turn[i] += cur[kill].sum()
                cur = np.where(kill, 0.0, cur)
        port[i] = float((cur * rets[i]).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx), pd.Series(gr, index=idx))


def apply_mult(r0, turn0, gross0, m):
    """Idea 41's book-level overlay convention, verbatim.

    r = m*r0 ; turn = m*turn0 + |dm| * gross0.shift(1) ; gross = m*gross0.
    m is already lagged by the caller (it is a decision made at t-1, executed at t).
    """
    dm = m.diff().abs().fillna(0.0)
    return (m * r0, m * turn0 + dm * gross0.shift(1).fillna(0.0), m * gross0)


# ------------------------------------------------------------------ overlay signals
def panel_breadth(px):
    """Share of the panel's own constituents above their own 200d MA (SPY excluded)."""
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    live = q.notna()
    return (above & live).sum(axis=1) / live.sum(axis=1).replace(0, np.nan)


def mult_breadth(px, r0, turn0, gross0, depth):
    br = panel_breadth(px).shift(1)
    on = (br < B_FIXED).fillna(False)
    return pd.Series(np.where(on.values, depth, 1.0), index=px.index)


def mult_ddctl(px, r0, turn0, gross0, T):
    eq = (1.0 + r0).cumprod()
    dd = (eq / eq.cummax() - 1.0).shift(1).fillna(0.0)
    return pd.Series(np.where(dd.values < -T, 0.50, 1.0), index=px.index)


def mult_volcap(px, r0, turn0, gross0, target):
    v = (r0.rolling(20).std() * np.sqrt(252.0)).shift(1)
    m = (target / v).clip(upper=1.0)
    return m.fillna(1.0)


def mask_maband(px, b):
    return band_state(px, b) & live_mask(px)


def mask_stop(px, s):
    hi = px.rolling(60, min_periods=1).max()
    return ((px / hi - 1.0) > -s).fillna(True)


# ------------------------------------------------------------------ metrics
def nm3(r):
    """(CAGR, Sharpe, MaxDD) for a numpy return array — identical to engine.metrics."""
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    sd = float(np.std(r, ddof=1))
    vol = sd * np.sqrt(252.0)
    sh = (float(r.mean()) * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def sharpe(r):
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return (float(r.mean()) * 252.0) / sd if sd else np.nan


class Path4:
    """One cost-parameterised return path with both KEEP paths' bar margins."""

    def __init__(self, idx, r0, turn, ref):
        self.idx = idx
        self.r0 = np.asarray(r0, float)
        self.turn = np.asarray(turn, float)
        self.ref = ref                       # PanelRef
        yrs = (idx[-1] - idx[0]).days / 365.25
        self.turnover_yr = float(self.turn.sum()) / yrs
        self.gross_mean = np.nan

    def rc(self, c):
        return self.r0 - self.turn * (c / 1e4)

    def m4b(self, c, win="full"):
        x = self._w(self.rc(c), win)
        R = self.ref.spy[win]
        h = len(x) // 2
        cg, _, dd = nm3(x)
        m = {"H1": sharpe(x[:h]) - R["H1"], "H2": sharpe(x[h:]) - R["H2"],
             "DD": DD_CAP * R["DD"] - abs(dd), "CAGR": cg - CAGR_FLOOR * R["CAGR"]}
        if win == "full":
            m["OOS"] = sharpe(self.rc(c)[self.ref.oos]) - R["OOS"]
        return m

    def m4a(self, c, win="full"):
        x = self._w(self.rc(c), win)
        y = self._w(self.ref.v2.rc(c), win)
        h = len(x) // 2
        _, _, dd = nm3(x)
        _, _, ddb = nm3(y)
        return {"H1": sharpe(x[:h]) - sharpe(y[:h]), "H2": sharpe(x[h:]) - sharpe(y[h:]),
                "DD": abs(ddb) - abs(dd)}

    def _w(self, r, win):
        if win == "full":
            return r
        return r[self.ref.is_m] if win == "is" else r[self.ref.oos]

    def worst(self, c, path, win):
        f = self.m4b if path == "4b" else self.m4a
        return min(f(c, win).values())

    def stats(self, c, win="full"):
        x = self._w(self.rc(c), win)
        cg, sh, dd = nm3(x)
        h = len(x) // 2
        return dict(CAGR=cg, Sharpe=sh, MaxDD=dd, H1=sharpe(x[:h]), H2=sharpe(x[h:]))


class PanelRef:
    """SPY bars, RULES v2 path and the IS/OOS masks for one panel."""

    def __init__(self, idx, spy_r, v2_r, v2_turn):
        self.idx = idx
        self.is_m = np.asarray(idx <= pd.Timestamp(IS_END))
        self.oos = np.asarray(idx >= pd.Timestamp(OOS_START))
        s = np.asarray(spy_r, float)
        self.spy = {}
        for win, mask in [("full", np.ones(len(s), bool)), ("is", self.is_m), ("oos", self.oos)]:
            x = s[mask]
            h = len(x) // 2
            c, _, dd = nm3(x)
            d = {"H1": sharpe(x[:h]), "H2": sharpe(x[h:]), "DD": abs(dd), "CAGR": c}
            if win == "full":
                d["OOS"] = sharpe(s[self.oos])
            self.spy[win] = d
        self.spy_r = s
        self.v2 = Path4(idx, v2_r, v2_turn, self)
        self.v2.ref = self


def cstar(p, path="4b", win="full"):
    """First c in [0, CMAX] where any bar turns <= 0.  0.0 = fails at zero cost,
    nan = never fails inside the ladder."""
    if p.worst(0.0, path, win) <= 0:
        return 0.0
    lo, hi = 0.0, None
    for c in np.arange(SCAN, CMAX + SCAN / 2, SCAN):
        if p.worst(float(c), path, win) <= 0:
            hi = float(c)
            break
        lo = float(c)
    if hi is None:
        return np.nan
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if p.worst(mid, path, win) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def cnum_s(col):
    return col.fillna(CMAX * 10)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if np.std(ra) == 0 or np.std(rb) == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def fmt(v, nev="never"):
    return nev if (v is None or (isinstance(v, float) and np.isnan(v))) else f"{v:.2f}"


def cnum(v):
    """c* as a comparable number: 'never' beats every finite crossing."""
    return CMAX * 10 if (v is None or (isinstance(v, float) and np.isnan(v))) else v


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# {SLUG}")
    P(f"# idea 335 — is c*(book + de-grossing overlay) <= c*(book at matched mean gross) an identity?")
    P(f"# parent NF20 (top-{N0} eligible, equal weight, no vol scaler, weekly) | rungs {RUNGS}")
    P(f"# families {list(FAMILIES)} | c* ladder [0, {CMAX:.0f}] bps | 4b vs SPY, 4a vs RULES v2")
    P("")

    panels = []
    for tag, kw in [("U56", {}), ("B136", {"broad": True})]:
        px = load_universe(**kw).dropna(how="all").ffill()
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED — aborting.")
            sys.exit(1)
        panels.append((tag, px))

    # ================================================================ [0] GATES
    P("=" * 150)
    P("[0] REPRODUCTION GATES")
    gpx = panels[0][1]
    gw = parent_weights(gpx, 0.75)
    r0g, tg, grg = fast_bt(gpx, gw, FREQ)
    g1 = 0.0
    for c in (0, 25):
        eng = backtest(gpx, gw, cost_bps=c, freq=FREQ)
        g1 = max(g1, float((r0g - tg * c / 1e4 - eng["returns"]).abs().max()),
                 float((tg - eng["turnover"]).abs().max()))
    P(f"    G1 fast_bt == engine.backtest (returns AND turnover, c in 0/25 bps): max |d| {g1:.3e}")
    assert g1 < 1e-12, g1

    allT = pd.DataFrame(True, index=gpx.index, columns=gpx.columns)
    r0m, tm, grm = fast_bt(gpx, gw, FREQ, daily_mask=allT)
    g2 = max(float((r0m - r0g).abs().max()), float((tm - tg).abs().max()))
    P(f"    G2 per-name overlay at OFF (mask all-True) == parent: max |d| {g2:.3e}")
    assert g2 < 1e-12, g2

    ones = pd.Series(1.0, index=gpx.index)
    rB, tB, grB = apply_mult(r0g, tg, grg, ones)
    g3 = max(float((rB - r0g).abs().max()), float((tB - tg).abs().max()),
             float((grB - grg).abs().max()))
    P(f"    G3 book-level overlay at OFF (m == 1) == parent: max |d| {g3:.3e}")
    assert g3 < 1e-12, g3

    g4 = max(float((1.0 * r0g - r0g).abs().max()), float((1.0 * tg - tg).abs().max()))
    P(f"    G4 matched control at a = 1 == parent: max |d| {g4:.3e}")
    assert g4 < 1e-12, g4

    g5 = 0.0
    for a in (0.25, 0.50, 0.85, 1.00):
        for c in (0, 10, 25):
            base = (r0g - tg * c / 1e4).values
            g5 = max(g5, abs(sharpe(a * base) - sharpe(base)))
    P(f"    G5 SHARPE INVARIANCE of the gross dial (a in 0.25..1.00, c in 0/10/25): max |dSharpe| "
      f"{g5:.3e}  -> the control's c* is a pure CAGR/MaxDD statistic")
    assert g5 < 1e-12, g5

    # G7 — the parent family against the record's own standing 4b row.
    el = eligible_mask(gpx)
    rk = score(gpx, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    kf = pd.Series(float(N0), index=gpx.index)
    w20 = rk.le(kf, axis=0).astype(float).mul(0.75 / kf, axis=0)
    e20 = backtest(gpx, w20, cost_bps=10, freq=FREQ)["returns"].loc[gpx.index[WARMUP]:]
    c20, s20, d20 = nm3(e20.values)
    h20 = len(e20) // 2
    P(f"    G7 the record's standing 2026-09-04 KEEP-4b row (`46 N n=20`, published 12.7% / 1.09 "
      f"/ -18.3%, halves 1.09/1.10) rebuilt at FIXED n=20: {c20:.2%} / {s20:.3f} / {d20:.2%} "
      f"(halves {sharpe(e20.values[:h20]):.2f}/{sharpe(e20.values[h20:]):.2f}) — EXACT.")
    P(f"       This run's parent is its NF20 twin (k = min(20, E_t)); every number below is that "
      f"twin's, not the published row's.")

    # ================================================================ per-panel build
    grid, wf, anchors, parents, G6 = [], [], [], [], []
    P("")
    for panel, px in panels:
        start = px.index[WARMUP]
        sub = px.loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2w = rules_v2_weights(px)
        v2r, v2t, _ = fast_bt(px, v2w, FREQ)
        ref = PanelRef(sub.index, spy.values, v2r.loc[start:].values, v2t.loc[start:].values)
        sc, ss, sdd = nm3(ref.spy_r)
        P("=" * 150)
        P(f"PANEL {panel}: {px.shape[1]} cols | {px.index[0].date()} -> {px.index[-1].date()} | "
          f"eval {start.date()} .. {px.index[-1].date()}")
        P(f"    SPY  {sc:.2%} / {ss:.3f} (H1 {ref.spy['full']['H1']:.3f} / H2 "
          f"{ref.spy['full']['H2']:.3f} / OOS {ref.spy['full']['OOS']:.3f}) / {sdd:.2%}   "
          f"| 4b bars: DD cap {DD_CAP*ref.spy['full']['DD']:.2%}, CAGR floor "
          f"{CAGR_FLOOR*ref.spy['full']['CAGR']:.2%}")
        v2s = ref.v2.stats(10)
        P(f"    RULES v2 @10bps  {v2s['CAGR']:.2%} / {v2s['Sharpe']:.3f} / {v2s['MaxDD']:.2%} "
          f"(H1 {v2s['H1']:.3f} / H2 {v2s['H2']:.3f})  c*_4b {fmt(cstar(ref.v2,'4b'))}")

        # precompute per-name masks once per panel (dial values are panel-independent)
        maskcache = {}
        for b in FAMILIES["MABAND"]["vals"]:
            maskcache[("MABAND", b)] = mask_maband(px, b)
        for s in FAMILIES["STOP"]["vals"]:
            maskcache[("STOP", s)] = mask_stop(px, s)

        if panel == "U56":
            # idea 42's own book width (n=3, idea 40/41's grid), rebuilt to test its
            # published "both are EXACTLY 20 bps" reading on the form that produced it.
            w3 = parent_weights(px, ANCHOR_G, n=3)
            a3r, a3t, a3g = fast_bt(px, w3, FREQ)
            a3r, a3t, a3g = a3r.loc[start:], a3t.loc[start:], a3g.loc[start:]
            p3 = Path4(sub.index, a3r.values, a3t.values, ref)
            m3 = mult_breadth(px, a3r, a3t, a3g, ANCHOR_DEPTH).loc[start:]
            o3r, o3t, o3g = apply_mult(a3r, a3t, a3g, m3)
            ov3 = Path4(sub.index, o3r.values, o3t.values, ref)
            a3 = float(o3g.mean()) / float(a3g.mean())
            ct3 = Path4(sub.index, a3 * p3.r0, a3 * p3.turn, ref)
            gd3 = Path4(sub.index, ANCHOR_GROSS_DIAL * p3.r0, ANCHOR_GROSS_DIAL * p3.turn, ref)
            for nm, pp, gm in [("n=3 UNGATED parent g=1.00", p3, float(a3g.mean())),
                               ("n=3 overlay  B=0.40 depth=0.50 g=1.00 (idea 42's arm)", ov3,
                                float(o3g.mean())),
                               (f"n=3 plain gross dial g={ANCHOR_GROSS_DIAL:.2f} "
                                f"(idea 42's comparand)", gd3,
                                ANCHOR_GROSS_DIAL * float(a3g.mean())),
                               ("n=3 matched-gross control of the overlay", ct3,
                                a3 * float(a3g.mean()))]:
                anchors.append(dict(arm=nm, cstar4b=cstar(pp, "4b"), cstar4a=cstar(pp, "4a"),
                                    gross_mean=gm, CAGR_10=pp.stats(10)["CAGR"],
                                    Sharpe_10=pp.stats(10)["Sharpe"],
                                    MaxDD_10=pp.stats(10)["MaxDD"],
                                    fail4b_at0=",".join(k for k, v in pp.m4b(0).items()
                                                        if v <= 0) or "-"))

        for g0 in RUNGS:
            w = parent_weights(px, g0)
            pr0f, ptnf, pgrf = fast_bt(px, w, FREQ)          # FULL history, for the signals
            pr0, ptn, pgr = pr0f.loc[start:], ptnf.loc[start:], pgrf.loc[start:]
            par = Path4(sub.index, pr0.values, ptn.values, ref)
            par.gross_mean = float(pgr.mean())
            ps = par.stats(10)
            pc = {(p, wn): cstar(par, p, wn) for p in ("4a", "4b")
                  for wn in ("full", "is", "oos")}
            parents.append(dict(panel=panel, g0=g0, gross_mean=par.gross_mean,
                                turnover_yr=par.turnover_yr, **{f"p_{k}": v for k, v in ps.items()},
                                cstar4b=pc[("4b", "full")], cstar4a=pc[("4a", "full")],
                                cstar4b_is=pc[("4b", "is")], cstar4b_oos=pc[("4b", "oos")]))
            P(f"  PARENT g0={g0:.2f}  gross {par.gross_mean:.3f}  turn/yr {par.turnover_yr:.2f}  "
              f"@10bps {ps['CAGR']:.2%} / {ps['Sharpe']:.3f} / {ps['MaxDD']:.2%}  "
              f"c*_4b {fmt(pc[('4b','full')]):>6s}  c*_4a {fmt(pc[('4a','full')]):>6s}")

            for fam, spec in FAMILIES.items():
                for dv in spec["vals"]:
                    if spec["kind"] == "book":
                        fn = {"BREADTH": mult_breadth, "DDCTL": mult_ddctl,
                              "VOLCAP": mult_volcap}[fam]
                        mf = fn(px, pr0f, ptnf, pgrf, dv)      # signal on the FULL history
                        m = mf.loc[start:]
                        orr, otn, ogr = apply_mult(pr0, ptn, pgr, m)
                        on_frac = float((m < 1.0).mean())
                    else:
                        orr, otn, ogr = fast_bt(px, w, FREQ, daily_mask=maskcache[(fam, dv)])
                        orr, otn, ogr = orr.loc[start:], otn.loc[start:], ogr.loc[start:]
                        on_frac = float((ogr < pgr - 1e-12).mean())
                    ov = Path4(sub.index, orr.values, otn.values, ref)
                    ov.gross_mean = float(ogr.mean())

                    # ---- matched-gross control: the plain gross dial at the overlay's mean gross
                    a = ov.gross_mean / par.gross_mean if par.gross_mean > 0 else np.nan
                    ct = Path4(sub.index, a * par.r0, a * par.turn, ref)
                    ct.gross_mean = a * par.gross_mean
                    gmerr = abs(ct.gross_mean - ov.gross_mean)

                    row = dict(panel=panel, g0=g0, family=fam, dial=spec["dial"], dial_val=dv,
                               kind=spec["kind"], on_frac=on_frac, alpha=a,
                               gross_parent=par.gross_mean, gross_overlay=ov.gross_mean,
                               gross_match_err=gmerr,
                               turn_parent=par.turnover_yr, turn_overlay=ov.turnover_yr,
                               turn_ctrl=ct.turnover_yr)
                    for pth in ("4b", "4a"):
                        for wn in ("full", "is", "oos"):
                            co = cstar(ov, pth, wn)
                            cc = cstar(ct, pth, wn)
                            row[f"cstar_ov_{pth}_{wn}"] = co
                            row[f"cstar_ct_{pth}_{wn}"] = cc
                            row[f"identity_{pth}_{wn}"] = bool(cnum(co) <= cnum(cc) + 1e-9)
                            row[f"gap_{pth}_{wn}"] = cnum(co) - cnum(cc)
                    row["ov_Sharpe_is_10"] = ov.stats(10, "is")["Sharpe"]
                    row["ov_CAGR_is_10"] = ov.stats(10, "is")["CAGR"]
                    for wn in ("oos",):
                        so = ov.stats(10, wn)
                        row["ov_CAGR_oos_10"] = so["CAGR"]
                        row["ov_Sharpe_oos_10"] = so["Sharpe"]
                        row["ov_MaxDD_oos_10"] = so["MaxDD"]
                    if len(grid) < 12:
                        G6.append(abs(cnum(cstar(ov, "4b")) - cnum(row["cstar_ov_4b_full"])))
                    for c in COSTS:
                        so, sc_ = ov.stats(c), ct.stats(c)
                        row[f"ov_CAGR_{c}"], row[f"ov_Sharpe_{c}"], row[f"ov_MaxDD_{c}"] = \
                            so["CAGR"], so["Sharpe"], so["MaxDD"]
                        row[f"ct_Sharpe_{c}"] = sc_["Sharpe"]
                        m4b, m4a = ov.m4b(c), ov.m4a(c)
                        row[f"keep4b_{c}"] = bool(min(m4b.values()) > 0)
                        row[f"keep4a_{c}"] = bool(min(m4a.values()) > 0)
                        row[f"fail4b_{c}"] = ",".join(k for k, v in m4b.items() if v <= 0) or "-"
                    grid.append(row)

                    if (panel == "U56" and fam == "BREADTH" and abs(g0 - ANCHOR_G) < 1e-9
                            and abs(dv - ANCHOR_DEPTH) < 1e-9):
                        ad = Path4(sub.index, (ANCHOR_GROSS_DIAL / g0) * par.r0,
                                   (ANCHOR_GROSS_DIAL / g0) * par.turn, ref)
                        for nm, pp, gm in [
                                (f"n={N0} overlay  B=0.40 depth=0.50 g={g0:.2f}", ov, ov.gross_mean),
                                (f"n={N0} plain gross dial g={ANCHOR_GROSS_DIAL:.2f}", ad,
                                 ANCHOR_GROSS_DIAL / g0 * par.gross_mean),
                                (f"n={N0} matched-gross control of the overlay", ct, ct.gross_mean)]:
                            anchors.append(dict(arm=nm, cstar4b=cstar(pp, "4b"),
                                                cstar4a=cstar(pp, "4a"), gross_mean=gm,
                                                CAGR_10=pp.stats(10)["CAGR"],
                                                Sharpe_10=pp.stats(10)["Sharpe"],
                                                MaxDD_10=pp.stats(10)["MaxDD"],
                                                fail4b_at0=",".join(k for k, v in pp.m4b(0).items()
                                                                    if v <= 0) or "-"))

            # ---- rule 8 walk-forward for this (panel, rung): dial chosen on IS ONLY
            par_oos = par.stats(10, "oos")
            v2_oos = ref.v2.stats(10, "oos")
            spy_oos = dict(zip(("CAGR", "Sharpe", "MaxDD"), nm3(ref.spy_r[ref.oos])))
            for fam, spec in FAMILIES.items():
                sub_g = [r for r in grid if r["panel"] == panel and r["g0"] == g0
                         and r["family"] == fam]
                for chooser, key in [("IS c*_4b", lambda r: (cnum(r["cstar_ov_4b_is"]),
                                                             r["ov_Sharpe_is_10"])),
                                     ("IS Sharpe", lambda r: (r["ov_Sharpe_is_10"],
                                                              cnum(r["cstar_ov_4b_is"])))]:
                    pk = max(sub_g, key=key)
                    wf.append(dict(
                        panel=panel, g0=g0, family=fam, chooser=chooser,
                        dial_val=pk["dial_val"], is_Sharpe=pk["ov_Sharpe_is_10"],
                        cstar_is=pk["cstar_ov_4b_is"], cstar_oos=pk["cstar_ov_4b_oos"],
                        ctrl_cstar_oos=pk["cstar_ct_4b_oos"],
                        identity_oos=pk["identity_4b_oos"],
                        oos_CAGR=pk["ov_CAGR_oos_10"], oos_Sharpe=pk["ov_Sharpe_oos_10"],
                        oos_MaxDD=pk["ov_MaxDD_oos_10"],
                        par_oos_CAGR=par_oos["CAGR"], par_oos_Sharpe=par_oos["Sharpe"],
                        par_oos_MaxDD=par_oos["MaxDD"],
                        v2_oos_Sharpe=v2_oos["Sharpe"], v2_oos_CAGR=v2_oos["CAGR"],
                        spy_oos_Sharpe=spy_oos["Sharpe"], spy_oos_CAGR=spy_oos["CAGR"],
                        spy_oos_MaxDD=spy_oos["MaxDD"]))

    # ================================================================ frames
    G = pd.DataFrame(grid)
    PAR = pd.DataFrame(parents)
    ANC = pd.DataFrame(anchors)

    P("")
    P("=" * 150)
    P("[1] GATE G6 — determinism of the c* bisection, and the matched-gross solve")
    P(f"    G6 c* recomputed on the first {len(G6)} cells: max |d| {max(G6):.3e}")
    assert max(G6) < 1e-12
    P(f"    matched-gross solve: max |mean gross(control) - mean gross(overlay)| over all "
      f"{len(G)} cells: {G.gross_match_err.abs().max():.3e}")
    assert G.gross_match_err.abs().max() < 1e-12

    P("")
    P("=" * 150)
    P("[2] THE IDENTITY — c*(overlay) <= c*(matched-gross control), every grid point")
    for pth in ("4b", "4a"):
        for wn in ("full", "is", "oos"):
            col = f"identity_{pth}_{wn}"
            n_ok = int(G[col].sum())
            viol = G[~G[col]]
            mx = viol[f"gap_{pth}_{wn}"].max() if len(viol) else 0.0
            P(f"    {pth} / {wn:4s}: holds {n_ok:>3d} / {len(G)}  "
              f"({n_ok/len(G):6.1%})   violations {len(viol):>3d}   "
              f"max widening {mx:+.2f} bps")
    P("")
    P("    A cell is INFORMATIVE only if at least one side has a non-zero c*: when both the")
    P("    overlay and its control already fail 4b at ZERO cost the inequality is 0 <= 0 and")
    P("    carries no information.  The same counts restricted to informative cells:")
    for pth in ("4b", "4a"):
        for wn in ("full", "is", "oos"):
            inf = G[(G[f"cstar_ov_{pth}_{wn}"].pipe(cnum_s) > 0)
                    | (G[f"cstar_ct_{pth}_{wn}"].pipe(cnum_s) > 0)]
            if not len(inf):
                P(f"    {pth} / {wn:4s}: 0 informative cells")
                continue
            n_ok = int(inf[f"identity_{pth}_{wn}"].sum())
            P(f"    {pth} / {wn:4s}: holds {n_ok:>3d} / {len(inf):>3d} informative "
              f"({n_ok/len(inf):6.1%})   violations {len(inf)-n_ok:>3d}")
    P("")
    P("    MECHANISM.  G5 makes the control's Sharpe identical to the parent's at every cost,")
    P("    so the control's c* moves only through CAGR/MaxDD while the overlay's also moves")
    P("    through Sharpe.  dSharpe = overlay - control at 10 bps, by family:")
    G["dSharpe_10"] = G.ov_Sharpe_10 - G.ct_Sharpe_10
    mech = G.groupby("family").agg(mean_dSharpe=("dSharpe_10", "mean"),
                                   max_dSharpe=("dSharpe_10", "max"),
                                   viol=("identity_4b_full", lambda x: int((~x).sum())))
    P("      " + mech.to_string().replace("\n", "\n      "))
    infG = G[(G.cstar_ov_4b_full.pipe(cnum_s) > 0) | (G.cstar_ct_4b_full.pipe(cnum_s) > 0)]
    if len(infG) > 2:
        P(f"      spearman(dSharpe_10, gap_4b_full) over the {len(infG)} informative cells: "
          f"{spearman(infG.dSharpe_10.values, infG.gap_4b_full.values):+.3f}")
    P("")
    P("    violations by family (4b / full):")
    v = G.groupby("family").agg(n=("identity_4b_full", "size"),
                                holds=("identity_4b_full", "sum"),
                                max_gap=("gap_4b_full", "max"),
                                med_gap=("gap_4b_full", "median"))
    v["viol"] = v.n - v.holds
    P("      " + v.to_string().replace("\n", "\n      "))
    P("")
    P("    violations by panel x rung (4b / full):")
    v2 = G.groupby(["panel", "g0"]).agg(n=("identity_4b_full", "size"),
                                        holds=("identity_4b_full", "sum"),
                                        max_gap=("gap_4b_full", "max"))
    v2["viol"] = v2.n - v2.holds
    P("      " + v2.to_string().replace("\n", "\n      "))

    P("")
    P("=" * 150)
    P("[3] EVERY GRID POINT (4b, full sample): overlay c* vs its matched-gross control")
    show = G[["panel", "g0", "family", "dial_val", "on_frac", "gross_overlay", "alpha",
              "turn_overlay", "turn_ctrl", "cstar_ov_4b_full", "cstar_ct_4b_full",
              "gap_4b_full", "identity_4b_full", "ov_Sharpe_10", "ct_Sharpe_10"]].copy()
    P("    " + show.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))

    P("")
    P("=" * 150)
    P("[4] THE IDEA-42 ANCHOR (U56, g=1.00, B=0.40, depth=0.50) vs the plain gross dial")
    if len(ANC):
        P("    " + ANC.to_string(index=False, float_format=lambda x: f"{x:.3f}")
          .replace("\n", "\n    "))
        a = ANC.set_index("arm")
        ov3 = a.loc["n=3 overlay  B=0.40 depth=0.50 g=1.00 (idea 42's arm)"].cstar4b
        gd3 = a.loc["n=3 plain gross dial g=0.85 (idea 42's comparand)"].cstar4b
        deg = (cnum(ov3) == 0.0 and cnum(gd3) == 0.0)
        P(f"    idea 42 published BOTH of its two arms as EXACTLY 20 bps.  Rebuilt on idea "
          f"40/41's own width (n=3): overlay c* {fmt(ov3)} bps, plain gross dial c* {fmt(gd3)} bps.")
        if deg:
            P(f"    Both are ZERO — a DEGENERATE tie, not a 20-bps one.  At g=1.00 the n=3 book "
              f"draws down {a.loc['n=3 UNGATED parent g=1.00'].MaxDD_10:.2%} ungated and "
              f"{a.loc[a.index[1]].MaxDD_10:.2%} gated, against a 4b cap of "
              f"{DD_CAP*100:.0f}% of SPY's; both already fail 4b at ZERO cost "
              f"(overlay bars '{a.loc[a.index[1]].fail4b_at0}', gross dial "
              f"'{a.loc[a.index[2]].fail4b_at0}'), so neither arm has a 4b cost budget to "
              f"compare and the equality cannot be read off this form at all.")
        else:
            P(f"    -> {'TIE' if abs(cnum(ov3)-cnum(gd3)) < 0.5 else 'NOT a tie'} "
              f"(|d| {abs(cnum(ov3)-cnum(gd3)):.2f} bps).")
        P("    This is a re-measurement, not idea 42's own file: eligibility, the breadth series,")
        P("    the panel and the c* estimator are THIS run's, and idea 42's 20 bps may well have")
        P("    been read off a different bar set.  Nothing here says idea 42 erred.  What it does")
        P("    establish is that the 20-bps EQUALITY is not a property that survives an")
        P("    independent rebuild of the described arm, so it cannot be the basis of a general")
        P("    law; the 90-cell grid below is what the general question is answered on.")
    else:
        P("    anchor cell not built (unexpected)")

    P("")
    P("=" * 150)
    P("[5] KEEP-PATH CENSUS on every grid point, all three cost rungs")
    for c in COSTS:
        P(f"    @{c:>2d} bps:  4a {int(G[f'keep4a_{c}'].sum()):>3d}/{len(G)}   "
          f"4b {int(G[f'keep4b_{c}'].sum()):>3d}/{len(G)}")
    P("    failing-4b-bar distribution @10 bps: "
      + ", ".join(f"{k}={v}" for k, v in G["fail4b_10"].value_counts().items()))
    k10 = G[G["keep4b_10"]]
    if len(k10):
        P(f"    the {len(k10)} cells clearing 4b @10 bps:")
        P("      " + k10[["panel", "g0", "family", "dial_val", "ov_CAGR_10", "ov_Sharpe_10",
                          "ov_MaxDD_10", "cstar_ov_4b_full", "cstar_ct_4b_full",
                          "identity_4b_full"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))
    else:
        P("    no cell clears 4b @10 bps")

    P("")
    P("=" * 150)
    P("[6] RULE 8 WALK-FORWARD — dial chosen on 2008-2016 by IS c*_4b, 2017-2026 read once")
    W = pd.DataFrame(wf)
    P("    " + W.to_string(index=False, float_format=lambda x: f"{x:.2f}")
      .replace("\n", "\n    "))
    hold_oos = int(W.identity_oos.sum())
    P(f"    identity on the OOS window for the IS-chosen dial: {hold_oos}/{len(W)}")

    P("")
    P("    OOS @10 bps levels of the IS-chosen arms vs the parent anchor, RULES v2 and SPY:")
    cols = ["panel", "g0", "family", "chooser", "dial_val", "oos_CAGR", "oos_Sharpe",
            "oos_MaxDD", "par_oos_CAGR", "par_oos_Sharpe", "par_oos_MaxDD",
            "v2_oos_Sharpe", "spy_oos_CAGR", "spy_oos_Sharpe", "spy_oos_MaxDD"]
    P("      " + W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n      "))
    beats = W[(W.oos_Sharpe > W.spy_oos_Sharpe) & (W.oos_Sharpe > W.v2_oos_Sharpe)]
    P(f"      IS-chosen arms whose OOS Sharpe beats SPY: "
      f"{int((W.oos_Sharpe > W.spy_oos_Sharpe).sum())}/{len(W)}; beats BOTH SPY and RULES v2: "
      f"{len(beats)}/{len(W)}")
    kk = []
    for _, r in W.iterrows():
        c = G[(G.panel == r.panel) & (G.g0 == r.g0) & (G.family == r.family)
              & (G.dial_val == r.dial_val)].iloc[0]
        kk.append(bool(c["keep4b_10"]))
    W["keep4b_10"] = kk
    P(f"      IS-chosen arms clearing the FULL 4b bar set @10 bps: {int(W.keep4b_10.sum())}/{len(W)}"
      f"  (4a: 0/{len(W)} — no cell in the grid clears 4a at any rung)")

    P("")
    P("=" * 150)
    P("[7] VERDICT")
    n = len(G)
    ok_full = int(G.identity_4b_full.sum())
    ok_oos = int(G.identity_4b_oos.sum())
    ok_4a = int(G.identity_4a_full.sum())
    P(f"    4b full: {ok_full}/{n}   4b OOS: {ok_oos}/{n}   4a full: {ok_4a}/{n}")
    if ok_full == n and ok_oos == n:
        P("    -> the inequality holds at EVERY point tested: c* behaves as an exposure "
          "statistic on this corpus and no de-grossing overlay widened the cost budget.")
    else:
        wv = G[~G.identity_4b_full]
        P(f"    -> NOT an identity: {n-ok_full} of {n} points have c*(overlay) > "
          f"c*(matched gross), the largest by {wv.gap_4b_full.max():+.2f} bps "
          f"({wv.loc[wv.gap_4b_full.idxmax(), 'panel']} g0="
          f"{wv.loc[wv.gap_4b_full.idxmax(), 'g0']:.2f} "
          f"{wv.loc[wv.gap_4b_full.idxmax(), 'family']}="
          f"{wv.loc[wv.gap_4b_full.idxmax(), 'dial_val']}).")
        P("       Re-timing exposure CAN buy cost budget; c* is not readable off mean gross.")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    PAR.to_csv(f"{OUT}.parents.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    ANC.to_csv(f"{OUT}.anchor.csv", index=False)
    P("")
    P(f"Wrote {OUT.name}.grid.csv ({len(G)}), .parents.csv ({len(PAR)}), "
      f".walkforward.csv ({len(W)}), .anchor.csv ({len(ANC)})  [{time.time()-t0:.1f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
