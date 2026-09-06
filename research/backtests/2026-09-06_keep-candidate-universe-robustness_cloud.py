#!/usr/bin/env python3
"""Idea 53 - "keep-candidate-universe-robustness".

The question
------------
Idea 2's KEEP candidate -- RULES v1's two-clause gate (px > 200d MA AND vol20 < 0.60),
composite score with NO vol scaler, top n=20 equal-weighted at 75% gross, weekly, 10 bps,
decided at close t and applied at t+1 -- passes PROTOCOL path 4b only on the 56-name list
it was fitted on (it fails universe_broad by ~0.02 and fails the small panel outright).
Parameter robustness was already tested; UNIVERSE COMPOSITION never was.  This run drops
5 and 10 of universe.json's 55 tradable names at random, 200 draws each, and reports the
distribution of 4b outcomes.

Three things are measured, not one:

  A. COMPOSITION   d = 5 and d = 10 names dropped at random from U56 (200 draws each),
                   plus the exhaustive d = 1 leave-one-out (55 draws) which names any
                   single load-bearing name.
  B. SIZE CONTROL  the same book on 200 random 50-name and 200 random 45-name panels
                   drawn from universe_broad.json's 135 names.  This control exists
                   because TODAY'S idea 287 established, on the sibling MA200-only book,
                   that the 4b drawdown cap is a monotone readout of POOL SIZE at fixed
                   n (median MaxDD -19.30% / -21.85% / -24.00% at k = 55 / 100 / 135).
                   Dropping names SHRINKS the pool, which mechanically makes the top-20
                   book less selective and its drawdown shallower -- so a high pass rate
                   at d = 10 could be a size artefact rather than robustness.  Without
                   this control the headline number is uninterpretable.
  C. RULE 8        per draw, n is chosen on <= 2016 by in-sample Sharpe from {10, 20, 30}
                   and 2017-2026 is read once; the OOS distribution is reported against
                   SPY, against RULES v2 (live, recomputed on the same draw) and against
                   the anchor n = 20.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n in {10, 20, 30}       2. d (names dropped) in {0, 1, 5, 10}
All grid points are reported.  The book is otherwise idea 2's published point, unchanged;
gross is held at 0.75 throughout precisely because idea 287 showed it is a Sharpe-neutral
level dial that only moves the two 4b LEVEL bars.

SPY is the same never-tradable series on every draw and the trading-day index is shared,
so the 4b level bars (MaxDD >= 60% of SPY's, CAGR >= 70% of SPY's) are constants.

Survivorship: universe.json is a hand-curated list of names that are large and liquid
TODAY, and universe_broad.json is a list of current constituents.  Every draw here is a
subset of one of those, so every number inherits that bias; absolute levels are
optimistic.  Dropping names at random does NOT simulate delisting -- it re-samples a
survivor list, so this run measures composition sensitivity, not survivorship.

Outputs: .grid.csv, .draws.csv, .loo.csv, .walkforward.csv, .console.txt, .result.md
"""
import sys
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

COST, FREQ, GROSS = 10, "W", 0.75
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [10, 20, 30]
ANCHOR_N = 20
DROPS = [5, 10]
N_DRAWS = 200
SEED = 53


# ---------------------------------------------------------------- book
def rank_of(sub):
    """Idea 2's selection surface for one panel: composite (no vol scaler), RULES v1 gate."""
    s, above, vol20 = score(sub, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    return elig.rank(axis=1, ascending=False)


def weights_from_rank(rank, cols, n):
    w = (rank <= n).astype(float) * (GROSS / n)
    return w.reindex(columns=cols).fillna(0.0)


def run_panel(px, ns=NS):
    """One panel -> {n: returns}. Score/rank computed once and reused across n."""
    tr = [c for c in px.columns if c != "SPY"]
    rank = rank_of(px[tr])
    out = {}
    for n in ns:
        res = backtest(px, weights_from_rank(rank, px.columns, n), cost_bps=COST, freq=FREQ)
        out[n] = res["returns"].iloc[WARMUP:]
    return out


def v2_returns(px):
    tr = [c for c in px.columns if c != "SPY"]
    w = rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)
    return backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].iloc[WARMUP:]


# ---------------------------------------------------------------- metrics
def row_of(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mo, mi = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"],
                OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def keep4b(x, spy):
    return bool(x["H1"] > spy["H1"] and x["H2"] > spy["H2"]
                and x["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and x["MaxDD"] >= 0.60 * spy["MaxDD"]
                and x["CAGR"] >= 0.70 * spy["CAGR"])


def keep4a(x, v2):
    return bool(x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])


def first_fail(x, spy):
    for lbl, ok in (("H1", x["H1"] > spy["H1"]), ("H2", x["H2"] > spy["H2"]),
                    ("OOS", x["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                    ("DD", x["MaxDD"] >= 0.60 * spy["MaxDD"]),
                    ("CAGR", x["CAGR"] >= 0.70 * spy["CAGR"])):
        if not ok:
            return lbl
    return "-"


def margins(x, spy):
    return dict(m_H1=x["H1"] - spy["H1"], m_H2=x["H2"] - spy["H2"],
                m_OOS=x["OOS_Sharpe"] - spy["OOS_Sharpe"],
                m_DD=x["MaxDD"] - 0.60 * spy["MaxDD"],
                m_CAGR=x["CAGR"] - 0.70 * spy["CAGR"])


# ---------------------------------------------------------------- panels
px_u = load_universe()
px_b = load_universe(broad=True)
U_T = sorted([c for c in px_u.columns if c != "SPY"])
B_T = sorted([c for c in px_b.columns if c != "SPY"])
spy_r = px_u["SPY"].pct_change().fillna(0.0).iloc[WARMUP:]
SPY = row_of(spy_r)

P("=" * 100)
P("Idea 53 - keep-candidate-universe-robustness (idea 2's n=20 book, composition draws)")
P("=" * 100)
P(f"U56 tradable {len(U_T)}   B136 tradable {len(B_T)}   U56 subset of B136: {set(U_T) <= set(B_T)}")
P(f"sample {px_u.index[WARMUP].date()} .. {px_u.index[-1].date()} after {WARMUP}-row warm-up; "
  f"cost {COST} bps, freq {FREQ}, gross {GROSS}")
P(f"SPY: CAGR {SPY['CAGR']:.2%}  Sharpe {SPY['Sharpe']:.4f}  MaxDD {SPY['MaxDD']:.2%}  "
  f"H1 {SPY['H1']:.4f}  H2 {SPY['H2']:.4f}  OOS {SPY['OOS_Sharpe']:.4f}")
P(f"4b LEVEL bars (constant on every draw): MaxDD >= {0.60 * SPY['MaxDD']:.2%}   "
  f"CAGR >= {0.70 * SPY['CAGR']:.2%}")

# ---------------------------------------------------------------- 0. the fitted panel
P("")
P("-" * 100)
P("0. THE FITTED PANEL (d=0) - full U56, all three n, both KEEP paths")
P("-" * 100)
V2_U = row_of(v2_returns(px_u))
base = run_panel(px_u)
grid = []
for n, r in base.items():
    x = row_of(r)
    grid.append(dict(panel="U56", d=0, n=n, **{k: round(float(v), 6) for k, v in x.items()},
                     keep4a=keep4a(x, V2_U), keep4b=keep4b(x, SPY), first_fail=first_fail(x, SPY),
                     **{k: round(float(v), 6) for k, v in margins(x, SPY).items()}))
U0 = {n: row_of(r) for n, r in base.items()}
P(f"  RULES v2 on U56: CAGR {V2_U['CAGR']:.2%} Sharpe {V2_U['Sharpe']:.4f} MaxDD {V2_U['MaxDD']:.2%} "
  f"H1/H2 {V2_U['H1']:.3f}/{V2_U['H2']:.3f} OOS {V2_U['OOS_Sharpe']:.4f}")
P(f"  {'n':>3} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} {'OOSShrp':>8} | 4a 4b firstfail")
for g in grid:
    P(f"  {g['n']:>3} | {g['CAGR']:>7.2%} {g['Sharpe']:>7.4f} {g['MaxDD']:>8.2%} {g['H1']:>6.3f} "
      f"{g['H2']:>6.3f} {g['OOS_Sharpe']:>8.4f} | {str(g['keep4a']):>5} {str(g['keep4b']):>5} {g['first_fail']}")
a = U0[ANCHOR_N]
P(f"  ANCHOR n=20 4b margins vs the bars: H1 {a['H1'] - SPY['H1']:+.4f}  H2 {a['H2'] - SPY['H2']:+.4f}  "
  f"OOS {a['OOS_Sharpe'] - SPY['OOS_Sharpe']:+.4f}  DD {a['MaxDD'] - 0.60 * SPY['MaxDD']:+.2%}  "
  f"CAGR {a['CAGR'] - 0.70 * SPY['CAGR']:+.2%}")

# ---------------------------------------------------------------- 1. leave-one-out
P("")
P("-" * 100)
P("1. LEAVE-ONE-OUT (d=1, all 55 panels, anchor n=20) - is any single name load-bearing?")
P("-" * 100)
loo = []
for t in U_T:
    cols = [c for c in U_T if c != t]
    r = run_panel(px_u[cols + ["SPY"]], ns=[ANCHOR_N])[ANCHOR_N]
    x = row_of(r)
    loo.append(dict(dropped=t, **{k: round(float(v), 6) for k, v in x.items()},
                    keep4b=keep4b(x, SPY), first_fail=first_fail(x, SPY)))
LOO = pd.DataFrame(loo).sort_values("Sharpe")
LOO.to_csv(f"{OUT}.loo.csv", index=False)
P(f"  4b passes: {int(LOO.keep4b.sum())}/{len(LOO)}")
P(f"  Sharpe range {LOO.Sharpe.min():.4f} .. {LOO.Sharpe.max():.4f} (full panel {a['Sharpe']:.4f});"
  f"  MaxDD range {LOO.MaxDD.min():.2%} .. {LOO.MaxDD.max():.2%} (full {a['MaxDD']:.2%})")
P("  5 names whose REMOVAL hurts most (lowest resulting Sharpe):")
for _, q in LOO.head(5).iterrows():
    P(f"    -{q['dropped']:6s} Sharpe {q['Sharpe']:.4f}  MaxDD {q['MaxDD']:7.2%}  "
      f"H2 {q['H2']:.3f}  OOS {q['OOS_Sharpe']:.4f}  4b {q['keep4b']}")
P("  5 names whose REMOVAL helps most:")
for _, q in LOO.tail(5).iloc[::-1].iterrows():
    P(f"    -{q['dropped']:6s} Sharpe {q['Sharpe']:.4f}  MaxDD {q['MaxDD']:7.2%}  "
      f"H2 {q['H2']:.3f}  OOS {q['OOS_Sharpe']:.4f}  4b {q['keep4b']}")
if (~LOO.keep4b).any():
    P(f"  names whose single removal BREAKS 4b: "
      f"{list(LOO[~LOO.keep4b].dropped)} (bar: {list(LOO[~LOO.keep4b].first_fail)})")

# ---------------------------------------------------------------- 2. composition draws + size control
P("")
P("-" * 100)
P(f"2. COMPOSITION DRAWS (d=5, d=10 from U56, {N_DRAWS} each, n in {NS} with per-draw rule-8) "
  f"and SIZE CONTROL (random 50- and 45-name panels from B136)")
P("-" * 100)
rng = np.random.default_rng(SEED)
draws = []
for d in DROPS:
    for i in range(N_DRAWS):
        keep = sorted(set(U_T) - set(rng.choice(U_T, size=d, replace=False).tolist()))
        sub = px_u[keep + ["SPY"]]
        rets = run_panel(sub)
        xs = {n: row_of(r) for n, r in rets.items()}
        pick = max(NS, key=lambda n: xs[n]["IS_Sharpe"])
        v2 = row_of(v2_returns(sub))
        for n in NS:
            x = xs[n]
            draws.append(dict(arm="U56-drop", d=d, k=len(keep), draw=i, n=n,
                              is_pick=(n == pick), anchor=(n == ANCHOR_N),
                              **{kk: round(float(v), 6) for kk, v in x.items()},
                              keep4a=keep4a(x, v2), keep4b=keep4b(x, SPY),
                              first_fail=first_fail(x, SPY),
                              v2_Sharpe=round(float(v2["Sharpe"]), 4),
                              v2_OOS_Sharpe=round(float(v2["OOS_Sharpe"]), 4),
                              **{kk: round(float(v), 6) for kk, v in margins(x, SPY).items()}))
    P(f"  ... U56 drop d={d}: {N_DRAWS} draws done")

for k in (50, 45):
    for i in range(N_DRAWS):
        cols = sorted(rng.choice(B_T, size=k, replace=False).tolist())
        sub = px_b[cols + ["SPY"]]
        r = run_panel(sub, ns=[ANCHOR_N])[ANCHOR_N]
        x = row_of(r)
        draws.append(dict(arm="B136-size-control", d=len(B_T) - k, k=k, draw=i, n=ANCHOR_N,
                          is_pick=True, anchor=True,
                          **{kk: round(float(v), 6) for kk, v in x.items()},
                          keep4a=False, keep4b=keep4b(x, SPY), first_fail=first_fail(x, SPY),
                          v2_Sharpe=np.nan, v2_OOS_Sharpe=np.nan,
                          **{kk: round(float(v), 6) for kk, v in margins(x, SPY).items()}))
    P(f"  ... B136 size control k={k}: {N_DRAWS} draws done")

D = pd.DataFrame(draws)
D.to_csv(f"{OUT}.draws.csv", index=False)
pd.DataFrame(grid).to_csv(f"{OUT}.grid.csv", index=False)


def describe(d, label):
    P(f"\n  {label}  (n={len(d)} panels)")
    for col, fmt in (("CAGR", "{:.2%}"), ("Sharpe", "{:.4f}"), ("MaxDD", "{:.2%}"),
                     ("H2", "{:.4f}"), ("OOS_Sharpe", "{:.4f}")):
        q = d[col].quantile([0.05, 0.25, 0.50, 0.75, 0.95])
        P(f"    {col:10s} p05 {fmt.format(q[0.05])}  p25 {fmt.format(q[0.25])}  "
          f"med {fmt.format(q[0.50])}  p75 {fmt.format(q[0.75])}  p95 {fmt.format(q[0.95])}")
    P(f"    4b pass rate {d.keep4b.mean():.1%} ({int(d.keep4b.sum())}/{len(d)})"
      + (f"   4a pass rate {d.keep4a.mean():.1%}" if d.keep4a.notna().any() else ""))
    ff = d[~d.keep4b].first_fail.value_counts()
    P(f"    first-failing bar among failures: {dict(ff) if len(ff) else '{}'}")
    P(f"    per-bar failure rates: H1 {(d.m_H1 <= 0).mean():.1%}  H2 {(d.m_H2 <= 0).mean():.1%}  "
      f"OOS {(d.m_OOS <= 0).mean():.1%}  DD {(d.m_DD < 0).mean():.1%}  CAGR {(d.m_CAGR < 0).mean():.1%}")


for d in DROPS:
    describe(D[(D.arm == "U56-drop") & (D.d == d) & D.anchor], f"U56 minus {d} names, ANCHOR n=20")
for k in (50, 45):
    describe(D[(D.arm == "B136-size-control") & (D.k == k)],
             f"SIZE CONTROL: random {k}-name panel from B136, n=20")

P("")
P("  HEAD-TO-HEAD at matched pool size (anchor n=20, 4b pass rate):")
for d, k in ((5, 50), (10, 45)):
    u = D[(D.arm == "U56-drop") & (D.d == d) & D.anchor]
    b = D[(D.arm == "B136-size-control") & (D.k == k)]
    P(f"    k={k}: U56-minus-{d} {u.keep4b.mean():.1%} vs random-B136 {b.keep4b.mean():.1%}   "
      f"(median MaxDD {u.MaxDD.median():.2%} vs {b.MaxDD.median():.2%}; "
      f"median Sharpe {u.Sharpe.median():.4f} vs {b.Sharpe.median():.4f})")

# ---------------------------------------------------------------- 3. rule 8 per draw
P("")
P("-" * 100)
P("3. RULE 8 PER DRAW - n chosen on <=2016 by IS Sharpe inside each draw, 2017-2026 read once")
P("-" * 100)
wf = []
for d in DROPS:
    sub = D[(D.arm == "U56-drop") & (D.d == d)]
    pick = sub[sub.is_pick]
    anch = sub[sub.anchor]
    best = sub.loc[sub.groupby("draw")["OOS_Sharpe"].idxmax()]
    wf.append(dict(d=d, k=int(pick.k.iloc[0]), draws=len(pick),
                   pick_n_counts=dict(pick.n.value_counts().sort_index()),
                   med_OOS_Sharpe=round(float(pick.OOS_Sharpe.median()), 4),
                   med_OOS_CAGR=round(float(pick.OOS_CAGR.median()), 6),
                   med_OOS_MaxDD=round(float(pick.OOS_MaxDD.median()), 6),
                   anchor_med_OOS=round(float(anch.OOS_Sharpe.median()), 4),
                   best_med_OOS=round(float(best.OOS_Sharpe.median()), 4),
                   med_regret=round(float(pick.OOS_Sharpe.median() - best.OOS_Sharpe.median()), 4),
                   beats_SPY_OOS=round(float((pick.OOS_Sharpe > SPY["OOS_Sharpe"]).mean()), 4),
                   beats_v2_OOS=round(float((pick.OOS_Sharpe > pick.v2_OOS_Sharpe).mean()), 4),
                   pick_4b_rate=round(float(pick.keep4b.mean()), 4),
                   anchor_4b_rate=round(float(anch.keep4b.mean()), 4)))
W = pd.DataFrame(wf)
W.to_csv(f"{OUT}.walkforward.csv", index=False)
P(W.to_string(index=False))
P(f"  SPY OOS Sharpe {SPY['OOS_Sharpe']:.4f}, CAGR {SPY['OOS_CAGR']:.2%}, MaxDD {SPY['OOS_MaxDD']:.2%}; "
  f"RULES v2 on full U56 OOS {V2_U['OOS_Sharpe']:.4f}")

# does the IS chooser add anything over just taking n=20?
for d in DROPS:
    sub = D[(D.arm == "U56-drop") & (D.d == d)]
    pk = sub[sub.is_pick].set_index("draw")["OOS_Sharpe"]
    an = sub[sub.anchor].set_index("draw")["OOS_Sharpe"]
    delta = (pk - an)
    P(f"    d={d}: IS-chooser minus anchor OOS Sharpe  mean {delta.mean():+.4f}  "
      f"median {delta.median():+.4f}  better in {(delta > 0).mean():.1%} of draws")

# ---------------------------------------------------------------- 4. verdict
P("")
P("-" * 100)
P("4. VERDICT")
P("-" * 100)
u5 = D[(D.arm == "U56-drop") & (D.d == 5) & D.anchor]
u10 = D[(D.arm == "U56-drop") & (D.d == 10) & D.anchor]
P(f"  fitted panel d=0 n=20: 4b {keep4b(a, SPY)}  (Sharpe {a['Sharpe']:.4f}, MaxDD {a['MaxDD']:.2%}, "
  f"H2 {a['H2']:.3f}, OOS {a['OOS_Sharpe']:.4f})")
P(f"  d=1 leave-one-out: 4b {int(LOO.keep4b.sum())}/{len(LOO)}")
P(f"  d=5:  4b {u5.keep4b.mean():.1%}   d=10: 4b {u10.keep4b.mean():.1%}")
P(f"  size control k=50: {D[(D.arm == 'B136-size-control') & (D.k == 50)].keep4b.mean():.1%}   "
  f"k=45: {D[(D.arm == 'B136-size-control') & (D.k == 45)].keep4b.mean():.1%}")

Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
print(f"\nwrote {OUT.name}.grid.csv, .draws.csv, .loo.csv, .walkforward.csv, .console.txt")
