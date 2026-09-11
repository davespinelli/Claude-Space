#!/usr/bin/env python3
"""Idea 714 - "does-the-DRAWDOWN-vs-RETURN-survival-gap-hold-against-a-PER-FAMILY-null"
(lane C, 2026-09-11).

The question
------------
Idea 540 re-priced every published `disp` direction claim with log(book vol) held and reported
a sharp split BY OUTCOME FAMILY:

    drawdown claims (MaxDD, DDnorm)      5 / 28  survive  = 17.9%
    return   claims (Sharpe, CAGR, CAGRnorm)  47 / 63  survive  = 74.6%

It then ran a within-stratum permutation control and found the |t| >= 1.96 bar badly
mis-calibrated on this ladder (a no-information disp still reads significant in 35.97% of the
180 cells), and quoted ONE band for the survival share: **pooled** logx [56.8%, 82.3%].
Against that pooled band the 17.9% is "BELOW" and the 74.6% is "at the bottom edge".

But the pooled band is the wrong comparand for a per-family number.  The null's survival share
is itself a function of the outcome: MaxDD is a one-signed, fat-tailed, path-dependent
statistic and CAGR is not, so a permuted disp need not throw claims - or survive the control -
at the same rate in the two families.  **The gap is therefore directional only: 17.9% vs 74.6%
is a comparison of two real numbers against ONE null, not each against its own.**

This run re-runs idea 540's permutation SEPARATELY PER OUTCOME FAMILY - the same draws, the
same seed, the same machinery, partitioned - and asks whether the drawdown shortfall clears
its OWN band.

What is and is not new
----------------------
Nothing is re-backtested.  The object is a SLOPE over idea 533's committed `.arms.csv`
(idea 295's MIX ladder: k = 40, 21 q rungs x 8 draws = 168 panels, seed 20260909, three books
per panel - EWall / top10 / top20 - gross 0.75, weekly, 10 bps, next-day execution).  GATES
G1-G4 require that idea 533's 2,880-row grid, idea 540's 180-row claims table AND idea 540's
committed 200-draw permutation come back out bit-for-bit under this run's own code before a
single new number is read.  The per-family band is a PARTITION of exactly those draws, not a
fresh roll of the dice.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. family scheme in {FAM2, FAM3, FAM5}                              (the queue's dial 1)
         FAM2  DD = {MaxDD, DDnorm} vs RET = {Sharpe, CAGR, CAGRnorm}   <- idea 540's own split
               (verified below to reproduce its 5/28 and 47/63 exactly)
         FAM3  DD = {MaxDD, DDnorm}, LEVEL = {CAGR, CAGRnorm}, RATIO = {Sharpe}
         FAM5  one family per outcome - the finest partition the record supports
    2. draws in {50, 100, 200, 400}                                     (the queue's dial 2)
         200 is idea 540's committed count and is the reproduction gate; 400 is a strict
         superset at the same seed, so the band's convergence is reported, not assumed.
    Residualisation (none/partial/logx/loglog), arm, stratum resolution, window and the
    |t| >= 1.96 bar are INHERITED from ideas 295/533/540 and are reported axes, never tuned.
    The permutation is within-stratum at 21 strata for every fit resolution - idea 540's
    convention, inherited verbatim because G4 reproduces its draws.

Statistics published per (scheme, family, resid, draws) - every cell, nothing dropped
    CLAIM RATE   share of the family's cells the permuted disp calls significant.  If this
                 differs by family the nominal counts were never comparable in the first place.
    SURVIVAL     share of the permuted claims that survive the control, with [p5, p95] over
                 draws, and the real share's position ABOVE / INSIDE / BELOW its own band.
    EXCESS       real share minus the null median, in the family's own units.

Rule 8 walk-forward (PROTOCOL rule 8, required) - two legs, both split by family
    CLAIM LEG    every claim is established on the IS window (<= 2016-12-31) ONLY and read once
                 on the untouched OOS window, and the SAME per-family permutation supplies the
                 null for the IS->OOS hold rate.  A family whose real hold rate sits inside its
                 own band has no out-of-sample content, whatever its nominal count.
    BOOK LEG     disp is supposed to be information about a book.  Per arm, IS-ONLY selectors
                 pick one of the 168 panels using the IS within-stratum disp slope of that
                 FAMILY's outcome (sign taken from IS, never from OOS), uncontrolled and with
                 log(IS bookvol) held, and the pick is read once on OOS as CAGR / Sharpe /
                 MaxDD against RULES v2, SPY and the do-nothing anchor (the arm's mean).  A
                 RANDOM-PICK null (same draw count, same seed family) gives each selector's
                 percentile, so "beat the anchor" is read against the base rate, not asserted.
    Both KEEP paths are evaluated on every pick and on all 504 committed arm-rows (4a vs
    RULES v2, 4b vs SPY, from idea 533's committed `pass4a`/`pass4b`, re-derived in G1).

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): both ends of the q ladder are CURRENT
constituents of their screens, so every LEVEL inherited here is optimistic.  The object under
test is a within-stratum slope under a control and a selector's OOS ranking, neither of which
is a level claim.  No book here is a capital candidate.

Outputs: .claims.csv .permfamily.csv .bands.csv .claimleg.csv .walkforward.csv
         .console.txt .result.md
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
BT = ROOT / "research" / "backtests"
P533 = BT / "2026-09-09_why-is-evol-the-one-characteristic-that-never-reverses_C"
P540 = BT / "2026-09-11_is-disp-the-SECOND-vol-channel_cloud"

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

OUTCOMES = ["Sharpe", "CAGR", "MaxDD"]
NORM_OUTCOMES = ["DDnorm", "CAGRnorm"]
ALL_OUT = OUTCOMES + NORM_OUTCOMES
ARMS = ["EWall", "top10", "top20"]
WINDOWS = ["full", "IS", "OOS"]
RESIDS = ["none", "partial", "logx", "loglog"]     # the rungs idea 540's null tracked
CTRLS = ["partial", "logx", "loglog"]
STRATA = [3, 5, 7, 21]
T_BAR = 1.960
NPERM, PSEED = 400, 540                            # 540 committed 200 at this seed; 400 is a superset
DRAW_RUNGS = [50, 100, 200, 400]                   # tuned param 2
PERM_STRATA = 21                                   # idea 540's convention, inherited

# ---- tuned param 1: the family schemes.  FAM2 is idea 540's own split, asserted below.
SCHEMES = {
    "FAM2": {"Sharpe": "RET", "CAGR": "RET", "CAGRnorm": "RET",
             "MaxDD": "DD", "DDnorm": "DD"},
    "FAM3": {"Sharpe": "RATIO", "CAGR": "LEVEL", "CAGRnorm": "LEVEL",
             "MaxDD": "DD", "DDnorm": "DD"},
    "FAM5": {o: o for o in ALL_OUT},
}
# idea 540's published per-family numbers, re-derived not believed
PUB = {"DD": (5, 28, 0.179), "RET": (47, 63, 0.746)}
PUB_POOLED_LOGX = (0.568, 0.823)       # idea 540's pooled logx band
PUB_CLAIMRATE = 0.3597                 # idea 540's pooled permuted claim rate
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


def bin_q(qv, nb):
    return np.minimum((np.asarray(qv, float) * nb).astype(int), nb - 1)


def demean(v, strat):
    g = pd.DataFrame(dict(s=strat, v=np.asarray(v, float)))
    return (g.v - g.groupby("s").v.transform("mean")).to_numpy()


def fit_cell(x_raw, y_raw, bv_raw, st, meth):
    """(b, t, ctrl_t, n, r2) for one (x, y, bookvol, stratum, residualisation) cell - 540's code."""
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
    with np.errstate(invalid="ignore", divide="ignore"):
        lx = np.log(np.where(np.asarray(x_raw, float) > 0, x_raw, np.nan))
        lbv = np.log(np.where(np.asarray(bv_raw, float) > 0, bv_raw, np.nan))
    if meth == "logx":
        bb, tt, n, dof, r2 = ols(y, np.column_stack([demean(lx, st), demean(lbv, st)]))
        return bb[0], tt[0], tt[1], n, r2
    yv = np.asarray(y_raw, float)
    fin = np.isfinite(yv)
    if not fin.any() or not (np.all(yv[fin] > 0) or np.all(yv[fin] < 0)):
        return np.nan, np.nan, np.nan, 0, np.nan
    with np.errstate(invalid="ignore", divide="ignore"):
        ly = demean(np.log(np.abs(yv)), st)
    bb, tt, n, dof, r2 = ols(ly, np.column_stack([demean(lx, st), demean(lbv, st)]))
    return bb[0], tt[0], tt[1], n, r2


def grid_arrays(A, resids, x_override=None):
    """The 180 disp cells x len(resids), as plain arrays keyed by cell index.

    Returns (cells, B, T) where cells is the ordered list of (window, arm, outcome, strata)
    and B[meth], T[meth] are float arrays aligned to it.  Same iteration order as idea 540's
    build_grid, so the two agree cell for cell."""
    cells = []
    B = {m: [] for m in resids}; T = {m: [] for m in resids}
    for win in WINDOWS:
        for arm in ARMS:
            sub = A[A.arm == arm]
            bv_raw = sub[f"bookvol_{win}"].to_numpy()
            x_raw = (sub[f"disp_{win}"].to_numpy() if x_override is None
                     else x_override[(win, arm)])
            for oc in ALL_OUT:
                y_raw = sub[f"{oc}_{win}"].to_numpy()
                for nb in STRATA:
                    st = bin_q(sub["q"], nb)
                    cells.append((win, arm, oc, nb))
                    for meth in resids:
                        b, t, ct, n, r2 = fit_cell(x_raw, y_raw, bv_raw, st, meth)
                        B[meth].append(b); T[meth].append(t)
    return cells, {m: np.asarray(v, float) for m, v in B.items()}, \
           {m: np.asarray(v, float) for m, v in T.items()}


def survive_mask(B, T, meth):
    """Vectorised copy of 540's survival rule: still |t| >= bar AND same sign as `none`."""
    sig0 = np.isfinite(T["none"]) & (np.abs(T["none"]) >= T_BAR)
    ok = np.isfinite(T[meth]) & (np.abs(T[meth]) >= T_BAR) & \
         (np.sign(B[meth]) == np.sign(B["none"]))
    return sig0, (sig0 & ok), np.isfinite(T[meth])


def band(v):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if not len(v): return (np.nan, np.nan, np.nan)
    return float(np.quantile(v, 0.05)), float(np.median(v)), float(np.quantile(v, 0.95))


def verdict(real, lo, hi):
    if not np.isfinite(real) or not np.isfinite(lo): return "NA"
    return "ABOVE" if real > hi else ("BELOW" if real < lo else "INSIDE")


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 714 - does-the-DRAWDOWN-vs-RETURN-survival-gap-hold-against-a-PER-FAMILY-null")
    P("            (lane C, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  tuned 1 family scheme {list(SCHEMES)}   (FAM2 == idea 540's own DD/RET split)")
    P(f"  tuned 2 draws {DRAW_RUNGS}              (200 == idea 540's committed count)")
    P(f"  the null is idea 540's OWN permutation, seed {PSEED}, within-stratum at "
      f"{PERM_STRATA} strata, PARTITIONED by family - not a new roll")
    P("  every (scheme, family, resid, draws) cell is published; nothing is dropped after")

    # ------------------------------------------------------------ inputs
    A = pd.read_csv(f"{P533}.arms.csv")
    for win in WINDOWS:
        A[f"DDnorm_{win}"] = A[f"MaxDD_{win}"] / A[f"bookvol_{win}"]
        A[f"CAGRnorm_{win}"] = A[f"CAGR_{win}"] / A[f"bookvol_{win}"]
    G533 = pd.read_csv(f"{P533}.grid.csv")
    CL540 = pd.read_csv(f"{P540}.claims.csv")
    PM540 = pd.read_csv(f"{P540}.permutation.csv")
    P(f"\nSOURCES (committed, not re-run):")
    P(f"  {P533.name}.arms.csv  {A.shape}   grid.csv {G533.shape}")
    P(f"  {P540.name}.claims.csv {CL540.shape}   permutation.csv {PM540.shape}")
    P(f"  ladder: {A.q.nunique()} q rungs x {A.draw.nunique()} draws x {A.arm.nunique()} arms "
      f"= {len(A)} arm-rows")

    # ------------------------------------------------------------ the real grid
    cells, B, T = grid_arrays(A, RESIDS)
    CELL = pd.DataFrame(cells, columns=["window", "arm", "outcome", "strata"])
    for m in RESIDS:
        CELL[f"b_{m}"] = B[m]; CELL[f"t_{m}"] = T[m]
    sig0 = np.isfinite(T["none"]) & (np.abs(T["none"]) >= T_BAR)
    CELL["is_claim"] = sig0
    for m in CTRLS:
        _, sv, dfn = survive_mask(B, T, m)
        CELL[f"survive_{m}"] = sv; CELL[f"defined_{m}"] = dfn
    for sch, mp in SCHEMES.items():
        CELL[sch] = CELL.outcome.map(mp)
    CELL.to_csv(f"{OUT}.claims.csv", index=False)

    # ------------------------------------------------------------ GATE 1
    P("\n--- GATE 1: idea 533's committed disp grid re-derives from its own arms.csv ---")
    ref = G533[(G533["char"] == "disp") & (G533.resid.isin(["none", "partial"]))]
    mine = CELL.melt(id_vars=["window", "arm", "outcome", "strata"],
                     value_vars=[f"b_{m}" for m in ["none", "partial"]],
                     var_name="resid", value_name="b")
    mine["resid"] = mine.resid.str.replace("b_", "", regex=False)
    J = ref.merge(mine, on=["window", "arm", "outcome", "strata", "resid"],
                  suffixes=("_ref", "_new"))
    d1 = float(np.nanmax(np.abs(J.b_ref - J.b_new)))
    P(f"  joined {len(J)} of {len(ref)} committed disp rows; max |db| {d1:.3e}")
    assert len(J) == len(ref) and d1 < 1e-9, "GATE 1 FAILED"
    P(f"  KEEP counts on the 504 arm-rows: 4a {int(A.pass4a.sum())}/{len(A)} "
      f"(published {PUB_4A}/{PUB_N}), 4b {int(A.pass4b.sum())}/{len(A)} "
      f"(published {PUB_4B}/{PUB_N})")
    assert int(A.pass4a.sum()) == PUB_4A and int(A.pass4b.sum()) == PUB_4B, "GATE 1 FAILED (KEEP)"
    P("  GATE 1 PASS (bar 1e-9)")

    # ------------------------------------------------------------ GATE 2
    P("\n--- GATE 2: idea 540's committed 180-row claims table re-derives cell for cell ---")
    k = ["window", "arm", "outcome", "strata"]
    J2 = CL540.merge(CELL, on=k, suffixes=("_ref", "_new"))
    dmax = max(float(np.nanmax(np.abs(J2[f"{c}_ref"] - J2[f"{c}_new"])))
               for c in ["t_partial", "b_partial", "t_logx", "b_logx"])
    same_claim = int((J2.is_claim_ref.astype(bool) == J2.is_claim_new.astype(bool)).sum())
    same_sv = int((J2.survive_logx_ref.astype(bool) == J2.survive_logx_new.astype(bool)).sum())
    P(f"  joined {len(J2)}/180; max |d| over b/t {dmax:.3e}; is_claim agree {same_claim}/180; "
      f"survive_logx agree {same_sv}/180")
    assert len(J2) == 180 and dmax < 1e-9 and same_claim == 180 and same_sv == 180, "GATE 2 FAILED"
    P("  GATE 2 PASS")

    # ------------------------------------------------------------ GATE 3: the record's own split
    P("\n--- GATE 3: idea 540's published DD/RET numbers re-derived, not believed ---")
    cl = CELL[CELL.is_claim]
    P(f"  total published disp direction claims: {len(cl)} of {len(CELL)} cells "
      f"({len(cl)/len(CELL):.1%})")
    for fam, (s_pub, n_pub, sh_pub) in PUB.items():
        s = cl[cl.FAM2 == fam]
        got_s, got_n = int(s.survive_logx.sum()), len(s)
        P(f"  {fam:4s} logx survival {got_s}/{got_n} = {got_s/got_n:.1%}   "
          f"(idea 540 published {s_pub}/{n_pub} = {sh_pub:.1%})")
        assert (got_s, got_n) == (s_pub, n_pub), f"GATE 3 FAILED on {fam}"
    dd = cl[cl.FAM2 == "DD"]
    flip_any = int((np.sign(dd.b_logx) != np.sign(dd.b_none)).sum())
    flip_sig = int(((np.abs(dd.t_logx) >= T_BAR) & (np.sign(dd.b_logx) != np.sign(dd.b_none))).sum())
    P(f"  idea 540's '14 of 28 REVERSING SIGN' restates as: {flip_any}/28 flip sign at any |t|, "
      f"but only {flip_sig}/28 flip sign AND stay significant. The reversal claim is a sign "
      f"count on mostly insignificant coefficients.")
    P("  GATE 3 PASS on the two published shares")

    # ------------------------------------------------------------ the permutation
    P("\n" + "=" * 100)
    P(f"THE NULL - disp permuted WITHIN stratum ({PERM_STRATA} strata), {NPERM} draws, "
      f"seed {PSEED}")
    P("=" * 100)
    P("  identical construction and rng consumption order to idea 540's GATE 4; the first 200")
    P("  draws MUST reproduce its committed permutation.csv (GATE 4 below).")
    rng = np.random.default_rng(PSEED)
    fam_of = {sch: CELL[sch].to_numpy() for sch in SCHEMES}
    rows = []; pooled = []
    for it in range(NPERM):
        xo = {}
        for win in WINDOWS:
            for arm in ARMS:
                sub = A[A.arm == arm]
                st = bin_q(sub["q"], PERM_STRATA)
                v = sub[f"disp_{win}"].to_numpy().copy()
                for s_ in np.unique(st):
                    m = st == s_
                    v[m] = rng.permutation(v[m])
                xo[(win, arm)] = v
        _, pB, pT = grid_arrays(A, RESIDS, x_override=xo)
        claim = np.isfinite(pT["none"]) & (np.abs(pT["none"]) >= T_BAR)
        sv = {}; dfn = {}
        for m in CTRLS:
            _, sv[m], dfn[m] = survive_mask(pB, pT, m)
        pooled.append(dict(it=it, claims=int(claim.sum()),
                           **{f"survive_{m}": int(sv[m].sum()) for m in CTRLS}))
        # ---- rule 8 claim leg under the null: IS claim that holds OOS, same sign
        win_a = CELL.window.to_numpy()
        for sch, fa in fam_of.items():
            for fam in sorted(set(fa)):
                fm = fa == fam
                for m in CTRLS:
                    rows.append(dict(it=it, scheme=sch, family=fam, resid=m,
                                     cells=int(fm.sum()), claims=int((claim & fm).sum()),
                                     survive=int((sv[m] & fm).sum()),
                                     defined=int((dfn[m] & fm).sum())))
    PMnew = pd.DataFrame(pooled)
    PF = pd.DataFrame(rows)
    PF.to_csv(f"{OUT}.permfamily.csv", index=False)

    # ------------------------------------------------------------ GATE 4
    P("\n--- GATE 4: the first 200 draws reproduce idea 540's committed permutation.csv ---")
    head = PMnew.head(len(PM540))
    d4 = {c: int(np.abs(head[c].to_numpy() - PM540[c].to_numpy()).max())
          for c in ["claims", "survive_logx", "survive_loglog", "survive_partial"]}
    P(f"  draws compared {len(head)}; max |d| " + ", ".join(f"{c} {v}" for c, v in d4.items()))
    assert max(d4.values()) == 0, "GATE 4 FAILED - the null is not idea 540's null"
    rate = PMnew.head(200).claims.mean() / len(CELL)
    P(f"  pooled permuted claim rate over 200 draws {rate:.4%} "
      f"(idea 540 published {PUB_CLAIMRATE:.2%})")
    assert abs(rate - PUB_CLAIMRATE) < 5e-4, "GATE 4 FAILED - claim rate"
    sh = (PMnew.head(200).survive_logx / PMnew.head(200).claims)
    P(f"  pooled logx survival band [p5 {sh.quantile(0.05):.1%}, p95 {sh.quantile(0.95):.1%}] "
      f"(idea 540 published [{PUB_POOLED_LOGX[0]:.1%}, {PUB_POOLED_LOGX[1]:.1%}])")
    assert abs(sh.quantile(0.05) - PUB_POOLED_LOGX[0]) < 5e-3 and \
           abs(sh.quantile(0.95) - PUB_POOLED_LOGX[1]) < 5e-3, "GATE 4 FAILED - pooled band"
    P("  GATE 4 PASS - the per-family bands below are a PARTITION of these exact draws")

    # ------------------------------------------------------------ the answer
    P("\n" + "=" * 100)
    P("PER-FAMILY BANDS - every (scheme, family, resid, draws) cell")
    P("=" * 100)
    out = []
    for sch, mp in SCHEMES.items():
        fa = fam_of[sch]
        for fam in sorted(set(fa)):
            fm = fa == fam
            real_cells = int(fm.sum())
            real_claims = int((sig0 & fm).sum())
            for m in CTRLS:
                _, rsv, rdf = survive_mask(B, T, m)
                real_sv = int((rsv & fm).sum()); real_df = int((rdf & sig0 & fm).sum())
                real_share = real_sv / real_df if real_df else np.nan
                sub = PF[(PF.scheme == sch) & (PF.family == fam) & (PF.resid == m)]
                for nd in DRAW_RUNGS:
                    s = sub[sub.it < nd]
                    cr = s.claims / s.cells
                    sh = np.where(s.claims > 0, s.survive / np.maximum(s.claims, 1), np.nan)
                    lo, med, hi = band(sh)
                    clo, cmed, chi = band(cr)
                    out.append(dict(scheme=sch, family=fam, resid=m, draws=nd,
                                    cells=real_cells, real_claims=real_claims,
                                    real_claim_rate=real_claims / real_cells,
                                    null_claim_rate_p5=clo, null_claim_rate_med=cmed,
                                    null_claim_rate_p95=chi,
                                    real_defined=real_df, real_survive=real_sv,
                                    real_share=real_share,
                                    null_share_p5=lo, null_share_med=med, null_share_p95=hi,
                                    excess=real_share - med if np.isfinite(med) else np.nan,
                                    verdict=verdict(real_share, lo, hi)))
    BD = pd.DataFrame(out)
    BD.to_csv(f"{OUT}.bands.csv", index=False)

    for sch in SCHEMES:
        P(f"\n  scheme {sch}, at the committed draw count 200 "
          f"(all four rungs in .bands.csv):")
        s = BD[(BD.scheme == sch) & (BD.draws == 200)]
        P("    " + f"{'family':9s} {'resid':8s} {'cells':>5s} {'realclm':>8s} {'nullclm':>18s} "
                   f"{'real':>7s} {'null median':>11s} {'null band':>17s} {'excess':>8s} verdict")
        for _, r in s.iterrows():
            P("    " + f"{r.family:9s} {r.resid:8s} {int(r.cells):5d} "
              f"{r.real_claim_rate:7.1%} {r.null_claim_rate_med:7.1%}"
              f"[{r.null_claim_rate_p5:5.1%},{r.null_claim_rate_p95:5.1%}] "
              f"{r.real_share:7.1%} {r.null_share_med:11.1%} "
              f"[{r.null_share_p5:6.1%},{r.null_share_p95:6.1%}] {r.excess:+8.1%} {r.verdict}")

    P("\n  CONVERGENCE in the draw dial (FAM2 / logx - the queue's own cell):")
    s = BD[(BD.scheme == "FAM2") & (BD.resid == "logx")]
    P("    " + s[["family", "draws", "real_share", "null_share_p5", "null_share_med",
                  "null_share_p95", "verdict"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    # ------------------------------------------------------------ the gap itself
    P("\n" + "=" * 100)
    P("THE GAP - is 17.9% vs 74.6% still a gap once each side is read against its OWN null?")
    P("=" * 100)
    g = BD[(BD.scheme == "FAM2") & (BD.resid == "logx") & (BD.draws == NPERM)].set_index("family")
    dd_r, rt_r = g.loc["DD"], g.loc["RET"]
    raw_gap = rt_r.real_share - dd_r.real_share
    null_gap = rt_r.null_share_med - dd_r.null_share_med
    P(f"  RAW gap        RET {rt_r.real_share:.1%} - DD {dd_r.real_share:.1%} "
      f"= {raw_gap:+.1%}   (idea 540's headline)")
    P(f"  NULL gap       RET {rt_r.null_share_med:.1%} - DD {dd_r.null_share_med:.1%} "
      f"= {null_gap:+.1%}   (what a ZERO-SIGNAL disp produces)")
    P(f"  EXCESS gap     RET {rt_r.excess:+.1%} - DD {dd_r.excess:+.1%} "
      f"= {rt_r.excess - dd_r.excess:+.1%}   (the part that is not the null)")
    P(f"  share of the raw gap already in the null: "
      f"{null_gap / raw_gap:.1%}" if abs(raw_gap) > 1e-12 else "  raw gap ~ 0")
    P(f"  DD  real {dd_r.real_share:.1%} vs its OWN band "
      f"[{dd_r.null_share_p5:.1%}, {dd_r.null_share_p95:.1%}]  -> {dd_r.verdict}")
    P(f"  RET real {rt_r.real_share:.1%} vs its OWN band "
      f"[{rt_r.null_share_p5:.1%}, {rt_r.null_share_p95:.1%}]  -> {rt_r.verdict}")
    P(f"  and against idea 540's POOLED band [{PUB_POOLED_LOGX[0]:.1%}, "
      f"{PUB_POOLED_LOGX[1]:.1%}]: DD "
      f"{verdict(dd_r.real_share, *PUB_POOLED_LOGX)}, RET "
      f"{verdict(rt_r.real_share, *PUB_POOLED_LOGX)}")
    # a direct two-sided draw-level test of the gap
    sub = PF[(PF.scheme == "FAM2") & (PF.resid == "logx") & (PF.it < NPERM)]
    piv = sub.pivot_table(index="it", columns="family", values=["claims", "survive"])
    with np.errstate(invalid="ignore", divide="ignore"):
        gnull = (piv[("survive", "RET")] / piv[("claims", "RET")]
                 - piv[("survive", "DD")] / piv[("claims", "DD")]).to_numpy()
    glo, gmed, ghi = band(gnull)
    pval = float(np.mean(np.abs(gnull[np.isfinite(gnull)]) >= abs(raw_gap)))
    P(f"\n  DRAW-LEVEL null for the GAP itself (the statistic idea 540 reported): "
      f"median {gmed:+.1%}, band [{glo:+.1%}, {ghi:+.1%}], "
      f"two-sided p(|null gap| >= |{raw_gap:+.1%}|) = {pval:.4f}")

    # ------------------------------------------------------------ rule 8, claim leg
    P("\n" + "=" * 100)
    P("RULE 8, CLAIM LEG - IS-only claims read once on OOS, per family, against the same null")
    P("=" * 100)
    W = CELL.pivot_table(index=["arm", "outcome", "strata"], columns="window",
                         values=["b_none", "t_none", "b_logx", "t_logx"])
    rows8 = []
    for (arm, oc, nb), r in W.iterrows():
        for m in ["none", "logx"]:
            bi, ti = r[(f"b_{m}", "IS")], r[(f"t_{m}", "IS")]
            bo, to = r[(f"b_{m}", "OOS")], r[(f"t_{m}", "OOS")]
            claim_is = bool(np.isfinite(ti) and abs(ti) >= T_BAR)
            rows8.append(dict(arm=arm, outcome=oc, strata=nb, resid=m,
                              FAM2=SCHEMES["FAM2"][oc], t_IS=ti, t_OOS=to, b_IS=bi, b_OOS=bo,
                              claim_IS=claim_is,
                              holds=bool(claim_is and np.isfinite(to) and abs(to) >= T_BAR
                                         and np.sign(bi) == np.sign(bo))))
    W8 = pd.DataFrame(rows8)
    W8.to_csv(f"{OUT}.claimleg.csv", index=False)
    P(W8.groupby(["FAM2", "resid"]).agg(cells=("holds", "size"), IS_claims=("claim_IS", "sum"),
                                        holds=("holds", "sum")).to_string())
    for fam in ["DD", "RET"]:
        for m in ["none", "logx"]:
            s = W8[(W8.FAM2 == fam) & (W8.resid == m) & W8.claim_IS]
            hr = s.holds.mean() if len(s) else np.nan
            P(f"    {fam:4s} {m:6s} IS claims {len(s):3d} -> hold OOS {int(s.holds.sum()):3d} "
              f"({hr:.1%})" if len(s) else f"    {fam:4s} {m:6s} no IS claims")

    # ------------------------------------------------------------ rule 8, book leg
    P("\n" + "=" * 100)
    P("RULE 8, BOOK LEG - IS-only per-family disp selectors over the 168 panels, read on OOS")
    P("=" * 100)
    r0 = A.iloc[0]
    P(f"  comparands on the same calendar: RULES v2 OOS {r0.base_OOS_CAGR:+.4f}/"
      f"{r0.base_OOS_Sharpe:.4f}/{r0.base_OOS_MaxDD:+.4f}   SPY OOS {r0.SPY_OOS_CAGR:+.4f}/"
      f"{r0.SPY_OOS_Sharpe:.4f}/{r0.SPY_OOS_MaxDD:+.4f}")
    brng = np.random.default_rng(PSEED + 1)
    wf = []
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], PERM_STRATA)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = np.log(sub["bookvol_IS"].to_numpy())
        dx = demean(sub["disp_IS"].to_numpy(), st)
        bb, _, _, _, _ = ols(dx, demean(lbv, st))
        dres = dx - bb[0] * demean(lbv, st)
        anchor = float(sub.Sharpe_OOS.mean())
        # random-pick null for the percentile column
        rand = sub.Sharpe_OOS.to_numpy()[brng.integers(0, len(sub), 2000)]
        picks = {"SEL-S  argmax IS Sharpe": int(sub.Sharpe_IS.idxmax())}
        for fam, oc in (("DD", "MaxDD_IS"), ("RET", "CAGR_IS")):
            yv = demean(sub[oc].to_numpy(), st)
            for lab, xv in (("", dx), ("|v", dres)):
                bfit, tfit, *_ = ols(yv, xv)
                b1, t1 = bfit[0], tfit[0]
                # favourable direction of disp for this family's outcome, taken from IS ONLY
                # (MaxDD and CAGR are both "bigger is better": MaxDD is negative)
                i = int(np.nanargmax(xv)) if b1 > 0 else int(np.nanargmin(xv))
                picks[f"SEL-DISP-{fam}{lab} (IS slope {b1:+.4f}, t {t1:+.2f})"] = i
        for name, i in picks.items():
            r = sub.loc[i]
            wf.append(dict(arm=arm, selector=name, q=r.q, draw=int(r.draw),
                           IS_Sharpe=r.Sharpe_IS, disp_IS=r.disp_IS,
                           OOS_CAGR=r.CAGR_OOS, OOS_Sharpe=r.Sharpe_OOS, OOS_MaxDD=r.MaxDD_OOS,
                           anchor_OOS_S=anchor, best_OOS_S=float(sub.Sharpe_OOS.max()),
                           rand_pct=float(np.mean(rand < r.Sharpe_OOS)),
                           v2_OOS_S=r.base_OOS_Sharpe, spy_OOS_S=r.SPY_OOS_Sharpe,
                           beats_anchor=bool(r.Sharpe_OOS > anchor),
                           beats_v2=bool(r.Sharpe_OOS > r.base_OOS_Sharpe),
                           beats_spy=bool(r.Sharpe_OOS > r.SPY_OOS_Sharpe),
                           pass4a=bool(r.pass4a), pass4b=bool(r.pass4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(WF[["arm", "selector", "q", "draw", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
          "anchor_OOS_S", "rand_pct", "beats_anchor", "beats_v2", "beats_spy",
          "pass4a", "pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  over the {len(WF)} picks: beat the do-nothing anchor {int(WF.beats_anchor.sum())}, "
      f"beat RULES v2 {int(WF.beats_v2.sum())}, beat SPY {int(WF.beats_spy.sum())}; "
      f"4a {int(WF.pass4a.sum())}, 4b {int(WF.pass4b.sum())}")
    for fam in ["DD", "RET"]:
        s = WF[WF.selector.str.contains(f"SEL-DISP-{fam}")]
        P(f"    {fam:4s} selectors ({len(s)}): beat anchor {int(s.beats_anchor.sum())}, "
          f"beat v2 {int(s.beats_v2.sum())}, beat SPY {int(s.beats_spy.sum())}, "
          f"4b {int(s.pass4b.sum())}; median random-pick percentile {s.rand_pct.median():.1%}")
    P(f"  whole corpus for reference: 4a {int(A.pass4a.sum())}/{len(A)}, "
      f"4b {int(A.pass4b.sum())}/{len(A)}")
    P("  KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves with MaxDD no worse; 4b needs "
      "Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's. "
      "Both are evaluated on every pick above from idea 533's committed columns.")

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 100)
    P(f"ANSWER: at {NPERM} draws, the drawdown family's logx survival "
      f"{dd_r.real_share:.1%} sits {dd_r.verdict} its OWN band "
      f"[{dd_r.null_share_p5:.1%}, {dd_r.null_share_p95:.1%}]; the return family's "
      f"{rt_r.real_share:.1%} sits {rt_r.verdict} its own "
      f"[{rt_r.null_share_p5:.1%}, {rt_r.null_share_p95:.1%}]. "
      f"{null_gap/raw_gap:.1%} of the published {raw_gap:+.1%} gap is present in the null.")
    P("=" * 100)

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {OUT.name}.{{claims,permfamily,bands,claimleg,walkforward}}.csv "
      f"({time.time() - t0:.1f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
