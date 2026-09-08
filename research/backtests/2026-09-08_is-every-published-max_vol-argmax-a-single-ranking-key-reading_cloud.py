#!/usr/bin/env python3
"""Idea 450 — is every published `max_vol` argmax a SINGLE-RANKING-KEY reading?

Pre-registration (fixed before any number was read):
  * Idea 232 showed the vol GATE (`vol20 < max_vol`) and the composite's 1/sqrt(vol20) rank
    TILT spend the same information: deleting the gate is worth +0.1345 mean Sharpe on the
    UN-TILTED key and +0.0171 on the LIVE (tilted) one.  If that is true, then the LOCATION
    of every published argmax over the `max_vol` dial is a statement about the key the book
    was ranked with, not about volatility.  This run back-fills BOTH keys under the dial and
    reports how many argmax locations survive the swap.
  * Book (one construction, two keys):  rank the panel every day by
        COMP  = score(px, vol_scale=False)   (un-tilted composite: mom + r6 + r3 ranks, x MA200 half-credit)
        V1KEY = score(px, vol_scale=True)    (the LIVE rules_v1 key: COMP / sqrt(clip(vol20,0.08)))
    eligibility = (close > 200d MA) AND (vol20 < max_vol); hold the top n at gross/n of NAV
    (RAW gross/n channel — fewer than n eligible names means a smaller realised gross; this is
    the channel `baseline.rules_v1_weights` itself uses, see gate G2).  Cash otherwise.
  * TWO tuned parameters, no more:  key in {COMP, V1KEY}, cost rung in {10, 25} bps.
    The `max_vol` dial is the OBJECT of the study, not a tuned parameter: every rung is
    reported for every cell and none is selected outside the rule-8 walk-forward.
        max_vol in {0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, OFF}   (8 rungs; 0.60 = live)
        n       in {5, 20}   (5 = live RULES v1, 20 = the 2026-09-04 4b KEEP shape) - reported, not tuned
        panels  = U56 (universe.json), B136 (universe_broad.json),
                  SMALL439 (sub-$2B panel less the 44 tickers with max_1d_move >= 1.0)
    3 panels x 2 keys x 8 rungs x 2 n x 2 cost rungs = 192 grid points, ALL reported.
  * Rule 8 walk-forward: `max_vol` chosen on IS <= 2016-12-31 by IS Sharpe, under each key
    separately; 2017-01-01.. read once.  Comparands: the pre-registered live 0.60, the
    pre-registered OFF, RULES v2 (live baseline) and SPY.
  * Both KEEP paths on every grid point: 4a vs live RULES v2 (cost-matched), 4b vs SPY.
  * SURVIVORSHIP: SMALL439 and B136 are CURRENT constituents only (data/SMALL_PANEL_README.md,
    universe_broad.json).  Levels are overstated on both; read the CONTRASTS between keys,
    which share the panel and therefore share the bias.

Costs 10/25 bps per unit turnover, weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .grid.csv, .argmax.csv, .walkforward.csv, .console.txt.
"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-08_is-every-published-max_vol-argmax-a-single-ranking-key-reading_cloud"
OUT = ROOT / "research" / "backtests"
VOLCAPS = [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, np.inf]   # inf = gate OFF
VLAB = {0.20: "0.20", 0.30: "0.30", 0.40: "0.40", 0.50: "0.50",
        0.60: "0.60", 0.80: "0.80", 1.00: "1.00", np.inf: "OFF"}
NS = [5, 20]
KEYS = ["COMP", "V1KEY"]
RUNGS = [10, 25]
GROSS = 0.75
FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, weights, cost_bps, freq):
    """Vectorised twin of engine.backtest (same drift, same t+1 application, same costs)."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, cost_bps):
    """Cost rung by the derived identity r(c) = r(0) - turnover * c / 1e4 (gated below)."""
    return res["returns0"] - res["turnover"] * cost_bps / 1e4


# ---------------------------------------------------------------- books
def topn_weights(px, n, max_vol, tilt, gross=GROSS):
    s, above, vol20 = score(px, vol_scale=tilt)
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def keep_flags(row, base, spy):
    """4a vs the live RULES v2 (PROTOCOL 4a); 4b vs SPY (PROTOCOL 4b, incl. rule-8 OOS)."""
    a = (row["Sharpe_H1"] > base["H1"]) and (row["Sharpe_H2"] > base["H2"]) and (row["MaxDD"] >= base["MaxDD"])
    b = (row["Sharpe_H1"] > spy["H1"] and row["Sharpe_H2"] > spy["H2"]
         and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and row["MaxDD"] >= 0.60 * spy["MaxDD"]          # MaxDD are negative: >= is "shallower than"
         and row["CAGR"] >= 0.70 * spy["CAGR"])
    return a, b


# ---------------------------------------------------------------- panels
def panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    out["SMALL439"] = sm[keep]
    return out


def main():
    PX = panels()
    for k, v in PX.items():
        say(f"panel {k}: {v.shape[1]} cols ({v.shape[1]-1} names + SPY), "
            f"{v.index[0].date()} -> {v.index[-1].date()}, {len(v)} days")

    # ------------------------------------------------------------ GATES
    say("\n=== GATES ===")
    px = PX["U56"]
    w = topn_weights(px, 5, 0.60, True)
    g2 = float(np.abs(w.values - rules_v1_weights(px).values).max())
    say(f"G2 construction: topn_weights(n=5, max_vol=0.60, tilt=True, gross=0.75) vs "
        f"baseline.rules_v1_weights  max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED: the book is not the live RULES v1 construction"

    eb = engine_backtest(px, w, cost_bps=10, freq=FREQ)
    fb = fast_backtest(px, w, 10, FREQ)
    # engine.backtest seeds cur from the SHIFTED weight row, which is NaN on day 0, so its
    # first two days (up to the first rebalance) are NaN; fast_backtest fills that row with 0.
    # Both are 258 trading days before the warm-up start px.index[260], so the gate is read
    # on the evaluation window (and the NaN count is reported rather than hidden).
    gst = px.index[260]
    say(f"G0 engine.backtest NaN return days before warm-up: {int(eb['returns'].isna().sum())} "
        f"(latest {eb['returns'].index[eb['returns'].isna()].max().date()}; warm-up starts {gst.date()})")
    g1 = float(np.abs((eb["returns"] - net(fb, 10)).loc[gst:].values).max())
    say(f"G1 fast_backtest vs engine.backtest @10 bps      max|diff| = {g1:.3e}")
    eb25 = engine_backtest(px, w, cost_bps=25, freq=FREQ)
    g3 = float(np.abs((eb25["returns"] - net(fb, 25)).loc[gst:].values).max())
    say(f"G3 derived rung identity vs engine.backtest(25)  max|diff| = {g3:.3e}")
    g4 = float(np.abs((eb["weights"].sum(axis=1) - fb["gross"]).loc[gst:].values).max())
    say(f"G4 realised-gross series vs engine held weights  max|diff| = {g4:.3e}")
    assert max(g1, g3, g4) < 1e-12, "GATE FAILED"

    ebv2 = engine_backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)
    st = px.index[260]
    m = mstats(ebv2["returns"].loc[st:])
    say(f"G5 LIVE RULES v2 on U56 @10 bps: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%} "
        f"(H {m['H1']:.4f} / {m['H2']:.4f})   [record: 8.66% / 1.2056 / -12.05% / 1.2259 / 1.1908]")

    # ------------------------------------------------------------ CENSUS of the record
    say("\n=== CENSUS: which key does the record's `max_vol` work use? ===")
    files = sorted((ROOT / "research" / "backtests").glob("*.py"))
    swept, tilted_only, both_keys, untilted_only = [], [], [], []
    for f in files:
        if f.name.startswith(STAMP):
            continue
        t = f.read_text(errors="ignore")
        if not re.search(r"max_vol|MAX_VOL|VOLCAP|volcap", t):
            continue
        swept.append(f.name)
        has_false = bool(re.search(r"vol_scale\s*=\s*False", t))
        has_true = bool(re.search(r"vol_scale\s*=\s*True", t))
        # a script that never mentions vol_scale ranks with baseline.score's default (True)
        if has_false and has_true: both_keys.append(f.name)
        elif has_false: untilted_only.append(f.name)
        else: tilted_only.append(f.name)
    say(f"committed scripts: {len(files)}; touching the vol-cap dial: {len(swept)}")
    say(f"  ranked on the TILTED key only (vol_scale default/True): {len(tilted_only)}")
    say(f"  ranked on the UN-TILTED key only (vol_scale=False):     {len(untilted_only)}")
    say(f"  carry BOTH keys:                                        {len(both_keys)}")
    for f in both_keys: say(f"    both: {f}")
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n")
    argmax_rows = [l for l in lb if re.search(r"max_vol|VOLCAP", l)]
    say(f"LEADERBOARD rows naming the dial: {len(argmax_rows)}")

    # ------------------------------------------------------------ GRID
    say("\n=== GRID: 3 panels x 2 keys x 8 vol caps x 2 n x 2 rungs = 192 points ===")
    rows = []
    ctx = {}
    for pname, px in PX.items():
        st = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[st:]
        base_r = net(fast_backtest(px, rules_v2_weights(px), 0, FREQ), 10).loc[st:]
        ctx[pname] = {}
        for rung in RUNGS:
            b = mstats(net(fast_backtest(px, rules_v2_weights(px), 0, FREQ), rung).loc[st:])
            b["OOS_Sharpe"] = metrics(net(fast_backtest(px, rules_v2_weights(px), 0, FREQ), rung).loc[OOS_START:])["Sharpe"]
            s = mstats(spy_r); s["OOS_Sharpe"] = metrics(spy_r.loc[OOS_START:])["Sharpe"]
            s["OOS_CAGR"] = metrics(spy_r.loc[OOS_START:])["CAGR"]
            s["OOS_MaxDD"] = metrics(spy_r.loc[OOS_START:])["MaxDD"]
            ctx[pname][rung] = dict(base=b, spy=s)
        for key in KEYS:
            tilt = (key == "V1KEY")
            for n in NS:
                for v in VOLCAPS:
                    res = fast_backtest(px, topn_weights(px, n, v, tilt), 0, FREQ)
                    for rung in RUNGS:
                        r = net(res, rung).loc[st:]
                        m = mstats(r)
                        oos = metrics(r.loc[OOS_START:])
                        row = dict(panel=pname, key=key, n=n, volcap=VLAB[v], volcap_num=v, rung=rung,
                                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                   Sharpe_H1=m["H1"], Sharpe_H2=m["H2"],
                                   OOS_Sharpe=oos["Sharpe"], OOS_CAGR=oos["CAGR"], OOS_MaxDD=oos["MaxDD"],
                                   IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                   turnover=res["turnover"].loc[st:].sum() / (len(r) / 252),
                                   gross=res["gross"].loc[st:].mean())
                        a, b4 = keep_flags(row, ctx[pname][rung]["base"], ctx[pname][rung]["spy"])
                        row["pass4a"], row["pass4b"] = a, b4
                        rows.append(row)
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say(f"grid points: {len(G)}  (4a passes {int(G.pass4a.sum())}, 4b passes {int(G.pass4b.sum())})")

    # ------------------------------------------------------------ PROVENANCE
    say("\n=== PROVENANCE: two committed rows must fall out of this grid unchanged ===")
    q = G[(G.panel == "U56") & (G.key == "COMP") & (G.n == 20) & (G.rung == 10)].set_index("volcap")
    r060, roff = q.loc["0.60"], q.loc["OFF"]
    say(f"G6 idea 2's KEEP-4b row `2 OFF EQW n=20` (the 2026-09-04 incumbent, vol cap at the live 0.60):")
    say(f"   here {r060.CAGR:.2%} / {r060.Sharpe:.4f} / {r060.MaxDD:.2%} (H {r060.Sharpe_H1:.4f} / {r060.Sharpe_H2:.4f})"
        f"   published 12.7% / 1.09 / -18.3% (1.09 / 1.10)")
    say(f"G7 idea 228's `U56 n=20 max_vol=off` row (idea 232's audit re-quotes it at g=0.75):")
    say(f"   here {roff.CAGR:.2%} / {roff.Sharpe:.4f} / {roff.MaxDD:.2%}, OOS {roff.OOS_Sharpe:.4f}"
        f"   published 14.27% / 1.1469 / -19.39%, OOS 1.1707")

    say("\n--- full grid, Sharpe @10 bps (rows = vol cap, cols = panel x key), n=20 ---")
    for n in NS:
        sub = G[(G.rung == 10) & (G.n == n)]
        piv = sub.pivot_table(index="volcap", columns=["panel", "key"], values="Sharpe")
        piv = piv.reindex([VLAB[v] for v in VOLCAPS])
        say(f"n={n}:\n" + piv.to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ ARGMAX SWAP
    say("\n=== THE QUESTION: does the argmax LOCATION survive the key swap? ===")
    amrows = []
    for (pname, n, rung), sub in G.groupby(["panel", "n", "rung"]):
        for metric in ["Sharpe", "CAGR", "OOS_Sharpe"]:
            loc, val, spread = {}, {}, {}
            for key in KEYS:
                s = sub[sub.key == key].set_index("volcap")[metric].reindex([VLAB[v] for v in VOLCAPS])
                loc[key] = s.idxmax(); val[key] = s.max(); spread[key] = s.max() - s.min()
            # cross-evaluation: what does each key's argmax cost the OTHER key?
            cross = {}
            for key in KEYS:
                other = "V1KEY" if key == "COMP" else "COMP"
                s_other = sub[sub.key == other].set_index("volcap")[metric]
                cross[key] = s_other[loc[other]] - s_other[loc[key]]     # loss on `other` from importing key's pick
            amrows.append(dict(panel=pname, n=n, rung=rung, metric=metric,
                               argmax_COMP=loc["COMP"], argmax_V1KEY=loc["V1KEY"],
                               same=loc["COMP"] == loc["V1KEY"],
                               val_COMP=val["COMP"], val_V1KEY=val["V1KEY"],
                               spread_COMP=spread["COMP"], spread_V1KEY=spread["V1KEY"],
                               loss_on_V1KEY_from_COMP_pick=cross["COMP"],
                               loss_on_COMP_from_V1KEY_pick=cross["V1KEY"]))
    A = pd.DataFrame(amrows)
    A.to_csv(OUT / f"{STAMP}.argmax.csv", index=False)
    say(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nargmax LOCATION identical under both keys: {int(A.same.sum())} of {len(A)} cells "
        f"({A.same.mean():.1%})")
    for metric, s in A.groupby("metric"):
        say(f"  {metric:11s}: same {int(s.same.sum())}/{len(s)}; "
            f"mean dial spread COMP {s.spread_COMP.mean():.4f} vs V1KEY {s.spread_V1KEY.mean():.4f} "
            f"({s.spread_COMP.mean()/max(s.spread_V1KEY.mean(),1e-12):.2f}x); "
            f"mean cost of importing the other key's pick: onto V1KEY {s.loss_on_V1KEY_from_COMP_pick.mean():.4f}, "
            f"onto COMP {s.loss_on_COMP_from_V1KEY_pick.mean():.4f}")
    say("\nHow often is the argmax at the OFF corner (no vol gate at all)?")
    for key in KEYS:
        c = (A[f"argmax_{key}"] == "OFF").mean()
        say(f"  {key}: {c:.1%} of {len(A)} cells")

    # ------------------------------------------------------------ RULE 8
    say("\n=== RULE 8 walk-forward: max_vol chosen on IS <= 2016 by IS Sharpe, 2017+ read once ===")
    wf = []
    for (pname, n, rung, key), sub in G.groupby(["panel", "n", "rung", "key"]):
        s = sub.set_index("volcap")
        pick = s["IS_Sharpe"].idxmax()
        r = s.loc[pick]
        preg60, pregoff = s.loc["0.60"], s.loc["OFF"]
        sp = ctx[pname][rung]["spy"]; bs = ctx[pname][rung]["base"]
        wf.append(dict(panel=pname, n=n, rung=rung, key=key, IS_pick=pick,
                       OOS_Sharpe=r["OOS_Sharpe"], OOS_CAGR=r["OOS_CAGR"], OOS_MaxDD=r["OOS_MaxDD"],
                       OOS_Sharpe_at_060=preg60["OOS_Sharpe"], OOS_Sharpe_at_OFF=pregoff["OOS_Sharpe"],
                       OOS_Sharpe_best=s["OOS_Sharpe"].max(), oracle_regret=s["OOS_Sharpe"].max() - r["OOS_Sharpe"],
                       SPY_OOS_Sharpe=sp["OOS_Sharpe"], SPY_OOS_CAGR=sp["OOS_CAGR"], SPY_OOS_MaxDD=sp["OOS_MaxDD"],
                       BASE_OOS_Sharpe=bs["OOS_Sharpe"],
                       beats_SPY=r["OOS_Sharpe"] > sp["OOS_Sharpe"], beats_BASE=r["OOS_Sharpe"] > bs["OOS_Sharpe"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nIS chooser picks the SAME rung under both keys in "
        f"{int((W.pivot_table(index=['panel','n','rung'], columns='key', values='IS_pick', aggfunc='first').nunique(axis=1) == 1).sum())}"
        f" of {len(W)//2} (panel,n,rung) cells")
    say(f"chooser beats the pre-registered 0.60: {(W.OOS_Sharpe > W.OOS_Sharpe_at_060).sum()}/{len(W)}; "
        f"beats pre-registered OFF: {(W.OOS_Sharpe > W.OOS_Sharpe_at_OFF).sum()}/{len(W)}; "
        f"mean oracle regret {W.oracle_regret.mean():.4f}")
    say(f"chooser beats SPY OOS: {int(W.beats_SPY.sum())}/{len(W)}; beats RULES v2 OOS: {int(W.beats_BASE.sum())}/{len(W)}")

    # ------------------------------------------------------------ KEEP paths
    say("\n=== KEEP paths over all 192 grid points ===")
    say(f"4a (vs live RULES v2): {int(G.pass4a.sum())}/{len(G)}")
    say(f"4b (vs SPY, incl. rule-8 OOS): {int(G.pass4b.sum())}/{len(G)}")
    if G.pass4b.any():
        say(G[G.pass4b].sort_values("Sharpe", ascending=False).head(12)
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for pname in PX:
        sub = G[G.panel == pname]
        say(f"  {pname}: 4a {int(sub.pass4a.sum())}/{len(sub)}, 4b {int(sub.pass4b.sum())}/{len(sub)} "
            f"(COMP {int(sub[sub.key=='COMP'].pass4b.sum())}, V1KEY {int(sub[sub.key=='V1KEY'].pass4b.sum())})")
    say("\nreference rows (10 bps, full sample, from ctx):")
    for pname in PX:
        b, s = ctx[pname][10]["base"], ctx[pname][10]["spy"]
        say(f"  {pname} RULES v2 {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} (H {b['H1']:.3f}/{b['H2']:.3f}); "
            f"SPY {s['CAGR']:.2%}/{s['Sharpe']:.4f}/{s['MaxDD']:.2%} (H {s['H1']:.3f}/{s['H2']:.3f}, OOS {s['OOS_Sharpe']:.4f})")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
