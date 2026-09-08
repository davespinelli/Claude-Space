#!/usr/bin/env python3
"""Idea 453 — does-the-MATCHED-margin-hold-off-the-Sharpe-statistic (cloud lane, 2026-09-08).

Pre-registered question (QUEUE 453): idea 231 found the per-name MATCHED margin

    matched(cell) = max_{d != best} [ (slope_d - slope_best)*(c_hi - c_lo)
                                      - (S(best, c_lo) - S(d, c_lo)) ]
    predict "the argmax moves with the cost rung" iff matched > 0

is an EXACT argmax reader on 8,529 of 8,529 committed cells, and idea 231 attributes that to
Sharpe's numerator being linear in the cost rung (net(c) = gross - turn*c/1e4 shifts the mean
exactly, and the denominator barely moves).  Re-run the same back-fill on the record's OTHER
swept statistics, where linearity does NOT hold, and report where the identity breaks.

TWO TUNED PARAMETERS ONLY:
    p1 = STATISTIC family read off each committed grid  {Sharpe, CAGR, MaxDD, OOS_Sharpe, M4B}
    p2 = DETECTION rule for "a swept dial inside a committed grid CSV"  {STRICT, LOOSE}
Nothing else is tuned.  The MATCHED margin itself is parameter-free (no threshold to pick):
its sign IS the prediction.  All grid points of both parameters are reported.

WHY THE STATISTIC SHOULD MATTER (the pre-registered mechanism):
    Sharpe(d,c) = (mean_d - turn_d*c/1e4)*252 / sd(d,c)      numerator EXACTLY affine in c
    CAGR(d,c)   = prod_t(1 + r_t - turn_t*c/1e4)^(252/T) - 1  degree-T polynomial in c
    MaxDD(d,c)  = min over a running max of that product      piecewise, non-smooth in c
    4b margins  = differences of the above against a SPY bar  inherit their parent's curvature
MATCHED is an identity only for a statistic affine in c.  A non-affine statistic can re-rank
between two rungs that the two ENDPOINT rungs cannot see, so MATCHED can miss (FN) as well as
over-fire (FP).  This script measures the break rate per statistic and prices the curvature.

Sign convention: every statistic is read HIGHER-IS-BETTER (MaxDD is negative, so argmax picks
the shallowest drawdown; the 4b margins are already signed as slack over the bar).

PART A (the archive): one pass over every committed CSV in research/backtests; for each
(file, dial, cell, statistic) rectangle, gap / tilt / MATCHED margin / actual re-rank.
PART B (live, PROTOCOL rule 8): 3 panels x 4 dials x 7 cost rungs re-simulated from prices, so
the SAME book is read by all five statistics at once.  Measures (i) the affinity residual that
drives the identity, (ii) the MATCHED break rate per statistic on live cells, (iii) rule 8:
gate and dial chosen on 2009-2016 only, 2017-2026 read once, OOS CAGR/Sharpe/MaxDD against
RULES v1, RULES v2 and SPY, with both KEEP paths (4a and 4b) on every grid point.

SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen only (see
data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first (44 of 483 -> SMALL439).  Small-panel numbers are upper bounds.

Outputs (all committed):
    .census.csv       every detected (file, dial, cell, statistic, rule) with its verdicts
    .breakage.csv     MATCHED confusion per (statistic, rule), archive and live
    .affinity.csv     Part B: per (panel, dial, value, statistic) endpoint-line residual
    .grid.csv         Part B: every (panel, dial, value, rung) point with 4a/4b bars
    .walkforward.csv  Part B rule 8: IS gate + IS pick per statistic, OOS read once
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

# ------------------------------------------------------------------ p1: the statistic families
# A column belongs to family F iff its (lowercased, stripped) name matches F's pattern.
STAT_PATTERNS = {
    "Sharpe":     re.compile(r"^sharpe$"),
    "CAGR":       re.compile(r"^cagr$"),
    "MaxDD":      re.compile(r"^maxdd$"),
    "OOS_Sharpe": re.compile(r"^(oos_sharpe|sharpe_oos|oos_sh)$"),
    "M4B":        re.compile(r"^(m4b_(h1|h2|dd|cagr|oos)(_\d+)?|m_(cagr|dd|h1|h2|oos)|"
                             r"(cagr|dd|h1|h2|oos)_margin|margin4b|dd_margin_pp|cagr_margin_pp)$"),
}
STATS = list(STAT_PATTERNS)

COST_NAMES = {"bps", "cost_bps", "cost", "rung", "cost_rung", "bps_rung", "c_bps"}
# a column is a METRIC (never a dial) if its lowercased name contains any of these
METRIC_SUBSTR = ("sharpe", "cagr", "maxdd", "dd", "vol", "turn", "gross", "pass", "fail",
                 "p4a", "p4b", "f4b", "m_", "oos", "_is", "is_", "h1", "h2", "ret", "equity",
                 "pval", "p_", "_p", "z", "ci", "sd", "std", "mean", "median", "hit", "win",
                 "margin", "regret", "room", "excess", "premium", "delta", "d_", "rho", "corr",
                 "n_", "count", "seed", "invested", "held", "episodes", "days", "bind", "y20",
                 "sortino", "calmar", "alpha", "beta", "te", "ir", "skew", "kurt", "auc")


def is_metric(col):
    c = str(col).lower()
    return any(s in c for s in METRIC_SUBSTR)


def cost_col(cols):
    for c in cols:
        if str(c).lower() in COST_NAMES:
            return c
    return None


def stat_cols(cols):
    """{family: [column, ...]} for every statistic column present in this file."""
    out = {}
    for c in cols:
        lc = str(c).strip().lower()
        for fam, pat in STAT_PATTERNS.items():
            if pat.match(lc):
                out.setdefault(fam, []).append(c)
    return out


# ------------------------------------------------------------------ the cell reading
def piv_stats(piv):
    """gap / tilt / MATCHED margin / actual re-rank for one (dial value) x (cost rung) frame.

    Identical arithmetic to idea 231's, statistic-agnostic and higher-is-better throughout.
    """
    rungs = sorted(piv.columns)
    c_lo, c_hi = rungs[0], rungs[-1]
    s_lo, s_hi = piv[c_lo], piv[c_hi]
    order = s_lo.sort_values(ascending=False)
    best = order.index[0]
    gap = float(order.iloc[0] - order.iloc[1])
    span = float(c_hi - c_lo)
    slope = (s_hi - s_lo) / span
    lift = (slope - slope.loc[best]) * span                 # endpoint-span tilt, per name
    tilt = float(lift.max())
    matched = float((lift - (s_lo.loc[best] - s_lo)).drop(index=best).max())
    argmaxes = {c: piv[c].idxmax() for c in rungs}
    ends = {argmaxes[c_lo], argmaxes[c_hi]}
    # ENDPOINT-visible re-rank vs the FULL-ladder re-rank: MATCHED can only ever see the former
    endpoint_rerank = bool(argmaxes[c_hi] != argmaxes[c_lo])
    actual = len(set(argmaxes.values())) > 1
    interior_only = int(sum(argmaxes[c] not in ends for c in rungs))
    # curvature: how far each name's interior rungs sit off its own endpoint line
    resid = 0.0
    if len(rungs) > 2:
        for c in rungs[1:-1]:
            lin = s_lo + (s_hi - s_lo) * ((c - c_lo) / span)
            resid = max(resid, float((piv[c] - lin).abs().max()))
    scale = float(np.abs(piv.values).max()) or 1.0
    return dict(n_values=len(piv), n_rungs=len(rungs), c_lo=c_lo, c_hi=c_hi,
                argmax_lo=str(best), gap=gap, tilt=tilt,
                ratio=(tilt / gap if gap > 0 else (np.inf if tilt > 0 else 0.0)),
                matched_margin=matched,
                pred_published=bool(tilt > gap), pred_matched=bool(matched > 0),
                actual_rerank=bool(actual), endpoint_rerank=endpoint_rerank,
                interior_only=interior_only, n_distinct_argmax=len(set(argmaxes.values())),
                degenerate_gap=bool(gap <= 0), max_interior_resid=resid,
                rel_interior_resid=resid / scale)


def scan_archive():
    """One pass over the archive; every (file, dial, cell) read under all five statistics
    and both detection rules.  p2: STRICT requires the rectangle to be single-valued (one row
    per (dial value, rung)); LOOSE median-collapses duplicate rows.  Columns bijective with the
    dial (label columns that merely re-encode it) are dropped from the grouping first."""
    rows, seen, t0 = [], 0, time.time()
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(SELF.replace(".py", "")):
            continue
        seen += 1
        if seen % 400 == 0:
            print(f"    ...{seen} files, {len(rows)} cell-readings, {time.time()-t0:.0f}s", flush=True)
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) < 6:
            continue
        ccol = cost_col(df.columns)
        scs = stat_cols(df.columns)
        if ccol is None or not scs:
            continue
        df = df[pd.to_numeric(df[ccol], errors="coerce").notna()].copy()
        df[ccol] = df[ccol].astype(float)
        if df[ccol].nunique() < 2:
            continue
        cols_flat = [(fam, c) for fam, cs in scs.items() for c in cs]
        for _, c in cols_flat:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        ids = [c for c in df.columns if c != ccol and not is_metric(c) and df[c].nunique() > 1]
        dials = [c for c in ids if pd.api.types.is_numeric_dtype(df[c]) and 3 <= df[c].nunique() <= 60]
        for d in dials:
            nd = df[d].nunique()
            grp = [g for g in ids if g != d]
            grp = [g for g in grp if not (df[g].nunique() == nd and df.groupby(d)[g].nunique().max() == 1
                                          and df.groupby(g)[d].nunique().max() == 1)]
            grp = [g for g in grp if df[g].nunique() <= 200]
            vals = [c for _, c in cols_flat]
            agg = df.groupby(grp + [d, ccol], dropna=False, sort=False)[vals].median().reset_index()
            cnt = df.groupby(grp + [d, ccol], dropna=False, sort=False).size().reset_index(name="cnt")
            agg["cnt"] = cnt["cnt"].values
            if grp:
                keys = agg[grp[0]].astype(str)
                for g in grp[1:]:
                    keys = keys + "|" + agg[g].astype(str)
            else:
                keys = pd.Series("_", index=agg.index)
            agg["_k"] = keys.values
            sz = agg.groupby("_k", sort=False).size()
            big = sz[sz >= 6].index                           # >= 3 dial values x 2 rungs
            if not len(big):
                continue
            for k, sub in agg[agg._k.isin(big)].groupby("_k", sort=False):
                nv, nc = sub[d].nunique(), sub[ccol].nunique()
                if nv < 3 or nc < 2 or len(sub) != nv * nc:   # incomplete rectangle
                    continue
                single = not bool((sub.cnt.values > 1).any())
                for fam, c in cols_flat:
                    s = sub[[d, ccol, c]].dropna()
                    if len(s) != nv * nc or s[c].nunique() < 2:
                        continue
                    st = piv_stats(s.pivot(index=d, columns=ccol, values=c))
                    base = dict(file=f.name, dial=d, cell=str(k)[:80], stat=fam, col=str(c), **st)
                    if single:
                        rows.append(dict(base, rule="STRICT"))
                    rows.append(dict(base, rule="LOOSE"))
    C = pd.DataFrame(rows)
    print(f"    scan done: {seen} files, {len(C)} cell-readings, {time.time()-t0:.0f}s", flush=True)
    return C


def confusion(sub, pred="pred_matched", truth="actual_rerank"):
    p, a = sub[pred].values.astype(bool), sub[truth].values.astype(bool)
    tp, fp = int((p & a).sum()), int((p & ~a).sum())
    fn, tn = int((~p & a).sum()), int((~p & ~a).sum())
    n = len(sub)
    return dict(n=n, TP=tp, FP=fp, FN=fn, TN=tn, errors=fp + fn,
                accuracy=(tp + tn) / n if n else np.nan,
                precision=tp / (tp + fp) if tp + fp else np.nan,
                recall=tp / (tp + fn) if tp + fn else np.nan,
                rerank_rate=a.mean() if n else np.nan)


# ------------------------------------------------------------------ Part B: live rule 8
RUNGS = [0, 5, 10, 15, 20, 25, 30]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1)
DIAL_VALUES = {"N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
               "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
               "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
               "K": [1, 2, 3, 4, 6, 8, 13]}


def load_small439():
    """The sub-$2B panel with the 44 max_1d_move >= 1.0 tickers removed (survivorship caveat
    in the docstring); SPY is kept as the benchmark column, never as a constituent."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {px.shape[1] - len(keep)} of {px.shape[1] - 1} names "
          f"(max_1d_move >= 1.0) -> {len(keep) - 1} constituents", flush=True)
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


def m4b(s, spy, oos_s, oos_spy):
    """The four 4b margins, signed as slack over the bar (positive = passes)."""
    return dict(m4b_H1=s["H1"] - spy["H1"], m4b_H2=s["H2"] - spy["H2"],
                m4b_OOS=oos_s - oos_spy,
                m4b_DD=s["MaxDD"] - 0.60 * spy["MaxDD"],
                m4b_CAGR=s["CAGR"] - 0.70 * spy["CAGR"])


def bars_4b(mm):
    return ",".join(k.replace("m4b_", "") for k, v in mm.items() if not v > 0)


def part_b():
    t0 = time.time()
    grid, aff, ident = [], [], []
    panels = (("U56", load_universe()), ("B136", load_universe(broad=True)),
              ("SMALL439", load_small439()))
    for pname, px in panels:
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
        eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        ident.append((pname, float(np.abs(eng - net(bg, bt, 10).loc[start:]).max())))

        cache = {}
        for dial, values in DIAL_VALUES.items():
            for v in values:
                kw = dict(DEFAULTS); kw[dial] = v
                if dial == "N" and v > px.shape[1] - 1:
                    continue
                W = book_weights(px, comp, ma, vol20, kw["N"], kw["G"], kw["V"])
                g_, t_ = simulate(px, W, week_mask(px.index, kw["K"]))
                g_, t_ = g_.loc[start:], t_.loc[start:]
                cache[(dial, v)] = (g_, t_)
                yrs = len(g_) / 252
                for c in RUNGS:
                    r = net(g_, t_, c); st = stats(r); o = metrics(r.loc[OOS_START:])
                    mm = m4b(st, spy_s, o["Sharpe"], spy_o["Sharpe"])
                    grid.append(dict(panel=pname, dial=dial, value=v, bps=c,
                                     turn_yr=t_.sum() / yrs, **st,
                                     OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                     IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                     IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                     **mm, fail4a=bars_4a(st, base[c]), fail4b=bars_4b(mm),
                                     spy_Sharpe=spy_s["Sharpe"], spy_CAGR=spy_s["CAGR"],
                                     spy_MaxDD=spy_s["MaxDD"],
                                     spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                                     spy_OOS_MaxDD=spy_o["MaxDD"],
                                     v1_Sharpe=base[c]["Sharpe"], v1_CAGR=base[c]["CAGR"],
                                     v1_MaxDD=base[c]["MaxDD"],
                                     v1_OOS_Sharpe=base_oos[c]["Sharpe"],
                                     v1_OOS_CAGR=base_oos[c]["CAGR"],
                                     v1_OOS_MaxDD=base_oos[c]["MaxDD"],
                                     v2_OOS_Sharpe=v2_oos[c]["Sharpe"],
                                     v2_OOS_CAGR=v2_oos[c]["CAGR"],
                                     v2_OOS_MaxDD=v2_oos[c]["MaxDD"]))
        print(f"  {pname}: {time.time()-t0:.0f}s", flush=True)
    G = pd.DataFrame(grid)

    # affinity residual: how far each interior rung sits off the name's own endpoint line,
    # in units of the statistic's own spread across the dial at the low rung
    for (p_, d_, v_), sub in G.groupby(["panel", "dial", "value"]):
        s = sub.sort_values("bps")
        c = s.bps.values.astype(float)
        for fam, col in (("Sharpe", "Sharpe"), ("CAGR", "CAGR"), ("MaxDD", "MaxDD"),
                         ("OOS_Sharpe", "OOS_Sharpe"), ("M4B", "m4b_CAGR")):
            y = s[col].values.astype(float)
            lin = y[0] + (y[-1] - y[0]) * (c - c[0]) / (c[-1] - c[0])
            aff.append(dict(panel=p_, dial=d_, value=v_, stat=fam,
                            max_abs_resid=float(np.abs(y - lin).max()),
                            span=float(abs(y[-1] - y[0])),
                            resid_over_span=float(np.abs(y - lin).max() / abs(y[-1] - y[0]))
                            if y[-1] != y[0] else np.nan))
    return G, pd.DataFrame(aff), ident


def live_cells(G):
    """Read every (panel, dial) live cell under all five statistics, full sample and IS-only."""
    rows = []
    fams = {"Sharpe": "Sharpe", "CAGR": "CAGR", "MaxDD": "MaxDD", "OOS_Sharpe": "OOS_Sharpe",
            "M4B": "m4b_CAGR"}
    is_fams = {"Sharpe": "IS_Sharpe", "CAGR": "IS_CAGR", "MaxDD": "IS_MaxDD"}
    for (p_, d_), sub in G.groupby(["panel", "dial"]):
        for fam, col in fams.items():
            st = piv_stats(sub.pivot_table(index="value", columns="bps", values=col))
            rows.append(dict(panel=p_, dial=d_, stat=fam, window="FULL", **st))
        for fam, col in is_fams.items():
            st = piv_stats(sub.pivot_table(index="value", columns="bps", values=col))
            rows.append(dict(panel=p_, dial=d_, stat=fam, window="IS", **st))
    return pd.DataFrame(rows)


def walk_forward(G):
    """PROTOCOL rule 8.  Everything on the left of the bar is computed on 2009-2016 only:
    the MATCHED gate, and the dial value the chooser picks at each rung.  2017-2026 is read
    once.  Three choosers per statistic: rung-aware (IS argmax at THIS rung), naive (IS argmax
    at 0 bps), do-nothing (the live default)."""
    wf = []
    is_cols = {"Sharpe": "IS_Sharpe", "CAGR": "IS_CAGR", "MaxDD": "IS_MaxDD"}
    for (p_, d_), sub in G.groupby(["panel", "dial"]):
        vals = sorted(sub.value.unique())
        dn = DEFAULTS[d_]
        for fam, icol in is_cols.items():
            piv = sub.pivot_table(index="value", columns="bps", values=icol)
            st = piv_stats(piv)
            is_arg = {c: piv[c].idxmax() for c in sorted(piv.columns)}
            pick0 = is_arg[min(is_arg)]
            for c in RUNGS:
                o = sub[sub.bps == c].set_index("value")
                pr = is_arg[c]
                wf.append(dict(panel=p_, dial=d_, stat=fam, bps=c,
                               IS_gap=st["gap"], IS_tilt=st["tilt"], IS_matched=st["matched_margin"],
                               gate_matched=st["pred_matched"], gate_published=st["pred_published"],
                               IS_argmax_moves=st["actual_rerank"],
                               IS_interior_only=st["interior_only"],
                               IS_resid=st["max_interior_resid"],
                               pick_rung=pr, pick_0bps=pick0, do_nothing=dn,
                               rung_OOS_Sharpe=o.OOS_Sharpe[pr], rung_OOS_CAGR=o.OOS_CAGR[pr],
                               rung_OOS_MaxDD=o.OOS_MaxDD[pr],
                               naive_OOS_Sharpe=o.OOS_Sharpe[pick0], naive_OOS_CAGR=o.OOS_CAGR[pick0],
                               naive_OOS_MaxDD=o.OOS_MaxDD[pick0],
                               dn_OOS_Sharpe=o.OOS_Sharpe[dn], dn_OOS_CAGR=o.OOS_CAGR[dn],
                               dn_OOS_MaxDD=o.OOS_MaxDD[dn],
                               rand_OOS_Sharpe=float(o.OOS_Sharpe.loc[vals].mean()),
                               rand_OOS_CAGR=float(o.OOS_CAGR.loc[vals].mean()),
                               oracle_OOS_Sharpe=float(o.OOS_Sharpe.max()),
                               v1_OOS_Sharpe=float(o.v1_OOS_Sharpe.iloc[0]),
                               v1_OOS_CAGR=float(o.v1_OOS_CAGR.iloc[0]),
                               v1_OOS_MaxDD=float(o.v1_OOS_MaxDD.iloc[0]),
                               v2_OOS_Sharpe=float(o.v2_OOS_Sharpe.iloc[0]),
                               spy_OOS_Sharpe=float(o.spy_OOS_Sharpe.iloc[0]),
                               spy_OOS_CAGR=float(o.spy_OOS_CAGR.iloc[0]),
                               spy_OOS_MaxDD=float(o.spy_OOS_MaxDD.iloc[0])))
    return pd.DataFrame(wf)


# ------------------------------------------------------------------ main
def main():
    print("=" * 90)
    print("PART A — back-fill the MATCHED margin over the archive under five statistics")
    print("=" * 90)
    C = scan_archive()
    C.to_csv(f"{OUT}.census.csv", index=False)

    brk = []
    for rule in ("STRICT", "LOOSE"):
        R = C[C.rule == rule]
        print(f"\n[p2={rule}] {len(R)} cell-readings, {R.file.nunique()} files, "
              f"{R.dial.nunique()} dial columns")
        print(f"  {'p1 statistic':12s} {'cells':>7s} {'files':>6s} {'rerank':>7s} "
              f"{'TP':>6s} {'FP':>5s} {'FN':>5s} {'TN':>6s} {'errors':>7s} {'acc':>7s} "
              f"{'endpt-blind':>12s}")
        for fam in STATS:
            S = R[R.stat == fam]
            if not len(S):
                print(f"  {fam:12s}       0 — no committed grid carries this column")
                continue
            cf = confusion(S)
            blind = int((S.actual_rerank & ~S.endpoint_rerank).sum())
            print(f"  {fam:12s} {cf['n']:7d} {S.file.nunique():6d} {cf['rerank_rate']:7.3f} "
                  f"{cf['TP']:6d} {cf['FP']:5d} {cf['FN']:5d} {cf['TN']:6d} {cf['errors']:7d} "
                  f"{cf['accuracy']:7.4f} {blind:12d}")
            brk.append(dict(source="ARCHIVE", rule=rule, stat=fam, files=int(S.file.nunique()),
                            endpoint_blind_reranks=blind,
                            mean_rel_resid=float(S.rel_interior_resid.mean()),
                            max_rel_resid=float(S.rel_interior_resid.max()), **cf))
            err = S[S.pred_matched != S.actual_rerank]
            if len(err):
                sole_int = int((err.actual_rerank & ~err.endpoint_rerank).sum())
                print(f"    -> {len(err)} MATCHED errors; {sole_int} are re-ranks INVISIBLE to the "
                      f"two endpoint rungs; top files: "
                      + ", ".join(f"{k}({v})" for k, v in err.file.value_counts().head(3).items()))
    B = pd.DataFrame(brk)

    print("\n=== reproduction gate: idea 231's Sharpe reading re-derived by this scanner ===")
    S = C[(C.rule == "STRICT") & (C.stat == "Sharpe")]
    cf = confusion(S)
    print(f"  Sharpe/STRICT cells {cf['n']} (idea 231 committed 8,529), MATCHED errors {cf['errors']} "
          f"(idea 231: 0), re-rank rate {cf['rerank_rate']:.4f} (idea 231: 0.194)")
    par = BT / "2026-09-08_the-gap-vs-tilt-rule-as-a-leaderboard-column_B.census.csv"
    if par.exists():
        P = pd.read_csv(par)
        P = P[P.rule == "STRICT"]
        j = S.merge(P, on=["file", "dial", "cell"], suffixes=("", "_231"))
        if len(j):
            print(f"  cell-for-cell join on idea 231's own census: {len(j)} matched cells, "
                  f"max |gap diff| {np.abs(j.gap - j.gap_231).max():.3e}, "
                  f"max |tilt diff| {np.abs(j.tilt - j.tilt_231).max():.3e}, "
                  f"max |matched diff| {np.abs(j.matched_margin - j.matched_margin_231).max():.3e}, "
                  f"actual agrees {int((j.actual_rerank == j.actual_rerank_231).sum())}/{len(j)}")
            key = set(zip(P.file, P.dial, P.cell))
            for _, e in S[S.pred_matched != S.actual_rerank].iterrows():
                inside = (e.file, e.dial, e.cell) in key
                print(f"    Sharpe MATCHED error: {e.file} dial={e.dial} cell={e.cell[:36]} "
                      f"gap {e.gap:.3e} tilt {e.tilt:.3e} matched {e.matched_margin:.3e} "
                      f"interior-resid {e.max_interior_resid:.3e} | "
                      f"{'INSIDE' if inside else 'OUTSIDE'} idea 231's committed corpus")

    print("\n" + "=" * 90)
    print("PART B — live: one book read by all five statistics; PROTOCOL rule 8")
    print("=" * 90)
    G, AFF, ident = part_b()
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    AFF.to_csv(f"{OUT}.affinity.csv", index=False)
    K = G.groupby(["panel", "dial", "bps"])[["pass4a", "pass4b"]].sum().reset_index()
    K.to_csv(f"{OUT}.keep.csv", index=False)
    print("\n cost identity |engine@10bps - (gross - turn*c/1e4)|:  "
          + "  ".join(f"{p}={d:.1e}" for p, d in ident))

    print("\n=== the mechanism: interior-rung deviation from the name's own endpoint line ===")
    print("   (max over interior rungs, mean/max over the 96 (panel,dial,value) books)")
    A = AFF.groupby("stat").agg(mean_abs=("max_abs_resid", "mean"), max_abs=("max_abs_resid", "max"),
                                mean_rel=("resid_over_span", "mean"),
                                max_rel=("resid_over_span", "max")).reindex(STATS)
    print(A.to_string(float_format=lambda x: f"{x:.3e}"))

    LC = live_cells(G)
    print("\n=== live cells (12 panel x dial, full sample): MATCHED as an argmax reader ===")
    print(f"  {'p1 statistic':12s} {'cells':>6s} {'rerank':>7s} {'TP':>4s} {'FP':>4s} {'FN':>4s} "
          f"{'TN':>4s} {'errors':>7s} {'endpt-blind':>12s}")
    for fam in STATS:
        S2 = LC[(LC.stat == fam) & (LC.window == "FULL")]
        cf = confusion(S2)
        blind = int((S2.actual_rerank & ~S2.endpoint_rerank).sum())
        print(f"  {fam:12s} {cf['n']:6d} {cf['rerank_rate']:7.3f} {cf['TP']:4d} {cf['FP']:4d} "
              f"{cf['FN']:4d} {cf['TN']:4d} {cf['errors']:7d} {blind:12d}")
        brk.append(dict(source="LIVE_FULL", rule="n/a", stat=fam, files=0,
                        endpoint_blind_reranks=blind,
                        mean_rel_resid=float(S2.rel_interior_resid.mean()),
                        max_rel_resid=float(S2.rel_interior_resid.max()), **cf))
    pd.DataFrame(brk).to_csv(f"{OUT}.breakage.csv", index=False)

    WF = walk_forward(G)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    print("\n=== rule 8: IS (2009-2016) gate per statistic, and the OOS (2017-2026) read ===")
    U = WF.drop_duplicates(["panel", "dial", "stat"])
    for fam in ("Sharpe", "CAGR", "MaxDD"):
        S3 = U[U.stat == fam]
        cf = confusion(S3, pred="gate_matched", truth="IS_argmax_moves")
        print(f"  {fam:7s} IS cells {cf['n']:2d}  MATCHED gate vs IS argmax move: "
              f"TP {cf['TP']} FP {cf['FP']} FN {cf['FN']} TN {cf['TN']}  errors {cf['errors']}  "
              f"mean IS interior resid {S3.IS_resid.mean():.3e}")
    print("\n  OOS Sharpe/CAGR/MaxDD by chooser, mean over 84 (panel x dial x rung) cells:")
    for fam in ("Sharpe", "CAGR", "MaxDD"):
        S3 = WF[WF.stat == fam]
        print(f"  IS selector = {fam:7s} rung-aware {S3.rung_OOS_Sharpe.mean():+.4f}/"
              f"{S3.rung_OOS_CAGR.mean():.2%}/{S3.rung_OOS_MaxDD.mean():.2%}   "
              f"naive-0bps {S3.naive_OOS_Sharpe.mean():+.4f}/{S3.naive_OOS_CAGR.mean():.2%}   "
              f"do-nothing {S3.dn_OOS_Sharpe.mean():+.4f}/{S3.dn_OOS_CAGR.mean():.2%}   "
              f"random {S3.rand_OOS_Sharpe.mean():+.4f}   oracle {S3.oracle_OOS_Sharpe.mean():+.4f}")
    t10 = WF[(WF.bps == 10) & (WF.stat == "Sharpe")]
    print("\n=== rule 8 headline at PROTOCOL's 10 bps (12 panel x dial cells, Sharpe selector) ===")
    for nm, a, b, c in (("rung-aware", "rung_OOS_Sharpe", "rung_OOS_CAGR", "rung_OOS_MaxDD"),
                        ("naive 0bps", "naive_OOS_Sharpe", "naive_OOS_CAGR", "naive_OOS_MaxDD"),
                        ("do-nothing", "dn_OOS_Sharpe", "dn_OOS_CAGR", "dn_OOS_MaxDD")):
        print(f"  {nm:11s} OOS Sharpe {t10[a].mean():.4f}  CAGR {t10[b].mean():.2%}  MaxDD {t10[c].mean():.2%}")
    for p_ in ("U56", "B136", "SMALL439"):
        s = t10[t10.panel == p_].iloc[0]
        print(f"  {p_:9s} RULES v1 OOS Sharpe {s.v1_OOS_Sharpe:.4f} (CAGR {s.v1_OOS_CAGR:.2%}, "
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
              f"CAGR {s.CAGR:.2%}  MaxDD {s.MaxDD:.2%}  OOS Sharpe {s.OOS_Sharpe:.3f}  "
              f"4a {'PASS' if s.pass4a else s.fail4a}  4b {'PASS' if s.pass4b else s.fail4b}")


if __name__ == "__main__":
    main()
