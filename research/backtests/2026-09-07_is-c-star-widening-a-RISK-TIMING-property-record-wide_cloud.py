#!/usr/bin/env python3
"""Idea 394 — "is-c-star-widening-a-RISK-TIMING-property-record-wide" (cloud, 2026-09-07).

QUESTION (QUEUE.md).  Idea 335 killed the proposed identity c*(book + de-grossing overlay)
<= c*(book at matched mean gross): 10 of 90 cells widened the book's cost breakeven, and the
widening cells were VOLCAP (5 of 11 informative) and DDCTL (2 of 8) — both timed on the
BOOK'S OWN REALISED RISK — while the panel-state gate (BREADTH) widened 0 of 6.  Spearman
(dSharpe, c* gap) was only +0.336, so "it widens because it lifts Sharpe" is a weak
explanation.  Does "widens c*" partition cleanly by WHAT THE OVERLAY IS TIMED ON?  Re-run the
same matched-gross control against a THIRD class — overlays timed on a variable that is
neither the book's risk nor the panel's state — on 2 panels x 3 gross rungs.

WHY IT MATTERS.  If only risk-timed overlays can widen c*, then "this overlay pays for its
own turnover" is a claim that can only be made for risk timing, and every calendar / budget
/ housekeeping overlay in the record can have its cost budget read straight off its mean
gross.  That is a screening rule worth having.  If EXOGENOUS overlays widen c* too, the
partition is not about timing at all and idea 335's family split was small-sample noise.

DESIGN — one convention, three timing classes, nothing else varied.

  PARENT (fixed, idea 40/41's book, never tuned, identical to idea 335): eligible = above the
  200d MA and vol20 < 0.60; rank eligible names by the v1 composite WITHOUT the /sqrt(vol20)
  term; hold the top k = min(20, E_t) equal-weight at w = g0/k; weekly; next-day execution.

  RUNGS (tuned parameter 1): g0 in {0.50, 0.75, 1.00}.  No leverage (PROTOCOL rule 2).

  EVERY overlay here is BOOK-LEVEL and uses idea 41's published convention verbatim:
      r = m*r0 ;  turn = m*turn0 + |dm| * gross0.shift(1) ;  gross = m*gross0
  with m lagged (decided at t-1, executed at t).  Idea 335's two PER-NAME families (MABAND,
  STOP) are deliberately EXCLUDED: they change the convention as well as the timing variable,
  and this run is a controlled comparison in which the ONLY thing that differs between arms
  is what the multiplier is timed on.  Idea 335's per-name numbers stand unchanged.

  CLASS R — timed on the BOOK'S OWN REALISED RISK  (idea 335's widening families)
    VOLCAP    m = min(1, target / lagged 20d annualised parent vol).  target in
              {0.10, 0.15, 0.25}.
    DDCTL     m = 0.50 while the parent's own lagged zero-cost drawdown is worse than -T.
              T in {0.05, 0.10, 0.20}.

  CLASS P — timed on the PANEL'S STATE  (idea 335's non-widening family, plus one)
    BREADTH   m = depth while panel breadth (share of constituents above their own 200d MA,
              lagged 1 day) < B = 0.40 (idea 42's pinned B).  depth in {0.75, 0.50, 0.25}.
    NAMEFLOOR m = min(1, E_{t-1} / F), E = the parent's own eligible-name count.
              F in {10, 20, 30}.

    RECLASSIFICATION, PRE-REGISTERED.  QUEUE.md lists "name-count floor" as an example of the
    THIRD class.  It is not one: E_t is the panel's breadth times its width, so NAMEFLOOR is
    a monotone transform of the same panel-state variable BREADTH is timed on.  It is filed
    under P, and [1] G10 reports corr(E_t, panel breadth) to justify that; [2] additionally
    reports the whole partition test with NAMEFLOOR moved into class X, so the reader can see
    the answer under the queue's own classification too.

  CLASS X — timed on NEITHER (the new third class)
    CALCAD    m = depth in the May-October calendar window, 1.00 otherwise.  Timed on the
              DATE alone.  depth in {0.75, 0.50, 0.25}.  The window is folklore ("sell in
              May"), fixed ex ante; only depth is dialled.
    TURNBUD   m = 0.50 while the parent's lagged trailing 63d turnover exceeds its own
              EXPANDING q-quantile (min 252 obs, so strictly past data).  q in
              {0.50, 0.75, 0.90}.  Timed on the book's TRADING ACTIVITY — not its risk,
              not the panel.
    RANDOM    m = 0.50 on weeks drawn by a fixed-seed Bernoulli(p), 1.00 otherwise; the draw
              is keyed on the ISO week so both panels see the SAME schedule.  p in
              {0.10, 0.25, 0.50}.  Timed on NOTHING — the negative control that says what a
              c* gap looks like when the overlay carries no information at all.

  MATCHED CONTROL (idea 335's, verbatim).  For every overlay cell, a = mean(gross_overlay_t)
  / mean(gross_parent_t) applied as a CONSTANT multiplier to the same parent.  Closed form,
  no search, a <= 1 because every family de-grosses.  This is the plain gross dial held at
  the overlay's own realised mean exposure.

  c* ESTIMATOR (idea 335's, verbatim).  First cost c in [0, 50] bps at which any bar of the
  path turns non-positive; 0.0 if the path fails at zero cost; "never" if it survives the
  ladder.  0.25-bps bracket then 60 bisections.  Computed for BOTH KEEP paths on three
  windows (full / IS 2008-2016 / OOS 2017-2026):
    4b  vs SPY: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%.
    4a  vs the LIVE RULES v2 book at the SAME cost rung: Sharpe > v2 in both halves and
        MaxDD no worse than v2's.
  A cell counts as INFORMATIVE only if at least one side has a non-zero c* (idea 393's fix):
  when both already fail at zero cost the inequality is 0 <= 0 and says nothing.

  RULE 8 WALK-FORWARD.  For every (panel, rung, family) the dial is chosen on 2008-2016 ONLY
  — by IS c*_4b and, separately, by IS Sharpe at 10 bps — and 2017-2026 is read once.  OOS
  CAGR / Sharpe / MaxDD against the parent anchor, RULES v2 (the live baseline) and SPY, and
  the partition test is re-run on the OOS window alone.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): (1) the parent's gross rung, (2) the overlay's
dial.  Panel, overlay family, timing class and cost rung are CENSUS axes — every level is
reported and nothing is selected on outcome.  All 126 grid points go to .grid.csv.

GATES (asserted / printed in [0] before any new number is read).
  G1  fast_bt == engine.backtest on returns AND turnover at 0 and 25 bps.
  G3  every overlay at its OFF setting (m == 1) == the parent, exactly.
  G4  the matched control at a = 1 == the parent, exactly.
  G5  SHARPE INVARIANCE of the gross dial (this is what makes the control's c* a pure
      CAGR/MaxDD statistic) — measured, not assumed.
  G6  c* reproduces its own value on a re-run (determinism of the bisection).
  G8  every cell's overlay is non-vacuous: on_frac > 0 and a < 1.
  G9  RANDOM's schedule is reproducible and panel-independent on shared weeks.
  G10 corr(NAMEFLOOR's E_t, panel breadth) — the reclassification evidence.
  G11 idea 335's five overlapping cells (U56/B136 x BREADTH/DDCTL/VOLCAP at the shared rungs)
      reproduce idea 335's committed .grid.csv c* values exactly, when that file is present.

CAVEATS.  (1) universe.json (56) and universe_broad.json (136) are CURRENT-CONSTITUENT lists
— SURVIVORSHIP; absolute CAGRs are optimistic on both, and B136 CONTAINS U56, so two panels
is not two independent samples.  (2) Gross is capped at 1.00; a c* only leverage would move
is reported as unmoved.  (3) c* is a breakeven, not a return: a high-c* book with a bad level
is still a bad book, and [5] reports the levels beside it.  (4) Class sizes are unequal
(R 2 families, P 2, X 3) and the informative-cell counts are small; the partition test is
reported as exact counts plus a one-sided Fisher p, not as an asymptotic claim.

Deterministic, standalone.  Reads baseline.py only; modifies nothing.
"""
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                          # noqa: E402

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
B_FIXED = 0.40                 # idea 42's pinned breadth threshold
RAND_SEED = 394                # fixed, published, never searched
IDEA335 = (REPO / "research" / "backtests" /
           "2026-09-07_does-the-c-star-EQUALITY-at-20-bps-generalise_C.grid.csv")

# family -> (timing class, dial name, dial values)
FAMILIES = {
    "VOLCAP":    dict(cls="R", dial="target", vals=[0.10, 0.15, 0.25]),
    "DDCTL":     dict(cls="R", dial="T",      vals=[0.05, 0.10, 0.20]),
    "BREADTH":   dict(cls="P", dial="depth",  vals=[0.75, 0.50, 0.25]),
    "NAMEFLOOR": dict(cls="P", dial="F",      vals=[10, 20, 30]),
    "CALCAD":    dict(cls="X", dial="depth",  vals=[0.75, 0.50, 0.25]),
    "TURNBUD":   dict(cls="X", dial="q",      vals=[0.50, 0.75, 0.90]),
    "RANDOM":    dict(cls="X", dial="p",      vals=[0.10, 0.25, 0.50]),
}
CLASSNAME = {"R": "R own realised risk", "P": "P panel state", "X": "X neither (exogenous)"}
# the queue's own classification, kept so the answer can be read both ways
QUEUE_CLS = dict(FAMILIES["NAMEFLOOR"], cls="X")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ book construction
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


# ------------------------------------------------------------------ simulator (idea 335's)
def fast_bt(px, w, freq):
    """engine.backtest at cost_bps=0, in numpy.  Returns (returns, turnover, gross)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    reb = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
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
        port[i] = float((cur * rets[i]).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx), pd.Series(gr, index=idx))


def apply_mult(r0, turn0, gross0, m):
    """Idea 41's book-level overlay convention, verbatim."""
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


# ---- class R: timed on the book's own realised risk
def mult_volcap(px, r0, turn0, gross0, target):
    v = (r0.rolling(20).std() * np.sqrt(252.0)).shift(1)
    return (target / v).clip(upper=1.0).fillna(1.0)


def mult_ddctl(px, r0, turn0, gross0, T):
    eq = (1.0 + r0).cumprod()
    dd = (eq / eq.cummax() - 1.0).shift(1).fillna(0.0)
    return pd.Series(np.where(dd.values < -T, 0.50, 1.0), index=px.index)


# ---- class P: timed on the panel's state
def mult_breadth(px, r0, turn0, gross0, depth):
    on = (panel_breadth(px).shift(1) < B_FIXED).fillna(False)
    return pd.Series(np.where(on.values, depth, 1.0), index=px.index)


def mult_namefloor(px, r0, turn0, gross0, F):
    e = eligible_mask(px).sum(axis=1).astype(float).shift(1)
    return (e / float(F)).clip(upper=1.0).fillna(1.0)


# ---- class X: timed on neither
def mult_calcad(px, r0, turn0, gross0, depth):
    on = px.index.month.isin([5, 6, 7, 8, 9, 10])
    return pd.Series(np.where(on, depth, 1.0), index=px.index)


def mult_turnbud(px, r0, turn0, gross0, q):
    t63 = turn0.rolling(63, min_periods=63).sum()
    thr = t63.expanding(252).quantile(q)
    on = (t63 > thr).shift(1).fillna(False)
    return pd.Series(np.where(on.values, 0.50, 1.0), index=px.index)


def _week_draws(idx, p):
    """Bernoulli(p) per ISO week, keyed on the week so both panels share the schedule."""
    iso = idx.isocalendar()
    keys = (iso["year"].astype(int) * 100 + iso["week"].astype(int)).values
    uniq = np.unique(keys)
    rng = np.random.default_rng(RAND_SEED)
    u = rng.random(len(uniq))
    on = dict(zip(uniq, u < p))
    return np.array([on[k] for k in keys])


def mult_random(px, r0, turn0, gross0, p):
    on = _week_draws(px.index, p)
    return pd.Series(np.where(on, 0.50, 1.0), index=px.index)


MULT = {"VOLCAP": mult_volcap, "DDCTL": mult_ddctl, "BREADTH": mult_breadth,
        "NAMEFLOOR": mult_namefloor, "CALCAD": mult_calcad, "TURNBUD": mult_turnbud,
        "RANDOM": mult_random}


# ------------------------------------------------------------------ metrics (idea 335's)
def nm3(r):
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
        self.ref = ref
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


def cnum(v):
    """c* as a comparable number: 'never' beats every finite crossing."""
    return CMAX * 10 if (v is None or (isinstance(v, float) and np.isnan(v))) else v


def cnum_s(col):
    return col.fillna(CMAX * 10)


def fmt(v, nev="never"):
    return nev if (v is None or (isinstance(v, float) and np.isnan(v))) else f"{v:.2f}"


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


def fisher_1s(a, b, c, d):
    """One-sided Fisher exact p for the 2x2 [[a,b],[c,d]]: P(X >= a) under the margins."""
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2
    lo, hi = max(0, c1 - r2), min(r1, c1)
    tot = math.comb(n, c1)
    return sum(math.comb(r1, k) * math.comb(r2, c1 - k) for k in range(a, hi + 1)) / tot if tot else np.nan


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# {SLUG}")
    P("# idea 394 — does 'the overlay widens the book's cost breakeven c*' partition by WHAT")
    P("#            the overlay is timed on?  R = own realised risk | P = panel state |")
    P("#            X = neither (calendar / turnover budget / fixed-seed random).")
    P(f"# parent NF20 (top-{N0} eligible, equal weight, no vol scaler, weekly, t+1) | rungs {RUNGS}")
    P(f"# 7 book-level families x 3 dials x 3 rungs x 2 panels = 126 cells, all reported")
    P(f"# c* ladder [0, {CMAX:.0f}] bps | 4b vs SPY, 4a vs the LIVE RULES v2 | matched-gross control")
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
    P("=" * 152)
    P("[0] REPRODUCTION GATES (all asserted before any new number is read)")
    gpx = panels[0][1]
    gw = parent_weights(gpx, 0.75)
    r0g, tg, grg = fast_bt(gpx, gw, FREQ)
    g1 = 0.0
    for c in (0, 25):
        eng = backtest(gpx, gw, cost_bps=c, freq=FREQ)
        g1 = max(g1, float((r0g - tg * c / 1e4 - eng["returns"]).abs().max()),
                 float((tg - eng["turnover"]).abs().max()))
    P(f"    G1  fast_bt == engine.backtest (returns AND turnover, c in 0/25 bps): max |d| {g1:.3e}")
    assert g1 < 1e-12, g1

    ones = pd.Series(1.0, index=gpx.index)
    rB, tB, grB = apply_mult(r0g, tg, grg, ones)
    g3 = max(float((rB - r0g).abs().max()), float((tB - tg).abs().max()),
             float((grB - grg).abs().max()))
    P(f"    G3  overlay at OFF (m == 1) == parent, on r, turnover AND gross: max |d| {g3:.3e}")
    assert g3 < 1e-12, g3

    g4 = max(float((1.0 * r0g - r0g).abs().max()), float((1.0 * tg - tg).abs().max()))
    P(f"    G4  matched control at a = 1 == parent: max |d| {g4:.3e}")
    assert g4 < 1e-12, g4

    g5 = 0.0
    for a in (0.25, 0.50, 0.85, 1.00):
        for c in (0, 10, 25):
            base = (r0g - tg * c / 1e4).values
            g5 = max(g5, abs(sharpe(a * base) - sharpe(base)))
    P(f"    G5  SHARPE INVARIANCE of the gross dial (a in 0.25..1.00, c in 0/10/25): max |dSharpe| "
      f"{g5:.3e}  -> the control's c* moves only through CAGR/MaxDD")
    assert g5 < 1e-12, g5

    d1, d2 = _week_draws(gpx.index, 0.25), _week_draws(gpx.index, 0.25)
    g9a = int((d1 != d2).sum())
    shared = panels[1][1].index.intersection(gpx.index)
    e1 = pd.Series(_week_draws(gpx.index, 0.25), index=gpx.index).loc[shared]
    e2 = pd.Series(_week_draws(panels[1][1].index, 0.25), index=panels[1][1].index).loc[shared]
    g9b = int((e1.values != e2.values).sum())
    P(f"    G9  RANDOM schedule reproducible: {g9a} disagreements on a re-draw; panel-independent "
      f"on the {len(shared)} shared days: {g9b} disagreements  (on-share {d1.mean():.3f} vs p=0.25)")
    assert g9a == 0 and g9b == 0

    br = panel_breadth(gpx)
    ec = eligible_mask(gpx).sum(axis=1).astype(float)
    ok = br.notna() & ec.notna()
    P(f"    G10 NAMEFLOOR's E_t vs panel breadth on U56: pearson "
      f"{float(np.corrcoef(ec[ok], br[ok])[0, 1]):+.3f}, spearman "
      f"{spearman(ec[ok].values, br[ok].values):+.3f}  -> E_t IS the panel-state variable, so")
    P("        NAMEFLOOR is filed under class P, not the queue's class X.  [2] reports both readings.")

    # ================================================================ per-panel build
    grid, wf, parents, G6 = [], [], [], []
    P("")
    for panel, px in panels:
        start = px.index[WARMUP]
        sub = px.loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2w = rules_v2_weights(px)
        v2r, v2t, _ = fast_bt(px, v2w, FREQ)
        ref = PanelRef(sub.index, spy.values, v2r.loc[start:].values, v2t.loc[start:].values)
        sc, ss, sdd = nm3(ref.spy_r)
        P("=" * 152)
        P(f"PANEL {panel}: {px.shape[1]} cols | {px.index[0].date()} -> {px.index[-1].date()} | "
          f"eval {start.date()} .. {px.index[-1].date()}")
        P(f"    SPY  {sc:.2%} / {ss:.3f} (H1 {ref.spy['full']['H1']:.3f} / H2 "
          f"{ref.spy['full']['H2']:.3f} / OOS {ref.spy['full']['OOS']:.3f}) / {sdd:.2%}   "
          f"| 4b bars: DD cap {DD_CAP*ref.spy['full']['DD']:.2%}, CAGR floor "
          f"{CAGR_FLOOR*ref.spy['full']['CAGR']:.2%}")
        v2s = ref.v2.stats(10)
        P(f"    RULES v2 @10bps  {v2s['CAGR']:.2%} / {v2s['Sharpe']:.3f} / {v2s['MaxDD']:.2%} "
          f"(H1 {v2s['H1']:.3f} / H2 {v2s['H2']:.3f})  c*_4b {fmt(cstar(ref.v2,'4b'))}")

        for g0 in RUNGS:
            w = parent_weights(px, g0)
            pr0f, ptnf, pgrf = fast_bt(px, w, FREQ)        # FULL history, for the signals
            pr0, ptn, pgr = pr0f.loc[start:], ptnf.loc[start:], pgrf.loc[start:]
            par = Path4(sub.index, pr0.values, ptn.values, ref)
            par.gross_mean = float(pgr.mean())
            ps = par.stats(10)
            pc = {(p_, wn): cstar(par, p_, wn) for p_ in ("4a", "4b")
                  for wn in ("full", "is", "oos")}
            parents.append(dict(panel=panel, g0=g0, gross_mean=par.gross_mean,
                                turnover_yr=par.turnover_yr,
                                **{f"p_{k}": v for k, v in ps.items()},
                                cstar4b=pc[("4b", "full")], cstar4a=pc[("4a", "full")],
                                cstar4b_is=pc[("4b", "is")], cstar4b_oos=pc[("4b", "oos")]))
            P(f"  PARENT g0={g0:.2f}  gross {par.gross_mean:.3f}  turn/yr {par.turnover_yr:.2f}  "
              f"@10bps {ps['CAGR']:.2%} / {ps['Sharpe']:.3f} / {ps['MaxDD']:.2%}  "
              f"c*_4b {fmt(pc[('4b','full')]):>6s}  c*_4a {fmt(pc[('4a','full')]):>6s}")

            for fam, spec in FAMILIES.items():
                for dv in spec["vals"]:
                    mf = MULT[fam](px, pr0f, ptnf, pgrf, dv)   # signal on the FULL history
                    m = mf.loc[start:]
                    orr, otn, ogr = apply_mult(pr0, ptn, pgr, m)
                    on_frac = float((m < 1.0 - 1e-12).mean())
                    ov = Path4(sub.index, orr.values, otn.values, ref)
                    ov.gross_mean = float(ogr.mean())

                    a = ov.gross_mean / par.gross_mean if par.gross_mean > 0 else np.nan
                    ct = Path4(sub.index, a * par.r0, a * par.turn, ref)
                    ct.gross_mean = a * par.gross_mean

                    row = dict(panel=panel, g0=g0, cls=spec["cls"], family=fam,
                               dial=spec["dial"], dial_val=dv, on_frac=on_frac, alpha=a,
                               gross_parent=par.gross_mean, gross_overlay=ov.gross_mean,
                               gross_match_err=abs(ct.gross_mean - ov.gross_mean),
                               turn_parent=par.turnover_yr, turn_overlay=ov.turnover_yr,
                               turn_ctrl=ct.turnover_yr)
                    for pth in ("4b", "4a"):
                        for wn in ("full", "is", "oos"):
                            co, cc = cstar(ov, pth, wn), cstar(ct, pth, wn)
                            row[f"cstar_ov_{pth}_{wn}"] = co
                            row[f"cstar_ct_{pth}_{wn}"] = cc
                            row[f"identity_{pth}_{wn}"] = bool(cnum(co) <= cnum(cc) + 1e-9)
                            row[f"gap_{pth}_{wn}"] = cnum(co) - cnum(cc)
                            row[f"informative_{pth}_{wn}"] = bool(cnum(co) > 0 or cnum(cc) > 0)
                    row["ov_Sharpe_is_10"] = ov.stats(10, "is")["Sharpe"]
                    row["ov_CAGR_is_10"] = ov.stats(10, "is")["CAGR"]
                    so = ov.stats(10, "oos")
                    row["ov_CAGR_oos_10"], row["ov_Sharpe_oos_10"], row["ov_MaxDD_oos_10"] = \
                        so["CAGR"], so["Sharpe"], so["MaxDD"]
                    if len(grid) < 12:
                        G6.append(abs(cnum(cstar(ov, "4b")) - cnum(row["cstar_ov_4b_full"])))
                    for c in COSTS:
                        s_o, s_c = ov.stats(c), ct.stats(c)
                        row[f"ov_CAGR_{c}"], row[f"ov_Sharpe_{c}"], row[f"ov_MaxDD_{c}"] = \
                            s_o["CAGR"], s_o["Sharpe"], s_o["MaxDD"]
                        row[f"ct_Sharpe_{c}"] = s_c["Sharpe"]
                        m4b, m4a = ov.m4b(c), ov.m4a(c)
                        row[f"keep4b_{c}"] = bool(min(m4b.values()) > 0)
                        row[f"keep4a_{c}"] = bool(min(m4a.values()) > 0)
                        row[f"fail4b_{c}"] = ",".join(k for k, v in m4b.items() if v <= 0) or "-"
                    grid.append(row)

            # ---- rule 8 walk-forward for this (panel, rung): dial chosen on IS ONLY
            par_oos = par.stats(10, "oos")
            v2_oos = ref.v2.stats(10, "oos")
            spy_oos = dict(zip(("CAGR", "Sharpe", "MaxDD"), nm3(ref.spy_r[ref.oos])))
            for fam, spec in FAMILIES.items():
                sub_g = [r for r in grid if r["panel"] == panel and r["g0"] == g0
                         and r["family"] == fam]
                for chooser, key in [
                        ("IS c*_4b", lambda r: (cnum(r["cstar_ov_4b_is"]), r["ov_Sharpe_is_10"])),
                        ("IS Sharpe", lambda r: (r["ov_Sharpe_is_10"], cnum(r["cstar_ov_4b_is"])))]:
                    pk = max(sub_g, key=key)
                    wf.append(dict(
                        panel=panel, g0=g0, cls=spec["cls"], family=fam, chooser=chooser,
                        dial_val=pk["dial_val"], is_Sharpe=pk["ov_Sharpe_is_10"],
                        cstar_is=pk["cstar_ov_4b_is"], cstar_oos=pk["cstar_ov_4b_oos"],
                        ctrl_cstar_oos=pk["cstar_ct_4b_oos"], identity_oos=pk["identity_4b_oos"],
                        informative_oos=pk["informative_4b_oos"],
                        oos_CAGR=pk["ov_CAGR_oos_10"], oos_Sharpe=pk["ov_Sharpe_oos_10"],
                        oos_MaxDD=pk["ov_MaxDD_oos_10"],
                        par_oos_CAGR=par_oos["CAGR"], par_oos_Sharpe=par_oos["Sharpe"],
                        par_oos_MaxDD=par_oos["MaxDD"],
                        v2_oos_Sharpe=v2_oos["Sharpe"], v2_oos_CAGR=v2_oos["CAGR"],
                        v2_oos_MaxDD=v2_oos["MaxDD"],
                        spy_oos_Sharpe=spy_oos["Sharpe"], spy_oos_CAGR=spy_oos["CAGR"],
                        spy_oos_MaxDD=spy_oos["MaxDD"],
                        keep4b_10=pk["keep4b_10"], keep4a_10=pk["keep4a_10"]))

    G = pd.DataFrame(grid)
    G["dSharpe_10"] = G.ov_Sharpe_10 - G.ct_Sharpe_10
    PAR = pd.DataFrame(parents)
    W = pd.DataFrame(wf)

    # ================================================================ [1] remaining gates
    P("")
    P("=" * 152)
    P("[1] GATES G6 / G8 / G11 (post-build)")
    P(f"    G6  c* recomputed on the first {len(G6)} cells: max |d| {max(G6):.3e}")
    assert max(G6) < 1e-12
    P(f"    G8  matched-gross solve: max |mean gross(control) - mean gross(overlay)| over all "
      f"{len(G)} cells: {G.gross_match_err.abs().max():.3e}")
    assert G.gross_match_err.abs().max() < 1e-12
    vac = G[(G.on_frac <= 0) | (G.alpha >= 1.0 - 1e-12)]
    P(f"    G8  vacuous cells (overlay never fires, or a >= 1): {len(vac)} / {len(G)}"
      + ("" if not len(vac) else "  -> " + ", ".join(
          f"{r.panel}/{r.family}={r.dial_val}" for r in vac.itertuples())))
    P("        on_frac by family: " + ", ".join(
        f"{k} {v:.3f}" for k, v in G.groupby("family").on_frac.mean().items()))
    if IDEA335.exists():
        old = pd.read_csv(IDEA335)
        j = G.merge(old, on=["panel", "g0", "family", "dial_val"], suffixes=("", "_335"))
        d = 0.0
        for c in ("cstar_ov_4b_full", "cstar_ct_4b_full", "gross_overlay"):
            d = max(d, float((j[c].pipe(cnum_s) - j[f"{c}_335"].pipe(cnum_s)).abs().max()))
        P(f"    G11 idea 335's {len(j)} overlapping cells (BREADTH/DDCTL/VOLCAP) reproduce its "
          f"committed .grid.csv: max |d| on c*(overlay), c*(control), mean gross = {d:.3e}")
        assert d < 1e-9, d
    else:
        P("    G11 idea 335's grid.csv not present — overlap check skipped")

    # ================================================================ [2] THE PARTITION
    P("")
    P("=" * 152)
    P("[2] THE PARTITION — does 'widens c*' sort by what the overlay is timed on?")
    P("    A cell WIDENS when c*(overlay) > c*(matched-gross control).  Only INFORMATIVE cells")
    P("    count (at least one side has a non-zero c*); 0 <= 0 cells carry no information.")
    for pth in ("4b", "4a"):
        for wn in ("full", "is", "oos"):
            inf = G[G[f"informative_{pth}_{wn}"]]
            P("")
            P(f"    --- {pth} / {wn} : {len(inf)} informative of {len(G)} cells")
            if not len(inf):
                continue
            t = inf.groupby(["cls", "family"]).agg(
                n=(f"identity_{pth}_{wn}", "size"),
                widens=(f"identity_{pth}_{wn}", lambda x: int((~x).sum())),
                max_gap=(f"gap_{pth}_{wn}", "max"),
                med_gap=(f"gap_{pth}_{wn}", "median"))
            P("      " + t.to_string(float_format=lambda x: f"{x:+.2f}").replace("\n", "\n      "))
            byc = inf.groupby("cls").agg(n=(f"identity_{pth}_{wn}", "size"),
                                         widens=(f"identity_{pth}_{wn}", lambda x: int((~x).sum())),
                                         max_gap=(f"gap_{pth}_{wn}", "max"))
            byc["rate"] = byc.widens / byc.n
            P("      by CLASS: " + " | ".join(
                f"{CLASSNAME[i]}: {r.widens}/{r.n} ({r.rate:.1%}, max {r.max_gap:+.2f} bps)"
                for i, r in byc.iterrows()))

    P("")
    P("    PARTITION TEST (4b / full, informative cells): risk-timed vs exogenous.")
    inf = G[G.informative_4b_full]
    for lbl, xset in [("as filed  (NAMEFLOOR in P)", {"CALCAD", "TURNBUD", "RANDOM"}),
                      ("queue's classification (NAMEFLOOR in X)",
                       {"CALCAD", "TURNBUD", "RANDOM", "NAMEFLOOR"})]:
        r_ = inf[inf.family.isin({"VOLCAP", "DDCTL"})]
        x_ = inf[inf.family.isin(xset)]
        p_ = inf[~inf.family.isin({"VOLCAP", "DDCTL"} | xset)]
        a, b = int((~r_.identity_4b_full).sum()), int(r_.identity_4b_full.sum())
        c_, d_ = int((~x_.identity_4b_full).sum()), int(x_.identity_4b_full.sum())
        pv = fisher_1s(a, b, c_, d_)
        P(f"      {lbl}:  R widens {a}/{a+b}   X widens {c_}/{c_+d_}   "
          f"P widens {int((~p_.identity_4b_full).sum())}/{len(p_)}   "
          f"one-sided Fisher p(R >= observed) = {pv:.4f}")

    P("")
    P("    MECHANISM.  G5 pins the control's Sharpe to the parent's at every cost, so the")
    P("    control's c* moves only through CAGR/MaxDD while the overlay's also moves through")
    P("    Sharpe.  dSharpe = overlay - control at 10 bps:")
    mech = G.groupby(["cls", "family"]).agg(mean_dSharpe=("dSharpe_10", "mean"),
                                            max_dSharpe=("dSharpe_10", "max"),
                                            widens=("identity_4b_full", lambda x: int((~x).sum())))
    P("      " + mech.to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n      "))
    P(f"      spearman(dSharpe_10, gap_4b_full) over all {len(inf)} informative cells: "
      f"{spearman(inf.dSharpe_10.values, inf.gap_4b_full.values):+.3f}   "
      "(idea 335 reported +0.336 on its own 39)")
    for cl in ("R", "P", "X"):
        s = inf[inf.cls == cl]
        if len(s) > 2:
            P(f"        within {CLASSNAME[cl]}: {spearman(s.dSharpe_10.values, s.gap_4b_full.values):+.3f}"
              f"  (n={len(s)})")

    # ================================================================ [3] every grid point
    P("")
    P("=" * 152)
    P("[3] EVERY GRID POINT (4b, full sample): overlay c* vs its matched-gross control")
    show = G[["panel", "g0", "cls", "family", "dial_val", "on_frac", "gross_overlay", "alpha",
              "turn_overlay", "turn_ctrl", "cstar_ov_4b_full", "cstar_ct_4b_full", "gap_4b_full",
              "informative_4b_full", "identity_4b_full", "ov_Sharpe_10", "ct_Sharpe_10"]]
    P("    " + show.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))

    # ================================================================ [4] parents
    P("")
    P("=" * 152)
    P("[4] THE SIX PARENTS (the anchors every overlay is measured against)")
    P("    " + PAR.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))

    # ================================================================ [5] KEEP census
    P("")
    P("=" * 152)
    P("[5] KEEP-PATH CENSUS on every grid point, all three cost rungs")
    for c in COSTS:
        P(f"    @{c:>2d} bps:  4a {int(G[f'keep4a_{c}'].sum()):>3d}/{len(G)}   "
          f"4b {int(G[f'keep4b_{c}'].sum()):>3d}/{len(G)}")
    P("    failing-4b-bar distribution @10 bps: "
      + ", ".join(f"{k}={v}" for k, v in G["fail4b_10"].value_counts().items()))
    k10 = G[G["keep4b_10"]]
    if len(k10):
        P(f"    the {len(k10)} cells clearing 4b @10 bps:")
        P("      " + k10[["panel", "g0", "cls", "family", "dial_val", "ov_CAGR_10", "ov_Sharpe_10",
                          "ov_MaxDD_10", "cstar_ov_4b_full", "cstar_ct_4b_full", "identity_4b_full"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))
    else:
        P("    no cell clears 4b @10 bps")

    # ================================================================ [6] rule 8
    P("")
    P("=" * 152)
    P("[6] RULE 8 WALK-FORWARD — dial chosen on 2008-2016 ONLY, 2017-2026 read once")
    cols = ["panel", "g0", "cls", "family", "chooser", "dial_val", "cstar_is", "cstar_oos",
            "ctrl_cstar_oos", "informative_oos", "identity_oos", "oos_CAGR", "oos_Sharpe",
            "oos_MaxDD", "par_oos_CAGR", "par_oos_Sharpe", "par_oos_MaxDD", "v2_oos_Sharpe",
            "spy_oos_CAGR", "spy_oos_Sharpe", "spy_oos_MaxDD", "keep4b_10", "keep4a_10"]
    P("    " + W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))
    infW = W[W.informative_oos]
    P("")
    P(f"    OOS identity for the IS-chosen dial: holds {int(infW.identity_oos.sum())}/{len(infW)} "
      f"informative ({len(W)} arms total).  Widening by class, OOS, IS-chosen only:")
    if len(infW):
        t = infW.groupby("cls").agg(n=("identity_oos", "size"),
                                    widens=("identity_oos", lambda x: int((~x).sum())))
        P("      " + t.to_string().replace("\n", "\n      "))
    P(f"    OOS Sharpe of the IS-chosen arms vs SPY: {int((W.oos_Sharpe > W.spy_oos_Sharpe).sum())}"
      f"/{len(W)} beat SPY; vs RULES v2: {int((W.oos_Sharpe > W.v2_oos_Sharpe).sum())}/{len(W)}; "
      f"vs their own parent: {int((W.oos_Sharpe > W.par_oos_Sharpe).sum())}/{len(W)}")
    P(f"    IS-chosen arms clearing the FULL bar set @10 bps: 4b {int(W.keep4b_10.sum())}/{len(W)}, "
      f"4a {int(W.keep4a_10.sum())}/{len(W)}")
    best = W.loc[W.oos_Sharpe.idxmax()]
    P(f"    best OOS Sharpe among IS-chosen arms: {best.panel} g0={best.g0:.2f} {best.family}="
      f"{best.dial_val} ({best.chooser}) -> OOS {best.oos_CAGR:.2%} / {best.oos_Sharpe:.3f} / "
      f"{best.oos_MaxDD:.2%}  vs parent {best.par_oos_CAGR:.2%} / {best.par_oos_Sharpe:.3f} / "
      f"{best.par_oos_MaxDD:.2%}, RULES v2 {best.v2_oos_CAGR:.2%} / {best.v2_oos_Sharpe:.3f}, "
      f"SPY {best.spy_oos_CAGR:.2%} / {best.spy_oos_Sharpe:.3f} / {best.spy_oos_MaxDD:.2%}")

    # ================================================================ [7] verdict
    P("")
    P("=" * 152)
    P("[7] VERDICT")
    infR = inf[inf.cls == "R"]
    infX = inf[inf.cls == "X"]
    infP = inf[inf.cls == "P"]
    wR, wX, wP = int((~infR.identity_4b_full).sum()), int((~infX.identity_4b_full).sum()), \
        int((~infP.identity_4b_full).sum())
    P(f"    4b / full, informative only:  R {wR}/{len(infR)} widen   P {wP}/{len(infP)}   "
      f"X {wX}/{len(infX)}")
    if wX == 0 and wR > 0:
        P("    -> the partition HOLDS on this corpus: only overlays timed on the book's own")
        P("       realised risk widen its cost breakeven; calendar, turnover-budget and")
        P("       fixed-seed-random overlays never do.")
    elif wX > 0 and wR > 0:
        P("    -> the partition FAILS: exogenous overlays widen c* too, so 'widens c*' is not a")
        P("       property of what the overlay is timed on.  A cost budget cannot be screened by")
        P("       timing class.")
    else:
        P("    -> neither class widens on this corpus; idea 335's family split does not reproduce")
        P("       under the book-level-only convention, so there is nothing to partition.")
    P(f"    KEEP: 4a {int(G.keep4a_10.sum())}/{len(G)} @10 bps, "
      f"4b {int(G.keep4b_10.sum())}/{len(G)} @10 bps, "
      f"{int(G.keep4b_25.sum())}/{len(G)} @25 bps.")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    PAR.to_csv(f"{OUT}.parents.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P(f"Wrote {OUT.name}.grid.csv ({len(G)}), .parents.csv ({len(PAR)}), "
      f".walkforward.csv ({len(W)})  [{time.time()-t0:.1f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
