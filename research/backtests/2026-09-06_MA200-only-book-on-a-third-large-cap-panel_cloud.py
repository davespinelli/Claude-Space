#!/usr/bin/env python3
"""Idea 287 - "does-the-MA200-only-book-pass-4b-on-a-THIRD-large-cap-panel".

The question
------------
Idea 56's by-product book -- MA200-only eligibility, top-20 equal-weighted at 75% gross,
weekly, no vol scaler -- passes PROTOCOL path 4b on universe.json (U56) with
14.4% CAGR / 1.158 Sharpe / -19.1% MaxDD (OOS Sharpe 1.181) and FAILS on
universe_broad.json (B136) on the drawdown cap ALONE (-24.00% against the -20.23% bar
= 60% of SPY's MaxDD).  One pass and one fail is not a result: it is a coin with two
sides.  This run asks where in PANEL SPACE the 4b drawdown cap actually binds, by
adding fixed third/fourth panels and, more importantly, a null distribution of random
same-size panels drawn from the same 135-name pool.

  U56    research/universe.json          55 tradable names  (where the pass was found)
  B136   research/universe_broad.json   135 tradable names  (where it failed)
  B100   the 100 names of B136 with the longest price history, ties alphabetical
         -- a deterministic "BSTK100" stand-in.  NOT a capitalisation ranking: this
         repo has no cap column for B136, so B100 is a HISTORY-length panel and is
         labelled as such everywhere below.
  BXU80  B136 \\ U56, the 80 names U56 does not contain -- the complement panel, which
         asks whether the extra drawdown lives in the names B136 ADDS.
  DRAW56 300 random 55-name draws from B136's 135 names (seeded, reproducible)
  DRAW100 200 random 100-name draws from the same pool

U56's 55 tradable names are a strict SUBSET of B136's 135 (verified in-script), so the
draws are a proper null for U56: "is -19.1% a property of THESE 55 names, or is it what
a random 55-name large-cap panel does?"

SPY is the same series on every panel (joined from data/prices.csv, never tradable) and
every panel shares the same trading-day index, so the two 4b LEVEL bars -- MaxDD >= 60%
of SPY's and CAGR >= 70% of SPY's -- are IDENTICAL constants across all panels.  That is
what makes the panel comparison clean.

Construction (idea 56's by-product, held fixed)
    composite score of research/scan.py with NO vol scaler; eligibility = px > 200d MA
    only; top n equal-weighted at gross/n each (de-gross convention: gated-out weight
    goes to CASH, never re-spread); weekly rebalance; 10 bps per unit turnover; weights
    decided at close t and applied at t+1 (engine does this).  First 260 rows dropped as
    warm-up on every panel, exactly as baseline.compare does.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n     in {10, 20, 30}
    2. gross in {0.50, 0.75, 1.00}
ALL 9 grid points are reported on every fixed panel.  CAVEAT stated up front, not
discovered later: gross is very close to a Sharpe-NEUTRAL level dial (cost is
proportional to gross, cash earns 0), so a 4b pass bought by lowering gross is the
"de-gross null" idea 288 already priced -- it is a fact about the BAR, not the book.
The grid reports it; the verdict does not lean on it.  The anchor is (n=20, gross=0.75),
idea 56's published point, pre-registered.

The random draws are run at the ANCHOR ONLY -- no per-draw selection, so the draw
distribution is a clean null and not a max-over-grid.

Rule 8 walk-forward: choose (n, gross) on <= 2016 by in-sample Sharpe INSIDE each fixed
panel, then read 2017-2026 once.  Reported against SPY, RULES v2 (live), the anchor and
the best OOS cell (regret).  For the draws, OOS is read at the anchor on every draw.

Both KEEP paths are evaluated on every cell and every draw:
    4a  Sharpe > RULES v2 in BOTH halves and MaxDD no worse than RULES v2
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD >= 60% of SPY's, CAGR >= 70% of SPY's

Survivorship: universe_broad.json is a list of CURRENT large-cap constituents, so every
panel here (U56, B136, B100, BXU80 and every draw) inherits that bias.  Absolute levels
are optimistic; the panel-to-panel CONTRAST, which is what this run is about, is not
protected by that but is at least measured on one common pool.

Outputs: .grid.csv, .draws.csv, .walkforward.csv, .console.txt, .result.md
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

COST, FREQ = 10, "W"
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [10, 20, 30]
GROSSES = [0.50, 0.75, 1.00]
ANCHOR = (20, 0.75)
N_DRAW56, N_DRAW100 = 300, 200
SEED = 287


# ---------------------------------------------------------------- books
def ma200_book(n, gross):
    """MA200-only eligibility, top-n equal weight at gross/n, de-gross to cash."""
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        sub = px[tr]
        s, _, _ = score(sub, vol_scale=False)
        elig = s.where(sub > sub.rolling(200).mean())
        sel = elig.rank(axis=1, ascending=False) <= n
        w = sel.astype(float) * (gross / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


def v2_book(px):
    tr = [c for c in px.columns if c != "SPY"]
    return rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)


def v1_book(px):
    tr = [c for c in px.columns if c != "SPY"]
    return rules_v1_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)


# ---------------------------------------------------------------- metrics
def run(px, wfn):
    res = backtest(px, wfn(px), cost_bps=COST, freq=FREQ)
    return res["returns"].iloc[WARMUP:]


def row_of(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"], IS_Sharpe=mi["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def keep_paths(x, spy, v2):
    a = (x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])
    b = (x["H1"] > spy["H1"] and x["H2"] > spy["H2"] and x["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and x["MaxDD"] >= 0.60 * spy["MaxDD"] and x["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def first_failing_4b(x, spy):
    for lbl, ok in (("H1", x["H1"] > spy["H1"]),
                    ("H2", x["H2"] > spy["H2"]),
                    ("OOS", x["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                    ("DD", x["MaxDD"] >= 0.60 * spy["MaxDD"]),
                    ("CAGR", x["CAGR"] >= 0.70 * spy["CAGR"])):
        if not ok:
            return lbl
    return "-"


def n_failing_4b(x, spy):
    return sum(0 if ok else 1 for ok in (
        x["H1"] > spy["H1"], x["H2"] > spy["H2"], x["OOS_Sharpe"] > spy["OOS_Sharpe"],
        x["MaxDD"] >= 0.60 * spy["MaxDD"], x["CAGR"] >= 0.70 * spy["CAGR"]))


# ---------------------------------------------------------------- panels
px_u = load_universe()
px_b = load_universe(broad=True)
U_T = [c for c in px_u.columns if c != "SPY"]
B_T = [c for c in px_b.columns if c != "SPY"]

P("=" * 100)
P("Idea 287 - does the MA200-only book pass 4b on a THIRD large-cap panel?")
P("=" * 100)
P(f"U56  tradable names: {len(U_T)}   B136 tradable names: {len(B_T)}")
P(f"U56 subset of B136: {set(U_T) <= set(B_T)}   |U56 \\ B136| = {len(set(U_T) - set(B_T))}")
P(f"index identical: {px_u.index.equals(px_b.index)}   sample "
  f"{px_b.index[WARMUP].date()} .. {px_b.index[-1].date()} after {WARMUP}-row warm-up")

cov = px_b[B_T].notna().sum().sort_values(ascending=False)
order = sorted(B_T, key=lambda t: (-cov[t], t))
B100_T = sorted(order[:100])
BXU_T = sorted(set(B_T) - set(U_T))
P(f"B100 = 100 longest-history names of B136 (min coverage {cov[B100_T].min()}/{len(px_b)}), "
  f"overlap with U56 = {len(set(B100_T) & set(U_T))}")
P(f"BXU80 = B136 \\ U56 = {len(BXU_T)} names")

PANELS = {
    "U56":   px_u,
    "B136":  px_b,
    "B100":  px_b[B100_T + ["SPY"]],
    "BXU80": px_b[BXU_T + ["SPY"]],
}

# SPY and the live baseline (SPY identical on every panel; v2 is panel-dependent)
spy_r = px_b["SPY"].pct_change().fillna(0.0).iloc[WARMUP:]
SPY = row_of(spy_r)
P("")
P(f"SPY (common sample): CAGR {SPY['CAGR']:.2%}  Sharpe {SPY['Sharpe']:.4f}  "
  f"MaxDD {SPY['MaxDD']:.2%}  H1 {SPY['H1']:.4f}  H2 {SPY['H2']:.4f}  OOS Sharpe {SPY['OOS_Sharpe']:.4f}")
P(f"4b LEVEL bars (identical on every panel): MaxDD >= {0.60 * SPY['MaxDD']:.2%}   "
  f"CAGR >= {0.70 * SPY['CAGR']:.2%}")

V2 = {}
for pname, px in PANELS.items():
    V2[pname] = row_of(run(px, v2_book))
    v1 = row_of(run(px, v1_book))
    P(f"  RULES v2 on {pname:6s}: CAGR {V2[pname]['CAGR']:6.2%} Sharpe {V2[pname]['Sharpe']:.4f} "
      f"MaxDD {V2[pname]['MaxDD']:7.2%} H1/H2 {V2[pname]['H1']:.3f}/{V2[pname]['H2']:.3f}   "
      f"| RULES v1 Sharpe {v1['Sharpe']:.4f} MaxDD {v1['MaxDD']:7.2%}")

# ---------------------------------------------------------------- 1. full grid, fixed panels
P("")
P("-" * 100)
P("1. FULL GRID - MA200-only book, all 9 (n, gross) points on each of 4 fixed panels")
P("-" * 100)
grid = []
for pname, px in PANELS.items():
    for n in NS:
        for g in GROSSES:
            r = run(px, ma200_book(n, g))
            x = row_of(r)
            a, b = keep_paths(x, SPY, V2[pname])
            grid.append(dict(panel=pname, n=n, gross=g, anchor=((n, g) == ANCHOR),
                             **{k: round(float(v), 6) for k, v in x.items()},
                             keep4a=a, keep4b=b, first_fail_4b=first_failing_4b(x, SPY)))
G = pd.DataFrame(grid)
G.to_csv(f"{OUT}.grid.csv", index=False)

for pname in PANELS:
    P(f"\n  panel {pname}")
    P(f"  {'n':>3} {'gross':>6} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} "
      f"{'OOSShrp':>8} {'OOSDD':>8} | 4a  4b  firstfail")
    for _, q in G[G.panel == pname].iterrows():
        star = " *" if q["anchor"] else "  "
        P(f"  {int(q['n']):>3} {q['gross']:>6.2f} | {q['CAGR']:>7.2%} {q['Sharpe']:>7.4f} "
          f"{q['MaxDD']:>8.2%} {q['H1']:>6.3f} {q['H2']:>6.3f} {q['OOS_Sharpe']:>8.4f} "
          f"{q['OOS_MaxDD']:>8.2%} | {str(q['keep4a']):>5} {str(q['keep4b']):>5} "
          f"{q['first_fail_4b']:>4}{star}")

P("")
P("  ANCHOR (n=20, gross=0.75) across the four fixed panels:")
A = G[G.anchor]
for _, q in A.iterrows():
    P(f"    {q['panel']:6s} CAGR {q['CAGR']:6.2%}  Sharpe {q['Sharpe']:.4f}  MaxDD {q['MaxDD']:7.2%}  "
      f"H1/H2 {q['H1']:.3f}/{q['H2']:.3f}  OOS {q['OOS_Sharpe']:.4f}  "
      f"4a {q['keep4a']}  4b {q['keep4b']}  first-fail {q['first_fail_4b']}")

P("")
P("  Sharpe-neutrality of the gross dial (max |dSharpe| across gross at fixed n, per panel):")
for pname in PANELS:
    sub = G[G.panel == pname]
    dd = [sub[sub.n == n]["Sharpe"].max() - sub[sub.n == n]["Sharpe"].min() for n in NS]
    P(f"    {pname:6s} {max(dd):.4f}   (MaxDD range at n=20: "
      f"{sub[sub.n == 20]['MaxDD'].min():.2%} .. {sub[sub.n == 20]['MaxDD'].max():.2%})")

# ---------------------------------------------------------------- 2. rule-8 walk-forward
P("")
P("-" * 100)
P("2. RULE 8 WALK-FORWARD - (n, gross) chosen on <=2016 by IS Sharpe inside each panel, "
  "2017-2026 read once")
P("-" * 100)
spy_oos = SPY["OOS_Sharpe"]
wf = []
for pname in PANELS:
    sub = G[G.panel == pname].reset_index(drop=True)
    pick = sub.loc[sub["IS_Sharpe"].idxmax()]
    best = sub.loc[sub["OOS_Sharpe"].idxmax()]
    anch = sub[sub.anchor].iloc[0]
    wf.append(dict(panel=pname, pick_n=int(pick["n"]), pick_gross=float(pick["gross"]),
                   IS_Sharpe=round(float(pick["IS_Sharpe"]), 4),
                   OOS_CAGR=round(float(pick["OOS_CAGR"]), 6),
                   OOS_Sharpe=round(float(pick["OOS_Sharpe"]), 4),
                   OOS_MaxDD=round(float(pick["OOS_MaxDD"]), 6),
                   anchor_OOS_Sharpe=round(float(anch["OOS_Sharpe"]), 4),
                   best_OOS_Sharpe=round(float(best["OOS_Sharpe"]), 4),
                   regret=round(float(pick["OOS_Sharpe"] - best["OOS_Sharpe"]), 4),
                   spy_OOS_Sharpe=round(float(spy_oos), 4),
                   v2_OOS_Sharpe=round(float(V2[pname]["OOS_Sharpe"]), 4),
                   beats_spy_OOS=bool(pick["OOS_Sharpe"] > spy_oos),
                   beats_v2_OOS=bool(pick["OOS_Sharpe"] > V2[pname]["OOS_Sharpe"])))
W = pd.DataFrame(wf)
W.to_csv(f"{OUT}.walkforward.csv", index=False)
P(W.to_string(index=False))
P(f"  SPY OOS: CAGR {SPY['OOS_CAGR']:.2%}  Sharpe {SPY['OOS_Sharpe']:.4f}  MaxDD {SPY['OOS_MaxDD']:.2%}")

# ---------------------------------------------------------------- 3. the null: random panels
P("")
P("-" * 100)
P(f"3. RANDOM PANEL NULL - anchor book (n=20, gross=0.75) on {N_DRAW56} random 55-name and "
  f"{N_DRAW100} random 100-name draws from B136's 135 names (seed {SEED})")
P("-" * 100)
rng = np.random.default_rng(SEED)
draws = []
for k, ndraw in ((len(U_T), N_DRAW56), (100, N_DRAW100)):
    for i in range(ndraw):
        cols = sorted(rng.choice(B_T, size=k, replace=False).tolist())
        sub = px_b[cols + ["SPY"]]
        x = row_of(run(sub, ma200_book(*ANCHOR)))
        a4, b4 = keep_paths(x, SPY, V2["B136"])   # 4a vs the B136 live book (same pool)
        draws.append(dict(k=k, draw=i, n_in_U56=len(set(cols) & set(U_T)),
                          **{kk: round(float(v), 6) for kk, v in x.items()},
                          keep4b=b4, first_fail_4b=first_failing_4b(x, SPY),
                          n_fail_4b=n_failing_4b(x, SPY)))
    P(f"  ... k={k}: {ndraw} draws done")
D = pd.DataFrame(draws)
D.to_csv(f"{OUT}.draws.csv", index=False)


def pct_rank(series, value):
    return float((series < value).mean())


for k in sorted(D.k.unique()):
    d = D[D.k == k]
    P(f"\n  k={k}  ({len(d)} draws)")
    for col, fmt in (("MaxDD", "{:.2%}"), ("CAGR", "{:.2%}"), ("Sharpe", "{:.4f}"),
                     ("OOS_Sharpe", "{:.4f}")):
        qs = d[col].quantile([0.05, 0.25, 0.50, 0.75, 0.95])
        P(f"    {col:10s} p05 {fmt.format(qs[0.05])}  p25 {fmt.format(qs[0.25])}  "
          f"med {fmt.format(qs[0.50])}  p75 {fmt.format(qs[0.75])}  p95 {fmt.format(qs[0.95])}")
    P(f"    4b pass rate: {d.keep4b.mean():.1%}  ({int(d.keep4b.sum())}/{len(d)})")
    ff = d[~d.keep4b].first_fail_4b.value_counts()
    P(f"    first-failing bar among failures: {dict(ff)}")
    dd_bind = (d["MaxDD"] < 0.60 * SPY["MaxDD"]).mean()
    cg_bind = (d["CAGR"] < 0.70 * SPY["CAGR"]).mean()
    P(f"    DD cap alone fails {dd_bind:.1%} of draws; CAGR floor alone fails {cg_bind:.1%}; "
      f"H1 {(d['H1'] <= SPY['H1']).mean():.1%}; H2 {(d['H2'] <= SPY['H2']).mean():.1%}; "
      f"OOS {(d['OOS_Sharpe'] <= SPY['OOS_Sharpe']).mean():.1%}")

d56 = D[D.k == len(U_T)]
u56 = A[A.panel == "U56"].iloc[0]
b136 = A[A.panel == "B136"].iloc[0]
P("")
P("  WHERE U56 SITS IN ITS OWN NULL (k=55 draws from the same pool):")
for col, fmt in (("MaxDD", "{:.2%}"), ("CAGR", "{:.2%}"), ("Sharpe", "{:.4f}"),
                 ("OOS_Sharpe", "{:.4f}")):
    P(f"    {col:10s} U56 {fmt.format(u56[col])}  -> percentile {pct_rank(d56[col], u56[col]):.1%} "
      f"of the draw distribution")
P(f"    draws whose MaxDD is BETTER (shallower) than U56's: {(d56['MaxDD'] > u56['MaxDD']).mean():.1%}")
P(f"    B136 (the full pool, not a draw) MaxDD {b136['MaxDD']:.2%} sits at percentile "
  f"{pct_rank(d56['MaxDD'], b136['MaxDD']):.1%} of the k=55 draws")

# does panel overlap with U56 explain the drawdown?
c = np.corrcoef(d56["n_in_U56"], d56["MaxDD"])[0, 1]
c2 = np.corrcoef(D[D.k == 100]["n_in_U56"], D[D.k == 100]["MaxDD"])[0, 1]
P(f"    corr(number of U56 names in the draw, MaxDD): k=55 {c:+.3f}   k=100 {c2:+.3f}   "
  f"(positive = more U56 names -> shallower drawdown)")

# ---------------------------------------------------------------- 4. verdict
P("")
P("-" * 100)
P("4. VERDICT")
P("-" * 100)
n4a = int(G.keep4a.sum()); n4b = int(G.keep4b.sum())
P(f"  fixed panels: 4a {n4a}/{len(G)}   4b {n4b}/{len(G)}")
for pname in PANELS:
    sub = G[G.panel == pname]
    P(f"    {pname:6s} 4b {int(sub.keep4b.sum())}/{len(sub)}  "
      f"(anchor {bool(sub[sub.anchor].iloc[0]['keep4b'])}); "
      f"first-fail counts {dict(sub[~sub.keep4b].first_fail_4b.value_counts())}")
anchor_pass = {p: bool(A[A.panel == p].iloc[0]["keep4b"]) for p in PANELS}
P(f"  anchor 4b by panel: {anchor_pass}")
P(f"  anchor 4b pass rate over random same-size panels: k=55 {d56.keep4b.mean():.1%}, "
  f"k=100 {D[D.k == 100].keep4b.mean():.1%}")

Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
P(f"\nwrote {OUT.name}.grid.csv, .draws.csv, .walkforward.csv, .console.txt")
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
