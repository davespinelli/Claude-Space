#!/usr/bin/env python3
"""Idea 717 - "is-DDnorm-s-EDGE-OF-BAND-reading-a-NORMALISATION-fact-or-a-POWER-fact"
(lane C, 2026-09-11).

The question
------------
Idea 714 (lane C, yesterday's run) cut idea 540's pooled permutation band by OUTCOME and found,
inside the drawdown family:

    MaxDD    19 claims   logx survival 10.5%   own null band [23.0%, 66.7%] med 45.5%  -> BELOW
    DDnorm    9 claims   logx survival 33.3%   own null band [33.3%, 84.6%] med 62.0%  -> INSIDE
                                                                            (on the exact edge)

and read that as "vol-normalising the drawdown kills the separation", i.e. a NORMALISATION fact.
But DDnorm carries HALF the claims, and the null band of a share over m claims widens roughly as
1/sqrt(m).  Half the claims is half the power, so the published contrast is confounded: the two
readings differ in the normaliser AND in the count, and idea 714 never separated them.

This run re-reads both outcomes at MATCHED CLAIM COUNT and reports whether the separation is a
property of the statistic or of the sample size.

What is and is not new
----------------------
Nothing is re-backtested.  The object is a within-stratum slope over idea 533's committed
`.arms.csv` (idea 295's MIX ladder: k = 40, 21 q rungs x 8 draws = 168 panels, seed 20260909,
three books per panel - EWall / top10 / top20 - gross 0.75, weekly, 10 bps, next-day execution),
and the null is idea 540's OWN within-stratum permutation (seed 540, 21 strata), re-rolled here
in the same rng consumption order so that GATE 4 reproduces its committed draws bit for bit.
GATES G0-G4 must pass before a single new number is read.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. normaliser in {MaxDD, DDnorm}                                    (the queue's dial 1)
         reported on the other three outcomes (Sharpe, CAGR, CAGRnorm) as well, always.
    2. claim count m in {4, 6, 9, 12, 15, 19, 24, 28}                   (the queue's dial 2)
         9 is DDnorm's native count, 19 is MaxDD's; every feasible cell is published and the
         infeasible ones are printed as NA rather than dropped.
    The MATCHING DEVICE is not a third tuned dial: BOTH devices are run on BOTH outcomes at
    EVERY m and both are published.  Nothing below is selected on its outcome.
         SUB  count-matched SUBSAMPLE at the inherited |t| >= 1.960 bar.  Only reaches m <= the
              outcome's native claim count, so it can take MaxDD DOWN to DDnorm's 9 but cannot
              take DDnorm UP.  The real side is simulated too (2,000 subsets), so the verdict's
              STABILITY under m claims is measured, not asserted.
         BAR  count-matched BAR: the claim bar is set to the outcome's own m-th largest |t_none|,
              so the claim count is EXACTLY m by construction, on the real grid and on every
              permutation draw separately.  This is the only device that takes DDnorm UP to
              MaxDD's 19 claims, and it prints the bar it needed.
    Residualisation (none/partial/logx/loglog), arm, stratum resolution, window and the ladder
    itself are INHERITED from ideas 295/533/540 and are reported axes, never tuned.

How the answer is decided (pre-registered, before any number below was read)
    POWER fact         if MaxDD's BELOW verdict does NOT survive being cut to m = 9, and/or
                       DDnorm's INSIDE verdict does NOT survive being taken up to m = 19, while
                       the two EXCESSES (real share - own null median) stay within each other's
                       draw-level spread at matched m.
    NORMALISATION fact if MaxDD reads BELOW and DDnorm reads INSIDE at the SAME m, with the
                       excess gap outside the matched-count null for that gap.
    The count-free comparand is the EXCESS and its standardised form z = (real - null med) /
    sd(null share at m); a power story moves the band width and leaves the excess alone.

Rule 8 walk-forward (PROTOCOL rule 8, required) - two legs, both at matched count
    CLAIM LEG  every claim is established on the IS window (<= 2016-12-31) ONLY and read once on
               the untouched OOS window, at matched claim counts via the BAR device.
    BOOK LEG   MaxDD-directed and DDnorm-directed IS-only disp selectors over the 168 panels,
               uncontrolled and with log(IS book vol) held, each read ONCE on OOS as
               CAGR / Sharpe / MaxDD against RULES v2, SPY and the do-nothing anchor, with a
               2,000-pick random null for the percentile.  BOTH KEEP PATHS (4a vs RULES v2,
               4b vs SPY) are evaluated on every pick from idea 533's committed pass4a/pass4b
               columns, and the whole 504-row corpus is quoted as the base rate.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): both ends of the q ladder are CURRENT
constituents of their screens, so every LEVEL inherited here is optimistic.  The object under
test is a within-stratum slope under a control and a selector's OOS ranking, neither of which is
a level claim.  No book here is a capital candidate.

Outputs: .cells.csv .permcells.csv .matched.csv .gap.csv .claimleg.csv .walkforward.csv
         .console.txt .result.md
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe  # noqa: E402  (PROTOCOL: the shared loader, caches only)
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
P533 = BT / "2026-09-09_why-is-evol-the-one-characteristic-that-never-reverses_C"
P540 = BT / "2026-09-11_is-disp-the-SECOND-vol-channel_cloud"
P714 = BT / "2026-09-11_does-the-DRAWDOWN-vs-RETURN-survival-gap-hold-against-a-PER-FAMILY-null_C"

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

OUTCOMES = ["Sharpe", "CAGR", "MaxDD"]
NORM_OUTCOMES = ["DDnorm", "CAGRnorm"]
ALL_OUT = OUTCOMES + NORM_OUTCOMES
FOCAL = ["MaxDD", "DDnorm"]                        # tuned param 1
ARMS = ["EWall", "top10", "top20"]
WINDOWS = ["full", "IS", "OOS"]
RESIDS = ["none", "partial", "logx", "loglog"]
CTRLS = ["partial", "logx", "loglog"]
STRATA = [3, 5, 7, 21]
T_BAR = 1.960
NPERM, PSEED = 400, 540
PERM_STRATA = 21
M_GRID = [4, 6, 9, 12, 15, 19, 24, 28]             # tuned param 2
NSUB = 2000                                        # subsample replicates (real side, device SUB)
WARMUP, IS_END = 260, pd.Timestamp("2016-12-31")

# what idea 714 published for the two focal outcomes, re-derived not believed
PUB714 = {"MaxDD": dict(claims=19, share=2/19, band=(0.230, 0.667), med=0.455, verdict="BELOW"),
          "DDnorm": dict(claims=9, share=3/9, band=(0.333, 0.846), med=0.620, verdict="INSIDE")}
PUB_POOLED_LOGX = (0.568, 0.823)
PUB_CLAIMRATE = 0.3597
PUB_4A, PUB_4B, PUB_N = 0, 41, 504
PUB_SPY_OOS = (0.1545, 0.8820, -0.3372)            # idea 533's committed SPY OOS row


# ----------------------------------------------------- idea 533/540's fitters, copied verbatim
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
    """The 180 disp cells x len(resids) - same iteration order as ideas 540/714."""
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


# --------------------------------------------------------------------------------------------
# Same arithmetic, 400 draws instead of 1: every quantity that does NOT depend on disp (the
# de-meaned y, log|y|, book vol and its log, per stratum resolution) is identical on every
# permutation draw, so it is computed ONCE.  The call sequence into `ols` and the iteration
# order over cells are unchanged, so this is the same function as `grid_arrays` - GATES 1, 2
# and 4 below hold it to that, bit for bit, against three committed artefacts.
# --------------------------------------------------------------------------------------------
def build_cache(A):
    C = {}
    for win in WINDOWS:
        for arm in ARMS:
            sub = A[A.arm == arm]
            bv_raw = sub[f"bookvol_{win}"].to_numpy()
            with np.errstate(invalid="ignore", divide="ignore"):
                lbv = np.log(np.where(bv_raw > 0, bv_raw, np.nan))
            for nb in STRATA:
                st = bin_q(sub["q"], nb)
                C[("bv", win, arm, nb)] = (zs(demean(bv_raw, st)), demean(lbv, st), st)
            for oc in ALL_OUT:
                y_raw = sub[f"{oc}_{win}"].to_numpy()
                fin = np.isfinite(y_raw)
                loggable = bool(fin.any() and (np.all(y_raw[fin] > 0) or np.all(y_raw[fin] < 0)))
                for nb in STRATA:
                    st = C[("bv", win, arm, nb)][2]
                    ly = None
                    if loggable:
                        with np.errstate(invalid="ignore", divide="ignore"):
                            ly = demean(np.log(np.abs(y_raw)), st)
                    C[("y", win, arm, oc, nb)] = (demean(y_raw, st), ly)
    return C


def grid_fast(A, C, resids, x_src):
    """x_src: (win, arm) -> the disp column to use (real or permuted)."""
    B = {m: [] for m in resids}; T = {m: [] for m in resids}
    for win in WINDOWS:
        for arm in ARMS:
            x_raw = x_src(win, arm)
            with np.errstate(invalid="ignore", divide="ignore"):
                lx = np.log(np.where(np.asarray(x_raw, float) > 0, x_raw, np.nan))
            xp = {}
            for nb in STRATA:
                st = C[("bv", win, arm, nb)][2]
                xp[nb] = (zs(demean(x_raw, st)), demean(lx, st))
            for oc in ALL_OUT:
                for nb in STRATA:
                    zbv, lbv_dm, _ = C[("bv", win, arm, nb)]
                    y_dm, ly_dm = C[("y", win, arm, oc, nb)]
                    zx, lx_dm = xp[nb]
                    for meth in resids:
                        if meth == "none":
                            b, t, *_ = ols(y_dm, zx)
                            B[meth].append(b[0]); T[meth].append(t[0])
                        elif meth == "partial":
                            b, t, *_ = ols(y_dm, np.column_stack([zx, zbv]))
                            B[meth].append(b[0]); T[meth].append(t[0])
                        elif meth == "logx":
                            b, t, *_ = ols(y_dm, np.column_stack([lx_dm, lbv_dm]))
                            B[meth].append(b[0]); T[meth].append(t[0])
                        else:
                            if ly_dm is None:
                                B[meth].append(np.nan); T[meth].append(np.nan)
                            else:
                                b, t, *_ = ols(ly_dm, np.column_stack([lx_dm, lbv_dm]))
                                B[meth].append(b[0]); T[meth].append(t[0])
    return {m: np.asarray(v, float) for m, v in B.items()}, \
           {m: np.asarray(v, float) for m, v in T.items()}


def surv_at(bn, tn, bc, tc, bar):
    """540's survival rule at an arbitrary bar: still |t| >= bar under the control AND same sign."""
    sig = np.isfinite(tn) & (np.abs(tn) >= bar)
    ok = np.isfinite(tc) & (np.abs(tc) >= bar) & (np.sign(bc) == np.sign(bn))
    return sig, sig & ok


def band(v):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if not len(v): return (np.nan, np.nan, np.nan)
    return float(np.quantile(v, 0.05)), float(np.median(v)), float(np.quantile(v, 0.95))


def verdict(real, lo, hi):
    if not np.isfinite(real) or not np.isfinite(lo): return "NA"
    return "ABOVE" if real > hi else ("BELOW" if real < lo else "INSIDE")


def topm(absT, m):
    """Indices of the m largest finite |t|, and the bar that produces exactly m claims."""
    a = np.where(np.isfinite(absT), absT, -np.inf)
    if m > np.isfinite(absT).sum(): return None, np.nan
    order = np.argsort(-a, kind="stable")[:m]
    return order, float(a[order[-1]])


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 717 - is-DDnorm-s-EDGE-OF-BAND-reading-a-NORMALISATION-fact-or-a-POWER-fact")
    P("           (lane C, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  tuned 1 normaliser {FOCAL} (other three outcomes always reported)")
    P(f"  tuned 2 claim count m {M_GRID}  (9 = DDnorm's native, 19 = MaxDD's native)")
    P("  devices SUB (subsample at the inherited 1.960 bar) and BAR (bar set to the m-th largest")
    P("  |t_none|, exactly m claims by construction) are BOTH run on BOTH outcomes at EVERY m")
    P(f"  null = idea 540's own within-stratum permutation, seed {PSEED}, {PERM_STRATA} strata, "
      f"{NPERM} draws")
    P("  decision rule: POWER if MaxDD's BELOW dies at m=9 and/or DDnorm's INSIDE dies at m=19")
    P("  while the two EXCESSES overlap at matched m; NORMALISATION if the verdicts separate at")
    P("  the SAME m with the excess gap outside its own matched-count null.")

    # ------------------------------------------------------------ inputs
    A = pd.read_csv(f"{P533}.arms.csv")
    for win in WINDOWS:
        A[f"DDnorm_{win}"] = A[f"MaxDD_{win}"] / A[f"bookvol_{win}"]
        A[f"CAGRnorm_{win}"] = A[f"CAGR_{win}"] / A[f"bookvol_{win}"]
    G533 = pd.read_csv(f"{P533}.grid.csv")
    CL540 = pd.read_csv(f"{P540}.claims.csv")
    PM540 = pd.read_csv(f"{P540}.permutation.csv")
    BD714 = pd.read_csv(f"{P714}.bands.csv")
    P("\nSOURCES (committed, not re-run):")
    P(f"  {P533.name}.arms.csv  {A.shape}    grid.csv {G533.shape}")
    P(f"  {P540.name}.claims.csv {CL540.shape}   permutation.csv {PM540.shape}")
    P(f"  {P714.name}.bands.csv {BD714.shape}")

    # ------------------------------------------------------------ GATE 0 (uses baseline.py)
    P("\n--- GATE 0: idea 533's SPY comparand re-derives from research/baseline.py caches ---")
    pxs = load_universe(small=True)
    SPY_RAW = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    idx = pxs.index
    spy = SPY_RAW.reindex(idx, method="ffill").pct_change().fillna(0).loc[idx[WARMUP]:]
    m_oos = metrics(spy.loc[IS_END + pd.Timedelta(days=1):])
    got = (m_oos["CAGR"], m_oos["Sharpe"], m_oos["MaxDD"])
    P(f"  common window {idx[0].date()} .. {idx[-1].date()} ({len(idx)} rows), warm-up {WARMUP}")
    P(f"  SPY OOS re-derived  CAGR {got[0]:+.4f}  Sharpe {got[1]:.4f}  MaxDD {got[2]:+.4f}")
    P(f"  committed in arms.csv  CAGR {A.SPY_OOS_CAGR.iloc[0]:+.4f}  "
      f"Sharpe {A.SPY_OOS_Sharpe.iloc[0]:.4f}  MaxDD {A.SPY_OOS_MaxDD.iloc[0]:+.4f}   "
      f"(unique rows {A[['SPY_OOS_CAGR','SPY_OOS_Sharpe','SPY_OOS_MaxDD']].drop_duplicates().shape[0]})")
    d0 = max(abs(got[i] - v) for i, v in enumerate(
        (A.SPY_OOS_CAGR.iloc[0], A.SPY_OOS_Sharpe.iloc[0], A.SPY_OOS_MaxDD.iloc[0])))
    P(f"  max |d| {d0:.3e}")
    assert d0 < 1e-6, "GATE 0 FAILED - the committed SPY comparand is not this calendar's SPY"
    P("  GATE 0 PASS")

    # ------------------------------------------------------------ the real grid
    CACHE = build_cache(A)
    cells = [(win, arm, oc, nb) for win in WINDOWS for arm in ARMS
             for oc in ALL_OUT for nb in STRATA]
    B, T = grid_fast(A, CACHE, RESIDS,
                     lambda w, a: A[A.arm == a][f"disp_{w}"].to_numpy())
    # the cached path must equal the literal one on the real grid before it is trusted on 400 draws
    _c0, _B0, _T0 = grid_arrays(A, RESIDS)
    _d = max(float(np.nanmax(np.abs(_B0[m] - B[m]))) for m in RESIDS)
    _dt = max(float(np.nanmax(np.abs(_T0[m] - T[m]))) for m in RESIDS)
    assert _c0 == cells and _d == 0.0 and _dt == 0.0, "fast path diverges from the literal fitter"
    CELL = pd.DataFrame(cells, columns=["window", "arm", "outcome", "strata"])
    for m in RESIDS:
        CELL[f"b_{m}"] = B[m]; CELL[f"t_{m}"] = T[m]
    sig0, sv_logx = surv_at(B["none"], T["none"], B["logx"], T["logx"], T_BAR)
    CELL["is_claim"] = sig0; CELL["survive_logx"] = sv_logx
    for m in ["partial", "loglog"]:
        _, s_ = surv_at(B["none"], T["none"], B[m], T[m], T_BAR)
        CELL[f"survive_{m}"] = s_
    CELL.to_csv(f"{OUT}.cells.csv", index=False)

    # ------------------------------------------------------------ GATE 1
    P("\n--- GATE 1: idea 533's committed disp grid re-derives from its own arms.csv ---")
    ref = G533[(G533["char"] == "disp") & (G533.resid.isin(["none", "partial"]))]
    mine = CELL.melt(id_vars=["window", "arm", "outcome", "strata"],
                     value_vars=[f"b_{m}" for m in ["none", "partial"]],
                     var_name="resid", value_name="b")
    mine["resid"] = mine.resid.str.replace("b_", "", regex=False)
    J = ref.merge(mine, on=["window", "arm", "outcome", "strata", "resid"], suffixes=("_r", "_n"))
    d1 = float(np.nanmax(np.abs(J.b_r - J.b_n)))
    P(f"  joined {len(J)} of {len(ref)} committed disp rows; max |db| {d1:.3e}")
    assert len(J) == len(ref) and d1 < 1e-9, "GATE 1 FAILED"
    P(f"  KEEP counts on the 504 arm-rows: 4a {int(A.pass4a.sum())}/{len(A)} (pub {PUB_4A}), "
      f"4b {int(A.pass4b.sum())}/{len(A)} (pub {PUB_4B})")
    assert int(A.pass4a.sum()) == PUB_4A and int(A.pass4b.sum()) == PUB_4B, "GATE 1 FAILED (KEEP)"
    P("  GATE 1 PASS (bar 1e-9)")

    # ------------------------------------------------------------ GATE 2
    P("\n--- GATE 2: idea 540's committed 180-row claims table re-derives cell for cell ---")
    k = ["window", "arm", "outcome", "strata"]
    J2 = CL540.merge(CELL, on=k, suffixes=("_ref", "_new"))
    dmax = max(float(np.nanmax(np.abs(J2[f"{c}_ref"] - J2[f"{c}_new"])))
               for c in ["t_partial", "b_partial", "t_logx", "b_logx"])
    same = int((J2.is_claim_ref.astype(bool) == J2.is_claim_new.astype(bool)).sum())
    samesv = int((J2.survive_logx_ref.astype(bool) == J2.survive_logx_new.astype(bool)).sum())
    P(f"  joined {len(J2)}/180; max |d| {dmax:.3e}; is_claim agree {same}/180; "
      f"survive_logx agree {samesv}/180")
    assert len(J2) == 180 and dmax < 1e-9 and same == 180 and samesv == 180, "GATE 2 FAILED"
    P("  GATE 2 PASS")

    # ------------------------------------------------------------ GATE 3: idea 714's own two rows
    P("\n--- GATE 3: idea 714's published MaxDD / DDnorm rows re-derive, not believed ---")
    oc_arr = CELL.outcome.to_numpy()
    for oc, pub in PUB714.items():
        m_ = oc_arr == oc
        c_ = int((sig0 & m_).sum()); s_ = int((sv_logx & m_).sum())
        P(f"  {oc:8s} claims {c_:2d}/{int(m_.sum())} (pub {pub['claims']})   "
          f"logx survival {s_}/{c_} = {s_/c_:.1%} (pub {pub['share']:.1%})   "
          f"idea 714 verdict {pub['verdict']} vs own band "
          f"[{pub['band'][0]:.1%}, {pub['band'][1]:.1%}]")
        assert c_ == pub["claims"] and abs(s_ / c_ - pub["share"]) < 1e-9, f"GATE 3 FAILED {oc}"
    ref714 = BD714[(BD714.scheme == "FAM5") & (BD714.resid == "logx") & (BD714.draws == 400)]
    P("  idea 714's committed FAM5/logx/400 rows (the object this run re-reads):")
    P("    " + ref714[["family", "real_claims", "real_share", "null_share_p5", "null_share_med",
                       "null_share_p95", "verdict"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    P("  GATE 3 PASS")

    # ------------------------------------------------------------ the null
    P("\n" + "=" * 100)
    P(f"THE NULL - disp permuted WITHIN stratum ({PERM_STRATA} strata), {NPERM} draws, seed {PSEED}")
    P("=" * 100)
    rng = np.random.default_rng(PSEED)
    pB = {m: np.full((NPERM, len(CELL)), np.nan) for m in RESIDS}
    pT = {m: np.full((NPERM, len(CELL)), np.nan) for m in RESIDS}
    pooled = []
    for it in range(NPERM):
        xo = {}
        for win in WINDOWS:
            for arm in ARMS:
                sub = A[A.arm == arm]
                st = bin_q(sub["q"], PERM_STRATA)
                v = sub[f"disp_{win}"].to_numpy().copy()
                for s_ in np.unique(st):
                    msk = st == s_
                    v[msk] = rng.permutation(v[msk])
                xo[(win, arm)] = v
        bb, tt = grid_fast(A, CACHE, RESIDS, lambda w, a: xo[(w, a)])
        for m in RESIDS:
            pB[m][it] = bb[m]; pT[m][it] = tt[m]
        cl, _ = surv_at(bb["none"], tt["none"], bb["none"], tt["none"], T_BAR)
        row = dict(it=it, claims=int(cl.sum()))
        for m in CTRLS:
            _, s_ = surv_at(bb["none"], tt["none"], bb[m], tt[m], T_BAR)
            row[f"survive_{m}"] = int(s_.sum())
        pooled.append(row)
    PMnew = pd.DataFrame(pooled)

    # ------------------------------------------------------------ GATE 4
    P("\n--- GATE 4: the first 200 draws reproduce idea 540's committed permutation.csv ---")
    head = PMnew.head(len(PM540))
    d4 = {c: int(np.abs(head[c].to_numpy() - PM540[c].to_numpy()).max())
          for c in ["claims", "survive_logx", "survive_loglog", "survive_partial"]}
    P(f"  draws compared {len(head)}; max |d| " + ", ".join(f"{c} {v}" for c, v in d4.items()))
    assert max(d4.values()) == 0, "GATE 4 FAILED - the null is not idea 540's null"
    rate = PMnew.head(200).claims.mean() / len(CELL)
    sh = PMnew.head(200).survive_logx / PMnew.head(200).claims
    P(f"  pooled permuted claim rate over 200 draws {rate:.4%} (pub {PUB_CLAIMRATE:.2%}); "
      f"pooled logx band [{sh.quantile(0.05):.1%}, {sh.quantile(0.95):.1%}] "
      f"(pub [{PUB_POOLED_LOGX[0]:.1%}, {PUB_POOLED_LOGX[1]:.1%}])")
    assert abs(rate - PUB_CLAIMRATE) < 5e-4, "GATE 4 FAILED - claim rate"
    assert abs(sh.quantile(0.05) - PUB_POOLED_LOGX[0]) < 5e-3, "GATE 4 FAILED - pooled band"
    P("  GATE 4 PASS - every band below is a re-reading of these exact draws")

    # ------------------------------------------------------------ per-outcome per-draw cache
    pc = []
    for oc in ALL_OUT:
        m_ = oc_arr == oc
        pc.append(pd.DataFrame(dict(
            outcome=oc, it=np.arange(NPERM),
            claims=[int(np.sum(np.isfinite(pT["none"][i][m_])
                               & (np.abs(pT["none"][i][m_]) >= T_BAR))) for i in range(NPERM)])))
    pd.concat(pc).to_csv(f"{OUT}.permcells.csv", index=False)

    # ------------------------------------------------------------ THE MATCHED-COUNT GRID
    P("\n" + "=" * 100)
    P("MATCHED CLAIM COUNT - every (outcome, device, m) cell, nothing dropped")
    P("=" * 100)
    srng = np.random.default_rng(PSEED + 717)
    rows = []
    for oc in ALL_OUT:
        m_ = oc_arr == oc
        ncell = int(m_.sum())
        rn, rt = B["none"][m_], T["none"][m_]
        rc, rct = B["logx"][m_], T["logx"][m_]
        absr = np.abs(rt)
        nat_cl = int(np.sum(np.isfinite(rt) & (absr >= T_BAR)))
        nat_idx = np.where(np.isfinite(rt) & (absr >= T_BAR))[0]
        nat_sv = np.array([bool(np.isfinite(rct[i]) and abs(rct[i]) >= T_BAR
                                and np.sign(rc[i]) == np.sign(rn[i])) for i in nat_idx])
        for M in M_GRID:
            # ---------------- device SUB (native bar, subsample down only)
            if M <= nat_cl:
                real_full = float(nat_sv.mean())
                sub_sh = np.array([nat_sv[srng.choice(nat_cl, M, replace=False)].mean()
                                   for _ in range(NSUB)])
                nsh, used = [], 0
                for i in range(NPERM):
                    tn, tc = pT["none"][i][m_], pT["logx"][i][m_]
                    bn, bc = pB["none"][i][m_], pB["logx"][i][m_]
                    ci = np.where(np.isfinite(tn) & (np.abs(tn) >= T_BAR))[0]
                    if len(ci) < M: continue
                    pick = srng.choice(len(ci), M, replace=False)
                    sel = ci[pick]
                    sv = (np.isfinite(tc[sel]) & (np.abs(tc[sel]) >= T_BAR)
                          & (np.sign(bc[sel]) == np.sign(bn[sel])))
                    nsh.append(sv.mean()); used += 1
                lo, med, hi = band(np.array(nsh))
                sd = float(np.std(nsh)) if used else np.nan
                rows.append(dict(outcome=oc, device="SUB", m=M, cells=ncell,
                                 native_claims=nat_cl, bar=T_BAR, real_share=real_full,
                                 real_sub_p5=float(np.quantile(sub_sh, 0.05)),
                                 real_sub_med=float(np.median(sub_sh)),
                                 real_sub_p95=float(np.quantile(sub_sh, 0.95)),
                                 null_p5=lo, null_med=med, null_p95=hi, null_sd=sd,
                                 draws_used=used, excess=real_full - med,
                                 z=(real_full - med) / sd if sd and np.isfinite(sd) else np.nan,
                                 p_left=float(np.mean(np.array(nsh) <= real_full)) if used else np.nan,
                                 verdict=verdict(real_full, lo, hi),
                                 stable_below=float(np.mean(sub_sh < lo)) if used else np.nan))
            else:
                rows.append(dict(outcome=oc, device="SUB", m=M, cells=ncell,
                                 native_claims=nat_cl, bar=np.nan, real_share=np.nan,
                                 verdict="NA (m > native claims)"))
            # ---------------- device BAR (bar set to the m-th largest |t|, exactly m claims)
            ridx, rbar = topm(absr, M)
            if ridx is None:
                rows.append(dict(outcome=oc, device="BAR", m=M, cells=ncell,
                                 native_claims=nat_cl, verdict="NA (m > cells)"))
                continue
            rsv = np.array([bool(np.isfinite(rct[i]) and abs(rct[i]) >= rbar
                                 and np.sign(rc[i]) == np.sign(rn[i])) for i in ridx])
            real_share = float(rsv.mean())
            nsh = []
            for i in range(NPERM):
                tn, tc = pT["none"][i][m_], pT["logx"][i][m_]
                bn, bc = pB["none"][i][m_], pB["logx"][i][m_]
                idx_, bar_ = topm(np.abs(tn), M)
                if idx_ is None: continue
                sv = (np.isfinite(tc[idx_]) & (np.abs(tc[idx_]) >= bar_)
                      & (np.sign(bc[idx_]) == np.sign(bn[idx_])))
                nsh.append(sv.mean())
            lo, med, hi = band(np.array(nsh))
            sd = float(np.std(nsh))
            rows.append(dict(outcome=oc, device="BAR", m=M, cells=ncell, native_claims=nat_cl,
                             bar=rbar, real_share=real_share,
                             real_sub_p5=np.nan, real_sub_med=np.nan, real_sub_p95=np.nan,
                             null_p5=lo, null_med=med, null_p95=hi, null_sd=sd,
                             draws_used=len(nsh), excess=real_share - med,
                             z=(real_share - med) / sd if sd else np.nan,
                             p_left=float(np.mean(np.array(nsh) <= real_share)),
                             verdict=verdict(real_share, lo, hi), stable_below=np.nan))
    MT = pd.DataFrame(rows)
    MT.to_csv(f"{OUT}.matched.csv", index=False)

    for dev in ["SUB", "BAR"]:
        P(f"\n  device {dev} - the two focal outcomes at every m "
          f"(all five outcomes in .matched.csv):")
        P("    " + f"{'outcome':8s} {'m':>3s} {'bar':>6s} {'real':>7s} {'null med':>9s} "
                   f"{'null band':>17s} {'excess':>8s} {'z':>7s} {'p_left':>7s} "
                   f"{'draws':>6s} {'stable':>7s}  verdict")
        for oc in FOCAL:
            for _, r in MT[(MT.outcome == oc) & (MT.device == dev)].iterrows():
                if not np.isfinite(r.get("real_share", np.nan)):
                    P("    " + f"{oc:8s} {int(r.m):3d} {'-':>6s} {'-':>7s} {'-':>9s} "
                               f"{'-':>17s} {'-':>8s} {'-':>7s} {'-':>7s} {'-':>6s} "
                               f"{'-':>7s}  {r.verdict}")
                    continue
                st = f"{r.stable_below:6.1%}" if np.isfinite(r.get("stable_below", np.nan)) else "     -"
                P("    " + f"{oc:8s} {int(r.m):3d} {r.bar:6.3f} {r.real_share:7.1%} "
                  f"{r.null_med:9.1%} [{r.null_p5:6.1%},{r.null_p95:6.1%}] {r.excess:+8.1%} "
                  f"{r.z:+7.2f} {r.p_left:7.3f} {int(r.draws_used):6d} {st}  {r.verdict}")
        if dev == "SUB":
            P("    NOTE: device SUB drops null draws with fewer than m claims, so a low `draws`")
            P("    count means the band is conditioned on high-claim draws and reads OPTIMISTIC")
            P("    for the null.  Device BAR has no such conditioning (draws = 400 everywhere).")

    # ------------------------------------------------------------ the answer
    P("\n" + "=" * 100)
    P("THE ANSWER - is the MaxDD / DDnorm split a NORMALISATION fact or a POWER fact?")
    P("=" * 100)
    gap_rows = []
    for dev in ["SUB", "BAR"]:
        for M in M_GRID:
            a_ = MT[(MT.outcome == "MaxDD") & (MT.device == dev) & (MT.m == M)]
            b_ = MT[(MT.outcome == "DDnorm") & (MT.device == dev) & (MT.m == M)]
            if not len(a_) or not len(b_): continue
            a_, b_ = a_.iloc[0], b_.iloc[0]
            if not (np.isfinite(a_.get("real_share", np.nan))
                    and np.isfinite(b_.get("real_share", np.nan))):
                continue
            gap_rows.append(dict(device=dev, m=M, MaxDD_share=a_.real_share,
                                 DDnorm_share=b_.real_share,
                                 MaxDD_verdict=a_.verdict, DDnorm_verdict=b_.verdict,
                                 MaxDD_excess=a_.excess, DDnorm_excess=b_.excess,
                                 excess_gap=a_.excess - b_.excess,
                                 MaxDD_z=a_.z, DDnorm_z=b_.z,
                                 MaxDD_null_width=a_.null_p95 - a_.null_p5,
                                 DDnorm_null_width=b_.null_p95 - b_.null_p5,
                                 separate=bool(a_.verdict == "BELOW" and b_.verdict != "BELOW")))
    GP = pd.DataFrame(gap_rows)
    GP.to_csv(f"{OUT}.gap.csv", index=False)
    P("\n  MATCHED-m comparison (the whole question on one table):")
    P("    " + GP.to_string(index=False, float_format=lambda x: f"{x:.4f}")
      .replace("\n", "\n    "))

    def cell(oc, dev, M):
        s = MT[(MT.outcome == oc) & (MT.device == dev) & (MT.m == M)]
        return s.iloc[0] if len(s) and np.isfinite(s.iloc[0].get("real_share", np.nan)) else None

    P("\n  the four decision cells:")
    for lab, oc, dev, M in (("MaxDD native 19", "MaxDD", "SUB", 19),
                            ("MaxDD cut to  9", "MaxDD", "SUB", 9),
                            ("DDnorm native 9", "DDnorm", "BAR", 9),
                            ("DDnorm up to 19", "DDnorm", "BAR", 19)):
        r = cell(oc, dev, M)
        if r is None:
            P(f"    {lab}: NA"); continue
        P(f"    {lab} ({dev}): real {r.real_share:.1%} vs own band "
          f"[{r.null_p5:.1%}, {r.null_p95:.1%}] med {r.null_med:.1%} -> {r.verdict}   "
          f"excess {r.excess:+.1%}, z {r.z:+.2f}, p_left {r.p_left:.3f}"
          + (f", verdict stability under m={M} claims {r.stable_below:.1%} BELOW"
             if np.isfinite(r.get("stable_below", np.nan)) else ""))

    m9 = GP[(GP.m == 9)]
    P("\n  at MATCHED m = 9 the excess gap is "
      + ", ".join(f"{r.device} {r.excess_gap:+.1%}" for _, r in m9.iterrows())
      + f"; the native-count gap idea 714 published is "
        f"{PUB714['MaxDD']['share'] - PUB714['MaxDD']['med']:+.1%} - "
        f"{PUB714['DDnorm']['share'] - PUB714['DDnorm']['med']:+.1%} = "
        f"{(PUB714['MaxDD']['share'] - PUB714['MaxDD']['med']) - (PUB714['DDnorm']['share'] - PUB714['DDnorm']['med']):+.1%}")

    # ------------------------------------------------------------ rule 8, claim leg
    P("\n" + "=" * 100)
    P("RULE 8, CLAIM LEG - IS-only claims read once on OOS, at matched count (device BAR)")
    P("=" * 100)
    W = CELL.pivot_table(index=["arm", "outcome", "strata"], columns="window",
                         values=["b_none", "t_none", "b_logx", "t_logx"])
    rows8 = []
    for (arm, oc, nb), r in W.iterrows():
        for meth in ["none", "logx"]:
            rows8.append(dict(arm=arm, outcome=oc, strata=nb, resid=meth,
                              b_IS=r[(f"b_{meth}", "IS")], t_IS=r[(f"t_{meth}", "IS")],
                              b_OOS=r[(f"b_{meth}", "OOS")], t_OOS=r[(f"t_{meth}", "OOS")]))
    W8 = pd.DataFrame(rows8)
    W8["claim_IS"] = np.isfinite(W8.t_IS) & (W8.t_IS.abs() >= T_BAR)
    W8["holds"] = (W8.claim_IS & np.isfinite(W8.t_OOS) & (W8.t_OOS.abs() >= T_BAR)
                   & (np.sign(W8.b_IS) == np.sign(W8.b_OOS)))
    W8.to_csv(f"{OUT}.claimleg.csv", index=False)
    P("  native bar 1.960:")
    for oc in FOCAL:
        for meth in ["none", "logx"]:
            s = W8[(W8.outcome == oc) & (W8.resid == meth)]
            c = s[s.claim_IS]
            P(f"    {oc:8s} {meth:5s} cells {len(s):2d}  IS claims {len(c):2d}  "
              f"hold OOS {int(c.holds.sum()):2d}"
              + (f" ({c.holds.mean():.1%})" if len(c) else ""))
    P("  matched count (top-m by |t_IS|, same rule on both outcomes):")
    P("    " + f"{'outcome':8s} {'resid':6s} {'m':>3s} {'bar_IS':>7s} {'hold':>5s} {'rate':>7s}")
    cl8 = []
    for oc in ALL_OUT:
        for meth in ["none", "logx"]:
            s = W8[(W8.outcome == oc) & (W8.resid == meth)].reset_index(drop=True)
            av = np.abs(s.t_IS.to_numpy())
            for M in [2, 3, 4, 6, 8, 12]:
                idx_, bar_ = topm(av, M)
                if idx_ is None: continue
                h = ((np.abs(s.t_OOS.to_numpy()[idx_]) >= bar_)
                     & (np.sign(s.b_IS.to_numpy()[idx_]) == np.sign(s.b_OOS.to_numpy()[idx_])))
                cl8.append(dict(outcome=oc, resid=meth, m=M, bar_IS=bar_,
                                holds=int(h.sum()), rate=float(h.mean())))
                if oc in FOCAL:
                    P("    " + f"{oc:8s} {meth:6s} {M:3d} {bar_:7.3f} {int(h.sum()):5d} "
                      f"{h.mean():7.1%}")
    pd.DataFrame(cl8).to_csv(f"{OUT}.claimleg_matched.csv", index=False)

    # ------------------------------------------------------------ rule 8, book leg
    P("\n" + "=" * 100)
    P("RULE 8, BOOK LEG - IS-only MaxDD- and DDnorm-directed disp selectors, read once on OOS")
    P("=" * 100)
    r0 = A.iloc[0]
    P(f"  comparands on the same calendar: RULES v2 OOS {r0.base_OOS_CAGR:+.4f}/"
      f"{r0.base_OOS_Sharpe:.4f}/{r0.base_OOS_MaxDD:+.4f}   SPY OOS {r0.SPY_OOS_CAGR:+.4f}/"
      f"{r0.SPY_OOS_Sharpe:.4f}/{r0.SPY_OOS_MaxDD:+.4f}  (GATE 0 re-derived SPY from baseline.py)")
    brng = np.random.default_rng(PSEED + 1)
    wf = []
    for arm in ARMS:
        sub = A[A.arm == arm].reset_index(drop=True)
        st = bin_q(sub["q"], PERM_STRATA)
        with np.errstate(invalid="ignore", divide="ignore"):
            lbv = demean(np.log(sub["bookvol_IS"].to_numpy()), st)
        dx = demean(sub["disp_IS"].to_numpy(), st)
        bb, _, _, _, _ = ols(dx, lbv)
        dres = dx - bb[0] * lbv
        anchor = float(sub.Sharpe_OOS.mean())
        rand = sub.Sharpe_OOS.to_numpy()[brng.integers(0, len(sub), 2000)]
        picks = {"SEL-S argmax IS Sharpe": int(sub.Sharpe_IS.idxmax())}
        for oc in FOCAL:
            yv = demean(sub[f"{oc}_IS"].to_numpy(), st)
            for lab, xv in (("", dx), ("|v", dres)):
                bfit, tfit, *_ = ols(yv, xv)
                b1, t1 = bfit[0], tfit[0]
                # both MaxDD and DDnorm are "bigger is better" (both negative)
                i = int(np.nanargmax(xv)) if b1 > 0 else int(np.nanargmin(xv))
                picks[f"SEL-DISP-{oc}{lab} (IS slope {b1:+.4f}, t {t1:+.2f})"] = i
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
    for oc in FOCAL:
        s = WF[WF.selector.str.contains(f"SEL-DISP-{oc}")]
        P(f"    {oc:8s} selectors ({len(s)}): beat anchor {int(s.beats_anchor.sum())}, "
          f"beat v2 {int(s.beats_v2.sum())}, beat SPY {int(s.beats_spy.sum())}, "
          f"4a {int(s.pass4a.sum())}, 4b {int(s.pass4b.sum())}; "
          f"OOS Sharpe {s.OOS_Sharpe.min():.4f}..{s.OOS_Sharpe.max():.4f}; "
          f"median random-pick percentile {s.rand_pct.median():.1%}")
    same_pick = WF[WF.selector.str.contains("SEL-DISP-MaxDD")].reset_index(drop=True)
    other = WF[WF.selector.str.contains("SEL-DISP-DDnorm")].reset_index(drop=True)
    agree = int((same_pick[["q", "draw"]].to_numpy() == other[["q", "draw"]].to_numpy())
                .all(axis=1).sum())
    P(f"    the normaliser changes the PANEL PICK in {len(same_pick) - agree} of "
      f"{len(same_pick)} (arm x control) cells")
    P(f"  whole corpus for reference: 4a {int(A.pass4a.sum())}/{len(A)}, "
      f"4b {int(A.pass4b.sum())}/{len(A)}")
    P("  KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves with MaxDD no worse; 4b needs "
      "Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's. Both "
      "are evaluated on every pick above from idea 533's committed columns.")

    P("\n" + "=" * 100)
    P(f"done in {time.time() - t0:.1f}s")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.{{cells,permcells,matched,gap,claimleg,claimleg_matched,"
          f"walkforward}}.csv")


if __name__ == "__main__":
    main()
