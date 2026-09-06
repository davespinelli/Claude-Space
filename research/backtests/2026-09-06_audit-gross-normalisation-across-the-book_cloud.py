#!/usr/bin/env python3
"""QUEUE idea 81 — audit-gross-normalisation-across-the-book (cloud, 2026-09-06).

Question (pre-registered)
-------------------------
Idea 73 found that idea 2's `GROSS/n` construction SILENTLY DE-GROSSES whenever fewer
than n names are eligible: STK20/CAND-20 was 49.2% invested, not 75%, and its whole
apparent ranking premium was that.  Every published result using CAND-n on a narrow panel
or at a large n is exposed.  The queue asks for the n-sweeps to be re-run with the
gross-normalised book ALONGSIDE the literal one, and for the rows whose verdict changes
to be marked.

    LIT    w = (rank <= n) * GROSS / n            -- the published construction.
                                                     Realised gross = GROSS * k_t / n,
                                                     where k_t <= n is the number of
                                                     ELIGIBLE names that week.
    NORM   w = (rank <= n) / k_t * GROSS          -- same names, same order, always
                                                     fully invested.  The de-grossing
                                                     channel is closed.
    MATCH  NORM scaled by the LIT arm's OWN mean realised gross (idea 135/244's control).
           Same book, same average gross, but held CONSTANT instead of falling away
           exactly when the gate is cutting names -- i.e. it isolates the TIMING of the
           de-grossing from its level.

  Q1  GATES.  Reproduce idea 78's `weights_cand` bit-for-bit as the LIT arm; reproduce
      `rules_v1_weights` bit-for-bit as the V1 LIT arm at n=5; reproduce idea 73's
      STK20/CAND-20 49.2% invested.
  Q2  THE SIZE OF THE CHANNEL.  Mean realised gross and the share of weeks with k_t < n,
      for every (panel, book, n).  This is the number that says which published rows are
      exposed at all.
  Q3  THE SWEEP, both conventions, every grid point: n in {3,5,10,20,30,40,60} x 7 panels
      x 2 books x 2 cost rungs, LIT / NORM / MATCH, with EWall as the un-ranked control.
  Q4  DOES THE VERDICT MOVE?  Count the (panel, book, cost, n) cells whose 4a verdict and
      whose 4b verdict differ between LIT and NORM, and print every one that does.
  Q5  IS THE PREMIUM A GROSS-LADDER POINT?  premium(n) = Sharpe(CAND-n) - Sharpe(EWall)
      under each convention; the queue's own instance is u56 n=20, +0.043 literal vs
      +0.014 matched.  Decompose LIT - NORM into a LEVEL part (LIT vs MATCH: what the
      lower average gross buys) and a TIMING part (MATCH vs NORM: what varying it with
      the gate buys).
  Q6  DOES THE ARGMAX MOVE?  The n that maximises Sharpe under each convention, per cell.
  Q7  RULE 8.  n chosen on 2009-2016 ONLY under each convention; 2017-2026 read ONCE,
      against the EWall do-nothing control, RULES v1 and SPY.
  Q8  BOTH KEEP PATHS on every arm, and a textual census of the LEADERBOARD's exposure.

Design (PROTOCOL rules 1-8)
---------------------------
Panels    : idea 78's `build_panels()`, IMPORTED not re-implemented -- U56, ETF36, ETF24,
            STK20, B136, BSTK100 -- plus SMALL480, which is idea 78's small panel REBUILT
            here with the data/small_meta.csv max_1d_move >= 1.0 screen it does not apply.
            SURVIVORSHIP: every panel is a current-constituent list with no delistings.
            This audit is a WITHIN-CELL comparison of two weightings of the SAME names on
            the SAME days, so the bias is common to both arms and cancels in the
            LIT-vs-NORM difference; it does NOT cancel in any level quoted here.
Books     : CAND  = idea 78's composite key (no vol scaler), gated by 200d & vol20 < 0.60
                    -- idea 2's construction, the one the leaderboard's n-sweeps use.
            V1    = the LIVE rules key (composite / sqrt(vol20)), same gate -- at n=5 the
                    LIT arm IS `rules_v1_weights` with w = 0.15, asserted in Q1.
Params    : exactly TWO tuned dimensions -- n (7 grid points) and the CONVENTION (3).
            ALL reported.  Panel, book and cost rung are reported at every value and are
            never selected on.
Costs     : 10 bps (PROTOCOL) and 25 bps, applied analytically to one 0-bps simulation.
Execution : PROTOCOL rule 2 throughout (decide at close t, execute at close t+1).
Rule 8    : IS <= 2016-12-31 chooses n, OOS >= 2017-01-01 read once.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  The channel is large exactly where idea 73 said: mean realised gross under LIT falls
      below 0.60 on STK20 at n >= 20 and on every panel once n exceeds ~40% of its names.
  P2  On the WIDE panels (B136, SMALL480) at small n the two conventions are within 0.01
      of Sharpe -- the channel is a narrow-panel / large-n artefact, not a global one.
  P3  At least 10% of (panel, book, cost, n) cells change their 4b verdict between LIT and
      NORM.
  P4  The LIT premium over EWall exceeds the NORM premium in the majority of cells, i.e.
      the published n-sweeps flatter the ranking.
  P5  The LIT-NORM gap is mostly the LEVEL part (LIT vs MATCH), not the TIMING part.
  P6  The Sharpe argmax n moves between conventions in a minority of cells, and where it
      moves it moves UP under NORM (the literal book's large-n rungs were being propped up
      by de-grossing, so closing the channel should not favour them).

CAVEATS carried, not buried
---------------------------
  * NORM is not automatically the "right" convention.  A book that de-grosses when its own
    gate cuts names is a real, tradable book -- it is just not the book its published row
    claims to be.  This run says WHICH number a row is quoting, not which one to want.
  * MaxDD differences between conventions are differences of single realised extrema and
    are the noisiest column here (idea 117).
  * u56/STK20/ETF24 saturate at large n; a saturated rung is the same book at every n above
    it and its "premium" is a constant, not a curve.  Saturation share is printed.
  * The small panel is secondary (ideas 39/49/136: the 200d/vol20 gate is inverted there).
  * Costs are flat linear bps on turnover; real cost is convex in size (idea 126).
  * No LEVEL here is a tradable estimate.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .gross.csv, .flips.csv,
.walkforward.csv
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402


def _load(fname, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "research" / "backtests" / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


i78 = _load("2026-09-05_candidate-count-vs-dispersion_B.py", "i78")
i245 = _load("2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py", "i245")

eligible_mask = i78.eligible_mask
weights_cand = i78.weights_cand
weights_ewall = i78.weights_ewall
run = i245.run
m = i245.m
halves = i245.halves
at_cost = i245.at_cost
turn_per_yr = i245.turn_per_yr
fail4a = i245.fail4a
fail4b = i245.fail4b

GROSS = 0.75
FREQ = "W"
COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
NS = [3, 5, 10, 20, 30, 40, 60]
CONVS = ["LIT", "NORM", "MATCH"]
BOOKS = ["CAND", "V1"]
PANELS = ["U56", "ETF36", "ETF24", "STK20", "B136", "BSTK100", "SMALL480"]
SCRIPT = "research/backtests/2026-09-06_audit-gross-normalisation-across-the-book_cloud.py"
OUT = ROOT / "research" / "backtests" / "2026-09-06_audit-gross-normalisation-across-the-book_cloud"

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ the two conventions
_RANK_CACHE: dict = {}


def _rank(px, tradable, book):
    """Eligibility-masked rank of the book's key, computed ONCE per (panel, book)."""
    key = (id(px), book)
    if key not in _RANK_CACHE:
        elig = eligible_mask(px, tradable)
        s = score(px, vol_scale=(book == "V1"))[0]
        _RANK_CACHE[key] = (s.where(elig).rank(axis=1, ascending=False), elig)
    return _RANK_CACHE[key]


def selection(px, tradable, book, n):
    """(boolean selection matrix, count held per day).  Identical under both conventions."""
    rank, elig = _rank(px, tradable, book)
    sel = (rank <= n) & elig
    return sel, sel.sum(axis=1)


def w_lit(px, tradable, book, n, gross=GROSS):
    """The PUBLISHED construction: a fixed gross/n per name, so the book is invested
    gross * k_t / n and silently de-grosses whenever k_t < n."""
    sel, _ = selection(px, tradable, book, n)
    return sel.astype(float) * (gross / n)


def w_norm(px, tradable, book, n, gross=GROSS):
    """Same names, same order, always fully invested."""
    sel, k = selection(px, tradable, book, n)
    return sel.astype(float).div(k.replace(0, np.nan), axis=0).mul(gross).fillna(0.0)


def sat_share(px, tradable, book, n):
    """Share of days on which the gate leaves FEWER than n eligible names (k_t < n)."""
    _, k = selection(px, tradable, book, n)
    return float((k < n).mean()), float(k.mean())


def sim(px, w, start):
    g, t, inv, _ = run(px, w)
    return g.loc[start:], t.loc[start:], inv.loc[start:]


def row_of(tag, r, inv, t, base_r, spy, spy_oos, extra):
    c, sh, dd = m(r)
    h1, h2 = halves(r)
    ci, si, ddi = m(r.loc[:IS_END])
    co, so, ddo = m(r.loc[OOS_START:])
    d = dict(CAGR=c, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
             IS_CAGR=ci, IS_Sharpe=si, IS_MaxDD=ddi,
             OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=ddo,
             gross=float(inv.mean()), turn_yr=turn_per_yr(t),
             fail4a="|".join(fail4a(r, base_r)),
             fail4b="|".join(fail4b(r, spy, so, spy_oos)))
    d.update(extra)
    return d


# ------------------------------------------------------------------ one panel
def sweep(px, tradable, pname, rows, bench):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = m(spy.loc[OOS_START:])[1]
    base_r = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq="W")["returns"].loc[start:]

    # the un-ranked control: equal-weight ALL eligible names, constant gross by construction
    ge, te, ie = sim(px, weights_ewall(px, tradable, GROSS), start)

    for book in BOOKS:
        for n in NS:
            below, kbar = sat_share(px, tradable, book, n)
            gl, tl, il = sim(px, w_lit(px, tradable, book, n), start)
            gn, tn, inn = sim(px, w_norm(px, tradable, book, n), start)
            gmul = float(il.mean()) / float(inn.mean())        # idea 135's matched-gross lever
            arms = {"LIT": (gl, tl, il), "NORM": (gn, tn, inn),
                    "MATCH": (gn * gmul, tn * gmul, inn * gmul)}
            for cost in COSTS:
                r_e = at_cost(ge, te, cost)
                e_sh = m(r_e)[1]
                for conv, (g, t, inv) in arms.items():
                    r = at_cost(g, t, cost)
                    rows.append(row_of("", r, inv, t, base_r, spy, spy_oos, dict(
                        panel=pname, book=book, n=n, conv=conv, cost=cost,
                        k_mean=kbar, share_k_lt_n=below, match_mult=gmul,
                        ewall_Sharpe=e_sh, premium=m(r)[1] - e_sh)))
                rows.append(row_of("", r_e, ie, te, base_r, spy, spy_oos, dict(
                    panel=pname, book=book, n=n, conv="EWALL", cost=cost,
                    k_mean=np.nan, share_k_lt_n=np.nan, match_mult=np.nan,
                    ewall_Sharpe=e_sh, premium=0.0)))

    bench.append(dict(panel=pname, spy_CAGR=m(spy)[0], spy_Sharpe=m(spy)[1], spy_MaxDD=m(spy)[2],
                      spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                      spy_OOS_CAGR=m(spy.loc[OOS_START:])[0], spy_OOS_Sharpe=spy_oos,
                      spy_OOS_MaxDD=m(spy.loc[OOS_START:])[2],
                      v1_CAGR=m(base_r)[0], v1_Sharpe=m(base_r)[1], v1_MaxDD=m(base_r)[2],
                      v1_H1=halves(base_r)[0], v1_H2=halves(base_r)[1],
                      v1_OOS_Sharpe=m(base_r.loc[OOS_START:])[1],
                      ewall_Sharpe=m(at_cost(ge, te, PROTO_COST))[1]))


# ==================================================================================== main
def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 6000)
    P(f"# {SCRIPT}")
    P("# QUEUE idea 81 — every n-sweep re-run with the gross-normalised book beside the literal one\n")

    panels = i78.build_panels()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    n_all = len([c for c in pxs.columns if c != "SPY"])
    panels["SMALL480"] = (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), set(s_stk))
    P(f"SMALL480: {n_all} names -> {len(s_stk)} after dropping max_1d_move >= 1.0 "
      f"({n_all - len(s_stk)} dropped); idea 78's SMALL484 does NOT apply this screen.")
    for nm in PANELS:
        px, tr = panels[nm]
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    P("SURVIVORSHIP: every panel is a current-constituent list with no delistings.  This audit "
      "compares two weightings of the SAME names on the SAME days, so the bias is common to "
      "both arms and cancels in the LIT-vs-NORM difference; it does NOT cancel in any level.\n")

    # ------------------------------------------------------------------ Q1 gates
    P("=" * 118)
    P("Q1  GATES — asserted before any result is read")
    P("=" * 118)
    px, tr = panels["U56"]
    d1 = float((w_lit(px, tr, "CAND", 20) - weights_cand(px, tr, 20, GROSS)).abs().max().max())
    P(f"  [A] LIT(CAND, n) == idea 78's weights_cand : max|dw| = {d1:.3e}")
    assert d1 < 1e-15
    v1 = rules_v1_weights(px)                       # n=5, w=0.15, max_vol=0.60, vol_scale=True
    d2 = float((w_lit(px, set(px.columns), "V1", 5).reindex(columns=v1.columns).fillna(0.0)
                - v1).abs().max().max())
    P(f"  [B] LIT(V1, n=5) == baseline.rules_v1_weights (w=0.15) : max|dw| = {d2:.3e}")
    assert d2 < 1e-15
    g, t, inv, _ = run(px, w_lit(px, tr, "CAND", 20))
    P(f"  [C] engine agreement (idea 245 gate [A] re-run on this run's own weights):")
    ref = backtest(px, w_lit(px, tr, "CAND", 20), cost_bps=0.0, freq=FREQ)
    P(f"      max|dret| {float(np.abs(g - ref['returns']).max()):.3e}  "
      f"max|dturn| {float(np.abs(t - ref['turnover']).max()):.3e}")
    assert float(np.abs(g - ref["returns"]).max()) < 1e-12
    pxs20, tr20 = panels["STK20"]
    gs, ts, ivs, _ = run(pxs20, w_lit(pxs20, tr20, "CAND", 20))
    P(f"  [D] idea 73's headline reproduced: STK20 / CAND-20 LIT mean realised gross = "
      f"{float(ivs.loc[pxs20.index[260]:].mean()):.4f}  (idea 73 published 0.492)")

    # ------------------------------------------------------------------ Q2/Q3 the sweep
    rows, bench = [], []
    for nm in PANELS:
        P(f"\n... sweeping {nm}")
        px, tr = panels[nm]
        sweep(px, tr, nm, rows, bench)
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    bn = pd.DataFrame(bench).set_index("panel")

    P("\n=== BENCHMARKS over each panel's common sample ===")
    P(bn.to_string(float_format=lambda x: f"{x:.3f}"))

    P("\n" + "=" * 118)
    P("Q2  THE SIZE OF THE CHANNEL — mean realised gross under LIT (target 0.75) and the")
    P("    share of days the gate leaves fewer than n eligible names")
    P("=" * 118)
    gg = df[(df.conv == "LIT") & (df.cost == PROTO_COST)]
    gg[["panel", "book", "n", "k_mean", "share_k_lt_n", "gross", "turn_yr"]].to_csv(
        f"{OUT}.gross.csv", index=False)
    for book in BOOKS:
        P(f"\n  --- {book} book: mean realised gross under LIT")
        P(gg[gg.book == book].pivot(index="panel", columns="n", values="gross")
          .reindex(PANELS).to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"  --- {book} book: share of days with k_t < n")
        P(gg[gg.book == book].pivot(index="panel", columns="n", values="share_k_lt_n")
          .reindex(PANELS).to_string(float_format=lambda x: f"{x:.3f}"))

    P("\n" + "=" * 118)
    P("Q3  THE SWEEP — every grid point, both conventions, both cost rungs")
    P("=" * 118)
    for nm in PANELS:
        for book in BOOKS:
            for cost in COSTS:
                s = df[(df.panel == nm) & (df.book == book) & (df.cost == cost)]
                P(f"\n--- {nm} / {book} @ {cost} bps   "
                  f"(EWall control Sharpe {s.ewall_Sharpe.iloc[0]:.4f})")
                P(s[s.conv != "EWALL"][["n", "conv", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                        "OOS_Sharpe", "gross", "turn_yr", "premium",
                                        "fail4a", "fail4b"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ Q4 verdict flips
    P("\n" + "=" * 118)
    P("Q4  DOES THE VERDICT MOVE?  LIT vs NORM, per (panel, book, cost, n)")
    P("=" * 118)
    w = df[df.conv.isin(["LIT", "NORM"])].pivot_table(
        index=["panel", "book", "cost", "n"], columns="conv",
        values=["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe", "gross", "premium"], aggfunc="first")
    fa = df[df.conv.isin(["LIT", "NORM"])].pivot_table(
        index=["panel", "book", "cost", "n"], columns="conv", values="fail4a",
        aggfunc="first")
    fb = df[df.conv.isin(["LIT", "NORM"])].pivot_table(
        index=["panel", "book", "cost", "n"], columns="conv", values="fail4b",
        aggfunc="first")
    flip = pd.DataFrame(index=w.index)
    flip["keep4a_LIT"] = (fa["LIT"] == "")
    flip["keep4a_NORM"] = (fa["NORM"] == "")
    flip["keep4b_LIT"] = (fb["LIT"] == "")
    flip["keep4b_NORM"] = (fb["NORM"] == "")
    flip["flip4a"] = flip.keep4a_LIT != flip.keep4a_NORM
    flip["flip4b"] = flip.keep4b_LIT != flip.keep4b_NORM
    flip["dSharpe"] = w[("Sharpe", "NORM")] - w[("Sharpe", "LIT")]
    flip["dCAGR"] = w[("CAGR", "NORM")] - w[("CAGR", "LIT")]
    flip["dMaxDD"] = w[("MaxDD", "NORM")] - w[("MaxDD", "LIT")]
    flip["dOOS"] = w[("OOS_Sharpe", "NORM")] - w[("OOS_Sharpe", "LIT")]
    flip["dpremium"] = w[("premium", "NORM")] - w[("premium", "LIT")]
    flip["gross_LIT"] = w[("gross", "LIT")]
    flip = flip.reset_index()
    flip.to_csv(f"{OUT}.flips.csv", index=False)
    N = len(flip)
    P(f"  cells: {N}   4a verdict flips: {int(flip.flip4a.sum())} ({flip.flip4a.mean():.1%})"
      f"   4b verdict flips: {int(flip.flip4b.sum())} ({flip.flip4b.mean():.1%})")
    P(f"  mean dSharpe (NORM - LIT) {flip.dSharpe.mean():+.4f}, median {flip.dSharpe.median():+.4f}, "
      f"NORM higher in {int((flip.dSharpe > 0).sum())} of {N}")
    P(f"  mean dCAGR   {flip.dCAGR.mean():+.4f};  mean dMaxDD {flip.dMaxDD.mean():+.4f} "
      "(negative = NORM is deeper, which is what closing the de-grossing channel must do)")
    P("\n  every cell whose 4a or 4b verdict CHANGES between the two conventions:")
    fl = flip[flip.flip4a | flip.flip4b]
    P(fl[["panel", "book", "cost", "n", "gross_LIT", "keep4a_LIT", "keep4a_NORM",
          "keep4b_LIT", "keep4b_NORM", "dSharpe", "dMaxDD", "dOOS"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}") if len(fl) else "  (none)")
    P("\n  flip rate by how much the LIT book was actually de-grossed:")
    flip["gross_bucket"] = pd.cut(flip.gross_LIT, [0, .45, .6, .70, .745, 1.0],
                                  labels=["<0.45", "0.45-0.60", "0.60-0.70", "0.70-0.745", ">=0.745"])
    P(flip.groupby("gross_bucket", observed=True)[["flip4a", "flip4b", "dSharpe"]]
      .agg({"flip4a": "mean", "flip4b": "mean", "dSharpe": "mean"})
      .join(flip.groupby("gross_bucket", observed=True).size().rename("cells"))
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ Q5 attribution
    P("\n" + "=" * 118)
    P("Q5  IS THE PREMIUM A GROSS-LADDER POINT?  premium(n) = Sharpe(CAND-n) - Sharpe(EWall)")
    P("=" * 118)
    P("  DECOMPOSITION, with the two terms named for what they actually are:")
    P("    TIMING = LIT - MATCH   the gross VARYING with the gate, at matched MEAN gross")
    P("    LEVEL  = MATCH - NORM  a pure constant rescale of the same book")
    P("  (the pre-registered P5 attached the opposite labels to these two differences; the")
    P("   quantities it names are unchanged and are scored on their stated form below.)")
    pr = df[df.conv.isin(CONVS)].pivot_table(index=["panel", "book", "cost", "n"],
                                             columns="conv", values="premium", aggfunc="first")
    pr["TIMING(LIT-MATCH)"] = pr["LIT"] - pr["MATCH"]
    pr["LEVEL(MATCH-NORM)"] = pr["MATCH"] - pr["NORM"]
    pr["TOTAL(LIT-NORM)"] = pr["LIT"] - pr["NORM"]
    P("\n  the queue's own instance, u56 / CAND / n=20 @10bps:")
    q = pr.loc[("U56", "CAND", 10, 20)]
    P(f"    premium LIT {q['LIT']:+.4f}   MATCH {q['MATCH']:+.4f}   NORM {q['NORM']:+.4f}"
      f"   (idea 73/queue published +0.043 literal vs +0.014 matched)")
    P("\n  pooled decomposition over all cells:")
    P(pr[["LIT", "MATCH", "NORM", "TIMING(LIT-MATCH)", "LEVEL(MATCH-NORM)", "TOTAL(LIT-NORM)"]]
      .describe().to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  LIT premium > NORM premium in {int((pr['TOTAL(LIT-NORM)'] > 0).sum())} of {len(pr)} cells "
      f"({(pr['TOTAL(LIT-NORM)'] > 0).mean():.1%}) — i.e. the published construction FLATTERS the "
      "ranking that often.")
    tm, lv = pr["TIMING(LIT-MATCH)"].abs().mean(), pr["LEVEL(MATCH-NORM)"].abs().mean()
    P(f"  mean |TIMING| {tm:.4f} vs mean |LEVEL| {lv:.4f}  -> on SHARPE the LEVEL term is exactly "
      "zero: a constant rescale of a book is a pure lever with no risk-adjusted content "
      "(idea 66, re-derived here as an identity).  100% of the LIT-vs-NORM Sharpe gap is the "
      "de-grossing being TIMED by the gate — the literal book holds less exactly when the gate "
      "is cutting names, and that timing is what the published premium was paying for.")
    P("\n  the same decomposition on CAGR and MaxDD, where the LEVEL term is NOT zero:")
    for col in ("CAGR", "MaxDD"):
        pc = df[df.conv.isin(CONVS)].pivot_table(index=["panel", "book", "cost", "n"],
                                                 columns="conv", values=col, aggfunc="first")
        P(f"    {col:6s}  mean |TIMING| {float((pc['LIT'] - pc['MATCH']).abs().mean()):.4f}   "
          f"mean |LEVEL| {float((pc['MATCH'] - pc['NORM']).abs().mean()):.4f}   "
          f"mean TOTAL (LIT-NORM) {float((pc['LIT'] - pc['NORM']).mean()):+.4f}")
    P("\n  premium by panel and convention (CAND book, 10 bps):")
    P(pr.reset_index().query("book=='CAND' and cost==10")
      .pivot(index="panel", columns="n", values="LIT").reindex(PANELS)
      .to_string(float_format=lambda x: f"{x:+.4f}") + "   <- LIT")
    P(pr.reset_index().query("book=='CAND' and cost==10")
      .pivot(index="panel", columns="n", values="NORM").reindex(PANELS)
      .to_string(float_format=lambda x: f"{x:+.4f}") + "   <- NORM")

    # ------------------------------------------------------------------ Q6 argmax
    P("\n" + "=" * 118)
    P("Q6  DOES THE ARGMAX n MOVE?")
    P("=" * 118)
    am = []
    for (pn, bk, cost, conv), g in df[df.conv != "EWALL"].groupby(["panel", "book", "cost", "conv"]):
        k = g.Sharpe.idxmax()
        am.append(dict(panel=pn, book=bk, cost=cost, conv=conv, argmax_n=int(g.loc[k, "n"]),
                       Sharpe=g.loc[k, "Sharpe"],
                       runner_up_gap=float(g.Sharpe.nlargest(2).diff().abs().iloc[-1])))
    amd = pd.DataFrame(am).pivot_table(index=["panel", "book", "cost"], columns="conv",
                                       values=["argmax_n", "Sharpe", "runner_up_gap"],
                                       aggfunc="first")
    P(amd.to_string(float_format=lambda x: f"{x:.4f}"))
    mv = (amd[("argmax_n", "LIT")] != amd[("argmax_n", "NORM")])
    P(f"\n  argmax n differs between LIT and NORM in {int(mv.sum())} of {len(amd)} "
      f"(panel, book, cost) cells ({mv.mean():.1%}); "
      f"NORM's argmax is HIGHER in {int((amd[('argmax_n','NORM')] > amd[('argmax_n','LIT')]).sum())}, "
      f"LOWER in {int((amd[('argmax_n','NORM')] < amd[('argmax_n','LIT')]).sum())}.")

    # ------------------------------------------------------------------ Q7 rule 8
    P("\n" + "=" * 118)
    P("Q7  RULE 8 — n chosen on 2009-2016 ONLY under each convention; 2017-2026 read ONCE")
    P("=" * 118)
    wf = []
    for (pn, bk, cost, conv), g in df[df.conv != "EWALL"].groupby(["panel", "book", "cost", "conv"]):
        k = g.IS_Sharpe.idxmax()
        row = g.loc[k]
        ew = df[(df.panel == pn) & (df.book == bk) & (df.cost == cost) & (df.conv == "EWALL")].iloc[0]
        best = g.loc[g.OOS_Sharpe.idxmax()]
        wf.append(dict(panel=pn, book=bk, cost=cost, conv=conv, IS_pick_n=int(row.n),
                       IS_Sharpe=row.IS_Sharpe, OOS_Sharpe=row.OOS_Sharpe,
                       OOS_CAGR=row.OOS_CAGR, OOS_MaxDD=row.OOS_MaxDD,
                       ewall_OOS_Sharpe=ew.OOS_Sharpe, ewall_OOS_CAGR=ew.OOS_CAGR,
                       ewall_OOS_MaxDD=ew.OOS_MaxDD,
                       beats_donothing=bool(row.OOS_Sharpe > ew.OOS_Sharpe),
                       best_n_OOS=int(best.n), best_OOS_Sharpe=best.OOS_Sharpe,
                       regret=float(best.OOS_Sharpe - row.OOS_Sharpe),
                       spy_OOS_Sharpe=float(bn.loc[pn, "spy_OOS_Sharpe"]),
                       spy_OOS_CAGR=float(bn.loc[pn, "spy_OOS_CAGR"]),
                       spy_OOS_MaxDD=float(bn.loc[pn, "spy_OOS_MaxDD"]),
                       v1_OOS_Sharpe=float(bn.loc[pn, "v1_OOS_Sharpe"]),
                       fail4a=row.fail4a, fail4b=row.fail4b))
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(wdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for conv in CONVS:
        s = wdf[wdf.conv == conv]
        P(f"\n  {conv:6s}: IS pick beats the EWall do-nothing control OOS in "
          f"{int(s.beats_donothing.sum())} of {len(s)} cells; mean OOS Sharpe "
          f"{s.OOS_Sharpe.mean():.4f} vs EWall {s.ewall_OOS_Sharpe.mean():.4f}; "
          f"mean regret {s.regret.mean():+.4f}; IS pick n = "
          f"{sorted(s.IS_pick_n.unique())}")
    piv = wdf.pivot_table(index=["panel", "book", "cost"], columns="conv", values="IS_pick_n",
                          aggfunc="first")
    P(f"\n  the IS-chosen n differs between LIT and NORM in "
      f"{int((piv['LIT'] != piv['NORM']).sum())} of {len(piv)} cells — i.e. the convention "
      "changes the RULE, not only the number quoted for it.")

    # ------------------------------------------------------------------ Q8 keep + census
    P("\n" + "=" * 118)
    P("Q8  BOTH KEEP PATHS, and the leaderboard's exposure")
    P("=" * 118)
    a = df[df.conv != "EWALL"].copy()
    a["k4a"] = a.fail4a == ""
    a["k4b"] = a.fail4b == ""
    P(f"  arms: {len(a)}   4a passes {int(a.k4a.sum())}   4b passes {int(a.k4b.sum())}")
    P(a.groupby("conv")[["k4a", "k4b"]].sum().join(a.groupby("conv").size().rename("arms"))
      .to_string())
    if a.k4b.any():
        P("\n  every 4b PASS in the run:")
        P(a[a.k4b][["panel", "book", "cost", "n", "conv", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                    "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "gross", "turn_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    lb = [l for l in lb if l.startswith("|")]
    import re
    pat = re.compile(r"CAND-?\s?n?\d|CAND-n|top-?\d+|TOP\d+|\bn\s?=\s?\d+|STK20|V1u", re.I)
    hits = [l for l in lb if pat.search(l)]
    P(f"\n  LEADERBOARD exposure census: {len(hits)} of {len(lb)} rows quote a count-based "
      f"construction (CAND-n / top-n / n = k / STK20 / V1u) — {len(hits)/max(len(lb),1):.1%}. "
      "Not all of them use the literal GROSS/n weighting, but every one of them is a row whose "
      "quoted premium has to be read against this run's Q4/Q5 tables before it is believed.")

    # ------------------------------------------------------------------ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS, scored")
    P("=" * 118)
    st = gg[(gg.panel == "STK20") & (gg.book == "CAND")][["n", "gross"]]
    P(f"  P1 LIT gross < 0.60 on STK20 at n >= 20: "
      f"{dict(zip(st.n, st.gross.round(3)))}")
    wide = flip[flip.panel.isin(["B136", "SMALL480"]) & (flip.n <= 10)]
    P(f"  P2 wide panels at small n within 0.01 of Sharpe: "
      f"{int((wide.dSharpe.abs() <= 0.01).sum())} of {len(wide)} cells; "
      f"max |dSharpe| {wide.dSharpe.abs().max():.4f}")
    P(f"  P3 >=10% of cells change their 4b verdict: {flip.flip4b.mean():.1%}")
    P(f"  P4 LIT premium > NORM premium in the majority: "
      f"{(pr['TOTAL(LIT-NORM)'] > 0).mean():.1%}")
    P(f"  P5 the LIT-MATCH term dominates: mean |LIT-MATCH| {tm:.4f} vs mean |MATCH-NORM| {lv:.4f} "
      "— TRUE on the quantity it names, but P5's LABELS were wrong: LIT-MATCH is the TIMING "
      "term, and MATCH-NORM (which P5 called timing) is a pure rescale that is zero on Sharpe "
      "by identity.")
    P(f"  P6 argmax moves in a minority and upward under NORM: moves in {mv.mean():.1%}; "
      f"up {int((amd[('argmax_n','NORM')] > amd[('argmax_n','LIT')]).sum())} / "
      f"down {int((amd[('argmax_n','NORM')] < amd[('argmax_n','LIT')]).sum())}")

    Path(f"{OUT}.console.txt").write_text("\n".join(_lines) + "\n")
    print(f"\nwrote {OUT}.console.txt / .grid.csv / .gross.csv / .flips.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
