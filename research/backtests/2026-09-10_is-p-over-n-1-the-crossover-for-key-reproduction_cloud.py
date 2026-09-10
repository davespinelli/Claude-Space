#!/usr/bin/env python3
"""Idea 498 - "is-p-over-n-1-the-crossover-for-key-reproduction" (cloud).

What this run exists to settle
------------------------------
Idea 483 (cloud lane) measured, on 200 draw books per panel, how well a WIDE membership control
reproduces the very key it is supposed to residualise OUT OF FOLD:

    sd_reproduced_OOF   U56 0.9387 (p=55,  n=200, p/n 0.275)
                        B136 0.6676 (p=135, n=200, p/n 0.675)
                        SMALL439 0.3151 (p=439, n=200, p/n 2.195)

Three points, one per panel, each at a different p/n AND a different panel.  The queue's reading
is that p/n is the axis and 1 is the crossing: below it the control honestly knows its own key,
above it the control cannot reproduce what it claims to remove and has stopped being a control.
That reading is not testable on three points that confound p/n with the panel, so this run sweeps
n finely at fixed panel - the queue's own prescription - and independently sweeps p by column
subset, which separates the two.

What makes the question answerable rather than definitional
-----------------------------------------------------------
The key `sd_i` = the cross-sectional dispersion of member annualised returns in book i is a
NONLINEAR function of the membership row M[i].  So a linear ridge on M has two distinct reasons
to fail to reproduce it: too few rows for p columns (the queue's p/n story), or a ceiling set by
the nonlinearity itself that no amount of n removes.  Those look identical at one n.

So this run carries a POSITIVE CONTROL that is EXACTLY linear in the same design:

    mn_i = mean of member annualised returns = (M[i] @ ann0) / k       (verified to machine
                                                                       precision in G4; ann0 is
                                                                       ann with any name lacking a
                                                                       return over the window set
                                                                       to the panel mean - 0 such
                                                                       names on U56 and SMALL439,
                                                                       1 of 135 on B136, and the
                                                                       count is printed)

`mn` is reproducible by construction at n >> p.  If the p/n = 1 crossing is a property of the
DESIGN, both targets cross together.  If `sd` crosses and `mn` does not, the crossing is about
the nonlinearity and p/n is the wrong axis to publish.  Either answer is reportable; the run is
built so it cannot only confirm.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (THE QUEUE'S)  REPRO_OOF(n, p) on a fine ladder, per panel.  Locate the crossing where
                      honest reproduction of `sd` falls below 0.50, and read it in p/n.
                      Pre-registered, at the headline (lam = 1.0, K = 10, p = the full panel):
                        CONFIRMED  crossing p/n in [0.75, 1.33] on ALL THREE panels
                        PARTIAL    crossing p/n in [0.50, 2.00] on all three
                        REFUTED    otherwise, or if a panel has no crossing at all
    Q2 (IS p/n THE AXIS?)  The same surface read as a function of p at fixed n and of n at fixed
                      p.  If p/n is the axis, cells with equal p/n agree; the spread of
                      REPRO_OOF within a p/n band is the test.
    Q3 (THE CONTROL)  `mn`, exactly linear in M, on the identical grid.  Its crossing separates
                      "not enough rows" from "not a linear function of the design".
    Q4 (RULE 8)       Crossing located on the FIRST half of each panel's sample only, read ONCE
                      on the second half.  Also the book-level rule-8 selector chooser.
    Q5 (PROTOCOL)     Both KEEP paths on every draw book at rungs 0/10/25, and the rule-8 book
                      chooser with OOS CAGR/Sharpe/MaxDD against the live RULES v2 baseline
                      and SPY.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. draws n   12 rungs 30..900, nested prefixes of one drawn pool, ALL reported
    2. p         column subsets 10..full panel, ALL reported
Reported axes, NEVER tuned and never selected on: ridge penalty lam (6), fold count K (4),
target (sd / mn), panel (3), cost rung (3), sample half.  The headline cell is PRE-REGISTERED as
lam = 1.0 (the log-midpoint of idea 483's own ladder) and K = 10 (idea 252's committed fold
count), fixed before any number is read; every other lam and K is reported beside it.

Reproduction gates (section [0], printed before any new number is read)
    G1  a draw book backtested on the 20-name SUB-PANEL equals the same book backtested on the
        whole panel.  Bar 1e-12.  This licenses the sweep's only speedup and nothing else.
    G2  idea 483 cloud's COMMITTED .grid.csv reproduced at its own settings (n = 200, its 6 lam
        x 4 K, BOTH widths), on R2_control_reproduces_sd_insample / _oof / t_insample / t_oof.
        Bar 1e-9.  Its NARROW10 subset is rebuilt from ITS OWN 200-draw M, not this run's
        900-draw pool, because the 10 most-drawn names are not the same set at the two depths.
    G3  the queue's quoted triple 0.939 / 0.668 / 0.315 at p/n 0.28 / 0.68 / 2.20.
    G4  mn is EXACTLY linear in M: max |mn - (M @ ann0)/k|.  Bar 1e-12.  The distance
        from the naive nanmean-over-members form is printed beside it, with the count
        of names the substitution touches, so the construction is not hidden.
    G5  fast numpy CAGR/Sharpe/MaxDD vs engine.metrics on 200 real series.  Bar 1e-12.

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is optimistic and SMALL439 is
a screen of sub-$2B names that exist today (names with max_1d_move >= 1.0 dropped per
data/small_meta.csv).  This run's object is a reproduction R-squared between a design and its own
key on a fixed panel, which a common level shift does not move; the cross-panel readings inherit
whatever differential the three screens carry, and Q2's within-panel n sweep is the control
offered against that.  SMALL439 starts 2010-01-04.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT = OUT / "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud.grid.csv"
CACHE = Path("/tmp/claude-0/-home-user-Claude-Space/a0283c62-8cfb-5098-bae0-b273fee4919a/scratchpad/i498books")   # outside the repo; books only

COST, FREQ = 10, "W"
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
KNAMES = 20                       # names per draw book (idea 483's)
NMAX = 900                        # drawn pool; the n ladder takes nested prefixes
NS = [30, 45, 60, 90, 120, 180, 240, 360, 480, 600, 750, 900]      # tuned param 1
PS = [10, 20, 40, 80, 160, 320]                                     # tuned param 2 (+ full panel)
LAMS = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]     # reported, never tuned
FOLDS = [2, 5, 10, 25]                          # reported, never tuned
LAM_HEAD, K_HEAD = 1.0, 10                      # PRE-REGISTERED headline cell
BAR = 0.50                                      # the queue's "honest reproduction" bar
SEED0, FOLD_SEED = 0, 7                         # idea 483's, verbatim, so its rows reproduce
PUB483 = {"U56": 0.9387, "B136": 0.6676, "SMALL439": 0.3151}
CONFIRM_LO, CONFIRM_HI = 0.75, 1.333
PARTIAL_LO, PARTIAL_HI = 0.50, 2.00

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 1200)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def ew_weights(px, names, gross=1.0):
    """Idea 483's, verbatim."""
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[names].notna().astype(float)
    w[names] = gross * sub.div(sub.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w


def draw_names(tickers, i):
    """Idea 483's draw_books draw, verbatim: one rng per book, seeded SEED0 + i."""
    rng = np.random.default_rng(SEED0 + i)
    return list(rng.choice(tickers, size=KNAMES, replace=False))


# ---------------------------------------------------------------- fast metrics
def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, (r.mean() * 252.0) / vol if vol else np.nan, dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


# ---------------------------------------------------------------- ridge (idea 483's, verbatim)
def ridge_fit(X, y, lam):
    Xc = X - X.mean(0)
    yc = y - y.mean()
    A = Xc.T @ Xc + lam * np.eye(X.shape[1])
    return np.linalg.solve(A, Xc.T @ yc), y.mean(), X.mean(0)


def ridge_pred(X, b, ym, xm):
    return (X - xm) @ b + ym


def oof_pred(X, y, lam, K, seed=FOLD_SEED):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y))
    fold = np.zeros(len(y), int)
    for f, chunk in enumerate(np.array_split(idx, K)):
        fold[chunk] = f
    pred = np.empty(len(y))
    for f in range(K):
        tr, te = fold != f, fold == f
        b, ym, xm = ridge_fit(X[tr], y[tr], lam)
        pred[te] = ridge_pred(X[te], b, ym, xm)
    return pred


def r2_of(pred, y):
    y, pred = np.asarray(y, float), np.asarray(pred, float)
    den = ((y - y.mean()) ** 2).sum()
    return 1 - ((y - pred) ** 2).sum() / den if den > 0 else np.nan


def ols_t(x, y):
    """Idea 483's, verbatim."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    xc, yc = x - x.mean(), y - y.mean()
    if xc.std() == 0:
        return 0.0, 0.0, 0.0
    b = (xc @ yc) / (xc @ xc)
    resid = yc - b * xc
    n = len(x)
    se = np.sqrt((resid @ resid) / (n - 2) / (xc @ xc))
    return b, b / se if se else 0.0, 1 - (resid @ resid) / (yc @ yc)


def crossing(ns, vals, bar=BAR):
    """Largest n on the ladder where the curve is still BELOW the bar, interpolated in log n.

    Returns (n_star, status).  'never_below' = honest at every n on the ladder; 'never_above' =
    below the bar at every n, i.e. the control never learns its key on this ladder."""
    ns, vals = np.asarray(ns, float), np.asarray(vals, float)
    ok = np.isfinite(vals)
    ns, vals = ns[ok], vals[ok]
    if len(ns) < 2:
        return np.nan, "insufficient"
    if (vals >= bar).all():
        return np.nan, "never_below"
    if (vals < bar).all():
        return np.nan, "never_above"
    below = np.where(vals < bar)[0]
    i = below.max()
    if i == len(ns) - 1:
        return np.nan, "below_at_top"
    lo, hi = i, i + 1
    v0, v1 = vals[lo], vals[hi]
    if v1 == v0:
        return float(ns[hi]), "crossed"
    w = (bar - v0) / (v1 - v0)
    return float(np.exp(np.log(ns[lo]) + w * (np.log(ns[hi]) - np.log(ns[lo])))), "crossed"


# ---------------------------------------------------------------- per-panel build
def build_panel(pname, px):
    tickers = [c for c in px.columns if c != "SPY"]
    start = px.index[260]
    t0 = time.time()
    log(f"\n{'='*185}\nPANEL {pname}: {len(tickers)} names, {px.index[0].date()} -> "
        f"{px.index[-1].date()}, eval from {start.date()}")

    M = np.zeros((NMAX, len(tickers)))
    tix = {t: j for j, t in enumerate(tickers)}
    for i in range(NMAX):
        for t in draw_names(tickers, i):
            M[i, tix[t]] = 1.0

    # the 900 books are a pure function of (panel, SEED0, KNAMES, NMAX, the price cache), so they
    # are cached OUTSIDE the repo; delete the cache to force a rebuild.  Nothing else is cached.
    cache = CACHE / f"{pname}_{SEED0}_{KNAMES}_{NMAX}.npz"
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        R0 = pd.DataFrame(z["r"], index=pd.DatetimeIndex(z["idx"]))
        T0 = pd.DataFrame(z["t"], index=pd.DatetimeIndex(z["idx"]))
        log(f"  books read from cache {cache.name}")
    else:
        rets, turns = {}, {}
        for i in range(NMAX):
            nm = draw_names(tickers, i)
            sub = px[nm]                                 # G1 licenses this
            res = backtest(sub, ew_weights(sub, nm), cost_bps=0, freq=FREQ)   # G1b the ladder
            rets[i], turns[i] = res["returns"], res["turnover"]
        R0 = pd.DataFrame(rets).loc[start:]
        T0 = pd.DataFrame(turns).loc[start:]
        CACHE.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cache, r=R0.values, t=T0.values, idx=R0.index.values)
    R_by_rung = {c: R0 - T0 * c / 1e4 for c in RUNGS}     # exact, gated at G1b
    R = R_by_rung[COST]
    log(f"  {NMAX} draw books at {KNAMES} names, {FREQ}, t+1, cost ladder derived: "
        f"{time.time()-t0:.0f}s; R {R.shape}")

    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    h = len(R) // 2

    ann_all = (px[tickers].pct_change().loc[start:].mean() * 252).values
    ann_h1 = (px[tickers].pct_change().loc[start:].iloc[:h].mean() * 252).values
    ann_h2 = (px[tickers].pct_change().loc[start:].iloc[h:].mean() * 252).values

    n_nan = int(np.isnan(ann_all).sum())

    def keys(ann):
        """sd is idea 483's key VERBATIM (nanstd over members of the raw ann), so its rows
        reproduce.  mn is the EXACTLY-LINEAR control: NaN annualised returns are replaced by the
        panel's own cross-sectional mean first, so mn == (M @ ann0)/k identically (G4) whatever
        the NaN count.  The substitution touches only names with no return over the window."""
        sd = np.array([np.nanstd(ann[M[i] > 0]) for i in range(NMAX)])
        ann0 = np.where(np.isfinite(ann), ann, np.nanmean(ann))
        mn = (M @ ann0) / KNAMES
        return sd, mn, ann0

    sd_full, mn_full, ann0_full = keys(ann_all)
    sd_h1, mn_h1, _ = keys(ann_h1)
    sd_h2, mn_h2, _ = keys(ann_h2)

    y_full = np.array([fsharpe(R[c].values) for c in R.columns])

    return dict(name=pname, px=px, tickers=tickers, start=start, R=R, R_by_rung=R_by_rung, M=M,
                spy=spy, base=base, v1=v1, h=h, y_full=y_full,
                sd_full=sd_full, mn_full=mn_full, sd_h1=sd_h1, mn_h1=mn_h1,
                sd_h2=sd_h2, mn_h2=mn_h2, ann_all=ann_all, ann0_full=ann0_full, n_nan=n_nan)


def col_ladder(P):
    return sorted({p for p in PS if p <= P} | {P})


def sweep(P, M, targets, ns=NS, lams=LAMS, folds=FOLDS, tag=""):
    """REPRO_IS / REPRO_OOF over n x p x lam x K x target.  Columns are the most-drawn names
    first, so a p-subset is nested inside every wider one."""
    order = np.argsort(-M.sum(0), kind="stable")
    rows = []
    for p in col_ladder(P):
        cols = order[:p]
        for n in ns:
            X = M[:n, cols]
            for tname, tvec in targets.items():
                y = tvec[:n]
                if np.nanstd(y) == 0:
                    continue
                for lam in lams:
                    b, ym, xm = ridge_fit(X, y, lam)
                    r_is = r2_of(ridge_pred(X, b, ym, xm), y)
                    for K in folds:
                        if K > n:
                            continue
                        r_oof = r2_of(oof_pred(X, y, lam, K), y)
                        rows.append(dict(window=tag, p=p, n=n, p_over_n=p / n, target=tname,
                                         lam=lam, K=K, repro_IS=r_is, repro_OOF=r_oof))
    return pd.DataFrame(rows)


def main():
    T0 = time.time()
    log("=" * 185)
    log(f"Idea 498 is-p-over-n-1-the-crossover-for-key-reproduction (cloud) | {SCRIPT}")
    log("=" * 185)
    log("Object: REPRO_OOF = out-of-fold R^2 of a ridge on the MEMBERSHIP matrix M predicting the")
    log("  control's OWN key.  Keys: sd_i = std of member annualised returns (idea 83's, NONLINEAR")
    log("  in M) and mn_i = mean of member annualised returns (EXACTLY linear in M, the control).")
    log("Books: 900 equal-weight 20-name draws per panel, 10 bps, weekly, t+1, idea 483's seeds.")
    log(f"Tuned (2): DRAWS n in {NS}")
    log(f"           P     in {PS} + the full panel, nested by draw frequency.")
    log(f"Reported, NEVER tuned: lam {LAMS}, K {FOLDS}, target, panel, cost rung, sample half.")
    log(f"PRE-REGISTERED headline cell, fixed before any number is read: lam = {LAM_HEAD}, "
        f"K = {K_HEAD}, p = the full panel, target = sd.")
    log(f"PRE-REGISTERED Q1 bar: crossing p/n in [{CONFIRM_LO}, {CONFIRM_HI}] on ALL THREE panels")
    log(f"  = CONFIRMED; in [{PARTIAL_LO}, {PARTIAL_HI}] on all three = PARTIAL; else REFUTED "
        f"(a panel with no crossing at all is REFUTED).")

    # =================================================================== [0] gates
    log("\n" + "=" * 185)
    log("[0] REPRODUCTION GATES (all printed before any new number is read)")
    px0 = load_universe()
    tick0 = [c for c in px0.columns if c != "SPY"]
    g1 = g1b = 0.0
    for i in range(8):
        nm = draw_names(tick0, i)
        sub = px0[nm]
        for c in RUNGS:
            a = backtest(px0, ew_weights(px0, nm), cost_bps=c, freq=FREQ)["returns"]
            b = backtest(sub, ew_weights(sub, nm), cost_bps=c, freq=FREQ)["returns"]
            g1 = max(g1, float((a - b).abs().max()))
        z = backtest(sub, ew_weights(sub, nm), cost_bps=0, freq=FREQ)
        for c in RUNGS:
            live = backtest(sub, ew_weights(sub, nm), cost_bps=c, freq=FREQ)["returns"]
            g1b = max(g1b, float((live - (z["returns"] - z["turnover"] * c / 1e4)).abs().max()))
    log(f"  G1  sub-panel backtest == whole-panel backtest, 8 books x 3 rungs: max |diff| "
        f"{g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}  [the sweep's only speedup]")
    log(f"  G1b derived cost ladder r(c) = r0 - turnover*c/1e4 == a live costed backtest, same "
        f"books: max |diff| {g1b:.3e} (bar 1e-12) -> {'PASS' if g1b < 1e-12 else 'FAIL'}")

    rng0 = np.random.default_rng(498)
    r0 = backtest(px0, rules_v2_weights(px0), cost_bps=COST, freq=FREQ)["returns"]
    g5 = 0.0
    for _ in range(200):
        a, b = sorted(rng0.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        s = r0.iloc[a:b]
        mm, f = metrics(s), fmet(s.values)
        g5 = max(g5, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G5 fast metrics vs engine.metrics on 200 series: max |diff| {g5:.3e} (bar 1e-12) -> "
        f"{'PASS' if g5 < 1e-12 else 'FAIL'}")

    ps, ndrop = small_panel()
    log(f"  SMALL panel: dropped {ndrop} names with max_1d_move >= 1.0 -> {ps.shape[1]-1} names "
        f"+ SPY (idea 483's construction, so its rows join)")

    PAN = {}
    for nm, px in [("U56", px0), ("B136", load_universe(broad=True)), ("SMALL439", ps)]:
        PAN[nm] = build_panel(nm, px)

    log("\n" + "=" * 185)
    log("[0b] G2 / G3 / G4")
    g4, g4b = 0.0, 0.0
    for nm, D in PAN.items():
        g4 = max(g4, float(np.abs(D["mn_full"] - (D["M"] @ D["ann0_full"]) / KNAMES).max()))
        naive = np.array([np.nanmean(D["ann_all"][D["M"][i] > 0]) for i in range(NMAX)])
        g4b = max(g4b, float(np.abs(D["mn_full"] - naive).max()))
    log(f"  G4 mn is EXACTLY linear in M: max |mn - (M @ ann0)/k| = {g4:.3e} (bar 1e-12) -> "
        f"{'PASS' if g4 < 1e-12 else 'FAIL'}  [so Q3's control is linear by construction]")
    log("     names with no annualised return over the eval window, per panel (the only names the"
        " NaN substitution touches): "
        + ", ".join(f"{nm} {D['n_nan']}/{len(D['tickers'])}" for nm, D in PAN.items())
        + f"; max |mn(exact-linear) - mn(nanmean over members)| = {g4b:.3e}, i.e. the")
    log("     substitution is the whole difference and it is confined to books holding those"
        " names.")

    g2max, g3ok = np.nan, None
    if PARENT.exists():
        par = pd.read_csv(PARENT)
        log(f"  G2 source: idea 483 cloud {PARENT.name}, {len(par)} rows")
        mine = []
        for nm, D in PAN.items():
            P = len(D["tickers"])
            M200, y200, sd200 = D["M"][:200], D["y_full"][:200], D["sd_full"][:200]
            # idea 483 picked its 10 most-drawn names from ITS OWN 200-draw M, not from a
            # 900-draw pool, so the narrow subset must be rebuilt at n = 200 for its rows to join.
            order200 = np.argsort(-M200.sum(0))
            for width, cols in (("WIDE", np.arange(P)), ("NARROW10", order200[:10])):
                X = M200[:, cols]
                for lam in LAMS:
                    b, ym, xm = ridge_fit(X, y200, lam)
                    e_is = y200 - ridge_pred(X, b, ym, xm)
                    _, t_is, _ = ols_t(sd200, e_is)
                    bs, yms, xms = ridge_fit(X, sd200, lam)
                    r_is = r2_of(ridge_pred(X, bs, yms, xms), sd200)
                    for K in [2, 3, 5, 10]:
                        e_oof = y200 - oof_pred(X, y200, lam, K)
                        _, t_oof, _ = ols_t(sd200, e_oof)
                        r_oof = r2_of(oof_pred(X, sd200, lam, K), sd200)
                        mine.append(dict(panel=nm, width=width, lam=lam, K=K, m_t_is=t_is,
                                         m_t_oof=t_oof, m_sd_is=r_is, m_sd_oof=r_oof))
        mine = pd.DataFrame(mine)
        j = par.merge(mine, on=["panel", "width", "lam", "K"])
        dd = {"R2_control_reproduces_sd_insample":
              float((j["R2_control_reproduces_sd_insample"] - j["m_sd_is"]).abs().max()),
              "R2_control_reproduces_sd_oof":
              float((j["R2_control_reproduces_sd_oof"] - j["m_sd_oof"]).abs().max()),
              "t_insample": float((j["t_insample"] - j["m_t_is"]).abs().max()),
              "t_oof": float((j["t_oof"] - j["m_t_oof"]).abs().max())}
        g2max = max(dd.values())
        log(f"     joined {len(j)} of {len(par)} committed rows on panel x width x lam x K")
        log("     max |diff|: " + "  ".join(f"{k} {v:.3e}" for k, v in dd.items()))
        log(f"  -> G2 {'PASS' if (g2max < 1e-9 and len(j) == len(par)) else 'FAIL'} (bar 1e-9)")

        log("  G3 the queue's quoted triple.  PROVENANCE, stated once: 0.939 / 0.668 / 0.315 is")
        log("     idea 483's MEDIAN over its own 6 lam x 4 K grid at WIDE and n=200, not a single")
        log("     cell - its per-panel MAX is 0.9545 / 0.8772 / 0.4546, a materially different")
        log("     reading, and the spread over that grid is what this run's lam/K table exposes.")
        g3ok = True
        for nm in ["U56", "B136", "SMALL439"]:
            s = j[(j["panel"] == nm) & (j["width"] == "WIDE")]
            got = float(s["m_sd_oof"].median())
            P = len(PAN[nm]["tickers"])
            ok = abs(got - PUB483[nm]) < 5e-4
            g3ok &= ok
            log(f"     {nm:9s} p={P:4d} n=200 p/n {P/200:.3f}  median {got:.4f} (published "
                f"{PUB483[nm]:.4f}) | max {float(s['m_sd_oof'].max()):.4f} | min "
                f"{float(s['m_sd_oof'].min()):.4f} -> {'PASS' if ok else 'FAIL'}")
        log(f"  -> G3 {'PASS' if g3ok else 'FAIL'}")
    else:
        log("  G2/G3 source: idea 483 cloud .grid.csv NOT FOUND -> G2/G3 cannot run")

    # =============================================================== [1] Q1 the sweep
    log("\n" + "=" * 185)
    log("[1] Q1 - THE SWEEP.  REPRO_OOF over n x p x lam x K x target, per panel, ALL reported.")
    G = []
    for nm, D in PAN.items():
        g = sweep(len(D["tickers"]), D["M"],
                  {"sd": D["sd_full"], "mn": D["mn_full"]}, tag="FULL")
        g["panel"] = nm
        G.append(g)
    G = pd.concat(G, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False)
    log(f"    {len(G)} grid points written to {STEM}.grid.csv.gz")

    head = G[(G["lam"] == LAM_HEAD) & (G["K"] == K_HEAD) & (G["target"] == "sd")]
    log(f"\n    THE HEADLINE SURFACE (lam {LAM_HEAD}, K {K_HEAD}, target sd): REPRO_OOF by n "
        f"(rows) x p (cols), per panel.  The full panel's p is the rightmost column.")
    for nm, D in PAN.items():
        P = len(D["tickers"])
        sub = head[head["panel"] == nm]
        log(f"\n    {nm} (full panel p = {P}):")
        log(sub.pivot_table(index="n", columns="p", values="repro_OOF").to_string(
            float_format=lambda x: f"{x:+.4f}"))
        log(f"      in-sample, same cells (the number the record publishes):")
        log(sub.pivot_table(index="n", columns="p", values="repro_IS").to_string(
            float_format=lambda x: f"{x:+.4f}"))

    log(f"\n    CROSSINGS: the n at which REPRO_OOF crosses {BAR:.2f}, read in p/n, "
        f"every p and both targets at the headline lam/K.")
    cross = []
    for nm, D in PAN.items():
        P = len(D["tickers"])
        for tgt in ["sd", "mn"]:
            for p in col_ladder(P):
                s = G[(G["panel"] == nm) & (G["lam"] == LAM_HEAD) & (G["K"] == K_HEAD)
                      & (G["target"] == tgt) & (G["p"] == p)].sort_values("n")
                nstar, status = crossing(s["n"].values, s["repro_OOF"].values)
                cross.append(dict(panel=nm, target=tgt, p=p, n_star=nstar,
                                  p_over_n_star=(p / nstar) if np.isfinite(nstar) else np.nan,
                                  status=status, is_full_panel=(p == P),
                                  repro_at_nmax=float(s["repro_OOF"].iloc[-1]),
                                  repro_at_nmin=float(s["repro_OOF"].iloc[0])))
    cross = pd.DataFrame(cross)
    cross.to_csv(OUT / f"{STEM}.crossings.csv", index=False)
    log(cross.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    hc = cross[(cross["target"] == "sd") & cross["is_full_panel"]].set_index("panel")
    log("\n    the pre-registered reading (target sd, p = the full panel, headline lam/K):")
    vals = {}
    for nm in ["U56", "B136", "SMALL439"]:
        r = hc.loc[nm]
        vals[nm] = float(r["p_over_n_star"])
        log(f"      {nm:9s} p={int(r['p']):4d}  crossing n* {r['n_star']:8.1f}  -> p/n* "
            f"**{r['p_over_n_star']:.3f}**   status {r['status']}   REPRO_OOF at n=900 "
            f"{r['repro_at_nmax']:+.4f}, at n=30 {r['repro_at_nmin']:+.4f}")
    fin_ok = all(np.isfinite(v) for v in vals.values())
    conf = fin_ok and all(CONFIRM_LO <= v <= CONFIRM_HI for v in vals.values())
    part = fin_ok and all(PARTIAL_LO <= v <= PARTIAL_HI for v in vals.values())
    verdict_q1 = "CONFIRMED" if conf else ("PARTIAL" if part else "REFUTED")
    log(f"    -> pre-registered Q1 verdict: **{verdict_q1}**  "
        f"(bars [{CONFIRM_LO}, {CONFIRM_HI}] / [{PARTIAL_LO}, {PARTIAL_HI}])")

    log("\n    the same crossing at EVERY lam and K (reported axes, never tuned) - is the")
    log("    crossing a property of the design or of the penalty?")
    stab = []
    for nm, D in PAN.items():
        P = len(D["tickers"])
        for lam in LAMS:
            for K in FOLDS:
                s = G[(G["panel"] == nm) & (G["lam"] == lam) & (G["K"] == K)
                      & (G["target"] == "sd") & (G["p"] == P)].sort_values("n")
                nstar, status = crossing(s["n"].values, s["repro_OOF"].values)
                stab.append(dict(panel=nm, lam=lam, K=K,
                                 p_over_n_star=(P / nstar) if np.isfinite(nstar) else np.nan,
                                 status=status))
    stab = pd.DataFrame(stab)
    stab.to_csv(OUT / f"{STEM}.lamK.csv", index=False)
    log(stab.pivot_table(index=["panel", "lam"], columns="K", values="p_over_n_star").to_string(
        float_format=lambda x: f"{x:.3f}"))
    ok = stab["p_over_n_star"].notna()
    log(f"    crossings that exist at all: {int(ok.sum())} of {len(stab)}; where they exist, "
        f"p/n* spans {stab.loc[ok,'p_over_n_star'].min():.3f} to "
        f"{stab.loc[ok,'p_over_n_star'].max():.3f} (median "
        f"{stab.loc[ok,'p_over_n_star'].median():.3f})")
    for nm in ["U56", "B136", "SMALL439"]:
        s = stab[(stab["panel"] == nm) & stab["p_over_n_star"].notna()]
        if len(s):
            log(f"      {nm:9s} n={len(s):2d}/24 cells cross; p/n* {s['p_over_n_star'].min():.3f}"
                f" - {s['p_over_n_star'].max():.3f}, median {s['p_over_n_star'].median():.3f}")
        else:
            log(f"      {nm:9s} 0/24 cells cross on this ladder")

    # =============================================================== [2] Q2 is p/n the axis
    log("\n" + "=" * 185)
    log("[2] Q2 - IS p/n THE AXIS?  If it is, cells with the same p/n agree whatever (n, p) made")
    log("    it.  REPRO_OOF binned by p/n decade, headline lam/K, target sd, ALL panels:")
    hs = G[(G["lam"] == LAM_HEAD) & (G["K"] == K_HEAD) & (G["target"] == "sd")].copy()
    edges = [0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.5, 4.0, 8.0, 1e9]
    hs["band"] = pd.cut(hs["p_over_n"], edges)
    bt = hs.groupby("band", observed=True).agg(
        n_cells=("repro_OOF", "size"), mean=("repro_OOF", "mean"), sd=("repro_OOF", "std"),
        lo=("repro_OOF", "min"), hi=("repro_OOF", "max"))
    bt["spread"] = bt["hi"] - bt["lo"]
    log(bt.to_string(float_format=lambda x: f"{x:+.4f}"))
    within = float(bt["spread"].max())
    log(f"    worst within-band spread of REPRO_OOF: {within:.4f}.  For p/n to be THE axis this")
    log("    must be small next to the range the statistic covers over the whole grid "
        f"({hs['repro_OOF'].min():+.4f} to {hs['repro_OOF'].max():+.4f}).")
    log("\n    the same question asked directly: REPRO_OOF at FIXED p/n ~ 1, every way of making it")
    near = hs[(hs["p_over_n"] >= 0.8) & (hs["p_over_n"] <= 1.25)]
    log(near[["panel", "p", "n", "p_over_n", "repro_IS", "repro_OOF"]].sort_values(
        ["panel", "p_over_n"]).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== [3] Q3 the control
    log("\n" + "=" * 185)
    log("[3] Q3 - THE POSITIVE CONTROL.  `mn` is EXACTLY linear in M (G4 {:.1e}).  If p/n is the"
        .format(g4))
    log("    axis, sd and mn cross together.  If mn is reproduced everywhere while sd is not, the")
    log("    crossing is the NONLINEARITY and p/n is the wrong thing to publish.")
    for nm, D in PAN.items():
        P = len(D["tickers"])
        s = G[(G["panel"] == nm) & (G["lam"] == LAM_HEAD) & (G["K"] == K_HEAD)
              & (G["p"] == P)].pivot_table(index="n", columns="target", values="repro_OOF")
        s["p_over_n"] = P / s.index
        log(f"\n    {nm} (p = {P}), REPRO_OOF by n:")
        log(s[["p_over_n", "sd", "mn"]].to_string(float_format=lambda x: f"{x:+.4f}"))
    mc = cross[(cross["target"] == "mn") & cross["is_full_panel"]].set_index("panel")
    log("\n    crossings side by side (target sd vs mn, full panel, headline lam/K):")
    for nm in ["U56", "B136", "SMALL439"]:
        log(f"      {nm:9s} sd p/n* {hc.loc[nm,'p_over_n_star']:8.3f} ({hc.loc[nm,'status']})"
            f"   |   mn p/n* {mc.loc[nm,'p_over_n_star']:8.3f} ({mc.loc[nm,'status']})"
            f"   |   mn REPRO_OOF at n=900 {mc.loc[nm,'repro_at_nmax']:+.4f}")
    log("\n    the ceiling question: REPRO_OOF at the largest n on the ladder, both targets, all p")
    ceil = G[(G["lam"] == LAM_HEAD) & (G["K"] == K_HEAD) & (G["n"] == max(NS))]
    log(ceil.pivot_table(index=["panel", "p"], columns="target", values="repro_OOF").to_string(
        float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== [4] Q4 rule 8
    log("\n" + "=" * 185)
    log("[4] Q4 - RULE 8.  The key is rebuilt on the FIRST half of each panel's sample alone, the")
    log("    crossing is located there, and the SECOND half is read ONCE at that crossing.")
    wf = []
    for nm, D in PAN.items():
        P = len(D["tickers"])
        for tag, sdv, mnv in (("H1", D["sd_h1"], D["mn_h1"]), ("H2", D["sd_h2"], D["mn_h2"])):
            g = sweep(P, D["M"], {"sd": sdv, "mn": mnv}, lams=[LAM_HEAD], folds=[K_HEAD], tag=tag)
            g["panel"] = nm
            wf.append(g)
    wf = pd.concat(wf, ignore_index=True)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    wfrows = []
    for nm, D in PAN.items():
        P = len(D["tickers"])
        r = {}
        for tag in ("H1", "H2"):
            s = wf[(wf["panel"] == nm) & (wf["window"] == tag) & (wf["target"] == "sd")
                   & (wf["p"] == P)].sort_values("n")
            ns_, st = crossing(s["n"].values, s["repro_OOF"].values)
            r[tag] = (P / ns_ if np.isfinite(ns_) else np.nan, st, ns_,
                      float(s["repro_OOF"].iloc[-1]))
        wfrows.append(dict(panel=nm, p=P, H1_p_over_n=r["H1"][0], H1_status=r["H1"][1],
                           H2_p_over_n=r["H2"][0], H2_status=r["H2"][1],
                           IS_pick_n=r["H1"][2],
                           H1_repro_nmax=r["H1"][3], H2_repro_nmax=r["H2"][3]))
    wfr = pd.DataFrame(wfrows)
    log(wfr.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    both = wfr[["H1_p_over_n", "H2_p_over_n"]].notna().all(axis=1)
    if both.any():
        d = (wfr.loc[both, "H2_p_over_n"] - wfr.loc[both, "H1_p_over_n"]).abs()
        rat = (wfr.loc[both, "H2_p_over_n"] / wfr.loc[both, "H1_p_over_n"])
        log(f"    crossings that exist in BOTH halves: {int(both.sum())} of 3; |H2 - H1| max "
            f"{float(d.max()):.3f}, H2/H1 ratio {', '.join(f'{v:.3f}' for v in rat)}")
    else:
        log("    no panel produces a crossing in both halves -> the crossing does not walk forward")

    log("\n    and the book-level rule-8 selector chooser: pick on the first half, read OOS once.")
    sel = []
    for nm, D in PAN.items():
        P = len(D["tickers"])
        R = D["R"]
        h = D["h"]
        y_is = np.array([fsharpe(R[c].values[:h]) for c in R.columns])
        oos = {c: R[c].values[h:] for c in R.columns}
        cols = np.arange(P)
        X = D["M"][:, cols]
        e_is = y_is - ridge_pred(X, *ridge_fit(X, y_is, LAM_HEAD))
        e_oof = y_is - oof_pred(X, y_is, LAM_HEAD, K_HEAD)
        cands = {"S_RAW_IS_SHARPE": y_is, "S_RESID_INSAMPLE": e_is, "S_RESID_OOF": e_oof,
                 "S_SD_ONLY": -D["sd_full"]}
        spy_o = D["spy"].values[h:]
        b_o = D["base"].values[h:]
        for snm, sc in cands.items():
            i = int(np.nanargmax(sc))
            c, s, dd = fmet(oos[list(R.columns)[i]])
            sel.append(dict(panel=nm, selector=snm, pick=i, OOS_CAGR=c, OOS_Sharpe=s,
                            OOS_MaxDD=dd,
                            mean_draw=float(np.nanmean([fsharpe(v) for v in oos.values()])),
                            base_v2=fsharpe(b_o), SPY=fsharpe(spy_o),
                            beats_v2=bool(s > fsharpe(b_o)), beats_spy=bool(s > fsharpe(spy_o))))
    sel = pd.DataFrame(sel)
    sel.to_csv(OUT / f"{STEM}.selectors.csv", index=False)
    log(sel.set_index(["panel", "selector"]).to_string(float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== [5] Q5 PROTOCOL
    log("\n" + "=" * 185)
    log("[5] Q5 - PROTOCOL.  Both KEEP paths on every draw book at rungs 0/10/25, vs the LIVE")
    log("    RULES v2 baseline and SPY.")
    kp = []
    for nm, D in PAN.items():
        spy = D["spy"].values
        h = D["h"]
        sc, ss, sdd = fmet(spy)
        s1, s2 = fsharpe(spy[:h]), fsharpe(spy[h:])
        so = fsharpe(spy[h:])
        for c in RUNGS:
            Rr = D["R_by_rung"][c]
            bb = backtest(D["px"], rules_v2_weights(D["px"]), cost_bps=c,
                          freq=FREQ)["returns"].loc[D["start"]:].values
            b1, b2, bdd = fsharpe(bb[:h]), fsharpe(bb[h:]), fmet(bb)[2]
            for col in Rr.columns:
                r = Rr[col].values
                cg, sh, dd = fmet(r)
                p1, p2 = fsharpe(r[:h]), fsharpe(r[h:])
                po = fsharpe(r[h:])
                t4b = dict(H1=p1 > s1, H2=p2 > s2, OOS=po > so,
                           DD=abs(dd) <= 0.60 * abs(sdd), CAGR=cg >= 0.70 * sc)
                kp.append(dict(panel=nm, rung=c, book=int(col), CAGR=cg, Sharpe=sh, MaxDD=dd,
                               H1=p1, H2=p2, OOS_Sharpe=po,
                               p4a=bool(p1 > b1 and p2 > b2 and dd >= bdd), p4b=all(t4b.values()),
                               fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))
    kp = pd.DataFrame(kp)
    kp.to_csv(OUT / f"{STEM}.keeppaths.csv.gz", index=False)
    log("    4a passes: " + "  ".join(
        f"{c:.0f}bps {int(kp[kp['rung']==c]['p4a'].sum())}/{int((kp['rung']==c).sum())}"
        for c in RUNGS))
    log("    4b passes: " + "  ".join(
        f"{c:.0f}bps {int(kp[kp['rung']==c]['p4b'].sum())}/{int((kp['rung']==c).sum())}"
        for c in RUNGS))
    hh = kp[kp["rung"] == RUNG_HEAD]
    log(f"    at PROTOCOL's own {RUNG_HEAD:.0f} bps: 4a {int(hh['p4a'].sum())}, 4b "
        f"{int(hh['p4b'].sum())} of {len(hh)}, BOTH {int((hh['p4a'] & hh['p4b']).sum())}; "
        f"by panel 4b " + "  ".join(
            f"{p} {int(hh[hh['panel']==p]['p4b'].sum())}/{int((hh['panel']==p).sum())}"
            for p in ["U56", "B136", "SMALL439"]))
    log("    dominant 4b failure legs at 10 bps: "
        + ", ".join(f"{k} {v}" for k, v in hh["fail4b"].value_counts().head(4).items()))

    log("\n    PROTOCOL rule 3/4 reference table at 10 bps (full, halves, second half):")
    rr = []
    for nm, D in PAN.items():
        h = D["h"]
        for lab, v in (("RULES v2 (live)", D["base"].values), ("RULES v1", D["v1"].values),
                       ("SPY", D["spy"].values),
                       ("mean draw book", D["R"].mean(axis=1).values)):
            c, s, dd = fmet(v)
            rr.append(dict(panel=nm, ref=lab, CAGR=c, Sharpe=s, MaxDD=dd,
                           H1=fsharpe(v[:h]), H2=fsharpe(v[h:]), OOS_CAGR=fmet(v[h:])[0],
                           OOS_Sharpe=fsharpe(v[h:]), OOS_MaxDD=fmet(v[h:])[2]))
    rr = pd.DataFrame(rr)
    rr.to_csv(OUT / f"{STEM}.refs.csv", index=False)
    log(rr.set_index(["panel", "ref"]).to_string(float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== [6] summary
    log("\n" + "=" * 185)
    log("[6] SUMMARY")
    log(f"  gates: G1 {g1:.2e} | G1b {g1b:.2e} | G2 {g2max:.2e} | G3 {'PASS' if g3ok else g3ok} | G4 {g4:.2e} | "
        f"G5 {g5:.2e}")
    log("  Q1 crossing p/n at the pre-registered headline (sd, full panel, lam 1.0, K 10): "
        + "  ".join(f"{k} {v:.3f}" for k, v in vals.items()) + f"  -> **{verdict_q1}**")
    log(f"  Q2 worst within-p/n-band spread of REPRO_OOF {within:.4f} against a grid range "
        f"{hs['repro_OOF'].min():+.4f}..{hs['repro_OOF'].max():+.4f}")
    log("  Q3 control: mn (exactly linear) crossings " + "  ".join(
        f"{nm} {mc.loc[nm,'p_over_n_star']:.3f}/{mc.loc[nm,'status']}"
        for nm in ["U56", "B136", "SMALL439"]))
    log(f"  Q4 rule 8: crossing exists in both halves on {int(both.sum())} of 3 panels")
    log(f"  Q5 4a {int(hh['p4a'].sum())} / 4b {int(hh['p4b'].sum())} of {len(hh)} at 10 bps; "
        f"selectors beating RULES v2 OOS {int(sel['beats_v2'].sum())}/{len(sel)}, SPY "
        f"{int(sel['beats_spy'].sum())}/{len(sel)}")
    log("  Nothing promoted; no RULES change proposed by this run.")
    log("  SURVIVORSHIP: three current-constituent panels; the object is a within-panel")
    log("  reproduction R^2, which a common level shift does not move.")
    log(f"  runtime {time.time()-T0:.0f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.{{grid,crossings,lamK,walkforward,selectors,keeppaths,refs,console}}")


if __name__ == "__main__":
    main()
