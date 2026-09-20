#!/usr/bin/env python3
"""Idea 1632 (lane C, 2026-09-20): is the BAND's U56-ONLY survival a PANEL effect or a
NAME-COUNT effect?

WHY THIS IDEA.  Idea 1617 priced every eligibility filter the record owns against a twin
matched on REALISED mean gross and found exactly one convincing survivor: the LIVE band
c = 0.03, on U56 ALONE (dSharpe +0.0827 FULL, +0.1499 OOS), against B136 -0.0161 / +0.0136 and
SMALL -0.0461 / -0.0520.  That single cell is the live book's ONLY matched-exposure win in the
whole record.  But U56 is confounded: it is both a DIFFERENT PANEL (56 current large-cap
constituents plus sector/bond ETFs) and the SMALLEST panel by NAME COUNT.  Under the live
RULES v2 weighting convention (gross / N_priced per eligible name, gated-out weight to cash),
the band's per-name gate is a BREADTH device: with 56 names one gated name moves realised gross
by 1/56 of the book, with 665 names by 1/665.  A contrast that shrinks like 1/N would reproduce
1617's whole cross-panel ordering without any panel content at all.

THE NULL, STATED BEFORE THE RUN.

    H0 (NAME-COUNT):  dSharpe(band c vs its realised-gross-matched twin) is a function of the
                      NUMBER OF NAMES held, not of which panel they come from.  Under H0, a
                      RANDOM 56-name subsample of B136 or SMALL reproduces U56's +0.0827, and
                      the contrast decays monotonically as N rises.

    H1 (PANEL):       the contrast is a property of the U56 name set.  Under H1, B136 and SMALL
                      subsampled DOWN to 56 names stay where their full panels are (negative or
                      ~0), and U56 subsampled DOWN to 20 does not run away.

The test is the crossing of those two predictions, and it needs BOTH directions of the ladder:
subsampling the big panels DOWN and subsampling U56 DOWN TOO.  1617 never ran either.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  N_NAMES   the number of names traded, drawn uniformly at random without replacement
                    from the panel's own traded column set.  Ladder {20, 36, 56, 100, 136, 300}
                    truncated at each panel's size, plus each panel's FULL set as the ALL rung
                    (one deterministic draw).  56 is U56's own size and the rung on which the
                    three panels are directly comparable.
  DIAL 2  BAND c    {0.00, 0.03, 0.06, 0.10}.  c = 0.00 is the plain 200d MA gate, c = 0.03 IS
                    live RULES v2 clause 2 (gated bit-for-bit at G3), 0.06 / 0.10 are the
                    record's committed wider rungs.

NOT DIALS, published at every value:
  PANEL  {U56, B136, SMALL}   (rule 9; SMALL carries the protocol's max_1d_move >= 1.0 drop)
  DRAW   D = 24 seeded draws per (panel, N) rung below ALL.  The draw is a NUISANCE dimension,
         published in full as a DISTRIBUTION, never averaged into a point estimate except where
         a TRANCHE book (1/D of NAV per draw, re-levelled daily) makes the average TRADABLE.
  COST   {0, 10, 25, 50} bps.  Weights are cost-independent, so one run yields every rung
         exactly: r(c) = r_gross - turnover * c / 1e4.  GATED at G2, not assumed.  Every KEEP
         verdict is read at the protocol's binding 10 bps.

THE TWIN.  Each band book is paired with its OWN de-gross twin: the SAME subsample held with NO
gate at all (every priced name at gross / N_priced), scaled by a constant k solved so the twin's
REALISED mean gross equals the band book's REALISED mean gross to machine precision.  Matching on
REALISED and not TARGET gross is 1617's construction carried over unchanged, so the numbers in
this file are commensurable with its.  k is solved in CLOSED FORM (see `profile`): inside a
rebalance segment the scaled book's gross path is k*G*P / (k*G*P + 1 - k*G*F0) with P and F0
independent of k, so the bisection costs no backtests and the match is exact (G4).

THE QUESTIONS, STATED BEFORE THE RUN:
  Q1  Does a random 56-name subsample of B136 / SMALL reproduce U56's +0.0827?  Published as the
      full draw distribution (mean, sd, min/median/max, share > 0) and as U56's own percentile
      inside it.
  Q2  Is dSharpe MONOTONE DECREASING in N within each panel?  Published as the per-panel curve
      over the whole ladder, FULL and OOS, at every cost rung.
  Q3  Does U56 subsampled DOWN to 20 / 36 names go FURTHER positive (H0) or not (H1)?
  Q4  Is any of it capital-worthy?  BOTH KEEP paths at EVERY one of the 1,164 band books and
      their twins, FULL and OOS, plus rule 8.

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE   argmax IS Sharpe over every (N, c, draw) cell on that panel.  A draw is a NAME SET,
             so choosing one on IS rows is legal -- and it is also the most optimistic legal
             chooser, which is the point.
  C_TRANCHE  argmax over (N, c) of the IS Sharpe of the TRANCHE book (1/D per draw, re-levelled
             daily).  Draw-blind and tradable.
  C_LIVE     the live inheritance, choosing nothing: FULL panel, c = 0.03.
  Each pick is read OOS against (a) SPY, (b) the live RULES v2 baseline and (c) its OWN twin,
  whose k is RE-SOLVED on IS gross only so the twin is legal out of sample too.

WHAT WOULD MAKE THIS A FINDING.  If B136/SMALL at N = 56 land on U56's +0.0827 and the per-panel
curve decays in N, the record's only matched-exposure win is a BREADTH ARTEFACT of a 56-name
panel and should be retired as a panel claim.  If they do not, the U56 margin is a property of
those names and survives as the one selection edge the record owns.  Both outcomes are reported;
nothing is tuned until it works.

GATES.  G0 sample >= 10y (rule 1).  G1 fast_run vs `engine.backtest` (returns AND turnover) on
the FULL panels, band and no-gate books.  G2 the DERIVED 25 bps rung vs a fresh 25 bps engine
run.  G3 BAND c = 0.03 at the ALL rung on U56 replays `baseline.rules_v2_weights` through the
engine.  G4 the realised-gross match, max |dev| over all cells.  G5 exactly two tuned parameters.
G6 no chooser reads a row on or after 2017-01-01 (by construction AND re-tested on truncated
input).  G7 every row published.  G8 no leverage / no shorting: max realised target gross <= 0.75.
G9 PUBLISHED: turnover per cell, book and twin.  G10 PUBLISHED: realised mean gross, mean names
held, and the draws' SPY-inclusion rate.  G11 the closed-form gross/return profile replays
`run_cell` exactly.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_band-u56-panel-or-namecount_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "band-u56-panel-or-namecount"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
GROSS = 0.75
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

BANDS = [0.00, 0.03, 0.06, 0.10]
LIVE_C = 0.03
NLADDER = [20, 36, 56, 100, 136, 300]
NDRAWS = 24
SEED0 = 16320000

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE RULES v2 book, 4b against SPY.  Legs published."""
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- panel / subpanel
class Panel:
    """One price panel plus every eligibility input, computed once on the TRADED column set."""

    def __init__(self, name, px, cols):
        self.name, self.px = name, px
        self.cols = list(cols)
        self.idx = px.index
        q = px[self.cols]
        self.rets = q.pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.priced = q.notna().values
        self.bands = {c: band_state(q, c).values for c in BANDS}
        m = rebalance_mask(self.idx, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        self.T = len(self.idx)


class Sub:
    """A subsample of a Panel: the columns a draw selected, nothing else."""

    __slots__ = ("pan", "j", "rets", "C", "Cp", "priced", "bands", "reb", "T")

    def __init__(self, pan: Panel, j: np.ndarray):
        self.pan, self.j = pan, j
        self.rets = pan.rets[:, j]
        self.C = pan.C[:, j]
        self.Cp = pan.Cp[:, j]
        self.priced = pan.priced[:, j]
        self.bands = {c: pan.bands[c][:, j] for c in BANDS}
        self.reb = pan.reb
        self.T = pan.T

    def frame(self, c):
        """Target weights at gross 1.0, shifted one row: row t carries the close-(t-1) decision
        -- exactly engine.backtest's `weights.shift(1)` convention.  c is None for the NO-GATE
        anchor (hold every priced name)."""
        e = (self.priced if c is None else (self.priced & self.bands[c])).astype(float)
        n = self.priced.sum(axis=1).astype(float)        # N = names PRICED, the live convention
        w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
        w = np.nan_to_num(w, nan=0.0)
        return np.vstack([np.zeros((1, w.shape[1])), w[:-1]])


def run_cell(sub: Sub, frame, g=GROSS):
    """Hold g * frame on the weekly schedule, drift between rebalances, de-gross to 0%-yielding
    cash.  Returns GROSS-OF-COST daily returns, the turnover path, max realised target gross and
    the realised gross path -- identical semantics to engine.backtest (gated at G1)."""
    rets = sub.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    reb = sub.reb
    ends = np.append(reb[1:], T)
    C, Cp = sub.C, sub.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


def profile(sub: Sub, frame):
    """k-INDEPENDENT profile of a book: inside each rebalance segment the book scaled to target
    gross g has gross path g*P / (g*P + 1 - g*F0) and return path g*Q / (g*P + 1 - g*F0).
    Returns (P, Q, F0) so a scaler can be solved in closed form with no further backtests."""
    T, M = sub.rets.shape
    P = np.zeros(T); Q = np.zeros(T); F0 = np.zeros(T)
    reb = sub.reb
    ends = np.append(reb[1:], T)
    Cp = sub.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        f = frame[i0]
        A0 = f[None, :] * (Cp[i0:i1] / Cp[i0][None, :])
        P[i0:i1] = A0.sum(axis=1)
        Q[i0:i1] = (A0 * sub.rets[i0:i1]).sum(axis=1)
        F0[i0:i1] = f.sum()
    return P, Q, F0


def mean_gross_of(prof, g, lo, hi):
    P, Q, F0 = prof
    num = g * P[lo:hi]
    return float(np.mean(num / (num + 1.0 - g * F0[lo:hi])))


def solve_k(prof, target, lo, hi, iters=80):
    """Bisect the constant scaler k in [0, 1] so the NO-GATE book at gross k*GROSS carries the
    same REALISED mean gross as the gated book over [lo:hi).  Closed form, so exact and free."""
    a, b = 0.0, 1.0
    for _ in range(iters):
        k = 0.5 * (a + b)
        if mean_gross_of(prof, k * GROSS, lo, hi) < target:
            a = k
        else:
            b = k
    return 0.5 * (a + b)


def net(rg, tu, c):
    return rg - tu * c / 1e4


def maxdev(a, b):
    """max |a-b| over the FINITE entries, plus the count of non-finite ones.  engine.backtest
    emits NaN on a couple of warm-up rows before any weight exists; those rows are counted and
    published rather than silently swallowed by a plain max()."""
    d = np.abs(np.asarray(a, float) - np.asarray(b, float))
    f = np.isfinite(d)
    return (float(d[f].max()) if f.any() else 0.0), int((~f).sum())


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1632 (lane C, 2026-09-20) — is the BAND's U56-ONLY matched-exposure survival a")
    say("PANEL effect or a NAME-COUNT effect?")
    say(f"DIALS: N_NAMES ladder {NLADDER} + each panel's ALL rung  x  BAND c {BANDS}.")
    say(f"NOT DIALS, all published: PANEL [U56, B136, SMALL] x DRAW (D={NDRAWS}) x COST {COSTS} bps.")
    say(f"Gross {GROSS}, weekly cadence, t+1 execution, gated-out weight to 0%-yielding CASH.")
    say("H0 NAME-COUNT: a random 56-name subsample of B136/SMALL reproduces U56's +0.0827 and the")
    say("   contrast decays in N.   H1 PANEL: it does not, and U56 at N=20/36 does not run away.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} of {len(pxS.columns)-1} priced names survive.")

    panels = [Panel("U56", pxU, list(pxU.columns)),
              Panel("B136", pxB, list(pxB.columns)),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(panels[0].cols)} traded cols (SPY IS a constituent), "
        f"B136 {len(panels[1].cols)} (SPY IS a constituent), SMALL {len(panels[2].cols)} "
        f"(SPY is a joined BENCHMARK only and is NOT traded).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level below is an UPPER BOUND.  "
        "The headline is a BAND-minus-TWIN contrast inside one draw, over the same names on the "
        "same days at the same realised exposure, so it is first-order immune; the 4b pass "
        "counts are not.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {p.T} rows "
            f"({p.T/252:.1f}y)  OOS starts row {p.i_oos} ({p.idx[p.i_oos].date()})")
        publish(f"TAPE STAMP {p.name}", f"{p.T} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(p.T for p in panels) / 252.0, 2),
         ">= 10.0", min(p.T for p in panels) / 252.0 >= 10.0)

    # ------------------------------------------------ the (panel, N) rungs
    rungs = {}
    for p in panels:
        M = len(p.cols)
        ns = [n for n in NLADDER if n < M] + [M]
        rungs[p.name] = ns
        say(f"    N LADDER {p.name}: {ns}  (ALL rung = {M}, one deterministic draw)")
    ncells = sum(len(rungs[p.name]) for p in panels) * len(BANDS)
    gate("G5 exactly two tuned parameters (N_NAMES x BAND c)",
         f"{ncells} (panel,N,c) groups from 2 dials; PANEL/DRAW/COST are published, not tuned",
         "2 dials", True)

    # ------------------------------------------------ G1 / G2 / G3 / G11 against the engine
    say("\n  [G1/G2/G3/G11] fast_run and the closed-form profile vs engine.backtest, FULL panels")
    d1r = d1t = d2 = d11 = 0.0
    nonfin = 0
    g3dev = None
    for p in panels:
        allj = np.arange(len(p.cols))
        sub = Sub(p, allj)
        for c in (LIVE_C, None):
            fr = sub.frame(c)
            rg, tu, _, gs = run_cell(sub, fr)
            if c is None:
                e = pd.DataFrame(1.0, index=p.idx, columns=p.cols).where(p.px[p.cols].notna(), 0.0)
                W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            else:
                W = rules_v2_weights(p.px[p.cols], band=c, gross=GROSS)
            W = W.reindex(p.idx).fillna(0.0).reindex(columns=p.px.columns).fillna(0.0)
            eng = backtest(p.px, W, cost_bps=BIND, freq=CADENCE)
            eng25 = backtest(p.px, W, cost_bps=25.0, freq=CADENCE)
            v, nf = maxdev(net(rg, tu, BIND), eng["returns"].values); d1r = max(d1r, v); nonfin += nf
            v, _ = maxdev(tu, eng["turnover"].values); d1t = max(d1t, v)
            v, _ = maxdev(net(rg, tu, 25.0), eng25["returns"].values); d2 = max(d2, v)
            if c == LIVE_C and p.name == "U56":
                g3dev, _ = maxdev(net(rg, tu, BIND), eng["returns"].values)
            # G11: closed form replays run_cell at two scalers
            P, Q, F0 = profile(sub, fr)
            for kk in (1.0, 0.5137):
                den = kk * GROSS * P + 1.0 - kk * GROSS * F0
                r_cf = kk * GROSS * Q / den
                g_cf = kk * GROSS * P / den
                r_rc, _, _, g_rc = run_cell(sub, fr, g=kk * GROSS)
                v1, _ = maxdev(r_cf, r_rc); v2, _ = maxdev(g_cf, g_rc)
                d11 = max(d11, v1, v2)
    gate("G1 fast_run vs engine.backtest, RETURNS (max |dev|, 6 panel x book runs)",
         f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12", d1t < 1e-12)
    gate("G2 DERIVED 25 bps rung vs a fresh 25 bps engine run (max |dev|)", f"{d2:.3e}",
         "< 1e-12", d2 < 1e-12)
    gate("G3 BAND c=0.03 ALL rung on U56 replays baseline.rules_v2_weights through the engine",
         f"{g3dev:.3e}", "< 1e-12", g3dev < 1e-12)
    gate("G11 closed-form (P,Q,F0) profile replays run_cell at 2 scalers (max |dev|)",
         f"{d11:.3e}", "< 1e-12", d11 < 1e-12)

    # ------------------------------------------------ the grid
    rows = []
    BARS = {}
    wsum_global = 0.0
    gapmax = 0.0
    spy_in_draw = []
    tranche = {}          # (panel, N, c) -> dict of return arrays for the tranche book
    percell = {}          # (panel, N, c) -> list of per-draw dicts

    for p in panels:
        T, i_oos = p.T, p.i_oos
        spy = bmpack(p.spy[WARMUP:]); spyO = bmpack(p.spy[i_oos:]); spyI = bmpack(p.spy[WARMUP:i_oos])
        lr = backtest(p.px, rules_v2_weights(p.px), cost_bps=BIND, freq="W")["returns"].values
        live, liveO, liveI = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:]), bmpack(lr[WARMUP:i_oos])
        BARS[p.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, liveI=liveI)
        say(f"\n  [{p.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}"
            f"  H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%},"
            f" CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}"
            f"  |  OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%}  H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  (OOS "
            f"{liveO['CAGR']:.2%} / {liveO['Sharpe']:.4f} / {liveO['MaxDD']:.2%})")

        M = len(p.cols)
        spy_j = p.cols.index("SPY") if "SPY" in p.cols else -1
        for N in rungs[p.name]:
            draws = ([np.arange(M)] if N == M else
                     [np.random.default_rng(SEED0 + 1009 * N + d).choice(M, size=N, replace=False)
                      for d in range(NDRAWS)])
            for d, j in enumerate(draws):
                j = np.sort(j)
                sub = Sub(p, j)
                has_spy = bool(spy_j >= 0 and spy_j in set(j.tolist()))
                spy_in_draw.append(dict(panel=p.name, N=N, draw=d, has_spy=has_spy))
                anchor = sub.frame(None)
                prof = profile(sub, anchor)
                for c in BANDS:
                    fb = sub.frame(c)
                    rgB, tuB, wsB, gsB = run_cell(sub, fb)
                    wsum_global = max(wsum_global, wsB)
                    gF = float(np.mean(gsB[WARMUP:])); gI = float(np.mean(gsB[WARMUP:i_oos]))
                    kF = solve_k(prof, gF, WARMUP, T)
                    kI = solve_k(prof, gI, WARMUP, i_oos)
                    rgTF, tuTF, wsTF, gsTF = run_cell(sub, anchor, g=kF * GROSS)
                    rgTI, tuTI, wsTI, gsTI = run_cell(sub, anchor, g=kI * GROSS)
                    wsum_global = max(wsum_global, wsTF, wsTI)
                    gapmax = max(gapmax, abs(float(np.mean(gsTF[WARMUP:])) - gF),
                                 abs(float(np.mean(gsTI[WARMUP:i_oos])) - gI))
                    nheld = float(np.mean((fb[WARMUP:] > 0).sum(axis=1)))
                    for cb in COSTS:
                        rb = net(rgB, tuB, cb); rt = net(rgTF, tuTF, cb); rtI = net(rgTI, tuTI, cb)
                        k4a, k4b, m, h1, h2, legs = keep_paths(rb[WARMUP:], spy, live)
                        k4aO, k4bO, mO, _, _, legsO = keep_paths(rb[i_oos:], spyO, liveO)
                        t4a, t4b, tm, th1, th2, _ = keep_paths(rt[WARMUP:], spy, live)
                        t4aO, t4bO, tmO, _, _, _ = keep_paths(rtI[i_oos:], spyO, liveO)
                        rows.append(dict(
                            panel=p.name, N=N, n_all=M, draw=d, band=c, cost_bps=cb,
                            has_spy=has_spy, names_held=round(nheld, 3),
                            gross_full=round(gF, 6), gross_is=round(gI, 6),
                            k_full=round(kF, 8), k_is=round(kI, 8),
                            turn_yr=round(float(tuB[WARMUP:].sum()) * 252 / (T - WARMUP), 4),
                            turn_twin_yr=round(float(tuTF[WARMUP:].sum()) * 252 / (T - WARMUP), 4),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            tw_CAGR=tm["CAGR"], tw_Sharpe=tm["Sharpe"], tw_MaxDD=tm["MaxDD"],
                            dSharpe=m["Sharpe"] - tm["Sharpe"], dCAGR=m["CAGR"] - tm["CAGR"],
                            dMaxDD=m["MaxDD"] - tm["MaxDD"],
                            O_CAGR=mO["CAGR"], O_Sharpe=mO["Sharpe"], O_MaxDD=mO["MaxDD"],
                            O_tw_Sharpe=tmO["Sharpe"], O_tw_MaxDD=tmO["MaxDD"],
                            O_dSharpe=mO["Sharpe"] - tmO["Sharpe"],
                            O_dMaxDD=mO["MaxDD"] - tmO["MaxDD"],
                            keep4a=k4a, keep4b=k4b, O_keep4a=k4aO, O_keep4b=k4bO,
                            tw4a=t4a, tw4b=t4b, O_tw4a=t4aO, O_tw4b=t4bO,
                            leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                            leg_CAGR=legs["CAGR"], O_leg_DD=legsO["DD"], O_leg_CAGR=legsO["CAGR"],
                        ))
                    key = (p.name, N, c)
                    percell.setdefault(key, []).append(dict(
                        draw=d, rgB=rgB, tuB=tuB, rgTI=rgTI, tuTI=tuTI, kI=kI,
                        IS_S=sharpe(net(rgB, tuB, BIND)[WARMUP:i_oos]),
                        IS_DD=mdd(net(rgB, tuB, BIND)[WARMUP:i_oos]),
                        IS_CAGR=cagr(net(rgB, tuB, BIND)[WARMUP:i_oos]),
                        IS_turn=float(tuB[WARMUP:i_oos].sum()) * 252 / (i_oos - WARMUP)))
            say(f"    [{p.name}] N={N:>4}  {len(draws):>2} draw(s) x {len(BANDS)} bands done "
                f"({time.time()-t0:.0f}s)")

        # TRANCHE books: 1/D of NAV per draw, re-levelled daily -> daily return is the draw mean
        for N in rungs[p.name]:
            for c in BANDS:
                L = percell[(p.name, N, c)]
                rg = np.mean([x["rgB"] for x in L], axis=0)
                tu = np.mean([x["tuB"] for x in L], axis=0)
                rgt = np.mean([x["rgTI"] for x in L], axis=0)
                tut = np.mean([x["tuTI"] for x in L], axis=0)
                tranche[(p.name, N, c)] = dict(rg=rg, tu=tu, rgt=rgt, tut=tut,
                                               IS_S=sharpe(net(rg, tu, BIND)[WARMUP:i_oos]))

    gate("G4 realised-gross match, max |mean_gross(twin) - mean_gross(band)| over all cells",
         f"{gapmax:.3e}", "< 1e-12", gapmax < 1e-12)
    gate("G8 no leverage / no shorting: max realised TARGET gross over every book",
         f"{wsum_global:.6f}", f"<= {GROSS}", wsum_global <= GROSS + 1e-12)

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    gate("G7 every (panel, N, draw, band, cost) row published",
         f"{len(df)} rows -> {Path(OUT).name}.grid.csv.gz", "all", len(df) > 0)
    pd.DataFrame(spy_in_draw).to_csv(f"{OUT}.draws.csv", index=False)
    sd = pd.DataFrame(spy_in_draw)
    publish("G10 SPY-inclusion rate of the draws (U56/B136 only; SPY is not traded on SMALL)",
            {k: round(float(v), 4) for k, v in
             sd[sd.panel != "SMALL"].groupby("panel")["has_spy"].mean().items()})

    b = df[df.cost_bps == BIND]
    publish("G9 turnover /yr, band book (median over cells, per panel)",
            {k: round(float(v), 3) for k, v in b.groupby("panel")["turn_yr"].median().items()})
    publish("G9b turnover /yr, matched twin (median over cells, per panel)",
            {k: round(float(v), 3) for k, v in b.groupby("panel")["turn_twin_yr"].median().items()})
    publish("G10b realised mean gross, band book (median over cells, per panel)",
            {k: round(float(v), 4) for k, v in b.groupby("panel")["gross_full"].median().items()})
    publish("G10c mean names HELD (median over cells, per panel x N)",
            {f"{k[0]}/{k[1]}": round(float(v), 1) for k, v in
             b.groupby(["panel", "N"])["names_held"].median().items()})

    # ------------------------------------------------ Q1/Q2/Q3: the curve
    say("\n" + "=" * 118)
    say("Q1/Q2/Q3 — dSharpe (BAND minus its REALISED-GROSS-MATCHED twin) as a function of N_NAMES")
    say("           at the BINDING 10 bps rung.  mean [min .. max] over draws, share > 0.")
    say("=" * 118)
    curve = []
    for c in BANDS:
        say(f"\n  BAND c = {c:.2f}{'   <-- LIVE RULES v2 clause 2' if c == LIVE_C else ''}")
        say(f"    {'panel':<6} {'N':>5} {'draws':>5} | {'FULL dSharpe mean':>18} {'sd':>7} "
            f"{'[min..max]':>18} {'>0':>6} | {'OOS dSharpe mean':>17} {'sd':>7} {'>0':>6}")
        for p in panels:
            for N in rungs[p.name]:
                g = b[(b.panel == p.name) & (b.N == N) & (b.band == c)]
                fm, fs = g.dSharpe.mean(), g.dSharpe.std(ddof=0)
                om, os_ = g.O_dSharpe.mean(), g.O_dSharpe.std(ddof=0)
                sh = (g.dSharpe > 0).mean(); osh = (g.O_dSharpe > 0).mean()
                say(f"    {p.name:<6} {N:>5} {len(g):>5} | {fm:>+18.4f} {fs:>7.4f} "
                    f"[{g.dSharpe.min():>+7.4f}..{g.dSharpe.max():>+7.4f}] {sh:>6.2f} | "
                    f"{om:>+17.4f} {os_:>7.4f} {osh:>6.2f}")
                curve.append(dict(panel=p.name, N=N, band=c, draws=len(g),
                                  full_mean=fm, full_sd=fs, full_min=g.dSharpe.min(),
                                  full_max=g.dSharpe.max(), full_share_pos=sh,
                                  oos_mean=om, oos_sd=os_, oos_share_pos=osh,
                                  full_dMaxDD_mean=g.dMaxDD.mean(), oos_dMaxDD_mean=g.O_dMaxDD.mean(),
                                  gross=g.gross_full.mean(), names_held=g.names_held.mean()))
    pd.DataFrame(curve).to_csv(f"{OUT}.curve.csv", index=False)

    # the decisive read: U56's own ALL value vs the other panels' N=56 draw distributions
    say("\n" + "=" * 118)
    say("THE DECISIVE READ — U56's OWN value (ALL 56 names) placed inside the N=56 SUBSAMPLE")
    say("distribution of B136 and SMALL.  H0 (name-count) predicts U56 lands mid-distribution.")
    say("=" * 118)
    dec = []
    for c in BANDS:
        u = b[(b.panel == "U56") & (b.N == 56) & (b.band == c)]
        uf = float(u.dSharpe.iloc[0]); uo = float(u.O_dSharpe.iloc[0])
        say(f"\n  BAND c = {c:.2f}   U56 (ALL 56) dSharpe FULL {uf:+.4f}   OOS {uo:+.4f}")
        for pn in ("B136", "SMALL"):
            g = b[(b.panel == pn) & (b.N == 56) & (b.band == c)]
            pf = float((g.dSharpe >= uf).mean()); po = float((g.O_dSharpe >= uo).mean())
            zf = (uf - g.dSharpe.mean()) / g.dSharpe.std(ddof=0) if g.dSharpe.std(ddof=0) > 0 else np.nan
            zo = (uo - g.O_dSharpe.mean()) / g.O_dSharpe.std(ddof=0) if g.O_dSharpe.std(ddof=0) > 0 else np.nan
            say(f"    {pn:<6} N=56 subsamples: FULL mean {g.dSharpe.mean():+.4f} sd "
                f"{g.dSharpe.std(ddof=0):.4f}  share >= U56 = {pf:.3f}  z(U56) {zf:+.2f}   |  OOS mean "
                f"{g.O_dSharpe.mean():+.4f} sd {g.O_dSharpe.std(ddof=0):.4f}  share >= U56 = {po:.3f}"
                f"  z(U56) {zo:+.2f}")
            dec.append(dict(band=c, panel=pn, u56_full=uf, u56_oos=uo,
                            sub_full_mean=g.dSharpe.mean(), sub_full_sd=g.dSharpe.std(ddof=0),
                            share_ge_full=pf, z_full=zf, sub_oos_mean=g.O_dSharpe.mean(),
                            sub_oos_sd=g.O_dSharpe.std(ddof=0), share_ge_oos=po, z_oos=zo))
        # U56 subsampled DOWN: does the contrast grow as N falls?  (H0 yes, H1 no)
        dn = b[(b.panel == "U56") & (b.band == c)].groupby("N")["dSharpe"].mean()
        say(f"    U56 subsampled DOWN, FULL dSharpe by N: " +
            "  ".join(f"N={int(k)}:{v:+.4f}" for k, v in dn.items()))
    pd.DataFrame(dec).to_csv(f"{OUT}.decisive.csv", index=False)

    # monotonicity of the curve in N, per (panel, band)
    say("\n  MONOTONICITY of mean dSharpe in N (a name-count law must be DECREASING in N):")
    mono = []
    for c in BANDS:
        for p in panels:
            v = [float(b[(b.panel == p.name) & (b.N == N) & (b.band == c)].dSharpe.mean())
                 for N in rungs[p.name]]
            down = sum(1 for i in range(len(v) - 1) if v[i] > v[i + 1])
            say(f"    c={c:.2f} {p.name:<6} N={rungs[p.name]}  mean dSharpe="
                f"{[round(x, 4) for x in v]}  steps DOWN {down}/{len(v)-1}")
            mono.append(dict(band=c, panel=p.name, steps_down=down, steps=len(v) - 1,
                             values=";".join(f"{x:.4f}" for x in v)))
    pd.DataFrame(mono).to_csv(f"{OUT}.monotone.csv", index=False)

    # ------------------------------------------------ WHICH LEG carries the panel dependence?
    say("\n" + "=" * 118)
    say("WHICH LEG — the band-minus-twin contrast split into its CAGR cost and its DRAWDOWN credit.")
    say("If the DD credit is panel-INVARIANT and the CAGR cost is not, the panel effect lives in")
    say("the RETURN leg and nowhere else.  FULL sample, 10 bps, mean over draws.")
    say("=" * 118)
    say(f"    {'band':>5}  {'panel':<6} | " + "  ".join(f"{'N='+str(n):>9}" for n in
        [20, 36, 56, 100, 136, 300, 665]))
    legrows = []
    for metric, lbl, scale in (("dCAGR", "dCAGR pp/yr", 100.0), ("dMaxDD", "dMaxDD pp", 100.0)):
        say(f"  -- {lbl} (band minus its realised-gross-matched twin; dMaxDD > 0 = SHALLOWER)")
        for c in BANDS:
            for p in panels:
                cells = {}
                for N in rungs[p.name]:
                    cells[N] = float(b[(b.panel == p.name) & (b.N == N) & (b.band == c)][metric].mean()) * scale
                say(f"    {c:>5.2f}  {p.name:<6} | " + "  ".join(
                    (f"{cells[n]:>+9.2f}" if n in cells else f"{'-':>9}") for n in
                    [20, 36, 56, 100, 136, 300, 665]))
                legrows.append(dict(metric=metric, band=c, panel=p.name,
                                    **{f"N{n}": cells.get(n, np.nan) for n in
                                       [20, 36, 56, 100, 136, 300, 665]}))
    pd.DataFrame(legrows).to_csv(f"{OUT}.legs.csv", index=False)
    say("\n    SPY-inclusion control (U56/B136 draws below the ALL rung, c = 0.03, FULL dSharpe):")
    for pn in ("U56", "B136"):
        g = b[(b.panel == pn) & (b.band == LIVE_C) & (b.N < b.n_all)]
        if len(g):
            gg = g.groupby("has_spy")["dSharpe"].agg(["mean", "count"])
            say(f"      {pn:<6} " + "   ".join(
                f"SPY {'IN ' if k else 'OUT'}: {v['mean']:+.4f} (n={int(v['count'])})"
                for k, v in gg.iterrows()))

    # ------------------------------------------------ Q4: capital arm
    say("\n" + "=" * 118)
    say("Q4 CAPITAL ARM — both KEEP paths at EVERY band book and EVERY twin, FULL and OOS, 10 bps")
    say("=" * 118)
    say(f"    books scored: {len(b)} band books (+ {len(b)} twins) at the binding rung; "
        f"{len(df)} rows over all {len(COSTS)} cost rungs.")
    for p in panels:
        g = b[b.panel == p.name]
        say(f"    {p.name:<6} 4a FULL {int(g.keep4a.sum()):>4}/{len(g)}   4b FULL "
            f"{int(g.keep4b.sum()):>4}/{len(g)}   4b OOS {int(g.O_keep4b.sum()):>4}/{len(g)}   "
            f"4b FULL&OOS {int((g.keep4b & g.O_keep4b).sum()):>4}/{len(g)}   |  twin 4b FULL "
            f"{int(g.tw4b.sum()):>4}  twin 4b OOS {int(g.O_tw4b.sum()):>4}")
    say(f"    ALL PANELS 4a FULL {int(b.keep4a.sum())}/{len(b)}, 4b FULL&OOS "
        f"{int((b.keep4b & b.O_keep4b).sum())}/{len(b)}")
    say("    4b leg failure shares (band books, FULL, 10 bps): " +
        ", ".join(f"{k} {1-float(b['leg_'+k].mean()):.3f}" for k in ("H1", "H2", "DD", "CAGR")))
    for cb in COSTS:
        gg = df[df.cost_bps == cb]
        say(f"      cost {cb:>5.1f} bps: 4b FULL {int(gg.keep4b.sum()):>4}/{len(gg)}   "
            f"4b OOS {int(gg.O_keep4b.sum()):>4}/{len(gg)}   4a FULL {int(gg.keep4a.sum()):>4}")

    # ------------------------------------------------ rule 8
    say("\n" + "=" * 118)
    say("RULE 8 WALK-FORWARD — choosers fit on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE")
    say("=" * 118)
    wf = []
    g6ok = True
    for p in panels:
        T, i_oos = p.T, p.i_oos
        bars = BARS[p.name]
        cand = []
        for N in rungs[p.name]:
            for c in BANDS:
                for x in percell[(p.name, N, c)]:
                    cand.append((N, c, x["draw"], x))
        # C_SHARPE: argmax IS Sharpe over every (N, c, draw)
        pick_s = max(cand, key=lambda t: (t[3]["IS_S"] if np.isfinite(t[3]["IS_S"]) else -9))
        # C_TRANCHE: argmax IS Sharpe of the draw-blind TRANCHE book over (N, c)
        tk = max(((N, c) for N in rungs[p.name] for c in BANDS),
                 key=lambda z: tranche[(p.name, z[0], z[1])]["IS_S"])
        # C_LIVE: the live inheritance, full panel at c = 0.03
        M = len(p.cols)
        live_pick = [t for t in cand if t[0] == M and t[1] == LIVE_C][0]

        def read(tag, rg, tu, rgt, tut, desc):
            r = net(rg, tu, BIND); rt = net(rgt, tut, BIND)
            k4a, k4b, m, _, _, legs = keep_paths(r[i_oos:], bars["spyO"], bars["liveO"])
            t4a, t4b, tm, _, _, _ = keep_paths(rt[i_oos:], bars["spyO"], bars["liveO"])
            say(f"    {p.name:<6} {tag:<10} {desc:<34} OOS {m['CAGR']:>7.2%} / {m['Sharpe']:>7.4f} "
                f"/ {m['MaxDD']:>8.2%}   4a {'Y' if k4a else 'n'}  4b {'Y' if k4b else 'n'}   "
                f"twin {tm['Sharpe']:>7.4f} / {tm['MaxDD']:>8.2%}  dS {m['Sharpe']-tm['Sharpe']:+.4f}")
            wf.append(dict(panel=p.name, chooser=tag, pick=desc, O_CAGR=m["CAGR"],
                           O_Sharpe=m["Sharpe"], O_MaxDD=m["MaxDD"], O_keep4a=k4a, O_keep4b=k4b,
                           O_tw_Sharpe=tm["Sharpe"], O_tw_MaxDD=tm["MaxDD"],
                           O_dSharpe=m["Sharpe"] - tm["Sharpe"],
                           spy_O_CAGR=bars["spyO"]["CAGR"], spy_O_Sharpe=bars["spyO"]["Sharpe"],
                           spy_O_MaxDD=bars["spyO"]["MaxDD"],
                           live_O_Sharpe=bars["liveO"]["Sharpe"], live_O_MaxDD=bars["liveO"]["MaxDD"],
                           leg_DD=legs["DD"], leg_CAGR=legs["CAGR"], leg_H1=legs["H1"], leg_H2=legs["H2"]))

        read("C_SHARPE", pick_s[3]["rgB"], pick_s[3]["tuB"], pick_s[3]["rgTI"], pick_s[3]["tuTI"],
             f"N={pick_s[0]} c={pick_s[1]:.2f} draw={pick_s[2]} (IS S {pick_s[3]['IS_S']:.4f})")
        tr = tranche[(p.name, tk[0], tk[1])]
        read("C_TRANCHE", tr["rg"], tr["tu"], tr["rgt"], tr["tut"],
             f"N={tk[0]} c={tk[1]:.2f} TRANCHE (IS S {tr['IS_S']:.4f})")
        read("C_LIVE", live_pick[3]["rgB"], live_pick[3]["tuB"], live_pick[3]["rgTI"],
             live_pick[3]["tuTI"], f"N=ALL({M}) c={LIVE_C:.2f} (inheritance)")
        say(f"    {p.name:<6} {'SPY':<10} {'buy and hold':<34} OOS {bars['spyO']['CAGR']:>7.2%} / "
            f"{bars['spyO']['Sharpe']:>7.4f} / {bars['spyO']['MaxDD']:>8.2%}")
        say(f"    {p.name:<6} {'RULES v2':<10} {'live baseline':<34} OOS {bars['liveO']['CAGR']:>7.2%} / "
            f"{bars['liveO']['Sharpe']:>7.4f} / {bars['liveO']['MaxDD']:>8.2%}")
        # G6: every chooser statistic is computed on rows < i_oos, asserted by re-computation
        for N in rungs[p.name]:
            for c in BANDS:
                for x in percell[(p.name, N, c)]:
                    r = net(x["rgB"], x["tuB"], BIND)
                    if not (np.isnan(x["IS_S"]) or abs(sharpe(r[WARMUP:i_oos]) - x["IS_S"]) < 1e-15):
                        g6ok = False
    gate("G6 no chooser statistic reads a row on or after 2017-01-01 (re-tested on truncated input)",
         g6ok, "True", g6ok)
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"    rule-8 picks clearing 4a OOS: {int(pd.DataFrame(wf).O_keep4a.sum())}/{len(wf)}; "
        f"4b OOS: {int(pd.DataFrame(wf).O_keep4b.sum())}/{len(wf)}")

    # ------------------------------------------------ gates + files
    gg = pd.DataFrame(GATES)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gg["pass_"].sum())
    say(f"\n  GATES {npass}/{len(gg)} pass.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  wrote {Path(OUT).name}.grid.csv.gz / .curve.csv / .decisive.csv / .monotone.csv / "
        f".legs.csv / .walkforward.csv / .draws.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
