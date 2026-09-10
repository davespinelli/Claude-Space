#!/usr/bin/env python3
"""Idea 485 - "does-sd-still-survive-the-PARTIAL-t-test-once-the-control-has-DATA" (lane B, 2026-09-10).

The question
------------
Idea 252 ran a partial test of draw dispersion `sd` against a NAME-LEVEL composition control
(136 membership dummies, ridge, fitted OUT OF FOLD) and reported, on the headline cell
(B136, pooled over 150 draws, n=20 CAND Sharpe, OOF, lambda*=2):

    R2(sd) 0.3062 (t +8.08)  ->  pR2(sd | F_oof) 0.2067 (t +6.19),  kill = 0.675

against a pre-registered bar (idea 83's, reused verbatim): `sd` is KILLED iff

    kill = pR2(sd | F_oof) / R2(sd) < 1/3   AND   |t(sd | F_oof)| < 2.

Both legs were missed at every penalty, so idea 252 concluded that `sd` SURVIVES the stronger
control and that idea 83's 62% is structural.

Idea 484 then showed that idea 252's control had almost no DATA: at 50 draws per k cell the
name-additive ridge predicts a draw's Sharpe out of fold at oofR2 +0.20 (B136) and -0.08
(SMALL484); at 500 draws per k cell it reaches +0.88 and +0.59.  Idea 484 said so explicitly and
filed the consequence to the queue rather than asserting it:

    "Whether the partial test still leaves sd alive once the control reaches oofR2 0.88 is a
     genuinely open question and is filed to the queue rather than asserted."

This run answers that.  Idea 252's OWN partial test, its OWN bar, its OWN estimator, on idea
484's committed D=500 grid, at every penalty.

Pre-registered reading (written before any new number was read)
    KILLED-BY-DATA   if at D=500 the OOF scheme meets BOTH of idea 252's legs (kill < 1/3 AND
                     |t| < 2) on the headline cell of a panel: idea 252's survival is then a
                     statement about a powerless control, exactly as leg (3) was a statement
                     about N, and the record must restate it with its D.
    SURVIVES         if kill stays >= 1/3 at D=500 on both panels: dispersion carries something
                     a name-additive composition model does not, and it carries it against a
                     control that now explains 0.88 of the target out of fold.  Idea 252's
                     headline then stands as written.
    SPLIT            anything between - in particular kill falling but staying above 1/3, or the
                     two legs disagreeing - reported with the full ladder and with the N-effect
                     on the t leg separated from the effect on the scale-free leg.

    NOTE, registered in advance because it decides how the two legs must be read: N rises 10x
    along this ladder (150 -> 1500 pooled rows), and a partial t is r * sqrt(N - p - 2) whether
    or not anything about the panel changed.  The |t| < 2 leg therefore gets MECHANICALLY harder
    to clear as the control gets better, which is the opposite of what the bar intends.  `kill`
    is the scale-free leg and is the one that can be read across D.  Both are reported at every
    point, plus `t_at50` - the same partial correlation restated at idea 252's own N - so the
    two effects are never confused.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue's own two
    1. draws  D per k cell in {50, 100, 150, 200, 300, 400, 500} (idea 484's nested ladder).
    2. panel  in {B136, SMALL484}.
    ALL grid points are written to `.partial.csv` (panel x D x scope x y x lambda x scheme) and
    the book-Sharpe ones are printed.  The ridge penalty is NOT a third tuned parameter: the
    whole six-point ladder lambda in {0.5, 2, 8, 32, 128, 512} is reported at every point, and
    idea 252's own IS-cross-validated lambda*=2 is marked where it appears.
    Everything else is idea 78/83/252/484's and is imported unchanged: k in {20,40,80},
    n in {5,20}, the gate, gross 0.75, weekly, 10 bps, next-day execution, the 2009-2016 /
    2017-2026 split, the seeds (SEED_B + k), 10 folds by draw index.

No book is re-run.  Every book metric is READ from idea 484's committed `.grid.csv.gz` (3,000
books), and the membership matrix behind it is REBUILT from the seeds and gated against that
file's own `sd` / `n_elig` columns before any new number is read.

Reproduction gates (run BEFORE any new number is read)
    [a] harness: U56/CAND20 and U56/RULES v1 from engine.backtest.
    [b] MEMBERSHIP: all 3,000 draws re-drawn from `SEED_B + k` on both panels and the four
        membership-derived columns of idea 484's committed grid (`n_elig`, `sd`, `n_elig_IS`,
        `sd_IS`) recomputed from the reconstructed name sets.  If these match, M is provably
        idea 484's own membership matrix and every regression below is on its rows.
    [c] IDEA 252's OWN HEADLINE: the partial test recomputed at D=50 on B136, pooled, n=20 CAND
        Sharpe, and checked against the published table (R2(sd) 0.3062 / t +8.08; OOF lam=2
        kill 0.675 at t +6.19; IS lam=0.5 kill 0.000 at t -0.10).

Walk-forward (PROTOCOL rule 8), selectors fixed before any OOS number was read
    The decision form of this idea's question: does a BETTER-POWERED name-level control change
    the draw you would pick?  Idea 252's S7 (max IS `sd` after the out-of-fold name-level fit of
    IS Sharpe is regressed out) picked the SAME draw as raw dispersion at all six penalties on
    N=50 - the residualisation added no selector content.  Every arm below is re-read at every D
    on the ladder and on both panels; 2009-2016 only feeds the selectors, 2017-2026 is read once.
    S0 do-nothing (whole panel, CAND-n)         S1 IS-Sharpe argmax
    S2 max IS `sd`                              S5 max IS `sd` residualised on the SCALAR W_IS
    S7 max IS `sd` residualised on F_oof (name-level, the arm under test, all six penalties)
    S6 random draw (fixed seed)
    OOS CAGR/Sharpe/MaxDD are reported against SPY and against the live book (RULES v2).

KEEP paths (PROTOCOL rule 4): this run introduces NO new book form - the object under test is a
statistic about drawn sub-panels - but idea 484's 3,000 committed books are scored on both paths
(4a vs the live RULES v2 and vs the superseded v1, 4b vs SPY incl. the OOS leg) so the run states
its own KEEP position from the same rows it regresses.

Survivorship (rule 9): `universe_broad.json` and the sub-$2B panel are CURRENT CONSTITUENTS.
As in ideas 83/252/484 this cuts AGAINST the name-additive control, which is fitted on names
already known to have survived - the most favourable possible sample for a fixed-effect design.
A control that still fails to kill `sd` fails on easy ground.

Deterministic (fixed seeds, folds by draw index), standalone.  Reads baseline.py and engine.py;
modifies nothing.
Run: python3 research/backtests/2026-09-10_does-sd-still-survive-the-PARTIAL-t-test-once-the-control-has-DATA_B.py
"""
import sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

# ---- idea 78/83/252/484's constants, imported verbatim ---------------------------
COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
KS = [20, 40, 80]
N_BOOKS = [5, 20]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_B = 78_500
SEED_S6 = 78_999
N_FOLDS = 10
LAMS = [0.5, 2.0, 8.0, 32.0, 128.0, 512.0]
LAM_STAR = 2.0                      # idea 252's IS-cross-validated penalty

# ---- this run's two tuned parameters ---------------------------------------------
DRAWS = [50, 100, 150, 200, 300, 400, 500]
D_MAX = max(DRAWS)
PANELS = ["B136", "SMALL484"]

KILL_BAR = 1.0 / 3.0
T_BAR = 2.0

SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"
STEM = SCRIPT[:-3]
REF_GRID = OUT / "2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C.grid.csv.gz"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def flush():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- regression helpers (idea 252's, verbatim)
def ols(y, X, names):
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    s2 = float(resid @ resid) / dof
    se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X)) * s2)
    ss = float(((y - y.mean()) ** 2).sum())
    return dict(R2=1.0 - float(resid @ resid) / ss if ss > 0 else np.nan, n=len(y), resid=resid,
                coef=dict(zip(["const"] + names, beta)), t=dict(zip(["const"] + names, beta / se)))


def resid_on(y, x):
    return ols(y, [x], ["x"])["resid"]


def partial_r2(y, x, ctrl):
    """R2 between resid(y|ctrl) and resid(x|ctrl); its t is the t on x in y ~ x + ctrl."""
    ry, rx = resid_on(y, ctrl), resid_on(x, ctrl)
    full = ols(y, [x, ctrl], ["x", "ctrl"])
    r = np.corrcoef(ry, rx)[0, 1]
    return dict(pR2=r ** 2, r=r, t=full["t"]["x"], full_R2=full["R2"], t_ctrl=full["t"]["ctrl"])


def oof_r2(y, pred):
    y = np.asarray(y, float)
    ss = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(((y - pred) ** 2).sum()) / ss if ss > 0 else np.nan


def _ridge_beta(A, Xc, Y, ym, lam, free):
    d = np.full(A.shape[0], float(lam))
    if free:
        d[:free] = 0.0
    return np.linalg.solve(A + np.diag(d), Xc.T @ (Y - ym))


def fit_composition_multi(M, Y, folds, lams, free=0):
    """(F_is, F_oof) for MANY targets sharing one design, per penalty.

    Identical estimator to idea 252's `ridge_fit`/`fit_composition` (unpenalised intercept via
    centring, `free` leading unpenalised columns) - the Gram is simply shared across targets,
    which is what makes 7 x 2 x 4 x 6 x 6 grid points affordable.  Gate [c] is what proves the
    two agree: it reproduces idea 252's published headline row through this function.
    """
    M = np.asarray(M, float); Y = np.asarray(Y, float)
    T, nY = Y.shape
    xm = M.mean(axis=0); Xc = M - xm; A = Xc.T @ Xc
    ym = Y.mean(axis=0)
    F_is = {lam: ym + Xc @ _ridge_beta(A, Xc, Y, ym, lam, free) for lam in lams}
    F_oof = {lam: np.empty((T, nY)) for lam in lams}
    for f in np.unique(folds):
        te = folds == f; tr = np.flatnonzero(~te)
        Xtr = M[tr]; xmt = Xtr.mean(axis=0); Xct = Xtr - xmt; At = Xct.T @ Xct
        Xte = M[te] - xmt; Ytr = Y[tr]; ymt = Ytr.mean(axis=0)
        for lam in lams:
            F_oof[lam][te] = ymt + Xte @ _ridge_beta(At, Xct, Ytr, ymt, lam, free)
    return F_is, F_oof


def t_at_n(r, n, p=3):
    """The same partial correlation restated at sample size n (p = params in the full model)."""
    r = float(np.clip(r, -0.999999, 0.999999))
    return r * np.sqrt(max(n - p, 1) / (1.0 - r * r))


def ann_logret(p):
    """idea 83/252's W, verbatim."""
    out = {}
    for c in p.columns:
        s = p[c].dropna()
        if len(s) < 252 or s.iloc[0] <= 0:
            out[c] = np.nan; continue
        yrs = (s.index[-1] - s.index[0]).days / 365.25
        out[c] = float(np.log(s.iloc[-1] / s.iloc[0]) / yrs)
    return pd.Series(out)


# ================================================================== membership (idea 484's draw order)
def panel_defs():
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    return {
        "B136": (px136, [c for c in px136.columns]),
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),
    }


def draw_names(names, k, d_hi, seed):
    """Draw d is the d-th name set from the generator seeded once per (panel, k) - idea 484's
    nested ladder, verbatim."""
    rng = np.random.default_rng(seed)
    return [list(rng.choice(names, size=k, replace=False)) for _ in range(d_hi)]


def membership_stats(px, cols, startb):
    """Recompute idea 484's four membership-derived columns from a name set (no backtest)."""
    keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
    p = px[keep].dropna(how="all").ffill()
    s, above, vol20 = score(p, vol_scale=False)
    elig = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in p.columns if c not in set(cols)]
    if drop:
        elig[drop] = False
    wm = rebalance_mask(p.index, FREQ).values
    ne = elig[wm].sum(axis=1).loc[startb:]
    mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(elig[cols])
    sdw = mom_p[wm].loc[startb:].std(axis=1)
    return (float(ne.mean()), float(sdw.mean()),
            float(ne.loc[:IS_END].mean()), float(sdw.loc[:IS_END].mean()))


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 210)
    P("IDEA 485 - does-sd-still-survive-the-PARTIAL-t-test-once-the-control-has-DATA (lane B, 2026-09-10)")
    P("Idea 252: sd survives a 136-name out-of-fold composition control, kill 0.675 at t +6.19 (D=50).")
    P("Idea 484: at D=50 that control explains oofR2 +0.20 of the target; at D=500 it explains +0.88.")
    P("Re-run idea 252's OWN partial test, its OWN bar (kill < 1/3 AND |t| < 2), on the D=500 grid.")
    P(f"Ladder D in {DRAWS} per k cell x panels {PANELS} x penalties {LAMS} x schemes IS/OOF.")
    P("=" * 210)

    if not REF_GRID.exists():
        P("    ABORT: idea 484's committed grid is missing."); flush(); return
    G = pd.read_csv(REF_GRID)
    P(f"\nidea 484's committed grid: {len(G)} rows x {G.shape[1]} columns, panels "
      f"{sorted(G.panel.unique())}, k {sorted(G.k.unique())}, draws {G.draw.min()}..{G.draw.max()}")

    # ---------------------------------------------------------------- [a] harness
    P("\n[a] HARNESS - published rows recomputed from engine.backtest before anything new is read")
    px56 = load_universe()
    s56 = px56.index[260]
    sc56, above56, vol56 = score(px56, vol_scale=False)
    e56 = (above56 & (vol56 < MAX_VOL))
    w56 = (sc56.where(e56).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
    r_u56 = backtest(px56, w56, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    m = metrics(r_u56); h1, h2 = half_sharpes(r_u56)
    P(f"    U56/CAND20   {m['CAGR']:.4%} / {m['Sharpe']:.5f} / {m['MaxDD']:.4%}  halves {h1:.5f}/{h2:.5f}"
      f"   (ideas 2/73/77/83/252/484 published 12.7% / 1.092-1.093 / -18.3%)")
    r_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[s56:]
    mv = metrics(r_v1)
    P(f"    U56/RULES v1 {mv['CAGR']:.4%} / {mv['Sharpe']:.5f} / {mv['MaxDD']:.4%}"
      f"   (published 6.5% / 0.664-0.666 / -13.8%)")
    P(f"    u56 window {px56.index[0].date()} -> {px56.index[-1].date()}")
    # `data/prices.csv` has been extended since idea 484 ran (2026-09-04 -> 2026-09-09) while
    # `data/prices_broad.csv` - the panel this run regresses on - has NOT.  The u56 rows
    # therefore drift by three trading days.  Truncated to idea 484's own last date they must
    # reproduce it exactly; that, not the extended row, is the harness check.
    cut = "2026-09-04"
    px56c = px56.loc[:cut]
    scc, abc, volc = score(px56c, vol_scale=False)
    w56c = ((scc.where(abc & (volc < MAX_VOL)).rank(axis=1, ascending=False) <= 20)
            .astype(float) * (GROSS / 20))
    rc = backtest(px56c, w56c, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[px56c.index[260]:]
    mc = metrics(rc)
    rc1 = backtest(px56c, rules_v1_weights(px56c), cost_bps=COST_BPS,
                   freq=FREQ)["returns"].loc[px56c.index[260]:]
    mc1 = metrics(rc1)
    P(f"    u56 truncated to {cut}:  CAND20 {mc['CAGR']:.4%} / {mc['Sharpe']:.5f} / {mc['MaxDD']:.4%}"
      f"   (idea 484 published 12.6530% / 1.09172 / -18.3083%)")
    P(f"                             RULES v1 {mc1['CAGR']:.4%} / {mc1['Sharpe']:.5f} / {mc1['MaxDD']:.4%}"
      f"   (idea 484 published 6.4194% / 0.66110 / -13.8278%)")
    ok_a = abs(mc["Sharpe"] - 1.09172) < 1e-4 and abs(mc1["Sharpe"] - 0.66110) < 1e-4
    P(f"    HARNESS {'PASS - idea 484s u56 rows reproduce exactly on its own window' if ok_a else 'DRIFT'}")
    if not ok_a:
        P(f"      u56 CAND20 Sharpe {mc['Sharpe'] - 1.09172:+.5f}, RULES v1 Sharpe "
          f"{mc1['Sharpe'] - 0.66110:+.5f} against idea 484's published rows ON ITS OWN LAST DATE,")
        P("      i.e. data/prices.csv has been RESTATED since 2026-09-09, not merely extended.")
        P("      The u56 panel plays NO part in this run's regressions - every row regressed below")
        P("      comes from prices_broad.csv / prices_small.csv - so gate [a] is reported as")
        P("      INFORMATIONAL and the BINDING gates are [b] (membership, 1e-9) and [c] (idea 252's")
        P("      published headline, reproduced exactly).  If [b] passes, the object under test is")
        P("      byte-for-byte idea 484's.")

    # ---------------------------------------------------------------- panels and comparands
    panels = panel_defs()
    ctx = {}
    for pan, (px, names) in panels.items():
        startb = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[startb:]
        b1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        b2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
        ms = metrics(spy); s1, s2 = half_sharpes(spy)
        m1 = metrics(b1); a1, a2 = half_sharpes(b1)
        m2 = metrics(b2); c1, c2 = half_sharpes(b2)
        ctx[pan] = dict(px=px, names=names, startb=startb,
                        spy=dict(CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"], H1=s1, H2=s2,
                                 OOS=metrics(spy.loc[OOS_START:])["Sharpe"]),
                        v1=dict(Sharpe=m1["Sharpe"], MaxDD=m1["MaxDD"], H1=a1, H2=a2,
                                CAGR=m1["CAGR"], OOS=metrics(b1.loc[OOS_START:])["Sharpe"]),
                        v2=dict(Sharpe=m2["Sharpe"], MaxDD=m2["MaxDD"], H1=c1, H2=c2, CAGR=m2["CAGR"],
                                OOS=metrics(b2.loc[OOS_START:])["Sharpe"],
                                OOS_CAGR=metrics(b2.loc[OOS_START:])["CAGR"],
                                OOS_MaxDD=metrics(b2.loc[OOS_START:])["MaxDD"]))
        P(f"\n    {pan}: {len(names)} tradable names, window {startb.date()} -> {px.index[-1].date()} "
          f"({len(spy)} days)")
        P(f"      SPY             {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  "
          f"halves {s1:.3f}/{s2:.3f}  OOS {ctx[pan]['spy']['OOS']:.3f}")
        P(f"      RULES v1        {m1['CAGR']:.2%} / {m1['Sharpe']:.3f} / {m1['MaxDD']:.2%}  "
          f"halves {a1:.3f}/{a2:.3f}  OOS {ctx[pan]['v1']['OOS']:.3f}")
        P(f"      RULES v2 (live) {m2['CAGR']:.2%} / {m2['Sharpe']:.3f} / {m2['MaxDD']:.2%}  "
          f"halves {c1:.3f}/{c2:.3f}  OOS {ctx[pan]['v2']['OOS']:.3f}")
        P(f"      4b bars: MaxDD <= {0.60 * abs(ms['MaxDD']):.2%}, CAGR >= {0.70 * ms['CAGR']:.2%}, "
          f"H1 > {s1:.3f}, H2 > {s2:.3f}, OOS Sharpe > {ctx[pan]['spy']['OOS']:.3f}")

    # ---------------------------------------------------------------- [b] membership gate
    P("\n" + "=" * 210)
    P("[b] MEMBERSHIP GATE - all 3,000 draws re-drawn from SEED_B+k on both panels and idea 484's")
    P("    four membership-derived columns recomputed from the reconstructed name sets (no backtest).")
    P("=" * 210)
    COLS = {}
    diffs = {c: 0.0 for c in ["n_elig", "sd", "n_elig_IS", "sd_IS"]}
    nrows = 0
    for pan in PANELS:
        c = ctx[pan]
        for k in KS:
            sets = draw_names(c["names"], k, D_MAX, SEED_B + k)
            ref = G[(G.panel == pan) & (G.k == k)].set_index("draw").sort_index()
            for d, cols in enumerate(sets):
                COLS[(pan, k, d)] = cols
                got = membership_stats(c["px"], cols, c["startb"])
                r = ref.loc[d]
                for nm, v in zip(["n_elig", "sd", "n_elig_IS", "sd_IS"], got):
                    diffs[nm] = max(diffs[nm], abs(v - float(r[nm])))
                nrows += 1
            P(f"    {pan} k={k:<3} {D_MAX} draws checked ({time.time() - t0:.0f}s)")
    P(f"    {nrows} rows; max abs difference by column:")
    for nm, v in diffs.items():
        P(f"      {nm:<10} {v:.3e}")
    ok_b = max(diffs.values()) < 1e-9 and nrows == 3000
    P(f"    MEMBERSHIP {'PASS - M is provably idea 484s own membership matrix' if ok_b else 'FAIL'}")
    P("    (this is the BINDING gate: it proves both the name sets AND the two price panels this")
    P("     run regresses on are exactly the ones idea 484's committed grid was built from.)")

    # membership matrices, and idea 83's scalar control W on both panels
    MM = {}; WW = {}
    for pan in PANELS:
        c = ctx[pan]; names = c["names"]; idxn = {x: i for i, x in enumerate(names)}
        M = np.zeros((len(KS) * D_MAX, len(names)))
        rowmap = {}
        i = 0
        for k in KS:
            for d in range(D_MAX):
                for x in COLS[(pan, k, d)]:
                    M[i, idxn[x]] = 1.0
                rowmap[(k, d)] = i
                i += 1
        MM[pan] = (M, rowmap)
        lr_full = ann_logret(c["px"][names].loc[c["startb"]:])
        lr_is = ann_logret(c["px"][names].loc[c["startb"]:IS_END])
        WW[pan] = (np.array([float(lr_full[COLS[(pan, k, d)]].mean()) for k in KS for d in range(D_MAX)]),
                   np.array([float(lr_is[COLS[(pan, k, d)]].mean()) for k in KS for d in range(D_MAX)]))
        cnt = M.sum(axis=0)
        P(f"    {pan}: P={len(names)} name columns, {len(M)} rows; name appearance count "
          f"min/median/max {int(cnt.min())}/{int(np.median(cnt))}/{int(cnt.max())}; "
          f"N/P per k cell at D=50 {50 / len(names):.2f}, at D={D_MAX} {D_MAX / len(names):.2f}")

    # ---------------------------------------------------------------- the regression rows
    # idea 484's grid re-ordered to the membership row order (k block, then draw) once
    GP = {}
    for pan in PANELS:
        GP[pan] = (G[G.panel == pan].sort_values(["k", "draw"]).reset_index(drop=True))
        assert list(GP[pan].k) == [kk for kk in KS for _ in range(D_MAX)]
        assert list(GP[pan].draw) == list(range(D_MAX)) * len(KS)

    def block(pan, D, k=None):
        """Rows for one (panel, D, scope) cell, ordered as idea 252 ordered them."""
        M, rowmap = MM[pan]; Wf, Wi = WW[pan]
        ks = KS if k is None else [k]
        idx = [rowmap[(kk, d)] for kk in ks for d in range(D)]
        rows = GP[pan].iloc[idx].reset_index(drop=True)
        X = M[idx]
        free = 0
        if k is None:                                  # pooled rows mix k: 2 unpenalised k dummies
            kd = np.column_stack([np.array([kk == KS[1] for kk in ks for _ in range(D)], float),
                                  np.array([kk == KS[2] for kk in ks for _ in range(D)], float)])
            X = np.column_stack([kd, X]); free = 2
        folds = np.arange(len(idx)) % N_FOLDS
        return rows, X, free, folds, Wf[idx], Wi[idx]

    YDEF = [(nb, kind) for nb in N_BOOKS for kind in ("CAND Sharpe", "EWall Sharpe", "premium")]

    def ycol(nb, kind):
        return {"CAND Sharpe": f"Sharpe{nb}", "EWall Sharpe": "ew_Sharpe", "premium": f"premium{nb}"}[kind]

    def run_cell(pan, D, k):
        """Every (y, lambda, scheme) point of one (panel, D, scope) cell."""
        rows, X, free, folds, Wf, Wi = block(pan, D, k)
        sdv = rows["sd"].values.astype(float)
        Y = np.column_stack([rows[ycol(nb, kind)].values.astype(float) for nb, kind in YDEF])
        F_is, F_oof = fit_composition_multi(X, Y, folds, LAMS, free)
        # power: how much of sd itself the control carries, on the same design and folds
        Fp_is, Fp_oof = fit_composition_multi(X, sdv.reshape(-1, 1), folds, LAMS, free)
        out = []
        for j, (nb, kind) in enumerate(YDEF):
            y = Y[:, j]
            u = ols(y, [sdv], ["sd"])
            pw = partial_r2(y, sdv, Wf)
            pwi = partial_r2(y, sdv, Wi)
            for lam in LAMS:
                for scheme, F in (("IS", F_is[lam][:, j]), ("OOF", F_oof[lam][:, j])):
                    pr = partial_r2(y, sdv, F)
                    out.append(dict(
                        panel=pan, D=D, scope="pooled" if k is None else f"k={k}", n=nb, y=kind,
                        N=len(y), lam=lam, scheme=scheme,
                        R2_sd=u["R2"], t_sd=u["t"]["sd"],
                        R2_F=oof_r2(y, F),
                        R2_sd_from_M=oof_r2(sdv, (Fp_is if scheme == "IS" else Fp_oof)[lam][:, 0]),
                        pR2_sd_given_F=pr["pR2"], r_sd_given_F=pr["r"], t_sd_given_F=pr["t"],
                        t50_sd_given_F=t_at_n(pr["r"], 50), t_F_given_sd=pr["t_ctrl"],
                        kill_F=pr["pR2"] / u["R2"] if u["R2"] > 0 else np.nan,
                        kill_W=pw["pR2"] / u["R2"] if u["R2"] > 0 else np.nan, t_sd_given_W=pw["t"],
                        kill_WIS=pwi["pR2"] / u["R2"] if u["R2"] > 0 else np.nan))
        return out

    # ---------------------------------------------------------------- [c] idea 252's headline
    P("\n" + "=" * 210)
    P("[c] IDEA 252's OWN HEADLINE, recomputed at D=50 on B136, pooled, n=20 CAND Sharpe")
    P("    published: R2(sd) 0.3062 (t +8.08); OOF lam=2 kill 0.675 at t +6.19; IS lam=0.5 kill 0.000 at t -0.10")
    P("=" * 210)
    head = pd.DataFrame(run_cell("B136", 50, None))
    hh = head[(head.n == 20) & (head.y == "CAND Sharpe")]
    P(fmt(hh.set_index(["scheme", "lam"])[["N", "R2_sd", "t_sd", "R2_F", "pR2_sd_given_F",
                                           "t_sd_given_F", "t_F_given_sd", "kill_F", "kill_W"]].sort_index()))
    ref_ok = []
    r0 = hh[(hh.scheme == "OOF") & (hh.lam == LAM_STAR)].iloc[0]
    ref_ok.append(("R2_sd 0.3062", abs(r0.R2_sd - 0.3062) < 5e-4))
    ref_ok.append(("t_sd +8.08", abs(r0.t_sd - 8.08) < 5e-2))
    ref_ok.append(("OOF lam=2 kill 0.675", abs(r0.kill_F - 0.675) < 1e-3))
    ref_ok.append(("OOF lam=2 t +6.19", abs(r0.t_sd_given_F - 6.19) < 1e-2))
    r1 = hh[(hh.scheme == "IS") & (hh.lam == 0.5)].iloc[0]
    ref_ok.append(("IS lam=0.5 kill 0.000", abs(r1.kill_F - 0.000) < 1e-3))
    ref_ok.append(("IS lam=0.5 t -0.10", abs(r1.t_sd_given_F + 0.10) < 1e-2))
    ref_ok.append(("kill_W 0.620", abs(r0.kill_W - 0.620) < 1e-3))
    for nm, v in ref_ok:
        P(f"      {nm:<24} {'PASS' if v else 'FAIL'}")
    ok_c = all(v for _, v in ref_ok)
    P(f"    IDEA 252 HEADLINE {'PASS - this run is running idea 252s estimator on idea 252s rows' if ok_c else 'FAIL'}")

    if not (ok_b and ok_c):
        P("\n    ABORT: the object under test is not the published one.")
        flush(); return

    # ---------------------------------------------------------------- THE TEST
    P("\n" + "=" * 210)
    P("THE TEST - idea 252's partial test up the draw ladder.  Bar (idea 83/252's, verbatim):")
    P("    sd is KILLED iff kill = pR2(sd|F_oof)/R2(sd) < 1/3 AND |t(sd|F_oof)| < 2.")
    P("Every panel x D x scope x y x lambda x scheme point is written to .partial.csv.")
    P("=" * 210)
    allrows = []
    for pan in PANELS:
        for D in DRAWS:
            for k in [None] + KS:
                allrows += run_cell(pan, D, k)
            P(f"    {pan} D={D:<4} done ({time.time() - t0:.0f}s)")
    R = pd.DataFrame(allrows)
    R.to_csv(OUT / f"{STEM}.partial.csv", index=False)
    P(f"    {len(R)} grid points written to {STEM}.partial.csv")

    # -- headline ladder: pooled, n=20 CAND Sharpe, OOF
    P("\n" + "-" * 210)
    P("HEADLINE LADDER - pooled, n=20 CAND Sharpe, OUT-OF-FOLD scheme, every penalty, every D.")
    P("R2_F = the control's own out-of-fold R2 (idea 484's power axis); R2_sd_from_M = how much of")
    P("sd the control carries; kill_F = idea 252's leg 1; t50 = the same partial r restated at N=50.")
    P("-" * 210)
    for pan in PANELS:
        P(f"\n  {pan}")
        h = R[(R.panel == pan) & (R.scope == "pooled") & (R.n == 20) & (R.y == "CAND Sharpe")
              & (R.scheme == "OOF")]
        P(fmt(h.pivot_table(index=["D", "N"], columns="lam",
                            values="R2_F").rename_axis(columns="R2_F  lam")))
        P(fmt(h.pivot_table(index=["D", "N"], columns="lam",
                            values="kill_F").rename_axis(columns="kill_F  lam")))
        P(fmt(h.pivot_table(index=["D", "N"], columns="lam",
                            values="t_sd_given_F").rename_axis(columns="t(sd|F)  lam")))
        P(fmt(h.pivot_table(index=["D", "N"], columns="lam",
                            values="t50_sd_given_F").rename_axis(columns="t50(sd|F)  lam")))
        P(fmt(h.pivot_table(index=["D", "N"], columns="lam",
                            values="R2_sd_from_M").rename_axis(columns="oofR2(sd~M)  lam")))
        st = h[h.lam == LAM_STAR].set_index("D")
        P(f"    at idea 252's lam*={LAM_STAR:g}:  D=50 kill {st.loc[50, 'kill_F']:.4f} t {st.loc[50, 't_sd_given_F']:+.2f}"
          f"   ->   D={D_MAX} kill {st.loc[D_MAX, 'kill_F']:.4f} t {st.loc[D_MAX, 't_sd_given_F']:+.2f}"
          f"   (control oofR2 {st.loc[50, 'R2_F']:+.4f} -> {st.loc[D_MAX, 'R2_F']:+.4f})")

    # -- the verdict census over every book-Sharpe point
    P("\n" + "-" * 210)
    P("VERDICT CENSUS - idea 252's bar applied to every OOF book-Sharpe point (CAND + EWall Sharpe,")
    P("both n, 4 scopes, 6 penalties) at each D.  KILLED = kill < 1/3 AND |t| < 2 (both legs).")
    P("-" * 210)
    bk = R[(R.scheme == "OOF") & (R.y.isin(["CAND Sharpe", "EWall Sharpe"]))].copy()
    bk["leg_kill"] = bk.kill_F < KILL_BAR
    bk["leg_t"] = bk.t_sd_given_F.abs() < T_BAR
    bk["leg_t50"] = bk.t50_sd_given_F.abs() < T_BAR
    bk["KILLED"] = bk.leg_kill & bk.leg_t
    bk["KILLED_at50"] = bk.leg_kill & bk.leg_t50
    cen = bk.groupby(["panel", "D"]).agg(
        points=("kill_F", "size"), kill_med=("kill_F", "median"),
        kill_min=("kill_F", "min"), kill_max=("kill_F", "max"),
        leg1_kill_lt_third=("leg_kill", "sum"), leg2_absT_lt_2=("leg_t", "sum"),
        leg2_absT50_lt_2=("leg_t50", "sum"), KILLED=("KILLED", "sum"),
        KILLED_at_N50=("KILLED_at50", "sum"),
        ctrl_oofR2_med=("R2_F", "median"), sd_carried_med=("R2_sd_from_M", "median")).reset_index()
    P(fmt(cen.set_index(["panel", "D"])))
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)

    P("\n  the same census on the IN-SAMPLE scheme (idea 252's known artefact, for contrast):")
    bi = R[(R.scheme == "IS") & (R.y.isin(["CAND Sharpe", "EWall Sharpe"]))].copy()
    bi["KILLED"] = (bi.kill_F < KILL_BAR) & (bi.t_sd_given_F.abs() < T_BAR)
    P(fmt(bi.groupby(["panel", "D"]).agg(points=("kill_F", "size"), kill_med=("kill_F", "median"),
                                         KILLED=("KILLED", "sum"),
                                         sd_carried_med=("R2_sd_from_M", "median")).reset_index()
          .set_index(["panel", "D"])))

    # -- the two legs, separated
    P("\n" + "-" * 210)
    P("THE TWO LEGS, SEPARATED - kill_F is scale-free, |t| is not (N rises 10x up the ladder).")
    P("-" * 210)
    lg = bk.groupby(["panel", "D"]).agg(N=("N", "median"), kill_med=("kill_F", "median"),
                                        t_med=("t_sd_given_F", "median"),
                                        t50_med=("t50_sd_given_F", "median")).reset_index()
    P(fmt(lg.set_index(["panel", "D"])))
    for pan in PANELS:
        s = lg[lg.panel == pan]
        k0 = float(s[s.D == 50].kill_med.iloc[0]); k1 = float(s[s.D == D_MAX].kill_med.iloc[0])
        P(f"    {pan}: median kill {k0:.4f} (D=50) -> {k1:.4f} (D={D_MAX}), change {k1 - k0:+.4f}; "
          f"bar is {KILL_BAR:.4f}")

    # -- scalar control reference
    P("\n  idea 83's SCALAR control (W) on the same rows, for reference - it does not gain power with D:")
    sc = R[(R.scheme == "OOF") & (R.lam == LAM_STAR) & (R.y.isin(["CAND Sharpe", "EWall Sharpe"]))]
    P(fmt(sc.groupby(["panel", "D"]).agg(kill_W_med=("kill_W", "median"),
                                         kill_WIS_med=("kill_WIS", "median"),
                                         kill_F_med=("kill_F", "median")).reset_index()
          .set_index(["panel", "D"])))

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 210)
    P("RULE 8 WALK-FORWARD - selectors fitted on 2009-2016 ONLY; 2017-2026 read once, at the end.")
    P("The decision form of this idea: does a BETTER-POWERED control change the draw you pick?")
    P("=" * 210)
    # S0: the whole panel, CAND-n, computed once per panel
    S0 = {}
    for pan in PANELS:
        c = ctx[pan]; px = c["px"]; nm = set(c["names"])
        s, above, vol20 = score(px, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [x for x in px.columns if x not in nm]
        if drop:
            elig[drop] = False
        rank = s.where(elig).rank(axis=1, ascending=False)
        for nb in N_BOOKS:
            w = (rank <= nb).astype(float) * (GROSS / nb)
            r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[c["startb"]:]
            oo = metrics(r.loc[OOS_START:])
            S0[(pan, nb)] = dict(CAGR=oo["CAGR"], Sharpe=oo["Sharpe"], MaxDD=oo["MaxDD"])
        P(f"    {pan} S0 do-nothing computed ({time.time() - t0:.0f}s)")

    wf = []
    rng6 = np.random.default_rng(SEED_S6)
    for pan in PANELS:
        M, rowmap = MM[pan]; Wf, Wi = WW[pan]
        for D in DRAWS:
            for nb in N_BOOKS:
                for k in KS:
                    idx = [rowmap[(k, d)] for d in range(D)]
                    rows = GP[pan].iloc[idx].reset_index(drop=True)
                    X = M[idx]; folds = np.arange(D) % N_FOLDS
                    sd_is = rows["sd_IS"].values.astype(float)
                    sh_is = rows[f"Sharpe_IS{nb}"].values.astype(float)
                    wis = Wi[idx]
                    _, Fo = fit_composition_multi(X, sh_is.reshape(-1, 1), folds, LAMS, 0)

                    def emit(arm, pick, lam=np.nan):
                        r = rows.iloc[pick]
                        wf.append(dict(panel=pan, D=D, k=k, n=nb, arm=arm, lam=lam, pick=int(r.name),
                                       OOS_CAGR=float(r[f"CAGR_OOS{nb}"]),
                                       OOS_Sharpe=float(r[f"Sharpe_OOS{nb}"]),
                                       OOS_MaxDD=float(r[f"MaxDD_OOS{nb}"])))

                    emit("S1 IS-Sharpe argmax", int(np.argmax(sh_is)))
                    emit("S2 max IS sd", int(np.argmax(sd_is)))
                    emit("S5 sd | W_IS (scalar)", int(np.argmax(resid_on(sd_is, wis))))
                    for lam in LAMS:
                        emit("S7 sd | F_oof (name-level)",
                             int(np.argmax(resid_on(sd_is, Fo[lam][:, 0]))), lam)
                    emit("S6 random", int(rng6.integers(D)))
                    s0 = S0[(pan, nb)]
                    wf.append(dict(panel=pan, D=D, k=k, n=nb, arm="S0 do-nothing", lam=np.nan, pick=-1,
                                   OOS_CAGR=s0["CAGR"], OOS_Sharpe=s0["Sharpe"], OOS_MaxDD=s0["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"    {len(WF)} rule-8 rows written to {STEM}.walkforward.csv")

    for pan in PANELS:
        c = ctx[pan]
        P(f"\n  {pan}  (SPY OOS Sharpe {c['spy']['OOS']:.4f}; live RULES v2 OOS "
          f"{c['v2']['OOS_CAGR']:.2%} / {c['v2']['OOS']:.4f} / {c['v2']['OOS_MaxDD']:.2%})")
        w = WF[WF.panel == pan].copy()
        w["beats_SPY"] = w.OOS_Sharpe > c["spy"]["OOS"]
        w["beats_v2"] = w.OOS_Sharpe > c["v2"]["OOS"]
        agg = w.groupby("arm").agg(rows=("OOS_Sharpe", "size"), OOS_CAGR=("OOS_CAGR", "mean"),
                                   OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                                   beats_SPY=("beats_SPY", "sum"), beats_v2=("beats_v2", "sum"))
        P(fmt(agg))
        P("    S7 (name-level residualised) vs S2 (raw sd) - does the control change the PICK?")
        for lam in LAMS:
            a = w[(w.arm == "S7 sd | F_oof (name-level)") & (w.lam == lam)].set_index(["D", "k", "n"])
            b = w[w.arm == "S2 max IS sd"].set_index(["D", "k", "n"])
            j = a.join(b, rsuffix="_s2")
            same = int((j["pick"] == j["pick_s2"]).sum())
            P(f"      lam={lam:<6g} same pick {same}/{len(j)}   mean dOOS Sharpe "
              f"{float((j.OOS_Sharpe - j.OOS_Sharpe_s2).mean()):+.4f}")
        P("    by D (S7 at lam*, vs S2):")
        for D in DRAWS:
            a = w[(w.arm == "S7 sd | F_oof (name-level)") & (w.lam == LAM_STAR) & (w.D == D)].set_index(["k", "n"])
            b = w[(w.arm == "S2 max IS sd") & (w.D == D)].set_index(["k", "n"])
            j = a.join(b, rsuffix="_s2")
            P(f"      D={D:<4} same pick {int((j['pick'] == j['pick_s2']).sum())}/{len(j)}  "
              f"S7 mean OOS Sharpe {j.OOS_Sharpe.mean():.4f}  S2 {j.OOS_Sharpe_s2.mean():.4f}")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 210)
    P("BOTH KEEP PATHS (PROTOCOL rule 4) on idea 484's 3,000 committed books.  No new book form is")
    P("introduced by this run - the object under test is a statistic about drawn sub-panels.")
    P("=" * 210)
    kp = []
    for pan in PANELS:
        c = ctx[pan]; spy = c["spy"]
        sub = G[G.panel == pan]
        for nb in N_BOOKS:
            h1 = sub[f"H1_{nb}"].values; h2 = sub[f"H2_{nb}"].values
            dd = sub[f"MaxDD{nb}"].values; cg = sub[f"CAGR{nb}"].values
            oos = sub[f"Sharpe_OOS{nb}"].values
            for lab, base in (("v1", c["v1"]), ("v2 (live)", c["v2"])):
                p4a = (h1 > base["H1"]) & (h2 > base["H2"]) & (dd >= base["MaxDD"])
                if lab == "v2 (live)":
                    pass4a = p4a
                kp.append(dict(panel=pan, book=f"CAND-{nb}", N=len(sub), comparand=lab,
                               path="4a", passes=int(p4a.sum())))
            p4b = ((h1 > spy["H1"]) & (h2 > spy["H2"]) & (oos > spy["OOS"])
                   & (dd >= -0.60 * abs(spy["MaxDD"])) & (cg >= 0.70 * spy["CAGR"]))
            kp.append(dict(panel=pan, book=f"CAND-{nb}", N=len(sub), comparand="SPY",
                           path="4b", passes=int(p4b.sum())))
            kp.append(dict(panel=pan, book=f"CAND-{nb}", N=len(sub), comparand="both",
                           path="4a(v2)+4b", passes=int((pass4a & p4b).sum())))
    KP = pd.DataFrame(kp)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(fmt(KP.pivot_table(index=["panel", "book", "N"], columns=["path", "comparand"],
                         values="passes", aggfunc="sum")))
    P("\n    NO KEEP-CANDIDATE IS CLAIMED BY THIS RUN.  It re-runs a REGRESSION on committed books;")
    P("    every book above is idea 484's, already scored and already declined there (its single")
    P("    both-paths book is one random 20-name list found by scanning 3,000 sub-panels).")

    P(f"\nElapsed {time.time() - t0:.0f}s")
    flush()


if __name__ == "__main__":
    main()
