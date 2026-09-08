#!/usr/bin/env python3
"""Idea 420 — does the IS-WINDOW DD CAP transfer at all?  (cloud lane, 2026-09-08)

QUESTION (QUEUE 420): idea 163 found the 4b-aware screen's core IS bars select arms whose
OOS drawdown is DEEPER by 3.30 pp — idea 128's window bias made concrete.  Measure the
transfer directly on the record's arm-rows: regress OOS MaxDD on IS MaxDD WITHIN CELL and
report slope and R2 per panel and rung against the same regression for CAGR and Sharpe.
"If the IS drawdown slope is ~0 while the CAGR slope is not, PROTOCOL's IS-window DD cap is
unenforceable and should be dropped from any IS screen."

DESIGN
  Part A — ARM-ROW CENSUS over every `research/backtests/*.csv` carrying, per arm, a matched
    (IS_M, OOS_M) pair.  Cells are discovered mechanically (a column is a cell label only if
    it is not a metric/mask column, has 2..40 values, and is NOT functionally determined by
    the arm); the full exclusion ledger is committed.  Within-cell (fixed-effects) transfer
    at 9 grid points: metric M in {MaxDD, CAGR, Sharpe} x transform in {demeaned level,
    within-cell rank, top-quartile hit rate}.  Two tuned parameters, all points reported.
    SEs clustered by parent file.  Split per panel and per cost rung.
  Part B — the DECISION the queue asks for, priced on REAL PRICES: a fresh 31-arm menu
    (band x gross x cadence + an ungated control) on u56 / broad136 / SMALL439 x 10 and 25
    bps, IS = through 2016-12-31, OOS = 2017-01-01.. read once.  Same regression on cells
    that did not exist when idea 163 ran, then the actionable comparison: an IS screen WITH
    its DD leg vs the SAME screen WITHOUT it — what the DD leg costs and buys out of sample,
    with both KEEP paths and fresh RULES v2 / SPY levels.

RULE 8 everywhere: Part A's slope is fitted on the record's first half by parent-file date
and read on the second half untouched; Part B's screens see only the IS window.
PROTOCOL: 10 bps anchor (25 bps also reported), next-day execution (engine), no shorting.
Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
from __future__ import annotations
import math
import re
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

STEM = "2026-09-08_does-the-IS-WINDOW-DD-CAP-transfer-at-all_cloud"
OUT = ROOT / "research" / "backtests"
METRICS = ["MaxDD", "CAGR", "Sharpe"]      # all "higher is better" as stored
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LINES.append(s)


def ncdf(z):
    return 0.5 * (1 + math.erf(z / np.sqrt(2)))


# ------------------------------------------------------------------ Part A: harvest
METRIC_PREFIX = re.compile(r"^(IS_|OOS_|pass|fail|adm_|m_|d_|uc_|sc_|U_|S_|C_|n_)")
METRIC_NAMES = {"CAGR", "Sharpe", "MaxDD", "Calmar", "Sortino", "Vol", "H1", "H2", "TO",
                "turnover", "Total", "Years", "WinRate", "breakeven", "cstar", "c_star"}
PANEL_COLS = ("panel", "universe", "u")
COST_COLS = ("cost", "cost_bps", "bps", "rung")


def id_columns(df: pd.DataFrame, armcol: str) -> list[str]:
    out = []
    for c in df.columns:
        if c == armcol or METRIC_PREFIX.match(c) or c in METRIC_NAMES:
            continue
        nu = df[c].nunique(dropna=False)
        if nu < 2 or nu > 40:
            continue
        if df[c].dtype.kind == "f" and nu > 12:
            continue
        if (df.groupby(armcol)[c].nunique(dropna=False) <= 1).all():
            continue                                   # arm parameter, not a cell label
        out.append(c)
    return out


def harvest() -> tuple[pd.DataFrame, pd.DataFrame]:
    """One row per (file, cell, arm) carrying every matched (IS_M, OOS_M) pair."""
    rows, ledger = [], []
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        rec = dict(file=f.name, status="", n_cells=0, n_arms=0)
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rec["status"] = f"unreadable:{type(e).__name__}"
            ledger.append(rec)
            continue
        armcol = "arm" if "arm" in df.columns else ("pick" if "pick" in df.columns else None)
        if armcol is None:
            rec["status"] = "no arm column"
            ledger.append(rec)
            continue
        mets = [m for m in METRICS if f"IS_{m}" in df.columns and f"OOS_{m}" in df.columns]
        if not mets:
            rec["status"] = "no matched IS_/OOS_ pair"
            ledger.append(rec)
            continue
        ids = id_columns(df, armcol)
        pcol = next((c for c in PANEL_COLS if c in df.columns), None)
        ccol = next((c for c in COST_COLS if c in df.columns), None)
        groups = df.groupby(ids, dropna=False, sort=True) if ids else [((), df)]
        nc = na = 0
        for key, cell in groups:
            nc += 1
            if cell[armcol].duplicated().any() or cell[armcol].nunique() < 4:
                continue                                # need >= 4 arms for a within-cell fit
            cid = f"{f.name}::" + ("|".join(map(str, key)) if ids else "ALL")
            for _, a in cell.iterrows():
                r = dict(file=f.name, date=f.name[:10], cell=cid, arm=str(a[armcol]),
                         panel=str(a[pcol]) if pcol else "n/a",
                         rung=str(a[ccol]) if ccol else "n/a", n_arms=int(len(cell)))
                keep = False
                for m in mets:
                    iv = pd.to_numeric(pd.Series([a[f"IS_{m}"]]), errors="coerce").iloc[0]
                    ov = pd.to_numeric(pd.Series([a[f"OOS_{m}"]]), errors="coerce").iloc[0]
                    if np.isfinite(iv) and np.isfinite(ov):
                        r[f"IS_{m}"], r[f"OOS_{m}"] = float(iv), float(ov)
                        keep = True
                if keep:
                    rows.append(r)
                    na += 1
        rec.update(status="ADMITTED" if na else "no usable cell", n_cells=nc, n_arms=na)
        ledger.append(rec)
    return pd.DataFrame(rows), pd.DataFrame(ledger)


# ------------------------------------------------------------------ transfer statistics
def within_cell_fit(df: pd.DataFrame, m: str) -> dict:
    """Fixed-effects (cell-demeaned) OLS of OOS_M on IS_M, with file-clustered SE."""
    d = df[["cell", "file", f"IS_{m}", f"OOS_{m}"]].dropna()
    if len(d) < 20:
        return dict(n=len(d), cells=0, slope=np.nan, R2=np.nan, t=np.nan, p=np.nan)
    d = d[d.groupby("cell")["cell"].transform("size") >= 4].copy()
    if len(d) < 20:
        return dict(n=len(d), cells=0, slope=np.nan, R2=np.nan, t=np.nan, p=np.nan)
    d["x"] = d[f"IS_{m}"] - d.groupby("cell")[f"IS_{m}"].transform("mean")
    d["y"] = d[f"OOS_{m}"] - d.groupby("cell")[f"OOS_{m}"].transform("mean")
    sxx = float((d.x ** 2).sum())
    if sxx <= 0:
        return dict(n=len(d), cells=d.cell.nunique(), slope=np.nan, R2=np.nan, t=np.nan, p=np.nan)
    b = float((d.x * d.y).sum() / sxx)
    d["e"] = d.y - b * d.x
    sst = float((d.y ** 2).sum())
    r2 = 1 - float((d.e ** 2).sum()) / sst if sst > 0 else np.nan
    # cluster on the parent file; fall back to the cell when there are too few files
    cl = "file" if d.file.nunique() >= 5 else "cell"
    ncl = d[cl].nunique()
    meat = float(((d.groupby(cl).apply(lambda g: float((g.x * g.e).sum()))) ** 2).sum())
    se = np.sqrt(meat) / sxx if meat > 0 else np.nan
    t = b / se if (se and np.isfinite(se) and se > 0 and ncl >= 5) else np.nan
    return dict(n=len(d), cells=int(d.cell.nunique()), files=int(d.file.nunique()),
                clusters=int(ncl), cluster_on=cl,
                slope=b, R2=r2, t=t, p=2 * (1 - ncdf(abs(t))) if np.isfinite(t) else np.nan)


def within_cell_rank(df: pd.DataFrame, m: str) -> dict:
    """Mean within-cell Spearman rho of OOS_M on IS_M, t over cells."""
    d = df[["cell", f"IS_{m}", f"OOS_{m}"]].dropna()
    rs = []
    for _, g in d.groupby("cell"):
        if len(g) >= 5 and g[f"IS_{m}"].nunique() > 1 and g[f"OOS_{m}"].nunique() > 1:
            rs.append(float(g[f"IS_{m}"].rank().corr(g[f"OOS_{m}"].rank())))
    rs = pd.Series(rs).dropna()
    if len(rs) < 3:
        return dict(cells=len(rs), mean_rho=np.nan, t=np.nan, frac_pos=np.nan)
    t = float(rs.mean() / (rs.std(ddof=1) / np.sqrt(len(rs)))) if rs.std(ddof=1) > 0 else np.nan
    return dict(cells=int(len(rs)), mean_rho=float(rs.mean()), t=t, frac_pos=float((rs > 0).mean()))


def quartile_hit(df: pd.DataFrame, m: str) -> dict:
    """P(arm is in the cell's OOS top quartile | it is in the cell's IS top quartile)."""
    d = df[["cell", f"IS_{m}", f"OOS_{m}"]].dropna()
    hit = tot = 0
    for _, g in d.groupby("cell"):
        if len(g) < 8:
            continue
        k = max(1, len(g) // 4)
        top_is = set(g[f"IS_{m}"].rank(ascending=False, method="first").nsmallest(k).index)
        top_oos = set(g[f"OOS_{m}"].rank(ascending=False, method="first").nsmallest(k).index)
        hit += len(top_is & top_oos)
        tot += k
    if tot == 0:
        return dict(n=0, hit=np.nan, base=np.nan, z=np.nan)
    p, p0 = hit / tot, 0.25
    z = (p - p0) / np.sqrt(p0 * (1 - p0) / tot)
    return dict(n=tot, hit=p, base=p0, z=z)



def level_bias(df: pd.DataFrame, m: str) -> dict:
    """Is the IS window's level a fair forecast of the OOS level, or only its ORDER?
    Reports the mean OOS-minus-IS shift and the share of arms that get WORSE out of sample."""
    d = df[[f"IS_{m}", f"OOS_{m}"]].dropna()
    if len(d) < 20:
        return dict(n=len(d), shift=np.nan, worse=np.nan, ratio=np.nan)
    s = d[f"OOS_{m}"] - d[f"IS_{m}"]
    ratio = float(d[f"OOS_{m}"].abs().mean() / d[f"IS_{m}"].abs().mean()) if d[f"IS_{m}"].abs().mean() else np.nan
    return dict(n=int(len(d)), shift=float(s.mean()), worse=float((s < 0).mean()), ratio=ratio)

def transfer_table(df: pd.DataFrame, label: str) -> pd.DataFrame:
    rows = []
    for m in METRICS:
        f = within_cell_fit(df, m)
        r = within_cell_rank(df, m)
        q = quartile_hit(df, m)
        lb = level_bias(df, m)
        rows.append(dict(scope=label, metric=m, n=f["n"], cells=f["cells"],
                         level_shift=lb["shift"], frac_worse=lb["worse"], level_ratio=lb["ratio"],
                         slope=f["slope"], R2=f["R2"], t_slope=f["t"], p_slope=f["p"],
                         rank_cells=r["cells"], mean_rho=r["mean_rho"], t_rho=r["t"],
                         frac_pos=r["frac_pos"], hit_n=q["n"], hit=q["hit"], hit_z=q["z"]))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ Part B: fresh grid
def ew_band_weights(px, band, gross, gated=True):
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


def win(r, lo=None, hi=None, prefix=""):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x)
    h = len(x) // 2
    return {f"{prefix}CAGR": m["CAGR"], f"{prefix}Sharpe": m["Sharpe"], f"{prefix}MaxDD": m["MaxDD"],
            f"{prefix}H1": metrics(x.iloc[:h])["Sharpe"], f"{prefix}H2": metrics(x.iloc[h:])["Sharpe"]}


def load_panels():
    P = {"u56": load_universe(), "broad136": load_universe(broad=True)}
    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["small439"] = small[[c for c in small.columns if c not in bad]]
    return P


def keep_paths(r, spy, base):
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


def fresh_grid(panels, costs=(10.0, 25.0)):
    rows, curves = [], {}
    for pname, px in panels.items():
        start = px.index[260]
        curves[(pname, "__SPY__")] = px["SPY"].pct_change().fillna(0.0).loc[start:]
        curves[(pname, "__V2__")] = backtest(px, rules_v2_weights(px), cost_bps=10.0,
                                             freq="W")["returns"].loc[start:]
        univ = px.drop(columns=["SPY"], errors="ignore") if pname == "small439" else px
        raw = {}
        for name, a in arm_menu():
            w = ew_band_weights(univ, a["band"], a["gross"], gated=a["gated"])
            res = backtest(px, w.reindex(columns=px.columns).fillna(0.0), cost_bps=0.0, freq=a["freq"])
            raw[name] = (res["returns"], res["turnover"])
        for c in costs:
            for name, a in arm_menu():
                r0, to = raw[name]
                r = (r0 - to * c / 1e4).loc[start:]          # rung identity (idea 352)
                curves[(pname, c, name)] = r
                row = dict(cell=f"{pname}@{c:g}", panel=pname, rung=str(c), arm=name,
                           band=a["band"], gross=a["gross"], freq=a["freq"], gated=a["gated"],
                           file="FRESH", date="2026-09-08", n_arms=31)
                row.update(win(r))
                row.update(win(r, hi=IS_END, prefix="IS_"))
                row.update(win(r, lo=OOS_START, prefix="OOS_"))
                row.update(keep_paths(r, curves[(pname, "__SPY__")], curves[(pname, "__V2__")]))
                rows.append(row)
    return pd.DataFrame(rows), curves


# ------------------------------------------------------------------ main
def main():
    say("=" * 100)
    say("IDEA 420 — does the IS-WINDOW DD CAP transfer at all?   (cloud, 2026-09-08)")
    say("=" * 100)

    say("\n## PART A — arm-row census: within-cell transfer of IS_M to OOS_M\n")
    cen, led = harvest()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    led.to_csv(OUT / f"{STEM}.ledger.csv", index=False)
    say(f"files scanned {len(led)} -> ADMITTED {int((led.status == 'ADMITTED').sum())}; "
        + "; ".join(f"{k} {v}" for k, v in led.status.value_counts().items() if k != "ADMITTED"))
    say(f"arm-rows {len(cen)}; cells {cen.cell.nunique()}; files {cen.file.nunique()}; "
        f"panels {sorted(cen.panel.unique())[:8]}; rungs {sorted(cen.rung.unique())[:8]}")
    for m in METRICS:
        say(f"  rows carrying a matched (IS_{m}, OOS_{m}) pair: {int(cen[f'IS_{m}'].notna().sum())}")

    say("\n### ALL 9 GRID POINTS — metric x transform, within cell (fixed effects), "
        "SE clustered by parent file")
    T = transfer_table(cen, "ALL")
    say(T.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("  reading: `slope` is d(OOS_M)/d(IS_M) within cell; `mean_rho` is the average "
        "within-cell Spearman; `hit` is P(OOS top quartile | IS top quartile), base 0.25.")

    say("\n### Per panel")
    tabs = [T]
    for pn, sub in cen.groupby("panel"):
        if sub.cell.nunique() >= 10:
            t = transfer_table(sub, f"panel={pn}")
            tabs.append(t)
            say(t.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("\n### Per cost rung")
    for rg, sub in cen.groupby("rung"):
        if sub.cell.nunique() >= 10:
            t = transfer_table(sub, f"rung={rg}")
            tabs.append(t)
            say(t.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    G = pd.concat(tabs, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.transfer.csv", index=False)

    say("\n### The queue's decision test — is the DD slope ~0 while the CAGR slope is not?")
    a = T.set_index("metric")
    say(f"  MaxDD  slope {a.loc['MaxDD', 'slope']:+.4f} (t {a.loc['MaxDD', 't_slope']:+.2f}), "
        f"R2 {a.loc['MaxDD', 'R2']:+.4f}, mean within-cell rho {a.loc['MaxDD', 'mean_rho']:+.3f}, "
        f"quartile hit {a.loc['MaxDD', 'hit']:.3f}")
    say(f"  CAGR   slope {a.loc['CAGR', 'slope']:+.4f} (t {a.loc['CAGR', 't_slope']:+.2f}), "
        f"R2 {a.loc['CAGR', 'R2']:+.4f}, mean within-cell rho {a.loc['CAGR', 'mean_rho']:+.3f}, "
        f"quartile hit {a.loc['CAGR', 'hit']:.3f}")
    say(f"  Sharpe slope {a.loc['Sharpe', 'slope']:+.4f} (t {a.loc['Sharpe', 't_slope']:+.2f}), "
        f"R2 {a.loc['Sharpe', 'R2']:+.4f}, mean within-cell rho {a.loc['Sharpe', 'mean_rho']:+.3f}, "
        f"quartile hit {a.loc['Sharpe', 'hit']:.3f}")

    say("\n### RULE 8 — fit on the record's FIRST half by parent-file date, read the SECOND untouched")
    dates = sorted(cen.date.unique())
    cut = dates[len(dates) // 2]
    A, B = cen[cen.date < cut], cen[cen.date >= cut]
    say(f"  IS: files dated < {cut} ({A.file.nunique()} files, {len(A)} arm-rows);  "
        f"OOS: >= {cut} ({B.file.nunique()} files, {len(B)} arm-rows)")
    wf = []
    for m in METRICS:
        fa, fb = within_cell_fit(A, m), within_cell_fit(B, m)
        ra, rb = within_cell_rank(A, m), within_cell_rank(B, m)
        wf.append(dict(metric=m, IS_slope=fa["slope"], IS_R2=fa["R2"], IS_t=fa["t"], IS_n=fa["n"],
                       OOS_slope=fb["slope"], OOS_R2=fb["R2"], OOS_t=fb["t"], OOS_n=fb["n"],
                       IS_rho=ra["mean_rho"], OOS_rho=rb["mean_rho"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ---------------- Part B
    say("\n\n## PART B — the same regression, and the DECISION, on fresh prices\n")
    panels = load_panels()
    for k, v in panels.items():
        say(f"  panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    say("  SMALL439 = the sub-$2B panel less the 44 names with max 1d move >= 1.0. "
        "SURVIVORSHIP: the small panel and universe_broad.json are current constituents only "
        "(data/SMALL_PANEL_README.md) — read the contrasts, not the levels.")
    fg, curves = fresh_grid(panels)
    fg.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  fresh grid: {len(fg)} arm-rows over {fg.cell.nunique()} cells "
        f"(IS through {IS_END}, OOS from {OOS_START}, both read once)")

    say("\n### Levels (freshly computed)")
    for pn in panels:
        ms = metrics(curves[(pn, "__SPY__")].loc[OOS_START:])
        mv = metrics(curves[(pn, "__V2__")].loc[OOS_START:])
        say(f"  {pn:9s} OOS  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}   "
            f"RULES v2@10bps {mv['CAGR']:.2%} / {mv['Sharpe']:.4f} / {mv['MaxDD']:.2%}   "
            f"[4b OOS bars: CAGR >= {0.70 * ms['CAGR']:.2%}, MaxDD >= {0.60 * ms['MaxDD']:.2%}]")

    say("\n### Transfer on the fresh cells (6 cells x 31 arms)")
    TF = transfer_table(fg, "FRESH")
    say(TF.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    per = []
    for cid, sub in fg.groupby("cell"):
        row = dict(cell=cid)
        for m in METRICS:
            row[f"rho_{m}"] = float(sub[f"IS_{m}"].rank().corr(sub[f"OOS_{m}"].rank()))
            x = sub[f"IS_{m}"] - sub[f"IS_{m}"].mean()
            y = sub[f"OOS_{m}"] - sub[f"OOS_{m}"].mean()
            row[f"slope_{m}"] = float((x * y).sum() / (x ** 2).sum())
        per.append(row)
    P = pd.DataFrame(per)
    P.to_csv(OUT / f"{STEM}.freshcells.csv", index=False)
    say(P.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))

    say("\n### THE DECISION — an IS screen WITH its DD leg vs the SAME screen WITHOUT it")
    say("  Screen (idea 163's S1 shape, computed on the IS window only): admit an arm whose "
        "IS H1 and H2 Sharpe both beat SPY's IS halves, IS CAGR >= 70% of SPY's IS CAGR, and "
        "(DD leg) IS MaxDD >= 60% of SPY's IS MaxDD.  NO-DD drops the last clause only.")
    dec = []
    for cid, sub in fg.groupby("cell"):
        pn = sub.panel.iloc[0]
        spy = curves[(pn, "__SPY__")]
        sm_is = win(spy, hi=IS_END, prefix="IS_")
        sm_oos = metrics(spy.loc[OOS_START:])
        base = (sub.IS_H1 > sm_is["IS_H1"]) & (sub.IS_H2 > sm_is["IS_H2"]) \
            & (sub.IS_CAGR >= 0.70 * sm_is["IS_CAGR"])
        ddleg = sub.IS_MaxDD >= 0.60 * sm_is["IS_MaxDD"]
        for lab, mask in (("WITH-DD", base & ddleg), ("NO-DD", base)):
            pool = sub[mask]
            if not len(pool):
                dec.append(dict(cell=cid, screen=lab, admitted=0, pick="(empty -> control)",
                                **{f"OOS_{k}": float(sub[sub.arm == "control"].iloc[0][f"OOS_{k}"])
                                   for k in METRICS}, pass4b_oos=bool(sub[sub.arm == "control"].iloc[0].pass4b_oos)))
                continue
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            dec.append(dict(cell=cid, screen=lab, admitted=int(len(pool)), pick=pick.arm,
                            OOS_MaxDD=float(pick.OOS_MaxDD), OOS_CAGR=float(pick.OOS_CAGR),
                            OOS_Sharpe=float(pick.OOS_Sharpe), pass4b_oos=bool(pick.pass4b_oos)))
        dec[-1]["SPY_OOS"] = f"{sm_oos['CAGR']:.2%}/{sm_oos['Sharpe']:.3f}/{sm_oos['MaxDD']:.2%}"
    D = pd.DataFrame(dec)
    D.to_csv(OUT / f"{STEM}.decision.csv", index=False)
    say(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    w = D[D.screen == "WITH-DD"].set_index("cell")
    n = D[D.screen == "NO-DD"].set_index("cell")
    diff = (w[["OOS_MaxDD", "OOS_CAGR", "OOS_Sharpe"]] - n[["OOS_MaxDD", "OOS_CAGR", "OOS_Sharpe"]])
    say("\n  WITH-DD minus NO-DD, per cell (pp for MaxDD/CAGR):")
    say(diff.assign(OOS_MaxDD=lambda d: d.OOS_MaxDD * 100, OOS_CAGR=lambda d: d.OOS_CAGR * 100)
        .to_string(float_format=lambda x: f"{x:+.3f}"))
    say(f"  mean dOOS MaxDD {diff.OOS_MaxDD.mean() * 100:+.2f} pp   "
        f"mean dOOS CAGR {diff.OOS_CAGR.mean() * 100:+.2f} pp   "
        f"mean dOOS Sharpe {diff.OOS_Sharpe.mean():+.4f}   "
        f"cells where the DD leg CHANGES the pick: {int((w.pick != n.pick).sum())} of {len(w)}   "
        f"cells where the DD leg EMPTIES the pool: {int((w.admitted == 0).sum())} of {len(w)}")

    say("\n### KEEP paths over the fresh grid")
    for rg, sub in fg.groupby("rung"):
        say(f"  @{float(rg):.0f} bps: 4a(v2) {int(sub.pass4a.sum())}/{len(sub)}  4b(full) "
            f"{int(sub.pass4b.sum())}/{len(sub)}  4b(OOS window) {int(sub.pass4b_oos.sum())}/{len(sub)}  "
            f"BOTH PATHS {int((sub.pass4a & sub.pass4b).sum())}/{len(sub)}")
    for pn, sub in fg.groupby("panel"):
        say(f"  {pn:9s}: 4a {int(sub.pass4a.sum())}/{len(sub)}  4b {int(sub.pass4b.sum())}/{len(sub)}  "
            f"4b(OOS) {int(sub.pass4b_oos.sum())}/{len(sub)}  BOTH {int((sub.pass4a & sub.pass4b).sum())}/{len(sub)}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    say(f"\nwrote {STEM}.{{census,ledger,transfer,walkforward,grid,freshcells,decision,console}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
