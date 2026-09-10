#!/usr/bin/env python3
"""Idea 493 — is the -0.014 Sharpe cost of choosing on CAGR a record-wide constant?
(lane B, 2026-09-10)

QUEUE ASK
    Idea 270 found the DENOMINATOR of the S_CAGR/S_SHARPE trade homogeneous across five dial
    families (blocked permutation p 0.28 unrestricted / 0.31 file-clustered) at about -0.014
    of OOS Sharpe, while the NUMERATOR (dOOS CAGR) is not (p 0.0001).  The ask: test the
    denominator directly on the record's 6,956 committed menus, FILE-CLUSTERED, with the dial
    FAMILY and the ARM COUNT as the only covariates, and report whether -0.014 survives as a
    quotable constant or is itself dial-specific once n_arms is controlled.

    Idea 270's own permutation never carried n_arms.  Its five families are not comparable in
    menu size: mean arms 3.67 (cadence), 4.67 (gross), 9.17 (other), 17.61 (trim), 18.02 (n) —
    and the two families with the big costs are the two big-menu families.  So the queue's
    question has a sharp form: is "family" in idea 270's table anything more than a label for
    menu size?

DESIGN — two legs, one estimator
    LEG A (the queue's literal ask, OBSERVATIONAL).  The corpus is idea 270's committed
    census.csv, unaltered: 6,956 menus over 73 files.  A menu is one (file, dial column, other-
    column key) group of >= 3 arms carrying IS_Sharpe, IS_CAGR, OOS_Sharpe, OOS_CAGR; its
    denominator is dOOS_Sharpe = OOS_Sharpe(argmax IS_CAGR) - OOS_Sharpe(argmax IS_Sharpe).
    Four models, ALL file-clustered (CR1, df = G-1), every coefficient reported:
        M0  dS ~ 1                      the quotable constant itself
        M1  dS ~ family                 idea 270's reading
        M2  dS ~ log2(arms)             the covariate idea 270 never carried
        M3  dS ~ family + log2(arms)    the queue's ask, both covariates together
    Inference: CR1 t (df = G-1 = 72) plus a wild cluster bootstrap (Rademacher, null imposed,
    B = 9,999, seed fixed) for every reported p, because 73 clusters with one file carrying
    1,028 menus is exactly where the analytic t misbehaves.  Family homogeneity is a joint
    Wald restriction, bootstrapped the same way, in M1 and again in M3.
    PRE-REGISTERED BAR for "-0.014 survives as a quotable constant" (all four must hold):
        B1  M0's 95% CI contains -0.014
        B2  family Wald p > 0.05 in BOTH M1 and M3
        B3  |t| < 2 on log2(arms) in M2
        B4  every family's own file-clustered 95% CI contains -0.014
    Also reported whatever they say: the rate/size decomposition E[dS] = P(disagree) *
    E[dS | disagree] by family and by arm bucket, and the same four models on TODAY's
    re-derived census (the corpus is append-only, so today's scan is a superset of idea 270's
    and the comparison is reproduction, not equality).

    LEG B (the live twin, EXPERIMENTAL).  The census cannot separate family from menu size
    because the record never varied one while holding the other.  So build menus where arm
    count is set BY DESIGN: 3 panels x 5 dial families, each family's arms ordered along its
    own dial, and every CONTIGUOUS WINDOW of length k for k = 3..A taken as a menu (windows,
    not prefixes, so menu SIZE varies without menu LOCATION moving with it).  Each arm is
    backtested once; the menus are selections over cached metrics.  Same two selectors, same
    denominator, same estimator, clusters = (panel, family).

RULE 8 / WHY THIS COSTS CAPITAL ANYTHING
    Every Leg B arm is chosen on IS 2009-01-01..2016-12-31 ONLY and read once on OOS
    2017-01-01+.  Each of the three selectors (S_SHARPE, S_CAGR, DONOTHING = the window's
    middle arm) yields a real book per menu; each book is scored full-sample, in halves and
    OOS against the LIVE RULES v2 baseline on its own panel, against RULES v1 and against SPY,
    and BOTH KEEP paths (4a beat-the-book, 4b capital-worthy) are evaluated at EVERY grid
    point.  If the denominator really is a record-wide constant then the size of the Sharpe
    a selector gives up is knowable in advance; if it is a menu-size effect then the record's
    published per-family costs are not transferable and every quoted cost needs its n_arms.

TUNED PARAMETERS (PROTOCOL rule 4: max 2)
    1. the arm chosen inside a menu — by each selector, on IS only, never on OOS.
    2. the menu size k — pre-registered ladder 3..A, ALL points reported.
    panel, family and window position are ENUMERATED axes, not tuned: every one is written to
    .live_menus.csv, .keeppaths.csv and .walkforward.csv.

CONVENTIONS
    10 bps per unit turnover, weights decided at close t applied at t+1, long only, no
    leverage, weekly base cadence except on the cadence dial.  4a judged against the LIVE
    RULES v2 book on the same panel, 4b against SPY, per PROTOCOL rule 4.
    SURVIVORSHIP: B136 is current constituents of a current screen; SMALL439 is the 483-name
    sub-$2B panel with the 44 tickers whose max_1d_move >= 1.0 dropped first (data/small_meta.csv,
    data/SMALL_PANEL_README.md).  No network is used.

Outputs: .models.csv .census_today.csv .live_arms.csv .live_menus.csv .keeppaths.csv
         .walkforward.csv .console.txt
"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, band_state, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask                                       # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
CENSUS = OUT / "2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_B.census.csv"

COST = 10.0
FREQ = "W"
GROSS, BAND, MAX_VOL = 0.75, 0.03, 0.60
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
QUOTED = -0.014                 # the record's quotable constant, from idea 270's controlled grid
B_BOOT = 9999
SEED = 493

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ==================================================================== estimator
def _codes(cl):
    c = pd.factorize(np.asarray(cl))[0]
    return c, int(c.max()) + 1


def ols_cluster(y, X, cl, XtX_inv=None, codes=None, G=None):
    """OLS with CR1 cluster-robust covariance.  Returns b, se, t, V, resid, G."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, k = X.shape
    if codes is None:
        codes, G = _codes(cl)
    if XtX_inv is None:
        XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    u = y - X @ b
    S = np.zeros((G, k))
    np.add.at(S, codes, X * u[:, None])          # cluster sums of the score
    meat = S.T @ S
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = XtX_inv @ (c * meat) @ XtX_inv
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, b / se, np.nan)
    return b, se, t, V, u, G


def wald(b, V, R):
    """Joint Wald statistic for R b = 0."""
    Rb = R @ b
    M = R @ V @ R.T
    return float(Rb @ np.linalg.pinv(M) @ Rb)


def wcb(y, X, cl, R=None, j=None, target=0.0, B=B_BOOT, seed=SEED):
    """Wild cluster bootstrap (Rademacher), null imposed, cluster-level weights.

    R  -> joint restriction R b = 0 (family homogeneity); returns p for the Wald statistic.
    j  -> single coefficient j, H0: b_j = target; returns two-sided p for |t|.
    """
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    codes, G = _codes(cl)
    XtX_inv = np.linalg.pinv(X.T @ X)
    rng = np.random.default_rng(seed)

    if R is not None:
        # restricted fit: drop the restricted directions by projecting X onto null(R)
        Nspace = np.linalg.svd(R)[2][R.shape[0]:].T          # basis of null(R), k x (k-q)
        Xr = X @ Nspace
        br = np.linalg.pinv(Xr.T @ Xr) @ (Xr.T @ y)
        yhat = Xr @ br
        u = y - yhat
        b0, _, _, V0, _, _ = ols_cluster(y, X, None, XtX_inv, codes, G)
        stat0 = wald(b0, V0, R)
        cnt = 0
        for _ in range(B):
            w = rng.choice([-1.0, 1.0], size=G)[codes]
            bb, _, _, Vb, _, _ = ols_cluster(yhat + u * w, X, None, XtX_inv, codes, G)
            if wald(bb, Vb, R) >= stat0 - 1e-12:
                cnt += 1
        return stat0, (cnt + 1) / (B + 1)

    # single-coefficient test with the null imposed
    b0, se0, _, _, _, _ = ols_cluster(y, X, None, XtX_inv, codes, G)
    t0 = abs((b0[j] - target) / se0[j])
    keep = [c for c in range(X.shape[1]) if c != j]
    Xr = X[:, keep]
    off = y - target * X[:, j]
    br = np.linalg.pinv(Xr.T @ Xr) @ (Xr.T @ off) if keep else np.zeros(0)
    yhat = target * X[:, j] + (Xr @ br if keep else 0.0)
    u = y - yhat
    cnt = 0
    for _ in range(B):
        w = rng.choice([-1.0, 1.0], size=G)[codes]
        bb, seb, _, _, _, _ = ols_cluster(yhat + u * w, X, None, XtX_inv, codes, G)
        if abs((bb[j] - target) / seb[j]) >= t0 - 1e-12:
            cnt += 1
    return t0, (cnt + 1) / (B + 1)


def design(df, fams, use_family, use_arms, base):
    """[intercept, family dummies (base omitted), log2(arms)] and the column names."""
    cols = [np.ones(len(df))]
    names = ["const"]
    if use_family:
        for f in fams:
            if f == base:
                continue
            cols.append((df.family.values == f).astype(float))
            names.append(f"fam[{f}]")
    if use_arms:
        cols.append(np.log2(df.arms.values.astype(float)))
        names.append("log2(arms)")
    return np.column_stack(cols), names


def fit_report(tag, df, fams, use_family, use_arms, base, cluster_col, boot=True):
    X, names = design(df, fams, use_family, use_arms, base)
    b, se, t, V, _, G = ols_cluster(df.dOOS_Sharpe.values, X, df[cluster_col].values)
    rows = []
    for i, nm in enumerate(names):
        lo, hi = b[i] - 1.99 * se[i], b[i] + 1.99 * se[i]
        rows.append(dict(model=tag, term=nm, coef=b[i], se=se[i], t=t[i], lo95=lo, hi95=hi))
    out = pd.DataFrame(rows)
    W = pW = np.nan
    if use_family and len(fams) > 1:
        q = len(fams) - 1
        R = np.zeros((q, X.shape[1]))
        off = 1
        for r in range(q):
            R[r, off + r] = 1.0
        W, pW = wcb(df.dOOS_Sharpe.values, X, df[cluster_col].values, R=R) if boot else (wald(b, V, R), np.nan)
    return out, W, pW, b, se, names, X, G


# ==================================================================== census (today's corpus)
METRIC_KEYS = {"is_sharpe": "IS_Sharpe", "is_cagr": "IS_CAGR",
               "oos_sharpe": "OOS_Sharpe", "oos_cagr": "OOS_CAGR"}
NON_DIAL = {"cagr", "sharpe", "maxdd", "vol", "sortino", "calmar", "h1", "h2", "turn",
            "turnover", "gross", "sat_share", "years", "total", "winrate", "bestday",
            "worstday", "oos_maxdd", "is_maxdd", "is_h1", "is_h2", "equity", "start",
            "end", "date"}
BARRED = {"seed", "draw", "rep", "reps", "rung", "phase", "shift", "fold", "cost_bps",
          "cost", "bps", "panel", "source", "book", "arm", "name", "label", "point",
          "key", "file", "idx", "id", "row", "m", "f", "verdict", "pick", "selector",
          "ticker", "sector", "year", "split", "sample", "variant", "run"}
MAX_ROWS, MAX_LEVELS, MAX_DIALS, MAX_MENUS = 200_000, 60, 12, 2000


def barred_dial(c):
    cl = c.lower().replace(" ", "")
    return cl in BARRED or cl.startswith(("fail", "pass", "p4", "f4", "unnamed"))


def dial_family(colname):
    c = colname.lower()
    if any(k in c for k in ("cadence", "freq", "sched", "period", "rebal")):
        return "cadence"
    if any(k in c for k in ("gross", "lever", "notional")) or c in ("g", "w"):
        return "gross"
    if "vol" in c:
        return "volgate"
    if any(k in c for k in ("band", "trim", "elig", "thresh", "quant", "cut", "floor",
                            "depth", "breadth")) or c in ("q", "b", "d", "t"):
        return "trim"
    if c in ("n", "k", "topn", "nn", "n_hold", "nhold", "top") or c.startswith("n_"):
        return "n"
    return "other"


def census():
    """Idea 270's leg-B scanner, verbatim, re-run over TODAY's (append-only) corpus."""
    files = sorted(OUT.glob("*.csv")) + sorted(OUT.glob("*.csv.gz"))
    files = [f for f in files if not f.name.startswith(STEM)]
    menus, nfiles, unread, skipped_big, dupcol = [], 0, 0, 0, 0
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            unread += 1
            continue
        if len(df) > MAX_ROWS:
            skipped_big += 1
            continue
        low = {c.lower().replace(" ", ""): c for c in df.columns}
        if not all(k in low for k in METRIC_KEYS):
            continue
        ren = {low[k]: v for k, v in METRIC_KEYS.items()}
        df = df.rename(columns=ren)
        if df.columns.duplicated().any():
            dupcol += 1          # a file carrying e.g. both IS_Sharpe and is_sharpe: skipped, not merged
            continue
        for v in METRIC_KEYS.values():
            df[v] = pd.to_numeric(df[v], errors="coerce")
        df = df.dropna(subset=list(METRIC_KEYS.values()))
        if len(df) < 3:
            continue
        labels = [c for c in df.columns
                  if c not in METRIC_KEYS.values()
                  and c.lower().replace(" ", "") not in NON_DIAL
                  and not c.lower().startswith(("is_", "oos_", "spy_", "v1_", "v2_"))
                  and 1 < df[c].nunique(dropna=False) <= MAX_LEVELS]
        used = False
        cands = [c for c in labels
                 if df[c].nunique(dropna=False) >= 3 and not barred_dial(c)][:MAX_DIALS]
        for d in cands:
            others = [c for c in labels if c != d]
            try:
                grp = df.groupby(others, dropna=False) if others else [((), df)]
                if others and grp.ngroups > MAX_MENUS:
                    continue
            except Exception:
                continue
            for key, g in grp:
                g = g.dropna(subset=[d])
                if g[d].nunique() < 3 or len(g) < 3:
                    continue
                s = g.loc[g.IS_Sharpe.idxmax()]
                c = g.loc[g.IS_CAGR.idxmax()]
                dS = float(c.OOS_Sharpe - s.OOS_Sharpe)
                dC = float(c.OOS_CAGR - s.OOS_CAGR)
                dC_pp = dC * 100.0 if g.OOS_CAGR.abs().max() < 2.0 else dC
                menus.append(dict(file=f.name, dial_col=d, family=dial_family(d),
                                  arms=len(g), same=bool(s.name == c.name),
                                  dOOS_Sharpe=dS, dOOS_CAGR_pp=dC_pp,
                                  xr=(np.nan if (s.name == c.name or dS >= 0)
                                      else dC_pp / (-dS)),
                                  key=str(key)))
                used = True
        nfiles += used
    return pd.DataFrame(menus), len(files), nfiles, unread, skipped_big, dupcol


# ==================================================================== live harness
def fast_backtest(prices, weights, freq=FREQ, cost=COST):
    """Vectorised equivalent of engine.backtest (asserted against it in GATE 1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    net = (held * rets).sum(axis=1) - turn * cost / 1e4
    return pd.Series(net, index=idx)


def _m(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable):
        keep = list(dict.fromkeys([c for c in cols if c in px.columns] + ["SPY"]))
        return px[keep].dropna(how="all").ffill(), set(tradable)

    return {
        "U56": sub(px56, list(px56.columns), [c for c in px56.columns if c != "SPY"]),
        "B136": sub(px136, list(px136.columns), [c for c in px136.columns if c != "SPY"]),
        "SMALL439": sub(pxs, s_stk, s_stk),
    }


def _ew(px, mask, gross, tradable):
    e = mask.astype(float).where(px.notna(), 0.0)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        e[drop] = 0.0
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_topn(px, tr, n, gross=GROSS):
    s, above, _ = score(px)
    return _ew(px, s.where(above).rank(axis=1, ascending=False) <= n, gross, tr)


def w_band(px, tr, band, gross=GROSS):
    return _ew(px, band_state(px, band), gross, tr)


def w_volcap(px, tr, cap, gross=GROSS):
    _, above, vol20 = score(px)
    return _ew(px, above & (vol20 < cap), gross, tr)


def w_v1(px, tr, n=5, w=0.15):
    """RULES v1 restricted to the panel's tradables (SPY is a benchmark, never a holding)."""
    s, above, vol20 = score(px)
    m = above & (vol20 < MAX_VOL)
    drop = [c for c in px.columns if c not in tr]
    if drop:
        m[drop] = False
    rank = s.where(m).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * w


DIALS = {
    "n":       [(f"N{v}", "topn", v, "W") for v in [3, 5, 8, 10, 15, 20, 30, 40, 50, 60]],
    "gross":   [(f"G{v:.2f}", "gross", v, "W") for v in [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.85, 1.00]],
    "trim":    [(f"B{v:.2f}", "band", v, "W") for v in [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16]],
    "volgate": [(f"V{v:.2f}", "volcap", v, "W") for v in [0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.80, 9.99]],
    "cadence": [(f"FREQ_{f}", "cadence", BAND, f) for f in ["D", "W", "M", "Q"]],
}


def arm_weights(px, tr, form, v):
    if form == "topn":
        return w_topn(px, tr, int(v))
    if form == "band" or form == "cadence":
        return w_band(px, tr, v)
    if form == "gross":
        return w_band(px, tr, BAND, gross=v)
    if form == "volcap":
        return w_volcap(px, tr, v)
    raise ValueError(form)


def keep_paths(r, base, spy):
    """PROTOCOL 4a (vs the live book) and 4b (vs SPY), verbatim, CAL split for the OOS leg."""
    r1, r2 = halves(r)
    b1, b2 = halves(base)
    s1, s2 = halves(spy)
    m, mb, ms = _m(r), _m(base), _m(spy)
    p4a = bool(_m(r1)["Sharpe"] > _m(b1)["Sharpe"] and _m(r2)["Sharpe"] > _m(b2)["Sharpe"]
               and m["MaxDD"] >= mb["MaxDD"])
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    fail = []
    if not _m(r1)["Sharpe"] > _m(s1)["Sharpe"]:
        fail.append("H1")
    if not _m(r2)["Sharpe"] > _m(s2)["Sharpe"]:
        fail.append("H2")
    if not _m(ro)["Sharpe"] > _m(so)["Sharpe"]:
        fail.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]):
        fail.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        fail.append("CAGR")
    return p4a, (not fail), (",".join(fail) if fail else "-")


# ==================================================================== main
def main():
    t_start = time.time()
    P("=" * 200)
    P(f"IDEA 493 — is the {QUOTED:+.3f} Sharpe cost of choosing on CAGR a record-wide constant?  (lane B, 2026-09-10)")
    P("=" * 200)

    # ---------------------------------------------------------------- GATES
    P("\n[0] GATES (pre-registered, run before any new number is read)")
    px56, tr56 = None, None
    panels = build_panels()
    px56, tr56 = panels["U56"]
    start56 = px56.index[260]

    w_v2 = rules_v2_weights(px56, band=BAND, gross=GROSS)
    r_eng = backtest(px56, w_v2, cost_bps=COST, freq=FREQ)["returns"]
    r_fast = fast_backtest(px56, w_v2)
    g1 = float(np.nanmax(np.abs((r_eng - r_fast).loc[start56:].values)))
    P(f"  G1 fast_backtest vs engine.backtest @10bps on U56 RULES v2 : max abs diff {g1:.3e}")

    g2 = float(np.nanmax(np.abs((w_band(px56, set(px56.columns), BAND, GROSS) - w_v2).values)))
    g2b = float(np.nanmax(np.abs((w_band(px56, tr56, BAND, GROSS) - w_v2).values)))
    P(f"  G2 local band book over ALL columns IS baseline.rules_v2_weights : max abs diff {g2:.3e}")
    P(f"     (the panel books below hold only the panel's TRADABLES, so SPY is a benchmark and never a "
      f"holding: that convention moves the same book by {g2b:.3e} on U56 — a stated design choice, not a gate)")

    mv2 = _m(r_fast.loc[start56:])
    h1, h2 = halves(r_fast.loc[start56:])
    P(f"  G3 LIVE RULES v2 on U56 : CAGR {mv2['CAGR']:.2%} / Sharpe {mv2['Sharpe']:.4f} / MaxDD {mv2['MaxDD']:.2%} "
      f"(halves {_m(h1)['Sharpe']:.4f} / {_m(h2)['Sharpe']:.4f})  [record 2026-09-10: 8.66% / 1.2056 / -12.05% "
      f"(1.2259/1.1909), read on data ending 2026-09-08]")
    P(f"     data/prices.csv now ends {px56.index[-1].date()} ({len(px56)} rows) — one extra session, so G3 is "
      f"REPRODUCTION, not equality; the deltas are CAGR {mv2['CAGR']-0.0866:+.4f}, Sharpe {mv2['Sharpe']-1.2056:+.4f}, "
      f"MaxDD {mv2['MaxDD']+0.1205:+.4f}")

    cen = pd.read_csv(CENSUS)
    fc = cen.groupby("file").dOOS_Sharpe.mean()
    fcc = cen.groupby("file").dOOS_CAGR_pp.mean()
    tS = fc.mean() / (fc.std(ddof=1) / np.sqrt(len(fc)))
    tC = fcc.mean() / (fcc.std(ddof=1) / np.sqrt(len(fcc)))
    P(f"  G4 idea 270's committed census re-read: {len(cen)} menus / {cen.file.nunique()} files "
      f"[published 6956 / 73]; file-clustered dS {fc.mean():+.4f} (t {tS:+.2f}, neg {(fc<0).sum()}/{len(fc)}) "
      f"[published -0.0162, t -3.07, 36/73]; dCAGR {fcc.mean():+.4f} pp (t {tC:+.2f}, pos {(fcc>0).sum()}/{len(fcc)}) "
      f"[published +0.63, t +5.07, 52/73]")
    famfile = cen.groupby(["family", "file"]).dOOS_Sharpe.mean().groupby("family").mean()
    P("  G4b per-family FILE-CLUSTERED dS (published: cadence -0.0024, gross -0.0035, n -0.0446, other -0.0150, trim -0.0446):")
    P("     " + "  ".join(f"{k} {v:+.4f}" for k, v in famfile.items()))

    # ---------------------------------------------------------------- LEG A
    P("\n[1] LEG A — the queue's literal ask: family and arm count on the record's 6,956 committed menus")
    fams = sorted(cen.family.unique())
    base_fam = "other"                       # the largest family is the omitted base
    P(f"  families {fams}, base = '{base_fam}'; clusters = file (G = {cen.file.nunique()})")
    P("\n  menu-size composition of idea 270's five families (the covariate its permutation never carried):")
    comp = cen.groupby("family").agg(menus=("same", "size"), files=("file", "nunique"),
                                     mean_arms=("arms", "mean"), med_arms=("arms", "median"),
                                     max_arms=("arms", "max"),
                                     disagree=("same", lambda s: 1 - s.mean()),
                                     dS=("dOOS_Sharpe", "mean"))
    P(fmt(comp))

    models = []
    P("\n  M0  dS ~ 1                    (the quotable constant)")
    o0, _, _, b0, se0, nm0, X0, G0 = fit_report("M0", cen, fams, False, False, base_fam, "file")
    P(fmt(o0.set_index("term")[["coef", "se", "t", "lo95", "hi95"]], 5))
    t_q, p_q = wcb(cen.dOOS_Sharpe.values, X0, cen.file.values, j=0, target=QUOTED)
    t_0, p_0 = wcb(cen.dOOS_Sharpe.values, X0, cen.file.values, j=0, target=0.0)
    P(f"    wild cluster bootstrap ({B_BOOT} draws): H0 const = {QUOTED:+.3f} -> |t| {t_q:.3f}, p {p_q:.4f}"
      f"   |   H0 const = 0 -> |t| {t_0:.3f}, p {p_0:.4f}")
    models.append(o0)

    P("\n  M1  dS ~ family               (idea 270's reading)")
    o1, W1, pW1, *_ = fit_report("M1", cen, fams, True, False, base_fam, "file")
    P(fmt(o1.set_index("term")[["coef", "se", "t", "lo95", "hi95"]], 5))
    P(f"    family homogeneity Wald {W1:.3f}, wild-cluster-bootstrap p {pW1:.4f}")
    models.append(o1)

    P("\n  M2  dS ~ log2(arms)           (the covariate idea 270 never carried)")
    o2, _, _, b2, se2, nm2, X2, _ = fit_report("M2", cen, fams, False, True, base_fam, "file")
    P(fmt(o2.set_index("term")[["coef", "se", "t", "lo95", "hi95"]], 5))
    t_a, p_a = wcb(cen.dOOS_Sharpe.values, X2, cen.file.values, j=1, target=0.0)
    P(f"    wild cluster bootstrap: H0 log2(arms) = 0 -> |t| {t_a:.3f}, p {p_a:.4f}")
    models.append(o2)

    P("\n  M3  dS ~ family + log2(arms)  (the queue's ask: both covariates together)")
    o3, W3, pW3, b3, se3, nm3, X3, _ = fit_report("M3", cen, fams, True, True, base_fam, "file")
    P(fmt(o3.set_index("term")[["coef", "se", "t", "lo95", "hi95"]], 5))
    P(f"    family homogeneity Wald {W3:.3f}, wild-cluster-bootstrap p {pW3:.4f}")
    ja = nm3.index("log2(arms)")
    t_a3, p_a3 = wcb(cen.dOOS_Sharpe.values, X3, cen.file.values, j=ja, target=0.0)
    P(f"    wild cluster bootstrap: H0 log2(arms) = 0 | family -> |t| {t_a3:.3f}, p {p_a3:.4f}")
    models.append(o3)

    # per-family own CI (file-clustered, one intercept per family)
    P("\n  per-family file-clustered mean with its own 95% CI, and whether it contains the quoted constant:")
    rows = []
    for f in fams:
        sub = cen[cen.family == f]
        Xf = np.ones((len(sub), 1))
        b, se, t, _, _, Gf = ols_cluster(sub.dOOS_Sharpe.values, Xf, sub.file.values)
        lo, hi = b[0] - 1.99 * se[0], b[0] + 1.99 * se[0]
        rows.append(dict(family=f, files=Gf, menus=len(sub), mean=b[0], se=se[0],
                         lo95=lo, hi95=hi, contains_quoted=bool(lo <= QUOTED <= hi)))
    fam_ci = pd.DataFrame(rows).set_index("family")
    P(fmt(fam_ci, 5))

    # rate / size decomposition
    P("\n  rate/size decomposition  E[dS] = P(disagree) * E[dS | disagree]:")
    dec = cen.assign(dis=(~cen.same.astype(bool)).astype(float))

    def decomp(frame, by):
        g = frame.groupby(by, observed=True)
        d = g.agg(menus=("dis", "size"), files=("file", "nunique"), rate=("dis", "mean"),
                  pooled=("dOOS_Sharpe", "mean"))
        d["cond"] = frame[frame.dis > 0].groupby(by, observed=True).dOOS_Sharpe.mean()
        d["product"] = d.rate * d.cond
        return d[["menus", "files", "rate", "cond", "product", "pooled"]]

    P(fmt(decomp(dec, "family")))
    dec["bucket"] = pd.cut(dec.arms, [2, 3, 4, 6, 10, 20, 10_000])
    P("\n  by ARM BUCKET (the same decomposition, menu size on the rows):")
    P(fmt(decomp(dec, "bucket")))

    bars = dict(
        B1=bool(o0.lo95.iloc[0] <= QUOTED <= o0.hi95.iloc[0]),
        B2=bool(pW1 > 0.05 and pW3 > 0.05),
        B3=bool(abs(o2.loc[o2.term == "log2(arms)", "t"].iloc[0]) < 2),
        B4=bool(fam_ci.contains_quoted.all()),
    )
    P("\n  PRE-REGISTERED BAR for '-0.014 survives as a quotable constant':")
    P(f"    B1 M0 95% CI contains {QUOTED:+.3f}                 : {bars['B1']}   "
      f"[{o0.lo95.iloc[0]:+.5f}, {o0.hi95.iloc[0]:+.5f}]")
    P(f"    B2 family Wald p > 0.05 in BOTH M1 and M3      : {bars['B2']}   [M1 {pW1:.4f}, M3 {pW3:.4f}]")
    P(f"    B3 |t| < 2 on log2(arms) in M2                 : {bars['B3']}   "
      f"[t {o2.loc[o2.term == 'log2(arms)', 't'].iloc[0]:+.3f}]")
    P(f"    B4 every family's own 95% CI contains {QUOTED:+.3f}  : {bars['B4']}   "
      f"[{fam_ci.contains_quoted.sum()}/{len(fam_ci)} families]")
    P(f"    VERDICT ON THE CONSTANT: {'SURVIVES' if all(bars.values()) else 'DOES NOT SURVIVE'} "
      f"({sum(bars.values())}/4 bars)")

    # ---------------------------------------------------------------- today's census
    P("\n[2] ROBUSTNESS — the same four models on TODAY's re-derived census (append-only superset)")
    t0 = time.time()
    cen2, nfile_all, nfile_used, unread, big, dupcol = census()
    cen2.to_csv(OUT / f"{STEM}.census_today.csv", index=False)
    P(f"  {nfile_all} committed CSVs scanned in {time.time()-t0:.0f}s ({unread} unreadable, {big} over {MAX_ROWS} rows, "
      f"{dupcol} with duplicated metric columns, all skipped); "
      f"{nfile_used} carry the four metrics and a sweepable dial -> {len(cen2)} menus "
      f"[idea 270 saw 2162 files / 73 used / 6956 menus]")
    fc2 = cen2.groupby("file").dOOS_Sharpe.mean()
    P(f"  file-clustered dS {fc2.mean():+.4f} (t {fc2.mean()/(fc2.std(ddof=1)/np.sqrt(len(fc2))):+.2f}, "
      f"neg {(fc2<0).sum()}/{len(fc2)})")
    fams2 = sorted(cen2.family.unique())
    for tag, uf, ua in (("M0'", False, False), ("M1'", True, False), ("M2'", False, True), ("M3'", True, True)):
        o, W, pW, *_ = fit_report(tag, cen2, fams2, uf, ua, base_fam, "file")
        models.append(o)
        P(f"\n  {tag}  dS ~ {'family ' if uf else ''}{'+ ' if uf and ua else ''}{'log2(arms)' if ua else ('1' if not uf else '')}")
        P(fmt(o.set_index("term")[["coef", "se", "t", "lo95", "hi95"]], 5))
        if uf:
            P(f"    family homogeneity Wald {W:.3f}, wild-cluster-bootstrap p {pW:.4f}")

    pd.concat(models).to_csv(OUT / f"{STEM}.models.csv", index=False)

    # ---------------------------------------------------------------- LEG B
    P("\n[3] LEG B — the live twin: menu size set BY DESIGN (contiguous windows), rule 8 throughout")
    arm_rows, menu_rows, keep_rows = [], [], []
    for pname, (px, tr) in panels.items():
        t0 = time.time()
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_r = fast_backtest(px, w_band(px, tr, BAND, GROSS)).loc[start:]
        v1_r = fast_backtest(px, w_v1(px, tr)).loc[start:]
        cache = {}
        for fam, arms in DIALS.items():
            for (arm, form, v, freq) in arms:
                key = (form, v, freq)
                if key not in cache:
                    w = arm_weights(px, tr, form, v)
                    cache[key] = fast_backtest(px, w, freq=freq).loc[start:]
                r = cache[key]
                mi, mo, mf = _m(r.loc[IS_START:IS_END]), _m(r.loc[OOS_START:]), _m(r)
                arm_rows.append(dict(panel=pname, family=fam, arm=arm, dial_value=v, freq=freq,
                                     IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                                     OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                                     FULL_CAGR=mf["CAGR"], FULL_Sharpe=mf["Sharpe"], FULL_MaxDD=mf["MaxDD"]))
        P(f"  {pname}: {len(px.columns)-1} tradables, {sum(len(a) for a in DIALS.values())} arms "
          f"backtested in {time.time()-t0:.0f}s")

        A = pd.DataFrame([a for a in arm_rows if a["panel"] == pname])
        for fam, arms in DIALS.items():
            order = [a[0] for a in arms]
            sub = A[A.family == fam].set_index("arm").loc[order]
            Aq = len(order)
            for k in range(3, Aq + 1):
                for w0 in range(0, Aq - k + 1):
                    win = sub.iloc[w0:w0 + k]
                    iS = win.IS_Sharpe.idxmax()
                    iC = win.IS_CAGR.idxmax()
                    iD = win.index[(k - 1) // 2]
                    dS = float(win.loc[iC, "OOS_Sharpe"] - win.loc[iS, "OOS_Sharpe"])
                    dC = float((win.loc[iC, "OOS_CAGR"] - win.loc[iS, "OOS_CAGR"]) * 100.0)
                    menu_rows.append(dict(panel=pname, family=fam, arms=k, window=w0,
                                          first=win.index[0], last=win.index[-1],
                                          pick_S=iS, pick_C=iC, pick_D=iD,
                                          same=bool(iS == iC), dOOS_Sharpe=dS, dOOS_CAGR_pp=dC,
                                          file=f"{pname}|{fam}"))
                    for sel, arm in (("S_SHARPE", iS), ("S_CAGR", iC), ("DONOTHING", iD)):
                        row = sub.loc[arm]
                        form, v, freq = [(f, vv, fq) for (a, f, vv, fq) in DIALS[fam] if a == arm][0]
                        r = cache[(form, v, freq)]
                        p4a, p4b, fail = keep_paths(r, base_r, spy)
                        keep_rows.append(dict(panel=pname, family=fam, arms=k, window=w0,
                                              selector=sel, arm=arm,
                                              FULL_CAGR=row.FULL_CAGR, FULL_Sharpe=row.FULL_Sharpe,
                                              FULL_MaxDD=row.FULL_MaxDD,
                                              H1=_m(halves(r)[0])["Sharpe"], H2=_m(halves(r)[1])["Sharpe"],
                                              OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                                              OOS_MaxDD=row.OOS_MaxDD,
                                              p4a=p4a, p4b=p4b, fail4b=fail))
        # panel comparands
        for nm, r in (("RULES v2 (live)", base_r), ("RULES v1", v1_r), ("SPY", spy)):
            mo, mf = _m(r.loc[OOS_START:]), _m(r)
            keep_rows.append(dict(panel=pname, family="_comparand", arms=-1, window=-1,
                                  selector=nm, arm=nm, FULL_CAGR=mf["CAGR"], FULL_Sharpe=mf["Sharpe"],
                                  FULL_MaxDD=mf["MaxDD"], H1=_m(halves(r)[0])["Sharpe"],
                                  H2=_m(halves(r)[1])["Sharpe"], OOS_CAGR=mo["CAGR"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  p4a=False, p4b=False, fail4b="-"))

    ARMS = pd.DataFrame(arm_rows)
    MEN = pd.DataFrame(menu_rows)
    KP = pd.DataFrame(keep_rows)
    ARMS.to_csv(OUT / f"{STEM}.live_arms.csv", index=False)
    MEN.to_csv(OUT / f"{STEM}.live_menus.csv", index=False)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(f"  {len(ARMS)} arms, {len(MEN)} designed menus, {len(KP)} scored books")

    P("\n  designed menus: dOOS_Sharpe by ARM COUNT (menu size varied, family held on the rows)")
    piv = MEN.pivot_table(index="family", columns="arms", values="dOOS_Sharpe", aggfunc="mean")
    P(fmt(piv))
    P("\n  disagreement rate by the same grid:")
    P(fmt(MEN.assign(dis=~MEN.same).pivot_table(index="family", columns="arms", values="dis", aggfunc="mean")))
    P("\n  pooled over families, by arm count:")
    byk = MEN.groupby("arms").agg(menus=("same", "size"), rate=("same", lambda s: 1 - s.mean()),
                                  dS=("dOOS_Sharpe", "mean"), dC=("dOOS_CAGR_pp", "mean"))
    P(fmt(byk))

    P("\n  conditional on DISAGREEMENT (the census's own dilution problem, stated for both corpora):")
    dis = MEN[~MEN.same]
    P(f"    designed grid: {len(dis)}/{len(MEN)} menus disagree ({len(dis)/len(MEN):.4f}); "
      f"E[dS | disagree] {dis.dOOS_Sharpe.mean():+.4f}; pooled {MEN.dOOS_Sharpe.mean():+.4f}")
    cd = cen[~cen.same.astype(bool)]
    P(f"    record census: {len(cd)}/{len(cen)} menus disagree ({len(cd)/len(cen):.4f}); "
      f"E[dS | disagree] {cd.dOOS_Sharpe.mean():+.4f}; pooled {cen.dOOS_Sharpe.mean():+.4f}")

    P("\n  the SAME four models on the designed grid (clusters = panel|family, G = %d; base family 'n'):"
      % MEN.file.nunique())
    live_models = []
    for tag, uf, ua in (("L0", False, False), ("L1", True, False), ("L2", False, True), ("L3", True, True)):
        o, W, pW, b, se, nms, XL, _ = fit_report(tag, MEN, sorted(MEN.family.unique()), uf, ua, "n", "file")
        live_models.append(o)
        P(f"\n  {tag}  dS ~ {'family ' if uf else ''}{'+ ' if uf and ua else ''}{'log2(arms)' if ua else ('1' if not uf else '')}")
        P(fmt(o.set_index("term")[["coef", "se", "t", "lo95", "hi95"]], 5))
        if uf:
            P(f"    family homogeneity Wald {W:.3f}, wild-cluster-bootstrap p {pW:.4f}")
        if tag == "L0":
            tq, pq = wcb(MEN.dOOS_Sharpe.values, XL, MEN.file.values, j=0, target=QUOTED)
            tz, pz = wcb(MEN.dOOS_Sharpe.values, XL, MEN.file.values, j=0, target=0.0)
            P(f"    wild cluster bootstrap: H0 const = {QUOTED:+.3f} (the record's quoted cost) -> |t| {tq:.3f}, "
              f"p {pq:.4f}   |   H0 const = 0 -> |t| {tz:.3f}, p {pz:.4f}")
        if tag == "L2":
            ta, pa = wcb(MEN.dOOS_Sharpe.values, XL, MEN.file.values, j=1, target=0.0)
            P(f"    wild cluster bootstrap: H0 log2(arms) = 0 -> |t| {ta:.3f}, p {pa:.4f}")
    pd.concat(models + live_models).to_csv(OUT / f"{STEM}.models.csv", index=False)

    # ---------------------------------------------------------------- rule 8 / KEEP paths
    P("\n[4] RULE 8 — books chosen on IS 2009-2016 only, read once on OOS 2017-2026")
    comp = KP[KP.family == "_comparand"].set_index(["panel", "selector"])
    sel = KP[KP.family != "_comparand"]
    P("\n  panel comparands (OOS 2017+):")
    P(fmt(comp[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD"]]))
    P("\n  selector books, OOS means by panel x selector (all %d books, every grid point in .keeppaths.csv):" % len(sel))
    tab = sel.groupby(["panel", "selector"]).agg(books=("arm", "size"),
                                                 OOS_CAGR=("OOS_CAGR", "mean"),
                                                 OOS_Sharpe=("OOS_Sharpe", "mean"),
                                                 OOS_MaxDD=("OOS_MaxDD", "mean"),
                                                 FULL_Sharpe=("FULL_Sharpe", "mean"),
                                                 FULL_MaxDD=("FULL_MaxDD", "mean"),
                                                 p4a=("p4a", "sum"), p4b=("p4b", "sum"))
    P(fmt(tab))
    P("\n  KEEP paths over EVERY selector book:")
    kk = sel.groupby("selector").agg(books=("arm", "size"), p4a=("p4a", "sum"), p4b=("p4b", "sum"))
    kk["both"] = [int(((sel.selector == s) & sel.p4a & sel.p4b).sum()) for s in kk.index]
    P(fmt(kk, 0))
    P("  4b failure legs over all books: " + ", ".join(
        f"{k} {v}" for k, v in sel.fail4b.value_counts().head(10).items()))
    uniq = sel.drop_duplicates(["panel", "family", "arm"])
    P(f"  distinct (panel, arm) books behind those rows: {len(uniq)}; 4a {int(uniq.p4a.sum())}, "
      f"4b {int(uniq.p4b.sum())}, both {int((uniq.p4a & uniq.p4b).sum())}")

    wf = sel.copy()
    wf["quoted_cost"] = QUOTED
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  walk-forward artefact -> {STEM}.walkforward.csv ({len(wf)} rows)")

    # ---------------------------------------------------------------- summary
    P("\n[5] SUMMARY")
    P(f"  LEG A  constant {o0.coef.iloc[0]:+.5f} [{o0.lo95.iloc[0]:+.5f}, {o0.hi95.iloc[0]:+.5f}]; "
      f"family Wald p M1 {pW1:.4f} -> M3 {pW3:.4f}; log2(arms) {o2.coef.iloc[1]:+.5f} "
      f"(t {o2.t.iloc[1]:+.2f}, p {p_a:.4f}); bars {sum(bars.values())}/4")
    P(f"  LEG B  designed menus {len(MEN)}; pooled dS {MEN.dOOS_Sharpe.mean():+.5f}; "
      f"k=3 {byk.dS.iloc[0]:+.5f} -> k={byk.index[-1]} {byk.dS.iloc[-1]:+.5f}")
    P(f"  run time {time.time()-t_start:.0f}s")
    P("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
