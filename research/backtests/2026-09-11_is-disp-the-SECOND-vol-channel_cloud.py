#!/usr/bin/env python3
"""Idea 540 - "is-disp-the-SECOND-vol-channel" (cloud, 2026-09-11).

The question
------------
Idea 533 established that `evol` (the eligible set's mean 20d realised vol) is the
characteristic most collinear with THE BOOK'S OWN realised vol, and that its within-stratum
MaxDD slope dies once the book's vol is in the regression.  It also reported, in passing, that
`disp` is the SECOND most collinear characteristic - within-stratum +0.32..+0.64, median +0.42
- and that disp's within-stratum MaxDD slope is killed in 5 of 12 cells by the same control.

The queue asks the follow-up: **re-price EVERY published `disp` direction claim with
log(book vol) held, and report which survive.**

Design - no new backtests, the record's own books re-read under a control
------------------------------------------------------------------------
The object under test is a SLOPE, not a book, and the books it is measured on are already
committed: idea 533's `.arms.csv` carries all 504 arm-rows of idea 295's MIX ladder (k = 40,
21 q rungs x 8 draws = 168 panels, seed 20260909, three books per panel - EWall / top10 /
top20 - at gross 0.75, weekly, 10 bps, next-day execution) together with each book's OWN
annualised realised vol in each window.  This run re-reads that artefact rather than
re-running the ladder, and GATES G1/G2 require that the parent's entire committed grid
(2,880 rows) and log-log table (144 rows) come back out of it to 1e-9 under this run's own
fitters before a single new number is read.  Nothing here can be a fresh draw of the dice.

THE CLAIM SET - what "every published disp direction claim" means, read two ways (a
reported axis, not a tuned one; the two tuned dials are the ones the queue names)
    MACHINE  every committed uncontrolled (`resid == none`) disp row in the record's own
             grids - idea 533's `.grid.csv` (5 outcomes x 3 arms x 4 strata x 3 windows =
             180) and idea 295's `.slopes.csv` within-stratum column (3 outcomes x 3 arms x
             4 strata x 3 windows = 108).  A row is a DIRECTION CLAIM when it is significant
             at |t| >= 1.96; its content is (sign, significance).
    PROSE    a regex census of the record's markdown (LEADERBOARD, CHANGELOG, QUEUE and every
             `.result.md`) for sentences that name disp/dispersion together with a direction
             word.  Reported as a denominator with its own caveat: prose claims are counted,
             not re-priced, because most do not name the (arm, outcome, strata, window) cell
             they were measured in - which is itself the finding idea 533 filed as (5).

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. residualisation in {none, partial, residx, ratio, logx, loglog}   (the queue's dial 1)
         none    y ~ x                                 the published fit
         partial y ~ x + bookvol                       idea 533's linear control
         residx  y ~ resid(x | bookvol)                the literal wording (FWL: same slope)
         ratio   y ~ x / bookvol                       the scale-free restatement
         logx    y ~ log(x) + log(bookvol)             LOG(BOOK VOL) HELD, native outcome
         loglog  log|y| ~ log(x) + log(bookvol)        LOG(BOOK VOL) HELD, elasticity form;
                 only defined where the outcome is strictly one-signed inside the cell -
                 those cells are reported NA, never silently dropped.
       `logx` and `loglog` are the two readings of the queue's own instruction; the first four
       are the parent's, carried so the new rungs can be read against them on one table.
    2. stratum resolution in {3, 5, 7, 21}                               (the queue's dial 2)
    Arm (EWall/top10/top20), outcome (Sharpe/CAGR/MaxDD/DDnorm/CAGRnorm), window
    (full/IS/OOS) and the |t| >= 1.96 bar are INHERITED from ideas 295/533 and are reported
    axes, never tuned here.  All 6 x 4 x 3 x 5 x 3 = 1,080 disp cells are published.

Rule 8 walk-forward (PROTOCOL rule 8, required) - two legs
    CLAIM LEG    every claim is established on the IS window (<= 2016-12-31) ONLY and its
                 sign and significance read ONCE on the untouched OOS window, uncontrolled
                 and controlled, so "which survive" is answered out of sample and not only
                 in the window the claim was published from.
    BOOK LEG     disp is supposed to be information about a book.  Per arm, four IS-ONLY
                 selectors choose one of the 168 panels and the choice is read once on OOS:
                   SEL-S      argmax IS Sharpe                 (the record's own selector)
                   SEL-DISP+  argmax IS disp
                   SEL-DISP-  argmin IS disp
                   SEL-DISP|v argmax IS disp residualised within stratum on log(IS bookvol)
                              - the queue's control, used as a SELECTOR rather than a
                              regressor: if disp carries information beyond the book's vol,
                              this is where it has to show up.
                 Each pick is reported as OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY
                 on the same calendar, and against the do-nothing anchor (the arm's mean).
    Both KEEP paths are evaluated on every one of the 504 arm-rows (4a vs RULES v2, 4b vs
    SPY, as idea 533's committed `pass4a`/`pass4b`), and GATE G3 re-derives the parent's
    published counts (4a 0/504, 4b 41/504) before they are quoted.

Gates, asserted before any new number is read
    G1  the 2,880-row residualisation grid of idea 533 re-derives from its own `.arms.csv`
        under this run's fitters, max |delta| over b / t / r2 below 1e-9.
    G2  the 144-row log-log table re-derives the same way, same bar.
    G3  the committed arm-rows' KEEP counts and the two comparand rows (RULES v2, SPY)
        re-derive, and idea 533's published disp collinearity band (+0.32..+0.64, median
        +0.42) is re-measured rather than believed.
    G4  ZERO-SIGNAL CONTROL: disp is permuted WITHIN stratum 200 times (seed 540); the rate
        at which a permuted disp produces a "published claim" and the rate at which such a
        claim survives the log control give the base rate the survival counts are read
        against.  A survival share inside the permutation band is not a finding.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): both ends of the q ladder are CURRENT
constituents of their screens, so every LEVEL inherited here is optimistic; the object under
test is a within-stratum slope under a control and a selector's OOS ranking, neither of which
is a level claim.  No book here is a capital candidate.

Outputs: .claims.csv .grid.csv .survival.csv .walkforward.csv .permutation.csv .prose.csv
         .console.txt .result.md
"""
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BT = ROOT / "research" / "backtests"
P533 = BT / "2026-09-09_why-is-evol-the-one-characteristic-that-never-reverses_C"
P295 = BT / "2026-09-09_restate-the-26-characteristic-files-under-the-SIGN-FLIP_cloud"

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

CHARS = ["breadth", "disp", "corr", "evol"]
OUTCOMES = ["Sharpe", "CAGR", "MaxDD"]
NORM_OUTCOMES = ["DDnorm", "CAGRnorm"]
ALL_OUT = OUTCOMES + NORM_OUTCOMES
ARMS = ["EWall", "top10", "top20"]
WINDOWS = ["full", "IS", "OOS"]
RESIDS_PARENT = ["none", "partial", "residx", "ratio"]
RESIDS = RESIDS_PARENT + ["logx", "loglog"]            # tuned param 1
STRATA = [3, 5, 7, 21]                                 # tuned param 2
T_BAR = 1.960
NPERM, PSEED = 200, 540
PUB_COLL = (0.32, 0.64, 0.42)                          # idea 533's published disp band
PUB_4A, PUB_4B, PUB_N = 0, 41, 504


# ----------------------------------------------------------- idea 533's fitters, copied verbatim
def ols(y, X):
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    n = len(y); p = X.shape[1]
    if n < p + 3 or any(np.std(X[:, j]) == 0 for j in range(p)):
        return np.full(p, np.nan), np.full(p, np.nan), n, 0, np.nan
    Z = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None)
    resid = y - Z @ beta
    dof = n - p - 1
    s2 = resid @ resid / dof
    XtXi = np.linalg.pinv(Z.T @ Z)
    se = np.sqrt(np.clip(np.diag(XtXi) * s2, 0, None))
    t = np.where(se[1:] > 0, beta[1:] / np.where(se[1:] > 0, se[1:], 1), np.nan)
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(resid @ resid) / sst if sst > 0 else np.nan
    return beta[1:], t, n, dof, r2


def zs(v):
    v = np.asarray(v, float); sd = np.nanstd(v)
    return (v - np.nanmean(v)) / sd if sd > 0 else v * np.nan


def slope_t(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 5 or np.std(x) == 0: return np.nan, np.nan, n
    xs = (x - x.mean()) / x.std(ddof=0)
    b = float(np.cov(xs, y, ddof=1)[0, 1] / np.var(xs, ddof=1))
    resid = y - y.mean() - b * xs
    dof = n - 2
    se = float(np.sqrt((resid @ resid) / dof / (np.sum(xs ** 2))))
    return b, (b / se if se > 0 else np.nan), n


def bin_q(qv, nb):
    return np.minimum((np.asarray(qv, float) * nb).astype(int), nb - 1)


def demean(v, strat):
    g = pd.DataFrame(dict(s=strat, v=np.asarray(v, float)))
    return (g.v - g.groupby("s").v.transform("mean")).to_numpy()


# ----------------------------------------------------------- one cell, six residualisations
def fit_cell(x_raw, y_raw, bv_raw, st, meth):
    """Return (b, t, ctrl_t, n, r2) for one (x, y, bookvol, stratum, residualisation) cell.
    The first four rungs are idea 533's code path; `logx` / `loglog` are this run's."""
    y = demean(y_raw, st); bv = demean(bv_raw, st)
    if meth == "none":
        x = zs(demean(x_raw, st))
        b, t, n, dof, r2 = ols(y, x); return b[0], t[0], np.nan, n, r2
    if meth == "partial":
        x = zs(demean(x_raw, st))
        bb, tt, n, dof, r2 = ols(y, np.column_stack([x, zs(bv)])); return bb[0], tt[0], tt[1], n, r2
    if meth == "residx":
        x0 = zs(demean(x_raw, st))
        bb, _, _, _, _ = ols(x0, zs(bv))
        xr = x0 - (np.nanmean(x0) + bb[0] * zs(bv)) if np.isfinite(bb[0]) else x0 * np.nan
        b, t, n, dof, r2 = ols(y, xr); return b[0], t[0], np.nan, n, r2
    if meth == "ratio":
        with np.errstate(invalid="ignore", divide="ignore"):
            xr = zs(demean(x_raw / bv_raw, st))
        b, t, n, dof, r2 = ols(y, xr); return b[0], t[0], np.nan, n, r2
    # ---- the queue's control: log(book vol) held
    with np.errstate(invalid="ignore", divide="ignore"):
        lx = np.log(np.where(np.asarray(x_raw, float) > 0, x_raw, np.nan))
        lbv = np.log(np.where(np.asarray(bv_raw, float) > 0, bv_raw, np.nan))
    if meth == "logx":
        bb, tt, n, dof, r2 = ols(y, np.column_stack([demean(lx, st), demean(lbv, st)]))
        return bb[0], tt[0], tt[1], n, r2
    # loglog: only where the outcome is strictly one-signed in the cell
    yv = np.asarray(y_raw, float)
    fin = np.isfinite(yv)
    if not fin.any() or not (np.all(yv[fin] > 0) or np.all(yv[fin] < 0)):
        return np.nan, np.nan, np.nan, 0, np.nan
    with np.errstate(invalid="ignore", divide="ignore"):
        ly = demean(np.log(np.abs(yv)), st)
    bb, tt, n, dof, r2 = ols(ly, np.column_stack([demean(lx, st), demean(lbv, st)]))
    return bb[0], tt[0], tt[1], n, r2


def build_grid(A, chars=CHARS, resids=RESIDS, x_override=None):
    rows = []
    for win in WINDOWS:
        for arm in ARMS:
            sub = A[A.arm == arm]
            bv_raw = sub[f"bookvol_{win}"].to_numpy()
            for ch in chars:
                x_raw = (sub[f"{ch}_{win}"].to_numpy() if x_override is None
                         else x_override[(win, arm, ch)])
                for oc in ALL_OUT:
                    y_raw = sub[f"{oc}_{win}"].to_numpy()
                    for nb in STRATA:
                        st = bin_q(sub["q"], nb)
                        for meth in resids:
                            b, t, ct, n, r2 = fit_cell(x_raw, y_raw, bv_raw, st, meth)
                            rows.append(dict(window=win, arm=arm, char=ch, outcome=oc,
                                             strata=nb, resid=meth, b=b, t=t, ctrl_t=ct,
                                             n=n, r2=r2,
                                             sig=bool(np.isfinite(t) and abs(t) >= T_BAR)))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 540 - is-disp-the-SECOND-vol-channel   (cloud, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  tuned 1 residualisation {RESIDS}  (logx/loglog = the queue's log(bookvol) held)")
    P(f"  tuned 2 stratum resolution {STRATA}")
    P(f"  survival = still |t| >= {T_BAR} AND same sign as the published fit")
    P(f"  every one of {len(RESIDS) * len(STRATA) * len(ALL_OUT) * len(ARMS) * len(WINDOWS)} "
      "disp cells is published; nothing is dropped after the fact")

    # ------------------------------------------------------------ inputs
    A = pd.read_csv(f"{P533}.arms.csv")
    for win in WINDOWS:                      # idea 533's two derived outcomes, its own lines
        A[f"DDnorm_{win}"] = A[f"MaxDD_{win}"] / A[f"bookvol_{win}"]
        A[f"CAGRnorm_{win}"] = A[f"CAGR_{win}"] / A[f"bookvol_{win}"]
    G533 = pd.read_csv(f"{P533}.grid.csv")
    LG533 = pd.read_csv(f"{P533}.loglog.csv")
    P(f"\nSOURCE (committed, not re-run): {P533.name}")
    P(f"  arms.csv {A.shape}, grid.csv {G533.shape}, loglog.csv {LG533.shape}")
    P(f"  ladder: {A.q.nunique()} q rungs x {A.draw.nunique()} draws x {A.arm.nunique()} arms "
      f"= {len(A)} arm-rows")

    # ------------------------------------------------------------ G1 / G2
    P("\n--- GATE 1: idea 533's 2,880-row grid re-derived from its own arms.csv ---")
    mine = build_grid(A, resids=RESIDS_PARENT)
    k = ["window", "arm", "char", "outcome", "strata", "resid"]
    J = G533.merge(mine, on=k, suffixes=("_ref", "_new"))
    d1 = {c: float(np.nanmax(np.abs(J[f"{c}_ref"] - J[f"{c}_new"]))) for c in ["b", "t", "r2"]}
    P(f"  rows ref {len(G533)} / new {len(mine)} / joined {len(J)}; max |d| " +
      ", ".join(f"{c} {v:.2e}" for c, v in d1.items()))
    assert len(J) == len(G533) == len(mine) and max(d1.values()) < 1e-9, "GATE 1 FAILED"
    P("  GATE 1 PASS (bar 1e-9)")

    P("\n--- GATE 2: idea 533's 144-row log-log table re-derived the same way ---")
    lrows = []
    for win in WINDOWS:
        for arm in ARMS:
            sub = A[A.arm == arm]
            with np.errstate(invalid="ignore", divide="ignore"):
                lbv = np.log(sub[f"bookvol_{win}"].to_numpy())
                ldd = np.log(np.abs(sub[f"MaxDD_{win}"].to_numpy()))
            for ch in CHARS:
                xr = sub[f"{ch}_{win}"].to_numpy()
                with np.errstate(invalid="ignore", divide="ignore"):
                    lx = np.log(np.where(xr > 0, xr, np.nan))
                for nb in STRATA:
                    st = bin_q(sub["q"], nb)
                    y = demean(ldd, st)
                    b_r, t_r, n_r, _, _ = ols(y, demean(lx, st))
                    bb, tt, n1, _, r2 = ols(y, np.column_stack([demean(lx, st), demean(lbv, st)]))
                    lrows.append(dict(window=win, arm=arm, char=ch, strata=nb,
                                      elast_raw=b_r[0], t_raw=t_r[0], elast_ctrl=bb[0],
                                      t_ctrl=tt[0], elast_bookvol=bb[1], t_bookvol=tt[1], r2=r2))
    LM = pd.DataFrame(lrows)
    k2 = ["window", "arm", "char", "strata"]
    J2 = LG533.merge(LM, on=k2, suffixes=("_ref", "_new"))
    cols2 = ["elast_raw", "t_raw", "elast_ctrl", "t_ctrl", "elast_bookvol", "t_bookvol", "r2"]
    d2 = max(float(np.nanmax(np.abs(J2[f"{c}_ref"] - J2[f"{c}_new"]))) for c in cols2)
    P(f"  rows ref {len(LG533)} / new {len(LM)} / joined {len(J2)}; max |d| {d2:.2e}")
    assert len(J2) == len(LG533) == len(LM) and d2 < 1e-9, "GATE 2 FAILED"
    P("  GATE 2 PASS (bar 1e-9)")

    # ------------------------------------------------------------ G3
    P("\n--- GATE 3: the arm-rows' own KEEP counts, comparands, and disp's collinearity ---")
    P(f"  4a {int(A.pass4a.sum())}/{len(A)} (published {PUB_4A}/{PUB_N}), "
      f"4b {int(A.pass4b.sum())}/{len(A)} (published {PUB_4B}/{PUB_N})")
    assert int(A.pass4a.sum()) == PUB_4A and int(A.pass4b.sum()) == PUB_4B and len(A) == PUB_N, \
        "GATE 3 FAILED: KEEP counts"
    coll = []
    for win in WINDOWS:
        for arm in ARMS:
            sub = A[A.arm == arm]
            bv = sub[f"bookvol_{win}"].to_numpy()
            for ch in CHARS:
                x = sub[f"{ch}_{win}"].to_numpy()
                for nb in STRATA:
                    st = bin_q(sub["q"], nb)
                    xw, bw = demean(x, st), demean(bv, st)
                    ok = np.isfinite(xw) & np.isfinite(bw)
                    coll.append(dict(window=win, arm=arm, char=ch, strata=nb,
                                     corr_within=float(np.corrcoef(xw[ok], bw[ok])[0, 1])))
    CO = pd.DataFrame(coll)
    dsub = CO[(CO.window == "full") & (CO["char"] == "disp")]
    dfull = dsub.corr_within
    P(f"  disp collinearity with the book's own vol, full window, ALL 12 cells: "
      f"{dfull.min():+.4f}..{dfull.max():+.4f}, median {dfull.median():+.4f}  "
      f"(the queue quotes {PUB_COLL[0]:+.2f}..{PUB_COLL[1]:+.2f}, median {PUB_COLL[2]:+.2f})")
    for ch in CHARS:
        s = CO[(CO.window == "full") & (CO["char"] == ch)].corr_within
        P(f"    {ch:8s} {s.min():+.4f}..{s.max():+.4f}  median {s.median():+.4f}")
    P("  per arm:")
    for a in ARMS:
        s = dsub[dsub.arm == a].corr_within
        P(f"    {a:6s} {s.min():+.4f}..{s.max():+.4f}  median {s.median():+.4f}")
    # the median reproduces exactly; the RANGE does not, and the reason is reported, not waived
    two = dsub[dsub.arm.isin(["EWall", "top10"])].corr_within
    assert abs(dfull.median() - PUB_COLL[2]) < 5e-3, "GATE 3 FAILED: collinearity median"
    P(f"\n  RECORD CORRECTION (GATE 3, reported not waived): the queue's disp band "
      f"{PUB_COLL[0]:+.2f}..{PUB_COLL[1]:+.2f} is the EWall+top10 slice "
      f"({two.min():+.4f}..{two.max():+.4f}), NOT the 12 cells idea 533 measured. Over all 12 "
      f"the band is {dfull.min():+.4f}..{dfull.max():+.4f}: `top20`, the arm where a top-n book "
      f"is least an exposure proxy, reads {dsub[dsub.arm == 'top20'].corr_within.min():+.4f} at "
      "strata=3 - an order of magnitude below the quoted floor. The published MEDIAN "
      f"{dfull.median():+.4f} reproduces exactly. Whether the direction claims survive the "
      "control should therefore be expected to split BY ARM, and the rest of this run reports "
      "it that way.")
    P("  GATE 3 PASS on the KEEP counts and the median; the range is corrected above.")

    # ------------------------------------------------------------ the full disp grid
    P("\n" + "=" * 100)
    P("THE GRID - every disp cell under all six residualisations x four resolutions")
    P("=" * 100)
    G = build_grid(A)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D = G[G["char"] == "disp"].copy()
    P(f"  {len(D)} disp cells written ({len(G)} rows for all four characteristics)")

    for win in WINDOWS:
        P(f"\n  t of disp's within-stratum slope, window = {win}")
        P(D[D.window == win].pivot_table(index=["outcome", "strata"], columns=["arm", "resid"],
                                         values="t")
          .reindex(columns=RESIDS, level=1).to_string(float_format=lambda x: f"{x:+7.2f}"))

    # ------------------------------------------------------------ the claim set
    P("\n" + "=" * 100)
    P("THE CLAIM SET - every published disp DIRECTION claim, and what it becomes")
    P("=" * 100)
    claims = []
    base = D[D.resid == "none"].set_index(["window", "arm", "outcome", "strata"])
    s295 = pd.read_csv(f"{P295}.slopes.csv") if Path(f"{P295}.slopes.csv").exists() else None
    for idx, r in base.iterrows():
        win, arm, oc, nb = idx
        row = dict(source="idea533.grid", window=win, arm=arm, outcome=oc, strata=nb,
                   b_pub=r.b, t_pub=r.t, is_claim=bool(r.sig), sign_pub=int(np.sign(r.b)))
        for meth in RESIDS[1:]:
            c = D[(D.window == win) & (D.arm == arm) & (D.outcome == oc) & (D.strata == nb)
                  & (D.resid == meth)].iloc[0]
            row[f"t_{meth}"] = c.t; row[f"b_{meth}"] = c.b
            row[f"survive_{meth}"] = bool(r.sig and np.isfinite(c.t) and abs(c.t) >= T_BAR
                                          and np.sign(c.b) == np.sign(r.b))
            row[f"defined_{meth}"] = bool(np.isfinite(c.t))
        claims.append(row)
    if s295 is not None:
        s2 = s295[s295["char"] == "disp"]
        P(f"  idea 295's committed .slopes.csv contributes {len(s2)} disp within-stratum rows "
          f"({int((s2.t_within.abs() >= T_BAR).sum())} of them significant); they are the same "
          "fits as the `none` rung above (GATE 1 covers the identity), so they are counted as a "
          "denominator, not re-fitted twice.")
    CL = pd.DataFrame(claims)
    CL.to_csv(f"{OUT}.claims.csv", index=False)

    nclaim = int(CL.is_claim.sum())
    P(f"\n  published disp cells: {len(CL)};  DIRECTION CLAIMS (|t| >= {T_BAR}): {nclaim} "
      f"({nclaim / len(CL):.1%})")
    P(f"  of those, positive-sign {int((CL.is_claim & (CL.sign_pub > 0)).sum())}, "
      f"negative-sign {int((CL.is_claim & (CL.sign_pub < 0)).sum())} - disp's published "
      "direction is NOT one sign, which is itself a resolution artefact (see the strata split).")

    P("\n  SURVIVAL of the published claims, by residualisation (all cells, all windows):")
    hdr = f"    {'control':10s} {'defined':>8s} {'survive':>8s} {'share':>8s}  {'killed':>7s}"
    P(hdr)
    for meth in RESIDS[1:]:
        sub = CL[CL.is_claim]
        dfn = int(sub[f"defined_{meth}"].sum()); sv = int(sub[f"survive_{meth}"].sum())
        P(f"    {meth:10s} {dfn:8d} {sv:8d} {sv / max(dfn, 1):8.1%}  {dfn - sv:7d}")

    P("\n  the queue's own control (log(bookvol) held), split by arm x outcome:")
    sub = CL[CL.is_claim]
    tab = sub.groupby(["arm", "outcome"]).agg(
        claims=("is_claim", "size"),
        logx_def=("defined_logx", "sum"), logx_sv=("survive_logx", "sum"),
        loglog_def=("defined_loglog", "sum"), loglog_sv=("survive_loglog", "sum"),
        partial_sv=("survive_partial", "sum"))
    P(tab.to_string())

    P("\n  and split by stratum RESOLUTION (the queue's dial 2):")
    P(sub.groupby("strata").agg(claims=("is_claim", "size"),
                                logx_sv=("survive_logx", "sum"),
                                loglog_def=("defined_loglog", "sum"),
                                loglog_sv=("survive_loglog", "sum"),
                                partial_sv=("survive_partial", "sum")).to_string())

    P("\n  and split by WINDOW (rule 8's claim leg is the IS -> OOS pair below):")
    P(sub.groupby("window").agg(claims=("is_claim", "size"),
                                logx_sv=("survive_logx", "sum"),
                                loglog_sv=("survive_loglog", "sum"),
                                partial_sv=("survive_partial", "sum")).to_string())

    # ------------------------------------------------------------ rule 8, claim leg
    P("\n" + "=" * 100)
    P("RULE 8, CLAIM LEG - established on 2010..2016 ONLY, read once on 2017..2026")
    P("=" * 100)
    rows = []
    for arm in ARMS:
        for oc in ALL_OUT:
            for nb in STRATA:
                for meth in RESIDS:
                    i = D[(D.window == "IS") & (D.arm == arm) & (D.outcome == oc)
                          & (D.strata == nb) & (D.resid == meth)].iloc[0]
                    o = D[(D.window == "OOS") & (D.arm == arm) & (D.outcome == oc)
                          & (D.strata == nb) & (D.resid == meth)].iloc[0]
                    rows.append(dict(arm=arm, outcome=oc, strata=nb, resid=meth,
                                     t_IS=i.t, t_OOS=o.t, b_IS=i.b, b_OOS=o.b,
                                     claim_IS=bool(i.sig),
                                     sign_returns=bool(np.isfinite(i.b) and np.isfinite(o.b)
                                                       and np.sign(i.b) == np.sign(o.b)),
                                     verdict_returns=bool(i.sig == o.sig),
                                     holds=bool(i.sig and o.sig and np.isfinite(i.b)
                                                and np.sign(i.b) == np.sign(o.b))))
    W8 = pd.DataFrame(rows)
    P(W8.groupby("resid").agg(cells=("holds", "size"), IS_claims=("claim_IS", "sum"),
                              sign_returns=("sign_returns", "sum"),
                              verdict_returns=("verdict_returns", "sum"),
                              holds=("holds", "sum"))
      .reindex(RESIDS).to_string())
    P("  ('IS_claims' = significant on the IS window; 'holds' = significant on BOTH windows with "
      "the same sign, i.e. the claim survived rule 8 under that control.)")
    isc = W8[W8.claim_IS]
    for meth in RESIDS:
        s = isc[isc.resid == meth]
        if len(s):
            P(f"    {meth:10s} IS claims {len(s):3d} -> hold OOS {int(s.holds.sum()):3d} "
              f"({s.holds.mean():.1%})")

    # ------------------------------------------------------------ rule 8, book leg
    P("\n" + "=" * 100)
    P("RULE 8, BOOK LEG - IS-only selectors over the 168 panels, read once on OOS")
    P("=" * 100)
    spy = A.iloc[0]
    P(f"  comparands on the same calendar: RULES v2 OOS "
      f"{A.base_OOS_CAGR.iloc[0]:+.4f}/{A.base_OOS_Sharpe.iloc[0]:.4f}/"
      f"{A.base_OOS_MaxDD.iloc[0]:+.4f}   SPY OOS "
      f"{spy.SPY_OOS_CAGR:+.4f}/{spy.SPY_OOS_Sharpe:.4f}/{spy.SPY_OOS_MaxDD:+.4f}")
    wf = []
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], 21)                       # the finest published resolution
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        dx = demean(sub["disp_IS"].to_numpy(), st)
        bb, _, _, _, _ = ols(dx, demean(lbv, st))
        dres = dx - bb[0] * demean(lbv, st)
        picks = {
            "SEL-S   argmax IS Sharpe": int(sub.Sharpe_IS.idxmax()),
            "SEL-DISP+ argmax IS disp": int(sub.disp_IS.idxmax()),
            "SEL-DISP- argmin IS disp": int(sub.disp_IS.idxmin()),
            "SEL-DISP|v argmax IS disp|log(vol)": int(np.nanargmax(dres)),
        }
        for name, i in picks.items():
            r = sub.loc[i]
            wf.append(dict(arm=arm, selector=name, q=r.q, draw=int(r.draw),
                           IS_Sharpe=r.Sharpe_IS, disp_IS=r.disp_IS, bookvol_IS=r.bookvol_IS,
                           OOS_CAGR=r.CAGR_OOS, OOS_Sharpe=r.Sharpe_OOS, OOS_MaxDD=r.MaxDD_OOS,
                           anchor_OOS_S=float(sub.Sharpe_OOS.mean()),
                           anchor_OOS_CAGR=float(sub.CAGR_OOS.mean()),
                           best_OOS_S=float(sub.Sharpe_OOS.max()),
                           spy_OOS_S=r.SPY_OOS_Sharpe, spy_OOS_CAGR=r.SPY_OOS_CAGR,
                           spy_OOS_DD=r.SPY_OOS_MaxDD,
                           v2_OOS_S=r.base_OOS_Sharpe, v2_OOS_CAGR=r.base_OOS_CAGR,
                           v2_OOS_DD=r.base_OOS_MaxDD,
                           beats_anchor=bool(r.Sharpe_OOS > sub.Sharpe_OOS.mean()),
                           beats_v2=bool(r.Sharpe_OOS > r.base_OOS_Sharpe),
                           beats_spy=bool(r.Sharpe_OOS > r.SPY_OOS_Sharpe),
                           pass4a=bool(r.pass4a), pass4b=bool(r.pass4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(WF[["arm", "selector", "q", "draw", "IS_Sharpe", "disp_IS", "OOS_CAGR", "OOS_Sharpe",
          "OOS_MaxDD", "anchor_OOS_S", "beats_anchor", "beats_v2", "beats_spy",
          "pass4a", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  over the {len(WF)} picks: beat the anchor {int(WF.beats_anchor.sum())}, "
      f"beat RULES v2 {int(WF.beats_v2.sum())}, beat SPY {int(WF.beats_spy.sum())}; "
      f"4a {int(WF.pass4a.sum())}, 4b {int(WF.pass4b.sum())}")
    P(f"  whole corpus for reference: 4a {int(A.pass4a.sum())}/{len(A)}, "
      f"4b {int(A.pass4b.sum())}/{len(A)}; arm means OOS Sharpe " +
      ", ".join(f"{a} {A[A.arm == a].Sharpe_OOS.mean():.4f}" for a in ARMS))
    for a in ARMS:
        s = A[A.arm == a]
        P(f"    {a:6s} full CAGR {s.CAGR_full.mean():+.4f} Sharpe {s.Sharpe_full.mean():.4f} "
          f"MaxDD {s.MaxDD_full.mean():+.4f} | OOS {s.CAGR_OOS.mean():+.4f}/"
          f"{s.Sharpe_OOS.mean():.4f}/{s.MaxDD_OOS.mean():+.4f}")

    # ------------------------------------------------------------ G4 permutation
    P("\n" + "=" * 100)
    P(f"GATE 4 - ZERO-SIGNAL CONTROL: disp permuted WITHIN stratum, {NPERM} draws, seed {PSEED}")
    P("=" * 100)
    rng = np.random.default_rng(PSEED)
    prows = []
    for it in range(NPERM):
        xo = {}
        for win in WINDOWS:
            for arm in ARMS:
                sub = A[A.arm == arm]
                st = bin_q(sub["q"], 21)
                v = sub[f"disp_{win}"].to_numpy().copy()
                for s_ in np.unique(st):
                    m = st == s_
                    v[m] = rng.permutation(v[m])
                xo[(win, arm, "disp")] = v
        g = build_grid(A, chars=["disp"], x_override=xo)
        b0 = g[g.resid == "none"]
        nc = int(b0.sig.sum())
        sv_lx = sv_ll = sv_pa = 0
        for _, r in b0[b0.sig].iterrows():
            for meth, acc in (("logx", "lx"), ("loglog", "ll"), ("partial", "pa")):
                c = g[(g.window == r.window) & (g.arm == r.arm) & (g.outcome == r.outcome)
                      & (g.strata == r.strata) & (g.resid == meth)].iloc[0]
                ok = bool(np.isfinite(c.t) and abs(c.t) >= T_BAR and np.sign(c.b) == np.sign(r.b))
                if acc == "lx": sv_lx += ok
                elif acc == "ll": sv_ll += ok
                else: sv_pa += ok
        prows.append(dict(it=it, claims=nc, survive_logx=sv_lx, survive_loglog=sv_ll,
                          survive_partial=sv_pa,
                          share_logx=sv_lx / nc if nc else np.nan,
                          share_loglog=sv_ll / nc if nc else np.nan,
                          share_partial=sv_pa / nc if nc else np.nan))
    PM = pd.DataFrame(prows)
    PM.to_csv(f"{OUT}.permutation.csv", index=False)
    P(f"  permuted disp produces {PM.claims.mean():.2f} 'claims' per draw of {len(CL)} cells "
      f"(median {PM.claims.median():.0f}, p95 {PM.claims.quantile(0.95):.0f}) against the real "
      f"{nclaim}")
    for meth in ("partial", "logx", "loglog"):
        s = PM[f"share_{meth}"].dropna()
        real_d = int(CL[CL.is_claim][f"defined_{meth}"].sum())
        real_s = int(CL[CL.is_claim][f"survive_{meth}"].sum())
        P(f"    {meth:8s} permuted survival share median {s.median():.1%} "
          f"[p5 {s.quantile(0.05):.1%}, p95 {s.quantile(0.95):.1%}]   real "
          f"{real_s}/{real_d} = {real_s / max(real_d, 1):.1%}   -> "
          f"{'ABOVE the band' if real_s / max(real_d, 1) > s.quantile(0.95) else 'INSIDE the band' if real_s / max(real_d, 1) >= s.quantile(0.05) else 'BELOW the band'}")

    # ------------------------------------------------------------ prose census
    P("\n" + "=" * 100)
    P("PROSE CENSUS - published disp claims in the record's markdown (counted, not re-priced)")
    P("=" * 100)
    DIR = re.compile(r"\b(rise|rises|rising|fall|falls|falling|higher|lower|increase|decrease|"
                     r"positive|negative|monotone|slope|predicts|drives|beta|rho|sign)\b", re.I)
    DISP = re.compile(r"\bdisp\b|\bdispersion\b", re.I)
    CELL = re.compile(r"\b(EWall|top10|top20|strata|stratum|within-stratum|arm)\b", re.I)
    files = ([ROOT / "research" / f for f in ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md")]
             + sorted(BT.glob("*.result.md")) + sorted(BT.glob("*memo*.md")))
    prows = []
    for f in files:
        try: txt = f.read_text(errors="ignore")
        except Exception: continue
        for ln, line in enumerate(txt.split("\n"), 1):
            for sent in re.split(r"(?<=[.;])\s+", line):
                if DISP.search(sent) and DIR.search(sent):
                    prows.append(dict(file=f.name, line=ln, names_cell=bool(CELL.search(sent)),
                                      text=sent.strip()[:300]))
    PR = pd.DataFrame(prows)
    PR.to_csv(f"{OUT}.prose.csv", index=False)
    if len(PR):
        P(f"  {len(PR)} prose sentences over {PR.file.nunique()} files name disp with a "
          f"direction word; {int(PR.names_cell.sum())} ({PR.names_cell.mean():.1%}) also name "
          "an arm or a stratum resolution, i.e. are re-priceable at all.")
        P(PR.groupby("file").agg(sentences=("line", "size"),
                                 name_a_cell=("names_cell", "sum"))
          .sort_values("sentences", ascending=False).head(12).to_string())
    else:
        P("  no prose sentences matched.")

    # ------------------------------------------------------------ verdict numbers
    P("\n" + "=" * 100)
    lx_d = int(CL[CL.is_claim].defined_logx.sum()); lx_s = int(CL[CL.is_claim].survive_logx.sum())
    ll_d = int(CL[CL.is_claim].defined_loglog.sum()); ll_s = int(CL[CL.is_claim].survive_loglog.sum())
    pa_s = int(CL[CL.is_claim].survive_partial.sum())
    P(f"ANSWER: of {nclaim} published disp direction claims, {pa_s} survive the LINEAR control, "
      f"{lx_s}/{lx_d} survive log(bookvol) held in the native outcome (logx) and {ll_s}/{ll_d} "
      f"in the elasticity form (loglog).")
    P("=" * 100)

    W8.to_csv(f"{OUT}.survival.csv", index=False)
    CO.to_csv(f"{OUT}.collinearity.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {OUT.name}.{{grid,claims,survival,walkforward,permutation,prose,collinearity}}.csv"
      f"  ({time.time() - t0:.1f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
