#!/usr/bin/env python3
"""Idea 487 — IS A DRAW'S *IS SHARPE* THE WRONG THING TO *PREDICT*?

Idea 484 settled the FIT question: on the D=500 grid the 136-name additive ridge beats one
dispersion number at predicting a draw's IS Sharpe out of fold by up to +0.6 R2.  It also
found that winning the fit does not win the CHOICE — no selector arm beat the live book on
either panel.  Those two facts are only compatible if IS Sharpe is not the thing worth
predicting.  This run tests that directly, and it tests it BEFORE the out-of-sample window
is touched, exactly as the queue asks:

    fit the same three models to a purely IS-side target — the FIRST half of the in-sample
    window's Sharpe — and score them on the SECOND half of the in-sample window.

If a draw's Sharpe does not transfer from 2009-2012 to 2013-2016, where both windows are
in-sample and no OOS information exists anywhere in the exercise, then sub-panel choice is a
null on this grid and the record should stop selecting on it — no OOS reading required.

Pre-registration (fixed before any number was read):

  * TWO tuned parameters and no more — the queue's own two:
      TARGET  FIT      fit y = IS Sharpe,  score out of fold on IS Sharpe   (idea 484's headline)
              IS1_IS2  fit y = IS1 Sharpe, score on IS2 Sharpe              (THE QUESTION)
              IS_OOS   fit y = IS Sharpe,  score on OOS Sharpe              (the record's choice)
      PANEL   B136 | SMALL439
    k (20/40/80), book size n (5/20), the model set, the fold count, the ridge penalty
    ladder, the cost rung (10/25 bps) and the selector set are REPORTED at every point,
    never chosen.  Every grid point is written to disk.

  * MODELS — idea 252's three, unchanged:
      sd     out-of-fold OLS on one dispersion number (IS-side)
      M      out-of-fold ridge on the P name-membership dummies, penalty by NESTED inner
             5-fold CV inside each training fold (the held-out fold never sees the choice)
      M+sd   the same ridge with sd entering unpenalised
    Folds are draw index % 10, so the fold map is identical across targets and models.
    Reported per cell: out-of-fold R2 against the scoring target AND Spearman rho, because a
    CHOICE uses only the ordering and R2 punishes a scale shift a chooser never pays.

  * THE NULL EVERY MODEL MUST BEAT — the raw statistic itself: rho(IS1 Sharpe, IS2 Sharpe)
    and rho(IS Sharpe, OOS Sharpe).  If the target does not autocorrelate across windows, no
    model of it can transfer, and that is the queue's "nothing transfers even inside IS".

  * THE CHOICE LEG — six selectors per (panel, k, n, rung), all pre-registered:
      S0 do-nothing (the whole panel's CAND-n book, no draw chosen)
      S1 argmax IS Sharpe            S2 argmax IS sd
      S3 argmax oof prediction (sd)  S4 argmax oof prediction (M)   S5 argmax oof (M+sd)
    Scored twice: the IS-ONLY tournament (choose on IS1 quantities, read IS2) and the rule-8
    tournament (choose on IS quantities, read 2017-01-01.. ONCE).

  * BOTH KEEP PATHS on every scored book.  4a against the LIVE book (native RULES v2 on the
    same panel, window and rung).  4b against SPY (Sharpe > SPY in BOTH halves AND OOS,
    MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's).

  * RULE 8 (PROTOCOL 8): every selector input is computed on 2009-2016 (SMALL: 2011-2016)
    ONLY; 2017-01-01.. is read once, at the end.  OOS CAGR/Sharpe/MaxDD reported against
    native RULES v2 and SPY on the same OOS window.

REPRODUCTION GATES (run before any new number is read):
  G1 fast_backtest vs engine.backtest on 6 drawn books.
  G2 the regenerated B136 grid vs idea 484's committed grid.csv.gz, column by column, on all
     1,500 B136 rows — the draws are the same generator (SEED_B + k) so this must be exact.
  G3 idea 484's SMALL panel is re-read as it stands today and its row count reported: if the
     cached panel has moved since 2026-09-09 the SMALL rows are NOT gated, and that is said.
  G4 IS1 and IS2 partition the IS window exactly (no overlap, no gap, both non-empty).

SURVIVORSHIP (idea 54, carried): B136 and the small panel are CURRENT-constituent lists, so
their LEVELS are biased upward; only within-panel contrasts (draw vs draw, model vs model in
the same window) are load-bearing.  SMALL439 drops the 44 sub-$2B names with max_1d_move
>= 1.0 (data/small_meta.csv) BEFORE any draw is taken, which is why it is NOT idea 484's
SMALL484 and is gated separately.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .grid.csv.gz, .models.csv, .null.csv, .choice.csv,
.walkforward.csv, .console.txt.
"""
import sys
import time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-10_is-a-draw-s-IS-SHARPE-the-wrong-thing-to-PREDICT_cloud"
OUT = ROOT / "research" / "backtests"
REF484 = OUT / "2026-09-09_does-one-dispersion-number-really-out-predict-136-name-dummies_C.grid.csv.gz"

# idea 78/83/252/484's constants, imported verbatim
FREQ = "W"; MAX_VOL = 0.60; GROSS = 0.75
KS = [20, 40, 80]; N_BOOKS = [5, 20]
IS_END = "2016-12-31"; OOS_START = "2017-01-01"
SEED_B = 78_500
N_FOLDS = 10
LAMS = [0.5, 2.0, 8.0, 32.0, 128.0, 512.0]
D_MAX = 500
BPS = [10, 25]
PANELS = ["B136", "SMALL439"]
TARGETS = ["FIT", "IS1_IS2", "IS_OOS"]
MODELS = ["sd", "M", "M+sd"]
SELECTORS = ["S0 do-nothing", "S1 IS Sharpe", "S2 IS sd", "S3 pred sd", "S4 pred M", "S5 pred M+sd"]

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _console.append(s)


# ------------------------------------------------------------------ idea 484's book helpers
def fast_backtest(prices, weights, freq=FREQ):
    """Idea 484's vectorised twin of engine.backtest, at ZERO cost plus the turnover path."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ------------------------------------------------------------------ idea 252's regressions
def oof_r2(y, pred):
    y = np.asarray(y, float); pred = np.asarray(pred, float)
    ss = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(((y - pred) ** 2).sum()) / ss if ss > 0 else np.nan


def spearman(a, b):
    """Rank correlation as the Pearson correlation of ranks (ties averaged) — no scipy."""
    ra = pd.Series(np.asarray(a, float)).rank()
    rb = pd.Series(np.asarray(b, float)).rank()
    return float(ra.corr(rb))


def _solve_multi(A, Xc, Y, ym, lam, free):
    """Idea 484's estimator, verbatim — kept as the reference the fast path is gated against."""
    d = np.full(A.shape[0], float(lam))
    if free: d[:free] = 0.0
    return np.linalg.solve(A + np.diag(d), Xc.T @ (Y - ym))


class RidgeOOF:
    """Out-of-fold ridge with a NESTED inner-CV penalty, precomputed per fold.

    The design and the fold map are identical across every target in a (panel, k) cell, so the
    Gram eigendecomposition — the only expensive step — is computed ONCE here and reused for
    every y and every lambda.  Mathematically identical to idea 484's `_solve_multi` path
    (gated at G5): with a free (unpenalised) leading column x, the Schur complement of the
    normal equations residualises x out of M and y, so beta solves a plain ridge on the
    residualised design and beta0 is recovered afterwards.
    """

    def __init__(self, M, folds, x=None, inner_k=5):
        self.M = M; self.folds = folds; self.x = x; self.inner_k = inner_k
        self.blocks = []
        for f in np.unique(folds):
            te = folds == f; tr = np.flatnonzero(~te)
            outer = self._prep(tr, np.flatnonzero(te))
            inner = np.arange(len(tr)) % inner_k
            inners = []
            for g in range(inner_k):
                ite = inner == g
                inners.append(self._prep(tr[~ite], tr[ite]))
            self.blocks.append((te, tr, outer, inners))

    def _prep(self, tr, te):
        Mtr = self.M[tr]; mm = Mtr.mean(axis=0); Mc = Mtr - mm
        Mte = self.M[te] - mm
        if self.x is None:
            A = Mc.T @ Mc
            w, V = np.linalg.eigh(A)
            return dict(tr=tr, te=te, Mc=Mc, Mte=Mte, w=w, V=V, free=False, Mt=Mc)
        xtr = self.x[tr]; xb = xtr.mean(); xc = xtr - xb
        a = 1.0 / float(xc @ xc)
        xM = xc @ Mc
        Mt = Mc - np.outer(xc, a * xM)                 # M residualised on the free column
        A = Mt.T @ Mt
        w, V = np.linalg.eigh(A)
        return dict(tr=tr, te=te, Mc=Mc, Mte=Mte, w=w, V=V, free=True,
                    xc=xc, a=a, xte=self.x[te] - xb, Mt=Mt)

    @staticmethod
    def _fit(b, y, lam):
        yb = float(y.mean()); yc = y - yb
        rhs = b["V"].T @ (b["Mt"].T @ yc)
        beta = b["V"] @ (rhs / (b["w"] + lam))
        if not b["free"]:
            return yb, 0.0, beta
        beta0 = b["a"] * float(b["xc"] @ (yc - b["Mc"] @ beta))
        return yb, beta0, beta

    @staticmethod
    def _pred(b, fit):
        yb, beta0, beta = fit
        p = yb + b["Mte"] @ beta
        if b["free"]:
            p = p + beta0 * b["xte"]
        return p

    def predict(self, y):
        y = np.asarray(y, float)
        out = np.empty(len(y))
        for te, tr, outer, inners in self.blocks:
            pos = {v: i for i, v in enumerate(tr)}
            best, bl = -np.inf, LAMS[0]
            for lam in LAMS:
                ip = np.empty(len(tr))
                for ib in inners:
                    p = self._pred(ib, self._fit(ib, y[ib["tr"]], lam))
                    ip[[pos[v] for v in ib["te"]]] = p
                s = oof_r2(y[tr], ip)
                if s > best:
                    best, bl = s, lam
            out[te] = self._pred(outer, self._fit(outer, y[tr], bl))
        return out


def oof_line(y, x, folds):
    """sd ALONE, out of fold — idea 252's floor, verbatim."""
    y = np.asarray(y, float); x = np.asarray(x, float)
    F = np.empty(len(y))
    for f in np.unique(folds):
        te = folds == f; tr = ~te
        X = np.column_stack([np.ones(tr.sum()), x[tr]])
        beta, *_ = np.linalg.lstsq(X, y[tr], rcond=None)
        F[te] = beta[0] + beta[1] * x[te]
    return F


# ------------------------------------------------------------------ the draw grid
def panel_defs():
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    dropped = len(bad & set(pxs.columns))
    pxk = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]]
    say(f"    SMALL panel: {len([c for c in pxs.columns if c != 'SPY'])} names cached;"
        f" dropped {dropped} with max_1d_move >= 1.0 ->"
        f" {len([c for c in pxk.columns if c != 'SPY'])} tradable (SMALL439)")
    return {
        "B136": (px136, list(px136.columns)),                          # idea 78: SPY tradable
        "SMALL439": (pxk, [c for c in pxk.columns if c != "SPY"]),     # SPY benchmark only
        "SMALL484": (pxs, [c for c in pxs.columns if c != "SPY"]),     # idea 484's panel, gate only
    }


def draw_books(px, names, k, n_draws, seed, startb, is1_end):
    """Books for the first n_draws draws of one k cell.  Draw d is the d-th name set from the
    generator seeded once per (panel, k) — idea 484's construction, unchanged."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(n_draws):
        cols = list(rng.choice(names, size=k, replace=False))
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop: elig[drop] = False
        rank = s.where(elig).rank(axis=1, ascending=False)
        wm = rebalance_mask(p.index, FREQ).values
        ne = elig[wm].sum(axis=1).loc[startb:]
        mom_p = (p[cols].shift(21) / p[cols].shift(252) - 1).where(elig[cols])
        sdw = mom_p[wm].loc[startb:].std(axis=1)
        cnt = elig.sum(axis=1).replace(0, np.nan)
        w_ew = elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
        r0e, tue = fast_backtest(p, w_ew)
        r0e, tue = r0e.loc[startb:], tue.loc[startb:]
        rec = dict(k=k, draw=d, cols="|".join(cols),
                   n_elig=float(ne.mean()), sd=float(sdw.mean()),
                   n_elig_IS=float(ne.loc[:IS_END].mean()), sd_IS=float(sdw.loc[:IS_END].mean()),
                   n_elig_IS1=float(ne.loc[:is1_end].mean()), sd_IS1=float(sdw.loc[:is1_end].mean()))
        me = metrics(r0e - tue * 10 / 1e4)
        rec.update(ew_Sharpe=me["Sharpe"], ew_CAGR=me["CAGR"], ew_MaxDD=me["MaxDD"])
        for nb in N_BOOKS:
            w_c = (rank <= nb).astype(float) * (GROSS / nb)
            r0, tu = fast_backtest(p, w_c)
            r0, tu = r0.loc[startb:], tu.loc[startb:]
            for bps in BPS:
                r = r0 - tu * bps / 1e4
                mc = metrics(r); h1, h2 = half_sharpes(r)
                mo = metrics(r.loc[OOS_START:])
                tag = "" if bps == 10 else f"_c{bps}"
                rec.update({f"CAGR{nb}{tag}": mc["CAGR"], f"Sharpe{nb}{tag}": mc["Sharpe"],
                            f"MaxDD{nb}{tag}": mc["MaxDD"], f"H1_{nb}{tag}": h1, f"H2_{nb}{tag}": h2,
                            f"Sharpe_IS{nb}{tag}": metrics(r.loc[:IS_END])["Sharpe"],
                            f"Sharpe_IS1{nb}{tag}": metrics(r.loc[:is1_end])["Sharpe"],
                            f"Sharpe_IS2{nb}{tag}": metrics(r.loc[is1_end:IS_END].iloc[1:])["Sharpe"],
                            f"CAGR_IS2{nb}{tag}": metrics(r.loc[is1_end:IS_END].iloc[1:])["CAGR"],
                            f"MaxDD_IS2{nb}{tag}": metrics(r.loc[is1_end:IS_END].iloc[1:])["MaxDD"],
                            f"Sharpe_OOS{nb}{tag}": mo["Sharpe"], f"CAGR_OOS{nb}{tag}": mo["CAGR"],
                            f"MaxDD_OOS{nb}{tag}": mo["MaxDD"]})
        rows.append(rec)
    return rows


def keep_flags(s_full, dd_full, cagr_full, h1, h2, oos_sharpe, base, spy):
    a = (h1 > base["H1"]) and (h2 > base["H2"]) and (dd_full >= base["MaxDD"])
    b = (h1 > spy["H1"] and h2 > spy["H2"] and oos_sharpe > spy["OOS_Sharpe"]
         and dd_full >= 0.60 * spy["MaxDD"] and cagr_full >= 0.70 * spy["CAGR"])
    return a, b


def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 487 — is a draw's IS SHARPE the wrong thing to PREDICT?")
    say("Fit the same three models to a purely IS-side target and score them INSIDE the")
    say("in-sample window, before any OOS number is read.")
    say("=" * 110)

    PX = panel_defs()
    ctx = {}
    for pan in PANELS + ["SMALL484"]:
        px, names = PX[pan]
        startb = px.index[260]
        is_days = px.loc[startb:IS_END].index
        is1_end = is_days[len(is_days) // 2]
        spy = px["SPY"].pct_change().fillna(0).loc[startb:]
        sh1, sh2 = half_sharpes(spy)
        ms = metrics(spy)
        ctx[pan] = dict(px=px, names=names, startb=startb, is1_end=is1_end, spy=spy,
                        spy_s=dict(CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"],
                                   H1=sh1, H2=sh2,
                                   OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                                   OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                                   OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"]))
        if pan in PANELS:
            b2 = engine_backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[startb:]
            b1, b2h = half_sharpes(b2)
            mb = metrics(b2)
            ctx[pan]["base"] = {10: dict(CAGR=mb["CAGR"], Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"],
                                         H1=b1, H2=b2h,
                                         OOS_Sharpe=metrics(b2.loc[OOS_START:])["Sharpe"],
                                         OOS_CAGR=metrics(b2.loc[OOS_START:])["CAGR"],
                                         OOS_MaxDD=metrics(b2.loc[OOS_START:])["MaxDD"])}
            b25 = engine_backtest(px, rules_v2_weights(px), cost_bps=25, freq=FREQ)["returns"].loc[startb:]
            c1, c2 = half_sharpes(b25); mc = metrics(b25)
            ctx[pan]["base"][25] = dict(CAGR=mc["CAGR"], Sharpe=mc["Sharpe"], MaxDD=mc["MaxDD"],
                                        H1=c1, H2=c2,
                                        OOS_Sharpe=metrics(b25.loc[OOS_START:])["Sharpe"],
                                        OOS_CAGR=metrics(b25.loc[OOS_START:])["CAGR"],
                                        OOS_MaxDD=metrics(b25.loc[OOS_START:])["MaxDD"])
            say(f"\n    {pan}: {len(names)} tradable names, {startb.date()} -> {px.index[-1].date()};"
                f" IS1 {startb.date()}..{is1_end.date()}, IS2 {is1_end.date()}..{IS_END},"
                f" OOS {OOS_START}..")
            say(f"      SPY            {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}"
                f"  halves {sh1:.3f}/{sh2:.3f}  OOS Sharpe"
                f" {ctx[pan]['spy_s']['OOS_Sharpe']:.3f}")
            for bps in BPS:
                bb = ctx[pan]["base"][bps]
                say(f"      RULES v2 @{bps:>2}bps {bb['CAGR']:.2%} / {bb['Sharpe']:.3f} /"
                    f" {bb['MaxDD']:.2%}  halves {bb['H1']:.3f}/{bb['H2']:.3f}"
                    f"  OOS Sharpe {bb['OOS_Sharpe']:.3f}")

    # ------------------------------------------------------------------ GATES
    say("\n=== GATES ===")
    px136, names136 = PX["B136"]; sb136 = ctx["B136"]["startb"]
    rng = np.random.default_rng(SEED_B + 40); g1 = 0.0
    for _ in range(6):
        cols = list(rng.choice(names136, size=40, replace=False))
        keep = list(dict.fromkeys(cols + ["SPY"]))
        p = px136[keep].dropna(how="all").ffill()
        s, above, vol20 = score(p, vol_scale=False)
        elig = (above & (vol20 < MAX_VOL)).copy()
        drop = [c for c in p.columns if c not in set(cols)]
        if drop: elig[drop] = False
        w = (s.where(elig).rank(axis=1, ascending=False) <= 20).astype(float) * (GROSS / 20)
        a = engine_backtest(p, w, cost_bps=10, freq=FREQ)["returns"].loc[sb136:]
        r0, tu = fast_backtest(p, w)
        b = (r0 - tu * 10 / 1e4).loc[sb136:]
        g1 = max(g1, float(np.abs(a.values - b.values).max()))
    say(f"G1 fast_backtest vs engine.backtest over 6 drawn books: max|dret| {g1:.3e}")
    assert g1 < 1e-12, "G1 FAILED"

    for pan in PANELS:
        c = ctx[pan]
        n_is = len(c["px"].loc[c["startb"]:IS_END].index)
        n1 = len(c["px"].loc[c["startb"]:c["is1_end"]].index)
        n2 = len(c["px"].loc[c["is1_end"]:IS_END].index) - 1
        say(f"G4 {pan}: IS {n_is} days = IS1 {n1} + IS2 {n2} (sum {n1+n2}), both non-empty:"
            f" {n1 > 0 and n2 > 0 and n1 + n2 == n_is}")
        assert n1 > 0 and n2 > 0 and n1 + n2 == n_is, "G4 FAILED"

    # G5 — the fast ridge must equal idea 484's `_solve_multi` estimator, free column included
    rg = np.random.default_rng(4870)
    Mg = (rg.random((60, 12)) < 0.3).astype(float)
    xg = rg.normal(size=60); yg = rg.normal(size=60)
    fg = np.arange(60) % 5
    worst5 = 0.0
    for xx, free in ((None, 0), (xg, 1)):
        R = RidgeOOF(Mg, fg, x=xx, inner_k=3)
        for lam in LAMS:
            for te, tr, outer, _ in R.blocks:
                fast = R._pred(outer, R._fit(outer, yg[tr], lam))
                D = Mg if xx is None else np.column_stack([xg, Mg])
                Xtr = D[tr]; xm = Xtr.mean(axis=0); Xc = Xtr - xm
                A = Xc.T @ Xc; ym = yg[tr].mean()
                beta = _solve_multi(A, Xc, yg[tr].reshape(-1, 1), np.array([ym]), lam, free)
                ref = (ym + (D[te] - xm) @ beta).ravel()
                worst5 = max(worst5, float(np.abs(fast - ref).max()))
    say(f"G5 RidgeOOF vs idea 484's _solve_multi (both penalties, 6 lambdas): max|diff| {worst5:.3e}")
    assert worst5 < 1e-8, "G5 FAILED"

    # ------------------------------------------------------------------ the grid
    say("\n" + "=" * 110)
    say(f"BOOK GRID — {D_MAX} draws per k cell x 3 k x {len(PANELS)} panels ="
        f" {D_MAX*3*len(PANELS)} sub-panels; CAND-5, CAND-20, EWall; 10 and 25 bps, weekly")
    say("=" * 110)
    G = {}
    for pan in PANELS:
        c = ctx[pan]; rows = []
        for k in KS:
            rows += draw_books(c["px"], c["names"], k, D_MAX, SEED_B + k, c["startb"], c["is1_end"])
            say(f"    {pan} k={k:<3} {D_MAX} draws done ({time.time()-t0:.0f}s)")
        G[pan] = pd.DataFrame(rows)
    ALL = pd.concat([G[p].assign(panel=p) for p in PANELS], ignore_index=True)
    ALL.to_csv(OUT / f"{STAMP}.grid.csv.gz", index=False, compression="gzip")

    # G2 — the B136 grid must reproduce idea 484's committed file exactly
    say("\nG2 regenerated B136 grid vs idea 484's committed grid.csv.gz")
    if REF484.exists():
        ref = pd.read_csv(REF484)
        r = ref[ref.panel == "B136"].set_index(["k", "draw"]).sort_index()
        m = G["B136"].set_index(["k", "draw"]).sort_index()
        shared = [c for c in r.columns if c in m.columns and r[c].dtype.kind == "f"]
        worst, wcol = 0.0, None
        for cc in shared:
            d = float(np.abs(r[cc].values - m[cc].values).max())
            if d > worst:
                worst, wcol = d, cc
        say(f"    {len(r)} rows, {len(shared)} shared float columns; worst max|diff|"
            f" {worst:.3e} on `{wcol}`")
        assert worst < 1e-9, "G2 FAILED"
        smallref = ref[ref.panel == "SMALL484"]
        say(f"G3 idea 484's SMALL484 rows in the committed file: {len(smallref)};"
            f" today's cached small panel carries {len(PX['SMALL484'][1])} tradable names —"
            f" this run's SMALL439 drops the max_1d_move >= 1.0 names, so the SMALL rows are"
            f" NOT gated against idea 484 and are reported as a separate panel.")
    else:
        say("    idea 484's committed grid is missing — G2 CANNOT RUN (reported, not asserted)")

    # ------------------------------------------------------------------ the null
    say("\n" + "=" * 110)
    say("PART A — THE NULL EVERY MODEL MUST BEAT: does the TARGET autocorrelate across windows?")
    say("=" * 110)
    nrows = []
    for pan in PANELS:
        B = G[pan]
        for k in KS:
            sub = B[B.k == k]
            for nb in N_BOOKS:
                for bps in BPS:
                    tag = "" if bps == 10 else f"_c{bps}"
                    r_is = spearman(sub[f"Sharpe_IS1{nb}{tag}"], sub[f"Sharpe_IS2{nb}{tag}"])
                    q_is = oof_r2(sub[f"Sharpe_IS2{nb}{tag}"], sub[f"Sharpe_IS1{nb}{tag}"])
                    r_oos = spearman(sub[f"Sharpe_IS{nb}{tag}"], sub[f"Sharpe_OOS{nb}{tag}"])
                    q_oos = oof_r2(sub[f"Sharpe_OOS{nb}{tag}"], sub[f"Sharpe_IS{nb}{tag}"])
                    nrows.append(dict(panel=pan, k=k, n=nb, bps=bps, draws=len(sub),
                                      rho_IS1_IS2=r_is, R2_IS1_IS2=q_is,
                                      rho_IS_OOS=r_oos, R2_IS_OOS=q_oos))
    NUL = pd.DataFrame(nrows); NUL.to_csv(OUT / f"{STAMP}.null.csv", index=False)
    say(NUL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  rho(IS1, IS2)  median {NUL.rho_IS1_IS2.median():+.4f}"
        f"  range [{NUL.rho_IS1_IS2.min():+.4f}, {NUL.rho_IS1_IS2.max():+.4f}]"
        f"  positive in {int((NUL.rho_IS1_IS2 > 0).sum())}/{len(NUL)} cells")
    say(f"  rho(IS, OOS)   median {NUL.rho_IS_OOS.median():+.4f}"
        f"  range [{NUL.rho_IS_OOS.min():+.4f}, {NUL.rho_IS_OOS.max():+.4f}]"
        f"  positive in {int((NUL.rho_IS_OOS > 0).sum())}/{len(NUL)} cells")

    # ------------------------------------------------------------------ the models
    say("\n" + "=" * 110)
    say("PART B — the three models at each TARGET (out of fold, folds = draw index % 10)")
    say("=" * 110)
    mrows = []
    PRED = {}
    for pan in PANELS:
        B = G[pan]; names = PX[pan][1]
        nix = {t: i for i, t in enumerate(names)}
        for k in KS:
            sub = B[B.k == k].reset_index(drop=True)
            folds = (sub["draw"].values % N_FOLDS)
            M = np.zeros((len(sub), len(names)))
            for i, cs in enumerate(sub["cols"]):
                for t in cs.split("|"):
                    M[i, nix[t]] = 1.0
            RM = RidgeOOF(M, folds)                                   # name dummies alone
            RX = {"IS": RidgeOOF(M, folds, x=sub["sd_IS"].values),    # M + sd, sd unpenalised
                  "IS1": RidgeOOF(M, folds, x=sub["sd_IS1"].values)}
            for nb in N_BOOKS:
                for bps in BPS:
                    tag = "" if bps == 10 else f"_c{bps}"
                    yIS = sub[f"Sharpe_IS{nb}{tag}"].values
                    yIS1 = sub[f"Sharpe_IS1{nb}{tag}"].values
                    yIS2 = sub[f"Sharpe_IS2{nb}{tag}"].values
                    yOOS = sub[f"Sharpe_OOS{nb}{tag}"].values
                    for target in TARGETS:
                        is1 = target == "IS1_IS2"
                        yfit = yIS1 if is1 else yIS
                        ysco = {"FIT": yIS, "IS1_IS2": yIS2, "IS_OOS": yOOS}[target]
                        xfit = sub["sd_IS1"].values if is1 else sub["sd_IS"].values
                        preds = {
                            "sd": oof_line(yfit, xfit, folds),
                            "M": RM.predict(yfit),
                            "M+sd": RX["IS1" if is1 else "IS"].predict(yfit),
                        }
                        for mod, pr in preds.items():
                            mrows.append(dict(panel=pan, k=k, n=nb, bps=bps, target=target,
                                              model=mod, draws=len(sub),
                                              oofR2=oof_r2(ysco, pr), rho=spearman(pr, ysco),
                                              fitR2=oof_r2(yfit, pr)))
                            PRED[(pan, k, nb, bps, target, mod)] = pr
            say(f"    {pan} k={k:<3} models fitted ({time.time()-t0:.0f}s)")
    MOD = pd.DataFrame(mrows); MOD.to_csv(OUT / f"{STAMP}.models.csv", index=False)
    for target in TARGETS:
        s = MOD[MOD.target == target]
        say(f"\n  TARGET {target}")
        piv = s.pivot_table(index=["panel", "k", "n", "bps"], columns="model",
                            values="oofR2")[MODELS]
        say("  " + piv.to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n  "))
        pr = s.pivot_table(index=["panel", "k", "n", "bps"], columns="model", values="rho")[MODELS]
        say(f"   median oofR2  " + "  ".join(f"{m} {s[s.model==m].oofR2.median():+.4f}"
                                             for m in MODELS))
        say(f"   median rho    " + "  ".join(f"{m} {s[s.model==m].rho.median():+.4f}"
                                             for m in MODELS))
        say(f"   cells with oofR2 > 0: " + "  ".join(
            f"{m} {int((s[s.model==m].oofR2 > 0).sum())}/{len(s[s.model==m])}" for m in MODELS))

    # ------------------------------------------------------------------ the choice
    say("\n" + "=" * 110)
    say("PART C — THE CHOICE: six selectors, scored INSIDE in-sample (IS1 -> IS2) and by rule 8")
    say("=" * 110)
    crows, wrows = [], []
    for pan in PANELS:
        B = G[pan]
        spy = ctx[pan]["spy_s"]
        for k in KS:
            sub = B[B.k == k].reset_index(drop=True)
            for nb in N_BOOKS:
                for bps in BPS:
                    tag = "" if bps == 10 else f"_c{bps}"
                    base = ctx[pan]["base"][bps]
                    # ---- IS-only tournament: choose on IS1, read IS2
                    picks_is = {
                        "S1 IS Sharpe": int(np.argmax(sub[f"Sharpe_IS1{nb}{tag}"].values)),
                        "S2 IS sd": int(np.argmax(sub["sd_IS1"].values)),
                        "S3 pred sd": int(np.argmax(PRED[(pan, k, nb, bps, "IS1_IS2", "sd")])),
                        "S4 pred M": int(np.argmax(PRED[(pan, k, nb, bps, "IS1_IS2", "M")])),
                        "S5 pred M+sd": int(np.argmax(PRED[(pan, k, nb, bps, "IS1_IS2", "M+sd")])),
                    }
                    med_is2 = float(np.median(sub[f"Sharpe_IS2{nb}{tag}"].values))
                    for sel, i in picks_is.items():
                        v = float(sub[f"Sharpe_IS2{nb}{tag}"].iloc[i])
                        pct = float((sub[f"Sharpe_IS2{nb}{tag}"].values < v).mean())
                        crows.append(dict(panel=pan, k=k, n=nb, bps=bps, leg="IS1->IS2",
                                          selector=sel, pick=int(sub["draw"].iloc[i]),
                                          scored_Sharpe=v, median_Sharpe=med_is2,
                                          edge=v - med_is2, percentile=pct,
                                          beats_median=v > med_is2))
                    # ---- rule 8: choose on IS, read OOS once
                    picks_oos = {
                        "S1 IS Sharpe": int(np.argmax(sub[f"Sharpe_IS{nb}{tag}"].values)),
                        "S2 IS sd": int(np.argmax(sub["sd_IS"].values)),
                        "S3 pred sd": int(np.argmax(PRED[(pan, k, nb, bps, "IS_OOS", "sd")])),
                        "S4 pred M": int(np.argmax(PRED[(pan, k, nb, bps, "IS_OOS", "M")])),
                        "S5 pred M+sd": int(np.argmax(PRED[(pan, k, nb, bps, "IS_OOS", "M+sd")])),
                    }
                    med_oos = float(np.median(sub[f"Sharpe_OOS{nb}{tag}"].values))
                    for sel, i in picks_oos.items():
                        row = sub.iloc[i]
                        v = float(row[f"Sharpe_OOS{nb}{tag}"])
                        pct = float((sub[f"Sharpe_OOS{nb}{tag}"].values < v).mean())
                        crows.append(dict(panel=pan, k=k, n=nb, bps=bps, leg="IS->OOS",
                                          selector=sel, pick=int(row["draw"]),
                                          scored_Sharpe=v, median_Sharpe=med_oos,
                                          edge=v - med_oos, percentile=pct,
                                          beats_median=v > med_oos))
                        a, bkeep = keep_flags(row[f"Sharpe{nb}{tag}"], row[f"MaxDD{nb}{tag}"],
                                              row[f"CAGR{nb}{tag}"], row[f"H1_{nb}{tag}"],
                                              row[f"H2_{nb}{tag}"], v, base, spy)
                        wrows.append(dict(panel=pan, k=k, n=nb, bps=bps, selector=sel,
                                          pick=int(row["draw"]),
                                          IS_Sharpe=row[f"Sharpe_IS{nb}{tag}"],
                                          CAGR=row[f"CAGR{nb}{tag}"],
                                          Sharpe=row[f"Sharpe{nb}{tag}"],
                                          MaxDD=row[f"MaxDD{nb}{tag}"],
                                          H1=row[f"H1_{nb}{tag}"], H2=row[f"H2_{nb}{tag}"],
                                          OOS_CAGR=row[f"CAGR_OOS{nb}{tag}"], OOS_Sharpe=v,
                                          OOS_MaxDD=row[f"MaxDD_OOS{nb}{tag}"],
                                          base_OOS_CAGR=base["OOS_CAGR"],
                                          base_OOS_Sharpe=base["OOS_Sharpe"],
                                          base_OOS_MaxDD=base["OOS_MaxDD"],
                                          spy_OOS_CAGR=spy["OOS_CAGR"],
                                          spy_OOS_Sharpe=spy["OOS_Sharpe"],
                                          spy_OOS_MaxDD=spy["OOS_MaxDD"],
                                          beats_base=v > base["OOS_Sharpe"],
                                          beats_spy=v > spy["OOS_Sharpe"],
                                          keep4a=a, keep4b=bkeep))
    CH = pd.DataFrame(crows); CH.to_csv(OUT / f"{STAMP}.choice.csv", index=False)
    WF = pd.DataFrame(wrows); WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    for leg in ("IS1->IS2", "IS->OOS"):
        s = CH[CH.leg == leg]
        say(f"\n  LEG {leg}: selector vs the MEDIAN draw of its own cell"
            f" ({len(s)//5} cells x 5 selectors)")
        t = s.groupby("selector").agg(mean_edge=("edge", "mean"), median_edge=("edge", "median"),
                                      mean_pctile=("percentile", "mean"),
                                      beats_median=("beats_median", "sum"),
                                      cells=("edge", "size"))
        say("  " + t.to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n  "))

    say("\n=== RULE 8 WALK-FORWARD (all inputs on IS only; 2017-01-01.. read ONCE) ===")
    say(WF[["panel", "k", "n", "bps", "selector", "pick", "IS_Sharpe", "CAGR", "Sharpe",
            "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n  picks beating the live book's OOS Sharpe: {int(WF.beats_base.sum())}/{len(WF)};"
        f" beating SPY's: {int(WF.beats_spy.sum())}/{len(WF)}")
    say(f"  KEEP PATHS over the {len(WF)} rule-8 picks: 4a {int(WF.keep4a.sum())},"
        f" 4b {int(WF.keep4b.sum())}, BOTH {int((WF.keep4a & WF.keep4b).sum())}")
    for sel in WF.selector.unique():
        s = WF[WF.selector == sel]
        say(f"    {sel:<14} OOS Sharpe median {s.OOS_Sharpe.median():.3f}"
            f"  beats live book {int(s.beats_base.sum())}/{len(s)}"
            f"  beats SPY {int(s.beats_spy.sum())}/{len(s)}"
            f"  4a {int(s.keep4a.sum())}  4b {int(s.keep4b.sum())}")
    if int(WF.keep4b.sum()):
        say("  4b passers:")
        say(WF[WF.keep4b][["panel", "k", "n", "bps", "selector", "pick", "CAGR", "Sharpe",
                           "MaxDD", "H1", "H2", "OOS_Sharpe"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n" + "=" * 110)
    say("PART D — the verdict the queue pre-registered")
    say("=" * 110)
    for target in TARGETS:
        s = MOD[MOD.target == target]
        say(f"  {target:8s} median oofR2 " + " ".join(
            f"{m} {s[s.model==m].oofR2.median():+.4f}" for m in MODELS)
            + "   median rho " + " ".join(f"{m} {s[s.model==m].rho.median():+.4f}"
                                          for m in MODELS))
    inside = MOD[MOD.target == "IS1_IS2"]
    say(f"  Inside IS, {int((inside.oofR2 > 0).sum())}/{len(inside)} model cells reach a"
        f" positive out-of-fold R2 on the held-out IS half, and"
        f" {int((inside.rho > 0).sum())}/{len(inside)} a positive rank correlation.")
    say(f"  The raw statistic itself transfers at rho(IS1, IS2) median"
        f" {NUL.rho_IS1_IS2.median():+.4f} and rho(IS, OOS) median {NUL.rho_IS_OOS.median():+.4f}.")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\nwrote .grid.csv.gz .models.csv .null.csv .choice.csv .walkforward.csv .console.txt"
        f"  ({time.time()-t0:.0f}s)")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
