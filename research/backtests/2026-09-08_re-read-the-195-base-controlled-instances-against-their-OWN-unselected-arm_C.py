#!/usr/bin/env python3
"""Idea 446 — re-read-the-195-base-controlled-instances-against-their-OWN-unselected-arm
   (lane C, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 229's P1 shows the do-nothing vocabulary flips the pooled sign by 0.155 of Sharpe:
    STRICT (the unselected arm of the same ladder) gives -0.0015, BROAD (which admits `base_*`,
    almost always the RULES baseline book) gives +0.1533.  195 SHAPE-W instances have `base_*`
    as their only control.  For every one whose ladder is reconstructable from a committed
    grid.csv, recompute the margin against the unselected arm and report how many published
    verdicts move.

WHAT THIS RUN DOES
    A. PREMISE AUDIT.  Re-runs idea 229's own `census()` (imported, not re-implemented, so the
       parent's numbers are reproduced rather than re-derived) and decomposes its 195 SHAPE-W
       BROAD instances by the control PREFIX each one actually uses.  The queue's sentence is
       checked, not assumed.
    B. LADDER RECOVERY.  For every BOOK-CONTROLLED instance (control prefix in base/v1/v2/live)
       the run tries to rebuild the arm ladder the selection ran over, from the committed
       `<stem>.grid.csv`, and re-prices the margin against an UNSELECTED ARM of that same
       ladder instead of against the baseline book.  Every file is admitted or rejected WITH
       ITS REASON; a reproduction certificate (does the recovered ladder actually contain the
       selected arm's own published OOS Sharpe?) is published per instance and per cell, and
       results are reported at three certificate thresholds so the reader can see the
       sensitivity rather than take a cut-off on faith.
    C. HOW MANY PUBLISHED VERDICTS MOVE.  Per instance: published sign (vs the book) against
       recomputed sign (vs the arm), the sign-flip count, the magnitude shift, and a bootstrap
       over instances on both pooled means.
    D. RULE 8 ON LIVE PRICES, out of corpus.  Idea 229's pre-registered 6-dial x 3-panel x
       2-cost corpus (its `run_live` inputs, reused unchanged) is re-priced under FOUR control
       vocabularies -- the declared incumbent arm, the ladder mean, the ladder median arm, and
       the baseline book (v1 and v2) -- so the vocabulary effect is measured on prices this run
       computed itself, not only on the record.  Pooled equal-weight books for CHOOSER, S0,
       LADDER-MEAN and BOOK-CONTROL are then run through BOTH KEEP paths (4a vs live RULES v2
       and v1; 4b vs SPY) full sample + halves + OOS.

TUNED PARAMETERS (exactly two; every one of the 2 x 3 = 6 grid points reported)
    P1  ladder-recovery rule in {SHARED-KEYS, DROP-ARM}.
        SHARED-KEYS: a cell is the group formed by every structural column the walk-forward
        file and the grid share; the ladder is the grid's remaining structural columns.
        DROP-ARM:    the same, except columns whose NAME is arm-like (arm, pick, sel, dial,
        kind, ...) are removed from the cell key, so a file that publishes the arm it chose
        still yields a ladder to compare against.
    P2  default (unselected) arm in {LADDER-MEAN, LADDER-MEDIAN, EXCL-MEAN}.
        LADDER-MEAN   hold every arm of the ladder equally -- the literal "do not select".
        LADDER-MEDIAN the middle rung of the ladder ordered along its own dial (numeric where
                      parseable, lexical otherwise) -- never ordered by outcome.
        EXCL-MEAN     the mean of every arm EXCEPT the one that was picked.
    Everything else -- the census vocabularies, the admitted shapes, the IS/OOS split, the
    live corpus's six ladders and their declared incumbents, costs, cadence, gross, panels,
    t+1 execution -- is idea 229's / the record's committed convention, imported, not chosen.

PRE-REGISTERED PREDICTIONS (written before any number in parts B-D was read)
    R1  The queue's premise is WRONG in its specifics: 195 is the count of ALL SHAPE-W BROAD
        instances, not of `base_*`-controlled ones.  `base_*` will be a minority; the record's
        dominant book-control will be `v1_`/`v2_`, i.e. the live RULES books.
    R2  Re-reading against the unselected arm will move the pooled mean from ~ +0.15 toward
        ~ 0, reproducing idea 229's STRICT/BROAD gap on a DIFFERENT set of instances (the ones
        229 could only read the BROAD way).
    R3  A large minority -- but not a majority -- of published instance verdicts will change
        SIGN.  A book-control is a biased comparand, not a random one: it is a low-return book,
        so most instances will look better against it, and re-reading will mostly SHRINK a
        positive margin rather than reverse it.
    R4  The choice of unselected arm (P2) will matter far less than the choice of comparand
        family (book vs arm): the three P2 levels will agree in sign on most instances.
    R5  The live 36-cell corpus will show the same ordering: margin vs book >> margin vs
        ladder-mean ~ margin vs incumbent ~ 0, and NO book will clear 4b.

CONFOUNDS / CAVEATS declared up front
    * This is a re-reading of the RECORD's committed artefacts.  A file that never wrote a
      grid CSV cannot be re-read, and its published verdict stands unaudited; the coverage
      fraction is published so the gap is visible, and unrecovered files are listed by reason.
    * A recovered ladder is an INFERENCE about what the selection ranged over.  The
      reproduction certificate (selected arm's OOS Sharpe present in the recovered ladder)
      is the check, and instances that fail it are reported separately, never pooled silently.
    * `v1_`/`v2_`-controlled instances often INTEND the baseline book as their comparand (a 4a
      question).  Re-reading them against the arm answers a different question -- the point of
      the exercise is precisely that the record's prose does not always say which one it asked.
      Both readings are published side by side; neither is deleted.
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md), max_1d_move >= 1.0
      dropped, 439 names.  SURVIVORSHIP BIAS -- a shape check, never a tradable return.
    * 10 bps is the protocol rung; 25 bps is carried as a robustness axis.  t+1 execution and
      the 260-bar warm-up skip are the engine's, unchanged.
    * Instances are not independent (shared panels, prices, dials, books); that is why the
      bootstrap blocks on the INSTANCE, and the file-level count is published beside it.

Deterministic (seed 446000), standalone, no network.
Writes .console.txt .premise.csv .recovery.csv .instances.csv .cells.csv .flips.csv
       .boot.csv .livegrid.csv .walkforward.csv .keeppaths.csv .result.md
"""
from __future__ import annotations

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
from baseline import rules_v1_weights, rules_v2_weights          # noqa: E402
from engine import metrics                                       # noqa: E402

STEM = "2026-09-08_re-read-the-195-base-controlled-instances-against-their-OWN-unselected-arm_C"
OUT = ROOT / "research" / "backtests"
SEED = 446000
B_BOOT = 2000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 400)
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


# The parent.  Its census(), vocabularies, ladders, panels and backtest helpers are IMPORTED
# so this run reproduces idea 229 rather than re-deriving it.
I229 = _load(OUT / "2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud.py",
             "i229")
C, IS_END, OOS_START = I229.C, I229.IS_END, I229.OOS_START

BOOK_PREFIX = {"base", "v1", "v2", "live"}      # the "comparand is a BOOK" family
ARM_PREFIX = {"ctl", "ctrl", "control", "anchor", "s0", "null", "nosel"}   # idea 229 STRICT

# a column is a METRIC (an outcome) rather than a STRUCTURAL column (a key or a dial) if its
# name says so, or if it is a float with essentially one value per row.
MET_RE = re.compile(
    r"(?i)(cagr|sharpe|maxdd|calmar|sortino|turn|regret|margin|equity|^dd$|_dd$|^h[12]$|"
    r"years|^t_|^p_|pval|pass|keep|beat|wins|losses|^n_cells$|spy_|^is_|_is$)")
ARMLIKE = {"arm", "pick", "sel", "selector", "rule", "method", "mode", "strategy", "chosen",
           "dial", "kind", "param", "level", "variant", "scheme", "conv"}

P1_GRID = ["SHARED-KEYS", "DROP-ARM"]
P2_GRID = ["LADDER-MEAN", "LADDER-MEDIAN", "EXCL-MEAN"]
CERT_LEVELS = [0.0, 0.5, 1.0]                   # reproduction-certificate thresholds reported


def is_metric(d: pd.DataFrame, c: str) -> bool:
    if MET_RE.search(c):
        return True
    return d[c].dtype.kind == "f" and d[c].nunique(dropna=True) > max(3, 0.5 * len(d))


def num_or_str(v):
    try:
        return (0, float(v))
    except (TypeError, ValueError):
        return (1, str(v))


# ============================================================== PART A — the premise audit
def premise_audit():
    P("=" * 118)
    P("PART A — PREMISE AUDIT.  idea 229's census() re-run (imported), its 195 SHAPE-W BROAD")
    P("         instances decomposed by the control prefix each one actually uses.")
    P("=" * 118)
    CE_S, CL_S = I229.census("STRICT")
    CE_B, CL_B = I229.census("BROAD")
    aS, aB = CE_S[CE_S.admitted], CE_B[CE_B.admitted]
    P(f"\n  reproduction of idea 229's census: STRICT {len(aS)} instances / "
      f"{aS.file.nunique()} files / {len(CL_S)} cells   (parent published 104 / 69 / 5302)")
    P(f"                                     BROAD  {len(aB)} instances / "
      f"{aB.file.nunique()} files / {len(CL_B)} cells   (parent published 237 / 119 / 19308)")
    P(f"                                     shapes BROAD: " + ", ".join(
        f"{k} {v}" for k, v in aB.kind.value_counts().items())
      + "   (parent published W 195 / L 42)")
    P(f"      pooled mean margin reproduced: STRICT {CL_S.margin.mean():+.5f} "
      f"(parent -0.00202), BROAD {CL_B.margin.mean():+.5f} (parent +0.15330)")

    W = aB[aB.kind == "W"].copy()
    W["ctl"] = W.reason.str.replace("control column ", "", regex=False)
    W["pre"] = (W.ctl.str.lower().str.replace("oos_sharpe", "", regex=False).str.strip("_"))
    W["family"] = np.where(W.pre.isin(BOOK_PREFIX), "BOOK", "ARM")
    P(f"\n  the 195 SHAPE-W BROAD instances by control prefix:")
    for pre, n in W.pre.value_counts().items():
        fam = "BOOK (a baseline book)" if pre in BOOK_PREFIX else "ARM (an unselected arm)"
        P(f"      {pre:>9s}_OOS_Sharpe  {n:4d} instances   {fam}")
    nb = int((W.family == "BOOK").sum())
    P(f"\n  ==> BOOK-controlled {nb} instances over {W[W.family=='BOOK'].file.nunique()} files; "
      f"ARM-controlled {len(W)-nb} over {W[W.family=='ARM'].file.nunique()} files "
      f"(the latter = idea 229's STRICT W count).")
    base_only = W[W.pre == "base"]
    strict_files = set(W[W.family == "ARM"].file)
    no_strict = W[(W.family == "BOOK") & (~W.file.isin(strict_files))]
    P(f"      `base_*` alone accounts for {len(base_only)} instances over "
      f"{base_only.file.nunique()} files, NOT 195.")
    P(f"      instances whose FILE carries no unselected-arm control at all: {len(no_strict)} "
      f"over {no_strict.file.nunique()} files -- these are the ones whose published verdict")
    P(f"      has no arm reading anywhere in the record, and they are the target of part B.")
    W.to_csv(OUT / f"{STEM}.premise.csv", index=False)
    return W, CL_S, CL_B


# ============================================================== PART B — ladder recovery
def recover(W):
    P("\n" + "=" * 118)
    P("PART B — LADDER RECOVERY.  For every BOOK-controlled SHAPE-W instance, rebuild the arm")
    P("         ladder from the committed <stem>.grid.csv and re-price the margin against an")
    P("         UNSELECTED ARM of that ladder.  Every file admitted or rejected with a reason.")
    P("=" * 118)
    BK = W[W.family == "BOOK"]
    rec_rows, cells = [], []
    for rule in P1_GRID:
        for f in sorted(BK.file.unique()):
            stem = f[: -len(".walkforward.csv")]
            g = OUT / f"{stem}.grid.csv"
            insts = BK[BK.file == f]
            if not g.exists():
                rec_rows.append(dict(rule=rule, file=f, ok=False,
                                     reason="no committed <stem>.grid.csv", n_cells=0,
                                     n_ladder=0, cert=np.nan, med_ladder=0))
                continue
            try:
                d = pd.read_csv(g)
            except Exception:
                rec_rows.append(dict(rule=rule, file=f, ok=False, reason="grid unreadable",
                                     n_cells=0, n_ladder=0, cert=np.nan, med_ladder=0))
                continue
            if "OOS_Sharpe" not in d.columns or not len(d):
                rec_rows.append(dict(rule=rule, file=f, ok=False,
                                     reason="grid carries no OOS_Sharpe column", n_cells=0,
                                     n_ladder=0, cert=np.nan, med_ladder=0))
                continue
            try:
                wf = pd.read_csv(OUT / f)
            except Exception:
                continue
            nmg = [c for c in d.columns if not is_metric(d, c)]
            nmw = [c for c in wf.columns if not is_metric(wf, c)]
            K = [c for c in nmg if c in nmw]
            if rule == "DROP-ARM":
                K = [c for c in K if c.lower() not in ARMLIKE]
            dial = [c for c in nmg if c not in K]
            if not dial:
                rec_rows.append(dict(rule=rule, file=f, ok=False,
                                     reason="grid has no structural column outside the cell key",
                                     n_cells=0, n_ladder=0, cert=np.nan, med_ladder=0))
                continue
            grp = d.groupby(K, dropna=False) if K else d.groupby(lambda i: 0)
            gd = {}
            for key, sub in grp:
                kk = key if isinstance(key, tuple) else (key,)
                order = sorted(range(len(sub)),
                               key=lambda i: tuple(num_or_str(sub.iloc[i][c]) for c in dial))
                gd[kk] = sub.iloc[order].reset_index(drop=True)
            ncell = nlad = nhit = 0
            lad_len = []
            for inst in insts.itertuples():
                c0 = inst.ctl
                if c0 not in wf.columns:
                    continue
                for _, row in wf.iterrows():
                    v = pd.to_numeric(pd.Series([row.get("OOS_Sharpe")]),
                                      errors="coerce").iloc[0]
                    b = pd.to_numeric(pd.Series([row.get(c0)]), errors="coerce").iloc[0]
                    if not (np.isfinite(v) and np.isfinite(b)):
                        continue
                    ncell += 1
                    key = tuple(row[c] for c in K) if K else (0,)
                    sub = gd.get(key)
                    if sub is None or len(sub) < 2:
                        continue
                    arr = pd.to_numeric(sub.OOS_Sharpe, errors="coerce").values
                    arr = arr[np.isfinite(arr)]
                    if len(arr) < 2:
                        continue
                    nlad += 1
                    lad_len.append(len(arr))
                    hit = bool(np.min(np.abs(arr - v)) < 1e-6)
                    nhit += int(hit)
                    j = int(np.argmin(np.abs(arr - v)))
                    excl = np.delete(arr, j)
                    cells.append(dict(
                        rule=rule, file=f, instance=f"{f}::W::{c0}", prefix=inst.pre,
                        ladder_len=len(arr), hit=hit,
                        oos_pick=float(v), oos_book=float(b),
                        margin_book=float(v - b),
                        d_LADDER_MEAN=float(v - np.mean(arr)),
                        d_LADDER_MEDIAN=float(v - arr[len(arr) // 2]),
                        d_EXCL_MEAN=float(v - np.mean(excl)) if len(excl) else np.nan))
            cert = nhit / nlad if nlad else np.nan
            rec_rows.append(dict(
                rule=rule, file=f, ok=nlad > 0,
                reason=(f"recovered: cell key {K if K else '(single group)'}, ladder axis {dial}"
                        if nlad else "no cell matched a >=2-arm ladder group"),
                n_cells=ncell, n_ladder=nlad, cert=cert,
                med_ladder=int(np.median(lad_len)) if lad_len else 0))
    RC = pd.DataFrame(rec_rows)
    CL = pd.DataFrame(cells)
    RC.to_csv(OUT / f"{STEM}.recovery.csv", index=False)
    for rule in P1_GRID:
        r = RC[RC.rule == rule]
        ok = r[r.ok]
        P(f"\n  P1 = {rule}:  {len(r)} book-controlled files attempted, "
          f"{len(ok)} recovered ({len(ok)/len(r):.1%}), "
          f"{int(ok.n_ladder.sum())} cells sit on a >= 2-arm ladder "
          f"(median ladder {ok.med_ladder.median():.0f} arms)")
        P(f"      reproduction certificate (selected arm's own OOS Sharpe found in the "
          f"recovered ladder): mean {ok.cert.mean():.1%} of cells; "
          f"{int((ok.cert >= 0.999).sum())}/{len(ok)} files at 100%, "
          f"{int((ok.cert >= 0.5).sum())}/{len(ok)} at >= 50%")
        rej = r[~r.ok]
        P(f"      REJECTED {len(rej)} files, by reason (nothing dropped silently):")
        for rr, n in rej.reason.value_counts().items():
            P(f"          {n:4d}  {rr}")
    return RC, CL


# ============================================================== PART C — do verdicts move?
def verdict_move(CL, RC):
    P("\n" + "=" * 118)
    P("PART C — HOW MANY PUBLISHED VERDICTS MOVE.  Published margin (vs the BOOK) against the")
    P("         re-priced margin (vs an UNSELECTED ARM), per instance, over the 2 x 3 grid.")
    P("=" * 118)
    rng = np.random.default_rng(SEED)
    out, flips, boots = [], [], []
    for rule in P1_GRID:
        sub0 = CL[CL.rule == rule]
        for cert in CERT_LEVELS:
            certmap = RC[(RC.rule == rule) & RC.ok].set_index("file").cert
            keep = set(certmap[certmap >= cert - 1e-12].index)
            sub = sub0[sub0.file.isin(keep)]
            if not len(sub):
                continue
            for p2 in P2_GRID:
                col = "d_" + p2.replace("-", "_")
                s = sub[np.isfinite(sub[col])]
                if not len(s):
                    continue
                inst_b = s.groupby("instance").margin_book.mean()
                inst_a = s.groupby("instance")[col].mean()
                j = pd.concat([inst_b.rename("book"), inst_a.rename("arm")], axis=1).dropna()
                flip = np.sign(j.book) != np.sign(j.arm)
                shrink = (j.arm.abs() < j.book.abs()) & ~flip
                out.append(dict(
                    rule=rule, cert=cert, default_arm=p2, files=s.file.nunique(),
                    instances=len(j), cells=len(s),
                    mean_book_cell=s.margin_book.mean(), mean_arm_cell=s[col].mean(),
                    mean_book_inst=j.book.mean(), mean_arm_inst=j.arm.mean(),
                    win_book=(j.book > 0).mean(), win_arm=(j.arm > 0).mean(),
                    sign_flips=int(flip.sum()), flip_share=flip.mean(),
                    shrink_share=shrink.mean(),
                    median_abs_shift=float((j.arm - j.book).abs().median())))
                if cert == 0.5:                                   # published detail at the mid rung
                    for inst, r in j.iterrows():
                        flips.append(dict(rule=rule, default_arm=p2, instance=inst,
                                          margin_vs_book=r.book, margin_vs_arm=r.arm,
                                          verdict_book="WIN" if r.book > 0 else "LOSS",
                                          verdict_arm="WIN" if r.arm > 0 else "LOSS",
                                          moved=bool(np.sign(r.book) != np.sign(r.arm))))
                    ii = j.index.values
                    db = np.array([j.book.values[rng.integers(0, len(ii), len(ii))].mean()
                                   for _ in range(B_BOOT)])
                    da = np.array([j.arm.values[rng.integers(0, len(ii), len(ii))].mean()
                                   for _ in range(B_BOOT)])
                    idx = np.array([rng.integers(0, len(ii), len(ii)) for _ in range(B_BOOT)])
                    dd = np.array([(j.arm.values[k] - j.book.values[k]).mean() for k in idx])
                    boots.append(dict(
                        rule=rule, default_arm=p2, instances=len(ii),
                        book_mean=j.book.mean(), book_lo=np.percentile(db, 2.5),
                        book_hi=np.percentile(db, 97.5),
                        arm_mean=j.arm.mean(), arm_lo=np.percentile(da, 2.5),
                        arm_hi=np.percentile(da, 97.5), arm_p_neg=(da < 0).mean(),
                        shift_mean=dd.mean(), shift_lo=np.percentile(dd, 2.5),
                        shift_hi=np.percentile(dd, 97.5)))
    S = pd.DataFrame(out)
    F = pd.DataFrame(flips)
    B = pd.DataFrame(boots)
    S.to_csv(OUT / f"{STEM}.instances.csv", index=False)
    F.to_csv(OUT / f"{STEM}.flips.csv", index=False)
    B.to_csv(OUT / f"{STEM}.boot.csv", index=False)
    CL.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    P(f"\n  ALL {len(S)} grid points (P1 x P2 x certificate threshold).  `book` = the published")
    P(f"  reading, `arm` = the re-priced one.  Means are instance-weighted.\n")
    P(f"  {'P1':12s} {'cert':>5s} {'P2':14s} {'inst':>5s} {'cells':>6s} {'mean book':>10s} "
      f"{'mean arm':>10s} {'win book':>9s} {'win arm':>8s} {'FLIPS':>7s} {'flip%':>7s} "
      f"{'shrink%':>8s}")
    for r in S.itertuples():
        P(f"  {r.rule:12s} {r.cert:5.0%} {r.default_arm:14s} {r.instances:5d} {r.cells:6d} "
          f"{r.mean_book_inst:+10.5f} {r.mean_arm_inst:+10.5f} {r.win_book:9.1%} "
          f"{r.win_arm:8.1%} {r.sign_flips:7d} {r.flip_share:7.1%} {r.shrink_share:8.1%}")

    P(f"\n  bootstrap over INSTANCES (2000 draws, certificate >= 50%):")
    P(f"  {'P1':12s} {'P2':14s} {'inst':>5s} {'book mean [95% CI]':>34s} "
      f"{'arm mean [95% CI]':>34s} {'P(arm<0)':>9s} {'shift [95% CI]':>30s}")
    for r in B.itertuples():
        P(f"  {r.rule:12s} {r.default_arm:14s} {r.instances:5d} "
          f"{r.book_mean:+10.5f} [{r.book_lo:+8.5f}, {r.book_hi:+8.5f}] "
          f"{r.arm_mean:+10.5f} [{r.arm_lo:+8.5f}, {r.arm_hi:+8.5f}] {r.arm_p_neg:9.1%} "
          f"{r.shift_mean:+8.5f} [{r.shift_lo:+8.5f}, {r.shift_hi:+8.5f}]")

    if len(F):
        mid = F[(F.rule == "DROP-ARM") & (F.default_arm == "LADDER-MEAN")]
        mv = mid[mid.moved].sort_values("margin_vs_book", ascending=False)
        P(f"\n  the instances whose VERDICT MOVES (P1 DROP-ARM, P2 LADDER-MEAN, cert >= 50%): "
          f"{len(mv)} of {len(mid)}")
        for r in mv.head(14).itertuples():
            P(f"      {r.margin_vs_book:+8.4f} -> {r.margin_vs_arm:+8.4f}  "
              f"{r.verdict_book} -> {r.verdict_arm}   {r.instance[:88]}")
        if len(mv) > 14:
            P(f"      ... {len(mv)-14} more in .flips.csv")
    return S, F, B


# ============================================================== PART D — rule 8, live prices
def csd(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def run_live():
    P("\n" + "=" * 118)
    P("PART D — RULE 8 ON LIVE PRICES, OUT OF CORPUS.  Idea 229's pre-registered 6-dial x")
    P("         3-panel x 2-cost corpus, re-priced under FOUR control vocabularies.  Choice on")
    P("         IS (<= 2016-12-31) only; 2017-2026 read once.")
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
        v2 = {c: I229.fast_backtest(px, rules_v2_weights(px), c).loc[start:] for c in I229.COSTS}
        v1 = {c: I229.fast_backtest(px, rules_v1_weights(px), c).loc[start:] for c in I229.COSTS}
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
                    o = r.loc[OOS_START:]
                    oc2, osh2, odd2 = csd(o)
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


def live_vocabularies(ref, LG, RET):
    P("\n  (i) THE SAME 36 CELLS, FOUR CONTROL VOCABULARIES.  `pick` is the IS-Sharpe argmax.")
    P(f"  {'panel':7s} {'cost':>5s} {'dial':9s} {'pick':>7s} {'OOS pick':>9s} "
      f"{'vs S0-arm':>10s} {'vs lad-mean':>12s} {'vs lad-med':>11s} {'vs v2 book':>11s} "
      f"{'vs v1 book':>11s}")
    wf = []
    for pk in I229.PANELS:
        for cost in I229.COSTS:
            b2 = metrics(ref[pk]["v2"][cost].loc[OOS_START:])["Sharpe"]
            b1 = metrics(ref[pk]["v1"][cost].loc[OOS_START:])["Sharpe"]
            for dial, (ladder, dflt) in I229.DIALS.items():
                sub = LG[(LG.panel == pk) & (LG.cost == cost) & (LG.dial == dial)]
                sub = sub.set_index("arm").reindex(ladder)
                pick = str(sub.IS_Sharpe.idxmax())
                o = sub.OOS_Sharpe
                lad_mean_r = sum(RET[(pk, cost, dial, a)] for a in ladder) / len(ladder)
                lad_mean_s = metrics(lad_mean_r.loc[OOS_START:])["Sharpe"]
                med = ladder[len(ladder) // 2]
                row = dict(panel=pk, cost=cost, dial=dial, pick=pick, s0=dflt,
                           ladder_len=len(ladder),
                           OOS_Sharpe=float(o[pick]),
                           s0_OOS_Sharpe=float(o[dflt]),
                           ladmean_OOS_Sharpe=float(lad_mean_s),
                           ladmed_OOS_Sharpe=float(o[med]),
                           v2_OOS_Sharpe=float(b2), v1_OOS_Sharpe=float(b1),
                           OOS_CAGR=float(sub.OOS_CAGR[pick]),
                           OOS_MaxDD=float(sub.OOS_MaxDD[pick]),
                           m_s0=float(o[pick] - o[dflt]),
                           m_ladmean=float(o[pick] - lad_mean_s),
                           m_ladmed=float(o[pick] - o[med]),
                           m_v2=float(o[pick] - b2), m_v1=float(o[pick] - b1))
                wf.append(row)
                P(f"  {pk:7s} {cost:5.0f} {dial:9s} {pick:>7s} {o[pick]:9.3f} "
                  f"{row['m_s0']:+10.4f} {row['m_ladmean']:+12.4f} {row['m_ladmed']:+11.4f} "
                  f"{row['m_v2']:+11.4f} {row['m_v1']:+11.4f}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n      {'vocabulary':22s} {'mean margin':>12s} {'chooser wins':>13s} "
      f"{'95% CI (cells)':>28s}")
    rng = np.random.default_rng(SEED + 7)
    for lab, col in [("S0 = incumbent arm", "m_s0"), ("ladder MEAN", "m_ladmean"),
                     ("ladder MEDIAN arm", "m_ladmed"), ("book = RULES v2", "m_v2"),
                     ("book = RULES v1", "m_v1")]:
        x = WF[col].values
        dr = np.array([x[rng.integers(0, len(x), len(x))].mean() for _ in range(B_BOOT)])
        P(f"      {lab:22s} {x.mean():+12.5f} {int((x>0).sum()):8d}/{len(x):<4d} "
          f"       [{np.percentile(dr,2.5):+8.5f}, {np.percentile(dr,97.5):+8.5f}]")
    P(f"\n      the vocabulary GAP on live prices: mean(vs v2) - mean(vs S0-arm) = "
      f"{WF.m_v2.mean()-WF.m_s0.mean():+.5f}, "
      f"mean(vs v1) - mean(vs S0-arm) = {WF.m_v1.mean()-WF.m_s0.mean():+.5f}")
    P(f"      sign agreement between the S0-arm reading and the book readings: "
      f"v2 {(np.sign(WF.m_s0)==np.sign(WF.m_v2)).mean():.1%}, "
      f"v1 {(np.sign(WF.m_s0)==np.sign(WF.m_v1)).mean():.1%}; "
      f"ladder-mean {(np.sign(WF.m_s0)==np.sign(WF.m_ladmean)).mean():.1%}")
    return WF


def keep_paths(ref, LG, RET, WF):
    P("\n  (ii) BOTH KEEP PATHS on the pooled books (equal weight over the 36 cells, t+1,")
    P("       10 bps rung shown for the baselines).")
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
        df = pd.concat(lst, axis=1)
        return df.mean(axis=1).dropna()

    pooled = {k: pool(v) for k, v in books.items()}
    SPY, V2, V1 = pool(spy_p), pool(v2_p), pool(v1_p)
    ref_rows = {"SPY": SPY, "RULES v2 (live) @10/25 bps pooled": V2,
                "RULES v1 @10/25 bps pooled": V1}

    def halves(r):
        mid = r.index[len(r) // 2]
        return (metrics(r.loc[:mid])["Sharpe"], metrics(r.loc[mid:])["Sharpe"])

    sH1, sH2 = halves(SPY)
    sOOS = metrics(SPY.loc[OOS_START:])
    v2H1, v2H2 = halves(V2)
    v1H1, v1H2 = halves(V1)
    P(f"\n      4b bars off the pooled SPY: H1 > {sH1:.3f}, H2 > {sH2:.3f}, "
      f"OOS Sharpe > {sOOS['Sharpe']:.3f}, |MaxDD| <= {abs(metrics(SPY)['MaxDD'])*0.6:.2%}, "
      f"CAGR >= {metrics(SPY)['CAGR']*0.7:.2%}")
    P(f"\n  {'book':34s} {'CAGR':>7s} {'Shrp':>6s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"{'oCAGR':>7s} {'oShrp':>6s} {'oMaxDD':>8s} {'4a v2':>6s} {'4a v1':>6s} {'4b':>5s} "
      f"{'failing':>22s}")
    kp = []
    for name, r in list(pooled.items()) + list(ref_rows.items()):
        m = metrics(r)
        o = metrics(r.loc[OOS_START:])
        h1, h2 = halves(r)
        is_ref = name in ref_rows
        a2 = (not is_ref) and h1 > v2H1 and h2 > v2H2 and abs(m["MaxDD"]) <= abs(metrics(V2)["MaxDD"])
        a1 = (not is_ref) and h1 > v1H1 and h2 > v1H2 and abs(m["MaxDD"]) <= abs(metrics(V1)["MaxDD"])
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
        P(f"  {name:34s} {m['CAGR']:7.2%} {m['Sharpe']:6.3f} {m['MaxDD']:8.2%} {h1:6.3f} "
          f"{h2:6.3f} {o['CAGR']:7.2%} {o['Sharpe']:6.3f} {o['MaxDD']:8.2%} "
          f"{('-' if is_ref else str(a2)):>6s} {('-' if is_ref else str(a1)):>6s} "
          f"{('-' if is_ref else str(b4)):>5s} {('-' if is_ref else '|'.join(fails) or 'none'):>22s}")
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


def main():
    t0 = time.time()
    P(f"# Idea 446 — re-read-the-195-base-controlled-instances-against-their-OWN-unselected-arm")
    P(f"# lane C, {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}, seed {SEED}\n")
    P(__doc__.split("Deterministic")[0].split("PRE-REGISTERED")[1][:0] or "", )
    W, CL_S, CL_B = premise_audit()
    RC, CELLS = recover(W)
    S, F, B = verdict_move(CELLS, RC)
    ref, LG, RET = run_live()
    WF = live_vocabularies(ref, LG, RET)
    KP = keep_paths(ref, LG, RET, WF)
    P(f"\n\n[done in {time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
