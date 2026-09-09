#!/usr/bin/env python3
"""Idea 285 — is the 4b footprint a monotone function of cap mix?

Question (QUEUE 285): idea 276's 4b passes were 3/66 (n=10) and 16/66 (n=20), every one at
q <= 0.5, i.e. the KEEP path's own eligibility tracks the panel's capitalisation.  Sweep q at
finer resolution with more draws and report the q at which EACH 4b bar (H1, H2, OOS, DD cap,
CAGR floor) first binds — a published admissibility curve rather than a per-panel verdict.

Construction is idea 276's MIX, rebuilt exactly as idea 286 rebuilt it: k=40 names per panel,
a share q drawn from the sub-$2B panel and 1-q from the large-cap STOCK pool (ETFs excluded),
all panels run on ONE common window (the small panel's trading days) so the q rungs are
comparable, SPY joined as a benchmark column only.

Two tuned parameters, both reporting axes with every point published:
    q in {0.00, 0.05, ..., 1.00}      21 rungs   (idea 276 used 5)
    n in {10, 20, 30}                 book size  (idea 276 used 10 and 20)
x 20 draws per rung (idea 276/286 used 8) = 420 panels; plus EWall as the un-ranked control and
the live RULES v2 book as the 4a comparand on each panel.  10 bps, weekly, next-day execution,
260-day warm-up skip.

ALL FIVE 4b BARS are evaluated separately, the OOS bar by PROTOCOL rule 8 (IS <= 2016-12-31,
2017..end read once), so this run reports the admissibility curve of each bar, not one verdict.

SURVIVORSHIP: the small panel is the CURRENT constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md) with the 44 max_1d_move >= 1.0 names dropped first; the large-cap
pool is the current constituents of research/universe_broad.json.  Both ends of the q ladder are
therefore survivor sets and the LEVEL of every number here is optimistic; the CONTRAST across q
is what the idea asks for and is the only thing claimed.

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
K_MIX, N_DRAWS = 40, 20
QS = [round(x / 20, 2) for x in range(21)]     # tuned param 1: 0.00 .. 1.00 in 0.05 steps
NS = [10, 20, 30]                              # tuned param 2
GROSS = 0.75
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
SEED = 20260909
REUSE = "--reuse" in sys.argv   # re-read <stem>.arms.csv instead of recomputing the panel loop
BARS = ["H1", "H2", "OOS", "DDcap", "CAGRfloor"]

OUT = []


def spearman(a, b):
    """Rank correlation without scipy (pandas' method='spearman' imports it)."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ra, rb = a.rank(), b.rank()
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(ra.corr(rb))


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


# ------------------------------------------------------------------ sources
def build_sources():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    pxb = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    b_stk = [c for c in pxb.columns if c != "SPY" and c not in etfs]
    return dict(pxs=pxs, pxb=pxb, s_stk=s_stk, b_stk=b_stk, ndrop=len(bad))


# ------------------------------------------------------------------ books (idea 286's forms)
def _elig(px, tr):
    s, above, vol20 = score(px[tr], vol_scale=False)
    return s.where(above & (vol20 < 0.60))


def w_topn(n, gross=GROSS):
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        rank = _elig(px, tr).rank(axis=1, ascending=False)
        return ((rank <= n).astype(float) * (gross / n)).reindex(columns=px.columns).fillna(0.0)
    return f


def w_ewall(gross=GROSS):
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        e = _elig(px, tr).notna().astype(float)
        cnt = e.sum(axis=1).replace(0, np.nan)
        return (gross * e.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0)
    return f


def w_v2():
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        return rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)
    return f


def breadth_of(px, tr):
    above = px[tr] > px[tr].rolling(200).mean()
    vol20 = px[tr].pct_change().rolling(20).std() * np.sqrt(252)
    e = (above & (vol20 < 0.60)).iloc[WARMUP:]
    return float((e.sum(axis=1) / len(tr)).mean())


# ================================================================== main
t0 = time.time()
say("=" * 100)
say("IDEA 285 — is the 4b footprint a monotone function of cap mix?   (cloud, 2026-09-09)")
say("=" * 100)
src = build_sources()
spy_raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
COMMON = src["pxs"].index
say(f"\nsmall panel: {src['ndrop']} tickers with max_1d_move >= 1.0 dropped, {len(src['s_stk'])} usable;"
    f" large-cap STOCK pool {len(src['b_stk'])} (ETFs excluded)")
say(f"common window {COMMON[0].date()} .. {COMMON[-1].date()} ({len(COMMON)} rows); "
    f"k={K_MIX} names/panel, {len(QS)} q rungs x {N_DRAWS} draws = {len(QS)*N_DRAWS} panels, seed {SEED}")
say(f"books per panel: RULES v2 (4a comparand) + EWall (un-ranked control) + top-n for n in {NS}")
say(f"costs {COST} bps, {FREQ} cadence, next-day execution, {WARMUP}-day warm-up skip; "
    f"rule 8 IS <= {IS_END.date()}, OOS {IS_END.date()}+1 .. end")
say("SURVIVORSHIP: both ends of the q ladder are CURRENT-constituent sets; levels are optimistic, "
    "the q CONTRAST is what is claimed.")


def mk(cols_s, cols_l):
    parts = []
    if cols_s:
        parts.append(src["pxs"][cols_s])
    if cols_l:
        parts.append(src["pxb"][cols_l].reindex(COMMON, method="ffill"))
    px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
    return px.join(spy_raw.reindex(px.index, method="ffill").rename("SPY"))


rng = np.random.default_rng(SEED)
panels = []
for q in QS:
    ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
    for d in range(N_DRAWS):
        sc = list(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
        lc = list(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
        panels.append((q, d, ns_, nl_, sc, lc))

rows = []
for i, (q, d, ns_, nl_, sc, lc) in enumerate([] if REUSE else panels):
    px = mk(sc, lc)
    tr = [c for c in px.columns if c != "SPY"]
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    h = len(spy) // 2
    oos_sl = slice(IS_END + pd.Timedelta(days=1), None)
    ms, ms1, ms2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    ms_oos = metrics(spy.loc[oos_sl])
    base = backtest(px, w_v2()(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb, mb1, mb2 = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:])
    mb_oos = metrics(base.loc[oos_sl])
    br = breadth_of(px, tr)
    specs = [("EWall", np.nan, w_ewall())] + [(f"top{n}", n, w_topn(n)) for n in NS]
    for arm, n, fn in specs:
        r = backtest(px, fn(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
        m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[oos_sl])
        bar = dict(H1=m1["Sharpe"] > ms1["Sharpe"], H2=m2["Sharpe"] > ms2["Sharpe"],
                   OOS=m_oos["Sharpe"] > ms_oos["Sharpe"],
                   DDcap=m["MaxDD"] >= 0.60 * ms["MaxDD"],
                   CAGRfloor=m["CAGR"] >= 0.70 * ms["CAGR"])
        rows.append(dict(q=q, draw=d, n_small=ns_, n_large=nl_, breadth=br, arm=arm, n=n,
                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=m1["Sharpe"], H2=m2["Sharpe"],
                         IS_Sharpe=m_is["Sharpe"], OOS_Sharpe=m_oos["Sharpe"],
                         OOS_CAGR=m_oos["CAGR"], OOS_MaxDD=m_oos["MaxDD"],
                         **{f"bar_{k}": bool(v) for k, v in bar.items()},
                         pass4b=bool(all(bar.values())),
                         pass4a=bool(m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                                     and m["MaxDD"] >= mb["MaxDD"]),
                         base_Sharpe=mb["Sharpe"], base_H1=mb1["Sharpe"], base_H2=mb2["Sharpe"],
                         base_MaxDD=mb["MaxDD"], base_OOS_Sharpe=mb_oos["Sharpe"],
                         base_OOS_CAGR=mb_oos["CAGR"], base_OOS_MaxDD=mb_oos["MaxDD"],
                         SPY_Sharpe=ms["Sharpe"], SPY_H1=ms1["Sharpe"], SPY_H2=ms2["Sharpe"],
                         SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
                         SPY_OOS_Sharpe=ms_oos["Sharpe"], SPY_OOS_CAGR=ms_oos["CAGR"],
                         SPY_OOS_MaxDD=ms_oos["MaxDD"]))
    if (i + 1) % 20 == 0:
        say(f"    q={q:.2f} done ({i+1}/{len(panels)} panels, {time.time()-t0:6.1f}s)")

if REUSE:
    A = pd.read_csv(f"{STEM}.arms.csv")
    say(f"--reuse: re-read {len(A)} arm-rows from {Path(STEM).name}.arms.csv "
        f"(the panel loop above is deterministic; seed {SEED})")
else:
    A = pd.DataFrame(rows)
    A.to_csv(f"{STEM}.arms.csv", index=False)
say(f"\n{len(A)} arm-rows over {len(panels)} panels written to {Path(STEM).name}.arms.csv")

# ---------------------------------------------------------------- 1. breadth / cap-mix sanity
say("\n[1] THE LADDER — does q move the panel the way idea 276 said?")
bl = A.groupby("q").agg(breadth=("breadth", "mean"), SPY_Sharpe=("SPY_Sharpe", "mean")).reset_index()
say(bl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
rho = spearman(bl["q"], bl["breadth"])
say(f"Spearman(q, breadth) = {rho:.4f}  (idea 286 measured -0.9801 on a 5-rung ladder)")

# ---------------------------------------------------------------- 2. admissibility curves
say("\n[2] THE ADMISSIBILITY CURVE — pass RATE of each 4b bar, per q, per arm (all points)")
curves = []
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    sub = A[A.arm == arm]
    g = sub.groupby("q").agg(**{b: (f"bar_{b}", "mean") for b in BARS},
                             joint4b=("pass4b", "mean"), pass4a=("pass4a", "mean"),
                             Sharpe=("Sharpe", "median"), CAGR=("CAGR", "median"),
                             MaxDD=("MaxDD", "median"), OOS_Sharpe=("OOS_Sharpe", "median"))
    g.insert(0, "arm", arm)
    curves.append(g.reset_index())
C = pd.concat(curves, ignore_index=True)
C.to_csv(f"{STEM}.curves.csv", index=False)
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    say(f"\n--- {arm} (n draws per rung = {N_DRAWS}) ---")
    say(C[C.arm == arm].drop(columns=["arm"]).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# ---------------------------------------------------------------- 3. first-binding q
say("\n[3] WHERE EACH BAR FIRST BINDS  (first q whose pass rate drops below the stated level)")
fb = []
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    g = C[C.arm == arm].sort_values("q")
    for b in BARS:
        r = g[b].to_numpy(); qs = g["q"].to_numpy()
        def first_below(th):
            k = np.where(r < th)[0]
            return float(qs[k[0]]) if len(k) else np.nan
        rho_b = spearman(r, qs)
        steps = np.diff(r)
        fb.append(dict(arm=arm, bar=b, rate_q0=r[0], rate_q1=r[-1],
                       first_q_below_1_0=first_below(1.0), first_q_below_0_5=first_below(0.5),
                       first_q_below_0_1=first_below(0.1), spearman_q=rho_b,
                       down_steps=int((steps < 0).sum()), up_steps=int((steps > 0).sum()),
                       flat_steps=int((steps == 0).sum())))
    r = g["joint4b"].to_numpy(); qs = g["q"].to_numpy()
    steps = np.diff(r)
    fb.append(dict(arm=arm, bar="JOINT 4b", rate_q0=r[0], rate_q1=r[-1],
                   first_q_below_1_0=float(qs[np.where(r < 1.0)[0][0]]) if (r < 1.0).any() else np.nan,
                   first_q_below_0_5=float(qs[np.where(r < 0.5)[0][0]]) if (r < 0.5).any() else np.nan,
                   first_q_below_0_1=float(qs[np.where(r < 0.1)[0][0]]) if (r < 0.1).any() else np.nan,
                   spearman_q=spearman(r, qs),
                   down_steps=int((steps < 0).sum()), up_steps=int((steps > 0).sum()),
                   flat_steps=int((steps == 0).sum())))
FB = pd.DataFrame(fb)
FB.to_csv(f"{STEM}.firstbind.csv", index=False)
say(FB.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say("\n(down/up/flat steps count the 20 q->q+0.05 transitions; a MONOTONE bar has up_steps == 0.")
say(" spearman_q is the rank correlation of the bar's pass rate with q over the 21 rungs.)")

# ---------------------------------------------------------------- 4. which bar is binding
say("\n[4] WHICH BAR IS BINDING — among 4b FAILURES at each q, the share failing on each bar,")
say("    and the share where that bar is the SOLE failure (the true binding bar)")
bind = []
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    for q in QS:
        sub = A[(A.arm == arm) & (A.q == q)]
        fail = sub[~sub.pass4b]
        if not len(fail):
            bind.append(dict(arm=arm, q=q, n_fail=0, **{f"fails_{b}": np.nan for b in BARS},
                             **{f"sole_{b}": np.nan for b in BARS}))
            continue
        nb = (~fail[[f"bar_{b}" for b in BARS]]).sum(axis=1)
        row = dict(arm=arm, q=q, n_fail=int(len(fail)))
        for b in BARS:
            f = ~fail[f"bar_{b}"]
            row[f"fails_{b}"] = float(f.mean())
            row[f"sole_{b}"] = float((f & (nb == 1)).mean())
        bind.append(row)
BD = pd.DataFrame(bind)
BD.to_csv(f"{STEM}.binding.csv", index=False)
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    say(f"\n--- {arm} ---")
    say(BD[BD.arm == arm].drop(columns=["arm"]).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say("\nPOOLED over all q, per arm — share of all 4b failures failing on each bar:")
pool = []
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    fail = A[(A.arm == arm) & (~A.pass4b)]
    nb = (~fail[[f"bar_{b}" for b in BARS]]).sum(axis=1)
    d = dict(arm=arm, n_fail=len(fail))
    for b in BARS:
        f = ~fail[f"bar_{b}"]
        d[f"fails_{b}"] = float(f.mean()); d[f"sole_{b}"] = float((f & (nb == 1)).mean())
    pool.append(d)
say(pd.DataFrame(pool).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# ---------------------------------------------------------------- 5. rule 8 + both KEEP paths
say("\n[5] RULE 8 — n chosen per draw on IS Sharpe (<= 2016-12-31), read ONCE on 2017..end")
wf = []
for q in QS:
    sub = A[(A.q == q) & (A.arm.str.startswith("top"))]
    picks = sub.loc[sub.groupby("draw").IS_Sharpe.idxmax()]
    ew = A[(A.q == q) & (A.arm == "EWall")].set_index("draw")
    wf.append(dict(q=q, n_draws=len(picks),
                   pick_top10=float((picks.n == 10).mean()), pick_top20=float((picks.n == 20).mean()),
                   pick_top30=float((picks.n == 30).mean()),
                   OOS_CAGR=float(picks.OOS_CAGR.median()), OOS_Sharpe=float(picks.OOS_Sharpe.median()),
                   OOS_MaxDD=float(picks.OOS_MaxDD.median()),
                   EWall_OOS_Sharpe=float(ew.OOS_Sharpe.median()),
                   base_OOS_Sharpe=float(picks.base_OOS_Sharpe.median()),
                   base_OOS_CAGR=float(picks.base_OOS_CAGR.median()),
                   SPY_OOS_Sharpe=float(picks.SPY_OOS_Sharpe.median()),
                   SPY_OOS_CAGR=float(picks.SPY_OOS_CAGR.median()),
                   beats_base=float((picks.OOS_Sharpe > picks.base_OOS_Sharpe).mean()),
                   beats_SPY=float((picks.OOS_Sharpe > picks.SPY_OOS_Sharpe).mean()),
                   pass4b=float(picks.pass4b.mean()), pass4a=float(picks.pass4a.mean())))
W = pd.DataFrame(wf)
W.to_csv(f"{STEM}.walkforward.csv", index=False)
say(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
picks_all = A[A.arm.str.startswith("top")]
picks_all = picks_all.loc[picks_all.groupby(["q", "draw"]).IS_Sharpe.idxmax()]
say(f"\n  rule-8 chooser pooled over {len(picks_all)} draws: beats RULES v2 OOS on "
    f"{picks_all.eval('OOS_Sharpe > base_OOS_Sharpe').mean():.1%} of draws, beats SPY OOS on "
    f"{picks_all.eval('OOS_Sharpe > SPY_OOS_Sharpe').mean():.1%}; "
    f"4b passes {picks_all.pass4b.mean():.1%}, 4a passes {picks_all.pass4a.mean():.1%}")

# ---------------------------------------------------------------- 6. headline
say("\n[6] HEADLINE — is the 4b footprint MONOTONE in q?")
for arm in ["EWall"] + [f"top{n}" for n in NS]:
    g = C[C.arm == arm].sort_values("q")
    r = g["joint4b"].to_numpy()
    up = int((np.diff(r) > 0).sum())
    say(f"  {arm:7s}  joint 4b pass rate {r[0]:.2f} at q=0 -> {r[-1]:.2f} at q=1; "
        f"Spearman {spearman(r, g['q'].to_numpy()):+.3f}; "
        f"up-steps {up}/20 -> {'MONOTONE' if up == 0 else 'NOT monotone'}")
say(f"\n  total 4b passes: {int(A.pass4b.sum())} of {len(A)} arm-rows; "
    f"max q at which any arm passes 4b: {A[A.pass4b].q.max() if A.pass4b.any() else float('nan')}")
say(f"  total 4a passes: {int(A.pass4a.sum())} of {len(A)} arm-rows")
say(f"\ndone in {time.time()-t0:.1f}s")
Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")
