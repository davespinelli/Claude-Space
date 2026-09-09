#!/usr/bin/env python3
"""Idea 483 — which published residualisations are IN-SAMPLE fits?

Idea 252 found that the queue's own proposed control (ridge the 136-name membership
matrix, residualise a draw-level outcome) reports kill 0.000 at t -0.10 IN SAMPLE and
kill 0.675 at t +6.19 OUT OF FOLD, because the in-sample name fit reproduces the
regressor itself at R2 0.998-0.9996.  Two questions here:

  A. CENSUS.  How much of the committed record fits a control or residualisation on the
     same rows it then tests on, and how many of those fits carry more than ~10 fitted
     parameters (the regime where the artefact bites)?  Static scan of every committed
     .py under research/ — heuristic, and reported as such.

  B. RE-RUN OUT OF FOLD.  Rebuild the wide-control design on three real panels and run
     it both ways (in sample and K-fold out of fold) across a full grid, with a NARROW
     (10-parameter) control beside the WIDE one so the ~10-parameter line in the idea
     text is measured rather than assumed.

Two tuned parameters only: fold count K and ridge penalty lam.  All grid points reported.
Rule 8 walk-forward: selectors are fitted on the FIRST half and evaluated on the SECOND.
Both KEEP paths (4a vs live RULES v2, 4b vs SPY) are evaluated for every draw book.

Costs 10 bps, weekly, weights decided at t applied at t+1 (engine).  No network.
SURVIVORSHIP: broad136 and the sub-$2B panel are current constituents only.
"""
from __future__ import annotations
import re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"
NDRAW, KNAMES = 200, 20                      # draws per panel, names per draw
FOLDS = [2, 3, 5, 10]                        # tuned param 1
LAMS = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]  # tuned param 2
NARROW_P = 10                                # "~10 fitted parameters" comparison

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ---------------------------------------------------------------- A. census
FIT_RE = re.compile(r"lstsq|polyfit|np\.linalg\.solve|pinv|Ridge\(|ridge_|_ridge|LinearRegression|OLS\(|curve_fit")
FOLD_RE = re.compile(r"KFold|out.?of.?fold|oof|n_folds|fold_id|folds|train_idx|holdout|_is_half|first half.*second half", re.I)
WIDE_RE = re.compile(r"get_dummies|membership|indicator matrix|onehot|one_hot|dummies|M\s*=\s*np\.zeros|design matrix|columns=names|columns=tick")

def census() -> pd.DataFrame:
    rows = []
    for p in sorted((ROOT / "research").rglob("*.py")):
        if p.name.startswith(STAMP.split("_")[0] + "_which-published"):
            continue                                   # skip this file
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        fits = len(FIT_RE.findall(txt))
        if not fits:
            continue
        has_fold = bool(FOLD_RE.search(txt))
        wide = bool(WIDE_RE.search(txt))
        # crude fitted-parameter count: widest explicit design matrix hint
        pcount = np.nan
        m = re.findall(r"np\.zeros\(\(\s*\w+\s*,\s*len\(([A-Za-z_]+)\)\s*\)\)", txt)
        if m: pcount = -1                                # per-name width, resolved as ">10"
        rows.append(dict(file=str(p.relative_to(ROOT)), fit_calls=fits, has_fold_machinery=has_fold,
                         wide_design_hint=wide, per_name_design=(pcount == -1)))
    return pd.DataFrame(rows)

# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep]

def panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    out["SMALL439"] = small_panel()
    return out

# ---------------------------------------------------------------- draw books
def ew_weights(px, names, gross=1.0):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[names].notna().astype(float)
    w[names] = gross * sub.div(sub.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w

def draw_books(px, tickers, ndraw=NDRAW, k=KNAMES, seed0=0):
    """ndraw equal-weight k-name books, weekly, 10 bps.  Returns (returns DataFrame, M)."""
    rets, M = {}, np.zeros((ndraw, len(tickers)))
    tix = {t: j for j, t in enumerate(tickers)}
    for i in range(ndraw):
        rng = np.random.default_rng(seed0 + i)
        names = list(rng.choice(tickers, size=k, replace=False))
        for t in names: M[i, tix[t]] = 1.0
        res = backtest(px, ew_weights(px, names), cost_bps=COST, freq=FREQ)
        rets[i] = res["returns"]
    return pd.DataFrame(rets), M

# ---------------------------------------------------------------- ridge / partials
def ridge_fit(X, y, lam):
    Xc = X - X.mean(0); yc = y - y.mean()
    A = Xc.T @ Xc + lam * np.eye(X.shape[1])
    b = np.linalg.solve(A, Xc.T @ yc)
    return b, y.mean(), X.mean(0)

def ridge_pred(X, b, ym, xm):
    return (X - xm) @ b + ym

def oof_pred(X, y, lam, K, seed=7):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y)); fold = np.zeros(len(y), int)
    for f, chunk in enumerate(np.array_split(idx, K)): fold[chunk] = f
    pred = np.empty(len(y))
    for f in range(K):
        tr, te = fold != f, fold == f
        b, ym, xm = ridge_fit(X[tr], y[tr], lam)
        pred[te] = ridge_pred(X[te], b, ym, xm)
    return pred

def ols_t(x, y):
    """t-stat and R2 of y ~ a + b x."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    xc, yc = x - x.mean(), y - y.mean()
    if xc.std() == 0: return 0.0, 0.0, 0.0
    b = (xc @ yc) / (xc @ xc); resid = yc - b * xc
    n = len(x); s2 = resid @ resid / (n - 2)
    se = np.sqrt(s2 / (xc @ xc))
    r2 = 1 - (resid @ resid) / (yc @ yc)
    return b, b / se if se else 0.0, r2

def r2_of(pred, y):
    y = np.asarray(y, float); pred = np.asarray(pred, float)
    return 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say(f"# {STAMP}\n")

    # ---- A. census -------------------------------------------------------
    cen = census()
    cen.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    n_fit = len(cen)
    n_nofold = int((~cen.has_fold_machinery).sum())
    n_wide = int((cen.wide_design_hint | cen.per_name_design).sum())
    n_wide_nofold = int(((cen.wide_design_hint | cen.per_name_design) & ~cen.has_fold_machinery).sum())
    say("## A. Census of committed fits (static scan, heuristic)")
    say(f"files under research/ containing a fit call: {n_fit}")
    say(f"  ... with NO fold/holdout machinery anywhere in the file: {n_nofold} ({n_nofold/max(n_fit,1):.1%})")
    say(f"  ... with a wide (per-name / dummy) design hint: {n_wide}")
    say(f"  ... wide AND no fold machinery (the >10-parameter in-sample class): {n_wide_nofold}")
    say("Heuristic: file-level regex, so 'has fold machinery' is an upper bound on discipline")
    say("(a file can fold one fit and not another) and the wide hint is a lower bound.\n")

    # ---- B. re-run out of fold ------------------------------------------
    grid, wf, keeps = [], [], []
    for pname, px in panels().items():
        tickers = [c for c in px.columns if c != "SPY"]
        say(f"## Panel {pname}: {len(tickers)} names, {px.index[0].date()}..{px.index[-1].date()}")
        R, M = draw_books(px, tickers)
        start = px.index[260]
        R = R.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        h = len(R) // 2
        IS, OOS = R.iloc[:h], R.iloc[h:]

        # outcomes and the low-dimensional summary the control is supposed to kill
        def sharpe(col): return metrics(col)["Sharpe"]
        y_full = np.array([sharpe(R[c]) for c in R.columns])
        y_is = np.array([sharpe(IS[c]) for c in IS.columns])
        y_oos = np.array([sharpe(OOS[c]) for c in OOS.columns])
        cagr_oos = np.array([metrics(OOS[c])["CAGR"] for c in OOS.columns])
        dd_oos = np.array([metrics(OOS[c])["MaxDD"] for c in OOS.columns])

        # sd = cross-sectional dispersion of member annualised returns (idea 83's key)
        ann = (px[tickers].pct_change().loc[start:].mean() * 252).values
        ann_is = (px[tickers].pct_change().loc[start:].iloc[:h].mean() * 252).values
        sd_full = np.array([np.nanstd(ann[M[i] > 0]) for i in range(len(M))])
        sd_is = np.array([np.nanstd(ann_is[M[i] > 0]) for i in range(len(M))])

        narrow_cols = np.argsort(-M.sum(0))[:NARROW_P]           # 10 most-drawn names
        b_raw, t_raw, r2_raw = ols_t(sd_full, y_full)
        # 'kill' (1 - pR2/R2_raw) is only interpretable where the raw signal exists at all
        strong = abs(t_raw) >= 2.0
        kdiv = r2_raw if strong else np.nan
        say(f"raw  sd -> book Sharpe: t {t_raw:+.2f}  R2 {r2_raw:.4f}"
            f"{'' if strong else '   [|t|<2: kill fractions suppressed as uninterpretable]'}")

        for width, cols in (("WIDE", np.arange(M.shape[1])), (f"NARROW{NARROW_P}", narrow_cols)):
            X = M[:, cols]
            for lam in LAMS:
                b, ym, xm = ridge_fit(X, y_full, lam)
                pred_is = ridge_pred(X, b, ym, xm)
                # in-sample residualisation (the published convention)
                e_is = y_full - pred_is
                _, t_isf, pr2_isf = ols_t(sd_full, e_is)
                # does the in-sample name fit reproduce sd itself?
                bs, yms, xms = ridge_fit(X, sd_full, lam)
                r2_sd_is = r2_of(ridge_pred(X, bs, yms, xms), sd_full)
                for K in FOLDS:
                    e_oof = y_full - oof_pred(X, y_full, lam, K)
                    _, t_oof, pr2_oof = ols_t(sd_full, e_oof)
                    r2_sd_oof = r2_of(oof_pred(X, sd_full, lam, K), sd_full)
                    grid.append(dict(panel=pname, p=len(cols), n=len(y_full), width=width, lam=lam, K=K,
                                     t_raw=t_raw, R2_raw=r2_raw, raw_signal_strong=strong,
                                     t_insample=t_isf, pR2_insample=pr2_isf,
                                     survive_insample=pr2_isf / kdiv if strong else np.nan,
                                     kill_insample=1 - pr2_isf / kdiv if strong else np.nan,
                                     t_oof=t_oof, pR2_oof=pr2_oof,
                                     survive_oof=pr2_oof / kdiv if strong else np.nan,
                                     kill_oof=1 - pr2_oof / kdiv if strong else np.nan,
                                     R2_fit_y_insample=r2_of(pred_is, y_full),
                                     R2_fit_y_oof=r2_of(oof_pred(X, y_full, lam, K), y_full),
                                     R2_control_reproduces_sd_insample=r2_sd_is,
                                     R2_control_reproduces_sd_oof=r2_sd_oof))
        g = pd.DataFrame([r for r in grid if r["panel"] == pname])
        say("survive = pR2(sd | control) / R2(sd raw), the record's convention (idea 252 quotes"
            " 0.000 in sample and 0.675 out of fold); medians over the 4 fold counts")
        for width in g.width.unique():
            gw = g[g.width == width]
            say(f"  {width} p={gw.p.iloc[0]}/n={len(y_full)}")
            tab = gw.groupby("lam").agg(survive_IS=("survive_insample", "median"), t_IS=("t_insample", "median"),
                                        survive_OOF=("survive_oof", "median"), t_OOF=("t_oof", "median"),
                                        sd_reproduced_IS=("R2_control_reproduces_sd_insample", "median"),
                                        sd_reproduced_OOF=("R2_control_reproduces_sd_oof", "median"))
            say(tab.to_string(float_format=lambda x: f"{x:+.4f}"))

        # ---- rule 8: selectors fitted on the FIRST half, evaluated on the SECOND
        Xw = M
        for lam in LAMS:
            for K in FOLDS:
                sel = {}
                sel["S_RAW_IS_SHARPE"] = int(np.argmax(y_is))
                b, ym, xm = ridge_fit(Xw, y_is, lam)
                sel["S_RESID_INSAMPLE"] = int(np.argmax(y_is - ridge_pred(Xw, b, ym, xm)))
                sel["S_RESID_OOF"] = int(np.argmax(y_is - oof_pred(Xw, y_is, lam, K)))
                sel["S_SD_ONLY"] = int(np.argmax(sd_is))
                for sname, i in sel.items():
                    wf.append(dict(panel=pname, lam=lam, K=K, selector=sname, draw=i,
                                   IS_Sharpe=y_is[i], OOS_Sharpe=y_oos[i], OOS_CAGR=cagr_oos[i],
                                   OOS_MaxDD=dd_oos[i],
                                   OOS_Sharpe_mean_draw=float(np.mean(y_oos)),
                                   OOS_Sharpe_median_draw=float(np.median(y_oos)),
                                   OOS_Sharpe_base=metrics(base.iloc[h:])["Sharpe"],
                                   OOS_Sharpe_SPY=metrics(spy.iloc[h:])["Sharpe"],
                                   OOS_CAGR_SPY=metrics(spy.iloc[h:])["CAGR"],
                                   OOS_CAGR_base=metrics(base.iloc[h:])["CAGR"]))

        # ---- KEEP paths for every draw book (full sample, both halves, OOS)
        mb, ms = metrics(base), metrics(spy)
        mb1, mb2 = metrics(base.iloc[:h]), metrics(base.iloc[h:])
        ms1, ms2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
        n4a = n4b = 0
        for j, c in enumerate(R.columns):
            m = metrics(R[c]); m1, m2 = metrics(IS[c]), metrics(OOS[c])
            p4a = (m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"] and m["MaxDD"] >= mb["MaxDD"])
            # H2 is the rule-8 OOS half here, so 'both halves AND OOS' == H1 and H2
            p4b = (m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                   and m["MaxDD"] >= 0.6 * ms["MaxDD"] and m["CAGR"] >= 0.7 * ms["CAGR"])
            n4a += p4a; n4b += p4b
            keeps.append(dict(panel=pname, draw=j, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                              H1=m1["Sharpe"], H2=m2["Sharpe"], pass4a=p4a, pass4b=p4b))
        say(f"draw books: 4a {n4a}/{len(R.columns)}  4b {n4b}/{len(R.columns)}   "
            f"base(v2) {mb['CAGR']:.1%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.1%}  "
            f"v1 {metrics(v1)['CAGR']:.1%}/{metrics(v1)['Sharpe']:.3f}  "
            f"SPY {ms['CAGR']:.1%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.1%}\n")

    G = pd.DataFrame(grid); W = pd.DataFrame(wf); KP = pd.DataFrame(keeps)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)

    say("## Grid summary (all 3 panels x 2 widths x 6 lam x 4 K = %d points, all in grid.csv)" % len(G))
    piv = G.groupby(["panel", "width"]).agg(survive_IS=("survive_insample", "median"), survive_OOF=("survive_oof", "median"),
                                            t_IS=("t_insample", "median"), t_OOF=("t_oof", "median"),
                                            sdR2_IS=("R2_control_reproduces_sd_insample", "median"),
                                            sdR2_OOF=("R2_control_reproduces_sd_oof", "median"))
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    flip = (G.survive_insample < 0.05) & (G.survive_oof > 0.3)
    say(f"\ngrid points reproducing idea 252's exact signature (survive_IS < 0.05, survive_OOF > 0.30): "
        f"{int(flip.sum())}/{len(G)}  (WIDE {int((flip & (G.width=='WIDE')).sum())}/{int((G.width=='WIDE').sum())}, "
        f"NARROW {int((flip & (G.width!='WIDE')).sum())}/{int((G.width!='WIDE').sum())})")
    say("direction of the artefact (sd survives MORE out of fold than in sample): %d of %d WIDE points, %d of %d NARROW"
        % (int(((G.survive_insample < G.survive_oof) & (G.width == 'WIDE')).sum()), int((G.width == 'WIDE').sum()),
           int(((G.survive_insample < G.survive_oof) & (G.width != 'WIDE')).sum()), int((G.width != 'WIDE').sum())))
    say("the mechanism, all panels/widths (median over the grid): the control reproduces the summary it is meant to")
    say(G.groupby(["panel", "width"]).agg(p=("p", "first"),
                                          sd_reproduced_IS=("R2_control_reproduces_sd_insample", "median"),
                                          sd_reproduced_OOF=("R2_control_reproduces_sd_oof", "median"),
                                          fit_y_IS=("R2_fit_y_insample", "median"),
                                          fit_y_OOF=("R2_fit_y_oof", "median")).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n## Rule 8 walk-forward (choose on first half, evaluate on second)")
    ws = W.groupby(["panel", "selector"]).agg(OOS_Sharpe=("OOS_Sharpe", "median"), OOS_CAGR=("OOS_CAGR", "median"),
                                              OOS_MaxDD=("OOS_MaxDD", "median"),
                                              vs_mean_draw=("OOS_Sharpe", "median"))
    ws["mean_draw"] = W.groupby(["panel", "selector"]).OOS_Sharpe_mean_draw.median()
    ws["base_v2"] = W.groupby(["panel", "selector"]).OOS_Sharpe_base.median()
    ws["SPY"] = W.groupby(["panel", "selector"]).OOS_Sharpe_SPY.median()
    ws = ws.drop(columns=["vs_mean_draw"])
    say(ws.to_string(float_format=lambda x: f"{x:.4f}"))
    for pn in W.panel.unique():
        sub = W[W.panel == pn]
        a = sub[sub.selector == "S_RESID_INSAMPLE"].set_index(["lam", "K"]).OOS_Sharpe
        b = sub[sub.selector == "S_RESID_OOF"].set_index(["lam", "K"]).OOS_Sharpe
        same = (sub[sub.selector == "S_RESID_INSAMPLE"].set_index(["lam", "K"]).draw ==
                sub[sub.selector == "S_RESID_OOF"].set_index(["lam", "K"]).draw)
        say(f"{pn}: IS-fitted and OOF selectors pick the SAME draw in {int(same.sum())}/{len(same)} cells; "
            f"median OOS Sharpe IS-fitted {a.median():.4f} vs OOF {b.median():.4f} (d {b.median()-a.median():+.4f})")

    say(f"\n## KEEP paths across all draw books: 4a {int(KP.pass4a.sum())}/{len(KP)}  4b {int(KP.pass4b.sum())}/{len(KP)}")
    say(KP.groupby("panel")[["pass4a", "pass4b"]].sum().to_string())
    say(f"\nruntime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()
