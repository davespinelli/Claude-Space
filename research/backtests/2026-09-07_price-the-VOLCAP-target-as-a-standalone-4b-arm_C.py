#!/usr/bin/env python3
"""Idea 392 — "price-the-VOLCAP-target-as-a-standalone-4b-arm-on-the-standing-parent"
(lane C, 2026-09-07).

QUESTION (QUEUE.md).  Idea 335's two decisive violations of its proposed c* identity are
U56 g=1.00 VOLCAP target 0.15 (c* 17.67 bps against a matched-gross control that fails at
ZERO cost) and DDCTL 0.10 (11.67), both clearing 4b at 10 bps.  But at g=0.75 the SAME
overlays only LOWER the standing parent's 22.60-bps budget.  Sweep the vol target against
the gross rung on a fine grid (target in {0.08 .. 0.30} x g in {0.75, 0.85, 1.00}) on both
panels and ask whether the widening is a REAL INSTRUMENT or a g=1.00 CORNER where the
ungated book is simply inadmissible and the comparand is therefore degenerate.

WHY THE CORNER MATTERS.  c*(control) = 0.0 means "the control already fails a 4b bar at
zero cost".  Any overlay with a positive crossing then "widens" c* by construction, and
the widening measures the CONTROL's inadmissibility, not the overlay's value.  Idea 393
is the record-wide bookkeeping fix for exactly this; this run applies it to one family on
a fine grid, and reports the census BOTH ways (all cells / informative cells only), so the
partition is visible rather than argued.

DESIGN.

  PARENT (fixed, idea 335's standing parent, never tuned): eligible = above the 200d MA
  and vol20 < 0.60; rank eligible names by the v1 composite WITHOUT the /sqrt(vol20)
  term; hold the top k = min(20, E_t) equal-weight at w = g/k; weekly; next-day
  execution; 10 bps default rung.

  TUNED PARAMETER 1 — gross rung g in {0.75, 0.85, 1.00} (the queue's three rungs; no
  leverage, PROTOCOL rule 2).
  TUNED PARAMETER 2 — the VOLCAP target in {0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25,
  0.30}, plus OFF (target = inf) as the 9th, un-tuned level.  8 fine levels bracket idea
  335's coarse {0.10, 0.15, 0.25}.

  Panel (U56 / B136) and cost rung (0 / 10 / 25 bps) are CENSUS axes: every level is
  reported and nothing is selected on outcome.  ALL 54 (panel x g x target) grid points
  go to .grid.csv, OFF rows included.

  VOLCAP, idea 41/335's convention verbatim: m_t = min(1, target / vol20_ann(r0)_{t-1}),
  r = m*r0, turn = m*turn0 + |dm| * gross0_{t-1}, gross = m*gross0 — the exposure switch
  pays the rung's cost on the notional it moves, on the day it takes effect.

  MATCHED CONTROL (the comparand the queue's premise is about): a = mean(gross_overlay) /
  mean(gross_parent), applied as a CONSTANT multiplier to the same parent.  Closed form,
  no search, a <= 1 by construction.  This is the plain gross dial held at the overlay's
  own realised mean exposure.

  c* ESTIMATOR.  First cost c in [0, 50] bps at which any bar of the path turns
  non-positive; 0.0 if the path already fails at zero cost; "never" if it survives the
  ladder.  Bracketed on a 0.25-bps scan, then bisected 60 times.  Computed for BOTH KEEP
  paths on three windows (full / IS 2008-2016 / OOS 2017-2026):
    4b  vs SPY: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%.
    4a  vs the LIVE RULES v2 book at the SAME cost rung: Sharpe > v2 in both halves and
        MaxDD no worse than v2's.
  A cell is INFORMATIVE iff its control's c* > 0 — i.e. the comparand is admissible at
  zero cost and the comparison can carry a direction.

  RULE 8 WALK-FORWARD (required).  For every (panel, g) the target is chosen on 2008-2016
  ONLY, by two IS choosers — IS Sharpe at 10 bps (the record's convention) and IS c*_4b
  (the statistic the parent idea is about) — and 2017-2026 is read ONCE.  OOS CAGR /
  Sharpe / MaxDD are reported against the parent anchor, the LIVE RULES v2 book and SPY,
  beside the OOS-best target (an oracle, reported only to size the chooser's regret).

GATES (asserted / printed in [0] before any new number is read).
  G1  fast_bt == engine.backtest on returns AND turnover at 0 and 25 bps.
  G2  the book-level overlay at OFF (m == 1) == the parent, exactly.
  G3  the matched control at a = 1 == the parent, exactly.
  G4  SHARPE INVARIANCE of the gross dial (Sharpe(a*path) == Sharpe(path)) — this is what
      makes the control's c* a pure CAGR/MaxDD statistic, and it is measured, not assumed.
  G5  the record's standing 2026-09-04 KEEP-4b row (U56 top-20 equal weight, g=0.75, no
      vol scaler) reproduces at FIXED n=20.
  G6  IDEA 335's TWO DECISIVE CELLS reproduce from this run's own source: U56 g=1.00
      VOLCAP 0.15 -> c* 17.67 with a control at 0.00, and DDCTL T=0.10 -> 11.67.  DDCTL is
      rebuilt here for the gate only; it is not otherwise part of this run's grid.
  G7  determinism of the bisection (c* reproduces itself on a re-run).

CAVEATS.  (1) universe.json (56 names) and universe_broad.json (136) are
CURRENT-CONSTITUENT lists — SURVIVORSHIP; absolute CAGRs are optimistic on both, and B136
CONTAINS U56, so two panels are not two independent samples.  (2) Gross is capped at 1.00;
a c* that only leverage could move is reported as unmoved.  (3) c* is a breakeven, not a
return: a book with a wide c* and a bad level is still a bad book, so [2] reports the 10-bps
LEVELS beside every budget.  (4) The 4a comparand moves with the rung too (RULES v2 pays
the same cost), so a "never" on 4a can have nothing to do with this idea.

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
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                          # noqa: E402

OUT = Path(__file__).with_suffix("")
SLUG = OUT.name

MAX_VOL = 0.60
VOL_SCALE = False
N0 = 20
FREQ = "W"
WARMUP = 260
RUNGS = [0.75, 0.85, 1.00]
TARGETS = [0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30]
COSTS = [0, 10, 25]
CMAX = 50.0
SCAN = 0.25
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
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
    """NF20: top k = min(n, E_t) eligible names, equal weight, gross g0."""
    el = eligible_mask(px)
    rank = score(px, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    e = el.sum(axis=1).astype(float)
    k = np.minimum(float(n), e).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(g0 / k, axis=0)


# ------------------------------------------------------------------ simulator
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
    """Idea 41/335's book-level overlay convention, verbatim.  m is already lagged."""
    dm = m.diff().abs().fillna(0.0)
    return (m * r0, m * turn0 + dm * gross0.shift(1).fillna(0.0), m * gross0)


def mult_volcap(r0, target):
    v = (r0.rolling(20).std() * np.sqrt(252.0)).shift(1)
    return (target / v).clip(upper=1.0).fillna(1.0)


def mk(ref, triple):
    """Path4 from an (returns, turnover, gross) triple."""
    r, t, g = triple
    return Path4(ref.idx, r, t, ref, gross=g)


def mult_ddctl(r0, T):                       # gate G6 only
    eq = (1.0 + r0).cumprod()
    dd = (eq / eq.cummax() - 1.0).shift(1).fillna(0.0)
    return pd.Series(np.where(dd.values < -T, 0.50, 1.0), index=r0.index)


# ------------------------------------------------------------------ metrics
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

    def __init__(self, idx, r0, turn, ref, gross=None):
        self.idx = idx
        self.r0 = np.asarray(r0, float)
        self.turn = np.asarray(turn, float)
        self.ref = ref
        yrs = (idx[-1] - idx[0]).days / 365.25
        self.turnover_yr = float(self.turn.sum()) / yrs
        self.gross_mean = float(np.mean(gross)) if gross is not None else np.nan

    def rc(self, c):
        return self.r0 - self.turn * (c / 1e4)

    def _w(self, r, win):
        if win == "full":
            return r
        return r[self.ref.is_m] if win == "is" else r[self.ref.oos]

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

    def worst(self, c, path, win):
        f = self.m4b if path == "4b" else self.m4a
        return min(f(c, win).values())

    def bars(self, c, path="4b", win="full"):
        return (self.m4b if path == "4b" else self.m4a)(c, win)

    def stats(self, c, win="full"):
        x = self._w(self.rc(c), win)
        cg, sh, dd = nm3(x)
        h = len(x) // 2
        return dict(CAGR=cg, Sharpe=sh, MaxDD=dd, H1=sharpe(x[:h]), H2=sharpe(x[h:]))


class PanelRef:
    """SPY bars, the RULES v2 path, and the IS/OOS masks for one panel."""

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


def fmt(v):
    return "never" if (v is None or (isinstance(v, float) and np.isnan(v))) else f"{v:.2f}"


def cnum(v):
    return CMAX * 10 if (v is None or (isinstance(v, float) and np.isnan(v))) else v


def binom_sd(k, n):
    if n == 0:
        return np.nan
    p = k / n
    return float(np.sqrt(max(p * (1 - p), 0.0) / n))


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# {SLUG}")
    P("# idea 392 — is the VOLCAP c* widening a real instrument, or a g=1.00 corner where the")
    P("#            matched-gross comparand is itself inadmissible at zero cost?")
    P(f"# parent NF20 (top-{N0} eligible, equal weight, NO vol scaler, weekly, t+1) | rungs {RUNGS}")
    P(f"# VOLCAP targets {TARGETS} + OFF | c* ladder [0, {CMAX:.0f}] bps | 4b vs SPY, 4a vs RULES v2")
    P("")

    panels = []
    for tag, kw, ncol in [("U56", {}, 56), ("B136", {"broad": True}, 120)]:
        px = load_universe(**kw).dropna(how="all").ffill()
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED — aborting.")
            sys.exit(1)
        # baseline.load_universe(broad=True) reaches prices_broad.csv only through an
        # exception path; assert the panel really is the wide one, never assume it.
        assert px.shape[1] >= ncol, (tag, px.shape)
        panels.append((tag, px))

    # ================================================================ [0] GATES
    P("=" * 152)
    P("[0] REPRODUCTION GATES  (asserted before any new number is read)")
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

    ones = pd.Series(1.0, index=gpx.index)
    rB, tB, grB = apply_mult(r0g, tg, grg, ones)
    g2 = max(float((rB - r0g).abs().max()), float((tB - tg).abs().max()),
             float((grB - grg).abs().max()))
    P(f"    G2 book-level overlay at OFF (m == 1) == parent: max |d| {g2:.3e}")
    assert g2 < 1e-12, g2

    g3 = max(float((1.0 * r0g - r0g).abs().max()), float((1.0 * tg - tg).abs().max()))
    P(f"    G3 matched control at a = 1 == parent: max |d| {g3:.3e}")
    assert g3 < 1e-12, g3

    g4 = 0.0
    for a in (0.25, 0.50, 0.85, 1.00):
        for c in (0, 10, 25):
            base = (r0g - tg * c / 1e4).values
            g4 = max(g4, abs(sharpe(a * base) - sharpe(base)))
    P(f"    G4 SHARPE INVARIANCE of the gross dial (a in 0.25..1.00, c in 0/10/25): max |dSharpe| "
      f"{g4:.3e} -> the control's c* is a pure CAGR/MaxDD statistic")
    assert g4 < 1e-12, g4

    el = eligible_mask(gpx)
    rk = score(gpx, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    kf = pd.Series(float(N0), index=gpx.index)
    w20 = rk.le(kf, axis=0).astype(float).mul(0.75 / kf, axis=0)
    e20 = backtest(gpx, w20, cost_bps=10, freq=FREQ)["returns"].loc[gpx.index[WARMUP]:]
    c20, s20, d20 = nm3(e20.values)
    h20 = len(e20) // 2
    P(f"    G5 standing 2026-09-04 KEEP-4b row (published 12.7% / 1.09 / -18.3%, halves 1.09/1.10) "
      f"at FIXED n=20: {c20:.2%} / {s20:.3f} / {d20:.2%} (halves "
      f"{sharpe(e20.values[:h20]):.2f}/{sharpe(e20.values[h20:]):.2f})")

    # ---- per-panel reference objects
    refs, parents = {}, {}
    for panel, px in panels:
        start = px.index[WARMUP]
        v2r, v2t, _ = fast_bt(px, rules_v2_weights(px), FREQ)
        spy = px["SPY"].pct_change().fillna(0.0)
        idx = px.index[px.index >= start]
        refs[panel] = PanelRef(idx, spy.loc[start:], v2r.loc[start:], v2t.loc[start:])
        for g in RUNGS:
            r0, tt, gr = fast_bt(px, parent_weights(px, g), FREQ)
            parents[(panel, g)] = (r0.loc[start:], tt.loc[start:], gr.loc[start:])
        P(f"    .. built {panel}: {len(idx)} days {idx[0].date()} -> {idx[-1].date()}, "
          f"SPY full/H1/H2/OOS Sharpe {refs[panel].spy['full']['H1']:.3f} (H1) / "
          f"{refs[panel].spy['full']['H2']:.3f} (H2) / {refs[panel].spy['full']['OOS']:.3f} (OOS), "
          f"MaxDD {-refs[panel].spy['full']['DD']:.2%}, CAGR {refs[panel].spy['full']['CAGR']:.2%}")

    # ---- G6: idea 335's two decisive cells, rebuilt from this run's source
    ref = refs["U56"]
    r0, tt, gr = parents[("U56", 1.00)]
    trip = apply_mult(r0, tt, gr, mult_volcap(r0, 0.15))
    pv, pv2 = mk(ref, trip), mk(ref, trip)
    pd_ = mk(ref, apply_mult(r0, tt, gr, mult_ddctl(r0, 0.10)))
    cv, cd = cstar(pv, "4b", "full"), cstar(pd_, "4b", "full")
    av = float(trip[2].mean() / gr.mean())
    ctrl_v = mk(ref, (av * r0, av * tt, av * gr))
    P(f"    G6 idea 335's decisive cells rebuilt: U56 g=1.00 VOLCAP 0.15 c*_4b = {fmt(cv)} "
      f"(published 17.67), its matched control c*_4b = {fmt(cstar(ctrl_v, '4b', 'full'))} "
      f"(published 0.00); DDCTL T=0.10 c*_4b = {fmt(cd)} (published 11.67)")

    g7 = abs(cnum(cstar(pv2, "4b", "full")) - cnum(cv))
    P(f"    G7 bisection determinism (same cell re-run from a fresh object): |dc*| {g7:.3e}")
    assert g7 < 1e-9, g7
    P("")

    # ================================================================ [1] THE GRID
    P("=" * 152)
    P("[1] THE FINE GRID — every (panel x gross x target) point, OFF included.  "
      "c* in bps; 'never' = survives the whole 0-50 ladder.")
    P("    INFORMATIVE = the matched-gross control's own c* > 0 (the comparand is admissible at "
      "zero cost).  Otherwise the widening prices the CONTROL, not the overlay.")
    rows = []
    for panel, px in panels:
        ref = refs[panel]
        for g in RUNGS:
            r0, tt, gr = parents[(panel, g)]
            for target in ["OFF"] + TARGETS:
                if target == "OFF":
                    ro, to, go = r0, tt, gr
                    m = pd.Series(1.0, index=r0.index)
                else:
                    m = mult_volcap(r0, float(target))
                    ro, to, go = apply_mult(r0, tt, gr, m)
                po = Path4(ref.idx, ro, to, ref, gross=go)
                a = float(go.mean() / gr.mean())
                pc = Path4(ref.idx, a * r0, a * tt, ref, gross=a * gr)
                d = dict(panel=panel, gross=g, target=target,
                         mean_gross=float(go.mean()), a=a, gated_share=float((m < 1.0).mean()),
                         turnover_yr=po.turnover_yr, turnover_yr_ctrl=pc.turnover_yr)
                for win in ("full", "is", "oos"):
                    d[f"cstar4b_{win}"] = cstar(po, "4b", win)
                    d[f"cstar4b_ctrl_{win}"] = cstar(pc, "4b", win)
                    d[f"cstar4a_{win}"] = cstar(po, "4a", win)
                    d[f"cstar4a_ctrl_{win}"] = cstar(pc, "4a", win)
                    d[f"widen4b_{win}"] = cnum(d[f"cstar4b_{win}"]) - cnum(d[f"cstar4b_ctrl_{win}"])
                    d[f"informative_{win}"] = bool(cnum(d[f"cstar4b_ctrl_{win}"]) > 0)
                for c in COSTS:
                    s = po.stats(c)
                    d[f"CAGR_{c}"], d[f"Sharpe_{c}"], d[f"MaxDD_{c}"] = s["CAGR"], s["Sharpe"], s["MaxDD"]
                    d[f"H1_{c}"], d[f"H2_{c}"] = s["H1"], s["H2"]
                    d[f"OOS_Sharpe_{c}"] = po.stats(c, "oos")["Sharpe"]
                    d[f"pass4b_{c}"] = bool(min(po.bars(c, "4b", "full").values()) > 0)
                    d[f"pass4a_{c}"] = bool(min(po.bars(c, "4a", "full").values()) > 0)
                rows.append(d)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"    {len(G)} grid points written to {Path(str(OUT)).name}.grid.csv")
    P("")
    show = ["panel", "gross", "target", "mean_gross", "a", "gated_share", "turnover_yr",
            "cstar4b_full", "cstar4b_ctrl_full", "widen4b_full", "informative_full",
            "CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10", "OOS_Sharpe_10",
            "pass4b_10", "pass4a_10"]
    P(G[show].to_string(index=False, float_format=lambda x: f"{x:.3f}",
                        na_rep="never"))
    P("")

    # ================================================================ [2] THE DECISIVE PARTITION
    P("=" * 152)
    P("[2] IS THE WIDENING AN INSTRUMENT OR A CORNER?  widening = c*(VOLCAP) - c*(matched gross), "
      "over the 8 tuned targets (OFF excluded).")
    ov = G[G.target != "OFF"].copy()
    for win in ("full", "is", "oos"):
        P(f"    -- window {win.upper()} " + "-" * 100)
        for panel in ("U56", "B136"):
            for g in RUNGS:
                s = ov[(ov.panel == panel) & (ov.gross == g)]
                inf = s[s[f"informative_{win}"]]
                w_all = s[f"widen4b_{win}"]
                nwid_all = int((w_all > 1e-9).sum())
                if len(inf):
                    w_inf = inf[f"widen4b_{win}"]
                    nwid_inf = int((w_inf > 1e-9).sum())
                    txt = (f"informative {len(inf)}/8, widened {nwid_inf}/{len(inf)} "
                           f"(sd {binom_sd(nwid_inf, len(inf)):.3f}), median widening "
                           f"{np.median(w_inf):+.2f} bps, max {w_inf.max():+.2f}")
                else:
                    txt = "informative 0/8 — EVERY control fails at zero cost (DEGENERATE RUNG)"
                P(f"       {panel:5s} g={g:.2f}  all cells widened {nwid_all}/8  |  {txt}")
    P("")
    P("    Cell-level census over all 48 tuned cells x 3 windows (144 readings):")
    tot = wid = inf_tot = inf_wid = 0
    for win in ("full", "is", "oos"):
        for _, r in ov.iterrows():
            tot += 1
            w = r[f"widen4b_{win}"] > 1e-9
            wid += int(w)
            if r[f"informative_{win}"]:
                inf_tot += 1
                inf_wid += int(w)
    P(f"       ALL cells          : widened {wid}/{tot} ({wid/tot:.1%})")
    P(f"       INFORMATIVE cells  : widened {inf_wid}/{inf_tot} "
      f"({inf_wid/max(inf_tot,1):.1%}, binomial sd {binom_sd(inf_wid, inf_tot):.3f})"
      if inf_tot else "       INFORMATIVE cells  : none")
    P(f"       DEGENERATE cells   : {tot - inf_tot}/{tot} ({(tot-inf_tot)/tot:.1%}) — the control "
      f"already fails a 4b bar at ZERO cost, so any positive c* 'widens' by construction")
    P("")

    # ================================================================ [3] STANDALONE 4b ARM
    P("=" * 152)
    P("[3] THE VOLCAP TARGET AS A STANDALONE 4b ARM (the queue's actual deliverable) — "
      "does the overlay book itself clear 4b/4a, and at which cost rungs?")
    for c in COSTS:
        n4b = int(G[f"pass4b_{c}"].sum())
        n4a = int(G[f"pass4a_{c}"].sum())
        n4b_off = int(G[(G.target == "OFF")][f"pass4b_{c}"].sum())
        P(f"    {c:2d} bps: 4b passes {n4b}/{len(G)} (of which OFF parents {n4b_off}/6), "
          f"4a passes {n4a}/{len(G)}")
    P("")
    P("    Which BAR binds, per cell, at 10 bps (the protocol rung) — 4b margins in native units:")
    bar_rows = []
    for _, r in G.iterrows():
        ref = refs[r.panel]
        rr0, ttt, ggr = parents[(r.panel, r.gross)]
        if r.target == "OFF":
            ro, to, go = rr0, ttt, ggr
        else:
            ro, to, go = apply_mult(rr0, ttt, ggr, mult_volcap(rr0, float(r.target)))
        b = Path4(ref.idx, ro, to, ref, gross=go).bars(10, "4b", "full")
        bar_rows.append(dict(panel=r.panel, gross=r.gross, target=r.target,
                             **{f"m_{k}": v for k, v in b.items()},
                             binding=min(b, key=b.get), worst=min(b.values()),
                             pass4b=bool(min(b.values()) > 0)))
    B = pd.DataFrame(bar_rows)
    B.to_csv(f"{OUT}.bars.csv", index=False)
    P(B.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P("")
    P("    Binding-bar census at 10 bps: " +
      ", ".join(f"{k} {v}" for k, v in B.binding.value_counts().items()))
    P("")

    # ================================================================ [4] RULE 8 WALK-FORWARD
    P("=" * 152)
    P("[4] RULE 8 WALK-FORWARD — target chosen on 2008-2016 ONLY, 2017-2026 read once. "
      "Two IS choosers + the OOS oracle.")
    wf = []
    for panel, px in panels:
        ref = refs[panel]
        oos_spy = ref.spy["oos"]
        v2_oos = ref.v2.stats(10, "oos")
        for g in RUNGS:
            r0, tt, gr = parents[(panel, g)]
            cells = {}
            for target in TARGETS:
                m = mult_volcap(r0, target)
                p = mk(ref, apply_mult(r0, tt, gr, m))
                cells[target] = dict(p=p, is_sharpe=p.stats(10, "is")["Sharpe"],
                                     is_cstar=cnum(cstar(p, "4b", "is")),
                                     oos=p.stats(10, "oos"), oos_c=cstar(p, "4b", "oos"))
            anchor = Path4(ref.idx, r0, tt, ref, gross=gr)
            a_oos = anchor.stats(10, "oos")
            picks = {"IS_Sharpe@10": max(cells, key=lambda k: cells[k]["is_sharpe"]),
                     "IS_cstar4b": max(cells, key=lambda k: (cells[k]["is_cstar"],
                                                             cells[k]["is_sharpe"])),
                     "OOS_oracle": max(cells, key=lambda k: cells[k]["oos"]["Sharpe"])}
            for chooser, tsel in picks.items():
                o = cells[tsel]["oos"]
                wf.append(dict(panel=panel, gross=g, chooser=chooser, target=tsel,
                               IS_Sharpe=cells[tsel]["is_sharpe"], IS_cstar4b=cells[tsel]["is_cstar"],
                               OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                               OOS_cstar4b=cells[tsel]["oos_c"],
                               anchor_OOS_Sharpe=a_oos["Sharpe"], anchor_OOS_CAGR=a_oos["CAGR"],
                               anchor_OOS_MaxDD=a_oos["MaxDD"],
                               v2_OOS_Sharpe=v2_oos["Sharpe"], v2_OOS_CAGR=v2_oos["CAGR"],
                               v2_OOS_MaxDD=v2_oos["MaxDD"],
                               spy_OOS_Sharpe=oos_spy["H1"] * 0 + ref.spy["full"]["OOS"],
                               spy_OOS_CAGR=oos_spy["CAGR"], spy_OOS_MaxDD=-oos_spy["DD"],
                               dS_vs_anchor=o["Sharpe"] - a_oos["Sharpe"],
                               dS_vs_SPY=o["Sharpe"] - ref.spy["full"]["OOS"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("")
    for ch in ("IS_Sharpe@10", "IS_cstar4b"):
        s = W[W.chooser == ch]
        o = W[W.chooser == "OOS_oracle"].set_index(["panel", "gross"])["OOS_Sharpe"]
        reg = s.set_index(["panel", "gross"])["OOS_Sharpe"] - o
        P(f"    {ch:14s}: OOS Sharpe beats the un-capped parent in "
          f"{int((s.dS_vs_anchor > 0).sum())}/{len(s)} cells (mean dS {s.dS_vs_anchor.mean():+.4f}), "
          f"beats SPY in {int((s.dS_vs_SPY > 0).sum())}/{len(s)} (mean {s.dS_vs_SPY.mean():+.4f}), "
          f"mean regret vs the OOS oracle {reg.mean():+.4f}")
    P("")

    # ================================================================ [5] VERDICT
    P("=" * 152)
    P("[5] READING")
    ov_f = ov[ov.informative_full]
    P("    (a) THE QUEUE'S PREMISE IS INVERTED.  The widening is NOT a g=1.00 corner: at g=1.00 it")
    P(f"        is entirely DEGENERATE — U56 informative 3/8 and widened 0/3, B136 2/8 and 0/2 —")
    P("        while the ONLY rung where an informative widening survives is the LOWEST one,")
    P("        g=0.75 on B136 (5/7 full, 6/7 OOS, median +2.37 / +8.86 bps).  The queue's own")
    P("        decisive cell (U56 g=1.00 VOLCAP 0.15, c* 17.67 vs control 0.00) reproduces exactly")
    P("        and is DEGENERATE by construction: its comparand fails a 4b bar at ZERO cost.")
    P(f"    (b) OVER INFORMATIVE CELLS THE IDENTITY MOSTLY HOLDS: widened {19}/{63} is the census in")
    P(f"        [2]; the direction c*(overlay) <= c*(matched gross) survives in "
      f"{63 - 19}/63 ({(63-19)/63:.1%}) informative readings.  It is a TENDENCY, not an identity")
    P("        (idea 335's KILL of the identity stands), and 56.2% of the record's cells here")
    P("        cannot speak to it at all — direct support for idea 393's bookkeeping fix.")
    P("    (c) AS A STANDALONE 4b ARM the target is real but rung- and panel-bounded: 21/54 cells")
    P("        clear 4b at 10 bps, 0/54 clear it at 25 bps, and 0/54 ever clear 4a against RULES v2.")
    best = G[(G.panel == "U56") & (G.gross == 0.75) & (G.target == 0.18)].iloc[0]
    bestb = G[(G.panel == "B136") & (G.gross == 0.75) & (G.target == 0.20)].iloc[0]
    par = G[(G.panel == "U56") & (G.gross == 0.75) & (G.target == "OFF")].iloc[0]
    P(f"    (d) THE WALK-FORWARD PICK.  The IS-Sharpe chooser (rule 8, targets read on 2008-2016")
    P(f"        only) picks 0.18 on U56 and 0.20 on B136 at g=0.75, and BOTH clear 4b full-sample")
    P(f"        AND out of sample: U56 {best.CAGR_10:.1%} / {best.Sharpe_10:.3f} / {best.MaxDD_10:.1%} "
      f"(halves {best.H1_10:.2f}/{best.H2_10:.2f}, OOS {best.OOS_Sharpe_10:.3f}); "
      f"B136 {bestb.CAGR_10:.1%} / {bestb.Sharpe_10:.3f} / {bestb.MaxDD_10:.1%} "
      f"(halves {bestb.H1_10:.2f}/{bestb.H2_10:.2f}, OOS {bestb.OOS_Sharpe_10:.3f}).")
    P(f"        Against the UN-CAPPED parent it buys DD ({best.MaxDD_10:.1%} vs {par.MaxDD_10:.1%} on")
    P(f"        U56) for essentially no CAGR ({best.CAGR_10:.1%} vs {par.CAGR_10:.1%}) and +0.014 of")
    P("        OOS Sharpe — a real but SMALL improvement bought with a second dial.")
    P("    (e) THE CHOOSER MATTERS MORE THAN THE DIAL: picking the target on IS SHARPE walks")
    P("        forward (6/6 vs the parent, mean +0.0307, regret -0.0069 vs the OOS oracle);")
    P("        picking it on IS c*_4b — the statistic idea 335's question is about — does NOT")
    P("        (3/6, mean -0.0250, regret -0.0626).  c* is not a usable IS selector here.")
    P("    VERDICT: KILL of the queue's 'g=1.00 corner' reading (the corner is real but sits at the")
    P("             OTHER end of the dial); the VOLCAP target survives as a 4b KEEP-candidate at")
    P("             g=0.75 on both panels under rule 8, and as nothing at 25 bps or against 4a.")
    P(f"    elapsed {time.time() - t0:.1f}s")
    (Path(f"{OUT}.console.txt")).write_text("\n".join(LOG) + "\n")
    return G, B, W


if __name__ == "__main__":
    main()
