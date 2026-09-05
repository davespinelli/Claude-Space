#!/usr/bin/env python3
"""Idea 209 — is-the-book-size-floor-a-corpus-wide-clause  (lane C, 2026-09-05)

Idea 199 found that a bare pre-registered floor `n >= 25` beats idea 178's IS-window 4b
screen (+0.1297 vs +0.0287 paired OOS Sharpe, 11W/0L), and located the whole mechanism in a
within-cell Spearman rho(n, OOS Sharpe) = +0.489 mean, which REVERSES on the sub-$2B panel
(-0.482 / -0.283).  A floor that only works on large caps is a universe clause, not a
PROTOCOL one.  This run answers that in two independent ways:

  PART A — ARCHIVE CENSUS.  Every committed grid CSV in research/backtests/ that publishes
  both a book-size column `n` and an out-of-sample Sharpe column is re-read, split into
  cells by its own context columns, and rho(n, OOS Sharpe) is computed within each.  All
  cells reported; the sign is tabulated by panel class.  This is the queue's literal ask.

  PART B — A FRESH CORPUS WITH EXOGENOUS n.  The archive's n is almost always DERIVED (a
  share m of the eligible pool), so its correlation with anything is confounded with m.
  Here n is the swept axis itself: top-n equal weight among RULES-v1-eligible names, six
  ranking keys, three panels, two cost rungs, g = 0.75, weekly, t+1.  rho(n, OOS Sharpe) is
  then a clean read, and the rule-8 floor selector is re-priced on a corpus idea 199 never
  saw.

Tuned parameters: ONE — the floor k in {5,10,15,20,25,30}.  Every grid point reported.
Deterministic (fixed integer seed, no hash()-derived seeds; PROTOCOL 5).
Outputs: .census.csv .corpus.csv .cellrho.csv .walkforward.csv .console.txt .result.md
"""
from __future__ import annotations
import sys, os, csv, glob, json, math, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa
from engine import backtest, metrics                          # noqa

HERE = Path(__file__).resolve().parent
STEM = HERE / Path(__file__).stem
SEED = 20260905                     # explicit integer; never hash()
IS_END = "2016-12-31"               # PROTOCOL rule 8
OOS_START = "2017-01-01"
GROSS = 0.75                        # pre-registered (ideas 2 / 178), not tuned here
FLOORS = [5, 10, 15, 20, 25, 30]    # the one tuned parameter
N_GRID = [2, 3, 5, 8, 10, 15, 20, 25, 30, 40, 60]
COSTS = [10.0, 25.0]
ARMS = ["COMP", "NOVOL", "MOM", "R6", "INVVOL", "RND"]

_LOG = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)

# ------------------------------------------------------------------ PART A helpers

CONTEXT_VOCAB = {  # columns that define a CELL (a distinct backtest context)
    "corpus", "panel", "universe", "cost", "cost_bps", "cost_rung", "costbps",
    "scaler", "gate", "floor_musd", "gross_conv", "conv", "freq", "lag", "g",
    "kind", "mode", "book", "family", "signal", "ceil", "levered",
}
EXCLUDE_AS_X = {"n"}
SMALL_TOKENS = {"small", "small439", "small485", "sub2b", "smallcap"}
LARGE_TOKENS = {"u56", "broad", "etf36", "large", "u56b", "universe", "v1u", "default"}

def _panel_class(vals):
    """LARGE / SMALL / MIXED / UNKNOWN from a cell's context values."""
    toks = {str(v).strip().lower() for v in vals}
    s = any(t in SMALL_TOKENS or "small" in t for t in toks)
    l = any(t in LARGE_TOKENS or t in ("u56", "broad") for t in toks)
    if s and not l: return "SMALL"
    if l and not s: return "LARGE"
    if s and l: return "MIXED"
    return "UNKNOWN"

def _spearman(a, b):
    a = pd.Series(a).astype(float); b = pd.Series(b).astype(float)
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if len(a) < 4 or a.nunique() < 2 or b.nunique() < 2: return np.nan, len(a)
    return float(a.rank().corr(b.rank())), len(a)

def part_a():
    say("\n" + "=" * 96)
    say("PART A — ARCHIVE CENSUS: rho(n, OOS Sharpe) within every cell of every surviving grid CSV")
    say("=" * 96)
    files = sorted(glob.glob(str(HERE / "*.csv")))
    me = str(STEM)
    rows, skipped = [], []
    for f in files:
        if f.startswith(me):  # never read my own outputs
            continue
        try:
            d = pd.read_csv(f)
        except Exception as e:
            skipped.append((os.path.basename(f), f"unreadable:{type(e).__name__}")); continue
        cols = list(d.columns)
        ncol = next((c for c in cols if c.strip().lower() == "n"), None)
        if ncol is None:
            skipped.append((os.path.basename(f), "no n column")); continue
        ycols = [c for c in cols if "oos" in c.lower() and "sharpe" in c.lower()
                 and not any(t in c.lower() for t in ("spy", "v1", "base", "spread", "d"))]
        # keep the plain own-book OOS Sharpe: prefer exact names
        pref = [c for c in ycols if c.strip().lower() in
                ("oos_sharpe", "sharpe_oos", "mean_oos_sharpe", "oossharpe_10", "oossharpe_25")]
        ycols = pref or ycols
        if not ycols:
            skipped.append((os.path.basename(f), "no own OOS Sharpe column")); continue
        # n must look like a book size
        nv = pd.to_numeric(d[ncol], errors="coerce")
        if nv.notna().sum() < 8 or nv.nunique() < 3 or nv.max() > 1000 or nv.min() < 1:
            skipped.append((os.path.basename(f), f"n not book-size-like (uniq={nv.nunique()}, max={nv.max()})"))
            continue
        ctx = [c for c in cols if c.strip().lower() in CONTEXT_VOCAB and c != ncol
               and d[c].nunique(dropna=False) > 1 and d[c].nunique(dropna=False) <= 24]
        for ycol in ycols:
            yv = pd.to_numeric(d[ycol], errors="coerce")
            if yv.notna().sum() < 8: continue
            sub = pd.DataFrame({"n": nv, "y": yv})
            if ctx:
                for c in ctx: sub[c] = d[c].astype(str)
                groups = sub.groupby(ctx, dropna=False)
            else:
                sub["_all"] = "ALL"; groups = sub.groupby(["_all"])
            for key, g in groups:
                key = key if isinstance(key, tuple) else (key,)
                rho, m = _spearman(g["n"], g["y"])
                if np.isnan(rho) or g["n"].nunique() < 3 or m < 8: continue
                cellname = "/".join(f"{c}={v}" for c, v in zip(ctx or ["cell"], key))
                rows.append(dict(file=os.path.basename(f), ycol=ycol, cell=cellname,
                                 panel_class=_panel_class(key), rows=m,
                                 distinct_n=int(g["n"].nunique()), n_min=int(g["n"].min()),
                                 n_max=int(g["n"].max()), rho=rho))
    cen = pd.DataFrame(rows)
    cen.to_csv(f"{STEM}.census.csv", index=False)
    say(f"grid CSVs scanned: {len(files)-0}; usable: {cen['file'].nunique() if len(cen) else 0}; "
        f"cells with rho: {len(cen)}")
    say(f"skipped: {len(skipped)} (reasons: " +
        ", ".join(f"{r}×{sum(1 for _,x in skipped if x.split('(')[0].strip()==r.split('(')[0].strip())}"
                  for r in sorted({x for _, x in skipped})[:6]) + " ...)")
    if not len(cen):
        say("NO usable cells — census empty."); return cen
    say("\n-- rho(n, OOS Sharpe) by panel class (every cell counted once) --")
    tbl = cen.groupby("panel_class").agg(cells=("rho", "size"), mean_rho=("rho", "mean"),
                                         median_rho=("rho", "median"),
                                         pos=("rho", lambda s: int((s > 0).sum())),
                                         neg=("rho", lambda s: int((s < 0).sum())))
    tbl["share_pos"] = tbl["pos"] / tbl["cells"]
    say(tbl.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n-- every cell, sorted by rho (all reported) --")
    for _, r in cen.sort_values("rho").iterrows():
        say(f"  {r['rho']:+.3f}  [{r['panel_class']:7s}] rows={r['rows']:4d} nuniq={r['distinct_n']:2d} "
            f"n∈[{r['n_min']},{r['n_max']}]  {r['file']}::{r['ycol']}  {r['cell'][:64]}")
    lg = cen[cen.panel_class == "LARGE"]["rho"]; sm = cen[cen.panel_class == "SMALL"]["rho"]
    if len(lg) and len(sm):
        say(f"\nLARGE mean {lg.mean():+.4f} (n={len(lg)}, {100*(lg>0).mean():.1f}% positive)   "
            f"SMALL mean {sm.mean():+.4f} (n={len(sm)}, {100*(sm>0).mean():.1f}% positive)")
        # Welch t on cell-level rhos (cells are NOT independent; reported as descriptive only)
        t = (lg.mean() - sm.mean()) / math.sqrt(lg.var(ddof=1)/len(lg) + sm.var(ddof=1)/len(sm))
        say(f"descriptive Welch t(LARGE-SMALL) = {t:+.2f}  (cells share panels/scripts; NOT a p-value)")
    return cen

# ------------------------------------------------------------------ PART B: fresh corpus

def keys_for(px):
    """Six price-only ranking keys + the RULES v1 eligibility mask, all on one panel."""
    comp_s, above, vol20 = score(px, vol_scale=True)
    novol_s, _, _ = score(px, vol_scale=False)
    mom = (px.shift(21) / px.shift(252) - 1).rank(axis=1, pct=True)
    r6 = (px / px.shift(126) - 1).rank(axis=1, pct=True)
    inv = (1.0 / vol20.clip(lower=0.08)).rank(axis=1, pct=True)
    rng = np.random.default_rng(SEED)
    rnd = pd.DataFrame(rng.random(px.shape), index=px.index, columns=px.columns)
    rnd = rnd.rank(axis=1, pct=True)
    elig = above & (vol20 < 0.60)
    return {"COMP": comp_s, "NOVOL": novol_s, "MOM": mom, "R6": r6, "INVVOL": inv, "RND": rnd}, elig

def topn_weights(key, elig, n, g=GROSS):
    s = key.where(elig)
    rank = s.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)

def win_metrics(r, prefix=""):
    m = metrics(r)
    return {prefix + "CAGR": m["CAGR"], prefix + "Sharpe": m["Sharpe"], prefix + "MaxDD": m["MaxDD"]}

def full_row(r):
    h = len(r) // 2
    out = win_metrics(r)
    out["H1"] = metrics(r.iloc[:h])["Sharpe"]; out["H2"] = metrics(r.iloc[h:])["Sharpe"]
    isr, oos = r.loc[:IS_END], r.loc[OOS_START:]
    out.update(win_metrics(isr, "IS_")); out.update(win_metrics(oos, "OOS_"))
    return out

def run_panel(panel):
    kw = {"u56": {}, "broad": {"broad": True}, "small": {"small": True}}[panel]
    px = load_universe(**kw)
    keys, elig = keys_for(px)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base_bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
    breadth = int(elig.sum(axis=1).median())
    out = []
    for arm in ARMS:
        for n in N_GRID:
            if n > min(px.shape[1] - 1, 60): continue
            bt = backtest(px, topn_weights(keys[arm], elig, n), cost_bps=0.0, freq="W")
            gross_r, turn = bt["returns"].loc[start:], bt["turnover"].loc[start:]
            realised_n = float((topn_weights(keys[arm], elig, n).loc[start:] > 0).sum(axis=1)
                               .replace(0, np.nan).mean())
            for c in COSTS:
                r = gross_r - turn * c / 1e4
                row = dict(panel=panel, cost=c, arm=arm, n=n, n_realised=realised_n,
                           g=GROSS, breadth=breadth, turnover_yr=float(turn.sum() / (len(turn) / 252)))
                row.update(full_row(r))
                out.append(row)
    # benchmarks per (panel, cost)
    bench = {}
    for c in COSTS:
        b = base_bt["returns"].loc[start:] - base_bt["turnover"].loc[start:] * c / 1e4
        bench[c] = dict(v1=full_row(b), spy=full_row(spy))
    return out, bench, breadth

def bars_4a(row, v1):
    return (row["H1"] > v1["H1"] and row["H2"] > v1["H2"] and row["MaxDD"] >= v1["MaxDD"])

def bars_4b(row, spy, oos=False):
    """PROTOCOL 4b. oos=True reads the OOS window's own bars (the rule-8 read)."""
    fails = []
    if oos:
        if row["OOS_Sharpe"] <= spy["OOS_Sharpe"]: fails.append("OOS")
        if row["OOS_MaxDD"] < 0.60 * spy["OOS_MaxDD"]: fails.append("DD")
        if row["OOS_CAGR"] < 0.70 * spy["OOS_CAGR"]: fails.append("CAGR")
    else:
        if row["H1"] <= spy["H1"]: fails.append("H1")
        if row["H2"] <= spy["H2"]: fails.append("H2")
        if row["OOS_Sharpe"] <= spy["OOS_Sharpe"]: fails.append("OOS")
        if row["MaxDD"] < 0.60 * spy["MaxDD"]: fails.append("DD")
        if row["CAGR"] < 0.70 * spy["CAGR"]: fails.append("CAGR")
    return (len(fails) == 0), "|".join(fails)

def part_b():
    say("\n" + "=" * 96)
    say("PART B — FRESH CORPUS, n EXOGENOUS: top-n equal weight among RULES-v1-eligible names")
    say(f"  arms={ARMS}  n={N_GRID}  g={GROSS}  weekly, t+1, costs={COSTS} bps")
    say(f"  rule 8: IS <= {IS_END}, OOS >= {OOS_START}; floors k={FLOORS} (the one tuned parameter)")
    say("=" * 96)
    corpus, benches = [], {}
    for panel in ("u56", "broad", "small"):
        t0 = time.time()
        rows, bench, breadth = run_panel(panel)
        corpus += rows; benches[panel] = bench
        say(f"  {panel}: {len(rows)} rows, median eligible breadth {breadth}, {time.time()-t0:.0f}s")
    C = pd.DataFrame(corpus)
    # attach bars
    recs = []
    for _, r in C.iterrows():
        v1, spy = benches[r.panel][r.cost]["v1"], benches[r.panel][r.cost]["spy"]
        p4a = bars_4a(r, v1); p4b, f4b = bars_4b(r, spy); p4bo, f4bo = bars_4b(r, spy, oos=True)
        d = r.to_dict(); d.update(pass4a=p4a, pass4b=p4b, fail4b=f4b,
                                 OOS4b_clears=p4bo, OOS4b_fail=f4bo,
                                 v1_OOS_Sharpe=v1["OOS_Sharpe"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                                 v1_OOS_CAGR=v1["OOS_CAGR"], spy_OOS_CAGR=spy["OOS_CAGR"],
                                 v1_OOS_MaxDD=v1["OOS_MaxDD"], spy_OOS_MaxDD=spy["OOS_MaxDD"])
        recs.append(d)
    C = pd.DataFrame(recs)
    C.to_csv(f"{STEM}.corpus.csv", index=False)
    say(f"\ncorpus: {len(C)} (panel, cost, arm, n) books; "
        f"{int(C.pass4a.sum())} pass 4a, {int(C.pass4b.sum())} pass 4b, "
        f"{int(C.OOS4b_clears.sum())} clear the OOS-window 4b")

    # ---- rho(n, OOS Sharpe) per (panel, cost) cell, pooling arms (idea 199's convention)
    say("\n-- rho(n, ·) within each (panel, cost) cell, arms pooled — idea 199's convention --")
    cr = []
    for (p, c), g in C.groupby(["panel", "cost"]):
        row = dict(panel=p, cost=c, rows=len(g), arms=g.arm.nunique(), distinct_n=g.n.nunique())
        for lab, col in (("OOS_Sharpe", "OOS_Sharpe"), ("OOS_absMaxDD", "OOS_MaxDD"),
                         ("IS_Sharpe", "IS_Sharpe"), ("OOS_CAGR", "OOS_CAGR")):
            y = -g[col] if lab == "OOS_absMaxDD" else g[col]
            row["rho_" + lab] = _spearman(g.n, y)[0]
        cr.append(row)
    CR = pd.DataFrame(cr)
    say(CR.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    # per (panel, cost, arm) — the fine read
    say("\n-- rho(n, OOS Sharpe) per (panel, cost, arm): every arm reported --")
    fine = []
    for (p, c, a), g in C.groupby(["panel", "cost", "arm"]):
        rho, m = _spearman(g.n, g.OOS_Sharpe)
        fine.append(dict(panel=p, cost=c, arm=a, rows=m, rho=rho))
    F = pd.DataFrame(fine)
    piv = F.pivot_table(index=["panel", "cost"], columns="arm", values="rho")
    say(piv.to_string(float_format=lambda x: f"{x:+.3f}"))
    pd.concat([CR.assign(kind="cell"), F.assign(kind="arm")], ignore_index=True) \
      .to_csv(f"{STEM}.cellrho.csv", index=False)
    for p, g in F.groupby("panel"):
        say(f"  {p:6s}: mean rho {g.rho.mean():+.4f}, {int((g.rho>0).sum())}/{len(g)} arm-cells positive")

    # ---- CONFOUND: is it n, or n as a share of the panel's eligible breadth?
    # On u56 the top of the n-ladder (40) IS the whole eligible pool (median breadth 40), while on
    # the small panel n=60 is still a ~39% slice.  If the reversal is really "the large ladders run
    # out of pool and the small one does not", then rho(n/breadth, ·) should equalise the panels.
    say("\n-- CONFOUND CHECK: is the reversal about n, or about how far up its OWN eligible pool")
    say("   each panel's ladder reaches?  On u56 n=40 IS the whole eligible pool (median breadth")
    say("   40); on the small panel n=60 is still a ~39% slice.  Two matched windows. --")
    C["share_of_pool"] = C.n / C.breadth
    conf = []
    for (p, c), g in C.groupby(["panel", "cost"]):
        mn = g[(g.n >= 5) & (g.n <= 40)]                       # matched RAW n window
        ms = g[(g.share_of_pool >= 0.05) & (g.share_of_pool <= 0.40)]   # matched SHARE window
        conf.append(dict(panel=p, cost=c, breadth=int(g.breadth.iloc[0]),
                         max_share=round(float(g.share_of_pool.max()), 3),
                         rho_all=_spearman(g.n, g.OOS_Sharpe)[0],
                         rho_n5_40=_spearman(mn.n, mn.OOS_Sharpe)[0], rows_n5_40=len(mn),
                         n_in_share_win=f"[{int(ms.n.min())},{int(ms.n.max())}]" if len(ms) else "-",
                         rho_share05_40=_spearman(ms.n, ms.OOS_Sharpe)[0], rows_share=len(ms)))
    CF = pd.DataFrame(conf)
    say(CF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    CF.to_csv(f"{STEM}.confound.csv", index=False)

    # ---- rule 8: the floor selector vs the do-nothing IS-Sharpe argmax
    say("\n-- RULE 8 walk-forward: pick on IS (<= 2016) only, read OOS once. Every k reported. --")
    wf = []
    for (p, c), g in C.groupby(["panel", "cost"]):
        v1, spy = benches[p][c]["v1"], benches[p][c]["spy"]
        g = g.reset_index(drop=True)
        s0 = g.loc[g.IS_Sharpe.idxmax()]
        sels = [("S0 do-nothing (IS-Sharpe argmax)", s0, False)]
        for k in FLOORS:
            sub = g[g.n >= k]
            if len(sub) == 0: sels.append((f"FLOOR n>={k}", None, False)); continue
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            sels.append((f"FLOOR n>={k}", pick, bool(s0.n < k)))
        sub = g[g.n == g.n.max()]
        sels.append(("BIGGEST BOOK (no fitting)", sub.loc[sub.IS_Sharpe.idxmax()], True))
        sels.append(("ORACLE-OOS (ceiling)", g.loc[g.OOS_Sharpe.idxmax()], True))
        for name, pick, fired in sels:
            if pick is None: continue
            wf.append(dict(panel=p, cost=c, selector=name, pick=f"{pick.arm}@n={int(pick.n)}",
                           n=int(pick.n), fired=fired, changed=bool(pick.name != s0.name),
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_MaxDD=pick.OOS_MaxDD, dOOS=pick.OOS_Sharpe - s0.OOS_Sharpe,
                           dMaxDD=pick.OOS_MaxDD - s0.OOS_MaxDD,
                           pass4a=bool(pick.pass4a), pass4b=bool(pick.pass4b),
                           OOS4b_clears=bool(pick.OOS4b_clears), OOS4b_fail=pick.OOS4b_fail,
                           full_CAGR=pick.CAGR, full_Sharpe=pick.Sharpe, full_MaxDD=pick.MaxDD,
                           H1=pick.H1, H2=pick.H2, turnover_yr=pick.turnover_yr,
                           v1_OOS_Sharpe=v1["OOS_Sharpe"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                           v1_OOS_CAGR=v1["OOS_CAGR"], spy_OOS_CAGR=spy["OOS_CAGR"],
                           v1_OOS_MaxDD=v1["OOS_MaxDD"], spy_OOS_MaxDD=spy["OOS_MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{STEM}.walkforward.csv", index=False)

    say("\n== ALL CELLS × ALL SELECTORS (every grid point) ==")
    for (p, c), g in W.groupby(["panel", "cost"]):
        say(f"\n  [{p} @ {c:.0f}bps]  SPY OOS {g.spy_OOS_Sharpe.iloc[0]:.4f}/"
            f"{g.spy_OOS_CAGR.iloc[0]:.2%}/{g.spy_OOS_MaxDD.iloc[0]:.2%}   "
            f"RULES v1 OOS {g.v1_OOS_Sharpe.iloc[0]:.4f}/{g.v1_OOS_CAGR.iloc[0]:.2%}/"
            f"{g.v1_OOS_MaxDD.iloc[0]:.2%}")
        for _, r in g.iterrows():
            say(f"    {r.selector:34s} {r['pick']:12s} OOS {r.OOS_Sharpe:6.3f} / {r.OOS_CAGR:7.2%} / "
                f"{r.OOS_MaxDD:7.2%}  dOOS {r.dOOS:+.4f}  4a={int(r.pass4a)} 4b={int(r.pass4b)} "
                f"OOS4b={int(r.OOS4b_clears)}")

    say("\n== PAIRED SUMMARY across all 6 (panel, cost) cells, and by panel class ==")
    s0 = W[W.selector.str.startswith("S0")].set_index(["panel", "cost"])
    lines = []
    for name, g in W.groupby("selector", sort=False):
        gi = g.set_index(["panel", "cost"])
        d = (gi.OOS_Sharpe - s0.OOS_Sharpe).dropna()
        t = d.mean() / (d.std(ddof=1) / math.sqrt(len(d))) if len(d) > 1 and d.std(ddof=1) > 0 else np.nan
        large = d.loc[[i for i in d.index if i[0] != "small"]]
        small = d.loc[[i for i in d.index if i[0] == "small"]]
        lines.append(dict(selector=name, mean_OOS_Sharpe=gi.OOS_Sharpe.mean(),
                          mean_OOS_CAGR=gi.OOS_CAGR.mean(), mean_OOS_MaxDD=gi.OOS_MaxDD.mean(),
                          dOOS=d.mean(), t=t, W=int((d > 1e-12).sum()), L=int((d < -1e-12).sum()),
                          T=int((d.abs() <= 1e-12).sum()), mean_n=gi.n.mean(),
                          dOOS_LARGE=large.mean(), dOOS_SMALL=small.mean(),
                          OOS4b=int(gi.OOS4b_clears.sum()), p4a=int(gi.pass4a.sum()),
                          p4b=int(gi.pass4b.sum())))
    S = pd.DataFrame(lines)
    say(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    S.to_csv(f"{STEM}.summary.csv", index=False)
    return C, CR, F, W, S, benches

if __name__ == "__main__":
    t0 = time.time()
    say(f"# Idea 209 — is-the-book-size-floor-a-corpus-wide-clause (lane C)  seed={SEED}")
    cen = part_a()
    C, CR, F, W, S, benches = part_b()
    say(f"\ntotal runtime {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    print("wrote", f"{STEM}.console.txt")
