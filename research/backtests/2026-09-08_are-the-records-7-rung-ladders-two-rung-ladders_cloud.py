#!/usr/bin/env python3
"""Idea 454 — are-the-record's-7-rung-ladders-two-rung-ladders (cloud lane, 2026-09-08).

Pre-registered question (QUEUE 454): idea 231 found the two ENDPOINT rungs reproduce the full
7-rung cost ladder's RE-RANK verdict in 8,529 of 8,529 cells (35 cells carry an interior-only
argmax that never changes the verdict).  PRICE THE DELETION: re-cost the record's own cost
ladders at 2 rungs, report the compute actually saved, and name the exact cells where an
interior rung was load-bearing for anything ELSE — the LEVEL of the quoted Sharpe, the KEEP
pass (4a/4b), or the 4b bar that binds.

Corpus: the record's published cost-ladder census, rebuilt end to end from prices — 3 panels x
3 books x their dials = 33 cells, the same corpus idea 230 published
(2026-09-06_is-cadence-the-only-cost-chooser-on-other-books_cloud.census.csv) and the same
construction idea 228 used.  Every ladder is the record's standard rung set
0/5/10/15/20/25/30 bps.  Nothing is selected: all 33 cells and all grid points are reported.

TWO tuned parameters only, exactly as the queue states:
    RUNG PAIR  — which 2 rungs replace the 7 ({0,30} endpoints, plus 4 alternatives)
    TOLERANCE  — the Sharpe tolerance at which an interpolated interior rung counts as
                 "reproduced" (0.000 / 0.001 / 0.005 / 0.010 / 0.020 / 0.050)
ALL grid points of both are reported (.pairs.csv, .tolerance.csv).  Nothing else is tuned:
panels, books, dials, dial grids, rungs and the two KEEP paths are the record's own.

What "load-bearing" is tested to mean, one test each:
  (L) LEVEL     — the interior Sharpe vs the straight line between the pair's endpoints.
                  net(c) = gross - turnover*c/1e4 is EXACTLY linear in c, so any residual is
                  the curvature of Sharpe(net) = mean/std, not of the return stream.
  (K) KEEP      — the 4a/4b pass at PROTOCOL's binding 10 bps rung.  An endpoint pair
                  RECOVERS it only when both endpoints already agree on the verdict; when
                  they disagree the interior rung is the only thing that decides.
  (B) 4b BAR    — which 4b bar fails at 10 bps, same recovery test.
  (F) FIRST MOVE— the rung at which a re-ranking ladder first re-ranks: unrecoverable from a
                  pair by construction; counted, then checked against (L)/(K)/(B).
  (C) COMPUTE   — measured, not assumed: wall-clock of the simulations vs the per-rung
                  scoring, since all 7 rungs share ONE simulation under the net identity.

PROTOCOL: 10 bps is the binding cost, weights at t applied at t+1 (engine convention, and the
net identity is asserted against engine.backtest at 10 bps), rule 8 walk-forward always run
(dial chosen on 2009-2016, 2017-2026 read once), both KEEP paths evaluated — 4a against the
LIVE RULES v2 baseline (and RULES v1 kept for continuity with the pre-2026-09-06 record) and
4b against SPY.

SURVIVORSHIP: B136 and SMALL439 are current constituents of their screens only
(data/SMALL_PANEL_README.md, idea 54); the bias runs in favour of every long book quoted here.
SMALL439 = the sub-$2B panel with every ticker whose max_1d_move >= 1.0 dropped per
data/small_meta.csv, as the standing screen requires.

Outputs (all committed):
    .grid.csv       every (panel, book, dial, value, rung): turnover, CAGR/Sharpe/MaxDD, H1/H2,
                    IS/OOS, 4a and 4b pass + failing bar
    .census.csv     per cell: full-ladder argmaxes, re-rank verdict, first move, interior-only
                    argmax flag
    .pairs.csv      per (cell, rung pair): re-rank agreement, max level residual, KEEP and 4b
                    bar recovery
    .tolerance.csv  the tolerance grid: cells reproduced at each tolerance, per pair
    .loadbearing.csv every grid point where an interior rung decides a KEEP or a 4b bar
    .walkforward.csv rule 8: the true 10-bps chooser vs the 2-rung interpolated chooser, OOS
                    Sharpe/CAGR/MaxDD vs RULES v2, RULES v1 and SPY
    .compute.csv    measured seconds: simulation vs per-rung scoring
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, metrics                                            # noqa: E402

OUT = Path(__file__).with_suffix("")
RUNGS = [0, 5, 10, 15, 20, 25, 30]
BINDING = 10                       # PROTOCOL rule 2
OOS_START = "2017-01-01"
IS_END = "2016-12-31"

# ---- tuned parameter 1: the rung pair that replaces the 7-rung ladder
PAIRS = [(0, 30), (0, 10), (10, 30), (0, 20), (5, 25)]
# ---- tuned parameter 2: the Sharpe tolerance for "the interior is reproduced"
TOLS = [0.000, 0.001, 0.005, 0.010, 0.020, 0.050]

DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1)
DIAL_VALUES = {
    "N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
    "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
    "K": [1, 2, 3, 4, 6, 8, 13],
}
BOOKS = ["TOPN", "V1C", "EWALL"]
BOOK_DIALS = {"TOPN": ["N", "G", "V", "K"], "V1C": ["N", "G", "V", "K"],
              "EWALL": ["G", "V", "K"]}


# ---------------------------------------------------------------- simulation (idea 230's)
def week_mask(idx, k):
    per = idx.to_period("W")
    s = pd.Series(per, index=idx)
    last = (s != s.shift(-1)).values
    if k == 1:
        return last
    ordinal = pd.Series(pd.factorize(per)[0], index=idx).values
    return last & ((ordinal % k) == 0)


def simulate(px, W, mask):
    """engine.backtest's loop with an arbitrary rebalance mask; GROSS returns + turnover."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    gross = pd.Series((held * rets).sum(axis=1), index=px.index)
    return gross, pd.Series(turn, index=px.index)


def eligible(px, ma, vol20, g, max_vol):
    if g == 0:
        above = px > ma
    else:
        sig = pd.DataFrame(np.where(px > ma * (1 + g), 1.0,
                           np.where(px < ma * (1 - g), 0.0, np.nan)),
                           index=px.index, columns=px.columns)
        above = sig.ffill().fillna(0.0) > 0.5
    return above & (vol20 < max_vol)


def book_weights(book, px, keys, ma, vol20, n, g, max_vol):
    el = eligible(px, ma, vol20, g, max_vol)
    if book == "EWALL":
        w = el.astype(float)
        cnt = w.sum(axis=1)
        return w.div(cnt.where(cnt > 0), axis=0).fillna(0.0)
    key = keys["comp"] if book == "TOPN" else keys["v1score"]
    rank = key.where(el).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) / n


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    """4a: Sharpe > the live baseline in BOTH halves and MaxDD no worse."""
    fail = []
    if not s["H1"] > b["H1"]: fail.append("H1")
    if not s["H2"] > b["H2"]: fail.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: fail.append("DD")
    return ",".join(fail)


def bars_4b(s, spy, oos_s, oos_spy):
    """4b: Sharpe > SPY in both halves AND OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's."""
    fail = []
    if not s["H1"] > spy["H1"]: fail.append("H1")
    if not s["H2"] > spy["H2"]: fail.append("H2")
    if not oos_s > oos_spy: fail.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: fail.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fail.append("CAGR")
    return ",".join(fail)


def small_screened():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
          f"{len(keep) - 1} names + SPY remain", flush=True)
    return px[keep]


def panels():
    yield "U56", load_universe()
    yield "B136", load_universe(broad=True)
    yield "SMALL439", small_screened()


def interp(lo, hi, c, v_lo, v_hi):
    """Linear interpolation of a value read at rungs lo and hi, evaluated at rung c."""
    return v_lo + (v_hi - v_lo) * (c - lo) / (hi - lo)


def main():
    t0 = time.time()
    grid, census, pair_rows, lb_rows, wf_rows, ident, comp_rows = [], [], [], [], [], [], []

    for pname, px in panels():
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))     # exact: recover the composite
        v1score, _, _ = score(px, vol_scale=True)
        keys = dict(comp=comp, v1score=v1score)
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos_m = metrics(spy_r.loc[OOS_START:])
        spy_oos = spy_oos_m["Sharpe"]

        # --- both baselines, per rung.  4a is judged against RULES v2 (live since 2026-09-06);
        #     RULES v1 is kept as a continuity row for the pre-2026-09-06 record.
        b2g, b2t = simulate(px, rules_v2_weights(px), week_mask(px.index, 1))
        base2 = {c: stats(net(b2g, b2t, c).loc[start:]) for c in RUNGS}
        base2_oos = {c: metrics(net(b2g, b2t, c).loc[OOS_START:]) for c in RUNGS}
        b1g, b1t = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base1 = {c: stats(net(b1g, b1t, c).loc[start:]) for c in RUNGS}
        base1_oos = {c: metrics(net(b1g, b1t, c).loc[OOS_START:]) for c in RUNGS}

        eng = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append((pname, "RULESv2",
                      float(np.abs(eng - net(b2g, b2t, 10).loc[start:]).max())))
        eng1 = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append((pname, "RULESv1",
                      float(np.abs(eng1 - net(b1g, b1t, 10).loc[start:]).max())))

        sims, t_sim, t_score = {}, 0.0, 0.0
        for book in BOOKS:
            for dial in BOOK_DIALS[book]:
                for v in DIAL_VALUES[dial]:
                    kw = dict(DEFAULTS); kw[dial] = v
                    if dial == "N" and v > px.shape[1] - 1:
                        continue
                    sig = (book, kw["N"] if book != "EWALL" else -1, kw["G"], kw["V"], kw["K"])
                    if sig not in sims:
                        ts = time.time()
                        W = book_weights(book, px, keys, ma, vol20, kw["N"], kw["G"], kw["V"])
                        g_, t_ = simulate(px, W, week_mask(px.index, kw["K"]))
                        sims[sig] = (g_.loc[start:], t_.loc[start:])
                        t_sim += time.time() - ts
                    g_s, t_s = sims[sig]
                    yrs = len(g_s) / 252
                    ts = time.time()
                    for c in RUNGS:
                        r = net(g_s, t_s, c)
                        st = stats(r)
                        o = metrics(r.loc[OOS_START:])
                        grid.append(dict(panel=pname, book=book, dial=dial, value=v, bps=c,
                                         turn_yr=t_s.sum() / yrs, **st,
                                         OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"],
                                         OOS_MaxDD=o["MaxDD"],
                                         IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                         fail4a=bars_4a(st, base2[c]),
                                         fail4a_v1=bars_4a(st, base1[c]),
                                         fail4b=bars_4b(st, spy_s, o["Sharpe"], spy_oos)))
                    t_score += time.time() - ts

                # ---------------- census for this cell (the full 7-rung ladder) ------------
                g = pd.DataFrame([x for x in grid if x["panel"] == pname
                                  and x["book"] == book and x["dial"] == dial])
                vals = sorted(g["value"].unique())
                sh = {c: g[g.bps == c].set_index("value")["Sharpe"].reindex(vals) for c in RUNGS}
                arg = {c: sh[c].idxmax() for c in RUNGS}
                rerank = len(set(arg.values())) > 1
                interior_only = (arg[0] == arg[30]) and len({arg[c] for c in RUNGS}) > 1
                census.append(dict(panel=pname, book=book, dial=dial, n_values=len(vals),
                                   **{f"argmax_{c}bps": arg[c] for c in RUNGS},
                                   n_distinct_argmax=len(set(arg.values())), rerankable=rerank,
                                   first_move_bps=next((c for c in RUNGS if arg[c] != arg[0]),
                                                       np.nan),
                                   interior_only_argmax=interior_only,
                                   sharpe_range_10bps=float(sh[10].max() - sh[10].min())))

                # ---------------- price the deletion, per rung pair -----------------------
                for lo, hi in PAIRS:
                    inter = [c for c in RUNGS if lo < c < hi]
                    pair_rerank = arg[lo] != arg[hi]
                    # (L) level residual: interior Sharpe vs the line between the endpoints
                    res = 0.0
                    for c in inter:
                        pred = interp(lo, hi, c, sh[lo], sh[hi])
                        res = max(res, float((sh[c] - pred).abs().max()))
                    # (L') does the interpolated argmax at the binding rung match the true one?
                    if lo <= BINDING <= hi:
                        pred10 = interp(lo, hi, BINDING, sh[lo], sh[hi])
                        argmax10_ok = bool(pred10.idxmax() == arg[BINDING])
                        lvl10 = float((sh[BINDING] - pred10).abs().max())
                    else:
                        argmax10_ok, lvl10 = np.nan, np.nan
                    # (K)/(B) recovery at the binding rung: endpoints must already agree
                    sub = g.set_index(["value", "bps"])
                    k4a = k4b = bar_ok = 0
                    n_undet_4a = n_undet_4b = n_undet_bar = 0
                    for v in vals:
                        a_lo, a_hi = sub.loc[(v, lo)], sub.loc[(v, hi)]
                        a_10 = sub.loc[(v, BINDING)]
                        agree4a = (a_lo.fail4a == "") == (a_hi.fail4a == "")
                        agree4b = (a_lo.fail4b == "") == (a_hi.fail4b == "")
                        agreebar = a_lo.fail4b == a_hi.fail4b
                        if agree4a:
                            k4a += int((a_10.fail4a == "") == (a_lo.fail4a == ""))
                        else:
                            n_undet_4a += 1
                        if agree4b:
                            k4b += int((a_10.fail4b == "") == (a_lo.fail4b == ""))
                        else:
                            n_undet_4b += 1
                        if agreebar:
                            bar_ok += int(a_10.fail4b == a_lo.fail4b)
                        else:
                            n_undet_bar += 1
                        if (lo, hi) == (0, 30) and (not agree4a or not agree4b or not agreebar):
                            lb_rows.append(dict(panel=pname, book=book, dial=dial, value=v,
                                                what=",".join(
                                                    [w for w, ok in (("4a", agree4a),
                                                                     ("4b", agree4b),
                                                                     ("4b_bar", agreebar))
                                                     if not ok]),
                                                fail4a_lo=a_lo.fail4a, fail4a_10=a_10.fail4a,
                                                fail4a_hi=a_hi.fail4a,
                                                fail4b_lo=a_lo.fail4b, fail4b_10=a_10.fail4b,
                                                fail4b_hi=a_hi.fail4b,
                                                Sharpe_10=a_10.Sharpe, turn_yr=a_10.turn_yr))
                    pair_rows.append(dict(panel=pname, book=book, dial=dial, pair=f"{lo}-{hi}",
                                          n_values=len(vals), full_rerank=rerank,
                                          pair_rerank=pair_rerank,
                                          rerank_agrees=bool(pair_rerank == rerank),
                                          max_level_residual=res, level_residual_at_10=lvl10,
                                          interp_argmax10_ok=argmax10_ok,
                                          keep4a_recovered=k4a, keep4a_undetermined=n_undet_4a,
                                          keep4b_recovered=k4b, keep4b_undetermined=n_undet_4b,
                                          bar_recovered=bar_ok, bar_undetermined=n_undet_bar))

                # ---------------- rule 8 walk-forward: true vs 2-rung chooser --------------
                def _sig(v):
                    kw = dict(DEFAULTS); kw[dial] = v
                    return (book, kw["N"] if book != "EWALL" else -1,
                            kw["G"], kw["V"], kw["K"])
                keyed = {v: sims[_sig(v)] for v in vals}
                is_sh = {c: {} for c in RUNGS}
                for c in RUNGS:
                    for v, (a, b) in keyed.items():
                        is_sh[c][v] = metrics(net(a, b, c).loc[:IS_END])["Sharpe"]
                oos_at = {}
                for c in RUNGS:
                    oos_at[c] = {v: metrics(net(a, b, c).loc[OOS_START:])
                                 for v, (a, b) in keyed.items()}
                for lo, hi in PAIRS:
                    if not lo <= BINDING <= hi:
                        continue
                    true_pick = max(is_sh[BINDING], key=is_sh[BINDING].get)
                    ip = {v: interp(lo, hi, BINDING, is_sh[lo][v], is_sh[hi][v]) for v in vals}
                    pair_pick = max(ip, key=ip.get)
                    o = oos_at[BINDING]
                    dn = DEFAULTS[dial]
                    wf_rows.append(dict(
                        panel=pname, book=book, dial=dial, pair=f"{lo}-{hi}",
                        true_pick=true_pick, pair_pick=pair_pick,
                        same_pick=bool(true_pick == pair_pick), do_nothing=dn,
                        true_OOS_Sharpe=o[true_pick]["Sharpe"],
                        true_OOS_CAGR=o[true_pick]["CAGR"],
                        true_OOS_MaxDD=o[true_pick]["MaxDD"],
                        pair_OOS_Sharpe=o[pair_pick]["Sharpe"],
                        pair_OOS_CAGR=o[pair_pick]["CAGR"],
                        pair_OOS_MaxDD=o[pair_pick]["MaxDD"],
                        dn_OOS_Sharpe=o[dn]["Sharpe"], dn_OOS_CAGR=o[dn]["CAGR"],
                        dn_OOS_MaxDD=o[dn]["MaxDD"],
                        oracle_OOS_Sharpe=max(x["Sharpe"] for x in o.values()),
                        d_pair_minus_true=o[pair_pick]["Sharpe"] - o[true_pick]["Sharpe"],
                        basev2_OOS_Sharpe=base2_oos[BINDING]["Sharpe"],
                        basev2_OOS_CAGR=base2_oos[BINDING]["CAGR"],
                        basev2_OOS_MaxDD=base2_oos[BINDING]["MaxDD"],
                        basev1_OOS_Sharpe=base1_oos[BINDING]["Sharpe"],
                        spy_OOS_Sharpe=spy_oos, spy_OOS_CAGR=spy_oos_m["CAGR"],
                        spy_OOS_MaxDD=spy_oos_m["MaxDD"]))
            print(f"  {pname}/{book}: {time.time()-t0:.0f}s", flush=True)
        comp_rows.append(dict(panel=pname, n_sims=len(sims), sim_seconds=t_sim,
                              score7_seconds=t_score,
                              score_seconds_per_rung=t_score / len(RUNGS)))
        print(f"{pname}: done {time.time()-t0:.0f}s ({len(sims)} sims, "
              f"sim {t_sim:.0f}s / score {t_score:.0f}s)", flush=True)

    G = pd.DataFrame(grid); C = pd.DataFrame(census); P = pd.DataFrame(pair_rows)
    WF = pd.DataFrame(wf_rows); LB = pd.DataFrame(lb_rows); CP = pd.DataFrame(comp_rows)
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.census.csv", index=False)
    P.to_csv(f"{OUT}.pairs.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    LB.to_csv(f"{OUT}.loadbearing.csv", index=False)
    CP.to_csv(f"{OUT}.compute.csv", index=False)

    print("\n=== GATE: net identity vs engine.backtest at 10 bps (max abs daily diff) ===")
    for p, b, d in ident:
        print(f"  {p:9s} {b:8s} {d:.3e}")

    print(f"\n=== CORPUS: {len(C)} cells, {len(G)} grid points "
          f"({len(G)//len(RUNGS)} arms x {len(RUNGS)} rungs) ===")
    print(C[["panel", "book", "dial", "n_values"] + [f"argmax_{c}bps" for c in RUNGS]
            + ["n_distinct_argmax", "rerankable", "first_move_bps", "interior_only_argmax",
               "sharpe_range_10bps"]].to_string(index=False,
                                                float_format=lambda x: f"{x:.3f}"))
    print(f"\nre-rankable cells: {int(C.rerankable.sum())} of {len(C)}; "
          f"interior-only argmax cells: {int(C.interior_only_argmax.sum())}")

    print("\n=== (1) RE-RANK VERDICT: does the pair reproduce the 7-rung verdict? ===")
    agg = P.groupby("pair").agg(cells=("rerank_agrees", "size"),
                                agrees=("rerank_agrees", "sum"),
                                full_rerank=("full_rerank", "sum"),
                                pair_rerank=("pair_rerank", "sum"))
    agg["disagrees"] = agg.cells - agg.agrees
    print(agg.to_string())
    for pr in P.pair.unique():
        d = P[(P.pair == pr) & (~P.rerank_agrees)]
        if len(d):
            print(f"  {pr} disagrees on: " +
                  ", ".join(f"{r.panel}/{r.book}/{r.dial}"
                            f"(full={r.full_rerank},pair={r.pair_rerank})"
                            for r in d.itertuples()))

    print("\n=== (2) LEVEL: interior Sharpe vs the straight line between the pair endpoints ===")
    print(P.groupby("pair")[["max_level_residual", "level_residual_at_10"]]
          .agg(["mean", "max"]).to_string(float_format=lambda x: f"{x:.5f}"))
    print("\nworst level residual per pair (the cell that bends most):")
    for pr, d in P.groupby("pair"):
        r = d.loc[d.max_level_residual.idxmax()]
        print(f"  {pr:6s} {r.panel}/{r.book}/{r.dial}  {r.max_level_residual:.5f}")
    print("\nby dial (pair 0-30):")
    print(P[P.pair == "0-30"].groupby("dial")["max_level_residual"]
          .agg(["mean", "max"]).to_string(float_format=lambda x: f"{x:.5f}"))

    print("\n=== (3) TOLERANCE GRID: cells whose interior is reproduced within tol ===")
    tol_rows = []
    for pr, d in P.groupby("pair"):
        for t in TOLS:
            tol_rows.append(dict(pair=pr, tol=t, cells=len(d),
                                 reproduced=int((d.max_level_residual <= t).sum()),
                                 reproduced_at_10=int((d.level_residual_at_10 <= t).sum())
                                 if d.level_residual_at_10.notna().any() else np.nan))
    T = pd.DataFrame(tol_rows)
    T.to_csv(f"{OUT}.tolerance.csv", index=False)
    print(T.pivot(index="tol", columns="pair", values="reproduced").to_string())

    print("\n=== (4) KEEP / 4b-BAR RECOVERY at PROTOCOL's binding 10 bps rung ===")
    kk = P[P.pair.isin([f"{lo}-{hi}" for lo, hi in PAIRS if lo <= BINDING <= hi])]
    s = kk.groupby("pair")[["n_values", "keep4a_recovered", "keep4a_undetermined",
                            "keep4b_recovered", "keep4b_undetermined",
                            "bar_recovered", "bar_undetermined"]].sum()
    s["4a_wrong"] = s.n_values - s.keep4a_recovered - s.keep4a_undetermined
    s["4b_wrong"] = s.n_values - s.keep4b_recovered - s.keep4b_undetermined
    s["bar_wrong"] = s.n_values - s.bar_recovered - s.bar_undetermined
    print(s.to_string())
    print("\ninterp argmax at 10 bps matches the true 10-bps argmax:")
    print(kk.groupby("pair")["interp_argmax10_ok"]
          .agg(["sum", "size"]).to_string())

    print("\n=== (5) LOAD-BEARING GRID POINTS (pair 0-30: endpoints do not decide) ===")
    if len(LB):
        print(f"{len(LB)} of {len(G)//len(RUNGS)} arms; by what they decide:")
        print(LB.what.value_counts().to_string())
        print(LB.groupby(["panel", "book", "dial"]).size().to_string())
        print("\nfull list (first 40):")
        print(LB.head(40).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        print("  none: the 0 and 30 bps endpoints agree on 4a, 4b and the failing 4b bar "
              "for every arm in the corpus")

    print("\n=== (6) COMPUTE actually saved by deleting 5 rungs ===")
    print(CP.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    tot_sim, tot_score = CP.sim_seconds.sum(), CP.score7_seconds.sum()
    saved = tot_score * 5 / len(RUNGS)
    print(f"\nsimulation {tot_sim:.1f}s + 7-rung scoring {tot_score:.1f}s = "
          f"{tot_sim+tot_score:.1f}s")
    print(f"deleting 5 of 7 rungs saves {saved:.1f}s = "
          f"{100*saved/(tot_sim+tot_score):.1f}% of the run "
          f"({100*5/len(RUNGS):.1f}% of the SCORING, 0% of the simulation: all 7 rungs "
          f"share ONE simulation under net(c) = gross - turnover*c/1e4)")

    print("\n=== (7) 4a / 4b passes across the corpus (both KEEP paths) ===")
    print(f"4a (vs RULES v2 live): {int(G.pass4a.sum())}/{len(G)}   "
          f"4a (vs RULES v1, continuity): {int((G.fail4a_v1 == '').sum())}/{len(G)}   "
          f"4b (vs SPY): {int(G.pass4b.sum())}/{len(G)}")
    print("\n4b failing-bar census (all rungs):")
    print(G[~G.pass4b].fail4b.value_counts().head(10).to_string())
    print("\n4b passes at PROTOCOL's 10 bps, if any:")
    p4 = G[(G.pass4b) & (G.bps == BINDING)]
    if len(p4):
        print(p4[["panel", "book", "dial", "value", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "turn_yr"]].to_string(index=False,
                                                      float_format=lambda x: f"{x:.4f}"))
    else:
        print("  none")
    print("\n4a passes at 10 bps, if any:")
    p4a = G[(G.pass4a) & (G.bps == BINDING)]
    print(f"  {len(p4a)} arms" if len(p4a) else "  none")
    if len(p4a):
        print(p4a[["panel", "book", "dial", "value", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "OOS_Sharpe"]].head(25).to_string(index=False,
                                                     float_format=lambda x: f"{x:.4f}"))

    print("\n=== (8) RULE 8 WALK-FORWARD: true 10-bps chooser vs the 2-rung chooser ===")
    print("(dial chosen on 2009-2016 IS Sharpe, 2017-2026 read once)")
    print(WF[["panel", "book", "dial", "pair", "true_pick", "pair_pick", "same_pick",
              "true_OOS_Sharpe", "pair_OOS_Sharpe", "d_pair_minus_true"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nby pair: how often the 2-rung chooser picks the same arm, and what it costs OOS")
    print(WF.groupby("pair").agg(cells=("same_pick", "size"), same=("same_pick", "sum"),
                                 mean_d_OOS_Sharpe=("d_pair_minus_true", "mean"),
                                 min_d=("d_pair_minus_true", "min"),
                                 max_d=("d_pair_minus_true", "max"))
          .to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nOOS LEVELS at 10 bps, means over the corpus (chooser vs baselines vs SPY):")
    lv = WF.groupby("pair")[["true_OOS_Sharpe", "true_OOS_CAGR", "true_OOS_MaxDD",
                             "pair_OOS_Sharpe", "pair_OOS_CAGR", "pair_OOS_MaxDD",
                             "dn_OOS_Sharpe", "dn_OOS_CAGR", "dn_OOS_MaxDD",
                             "basev2_OOS_Sharpe", "basev2_OOS_CAGR", "basev2_OOS_MaxDD",
                             "basev1_OOS_Sharpe",
                             "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]].mean()
    print(lv.to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nper panel (pair 0-30), OOS Sharpe/CAGR/MaxDD of the true chooser, the 2-rung "
          "chooser, do-nothing, RULES v2, RULES v1 and SPY:")
    w = WF[WF.pair == "0-30"]
    print(w.groupby("panel")[["true_OOS_Sharpe", "pair_OOS_Sharpe", "dn_OOS_Sharpe",
                              "basev2_OOS_Sharpe", "basev1_OOS_Sharpe", "spy_OOS_Sharpe",
                              "true_OOS_CAGR", "pair_OOS_CAGR", "basev2_OOS_CAGR",
                              "spy_OOS_CAGR", "true_OOS_MaxDD", "pair_OOS_MaxDD",
                              "basev2_OOS_MaxDD", "spy_OOS_MaxDD"]].mean()
          .to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
