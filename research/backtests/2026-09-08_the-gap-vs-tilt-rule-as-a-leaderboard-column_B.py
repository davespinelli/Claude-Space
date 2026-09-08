#!/usr/bin/env python3
"""Idea 231 — the-gap-vs-tilt-rule-as-a-leaderboard-column (lane B, 2026-09-08).

Pre-registered question (QUEUE 231): idea 228's re-rank predictor — "a cost rung re-ranks a
dial iff the 0-bps top-2 Sharpe gap is smaller than the ladder's maximum 30-bp tilt" — caught
3/3 actual re-ranks and OVER-fired on 3 of 12 cells.  Back-fill gap and tilt over every swept
dial in the record whose parent committed a grid CSV, and report the tilt/gap RATIO at which
the prediction stops over-firing.  If it separates cleanly the pair belongs beside every
published argmax.

TWO TUNED PARAMETERS ONLY:
    p1 = DETECTION rule for "a swept dial inside a committed grid CSV"  {STRICT, LOOSE}
    p2 = RATIO THRESHOLD t: predict re-rank iff tilt/gap > t          (swept, all points reported)
Nothing else is tuned.  The MATCHED predictor below is parameter-free (no threshold, no
detection choice of its own) and is reported as a diagnostic, not as a third tuned dial.

DEFINITIONS (idea 228's, verbatim, generalised from 0/30 bps to the cell's own rung span):
    c_lo, c_hi   = lowest / highest cost rung present in the cell
    best         = argmax_d Sharpe(d, c_lo)
    gap          = Sharpe(best, c_lo) - second-best Sharpe(., c_lo)
    slope_d      = (Sharpe(d, c_hi) - Sharpe(d, c_lo)) / (c_hi - c_lo)          [Sharpe per bp]
    tilt         = max_d (slope_d - slope_best) * (c_hi - c_lo)
    PUBLISHED    : predict re-rank iff tilt > gap             (i.e. ratio = tilt/gap > 1)
    MATCHED      : predict re-rank iff max_d [ (slope_d - slope_best)*(c_hi-c_lo)
                                               - (Sharpe(best,c_lo) - Sharpe(d,c_lo)) ] > 0
    actual       = argmax_d Sharpe(d, c) differs from best at ANY rung c in the cell
PUBLISHED takes the max tilt and the min gap over POSSIBLY DIFFERENT names d; MATCHED pairs
them.  Under exact linearity of Sharpe in the rung MATCHED is an identity, so any MATCHED
error measures the curvature the identity net(c) = gross - turn*c/1e4 leaves in the
denominator (mean is linear in c, sd is not).

PART B (PROTOCOL rule 8, live data): re-run idea 228's four dials on three panels with gap,
tilt and ratio computed on 2009-2016 ONLY, then read 2017-2026 once.  Measures the thing a
leaderboard column would actually be used for: trusting "gate says safe -> the 0-bps argmax
is safe at your rung" and paying for it out of sample.  All KEEP paths (4a and 4b) reported
on every grid point, against RULES v1/v2 and SPY.

Outputs (all committed):
    .census.csv       every detected (file, dial, cell): gap, tilt, ratio, predictions, actual
    .threshold.csv    every point of the t sweep under both detection rules
    .grid.csv         Part B: every (panel, dial, value, rung) point, 4a/4b bars
    .walkforward.csv  Part B rule 8: IS-chosen dial per rung, OOS read once, gate verdicts
    .keep.csv         4a/4b pass counts per (panel, dial, rung)
"""
import sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, metrics                                            # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
SELF = Path(__file__).name

# ---------------------------------------------------------------- Part A: the archive scan
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


def sharpe_col(cols):
    for c in cols:
        if str(c).lower() == "sharpe":
            return c
    cand = [c for c in cols if "sharpe" in str(c).lower()
            and not any(p in str(c).lower() for p in ("oos", "is_", "h1", "h2", "_o", "d_", "spy", "base", "rand", "oracle", "dn_"))]
    return cand[0] if cand else None


def cost_col(cols):
    for c in cols:
        if str(c).lower() in COST_NAMES:
            return c
    return None


def cell_stats(sub, dcol, ccol, scol):
    """gap / tilt / ratio / predictions / actual for one complete (dial x rung) rectangle."""
    return piv_stats(sub.pivot_table(index=dcol, columns=ccol, values=scol, aggfunc="median"))


def piv_stats(piv):
    rungs = sorted(piv.columns)
    c_lo, c_hi = rungs[0], rungs[-1]
    s_lo, s_hi = piv[c_lo], piv[c_hi]
    order = s_lo.sort_values(ascending=False)
    best = order.index[0]
    gap = float(order.iloc[0] - order.iloc[1])
    span = float(c_hi - c_lo)
    slope = (s_hi - s_lo) / span
    lift = (slope - slope.loc[best]) * span                    # 30-bp-equivalent tilt, per name
    tilt = float(lift.max())
    matched = float((lift - (s_lo.loc[best] - s_lo)).drop(index=best).max())
    argmaxes = {c: piv[c].idxmax() for c in rungs}
    actual = len(set(argmaxes.values())) > 1
    ratio = tilt / gap if gap > 0 else (np.inf if tilt > 0 else 0.0)
    ends = {argmaxes[c_lo], argmaxes[c_hi]}
    return dict(n_values=len(piv), n_rungs=len(rungs), c_lo=c_lo, c_hi=c_hi,
                argmax_lo=best, gap=gap, tilt=tilt, ratio=ratio, matched_margin=matched,
                pred_published=bool(tilt > gap), pred_matched=bool(matched > 0),
                actual_rerank=bool(actual), degenerate_gap=bool(gap <= 0),
                # do the two ENDPOINT rungs alone see everything the whole ladder sees?
                endpoint_rerank=bool(argmaxes[c_hi] != argmaxes[c_lo]),
                interior_only=int(sum(argmaxes[c] not in ends for c in rungs)),
                n_distinct_argmax=len(set(argmaxes.values())),
                first_move=next((c for c in rungs if argmaxes[c] != best), np.nan))


def scan_archive(strict=True):
    """Detect every (committed grid CSV, dial, cell) sweep. p1 = STRICT vs LOOSE.

    STRICT: the (dial x rung) rectangle must be complete AND single-valued (one row per cell).
    LOOSE : the rectangle must be complete; duplicate rows inside a cell are median-collapsed.
    Both rules first drop group columns that are bijective with the dial (label columns such
    as arm='n=20' that merely re-encode it), otherwise every sweep shatters into singletons.
    """
    rows = []
    seen = 0
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(SELF.replace(".py", "")):
            continue
        seen += 1
        if seen % 300 == 0:
            print(f"    ...{seen} files, {len(rows)} cells", flush=True)
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) < 6:
            continue
        ccol, scol = cost_col(df.columns), sharpe_col(df.columns)
        if ccol is None or scol is None:
            continue
        df = df[pd.to_numeric(df[ccol], errors="coerce").notna() & pd.to_numeric(df[scol], errors="coerce").notna()].copy()
        df[ccol] = df[ccol].astype(float); df[scol] = df[scol].astype(float)
        if df[ccol].nunique() < 2:
            continue
        ids = [c for c in df.columns if c not in (ccol, scol) and not is_metric(c) and df[c].nunique() > 1]
        dials = [c for c in ids if pd.api.types.is_numeric_dtype(df[c]) and 3 <= df[c].nunique() <= 60]
        for d in dials:
            nd = df[d].nunique()
            grp = [g for g in ids if g != d]
            grp = [g for g in grp if not (df[g].nunique() == nd and df.groupby(d)[g].nunique().max() == 1
                                          and df.groupby(g)[d].nunique().max() == 1)]
            grp = [g for g in grp if df[g].nunique() <= 200]
            # one aggregation pass: (group, dial, rung) -> median Sharpe + row count
            agg = (df.groupby(grp + [d, ccol], dropna=False, sort=False)[scol]
                     .agg(med="median", cnt="size").reset_index())
            if grp:
                keys = agg[grp[0]].astype(str)
                for g in grp[1:]:
                    keys = keys + "|" + agg[g].astype(str)
            else:
                keys = pd.Series("_", index=agg.index)
            agg["_k"] = keys.values
            sz = agg.groupby("_k", sort=False).size()
            big = sz[sz >= 6].index                               # >= 3 dial values x 2 rungs
            if not len(big):
                continue
            for k, sub in agg[agg._k.isin(big)].groupby("_k", sort=False):
                nv, nc = sub[d].nunique(), sub[ccol].nunique()
                if nv < 3:
                    continue
                if nc < 2 or len(sub) != nv * nc:                 # incomplete rectangle
                    continue
                if strict and (sub.cnt.values > 1).any():         # not single-valued
                    continue
                st = piv_stats(sub.pivot(index=d, columns=ccol, values="med"))
                rows.append(dict(file=f.name, dial=d, cell=str(k)[:80], **st))
    C = pd.DataFrame(rows)
    if len(C):
        C["rule"] = "STRICT" if strict else "LOOSE"
    return C


def sweep_thresholds(C, ts):
    """p2: predict re-rank iff ratio > t. Every grid point reported."""
    out = []
    a = C["actual_rerank"].values
    r = C["ratio"].values
    for t in ts:
        p = r > t
        tp = int((p & a).sum()); fp = int((p & ~a).sum())
        fn = int((~p & a).sum()); tn = int((~p & ~a).sum())
        out.append(dict(t=t, TP=tp, FP=fp, FN=fn, TN=tn, n=len(C),
                        precision=tp / (tp + fp) if tp + fp else np.nan,
                        recall=tp / (tp + fn) if tp + fn else np.nan,
                        accuracy=(tp + tn) / len(C) if len(C) else np.nan,
                        overfires=fp, misses=fn))
    return pd.DataFrame(out)


def auc(C):
    """Mann-Whitney AUC of ratio as a re-rank score. Parameter-free separation statistic."""
    pos = C.loc[C.actual_rerank, "ratio"].values
    neg = C.loc[~C.actual_rerank, "ratio"].values
    if not len(pos) or not len(neg):
        return np.nan
    r = pd.Series(np.concatenate([pos, neg])).rank().values
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


# ---------------------------------------------------------------- Part B: live rule-8
RUNGS = [0, 5, 10, 15, 20, 25, 30]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1)
DIAL_VALUES = {"N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
               "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
               "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
               "K": [1, 2, 3, 4, 6, 8, 13]}


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


def is_cell_stats(sh):
    """gap/tilt/ratio/matched from an IS Sharpe frame indexed [value] x [rung]."""
    rungs = sorted(sh.columns); c_lo, c_hi = rungs[0], rungs[-1]
    s_lo, s_hi = sh[c_lo], sh[c_hi]
    order = s_lo.sort_values(ascending=False); best = order.index[0]
    gap = float(order.iloc[0] - order.iloc[1]); span = float(c_hi - c_lo)
    lift = ((s_hi - s_lo) / span - (s_hi.loc[best] - s_lo.loc[best]) / span) * span
    tilt = float(lift.max())
    matched = float((lift - (s_lo.loc[best] - s_lo)).drop(index=best).max())
    return best, gap, tilt, (tilt / gap if gap > 0 else np.inf), matched


def part_b():
    t0 = time.time()
    grid, wf, ident = [], [], []
    for pname, px in (("U56", load_universe()), ("B136", load_universe(broad=True)),
                      ("SMALL484", load_universe(small=True))):
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r); spy_o = metrics(spy_r.loc[OOS_START:])

        bg, bt = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base = {c: stats(net(bg, bt, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(bg, bt, c).loc[OOS_START:])["Sharpe"] for c in RUNGS}
        vg, vt = simulate(px, rules_v2_weights(px), week_mask(px.index, 1))
        v2_oos = {c: metrics(net(vg, vt, c).loc[OOS_START:])["Sharpe"] for c in RUNGS}
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
                    grid.append(dict(panel=pname, dial=dial, value=v, bps=c, turn_yr=t_.sum() / yrs,
                                     **st, OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                     fail4a=bars_4a(st, base[c]),
                                     fail4b=bars_4b(st, spy_s, o["Sharpe"], spy_o["Sharpe"])))

            vals = [v for (d, v) in cache if d == dial]
            IS = pd.DataFrame({c: {v: metrics(net(*cache[(dial, v)], c).loc[:IS_END])["Sharpe"] for v in vals}
                               for c in RUNGS})
            best0, gap, tilt, ratio, matched = is_cell_stats(IS)
            is_arg = {c: IS[c].idxmax() for c in RUNGS}
            is_moves = len(set(is_arg.values())) > 1
            for c in RUNGS:
                oo = {v: metrics(net(*cache[(dial, v)], c).loc[OOS_START:]) for v in vals}
                pick_r, pick_0, dn = is_arg[c], best0, DEFAULTS[dial]
                full_arg = max(vals, key=lambda v: metrics(net(*cache[(dial, v)], c))["Sharpe"])
                wf.append(dict(panel=pname, dial=dial, bps=c,
                               IS_gap=gap, IS_tilt=tilt, IS_ratio=ratio, IS_matched=matched,
                               gate_published=bool(tilt > gap), gate_matched=bool(matched > 0),
                               IS_argmax_moves=bool(is_moves), pick_rung=pick_r, pick_0bps=pick_0,
                               do_nothing=dn, full_argmax=full_arg,
                               rung_OOS_Sharpe=oo[pick_r]["Sharpe"], naive_OOS_Sharpe=oo[pick_0]["Sharpe"],
                               rung_OOS_CAGR=oo[pick_r]["CAGR"], rung_OOS_MaxDD=oo[pick_r]["MaxDD"],
                               naive_OOS_CAGR=oo[pick_0]["CAGR"], naive_OOS_MaxDD=oo[pick_0]["MaxDD"],
                               dn_OOS_Sharpe=oo[dn]["Sharpe"], dn_OOS_CAGR=oo[dn]["CAGR"],
                               dn_OOS_MaxDD=oo[dn]["MaxDD"],
                               rand_OOS_Sharpe=float(np.mean([oo[v]["Sharpe"] for v in vals])),
                               oracle_OOS_Sharpe=oo[full_arg]["Sharpe"],
                               v1_OOS_Sharpe=base_oos[c], v2_OOS_Sharpe=v2_oos[c],
                               spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                               spy_OOS_MaxDD=spy_o["MaxDD"]))
        print(f"  {pname}: {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame(grid), pd.DataFrame(wf), ident


# ---------------------------------------------------------------- main
def main():
    print("=" * 78)
    print("PART A — back-fill gap and tilt over every swept dial with a committed grid CSV")
    print("=" * 78)
    frames = {}
    for strict in (True, False):
        C = scan_archive(strict=strict)
        frames["STRICT" if strict else "LOOSE"] = C
        tag = "STRICT" if strict else "LOOSE"
        print(f"\n[p1={tag}] {len(C)} cells from {C.file.nunique() if len(C) else 0} files, "
              f"{C.dial.nunique() if len(C) else 0} distinct dial columns")
        if not len(C):
            continue
        print(f"  actual re-ranks: {int(C.actual_rerank.sum())} / {len(C)} "
              f"({C.actual_rerank.mean():.1%});  degenerate gap (<=0): {int(C.degenerate_gap.sum())}")
        for nm, col in (("PUBLISHED (tilt > gap)", "pred_published"), ("MATCHED (parameter-free)", "pred_matched")):
            p, a = C[col].values, C.actual_rerank.values
            tp, fp = int((p & a).sum()), int((p & ~a).sum())
            fn, tn = int((~p & a).sum()), int((~p & ~a).sum())
            print(f"  {nm:26s} TP {tp:5d}  FP(over-fire) {fp:5d}  FN(miss) {fn:5d}  TN {tn:5d}"
                  f"   acc {(tp+tn)/len(C):.3f}")
        print(f"  AUC(ratio as re-rank score) = {auc(C):.4f}")
        # is the over-firing a MAGNITUDE problem or a PAIRING problem?
        fp = C[C.pred_published & ~C.actual_rerank]
        print(f"  of the {len(fp)} PUBLISHED over-fires, {int((~fp.pred_matched).sum())} "
              f"({(~fp.pred_matched).mean() if len(fp) else 0:.1%}) are cells where the max-tilt name and the "
              f"min-gap name are DIFFERENT names (pairing, not magnitude)")
        tie = C[(C.gap.abs() < 1e-9) & (C.tilt.abs() < 1e-9)]
        err = C[C.pred_matched != C.actual_rerank]
        print(f"  MATCHED errors: {len(err)} total, {int((err.gap.abs() >= 1e-9).sum())} outside "
              f"machine-epsilon ties (|gap| and |tilt| < 1e-9 in {len(tie)} cells overall)")
        # does the whole ladder ever say something its two endpoint rungs do not?
        print(f"  endpoint-only reading (c_lo and c_hi alone) agrees with the full ladder in "
              f"{int((C.endpoint_rerank == C.actual_rerank).sum())} / {len(C)} cells; "
              f"cells with an INTERIOR-only argmax: {int((C.interior_only > 0).sum())}")
        fin = C[np.isfinite(C.ratio)]
        pos, neg = fin.loc[fin.actual_rerank, "ratio"], fin.loc[~fin.actual_rerank, "ratio"]
        if len(pos) and len(neg):
            print(f"  finite-ratio separation: min(ratio | re-rank) = {pos.min():.4f}, "
                  f"max(ratio | no re-rank) = {neg.max():.4f} -> "
                  f"{'CLEAN' if pos.min() > neg.max() else 'OVERLAP'}")
            print(f"    ratio quantiles | re-rank    : "
                  f"{', '.join(f'{q:.0%}={pos.quantile(q):.3f}' for q in (0.05,0.25,0.5,0.75,0.95))}")
            print(f"    ratio quantiles | no re-rank : "
                  f"{', '.join(f'{q:.0%}={neg.quantile(q):.3f}' for q in (0.05,0.25,0.5,0.75,0.95))}")

    TS = [0.0, 0.10, 0.25, 0.50, 0.75, 0.90, 1.00, 1.10, 1.25, 1.50, 2.0, 3.0, 4.0, 5.0,
          7.5, 10.0, 20.0, 50.0, 100.0, 1e9]
    sweeps = []
    for tag, C in frames.items():
        if not len(C):
            continue
        S = sweep_thresholds(C, TS); S["rule"] = tag
        sweeps.append(S)
        print(f"\n=== p2 threshold sweep, all grid points [p1={tag}] "
              f"(predict re-rank iff ratio > t) ===")
        print(S[["t", "TP", "FP", "FN", "TN", "precision", "recall", "accuracy"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        zero_fp = S[(S.FP == 0) & (S.TP > 0)]
        print("  ANSWER to the queue's question — first t with ZERO over-fires and TP>0: "
              + (f"t={zero_fp.t.iloc[0]:g} (recall {zero_fp.recall.iloc[0]:.3f}, "
                 f"misses {int(zero_fp.FN.iloc[0])})" if len(zero_fp)
                 else "NONE EXISTS — the prediction never stops over-firing; "
                      f"best precision on the whole sweep is {S.precision.max():.4f}"))
    SW = pd.concat(sweeps, ignore_index=True) if sweeps else pd.DataFrame()
    CA = pd.concat([f for f in frames.values() if len(f)], ignore_index=True)
    CA.to_csv(f"{OUT}.census.csv", index=False)
    SW.to_csv(f"{OUT}.threshold.csv", index=False)

    # --- reproduction check against idea 228's own committed mechanism table
    par = BT / "2026-09-06_does-any-dial-argmax-move-with-cost_C.mechanism.csv"
    if par.exists():
        M = pd.read_csv(par)
        G = pd.read_csv(BT / "2026-09-06_does-any-dial-argmax-move-with-cost_C.grid.csv")
        rep = []
        for (p_, d_), sub in G.groupby(["panel", "dial"]):
            st = cell_stats(sub, "value", "bps", "Sharpe")
            m = M[(M.panel == p_) & (M.dial == d_)].iloc[0]
            rep.append(dict(panel=p_, dial=d_, d_gap=abs(st["gap"] - m.top2_gap_0bps),
                            d_tilt=abs(st["tilt"] - m.max_tilt_30bps),
                            pred_ok=bool(st["pred_published"] == bool(m.predicted_rerank)),
                            act_ok=bool(st["actual_rerank"] == bool(m.actual_rerank))))
        R = pd.DataFrame(rep)
        print("\n=== reproduction: idea 228's 12 cells re-read by this scanner ===")
        print(f"  max |gap diff| {R.d_gap.max():.3e}   max |tilt diff| {R.d_tilt.max():.3e}   "
              f"prediction agrees {int(R.pred_ok.sum())}/{len(R)}   actual agrees {int(R.act_ok.sum())}/{len(R)}")

    print("\n" + "=" * 78)
    print("PART B — PROTOCOL rule 8: gate computed on 2009-2016, 2017-2026 read once")
    print("=" * 78)
    G, WF, ident = part_b()
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    K = G.groupby(["panel", "dial", "bps"])[["pass4a", "pass4b"]].sum().reset_index()
    K.to_csv(f"{OUT}.keep.csv", index=False)

    print("\n cost identity |engine@10bps - (gross - turn*c/1e4)|:  "
          + "  ".join(f"{p}={d:.1e}" for p, d in ident))

    print("\n=== IS (2009-2016) gate per (panel, dial), and what trusting it costs OOS ===")
    U = WF.drop_duplicates(["panel", "dial"])[["panel", "dial", "IS_gap", "IS_tilt", "IS_ratio",
                                               "IS_matched", "gate_published", "gate_matched",
                                               "IS_argmax_moves"]]
    print(U.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    p, a = U.gate_published.values, U.IS_argmax_moves.values
    print(f"  PUBLISHED gate vs IS re-rank: TP {int((p&a).sum())} FP {int((p&~a).sum())} "
          f"FN {int((~p&a).sum())} TN {int((~p&~a).sum())}")
    m = U.gate_matched.values
    print(f"  MATCHED   gate vs IS re-rank: TP {int((m&a).sum())} FP {int((m&~a).sum())} "
          f"FN {int((~m&a).sum())} TN {int((~m&~a).sum())}")

    WF["d_rung_minus_naive"] = WF.rung_OOS_Sharpe - WF.naive_OOS_Sharpe
    WF["d_rung_minus_dn"] = WF.rung_OOS_Sharpe - WF.dn_OOS_Sharpe
    WF["d_naive_minus_dn"] = WF.naive_OOS_Sharpe - WF.dn_OOS_Sharpe
    WF["d_rand_minus_dn"] = WF.rand_OOS_Sharpe - WF.dn_OOS_Sharpe
    safe = WF[~WF.gate_published]
    fired = WF[WF.gate_published]
    print("\n=== rule 8: OOS Sharpe, mean over cells (84 = 3 panels x 4 dials x 7 rungs) ===")
    for nm, sub in (("ALL", WF), ("gate says SAFE", safe), ("gate FIRED", fired)):
        if not len(sub):
            continue
        print(f"  {nm:16s} n={len(sub):3d}  rung-aware {sub.rung_OOS_Sharpe.mean():+.4f}  "
              f"naive-0bps {sub.naive_OOS_Sharpe.mean():+.4f}  do-nothing {sub.dn_OOS_Sharpe.mean():+.4f}  "
              f"random {sub.rand_OOS_Sharpe.mean():+.4f}  oracle {sub.oracle_OOS_Sharpe.mean():+.4f}")
        print(f"  {'':16s}        rung-naive {sub.d_rung_minus_naive.mean():+.4f}  "
              f"rung-dn {sub.d_rung_minus_dn.mean():+.4f}  naive-dn {sub.d_naive_minus_dn.mean():+.4f}  "
              f"rand-dn {sub.d_rand_minus_dn.mean():+.4f}")
    miss = WF[(~WF.gate_published) & (WF.pick_rung != WF.pick_0bps)]
    print(f"\n  gate says SAFE but the IS argmax DID move: {len(miss)} of {len(safe)} safe cells; "
          f"OOS Sharpe left on the table = {miss.d_rung_minus_naive.mean() if len(miss) else 0.0:+.4f}")
    fire_no = WF[(WF.gate_published) & (WF.pick_rung == WF.pick_0bps)]
    print(f"  gate FIRED but the IS argmax did NOT move (wasted ladder): {len(fire_no)} of {len(fired)}")

    print("\n=== rule 8 headline at 10 bps (mean over 12 panel x dial cells) ===")
    t10 = WF[WF.bps == 10]
    print(f"  rung-aware  OOS Sharpe {t10.rung_OOS_Sharpe.mean():.4f}  CAGR {t10.rung_OOS_CAGR.mean():.2%}  "
          f"MaxDD {t10.rung_OOS_MaxDD.mean():.2%}")
    print(f"  naive 0-bps OOS Sharpe {t10.naive_OOS_Sharpe.mean():.4f}  CAGR {t10.naive_OOS_CAGR.mean():.2%}  "
          f"MaxDD {t10.naive_OOS_MaxDD.mean():.2%}")
    print(f"  do-nothing  OOS Sharpe {t10.dn_OOS_Sharpe.mean():.4f}  CAGR {t10.dn_OOS_CAGR.mean():.2%}  "
          f"MaxDD {t10.dn_OOS_MaxDD.mean():.2%}")
    for p_ in ("U56", "B136", "SMALL484"):
        s = t10[t10.panel == p_]
        print(f"  {p_:9s} RULES v1 {s.v1_OOS_Sharpe.iloc[0]:.4f}  RULES v2 {s.v2_OOS_Sharpe.iloc[0]:.4f}  "
              f"SPY {s.spy_OOS_Sharpe.iloc[0]:.4f} (CAGR {s.spy_OOS_CAGR.iloc[0]:.2%}, "
              f"MaxDD {s.spy_OOS_MaxDD.iloc[0]:.2%})")

    print("\n=== KEEP paths over all Part B grid points ===")
    print(f"  4a {int(G.pass4a.sum())} / {len(G)}    4b {int(G.pass4b.sum())} / {len(G)}")
    for p_ in ("U56", "B136", "SMALL484"):
        s = G[G.panel == p_]
        print(f"    {p_:9s} 4a {int(s.pass4a.sum()):3d}/{len(s)}   4b {int(s.pass4b.sum()):3d}/{len(s)}")
    fb = G[~G.pass4b].fail4b.str.split(",").explode().value_counts()
    print("  4b failing bars (sole + joint):", ", ".join(f"{k} {v}" for k, v in fb.items()))
    print("\nfull sample (10 bps) top of each panel:")
    for p_ in ("U56", "B136", "SMALL484"):
        s = G[(G.panel == p_) & (G.bps == 10)].nlargest(1, "Sharpe").iloc[0]
        print(f"  {p_:9s} best {s.dial}={s.value}  Sharpe {s.Sharpe:.3f} (H1 {s.H1:.3f}/H2 {s.H2:.3f})  "
              f"CAGR {s.CAGR:.2%}  MaxDD {s.MaxDD:.2%}  OOS {s.OOS_Sharpe:.3f}")


if __name__ == "__main__":
    main()
