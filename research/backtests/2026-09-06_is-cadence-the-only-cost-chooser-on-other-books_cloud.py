#!/usr/bin/env python3
"""Idea 230 — is-cadence-the-only-cost-chooser-on-other-books (cloud lane, 2026-09-06).

Pre-registered question (QUEUE 230): idea 228 ran a 4-dial census (N, G, V, K) on ONE
construction (top-n equal weight, composite WITHOUT the vol scaler, gross 1.00) and found the
cost rung re-ranks 3 of 12 panel x dial cells, 2 of the 3 being CADENCE.  Re-run the identical
census on two other books named by the queue — the LIVE RULES v1 COMPOSITE book (same top-n
shape but ranked by the traded score, i.e. composite / sqrt(vol20)) and an EW-ALL-ELIGIBLE
book (no ranking at all) — and report whether cadence keeps its status as the only dial a rung
can choose.

Two tuned parameters only: the DIAL VALUE and the COST RUNG.  The three books are
pre-registered (two named by the queue, one the parent's own construction re-run on this
harness as a control), not selected.  Every grid point is reported in .grid.csv.

Books (all gross 1.00, all over the same band-gated 200d AND vol20 eligible set):
    TOPN  — control, idea 228's book: rank = composite (12-1 / 6m / 3m rank average, NO vol
            scaler), hold top n at 1/n.
    V1C   — the live RULES v1 composite book: rank = composite / max(vol20, 0.08)**0.5, the
            score research/scan.py actually trades, hold top n at 1/n.  (The literal live book
            holds n=5 at w=0.15; that de-grosses to 0.75 and would confound the N dial with
            gross, so gross is held at 1.00 exactly as in 228.  The literal w=0.15 book is
            reported separately as `V1LIT` reference rows, not as part of the census.)
    EWALL — equal-weight EVERY eligible name, gross 1.00.  This book HAS NO COUNT DIAL: N is
            undefined for it and is reported as absent rather than invented.  It therefore
            contributes 3 dials, not 4.

Dials and their grids (identical to idea 228):
    N (count)     3, 5, 8, 10, 15, 20, 25, 30, 40, 56        default 20
    G (200d band) 0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12   default 0.00
    V (vol cap)   0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00 (5.00 == off)  default 0.60
    K (cadence)   1, 2, 3, 4, 6, 8, 13 weeks                 default 1

Panels: U56 (research/universe.json), B136 (universe_broad.json), SMALL439 (the sub-$2B panel
with max_1d_move >= 1.0 dropped per data/small_meta.csv).  NOTE: idea 228 used the UNSCREENED
SMALL484; the screened panel is this run's, so the small-panel control rows will not match 228
exactly.  SURVIVORSHIP: the small panel is current constituents of the screen only
(data/SMALL_PANEL_README.md, idea 54) and the broad panel is current constituents too — both
biases run in favour of any long book quoted here.

Cost ladder uses the exact identity net(c) = gross - turnover * c/1e4 (held weights and
turnover do not depend on cost), asserted against engine.backtest at 10 bps.

Outputs (all committed):
    .grid.csv        every (panel, book, dial, value, rung): turnover, CAGR/Sharpe/MaxDD,
                     H1/H2, IS/OOS, 4a and 4b pass + failing bar
    .census.csv      per (panel, book, dial): Spearman(dial, turnover), argmax at each rung,
                     distinct argmaxes, re-rank verdict, cost of ignoring the rung
    .mechanism.csv   idea 228's predictor (0-bps top-2 gap vs the ladder's 30-bp tilt)
    .walkforward.csv rule 8: dial chosen on 2009-2016 at each rung, 2017-2026 read once,
                     vs do-nothing / random / oracle / RULES v1 / SPY
    .keep.csv        4a and 4b pass counts per (panel, book, dial, rung)
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score          # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

OUT = Path(__file__).with_suffix("")
RUNGS = [0, 5, 10, 15, 20, 25, 30]
OOS_START = "2017-01-01"           # rule 8: params on 2009-2016, 2017-2026 read once
IS_END = "2016-12-31"
DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1)
DIAL_VALUES = {
    "N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
    "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
    "K": [1, 2, 3, 4, 6, 8, 13],
}
BOOKS = ["TOPN", "V1C", "EWALL"]           # control, then the two the queue names
BOOK_DIALS = {"TOPN": ["N", "G", "V", "K"],
              "V1C":  ["N", "G", "V", "K"],
              "EWALL": ["G", "V", "K"]}    # EWALL has no count dial, by construction


def spearman(a, b):
    a, b = pd.Series(list(a), dtype=float), pd.Series(list(b), dtype=float)
    return float(a.rank().corr(b.rank()))


# ---------------------------------------------------------------- simulation
def week_mask(idx, k):
    """True on the last trading day of every k-th ISO week (k=1 == engine's freq='W')."""
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
    invested = pd.Series(held.sum(axis=1), index=px.index)
    return gross, pd.Series(turn, index=px.index), invested


def eligible(px, ma, vol20, g, max_vol):
    if g == 0:
        above = px > ma
    else:                                        # hysteresis band around the 200d MA
        sig = pd.DataFrame(np.where(px > ma * (1 + g), 1.0,
                           np.where(px < ma * (1 - g), 0.0, np.nan)),
                           index=px.index, columns=px.columns)
        above = sig.ffill().fillna(0.0) > 0.5
    return above & (vol20 < max_vol)


def book_weights(book, px, keys, ma, vol20, n, g, max_vol):
    """Gross-1.00 weights for one of the three books over the same eligible set."""
    el = eligible(px, ma, vol20, g, max_vol)
    if book == "EWALL":
        w = el.astype(float)
        cnt = w.sum(axis=1)
        return w.div(cnt.where(cnt > 0), axis=0).fillna(0.0)
    key = keys["comp"] if book == "TOPN" else keys["v1score"]
    rank = key.where(el).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) / n


def v1_literal_weights(px, keys, ma, vol20, n, g, max_vol, w=0.15):
    """The live book exactly as RULES v1 states it: top-n by the traded score at w each."""
    el = eligible(px, ma, vol20, g, max_vol)
    rank = keys["v1score"].where(el).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * w


# ---------------------------------------------------------------- metrics helpers
def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    """4a: Sharpe > live rules in BOTH halves and MaxDD no worse."""
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


# ---------------------------------------------------------------- panels
def small_screened():
    """Sub-$2B panel with max_1d_move >= 1.0 dropped (prompt's standing screen)."""
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


def main():
    t0 = time.time()
    grid, census, wf_rows, ident, lit_rows = [], [], [], [], []
    for pname, px in panels():
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))     # exact: recover the composite
        v1score, _, _ = score(px, vol_scale=True)               # the traded score
        keys = dict(comp=comp, v1score=v1score)
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos_m = metrics(spy_r.loc[OOS_START:])
        spy_oos = spy_oos_m["Sharpe"]

        # --- RULES v1 baseline on this panel, per rung (weekly, per PROTOCOL rule 3)
        bg, bt, _ = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base = {c: stats(net(bg, bt, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(bg, bt, c).loc[OOS_START:])["Sharpe"] for c in RUNGS}
        eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append((pname, float(np.abs(eng - net(bg, bt, 10).loc[start:]).max())))

        # --- literal live book (w=0.15, n=5) as a reference row, not part of the census
        lg, lt, li = simulate(px, v1_literal_weights(px, keys, ma, vol20, 5, 0.0, 0.60),
                              week_mask(px.index, 1))
        for c in RUNGS:
            r = net(lg.loc[start:], lt.loc[start:], c)
            lit_rows.append(dict(panel=pname, book="V1LIT(n=5,w=0.15)", bps=c,
                                 turn_yr=lt.loc[start:].sum() / (len(r) / 252),
                                 mean_invested=float(li.loc[start:].mean()), **stats(r),
                                 OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"]))

        sims = {}                       # (book, n, g, v, k) -> (gross, turn, invested)
        for book in BOOKS:
            for dial in BOOK_DIALS[book]:
                for v in DIAL_VALUES[dial]:
                    kw = dict(DEFAULTS); kw[dial] = v
                    if dial == "N" and v > px.shape[1] - 1:
                        continue
                    sig = (book, kw["N"] if book != "EWALL" else -1, kw["G"], kw["V"], kw["K"])
                    if sig not in sims:
                        W = book_weights(book, px, keys, ma, vol20, kw["N"], kw["G"], kw["V"])
                        g_, t_, i_ = simulate(px, W, week_mask(px.index, kw["K"]))
                        sims[sig] = (g_.loc[start:], t_.loc[start:], i_.loc[start:])
                    g_s, t_s, i_s = sims[sig]
                    yrs = len(g_s) / 252
                    for c in RUNGS:
                        r = net(g_s, t_s, c)
                        st = stats(r)
                        o = metrics(r.loc[OOS_START:])
                        grid.append(dict(panel=pname, book=book, dial=dial, value=v, bps=c,
                                         turn_yr=t_s.sum() / yrs,
                                         mean_invested=float(i_s.mean()), **st,
                                         OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"],
                                         OOS_MaxDD=o["MaxDD"],
                                         IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                         fail4a=bars_4a(st, base[c]),
                                         fail4b=bars_4b(st, spy_s, o["Sharpe"], spy_oos)))

                # ---- census for this (panel, book, dial)
                g = pd.DataFrame([x for x in grid if x["panel"] == pname
                                  and x["book"] == book and x["dial"] == dial])
                vals = sorted(g["value"].unique())
                turns = g[g.bps == 0].set_index("value")["turn_yr"].reindex(vals)
                arg = {c: g[g.bps == c].set_index("value")["Sharpe"].idxmax() for c in RUNGS}
                sh30 = g[g.bps == 30].set_index("value")["Sharpe"]
                census.append(dict(panel=pname, book=book, dial=dial, n_values=len(vals),
                                   spearman_dial_turnover=spearman(vals, turns.values),
                                   turn_min=turns.min(), turn_max=turns.max(),
                                   **{f"argmax_{c}bps": arg[c] for c in RUNGS},
                                   n_distinct_argmax=len(set(arg.values())),
                                   rerankable=len(set(arg.values())) > 1,
                                   first_move_bps=next((c for c in RUNGS if arg[c] != arg[0]),
                                                       np.nan),
                                   sharpe_range_10bps=float(g[g.bps == 10]["Sharpe"].max()
                                                            - g[g.bps == 10]["Sharpe"].min()),
                                   cost_of_0bps_pick_at_30=float(sh30.max() - sh30.loc[arg[0]])))

                # ---- rule 8 walk-forward for this (panel, book, dial), per rung
                def _sig(v):
                    kw = dict(DEFAULTS); kw[dial] = v
                    return (book, kw["N"] if book != "EWALL" else -1,
                            kw["G"], kw["V"], kw["K"])
                keyed = {v: sims[_sig(v)] for v in vals}
                for c in RUNGS:
                    sub = {v: net(a, b, c) for v, (a, b, _i) in keyed.items()}
                    is_sh = {v: metrics(r.loc[:IS_END])["Sharpe"] for v, r in sub.items()}
                    pick = max(is_sh, key=is_sh.get)
                    full_arg = max(sub, key=lambda v: metrics(sub[v])["Sharpe"])
                    dn = DEFAULTS[dial]
                    oos = lambda v: metrics(sub[v].loc[OOS_START:])
                    rand = float(np.mean([oos(v)["Sharpe"] for v in sub]))
                    wf_rows.append(dict(panel=pname, book=book, dial=dial, bps=c, IS_pick=pick,
                                        do_nothing=dn, full_argmax=full_arg,
                                        pick_OOS_Sharpe=oos(pick)["Sharpe"],
                                        pick_OOS_CAGR=oos(pick)["CAGR"],
                                        pick_OOS_MaxDD=oos(pick)["MaxDD"],
                                        dn_OOS_Sharpe=oos(dn)["Sharpe"],
                                        dn_OOS_CAGR=oos(dn)["CAGR"],
                                        dn_OOS_MaxDD=oos(dn)["MaxDD"],
                                        rand_OOS_Sharpe=rand,
                                        oracle_OOS_Sharpe=oos(full_arg)["Sharpe"],
                                        d_pick_minus_dn=oos(pick)["Sharpe"] - oos(dn)["Sharpe"],
                                        d_rand_minus_dn=rand - oos(dn)["Sharpe"],
                                        base_OOS_Sharpe=base_oos[c], spy_OOS_Sharpe=spy_oos,
                                        spy_OOS_CAGR=spy_oos_m["CAGR"],
                                        spy_OOS_MaxDD=spy_oos_m["MaxDD"]))
            print(f"  {pname}/{book}: {time.time()-t0:.0f}s", flush=True)
        print(f"{pname}: done {time.time()-t0:.0f}s ({len(sims)} sims)", flush=True)

    G = pd.DataFrame(grid); C = pd.DataFrame(census); WF = pd.DataFrame(wf_rows)
    L = pd.DataFrame(lit_rows)
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.census.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    K = G.groupby(["panel", "book", "dial", "bps"])[["pass4a", "pass4b"]].sum().reset_index()
    K.to_csv(f"{OUT}.keep.csv", index=False)

    print("\n=== identity/engine check (max |engine@10bps - (gross - turn*c/1e4)|) ===")
    for p, d in ident: print(f"  {p}: {d:.3e}")

    print("\n=== CENSUS: Spearman(dial, turnover) and argmax vs cost rung ===")
    cols = ["panel", "book", "dial", "spearman_dial_turnover", "turn_min", "turn_max"] + \
           [f"argmax_{c}bps" for c in RUNGS] + ["n_distinct_argmax", "rerankable",
                                                "first_move_bps", "sharpe_range_10bps",
                                                "cost_of_0bps_pick_at_30"]
    print(C[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== HEADLINE: re-rankable cells by dial and by book ===")
    print(pd.crosstab(C.dial, C.rerankable).to_string())
    print()
    print(pd.crosstab(C.book, C.rerankable).to_string())
    print("\nre-rankable cells in full:")
    rr = C[C.rerankable]
    print(rr[["panel", "book", "dial", "first_move_bps"] + [f"argmax_{c}bps" for c in RUNGS]
             + ["cost_of_0bps_pick_at_30"]].to_string(index=False,
                                                      float_format=lambda x: f"{x:.3f}"))
    hi = C[[f"argmax_{c}bps" for c in RUNGS if c >= 10]].nunique(axis=1)
    lo = C[[f"argmax_{c}bps" for c in RUNGS if c <= 10]].nunique(axis=1)
    print(f"\nArgmax changes ANYWHERE in 10-30 bps: {int((hi > 1).sum())} of {len(C)} cells.")
    print(f"Argmax changes in 0-10 bps:            {int((lo > 1).sum())} of {len(C)} cells.")
    print("\ncost of ignoring the rung (Sharpe given up at 30 bps by taking the 0-bps pick):")
    print(C.groupby("dial")["cost_of_0bps_pick_at_30"]
          .agg(["mean", "max"]).to_string(float_format=lambda x: f"{x:.4f}"))
    print(C.groupby("book")["cost_of_0bps_pick_at_30"]
          .agg(["mean", "max"]).to_string(float_format=lambda x: f"{x:.4f}"))

    # --- idea 228's mechanism predictor, re-applied
    mech = []
    for (p_, bk_, d_), sub in G.groupby(["panel", "book", "dial"]):
        s0 = sub[sub.bps == 0].set_index("value")["Sharpe"].sort_values(ascending=False)
        s30 = sub[sub.bps == 30].set_index("value")["Sharpe"]
        best0 = s0.index[0]
        gap = float(s0.iloc[0] - s0.iloc[1])
        slope = (s30 - s0) / 30.0                       # Sharpe per bp, negative
        tilt = float((slope - slope.loc[best0]).max() * 30.0)
        mech.append(dict(panel=p_, book=bk_, dial=d_, argmax_0bps=best0, top2_gap_0bps=gap,
                         max_tilt_30bps=tilt, predicted_rerank=tilt > gap,
                         actual_rerank=bool(C.set_index(["panel", "book", "dial"])
                                            .loc[(p_, bk_, d_), "rerankable"])))
    M = pd.DataFrame(mech)
    M.to_csv(f"{OUT}.mechanism.csv", index=False)
    print("\n=== MECHANISM (idea 228's predictor): 0-bps top-2 gap vs max 30-bp tilt ===")
    print(M.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"predicted == actual in {int((M.predicted_rerank == M.actual_rerank).sum())} "
          f"of {len(M)}; catches "
          f"{int(((M.actual_rerank) & (M.predicted_rerank)).sum())} of "
          f"{int(M.actual_rerank.sum())} actual re-ranks; "
          f"false positives {int(((~M.actual_rerank) & (M.predicted_rerank)).sum())}")

    print("\n=== 4b passes (every passing grid point) ===")
    p4 = G[G.pass4b]
    if len(p4):
        print(p4[["panel", "book", "dial", "value", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "turn_yr", "mean_invested"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        print("  none")
    print("\n4b pass counts by panel/book/dial:")
    print(K.groupby(["panel", "book", "dial"])["pass4b"].sum().to_string())
    print("\n4a pass counts by panel/book/dial:")
    print(K.groupby(["panel", "book", "dial"])["pass4a"].sum().to_string())
    print(f"\n4a: {int(G.pass4a.sum())}/{len(G)}   4b: {int(G.pass4b.sum())}/{len(G)}")
    print("\n4b failing-bar census:")
    print(G[~G.pass4b].fail4b.value_counts().head(12).to_string())

    print("\n=== the default ('do-nothing') book of each panel x book at 10 bps ===")
    dflt = G[(G.bps == 10) & (G.dial == "G") & (G.value == 0.00)]
    print(dflt[["panel", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                "OOS_CAGR", "OOS_MaxDD", "turn_yr", "mean_invested", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nRULES v1 literal book (n=5, w=0.15) reference rows:")
    print(L[["panel", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "turn_yr",
             "mean_invested"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== RULE 8 walk-forward (dial chosen on 2009-2016, 2017-2026 read once) ===")
    print(WF[["panel", "book", "dial", "bps", "IS_pick", "do_nothing", "full_argmax",
              "pick_OOS_Sharpe", "dn_OOS_Sharpe", "rand_OOS_Sharpe", "oracle_OOS_Sharpe",
              "d_pick_minus_dn"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nmean d(pick - do-nothing) OOS Sharpe by dial:")
    print(WF.groupby("dial")["d_pick_minus_dn"]
          .agg(["mean", "min", "max", lambda s: (s > 0).mean()])
          .rename(columns={"<lambda_0>": "win_rate"}).to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nby book:")
    print(WF.groupby("book")[["d_pick_minus_dn", "d_rand_minus_dn"]]
          .mean().to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nby panel:")
    print(WF.groupby("panel")[["d_pick_minus_dn", "d_rand_minus_dn"]]
          .mean().to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\nOVERALL mean d(pick - do-nothing) = {WF.d_pick_minus_dn.mean():+.4f} "
          f"(random {WF.d_rand_minus_dn.mean():+.4f}), pick wins "
          f"{100*(WF.d_pick_minus_dn>0).mean():.1f}% of {len(WF)} cells")
    nv = WF[WF.dial != "V"]
    print(f"excluding the V dial: {nv.d_pick_minus_dn.mean():+.4f} over {len(nv)} cells, "
          f"wins {100*(nv.d_pick_minus_dn>0).mean():.1f}%")
    piv = WF.groupby(["panel", "book", "dial"])["IS_pick"].nunique()
    print(f"\nIS pick moves with the rung in {int((piv>1).sum())} of {len(piv)} cells:")
    print(piv[piv > 1].to_string())

    print("\n=== OOS levels at 10 bps (do-nothing vs baseline vs SPY) ===")
    w10 = WF[(WF.bps == 10) & (WF.dial == "G")]
    print(w10[["panel", "book", "dn_OOS_Sharpe", "dn_OOS_CAGR", "dn_OOS_MaxDD",
               "base_OOS_Sharpe", "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
