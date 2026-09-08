#!/usr/bin/env python3
"""Idea 445 — make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN  (cloud lane, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 229 shows the record's 'an IS chooser loses to doing nothing' sentence is not
    supported: pooled over 104 instances the margin is -0.0015 with CI [-0.013, +0.014],
    because margin = ROOM - REGRET and ROOM is a verdict on the INCUMBENT, not on the
    selector.  Only REGRET (0.0387 [0.021, 0.058] live; 0.030-0.055 on the record's own
    published regret columns) is attributable to selection.  Draft the PROTOCOL clause
    requiring ROOM and REGRET to be published separately on any selection result, and
    back-fill both over the 32 instances that already publish a regret column plus every
    instance whose ladder is reconstructable.

WHAT THIS RUN DOES
    A. THE `32` AUDIT.  Every committed `*.walkforward.csv` is scanned for a published regret
       column (a literal `regret`, or a best-in-pool column from which regret is derivable).
       The queue's count is checked, not assumed, and reported per file.
    B. BACK-FILL.  For every admitted SHAPE-W instance (idea 229's census, imported) whose arm
       ladder can be rebuilt from the committed `<stem>.grid.csv`, this run computes, per cell,

            REGRET = OOS_best(ladder) - OOS_pick        >= 0 when the ladder contains the pick
            ROOM   = OOS_best(ladder) - OOS_control
            MARGIN = OOS_pick - OOS_control  ==  ROOM - REGRET      (identity, checked to 1e-12)

       Every file is admitted or rejected WITH ITS REASON, and a reproduction certificate (is
       the selected arm's own published OOS Sharpe actually in the recovered ladder?) is
       published per file; results are reported at three certificate thresholds.
    C. THE ATTRIBUTION.  How much of the record's published margin is ROOM (a verdict on the
       incumbent) and how much is REGRET (the only term selection controls)?  Reported
       cell- and instance-weighted with bootstraps blocked on the instance, plus the share of
       instances that are ROOM-dominated.
    D. THE INVARIANCE TEST — the whole case for the clause.  Where one file publishes SEVERAL
       control columns, the pick and the ladder are the same, so REGRET is IDENTICAL across
       them while ROOM and MARGIN move with the comparand.  The within-file sd of each of the
       three quantities across control columns is published: if REGRET's is 0 and MARGIN's is
       not, then MARGIN is a statement about the chosen comparand and REGRET is not.
    E. RULE 8 ON LIVE PRICES, OUT OF CORPUS.  Idea 229's pre-registered 6-dial x 3-panel x
       2-cost ladder (imported unchanged, choice on IS <= 2016-12-31, 2017-2026 read once),
       re-read under FOUR control vocabularies, with ROOM/REGRET/MARGIN quoted for each, and
       both KEEP paths (4a vs live RULES v2 and vs v1; 4b vs SPY) on the pooled books, full
       sample + halves + OOS CAGR/Sharpe/MaxDD.
    F. The drafted PROTOCOL clause, in the exact wording it would be adopted in.

TUNED PARAMETERS (exactly two; all 2 x 2 = 4 grid points reported)
    P1  ladder-recovery rule in {SHARED-KEYS, DROP-ARM}  (idea 446's, imported semantics).
        SHARED-KEYS: a cell is the group formed by every structural column the walk-forward
        file and the grid share; the ladder is the grid's remaining structural columns.
        DROP-ARM:    the same, minus arm-like columns from the cell key, so a file that
        publishes the arm it chose still yields a ladder to compare against.
    P2  control vocabulary in {STRICT, BROAD}  (idea 229's, imported).  STRICT admits only an
        unselected ARM of the same ladder as the control; BROAD additionally admits the
        baseline BOOKS (base/v1/v2/live).  P2 is carried precisely because REGRET should be
        invariant to it and MARGIN should not.
    Everything else -- the admitted shapes, the IS/OOS split, the live corpus's six ladders and
    their declared incumbents, costs, cadence, gross, panels, t+1 execution, the 260-bar
    warm-up skip -- is the record's committed convention, imported, not chosen here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    R1  The queue's "32 instances publish a regret column" is a FILE-or-instance count that
        will not reproduce exactly; the true count is checked and published either way.
    R2  Across the back-filled record the pooled ROOM will be LARGE and positive relative to
        REGRET, so the published MARGIN is mostly a verdict on the incumbent.
    R3  REGRET will be strictly positive and much more tightly dispersed (relative to its own
        mean) than MARGIN, which is what makes it the quotable number.
    R4  Within a file with several control columns, sd(REGRET) will be exactly 0 and
        sd(MARGIN) = sd(ROOM) > 0.  This is an identity, so a non-zero sd(REGRET) would be a
        bug in the recovery, not a finding.
    R5  The live 36-cell corpus will reproduce idea 229's REGRET ~0.04 and will produce NO 4b
        KEEP for any of the pooled books.

CONFOUNDS / CAVEATS declared up front
    * This is a re-reading of the RECORD's committed artefacts.  A file that never wrote a grid
      CSV cannot be back-filled and its published margin stands unaudited; the coverage
      fraction is published so the gap is visible, and rejected files are listed by reason.
    * A recovered ladder is an INFERENCE about what the selection ranged over.  The
      reproduction certificate is the check; cells that fail it can produce a NEGATIVE regret
      (the pick is not on the recovered ladder) and are reported separately, never pooled
      silently.
    * OOS_best is the ladder's OOS argmax, which is an ORACLE quantity: ROOM is therefore an
      upper bound on what any chooser could have won, not an achievable return.
    * Instances are not independent (shared panels, prices, dials, books); the bootstrap blocks
      on the instance and the file count is published beside it.
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md); tickers with
      max_1d_move >= 1.0 in data/small_meta.csv are dropped first (439 names).  SURVIVORSHIP
      BIAS -- used as a shape check, never as a tradable return.
    * 10 bps is the protocol rung; 25 bps is carried as a robustness axis.
    * This run does NOT edit PROTOCOL.md.  PROTOCOL rule 6 puts wording changes at the Sunday
      review; part F publishes the draft clause for that review.

Deterministic (seed 445000), standalone, no network.
Writes .console.txt .regretcols.csv .recovery.csv .cells.csv .instances.csv .invariance.csv
       .boot.csv .livegrid.csv .walkforward.csv .keeppaths.csv .result.md
"""
from __future__ import annotations

import glob
import importlib.util
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights            # noqa: E402
from engine import metrics                                          # noqa: E402

STEM = "2026-09-08_make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 445000
B_BOOT = 2000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I229 = _load(OUT / "2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud.py",
             "i229")
I446 = _load(OUT / "2026-09-08_re-read-the-195-base-controlled-instances-against-their-OWN-"
                   "unselected-arm_C.py", "i446")
C, H = I229.C, I229.H
IS_END, OOS_START = I229.IS_END, I229.OOS_START

P1_GRID = ["SHARED-KEYS", "DROP-ARM"]
P2_GRID = ["STRICT", "BROAD"]
CERT_LEVELS = [0.0, 0.5, 1.0]
BOOK_PREFIX = I446.BOOK_PREFIX
ARMLIKE = I446.ARMLIKE
BEST_COLS = {"best_oos_sharpe", "best_oos_in_pool", "oracle_oos_sharpe", "best_oos",
             "oos_best", "oos_best_sharpe"}


# ============================================================ PART A — the `32` audit
def regret_column_audit():
    P("=" * 118)
    P("PART A — THE `32` AUDIT.  Which committed walk-forward files already publish a REGRET")
    P("         column, or a best-in-pool column from which regret is derivable?")
    P("=" * 118)
    # this run's OWN walkforward artefact is excluded so the census is idempotent on a re-run
    files = [f for f in sorted(glob.glob(str(OUT / "*.walkforward.csv")))
             if not os.path.basename(f).startswith(STEM)]
    rows = []
    for f in files:
        base = os.path.basename(f)
        d = I229.read_csv_safe(f)
        if d is None:
            rows.append(dict(file=base, has_regret=False, has_best=False, n_rows=0,
                             mean_regret=np.nan, min_regret=np.nan,
                             reason="unreadable or empty"))
            continue
        low = {c.lower(): c for c in d.columns}
        rg = low.get("regret")
        bst = next((low[k] for k in BEST_COLS if k in low), None)
        vals = np.array([])
        if rg is not None:
            vals = pd.to_numeric(d[rg], errors="coerce").dropna().values
        elif bst is not None and "OOS_Sharpe" in d.columns:
            vals = (pd.to_numeric(d[bst], errors="coerce")
                    - pd.to_numeric(d["OOS_Sharpe"], errors="coerce")).dropna().values
        rows.append(dict(file=base, has_regret=rg is not None, has_best=bst is not None,
                         n_rows=len(d), n_regret_vals=len(vals),
                         mean_regret=float(vals.mean()) if len(vals) else np.nan,
                         min_regret=float(vals.min()) if len(vals) else np.nan,
                         neg_share=float((vals < -1e-9).mean()) if len(vals) else np.nan,
                         reason=("literal `regret` column" if rg is not None else
                                 (f"derivable from `{bst}`" if bst is not None else
                                  "no regret and no best-in-pool column"))))
    RG = pd.DataFrame(rows)
    RG.to_csv(OUT / f"{STEM}.regretcols.csv", index=False)
    lit = RG[RG.has_regret]
    der = RG[(~RG.has_regret) & RG.has_best]
    P(f"\n  {len(RG)} committed *.walkforward.csv files scanned.")
    P(f"      files with a LITERAL `regret` column          : {len(lit):4d} "
      f"({len(lit)/len(RG):.1%})")
    P(f"      files with regret DERIVABLE from a best column: {len(der):4d}")
    P(f"      files with neither                            : "
      f"{len(RG)-len(lit)-len(der):4d}")
    v = lit[np.isfinite(lit.mean_regret)]
    if len(v):
        P(f"\n      on the {len(v)} files that publish it, mean regret per file ranges "
          f"{v.mean_regret.min():+.5f} to {v.mean_regret.max():+.5f}, "
          f"file-mean {v.mean_regret.mean():+.5f}, median {v.mean_regret.median():+.5f}")
        P(f"      files with at least one NEGATIVE published regret (impossible if regret is "
          f"best-minus-pick): {int((v.min_regret < -1e-9).sum())} of {len(v)}")
        negsh = float((v.neg_share * v.n_regret_vals).sum() / v.n_regret_vals.sum())
        P(f"      share of ALL {int(v.n_regret_vals.sum())} published regret VALUES that are "
          f"negative: {negsh:.1%}  ->  `regret` is not a defined term in this record; in "
          f"several\n      files it is a signed margin wearing the name.")
    P(f"\n  ==> the queue's '32 instances that already publish a regret column' is checked "
      f"against\n      {len(lit)} FILES with a literal column ({int(lit.n_regret_vals.sum())} "
      f"rows) and {len(der)} more that are derivable.")
    return RG


# ============================================================ census helper
def wframe(vocab):
    CE, CL = I229.census(vocab)
    a = CE[CE.admitted & (CE.kind == "W")].copy()
    a["ctl"] = a.reason.str.replace("control column ", "", regex=False)
    a["pre"] = a.ctl.str.lower().str.replace("oos_sharpe", "", regex=False).str.strip("_")
    a["family"] = np.where(a.pre.isin(BOOK_PREFIX), "BOOK", "ARM")
    a["vocab"] = vocab
    return a, CE, CL


# ============================================================ PART B — the back-fill
def backfill(WS):
    P("\n" + "=" * 118)
    P("PART B — BACK-FILL ROOM AND REGRET over every SHAPE-W instance whose ladder can be")
    P("         rebuilt from its committed <stem>.grid.csv.  4 grid points (P1 x P2).")
    P("=" * 118)
    rec_rows, cells = [], []
    for vocab in P2_GRID:
        W = WS[vocab]
        for rule in P1_GRID:
            for f in sorted(W.file.unique()):
                stem = f[: -len(".walkforward.csv")]
                g = OUT / f"{stem}.grid.csv"
                insts = W[W.file == f]
                def rej(reason):
                    rec_rows.append(dict(vocab=vocab, rule=rule, file=f, ok=False,
                                         reason=reason, n_cells=0, n_ladder=0,
                                         cert=np.nan, med_ladder=0))
                if not g.exists():
                    rej("no committed <stem>.grid.csv"); continue
                try:
                    d = pd.read_csv(g)
                except Exception:
                    rej("grid unreadable"); continue
                if "OOS_Sharpe" not in d.columns or not len(d):
                    rej("grid carries no OOS_Sharpe column"); continue
                try:
                    wf = pd.read_csv(OUT / f)
                except Exception:
                    rej("walkforward unreadable"); continue
                nmg = [c for c in d.columns if not I446.is_metric(d, c)]
                nmw = [c for c in wf.columns if not I446.is_metric(wf, c)]
                K = [c for c in nmg if c in nmw]
                if rule == "DROP-ARM":
                    K = [c for c in K if c.lower() not in ARMLIKE]
                dial = [c for c in nmg if c not in K]
                if not dial:
                    rej("grid has no structural column outside the cell key"); continue
                grp = d.groupby(K, dropna=False) if K else [((0,), d)]
                gd = {}
                for key, sub in grp:
                    kk = key if isinstance(key, tuple) else (key,)
                    arr = pd.to_numeric(sub.OOS_Sharpe, errors="coerce").values
                    arr = arr[np.isfinite(arr)]
                    if len(arr) >= 2:
                        gd[kk] = arr
                low = {c.lower(): c for c in wf.columns}
                pub_rg = low.get("regret")
                v_all = pd.to_numeric(wf.get("OOS_Sharpe"), errors="coerce").values
                keys_all = ([tuple(r) for r in wf[K].itertuples(index=False, name=None)]
                            if K else [(0,)] * len(wf))
                ncell = nlad = nhit = 0
                lad_len = []
                for inst in insts.itertuples():
                    c0 = inst.ctl
                    if c0 not in wf.columns:
                        continue
                    b_all = pd.to_numeric(wf[c0], errors="coerce").values
                    pr_all = (pd.to_numeric(wf[pub_rg], errors="coerce").values
                              if pub_rg else np.full(len(wf), np.nan))
                    for i in range(len(wf)):
                        v, b = v_all[i], b_all[i]
                        if not (np.isfinite(v) and np.isfinite(b)):
                            continue
                        ncell += 1
                        arr = gd.get(keys_all[i])
                        if arr is None:
                            continue
                        nlad += 1
                        lad_len.append(len(arr))
                        hit = bool(np.min(np.abs(arr - v)) < 1e-6)
                        nhit += int(hit)
                        best = float(arr.max())
                        cells.append(dict(
                            vocab=vocab, rule=rule, file=f,
                            instance=f"{f}::W::{c0}", control=c0, prefix=inst.pre,
                            family=inst.family, ladder_len=len(arr), hit=hit,
                            oos_pick=float(v), oos_ctl=float(b), oos_best=best,
                            regret=best - float(v), room=best - float(b),
                            margin=float(v) - float(b),
                            pub_regret=float(pr_all[i]) if np.isfinite(pr_all[i]) else np.nan))
                cert = nhit / nlad if nlad else np.nan
                rec_rows.append(dict(
                    vocab=vocab, rule=rule, file=f, ok=nlad > 0,
                    reason=(f"recovered: cell key {K if K else '(single group)'}, "
                            f"ladder axis {dial}" if nlad
                            else "no cell matched a >=2-arm ladder group"),
                    n_cells=ncell, n_ladder=nlad, cert=cert,
                    med_ladder=int(np.median(lad_len)) if lad_len else 0))
    RC = pd.DataFrame(rec_rows)
    CL = pd.DataFrame(cells)
    RC.to_csv(OUT / f"{STEM}.recovery.csv", index=False)
    CL.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    for vocab in P2_GRID:
        for rule in P1_GRID:
            r = RC[(RC.vocab == vocab) & (RC.rule == rule)]
            ok = r[r.ok]
            P(f"\n  P2={vocab:6s} P1={rule:11s}: {len(r):3d} SHAPE-W files attempted, "
              f"{len(ok):3d} recovered ({len(ok)/max(len(r),1):.1%}), "
              f"{int(ok.n_ladder.sum()):6d} cells on a >=2-arm ladder "
              f"(median ladder {ok.med_ladder.median() if len(ok) else float('nan'):.0f} arms)")
            P(f"      reproduction certificate: mean {ok.cert.mean():.1%} of cells; "
              f"{int((ok.cert >= 0.999).sum())}/{len(ok)} files at 100%, "
              f"{int((ok.cert >= 0.5).sum())}/{len(ok)} at >= 50%")
            rej = r[~r.ok]
            if len(rej):
                P(f"      REJECTED {len(rej)} files, by reason (nothing dropped silently):")
                for rr, n in rej.reason.value_counts().items():
                    P(f"          {n:4d}  {rr}")

    # ---- the identity, checked
    if len(CL):
        err = float(np.abs(CL.margin - (CL.room - CL.regret)).max())
        P(f"\n  IDENTITY CHECK  max |MARGIN - (ROOM - REGRET)| over all "
          f"{len(CL)} back-filled cells = {err:.3e}   (must be ~0 by construction)")
        pub = CL[np.isfinite(CL.pub_regret)]
        if len(pub):
            d_ = (pub.pub_regret - pub.regret).abs()
            P(f"  PUBLISHED-vs-RECOVERED regret agrees on {len(pub)} cells: "
              f"mean |diff| {d_.mean():.5f}, median {d_.median():.5f}, "
              f"share within 1e-6 {(d_ < 1e-6).mean():.1%}")
        else:
            P("  PUBLISHED-vs-RECOVERED regret: no back-filled cell also carries a published "
              "regret column.")
    return RC, CL


# ============================================================ PART C — the attribution
def attribution(CL):
    P("\n" + "=" * 118)
    P("PART C — THE ATTRIBUTION.  How much of the record's published MARGIN is ROOM (a verdict")
    P("         on the incumbent) and how much is REGRET (the only term selection controls)?")
    P("=" * 118)
    rows = []
    for vocab in P2_GRID:
        for rule in P1_GRID:
            for cmin in CERT_LEVELS:
                sub = CL[(CL.vocab == vocab) & (CL.rule == rule)]
                fc = sub.groupby("file").hit.mean()
                sub = sub[sub.file.isin(fc[fc >= cmin].index)]
                if not len(sub):
                    continue
                inst = sub.groupby("instance")[["margin", "room", "regret"]].mean()
                rng = np.random.default_rng(SEED + 7)
                iv = inst.values
                bs = {}
                for j, nm in enumerate(["margin", "room", "regret"]):
                    dr = np.array([iv[rng.integers(0, len(iv), len(iv)), j].mean()
                                   for _ in range(B_BOOT)])
                    bs[nm] = np.percentile(dr, [2.5, 97.5])
                roomdom = float((inst.room.abs() > inst.regret.abs()).mean())
                rows.append(dict(
                    vocab=vocab, rule=rule, cert_min=cmin, files=sub.file.nunique(),
                    instances=len(inst), cells=len(sub),
                    margin_cell=sub.margin.mean(), room_cell=sub.room.mean(),
                    regret_cell=sub.regret.mean(),
                    margin_inst=inst.margin.mean(), room_inst=inst.room.mean(),
                    regret_inst=inst.regret.mean(),
                    margin_lo=bs["margin"][0], margin_hi=bs["margin"][1],
                    room_lo=bs["room"][0], room_hi=bs["room"][1],
                    regret_lo=bs["regret"][0], regret_hi=bs["regret"][1],
                    margin_sd=inst.margin.std(ddof=1), room_sd=inst.room.std(ddof=1),
                    regret_sd=inst.regret.std(ddof=1),
                    room_dominated=roomdom,
                    regret_nonneg=float((sub.regret >= -1e-9).mean())))
    A = pd.DataFrame(rows)
    A.to_csv(OUT / f"{STEM}.boot.csv", index=False)
    P(f"\n  {'P2':6s} {'P1':11s} {'cert':>5s} {'inst':>5s} {'cells':>6s} "
      f"{'MARGIN':>9s} {'95% CI':>19s} {'ROOM':>9s} {'REGRET':>9s} {'95% CI':>19s} "
      f"{'room-dom':>9s}")
    for r in A.itertuples():
        P(f"  {r.vocab:6s} {r.rule:11s} {r.cert_min:5.1f} {r.instances:5d} {r.cells:6d} "
          f"{r.margin_inst:+9.5f} [{r.margin_lo:+8.5f},{r.margin_hi:+8.5f}] "
          f"{r.room_inst:+9.5f} {r.regret_inst:+9.5f} "
          f"[{r.regret_lo:+8.5f},{r.regret_hi:+8.5f}] {r.room_dominated:8.1%}")
    if len(A):
        a0 = A[A.cert_min == 0.0]
        P(f"\n      Across the 4 (P1 x P2) grid points at cert>=0:")
        P(f"          MARGIN spans {a0.margin_inst.min():+.5f} .. {a0.margin_inst.max():+.5f} "
          f"(swing {a0.margin_inst.max()-a0.margin_inst.min():.5f})")
        P(f"          ROOM   spans {a0.room_inst.min():+.5f} .. {a0.room_inst.max():+.5f} "
          f"(swing {a0.room_inst.max()-a0.room_inst.min():.5f})")
        P(f"          REGRET spans {a0.regret_inst.min():+.5f} .. "
          f"{a0.regret_inst.max():+.5f} (swing "
          f"{a0.regret_inst.max()-a0.regret_inst.min():.5f})")
        P(f"          relative dispersion across instances (sd / |mean|): "
          f"MARGIN {(a0.margin_sd/a0.margin_inst.abs()).mean():.2f}, "
          f"REGRET {(a0.regret_sd/a0.regret_inst.abs()).mean():.2f}  "
          f"— lower is more quotable")
    return A


# ============================================================ PART D — the invariance test
def invariance(CL):
    P("\n" + "=" * 118)
    P("PART D — THE INVARIANCE TEST.  Within one file, several control columns share the same")
    P("         pick and the same ladder.  REGRET must be identical across them; ROOM and")
    P("         MARGIN must move with the comparand.  That asymmetry IS the clause.")
    P("=" * 118)
    rows = []
    for (vocab, rule, f), g in CL.groupby(["vocab", "rule", "file"]):
        if g.control.nunique() < 2:
            continue
        # align cells across controls by their pick's OOS Sharpe (the row identity)
        piv = g.pivot_table(index="oos_pick", columns="control",
                            values=["regret", "room", "margin"], aggfunc="mean")
        for nm in ("regret", "room", "margin"):
            sub = piv[nm].dropna()
            if len(sub) == 0 or sub.shape[1] < 2:
                continue
            rows.append(dict(vocab=vocab, rule=rule, file=f, quantity=nm,
                             n_controls=sub.shape[1], n_cells=len(sub),
                             within_sd=float(sub.std(axis=1, ddof=0).mean()),
                             within_range=float((sub.max(axis=1) - sub.min(axis=1)).mean())))
    IV = pd.DataFrame(rows)
    IV.to_csv(OUT / f"{STEM}.invariance.csv", index=False)
    if not len(IV):
        P("\n  No file publishes two or more admitted control columns under any grid point;")
        P("  the invariance test is unavailable on the record and is carried in part E only.")
        return IV
    P(f"\n  {IV.file.nunique()} files publish >=2 admitted control columns "
      f"({len(IV)//3} file x gridpoint blocks).")
    P(f"\n  {'quantity':9s} {'blocks':>7s} {'mean within-file sd':>21s} "
      f"{'mean within-file range':>24s} {'blocks with sd=0':>18s}")
    for nm, g in IV.groupby("quantity"):
        P(f"  {nm:9s} {len(g):7d} {g.within_sd.mean():21.9f} "
          f"{g.within_range.mean():24.9f} "
          f"{int((g.within_sd < 1e-12).sum()):10d}/{len(g):<7d}")
    rg = IV[IV.quantity == "regret"]
    mg = IV[IV.quantity == "margin"]
    P(f"\n      ==> REGRET is invariant to the comparand in "
      f"{int((rg.within_sd < 1e-12).sum())} of {len(rg)} blocks; MARGIN is invariant in "
      f"{int((mg.within_sd < 1e-12).sum())} of {len(mg)}.")
    return IV


# ============================================================ PART E — rule 8 on live prices
def csd(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def run_live():
    P("\n" + "=" * 118)
    P("PART E — RULE 8 ON LIVE PRICES, OUT OF CORPUS.  Idea 229's pre-registered 6-dial x")
    P("         3-panel x 2-cost ladder, imported unchanged.  Choice on IS (<= 2016-12-31)")
    P("         only; 2017-2026 read once.")
    P("=" * 118)
    ref, rows, RET = {}, [], {}
    t0 = time.time()
    for pk in I229.PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        s, above, v = I229.parts(px, pk)
        n_elig = float((above & (v < 0.60)).loc[start:].sum(axis=1).mean())
        nmap = {mm: max(2, int(round(mm * n_elig)))
                for mm in [0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.53, 0.75]}
        v2 = {c: I229.fast_backtest(px, rules_v2_weights(px), c).loc[start:]
              for c in I229.COSTS}
        v1 = {c: I229.fast_backtest(px, rules_v1_weights(px), c).loc[start:]
              for c in I229.COSTS}
        ref[pk] = dict(px=px, start=start, spy=spy, v2=v2, v1=v1, desc=desc)
        cg, sh, dd = csd(spy)
        oc, osh, odd = csd(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        P(f"      SPY {cg:.2%}/{sh:.3f}/{dd:.2%} | OOS {oc:.2%}/{osh:.3f}/{odd:.2%}")
        for c in I229.COSTS:
            a, b, d_ = csd(v2[c])
            e, f_, g_ = csd(v1[c])
            P(f"      RULES v2 @{c:.0f}bps {a:.2%}/{b:.3f}/{d_:.2%}   "
              f"RULES v1 @{c:.0f}bps {e:.2%}/{f_:.3f}/{g_:.2%}")
        for dial, (ladder, dflt) in I229.DIALS.items():
            for arm in ladder:
                Wt, freq = I229.live_book(px, pk, dial, arm, nmap)
                for cost in I229.COSTS:
                    r = I229.fast_backtest(px, Wt, cost, freq).loc[start:]
                    RET[(pk, cost, dial, arm)] = r
                    cgr, shr, ddr = csd(r)
                    oc2, osh2, odd2 = csd(r.loc[OOS_START:])
                    rows.append(dict(panel=pk, cost=cost, dial=dial, arm=arm,
                                     is_default=(arm == dflt),
                                     IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                     CAGR=cgr, Sharpe=shr, MaxDD=ddr,
                                     OOS_CAGR=oc2, OOS_Sharpe=osh2, OOS_MaxDD=odd2))
        P(f"      {sum(len(l) for l, _ in I229.DIALS.values())*len(I229.COSTS)} books done "
          f"({time.time()-t0:.0f}s cum.)")
    LG = pd.DataFrame(rows)
    LG.to_csv(OUT / f"{STEM}.livegrid.csv", index=False)
    return ref, LG, RET


def live_room_regret(ref, LG, RET):
    P("\n  (i) ROOM / REGRET / MARGIN on the 36 live cells, under FOUR control vocabularies.")
    P("      REGRET = OOS_best - OOS_pick does not depend on the control at all; ROOM and")
    P("      MARGIN do.  Same picks, same ladders, four comparands.")
    wf = []
    for pk in I229.PANELS:
        for cost in I229.COSTS:
            for dial, (ladder, dflt) in I229.DIALS.items():
                sub = LG[(LG.panel == pk) & (LG.cost == cost)
                         & (LG.dial == dial)].set_index("arm").reindex(ladder)
                pick = str(sub.IS_Sharpe.idxmax())
                oarg = str(sub.OOS_Sharpe.idxmax())
                best = float(sub.OOS_Sharpe.max())
                opick = float(sub.loc[pick, "OOS_Sharpe"])
                lad_mean = float(sub.OOS_Sharpe.mean())
                ctls = {
                    "INCUMBENT arm": float(sub.loc[dflt, "OOS_Sharpe"]),
                    "LADDER-MEAN": lad_mean,
                    "BOOK v2 (live)": metrics(ref[pk]["v2"][cost].loc[OOS_START:])["Sharpe"],
                    "BOOK v1": metrics(ref[pk]["v1"][cost].loc[OOS_START:])["Sharpe"],
                }
                for cn, cv in ctls.items():
                    wf.append(dict(panel=pk, cost=cost, dial=dial, control=cn, pick=pick,
                                   s0=dflt, oos_argmax=oarg,
                                   dist_steps=abs(ladder.index(pick) - ladder.index(oarg)),
                                   ladder_len=len(ladder),
                                   OOS_Sharpe_pick=opick, OOS_Sharpe_ctl=cv,
                                   OOS_best=best, regret=best - opick, room=best - cv,
                                   margin=opick - cv,
                                   OOS_CAGR_pick=float(sub.loc[pick, "OOS_CAGR"]),
                                   OOS_MaxDD_pick=float(sub.loc[pick, "OOS_MaxDD"]),
                                   OOS_CAGR_s0=float(sub.loc[dflt, "OOS_CAGR"]),
                                   OOS_MaxDD_s0=float(sub.loc[dflt, "OOS_MaxDD"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  {'control':16s} {'cells':>5s} {'beats ctl':>10s} {'ROOM':>10s} {'REGRET':>10s} "
      f"{'MARGIN':>10s} {'95% CI on MARGIN':>24s}")
    rng = np.random.default_rng(SEED + 3)
    for cn, g in WF.groupby("control", sort=False):
        dr = np.array([g.margin.values[rng.integers(0, len(g), len(g))].mean()
                       for _ in range(B_BOOT)])
        lo, hi = np.percentile(dr, [2.5, 97.5])
        P(f"  {cn:16s} {len(g):5d} {int((g.margin>0).sum()):6d}/{len(g):<3d} "
          f"{g.room.mean():+10.5f} {g.regret.mean():10.5f} {g.margin.mean():+10.5f} "
          f"[{lo:+10.5f}, {hi:+10.5f}]")
    r0 = WF[WF.control == "INCUMBENT arm"]
    rng2 = np.random.default_rng(SEED + 4)
    dr2 = np.array([r0.regret.values[rng2.integers(0, len(r0), len(r0))].mean()
                    for _ in range(B_BOOT)])
    lo2, hi2 = np.percentile(dr2, [2.5, 97.5])
    P(f"\n      REGRET is IDENTICAL under all four vocabularies (sd across controls "
      f"{WF.groupby(['panel','cost','dial']).regret.std(ddof=0).max():.2e}); "
      f"MARGIN swings\n      "
      f"{WF.groupby('control').margin.mean().max() - WF.groupby('control').margin.mean().min():.5f} "
      f"of Sharpe across the same four.")
    P(f"      MEAN REGRET = {r0.regret.mean():.5f}, 95% CI [{lo2:.5f}, {hi2:.5f}] "
      f"(idea 229 published 0.03871 [0.02078, 0.05805]).")
    P(f"\n      by dial (REGRET is a property of the DIAL and the SELECTOR, not the comparand):")
    P(f"      {'dial':9s} {'cells':>5s} {'ROOM(incumbent)':>16s} {'REGRET':>9s} "
      f"{'MARGIN':>9s} {'|IS-OOS| steps':>15s}")
    for d, g in r0.groupby("dial"):
        P(f"      {d:9s} {len(g):5d} {g.room.mean():+16.5f} {g.regret.mean():9.5f} "
          f"{g.margin.mean():+9.5f} {g.dist_steps.mean():15.2f}")
    P(f"      {'ALL':9s} {len(r0):5d} {r0.room.mean():+16.5f} {r0.regret.mean():9.5f} "
      f"{r0.margin.mean():+9.5f} {r0.dist_steps.mean():15.2f}")
    return WF


def keep_paths(ref, LG, RET):
    P("\n  (ii) BOTH KEEP PATHS on the pooled books (equal weight over the 36 cells, t+1).")
    books = {"S1 IS-Sharpe chooser": [], "S0 do nothing (incumbent arm)": [],
             "LADDER-MEAN (hold every arm)": [], "ORACLE (OOS argmax, not a rule)": []}
    spy_p, v2_p, v1_p = [], [], []
    for pk in I229.PANELS:
        for cost in I229.COSTS:
            for dial, (ladder, dflt) in I229.DIALS.items():
                sub = LG[(LG.panel == pk) & (LG.cost == cost)
                         & (LG.dial == dial)].set_index("arm").reindex(ladder)
                pick = str(sub.IS_Sharpe.idxmax())
                orc = str(sub.OOS_Sharpe.idxmax())
                books["S1 IS-Sharpe chooser"].append(RET[(pk, cost, dial, pick)])
                books["S0 do nothing (incumbent arm)"].append(RET[(pk, cost, dial, dflt)])
                books["LADDER-MEAN (hold every arm)"].append(
                    sum(RET[(pk, cost, dial, a)] for a in ladder) / len(ladder))
                books["ORACLE (OOS argmax, not a rule)"].append(RET[(pk, cost, dial, orc)])
            spy_p.append(ref[pk]["spy"])
            v2_p.append(ref[pk]["v2"][cost])
            v1_p.append(ref[pk]["v1"][cost])

    def pool(lst):
        return pd.concat(lst, axis=1).mean(axis=1).dropna()

    pooled = {k: pool(v) for k, v in books.items()}
    SPY, V2, V1 = pool(spy_p), pool(v2_p), pool(v1_p)
    ref_rows = {"SPY": SPY, "RULES v2 (live) pooled": V2, "RULES v1 pooled": V1}

    def halves(r):
        mid = r.index[len(r) // 2]
        return metrics(r.loc[:mid])["Sharpe"], metrics(r.loc[mid:])["Sharpe"]

    sH1, sH2 = halves(SPY)
    sOOS = metrics(SPY.loc[OOS_START:])
    v2H1, v2H2 = halves(V2)
    v1H1, v1H2 = halves(V1)
    P(f"\n      4b bars off the pooled SPY: H1 > {sH1:.3f}, H2 > {sH2:.3f}, "
      f"OOS Sharpe > {sOOS['Sharpe']:.3f}, |MaxDD| <= "
      f"{abs(metrics(SPY)['MaxDD'])*0.6:.2%}, CAGR >= {metrics(SPY)['CAGR']*0.7:.2%}")
    P(f"\n  {'book':32s} {'CAGR':>7s} {'Shrp':>6s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"{'oCAGR':>7s} {'oShrp':>6s} {'oMaxDD':>8s} {'4a v2':>6s} {'4a v1':>6s} {'4b':>5s} "
      f"{'failing':>20s}")
    kp = []
    for name, r in list(pooled.items()) + list(ref_rows.items()):
        m, o = metrics(r), metrics(r.loc[OOS_START:])
        h1, h2 = halves(r)
        is_ref = name in ref_rows
        a2 = (not is_ref) and h1 > v2H1 and h2 > v2H2 and \
            abs(m["MaxDD"]) <= abs(metrics(V2)["MaxDD"])
        a1 = (not is_ref) and h1 > v1H1 and h2 > v1H2 and \
            abs(m["MaxDD"]) <= abs(metrics(V1)["MaxDD"])
        fails = []
        if h1 <= sH1:
            fails.append("H1")
        if h2 <= sH2:
            fails.append("H2")
        if o["Sharpe"] <= sOOS["Sharpe"]:
            fails.append("OOS")
        if abs(m["MaxDD"]) > abs(metrics(SPY)["MaxDD"]) * 0.6:
            fails.append("MaxDD")
        if m["CAGR"] < metrics(SPY)["CAGR"] * 0.7:
            fails.append("CAGR")
        b4 = (not is_ref) and not fails
        P(f"  {name:32s} {m['CAGR']:7.2%} {m['Sharpe']:6.3f} {m['MaxDD']:8.2%} {h1:6.3f} "
          f"{h2:6.3f} {o['CAGR']:7.2%} {o['Sharpe']:6.3f} {o['MaxDD']:8.2%} "
          f"{('-' if is_ref else str(a2)):>6s} {('-' if is_ref else str(a1)):>6s} "
          f"{('-' if is_ref else str(b4)):>5s} "
          f"{('-' if is_ref else '|'.join(fails) or 'none'):>20s}")
        kp.append(dict(book=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                       H1=h1, H2=h2, OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"],
                       OOS_MaxDD=o["MaxDD"], keep4a_v2=a2, keep4a_v1=a1, keep4b=b4,
                       failing="|".join(fails), is_reference=is_ref))
    KP = pd.DataFrame(kp)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    cand = KP[~KP.is_reference]
    P(f"\n      KEEP: 4a-vs-v2 {int(cand.keep4a_v2.sum())} of {len(cand)}, "
      f"4a-vs-v1 {int(cand.keep4a_v1.sum())} of {len(cand)}, "
      f"4b {int(cand.keep4b.sum())} of {len(cand)}.")
    return KP


# ============================================================ PART F — the drafted clause
CLAUSE = """\
10. **Selection results publish ROOM and REGRET, not the margin alone (proposed, idea 445).**
    Any result that reports an in-sample chooser beating (or losing to) a comparand must
    publish, beside the margin, the two terms it decomposes into:

        MARGIN = OOS(pick) - OOS(control)  =  ROOM - REGRET
        ROOM   = OOS(best arm on the ladder) - OOS(control)   [a verdict on the CONTROL]
        REGRET = OOS(best arm on the ladder) - OOS(pick)      [>= 0; the SELECTOR's shortfall]

    ROOM is a property of the comparand and the dial; it changes when the comparand changes
    and says nothing about the selector.  REGRET is invariant to the comparand and is the only
    term selection controls.  A run may therefore not claim "selection helps/loses" from the
    margin alone; it must quote the REGRET, and it must name the control's family (an
    unselected ARM of the same ladder, or a BOOK).  The ladder and its per-arm OOS metrics are
    committed with the result so both terms are reconstructable.
"""


def main():
    t0 = time.time()
    P("# Idea 445 — make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN")
    P(f"# cloud lane, {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}, seed {SEED}")
    P("# P1 ladder recovery in {SHARED-KEYS, DROP-ARM}; P2 control vocabulary in "
      "{STRICT, BROAD}; all 4 points reported.\n")
    RG = regret_column_audit()
    WS = {}
    for vocab in P2_GRID:
        W, CE, CL = wframe(vocab)
        WS[vocab] = W
        P(f"\n  census {vocab}: {len(W)} SHAPE-W instances over {W.file.nunique()} files "
          f"(ARM-controlled {int((W.family=='ARM').sum())}, "
          f"BOOK-controlled {int((W.family=='BOOK').sum())})")
    RC, CL = backfill(WS)
    A = attribution(CL)
    IV = invariance(CL)
    ref, LG, RET = run_live()
    WF = live_room_regret(ref, LG, RET)
    KP = keep_paths(ref, LG, RET)
    P("\n" + "=" * 118)
    P("PART F — THE DRAFTED PROTOCOL CLAUSE (for the Sunday review; this run does not edit")
    P("         PROTOCOL.md).")
    P("=" * 118 + "\n")
    for ln in CLAUSE.rstrip().split("\n"):
        P("  " + ln)
    # instance-level table for the record
    if len(CL):
        inst = (CL.groupby(["vocab", "rule", "instance", "family", "prefix"])
                [["margin", "room", "regret", "oos_pick", "oos_ctl", "oos_best", "hit"]]
                .mean().reset_index())
        inst.to_csv(OUT / f"{STEM}.instances.csv", index=False)
        P(f"\n  wrote {len(inst)} back-filled instance rows to {STEM}.instances.csv")
    P(f"\n\n[done in {time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
