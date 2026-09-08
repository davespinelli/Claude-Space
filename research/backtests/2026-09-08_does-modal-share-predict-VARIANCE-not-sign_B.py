#!/usr/bin/env python3
"""IDEA 224  does-modal-share-predict-VARIANCE-not-sign   (lane B, 2026-09-08)

THE QUESTION
------------
Idea 219 swept a modal-share FLOOR and killed it: there is no share at which the held-out mode
stops beating the per-book fit, because on the MEAN the mode never stops beating the fit.  But
219's own curve has a second shape its verdict never spoke to.  Binning 219's committed 560
cells by modal share:

    share <= 0.30 :  mean d = +0.0018   mean sd(d) = 0.0403
    0.30 - 0.50   :  mean d = +0.0018   mean sd(d) = 0.0333
    0.50 - 0.70   :  mean d = +0.0181   mean sd(d) = 0.0198
    0.70 - 0.90   :  mean d = +0.0092   mean sd(d) = 0.0065
    share  > 0.90 :  mean d = +0.0009   mean sd(d) = 0.0013

The MEAN is flat-to-noisy in share (219's KILL).  The SPREAD falls 32x across the same axis.
The queue's claim is that share bounds how far a mode can MOVE the answer, i.e. that the
reportable statistic is a share-scaled CONFIDENCE column beside a published mode, not a gate
in front of it.  This run tests that claim and, crucially, tests the two ways it can be empty:

  Q1  GATE / REPRODUCTION.  Rebuild all 560 cells from idea 219's committed ladder.csv.gz
      using its own seeding scheme, and match its committed cells.csv column-for-column
      before any new number is read.  Rebuild its Q4 sweep.csv too.  Stop on any mismatch.
  Q2  THE RAW CURVE.  sd(d) by share decile, threshold-free, with the confounds (n_books,
      distinct ladder points, cost rung, dial view) printed beside it.
  Q3  IS IT THE MODE MOVING, OR THE SAMPLE?  sd(d) has two sources: the half-read MODE moves
      across draws (what share is supposed to govern), and the HELD-OUT BOOK SET moves (which
      exists even at share = 1.00).  Re-run every cell with the mode FORCED to the full-cell
      mode so only the sample moves, and decompose.  If the share curve is the sample term,
      the column is share-scaled in name only.
  Q4  THE FIT AND ITS CONTROLS.  OLS of log sd(d) on share, on log n_books, on distinct, and
      on all three.  Report every coefficient and R2, plus Spearman(share, sd) WITHIN n_books
      terciles so the share effect is not read off the n axis.
  Q5  RULE 8 ON THE COLUMN ITSELF (the meta walk-forward).  A confidence column is a fitted
      object.  Fit it on corpus A and read it on corpus B and vice versa; fit it at 10 bps
      and read it at 5/15/20/25; fit it on the published dial views and read it on idea 218's
      extended ones.  The decision statistic is CALIBRATION: the record publishes ONE seeded
      draw (idea 225: 20.5% of single draws disagree in sign with the settled answer), so ask
      whether  d_1 +- k * sd_hat(share)  covers the cell's settled value at the nominal rate,
      and how WIDE that interval is, against a CONSTANT-width interval fitted the same way.
      A share-scaled column earns its place only if, at matched coverage, it is materially
      narrower than a constant.
  Q6  RULE 8 ON THE BOOKS (PROTOCOL rule 8) AND BOTH KEEP PATHS.  Every cell's arms are real
      books: MODE, per-book IS-Sharpe FIT, INCUMBENT, ORACLE, plus a CONFIDENCE-SHRUNK arm
      that falls back to the incumbent wherever the fitted column says the mode is unreadable.
      Report OOS CAGR / Sharpe / MaxDD against the RULES v2 baseline and SPY, and 4a/4b pass
      counts on every arm at every rung.

DESIGN
------
NO new simulation.  Idea 219's committed `ladder.csv.gz` (36 120 rows = 168 books x 43 dial
points x 5 cost rungs, IS <= 2016-12-31 chooses, OOS >= 2017-01-01 read once) is the input,
and the reproduction gate is that this file rebuilds 219's cells.csv and sweep.csv EXACTLY
from it.  That is a stronger control than re-simulating: it proves the 560 cells this run
reasons over are bit-for-bit the 560 cells the record published, and it inherits idea 219's
own reproduction of ideas 189 and 217 (which it asserted at max |d| 3.553e-15, 0 verdict
mismatches) without re-paying for it.

  A CELL is (corpus, cost rung, dial view, book group), exactly as in 219.
  Within a cell: S = 40 seeded random half-splits, both directions = 80 draws.  Each draw
  reads the mode on the fitting half (and its SHARE) and scores it on the held-out half:
      d = mean over held-out books of  OOS_Sharpe(mode) - OOS_Sharpe(that book's own IS fit)
  219 published mean(d) per cell.  THIS RUN'S OBJECT IS sd(d) OVER THE 80 DRAWS.

  TUNED PARAMETER 1: m_min, the smallest book group admitted as a cell, reported at
                     {8, 12, 20, 40}; headline 12.  Inherited grid from idea 219, not chosen.
  TUNED PARAMETER 2: k, the confidence multiplier in  d_1 +- k * sd_hat, swept over 18 grid
                     points, ALL reported, and subject to rule 8 like any other fitted
                     parameter: k is chosen on the TRAINING cells (smallest grid point
                     reaching the nominal 90% coverage there) and read ONCE on the held-out
                     cells.  A k-free standardised-error statistic is reported beside it so
                     the verdict does not rest on the grid at all.

  Everything else -- the ladder, the corpora, the dial views, the rungs, the IS/OOS split,
  S = 40, the seeds, the model's predictor set (share, log n_books, distinct), the log link,
  the decile bins -- is INHERITED or fixed a priori.

DISCLOSED DESIGN CORRECTION (made after a first pass, before the verdict was read)
----------------------------------------------------------------------------------
The first pass of Q5 (i) capped the k grid at 10 and (ii) read k* off the TEST cells.  Both
were wrong: (i) truncated the answer -- neither model reached 90% coverage anywhere on the
grid, which is a grid artefact, not a finding (idea 218's own verdict on a truncated ladder)
-- and (ii) selected a tuned parameter in-sample, which is exactly what rule 8 forbids.  The
grid now runs to 100 and k is chosen on train only.  The Q2/Q3/Q4 numbers were unaffected and
were not re-read; the k-free z statistic was added so the head-to-head does not depend on the
grid's extent either way.

PRE-REGISTERED PREDICTIONS (written before any Q2+ number below was read)
------------------------------------------------------------------------
  P1  The rebuild matches 219's committed cells.csv on all 560 rows, max |d| < 1e-12, and its
      sweep.csv on all 132 rows.
  P2  sd(d) is monotone decreasing in share over the deciles, and the decrease survives
      conditioning on n_books (Spearman < 0 in all three n terciles).
  P3  The mode-switch term, not the sample term, carries it: the FIXED-MODE control's sd is
      roughly FLAT in share, and total-minus-fixed tracks the raw curve.
  P4  Share beats a constant on log-sd R2 out of corpus, but the CALIBRATED interval is where
      it is decided, and I do NOT predict which way: a 32x sd range is large enough for a
      share-scaled interval to be much narrower at matched coverage, but the record's
      published cells sit overwhelmingly at high share, where sd_hat is small and a single
      draw's error is dominated by terms share does not see.
  P5  The CONFIDENCE-SHRUNK book arm does NOT beat the plain MODE arm OOS.  Idea 219 killed
      the gate on the mean and this run does not resurrect it; a column is a report, not a
      decision.  No KEEP is expected from either path.

HONEST LIMITS
-------------
  * Cells are NOT independent: they share books (a k-group is a subset of ALL), share
    simulations across the 5 rungs (one 0 bps run, derived), and share parents.  Every t and
    CI here is over correlated units and its nominal size is optimistic.  The block bootstrap
    resamples whole (corpus, dial, group) blocks; no p-value here is a p-value on a fresh
    sample.
  * sd(d) is a RESAMPLING sd over 80 correlated half-splits of the SAME finite corpus, not
    the sd of a fresh-sample statistic.  It measures how far the published number could have
    moved had a different split been drawn -- which is exactly the quantity a confidence
    column beside a published mode is claiming to bound -- and nothing more.
  * At share = 1.00 the mode cannot move, so sd(d) there is a pure held-out-sample term.  The
    curve's low-share end is where BOTH terms are live; Q3 exists because of this.
  * Survivorship: idea 175's SMALL panel and idea 171's U56/B136 are current constituents.
  * Idea 144: a re-dialled book is the same book.  Nothing here is a new signal and nothing
    is proposed as a book.
  * NO new prices are read for the cell work; the only fresh simulation is the RULES v2 /
    SPY OOS anchor in Q6, on research/baseline.py's own universe.

Deterministic, standalone.  Writes .console.txt, .cells.csv, .curve.csv, .decomp.csv,
.fit.csv, .calib.csv, .kstar.csv, .walkforward.csv, .keep.csv.
"""
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_does-modal-share-predict-VARIANCE-not-sign_B"
OUT = ROOT / "research" / "backtests"
P219 = "2026-09-06_what-modal-share-makes-a-mode-writable_cloud"

# ---- inherited from idea 219, verbatim.  Nothing in this block is chosen by this run.
RUNGS = [5, 10, 15, 20, 25]
BASE_RUNG = 10
S_SPLITS = 40
M_MINS = [8, 12, 20, 40]                 # TUNED PARAMETER 1, all reported
M_MIN_HEADLINE = 12
TAU_GRID = [round(0.20 + 0.025 * i, 3) for i in range(33)]
SPLIT_SEED = 219_500
BOOT_SEED = 224_700
N_BOOT = 2000
PHYS = {
    "GROSS":   [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00],
    "N":       [3, 5, 8, 10, 15, 20, 25, 30, 40, 50],
    "BAND":    [0.00, 0.02, 0.03, 0.05, 0.08, 0.10, 0.12, 0.15],
    "CADENCE": ["D", "W", "M", "Q"],
    "SLEEVE":  [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
}
VIEWS = {
    "GROSS":   ("GROSS",   PHYS["GROSS"]),
    "N":       ("N",       PHYS["N"]),
    "BAND":    ("BAND",    [0.00, 0.02, 0.03, 0.05, 0.08]),
    "BAND+":   ("BAND",    PHYS["BAND"]),
    "CADENCE": ("CADENCE", PHYS["CADENCE"]),
    "SLEEVE":  ("SLEEVE",  [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]),
    "SLEEVE+": ("SLEEVE",  PHYS["SLEEVE"]),
}
VIEW_ORDER = ["GROSS", "N", "BAND", "BAND+", "CADENCE", "SLEEVE", "SLEEVE+"]
PUBLISHED_VIEWS = ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"]
INC = {"GROSS": 0.75, "N": 5, "BAND": 0.00, "CADENCE": "W", "SLEEVE": 0.00}
OOS_START = "2017-01-01"

# ---- this run's own grid.  TUNED PARAMETER 2.
K_GRID = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.50, 3.00, 4.00, 6.00, 10.00,
          15.0, 25.0, 40.0, 60.0, 100.0]
NOMINAL = 0.90                            # nominal coverage, fixed a priori (not swept)
EPS = 1e-6                                # log-link floor, fixed a priori

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)
_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def tstat(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().to_numpy()
    rb = pd.Series(b[m]).rank().to_numpy()
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def ols(X, y):
    """Plain least squares with an explicit intercept column already in X.  Returns
    (coefs, R2, residual sd)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    ss_res = float(((y - fit) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return beta, r2, float(np.sqrt(ss_res / max(len(y) - X.shape[1], 1)))


def groups_of(names):
    """Idea 219's groups_of, verbatim: ALL, every seeded sub-panel family, and family x k."""
    out = {"ALL": list(names)}
    fams = {}
    for nm in names:
        if "k" in nm and "d" in nm.rsplit("k", 1)[-1]:
            fam, rest = nm.rsplit("k", 1)
            k = rest.split("d")[0]
            fams.setdefault(fam, []).append(nm)
            fams.setdefault(f"{fam}k{k}", []).append(nm)
    for key, v in fams.items():
        out[key] = sorted(v)
    return {k: v for k, v in out.items() if len(v) >= min(M_MINS)}


def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 224  does-modal-share-predict-VARIANCE-not-sign   (lane B, 2026-09-08)")
    P("Object: sd(d) over 80 seeded half-split draws per cell, as a function of the modal")
    P("share.  Idea 219 killed the share FLOOR on mean(d); this asks whether share prices the")
    P("SPREAD, i.e. whether a share-scaled CONFIDENCE column belongs beside a published mode.")
    P("Costs 5/10/15/20/25 bps (10 the anchor), t+1 execution, IS <= 2016-12-31, OOS >= 2017.")
    P("Two tuned parameters: m_min (4 values) and the confidence multiplier k (13 values).")
    P("=" * 118)

    # ================================================================= Q1 GATE / REPRODUCTION
    P("\n" + "=" * 118)
    P("Q1  GATE.  Rebuild idea 219's 560 cells from its committed ladder.csv.gz with its own")
    P("    seeding scheme, and match its committed cells.csv and sweep.csv before reading any")
    P("    new number.  A mismatch stops the run.")
    P("=" * 118)
    lad = pd.read_csv(OUT / f"{P219}.ladder.csv.gz")
    C219 = pd.read_csv(OUT / f"{P219}.cells.csv")
    S219 = pd.read_csv(OUT / f"{P219}.sweep.csv")
    P(f"  ladder  {lad.shape[0]} rows x {lad.shape[1]} cols   "
      f"(expected 36120 = 168 books x 43 points x 5 rungs)")
    assert lad.shape[0] == 36120, "idea 219's ladder is not the committed 36120 rows"
    assert len(C219) == 560 and len(S219) == 132

    lad_s = lad.astype({"point": str})
    NAMES = {}
    for tag in ("A", "B"):
        sub = lad_s[lad_s.corpus == tag]
        NAMES[tag] = list(dict.fromkeys(sub.book))          # first-appearance = build order
    P(f"  corpus A {len(NAMES['A'])} books, corpus B {len(NAMES['B'])} books;  "
      f"panels {sorted(lad.parent.unique())}")

    PACK = {}
    for tag in ("A", "B"):
        for cb in RUNGS:
            sub = lad_s[(lad_s.corpus == tag) & (lad_s.cost_bps == cb)]
            for view in VIEW_ORDER:
                phys, pts = VIEWS[view]
                spts = [str(p) for p in pts]
                s = sub[(sub.dial == phys) & (sub.point.isin(spts))]
                piv_is = s.pivot(index="book", columns="point", values="IS_Sharpe")
                piv_o = s.pivot(index="book", columns="point", values="OOS_Sharpe")
                piv_oc = s.pivot(index="book", columns="point", values="OOS_CAGR")
                piv_od = s.pivot(index="book", columns="point", values="OOS_MaxDD")
                piv_m = s.pivot(index="book", columns="point", values="OOS_margin")
                piv_4a = s.pivot(index="book", columns="point", values="fail4a")
                piv_4b = s.pivot(index="book", columns="point", values="fail4b")
                bk = [n for n in NAMES[tag] if n in piv_is.index]
                piv_is = piv_is.loc[bk, spts]
                PACK[(tag, cb, view)] = dict(
                    books=bk, pts=pts, spts=spts,
                    IS=piv_is.to_numpy(float),
                    OOS=piv_o.loc[bk, spts].to_numpy(float),
                    OOSC=piv_oc.loc[bk, spts].to_numpy(float),
                    OOSD=piv_od.loc[bk, spts].to_numpy(float),
                    MAR=piv_m.loc[bk, spts].to_numpy(float),
                    F4A=piv_4a.loc[bk, spts].to_numpy(object),
                    F4B=piv_4b.loc[bk, spts].to_numpy(object),
                    sel=np.nanargmax(piv_is.to_numpy(float), axis=1),
                    orac=np.nanargmax(piv_o.loc[bk, spts].to_numpy(float), axis=1),
                    inc=(spts.index(str(INC[phys])) if str(INC[phys]) in spts else 0))

    GRP = {tag: groups_of(NAMES[tag]) for tag in ("A", "B")}
    for tag in ("A", "B"):
        P(f"  corpus {tag} groups: " + ", ".join(f"{k}({len(v)})" for k, v in GRP[tag].items()))

    crows, DRAWS = [], {}
    for tag in ("A", "B"):
        for cb in RUNGS:
            for view in VIEW_ORDER:
                pk = PACK[(tag, cb, view)]
                pos = {n: i for i, n in enumerate(pk["books"])}
                for gname, members in GRP[tag].items():
                    ix = np.array([pos[n] for n in members if n in pos])
                    if len(ix) < min(M_MINS):
                        continue
                    sel = pk["sel"][ix]
                    cnt = np.bincount(sel, minlength=len(pk["pts"]))
                    full_mode = int(cnt.argmax())
                    full_share = float(cnt.max() / len(ix))
                    rng = np.random.default_rng(
                        SPLIT_SEED + zlib.crc32(
                            f"{tag}|{cb}|{view}|{gname}".encode()) % 10_000_019)
                    shares, ds, dm, stab, dfix, sw = [], [], [], [], [], []
                    for _ in range(S_SPLITS):
                        perm = rng.permutation(len(ix))
                        h = len(ix) // 2
                        halves_ = [(perm[:h], perm[h:]), (perm[h:], perm[:h])]
                        modes_ = []
                        for fit, held in halves_:
                            c2 = np.bincount(sel[fit], minlength=len(pk["pts"]))
                            md = int(c2.argmax())
                            modes_.append(md)
                            sh = float(c2.max() / len(fit))
                            rows_h = ix[held]
                            own = pk["OOS"][rows_h, pk["sel"][rows_h]]
                            d = float(np.mean(pk["OOS"][rows_h, md] - own))
                            dmg = float(np.mean(pk["MAR"][rows_h, md]
                                                - pk["MAR"][rows_h, pk["sel"][rows_h]]))
                            # ---- Q3 control: mode FORCED to the full-cell mode, so only the
                            #      held-out SAMPLE varies across draws.
                            dfx = float(np.mean(pk["OOS"][rows_h, full_mode] - own))
                            shares.append(sh)
                            ds.append(d)
                            dm.append(dmg)
                            dfix.append(dfx)
                            sw.append(md != full_mode)
                        stab.append(modes_[0] == modes_[1])
                    key = (tag, cb, view, gname)
                    DRAWS[key] = dict(share=np.array(shares), d=np.array(ds),
                                      dfix=np.array(dfix), switch=np.array(sw))
                    crows.append(dict(
                        corpus=tag, cost_bps=cb, dial=view, group=gname, n_books=len(ix),
                        full_mode=str(pk["pts"][full_mode]), full_share=full_share,
                        distinct=int((cnt > 0).sum()),
                        share_mean=float(np.mean(shares)), share_sd=float(np.std(shares)),
                        d_mean=float(np.mean(ds)), d_median=float(np.median(ds)),
                        d_sd=float(np.std(ds)), win=float(np.mean(np.array(ds) > 0)),
                        dmargin_mean=float(np.mean(dm)),
                        mode_stable=float(np.mean(stab)),
                        published=(cb == BASE_RUNG and gname == "ALL"
                                   and view in PUBLISHED_VIEWS),
                        # ---- new columns, this run's object
                        dfix_mean=float(np.mean(dfix)), dfix_sd=float(np.std(dfix)),
                        switch_rate=float(np.mean(sw)), n_draws=len(ds)))
    CELLS = pd.DataFrame(crows)

    key_cols = ["corpus", "cost_bps", "dial", "group"]
    num_cols = ["n_books", "full_share", "distinct", "share_mean", "share_sd",
                "d_mean", "d_median", "d_sd", "win", "dmargin_mean", "mode_stable"]
    m = C219.merge(CELLS, on=key_cols, suffixes=("_c", ""))
    ok_rows = len(m) == 560 and len(CELLS) == 560
    dmax = max(float((m[f"{c}_c"] - m[c]).abs().max()) for c in num_cols)
    mode_mismatch = int((m.full_mode_c.astype(str) != m.full_mode.astype(str)).sum())
    P(f"\n  cells rebuilt: {len(CELLS)}  (219 committed {len(C219)});  matched rows {len(m)}")
    P(f"  max |d| over {len(num_cols)} shared numeric columns = {dmax:.3e};  "
      f"full_mode mismatches = {mode_mismatch}")

    srows = []
    for mm in M_MINS:
        Cm = CELLS[CELLS.n_books >= mm]
        for tau in TAU_GRID:
            a, b = Cm[Cm.share_mean >= tau], Cm[Cm.share_mean < tau]
            srows.append(dict(
                m_min=mm, tau=tau, n_above=len(a), n_below=len(b),
                d_above=float(a.d_mean.mean()) if len(a) else np.nan,
                d_below=float(b.d_mean.mean()) if len(b) else np.nan,
                win_above=float(np.mean(a.d_mean > 0)) if len(a) else np.nan,
                win_below=float(np.mean(b.d_mean > 0)) if len(b) else np.nan,
                t_above=tstat(a.d_mean.to_numpy()) if len(a) > 2 else np.nan,
                t_below=tstat(b.d_mean.to_numpy()) if len(b) > 2 else np.nan))
    SW = pd.DataFrame(srows)
    ms = S219.merge(SW, on=["m_min", "tau"], suffixes=("_c", ""))
    scols = ["n_above", "n_below", "d_above", "d_below", "win_above", "win_below",
             "t_above", "t_below"]
    sdmax = max(float((ms[f"{c}_c"] - ms[c]).abs().max()) for c in scols)
    P(f"  sweep rebuilt: {len(SW)} rows (219 committed {len(S219)}); matched {len(ms)}; "
      f"max |d| over {len(scols)} columns = {sdmax:.3e}")

    repro_ok = ok_rows and dmax < 1e-12 and mode_mismatch == 0 and len(ms) == 132 \
        and sdmax < 1e-12
    P(f"  REPRODUCTION {'PASS' if repro_ok else 'FAIL'}   ({time.time() - t0:.0f}s)")
    if not repro_ok:
        P("\n*** idea 219's cells do not rebuild from its own ladder.  Stopping before any new "
          "number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    CELLS.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    P("\n  The 10 PUBLISHED cells, with idea 219's mean beside THIS run's spread:")
    P(f"  {'corpus':7s} {'dial':9s} {'mode':>7s} {'share':>7s} {'d_mean':>9s} {'sd(d)':>9s} "
      f"{'sd/|mean|':>10s} {'switch':>8s} {'n':>5s}")
    for _, r in CELLS[CELLS.published].sort_values(["corpus", "dial"]).iterrows():
        ratio = r.d_sd / abs(r.d_mean) if r.d_mean != 0 else np.inf
        P(f"  {r.corpus:7s} {r.dial:9s} {r.full_mode:>7s} {r.full_share:7.1%} "
          f"{r.d_mean:+9.4f} {r.d_sd:9.4f} {ratio:10.2f} {r.switch_rate:8.1%} "
          f"{int(r.n_books):5d}")

    # =================================================================== Q2 THE RAW CURVE
    P("\n" + "=" * 118)
    P("Q2  THE RAW CURVE.  sd(d) by modal-share decile, threshold-free, with every confound")
    P("    printed beside it.  Deciles are of the cell distribution, not chosen.")
    P("=" * 118)
    Cv = CELLS[CELLS.n_books >= M_MIN_HEADLINE].copy()
    P(f"  headline m_min = {M_MIN_HEADLINE}: {len(Cv)} of {len(CELLS)} cells")
    qs = np.quantile(CELLS.share_mean, np.arange(0, 1.0001, 0.1))
    qs[0] -= 1e-9
    crows2 = []
    for mm in M_MINS:
        Cm = CELLS[CELLS.n_books >= mm]
        for i in range(10):
            lo, hi = qs[i], qs[i + 1]
            s = Cm[(Cm.share_mean > lo) & (Cm.share_mean <= hi)]
            if not len(s):
                continue
            crows2.append(dict(
                m_min=mm, decile=i + 1, share_lo=lo, share_hi=hi, n_cells=len(s),
                share=float(s.share_mean.mean()),
                d_mean=float(s.d_mean.mean()), abs_d=float(s.d_mean.abs().mean()),
                sd_d=float(s.d_sd.mean()), sd_d_median=float(s.d_sd.median()),
                sd_fix=float(s.dfix_sd.mean()), switch=float(s.switch_rate.mean()),
                n_books=float(s.n_books.mean()), distinct=float(s.distinct.mean()),
                mode_stable=float(s.mode_stable.mean())))
    CURVE = pd.DataFrame(crows2)
    CURVE.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    for mm in M_MINS:
        P(f"\n  --- m_min = {mm} " + "-" * 92)
        P(f"  {'dec':>4s} {'share range':>15s} {'cells':>6s} {'share':>7s} {'mean d':>9s} "
          f"{'|mean d|':>9s} {'sd(d)':>9s} {'med sd':>9s} {'sd fixmode':>11s} "
          f"{'switch':>8s} {'n_books':>8s} {'points':>7s}")
        for _, r in CURVE[CURVE.m_min == mm].iterrows():
            P(f"  {int(r.decile):4d} [{r.share_lo:5.3f},{r.share_hi:5.3f}] {int(r.n_cells):6d} "
              f"{r.share:7.1%} {r.d_mean:+9.4f} {r.abs_d:9.4f} {r.sd_d:9.4f} "
              f"{r.sd_d_median:9.4f} {r.sd_fix:11.4f} {r.switch:8.1%} {r.n_books:8.1f} "
              f"{r.distinct:7.2f}")

    sp_all = spearman(Cv.share_mean, Cv.d_sd)
    P(f"\n  Spearman(share, sd(d)) over the {len(Cv)} headline cells = {sp_all:+.3f}")
    P(f"  Spearman(share, |mean d|)                              = "
      f"{spearman(Cv.share_mean, Cv.d_mean.abs()):+.3f}   "
      f"(219's KILL was on the SIGNED mean: {spearman(Cv.share_mean, Cv.d_mean):+.3f})")

    P("\n  ...WITHIN n_books terciles, so the share effect is not read off the n axis:")
    nq = np.quantile(Cv.n_books, [0, 1 / 3, 2 / 3, 1.0])
    nq[0] -= 1e-9
    for i in range(3):
        s = Cv[(Cv.n_books > nq[i]) & (Cv.n_books <= nq[i + 1])]
        P(f"    n_books ({nq[i]:5.1f},{nq[i+1]:5.1f}]  {len(s):4d} cells   "
          f"Spearman(share, sd) = {spearman(s.share_mean, s.d_sd):+.3f}   "
          f"mean sd = {s.d_sd.mean():.4f}")
    P("\n  ...and WITHIN each dial view and each cost rung (share effect must not be a dial):")
    P(f"  {'view':9s} {'cells':>6s} {'rho(share,sd)':>14s} | "
      f"{'rung':>5s} {'cells':>6s} {'rho(share,sd)':>14s}")
    for i, view in enumerate(VIEW_ORDER):
        s = Cv[Cv.dial == view]
        rung_txt = ""
        if i < len(RUNGS):
            sr = Cv[Cv.cost_bps == RUNGS[i]]
            rung_txt = (f"{RUNGS[i]:5d} {len(sr):6d} "
                        f"{spearman(sr.share_mean, sr.d_sd):+14.3f}")
        P(f"  {view:9s} {len(s):6d} {spearman(s.share_mean, s.d_sd):+14.3f} | {rung_txt}")

    # ============================================== Q3 MODE MOVING vs SAMPLE MOVING
    P("\n" + "=" * 118)
    P("Q3  DECOMPOSITION.  sd(d) mixes (i) the half-read MODE moving across draws -- what")
    P("    share is supposed to govern -- and (ii) the HELD-OUT BOOK SET moving, which is")
    P("    live even at share = 1.00.  The FIXED-MODE control re-scores every draw with the")
    P("    full-cell mode, so only (ii) survives.  var_switch = var_total - var_fixed.")
    P("=" * 118)
    drows = []
    for mm in M_MINS:
        Cm = CELLS[CELLS.n_books >= mm]
        for i in range(10):
            lo, hi = qs[i], qs[i + 1]
            s = Cm[(Cm.share_mean > lo) & (Cm.share_mean <= hi)]
            if not len(s):
                continue
            vt = float((s.d_sd ** 2).mean())
            vf = float((s.dfix_sd ** 2).mean())
            drows.append(dict(
                m_min=mm, decile=i + 1, share=float(s.share_mean.mean()), n_cells=len(s),
                sd_total=np.sqrt(vt), sd_fixed=np.sqrt(vf),
                sd_switch=np.sqrt(max(vt - vf, 0.0)),
                share_of_var_from_switch=(1 - vf / vt) if vt > 0 else np.nan,
                switch_rate=float(s.switch_rate.mean())))
    DEC = pd.DataFrame(drows)
    DEC.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    for mm in M_MINS:
        P(f"\n  --- m_min = {mm} " + "-" * 80)
        P(f"  {'dec':>4s} {'share':>7s} {'cells':>6s} {'sd total':>10s} {'sd FIXED':>10s} "
          f"{'sd SWITCH':>10s} {'var share from switch':>22s} {'switch rate':>12s}")
        for _, r in DEC[DEC.m_min == mm].iterrows():
            P(f"  {int(r.decile):4d} {r.share:7.1%} {int(r.n_cells):6d} {r.sd_total:10.4f} "
              f"{r.sd_fixed:10.4f} {r.sd_switch:10.4f} "
              f"{r.share_of_var_from_switch:22.1%} {r.switch_rate:12.1%}")
    Cv = CELLS[CELLS.n_books >= M_MIN_HEADLINE].copy()
    P(f"\n  Spearman(share, sd_total)  = {spearman(Cv.share_mean, Cv.d_sd):+.3f}")
    P(f"  Spearman(share, sd_FIXED)  = {spearman(Cv.share_mean, Cv.dfix_sd):+.3f}   "
      "<- if this is as negative as the total, share is pricing the SAMPLE, not the mode")
    P(f"  Spearman(share, switch)    = {spearman(Cv.share_mean, Cv.switch_rate):+.3f}")
    P(f"  Spearman(switch, sd_total) = {spearman(Cv.switch_rate, Cv.d_sd):+.3f}")

    # =============================================================== Q4 THE FIT AND CONTROLS
    P("\n" + "=" * 118)
    P("Q4  THE FIT.  log(sd(d) + eps) on share, on log n_books, on distinct, and on all")
    P("    three.  Every coefficient and R2 reported; no model is selected here.")
    P("=" * 118)
    Cf = CELLS[CELLS.n_books >= M_MIN_HEADLINE].copy()

    def design(df, spec):
        cols = [np.ones(len(df))]
        if "share" in spec:
            cols.append(df.share_mean.to_numpy(float))
        if "logn" in spec:
            cols.append(np.log(df.n_books.to_numpy(float)))
        if "distinct" in spec:
            cols.append(np.log(df.distinct.to_numpy(float)))
        return np.column_stack(cols)

    SPECS = [(), ("share",), ("logn",), ("distinct",), ("share", "logn"),
             ("share", "logn", "distinct")]
    frows = []
    for mm in M_MINS:
        Cm = CELLS[CELLS.n_books >= mm]
        y = np.log(Cm.d_sd.to_numpy(float) + EPS)
        for spec in SPECS:
            beta, r2, rsd = ols(design(Cm, spec), y)
            frows.append(dict(m_min=mm, spec="+".join(spec) or "const", n=len(Cm), R2=r2,
                              resid_sd=rsd,
                              b_intercept=beta[0],
                              b_share=beta[1 + list(spec).index("share")] if "share" in spec
                              else np.nan,
                              b_logn=beta[1 + list(spec).index("logn")] if "logn" in spec
                              else np.nan,
                              b_distinct=beta[1 + list(spec).index("distinct")]
                              if "distinct" in spec else np.nan))
    FIT = pd.DataFrame(frows)
    FIT.to_csv(OUT / f"{STEM}.fit.csv", index=False)
    for mm in M_MINS:
        P(f"\n  --- m_min = {mm} " + "-" * 84)
        P(f"  {'model':26s} {'n':>5s} {'R2':>8s} {'resid sd':>10s} {'intercept':>11s} "
          f"{'b share':>10s} {'b log n':>10s} {'b log pts':>10s}")
        for _, r in FIT[FIT.m_min == mm].iterrows():
            def f(x):
                return "     --   " if not np.isfinite(x) else f"{x:+10.3f}"
            P(f"  {r.spec:26s} {int(r.n):5d} {r.R2:8.3f} {r.resid_sd:10.3f} "
              f"{r.b_intercept:+11.3f} {f(r.b_share)} {f(r.b_logn)} {f(r.b_distinct)}")
    P("\n  Read: b_share is the log-sd slope per unit of share.  exp(b_share) is the multiple")
    P("  by which sd(d) changes going from share 0 to share 1, holding the controls fixed.")
    for mm in M_MINS:
        b = FIT[(FIT.m_min == mm) & (FIT.spec == "share+logn+distinct")].iloc[0]
        b1 = FIT[(FIT.m_min == mm) & (FIT.spec == "share")].iloc[0]
        P(f"    m_min {mm:2d}:  share alone  exp(b) = {np.exp(b1.b_share):8.4f}  "
          f"(R2 {b1.R2:.3f});   with controls  exp(b) = {np.exp(b.b_share):8.4f}  "
          f"(R2 {b.R2:.3f})")

    # ===================================== Q5 RULE 8 ON THE COLUMN: OOS CALIBRATION
    P("\n" + "=" * 118)
    P("Q5  RULE 8 ON THE COLUMN.  The column is a fitted object, so it is fitted on one part")
    P("    of the cell corpus and read on another, never on itself.  The decision statistic")
    P("    is CALIBRATION of the interval the record would actually publish:")
    P("        one seeded draw d_1  +-  k * sd_hat(share)   must cover the cell's SETTLED")
    P("        value (its mean over all 80 draws).")
    P("    against a CONSTANT-width interval fitted the same way.  All 13 k reported.")
    P("=" * 118)

    def fit_model(train, spec):
        y = np.log(train.d_sd.to_numpy(float) + EPS)
        beta, _, _ = ols(design(train, spec), y)
        return beta

    def predict(beta, test, spec):
        return np.exp(design(test, spec) @ beta) - EPS

    def one_draw(key):
        """The record's practice: ONE seeded split.  Draw 0 of the cell's own 80."""
        return float(DRAWS[key]["d"][0])

    SPLITS = [
        ("corpus A -> corpus B", lambda c: c.corpus == "A", lambda c: c.corpus == "B"),
        ("corpus B -> corpus A", lambda c: c.corpus == "B", lambda c: c.corpus == "A"),
        ("10 bps -> 5/15/20/25", lambda c: c.cost_bps == 10, lambda c: c.cost_bps != 10),
        ("published views -> BAND+/SLEEVE+",
         lambda c: c.dial.isin(PUBLISHED_VIEWS), lambda c: ~c.dial.isin(PUBLISHED_VIEWS)),
    ]
    MODELS = ((("share",), "SHARE"), ((), "CONST"),
              (("share", "logn", "distinct"), "SHARE+CTRL"),
              (("logn", "distinct"), "CTRL-ONLY"))

    def err_of(df):
        keys = list(zip(df.corpus, df.cost_bps, df.dial, df.group))
        d1 = np.array([one_draw(k) for k in keys])
        return np.abs(d1 - df.d_mean.to_numpy(float))

    calib, chosen = [], []
    for mm in M_MINS:
        Cm = CELLS[CELLS.n_books >= mm].reset_index(drop=True)
        for sname, ftr, fte in SPLITS:
            tr, te = Cm[ftr(Cm)], Cm[fte(Cm)]
            if len(tr) < 20 or len(te) < 20:
                continue
            err, err_tr = err_of(te), err_of(tr)
            for spec, label in MODELS:
                beta = fit_model(tr, spec)
                sd_hat = np.clip(predict(beta, te, spec), 0.0, None)
                sd_tr = np.clip(predict(beta, tr, spec), 0.0, None)
                for k in K_GRID:
                    w = k * sd_hat
                    calib.append(dict(
                        m_min=mm, split=sname, model=label, k=k, n_test=len(te),
                        coverage=float(np.mean(err <= w)),
                        mean_width=float(np.mean(2 * w)),
                        median_width=float(np.median(2 * w)),
                        rho_w_err=spearman(w, err),
                        oos_logsd_R2=float(1 - ((np.log(te.d_sd + EPS)
                                                 - np.log(sd_hat + EPS)) ** 2).sum()
                                           / ((np.log(te.d_sd + EPS)
                                               - np.log(te.d_sd + EPS).mean()) ** 2).sum())))
                # ---- RULE 8 ON k: k is chosen on the TRAINING cells only (smallest k whose
                #      TRAIN coverage reaches the nominal 90%) and read once on the test cells.
                kstar = next((k for k in K_GRID
                              if np.mean(err_tr <= k * sd_tr) >= NOMINAL), np.nan)
                if np.isfinite(kstar):
                    w = kstar * sd_hat
                    cov, mw = float(np.mean(err <= w)), float(np.mean(2 * w))
                else:
                    cov = mw = np.nan
                # ---- k-FREE statistic: the standardised error |d1 - settled| / sd_hat.
                #      A column that prices the spread makes this distribution TIGHT.
                z = err / np.where(sd_hat > 0, sd_hat, np.nan)
                z = z[np.isfinite(z)]
                chosen.append(dict(
                    m_min=mm, split=sname, model=label, n_train=len(tr), n_test=len(te),
                    k_star_train=kstar, test_coverage=cov, test_mean_width=mw,
                    z_median=float(np.median(z)) if len(z) else np.nan,
                    z_p90=float(np.percentile(z, 90)) if len(z) else np.nan,
                    z_p90_over_median=(float(np.percentile(z, 90) / np.median(z))
                                       if len(z) and np.median(z) > 0 else np.nan),
                    rho_sdhat_err=spearman(sd_hat, err)))
    CAL = pd.DataFrame(calib)
    CHOSEN = pd.DataFrame(chosen)
    CHOSEN.to_csv(OUT / f"{STEM}.kstar.csv", index=False)
    CAL.to_csv(OUT / f"{STEM}.calib.csv", index=False)

    P("\n  OOS fit quality on log sd(d) (held-out cells, one number per split x model):")
    P(f"  {'split':36s} {'model':12s} {'n_test':>7s} {'OOS R2 (log sd)':>16s} "
      f"{'rho(width, |d1-settled|)':>26s}")
    for mm in [M_MIN_HEADLINE]:
        for sname, _, _ in SPLITS:
            for label in ("SHARE", "CONST", "SHARE+CTRL", "CTRL-ONLY"):
                s = CAL[(CAL.m_min == mm) & (CAL.split == sname) & (CAL.model == label)]
                if not len(s):
                    continue
                r = s.iloc[0]
                P(f"  {sname:36s} {label:12s} {int(r.n_test):7d} {r.oos_logsd_R2:+16.3f} "
                  f"{r.rho_w_err:+26.3f}")

    P("\n  CALIBRATION.  Every k reported.  'coverage' = share of held-out cells whose settled")
    P("  value falls inside one draw +- k*sd_hat.  The share column earns its place only if,")
    P("  at MATCHED coverage, its interval is materially NARROWER than the constant's.")
    for mm in [M_MIN_HEADLINE]:
        for sname, _, _ in SPLITS:
            P(f"\n  --- m_min {mm}   split: {sname} " + "-" * 40)
            P(f"  {'k':>6s} | " + " | ".join(
                f"{lab:>22s}" for lab in ("SHARE cov / width", "CONST cov / width",
                                          "SHARE+CTRL cov / width")))
            for k in K_GRID:
                cells = []
                for label in ("SHARE", "CONST", "SHARE+CTRL"):
                    s = CAL[(CAL.m_min == mm) & (CAL.split == sname)
                            & (CAL.model == label) & (CAL.k == k)]
                    cells.append(f"{s.iloc[0].coverage:9.1%} / {s.iloc[0].mean_width:9.4f}"
                                 if len(s) else " " * 22)
                P(f"  {k:6.2f} | " + " | ".join(cells))

    P("\n  THE HEAD-TO-HEAD, RULE 8 ON k.  k is the smallest grid point reaching 90% coverage")
    P("  on the TRAINING cells; the coverage and width below are then read ONCE on the held-out")
    P("  cells.  The column earns its place if it delivers nominal coverage at a materially")
    P("  smaller width than the constant, or materially better coverage at a comparable width.")
    P(f"  {'split':36s} {'model':12s} {'k(train)':>9s} {'test cov':>9s} {'test width':>11s} "
      f"{'width vs CONST':>15s}")
    for mm in [M_MIN_HEADLINE]:
        for sname, _, _ in SPLITS:
            ref = CHOSEN[(CHOSEN.m_min == mm) & (CHOSEN.split == sname)
                         & (CHOSEN.model == "CONST")]
            ref_w = float(ref.iloc[0].test_mean_width) if len(ref) else np.nan
            for label in ("CONST", "SHARE", "SHARE+CTRL", "CTRL-ONLY"):
                s = CHOSEN[(CHOSEN.m_min == mm) & (CHOSEN.split == sname)
                           & (CHOSEN.model == label)]
                if not len(s):
                    continue
                r = s.iloc[0]
                k_t = ("      n/a" if not np.isfinite(r.k_star_train)
                       else f"{r.k_star_train:9.2f}")
                c_t = ("      n/a" if not np.isfinite(r.test_coverage)
                       else f"{r.test_coverage:9.1%}")
                w_t = ("        n/a" if not np.isfinite(r.test_mean_width)
                       else f"{r.test_mean_width:11.4f}")
                rt = (r.test_mean_width / ref_w) if (np.isfinite(ref_w) and ref_w > 0
                                                     and np.isfinite(r.test_mean_width)) \
                    else np.nan
                r_t = "            n/a" if not np.isfinite(rt) else f"{rt:14.2f}x"
                P(f"  {sname:36s} {label:12s} {k_t} {c_t} {w_t} {r_t}")

    P("\n  THE k-FREE READ.  z = |one draw - settled| / sd_hat on the held-out cells.  A column")
    P("  that prices the spread makes z's spread SMALL: the p90/median ratio is how many times")
    P("  wider an interval must be to cover the tail than to cover the typical cell.")
    P(f"  {'split':36s} {'model':12s} {'z median':>10s} {'z p90':>10s} {'p90/median':>12s} "
      f"{'rho(sd_hat,err)':>16s}")
    for mm in [M_MIN_HEADLINE]:
        for sname, _, _ in SPLITS:
            for label in ("CONST", "SHARE", "SHARE+CTRL", "CTRL-ONLY"):
                s = CHOSEN[(CHOSEN.m_min == mm) & (CHOSEN.split == sname)
                           & (CHOSEN.model == label)]
                if not len(s):
                    continue
                r = s.iloc[0]
                P(f"  {sname:36s} {label:12s} {r.z_median:10.2f} {r.z_p90:10.2f} "
                  f"{r.z_p90_over_median:12.2f} {r.rho_sdhat_err:+16.3f}")

    P("\n  Block bootstrap on the headline question (m_min = 12, corpus A -> corpus B):")
    P(f"  resample whole (corpus, dial, group) blocks of the HELD-OUT cells {N_BOOT} times and")
    P("  re-read SHARE's test coverage and its width ratio against CONST, both models carrying")
    P("  the k each chose on corpus A.")
    Cm = CELLS[CELLS.n_books >= M_MIN_HEADLINE].reset_index(drop=True)
    tr = Cm[Cm.corpus == "A"]
    te_full = Cm[Cm.corpus == "B"].reset_index(drop=True)
    bidx = {k: np.asarray(v) for k, v in
            te_full.groupby(["corpus", "dial", "group"]).indices.items()}
    bk_list = list(bidx.keys())
    err_full = err_of(te_full)
    err_tr = err_of(tr)
    KS, SDH = {}, {}
    for spec, label in ((("share",), "SHARE"), ((), "CONST")):
        beta = fit_model(tr, spec)
        sd_tr = np.clip(predict(beta, tr, spec), 0, None)
        KS[label] = next((k for k in K_GRID
                          if np.mean(err_tr <= k * sd_tr) >= NOMINAL), np.nan)
        SDH[label] = np.clip(predict(beta, te_full, spec), 0, None)
    P(f"  k chosen on corpus A: SHARE {KS['SHARE']}, CONST {KS['CONST']}")
    rngb = np.random.default_rng(BOOT_SEED)
    covs, ratios = [], []
    for _ in range(N_BOOT):
        pick = rngb.integers(0, len(bk_list), len(bk_list))
        ii = np.concatenate([bidx[bk_list[j]] for j in pick])
        e = err_full[ii]
        ws = float(np.mean(2 * KS["SHARE"] * SDH["SHARE"][ii]))
        wc = float(np.mean(2 * KS["CONST"] * SDH["CONST"][ii]))
        covs.append(float(np.mean(e <= KS["SHARE"] * SDH["SHARE"][ii])))
        if wc > 0:
            ratios.append(ws / wc)
    covs, ratios = np.array(covs), np.array(ratios)
    P(f"  SHARE test coverage: median {np.median(covs):.1%}, "
      f"90% CI [{np.percentile(covs, 5):.1%}, {np.percentile(covs, 95):.1%}]")
    if len(ratios):
        P(f"  width ratio SHARE/CONST: median {np.median(ratios):.2f}x, "
          f"90% CI [{np.percentile(ratios, 5):.2f}x, {np.percentile(ratios, 95):.2f}x]")

    # ===================================== Q6 RULE 8 ON THE BOOKS + BOTH KEEP PATHS
    P("\n" + "=" * 118)
    P("Q6  PROTOCOL RULE 8 ON THE BOOKS, and BOTH KEEP PATHS.  Picks made on IS <= 2016-12-31,")
    P("    OOS >= 2017-01-01 read once.  Arms: MODE (write the cell's mode down), FIT (each")
    P("    book's own IS-Sharpe argmax), INCUMBENT, ORACLE (upper bound), and SHRUNK (this")
    P("    run's column used as a DECISION: fall back to the incumbent wherever the fitted")
    P("    sd_hat is in the top tercile).  Averaged over the books of each cell.")
    P("=" * 118)
    beta_share = fit_model(CELLS[CELLS.n_books >= M_MIN_HEADLINE], ("share",))
    sd_hat_all = np.clip(predict(beta_share, CELLS, ("share",)), 0, None)
    CELLS["sd_hat"] = sd_hat_all
    cut = float(np.quantile(sd_hat_all, 2 / 3))
    P(f"  sd_hat top-tercile cut = {cut:.4f}  "
      f"({int((sd_hat_all > cut).sum())} of {len(CELLS)} cells fall back to the incumbent)")

    wrows = []
    for _, r in CELLS.iterrows():
        pk = PACK[(r.corpus, r.cost_bps, r.dial)]
        pos = {n: i for i, n in enumerate(pk["books"])}
        members = GRP[r.corpus][r.group]
        ix = np.array([pos[n] for n in members if n in pos])
        sel = pk["sel"][ix]
        cnt = np.bincount(sel, minlength=len(pk["pts"]))
        md = int(cnt.argmax())
        arms = dict(MODE=np.full(len(ix), md), FIT=sel,
                    INCUMBENT=np.full(len(ix), pk["inc"]), ORACLE=pk["orac"][ix],
                    SHRUNK=np.full(len(ix), pk["inc"] if r.sd_hat > cut else md))
        for aname, pick in arms.items():
            sh = pk["OOS"][ix, pick]
            cg = pk["OOSC"][ix, pick]
            dd = pk["OOSD"][ix, pick]
            f4a = pk["F4A"][ix, pick]
            f4b = pk["F4B"][ix, pick]
            wrows.append(dict(
                corpus=r.corpus, cost_bps=r.cost_bps, dial=r.dial, group=r.group,
                n_books=len(ix), share=r.share_mean, sd_hat=r.sd_hat, arm=aname,
                OOS_Sharpe=float(np.mean(sh)), OOS_CAGR=float(np.mean(cg)),
                OOS_MaxDD=float(np.mean(dd)),
                pass4a=int(np.sum(pd.isna(f4a) | (f4a == "-"))),
                pass4b=int(np.sum(pd.isna(f4b) | (f4b == "-")))))
    WF = pd.DataFrame(wrows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    P("\n  Pooled over all cells (m_min = 12), per cost rung.  OOS = 2017-01-01 onward.")
    P(f"  {'rung':>5s} {'arm':10s} {'cells':>6s} {'OOS Sharpe':>11s} {'OOS CAGR':>10s} "
      f"{'OOS MaxDD':>11s} {'4a pass':>9s} {'4b pass':>9s} {'book-picks':>11s}")
    Wv = WF[WF.n_books >= M_MIN_HEADLINE]
    krows = []
    for cb in RUNGS:
        for aname in ("MODE", "FIT", "SHRUNK", "INCUMBENT", "ORACLE"):
            s = Wv[(Wv.cost_bps == cb) & (Wv.arm == aname)]
            tot = int(s.n_books.sum())
            krows.append(dict(cost_bps=cb, arm=aname, cells=len(s),
                              OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                              OOS_CAGR=float(s.OOS_CAGR.mean()),
                              OOS_MaxDD=float(s.OOS_MaxDD.mean()),
                              picks=tot, pass4a=int(s.pass4a.sum()),
                              pass4b=int(s.pass4b.sum())))
            P(f"  {cb:5d} {aname:10s} {len(s):6d} {s.OOS_Sharpe.mean():11.4f} "
              f"{s.OOS_CAGR.mean():10.2%} {s.OOS_MaxDD.mean():11.2%} "
              f"{int(s.pass4a.sum()):9d} {int(s.pass4b.sum()):9d} {tot:11d}")
    KEEP = pd.DataFrame(krows)
    KEEP.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    P("\n  SHRUNK minus MODE (the column used as a decision), per rung -- P5's test:")
    for cb in RUNGS:
        a = Wv[(Wv.cost_bps == cb) & (Wv.arm == "SHRUNK")].set_index(
            ["corpus", "dial", "group"]).OOS_Sharpe
        b = Wv[(Wv.cost_bps == cb) & (Wv.arm == "MODE")].set_index(
            ["corpus", "dial", "group"]).OOS_Sharpe
        d = (a - b).dropna()
        P(f"    {cb:2d} bps: mean {d.mean():+.4f}   t {tstat(d.to_numpy()):+6.2f}   "
          f"cells improved {np.mean(d > 0):.1%}  of {len(d)}")

    P("\n  THE ANCHOR the sprint asks for: RULES v2 (live baseline) and SPY over the SAME OOS")
    P("  window, on research/baseline.py's own universe, 10 bps, weekly.")
    px = load_universe()
    st = px.index[260]
    bres = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")
    br = bres["returns"].loc[st:].loc[OOS_START:]
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:].loc[OOS_START:]
    mb, msp = metrics(br), metrics(spy)
    P(f"  {'series':28s} {'OOS CAGR':>10s} {'OOS Sharpe':>11s} {'OOS MaxDD':>11s}")
    P(f"  {'RULES v2 baseline (live)':28s} {mb['CAGR']:10.2%} {mb['Sharpe']:11.2f} "
      f"{mb['MaxDD']:11.2%}")
    P(f"  {'SPY buy-and-hold':28s} {msp['CAGR']:10.2%} {msp['Sharpe']:11.2f} "
      f"{msp['MaxDD']:11.2%}")
    best = Wv[(Wv.cost_bps == BASE_RUNG) & (Wv.arm == "MODE")]
    P(f"  {'idea 224 MODE arm (10 bps)':28s} {best.OOS_CAGR.mean():10.2%} "
      f"{best.OOS_Sharpe.mean():11.2f} {best.OOS_MaxDD.mean():11.2%}   "
      f"(mean over {len(best)} cells' books; NOT a new book -- idea 144)")
    P("\n  NOTE: no arm here is a new book.  Every arm is a re-dial of books already in the")
    P("  record (idea 144), so neither KEEP path can be claimed by this run whatever the")
    P("  numbers say; the 4a/4b counts are reported because PROTOCOL rule 4 asks for them.")

    # ================================================================= VERDICT vs P1..P5
    P("\n" + "=" * 118)
    P("VERDICT, against the predictions registered at the top of this file.")
    P("=" * 118)
    Cq = CELLS[CELLS.n_books >= M_MIN_HEADLINE]
    r_sd = spearman(Cq.share_mean, Cq.d_sd)
    r_mean = spearman(Cq.share_mean, Cq.d_mean)
    f_share = FIT[(FIT.m_min == M_MIN_HEADLINE) & (FIT.spec == "share")].iloc[0]
    f_dist = FIT[(FIT.m_min == M_MIN_HEADLINE) & (FIT.spec == "distinct")].iloc[0]
    f_all = FIT[(FIT.m_min == M_MIN_HEADLINE) & (FIT.spec == "share+logn+distinct")].iloc[0]
    P(f"  P1 REPRODUCTION            PASS   560/560 cells and 132/132 sweep rows, "
      f"max |d| {max(dmax, sdmax):.3e}")
    P(f"  P2 sd(d) falls with share  PASS   Spearman {r_sd:+.3f} on sd(d) against "
      f"{r_mean:+.3f} on the signed mean (219's KILL);")
    P("                                    negative in all 3 n_books terciles, all 7 dial "
      "views and all 5 rungs.")
    P(f"  P3 switch term carries it  SPLIT  it DOES carry the low-share end "
      f"({DEC[(DEC.m_min == M_MIN_HEADLINE)].iloc[0].share_of_var_from_switch:.0%} of the "
      "variance in decile 1)")
    P("                                    and is exactly 0% above share ~0.78, but the "
      "FIXED-MODE control is NOT flat")
    P(f"                                    (Spearman {spearman(Cq.share_mean, Cq.dfix_sd):+.3f}"
      "): at high share the mode equals nearly every")
    P("                                    book's own pick, so the SAMPLE term collapses too.")
    P(f"  P4 the column, calibrated  FAIL   share ranks the spread strongly out of corpus "
      f"(OOS log-sd R2 up to")
    P("                                    +0.59 against ~0.00 for a constant; rho(sd_hat, "
      "|error|) +0.70..+0.83),")
    P("                                    but as an INTERVAL it loses outright: at the k each "
      "model picks on")
    P("                                    training cells, SHARE covers 88.8% at 15.0x the "
      "width of a FLAT constant")
    P("                                    that covers 89.6% (A->B; 8.6x/12.0x/53.3x on the "
      "other three splits).")
    a10 = Wv[(Wv.cost_bps == BASE_RUNG) & (Wv.arm == "SHRUNK")].set_index(
        ["corpus", "dial", "group"]).OOS_Sharpe
    b10 = Wv[(Wv.cost_bps == BASE_RUNG) & (Wv.arm == "MODE")].set_index(
        ["corpus", "dial", "group"]).OOS_Sharpe
    d10 = (a10 - b10).dropna()
    P(f"  P5 SHRUNK does not win     PASS   SHRUNK - MODE = {d10.mean():+.4f} OOS Sharpe at "
      f"{BASE_RUNG} bps, t {tstat(d10.to_numpy()):+.2f}, "
      f"{np.mean(d10 > 0):.1%} of cells improved.")
    _g = CAL[(CAL.m_min == M_MIN_HEADLINE) & (CAL.k == K_GRID[0])]
    _g = _g.pivot(index="split", columns="model", values="oos_logsd_R2")
    gap_ctrl = float((_g["SHARE+CTRL"] - _g["CTRL-ONLY"]).abs().max())
    P("\n  AND THE COLUMN THE RECORD SHOULD ACTUALLY QUOTE IS NOT THE SHARE.  `distinct` -- the")
    P("  number of ladder points that receive ANY book's vote -- beats share on its own")
    P(f"  (R2 {f_dist.R2:.3f} vs {f_share.R2:.3f}) and absorbs it: with distinct in the model "
      f"share's log-sd slope")
    P(f"  collapses from {f_share.b_share:+.2f} to {f_all.b_share:+.2f}, and CTRL-ONLY (no "
      "share at all) matches SHARE+CTRL")
    P(f"  on every split's OOS log-sd R2 to within {gap_ctrl:.3f}.")
    P("\n  KILL as a PROTOCOL clause and as a published interval.  The queue's PREMISE is")
    P("  CONFIRMED -- modal share prices the VARIANCE where idea 219 showed it does not price")
    P("  the SIGN -- but the proposed CONFIDENCE column does not survive being calibrated, and")
    P("  the ranking it does deliver is delivered better by the cell's pick COUNT.  No RULES")
    P("  change, no book promoted, no KEEP on either path; RULES.md, scan.py, bot.py and")
    P("  baseline.py untouched.")

    P(f"\n  total runtime {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
