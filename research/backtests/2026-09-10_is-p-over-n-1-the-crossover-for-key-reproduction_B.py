#!/usr/bin/env python3
"""Idea 498 — is p/n = 1 the crossover for KEY REPRODUCTION?

Idea 483 measured out-of-fold reproduction of the wide control's own key at
R2 0.939 / 0.668 / 0.315 for p/n 0.28 / 0.68 / 2.20 (p = 56 / 136 / 439 names,
n = 200 draws) and called it "monotone in p/n".  Three panels is three points.
This run sweeps p/n finely, by varying BOTH the draw count n and the design
width p, and asks where honest (out-of-fold) reproduction falls below 0.5 —
i.e. where a wide control stops being a control.

Design (the two tuned parameters are exactly the ones the queue names: DRAWS n
and WIDTH p; the ridge penalty lam and fold count K are inherited from idea 483
and are swept without selection, every point reported):

  KEY 1  sd   — cross-sectional dispersion of member annualised returns.  This is
                the record's actual key (idea 83 / 252 / 483).  It is NOT a linear
                function of membership, so its reproduction has a ceiling below 1
                even at n = infinity.
  KEY 2  mu   — mean member annualised return = M @ ann / k.  EXACTLY linear in the
                full-width membership matrix, so at p = N its only obstacle is p/n.
                This is the positive control that separates "the control is too wide
                for the sample" from "the key was never in the column space".
  KEY 3  yS   — the draw book's own full-sample Sharpe (the outcome idea 483 fitted).

  Draws are NESTED: one seeded stream of MAXDRAW books per panel, and n = the first
  n of them, so the sweep is monotone and comparable across n.

  Pre-registered before looking: if the crossover is a pure width effect it should
  sit at p/n_train = 1, where n_train = n(1 - 1/K) is what the fold actually fits on,
  NOT at p/n = 1.  That predicts p/n* = (K-1)/K — 0.50 at K=2, 0.80 at K=5, 0.90 at
  K=10 — and the record's "p/n = 1" would be wrong by the fold count.

Gate: n = 200, full width, medians over lam x K must reproduce idea 483's
0.939 / 0.668 / 0.315.

Rule 8 walk-forward: every selector is fitted on the FIRST half of the sample and
evaluated on the SECOND, untouched.  Both KEEP paths (4a vs live RULES v2, 4b vs SPY)
are evaluated for every draw book.

Costs 10 bps, weekly, weights decided at t applied at t+1.  No network.
SURVIVORSHIP: broad136 and the sub-$2B panel are current constituents only.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-10_is-p-over-n-1-the-crossover-for-key-reproduction_B"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"
KNAMES = 20                                   # names per draw book (idea 483's)
MAXDRAW = 1200                                # nested draw stream per panel
NGRID = [30, 40, 50, 60, 80, 100, 125, 150, 200, 250, 300, 400, 500, 700, 900, 1200]
LAMS = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]   # idea 483's, swept not selected
FOLDS = [2, 3, 5, 10]                         # idea 483's, swept not selected
LAM0, K0 = 1.0, 5                             # pinned headline cell (mid of each list)
PGRID_FRAC = [10, 25, 50, 100]                # narrow widths, plus full width N
THRESH = 0.5                                  # the queue's "stops being a control" line

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ------------------------------------------------------------------ panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]

def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

# ------------------------------------------------------------------ fast books
def ew_weights(px, names, gross=1.0):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[names].notna().astype(float)
    w[names] = gross * sub.div(sub.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w

def fast_books(px, idx_mat):
    """Exact numpy re-implementation of engine.backtest for equal-weight k-name books,
    run for all draws at once.  Identical arithmetic to the engine loop restricted to the
    held columns (weights are zero elsewhere, so the restriction is exact).  Gated against
    engine.backtest in main()."""
    rets = px.pct_change().fillna(0.0).values                     # (T, N)
    notna = px.notna().values.astype(float)                       # (T, N)
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    D, k = idx_mat.shape
    T = len(px)
    cur = np.zeros((D, k)); port = np.zeros((T, D))
    # target weights decided at t applied at t+1: w_target[i] = ew(t=i-1)
    for i in range(T):
        if mask[i] or i == 0:
            j = max(i - 1, 0)
            live = notna[j][idx_mat]                              # (D, k)
            s = live.sum(axis=1)
            new = np.where(s[:, None] > 0, live / np.where(s[:, None] == 0, 1, s[:, None]), 0.0)
            if i == 0: new = np.zeros((D, k))                     # engine: w_target row 0 is NaN->0
            to = np.abs(new - cur).sum(axis=1); cur = new
        else:
            to = np.zeros(D)
        r = rets[i][idx_mat]                                      # (D, k)
        port[i] = (cur * r).sum(axis=1) - to * COST / 1e4
        growth = cur * (1 + r)
        tot = growth.sum(axis=1) + (1 - cur.sum(axis=1))
        cur = np.where(tot[:, None] > 0, growth / np.where(tot[:, None] == 0, 1, tot[:, None]), cur)
    return pd.DataFrame(port, index=px.index)

# ------------------------------------------------------------------ ridge
def eig_solve(G, C, lam):
    """(G + lam I)^-1 C for a symmetric PSD G, via one eigendecomposition reused over lam."""
    d, V = G
    return V @ ((V.T @ C) / (d + lam)[:, None])

def oof_r2(X, Y, lam_list, K, seed=7):
    """Out-of-fold R2 of each column of Y on X (ridge, centred), for every lam.
    Returns array (len(lam_list), Y.shape[1]).  One eigendecomposition per fold."""
    n = X.shape[0]
    rng = np.random.default_rng(seed)
    order = rng.permutation(n); fold = np.zeros(n, int)
    for f, chunk in enumerate(np.array_split(order, K)): fold[chunk] = f
    pred = np.zeros((len(lam_list), n, Y.shape[1]))
    for f in range(K):
        tr, te = fold != f, fold == f
        Xtr, Ytr = X[tr], Y[tr]
        xm, ym = Xtr.mean(0), Ytr.mean(0)
        Xc, Yc = Xtr - xm, Ytr - ym
        d, V = np.linalg.eigh(Xc.T @ Xc)
        d = np.clip(d, 0, None)
        C = Xc.T @ Yc
        VtC = V.T @ C
        Xte = X[te] - xm
        for li, lam in enumerate(lam_list):
            B = V @ (VtC / (d + lam)[:, None])
            pred[li, te] = Xte @ B + ym
    ss_tot = ((Y - Y.mean(0)) ** 2).sum(0)
    out = np.zeros((len(lam_list), Y.shape[1]))
    for li in range(len(lam_list)):
        out[li] = 1 - ((Y - pred[li]) ** 2).sum(0) / np.where(ss_tot == 0, np.nan, ss_tot)
    return out

def insample_r2(X, Y, lam_list):
    xm, ym = X.mean(0), Y.mean(0)
    Xc, Yc = X - xm, Y - ym
    d, V = np.linalg.eigh(Xc.T @ Xc); d = np.clip(d, 0, None)
    VtC = V.T @ (Xc.T @ Yc)
    ss_tot = (Yc ** 2).sum(0)
    out = np.zeros((len(lam_list), Y.shape[1]))
    for li, lam in enumerate(lam_list):
        P = Xc @ (V @ (VtC / (d + lam)[:, None])) + ym
        out[li] = 1 - ((Y - P) ** 2).sum(0) / np.where(ss_tot == 0, np.nan, ss_tot)
    return out

def crossover(pn, r2, thresh=THRESH):
    """First p/n at which r2 crosses below thresh, linear in log(p/n).  pn ascending."""
    pn = np.asarray(pn, float); r2 = np.asarray(r2, float)
    ok = np.isfinite(r2)
    pn, r2 = pn[ok], r2[ok]
    if len(pn) < 2: return np.nan
    if r2[0] < thresh: return np.nan          # already below at the smallest p/n
    if r2[-1] >= thresh: return np.nan        # never crosses inside the swept range
    for i in range(1, len(pn)):
        if r2[i] < thresh <= r2[i - 1]:
            x0, x1 = np.log(pn[i - 1]), np.log(pn[i]); y0, y1 = r2[i - 1], r2[i]
            if y0 == y1: return float(pn[i])
            return float(np.exp(x0 + (thresh - y0) * (x1 - x0) / (y1 - y0)))
    return np.nan

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {STAMP}")
    say("Idea 498: sweep p/n finely and locate where out-of-fold KEY REPRODUCTION < 0.5.")
    say("Tuned params: DRAWS n and WIDTH p.  lam and K inherited from idea 483, swept, all reported.")
    say(f"Pre-registered: a pure width effect crosses at p/n_train = 1, i.e. p/n* = (K-1)/K "
        f"= {', '.join(f'{(k-1)/k:.2f} at K={k}' for k in FOLDS)} — not at p/n = 1.\n")

    rows, wf, keeps, gate_rows, ceil_rows = [], [], [], [], []

    for pname, px in panels().items():
        tickers = [c for c in px.columns if c != "SPY"]
        N = len(tickers)
        tix = {t: j for j, t in enumerate(tickers)}
        say(f"## Panel {pname}: N={N} names, {px.index[0].date()}..{px.index[-1].date()}")

        # ---- nested draw stream ---------------------------------------
        idx_mat = np.zeros((MAXDRAW, KNAMES), int)
        for i in range(MAXDRAW):
            rng = np.random.default_rng(i)
            idx_mat[i] = rng.choice(N, size=KNAMES, replace=False)
        M = np.zeros((MAXDRAW, N))
        np.put_along_axis(M, idx_mat, 1.0, axis=1)

        # ---- books (fast path, gated against the engine) ---------------
        tg = time.time()
        col_of = np.array([px.columns.get_loc(t) for t in tickers])   # ticker slot -> px column slot
        R = fast_books(px, col_of[idx_mat])
        gate_err = 0.0
        gstart = px.index[260]
        for i in (0, 1, 7, 33, 199):
            names = [tickers[j] for j in idx_mat[i]]
            eng = backtest(px, ew_weights(px, names), cost_bps=COST, freq=FREQ)["returns"].loc[gstart:]
            gate_err = max(gate_err, float(np.abs(eng.values - R[i].loc[gstart:].values).max()))
        say(f"fast-book gate vs engine.backtest on 5 draws, over the evaluated window (from index 260, "
            f"the same warm-up skip idea 483 uses): max |d daily return| = {gate_err:.3e} "
            f"({MAXDRAW} books in {time.time()-tg:.0f}s)")
        say("  (the engine's first rows before the first weekly rebalance are NaN by construction — "
            "w_target.shift(1) row 0 — and are outside the evaluated window; the two paths coincide "
            "exactly from the first rebalance onward.)")
        gate_rows.append(dict(panel=pname, gate_max_abs_daily_return_diff=gate_err))
        assert gate_err < 1e-12, "fast book path does not reproduce the engine"

        start = px.index[260]
        R = R.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        h = len(R) // 2
        IS, OOS = R.iloc[:h], R.iloc[h:]

        # ---- keys ------------------------------------------------------
        pc = px[tickers].pct_change().loc[start:]
        ann = (pc.mean() * 252).values
        ann_is = (pc.iloc[:h].mean() * 252).values
        memb = M > 0
        sd_full = np.array([np.nanstd(ann[memb[i]]) for i in range(MAXDRAW)])
        mu_full = np.array([np.nanmean(ann[memb[i]]) for i in range(MAXDRAW)])
        sd_is = np.array([np.nanstd(ann_is[memb[i]]) for i in range(MAXDRAW)])
        yS = np.array([metrics(R[c])["Sharpe"] for c in R.columns])
        y_is = np.array([metrics(IS[c])["Sharpe"] for c in IS.columns])
        y_oos = np.array([metrics(OOS[c])["Sharpe"] for c in OOS.columns])
        cagr_oos = np.array([metrics(OOS[c])["CAGR"] for c in OOS.columns])
        dd_oos = np.array([metrics(OOS[c])["MaxDD"] for c in OOS.columns])
        KEYS = {"sd": sd_full, "mu": mu_full, "yS": yS}
        Yall = np.column_stack([KEYS[k] for k in ("sd", "mu", "yS")])

        # ---- the sweep -------------------------------------------------
        perm = np.random.default_rng(4242).permutation(N)
        widths = sorted({min(w, N) for w in PGRID_FRAC} | {N})
        for p in widths:
            cols = perm[:p]
            for K in FOLDS:
                for n in NGRID:
                    if n < 2 * K: continue
                    X = M[:n][:, cols]
                    Y = Yall[:n]
                    r2o = oof_r2(X, Y, LAMS, K)
                    r2i = insample_r2(X, Y, LAMS)
                    for li, lam in enumerate(LAMS):
                        for ki, kn in enumerate(("sd", "mu", "yS")):
                            rows.append(dict(panel=pname, N=N, p=p, n=n, pn=p / n,
                                             pn_train=p / (n * (1 - 1 / K)), K=K, lam=lam, key=kn,
                                             full_width=(p == N),
                                             R2_oof=r2o[li, ki], R2_insample=r2i[li, ki]))

        # ---- ceiling: how much of each key is linearly recoverable at all
        for K in FOLDS:
            X = M[:MAXDRAW][:, perm[:N]]
            r2o = oof_r2(X, Yall, LAMS, K)
            for li, lam in enumerate(LAMS):
                for ki, kn in enumerate(("sd", "mu", "yS")):
                    ceil_rows.append(dict(panel=pname, K=K, lam=lam, key=kn, n=MAXDRAW,
                                          pn=N / MAXDRAW, R2_oof=r2o[li, ki]))

        # ---- rule 8: selectors fitted on the FIRST half, evaluated on the SECOND
        for n in (100, 200, 500, 1200):
            X = M[:n]
            for lam in LAMS:
                for K in FOLDS:
                    if n < 2 * K: continue
                    yi = y_is[:n]
                    pin = insample_r2(X, yi[:, None], [lam])  # noqa: kept for symmetry
                    xm, ym = X.mean(0), yi.mean()
                    Xc = X - xm
                    d, V = np.linalg.eigh(Xc.T @ Xc); d = np.clip(d, 0, None)
                    b = V @ ((V.T @ (Xc.T @ (yi - ym))) / (d + lam))
                    resid_is = yi - (Xc @ b + ym)
                    predo = np.zeros(n)
                    rng = np.random.default_rng(7); order = rng.permutation(n)
                    fold = np.zeros(n, int)
                    for f, ch in enumerate(np.array_split(order, K)): fold[ch] = f
                    for f in range(K):
                        tr, te = fold != f, fold == f
                        xm2, ym2 = X[tr].mean(0), yi[tr].mean()
                        Xc2 = X[tr] - xm2
                        d2, V2 = np.linalg.eigh(Xc2.T @ Xc2); d2 = np.clip(d2, 0, None)
                        b2 = V2 @ ((V2.T @ (Xc2.T @ (yi[tr] - ym2))) / (d2 + lam))
                        predo[te] = (X[te] - xm2) @ b2 + ym2
                    resid_oof = yi - predo
                    sel = {"S_RAW_IS_SHARPE": int(np.argmax(yi)),
                           "S_RESID_INSAMPLE": int(np.argmax(resid_is)),
                           "S_RESID_OOF": int(np.argmax(resid_oof)),
                           "S_SD_ONLY": int(np.argmax(sd_is[:n]))}
                    for sname, i in sel.items():
                        wf.append(dict(panel=pname, n=n, lam=lam, K=K, selector=sname, draw=i,
                                       IS_Sharpe=y_is[i], OOS_Sharpe=y_oos[i], OOS_CAGR=cagr_oos[i],
                                       OOS_MaxDD=dd_oos[i],
                                       OOS_Sharpe_base=metrics(base.iloc[h:])["Sharpe"],
                                       OOS_CAGR_base=metrics(base.iloc[h:])["CAGR"],
                                       OOS_MaxDD_base=metrics(base.iloc[h:])["MaxDD"],
                                       OOS_Sharpe_SPY=metrics(spy.iloc[h:])["Sharpe"],
                                       OOS_CAGR_SPY=metrics(spy.iloc[h:])["CAGR"],
                                       OOS_MaxDD_SPY=metrics(spy.iloc[h:])["MaxDD"],
                                       OOS_Sharpe_median_draw=float(np.median(y_oos))))

        # ---- KEEP paths for every draw book
        mb, ms = metrics(base), metrics(spy)
        mb1, mb2 = metrics(base.iloc[:h]), metrics(base.iloc[h:])
        ms1, ms2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
        n4a = n4b = 0
        for j, c in enumerate(R.columns):
            m = metrics(R[c]); m1, m2 = metrics(IS[c]), metrics(OOS[c])
            p4a = (m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"] and m["MaxDD"] >= mb["MaxDD"])
            p4b = (m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                   and m["MaxDD"] >= 0.6 * ms["MaxDD"] and m["CAGR"] >= 0.7 * ms["CAGR"])
            n4a += p4a; n4b += p4b
            keeps.append(dict(panel=pname, draw=j, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                              H1=m1["Sharpe"], H2=m2["Sharpe"], pass4a=bool(p4a), pass4b=bool(p4b)))
        say(f"draw books ({MAXDRAW}): 4a {n4a}  4b {n4b}   "
            f"base(v2) {mb['CAGR']:.1%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.1%}  "
            f"v1 {metrics(v1)['CAGR']:.1%}/{metrics(v1)['Sharpe']:.3f}  "
            f"SPY {ms['CAGR']:.1%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.1%}  ({time.time()-t0:.0f}s)\n")

    G = pd.DataFrame(rows); W = pd.DataFrame(wf); KP = pd.DataFrame(keeps)
    C = pd.DataFrame(ceil_rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    C.to_csv(OUT / f"{STAMP}.ceiling.csv", index=False)
    pd.DataFrame(gate_rows).to_csv(OUT / f"{STAMP}.gate.csv", index=False)

    # ---------------- gate against idea 483 ------------------------------
    say("## GATE — idea 483's published triple (n=200, full width, key=sd, medians over lam x K)")
    g = G[(G.n == 200) & G.full_width & (G.key == "sd")]
    gt = g.groupby("panel").agg(pn=("pn", "first"), R2_oof=("R2_oof", "median"),
                                R2_insample=("R2_insample", "median"))
    say(gt.to_string(float_format=lambda x: f"{x:.4f}"))
    say("idea 483 published: U56 0.939 (p/n 0.28), B136 0.668 (0.68), SMALL439 0.315 (2.20)\n")

    # ---------------- headline crossover ---------------------------------
    say(f"## A. Where does out-of-fold reproduction cross {THRESH}?  (headline cell lam={LAM0}, K={K0})")
    say("Crossover located by sweeping n at each width p; p/n* is interpolated in log(p/n).")
    cross = []
    for (pan, p, K, lam, key), sub in G.groupby(["panel", "p", "K", "lam", "key"]):
        sub = sub.sort_values("pn")
        cross.append(dict(panel=pan, p=p, K=K, lam=lam, key=key, full_width=bool(sub.full_width.iloc[0]),
                          pn_star=crossover(sub.pn.values, sub.R2_oof.values),
                          pn_train_star=crossover(sub.pn_train.values, sub.R2_oof.values),
                          r2_at_smallest_pn=sub.R2_oof.iloc[0], r2_at_largest_pn=sub.R2_oof.iloc[-1]))
    CR = pd.DataFrame(cross)
    CR.to_csv(OUT / f"{STAMP}.crossover.csv", index=False)
    head = CR[(CR.lam == LAM0) & (CR.K == K0)]
    say(head.pivot_table(index=["panel", "p"], columns="key", values="pn_star").to_string(
        float_format=lambda x: f"{x:.3f}"))
    say("")

    say("## B. Full n-sweep, headline cell, FULL WIDTH (the queue's own configuration)")
    for key in ("sd", "mu", "yS"):
        sub = G[(G.lam == LAM0) & (G.K == K0) & G.full_width & (G.key == key)]
        t = sub.pivot_table(index="n", columns="panel", values="R2_oof")
        say(f"key = {key}   (out-of-fold R2 by draw count n)")
        say(t.to_string(float_format=lambda x: f"{x:.4f}"))
        t2 = sub.pivot_table(index="n", columns="panel", values="pn")
        say("  p/n at each n: " + ", ".join(f"{c} {t2[c].iloc[0]:.2f}..{t2[c].iloc[-1]:.3f}" for c in t2.columns))
        say("")

    say("## C. Is p/n a sufficient statistic?  Same p/n reached by different (p, n)")
    for key in ("sd", "mu"):
        sub = G[(G.lam == LAM0) & (G.K == K0) & (G.key == key)].copy()
        sub["pn_bin"] = pd.cut(np.log10(sub.pn), bins=np.arange(-2.0, 1.8, 0.25))
        agg = sub.groupby(["pn_bin", "panel"], observed=True).R2_oof.mean().unstack()
        sp = sub.groupby("pn_bin", observed=True).R2_oof.agg(["mean", "std", "count"])
        say(f"key = {key}: mean R2_oof by log10(p/n) bin, and the SPREAD across (panel, p) at the same p/n")
        say(pd.concat([agg, sp[["std", "count"]]], axis=1).to_string(float_format=lambda x: f"{x:.4f}"))
        say("")

    say("## D. Pre-registered test: does the crossover sit at p/n = 1 or at p/n_train = 1?")
    say("If it is a pure width effect, pn_star should track (K-1)/K and pn_train_star should be flat at ~1.")
    for key in ("sd", "mu", "yS"):
        sub = CR[(CR.key == key) & CR.full_width & (CR.lam == LAM0)]
        t = sub.pivot_table(index="K", columns="panel", values=["pn_star", "pn_train_star"])
        say(f"key = {key}  (lam={LAM0}, full width)")
        say(t.to_string(float_format=lambda x: f"{x:.3f}"))
        say("  predicted pn_star if pure width: " + ", ".join(f"K={k}: {(k-1)/k:.2f}" for k in FOLDS))
        say("")

    say("## E. Penalty sweep — is the crossover a p/n fact or a lam fact?  (all lam x K reported)")
    for key in ("sd", "mu"):
        sub = CR[(CR.key == key) & CR.full_width]
        say(f"key = {key}: pn_star by lam x K, median over panels")
        say(sub.pivot_table(index="lam", columns="K", values="pn_star").to_string(float_format=lambda x: f"{x:.3f}"))
        nan_share = sub.pn_star.isna().mean()
        say(f"  cells that never cross {THRESH} inside the swept p/n range: {nan_share:.1%}")
        say("")

    say("## F. Ceiling — R2_oof at the widest sample (n=%d), i.e. is the key linearly recoverable AT ALL" % MAXDRAW)
    say(C.pivot_table(index=["panel", "key"], columns="lam", values="R2_oof", aggfunc="median")
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("")

    # ---------------- rule 8 --------------------------------------------
    say("## Rule 8 walk-forward (fit on first half, evaluate on second, untouched)")
    ws = W.groupby(["panel", "selector"]).agg(
        OOS_Sharpe=("OOS_Sharpe", "median"), OOS_CAGR=("OOS_CAGR", "median"),
        OOS_MaxDD=("OOS_MaxDD", "median"))
    ws["median_draw"] = W.groupby(["panel", "selector"]).OOS_Sharpe_median_draw.median()
    ws["base_v2_Sharpe"] = W.groupby(["panel", "selector"]).OOS_Sharpe_base.median()
    ws["base_v2_CAGR"] = W.groupby(["panel", "selector"]).OOS_CAGR_base.median()
    ws["base_v2_MaxDD"] = W.groupby(["panel", "selector"]).OOS_MaxDD_base.median()
    ws["SPY_Sharpe"] = W.groupby(["panel", "selector"]).OOS_Sharpe_SPY.median()
    ws["SPY_CAGR"] = W.groupby(["panel", "selector"]).OOS_CAGR_SPY.median()
    ws["SPY_MaxDD"] = W.groupby(["panel", "selector"]).OOS_MaxDD_SPY.median()
    say(ws.to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    say("Does honest folding change the CHOICE, and does the change track p/n?")
    for pan in W.panel.unique():
        for n in sorted(W.n.unique()):
            a = W[(W.panel == pan) & (W.n == n) & (W.selector == "S_RESID_INSAMPLE")].set_index(["lam", "K"])
            b = W[(W.panel == pan) & (W.n == n) & (W.selector == "S_RESID_OOF")].set_index(["lam", "K"])
            if a.empty: continue
            same = int((a.draw == b.draw).sum()); tot = len(a)
            Np = G[G.panel == pan].N.iloc[0]
            say(f"  {pan} n={n:>4} (p/n {Np/n:5.2f}): IS-fitted and OOF selectors agree {same}/{tot} cells; "
                f"median OOS Sharpe IS {a.OOS_Sharpe.median():+.4f} vs OOF {b.OOS_Sharpe.median():+.4f} "
                f"(d {b.OOS_Sharpe.median()-a.OOS_Sharpe.median():+.4f})")
    say("")

    say(f"## KEEP paths across all {len(KP)} draw books: "
        f"4a {int(KP.pass4a.sum())}/{len(KP)}  4b {int(KP.pass4b.sum())}/{len(KP)}")
    say(KP.groupby("panel")[["pass4a", "pass4b"]].sum().to_string())
    both = int((KP.pass4a & KP.pass4b).sum())
    say(f"books clearing BOTH paths: {both}/{len(KP)}")
    say(f"\nruntime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()
