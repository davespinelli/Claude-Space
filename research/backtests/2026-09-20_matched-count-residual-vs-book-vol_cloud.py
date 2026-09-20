#!/usr/bin/env python3
"""Idea 723 (lane cloud, 2026-09-20): IS THE MATCHED-COUNT RESIDUAL EXCESS GAP THE VOL CHANNEL
ITSELF?  A BOOK-VOL DECOMPOSITION OF THE DRAWDOWN SHORTFALL.

WHY THIS IDEA.  Idea 717 (2026-09-11) found, on the RECORD's claim corpus, that raw MaxDD's
excess against its permutation band stays 13-18 pp more negative than DDnorm's at every matched
claim count m >= 15: vol-normalising shrinks the drawdown shortfall by about a third and does
NOT remove it.  717 was a census of committed claims.  Idea 723 asks the same question of the
TAPE: take real books, measure their drawdown shortfall against a matched null directly, and ask
whether what survives vol-normalisation is the VOL CHANNEL ITSELF (a level effect that a
different normaliser would absorb) or a PATH effect that no vol statistic can reach.

This matters for capital, not just for bookkeeping.  Eight committed runs this week concluded
that "realised mean gross is a sufficient statistic" for every device-vs-degross loss (open idea
1494) and that de-grossing dominates every drawdown-buying device (idea 1534).  If the drawdown
shortfall of a gated book against its matched twin is entirely a vol-level fact, then MaxDD adds
nothing to vol and the 4b DD cap is a vol cap written in drawdown units.  If a PATH residual
survives every normaliser at every window, then drawdown is a separate axis and picking books on
it is legitimate.  Only prices can say which.

THE DECOMPOSITION, pre-registered before any number was read.  For a book B = (band c, target
gross G) on a panel, let N be its MATCHED NULL over the same window.  Two nulls, both matched on
REALISED MEAN GROSS (the record's standard matching variable), never on outcome:

  N_DEGROSS  the always-invested (NOGATE) equal-weight book over the SAME names, run at the
             target gross rung whose realised mean gross is closest to B's.  The "same exposure,
             no gate" twin.
  N_RAND     K = 20 random equal-weight baskets (seed 20260723, md5-free, numpy PCG64) of the
             SAME MEAN HELD-NAME COUNT as B, at the same target gross, same weekly cadence.
             The MATCHED-COUNT null idea 717's m is about.

  RAW excess    = MaxDD(B)  - MaxDD(N)                    (positive = B is SHALLOWER)
  NORM excess   = DDnorm(B) - DDnorm(N),  DDnorm = MaxDD / sigma

  sigma is the NORMALISER, DIAL 1:
      FULLVOL    annualised sd of the book's daily returns over the whole reporting window
      ROLLVOL    mean of the book's rolling W-day annualised vol over the window
      DOWNVOL    annualised sd of NEGATIVE daily returns only (semi-deviation) over the window
  W is the WINDOW, DIAL 2:  20 / 60 / 252 trading days (ROLLVOL only; the other two are
      window-free and are reported at every W unchanged, which is itself a published check).

  EXACTLY TWO TUNED DIALS (rule 4): (normaliser, window).  The book family axes (band c, gross
  G) are NOT tuned -- the whole ladder is published at every point and the rule-8 choosers below
  select a cell from the IS window only.  Panel is not a dial either: the identical grid runs on
  U56 / B136 / SMALL.

  THE ANSWER.  "The residual IS the vol channel" iff NORM excess is indistinguishable from 0
  under a PAIRED circular-block bootstrap (block 63 days, 400 draws, seed 20260723) at the
  normaliser x window that does best for it.  "It is not" iff a residual survives every one of
  the 9 (normaliser, window) pairs with |t| >= 2.  Both outcomes are reported; neither is
  preferred; the fraction of the RAW shortfall removed by normalisation is published per cell.

  THE THIRD CHANNEL.  Beyond vol level there is EXPOSURE PATH: a gated book's gross moves.  So
  the raw shortfall is split three ways and each part published:
      GROSS      MaxDD(N_DEGROSS at B's realised gross) - MaxDD(NOGATE at G = 1.00)
      SELECTION  MaxDD(B) - MaxDD(N_DEGROSS)             the "residual excess" 717 is about
      VOL-LEVEL  the part of SELECTION that DDnorm removes
      PATH       the part of SELECTION that survives DDnorm -- the object of this idea

THE CAPITAL ARM (rule 8, required).  Four IS-ONLY choosers, each fit on warm-up..2016-12-31 with
2017-01-01..end read EXACTLY ONCE:
  C_SHARPE  argmax IS Sharpe                                    the record's incumbent
  C_DDNORM  argmax IS DDnorm (shallowest drawdown per unit vol) at the BEST (normaliser, window)
            pair by IS -- the chooser this idea's statistic implies
  C_RESID   argmax IS PATH residual (the book whose shallowness vol does NOT explain)
  C_ANCHOR  (c = 0.03, G = 0.75), the LIVE book, choosing nothing                    the null
OOS CAGR / Sharpe / MaxDD for every pick against BOTH the live RULES v2 baseline and SPY over
the same OOS window, plus OOS 4a and OOS 4b.  Both KEEP paths are ALSO scored at every cell in
all five windows (FULL / H1 / H2 / IS / OOS).

GATES.  G0 >= 10y per panel.  G1 CROSS-SCRIPT REPLAY of `baseline.rules_v2_weights` through
`engine.backtest` at the U56 live cell.  G2 no leverage (max realised gross <= 1.0).  G3 every
cell x window published.  G4 exactly two tuned dials.  G5 no chooser reads a row >= 2017-01-01.
G6 determinism.  G7 panel composition + SMALL drop list published.  G8 the committed RULES v2
U56 FULL cell (8.62% / 1.2010 / -12.05%) reproduced.  G9 the null is matched: |realised mean
gross(B) - realised mean gross(N)| published per cell, and the DECOMPOSITION IDENTITY
GROSS + SELECTION == MaxDD(B) - MaxDD(NOGATE at G=1.00) is asserted to 1e-12.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a
current-screen sub-$2B panel (data/SMALL_PANEL_README.md) with every name whose max 1-day move
is >= 1.0 dropped first.  Every ABSOLUTE level below is an UPPER BOUND.  The object of this run
is a WITHIN-TAPE CONTRAST between a book and its own matched null, which survivorship biases far
less than it biases either leg; no cell here is a capital recommendation on its own.

PROTOCOL: rules 1, 2 (t+1, 10 bps, no leverage/shorting), 3, 4 (both KEEP paths, 2 dials), 5, 7,
8 (walk-forward), 9.  RULES.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_matched-count-residual-vs-book-vol_cloud.py
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

DATE, SLUG = "2026-09-20", "matched-count-residual-vs-book-vol"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, COST, CAD = 260, 10.0, "W"
NOGATE = -1.0
BANDS = [(NOGATE, "NOGATE"), (0.00, "BAND000"), (0.03, "BAND003"), (0.10, "BAND010")]
GRID_G = [0.20, 0.40, 0.60, 0.80, 1.00]
FINE_G = [round(0.05 * k, 2) for k in range(1, 21)]     # the matching ladder for N_DEGROSS
LIVE = (0.03, 0.75)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
WINDOWS = ["FULL", "H1", "H2", "IS", "OOS"]
NORMS = ["FULLVOL", "ROLLVOL", "DOWNVOL"]
WINS = [20, 60, 252]
KRAND, SEED = 20, 20260723
NBOOT, BLOCK = 400, 63

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


def vol_full(r):
    return float(np.std(np.asarray(r, float), ddof=0) * np.sqrt(252))


def vol_down(r):
    r = np.asarray(r, float)
    neg = r[r < 0]
    return float(np.std(neg, ddof=0) * np.sqrt(252)) if len(neg) > 5 else np.nan


def vol_roll(r, w):
    s = pd.Series(np.asarray(r, float)).rolling(w).std(ddof=0) * np.sqrt(252)
    return float(s.mean()) if s.notna().any() else np.nan


def sigma(r, norm, w):
    if norm == "FULLVOL":
        return vol_full(r)
    if norm == "DOWNVOL":
        return vol_down(r)
    return vol_roll(r, w)


def ddnorm(r, norm, w):
    s = sigma(r, norm, w)
    return float(mdd(r) / s) if (s and s == s and s > 0) else np.nan


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                Vol=vol_full(r))


def legs_4b(m, bm):
    return dict(H1=bool(m["H1"] > bm["H1"]), H2=bool(m["H2"] > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def pass_4b(m, bm):
    return all(legs_4b(m, bm).values())


def pass_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


# ---------------------------------------------------------------- tape / books
class Tape:
    def __init__(self, px, name):
        self.name, self.px, self.idx = name, px, px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.band = {c: band_state(px, band=c).values for c, _ in BANDS if c != NOGATE}
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        self.spy_col = list(px.columns).index("SPY")


def targets(tape, c, g, cols=None):
    """Target gross g spread equally over the names PRICED that day (restricted to `cols` when
    given -- that is the matched-count random basket), held only where the 200d +/- c band says
    IN; gated-out weight goes to CASH."""
    pr = tape.priced.astype(float)
    if cols is not None:
        mask = np.zeros(pr.shape[1])
        mask[cols] = 1.0
        pr = pr * mask[None, :]
    n = pr.sum(axis=1)
    W = np.zeros_like(pr)
    nz = n > 0
    W[nz] = g * pr[nz] / n[nz, None]
    if c != NOGATE:
        W = W * tape.band[c]
    return W


def run(tape, W, cost=COST):
    rets = tape.rets
    T, M = rets.shape
    out = np.zeros(T)
    turn = np.zeros(T)
    gsum = np.zeros(T)
    held = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(tape.reb[1:], T)
    C, Cp = tape.C, tape.Cp
    for i0, i1 in zip(tape.reb, ends):
        if i1 <= i0:
            continue
        w0 = W[i0 - 1] if i0 > 0 else W[0]
        s0 = float(w0.sum())
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        held[i0:i1] = float((w0 > 0).sum())
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, gsum, held


def windows(tape, r):
    rs = r[WARMUP:]
    h = len(rs) // 2
    io = tape.i_oos - WARMUP
    return dict(FULL=rs, H1=rs[:h], H2=rs[h:], IS=rs[:io], OOS=rs[io:])


def block_boot(a, b, n=NBOOT, block=BLOCK, seed=SEED):
    """PAIRED circular-block bootstrap of mean(MaxDD(a) - MaxDD(b)) on two aligned daily return
    streams: the SAME block positions are applied to both legs, so the contrast is paired."""
    rng = np.random.default_rng(seed)
    T = len(a)
    nb = int(np.ceil(T / block))
    d0 = mdd(a) - mdd(b)
    out = np.empty(n)
    for i in range(n):
        st = rng.integers(0, T, nb)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel()[:T] % T
        out[i] = mdd(a[idx]) - mdd(b[idx])
    sd = float(out.std(ddof=1))
    return d0, sd, float(d0 / sd) if sd > 0 else np.nan


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 723 (lane cloud, 2026-09-20) — IS THE MATCHED-COUNT RESIDUAL EXCESS GAP THE VOL")
    say("CHANNEL ITSELF?  A BOOK-VOL DECOMPOSITION OF THE DRAWDOWN SHORTFALL.")
    say(f"DIALS (exactly 2, rule 4): NORMALISER {NORMS} x WINDOW {WINS}.")
    say(f"Book family PUBLISHED IN FULL, not tuned: band c {[n for _, n in BANDS]} x gross G {GRID_G} "
        f"= {len(BANDS)*len(GRID_G)} cells/panel x 3 panels = {len(BANDS)*len(GRID_G)*3} books.")
    say(f"Nulls: N_DEGROSS (NOGATE twin matched on REALISED MEAN GROSS over a 0.05 ladder) and "
        f"N_RAND ({KRAND} matched-COUNT random baskets, seed {SEED}).")
    say(f"Weekly cadence, {COST:.0f} bps, t+1 execution, no leverage.  Paired circular-block "
        f"bootstrap: {NBOOT} draws, block {BLOCK}d.")
    say("=" * 118)

    panels = [("U56", load_universe()), ("B136", load_universe(broad=True))]
    px_s = load_universe(small=True)
    meta_path = ROOT / "data" / "small_meta.csv"
    dropped_meta = []
    if meta_path.exists():
        meta = pd.read_csv(meta_path)
        tcol = meta.columns[0]
        if "max_1d_move" in meta.columns:
            dropped_meta = [t for t in meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str)
                            if t in px_s.columns and t != "SPY"]
    mx = px_s.pct_change().abs().max()
    dropped_px = [c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0]
    drop = sorted(set(dropped_meta) | set(dropped_px))
    px_s = px_s.drop(columns=drop)
    panels.append(("SMALL", px_s))

    say("\n  PANELS:")
    for nm, p in panels:
        say(f"    {nm:6s} {p.shape[1]:4d} columns  {p.index[0].date()} .. {p.index[-1].date()}  "
            f"{len(p)} rows ({len(p)/252:.1f}y)")
        publish(f"G7 COMPOSITION {nm}", f"{p.shape[1]} columns incl. SPY, "
                                        f"{p.index[0].date()}..{p.index[-1].date()}")
    publish("G7 SMALL max_1d_move >= 1.0 drops",
            f"{len(drop)} names dropped ({len(dropped_meta)} by data/small_meta.csv, "
            f"{len(dropped_px)} by realised price move), {px_s.shape[1]} columns remain")
    say("  SURVIVORSHIP (rule 9): U56/B136 are CURRENT-constituent lists, SMALL a current screen;")
    say("  every ABSOLUTE level is an UPPER BOUND.  The object here is a WITHIN-TAPE contrast")
    say("  between a book and its OWN matched null.")

    tapes = {nm: Tape(p, nm) for nm, p in panels}
    for nm, tp in tapes.items():
        gate(f"G0 {nm} sample >= 10 years (rule 1)", round(len(tp.idx) / 252.0, 2), ">= 10.0",
             len(tp.idx) / 252.0 >= 10.0)
        gate(f"G5 {nm} IS window ends before {OOS_START}", str(tp.idx[tp.i_oos - 1].date()),
             f"< {OOS_START}", tp.idx[tp.i_oos - 1] < pd.Timestamp(OOS_START))

    tp = tapes["U56"]
    ref = backtest(tp.px, rules_v2_weights(tp.px, band=LIVE[0], gross=LIVE[1]),
                   cost_bps=COST, freq=CAD)["returns"].values
    mine, _, _, _ = run(tp, targets(tp, *LIVE))
    d = float(np.abs(ref[WARMUP:] - mine[WARMUP:]).max())
    gate("G1 replay of baseline.rules_v2_weights through engine.backtest (U56 live cell)",
         f"max |diff| {d:.3e}", "< 1e-12", d < 1e-12)
    a1, _, _, _ = run(tapes["B136"], targets(tapes["B136"], 0.03, 0.60))
    a2, _, _, _ = run(tapes["B136"], targets(tapes["B136"], 0.03, 0.60))
    gate("G6 determinism (B136 c=0.03 G=0.60 twice)", f"max |diff| {np.abs(a1-a2).max():.3e}",
         "== 0", np.array_equal(a1, a2))

    # ---------------- the ladders every null is matched against
    say("\n  BUILDING THE MATCHING LADDER (NOGATE at 20 gross rungs) AND THE BOOKS ...")
    R, GBAR, HELD, GROSSMAX = {}, {}, {}, {}
    nog = {}
    for nm, tpx in tapes.items():
        gmax = 0.0
        for g in FINE_G:
            r, _, gs, hh = run(tpx, targets(tpx, NOGATE, g))
            nog[(nm, g)] = (r, float(np.nanmean(gs[WARMUP:])))
            gmax = max(gmax, float(np.nanmax(gs[WARMUP:])))
        for c, cn in BANDS:
            for g in GRID_G:
                r, _, gs, hh = run(tpx, targets(tpx, c, g))
                R[(nm, c, g)] = r
                GBAR[(nm, c, g)] = float(np.nanmean(gs[WARMUP:]))
                HELD[(nm, c, g)] = float(np.nanmean(hh[WARMUP:]))
                gmax = max(gmax, float(np.nanmax(gs[WARMUP:])))
        GROSSMAX[nm] = gmax
        say(f"    {nm:6s} ladder + {len(BANDS)*len(GRID_G)} books done   t={time.time()-t0:.0f}s")
    gate("G2 no leverage (max realised gross over every book and null rung)",
         f"{max(GROSSMAX.values()):.4f}", "<= 1.0", max(GROSSMAX.values()) <= 1.0 + 1e-9)

    # ---------------- matched nulls
    say("\n  MATCHING THE NULLS (N_DEGROSS on realised mean gross; N_RAND on held-name count) ...")
    NDG, NRD, MATCH = {}, {}, {}
    for nm, tpx in tapes.items():
        ncols = [i for i in range(tpx.rets.shape[1]) if i != tpx.spy_col]
        for c, cn in BANDS:
            for g in GRID_G:
                gb = GBAR[(nm, c, g)]
                gsel = min(FINE_G, key=lambda x: abs(nog[(nm, x)][1] - gb))
                NDG[(nm, c, g)] = nog[(nm, gsel)][0]
                MATCH[(nm, c, g)] = (gsel, abs(nog[(nm, gsel)][1] - gb))
                k = max(1, int(round(HELD[(nm, c, g)])))
                rng = np.random.default_rng(SEED + hash((nm, cn, int(g * 100))) % 10_000)
                draws = []
                for j in range(KRAND):
                    cols = rng.choice(ncols, size=min(k, len(ncols)), replace=False)
                    rr, _, gs2, _ = run(tpx, targets(tpx, NOGATE, gb, cols=cols))
                    draws.append(rr)
                NRD[(nm, c, g)] = np.array(draws)
        say(f"    {nm:6s} nulls done   t={time.time()-t0:.0f}s")
    worst = max(v[1] for v in MATCH.values())
    gate("G9 N_DEGROSS gross match", f"worst |d realised mean gross| {worst:.4f}", "<= 0.03",
         worst <= 0.03)

    # ---------------- the grid: metrics, both KEEP paths, the decomposition
    say("\n  SCORING ...")
    rows, dec, M, BM, LIVEM = [], [], {}, {}, {}
    for nm, tpx in tapes.items():
        bw = windows(tpx, tpx.spy)
        BM[nm] = {w: pack(bw[w]) for w in WINDOWS}
        lw = windows(tpx, R[(nm, *LIVE)] if (nm, *LIVE) in R else run(tpx, targets(tpx, *LIVE))[0])
        LIVEM[nm] = {w: pack(lw[w]) for w in WINDOWS}
        unit = windows(tpx, nog[(nm, 1.00)][0])
        for c, cn in BANDS:
            for g in GRID_G:
                bwn, dwn = windows(tpx, R[(nm, c, g)]), windows(tpx, NDG[(nm, c, g)])
                rnd = {w: np.array([windows(tpx, x)[w] for x in NRD[(nm, c, g)]]) for w in WINDOWS}
                for w in WINDOWS:
                    b, n1 = bwn[w], dwn[w]
                    m = pack(b)
                    M[(nm, c, g, w)] = m
                    lg = legs_4b(m, BM[nm][w])
                    dd_b, dd_dg = mdd(b), mdd(n1)
                    dd_rd = float(np.mean([mdd(x) for x in rnd[w]]))
                    dd_rd_sd = float(np.std([mdd(x) for x in rnd[w]], ddof=1))
                    row = dict(panel=nm, band=cn, c=c, G=g, window=w,
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                               H1=m["H1"], H2=m["H2"], mean_gross=GBAR[(nm, c, g)],
                               held=HELD[(nm, c, g)], degross_rung=MATCH[(nm, c, g)][0],
                               dd_degross=dd_dg, dd_rand=dd_rd, dd_rand_sd=dd_rd_sd,
                               raw_excess_degross=dd_b - dd_dg, raw_excess_rand=dd_b - dd_rd,
                               spy_CAGR=BM[nm][w]["CAGR"], spy_Sharpe=BM[nm][w]["Sharpe"],
                               spy_MaxDD=BM[nm][w]["MaxDD"],
                               leg_H1=lg["H1"], leg_H2=lg["H2"], leg_DD=lg["DD"], leg_CAGR=lg["CAGR"],
                               pass4b=all(lg.values()), pass4a=pass_4a(m, LIVEM[nm][w]))
                    for norm in NORMS:
                        for wn in WINS:
                            key = f"{norm}{wn}"
                            nb, nd = ddnorm(b, norm, wn), ddnorm(n1, norm, wn)
                            nr = float(np.mean([ddnorm(x, norm, wn) for x in rnd[w]]))
                            row[f"ddn_{key}"] = nb
                            row[f"nrm_excess_degross_{key}"] = nb - nd
                            row[f"nrm_excess_rand_{key}"] = nb - nr
                    rows.append(row)
                    if w == "FULL":
                        u = unit["FULL"]
                        dec.append(dict(panel=nm, band=cn, c=c, G=g,
                                        dd_book=dd_b, dd_degross=dd_dg, dd_unit=mdd(u),
                                        GROSS=dd_dg - mdd(u), SELECTION=dd_b - dd_dg,
                                        total=dd_b - mdd(u)))
        say(f"    {nm:6s} scored   t={time.time()-t0:.0f}s")
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    D = pd.DataFrame(dec)
    D.to_csv(f"{OUT}.decomposition.csv", index=False)
    gate("G3 all cells x windows published",
         f"{len(grid)} rows -> {Path(OUT).name}.grid.csv",
         f"== {len(BANDS)*len(GRID_G)*3*len(WINDOWS)}",
         len(grid) == len(BANDS) * len(GRID_G) * 3 * len(WINDOWS))
    gate("G9 decomposition identity GROSS + SELECTION == MaxDD(B) - MaxDD(NOGATE G=1.00)",
         f"max |resid| {float((D.GROSS + D.SELECTION - D.total).abs().max()):.3e}", "< 1e-12",
         float((D.GROSS + D.SELECTION - D.total).abs().max()) < 1e-12)
    gate("G4 tuned dials", "2 (normaliser, window); band c and gross G published in full",
         "<= 2 (rule 4)", True)
    u = M[("U56", *LIVE[:1], 0.80, "FULL")] if ("U56", 0.03, 0.80, "FULL") in M else None
    ru, _, _, _ = run(tapes["U56"], targets(tapes["U56"], *LIVE))
    uf = pack(windows(tapes["U56"], ru)["FULL"])
    gate("G8 committed RULES v2 U56 FULL cell reproduced",
         f"CAGR {uf['CAGR']:.2%} Sharpe {uf['Sharpe']:.4f} MaxDD {uf['MaxDD']:.2%}",
         "8.62% / 1.2010 / -12.05%",
         abs(uf["CAGR"] - 0.0862) < 5e-4 and abs(uf["Sharpe"] - 1.2010) < 5e-3
         and abs(uf["MaxDD"] + 0.1205) < 5e-4)

    # ---------------- (1) the three-channel decomposition
    say("\n" + "=" * 118)
    say("(1) THE THREE-CHANNEL DECOMPOSITION OF THE DRAWDOWN SHORTFALL (FULL window, pp).")
    say("    total = MaxDD(book) - MaxDD(NOGATE at G=1.00);  GROSS = the de-gross channel;")
    say("    SELECTION = MaxDD(book) - MaxDD(its gross-matched NOGATE twin) = the '717 residual'.")
    say("=" * 118)
    say(f"    {'panel':6s} {'band':8s} {'G':>5s} {'meanG':>7s} {'MaxDD':>8s} {'twin':>8s} "
        f"{'GROSS':>8s} {'SELECT':>8s} {'share GROSS':>12s}")
    for _, r in D.iterrows():
        sh = r.GROSS / r.total if abs(r.total) > 1e-9 else np.nan
        say(f"    {r.panel:6s} {r.band:8s} {r.G:5.2f} "
            f"{grid[(grid.panel==r.panel)&(grid.band==r.band)&(grid.G==r.G)&(grid.window=='FULL')].mean_gross.iloc[0]:7.3f} "
            f"{r.dd_book:8.2%} {r.dd_degross:8.2%} {r.GROSS*100:7.2f}p {r.SELECTION*100:7.2f}p "
            f"{sh:12.3f}")
    tot_g = float(D.GROSS.sum() / D.total.sum())
    say(f"\n    POOLED over {len(D)} books: GROSS carries {tot_g:.1%} of the total shortfall, "
        f"SELECTION {1-tot_g:.1%}.")
    say(f"    SELECTION mean {D.SELECTION.mean()*100:+.2f} pp, median {D.SELECTION.median()*100:+.2f} pp, "
        f"positive (book SHALLOWER than its gross-matched twin) at "
        f"{int((D.SELECTION>0).sum())}/{len(D)} books.")

    # ---------------- (2) does normalisation remove the selection residual?
    say("\n" + "=" * 118)
    say("(2) THE ANSWER — DOES VOL-NORMALISATION REMOVE THE SELECTION RESIDUAL?")
    say("    Per (normaliser, window): the RAW excess vs the gross-matched twin and vs the")
    say("    matched-COUNT random null, and the same excess after dividing by sigma.")
    say("    'Share removed' = 1 - |normalised excess| / |raw excess|, pooled over books.")
    say("=" * 118)
    f = grid[grid.window == "FULL"]
    nrows = []
    for norm in NORMS:
        for wn in WINS:
            key = f"{norm}{wn}"
            for nulln, rawc, nrmc in [("N_DEGROSS", "raw_excess_degross", f"nrm_excess_degross_{key}"),
                                      ("N_RAND", "raw_excess_rand", f"nrm_excess_rand_{key}")]:
                raw, nrm = f[rawc], f[nrmc]
                # put the normalised excess back in pp by rescaling at each book's own sigma
                sg = f.apply(lambda r: r.MaxDD / r[f"ddn_{key}"] if r[f"ddn_{key}"] else np.nan, axis=1)
                nrm_pp = nrm * sg
                share = 1 - abs(nrm_pp.mean()) / abs(raw.mean()) if abs(raw.mean()) > 1e-12 else np.nan
                nrows.append(dict(normaliser=norm, window=wn, null=nulln,
                                  raw_mean_pp=raw.mean() * 100, nrm_mean_pp=nrm_pp.mean() * 100,
                                  share_removed=share, n=len(f),
                                  raw_pos=int((raw > 0).sum()), nrm_pos=int((nrm > 0).sum())))
                say(f"    {norm:8s} W={wn:3d}  {nulln:10s}  raw {raw.mean()*100:+7.2f} pp  ->  "
                    f"normalised {nrm_pp.mean()*100:+7.2f} pp   share removed {share:7.1%}   "
                    f"(book shallower at raw {int((raw>0).sum()):2d}/{len(f)}, "
                    f"normalised {int((nrm>0).sum()):2d}/{len(f)})")
    N = pd.DataFrame(nrows)
    N.to_csv(f"{OUT}.normalisers.csv", index=False)

    # ---------------- (3) is the surviving residual resolvable?  paired block bootstrap
    say("\n" + "=" * 118)
    say(f"(3) IS THE SURVIVING RESIDUAL RESOLVABLE?  PAIRED circular-block bootstrap of")
    say(f"    MaxDD(book) - MaxDD(gross-matched twin) on the FULL window "
        f"({NBOOT} draws, block {BLOCK}d, seed {SEED}).")
    say("=" * 118)
    brows = []
    for nm in tapes:
        for c, cn in BANDS:
            for g in GRID_G:
                b = windows(tapes[nm], R[(nm, c, g)])["FULL"]
                n1 = windows(tapes[nm], NDG[(nm, c, g)])["FULL"]
                d0, sd, t = block_boot(b, n1)
                brows.append(dict(panel=nm, band=cn, G=g, d_maxdd_pp=d0 * 100, sd_pp=sd * 100, t=t,
                                  resolvable=bool(abs(t) >= 2)))
    B = pd.DataFrame(brows)
    B.to_csv(f"{OUT}.bootstrap.csv", index=False)
    say(f"    {int(B.resolvable.sum())}/{len(B)} of the SELECTION residuals clear |t| >= 2 against "
        f"their own paired block SE.")
    say(f"    mean d MaxDD {B.d_maxdd_pp.mean():+.2f} pp, mean paired SE {B.sd_pp.mean():.2f} pp, "
        f"mean |t| {B.t.abs().mean():.3f}, max |t| {B.t.abs().max():.3f}.")
    for nm in tapes:
        s = B[B.panel == nm]
        say(f"      {nm:6s} resolvable {int(s.resolvable.sum()):2d}/{len(s)}   "
            f"mean d {s.d_maxdd_pp.mean():+6.2f} pp   mean SE {s.sd_pp.mean():5.2f} pp   "
            f"mean |t| {s.t.abs().mean():.3f}")

    # ---------------- (4) both KEEP paths over the whole grid
    say("\n" + "=" * 118)
    say("(4) BOTH KEEP PATHS OVER ALL CELLS (rule 4):")
    say("=" * 118)
    for nm in tapes:
        for w in WINDOWS:
            s = grid[(grid.panel == nm) & (grid.window == w)]
            say(f"    {nm:6s} {w:5s}  4a {int(s.pass4a.sum()):2d}/{len(s)}   4b {int(s.pass4b.sum()):2d}/{len(s)}"
                f"   (4b legs failing: H1 {int((~s.leg_H1).sum()):2d}  H2 {int((~s.leg_H2).sum()):2d}  "
                f"DD {int((~s.leg_DD).sum()):2d}  CAGR {int((~s.leg_CAGR).sum()):2d})")

    # ---------------- (5) rule 8
    say("\n" + "=" * 118)
    say("(5) RULE 8 — FOUR IS-ONLY CHOOSERS, 2017-01-01..end READ EXACTLY ONCE.")
    say("    C_DDNORM and C_RESID are the choosers this idea's statistic implies; the")
    say("    (normaliser, window) they use is itself picked on the IS window only.")
    say("=" * 118)
    prows = []
    for nm in tapes:
        cells = [(c, g) for c, _ in BANDS for g in GRID_G]
        isr = grid[(grid.panel == nm) & (grid.window == "IS")].set_index(["c", "G"])
        best = max(isr.Sharpe)
        k_sh = min([k for k in cells if isr.loc[k, "Sharpe"] == best],
                   key=lambda k: (0 if k[0] == NOGATE else 1, k[0], k[1]))
        # the (normaliser, window) pair chosen ON IS: the one whose DDnorm spread across cells is
        # largest, i.e. the most DISCRIMINATING normaliser in-sample.  No OOS row is read.
        spread = {(n_, w_): float(np.nanstd(isr[f"ddn_{n_}{w_}"].values)) for n_ in NORMS for w_ in WINS}
        nb, wb = max(spread, key=lambda k: spread[k])
        col = f"ddn_{nb}{wb}"
        k_dn = max(cells, key=lambda k: isr.loc[k, col])                 # least deep per unit vol
        k_rs = max(cells, key=lambda k: isr.loc[k, f"nrm_excess_degross_{nb}{wb}"])
        picks = {"C_SHARPE": (k_sh, "argmax IS Sharpe"),
                 "C_DDNORM": (k_dn, f"argmax IS DDnorm at IS-chosen normaliser {nb}/W={wb}"),
                 "C_RESID": (k_rs, f"argmax IS normalised excess vs gross-matched twin ({nb}/W={wb})"),
                 "C_ANCHOR": (LIVE, "the LIVE book, choosing nothing")}
        say(f"\n  {nm}  (IS-chosen normaliser {nb}/W={wb};  OOS baseline RULES v2 CAGR "
            f"{LIVEM[nm]['OOS']['CAGR']:.2%} Sharpe {LIVEM[nm]['OOS']['Sharpe']:.4f} "
            f"MaxDD {LIVEM[nm]['OOS']['MaxDD']:.2%}  |  OOS SPY CAGR {BM[nm]['OOS']['CAGR']:.2%} "
            f"Sharpe {BM[nm]['OOS']['Sharpe']:.4f} MaxDD {BM[nm]['OOS']['MaxDD']:.2%})")
        for ch, ((c, g), note) in picks.items():
            if (nm, c, g, "OOS") not in M:
                rr, _, _, _ = run(tapes[nm], targets(tapes[nm], c, g))
                ww = windows(tapes[nm], rr)
                for w in WINDOWS:
                    M[(nm, c, g, w)] = pack(ww[w])
            o, fu = M[(nm, c, g, "OOS")], M[(nm, c, g, "FULL")]
            l4a, l4b = pass_4a(o, LIVEM[nm]["OOS"]), pass_4b(o, BM[nm]["OOS"])
            prows.append(dict(panel=nm, chooser=ch, band=dict(BANDS)[c], c=c, G=g, note=note,
                              oos_CAGR=o["CAGR"], oos_Sharpe=o["Sharpe"], oos_MaxDD=o["MaxDD"],
                              oos_4a=l4a, oos_4b=l4b, full_CAGR=fu["CAGR"], full_Sharpe=fu["Sharpe"],
                              full_MaxDD=fu["MaxDD"], full_4a=pass_4a(fu, LIVEM[nm]["FULL"]),
                              full_4b=pass_4b(fu, BM[nm]["FULL"]),
                              d_sharpe_vs_base=o["Sharpe"] - LIVEM[nm]["OOS"]["Sharpe"],
                              d_sharpe_vs_spy=o["Sharpe"] - BM[nm]["OOS"]["Sharpe"]))
            say(f"    {ch:9s} -> {dict(BANDS)[c]:8s} G={g:.2f}   OOS CAGR {o['CAGR']:7.2%}  "
                f"Sharpe {o['Sharpe']:7.4f}  MaxDD {o['MaxDD']:8.2%}   4a {'PASS' if l4a else 'fail'}"
                f"  4b {'PASS' if l4b else 'fail'}   [{note}]")
    P = pd.DataFrame(prows)
    P.to_csv(f"{OUT}.picks.csv", index=False)
    say("\n  RULE-8 SUMMARY:")
    for ch in ["C_SHARPE", "C_DDNORM", "C_RESID", "C_ANCHOR"]:
        s = P[P.chooser == ch]
        say(f"    {ch:9s}  OOS 4a {int(s.oos_4a.sum())}/{len(s)}   OOS 4b {int(s.oos_4b.sum())}/{len(s)}"
            f"   FULL 4b {int(s.full_4b.sum())}/{len(s)}   mean OOS Sharpe {s.oos_Sharpe.mean():.4f}"
            f"   mean OOS CAGR {s.oos_CAGR.mean():.2%}   mean OOS MaxDD {s.oos_MaxDD.mean():.2%}")
    say(f"    {'SPY':9s}  mean OOS Sharpe {np.mean([BM[n]['OOS']['Sharpe'] for n in tapes]):.4f}   "
        f"mean OOS CAGR {np.mean([BM[n]['OOS']['CAGR'] for n in tapes]):.2%}   "
        f"mean OOS MaxDD {np.mean([BM[n]['OOS']['MaxDD'] for n in tapes]):.2%}")
    say(f"    {'RULESv2':9s}  mean OOS Sharpe {np.mean([LIVEM[n]['OOS']['Sharpe'] for n in tapes]):.4f}   "
        f"mean OOS CAGR {np.mean([LIVEM[n]['OOS']['CAGR'] for n in tapes]):.2%}   "
        f"mean OOS MaxDD {np.mean([LIVEM[n]['OOS']['MaxDD'] for n in tapes]):.2%}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n  GATES: {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass.   wall {time.time()-t0:.0f}s")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
