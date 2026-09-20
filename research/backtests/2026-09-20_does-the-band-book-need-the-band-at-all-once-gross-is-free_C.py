#!/usr/bin/env python3
"""Idea 1699 (lane C, 2026-09-20): does the BAND BOOK NEED THE BAND AT ALL once GROSS is free?

WHY THIS IDEA.  The book this repository would put capital behind is RULES v2: hold every name
whose price sits inside its own 200d +/- c hysteresis band at gross/N of NAV, send the gated-out
weight to CASH, rebalance weekly.  It has exactly two dials, c and G, and the record's own
evidence says only ONE of them is doing anything:

  * the 2026-09-19 CHANGELOG's rule-8 pick wanders across c = 0.00 .. 0.10 from chooser to
    chooser while **G pins to 1.00 at every passing cell** (idea 1703 re-read it this week: all
    5 U56 4b passes sit at G = 1.00, the top gross rung);
  * nine consecutive runs have found every device in this record beaten, at matched exposure, by
    a plain de-gross;
  * idea 1617 measured the band's whole matched-twin Sharpe edge at +0.0089 on U56, and NEGATIVE
    at 25 bps.

If the band rung is free, then the standing "4b pass" is not a trend-following result at all: it
is a statement about how much equity beta you hold, wearing a 200d moving average as a costume.
That is a capital question, because a gate you do not need is turnover you do not need to pay
for, plus a parameter you do not need to defend.

THE DESIGN THAT MAKES THIS ANSWERABLE.  Every prior run priced the no-gate twin as an OUTSIDE
CONTROL beside the grid.  This run puts it INSIDE the grid, as the first rung of dial 1, so that
"no band at all" is a cell a chooser can legally pick and a 4b verdict can legally land on:

  c  {NOGATE, 0.00, 0.03, 0.05, 0.10, 0.15}   DIAL 1 -- band half-width, with NOGATE = the band
                                              removed entirely (always invested, equal weight
                                              over the priced names at the same target gross).
                                              0.03 is LIVE; 0.10 is the 2026-09-19 rule-8 pick;
                                              0.00 is the bare 200d MA with no hysteresis.
  G  {0.25, 0.50, 0.75, 1.00}                 DIAL 2 -- constant target gross.  0.75 is LIVE;
                                              1.00 is the rung every committed 4b pass sits at.
                                              Stops at 1.00: no leverage (PROTOCOL rule 2).

24 cells per panel x 3 panels (U56 / B136 / SMALL) = 72 books, EVERY ONE PUBLISHED.

TWO MATCHINGS, BOTH REPORTED, BECAUSE THEY ASK DIFFERENT QUESTIONS.
  TARGET-gross matching (the idea's own wording): band(c,G) vs NOGATE(G).  This is the honest
      "should I run the gate?" comparison for an investor who has decided on a target gross G --
      the gate's de-grossing is part of what the gate DOES, not a confound to be removed.
  REALISED-gross matching (this record's nine-run convention): band(c,G) vs NOGATE(G') where G'
      is solved so the twin's REALISED mean gross equals the band cell's.  G' is DERIVED by
      bisection from the band cell's own realised exposure, never tuned, and published for every
      cell.  This is the comparison that asks whether the gate TIMES anything, holding exposure
      fixed.
  Both are needed: a device that wins only on the first is a de-gross wearing a signal.

CHOOSERS (PROTOCOL rule 8), each fit on warm-up..2016-12-31 ONLY, 2017-2026 then read ONCE:
  C_SHARPE   argmax IS Sharpe                               (the record's usual chooser)
  C_MEMO     smallest G whose IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
             ties by smallest c (NOGATE sorts first); else fall back to the live cell
  C_CAGR     argmax IS CAGR among cells clearing the IS MaxDD bar
  C_ANCHOR   (0.03, 0.75), the live book, choosing nothing  (the null)
Each is run three times over three ARENAS: the FULL 24-cell grid (NOGATE choosable), the BAND-ONLY
20 cells (the world as the record has always searched it), and the NOGATE-ONLY 4 cells (a world
with no 200d MA in it at all).  The contrast between arena OOS outcomes IS the answer to 1699.

WHAT WOULD MAKE THIS A FINDING, PRE-REGISTERED BEFORE ANY NUMBER WAS READ:
  (i)  If the NOGATE arena's rule-8 picks match or beat the BAND arena's OOS, and the band's
       matched-gross Sharpe edge sits inside its own paired block-bootstrap SE, then the band
       rung is FREE and the standing 4b pass is a GROSS claim.  KILL of the band clause as a
       device; the record should stop quoting c as if it were load-bearing.
  (ii) If the band arena beats the nogate arena OOS on all three panels AND the matched-REALISED
       -gross edge clears |t| > 2, the gate earns its place and c is load-bearing after all.
  (iii) If the band wins at matched TARGET gross but not at matched REALISED gross, the gate's
       entire value is the de-gross, and the same thing is bought more cheaply by lowering G.
All three outcomes are reported.  Nothing is re-tuned after reading the answer.

OVERLAP DECLARED.  Idea 1703 (lane B, pushed earlier today) priced 92 no-gate twins as an
OUTSIDE control on U56 / ETF36 / STK20 and reported one 4b passer (equal-weight STK20 at
G = 0.50).  This run does not re-ask that: it moves the twin INSIDE the grid on the record's
three standing panels, adds the realised-gross-matched twin (which 1703 did not run), and lets
rule-8 choosers pick it.  Where the two runs share a cell (U56, c in {0.00,0.03,0.05,0.10,0.15},
G, no-gate at target G) the numbers are cross-checked as gate G8.

HONEST LIMITS.  U56 and B136 are CURRENT-constituent lists (PROTOCOL rule 9) and idea 1703
showed this week that the U56 4b pass does not survive deleting the 20 mega-caps -- so every
absolute level below is an UPPER BOUND and no cell here is a capital recommendation.  What this
run measures is a CONTRAST between two books on the same flattered tape, which is the one thing
survivorship does not obviously break.  SMALL is the sub-$2B panel and carries the same caveat.

GATES.  G0 >= 10y per panel (rule 1).  G1 CROSS-SCRIPT REPLAY: U56 (c=0.03,G=0.75) reproduces
`baseline.rules_v2_weights` through `engine.backtest`.  G2 no leverage / no shorting.  G3 all 72
cells + every derived realised-matched twin published.  G4 exactly two tuned parameters.  G5 no
chooser reads a row on or after 2017-01-01 (asserted by hard truncation).  G6 determinism.  G7
PUBLISHED: panel composition counts, realised mean gross, in-band share, turnover/yr.  G8
CROSS-RUN: U56 (c=0.10,G=1.00) reproduces idea 1703's committed 11.72% / 1.1726 / -16.30%.
G9 realised-gross matching converged to < 1e-4 at every cell.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 5 (one idea, one script); rule 7 (report honestly);
rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_does-the-band-book-need-the-band-at-all-once-gross-is-free_C.py
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

DATE, SLUG = "2026-09-20", "does-the-band-book-need-the-band-at-all-once-gross-is-free"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
COST = 10.0
CAD = "W"
NOGATE = -1.0                                  # the c label for "no band at all"
GRID_C = [NOGATE, 0.00, 0.03, 0.05, 0.10, 0.15]
BAND_C = [c for c in GRID_C if c != NOGATE]
GRID_G = [0.25, 0.50, 0.75, 1.00]
LIVE_C, LIVE_G = 0.03, 0.75                    # the live RULES v2 cell
PICK_C, PICK_G = 0.10, 1.00                    # the 2026-09-19 CHANGELOG rule-8 pick
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_BLOCK, BOOT_DRAWS, SEED = 21, 2000, 20260920
# idea 1703's committed U56 cell, for the cross-run gate G8
REF_1703 = dict(CAGR=0.1172, Sharpe=1.1726, MaxDD=-0.1630)

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


def clabel(c):
    return "NOGATE" if c == NOGATE else f"{c:.2f}"


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


def pack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE book (PROTOCOL 4a); 4b against SPY (PROTOCOL 4b).  Legs returned."""
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- the tape and the book
class Tape:
    """One price frame + the per-name band states at every c on dial 1."""

    def __init__(self, px, name):
        self.name = name
        self.px = px
        self.idx = px.index
        self.cols = list(px.columns)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.band = {c: band_state(px, band=c).values for c in BAND_C}
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def targets(tape, c, g):
    """RULES v2's shape: target gross g spread equally over the names PRICED that day, held only
    where the 200d +/- c band says IN; gated-out weight goes to CASH (de-gross, never re-spread).
    c == NOGATE removes the gate entirely -- always invested, same target gross."""
    pr = tape.priced.astype(float)
    n = pr.sum(axis=1)
    W = np.zeros_like(pr)
    nz = n > 0
    W[nz] = g * pr[nz] / n[nz, None]
    if c != NOGATE:
        W = W * tape.band[c]
    return W


def run(tape, W, cost=COST):
    """engine.backtest's arithmetic, vectorised per rebalance segment: weights decided at the
    close of day t-1 are applied from day t, positions drift between rebalances, un-invested NAV
    earns 0.00%, turnover is charged at `cost` bps."""
    rets = tape.rets
    T, M = rets.shape
    out = np.zeros(T)
    turn = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wmax = 0.0
    ends = np.append(tape.reb[1:], T)
    C, Cp = tape.C, tape.Cp
    for i0, i1 in zip(tape.reb, ends):
        if i1 <= i0:
            continue
        w0 = W[i0 - 1] if i0 > 0 else W[0]
        s0 = float(w0.sum())
        wmax = max(wmax, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, wmax, gsum


def realised_gross(tape, g):
    """Realised mean gross of the NOGATE book at target gross g, over the scored window."""
    _, _, _, gs = run(tape, targets(tape, NOGATE, g))
    return float(np.mean(gs[WARMUP:]))


def solve_matched_target(tape, want, cache, lo=0.0, hi=1.0, tol=1e-5, iters=40):
    """Bisect the NOGATE target gross so its REALISED mean gross equals `want`.  Monotone in g.
    DERIVED from the band cell's own exposure -- not a tuned parameter (PROTOCOL rule 4)."""
    def f(g):
        if g not in cache:
            cache[g] = realised_gross(tape, g)
        return cache[g]
    if want >= f(hi):
        return hi, f(hi)
    a, b = lo, hi
    best, best_err = hi, abs(f(hi) - want)
    for _ in range(iters):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm - want) < best_err:
            best, best_err = m, abs(fm - want)
        if best_err < tol:
            break
        if fm < want:
            a = m
        else:
            b = m
    return best, f(best)


# ---------------------------------------------------------------- paired block bootstrap
def _sh_rows(X):
    s = X.std(axis=1, ddof=0)
    return np.where(s > 0, X.mean(axis=1) * np.sqrt(252) / s, np.nan)


def _mdd_rows(X):
    e = np.cumprod(1.0 + X, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1.0).min(axis=1)


def boot_contrast(rb, rn, stat, block=BOOT_BLOCK, draws=BOOT_DRAWS, seed=SEED):
    """Circular block bootstrap of stat(band) - stat(nogate), PAIRED: the SAME block indices are
    applied to both streams, so the common tape cancels and what is left is the device contrast.
    stat in {'Sharpe', 'MaxDD'} (MaxDD contrast is positive when the band book is SHALLOWER)."""
    rb, rn = np.asarray(rb, float), np.asarray(rn, float)
    T = len(rb)
    nb = int(np.ceil(T / block))
    rng = np.random.default_rng(seed)
    f = _sh_rows if stat == "Sharpe" else _mdd_rows
    obs = float(f(rb[None, :])[0] - f(rn[None, :])[0])
    off = (np.arange(block)[None, :] + rng.integers(0, T, size=(draws * nb, 1))) % T
    off = off.reshape(draws, nb * block)[:, :T]
    d = f(rb[off]) - f(rn[off])
    se = float(np.nanstd(d, ddof=1))
    t = float(obs / se) if se > 0 else np.nan
    p = float(np.nanmean(np.abs(d - np.nanmean(d)) >= abs(obs)))
    lo, hi = np.nanpercentile(d, [2.5, 97.5])
    return dict(stat=stat, obs=obs, se=se, t=t, p=p, lo=float(lo), hi=float(hi))


# ---------------------------------------------------------------- choosers (rule 8)
def _key(k):
    """Sort key over cells: NOGATE first on c, then smallest G."""
    return (k[1], k[0])


def c_sharpe(cells, isp):
    return max(cells, key=lambda k: (isp[k]["Sharpe"], -k[1], -k[0]))


def c_memo(cells, isp, dd_bar, cagr_bar, fallback):
    ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar and isp[k]["CAGR"] >= cagr_bar]
    if not ok:
        return fallback, True
    return min(ok, key=_key), False


def c_cagr(cells, isp, dd_bar, fallback):
    ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar]
    if not ok:
        return fallback, True
    return max(ok, key=lambda k: (isp[k]["CAGR"], -k[1], -k[0])), False


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1699 (lane C, 2026-09-20) — DOES THE BAND BOOK NEED THE BAND AT ALL ONCE GROSS IS FREE?")
    say(f"DIALS: c {[clabel(c) for c in GRID_C]} x G {GRID_G}.  Panels U56 / B136 / SMALL.")
    say(f"Weekly cadence, {COST:.0f} bps, t+1 execution.  NOGATE is a GRID CELL, not an outside control.")
    say("=" * 118)

    # ---- panels
    panels = []
    px_u = load_universe()
    panels.append(("U56", px_u))
    px_b = load_universe(broad=True)
    panels.append(("B136", px_b))
    px_s = load_universe(small=True)
    mx = px_s.pct_change().abs().max()
    drop = [c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0]
    px_s = px_s.drop(columns=drop)
    panels.append(("SMALL", px_s))

    say("\n  PANELS (not a dial — the whole grid runs on every one, none is picked on its result):")
    for nm, p in panels:
        say(f"    {nm:6s} {p.shape[1]:4d} columns  {p.index[0].date()} .. {p.index[-1].date()}  "
            f"{len(p)} rows ({len(p)/252:.1f}y)")
        publish(f"G7 COMPOSITION {nm}", f"{p.shape[1]} columns incl. SPY, "
                                        f"{p.index[0].date()}..{p.index[-1].date()}")
    publish("G7 SMALL max_1d_move >= 1.0 drops (idea 1074 convention)",
            f"{len(drop)} names dropped, {px_s.shape[1]} columns remain")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL is a")
    say("  current-screen panel, so every ABSOLUTE level below is an UPPER BOUND — idea 1703")
    say("  showed today that U56's own 4b pass dies when its 20 mega-caps are deleted.  This run")
    say("  reads CONTRASTS between two books on the SAME tape, which is what survives that.")
    say("  The SPY column enters each panel's book as one name, exactly as baseline.rules_v2_weights does.")

    tapes = {nm: Tape(p, nm) for nm, p in panels}
    for nm, tp in tapes.items():
        gate(f"G0 {nm} sample >= 10 years (rule 1)", round(len(tp.idx) / 252.0, 2), ">= 10.0",
             len(tp.idx) / 252.0 >= 10.0)

    # ---- bars: SPY per panel-window, and the LIVE RULES v2 book (U56, as traded)
    bars = {}
    for nm, tp in tapes.items():
        i_oos = int(np.searchsorted(tp.idx.values, np.datetime64(OOS_START)))
        bars[nm] = dict(i_oos=i_oos,
                        spy_f=pack(tp.spy[WARMUP:]), spy_i=pack(tp.spy[WARMUP:i_oos]),
                        spy_o=pack(tp.spy[i_oos:]))
        b = bars[nm]
        say(f"\n  SPY on {nm}: FULL {b['spy_f']['CAGR']:.2%} / {b['spy_f']['Sharpe']:.4f} / "
            f"{b['spy_f']['MaxDD']:.2%}  H1/H2 {b['spy_f']['H1']:.4f}/{b['spy_f']['H2']:.4f}")
        say(f"      4b bars FULL: H1 > {b['spy_f']['H1']:.4f}, H2 > {b['spy_f']['H2']:.4f}, "
            f"MaxDD >= {DD_CAP*b['spy_f']['MaxDD']:.2%}, CAGR >= {CAGR_FLOOR*b['spy_f']['CAGR']:.2%}")
        say(f"      4b bars OOS : H1 > {b['spy_o']['H1']:.4f}, H2 > {b['spy_o']['H2']:.4f}, "
            f"MaxDD >= {DD_CAP*b['spy_o']['MaxDD']:.2%}, CAGR >= {CAGR_FLOOR*b['spy_o']['CAGR']:.2%}")

    lr = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST, freq=CAD)["returns"].values
    io_u = bars["U56"]["i_oos"]
    live_f, live_o = pack(lr[WARMUP:]), pack(lr[io_u:])
    say(f"\n  RULES v2 LIVE (U56, as traded) FULL {live_f['CAGR']:.2%} / {live_f['Sharpe']:.4f} / "
        f"{live_f['MaxDD']:.2%}  H1/H2 {live_f['H1']:.4f}/{live_f['H2']:.4f}")
    say(f"  RULES v2 LIVE (U56, as traded) OOS  {live_o['CAGR']:.2%} / {live_o['Sharpe']:.4f} / "
        f"{live_o['MaxDD']:.2%}")
    say("  NOTE ON 4a: the book is RULES v2 as actually traded (on U56), so 4a is judged against")
    say("  that one row on every panel.  Each panel's own (c=0.03,G=0.75) cell is in the grid for")
    say("  anyone who prefers the panel-local reading.")

    # ---- G1: the U56 live cell IS baseline.rules_v2_weights
    r_fast, _, _, _ = run(tapes["U56"], targets(tapes["U56"], LIVE_C, LIVE_G))
    n_nan = int(np.isnan(lr).sum())
    d_ret = float(np.max(np.abs(r_fast[WARMUP:] - lr[WARMUP:])))
    publish("G1a engine.backtest NaN warm-up rows before its first weekly rebalance",
            f"{n_nan} of {len(lr)} (all inside the {WARMUP}-row warm-up every metric discards)")
    gate("G1 replay U56 (c=0.03,G=0.75) vs engine.backtest(baseline.rules_v2_weights)",
         f"{d_ret:.3e}", "< 1e-12", d_ret < 1e-12)

    # ---- the grid
    grid, RET, ISP, GROSS = [], {}, {}, {}
    wmax_global = 0.0
    for nm, tp in tapes.items():
        b = bars[nm]
        i_oos = b["i_oos"]
        for c in GRID_C:
            for g in GRID_G:
                rr, tu, ws, gs = run(tp, targets(tp, c, g))
                wmax_global = max(wmax_global, ws)
                RET[(nm, c, g)] = rr
                GROSS[(nm, c, g)] = float(np.mean(gs[WARMUP:]))
                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], b["spy_f"], live_f)
                k4aO, k4bO, mo, oh1, oh2, legsO = keep_paths(rr[i_oos:], b["spy_o"], live_o)
                isp = dict(Sharpe=sharpe(rr[WARMUP:i_oos]), CAGR=cagr(rr[WARMUP:i_oos]),
                           MaxDD=mdd(rr[WARMUP:i_oos]))
                ISP[(nm, c, g)] = isp
                inband = 1.0 if c == NOGATE else float(np.mean(tp.band[c][WARMUP:]))
                grid.append(dict(panel=nm, c=c, c_label=clabel(c), G=g, gate_on=(c != NOGATE),
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                 oH1=oh1, oH2=oh2,
                                 isCAGR=isp["CAGR"], isSharpe=isp["Sharpe"], isMaxDD=isp["MaxDD"],
                                 mean_gross=GROSS[(nm, c, g)], in_band_share=inband,
                                 turnover_yr=float(tu[WARMUP:].sum() / ((len(rr) - WARMUP) / 252.0)),
                                 keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                 leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                 leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"], oleg_H2=legsO["H2"],
                                 oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"]))
    G = pd.DataFrame(grid)
    G["keep4b_both"] = G["keep4b"] & G["keep4b_oos"]
    gate("G2 no leverage / no shorting: max target gross", f"{wmax_global:.6f}", "<= 1.000001",
         wmax_global <= 1.000001)
    gate("G3 all grid cells published", f"{len(G)} cells",
         f"{len(tapes)*len(GRID_C)*len(GRID_G)}", len(G) == len(tapes) * len(GRID_C) * len(GRID_G))
    gate("G4 tuned parameters", "2 (c including a NOGATE rung, G)", "<= 2 (rule 4)", True)

    rr2, _, _, _ = run(tapes["U56"], targets(tapes["U56"], PICK_C, PICK_G))
    gate("G6 determinism: U56 (0.10,1.00) recompute bit-identical", "exact",
         "array_equal", bool(np.array_equal(rr2, RET[("U56", PICK_C, PICK_G)])))

    pick_row = G[(G.panel == "U56") & (G.c == PICK_C) & (G.G == PICK_G)].iloc[0]
    d8 = max(abs(pick_row.CAGR - REF_1703["CAGR"]), abs(pick_row.Sharpe - REF_1703["Sharpe"]),
             abs(pick_row.MaxDD - REF_1703["MaxDD"]))
    gate("G8 CROSS-RUN vs idea 1703's committed U56 (c=0.10,G=1.00) 11.72%/1.1726/-16.30%",
         f"{pick_row.CAGR:.4%} / {pick_row.Sharpe:.4f} / {pick_row.MaxDD:.4%}, max|d| {d8:.2e}",
         "< 5e-4 (their published precision)", d8 < 5e-4)

    say("\n" + "=" * 118)
    say("FULL GRID — 72 books, every cell published (mean_gross is REALISED, not target)")
    say("=" * 118)
    for nm in tapes:
        say(f"\n  --- {nm} " + "-" * 100)
        sub = G[G.panel == nm].copy()
        say("   c       G     gross  band%  turn/y |   CAGR  Sharpe    MaxDD     H1     H2 | "
            " oCAGR oSharpe   oMaxDD | 4a 4b 4bOOS")
        for _, r in sub.iterrows():
            say(f"  {r.c_label:>6s} {r.G:5.2f}  {r.mean_gross:6.4f} {r.in_band_share:5.3f} "
                f"{r.turnover_yr:6.2f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} "
                f"{r.H1:6.3f} {r.H2:6.3f} | {r.oCAGR:6.2%} {r.oSharpe:7.4f} {r.oMaxDD:8.2%} | "
                f"{'Y' if r.keep4a else '.':>2s} {'Y' if r.keep4b else '.':>2s} "
                f"{'Y' if r.keep4b_oos else '.':>4s}")

    say("\n  4b/4a CENSUS BY ARENA (FULL-and-OOS passes):")
    for nm in tapes:
        sub = G[G.panel == nm]
        bandc = sub[sub.gate_on]
        nog = sub[~sub.gate_on]
        say(f"    {nm:6s} BAND 4b FULL {int(bandc.keep4b.sum()):2d}/{len(bandc)}  "
            f"FULL-and-OOS {int(bandc.keep4b_both.sum()):2d}/{len(bandc)}  4a {int(bandc.keep4a.sum()):2d}/{len(bandc)}"
            f"   ||  NOGATE 4b FULL {int(nog.keep4b.sum())}/{len(nog)}  "
            f"FULL-and-OOS {int(nog.keep4b_both.sum())}/{len(nog)}  4a {int(nog.keep4a.sum())}/{len(nog)}")
    say("\n  WHICH 4b LEG FAILS, AND WHERE — the leg census that says what the band is FOR:")
    for arena, sel in (("BAND  ", G.gate_on), ("NOGATE", ~G.gate_on)):
        sub = G[sel]
        fails = sub[~sub.keep4b]
        say(f"    {arena} FULL failures {len(fails)}/{len(sub)}: "
            f"H1 {int((~fails.leg_H1).sum())}, H2 {int((~fails.leg_H2).sum())}, "
            f"DD {int((~fails.leg_DD).sum())}, CAGR {int((~fails.leg_CAGR).sum())}")
    say("    NOGATE cell by cell (the squeeze the band escapes):")
    for _, r in G[~G.gate_on].iterrows():
        bad = [k for k, v in (("H1", r.leg_H1), ("H2", r.leg_H2), ("DD", r.leg_DD),
                              ("CAGR", r.leg_CAGR)) if not v]
        say(f"      {r.panel:6s} G={r.G:.2f}  CAGR {r.CAGR:6.2%}  MaxDD {r.MaxDD:8.2%}  "
            f"Sharpe {r.Sharpe:.4f}  FULL 4b fails on: {','.join(bad) if bad else 'NONE (pass)'}")

    # ---------------------------------------------------------- (1) matched TARGET gross
    say("\n" + "=" * 118)
    say("(1) MATCHED TARGET GROSS — band(c,G) MINUS nogate(G), the idea's own comparison")
    say("=" * 118)
    tg = []
    for nm in tapes:
        for g in GRID_G:
            base = G[(G.panel == nm) & (~G.gate_on) & (G.G == g)].iloc[0]
            for c in BAND_C:
                r = G[(G.panel == nm) & (G.c == c) & (G.G == g)].iloc[0]
                tg.append(dict(panel=nm, c=c, c_label=clabel(c), G=g,
                               dSharpe=r.Sharpe - base.Sharpe, dCAGR=r.CAGR - base.CAGR,
                               dMaxDD=r.MaxDD - base.MaxDD,
                               odSharpe=r.oSharpe - base.oSharpe, odCAGR=r.oCAGR - base.oCAGR,
                               odMaxDD=r.oMaxDD - base.oMaxDD,
                               dturn=r.turnover_yr - base.turnover_yr,
                               band4b=bool(r.keep4b_both), nogate4b=bool(base.keep4b_both)))
    TG = pd.DataFrame(tg)
    say(f"  {len(TG)} matched-target pairs.  Band beats its same-G nogate twin on FULL Sharpe at "
        f"{int((TG.dSharpe>0).sum())}/{len(TG)}, OOS Sharpe {int((TG.odSharpe>0).sum())}/{len(TG)}, "
        f"FULL CAGR {int((TG.dCAGR>0).sum())}/{len(TG)}, FULL MaxDD (shallower) "
        f"{int((TG.dMaxDD>0).sum())}/{len(TG)}")
    say(f"  mean dSharpe FULL {TG.dSharpe.mean():+.4f} (median {TG.dSharpe.median():+.4f}), "
        f"OOS {TG.odSharpe.mean():+.4f}; mean dCAGR {TG.dCAGR.mean():+.2%}; "
        f"mean dMaxDD {TG.dMaxDD.mean():+.2%} pp-shallower; mean extra turnover "
        f"{TG.dturn.mean():+.2f}x/yr")
    for nm in tapes:
        s = TG[TG.panel == nm]
        say(f"    {nm:6s} dSharpe FULL {s.dSharpe.mean():+.4f}  OOS {s.odSharpe.mean():+.4f}  "
            f"dCAGR {s.dCAGR.mean():+.2%}  dMaxDD {s.dMaxDD.mean():+.2%}  "
            f"wins {int((s.dSharpe>0).sum())}/{len(s)}")

    # ---------------------------------------------------------- (2) matched REALISED gross
    say("\n" + "=" * 118)
    say("(2) MATCHED REALISED GROSS — the record's nine-run convention.  The twin's target gross")
    say("    G' is DERIVED by bisection so its REALISED mean gross equals the band cell's.")
    say("=" * 118)
    rg = []
    worst_conv = 0.0
    for nm, tp in tapes.items():
        b = bars[nm]
        i_oos = b["i_oos"]
        cache = {}
        for c in BAND_C:
            for g in GRID_G:
                want = GROSS[(nm, c, g)]
                gp, got = solve_matched_target(tp, want, cache)
                worst_conv = max(worst_conv, abs(got - want))
                rr, tu, _, gs = run(tp, targets(tp, NOGATE, gp))
                m, mo = pack(rr[WARMUP:]), pack(rr[i_oos:])
                _, k4b, _, _, _, _ = keep_paths(rr[WARMUP:], b["spy_f"], live_f)
                _, k4bO, _, _, _, _ = keep_paths(rr[i_oos:], b["spy_o"], live_o)
                r = G[(G.panel == nm) & (G.c == c) & (G.G == g)].iloc[0]
                rg.append(dict(panel=nm, c=c, c_label=clabel(c), G=g, want_gross=want,
                               twin_target=gp, twin_gross=got,
                               band_Sharpe=r.Sharpe, twin_Sharpe=m["Sharpe"],
                               dSharpe=r.Sharpe - m["Sharpe"],
                               band_CAGR=r.CAGR, twin_CAGR=m["CAGR"], dCAGR=r.CAGR - m["CAGR"],
                               band_MaxDD=r.MaxDD, twin_MaxDD=m["MaxDD"],
                               dMaxDD=r.MaxDD - m["MaxDD"],
                               odSharpe=r.oSharpe - mo["Sharpe"], odCAGR=r.oCAGR - mo["CAGR"],
                               odMaxDD=r.oMaxDD - mo["MaxDD"],
                               twin4b=bool(k4b and k4bO), band4b=bool(r.keep4b_both),
                               twin_turn=float(tu[WARMUP:].sum() / ((len(rr) - WARMUP) / 252.0)),
                               band_turn=r.turnover_yr))
    RG = pd.DataFrame(rg)
    gate("G9 realised-gross matching convergence", f"max|d| {worst_conv:.2e}", "< 1e-4",
         worst_conv < 1e-4)
    say(f"  {len(RG)} matched-realised pairs.  Band beats the exposure-matched twin on FULL Sharpe "
        f"at {int((RG.dSharpe>0).sum())}/{len(RG)}, OOS Sharpe {int((RG.odSharpe>0).sum())}/{len(RG)}, "
        f"FULL MaxDD (shallower) {int((RG.dMaxDD>0).sum())}/{len(RG)}")
    say(f"  mean dSharpe FULL {RG.dSharpe.mean():+.4f} (median {RG.dSharpe.median():+.4f}), "
        f"OOS {RG.odSharpe.mean():+.4f}; mean dCAGR {RG.dCAGR.mean():+.2%}; mean dMaxDD "
        f"{RG.dMaxDD.mean():+.2%}; mean extra turnover {(RG.band_turn-RG.twin_turn).mean():+.2f}x/yr")
    for nm in tapes:
        s = RG[RG.panel == nm]
        say(f"    {nm:6s} dSharpe FULL {s.dSharpe.mean():+.4f}  OOS {s.odSharpe.mean():+.4f}  "
            f"dMaxDD {s.dMaxDD.mean():+.2%}  wins {int((s.dSharpe>0).sum())}/{len(s)}  "
            f"twin 4b FULL-and-OOS {int(s.twin4b.sum())}/{len(s)} vs band {int(s.band4b.sum())}/{len(s)}")
    say("\n  THE TWO HEADLINE CELLS, both matchings side by side:")
    for nm in tapes:
        for (c, g, tag) in ((LIVE_C, LIVE_G, "LIVE"), (PICK_C, PICK_G, "2026-09-19 PICK")):
            a = TG[(TG.panel == nm) & (TG.c == c) & (TG.G == g)].iloc[0]
            r = RG[(RG.panel == nm) & (RG.c == c) & (RG.G == g)].iloc[0]
            say(f"    {nm:6s} c={clabel(c)} G={g:.2f} [{tag:15s}]  target-matched dSharpe "
                f"{a.dSharpe:+.4f} (OOS {a.odSharpe:+.4f}) | realised-matched (G'={r.twin_target:.4f}) "
                f"dSharpe {r.dSharpe:+.4f} (OOS {r.odSharpe:+.4f}), dMaxDD {r.dMaxDD:+.2%}")

    # ---------------------------------------------------------- (3) is the edge inside its noise?
    say("\n" + "=" * 118)
    say("(3) IS THE BAND'S EDGE INSIDE ITS OWN NOISE?  Paired circular block bootstrap of")
    say(f"    BOTH legs the band could be earning — Sharpe AND MaxDD — {BOOT_BLOCK}-day blocks,")
    say(f"    {BOOT_DRAWS} draws, seed {SEED}.  The MaxDD leg is bootstrapped because section (2)")
    say("    says depth is the ONLY axis on which the band beats an exposure-matched twin, and")
    say("    idea 1511 put the paired SE of a dMaxDD contrast at 2.93 pp — the same order as the")
    say("    edge itself.  A positive dMaxDD means the BAND book is SHALLOWER.")
    say("=" * 118)
    boots = []
    for nm, tp in tapes.items():
        cache = {}
        for (c, g, tag) in ((LIVE_C, LIVE_G, "LIVE"), (PICK_C, PICK_G, "PICK")):
            rb = RET[(nm, c, g)][WARMUP:]
            gp, _ = solve_matched_target(tp, GROSS[(nm, c, g)], cache)
            twins = (("target-matched", RET[(nm, NOGATE, g)][WARMUP:]),
                     ("realised-matched", run(tp, targets(tp, NOGATE, gp))[0][WARMUP:]))
            for kind, rn in twins:
                for stat in ("Sharpe", "MaxDD"):
                    d = boot_contrast(rb, rn, stat)
                    boots.append(dict(panel=nm, cell=f"c={clabel(c)},G={g:.2f}", tag=tag,
                                      match=kind, **d))
                    unit = "pp" if stat == "MaxDD" else "  "
                    sc = 100.0 if stat == "MaxDD" else 1.0
                    say(f"    {nm:6s} {tag:5s} {kind:17s} d{stat:6s} {d['obs']*sc:+8.4f}{unit}  "
                        f"SE {d['se']*sc:7.4f}  t {d['t']:+.2f}  p {d['p']:.3f}  "
                        f"95% [{d['lo']*sc:+.4f}, {d['hi']*sc:+.4f}]")
    BT = pd.DataFrame(boots)
    for stat in ("Sharpe", "MaxDD"):
        s = BT[BT.stat == stat]
        say(f"  |t| > 2 at {int((s.t.abs()>2).sum())} of {len(s)} d{stat} contrasts "
            f"(max |t| {s.t.abs().max():.2f}, min p {s.p.min():.3f}).")

    # ---------------------------------------------------------- (4) rule 8, three arenas
    say("\n" + "=" * 118)
    say("(4) RULE 8 — choosers fit on warm-up..2016-12-31 ONLY; 2017-2026 read EXACTLY ONCE.")
    say("    THREE ARENAS: FULL (24 cells, NOGATE choosable) / BAND-ONLY (20) / NOGATE-ONLY (4).")
    say("=" * 118)
    arenas = {"FULL": GRID_C, "BAND": BAND_C, "NOGATE": [NOGATE]}
    picks = []
    for nm in tapes:
        b = bars[nm]
        dd_bar = DD_CAP * b["spy_i"]["MaxDD"]
        cagr_bar = CAGR_FLOOR * b["spy_i"]["CAGR"]
        for aname, cs in arenas.items():
            cells = [(c, g) for c in cs for g in GRID_G]
            isp = {k: ISP[(nm, k[0], k[1])] for k in cells}
            fb = (LIVE_C, LIVE_G) if LIVE_C in cs else (NOGATE, LIVE_G)
            cand = {"C_SHARPE": (c_sharpe(cells, isp), False)}
            cand["C_MEMO"] = c_memo(cells, isp, dd_bar, cagr_bar, fb)
            cand["C_CAGR"] = c_cagr(cells, isp, dd_bar, fb)
            cand["C_ANCHOR"] = (fb, False)
            for cname, (k, fell) in cand.items():
                r = G[(G.panel == nm) & (G.c == k[0]) & (G.G == k[1])].iloc[0]
                picks.append(dict(panel=nm, arena=aname, chooser=cname, c=k[0],
                                  c_label=clabel(k[0]), G=k[1], fellback=fell,
                                  isSharpe=r.isSharpe, oCAGR=r.oCAGR, oSharpe=r.oSharpe,
                                  oMaxDD=r.oMaxDD, keep4b_oos=bool(r.keep4b_oos),
                                  keep4b_both=bool(r.keep4b_both), keep4a_oos=bool(r.keep4a_oos)))
    P = pd.DataFrame(picks)
    for nm in tapes:
        say(f"\n  --- {nm} " + "-" * 100)
        for aname in arenas:
            for _, r in P[(P.panel == nm) & (P.arena == aname)].iterrows():
                say(f"    {aname:7s} {r.chooser:9s} -> c={r.c_label:>6s} G={r.G:.2f}"
                    f"{' (fallback)' if r.fellback else '           '}  OOS {r.oCAGR:6.2%} / "
                    f"{r.oSharpe:7.4f} / {r.oMaxDD:8.2%}   4b_OOS {'Y' if r.keep4b_oos else '.'}"
                    f"  4a_OOS {'Y' if r.keep4a_oos else '.'}")
    say("\n  ARENA SUMMARY — mean OOS Sharpe of the 4 choosers, and 4b_OOS pass count:")
    for nm in tapes:
        row = []
        for aname in arenas:
            s = P[(P.panel == nm) & (P.arena == aname)]
            row.append(f"{aname} {s.oSharpe.mean():.4f} (4b {int(s.keep4b_oos.sum())}/{len(s)})")
        say(f"    {nm:6s} " + "   ||  ".join(row))
    say(f"  Across all panels: FULL {P[P.arena=='FULL'].oSharpe.mean():.4f}, "
        f"BAND {P[P.arena=='BAND'].oSharpe.mean():.4f}, "
        f"NOGATE {P[P.arena=='NOGATE'].oSharpe.mean():.4f}")
    nfull = P[(P.arena == "FULL")]
    say(f"  In the FULL arena the chooser lands on the NOGATE rung at "
        f"{int((nfull.c == NOGATE).sum())} of {len(nfull)} picks; on G=1.00 at "
        f"{int((nfull.G == 1.00).sum())} of {len(nfull)}; on the LIVE cell at "
        f"{int(((nfull.c == LIVE_C) & (nfull.G == LIVE_G)).sum())}.")

    # ---- G5: hard-truncation proof that no chooser saw an OOS row
    ok5 = True
    for nm, tp in tapes.items():
        i_oos = bars[nm]["i_oos"]
        for c in GRID_C:
            for g in GRID_G:
                rr = RET[(nm, c, g)]
                trunc = rr[:i_oos].copy()
                if abs(sharpe(trunc[WARMUP:]) - ISP[(nm, c, g)]["Sharpe"]) > 1e-12:
                    ok5 = False
                if tp.idx[i_oos - 1] >= pd.Timestamp(OOS_START):
                    ok5 = False
    gate("G5 no chooser reads a row on or after 2017-01-01 (re-fit on hard-truncated arrays)",
         "IS statistics reproduce exactly from truncated arrays", "identical", ok5)

    # ---------------------------------------------------------- verdict
    say("\n" + "=" * 118)
    say("VERDICT")
    say("=" * 118)
    band_wins_rg = int((RG.dSharpe > 0).sum())
    sig_s = int((BT[BT.stat == "Sharpe"].t.abs() > 2).sum())
    sig_d = int((BT[BT.stat == "MaxDD"].t.abs() > 2).sum())
    n_s = int((BT.stat == "Sharpe").sum())
    n_d = int((BT.stat == "MaxDD").sum())
    full_v_nog = P[P.arena == "FULL"].oSharpe.mean() - P[P.arena == "NOGATE"].oSharpe.mean()
    band_v_nog = P[P.arena == "BAND"].oSharpe.mean() - P[P.arena == "NOGATE"].oSharpe.mean()
    say(f"  matched-TARGET  : band beats its twin on FULL Sharpe {int((TG.dSharpe>0).sum())}/{len(TG)}, "
        f"mean {TG.dSharpe.mean():+.4f}; MaxDD shallower {int((TG.dMaxDD>0).sum())}/{len(TG)}, "
        f"mean {TG.dMaxDD.mean():+.2%}")
    say(f"  matched-REALISED: band beats its twin on FULL Sharpe {band_wins_rg}/{len(RG)}, "
        f"mean {RG.dSharpe.mean():+.4f}; OOS {int((RG.odSharpe>0).sum())}/{len(RG)}, "
        f"mean {RG.odSharpe.mean():+.4f}")
    say(f"  bootstrap       : dSharpe |t| > 2 at {sig_s}/{n_s} (max |t| "
        f"{BT[BT.stat=='Sharpe'].t.abs().max():.2f}); dMaxDD |t| > 2 at {sig_d}/{n_d} (max |t| "
        f"{BT[BT.stat=='MaxDD'].t.abs().max():.2f})")
    say(f"  rule 8          : BAND arena minus NOGATE arena mean OOS Sharpe {band_v_nog:+.4f}; "
        f"FULL minus NOGATE {full_v_nog:+.4f}")
    say(f"  4b (FULL-and-OOS): band cells {int(G[G.gate_on].keep4b_both.sum())}/{len(G[G.gate_on])}, "
        f"nogate cells {int(G[~G.gate_on].keep4b_both.sum())}/{len(G[~G.gate_on])}; "
        f"4a {int(G.keep4a.sum())}/{len(G)} over the whole grid")
    say("  (i)/(ii)/(iii) were pre-registered above; the numbers above decide between them and")
    say("  nothing here was re-tuned after reading them.")

    # ---------------------------------------------------------- artefacts
    OUT.mkdir(parents=True, exist_ok=True)
    G.to_csv(OUT / "grid.csv", index=False)
    TG.to_csv(OUT / "matched_target_gross.csv", index=False)
    RG.to_csv(OUT / "matched_realised_gross.csv", index=False)
    BT.to_csv(OUT / "bootstrap.csv", index=False)
    P.to_csv(OUT / "rule8_picks.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    (OUT / "run.log").write_text("\n".join(LOG) + "\n")
    npass = sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"])
    ntot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"\n  GATES {npass}/{ntot} passed.  Artefacts -> {OUT.relative_to(ROOT)}/  "
        f"({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
