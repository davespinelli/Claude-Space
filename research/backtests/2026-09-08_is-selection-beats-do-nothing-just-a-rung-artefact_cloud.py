#!/usr/bin/env python3
"""Idea 235 — is-selection-beats-do-nothing-just-a-rung-artefact (cloud lane, 2026-09-08).

Pre-registered question (QUEUE 235): idea 230's rule-8 premium is monotone in the cost rung for
BOTH the IS chooser (-0.0161 at 0 bps -> +0.1055 at 30) and a RANDOM dial (-0.0275 -> +0.0076),
and is a coin flip at PROTOCOL's own 10 bps.  Re-read every published "selection beats
do-nothing" claim against the rung it was quoted at and the do-nothing book's own turnover
break-even.

THE HYPOTHESIS BEING TESTED, stated so it can fail: a "selection beats do-nothing" premium is a
RUNG ARTEFACT if (i) it grows monotonically with the cost rung, (ii) a random arm of the same
grid earns the same growth, and (iii) it is explained by the TURNOVER DIFFERENCE between the
picked arm and the do-nothing arm rather than by which names get held.  Under that hypothesis
the chooser is not selecting return, it is selecting LOW TURNOVER, and at a low enough rung the
premium vanishes or reverses.  The falsifier is a premium that survives net of the random arm
and is not a function of dturn * c.

TWO TUNED PARAMETERS ONLY:
    p1 = COMPARAND — what "not choosing" means  {MEDIAN arm, RANDOM (mean over arms)}
         Both are parameter-free readings of the same swept grid; no arm is hand-picked.
    p2 = RUNG at which the claim is read  {0, 5, 10, 15, 20, 25, 30 bps}   ALL POINTS REPORTED
Nothing else is tuned.  The ORACLE (full-sample argmax) is reported as a ceiling, never as a
comparand choice.

PART A (the archive): every committed CSV carrying a cost rung + IS_Sharpe + OOS_Sharpe is
re-read as a selection claim — pick = argmax IS_Sharpe AT THAT RUNG, read OOS_Sharpe once —
and the premium is reported at every rung against both comparands, with the do-nothing arm's
own turnover break-even wherever a turnover column is committed.
PART B (live, PROTOCOL rule 8): 3 panels x 4 dials x 7 rungs re-simulated from prices, IS =
2009-2016, OOS = 2017-2026 read once, so the turnover of every arm is known exactly and the
artefact can be priced rather than inferred.  Both KEEP paths (4a and 4b) on every grid point,
against RULES v1, RULES v2 and SPY.

SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen only (see
data/SMALL_PANEL_README.md); the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first (483 -> SMALL439).  Small-panel numbers are upper bounds.

Outputs (all committed):
    .census.csv       every archive (file, dial, cell, rung): pick, comparands, premia, turnover
    .rungcurve.csv    premium vs rung, by comparand, archive and live
    .grid.csv         Part B: every (panel, dial, value, rung) point with 4a/4b bars
    .walkforward.csv  Part B rule 8: IS pick per rung, OOS read once, all comparands
    .decomp.csv       Part B: premium vs the turnover-difference prediction, per cell
    .keep.csv         4a/4b pass counts per (panel, dial, rung)
"""
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics                                          # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
SELF = Path(__file__).name

COST_NAMES = {"bps", "cost_bps", "cost", "rung", "cost_rung", "bps_rung", "c_bps"}
TURN_NAMES = {"turnover", "to", "turn", "turn_yr", "turnover_yr", "turn_per_yr", "TO_yr"}
METRIC_SUBSTR = ("sharpe", "cagr", "maxdd", "dd", "vol", "turn", "gross", "pass", "fail",
                 "p4a", "p4b", "f4b", "m_", "oos", "_is", "is_", "h1", "h2", "ret", "equity",
                 "pval", "p_", "_p", "z", "ci", "sd", "std", "mean", "median", "hit", "win",
                 "margin", "regret", "room", "excess", "premium", "delta", "d_", "rho", "corr",
                 "n_", "count", "seed", "invested", "held", "episodes", "days", "bind", "y20",
                 "sortino", "calmar", "alpha", "beta", "te", "ir", "skew", "kurt", "auc")
COMPARANDS = ["MEDIAN", "RANDOM"]


def is_metric(col):
    c = str(col).lower()
    return any(s in c for s in METRIC_SUBSTR)


def named(cols, names):
    for c in cols:
        if str(c).strip().lower() in names:
            return c
    return None


def exact(cols, name):
    for c in cols:
        if str(c).strip().lower() == name:
            return c
    return None


def read_cell(piv_is, piv_oos, piv_turn):
    """One (dial values) x (cost rungs) rectangle re-read as a selection claim at every rung.

    pick(c)      = argmax_d IS_Sharpe(d, c)                    chosen in-sample, at THIS rung
    pick0        = argmax_d IS_Sharpe(d, c_lo)                 the cost-blind chooser
    MEDIAN       = the middle arm of the swept grid            "do nothing", parameter-free
    RANDOM       = mean OOS over all arms                      "any arm at all"
    ORACLE       = max OOS over arms                           ceiling, not a comparand
    """
    vals = list(piv_is.index)
    rungs = sorted(piv_is.columns)
    med = vals[len(vals) // 2]
    pick0 = piv_is[rungs[0]].idxmax()
    out = []
    for c in rungs:
        pick = piv_is[c].idxmax()
        o = piv_oos[c]
        row = dict(bps=float(c), n_values=len(vals), pick=pick, pick0=pick0, median_arm=med,
                   OOS_pick=float(o[pick]), OOS_pick0=float(o[pick0]),
                   OOS_MEDIAN=float(o[med]), OOS_RANDOM=float(o.mean()),
                   OOS_ORACLE=float(o.max()),
                   prem_MEDIAN=float(o[pick] - o[med]),
                   prem_RANDOM=float(o[pick] - o.mean()),
                   rand_minus_MEDIAN=float(o.mean() - o[med]),
                   pick_moved=bool(pick != pick0))
        if piv_turn is not None:
            t = piv_turn[c]
            row.update(turn_pick=float(t[pick]), turn_MEDIAN=float(t[med]),
                       dturn=float(t[med] - t[pick]))
        out.append(row)
    return out


def scan_archive():
    """Every committed CSV with a cost rung + IS_Sharpe + OOS_Sharpe, re-read as a selection
    claim.  Dial/cell detection is idea 231's, unchanged: numeric id column with 3..60 values,
    grouping columns bijective with the dial dropped, complete rectangle required."""
    rows, seen, t0, files_used = [], 0, time.time(), set()
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(SELF.replace(".py", "")):
            continue
        seen += 1
        if seen % 400 == 0:
            print(f"    ...{seen} files, {len(rows)} rung-readings, {time.time()-t0:.0f}s", flush=True)
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) < 6:
            continue
        ccol = named(df.columns, COST_NAMES)
        icol, ocol = exact(df.columns, "is_sharpe"), exact(df.columns, "oos_sharpe")
        tcol = named(df.columns, TURN_NAMES)
        if ccol is None or icol is None or ocol is None:
            continue
        for c in (ccol, icol, ocol) + ((tcol,) if tcol else ()):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df[df[ccol].notna() & df[icol].notna() & df[ocol].notna()].copy()
        if len(df) < 6 or df[ccol].nunique() < 2:
            continue
        used = {ccol, icol, ocol, tcol}
        ids = [c for c in df.columns if c not in used and not is_metric(c) and df[c].nunique() > 1]
        dials = [c for c in ids if pd.api.types.is_numeric_dtype(df[c]) and 3 <= df[c].nunique() <= 60]
        vals = [icol, ocol] + ([tcol] if tcol else [])
        for d in dials:
            nd = df[d].nunique()
            grp = [g for g in ids if g != d]
            grp = [g for g in grp if not (df[g].nunique() == nd and df.groupby(d)[g].nunique().max() == 1
                                          and df.groupby(g)[d].nunique().max() == 1)]
            grp = [g for g in grp if df[g].nunique() <= 200]
            agg = df.groupby(grp + [d, ccol], dropna=False, sort=False)[vals].median().reset_index()
            if grp:
                keys = agg[grp[0]].astype(str)
                for g in grp[1:]:
                    keys = keys + "|" + agg[g].astype(str)
            else:
                keys = pd.Series("_", index=agg.index)
            agg["_k"] = keys.values
            sz = agg.groupby("_k", sort=False).size()
            big = sz[sz >= 6].index
            if not len(big):
                continue
            for k, sub in agg[agg._k.isin(big)].groupby("_k", sort=False):
                nv, nc = sub[d].nunique(), sub[ccol].nunique()
                if nv < 3 or nc < 2 or len(sub) != nv * nc:
                    continue
                pi = sub.pivot(index=d, columns=ccol, values=icol)
                po = sub.pivot(index=d, columns=ccol, values=ocol)
                pt = sub.pivot(index=d, columns=ccol, values=tcol) if tcol else None
                if pi.isna().any().any() or po.isna().any().any():
                    continue
                if po.nunique().max() < 2:            # OOS identical across arms: no claim
                    continue
                files_used.add(f.name)
                for r in read_cell(pi, po, pt):
                    rows.append(dict(file=f.name, dial=d, cell=str(k)[:80],
                                     has_turnover=pt is not None, **r))
    C = pd.DataFrame(rows)
    print(f"    scan done: {seen} files scanned, {len(files_used)} usable, "
          f"{len(C)} rung-readings, {time.time()-t0:.0f}s", flush=True)
    return C


def sign_test(x):
    """Two-sided exact-ish sign test on a vector of premia (normal approx, n large)."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x) & (x != 0)]
    n = len(x)
    if n < 5:
        return np.nan, np.nan, n
    k = int((x > 0).sum())
    z = (k - n / 2) / np.sqrt(n / 4)
    from math import erfc, sqrt
    return k / n, float(erfc(abs(z) / sqrt(2))), n


def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3 or np.ptp(x[m]) == 0:
        return np.nan, np.nan
    b, a = np.polyfit(x[m], y[m], 1)
    yhat = a + b * x[m]
    ss = ((y[m] - y[m].mean()) ** 2).sum()
    return float(b), float(1 - ((y[m] - yhat) ** 2).sum() / ss) if ss > 0 else np.nan


# ------------------------------------------------------------------ Part B: live
RUNGS = [0, 5, 10, 15, 20, 25, 30]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1)
DIAL_VALUES = {"N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
               "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
               "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
               "K": [1, 2, 3, 4, 6, 8, 13]}


def load_small439():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {px.shape[1]-len(keep)} of {px.shape[1]-1} names "
          f"(max_1d_move >= 1.0) -> {len(keep)-1} constituents", flush=True)
    return px[keep]


def week_mask(idx, k):
    per = idx.to_period("W")
    s = pd.Series(per, index=idx)
    last = (s != s.shift(-1)).values
    if k == 1:
        return last
    ordinal = pd.Series(pd.factorize(per)[0], index=idx).values
    return last & ((ordinal % k) == 0)


def simulate(px, W, mask):
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1]); held = np.empty_like(rets); turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index))


def book_weights(px, comp, ma, vol20, n, g, max_vol):
    if g == 0:
        above = px > ma
    else:
        sig = pd.DataFrame(np.where(px > ma * (1 + g), 1.0, np.where(px < ma * (1 - g), 0.0, np.nan)),
                           index=px.index, columns=px.columns)
        above = sig.ffill().fillna(0.0) > 0.5
    elig = comp.where(above & (vol20 < max_vol))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) / n


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]: f.append("H1")
    if not s["H2"] > b["H2"]: f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: f.append("DD")
    return ",".join(f)


def bars_4b(s, spy, oos_s, oos_spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not oos_s > oos_spy: f.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return ",".join(f)


def part_b():
    t0 = time.time()
    grid = []
    for pname, px in (("U56", load_universe()), ("B136", load_universe(broad=True)),
                      ("SMALL439", load_small439())):
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r); spy_o = metrics(spy_r.loc[OOS_START:])
        bg, bt = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base = {c: stats(net(bg, bt, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(bg, bt, c).loc[OOS_START:]) for c in RUNGS}
        vg, vt = simulate(px, rules_v2_weights(px), week_mask(px.index, 1))
        v2_oos = {c: metrics(net(vg, vt, c).loc[OOS_START:]) for c in RUNGS}
        for dial, values in DIAL_VALUES.items():
            for v in values:
                kw = dict(DEFAULTS); kw[dial] = v
                if dial == "N" and v > px.shape[1] - 1:
                    continue
                W = book_weights(px, comp, ma, vol20, kw["N"], kw["G"], kw["V"])
                g_, t_ = simulate(px, W, week_mask(px.index, kw["K"]))
                g_, t_ = g_.loc[start:], t_.loc[start:]
                yrs = len(g_) / 252
                yrs_oos = len(g_.loc[OOS_START:]) / 252
                for c in RUNGS:
                    r = net(g_, t_, c); st = stats(r); o = metrics(r.loc[OOS_START:])
                    ir = r.loc[:IS_END]
                    grid.append(dict(panel=pname, dial=dial, value=v, bps=c,
                                     turn_yr=t_.sum() / yrs,
                                     turn_yr_oos=t_.loc[OOS_START:].sum() / yrs_oos,
                                     turn_yr_is=t_.loc[:IS_END].sum() / (len(ir) / 252),
                                     OOS_vol=r.loc[OOS_START:].std() * np.sqrt(252), **st,
                                     IS_Sharpe=metrics(ir)["Sharpe"],
                                     OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     fail4a=bars_4a(st, base[c]),
                                     fail4b=bars_4b(st, spy_s, o["Sharpe"], spy_o["Sharpe"]),
                                     spy_Sharpe=spy_s["Sharpe"], spy_CAGR=spy_s["CAGR"],
                                     spy_MaxDD=spy_s["MaxDD"],
                                     spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                                     spy_OOS_MaxDD=spy_o["MaxDD"],
                                     v1_Sharpe=base[c]["Sharpe"],
                                     v1_OOS_Sharpe=base_oos[c]["Sharpe"],
                                     v1_OOS_CAGR=base_oos[c]["CAGR"],
                                     v1_OOS_MaxDD=base_oos[c]["MaxDD"],
                                     v2_OOS_Sharpe=v2_oos[c]["Sharpe"]))
        print(f"  {pname}: {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame(grid)


def walk_forward(G):
    """PROTOCOL rule 8.  Pick on 2009-2016 IS Sharpe at each rung; 2017-2026 read once.
    do-nothing = the LIVE default arm (RULES' own value), median = the middle swept arm,
    random = mean over arms, oracle = the OOS argmax (ceiling)."""
    wf = []
    for (p_, d_), sub in G.groupby(["panel", "dial"]):
        vals = sorted(sub.value.unique())
        med, dn = vals[len(vals) // 2], DEFAULTS[d_]
        pi = sub.pivot_table(index="value", columns="bps", values="IS_Sharpe")
        pick0 = pi[min(pi.columns)].idxmax()
        for c in RUNGS:
            o = sub[sub.bps == c].set_index("value")
            pick = pi[c].idxmax()
            wf.append(dict(panel=p_, dial=d_, bps=c, pick=pick, pick0=pick0,
                           median_arm=med, do_nothing=dn, pick_moved=bool(pick != pick0),
                           OOS_pick=float(o.OOS_Sharpe[pick]), OOS_pick0=float(o.OOS_Sharpe[pick0]),
                           OOS_DN=float(o.OOS_Sharpe[dn]), OOS_MEDIAN=float(o.OOS_Sharpe[med]),
                           OOS_RANDOM=float(o.OOS_Sharpe.loc[vals].mean()),
                           OOS_ORACLE=float(o.OOS_Sharpe.max()),
                           prem_DN=float(o.OOS_Sharpe[pick] - o.OOS_Sharpe[dn]),
                           prem_MEDIAN=float(o.OOS_Sharpe[pick] - o.OOS_Sharpe[med]),
                           prem_RANDOM=float(o.OOS_Sharpe[pick] - o.OOS_Sharpe.loc[vals].mean()),
                           rand_prem_DN=float(o.OOS_Sharpe.loc[vals].mean() - o.OOS_Sharpe[dn]),
                           CAGR_pick=float(o.OOS_CAGR[pick]), CAGR_DN=float(o.OOS_CAGR[dn]),
                           CAGR_RANDOM=float(o.OOS_CAGR.loc[vals].mean()),
                           MaxDD_pick=float(o.OOS_MaxDD[pick]), MaxDD_DN=float(o.OOS_MaxDD[dn]),
                           turn_pick=float(o.turn_yr_oos[pick]), turn_DN=float(o.turn_yr_oos[dn]),
                           turn_RANDOM=float(o.turn_yr_oos.loc[vals].mean()),
                           vol_pick=float(o.OOS_vol[pick]), vol_DN=float(o.OOS_vol[dn]),
                           v1_OOS_Sharpe=float(o.v1_OOS_Sharpe.iloc[0]),
                           v1_OOS_CAGR=float(o.v1_OOS_CAGR.iloc[0]),
                           v1_OOS_MaxDD=float(o.v1_OOS_MaxDD.iloc[0]),
                           v2_OOS_Sharpe=float(o.v2_OOS_Sharpe.iloc[0]),
                           spy_OOS_Sharpe=float(o.spy_OOS_Sharpe.iloc[0]),
                           spy_OOS_CAGR=float(o.spy_OOS_CAGR.iloc[0]),
                           spy_OOS_MaxDD=float(o.spy_OOS_MaxDD.iloc[0])))
    W = pd.DataFrame(wf)
    # the artefact's own prediction: a premium bought purely by holding a lower-turnover arm is
    #   dSharpe(c) = (turn_DN - turn_pick) * c/1e4 / vol      (annual turnover, annualised vol)
    W["pred_turn_DN"] = (W.turn_DN - W.turn_pick) * W.bps / 1e4 / W.vol_pick
    W["resid_DN"] = W.prem_DN - W.pred_turn_DN
    return W


# ------------------------------------------------------------------ main
def main():
    print("=" * 92)
    print("PART A — re-read every archived selection claim rung by rung")
    print("=" * 92)
    C = scan_archive()
    C.to_csv(f"{OUT}.census.csv", index=False)
    print(f"\n  corpus: {len(C)} rung-readings, {C.file.nunique()} files, "
          f"{C.dial.nunique()} dial columns, {C.groupby(['file','dial','cell']).ngroups} cells; "
          f"turnover committed on {C.has_turnover.mean():.1%} of readings")

    curve = []
    print(f"\n=== p2 = RUNG the claim is read at, p1 = COMPARAND (all grid points) ===")
    print(f"  {'p1':8s} {'rung':>5s} {'n':>6s} {'mean prem':>10s} {'median':>9s} {'win rate':>9s} "
          f"{'sign p':>8s} {'RANDOM-arm prem':>16s} {'selection only':>15s}")
    for comp in COMPARANDS:
        for c in sorted(C.bps.unique()):
            S = C[C.bps == c]
            if len(S) < 20:
                continue
            prem = S[f"prem_{comp}"]
            rnd = S["rand_minus_MEDIAN"] if comp == "MEDIAN" else pd.Series(0.0, index=S.index)
            sel = prem - rnd
            w, p, n = sign_test(prem)
            curve.append(dict(source="ARCHIVE", comparand=comp, bps=c, n=len(S),
                              mean_prem=float(prem.mean()), median_prem=float(prem.median()),
                              win_rate=w, sign_p=p, mean_rand_prem=float(rnd.mean()),
                              mean_selection_only=float(sel.mean())))
            print(f"  {comp:8s} {c:5.0f} {len(S):6d} {prem.mean():+10.4f} {prem.median():+9.4f} "
                  f"{w:9.3f} {p:8.4f} {rnd.mean():+16.4f} {sel.mean():+15.4f}")
    A = pd.DataFrame(curve)
    for comp in COMPARANDS:
        S = A[A.comparand == comp]
        b, r2 = slope(S.bps, S.mean_prem)
        print(f"  slope of mean premium in the rung [{comp}]: {b:+.6f} Sharpe/bp "
              f"(R2 {r2:.3f}) -> {b*30:+.4f} over a 0-30 bps span")
    b, r2 = slope(A[A.comparand == "MEDIAN"].bps, A[A.comparand == "MEDIAN"].mean_rand_prem)
    print(f"  slope of the RANDOM ARM's own premium over MEDIAN: {b:+.6f} Sharpe/bp (R2 {r2:.3f})"
          f" — the null carries the same rung tilt iff this is nonzero")

    print("\n=== weighting check: cells are NOT independent (one file can commit thousands) ===")
    top = C[C.bps == C.bps.median()].file.value_counts()
    print(f"  heaviest files at the median rung: "
          + ", ".join(f"{k.split('_')[-1]}({v})" for k, v in top.head(3).items()))
    print(f"  {'rung':>5s} {'cells':>6s} {'files':>6s} {'cell-wtd MEDIAN':>16s} {'win':>5s} {'p':>7s} "
          f"{'file-wtd MEDIAN':>16s} {'win':>5s} {'p':>7s} {'file-wtd RANDOM':>16s} {'win':>5s} {'p':>7s}")
    for c in sorted(C.bps.unique()):
        S = C[C.bps == c]
        if len(S) < 20:
            continue
        fm = S.groupby("file").prem_MEDIAN.mean()
        fr = S.groupby("file").prem_RANDOM.mean()
        w0, p0, _ = sign_test(S.prem_MEDIAN)
        w1, p1, n1 = sign_test(fm)
        w2, p2, _ = sign_test(fr)
        print(f"  {c:5.0f} {len(S):6d} {S.file.nunique():6d} {S.prem_MEDIAN.mean():+16.4f} "
              f"{w0:5.2f} {p0:7.4f} {fm.mean():+16.4f} {w1:5.2f} {p1:7.4f} "
              f"{fr.mean():+16.4f} {w2:5.2f} {p2:7.4f}")
        curve.append(dict(source="ARCHIVE_FILEWTD", comparand="MEDIAN", bps=c, n=int(n1),
                          mean_prem=float(fm.mean()), median_prem=float(fm.median()),
                          win_rate=w1, sign_p=p1, mean_rand_prem=np.nan,
                          mean_selection_only=float(fr.mean())))
    b, r2 = slope([c for c in sorted(C.bps.unique()) if (C.bps == c).sum() >= 20],
                  [C[C.bps == c].groupby("file").prem_MEDIAN.mean().mean()
                   for c in sorted(C.bps.unique()) if (C.bps == c).sum() >= 20])
    print(f"  slope of the FILE-WEIGHTED mean premium in the rung: {b:+.6f} Sharpe/bp (R2 {r2:.3f})")

    print("\n=== the do-nothing book's own turnover break-even (archive cells with turnover) ===")
    T = C[C.has_turnover & C.dturn.notna()]
    if len(T):
        for c in sorted(T.bps.unique()):
            S = T[T.bps == c]
            if len(S) < 20:
                continue
            b, r2 = slope(S.dturn * c, S.prem_MEDIAN)
            print(f"  rung {c:5.0f} bps  n {len(S):5d}  mean dturn (do-nothing minus pick) "
                  f"{S.dturn.mean():+9.2f} /yr  premium ~ dturn*c: slope {b:+.3e} R2 {r2:.3f}")
        lo = T[T.bps == T.bps.min()]
        print(f"  at the LOWEST rung the record quotes ({lo.bps.iloc[0]:.0f} bps): mean premium "
              f"{lo.prem_MEDIAN.mean():+.4f}, win rate {sign_test(lo.prem_MEDIAN)[0]:.3f}")

    print("\n" + "=" * 92)
    print("PART B — live, PROTOCOL rule 8: pick on 2009-2016, read 2017-2026 once")
    print("=" * 92)
    G = part_b()
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    G.groupby(["panel", "dial", "bps"])[["pass4a", "pass4b"]].sum().reset_index().to_csv(
        f"{OUT}.keep.csv", index=False)
    W = walk_forward(G)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    print(f"\n=== live rung curve, 12 (panel x dial) cells per rung — OOS Sharpe ===")
    print(f"  {'rung':>5s} {'pick':>8s} {'do-noth':>8s} {'median':>8s} {'random':>8s} {'oracle':>8s} "
          f"{'prem_DN':>9s} {'rand_DN':>9s} {'SELECTION':>10s} {'win':>5s} {'p':>7s}")
    for c in RUNGS:
        S = W[W.bps == c]
        sel = S.prem_DN - S.rand_prem_DN
        w, p, n = sign_test(S.prem_DN)
        print(f"  {c:5d} {S.OOS_pick.mean():8.4f} {S.OOS_DN.mean():8.4f} {S.OOS_MEDIAN.mean():8.4f} "
              f"{S.OOS_RANDOM.mean():8.4f} {S.OOS_ORACLE.mean():8.4f} {S.prem_DN.mean():+9.4f} "
              f"{S.rand_prem_DN.mean():+9.4f} {sel.mean():+10.4f} {w if w==w else float('nan'):5.2f} "
              f"{p if p==p else float('nan'):7.3f}")
        curve.append(dict(source="LIVE", comparand="DO_NOTHING", bps=c, n=len(S),
                          mean_prem=float(S.prem_DN.mean()), median_prem=float(S.prem_DN.median()),
                          win_rate=w, sign_p=p, mean_rand_prem=float(S.rand_prem_DN.mean()),
                          mean_selection_only=float(sel.mean())))
    pd.DataFrame(curve).to_csv(f"{OUT}.rungcurve.csv", index=False)
    b1, r1 = slope(W.bps, W.prem_DN)
    b2, r2_ = slope(W.bps, W.rand_prem_DN)
    print(f"\n  slope in the rung: CHOOSER premium {b1:+.6f}/bp (R2 {r1:.3f}), "
          f"RANDOM ARM premium {b2:+.6f}/bp (R2 {r2_:.3f}) — "
          f"{'THE NULL CARRIES THE SAME TILT' if b2 > 0.5 * b1 else 'the null does NOT carry it'}")

    print("\n=== is the premium bought by TURNOVER? (live, exact turnover per arm) ===")
    W.to_csv(f"{OUT}.decomp.csv", index=False)
    b, r2 = slope(W.pred_turn_DN, W.prem_DN)
    print(f"  premium_DN vs its own turnover prediction (turn_DN - turn_pick)*c/1e4/vol: "
          f"slope {b:+.3f}, R2 {r2:.3f} over {len(W)} cells")
    print(f"  mean predicted {W.pred_turn_DN.mean():+.4f}  mean actual {W.prem_DN.mean():+.4f}  "
          f"mean residual {W.resid_DN.mean():+.4f}")
    for c in (0, 10, 30):
        S = W[W.bps == c]
        wr, p, n = sign_test(S.resid_DN)
        print(f"    rung {c:2d}: predicted {S.pred_turn_DN.mean():+.4f}  actual {S.prem_DN.mean():+.4f}"
              f"  residual {S.resid_DN.mean():+.4f} (win {wr:.2f}, sign p {p:.3f})")
    print(f"  mean turnover of the picked arm {W.turn_pick.mean():.2f}/yr vs the do-nothing arm "
          f"{W.turn_DN.mean():.2f}/yr (random arm {W.turn_RANDOM.mean():.2f}/yr) -> the chooser "
          f"picks a {'LOWER' if W.turn_pick.mean() < W.turn_DN.mean() else 'HIGHER'}-turnover book")
    lo, hi = W[W.bps == 0], W[W.bps == 30]
    print(f"  break-even: chooser premium is {lo.prem_DN.mean():+.4f} at 0 bps and "
          f"{hi.prem_DN.mean():+.4f} at 30 bps")

    print("\n=== rule 8 headline at PROTOCOL's own 10 bps (12 panel x dial cells) ===")
    t = W[W.bps == 10]
    for nm, s, cg, dd in (("IS chooser", "OOS_pick", "CAGR_pick", "MaxDD_pick"),
                          ("do-nothing", "OOS_DN", "CAGR_DN", "MaxDD_DN")):
        print(f"  {nm:11s} OOS Sharpe {t[s].mean():.4f}  CAGR {t[cg].mean():.2%}  MaxDD {t[dd].mean():.2%}")
    print(f"  random arm  OOS Sharpe {t.OOS_RANDOM.mean():.4f}  CAGR {t.CAGR_RANDOM.mean():.2%}")
    wr, p, n = sign_test(t.prem_DN)
    print(f"  chooser minus do-nothing at 10 bps: mean {t.prem_DN.mean():+.4f}, "
          f"wins {int(wr*n)}/{n} (sign p {p:.3f}); net of the random arm "
          f"{(t.prem_DN - t.rand_prem_DN).mean():+.4f}")
    for p_ in ("U56", "B136", "SMALL439"):
        s = t[t.panel == p_].iloc[0]
        print(f"  {p_:9s} RULES v1 OOS {s.v1_OOS_Sharpe:.4f} (CAGR {s.v1_OOS_CAGR:.2%}, "
              f"MaxDD {s.v1_OOS_MaxDD:.2%})  RULES v2 {s.v2_OOS_Sharpe:.4f}  "
              f"SPY {s.spy_OOS_Sharpe:.4f} (CAGR {s.spy_OOS_CAGR:.2%}, MaxDD {s.spy_OOS_MaxDD:.2%})")

    print("\n=== KEEP paths over all Part B grid points ===")
    print(f"  4a {int(G.pass4a.sum())} / {len(G)}    4b {int(G.pass4b.sum())} / {len(G)}")
    for p_ in ("U56", "B136", "SMALL439"):
        s = G[G.panel == p_]
        print(f"    {p_:9s} 4a {int(s.pass4a.sum()):3d}/{len(s)}   4b {int(s.pass4b.sum()):3d}/{len(s)}")
    fb = G[~G.pass4b].fail4b.str.split(",").explode().value_counts()
    print("  4b failing bars (sole + joint): " + ", ".join(f"{k} {v}" for k, v in fb.items()))
    print("\n  full sample at 10 bps, best Sharpe per panel:")
    for p_ in ("U56", "B136", "SMALL439"):
        s = G[(G.panel == p_) & (G.bps == 10)].nlargest(1, "Sharpe").iloc[0]
        print(f"    {p_:9s} {s.dial}={s.value}  Sharpe {s.Sharpe:.3f} (H1 {s.H1:.3f}/H2 {s.H2:.3f})  "
              f"CAGR {s.CAGR:.2%}  MaxDD {s.MaxDD:.2%}  OOS {s.OOS_Sharpe:.3f}  "
              f"4a {'PASS' if s.pass4a else s.fail4a}  4b {'PASS' if s.pass4b else s.fail4b}")


if __name__ == "__main__":
    main()
