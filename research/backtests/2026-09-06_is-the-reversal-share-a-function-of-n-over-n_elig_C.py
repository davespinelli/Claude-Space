#!/usr/bin/env python3
"""Idea 269 - "is-the-reversal-share-a-function-of-n-over-n_elig" (lane C, 2026-09-06).

The question
------------
Idea 259 established that the EWall-vs-ranked Sharpe/CAGR reversal is GENERAL: 33.7% of
37,044 RANKED census pairs reverse, and conditional on EWall winning on Sharpe it loses
on CAGR 47.5% of the time.  Its fresh grid also showed the reversal DYING as the ranked
book's n approaches the eligible count (B136 6/6 reverse at n=5..60, U56 only 2/6).  The
queue asks whether reversal share is a MONOTONE function of the concentration ratio

        r = n / n_elig          (names held by the ranked book / names the gate admits)

If it is, a reversal can be predicted from the book's WIDTH alone - a number every
published grid already carries - instead of from a re-run.

Design (three legs)
-------------------
A. CENSUS re-read.  Idea 259's committed `.census.csv.gz` (44,358 pairs, 37,044 RANKED)
   is read verbatim - not rebuilt - so the corpus is exactly the one the record
   published.  Two columns are back-filled onto it:
       n       parsed STRICTLY from the comparand's label (TOP20/CAND20/FWD40/RANKED20/
               V1C20/STK20 -> the digits; a bare V1/V1u/V1C/v1 -> 5, the live rules' n).
               Labels with no unambiguous n (bare FWD/CAND/RANKED/REV, frac085, band
               arms) are DROPPED and counted, never guessed.
       n_elig  the panel's median eligible-name count on weekly rebalance days, computed
               FRESH here under the canonical gate (above-200d AND vol20 < 0.60), for the
               five panels the record names.  Cells whose panel cannot be mapped are
               dropped and counted.
   Monotonicity is then tested pair-level (Spearman), point-level (distinct (panel,n)
   ratio points), file-clustered (one r and one share per file, so 84 files cannot be
   outvoted by one 21k-pair file), and WITHIN PANEL - because in the census r varies
   mostly BETWEEN panels, panel is the obvious confound and is reported as such.

B. MATCHED-RATIO GRID (the census cannot settle it, so the ratio is set directly).
   Idea 259's leg-B construction imported verbatim (weekly, next-day, 10 bps, gate =
   above-200d AND vol20 < 0.60, ranking key = composite WITHOUT the vol scaler, every
   arm gross-matched at 0.75):
       EWall   every eligible name, equal weight        (the un-ranked book)
       FWD-n   top-n by the composite key               (the ranked book)
   but n is now chosen PER PANEL so that r hits the same pre-registered targets on all
   five panels: r* in {0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00}, n = round(r* * n_elig).
   That breaks the panel/ratio confound: if reversal share is a function of r alone,
   matched-r cells agree ACROSS panels and the share falls monotonically in r.
   0 bps is carried as a DIAGNOSTIC column only (idea 260's channel), never selected on.

C. Does the ratio beat the alternatives?  The same cells are also scored by n alone and
   by panel alone, so "a function of r" is compared against "a function of width" and
   "a function of the panel you happened to run".

Tuned parameters (PROTOCOL rule 4: at most two) - leg B only
    1. panel (5)      2. target ratio r* (7)
The arm axis (EWall vs FWD) is the hypothesis, not a dial; the cost rung is fixed at
PROTOCOL's 10 bps.  Leg A tunes nothing - it reads a committed file.  The reversal
epsilons are idea 259's, unchanged (|dSharpe| > 0.005 AND |dCAGR| > 5 bps/yr), and eps=0
is reported beside them.  ALL grid points are written to the .csv outputs.

Walk-forward (PROTOCOL rule 8), pre-registered with direction before any OOS read
    IS = 2009-01-01..2016-12-31 chooses; OOS = 2017-01-01..end read ONCE.
    (i) THE RELATIONSHIP.  Reversal is recomputed from IS-window metrics only; the
        threshold r* that best separates reversing from non-reversing cells IS is picked
        on the IS window, then applied ONCE to OOS-window reversals.  Accuracy is
        reported against the OOS majority-class base rate.  A width rule that only
        classifies in-sample is not a rule.
    (ii) THE BOOK.  EWALL (do nothing) / FWD20 (incumbent) / S_SHARPE (argmax IS Sharpe)
        / S_CAGR (argmax IS CAGR) / RSEL (the width rule: the narrowest n whose r >= the
        IS-fitted threshold, i.e. the first book the rule calls reversal-safe), pooled
        equal-weight over panels, OOS CAGR/Sharpe/MaxDD against RULES v1 and SPY.

Verdicts (both KEEP paths, on every leg-B point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json, the megacap cut and the small panel are CURRENT
constituents.  The un-ranked book holds everything and so inherits the full survivorship
premium, while any selection rule can only redistribute it - the bias runs TOWARD the
pro-EWall side of every comparison counted here, i.e. toward MORE reversals at low r.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import re
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
DIAG_BPS = 0
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
RATIOS = [0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
EPS_S, EPS_C = 0.005, 0.0005            # idea 259's, unchanged
BINS = [0.0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.01]   # pre-registered, = the targets
PARENT = "2026-09-06_does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim_C.census.csv.gz"

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(x, y):
    """Spearman rho and its large-sample t, on the finite pairs only."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 4:
        return np.nan, np.nan, n
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return np.nan, np.nan, n
    rho = float(np.corrcoef(rx, ry)[0, 1])
    t = rho * np.sqrt((n - 2) / max(1e-12, 1 - rho ** 2))
    return rho, t, n


# ============================================================ panels (idea 259 verbatim)
def build_panels():
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

    return {
        "U56": sub(px56, [c for c in px56.columns]),
        "B136": sub(px136, [c for c in px136.columns]),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL439": sub(pxs, s_stk, tradable=s_stk),
        "ETF36": sub(px136, etf36, tradable=etf36),
    }


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, arm, n=None):
    elig = eligible_mask(px, tradable)
    if arm == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        key = score(px, vol_scale=False)[0]
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


def elig_counts(panels):
    """Median eligible names on weekly rebalance days, full / IS / OOS, per panel."""
    rows = {}
    for pname, (px, tr) in panels.items():
        elig = eligible_mask(px, tr)
        m = rebalance_mask(px.index, FREQ)
        nel = elig[m.values].sum(axis=1)
        start = px.index[260]
        nel = nel.loc[start:]
        rows[pname] = dict(
            n_elig=float(nel.median()),
            n_elig_is=float(nel.loc[IS_START:IS_END].median()),
            n_elig_oos=float(nel.loc[OOS_START:].median()),
            n_elig_p10=float(nel.quantile(0.10)),
            n_elig_p90=float(nel.quantile(0.90)),
            n_cols=int(len(tr)),
        )
    return pd.DataFrame(rows).T


# ==================================================================== LEG A: census re-read
FAM = re.compile(r"^(top|cand|fwd|fwdvs|ranked|v1c|stk|n)[-_ ]?(\d+)", re.I)
V1BARE = re.compile(r"^v1[a-z]*$", re.I)
PMAP = {
    "u56": "U56", "U56": "U56", "universe.json": "U56", "universe.json(56)": "U56",
    "broad": "B136", "broad136": "B136", "B136": "B136", "universe_broad.json": "B136",
    "small": "SMALL439", "SMALL": "SMALL439", "SMALL439": "SMALL439", "SMALL484": "SMALL439",
    "BSTK100": "BSTK100", "ETF36": "ETF36",
}


def parse_n(a):
    a = str(a).strip()
    m = FAM.match(a)
    if m:
        return float(m.group(2))
    if V1BARE.match(a):
        return 5.0                      # the live rules hold 5 names
    return np.nan


def leg_a(nel):
    src = OUT / PARENT
    cen = pd.read_csv(src)
    r = cen[cen.cmp_class == "RANKED"].copy()
    n_ranked = len(r)
    r["n"] = r.cmp_arm.map(parse_n)
    fk = r["keys"].astype(str).str.split("|").str[0]
    pan = r["cell"].astype(str).str.split("|").str[0].where(fk.isin(["panel", "uni", "universe"]))
    r["panel"] = pan.map(PMAP)
    r["n_elig"] = r.panel.map(nel["n_elig"])
    r["ratio"] = r.n / r.n_elig
    keep = r.n.notna() & r.panel.notna()
    P(f"LEG A: parent census {len(cen):,} pairs, RANKED {n_ranked:,}.")
    P(f"  n parsed on {int(r.n.notna().sum()):,}  ({r.n.notna().mean():.1%}); "
      f"panel mapped on {int(r.panel.notna().sum()):,}  ({r.panel.notna().mean():.1%}); "
      f"BOTH {int(keep.sum()):,}  ({keep.mean():.1%}) over {r.loc[keep,'file'].nunique()} files.")
    drops = pd.concat([
        r.loc[~r.n.notna(), "cmp_arm"].value_counts().rename("dropped_no_n"),
    ], axis=1)
    P("  dropped comparand labels (no unambiguous n):")
    P(fmt(drops, 0))
    unmapped = r.loc[r.panel.isna(), "cell"].astype(str).str.split("|").str[0].value_counts().head(10)
    P("  dropped panels (unmappable): " + ", ".join(f"{k}={v}" for k, v in unmapped.items()))
    a = r[keep].copy()
    a["rbin"] = pd.cut(a.ratio.clip(upper=1.0), BINS, right=True, include_lowest=True)
    return a


def leg_a_tests(a):
    P("")
    P("LEG A.1 - reversal share by pre-registered ratio bin (pair-level):")
    g = a.groupby("rbin", observed=True).agg(
        pairs=("rev", "size"), rev=("rev", "mean"), rev_eps0=("rev_eps0", "mean"),
        rev_oos=("rev_oos", "mean"), files=("file", "nunique"),
        r_mid=("ratio", "median"), panels=("panel", "nunique"))
    P(fmt(g, 4))
    rho, t, n = spearman(a.ratio, a.rev.astype(float))
    P(f"  pair-level Spearman(rev, r) = {rho:+.4f}  t {t:+.2f}  n {n:,}")

    P("")
    P("LEG A.2 - distinct (panel, n) ratio POINTS (one row per published width, unweighted):")
    pt = a.groupby(["panel", "n"], observed=True).agg(
        pairs=("rev", "size"), files=("file", "nunique"), n_elig=("n_elig", "first"),
        ratio=("ratio", "first"), rev=("rev", "mean")).reset_index().sort_values("ratio")
    P(fmt(pt, 4))
    rho, t, n = spearman(pt.ratio, pt.rev)
    P(f"  point-level Spearman = {rho:+.4f}  t {t:+.2f}  n {n}")

    P("")
    P("LEG A.3 - file-clustered (one r, one share per file; a 21k-pair file gets one vote):")
    fc = a.groupby("file").agg(pairs=("rev", "size"), ratio=("ratio", "median"),
                               rev=("rev", "mean"), panels=("panel", "nunique"))
    rho, t, n = spearman(fc.ratio, fc.rev)
    P(f"  file-level Spearman = {rho:+.4f}  t {t:+.2f}  n {n} files")
    fcb = fc.assign(rbin=pd.cut(fc.ratio.clip(upper=1.0), BINS, right=True, include_lowest=True))
    P(fmt(fcb.groupby("rbin", observed=True).agg(files=("rev", "size"), rev=("rev", "mean")), 4))

    P("")
    P("LEG A.4 - WITHIN PANEL (the census's r varies mostly BETWEEN panels - the confound):")
    rows = []
    for pn, d in a.groupby("panel"):
        rho, t, n = spearman(d.ratio, d.rev.astype(float))
        rows.append(dict(panel=pn, pairs=len(d), widths=d.n.nunique(),
                         r_min=d.ratio.min(), r_max=d.ratio.max(), rev=d.rev.mean(),
                         rho=rho, t=t))
    wp = pd.DataFrame(rows).sort_values("panel")
    P(fmt(wp, 4))
    P("  between-panel share (panel means, unweighted by pairs):")
    pm = a.groupby("panel").agg(pairs=("rev", "size"), n_elig=("n_elig", "first"),
                                r=("ratio", "median"), rev=("rev", "mean"))
    P(fmt(pm, 4))
    return pt, fc, wp, pm


# ==================================================================== LEG B: matched-ratio grid
def run_leg_b(panels, nel):
    rows, cache = [], {}
    for pname, (px, tr) in panels.items():
        ne = float(nel.loc[pname, "n_elig"])
        elig = eligible_mask(px, tr)
        m = rebalance_mask(px.index, FREQ)
        nel_ser = elig[m.values].sum(axis=1)
        spy = px["SPY"].pct_change().fillna(0)
        ns = []
        for rt in RATIOS:
            n = int(max(1, round(rt * ne)))
            ns.append((rt, n))
        arms = [("EWall", None, np.nan), ("v1", None, np.nan)] + [("FWD", n, rt) for rt, n in ns]
        for arm, n, rt in arms:
            w = weights(px, tr, arm, n)
            for bps in (COST_BPS, DIAG_BPS):
                res = backtest(px, w, cost_bps=bps, freq=FREQ)
                start = px.index[260]
                r = res["returns"].loc[start:]
                sp = spy.loc[start:]
                r_is, r_oos = r.loc[IS_START:IS_END], r.loc[OOS_START:]
                sp_is, sp_oos = sp.loc[IS_START:IS_END], sp.loc[OOS_START:]
                mm, mo, mi = metrics(r), metrics(r_oos), metrics(r_is)
                h1, h2 = half_sharpes(r)
                ns_ = nel_ser.loc[start:]
                sat = float((ns_ <= (n if n else 0)).mean()) if n else 0.0
                cache[(pname, arm, n, bps)] = dict(r=r, sp=sp, r_is=r_is, r_oos=r_oos,
                                                   sp_is=sp_is, sp_oos=sp_oos)
                rows.append(dict(
                    panel=pname, arm=arm, n=(n if n else np.nan), r_target=rt, bps=bps,
                    n_elig=ne, r_real=(n / ne if n else np.nan),
                    CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                    H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_Vol=mi["Vol"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    OOS_Vol=mo["Vol"],
                    turn=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
                    gross=float(w.loc[start:].sum(axis=1).mean()),
                    sat_share=sat,
                    SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                    SPY_MaxDD=metrics(sp)["MaxDD"],
                    SPY_OOS_Sharpe=metrics(sp_oos)["Sharpe"],
                ))
        for bps in (COST_BPS, DIAG_BPS):
            b = cache[(pname, "v1", None, bps)]
            for arm, n, rt in arms:
                c = cache[(pname, arm, n, bps)]
                for i, rr in enumerate(rows):
                    same_n = (np.isnan(rr["n"]) if n is None else rr["n"] == n)
                    if rr["panel"] == pname and rr["arm"] == arm and same_n and rr["bps"] == bps:
                        rows[i]["p4a"] = v4a(c["r"], b["r"])
                        rows[i]["f4b"] = fail4b(c["r"], c["sp"], c["r_oos"], c["sp_oos"])
                        rows[i]["p4b"] = (rows[i]["f4b"] == "-")
    return pd.DataFrame(rows), cache


def reversal_table(grid, bps, window=""):
    """EWall - FWD per (panel, r_target) at one cost rung; window in {'', 'IS_', 'OOS_'}."""
    S, C = f"{window}Sharpe", f"{window}CAGR"
    g = grid[grid.bps == bps]
    out = []
    for pname, d in g.groupby("panel"):
        ew = d[d.arm == "EWall"].iloc[0]
        for _, f in d[d.arm == "FWD"].sort_values("r_target").iterrows():
            dS, dC = ew[S] - f[S], ew[C] - f[C]
            out.append(dict(
                panel=pname, r_target=f.r_target, n=int(f.n), n_elig=f.n_elig,
                r_real=f.r_real, sat_share=f.sat_share,
                S_ew=ew[S], S_fwd=f[S], C_ew=ew[C], C_fwd=f[C], dS=dS, dC=dC,
                rev=bool((np.sign(dS) != np.sign(dC)) and abs(dS) > EPS_S and abs(dC) > EPS_C),
                rev_eps0=bool((np.sign(dS) != np.sign(dC)) and dS != 0 and dC != 0),
                ew_wins_S=bool(dS > EPS_S), ew_wins_C=bool(dC > EPS_C),
                turn_fwd=f.turn, turn_ew=ew.turn))
    return pd.DataFrame(out)


# ==================================================================== rule 8
def rule8_relationship(grid):
    """IS-window reversal fits ONE threshold r*; OOS-window reversal is read once."""
    tis = reversal_table(grid, COST_BPS, "IS_")
    toos = reversal_table(grid, COST_BPS, "OOS_")
    key = ["panel", "r_target"]
    m = tis[key + ["r_real", "rev"]].rename(columns={"rev": "rev_is"}).merge(
        toos[key + ["rev"]].rename(columns={"rev": "rev_oos"}), on=key)
    cands = sorted(set(np.round(np.arange(0.05, 1.01, 0.05), 2)))
    best, best_acc = None, -1.0
    grid_rows = []
    for th in cands:
        pred = m.r_real < th                     # narrow books reverse, wide ones do not
        acc = float((pred == m.rev_is).mean())
        grid_rows.append(dict(threshold=th, IS_accuracy=acc,
                              OOS_accuracy=float((pred == m.rev_oos).mean())))
        if acc > best_acc:
            best_acc, best = acc, th
    gr = pd.DataFrame(grid_rows)
    pred = m.r_real < best
    oos_acc = float((pred == m.rev_oos).mean())
    base = float(max(m.rev_oos.mean(), 1 - m.rev_oos.mean()))
    # RIVAL classifiers, all fitted on the IS window only and read ONCE out of sample
    m = m.copy()
    m["pred_r"] = pred
    maj_is = bool(m.rev_is.mean() > 0.5)
    m["pred_const"] = maj_is
    pan_maj = m.groupby("panel").rev_is.mean() > 0.5
    m["pred_panel"] = m.panel.map(pan_maj)
    rivals = pd.DataFrame([
        dict(classifier=f"CONST (IS majority = {maj_is})",
             IS_acc=float((m.pred_const == m.rev_is).mean()),
             OOS_acc=float((m.pred_const == m.rev_oos).mean())),
        dict(classifier=f"R_THRESH (r < {best:.2f})", IS_acc=best_acc, OOS_acc=oos_acc),
        dict(classifier="PANEL (per-panel IS majority)",
             IS_acc=float((m.pred_panel == m.rev_is).mean()),
             OOS_acc=float((m.pred_panel == m.rev_oos).mean())),
    ])
    return m, gr, best, best_acc, oos_acc, base, rivals


def rule8_book(grid, cache, r_star):
    g10 = grid[grid.bps == COST_BPS]
    panels = sorted(g10.panel.unique())
    sels = {}
    for pname in panels:
        d = g10[(g10.panel == pname) & (g10.arm == "FWD")].sort_values("r_target")
        ew = g10[(g10.panel == pname) & (g10.arm == "EWall")].iloc[0]
        s_sharpe = d.loc[d.IS_Sharpe.idxmax()]
        s_cagr = d.loc[d.IS_CAGR.idxmax()]
        safe = d[d.r_real >= r_star]
        rsel = (safe.iloc[0] if len(safe) else d.iloc[-1])
        fwd20 = d.iloc[(d.n - 20).abs().argmin()]
        sels[pname] = dict(EWALL=("EWall", None), FWD20=("FWD", int(fwd20.n)),
                           S_SHARPE=("FWD", int(s_sharpe.n)), S_CAGR=("FWD", int(s_cagr.n)),
                           RSEL=("FWD", int(rsel.n)))
    rows = []
    for sel in ["EWALL", "FWD20", "S_SHARPE", "S_CAGR", "RSEL"]:
        rs, picks = [], []
        for pname in panels:
            arm, n = sels[pname][sel]
            c = cache[(pname, arm, n, COST_BPS)]
            rs.append(c["r_oos"])
            picks.append(f"{pname}:{arm}{'' if n is None else n}")
        pooled = pd.concat(rs, axis=1).mean(axis=1).dropna()
        m = metrics(pooled)
        rows.append(dict(selector=sel, picks=" ".join(picks), OOS_CAGR=m["CAGR"],
                         OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    # baselines pooled the same way
    for nm, arm in [("RULES v1", "v1")]:
        rs = [cache[(p, arm, None, COST_BPS)]["r_oos"] for p in panels]
        pooled = pd.concat(rs, axis=1).mean(axis=1).dropna()
        m = metrics(pooled)
        rows.append(dict(selector=nm, picks="v1 x" + str(len(panels)), OOS_CAGR=m["CAGR"],
                         OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    sp = cache[(panels[0], "EWall", None, COST_BPS)]["sp_oos"]
    m = metrics(sp)
    rows.append(dict(selector="SPY", picks="-", OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                     OOS_MaxDD=m["MaxDD"]))
    return pd.DataFrame(rows), sels


# ==================================================================== main
def main():
    P("=" * 110)
    P("Idea 269 - is-the-reversal-share-a-function-of-n-over-n_elig  (lane C, 2026-09-06)")
    P(f"10 bps headline, 0 bps diagnostic; weekly; next-day execution; gross {GROSS}; "
      f"gate above-200d AND vol20 < {MAX_VOL}")
    P("=" * 110)

    panels = build_panels()
    nel = elig_counts(panels)
    P("")
    P("Panel eligible-name counts (median on weekly rebalance days, canonical gate):")
    P(fmt(nel, 1))
    nel.to_csv(OUT / f"{STEM}.elig.csv")

    a = leg_a(nel)
    pt, fc, wp, pm = leg_a_tests(a)
    a.to_csv(OUT / f"{STEM}.census_backfill.csv.gz", index=False, compression="gzip")
    pt.to_csv(OUT / f"{STEM}.points.csv", index=False)

    P("")
    P("=" * 110)
    P("LEG B - matched-ratio grid (n chosen per panel so r hits the same targets everywhere)")
    P("=" * 110)
    grid, cache = run_leg_b(panels, nel)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # reproduction gate: idea 259 published B136/EWall 10.7% / 1.026 / -17.7%, OOS 1.019 and
    # U56/EWall 10.4% / 1.049 / -15.9% failing 4b on CAGR alone.  Same construction here.
    g10 = grid[grid.bps == COST_BPS]
    for pn, want in [("B136", "10.7% / 1.026 / -17.7%, OOS 1.019"),
                     ("U56", "10.4% / 1.049 / -15.9%, 4b fails on CAGR")]:
        e = g10[(g10.panel == pn) & (g10.arm == "EWall")].iloc[0]
        P(f"  reproduction {pn}/EWall: here {e.CAGR:.1%} / {e.Sharpe:.3f} / {e.MaxDD:.1%}, "
          f"OOS {e.OOS_Sharpe:.3f}, 4b fails on [{e.f4b}]  | idea 259 published {want}")

    t10 = reversal_table(grid, COST_BPS)
    t0 = reversal_table(grid, DIAG_BPS)
    t10.to_csv(OUT / f"{STEM}.reversal.csv", index=False)
    t0.to_csv(OUT / f"{STEM}.reversal_0bps.csv", index=False)
    P("")
    P("B.1 - every matched-ratio cell at 10 bps (EWall minus FWD-n):")
    P(fmt(t10, 4))

    P("")
    P("B.2 - reversal share by target ratio, pooled over the 5 panels (10 bps | 0 bps):")
    for nm, t in [("10 bps", t10), ("0 bps", t0)]:
        s = t.groupby("r_target").agg(cells=("rev", "size"), rev=("rev", "mean"),
                                      rev_eps0=("rev_eps0", "mean"),
                                      ew_wins_S=("ew_wins_S", "mean"),
                                      ew_wins_C=("ew_wins_C", "mean"),
                                      mean_dS=("dS", "mean"), mean_dC=("dC", "mean"),
                                      sat=("sat_share", "mean"))
        P(f"  {nm}:")
        P(fmt(s, 4))
        rho, tt, n = spearman(t.r_real, t.rev.astype(float))
        P(f"    Spearman(rev, r_real) over all {n} cells = {rho:+.4f}  t {tt:+.2f}")
        # r = 1 is the IDENTITY cell: FWD-n holds every eligible name, so it IS EWall and
        # cannot reverse by construction.  The trend must survive dropping it.
        d = t[t.r_target < 1.0]
        rho, tt, n = spearman(d.r_real, d.rev.astype(float))
        P(f"    ... dropping the r=1 identity cell:      {n} cells = {rho:+.4f}  t {tt:+.2f}")

    P("")
    P("B.3 - is the share the SAME across panels at matched r?  (rows = target ratio)")
    piv = t10.pivot_table(index="r_target", columns="panel", values="rev", observed=True)
    P(fmt(piv, 2))
    P("  per-panel Spearman(rev, r_real):")
    rows = []
    for pn, d in t10.groupby("panel"):
        rho, tt, n = spearman(d.r_real, d.rev.astype(float))
        rows.append(dict(panel=pn, cells=n, rev=d.rev.mean(), rho=rho, t=tt))
    P(fmt(pd.DataFrame(rows), 4))

    P("")
    P("B.4 - LEG C: ratio vs the alternatives (same 35 cells, 10 bps).")
    for var in ["r_real", "n", "n_elig"]:
        rho, tt, n = spearman(t10[var], t10.rev.astype(float))
        P(f"  Spearman(rev, {var:7s}) = {rho:+.4f}  t {tt:+.2f}  n {n}")
    P("  reversal share by n (width alone, pooled over panels):")
    nb = t10.assign(nbin=pd.cut(t10.n, [0, 5, 10, 20, 40, 80, 10000])).groupby(
        "nbin", observed=True).agg(cells=("rev", "size"), rev=("rev", "mean"))
    P(fmt(nb, 4))
    P("  reversal share by panel (panel alone):")
    P(fmt(t10.groupby("panel").agg(cells=("rev", "size"), rev=("rev", "mean")), 4))

    P("")
    P("=" * 110)
    P("RULE 8 (i) - the RELATIONSHIP out of sample: threshold fitted on IS reversals only")
    P("=" * 110)
    m, gr, th, is_acc, oos_acc, base, rivals = rule8_relationship(grid)
    P("  ALL threshold grid points (IS accuracy is what selects; OOS is read once, after):")
    P(fmt(gr, 4))
    P(f"  IS-fitted threshold r* = {th:.2f}  (IS accuracy {is_acc:.3f})")
    P(f"  OOS accuracy {oos_acc:.3f} against a majority-class base rate of {base:.3f} "
      f"-> {'BEATS' if oos_acc > base else 'DOES NOT BEAT'} the base rate")
    P(f"  IS reversal share {m.rev_is.mean():.3f}; OOS reversal share {m.rev_oos.mean():.3f}; "
      f"cells agreeing IS vs OOS {float((m.rev_is == m.rev_oos).mean()):.3f}")
    P("  RIVAL classifiers (all fitted IS, read once OOS) - is the WIDTH the predictor, "
      "or the PANEL?")
    P(fmt(rivals.set_index("classifier"), 4))
    P(fmt(m, 3))
    m.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    rivals.to_csv(OUT / f"{STEM}.rivals.csv", index=False)
    gr.to_csv(OUT / f"{STEM}.threshold_grid.csv", index=False)

    P("")
    P("RULE 8 (ii) - the BOOK: does the width rule change what you would run?")
    tab, sels = rule8_book(grid, cache, th)
    P(fmt(tab.set_index("selector"), 4))
    tab.to_csv(OUT / f"{STEM}.selectors.csv", index=False)
    P("  RULES v1 per-panel OOS Sharpe:")
    v1 = grid[(grid.bps == COST_BPS) & (grid.arm == "v1")][["panel", "OOS_Sharpe", "OOS_CAGR",
                                                            "OOS_MaxDD"]]
    P(fmt(v1.set_index("panel"), 4))

    P("")
    P("=" * 110)
    P("KEEP paths - ALL leg-B grid points")
    P("=" * 110)
    for bps in (COST_BPS, DIAG_BPS):
        g = grid[grid.bps == bps]
        arms = g[g.arm.isin(["EWall", "FWD"])]
        P(f"  {bps} bps: 4a {int(arms.p4a.sum())}/{len(arms)}, 4b {int(arms.p4b.sum())}/{len(arms)}")
        pas = arms[arms.p4b]
        if len(pas):
            P(fmt(pas[["panel", "arm", "n", "r_real", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                       "OOS_Sharpe", "turn", "p4a"]].set_index(["panel", "arm"]), 4))
        P(f"  {bps} bps failing-bar census: " +
          ", ".join(f"{k}={v}" for k, v in arms.f4b.value_counts().items()))
    P("")
    P("Full-sample table, 10 bps, every arm:")
    P(grid[grid.bps == COST_BPS][["panel", "arm", "n", "r_real", "CAGR", "Sharpe", "MaxDD",
                                  "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "turn", "gross",
                                  "sat_share", "p4a", "p4b", "f4b"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {STEM}.*.csv / .console.txt")


if __name__ == "__main__":
    main()
