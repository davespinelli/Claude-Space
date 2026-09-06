#!/usr/bin/env python3
"""Idea 284 - "does-any-panel-property-separate-at-FIXED-cap-mix" (lane C, 2026-09-06).

The question
------------
Idea 271 fitted a four-characteristic model of panel behaviour (breadth, dispersion, mean
pairwise correlation, eligible-set vol) over 53 panels.  Idea 276 then showed that on that
corpus `breadth` is a near-deterministic readout of the small-cap share q of a panel
(Spearman -0.9759, R2 linear in q = 0.9546) and that once q is known, breadth adds nothing:
over the mix book cells Spearman(q, OOS Sharpe) = -0.8737 against breadth's +0.8340, i.e.
breadth is a strictly NOISIER proxy for the same one thing.

But idea 276 only established that breadth is collinear with capitalisation ACROSS strata.
It never asked the question that decides whether the other three characteristics are real:

    hold capitalisation FIXED and re-ask.  Inside one q stratum, does ANY of idea 271's four
    characteristics still order out-of-sample Sharpe?

If a characteristic orders OOS Sharpe within a stratum, it is a panel property with its own
content and the record's characteristic language survives.  If every characteristic goes to
zero inside the stratum while the pooled (cross-stratum) correlation stays large, then the
whole four-characteristic model of idea 271 is one capitalisation dummy wearing four names,
and every published claim that explains a result by a panel property is restating the cap
mix.  That is a KILL of the characteristic vocabulary, not just of breadth.

Design
------
STRATA.  k = 40 names per panel throughout, so panel WIDTH is never confounded with
composition.  q = the share of the 40 drawn from SMALL439, the rest from BSTK100 (stock vs
stock, so the axis is capitalisation, not asset class - idea 276's construction, unchanged).

    MAIN STRATUM   q = 0.500 (20 small + 20 large), 60 seeded draws.  This is the "many
                   draws at fixed q" the queue asked for.  Within this stratum q is constant
                   BY CONSTRUCTION, so any surviving characteristic-OOS relation cannot be
                   capitalisation.
    ANCHOR STRATA  q = 0.000 and q = 1.000, 20 seeded draws each, used ONLY to (a) reproduce
                   idea 276's pooled/cross-stratum correlations inside this run and (b) give
                   the pooled-vs-within contrast its numbers.  No verdict rests on them
                   alone.
    NAMED          U56, B136, BSTK100, ETF36, SMALL439 - carried as reproduction rows.

    100 constructed panels + 5 named = 105 panels.  Every panel is reported.
    Seeds are REPLICATION, not tuning: every seed is reported, nothing is selected on seed.

CHARACTERISTICS.  idea 271's four, measured by idea 277's `panel_chars` verbatim (prices and
the RULES v1 gate only, no returns of any book), on the IS window 2009-2016:
    breadth  mean over weekly rebalance days of n_elig / k
    disp     mean over those days of the cross-sectional sd of 63d return among eligibles
    corr     mean off-diagonal pairwise correlation of daily returns
    evol     mean over those days of the mean 20d annualised vol among eligibles
Each is ALSO measured on the OOS window, to report IS->OOS rank stability separately from
predictive content (idea 276 found breadth is a stable measurement of the wrong thing).

BOOKS.  CAND-n, the record's standing construction: RULES v1 gate (px > 200d MA AND
vol20 < 0.60), composite score WITHOUT the vol scaler as the ranking key, top n equal
weighted at 75% gross, weekly, 10 bps, next-day execution.  Plus per panel: EWall (every
eligible name, the un-ranked book idea 271 found carries the whole predictable part),
RULES v1 and RULES v2 (the live book) on the same panel, and SPY.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q  (3 strata: 0.0, 0.5, 1.0 - and the verdict is read INSIDE q = 0.5, where it is fixed)
    2. n  (2 values: 10, 20)
k = 40, the seeds, the gate, 75% gross, weekly cadence, 10 bps and next-day execution are
fixed at the record's published conventions and are NOT tuned.  The four characteristics are
MEASURED, not tuned, and their selector directions are pre-registered below.

Rule 8 walk-forward (required; directions fixed before any OOS number was read)
    IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end read ONCE.
    Within the q = 0.5 stratum, each pre-registered selector picks ONE panel on its IS
    characteristic and that panel's OOS book is read:
        S_BREADTH  highest IS breadth        (idea 271/276 direction: more eligible = better)
        S_DISP     highest IS dispersion     (idea 73's S3 direction)
        S_CORR     LOWEST IS mean pairwise correlation (idea 271's S_CORR direction)
        S_EVOL     LOWEST IS eligible-set vol (less risk in the eligible set = better)
        S_EWALL    highest IS EWall Sharpe   (idea 271's winning predictor, carried as the
                                              benchmark a characteristic must beat)
        S_ISS      highest IS Sharpe of the CAND-n book itself (the classic IS chooser)
    Each selector's REVERSE extreme is reported as a sign check.  The do-nothing anchor is
    the MEAN OOS Sharpe over all 60 panels in the stratum (= drawing a panel at random),
    with its seed sd, so "beats a coin flip" is a stated number, not a claim.  SPY, RULES v2
    and RULES v1 OOS are reported beside it.

Verdicts (both KEEP paths, on every one of the grid points)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
        (RULES v1 carried as a second column for continuity with the pre-2026-09-06 record.)
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens, so every
panel here inherits the bias whole.  It affects the LEVEL of every panel's return.  The
object under test is whether a characteristic ORDERS panels within a fixed cap mix; the
bias is common to all panels in the stratum and so runs against finding nothing (it inflates
between-panel spread in level, which is what a characteristic would have to order).  A
"nothing separates" verdict is therefore the conservative one.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
Outputs: .panels.csv .cells.csv .walkforward.csv .console.txt
"""
import sys
import zlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state, rules_v1_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
BAND_V2 = 0.03
K_MIX = 40
Q_MAIN = 0.500
Q_ANCHOR = [0.000, 1.000]
N_SEEDS_MAIN = 60
N_SEEDS_ANCHOR = 20
NS = [10, 20]
CHARS = ["breadth", "disp", "corr", "evol"]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
N_PERM = 20000

OUT = Path(__file__).with_suffix("")
LOG = []

pd.set_option("display.width", 240)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 4:
        return np.nan, n
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, n
    return float(np.corrcoef(rx, ry)[0, 1]), n


def perm_p(x, y, seed=7):
    """Two-sided permutation p for Spearman under label exchangeability."""
    rho, n = spearman(x, y)
    if not np.isfinite(rho):
        return np.nan, np.nan, n
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    rx = pd.Series(x[ok]).rank().to_numpy()
    ry = pd.Series(y[ok]).rank().to_numpy()
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(N_PERM):
        if abs(float(np.corrcoef(rx, rng.permutation(ry))[0, 1])) >= abs(rho) - 1e-12:
            cnt += 1
    return rho, (cnt + 1) / (N_PERM + 1), n


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
    adj = 1 - (1 - r2) * (n - 1) / max(1, n - p)
    dof = max(1, n - p)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ss_res / dof)), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    return b, t, r2, adj, n


# ------------------------------------------------------------------ panels
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
    P(f"sources: BSTK{len(b_stk)} large-cap stocks, SMALL{len(s_stk)} small-cap stocks, "
      f"ETF{len(etf36)} ETFs, U56 {len([c for c in px56.columns if c != 'SPY'])}")
    return px56, px136, pxs, etf36, b_stk, s_stk


def make_panel(px_small, px_large, small_names, large_names):
    """One k=40 panel on the COMMON calendar, with SPY joined as the benchmark column."""
    parts = []
    if large_names:
        parts.append(px_large[large_names])
    if small_names:
        parts.append(px_small[small_names])
    p = pd.concat(parts, axis=1)
    p = pd.concat([p, px_large["SPY"].rename("SPY")], axis=1)
    return p.dropna(how="all").ffill(), set(small_names) | set(large_names)


def build_pool(px56, px136, pxs, etf36, b_stk, s_stk):
    """5 named panels + the fixed-q strata on one common calendar."""
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
        pool[nm] = dict(px=p, tradable=t, kind="NAMED", q=np.nan, seed=-1, k=len(t))

    small_pool = np.array(sorted(s_stk))
    large_pool = np.array(sorted(b_stk))
    plan = [(Q_MAIN, N_SEEDS_MAIN)] + [(q, N_SEEDS_ANCHOR) for q in Q_ANCHOR]
    for q, nseeds in plan:
        n_s = int(round(q * K_MIX))
        n_l = K_MIX - n_s
        for sd in range(nseeds):
            seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)
            rng = np.random.default_rng(seed)
            sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
            lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
            p, t = make_panel(pxs_c, pxb_c, sc, lc)
            pool[f"q{q:.3f}~s{sd:02d}"] = dict(px=p, tradable=t, kind=f"Q{q:.3f}",
                                               q=q, seed=sd, k=len(t))
    return pool


# ------------------------------------------------------------------ books
def eligible_mask(px, tradable):
    _, above, vol20 = score(px, vol_scale=False)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def book_weights(px, tradable, arm, n=None):
    key, above, vol20 = score(px, vol_scale=False)
    elig = eligible_mask(px, tradable)
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


def stat_block(r, spy):
    """Full / halves / IS / OOS on the post-warm-up window shared by r and spy."""
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


# ------------------------------------------------------------------ characteristics
def panel_chars(px, tradable, elig, lo, hi, tag):
    """idea 271's four characteristics, measured from prices and the gate only."""
    cols = [c for c in px.columns if c in tradable]
    m = rebalance_mask(px.index, FREQ)
    start = px.index[260]
    idx = px.loc[start:].index
    idx = idx[idx >= pd.Timestamp(lo)]
    if hi:
        idx = idx[idx <= pd.Timestamp(hi)]
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


# ------------------------------------------------------------------ main
def main():
    px56, px136, pxs, etf36, b_stk, s_stk = build_sources()
    pool = build_pool(px56, px136, pxs, etf36, b_stk, s_stk)
    P(f"pool: {len(pool)} panels "
      f"({sum(1 for v in pool.values() if v['kind'] == 'NAMED')} named, "
      f"{sum(1 for v in pool.values() if v['kind'] == 'Q0.500')} at q=0.5, "
      f"{sum(1 for v in pool.values() if v['kind'] in ('Q0.000', 'Q1.000'))} anchors)")

    prows, crows = [], []
    for i, (name, meta) in enumerate(pool.items(), 1):
        px, tr = meta["px"], meta["tradable"]
        elig = eligible_mask(px, tr)
        cis = panel_chars(px, tr, elig, IS_START, IS_END, name)
        cos = panel_chars(px, tr, elig, OOS_START, None, name)
        rec = dict(panel=name, kind=meta["kind"], q=meta["q"], seed=meta["seed"], k=meta["k"],
                   n_elig_IS=cis["n_elig"])
        for c in CHARS:
            rec[f"{c}_IS"] = cis[c]
            rec[f"{c}_OOS"] = cos[c]

        spy_r = px["SPY"].pct_change().fillna(0.0)
        start = px.index[260]
        spy_r = spy_r.loc[start:]
        spy_row = stat_block(spy_r, spy_r)

        books = {}
        for arm, n in [("EWall", None), ("CAND10", 10), ("CAND20", 20), ("v1", None), ("v2", None)]:
            w = book_weights(px, tr, "CAND" if arm.startswith("CAND") else arm, n=n)
            r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            books[arm] = stat_block(r, spy_r)
        v2_row = books["v2"]

        for arm in ("EWall", "CAND10", "CAND20", "v1", "v2"):
            b = books[arm]
            a, bkeep, fails = keep_flags(b, spy_row, v2_row)
            crows.append(dict(panel=name, kind=meta["kind"], q=meta["q"], seed=meta["seed"],
                              arm=arm, **{k: b[k] for k in
                                          ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                           "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                              keep4a=a, keep4b=bkeep, fails4b=fails,
                              spy_Sharpe=spy_row["Sharpe"], spy_OOS_Sharpe=spy_row["OOS_Sharpe"],
                              spy_CAGR=spy_row["CAGR"], spy_MaxDD=spy_row["MaxDD"]))
        for arm in ("EWall", "CAND10", "CAND20", "v1", "v2"):
            for f in ("IS_Sharpe", "OOS_Sharpe", "Sharpe", "CAGR", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"):
                rec[f"{arm}_{f}"] = books[arm][f]
        for f in ("Sharpe", "OOS_Sharpe", "CAGR", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"):
            rec[f"SPY_{f}"] = spy_row[f]
        prows.append(rec)
        if i % 10 == 0 or i == len(pool):
            P(f"  ... {i}/{len(pool)} panels")

    panels = pd.DataFrame(prows)
    cells = pd.DataFrame(crows)
    panels.to_csv(f"{OUT}.panels.csv", index=False)
    cells.to_csv(f"{OUT}.cells.csv", index=False)

    named = panels[panels.kind == "NAMED"].set_index("panel")
    P("\n=== REPRODUCTION: named panels, idea 271 characteristics (IS 2009-2016) ===")
    P(fmt(named[["k", "n_elig_IS"] + [f"{c}_IS" for c in CHARS] +
                ["CAND20_Sharpe", "CAND20_OOS_Sharpe", "EWall_OOS_Sharpe"]]))

    main_s = panels[panels.kind == f"Q{Q_MAIN:.3f}"].copy()
    a0 = panels[panels.kind == "Q0.000"].copy()
    a1 = panels[panels.kind == "Q1.000"].copy()
    P(f"\n=== STRATUM SUMMARY (k={K_MIX}) ===")
    summ = []
    for tag, d in [("q=0.0 (all large)", a0), ("q=0.5 (20+20)", main_s), ("q=1.0 (all small)", a1)]:
        row = dict(stratum=tag, n=len(d))
        for c in CHARS:
            row[f"{c}_mean"] = d[f"{c}_IS"].mean()
            row[f"{c}_sd"] = d[f"{c}_IS"].std()
        for arm in ("CAND10", "CAND20", "EWall"):
            row[f"{arm}_OOS_mean"] = d[f"{arm}_OOS_Sharpe"].mean()
            row[f"{arm}_OOS_sd"] = d[f"{arm}_OOS_Sharpe"].std()
        summ.append(row)
    P(fmt(pd.DataFrame(summ).set_index("stratum")))

    # ---------- Q1: within-stratum ordering vs pooled ordering
    P("\n=== Q1: does any characteristic order OOS Sharpe INSIDE the fixed-q stratum? ===")
    P(f"Spearman(characteristic measured IS, OOS Sharpe), exact-style permutation p "
      f"({N_PERM} permutations).")
    pooled = pd.concat([a0, main_s, a1])
    qrows = []
    for arm in ("CAND10", "CAND20", "EWall"):
        for c in CHARS:
            r_in, p_in, n_in = perm_p(main_s[f"{c}_IS"], main_s[f"{arm}_OOS_Sharpe"])
            r_po, p_po, n_po = perm_p(pooled[f"{c}_IS"], pooled[f"{arm}_OOS_Sharpe"])
            r_is, _ = spearman(main_s[f"{c}_IS"], main_s[f"{arm}_IS_Sharpe"])
            r_st, _ = spearman(main_s[f"{c}_IS"], main_s[f"{c}_OOS"])
            qrows.append(dict(book=arm, char=c, rho_within=r_in, p_within=p_in, n_within=n_in,
                              rho_pooled=r_po, p_pooled=p_po, n_pooled=n_po,
                              rho_within_IS=r_is, IS_OOS_stability=r_st))
    q1 = pd.DataFrame(qrows)
    P(fmt(q1.set_index(["book", "char"])))

    P("\nControl predictors on the SAME within-stratum points (not queue characteristics):")
    ctrl = []
    for arm in ("CAND10", "CAND20"):
        for lbl, series in [("EWall_IS_Sharpe", main_s["EWall_IS_Sharpe"]),
                            ("own_IS_Sharpe", main_s[f"{arm}_IS_Sharpe"]),
                            ("n_elig_IS", main_s["n_elig_IS"])]:
            r, p, n = perm_p(series, main_s[f"{arm}_OOS_Sharpe"])
            ctrl.append(dict(book=arm, predictor=lbl, rho_within=r, p_within=p, n=n))
    P(fmt(pd.DataFrame(ctrl).set_index(["book", "predictor"])))

    P("\nJoint fit inside the stratum: OOS Sharpe ~ 1 + the four IS characteristics (z-scored)")
    for arm in ("CAND10", "CAND20", "EWall"):
        d = main_s.dropna(subset=[f"{arm}_OOS_Sharpe"])
        Z = np.column_stack([np.ones(len(d))] +
                            [((d[f"{c}_IS"] - d[f"{c}_IS"].mean()) / d[f"{c}_IS"].std()).to_numpy()
                             for c in CHARS])
        b, t, r2, adj, n = ols(d[f"{arm}_OOS_Sharpe"], Z)
        P(f"  {arm}: n={n}  R2={r2:.4f}  adjR2={adj:.4f}   " +
          "  ".join(f"{c} b={bb:+.4f} t={tt:+.2f}" for c, bb, tt in zip(["const"] + CHARS, b, t)))

    # ---------- Q2: rule 8 walk-forward inside the stratum
    P("\n=== Rule 8 WALK-FORWARD inside q=0.5 (selectors + directions pre-registered) ===")
    SEL = {
        "S_BREADTH": ("breadth_IS", "max", "highest IS breadth"),
        "S_DISP":    ("disp_IS", "max", "highest IS dispersion"),
        "S_CORR":    ("corr_IS", "min", "LOWEST IS mean pairwise correlation"),
        "S_EVOL":    ("evol_IS", "min", "LOWEST IS eligible-set vol"),
        "S_EWALL":   ("EWall_IS_Sharpe", "max", "highest IS EWall Sharpe (idea 271's winner)"),
    }
    wf = []
    for arm in ("CAND10", "CAND20"):
        d = main_s.dropna(subset=[f"{arm}_OOS_Sharpe"]).copy()
        anchor = d[f"{arm}_OOS_Sharpe"].mean()
        anchor_sd = d[f"{arm}_OOS_Sharpe"].std()
        best = d[f"{arm}_OOS_Sharpe"].max()
        spy_oos = d["SPY_OOS_Sharpe"].mean()
        v2_oos = d["v2_OOS_Sharpe"].mean()
        v1_oos = d["v1_OOS_Sharpe"].mean()
        sels = dict(SEL)
        sels["S_ISS"] = (f"{arm}_IS_Sharpe", "max", "highest IS Sharpe of the book itself")
        for nm, (col, direction, desc) in sels.items():
            for lbl, dr in ((nm, direction), (nm + "^rev", "min" if direction == "max" else "max")):
                pick = d.loc[d[col].idxmax() if dr == "max" else d[col].idxmin()]
                _, kb, fails = keep_flags(
                    {k: pick[f"{arm}_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                    {k: pick[f"SPY_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                    {k: pick[f"v2_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")})
                wf.append(dict(book=arm, rule=lbl, prereg=desc if lbl == nm else "sign check",
                               pick=pick["panel"], IS_Sharpe=pick[f"{arm}_IS_Sharpe"],
                               OOS_CAGR=pick[f"{arm}_OOS_CAGR"],
                               OOS_Sharpe=pick[f"{arm}_OOS_Sharpe"],
                               OOS_MaxDD=pick[f"{arm}_OOS_MaxDD"],
                               vs_anchor=pick[f"{arm}_OOS_Sharpe"] - anchor,
                               vs_SPY=pick[f"{arm}_OOS_Sharpe"] - spy_oos,
                               vs_v2=pick[f"{arm}_OOS_Sharpe"] - v2_oos,
                               regret=best - pick[f"{arm}_OOS_Sharpe"],
                               keep4b=kb, fails4b=fails))
        wf.append(dict(book=arm, rule="ANCHOR (do nothing: mean of 60 draws)", prereg="control",
                       pick="-", IS_Sharpe=d[f"{arm}_IS_Sharpe"].mean(),
                       OOS_CAGR=d[f"{arm}_OOS_CAGR"].mean(), OOS_Sharpe=anchor,
                       OOS_MaxDD=d[f"{arm}_OOS_MaxDD"].mean(), vs_anchor=0.0,
                       vs_SPY=anchor - spy_oos, vs_v2=anchor - v2_oos, regret=best - anchor,
                       keep4b=False, fails4b="n/a (mean)"))
        P(f"\n[{arm}]  anchor OOS Sharpe {anchor:.4f} (seed sd {anchor_sd:.4f}, best {best:.4f});"
          f"  SPY OOS {spy_oos:.4f}   RULES v2 OOS {v2_oos:.4f}   RULES v1 OOS {v1_oos:.4f}")
    wfdf = pd.DataFrame(wf)
    wfdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n" + fmt(wfdf.set_index(["book", "rule"]).drop(columns=["prereg"])))

    P("\nSelector edge over the anchor, pre-registered directions only (a characteristic "
      "'separates' only if this is positive AND the sign check is ordinally right):")
    prime = wfdf[~wfdf.rule.str.endswith("^rev") & ~wfdf.rule.str.startswith("ANCHOR")]
    P(fmt(prime.pivot_table(index="rule", columns="book", values="vs_anchor")))

    # ---------- KEEP paths over every cell
    P("\n=== KEEP PATHS over every grid cell (all reported) ===")
    kp = cells.groupby(["kind", "arm"]).agg(n=("keep4a", "size"), keep4a=("keep4a", "sum"),
                                            keep4b=("keep4b", "sum"),
                                            OOS_Sharpe=("OOS_Sharpe", "mean"),
                                            Sharpe=("Sharpe", "mean"),
                                            CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"))
    P(fmt(kp))
    passes = cells[cells.keep4b]
    P(f"\n4b passes: {len(passes)} of {len(cells)} cells.")
    if len(passes):
        P(fmt(passes.sort_values("OOS_Sharpe", ascending=False)
              [["panel", "kind", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "keep4a"]]
              .head(40).set_index(["panel", "arm"])))
        st = passes[passes.kind == f"Q{Q_MAIN:.3f}"]
        P(f"\n4b passes inside q=0.5: {len(st)} of "
          f"{len(cells[cells.kind == f'Q{Q_MAIN:.3f}'])} cells in the stratum.")
        if len(st):
            P("Are the passing stratum panels distinguished by any characteristic?  "
              "(mean of passers vs non-passers, per book)")
            for arm in ("CAND10", "CAND20"):
                sa = st[st.arm == arm]
                if not len(sa):
                    continue
                names = set(sa.panel)
                d = main_s.copy()
                d["pass"] = d.panel.isin(names)
                P(f"  [{arm}] {len(names)} passers / {len(d)}")
                P(fmt(d.groupby("pass")[[f"{c}_IS" for c in CHARS] +
                                        [f"{arm}_OOS_Sharpe"]].mean()))
    P(f"\n4a passes: {int(cells.keep4a.sum())} of {len(cells)} cells "
      f"(RULES v2 is the comparand; the v2 rows themselves are excluded from any claim).")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {OUT.name}.panels.csv .cells.csv .walkforward.csv .console.txt")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
