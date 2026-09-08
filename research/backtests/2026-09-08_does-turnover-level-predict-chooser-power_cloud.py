#!/usr/bin/env python3
"""Idea 233 — does-turnover-level-predict-chooser-power (cloud lane, 2026-09-08).

Pre-registered question (QUEUE 233): pool idea 230's 33 cells with idea 228's 12 and regress
`cost_of_0bps_pick_at_30` on the do-nothing book's turnover.  If it is a clean function of
turnover, the cost ladder's chooser value is publishable from ONE NUMBER instead of a census.

The claim under test is a REPLACEMENT claim, so the test is a replacement test, not an R^2:
a turnover model earns the census only if, OUT of its own fit, it beats the trivial predictor
"quote the pooled mean of y".  Both leave-one-cell-out and leave-one-PANEL-out are reported.

Corpus, rebuilt end to end from prices so both parents are reproduced rather than cited:
  * idea 230's 33 cells — 3 books (TOPN / V1C / EWALL) x their dials x panels
    U56, B136, SMALL439 (the sub-$2B panel with max_1d_move >= 1.0 dropped).
  * idea 228's 12 cells — the TOPN book only, on U56, B136 and the UNSCREENED SMALL484, which
    is the panel 228 actually used.
  Pooled as the queue asks = 45 rows.  8 of those rows are literal duplicates (U56 and B136
  TOPN, 4 dials each, appear in both parents), so the DE-DUPLICATED corpus of 37 distinct
  cells is reported beside the 45, and every headline is quoted on both.

TWO tuned parameters only, all grid points reported (.params.csv):
    X TRANSFORM  — how the do-nothing turnover enters: level, log, rank, the cell's turnover
                   SPAN (max-min over the dial), and span/level
    RUNG         — the rung `cost_of_0bps_pick_at_R` is read at: 10, 20, 25, 30 bps
Nothing else is tuned: panels, books, dials, dial grids, rungs, the do-nothing defaults and the
two KEEP paths are the record's own.

Two targets are regressed, because "chooser power" has an in-sample and an out-of-sample
reading and the queue's y is the in-sample one:
    y_IS  = cost_of_0bps_pick_at_R — Sharpe given up at rung R by taking the 0-bps argmax
    y_OOS = rule 8 chooser power   — OOS Sharpe of the IS-chosen arm minus the do-nothing arm
                                     (params on 2009-2016, 2017-2026 read once)

PROTOCOL: 10 bps binding, weights at t applied at t+1 (engine convention; the ladder identity
net(c) = gross - turnover*c/1e4 is asserted against engine.backtest at 10 bps), rule 8 always
run, both KEEP paths evaluated — 4a against the LIVE RULES v2 baseline (RULES v1 kept for
continuity with the pre-2026-09-06 record) and 4b against SPY.

SURVIVORSHIP: B136, SMALL439 and SMALL484 are current constituents of their screens only
(data/SMALL_PANEL_README.md, idea 54); the bias runs in favour of every long book quoted here.

Outputs (all committed):
    .grid.csv        every (panel, book, dial, value, rung): turnover, CAGR/Sharpe/MaxDD, H1/H2,
                     IS/OOS, 4a and 4b pass + failing bar
    .census.csv      per cell: argmaxes per rung, re-rank verdict, do-nothing turnover,
                     cost_of_0bps_pick at every rung, rule-8 chooser power
    .params.csv      the full 5 transforms x 4 rungs x 2 corpora x 2 targets grid: slope,
                     R^2, Spearman, and the replacement test vs the pooled mean
    .lopo.csv        leave-one-panel-out replacement test, every fold
    .walkforward.csv rule 8 per cell and rung, OOS Sharpe/CAGR/MaxDD vs RULES v2, v1 and SPY
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
BINDING = 10
COST_RUNGS = [10, 20, 25, 30]          # tuned parameter 2
TRANSFORMS = ["level", "log", "rank", "span", "span_over_level"]   # tuned parameter 1
OOS_START = "2017-01-01"
IS_END = "2016-12-31"

DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1)
DIAL_VALUES = {
    "N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
    "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
    "K": [1, 2, 3, 4, 6, 8, 13],
}
# (corpus tag, panel name, books) — 230's three books on the screened panels, 228's TOPN-only
# census on the panels 228 used (SMALL484 unscreened).
PARENTS = {"i230": ["TOPN", "V1C", "EWALL"], "i228": ["TOPN"]}
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
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index))


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
    fail = []
    if not s["H1"] > b["H1"]: fail.append("H1")
    if not s["H2"] > b["H2"]: fail.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: fail.append("DD")
    return ",".join(fail)


def bars_4b(s, spy, oos_s, oos_spy):
    fail = []
    if not s["H1"] > spy["H1"]: fail.append("H1")
    if not s["H2"] > spy["H2"]: fail.append("H2")
    if not oos_s > oos_spy: fail.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: fail.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fail.append("CAGR")
    return ",".join(fail)


def small_panel(screened):
    px = load_universe(small=True)
    if not screened:
        print(f"SMALL484: unscreened (idea 228's panel), {px.shape[1]-1} names + SPY",
              flush=True)
        return px
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"SMALL439: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
          f"{len(keep)-1} names + SPY remain", flush=True)
    return px[keep]


def panels():
    """(panel tag, prices, which parent censuses this panel serves)."""
    yield "U56", load_universe(), ["i230", "i228"]
    yield "B136", load_universe(broad=True), ["i230", "i228"]
    yield "SMALL439", small_panel(True), ["i230"]
    yield "SMALL484", small_panel(False), ["i228"]


# ---------------------------------------------------------------- regression helpers
def ols(x, y):
    """Slope, intercept, R^2 of a one-regressor OLS with intercept."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3 or x.std() == 0:
        return np.nan, np.nan, np.nan, len(x)
    b = np.cov(x, y, ddof=1)[0, 1] / x.var(ddof=1)
    a = y.mean() - b * x.mean()
    r2 = 1 - ((y - (a + b * x)) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return b, a, r2, len(x)


def loo_rmse(x, y):
    """Leave-one-out RMSE of the OLS line vs the leave-one-out MEAN. The replacement test."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 4:
        return np.nan, np.nan, n
    e_fit, e_mean = [], []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        b, a, _, _ = ols(x[m], y[m])
        e_fit.append(y[i] - (a + b * x[i]) if np.isfinite(b) else np.nan)
        e_mean.append(y[i] - y[m].mean())
    return (float(np.sqrt(np.nanmean(np.square(e_fit)))),
            float(np.sqrt(np.mean(np.square(e_mean)))), n)


def transform(name, level, span):
    if name == "level":  return level
    if name == "log":    return np.log(np.maximum(level, 1e-9))
    if name == "rank":   return pd.Series(level).rank().values
    if name == "span":   return span
    if name == "span_over_level":
        return np.asarray(span, float) / np.maximum(np.asarray(level, float), 1e-9)
    raise ValueError(name)


def main():
    t0 = time.time()
    grid, census, wf_rows, ident = [], [], [], []

    for pname, px, parents in panels():
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))
        v1score, _, _ = score(px, vol_scale=True)
        keys = dict(comp=comp, v1score=v1score)
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos_m = metrics(spy_r.loc[OOS_START:])
        spy_oos = spy_oos_m["Sharpe"]

        b2g, b2t = simulate(px, rules_v2_weights(px), week_mask(px.index, 1))
        base2 = {c: stats(net(b2g, b2t, c).loc[start:]) for c in RUNGS}
        base2_oos = metrics(net(b2g, b2t, BINDING).loc[OOS_START:])
        b1g, b1t = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base1 = {c: stats(net(b1g, b1t, c).loc[start:]) for c in RUNGS}
        base1_oos = metrics(net(b1g, b1t, BINDING).loc[OOS_START:])
        eng = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append((pname, float(np.abs(eng - net(b2g, b2t, 10).loc[start:]).max())))

        books = sorted({b for pa in parents for b in PARENTS[pa]})
        sims = {}
        for book in books:
            for dial in BOOK_DIALS[book]:
                for v in DIAL_VALUES[dial]:
                    kw = dict(DEFAULTS); kw[dial] = v
                    if dial == "N" and v > px.shape[1] - 1:
                        continue
                    sig = (book, kw["N"] if book != "EWALL" else -1, kw["G"], kw["V"], kw["K"])
                    if sig not in sims:
                        W = book_weights(book, px, keys, ma, vol20, kw["N"], kw["G"], kw["V"])
                        g_, t_ = simulate(px, W, week_mask(px.index, kw["K"]))
                        sims[sig] = (g_.loc[start:], t_.loc[start:])
                    g_s, t_s = sims[sig]
                    yrs = len(g_s) / 252
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

                g = pd.DataFrame([x for x in grid if x["panel"] == pname
                                  and x["book"] == book and x["dial"] == dial])
                vals = sorted(g["value"].unique())
                sh = {c: g[g.bps == c].set_index("value")["Sharpe"].reindex(vals) for c in RUNGS}
                arg = {c: sh[c].idxmax() for c in RUNGS}
                turns = g[g.bps == 0].set_index("value")["turn_yr"].reindex(vals)
                dn = DEFAULTS[dial]

                def _sig(v):
                    kw = dict(DEFAULTS); kw[dial] = v
                    return (book, kw["N"] if book != "EWALL" else -1,
                            kw["G"], kw["V"], kw["K"])
                keyed = {v: sims[_sig(v)] for v in vals}
                power = {}
                for c in RUNGS:
                    sub = {v: net(a, b, c) for v, (a, b) in keyed.items()}
                    is_sh = {v: metrics(r.loc[:IS_END])["Sharpe"] for v, r in sub.items()}
                    pick = max(is_sh, key=is_sh.get)
                    o = {v: metrics(r.loc[OOS_START:]) for v, r in sub.items()}
                    power[c] = o[pick]["Sharpe"] - o[dn]["Sharpe"]
                    wf_rows.append(dict(panel=pname, book=book, dial=dial, bps=c, IS_pick=pick,
                                        do_nothing=dn,
                                        pick_OOS_Sharpe=o[pick]["Sharpe"],
                                        pick_OOS_CAGR=o[pick]["CAGR"],
                                        pick_OOS_MaxDD=o[pick]["MaxDD"],
                                        dn_OOS_Sharpe=o[dn]["Sharpe"],
                                        dn_OOS_CAGR=o[dn]["CAGR"],
                                        dn_OOS_MaxDD=o[dn]["MaxDD"],
                                        rand_OOS_Sharpe=float(np.mean(
                                            [x["Sharpe"] for x in o.values()])),
                                        oracle_OOS_Sharpe=max(x["Sharpe"] for x in o.values()),
                                        d_pick_minus_dn=power[c],
                                        basev2_OOS_Sharpe=base2_oos["Sharpe"],
                                        basev2_OOS_CAGR=base2_oos["CAGR"],
                                        basev2_OOS_MaxDD=base2_oos["MaxDD"],
                                        basev1_OOS_Sharpe=base1_oos["Sharpe"],
                                        spy_OOS_Sharpe=spy_oos, spy_OOS_CAGR=spy_oos_m["CAGR"],
                                        spy_OOS_MaxDD=spy_oos_m["MaxDD"]))
                row = dict(panel=pname, book=book, dial=dial, n_values=len(vals),
                           parents=",".join(parents),
                           dn_turnover=float(turns.loc[dn]), turn_min=float(turns.min()),
                           turn_max=float(turns.max()),
                           turn_span=float(turns.max() - turns.min()),
                           **{f"argmax_{c}bps": arg[c] for c in RUNGS},
                           n_distinct_argmax=len(set(arg.values())),
                           rerankable=len(set(arg.values())) > 1,
                           **{f"cost_of_0bps_pick_at_{c}": float(sh[c].max() - sh[c].loc[arg[0]])
                              for c in COST_RUNGS},
                           **{f"chooser_power_{c}": power[c] for c in COST_RUNGS},
                           sharpe_range_10bps=float(sh[10].max() - sh[10].min()))
                census.append(row)
            print(f"  {pname}/{book}: {time.time()-t0:.0f}s", flush=True)
        print(f"{pname}: done {time.time()-t0:.0f}s ({len(sims)} sims)", flush=True)

    G = pd.DataFrame(grid); C = pd.DataFrame(census); WF = pd.DataFrame(wf_rows)
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.census.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\n=== GATE: net identity vs engine.backtest at 10 bps (max abs daily diff) ===")
    for p, d in ident: print(f"  {p:9s} {d:.3e}")

    # ---- the two corpora the queue names, and the de-duplicated union
    i230 = C[C.parents.str.contains("i230")].copy()
    i228 = C[C.parents.str.contains("i228") & (C.book == "TOPN")].copy()
    pooled45 = pd.concat([i230, i228], ignore_index=True)          # as the queue states it
    dedup = C.drop_duplicates(subset=["panel", "book", "dial"]).copy()
    print(f"\n=== CORPUS: idea 230 {len(i230)} cells + idea 228 {len(i228)} cells "
          f"= {len(pooled45)} pooled rows; {len(dedup)} distinct cells "
          f"({len(pooled45)-len(dedup)} of the pooled rows are literal duplicates: "
          f"U56/B136 TOPN appear in both parents) ===")
    print(C[["panel", "book", "dial", "parents", "n_values", "dn_turnover", "turn_span",
             "rerankable", "cost_of_0bps_pick_at_30", "chooser_power_30",
             "cost_of_0bps_pick_at_10", "chooser_power_10"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- the regression grid
    rows, lopo_rows = [], []
    for corpus_name, D in (("pooled45", pooled45), ("dedup37", dedup)):
        for tname in TRANSFORMS:
            x = transform(tname, D.dn_turnover.values, D.turn_span.values)
            for R in COST_RUNGS:
                for target, col in (("y_IS", f"cost_of_0bps_pick_at_{R}"),
                                    ("y_OOS", f"chooser_power_{R}")):
                    y = D[col].values
                    b, a, r2, n = ols(x, y)
                    sp = float(pd.Series(x).rank().corr(pd.Series(y).rank()))
                    rf, rm, _ = loo_rmse(x, y)
                    rows.append(dict(corpus=corpus_name, transform=tname, rung=R,
                                     target=target, n=n, slope=b, intercept=a, R2=r2,
                                     spearman=sp, y_mean=float(np.nanmean(y)),
                                     y_sd=float(np.nanstd(y, ddof=1)),
                                     loo_rmse_fit=rf, loo_rmse_mean=rm,
                                     beats_mean=bool(np.isfinite(rf) and rf < rm),
                                     rmse_ratio=rf / rm if np.isfinite(rf) and rm else np.nan))
                    # leave-one-PANEL-out: the only honest generalisation this corpus allows
                    for pan in sorted(D.panel.unique()):
                        m = (D.panel != pan).values
                        bb, aa, _, _ = ols(x[m], y[m])
                        if not np.isfinite(bb):
                            continue
                        yt = y[~m]
                        e_fit = yt - (aa + bb * x[~m])
                        e_mean = yt - y[m].mean()
                        lopo_rows.append(dict(corpus=corpus_name, transform=tname, rung=R,
                                              target=target, held_out=pan, n_test=int((~m).sum()),
                                              rmse_fit=float(np.sqrt(np.mean(e_fit ** 2))),
                                              rmse_mean=float(np.sqrt(np.mean(e_mean ** 2))),
                                              slope=bb))
    P = pd.DataFrame(rows); LP = pd.DataFrame(lopo_rows)
    P.to_csv(f"{OUT}.params.csv", index=False)
    LP.to_csv(f"{OUT}.lopo.csv", index=False)

    print("\n=== THE FULL PARAMETER GRID (5 transforms x 4 rungs x 2 targets x 2 corpora) ===")
    for corpus_name in ("pooled45", "dedup37"):
        print(f"\n--- {corpus_name} ---")
        print(P[P.corpus == corpus_name][["transform", "rung", "target", "n", "slope", "R2",
                                          "spearman", "y_mean", "y_sd", "loo_rmse_fit",
                                          "loo_rmse_mean", "beats_mean", "rmse_ratio"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== HEADLINE 1: does turnover explain y at all? (R^2 and Spearman) ===")
    print(P.groupby(["corpus", "target"])[["R2", "spearman"]]
          .agg(["mean", "max"]).to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nbest cell of the whole grid by R^2, per target:")
    for tg in ("y_IS", "y_OOS"):
        b = P[P.target == tg].sort_values("R2", ascending=False).head(3)
        print(b[["corpus", "transform", "rung", "R2", "spearman", "slope", "beats_mean",
                 "rmse_ratio"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== HEADLINE 2: THE REPLACEMENT TEST — does the line beat the pooled MEAN? ===")
    print("(leave-one-cell-out RMSE of the fitted line vs of the leave-one-out mean)")
    print(P.groupby(["corpus", "target"])["beats_mean"]
          .agg(["sum", "size"]).to_string())
    print("\nby transform (both corpora pooled):")
    print(P.groupby(["transform", "target"])[["beats_mean", "rmse_ratio"]]
          .agg({"beats_mean": ["sum", "size"], "rmse_ratio": "mean"})
          .to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nby rung:")
    print(P.groupby(["rung", "target"])[["beats_mean", "rmse_ratio"]]
          .agg({"beats_mean": ["sum", "size"], "rmse_ratio": "mean"})
          .to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n=== HEADLINE 3: LEAVE-ONE-PANEL-OUT (the only honest generalisation here) ===")
    LP["beats"] = LP.rmse_fit < LP.rmse_mean
    print(LP.groupby(["corpus", "target"])["beats"].agg(["sum", "size"]).to_string())
    print("\nper held-out panel, target y_IS, transform=level:")
    d = LP[(LP.target == "y_IS") & (LP["transform"] == "level")]
    print(d[["corpus", "rung", "held_out", "n_test", "rmse_fit", "rmse_mean", "beats", "slope"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nsign stability of the slope across folds (y_IS, all transforms/rungs):")
    ss = LP[LP.target == "y_IS"].groupby(["transform", "rung"])["slope"].agg(
        ["mean", "min", "max", lambda s: (s > 0).mean()]).rename(
        columns={"<lambda_0>": "frac_positive"})
    print(ss.to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n=== HEADLINE 4: the ZERO problem — y is a spike at zero ===")
    for tg, R in (("cost_of_0bps_pick_at_30", 30), ("cost_of_0bps_pick_at_10", 10)):
        v = C[tg]
        print(f"  {tg}: {(v == 0).sum()} of {len(v)} distinct cells are EXACTLY 0 "
              f"({100*(v==0).mean():.1f}%); mean {v.mean():.4f}, "
              f"mean among nonzero {v[v>0].mean():.4f}, max {v.max():.4f}")
    print("  (a cell is exactly 0 iff its ladder never re-ranks, so y is "
          "P(re-rank) x E[cost | re-rank] and any 'clean function of turnover' must "
          "first be a clean function of P(re-rank))")
    print("\n  do-nothing turnover of re-ranking vs non-re-ranking cells (distinct cells):")
    print(C.groupby("rerankable")["dn_turnover"]
          .agg(["count", "mean", "min", "max"]).to_string(float_format=lambda x: f"{x:.3f}"))
    print("  turnover SPAN of re-ranking vs non-re-ranking cells:")
    print(C.groupby("rerankable")["turn_span"]
          .agg(["count", "mean", "min", "max"]).to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n=== HEADLINE 5: does y_IS predict y_OOS at all? ===")
    for R in COST_RUNGS:
        b, a, r2, n = ols(C[f"cost_of_0bps_pick_at_{R}"], C[f"chooser_power_{R}"])
        sp = float(C[f"cost_of_0bps_pick_at_{R}"].rank()
                   .corr(C[f"chooser_power_{R}"].rank()))
        print(f"  rung {R}: slope {b:+.4f}  R2 {r2:.4f}  spearman {sp:+.4f}  n {n}")

    print("\n=== BOTH KEEP PATHS on all grid points ===")
    print(f"4a (vs live RULES v2): {int(G.pass4a.sum())}/{len(G)}   "
          f"4a (vs retired RULES v1): {int((G.fail4a_v1 == '').sum())}/{len(G)}   "
          f"4b (vs SPY): {int(G.pass4b.sum())}/{len(G)}")
    print("\n4b passes at PROTOCOL's 10 bps:")
    p4 = G[(G.pass4b) & (G.bps == BINDING)]
    if len(p4):
        print(p4[["panel", "book", "dial", "value", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "turn_yr"]].to_string(index=False,
                                                      float_format=lambda x: f"{x:.4f}"))
    else:
        print("  none")
    print("\n4b failing-bar census (all rungs):")
    print(G[~G.pass4b].fail4b.value_counts().head(10).to_string())

    print("\n=== RULE 8 WALK-FORWARD (params 2009-2016, 2017-2026 read once) ===")
    w = WF[WF.bps == BINDING]
    print("at PROTOCOL's 10 bps, per cell:")
    print(w[["panel", "book", "dial", "IS_pick", "do_nothing", "pick_OOS_Sharpe",
             "dn_OOS_Sharpe", "rand_OOS_Sharpe", "oracle_OOS_Sharpe", "d_pick_minus_dn"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nOVERALL at 10 bps: mean d(pick - do-nothing) = {w.d_pick_minus_dn.mean():+.4f}, "
          f"pick wins {100*(w.d_pick_minus_dn>0).mean():.1f}% of {len(w)} cells")
    print("\nOOS levels at 10 bps, means over cells (chooser vs baselines vs SPY):")
    print(w[["pick_OOS_Sharpe", "pick_OOS_CAGR", "pick_OOS_MaxDD", "dn_OOS_Sharpe",
             "dn_OOS_CAGR", "dn_OOS_MaxDD", "basev2_OOS_Sharpe", "basev2_OOS_CAGR",
             "basev2_OOS_MaxDD", "basev1_OOS_Sharpe", "spy_OOS_Sharpe", "spy_OOS_CAGR",
             "spy_OOS_MaxDD"]].mean().to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nper panel:")
    print(w.groupby("panel")[["pick_OOS_Sharpe", "pick_OOS_CAGR", "pick_OOS_MaxDD",
                              "dn_OOS_Sharpe", "basev2_OOS_Sharpe", "basev2_OOS_CAGR",
                              "basev2_OOS_MaxDD", "spy_OOS_Sharpe", "spy_OOS_CAGR",
                              "spy_OOS_MaxDD"]].mean()
          .to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
