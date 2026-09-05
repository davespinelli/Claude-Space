#!/usr/bin/env python3
"""
IDEA 192 - does-a-harmful-instrument-clear-more-often-than-a-helpful-one   (lane B, 2026-09-05)

QUESTION (from the queue)
------------------------
Idea 186's matched-null clause cleared 15 DDCTL points and ALL 15 have NEGATIVE dSharpe, while the
two families whose effects are small clear almost never.  That is consistent with the clause
measuring EFFECT SIZE and being blind to SIGN, which would make it a poor filter for KEEPs
specifically.  Test it directly: across ideas 181 and 186's combined 288 real arms, regress
clause-clearing on |dSharpe| and on sign, and report whether any clearing arm has ever been a
positive one.

WHAT THIS RUN IS
----------------
A meta-analysis of the project's own two null-clause corpora, plus an INDEPENDENT reproduction of a
stratified slice of each (nothing is regressed until the slice reproduces), plus the required
rule-8 walk-forward of the thing the question implies: a SIGN-AWARE clause gate.

  corpus T (idea 181, keyed tilts):    3 panels x 5 keys x 2 dirs x 3 m x 2 cost rungs = 180 arms
  corpus O (idea 186, overlays):       3 panels x 3 families x 3 thr x 2 depths x 2 rungs = 108 arms
                                                                                    ----------
                                                                                    288 real arms

  clause (both corpora, identical form):  clears  <=>  |dSharpe(real)| > max over 20 matched null
  draws of |dSharpe(null)|.  One-sided 1/21 = 4.8%.  The matched null is a random KEY (181) or a
  circular ROTATION of the ON indicator (186).

PRE-REGISTERED PREDICTIONS (written before the numbers were read; all reported hit or miss)
  P1  |dSharpe| is strongly and significantly positive in the logit.
  P2  Controlling for |dSharpe| and the arm's own null band, the NEGATIVE-sign dummy is NOT
      significant: the clause is sign-blind by construction, so any sign tilt must come from the
      corpus, not the test.
  P3  Unconditionally, clearing arms skew negative: P(d<0 | clear) > P(d<0 | not clear).
  P4  At least ONE clearing arm has positive dSharpe (idea 181's PRICE/NEG walk-forward win says
      the corpus is not uniformly harmful at large |d|).
  P5  Among arms that PASS 4b, the clear rate is far below the corpus clear rate - the clause is a
      poor filter for KEEPs specifically.
  P6  Rule 8: the sign-aware gate S3 does NOT beat do-nothing S0 (eighth consecutive do-nothing
      win in this project).
  P7  Rule 8: S3 >= S2, i.e. adding the sign at least does not make the sign-blind gate worse.

TUNED PARAMETERS: 0 for the meta-analysis (the corpus is fixed and fully published), and the two
inherited grid dials of each parent are carried through unchanged and REPORTED IN FULL (all 288
arms are written to .arms.csv; all 24 walk-forward cells to .walkforward.csv).

OUTPUTS
  <stem>.arms.csv         288 real arms, unified schema, one row each
  <stem>.regression.csv   every logit fitted, with coefficients / SE / z
  <stem>.reproduction.csv the independent recomputation vs the published grids
  <stem>.walkforward.csv  24 rule-8 cells x 5 selectors
  <stem>.console.txt      full console
  <stem>.result.md        the write-up
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B"
OUT = ROOT / "research" / "backtests"
T_STEM = "2026-09-05_does-a-null-column-change-any-published-verdict_cloud"      # idea 181
O_STEM = "2026-09-05_the-null-column-for-instruments-that-are-not-keyed-tilts_cloud"  # idea 186

IS_END = pd.Timestamp("2016-12-31")
OOS_START = "2017-01-01"
FREQ, MAX_VOL = "W", 0.60
BASE_N, BASE_GROSS = 20, 0.75
COST_RUNGS = [10.0, 25.0]

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# =============================================================== shared machinery (my own code)
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def rankpct(df):
    return df.rank(axis=1, pct=True)


def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def net(res, bps):
    """The engine's own cost definition applied to a 0 bps run (asserted exact below)."""
    return res["returns"] - res["turnover"] * bps / 1e4


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], bad


# =============================================================== logistic regression (IRLS)
def logit(X, y, names, ridge=1e-6, iters=200):
    """Newton-Raphson IRLS.  Returns a tidy DataFrame of coef / SE / z / p (normal approx).
    Perfect-separation is handled by the ridge and flagged by a huge SE, which is reported."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, k = X.shape
    b = np.zeros(k)
    for _ in range(iters):
        eta = np.clip(X @ b, -30, 30)
        p = 1.0 / (1.0 + np.exp(-eta))
        w = np.clip(p * (1 - p), 1e-9, None)
        H = X.T @ (X * w[:, None]) + ridge * np.eye(k)
        g = X.T @ (y - p) - ridge * b
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    eta = np.clip(X @ b, -30, 30)
    p = 1.0 / (1.0 + np.exp(-eta))
    w = np.clip(p * (1 - p), 1e-9, None)
    cov = np.linalg.inv(X.T @ (X * w[:, None]) + ridge * np.eye(k))
    se = np.sqrt(np.diag(cov))
    z = b / se
    from math import erfc, sqrt
    pv = [erfc(abs(zi) / sqrt(2)) for zi in z]
    ll = float(np.sum(y * np.log(np.clip(p, 1e-12, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-12, 1))))
    return pd.DataFrame(dict(term=names, coef=b, se=se, z=z, p=pv)), ll, n


def fisher_exact_2x2(a, b, c, d):
    """Two-sided Fisher exact p for [[a,b],[c,d]] (small tables only)."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def pr(x):
        return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)

    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    p0 = pr(a)
    return float(sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 * (1 + 1e-12)))


# =============================================================== corpus assembly
def load_corpora():
    gT = pd.read_csv(OUT / f"{T_STEM}.grid.csv")
    cT = pd.read_csv(OUT / f"{T_STEM}.clause.csv")
    gO = pd.read_csv(OUT / f"{O_STEM}.grid.csv", keep_default_na=False, na_values=[""])
    cO = pd.read_csv(OUT / f"{O_STEM}.clause.csv")
    return gT, cT, gO, cO


def build_arms(gT, cT, gO, cO):
    """One row per real arm, unified schema, from BOTH corpora."""
    rows = []

    # ---- corpus T (keyed tilts, idea 181).  Null band is per (panel, dir, m, cost) cell.
    cF = cT[cT.window == "F"].set_index(["panel", "dir", "m", "cost", "key"])
    cI = cT[cT.window == "IS"].set_index(["panel", "dir", "m", "cost", "key"])
    real = gT[gT.kind == "real"]
    for r in real.itertuples():
        k = (r.panel, getattr(r, "dir"), r.m, r.cost, r.key)
        f, i = cF.loc[k], cI.loc[k]
        rows.append(dict(
            corpus="T", panel=r.panel, family=r.key, arm=f"{r.key}/{getattr(r,'dir')}/{r.m:g}",
            cost=float(r.cost),
            dSharpe=float(r.dSharpe_F), absd=abs(float(r.dSharpe_F)),
            band=float(f.null_max), clears=bool(int(f.clears)),
            IS_dSharpe=float(r.dSharpe_IS), IS_band=float(i.null_max),
            IS_clears=bool(int(i.clears)),
            Sharpe=float(r.Sharpe_F), MaxDD=float(r.MaxDD_F),
            OOS_CAGR=float(r.CAGR_OOS), OOS_Sharpe=float(r.Sharpe_OOS), OOS_MaxDD=float(r.MaxDD_OOS),
            oosH1=float(r.oosH1), oosH2=float(r.oosH2),
            H1=float(r.Sharpe_H1), H2=float(r.Sharpe_H2), CAGR=float(r.CAGR_F),
        ))

    # ---- corpus O (overlays, idea 186).  Null band is per arm (20 circular rotations).
    realO = gO[gO.draw == -1]
    nullO = gO[gO.draw >= 0]
    keyc = ["panel", "family", "thr", "depth", "bps"]
    isband = nullO.groupby(keyc)["IS_dSharpe"].apply(lambda s: float(s.abs().max()))
    cOx = cO.set_index(keyc)
    for r in realO.itertuples():
        k = (r.panel, r.family, r.thr, r.depth, r.bps)
        cc = cOx.loc[k]
        isb = float(isband.loc[k])
        rows.append(dict(
            corpus="O", panel=r.panel, family=r.family,
            arm=f"{r.family}/{r.thr:g}/{r.depth}", cost=float(r.bps),
            dSharpe=float(r.dSharpe), absd=abs(float(r.dSharpe)),
            band=float(cc.null_max_abs), clears=bool(cc.clears),
            IS_dSharpe=float(r.IS_dSharpe), IS_band=isb,
            IS_clears=bool(abs(float(r.IS_dSharpe)) > isb),
            Sharpe=float(r.Sharpe), MaxDD=float(r.MaxDD),
            OOS_CAGR=float(r.OOS_CAGR), OOS_Sharpe=float(r.OOS_Sharpe), OOS_MaxDD=float(r.OOS_MaxDD),
            oosH1=np.nan, oosH2=np.nan,
            H1=float(r.H1), H2=float(r.H2), CAGR=float(r.CAGR),
        ))
    A = pd.DataFrame(rows)
    # published KEEP labels, carried through verbatim from each parent
    A["pass4a"] = np.nan
    A["pass4b"] = np.nan
    ra = realO.set_index(keyc)
    for ix, r in A[A.corpus == "O"].iterrows():
        fam, thr, dep = r["arm"].split("/")
        k = (r["panel"], fam, float(thr), dep, int(r["cost"]))
        A.loc[ix, "pass4a"] = float(str(ra.loc[k, "fail4a"]) == "-")
        A.loc[ix, "pass4b"] = float(str(ra.loc[k, "fail4b"]) == "-")
    return A


def tilt_keeps(gT):
    """Recompute 4a/4b for corpus T with idea 181's own bars (the parent published counts, not a
    per-row flag), so both corpora carry the same two KEEP columns."""
    out = {}
    for pn, sub in gT.groupby("panel"):
        spy = None  # SPY row is not in the grid; recomputed by the caller
        out[pn] = sub
        _ = spy
    return out


# =============================================================== reproduction: corpus T slice
def reproduce_T(px, panel_name, seed_panel, B_NULL=20, MS=(0.20, 0.50, 1.00)):
    """Independently rebuild idea 181's u56 slice: 5 real keys + 20 matched null keys, 2 dirs,
    3 tilt strengths, both cost rungs, and the clause on top."""
    rng = np.random.default_rng(seed_panel)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    keys = {
        "VOL": rankpct(vol20),
        "MOM": rankpct(px.shift(21) / px.shift(252) - 1),
        "R6": rankpct(px / px.shift(126) - 1),
        "R3": rankpct(px / px.shift(63) - 1),
        "PRICE": rankpct(px),
    }
    sd = float(np.nanmedian(px.pct_change().std().values))
    for j in range(B_NULL):
        steps = rng.normal(0.0, sd, size=px.shape)
        walk = pd.DataFrame(np.cumsum(steps, axis=0), index=px.index, columns=px.columns) + 10.0
        keys[f"NULL{j:02d}"] = rankpct(walk / walk.shift(126) - 1)
    comp = comp_score(px)
    above = px > px.rolling(200).mean()
    elig = above & (vol20 < MAX_VOL)
    start = px.index[260]

    def run(score):
        rk = score.where(elig).rank(axis=1, ascending=False)
        w = (rk <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
        res = backtest(px, w, cost_bps=0.0, freq=FREQ)
        return res["returns"].loc[start:], res["turnover"].loc[start:]

    c0, ct = run(comp)
    ctrl = {c: c0 - ct * c / 1e4 for c in COST_RUNGS}
    rows = []
    for kn, kv in keys.items():
        for dn, dv in (("POS", 1.0), ("NEG", -1.0)):
            for m in MS:
                r0, trn = run(comp + dv * m * kv)
                for c in COST_RUNGS:
                    r = r0 - trn * c / 1e4
                    rows.append(dict(panel=panel_name, key=kn, dir=dn, m=m, cost=c,
                                     kind="real" if not kn.startswith("NULL") else "nullkey",
                                     dSharpe_F=sh(r) - sh(ctrl[c]),
                                     dSharpe_IS=sh(win(r, hi=IS_END)) - sh(win(ctrl[c], hi=IS_END))))
    R = pd.DataFrame(rows)
    out = []
    for (dn, m, c), sub in R.groupby(["dir", "m", "cost"], sort=False):
        nb = sub[sub.kind == "nullkey"]
        for tag in ("F", "IS"):
            thr = float(nb[f"dSharpe_{tag}"].abs().max())
            for r in sub[sub.kind == "real"].itertuples():
                out.append(dict(panel=panel_name, dir=dn, m=m, cost=c, window=tag, key=r.key,
                                d=getattr(r, f"dSharpe_{tag}"), null_max=thr,
                                clears=int(abs(getattr(r, f"dSharpe_{tag}")) > thr)))
    return R, pd.DataFrame(out)


# =============================================================== reproduction: corpus O slice
def ddctl_arm(px, W, mask, reb, thr, depth, roll=0):
    """Idea 186's DDCTL overlay, re-implemented: scale the book by (1-depth) on rebalance dates on
    which the untreated book's own 1y trailing drawdown is worse than -thr.  roll>0 gives the
    matched null (a circular rotation of the ON indicator over the rebalance dates)."""
    r0 = backtest(px, W, cost_bps=0.0, freq=FREQ)["returns"]
    eq = (1 + r0).cumprod()
    dd = eq / eq.rolling(252, min_periods=20).max() - 1
    s_reb = (dd <= -thr).values[reb]
    if roll:
        s_reb = np.roll(s_reb, roll)
    on = pd.Series(False, index=px.index)
    on.iloc[reb] = s_reb
    on = on.where(pd.Series(mask, index=px.index)).ffill().fillna(False).astype(bool)
    return W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0), s_reb


def base_book(px, tradable):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in set(tradable)]
    if drop:
        elig[drop] = False
    rank = comp_score(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)


def rotations(J, n, seed):
    rng = np.random.default_rng(seed)
    return sorted(rng.permutation(np.arange(1, J))[:n].tolist())


def reproduce_O(px, tradable, panel_name, N_NULL=20, SEED=186_400):
    W = base_book(px, tradable)
    mask = rebalance_mask(px.index, FREQ).values
    reb = np.flatnonzero(mask)
    start = px.index[260]
    b0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
    offs = rotations(len(reb), N_NULL, SEED)
    rows = []
    for thr in (0.06, 0.10, 0.15):
        for dep in (0.50, 1.00):
            for draw in range(-1, N_NULL):
                Wt, _ = ddctl_arm(px, W, mask, reb, thr, dep, roll=0 if draw < 0 else offs[draw])
                res = backtest(px, Wt, cost_bps=0.0, freq=FREQ)
                for bps in (10, 25):
                    r = net(res, bps).loc[start:]
                    b = net(b0, bps).loc[start:]
                    rows.append(dict(panel=panel_name, family="DDCTL", thr=thr, depth=str(dep),
                                     bps=bps, draw=draw,
                                     dSharpe=sh(r) - sh(b),
                                     IS_dSharpe=sh(win(r, hi=IS_END)) - sh(win(b, hi=IS_END))))
    return pd.DataFrame(rows)


# =============================================================== rule 8 walk-forward
def selector_table(A, refs):
    """24 cells (6 tilt + 18 overlay).  Everything the selector reads is <= 2016-12-31; the
    2017-2026 window is read exactly once, at the end, for the arm each selector names.

      S0  do-nothing            - the cell's own control book (untreated)
      S1  IS-argmax dSharpe     - the naive fit
      S2  clause-gated          - restrict to arms clearing their IS null band, then IS-argmax
      S3  clause + POSITIVE     - S2's set intersected with IS_dSharpe > 0     <-- idea 192's gate
      S4  sign only             - IS_dSharpe > 0, then IS-argmax (drop the clause, keep the sign)

    S2/S3/S4 abstain to S0 when their admissible set is empty."""
    rows = []
    cells = ([("T", p, c, None) for p in sorted(A[A.corpus == "T"].panel.unique()) for c in COST_RUNGS]
             + [("O", p, c, f) for p in sorted(A[A.corpus == "O"].panel.unique())
                for f in ["DDCTL", "BUDGET", "SLEEVE"] for c in COST_RUNGS])
    for corpus, panel, cost, fam in cells:
        sub = A[(A.corpus == corpus) & (A.panel == panel) & (A.cost == cost)]
        if fam is not None:
            sub = sub[sub.family == fam]
        if sub.empty:
            continue
        ref = refs[(corpus, panel, cost)]
        picks = {"S0 do-nothing": None}
        picks["S1 IS-argmax"] = sub.loc[sub.IS_dSharpe.idxmax()]
        for tag, cand in (("S2 clause-gated", sub[sub.IS_clears]),
                          ("S3 clause+positive", sub[sub.IS_clears & (sub.IS_dSharpe > 0)]),
                          ("S4 sign-only", sub[sub.IS_dSharpe > 0])):
            picks[tag] = None if cand.empty else cand.loc[cand.IS_dSharpe.idxmax()]
        for tag, pk in picks.items():
            if pk is None:
                nm, oc, os_, od = "CONTROL(abstain)" if tag != "S0 do-nothing" else "CONTROL", \
                    ref["ctrl_OOS_CAGR"], ref["ctrl_OOS_Sharpe"], ref["ctrl_OOS_MaxDD"]
                dS = 0.0
            else:
                nm, oc, os_, od = pk["arm"], pk["OOS_CAGR"], pk["OOS_Sharpe"], pk["OOS_MaxDD"]
                dS = float(pk["IS_dSharpe"])
            rows.append(dict(corpus=corpus, panel=panel, family=fam or "-", cost=cost,
                             selector=tag, pick=nm, IS_dSharpe_of_pick=dS,
                             OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                             ctrl_OOS_Sharpe=ref["ctrl_OOS_Sharpe"],
                             base_OOS_CAGR=ref["v1_OOS_CAGR"], base_OOS_Sharpe=ref["v1_OOS_Sharpe"],
                             base_OOS_MaxDD=ref["v1_OOS_MaxDD"],
                             spy_OOS_CAGR=ref["spy_OOS_CAGR"], spy_OOS_Sharpe=ref["spy_OOS_Sharpe"],
                             spy_OOS_MaxDD=ref["spy_OOS_MaxDD"],
                             n_admissible=int(sub.IS_clears.sum()),
                             n_admissible_pos=int((sub.IS_clears & (sub.IS_dSharpe > 0)).sum()),
                             n_cand=len(sub)))
    return pd.DataFrame(rows)


def tstat(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# =============================================================== main
def main():
    t0 = time.time()
    P(f"IDEA 192 - does-a-harmful-instrument-clear-more-often-than-a-helpful-one   (lane B, {pd.Timestamp.today().date()})")
    P("=" * 122)
    P("Idea 186: the clause cleared 15 DDCTL points and ALL 15 have NEGATIVE dSharpe.  If the clause")
    P("measures EFFECT SIZE and is blind to SIGN, it is a poor filter for KEEPs specifically.  This run")
    P("pools ideas 181 (180 keyed-tilt arms) and 186 (108 overlay arms) = 288 real arms, reproduces a")
    P("stratified slice of each from scratch, regresses clearing on |dSharpe| and on sign, and walks")
    P("forward a SIGN-AWARE clause gate (rule 8).")
    P("")

    gT, cT, gO, cO = load_corpora()
    A = build_arms(gT, cT, gO, cO)
    P(f"pooled corpus: {len(A)} real arms  (T {int((A.corpus=='T').sum())} tilts + "
      f"O {int((A.corpus=='O').sum())} overlays)   clears(full sample) {int(A.clears.sum())}")
    assert len(A) == 288, len(A)

    # ------------------------------------------------------------------ panels + benchmarks
    P("")
    P("PANELS AND BENCHMARKS")
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs, bad = small_panel()
    ref_prices = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    SLEEVE = ["TLT", "GLD", "UUP"]

    def add_sleeve(px):
        a = ref_prices[SLEEVE].reindex(px.index, method="ffill")
        return pd.concat([px.drop(columns=SLEEVE, errors="ignore"), a], axis=1).ffill()

    s_stk = [c for c in pxs.columns if c != "SPY"]
    pxsO = add_sleeve(pxs[s_stk + ["SPY"]])
    px136O = add_sleeve(px136)
    PANELS = {
        # corpus, panel name -> (prices, tradable set, control-book builder)
        ("T", "u56"): (px56, [c for c in px56.columns if c != "SPY"]),
        ("T", "broad"): (px136, [c for c in px136.columns if c != "SPY"]),
        ("T", "small"): (pxs, [c for c in pxs.columns if c != "SPY"]),
        ("O", "U56"): (px56, [c for c in px56.columns if c != "SPY"]),
        ("O", "BROAD136"): (px136O, [c for c in px136O.columns if c != "SPY" and c not in SLEEVE]),
        ("O", "SMALL439"): (pxsO, s_stk),
    }
    refs = {}
    for (corpus, pn), (px, trad) in PANELS.items():
        start = px.index[260]
        W = base_book(px, trad) if corpus == "O" else None
        if corpus == "T":
            vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
            elig = (px > px.rolling(200).mean()) & (vol20 < MAX_VOL)
            rk = comp_score(px).where(elig).rank(axis=1, ascending=False)
            W = (rk <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
        c0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
        v1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        mspy, mspyo = metrics(spy), metrics(spy.loc[OOS_START:])
        for c in COST_RUNGS:
            ctrl = net(c0, c).loc[start:]
            b1 = net(v1, c).loc[start:]
            mc, mv = metrics(ctrl.loc[OOS_START:]), metrics(b1.loc[OOS_START:])
            refs[(corpus, pn, c)] = dict(
                ctrl_OOS_CAGR=mc["CAGR"], ctrl_OOS_Sharpe=mc["Sharpe"], ctrl_OOS_MaxDD=mc["MaxDD"],
                v1_OOS_CAGR=mv["CAGR"], v1_OOS_Sharpe=mv["Sharpe"], v1_OOS_MaxDD=mv["MaxDD"],
                spy_OOS_CAGR=mspyo["CAGR"], spy_OOS_Sharpe=mspyo["Sharpe"], spy_OOS_MaxDD=mspyo["MaxDD"],
                spy_F=mspy)
        P(f"  {corpus}/{pn:9s} {px.shape[1]:4d} cols  {start.date()}..{px.index[-1].date()}   "
          f"SPY OOS {mspyo['CAGR']:6.2%}/{mspyo['Sharpe']:.4f}/{mspyo['MaxDD']:7.2%}   "
          f"CONTROL@10 OOS {refs[(corpus,pn,10.0)]['ctrl_OOS_Sharpe']:.4f}   "
          f"RULES v1@10 OOS {refs[(corpus,pn,10.0)]['v1_OOS_Sharpe']:.4f}")

    # ------------------------------------------------------------------ REPRODUCTION
    P("")
    P("REPRODUCTION CONTROLS (nothing below is read until these pass)")
    rep = []

    # (a) engine cost identity: a 25 bps run == a 0 bps run minus turnover*25/1e4
    W56 = rules_v1_weights(px56)
    r0 = backtest(px56, W56, cost_bps=0.0, freq=FREQ)
    r25 = backtest(px56, W56, cost_bps=25.0, freq=FREQ)
    e = float(np.abs(net(r0, 25.0) - r25["returns"]).max())
    rep.append(dict(check="a cost identity 0bps->25bps", value=e, tol=1e-12, ok=e < 1e-12))
    P(f"  [a] cost identity                              max|diff| {e:.3e}   {'OK' if e<1e-12 else 'FAIL'}")

    # (b) RULES v1 on u56 reproduces the project's published 0.6642 @10bps
    v1_10 = net(r0, 10.0).loc[px56.index[260]:]
    s_v1 = sh(v1_10)
    rep.append(dict(check="b RULES v1 u56 @10bps Sharpe", value=s_v1, tol=0.6642, ok=abs(s_v1 - 0.6642) < 5e-4))
    P(f"  [b] RULES v1 u56 @10bps Sharpe                 {s_v1:.4f} vs published 0.6642   "
      f"{'OK' if abs(s_v1-0.6642)<5e-4 else 'FAIL'}")

    # (c) corpus T: independently rebuild idea 181's u56 slice (25 keys x 2 dirs x 3 m x 2 rungs)
    P("  [c] corpus T  u56 slice rebuilt from scratch (5 real + 20 null keys) ...")
    cT_path, cC_path = OUT / f"{STEM}.repro_T.csv", OUT / f"{STEM}.repro_Tclause.csv"
    if cT_path.exists() and cC_path.exists():
        RT, CT = pd.read_csv(cT_path), pd.read_csv(cC_path)
    else:
        RT, CT = reproduce_T(px56, "u56", seed_panel=181 + 1000 * 1)
        RT.to_csv(cT_path, index=False); CT.to_csv(cC_path, index=False)
    pubF = cT[(cT.panel == "u56") & (cT.window == "F")].set_index(["dir", "m", "cost", "key"])
    mineF = CT[CT.window == "F"].set_index(["dir", "m", "cost", "key"])
    j = mineF.join(pubF, rsuffix="_pub", how="inner")
    dmax = float((j["d"] - j["d_pub"]).abs().max())
    cmis = int((j["clears"] != j["clears_pub"]).sum())
    ok_c = dmax < 1e-10 and cmis == 0 and len(j) == 60
    rep.append(dict(check=f"c corpus-T u56 {len(j)} arms max|d - d_pub|", value=dmax, tol=1e-10, ok=ok_c))
    P(f"      {len(j)} arms   max|dSharpe - published| {dmax:.3e}   clause mismatches {cmis}   "
      f"{'OK' if ok_c else 'FAIL'}")

    # (d) corpus O: independently rebuild idea 186's U56 DDCTL family (6 arms x 21 draws)
    P("  [d] corpus O  U56 DDCTL family rebuilt from scratch (6 arms x 21 draws) ...")
    cO_path = OUT / f"{STEM}.repro_O.csv"
    if cO_path.exists():
        RO = pd.read_csv(cO_path)
        RO["depth"] = RO["depth"].astype(str)
    else:
        RO = reproduce_O(px56, [c for c in px56.columns if c != "SPY"], "U56")
        RO.to_csv(cO_path, index=False)
    pubO = gO[(gO.panel == "U56") & (gO.family == "DDCTL")].set_index(["thr", "depth", "bps", "draw"])
    minO = RO.set_index(["thr", "depth", "bps", "draw"])
    jo = minO.join(pubO, rsuffix="_pub", how="inner")
    domax = float((jo["dSharpe"] - jo["dSharpe_pub"]).abs().max())
    # and the clause on the reproduced numbers
    myclear = {}
    for (thr, dep, bps), s in RO.groupby(["thr", "depth", "bps"]):
        band = float(s[s.draw >= 0]["dSharpe"].abs().max())
        d = float(s[s.draw == -1]["dSharpe"].iloc[0])
        myclear[(thr, dep, bps)] = abs(d) > band
    pubclear = cO[(cO.panel == "U56") & (cO.family == "DDCTL")].set_index(["thr", "depth", "bps"])["clears"].to_dict()
    cmis2 = sum(1 for k, v in myclear.items() if bool(pubclear[k]) != bool(v))
    ok_d = domax < 1e-10 and cmis2 == 0 and len(jo) == 252
    rep.append(dict(check=f"d corpus-O U56 DDCTL {len(jo)} rows max|d - d_pub|", value=domax, tol=1e-10, ok=ok_d))
    P(f"      {len(jo)} rows  max|dSharpe - published| {domax:.3e}   clause mismatches {cmis2}/6   "
      f"{'OK' if ok_d else 'FAIL'}")

    REP = pd.DataFrame(rep)
    REP.to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    if not REP.ok.all():
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P(f"  reproduction {int(REP.ok.sum())}/{len(REP)}  ({time.time()-t0:.0f}s)")

    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    P(f"  288 arms -> {STEM}.arms.csv")

    # ================================================================== Q1  sign vs magnitude
    P("")
    P("=" * 122)
    P("Q1  IS THE CLAUSE BLIND TO SIGN?   (clears  <=>  |dSharpe| > the arm's own 20-draw null band)")
    P("=" * 122)
    neg, pos = A[A.dSharpe < 0], A[A.dSharpe > 0]
    P(f"  corpus split by sign of dSharpe:  NEGATIVE {len(neg)} arms, POSITIVE {len(pos)} arms")
    P(f"  clear rate   NEGATIVE {int(neg.clears.sum()):3d}/{len(neg):3d} = {neg.clears.mean():6.1%}"
      f"     POSITIVE {int(pos.clears.sum()):3d}/{len(pos):3d} = {pos.clears.mean():6.1%}")
    fp = fisher_exact_2x2(int(neg.clears.sum()), len(neg) - int(neg.clears.sum()),
                          int(pos.clears.sum()), len(pos) - int(pos.clears.sum()))
    P(f"  Fisher exact (2x2, two-sided) p = {fp:.3g}")
    P(f"  mean |dSharpe|   NEGATIVE {neg.absd.mean():.4f}   POSITIVE {pos.absd.mean():.4f}"
      f"    (the corpus's own asymmetry, before any test is applied)")
    P("")
    P("  by corpus and family:")
    P(f"  {'corpus/family':22s} {'n':>4s} {'clear':>6s} {'rate':>7s} | "
      f"{'n-':>4s} {'clr-':>5s} {'rate-':>7s} | {'n+':>4s} {'clr+':>5s} {'rate+':>7s} | "
      f"{'mean d':>8s} {'mean|d|':>8s}")
    for (co, fa), s in A.groupby(["corpus", "family"], sort=False):
        n_, p_ = s[s.dSharpe < 0], s[s.dSharpe > 0]
        P(f"  {co+'/'+fa:22s} {len(s):4d} {int(s.clears.sum()):6d} {s.clears.mean():7.1%} | "
          f"{len(n_):4d} {int(n_.clears.sum()):5d} {(n_.clears.mean() if len(n_) else np.nan):7.1%} | "
          f"{len(p_):4d} {int(p_.clears.sum()):5d} {(p_.clears.mean() if len(p_) else np.nan):7.1%} | "
          f"{s.dSharpe.mean():8.4f} {s.absd.mean():8.4f}")

    # ---- the regressions the queue asked for
    P("")
    P("  LOGIT  clears ~ ...     (IRLS, ridge 1e-6; z from the inverse observed information)")
    A["neg"] = (A.dSharpe < 0).astype(float)
    A["one"] = 1.0
    A["logband"] = np.log(A.band.clip(lower=1e-6))
    A["isO"] = (A.corpus == "O").astype(float)
    regs = []
    specs = [
        ("M1  |d| only", ["one", "absd"]),
        ("M2  sign only", ["one", "neg"]),
        ("M3  |d| + sign", ["one", "absd", "neg"]),
        ("M4  |d| + sign + log(band)", ["one", "absd", "neg", "logband"]),
        ("M5  |d| + sign + log(band) + corpus", ["one", "absd", "neg", "logband", "isO"]),
    ]
    for nm, cols in specs:
        tab, ll, n = logit(A[cols].values, A.clears.values.astype(float), cols)
        P(f"   {nm:38s} n={n}  logL={ll:9.3f}")
        for r in tab.itertuples():
            star = "***" if r.p < 0.001 else "**" if r.p < 0.01 else "*" if r.p < 0.05 else ""
            P(f"      {r.term:10s} coef {r.coef:+10.4f}  se {r.se:9.4f}  z {r.z:+7.2f}  p {r.p:9.3g} {star}")
            regs.append(dict(model=nm, **{k: getattr(r, k) for k in ("term", "coef", "se", "z", "p")}))
    pd.DataFrame(regs).to_csv(OUT / f"{STEM}.regression.csv", index=False)

    # ---- matched-|d| test: the direct, model-free version of P2
    P("")
    P("  MATCHED-|d| TEST (model-free): within terciles of |dSharpe|, does the clear rate differ by sign?")
    A["dterc"] = pd.qcut(A.absd, 3, labels=["low|d|", "mid|d|", "high|d|"])
    for tc, s in A.groupby("dterc", observed=True):
        n_, p_ = s[s.dSharpe < 0], s[s.dSharpe > 0]
        rn = n_.clears.mean() if len(n_) else np.nan
        rp = p_.clears.mean() if len(p_) else np.nan
        pv = (fisher_exact_2x2(int(n_.clears.sum()), len(n_) - int(n_.clears.sum()),
                               int(p_.clears.sum()), len(p_) - int(p_.clears.sum()))
              if len(n_) and len(p_) else np.nan)
        P(f"    {str(tc):8s} |d| in [{s.absd.min():.4f},{s.absd.max():.4f}]  "
          f"NEG {int(n_.clears.sum()):3d}/{len(n_):3d} = {rn:6.1%}   "
          f"POS {int(p_.clears.sum()):3d}/{len(p_):3d} = {rp:6.1%}   Fisher p {pv:.3g}")

    # ================================================================== Q2  any positive clearer?
    P("")
    P("=" * 122)
    P("Q2  HAS A CLEARING ARM EVER BEEN A POSITIVE ONE?")
    P("=" * 122)
    cl = A[A.clears]
    clp = cl[cl.dSharpe > 0]
    P(f"  {len(cl)} of 288 arms clear.  Of those, {len(clp)} have POSITIVE dSharpe and "
      f"{len(cl)-len(clp)} NEGATIVE.")
    if len(clp):
        P("  every positive clearing arm, in full:")
        P(f"  {'corpus':6s} {'panel':9s} {'arm':22s} {'cost':>5s} {'dSharpe':>9s} {'band':>8s} "
          f"{'Sharpe':>7s} {'MaxDD':>8s} {'OOS Sh':>7s} {'4a':>3s} {'4b':>3s}")
        for r in clp.sort_values("dSharpe", ascending=False).itertuples():
            P(f"  {r.corpus:6s} {r.panel:9s} {r.arm:22s} {r.cost:5.0f} {r.dSharpe:+9.4f} "
              f"{r.band:8.4f} {r.Sharpe:7.4f} {r.MaxDD:8.2%} {r.OOS_Sharpe:7.4f} "
              f"{('-' if np.isnan(r.pass4a) else ('Y' if r.pass4a else 'n')):>3s} "
              f"{('-' if np.isnan(r.pass4b) else ('Y' if r.pass4b else 'n')):>3s}")
    P("")
    P("  the negative clearing arms, by family:")
    for (co, fa), s in cl[cl.dSharpe < 0].groupby(["corpus", "family"], sort=False):
        P(f"    {co}/{fa:8s} {len(s):3d} arms   dSharpe {s.dSharpe.min():+.4f} .. {s.dSharpe.max():+.4f}")

    # ================================================================== Q3  a filter for KEEPs?
    P("")
    P("=" * 122)
    P("Q3  IS THE CLAUSE A POOR FILTER FOR KEEPs SPECIFICALLY?")
    P("=" * 122)
    P("  corpus O carries each parent's own 4a/4b flags; corpus T's 180 tilt arms are recomputed")
    P("  against their panel's SPY / RULES v1 with idea 181's bars, so both are on one footing.")
    # recompute 4a/4b for corpus T from its grid + panel benchmarks
    for pn in A[A.corpus == "T"].panel.unique():
        px, _ = PANELS[("T", pn)]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        h = len(spy) // 2
        sp = dict(H1=sh(spy.iloc[:h]), H2=sh(spy.iloc[h:]), OOS=sh(spy.loc[OOS_START:]),
                  MaxDD=metrics(spy)["MaxDD"], CAGR=metrics(spy)["CAGR"])
        v1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        for c in COST_RUNGS:
            b = net(v1, c).loc[start:]
            hb = len(b) // 2
            bb = dict(H1=sh(b.iloc[:hb]), H2=sh(b.iloc[hb:]), MaxDD=metrics(b)["MaxDD"])
            m = (A.corpus == "T") & (A.panel == pn) & (A.cost == c)
            A.loc[m, "pass4a"] = ((A.loc[m, "H1"] > bb["H1"]) & (A.loc[m, "H2"] > bb["H2"])
                                  & (A.loc[m, "MaxDD"] >= bb["MaxDD"])).astype(float)
            A.loc[m, "pass4b"] = ((A.loc[m, "H1"] > sp["H1"]) & (A.loc[m, "H2"] > sp["H2"])
                                  & (A.loc[m, "OOS_Sharpe"] > sp["OOS"])
                                  & (A.loc[m, "MaxDD"] >= 0.60 * sp["MaxDD"])
                                  & (A.loc[m, "CAGR"] >= 0.70 * sp["CAGR"])).astype(float)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    for path in ("pass4a", "pass4b"):
        k = A[A[path] == 1]
        nk = A[A[path] == 0]
        P(f"  {path.upper()}: {len(k)}/288 arms pass.  clear rate among PASSES "
          f"{int(k.clears.sum())}/{len(k)} = {(k.clears.mean() if len(k) else np.nan):.1%}   "
          f"among FAILS {int(nk.clears.sum())}/{len(nk)} = {nk.clears.mean():.1%}")
        if len(k):
            P(f"     of the {len(k)} passes, {int((k.dSharpe>0).sum())} have positive dSharpe; "
              f"{int((k.clears & (k.dSharpe>0)).sum())} both clear AND are positive")
    P("")
    P("  the 2x2 that matters for a KEEP gate (clause as a gate on 4b):")
    a_ = int(((A.pass4b == 1) & A.clears).sum()); b_ = int(((A.pass4b == 1) & ~A.clears).sum())
    c_ = int(((A.pass4b == 0) & A.clears).sum()); d_ = int(((A.pass4b == 0) & ~A.clears).sum())
    P(f"                 clears   inside band")
    P(f"     4b pass    {a_:6d}   {b_:11d}")
    P(f"     4b fail    {c_:6d}   {d_:11d}")
    P(f"     Fisher exact p = {fisher_exact_2x2(a_, b_, c_, d_):.3g}   "
      f"gate would retain {a_}/{a_+b_} of the 4b passes and {c_}/{c_+d_} of the failures")

    # ================================================================== rule 8
    P("")
    P("=" * 122)
    P("RULE 8  WALK-FORWARD - every selector reads only <= 2016-12-31; 2017-2026 is read once")
    P("=" * 122)
    WF = selector_table(A, refs)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  {WF.cell_id.nunique() if 'cell_id' in WF else len(WF)//5} cells x 5 selectors = {len(WF)} rows"
      f" -> {STEM}.walkforward.csv")
    P("")
    P(f"  {'selector':20s} {'meanOOS Sh':>11s} {'vs S0':>9s} {'t':>7s} {'W/L':>7s} "
      f"{'meanOOS CAGR':>13s} {'meanOOS MaxDD':>14s} {'abstains':>9s}")
    s0 = WF[WF.selector == "S0 do-nothing"].set_index(["corpus", "panel", "family", "cost"])
    summary = []
    for tag in ["S0 do-nothing", "S1 IS-argmax", "S2 clause-gated", "S3 clause+positive", "S4 sign-only"]:
        s = WF[WF.selector == tag].set_index(["corpus", "panel", "family", "cost"])
        d = (s.OOS_Sharpe - s0.OOS_Sharpe).reindex(s0.index)
        w, l = int((d > 1e-12).sum()), int((d < -1e-12).sum())
        ab = int(s.pick.astype(str).str.contains("abstain").sum())
        P(f"  {tag:20s} {s.OOS_Sharpe.mean():11.4f} {d.mean():+9.4f} {tstat(d.values):7.2f} "
          f"{str(w)+'/'+str(l):>7s} {s.OOS_CAGR.mean():13.2%} {s.OOS_MaxDD.mean():14.2%} {ab:9d}")
        summary.append(dict(selector=tag, mean_OOS_Sharpe=s.OOS_Sharpe.mean(), d_vs_S0=d.mean(),
                            t=tstat(d.values), wins=w, losses=l, abstains=ab,
                            mean_OOS_CAGR=s.OOS_CAGR.mean(), mean_OOS_MaxDD=s.OOS_MaxDD.mean()))
    P("")
    P("  benchmarks over the same 24 cells (each cell's own panel):")
    P(f"  {'RULES v1 baseline':20s} {s0.base_OOS_Sharpe.mean():11.4f} {'':9s} {'':7s} {'':7s} "
      f"{s0.base_OOS_CAGR.mean():13.2%} {s0.base_OOS_MaxDD.mean():14.2%}")
    P(f"  {'SPY buy-and-hold':20s} {s0.spy_OOS_Sharpe.mean():11.4f} {'':9s} {'':7s} {'':7s} "
      f"{s0.spy_OOS_CAGR.mean():13.2%} {s0.spy_OOS_MaxDD.mean():14.2%}")
    P("")
    P("  per-cell detail (ALL 24 cells, all 5 selectors):")
    P(f"  {'cell':34s} {'nadm':>4s} {'nadm+':>5s} | " +
      " | ".join(f"{t.split()[0]:>22s}" for t in
                 ["S0", "S1", "S2", "S3", "S4"]))
    for k, s in WF.groupby(["corpus", "panel", "family", "cost"], sort=False):
        d = s.set_index("selector")
        cell = f"{k[0]}/{k[1]}/{k[2]}@{k[3]:.0f}bps"
        cells = []
        for tag in ["S0 do-nothing", "S1 IS-argmax", "S2 clause-gated", "S3 clause+positive", "S4 sign-only"]:
            r = d.loc[tag]
            cells.append(f"{str(r['pick'])[:14]:14s}{r['OOS_Sharpe']:8.4f}")
        P(f"  {cell:34s} {int(s.n_admissible.iloc[0]):4d} {int(s.n_admissible_pos.iloc[0]):5d} | "
          + " | ".join(cells))

    # ------------- 4a/4b on the walk-forward picks
    P("")
    P("  both KEEP paths on every walk-forward pick (OOS window, vs that panel's SPY / RULES v1):")
    P(f"  {'selector':20s} {'4a-style wins vs RULES v1':>26s} {'4b-style wins vs SPY':>22s}")
    for tag in ["S0 do-nothing", "S1 IS-argmax", "S2 clause-gated", "S3 clause+positive", "S4 sign-only"]:
        s = WF[WF.selector == tag]
        p4a = int(((s.OOS_Sharpe > s.base_OOS_Sharpe) & (s.OOS_MaxDD >= s.base_OOS_MaxDD)).sum())
        p4b = int(((s.OOS_Sharpe > s.spy_OOS_Sharpe) & (s.OOS_MaxDD >= 0.60 * s.spy_OOS_MaxDD)
                   & (s.OOS_CAGR >= 0.70 * s.spy_OOS_CAGR)).sum())
        P(f"  {tag:20s} {str(p4a)+'/'+str(len(s)):>26s} {str(p4b)+'/'+str(len(s)):>22s}")

    # ================================================================== predictions
    P("")
    P("=" * 122)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 122)
    m3, _, _ = logit(A[["one", "absd", "neg"]].values, A.clears.values.astype(float),
                     ["one", "absd", "neg"])
    m4, _, _ = logit(A[["one", "absd", "neg", "logband"]].values, A.clears.values.astype(float),
                     ["one", "absd", "neg", "logband"])
    c_absd = m3[m3.term == "absd"].iloc[0]
    c_neg4 = m4[m4.term == "neg"].iloc[0]
    negrate = A[A.dSharpe < 0].clears.mean()
    posrate = A[A.dSharpe > 0].clears.mean()
    pc_neg = (cl.dSharpe < 0).mean()
    ncl_neg = (A[~A.clears].dSharpe < 0).mean()
    k4b = A[A.pass4b == 1]
    s3 = WF[WF.selector == "S3 clause+positive"].set_index(["corpus", "panel", "family", "cost"])
    s2 = WF[WF.selector == "S2 clause-gated"].set_index(["corpus", "panel", "family", "cost"])
    d3 = float((s3.OOS_Sharpe - s0.OOS_Sharpe).mean())
    d32 = float((s3.OOS_Sharpe - s2.OOS_Sharpe).mean())
    preds = [
        ("P1 |dSharpe| positive & significant in the logit",
         c_absd.coef > 0 and c_absd.p < 0.05, f"coef {c_absd.coef:+.3f}, z {c_absd.z:+.2f}, p {c_absd.p:.2g}"),
        ("P2 NEG dummy insignificant once |d| and band are controlled",
         c_neg4.p >= 0.05, f"coef {c_neg4.coef:+.3f}, z {c_neg4.z:+.2f}, p {c_neg4.p:.2g}"),
        ("P3 clearing arms skew negative",
         pc_neg > ncl_neg, f"P(d<0|clear) {pc_neg:.1%} vs P(d<0|not clear) {ncl_neg:.1%}"),
        ("P4 at least one clearing arm is positive",
         len(clp) > 0, f"{len(clp)} of {len(cl)} clearing arms have dSharpe > 0"),
        ("P5 clear rate among 4b passes << corpus rate",
         (k4b.clears.mean() if len(k4b) else 0) < A.clears.mean(),
         f"{(k4b.clears.mean() if len(k4b) else np.nan):.1%} vs corpus {A.clears.mean():.1%}"),
        ("P6 S3 does NOT beat do-nothing OOS", d3 <= 0, f"S3 - S0 = {d3:+.4f} mean OOS Sharpe"),
        ("P7 S3 >= S2", d32 >= -1e-12, f"S3 - S2 = {d32:+.4f} mean OOS Sharpe"),
    ]
    for nm, hit, detail in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:58s}  {detail}")
    P(f"  {sum(1 for _, h, _ in preds if h)} of {len(preds)} predictions hit.")

    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
    return dict(A=A, WF=WF, summary=pd.DataFrame(summary), preds=preds)


if __name__ == "__main__":
    main()
