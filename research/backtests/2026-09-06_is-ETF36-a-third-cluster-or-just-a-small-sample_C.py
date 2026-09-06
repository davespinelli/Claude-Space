#!/usr/bin/env python3
"""Idea 277 - "is-ETF36-a-third-cluster-or-just-a-small-sample" (lane C, 2026-09-06).

The question
------------
Idea 271 fitted a four-characteristic model (breadth, dispersion, pairwise correlation,
eligible-set vol) of the matched-ratio Sharpe/CAGR reversal share over 53 panels.  On four
of its five sources the leave-one-SOURCE-out fit was wrong in an informative direction; on
ETF36 it predicted ZERO reversals at every LOSO fit and landed EXACTLY on that source's own
base rate, lift 0.0000 - the one source where the model is neither right nor wrong.  ETF36
is also the odd panel physically: 36 names against 100-439, mean pairwise correlation 0.34
against ~0.25, dispersion 0.062 against ~0.09.  So the queue asks:

    is an ETF panel a DISTINCT REGIME - a third cluster beside idea 271's small-cap and
    large-cap ones - or is it just a SMALL SAMPLE of the large-cap cluster?

Design: mix the two panels and sweep the ETF share
--------------------------------------------------
A cluster claim is a claim about a DISCONTINUITY.  The way to test one is to build the
intermediate panels the record never had and see whether the reversal share travels
smoothly between the endpoints or steps.  Panel WIDTH is held FIXED at k = 36 across the
whole sweep, which is what makes this a test of ETF-ness rather than of narrowness:
ETF36's k=36 is otherwise perfectly confounded with its composition.

    POOL (pre-registered, seeded, fixed before any number was read)
      MIX  k = 36 names drawn as n_etf = round(s * 36) ETFs from the 36-name ETF set and
           36 - n_etf stocks from the 100-name BSTK100 set, for
              s in {0.000, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000}
              -> n_etf   0     5      9      14     18     23     27     32     36
           x seed in {0, 1, 2, 3, 4, 5} (uniform draw without replacement, zlib.crc32-seeded).
           SEED HISTORY, stated because it is a design change: the first pass ran seeds
           {0, 1, 2} and died in Q3's print formatting AFTER Q1/Q2 had printed.  The seed
           count was raised 3 -> 6 for power before any verdict was formed; the seeds are
           keyed by string, so seeds 0-2 are the IDENTICAL panels, and the 3-seed subset is
           reported beside the 6-seed pool everywhere the verdict rests on it.
           At s = 1.000 all three seeds are the SAME panel and it is ETF36 EXACTLY, so the
           sweep terminates on the parent's own panel (asserted at run time, not assumed).
           24 MIX panels + ETF36 = 25 points on the sweep.
      NAMED  U56, B136, BSTK100, SMALL439, ETF36 - idea 269C's build_panels() imported
           verbatim so its published cells reproduce inside this run (reproduction gate).
      = 29 panels x 7 pre-registered ratios = 203 reversal cells, 580 backtests,
        290 grid points per cost rung.  ALL are written.

    SEEDS ARE REPLICATION, NOT TUNING.  Every seed is reported; nothing is selected on
    seed.  The seed spread at fixed s is exactly the "just a small sample" null band: if
    ETF36's share sits inside the spread of k-matched STOCK panels (s = 0), the record has
    been reading sampling noise.

Grid, imported verbatim from idea 269C / idea 271 (weekly, next-day, 10 bps, gate =
above-200d AND vol20 < 0.60, ranking key = the composite WITHOUT the vol scaler, every arm
gross-matched at 0.75; 0 bps carried as a DIAGNOSTIC column only, never selected on):
      EWall   every eligible name, equal weight   (the un-ranked book)
      FWD-n   top-n by the composite key, n = round(r* * n_elig), r* in
              {0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00}
      v1      RULES v1 (continuity row)        v2  RULES v2, the live book (4a comparand)
Reversal is idea 259/269's epsilon rule unchanged: sign(dS) != sign(dC) with |dS| > 0.005
and |dC| > 5 bps/yr, dS = Sharpe(EWall) - Sharpe(FWD-n), dC likewise for CAGR.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. ETF share s (9)      2. target ratio r* (7)
The characteristics are measured, not tuned; seed is replication; the cost rung is fixed at
PROTOCOL's 10 bps.

Pre-registered readings (direction fixed before any number was read)
    THIRD CLUSTER  the s-curve steps: a break at the ETF end that a linear-in-s fit misses,
                   AND ETF36 outside the prediction interval of idea 271's four-
                   characteristic model fitted on the s < 1 panels (i.e. ETF-ness is NOT
                   mediated by breadth/dispersion/correlation/vol), AND ETF36 outside the
                   k-matched s = 0 seed band.
    SMALL SAMPLE   the s-curve is flat or the ETF end sits inside the s = 0 seed band; the
                   parent's 2/7 is then a draw, not a regime.
    CONTINUUM      the share moves monotonically in s and the characteristic model predicts
                   ETF36 from the s < 1 panels; ETF-ness is a position on the characteristic
                   axes, not a cluster.  Report where the curve TURNS OVER either way.

Walk-forward (PROTOCOL rule 8), pre-registered with direction before any OOS read
    IS = 2009-01-01..2016-12-31 chooses; OOS = 2017-01-01..end read ONCE.
    (i)  THE RELATIONSHIP.  P(reversal) fitted on IS-window characteristics against IS-window
         reversals and applied ONCE to OOS reversals, for four nested rules - CHAR (idea
         271's four), CHAR+s, S_ONLY (the ETF share alone) and R_THRESH (idea 269C's width
         rule) - against the OOS majority base rate.  The WHOLE threshold grid is printed.
         Beside it: a HOLD-OUT-THE-ETF-END fit (train on s <= 0.500, predict s >= 0.625),
         which is the only honest form of "does the ETF regime travel".
    (ii) THE BOOK.  ESEL (narrowest n whose fitted reversal probability is below the
         threshold, model = CHAR+s) against EWALL (do nothing), FWD20 (incumbent), S_SHARPE,
         S_CAGR, RULES v1, RULES v2 and SPY, pooled equal-weight over the 5 NAMED panels so
         the numbers sit directly beside idea 271's published pooled row.  OOS CAGR, Sharpe
         and MaxDD are reported for every book against the baseline and SPY.

Verdicts (both KEEP paths, on every one of the 580 grid points)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.  The v1
        comparand is carried as a second column for continuity with the pre-2026-09-06 record.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents, and every
MIX panel is a subset of universe_broad, so the bias is inherited whole.  The un-ranked book
holds everything and takes the full survivorship premium while a ranked book can only
redistribute it, so the bias runs TOWARD reversals - toward finding MORE structure, i.e.
more of a "cluster", than a live universe would have shown.  A "distinct regime" verdict
here is an upper bound; a "no distinct regime" verdict is conservative.

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
SHARES = [0.000, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000]
SEEDS = [0, 1, 2, 3, 4, 5]
SEEDS_PREREG = [0, 1, 2]                 # the first pass; reported beside the full pool
N_PERM = 2000                            # label permutations for the s-effect null
K_MIX = 36                               # = |ETF36|, so s=1 lands exactly on the parent panel
CHARS = ["breadth", "disp", "corr", "evol"]
CONTROLS = ["k", "n_elig"]
HOLDOUT_S = 0.500                        # train s <= this, predict s > this (ETF-end hold-out)

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)

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


def ols(y, X, names, cluster=None):
    """Least squares with a constant already in X. Returns tidy frame, R2, adjR2, n, beta."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
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
            u = X[ii].T @ e[ii]
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
    return named, sub, px136, etf36, b_stk


def build_pool():
    """5 NAMED panels + the pre-registered k-matched ETF-share sweep."""
    named, sub, px136, etf36, b_stk = build_named()
    pool = {}
    for nm, (px, tr) in named.items():
        pool[nm] = dict(px=px, tradable=tr, source=nm, kind="NAMED", k=len(tr), seed=-1,
                        etf_share=(1.0 if nm == "ETF36" else np.nan), n_etf=np.nan)
    etf_pool = np.array(sorted(etf36))
    stk_pool = np.array(sorted(b_stk))
    seen = {frozenset(etf36)}                      # ETF36 already in the pool as s = 1.000
    for s in SHARES:
        n_etf = int(round(s * K_MIX))
        n_stk = K_MIX - n_etf
        for sd in SEEDS:
            seed = zlib.crc32(f"MIX|{s:.3f}|{sd}".encode()) % (2 ** 32)
            rng = np.random.default_rng(seed)
            pick = []
            if n_etf:
                pick += rng.choice(etf_pool, size=n_etf, replace=False).tolist()
            if n_stk:
                pick += rng.choice(stk_pool, size=n_stk, replace=False).tolist()
            pick = sorted(pick)
            fs = frozenset(pick)
            if fs in seen:                          # s = 1.000 is ETF36 for every seed
                continue
            seen.add(fs)
            p, t = sub(px136, pick, tradable=pick)
            pool[f"MIX~s{s:.3f}~{sd}"] = dict(px=p, tradable=t, source="MIX", kind="MIX",
                                              k=len(t), seed=sd, etf_share=s, n_etf=n_etf)
    return pool, etf36


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
    """idea 271's four characteristics + controls on [lo, hi]. Prices and the gate only."""
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
            c.update(panel=pname, source=meta["source"], kind=meta["kind"], seed=meta["seed"],
                     etf_share=meta["etf_share"], n_etf=meta["n_etf"], n_elig_grid=ne)
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
                    panel=pname, source=meta["source"], kind=meta["kind"],
                    etf_share=meta["etf_share"], seed=meta["seed"], arm=arm,
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
                    SPY_OOS_CAGR=metrics(sp_oos)["CAGR"], SPY_OOS_MaxDD=metrics(sp_oos)["MaxDD"],
                ))
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
          f"etf_share={meta['etf_share'] if meta['etf_share']==meta['etf_share'] else float('nan'):.3f} "
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
                panel=pname, source=f.source, kind=f.kind, etf_share=f.etf_share,
                seed=f.seed, r_target=f.r_target, n=int(f.n), n_elig=f.n_elig,
                r_real=f.r_real, k=f.k, dS=dS, dC=dC,
                rev=bool((np.sign(dS) != np.sign(dC)) and abs(dS) > EPS_S and abs(dC) > EPS_C),
                rev_eps0=bool((np.sign(dS) != np.sign(dC)) and dS != 0 and dC != 0)))
    return pd.DataFrame(out)


# ==================================================================== main
def main():
    P(f"=== idea 277 - is ETF36 a third cluster or just a small sample?  ({SCRIPT}) ===")
    P(f"costs {COST_BPS} bps (diagnostic rung {DIAG_BPS}), weekly, next-day, gross {GROSS}, "
      f"gate above-200d AND vol20<{MAX_VOL}; MIX panels all k={K_MIX}")
    pool, etf36 = build_pool()
    nmix = sum(1 for m in pool.values() if m["kind"] == "MIX")
    P(f"POOL: {len(pool)} panels = 5 NAMED + {nmix} MIX; "
      f"{len(pool)*len(RATIOS)} reversal cells, {len(pool)*(3+len(RATIOS))*2} backtests.")
    # the sweep must terminate ON the parent's panel, not near it
    assert set(pool["ETF36"]["tradable"]) == set(etf36) and len(etf36) == K_MIX
    P(f"  s=1.000 endpoint identity check: ETF36 tradable set == the {K_MIX}-name ETF draw  OK")
    grid, cache, chars = run_grid(pool)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    chars.to_csv(OUT / f"{STEM}.chars.csv", index=False)

    # ---------------------------------------------------------------- reproduction gate
    P("")
    P("REPRODUCTION GATE (idea 269C / idea 271 published cells, recomputed here):")
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
    ok_all = True
    for pn in named5:
        c = int(rev_full[rev_full.panel == pn].rev.sum())
        ok = (c == pub[pn])
        ok_all &= ok
        P(f"    {pn:<9} {c}/7   [published {pub[pn]}/7]  {'OK' if ok else 'MISMATCH'}")
    byr = rev_full[rev_full.kind == "NAMED"].groupby("r_target").rev.mean()
    P("  share by ratio over the 5 NAMED panels (published 0.60/0.60/0.80/0.80/0.40/0.40/0.00):")
    P("    " + " / ".join(f"{v:.2f}" for v in byr.values))
    P(f"  GATE: {'5/5 reproduced' if ok_all else 'NOT all reproduced - read every number below with that'}")

    # =============================================================== Q1 the mixing curve
    P("")
    P("Q1 - THE SWEEP: reversal share against the ETF share, panel width held at k=36")
    cf = chars[chars.tag == "FULL"].set_index("panel")
    ps = rev_full.groupby("panel").agg(source=("source", "first"), kind=("kind", "first"),
                                       etf_share=("etf_share", "first"), seed=("seed", "first"),
                                       k=("k", "first"), n_elig=("n_elig", "first"),
                                       rev=("rev", "mean"), rev_eps0=("rev_eps0", "mean"))
    ps = ps.join(cf[CHARS + ["days"]])
    ps.to_csv(OUT / f"{STEM}.panelshare.csv")
    sw = ps[ps.etf_share.notna()].copy()          # the 25 sweep points (24 MIX + ETF36)
    P(fmt(sw.sort_values(["etf_share", "seed"]), 4))
    curve = sw.groupby("etf_share").agg(panels=("rev", "size"), rev=("rev", "mean"),
                                        sd=("rev", "std"), lo=("rev", "min"), hi=("rev", "max"),
                                        breadth=("breadth", "mean"), disp=("disp", "mean"),
                                        corr=("corr", "mean"), evol=("evol", "mean"),
                                        n_elig=("n_elig", "mean"))
    curve.to_csv(OUT / f"{STEM}.curve.csv")
    P("")
    P("  the curve (mean over seeds at each rung; every seed is in the table above):")
    P(fmt(curve, 4))
    rho, t, n = spearman(sw.etf_share, sw.rev)
    P(f"  Spearman(etf_share, share) over the {n} sweep panels: rho {rho:+.4f}  t {t:+.2f}")
    sw3 = sw[(sw.seed.isin(SEEDS_PREREG)) | (sw.etf_share >= 1.0)]
    c3 = sw3.groupby("etf_share").rev.agg(["size", "mean", "std", "min", "max"])
    P(f"  the PRE-REGISTERED 3-seed subset (seeds {SEEDS_PREREG}, {len(sw3)} panels) "
      f"beside it:")
    P(fmt(c3, 4))
    r3, t3, n3 = spearman(sw3.etf_share, sw3.rev)
    P(f"    Spearman over the 3-seed subset: rho {r3:+.4f}  t {t3:+.2f}  n {n3}")

    lo_lvl, hi_lvl = float(curve.rev.iloc[0]), float(curve.rev.iloc[-1])
    mid = 0.5 * (lo_lvl + hi_lvl)
    def crossings(level):
        xs, ys = curve.index.to_numpy(float), curve.rev.to_numpy(float)
        out = []
        for i in range(1, len(xs)):
            if (ys[i - 1] - level) * (ys[i] - level) <= 0 and ys[i] != ys[i - 1]:
                out.append(xs[i - 1] + (level - ys[i - 1]) * (xs[i] - xs[i - 1]) / (ys[i] - ys[i - 1]))
        return out
    nmono = int(sum(1 for i in range(1, len(curve))
                    if np.sign(curve.rev.iloc[i] - curve.rev.iloc[i - 1]) !=
                    np.sign(curve.rev.iloc[1] - curve.rev.iloc[0])))
    P(f"  endpoints: s=0.000 share {lo_lvl:.4f}   s=1.000 share {hi_lvl:.4f}   "
      f"midpoint {mid:.4f}")
    P(f"  TURNOVER POINT (the queue's ask): the curve crosses its own midpoint at s = "
      f"{crossings(mid)} and the 0.50 level at s = {crossings(0.5)} (linear interpolation).")
    P(f"    the curve reverses direction {nmono} times over its 8 steps, so a single "
      f"turnover point is only meaningful if the curve is monotone - read the count first.")

    # permutation null for ANY s-effect: shuffle the rung labels across panels
    rng = np.random.default_rng(20260906)
    obs_rho = abs(rho)
    obs_f = float(curve.rev.std(ddof=1) / max(1e-9, sw.groupby("etf_share").rev.std(ddof=1).mean()))
    yv = sw.rev.to_numpy(float)
    xv = sw.etf_share.to_numpy(float)
    hits_r = hits_f = 0
    for _ in range(N_PERM):
        perm = rng.permutation(yv)
        rr_, _, _ = spearman(xv, perm)
        dfp = pd.DataFrame(dict(s=xv, y=perm))
        between = dfp.groupby("s").y.mean().std(ddof=1)
        within = dfp.groupby("s").y.std(ddof=1).mean()
        if abs(rr_) >= obs_rho: hits_r += 1
        if between / max(1e-9, within) >= obs_f: hits_f += 1
    P(f"  PERMUTATION NULL ({N_PERM} shuffles of the rung label across the {len(sw)} panels):")
    P(f"    |Spearman| {obs_rho:.4f}  p = {hits_r/N_PERM:.4f}")
    P(f"    between/within sd ratio {obs_f:.4f}  p = {hits_f/N_PERM:.4f}   "
      f"(ratio <= 1 means the rung explains less than the seed does)")

    # ============================================ Q2 step or continuum, and the sample band
    P("")
    P("Q2 - STEP or CONTINUUM? (linear in s vs a step dummy at the ETF end)")
    d = sw.dropna(subset=CHARS + ["rev"]).copy()
    d["etf_end"] = (d.etf_share >= 0.875).astype(float)
    d["is_etf36"] = (d.etf_share >= 1.0).astype(float)
    rows = []
    for cols, lab in ((["etf_share"], "linear in s"),
                      (["is_etf36"], "step at s=1 only"),
                      (["etf_end"], "step at s>=0.875"),
                      (["etf_share", "is_etf36"], "linear in s + step at s=1")):
        mu, sd = zscore_fit(d, cols)
        tab, r2, ar2, nn, _ = ols(d.rev.to_numpy(), design(d, cols, mu, sd), ["const"] + cols)
        rows.append(dict(model=lab, R2=r2, adjR2=ar2, n=nn))
        P(f"  [{lab}]  R2 {r2:.4f}  adjR2 {ar2:.4f}  n {nn}")
        P(fmt(tab, 4))
    pd.DataFrame(rows).set_index("model").to_csv(OUT / f"{STEM}.shape.csv")

    s0 = sw[sw.etf_share == 0.0].rev
    P("")
    P("  THE SMALL-SAMPLE BAND: k-matched STOCK panels (s=0.000, same k=36, same grid)")
    P(f"    s=0 seeds: {', '.join(f'{v:.4f}' for v in sorted(s0))}   "
      f"mean {s0.mean():.4f}  sd {s0.std(ddof=1):.4f}  range [{s0.min():.4f}, {s0.max():.4f}]")
    s0q = np.quantile(s0.to_numpy(float), [0.05, 0.95])
    P(f"    s=0 5th/95th pct {s0q[0]:.4f} / {s0q[1]:.4f}; the whole s<1 pool "
      f"[{sw[sw.etf_share < 1].rev.min():.4f}, {sw[sw.etf_share < 1].rev.max():.4f}], "
      f"share of s<1 panels at or below ETF36's "
      f"{float((sw[sw.etf_share < 1].rev <= sw.loc['ETF36', 'rev']).mean()):.4f}")
    etf_share_val = float(sw.loc["ETF36", "rev"])
    P(f"    ETF36 share {etf_share_val:.4f}  ->  "
      f"{'INSIDE' if s0.min() <= etf_share_val <= s0.max() else 'OUTSIDE'} the s=0 seed range; "
      f"z vs the s=0 seeds = {(etf_share_val - s0.mean()) / max(1e-9, s0.std(ddof=1)):+.2f}")
    allsd = sw.groupby("etf_share").rev.std(ddof=1)
    P(f"    mean within-rung seed sd across the sweep {allsd.mean():.4f}; the MECHANICAL floor "
      f"from 7 cells at p=0.5 is sqrt(.25/7) = {np.sqrt(0.25/7):.4f}")
    P(f"    between-rung sd of the curve {curve.rev.std(ddof=1):.4f}  vs within-rung "
      f"{allsd.mean():.4f}  ->  ratio {curve.rev.std(ddof=1)/max(1e-9, allsd.mean()):.2f}x")

    # ===================================== Q3 is ETF-ness mediated by the characteristics?
    P("")
    P("Q3 - MEDIATION: does idea 271's four-characteristic model, fitted on the s<1 panels, "
      "predict ETF36? (the parent's LOSO lift was 0.0000 there)")
    tr = d[d.etf_share < 1.0]
    te = d[d.etf_share >= 1.0]
    mu, sd = zscore_fit(tr, CHARS)
    tab, r2, _, nn, b = ols(tr.rev.to_numpy(), design(tr, CHARS, mu, sd), ["const"] + CHARS)
    P(f"  fit on the {nn} s<1 MIX panels: R2 {r2:.4f}")
    P(fmt(tab, 4))
    resid = tr.rev.to_numpy() - design(tr, CHARS, mu, sd) @ b
    rse = float(np.sqrt((resid ** 2).sum() / max(1, nn - len(CHARS) - 1)))
    pred_etf = float(np.ravel(design(te, CHARS, mu, sd) @ b)[0])
    act_etf = float(te.rev.iloc[0])
    P(f"  ETF36: predicted {pred_etf:.4f}  actual {act_etf:.4f}  residual {act_etf-pred_etf:+.4f}  "
      f"= {(act_etf-pred_etf)/max(1e-9, rse):+.2f} residual sd (fit rse {rse:.4f})")
    P(f"  95% prediction band (+/-1.96 rse): [{pred_etf-1.96*rse:.4f}, {pred_etf+1.96*rse:.4f}]"
      f"  ->  ETF36 is {'OUTSIDE' if abs(act_etf-pred_etf) > 1.96*rse else 'INSIDE'} it")
    P("")
    P("  does the ETF share add anything BEYOND the four characteristics? (all 25 sweep panels)")
    for cols, lab in ((CHARS, "4 chars"), (CHARS + ["etf_share"], "4 chars + etf_share"),
                      (["etf_share"], "etf_share alone"),
                      (CHARS + CONTROLS, "4 chars + k, n_elig")):
        mu2, sd2 = zscore_fit(d, cols)
        tab, r2, ar2, nn, _ = ols(d.rev.to_numpy(), design(d, cols, mu2, sd2), ["const"] + cols)
        P(f"  [{lab}]  R2 {r2:.4f}  adjR2 {ar2:.4f}  n {nn}")
        P(fmt(tab, 4))
    P("  univariate Spearman(share, x) over the sweep:")
    rr = []
    for c in CHARS + CONTROLS + ["etf_share"]:
        rho, t, n = spearman(d[c], d.rev)
        rr.append(dict(x=c, rho=rho, t=t, n=n))
    P(fmt(pd.DataFrame(rr).set_index("x"), 4))

    # ---------------------------------------------------------------- rule 8
    P("")
    P("RULE 8 (i) THE RELATIONSHIP - fit on IS characteristics + IS reversals, read OOS once")
    tis = reversal_table(grid, COST_BPS, "IS_")
    toos = reversal_table(grid, COST_BPS, "OOS_")
    ci = chars[chars.tag == "IS"].set_index("panel")
    kk = ["panel", "r_target"]
    m = (tis[kk + ["source", "kind", "etf_share", "r_real"] + ["rev"]]
         .rename(columns={"rev": "rev_is"})
         .merge(toos[kk + ["rev"]].rename(columns={"rev": "rev_oos"}), on=kk)
         .merge(ci.reset_index()[["panel"] + CHARS], on="panel", how="left"))
    m = m.dropna(subset=CHARS)
    msw = m[m.etf_share.notna()].copy()           # the sweep cells, where s is defined
    fits = {"CHAR": CHARS + ["r_real"], "CHAR+s": CHARS + ["r_real", "etf_share"],
            "S_ONLY": ["etf_share"]}
    betas = {}
    grid_rows = []
    for lab, cols in fits.items():
        mu4, sd4 = zscore_fit(msw, cols)
        X = design(msw, cols, mu4, sd4)
        _, r2c, _, _, bc = ols(msw.rev_is.astype(float).to_numpy(), X, ["const"] + cols)
        msw[f"phat_{lab}"] = X @ bc
        betas[lab] = (cols, mu4, sd4, bc, r2c)
        for th in np.round(np.arange(0.05, 1.00, 0.05), 2):
            pr = msw[f"phat_{lab}"] >= th
            grid_rows.append(dict(rule=lab, threshold=float(th),
                                  IS_accuracy=float((pr == msw.rev_is).mean()),
                                  OOS_accuracy=float((pr == msw.rev_oos).mean()),
                                  predicted_rate=float(pr.mean())))
    for th in np.round(np.arange(0.05, 1.01, 0.05), 2):
        pr = msw.r_real < th
        grid_rows.append(dict(rule="R_THRESH", threshold=float(th),
                              IS_accuracy=float((pr == msw.rev_is).mean()),
                              OOS_accuracy=float((pr == msw.rev_oos).mean()),
                              predicted_rate=float(pr.mean())))
    gr = pd.DataFrame(grid_rows)
    gr.to_csv(OUT / f"{STEM}.threshold_grid.csv", index=False)
    for lab in fits:
        P(f"  IS fit [{lab}]: R2 {betas[lab][4]:.4f}, {len(msw)} sweep cells")
    P("  ALL threshold grid points (4 rules x 19-20 thresholds):")
    P(fmt(gr.set_index(["rule", "threshold"]).sort_index(), 4))

    bests = {}
    for lab in list(fits) + ["R_THRESH"]:
        g = gr[gr.rule == lab]
        bests[lab] = g.loc[g.IS_accuracy.idxmax()]
    maj_is = bool(msw.rev_is.mean() > 0.5)
    # ETF-END HOLD-OUT: train on s <= HOLDOUT_S, predict s > HOLDOUT_S
    ho_rows = []
    tr_m = msw[msw.etf_share <= HOLDOUT_S]
    te_m = msw[msw.etf_share > HOLDOUT_S]
    for lab, cols in fits.items():
        mu5, sd5 = zscore_fit(tr_m, cols)
        _, _, _, _, b5 = ols(tr_m.rev_is.astype(float).to_numpy(),
                             design(tr_m, cols, mu5, sd5), ["const"] + cols)
        ph = design(te_m, cols, mu5, sd5) @ b5
        pr = ph >= bests[lab].threshold
        ho_rows.append(dict(rule=lab, train_cells=len(tr_m), test_cells=len(te_m),
                            pred_rate=float(pr.mean()),
                            IS_acc_heldout=float((pr == te_m.rev_is).mean()),
                            OOS_acc_heldout=float((pr == te_m.rev_oos).mean())))
    ho = pd.DataFrame(ho_rows).set_index("rule")
    ho.to_csv(OUT / f"{STEM}.holdout.csv")
    P("")
    P(f"  ETF-END HOLD-OUT (train s<={HOLDOUT_S:.3f}, predict s>{HOLDOUT_S:.3f}); "
      f"held-out OOS base rate {max(te_m.rev_oos.mean(), 1-te_m.rev_oos.mean()):.4f}:")
    P(fmt(ho, 4))

    rivals = pd.DataFrame([
        dict(classifier=f"CONST (IS majority = {maj_is})",
             IS_acc=float((maj_is == msw.rev_is).mean()),
             OOS_acc=float((maj_is == msw.rev_oos).mean())),
        dict(classifier=f"R_THRESH (r < {bests['R_THRESH'].threshold:.2f})  [idea 269C]",
             IS_acc=bests["R_THRESH"].IS_accuracy, OOS_acc=bests["R_THRESH"].OOS_accuracy),
        dict(classifier=f"S_ONLY (phat >= {bests['S_ONLY'].threshold:.2f})  [ETF share alone]",
             IS_acc=bests["S_ONLY"].IS_accuracy, OOS_acc=bests["S_ONLY"].OOS_accuracy),
        dict(classifier=f"CHAR (phat >= {bests['CHAR'].threshold:.2f})  [idea 271's four]",
             IS_acc=bests["CHAR"].IS_accuracy, OOS_acc=bests["CHAR"].OOS_accuracy),
        dict(classifier=f"CHAR+s (phat >= {bests['CHAR+s'].threshold:.2f})",
             IS_acc=bests["CHAR+s"].IS_accuracy, OOS_acc=bests["CHAR+s"].OOS_accuracy),
    ]).set_index("classifier")
    base_rate = float(max(msw.rev_oos.mean(), 1 - msw.rev_oos.mean()))
    P("")
    P(f"  OOS majority base rate over the sweep cells = {base_rate:.4f} "
      f"(OOS reversal rate {msw.rev_oos.mean():.4f})")
    P(fmt(rivals, 4))
    rivals.to_csv(OUT / f"{STEM}.rivals.csv")
    m.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    msw.to_csv(OUT / f"{STEM}.sweep_cells.csv", index=False)

    # ---------------------------------------------------------------- rule 8 (ii) the book
    P("")
    P("RULE 8 (ii) THE BOOK - pooled equal-weight over the 5 NAMED panels, OOS read once")
    cols, mu6, sd6, b6, _ = betas["CHAR+s"]
    mall = m.copy()
    mall["etf_share"] = mall.etf_share.fillna(0.0)     # NAMED stock panels: no ETF content
    mall.loc[mall.panel == "B136", "etf_share"] = 36.0 / 136.0
    mall.loc[mall.panel == "U56", "etf_share"] = float(
        len([c for c in pool["U56"]["tradable"] if c in set(etf36)])) / len(pool["U56"]["tradable"])
    mall["phat"] = design(mall, cols, mu6, sd6) @ b6
    th = float(bests["CHAR+s"].threshold)
    sels = {}
    for pn in named5:
        dd = g10[(g10.panel == pn) & (g10.arm == "FWD")].sort_values("r_target")
        mm = mall[mall.panel == pn].sort_values("r_real")
        safe = mm[mm.phat < th]
        esel_n = int(dd.loc[dd.r_target == safe.iloc[0].r_target].iloc[0].n) if len(safe) else int(dd.iloc[-1].n)
        wsel = mm[mm.r_real >= float(bests["R_THRESH"].threshold)]
        rsel_n = int(dd.loc[dd.r_target == wsel.iloc[0].r_target].iloc[0].n) if len(wsel) else int(dd.iloc[-1].n)
        sels[pn] = dict(EWALL=("EWall", None),
                        FWD20=("FWD", int(dd.iloc[(dd.n - 20).abs().argmin()].n)),
                        S_SHARPE=("FWD", int(dd.loc[dd.IS_Sharpe.idxmax()].n)),
                        S_CAGR=("FWD", int(dd.loc[dd.IS_CAGR.idxmax()].n)),
                        ESEL=("FWD", esel_n), RSEL=("FWD", rsel_n),
                        V1=("v1", None), V2=("v2", None))
    P("  per-panel selections: " + "; ".join(
        f"{pn}: ESEL n={sels[pn]['ESEL'][1]}, RSEL n={sels[pn]['RSEL'][1]}, "
        f"S_SHARPE n={sels[pn]['S_SHARPE'][1]}, S_CAGR n={sels[pn]['S_CAGR'][1]}" for pn in named5))
    rows = []
    for lab in ["EWALL", "FWD20", "S_SHARPE", "S_CAGR", "ESEL", "RSEL", "V1", "V2"]:
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
    sp_p = pd.concat([cache[(pn, "EWall", None, COST_BPS)]["sp"] for pn in named5],
                     axis=1).mean(axis=1).dropna()
    sp_o = pd.concat([cache[(pn, "EWall", None, COST_BPS)]["sp_oos"] for pn in named5],
                     axis=1).mean(axis=1).dropna()
    ms, mso = metrics(sp_p), metrics(sp_o)
    h1, h2 = half_sharpes(sp_p)
    rows.append(dict(book="SPY", CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"],
                     H1=h1, H2=h2, OOS_CAGR=mso["CAGR"], OOS_Sharpe=mso["Sharpe"],
                     OOS_MaxDD=mso["MaxDD"]))
    wf = pd.DataFrame(rows).set_index("book")
    wf.to_csv(OUT / f"{STEM}.walkforward.csv")
    P(fmt(wf, 4))
    P("  (V2 is the live RULES v2 baseline; SPY is buy-and-hold, both pooled the same way)")

    # ------------------------------------------- rule 8 (iii) the sweep's own OOS book
    P("")
    P("RULE 8 (iii) the sweep rungs as books - OOS Sharpe/CAGR/MaxDD by ETF share "
      "(EWall and the IS-Sharpe pick, seed-averaged)")
    rr = []
    for s in SHARES:
        pans = [p for p, mt in pool.items() if mt["etf_share"] == s]
        if not pans:
            continue
        ew = [cache[(p, "EWall", None, COST_BPS)] for p in pans]
        pick = []
        for p in pans:
            dd = g10[(g10.panel == p) & (g10.arm == "FWD")]
            npick = int(dd.loc[dd.IS_Sharpe.idxmax()].n)
            pick.append(cache[(p, "FWD", npick, COST_BPS)])
        for lab, cs in (("EWall", ew), ("IS-Sharpe pick", pick)):
            po = pd.concat([c["r_oos"] for c in cs], axis=1).mean(axis=1).dropna()
            pf = pd.concat([c["r"] for c in cs], axis=1).mean(axis=1).dropna()
            mo_, mf_ = metrics(po), metrics(pf)
            rr.append(dict(etf_share=s, book=lab, panels=len(pans), CAGR=mf_["CAGR"],
                           Sharpe=mf_["Sharpe"], MaxDD=mf_["MaxDD"],
                           OOS_CAGR=mo_["CAGR"], OOS_Sharpe=mo_["Sharpe"],
                           OOS_MaxDD=mo_["MaxDD"]))
    sb = pd.DataFrame(rr).set_index(["book", "etf_share"]).sort_index()
    sb.to_csv(OUT / f"{STEM}.sweepbooks.csv")
    P(fmt(sb, 4))
    spy_row = g10[g10.panel == "ETF36"].iloc[0]
    P(f"  SPY over the same window: {spy_row.SPY_CAGR:.2%}/{spy_row.SPY_Sharpe:.4f}/"
      f"{spy_row.SPY_MaxDD:.2%}, OOS {spy_row.SPY_OOS_CAGR:.2%}/{spy_row.SPY_OOS_Sharpe:.4f}/"
      f"{spy_row.SPY_OOS_MaxDD:.2%}")

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("KEEP paths on ALL grid points (4a vs live RULES v2; 4b vs SPY + rule 8):")
    for bps in (COST_BPS, DIAG_BPS):
        g = grid[grid.bps == bps]
        P(f"  @{bps} bps: 4a {int(g.p4a.sum())}/{len(g)}   4a(vs v1) {int(g.p4a_v1.sum())}/{len(g)}"
          f"   4b {int(g.p4b.sum())}/{len(g)}")
    g10b = grid[grid.bps == COST_BPS]
    P("  4b passes @10 bps by kind and arm:")
    tb = g10b[g10b.p4b].groupby(["kind", "arm"]).size().rename("passes").to_frame()
    P(fmt(tb, 0) if len(tb) else "    none")
    P("  4b pass RATE by ETF-share rung (the sweep only):")
    sws = g10b[g10b.etf_share.notna()]
    P(fmt(sws.groupby("etf_share").agg(points=("p4b", "size"), passes=("p4b", "sum"),
                                       rate=("p4b", "mean")), 4))
    P("  binding bar over the @10 bps failures:")
    fb = g10b[~g10b.p4b].f4b.str.split(",").explode().value_counts()
    P(fmt(fb.rename("count").to_frame(), 0))
    keep = g10b[g10b.p4b].sort_values("Sharpe", ascending=False)
    keep.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("  top 15 of the @10 bps 4b passes:")
    P(fmt(keep.head(15)[["panel", "etf_share", "arm", "n", "CAGR", "Sharpe", "MaxDD", "H1",
                         "H2", "OOS_Sharpe", "turn"]].set_index("panel"), 4)
      if len(keep) else "    none")
    kn = keep[keep.kind == "NAMED"]
    P("  NAMED-panel 4b passes @10 bps (the only cells the record can act on):")
    P(fmt(kn[["panel", "arm", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
              "turn"]].set_index("panel"), 4) if len(kn) else "    none")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"wrote {STEM}.{{grid,chars,reversal,panelshare,curve,shape,threshold_grid,holdout,"
      f"rivals,cells,sweep_cells,walkforward,sweepbooks,keep,console}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
