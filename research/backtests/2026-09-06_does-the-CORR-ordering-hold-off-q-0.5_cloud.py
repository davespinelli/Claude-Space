#!/usr/bin/env python3
"""Idea 293 - "does-the-CORR-ordering-hold-off-q-0.5" (cloud, 2026-09-06).

The question
------------
Idea 284 held capitalisation fixed (q = 0.5, twenty small + twenty large, k = 40) and found
that `breadth` has ZERO independent content while `corr` and `disp` survive with signs OPPOSITE
to their pooled (cross-stratum) signs.  The `corr` reading was the headline: Spearman(IS mean
pairwise correlation, OOS Sharpe) = -0.3648 / -0.4815 / -0.4708 on CAND10 / CAND20 / EWall,
permutation p 0.0046 / 0.0003 / 0.0005, negative in BOTH seed halves in all three books, and the
only individually significant coefficient in the joint fit.  It was parked, not kept, because it
was measured at ONE cap mix (q = 0.5) and ONE panel width (k = 40).

A Simpson reversal that appears at exactly one interior point of the mixing axis is indis-
tinguishable from an artefact of that point.  So:

    Is the within-stratum NEGATIVE corr->OOS-Sharpe ordering a property of fixed-capitalisation
    panels, or is it a q = 0.5 / k = 40 artefact?

Design
------
The construction of idea 284 is re-run VERBATIM (same sources, same gate, same books, same
characteristic estimator, same permutation machinery) over a full cross of the two dials the
queue names:

    q in {0.25, 0.50, 0.75}   share of the k names drawn from SMALL439, rest from BSTK100
    k in {20, 40, 80}         panel width

    9 strata x 60 seeded draws = 540 constructed panels, plus the 5 NAMED reproduction panels
    (U56, B136, BSTK100, ETF36, SMALL439) = 545 panels.  Every panel is reported.

Seeds are REPLICATION, never selection.  The seed key is idea 284's verbatim,
`STRAT|{q:.3f}|{sd}` -- k deliberately absent -- which buys two things:

  (1) the (q = 0.500, k = 40) stratum is idea 284's stratum BIT-IDENTICALLY, so its 27 numbers
      are a hard reproduction gate asserted before any new stratum is read; and
  (2) strata that differ only in k are seed-PAIRED, so the k contrast is not a fresh draw.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q  (3 values)
    2. k  (3 values)
Everything else is fixed at the record's published conventions and is NOT tuned: 60 seeds, the
RULES v1 gate (px > 200d MA AND vol20 < 0.60), the composite score without the vol scaler as
ranking key, 75% gross, weekly cadence, 10 bps, next-day execution, IS <= 2016-12-31.
`n` is NOT a third dial here -- CAND10/CAND20/EWall are the three books idea 284 reported and
every one of them is reported at every grid point; no book is selected on its result.
The four characteristics are MEASURED, not tuned; every selector direction is pre-registered
below, before any OOS number is read.

Pre-registered predictions (written before the run; graded verbatim in the result)
    P1  corr rho_within < 0 in at least 7 of the 9 strata on CAND20  -> ordering is general.
    P2  the q = 0.500 / k = 40 cell reproduces -0.3648 / -0.4815 / -0.4708 to < 0.002.
    P3  breadth rho_within stays indistinguishable from 0 at every (q, k).
    P4  the POOLED (cross-stratum) corr rho is POSITIVE, i.e. the reversal is reproduced.

Rule 8 walk-forward (required; directions fixed before any OOS number was read)
    IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end read ONCE.
    Inside EVERY stratum each pre-registered selector picks ONE panel on its IS characteristic
    and that panel's OOS book is read:
        S_CORR     LOWEST IS mean pairwise correlation   (idea 284's surviving direction)
        S_DISP     HIGHEST IS dispersion                 (idea 284's other survivor)
        S_BREADTH  HIGHEST IS breadth                    (the killed one, carried as a control)
        S_EVOL     LOWEST IS eligible-set vol
        S_EWALL    HIGHEST IS EWall Sharpe               (idea 271's winner, the bar to beat)
        S_ISS      HIGHEST IS Sharpe of the book itself  (the classic IS chooser)
    Each selector's REVERSE extreme is reported as a sign check.  The do-nothing anchor is the
    MEAN OOS Sharpe over the 60 draws of that stratum with its seed sd, so "beats a coin flip"
    is a number.  SPY, RULES v2 and RULES v1 OOS are reported beside every anchor.

Verdicts (both KEEP paths, on every grid point)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens, so every panel
inherits the bias whole and the LEVEL of every panel's return is inflated.  The object under
test is whether a characteristic ORDERS panels within a fixed cap mix, and the bias is common to
all panels of a stratum; it inflates between-panel spread in level, which is what a
characteristic would have to order, so it runs AGAINST a "nothing separates" verdict.  It does
NOT protect a "the ordering is general" verdict, which is the one this run may reach -- so that
verdict is stated as a within-corpus regularity, never as a tradable edge.  The 44 SMALL439
tickers with max_1d_move >= 1.0 are dropped before any draw (data/small_meta.csv).

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
Outputs: .panels.csv .cells.csv .strata.csv .walkforward.csv .console.txt
"""
import sys
import zlib
import json
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
W_FIXED = 0.15
BAND_V2 = 0.03
QS = [0.250, 0.500, 0.750]
KS = [20, 40, 80]
N_SEEDS = 60
CHARS = ["breadth", "disp", "corr", "evol"]
ARMS = ["EWall", "CAND10", "CAND20", "v1", "v2"]
BOOKS = ["EWall", "CAND10", "CAND20"]          # the three the verdict is read on
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
N_PERM = 20000
REPRO_CELL = (0.500, 40)
REPRO_284 = {"CAND10": -0.3648, "CAND20": -0.4815, "EWall": -0.4708}   # idea 284, published
REPRO_284_TOL = 0.002

OUT = Path(__file__).with_suffix("")
LOG = []

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


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
    """Two-sided permutation p for Spearman under label exchangeability (idea 284's estimator)."""
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


def rank_partial(y, x, controls):
    """Spearman-style partial: rank everything, residualise x and y on the controls, correlate."""
    def rk(v):
        v = pd.Series(np.asarray(v, float)).rank().to_numpy()
        return (v - v.mean()) / (v.std() if v.std() > 0 else 1.0)
    Y, X = rk(y), rk(x)
    C = np.column_stack([np.ones(len(Y))] + [rk(c) for c in controls])
    B = np.linalg.pinv(C.T @ C) @ C.T
    ry = Y - C @ (B @ Y)
    rx = X - C @ (B @ X)
    if ry.std() == 0 or rx.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def ols(y, X):
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
    return b, t, r2, n


# ------------------------------------------------------------------ sources (idea 284 verbatim)
def build_sources():
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
    P(f"sources: BSTK{len(b_stk)} large-cap stocks, SMALL{len(s_stk)} small-cap stocks "
      f"({len(bad)} dropped for max_1d_move >= 1.0), ETF{len(etf36)} ETFs, "
      f"U56 {len([c for c in px56.columns if c != 'SPY'])}")
    return px56, px136, pxs, etf36, b_stk, s_stk


def build_pool(px56, px136, pxs, etf36, b_stk, s_stk):
    idx = pxs.index.intersection(px136.index)
    pxs_c = pxs.reindex(idx).ffill()
    pxb_c = px136.reindex(idx).ffill()
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days)")

    pool = {}

    def sub(px, cols, tradable):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        return px[keep].dropna(how="all").ffill(), set(tradable)

    named = {
        "U56": sub(px56, [c for c in px56.columns if c != "SPY"], [c for c in px56.columns if c != "SPY"]),
        "B136": sub(px136, [c for c in px136.columns if c != "SPY"], [c for c in px136.columns if c != "SPY"]),
        "BSTK100": sub(px136, b_stk, b_stk),
        "ETF36": sub(px136, etf36, etf36),
        "SMALL439": sub(pxs, s_stk, s_stk),
    }
    for nm, (p, t) in named.items():
        pool[nm] = dict(px=p, tradable=t, kind="NAMED", q=np.nan, k=len(t), seed=-1)

    small_pool = np.array(sorted(s_stk))
    large_pool = np.array(sorted(b_stk))
    for k in KS:
        for q in QS:
            n_s = int(round(q * k))
            n_l = k - n_s
            assert n_s <= len(small_pool) and n_l <= len(large_pool), (k, q)
            for sd in range(N_SEEDS):
                seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)   # idea 284's key
                rng = np.random.default_rng(seed)
                sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
                lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
                parts = []
                if lc:
                    parts.append(pxb_c[lc])
                if sc:
                    parts.append(pxs_c[sc])
                p = pd.concat(parts + [pxb_c["SPY"].rename("SPY")], axis=1).dropna(how="all").ffill()
                pool[f"k{k:02d}~q{q:.3f}~s{sd:02d}"] = dict(
                    px=p, tradable=set(sc) | set(lc), kind=f"k{k:02d}q{q:.3f}",
                    q=q, k=k, seed=sd)
    return pool


# ------------------------------------------------------------------ books (idea 284 verbatim)
def eligible_mask(px, tradable, above, vol20):
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def book_weights(px, tradable, arm, key, elig, n=None):
    if arm == "v1":
        s_v1, _, _ = score(px, vol_scale=True)
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


# ------------------------------------------------------------------ characteristics (idea 277/284)
def panel_chars(px, tradable, elig, lo, hi, cols=None, rbmask=None):
    cols = cols if cols is not None else [c for c in px.columns if c in tradable]
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
    return dict(k=k, n_elig=float(nel.median()), breadth=breadth, disp=disp, corr=corr,
                evol=evol, days=len(rb))


# ------------------------------------------------------------------ main
def main():
    px56, px136, pxs, etf36, b_stk, s_stk = build_sources()
    pool = build_pool(px56, px136, pxs, etf36, b_stk, s_stk)
    nstrat = sum(1 for v in pool.values() if v["kind"] != "NAMED")
    P(f"pool: {len(pool)} panels ({nstrat} constructed = {len(KS)}k x {len(QS)}q x {N_SEEDS} seeds, "
      f"5 named).  Tuned dials: q {QS}, k {KS}.")
    P(f"reproduction gate: stratum q={REPRO_CELL[0]:.3f} k={REPRO_CELL[1]} must reproduce idea 284's "
      f"corr rho_within {REPRO_284} to {REPRO_284_TOL}")

    prows, crows = [], []
    for i, (name, meta) in enumerate(pool.items(), 1):
        px, tr = meta["px"], meta["tradable"]
        key, above, vol20 = score(px, vol_scale=False)
        elig = eligible_mask(px, tr, above, vol20)
        cols = [c for c in px.columns if c in tr]
        rbm = pd.Series(rebalance_mask(px.index, FREQ), index=px.index)
        cis = panel_chars(px, tr, elig, IS_START, IS_END, cols, rbm)
        cos = panel_chars(px, tr, elig, OOS_START, None, cols, rbm)
        rec = dict(panel=name, kind=meta["kind"], q=meta["q"], k=meta["k"], seed=meta["seed"],
                   n_elig_IS=cis["n_elig"])
        for c in CHARS:
            rec[f"{c}_IS"] = cis[c]
            rec[f"{c}_OOS"] = cos[c]

        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_row = stat_block(spy_r)

        books = {}
        for arm, n in [("EWall", None), ("CAND10", 10), ("CAND20", 20), ("v1", None), ("v2", None)]:
            w = book_weights(px, tr, "CAND" if arm.startswith("CAND") else arm, key, elig, n=n)
            r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            books[arm] = stat_block(r)
        v2_row = books["v2"]

        for arm in ARMS:
            b = books[arm]
            a, bkeep, fails = keep_flags(b, spy_row, v2_row)
            crows.append(dict(panel=name, kind=meta["kind"], q=meta["q"], k=meta["k"],
                              seed=meta["seed"], arm=arm,
                              **{kk: b[kk] for kk in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                      "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
                                                      "OOS_MaxDD")},
                              keep4a=a, keep4b=bkeep, fails4b=fails,
                              spy_Sharpe=spy_row["Sharpe"], spy_OOS_Sharpe=spy_row["OOS_Sharpe"],
                              spy_CAGR=spy_row["CAGR"], spy_MaxDD=spy_row["MaxDD"]))
            for f in ("IS_Sharpe", "OOS_Sharpe", "Sharpe", "CAGR", "MaxDD", "H1", "H2",
                      "OOS_CAGR", "OOS_MaxDD"):
                rec[f"{arm}_{f}"] = books[arm][f]
        for f in ("Sharpe", "OOS_Sharpe", "CAGR", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"):
            rec[f"SPY_{f}"] = spy_row[f]
        prows.append(rec)
        if i % 25 == 0 or i == len(pool):
            P(f"  ... {i}/{len(pool)} panels")
            flush_log()

    panels = pd.DataFrame(prows)
    cells = pd.DataFrame(crows)
    panels.to_csv(f"{OUT}.panels.csv", index=False)
    cells.to_csv(f"{OUT}.cells.csv", index=False)

    named = panels[panels.kind == "NAMED"].set_index("panel")
    P("\n=== REPRODUCTION A: named panels, idea 271/284 characteristics (IS 2009-2016) ===")
    P(fmt(named[["k", "n_elig_IS"] + [f"{c}_IS" for c in CHARS] +
                ["CAND20_CAGR", "CAND20_Sharpe", "CAND20_MaxDD", "CAND20_OOS_Sharpe",
                 "EWall_OOS_Sharpe"]]))
    P(f"SPY on the common calendar: CAGR {named['SPY_CAGR'].iloc[0]:.4f}  "
      f"Sharpe {named['SPY_Sharpe'].iloc[0]:.4f}  MaxDD {named['SPY_MaxDD'].iloc[0]:.4f}  "
      f"halves {named['SPY_H1'].iloc[0]:.4f}/{named['SPY_H2'].iloc[0]:.4f}  "
      f"OOS {named['SPY_OOS_Sharpe'].iloc[0]:.4f}")

    # ---------------- reproduction gate on the (0.500, 40) stratum
    rep_kind = f"k{REPRO_CELL[1]:02d}q{REPRO_CELL[0]:.3f}"
    rep = panels[panels.kind == rep_kind]
    P(f"\n=== REPRODUCTION B: stratum {rep_kind} vs idea 284 (n={len(rep)}) ===")
    gate_ok = True
    for arm in BOOKS:
        r, _ = spearman(rep["corr_IS"], rep[f"{arm}_OOS_Sharpe"])
        d = abs(r - REPRO_284[arm])
        ok = d < REPRO_284_TOL
        gate_ok &= ok
        P(f"  corr rho_within {arm:7s} = {r:+.4f}   idea 284 published {REPRO_284[arm]:+.4f}   "
          f"|diff| {d:.5f}   {'OK' if ok else 'MISMATCH'}")
    P(f"  reproduction gate: {'PASS' if gate_ok else 'FAIL'}")
    flush_log()

    # ---------------- stratum descriptives
    P("\n=== STRATUM DESCRIPTIVES (60 draws each, all reported) ===")
    srows = []
    for k in KS:
        for q in QS:
            d = panels[panels.kind == f"k{k:02d}q{q:.3f}"]
            row = dict(k=k, q=q, n=len(d))
            for c in CHARS:
                row[f"{c}_mean"] = d[f"{c}_IS"].mean()
                row[f"{c}_sd"] = d[f"{c}_IS"].std()
            for arm in BOOKS:
                row[f"{arm}_OOSmean"] = d[f"{arm}_OOS_Sharpe"].mean()
                row[f"{arm}_OOSsd"] = d[f"{arm}_OOS_Sharpe"].std()
            srows.append(row)
    desc = pd.DataFrame(srows)
    P(fmt(desc.set_index(["k", "q"])))

    # ---------------- Q1: within-stratum corr ordering at every (q, k)
    P("\n=== Q1: Spearman(IS characteristic, OOS Sharpe) INSIDE each stratum ===")
    P(f"permutation p, {N_PERM} label permutations.  ALL {len(KS) * len(QS) * len(CHARS) * len(BOOKS)} "
      f"grid points reported.")
    grows = []
    for k in KS:
        for q in QS:
            d = panels[panels.kind == f"k{k:02d}q{q:.3f}"]
            h1 = d[d.seed < N_SEEDS // 2]
            h2 = d[d.seed >= N_SEEDS // 2]
            for arm in BOOKS:
                y = d[f"{arm}_OOS_Sharpe"]
                for c in CHARS:
                    rho, p, n = perm_p(d[f"{c}_IS"], y)
                    others = [d[f"{o}_IS"].to_numpy() for o in CHARS if o != c]
                    rp = rank_partial(y, d[f"{c}_IS"], others)
                    ra, _ = spearman(h1[f"{c}_IS"], h1[f"{arm}_OOS_Sharpe"])
                    rb, _ = spearman(h2[f"{c}_IS"], h2[f"{arm}_OOS_Sharpe"])
                    rstab, _ = spearman(d[f"{c}_IS"], d[f"{c}_OOS"])
                    ris, _ = spearman(d[f"{c}_IS"], d[f"{arm}_IS_Sharpe"])
                    grows.append(dict(k=k, q=q, book=arm, char=c, n=n, rho=rho, p=p,
                                      rho_partial=rp, rho_seed_h1=ra, rho_seed_h2=rb,
                                      both_halves_same_sign=bool(np.sign(ra) == np.sign(rb)),
                                      rho_IS=ris, IS_OOS_stability=rstab))
    grid = pd.DataFrame(grows)
    grid.to_csv(f"{OUT}.strata.csv", index=False)
    for c in CHARS:
        P(f"\n--- {c} ---")
        P(fmt(grid[grid.char == c].pivot_table(index=["k", "q"], columns="book",
                                               values=["rho", "p"])))
    P("\nHeadline table: corr, every stratum, every book")
    P(fmt(grid[grid.char == "corr"].set_index(["k", "q", "book"])
          [["n", "rho", "p", "rho_partial", "rho_seed_h1", "rho_seed_h2",
            "both_halves_same_sign", "IS_OOS_stability"]]))
    flush_log()

    P("\n=== P1 GRADE: sign stability of corr rho_within across the 9 strata ===")
    for arm in BOOKS:
        g = grid[(grid.char == "corr") & (grid.book == arm)]
        neg = int((g.rho < 0).sum())
        sig = int(((g.rho < 0) & (g.p < 0.05)).sum())
        P(f"  {arm:7s}: {neg}/9 strata negative, {sig}/9 negative at p<0.05, "
          f"mean rho {g.rho.mean():+.4f}  range {g.rho.min():+.4f}..{g.rho.max():+.4f}, "
          f"both-seed-halves-same-sign {int(g.both_halves_same_sign.sum())}/9")
    g = grid[grid.char == "corr"]
    P(f"  ALL BOOKS: {int((g.rho < 0).sum())}/{len(g)} negative, "
      f"{int(((g.rho < 0) & (g.p < 0.05)).sum())}/{len(g)} negative at p<0.05, "
      f"mean {g.rho.mean():+.4f}")
    P("\n=== P3 GRADE: breadth inside the strata (should be ~0 everywhere) ===")
    b = grid[grid.char == "breadth"]
    P(f"  |rho| mean {b.rho.abs().mean():.4f}, max {b.rho.abs().max():.4f}; "
      f"{int((b.p < 0.05).sum())}/{len(b)} at p<0.05; "
      f"both-seed-halves-same-sign {int(b.both_halves_same_sign.sum())}/{len(b)}")
    for c in CHARS:
        cc = grid[grid.char == c]
        P(f"  [{c:8s}] mean rho {cc.rho.mean():+.4f}  neg {int((cc.rho < 0).sum())}/{len(cc)}  "
          f"p<0.05 {int((cc.p < 0.05).sum())}/{len(cc)}  "
          f"mean partial {cc.rho_partial.mean():+.4f}")

    # ---------------- P4: pooled (cross-stratum) sign, reproduced
    P("\n=== P4 GRADE: POOLED across strata (the reversal control) ===")
    prow = []
    for k in KS:
        d = panels[panels.k == k].dropna(subset=["q"])
        for arm in BOOKS:
            for c in CHARS:
                rho, p, n = perm_p(d[f"{c}_IS"], d[f"{arm}_OOS_Sharpe"])
                prow.append(dict(scope=f"pooled q at k={k}", book=arm, char=c, n=n, rho=rho, p=p))
    dall = panels[panels.kind != "NAMED"]
    for arm in BOOKS:
        for c in CHARS:
            rho, p, n = perm_p(dall[f"{c}_IS"], dall[f"{arm}_OOS_Sharpe"])
            prow.append(dict(scope="pooled all 540", book=arm, char=c, n=n, rho=rho, p=p))
    pooled = pd.DataFrame(prow)
    P(fmt(pooled.pivot_table(index=["scope", "char"], columns="book", values="rho")))
    P("\n  Within-vs-pooled contrast for corr (mean within-stratum rho vs pooled rho):")
    for arm in BOOKS:
        w = grid[(grid.char == "corr") & (grid.book == arm)].rho.mean()
        po = pooled[(pooled.scope == "pooled all 540") & (pooled.char == "corr") &
                    (pooled.book == arm)].rho.iloc[0]
        P(f"    {arm:7s} within {w:+.4f}   pooled {po:+.4f}   "
          f"{'REVERSAL REPRODUCED' if w * po < 0 else 'no reversal'}")

    P("\n=== Joint fit inside each stratum: OOS Sharpe ~ 1 + four z-scored IS characteristics ===")
    for k in KS:
        for q in QS:
            d = panels[panels.kind == f"k{k:02d}q{q:.3f}"]
            for arm in BOOKS:
                dd = d.dropna(subset=[f"{arm}_OOS_Sharpe"])
                Z = np.column_stack([np.ones(len(dd))] +
                                    [((dd[f"{c}_IS"] - dd[f"{c}_IS"].mean()) /
                                      dd[f"{c}_IS"].std()).to_numpy() for c in CHARS])
                bb, tt, r2, n = ols(dd[f"{arm}_OOS_Sharpe"], Z)
                P(f"  k={k:2d} q={q:.2f} {arm:7s} n={n} R2={r2:.4f}  " +
                  "  ".join(f"{c} b={x:+.4f} t={y:+.2f}"
                            for c, x, y in zip(["const"] + CHARS, bb, tt)))
    flush_log()

    # ---------------- Rule 8 walk-forward, every stratum
    P("\n=== Rule 8 WALK-FORWARD in every stratum (selectors pre-registered) ===")
    SEL = {
        "S_CORR":    ("corr_IS", "min", "LOWEST IS mean pairwise correlation"),
        "S_DISP":    ("disp_IS", "max", "HIGHEST IS dispersion"),
        "S_BREADTH": ("breadth_IS", "max", "HIGHEST IS breadth"),
        "S_EVOL":    ("evol_IS", "min", "LOWEST IS eligible-set vol"),
        "S_EWALL":   ("EWall_IS_Sharpe", "max", "HIGHEST IS EWall Sharpe"),
    }
    wf = []
    for k in KS:
        for q in QS:
            d = panels[panels.kind == f"k{k:02d}q{q:.3f}"].copy()
            for arm in ("CAND10", "CAND20"):
                dd = d.dropna(subset=[f"{arm}_OOS_Sharpe"])
                anchor = dd[f"{arm}_OOS_Sharpe"].mean()
                asd = dd[f"{arm}_OOS_Sharpe"].std()
                best = dd[f"{arm}_OOS_Sharpe"].max()
                spy_oos = dd["SPY_OOS_Sharpe"].mean()
                v2_oos = dd["v2_OOS_Sharpe"].mean()
                v1_oos = dd["v1_OOS_Sharpe"].mean()
                sels = dict(SEL)
                sels["S_ISS"] = (f"{arm}_IS_Sharpe", "max", "HIGHEST IS Sharpe of the book")
                for nm, (col, direction, desc) in sels.items():
                    for lbl, dr in ((nm, direction),
                                    (nm + "^rev", "min" if direction == "max" else "max")):
                        pick = dd.loc[dd[col].idxmax() if dr == "max" else dd[col].idxmin()]
                        _, kb, fails = keep_flags(
                            {x: pick[f"{arm}_{x}"] for x in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                            {x: pick[f"SPY_{x}"] for x in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                            {x: pick[f"v2_{x}"] for x in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")})
                        wf.append(dict(k=k, q=q, book=arm, rule=lbl,
                                       prereg=desc if lbl == nm else "sign check",
                                       pick=pick["panel"], IS_Sharpe=pick[f"{arm}_IS_Sharpe"],
                                       OOS_CAGR=pick[f"{arm}_OOS_CAGR"],
                                       OOS_Sharpe=pick[f"{arm}_OOS_Sharpe"],
                                       OOS_MaxDD=pick[f"{arm}_OOS_MaxDD"],
                                       vs_anchor=pick[f"{arm}_OOS_Sharpe"] - anchor,
                                       vs_SPY=pick[f"{arm}_OOS_Sharpe"] - spy_oos,
                                       vs_v2=pick[f"{arm}_OOS_Sharpe"] - v2_oos,
                                       regret=best - pick[f"{arm}_OOS_Sharpe"],
                                       keep4b=kb, fails4b=fails))
                wf.append(dict(k=k, q=q, book=arm, rule="ANCHOR (do nothing, mean of 60)",
                               prereg="control", pick="-",
                               IS_Sharpe=dd[f"{arm}_IS_Sharpe"].mean(),
                               OOS_CAGR=dd[f"{arm}_OOS_CAGR"].mean(), OOS_Sharpe=anchor,
                               OOS_MaxDD=dd[f"{arm}_OOS_MaxDD"].mean(), vs_anchor=0.0,
                               vs_SPY=anchor - spy_oos, vs_v2=anchor - v2_oos,
                               regret=best - anchor, keep4b=False, fails4b="n/a (mean)"))
                P(f"  k={k:2d} q={q:.2f} [{arm}] anchor OOS Sharpe {anchor:.4f} (seed sd {asd:.4f}, "
                  f"best {best:.4f});  SPY OOS {spy_oos:.4f}  v2 OOS {v2_oos:.4f}  "
                  f"v1 OOS {v1_oos:.4f}")
    wfdf = pd.DataFrame(wf)
    wfdf.to_csv(f"{OUT}.walkforward.csv", index=False)

    P("\nS_CORR (pre-registered direction) edge over the do-nothing anchor, every stratum:")
    sc = wfdf[wfdf.rule == "S_CORR"]
    P(fmt(sc.pivot_table(index=["k", "q"], columns="book", values="vs_anchor")))
    P("S_CORR^rev (sign check: should be WORSE than the anchor if the direction is real):")
    P(fmt(wfdf[wfdf.rule == "S_CORR^rev"].pivot_table(index=["k", "q"], columns="book",
                                                      values="vs_anchor")))
    P("\nAll selectors, mean edge over the anchor across the 9 strata (pre-registered only):")
    prime = wfdf[~wfdf.rule.str.endswith("^rev") & ~wfdf.rule.str.startswith("ANCHOR")]
    P(fmt(prime.pivot_table(index="rule", columns="book",
                            values="vs_anchor", aggfunc=["mean", "min", "max"])))
    P("\nWin count over the anchor (of 9 strata), pre-registered directions:")
    P(fmt(prime.assign(win=prime.vs_anchor > 0)
          .pivot_table(index="rule", columns="book", values="win", aggfunc="sum")))
    P("\nS_CORR full detail, every stratum and both books:")
    P(fmt(sc.set_index(["k", "q", "book"])
          [["pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "vs_anchor",
            "vs_SPY", "vs_v2", "regret", "keep4b", "fails4b"]]))
    flush_log()

    # ---------------- KEEP paths
    P("\n=== KEEP PATHS over every grid cell (all reported) ===")
    kp = cells.groupby(["kind", "arm"]).agg(n=("keep4a", "size"), keep4a=("keep4a", "sum"),
                                            keep4b=("keep4b", "sum"),
                                            Sharpe=("Sharpe", "mean"),
                                            OOS_Sharpe=("OOS_Sharpe", "mean"),
                                            CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"))
    P(fmt(kp))
    P(f"\n4a passes: {int(cells.keep4a.sum())} of {len(cells)} cells.")
    P(f"4b passes: {int(cells.keep4b.sum())} of {len(cells)} cells.")
    passes = cells[cells.keep4b]
    if len(passes):
        P(fmt(passes.sort_values("OOS_Sharpe", ascending=False)
              [["panel", "kind", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                "keep4a"]].head(40).set_index(["panel", "arm"])))
        P("\n4b pass counts by stratum and arm:")
        P(fmt(passes.pivot_table(index=["k", "q"], columns="arm", values="keep4b",
                                 aggfunc="sum", fill_value=0)))
        P("\nIs a 4b passer distinguished by its IS corr?  (mean IS corr, passers vs rest, "
          "per stratum, CAND20)")
        for k in KS:
            for q in QS:
                d = panels[panels.kind == f"k{k:02d}q{q:.3f}"].copy()
                nm = set(passes[(passes.arm == "CAND20") & (passes.k == k) &
                                (passes.q == q)].panel)
                if not nm:
                    continue
                d["pass"] = d.panel.isin(nm)
                m = d.groupby("pass")[["corr_IS", "disp_IS", "breadth_IS", "evol_IS",
                                       "CAND20_OOS_Sharpe"]].mean()
                P(f"  k={k} q={q:.2f}  {len(nm)} passers / {len(d)}")
                P(fmt(m))
    P("\nfails4b census (why cells fail), CAND20 only:")
    P(fmt(cells[cells.arm == "CAND20"].groupby("fails4b").size().sort_values(ascending=False)
          .to_frame("cells").head(20), 0))

    flush_log()
    P(f"\nwrote {OUT.name}.panels.csv .cells.csv .strata.csv .walkforward.csv .console.txt")
    flush_log()


if __name__ == "__main__":
    main()
