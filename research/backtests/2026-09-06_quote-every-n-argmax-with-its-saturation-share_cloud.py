#!/usr/bin/env python3
"""Idea 242 - "quote-every-n-argmax-with-its-saturation-share" (cloud, 2026-09-06).

The question
------------
Idea 240 found that the OOS argmax position count `n` tracks a panel's MEAN ELIGIBLE
COUNT at Spearman +0.926, and that "n=20" means two completely different things on two
panels: on STK20 99.3% of rebalance weeks cannot supply 20 eligible names, on SMALL484
0.9% cannot.  A published argmax quoted as a bare integer is therefore not comparable
across panels, and an argmax quoted AT OR PAST its panel's saturation point is not a
choice about book width at all -- it is the widest book the panel can build (and, under
idea 73's FIXED `GROSS/n` convention, a de-grossing dial wearing an n label).

This run does the back-fill idea 242 asks for, and then asks the one question that makes
the column worth carrying:

    Q1 (census, the deliverable): attach `mean eligible count` and `under-fill share` to
       every published position-count argmax in the record.  How many were quoted at or
       past their panel's saturation point?
    Q2 (does the column predict anything): among the recomputable cells, does under-fill
       share at the argmax predict the argmax's OOS shortfall against doing nothing?
    Q3 (rule 8): does a SATURATION-CAPPED chooser -- pick the IS argmax but only among n
       the panel can actually fill -- beat the plain IS argmax, the widest-n rule, a
       random dial and the do-nothing incumbent, out of sample?

Definitions (pre-registered here, before any OOS number was read)
----------------------------------------------------------------
For a panel P and a count n, on weekly rebalance dates only:
    n_elig_t     number of names passing the v1 eligibility gate (above 200d MA and
                 vol20 < 0.60) at date t.
    under-fill share u(P, n) = fraction of rebalance dates with n_elig_t < n.
    mean eligible count      = mean of n_elig_t.
    SATURATION POINT n_sat(P) = the largest n on the grid with u(P, n) <= 0.50, i.e. the
                 widest book the panel can fill in a majority of weeks.  0.50 is the one
                 pre-registered threshold; u at 0.25 and 0.75 are reported for every
                 panel so any other threshold can be read off the table.
    A quoted argmax is "AT OR PAST SATURATION" when u(P, n_argmax) > 0.50.

Two weighting conventions, both reported in full (idea 240's, verbatim):
    FIXED  w = GROSS / n on the top-n names       (idea 73's; under-filling DE-GROSSES)
    NORM   w = GROSS / min(n, n_elig)             (width dial, gross channel closed)

Census scope and its honest limits
----------------------------------
The census is MECHANICAL, not read out of prose: every committed grid CSV in
research/backtests/ is scanned for a position-count column (`n`, `top_n`, `n_names`,
`npos`, `count`) that (a) carries >= 3 distinct integer values inside [2, 500], (b) sits
beside a Sharpe column, and (c) comes from a script whose source actually ranks on that
count.  Files whose `n` is a sample size, a draw count or a block count are rejected by
(c) and the rejects are listed, with their reason, in `.census_rejects.csv` -- so the
denominator of "how many published argmaxes" is auditable rather than asserted.
A cell's panel is mapped to one of this run's 7 panels by name; cells whose panel cannot
be mapped are reported as `unmapped` and EXCLUDED from every share statistic rather than
guessed at.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (7)      2. n (6 values)
The weighting convention is a reported CONTROL on every point (both conventions, always),
not a third tuned dial.  The 0.50 saturation threshold is pre-registered, with the full
u-curve published so it is inspectable, not fitted.
Live grid = 7 panels x n in {5,10,20,30,40,60} x 2 conventions = 84 points, + 7 EWall
+ 7 v1 references = 98, ALL reported in `.grid.csv`.

Walk-forward (PROTOCOL rule 8) -- rules and directions fixed before any OOS read
    IS = 2009-2016, OOS = 2017-2026, read once.
    ISARGMAX   n = argmax IS Sharpe over the whole grid           (the dial as published)
    SATARGMAX  n = argmax IS Sharpe over {n : u_IS(P, n) <= 0.50} (the proposed column,
               used as a constraint; u computed on the IS window ONLY)
    WIDEST     n = 60, the grid top                               (idea 240's WIDEST60)
    NARROWEST  n = 5, the grid bottom                             (sign check)
    NOTHING    U56 / n=20, the project's incumbent book           (do-nothing control)
    RANDOM     mean OOS Sharpe over the 6 n values                (a coin flip on the dial)
    Reported per panel and pooled (equal-weight over panels), on BOTH conventions.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: every name list here is CURRENT constituents, one-directional.  It falls
hardest on STK20 / BSTK100 / SMALL484.  The small panel additionally drops any ticker
with max_1d_move >= 1.0 in data/small_meta.csv (bad splits/prints) before use.  Widening
n on a survivorship-selected list adds names known ex post to have survived, so any
"wider is better" reading is partly manufactured on this data.  Restated in the memo.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import ast
import json
import re
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [5, 10, 20, 30, 40, 60]
U_GRID = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 200]
SAT_TAU = 0.50                       # pre-registered saturation threshold
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
CONVS = ("FIXED", "NORM")
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)


# ---------------------------------------------------------------- panels (idea 240, verbatim + small hygiene)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep_small = [c for c in pxs.columns if c == "SPY" or c not in bad]
    dropped = pxs.shape[1] - len(keep_small)
    pxs = pxs[keep_small]

    etf36 = broad_g + sect_g + bfc_g
    etf24 = broad_g + sect_g
    b_stk = [t for t in px136.columns if t not in set(etf36)]
    s_stk = [c for c in pxs.columns if c != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    panels = {
        "U56":     sub(px56, list(px56.columns)),
        "ETF36":   sub(px56, etf36),
        "ETF24":   sub(px56, etf24),
        "STK20":   sub(px56, stk_g, tradable=stk_g),
        "B136":    sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL":   sub(pxs, s_stk, tradable=s_stk),
    }
    return panels, dropped


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, kind, n=None, conv="FIXED"):
    if kind == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(eligible_mask(px, tradable)).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    elig = eligible_mask(px, tradable)
    if kind == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    if conv == "FIXED":
        return sel * (GROSS / n)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def elig_series(px, tradable):
    """n_elig on weekly rebalance dates."""
    elig = eligible_mask(px, tradable)
    mask = rebalance_mask(px.index, FREQ)
    return elig[mask.values].sum(axis=1)


# ---------------------------------------------------------------- metrics helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan, ok.sum()
    xr = pd.Series(x[ok]).rank().values
    yr = pd.Series(y[ok]).rank().values
    if xr.std() == 0 or yr.std() == 0:
        return np.nan, ok.sum()
    return float(np.corrcoef(xr, yr)[0, 1]), int(ok.sum())


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- census over the committed record
COUNT_COLS = ("n", "top_n", "topn", "n_names", "npos", "n_pos", "count", "nn")
PANEL_COLS = ("panel", "universe", "corpus", "book", "panel_name", "uni")
SHARPE_COLS = ("Sharpe", "OOS_Sharpe", "IS_Sharpe", "mean_OOS_Sharpe")
# panel-name synonyms -> this run's panel keys
PANEL_MAP = {
    "u56": "U56", "universe.json": "U56", "universe": "U56", "56": "U56", "etf56": "U56",
    "etf36": "ETF36", "etf24": "ETF24", "stk20": "STK20", "megacap": "STK20", "mega": "STK20",
    "b136": "B136", "broad": "B136", "universe_broad.json": "B136", "broad136": "B136", "b100": "BSTK100",
    "bstk100": "BSTK100", "bstk": "BSTK100",
    "small": "SMALL", "small484": "SMALL", "small483": "SMALL", "small439": "SMALL",
    "small485": "SMALL", "smallcap": "SMALL",
}
# a count column is only a POSITION count if its own script ranks on it
RANK_PAT = re.compile(r"rank\s*\(|rank\s*<=|nlargest|argsort|<=\s*n\b|top[_ ]?n", re.I)


def script_for(csv_path):
    stem = csv_path.name.split(".")[0]
    p = csv_path.parent / f"{stem}.py"
    return p if p.exists() else None


def census(panels_u):
    """Scan every committed grid CSV for a position-count sweep; return (cells, rejects)."""
    cells, rejects = [], []
    src_cache = {}
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rejects.append(dict(file=f.name, col="", reason=f"unreadable:{type(e).__name__}"))
            continue
        if df.empty:
            rejects.append(dict(file=f.name, col="", reason="empty"))
            continue
        ccols = [c for c in df.columns if c in COUNT_COLS]
        if not ccols:
            continue
        scols = [c for c in df.columns if c in SHARPE_COLS]
        sp = script_for(f)
        if sp is None:
            rejects.append(dict(file=f.name, col=",".join(ccols), reason="no parent script"))
            continue
        if sp not in src_cache:
            src_cache[sp] = sp.read_text(errors="ignore")
        ranks = bool(RANK_PAT.search(src_cache[sp]))
        for c in ccols:
            v = pd.to_numeric(df[c], errors="coerce").dropna()
            uv = sorted(set(v.astype(int))) if len(v) and (v % 1 == 0).all() else []
            if len(uv) < 3:
                rejects.append(dict(file=f.name, col=c, reason=f"<3 distinct int values ({len(uv)})"))
                continue
            if min(uv) < 2 or max(uv) > 500:
                rejects.append(dict(file=f.name, col=c, reason=f"range {min(uv)}..{max(uv)} outside [2,500]"))
                continue
            if not scols:
                rejects.append(dict(file=f.name, col=c, reason="no Sharpe column beside it"))
                continue
            if not ranks:
                rejects.append(dict(file=f.name, col=c, reason="parent script never ranks on a count"))
                continue
            pcol = next((p for p in PANEL_COLS if p in df.columns), None)
            groups = df.groupby(df[pcol].astype(str)) if pcol else [("(all)", df)]
            for gname, g in groups:
                key = str(gname).strip().lower().replace("-", "").replace("_", "")
                pk = PANEL_MAP.get(key, "")
                for scol in scols:
                    gg = g[[c, scol]].apply(pd.to_numeric, errors="coerce").dropna()
                    if gg.empty or gg[c].nunique() < 3:
                        continue
                    best = gg.loc[gg[scol].idxmax()]
                    cells.append(dict(file=f.name, count_col=c, sharpe_col=scol,
                                      panel_raw=str(gname), panel=pk if pk else "unmapped",
                                      n_grid=len(sorted(set(gg[c].astype(int)))),
                                      n_min=int(gg[c].min()), n_max=int(gg[c].max()),
                                      n_argmax=int(best[c]), sharpe_at_argmax=float(best[scol])))
    return pd.DataFrame(cells), pd.DataFrame(rejects)


# ---------------------------------------------------------------- main
def main():
    panels, small_dropped = build_panels()

    print("=" * 200)
    print(f"Idea 242 quote-every-n-argmax-with-its-saturation-share (cloud) | {SCRIPT} | "
          f"{COST_BPS} bps, weekly, next-day execution")
    print("=" * 200)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
    print(f"small panel hygiene: dropped {small_dropped} tickers with max_1d_move >= 1.0 "
          f"(data/small_meta.csv); {len(panels['SMALL'][1])} tradable remain")

    # ---------------- (1) the saturation table
    ecs, ecs_is = {}, {}
    rows = []
    for k, (p, tr) in panels.items():
        e = elig_series(p, tr)
        ecs[k] = e
        ecs_is[k] = e.loc[:IS_END]
        rows.append(dict(panel=k, tradable=len(tr), start=str(p.index[0].date()), end=str(p.index[-1].date()),
                         mean_elig=e.mean(), med_elig=e.median(), p10_elig=e.quantile(0.10),
                         p90_elig=e.quantile(0.90), mean_elig_IS=ecs_is[k].mean()))
    pan = pd.DataFrame(rows).set_index("panel")

    ucurve = pd.DataFrame({k: [float((ecs[k] < n).mean()) for n in U_GRID] for k in panels},
                          index=U_GRID)
    ucurve.index.name = "n"

    def sat_point(k, tau=SAT_TAU, series=None):
        s = ecs[k] if series is None else series
        ok = [n for n in U_GRID if float((s < n).mean()) <= tau]
        return max(ok) if ok else 0

    pan["n_sat25"] = [sat_point(k, 0.25) for k in pan.index]
    pan["n_sat50"] = [sat_point(k, 0.50) for k in pan.index]
    pan["n_sat75"] = [sat_point(k, 0.75) for k in pan.index]
    pan["n_sat50_IS"] = [sat_point(k, 0.50, ecs_is[k]) for k in pan.index]

    print("\n" + "=" * 200)
    print("(1) PANELS AND SATURATION  (n_satXX = widest n the panel fills in >= 1-XX of weekly rebalances)")
    print("=" * 200)
    print(fmt(pan, 2))
    print("\nunder-fill share u(panel, n) = P(n_elig < n) on weekly rebalance dates, FULL SAMPLE:")
    print(fmt(ucurve, 3))
    ucurve.to_csv(OUT / f"{STEM}.ucurve.csv")
    pan.to_csv(OUT / f"{STEM}.panels.csv")

    # ---------------- (2) the live grid
    res, turn, wsum, hcnt = {}, {}, {}, {}
    jobs = [("EWall", None, "FIXED"), ("v1", None, "FIXED")]
    jobs += [("CAND", n, c) for c in CONVS for n in NS]
    for pk, (p, tr) in panels.items():
        for kind, n, conv in jobs:
            w = weights(p, tr, kind, n, conv)
            r = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            key = (pk, "EWall" if kind == "EWall" else ("v1" if kind == "v1" else f"CAND{n}"), conv)
            res[key] = r["returns"]; turn[key] = r["turnover"]
            wsum[key] = r["weights"].sum(axis=1)
            hcnt[key] = (r["weights"] > 1e-12).sum(axis=1)
        print(f"  ran {pk}")

    start56 = px56.index[260]
    print("\n--- harness sanity (universe.json window, must match published rows) ---")
    for key, want in [(("U56", "CAND20", "FIXED"), "idea 2 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                      (("U56", "v1", "FIXED"), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = res[key].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        print(f"  {key[0]}/{key[1]:<7} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  "
              f"halves {h1:.3f}/{h2:.3f}   [{want}]")

    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    print(f"\nCommon evaluation window: {start.date()} -> {end.date()}")
    spy = px56["SPY"].pct_change().fillna(0).loc[start:end]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    grid = []
    for pk in panels:
        base = res[(pk, "v1", "FIXED")].loc[start:end]
        for kind in ["EWall", "v1"] + [f"CAND{n}" for n in NS]:
            for conv in CONVS:
                if kind in ("EWall", "v1") and conv != "FIXED":
                    continue
                key = (pk, kind, conv)
                r = res[key].loc[start:end]
                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                m, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
                h1, h2 = half_sharpes(r)
                n = int(kind[4:]) if kind.startswith("CAND") else np.nan
                e = ecs[pk].loc[start:end]
                grid.append(dict(
                    panel=pk, book=kind, conv=conv, n=n,
                    mean_elig=e.mean(), mean_elig_IS=e.loc[:IS_END].mean(),
                    underfill=float((e < n).mean()) if kind.startswith("CAND") else np.nan,
                    underfill_IS=float((e.loc[:IS_END] < n).mean()) if kind.startswith("CAND") else np.nan,
                    saturated=bool((e < n).mean() > SAT_TAU) if kind.startswith("CAND") else False,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    turnover=turn[key].loc[start:end].sum() / ((end - start).days / 365.25),
                    gross=wsum[key].loc[start:end].mean(), held=hcnt[key].loc[start:end].mean(),
                    pass4a=verdict_4a(r, base),
                    fail4b=fail_4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(grid)
    grid["pass4b"] = grid["fail4b"] == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    print("\n" + "=" * 200)
    print("(2) LIVE GRID - every point reported (98 rows)")
    print("=" * 200)
    show = ["panel", "book", "conv", "n", "mean_elig", "underfill", "saturated", "gross", "held",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "OOS_MaxDD",
            "turnover", "pass4a", "pass4b", "fail4b"]
    print(fmt(grid[show], 3))
    ms = metrics(spy); sh1, sh2 = half_sharpes(spy)
    print(f"\nSPY reference: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {sh1:.3f}/{sh2:.3f}  OOS {metrics(spy_oos)['CAGR']:.1%}/"
          f"{metrics(spy_oos)['Sharpe']:.3f}/{metrics(spy_oos)['MaxDD']:.1%}")
    print(f"4b bars: Sharpe > SPY both halves and OOS; MaxDD <= {0.60*abs(ms['MaxDD']):.1%}; "
          f"CAGR >= {0.70*ms['CAGR']:.1%}")
    print(f"\n4a passes: {int(grid['pass4a'].sum())} of {len(grid)}   "
          f"4b passes: {int(grid['pass4b'].sum())} of {len(grid)}")
    for conv in CONVS:
        sub = grid[(grid.book.str.startswith("CAND")) & (grid.conv == conv)]
        print(f"  CAND/{conv}: 4a {int(sub.pass4a.sum())}/{len(sub)}  4b {int(sub.pass4b.sum())}/{len(sub)}")
    if grid["pass4b"].any():
        print("\n4b-passing points:")
        print(fmt(grid[grid.pass4b][show], 3))

    # ---------------- (2b) saturation makes grid points DUPLICATES
    print("\n" + "=" * 200)
    print("(2b) DUPLICATE POINTS - under NORM a saturated cell is the same book as the widest unsaturated one")
    print("=" * 200)
    dup_rows = []
    for pk in panels:
        for conv in CONVS:
            sub = grid[(grid.panel == pk) & (grid.conv == conv) & grid.book.str.startswith("CAND")]
            sub = sub.sort_values("n")
            seen = {}
            for _, r in sub.iterrows():
                sig = (round(r["CAGR"], 9), round(r["Sharpe"], 9), round(r["MaxDD"], 9))
                dup_of = seen.get(sig)
                if dup_of is None:
                    seen[sig] = int(r["n"])
                dup_rows.append(dict(panel=pk, conv=conv, n=int(r["n"]), underfill=r["underfill"],
                                     saturated=bool(r["saturated"]), duplicate_of=dup_of,
                                     Sharpe=r["Sharpe"], pass4b=bool(r["pass4b"])))
    dup = pd.DataFrame(dup_rows)
    dup.to_csv(OUT / f"{STEM}.duplicates.csv", index=False)
    d = dup[dup.duplicate_of.notna()]
    print(f"{len(d)} of {len(dup)} CAND points are byte-identical to a narrower n on the same panel "
          f"(all of them saturated: {bool(d['saturated'].all()) if len(d) else 'n/a'}); "
          f"{int(d['pass4b'].sum())} of the {int(dup['pass4b'].sum())} CAND 4b passes are such duplicates.")
    if len(d):
        print(fmt(d, 3))
    print("\n4b pass counts BEFORE and AFTER collapsing duplicated books:")
    for conv in CONVS:
        a = dup[dup.conv == conv]
        print(f"  {conv}: 4b {int(a['pass4b'].sum())}/{len(a)} raw -> "
              f"{int(a[a.duplicate_of.isna()]['pass4b'].sum())}/{int(a['duplicate_of'].isna().sum())} distinct books")

    # ---------------- (3) census over the record
    print("\n" + "=" * 200)
    print("(3) CENSUS - every committed position-count sweep in research/backtests/, back-filled")
    print("=" * 200)
    cen, rej = census(panels)
    rej.to_csv(OUT / f"{STEM}.census_rejects.csv", index=False)
    if cen.empty:
        print("no position-count sweeps found in the committed record")
    else:
        def u_at(row, is_window=False):
            pk = row["panel"]
            if pk not in ecs:
                return np.nan
            s = ecs_is[pk] if is_window else ecs[pk]
            return float((s < row["n_argmax"]).mean())

        cen["mean_elig"] = [ecs[p].mean() if p in ecs else np.nan for p in cen["panel"]]
        cen["underfill_at_argmax"] = [u_at(r) for _, r in cen.iterrows()]
        cen["n_sat50"] = [pan.loc[p, "n_sat50"] if p in pan.index else np.nan for p in cen["panel"]]
        cen["at_or_past_saturation"] = cen["underfill_at_argmax"] > SAT_TAU
        cen["argmax_at_grid_top"] = cen["n_argmax"] == cen["n_max"]
        cen.to_csv(OUT / f"{STEM}.census.csv", index=False)

        mapped = cen[cen.panel != "unmapped"]
        print(f"scanned {len(list(OUT.glob('*.csv')))} committed CSVs -> "
              f"{cen['file'].nunique()} files carry a position-count sweep, {len(cen)} argmax cells "
              f"({len(mapped)} on a mappable panel, {len(cen)-len(mapped)} unmapped and excluded).")
        print(f"rejects logged: {len(rej)} (see .census_rejects.csv); reject reasons:")
        if not rej.empty:
            print(rej["reason"].str.replace(r"\(.*\)", "", regex=True).value_counts().to_string())
        print("\nper-file census (mapped cells):")
        cols = ["file", "count_col", "sharpe_col", "panel", "n_min", "n_max", "n_argmax",
                "mean_elig", "underfill_at_argmax", "n_sat50", "at_or_past_saturation",
                "argmax_at_grid_top"]
        with pd.option_context("display.max_colwidth", 78):
            print(fmt(mapped[cols].sort_values(["panel", "file"]), 3))

        if len(mapped):
            k = int(mapped["at_or_past_saturation"].sum())
            print(f"\nHEADLINE: {k} of {len(mapped)} mapped published argmax cells "
                  f"({k/len(mapped):.1%}) are AT OR PAST their panel's saturation point "
                  f"(u > {SAT_TAU:.2f}); {int(mapped['argmax_at_grid_top'].sum())} sit at their own grid top.")
            print("by panel:")
            print(mapped.groupby("panel").agg(cells=("n_argmax", "size"),
                                              mean_n_argmax=("n_argmax", "mean"),
                                              mean_underfill=("underfill_at_argmax", "mean"),
                                              at_or_past=("at_or_past_saturation", "sum")).to_string())
            rho, nn = spearman(mapped["mean_elig"], mapped["n_argmax"])
            print(f"\nSpearman(panel mean eligible count, published n_argmax) over the census = "
                  f"{rho:+.3f} (N={nn})  [idea 240 reported +0.926 on its own 7 cells]")

    # ---------------- (4) does under-fill predict the argmax's OOS shortfall?
    print("\n" + "=" * 200)
    print("(4) Q2 - does under-fill share at the IS argmax predict its OOS shortfall vs doing nothing?")
    print("=" * 200)
    q2 = []
    for pk in panels:
        for conv in CONVS:
            sub = grid[(grid.panel == pk) & (grid.conv == conv) & grid.book.str.startswith("CAND")]
            pick = sub.loc[sub["IS_Sharpe"].idxmax()]
            nothing = grid[(grid.panel == "U56") & (grid.conv == conv) & (grid.n == 20)]
            nothing = nothing.iloc[0] if len(nothing) else grid[(grid.panel == "U56") & (grid.n == 20)].iloc[0]
            q2.append(dict(panel=pk, conv=conv, n_pick=int(pick["n"]),
                           underfill_IS_at_pick=pick["underfill_IS"],
                           saturated_pick=bool(pick["underfill_IS"] > SAT_TAU),
                           IS_Sharpe=pick["IS_Sharpe"], OOS_Sharpe=pick["OOS_Sharpe"],
                           best_OOS=sub["OOS_Sharpe"].max(),
                           regret=pick["OOS_Sharpe"] - sub["OOS_Sharpe"].max(),
                           vs_nothing=pick["OOS_Sharpe"] - nothing["OOS_Sharpe"],
                           vs_random=pick["OOS_Sharpe"] - sub["OOS_Sharpe"].mean()))
    q2 = pd.DataFrame(q2)
    q2.to_csv(OUT / f"{STEM}.q2.csv", index=False)
    print(fmt(q2, 3))
    for col in ("regret", "vs_nothing", "vs_random"):
        rho, nn = spearman(q2["underfill_IS_at_pick"], q2[col])
        print(f"  Spearman(under-fill at IS pick, {col:<11}) = {rho:+.3f} (N={nn})")
    sat, uns = q2[q2.saturated_pick], q2[~q2.saturated_pick]
    print(f"  saturated picks   N={len(sat)}  mean regret {sat['regret'].mean():+.4f}  "
          f"mean vs_nothing {sat['vs_nothing'].mean():+.4f}" if len(sat) else "  saturated picks   N=0")
    print(f"  unsaturated picks N={len(uns)}  mean regret {uns['regret'].mean():+.4f}  "
          f"mean vs_nothing {uns['vs_nothing'].mean():+.4f}" if len(uns) else "  unsaturated picks N=0")

    # ---------------- (5) rule 8 walk-forward
    print("\n" + "=" * 200)
    print(f"(5) RULE 8 WALK-FORWARD - IS <= {IS_END}, OOS >= {OOS_START} read once")
    print("=" * 200)
    wf_rows, pooled = [], {}
    for conv in CONVS:
        for rule in ("ISARGMAX", "SATARGMAX", "WIDEST", "NARROWEST", "NOTHING", "RANDOM"):
            per = []
            for pk in panels:
                sub = grid[(grid.panel == pk) & (grid.conv == conv) & grid.book.str.startswith("CAND")]
                if rule == "ISARGMAX":
                    pick = sub.loc[sub["IS_Sharpe"].idxmax()]
                elif rule == "SATARGMAX":
                    ok = sub[sub["underfill_IS"] <= SAT_TAU]
                    if ok.empty:                                # panel fills nothing: take narrowest
                        ok = sub[sub["n"] == sub["n"].min()]
                    pick = ok.loc[ok["IS_Sharpe"].idxmax()]
                elif rule == "WIDEST":
                    pick = sub[sub["n"] == max(NS)].iloc[0]
                elif rule == "NARROWEST":
                    pick = sub[sub["n"] == min(NS)].iloc[0]
                elif rule == "NOTHING":
                    pick = grid[(grid.panel == "U56") & (grid.conv == conv) & (grid.n == 20)].iloc[0]
                else:
                    pick = sub.mean(numeric_only=True)
                    pick["n"] = np.nan
                per.append(dict(rule=rule, conv=conv, panel=pk,
                                n_pick=(np.nan if rule == "RANDOM" else int(pick["n"])),
                                underfill_IS=pick["underfill_IS"],
                                OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                OOS_MaxDD=pick["OOS_MaxDD"]))
            per = pd.DataFrame(per)
            wf_rows.append(per)
            pooled[(conv, rule)] = dict(OOS_CAGR=per["OOS_CAGR"].mean(),
                                        OOS_Sharpe=per["OOS_Sharpe"].mean(),
                                        OOS_MaxDD=per["OOS_MaxDD"].mean())
    wf = pd.concat(wf_rows, ignore_index=True)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(fmt(wf, 3))

    pool = pd.DataFrame([dict(conv=c, rule=r, **v) for (c, r), v in pooled.items()])
    pool = pool.pivot(index="rule", columns="conv", values=["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"])
    print("\npooled OOS (equal weight over the 7 panels):")
    print(fmt(pool, 3))
    print(f"\nSPY OOS: {metrics(spy_oos)['CAGR']:.1%} / {metrics(spy_oos)['Sharpe']:.3f} / "
          f"{metrics(spy_oos)['MaxDD']:.1%}")
    v1o = res[("U56", "v1", "FIXED")].loc[OOS_START:end]
    print(f"RULES v1 OOS: {metrics(v1o)['CAGR']:.1%} / {metrics(v1o)['Sharpe']:.3f} / "
          f"{metrics(v1o)['MaxDD']:.1%}")

    print("\npaired SATARGMAX - ISARGMAX, per panel (the proposed column used as a constraint):")
    for conv in CONVS:
        a = wf[(wf.rule == "SATARGMAX") & (wf.conv == conv)].set_index("panel")
        b = wf[(wf.rule == "ISARGMAX") & (wf.conv == conv)].set_index("panel")
        d = (a["OOS_Sharpe"] - b["OOS_Sharpe"])
        chg = int((a["n_pick"] != b["n_pick"]).sum())
        print(f"  {conv}: mean {d.mean():+.4f}  wins {int((d>0).sum())} losses {int((d<0).sum())} "
              f"ties {int((d==0).sum())}  (picks differ in {chg}/{len(d)} panels)  "
              f"per-panel {dict((k, round(v,3)) for k,v in d.items())}")

    print("\n" + "=" * 200)
    print("Artefacts:", ", ".join(sorted(p.name for p in OUT.glob(f"{STEM}.*"))))
    print("=" * 200)


if __name__ == "__main__":
    main()
