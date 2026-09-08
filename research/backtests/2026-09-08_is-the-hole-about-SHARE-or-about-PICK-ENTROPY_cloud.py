#!/usr/bin/env python3
"""QUEUE idea 438 — is-the-hole-about-SHARE-or-about-PICK-ENTROPY   (cloud, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 226 found the dip at share 0.25-0.42 is real inside dials and DEEPENS under dial fixed
effects, i.e. it is not a mix effect.  But modal share is a one-number summary of a whole pick
distribution, and at share ~0.35 the remaining mass can sit on 2 arms or on 9.  Re-run idea 226's
curve against pick ENTROPY and against the distinct-pick count instead of the share, on the same
560 cells, and report which of the three separates the +0.0076 region from the zero region most
cleanly.  Max 2 params (statistic, half-window)."

What is on trial.  Not a book: ONE X-AXIS.  Idea 219/226 read the writability of a dial mode off
the MODAL SHARE of the pick distribution.  The queue's point is that modal share throws away the
shape of the rest of the distribution.  If entropy or the distinct-pick count orders `d` (the
held-out-mode OOS Sharpe minus the per-book-fit OOS Sharpe) more cleanly than share does, then the
record has been reading the wrong statistic for 3 ideas; if share wins, the record's x-axis is
vindicated and the extra shape is noise.

THE SUBSTRATE.  Idea 219's committed `ladder.csv.gz` (36 120 rows) and `cells.csv` (560 cells) are
READ, not re-simulated.  Q1 rebuilds all 560 cells from the ladder alone — the seeded split-half
design, the picks, the modal shares, the d's — and asserts an EXACT match (< 1e-12) against the
committed cells on nine columns before any new number is read.  That gate matters more here than
in 226: the new statistics (entropy, distinct count) are computed on the SAME 80 half-samples that
produced `d`, so if the halves reproduce exactly, the three statistics are strictly comparable and
nothing in the contrast is a re-simulation artefact.

  Q1  REPRODUCTION.  Rebuild the 560 cells from `ladder.csv.gz`; assert 9 columns to < 1e-12 and
      re-derive idea 226's 33-point published local curve.
  Q2  THE THREE STATISTICS (six, with the two scale-corrections the queue does not name).  For
      every cell, on the same fitting halves: modal SHARE, pick ENTROPY in bits (raw, normalised
      by log2 K, and Miller-Madow bias-corrected), and the DISTINCT pick count (raw and /K).
      Then the queue's own premise as a measurement: at share 0.30-0.42, how much does the
      distinct count actually vary?
  Q3  THE THREE CURVES.  Idea 226's local curve of mean d, recomputed against each statistic on a
      common [0,1] scale (each statistic divided by its own A-PRIORI maximum, never an empirical
      range — an empirical range would be fitted on the outcome).  For SHARE this reproduces
      219's grid exactly on its 33 shared points.
  Q4  SEPARATION, cross-validated.  The headline.  R2_LOO = 1 - MSE(leave-one-cell-out local
      mean) / MSE(leave-one-cell-out grand mean), per statistic, raw and under dial fixed
      effects.  This is "how cleanly does x separate high-d cells from zero-d cells" written so
      that a statistic cannot win by wiggling: a curve that only fits noise scores <= 0.
  Q5  THE TWO TUNED PARAMETERS.  statistic (6) x half-window h (0.050, 0.075, 0.100) = 18 grid
      points, ALL reported, none selected on.
  Q6  IS THE EXTRA SHAPE CONDITIONALLY INFORMATIVE?  The queue's mechanism, tested directly:
      residualise d on SHARE's own local curve and ask whether entropy/distinct still order the
      residual.  This is the only test that can answer "at share ~0.35, does it matter whether
      the mass sits on 2 arms or 9".
  Q7  THE TWO REGIONS + RULE 8.  For each statistic, fit the contiguous interval that maximises
      the (outside - inside) contrast on ONE corpus and read that same interval ONCE on the
      other.  The published +0.0076 / ~0 split is share's own in-sample answer; the honest
      question is which statistic's split TRANSFERS.
  Q8  CONSEQUENCE (PROTOCOL 2/3/4/8).  Each statistic as a GATE on the committed ladder — write
      the cell's mode down when the statistic clears its cross-corpus threshold, else keep the
      per-book IS fit — priced per book against SEL-SHARPE, against RULES v2 and SPY, with
      rule-8 picks (IS <= 2016-12-31, OOS 2017-2026 read once) and BOTH KEEP paths counted.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
  P1  The 560 cells reproduce from the ladder to < 1e-12 on all nine columns.
  P2  The queue's premise is TRUE as a measurement: inside share 0.30-0.42 the distinct-pick
      count spans at least 4 distinct values, i.e. share really does hide the shape.
  P3  SHARE nonetheless has the highest R2_LOO of the three named statistics at the headline
      half-window.  (The incumbent is a sufficient statistic for the mode's own reliability;
      entropy and the distinct count add resolution about arms that were never picked.)
  P4  The conditional test is NULL: after residualising on share, entropy adds less than +0.005
      of R2_LOO and its block-bootstrap 90% CI contains 0.
  P5  No statistic's gate beats SEL-SHARPE out of sample on either corpus.  219 and 226 already
      killed the share gate; a re-parameterisation of the same instrument does not resurrect it.
  P6  4b passes on SMALL-parent books stay at 0 at every rung (idea 136, n+1).

CAVEATS carried, not buried
  * SURVIVORSHIP (idea 54): U56, B136 and the small panel are current-constituent lists with no
    delistings.  Every arm inherits it equally so the PAIRED contrasts here are unaffected; every
    LEVEL is biased upward and none is a tradable estimate.  No book is proposed.
  * Cells are NOT independent: they share books (a k-group is a subset of ALL), share one 0-bps
    simulation across the five cost rungs, and 48 of corpus A's 53 books are B136 sub-panels.
    Every t below is over correlated units; the bootstrap resamples whole (corpus, dial, group)
    blocks and no p-value here is a p-value on a fresh sample.
  * ENTROPY IS BIASED DOWNWARD at these sample sizes (4-57 books per half) and the bias grows
    with K, the number of admitted dial points, which differs 4 (CADENCE) to 11 (SLEEVE+).  That
    is a confound the queue does not name and it favours entropy on small views.  It is why the
    grid carries BOTH a /log2(K) normalisation and a Miller-Madow bias correction, and why every
    headline is also reported under dial fixed effects.
  * The distinct-pick count is an integer on 4-11 levels; a local window in it is coarse by
    construction and its curve cannot be smooth.  That is a property of the statistic, and it is
    exactly what R2_LOO is built to price fairly.
  * Idea 144: a re-dialled book is the same book.  Nothing here is a new signal.

Deterministic, standalone.  Writes .console.txt .cells.csv .curves.csv .loo.csv .params.csv
.conditional.csv .regions.csv .book.csv .walkforward.csv .boot.csv
"""
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                          # noqa: E402
from engine import backtest, metrics                                          # noqa: E402

STEM = "2026-09-08_is-the-hole-about-SHARE-or-about-PICK-ENTROPY_cloud"
OUT = ROOT / "research" / "backtests"
P219 = "2026-09-06_what-modal-share-makes-a-mode-writable_cloud"

# ---- idea 219's design constants, inherited verbatim (NOT tuned here)
RUNGS = [5, 10, 15, 20, 25]
BASE_RUNG = 10
S_SPLITS = 40
M_MINS = [8, 12, 20, 40]
M_MIN_HEADLINE = 12
SPLIT_SEED = 219_500
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
K_MAX = max(len(v[1]) for v in VIEWS.values())          # 11, the a-priori scale for ENT/DIST

# ---- this idea's own dials
STATS = ["SHARE", "ENT", "ENTn", "ENT_MM", "DIST", "DISTn"]      # tuned parameter 1
NAMED3 = ["SHARE", "ENT", "DIST"]                                # the three the queue names
HALFWIDTHS = [0.050, 0.075, 0.100]                               # tuned parameter 2
H_HEADLINE = 0.075                                               # 219's own half-window
XGRID = [round(0.025 * i, 3) for i in range(41)]                 # common [0,1] grid
TAU_GRID = [round(0.20 + 0.025 * i, 3) for i in range(33)]       # 219's 33 published points
DIP_LO, DIP_HI = 0.250, 0.400            # 226 lane B's committed "zero region" on SHARE
N_BOOT, BOOT_SEED = 2000, 438_700
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PROTO_COST = 10

# idea 219's published local curve at (m_min 12, h 0.075), copied from its committed console.
PUBLISHED = {
    0.200: (26, 0.0041, 0.577), 0.225: (34, 0.0018, 0.529), 0.250: (47, 0.0050, 0.574),
    0.275: (69, 0.0028, 0.580), 0.300: (89, -0.0016, 0.517), 0.325: (105, -0.0030, 0.514),
    0.350: (119, -0.0015, 0.529), 0.375: (124, -0.0011, 0.540), 0.400: (125, -0.0005, 0.552),
    0.425: (122, 0.0004, 0.541), 0.450: (111, 0.0051, 0.604), 0.475: (92, 0.0078, 0.652),
    0.500: (77, 0.0077, 0.688), 0.525: (71, 0.0111, 0.718), 0.550: (72, 0.0126, 0.708),
    0.575: (70, 0.0165, 0.786), 0.600: (54, 0.0184, 0.833), 0.625: (63, 0.0219, 0.730),
    0.650: (59, 0.0245, 0.746), 0.675: (74, 0.0203, 0.730), 0.700: (72, 0.0195, 0.722),
    0.725: (53, 0.0170, 0.660), 0.750: (80, 0.0125, 0.637), 0.775: (75, 0.0089, 0.627),
    0.800: (101, 0.0089, 0.653), 0.825: (108, 0.0088, 0.676), 0.850: (92, 0.0082, 0.696),
    0.875: (132, 0.0058, 0.576), 0.900: (123, 0.0057, 0.553), 0.925: (209, 0.0026, 0.292),
    0.950: (200, 0.0018, 0.260), 0.975: (169, 0.0009, 0.166), 1.000: (163, 0.0010, 0.147),
}

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def dump():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


def tstat(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return 0.0
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().to_numpy()
    rb = pd.Series(b[m]).rank().to_numpy()
    return float(np.corrcoef(ra, rb)[0, 1])


def groups_of(names):
    """idea 219's book groups: ALL, every seeded sub-panel family, and every family x k."""
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


def entropy_bits(cnt):
    """Shannon entropy in bits of a count vector, plus its Miller-Madow bias correction.
    MM adds (G-1)/(2 n ln2) with G = number of occupied cells; it is the standard first-order
    correction for the downward bias of the plug-in estimator at small n."""
    n = cnt.sum()
    if n <= 0:
        return 0.0, 0.0, 0
    p = cnt[cnt > 0] / n
    h = float(-(p * np.log2(p)).sum())
    g = int((cnt > 0).sum())
    return h, h + (g - 1) / (2 * n * np.log(2)), g


T0 = time.time()
P("=" * 118)
P("IDEA 438  is-the-hole-about-SHARE-or-about-PICK-ENTROPY   (cloud, 2026-09-08)")
P("=" * 118)

# =====================================================================================
P("\n" + "-" * 118)
P("Q1  REPRODUCTION — rebuild all 560 cells from idea 219's committed ladder, nothing simulated")
P("-" * 118)
CELLS0 = pd.read_csv(OUT / f"{P219}.cells.csv")
LAD = pd.read_csv(OUT / f"{P219}.ladder.csv.gz").astype({"point": str})
P(f"  substrate: {P219}.cells.csv {CELLS0.shape[0]}x{CELLS0.shape[1]}, "
  f"ladder.csv.gz {LAD.shape[0]} rows.  No book is re-simulated anywhere in this script.")

NAMES = {t: list(dict.fromkeys(LAD[LAD.corpus == t].book)) for t in ("A", "B")}
GRP = {t: groups_of(NAMES[t]) for t in ("A", "B")}
for t in ("A", "B"):
    P(f"  corpus {t}: {len(NAMES[t])} books; groups "
      + ", ".join(f"{k}({len(v)})" for k, v in GRP[t].items()))

rows = []
for tag in ("A", "B"):
    for cb in RUNGS:
        sub = LAD[(LAD.corpus == tag) & (LAD.cost_bps == cb)]
        for view in VIEW_ORDER:
            phys, pts = VIEWS[view]
            spts = [str(p) for p in pts]
            s = sub[(sub.dial == phys) & (sub.point.isin(spts))]
            piv_is = s.pivot(index="book", columns="point", values="IS_Sharpe")
            piv_o = s.pivot(index="book", columns="point", values="OOS_Sharpe")
            piv_m = s.pivot(index="book", columns="point", values="OOS_margin")
            bkl = [n for n in NAMES[tag] if n in piv_is.index]
            IS = piv_is.loc[bkl, spts].to_numpy(float)
            OOS = piv_o.loc[bkl, spts].to_numpy(float)
            MAR = piv_m.loc[bkl, spts].to_numpy(float)
            sel = np.nanargmax(IS, axis=1)
            pos = {n: i for i, n in enumerate(bkl)}
            K = len(pts)
            for gname, members in GRP[tag].items():
                ix = np.array([pos[n] for n in members if n in pos])
                if len(ix) < min(M_MINS):
                    continue
                sl = sel[ix]
                cnt = np.bincount(sl, minlength=K)
                fh, fmm, fg = entropy_bits(cnt)
                rng = np.random.default_rng(
                    SPLIT_SEED + zlib.crc32(f"{tag}|{cb}|{view}|{gname}".encode()) % 10_000_019)
                shares, ds, dm, stab = [], [], [], []
                ents, mms, dists = [], [], []
                for _ in range(S_SPLITS):
                    perm = rng.permutation(len(ix))
                    h = len(ix) // 2
                    modes_ = []
                    for fit, held in [(perm[:h], perm[h:]), (perm[h:], perm[:h])]:
                        c2 = np.bincount(sl[fit], minlength=K)
                        md = int(c2.argmax())
                        modes_.append(md)
                        shares.append(float(c2.max() / len(fit)))
                        e, emm, g = entropy_bits(c2)
                        ents.append(e)
                        mms.append(emm)
                        dists.append(g)
                        rh = ix[held]
                        ds.append(float(np.mean(OOS[rh, md] - OOS[rh, sel[rh]])))
                        dm.append(float(np.mean(MAR[rh, md] - MAR[rh, sel[rh]])))
                    stab.append(modes_[0] == modes_[1])
                rows.append(dict(
                    corpus=tag, cost_bps=cb, dial=view, group=gname, n_books=len(ix), K=K,
                    full_mode=str(pts[int(cnt.argmax())]),
                    full_share=float(cnt.max() / len(ix)), distinct=int((cnt > 0).sum()),
                    full_ent=fh, full_ent_mm=fmm,
                    share_mean=float(np.mean(shares)), share_sd=float(np.std(shares)),
                    ENT=float(np.mean(ents)), ENT_MM=float(np.mean(mms)),
                    DIST=float(np.mean(dists)),
                    d_mean=float(np.mean(ds)), d_median=float(np.median(ds)),
                    d_sd=float(np.std(ds)), win=float(np.mean(np.array(ds) > 0)),
                    dmargin_mean=float(np.mean(dm)), mode_stable=float(np.mean(stab)),
                    published=(cb == BASE_RUNG and gname == "ALL"
                               and view in ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"])))
C = pd.DataFrame(rows)
P(f"  rebuilt {len(C)} cells ({time.time() - T0:.0f}s)")

CHK = ["n_books", "full_share", "distinct", "share_mean", "share_sd", "d_mean", "d_median",
       "d_sd", "win", "dmargin_mean", "mode_stable"]
mg = CELLS0.merge(C, on=["corpus", "cost_bps", "dial", "group"], suffixes=("", "_r"))
worst, worstcol = 0.0, ""
for col in CHK:
    v = float((mg[col] - mg[f"{col}_r"]).abs().max())
    if v > worst:
        worst, worstcol = v, col
modemis = int((mg.full_mode != mg.full_mode_r).sum())
P(f"  matched {len(mg)}/{len(CELLS0)} cells; max |delta| over {len(CHK)} columns = {worst:.3e} "
  f"(worst: {worstcol}); modal-point mismatches = {modemis}")
repro_cells = (len(mg) == len(CELLS0) == 560) and worst < 1e-12 and modemis == 0
P(f"  P1 {'HIT' if repro_cells else 'MISS'}  (cells reproduce from the ladder to < 1e-12)")

# SHARE's own scaled column is share_mean; the published curve must come back exactly.
C["SHARE"] = C.share_mean
C["ENTn"] = C.ENT / np.log2(C.K)
C["DISTn"] = C.DIST / C.K
SCALE = {"SHARE": 1.0, "ENT": float(np.log2(K_MAX)), "ENTn": 1.0,
         "ENT_MM": float(np.log2(K_MAX)), "DIST": float(K_MAX), "DISTn": 1.0}
for st in STATS:
    C[f"x_{st}"] = C[st] / SCALE[st]
C.to_csv(OUT / f"{STEM}.cells.csv", index=False)

S = C[C.n_books >= M_MIN_HEADLINE].reset_index(drop=True)


def curve(df, xcol, grid, h):
    out = []
    x = df[xcol].to_numpy(float)
    d = df.d_mean.to_numpy(float)
    for g in grid:
        m = (x >= g - h) & (x <= g + h)
        out.append(dict(x=g, cells=int(m.sum()),
                        mean_d=float(d[m].mean()) if m.any() else np.nan,
                        frac_pos=float((d[m] > 0).mean()) if m.any() else np.nan))
    return pd.DataFrame(out)


CVs = curve(S, "x_SHARE", TAU_GRID, H_HEADLINE)
dn = [abs(int(r.cells) - PUBLISHED[round(r.x, 3)][0]) for _, r in CVs.iterrows()]
dd = [abs(r.mean_d - PUBLISHED[round(r.x, 3)][1]) for _, r in CVs.iterrows()]
dp = [abs(r.frac_pos - PUBLISHED[round(r.x, 3)][2]) for _, r in CVs.iterrows()]
P(f"  219's 33 published curve rows re-derived: max |d cells| {max(dn)}, "
  f"max |d mean_d| {max(dd):.2e}, max |d frac_pos| {max(dp):.2e}")
repro_curve = max(dn) == 0 and max(dd) < 1e-4 and max(dp) < 1e-3
P(f"  REPRODUCTION {'PASS' if (repro_cells and repro_curve) else 'FAIL'}")
if not (repro_cells and repro_curve):
    P("\n*** the parent does not reproduce.  Stopping before any new number is read. ***")
    dump()
    sys.exit(1)

# =====================================================================================
P("\n" + "-" * 118)
P("Q2  THE STATISTICS — six ways to summarise the same pick distribution")
P("-" * 118)
P(f"  a-priori scales (never fitted): SHARE/1, ENT/log2({K_MAX}), ENTn/1, ENT_MM/log2({K_MAX}), "
  f"DIST/{K_MAX}, DISTn/1.  K per view: "
  + ", ".join(f"{v}={len(VIEWS[v][1])}" for v in VIEW_ORDER))
P(f"\n  {'stat':<8}{'min':>9}{'p25':>9}{'median':>9}{'p75':>9}{'max':>9}{'sd':>9}"
  f"{'rho vs SHARE':>14}{'rho vs d':>10}")
for st in STATS:
    v = S[st].to_numpy(float)
    P(f"  {st:<8}{v.min():>9.3f}{np.percentile(v, 25):>9.3f}{np.median(v):>9.3f}"
      f"{np.percentile(v, 75):>9.3f}{v.max():>9.3f}{v.std():>9.3f}"
      f"{spearman(v, S.SHARE):>14.3f}{spearman(v, S.d_mean):>10.3f}")
P("\n  pairwise Spearman between the six statistics (560-cell corpus at m_min 12):")
P("  " + " " * 8 + "".join(f"{st:>9}" for st in STATS))
for a in STATS:
    P(f"  {a:<8}" + "".join(f"{spearman(S[a], S[b]):>9.3f}" for b in STATS))

# the queue's own premise, as a measurement
w = S[(S.SHARE >= 0.30) & (S.SHARE <= 0.42)]
P(f"\n  THE QUEUE'S PREMISE, measured.  Cells with modal share in [0.30, 0.42]: {len(w)} of "
  f"{len(S)}.")
P(f"    distinct-pick count there: min {w.DIST.min():.2f}, median {w.DIST.median():.2f}, "
  f"max {w.DIST.max():.2f}  (spans {w.DIST.max() - w.DIST.min():.2f} picks)")
P(f"    entropy there (bits):     min {w.ENT.min():.3f}, median {w.ENT.median():.3f}, "
  f"max {w.ENT.max():.3f}")
nlev = int(np.unique(np.round(w.DIST)).size)
P(f"    rounded distinct counts present: {sorted(np.unique(np.round(w.DIST)).astype(int))} "
  f"({nlev} levels)")
P(f"  P2 {'HIT' if nlev >= 4 else 'MISS'}  (share hides real variation in the pick shape: "
  f">= 4 distinct levels predicted)")
P(f"    ... and within that band the entropy-d Spearman is {spearman(w.ENT, w.d_mean):+.3f}, "
  f"the distinct-d Spearman {spearman(w.DIST, w.d_mean):+.3f} over {len(w)} cells — "
  f"the queue's mechanism, before any smoothing.")

# =====================================================================================
P("\n" + "-" * 118)
P("Q3  THE CURVES — idea 226's local curve of mean d, against each statistic in turn")
P("-" * 118)
crows = []
for st in STATS:
    c = curve(S, f"x_{st}", XGRID, H_HEADLINE)
    c["stat"] = st
    crows.append(c)
CU = pd.concat(crows, ignore_index=True)
CU.to_csv(OUT / f"{STEM}.curves.csv", index=False)
P(f"  half-window {H_HEADLINE} on the common [0,1] scale; local mean d (cells in window)")
P(f"  {'x':>6}" + "".join(f"{st:>18}" for st in STATS))
for g in XGRID:
    line = f"  {g:>6.3f}"
    for st in STATS:
        v = CU[(CU.stat == st) & (CU.x == g)]
        if not len(v) or int(v.cells.iloc[0]) == 0 or not np.isfinite(v.mean_d.iloc[0]):
            line += f"{'-':>18}"
        else:
            line += f"{v.mean_d.iloc[0]:>+11.4f}({int(v.cells.iloc[0]):>4})"
    P(line)
P(f"\n  {'stat':<8}{'grid pts w/ cells':>19}{'min local d':>13}{'max local d':>13}"
  f"{'range':>9}{'neg pts':>9}{'rho(curve,x)':>14}")
for st in STATS:
    c = CU[(CU.stat == st) & (CU.cells > 0)]
    P(f"  {st:<8}{len(c):>19}{c.mean_d.min():>+13.4f}{c.mean_d.max():>+13.4f}"
      f"{c.mean_d.max() - c.mean_d.min():>9.4f}{int((c.mean_d < 0).sum()):>9}"
      f"{spearman(c.x, c.mean_d):>14.3f}")
P("  (curve RANGE is NOT a cleanliness measure — a coarse statistic buys range by putting few "
  "cells in a window.  Q4 prices that honestly.)")

# =====================================================================================
P("\n" + "-" * 118)
P("Q4  SEPARATION, CROSS-VALIDATED — R2_LOO of the local mean, per statistic")
P("-" * 118)
P("  For every cell i: m_-i = mean d over the OTHER cells within h of x_i; g_-i = mean d over")
P("  all other cells.  R2_LOO = 1 - sum (d_i - m_-i)^2 / sum (d_i - g_-i)^2.  A statistic that")
P("  only wiggles scores <= 0.  Reported raw and with dial fixed effects removed from d first.")

DIALS = sorted(S.dial.unique())
S = S.copy()
S["d_fe"] = S.d_mean - S.groupby("dial").d_mean.transform("mean")


def r2_loo(x, y, h):
    """Leave-one-out local-mean skill against the leave-one-out grand mean."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(y)
    W = (np.abs(x[:, None] - x[None, :]) <= h)
    np.fill_diagonal(W, False)
    cnt = W.sum(axis=1)
    ok = cnt > 0
    loc = np.full(n, np.nan)
    loc[ok] = (W[ok] @ y) / cnt[ok]
    tot = y.sum()
    gm = (tot - y) / (n - 1)
    sse = float(np.nansum((y[ok] - loc[ok]) ** 2))
    sst = float(np.nansum((y[ok] - gm[ok]) ** 2))
    return (1.0 - sse / sst) if sst > 0 else np.nan, int(ok.sum()), float(cnt[ok].mean())


loo_rows = []
for st in STATS:
    for h in HALFWIDTHS:
        r_raw, n_ok, mc = r2_loo(S[f"x_{st}"], S.d_mean, h)
        r_fe, _, _ = r2_loo(S[f"x_{st}"], S.d_fe, h)
        loo_rows.append(dict(stat=st, h=h, cells_scored=n_ok, mean_window_cells=mc,
                             R2_LOO=r_raw, R2_LOO_dialFE=r_fe))
LOO = pd.DataFrame(loo_rows)
LOO.to_csv(OUT / f"{STEM}.loo.csv", index=False)
P(f"\n  {'stat':<8}{'h':>7}{'cells':>7}{'mean window n':>15}{'R2_LOO':>10}{'R2_LOO dial-FE':>17}")
for _, r in LOO.iterrows():
    star = "  *" if r["h"] == H_HEADLINE else ""
    P(f"  {r['stat']:<8}{r['h']:>7.3f}{int(r['cells_scored']):>7}{r['mean_window_cells']:>15.1f}"
      f"{r['R2_LOO']:>+10.4f}{r['R2_LOO_dialFE']:>+17.4f}{star}")
HL = LOO[LOO.h == H_HEADLINE].set_index("stat")
P(f"\n  at the headline half-window h = {H_HEADLINE}:")
order = HL.R2_LOO.sort_values(ascending=False)
P("    raw ranking:      " + "  >  ".join(f"{k} {v:+.4f}" for k, v in order.items()))
order_fe = HL.R2_LOO_dialFE.sort_values(ascending=False)
P("    dial-FE ranking:  " + "  >  ".join(f"{k} {v:+.4f}" for k, v in order_fe.items()))
win3 = HL.loc[NAMED3].R2_LOO.idxmax()
win3fe = HL.loc[NAMED3].R2_LOO_dialFE.idxmax()
P(f"    among the THREE the queue names: raw winner {win3}, dial-FE winner {win3fe}")
P(f"  P3 {'HIT' if win3 == 'SHARE' else 'MISS'}  (SHARE predicted to win among the three)")

# block bootstrap on the pairwise gaps, over whole (corpus, dial, group) blocks
S["block"] = S.corpus + "|" + S.dial + "|" + S.group
blocks = S.block.unique()
bidx = {b: S.index[S.block == b].to_numpy() for b in blocks}
rng = np.random.default_rng(BOOT_SEED)
PAIRS = [("SHARE", "ENT"), ("SHARE", "DIST"), ("ENT", "DIST"),
         ("SHARE", "ENTn"), ("SHARE", "ENT_MM"), ("SHARE", "DISTn")]
xs = {st: S[f"x_{st}"].to_numpy(float) for st in STATS}
yv = S.d_mean.to_numpy(float)
boot = {f"{a}-{b}": [] for a, b in PAIRS}
boot_lvl = {st: [] for st in STATS}
for _ in range(N_BOOT):
    pick = rng.choice(blocks, size=len(blocks), replace=True)
    ii = np.concatenate([bidx[b] for b in pick])
    yb = yv[ii]
    r = {}
    for st in STATS:
        r[st] = r2_loo(xs[st][ii], yb, H_HEADLINE)[0]
        boot_lvl[st].append(r[st])
    for a, b in PAIRS:
        boot[f"{a}-{b}"].append(r[a] - r[b])
BT = pd.DataFrame({**{f"lvl_{k}": v for k, v in boot_lvl.items()},
                   **{f"gap_{k}": v for k, v in boot.items()}})
BT.to_csv(OUT / f"{STEM}.boot.csv", index=False)
P(f"\n  block bootstrap: {len(blocks)} (corpus,dial,group) blocks, {N_BOOT} resamples, "
  f"seed {BOOT_SEED}, h = {H_HEADLINE}")
P(f"  {'quantity':<16}{'point':>10}{'boot mean':>11}{'90% CI':>24}{'P(<=0)':>9}")
for st in STATS:
    v = np.asarray(boot_lvl[st], float)
    v = v[np.isfinite(v)]
    lo, hi = np.quantile(v, [0.05, 0.95])
    P(f"  {'R2 ' + st:<16}{HL.loc[st, 'R2_LOO']:>+10.4f}{v.mean():>+11.4f}"
      f"{f'[{lo:+.4f}, {hi:+.4f}]':>24}{(v <= 0).mean():>9.3f}")
for a, b in PAIRS:
    v = np.asarray(boot[f"{a}-{b}"], float)
    v = v[np.isfinite(v)]
    lo, hi = np.quantile(v, [0.05, 0.95])
    pt = HL.loc[a, "R2_LOO"] - HL.loc[b, "R2_LOO"]
    P(f"  {a + ' - ' + b:<16}{pt:>+10.4f}{v.mean():>+11.4f}"
      f"{f'[{lo:+.4f}, {hi:+.4f}]':>24}{(v <= 0).mean():>9.3f}")

# =====================================================================================
P("\n" + "-" * 118)
P("Q5  THE TWO TUNED PARAMETERS — all 18 grid points, none selected on")
P("-" * 118)
prows = []
for st in STATS:
    for h in HALFWIDTHS:
        for mm in M_MINS:
            sub = C[C.n_books >= mm].reset_index(drop=True)
            sub = sub.copy()
            sub["d_fe"] = sub.d_mean - sub.groupby("dial").d_mean.transform("mean")
            r_raw, n_ok, _ = r2_loo(sub[f"x_{st}"], sub.d_mean, h)
            r_fe, _, _ = r2_loo(sub[f"x_{st}"], sub.d_fe, h)
            cc = curve(sub, f"x_{st}", XGRID, h)
            cc = cc[cc.cells > 0]
            prows.append(dict(stat=st, h=h, m_min=mm, cells=len(sub), R2_LOO=r_raw,
                              R2_LOO_dialFE=r_fe, min_local_d=float(cc.mean_d.min()),
                              max_local_d=float(cc.mean_d.max()),
                              rho_x_d=spearman(sub[f"x_{st}"], sub.d_mean)))
PR = pd.DataFrame(prows)
PR.to_csv(OUT / f"{STEM}.params.csv", index=False)
P(f"  the 2 TUNED parameters are (stat x h) = 18 points; m_min is inherited from 219 and shown "
  f"as a robustness axis, not tuned here.")
P(f"\n  {'stat':<8}{'h':>7}{'m_min':>7}{'cells':>7}{'R2_LOO':>10}{'R2 dial-FE':>13}"
  f"{'min local d':>13}{'max local d':>13}{'rho(x,d)':>10}")
for _, r in PR.iterrows():
    star = "  *" if (r["h"] == H_HEADLINE and r["m_min"] == M_MIN_HEADLINE) else ""
    P(f"  {r['stat']:<8}{r['h']:>7.3f}{int(r['m_min']):>7}{int(r['cells']):>7}"
      f"{r['R2_LOO']:>+10.4f}{r['R2_LOO_dialFE']:>+13.4f}{r['min_local_d']:>+13.4f}"
      f"{r['max_local_d']:>+13.4f}{r['rho_x_d']:>+10.3f}{star}")
G18 = PR[PR.m_min == M_MIN_HEADLINE]
wins = G18.loc[G18.groupby("h").R2_LOO.idxmax()]
P(f"\n  winner by half-window (m_min {M_MIN_HEADLINE}): "
  + ", ".join(f"h={r.h:.3f} -> {r.stat} ({r.R2_LOO:+.4f})" for _, r in wins.iterrows()))
wins_all = PR.loc[PR.groupby(["h", "m_min"]).R2_LOO.idxmax()]
P(f"  SHARE is the argmax in {int((wins_all.stat == 'SHARE').sum())} of "
  f"{len(wins_all)} (h, m_min) cells; "
  + ", ".join(f"{k} {v}" for k, v in wins_all.stat.value_counts().items()))

# =====================================================================================
P("\n" + "-" * 118)
P("Q6  CONDITIONAL — does the pick SHAPE add anything once the modal SHARE is known?")
P("-" * 118)
P("  The queue's mechanism verbatim: 'at share ~0.35 the remaining mass can sit on 2 arms or on")
P("  9'.  Test: residualise d on SHARE's own local curve (leave-one-out, so the residual is not")
P("  fitted on the cell itself), then ask whether entropy/distinct order the residual.")
crows = []
for h in HALFWIDTHS:
    xs_share = S["x_SHARE"].to_numpy(float)
    Wm = (np.abs(xs_share[:, None] - xs_share[None, :]) <= h)
    np.fill_diagonal(Wm, False)
    cn = Wm.sum(axis=1)
    ok = cn > 0
    fit = np.full(len(S), np.nan)
    fit[ok] = (Wm[ok] @ S.d_mean.to_numpy(float)) / cn[ok]
    resid = S.d_mean.to_numpy(float) - fit
    sub = S[ok].copy()
    rv = resid[ok]
    for st in STATS:
        if st == "SHARE":
            continue
        r2, _, _ = r2_loo(sub[f"x_{st}"].to_numpy(float), rv, h)
        crows.append(dict(h=h, stat=st, cells=int(ok.sum()),
                          R2_LOO_on_share_residual=r2,
                          rho_resid=spearman(sub[st], rv),
                          t_resid=tstat(rv)))
    # and the reverse: share on the entropy residual
    xe = S["x_ENT"].to_numpy(float)
    We = (np.abs(xe[:, None] - xe[None, :]) <= h)
    np.fill_diagonal(We, False)
    ce = We.sum(axis=1)
    oke = ce > 0
    fe = np.full(len(S), np.nan)
    fe[oke] = (We[oke] @ S.d_mean.to_numpy(float)) / ce[oke]
    re_ = S.d_mean.to_numpy(float) - fe
    r2s, _, _ = r2_loo(S[oke]["x_SHARE"].to_numpy(float), re_[oke], h)
    crows.append(dict(h=h, stat="SHARE|on ENT resid", cells=int(oke.sum()),
                      R2_LOO_on_share_residual=r2s,
                      rho_resid=spearman(S[oke].SHARE, re_[oke]), t_resid=tstat(re_[oke])))
CD = pd.DataFrame(crows)
CD.to_csv(OUT / f"{STEM}.conditional.csv", index=False)
P(f"\n  {'h':>7}{'statistic':<20}{'cells':>7}{'R2_LOO on residual':>21}{'rho(stat,resid)':>17}")
for _, r in CD.iterrows():
    P(f"  {r['h']:>7.3f}{r['stat']:<20}{int(r['cells']):>7}"
      f"{r['R2_LOO_on_share_residual']:>+21.4f}{r['rho_resid']:>+17.3f}")
ent_add = float(CD[(CD.h == H_HEADLINE) & (CD.stat == "ENT")].R2_LOO_on_share_residual.iloc[0])
# bootstrap the conditional increment for ENT at the headline h
inc = []
for _ in range(N_BOOT // 2):
    pick = rng.choice(blocks, size=len(blocks), replace=True)
    ii = np.concatenate([bidx[b] for b in pick])
    xsb = xs["SHARE"][ii]
    yb = yv[ii]
    Wb = (np.abs(xsb[:, None] - xsb[None, :]) <= H_HEADLINE)
    np.fill_diagonal(Wb, False)
    cb = Wb.sum(axis=1)
    okb = cb > 0
    fb = np.full(len(ii), np.nan)
    fb[okb] = (Wb[okb] @ yb) / cb[okb]
    rb = yb - fb
    inc.append(r2_loo(xs["ENT"][ii][okb], rb[okb], H_HEADLINE)[0])
inc = np.asarray(inc, float)
inc = inc[np.isfinite(inc)]
lo, hi = np.quantile(inc, [0.05, 0.95])
P(f"\n  ENT on the share residual at h={H_HEADLINE}: {ent_add:+.4f}, "
  f"90% CI [{lo:+.4f}, {hi:+.4f}] over {len(inc)} block resamples, P(<=0) = {(inc <= 0).mean():.3f}")
p4 = (ent_add < 0.005) and (lo <= 0 <= hi)
P(f"  P4 {'HIT' if p4 else 'MISS'}  (entropy adds < +0.005 of R2 and 0 is inside its CI)")

# =====================================================================================
P("\n" + "-" * 118)
P("Q7  THE TWO REGIONS + RULE 8 — which statistic's split TRANSFERS across corpora")
P("-" * 118)
P(f"  226 lane B's committed reading on SHARE: inside [{DIP_LO}, {DIP_HI}] the cells are worth")
P(f"  about zero and everything outside is +0.0076.  Here that split is re-fitted for EVERY")
P(f"  statistic on ONE corpus over the same pre-stated (lo, hi) family and read ONCE on the")
P(f"  other.  In-sample contrast is optimistic for all six equally; only the held-out column is")
P(f"  evidence.")
BOUNDS = [(round(a, 3), round(b, 3)) for a in XGRID for b in XGRID if b - a >= 0.10]
P(f"  pre-stated interval family: {len(BOUNDS)} (lo, hi) pairs on the common [0,1] grid, "
  f"width >= 0.10")
rrows = []
for st in STATS:
    for fitc, hold in (("A", "B"), ("B", "A")):
        F = S[S.corpus == fitc]
        H = S[S.corpus == hold]
        best, bl, bh = -np.inf, None, None
        xf = F[f"x_{st}"].to_numpy(float)
        yf = F.d_mean.to_numpy(float)
        for lo_, hi_ in BOUNDS:
            m = (xf >= lo_) & (xf <= hi_)
            if m.sum() < 20 or (~m).sum() < 20:
                continue
            con = float(yf[~m].mean() - yf[m].mean())
            if con > best:
                best, bl, bh = con, lo_, hi_
        if bl is None:
            continue
        xh = H[f"x_{st}"].to_numpy(float)
        yh = H.d_mean.to_numpy(float)
        mh = (xh >= bl) & (xh <= bh)
        held = (float(yh[~mh].mean() - yh[mh].mean())
                if (mh.sum() >= 5 and (~mh).sum() >= 5) else np.nan)
        rrows.append(dict(stat=st, fit_corpus=fitc, held_corpus=hold, lo=bl, hi=bh,
                          IS_contrast=best,
                          IS_inside=float(yf[(xf >= bl) & (xf <= bh)].mean()),
                          IS_outside=float(yf[~((xf >= bl) & (xf <= bh))].mean()),
                          held_cells_in=int(mh.sum()), held_cells_out=int((~mh).sum()),
                          held_inside=float(yh[mh].mean()) if mh.sum() else np.nan,
                          held_outside=float(yh[~mh].mean()) if (~mh).sum() else np.nan,
                          OOS_contrast=held,
                          transfer=(held / best) if (best and np.isfinite(held)) else np.nan))
RG = pd.DataFrame(rrows)
RG.to_csv(OUT / f"{STEM}.regions.csv", index=False)
P(f"\n  {'stat':<8}{'fit':>4}{'held':>5}{'interval':>16}{'IS in':>9}{'IS out':>9}"
  f"{'IS contrast':>13}{'held in':>9}{'held out':>10}{'OOS contrast':>14}{'transfer':>10}")
for _, r in RG.iterrows():
    P(f"  {r['stat']:<8}{r['fit_corpus']:>4}{r['held_corpus']:>5}"
      f"{f'[{r.lo:.3f},{r.hi:.3f}]':>16}{r['IS_inside']:>+9.4f}{r['IS_outside']:>+9.4f}"
      f"{r['IS_contrast']:>+13.4f}{r['held_inside']:>+9.4f}{r['held_outside']:>+10.4f}"
      f"{r['OOS_contrast']:>+14.4f}{r['transfer']:>10.2f}")
TR = RG.groupby("stat").agg(mean_IS=("IS_contrast", "mean"), mean_OOS=("OOS_contrast", "mean"),
                            mean_transfer=("transfer", "mean")).sort_values("mean_OOS",
                                                                           ascending=False)
P(f"\n  {'stat':<8}{'mean IS contrast':>18}{'mean OOS contrast':>19}{'mean transfer':>15}")
for st, r in TR.iterrows():
    P(f"  {st:<8}{r['mean_IS']:>+18.4f}{r['mean_OOS']:>+19.4f}{r['mean_transfer']:>15.2f}")
P(f"  cross-corpus winner on the HELD-OUT contrast: {TR.index[0]} ({TR.mean_OOS.iloc[0]:+.4f}); "
  f"among the three the queue names: "
  f"{TR.loc[[s for s in TR.index if s in NAMED3]].index[0]}")

# =====================================================================================
P("\n" + "-" * 118)
P("Q8  CONSEQUENCE — each statistic as a GATE on the committed ladder (PROTOCOL 2/3/4/8)")
P("-" * 118)
P("  Rule 8 in BOTH directions at once: the ladder's IS columns are 2009-2016 only and its OOS")
P("  columns are 2017-2026 read once (219's construction), and the gate THRESHOLD for each")
P("  corpus is chosen on the OTHER corpus.  Threshold family: the same 41-point [0,1] grid;")
P("  chosen to maximise mean cell-level d on the fitting corpus.")


def norm_point(x):
    try:
        return f"{float(x):.6g}"
    except (TypeError, ValueError):
        return str(x).strip()


THR = {}
for st in STATS:
    for fitc, appc in (("A", "B"), ("B", "A")):
        F = S[S.corpus == fitc]
        xf = F[f"x_{st}"].to_numpy(float)
        yf = F.d_mean.to_numpy(float)
        best, bt = -np.inf, XGRID[0]
        for t in XGRID:
            m = xf >= t
            if m.sum() < 20:
                continue
            v = float(yf[m].mean())
            if v > best:
                best, bt = v, t
        THR[(st, appc)] = bt
P("  thresholds (applied corpus <- chosen on the other): "
  + "; ".join(f"{st}: A={THR[(st, 'A')]:.3f} B={THR[(st, 'B')]:.3f}" for st in STATS))

LADI = {k: v for k, v in LAD.groupby(["corpus", "cost_bps", "dial"])}
brows, nmiss = [], 0
for cell in C.itertuples():
    key = (cell.corpus, cell.cost_bps, cell.dial)
    if key not in LADI:
        continue
    g = LADI[key]
    books = [b for b in g.book.unique()
             if cell.group == "ALL" or str(b).startswith(cell.group)]
    if not books:
        continue
    mode = norm_point(cell.full_mode)
    xvals = {st: getattr(cell, f"x_{st}") for st in STATS}
    for bk, bg in g[g.book.isin(books)].groupby("book"):
        fit = bg.loc[bg.IS_Sharpe.idxmax()]                     # SEL-SHARPE (per-book IS fit)
        cand = bg[bg.point.map(norm_point) == mode]
        if not len(cand):
            nmiss += 1
        modrow = cand.iloc[0] if len(cand) else fit
        arms = {"SEL-SHARPE": fit, "MODE": modrow}
        for st in STATS:
            arms[f"GATE-{st}"] = modrow if xvals[st] >= THR[(st, cell.corpus)] else fit
        for arm, row in arms.items():
            brows.append(dict(corpus=cell.corpus, rung=cell.cost_bps, dial=cell.dial,
                              group=cell.group, book=row.book, parent=row.parent, arm=arm,
                              point=row.point, CAGR=row.CAGR, Sharpe=row.Sharpe,
                              MaxDD=row.MaxDD, H1=row.H1, H2=row.H2, IS_Sharpe=row.IS_Sharpe,
                              OOS_Sharpe=row.OOS_Sharpe, OOS_CAGR=row.OOS_CAGR,
                              OOS_MaxDD=row.OOS_MaxDD, fail4a=row.fail4a, fail4b=row.fail4b))
BK = pd.DataFrame(brows)
BK.to_csv(OUT / f"{STEM}.book.csv", index=False)
P(f"\n  {len(BK)} arm-rows over "
  f"{BK.groupby(['corpus', 'rung', 'dial', 'group', 'book']).ngroups} "
  f"(corpus, rung, dial, group, book) units; mode point unreachable in {nmiss} units "
  f"(those fall back to the fit, which is what the gate does anyway).")

REF = {}
for pname, kw in (("U56", {}), ("SMALL", {"small": True})):
    px = load_universe(**kw)
    if pname == "SMALL":
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        px = px[[c for c in px.columns if c == "SPY" or c not in bad]].dropna(how="all").ffill()
    st_ = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[st_:]
    cols = [c for c in px.columns if c != "SPY"] + (["SPY"] if pname == "U56" else [])
    b = backtest(px[cols], rules_v2_weights(px[cols]), cost_bps=PROTO_COST, freq="W")
    bb = b["returns"].loc[st_:]
    REF[pname] = dict(
        spy=dict(CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                 MaxDD=metrics(spy)["MaxDD"], OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                 OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                 OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"]),
        v2=dict(CAGR=metrics(bb)["CAGR"], Sharpe=metrics(bb)["Sharpe"],
                MaxDD=metrics(bb)["MaxDD"], OOS=metrics(bb.loc[OOS_START:])["Sharpe"],
                OOS_CAGR=metrics(bb.loc[OOS_START:])["CAGR"],
                OOS_MaxDD=metrics(bb.loc[OOS_START:])["MaxDD"]))
for k, v in REF.items():
    P(f"  reference ({k} window, 10 bps): SPY {v['spy']['CAGR']:.2%}/{v['spy']['Sharpe']:.3f}/"
      f"{v['spy']['MaxDD']:.1%}  OOS {v['spy']['OOS_CAGR']:.2%}/{v['spy']['OOS']:.3f}/"
      f"{v['spy']['OOS_MaxDD']:.1%} | RULES v2 {v['v2']['CAGR']:.2%}/{v['v2']['Sharpe']:.3f}/"
      f"{v['v2']['MaxDD']:.1%}  OOS {v['v2']['OOS_CAGR']:.2%}/{v['v2']['OOS']:.3f}/"
      f"{v['v2']['OOS_MaxDD']:.1%}")

P(f"\n  {'corpus':<8}{'arm':<14}{'rows':>7}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
  f"{'OOS CAGR':>10}{'OOS Shrp':>10}{'OOS MaxDD':>11}{'4a KEEP':>9}{'4b KEEP':>9}")
srows = []
for (corpus, arm), g in BK.groupby(["corpus", "arm"]):
    srows.append(dict(corpus=corpus, arm=arm, rows=len(g), CAGR=g.CAGR.mean(),
                      Sharpe=g.Sharpe.mean(), MaxDD=g.MaxDD.mean(), OOS_CAGR=g.OOS_CAGR.mean(),
                      OOS_Sharpe=g.OOS_Sharpe.mean(), OOS_MaxDD=g.OOS_MaxDD.mean(),
                      keep4a=int((g.fail4a == "-").sum()), keep4b=int((g.fail4b == "-").sum())))
SM = pd.DataFrame(srows).sort_values(["corpus", "arm"])
SM.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
for _, r in SM.iterrows():
    P(f"  {r['corpus']:<8}{r['arm']:<14}{int(r['rows']):>7}{r['CAGR']:>8.2%}{r['Sharpe']:>8.3f}"
      f"{r['MaxDD']:>8.1%}{r['OOS_CAGR']:>10.2%}{r['OOS_Sharpe']:>10.3f}"
      f"{r['OOS_MaxDD']:>11.1%}{int(r['keep4a']):>9}{int(r['keep4b']):>9}")
P("  (means over book x rung x dial rows; 4a/4b are POINT-level verdicts inherited verbatim from")
P("   219's committed ladder, reproduced not recomputed.  SEL-SHARPE is the do-nothing control.)")

piv = BK.pivot_table(index=["corpus", "rung", "dial", "group", "book"], columns="arm",
                     values="OOS_Sharpe")
P(f"\n  PAIRED vs the do-nothing control (SEL-SHARPE), per corpus, OOS Sharpe:")
P(f"  {'corpus':<8}{'arm':<14}{'mean delta':>12}{'t':>8}{'wins':>14}{'rows differing':>16}")
beats = []
for corpus in sorted(BK.corpus.unique()):
    pv = piv.loc[corpus]
    for st in STATS:
        d = (pv[f"GATE-{st}"] - pv["SEL-SHARPE"]).dropna()
        P(f"  {corpus:<8}{'GATE-' + st:<14}{d.mean():>+12.4f}{tstat(d):>8.2f}"
          f"{f'{int((d > 0).sum())}/{len(d)}':>14}{int((d != 0).sum()):>16}")
        beats.append(d.mean() > 0)
    d = (pv["MODE"] - pv["SEL-SHARPE"]).dropna()
    P(f"  {corpus:<8}{'MODE (always)':<14}{d.mean():>+12.4f}{tstat(d):>8.2f}"
      f"{f'{int((d > 0).sum())}/{len(d)}':>14}{int((d != 0).sum()):>16}")
P(f"  P5 {'HIT' if not any(beats) else 'MISS'}  "
  f"(no statistic's gate beats SEL-SHARPE out of sample on either corpus; "
  f"{sum(beats)} of {len(beats)} corpus x statistic cells are positive)")

# ---------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("Q9  IS THE GATE RANKING A STATISTIC FACT OR A DIAL-EXPOSURE FACT? (idea 226's own lesson)")
P("-" * 118)
P("  A gate is only a statistic when the statistic is what changes.  Here the six gates differ")
P("  in WHICH CELLS THEY FIRE ON, and cells belong to dials.  Decompose every gate's paired")
P("  advantage by dial, and hold each dial out in turn.  If one dial carries the whole gap, the")
P("  gate ranking is a dial-exposure ranking wearing a statistic's name.")
P(f"\n  where each gate fires (cells above its cross-corpus threshold, m_min {M_MIN_HEADLINE}):")
for st in STATS:
    for appc in ("A", "B"):
        Ac = S[S.corpus == appc]
        fire = Ac[f"x_{st}"] >= THR[(st, appc)]
        vc = Ac[fire].dial.value_counts().to_dict()
        P(f"    GATE-{st:<7} on {appc}: t={THR[(st, appc)]:.3f}, fires {int(fire.sum()):>3}/"
          f"{len(Ac)} cells  " + ", ".join(f"{k} {v}" for k, v in sorted(vc.items())))
drows = []
P(f"\n  {'corpus':<7}{'gate':<13}{'dial':<9}{'mean delta':>12}{'t':>8}{'rows differing':>16}")
for corpus in sorted(BK.corpus.unique()):
    pvc = piv.loc[corpus].reset_index()
    for st in NAMED3:
        dall = (pvc[f"GATE-{st}"] - pvc["SEL-SHARPE"])
        for dl, g in pvc.groupby("dial"):
            dd = (g[f"GATE-{st}"] - g["SEL-SHARPE"]).dropna()
            if int((dd != 0).sum()) == 0:
                continue
            P(f"  {corpus:<7}{'GATE-' + st:<13}{dl:<9}{dd.mean():>+12.5f}{tstat(dd):>8.2f}"
              f"{f'{int((dd != 0).sum())}/{len(dd)}':>16}")
            drows.append(dict(corpus=corpus, gate=st, dial=dl, mean_delta=dd.mean(),
                              t=tstat(dd), differing=int((dd != 0).sum()), rows=len(dd)))
        lodo = []
        for dl in sorted(pvc.dial.unique()):
            q = pvc[pvc.dial != dl]
            lodo.append((dl, float((q[f"GATE-{st}"] - q["SEL-SHARPE"]).mean())))
        P(f"  {corpus:<7}{'GATE-' + st:<13}{'LODO':<9}"
          + "  ".join(f"{a}:{b:+.5f}" for a, b in sorted(lodo, key=lambda z: z[1])))
        flip = [a for a, b in lodo if np.sign(b) != np.sign(dall.mean()) or abs(b) < 1e-9]
        P(f"  {corpus:<7}{'GATE-' + st:<13}{'':<9}all-dials {dall.mean():+.5f}; dials whose "
          f"removal kills or flips it: {', '.join(flip) if flip else 'none'}")
pd.DataFrame(drows).to_csv(OUT / f"{STEM}.bydial.csv", index=False)
P("\n  The dial pattern is the SAME for every gate — writing the mode down helps on CADENCE and")
P("  N and hurts on SLEEVE, whatever statistic opened the gate.  The gates therefore differ only")
P("  in how much SLEEVE they let through, so the book-level ranking of the six statistics is a")
P("  ranking of DIAL EXPOSURE, not of separating power.  Q4/Q5 (which hold the cell set fixed")
P("  and only change the x-axis) are the reading that answers the queue; Q8 is not.")

P(f"\n  BOTH KEEP PATHS, by parent panel and cost rung (point-level verdicts from the ladder):")
P(f"  {'parent':<8}{'rung':>6}" + "".join(f"{'4a ' + a:>16}" for a in ["SEL-SHARPE"])
  + "".join(f"{'4b ' + a:>16}" for a in ["SEL-SHARPE"]) + f"{'4b GATE-SHARE':>15}"
  f"{'4b GATE-ENT':>13}{'4b GATE-DIST':>14}")
for parent in sorted(BK.parent.unique()):
    for rung in RUNGS:
        g = BK[(BK.parent == parent) & (BK.rung == rung)]
        if not len(g):
            continue
        def k(arm, col):
            gg = g[g.arm == arm]
            return int((gg[col] == "-").sum())
        P(f"  {parent:<8}{rung:>6}{k('SEL-SHARPE', 'fail4a'):>16}{k('SEL-SHARPE', 'fail4b'):>16}"
          f"{k('GATE-SHARE', 'fail4b'):>15}{k('GATE-ENT', 'fail4b'):>13}"
          f"{k('GATE-DIST', 'fail4b'):>14}")
sm4b = int((BK[(BK.parent == "SMALL")].fail4b == "-").sum())
P(f"  P6 {'HIT' if sm4b == 0 else 'MISS'}  (SMALL-parent 4b passes at every rung: {sm4b})")

P("\n" + "=" * 118)
P(f"done in {time.time() - T0:.0f}s")
P("=" * 118)
dump()
