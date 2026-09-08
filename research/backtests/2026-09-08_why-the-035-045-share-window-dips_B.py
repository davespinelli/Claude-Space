#!/usr/bin/env python3
"""IDEA 226  why-the-035-045-share-window-dips   (lane B, 2026-09-08)

THE QUESTION
------------
Idea 219 killed the modal-share FLOOR and published, as the shape behind that kill, a local
(+-0.075) curve of "held-out mode minus fit" (OOS Sharpe) against the modal share read on the
fitting half.  The curve is positive everywhere except one window:

    share  cells  local mean d          share  cells  local mean d
    0.275     69      +0.0028           0.375    124      -0.0011
    0.300     89      -0.0016           0.400    125      -0.0005
    0.325    105      -0.0030           0.425    122      +0.0004
    0.350    119      -0.0015           0.450    111      +0.0051

and the crossing bootstrap's 90% CI, [0.200, 0.450], has its LOWER limit on the grid's own
edge -- i.e. the dip is what makes the crossing statistic ill-determined.  The queue's own
hypothesis: the window is where the two EXTENDED dial views (BAND+, SLEEVE+) concentrate, so
the hole may be a dial-composition artefact rather than a property of the share axis.

    Q1  REPRODUCTION.  Rebuild idea 219's 560 cells and its 33-point local curve FROM ITS
        COMMITTED LADDER, and match its committed cells.csv before any new number is read.
        Nothing is re-simulated: the ladder (36 120 rows, one 0 bps simulation per book x dial
        x point with the 5 rungs derived by idea 217's exact identity) is the parent's own
        artefact, and the cells are a deterministic function of it plus the parent's seeds.
    Q2  THE QUEUE'S PREMISE, as a checkable claim.  Dial composition of the dip window against
        the dial composition of the whole cell corpus.  Concentration ratio per dial view.
    Q3  THE CURVE, DIAL BY DIAL.  The same local curve computed WITHIN each of the 7 dial
        views.  A hole on the share axis should appear inside dials, not only across them.
    Q4  LEAVE ONE DIAL VIEW OUT.  Seven pooled curves, each dropping one view.  If dropping
        exactly one view removes the dip, the dip is that view's level, not the share axis.
    Q5  HOLD THE MIX FIXED.  Two ways: (a) subtract each dial view's own mean d (dial fixed
        effects) and re-run the pooled curve; (b) direct standardization -- reweight every
        local window's dial mix to the global mix.  Both answer "is there a hole once
        composition cannot move".
    Q6  IS THE HOLE NON-ZERO AT ALL?  The parent read the dip off S=40 seeded splits per cell.
        Re-read it at S=200 (a SUPERSET: the parent's 40 draws are the first 40 of the same
        seeded stream, so the S=40 numbers reproduce exactly inside this run) and block-
        bootstrap the window mean over (corpus, dial, group) blocks.
    Q7  RULE 8.  A dip, if real, is a rule: "fit inside the window, write the mode down
        outside it".  Choose the window on one corpus / one rung, apply it to the other, and
        score the book-level arms on OOS (picks on <= 2016-12-31, 2017-2026 read once)
        against MODE-LOO and SEL-SHARPE, with SPY and RULES v1 beside them.
    Q8  Benchmarks and BOTH KEEP paths on every ladder row.

DESIGN
------
  cell        = (corpus, cost rung, dial view, book group), exactly idea 219's unit
  observation = (modal share on the fitting half, mean over held-out books of
                 OOS_Sharpe(that mode) - OOS_Sharpe(that book's own IS-Sharpe fit))
  positive d  = the held-out mode BEATS the fit
  corpora     A = idea 171's 53 books, B = idea 189's 115 books
  rungs       5/10/15/20/25 bps (idea 217's derived ladder, inherited byte-for-byte)
  views       GROSS, N, BAND, BAND+, CADENCE, SLEEVE, SLEEVE+ (ideas 171/218)
  windows     IS <= 2016-12-31 chooses; OOS >= 2017-01-01 is read ONCE

  TUNED PARAMETER 1: HALF_W, the local half-window on the share axis -- {0.050, 0.075, 0.100,
                     0.125}, ALL reported; the headline is 0.075, inherited from idea 219.
  TUNED PARAMETER 2: m_min, the smallest book group admitted as a cell -- {8, 12, 20, 40},
                     ALL reported; the headline is 12, inherited from idea 219.
  The dip window itself is NOT tuned here: it is fixed a priori at idea 219's published
  non-positive centres [0.300, 0.400] (cells with share in [0.225, 0.475]), with the queue's
  narrower [0.30, 0.42] reported beside it.  The rule-8 window in Q7 is CHOSEN on a training
  corpus/rung over a pre-stated grid and every grid point is reported.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  The rebuilt 560 cells match idea 219's committed cells.csv at max |d| < 1e-12 on every
      numeric column, and the rebuilt local curve reproduces its published crossing (last
      non-positive centre 0.400, first all-positive share 0.425).
  P2  The queue's premise holds as stated: BAND+ and SLEEVE+ are over-represented in the dip
      window by at least 1.5x their share of the whole cell corpus.
  P3  Dial-demeaning removes the dip: the dial-demeaned pooled curve has NO non-positive local
      window centre in [0.275, 0.425].
  P4  At least one single-dial curve has a non-positive local window inside [0.275, 0.425],
      i.e. the hole is not purely a between-dial mix effect.
  P5  Leave-one-out: there is a single dial view whose removal makes every pooled local window
      centre in [0.275, 0.425] positive.
  P6  The window-gated arm does NOT beat MODE-LOO on OOS Sharpe on either corpus (idea 219
      found every share-conditioned gate costs part of the modal constant's value).
  P7  Zero 4b passes on SMALL-parent books at every rung (idea 136, reproduction n+1).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): B136, U56 and both small panels are current-constituent lists.
    Every arm inherits it equally so the PAIRED comparisons are unaffected; every LEVEL is
    biased upward and none is a tradable estimate.
  * Cells are NOT independent: they share books (a k-group is a subset of ALL), share
    simulations across the 5 rungs (one 0 bps run, rungs derived by subtraction), and share
    parents (48 of corpus A's 53 books are B136 sub-panels).  Every t below is over correlated
    units with an optimistic nominal size; the bootstrap resamples whole (corpus, dial, group)
    blocks, and no p-value here is a p-value on a fresh sample.
  * The modal share is estimated on a half-corpus of 4-57 books, so its sampling error is
    LARGEST exactly where the share is lowest -- which is the region under test.  That is a
    property of the statistic, reported not corrected.
  * S=200 splits per cell reduce the split noise but not the corpus noise: the 560 cells are
    draws from ~112 blocks, and no amount of resplitting adds blocks.
  * Corpus A's SMALL484 book is idea 171's, built WITHOUT the max_1d_move >= 1.0 screen;
    corpus B's SMALL439 applies it.  Inherited unchanged (corpus A is the reproduction target).
  * Idea 144 (a re-dialled book is the same book), idea 38's calendar-day index and idea 126's
    t+1-only execution carry over.  Nothing here is proposed as a book.

Deterministic, standalone.  Writes .console.txt, .cells.csv, .curves.csv, .lodo.csv,
.composition.csv, .walkforward.csv, .keep.csv.
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

STEM = "2026-09-08_why-the-035-045-share-window-dips_B"
OUT = ROOT / "research" / "backtests"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
P219_STEM = "2026-09-06_what-modal-share-makes-a-mode-writable_cloud"

RUNGS = [5, 10, 15, 20, 25]
BASE_RUNG = 10
S_PARENT = 40                        # idea 219's split count (reproduction target)
S_SPLITS = 200                       # this run's, a superset of the same seeded stream
M_MINS = [8, 12, 20, 40]             # tuned parameter 2, all reported
M_MIN_HEADLINE = 12
HALF_WS = [0.050, 0.075, 0.100, 0.125]   # tuned parameter 1, all reported
HALF_W_HEADLINE = 0.075
MIN_IN_WIN = 5
GRID = np.round(np.arange(0.20, 1.001, 0.025), 4)
DIP_CENTRES = (0.300, 0.400)         # idea 219's published non-positive window centres
DIP_CELLS = (0.225, 0.475)           # the cells those windows are built from (centre +- 0.075)
QUEUE_WINDOW = (0.300, 0.420)        # the queue's own wording
SPLIT_SEED = 219_500                 # idea 219's, so the first 40 draws reproduce
BOOT_SEED = 226_700
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


p171 = _load(P171_STEM, "p171_226")
p171.P = P
fast_backtest = p171.fast_backtest
IS_END, OOS_START = p171.IS_END, p171.OOS_START
INC = dict(p171.INC)


def _cagr_sh_dd(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    sd = r.std(ddof=1)
    sh = (r.mean() / sd * np.sqrt(252.0)) if sd > 0 else np.nan
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    return float(cagr), float(sh), dd


def tstat(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# ---- dial views (ideas 171 / 218), identical to idea 219's
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


def groups_of(names):
    """idea 219's group definition, verbatim."""
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


def local_curve(sh, d, half_w=HALF_W_HEADLINE, grid=GRID, min_in=MIN_IN_WIN):
    """(centre, n, mean d, share of cells with d>0) at every grid point."""
    sh = np.asarray(sh, float)
    d = np.asarray(d, float)
    rows = []
    for g in grid:
        m = (sh >= g - half_w) & (sh <= g + half_w)
        n = int(m.sum())
        rows.append((float(g), n,
                     float(d[m].mean()) if n >= min_in else np.nan,
                     float((d[m] > 0).mean()) if n >= min_in else np.nan))
    return rows


def crossing_of(loc):
    """(first share above which every defined window is positive, last non-positive centre)."""
    defined = np.array([np.isfinite(r[2]) for r in loc])
    pos = np.array([np.isfinite(r[2]) and r[2] > 0 for r in loc])
    ch = np.nan
    for i, r in enumerate(loc):
        if not defined[i] or not pos[i]:
            continue
        if bool(np.all(pos[i:][defined[i:]])):
            ch = float(r[0])
            break
    below = [r[0] for i, r in enumerate(loc)
             if defined[i] and not pos[i] and (not np.isfinite(ch) or r[0] < ch)]
    return ch, (max(below) if below else np.nan)


def dip_min(loc, lo=DIP_CENTRES[0] - 0.026, hi=DIP_CENTRES[1] + 0.026):
    """Lowest local mean d over defined window centres inside the dip range."""
    v = [r[2] for r in loc if lo <= r[0] <= hi and np.isfinite(r[2])]
    return (min(v), float(np.mean(v)), len(v)) if v else (np.nan, np.nan, 0)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 226  why-the-035-045-share-window-dips   (lane B, 2026-09-08)")
    P("=" * 118)
    P("Unit = idea 219's cell (corpus, rung, dial view, book group).  Nothing is re-simulated:")
    P("the parent's committed 36 120-row ladder IS the simulation, and the cells are a")
    P("deterministic function of it plus the parent's seeds.  10 bps is PROTOCOL's rung; the")
    P("other four are idea 217's derived ladder, carried so the cell corpus keeps its width.")

    # ------------------------------------------------------------------ Q1 reproduction
    lad = pd.read_csv(OUT / f"{P219_STEM}.ladder.csv.gz")
    P(f"\n  ladder loaded: {len(lad)} rows, {lad.book.nunique()} distinct book names, "
      f"rungs {sorted(lad.cost_bps.unique())}")
    NAMES = {tag: list(dict.fromkeys(lad[lad.corpus == tag].book))
             for tag in ("A", "B")}
    P(f"  corpus A {len(NAMES['A'])} books, corpus B {len(NAMES['B'])} books "
      f"(order recovered from the ladder's own row order)")

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
                bk = [n for n in NAMES[tag] if n in piv_is.index]
                piv_is = piv_is.loc[bk, spts]

                def pv(col):
                    return s.pivot(index="book", columns="point",
                                   values=col).loc[bk, spts].to_numpy(float)
                PACK[(tag, cb, view)] = dict(
                    books=bk, pts=pts, spts=spts,
                    IS=piv_is.to_numpy(float), OOS=pv("OOS_Sharpe"), OOSC=pv("OOS_CAGR"),
                    OOSD=pv("OOS_MaxDD"), MAR=pv("OOS_margin"),
                    sel=np.nanargmax(piv_is.to_numpy(float), axis=1),
                    sel4b=np.nanargmax(pv("OOS_margin"), axis=1),
                    orac=np.nanargmax(pv("OOS_Sharpe"), axis=1),
                    inc=(spts.index(str(INC[phys])) if str(INC[phys]) in spts else 0))

    GRP = {tag: groups_of(NAMES[tag]) for tag in ("A", "B")}
    for tag in ("A", "B"):
        P(f"  corpus {tag} groups: " + ", ".join(f"{k}({len(v)})" for k, v in GRP[tag].items()))

    P("\n  building cells: S=200 seeded split-halves x 2 directions per cell, the first 40 of")
    P("  which are idea 219's own draws (same seed stream) and are recorded separately.")
    crows = []
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
                        SPLIT_SEED + zlib.crc32(f"{tag}|{cb}|{view}|{gname}".encode())
                        % 10_000_019)
                    shares, ds, dm, stab = [], [], [], []
                    for _ in range(S_SPLITS):
                        perm = rng.permutation(len(ix))
                        h = len(ix) // 2
                        modes_ = []
                        for fit, held in ((perm[:h], perm[h:]), (perm[h:], perm[:h])):
                            c2 = np.bincount(sel[fit], minlength=len(pk["pts"]))
                            md = int(c2.argmax())
                            modes_.append(md)
                            rows_h = ix[held]
                            shares.append(float(c2.max() / len(fit)))
                            ds.append(float(np.mean(pk["OOS"][rows_h, md]
                                                    - pk["OOS"][rows_h, pk["sel"][rows_h]])))
                            dm.append(float(np.mean(pk["MAR"][rows_h, md]
                                                    - pk["MAR"][rows_h, pk["sel"][rows_h]])))
                        stab.append(modes_[0] == modes_[1])
                    n40 = 2 * S_PARENT
                    crows.append(dict(
                        corpus=tag, cost_bps=cb, dial=view, group=gname, n_books=len(ix),
                        full_mode=str(pk["pts"][full_mode]), full_share=full_share,
                        distinct=int((cnt > 0).sum()),
                        # --- idea 219's S=40 statistics (the reproduction target)
                        share_mean40=float(np.mean(shares[:n40])),
                        share_sd40=float(np.std(shares[:n40])),
                        d_mean40=float(np.mean(ds[:n40])), d_median40=float(np.median(ds[:n40])),
                        d_sd40=float(np.std(ds[:n40])), win40=float(np.mean(np.array(ds[:n40]) > 0)),
                        dmargin_mean40=float(np.mean(dm[:n40])),
                        mode_stable40=float(np.mean(stab[:S_PARENT])),
                        # --- this run's S=200 statistics
                        share_mean=float(np.mean(shares)), share_sd=float(np.std(shares)),
                        d_mean=float(np.mean(ds)), d_median=float(np.median(ds)),
                        d_sd=float(np.std(ds)), win=float(np.mean(np.array(ds) > 0)),
                        dmargin_mean=float(np.mean(dm)), mode_stable=float(np.mean(stab)),
                        published=(cb == BASE_RUNG and gname == "ALL"
                                   and view in PUBLISHED_VIEWS)))
    CELLS = pd.DataFrame(crows)
    CELLS.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    P(f"  {len(CELLS)} cells built in {time.time() - t0:.0f}s "
      f"({len(CELLS) * S_SPLITS * 2} split-half observations)")

    P("\n" + "=" * 118)
    P("Q1  REPRODUCTION of idea 219's committed cells.csv (its S=40 columns), before any new")
    P("    number is read.")
    P("=" * 118)
    par = pd.read_csv(OUT / f"{P219_STEM}.cells.csv")
    key = ["corpus", "cost_bps", "dial", "group"]
    mine = CELLS.rename(columns={
        "share_mean40": "share_mean_r", "share_sd40": "share_sd_r", "d_mean40": "d_mean_r",
        "d_median40": "d_median_r", "d_sd40": "d_sd_r", "win40": "win_r",
        "dmargin_mean40": "dmargin_mean_r", "mode_stable40": "mode_stable_r"})
    M = par.merge(mine, on=key, suffixes=("", "_new"), how="outer", indicator=True)
    P(f"  rows: parent {len(par)}, rebuilt {len(CELLS)}, merged {len(M)}, "
      f"unmatched {int((M._merge != 'both').sum())}")
    cols = [("share_mean", "share_mean_r"), ("share_sd", "share_sd_r"),
            ("d_mean", "d_mean_r"), ("d_median", "d_median_r"), ("d_sd", "d_sd_r"),
            ("win", "win_r"), ("dmargin_mean", "dmargin_mean_r"),
            ("mode_stable", "mode_stable_r"), ("full_share", "full_share_new")]
    worst = 0.0
    P(f"  {'column':16s} {'max |parent - rebuilt|':>24s}")
    for a, b in cols:
        dd = float(np.nanmax(np.abs(M[a].to_numpy(float) - M[b].to_numpy(float))))
        worst = max(worst, dd)
        P(f"  {a:16s} {dd:24.3e}")
    mode_mm = int((M.full_mode.astype(str) != M.full_mode_new.astype(str)).sum())
    P(f"  full_mode string mismatches: {mode_mm} of {len(M)}")
    repro_ok = bool(worst < 1e-12 and mode_mm == 0 and int((M._merge != "both").sum()) == 0)
    P(f"  => REPRODUCTION {'OK' if repro_ok else 'FAILED'}  (max |d| {worst:.3e})")

    Cp = CELLS[CELLS.n_books >= M_MIN_HEADLINE]
    loc40 = local_curve(Cp.share_mean40, Cp.d_mean40)
    ch40, lo40 = crossing_of(loc40)
    P(f"\n  idea 219's own curve, rebuilt (S=40, m_min=12, half-window 0.075):")
    P(f"    crossing = {ch40:.3f} (published 0.425);  last non-positive centre = "
      f"{lo40:.3f} (published 0.400)")
    P(f"  {'centre':>7s} {'n':>6s} {'mean d':>10s} {'d>0':>8s}   (published values in brackets)")
    pub = {0.300: -0.0016, 0.325: -0.0030, 0.350: -0.0015, 0.375: -0.0011, 0.400: -0.0005,
           0.425: +0.0004, 0.450: +0.0051}
    for g, n, d, w in loc40:
        if 0.275 <= g <= 0.475:
            tagp = f"   [{pub[g]:+.4f}]" if g in pub else ""
            P(f"  {g:7.3f} {n:6d} {d:+10.4f} {w:8.1%}{tagp}")
    curve_ok = bool(abs(ch40 - 0.425) < 1e-9 and abs(lo40 - 0.400) < 1e-9)
    P(f"  => CURVE REPRODUCTION {'OK' if curve_ok else 'FAILED'}")

    # ---------------------------------------------------------------- Q2 the queue's premise
    P("\n" + "=" * 118)
    P("Q2  THE QUEUE'S PREMISE.  'The window is where BAND+ and SLEEVE+ concentrate.'")
    P(f"    Dip cells = share in [{DIP_CELLS[0]:.3f}, {DIP_CELLS[1]:.3f}] (the cells feeding")
    P(f"    idea 219's non-positive centres {DIP_CENTRES[0]:.3f}-{DIP_CENTRES[1]:.3f});")
    P(f"    the queue's narrower window [{QUEUE_WINDOW[0]:.2f}, {QUEUE_WINDOW[1]:.2f}] beside it.")
    P("=" * 118)
    C = CELLS[CELLS.n_books >= M_MIN_HEADLINE].copy()
    in_dip = (C.share_mean >= DIP_CELLS[0]) & (C.share_mean <= DIP_CELLS[1])
    in_q = (C.share_mean >= QUEUE_WINDOW[0]) & (C.share_mean <= QUEUE_WINDOW[1])
    comp = []
    P(f"  {'dial':9s} {'cells':>6s} {'all %':>8s} | {'dip n':>6s} {'dip %':>8s} {'conc':>6s} "
      f"{'dip mean d':>11s} | {'queue n':>8s} {'queue %':>8s} {'conc':>6s} | "
      f"{'dial mean d':>12s}")
    for view in VIEW_ORDER:
        s = C[C.dial == view]
        a_p = len(s) / len(C)
        dsub = C[in_dip & (C.dial == view)]
        qsub = C[in_q & (C.dial == view)]
        d_p = len(dsub) / max(int(in_dip.sum()), 1)
        q_p = len(qsub) / max(int(in_q.sum()), 1)
        comp.append(dict(dial=view, n_all=len(s), pct_all=a_p, n_dip=len(dsub), pct_dip=d_p,
                         conc_dip=d_p / a_p if a_p else np.nan, n_queue=len(qsub),
                         pct_queue=q_p, conc_queue=q_p / a_p if a_p else np.nan,
                         dip_mean_d=float(dsub.d_mean.mean()) if len(dsub) else np.nan,
                         dial_mean_d=float(s.d_mean.mean())))
        P(f"  {view:9s} {len(s):6d} {a_p:8.1%} | {len(dsub):6d} {d_p:8.1%} "
          f"{(d_p / a_p if a_p else np.nan):6.2f} "
          f"{(dsub.d_mean.mean() if len(dsub) else np.nan):+11.4f} | "
          f"{len(qsub):8d} {q_p:8.1%} {(q_p / a_p if a_p else np.nan):6.2f} | "
          f"{s.d_mean.mean():+12.4f}")
    COMP = pd.DataFrame(comp)
    COMP.to_csv(OUT / f"{STEM}.composition.csv", index=False)
    ext_conc = float(COMP[COMP.dial.isin(["BAND+", "SLEEVE+"])].n_dip.sum()
                     / max(int(in_dip.sum()), 1)) / float(
        COMP[COMP.dial.isin(["BAND+", "SLEEVE+"])].n_all.sum() / len(C))
    P(f"\n  BAND+ and SLEEVE+ together: {COMP[COMP.dial.isin(['BAND+','SLEEVE+'])].n_dip.sum()}"
      f" of {int(in_dip.sum())} dip cells "
      f"({COMP[COMP.dial.isin(['BAND+','SLEEVE+'])].n_dip.sum()/max(int(in_dip.sum()),1):.1%}) "
      f"vs {COMP[COMP.dial.isin(['BAND+','SLEEVE+'])].n_all.sum()} of {len(C)} overall "
      f"({COMP[COMP.dial.isin(['BAND+','SLEEVE+'])].n_all.sum()/len(C):.1%}); "
      f"concentration {ext_conc:.2f}x")
    P("  corpus / rung composition of the dip window (the other two axes, for completeness):")
    for axis in ("corpus", "cost_bps"):
        for v in sorted(C[axis].unique()):
            a_p = float((C[axis] == v).mean())
            d_p = float((C[in_dip][axis] == v).mean())
            P(f"    {axis:9s} {str(v):>4s}: all {a_p:6.1%}  dip {d_p:6.1%}  "
              f"conc {d_p / a_p if a_p else np.nan:5.2f}")

    # ------------------------------------------------------------------ Q3 dial by dial
    P("\n" + "=" * 118)
    P("Q3  THE CURVE, DIAL BY DIAL.  The same local curve inside each dial view.  A hole on the")
    P("    SHARE axis must appear within dials, not only across them.")
    P("=" * 118)
    curve_rows = []
    P(f"  {'dial':9s} {'cells':>6s} {'share range':>16s} {'defined centres':>16s} "
      f"{'min d in dip':>13s} {'mean d in dip':>14s} {'crossing':>9s} {'dip windows<=0':>15s}")
    for view in VIEW_ORDER:
        s = C[C.dial == view]
        loc = local_curve(s.share_mean, s.d_mean)
        for g, n, d, w in loc:
            curve_rows.append(dict(scope=f"dial:{view}", centre=g, n=n, mean_d=d, win=w))
        ch, lo = crossing_of(loc)
        mn, mean_, ndef = dip_min(loc)
        nneg = sum(1 for r in loc if DIP_CENTRES[0] - 0.026 <= r[0] <= DIP_CENTRES[1] + 0.026
                   and np.isfinite(r[2]) and r[2] <= 0)
        P(f"  {view:9s} {len(s):6d} "
          f"{f'{s.share_mean.min():.3f}-{s.share_mean.max():.3f}':>16s} {ndef:16d} "
          f"{mn:+13.4f} {mean_:+14.4f} "
          f"{('n/a' if not np.isfinite(ch) else f'{ch:.3f}'):>9s} {nneg:15d}")
    P("\n  Full per-dial local curves over the dip range:")
    P(f"  {'centre':>7s} " + " ".join(f"{v:>10s}" for v in VIEW_ORDER))
    percurve = {v: {r[0]: r for r in local_curve(C[C.dial == v].share_mean,
                                                 C[C.dial == v].d_mean)} for v in VIEW_ORDER}
    for g in GRID:
        if not (0.250 <= g <= 0.500):
            continue
        cells = []
        for v in VIEW_ORDER:
            r = percurve[v][float(g)]
            cells.append("    --    " if not np.isfinite(r[2]) else f"{r[2]:+10.4f}")
        P(f"  {g:7.3f} " + " ".join(cells))
    P(f"  (n in each window: " + ", ".join(
        f"{v}={[int(percurve[v][float(g)][1]) for g in GRID if 0.30 <= g <= 0.40]}"
        for v in VIEW_ORDER) + ")")

    # ------------------------------------------------------------ Q4 leave one dial out
    P("\n" + "=" * 118)
    P("Q4  LEAVE ONE DIAL VIEW OUT.  Seven pooled curves; if removing exactly one view removes")
    P("    the dip, the dip is that view's LEVEL, not a property of the share axis.")
    P("=" * 118)
    lodo_rows = []
    loc_all = local_curve(C.share_mean, C.d_mean)
    for g, n, d, w in loc_all:
        curve_rows.append(dict(scope="pooled", centre=g, n=n, mean_d=d, win=w))
    ch_all, lo_all = crossing_of(loc_all)
    mn_all, mean_all, _ = dip_min(loc_all)
    nneg_all = sum(1 for r in loc_all if DIP_CENTRES[0] - 0.026 <= r[0] <= DIP_CENTRES[1] + 0.026
                   and np.isfinite(r[2]) and r[2] <= 0)
    P(f"  {'dropped':9s} {'cells':>6s} {'min d in dip':>13s} {'mean d in dip':>14s} "
      f"{'windows<=0':>11s} {'crossing':>9s} {'last<=0':>9s}")
    P(f"  {'[none]':9s} {len(C):6d} {mn_all:+13.4f} {mean_all:+14.4f} {nneg_all:11d} "
      f"{('n/a' if not np.isfinite(ch_all) else f'{ch_all:.3f}'):>9s} "
      f"{('n/a' if not np.isfinite(lo_all) else f'{lo_all:.3f}'):>9s}")
    lodo_rows.append(dict(dropped="[none]", n=len(C), min_d=mn_all, mean_d=mean_all,
                          n_neg=nneg_all, crossing=ch_all, last_neg=lo_all))
    for view in VIEW_ORDER:
        s = C[C.dial != view]
        loc = local_curve(s.share_mean, s.d_mean)
        for g, n, d, w in loc:
            curve_rows.append(dict(scope=f"drop:{view}", centre=g, n=n, mean_d=d, win=w))
        ch, lo = crossing_of(loc)
        mn, mean_, _ = dip_min(loc)
        nneg = sum(1 for r in loc if DIP_CENTRES[0] - 0.026 <= r[0] <= DIP_CENTRES[1] + 0.026
                   and np.isfinite(r[2]) and r[2] <= 0)
        lodo_rows.append(dict(dropped=view, n=len(s), min_d=mn, mean_d=mean_, n_neg=nneg,
                              crossing=ch, last_neg=lo))
        P(f"  {view:9s} {len(s):6d} {mn:+13.4f} {mean_:+14.4f} {nneg:11d} "
          f"{('n/a' if not np.isfinite(ch) else f'{ch:.3f}'):>9s} "
          f"{('n/a' if not np.isfinite(lo) else f'{lo:.3f}'):>9s}")
    LODO = pd.DataFrame(lodo_rows)

    # ----------------------------------------------------------- Q5 hold the mix fixed
    P("\n" + "=" * 118)
    P("Q5  HOLD THE MIX FIXED.  (a) dial fixed effects removed from d; (b) each local window's")
    P("    dial mix re-weighted to the global mix (direct standardisation).")
    P("=" * 118)
    C = C.copy()
    C["d_dm"] = C.d_mean - C.groupby("dial").d_mean.transform("mean")
    loc_dm = local_curve(C.share_mean, C.d_dm)
    for g, n, d, w in loc_dm:
        curve_rows.append(dict(scope="dial-demeaned", centre=g, n=n, mean_d=d, win=w))
    ch_dm, lo_dm = crossing_of(loc_dm)
    mn_dm, mean_dm, _ = dip_min(loc_dm)

    wglob = C.dial.value_counts(normalize=True)
    std_rows = []
    for g in GRID:
        m = (C.share_mean >= g - HALF_W_HEADLINE) & (C.share_mean <= g + HALF_W_HEADLINE)
        s = C[m]
        if len(s) < MIN_IN_WIN:
            std_rows.append((float(g), len(s), np.nan, np.nan))
            continue
        per = s.groupby("dial").d_mean.mean()
        wt = wglob.reindex(per.index)
        wt = wt / wt.sum()
        std_rows.append((float(g), len(s), float((per * wt).sum()), float(s.d_mean.mean())))
    for g, n, d, raw in std_rows:
        curve_rows.append(dict(scope="standardised", centre=g, n=n, mean_d=d, win=np.nan))
    std_loc = [(g, n, d, np.nan) for g, n, d, _ in std_rows]
    ch_st, lo_st = crossing_of(std_loc)
    mn_st, mean_st, _ = dip_min(std_loc)

    P(f"  {'centre':>7s} {'n':>6s} {'raw':>10s} {'dial-demeaned':>14s} {'standardised':>13s} "
      f"{'dials in win':>13s}")
    for i, g in enumerate(GRID):
        if not (0.250 <= g <= 0.500):
            continue
        r0 = loc_all[i]
        r1 = loc_dm[i]
        r2 = std_rows[i]
        m = (C.share_mean >= g - HALF_W_HEADLINE) & (C.share_mean <= g + HALF_W_HEADLINE)
        P(f"  {g:7.3f} {r0[1]:6d} "
          f"{('    --    ' if not np.isfinite(r0[2]) else f'{r0[2]:+10.4f}')} "
          f"{('      --      ' if not np.isfinite(r1[2]) else f'{r1[2]:+14.4f}')} "
          f"{('     --      ' if not np.isfinite(r2[2]) else f'{r2[2]:+13.4f}')} "
          f"{int(C[m].dial.nunique()):13d}")
    P(f"\n  raw           : min d in dip {mn_all:+.4f}, mean {mean_all:+.4f}, "
      f"crossing {ch_all if np.isfinite(ch_all) else float('nan'):.3f}")
    P(f"  dial-demeaned : min d in dip {mn_dm:+.4f}, mean {mean_dm:+.4f}, "
      f"crossing {ch_dm if np.isfinite(ch_dm) else float('nan'):.3f}")
    P(f"  standardised  : min d in dip {mn_st:+.4f}, mean {mean_st:+.4f}, "
      f"crossing {ch_st if np.isfinite(ch_st) else float('nan'):.3f}")

    P("\n  BOTH TUNED PARAMETERS, every grid point: min local mean d inside the dip range,")
    P("  raw / dial-demeaned, over half-window x m_min.")
    P(f"  {'m_min':>6s} {'half_w':>7s} {'cells':>6s} {'raw min':>10s} {'raw mean':>10s} "
      f"{'dm min':>10s} {'dm mean':>10s} {'raw cross':>10s} {'dm cross':>9s}")
    for mm in M_MINS:
        Cm = CELLS[CELLS.n_books >= mm].copy()
        Cm["d_dm"] = Cm.d_mean - Cm.groupby("dial").d_mean.transform("mean")
        for hw in HALF_WS:
            l0 = local_curve(Cm.share_mean, Cm.d_mean, half_w=hw)
            l1 = local_curve(Cm.share_mean, Cm.d_dm, half_w=hw)
            a0, b0, _ = dip_min(l0)
            a1, b1, _ = dip_min(l1)
            c0, _ = crossing_of(l0)
            c1, _ = crossing_of(l1)
            P(f"  {mm:6d} {hw:7.3f} {len(Cm):6d} {a0:+10.4f} {b0:+10.4f} {a1:+10.4f} "
              f"{b1:+10.4f} {('n/a' if not np.isfinite(c0) else f'{c0:.3f}'):>10s} "
              f"{('n/a' if not np.isfinite(c1) else f'{c1:.3f}'):>9s}")
    pd.DataFrame(curve_rows).to_csv(OUT / f"{STEM}.curves.csv", index=False)
    LODO.to_csv(OUT / f"{STEM}.lodo.csv", index=False)

    # ------------------------------------------------------- Q6 is the hole non-zero at all
    P("\n" + "=" * 118)
    P("Q6  IS THE HOLE NON-ZERO?  Block bootstrap over (corpus, dial, group) blocks on the dip")
    P("    window's mean d, raw and dial-demeaned, at S=40 (idea 219's precision) and S=200.")
    P("=" * 118)
    bidx = {k: np.asarray(v) for k, v in C.groupby(["corpus", "dial", "group"]).indices.items()}
    keys = list(bidx.keys())
    Ci = C.reset_index(drop=True)
    bidx = {k: np.asarray(v) for k, v in Ci.groupby(["corpus", "dial", "group"]).indices.items()}
    keys = list(bidx.keys())
    dipm = ((Ci.share_mean >= DIP_CELLS[0]) & (Ci.share_mean <= DIP_CELLS[1])).to_numpy()
    P(f"  {'statistic':22s} {'n cells':>8s} {'mean':>10s} {'t':>8s} {'90% CI (block boot)':>26s}")
    for label, col, mask in [
            ("dip raw S=40", Ci.d_mean40.to_numpy(), dipm),
            ("dip raw S=200", Ci.d_mean.to_numpy(), dipm),
            ("dip dial-demeaned", Ci.d_dm.to_numpy(), dipm),
            ("outside dip S=200", Ci.d_mean.to_numpy(), ~dipm)]:
        rngb = np.random.default_rng(BOOT_SEED)
        obs = float(np.mean(col[mask]))
        bs = []
        for _ in range(N_BOOT):
            pick = rngb.integers(0, len(keys), len(keys))
            ii = np.concatenate([bidx[keys[j]] for j in pick])
            ii = ii[mask[ii]]
            if len(ii):
                bs.append(float(np.mean(col[ii])))
        bs = np.array(bs)
        P(f"  {label:22s} {int(mask.sum()):8d} {obs:+10.4f} {tstat(col[mask]):+8.2f} "
          f"{f'[{np.percentile(bs,5):+.4f}, {np.percentile(bs,95):+.4f}]':>26s}")
    P("\n  Split noise removed: the S=40 -> S=200 change in the dip window's mean d is")
    P(f"  {float(np.mean(Ci.d_mean.to_numpy()[dipm]) - np.mean(Ci.d_mean40.to_numpy()[dipm])):+.5f}"
      f", i.e. the dip is not a resampling accident of the parent's 40 draws.")

    P("\n  The DEEPEST local window itself (the statistic the dip actually is), and the two")
    P("  windows flanking it, each bootstrapped over the same blocks:")
    P(f"  {'window (cells)':22s} {'n cells':>8s} {'raw mean':>10s} {'t':>7s} "
      f"{'90% CI':>22s} {'demeaned':>10s} {'t':>7s} {'90% CI':>22s}")
    for centre in (0.250, 0.325, 0.400, 0.475, 0.550):
        m = ((Ci.share_mean >= centre - HALF_W_HEADLINE)
             & (Ci.share_mean <= centre + HALF_W_HEADLINE)).to_numpy()
        if m.sum() < MIN_IN_WIN:
            continue
        cells_lab = f"[{centre - HALF_W_HEADLINE:.3f},{centre + HALF_W_HEADLINE:.3f}]"
        out = [cells_lab, int(m.sum())]
        txt = f"  {cells_lab:22s} {int(m.sum()):8d}"
        for col in (Ci.d_mean.to_numpy(), Ci.d_dm.to_numpy()):
            rngb = np.random.default_rng(BOOT_SEED)
            bs = []
            for _ in range(N_BOOT):
                pick = rngb.integers(0, len(keys), len(keys))
                ii = np.concatenate([bidx[keys[j]] for j in pick])
                ii = ii[m[ii]]
                if len(ii):
                    bs.append(float(np.mean(col[ii])))
            bs = np.array(bs)
            txt += (f" {float(np.mean(col[m])):+10.4f} {tstat(col[m]):+7.2f} "
                    f"{f'[{np.percentile(bs, 5):+.4f}, {np.percentile(bs, 95):+.4f}]':>22s}")
        P(txt)
    P("  A window whose 90% CI covers 0 is an ABSENCE of the modal constant's edge, not a")
    P("  region where writing the mode down loses.")

    # ------------------------------------------------------------------------ Q7 rule 8
    P("\n" + "=" * 118)
    P("Q7  RULE 8.  A dip is a RULE: 'fit inside the window, write the mode down outside it'.")
    P("    The window is chosen on one corpus and applied to the other (and chosen at 10 bps")
    P("    and applied to the other four rungs).  Every grid point of the chooser is reported.")
    P("=" * 118)
    WGRID = [(lo, hi) for lo in np.round(np.arange(0.20, 0.601, 0.025), 4)
             for hi in np.round(np.arange(0.20, 0.601, 0.025), 4)
             if 0 < hi - lo <= 0.2501]
    P(f"  window grid: {len(WGRID)} (lo, hi) pairs on the 0.025 grid, lo,hi in [0.20, 0.60],")
    P("  width <= 0.25.  Value of a window on a cell set = mean over cells of the d it banks")
    P("  (0 inside the window where the rule falls back to the fit, d outside).")

    def window_value(sub, lo, hi):
        out = sub[(sub.share_mean < lo) | (sub.share_mean > hi)]
        return float(out.d_mean.sum() / len(sub)) if len(sub) else np.nan

    def best_window(sub):
        best, bv = None, -np.inf
        for lo, hi in WGRID:
            v = window_value(sub, lo, hi)
            if np.isfinite(v) and v > bv:
                bv, best = v, (lo, hi)
        return best, bv

    wf_rows = []
    P(f"\n  {'train':16s} {'window*':>16s} {'train value':>12s} | {'test':16s} "
      f"{'test value':>11s} {'always-mode':>12s} {'window - mode':>14s}")
    splits = [("corpus A", Ci[Ci.corpus == "A"], "corpus B", Ci[Ci.corpus == "B"]),
              ("corpus B", Ci[Ci.corpus == "B"], "corpus A", Ci[Ci.corpus == "A"]),
              ("10 bps", Ci[Ci.cost_bps == 10], "5/15/20/25 bps", Ci[Ci.cost_bps != 10]),
              ("published views", Ci[Ci.dial.isin(PUBLISHED_VIEWS)],
               "extended views", Ci[~Ci.dial.isin(PUBLISHED_VIEWS)])]
    for ntr, tr, nte, te in splits:
        (lo, hi), tv = best_window(tr)
        vte = window_value(te, lo, hi)
        vmode = float(te.d_mean.mean())
        wf_rows.append(dict(train=ntr, test=nte, lo=lo, hi=hi, train_value=tv,
                            test_value=vte, always_mode=vmode, delta=vte - vmode))
        P(f"  {ntr:16s} {f'[{lo:.3f},{hi:.3f}]':>16s} {tv:+12.4f} | {nte:16s} "
          f"{vte:+11.4f} {vmode:+12.4f} {vte - vmode:+14.4f}")
    (lo0, hi0) = (DIP_CELLS[0], DIP_CELLS[1])
    P(f"\n  the FIXED a-priori window [{lo0:.3f}, {hi0:.3f}] (idea 219's published dip), applied")
    P("  without any fitting:")
    for ntag, sub in [("corpus A", Ci[Ci.corpus == "A"]), ("corpus B", Ci[Ci.corpus == "B"]),
                      ("all cells", Ci)]:
        v = window_value(sub, lo0, hi0)
        vm = float(sub.d_mean.mean())
        wf_rows.append(dict(train="fixed [0.225,0.475]", test=ntag, lo=lo0, hi=hi0,
                            train_value=np.nan, test_value=v, always_mode=vm, delta=v - vm))
        P(f"    {ntag:12s} window {v:+.4f}   always-mode {vm:+.4f}   delta {v - vm:+.4f}")

    P("\n  BOOK-LEVEL rule 8: every pick made on IS <= 2016-12-31, OOS >= 2017-01-01 read once.")
    P("  Arms per (corpus, rung, dial view) over the group=ALL books.  WINDOW-X uses the")
    P("  window fitted on the OTHER corpus; WINDOW-FIX uses the a-priori [0.225, 0.475].")
    wA = [r for r in wf_rows if r["train"] == "corpus B"][0]        # chosen on B, applied to A
    wB = [r for r in wf_rows if r["train"] == "corpus A"][0]        # chosen on A, applied to B
    WIN_FOR = {"A": (wA["lo"], wA["hi"]), "B": (wB["lo"], wB["hi"])}
    P(f"  window applied to corpus A = [{WIN_FOR['A'][0]:.3f}, {WIN_FOR['A'][1]:.3f}] "
      f"(chosen on B);  to corpus B = [{WIN_FOR['B'][0]:.3f}, {WIN_FOR['B'][1]:.3f}] "
      f"(chosen on A)")
    arows = []
    for tag in ("A", "B"):
        for cb in RUNGS:
            for view in VIEW_ORDER:
                pk = PACK[(tag, cb, view)]
                nb = len(pk["books"])
                sel = pk["sel"]
                cnt = np.bincount(sel, minlength=len(pk["pts"]))
                share = cnt.max() / nb
                loo = np.empty(nb, dtype=int)
                for i in range(nb):
                    c2 = cnt.copy()
                    c2[sel[i]] -= 1
                    loo[i] = int(c2.argmax())
                rngr = np.random.default_rng(226_900 + cb)
                rand = rngr.integers(0, len(pk["pts"]), nb)
                lo_t, hi_t = WIN_FOR[tag]
                in_win_x = bool(lo_t <= share <= hi_t)
                in_win_f = bool(lo0 <= share <= hi0)
                arms = {"SEL-SHARPE": sel, "SEL-4B": pk["sel4b"], "MODE-LOO": loo,
                        "WINDOW-X": (sel if in_win_x else loo),
                        "WINDOW-FIX": (sel if in_win_f else loo),
                        "CONST-INC": np.full(nb, pk["inc"]), "RANDOM": rand,
                        "ORACLE": pk["orac"]}
                rr = np.arange(nb)
                for arm, pick in arms.items():
                    arows.append(dict(
                        corpus=tag, cost_bps=cb, dial=view, arm=arm, share=float(share),
                        in_window_x=in_win_x, in_window_fix=in_win_f, n=nb,
                        OOS_Sharpe=float(pk["OOS"][rr, pick].mean()),
                        OOS_CAGR=float(pk["OOSC"][rr, pick].mean()),
                        OOS_MaxDD=float(pk["OOSD"][rr, pick].mean()),
                        OOS_margin=float(pk["MAR"][rr, pick].mean()),
                        d_vs_fit=float((pk["OOS"][rr, pick] - pk["OOS"][rr, sel]).mean()),
                        d_vs_mode=float((pk["OOS"][rr, pick] - pk["OOS"][rr, loo]).mean())))
    ARM = pd.DataFrame(arows)
    ARM.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  Pooled over 7 dial views x 5 rungs (35 cells per corpus):")
    P(f"  {'corpus':7s} {'arm':11s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} {'OOS MaxDD':>10s} "
      f"{'d vs fit':>10s} {'d vs mode':>11s}")
    for tag in ("A", "B"):
        for arm in ["ORACLE", "MODE-LOO", "WINDOW-X", "WINDOW-FIX", "SEL-SHARPE", "SEL-4B",
                    "CONST-INC", "RANDOM"]:
            s = ARM[(ARM.corpus == tag) & (ARM.arm == arm)]
            P(f"  {tag:7s} {arm:11s} {s.OOS_Sharpe.mean():11.4f} {s.OOS_CAGR.mean():9.2%} "
              f"{s.OOS_MaxDD.mean():10.2%} {s.d_vs_fit.mean():+10.4f} "
              f"{s.d_vs_mode.mean():+11.4f}")
    P(f"\n  Same at {BASE_RUNG} bps (PROTOCOL's rung) on the 5 published views:")
    P(f"  {'corpus':7s} {'arm':11s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} {'OOS MaxDD':>10s} "
      f"{'d vs mode':>11s}")
    for tag in ("A", "B"):
        for arm in ["ORACLE", "MODE-LOO", "WINDOW-X", "WINDOW-FIX", "SEL-SHARPE", "CONST-INC"]:
            s = ARM[(ARM.corpus == tag) & (ARM.arm == arm) & (ARM.cost_bps == BASE_RUNG)
                    & (ARM.dial.isin(PUBLISHED_VIEWS))]
            P(f"  {tag:7s} {arm:11s} {s.OOS_Sharpe.mean():11.4f} {s.OOS_CAGR.mean():9.2%} "
              f"{s.OOS_MaxDD.mean():10.2%} {s.d_vs_mode.mean():+11.4f}")
    P("\n  Which (corpus, rung, view) cells the fitted window actually switches to the FIT:")
    for tag in ("A", "B"):
        s = ARM[(ARM.corpus == tag) & (ARM.arm == "WINDOW-X")]
        on = sorted(set(s[s.in_window_x].dial))
        P(f"    corpus {tag}: fit inside window for {on or '[none]'}  "
          f"({int(s.in_window_x.sum())} of {len(s)} cells)")

    # ----------------------------------------------------- Q8 benchmarks and KEEP paths
    P("\n" + "=" * 118)
    P("Q8  BENCHMARKS (OOS 2017-2026) AND BOTH KEEP PATHS")
    P("=" * 118)
    P(f"  {'panel':10s} {'series':12s} {'cost':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
      f"{'OOS MaxDD':>10s}")
    for lab, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]:
        px = load_universe(**kw)
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
    sp = lad[lad.fail4b == "-"]
    tot = lad.groupby("parent").size()
    for parn in sorted(lad.parent.unique()):
        P(f"    {parn:8s} {int((sp.parent == parn).sum()):6d} of {int(tot[parn]):6d}")
    small4b = int((lad[lad.parent == "SMALL"].fail4b == "-").sum())
    P("  (idea 144: a re-dialled book is the SAME book -- nothing here is proposed as a book;")
    P("   the ladder is idea 219's committed artefact and its KEEP counts are re-read, not new.)")

    # --------------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    ext = COMP[COMP.dial.isin(["BAND+", "SLEEVE+"])]
    p2 = bool((ext.conc_dip >= 1.5).all())
    p3 = bool(all(not (np.isfinite(r[2]) and r[2] <= 0)
                  for r in loc_dm if 0.275 <= r[0] <= 0.425))
    dial_neg = [v for v in VIEW_ORDER
                if any(np.isfinite(percurve[v][float(g)][2]) and percurve[v][float(g)][2] <= 0
                       for g in GRID if 0.275 <= g <= 0.425)]
    p4 = len(dial_neg) >= 1
    fixers = [r["dropped"] for _, r in LODO.iterrows()
              if r["dropped"] != "[none]" and r["n_neg"] == 0]
    p5 = len(fixers) >= 1
    gA = float(ARM[(ARM.corpus == "A") & (ARM.arm == "WINDOW-X")].d_vs_mode.mean())
    gB = float(ARM[(ARM.corpus == "B") & (ARM.arm == "WINDOW-X")].d_vs_mode.mean())
    p6 = bool(gA <= 0 and gB <= 0)
    preds = [
        ("P1 cells + curve reproduce idea 219 (<1e-12, crossing 0.425/0.400)",
         bool(repro_ok and curve_ok), f"max|d| {worst:.2e}, crossing {ch40:.3f}/{lo40:.3f}"),
        ("P2 BAND+ and SLEEVE+ each >=1.5x concentrated in the dip", p2,
         ", ".join(f"{r.dial} {r.conc_dip:.2f}x" for _, r in ext.iterrows())),
        ("P3 dial-demeaning removes the dip", p3,
         f"min dial-demeaned d in dip {mn_dm:+.4f}"),
        ("P4 >=1 single-dial curve is non-positive inside the dip", p4,
         f"{dial_neg or '[none]'}"),
        ("P5 dropping ONE view makes every dip window positive", p5,
         f"{fixers or '[none]'}"),
        ("P6 WINDOW-X does not beat MODE-LOO on either corpus", p6,
         f"A {gA:+.4f}, B {gB:+.4f}"),
        ("P7 zero 4b passes on SMALL-parent books", small4b == 0, f"{small4b} passes"),
    ]
    hits = 0
    for name, ok, detail in preds:
        hits += int(bool(ok))
        P(f"  [{'HIT ' if ok else 'MISS'}]  {name:<62s}  {detail}")
    P(f"  {hits}/{len(preds)} predictions hit")

    P(f"\nDONE in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
