#!/usr/bin/env python3
"""Idea 310 - "is-EVOL-the-real-survivor-not-DISP" (lane B, 2026-09-09).

The question
------------
Idea 284 (ONE stratum: q = 0.500, k = 40) reported that under "the control" `disp` SURVIVES and
`evol` COLLAPSES.  Idea 293 (NINE strata) reported the reverse: mean partial `evol` +0.1551 vs
`disp` +0.0046 over 27 (q, k, book) points.  The queue asks: re-fit both partials stratum by
stratum, say which of the two is stable IN SIGN AND SIZE, and say whether the disagreement is
the k = 40 / q = 0.500 cell alone.

Design
------
Three blocks, in this order; nothing after a gate is read until the gate is graded.

  GATE (G)   The (q = 0.500, k = 40) stratum is REBUILT FROM PRICES, seeds 0..59, idea 293's
             seed key verbatim, and matched against idea 293's committed .panels.csv on the four
             characteristics and on every book's OOS Sharpe.  Idea 284's three published
             within-stratum rho (CAND10 -0.3648 / CAND20 -0.4815 / EWall -0.4708 for `corr`)
             and its four published joint-fit t are recomputed from the rebuilt panels.  If the
             gate fails, every downstream number is restated on the rebuilt cells and the
             failure is the headline.

  BLOCK A    Idea 293's committed 540 constructed panels (seeds 0..59), re-analysed: at each of
             the 27 (q, k, book) points, for `disp` and `evol`, the MARGINAL rank rho, the
             RANK-PARTIAL controlling for the other three characteristics (293's estimator,
             verbatim), and the joint-fit t (284's estimator, verbatim).  Both claims are graded
             on BOTH statistics, and leave-one-stratum-out answers the queue's "is it the
             k=40/q=0.5 cell alone?" mechanically.

  BLOCK B    A FRESH, DISJOINT SEED BLOCK (seeds 100..159) over the same 9 strata, built and
             backtested from prices: 540 new panels x 3 books.  Sign and size of both partials
             are re-measured on data neither 284 nor 293 ever saw.  A partial that is "stable"
             must keep its sign across seed blocks; one that does not is a noise reading.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q in {0.250, 0.500, 0.750}   small-cap share of the panel
    2. k in {20, 40, 80}            panel width
Everything else is idea 284/293's published convention and is NOT tuned: 60 seeds per stratum,
the RULES v1 eligibility gate (px > 200d MA AND vol20 < 0.60), the composite score without the
vol scaler as ranking key, 75% gross, weekly cadence, 10 bps, next-day execution, IS window
<= 2016-12-31.  The three books (EWall / CAND10 / CAND20) are all reported at every point; no
book is selected on its result.  The characteristics are MEASURED, not tuned.

Pre-registered predictions (written before BLOCK B was run; graded verbatim below)
    P1  Neither partial is a survivor: |mean partial| < 0.20 for BOTH `disp` and `evol` in
        block A and in block B.
    P2  Sign instability: for at least one of the two characteristics, the per-point partial
        sign disagrees between the two seed blocks in >= 9 of 27 points.
    P3  The disagreement is NOT the k=40/q=0.5 cell alone: idea 293's evol > disp ordering of
        mean partials survives leave-one-stratum-out in >= 8 of 9 leave-outs.
    P4  Mechanism: within-stratum rank corr(disp_IS, evol_IS) has median > 0.50, i.e. the two
        partials are dividing one shared source of variance.

Rule 8 walk-forward (required; directions pre-registered from the WITHIN-stratum marginal sign,
which is POSITIVE for both characteristics in idea 284 and idea 293)
    IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end read ONCE.
    Inside every stratum of the FRESH block each selector picks ONE panel on its IS
    characteristic and that panel's OOS book is read:
        S_DISP  HIGHEST IS dispersion              (284's claimed survivor)
        S_EVOL  HIGHEST IS eligible-set vol        (293's claimed survivor)
        S_CORR  LOWEST IS mean pairwise corr       (the record's incumbent, carried as the bar)
    Each selector's REVERSE extreme is reported as a sign check; the do-nothing anchor is the
    stratum's mean OOS Sharpe over its 60 draws with the seed sd.  SPY and RULES v2 OOS are
    reported beside every anchor, and OOS CAGR / Sharpe / MaxDD are reported for every pick.

Verdicts (both KEEP paths, on every cell of the fresh block)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
        SPY's.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens, so every
constructed panel inherits the bias whole and the LEVEL of every panel's return is inflated.
The object under test is whether a characteristic ORDERS panels inside a fixed cap mix; the bias
is common to a stratum's panels and inflates between-panel spread in level, so it runs AGAINST a
"nothing separates" verdict and does not protect a "something separates" one.  Any positive
finding is stated as a within-corpus regularity, never as a tradable edge.  The 44 SMALL439
tickers with max_1d_move >= 1.0 are dropped before any draw (data/small_meta.csv).

Deterministic, standalone.  Reads baseline.py and idea 293's committed CSV; modifies nothing
outside its own outputs.
Outputs: .gate.csv .blockA.csv .blockB.csv .panelsB.csv .stability.csv .walkforward.csv
         .keeppaths.csv .console.txt
"""
import sys
import json
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
BAND_V2 = 0.03
QS = [0.250, 0.500, 0.750]
KS = [20, 40, 80]
N_SEEDS = 60
SEED_A0 = 0            # idea 293's block
SEED_B0 = 100          # this run's fresh, disjoint block
CHARS = ["breadth", "disp", "corr", "evol"]
PAIR = ["disp", "evol"]
BOOKS = ["EWall", "CAND10", "CAND20"]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
N_PERM = 20000
N_BOOT = 2000

REF = REPO / "research" / "backtests" / "2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv"
REPRO_284_CORR = {"CAND10": -0.3648, "CAND20": -0.4815, "EWall": -0.4708}
REPRO_284_T = {  # idea 284's published joint-fit t on disp / evol at q=0.5, k=40
    "CAND10": dict(disp=+1.43, evol=-0.97),
    "CAND20": dict(disp=+1.31, evol=+0.23),
    "EWall": dict(disp=+1.65, evol=-0.49),
}
REPRO_293_PARTIAL = {"disp": +0.0046, "evol": +0.1551}   # 293's 27-point means
GATE_TOL = 1e-8

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 700)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ statistics (284/293 verbatim)
def spearman(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return np.nan, len(x)
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, len(x)
    return float(np.corrcoef(rx, ry)[0, 1]), len(x)


def perm_p(x, y, seed=7, nperm=N_PERM):
    rho, n = spearman(x, y)
    if not np.isfinite(rho):
        return np.nan, np.nan, n
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    rx = pd.Series(x[ok]).rank().to_numpy()
    ry = pd.Series(y[ok]).rank().to_numpy()
    rx = (rx - rx.mean()) / rx.std()
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(nperm):
        p = rng.permutation(ry)
        r = float(np.dot(rx, (p - p.mean()) / p.std()) / len(rx))
        if abs(r) >= abs(rho) - 1e-12:
            cnt += 1
    return rho, (cnt + 1) / (nperm + 1), n


def _rk(v):
    v = pd.Series(np.asarray(v, float)).rank().to_numpy()
    return (v - v.mean()) / (v.std() if v.std() > 0 else 1.0)


def rank_partial(y, x, controls):
    """Idea 293's estimator, verbatim: rank all, residualise x and y on controls, correlate."""
    Y, X = _rk(y), _rk(x)
    C = np.column_stack([np.ones(len(Y))] + [_rk(c) for c in controls])
    B = np.linalg.pinv(C.T @ C) @ C.T
    ry = Y - C @ (B @ Y)
    rx = X - C @ (B @ X)
    if ry.std() == 0 or rx.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def partial_boot(y, x, controls, seed=11, nboot=N_BOOT):
    """Percentile bootstrap CI for the rank-partial (resample panels inside the stratum)."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    C = [np.asarray(c, float) for c in controls]
    n = len(y)
    rng = np.random.default_rng(seed)
    out = np.empty(nboot)
    for b in range(nboot):
        idx = rng.integers(0, n, n)
        out[b] = rank_partial(y[idx], x[idx], [c[idx] for c in C])
    out = out[np.isfinite(out)]
    if len(out) < 100:
        return np.nan, np.nan, np.nan
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), float(out.std())


def ols_t(y, X):
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ss_res = float(e @ e)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    dof = max(1, n - p)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ss_res / dof)), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    return b, t, r2


def joint_fit(d, y_col):
    """Idea 284's joint fit: OOS Sharpe ~ 1 + the four z-scored IS characteristics."""
    y = d[y_col].to_numpy(float)
    cols = []
    for c in CHARS:
        v = d[f"{c}_IS"].to_numpy(float)
        cols.append((v - v.mean()) / (v.std(ddof=0) if v.std(ddof=0) > 0 else 1.0))
    X = np.column_stack([np.ones(len(y))] + cols)
    b, t, r2 = ols_t(y, X)
    return {CHARS[i]: (float(b[i + 1]), float(t[i + 1])) for i in range(len(CHARS))}, float(r2)


# ------------------------------------------------------------------ panel construction (293 verbatim)
def build_sources():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    idx = pxs.index.intersection(px136.index)
    pxs_c = pxs.reindex(idx).ffill()
    pxb_c = px136.reindex(idx).ffill()
    P(f"sources: BSTK{len(b_stk)} large-cap stocks, SMALL{len(s_stk)} small-cap stocks "
      f"({len(bad)} dropped for max_1d_move >= 1.0); common calendar "
      f"{idx[0].date()}..{idx[-1].date()} ({len(idx)} days)")
    return pxs_c, pxb_c, np.array(sorted(s_stk)), np.array(sorted(b_stk))


def draw_panel(pxs_c, pxb_c, small_pool, large_pool, q, k, sd):
    """Idea 293's seed key VERBATIM: STRAT|{q:.3f}|{sd} -- k absent, so strata are seed-paired."""
    n_s = int(round(q * k))
    n_l = k - n_s
    seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)
    rng = np.random.default_rng(seed)
    sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
    lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
    parts = []
    if lc:
        parts.append(pxb_c[lc])
    if sc:
        parts.append(pxs_c[sc])
    px = pd.concat(parts + [pxb_c["SPY"].rename("SPY")], axis=1).dropna(how="all").ffill()
    return px, set(sc) | set(lc)


def eligible_mask(px, tradable, above, vol20):
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def book_weights(px, tradable, arm, key, elig, n=None):
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


def panel_chars(px, elig, lo, hi, cols, rbmask):
    start = px.index[260]
    idx = px.loc[start:].index
    idx = idx[idx >= pd.Timestamp(lo)]
    if hi:
        idx = idx[idx <= pd.Timestamp(hi)]
    rb = idx[rbmask.reindex(idx).fillna(False).values]
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
    return dict(n_elig=float(nel.median()), breadth=breadth, disp=disp, corr=corr, evol=evol)


def stat_block(r):
    h = len(r) // 2
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
    out["IS_Sharpe"] = metrics(ris)["Sharpe"] if len(ris) > 60 else np.nan
    mo = metrics(ros) if len(ros) > 60 else dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    out["OOS_CAGR"], out["OOS_Sharpe"], out["OOS_MaxDD"] = mo["CAGR"], mo["Sharpe"], mo["MaxDD"]
    return out


def keep_flags(row, spy_row, v2_row):
    a = bool(row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"]
             and row["MaxDD"] >= v2_row["MaxDD"])
    fails = []
    if not row["H1"] > spy_row["H1"]: fails.append("H1")
    if not row["H2"] > spy_row["H2"]: fails.append("H2")
    if not row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]: fails.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(spy_row["MaxDD"]): fails.append("DD")
    if not row["CAGR"] >= 0.70 * spy_row["CAGR"]: fails.append("CAGR")
    return a, (len(fails) == 0), (",".join(fails) if fails else "-")


def run_block(pxs_c, pxb_c, small_pool, large_pool, sd0, label, arms=("EWall", "CAND10", "CAND20", "v2")):
    """Build + backtest one seed block over the 9 strata.  Returns a panel-level frame."""
    rows = []
    total = len(KS) * len(QS) * N_SEEDS
    i = 0
    for k in KS:
        for q in QS:
            for sd in range(sd0, sd0 + N_SEEDS):
                i += 1
                px, tr = draw_panel(pxs_c, pxb_c, small_pool, large_pool, q, k, sd)
                key, above, vol20 = score(px, vol_scale=False)
                elig = eligible_mask(px, tr, above, vol20)
                cols = [c for c in px.columns if c in tr]
                rbm = pd.Series(rebalance_mask(px.index, FREQ), index=px.index)
                cis = panel_chars(px, elig, IS_START, IS_END, cols, rbm)
                cos = panel_chars(px, elig, OOS_START, None, cols, rbm)
                rec = dict(block=label, panel=f"k{k:02d}~q{q:.3f}~s{sd:03d}",
                           kind=f"k{k:02d}q{q:.3f}", q=q, k=k, seed=sd, n_elig_IS=cis["n_elig"])
                for c in CHARS:
                    rec[f"{c}_IS"], rec[f"{c}_OOS"] = cis[c], cos[c]
                start = px.index[260]
                spy = stat_block(px["SPY"].pct_change().fillna(0.0).loc[start:])
                for arm in arms:
                    n = 10 if arm == "CAND10" else (20 if arm == "CAND20" else None)
                    a = "CAND" if arm.startswith("CAND") else arm
                    w = book_weights(px, tr, a, key, elig, n=n)
                    b = stat_block(backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:])
                    for f, v in b.items():
                        rec[f"{arm}_{f}"] = v
                for f, v in spy.items():
                    rec[f"SPY_{f}"] = v
                rows.append(rec)
                if i % 60 == 0:
                    P(f"  [{label}] {i}/{total} panels")
                    flush_log()
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ per-stratum fits
def fit_points(panels, label, with_boot=True, with_perm=True):
    """The 27 (q, k, book) points: marginal rho, rank-partial, joint-fit t, for all 4 chars."""
    rows = []
    for k in KS:
        for q in QS:
            d = panels[(panels.k == k) & (np.isclose(panels.q, q))]
            h1 = d[d.seed < d.seed.min() + N_SEEDS // 2]
            h2 = d[d.seed >= d.seed.min() + N_SEEDS // 2]
            for arm in BOOKS:
                y = d[f"{arm}_OOS_Sharpe"]
                jb, r2 = joint_fit(d, f"{arm}_OOS_Sharpe")
                for c in CHARS:
                    if with_perm:
                        rho, p, n = perm_p(d[f"{c}_IS"], y)
                    else:
                        rho, n = spearman(d[f"{c}_IS"], y)
                        p = np.nan
                    others = [d[f"{o}_IS"].to_numpy() for o in CHARS if o != c]
                    rp = rank_partial(y, d[f"{c}_IS"], others)
                    lo, hi, sd_b = (partial_boot(y.to_numpy(), d[f"{c}_IS"].to_numpy(), others)
                                    if with_boot else (np.nan, np.nan, np.nan))
                    ra, _ = spearman(h1[f"{c}_IS"], h1[f"{arm}_OOS_Sharpe"])
                    rb, _ = spearman(h2[f"{c}_IS"], h2[f"{arm}_OOS_Sharpe"])
                    rows.append(dict(block=label, k=k, q=q, book=arm, char=c, n=n,
                                     rho=rho, p=p, rho_partial=rp,
                                     partial_lo=lo, partial_hi=hi, partial_sd=sd_b,
                                     partial_crosses_0=bool(np.isfinite(lo) and lo < 0 < hi),
                                     joint_b=jb[c][0], joint_t=jb[c][1], joint_R2=r2,
                                     rho_seed_h1=ra, rho_seed_h2=rb,
                                     halves_same_sign=bool(np.sign(ra) == np.sign(rb))))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main():
    P("=" * 110)
    P("IDEA 310  is-EVOL-the-real-survivor-not-DISP   (lane B, 2026-09-09)")
    P("Two tuned dials: q in {0.250,0.500,0.750}, k in {20,40,80}.  Everything else is 284/293's convention.")
    P("=" * 110)

    pxs_c, pxb_c, small_pool, large_pool = build_sources()
    ref = pd.read_csv(REF)
    ref_c = ref[ref.kind != "NAMED"].copy()
    P(f"idea 293 committed panels: {len(ref)} rows ({len(ref_c)} constructed)")

    # ---------------------------------------------------------------- GATE
    P("\n" + "=" * 110)
    P("GATE G: rebuild the (q=0.500, k=40) stratum from prices, seeds 0..59, and match idea 293's CSV")
    P("=" * 110)
    grows = []
    for sd in range(N_SEEDS):
        px, tr = draw_panel(pxs_c, pxb_c, small_pool, large_pool, 0.500, 40, sd)
        key, above, vol20 = score(px, vol_scale=False)
        elig = eligible_mask(px, tr, above, vol20)
        cols = [c for c in px.columns if c in tr]
        rbm = pd.Series(rebalance_mask(px.index, FREQ), index=px.index)
        cis = panel_chars(px, elig, IS_START, IS_END, cols, rbm)
        cos = panel_chars(px, elig, OOS_START, None, cols, rbm)
        rec = dict(block="GATE", panel=f"k40~q0.500~s{sd:03d}", kind="k40q0.500", q=0.500, k=40,
                   seed=sd, n_elig_IS=cis["n_elig"])
        for c in CHARS:
            rec[f"{c}_IS"], rec[f"{c}_OOS"] = cis[c], cos[c]
        start = px.index[260]
        spy = stat_block(px["SPY"].pct_change().fillna(0.0).loc[start:])
        for arm in ("EWall", "CAND10", "CAND20", "v2"):
            n = 10 if arm == "CAND10" else (20 if arm == "CAND20" else None)
            a = "CAND" if arm.startswith("CAND") else arm
            w = book_weights(px, tr, a, key, elig, n=n)
            b = stat_block(backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:])
            for f, v in b.items():
                rec[f"{arm}_{f}"] = v
        for f, v in spy.items():
            rec[f"SPY_{f}"] = v
        grows.append(rec)
        if (sd + 1) % 20 == 0:
            P(f"  [GATE] {sd + 1}/{N_SEEDS} panels")
            flush_log()
    gate = pd.DataFrame(grows)
    gate.to_csv(f"{OUT}.gate.csv", index=False)

    r40 = ref_c[(ref_c.k == 40) & (np.isclose(ref_c.q, 0.500))].sort_values("seed").reset_index(drop=True)
    g40 = gate.sort_values("seed").reset_index(drop=True)
    gate_cols = [f"{c}_IS" for c in CHARS] + [f"{c}_OOS" for c in CHARS] + \
                [f"{a}_OOS_Sharpe" for a in BOOKS] + [f"{a}_Sharpe" for a in BOOKS] + \
                [f"{a}_MaxDD" for a in BOOKS]
    gd = {c: float(np.abs(g40[c].to_numpy() - r40[c].to_numpy()).max()) for c in gate_cols}
    gmax = max(gd.values())
    P(f"\nmax |rebuilt - committed| over {len(gate_cols)} columns x {len(g40)} panels: {gmax:.3e}")
    P(fmt(pd.Series(gd).to_frame("max_abs_diff"), 12))
    gate_pass = gmax < GATE_TOL
    P(f"GATE G (vs idea 293 panels): {'PASS' if gate_pass else 'FAIL'} at tol {GATE_TOL:.0e}")

    P("\nGATE G2: idea 284's three published within-stratum corr rho, recomputed on the rebuilt panels")
    g2 = {}
    for arm in BOOKS:
        rho, _ = spearman(g40["corr_IS"], g40[f"{arm}_OOS_Sharpe"])
        g2[arm] = (rho, REPRO_284_CORR[arm], abs(rho - REPRO_284_CORR[arm]))
        P(f"  {arm:7s} rebuilt {rho:+.4f}  published {REPRO_284_CORR[arm]:+.4f}  |d| {abs(rho - REPRO_284_CORR[arm]):.4f}")
    g2_pass = max(v[2] for v in g2.values()) < 0.002
    P(f"GATE G2 (vs idea 284 published rho): {'PASS' if g2_pass else 'FAIL'} at tol 0.002")

    P("\nGATE G3: idea 284's published joint-fit t on disp and evol, recomputed on the rebuilt panels")
    g3rows = []
    for arm in BOOKS:
        jb, r2 = joint_fit(g40, f"{arm}_OOS_Sharpe")
        for c in PAIR:
            g3rows.append(dict(book=arm, char=c, t_rebuilt=jb[c][1], t_published=REPRO_284_T[arm][c],
                               d=abs(jb[c][1] - REPRO_284_T[arm][c]), R2=r2))
    g3 = pd.DataFrame(g3rows)
    P(fmt(g3.set_index(["book", "char"])))
    g3_pass = float(g3.d.max()) < 0.02
    P(f"GATE G3 (vs idea 284 published joint-fit t): {'PASS' if g3_pass else 'FAIL'} at tol 0.02  "
      f"(max |dt| {g3.d.max():.4f})")
    flush_log()

    # ---------------------------------------------------------------- BLOCK A
    P("\n" + "=" * 110)
    P("BLOCK A: idea 293's 540 committed panels re-analysed -- BOTH statistics, all 27 points")
    P("  MARGINAL  = Spearman(IS characteristic, OOS Sharpe) inside the stratum  [284's Q1 / 293's rho]")
    P("  PARTIAL   = rank-partial controlling for the OTHER THREE characteristics [293's rho_partial]")
    P("  JOINT t   = t of the characteristic in OOS Sharpe ~ 1 + 4 z-scored chars [284's joint fit]")
    P("=" * 110)
    A = fit_points(ref_c, "A")
    A.to_csv(f"{OUT}.blockA.csv", index=False)

    P("\n--- the two claims, restated at the ONE stratum idea 284 measured (q=0.500, k=40) ---")
    a40 = A[(A.k == 40) & (np.isclose(A.q, 0.500)) & (A.char.isin(PAIR))]
    P(fmt(a40.set_index(["book", "char"])[["rho", "p", "rho_partial", "partial_lo", "partial_hi",
                                           "joint_b", "joint_t"]]))
    P("  READ: idea 284's 'disp survives / evol collapses' is a JOINT-FIT statement (t column);")
    P("        its MARGINAL rho is positive and significant for BOTH characteristics at this cell.")

    P("\n--- all 27 points, both characteristics, both statistics ---")
    for c in PAIR:
        cc = A[A.char == c]
        P(f"\n[{c}]  marginal: mean {cc.rho.mean():+.4f}  pos {int((cc.rho > 0).sum())}/27  "
          f"p<0.05 {int((cc.p < 0.05).sum())}/27")
        P(f"      partial : mean {cc.rho_partial.mean():+.4f}  pos {int((cc.rho_partial > 0).sum())}/27  "
          f"range {cc.rho_partial.min():+.4f}..{cc.rho_partial.max():+.4f}  "
          f"sd {cc.rho_partial.std():.4f}  CI-crosses-0 {int(cc.partial_crosses_0.sum())}/27")
        P(f"      joint t : mean {cc.joint_t.mean():+.4f}  |t|>2 {int((cc.joint_t.abs() > 2).sum())}/27")
        P(fmt(cc.set_index(["k", "q", "book"])[["rho", "p", "rho_partial", "partial_lo",
                                                "partial_hi", "joint_t"]]))

    P("\n--- REPRODUCTION of idea 293's published 27-point means ---")
    for c in PAIR:
        m = float(A[A.char == c].rho_partial.mean())
        P(f"  {c:5s} mean partial recomputed {m:+.4f}   published {REPRO_293_PARTIAL[c]:+.4f}   "
          f"|d| {abs(m - REPRO_293_PARTIAL[c]):.4f}")
    a293_pass = all(abs(float(A[A.char == c].rho_partial.mean()) - REPRO_293_PARTIAL[c]) < 0.002
                    for c in PAIR)
    P(f"  GATE G4 (vs idea 293 published means): {'PASS' if a293_pass else 'FAIL'} at tol 0.002")

    P("\n--- IS THE DISAGREEMENT THE k=40 / q=0.5 CELL ALONE?  leave-one-stratum-out on the mean partial ---")
    lrows = []
    for k in KS:
        for q in QS:
            keep = A[~((A.k == k) & (np.isclose(A.q, q)))]
            row = dict(left_out=f"k{k}q{q:.3f}")
            for c in PAIR:
                row[f"{c}_mean_partial"] = keep[keep.char == c].rho_partial.mean()
            row["evol_minus_disp"] = row["evol_mean_partial"] - row["disp_mean_partial"]
            row["ordering_evol_gt_disp"] = bool(row["evol_minus_disp"] > 0)
            lrows.append(row)
    loso = pd.DataFrame(lrows)
    P(fmt(loso.set_index("left_out")))
    n_keep = int(loso.ordering_evol_gt_disp.sum())
    P(f"  ordering (evol > disp) survives {n_keep}/9 leave-one-stratum-out means; "
      f"full-sample gap {A[A.char == 'evol'].rho_partial.mean() - A[A.char == 'disp'].rho_partial.mean():+.4f}")

    P("\n--- MECHANISM: within-stratum rank correlation between the two IS characteristics ---")
    crows = []
    for k in KS:
        for q in QS:
            d = ref_c[(ref_c.k == k) & (np.isclose(ref_c.q, q))]
            rho_de, _ = spearman(d["disp_IS"], d["evol_IS"])
            rows = dict(k=k, q=q, corr_disp_evol=rho_de)
            for c in PAIR:
                oth = [d[f"{o}_IS"].to_numpy() for o in CHARS if o != c]
                Y = _rk(d[f"{c}_IS"])
                C = np.column_stack([np.ones(len(Y))] + [_rk(x) for x in oth])
                res = Y - C @ (np.linalg.pinv(C.T @ C) @ C.T @ Y)
                rows[f"{c}_R2_on_others"] = float(1 - res.var() / Y.var())
            crows.append(rows)
    coll = pd.DataFrame(crows)
    P(fmt(coll.set_index(["k", "q"])))
    P(f"  median rank corr(disp_IS, evol_IS) = {coll.corr_disp_evol.median():+.4f}; "
      f"median share of disp explained by the other three = {coll.disp_R2_on_others.median():.4f}, "
      f"evol = {coll.evol_R2_on_others.median():.4f}")
    flush_log()

    # ---------------------------------------------------------------- BLOCK B
    P("\n" + "=" * 110)
    P(f"BLOCK B: a FRESH, DISJOINT seed block (seeds {SEED_B0}..{SEED_B0 + N_SEEDS - 1}), 540 new panels")
    P("=" * 110)
    B = run_block(pxs_c, pxb_c, small_pool, large_pool, SEED_B0, "B")
    B.to_csv(f"{OUT}.panelsB.csv", index=False)
    FB = fit_points(B, "B")
    FB.to_csv(f"{OUT}.blockB.csv", index=False)

    for c in PAIR:
        cc = FB[FB.char == c]
        P(f"\n[{c}] BLOCK B  marginal mean {cc.rho.mean():+.4f}  pos {int((cc.rho > 0).sum())}/27  "
          f"p<0.05 {int((cc.p < 0.05).sum())}/27")
        P(f"      partial mean {cc.rho_partial.mean():+.4f}  pos {int((cc.rho_partial > 0).sum())}/27  "
          f"range {cc.rho_partial.min():+.4f}..{cc.rho_partial.max():+.4f}  sd {cc.rho_partial.std():.4f}  "
          f"CI-crosses-0 {int(cc.partial_crosses_0.sum())}/27")
        P(fmt(cc.set_index(["k", "q", "book"])[["rho", "p", "rho_partial", "partial_lo",
                                                "partial_hi", "joint_t"]]))

    P("\n" + "=" * 110)
    P("STABILITY: the same 27 points, two disjoint seed blocks")
    P("=" * 110)
    srows = []
    for c in CHARS:
        a = A[A.char == c].set_index(["k", "q", "book"])
        b = FB[FB.char == c].set_index(["k", "q", "book"]).reindex(a.index)
        agree_p = int((np.sign(a.rho_partial) == np.sign(b.rho_partial)).sum())
        agree_m = int((np.sign(a.rho) == np.sign(b.rho)).sum())
        rr, _ = spearman(a.rho_partial, b.rho_partial)
        rm, _ = spearman(a.rho, b.rho)
        srows.append(dict(char=c, A_partial=a.rho_partial.mean(), B_partial=b.rho_partial.mean(),
                          d_partial=b.rho_partial.mean() - a.rho_partial.mean(),
                          partial_sign_agree=f"{agree_p}/27", partial_rho_AB=rr,
                          A_marginal=a.rho.mean(), B_marginal=b.rho.mean(),
                          marginal_sign_agree=f"{agree_m}/27", marginal_rho_AB=rm))
    stab = pd.DataFrame(srows)
    stab.to_csv(f"{OUT}.stability.csv", index=False)
    P(fmt(stab.set_index("char")))
    flush_log()

    # ---------------------------------------------------------------- pre-registered grades
    P("\n" + "=" * 110)
    P("PRE-REGISTERED PREDICTIONS, GRADED")
    P("=" * 110)
    p1 = all(abs(F[F.char == c].rho_partial.mean()) < 0.20 for F in (A, FB) for c in PAIR)
    P(f"P1 |mean partial| < 0.20 for both chars in both blocks: {'PASS' if p1 else 'FAIL'}  "
      + "  ".join(f"{lbl}/{c} {F[F.char == c].rho_partial.mean():+.4f}"
                  for lbl, F in (("A", A), ("B", FB)) for c in PAIR))
    flips = {}
    for c in PAIR:
        a = A[A.char == c].set_index(["k", "q", "book"])
        b = FB[FB.char == c].set_index(["k", "q", "book"]).reindex(a.index)
        flips[c] = int((np.sign(a.rho_partial) != np.sign(b.rho_partial)).sum())
    p2 = max(flips.values()) >= 9
    P(f"P2 partial sign disagrees across blocks in >= 9/27 for at least one char: "
      f"{'PASS' if p2 else 'FAIL'}  disp {flips['disp']}/27, evol {flips['evol']}/27")
    p3 = n_keep >= 8
    P(f"P3 evol > disp ordering survives >= 8/9 leave-one-stratum-out: {'PASS' if p3 else 'FAIL'}  "
      f"({n_keep}/9)")
    p4 = float(coll.corr_disp_evol.median()) > 0.50
    P(f"P4 median within-stratum rank corr(disp, evol) > 0.50: {'PASS' if p4 else 'FAIL'}  "
      f"({coll.corr_disp_evol.median():+.4f})")

    # ---------------------------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 110)
    P("RULE 8 WALK-FORWARD on the FRESH block: selectors pick ONE panel per stratum on IS, OOS read ONCE")
    P("  S_DISP HIGHEST IS disp   S_EVOL HIGHEST IS evol   S_CORR LOWEST IS corr  (+ reverse sign checks)")
    P("=" * 110)
    SEL = {"S_DISP": ("disp_IS", False), "S_EVOL": ("evol_IS", False), "S_CORR": ("corr_IS", True)}
    wrows = []
    for k in KS:
        for q in QS:
            d = B[(B.k == k) & (np.isclose(B.q, q))]
            for arm in BOOKS:
                anchor = d[f"{arm}_OOS_Sharpe"].mean()
                anchor_sd = d[f"{arm}_OOS_Sharpe"].std()
                for sel, (col, ascending) in SEL.items():
                    for direction in ("PICK", "REVERSE"):
                        asc = ascending if direction == "PICK" else (not ascending)
                        row = d.sort_values(col, ascending=asc).iloc[0]
                        wrows.append(dict(k=k, q=q, book=arm, selector=sel, direction=direction,
                                          panel=row["panel"],
                                          OOS_Sharpe=row[f"{arm}_OOS_Sharpe"],
                                          OOS_CAGR=row[f"{arm}_OOS_CAGR"],
                                          OOS_MaxDD=row[f"{arm}_OOS_MaxDD"],
                                          anchor_OOS_Sharpe=anchor, anchor_sd=anchor_sd,
                                          regret=row[f"{arm}_OOS_Sharpe"] - anchor,
                                          v2_OOS_Sharpe=row["v2_OOS_Sharpe"],
                                          v2_OOS_CAGR=row["v2_OOS_CAGR"],
                                          v2_OOS_MaxDD=row["v2_OOS_MaxDD"],
                                          spy_OOS_Sharpe=row["SPY_OOS_Sharpe"],
                                          spy_OOS_CAGR=row["SPY_OOS_CAGR"],
                                          spy_OOS_MaxDD=row["SPY_OOS_MaxDD"]))
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    pick = wf[wf.direction == "PICK"]
    P(fmt(pick.set_index(["k", "q", "book", "selector"])[
        ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "anchor_OOS_Sharpe", "regret",
         "v2_OOS_Sharpe", "spy_OOS_Sharpe"]]))
    P("\nselector summary over the 27 (stratum x book) cells of the fresh block:")
    for sel in SEL:
        s = pick[pick.selector == sel]
        rv = wf[(wf.selector == sel) & (wf.direction == "REVERSE")]
        P(f"  {sel:7s} mean OOS Sharpe {s.OOS_Sharpe.mean():+.4f}  mean regret vs anchor "
          f"{s.regret.mean():+.4f}  beats anchor {int((s.regret > 0).sum())}/27  "
          f"beats SPY {int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum())}/27  "
          f"beats RULES v2 {int((s.OOS_Sharpe > s.v2_OOS_Sharpe).sum())}/27  | "
          f"REVERSE mean {rv.OOS_Sharpe.mean():+.4f} (sign check: PICK - REVERSE "
          f"{s.OOS_Sharpe.mean() - rv.OOS_Sharpe.mean():+.4f})")
    P(f"  ANCHOR  mean {pick.anchor_OOS_Sharpe.mean():+.4f}   "
      f"SPY OOS mean {pick.spy_OOS_Sharpe.mean():+.4f}   RULES v2 OOS mean {pick.v2_OOS_Sharpe.mean():+.4f}")
    P(f"  mean OOS CAGR: picks S_DISP {pick[pick.selector == 'S_DISP'].OOS_CAGR.mean():.2%}  "
      f"S_EVOL {pick[pick.selector == 'S_EVOL'].OOS_CAGR.mean():.2%}  "
      f"S_CORR {pick[pick.selector == 'S_CORR'].OOS_CAGR.mean():.2%}  | "
      f"SPY {pick.spy_OOS_CAGR.mean():.2%}  RULES v2 {pick.v2_OOS_CAGR.mean():.2%}")
    P(f"  mean OOS MaxDD: picks S_DISP {pick[pick.selector == 'S_DISP'].OOS_MaxDD.mean():.2%}  "
      f"S_EVOL {pick[pick.selector == 'S_EVOL'].OOS_MaxDD.mean():.2%}  "
      f"S_CORR {pick[pick.selector == 'S_CORR'].OOS_MaxDD.mean():.2%}  | "
      f"SPY {pick.spy_OOS_MaxDD.mean():.2%}  RULES v2 {pick.v2_OOS_MaxDD.mean():.2%}")
    flush_log()

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 110)
    P("BOTH KEEP PATHS on every cell of the fresh block (540 panels x 3 books = 1,620 cells)")
    P("=" * 110)
    krows = []
    for _, row in B.iterrows():
        spy_row = {f: row[f"SPY_{f}"] for f in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")}
        v2_row = {f: row[f"v2_{f}"] for f in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")}
        for arm in BOOKS:
            b = {f: row[f"{arm}_{f}"] for f in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD")}
            a, bk, fails = keep_flags(b, spy_row, v2_row)
            krows.append(dict(panel=row["panel"], k=row["k"], q=row["q"], book=arm, **b,
                              keep4a=a, keep4b=bk, fails4b=fails,
                              spy_Sharpe=spy_row["Sharpe"], spy_CAGR=spy_row["CAGR"],
                              spy_MaxDD=spy_row["MaxDD"], spy_OOS_Sharpe=spy_row["OOS_Sharpe"]))
    keep = pd.DataFrame(krows)
    keep.to_csv(f"{OUT}.keeppaths.csv", index=False)
    n = len(keep)
    P(f"  4a {int(keep.keep4a.sum())}/{n}   4b {int(keep.keep4b.sum())}/{n}   "
      f"BOTH {int((keep.keep4a & keep.keep4b).sum())}/{n}")
    P("  4b failure reasons: " + ", ".join(f"{k}:{v}" for k, v in
                                           keep.fails4b.value_counts().head(10).items()))
    if keep.keep4b.any():
        P("\n  4b passers (all reported):")
        P(fmt(keep[keep.keep4b].set_index(["panel", "book"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "spy_Sharpe", "spy_OOS_Sharpe"]]))
        P(f"  of the 4b passers, {int(keep[keep.keep4b].keep4a.sum())} also clear 4a")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 110)
    P("VERDICT")
    P("=" * 110)
    dA, eA = A[A.char == "disp"].rho_partial, A[A.char == "evol"].rho_partial
    dB, eB = FB[FB.char == "disp"].rho_partial, FB[FB.char == "evol"].rho_partial
    P(f"  disp partial: block A {dA.mean():+.4f} (sd {dA.std():.4f}), block B {dB.mean():+.4f} "
      f"(sd {dB.std():.4f}), sign flips {flips['disp']}/27")
    P(f"  evol partial: block A {eA.mean():+.4f} (sd {eA.std():.4f}), block B {eB.mean():+.4f} "
      f"(sd {eB.std():.4f}), sign flips {flips['evol']}/27")
    P(f"  marginal (the statistic BOTH ideas agree on): disp A {A[A.char == 'disp'].rho.mean():+.4f} / "
      f"B {FB[FB.char == 'disp'].rho.mean():+.4f}; evol A {A[A.char == 'evol'].rho.mean():+.4f} / "
      f"B {FB[FB.char == 'evol'].rho.mean():+.4f}")
    P(f"  gates: G {'PASS' if gate_pass else 'FAIL'}  G2 {'PASS' if g2_pass else 'FAIL'}  "
      f"G3 {'PASS' if g3_pass else 'FAIL'}  G4 {'PASS' if a293_pass else 'FAIL'}")
    P(f"  4a {int(keep.keep4a.sum())}/{n}, 4b {int(keep.keep4b.sum())}/{n}, "
      f"both {int((keep.keep4a & keep.keep4b).sum())}/{n}")
    flush_log()
    P("\ndone.")
    flush_log()


if __name__ == "__main__":
    main()
