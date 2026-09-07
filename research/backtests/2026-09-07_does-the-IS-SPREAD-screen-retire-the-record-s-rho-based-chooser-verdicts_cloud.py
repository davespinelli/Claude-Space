#!/usr/bin/env python3
"""Idea 373 (cloud, 2026-09-07): does-the-IS-SPREAD-screen-retire-the-record's-rho-based-chooser-verdicts.

QUESTION (queue text): idea 371 found the gross dial inverts perfectly (rho -1.00, 6/6) on an IS
Sharpe spread of 0.001-0.005 -- i.e. rho ranked NOISE -- while the material damage was 4.8x OOS
drawdown that Sharpe never showed.  "Recompute the IS spread beside every rule-8 chooser verdict
already in LEADERBOARD.md and report how many rest on a spread below 0.01, and how many of those
flip when the pick is judged by OOS MaxDD instead."

TWO ARMS, because the leaderboard's verdicts are prose but their EVIDENCE is committed:

  [A] CORPUS CENSUS (zero backtests).  Every committed research/backtests/*.csv carrying the
      record's canonical triple `IS_Sharpe` / `OOS_Sharpe` / `OOS_MaxDD` is a grid a rule-8
      chooser was run on.  A MENU is the set of rows sharing every pre-registered STRATIFIER
      present in that file (panel, universe, book, form, cost, bps, cost_bps, rung, freq,
      cadence, kind) -- the dial being chosen over is whatever is left.  Both menu definitions
      are reported: STRATIFIED (primary) and FILE-LEVEL (every row of the file, one menu).
      Per menu: S1 = IS_top1 - IS_top2 (idea 241's margin), the IS argmax pick, its OOS Sharpe
      regret, and the SAME menu re-scored on OOS MaxDD.

  [B] LIVE REPLICATION (backtests).  The corpus reads committed numbers; this arm rebuilds six
      dials from source on three panels at three cost rungs, chooses on IS <= 2016-12-31 and
      reads 2017- once, so every statistic above is recomputed on paths this file controls --
      including OOS MaxDD, which most committed grids report but no chooser in the record scored.

DEFINITIONS (fixed before any number was read)
    S1          = IS_Sharpe(top1) - IS_Sharpe(top2)          "the IS spread"
    regret      = OOS_Sharpe(menu best) - OOS_Sharpe(pick)
    dd_regret   = |OOS_MaxDD(pick)| - |OOS_MaxDD(menu best by OOS MaxDD)|   in pp
    ARGMAX FLIP = the IS pick is not the menu's best arm by OOS MaxDD
    VERDICT FLIP= the pick beats its menu's MEDIAN arm on OOS Sharpe but LOSES to it on OOS MaxDD
                  (or the reverse) -- i.e. the published verdict's sign depends on which of the
                  two OOS columns it was scored on.

TUNED PARAMETERS: none.  The spread threshold is a REPORTED LADDER (0.005/0.01/0.02/0.05/0.10),
the menu definition is a REPORTED axis, and the live arm's six dials are all reported in full.

BOTH KEEP PATHS are evaluated at every live grid point (4a vs the live RULES v2 on the same panel,
4b vs SPY over the same window).

CAVEATS: (1) the corpus is the record's committed CSVs, which is a superset of the leaderboard's
chooser verdicts and includes menus no chooser was ever run on -- so the census answers "how many
menus in the record's evidence rest on a spread below 0.01", which is the queue's question up to
that widening, and the live arm pins the same statistics on a pre-registered menu set.
(2) Benchmark rows (SPY) are dropped from menus: a benchmark is never a selectable arm.
(3) Current-constituent panels: survivorship flatters every level in arm [B].

Deterministic, standalone, offline.  Modifies nothing.
"""
import re
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score                 # noqa
from engine import backtest, metrics                                        # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
OUT = ROOT / "research" / "backtests" / "2026-09-07_does-the-IS-SPREAD-screen-retire-the-record-s-rho-based-chooser-verdicts_cloud"
BT = ROOT / "research" / "backtests"

STRATIFIERS = ["panel", "universe", "book", "form", "cost", "bps", "cost_bps", "rung",
               "freq", "cadence", "kind"]
THRESHOLDS = [0.005, 0.01, 0.02, 0.05, 0.10]
MIN_MENU = 3
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP, FREQ = 260, "W"
MAX_VOL, GROSS, BAND = 0.60, 0.75, 0.03
COSTS = [0, 10, 25]


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, dtype=float)), pd.Series(np.asarray(b, dtype=float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(a[ok].rank().corr(b[ok].rank()))


# ================================================================ [A] corpus census
def menus_from_file(f, stratified=True):
    try:
        d = pd.read_csv(f)
    except Exception:
        return []
    if not {"IS_Sharpe", "OOS_Sharpe"}.issubset(d.columns) or "OOS_MaxDD" not in d.columns:
        return []
    d = d[d.IS_Sharpe.notna() & d.OOS_Sharpe.notna() & d.OOS_MaxDD.notna()].copy()
    if d.empty:
        return []
    obj = d.select_dtypes(include=["object", "string"])
    if len(obj.columns):
        is_bench = obj.apply(lambda c: c.astype(str).str.fullmatch("SPY", case=False).fillna(False)).any(axis=1)
        d = d[~is_bench]
    keys = [c for c in STRATIFIERS if c in d.columns] if stratified else []
    groups = d.groupby(keys, dropna=False) if keys else [((), d)]
    out = []
    for k, g in groups:
        if len(g) < MIN_MENU:
            continue
        g = g.sort_values("IS_Sharpe", ascending=False)
        pick = g.iloc[0]
        s1 = float(g.IS_Sharpe.iloc[0] - g.IS_Sharpe.iloc[1])
        best_sh = g.OOS_Sharpe.max()
        # OOS MaxDD is negative; the best arm is the one closest to zero
        best_dd = g.OOS_MaxDD.max()
        med_sh, med_dd = g.OOS_Sharpe.median(), g.OOS_MaxDD.median()
        argmax_flip = bool(abs(pick.OOS_MaxDD - best_dd) > 1e-12)
        beats_med_sh = bool(pick.OOS_Sharpe > med_sh)
        beats_med_dd = bool(pick.OOS_MaxDD > med_dd)
        out.append(dict(file=Path(f).name, keys="|".join(map(str, k)) if isinstance(k, tuple) else str(k),
                        n=len(g), S1=s1, IS_spread=float(g.IS_Sharpe.max() - g.IS_Sharpe.min()),
                        OOS_pick=float(pick.OOS_Sharpe), OOS_best=float(best_sh),
                        regret=float(best_sh - pick.OOS_Sharpe),
                        OOS_MaxDD_pick=float(pick.OOS_MaxDD), OOS_MaxDD_best=float(best_dd),
                        OOS_MaxDD_med=float(med_dd),
                        dd_regret_pp=100.0 * (abs(pick.OOS_MaxDD) - abs(best_dd)),
                        dd_ratio=float(abs(pick.OOS_MaxDD) / abs(best_dd)) if abs(best_dd) > 1e-9 else np.nan,
                        argmax_flip=argmax_flip, beats_med_sh=beats_med_sh, beats_med_dd=beats_med_dd,
                        verdict_flip=bool(beats_med_sh != beats_med_dd),
                        OOS_sh_spread=float(g.OOS_Sharpe.max() - g.OOS_Sharpe.min())))
    return out


def corpus():
    print("=" * 118)
    print("[A] CORPUS CENSUS - every committed grid carrying IS_Sharpe / OOS_Sharpe / OOS_MaxDD")
    print("=" * 118)
    files = sorted(BT.glob("*.csv"))
    res = {}
    for tag, strat in (("STRATIFIED", True), ("FILE-LEVEL", False)):
        rows = []
        for f in files:
            rows += menus_from_file(f, strat)
        m = pd.DataFrame(rows)
        res[tag] = m
        nf = m.file.nunique() if len(m) else 0
        print(f"\n{tag}: {len(m)} menus from {nf} files, median menu size {m.n.median() if len(m) else float('nan'):.0f},"
              f" total arms {int(m.n.sum()) if len(m) else 0}")
        if not len(m):
            continue
        print(f"  IS spread S1: median {m.S1.median():.4f}, mean {m.S1.mean():.4f}, "
              f"p10 {m.S1.quantile(0.10):.4f}, p90 {m.S1.quantile(0.90):.4f}")
        lad = []
        for t in THRESHOLDS:
            sub = m[m.S1 < t]
            lad.append(dict(threshold=t, menus=len(sub), share=len(sub) / len(m),
                            mean_regret=sub.regret.mean(), med_regret=sub.regret.median(),
                            argmax_flip=sub.argmax_flip.mean(), verdict_flip=sub.verdict_flip.mean(),
                            med_dd_regret_pp=sub.dd_regret_pp.median(), med_dd_ratio=sub.dd_ratio.median()))
        lad.append(dict(threshold=np.inf, menus=len(m), share=1.0, mean_regret=m.regret.mean(),
                        med_regret=m.regret.median(), argmax_flip=m.argmax_flip.mean(),
                        verdict_flip=m.verdict_flip.mean(), med_dd_regret_pp=m.dd_regret_pp.median(),
                        med_dd_ratio=m.dd_ratio.median()))
        print("\n  the queue's count, as a ladder (rows are S1 < threshold; last row = all menus):")
        print(pd.DataFrame(lad).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        print(f"\n  Spearman(S1, OOS Sharpe regret) = {spearman(m.S1, m.regret):+.4f}"
              f"   (a working screen needs this NEGATIVE and large: small spread -> big regret)")
        print(f"  Spearman(S1, dd_regret_pp)      = {spearman(m.S1, m.dd_regret_pp):+.4f}")
        print(f"  Spearman(S1, menu OOS spread)   = {spearman(m.S1, m.OOS_sh_spread):+.4f}"
              f"   (is a tight IS menu just a tight menu?)")
        b = m.assign(bucket=pd.cut(m.S1, [-1e9, 0.005, 0.01, 0.02, 0.05, 0.10, 1e9],
                                   labels=["<0.005", "0.005-0.01", "0.01-0.02", "0.02-0.05",
                                           "0.05-0.10", ">0.10"]))
        print("\n  by S1 bucket:")
        print(b.groupby("bucket", observed=True).agg(
            menus=("regret", "size"), mean_regret=("regret", "mean"), med_regret=("regret", "median"),
            argmax_flip=("argmax_flip", "mean"), verdict_flip=("verdict_flip", "mean"),
            med_dd_ratio=("dd_ratio", "median"), med_dd_regret_pp=("dd_regret_pp", "median"),
            med_menu_n=("n", "median")).to_string(float_format=lambda x: f"{x:.4f}"))
        print(f"\n  ARGMAX FLIP (the IS pick is not the menu's best arm by OOS MaxDD): "
              f"{int(m.argmax_flip.sum())}/{len(m)} = {m.argmax_flip.mean():.1%}")
        print(f"  VERDICT FLIP (pick beats its menu median on one OOS column and loses on the other): "
              f"{int(m.verdict_flip.sum())}/{len(m)} = {m.verdict_flip.mean():.1%}")
        lo = m[m.S1 < 0.01]
        print(f"  restricted to the queue's S1 < 0.01: argmax flip {lo.argmax_flip.mean():.1%}, "
              f"verdict flip {lo.verdict_flip.mean():.1%}, median dd_ratio {lo.dd_ratio.median():.3f}, "
              f"median dd regret {lo.dd_regret_pp.median():.2f} pp"
              f"   (idea 371's own cell: 4.8x)")

        print("\n  ABSTENTION (idea 241): when S1 < t take the menu's MEDIAN-IS arm instead of its argmax")
        ab = []
        for t in THRESHOLDS:
            sub = m[m.S1 < t]
            ab.append(dict(threshold=t, menus_abstained=len(sub),
                           argmax_mean_OOS=sub.OOS_pick.mean(),
                           argmax_mean_regret=sub.regret.mean(),
                           mean_dd_regret_pp=sub.dd_regret_pp.mean()))
        print(pd.DataFrame(ab).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        print("  (the corpus cannot score the abstention arm's OOS itself -- committed grids do not"
              " carry the median arm's identity per menu -- so arm [B] runs it on live paths.)")
        m.to_csv(f"{OUT}.corpus_{tag.lower().replace('-', '')}.csv", index=False)
    return res


# ================================================================ [B] live replication
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def book_cols(px, panel):
    return [c for c in px.columns if not (panel == "SMALL439" and c == "SPY")]


def breadth(px):
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    priced = q.notna() & q.rolling(200).mean().notna()
    return (above & priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)


def topn(px, panel, n, g=GROSS):
    q = px[book_cols(px, panel)]
    s = score(q, vol_scale=False)[0]
    _, above, vol20 = score(q)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def ewall(px, panel, g=GROSS):
    q = px[book_cols(px, panel)]
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]), "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def live():
    print("\n" + "=" * 118)
    print("[B] LIVE REPLICATION - six dials x 3 panels x 3 rungs, IS <= 2016 chooses, 2017- read once")
    print("=" * 118)
    P = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    rows = []
    for panel, px in P.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        E = breadth(px)
        v2 = backtest(px, rules_v2_weights(px[book_cols(px, panel)], band=BAND, gross=GROSS
                                           ).reindex(columns=px.columns).fillna(0.0), cost_bps=0, freq=FREQ)
        base20 = backtest(px, topn(px, panel, 20), cost_bps=0, freq=FREQ)
        arms = []                                            # (dial, arm, weights, freq)
        for n in [3, 5, 10, 20, 40]:
            arms.append(("N", f"n{n}", topn(px, panel, n), FREQ))
        for g in [0.40, 0.55, 0.70, 0.85, 1.00]:
            arms.append(("GROSS", f"g{g:.2f}", topn(px, panel, 20, g), FREQ))
        for f in ["W", "M", "Q"]:
            arms.append(("CADENCE", f, topn(px, panel, 20), f))
        for b in [0.00, 0.03, 0.06, 0.12]:
            arms.append(("BAND", f"b{b:.2f}",
                         rules_v2_weights(px[book_cols(px, panel)], band=b, gross=GROSS
                                          ).reindex(columns=px.columns).fillna(0.0), FREQ))
        vol20 = base20["returns"].rolling(20).std() * np.sqrt(252)
        for t in [0.08, 0.10, 0.12, 0.15]:
            k = (t / vol20.replace(0, np.nan)).clip(upper=1.0).shift(1).fillna(1.0)
            arms.append(("VOLTGT", f"t{t:.2f}", topn(px, panel, 20).mul(k, axis=0), FREQ))
        for B in [0.00, 0.30, 0.40, 0.50]:
            armed = (E.shift(1) < B).fillna(False)
            arms.append(("BREADTH", f"B{B:.2f}", topn(px, panel, 20).mul(np.where(armed, 0.0, 1.0), axis=0), FREQ))
        for dial, arm, w, f in arms:
            r = backtest(px, w, cost_bps=0, freq=f)
            rr, tt = r["returns"].loc[start:], r["turnover"].loc[start:]
            for k in COSTS:
                rn = rr - tt * k / 1e4
                v2n = v2["returns"].loc[start:] - v2["turnover"].loc[start:] * k / 1e4
                mi, mo, m = metrics(rn.loc[:IS_END]), metrics(rn.loc[OOS_START:]), metrics(rn)
                p4b, f4b = bars_4b(rn, spy); p4a, f4a = bars_4a(rn, v2n)
                h1, h2 = hs(rn)
                rows.append(dict(panel=panel, dial=dial, arm=arm, bps=k,
                                 IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"], OOS_CAGR=mo["CAGR"],
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 turn=tt.mean() * 252, pass4a=p4a, fail4a=",".join(f4a),
                                 pass4b=p4b, fail4b=",".join(f4b)))
        print(f"    [{panel}] {len(arms)} arms x {len(COSTS)} rungs; SPY "
              f"{metrics(spy)['CAGR']:.1%}/{metrics(spy)['Sharpe']:.3f}/{metrics(spy)['MaxDD']:.1%}, "
              f"OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
    d = pd.DataFrame(rows)
    d.to_csv(f"{OUT}.live.csv", index=False)

    print("\n  per-menu chooser statistics (menu = panel x dial x rung, 54 menus):")
    out = []
    for (pan, dial, k), g in d.groupby(["panel", "dial", "bps"]):
        g = g.sort_values("IS_Sharpe", ascending=False)
        pick = g.iloc[0]
        med = g.iloc[len(g) // 2]                                  # the median-IS arm (abstention)
        best_dd = g.OOS_MaxDD.max()
        out.append(dict(panel=pan, dial=dial, bps=k, n=len(g), pick=pick.arm, S1=float(g.IS_Sharpe.iloc[0] - g.IS_Sharpe.iloc[1]),
                        OOS_pick=pick.OOS_Sharpe, OOS_best=g.OOS_Sharpe.max(),
                        regret=g.OOS_Sharpe.max() - pick.OOS_Sharpe,
                        OOS_MaxDD_pick=pick.OOS_MaxDD, OOS_MaxDD_best=best_dd,
                        dd_regret_pp=100 * (abs(pick.OOS_MaxDD) - abs(best_dd)),
                        dd_ratio=abs(pick.OOS_MaxDD) / abs(best_dd),
                        argmax_flip=abs(pick.OOS_MaxDD - best_dd) > 1e-12,
                        beats_med_sh=pick.OOS_Sharpe > g.OOS_Sharpe.median(),
                        beats_med_dd=pick.OOS_MaxDD > g.OOS_MaxDD.median(),
                        abst_arm=med.arm, abst_OOS=med.OOS_Sharpe, abst_OOS_MaxDD=med.OOS_MaxDD,
                        pick4b=pick.pass4b))
    w = pd.DataFrame(out)
    w["verdict_flip"] = w.beats_med_sh != w.beats_med_dd
    print(w[["panel", "dial", "bps", "n", "pick", "S1", "OOS_pick", "OOS_best", "regret",
             "OOS_MaxDD_pick", "OOS_MaxDD_best", "dd_ratio", "argmax_flip", "verdict_flip"]
            ].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    w.to_csv(f"{OUT}.rule8.csv", index=False)
    print(f"\n  menus with S1 < 0.01: {int((w.S1 < 0.01).sum())}/{len(w)};"
          f" argmax flip {w.argmax_flip.mean():.1%}; verdict flip {w.verdict_flip.mean():.1%}")
    print(f"  Spearman(S1, regret) = {spearman(w.S1, w.regret):+.4f};"
          f"  Spearman(S1, dd_regret_pp) = {spearman(w.S1, w.dd_regret_pp):+.4f}")
    lo, hi = w[w.S1 < 0.01], w[w.S1 >= 0.01]
    print(f"  mean regret  S1<0.01 {lo.regret.mean():.4f} (n={len(lo)})  vs  S1>=0.01 {hi.regret.mean():.4f} (n={len(hi)})")
    print(f"  mean dd_ratio S1<0.01 {lo.dd_ratio.mean():.3f}          vs  S1>=0.01 {hi.dd_ratio.mean():.3f}")
    print("\n  ABSTENTION scored on live paths (take the median-IS arm when S1 < t):")
    ab = []
    for t in THRESHOLDS:
        sel = w.S1 < t
        oos = np.where(sel, w.abst_OOS, w.OOS_pick)
        dd = np.where(sel, w.abst_OOS_MaxDD, w.OOS_MaxDD_pick)
        ab.append(dict(threshold=t, abstained=int(sel.sum()), mean_OOS=float(np.mean(oos)),
                       mean_OOS_MaxDD=float(np.mean(dd)),
                       d_vs_argmax_OOS=float(np.mean(oos) - w.OOS_pick.mean()),
                       d_vs_argmax_DD_pp=100 * float(np.mean(np.abs(w.OOS_MaxDD_pick)) - np.mean(np.abs(dd)))))
    ab.append(dict(threshold=0.0, abstained=0, mean_OOS=float(w.OOS_pick.mean()),
                   mean_OOS_MaxDD=float(w.OOS_MaxDD_pick.mean()), d_vs_argmax_OOS=0.0,
                   d_vs_argmax_DD_pp=0.0))
    print(pd.DataFrame(ab).sort_values("threshold").to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n  KEEP paths over the live grid:")
    print(f"    4a {int(d.pass4a.sum())}/{len(d)}    4b {int(d.pass4b.sum())}/{len(d)}")
    print(d.groupby("bps").agg(n=("pass4b", "size"), p4b=("pass4b", "sum"), p4a=("pass4a", "sum")).to_string())
    if d.pass4b.any():
        print("\n    4b passes by panel x dial:")
        print(d[d.pass4b].groupby(["panel", "dial"]).size().to_string())
        print("\n    top 4b passes by OOS Sharpe:")
        print(d[d.pass4b].sort_values("OOS_Sharpe", ascending=False).head(6)[
            ["panel", "dial", "arm", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
             "OOS_CAGR", "OOS_MaxDD", "turn"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n    first failing 4b bar:")
    print(d.fail4b.replace("", "PASS").str.split(",").str[0].value_counts().to_string())
    return d, w


def gates(w, d):
    print("\n" + "=" * 118)
    print("REPRODUCTION GATES")
    print("=" * 118)
    px = load_universe(); start = px.index[WARMUP]
    for n, pub in ((3, (0.219, 1.04, -0.258)), (5, (0.165, 0.95, -0.216))):
        r = backtest(px, topn(px, "U56", n), cost_bps=10, freq=FREQ)["returns"].loc[start:]
        m = metrics(r)
        ok = abs(m["CAGR"] - pub[0]) < 0.005 and abs(m["Sharpe"] - pub[1]) < 0.02 and abs(m["MaxDD"] - pub[2]) < 0.005
        print(f"GATE 1  idea 40/41 U56 TOP{n} @10bps {m['CAGR']:.1%}/{m['Sharpe']:.2f}/{m['MaxDD']:.1%} "
              f"vs published {pub[0]:.1%}/{pub[1]:.2f}/{pub[2]:.1%} -> {'PASS' if ok else 'FAIL'}")
    r = backtest(px, rules_v2_weights(px, band=BAND, gross=GROSS), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    m = metrics(r)
    ok = abs(m["CAGR"] - 0.0866) < 0.002 and abs(m["Sharpe"] - 1.2056) < 0.01
    print(f"GATE 2  live RULES v2 U56 @10bps {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} "
          f"vs published 8.66%/1.2056/-12.05% -> {'PASS' if ok else 'FAIL'}")
    g = w[(w.panel == "U56") & (w.dial == "GROSS")]
    print(f"GATE 3  idea 371's own object (the GROSS dial): S1 = "
          + " / ".join(f"{x:.4f}" for x in g.sort_values('bps').S1)
          + f" at 0/10/25 bps   (idea 371 reported an IS spread of 0.001-0.005)")
    gg = d[(d.panel == "U56") & (d.dial == "GROSS") & (d.bps == 10)].sort_values("arm")
    print(f"        rho(IS rank, OOS rank) on that dial = "
          f"{spearman(gg.IS_Sharpe, gg.OOS_Sharpe):+.3f}  (idea 371: -1.00, 6/6);"
          f" OOS MaxDD range {gg.OOS_MaxDD.min():.3f}..{gg.OOS_MaxDD.max():.3f}"
          f" = {abs(gg.OOS_MaxDD.min()/gg.OOS_MaxDD.max()):.1f}x  (idea 371: 4.8x)")


def main():
    print("=" * 118)
    print("IDEA 373 - does the IS-SPREAD screen retire the record's rho-based chooser verdicts?")
    print("  S1 = IS_Sharpe(top1) - IS_Sharpe(top2).  0 tuned parameters; thresholds are a ladder.")
    print("=" * 118)
    corpus()
    d, w = live()
    gates(w, d)
    print(f"\nwrote {OUT}.corpus_stratified.csv, .corpus_filelevel.csv, .live.csv, .rule8.csv")


if __name__ == "__main__":
    main()
