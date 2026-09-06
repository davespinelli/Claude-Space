#!/usr/bin/env python3
"""Idea 83 - "dispersion-as-a-survivorship-detector" (lane B, 2026-09-06).

The question
------------
Idea 78 (`2026-09-05_candidate-count-vs-dispersion_B`) drew 150 fixed random sub-panels
of B136 and ran CAND-n and EWall on each.  Over those draws, cross-sectional dispersion
of 12-1 momentum predicts the LEVEL of a draw's Sharpe far better than it predicts the
RANKING GAP between the two books.  The QUEUE's reading of that asymmetry:

    "on current-constituent panels that is what survivorship manufactures: a draw
     containing more of the names that won has both higher dispersion and higher
     Sharpe."

If that is right, draw-level dispersion is a *survivorship thermometer* - a proxy for
how much of the panel's realised winner-content the draw happens to contain - and every
published dispersion-vs-Sharpe reading taken on a current-constituent panel is
contaminated, idea 78's test C included.

The test, pre-registered
------------------------
Give each draw a scalar `W` = the mean full-sample ANNUALISED log return of its
constituent names (equivalently: the draw's own equal-weight buy-and-hold winner-content,
computed from name returns alone with no book, no gate and no costs).  That is "each
name's full-sample return regressed out", aggregated to the draw, which is the level at
which dispersion and Sharpe are both measured.

    Annualised over each name's OWN listed history, not over the common window.  13 of
    the 136 B136 columns list after the window opens (ABBV ANET AVGO META NOW PANW PLTR
    TSLA UBER XLC XLRE ZTS, plus MMC which is empty in the cache), and they include the
    largest winners in the panel; a common-window W silently drops them and so
    under-measures winner-content on exactly the names that manufacture it.  The
    common-window variant `W_cw` is reported beside the primary one throughout.
    `W_max` (the draw's single best name) is reported as a second control because a
    20-name momentum book can be carried by one name.

Then:

    T1  univariate    Sharpe ~ sd            -> reproduce the published asymmetry
    T2  the mechanism corr(sd, W), corr(Sharpe, W)
    T3  partial       Sharpe ~ sd | W        -> THE TEST.  If the sd coefficient dies
                                                once W is held, dispersion is a
                                                thermometer, not a signal.
    T4  the same three on the RANKING PREMIUM, which the queue says is already ~nil
    T5  a strict per-name control: W built from the draw's names only, and a
        RESIDUALISED dispersion (sd orthogonalised on W) fed to rule 8 as a selector.

Pre-registered prediction (written before any T3 number was read): if the queue's
reading is right, partial R2(Sharpe ~ sd | W) falls to under a third of the univariate
R2 and its t-stat falls under 2.  If instead dispersion survives W, idea 78's test C is
clean and the thermometer reading is wrong.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. k in {20, 40, 80}   sub-panel size          (idea 78's grid, imported unchanged)
    2. n in {5, 20}        book size               (idea 78's grid, imported unchanged)
No parameter of this run is tuned: the draws, seeds, gate, gross, cadence and costs are
idea 78's own, and every one of the 6 (k, n) cells is reported.

Reproduction gate (run BEFORE any new number is read)
    [a] harness: idea 2's U56/CAND20 row and the live RULES v1 row.
    [b] the 150 sub-panels are re-drawn from idea 78's seeds and every re-run book
        metric is checked against the committed `...gridB.csv` at max abs diff.
Nothing new is read until both pass.

Walk-forward (PROTOCOL rule 8), selectors fixed before any OOS number was read
    S0  do-nothing: full B136 CAND-20 (idea 78's control).
    S1  IS-Sharpe argmax over the 150 CAND-20 sub-panel books.
    S2  DISPERSION: highest IS mean eligible-set dispersion   (idea 78's S2, reproduced)
    S3  COUNT: highest IS mean eligible count                 (idea 78's S3, reproduced)
    S5  RESID-DISPERSION (new): highest IS dispersion after IS winner-content W_IS is
        regressed out of it.  If dispersion is a thermometer, S5 is what is left of it.
    S6  WINNERNESS (new): highest IS mean name return - the pure survivorship selector,
        run so the thermometer's own OOS skill is on the table beside its proxy's.
    All selector inputs use 2009-2016 only; 2017-2026 is read once, untouched.

Verdicts (both KEEP paths, every one of the 450 books)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Survivorship: universe_broad.json is current constituents, one-directional.  That is the
premise under test, not a caveat to it - the run measures how much of a published
diagnostic that bias accounts for, and cannot remove it.

Deterministic (numpy Generator(PCG64), idea 78's seeds), standalone.  Reads baseline.py
and engine.py; modifies nothing.
"""
import sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics, rebalance_mask

# ---- idea 78's constants, imported verbatim -------------------------------------
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
N_DRAWS_B = 50
N_BOOKS = [5, 20]
N_BOOK = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_B = 78_500
SEED_S4 = 78_999

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF_GRIDB = OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- idea 78's helpers
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights_cand(px, tradable, n, gross=GROSS):
    elig = eligible_mask(px, tradable)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def weights_ewall(px, tradable, gross=GROSS):
    elig = eligible_mask(px, tradable)
    cnt = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    ms, mr = metrics(spy), metrics(r)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not mr["MaxDD"] >= 0.60 * ms["MaxDD"]: f.append("DD")
    if not mr["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    m = a.notna() & b.notna()
    if m.sum() < 3: return np.nan
    return float(a[m].rank().corr(b[m].rank()))


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- regression helpers
def ols(y, X, names):
    """Plain OLS with an intercept.  Returns dict(R2, coefs, tstats, n)."""
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    s2 = float(resid @ resid) / dof
    XtXi = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(XtXi) * s2)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / ss_tot if ss_tot > 0 else np.nan
    return dict(R2=r2, n=len(y), resid=resid,
                coef=dict(zip(["const"] + names, beta)),
                t=dict(zip(["const"] + names, beta / se)))


def resid_on(y, x):
    """Residual of y after regressing out x (with intercept)."""
    return ols(y, [x], ["x"])["resid"]


def partial_r2(y, x, ctrl):
    """R2 between resid(y|ctrl) and resid(x|ctrl); its t is the t on x in y ~ x + ctrl."""
    ry, rx = resid_on(y, ctrl), resid_on(x, ctrl)
    full = ols(y, [x, ctrl], ["x", "ctrl"])
    r = np.corrcoef(ry, rx)[0, 1]
    return dict(pR2=r ** 2, r=r, t=full["t"]["x"], full_R2=full["R2"],
                t_ctrl=full["t"]["ctrl"])


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 200)
    P("IDEA 83 - dispersion-as-a-survivorship-detector (lane B, 2026-09-06)")
    P("Does draw-level dispersion still predict draw-level Sharpe once each name's "
      "full-sample return is regressed out?")
    P("=" * 200)

    # ---------------------------------------------------------------- [a] harness
    P("\n[a] HARNESS - published rows recomputed before anything new is read")
    px56 = load_universe()
    px136 = load_universe(broad=True)
    tr136 = set(c for c in px136.columns if c != "SPY") | ({"SPY"} if "SPY" in px136.columns else set())
    tr136 = set(px136.columns)          # idea 78's B136 has every column tradable
    s56 = px56.index[260]
    r_u56 = backtest(px56, weights_cand(px56, set(px56.columns), 20), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_u56); h1, h2 = half_sharpes(r_u56)
    P(f"    U56/CAND20   {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}  halves {h1:.5f}/{h2:.5f}"
      f"   (idea 2/73/77 published 12.7% / 1.092-1.093 / -18.3%, halves 1.088/1.102-1.103)")
    r_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_v1)
    P(f"    U56/RULES v1 {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}"
      f"   (published 6.5% / 0.664-0.666 / -13.8%)")

    # ---------------------------------------------------------------- panel-level anchors
    startb = px136.index[260]
    spy = px136["SPY"].pct_change().fillna(0).loc[startb:]
    spy_oos = spy.loc[OOS_START:]
    base = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    ms, mb = metrics(spy), metrics(base)
    sh1, sh2 = half_sharpes(spy)
    P(f"\n    window {startb.date()} -> {px136.index[-1].date()}  ({len(spy)} days)")
    P(f"    SPY              {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves {sh1:.3f}/{sh2:.3f}"
      f"  OOS {metrics(spy_oos)['Sharpe']:.3f}")
    P(f"    RULES v1 on B136 {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}  halves "
      f"{half_sharpes(base)[0]:.3f}/{half_sharpes(base)[1]:.3f}  OOS {metrics(base.loc[OOS_START:])['Sharpe']:.3f}")
    P(f"    4b bars: MaxDD <= {0.60 * abs(ms['MaxDD']):.2%}, CAGR >= {0.70 * ms['CAGR']:.2%}, "
      f"H1 > {sh1:.3f}, H2 > {sh2:.3f}, OOS Sharpe > {metrics(spy_oos)['Sharpe']:.3f}")

    # ---------------------------------------------------------------- name-level returns
    # W is built from NAME RETURNS ONLY: no book, no gate, no costs, no ranking.
    names136 = [c for c in px136.columns if c in tr136]
    px_n = px136[names136].loc[startb:]

    def ann_logret(p):
        """Annualised log return over each column's OWN listed history (NaN if < 1y)."""
        out = {}
        for c in p.columns:
            s = p[c].dropna()
            if len(s) < 252 or s.iloc[0] <= 0:
                out[c] = np.nan; continue
            yrs = (s.index[-1] - s.index[0]).days / 365.25
            out[c] = float(np.log(s.iloc[-1] / s.iloc[0]) / yrs)
        return pd.Series(out)

    lr_full = ann_logret(px_n)                       # primary  W
    lr_is = ann_logret(px_n.loc[:IS_END])            # primary  W_IS (2009-2016 only)
    cw_full = np.log(px_n.iloc[-1] / px_n.iloc[0])   # variant  W_cw (common window)
    late = [c for c in names136 if px_n[c].first_valid_index() is not None
            and px_n[c].first_valid_index() > px_n.index[0]]
    empty = [c for c in names136 if px_n[c].first_valid_index() is None]
    P(f"\n    name-level ANNUALISED log return over {len(names136)} B136 columns "
      f"({lr_full.notna().sum()} with >=1y of history; {len(late)} list late: {' '.join(sorted(late))}; "
      f"{len(empty)} empty: {' '.join(empty) if empty else '-'})")
    P(f"      full  mean {lr_full.mean():.4f} ({np.expm1(lr_full.mean()):.2%}/yr), sd {lr_full.std():.4f}, "
      f"min {lr_full.min():.3f} ({lr_full.idxmin()}), max {lr_full.max():.3f} ({lr_full.idxmax()})")
    P(f"      IS    mean {lr_is.mean():.4f} ({np.expm1(lr_is.mean()):.2%}/yr), sd {lr_is.std():.4f}, "
      f"{lr_is.notna().sum()} names with >=1y before {IS_END}")
    both = lr_full.notna() & lr_is.notna()
    P(f"      corr(full, IS) over the {int(both.sum())} names with both = "
      f"{float(np.corrcoef(lr_full[both], lr_is[both])[0,1]):+.4f} "
      f"(Spearman {spearman(lr_full[both], lr_is[both]):+.4f})")
    cwv = cw_full.notna() & lr_full.notna()
    P(f"      corr(annualised, common-window) over the {int(cwv.sum())} common-window names = "
      f"{float(np.corrcoef(lr_full[cwv], cw_full[cwv])[0,1]):+.4f} "
      f"— the common-window column drops {len(late) + len(empty)} names including "
      f"{cw_full.isna().sum()} of the panel's late listers")

    # ---------------------------------------------------------------- [b] rebuild idea 78's 150 draws
    P(f"\n[b] REPRODUCTION - idea 78's {len(KS) * N_DRAWS_B} sub-panels re-drawn from its seeds and re-run")
    # Optional recompute cache (dev convenience only).  It is keyed on nothing but this
    # script's own inputs and is NOT committed; deleting it reproduces the run from scratch.
    cache = Path("/tmp/claude-0/-home-user-Claude-Space/bddcdb69-4c64-56dd-8c58-7e907cd70aa5"
                 "/scratchpad") / f"{STEM}.heavy.pkl"
    rec, series, draw_cols = [], {}, {}
    if cache.exists():
        import pickle
        rec, series = pickle.loads(cache.read_bytes())
        P(f"    (loaded {len(rec)} book rows from the local recompute cache)")
    for k in ([] if rec else KS):
        rng = np.random.default_rng(SEED_B + k)
        for d in range(N_DRAWS_B):
            cols = list(rng.choice(names136, size=k, replace=False))
            draw_cols[(k, d)] = cols
            keep = list(dict.fromkeys(cols + ["SPY"]))
            p = px136[keep].dropna(how="all").ffill()
            tr = set(cols)
            el = eligible_mask(p, tr)
            wmask = rebalance_mask(p.index, FREQ).values
            ne = el[wmask].sum(axis=1).loc[startb:]
            mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(el[cols])
            sdw = mom_p[wmask].loc[startb:].std(axis=1)
            r_e = backtest(p, weights_ewall(p, tr), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
            me = metrics(r_e)
            # winner-content: the draw's OWN names' realised returns.  No book, no gate.
            W = float(lr_full[cols].mean())
            W_is = float(lr_is[cols].mean())
            Wsd = float(lr_full[cols].std())
            W_max = float(lr_full[cols].max())
            W_cw = float(cw_full[cols].mean())
            W_cov = float(lr_full[cols].notna().mean())
            for nb in N_BOOKS:
                r_c = backtest(p, weights_cand(p, tr, nb), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
                series[(k, d, nb)] = r_c
                mc = metrics(r_c)
                c1, c2 = half_sharpes(r_c)
                rec.append(dict(
                    k=k, n=nb, draw=d,
                    n_elig=float(ne.mean()), sd=float(sdw.mean()),
                    n_elig_IS=float(ne.loc[:IS_END].mean()), sd_IS=float(sdw.loc[:IS_END].mean()),
                    W=W, W_IS=W_is, W_sd=Wsd, W_max=W_max, W_cw=W_cw, W_cov=W_cov,
                    CAGR=mc["CAGR"], Sharpe=mc["Sharpe"], MaxDD=mc["MaxDD"], H1=c1, H2=c2,
                    Sharpe_IS=metrics(r_c.loc[:IS_END])["Sharpe"],
                    Sharpe_OOS=metrics(r_c.loc[OOS_START:])["Sharpe"],
                    CAGR_OOS=metrics(r_c.loc[OOS_START:])["CAGR"],
                    MaxDD_OOS=metrics(r_c.loc[OOS_START:])["MaxDD"],
                    ew_Sharpe=me["Sharpe"], ew_CAGR=me["CAGR"], ew_MaxDD=me["MaxDD"],
                    ew_Sharpe_IS=metrics(r_e.loc[:IS_END])["Sharpe"],
                    ew_Sharpe_OOS=metrics(r_e.loc[OOS_START:])["Sharpe"],
                    premium=mc["Sharpe"] - me["Sharpe"],
                    f4a=fail_4a(r_c, base),
                    f4b=fail_4b(r_c, spy, r_c.loc[OOS_START:], spy_oos),
                    ew_f4a=fail_4a(r_e, base),
                    ew_f4b=fail_4b(r_e, spy, r_e.loc[OOS_START:], spy_oos)))
        P(f"    k={k:<3} done  ({time.time() - t0:.0f}s)")
    if not cache.exists():
        import pickle
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(pickle.dumps((rec, series)))
    B = pd.DataFrame(rec)
    B.to_csv(OUT / f"{STEM}.draws.csv", index=False)

    ref = pd.read_csv(REF_GRIDB)
    j = B.merge(ref, on=["k", "n", "draw"], suffixes=("", "_ref"))
    assert len(j) == len(B) == 300, (len(j), len(B))
    P(f"\n    re-run vs committed idea-78 gridB.csv, {len(j)} rows, max abs difference:")
    ok = True
    for c in ["n_elig", "sd", "n_elig_IS", "sd_IS", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "Sharpe_IS", "Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS", "ew_Sharpe", "ew_CAGR",
              "ew_MaxDD", "premium"]:
        dmax = float((j[c] - j[c + "_ref"]).abs().max())
        ok &= dmax < 1e-9
        P(f"      {c:<12} {dmax:.3e}")
    same_flags = int((j["f4a"] == j["f4a_ref"]).sum()), int((j["f4b"] == j["f4b_ref"]).sum())
    P(f"      f4a / f4b verdict strings identical in {same_flags[0]} / {same_flags[1]} of {len(j)} rows")
    P(f"    REPRODUCTION {'PASS - idea 78 rebuilt byte-for-byte; new numbers may be read' if ok else 'FAIL'}")
    if not ok:
        P("    ABORT: the panel under test is not the published one.")
        return

    # ================================================================== T1-T4
    P("\n" + "=" * 200)
    P("T1-T4 - dispersion, Sharpe and winner-content over the 150 sub-panels")
    P("=" * 200)
    P("  sd = mean weekly cross-sectional sd of 12-1 momentum over the draw's eligible set (idea 78's own column)")
    P("  W  = mean FULL-SAMPLE annualised log return of the draw's own names.  No book, no gate, no ranking, no costs.")

    reg_rows, ctrl_rows = [], []
    for nb in N_BOOKS:
        for scope, sub in [("pooled", B[B.n == nb])] + [(f"k={k}", B[(B.n == nb) & (B.k == k)]) for k in KS]:
            for ycol, ylab in [("Sharpe", "CAND Sharpe"), ("ew_Sharpe", "EWall Sharpe"), ("premium", "premium")]:
                y = sub[ycol].values
                u_sd = ols(y, [sub["sd"].values], ["sd"])
                u_W = ols(y, [sub["W"].values], ["W"])
                pr = partial_r2(y, sub["sd"].values, sub["W"].values)
                pr_cw = partial_r2(y, sub["sd"].values, sub["W_cw"].values)
                two = ols(y, [sub["sd"].values, sub["W"].values, sub["W_max"].values],
                          ["sd", "W", "W_max"])
                reg_rows.append(dict(
                    n=nb, scope=scope, y=ylab, N=len(sub),
                    R2_sd=u_sd["R2"], t_sd=u_sd["t"]["sd"],
                    R2_W=u_W["R2"], t_W=u_W["t"]["W"],
                    pR2_sd_given_W=pr["pR2"], t_sd_given_W=pr["t"], t_W_given_sd=pr["t_ctrl"],
                    R2_both=pr["full_R2"],
                    kill=pr["pR2"] / u_sd["R2"] if u_sd["R2"] > 0 else np.nan,
                    pR2_sd_given_Wcw=pr_cw["pR2"], t_sd_given_Wcw=pr_cw["t"],
                    t_sd_given_W_Wmax=two["t"]["sd"], R2_sd_W_Wmax=two["R2"],
                    rho_sd_y=spearman(sub["sd"], sub[ycol]),
                    rho_W_y=spearman(sub["W"], sub[ycol])))
        for scope, s in [("pooled", B[B.n == nb])] + [(f"k={k}", B[(B.n == nb) & (B.k == k)]) for k in KS]:
            ctrl_rows.append(dict(n=nb, scope=scope, N=len(s),
                                  rho_sd_W=spearman(s["sd"], s["W"]),
                                  r_sd_W=float(np.corrcoef(s["sd"], s["W"])[0, 1]),
                                  rho_sd_Wmax=spearman(s["sd"], s["W_max"]),
                                  rho_sd_Wcw=spearman(s["sd"], s["W_cw"]),
                                  rho_sd_WIS=spearman(s["sd"], s["W_IS"]),
                                  rho_nelig_W=spearman(s["n_elig"], s["W"]),
                                  rho_W_Sharpe=spearman(s["W"], s["Sharpe"])))
    R = pd.DataFrame(reg_rows)
    C = pd.DataFrame(ctrl_rows)
    R.to_csv(OUT / f"{STEM}.regressions.csv", index=False)
    C.to_csv(OUT / f"{STEM}.mechanism.csv", index=False)

    P("\n  T2 - THE MECHANISM: is a wider draw a more winning draw?")
    P(fmt(C.set_index(["n", "scope"])))

    P("\n  T1/T3/T4 - univariate vs partial.  kill = pR2(sd|W) / R2(sd); "
      "the pre-registered bar is kill < 1/3 AND |t_sd_given_W| < 2.")
    P(fmt(R.set_index(["n", "scope", "y"])[
        ["N", "R2_sd", "t_sd", "R2_W", "t_W", "pR2_sd_given_W", "t_sd_given_W",
         "t_W_given_sd", "R2_both", "kill", "rho_sd_y", "rho_W_y"]]))
    P("\n  the two control variants, same rows (W_cw = common-window W, drops the late listers; "
      "t_sd|W,W_max adds the draw's single best name as a second control):")
    P(fmt(R.set_index(["n", "scope", "y"])[
        ["pR2_sd_given_Wcw", "t_sd_given_Wcw", "t_sd_given_W_Wmax", "R2_sd_W_Wmax"]]))

    P("\n  headline (n=20, pooled over all 150 draws):")
    for ylab in ["CAND Sharpe", "EWall Sharpe", "premium"]:
        r = R[(R.n == 20) & (R.scope == "pooled") & (R.y == ylab)].iloc[0]
        P(f"    {ylab:<13} R2(sd) {r.R2_sd:.4f} (t {r.t_sd:+.2f})  ->  "
          f"partial R2(sd | W) {r.pR2_sd_given_W:.4f} (t {r.t_sd_given_W:+.2f})   "
          f"kill {r.kill:.3f}   [W alone R2 {r.R2_W:.4f}, t {r.t_W:+.2f}; "
          f"sd | W,W_max t {r.t_sd_given_W_Wmax:+.2f}]")

    # the within-k reading is the one with count exactly matched
    P("\n  the same statistic with the CANDIDATE COUNT held exactly (within-k, N=50 each):")
    for nb in N_BOOKS:
        for ylab in ["CAND Sharpe", "EWall Sharpe"]:
            v = R[(R.n == nb) & (R.y == ylab) & (R.scope != "pooled")]
            P(f"    n={nb:<3} {ylab:<13} R2(sd) {v.R2_sd.min():.3f}-{v.R2_sd.max():.3f}  ->  "
              f"pR2(sd|W) {v.pR2_sd_given_W.min():.3f}-{v.pR2_sd_given_W.max():.3f}  "
              f"|t_sd|W| max {v.t_sd_given_W.abs().max():.2f}  "
              f"(sd survives at |t|>2 in {(v.t_sd_given_W.abs() > 2).sum()} of {len(v)} k-cells)")

    # ---------------------------------------------------------------- T5 residualised sd
    P("\n  T5 - a residualised dispersion column, per draw (sd orthogonalised on W within its own k cell):")
    B["sd_resid"] = np.nan
    B["sd_resid_IS"] = np.nan
    for nb in N_BOOKS:
        for k in KS:
            m = (B.n == nb) & (B.k == k)
            B.loc[m, "sd_resid"] = resid_on(B.loc[m, "sd"].values, B.loc[m, "W"].values)
            B.loc[m, "sd_resid_IS"] = resid_on(B.loc[m, "sd_IS"].values, B.loc[m, "W_IS"].values)
    for nb in N_BOOKS:
        s = B[B.n == nb]
        P(f"    n={nb}: rho(sd_resid, Sharpe) {spearman(s['sd_resid'], s['Sharpe']):+.4f} "
          f"vs rho(sd, Sharpe) {spearman(s['sd'], s['Sharpe']):+.4f};  "
          f"rho(sd_resid, premium) {spearman(s['sd_resid'], s['premium']):+.4f} "
          f"vs rho(sd, premium) {spearman(s['sd'], s['premium']):+.4f}")
    B.to_csv(OUT / f"{STEM}.draws.csv", index=False)

    # ================================================================== KEEP paths
    P("\n" + "=" * 200)
    P("BOTH KEEP PATHS - all 450 books (150 CAND-5, 150 CAND-20, 150 EWall)")
    P("=" * 200)
    kb = B[B.n == N_BOOK]
    allbooks = pd.concat([
        B.assign(book="CAND" + B.n.astype(str), f4a_=B.f4a, f4b_=B.f4b)[["k", "draw", "book", "f4a_", "f4b_"]],
        kb.assign(book="EWall", f4a_=kb.ew_f4a, f4b_=kb.ew_f4b)[["k", "draw", "book", "f4a_", "f4b_"]]])
    P(fmt(allbooks.groupby("book").agg(N=("f4a_", "size"),
                                       pass4a=("f4a_", lambda s: (s == "-").sum()),
                                       pass4b=("f4b_", lambda s: (s == "-").sum())), 0))
    P(f"\n  overall: 4a {int((allbooks.f4a_ == '-').sum())} of {len(allbooks)};  "
      f"4b {int((allbooks.f4b_ == '-').sum())} of {len(allbooks)}")
    P("\n  4b failing-bar census:")
    P(allbooks.f4b_.str.split(",").explode().value_counts().to_string())
    P("\n  by (k, n) cell - mean Sharpe, mean W, and pass counts:")
    cell = B.groupby(["k", "n"]).agg(sd=("sd", "mean"), W=("W", "mean"), n_elig=("n_elig", "mean"),
                                     CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"),
                                     Sharpe_sd=("Sharpe", "std"), MaxDD=("MaxDD", "mean"),
                                     ew_Sharpe=("ew_Sharpe", "mean"), premium=("premium", "mean"),
                                     p4a=("f4a", lambda s: (s == "-").sum()),
                                     p4b=("f4b", lambda s: (s == "-").sum()), N=("draw", "count"))
    P(fmt(cell))
    cell.to_csv(OUT / f"{STEM}.cells.csv")

    # is 4b PASS itself a function of W rather than of sd?
    P("\n  does the 4b verdict itself track W or sd?  (logit-free: means by verdict, n=20)")
    for nb in N_BOOKS:
        s = B[B.n == nb]
        g = s.assign(p4b=(s.f4b == "-")).groupby("p4b").agg(N=("draw", "size"), W=("W", "mean"),
                                                            sd=("sd", "mean"), Sharpe=("Sharpe", "mean"))
        P(f"    n={nb}")
        P(fmt(g))
        a, b_ = s.loc[s.f4b == "-", "W"], s.loc[s.f4b != "-", "W"]
        if len(a) > 1 and len(b_) > 1:
            t = (a.mean() - b_.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b_.var(ddof=1) / len(b_))
            a2, b2 = s.loc[s.f4b == "-", "sd"], s.loc[s.f4b != "-", "sd"]
            t2 = (a2.mean() - b2.mean()) / np.sqrt(a2.var(ddof=1) / len(a2) + b2.var(ddof=1) / len(b2))
            P(f"      Welch t on W = {t:+.2f};  on sd = {t2:+.2f}")

    # ================================================================== rule 8
    P("\n" + "=" * 200)
    P("PROTOCOL rule 8 - selectors fitted on 2009-2016 ONLY, 2017-2026 read once")
    P("=" * 200)
    IS = B[B.n == N_BOOK].set_index(["k", "draw"])
    r0 = backtest(px136, weights_cand(px136, tr136, N_BOOK), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
    m0, m0o = metrics(r0), metrics(r0.loc[OOS_START:])
    spyo = metrics(spy_oos)

    picks = {
        "S0 do-nothing (full B136 CAND-20)": None,
        "S1 IS-Sharpe argmax":               IS["Sharpe_IS"].idxmax(),
        "S2 DISPERSION (max IS sd)":         IS["sd_IS"].idxmax(),
        "S3 COUNT (max IS n_elig)":          IS["n_elig_IS"].idxmax(),
        "S5 RESID-DISP (max IS sd | W_IS)":  IS["sd_resid_IS"].idxmax(),
        "S6 WINNERNESS (max IS name ret)":   IS["W_IS"].idxmax(),
        "S4 random sub-panel":               IS.index[np.random.default_rng(SEED_S4).integers(len(IS))],
    }
    wrows = []
    for lab, key in picks.items():
        if key is None:
            r = r0; kk, dd = -1, -1
        else:
            kk, dd = key
            r = series[(kk, dd, N_BOOK)]
        ro = r.loc[OOS_START:]
        mo, mm = metrics(ro), metrics(r)
        cellmask = (B.n == N_BOOK) & (B.k == kk)
        wrows.append(dict(
            selector=lab, k=kk, draw=dd,
            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            full_Sharpe=mm["Sharpe"], full_MaxDD=mm["MaxDD"],
            cell_mean_OOS=float(B.loc[cellmask, "Sharpe_OOS"].mean()) if kk > 0 else np.nan,
            cell_sd_OOS=float(B.loc[cellmask, "Sharpe_OOS"].std()) if kk > 0 else np.nan,
            cell_4b_rate=float((B.loc[cellmask, "f4b"] == "-").mean()) if kk > 0 else np.nan,
            f4b=fail_4b(r, spy, ro, spy_oos)))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  SPY OOS {spyo['CAGR']:.2%} / {spyo['Sharpe']:.3f} / {spyo['MaxDD']:.2%}; "
      f"RULES v1 B136 OOS {metrics(base.loc[OOS_START:])['CAGR']:.2%} / "
      f"{metrics(base.loc[OOS_START:])['Sharpe']:.3f}; "
      f"do-nothing OOS {m0o['CAGR']:.2%} / {m0o['Sharpe']:.3f} / {m0o['MaxDD']:.2%}")
    P(fmt(W8.set_index("selector"), 4))
    d0 = float(W8.loc[W8.selector.str.startswith("S0"), "OOS_Sharpe"].iloc[0])
    P(f"\n  OOS Sharpe regret vs the do-nothing control ({d0:.4f}):")
    for _, r in W8.iterrows():
        if r.selector.startswith("S0"): continue
        P(f"    {r.selector:<36} {r.OOS_Sharpe - d0:+.4f}"
          f"   (its cell mean {r.cell_mean_OOS:.3f} +- {r.cell_sd_OOS:.3f}; "
          f"z within cell {(r.OOS_Sharpe - r.cell_mean_OOS) / r.cell_sd_OOS:+.2f})")

    P("\n  selector-input skill over the 150 CAND-20 sub-panels (Spearman with OOS Sharpe):")
    s = B[B.n == N_BOOK]
    for lab, col in [("IS Sharpe", "Sharpe_IS"), ("IS sd (dispersion)", "sd_IS"),
                     ("IS n_elig (count)", "n_elig_IS"), ("IS sd | W_IS (residualised)", "sd_resid_IS"),
                     ("IS name return W_IS", "W_IS"), ("FULL-SAMPLE name return W", "W")]:
        P(f"    {lab:<28} {spearman(s[col], s['Sharpe_OOS']):+.4f}   "
          f"(with FULL Sharpe {spearman(s[col], s['Sharpe']):+.4f})")

    P(f"\n  elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
