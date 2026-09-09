#!/usr/bin/env python3
"""Idea 278 - "do-CLASSIFIER-selectors-behave-differently-from-ARGMAX-selectors" (lane B, 2026-09-09).

QUESTION (from the queue, verbatim)
-----------------------------------
    idea 271's CSEL is one of the few selectors in the record that BEATS do-nothing out of
    sample (+0.0476 of Sharpe over EWALL) while LOSING on the full sample, the opposite shape
    to the argmax choosers in idea 229's pool.  Re-classify every selector in that pool by
    whether it maximises an IS metric or thresholds a fitted probability, and test whether the
    two classes have different OOS expectancy.

Why this is not idea 229 Q3 again
---------------------------------
Idea 229 Q3 published FIVE name-classes with per-class instance-block CIs and read
"overlapping CIs" as "not separable".  Two marginal CIs overlapping is not a test of a
difference, and the five classes cut the pool along the selector's *name*, not along its
*mechanism*.  This run does three things Q3 did not:
    (1) collapses the record's name-classes onto the queue's declared MECHANISM axis
        (ARGMAX vs CLASSIFIER) and publishes the crosswalk before any number is read;
    (2) bootstraps the DIFFERENCE ARGMAX - CLASSIFIER directly, so the CI is on the quantity
        the queue asks about;
    (3) prices the obvious confound.  A CLASSIFIER can ABSTAIN - hold the control arm - and an
        abstained cell contributes a margin of exactly zero.  A class that abstains often has
        its mean shrunk toward zero and its variance compressed, which reads as "different
        expectancy" while being pure inactivity (cf. idea 506's minimum-activity concern).
        Every table is therefore repeated on the ACTIVE subset (|margin| > 1e-9).

The declared mechanism map (fixed before any number in this run was read)
------------------------------------------------------------------------
    ARGMAX      the pick is the arm that maximises an IS-estimated PERFORMANCE metric over the
                ladder.  Record classes: IS-SHARPE, IS-CAGR, SHRUNK-FIT (a shrunk estimate is
                still argmaxed).
    CLASSIFIER  the pick is set by a THRESHOLD on a fitted statistic that is not itself the
                objective - a fitted probability, an IS margin gate, a sign/clause test - and
                the selector may ABSTAIN back onto the control.  Record classes: GATED, ABSTAIN.
    HELD OUT    RANDOM (not a selector, it is a null), OTHER (mode/incumbent, no mechanism),
                ORACLE (already excluded by the parent's census).
Idea 271's CSEL - "narrowest n whose fitted reversal probability is below the threshold" - is
the archetype of CLASSIFIER and is why the queue asks.

PART A - the record.  idea 229's `census()` is IMPORTED and re-run, not re-derived, so its
published counts reproduce inside this run and any divergence is visible.

PART B - out of corpus, live prices, PROTOCOL rule 8.  idea 229's 36-cell live corpus
(3 panels x 2 cost rungs x 6 pre-registered dials, choice on IS <= 2016-12-31 only, 2017-2026
read once) is re-run through its own `run_live()`, and a REAL classifier in idea 271's shape is
built on it:
    inner split of the IS window only - FIT 2009-01-01..2012-12-31, LABEL 2013-01-01..2016-12-31
    features (both from the FIT window alone): d_is_sharpe = arm Sharpe - incumbent Sharpe, and
        step = |ladder index - incumbent index|
    label   1 if the arm beats the incumbent's Sharpe on the LABEL window
    model   logistic regression, hand-rolled IRLS, deterministic, fitted ONCE on all cells
    decide  features recomputed on the FULL IS window; take the highest-phat arm among those
            with phat >= p*, else ABSTAIN onto the incumbent.  The OOS window is read once.
The ARGMAX comparand is the parent's S1 (IS-Sharpe argmax) and the control is S0 (the dial's
declared incumbent), both unchanged.

TUNED PARAMETERS (PROTOCOL rule 4: at most two)
    P1  the census vocabulary, STRICT | BROAD                (Part A)
    P2  the classifier threshold p*, 7 rungs 0.50 .. 0.90    (Part B)
ALL grid points are printed.  The bootstrap block (cell/instance/file) is a resampling axis,
not a choice: all three are published, with the instance block declared in advance as the
headline.  The 25 bps rung is the parent's robustness axis, carried unchanged.

KEEP paths, both evaluated on the pooled live books
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2 (the v1 column
        is carried for continuity with the pre-2026-09-06 record).
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

SURVIVORSHIP: the broad and small panels are CURRENT constituents (research/universe_broad.json,
data/SMALL_PANEL_README.md), inherited whole from the parent corpus.  The bias inflates every
book on those panels equally; this run reads only DIFFERENCES between selectors on the same
panel, which is the comparison the bias leaves usable.

Deterministic (seed 278000), standalone, no network.
Writes .console.txt .classes.csv .diff.csv .livegrid.csv .walkforward.csv .grid.csv .keeppaths.csv
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import metrics                                            # noqa: E402

STEM = "2026-09-09_do-CLASSIFIER-selectors-behave-differently-from-ARGMAX-selectors_B"
OUT = ROOT / "research" / "backtests"
SEED = 278000
B_BOOT = 2000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 500)
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


# idea 229's script, imported verbatim.  Its STEM and LOG are redirected so its writers land on
# THIS run's files and its P() lands in this console; nothing of the parent's is overwritten.
M229 = _load(OUT / "2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud.py",
             "i229")
M229.STEM = STEM
M229.LOG = LOG
H, C = M229.H, M229.C
IS_END, OOS_START = M229.IS_END, M229.OOS_START
FIT_END, LAB_START = "2012-12-31", "2013-01-01"

# ============================================================ the declared mechanism map (P1-free)
MECH = {"IS-SHARPE": "ARGMAX", "IS-CAGR": "ARGMAX", "SHRUNK-FIT": "ARGMAX",
        "GATED": "CLASSIFIER", "ABSTAIN": "CLASSIFIER",
        "RANDOM": "HELD-OUT", "OTHER": "HELD-OUT", "ORACLE": "HELD-OUT"}
PSTARS = [0.50, 0.55, 0.60, 0.65, 0.70, 0.80, 0.90]      # tuned parameter 2, all reported


# =================================================================== PART A helpers
def mech_stats(CL, subset_name):
    """Per-mechanism pooled statistics, including the inactivity diagnostic."""
    rows = []
    for mech, d in CL.groupby("mech"):
        inst = d.groupby("instance").margin.mean()
        rows.append(dict(mech=mech, cells=len(d), instances=d.instance.nunique(),
                         files=d.file.nunique(), cell_mean=d.margin.mean(),
                         inst_mean=inst.mean(), median=d.margin.median(),
                         win_rate=float((d.margin > 0).mean()),
                         abs_mean=float(d.margin.abs().mean()),
                         zero_share=float((d.margin.abs() <= 1e-9).mean()),
                         sd=float(d.margin.std(ddof=1))))
    R = pd.DataFrame(rows).sort_values("cells", ascending=False)
    R.insert(0, "subset", subset_name)
    return R


def boot_diff(CL, block, B=B_BOOT, seed_off=0):
    """Bootstrap the DIFFERENCE ARGMAX - CLASSIFIER, resampling each class independently
    within the declared block.  Returns (mean, lo, hi, P(diff<0))."""
    rng = np.random.default_rng(SEED + 101 + seed_off)
    draws = np.empty(B)
    pools = {}
    for mech in ("ARGMAX", "CLASSIFIER"):
        d = CL[CL.mech == mech]
        if not len(d):
            return np.nan, np.nan, np.nan, np.nan
        pools[mech] = ([d.margin.values] if block == "cell"
                       else [np.asarray(v) for v in d.groupby(block).margin.apply(list)])
    for i in range(B):
        vals = {}
        for mech, g in pools.items():
            if block == "cell":
                v = g[0]
                vals[mech] = v[rng.integers(0, len(v), len(v))].mean()
            else:
                pick = rng.integers(0, len(g), len(g))
                vals[mech] = np.mean(np.concatenate([g[j] for j in pick]))
        draws[i] = vals["ARGMAX"] - vals["CLASSIFIER"]
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return float(draws.mean()), float(lo), float(hi), float((draws < 0).mean())


def part_a():
    P("\n" + "=" * 118)
    P("PART A - THE RECORD.  idea 229's census() re-run, then collapsed onto the MECHANISM axis")
    P("=" * 118)
    P("  declared map (fixed before any number below was read):")
    for k, v in MECH.items():
        P(f"      {k:12s} -> {v}")
    P("  RANDOM and OTHER are HELD OUT: a null and an incumbent are not selection mechanisms.")

    CL = {}
    for vocab in ("STRICT", "BROAD"):
        CE, cl = M229.census(vocab)
        M229.report_census(CE, cl, vocab)
        cl = cl.assign(mech=cl.cls.map(MECH).fillna("HELD-OUT"))
        CL[vocab] = cl
        P(f"      crosswalk (cells): " + ", ".join(
            f"{a}->{b} {n}" for (a, b), n in
            cl.groupby(["cls", "mech"]).size().sort_values(ascending=False).items()))

    tabs, diffs = [], []
    for vocab in ("STRICT", "BROAD"):
        full = CL[vocab][CL[vocab].mech != "HELD-OUT"]
        act = full[full.margin.abs() > 1e-9]
        for nm, sub in (("ALL", full), ("ACTIVE (|margin|>0)", act)):
            T = mech_stats(sub, nm); T.insert(0, "vocab", vocab)
            P(f"\n  vocabulary {vocab}, subset {nm}:")
            P(f"      {'mech':11s} {'cells':>6s} {'inst':>5s} {'files':>6s} {'cell mean':>10s} "
              f"{'inst mean':>10s} {'win rate':>9s} {'mean |m|':>9s} {'zero share':>11s} {'sd':>8s}")
            for _, r in T.iterrows():
                P(f"      {r.mech:11s} {r.cells:6d} {r.instances:5d} {r.files:6d} "
                  f"{r.cell_mean:+10.5f} {r.inst_mean:+10.5f} {r.win_rate:9.1%} "
                  f"{r.abs_mean:9.5f} {r.zero_share:11.1%} {r.sd:8.5f}")
            tabs.append(T)
            for block in ("cell", "instance", "file"):
                m, lo, hi, pn = boot_diff(sub, block, seed_off=len(nm) + len(vocab) + len(block))
                sep = "SEPARABLE" if (lo > 0 or hi < 0) else "not separable"
                P(f"      DIFF ARGMAX-CLASSIFIER, {block:8s} block: {m:+.5f}  95% CI "
                  f"[{lo:+.5f}, {hi:+.5f}]  P(<0) {pn:5.1%}   {sep}")
                diffs.append(dict(vocab=vocab, subset=nm, block=block, diff=m, lo=lo, hi=hi,
                                  p_neg=pn, separable=bool(lo > 0 or hi < 0)))
    TAB = pd.concat(tabs); DIF = pd.DataFrame(diffs)
    TAB.to_csv(OUT / f"{STEM}.classes.csv", index=False)
    DIF.to_csv(OUT / f"{STEM}.diff.csv", index=False)
    return CL, TAB, DIF


# =================================================================== PART B - the live classifier
def logistic_fit(X, y, iters=60, ridge=1e-4):
    """Deterministic IRLS with a small ridge.  X already carries an intercept column."""
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(X @ b, -30, 30)))
        w = np.clip(p * (1 - p), 1e-6, None)
        z = X @ b + (y - p) / w
        A = X.T @ (X * w[:, None]) + ridge * np.eye(X.shape[1])
        b_new = np.linalg.solve(A, X.T @ (w * z))
        if np.max(np.abs(b_new - b)) < 1e-9:
            b = b_new
            break
        b = b_new
    return b


def sharpe_win(r, lo=None, hi=None):
    s = r.loc[lo:hi] if (lo or hi) else r
    return float(metrics(s)["Sharpe"]) if len(s) > 20 else np.nan


def build_features(RET):
    """One row per (panel, cost, dial, arm): FIT-window and full-IS features, LABEL-window
    outcome.  The incumbent is the dial's declared default; it is the reference, never a row
    the classifier can 'pick' by threshold (it is the abstention target)."""
    rows = []
    for (pk, cost, dial, arm), r in RET.items():
        ladder, dflt = M229.DIALS[dial]
        ref = RET[(pk, cost, dial, dflt)]
        rows.append(dict(
            panel=pk, cost=cost, dial=dial, arm=arm, is_default=(arm == dflt),
            step=abs(ladder.index(arm) - ladder.index(dflt)), ladder_len=len(ladder),
            d_fit=sharpe_win(r, None, FIT_END) - sharpe_win(ref, None, FIT_END),
            d_lab=sharpe_win(r, LAB_START, IS_END) - sharpe_win(ref, LAB_START, IS_END),
            d_is=sharpe_win(r, None, IS_END) - sharpe_win(ref, None, IS_END),
            IS_Sharpe=sharpe_win(r, None, IS_END),
            OOS_Sharpe=sharpe_win(r, OOS_START, None)))
    return pd.DataFrame(rows)


def part_b(ref, LG, RET, WF):
    P("\n" + "=" * 118)
    P("PART B - OUT OF CORPUS, LIVE PRICES.  A REAL fitted-probability classifier (idea 271's")
    P("         CSEL shape) against idea 229's IS-Sharpe ARGMAX on the same 36 cells.")
    P("=" * 118)
    F = build_features(RET)
    tr = F[(~F.is_default) & np.isfinite(F.d_fit) & np.isfinite(F.d_lab)]
    X = np.column_stack([np.ones(len(tr)), tr.d_fit.values,
                         tr.step.values / tr.ladder_len.values])
    y = (tr.d_lab.values > 0).astype(float)
    b = logistic_fit(X, y)
    P(f"\n  classifier fitted on the INNER IS split only: FIT <= {FIT_END} supplies the features,")
    P(f"  {LAB_START}..{IS_END} supplies the label.  {len(tr)} non-incumbent arms, base rate "
      f"{y.mean():.3f}.")
    P(f"      logit(p) = {b[0]:+.4f} {b[1]:+.4f}*d_fit_sharpe {b[2]:+.4f}*(step/ladder_len)")
    ph = 1.0 / (1.0 + np.exp(-np.clip(X @ b, -30, 30)))
    P(f"      in-fit accuracy at 0.50 {float(((ph > 0.5) == (y > 0)).mean()):.3f} "
      f"(majority base {max(y.mean(), 1-y.mean()):.3f})")

    # decision features: recomputed on the FULL IS window, OOS never touched
    F["phat"] = np.nan
    nd = (~F.is_default) & np.isfinite(F.d_is)
    Xd = np.column_stack([np.ones(int(nd.sum())), F.loc[nd, "d_is"].values,
                          F.loc[nd, "step"].values / F.loc[nd, "ladder_len"].values])
    F.loc[nd, "phat"] = 1.0 / (1.0 + np.exp(-np.clip(Xd @ b, -30, 30)))

    P(f"\n  (i) TUNED PARAMETER 2 - the threshold p*.  Every rung, all 36 cells, OOS read once.")
    P(f"      the LABEL-window column is the only one a pre-registration may read; the OOS")
    P(f"      columns beside it are published for completeness, not to choose on.")
    P(f"      {'p*':>5s} {'picks':>6s} {'abstains':>9s} {'LAB margin':>11s} {'OOS margin':>11s} "
      f"{'beats S0':>9s} {'vs ARGMAX':>10s}")
    grid, picks_by_p = [], {}
    for ps in PSTARS:
        cells, picks = [], {}
        for _, w in WF.iterrows():
            sub = F[(F.panel == w.panel) & (F.cost == w.cost) & (F.dial == w.dial)]
            cand = sub[(~sub.is_default) & (sub.phat >= ps)]
            pick = str(cand.loc[cand.phat.idxmax(), "arm"]) if len(cand) else str(w.s0)
            picks[(w.panel, w.cost, w.dial)] = pick
            g = sub.set_index("arm")
            cells.append(dict(panel=w.panel, cost=w.cost, dial=w.dial, pick=pick,
                              abstain=(pick == str(w.s0)),
                              lab_margin=float(g.loc[pick, "d_lab"] if pick != str(w.s0) else 0.0),
                              oos_margin=float(g.loc[pick, "OOS_Sharpe"] - g.loc[str(w.s0), "OOS_Sharpe"]),
                              argmax_margin=float(w.margin)))
        D = pd.DataFrame(cells); D.insert(0, "p_star", ps)
        picks_by_p[ps] = picks
        grid.append(D)
        P(f"      {ps:5.2f} {int((~D.abstain).sum()):6d} {int(D.abstain.sum()):9d} "
          f"{D.lab_margin.mean():+11.5f} {D.oos_margin.mean():+11.5f} "
          f"{int((D.oos_margin>0).sum()):5d}/{len(D):<3d} "
          f"{D.oos_margin.mean()-D.argmax_margin.mean():+10.5f}")
    G = pd.concat(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    lab = G.groupby("p_star").lab_margin.mean()
    p_reg = float(lab.idxmax())
    P(f"\n  PRE-REGISTERED p* = {p_reg:.2f} (the rung with the best LABEL-window margin, chosen")
    P(f"  inside the IS window).  Its OOS margin is read once below.")
    D = G[G.p_star == p_reg]
    P(f"      CLASSIFIER @p*={p_reg:.2f}: beats do-nothing in {int((D.oos_margin>0).sum())} of "
      f"{len(D)} cells, mean OOS margin {D.oos_margin.mean():+.5f}, abstains "
      f"{int(D.abstain.sum())}/{len(D)}")
    P(f"      ARGMAX (idea 229 S1):       beats do-nothing in {int((WF.margin>0).sum())} of "
      f"{len(WF)} cells, mean OOS margin {WF.margin.mean():+.5f}, abstains 0/{len(WF)}")
    d = D.oos_margin.values - D.argmax_margin.values
    rng = np.random.default_rng(SEED + 7)
    dr = np.array([d[rng.integers(0, len(d), len(d))].mean() for _ in range(B_BOOT)])
    lo, hi = np.percentile(dr, [2.5, 97.5])
    P(f"      PAIRED difference CLASSIFIER - ARGMAX over the 36 cells: {d.mean():+.5f}, "
      f"95% CI [{lo:+.5f}, {hi:+.5f}], P(<0) {(dr<0).mean():.1%}  "
      f"{'SEPARABLE' if (lo>0 or hi<0) else 'not separable'}")
    act = d[np.abs(D.oos_margin.values) > 1e-12]
    P(f"      on the {len(act)} cells where the classifier did NOT abstain: mean difference "
      f"{act.mean() if len(act) else float('nan'):+.5f}")
    return F, G, p_reg, picks_by_p


def part_b_books(ref, RET, WF, G, p_reg, picks_by_p):
    P("\n  (ii) THE BOOKS, POOLED equal-weight over the 36 cells, and BOTH KEEP paths.")

    def eq(sl):
        return pd.concat(sl, axis=1).fillna(0.0).mean(axis=1)

    argmax = eq([RET[(r.panel, r.cost, r.dial, r["pick"])] for _, r in WF.iterrows()])
    donoth = eq([RET[(r.panel, r.cost, r.dial, r.s0)] for _, r in WF.iterrows()])
    oracle = eq([RET[(r.panel, r.cost, r.dial, r.oos_argmax)] for _, r in WF.iterrows()])
    spy = eq([ref[p]["spy"] for p in M229.PANELS])
    v2 = eq([ref[p]["v2"][10.0] for p in M229.PANELS])
    v1 = eq([ref[p]["v1"][10.0] for p in M229.PANELS])
    bars = H.bars_of(spy)
    P(f"      4b bars off the pooled SPY: H1>{bars['s1']:.3f} H2>{bars['s2']:.3f} "
      f"OOS>{bars['soos']:.3f} |MaxDD|<={0.60*abs(bars['sdd']):.2%} "
      f"CAGR>={0.70*bars['scagr']:.2%}")

    books = []
    for ps in PSTARS:
        pk = picks_by_p[ps]
        books.append((f"CLASSIFIER p*={ps:.2f}" + ("  <- pre-registered" if ps == p_reg else ""),
                      eq([RET[(r.panel, r.cost, r.dial, pk[(r.panel, r.cost, r.dial)])]
                          for _, r in WF.iterrows()])))
    books += [("ARGMAX  IS-Sharpe (idea 229 S1)", argmax),
              ("S0  do nothing (declared defaults)", donoth),
              ("ORACLE (OOS argmax, not a rule)", oracle),
              ("SPY", spy), ("RULES v2 (live) @10bps", v2), ("RULES v1 @10bps", v1)]

    P(f"  {'book':38s} | {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"| {'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} | {'4a v2':>6s} {'4a v1':>6s} "
      f"{'4b':>5s}  failing")
    kp = []
    for nm, r in books:
        cg, sh, dd = M229.csd(r)
        oc, osh, odd = M229.csd(r.loc[OOS_START:])
        h1, h2 = H.halves(r)
        mg = H.margins(r, bars)
        fb = [x for x in ("H1", "H2", "OOS", "DD", "CAGR") if mg[x] <= 0]
        p4a2, p4a1 = H.pass4a(r, v2), H.pass4a(r, v1)
        P(f"  {nm:38s} | {cg:8.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} | {oc:9.2%} "
          f"{osh:7.3f} {odd:8.2%} | {str(p4a2):>6s} {str(p4a1):>6s} {str(len(fb)==0):>5s}  "
          f"{'|'.join(fb) if fb else '-'}")
        kp.append(dict(book=nm, CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2, OOS_CAGR=oc,
                       OOS_Sharpe=osh, OOS_MaxDD=odd, pass4a_v2=p4a2, pass4a_v1=p4a1,
                       pass4b=(len(fb) == 0), failing="|".join(fb)))
    K = pd.DataFrame(kp)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    cls_row = K[K.book.str.startswith(f"CLASSIFIER p*={p_reg:.2f}")].iloc[0]
    arg_row = K[K.book.str.startswith("ARGMAX")].iloc[0]
    s0_row = K[K.book.str.startswith("S0")].iloc[0]
    P(f"\n      pooled OOS Sharpe: CLASSIFIER {cls_row.OOS_Sharpe:.4f}  ARGMAX "
      f"{arg_row.OOS_Sharpe:.4f}  S0 {s0_row.OOS_Sharpe:.4f}  "
      f"(CLASSIFIER - ARGMAX {cls_row.OOS_Sharpe-arg_row.OOS_Sharpe:+.4f}, "
      f"CLASSIFIER - S0 {cls_row.OOS_Sharpe-s0_row.OOS_Sharpe:+.4f})")
    P(f"      pooled OOS CAGR:   CLASSIFIER {cls_row.OOS_CAGR:.2%}  ARGMAX "
      f"{arg_row.OOS_CAGR:.2%}  S0 {s0_row.OOS_CAGR:.2%}")
    return K


# ============================================================================== main
def main():
    t0 = time.time()
    # this run writes its own *.walkforward.csv (PART B); remove any copy from a previous run so
    # the PART A census can never read this script's own output back as record evidence.
    own = OUT / f"{STEM}.walkforward.csv"
    if own.exists():
        own.unlink()
    P("=" * 118)
    P("IDEA 278 - do-CLASSIFIER-selectors-behave-differently-from-ARGMAX-selectors  (lane B, 2026-09-09)")
    P("=" * 118)
    P(__doc__.split("QUESTION (from the queue, verbatim)")[1].split("Deterministic")[0].strip())

    CL, TAB, DIF = part_a()

    ref, LG, RET = M229.run_live()
    WF = M229.live_walkforward(ref, LG, RET)
    F, G, p_reg, picks_by_p = part_b(ref, LG, RET, WF)
    K = part_b_books(ref, RET, WF, G, p_reg, picks_by_p)

    P("\n" + "=" * 118)
    P("ANSWERS")
    P("=" * 118)
    s = TAB[(TAB.vocab == "STRICT") & (TAB.subset == "ALL")].set_index("mech")
    for m in ("ARGMAX", "CLASSIFIER"):
        if m in s.index:
            r = s.loc[m]
            P(f"  A1 {m:11s} STRICT/ALL: {int(r.cells)} cells / {int(r.instances)} instances "
              f"/ {int(r.files)} files, cell mean {r.cell_mean:+.5f}, instance mean "
              f"{r.inst_mean:+.5f}, win {r.win_rate:.1%}, mean |margin| {r.abs_mean:.5f}, "
              f"exactly-zero {r.zero_share:.1%}")
    sep = DIF[DIF.separable]
    P(f"  A2 DIFFERENCE ARGMAX-CLASSIFIER separable at {len(sep)} of {len(DIF)} grid points"
      + (": " + ", ".join(f"{r.vocab}/{r.subset}/{r.block} {r['diff']:+.5f}"
                          for _, r in sep.iterrows()) if len(sep) else " - NONE"))
    d0 = DIF[(DIF.vocab == "STRICT") & (DIF.subset == "ALL") & (DIF.block == "instance")].iloc[0]
    P(f"     headline (STRICT/ALL/instance block, declared in advance): {d0['diff']:+.5f} "
      f"95% CI [{d0.lo:+.5f}, {d0.hi:+.5f}]")
    Dg = G[G.p_star == p_reg]
    P(f"  A3 LIVE, out of corpus, p*={p_reg:.2f}: classifier mean OOS margin "
      f"{Dg.oos_margin.mean():+.5f} vs argmax {Dg.argmax_margin.mean():+.5f}; "
      f"abstains {int(Dg.abstain.sum())}/{len(Dg)}")
    P(f"     every p* rung's OOS margin: " + ", ".join(
        f"{p:.2f} {G[G.p_star==p].oos_margin.mean():+.5f}" for p in PSTARS))
    P(f"  A4 KEEP paths on the pooled live books: 4a-v2 {int(K.pass4a_v2.sum())}/{len(K)}, "
      f"4a-v1 {int(K.pass4a_v1.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}")
    P(f"\n  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
