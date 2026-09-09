#!/usr/bin/env python3
"""Idea 308 - "why-does-the-CORR-ordering-die-at-q-0.75" (cloud, 2026-09-09).

The question
------------
Idea 293 re-ran idea 284's construction over the full cross q in {0.25, 0.50, 0.75} x
k in {20, 40, 80}, 60 seeded panels per stratum, and found the corr ordering -- the
cross-panel Spearman rho between a panel's IS average pairwise correlation and that panel's
OOS book Sharpe -- decaying in the SMALL-CAP SHARE q and not in the width k:

    mean rho_within   -0.3426 (q=0.25)   -0.3152 (q=0.50)   -0.1462 (q=0.75)
    significant       7/9                 7/9                1/9
    seed halves agree 9/9                 9/9                4/9

The queue names two candidate causes and asks for the two statistics that separate them:
    (A) RANGE RESTRICTION -- the cross-panel SPREAD of corr_IS shrinks as q rises, so the
        predictor has less variation to work with and rho attenuates mechanically.
    (B) A RISING OOS SHARPE NOISE FLOOR -- the OOS Sharpe of a q=0.75 panel is a noisier
        estimate of that panel's true Sharpe, so the outcome carries more measurement error
        and rho attenuates for a completely different reason.
These are not rival stories about the world; they are rival terms in an IDENTITY.  In raw
(Pearson) space rho = beta * sd_x / sd_y exactly, so the q=0.25 -> q=0.75 change in log|rho|
decomposes ADDITIVELY into d log|beta| + d log sd_x - d log sd_y, and this run reports that
decomposition per stratum instead of arguing about which story sounds better.  The noise
question is then whether the sd_y term (if any) is signal or measurement error, which is
answered by a reliability coefficient, not by sd_y itself.

Design (fixed before any number was read)
-----------------------------------------
FIXED, never varied -- idea 284/293's construction VERBATIM:
    panels     540 constructed = 3 q x 3 k x 60 seeds, seed key crc32("STRAT|{q:.3f}|{sd}")
               exactly as idea 284, drawn from BSTK (large-cap stocks in universe_broad) and
               the sub-$2B small-cap panel; plus the 5 named panels for the gates.
    books      EWall, CAND10, CAND20 (idea 293's three verdict books) + v2 (the 4a comparand).
    execution  weekly, 10 bps, next-day (t decided, t+1 applied), gross 0.75.
    windows    IS 2009-01-01..2016-12-31, OOS 2017-01-01.. (PROTOCOL rule 8).
    statistic  Spearman rho (idea 293's headline) reported beside Pearson rho (the one in
               which the decomposition identity is exact).  Both are always shown.

TUNED PARAMETERS -- exactly two, the same two idea 293 tuned (q, k):
    q in {0.25, 0.50, 0.75}   small-cap share (the dial the effect dies on)
    k in {20, 40, 80}         panel width
    ALL 9 strata x 3 books = 27 cells reported.  Nothing is selected on the outcome.

Pre-registered claims, written before any number was read
---------------------------------------------------------
C1  THE TWO STATISTICS THE QUEUE ASKS FOR, per stratum x book:
      sd(corr_IS) across the 60 seeds  -- the predictor spread (cause A)
      sd(OOS Sharpe) across the 60 seeds -- the outcome spread (cause B, upper bound)
C2  THE EXACT DECOMPOSITION.  rho_pearson = beta * sd_x / sd_y.  Report, per (k, book), the
    q=0.25 -> q=0.75 change split into the beta term, the sd_x term and the sd_y term, in
    log units.  Whichever term carries the change IS the answer; there is nothing to argue.
C3  IS THE sd_y TERM NOISE OR SIGNAL?  Two independent reliability estimates of OOS Sharpe:
      (i)  ANALYTIC  Lo (2002) SE(Sharpe) = sqrt((1 + S^2/2)/T_years); noise variance is the
           cross-seed mean of SE^2, reliability R_a = 1 - mean(SE^2)/var(OOS Sharpe).
      (ii) EMPIRICAL SPLIT-HALF  Sharpe measured on two disjoint OOS sub-windows (A and B,
           split at the OOS median date), correlated across the 60 seeds, Spearman-Brown
           corrected: R_e = 2 r_AB / (1 + r_AB).
    Disattenuated rho = rho / sqrt(R).  If the noise floor is the cause, disattenuating
    RESTORES the q=0.75 ordering to the q=0.25 level; if range restriction is the cause,
    it does not, and the range-restriction correction (Thorndike case 2, applied on the
    predictor) does.  BOTH corrections are reported for every cell; neither is chosen.
C4  RULE 8 (PROTOCOL 8).  Direction and selector fitted on the FIRST seed half (seeds 0-29)
    using IS-window statistics ONLY, then applied once to the untouched SECOND seed half
    (seeds 30-59); report the picks' OOS CAGR / Sharpe / MaxDD against the do-nothing anchor
    (the stratum's mean panel), against SPY, and against the live RULES v2 book on the same
    panel.  A selector that only works with both seed halves in hand is not a selector.
C5  BOTH KEEP PATHS on every panel x book, no selection:
      4a  Sharpe > RULES v2 on the SAME panel in BOTH halves AND MaxDD no worse.
      4b  Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% SPY, CAGR >= 70% SPY.

Gates (asserted before any verdict is read)
    G1  this run's rebuilt panels reproduce idea 293's COMMITTED .panels.csv (corr_IS and the
        three books' OOS Sharpe) to < 1e-9 on all 540 constructed panels -- i.e. the panel
        draw and the books are the same objects, not a re-specification.
    G2  the (q=0.500, k=40) stratum reproduces idea 284's published corr rho_within
        (EWall -0.4708, CAND10 -0.3648, CAND20 -0.4815) to < 2e-3.
    G3  idea 293's published q-gradient of the mean rho (-0.3426 / -0.3152 / -0.1462) is
        reproduced from this run's own 27 cells to < 2e-3.

SURVIVORSHIP: every panel here is drawn from CURRENT constituents of universe_broad.json and
of the sub-$2B screen (data/prices_small.csv.gz, less the 44 tickers with max_1d_move >= 1.0
in data/small_meta.csv).  No delistings, no dead names.  Small-cap survivorship is the worse
of the two, so the q dial -- the dial this whole run is about -- is also the dial along which
survivorship inflation rises.  Every level below is inflated; the CROSS-STRATUM CONTRASTS
this run reports are the defensible objects, not the levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .panels.csv .strata.csv .decomp.csv .walkforward.csv .keeppaths.csv .console.txt .result.md
"""
import json
import sys
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state
from engine import backtest, metrics, rebalance_mask

QS = [0.250, 0.500, 0.750]
KS = [20, 40, 80]
N_SEEDS = 60
BOOKS = ["EWall", "CAND10", "CAND20"]
COST_BPS = 10
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
BAND_V2 = 0.03
IS_START, IS_END = "2009-01-01", "2016-12-31"
OOS_START = "2017-01-01"
CHARS = ["breadth", "disp", "corr", "evol"]

REPRO_284 = {"EWall": -0.4708, "CAND10": -0.3648, "CAND20": -0.4815}
REPRO_284_TOL = 2e-3
REPRO_293_QGRAD = {0.250: -0.3426, 0.500: -0.3152, 0.750: -0.1462}
REPRO_293_TOL = 2e-3
PRIOR = REPO / "research" / "backtests" / "2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv"

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


# ------------------------------------------------------------------ statistics
def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return np.nan, len(x)
    rx, ry = pd.Series(x).rank().to_numpy(), pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, len(x)
    return float(np.corrcoef(rx, ry)[0, 1]), len(x)


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4 or x.std() == 0 or y.std() == 0:
        return np.nan, len(x)
    return float(np.corrcoef(x, y)[0, 1]), len(x)


def perm_p(x, y, seed=7, nperm=2000):
    rho, n = spearman(x, y)
    if not np.isfinite(rho):
        return np.nan, np.nan, n
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    rx, ry = pd.Series(x[ok]).rank().to_numpy(), pd.Series(y[ok]).rank().to_numpy()
    rx = (rx - rx.mean()) / rx.std()
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(nperm):
        p = rng.permutation(ry)
        r = float(np.dot(rx, (p - p.mean()) / p.std()) / len(rx))
        if abs(r) >= abs(rho) - 1e-12:
            cnt += 1
    return rho, (cnt + 1) / (nperm + 1), n


# ------------------------------------------------------------------ construction (idea 284/293 verbatim)
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
      f"({len(bad)} dropped for max_1d_move >= 1.0), ETF{len(etf36)} ETFs")
    return px56, px136, pxs, etf36, b_stk, s_stk


def build_pool(px56, px136, pxs, etf36, b_stk, s_stk):
    idx = pxs.index.intersection(px136.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), px136.reindex(idx).ffill()
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

    small_pool, large_pool = np.array(sorted(s_stk)), np.array(sorted(b_stk))
    for k in KS:
        for q in QS:
            n_s = int(round(q * k)); n_l = k - n_s
            for sd in range(N_SEEDS):
                seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)   # idea 284's key
                rng = np.random.default_rng(seed)
                sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
                lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
                parts = ([pxb_c[lc]] if lc else []) + ([pxs_c[sc]] if sc else [])
                p = pd.concat(parts + [pxb_c["SPY"].rename("SPY")], axis=1).dropna(how="all").ffill()
                pool[f"k{k:02d}~q{q:.3f}~s{sd:02d}"] = dict(
                    px=p, tradable=set(sc) | set(lc), kind=f"k{k:02d}q{q:.3f}", q=q, k=k, seed=sd)
    return pool


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
        sel = (key.where(elig).rank(axis=1, ascending=False) <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def panel_chars(px, tradable, elig, lo, hi, cols, rbmask):
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
    return dict(k=k, n_elig=float(nel.median()), breadth=breadth, disp=disp, corr=corr, evol=evol)


def stat_block(r, oos_split):
    """idea 293's stat_block, PLUS the two disjoint OOS sub-window Sharpes (new, for C3)."""
    h = len(r) // 2
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
    out["IS_Sharpe"] = metrics(ris)["Sharpe"] if len(ris) > 60 else np.nan
    out["IS_CAGR"] = metrics(ris)["CAGR"] if len(ris) > 60 else np.nan
    mo = metrics(ros) if len(ros) > 60 else dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    out["OOS_CAGR"], out["OOS_Sharpe"], out["OOS_MaxDD"] = mo["CAGR"], mo["Sharpe"], mo["MaxDD"]
    out["OOS_days"] = len(ros)
    ra, rb = ros.loc[:oos_split], ros.loc[oos_split:]
    out["OOS_A_Sharpe"] = metrics(ra)["Sharpe"] if len(ra) > 60 else np.nan
    out["OOS_B_Sharpe"] = metrics(rb)["Sharpe"] if len(rb) > 60 else np.nan
    return out


def keep_flags(row, spy_row, v2_row):
    a = bool(row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"] and row["MaxDD"] >= v2_row["MaxDD"])
    fails = []
    if not row["H1"] > spy_row["H1"]: fails.append("H1")
    if not row["H2"] > spy_row["H2"]: fails.append("H2")
    if not row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]: fails.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(spy_row["MaxDD"]): fails.append("DD")
    if not row["CAGR"] >= 0.70 * spy_row["CAGR"]: fails.append("CAGR")
    return a, (len(fails) == 0), (",".join(fails) if fails else "-")


def lo_se(sharpe, years):
    """Lo (2002) asymptotic SE of an annualised Sharpe ratio under iid returns."""
    if not np.isfinite(sharpe) or years <= 0:
        return np.nan
    return float(np.sqrt((1.0 + 0.5 * sharpe ** 2) / years))


# ------------------------------------------------------------------ main
def main():
    P("=" * 190)
    P("Idea 308 why-does-the-CORR-ordering-die-at-q-0.75 (cloud) | " + Path(__file__).name)
    P("=" * 190)
    P(f"DIALS (2): q {QS} x k {KS}, {N_SEEDS} seeds each = 540 constructed panels; "
      f"books {BOOKS} (+ v2 as the 4a comparand).  ALL 27 (q,k,book) cells reported.")
    P(f"FIXED: weekly, {COST_BPS} bps, next-day execution, gross {GROSS}, IS <= {IS_END}, "
      f"OOS >= {OOS_START}.")
    P("SURVIVORSHIP: current constituents only, on both source panels; small-cap survivorship")
    P("  is the worse of the two and rises WITH q, so levels are inflated along the very dial")
    P("  under test.  The cross-stratum CONTRASTS are the defensible objects here, not levels.")

    px56, px136, pxs, etf36, b_stk, s_stk = build_sources()
    pool = build_pool(px56, px136, pxs, etf36, b_stk, s_stk)
    P(f"pool: {len(pool)} panels ({sum(1 for v in pool.values() if v['kind'] != 'NAMED')} constructed, 5 named)")
    flush_log()

    # OOS split date: the median OOS trading day of the common calendar (fixed, not tuned)
    ref = pool["k20~q0.500~s00"]["px"]
    oos_idx = ref.loc[OOS_START:].index
    OOS_SPLIT = oos_idx[len(oos_idx) // 2]
    P(f"OOS split for the reliability estimate: A = {oos_idx[0].date()}..{OOS_SPLIT.date()}, "
      f"B = {OOS_SPLIT.date()}..{oos_idx[-1].date()} (median OOS trading day, fixed by the calendar)")

    prows, krows = [], []
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
            rec[f"{c}_IS"], rec[f"{c}_OOS"] = cis[c], cos[c]

        start = px.index[260]
        spy_row = stat_block(px["SPY"].pct_change().fillna(0.0).loc[start:], OOS_SPLIT)
        books = {}
        for arm, n in [("EWall", None), ("CAND10", 10), ("CAND20", 20), ("v2", None)]:
            w = book_weights(px, tr, "CAND" if arm.startswith("CAND") else arm, key, elig, n=n)
            r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            books[arm] = stat_block(r, OOS_SPLIT)
        v2_row = books["v2"]
        for arm in BOOKS + ["v2"]:
            b = books[arm]
            for f in ("IS_Sharpe", "IS_CAGR", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_days",
                      "OOS_A_Sharpe", "OOS_B_Sharpe", "Sharpe", "CAGR", "MaxDD", "H1", "H2"):
                rec[f"{arm}_{f}"] = b[f]
            if arm in BOOKS:
                a, b4, fails = keep_flags(b, spy_row, v2_row)
                krows.append(dict(panel=name, kind=meta["kind"], q=meta["q"], k=meta["k"],
                                  seed=meta["seed"], arm=arm, keep4a=a, keep4b=b4, fails4b=fails,
                                  CAGR=b["CAGR"], Sharpe=b["Sharpe"], MaxDD=b["MaxDD"],
                                  H1=b["H1"], H2=b["H2"], OOS_Sharpe=b["OOS_Sharpe"],
                                  OOS_CAGR=b["OOS_CAGR"], OOS_MaxDD=b["OOS_MaxDD"]))
        for f in ("Sharpe", "OOS_Sharpe", "CAGR", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"):
            rec[f"SPY_{f}"] = spy_row[f]
        prows.append(rec)
        if i % 60 == 0 or i == len(pool):
            P(f"  ... {i}/{len(pool)} panels")
            flush_log()

    panels = pd.DataFrame(prows)
    keeps = pd.DataFrame(krows)
    panels.to_csv(f"{OUT}.panels.csv", index=False)
    keeps.to_csv(f"{OUT}.keeppaths.csv", index=False)
    con = panels[panels.kind != "NAMED"].copy()

    # ---------------------------------------------------------------- GATES
    P("\n" + "=" * 190)
    P("GATES")
    prior = pd.read_csv(PRIOR)
    pr = prior[prior.kind != "NAMED"].set_index("panel")
    me = con.set_index("panel")
    common = me.index.intersection(pr.index)
    P(f"  G1 rebuild vs idea 293's committed .panels.csv on {len(common)} constructed panels:")
    g1max = 0.0
    for c in ["corr_IS", "disp_IS", "evol_IS", "breadth_IS"] + [f"{a}_OOS_Sharpe" for a in BOOKS] \
             + [f"{a}_Sharpe" for a in BOOKS]:
        d = float((me.loc[common, c] - pr.loc[common, c]).abs().max())
        g1max = max(g1max, d)
        P(f"       {c:22s} max abs diff {d:.3e}")
    P(f"     G1: max over all columns {g1max:.3e}  ({'PASS' if g1max < 1e-9 else 'FAIL'})")
    assert g1max < 1e-9, g1max

    rep = con[(con.k == 40) & (np.isclose(con.q, 0.500))]
    P(f"  G2 stratum (q=0.500, k=40) vs idea 284's published corr rho_within (n={len(rep)}):")
    g2 = True
    for arm in BOOKS:
        r, _ = spearman(rep["corr_IS"], rep[f"{arm}_OOS_Sharpe"])
        d = abs(r - REPRO_284[arm]); g2 &= d < REPRO_284_TOL
        P(f"       {arm:7s} {r:+.4f}  published {REPRO_284[arm]:+.4f}  |diff| {d:.5f}  "
          f"{'OK' if d < REPRO_284_TOL else 'MISMATCH'}")
    P(f"     G2: {'PASS' if g2 else 'FAIL'}")

    # ---------------------------------------------------------------- the 27 cells
    P("\n" + "=" * 190)
    P("THE 27 CELLS  (Spearman = idea 293's headline statistic; Pearson = the one the")
    P("decomposition identity rho = beta * sd_x / sd_y is exact in.  ALL cells reported.)")
    srows = []
    for k in KS:
        for q in QS:
            d = con[(con.k == k) & (np.isclose(con.q, q))]
            years = float(d[f"EWall_OOS_days"].mean()) / 252.0
            for arm in BOOKS:
                x = d["corr_IS"].to_numpy(float)
                y = d[f"{arm}_OOS_Sharpe"].to_numpy(float)
                rs, p, n = perm_p(x, y)
                rp, _ = pearson(x, y)
                sdx, sdy = float(np.std(x, ddof=1)), float(np.std(y, ddof=1))
                beta = rp * sdy / sdx if sdx > 0 else np.nan
                # seed-half agreement (idea 293's stability check)
                h1 = d[d.seed < N_SEEDS // 2]; h2 = d[d.seed >= N_SEEDS // 2]
                r1, _ = spearman(h1["corr_IS"], h1[f"{arm}_OOS_Sharpe"])
                r2, _ = spearman(h2["corr_IS"], h2[f"{arm}_OOS_Sharpe"])
                # reliability (i) analytic
                se = np.array([lo_se(s, years) for s in y])
                noise_var = float(np.nanmean(se ** 2))
                Ra = 1.0 - noise_var / (sdy ** 2) if sdy > 0 else np.nan
                # reliability (ii) empirical split-half, Spearman-Brown
                a_, b_ = d[f"{arm}_OOS_A_Sharpe"].to_numpy(float), d[f"{arm}_OOS_B_Sharpe"].to_numpy(float)
                rab, _ = pearson(a_, b_)
                Re = 2 * rab / (1 + rab) if np.isfinite(rab) and rab > -1 else np.nan
                srows.append(dict(k=k, q=q, book=arm, n=n, rho_spearman=rs, p=p, rho_pearson=rp,
                                  sd_corrIS=sdx, sd_OOSsharpe=sdy, beta=beta,
                                  mean_OOSsharpe=float(np.nanmean(y)),
                                  seed_h1=r1, seed_h2=r2, halves_agree=bool(np.sign(r1) == np.sign(r2)),
                                  years=years, noise_sd=float(np.sqrt(noise_var)),
                                  R_analytic=Ra, r_AB=rab, R_empirical=Re,
                                  rho_dis_analytic=rs / np.sqrt(Ra) if (Ra and Ra > 0) else np.nan,
                                  rho_dis_empirical=rs / np.sqrt(Re) if (Re and Re > 0) else np.nan))
    st = pd.DataFrame(srows)
    st.to_csv(f"{OUT}.strata.csv", index=False)
    P(fmt(st.set_index(["k", "q", "book"])[["n", "rho_spearman", "p", "rho_pearson", "sd_corrIS",
                                            "sd_OOSsharpe", "beta", "noise_sd", "R_analytic",
                                            "r_AB", "R_empirical", "rho_dis_analytic",
                                            "rho_dis_empirical", "seed_h1", "seed_h2"]]))
    flush_log()

    P("\n  G3 idea 293's published q-gradient of mean rho_spearman:")
    g3 = True
    for q in QS:
        m = float(st[np.isclose(st.q, q)].rho_spearman.mean())
        d = abs(m - REPRO_293_QGRAD[q]); g3 &= d < REPRO_293_TOL
        nsig = int((st[np.isclose(st.q, q)].p < 0.05).sum())
        nagr = int(st[np.isclose(st.q, q)].halves_agree.sum())
        P(f"     q={q:.2f}  mean rho {m:+.4f}  published {REPRO_293_QGRAD[q]:+.4f}  |diff| {d:.5f}  "
          f"{'OK' if d < REPRO_293_TOL else 'MISMATCH'}   sig {nsig}/9   halves agree {nagr}/9")
    P(f"     G3: {'PASS' if g3 else 'FAIL'}")

    # ---------------------------------------------------------------- C1 the two statistics
    P("\n" + "=" * 190)
    P("C1 THE TWO STATISTICS THE QUEUE ASKS FOR, by q (pooled over k and book, 9 cells each)")
    c1 = st.groupby("q").agg(rho=("rho_spearman", "mean"),
                             sd_corrIS=("sd_corrIS", "mean"), sd_OOSsharpe=("sd_OOSsharpe", "mean"),
                             beta=("beta", "mean"), noise_sd=("noise_sd", "mean"),
                             R_analytic=("R_analytic", "mean"), R_empirical=("R_empirical", "mean"),
                             sig=("p", lambda s: int((s < 0.05).sum())))
    P(fmt(c1))
    q0, q2 = QS[0], QS[-1]
    a0, a2 = c1.loc[q0], c1.loc[q2]
    P(f"\n  q {q0:.2f} -> {q2:.2f}:  sd(corr_IS) {a0.sd_corrIS:.4f} -> {a2.sd_corrIS:.4f} "
      f"({a2.sd_corrIS / a0.sd_corrIS:.3f}x)   sd(OOS Sharpe) {a0.sd_OOSsharpe:.4f} -> "
      f"{a2.sd_OOSsharpe:.4f} ({a2.sd_OOSsharpe / a0.sd_OOSsharpe:.3f}x)   |rho| "
      f"{abs(a0.rho):.4f} -> {abs(a2.rho):.4f} ({abs(a2.rho) / abs(a0.rho):.3f}x)")

    # ---------------------------------------------------------------- C2 exact decomposition
    P("\n" + "=" * 190)
    P("C2 THE EXACT DECOMPOSITION.  rho_pearson = beta * sd_x / sd_y, so")
    P("     dlog|rho| = dlog|beta| + dlog sd_x - dlog sd_y     (exact, per (k, book) pair)")
    P("   A NEGATIVE dlog sd_x term = range restriction (cause A).  A NEGATIVE -dlog sd_y term")
    P("   (i.e. sd_y grew) = the outcome-spread channel (cause B's upper bound).  A negative")
    P("   dlog|beta| term = the relationship itself is weaker, which is NEITHER stated cause.")
    drows = []
    for k in KS:
        for arm in BOOKS:
            lo = st[(st.k == k) & (st.book == arm) & (np.isclose(st.q, q0))].iloc[0]
            hi = st[(st.k == k) & (st.book == arm) & (np.isclose(st.q, q2))].iloc[0]
            dl = np.log(abs(hi.rho_pearson)) - np.log(abs(lo.rho_pearson))
            db = np.log(abs(hi.beta)) - np.log(abs(lo.beta))
            dx = np.log(hi.sd_corrIS) - np.log(lo.sd_corrIS)
            dy = -(np.log(hi.sd_OOSsharpe) - np.log(lo.sd_OOSsharpe))
            drows.append(dict(k=k, book=arm, rho_q025=lo.rho_pearson, rho_q075=hi.rho_pearson,
                              dlog_rho=dl, term_beta=db, term_sdx=dx, term_sdy=dy,
                              resid=dl - (db + dx + dy),
                              share_beta=db / dl if dl else np.nan,
                              share_sdx=dx / dl if dl else np.nan,
                              share_sdy=dy / dl if dl else np.nan))
    dec = pd.DataFrame(drows)
    dec.to_csv(f"{OUT}.decomp.csv", index=False)
    P(fmt(dec.set_index(["k", "book"])))
    P(f"\n  identity residual max |dlog_rho - (beta + sdx + sdy terms)| = {dec.resid.abs().max():.2e}")
    P(f"  MEAN SHARE OF THE q=0.25 -> q=0.75 CHANGE IN log|rho|:  beta {dec.share_beta.mean():+.3f}"
      f"   sd_x (range restriction) {dec.share_sdx.mean():+.3f}   sd_y (outcome spread) "
      f"{dec.share_sdy.mean():+.3f}")
    P(f"  sign counts over the 9 (k, book) pairs: dlog|rho| < 0 in {int((dec.dlog_rho < 0).sum())}/9; "
      f"beta term < 0 in {int((dec.term_beta < 0).sum())}/9; sd_x term < 0 in "
      f"{int((dec.term_sdx < 0).sum())}/9; sd_y term < 0 in {int((dec.term_sdy < 0).sum())}/9")

    # ---------------------------------------------------------------- C3 noise or signal
    P("\n" + "=" * 190)
    P("C3 IS THE OUTCOME SPREAD NOISE OR SIGNAL?  Two independent reliability estimates of a")
    P("   panel's OOS Sharpe, and the disattenuated rho each implies.")
    c3 = st.groupby("q").agg(rho=("rho_spearman", "mean"), R_analytic=("R_analytic", "mean"),
                             R_empirical=("R_empirical", "mean"), r_AB=("r_AB", "mean"),
                             dis_a=("rho_dis_analytic", "mean"), dis_e=("rho_dis_empirical", "mean"))
    P(fmt(c3))
    P("   Reading: if the NOISE FLOOR is the cause, R falls with q and the disattenuated rho at")
    P("   q=0.75 returns to the q=0.25 level.  If it does not, the noise floor is not the cause.")
    for q in QS:
        r = c3.loc[q]
        P(f"     q={q:.2f}  raw {r.rho:+.4f}  ->  analytic-disattenuated {r.dis_a:+.4f}   "
          f"empirical-disattenuated {r.dis_e:+.4f}")
    gap_raw = abs(c3.loc[q0].rho) - abs(c3.loc[q2].rho)
    gap_a = abs(c3.loc[q0].dis_a) - abs(c3.loc[q2].dis_a)
    gap_e = abs(c3.loc[q0].dis_e) - abs(c3.loc[q2].dis_e)
    P(f"   |rho| gap q0.25 - q0.75:  raw {gap_raw:+.4f}  after analytic disattenuation {gap_a:+.4f} "
      f"({1 - gap_a / gap_raw if gap_raw else float('nan'):.1%} closed)  after empirical "
      f"{gap_e:+.4f} ({1 - gap_e / gap_raw if gap_raw else float('nan'):.1%} closed)")

    P("\n   RANGE-RESTRICTION CORRECTION (Thorndike case 2) applied instead: rescale each q=0.75")
    P("   cell's rho to the q=0.25 predictor spread, holding beta and the residual variance fixed.")
    rr = []
    for k in KS:
        for arm in BOOKS:
            lo = st[(st.k == k) & (st.book == arm) & (np.isclose(st.q, q0))].iloc[0]
            hi = st[(st.k == k) & (st.book == arm) & (np.isclose(st.q, q2))].iloc[0]
            u = lo.sd_corrIS / hi.sd_corrIS          # spread ratio
            r = hi.rho_pearson
            corrected = u * r / np.sqrt(1 + r ** 2 * (u ** 2 - 1))
            rr.append(dict(k=k, book=arm, u=u, rho_q075=r, rho_q075_rangecorrected=corrected,
                           rho_q025=lo.rho_pearson))
    rrd = pd.DataFrame(rr)
    P(fmt(rrd.set_index(["k", "book"])))
    P(f"   mean |rho| at q=0.75: raw {rrd.rho_q075.abs().mean():.4f} -> range-corrected "
      f"{rrd.rho_q075_rangecorrected.abs().mean():.4f};  q=0.25 target "
      f"{rrd.rho_q025.abs().mean():.4f}")
    flush_log()

    # ---------------------------------------------------------------- C4 rule 8
    P("\n" + "=" * 190)
    P("C4 RULE 8 WALK-FORWARD.  Direction fitted on seeds 0-29 with IS-window statistics ONLY")
    P("   (sign of Spearman between corr_IS and IS Sharpe); applied ONCE to seeds 30-59; that")
    P("   half's OOS is read once.  Selector = pick the 5 panels the fitted direction favours.")
    PICK = 5
    wrows = []
    for k in KS:
        for q in QS:
            d = con[(con.k == k) & (np.isclose(con.q, q))]
            h1, h2 = d[d.seed < N_SEEDS // 2], d[d.seed >= N_SEEDS // 2]
            for arm in BOOKS:
                sgn_r, _ = spearman(h1["corr_IS"], h1[f"{arm}_IS_Sharpe"])   # IS only, first half
                if not np.isfinite(sgn_r) or sgn_r == 0:
                    continue
                asc = sgn_r < 0        # negative direction -> favour LOW corr_IS
                sel = h2.sort_values("corr_IS", ascending=asc).head(PICK)
                anchor = h2                                                  # do-nothing
                wrows.append(dict(k=k, q=q, book=arm, fit_sign=np.sign(sgn_r), fit_rho=sgn_r,
                                  pick_OOS_Sharpe=float(sel[f"{arm}_OOS_Sharpe"].mean()),
                                  anchor_OOS_Sharpe=float(anchor[f"{arm}_OOS_Sharpe"].mean()),
                                  edge_Sharpe=float(sel[f"{arm}_OOS_Sharpe"].mean()
                                                    - anchor[f"{arm}_OOS_Sharpe"].mean()),
                                  pick_OOS_CAGR=float(sel[f"{arm}_OOS_CAGR"].mean()),
                                  anchor_OOS_CAGR=float(anchor[f"{arm}_OOS_CAGR"].mean()),
                                  pick_OOS_MaxDD=float(sel[f"{arm}_OOS_MaxDD"].mean()),
                                  anchor_OOS_MaxDD=float(anchor[f"{arm}_OOS_MaxDD"].mean()),
                                  v2_OOS_Sharpe=float(h2["v2_OOS_Sharpe"].mean()),
                                  v2_OOS_CAGR=float(h2["v2_OOS_CAGR"].mean()),
                                  v2_OOS_MaxDD=float(h2["v2_OOS_MaxDD"].mean()),
                                  spy_OOS_Sharpe=float(h2["SPY_OOS_Sharpe"].mean()),
                                  spy_OOS_CAGR=float(h2["SPY_OOS_CAGR"].mean()),
                                  spy_OOS_MaxDD=float(h2["SPY_OOS_MaxDD"].mean())))
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(wf.set_index(["k", "q", "book"])))
    P("\n  rule-8 edge over the do-nothing anchor, by q (mean over k x book, 9 cells each):")
    for q in QS:
        s = wf[np.isclose(wf.q, q)]
        P(f"    q={q:.2f}  mean edge {s.edge_Sharpe.mean():+.4f} Sharpe, positive in "
          f"{int((s.edge_Sharpe > 0).sum())}/{len(s)} cells | picks OOS CAGR "
          f"{s.pick_OOS_CAGR.mean():.4f} vs anchor {s.anchor_OOS_CAGR.mean():.4f} vs SPY "
          f"{s.spy_OOS_CAGR.mean():.4f} vs RULES v2 {s.v2_OOS_CAGR.mean():.4f} | picks OOS Sharpe "
          f"{s.pick_OOS_Sharpe.mean():.4f} vs SPY {s.spy_OOS_Sharpe.mean():.4f} vs v2 "
          f"{s.v2_OOS_Sharpe.mean():.4f} | picks OOS MaxDD {s.pick_OOS_MaxDD.mean():.4f} vs SPY "
          f"{s.spy_OOS_MaxDD.mean():.4f} vs v2 {s.v2_OOS_MaxDD.mean():.4f}")
    P(f"  fitted direction is NEGATIVE (low corr_IS favoured) in {int((wf.fit_sign < 0).sum())}/{len(wf)} cells")

    # ---------------------------------------------------------------- C5 keep paths
    P("\n" + "=" * 190)
    P("C5 BOTH KEEP PATHS on all 1,620 panel-books (540 panels x 3 books), no selection")
    kp = keeps.groupby(["q", "arm"]).agg(n=("keep4a", "size"), pass4a=("keep4a", "sum"),
                                         pass4b=("keep4b", "sum"))
    kp["both"] = [int(((np.isclose(keeps.q, q)) & (keeps.arm == a) & keeps.keep4a & keeps.keep4b).sum())
                  for q, a in kp.index]
    P(fmt(kp, 0))
    P("\n  4b first-fail reasons by q (the fails4b column is the FULL failing set, not the first):")
    for q in QS:
        s = keeps[np.isclose(keeps.q, q)]
        vc = s.fails4b.value_counts().head(6)
        P(f"    q={q:.2f} n={len(s)} pass4b {int(s.keep4b.sum())} pass4a {int(s.keep4a.sum())} | "
          + "  ".join(f"{kk}:{vv}" for kk, vv in vc.items()))

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 190)
    P("VERDICT (see .result.md)")
    P(f"  decomposition shares over 9 (k, book) pairs: beta {dec.share_beta.mean():+.3f}, "
      f"sd_x {dec.share_sdx.mean():+.3f}, sd_y {dec.share_sdy.mean():+.3f}")
    P(f"  reliability of a panel's OOS Sharpe: analytic {c3.R_analytic.tolist()}, "
      f"empirical {c3.R_empirical.tolist()} (q = 0.25 / 0.50 / 0.75)")
    flush_log()
    return panels, st, dec, wf, keeps


if __name__ == "__main__":
    main()
    flush_log()
