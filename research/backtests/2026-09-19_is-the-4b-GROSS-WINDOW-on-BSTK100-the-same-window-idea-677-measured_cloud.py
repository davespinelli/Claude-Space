#!/usr/bin/env python3
"""Idea 710 (lane cloud, run 7, 2026-09-19): IS THE 4b GROSS WINDOW ON BSTK100 THE SAME WINDOW IDEA 677 MEASURED?

THE QUESTION.  Idea 702 ran CAND-n on BSTK100 over a THREE-RUNG gross ladder {0.50, 0.75, 1.00}
and found its six 4b passes are a GROSS window, not an n window: five sit at exactly g = 0.75,
the CAGR floor (0.70 x 14.13% = 9.89%) bites at g = 0.50 where every cell tops out at 9.51%, and
the DD cap (0.60 x -33.72% = -20.23%) bites at g = 1.00 for every n <= 60.  A three-rung ladder
cannot locate an edge: "the window is 0.75" is a statement about the ladder, not about the book.
This run re-cuts the gross axis at 0.05 RESOLUTION and reports THE WINDOW'S TWO EDGES AS NUMBERS,
against idea 677's committed width reading.

IDEA 677's COMMITTED READING, quoted before this run's numbers (LEADERBOARD 2026-09-15):
  * W = g_max - g_min over 192 books x a 30-rung ladder (5,760 runs); gate-book median
    W = **-0.0523**, `W >= 0` in **76/180**, floor unreachable to g = 1.50 in **21/180**.
  * "TUNED DIAL 1 IS INERT: moving the rung resolution 0.25 -> 0.05 moves the median width by
    0.0002."  That inertness claim is the thing this run can independently confirm or break on a
    family 677 did not use, because idea 702's own ladder WAS the coarse 0.25 grid.
A NEGATIVE W is not a typo: with g_min the CAGR floor's crossing and g_max the DD cap's, W < 0
means the two constraints have CROSSED and the 4b window is EMPTY.  This run adopts that exact
convention so its numbers are commensurable with 677's, and publishes the discrete PASS-set edges
beside it so the reader can see both currencies.

THE BOOK (idea 702's, frozen, not re-derived).  CAND-n: rank the eligible names (above the 200d
MA, vol20 < 0.60) by the composite of three momentum legs, take the top n, hold g/n of NAV each.
Realised gross is g x (held/n), so a capacity-bound n DE-GROSSES the book on its own — which is
why the edges must be read in REALISED gross as well as nominal.  Weekly, t+1, 10 bps both legs.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  g {0.30, 0.35, ..., 1.00}          DIAL 1 — 15 rungs at 0.05, the resolution the idea asks for.
  n {5,10,15,20,25,30,40,50,60,75,100}  DIAL 2 — idea 702's own 11 rungs, unchanged.
165 cells per panel.  NOT A DIAL, reported at every value: PANEL {BSTK100, B136, U56}.  **495
cells in all, EVERY ONE PUBLISHED** in the .grid.csv.  BSTK100 is the idea's panel; B136 and U56
are carried so the window's location can be read as a panel property rather than a BSTK100 fact.

NO LEVERAGE (PROTOCOL rule 2).  677 swept to g = 1.50; this run STOPS AT g = 1.00 because the
protocol forbids leverage unless the idea asks for it, and idea 710 does not.  A g_max that is
not reached by g = 1.00 is therefore reported as RIGHT-CENSORED at 1.00, never extrapolated — the
same treatment 677 gave its own "floor unreachable" cells, in the opposite direction.

THE TWO EDGE CURRENCIES, both published:
  LEG EDGES (677's convention, continuous).  CAGR rises with g and MaxDD deepens with g, so
      g_min = the smallest g whose CAGR clears 0.70 x SPY's, LINEARLY INTERPOLATED between the
              bracketing rungs;
      g_max = the largest g whose MaxDD clears 0.60 x SPY's, likewise interpolated;
      W     = g_max - g_min, NEGATIVE when the constraints cross (an empty window).
      The two Sharpe-half legs of 4b are checked separately and reported; they are not part of W,
      exactly as in 677.
  PASS-SET EDGES (702's convention, discrete).  The lowest and highest g at which the cell
      actually clears ALL FOUR 4b legs, and the count of passing rungs between them.
  MONOTONICITY IS TESTED, NOT ASSUMED: the run reports how many (panel, n) rows have a
  NON-CONTIGUOUS pass set, because interpolated edges are only meaningful where the set is an
  interval.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) If the 0.05 ladder puts the edges near 0.75 and the widths near 677's median, 702's coarse
      reading was lucky and 677's inertness claim replicates on a fresh family.
  (b) If the true edges sit well away from 0.75, 702's "five of six at exactly 0.75" is a
      GRID ARTEFACT of its own three-rung ladder and must be restated.
  (c) If W is negative on most (panel, n) rows — as 677's median says — then BSTK100's six passes
      are the tail of a distribution whose centre has NO window at all.
  (d) If the window's location moves with the panel, it is not a property of the BOOK.
All four are reported.  Nothing is tuned until it works.

RULE 8.  Dials fit on warm-up..2016-12-31 ONLY; 2017-2026 read EXACTLY ONCE.  Four choosers over
the same 165 cells: C_SHARPE (argmax IS Sharpe), C_4b (argmax IS Sharpe among cells clearing 4b
on the IS window alone — idea 702's S5), C_MIDWIN (the MIDPOINT of the IS leg-window at the IS-best
n, i.e. choose the window rather than the cell), C_NULL (the live RULES v2 book, choosing nothing).
Both KEEP paths are evaluated at EVERY cell on FULL, IS and OOS.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of idea 702's committed best 4b passer
(BSTK100, n = 60, g = 0.75: 11.42% / 1.1102 / -17.07%).  G2 REPLAY of 702's binding-leg claims:
every g = 0.50 cell tops out near 9.51% and the DD cap binds every g = 1.00 cell at n <= 60.
G3 NO LEVERAGE: realised gross never exceeds 1.0.  G4 exactly two tuned parameters.  G5 no
chooser reads a row on or after 2017-01-01.  G6 all 495 cells published.  G7 MONOTONICITY
PUBLISHED, not asserted.  G8 the de-grossing identity: realised gross == g x mean(held)/n.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (RULES v2 AND SPY);
rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9 (survivorship stated).
RULES.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only).
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "is-the-4b-GROSS-WINDOW-on-BSTK100-the-same-window-idea-677-measured"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
CAD, COST = "W", 10.0
GRID_G = [round(0.30 + 0.05 * i, 2) for i in range(15)]          # 0.30 .. 1.00 at 0.05
GRID_N = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]            # idea 702's own rungs
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
REPLAY_702 = dict(n=60, g=0.75, CAGR=0.1142, Sharpe=1.1102, MaxDD=-0.1707)
W677_MEDIAN, W677_NONNEG = -0.0523, 76 / 180

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


# ---------------------------------------------------------------- panel + book (idea 702's, frozen)
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence=CAD):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def cand_weights(pan, reb, n, g, lag=1):
    """CAND-n at nominal gross g: top-n eligible by composite, g/n of NAV each.

    A capacity-bound n holds fewer than n lots, so the book DE-GROSSES itself: realised gross is
    g x held/n.  Returns (weight matrix, held-count path on rebalance rows).
    """
    T, M = pan.rets.shape
    W = np.zeros((T, M))
    held = np.zeros(len(reb))
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        k = pan.rank_key[ts].copy()
        k[~(pan.elig[ts] & pan.priced[ts][pan.iinv])] = np.inf
        order = np.argsort(k, kind="stable")
        take = [int(c) for c in order[:n] if np.isfinite(k[c])]
        held[i] = len(take)
        if take:
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[take]] = g / n
    return W, held


def run_book(pan, W, reb, cost=COST):
    """Buy-and-hold-between-rebalances accounting with cash residual, t+1, `cost` bps turnover."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = W[i0]
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


def legs_4b(m, spy):
    return dict(H1=bool(m["H1"] > spy["H1"]), H2=bool(m["H2"] > spy["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))


def keep_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


def interp_edge(gs, vals, bar, rising):
    """First (rising) / last (falling) g whose `vals` clears `bar`, linearly interpolated.

    rising=True  -> CAGR: the SMALLEST g with val >= bar (g_min).
    rising=False -> MaxDD: the LARGEST g with val >= bar (g_max; MaxDD is negative and deepens).
    Returns (edge, status) with status in {'interp', 'left-censored', 'right-censored', 'none'}.
    """
    gs = np.asarray(gs, float)
    ok = np.asarray(vals, float) >= bar
    if not ok.any():
        return np.nan, "none"
    if rising:
        j = int(np.argmax(ok))
        if j == 0:
            return float(gs[0]), "left-censored"
        v0, v1 = float(vals[j - 1]), float(vals[j])
        t = 0.0 if v1 == v0 else (bar - v0) / (v1 - v0)
        return float(gs[j - 1] + t * (gs[j] - gs[j - 1])), "interp"
    j = int(len(ok) - 1 - np.argmax(ok[::-1]))
    if j == len(gs) - 1:
        return float(gs[-1]), "right-censored"
    v0, v1 = float(vals[j]), float(vals[j + 1])
    t = 0.0 if v1 == v0 else (bar - v0) / (v1 - v0)
    return float(gs[j] + t * (gs[j + 1] - gs[j])), "interp"


def main():
    t0 = time.time()
    say("=" * 122)
    say("IDEA 710 (lane cloud, run 7, 2026-09-19) — IS THE 4b GROSS WINDOW ON BSTK100 THE SAME WINDOW IDEA 677 MEASURED?")
    say(f"DIALS (2, and no more): g {GRID_G[0]}..{GRID_G[-1]} at 0.05 ({len(GRID_G)} rungs)  x  n {GRID_N} "
        f"({len(GRID_N)} rungs).  PANEL is reported, not tuned.")
    say(f"BOOK: idea 702's CAND-n, frozen.  Weekly, t+1, {COST:.0f} bps both legs.  NO LEVERAGE: the ladder "
        f"STOPS at g = 1.00 (677 swept to 1.50; PROTOCOL rule 2 forbids it here).")
    say(f"IDEA 677's COMMITTED READING, quoted first: gate-book median W = {W677_MEDIAN:+.4f}, "
        f"W >= 0 in 76/180 = {W677_NONNEG:.3f}, and 'resolution 0.25 -> 0.05 moves the median width by 0.0002'.")
    say("=" * 122)

    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = set(t for k in ("broad", "sectors", "bonds_fx_commod") for t in U[k] if t not in crypto)
    px56, px136 = load_universe(), load_universe(broad=True)
    b_stk = [c for c in px136.columns if c not in etf36 and c != "SPY"]
    keep = list(dict.fromkeys(b_stk + ["SPY"]))
    pxBS = px136[keep].dropna(how="all").ffill()

    panels = [Panel("BSTK100", pxBS, b_stk),
              Panel("B136", px136, [c for c in px136.columns if c != "SPY"]),
              Panel("U56", px56, [c for c in px56.columns if c != "SPY"])]
    say(f"  PANELS: BSTK100 {len(b_stk)} names (B136 minus the {len(etf36)} ETFs of universe.json), "
        f"B136 {len(px136.columns)-1}, U56 {len(px56.columns)-1}.")
    say("  SURVIVORSHIP (rule 9): BSTK100 / B136 / U56 are CURRENT-constituent lists carried back, so every")
    say("  absolute CAGR and every 4b pass below is an UPPER BOUND — idea 702 said the same of this panel.")
    say("  What survives the bias is the LOCATION of the edges on the gross axis, which is a contrast")
    say("  between rungs on one set of names, and the CROSS-PANEL comparison, which shares one construction.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows ({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned parameters", f"g ({len(GRID_G)} rungs) x n ({len(GRID_N)} rungs)", "2", True)

    rows, ident, maxgross = [], [], []
    BARS, CELLR = {}, {}
    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        WIN = dict(FULL=slice(WARMUP, None), IS=slice(WARMUP, i_oos), OOS=slice(i_oos, None))
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CAD)["returns"].values
        spyb = {k: pack(pan.spy[s]) for k, s in WIN.items()}
        liveb = {k: pack(lr[s]) for k, s in WIN.items()}
        BARS[pan.name] = dict(spy=spyb, live=liveb, i_oos=i_oos)
        say(f"\n  [{pan.name}] BARS")
        for k in ["FULL", "IS", "OOS"]:
            s, l = spyb[k], liveb[k]
            say(f"    {k:4s} SPY {s['CAGR']:7.2%} / {s['Sharpe']:7.4f} / {s['MaxDD']:7.2%}  "
                f"-> 4b bars: CAGR floor {CAGR_FLOOR*s['CAGR']:6.2%}, DD cap {DD_CAP*s['MaxDD']:7.2%}, "
                f"halves {s['H1']:.4f}/{s['H2']:.4f}  |  RULES v2 {l['CAGR']:7.2%} / {l['Sharpe']:7.4f} / "
                f"{l['MaxDD']:7.2%} H {l['H1']:.3f}/{l['H2']:.3f}")

        reb = pan.reb_rows()
        for n in GRID_N:
            for g in GRID_G:
                W, held = cand_weights(pan, reb, n, g)
                r, turn, gsum = run_book(pan, W, reb)
                CELLR[(pan.name, n, g)] = r
                mg = float(np.max(gsum))
                maxgross.append(mg)
                ident.append(abs(float(np.mean(W[reb].sum(axis=1))) - g * float(held.mean()) / n))
                row = dict(panel=pan.name, n=n, g=g, held_mean=float(held.mean()),
                           realised_gross=float(np.mean(gsum[WARMUP:])), max_gross=mg,
                           turnover=float(turn.sum()) * 252 / max(len(pan.idx) - WARMUP, 1))
                for k, s in WIN.items():
                    m = pack(r[s])
                    row[f"{k}_CAGR"], row[f"{k}_Sharpe"], row[f"{k}_MaxDD"] = m["CAGR"], m["Sharpe"], m["MaxDD"]
                    row[f"{k}_H1"], row[f"{k}_H2"] = m["H1"], m["H2"]
                    lg = legs_4b(m, spyb[k])
                    row[f"{k}_4b"] = all(lg.values())
                    for lk, lv in lg.items():
                        row[f"{k}_4b_{lk}"] = lv
                    row[f"{k}_4a"] = keep_4a(m, liveb[k])
                rows.append(row)

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G6 all 495 cells published", len(grid), "495", len(grid) == 495)
    gate("G3 no leverage (max realised gross over all 495 cells)", f"{max(maxgross):.6f}", "<= 1.0 + 1e-9",
         max(maxgross) <= 1.0 + 1e-9)
    gate("G8 de-grossing identity  mean nominal weight == g x mean(held)/n", f"{max(ident):.3e}", "< 1e-12",
         max(ident) < 1e-12)

    # ---- G1 / G2: replay idea 702
    c = grid[(grid.panel == "BSTK100") & (grid.n == REPLAY_702["n"]) & (grid.g == REPLAY_702["g"])].iloc[0]
    d = max(abs(c.FULL_CAGR - REPLAY_702["CAGR"]), abs(c.FULL_Sharpe - REPLAY_702["Sharpe"]),
            abs(c.FULL_MaxDD - REPLAY_702["MaxDD"]))
    gate("G1 replay idea 702's best 4b passer (BSTK100, n=60, g=0.75)",
         f"{c.FULL_CAGR:.2%}/{c.FULL_Sharpe:.4f}/{c.FULL_MaxDD:.2%} vs committed "
         f"{REPLAY_702['CAGR']:.2%}/{REPLAY_702['Sharpe']:.4f}/{REPLAY_702['MaxDD']:.2%}, max|d| = {d:.3e}",
         "< 2e-2 (702 ran a DIFFERENT start calendar; see note)", d < 2e-2)
    bs = grid[grid.panel == "BSTK100"]
    top50 = bs[bs.g == 0.50].FULL_CAGR.max()
    ddbind = bs[(bs.g == 1.00) & (bs.n <= 60)]
    cf_full = CAGR_FLOOR * BARS["BSTK100"]["spy"]["FULL"]["CAGR"]
    gate("G2a replay 702's CAGR-floor claim: every g=0.50 cell tops out near 9.51%, below the floor",
         f"max FULL CAGR at g=0.50 = {top50:.2%} against this run's floor {cf_full:.2%} "
         f"({int(bs[(bs.g==0.50)&bs.FULL_4b_CAGR.astype(bool)].shape[0])}/11 g=0.50 cells CLEAR the floor here)",
         "<= the floor, as 702 committed", bool(top50 <= cf_full))
    gate("G2b replay 702's DD-cap claim: the cap binds every g=1.00 cell at n<=60",
         f"{int((~ddbind.FULL_4b_DD).sum())}/{len(ddbind)} of them fail the DD leg", "all of them",
         bool((~ddbind.FULL_4b_DD).all()))

    # ---------------------------------------------------------- (1) THE EDGES
    say("\n" + "=" * 122)
    say("(1) THE WINDOW'S TWO EDGES AS NUMBERS — 677's LEG CONVENTION (interpolated) AND 702's PASS-SET CONVENTION")
    say("=" * 122)
    edges = []
    for pan in panels:
        for k in ["FULL", "IS", "OOS"]:
            spyb = BARS[pan.name]["spy"][k]
            cf, dc = CAGR_FLOOR * spyb["CAGR"], DD_CAP * spyb["MaxDD"]
            for n in GRID_N:
                z = grid[(grid.panel == pan.name) & (grid.n == n)].sort_values("g")
                gmin, s1 = interp_edge(z.g.values, z[f"{k}_CAGR"].values, cf, True)
                gmax, s2 = interp_edge(z.g.values, z[f"{k}_MaxDD"].values, dc, False)
                W = (gmax - gmin) if (np.isfinite(gmin) and np.isfinite(gmax)) else np.nan
                ps = z[z[f"{k}_4b"]].g.values
                contig = (len(ps) == 0) or (len(ps) == int(round((ps.max() - ps.min()) / 0.05)) + 1)
                edges.append(dict(panel=pan.name, window=k, n=n, g_min=gmin, g_min_status=s1,
                                  g_max=gmax, g_max_status=s2, W=W, n_pass=len(ps),
                                  pass_lo=ps.min() if len(ps) else np.nan,
                                  pass_hi=ps.max() if len(ps) else np.nan, contiguous=contig,
                                  cagr_floor=cf, dd_cap=dc))
    ed = pd.DataFrame(edges)
    ed.to_csv(f"{OUT}.edges.csv", index=False)
    for pan in panels:
        for k in ["FULL", "OOS"]:
            e = ed[(ed.panel == pan.name) & (ed.window == k)]
            say(f"\n  [{pan.name} / {k}]  CAGR floor {e.cagr_floor.iloc[0]:.2%}, DD cap {e.dd_cap.iloc[0]:.2%}")
            say("     n   g_min(CAGR floor)     g_max(DD cap)        W        4b PASS rungs   pass window   contiguous")
            for _, r in e.iterrows():
                pw = f"{r.pass_lo:.2f}..{r.pass_hi:.2f}" if r.n_pass else "   —   "
                say(f"   {int(r.n):3d}   {r.g_min:6.4f} ({r.g_min_status:14s})  {r.g_max:6.4f} ({r.g_max_status:14s})  "
                    f"{r.W:+7.4f}   {int(r.n_pass):2d}/15        {pw}      {bool(r.contiguous)}")
            say(f"     -> median W {e.W.median():+.4f}   W >= 0 in {int((e.W>=0).sum())}/{len(e)}   "
                f"rows with any 4b PASS {int((e.n_pass>0).sum())}/{len(e)}   non-contiguous {int((~e.contiguous).sum())}")
    publish("G7 MONOTONICITY: non-contiguous 4b pass sets over all 99 (panel, window, n) rows",
            f"{int((~ed.contiguous).sum())}/{len(ed)}")

    say("\n  AGAINST IDEA 677's COMMITTED READING:")
    for k in ["FULL", "IS", "OOS"]:
        e = ed[ed.window == k]
        eb = ed[(ed.window == k) & (ed.panel == "BSTK100")]
        say(f"    {k:4s}  all 3 panels: median W {e.W.median():+.4f} (677 gate-book median {W677_MEDIAN:+.4f}), "
            f"W >= 0 in {int((e.W>=0).sum())}/{len(e)} = {(e.W>=0).mean():.3f} (677 {W677_NONNEG:.3f})  |  "
            f"BSTK100 alone: median W {eb.W.median():+.4f}, W >= 0 in {int((eb.W>=0).sum())}/{len(eb)}")

    # ---------------------------------------------------------- (2) IS 0.75 THE WINDOW?
    say("\n" + "=" * 122)
    say("(2) IS 702's 'FIVE OF SIX AT EXACTLY g = 0.75' A GRID ARTEFACT?  — the 4b PASS count by rung")
    say("=" * 122)
    for pan in panels:
        z = grid[grid.panel == pan.name]
        say(f"  [{pan.name}] FULL 4b passes by g rung (out of {len(GRID_N)} n rungs each):")
        say("     " + "  ".join(f"{g:.2f}" for g in GRID_G))
        say("     " + "  ".join(f"{int(z[(z.g==g)].FULL_4b.sum()):4d}" for g in GRID_G))
        say("     " + f"OOS: " + "  ".join(f"{int(z[(z.g==g)].OOS_4b.sum()):4d}" for g in GRID_G))
    say(f"\n  702's THREE-RUNG LADDER on BSTK100 re-read here: "
        f"g=0.50 {int(bs[bs.g==0.50].FULL_4b.sum())}/11, g=0.75 {int(bs[bs.g==0.75].FULL_4b.sum())}/11, "
        f"g=1.00 {int(bs[bs.g==1.00].FULL_4b.sum())}/11  (702 committed 6 passes over those 33 cells).")
    say(f"  THE SAME PANEL AT 0.05 RESOLUTION: {int(bs.FULL_4b.sum())}/165 FULL, {int(bs.OOS_4b.sum())}/165 OOS, "
        f"{int(bs.FULL_4a.sum())}/165 4a FULL, {int(bs.OOS_4a.sum())}/165 4a OOS.")

    # ---------------------------------------------------------- (3) RULE 8
    say("\n" + "=" * 122)
    say("(3) RULE 8 — DIALS FIT ON warm-up..2016-12-31 ONLY, 2017-2026 READ EXACTLY ONCE")
    say("=" * 122)
    wf = []
    for pan in panels:
        z = grid[grid.panel == pan.name]
        live, spy = BARS[pan.name]["live"], BARS[pan.name]["spy"]
        picks = {"C_SHARPE": z.loc[z.IS_Sharpe.idxmax()]}
        ok = z[z.IS_4b]
        picks["C_4b"] = ok.loc[ok.IS_Sharpe.idxmax()] if len(ok) else None
        nbest = int(z.loc[z.IS_Sharpe.idxmax()].n)
        e = ed[(ed.panel == pan.name) & (ed.window == "IS") & (ed.n == nbest)].iloc[0]
        if np.isfinite(e.W) and e.W >= 0:
            gm = min(GRID_G, key=lambda x: abs(x - 0.5 * (e.g_min + e.g_max)))
            picks["C_MIDWIN"] = z[(z.n == nbest) & (z.g == gm)].iloc[0]
        else:
            picks["C_MIDWIN"] = None
        for cname, c in picks.items():
            if c is None:
                wf.append(dict(panel=pan.name, chooser=cname, pick_n=np.nan, pick_g=np.nan,
                               note="IS window EMPTY -> chooser declines"))
                continue
            wf.append(dict(panel=pan.name, chooser=cname, pick_n=int(c.n), pick_g=float(c.g),
                           IS_Sharpe=c.IS_Sharpe, OOS_CAGR=c.OOS_CAGR, OOS_Sharpe=c.OOS_Sharpe,
                           OOS_MaxDD=c.OOS_MaxDD, OOS_4a=bool(c.OOS_4a), OOS_4b=bool(c.OOS_4b),
                           dOOS_S_vs_SPY=c.OOS_Sharpe - spy["OOS"]["Sharpe"],
                           dOOS_S_vs_LIVE=c.OOS_Sharpe - live["OOS"]["Sharpe"], note=""))
        wf.append(dict(panel=pan.name, chooser="C_NULL (RULES v2)", pick_n=np.nan, pick_g=np.nan,
                       OOS_CAGR=live["OOS"]["CAGR"], OOS_Sharpe=live["OOS"]["Sharpe"],
                       OOS_MaxDD=live["OOS"]["MaxDD"], OOS_4a=False, OOS_4b=False,
                       dOOS_S_vs_SPY=live["OOS"]["Sharpe"] - spy["OOS"]["Sharpe"], dOOS_S_vs_LIVE=0.0, note=""))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gate("G5 no chooser reads a row on or after 2017-01-01", "IS slices end at i_oos-1 by construction",
         "by construction", True)

    # ---------------------------------------------------------- (4) the mandated comparison
    say("\n" + "=" * 122)
    say("(4) THE PROTOCOL'S MANDATED COMPARISON — the rule-8 pick on BSTK100 vs RULES v2 and SPY")
    say("=" * 122)
    for pan in panels:
        live, spy = BARS[pan.name]["live"], BARS[pan.name]["spy"]
        w = wfd[(wfd.panel == pan.name) & (wfd.chooser == "C_SHARPE")].iloc[0]
        for k in ["FULL", "OOS"]:
            c = grid[(grid.panel == pan.name) & (grid.n == w.pick_n) & (grid.g == w.pick_g)].iloc[0]
            say(f"  [{pan.name}] {k:4s} C_SHARPE pick (n={int(w.pick_n)}, g={w.pick_g:.2f}) "
                f"{c[f'{k}_CAGR']:7.2%}/{c[f'{k}_Sharpe']:7.4f}/{c[f'{k}_MaxDD']:7.2%}  |  RULES v2 "
                f"{live[k]['CAGR']:7.2%}/{live[k]['Sharpe']:7.4f}/{live[k]['MaxDD']:7.2%}  |  SPY "
                f"{spy[k]['CAGR']:7.2%}/{spy[k]['Sharpe']:7.4f}/{spy[k]['MaxDD']:7.2%}  |  "
                f"4a {bool(c[f'{k}_4a'])}  4b {bool(c[f'{k}_4b'])}")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(1 for g in GATES if g["pass_"])
    say(f"\nGATES {npass}/{len(GATES)} pass.  Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
