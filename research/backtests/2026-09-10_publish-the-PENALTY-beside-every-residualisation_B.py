#!/usr/bin/env python3
"""Idea 496 — publish the PENALTY beside every residualisation.

Premise under test (from idea 483, cloud run): "`survive` moves 0.020 -> 0.959 across
lam 1e-3..100 on broad136 while the in-sample-vs-out-of-fold gap never exceeds 0.13, so
the record's residualisation results are dominated by an unpublished dial."

Three questions, in order:

  A. CENSUS — does the dial exist in the record at all, and is it published?
     A1: every committed .py under research/ carrying a fit call: does it PENALISE
         (ridge / alpha / lam*eye) or is it unpenalised OLS (lam == 0, no dial)?
     A2: every committed CSV under research/ carrying a residualisation STATISTIC
         (survive/kill/pR2/partial/resid/t_resid...): does the SAME file carry a
         lam/alpha/penalty column beside it?  This is the idea's literal ask.

  B. RE-READ at THREE PENALTIES — rebuild the record's canonical residualisation
     (ridge the name-membership design, residualise a draw-level key) on real panels
     and re-read every conclusion at the three PRE-REGISTERED penalties
     lam in {0.01, 1.0, 100.0}, over a reported grid of design widths p and sample
     sizes n so p/n spans the record's actual range and idea 483's.  Report which
     verdicts are PENALTY-STABLE (identical at all three penalties).
     Verdicts are the record's own, not invented here:
       KILL    survive = pR2(key|control)/R2(key) < 1/3 AND |t_resid| < 2   (idea 252's bar)
       SIGN    sign of the residualised slope
       SIG     |t_resid| >= 2

  C. RULE 8 walk-forward — parameters chosen on 2009-2016 only, evaluated untouched on
     2017-2026, with both KEEP paths (4a vs live RULES v2, 4b vs SPY) priced for every
     draw book.

TUNED PARAMETERS (max 2, as the queue allows): PENALTY (lam) and PANEL.
Reported-but-not-tuned axes: design width p, sample size n, target key, cost rung.
ALL grid points are written to .grid.csv.

Costs 10 bps, weekly, weights decided at close t applied at t+1 (engine).  No network.
SURVIVORSHIP: broad136 is current constituents only.
"""
from __future__ import annotations
import re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-10_publish-the-PENALTY-beside-every-residualisation_B"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"
NDRAW, KNAMES = 250, 20
SEED0 = 4960

LAM3 = [0.01, 1.0, 100.0]                                  # PRE-REGISTERED three penalties
LAMS = [0.0, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]   # full reported sweep (tuned axis)
PS = [2, 5, 10, 20, 40, 80, None]                          # design widths; None = full panel
NS = [50, 100, 250]                                        # nested draw prefixes -> p/n axis
IS_END, OOS_START = "2016-12-31", "2017-01-01"             # PROTOCOL rule 8

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ================================================================ A. census
FIT_RE = re.compile(r"lstsq|polyfit|np\.linalg\.solve|pinv|Ridge\(|ridge_|_ridge|"
                    r"LinearRegression|OLS\(|curve_fit")
PEN_RE = re.compile(r"lam\s*\*\s*np\.eye|alpha\s*\*\s*np\.eye|lam\s*\*\s*np\.identity|"
                    r"alpha\s*\*\s*np\.identity|Ridge\(|ridge_fit|ridge_pred|_ridge\(")
RESID_RE = re.compile(r"resid|partial|pR2|survive|orthogonal|controlling for|control for|"
                      r"residualis|residualiz", re.I)
WIDE_RE = re.compile(r"get_dummies|membership|onehot|one_hot|dummies|"
                     r"np\.zeros\(\(\s*\w+\s*,\s*len\(", re.I)
# residualisation statistics as they appear as CSV COLUMN names in the record
STAT_COL_RE = re.compile(r"^(survive|kill|pr2|partial|resid|t_resid|t_partial|beta_resid|"
                         r"b_resid|r2_partial|.*_resid.*|.*partial.*|.*survive.*|.*_pr2.*)$", re.I)
PEN_COL_RE = re.compile(r"^(lam|lambda|alpha|penalty|ridge|shrink.*|lam_.*|.*_lam|.*penalty.*)$", re.I)


def census_py() -> pd.DataFrame:
    rows = []
    for p in sorted((ROOT / "research").rglob("*.py")):
        if p.name.startswith(STAMP):
            continue
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        n_fit = len(FIT_RE.findall(txt))
        if not n_fit:
            continue
        rows.append(dict(file=str(p.relative_to(ROOT)),
                         fit_calls=n_fit,
                         penalised=bool(PEN_RE.search(txt)),
                         does_residualise=bool(RESID_RE.search(txt)),
                         wide_design_hint=bool(WIDE_RE.search(txt)),
                         lam_is_swept=bool(re.search(r"LAMS?\s*=\s*[\[\(]|for\s+lam\s+in", txt))))
    return pd.DataFrame(rows)


def census_csv() -> pd.DataFrame:
    """Every committed CSV under research/: does it carry a residualisation statistic,
    and if so does it carry the penalty beside it?"""
    rows = []
    for p in sorted((ROOT / "research").rglob("*.csv")) + sorted((ROOT / "research").rglob("*.csv.gz")):
        if p.name.startswith(STAMP):
            continue                      # never count this run's own artefacts
        try:
            head = pd.read_csv(p, nrows=1)
        except Exception:
            continue
        cols = [str(c) for c in head.columns]
        stat = [c for c in cols if STAT_COL_RE.match(c)]
        pen = [c for c in cols if PEN_COL_RE.match(c)]
        if not stat:
            continue
        try:
            nrow = sum(1 for _ in open(p, "rb")) - 1 if not str(p).endswith(".gz") else len(pd.read_csv(p))
        except Exception:
            nrow = -1
        rows.append(dict(file=str(p.relative_to(ROOT)), rows=nrow,
                         stat_cols=";".join(stat[:6]), n_stat_cols=len(stat),
                         penalty_cols=";".join(pen[:3]), penalty_published=bool(pen)))
    return pd.DataFrame(rows)


# ================================================================ panels
def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True)}


def ew_weights(px, names):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[names].notna().astype(float)
    w[names] = sub.div(sub.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w


def draw_books(px, tickers, ndraw=NDRAW, k=KNAMES, seed0=SEED0):
    rets, M = {}, np.zeros((ndraw, len(tickers)))
    tix = {t: j for j, t in enumerate(tickers)}
    for i in range(ndraw):
        rng = np.random.default_rng(seed0 + i)
        names = list(rng.choice(tickers, size=k, replace=False))
        for t in names:
            M[i, tix[t]] = 1.0
        rets[i] = backtest(px, ew_weights(px, names), cost_bps=COST, freq=FREQ)["returns"]
    return pd.DataFrame(rets), M


# ================================================================ ridge / partials
def ridge_fit(X, y, lam):
    Xc = X - X.mean(0); yc = y - y.mean()
    A = Xc.T @ Xc + lam * np.eye(X.shape[1])
    try:
        b = np.linalg.solve(A, Xc.T @ yc)
    except np.linalg.LinAlgError:                 # lam == 0 with a singular design -> OLS pinv
        b = np.linalg.pinv(A) @ (Xc.T @ yc)
    return b, y.mean(), X.mean(0)


def ridge_pred(X, b, ym, xm):
    return (X - xm) @ b + ym


def ols_t(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    xc, yc = x - x.mean(), y - y.mean()
    if xc.std() == 0 or len(x) < 3:
        return 0.0, 0.0, 0.0
    b = (xc @ yc) / (xc @ xc); resid = yc - b * xc
    s2 = (resid @ resid) / (len(x) - 2)
    se = np.sqrt(s2 / (xc @ xc))
    r2 = 1 - (resid @ resid) / (yc @ yc) if (yc @ yc) > 0 else 0.0
    return b, (b / se if se else 0.0), r2


def r2_of(pred, y):
    y = np.asarray(y, float); pred = np.asarray(pred, float)
    return 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def verdicts(b_resid, t_resid, survive):
    """The record's own verdicts, read off one residualisation.  When the RAW signal is
    absent (survive is NaN because |t_raw| < 2) the kill fraction is uninterpretable and
    is reported as such rather than imputed — idea 483's own convention."""
    if survive != survive:                       # NaN
        return dict(V_KILL=np.nan, V_SIGN=int(np.sign(b_resid)),
                    V_SIG=bool(abs(t_resid) >= 2.0), readable=False)
    kill = (survive < 1.0 / 3.0) and (abs(t_resid) < 2.0)
    return dict(V_KILL=bool(kill), V_SIGN=int(np.sign(b_resid)),
                V_SIG=bool(abs(t_resid) >= 2.0), readable=True)


# ================================================================ main
def main():
    t0 = time.time()
    say(f"# {STAMP}")
    say("Idea 496: publish the PENALTY beside every residualisation.")
    say(f"PRE-REGISTERED three penalties: {LAM3}.  Full reported sweep: {LAMS}.")
    say(f"Tuned: penalty, panel.  Reported-not-tuned: width p {PS}, sample n {NS}, target key.\n")

    # ---------------------------------------------------------- A. census
    cpy = census_py(); cpy.to_csv(OUT / f"{STAMP}.census_py.csv", index=False)
    ccsv = census_csv(); ccsv.to_csv(OUT / f"{STAMP}.census_csv.csv", index=False)

    say("## A1. Does the penalty dial exist in the committed record?")
    say(f"committed .py under research/ with a fit call: {len(cpy)}")
    say(f"  ... that PENALISE (ridge/alpha/lam*eye):       {int(cpy.penalised.sum())} "
        f"({cpy.penalised.mean():.1%})")
    say(f"  ... unpenalised OLS (lam == 0, NO dial to publish): {int((~cpy.penalised).sum())} "
        f"({(~cpy.penalised).mean():.1%})")
    say(f"  ... that residualise / control for something:  {int(cpy.does_residualise.sum())}")
    say(f"  ... penalised AND residualising:               "
        f"{int((cpy.penalised & cpy.does_residualise).sum())}")
    say(f"  ... penalised with lam SWEPT in the file:      {int((cpy.penalised & cpy.lam_is_swept).sum())}")
    say("penalised files, in full:")
    for f in cpy.loc[cpy.penalised, "file"]:
        say(f"    {f}")

    say("\n## A2. Is the penalty published BESIDE the residualisation statistic?")
    say(f"committed CSVs under research/ carrying a residualisation statistic column: {len(ccsv)}")
    if len(ccsv):
        say(f"  ... that also carry a penalty column:  {int(ccsv.penalty_published.sum())} "
            f"({ccsv.penalty_published.mean():.1%})")
        say(f"  rows behind those files: with penalty {int(ccsv.loc[ccsv.penalty_published,'rows'].clip(lower=0).sum())}, "
            f"without {int(ccsv.loc[~ccsv.penalty_published,'rows'].clip(lower=0).sum())}")
    say("")

    # ---------------------------------------------------------- B/C
    grid, wf, keeps, stab = [], [], [], []
    for pname, px in panels().items():
        tickers = [c for c in px.columns if c != "SPY"]
        say(f"## Panel {pname}: {len(tickers)} names, {px.index[0].date()}..{px.index[-1].date()}")
        R, M = draw_books(px, tickers)
        start = px.index[260]
        R = R.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]

        R_is, R_oos = R.loc[:IS_END], R.loc[OOS_START:]
        h = len(R) // 2
        H1, H2 = R.iloc[:h], R.iloc[h:]

        def sh(c): return metrics(c)["Sharpe"]
        y_full = np.array([sh(R[c]) for c in R.columns])
        y_is = np.array([sh(R_is[c]) for c in R_is.columns])
        y_oos = np.array([sh(R_oos[c]) for c in R_oos.columns])
        cagr_oos = np.array([metrics(R_oos[c])["CAGR"] for c in R_oos.columns])
        dd_oos = np.array([metrics(R_oos[c])["MaxDD"] for c in R_oos.columns])

        # ---- keys (targets of the residualisation) — reported axis, not tuned
        rets = px[tickers].pct_change().loc[start:]
        ann = (rets.mean() * 252).values
        vol = (rets.std() * np.sqrt(252)).values
        ann_is = (rets.loc[:IS_END].mean() * 252).values
        keys = {
            "sd_ann_ret": np.array([np.nanstd(ann[M[i] > 0]) for i in range(len(M))]),
            "mean_vol": np.array([np.nanmean(vol[M[i] > 0]) for i in range(len(M))]),
        }
        keys_is = {"sd_ann_ret": np.array([np.nanstd(ann_is[M[i] > 0]) for i in range(len(M))])}

        # ---- positive control: y built to depend on the key and nothing else.
        # A correct residualisation must NOT kill it at ANY penalty.
        rng = np.random.default_rng(11)
        k0 = keys["sd_ann_ret"]
        y_ctrl = 3.0 * (k0 - k0.mean()) / (k0.std() or 1) + rng.normal(0, 0.5, len(k0))

        order = np.argsort(-M.sum(0))            # most-drawn names first, deterministic
        for key_name, kvec in keys.items():
            for n in NS:
                if n > len(y_full):
                    continue
                Msub, ysub, kk = M[:n], y_full[:n], kvec[:n]
                b_raw, t_raw, r2_raw = ols_t(kk, ysub)
                strong = abs(t_raw) >= 2.0
                for p in PS:
                    cols = order if p is None else order[:p]
                    X = Msub[:, cols]
                    pp = X.shape[1]
                    for lam in LAMS:
                        b, ym, xm = ridge_fit(X, ysub, lam)
                        e = ysub - ridge_pred(X, b, ym, xm)
                        b_r, t_r, pr2 = ols_t(kk, e)
                        surv = (pr2 / r2_raw) if (strong and r2_raw > 0) else np.nan
                        bs, yms, xms = ridge_fit(X, kk, lam)
                        r2_key = r2_of(ridge_pred(X, bs, yms, xms), kk)
                        # positive control at the same (p, n, lam)
                        bc, ymc, xmc = ridge_fit(X, y_ctrl[:n], lam)
                        ec = y_ctrl[:n] - ridge_pred(X, bc, ymc, xmc)
                        _, t_c, pr2_c = ols_t(kk, ec)
                        _, _, r2_c_raw = ols_t(kk, y_ctrl[:n])
                        v = verdicts(b_r, t_r, surv)
                        grid.append(dict(panel=pname, key=key_name, n=n, p=pp, p_over_n=pp / n,
                                         lam=lam, preregistered=lam in LAM3,
                                         t_raw=t_raw, R2_raw=r2_raw, raw_signal_strong=strong,
                                         b_resid=b_r, t_resid=t_r, pR2=pr2, survive=surv,
                                         kill=1 - surv if surv == surv else np.nan,
                                         R2_control_reproduces_key=r2_key,
                                         R2_fit_y=r2_of(ridge_pred(X, b, ym, xm), ysub),
                                         ctrl_t_resid=t_c,
                                         ctrl_survive=pr2_c / r2_c_raw if r2_c_raw > 0 else np.nan,
                                         **v))

        g = pd.DataFrame([r for r in grid if r["panel"] == pname])
        # ---- penalty stability of each conclusion, at the THREE pre-registered penalties
        g3 = g[g.preregistered]
        for (kn, n, p), sub in g3.groupby(["key", "n", "p"]):
            sub = sub.sort_values("lam")
            if len(sub) != 3:
                continue
            readable = bool(sub.readable.all())
            srange = (float(sub.survive.max() - sub.survive.min()) if readable else np.nan)
            stab.append(dict(panel=pname, key=kn, n=n, p=p, p_over_n=p / n,
                             readable=readable,
                             survive_lo=sub.survive.iloc[0], survive_mid=sub.survive.iloc[1],
                             survive_hi=sub.survive.iloc[2],
                             survive_range=srange,
                             t_range=float(sub.t_resid.max() - sub.t_resid.min()),
                             KILL_stable=(bool(sub.V_KILL.nunique() == 1) if readable else np.nan),
                             SIGN_stable=bool(sub.V_SIGN.nunique() == 1),
                             SIG_stable=bool(sub.V_SIG.nunique() == 1),
                             ALL_stable=(bool(sub.V_KILL.nunique() == 1 and sub.V_SIGN.nunique() == 1
                                              and sub.V_SIG.nunique() == 1) if readable else np.nan)))

        say(f"raw key -> book Sharpe (n=250): " + ", ".join(
            f"{k} t {ols_t(v, y_full)[1]:+.2f} R2 {ols_t(v, y_full)[2]:.4f}" for k, v in keys.items()))
        say(f"positive control (y = 3*sd + noise): raw t {ols_t(k0, y_ctrl)[1]:+.2f}")

        # ---- RULE 8 walk-forward: choose lam (and the draw) on 2009-2016 ONLY
        Xw = M
        for lam in LAMS:
            b, ym, xm = ridge_fit(Xw, y_is, lam)
            e_is = y_is - ridge_pred(Xw, b, ym, xm)
            sel = {
                "S_RAW_IS_SHARPE": int(np.argmax(y_is)),
                "S_RESID_lam": int(np.argmax(e_is)),
                "S_KEY_ONLY": int(np.argmax(keys_is["sd_ann_ret"])),
            }
            for sname, i in sel.items():
                wf.append(dict(panel=pname, lam=lam, selector=sname, draw=i,
                               IS_Sharpe=y_is[i], OOS_Sharpe=y_oos[i], OOS_CAGR=cagr_oos[i],
                               OOS_MaxDD=dd_oos[i],
                               OOS_Sharpe_median_draw=float(np.median(y_oos)),
                               OOS_CAGR_median_draw=float(np.median(cagr_oos)),
                               OOS_Sharpe_base=metrics(base.loc[OOS_START:])["Sharpe"],
                               OOS_CAGR_base=metrics(base.loc[OOS_START:])["CAGR"],
                               OOS_MaxDD_base=metrics(base.loc[OOS_START:])["MaxDD"],
                               OOS_Sharpe_SPY=metrics(spy.loc[OOS_START:])["Sharpe"],
                               OOS_CAGR_SPY=metrics(spy.loc[OOS_START:])["CAGR"],
                               OOS_MaxDD_SPY=metrics(spy.loc[OOS_START:])["MaxDD"]))

        # ---- KEEP paths for every draw book (full, halves, OOS)
        mb, ms = metrics(base), metrics(spy)
        mb1, mb2 = metrics(base.iloc[:h]), metrics(base.iloc[h:])
        ms1, ms2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
        mb_oos, ms_oos = metrics(base.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
        n4a = n4b = 0
        for j, c in enumerate(R.columns):
            m = metrics(R[c]); m1, m2 = metrics(H1[c]), metrics(H2[c]); mo = metrics(R_oos[c])
            p4a = (m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                   and m["MaxDD"] >= mb["MaxDD"])
            p4b = (m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                   and mo["Sharpe"] > ms_oos["Sharpe"]
                   and m["MaxDD"] >= 0.6 * ms["MaxDD"] and m["CAGR"] >= 0.7 * ms["CAGR"])
            n4a += p4a; n4b += p4b
            keeps.append(dict(panel=pname, draw=j, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                              MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                              OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                              leg4b_H1=bool(m1["Sharpe"] > ms1["Sharpe"]),
                              leg4b_H2=bool(m2["Sharpe"] > ms2["Sharpe"]),
                              leg4b_OOS=bool(mo["Sharpe"] > ms_oos["Sharpe"]),
                              leg4b_MaxDD=bool(m["MaxDD"] >= 0.6 * ms["MaxDD"]),
                              leg4b_CAGR=bool(m["CAGR"] >= 0.7 * ms["CAGR"]),
                              leg4a_H1=bool(m1["Sharpe"] > mb1["Sharpe"]),
                              leg4a_H2=bool(m2["Sharpe"] > mb2["Sharpe"]),
                              leg4a_MaxDD=bool(m["MaxDD"] >= mb["MaxDD"]),
                              pass4a=bool(p4a), pass4b=bool(p4b)))
        say(f"draw books: 4a {n4a}/{len(R.columns)}  4b {n4b}/{len(R.columns)}")
        kk_ = pd.DataFrame([r for r in keeps if r["panel"] == pname])
        say("  which leg fails: " + ", ".join(
            f"{c.replace('leg','')} {int(kk_[c].sum())}/{len(kk_)} pass"
            for c in ["leg4b_H1", "leg4b_H2", "leg4b_OOS", "leg4b_MaxDD", "leg4b_CAGR"]))
        say("  4a legs:         " + ", ".join(
            f"{c.replace('leg','')} {int(kk_[c].sum())}/{len(kk_)} pass"
            for c in ["leg4a_H1", "leg4a_H2", "leg4a_MaxDD"]))
        say(f"  base RULES v2 {mb['CAGR']:.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.2%} "
            f"(H1 {mb1['Sharpe']:.3f} H2 {mb2['Sharpe']:.3f}, OOS {mb_oos['CAGR']:.2%}/"
            f"{mb_oos['Sharpe']:.3f}/{mb_oos['MaxDD']:.2%})")
        say(f"  RULES v1     {metrics(v1)['CAGR']:.2%}/{metrics(v1)['Sharpe']:.3f}/{metrics(v1)['MaxDD']:.2%}")
        say(f"  SPY          {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} "
            f"(H1 {ms1['Sharpe']:.3f} H2 {ms2['Sharpe']:.3f}, OOS {ms_oos['CAGR']:.2%}/"
            f"{ms_oos['Sharpe']:.3f}/{ms_oos['MaxDD']:.2%})\n")

    G = pd.DataFrame(grid); W = pd.DataFrame(wf); KP = pd.DataFrame(keeps); ST = pd.DataFrame(stab)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    ST.to_csv(OUT / f"{STAMP}.stability.csv", index=False)

    # ---------------------------------------------------------- B. results
    say(f"## B. Re-read at three penalties — {len(G)} grid points, ALL in grid.csv")
    say("survive = pR2(key | ridge name-control) / R2(key raw); the record's convention.\n")

    say("### B1. How far does the penalty actually move `survive`?  (by p/n bucket, full sweep)")
    G["pn_bucket"] = pd.cut(G.p_over_n, [0, 0.05, 0.2, 0.5, 1.0, 10.0],
                            labels=["<0.05", "0.05-0.2", "0.2-0.5", "0.5-1", ">1"])
    rng_tab = G.groupby(["panel", "pn_bucket"], observed=True).agg(
        cells=("survive", "size"),
        survive_min=("survive", "min"), survive_max=("survive", "max"),
        t_min=("t_resid", "min"), t_max=("t_resid", "max"))
    rng_tab["survive_span"] = rng_tab.survive_max - rng_tab.survive_min
    say(rng_tab.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n### B2. The THREE pre-registered penalties: is each published conclusion stable?")
    RD = ST[ST.readable]
    say(f"cells (panel x key x n x p) re-read at lam {LAM3}: {len(ST)}")
    say(f"  of these, cells whose RAW signal is too weak to read a kill fraction at all "
        f"(|t_raw| < 2): {len(ST) - len(RD)} — suppressed from the KILL/ALL tallies below,")
    say(f"  not imputed (idea 483's convention).  Readable cells: {len(RD)}.")
    say(f"  KILL verdict stable at all three penalties: {int(RD.KILL_stable.sum())}/{len(RD)} "
        f"({RD.KILL_stable.mean():.1%})")
    say(f"  SIGN verdict stable (all {len(ST)} cells):     {int(ST.SIGN_stable.sum())}/{len(ST)} "
        f"({ST.SIGN_stable.mean():.1%})")
    say(f"  SIG  verdict stable (all {len(ST)} cells):     {int(ST.SIG_stable.sum())}/{len(ST)} "
        f"({ST.SIG_stable.mean():.1%})")
    say(f"  ALL THREE stable (readable cells):          {int(RD.ALL_stable.sum())}/{len(RD)} "
        f"({RD.ALL_stable.mean():.1%})")
    for d in (ST, RD):
        d["pn_bucket"] = pd.cut(d.p_over_n, [0, 0.05, 0.2, 0.5, 1.0, 10.0],
                                labels=["<0.05", "0.05-0.2", "0.2-0.5", "0.5-1", ">1"])
    say("\nstability by design width p/n (readable cells; the axis idea 483 found the")
    say("mechanism monotone in):")
    say(RD.groupby("pn_bucket", observed=True).agg(
        cells=("ALL_stable", "size"), ALL_stable=("ALL_stable", "mean"),
        KILL_stable=("KILL_stable", "mean"), survive_range=("survive_range", "median"),
        t_range=("t_range", "median")).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\nSIGN/SIG stability by p/n over ALL cells (these two verdicts need no kill fraction):")
    say(ST.groupby("pn_bucket", observed=True).agg(
        cells=("SIGN_stable", "size"), SIGN_stable=("SIGN_stable", "mean"),
        SIG_stable=("SIG_stable", "mean"), t_range=("t_range", "median")
        ).to_string(float_format=lambda x: f"{x:.4f}"))
    ST = ST.drop(columns=["pn_bucket"]); ST.to_csv(OUT / f"{STAMP}.stability.csv", index=False)

    say("\n### B3. THE RECORD'S OWN p/n.  Idea 658 measured the record's widest committed")
    say("residualisation at p=6 on n=162 (p/n 0.0370); idea 483 called 3 of 70 files wide.")
    narrow = RD[RD.p_over_n <= 0.0370]
    if len(narrow):
        say(f"readable cells at or below the record's widest p/n (<= 0.0370): {len(narrow)}, "
            f"ALL-stable {narrow.ALL_stable.mean():.1%}, median survive range across the three "
            f"penalties {narrow.survive_range.median():.5f}")
    wide = RD[RD.p_over_n > 0.5]
    if len(wide):
        say(f"readable cells at p/n > 0.5 (idea 483's WIDE regime): {len(wide)}, "
            f"ALL-stable {wide.ALL_stable.mean():.1%}, median survive range {wide.survive_range.median():.4f}")

    say("\n### B4. Positive control (y = 3*key + noise; the key MUST survive at every penalty)")
    pc = G.groupby(["panel", "pn_bucket"], observed=True).agg(
        ctrl_survive_min=("ctrl_survive", "min"), ctrl_survive_max=("ctrl_survive", "max"),
        ctrl_t_min=("ctrl_t_resid", "min"), ctrl_t_max=("ctrl_t_resid", "max"))
    say(pc.to_string(float_format=lambda x: f"{x:.4f}"))
    bad = G[(G.ctrl_survive < 1.0 / 3.0) & (G.ctrl_t_resid.abs() < 2.0)]
    say(f"grid points where the control's OWN key is spuriously KILLED: {len(bad)}/{len(G)}")
    if len(bad):
        say("  " + bad.groupby("pn_bucket", observed=True).size().to_string().replace("\n", "\n  "))

    say("\n### B5. Does the control reproduce the key it is meant to control for?")
    say(G.groupby(["panel", "pn_bucket"], observed=True)
         .R2_control_reproduces_key.agg(["min", "median", "max"])
         .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------- C. rule 8
    say("\n## C. Rule 8 walk-forward — parameters chosen on 2009-2016, evaluated on 2017-2026")
    ws = W.groupby(["panel", "selector"]).agg(
        OOS_Sharpe=("OOS_Sharpe", "median"), OOS_CAGR=("OOS_CAGR", "median"),
        OOS_MaxDD=("OOS_MaxDD", "median"), median_draw_Sharpe=("OOS_Sharpe_median_draw", "median"),
        base_v2=("OOS_Sharpe_base", "median"), SPY=("OOS_Sharpe_SPY", "median"))
    say(ws.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\nfull walk-forward grid (every lam, every selector) is in .walkforward.csv")
    for pn in W.panel.unique():
        sub = W[(W.panel == pn) & (W.selector == "S_RESID_lam")].sort_values("lam")
        say(f"{pn}: the penalty picks {sub.draw.nunique()} distinct draws over {len(sub)} lam values; "
            f"OOS Sharpe of the pick ranges {sub.OOS_Sharpe.min():.4f}..{sub.OOS_Sharpe.max():.4f} "
            f"(SPY OOS {sub.OOS_Sharpe_SPY.iloc[0]:.4f}, RULES v2 OOS {sub.OOS_Sharpe_base.iloc[0]:.4f})")
        say(f"    draws by lam: " + ", ".join(f"{l:g}->{d}" for l, d in zip(sub.lam, sub.draw)))
        # the honest test: does the penalty change the BOOK's OOS outcome at all?
        beat_spy = (sub.OOS_Sharpe > sub.OOS_Sharpe_SPY).sum()
        beat_base = (sub.OOS_Sharpe > sub.OOS_Sharpe_base).sum()
        say(f"    lam values whose pick beats SPY on OOS Sharpe: {beat_spy}/{len(sub)}; "
            f"beats RULES v2: {beat_base}/{len(sub)}")

    # honest single-number rule 8: pre-register lam = 1.0 (mid of the three), report untouched OOS
    say("\nPRE-REGISTERED rule-8 arm (lam = 1.0, the middle of the three penalties, chosen before")
    say("any OOS number was read; the draw is the IS argmax of the residualised Sharpe):")
    for pn in W.panel.unique():
        r = W[(W.panel == pn) & (W.selector == "S_RESID_lam") & (W.lam == 1.0)].iloc[0]
        say(f"  {pn}: OOS CAGR {r.OOS_CAGR:.2%} Sharpe {r.OOS_Sharpe:.3f} MaxDD {r.OOS_MaxDD:.2%}  |  "
            f"RULES v2 OOS {r.OOS_CAGR_base:.2%}/{r.OOS_Sharpe_base:.3f}/{r.OOS_MaxDD_base:.2%}  |  "
            f"SPY OOS {r.OOS_CAGR_SPY:.2%}/{r.OOS_Sharpe_SPY:.3f}/{r.OOS_MaxDD_SPY:.2%}")

    say(f"\n## KEEP paths across every draw book: 4a {int(KP.pass4a.sum())}/{len(KP)}  "
        f"4b {int(KP.pass4b.sum())}/{len(KP)}")
    say(KP.groupby("panel")[["pass4a", "pass4b"]].sum().to_string())
    say(f"\nruntime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
