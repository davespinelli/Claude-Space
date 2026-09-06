#!/usr/bin/env python3
"""Idea 228 — does-any-dial-argmax-move-with-cost (lane C, 2026-09-06).

Pre-registered question (QUEUE 228): idea 155 found argmax_q flat across 0-30 bps on all
three panels because Spearman(q, turnover) = -1.000.  Census the record's OTHER swept dials
(n, band g, cadence, vol threshold) for the same property: compute Spearman(dial, turnover)
and argmax-vs-rung for each, and report which dials the cost rung can actually re-rank.
If none can, PROTOCOL's cost ladder is a level check, not a chooser.

Two tuned parameters only: the DIAL VALUE and the COST RUNG.  Every grid point is reported.

Construction (pre-registered, held fixed across all four dials — this is the record's
standing 4b candidate shape: top-n equal weight, no vol scaler, gross 1.00):
    eligible_t  = (band-gated 200d trend) AND (vol20 < max_vol)
    rank        = RULES v1 composite (12-1 / 6m / 3m rank average), NO vol scaler
    hold        = top n eligible, 1/n each, rebalanced every k weeks
    defaults    = n=20, g=0.00, max_vol=0.60, k=1  (the "do-nothing" point of every dial)

Cost ladder uses the exact identity net(c) = gross - turnover * c/1e4 (held weights and
turnover do not depend on cost), asserted against engine.backtest at 10 bps.

Outputs (all committed):
    .grid.csv        every (panel, dial, value, rung) point: turnover, CAGR/Sharpe/MaxDD,
                     H1/H2, OOS, 4a/4b pass and failing bar
    .census.csv      per (panel, dial): Spearman(dial, turnover), argmax at each rung,
                     number of distinct argmaxes, re-rank verdict
    .walkforward.csv rule 8: dial chosen on 2009-2016 at each rung, 2017-2026 read once,
                     against do-nothing / random / oracle / RULES v1 / SPY
    .keep.csv        4a and 4b pass counts per (panel, dial, rung)
"""
import sys, itertools, time
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


def spearman(a, b):
    """Rank correlation without scipy (pandas' spearman needs it)."""
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
    """engine.backtest's loop with an arbitrary rebalance mask; returns GROSS returns and turnover."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    ncol = px.shape[1]
    cur = np.zeros(ncol)
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
    invested = pd.Series(held.sum(axis=1), index=px.index)     # idea 157's cash channel
    return gross, pd.Series(turn, index=px.index), invested


def book_weights(px, comp, ma, vol20, n, g, max_vol):
    """Top-n equal weight over the band-gated, vol-capped eligible set. Gross 1.00."""
    if g == 0:
        above = px > ma
    else:                                        # hysteresis band around the 200d MA
        sig = pd.DataFrame(np.where(px > ma * (1 + g), 1.0,
                           np.where(px < ma * (1 - g), 0.0, np.nan)),
                           index=px.index, columns=px.columns)
        above = sig.ffill().fillna(0.0) > 0.5
    elig = comp.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) / n


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
    return ("" if not fail else ",".join(fail))


def bars_4b(s, spy, oos_s, oos_spy):
    """4b: Sharpe > SPY in both halves AND OOS; MaxDD <= 60% of SPY's; CAGR >= 70% of SPY's."""
    fail = []
    if not s["H1"] > spy["H1"]: fail.append("H1")
    if not s["H2"] > spy["H2"]: fail.append("H2")
    if not oos_s > oos_spy: fail.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: fail.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fail.append("CAGR")
    return ("" if not fail else ",".join(fail))


# ---------------------------------------------------------------- panels
def panels():
    yield "U56", load_universe()
    yield "B136", load_universe(broad=True)
    yield "SMALL484", load_universe(small=True)


def main():
    t0 = time.time()
    grid, census, wf_rows, ident = [], [], [], []
    for pname, px in panels():
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))     # exact: recover the composite
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])["Sharpe"]

        # --- RULES v1 baseline on this panel, per rung (weekly, per PROTOCOL rule 3)
        bg, bt, _ = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base = {c: stats(net(bg, bt, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(bg, bt, c).loc[OOS_START:])["Sharpe"] for c in RUNGS}
        # identity + engine check at 10 bps
        eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append((pname, float(np.abs(eng - net(bg, bt, 10).loc[start:]).max())))

        cache = {}
        for dial, values in DIAL_VALUES.items():
            for v in values:
                kw = dict(DEFAULTS); kw[dial] = v
                if dial == "N" and v > px.shape[1] - 1:
                    continue
                W = book_weights(px, comp, ma, vol20, kw["N"], kw["G"], kw["V"])
                gross, turn, inv = simulate(px, W, week_mask(px.index, kw["K"]))
                g_s, t_s = gross.loc[start:], turn.loc[start:]
                yrs = len(g_s) / 252
                cache[(dial, v)] = (g_s, t_s)
                for c in RUNGS:
                    r = net(g_s, t_s, c)
                    st = stats(r)
                    o = metrics(r.loc[OOS_START:])
                    grid.append(dict(panel=pname, dial=dial, value=v, bps=c,
                                     turn_yr=t_s.sum() / yrs, mean_invested=float(inv.loc[start:].mean()), **st,
                                     OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                     fail4a=bars_4a(st, base[c]), fail4b=bars_4b(st, spy_s, o["Sharpe"], spy_oos)))

            # ---- census for this (panel, dial)
            g = pd.DataFrame([x for x in grid if x["panel"] == pname and x["dial"] == dial])
            vals = sorted(g["value"].unique())
            turns = g[g.bps == 0].set_index("value")["turn_yr"].reindex(vals)
            rho = spearman(vals, turns.values)
            arg = {c: g[g.bps == c].set_index("value")["Sharpe"].idxmax() for c in RUNGS}
            sh0 = g[g.bps == 0].set_index("value")["Sharpe"]
            sh30 = g[g.bps == 30].set_index("value")["Sharpe"]
            census.append(dict(panel=pname, dial=dial, n_values=len(vals),
                               spearman_dial_turnover=rho,
                               turn_min=turns.min(), turn_max=turns.max(),
                               **{f"argmax_{c}bps": arg[c] for c in RUNGS},
                               n_distinct_argmax=len(set(arg.values())),
                               rerankable=len(set(arg.values())) > 1,
                               first_move_bps=next((c for c in RUNGS if arg[c] != arg[0]), np.nan),
                               sharpe_range_10bps=float(g[g.bps == 10]["Sharpe"].max() - g[g.bps == 10]["Sharpe"].min()),
                               cost_of_0bps_pick_at_30=float(sh30.max() - sh30.loc[arg[0]])))

            # ---- rule 8 walk-forward for this (panel, dial), per rung
            for c in RUNGS:
                sub = {v: net(cache[(dial, v)][0], cache[(dial, v)][1], c) for (d, v) in cache if d == dial}
                is_sh = {v: metrics(r.loc[:IS_END])["Sharpe"] for v, r in sub.items()}
                pick = max(is_sh, key=is_sh.get)
                full_arg = max(sub, key=lambda v: metrics(sub[v])["Sharpe"])
                dn = DEFAULTS[dial]
                oos = lambda v: metrics(sub[v].loc[OOS_START:])
                wf_rows.append(dict(panel=pname, dial=dial, bps=c, IS_pick=pick, do_nothing=dn,
                                    full_argmax=full_arg,
                                    pick_OOS_Sharpe=oos(pick)["Sharpe"], pick_OOS_CAGR=oos(pick)["CAGR"],
                                    pick_OOS_MaxDD=oos(pick)["MaxDD"],
                                    dn_OOS_Sharpe=oos(dn)["Sharpe"], dn_OOS_CAGR=oos(dn)["CAGR"],
                                    dn_OOS_MaxDD=oos(dn)["MaxDD"],
                                    rand_OOS_Sharpe=float(np.mean([oos(v)["Sharpe"] for v in sub])),
                                    oracle_OOS_Sharpe=oos(full_arg)["Sharpe"],
                                    d_pick_minus_dn=oos(pick)["Sharpe"] - oos(dn)["Sharpe"],
                                    d_rand_minus_dn=float(np.mean([oos(v)["Sharpe"] for v in sub])) - oos(dn)["Sharpe"],
                                    base_OOS_Sharpe=base_oos[c], spy_OOS_Sharpe=spy_oos,
                                    spy_OOS_CAGR=metrics(spy_r.loc[OOS_START:])["CAGR"],
                                    spy_OOS_MaxDD=metrics(spy_r.loc[OOS_START:])["MaxDD"]))
        print(f"{pname}: done {time.time()-t0:.0f}s", flush=True)

    G = pd.DataFrame(grid); C = pd.DataFrame(census); WF = pd.DataFrame(wf_rows)
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.census.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    K = G.groupby(["panel", "dial", "bps"])[["pass4a", "pass4b"]].sum().reset_index()
    K.to_csv(f"{OUT}.keep.csv", index=False)

    print("\n=== identity/engine check (max |engine@10bps - gross - turn*c/1e4|) ===")
    for p, d in ident: print(f"  {p}: {d:.3e}")

    # --- parent dial (idea 155's q) read from its committed grid, no re-simulation
    par = pd.read_csv(ROOT / "research/backtests/2026-09-06_where-selectivity-and-cost-cross_B.grid.csv")
    prow = []
    for p, sub in par.groupby("panel"):
        vals = sorted(sub.q.unique())
        turns = sub[sub.bps == 0].set_index("q")["turn_yr"].reindex(vals)
        arg = {c: sub[sub.bps == c].set_index("q")["Sharpe"].idxmax() for c in RUNGS if c in set(sub.bps)}
        prow.append(dict(panel=p, dial="Q(parent 155)", n_values=len(vals),
                         spearman_dial_turnover=spearman(vals, turns.values),
                         n_distinct_argmax=len(set(arg.values())), argmaxes=sorted(set(arg.values()))))
    P = pd.DataFrame(prow)
    print("\n=== parent check: idea 155's q dial re-read from its committed grid ===")
    print(P.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n=== CENSUS: Spearman(dial, turnover) and argmax vs cost rung ===")
    cols = ["panel", "dial", "spearman_dial_turnover", "turn_min", "turn_max"] + \
           [f"argmax_{c}bps" for c in RUNGS] + ["n_distinct_argmax", "rerankable",
                                                "sharpe_range_10bps", "cost_of_0bps_pick_at_30"]
    print(C[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    # --- mechanism: a rung re-ranks iff the 0-bps top-2 gap is smaller than the tilt the
    #     ladder applies over that pair.  Sharpe is exactly linear in the rung only in the
    #     numerator, so measure the tilt empirically as the 0->30 bps Sharpe slope spread.
    mech = []
    for (p_, d_), sub in G.groupby(["panel", "dial"]):
        s0 = sub[sub.bps == 0].set_index("value")["Sharpe"].sort_values(ascending=False)
        s30 = sub[sub.bps == 30].set_index("value")["Sharpe"]
        best0 = s0.index[0]
        gap = float(s0.iloc[0] - s0.iloc[1])
        slope = (s30 - s0) / 30.0                       # Sharpe per bp, negative
        tilt = float((slope - slope.loc[best0]).max() * 30.0)   # best available 30-bp gain on the leader
        mech.append(dict(panel=p_, dial=d_, argmax_0bps=best0, top2_gap_0bps=gap,
                         max_tilt_30bps=tilt, predicted_rerank=tilt > gap,
                         actual_rerank=bool(C.set_index(["panel", "dial"]).loc[(p_, d_), "rerankable"])))
    M = pd.DataFrame(mech)
    M.to_csv(f"{OUT}.mechanism.csv", index=False)
    print("\n=== MECHANISM: 0-bps top-2 gap vs the ladder's maximum 30-bp tilt ===")
    print(M.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("predicted == actual in", int((M.predicted_rerank == M.actual_rerank).sum()), "of", len(M), "cells")

    hi = C[[f"argmax_{c}bps" for c in RUNGS if c >= 10]].nunique(axis=1)
    print(f"\nArgmax changes ANYWHERE in 10-30 bps: {int((hi > 1).sum())} of {len(C)} cells.")
    lo = C[[f"argmax_{c}bps" for c in RUNGS if c <= 10]].nunique(axis=1)
    print(f"Argmax changes in 0-10 bps:            {int((lo > 1).sum())} of {len(C)} cells.")

    print("\n=== 4b passes (every passing grid point) ===")
    print(G[G.pass4b][["panel", "dial", "value", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                       "OOS_Sharpe", "turn_yr", "mean_invested"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n=== cash channel (idea 157): mean invested fraction by dial value, 10 bps ===")
    print(G[G.bps == 10].pivot_table(index="value", columns=["panel", "dial"], values="mean_invested")
          .to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n=== 4a passes by panel/dial ===")
    print(G[G.pass4a].groupby(["panel", "dial"]).size().to_string())

    print("\n=== rule 8 excluding the V dial (the 'switch the gate off' corner) ===")
    nv = WF[WF.dial != "V"]
    print(f"mean d(pick - do-nothing) = {nv.d_pick_minus_dn.mean():+.4f} over {len(nv)} cells, "
          f"wins {100*(nv.d_pick_minus_dn>0).mean():.1f}%")

    print(f"\nRe-rankable dials: {int(C.rerankable.sum())} of {len(C)} (panel x dial cells).")
    print("|Spearman| == 1.000 in", int((C.spearman_dial_turnover.abs().round(3) == 1.0).sum()), "of", len(C), "cells.")
    ct = pd.crosstab(C.spearman_dial_turnover.abs().round(3) == 1.0, C.rerankable)
    print("\nmonotone-turnover x re-rankable:\n", ct.to_string())

    print("\n=== KEEP paths (rows passing, out of all grid points) ===")
    print(f"4a: {int(G.pass4a.sum())}/{len(G)}   4b: {int(G.pass4b.sum())}/{len(G)}")
    print(K.pivot_table(index=["panel", "dial"], columns="bps", values="pass4b").to_string())
    print("\n4b failing-bar census:")
    print(G[~G.pass4b].fail4b.value_counts().head(12).to_string())

    print("\n=== RULE 8 walk-forward (dial chosen on 2009-2016, 2017-2026 read once) ===")
    print(WF[["panel", "dial", "bps", "IS_pick", "do_nothing", "full_argmax", "pick_OOS_Sharpe",
              "dn_OOS_Sharpe", "rand_OOS_Sharpe", "oracle_OOS_Sharpe", "d_pick_minus_dn"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nmean d(pick - do-nothing) OOS Sharpe by dial:")
    print(WF.groupby("dial")["d_pick_minus_dn"].agg(["mean", "min", "max", lambda s: (s > 0).mean()])
          .rename(columns={"<lambda_0>": "win_rate"}).to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nmean d by panel:")
    print(WF.groupby("panel")[["d_pick_minus_dn", "d_rand_minus_dn"]].mean().to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\nOVERALL mean d(pick - do-nothing) = {WF.d_pick_minus_dn.mean():+.4f} "
          f"(random {WF.d_rand_minus_dn.mean():+.4f}), pick wins {100*(WF.d_pick_minus_dn>0).mean():.1f}% of {len(WF)} cells")
    print("\nDoes the RUNG change the IS pick? (distinct IS picks across the 7 rungs)")
    piv = WF.groupby(["panel", "dial"])["IS_pick"].nunique()
    print(piv.to_string())
    print(f"  {int((piv>1).sum())} of {len(piv)} panel x dial cells have an IS pick that moves with cost.")

    print("\n=== OOS levels at 10 bps (do-nothing book vs baseline vs SPY) ===")
    w10 = WF[WF.bps == 10]
    print(w10[["panel", "dial", "dn_OOS_Sharpe", "dn_OOS_CAGR", "dn_OOS_MaxDD", "pick_OOS_Sharpe",
               "pick_OOS_CAGR", "pick_OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe", "spy_OOS_CAGR",
               "spy_OOS_MaxDD"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
