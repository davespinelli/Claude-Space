#!/usr/bin/env python3
"""Idea 440 — is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end   (cloud lane, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 439 found idea 168c's crossing in the vol-scaler exponent k moves 4 grid steps
    (k = 0.10 -> 1.00) on the HALF-WINDOW alone, while fixed effects move it 0 — the opposite
    failure mode to the one idea 226 chased.  Re-read that crossing WITHOUT ANY SMOOTHING
    (per-k cell means, exact) and WITH A BOOTSTRAP over cells, and say whether a k threshold
    exists at all or whether the record has been reading a slope.

WHAT THIS RUN DOES
    A. Reproduction gate.  Rebuild idea 168c's 352 books from prices with its own committed
       conventions (score_k / weights_k / panel / eligible_mask imported verbatim from the
       committed 168c script) and assert against its committed .grid.csv before reading
       anything new.  Also assert fast_backtest == engine.backtest bit-for-bit, and reproduce
       idea 439's five smoothed readings of item 168c (hmult 1..5 -> 0.10/0.10/0.50/0.75/1.00).
    B. The exact reading.  Per-k cell means, no window at all, on 168c's 32 cells and on a
       fresh 3-panel corpus that adds SMALL439 (survivorship caveat below).
    C. Why the window moves it.  Because the k grid is balanced (32 cells at every k), a
       windowed local mean is an EXACT unweighted average of the per-k means inside the
       window.  So the smoothed curve is a linear functional of the exact curve: it carries
       no information the exact curve does not, and can only relocate the reading.  Proved
       numerically (max abs diff vs idea 439's own local_curve output).
    D. Bootstrap over cells, three block definitions (TUNED PARAMETER 2).
    E. Threshold vs slope: linear / step-at-tau / free-knot hinge / hinge-pinned-at-0, RSS +
       AIC + bootstrap CI on tau-hat.
    F. Rule 8 walk-forward on live prices: k chosen on IS (<= 2016-12-31) only, evaluated
       untouched on 2017-2026, against the k = 0 control, the live k = -0.5, and the k that
       each READING of the crossing would have you adopt.  Both KEEP paths (4a vs RULES v2
       live and RULES v1; 4b vs SPY), full sample + halves + OOS, vs SPY.

TUNED PARAMETERS (exactly two; every grid point is reported)
    P1  half-window multiple  hmult in {0 (EXACT, no smoothing), 1, 2, 3, 4, 5} x median grid
        step (0.25) — idea 439's own P1 with the exact reading prepended.
    P2  bootstrap block in {cell, panel x cost, panel} — how much dependence between the 32
        (panel, cost, share) cells the resample is allowed to break.
    Everything else (k grid, share grid, cost grid, panels, gross 0.75, MAX_VOL 0.60, vol
    floor 0.08, weekly cadence, t+1 execution, IS/OOS split, crossing_of, local_curve,
    make_grid) is imported or copied verbatim from the committed record, not re-chosen here.

PRE-REGISTERED PREDICTIONS (written before the new numbers were read)
    Q1  dSharpe is defined WITHIN cell as Sharpe(k) - Sharpe(k=0), so the curve passes through
        exactly 0.0 at k = 0 in all 32 cells with zero variance.  A "sign crossing" read off it
        is therefore anchored to a DEFINITIONAL zero, not a measured one.
    Q2  The exact per-k mean curve is monotone increasing and its crossing_of reading is the
        SMALLEST POSITIVE GRID POINT (0.10) — i.e. the smallest value the reader can return.
    Q3  Idea 439's upward march (0.10 -> 1.00) is the symmetric window dragging the steep
        NEGATIVE arm (k <= -0.25) into windows centred on positive k.  It is reproducible
        from the 11 exact per-k means alone.
    Q4  Above k = 0 the curve is a PLATEAU, not a ramp: the spread of mean dSharpe across
        k in {0.10 ... 1.00} is small against the cross-cell sd, so the bootstrap crossing
        distribution should sit on 0.10 and the plateau contrast should not be separable.
    Q5  No KEEP.  The deliverable is a KILL of the "k threshold" object and, if Q1-Q4 hold,
        a reporting clause: a within-cell difference curve cannot carry a sign threshold at
        its own control point.

CONFOUNDS / CAVEATS declared up front
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md).  Tickers with
      max_1d_move >= 1.0 in data/small_meta.csv are dropped first (439 names survive).  Every
      SMALL439 number in this run inherits SURVIVORSHIP BIAS and is reported as a shape check,
      never as a tradable return.
    * dSharpe(k=0) == 0 by construction.  That is the point of section (1), not a bug.
    * The k grid is IRREGULAR (steps 0.10/0.15/0.25), so a symmetric window in k-units covers
      a different number of grid points at different centres.  Reported, not corrected — the
      correction would be a third tuned parameter.
    * Costs 10 bps is the protocol rung; 25 bps is carried as 168c's own robustness axis.
    * t+1 execution and the 260-bar warm-up skip are the engine's / 168c's, unchanged.
    * DATA VINTAGE.  `data/prices.csv` (the u56 panel) is refreshed by the daily job scan and
      only entered git on 2026-09-08 (commit dcaffa8); the vintage idea 168c ran on 2026-09-05
      no longer exists.  `data/prices_broad.csv` is refreshed WEEKLY (protocol rule 9) and its
      vintage is unchanged.  So the reproduction gate demands BIT-EXACTNESS on broad (which is
      what proves the code path here is 168c's verbatim) and a declared tolerance on u56, and
      it re-asserts 168c's published QUALITATIVE readings on this run's own books.  The record
      analysis in parts B-E reads 168c's OWN COMMITTED `.curve.csv`, so no conclusion about
      the crossing depends on the re-run at all.

Deterministic (seed 440000), standalone, no network.
Writes .console.txt .grid.csv .exact.csv .window.csv .boot.csv .shape.csv .walkforward.csv
       .keeppaths.csv .result.md
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights            # noqa: E402
from engine import backtest, metrics, rebalance_mask               # noqa: E402

STEM = "2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 440000
COST_MAIN = 10.0

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 400)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- the record, imported verbatim
I168 = _load(OUT / "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.py", "i168c")
C, H, I153 = I168.C, I168.H, I168.I153
KS = list(I168.KS)                       # 11 exponents, committed
SHARES = list(I168.SHARES)               # 8 shares, committed
COSTS = list(I168.COSTS)                 # [10, 25], committed
FREQ, GROSS, MAX_VOL = I168.FREQ, I168.GROSS, I168.MAX_VOL
IS_END, OOS_START = H.IS_END, H.OOS_START
K_LIVE, K_ZERO = I168.K_LIVE, I168.K_ZERO

PANELS_168 = ["u56", "broad"]            # 168c's own corpus
PANELS_ALL = ["u56", "broad", "small"]   # + the shape check

# idea 439's curve reader, verbatim
MIN_IN_WIN = 5


def local_curve(x, y, grid, half_w, min_in=MIN_IN_WIN):
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    out = []
    for g in grid:
        m = (x >= g - half_w) & (x <= g + half_w)
        n = int(m.sum())
        out.append((float(g), n, float(y[m].mean()) if n >= min_in else np.nan))
    return out


def crossing_of(loc):
    """idea 226/439: (first centre above which every defined window is positive,
    last non-positive centre below it)."""
    defined = [np.isfinite(r[2]) for r in loc]
    pos = [np.isfinite(r[2]) and r[2] > 0 for r in loc]
    ch = np.nan
    for i, r in enumerate(loc):
        if not defined[i] or not pos[i]:
            continue
        if all(pos[j] for j in range(i, len(loc)) if defined[j]):
            ch = float(r[0]); break
    below = [r[0] for i, r in enumerate(loc)
             if defined[i] and not pos[i] and (not np.isfinite(ch) or r[0] < ch)]
    return ch, (max(below) if below else np.nan)


def make_grid(x):
    u = np.unique(np.asarray(x, float))
    u = u[np.isfinite(u)]
    return u if len(u) <= 25 else np.linspace(u.min(), u.max(), 25)


def steps_apart(a, b, grid):
    if not (np.isfinite(a) and np.isfinite(b)):
        return np.nan
    g = np.asarray(grid, float)
    return float(abs(np.argmin(abs(g - a)) - np.argmin(abs(g - b))))


def fast_backtest(px, W, cost_bps, freq=FREQ):
    """engine.backtest, same arithmetic, numpy inner loop (asserted identical below)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); held = np.empty((n, k)); to = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return pd.Series((held * rets).sum(axis=1) - to * cost_bps / 1e4, index=px.index)


def csd(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


# ============================================================================ PART A — corpus
def build_corpus():
    P("=" * 118)
    P("PART A — THE CORPUS, REBUILT FROM PRICES (reproduction gate before any new number)")
    P("=" * 118)
    ref, rows, RET = {}, [], {}
    t0 = time.time()
    for pk in PANELS_ALL:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        el = I153.eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        bars = C.bars_win(spy, "full")
        v2 = {c: fast_backtest(px, rules_v2_weights(px), c).loc[start:] for c in COSTS}
        v1 = {c: fast_backtest(px, rules_v1_weights(px), c).loc[start:] for c in COSTS}
        ref[pk] = dict(px=px, start=start, spy=spy, bars=bars, n_elig=n_elig, desc=desc,
                       nmap=nmap, v2=v2, v1=v1)
        sc, ss, sd = csd(spy)
        so = csd(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        P(f"      share -> n: " + ", ".join(f"{m:.3g}->{nmap[m]}" for m in SHARES))
        P(f"      SPY  {sc:.2%}/{ss:.3f}/{sd:.2%}  halves {bars['s1']:.3f}/{bars['s2']:.3f}"
          f"  | OOS {so[0]:.2%}/{so[1]:.3f}/{so[2]:.2%}")
        P(f"      4b bars: H1>{bars['s1']:.3f}  H2>{bars['s2']:.3f}  OOS>{bars['soos']:.3f}  "
          f"|MaxDD|<={0.60*abs(bars['sdd']):.2%}  CAGR>={0.70*bars['scagr']:.2%}")
        for c in COSTS:
            m2, m1 = csd(ref[pk]['v2'][c]), csd(ref[pk]['v1'][c])
            P(f"      RULES v2 @{c:.0f}bps {m2[0]:.2%}/{m2[1]:.3f}/{m2[2]:.2%}   "
              f"RULES v1 @{c:.0f}bps {m1[0]:.2%}/{m1[1]:.3f}/{m1[2]:.2%}")

        for cost in COSTS:
            for k in KS:
                for m in SHARES:
                    n = nmap[m]
                    r = fast_backtest(px, I168.weights_k(px, k, n, pk), cost).loc[start:]
                    RET[(pk, cost, k, m)] = r
                    cg, sh, dd = csd(r)
                    oc, osh, odd = csd(r.loc[OOS_START:])
                    h1, h2 = H.halves(r)
                    mg = H.margins(r, bars)
                    fb = [b for b in ("H1", "H2", "OOS", "DD", "CAGR") if mg[b] <= 0]
                    rows.append(dict(panel=pk, cost=cost, k=k, share=m, n=n,
                                     CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                                     OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd,
                                     IS_CAGR=metrics(H.window(r, "IS"))["CAGR"],
                                     IS_Sharpe=metrics(H.window(r, "IS"))["Sharpe"],
                                     pass4a_v1=H.pass4a(r, ref[pk]["v1"][cost]),
                                     pass4a_v2=H.pass4a(r, ref[pk]["v2"][cost]),
                                     pass4b=(len(fb) == 0), failing="|".join(fb)))
        P(f"      {len(KS)*len(SHARES)*len(COSTS)} books done ({time.time()-t0:.0f}s cum.)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    return ref, G, RET


def repro_gate(ref, G):
    P("\n" + "-" * 118)
    P("  REPRODUCTION GATE")
    P("-" * 118)
    ok = True

    # [a] fast_backtest == engine.backtest
    px = ref["u56"]["px"]
    W = I168.weights_k(px, K_LIVE, 10, "u56")
    d = float((backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"]
               - fast_backtest(px, W, 10.0)).abs().max())
    P(f"  [a] fast_backtest vs engine.backtest, u56 k={K_LIVE} n=10 @10bps: max abs diff "
      f"{d:.3e}  {'MATCH' if d == 0.0 else 'FAIL'}")
    ok &= (d == 0.0)

    # [b] this run's u56/broad books vs 168c's committed grid
    #     PRE-DECLARED: `data/prices_broad.csv` is refreshed WEEKLY (protocol rule 9) and its
    #     vintage is unchanged since 2026-09-05, so the broad half must be BIT-EXACT and is the
    #     proof that the code path here is 168c's verbatim.  `data/prices.csv` is refreshed by
    #     the daily job scan and only entered git on 2026-09-08 (commit dcaffa8); the vintage
    #     168c ran on no longer exists, so the u56 half is held to a declared tolerance
    #     (1e-2 Sharpe / 1e-3 CAGR) instead, and the actual drift is reported.
    pub = pd.read_csv(OUT / "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.grid.csv")
    mine = G[G.panel.isin(PANELS_168)]
    kcols = ["panel", "cost", "k", "share"]
    j = pub.merge(mine, on=kcols, suffixes=("_pub", "_new"))
    P(f"  [b] 168c committed books {len(pub)}, matched here {len(j)}  "
      f"{'MATCH' if len(j) == len(pub) == 352 else 'FAIL'}")
    ok &= (len(j) == len(pub) == 352)
    TOL = {"CAGR": 1e-3, "Sharpe": 1e-2, "MaxDD": 1e-2, "OOS_Sharpe": 1e-2,
           "IS_Sharpe": 1e-2, "H1": 1e-2, "H2": 1e-2}
    for col in TOL:
        db = float((j[j.panel == "broad"][f"{col}_pub"]
                    - j[j.panel == "broad"][f"{col}_new"]).abs().max())
        du = float((j[j.panel == "u56"][f"{col}_pub"]
                    - j[j.panel == "u56"][f"{col}_new"]).abs().max())
        good = (db < 1e-12) and (du < TOL[col])
        P(f"        {col:11s} broad (weekly cache, must reproduce) {db:.3e}   "
          f"u56 (daily cache, tol {TOL[col]:.0e}) {du:.3e}   {'MATCH' if good else 'FAIL'}")
        ok &= bool(good)
    nz = int((j.groupby("panel").apply(
        lambda t: (t.CAGR_pub - t.CAGR_new).abs().max(), include_groups=False) > 1e-12).sum())
    P(f"        -> {nz} of 2 panels drift at all; the drifting one is the daily-refreshed "
      f"data/prices.csv vintage,\n           not the code (see the note in repro_gate).")

    # [b2] the PUBLISHED QUALITATIVE claims of 168c, re-asserted on this run's own books
    su = mine.set_index(["panel", "cost", "k", "share"]).Sharpe
    cu_ = mine.set_index(["panel", "cost", "k", "share"]).CAGR
    cells = [(p, c, m) for p in PANELS_168 for c in COSTS for m in SHARES]
    lose_to_zero = sum(1 for (p, c, m) in cells if su[(p, c, K_LIVE, m)] < su[(p, c, 0.0, m)])
    neg_dcagr = sum(1 for (p, c, m) in cells if c == 10.0
                    and cu_[(p, c, K_LIVE, m)] < cu_[(p, c, 0.0, m)])
    sp = [H.spearman(KS, [cu_[(p, c, k, m)] for k in KS]) for (p, c, m) in cells]
    sp10 = [H.spearman(KS, [cu_[(p, 10.0, k, m)] for k in KS])
            for (p, c, m) in cells if c == 10.0]
    P(f"  [b2] 168c's published qualitative readings, re-asserted here:")
    P(f"        live k={K_LIVE} loses to k=0 on Sharpe: published 32/32, this run "
      f"{lose_to_zero}/32  {'MATCH' if lose_to_zero == 32 else 'FAIL'}")
    P(f"        signed dCAGR at live k negative @10bps: published 16/16, this run "
      f"{neg_dcagr}/16  {'MATCH' if neg_dcagr == 16 else 'FAIL'}")
    P(f"        Spearman(k, CAGR) POSITIVE in every cell (168's 'the exponent curve is "
      f"monotone'): {int(sum(1 for v in sp if v > 0))}/32  "
      f"{'MATCH' if min(sp) > 0 else 'FAIL'}")
    P(f"        (descriptive, not an assertion: Spearman range over the 32 cells "
      f"{min(sp):+.3f} .. {max(sp):+.3f}; over the 16 cells at 10 bps "
      f"{min(sp10):+.3f} .. {max(sp10):+.3f}.  Idea 168's published '+0.93..+1.00 in 12 of 12'"
      f" is LANE B's 12-cell corpus, a different corpus from 168c's 32, so it is reported "
      f"here rather than asserted.)")
    ok &= (lose_to_zero == 32) and (neg_dcagr == 16) and (min(sp) > 0)

    # [c] idea 439's five smoothed readings of item 168c
    cu = pd.read_csv(OUT / "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.curve.csv")
    grid = make_grid(cu.k.values)
    step = float(np.median(np.diff(np.sort(grid))))
    pub439 = {1.0: 0.10, 2.0: 0.10, 3.0: 0.50, 4.0: 0.75, 5.0: 1.00}
    P(f"  [c] idea 439's pooled (FE=NONE) readings of item 168c, grid {len(grid)} pts, "
      f"median step {step:.4g}:")
    for hm, want in pub439.items():
        ch, _ = crossing_of(local_curve(cu.k.values, cu.dSharpe.values, grid, hm * step))
        good = np.isfinite(ch) and abs(ch - want) < 1e-9
        P(f"        hmult {hm:.0f} (half-w {hm*step:.2f}): published {want:.2f}  this run "
          f"{ch:.2f}  {'MATCH' if good else 'FAIL'}")
        ok &= bool(good)
    P(f"\n  GATE: {'PASS' if ok else 'FAIL'}")
    if not ok:
        raise SystemExit("reproduction gate failed — no new number is read")
    return cu, grid, step


# ============================================================ PART B/C — exact vs windowed
def exact_and_window(cu, grid, step, G):
    P("\n" + "=" * 118)
    P("PART B — THE EXACT READING (per-k cell means, NO WINDOW)")
    P("=" * 118)
    ex_rows = []

    def curve_of(d, tag, nc):
        g = d.groupby("k").dSharpe.agg(["mean", "std", "count", "min", "max"])
        g = g.reindex(KS)
        loc = [(float(k), int(g.loc[k, "count"]), float(g.loc[k, "mean"])) for k in KS]
        ch, below = crossing_of(loc)
        P(f"\n  {tag}  ({nc} cells x {len(KS)} exponents = {len(d)} points)")
        P(f"  {'k':>7s} {'cells':>6s} {'mean dSharpe':>13s} {'sd':>9s} {'min':>9s} {'max':>9s} "
          f"{'>0 in':>10s} {'t':>7s}")
        for k in KS:
            v = d[d.k == k].dSharpe.values
            npos = int((v > 0).sum())
            t = float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))) if v.std(ddof=1) > 0 else np.nan
            P(f"  {k:+7.2f} {len(v):6d} {v.mean():13.5f} {v.std(ddof=1):9.5f} {v.min():9.4f} "
              f"{v.max():9.4f} {npos:5d}/{len(v):<4d} {t:7.2f}")
            ex_rows.append(dict(corpus=tag, k=k, cells=len(v), mean=v.mean(),
                                sd=v.std(ddof=1), lo=v.min(), hi=v.max(), n_pos=npos, t=t))
        P(f"  -> EXACT crossing_of = {ch:.2f}   (last non-positive centre {below:.2f})")
        return g, ch

    g168, ch168 = curve_of(cu[["k", "dSharpe"]].copy(), "168c's own 32 cells (u56+broad, 10/25bps)",
                           cu.groupby(["panel", "cost", "share"]).ngroups)

    # fresh 3-panel corpus, dSharpe recomputed the same way (within-cell vs k=0)
    base = G.set_index(["panel", "cost", "k", "share"]).Sharpe
    fresh = []
    for pk in PANELS_ALL:
        for cost in COSTS:
            for m in SHARES:
                s0 = base[(pk, cost, 0.0, m)]
                for k in KS:
                    fresh.append(dict(panel=pk, cost=cost, share=m, k=k,
                                      dSharpe=base[(pk, cost, k, m)] - s0))
    F = pd.DataFrame(fresh)
    gALL, chALL = curve_of(F[["k", "dSharpe"]].copy(),
                           "fresh 3-panel corpus incl. SMALL439 (48 cells)", 48)
    for pk in PANELS_ALL:
        d = F[F.panel == pk]
        gp, chp = curve_of(d[["k", "dSharpe"]].copy(), f"panel {pk} only (16 cells)", 16)

    P("\n  PLATEAU CHECK — the k > 0 arm, 168c's 32 cells:")
    pos = g168.loc[[k for k in KS if k > 0]]
    P(f"      mean dSharpe over k in (0, 1]: min {pos['mean'].min():.5f} at "
      f"{pos['mean'].idxmin():+.2f}, max {pos['mean'].max():.5f} at {pos['mean'].idxmax():+.2f}, "
      f"spread {pos['mean'].max()-pos['mean'].min():.5f}")
    P(f"      cross-cell sd at those k: {pos['std'].mean():.5f} (mean over the 5 points)")
    P(f"      spread / sd = {(pos['mean'].max()-pos['mean'].min())/pos['std'].mean():.3f}")
    neg = g168.loc[[k for k in KS if k < 0]]
    P(f"      by contrast the k < 0 arm spans {neg['mean'].min():.5f} .. {neg['mean'].max():.5f}"
      f"  (spread {neg['mean'].max()-neg['mean'].min():.5f}, "
      f"{(neg['mean'].max()-neg['mean'].min())/pos['std'].mean():.2f} sd)")

    # ------------------------------------------------------------------ P1 sweep
    P("\n" + "=" * 118)
    P("PART C — TUNED PARAMETER 1: THE HALF-WINDOW, AND WHY IT MOVES THE READING")
    P("=" * 118)
    P("  hmult 0 = EXACT (per-k means).  hmult h = half-window h x median grid step "
      f"({step:.4g}).")
    P(f"\n  {'hmult':>6s} {'half-w':>8s} {'crossing':>9s} {'steps vs exact':>15s} "
      f"{'grid pts in window @+0.10':>26s} {'window mean @+0.10':>19s}")
    win_rows = []
    for hm in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        if hm == 0.0:
            loc = [(float(k), int(g168.loc[k, "count"]), float(g168.loc[k, "mean"])) for k in KS]
        else:
            loc = local_curve(cu.k.values, cu.dSharpe.values, grid, hm * step)
        ch, below = crossing_of(loc)
        inwin = [k for k in KS if abs(k - 0.10) <= hm * step] if hm > 0 else [0.10]
        wm = float(np.mean([g168.loc[k, "mean"] for k in inwin]))
        P(f"  {hm:6.0f} {hm*step:8.2f} {ch:9.2f} {steps_apart(ch, ch168, grid):15.0f} "
          f"{str([f'{k:+.2f}' for k in inwin]):>26s} {wm:19.5f}")
        for (c, n, v) in loc:
            win_rows.append(dict(hmult=hm, half_w=hm * step, centre=c, n=n, mean=v,
                                 crossing=ch, last_nonpos=below))

    # the window curve is an exact re-average of the per-k means (balanced design)
    P("\n  Is the windowed curve a linear functional of the exact one?  The design is balanced "
      "(32 cells at\n  every k), so the window mean must equal the unweighted mean of the "
      "per-k means inside it:")
    worst = 0.0
    for hm in [1.0, 2.0, 3.0, 4.0, 5.0]:
        loc = local_curve(cu.k.values, cu.dSharpe.values, grid, hm * step)
        for (c, n, v) in loc:
            inwin = [k for k in KS if abs(k - c) <= hm * step + 1e-12]
            pred = float(np.mean([g168.loc[k, "mean"] for k in inwin])) if len(inwin) else np.nan
            if np.isfinite(v) and np.isfinite(pred):
                worst = max(worst, abs(v - pred))
    P(f"      max abs |windowed - re-average of exact per-k means| over all 55 grid points: "
      f"{worst:.3e}  {'EXACT' if worst < 1e-12 else 'NOT EXACT'}")
    P("      => the smoothed curve carries NO information the exact curve does not.  The "
      "half-window can\n         only relocate the reading, never inform it.")

    P("\n  Mechanism, spelled out: at every positive centre the symmetric window reaches back "
      "into the\n  steep NEGATIVE arm.  Grid points pulled in at centre +0.10:")
    for hm in [1.0, 2.0, 3.0, 4.0, 5.0]:
        inwin = [k for k in KS if abs(k - 0.10) <= hm * step]
        negs = [k for k in inwin if k < 0]
        P(f"      hmult {hm:.0f}: {len(inwin)} pts, {len(negs)} of them negative "
          f"({', '.join(f'{k:+.2f}' for k in negs) if negs else 'none'})")

    pd.DataFrame(ex_rows).to_csv(OUT / f"{STEM}.exact.csv", index=False)
    pd.DataFrame(win_rows).to_csv(OUT / f"{STEM}.window.csv", index=False)
    return g168, ch168, F, grid, step


# ============================================================ PART D — bootstrap over cells
def bootstrap(cu, grid, B=2000):
    P("\n" + "=" * 118)
    P("PART D — TUNED PARAMETER 2: BOOTSTRAP OVER CELLS (exact per-k means, no smoothing)")
    P("=" * 118)
    W = cu.pivot_table(index=["panel", "cost", "share"], columns="k", values="dSharpe")
    W = W[KS]
    P(f"  cell x k matrix: {W.shape[0]} cells x {W.shape[1]} exponents, "
      f"{int(W.notna().values.sum())} finite entries")
    blocks = {
        "cell": [[i] for i in range(len(W))],
        "panelxcost": [list(np.where((W.index.get_level_values(0) == p)
                                     & (W.index.get_level_values(1) == c))[0])
                       for p in W.index.get_level_values(0).unique()
                       for c in W.index.get_level_values(1).unique()],
        "panel": [list(np.where(W.index.get_level_values(0) == p)[0])
                  for p in W.index.get_level_values(0).unique()],
    }
    Y = W.values
    OFFS = {"cell": 1, "panelxcost": 2, "panel": 3}      # fixed, not hash()-derived
    rows, dist = [], []
    for bname, bl in blocks.items():
        rng = np.random.default_rng(SEED + OFFS[bname])
        chs, plat, argm = [], [], []
        for _ in range(B):
            pick = rng.integers(0, len(bl), size=len(bl))
            idx = np.concatenate([bl[j] for j in pick])
            mu = Y[idx].mean(axis=0)
            loc = [(KS[i], len(idx), float(mu[i])) for i in range(len(KS))]
            ch, _ = crossing_of(loc)
            chs.append(ch)
            plat.append(mu[KS.index(1.00)] - mu[KS.index(0.10)])
            argm.append(KS[int(np.argmax(mu))])
        chs = np.array(chs, float); plat = np.array(plat, float); argm = np.array(argm, float)
        vc = pd.Series(chs).value_counts(dropna=False).sort_index()
        P(f"\n  block = {bname}  ({len(bl)} blocks resampled, B={B})")
        P(f"      crossing distribution:")
        for v, n in vc.items():
            P(f"          {('nan' if not np.isfinite(v) else f'{v:+.2f}'):>7s}: "
              f"{n:5d}  ({n/B:6.1%})")
        P(f"      P(crossing == exact 0.10) = {np.mean(chs == 0.10):.1%};  "
          f"P(crossing >= 0.50, i.e. the hmult>=3 readings) = {np.mean(chs >= 0.50):.1%}")
        lo, hi = np.percentile(plat, [2.5, 97.5])
        P(f"      plateau contrast mean dSharpe(k=+1.00) - mean dSharpe(k=+0.10): "
          f"point {plat.mean():+.5f}, 95% CI [{lo:+.5f}, {hi:+.5f}], "
          f"P(>0) = {np.mean(plat > 0):.1%}  -> "
          f"{'SEPARABLE' if lo > 0 or hi < 0 else 'NOT SEPARABLE'}")
        avc = pd.Series(argm).value_counts().sort_index()
        P(f"      argmax-k distribution: " + ", ".join(f"{v:+.2f}:{n/B:.1%}" for v, n in avc.items()))
        rows.append(dict(block=bname, B=B, p_exact=float(np.mean(chs == 0.10)),
                         p_ge_050=float(np.mean(chs >= 0.50)),
                         plateau=float(plat.mean()), plateau_lo=float(lo), plateau_hi=float(hi),
                         plateau_p_pos=float(np.mean(plat > 0)),
                         argmax_mode=float(avc.idxmax()), argmax_mode_share=float(avc.max() / B)))
        for v, n in vc.items():
            dist.append(dict(block=bname, crossing=v, count=int(n), share=n / B))
    pd.DataFrame(dist).to_csv(OUT / f"{STEM}.boot.csv", index=False)
    return pd.DataFrame(rows)


# ============================================================ PART E — threshold vs slope
def shape_test(cu, B=1000):
    P("\n" + "=" * 118)
    P("PART E — IS IT A THRESHOLD OR A SLOPE?  four shapes, same 352 points")
    P("=" * 118)
    x = cu.k.values.astype(float); y = cu.dSharpe.values.astype(float)
    TAUS = [k for k in KS[1:-1]]                     # interior candidate knots only

    def rss_of(X, y):
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(((y - X @ b) ** 2).sum()), b

    def fits(x, y):
        one = np.ones_like(x)
        out = {}
        out["linear"] = rss_of(np.column_stack([one, x]), y) + (2, np.nan)
        best = None
        for t in TAUS:
            r, b = rss_of(np.column_stack([one, (x > t).astype(float)]), y)
            if best is None or r < best[0]:
                best = (r, b, t)
        out["step@tau"] = (best[0], best[1], 3, best[2])          # +1 for the searched knot
        best = None
        for t in TAUS:
            r, b = rss_of(np.column_stack([one, x, np.maximum(0.0, x - t)]), y)
            if best is None or r < best[0]:
                best = (r, b, t)
        out["hinge@tau"] = (best[0], best[1], 4, best[2])          # +1 for the searched knot
        r, b = rss_of(np.column_stack([one, x, np.maximum(0.0, x - 0.0)]), y)
        out["hinge@0 (pinned)"] = (r, b, 3, 0.0)
        return out

    F = fits(x, y)
    n = len(y)
    P(f"  {'model':20s} {'params':>7s} {'tau':>7s} {'RSS':>12s} {'R2':>8s} {'AIC':>10s} "
      f"{'dAIC':>8s}")
    tss = float(((y - y.mean()) ** 2).sum())
    aics = {k: n * np.log(v[0] / n) + 2 * v[2] for k, v in F.items()}
    a0 = min(aics.values())
    for k, v in F.items():
        P(f"  {k:20s} {v[2]:7d} {('' if not np.isfinite(v[3]) else f'{v[3]:+.2f}'):>7s} "
          f"{v[0]:12.5f} {1-v[0]/tss:8.4f} {aics[k]:10.2f} {aics[k]-a0:8.2f}")
    winner = min(aics, key=aics.get)
    P(f"  -> best by AIC: {winner}")

    rng = np.random.default_rng(SEED + 7)
    cells = cu.groupby(["panel", "cost", "share"]).indices
    keys = list(cells)
    taus_h, taus_s, wins = [], [], []
    for _ in range(B):
        pick = rng.integers(0, len(keys), size=len(keys))
        idx = np.concatenate([cells[keys[j]] for j in pick])
        Fb = fits(x[idx], y[idx])
        taus_h.append(Fb["hinge@tau"][3]); taus_s.append(Fb["step@tau"][3])
        ab = {k: len(idx) * np.log(v[0] / len(idx)) + 2 * v[2] for k, v in Fb.items()}
        wins.append(min(ab, key=ab.get))
    th = pd.Series(taus_h).value_counts(normalize=True).sort_index()
    ts = pd.Series(taus_s).value_counts(normalize=True).sort_index()
    P(f"\n  bootstrap over cells (B={B}, block = cell):")
    P(f"      free-knot HINGE tau-hat:  " + ", ".join(f"{v:+.2f}:{p:.1%}" for v, p in th.items()))
    P(f"      free-knot STEP tau-hat:   " + ", ".join(f"{v:+.2f}:{p:.1%}" for v, p in ts.items()))
    P(f"      P(hinge tau-hat == 0.00) = {np.mean(np.array(taus_h) == 0.0):.1%}")
    wv = pd.Series(wins).value_counts(normalize=True)
    P(f"      AIC winner:               " + ", ".join(f"{k}:{p:.1%}" for k, p in wv.items()))
    S = pd.DataFrame([dict(model=k, params=v[2], tau=v[3], RSS=v[0], R2=1 - v[0] / tss,
                           AIC=aics[k], dAIC=aics[k] - a0,
                           boot_win_share=float(wv.get(k, 0.0))) for k, v in F.items()])
    S.to_csv(OUT / f"{STEM}.shape.csv", index=False)
    return S, winner, float(np.mean(np.array(taus_h) == 0.0))


# ============================================================ PART F — rule 8, live prices
def rule8(ref, G, RET):
    P("\n" + "=" * 118)
    P("PART F — RULE 8 WALK-FORWARD ON LIVE PRICES: k chosen on IS (<= 2016-12-31) only,")
    P("         evaluated untouched on 2017-2026.  Does WHICH READING of the crossing you")
    P("         adopt change what you earn?")
    P("=" * 118)
    ARMS = {
        "A_IS      (IS-Sharpe argmax k, per cell)": None,
        "A_EXACT   (k = +0.10, the unsmoothed crossing)": 0.10,
        "A_HM3     (k = +0.50, idea 439's headline window)": 0.50,
        "A_HM5     (k = +1.00, the widest window)": 1.00,
        "A_ZERO    (k =  0.00, no vol scaler — the control)": 0.00,
        "A_LIVE    (k = -0.50, RULES v1's live scaler)": -0.50,
    }
    idx = G.set_index(["panel", "cost", "share", "k"])
    rows, pooled = [], {}
    for label, kfix in ARMS.items():
        for pk in PANELS_ALL:
            for cost in COSTS:
                for m in SHARES:
                    if kfix is None:
                        sub = G[(G.panel == pk) & (G.cost == cost) & (G.share == m)]
                        kk = float(sub.loc[sub.IS_Sharpe.idxmax(), "k"])
                    else:
                        kk = kfix
                    r = RET[(pk, cost, kk, m)]
                    o = r.loc[OOS_START:]
                    oc, osh, odd = csd(o)
                    rows.append(dict(arm=label, panel=pk, cost=cost, share=m, k=kk,
                                     IS_Sharpe=float(idx.loc[(pk, cost, m, kk), "IS_Sharpe"]),
                                     OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd))
                    pooled.setdefault((label, "ALL"), []).append(r)
                    pooled.setdefault((label, pk), []).append(r)
    WF = pd.DataFrame(rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    def eq(series_list):
        df = pd.concat(series_list, axis=1).fillna(0.0)
        return df.mean(axis=1)

    P("\n  (i) POOLED equal-weight-of-cells book, 48 cells (3 panels x 2 costs x 8 shares).")
    P(f"  {'arm':52s} {'k':>18s} | {'FULL CAGR':>10s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'H1':>6s} {'H2':>6s} | {'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s}")
    prow = []
    for label in ARMS:
        r = eq(pooled[(label, "ALL")])
        cg, sh, dd = csd(r); oc, osh, odd = csd(r.loc[OOS_START:])
        h1, h2 = H.halves(r)
        ks = sorted(set(WF[WF.arm == label].k))
        kd = f"{ks[0]:+.2f}" if len(ks) == 1 else f"{len(ks)} distinct"
        P(f"  {label:52s} {kd:>18s} | {cg:10.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} "
          f"| {oc:9.2%} {osh:7.3f} {odd:8.2%}")
        prow.append(dict(arm=label, scope="ALL", k=kd, CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                         OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd))
    spy_all = eq([ref[p]["spy"] for p in PANELS_ALL])
    for nm, r in (("SPY (equal-weight of the 3 panels' SPY series)", spy_all),
                  ("RULES v2 (live) @10bps, pooled 3 panels",
                   eq([ref[p]["v2"][10.0] for p in PANELS_ALL])),
                  ("RULES v1 @10bps, pooled 3 panels",
                   eq([ref[p]["v1"][10.0] for p in PANELS_ALL]))):
        cg, sh, dd = csd(r); oc, osh, odd = csd(r.loc[OOS_START:]); h1, h2 = H.halves(r)
        P(f"  {nm:52s} {'—':>18s} | {cg:10.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} "
          f"| {oc:9.2%} {osh:7.3f} {odd:8.2%}")
        prow.append(dict(arm=nm, scope="ALL", k="—", CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                         OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd))

    P("\n  (ii) PER PANEL, 10 bps only, pooled over the 8 shares (SMALL439 = survivorship).")
    for pk in PANELS_ALL:
        P(f"\n      panel {pk}:")
        for label in ARMS:
            sl = [RET[(pk, 10.0, float(r.k), r.share)]
                  for _, r in WF[(WF.arm == label) & (WF.panel == pk) & (WF.cost == 10.0)].iterrows()]
            r = eq(sl)
            cg, sh, dd = csd(r); oc, osh, odd = csd(r.loc[OOS_START:]); h1, h2 = H.halves(r)
            P(f"      {label:52s} | {cg:9.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} "
              f"| {oc:9.2%} {osh:7.3f} {odd:8.2%}")
            prow.append(dict(arm=label, scope=pk, k="", CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                             OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd))
        sp = ref[pk]["spy"]
        cg, sh, dd = csd(sp); oc, osh, odd = csd(sp.loc[OOS_START:]); h1, h2 = H.halves(sp)
        P(f"      {'SPY':52s} | {cg:9.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} "
          f"| {oc:9.2%} {osh:7.3f} {odd:8.2%}")
        for nm, key in (("RULES v2 (live) @10bps", "v2"), ("RULES v1 @10bps", "v1")):
            r = ref[pk][key][10.0]
            cg, sh, dd = csd(r); oc, osh, odd = csd(r.loc[OOS_START:]); h1, h2 = H.halves(r)
            P(f"      {nm:52s} | {cg:9.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} "
              f"| {oc:9.2%} {osh:7.3f} {odd:8.2%}")

    P("\n  (iii) DOES THE READING PAY?  Adopting one crossing reading instead of another,")
    P("        pooled OOS, 48 cells:")
    base_ex = eq(pooled[("A_EXACT   (k = +0.10, the unsmoothed crossing)", "ALL")]).loc[OOS_START:]
    for label in ARMS:
        r = eq(pooled[(label, "ALL")]).loc[OOS_START:]
        a, b, c = csd(r); a0, b0, c0 = csd(base_ex)
        P(f"      {label:52s}  dOOS Sharpe vs A_EXACT {b-b0:+.4f}   dOOS CAGR "
          f"{(a-a0)*100:+.3f} pp   dOOS MaxDD {(abs(c)-abs(c0))*100:+.3f} pp")

    P("\n  (iv) PER-CELL: how often does the IS chooser beat the k = 0 control OOS?")
    a_is = WF[WF.arm.str.startswith("A_IS")].set_index(["panel", "cost", "share"])
    a_0 = WF[WF.arm.str.startswith("A_ZERO")].set_index(["panel", "cost", "share"])
    d = a_is.OOS_Sharpe - a_0.OOS_Sharpe
    P(f"      IS chooser beats the k=0 control on OOS Sharpe in {int((d>0).sum())} of {len(d)} "
      f"cells; mean margin {d.mean():+.4f} (sd {d.std(ddof=1):.4f})")
    dl = a_is.OOS_Sharpe - WF[WF.arm.str.startswith("A_LIVE")].set_index(
        ["panel", "cost", "share"]).OOS_Sharpe
    P(f"      IS chooser beats the LIVE k=-0.5 in {int((dl>0).sum())} of {len(dl)} cells; "
      f"mean margin {dl.mean():+.4f}")
    P(f"      IS-chosen k values: " + ", ".join(
        f"{v:+.2f}:{n}" for v, n in a_is.k.value_counts().sort_index().items()))

    # ------------------------------------------------------------------ KEEP paths
    P("\n  (v) KEEP PATHS on the pooled 48-cell book (protocol rule 4).")
    kp = []
    b2 = eq([ref[p]["v2"][10.0] for p in PANELS_ALL])
    b1 = eq([ref[p]["v1"][10.0] for p in PANELS_ALL])
    bars = H.bars_of(spy_all)
    P(f"      4b bars off the pooled SPY: H1>{bars['s1']:.3f} H2>{bars['s2']:.3f} "
      f"OOS>{bars['soos']:.3f} |MaxDD|<={0.60*abs(bars['sdd']):.2%} "
      f"CAGR>={0.70*bars['scagr']:.2%}")
    P(f"  {'arm':52s} {'4a v2':>7s} {'4a v1':>7s} {'4b':>5s}  failing")
    for label in ARMS:
        r = eq(pooled[(label, "ALL")])
        mg = H.margins(r, bars)
        fb = [b for b in ("H1", "H2", "OOS", "DD", "CAGR") if mg[b] <= 0]
        p4a2, p4a1 = H.pass4a(r, b2), H.pass4a(r, b1)
        P(f"  {label:52s} {str(p4a2):>7s} {str(p4a1):>7s} {str(len(fb)==0):>5s}  "
          f"{'|'.join(fb) if fb else '—'}")
        kp.append(dict(arm=label, pass4a_v2=p4a2, pass4a_v1=p4a1, pass4b=(len(fb) == 0),
                       failing="|".join(fb), **{f"margin_{k}": v for k, v in mg.items()}))
    K = pd.DataFrame(kp)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    pd.DataFrame(prow).to_csv(OUT / f"{STEM}.pooled.csv", index=False)
    P(f"\n      4a/4b passes among the {len(ARMS)} arms: "
      f"4a-v2 {int(K.pass4a_v2.sum())}, 4a-v1 {int(K.pass4a_v1.sum())}, "
      f"4b {int(K.pass4b.sum())}")
    return WF, K


# ============================================================================== main
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 440 — is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end   (cloud, 2026-09-08)")
    P("=" * 118)
    P(__doc__.split("QUESTION")[1].split("Deterministic")[0].strip())
    ref, G, RET = build_corpus()
    cu, grid, step = repro_gate(ref, G)
    g168, ch168, F, grid, step = exact_and_window(cu, grid, step, G)
    BOOT = bootstrap(cu, grid)
    S, winner, p_tau0 = shape_test(cu)
    WF, K = rule8(ref, G, RET)

    P("\n" + "=" * 118)
    P("VERDICT")
    P("=" * 118)
    P(f"  Q1 dSharpe(k=0) == 0 in all 32 cells with zero variance: "
      f"{'CONFIRMED' if cu.loc[cu.k == 0, 'dSharpe'].abs().max() == 0.0 else 'REFUTED'}")
    P(f"  Q2 exact (unsmoothed) crossing = {ch168:+.2f} = the smallest positive grid point: "
      f"{'CONFIRMED' if ch168 == 0.10 else 'REFUTED'}")
    P(f"  Q3 the windowed curve is an exact re-average of the per-k means (no new information)")
    P(f"  Q4 bootstrap P(crossing == 0.10): " +
      ", ".join(f"{r.block} {r.p_exact:.1%}" for _, r in BOOT.iterrows()))
    P(f"     plateau contrast separable from zero in "
      f"{int(((BOOT.plateau_lo > 0) | (BOOT.plateau_hi < 0)).sum())} of {len(BOOT)} blocks")
    P(f"  Q5 best shape by AIC: {winner};  P(free-knot hinge tau-hat == 0.00) = {p_tau0:.1%}")
    P(f"  KEEP paths: 4a-v2 {int(K.pass4a_v2.sum())}/{len(K)}, "
      f"4a-v1 {int(K.pass4a_v1.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}")
    P(f"\n  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
