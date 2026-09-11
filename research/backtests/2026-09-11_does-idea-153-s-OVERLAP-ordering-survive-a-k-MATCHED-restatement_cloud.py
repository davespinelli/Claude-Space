#!/usr/bin/env python3
"""IDEA 684 (cloud) — does idea 153's OVERLAP ordering survive a k-MATCHED restatement?

QUESTION (queue).  Idea 525 found S2 (the INV-vs-NONE top-20 name overlap) is the record's only
published panel-property claim with a real width channel, and that it loads -0.919 on log k
against -0.421 on log breadth, i.e. it is a RAW PANEL WIDTH claim, not a breadth or an n_elig one.
Re-run idea 153's headline on panels matched on k and varied only in breadth (cap mix q), and
report what the published 0.694 / 0.425 / 0.269 ordering (U56 > B136 > SMALL439) becomes.

WHY IT MATTERS FOR CAPITAL.  S2 is the record's measure of "how much does the vol scaler change
what you hold".  Idea 153 read a low overlap on the small panel as a PANEL PROPERTY and that
reading is quoted downstream.  If S2 is really 1/k arithmetic, every downstream sentence that
treats it as a cap-mix fact is wrong, and the vol scaler's real cost has to be read off the BOOKS,
not off the overlap.  So this run prices the books beside the statistic.

DESIGN — the confound, stated.  A named panel carries k (its width) and its cap mix q at once.
top-20 of two scores drawn from k candidates overlap by ~20/k under independence, so ANY statistic
of the form |topN(A) & topN(B)|/N falls with k whatever the panel is made of.  The only way to
separate the two is to HOLD k and move q, which is what this run does.

PARAMETERS — exactly two, every grid point reported, neither tuned on an outcome:
  P1  k, the MATCHED PANEL WIDTH, 4 levels {20, 40, 80, 120}.  120 is the largest k the LARGE pool
      can supply at q=0 (B136 has 135 tradables); 20 is the record's standard book size.
  P2  q, the CAP MIX, 5 levels {0.00, 0.25, 0.50, 0.75, 1.00} = the small-cap share of the drawn
      panel.  q is the dial that moves breadth at FIXED k (the record's named panels read breadth
      0.657 at q=0 and 0.322 at q=1), and it is the ONLY thing varying inside a k row.
  Draws per (k, q) are FIXED at 6 and seeded (SEED=684), not swept.  Gross FIXED at the live 0.75,
  costs FIXED at PROTOCOL's 10 bps, weekly cadence, weights at close t applied t+1 (engine).

LEGS.
  [A] THE RESTATEMENT.  4 k x 5 q x 6 draws = 120 matched panels + the 3 named panels
      (U56, B136, SMALL439).  Each publishes k, Ebar, breadth=Ebar/k and S2 side by side.
      Read: S2 across q INSIDE each k row (the breadth channel with width held) against S2 across
      k (the width channel), plus the log-log regression idea 525 reported.
  [B] THE BOOKS.  On every panel, the KEEP-4b-candidate construction in both score variants —
      CAND20-NONE (top-20 by the unscaled composite, equal weight, gross 0.75: the 2026-09-04
      KEEP 4b book) and CAND20-INV (the same book with the live vol scaler restored) — at 10 bps,
      with full / halves / OOS metrics and BOTH KEEP paths against RULES v2 and SPY.  This is what
      S2 is supposed to be a proxy for; the run reports whether it is one.
  [C] RULE 8.  The score variant is chosen on 2009-2016 alone (per k x q cell, best mean IS
      Sharpe over that cell's 6 draws) and 2017-2026 is read ONCE.  OOS CAGR / Sharpe / MaxDD
      against RULES v2 (do-nothing) and SPY, pooled and per cell.

REPRODUCTION GATES (recorded, NEVER raising).  Idea 286/525's named-panel numbers under the same
eligibility definition (200d MA AND 20d ann. vol < 0.60, on weekly rebalance days, first 40
dropped): k 55 / 135 / 439, Ebar U56 ~36.1 and SMALL439 ~141.5, breadth ~0.6571 / ~0.6619 /
~0.3224, and 44 names dropped from the 483-name small panel by max_1d_move >= 1.0.  Idea 153's
published S2 ordering 0.694 / 0.425 / 0.269 is quoted as the target; the 2026-09-09 lane-B rerun
of the same statistic read 0.7983 / 0.5756 / 0.4010 (ordering reproduced, levels higher).

SURVIVORSHIP (idea 54).  Every pool here is CURRENT constituents only.  The sub-$2B panel is the
worst case: it is the survivors of a screen run today, so its LEVELS are optimistic.  The
matched-k CONTRASTS are the part of this run that survives that caveat, not the levels.

Deterministic; seeded draws only.  Writes <STEM>.{panels,grid,books,walkforward}.csv and
<STEM>.console.txt.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-11_does-idea-153-s-OVERLAP-ordering-survive-a-k-MATCHED-restatement_cloud"
KS = [20, 40, 80, 120]
QS = [0.00, 0.25, 0.50, 0.75, 1.00]
DRAWS = 6
SEED = 684
GROSS = 0.75
NBOOK = 20
COST_BPS, FREQ = 10, "W"
START = "2010-01-01"          # the small panel's first year; every panel uses the SAME window
OOS_START = "2017-01-01"
MAXVOL = 0.60

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ panels
def small_pool():
    """The 483-name sub-$2B panel with max_1d_move >= 1.0 dropped (PROTOCOL-mandated)."""
    px = load_universe(start=START, small=True, with_spy=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    tcol = "ticker" if "ticker" in meta.columns else meta.columns[0]
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str))
    keep = [c for c in px.columns if c != "SPY" and c not in bad]
    return px, keep, len(bad)


def gate_stats(px, cols):
    """Ebar = mean daily n_elig on rebalance days (first 40 dropped); breadth = Ebar / k."""
    sub = px[cols]
    above = sub > sub.rolling(200).mean()
    vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
    gate = above & (vol20 < MAXVOL)
    mask = rebalance_mask(sub.index, FREQ)
    cnt = gate.loc[mask.values].sum(axis=1).iloc[40:]
    ebar = float(cnt.mean())
    return ebar, ebar / len(cols)


def overlap_inv_none(px, cols, n=NBOOK):
    """Idea 153's statistic: mean over rebalance days of |topn(INV) & topn(NONE)| / n."""
    sub = px[cols]
    s0, above, vol20 = score(sub, vol_scale=False)
    gate = above & (vol20 < MAXVOL)
    s_inv = (s0 / vol20.clip(lower=0.08) ** 0.5).where(gate)
    s_non = s0.where(gate)
    mask = rebalance_mask(sub.index, FREQ)
    days = sub.index[mask.values][40:]
    ri = s_inv.loc[days].rank(axis=1, ascending=False)
    rn = s_non.loc[days].rank(axis=1, ascending=False)
    ok = (ri.notna().sum(axis=1) >= n) & (rn.notna().sum(axis=1) >= n)
    both = ((ri <= n) & (rn <= n)).sum(axis=1) / float(n)
    return float(both[ok].mean()) if ok.any() else np.nan


# ------------------------------------------------------------------ books
def cand_weights(n, vol_scale, gross=GROSS):
    """Top-n by the composite, EQUAL WEIGHT at constant gross (NORM convention: divide by the
    count actually held, so the gross ladder idea 244 found inside `gross/n` books is closed)."""
    def f(px):
        cols = [c for c in px.columns if c != "SPY"]
        sub = px[cols]
        s, above, vol20 = score(sub, vol_scale=vol_scale)
        elig = s.where(above & (vol20 < MAXVOL))
        rank = elig.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float)
        held = w.sum(axis=1).replace(0, np.nan)
        w = gross * w.div(held, axis=0).fillna(0.0)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


def v2_on(px):
    return rules_v2_weights(px.drop(columns=["SPY"], errors="ignore")).reindex(
        columns=px.columns).fillna(0.0)


def run(px, wfn):
    return backtest(px, wfn(px), cost_bps=COST_BPS, freq=FREQ)["returns"]


def full_row(tag, r):
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = r.loc[OOS_START:]
    mo = metrics(o)
    i = r.loc[:OOS_START]
    mi = metrics(i)
    return dict(tag=tag, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"], IS_Sharpe=mi["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def keep_paths(row, spy, v2):
    """PROTOCOL rule 4.  4a is judged against the LIVE book (RULES v2); 4b against SPY."""
    a = (row["H1"] > v2["H1"]) and (row["H2"] > v2["H2"]) and (row["MaxDD"] >= v2["MaxDD"])
    b = (row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and
         row["OOS_Sharpe"] > spy["OOS_Sharpe"] and
         row["MaxDD"] >= 0.60 * spy["MaxDD"] and
         row["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    rx = pd.Series(x[m]).rank().values
    ry = pd.Series(y[m]).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


def ols(y, X):
    """Least squares with an intercept; returns coefficient vector (intercept first)."""
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    y = np.asarray(y, float)
    m = np.isfinite(y) & np.isfinite(X).all(axis=1)
    beta, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
    return beta, int(m.sum())


# ================================================================== main
def main():
    P("=" * 100)
    P("IDEA 684 (cloud) — does idea 153's OVERLAP ordering survive a k-MATCHED restatement?")
    P("=" * 100)

    pxs, small_cols, n_dropped = small_pool()
    pxb = load_universe(start=START, broad=True)
    pxu = load_universe(start=START)
    large_cols = [c for c in pxb.columns if c != "SPY"]
    u56_cols = [c for c in pxu.columns if c != "SPY"]

    spy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]

    P(f"\npools: LARGE {len(large_cols)} (broad panel tradables)  SMALL {len(small_cols)} "
      f"(sub-$2B panel, {n_dropped} names dropped by max_1d_move >= 1.0)  U56 {len(u56_cols)}")
    P(f"window: {START} .. {pxs.index[-1].date()}   costs {COST_BPS} bps   cadence {FREQ}   "
      f"gross {GROSS}   book n={NBOOK}   draws {DRAWS}   seed {SEED}")

    # ---------------- reproduction gates (recorded, never raising)
    P("\n" + "-" * 100)
    P("REPRODUCTION GATES (recorded, non-raising)")
    P("-" * 100)
    named = {}
    for tag, px_, cols in (("U56", pxu, u56_cols), ("B136", pxb, large_cols),
                           ("SMALL439", pxs, small_cols)):
        e, b = gate_stats(px_, cols)
        named[tag] = dict(k=len(cols), Ebar=e, breadth=b)
        P(f"  {tag:9s} k={len(cols):4d}  Ebar={e:8.2f}  breadth={b:.4f}")
    P(f"  small-panel names dropped by max_1d_move >= 1.0: {n_dropped}   (idea 525 published 44)")
    P("  idea 525 published (own windows): k 55/135/439, Ebar 36.14/-/141.53, "
      "breadth 0.6571/0.6619/0.3224")
    P(f"  NOTE this run starts every panel at {START} for a MATCHED window, so Ebar/breadth "
      "differ from idea 525's per-panel natural starts; k is the gate that must match exactly.")

    # ---------------- LEG A: the matched-k restatement
    P("\n" + "=" * 100)
    P("LEG A — S2 (INV-vs-NONE top-20 overlap) on panels MATCHED on k, varied only in cap mix q")
    P("=" * 100)

    # named-panel S2 first: what idea 153's headline reads on today's data
    for tag, px_, cols in (("U56", pxu, u56_cols), ("B136", pxb, large_cols),
                           ("SMALL439", pxs, small_cols)):
        named[tag]["S2"] = overlap_inv_none(px_, cols)
    P(f"\n  idea 153 published S2 ordering U56 > B136 > SMALL439 = 0.694 / 0.425 / 0.269 "
      f"(spread 0.425)")
    P(f"  this run, NAMED panels, matched window: "
      f"{named['U56']['S2']:.4f} / {named['B136']['S2']:.4f} / {named['SMALL439']['S2']:.4f}   "
      f"spread {named['U56']['S2'] - named['SMALL439']['S2']:.4f}  -> "
      f"{'ORDERING REPRODUCED' if named['U56']['S2'] > named['B136']['S2'] > named['SMALL439']['S2'] else 'NOT reproduced'}")
    P(f"  ...but those panels differ in k by 8.0x (55 -> 439).  Everything below holds k.")

    rng = np.random.default_rng(SEED)
    prows, brows = [], []

    def panel_px(sc, lc):
        parts = []
        if sc:
            parts.append(pxs[sc])
        if lc:
            parts.append(pxb[lc])
        px = pd.concat(parts + [spy.rename("SPY")], axis=1)
        px = px.loc[START:].dropna(how="all").ffill()
        px = px.loc[pxs.index[0]:]
        return px[[c for c in (sc + lc)] + ["SPY"]].dropna(how="all")

    total = len(KS) * len(QS) * DRAWS
    done = 0
    for k in KS:
        for q in QS:
            ns = int(round(k * q))
            nl = k - ns
            if ns > len(small_cols) or nl > len(large_cols):
                P(f"  SKIP k={k} q={q}: needs {ns} small / {nl} large, pools are "
                  f"{len(small_cols)}/{len(large_cols)}")
                continue
            for d in range(DRAWS):
                sc = list(rng.choice(small_cols, ns, replace=False)) if ns else []
                lc = list(rng.choice(large_cols, nl, replace=False)) if nl else []
                px = panel_px(sc, lc)
                cols = [c for c in px.columns if c != "SPY"]
                ebar, breadth = gate_stats(px, cols)
                s2 = overlap_inv_none(px, cols)

                st = px.index[260]
                spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
                v2_r = full_row("v2", run(px, v2_on).loc[st:])
                cell = dict(k=k, q=q, draw=d, k_real=len(cols), Ebar=ebar, breadth=breadth, S2=s2)
                for vs, name in ((False, "CAND20-NONE"), (True, "CAND20-INV")):
                    r = run(px, cand_weights(NBOOK, vs)).loc[st:]
                    row = full_row(name, r)
                    a, b = keep_paths(row, spy_r, v2_r)
                    brows.append(dict(**cell, book=name,
                                      **{x: v for x, v in row.items() if x != "tag"},
                                      spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"],
                                      spy_DD=spy_r["MaxDD"], spy_H1=spy_r["H1"],
                                      spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                                      spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                                      v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                                      v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                                      v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                                      v2_IS=v2_r["IS_Sharpe"], pass4a=a, pass4b=b))
                prows.append(cell)
                done += 1
                if done % 20 == 0:
                    P(f"  ... {done}/{total} panels")

    pan = pd.DataFrame(prows)
    bk = pd.DataFrame(brows)
    pan.to_csv(f"{OUT}/{STEM}.panels.csv", index=False)
    bk.to_csv(f"{OUT}/{STEM}.books.csv", index=False)

    P("\n  THE GRID — every point reported, S2 mean over the 6 draws (sd in brackets):")
    g = pan.groupby(["k", "q"]).agg(S2=("S2", "mean"), S2sd=("S2", "std"),
                                    breadth=("breadth", "mean"), Ebar=("Ebar", "mean")).reset_index()
    g.to_csv(f"{OUT}/{STEM}.grid.csv", index=False)
    piv = g.pivot(index="k", columns="q", values="S2")
    pivb = g.pivot(index="k", columns="q", values="breadth")
    P("\n  S2 by (k rows, q columns):")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  breadth by (k rows, q columns)  [the dial q is actually moving]:")
    P(pivb.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  S2 sd across the 6 draws inside a cell:")
    P(g.pivot(index="k", columns="q", values="S2sd").to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  THE TWO CHANNELS, side by side:")
    within_k = piv.max(axis=1) - piv.min(axis=1)
    across_k = piv.max(axis=0) - piv.min(axis=0)
    for k in piv.index:
        P(f"    k={k:4d}: S2 spread across the WHOLE cap ladder q=0..1 = {within_k.loc[k]:.4f}"
          f"   (breadth moves {pivb.loc[k].max() - pivb.loc[k].min():+.4f})")
    for q in piv.columns:
        P(f"    q={q:.2f}: S2 spread across k=20..120                = {across_k.loc[q]:.4f}")
    P(f"\n    MEAN within-k (breadth) spread {within_k.mean():.4f}   vs   "
      f"MEAN across-k (width) spread {across_k.mean():.4f}   "
      f"ratio {across_k.mean() / max(within_k.mean(), 1e-12):.2f}x")

    P("\n  THE LOG-LOG REGRESSION idea 525 reported (its loadings: log k -0.919, log breadth -0.421):")
    y = np.log(pan.S2.values)
    beta, n = ols(y, [np.log(pan.k_real.values), np.log(pan.breadth.values)])
    P(f"    log S2 = {beta[0]:+.4f} {beta[1]:+.4f}*log k {beta[2]:+.4f}*log breadth   (N={n})")
    b1, _ = ols(y, [np.log(pan.k_real.values)])
    b2, _ = ols(y, [np.log(pan.breadth.values)])
    P(f"    log k ALONE      {b1[1]:+.4f}")
    P(f"    log breadth ALONE{b2[1]:+.4f}")
    P(f"    rho(S2, k) = {spearman(pan.k_real, pan.S2):+.4f}    "
      f"rho(S2, breadth) = {spearman(pan.breadth, pan.S2):+.4f}")
    inside = [spearman(sub.breadth, sub.S2) for _, sub in pan.groupby("k")]
    P(f"    rho(S2, breadth) INSIDE each matched-k row: "
      f"{' '.join(f'{v:+.4f}' for v in inside)}   mean {np.nanmean(inside):+.4f}")
    P(f"    20/k, the independence benchmark, by k: "
      f"{' '.join(f'{NBOOK / k:.4f}' for k in KS)}")
    P(f"    S2 at q=0 (all large) by k: {' '.join(f'{piv.loc[k, 0.0]:.4f}' for k in KS)}")
    P(f"    S2 at q=1 (all small) by k: {' '.join(f'{piv.loc[k, 1.0]:.4f}' for k in KS)}")

    P("\n  THE RESTATEMENT the queue asks for — idea 153's ordering read at MATCHED k:")
    for k in piv.index:
        r = piv.loc[k]
        ordered = r.loc[0.0] > r.loc[0.5] > r.loc[1.0]
        P(f"    k={k:4d}: q=0 {r.loc[0.0]:.4f} | q=0.5 {r.loc[0.5]:.4f} | q=1 {r.loc[1.0]:.4f}  "
          f"-> {'ordering HOLDS' if ordered else 'ordering DOES NOT hold'}"
          f"   (published spread 0.425, here {r.loc[0.0] - r.loc[1.0]:+.4f})")

    # ---------------- LEG B: the books
    P("\n" + "=" * 100)
    P("LEG B — THE BOOKS the statistic is supposed to be a proxy for (10 bps, both KEEP paths)")
    P("=" * 100)
    bb = bk.groupby(["book", "k"]).agg(CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"),
                                       MaxDD=("MaxDD", "mean"), H1=("H1", "mean"),
                                       H2=("H2", "mean"), OOS_S=("OOS_Sharpe", "mean"),
                                       p4a=("pass4a", "sum"), p4b=("pass4b", "sum"),
                                       N=("CAGR", "size")).reset_index()
    P("\n  by book x k (means over q and draws):")
    P(bb.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    bq = bk.groupby(["book", "q"]).agg(CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"),
                                       MaxDD=("MaxDD", "mean"), OOS_S=("OOS_Sharpe", "mean"),
                                       p4a=("pass4a", "sum"), p4b=("pass4b", "sum"),
                                       N=("CAGR", "size")).reset_index()
    P("\n  by book x q:")
    P(bq.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  KEEP PATHS over all {len(bk)} books:  4a {int(bk.pass4a.sum())}/{len(bk)}   "
      f"4b {int(bk.pass4b.sum())}/{len(bk)}")
    for nm, sub in bk.groupby("book"):
        P(f"    {nm:12s} 4a {int(sub.pass4a.sum()):3d}/{len(sub)}   4b {int(sub.pass4b.sum()):3d}/{len(sub)}")
    if bk.pass4b.any():
        P("\n  every 4b pass:")
        P(bk[bk.pass4b][["book", "k", "q", "draw", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "S2", "breadth"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  IS S2 A PROXY FOR THE BOOK DIFFERENCE?  per panel, NONE minus INV:")
    w = bk.pivot_table(index=["k", "q", "draw"], columns="book",
                       values=["Sharpe", "CAGR", "OOS_Sharpe", "MaxDD"])
    d_sh = (w[("Sharpe", "CAND20-NONE")] - w[("Sharpe", "CAND20-INV")]).reset_index(name="dS")
    d_sh = d_sh.merge(pan[["k", "q", "draw", "S2", "breadth", "k_real"]], on=["k", "q", "draw"])
    P(f"    dSharpe(NONE - INV): mean {d_sh.dS.mean():+.4f}  median {d_sh.dS.median():+.4f}  "
      f"positive {int((d_sh.dS > 0).sum())}/{len(d_sh)}")
    P(f"    rho(S2, |dSharpe|) = {spearman(d_sh.S2, d_sh.dS.abs()):+.4f}   "
      f"(S2 high = the two books hold the SAME names, so |dSharpe| should fall with S2)")
    ins = [spearman(s.S2, s.dS.abs()) for _, s in d_sh.groupby("k")]
    P(f"    the same rho INSIDE each matched-k row: {' '.join(f'{v:+.4f}' for v in ins)}"
      f"   mean {np.nanmean(ins):+.4f}")

    # ---------------- LEG C: rule 8
    P("\n" + "=" * 100)
    P("LEG C — RULE 8 WALK-FORWARD: score variant chosen on 2009-2016, 2017-2026 read ONCE")
    P("=" * 100)
    wrows = []
    for (k, q), sub in bk.groupby(["k", "q"]):
        iss = sub.groupby("book").IS_Sharpe.mean()
        pick = iss.idxmax()
        sel = sub[sub.book == pick]
        alt = sub[sub.book != pick]
        wrows.append(dict(k=k, q=q, pick=pick, IS_none=iss.get("CAND20-NONE", np.nan),
                          IS_inv=iss.get("CAND20-INV", np.nan),
                          OOS_CAGR=sel.OOS_CAGR.mean(), OOS_Sharpe=sel.OOS_Sharpe.mean(),
                          OOS_MaxDD=sel.OOS_MaxDD.mean(),
                          OOS_Sharpe_alt=alt.OOS_Sharpe.mean(),
                          v2_OOS_CAGR=sub.v2_OOS_CAGR.mean(), v2_OOS_Sharpe=sub.v2_OOS_S.mean(),
                          v2_OOS_MaxDD=sub.v2_OOS_DD.mean(),
                          spy_OOS_CAGR=sub.spy_OOS_CAGR.mean(), spy_OOS_Sharpe=sub.spy_OOS_S.mean(),
                          spy_OOS_MaxDD=sub.spy_OOS_DD.mean()))
    wf = pd.DataFrame(wrows)
    wf["vs_v2"] = wf.OOS_Sharpe - wf.v2_OOS_Sharpe
    wf["vs_spy"] = wf.OOS_Sharpe - wf.spy_OOS_Sharpe
    wf["vs_alt"] = wf.OOS_Sharpe - wf.OOS_Sharpe_alt
    wf.to_csv(f"{OUT}/{STEM}.walkforward.csv", index=False)
    P("\n" + wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  IS pick = CAND20-NONE in {int((wf.pick == 'CAND20-NONE').sum())} of {len(wf)} cells "
      f"(the 2026-09-04 KEEP 4b book); CAND20-INV in {int((wf.pick == 'CAND20-INV').sum())}.")
    P(f"  POOLED OOS 2017-2026, equal weight over the {len(wf)} cells:")
    P(f"    rule-8 pick   CAGR {wf.OOS_CAGR.mean():7.2%}  Sharpe {wf.OOS_Sharpe.mean():6.3f}  "
      f"MaxDD {wf.OOS_MaxDD.mean():7.2%}")
    P(f"    the REJECTED  CAGR {'':7s}  Sharpe {wf.OOS_Sharpe_alt.mean():6.3f}")
    P(f"    RULES v2      CAGR {wf.v2_OOS_CAGR.mean():7.2%}  Sharpe {wf.v2_OOS_Sharpe.mean():6.3f}  "
      f"MaxDD {wf.v2_OOS_MaxDD.mean():7.2%}")
    P(f"    SPY           CAGR {wf.spy_OOS_CAGR.mean():7.2%}  Sharpe {wf.spy_OOS_Sharpe.mean():6.3f}  "
      f"MaxDD {wf.spy_OOS_MaxDD.mean():7.2%}")
    P(f"    pick beats RULES v2 OOS in {int((wf.vs_v2 > 0).sum())}/{len(wf)} cells "
      f"(median {wf.vs_v2.median():+.4f});  beats SPY in {int((wf.vs_spy > 0).sum())}/{len(wf)} "
      f"(median {wf.vs_spy.median():+.4f});  beats the variant it REJECTED in "
      f"{int((wf.vs_alt > 0).sum())}/{len(wf)} (median {wf.vs_alt.median():+.4f})")

    P("\n" + "=" * 100)
    P("SURVIVORSHIP: all pools are current constituents; the sub-$2B panel is a screen run today,")
    P("so q=1 LEVELS are optimistic.  The matched-k CONTRASTS are what survives that caveat.")
    P("=" * 100)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
