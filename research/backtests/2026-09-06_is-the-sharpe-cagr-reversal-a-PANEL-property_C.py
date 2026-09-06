#!/usr/bin/env python3
"""Idea 271 - "is-the-sharpe-cagr-reversal-a-PANEL-property-not-a-width-one" (lane C, 2026-09-06).

The question
------------
Idea 269C set the concentration ratio r = n / n_elig equal across panels and found the
EWall-vs-ranked Sharpe/CAGR reversal share runs

        B136 6/7,  BSTK100 6/7,  U56 4/7,  ETF36 2/7,  SMALL439 0/7

i.e. AT MATCHED WIDTH the five panels disagree 0.00 vs 1.00 in 6 of 7 rows.  Its verdict
was "it is the panel that decides, not the book's width".  That is a negative result about
r; it is not yet a positive result about panels.  The queue asks the positive form:

    regress the matched-ratio reversal indicator on panel characteristics computable
    BEFORE any backtest - breadth, cross-sectional return dispersion, mean pairwise
    correlation and vol of the eligible set - and report whether the panel-level share
    is predictable at all.

Why the parent's five panels cannot answer it, and what this run does instead
----------------------------------------------------------------------------
Four regressors on five observations is a rank-deficient fit with zero residual degrees
of freedom: any four-characteristic model reproduces 5 panel shares EXACTLY and says
nothing.  The design therefore ENLARGES THE PANEL COUNT rather than the regressor count.
A pre-registered pool of random SUB-PANELS is drawn from the five sources - each sub-panel
is itself a panel with its own breadth, dispersion, correlation and vol - and the whole
matched-ratio grid is re-run on every one.  This is idea 78/83's random sub-panel channel
used as a design device, not as a null.

    POOL (pre-registered, seeded, fixed before any number was read)
      5 NAMED panels  : U56, B136, BSTK100, SMALL439, ETF36 - idea 269C's build_panels()
                        imported verbatim, so its published cells reproduce inside this run
      up to 50 SUB    : each SOURCE in {U56, B136, BSTK100, SMALL439, ETF36} x
                        k_frac in {0.25, 0.40, 0.55, 0.70, 0.85} of the source's tradable
                        names x seed in {0, 1}, uniform draw without replacement, subject
                        to k >= 12 (this drops ETF36's two 0.25 draws, k=9, so the pool is
                        48 sub-panels + 5 named = 53).  SPY is carried as the benchmark
                        column only and is NOT tradable in a sub-panel (it is tradable in
                        NAMED U56/B136, exactly as idea 269C had it).
      = 53 panels x 7 pre-registered ratios = 371 reversal cells.  On narrow panels two
      adjacent ratios can round to the same n (r*=0.05 and 0.10 both give n=1 at
      n_elig<=14); those cells are DEGENERATE duplicates by construction, are counted and
      reported, and are left in place because idea 269C's construction is what is being
      extended.

Panel characteristics (all four are functions of prices and the gate ONLY - no backtest,
no return stream, no arm; each is computed twice, once on the FULL sample and once on the
IS window alone, so the rule-8 leg never sees an OOS-informed regressor)
      breadth  mean over weekly rebalance days of n_elig,t / k          (how much the gate admits)
      disp     mean over rebalance days of the cross-sectional sd of trailing 63d returns
               among the ELIGIBLE names                                  (return dispersion)
      corr     mean off-diagonal pairwise correlation of daily returns over the tradable set
      evol     mean over rebalance days of the cross-sectional mean vol20 of eligible names
      controls k (panel width) and n_elig (median eligible count) - reported, and the model
               is refitted with them to show what the four named characteristics add.

Grid, imported verbatim from idea 269C (weekly, next-day, 10 bps, gate = above-200d AND
vol20 < 0.60, ranking key = the composite WITHOUT the vol scaler, every arm gross-matched
at 0.75; 0 bps carried as a DIAGNOSTIC column only, never selected on):
      EWall   every eligible name, equal weight   (the un-ranked book)
      FWD-n   top-n by the composite key,  n = round(r* * n_elig),  r* in
              {0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00}
      v1      RULES v1 as live pre-2026-09-06 (continuity row)
      v2      RULES v2, the live book (the 4a comparand)
Reversal is idea 269C's epsilon rule unchanged: sign(dS) != sign(dC) with |dS| > 0.005 and
|dC| > 5 bps/yr, where dS = Sharpe(EWall) - Sharpe(FWD-n) and dC likewise for CAGR.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (55)      2. target ratio r* (7)
The characteristics are measured, not tuned; the arm axis is the hypothesis; the cost rung
is fixed at PROTOCOL's 10 bps.  ALL 1100 grid points and ALL 385 reversal cells are written.

Walk-forward (PROTOCOL rule 8), pre-registered with direction before any OOS read
    IS = 2009-01-01..2016-12-31 chooses; OOS = 2017-01-01..end read ONCE.
    (i)  THE RELATIONSHIP.  The characteristic model is fitted on IS-window characteristics
         against IS-window reversals, then applied ONCE to OOS-window reversals.  Accuracy
         against the OOS majority base rate, and against three rivals fitted the same way:
         CONST (IS majority), SOURCE (per-source IS majority) and idea 269C's R_THRESH
         (r < th).  The whole threshold grid is printed.  A leave-one-SOURCE-out fit is
         reported beside it, because the question is whether a genuinely NEW panel family
         is predictable, not whether neighbours of a fitted panel are.
    (ii) THE BOOK.  CSEL (narrowest n whose fitted reversal probability is below the
         threshold) against EWALL (do nothing), FWD20 (incumbent), S_SHARPE, S_CAGR,
         RULES v1, RULES v2 and SPY, pooled equal-weight over the five NAMED panels so the
         numbers sit directly beside idea 269C's published pooled row.

Verdicts (both KEEP paths, on every one of the 1100 grid points)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
        The v1 comparand is carried as a second column for continuity with the pre-
        2026-09-06 record.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json, the megacap cut and the small panel are CURRENT
constituents, and every sub-panel is a subset of one of them, so the bias is inherited
whole.  The un-ranked book holds everything and so takes the full survivorship premium
while a ranked book can only redistribute it: the bias runs TOWARD reversals, i.e. toward
finding MORE structure than a live universe would have shown.  Any "predictable" verdict
here is therefore an upper bound; a "not predictable" verdict is conservative.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import zlib
import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
DIAG_BPS = 0
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
BAND_V2 = 0.03
RATIOS = [0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
EPS_S, EPS_C = 0.005, 0.0005            # idea 259/269's, unchanged
K_FRACS = [0.25, 0.40, 0.55, 0.70, 0.85]
SEEDS = [0, 1]
K_MIN = 12
CHARS = ["breadth", "disp", "corr", "evol"]
CONTROLS = ["k", "n_elig"]

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 800)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 4:
        return np.nan, np.nan, n
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, np.nan, n
    rho = float(np.corrcoef(rx, ry)[0, 1])
    t = rho * np.sqrt((n - 2) / max(1e-12, 1 - rho ** 2))
    return rho, t, n


# ---------------------------------------------------------------- OLS with (cluster) SEs
def ols(y, X, names, cluster=None):
    """Least squares with a constant already in X. Returns tidy frame + R2.
    cluster: array of group labels -> cluster-robust sandwich SEs."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, p = X.shape
    XtX = X.T @ X
    XtXi = np.linalg.pinv(XtX)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ss_res = float(e @ e)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    if cluster is None:
        dof = max(1, n - p)
        V = XtXi * (ss_res / dof)
    else:
        cl = pd.Series(np.asarray(cluster))
        meat = np.zeros((p, p))
        for _, idx in cl.groupby(cl).groups.items():
            ii = np.asarray(idx)
            Xg, eg = X[ii], e[ii]
            u = Xg.T @ eg
            meat += np.outer(u, u)
        G = cl.nunique()
        adj = (G / max(1, G - 1)) * ((n - 1) / max(1, n - p))
        V = XtXi @ meat @ XtXi * adj
    se = np.sqrt(np.maximum(np.diag(V), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    adj_r2 = 1 - (1 - r2) * (n - 1) / max(1, n - p) if np.isfinite(r2) else np.nan
    return (pd.DataFrame(dict(term=names, coef=b, se=se, t=t)).set_index("term"),
            r2, adj_r2, n, b)


def zscore_fit(df, cols):
    mu = df[cols].mean()
    sd = df[cols].std(ddof=0).replace(0, 1.0)
    return mu, sd


def design(df, cols, mu, sd):
    Z = (df[cols] - mu) / sd
    return np.column_stack([np.ones(len(df))] + [Z[c].to_numpy() for c in cols])


# ============================================================ panels (idea 269C verbatim)
def build_named():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    named = {
        "U56": sub(px56, [c for c in px56.columns]),
        "B136": sub(px136, [c for c in px136.columns]),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL439": sub(pxs, s_stk, tradable=s_stk),
        "ETF36": sub(px136, etf36, tradable=etf36),
    }
    return named, sub


def build_pool():
    """5 named panels + 50 pre-registered seeded sub-panels."""
    named, sub = build_named()
    pool = {}
    for nm, (px, tr) in named.items():
        pool[nm] = dict(px=px, tradable=tr, source=nm, kind="NAMED", k=len(tr), seed=-1,
                        k_frac=1.0)
    for src, (px, tr) in named.items():
        base = sorted(tr - {"SPY"}) if src in ("U56", "B136") else sorted(tr)
        for kf in K_FRACS:
            k = int(round(kf * len(base)))
            if k < K_MIN or k >= len(base):
                continue
            for sd in SEEDS:
                # zlib.crc32, NOT hash(): Python string hashing is salted per process
                seed = zlib.crc32(f"{src}|{kf:.2f}|{sd}".encode()) % (2 ** 32)
                rng = np.random.default_rng(seed)
                pick = sorted(rng.choice(np.array(base), size=k, replace=False).tolist())
                p, t = sub(px, pick, tradable=pick)
                pool[f"{src}~{kf:.2f}~s{sd}"] = dict(px=p, tradable=t, source=src,
                                                     kind="SUB", k=k, seed=sd, k_frac=kf)
    return pool


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, arm, n=None, elig=None, key=None, s_v1=None):
    if arm == "v1":
        rank = s_v1.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if arm == "v2":
        e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        for c in px.columns:
            if c in tradable:
                e[c] = px[c].notna().astype(float)
        ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND_V2), 0.0)
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
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


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ==================================================== panel characteristics (pre-backtest)
def panel_chars(px, tradable, elig, lo, hi, tag):
    """All four characteristics + controls, on [lo, hi]. Prices and the gate only."""
    cols = [c for c in px.columns if c in tradable]
    m = rebalance_mask(px.index, FREQ)
    start = px.index[260]
    idx = px.loc[start:].index
    idx = idx[(idx >= pd.Timestamp(lo)) & (idx <= pd.Timestamp(hi))] if hi else idx[idx >= pd.Timestamp(lo)]
    rb = idx[m.reindex(idx).fillna(False).values]
    e = elig.loc[rb, cols]
    k = len(cols)
    nel = e.sum(axis=1)
    breadth = float((nel / k).mean())
    r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
    disp = float(r63.where(e).std(axis=1, ddof=0).mean())
    vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
    evol = float(vol20.where(e).mean(axis=1).mean())
    dr = px[cols].pct_change().loc[idx]
    C = dr.corr().to_numpy()
    iu = np.triu_indices(k, 1)
    corr = float(np.nanmean(C[iu])) if k > 1 else np.nan
    return dict(tag=tag, k=k, n_elig=float(nel.median()), breadth=breadth, disp=disp,
                corr=corr, evol=evol, days=len(rb))


# ==================================================================== the grid
def run_grid(pool):
    rows, cache, chars = [], {}, []
    for i, (pname, meta) in enumerate(pool.items(), 1):
        px, tr = meta["px"], meta["tradable"]
        elig = eligible_mask(px, tr)
        key = score(px, vol_scale=False)[0]
        s_v1 = score(px, vol_scale=True)[0]
        m = rebalance_mask(px.index, FREQ)
        start = px.index[260]
        nel_ser = elig[m.values].sum(axis=1).loc[start:]
        ne = float(nel_ser.median())
        spy = px["SPY"].pct_change().fillna(0)

        for lo, hi, tag in ((IS_START, None, "FULL"), (IS_START, IS_END, "IS")):
            c = panel_chars(px, tr, elig, lo, hi, tag)
            c.update(panel=pname, source=meta["source"], kind=meta["kind"],
                     seed=meta["seed"], k_frac=meta["k_frac"], n_elig_grid=ne)
            chars.append(c)

        arms = [("EWall", None, np.nan), ("v1", None, np.nan), ("v2", None, np.nan)]
        arms += [("FWD", int(max(1, round(rt * ne))), rt) for rt in RATIOS]
        for arm, n, rt in arms:
            w = weights(px, tr, arm, n, elig=elig, key=key, s_v1=s_v1)
            for bps in (COST_BPS, DIAG_BPS):
                res = backtest(px, w, cost_bps=bps, freq=FREQ)
                r = res["returns"].loc[start:]
                sp = spy.loc[start:]
                r_is, r_oos = r.loc[IS_START:IS_END], r.loc[OOS_START:]
                sp_is, sp_oos = sp.loc[IS_START:IS_END], sp.loc[OOS_START:]
                mm, mo, mi = metrics(r), metrics(r_oos), metrics(r_is)
                h1, h2 = half_sharpes(r)
                cache[(pname, arm, n, bps)] = dict(r=r, sp=sp, r_oos=r_oos, sp_oos=sp_oos)
                rows.append(dict(
                    panel=pname, source=meta["source"], kind=meta["kind"], arm=arm,
                    n=(n if n else np.nan), r_target=rt, bps=bps, n_elig=ne,
                    r_real=(n / ne if n else np.nan), k=meta["k"],
                    CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                    H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    turn=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
                    gross=float(w.loc[start:].sum(axis=1).mean()),
                    sat_share=float((nel_ser <= n).mean()) if n else np.nan,
                    SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                    SPY_MaxDD=metrics(sp)["MaxDD"], SPY_OOS_Sharpe=metrics(sp_oos)["Sharpe"],
                ))
        # verdicts once both comparands exist
        for bps in (COST_BPS, DIAG_BPS):
            b2 = cache[(pname, "v2", None, bps)]["r"]
            b1 = cache[(pname, "v1", None, bps)]["r"]
            for rr in rows:
                if rr["panel"] != pname or rr["bps"] != bps or "p4a" in rr:
                    continue
                c = cache[(pname, rr["arm"], (None if np.isnan(rr["n"]) else int(rr["n"])), bps)]
                rr["p4a"] = v4a(c["r"], b2)
                rr["p4a_v1"] = v4a(c["r"], b1)
                rr["f4b"] = fail4b(c["r"], c["sp"], c["r_oos"], c["sp_oos"])
                rr["p4b"] = (rr["f4b"] == "-")
        P(f"  [{i:>2}/{len(pool)}] {pname:<18} k={meta['k']:<4} n_elig={ne:6.1f} "
          f"n={[int(max(1, round(rt*ne))) for rt in RATIOS]}")
        if i % 5 == 0 or i == len(pool):
            pd.DataFrame(rows).to_csv(OUT / f"{STEM}.partial.csv", index=False)
    return pd.DataFrame(rows), cache, pd.DataFrame(chars)


def reversal_table(grid, bps, window=""):
    S, C = f"{window}Sharpe", f"{window}CAGR"
    g = grid[grid.bps == bps]
    out = []
    for pname, d in g.groupby("panel", sort=False):
        ew = d[d.arm == "EWall"].iloc[0]
        for _, f in d[d.arm == "FWD"].sort_values("r_target").iterrows():
            dS, dC = ew[S] - f[S], ew[C] - f[C]
            out.append(dict(
                panel=pname, source=f.source, kind=f.kind, r_target=f.r_target,
                n=int(f.n), n_elig=f.n_elig, r_real=f.r_real, k=f.k,
                dS=dS, dC=dC,
                rev=bool((np.sign(dS) != np.sign(dC)) and abs(dS) > EPS_S and abs(dC) > EPS_C),
                rev_eps0=bool((np.sign(dS) != np.sign(dC)) and dS != 0 and dC != 0)))
    return pd.DataFrame(out)


# ==================================================================== main
def main():
    P(f"=== idea 271 - is the Sharpe/CAGR reversal a PANEL property?  ({SCRIPT}) ===")
    P(f"costs {COST_BPS} bps (diagnostic rung {DIAG_BPS}), weekly, next-day, gross {GROSS}, "
      f"gate above-200d AND vol20<{MAX_VOL}")
    pool = build_pool()
    P(f"POOL: {len(pool)} panels = {sum(1 for m in pool.values() if m['kind']=='NAMED')} NAMED "
      f"+ {sum(1 for m in pool.values() if m['kind']=='SUB')} SUB; "
      f"{len(pool)*len(RATIOS)} reversal cells, {len(pool)*(3+len(RATIOS))*2} backtests.")
    grid, cache, chars = run_grid(pool)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    chars.to_csv(OUT / f"{STEM}.chars.csv", index=False)

    # ---------------------------------------------------------------- reproduction gate
    P("")
    P("REPRODUCTION GATE (idea 269C's published cells, recomputed here):")
    g10 = grid[grid.bps == COST_BPS]
    for pn, want in (("B136", "10.7%/1.026/-17.7%, OOS 1.019"), ("U56", "10.4%/1.049/-15.9%")):
        e = g10[(g10.panel == pn) & (g10.arm == "EWall")].iloc[0]
        P(f"  {pn}/EWall  {e.CAGR:.1%}/{e.Sharpe:.3f}/{e.MaxDD:.1%}  OOS {e.OOS_Sharpe:.3f}"
          f"   [published {want}]")
    rev_full = reversal_table(grid, COST_BPS)
    rev_full.to_csv(OUT / f"{STEM}.reversal.csv", index=False)
    named5 = ["B136", "BSTK100", "U56", "ETF36", "SMALL439"]
    pub = {"B136": 6, "BSTK100": 6, "U56": 4, "ETF36": 2, "SMALL439": 0}
    P("  per-panel reversal count over the 7 matched ratios (published: 6/6/4/2/0 of 7):")
    for pn in named5:
        c = int(rev_full[rev_full.panel == pn].rev.sum())
        P(f"    {pn:<9} {c}/7   [published {pub[pn]}/7]  {'OK' if c == pub[pn] else 'MISMATCH'}")
    byr = rev_full[rev_full.kind == "NAMED"].groupby("r_target").rev.mean()
    P("  share by ratio over the 5 NAMED panels (published 0.60/0.60/0.80/0.80/0.40/0.40/0.00):")
    P("    " + " / ".join(f"{v:.2f}" for v in byr.values))

    # ---------------------------------------------------------------- Q1 the pool
    dup = rev_full.duplicated(subset=["panel", "n"], keep="first")
    P(f"  DEGENERATE cells (two ratios rounding to the same n on a narrow panel): "
      f"{int(dup.sum())} of {len(rev_full)}; share over the non-degenerate cells only = "
      f"{rev_full.loc[~dup, 'rev'].mean():.4f} vs {rev_full.rev.mean():.4f} over all.")

    P("")
    P("Q1 - the reversal share over the enlarged pool (full sample, 10 bps):")
    ps = rev_full.groupby("panel").agg(source=("source", "first"), kind=("kind", "first"),
                                       k=("k", "first"), n_elig=("n_elig", "first"),
                                       rev=("rev", "mean"), rev_eps0=("rev_eps0", "mean"))
    cf = chars[chars.tag == "FULL"].set_index("panel")
    ps = ps.join(cf[CHARS + ["days"]])
    ps.to_csv(OUT / f"{STEM}.panelshare.csv")
    P(fmt(ps.sort_values(["kind", "source", "k"]), 4))
    P(f"  pool share mean {ps.rev.mean():.4f}  sd {ps.rev.std(ddof=1):.4f}  "
      f"min {ps.rev.min():.4f}  max {ps.rev.max():.4f}   "
      f"(0/7 in {int((ps.rev==0).sum())} panels, 7/7 in {int((ps.rev==1).sum())})")
    P("  by SOURCE (does the parent's panel disagreement survive sub-sampling?):")
    P(fmt(ps.groupby("source").agg(panels=("rev", "size"), rev=("rev", "mean"),
                                   sd=("rev", "std"), lo=("rev", "min"), hi=("rev", "max")), 4))

    # ---------------------------------------------------------------- Q2 the regression
    P("")
    P("Q2 - PANEL-LEVEL regression of the reversal share on the four pre-backtest "
      "characteristics (z-scored; n = %d panels):" % len(ps))
    d = ps.dropna(subset=CHARS + ["rev"]).copy()
    mu, sd = zscore_fit(d, CHARS + CONTROLS)
    for cols, lab in ((CHARS, "4 chars"), (CHARS + CONTROLS, "4 chars + k, n_elig"),
                      (CONTROLS, "controls only")):
        X = design(d, cols, mu, sd)
        tab, r2, ar2, n, _ = ols(d.rev.to_numpy(), X, ["const"] + cols)
        P(f"  [{lab}]  R2 {r2:.4f}  adjR2 {ar2:.4f}  n {n}")
        P(fmt(tab, 4))
    P("  univariate Spearman(share, characteristic) over the pool:")
    rows = []
    for c in CHARS + CONTROLS:
        rho, t, n = spearman(d[c], d.rev)
        rows.append(dict(characteristic=c, rho=rho, t=t, n=n))
    P(fmt(pd.DataFrame(rows).set_index("characteristic"), 4))

    P("")
    P("Q3 - CELL-LEVEL linear probability model (rev ~ chars + r_real), SEs clustered "
      "by panel:")
    cells = rev_full.merge(cf.reset_index()[["panel"] + CHARS], on="panel", how="left")
    cells = cells.dropna(subset=CHARS)
    mu2, sd2 = zscore_fit(cells, CHARS + ["r_real"])
    for cols, lab in ((["r_real"], "width only (idea 269C's regressor)"),
                      (CHARS, "4 chars only"),
                      (CHARS + ["r_real"], "4 chars + width")):
        X = design(cells, cols, mu2, sd2)
        tab, r2, ar2, n, _ = ols(cells.rev.astype(float).to_numpy(), X, ["const"] + cols,
                                 cluster=cells.panel.to_numpy())
        P(f"  [{lab}]  R2 {r2:.4f}  n {n} cells, {cells.panel.nunique()} clusters")
        P(fmt(tab, 4))

    # -------------------------------------------- Q4 leave-one-SOURCE-out (does it travel?)
    P("")
    P("Q4 - LEAVE-ONE-SOURCE-OUT: fit the panel-level model on four sources, predict the "
      "fifth (the only honest test of 'a new panel is predictable'):")
    rows = []
    for src in sorted(d.source.unique()):
        tr, te = d[d.source != src], d[d.source == src]
        mu3, sd3 = zscore_fit(tr, CHARS)
        _, _, _, _, b = ols(tr.rev.to_numpy(), design(tr, CHARS, mu3, sd3), ["const"] + CHARS)
        pred = design(te, CHARS, mu3, sd3) @ b
        err = te.rev.to_numpy() - pred
        base = tr.rev.mean()
        ss_res, ss_base = float((err ** 2).sum()), float(((te.rev - base) ** 2).sum())
        rho, t, _ = spearman(pred, te.rev)
        rows.append(dict(held_out=src, panels=len(te), actual=te.rev.mean(),
                         pred=float(pred.mean()), rmse=float(np.sqrt((err ** 2).mean())),
                         rmse_mean_rule=float(np.sqrt(((te.rev - base) ** 2).mean())),
                         oos_R2=1 - ss_res / ss_base if ss_base > 0 else np.nan,
                         spearman=rho))
    loso = pd.DataFrame(rows).set_index("held_out")
    loso.to_csv(OUT / f"{STEM}.loso.csv")
    P(fmt(loso, 4))
    P(f"  mean out-of-source R2 vs the pool mean: {loso.oos_R2.mean():+.4f}  "
      f"(<= 0 means the four characteristics beat NOTHING)")

    # ---------------------------------------------------------------- rule 8
    P("")
    P("RULE 8 (i) THE RELATIONSHIP - fit on IS characteristics + IS reversals, read OOS once")
    tis = reversal_table(grid, COST_BPS, "IS_")
    toos = reversal_table(grid, COST_BPS, "OOS_")
    ci = chars[chars.tag == "IS"].set_index("panel")
    key = ["panel", "r_target"]
    m = (tis[key + ["source", "kind", "r_real", "rev"]].rename(columns={"rev": "rev_is"})
         .merge(toos[key + ["rev"]].rename(columns={"rev": "rev_oos"}), on=key)
         .merge(ci.reset_index()[["panel"] + CHARS], on="panel", how="left"))
    m = m.dropna(subset=CHARS)
    mu4, sd4 = zscore_fit(m, CHARS + ["r_real"])
    Xc = design(m, CHARS + ["r_real"], mu4, sd4)
    _, r2c, _, _, bc = ols(m.rev_is.astype(float).to_numpy(), Xc, ["const"] + CHARS + ["r_real"])
    m["phat"] = Xc @ bc
    grid_rows = []
    for th in np.round(np.arange(0.05, 1.00, 0.05), 2):
        pr = m.phat >= th
        grid_rows.append(dict(threshold=float(th),
                              IS_accuracy=float((pr == m.rev_is).mean()),
                              OOS_accuracy=float((pr == m.rev_oos).mean()),
                              predicted_rate=float(pr.mean())))
    # idea 269C's width rule, refitted here on the same cells
    for th in np.round(np.arange(0.05, 1.01, 0.05), 2):
        pr = m.r_real < th
        grid_rows.append(dict(threshold=float(th), rule="R_THRESH",
                              IS_accuracy=float((pr == m.rev_is).mean()),
                              OOS_accuracy=float((pr == m.rev_oos).mean()),
                              predicted_rate=float(pr.mean())))
    gr = pd.DataFrame(grid_rows).fillna({"rule": "CHAR"})
    gr.to_csv(OUT / f"{STEM}.threshold_grid.csv", index=False)
    P(f"  IS fit of P(reversal) on 4 chars + width: R2 {r2c:.4f}, {len(m)} cells")
    P("  ALL threshold grid points (both rules):")
    P(fmt(gr.set_index(["rule", "threshold"]).sort_index(), 4))
    gc = gr[gr.rule == "CHAR"]
    best_c = gc.loc[gc.IS_accuracy.idxmax()]
    gw = gr[gr.rule == "R_THRESH"]
    best_w = gw.loc[gw.IS_accuracy.idxmax()]
    maj_is = bool(m.rev_is.mean() > 0.5)
    src_maj = m.groupby("source").rev_is.mean() > 0.5
    pan_maj = m.groupby("panel").rev_is.mean() > 0.5
    # leave-one-source-out version of the characteristic rule
    pr_loso = pd.Series(False, index=m.index)
    for src in sorted(m.source.unique()):
        tr, te = m[m.source != src], m[m.source == src]
        mu5, sd5 = zscore_fit(tr, CHARS + ["r_real"])
        _, _, _, _, b5 = ols(tr.rev_is.astype(float).to_numpy(),
                             design(tr, CHARS + ["r_real"], mu5, sd5),
                             ["const"] + CHARS + ["r_real"])
        pr_loso.loc[te.index] = (design(te, CHARS + ["r_real"], mu5, sd5) @ b5) >= best_c.threshold
    rivals = pd.DataFrame([
        dict(classifier=f"CONST (IS majority = {maj_is})",
             IS_acc=float((maj_is == m.rev_is).mean()), OOS_acc=float((maj_is == m.rev_oos).mean())),
        dict(classifier=f"R_THRESH (r < {best_w.threshold:.2f})  [idea 269C]",
             IS_acc=best_w.IS_accuracy, OOS_acc=best_w.OOS_accuracy),
        dict(classifier="SOURCE (per-source IS majority)",
             IS_acc=float((m.source.map(src_maj) == m.rev_is).mean()),
             OOS_acc=float((m.source.map(src_maj) == m.rev_oos).mean())),
        dict(classifier="PANEL (per-panel IS majority)",
             IS_acc=float((m.panel.map(pan_maj) == m.rev_is).mean()),
             OOS_acc=float((m.panel.map(pan_maj) == m.rev_oos).mean())),
        dict(classifier=f"CHAR (phat >= {best_c.threshold:.2f}, fitted on all sources)",
             IS_acc=best_c.IS_accuracy, OOS_acc=best_c.OOS_accuracy),
        dict(classifier=f"CHAR-LOSO (same, fitted without the held-out source)",
             IS_acc=np.nan, OOS_acc=float((pr_loso == m.rev_oos).mean())),
    ]).set_index("classifier")
    base_rate = float(max(m.rev_oos.mean(), 1 - m.rev_oos.mean()))
    P("")
    P(f"  OOS majority base rate = {base_rate:.4f}  (OOS reversal rate {m.rev_oos.mean():.4f})")
    P(fmt(rivals, 4))
    rivals.to_csv(OUT / f"{STEM}.rivals.csv")
    m.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    # ---------------------------------------------------------------- rule 8 (ii) the book
    P("")
    P("RULE 8 (ii) THE BOOK - pooled equal-weight over the 5 NAMED panels, OOS read once")
    sels = {}
    for pn in named5:
        dd = g10[(g10.panel == pn) & (g10.arm == "FWD")].sort_values("r_target")
        mm = m[m.panel == pn].sort_values("r_real")
        safe = mm[mm.phat < best_c.threshold]          # model says reversal-SAFE
        csel_n = int(dd.loc[dd.r_target == safe.iloc[0].r_target].iloc[0].n) if len(safe) else int(dd.iloc[-1].n)
        wsel = mm[mm.r_real >= best_w.threshold]
        rsel_n = int(dd.loc[dd.r_target == wsel.iloc[0].r_target].iloc[0].n) if len(wsel) else int(dd.iloc[-1].n)
        sels[pn] = dict(EWALL=("EWall", None), FWD20=("FWD", int(dd.iloc[(dd.n - 20).abs().argmin()].n)),
                        S_SHARPE=("FWD", int(dd.loc[dd.IS_Sharpe.idxmax()].n)),
                        S_CAGR=("FWD", int(dd.loc[dd.IS_CAGR.idxmax()].n)),
                        CSEL=("FWD", csel_n), RSEL=("FWD", rsel_n),
                        V1=("v1", None), V2=("v2", None))
    P("  per-panel selections: " + "; ".join(
        f"{pn}: CSEL n={sels[pn]['CSEL'][1]}, RSEL n={sels[pn]['RSEL'][1]}, "
        f"S_SHARPE n={sels[pn]['S_SHARPE'][1]}, S_CAGR n={sels[pn]['S_CAGR'][1]}" for pn in named5))
    rows = []
    for lab in ["EWALL", "FWD20", "S_SHARPE", "S_CAGR", "CSEL", "RSEL", "V1", "V2"]:
        streams, o_streams = [], []
        for pn in named5:
            arm, n = sels[pn][lab]
            c = cache[(pn, arm, n, COST_BPS)]
            streams.append(c["r"]); o_streams.append(c["r_oos"])
        pooled = pd.concat(streams, axis=1).mean(axis=1).dropna()
        po = pd.concat(o_streams, axis=1).mean(axis=1).dropna()
        mm_, mo_ = metrics(pooled), metrics(po)
        h1, h2 = half_sharpes(pooled)
        rows.append(dict(book=lab, CAGR=mm_["CAGR"], Sharpe=mm_["Sharpe"], MaxDD=mm_["MaxDD"],
                         H1=h1, H2=h2, OOS_CAGR=mo_["CAGR"], OOS_Sharpe=mo_["Sharpe"],
                         OOS_MaxDD=mo_["MaxDD"]))
    spys = [cache[(pn, "EWall", None, COST_BPS)]["sp"] for pn in named5]
    spyo = [cache[(pn, "EWall", None, COST_BPS)]["sp_oos"] for pn in named5]
    sp_p = pd.concat(spys, axis=1).mean(axis=1).dropna()
    sp_o = pd.concat(spyo, axis=1).mean(axis=1).dropna()
    ms, mso = metrics(sp_p), metrics(sp_o)
    h1, h2 = half_sharpes(sp_p)
    rows.append(dict(book="SPY", CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"],
                     H1=h1, H2=h2, OOS_CAGR=mso["CAGR"], OOS_Sharpe=mso["Sharpe"],
                     OOS_MaxDD=mso["MaxDD"]))
    wf = pd.DataFrame(rows).set_index("book")
    wf.to_csv(OUT / f"{STEM}.walkforward.csv")
    P(fmt(wf, 4))

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("KEEP paths on ALL grid points (4a vs live RULES v2; 4b vs SPY):")
    for bps in (COST_BPS, DIAG_BPS):
        g = grid[grid.bps == bps]
        P(f"  @{bps} bps: 4a {int(g.p4a.sum())}/{len(g)}   4a(vs v1) {int(g.p4a_v1.sum())}/{len(g)}"
          f"   4b {int(g.p4b.sum())}/{len(g)}")
    g10b = grid[(grid.bps == COST_BPS)]
    P("  4b passes @10 bps by source and arm:")
    P(fmt(g10b[g10b.p4b].groupby(["source", "arm"]).size().rename("passes").to_frame(), 0))
    P("  binding bar over the @10 bps failures:")
    fb = g10b[~g10b.p4b].f4b.str.split(",").explode().value_counts()
    P(fmt(fb.rename("count").to_frame(), 0))
    keep = g10b[g10b.p4b].sort_values("Sharpe", ascending=False)
    keep.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("  top 15 of the @10 bps 4b passes:")
    P(fmt(keep.head(15)[["panel", "arm", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "turn"]].set_index("panel"), 4))
    P("  NAMED-panel 4b passes @10 bps (the only cells the record can act on):")
    kn = keep[keep.kind == "NAMED"]
    P(fmt(kn[["panel", "arm", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
              "turn"]].set_index("panel"), 4) if len(kn) else "    none")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P("")
    P(f"wrote {STEM}.{{grid,chars,reversal,panelshare,loso,threshold_grid,rivals,cells,"
      f"walkforward,keep,console}}")


if __name__ == "__main__":
    main()
