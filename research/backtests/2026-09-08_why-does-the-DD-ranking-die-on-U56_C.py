#!/usr/bin/env python3
"""Idea 422 — why does the DD ranking die on U56?   (lane C, 2026-09-08)

QUESTION (QUEUE 422): idea 420's within-cell MaxDD transfer slope is +1.085 (t +7.23) on
broad136 and +0.051 (t +0.45, ns) on U56, on the SAME 31-arm construction and the SAME cost
rungs.  Is that the panel's ETF SHARE, its NAME COUNT, or its 2020/2022 EPISODE STRUCTURE?

DESIGN
  The two panels differ on exactly two measurable axes: U56 is 36/56 ETFs (0.643) and
  broad136 is 36/136 (0.265); U56 holds 56 names and broad136 holds 136.  U56 is a strict
  subset of broad136, so both axes can be swept on ONE pooled name pool: 35 ETFs + 100
  stocks (SPY held out as the benchmark, never investable here).

  TWO TUNED PARAMETERS, all grid points reported:
      e = target ETF share in {0.00, 0.35, 0.65, 1.00}
      k = name count       in {20, 35, 56, 100}
  16 points; 12 are feasible against the pool (a point needs round(k*e) <= 35 ETFs and
  k-round(k*e) <= 100 stocks).  Infeasible points are reported as infeasible, not dropped.
  Each feasible point is drawn SEEDS=6 times (deterministic RNG seeded by (e,k,seed)); each
  draw x cost rung in {0, 10, 25} bps is one CELL of 31 arms — idea 420's exact arm menu
  (an ungated control + band x gross x cadence).

  TRANSFER STATISTIC (idea 420's, reused verbatim in form): within-cell (cell-demeaned) OLS
  of OOS_MaxDD on IS_MaxDD, SEs clustered on the sub-panel; plus the mean per-cell slope
  with t over cells, the mean within-cell Spearman rho, the top-quartile hit rate and the
  level bias.  IS = through 2016-12-31, OOS = 2017-01-01 on.

  THIRD LEG — EPISODE STRUCTURE: the OOS drawdown is recomputed with the 2020 crash
  (2020-02-15..2020-05-31) excised, with 2022 excised, and with both excised.  If U56's
  slope revives once an episode is removed, the death is episode structure and not
  composition.  This is an outcome DECOMPOSITION, not a third tuned dial: every variant is
  reported for every scope.

  REFERENCE PANELS: u56 and broad136 run under the same construction, each both WITH and
  WITHOUT SPY in the investable set (idea 420's fresh grid held SPY investable on these two
  panels; the sub-panels never do), so the reproduction is not confounded by that choice.

RULE 8 (required): the IS window is used ONLY to pick — on each panel the arm with the
shallowest IS MaxDD (the instrument under test) and, as comparands, the IS-Sharpe argmax and
the ungated control — and the pick is then read untouched on 2017-01-01.. against RULES v2
on the same panel and against SPY, with both KEEP paths (4a and 4b) evaluated on the OOS
window.  Nothing is retuned after the pick.

PROTOCOL: 10 bps anchor (0 and 25 bps also reported), next-day execution (engine), no
shorting, no leverage.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
from __future__ import annotations
import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "products" / "backtester"))
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_why-does-the-DD-ranking-die-on-U56_C"
OUT = ROOT / "research" / "backtests"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
RUNGS = (0.0, 10.0, 25.0)
E_GRID = (0.00, 0.35, 0.65, 1.00)
K_GRID = (20, 35, 56, 100)
SEEDS = 6
EPISODES = {
    "full": [],
    "ex2020": [("2020-02-15", "2020-05-31")],
    "ex2022": [("2022-01-01", "2022-12-31")],
    "exboth": [("2020-02-15", "2020-05-31"), ("2022-01-01", "2022-12-31")],
}
# the 36 ETFs of universe.json / universe_broad.json (SPY is the benchmark, held out)
ETFS = {"DBC", "DIA", "EEM", "EFA", "GDX", "GLD", "HYG", "IEF", "ITB", "IWM", "KRE", "LQD",
        "QQQ", "RSP", "SHY", "SLV", "SMH", "SPY", "TIP", "TLT", "UNG", "USO", "UUP", "VTI",
        "XBI", "XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"}
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(s)


def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ------------------------------------------------------------------ books
def ew_band_weights(px, band, gross, gated=True):
    """idea 420's book: equal weight over everything priced, optionally gated by the 200d
    +/-band state, gated-out weight to CASH."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if gated else ew


def arm_menu():
    arms = [("control", dict(band=0.0, gross=1.0, freq="W", gated=False))]
    for band in (0.0, 0.015, 0.03, 0.045, 0.06):
        for gross in (0.50, 0.75, 1.00):
            for freq in ("W", "M"):
                arms.append((f"b{band:g}-g{gross:.2f}-{freq}",
                             dict(band=band, gross=gross, freq=freq, gated=True)))
    return arms


ARMS = arm_menu()


# ------------------------------------------------------------------ metric helpers
def maxdd(r: pd.Series) -> float:
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def maxdd_excl(r: pd.Series, windows) -> float:
    """MaxDD of the same book with the named episodes' RETURNS excised (spliced out)."""
    keep = pd.Series(True, index=r.index)
    for lo, hi in windows:
        keep &= ~((r.index >= pd.Timestamp(lo)) & (r.index <= pd.Timestamp(hi)))
    return maxdd(r[keep])


def win(r, lo=None, hi=None, prefix=""):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x)
    h = len(x) // 2
    return {f"{prefix}CAGR": m["CAGR"], f"{prefix}Sharpe": m["Sharpe"], f"{prefix}MaxDD": m["MaxDD"],
            f"{prefix}H1": metrics(x.iloc[:h])["Sharpe"], f"{prefix}H2": metrics(x.iloc[h:])["Sharpe"]}


# ------------------------------------------------------------------ transfer statistics
# (form taken from 2026-09-08_does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud.py)
def within_cell_fit(df, xcol, ycol, cluster="panel_id"):
    d = df[["cell", cluster, xcol, ycol]].dropna()
    d = d[d.groupby("cell")["cell"].transform("size") >= 4].copy()
    if len(d) < 20:
        return dict(n=len(d), cells=0, slope=np.nan, R2=np.nan, t=np.nan, p=np.nan, clusters=0)
    d["x"] = d[xcol] - d.groupby("cell")[xcol].transform("mean")
    d["y"] = d[ycol] - d.groupby("cell")[ycol].transform("mean")
    sxx = float((d.x ** 2).sum())
    if sxx <= 0:
        return dict(n=len(d), cells=d.cell.nunique(), slope=np.nan, R2=np.nan, t=np.nan, p=np.nan,
                    clusters=0)
    b = float((d.x * d.y).sum() / sxx)
    d["e"] = d.y - b * d.x
    sst = float((d.y ** 2).sum())
    r2 = 1 - float((d.e ** 2).sum()) / sst if sst > 0 else np.nan
    ncl = d[cluster].nunique()
    meat = float(((d.groupby(cluster).apply(lambda g: float((g.x * g.e).sum()))) ** 2).sum())
    se = np.sqrt(meat) / sxx if meat > 0 else np.nan
    t = b / se if (se and np.isfinite(se) and se > 0 and ncl >= 5) else np.nan
    return dict(n=int(len(d)), cells=int(d.cell.nunique()), clusters=int(ncl),
                slope=b, R2=r2, t=t, p=2 * (1 - ncdf(abs(t))) if np.isfinite(t) else np.nan)


def per_cell_slopes(df, xcol, ycol):
    """One OLS slope per cell; mean and t over cells (no clustering assumption)."""
    out = []
    for c, g in df.groupby("cell"):
        d = g[[xcol, ycol]].dropna()
        if len(d) < 8 or d[xcol].std() == 0:
            continue
        x = d[xcol] - d[xcol].mean(); y = d[ycol] - d[ycol].mean()
        sxx = float((x ** 2).sum())
        if sxx <= 0:
            continue
        out.append(dict(cell=c, slope=float((x * y).sum() / sxx),
                        rho=float(d[xcol].rank().corr(d[ycol].rank()))))
    o = pd.DataFrame(out)
    if len(o) < 3:
        return dict(cells=len(o), mean_slope=np.nan, t_slope=np.nan, mean_rho=np.nan,
                    t_rho=np.nan, frac_pos=np.nan)
    def _t(s):
        return float(s.mean() / (s.std(ddof=1) / np.sqrt(len(s)))) if s.std(ddof=1) > 0 else np.nan
    return dict(cells=int(len(o)), mean_slope=float(o.slope.mean()), t_slope=_t(o.slope),
                mean_rho=float(o.rho.mean()), t_rho=_t(o.rho), frac_pos=float((o.rho > 0).mean()))


def quartile_hit(df, xcol, ycol):
    d = df[["cell", xcol, ycol]].dropna()
    hit = tot = 0
    for _, g in d.groupby("cell"):
        if len(g) < 8:
            continue
        kq = max(1, len(g) // 4)
        top_is = set(g[xcol].rank(ascending=False, method="first").nsmallest(kq).index)
        top_oos = set(g[ycol].rank(ascending=False, method="first").nsmallest(kq).index)
        hit += len(top_is & top_oos); tot += kq
    if tot == 0:
        return dict(hit_n=0, hit=np.nan, hit_z=np.nan)
    p = hit / tot
    return dict(hit_n=tot, hit=p, hit_z=(p - .25) / np.sqrt(.25 * .75 / tot))


def level_bias(df, xcol, ycol):
    d = df[[xcol, ycol]].dropna()
    if len(d) < 20:
        return dict(level_shift=np.nan, frac_worse=np.nan, level_ratio=np.nan)
    s = d[ycol] - d[xcol]
    den = d[xcol].abs().mean()
    return dict(level_shift=float(s.mean()), frac_worse=float((s < 0).mean()),
                level_ratio=float(d[ycol].abs().mean() / den) if den else np.nan)


def transfer_row(df, scope, ep, xcol="IS_MaxDD"):
    ycol = f"OOS_MaxDD_{ep}"
    r = dict(scope=scope, episode=ep)
    r.update(within_cell_fit(df, xcol, ycol))
    r.update(per_cell_slopes(df, xcol, ycol))
    r.update(quartile_hit(df, xcol, ycol))
    r.update(level_bias(df, xcol, ycol))
    return r


# ------------------------------------------------------------------ panels
def build_pool():
    px = load_universe(broad=True)               # 136 names, committed cache
    names = [c for c in px.columns if c != "SPY"]
    etf = sorted([c for c in names if c in ETFS])
    stk = sorted([c for c in names if c not in ETFS])
    return px, etf, stk


def draw(etf, stk, e, k, seed):
    n_e = int(round(k * e)); n_s = k - n_e
    if n_e > len(etf) or n_s > len(stk) or n_s < 0:
        return None
    rng = np.random.default_rng(hash((round(e * 100), k, seed)) % (2 ** 32))
    a = list(rng.choice(etf, n_e, replace=False)) if n_e else []
    b = list(rng.choice(stk, n_s, replace=False)) if n_s else []
    return sorted(a + b)


def run_panel(px_all, names, panel_id, meta):
    """31 arms x 3 rungs on one sub-panel.  Returns (rows, curves)."""
    cols = [c for c in names] + ["SPY"]
    px = px_all[cols]
    univ = px[names]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    v2 = backtest(px, rules_v2_weights(univ).reindex(columns=px.columns).fillna(0.0),
                  cost_bps=10.0, freq="W")["returns"].loc[start:]
    raw = {}
    for name, a in ARMS:
        w = ew_band_weights(univ, a["band"], a["gross"], gated=a["gated"])
        res = backtest(px, w.reindex(columns=px.columns).fillna(0.0), cost_bps=0.0, freq=a["freq"])
        raw[name] = (res["returns"], res["turnover"])
    rows, curves = [], {"__SPY__": spy, "__V2__": v2}
    for c in RUNGS:
        for name, a in ARMS:
            r0, to = raw[name]
            r = (r0 - to * c / 1e4).loc[start:]            # rung identity (idea 352)
            curves[(c, name)] = r
            row = dict(panel_id=panel_id, cell=f"{panel_id}@{c:g}", rung=c, arm=name,
                       band=a["band"], gross=a["gross"], freq=a["freq"], gated=a["gated"], **meta)
            row.update(win(r))
            row.update(win(r, hi=IS_END, prefix="IS_"))
            row.update(win(r, lo=OOS_START, prefix="OOS_"))
            ro = r.loc[OOS_START:]
            for ep, wins in EPISODES.items():
                row[f"OOS_MaxDD_{ep}"] = maxdd_excl(ro, wins) if wins else maxdd(ro)
            ri = r.loc[:IS_END]
            row["IS_MaxDD_full"] = maxdd(ri)
            rows.append(row)
    return rows, curves


# ------------------------------------------------------------------ rule 8
def keep_paths(r, base, spy):
    def bars(x, b, s):
        mx, mb, ms = metrics(x), metrics(b), metrics(s)
        h = len(x) // 2
        xh = (metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"])
        bh = (metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"])
        sh = (metrics(s.iloc[:h])["Sharpe"], metrics(s.iloc[h:])["Sharpe"])
        return (xh[0] > bh[0] and xh[1] > bh[1] and mx["MaxDD"] >= mb["MaxDD"],
                xh[0] > sh[0] and xh[1] > sh[1] and mx["Sharpe"] > ms["Sharpe"]
                and mx["MaxDD"] >= 0.60 * ms["MaxDD"] and mx["CAGR"] >= 0.70 * ms["CAGR"])
    a, b = bars(r, base, spy)
    ao, bo = bars(r.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:])
    return dict(pass4a=a, pass4b=b, pass4a_oos=ao, pass4b_oos=bo)


def walkforward(rows_df, curves, panel_id, meta):
    """Parameters chosen on the IS window ONLY, read on 2017-01-01.. untouched."""
    out = []
    g_all = rows_df[rows_df.panel_id == panel_id]
    spy, v2 = curves["__SPY__"], curves["__V2__"]
    for c in RUNGS:
        g = g_all[g_all.rung == c]
        picks = {
            "IS_MaxDD_argmax": g.loc[g.IS_MaxDD.idxmax(), "arm"],      # shallowest IS drawdown
            "IS_Sharpe_argmax": g.loc[g.IS_Sharpe.idxmax(), "arm"],
            "control": "control",
            "ORACLE_OOS_MaxDD": g.loc[g.OOS_MaxDD.idxmax(), "arm"],    # not a rule, a ceiling
        }
        for sel, arm in picks.items():
            r = curves[(c, arm)]
            ro, so, bo = r.loc[OOS_START:], spy.loc[OOS_START:], v2.loc[OOS_START:]
            mo, ms, mb = metrics(ro), metrics(so), metrics(bo)
            row = dict(panel_id=panel_id, rung=c, selector=sel, arm=arm, **meta,
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       SPY_OOS_CAGR=ms["CAGR"], SPY_OOS_Sharpe=ms["Sharpe"], SPY_OOS_MaxDD=ms["MaxDD"],
                       V2_OOS_CAGR=mb["CAGR"], V2_OOS_Sharpe=mb["Sharpe"], V2_OOS_MaxDD=mb["MaxDD"],
                       d_vs_ORACLE_MaxDD=np.nan)
            row.update(keep_paths(r, v2, spy))
            out.append(row)
        orc = metrics(curves[(c, picks["ORACLE_OOS_MaxDD"])].loc[OOS_START:])["MaxDD"]
        for row in out[-len(picks):]:
            row["d_vs_ORACLE_MaxDD"] = row["OOS_MaxDD"] - orc
    return out


# ------------------------------------------------------------------ main
PARENT = "2026-09-08_does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud"
# label spellings that name the SAME panel in idea 420's harvested census
CANON = {"u56": "u56(56)", "U56": "u56(56)", "universe.json(56)": "u56(56)",
         "broad": "broad136", "broad136": "broad136", "B136": "broad136",
         "BROAD136": "broad136", "universe_broad(136)": "broad136",
         "small": "small", "SMALL484": "small484", "SMALL439": "small439",
         "small439": "small439", "bstk100": "bstk100", "BSTK100": "bstk100", "ETF36": "etf36"}


def part0():
    """The premise's PROVENANCE: idea 420's per-panel slopes are per LABEL, not per panel."""
    say("\n\n## PART 0 — where the +0.051 comes from (idea 420's committed CSVs, re-read)\n")
    tp = OUT / f"{PARENT}.transfer.csv"
    cp = OUT / f"{PARENT}.census.csv"
    if not (tp.exists() and cp.exists()):
        say("  parent CSVs missing — Part 0 skipped")
        return None
    T0 = pd.read_csv(tp)
    m = T0[(T0.metric == "MaxDD") & (T0.scope.str.startswith("panel="))].copy()
    m["label"] = m.scope.str.replace("panel=", "", regex=False)
    say("  idea 420's per-PANEL-LABEL MaxDD transfer, as committed:")
    say(m[["label", "n", "cells", "slope", "R2", "t_slope", "hit"]]
        .sort_values("n", ascending=False)
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    C = pd.read_csv(cp)
    C["canon"] = C.panel.map(CANON).fillna("other")
    say("\n  the same census RE-PARTITIONED by canonical panel (label spellings merged):")
    rows = []
    for canon, g in C.groupby("canon"):
        g = g.copy(); g["panel_id"] = g.file
        r = dict(canon=canon, rows=len(g), files=g.file.nunique(),
                 labels=",".join(sorted({str(x) for x in g.panel.dropna().unique()})))
        r.update(within_cell_fit(g, "IS_MaxDD", "OOS_MaxDD", cluster="file"))
        rows.append(r)
    R = pd.DataFrame(rows).sort_values("rows", ascending=False)
    say(R[["canon", "labels", "rows", "n", "cells", "slope", "R2", "t", "p"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    R.to_csv(OUT / f"{STEM}.provenance.csv", index=False)
    return R


def main():
    say("=" * 100)
    say("IDEA 422 — why does the DD ranking die on U56?   (lane C, 2026-09-08)")
    say("=" * 100)
    part0()
    px_all, etf, stk = build_pool()
    say(f"pool: {len(etf)} ETFs + {len(stk)} stocks (SPY held out as benchmark), "
        f"{px_all.shape[0]} days {px_all.index[0].date()}..{px_all.index[-1].date()}")
    say(f"U56 = 36/56 ETFs (share 0.643, 55 investable ex-SPY -> 35/55 = 0.636); "
        f"broad136 = 36/136 (0.265)")
    say(f"IS <= {IS_END}, OOS >= {OOS_START}; rungs {RUNGS} bps; {len(ARMS)} arms/cell; "
        f"seeds {SEEDS}")

    all_rows, wf_rows, curve_store = [], [], {}

    # ---- reference panels (the two the queue names), SPY investable and not
    u56 = load_universe()
    refs = [
        ("REF_u56_SPYin", [c for c in u56.columns], dict(scope="REF u56 (SPY investable)",
                                                         e=0.643, k=56, seed=-1, kind="reference")),
        ("REF_u56_SPYout", [c for c in u56.columns if c != "SPY"],
         dict(scope="REF u56 (ex-SPY)", e=0.636, k=55, seed=-1, kind="reference")),
        ("REF_broad136_SPYin", [c for c in px_all.columns],
         dict(scope="REF broad136 (SPY investable)", e=0.265, k=136, seed=-1, kind="reference")),
        ("REF_broad136_SPYout", [c for c in px_all.columns if c != "SPY"],
         dict(scope="REF broad136 (ex-SPY)", e=0.259, k=135, seed=-1, kind="reference")),
    ]
    for pid, names, meta in refs:
        if pid.endswith("SPYin"):        # SPY investable (idea 420's u56/broad handling)
            rows, curves = run_panel_spyin(px_all, names, pid, meta)
        else:
            rows, curves = run_panel(px_all, [c for c in names if c != "SPY"], pid, meta)
        all_rows += rows; curve_store[pid] = curves
        say(f"  ran {pid}: {len(names)} names")

    # ---- the 4x4 grid
    feas = []
    for e in E_GRID:
        for k in K_GRID:
            n_e = int(round(k * e)); n_s = k - n_e
            ok = n_e <= len(etf) and 0 <= n_s <= len(stk)
            distinct = ok and not ((n_e == len(etf) and n_s == 0) or (n_s == len(stk) and n_e == 0))
            feas.append(dict(e=e, k=k, n_etf=n_e, n_stk=n_s, feasible=ok,
                             seed_variation=distinct,
                             seeds=(SEEDS if distinct else (1 if ok else 0))))
    F = pd.DataFrame(feas)
    say("\n### GRID FEASIBILITY (all 16 points reported)")
    say(F.to_string(index=False))

    for _, row in F[F.feasible].iterrows():
        e, k, ns = float(row.e), int(row.k), int(row.seeds)
        for s in range(ns):
            names = draw(etf, stk, e, k, s)
            pid = f"e{e:.2f}_k{k}_s{s}"
            meta = dict(scope=f"e={e:.2f} k={k}", e=e, k=k, seed=s, kind="grid")
            rows, curves = run_panel(px_all, names, pid, meta)
            all_rows += rows; curve_store[pid] = curves
        say(f"  ran e={e:.2f} k={k}: {ns} sub-panel(s) x {len(ARMS)} arms x {len(RUNGS)} rungs")

    G = pd.DataFrame(all_rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\ngrid: {len(G)} arm-rows over {G.cell.nunique()} cells, {G.panel_id.nunique()} panels")

    # ---- transfer per scope x episode
    T = []
    for scope, g in G.groupby("scope"):
        for ep in EPISODES:
            T.append(transfer_row(g, scope, ep))
    for ep in EPISODES:                                   # pooled over the whole grid
        T.append(transfer_row(G[G.kind == "grid"], "ALL GRID SUB-PANELS", ep))
    T = pd.DataFrame(T)
    T.to_csv(OUT / f"{STEM}.transfer.csv", index=False)

    say("\n### PART 1 — REPRODUCTION on the two panels the queue names (episode = full)")
    cols = ["scope", "n", "cells", "slope", "t", "R2", "mean_slope", "t_slope", "mean_rho",
            "frac_pos", "hit", "level_shift", "frac_worse", "level_ratio"]
    say(T[(T.episode == "full") & (T.scope.str.startswith("REF"))][cols]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n### PART 2 — the 2-parameter grid (episode = full), ALL feasible points")
    sub = T[(T.episode == "full") & (~T.scope.str.startswith("REF"))].copy()
    say(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n### PART 2b — slope surface: rows = ETF share e, cols = name count k")
    surf = sub[sub.scope.str.startswith("e=")].copy()
    surf["e"] = surf.scope.str.extract(r"e=([0-9.]+)").astype(float)
    surf["k"] = surf.scope.str.extract(r"k=(\d+)").astype(int)
    for stat in ("slope", "mean_rho", "hit"):
        say(f"\n  {stat}:")
        say(surf.pivot(index="e", columns="k", values=stat)
            .to_string(float_format=lambda x: f"{x:+.3f}"))

    # ---- which dial explains the slope?
    d = surf.dropna(subset=["slope"]).copy()
    dec = []
    for lab, X in (("e only", ["e"]), ("k only", ["k"]), ("e + k", ["e", "k"])):
        A = np.column_stack([np.ones(len(d))] + [d[c].values.astype(float) for c in X])
        y = d.slope.values
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        yhat = A @ beta
        r2 = 1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        rec = dict(model=lab, n=len(d), R2=r2, const=beta[0])
        for i, c in enumerate(X):
            rec[f"b_{c}"] = beta[i + 1]
        dec.append(rec)
    # per-cell slopes regressed on e and k, with a t (many more points)
    cellslopes = []
    for (scope, pid, rung), g in G[G.kind == "grid"].groupby(["scope", "panel_id", "rung"]):
        dd = g[["IS_MaxDD", "OOS_MaxDD"]].dropna()
        if len(dd) < 8 or dd.IS_MaxDD.std() == 0:
            continue
        x = dd.IS_MaxDD - dd.IS_MaxDD.mean(); y = dd.OOS_MaxDD - dd.OOS_MaxDD.mean()
        cellslopes.append(dict(scope=scope, panel_id=pid, rung=rung,
                               e=float(g.e.iloc[0]), k=int(g.k.iloc[0]),
                               slope=float((x * y).sum() / (x ** 2).sum())))
    CS = pd.DataFrame(cellslopes)
    if len(CS) > 5:
        A = np.column_stack([np.ones(len(CS)), CS.e.values, CS.k.values.astype(float)])
        y = CS.slope.values
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        res = y - A @ beta
        # cluster on sub-panel
        XtX_inv = np.linalg.pinv(A.T @ A)
        meat = np.zeros((3, 3))
        for _, gg in pd.DataFrame(A, columns=["c", "e", "k"]).assign(
                res=res, pid=CS.panel_id.values).groupby("pid"):
            u = (gg[["c", "e", "k"]].values * gg.res.values[:, None]).sum(axis=0)
            meat += np.outer(u, u)
        V = XtX_inv @ meat @ XtX_inv
        se = np.sqrt(np.diag(V))
        r2 = 1 - (res ** 2).sum() / ((y - y.mean()) ** 2).sum()
        dec.append(dict(model="per-cell slope ~ e + k (clustered on sub-panel)", n=len(CS), R2=r2,
                        const=beta[0], b_e=beta[1], b_k=beta[2],
                        t_e=beta[1] / se[1], t_k=beta[2] / se[2]))
    D = pd.DataFrame(dec)
    D.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    CS.to_csv(OUT / f"{STEM}.cellslopes.csv", index=False)
    say("\n### PART 3 — which dial prices the slope?")
    say(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n### PART 4 — EPISODE STRUCTURE (does excising 2020 / 2022 revive the ranking?)")
    ep_tab = T.pivot(index="scope", columns="episode", values="slope")[list(EPISODES)]
    say(ep_tab.to_string(float_format=lambda x: f"{x:+.3f}"))
    say("\n  same table, top-quartile hit rate (base 0.25):")
    say(T.pivot(index="scope", columns="episode", values="hit")[list(EPISODES)]
        .to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- rule 8
    say("\n### PART 5 — RULE 8 WALK-FORWARD (IS-only picks read on 2017-01-01..)")
    for pid, curves in curve_store.items():
        meta = G[G.panel_id == pid].iloc[0][["scope", "e", "k", "seed", "kind"]].to_dict()
        wf_rows += walkforward(G, curves, pid, meta)
    W = pd.DataFrame(wf_rows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    ref = W[(W.kind == "reference") & (W.rung == 10.0)]
    say(ref[["scope", "selector", "arm", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "V2_OOS_Sharpe", "V2_OOS_MaxDD", "SPY_OOS_CAGR", "SPY_OOS_Sharpe", "SPY_OOS_MaxDD",
             "d_vs_ORACLE_MaxDD", "pass4a_oos", "pass4b_oos"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  grid sub-panels, mean over sub-panels by selector and rung "
        "(d_vs_ORACLE_MaxDD: 0 = the IS pick found the OOS-shallowest arm)")
    gw = W[W.kind == "grid"].groupby(["rung", "selector"]).agg(
        n=("OOS_MaxDD", "size"), OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), d_ORACLE=("d_vs_ORACLE_MaxDD", "mean"),
        p4a=("pass4a_oos", "mean"), p4b=("pass4b_oos", "mean")).reset_index()
    say(gw.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  the SAME table split by ETF share e (rung 10 bps, IS_MaxDD selector) — "
        "does the IS-DD pick get worse as the panel gets more ETF?")
    hi = W[(W.kind == "grid") & (W.rung == 10.0) & (W.selector == "IS_MaxDD_argmax")]
    say(hi.groupby(["e", "k"]).agg(n=("OOS_MaxDD", "size"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                                   d_ORACLE=("d_vs_ORACLE_MaxDD", "mean"),
                                   OOS_Sharpe=("OOS_Sharpe", "mean"),
                                   p4b=("pass4b_oos", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))

    K = W[["scope", "panel_id", "rung", "selector", "arm", "pass4a", "pass4b",
           "pass4a_oos", "pass4b_oos"]]
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"\n  KEEP paths over all {len(W)} walk-forward rows: "
        f"4a {int(W.pass4a.sum())}, 4b {int(W.pass4b.sum())}, "
        f"4a_oos {int(W.pass4a_oos.sum())}, 4b_oos {int(W.pass4b_oos.sum())}")

    F.to_csv(OUT / f"{STEM}.feasibility.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES))
    say(f"\nwrote {STEM}.{{grid,transfer,decomp,cellslopes,walkforward,keeppaths,feasibility,console}}")


def run_panel_spyin(px_all, names, panel_id, meta):
    """Reference variant where SPY is INVESTABLE (idea 420's u56/broad handling)."""
    px = px_all[names]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
    raw = {}
    for name, a in ARMS:
        w = ew_band_weights(px, a["band"], a["gross"], gated=a["gated"])
        res = backtest(px, w, cost_bps=0.0, freq=a["freq"])
        raw[name] = (res["returns"], res["turnover"])
    rows, curves = [], {"__SPY__": spy, "__V2__": v2}
    for c in RUNGS:
        for name, a in ARMS:
            r0, to = raw[name]
            r = (r0 - to * c / 1e4).loc[start:]
            curves[(c, name)] = r
            row = dict(panel_id=panel_id, cell=f"{panel_id}@{c:g}", rung=c, arm=name,
                       band=a["band"], gross=a["gross"], freq=a["freq"], gated=a["gated"], **meta)
            row.update(win(r)); row.update(win(r, hi=IS_END, prefix="IS_"))
            row.update(win(r, lo=OOS_START, prefix="OOS_"))
            ro = r.loc[OOS_START:]
            for ep, wins in EPISODES.items():
                row[f"OOS_MaxDD_{ep}"] = maxdd_excl(ro, wins) if wins else maxdd(ro)
            row["IS_MaxDD_full"] = maxdd(r.loc[:IS_END])
            rows.append(row)
    return rows, curves


if __name__ == "__main__":
    main()
