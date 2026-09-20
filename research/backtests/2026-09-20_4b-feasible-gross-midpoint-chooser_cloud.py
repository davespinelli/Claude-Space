#!/usr/bin/env python3
"""Idea 1705 (lane cloud, 2026-09-20): IS THE 4b-FEASIBLE GROSS INTERVAL MIDPOINT A BETTER
IS CHOOSER THAN IS-SHARPE ARGMAX?

WHY THIS IDEA.  Two committed findings set it up:
  * idea 1695 (2026-09-20, lane cloud) found 4b is operationally an INTERVAL ON GROSS --
    [g_CAGR, g_DD] -- of mean feasible width 1.11 of 20 rungs, EMPTY at 22 of 45 (panel, form,
    window) triples, because the CAGR floor passes on an UPPER set of G and the DD cap on a
    LOWER set while the two Sharpe legs are near gross-invariant.
  * idea 720 / 1713 (2026-09-20) found argmax-IS-Sharpe pins to G = 0.95-1.00 on essentially
    every panel, because IS Sharpe moves 0.0015-0.0106 over the WHOLE gross ladder against a
    leave-one-year-out SD of 0.09-0.25, while the 4b passes sit at G = 0.50-0.75.  That is why
    0 of 100 committed rule-8 picks clear 4a.

If 4b is an interval on gross and IS Sharpe cannot see gross, then the RIGHT IS-only chooser is
not an argmax of a gross-blind objective at all: it is the MIDPOINT of the interval the bar
itself defines, computed on the IS window only.  That chooser has no free parameter beyond the
two dials, it is legal under rule 8, and it aims at the centre of the feasible set rather than
at its edge.  This run prices it.

THE DESIGN.  Exactly two tuned dials (PROTOCOL rule 4), EVERY grid point published:

  c   {NOGATE, 0.00, 0.03, 0.10}          DIAL 1 -- the 200d MA band.  NOGATE = always invested
                                          (no MA gate at all); 0.00 = plain 200d MA, no
                                          hysteresis; 0.03 = the LIVE RULES v2 band; 0.10 = the
                                          2026-09-19 committed rule-8 pick.
  G   0.05, 0.10, ..., 1.00               DIAL 2 -- target gross.  20 rungs, no leverage.
                                          0.75 is LIVE.

  4 x 20 = 80 cells per panel x 3 panels (U56 / B136 / SMALL) = 240 books, each resolved in
  FIVE windows (FULL / H1 / H2 / IS / OOS) -> 1,200 cell-windows, ALL written to grid.csv with
  both KEEP paths and all four 4b legs.  PANEL IS NOT A DIAL: the identical grid runs on all
  three and no panel is selected on its own result.

THE CHOOSERS (rule 8; each fit on warm-up..2016-12-31 ONLY, 2017-01-01..end read EXACTLY ONCE).
A chooser is the object under study here, not a tuned parameter -- all five see the same grid:

  C_SHARPE   argmax IS Sharpe.                               The record's incumbent chooser.
  C_MID      per band c, the IS-4b-FEASIBLE G set {G : all four 4b legs pass on the IS window
             against SPY on the IS window}; its interval [g_lo, g_hi]; the MIDPOINT RUNG
             (index (i_lo + i_hi) // 2, i.e. ties to the LOWER rung).  Among bands with a
             non-empty feasible set, take the one whose own midpoint has the highest IS Sharpe.
             THE IDEA'S CHOOSER.
  C_MIDW     same midpoints, but the band is taken by WIDEST feasible interval (ties to the
             smallest c, NOGATE first).  A second reading of "the midpoint chooser" that never
             consults Sharpe at all.
  C_LO       the LOWEST feasible rung (the interval's left edge).  Control: isolates whether any
             gain of C_MID is "the interval" or merely "de-grossing".
  C_ANCHOR   (c = 0.03, G = 0.75), the LIVE book, choosing nothing.                  The null.

  Fallback, declared before the read: if a chooser's feasible set is EMPTY on every band, it
  falls back to C_SHARPE's pick and the row is flagged EMPTY_FALLBACK.

WHAT IS MEASURED, PRE-REGISTERED BEFORE ANY NUMBER WAS READ.
  (A) THE HEADLINE.  Per (panel, chooser): OOS CAGR / Sharpe / MaxDD of the picked book against
      BOTH the live RULES v2 baseline and SPY over the SAME OOS window, plus the OOS 4a and OOS
      4b verdicts.  C_MID beats C_SHARPE only if it wins on PASS COUNT or on OOS Sharpe/CAGR at
      no worse drawdown.  15 picks (3 panels x 5 choosers).
  (B) THE MECHANISM.  Where each chooser lands on the gross ladder (the 720 complaint), and
      whether the IS-feasible interval CONTAINS the OOS-feasible interval -- i.e. whether the
      IS window can locate the OOS feasible set at all.  Published per (panel, band):
      IS interval, OOS interval, overlap, and the IS midpoint's OOS 4b verdict.
  (C) THE ORACLE GAP.  The best OOS cell per panel (not reachable in practice) is published
      beside the picks, so the chooser's loss is quoted against what was there to win.
  (D) BOTH KEEP PATHS at every one of the 240 cells in all five windows (rule 4).

GATES.  G0 >= 10y per panel (rule 1).  G1 CROSS-SCRIPT REPLAY: the U56 (c=0.03, G=0.75) cell
reproduces `baseline.rules_v2_weights` through `engine.backtest` to floating point.  G2 no
leverage / no shorting (max realised gross <= 1.0).  G3 all 240 cells x 5 windows published.
G4 exactly two tuned dials.  G5 NO chooser reads a row on or after 2017-01-01 (asserted by
construction: choosers see only the IS slice).  G6 determinism (one cell run twice).  G7 panel
composition published.  G8 the committed RULES v2 FULL cells (U56 8.62% / 1.2010 / -12.05%) are
reproduced.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a
current-screen sub-$2B panel (data/SMALL_PANEL_README.md) with every name whose max 1-day move
is >= 1.0 dropped first.  Every ABSOLUTE level below is therefore an UPPER BOUND.  What this run
reads is a CONTRAST BETWEEN TWO CHOOSERS on one tape, which survivorship biases far less than it
biases either chooser's level; no cell here is a capital recommendation on its own.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 5 (one idea, one script); rule 7 (honest report);
rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md, scan.py, bot.py and baseline.py
are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_4b-feasible-gross-midpoint-chooser_cloud.py
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

DATE, SLUG = "2026-09-20", "4b-feasible-gross-midpoint-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
COST = 10.0
CAD = "W"
NOGATE = -1.0
BANDS = [(NOGATE, "NOGATE"), (0.00, "BAND000"), (0.03, "BAND003"), (0.10, "BAND010")]
GRID_G = [round(0.05 * k, 2) for k in range(1, 21)]
LIVE = (0.03, 0.75)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
WINDOWS = ["FULL", "H1", "H2", "IS", "OOS"]
CHOOSERS = ["C_SHARPE", "C_MID", "C_MIDW", "C_LO", "C_ANCHOR"]

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


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_4b(m, bm):
    return dict(H1=bool(m["H1"] > bm["H1"]), H2=bool(m["H2"] > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def pass_4b(m, bm):
    return all(legs_4b(m, bm).values())


def pass_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


# ---------------------------------------------------------------- tape and book
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


def targets(tape, c, g):
    """RULES v2's shape: target gross g spread equally over the names PRICED that day, held only
    where the 200d +/- c band says IN; gated-out weight goes to CASH (never re-spread)."""
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
    close of t-1 applied from t, drift between rebalances, un-invested NAV earns 0.00%,
    turnover charged at `cost` bps."""
    rets = tape.rets
    T, M = rets.shape
    out = np.zeros(T)
    turn = np.zeros(T)
    gsum = np.zeros(T)
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
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, gsum


def windows(tape, r):
    rs = r[WARMUP:]
    h = len(rs) // 2
    io = tape.i_oos - WARMUP
    return dict(FULL=rs, H1=rs[:h], H2=rs[h:], IS=rs[:io], OOS=rs[io:])


# ---------------------------------------------------------------- choosers (rule 8, IS only)
def _tie(k):
    """Deterministic sort key over cells (c, G): NOGATE first on band, then smallest c, then G."""
    return (0 if k[0] == NOGATE else 1, k[0], k[1])


def interval(feas):
    """[i_lo, i_hi] over GRID_G indices of a feasible G set, its midpoint index (ties LOW),
    width and contiguity.  feas: list of G values."""
    if not feas:
        return None
    ii = sorted(GRID_G.index(g) for g in feas)
    lo, hi = ii[0], ii[-1]
    return dict(lo=lo, hi=hi, mid=(lo + hi) // 2, width=hi - lo + 1, n=len(ii),
                contiguous=(hi - lo + 1 == len(ii)))


def choose(panel_cells, isp, feas_by_band):
    """All five choosers on the IS window only.  Returns {chooser: (cell, note)}."""
    out = {}
    best = max(isp[k]["Sharpe"] for k in panel_cells)
    k_sh = min([k for k in panel_cells if isp[k]["Sharpe"] == best], key=_tie)
    out["C_SHARPE"] = (k_sh, "argmax IS Sharpe")

    iv = {c: interval(feas_by_band[c]) for c, _ in BANDS}
    live_bands = [c for c in iv if iv[c] is not None]

    if live_bands:
        mids = {c: (c, GRID_G[iv[c]["mid"]]) for c in live_bands}
        b = max(live_bands, key=lambda c: (isp[mids[c]]["Sharpe"], -_tie((c, 0))[1]))
        top = max(isp[mids[c]]["Sharpe"] for c in live_bands)
        b = min([c for c in live_bands if isp[mids[c]]["Sharpe"] == top], key=lambda c: _tie((c, 0)))
        out["C_MID"] = (mids[b], f"IS-feasible interval midpoint, band by IS Sharpe at midpoint "
                                 f"(interval {GRID_G[iv[b]['lo']]:.2f}-{GRID_G[iv[b]['hi']]:.2f})")
        wmax = max(iv[c]["width"] for c in live_bands)
        bw = min([c for c in live_bands if iv[c]["width"] == wmax], key=lambda c: _tie((c, 0)))
        out["C_MIDW"] = (mids[bw], f"IS-feasible interval midpoint, band by WIDEST interval "
                                   f"(width {wmax} rungs)")
        out["C_LO"] = ((bw, GRID_G[iv[bw]["lo"]]), "lowest feasible rung of the widest interval")
    else:
        out["C_MID"] = (k_sh, "EMPTY_FALLBACK -> C_SHARPE (no band has an IS-feasible rung)")
        out["C_MIDW"] = (k_sh, "EMPTY_FALLBACK -> C_SHARPE")
        out["C_LO"] = (k_sh, "EMPTY_FALLBACK -> C_SHARPE")
    out["C_ANCHOR"] = (LIVE, "the LIVE book, choosing nothing")
    return out, iv


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1705 (lane cloud, 2026-09-20) — IS THE 4b-FEASIBLE GROSS INTERVAL MIDPOINT A BETTER")
    say("IS CHOOSER THAN IS-SHARPE ARGMAX?")
    say(f"DIALS: band c {[n for _, n in BANDS]} x gross G {GRID_G[0]:.2f}..{GRID_G[-1]:.2f} step 0.05 "
        f"({len(GRID_G)} rungs) = {len(BANDS)*len(GRID_G)} cells/panel.")
    say(f"Panels U56 / B136 / SMALL (published, NOT a dial).  Weekly cadence, {COST:.0f} bps, t+1, "
        f"no leverage.  {len(BANDS)*len(GRID_G)*3} books x {len(WINDOWS)} windows = "
        f"{len(BANDS)*len(GRID_G)*3*len(WINDOWS)} cell-windows, all published.")
    say("=" * 118)

    # ---- panels
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
    say("  every ABSOLUTE level below is an UPPER BOUND.  The object of the run is the CONTRAST")
    say("  between two IS-only choosers on one tape.")

    tapes = {nm: Tape(p, nm) for nm, p in panels}
    for nm, tp in tapes.items():
        gate(f"G0 {nm} sample >= 10 years (rule 1)", round(len(tp.idx) / 252.0, 2), ">= 10.0",
             len(tp.idx) / 252.0 >= 10.0)
        gate(f"G5 {nm} IS window ends before {OOS_START}", str(tp.idx[tp.i_oos - 1].date()),
             f"< {OOS_START}", tp.idx[tp.i_oos - 1] < pd.Timestamp(OOS_START))

    # ---- G1 cross-script replay
    tp = tapes["U56"]
    ref = backtest(tp.px, rules_v2_weights(tp.px, band=LIVE[0], gross=LIVE[1]),
                   cost_bps=COST, freq=CAD)["returns"].values
    mine, _, _ = run(tp, targets(tp, *LIVE))
    d = float(np.abs(ref[WARMUP:] - mine[WARMUP:]).max())
    gate("G1 replay of baseline.rules_v2_weights through engine.backtest (U56 live cell)",
         f"max |diff| {d:.3e}", "< 1e-12", d < 1e-12)

    # ---- G6 determinism
    a, _, _ = run(tapes["B136"], targets(tapes["B136"], 0.03, 0.50))
    b, _, _ = run(tapes["B136"], targets(tapes["B136"], 0.03, 0.50))
    gate("G6 determinism (B136 c=0.03 G=0.50 run twice)", f"max |diff| {np.abs(a-b).max():.3e}",
         "== 0", np.array_equal(a, b))

    # ---- the grid
    say("\n  RUNNING THE GRID ...")
    rows, M, BM, LIVEM, GROSSMAX = [], {}, {}, {}, {}
    for nm, tp in tapes.items():
        bw = windows(tp, tp.spy)
        BM[nm] = {w: pack(bw[w]) for w in WINDOWS}
        rl, _, _ = run(tp, targets(tp, *LIVE))
        lw = windows(tp, rl)
        LIVEM[nm] = {w: pack(lw[w]) for w in WINDOWS}
        gmax = 0.0
        for c, cn in BANDS:
            for g in GRID_G:
                r, turn, gs = run(tp, targets(tp, c, g))
                gmax = max(gmax, float(np.nanmax(gs[WARMUP:])))
                ww = windows(tp, r)
                for w in WINDOWS:
                    m = pack(ww[w])
                    lg = legs_4b(m, BM[nm][w])
                    M[(nm, c, g, w)] = m
                    rows.append(dict(panel=nm, band=cn, c=c, G=g, window=w,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=m["H1"], H2=m["H2"],
                                     spy_CAGR=BM[nm][w]["CAGR"], spy_Sharpe=BM[nm][w]["Sharpe"],
                                     spy_MaxDD=BM[nm][w]["MaxDD"],
                                     leg_H1=lg["H1"], leg_H2=lg["H2"], leg_DD=lg["DD"],
                                     leg_CAGR=lg["CAGR"], pass4b=all(lg.values()),
                                     pass4a=pass_4a(m, LIVEM[nm][w]),
                                     turnover_yr=float(turn[WARMUP:].sum()) / (len(turn[WARMUP:]) / 252),
                                     mean_gross=float(np.nanmean(gs[WARMUP:]))))
        GROSSMAX[nm] = gmax
        say(f"    {nm:6s} done  ({len(BANDS)*len(GRID_G)} cells)  t={time.time()-t0:.0f}s")
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G3 all cells x windows published", f"{len(grid)} rows -> {Path(OUT).name}.grid.csv",
         f"== {len(BANDS)*len(GRID_G)*3*len(WINDOWS)}",
         len(grid) == len(BANDS) * len(GRID_G) * 3 * len(WINDOWS))
    gate("G2 no leverage (max realised gross over all cells)",
         f"{max(GROSSMAX.values()):.4f}", "<= 1.0", max(GROSSMAX.values()) <= 1.0 + 1e-9)
    gate("G4 tuned dials", "2 (band c, gross G)", "<= 2 (rule 4)", True)
    u = M[("U56", *LIVE, "FULL")]
    gate("G8 committed RULES v2 U56 FULL cell reproduced",
         f"CAGR {u['CAGR']:.2%} Sharpe {u['Sharpe']:.4f} MaxDD {u['MaxDD']:.2%}",
         "8.62% / 1.2010 / -12.05%",
         abs(u["CAGR"] - 0.0862) < 5e-4 and abs(u["Sharpe"] - 1.2010) < 5e-3
         and abs(u["MaxDD"] + 0.1205) < 5e-4)

    # ---- (D) grid-wide KEEP census
    say("\n" + "=" * 118)
    say("(D) BOTH KEEP PATHS OVER ALL 240 CELLS (rule 4).  Counts of cells PASSING, by window:")
    say("=" * 118)
    cens = []
    for nm in tapes:
        for w in WINDOWS:
            s = grid[(grid.panel == nm) & (grid.window == w)]
            cens.append(dict(panel=nm, window=w, n=len(s), pass4a=int(s.pass4a.sum()),
                             pass4b=int(s.pass4b.sum())))
            say(f"    {nm:6s} {w:5s}  4a {int(s.pass4a.sum()):3d}/{len(s)}   "
                f"4b {int(s.pass4b.sum()):3d}/{len(s)}   "
                f"(legs failing 4b: H1 {int((~s.leg_H1).sum()):3d}  H2 {int((~s.leg_H2).sum()):3d}  "
                f"DD {int((~s.leg_DD).sum()):3d}  CAGR {int((~s.leg_CAGR).sum()):3d})")
    pd.DataFrame(cens).to_csv(f"{OUT}.keep_census.csv", index=False)

    # ---- (B) the feasible intervals, IS vs OOS
    say("\n" + "=" * 118)
    say("(B) THE MECHANISM — the 4b-FEASIBLE GROSS INTERVAL, IS vs OOS, per (panel, band).")
    say("    IS = warm-up..2016-12-31 (what a chooser may see).  OOS = 2017-01-01..end (read once).")
    say("=" * 118)
    ivrows = []
    feas = {}
    for nm in tapes:
        for c, cn in BANDS:
            fis = [g for g in GRID_G if M[(nm, c, g, "IS")] and pass_4b(M[(nm, c, g, "IS")], BM[nm]["IS"])]
            foos = [g for g in GRID_G if pass_4b(M[(nm, c, g, "OOS")], BM[nm]["OOS"])]
            feas[(nm, c)] = fis
            a_, b_ = interval(fis), interval(foos)
            mid = GRID_G[a_["mid"]] if a_ else None
            ov = len(set(fis) & set(foos))
            ivrows.append(dict(panel=nm, band=cn, is_n=len(fis), is_lo=min(fis) if fis else None,
                               is_hi=max(fis) if fis else None, is_mid=mid,
                               is_contiguous=a_["contiguous"] if a_ else None,
                               oos_n=len(foos), oos_lo=min(foos) if foos else None,
                               oos_hi=max(foos) if foos else None, overlap=ov,
                               mid_passes_oos=(mid in foos) if mid is not None else None))
            say(f"    {nm:6s} {cn:8s} IS  n={len(fis):2d} "
                f"[{(min(fis) if fis else float('nan')):.2f},{(max(fis) if fis else float('nan')):.2f}] "
                f"mid {('%.2f' % mid) if mid is not None else ' -- '}"
                f"{'' if (a_ is None or a_['contiguous']) else ' (NON-CONTIGUOUS)'}"
                f"   |  OOS n={len(foos):2d} "
                f"[{(min(foos) if foos else float('nan')):.2f},{(max(foos) if foos else float('nan')):.2f}]"
                f"   overlap {ov:2d}   IS-mid clears OOS 4b: "
                f"{'YES' if (mid is not None and mid in foos) else ('no' if mid is not None else 'n/a')}")
    pd.DataFrame(ivrows).to_csv(f"{OUT}.intervals.csv", index=False)

    # ---- (A) the choosers
    say("\n" + "=" * 118)
    say("(A) RULE 8 — FIVE IS-ONLY CHOOSERS, 2017-01-01..end READ EXACTLY ONCE.")
    say("=" * 118)
    prows = []
    for nm, tp in tapes.items():
        cells = [(c, g) for c, _ in BANDS for g in GRID_G]
        isp = {(c, g): M[(nm, c, g, "IS")] for (c, g) in cells}
        picks, iv = choose(cells, isp, {c: feas[(nm, c)] for c, _ in BANDS})
        say(f"\n  {nm}  (OOS baseline RULES v2: CAGR {LIVEM[nm]['OOS']['CAGR']:.2%} "
            f"Sharpe {LIVEM[nm]['OOS']['Sharpe']:.4f} MaxDD {LIVEM[nm]['OOS']['MaxDD']:.2%}"
            f"  |  OOS SPY: CAGR {BM[nm]['OOS']['CAGR']:.2%} Sharpe {BM[nm]['OOS']['Sharpe']:.4f} "
            f"MaxDD {BM[nm]['OOS']['MaxDD']:.2%})")
        for ch in CHOOSERS:
            (c, g), note = picks[ch]
            cn = dict(BANDS)[c]
            o, f = M[(nm, c, g, "OOS")], M[(nm, c, g, "FULL")]
            l4b, l4a = pass_4b(o, BM[nm]["OOS"]), pass_4a(o, LIVEM[nm]["OOS"])
            prows.append(dict(panel=nm, chooser=ch, band=cn, c=c, G=g, note=note,
                              is_Sharpe=isp[(c, g)]["Sharpe"],
                              oos_CAGR=o["CAGR"], oos_Sharpe=o["Sharpe"], oos_MaxDD=o["MaxDD"],
                              oos_4a=l4a, oos_4b=l4b,
                              full_CAGR=f["CAGR"], full_Sharpe=f["Sharpe"], full_MaxDD=f["MaxDD"],
                              full_4a=pass_4a(f, LIVEM[nm]["FULL"]), full_4b=pass_4b(f, BM[nm]["FULL"]),
                              d_sharpe_vs_base=o["Sharpe"] - LIVEM[nm]["OOS"]["Sharpe"],
                              d_sharpe_vs_spy=o["Sharpe"] - BM[nm]["OOS"]["Sharpe"],
                              d_cagr_vs_spy=o["CAGR"] - BM[nm]["OOS"]["CAGR"]))
            say(f"    {ch:9s} -> {cn:8s} G={g:.2f}   OOS CAGR {o['CAGR']:7.2%}  Sharpe {o['Sharpe']:7.4f}"
                f"  MaxDD {o['MaxDD']:8.2%}   4a {'PASS' if l4a else 'fail'}  4b "
                f"{'PASS' if l4b else 'fail'}   [{note}]")
        # (C) the oracle
        best = max(cells, key=lambda k: M[(nm, k[0], k[1], "OOS")]["Sharpe"])
        ob = M[(nm, best[0], best[1], "OOS")]
        n4b = [k for k in cells if pass_4b(M[(nm, k[0], k[1], "OOS")], BM[nm]["OOS"])]
        say(f"    {'ORACLE':9s} -> {dict(BANDS)[best[0]]:8s} G={best[1]:.2f}   OOS CAGR {ob['CAGR']:7.2%}"
            f"  Sharpe {ob['Sharpe']:7.4f}  MaxDD {ob['MaxDD']:8.2%}   "
            f"[NOT REACHABLE: argmax OOS Sharpe.  {len(n4b)}/{len(cells)} cells clear OOS 4b]")
        prows.append(dict(panel=nm, chooser="ORACLE_OOS", band=dict(BANDS)[best[0]], c=best[0],
                          G=best[1], note="argmax OOS Sharpe, NOT reachable",
                          is_Sharpe=isp[best]["Sharpe"], oos_CAGR=ob["CAGR"], oos_Sharpe=ob["Sharpe"],
                          oos_MaxDD=ob["MaxDD"], oos_4a=pass_4a(ob, LIVEM[nm]["OOS"]),
                          oos_4b=pass_4b(ob, BM[nm]["OOS"]),
                          full_CAGR=M[(nm, best[0], best[1], "FULL")]["CAGR"],
                          full_Sharpe=M[(nm, best[0], best[1], "FULL")]["Sharpe"],
                          full_MaxDD=M[(nm, best[0], best[1], "FULL")]["MaxDD"],
                          full_4a=pass_4a(M[(nm, best[0], best[1], "FULL")], LIVEM[nm]["FULL"]),
                          full_4b=pass_4b(M[(nm, best[0], best[1], "FULL")], BM[nm]["FULL"]),
                          d_sharpe_vs_base=ob["Sharpe"] - LIVEM[nm]["OOS"]["Sharpe"],
                          d_sharpe_vs_spy=ob["Sharpe"] - BM[nm]["OOS"]["Sharpe"],
                          d_cagr_vs_spy=ob["CAGR"] - BM[nm]["OOS"]["CAGR"]))
    picks_df = pd.DataFrame(prows)
    picks_df.to_csv(f"{OUT}.picks.csv", index=False)

    # ---- the verdict
    say("\n" + "=" * 118)
    say("THE ANSWER — C_MID (the idea's chooser) vs C_SHARPE (the incumbent), 3 panels:")
    say("=" * 118)
    rp = picks_df[picks_df.chooser != "ORACLE_OOS"]
    summ = []
    for ch in CHOOSERS:
        s = rp[rp.chooser == ch]
        summ.append(dict(chooser=ch, picks=len(s), oos_4a=int(s.oos_4a.sum()), oos_4b=int(s.oos_4b.sum()),
                         full_4b=int(s.full_4b.sum()), mean_oos_Sharpe=s.oos_Sharpe.mean(),
                         mean_oos_CAGR=s.oos_CAGR.mean(), mean_oos_MaxDD=s.oos_MaxDD.mean(),
                         mean_G=s.G.mean()))
        say(f"    {ch:9s}  OOS 4a {int(s.oos_4a.sum())}/{len(s)}   OOS 4b {int(s.oos_4b.sum())}/{len(s)}"
            f"   FULL 4b {int(s.full_4b.sum())}/{len(s)}   mean OOS Sharpe {s.oos_Sharpe.mean():.4f}"
            f"   mean OOS CAGR {s.oos_CAGR.mean():.2%}   mean OOS MaxDD {s.oos_MaxDD.mean():.2%}"
            f"   mean picked G {s.G.mean():.3f}")
    pd.DataFrame(summ).to_csv(f"{OUT}.summary.csv", index=False)
    spy_oos = np.mean([BM[nm]["OOS"]["Sharpe"] for nm in tapes])
    base_oos = np.mean([LIVEM[nm]["OOS"]["Sharpe"] for nm in tapes])
    say(f"    {'SPY':9s}  mean OOS Sharpe {spy_oos:.4f}   "
        f"mean OOS CAGR {np.mean([BM[nm]['OOS']['CAGR'] for nm in tapes]):.2%}   "
        f"mean OOS MaxDD {np.mean([BM[nm]['OOS']['MaxDD'] for nm in tapes]):.2%}")
    say(f"    {'RULESv2':9s}  mean OOS Sharpe {base_oos:.4f}   "
        f"mean OOS CAGR {np.mean([LIVEM[nm]['OOS']['CAGR'] for nm in tapes]):.2%}   "
        f"mean OOS MaxDD {np.mean([LIVEM[nm]['OOS']['MaxDD'] for nm in tapes]):.2%}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n  GATES: {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass.")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"  wall {time.time()-t0:.0f}s   artifacts: {Path(OUT).name}.{{grid,intervals,picks,"
        f"summary,keep_census,gates}}.csv + .console.txt")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
