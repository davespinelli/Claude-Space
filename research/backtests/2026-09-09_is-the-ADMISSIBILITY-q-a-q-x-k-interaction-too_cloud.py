#!/usr/bin/env python3
"""Idea 526 — is the admissibility q a (q x k) interaction too?

Question (QUEUE 526): idea 285 found the 4b binding ORDER reverses across book size n (at
n=30 the CAGR floor is gone by q=0.05 and the DD cap never binds; at n=10/EWall the DD cap
binds at q=0), with PANEL size k held fixed at idea 276's 40.  Sweep k against n at fixed q
rungs and report whether the binding bar is a function of n/k (CONCENTRATION) rather than of
n itself.

Two tuned parameters, both reporting axes with every grid point published:
    k in {20, 40, 80, 100}     panel size   (tuned param 1)
    n in {5, 10, 20, 25, 40, 50} book size, per k, n <= k   (tuned param 2)
q is NOT tuned: it is held at the five fixed rungs {0.00, 0.25, 0.50, 0.75, 1.00}, exactly as
the queue asks ("at fixed q rungs").

k=136 IS NOT REACHABLE and is reported as k=100 instead.  The queue's "136" is B136's column
count, but 36 of those are ETFs and idea 276/285's MIX excludes ETFs from the large-cap pool,
which leaves 100 large-cap STOCKS.  A k=136 panel therefore cannot be built at q=0 (it would
need 136 large-cap stocks), and a ladder whose top rung exists only above q~0.27 is not
comparable across q.  k=100 is the largest panel size that exists at EVERY q rung, so the
top rung is k=100 = the whole large-cap stock pool, and this substitution is stated in the
result rather than papered over.

Construction is idea 276's MIX rebuilt exactly as ideas 285/286 rebuilt it: a share q of each
k-name panel drawn from the sub-$2B panel and 1-q from the large-cap STOCK pool (ETFs
excluded), all panels run on ONE common window (the small panel's trading days) so the rungs
are comparable, SPY joined as a benchmark column only.  12 draws per (k, q) cell = 240 panels.
10 bps, weekly, next-day execution, 260-day warm-up skip.

ALL FIVE 4b BARS are evaluated separately (H1, H2, OOS, DDcap, CAGRfloor), the OOS bar by
PROTOCOL rule 8 (IS <= 2016-12-31, 2017..end read once).  BOTH KEEP paths are evaluated:
4a against the live RULES v2 book on the SAME panel, 4b against SPY.

SURVIVORSHIP: the small panel is the CURRENT constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md) with the 44 max_1d_move >= 1.0 names dropped first; the large-cap
pool is the current constituents of research/universe_broad.json.  Both ends of the q ladder
are survivor sets, so the LEVEL of every number here is optimistic; the CONTRAST across
(q, k, n) is what the idea asks for and is the only thing claimed.

Deterministic (seed 20260909), standalone, no network.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import backtest, load_universe, metrics, rules_v2_weights, score  # noqa: E402

STEM = Path(__file__).with_suffix("")
COST, FREQ = 10, "W"
KS = [20, 40, 80, 100]                              # tuned param 1
NS_BY_K = {20: [5, 10, 20], 40: [5, 10, 20, 40],    # tuned param 2 (n <= k)
           80: [5, 10, 20, 40], 100: [5, 10, 20, 25, 40, 50]}
QS = [0.00, 0.25, 0.50, 0.75, 1.00]                 # FIXED rungs, not tuned
N_DRAWS = 12
GROSS = 0.75
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
SEED = 20260909
BARS = ["H1", "H2", "OOS", "DDcap", "CAGRfloor"]
REUSE = "--reuse" in sys.argv

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ra, rb = a.rank(), b.rank()
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(ra.corr(rb))


# ------------------------------------------------------------------ sources
U = json.loads((ROOT / "research" / "universe.json").read_text())
ETFS = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
pxb = load_universe(broad=True)
pxs = load_universe(small=True)
meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
S_STK = [c for c in pxs.columns if c != "SPY" and c not in BAD]
B_STK = [c for c in pxb.columns if c != "SPY" and c not in ETFS]
SPY_RAW = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
COMMON = pxs.index


def mk(cols_s, cols_l):
    parts = []
    if cols_s:
        parts.append(pxs[cols_s])
    if cols_l:
        parts.append(pxb[cols_l].reindex(COMMON, method="ffill"))
    px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
    return px.join(SPY_RAW.reindex(px.index, method="ffill").rename("SPY"))


# ------------------------------------------------------------------ books (idea 285/286's forms)
def eligible(px, tr):
    s, above, vol20 = score(px[tr], vol_scale=False)
    return s.where(above & (vol20 < 0.60))


def breadth_of(px, tr):
    above = px[tr] > px[tr].rolling(200).mean()
    vol20 = px[tr].pct_change().rolling(20).std() * np.sqrt(252)
    e = (above & (vol20 < 0.60)).iloc[WARMUP:]
    return float((e.sum(axis=1) / len(tr)).mean())


# ================================================================== main
t0 = time.time()
say("=" * 100)
say("IDEA 526 — is the admissibility q a (q x k) interaction too?   (cloud, 2026-09-09)")
say("=" * 100)
say(f"\nsmall panel: {len(BAD)} tickers with max_1d_move >= 1.0 dropped first, {len(S_STK)} usable;"
    f" large-cap STOCK pool {len(B_STK)} (the 36 ETFs of B136 excluded)")
say(f"k=136 NOT REACHABLE: only {len(B_STK)} large-cap stocks exist, so a k=136 panel cannot be built "
    f"at q=0.  Top rung is k=100 = the WHOLE large-cap stock pool.  Stated, not papered over.")
say(f"common window {COMMON[0].date()} .. {COMMON[-1].date()} ({len(COMMON)} rows)")
say(f"grid: k in {KS} x q in {QS} x {N_DRAWS} draws = {len(KS)*len(QS)*N_DRAWS} panels, seed {SEED}")
say(f"books per panel: RULES v2 (4a comparand) + EWall (un-ranked control) + top-n for n in "
    + ", ".join(f"k={k}:{NS_BY_K[k]}" for k in KS))
say(f"costs {COST} bps, {FREQ} cadence, next-day execution, {WARMUP}-day warm-up skip; "
    f"rule 8 IS <= {IS_END.date()}, OOS {IS_END.date()}+1 .. end")
say("SURVIVORSHIP: both ends of the q ladder are CURRENT-constituent sets; levels are optimistic, "
    "the (q, k, n) CONTRAST is what is claimed.")

rng = np.random.default_rng(SEED)
panels = []
for k in KS:
    for q in QS:
        ns_ = int(round(q * k)); nl_ = k - ns_
        for d in range(N_DRAWS):
            sc = list(rng.choice(S_STK, size=ns_, replace=False)) if ns_ else []
            lc = list(rng.choice(B_STK, size=nl_, replace=False)) if nl_ else []
            panels.append((k, q, d, ns_, nl_, sc, lc))

rows = []
for i, (k, q, d, ns_, nl_, sc, lc) in enumerate([] if REUSE else panels):
    px = mk(sc, lc)
    tr = [c for c in px.columns if c != "SPY"]
    start = px.index[WARMUP]
    oos_sl = slice(IS_END + pd.Timedelta(days=1), None)
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    h = len(spy) // 2
    ms, ms1, ms2, ms_oos = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:]), metrics(spy.loc[oos_sl])
    base = backtest(px, rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0),
                    cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb, mb1, mb2, mb_oos = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:]), metrics(base.loc[oos_sl])
    br = breadth_of(px, tr)

    el = eligible(px, tr)
    rank = el.rank(axis=1, ascending=False)
    e01 = el.notna().astype(float)
    cnt = e01.sum(axis=1).replace(0, np.nan)
    specs = [("EWall", np.nan, (GROSS * e01.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0))]
    for n in NS_BY_K[k]:
        specs.append((f"top{n}", n, ((rank <= n).astype(float) * (GROSS / n))
                      .reindex(columns=px.columns).fillna(0.0)))
    for arm, n, w in specs:
        r = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
        m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[oos_sl])
        bar = dict(H1=m1["Sharpe"] > ms1["Sharpe"], H2=m2["Sharpe"] > ms2["Sharpe"],
                   OOS=m_oos["Sharpe"] > ms_oos["Sharpe"],
                   DDcap=m["MaxDD"] >= 0.60 * ms["MaxDD"],
                   CAGRfloor=m["CAGR"] >= 0.70 * ms["CAGR"])
        rows.append(dict(k=k, q=q, draw=d, n_small=ns_, n_large=nl_, breadth=br, arm=arm, n=n,
                         conc=(np.nan if not np.isfinite(n) else n / k),
                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=m1["Sharpe"], H2=m2["Sharpe"],
                         IS_Sharpe=m_is["Sharpe"], OOS_Sharpe=m_oos["Sharpe"],
                         OOS_CAGR=m_oos["CAGR"], OOS_MaxDD=m_oos["MaxDD"],
                         **{f"bar_{b}": bool(v) for b, v in bar.items()},
                         pass4b=bool(all(bar.values())),
                         pass4a=bool(m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                                     and m["MaxDD"] >= mb["MaxDD"]),
                         base_Sharpe=mb["Sharpe"], base_H1=mb1["Sharpe"], base_H2=mb2["Sharpe"],
                         base_CAGR=mb["CAGR"], base_MaxDD=mb["MaxDD"],
                         base_OOS_Sharpe=mb_oos["Sharpe"], base_OOS_CAGR=mb_oos["CAGR"],
                         base_OOS_MaxDD=mb_oos["MaxDD"],
                         SPY_Sharpe=ms["Sharpe"], SPY_H1=ms1["Sharpe"], SPY_H2=ms2["Sharpe"],
                         SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
                         SPY_OOS_Sharpe=ms_oos["Sharpe"], SPY_OOS_CAGR=ms_oos["CAGR"],
                         SPY_OOS_MaxDD=ms_oos["MaxDD"]))
    if (i + 1) % 20 == 0:
        say(f"    k={k} q={q:.2f} done ({i+1}/{len(panels)} panels, {time.time()-t0:6.1f}s)")

if REUSE:
    A = pd.read_csv(f"{STEM}.arms.csv")
    say(f"--reuse: re-read {len(A)} arm-rows (the panel loop is deterministic; seed {SEED})")
else:
    A = pd.DataFrame(rows)
    A.to_csv(f"{STEM}.arms.csv", index=False)
say(f"\n{len(A)} arm-rows over {len(panels)} panels written to {Path(STEM).name}.arms.csv")

# ---------------------------------------------------------------- 0. ladder sanity
say("\n[0] THE LADDER — does q still move the panel the same way at every k?")
bl = A.pivot_table(index="q", columns="k", values="breadth", aggfunc="mean")
say(bl.to_string(float_format=lambda x: f"{x:.4f}"))
for k in KS:
    sub = bl[k].reset_index()
    say(f"    Spearman(q, breadth) at k={k}: {spearman(sub['q'], sub[k]):.4f}")

# ---------------------------------------------------------------- 1. the full grid (all points)
say("\n[1] THE FULL GRID — pass rate of every 4b bar, per (k, n, q) cell. ALL POINTS.")
G = (A[A.arm != "EWall"]
     .groupby(["k", "n", "conc", "q"])
     .agg(**{b: (f"bar_{b}", "mean") for b in BARS},
          joint4b=("pass4b", "mean"), pass4a=("pass4a", "mean"),
          CAGR=("CAGR", "median"), Sharpe=("Sharpe", "median"), MaxDD=("MaxDD", "median"),
          OOS_Sharpe=("OOS_Sharpe", "median"), draws=("pass4b", "size"))
     .reset_index())
G.to_csv(f"{STEM}.grid.csv", index=False)
for k in KS:
    say(f"\n--- k={k} ({N_DRAWS} draws per cell) ---")
    say(G[G.k == k].drop(columns=["k"]).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say("\n--- EWall control (un-ranked, per k) ---")
E = (A[A.arm == "EWall"].groupby(["k", "q"])
     .agg(**{b: (f"bar_{b}", "mean") for b in BARS}, joint4b=("pass4b", "mean"),
          pass4a=("pass4a", "mean"), CAGR=("CAGR", "median"), Sharpe=("Sharpe", "median"),
          MaxDD=("MaxDD", "median"), OOS_Sharpe=("OOS_Sharpe", "median")).reset_index())
say(E.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
E.to_csv(f"{STEM}.ewall.csv", index=False)

# ---------------------------------------------------------------- 2. the binding bar per cell
say("\n[2] THE BINDING BAR — the bar with the LOWEST pass rate in each (k, n, q) cell")
G["binding"] = G[BARS].idxmin(axis=1)
G["binding_rate"] = G[BARS].min(axis=1)
G["tied"] = (G[BARS].eq(G[BARS].min(axis=1), axis=0)).sum(axis=1)
say(G.pivot_table(index=["k", "n"], columns="q", values="binding", aggfunc="first").to_string())
say("\n(ties are common when a bar's rate is 1.000 or 0.000; tie counts:)")
say(G["tied"].value_counts().sort_index().to_string())
G.to_csv(f"{STEM}.grid.csv", index=False)

# ---------------------------------------------------------------- 3. matched-pair test
say("\n[3] THE TEST — matched pairs. Is the binding bar a function of n/k, or of n?")
say("    MATCHED-CONC pairs: same conc and same q, different k.  If concentration governs, they agree.")
say("    MATCHED-N    pairs: same n    and same q, different k.  If n itself governs, they agree.")
pairs = []
for key, lab in [("conc", "MATCHED-CONC"), ("n", "MATCHED-N")]:
    for (kv, q), g in G.groupby([key, "q"]):
        g = g.sort_values("k")
        for a in range(len(g)):
            for b in range(a + 1, len(g)):
                ra, rb = g.iloc[a], g.iloc[b]
                if ra["k"] == rb["k"]:
                    continue
                pairs.append(dict(kind=lab, key=key, key_val=kv, q=q,
                                  k_a=ra["k"], n_a=ra["n"], k_b=rb["k"], n_b=rb["n"],
                                  bind_a=ra["binding"], bind_b=rb["binding"],
                                  tied_a=int(ra["tied"]), tied_b=int(rb["tied"]),
                                  unique=bool(ra["tied"] == 1 and rb["tied"] == 1),
                                  agree=bool(ra["binding"] == rb["binding"]),
                                  d_joint=abs(ra["joint4b"] - rb["joint4b"]),
                                  d_rate=float(np.mean([abs(ra[x] - rb[x]) for x in BARS]))))
P = pd.DataFrame(pairs)
P.to_csv(f"{STEM}.pairs.csv", index=False)
say(P.groupby("kind").agg(pairs=("agree", "size"), agree_rate=("agree", "mean"),
                          mean_abs_d_joint4b=("d_joint", "mean"),
                          mean_abs_d_barrate=("d_rate", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))
say("\n(per q rung:)")
say(P.pivot_table(index="q", columns="kind", values="agree", aggfunc="mean")
    .to_string(float_format=lambda x: f"{x:.3f}"))
say("\n(TIE-ROBUST: `binding` is an argmin, and at 12 draws a pass rate of 1.000 or 0.000 is common, "
    "so most cells have several bars tied at the minimum. Restricted to pairs where BOTH cells have "
    "a UNIQUE minimum, the same comparison reads:)")
PU = P[P.unique]
if len(PU):
    say(PU.groupby("kind").agg(pairs=("agree", "size"), agree_rate=("agree", "mean"),
                               mean_abs_d_barrate=("d_rate", "mean"))
        .to_string(float_format=lambda x: f"{x:.4f}"))
else:
    say("    no pair has a unique minimum on both sides.")
say(f"    cells with a unique minimum: {int((G['tied']==1).sum())} of {len(G)}; "
    f"pairs with both unique: {len(PU)} of {len(P)}")
say("\n(and the tie-free reading of the same question — mean |difference| in the FIVE bar pass "
    "rates within a matched pair, which needs no argmin at all: lower = the two cells behave more "
    "alike. This is the column `mean_abs_d_barrate` above.)")

# ---------------------------------------------------------------- 4. continuous version
say("\n[4] CONTINUOUS — which predictor orders each bar's pass rate better, log(n) or log(n/k)?")
cont = []
for b in BARS + ["joint4b", "pass4a"]:
    for q in QS:
        g = G[G.q == q]
        cont.append(dict(bar=b, q=q, cells=len(g),
                         rho_n=spearman(np.log(g["n"]), g[b]),
                         rho_conc=spearman(np.log(g["conc"]), g[b]),
                         rho_k=spearman(np.log(g["k"]), g[b])))
CT = pd.DataFrame(cont)
CT.to_csv(f"{STEM}.rho.csv", index=False)
say(CT.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say("\n(|rho| averaged over the five q rungs:)")
say(CT.assign(an=CT.rho_n.abs(), ac=CT.rho_conc.abs(), ak=CT.rho_k.abs())
    .groupby("bar")[["an", "ac", "ak"]].mean()
    .rename(columns=dict(an="|rho| vs log n", ac="|rho| vs log(n/k)", ak="|rho| vs log k"))
    .to_string(float_format=lambda x: f"{x:.4f}"))

# ---------------------------------------------------------------- 5. rule 8 walk-forward
say("\n[5] RULE 8 WALK-FORWARD — the (k, n) cell chosen on the FIRST HALF only, read ONCE on the second")
say(f"    chooser: within each q rung and each draw index, pick the arm with the best IS Sharpe "
    f"(<= {IS_END.date()}); evaluate that arm's OOS ({IS_END.date()}+1 .. {COMMON[-1].date()}) leg.")
wf = []
R = A[A.arm != "EWall"]
for q in QS:
    sub = R[R.q == q]
    # per draw index, the chooser sees every (k, n) arm on that draw and picks on IS Sharpe alone
    picks = sub.loc[sub.groupby("draw")["IS_Sharpe"].idxmax()]
    ew = A[(A.arm == "EWall") & (A.q == q)]
    anchor = sub.groupby("draw")["OOS_Sharpe"].mean()          # blind average over all cells
    wf.append(dict(q=q, picks=len(picks),
                   pick_k=picks["k"].median(), pick_n=picks["n"].median(),
                   pick_conc=picks["conc"].median(),
                   OOS_CAGR=picks["OOS_CAGR"].median(), OOS_Sharpe=picks["OOS_Sharpe"].median(),
                   OOS_MaxDD=picks["OOS_MaxDD"].median(),
                   EWall_OOS_Sharpe=ew["OOS_Sharpe"].median(), EWall_OOS_CAGR=ew["OOS_CAGR"].median(),
                   EWall_OOS_MaxDD=ew["OOS_MaxDD"].median(),
                   anchor_OOS_Sharpe=anchor.median(),
                   base_OOS_CAGR=picks["base_OOS_CAGR"].median(),
                   base_OOS_Sharpe=picks["base_OOS_Sharpe"].median(),
                   base_OOS_MaxDD=picks["base_OOS_MaxDD"].median(),
                   SPY_OOS_CAGR=picks["SPY_OOS_CAGR"].median(),
                   SPY_OOS_Sharpe=picks["SPY_OOS_Sharpe"].median(),
                   SPY_OOS_MaxDD=picks["SPY_OOS_MaxDD"].median(),
                   beats_SPY=float((picks["OOS_Sharpe"] > picks["SPY_OOS_Sharpe"]).mean()),
                   beats_base=float((picks["OOS_Sharpe"] > picks["base_OOS_Sharpe"]).mean()),
                   pass4b=float(picks["pass4b"].mean()), pass4a=float(picks["pass4a"].mean())))
W = pd.DataFrame(wf)
W.to_csv(f"{STEM}.walkforward.csv", index=False)
say(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say(f"\npooled over all {len(QS)} rungs x {N_DRAWS} draws: chooser beats SPY OOS on "
    f"{100*W['beats_SPY'].mean():.1f}% of draws, RULES v2 OOS on {100*W['beats_base'].mean():.1f}%; "
    f"4b {100*W['pass4b'].mean():.1f}%, 4a {100*W['pass4a'].mean():.1f}%")

# ---------------------------------------------------------------- 6. KEEP paths
say("\n[6] BOTH KEEP PATHS on the full grid (all arm-rows, no selection)")
kp = (A.groupby(["k", "arm"])
      .agg(rows=("pass4b", "size"), pass4a=("pass4a", "mean"), pass4b=("pass4b", "mean"),
           CAGR=("CAGR", "median"), Sharpe=("Sharpe", "median"), MaxDD=("MaxDD", "median"),
           H1=("H1", "median"), H2=("H2", "median"), OOS_Sharpe=("OOS_Sharpe", "median"))
      .reset_index())
kp.to_csv(f"{STEM}.keeppaths.csv", index=False)
say(kp.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
n4a, n4b = int(A["pass4a"].sum()), int(A["pass4b"].sum())
say(f"\n4a passes {n4a}/{len(A)} ({100*n4a/len(A):.1f}%);  4b passes {n4b}/{len(A)} ({100*n4b/len(A):.1f}%)")
say(f"SPY over the common window: CAGR {A['SPY_CAGR'].iloc[0]:.2%}, Sharpe {A['SPY_Sharpe'].iloc[0]:.3f}, "
    f"MaxDD {A['SPY_MaxDD'].iloc[0]:.2%}; OOS Sharpe {A['SPY_OOS_Sharpe'].iloc[0]:.3f}, "
    f"OOS CAGR {A['SPY_OOS_CAGR'].iloc[0]:.2%}")

say(f"\ndone in {time.time()-t0:.1f}s")
Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")
