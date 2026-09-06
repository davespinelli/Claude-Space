#!/usr/bin/env python3
"""IDEA 219  what-modal-share-makes-a-mode-writable   (cloud, 2026-09-06)

THE QUESTION
------------
Idea 189 found that "read the selector's mode once and write it down" beats fitting the dial
per book -- EXCEPT in exactly one of its 10 corpus x dial cells.  Its Q5 split-half control
read the mode on one half of the corpus and scored it on the other:

    the mode reproduces across halves in 9 of 10 cells; the exception is N on corpus A
    (mode 10 on one half, 20 on the other) whose modal SHARE is 22.6% on 53 books, and there
    the held-out mode LOSES -0.0229, while CADENCE at 83.0%/88.7% wins +0.0261/+0.0255.

Idea 189's own words: "the modal constant is only as good as the mode's own concentration, and
a dial whose modal share is ~23% on 53 books does not have a readable mode."  That sentence is
a PROTOCOL clause with a blank in it.  This run fills the blank:

    SWEEP the modal-share threshold over every dial x corpus cell in the record whose picks
    survive, and report the share at which the held-out mode stops beating the fit.

  Q1  REPRODUCTION.  Rebuild idea 217's 5-rung derived cost ladder (which itself rebuilds idea
      171's/189's) and match BOTH committed ladder CSVs before any new number is read.
  Q2  THE CELL CORPUS.  10 published cells cannot locate a threshold: their modal shares
      cluster at ~0.23 (N) and 0.67-1.00 (everything else), leaving the whole 0.25-0.65 range
      empty.  Widen the cell corpus along three axes that are ALREADY in the record and cost
      nothing extra: the 5-rung cost ladder (idea 217), sub-corpus GROUPS (each seeded
      sub-panel family, which is a different pick distribution, not a different simulator),
      and idea 218's two extendable dials (BAND -> 0.15, SLEEVE -> 0.50; GROSS is NOT extended
      because past 1.00 it needs a financing assumption and idea 218 called its extension a
      truncation artefact).
  Q3  THE CURVE.  Held-out-mode-minus-fit OOS Sharpe as a function of the modal share read on
      the FITTING half.  Binned, threshold-free, reported before any threshold is chosen.
  Q4  THE THRESHOLD.  Sweep tau over [0.20, 1.00]; report EVERY grid point; read the crossing
      off the table with a bootstrap CI over cells.
  Q5  RULE 8 ON THE THRESHOLD ITSELF.  tau is a fitted parameter like any other.  Choose it on
      corpus A and evaluate on corpus B, and vice versa; and choose it at 10 bps and evaluate
      at 5/15/20/25.  A threshold that only works where it was fitted is a PARK, not a clause.
  Q6  RULE 8 (picks on <= 2016-12-31, 2017-> read once) and BOTH KEEP PATHS on every row.

DESIGN
------
Idea 171's `Book`/`build_corpus`/`fast_backtest`, idea 189's `build_corpus_B`, and idea 217's
metric helpers and exact cost-additivity identity are IMPORTED, not re-implemented.  The ladder
runner is written here only because it must dispatch two extra dial VIEWS (BAND+, SLEEVE+) that
the parents' hard-coded if/elif chain cannot express; it is asserted row-for-row against BOTH
parents' committed ladder CSVs on every shared point, which is a stronger control than reuse.

  physical ladders simulated (union; the published views are slices of these)
      GROSS   [0.20 .. 1.00]  10 pts        view GROSS   = all 10   (idea 171's)
      N       [3 .. 50]       10 pts        view N       = all 10
      BAND    [0.00 .. 0.15]   8 pts        view BAND    = first 5  (idea 171's)
                                            view BAND+   = all 8    (idea 218's extension)
      CADENCE [D, W, M, Q]     4 pts        view CADENCE = all 4
      SLEEVE  [0.00 .. 0.50]  11 pts        view SLEEVE  = first 7  (idea 171's)
                                            view SLEEVE+ = all 11   (idea 218's extension)
  corpora   A = idea 171's 53 books, B = idea 189's 115 books on idea 175's panels
  rungs     5/10/15/20/25 bps, DERIVED exactly from one 0 bps simulation per (book, dial,
            point) by net(c) = gross - turnover*c/1e4  (idea 217's identity, re-asserted here)
  windows   IS <= 2016-12-31 chooses; OOS >= 2017-01-01 is read ONCE

  A CELL is (corpus, cost rung, dial view, book group).  Book groups are ALL plus every
  seeded sub-panel family and family x k with at least m_min books.  Within a cell the mode's
  own walk-forward is run S = 40 times: a seeded random half chooses the mode (and reports the
  modal SHARE it was read at), the other half is scored, both directions used.

  observation  = (modal share on the fitting half, mean over held-out books of
                  OOS_Sharpe(that mode) - OOS_Sharpe(that book's own IS-Sharpe fit))
  positive d   = the held-out mode BEATS the fit.

  TUNED PARAMETER 1: the modal-share threshold tau -- swept over 33 grid points, ALL reported.
                     It is the output, not a setting.
  TUNED PARAMETER 2: m_min, the smallest book group admitted as a cell -- reported at
                     {8, 12, 20, 40}; the headline uses 12 and every value is in the table.
  Everything else (dials, ladders, corpora, rungs, IS/OOS split, S, the seeds) is INHERITED
  from ideas 171/175/189/217/218 or fixed a priori, not chosen here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  The rebuilt 10 bps base-dial ladder matches idea 189's committed ladder.csv and idea
      217's matches on all 5 rungs, both at max |d| < 1e-12, with 0 4a/4b verdict mismatches.
  P2  Mean d is INCREASING in modal share: Spearman(share, d) > 0 over cells, sign-consistent
      on both corpora separately.
  P3  The crossing is bracketed by the record's own two anchors: it lies strictly between
      0.226 (idea 189's failing N cell) and 0.830 (its winning CADENCE cell).
  P4  The crossing is BELOW 0.60, i.e. a bare-majority floor (share > 0.5) is sufficient but
      stricter than necessary.
  P5  The GATED arm (mode where share >= tau, fit otherwise) with tau chosen on the OTHER
      corpus beats SEL-SHARPE on mean OOS Sharpe on BOTH corpora.
  P6  Zero 4b passes on SMALL-parent books, at every rung (idea 136, reproduction n+1).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): B136, U56 and the small panel are current-constituent lists with no
    delistings.  Every arm inherits it equally so the PAIRED comparison is unaffected; every
    LEVEL below is biased upward and none of them is a tradable estimate.
  * Corpus A's SMALL484 book is idea 171's, built WITHOUT the max_1d_move >= 1.0 screen; corpus
    B's SMALL439 applies it (44 names dropped).  Corpus A is not altered because it is the
    reproduction target.  1 of 53 corpus-A books is affected and it is a fixed panel, never a
    group of its own.
  * Cells are NOT independent.  They share books (a k-group is a subset of ALL), share
    simulations across the 5 cost rungs (one 0 bps run, derived by subtraction), and share
    parents (48 of corpus A's 53 books are B136 sub-panels).  Every t and CI below is over
    correlated units and its nominal size is optimistic; the cell-level bootstrap resamples
    whole (corpus, dial, group) blocks to blunt the worst of it, and no p-value here is a
    p-value on a fresh sample.
  * The modal share is itself estimated on a half-corpus of 4-57 books, so it carries sampling
    error that is largest exactly where the share is lowest.  That is a property of the
    statistic the clause would be written on, not a defect of the measurement, and it is why
    the sweep is reported as a crossing INTERVAL rather than a point.
  * Idea 144: a re-dialled book is the same book.  Nothing here is a new signal and nothing is
    proposed as a book.
  * On k=20 sub-panels the N ladder saturates (n >= 20 admits every eligible name).  Inherited
    from idea 171, reported not hidden.
  * Idea 38's calendar-day index and idea 126's t+1-only execution carry over.
  * GROSS is not extended past 1.00 (financing assumption); idea 218's own verdict on that
    extension was TRUNCATION ARTEFACT, so its extended cell would not have been usable anyway.

Deterministic, standalone.  Writes .console.txt, .ladder.csv.gz, .cells.csv, .sweep.csv,
.walkforward.csv, .keep.csv.
"""
import importlib.util
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import metrics  # noqa: E402

STEM = "2026-09-06_what-modal-share-makes-a-mode-writable_cloud"
OUT = ROOT / "research" / "backtests"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
P189_STEM = "2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_cloud"
P217_STEM = "2026-09-05_does-the-modal-constant-result-survive-a-cost-ladder_cloud"

RUNGS = [5, 10, 15, 20, 25]
BASE_RUNG = 10
S_SPLITS = 40                       # split-half repetitions per cell (design constant)
M_MINS = [8, 12, 20, 40]            # tuned parameter 2, all reported
M_MIN_HEADLINE = 12
TAU_GRID = [round(0.20 + 0.025 * i, 3) for i in range(33)]   # tuned parameter 1, all reported
SPLIT_SEED = 219_500
BOOT_SEED = 219_700
N_BOOT = 2000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p171 = _load(P171_STEM, "p171")
p189 = _load(P189_STEM, "p189")
p217 = _load(P217_STEM, "p217")
for m in (p171, p189, p217):
    m.P = P

fast_backtest = p171.fast_backtest
IS_END, OOS_START = p171.IS_END, p171.OOS_START
INC = dict(p171.INC)

_cagr_sh_dd, _halves = p217._cagr_sh_dd, p217._halves
_rel_margin, _spy_pack = p217._rel_margin, p217._spy_pack
_keep_4a, _keep_4b = p217._keep_4a, p217._keep_4b
tstat, sign_p = p171.tstat, p171.sign_p

def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson on midranks."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 3:
        return np.nan
    ra = pd.Series(a).rank().to_numpy()
    rb = pd.Series(b).rank().to_numpy()
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ---- physical ladders actually simulated (union of the published and the extended)
PHYS = {
    "GROSS":   [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00],
    "N":       [3, 5, 8, 10, 15, 20, 25, 30, 40, 50],
    "BAND":    [0.00, 0.02, 0.03, 0.05, 0.08, 0.10, 0.12, 0.15],
    "CADENCE": ["D", "W", "M", "Q"],
    "SLEEVE":  [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
}
PHYS_ORDER = ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"]

# ---- the dial VIEWS that become cells.  (physical dial, points admitted)
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
PUBLISHED_VIEWS = ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"]   # idea 171/189/217's five

# the Book class precomputes an eligibility mask per BAND ladder point; the extended points
# must exist before any corpus is built.  Each parent module loads its OWN copy of idea 171
# (importlib, not sys.modules), so corpus B's Book class is p189's copy and must be patched
# too -- otherwise the extended BAND view silently falls back to the incumbent mask.
for _m in (p171, getattr(p189, "p171", None), getattr(p217, "p171", None)):
    if _m is not None:
        _m.DIALS["BAND"] = (PHYS["BAND"], 0.00)


# ------------------------------------------------------------------------- ladder runner
def run_ladder(books, panels, tag, t0):
    """One simulation per (book, physical dial, point) at 0 bps; every rung derived exactly."""
    ctx = {}
    for b in books:
        if b.parent not in ctx:
            px = panels[b.parent]
            st = px.index[260]
            spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
            bres = fast_backtest(px, rules_v1_weights(px), 0.0, "W")
            ctx[b.parent] = dict(st=st, spy=spy, bg=bres["returns"].loc[st:],
                                 bt=bres["turnover"].loc[st:])
    rows = []
    for bi, bk in enumerate(books):
        c = ctx[bk.parent]
        idx = bk.px.index
        i0 = int(np.searchsorted(idx, c["st"]))
        widx = idx[i0:]
        is_n = int((widx <= pd.Timestamp(IS_END)).sum())
        oos_i = int(np.searchsorted(widx, pd.Timestamp(OOS_START)))

        spy = c["spy"].reindex(widx).fillna(0.0).values
        spy_is, spy_oos = spy[:is_n], spy[oos_i:]
        SM_F, SM_IS, SM_OOS = _spy_pack(spy), _spy_pack(spy_is), _spy_pack(spy_oos)
        sh_spy_oos = _cagr_sh_dd(spy_oos)[1]

        bg = c["bg"].reindex(widx).fillna(0.0).values
        bt = c["bt"].reindex(widx).fillna(0.0).values
        BASE = {}
        for cb in RUNGS:
            bn = bg - bt * cb / 1e4
            b1, b2 = _halves(bn)
            BASE[cb] = (b1, b2, _cagr_sh_dd(bn)[2])

        for dial in PHYS_ORDER:
            for pt in PHYS[dial]:
                kw = dict(gross=INC["GROSS"], n=INC["N"], band=INC["BAND"],
                          sleeve=INC["SLEEVE"])
                fq = INC["CADENCE"]
                if dial == "GROSS":
                    kw["gross"] = pt
                elif dial == "N":
                    kw["n"] = pt
                elif dial == "BAND":
                    kw["band"] = pt
                elif dial == "SLEEVE":
                    kw["sleeve"] = pt
                else:
                    fq = pt
                res = fast_backtest(bk.px, bk.weights(**kw), 0.0, fq)
                g = res["returns"].values[i0:]
                tn = res["turnover"].values[i0:]
                tpy = tn.sum() / (len(g) / 252.0)
                for cb in RUNGS:
                    r = g - tn * cb / 1e4
                    r_is, r_oos = r[:is_n], r[oos_i:]
                    cf, shf, ddf = _cagr_sh_dd(r)
                    ci, shi, ddi = _cagr_sh_dd(r_is)
                    co, sho, ddo = _cagr_sh_dd(r_oos)
                    h1, h2 = _halves(r)
                    mg_is, wb_is = _rel_margin(r_is, spy_is, SM_IS)
                    mg_oos, wb_oos = _rel_margin(r_oos, spy_oos, SM_OOS)
                    b1, b2, bdd = BASE[cb]
                    rows.append(dict(
                        corpus=tag, cost_bps=cb, book=bk.name, parent=bk.parent, dial=dial,
                        point=pt, is_incumbent=(pt == INC[dial]),
                        CAGR=cf, Sharpe=shf, MaxDD=ddf, H1=h1, H2=h2, turnover=tpy,
                        IS_Sharpe=shi, IS_CAGR=ci, IS_MaxDD=ddi,
                        IS_margin=mg_is, IS_worstbar=wb_is,
                        OOS_Sharpe=sho, OOS_CAGR=co, OOS_MaxDD=ddo,
                        OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                        fail4a=_keep_4a(h1, h2, ddf, b1, b2, bdd),
                        fail4b=_keep_4b(h1, h2, sho, cf, ddf, SM_F, sh_spy_oos)))
        if (bi + 1) % 25 == 0:
            P(f"   ... {tag} {bi + 1}/{len(books)} books  ({time.time() - t0:.0f}s)")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- book groups
def groups_of(tag, names):
    """ALL, every seeded sub-panel family, and every family x k.  Fixed panels are never a
    group of their own (n < 5).  Keys are stable strings; membership is by name prefix, which
    is how ideas 171/175 name their draws."""
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


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 219  what-modal-share-makes-a-mode-writable   (cloud, 2026-09-06)")
    P("=" * 118)

    # ------------------------------------------------------ Q1 reproduction, before anything
    P("\nbuilding corpus A (idea 171's build_corpus, imported) ...")
    booksA, panelsA = p171.build_corpus()
    P(f"  corpus A: {len(booksA)} books")
    P("\nbuilding corpus B (idea 189's build_corpus_B, imported) ...")
    booksB, panelsB = p189.build_corpus_B()
    P(f"  corpus B: {len(booksB)} books")

    P("\nREPRODUCTION CONTROLS (asserted before any new number is read)")
    okA = p171.check_a(booksA[1])
    okB = all(p171.check_b(b) for b in booksA[:3])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED -- not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\n  [c] cost additivity identity: net(c) == gross - turnover*c/1e4, direct vs derived")
    dmax_add = 0.0
    for bk in booksA[:3]:
        for kw, fq in [(dict(gross=0.75, n=20, band=0.0, sleeve=0.0), "W"),
                       (dict(gross=1.00, n=10, band=0.08, sleeve=0.0), "M"),
                       (dict(gross=0.50, n=40, band=0.0, sleeve=0.30), "Q")]:
            z = fast_backtest(bk.px, bk.weights(**kw), 0.0, fq)
            for cb in RUNGS:
                direct = fast_backtest(bk.px, bk.weights(**kw), float(cb), fq)["returns"].values
                der = z["returns"].values - z["turnover"].values * cb / 1e4
                dmax_add = max(dmax_add, float(np.abs(direct - der).max()))
    P(f"      max |direct - derived| over 3 books x 3 configs x 5 rungs = {dmax_add:.3e}")
    if dmax_add > 1e-12:
        P("\n*** the derived cost ladder is not an identity.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\nrunning ladders (1 simulation per book x dial x point, 5 rungs derived) ...")
    ladA = run_ladder(booksA, panelsA, "A", t0)
    ladB = run_ladder(booksB, panelsB, "B", t0)
    lad = pd.concat([ladA, ladB], ignore_index=True)
    P(f"   {len(lad)} ladder rows ({len(ladA)} A + {len(ladB)} B)  ({time.time() - t0:.0f}s)")

    key = ["corpus", "book", "dial", "point"]
    base_pts = {d: set(map(str, VIEWS[d][1])) for d in PUBLISHED_VIEWS}
    mine = lad.astype({"point": str}).copy()
    mine = mine[[r.dial in base_pts and r.point in base_pts[r.dial]
                 for r in mine.itertuples()]]

    C189 = pd.read_csv(OUT / f"{P189_STEM}.ladder.csv").astype({"point": str})
    m189 = mine[mine.cost_bps == BASE_RUNG].merge(C189, on=key, suffixes=("", "_c"))
    P(f"\n  [d] rebuilt 10 bps rung vs idea 189's committed ladder.csv: "
      f"{len(m189)}/{len(C189)} rows matched")
    d189 = 0.0
    for col in ["IS_Sharpe", "IS_margin", "OOS_Sharpe", "OOS_margin", "OOS_CAGR", "OOS_MaxDD",
                "CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover"]:
        v = float((m189[col] - m189[f"{col}_c"]).abs().max())
        d189 = max(d189, v)
    v189 = int((m189.fail4a != m189.fail4a_c).sum()) + int((m189.fail4b != m189.fail4b_c).sum())
    P(f"      max |d| over 12 metric columns = {d189:.3e};  4a/4b verdict mismatches = {v189}")

    C217 = pd.read_csv(OUT / f"{P217_STEM}.ladder.csv").astype({"point": str})
    m217 = mine.merge(C217, on=key + ["cost_bps"], suffixes=("", "_c"))
    P(f"  [e] rebuilt 5-rung ladder vs idea 217's committed ladder.csv: "
      f"{len(m217)}/{len(C217)} rows matched")
    d217 = 0.0
    for col in ["IS_Sharpe", "IS_margin", "OOS_Sharpe", "OOS_margin", "OOS_CAGR", "OOS_MaxDD",
                "CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover"]:
        v = float((m217[col] - m217[f"{col}_c"]).abs().max())
        d217 = max(d217, v)
    v217 = int((m217.fail4a != m217.fail4a_c).sum()) + int((m217.fail4b != m217.fail4b_c).sum())
    P(f"      max |d| over 12 metric columns = {d217:.3e};  4a/4b verdict mismatches = {v217}")
    repro_ok = (len(m189) == len(C189) and len(m217) == len(C217)
                and max(d189, d217) < 1e-12 and (v189 + v217) == 0)
    P(f"      REPRODUCTION {'PASS' if repro_ok else 'FAIL'}")
    if not repro_ok:
        P("\n*** the parents do not reproduce.  Stopping before any new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    lad.to_csv(OUT / f"{STEM}.ladder.csv.gz", index=False, compression="gzip")

    # ------------------------------------------------------------- packed per-cell matrices
    NAMES = {"A": [b.name for b in booksA], "B": [b.name for b in booksB]}
    PARENT = {b.name: b.parent for b in booksA + booksB}
    PACK = {}
    lad_s = lad.astype({"point": str})
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
                bk = [n for n in NAMES[tag] if n in piv_is.index]
                piv_is = piv_is.loc[bk, spts]
                PACK[(tag, cb, view)] = dict(
                    books=bk, pts=pts, spts=spts,
                    IS=piv_is.to_numpy(float),
                    OOS=piv_o.loc[bk, spts].to_numpy(float),
                    OOSC=piv_oc.loc[bk, spts].to_numpy(float),
                    OOSD=piv_od.loc[bk, spts].to_numpy(float),
                    MAR=piv_m.loc[bk, spts].to_numpy(float),
                    sel=np.nanargmax(piv_is.to_numpy(float), axis=1),
                    sel4b=np.nanargmax(piv_m.loc[bk, spts].to_numpy(float), axis=1),
                    orac=np.nanargmax(piv_o.loc[bk, spts].to_numpy(float), axis=1),
                    inc=(spts.index(str(INC[VIEWS[view][0]]))
                         if str(INC[VIEWS[view][0]]) in spts else 0))

    # -------------------------------------------------------------------- Q2 the cell corpus
    P("\n" + "=" * 118)
    P("Q2  THE CELL CORPUS.  Full-cell modal share per (corpus, rung, dial view, group).")
    P("    The published record contributes 10 cells (2 corpora x 5 dials at 10 bps, group=ALL);")
    P("    the extra axes are the cost rungs (idea 217), the sub-panel groups, and idea 218's")
    P("    two extendable dial views.  No new simulator, no new panel.")
    P("=" * 118)
    GRP = {tag: groups_of(tag, NAMES[tag]) for tag in ("A", "B")}
    for tag in ("A", "B"):
        P(f"  corpus {tag} groups: " + ", ".join(f"{k}({len(v)})" for k, v in GRP[tag].items()))

    crows = []
    rng_master = np.random.default_rng(SPLIT_SEED)
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
                    # ---- the mode's own walk-forward, S seeded splits, both directions
                    # idea 208: NEVER seed from hash() -- PYTHONHASHSEED salts it and the run
                    # stops being deterministic.  crc32 of the cell key instead.
                    rng = np.random.default_rng(
                        SPLIT_SEED + zlib.crc32(
                            f"{tag}|{cb}|{view}|{gname}".encode()) % 10_000_019)
                    shares, ds, dm, stab = [], [], [], []
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
                            d = float(np.mean(pk["OOS"][rows_h, md]
                                              - pk["OOS"][rows_h, pk["sel"][rows_h]]))
                            dmg = float(np.mean(pk["MAR"][rows_h, md]
                                                - pk["MAR"][rows_h, pk["sel"][rows_h]]))
                            shares.append(sh)
                            ds.append(d)
                            dm.append(dmg)
                        stab.append(modes_[0] == modes_[1])
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
                                   and view in PUBLISHED_VIEWS)))
    CELLS = pd.DataFrame(crows)
    CELLS.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    P(f"\n  {len(CELLS)} cells built  ({time.time() - t0:.0f}s);  "
      f"{S_SPLITS} splits x 2 directions each = {len(CELLS) * S_SPLITS * 2} observations")

    P("\n  The 10 PUBLISHED cells (idea 189's Q5 grid), re-derived here:")
    P(f"  {'corpus':7s} {'dial':9s} {'mode':>7s} {'share':>7s} {'stable':>7s} {'d_mean':>9s} "
      f"{'d_med':>9s} {'win':>7s}")
    for _, r in CELLS[CELLS.published].sort_values(["corpus", "dial"]).iterrows():
        P(f"  {r.corpus:7s} {r.dial:9s} {r.full_mode:>7s} {r.full_share:7.1%} "
          f"{r.mode_stable:7.1%} {r.d_mean:+9.4f} {r.d_median:+9.4f} {r.win:7.1%}")

    P("\n  Modal-share coverage of the widened corpus (why the 10 published cells were not enough):")
    for lo in np.arange(0.15, 1.0, 0.1):
        n_all = int(((CELLS.share_mean >= lo) & (CELLS.share_mean < lo + 0.1)).sum())
        n_pub = int(((CELLS.published) & (CELLS.share_mean >= lo)
                     & (CELLS.share_mean < lo + 0.1)).sum())
        P(f"    share [{lo:.2f},{lo + 0.1:.2f}) : {n_all:4d} cells   (published: {n_pub})")

    # --------------------------------------------------------------------- Q3 the curve
    P("\n" + "=" * 118)
    P("Q3  THE CURVE.  Held-out-mode minus fit (OOS Sharpe), binned by the modal share read on")
    P("    the FITTING half.  Threshold-free; reported before any threshold is chosen.")
    P("=" * 118)
    for mm in M_MINS:
        C = CELLS[CELLS.n_books >= mm]
        P(f"\n  --- m_min = {mm}  ({len(C)} cells) " + "-" * 60)
        P(f"  {'share bin':>14s} {'cells':>6s} {'books':>6s} {'mean d':>10s} {'median d':>10s} "
          f"{'t':>7s} {'cells d>0':>10s} {'mean dMargin':>13s}")
        edges = [0.0, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.01]
        for lo, hi in zip(edges[:-1], edges[1:]):
            s = C[(C.share_mean >= lo) & (C.share_mean < hi)]
            if not len(s):
                P(f"  [{lo:.2f},{hi:.2f})".rjust(14) + f" {0:6d}" + "        --")
                continue
            d = s.d_mean.to_numpy()
            P(f"  [{lo:.2f},{hi:.2f})".rjust(14) + f" {len(s):6d} {int(s.n_books.mean()):6d} "
              f"{d.mean():+10.4f} {np.median(d):+10.4f} {tstat(d):+7.2f} "
              f"{np.mean(d > 0):10.1%} {s.dmargin_mean.mean():+13.4f}")
        rho = spearman(C.share_mean, C.d_mean)
        P(f"  Spearman(modal share, mean d) = {rho:+.4f}  over {len(C)} cells")
        for tag in ("A", "B"):
            s = C[C.corpus == tag]
            P(f"      corpus {tag}: Spearman = {spearman(s.share_mean, s.d_mean):+.4f} "
              f"over {len(s)} cells")

    C = CELLS[CELLS.n_books >= M_MIN_HEADLINE]
    P(f"\n  Per dial view (m_min = {M_MIN_HEADLINE}), pooled over rungs and groups:")
    P(f"  {'dial':9s} {'cells':>6s} {'share':>8s} {'mean d':>10s} {'cells d>0':>10s} "
      f"{'mode stable':>12s}")
    for view in VIEW_ORDER:
        s = C[C.dial == view]
        P(f"  {view:9s} {len(s):6d} {s.share_mean.mean():8.1%} {s.d_mean.mean():+10.4f} "
          f"{np.mean(s.d_mean > 0):10.1%} {s.mode_stable.mean():12.1%}")

    # ------------------------------------------------------------------ Q4 the threshold
    P("\n" + "=" * 118)
    P("Q4  THE THRESHOLD SWEEP.  Every grid point reported.  'above' = cells whose modal share")
    P("    is >= tau (where the clause would license writing the mode down); 'below' = cells")
    P("    where it would not.  The clause is only worth writing if 'above' is positive AND")
    P("    'below' is not.")
    P("=" * 118)
    srows = []
    for mm in M_MINS:
        C = CELLS[CELLS.n_books >= mm]
        for tau in TAU_GRID:
            a = C[C.share_mean >= tau]
            b = C[C.share_mean < tau]
            srows.append(dict(
                m_min=mm, tau=tau, n_above=len(a), n_below=len(b),
                d_above=float(a.d_mean.mean()) if len(a) else np.nan,
                d_below=float(b.d_mean.mean()) if len(b) else np.nan,
                win_above=float(np.mean(a.d_mean > 0)) if len(a) else np.nan,
                win_below=float(np.mean(b.d_mean > 0)) if len(b) else np.nan,
                t_above=tstat(a.d_mean.to_numpy()) if len(a) > 2 else np.nan,
                t_below=tstat(b.d_mean.to_numpy()) if len(b) > 2 else np.nan,
                sep=((float(a.d_mean.mean()) if len(a) else np.nan)
                     - (float(b.d_mean.mean()) if len(b) else np.nan))))
    SW = pd.DataFrame(srows)
    SW.to_csv(OUT / f"{STEM}.sweep.csv", index=False)
    for mm in M_MINS:
        P(f"\n  --- m_min = {mm} " + "-" * 70)
        P(f"  {'tau':>6s} {'n>=':>5s} {'mean d above':>13s} {'cells d>0':>10s} {'t':>7s} | "
          f"{'n<':>5s} {'mean d below':>13s} {'cells d>0':>10s} {'t':>7s} | {'separation':>11s}")
        for _, r in SW[SW.m_min == mm].iterrows():
            P(f"  {r.tau:6.3f} {int(r.n_above):5d} {r.d_above:+13.4f} {r.win_above:10.1%} "
              f"{r.t_above:+7.2f} | {int(r.n_below):5d} "
              f"{'      --     ' if not np.isfinite(r.d_below) else f'{r.d_below:+13.4f}'} "
              f"{'    --    ' if not np.isfinite(r.win_below) else f'{r.win_below:10.1%}'} "
              f"{'   --  ' if not np.isfinite(r.t_below) else f'{r.t_below:+7.2f}'} | "
              f"{r.sep:+11.4f}")

    P("\n  THE CROSSING, read off a local (+-0.075) window on the share axis "
      f"(m_min = {M_MIN_HEADLINE}):")
    Cv = CELLS[CELLS.n_books >= M_MIN_HEADLINE].sort_values("share_mean").reset_index(drop=True)
    grid = np.round(np.arange(0.20, 1.001, 0.025), 4)
    HALF_W, MIN_IN_WIN = 0.075, 5
    sh_all = Cv.share_mean.to_numpy()
    d_all = Cv.d_mean.to_numpy()

    def crossing(sh, d):
        """Smallest share s.t. every local window at or above it has positive mean d.
        Returns (crossing, last non-positive window centre below it)."""
        loc = []
        for g in grid:
            m = (sh >= g - HALF_W) & (sh <= g + HALF_W)
            n = int(m.sum())
            loc.append((g, n, float(d[m].mean()) if n else np.nan,
                        float((d[m] > 0).mean()) if n else np.nan))
        defined = np.array([(nn >= MIN_IN_WIN and np.isfinite(dd)) for _, nn, dd, _ in loc])
        pos = np.array([(np.isfinite(dd) and dd > 0) for _, _, dd, _ in loc])
        ch = np.nan
        for i, g in enumerate(grid):
            if not defined[i] or not pos[i]:
                continue
            if bool(np.all(pos[i:][defined[i:]])):
                ch = float(g)
                break
        below = [g for i, g in enumerate(grid)
                 if defined[i] and not pos[i] and (not np.isfinite(ch) or g < ch)]
        return ch, (max(below) if below else np.nan), loc

    cross_hi, cross_lo, loc_curve = crossing(sh_all, d_all)
    P(f"  {'share':>7s} {'cells in window':>16s} {'local mean d':>13s} {'local cells d>0':>16s}")
    for g, n, d, w in loc_curve:
        P(f"  {g:7.3f} {n:16d} "
          f"{'      --     ' if not np.isfinite(d) else f'{d:+13.4f}'} "
          f"{'       --       ' if not np.isfinite(w) else f'{w:16.1%}'}")
    P(f"\n  crossing: last non-positive local window centre = "
      f"{'n/a' if not np.isfinite(cross_lo) else f'{cross_lo:.3f}'};  "
      f"first share above which EVERY local window is positive = "
      f"{'n/a' if not np.isfinite(cross_hi) else f'{cross_hi:.3f}'}")

    bidx = {k: np.asarray(v) for k, v in
            Cv.groupby(["corpus", "dial", "group"]).indices.items()}
    bk_list = list(bidx.keys())
    rngb = np.random.default_rng(BOOT_SEED)
    boots = []
    for _ in range(N_BOOT):
        pick = rngb.integers(0, len(bk_list), len(bk_list))
        ii = np.concatenate([bidx[bk_list[j]] for j in pick])
        ch, _lo, _c = crossing(sh_all[ii], d_all[ii])
        boots.append(ch)
    bo = np.array([b for b in boots if np.isfinite(b)])
    P(f"  block bootstrap over {len(bk_list)} (corpus,dial,group) blocks, {N_BOOT} draws "
      f"({len(bo)} with a defined crossing): median {np.median(bo):.3f}, "
      f"90% CI [{np.percentile(bo, 5):.3f}, {np.percentile(bo, 95):.3f}]"
      if len(bo) else "  bootstrap: no defined crossing in any draw")

    # ------------------------------------------------ Q5 rule 8 ON THE THRESHOLD ITSELF
    P("\n" + "=" * 118)
    P("Q5  RULE 8 ON THE THRESHOLD.  tau is a fitted parameter.  Choose it on one corpus /")
    P("    one rung and evaluate the GATED arm on the other.  Arm value is reported against")
    P("    SEL-SHARPE (the incumbent fit), paired over books.")
    P("=" * 118)

    def gated_value(train, test, name_train, name_test):
        """tau* chosen to maximise mean d among admitted cells on `train`; the gate is then
        applied cell-by-cell on `test` and scored against always-fitting."""
        best_tau, best_v = np.nan, -np.inf
        for tau in TAU_GRID:
            a = train[train.share_mean >= tau]
            if len(a) < 5:
                continue
            v = float(a.d_mean.sum())          # total value banked by gating at tau
            if v > best_v:
                best_v, best_tau = v, tau
        gate = test[test.share_mean >= best_tau]
        allc = test
        return dict(train=name_train, test=name_test, tau=best_tau,
                    n_test_cells=len(allc), n_gated=len(gate),
                    d_gated=float(gate.d_mean.mean()) if len(gate) else np.nan,
                    win_gated=float(np.mean(gate.d_mean > 0)) if len(gate) else np.nan,
                    d_ungated_all=float(allc.d_mean.mean()),
                    d_if_never_gate=0.0,
                    value_per_cell=float(gate.d_mean.sum() / len(allc)) if len(allc) else np.nan)

    C = CELLS[CELLS.n_books >= M_MIN_HEADLINE]
    wf = []
    wf.append(gated_value(C[C.corpus == "A"], C[C.corpus == "B"], "corpus A", "corpus B"))
    wf.append(gated_value(C[C.corpus == "B"], C[C.corpus == "A"], "corpus B", "corpus A"))
    wf.append(gated_value(C[C.cost_bps == BASE_RUNG], C[C.cost_bps != BASE_RUNG],
                          "10 bps", "5/15/20/25 bps"))
    wf.append(gated_value(C[C.dial.isin(PUBLISHED_VIEWS)], C[~C.dial.isin(PUBLISHED_VIEWS)],
                          "published dials", "extended dials"))
    WF = pd.DataFrame(wf)
    P(f"  {'chosen on':17s} {'evaluated on':17s} {'tau*':>6s} {'cells':>6s} {'gated':>6s} "
      f"{'mean d | gated':>15s} {'gated d>0':>10s} {'value/cell':>11s}")
    for _, r in WF.iterrows():
        P(f"  {r.train:17s} {r.test:17s} {r.tau:6.3f} {int(r.n_test_cells):6d} "
          f"{int(r.n_gated):6d} {r.d_gated:+15.4f} {r.win_gated:10.1%} "
          f"{r.value_per_cell:+11.4f}")

    P("\n  BOOK-LEVEL rule 8: every pick made on IS <= 2016-12-31, OOS >= 2017-01-01 read once.")
    P("  Arms per (corpus, rung, dial view), averaged over the group=ALL books.  GATED-X uses")
    P("  tau* chosen on the OTHER corpus (the row's own corpus never sees it).")
    tauB = float(WF[WF.train == "corpus A"].tau.iloc[0])     # chosen on A, applied to B
    tauA = float(WF[WF.train == "corpus B"].tau.iloc[0])     # chosen on B, applied to A
    TAU_FOR = {"A": tauA, "B": tauB}
    P(f"  tau applied to corpus A = {tauA:.3f} (chosen on B);  "
      f"to corpus B = {tauB:.3f} (chosen on A)")

    arows = []
    for tag in ("A", "B"):
        for cb in RUNGS:
            for view in VIEW_ORDER:
                pk = PACK[(tag, cb, view)]
                nb = len(pk["books"])
                sel = pk["sel"]
                cnt = np.bincount(sel, minlength=len(pk["pts"]))
                share = cnt.max() / nb
                # LOO mode per book (no self-vote)
                loo = np.empty(nb, dtype=int)
                for i in range(nb):
                    c2 = cnt.copy()
                    c2[sel[i]] -= 1
                    loo[i] = int(c2.argmax())
                rngr = np.random.default_rng(219_900 + cb)
                rand = rngr.integers(0, len(pk["pts"]), nb)
                gate_on = share >= TAU_FOR[tag]
                arms = {"SEL-SHARPE": sel, "SEL-4B": pk["sel4b"],
                        "MODE-LOO": loo,
                        "GATED": (loo if gate_on else sel),
                        "CONST-INC": np.full(nb, pk["inc"]),
                        "RANDOM": rand, "ORACLE": pk["orac"]}
                rr = np.arange(nb)
                for arm, pick in arms.items():
                    arows.append(dict(
                        corpus=tag, cost_bps=cb, dial=view, arm=arm,
                        gate_on=bool(gate_on), share=float(share), n=nb,
                        OOS_Sharpe=float(pk["OOS"][rr, pick].mean()),
                        OOS_CAGR=float(pk["OOSC"][rr, pick].mean()),
                        OOS_MaxDD=float(pk["OOSD"][rr, pick].mean()),
                        OOS_margin=float(pk["MAR"][rr, pick].mean()),
                        d_vs_fit=float((pk["OOS"][rr, pick]
                                        - pk["OOS"][rr, sel]).mean())))
    ARM = pd.DataFrame(arows)
    ARM.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    P(f"\n  Pooled over the 7 dial views and 5 rungs (35 cells per corpus):")
    P(f"  {'corpus':7s} {'arm':11s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} {'OOS MaxDD':>10s} "
      f"{'d vs fit':>10s} {'cells d>0':>10s}")
    for tag in ("A", "B"):
        for arm in ["ORACLE", "MODE-LOO", "GATED", "SEL-SHARPE", "SEL-4B", "CONST-INC",
                    "RANDOM"]:
            s = ARM[(ARM.corpus == tag) & (ARM.arm == arm)]
            P(f"  {tag:7s} {arm:11s} {s.OOS_Sharpe.mean():11.4f} {s.OOS_CAGR.mean():9.2%} "
              f"{s.OOS_MaxDD.mean():10.2%} {s.d_vs_fit.mean():+10.4f} "
              f"{np.mean(s.d_vs_fit > 0):10.1%}")

    P(f"\n  Same, restricted to the 5 PUBLISHED dial views at {BASE_RUNG} bps "
      f"(idea 189's own grid):")
    P(f"  {'corpus':7s} {'arm':11s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} {'OOS MaxDD':>10s} "
      f"{'d vs fit':>10s}")
    for tag in ("A", "B"):
        for arm in ["ORACLE", "MODE-LOO", "GATED", "SEL-SHARPE", "CONST-INC", "RANDOM"]:
            s = ARM[(ARM.corpus == tag) & (ARM.arm == arm) & (ARM.cost_bps == BASE_RUNG)
                    & (ARM.dial.isin(PUBLISHED_VIEWS))]
            P(f"  {tag:7s} {arm:11s} {s.OOS_Sharpe.mean():11.4f} {s.OOS_CAGR.mean():9.2%} "
              f"{s.OOS_MaxDD.mean():10.2%} {s.d_vs_fit.mean():+10.4f}")

    P("\n  Which dial views the gate actually switches ON (share >= tau for that corpus):")
    for tag in ("A", "B"):
        s = ARM[(ARM.corpus == tag) & (ARM.arm == "GATED")]
        on = sorted(set(s[s.gate_on].dial))
        off = sorted(set(s[~s.gate_on].dial))
        P(f"    corpus {tag} (tau={TAU_FOR[tag]:.3f}): ON {on or '[none]'} | OFF {off or '[none]'}")

    # -------------------------------------------------------------- benchmarks + KEEP paths
    P("\n" + "=" * 118)
    P("Q6  BENCHMARKS AND BOTH KEEP PATHS")
    P("=" * 118)
    P(f"  {'panel':10s} {'series':12s} {'cost':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
      f"{'OOS MaxDD':>10s}")
    seen = {}
    for nm, panels in [("A", panelsA), ("B", panelsB)]:
        for par, px in panels.items():
            lab = par if par not in seen else f"{par}({nm})"
            if par in seen and px.shape == seen[par]:
                continue                                  # same panel object, already printed
            seen[par] = px.shape
            st = px.index[260]
            spy = px["SPY"].pct_change().fillna(0.0).loc[st:].loc[OOS_START:]
            c, s, dd = _cagr_sh_dd(spy.values)
            P(f"  {lab:10s} {'SPY':12s} {'-':>5s} {c:9.2%} {s:11.4f} {dd:10.2%}")
            br = fast_backtest(px, rules_v1_weights(px), 0.0, "W")
            g = br["returns"].loc[st:].loc[OOS_START:].values
            tn = br["turnover"].loc[st:].loc[OOS_START:].values
            for cb in (10, 25):
                c, s, dd = _cagr_sh_dd(g - tn * cb / 1e4)
                P(f"  {lab:10s} {'RULES v1':12s} {cb:5d} {c:9.2%} {s:11.4f} {dd:10.2%}")

    krows = []
    for tag in ("A", "B"):
        for cb in RUNGS:
            s = lad[(lad.corpus == tag) & (lad.cost_bps == cb)]
            krows.append(dict(corpus=tag, cost_bps=cb, rows=len(s),
                              pass4a=int((s.fail4a == "-").sum()),
                              pass4b=int((s.fail4b == "-").sum())))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  {'corpus':7s} {'cost':>5s} {'rows':>7s} {'4a pass':>8s} {'4b pass':>8s}")
    for _, r in K.iterrows():
        P(f"  {r.corpus:7s} {int(r.cost_bps):5d} {int(r.rows):7d} {int(r.pass4a):8d} "
          f"{int(r.pass4b):8d}")
    P("\n  4b passes by parent panel (all rungs pooled):")
    s = lad[lad.fail4b == "-"]
    tot = lad.groupby("parent").size()
    for par in sorted(lad.parent.unique()):
        P(f"    {par:8s} {int((s.parent == par).sum()):6d} of {int(tot[par]):6d}")
    P("  (idea 144: a re-dialled book is the SAME book -- nothing here is proposed as new.)")

    # --------------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    Ch = CELLS[CELLS.n_books >= M_MIN_HEADLINE]
    rho_all = spearman(Ch.share_mean, Ch.d_mean)
    rho_A = spearman(Ch[Ch.corpus == "A"].share_mean, Ch[Ch.corpus == "A"].d_mean)
    rho_B = spearman(Ch[Ch.corpus == "B"].share_mean, Ch[Ch.corpus == "B"].d_mean)
    gA = ARM[(ARM.corpus == "A") & (ARM.arm == "GATED")].d_vs_fit.mean()
    gB = ARM[(ARM.corpus == "B") & (ARM.arm == "GATED")].d_vs_fit.mean()
    small4b = int((lad[lad.parent == "SMALL"].fail4b == "-").sum())
    preds = [
        ("P1 both parents reproduce at <1e-12, 0 verdict mismatches", repro_ok,
         f"max|d| {max(d189, d217):.2e}, mismatches {v189 + v217}"),
        ("P2 Spearman(share, d) > 0 overall and on both corpora",
         bool(rho_all > 0 and rho_A > 0 and rho_B > 0),
         f"all {rho_all:+.3f}, A {rho_A:+.3f}, B {rho_B:+.3f}"),
        ("P3 crossing strictly inside (0.226, 0.830)",
         bool(np.isfinite(cross_hi) and 0.226 < cross_hi < 0.830),
         f"crossing {cross_hi if np.isfinite(cross_hi) else float('nan'):.3f}"),
        ("P4 crossing below 0.60", bool(np.isfinite(cross_hi) and cross_hi < 0.60),
         f"crossing {cross_hi if np.isfinite(cross_hi) else float('nan'):.3f}"),
        ("P5 GATED beats SEL-SHARPE on both corpora", bool(gA > 0 and gB > 0),
         f"A {gA:+.4f}, B {gB:+.4f}"),
        ("P6 zero 4b passes on SMALL-parent books", small4b == 0, f"{small4b} passes"),
    ]
    hits = 0
    for name, ok, detail in preds:
        hits += int(bool(ok))
        P(f"  [{'HIT ' if ok else 'MISS'}]  {name:<58s}  {detail}")
    P(f"  {hits}/{len(preds)} predictions hit")

    P(f"\nDONE in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
