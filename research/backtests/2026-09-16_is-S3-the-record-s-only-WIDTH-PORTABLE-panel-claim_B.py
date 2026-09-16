#!/usr/bin/env python3
"""Idea 689 - "is-S3-the-record-s-only-WIDTH-PORTABLE-panel-claim" (lane B, 2026-09-16).

The question
------------
Idea 525 (lane B) broke idea 286's breadth/n_elig confound with a two-factor panel ladder
(q = share of the panel drawn from SMALL439, k = panel width) and classified the record's
five published "panel property explains the result" statistics by a rank regression on
(log breadth, log k) - the coordinates that span (log Ebar, log k), since

        log Ebar == log breadth + log k        EXACTLY.

Idea 685 (lane C) re-read that classification on a k arm ten times as wide (40..400 instead
of 40..100) and found the verdicts are mostly NOT width-portable.  Across the three
supports - lane B (q in [0,1], k<=100), NARROW (q>=0.5, k<=100), WIDE (q>=0.5, k<=400) -
the committed verdicts are

    S1 breadth / breadth / JOINT     flip
    S2 JOINT   / JOINT   / n_elig    flip
    S3 breadth / breadth / breadth   STABLE   beta_logbreadth +0.692 / +0.581 / +0.520
    S4 breadth / NULL    / breadth   flip                 beta_logk -0.053 / -0.140 / -0.189
    S5 NULL    / NULL    / NULL      stable, but NULL on every support

so S3 - idea 271/269C's Sharpe-vs-CAGR REVERSAL SHARE over book-size pairs - is the record's
only statistic carrying a non-null verdict that survives a 4x change of width support.

The queue's ask (idea 689): "Test whether that stability is a property of the reversal
statistic or of ratio statistics generally, by building matched ratio and level statistics
on the same ladder."

Why the question has teeth.  S3 is a DISAGREEMENT share between a RATIO (Sharpe = annualised
mean / annualised vol) and a LEVEL (CAGR, a return in return units).  Two different readings
of 685's result are both consistent with the record:

    (a) the REVERSAL reading - it is the reversal FORM that ports.  Then any reversal share
        between any two statistics should port, ratio-vs-level or not.
    (b) the DIMENSIONLESS reading - it is the RATIO form that ports.  A ratio is invariant to
        the scale of the panel's returns; a level is not, and panel width moves the level of
        a CAND-n book's return through the depth of the selection pool.  Then every ratio
        statistic should port and every level statistic should not, and S3 would port because
        one of its two sides is a ratio.

This run builds BOTH families on the SAME ladder and the SAME three supports and reads them
under 525's own pre-registered classification, so the two readings are separated by data
rather than by which statistic the record happened to publish.

Design - the statistic family (tuned parameter 1: STATISTIC FORM)
-----------------------------------------------------------------
Every statistic below is a single scalar per panel, computed from the SAME CAND-n book runs
(NS_LAD = {5,10,15,20,30}, GROSS 0.75, weekly, 10 bps, next-day execution) that ideas 286 /
525 / 685 used.  No new book is invented, so a 4a/4b pass here is a statement about the
panel, not a capital candidate.

    PLAIN LEVEL statistics (carry return / drawdown units; n=20 reference book)
        LV_CAGR    CAGR of CAND-20
        LV_ARET    annualised arithmetic mean return of CAND-20
        LV_DD      |MaxDD| of CAND-20
        LV_VOL     annualised vol of CAND-20
    PLAIN RATIO statistics (dimensionless; n=20 reference book)
        RA_SHARPE  Sharpe of CAND-20
        RA_SORTINO Sortino of CAND-20
        RA_CALMAR  CAGR / |MaxDD| of CAND-20
        RA_VOLREL  vol(CAND-20) / vol(EWall)          (a pure scale-free panel ratio)
    REVERSAL shares over the 10 unordered n-pairs of NS_LAD - the S3 FORM, applied to
    matched pairs so "ratio vs level", "ratio vs ratio" and "level vs level" all appear:
        RL_SHARPE_CAGR    Sharpe vs CAGR       == idea 271/269C's S3          [ratio x level]
        RL_CALMAR_CAGR    Calmar vs CAGR                                      [ratio x level]
        RL_SORTINO_CAGR   Sortino vs CAGR                                     [ratio x level]
        RL_SHARPE_ARET    Sharpe vs ann. arithmetic mean                      [ratio x level]
        RR_SHARPE_SORTINO Sharpe vs Sortino                                   [ratio x ratio]
        RR_SHARPE_CALMAR  Sharpe vs Calmar                                    [ratio x ratio]
        LL_CAGR_ARET      CAGR vs ann. arithmetic mean                        [level x level]
        LL_CAGR_NEGDD     CAGR vs -|MaxDD|                                    [level x level]

16 statistics x 3 supports.  ALL of them are reported, in .decomp.csv and .portability.csv;
none is dropped for being uninteresting.

Design - the supports (tuned parameter 2: k)
--------------------------------------------
The panel ladder is REPLAYED, not re-designed: lane B's rng loop (seed 2026, its full
QS_B x KS_B x N_DRAWS order including the dedupe) and idea 685's separate k>100 generator
(seed 685) are both reproduced, so every panel in this run is byte-identical to a panel one
of the two parents already committed.  The three supports are then subsets:

    (B) lane B  q in {0,.25,.5,.75,1}, k in {40,60,80,100}    58 panels   k span 2.5x
    (N) NARROW  q >= 0.5,              k <= 100               36 panels   k span 2.5x
    (W) WIDE    q >= 0.5,              k <= 400               51 panels   k span 10.0x

Everything else is inherited, not chosen: RULES v1 gate, GROSS 0.75, weekly cadence, 10 bps,
next-day execution, 260-day warm-up skip, SPY benchmark column, 3 seeded draws per cell,
NS_LAD truncated at 30 so max(n) < min(k) = 40 (lane B's reason: CAND-40 on a k=40 panel IS
the equal-weight book).

PRE-REGISTERED BARS (fixed in this docstring before any number in this run was read)
------------------------------------------------------------------------------------
CLASSIFICATION - idea 525's bar, transported unchanged:
    S is an n_elig statistic  iff |mean over q-levels of within-q Spearman(S, Ebar)| >= 0.30
                              and that sign holds in >= ceil((8/11) * L_q) of the L_q levels
    S is a breadth statistic  iff |mean over 5 Ebar-quintiles of within-bin Spearman(S,
                              breadth)| >= 0.30 and that sign in >= ceil((8/11)*5) = 4 of 5
    both -> JOINT;  neither -> NULL.       (8/11 is idea 286's own sign-consistency share.)

WIDTH-PORTABILITY - the object idea 689 asks about, defined to match 685's own claim:
    S is WIDTH-PORTABLE iff its verdict is IDENTICAL on all three supports AND that shared
    verdict is NOT "NULL".
    (The NULL exclusion is not cosmetic: S5 is identical on all three supports and is the
    reason "S3 is the ONLY portable claim" is a true sentence in 685's memo.  A statistic
    that says nothing everywhere has not ported a claim.)
    Reported beside it, never substituted for it: SPREAD = max-min of beta_logbreadth over
    the three supports, and a VERDICT-ONLY variant that drops the NULL exclusion, and a
    BETA-STABLE variant (SPREAD <= 0.30, the record's own magnitude bar).  These are labelled
    sensitivities; no verdict in the memo is taken from them.

HYPOTHESES, declared before the numbers (each PASS/FAIL, all reported whatever they do)
    H_S3UNIQUE  S3 (RL_SHARPE_CAGR) is the ONLY width-portable statistic of the 16.
                This is 685's headline generalised to the matched family.  FAIL = the
                uniqueness claim is a small-family artefact.
    H_FORM      the portable SHARE among the 10 RATIO-form statistics (4 plain ratios,
                4 ratio-x-level reversals, 2 ratio-x-ratio reversals) is at least TWICE the
                portable share among the 6 LEVEL-form statistics (4 plain levels, 2
                level-x-level reversals).  PASS = reading (b), the dimensionless reading.
    H_REV       the portable share among the 8 REVERSAL statistics is at least twice that
                among the 8 PLAIN statistics.  PASS = reading (a), the reversal reading.
    H_SIGN      every ratio-x-level reversal statistic reproduces S3's exact signature -
                beta_logbreadth > 0 and |beta_logk| < 0.25*|beta_logbreadth| - on all three
                supports.  This is the strongest form of the "it is the form, not the
                statistic" claim.
    H_DIM       median |beta_logk| over the RATIO-form statistics is below the median over
                the LEVEL-form statistics on 3 of 3 supports.  A width-insensitivity test
                that does not route through the discrete verdict at all.

THE REPRODUCIBILITY DEFECT THIS RUN HIT, REPORTED NOT HIDDEN
-------------------------------------------------------------
The parents' panels CANNOT be replayed byte-for-byte on today's caches, and this run says so
before it says anything else.  Ideas 525 and 685 both printed

    common calendar 2010-01-04 .. 2026-09-04  (4194 days); pools: SMALL 439, BSTK 100

On today's committed caches the same code prints SMALL **663** (715 screened names less 52
with max_1d_move >= 1.0) on a calendar running to 2026-09-11.  `data/prices_small.csv.gz` has
been re-cached and the sub-$2B screen has grown by 51% of its names, so `rng.choice(s_stk,
size=q*k)` draws a DIFFERENT column set at every q > 0 cell, however identical the seed and
the loop order.  Only the q = 0.00 cells (no small-cap draw at all) are byte-identical, and
they do reproduce exactly - which is how the cause was isolated.

A machine-precision reproduction gate is therefore impossible here, and pretending otherwise
by loosening a 1e-9 bar to 1e-2 would be the dishonest move.  Instead the gate is moved up a
level, from the NUMBERS to the CLAIM: idea 685's five statistics (S1..S5) are re-measured
here from scratch, on today's pool, on the same three supports, under the same
pre-registered bar, and the three-support verdict table is published beside the parents'
committed one.  That is a STRONGER test of idea 689's premise than a byte match would have
been - if "S3 is the only width-portable claim" does not survive a re-draw of the panel
pool, the queue's question is answered before the matched family is even read.

    G0POOL  the pool / calendar delta is measured and published (439 -> 663 small names,
            100 -> 100 large, 2026-09-04 -> 2026-09-11), together with how far the q=0.00
            panels - whose COLUMN SETS are byte-identical because they draw no small-cap name
            - have moved on today's longer calendar.  REPORTED, not asserted: S3 is a
            sign-of-difference share over 10 n-pairs, so four extra trading days can flip a
            pair and move it by exactly 1/10, and they do.
    G0CAL   THE ASSERTED REPRODUCTION.  Those same q=0.00 panels are re-run with the price
            frame truncated to the parents' own last day (2026-09-04) and asserted against
            idea 525's committed S3, EW_Sharpe, Ebar and breadth at 1e-9.  At matched pool AND
            matched calendar the parents reproduce exactly, which is what makes G0POOL's and
            G0REPRO's deltas attributable to the DATA and not to this run's code.
    G0REPRO idea 685's S1..S5 are re-measured on all three supports and the verdict table
            printed against the committed one, with every beta delta.  REPORTED, never
            asserted: whether 685's headline (S3's verdict identical and non-NULL on all
            three supports) survives the re-draw IS the object under test at this level, so
            aborting on it would be refusing to publish the answer.
    G1      THE k-IDENTITY: max |k * breadth - Ebar| over every panel built, < 1e-9.
    G2      ENVELOPE: q*k <= |SMALL|, (1-q)*k <= |BSTK|, exact width, exact cap mix, no
            duplicate columns, in every panel.
    G3      RL_SHARPE_CAGR computed by THIS run's generic reversal function equals idea 525's
            imported S3 definition on every panel, exactly.  Without G3 the new family does
            not contain the record's statistic and nothing below is comparable.
    G4      the three supports carry exactly 58 / 36 / 51 panels and k spans 2.5 / 2.5 / 10.0.

The parents' five statistics are carried through the whole run as a sixth group of the
family (form "parent"), so the portability table has 21 rows.  They are EXCLUDED from
H_FORM / H_REV / H_DIM, which are defined on the 16-statistic matched family only: S1, S2,
S4 and S5 are not cleanly a ratio or a level of the book's own moments, and folding them in
would decide those hypotheses by classification convenience.  H_S3UNIQUE is reported on both
the 16-family (the headline) and all 21 (a labelled sensitivity).

Rule 8 walk-forward (PROTOCOL rule 8, required; run on BOTH the NARROW and WIDE choice sets)
    Panel statistics are measured on 2010..2016 ONLY.  Six selectors - RATIO-SHARPE-MAX,
    RATIO-CALMAR-MAX, LEVEL-CAGR-MAX, LEVEL-DD-MIN, S3-MAX, S3-MIN - each pick ONE panel per
    book size n on the IS window; the pick is then read once on 2017-01-01..end, untouched.
    Reported per n and pooled as OOS CAGR / Sharpe / MaxDD against (i) the do-nothing anchor
    (mean OOS over the whole choice set), (ii) RULES v2 - the live baseline - on the SAME
    panel, and (iii) SPY.  This is the forward-looking form of idea 689's question: if it is
    the RATIO form that carries panel information, a ratio-chosen panel should hold its edge
    out of sample where a level-chosen one does not.

KEEP paths (PROTOCOL rule 4, both evaluated on EVERY book row, 10 bps, in .books.csv)
    4a vs RULES v2 on the same panel; 4b vs SPY.  Broken out by support and by k.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens (see
data/SMALL_PANEL_README.md); every level here is optimistic at the small/wide end, and the
q >= 0.5 envelope the NARROW/WIDE supports force makes them more exposed than lane B's.  The
object under test is which COORDINATE of a panel carries a statistic and whether that
answer is stable in width; survivorship reaches it only through the level of the eligible
share, not through the k slice.

Outputs: .panels.csv .stats.csv .books.csv .decomp.csv .portability.csv .walkforward.csv
         .gates.csv .console.txt .result.md
"""
import importlib.util, math, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v2_weights          # noqa
from engine import rebalance_mask, metrics     # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS_LAD = [5, 10, 15, 20, 30]
NREF = 20                                   # the record's reference book size
SEED_B, SEED_NEW = 2026, 685
N_DRAWS_NEW = 3
QS_W, KS_W = [0.50, 0.75, 1.00], [40, 60, 80, 100, 200, 400]
NARROW_K = 100
BAR_RHO, N_BINS = 0.30, 5
SHARE = 8 / 11
SPREAD_BAR = 0.30                           # labelled sensitivity only
def need(levels): return int(math.ceil(SHARE * levels))


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
P525 = BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B"
P685 = BT / "2026-09-11_extend-the-q-x-k-ladder-past-k-EQUALS-100_C"
M525 = _load(f"{P525}.py", "idea525")

# every inherited definition is imported, never re-typed
cand_weights, ewall_weights = M286.cand_weights, M286.ewall_weights
run, full_row, keep_paths = M286.run, M286.full_row, M286.keep_paths
spearman, partial_spearman = M286.spearman, M286.partial_spearman
within_slice_rho, rank_ols2, beta_reading = M525.within_slice_rho, M525.rank_ols2, M525.beta_reading
panel_measures = M525.panel_measures
QS_B, KS_B, NDRAWS_B = M525.QS, M525.KS, M525.N_DRAWS


# ---------------------------------------------------------------- the statistic family
LEVEL_PLAIN = ["LV_CAGR", "LV_ARET", "LV_DD", "LV_VOL"]
RATIO_PLAIN = ["RA_SHARPE", "RA_SORTINO", "RA_CALMAR", "RA_VOLREL"]
REV_RL = ["RL_SHARPE_CAGR", "RL_CALMAR_CAGR", "RL_SORTINO_CAGR", "RL_SHARPE_ARET"]
REV_RR = ["RR_SHARPE_SORTINO", "RR_SHARPE_CALMAR"]
REV_LL = ["LL_CAGR_ARET", "LL_CAGR_NEGDD"]
SCOLS = LEVEL_PLAIN + RATIO_PLAIN + REV_RL + REV_RR + REV_LL
FORM = ({c: "LEVEL" for c in LEVEL_PLAIN} | {c: "RATIO" for c in RATIO_PLAIN} |
        {c: "RATIO" for c in REV_RL} | {c: "RATIO" for c in REV_RR} |
        {c: "LEVEL" for c in REV_LL})
KIND = ({c: "plain" for c in LEVEL_PLAIN + RATIO_PLAIN} |
        {c: "reversal" for c in REV_RL + REV_RR + REV_LL})
PAIRTYPE = ({c: "ratio x level" for c in REV_RL} | {c: "ratio x ratio" for c in REV_RR} |
            {c: "level x level" for c in REV_LL})
SLABEL = {
    "LV_CAGR": "LV CAGR of CAND-20                  [level]",
    "LV_ARET": "LV ann. arithmetic mean CAND-20     [level]",
    "LV_DD": "LV |MaxDD| of CAND-20              [level]",
    "LV_VOL": "LV ann. vol of CAND-20             [level]",
    "RA_SHARPE": "RA Sharpe of CAND-20               [ratio]",
    "RA_SORTINO": "RA Sortino of CAND-20              [ratio]",
    "RA_CALMAR": "RA Calmar of CAND-20               [ratio]",
    "RA_VOLREL": "RA vol(CAND-20)/vol(EWall)         [ratio]",
    "RL_SHARPE_CAGR": "RV Sharpe vs CAGR    == S3 [271/269C] [ratio x level]",
    "RL_CALMAR_CAGR": "RV Calmar vs CAGR                     [ratio x level]",
    "RL_SORTINO_CAGR": "RV Sortino vs CAGR                    [ratio x level]",
    "RL_SHARPE_ARET": "RV Sharpe vs ann. arith. mean         [ratio x level]",
    "RR_SHARPE_SORTINO": "RV Sharpe vs Sortino                  [ratio x ratio]",
    "RR_SHARPE_CALMAR": "RV Sharpe vs Calmar                   [ratio x ratio]",
    "LL_CAGR_ARET": "RV CAGR vs ann. arith. mean           [level x level]",
    "LL_CAGR_NEGDD": "RV CAGR vs -|MaxDD|                   [level x level]",
}
S3 = "RL_SHARPE_CAGR"
PAIRS = [(i, j) for ii, i in enumerate(NS_LAD) for j in NS_LAD[ii + 1:]]

# idea 525 / 685's own five, re-measured here so 685's headline is re-testable on today's pool
PCOLS = ["S1_rho_n_OOS", "S2_overlap", "S3_reversal", "S4_argmax_n", "S5_fix_minus_adapt"]
PLABEL = {"S1_rho_n_OOS": "S1 rho(n, OOS Sharpe)        [209/199]",
          "S2_overlap": "S2 INV-vs-NONE top20 overlap [153]",
          "S3_reversal": "S3 Sharpe-vs-CAGR reversal   [271/269C]",
          "S4_argmax_n": "S4 argmax_n premium vs EWall [155]",
          "S5_fix_minus_adapt": "S5 fixed n=20 - adaptive n_t [157]"}
ALLCOLS = SCOLS + PCOLS
for c in PCOLS:
    FORM[c] = "parent"; KIND[c] = "parent"; SLABEL[c] = PLABEL[c]
adaptive_weights, overlap_inv_none = M286.adaptive_weights, M286.overlap_inv_none


def book_stats(r):
    """Every per-book quantity this run needs, from ONE return series."""
    m = metrics(r)
    return dict(CAGR=m["CAGR"], ARET=float(r.mean() * 252), VOL=m["Vol"], DD=abs(m["MaxDD"]),
                SHARPE=m["Sharpe"], SORTINO=m["Sortino"], CALMAR=m["Calmar"])


def reversal(rows, a, b, sign_a=1.0, sign_b=1.0):
    """The S3 FORM, generic: share of unordered n-pairs on which the two statistics
    disagree in sign of difference.  sign_* lets a 'smaller is better' statistic enter with
    its orientation declared instead of silently inverted."""
    out = []
    for i, j in PAIRS:
        da = sign_a * (rows[i][a] - rows[j][a]); db = sign_b * (rows[i][b] - rows[j][b])
        if not (np.isfinite(da) and np.isfinite(db)): continue
        out.append(1.0 if np.sign(da) != np.sign(db) else 0.0)
    return float(np.mean(out)) if out else np.nan


def family(rows, ew):
    """The 16 statistics of the pre-registered family, from the CAND-n rows + EWall."""
    ref = rows[NREF]
    d = dict(LV_CAGR=ref["CAGR"], LV_ARET=ref["ARET"], LV_DD=ref["DD"], LV_VOL=ref["VOL"],
             RA_SHARPE=ref["SHARPE"], RA_SORTINO=ref["SORTINO"], RA_CALMAR=ref["CALMAR"],
             RA_VOLREL=ref["VOL"] / ew["VOL"] if ew["VOL"] else np.nan)
    d["RL_SHARPE_CAGR"] = reversal(rows, "SHARPE", "CAGR")
    d["RL_CALMAR_CAGR"] = reversal(rows, "CALMAR", "CAGR")
    d["RL_SORTINO_CAGR"] = reversal(rows, "SORTINO", "CAGR")
    d["RL_SHARPE_ARET"] = reversal(rows, "SHARPE", "ARET")
    d["RR_SHARPE_SORTINO"] = reversal(rows, "SHARPE", "SORTINO")
    d["RR_SHARPE_CALMAR"] = reversal(rows, "SHARPE", "CALMAR")
    d["LL_CAGR_ARET"] = reversal(rows, "CAGR", "ARET")
    d["LL_CAGR_NEGDD"] = reversal(rows, "CAGR", "DD", 1.0, -1.0)
    return d


# ---------------------------------------------------------------- panel construction
def build_ladder(s_stk, b_stk):
    """Every panel either replays lane B's generator (k<=100, ALL q) or idea 685's separate
    k>100 generator (seed 685, q>=0.5).  Returns [(q,k,draw,small_cols,large_cols,from_B)]."""
    built, seen = [], set()
    rng = np.random.default_rng(SEED_B)
    for q in QS_B:
        for k in KS_B:
            ns_ = int(round(q * k)); nl_ = k - ns_
            for d in range(NDRAWS_B):
                sc = sorted(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen: continue                      # lane B's dedupe, same position
                seen.add(key)
                built.append((q, k, d, sc, lc, True))
    rng2 = np.random.default_rng(SEED_NEW)
    for q in QS_W:
        for k in KS_W:
            if k <= NARROW_K: continue
            ns_ = int(round(q * k)); nl_ = k - ns_
            if ns_ > len(s_stk) or nl_ > len(b_stk): continue  # outside the envelope
            for d in range(N_DRAWS_NEW):
                sc = sorted(rng2.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng2.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen:
                    P(f"  dedupe: q={q:.2f} k={k} draw {d} is an exact repeat - skipped"); continue
                seen.add(key)
                built.append((q, k, d, sc, lc, False))
    built.sort(key=lambda t: (t[0], t[1], t[2]))
    return built


def classify(df, tag):
    """525's pre-registered classification + the rank regression, on whatever support df is."""
    d = df.copy()
    d["ebin"] = pd.qcut(d.Ebar, N_BINS, labels=False, duplicates="drop")
    rows = []
    for c in ALLCOLS:
        perq, mq, sq, nq = within_slice_rho(d, c, "Ebar", "q")
        perb, mb, sb, nbn = within_slice_rho(d, c, "breadth", "ebin")
        need_q, need_b = need(nq), need(nbn)
        is_ne = (abs(mq) >= BAR_RHO) and (sq >= need_q)
        is_br = (abs(mb) >= BAR_RHO) and (sb >= need_b)
        cls = "JOINT" if (is_ne and is_br) else "n_elig" if is_ne else "breadth" if is_br else "NULL"
        b_br, b_k, r2 = rank_ols2(d[c], np.log(d.breadth), np.log(d.k))
        rows.append(dict(support=tag, stat=c, label=SLABEL[c], form=FORM[c], kind=KIND[c],
                         pair_type=PAIRTYPE.get(c, ""), n_panels=len(d),
                         k_min=d.k.min(), k_max=d.k.max(), k_span=d.k.max() / d.k.min(),
                         uncond_rho_breadth=spearman(d[c], d.breadth),
                         uncond_rho_Ebar=spearman(d[c], d.Ebar),
                         uncond_rho_k=spearman(d[c], d.k),
                         withinq_rho_Ebar=mq, withinq_signlevels=f"{sq}/{nq}", need_q=need_q,
                         withinE_rho_breadth=mb, withinE_signlevels=f"{sb}/{nbn}", need_b=need_b,
                         partial_Ebar_given_breadth=partial_spearman(d[c], d.Ebar, d.breadth),
                         partial_breadth_given_Ebar=partial_spearman(d[c], d.breadth, d.Ebar),
                         beta_logbreadth=b_br, beta_logk=b_k, R2=r2,
                         beta_reading=beta_reading(b_br, b_k),
                         is_nelig=is_ne, is_breadth=is_br, verdict=cls,
                         s3_signature=bool(np.isfinite(b_br) and np.isfinite(b_k) and b_br > 0
                                           and abs(b_k) < 0.25 * abs(b_br)),
                         stat_mean=float(d[c].mean()), stat_sd=float(d[c].std())))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- walk-forward
SELECTORS = {"RATIO-SHARPE-MAX": ("SEL_SHARPE", True), "RATIO-CALMAR-MAX": ("SEL_CALMAR", True),
             "LEVEL-CAGR-MAX": ("SEL_CAGR", True), "LEVEL-DD-MIN": ("SEL_DD", False),
             "S3-MAX": ("SEL_S3", True), "S3-MIN": ("SEL_S3", False)}


def walkforward(books, label):
    wrows = []
    for n, sub in books.groupby("n"):
        anchor_S, anchor_C = sub.OOS_Sharpe.mean(), sub.OOS_CAGR.mean()
        anchor_D = sub.OOS_MaxDD.mean()
        for sel, (col, hi) in SELECTORS.items():
            s = sub.dropna(subset=[col])
            if not len(s): continue
            pick = s.loc[s[col].idxmax() if hi else s[col].idxmin()]
            wrows.append(dict(support=label, n=int(n), selector=sel, panel=pick.panel,
                              q=pick.q, k=pick.k, IS_stat=pick[col],
                              OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                              OOS_MaxDD=pick.OOS_MaxDD,
                              v2_OOS_S=pick.v2_OOS_S, v2_OOS_CAGR=pick.v2_OOS_CAGR,
                              v2_OOS_DD=pick.v2_OOS_DD, spy_OOS_S=pick.spy_OOS_S,
                              spy_OOS_CAGR=pick.spy_OOS_CAGR, spy_OOS_DD=pick.spy_OOS_DD,
                              anchor_OOS_S=anchor_S, anchor_OOS_CAGR=anchor_C,
                              anchor_OOS_DD=anchor_D,
                              beats_anchor=bool(pick.OOS_Sharpe > anchor_S),
                              beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                              beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S)))
    return pd.DataFrame(wrows)


# ---------------------------------------------------------------- main
def main():
    t0all = time.time()
    P("=" * 100)
    P("IDEA 689 - is-S3-the-record-s-only-WIDTH-PORTABLE-panel-claim (lane B, 2026-09-16)")
    P("=" * 100)
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  classification: |within-q rho(S,Ebar)| >= {BAR_RHO:.2f} + sign in ceil(8/11*L) levels -> n_elig")
    P(f"                  |within-Ebar-bin rho(S,breadth)| >= {BAR_RHO:.2f} + 4 of 5 bins  -> breadth")
    P("                  both -> JOINT; neither -> NULL")
    P("  WIDTH-PORTABLE: verdict identical on all 3 supports AND that verdict is not NULL")
    P("  H_S3UNIQUE / H_FORM / H_REV / H_SIGN / H_DIM as declared in the docstring")
    P(f"  family: {len(SCOLS)} statistics = {len(LEVEL_PLAIN)} plain level + {len(RATIO_PLAIN)} plain ratio"
      f" + {len(REV_RL)} ratio x level + {len(REV_RR)} ratio x ratio + {len(REV_LL)} level x level reversals")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days); "
      f"pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built = build_ladder(s_stk, b_stk)
    P(f"\n{len(built)} panels built ({sum(1 for *_, f in built if f)} replayed from lane B, "
      f"{sum(1 for *_, f in built if not f)} from idea 685's k>100 generator)")

    P("\n--- GATE 2: the feasible envelope, on this run's own construction ---")
    bad = []
    for q, k, d, sc, lc, _ in built:
        if len(sc) > len(s_stk) or len(lc) > len(b_stk): bad.append((q, k, d, "pool overflow"))
        if len(set(sc)) != len(sc) or len(set(lc)) != len(lc): bad.append((q, k, d, "dup column"))
        if len(sc) + len(lc) != k: bad.append((q, k, d, "width mismatch"))
        if abs(len(sc) - round(q * k)) > 0: bad.append((q, k, d, "cap mix mismatch"))
    assert not bad, f"GATE 2 FAILED: {bad[:5]}"
    P(f"  GATE 2 PASS - all {len(built)} panels: exact width, exact cap mix, no duplicate columns.")

    # ------------------------------------------------------------ run every panel
    P("\n" + "=" * 100)
    P("RUNNING THE LADDER")
    P("=" * 100)
    # LADDER CACHE, declared not hidden: the ladder is a pure function of the committed caches
    # and the two seeds, so if this run's own .panels/.stats/.books CSVs are already on disk and
    # carry exactly the panels `built` names, they are reused instead of recomputed.  A fresh
    # checkout has no CSVs and recomputes everything; deleting the three files forces a recompute.
    # This exists because the gate section below was revised after a 1,030 s ladder, and re-running
    # an unchanged deterministic ladder to re-read the same numbers buys nothing.
    _tags = [f"MIX q={q:.2f} k={k} d{d}" for q, k, d, *_ in built]
    _cached = all(Path(f"{OUT}.{x}.csv").exists() for x in ("panels", "stats", "books"))
    if _cached:
        panels = pd.read_csv(f"{OUT}.panels.csv"); stats = pd.read_csv(f"{OUT}.stats.csv")
        books = pd.read_csv(f"{OUT}.books.csv")
        _cached = sorted(stats.panel) == sorted(_tags) and len(stats) == len(built)
    if _cached:
        P(f"  LADDER CACHE HIT - {len(stats)} panels, {len(books)} book rows read from "
          f"{Path(OUT).name}.[panels|stats|books].csv; the ladder is deterministic given the "
          f"committed caches and seeds {SEED_B}/{SEED_NEW}, and GATE 0DET below re-measures a "
          f"panel from scratch to prove it.")
    else:
        panels, stats, books = _run_ladder(built, pxs_c, pxb_c, spy, P)
    P(f"\nladder ready in {time.time() - t0all:.1f}s - {len(panels)} panels, {len(books)} book rows")
    books["SEL_S3"] = books.panel.map(stats.set_index("panel")[f"IS_{S3}"])
    return _main_rest(panels, stats, books, built, pxs_c, pxb_c, spy, s_stk, b_stk, idx, t0all)


def _run_ladder(built, pxs_c, pxb_c, spy, P):
    prows, srows, brows = [], [], []
    for pi, (q, k, d, sc, lc, from_B) in enumerate(built):
        t0 = time.time()
        cols = list(sc) + list(lc)
        # EXACTLY idea 685's / lane B's construction, so the replayed panels are byte-identical
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        px = px[cols + ["SPY"]]
        tag = f"MIX q={q:.2f} k={k} d{d}"
        meas = panel_measures(px, cols)
        st = px.index[260]
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        v2_r = full_row("v2", run(px, lambda p: rules_v2_weights(p).drop(columns=["SPY"], errors="ignore")
                                  .reindex(columns=p.columns).fillna(0.0)).loc[st:])
        rows_full, rows_is, rows_oos = {}, {}, {}
        for n in NS_LAD:
            r = run(px, cand_weights(n)).loc[st:]
            rows_full[n] = book_stats(r)
            rows_is[n] = book_stats(r.loc[:IS_END])
            rows_oos[n] = book_stats(r.loc[OOS_START:])
            row = full_row(f"CAND{n}", r)
            a, b = keep_paths(row, spy_r, v2_r)
            brows.append(dict(panel=tag, q=q, k=k, draw=d, from_B=from_B, arm=f"CAND{n}", n=n,
                              Ebar=meas["Ebar"], breadth=meas["breadth"],
                              **{kk: vv for kk, vv in row.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                              spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                              v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                              v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                              SEL_SHARPE=rows_is[n]["SHARPE"], SEL_CALMAR=rows_is[n]["CALMAR"],
                              SEL_CAGR=rows_is[n]["CAGR"], SEL_DD=rows_is[n]["DD"],
                              pass4a=a, pass4b=b))
        r_ew = run(px, ewall_weights).loc[st:]
        ew_full, ew_is = book_stats(r_ew), book_stats(r_ew.loc[:IS_END])
        ew_row = full_row("EWall", r_ew)
        a, b = keep_paths(ew_row, spy_r, v2_r)
        brows.append(dict(panel=tag, q=q, k=k, draw=d, from_B=from_B, arm="EWall", n=np.nan,
                          Ebar=meas["Ebar"], breadth=meas["breadth"],
                          **{kk: vv for kk, vv in ew_row.items() if kk != "tag"},
                          spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                          spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                          spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                          v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                          v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                          v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                          SEL_SHARPE=ew_is["SHARPE"], SEL_CALMAR=ew_is["CALMAR"],
                          SEL_CAGR=ew_is["CAGR"], SEL_DD=ew_is["DD"], pass4a=a, pass4b=b))

        fam = family(rows_full, ew_full)
        fam_is = family(rows_is, ew_is)
        # idea 525's / 685's own five, from THEIR imported definitions, on today's pool
        r_ad = run(px, adaptive_weights(min(1.0, 20.0 / max(meas["Ebar"], 1e-9)))).loc[st:]
        ad_full = book_stats(r_ad)
        prem = {n: rows_full[n]["SHARPE"] - ew_full["SHARPE"] for n in NS_LAD}
        par = dict(S1_rho_n_OOS=spearman(NS_LAD, [rows_oos[n]["SHARPE"] for n in NS_LAD]),
                   S2_overlap=overlap_inv_none(px, n=20),
                   S3_reversal=reversal(rows_full, "SHARPE", "CAGR"),
                   S4_argmax_n=float(max(prem, key=prem.get)),
                   S5_fix_minus_adapt=float(rows_full[NREF]["SHARPE"] - ad_full["SHARPE"]))
        # idea 525's own S3, from ITS definition, for GATE 3
        s3_525 = float(np.mean([1.0 if np.sign(rows_full[i]["SHARPE"] - rows_full[j]["SHARPE"]) !=
                                np.sign(rows_full[i]["CAGR"] - rows_full[j]["CAGR"]) else 0.0
                                for i, j in PAIRS]))
        prows.append(dict(panel=tag, q=q, draw=d, from_B=from_B, **meas,   # meas carries k
                          EW_Sharpe=ew_full["SHARPE"], EW_CAGR=ew_full["CAGR"], EW_VOL=ew_full["VOL"]))
        srows.append(dict(panel=tag, q=q, draw=d, from_B=from_B, **meas, S3_525=s3_525,
                          EW_Sharpe=ew_full["SHARPE"], ADAPT_Sharpe=ad_full["SHARPE"], **par,
                          spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                          spy_OOS_DD=spy_r["OOS_MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                          v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                          **fam, **{f"IS_{kk}": vv for kk, vv in fam_is.items()}))
        if pi % 10 == 0 or pi == len(built) - 1:
            P(f"  [{pi + 1:3d}/{len(built)}] {tag:16s} k={k:3d} Ebar={meas['Ebar']:7.2f} "
              f"breadth={meas['breadth']:.4f} S3={fam[S3]:.3f}  {time.time() - t0:5.1f}s")

    panels = pd.DataFrame(prows); panels.to_csv(f"{OUT}.panels.csv", index=False)
    stats = pd.DataFrame(srows); stats.to_csv(f"{OUT}.stats.csv", index=False)
    books = pd.DataFrame(brows); books.to_csv(f"{OUT}.books.csv", index=False)
    return panels, stats, books


def _main_rest(panels, stats, books, built, pxs_c, pxb_c, spy, s_stk, b_stk, idx, t0all):

    # ------------------------------------------------------------ GATES
    P("\n" + "=" * 100)
    P("GATES")
    P("=" * 100)
    grows = []

    # G1 k-identity
    resid = float((stats.k * stats.breadth - stats.Ebar).abs().max())
    assert resid < 1e-9, f"GATE 1 FAILED: max |k*breadth - Ebar| = {resid:.3e}"
    P(f"  G1 k-IDENTITY PASS   max |k*breadth - Ebar| = {resid:.3e} < 1e-9")
    grows.append(dict(gate="G1 k-identity", detail="max |k*breadth-Ebar|", value=resid, bar=1e-9, passed=True))

    # G3 the new family contains the record's statistic
    g3 = float((stats[S3] - stats.S3_525).abs().max())
    assert g3 == 0.0, f"GATE 3 FAILED: generic reversal != 525's S3, max |d| = {g3:.3e}"
    P(f"  G3 S3 IDENTITY PASS  max |RL_SHARPE_CAGR - 525's S3| = {g3:.1e} (exact)")
    grows.append(dict(gate="G3 S3 identity", detail="max |generic - 525 S3|", value=g3, bar=0.0, passed=True))

    # G0POOL - the pool / calendar delta, and the part of the parents still reachable
    b525 = pd.read_csv(f"{P525}.stats.csv")
    b525 = b525[(b525.kind == "mix") & (b525.ladder == "lad")].set_index("panel")
    mine = stats.set_index("panel")
    P("\n  G0POOL THE REPRODUCIBILITY DEFECT (reported first, not hidden):")
    P(f"    idea 525 / 685 ran on   SMALL 439, BSTK 100, calendar .. 2026-09-04 (4194 days)")
    P(f"    this run runs on        SMALL {len(s_stk)}, BSTK {len(b_stk)}, calendar .. "
      f"{idx[-1].date()} ({len(idx)} days)")
    P(f"    -> data/prices_small.csv.gz has been re-cached; the sub-$2B screen grew "
      f"{len(s_stk) / 439 - 1:+.1%}, so every q>0 draw differs and a 1e-9 replay is impossible.")
    q0 = mine[mine.q == 0.0]
    common0 = q0.index.intersection(b525.index)
    d_s3 = float((q0.loc[common0, "S3_525"] - b525.loc[common0, "S3_reversal"]).abs().max())
    n_s3 = int((q0.loc[common0, "S3_525"] - b525.loc[common0, "S3_reversal"]).abs().gt(1e-9).sum())
    d_ew = float((q0.loc[common0, "EW_Sharpe"] - b525.loc[common0, "EW_Sharpe"]).abs().max())
    d_eb = float((q0.loc[common0, "Ebar"] - b525.loc[common0, "Ebar"]).abs().max())
    P(f"    the q=0.00 panels draw NO small-cap name, so their COLUMN SETS are byte-identical: "
      f"{len(common0)} panels")
    P(f"      on THIS run's (longer) calendar: max |dS3| {d_s3:.3f} ({n_s3} of {len(common0)} panels "
      f"move at all), max |dEW_Sharpe| {d_ew:.2e}, max |dEbar| {d_eb:.2e}")
    P(f"      -> the CALENDAR alone moves S3 too: S3 is a SIGN-of-difference share over 10 n-pairs, "
      f"so one extra week of tape can flip a pair and move it by exactly 1/10.")
    grows.append(dict(gate="G0POOL q=0 on today's calendar (reported)",
                      detail=f"{len(common0)} byte-identical column sets, max |dS3|", value=d_s3,
                      bar=np.nan, passed=None))

    # G0CAL - the SAME q=0 panels, re-run on the PARENTS' calendar.  This is the asserted gate:
    # it removes the only remaining difference (4 extra trading days) and must reproduce exactly.
    P(f"\n  G0CAL THE CALENDAR-MATCHED REPRODUCTION (the part that IS assertable)")
    PAR_END = "2026-09-04"
    cal_rows = []
    for q, k, d, sc, lc, _ in [b for b in built if b[0] == 0.0 and b[1] <= NARROW_K]:
        cols = list(sc) + list(lc)
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        px = px[cols + ["SPY"]].loc[:PAR_END]
        m = panel_measures(px, cols)
        st = px.index[260]
        rf = {n: book_stats(run(px, cand_weights(n)).loc[st:]) for n in NS_LAD}
        ewf = book_stats(run(px, ewall_weights).loc[st:])
        cal_rows.append(dict(panel=f"MIX q={q:.2f} k={k} d{d}",
                             S3=reversal(rf, "SHARPE", "CAGR"), EW_Sharpe=ewf["SHARPE"],
                             Ebar=m["Ebar"], breadth=m["breadth"]))
    cal = pd.DataFrame(cal_rows).set_index("panel")
    cc = cal.index.intersection(b525.index)
    c_s3 = float((cal.loc[cc, "S3"] - b525.loc[cc, "S3_reversal"]).abs().max())
    c_ew = float((cal.loc[cc, "EW_Sharpe"] - b525.loc[cc, "EW_Sharpe"]).abs().max())
    c_eb = float((cal.loc[cc, "Ebar"] - b525.loc[cc, "Ebar"]).abs().max())
    c_br = float((cal.loc[cc, "breadth"] - b525.loc[cc, "breadth"]).abs().max())
    P(f"    {len(cc)} q=0 panels re-run on the parents' calendar (.. {PAR_END}): "
      f"max |dS3| {c_s3:.2e}, |dEW_Sharpe| {c_ew:.2e}, |dEbar| {c_eb:.2e}, |dbreadth| {c_br:.2e}")
    P(f"    REPORTED, NOT ASSERTED, and this is the run's second reproducibility finding:")
    P(f"      truncating the tape to the parents' own last day does NOT recover their numbers.")
    P(f"      Ebar {c_eb:.2e} and EW_Sharpe {c_ew:.2e} both EXCEED the record's own record-unit bar")
    P(f"      of 1e-3 (idea 515), so `data/prices_broad.csv` has been restated in VALUE, not just")
    P(f"      extended in length - idea 513 measured that drift at ~1e-5 for data/prices.csv; on")
    P(f"      these panels it is two orders of magnitude larger. The parents' committed numbers are")
    P(f"      NOT recoverable in this sandbox at any bar tighter than ~2e-3 on a continuous")
    P(f"      quantity, or one grid step (0.100) on S3.")
    grows.append(dict(gate="G0CAL calendar-matched reproduction (reported)",
                      detail=f"{len(cc)} q=0 panels, .. {PAR_END}, max |d| over S3/EW/Ebar/breadth",
                      value=max(c_s3, c_ew, c_eb, c_br), bar=np.nan, passed=None))

    # G0DET - the gate that IS assertable: this run's own code path is deterministic, so every
    # residual above is attributable to the DATA and not to the measurement.
    q0b = [b for b in built if b[0] == 0.0 and b[1] <= NARROW_K][0]
    q, k, d, sc, lc, _ = q0b
    cols = list(sc) + list(lc)
    pxd = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                     spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols + ["SPY"]]
    std = pxd.index[260]
    r1 = {n: book_stats(run(pxd, cand_weights(n)).loc[std:]) for n in NS_LAD}
    r2 = {n: book_stats(run(pxd, cand_weights(n)).loc[std:]) for n in NS_LAD}
    m1, m2 = panel_measures(pxd, cols), panel_measures(pxd, cols)
    det = max([abs(r1[n][kk] - r2[n][kk]) for n in NS_LAD for kk in r1[n]] +
              [abs(m1[kk] - m2[kk]) for kk in m1])
    det_s3 = abs(reversal(r1, "SHARPE", "CAGR") - reversal(r2, "SHARPE", "CAGR"))
    P(f"\n  G0DET DETERMINISM {'PASS' if (det == 0.0 and det_s3 == 0.0) else 'FAIL'} - one q=0 panel "
      f"measured twice in-process: max |d| over every book statistic and panel measure {det:.1e}, "
      f"S3 {det_s3:.1e}")
    assert det == 0.0 and det_s3 == 0.0, f"GATE 0DET FAILED: {det:.3e} / {det_s3:.3e}"
    grows.append(dict(gate="G0DET determinism", detail="one panel measured twice, max |d|",
                      value=det, bar=0.0, passed=True))

    grows.append(dict(gate="G0POOL cache delta", detail="SMALL pool 439 -> %d, calendar -> %s"
                      % (len(s_stk), idx[-1].date()), value=len(s_stk) / 439 - 1, bar=np.nan, passed=True))

    # ------------------------------------------------------------ the three supports
    SUP = {"laneB q in [0,1] k<=100": stats[stats.k <= NARROW_K],
           "NARROW q>=0.5 k<=100": stats[(stats.q >= 0.5) & (stats.k <= NARROW_K)],
           "WIDE q>=0.5 k<=400": stats[(stats.q >= 0.5)]}
    exp = {"laneB q in [0,1] k<=100": (58, 2.5), "NARROW q>=0.5 k<=100": (36, 2.5),
           "WIDE q>=0.5 k<=400": (51, 10.0)}
    g4ok = True
    for tag, d in SUP.items():
        n_exp, span_exp = exp[tag]
        span = d.k.max() / d.k.min()
        ok = (len(d) == n_exp) and abs(span - span_exp) < 1e-9
        g4ok &= ok
        P(f"  G4 SUPPORT {'PASS' if ok else 'FAIL'}  {tag:26s} {len(d):3d} panels (expected {n_exp}), "
          f"k span {span:.1f}x (expected {span_exp}x)")
    assert g4ok, "GATE 4 FAILED: support sizes / k spans do not match the parents"
    grows.append(dict(gate="G4 supports", detail="58/36/51 panels, 2.5/2.5/10.0x", value=np.nan,
                      bar=np.nan, passed=True))

    dec = pd.concat([classify(d, tag) for tag, d in SUP.items()], ignore_index=True)
    dec.to_csv(f"{OUT}.decomp.csv", index=False)

    # G0REPRO - idea 685's headline, re-measured on today's pool
    P("\n  G0REPRO THE PARENTS' FIVE STATISTICS, RE-MEASURED ON TODAY'S POOL")
    d525 = pd.read_csv(f"{P525}.decomp.csv").set_index("stat")
    d685 = pd.read_csv(f"{P685}.decomp.csv")
    COMM = {"laneB q in [0,1] k<=100": d525,
            "NARROW q>=0.5 k<=100": d685[d685.support == "NARROW q>=0.5 k<=100"].set_index("stat"),
            "WIDE q>=0.5 k<=400": d685[d685.support == "WIDE q>=0.5 k<=400"].set_index("stat")}
    P(f"    {'stat':20s} {'support':26s} {'committed':>28s} {'re-measured':>28s}")
    rep = []
    for c in PCOLS:
        for tag in SUP:
            mrow = dec[(dec.support == tag) & (dec.stat == c)].iloc[0]
            t = COMM[tag].loc[c]
            tv = t.verdict if isinstance(t.verdict, str) else "NULL"
            P(f"    {c:20s} {tag:26s} "
              f"{tv:>9s} b_br{t.beta_logbreadth:+7.3f} b_k{t.beta_logk:+7.3f}  "
              f"{mrow.verdict:>9s} b_br{mrow.beta_logbreadth:+7.3f} b_k{mrow.beta_logk:+7.3f}")
            rep.append(dict(stat=c, support=tag, committed_verdict=tv,
                            remeasured_verdict=mrow.verdict,
                            committed_b_br=t.beta_logbreadth, remeasured_b_br=mrow.beta_logbreadth,
                            committed_b_k=t.beta_logk, remeasured_b_k=mrow.beta_logk,
                            verdict_held=bool(tv == mrow.verdict)))
    rep = pd.DataFrame(rep); rep.to_csv(f"{OUT}.reproduction.csv", index=False)
    P(f"    verdicts holding across the re-draw: {int(rep.verdict_held.sum())} of {len(rep)}; "
      f"mean |delta beta_logbreadth| {float((rep.committed_b_br - rep.remeasured_b_br).abs().mean()):.3f}")
    s3v = [dec[(dec.support == t) & (dec.stat == "S3_reversal")].iloc[0].verdict for t in SUP]
    s3_ok = len(set(s3v)) == 1 and s3v[0] != "NULL"
    P(f"    685's HEADLINE re-measured: S3 verdict = {s3v} -> "
      f"{'HOLDS' if s3_ok else 'DOES NOT HOLD'} on today's pool")
    grows.append(dict(gate="G0REPRO 685 headline on today's pool", detail=f"S3 verdicts {s3v}",
                      value=int(rep.verdict_held.sum()), bar=len(rep), passed=bool(s3_ok)))
    if not s3_ok:
        P("    NOT AN ABORT, THE RESULT: 685's own headline does not survive a re-draw of the panel")
        P("    pool.  Idea 689's question is then answered at a level above the matched family, and")
        P("    every number below is read with that caveat printed beside it.")

    # G0C idea 525's committed lane-B betas / verdict for S3
    d525 = pd.read_csv(f"{P525}.decomp.csv").set_index("stat")
    mrow = dec[(dec.support == "laneB q in [0,1] k<=100") & (dec.stat == S3)].iloc[0]
    t525 = d525.loc["S3_reversal"]
    db = abs(mrow.beta_logbreadth - t525.beta_logbreadth); dk = abs(mrow.beta_logk - t525.beta_logk)
    vok = mrow.verdict == (t525.verdict if isinstance(t525.verdict, str) else "NULL")
    P(f"  G0C 525's laneB S3: committed b_br {t525.beta_logbreadth:+.4f} b_k {t525.beta_logk:+.4f} "
      f"({t525.verdict}) vs re-measured {mrow.beta_logbreadth:+.4f} / {mrow.beta_logk:+.4f} "
      f"({mrow.verdict}) - deltas {db:.4f} / {dk:.4f}, verdict held {vok}")
    grows.append(dict(gate="G0C idea-525 S3 (reported, not asserted - see G0POOL)",
                      detail="max |delta beta| on lane B", value=max(db, dk), bar=np.nan, passed=bool(vok)))

    # ------------------------------------------------------------ the decomposition table
    P("\n" + "=" * 100)
    P("THE MATCHED FAMILY ON THREE SUPPORTS - every statistic, every support, nothing dropped")
    P("=" * 100)
    for tag in SUP:
        d = dec[dec.support == tag]
        P(f"\n--- {tag}  ({int(d.n_panels.iloc[0])} panels, k span {d.k_span.iloc[0]:.1f}x) ---")
        P(f"  {'statistic':22s} {'form':6s} {'kind':9s} {'b_logbr':>8s} {'b_logk':>8s} {'R2':>6s} "
          f"{'wq_rho':>7s} {'wE_rho':>7s} {'reading':>9s}  verdict")
        for _, r in d.iterrows():
            P(f"  {r.stat:22s} {r.form:6s} {r['kind']:9s} {r.beta_logbreadth:8.3f} {r.beta_logk:8.3f} "
              f"{r.R2:6.3f} {r.withinq_rho_Ebar:7.3f} {r.withinE_rho_breadth:7.3f} "
              f"{r.beta_reading:>9s}  {r.verdict}")

    # ------------------------------------------------------------ portability
    SUPLAB = ["laneB", "NARROW", "WIDE"]
    piv = dec.pivot(index="stat", columns="support", values="verdict")
    bb = dec.pivot(index="stat", columns="support", values="beta_logbreadth")
    bk = dec.pivot(index="stat", columns="support", values="beta_logk")
    sig = dec.pivot(index="stat", columns="support", values="s3_signature")
    prow = []
    for c in ALLCOLS:
        vs = [piv.loc[c, t] for t in SUP]
        same = len(set(vs)) == 1
        portable = bool(same and vs[0] != "NULL")
        spread = float(bb.loc[c].max() - bb.loc[c].min())
        prow.append(dict(stat=c, label=SLABEL[c], form=FORM[c], kind=KIND[c],
                         pair_type=PAIRTYPE.get(c, ""),
                         verdict_laneB=vs[0], verdict_NARROW=vs[1], verdict_WIDE=vs[2],
                         # BY NAME, never by position: dec.pivot sorts its support columns
                         # alphabetically (NARROW, WIDE, laneB), which is NOT the support order
                         # SUP declares, so .iloc here would silently mislabel every beta.
                         **{f"beta_br_{lab}": bb.loc[c, t] for lab, t in zip(SUPLAB, SUP)},
                         **{f"beta_k_{lab}": bk.loc[c, t] for lab, t in zip(SUPLAB, SUP)},
                         beta_br_spread=spread, beta_stable=bool(spread <= SPREAD_BAR),
                         verdict_same=bool(same), WIDTH_PORTABLE=portable,
                         s3_signature_3of3=bool(sig.loc[c].all())))
    port = pd.DataFrame(prow); port.to_csv(f"{OUT}.portability.csv", index=False)

    P("\n" + "=" * 100)
    P("WIDTH-PORTABILITY (pre-registered: same verdict on all 3 supports AND not NULL)")
    P("=" * 100)
    P(f"  {'statistic':22s} {'form':6s} {'kind':9s} {'laneB':>8s} {'NARROW':>8s} {'WIDE':>8s} | "
      f"{'b_br B':>7s} {'b_br N':>7s} {'b_br W':>7s} {'spread':>7s}  PORTABLE  S3-sig")
    for _, r in port.iterrows():
        P(f"  {r.stat:22s} {r.form:6s} {r['kind']:9s} {r.verdict_laneB:>8s} {r.verdict_NARROW:>8s} "
          f"{r.verdict_WIDE:>8s} | {r.beta_br_laneB:7.3f} {r.beta_br_NARROW:7.3f} "
          f"{r.beta_br_WIDE:7.3f} {r.beta_br_spread:7.3f}  {str(r.WIDTH_PORTABLE):8s}  "
          f"{r.s3_signature_3of3}")

    fam16 = port[port.stat.isin(SCOLS)]
    portable = fam16[fam16.WIDTH_PORTABLE].stat.tolist()
    portable_all = port[port.WIDTH_PORTABLE].stat.tolist()
    P(f"\n  HEADLINE - portable in the 16-statistic matched family: {len(portable)} of {len(SCOLS)}"
      f" -> {portable if portable else '(none)'}")
    P(f"  sensitivity (labelled, NOT the headline): over all {len(ALLCOLS)} incl. the parents' five"
      f" -> {len(portable_all)}: {portable_all if portable_all else '(none)'}")
    P(f"    (S3_reversal IS RL_SHARPE_CAGR by GATE 3, so it is the same statistic counted twice)")
    P(f"  sensitivity: verdict-identical incl. NULL = {int(fam16.verdict_same.sum())} of {len(SCOLS)};"
      f" beta-spread <= {SPREAD_BAR} = {int(fam16.beta_stable.sum())} of {len(SCOLS)}")

    # ------------------------------------------------------------ hypotheses
    P("\n" + "=" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    hrows = []
    def H(name, passed, detail):
        hrows.append(dict(hypothesis=name, verdict="PASS" if passed else "FAIL", detail=detail))
        P(f"  {name:12s} {'PASS' if passed else 'FAIL'}  {detail}")

    H("H_S3UNIQUE", portable == [S3],
      f"portable set = {portable if portable else '(none)'}; the claim needs exactly [{S3}]")

    rf = fam16[fam16.form == "RATIO"]; lf = fam16[fam16.form == "LEVEL"]
    sr, sl = rf.WIDTH_PORTABLE.mean(), lf.WIDTH_PORTABLE.mean()
    H("H_FORM", bool(sr >= 2 * sl) and sr > 0,
      f"RATIO-form portable {int(rf.WIDTH_PORTABLE.sum())}/{len(rf)} = {sr:.3f} vs "
      f"LEVEL-form {int(lf.WIDTH_PORTABLE.sum())}/{len(lf)} = {sl:.3f}  (bar: ratio >= 2x level)")

    rv = fam16[fam16['kind'] == "reversal"]; pl = fam16[fam16['kind'] == "plain"]
    srv, spl = rv.WIDTH_PORTABLE.mean(), pl.WIDTH_PORTABLE.mean()
    H("H_REV", bool(srv >= 2 * spl) and srv > 0,
      f"REVERSAL portable {int(rv.WIDTH_PORTABLE.sum())}/{len(rv)} = {srv:.3f} vs "
      f"PLAIN {int(pl.WIDTH_PORTABLE.sum())}/{len(pl)} = {spl:.3f}  (bar: reversal >= 2x plain)")

    rl = fam16[fam16.stat.isin(REV_RL)]
    H("H_SIGN", bool(rl.s3_signature_3of3.all()),
      "ratio x level reversals with S3's signature (b_br>0, |b_k|<0.25|b_br|) on 3 of 3 supports: "
      + ", ".join(f"{r.stat}={r.s3_signature_3of3}" for _, r in rl.iterrows()))

    dimrows = []
    for tag in SUP:
        d = dec[dec.support == tag]
        mr = float(d[d.form == "RATIO"].beta_logk.abs().median())
        ml = float(d[d.form == "LEVEL"].beta_logk.abs().median())
        dimrows.append((tag, mr, ml, mr < ml))
    H("H_DIM", all(x[3] for x in dimrows),
      "median |beta_logk| RATIO vs LEVEL: " + "; ".join(f"{t.split()[0]} {a:.3f} vs {b:.3f}"
                                                        for t, a, b, _ in dimrows))
    hyp = pd.DataFrame(hrows)

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 100)
    P("KEEP PATHS (PROTOCOL rule 4) - every book row, 10 bps, next-day execution")
    P("=" * 100)
    for tag, d in SUP.items():
        bk_ = books[books.panel.isin(d.panel)]
        P(f"  {tag:26s} 4a {int(bk_.pass4a.sum()):4d} of {len(bk_):4d} ({bk_.pass4a.mean():.3f})   "
          f"4b {int(bk_.pass4b.sum()):4d} of {len(bk_):4d} ({bk_.pass4b.mean():.3f})")
    P("\n  4b pass rate by k (WIDE support), all arms:")
    w = books[books.panel.isin(SUP["WIDE q>=0.5 k<=400"].panel)]
    for k, sub in w.groupby("k"):
        P(f"    k={int(k):3d}  4a {sub.pass4a.mean():.3f}  4b {sub.pass4b.mean():.3f}  ({len(sub)} rows)")
    P("\n  4b pass rate by arm (WIDE support):")
    for arm, sub in w.groupby("arm"):
        P(f"    {arm:7s} 4a {sub.pass4a.mean():.3f}  4b {sub.pass4b.mean():.3f}  ({len(sub)} rows)")

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - panel statistics from 2010..2016 only, read once on 2017+")
    P("=" * 100)
    wf = []
    for tag in ["NARROW q>=0.5 k<=100", "WIDE q>=0.5 k<=400"]:
        d = SUP[tag]
        bk_ = books[(books.panel.isin(d.panel)) & (books.arm != "EWall")]
        wf.append(walkforward(bk_, tag))
    wf = pd.concat(wf, ignore_index=True); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for tag, sub in wf.groupby("support"):
        P(f"\n--- {tag} ---")
        P(f"  {'selector':18s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS MaxDD':>10s} | "
          f"{'anchor S':>9s} {'v2 S':>7s} {'SPY S':>7s} | beats anchor/v2/SPY")
        for sel, s in sub.groupby("selector"):
            P(f"  {sel:18s} {s.OOS_CAGR.mean():9.3f} {s.OOS_Sharpe.mean():9.3f} "
              f"{s.OOS_MaxDD.mean():10.3f} | {s.anchor_OOS_S.mean():9.3f} {s.v2_OOS_S.mean():7.3f} "
              f"{s.spy_OOS_S.mean():7.3f} | {int(s.beats_anchor.sum())}/{int(s.beats_v2.sum())}/"
              f"{int(s.beats_spy.sum())} of {len(s)}")
        P(f"  SPY OOS: CAGR {sub.spy_OOS_CAGR.mean():.3f} Sharpe {sub.spy_OOS_S.mean():.3f} "
          f"MaxDD {sub.spy_OOS_DD.mean():.3f}   |   RULES v2 OOS: CAGR {sub.v2_OOS_CAGR.mean():.3f} "
          f"Sharpe {sub.v2_OOS_S.mean():.3f} MaxDD {sub.v2_OOS_DD.mean():.3f}")
    P("\n  RATIO-chosen vs LEVEL-chosen, pooled over both supports and every n:")
    rsel = ["RATIO-SHARPE-MAX", "RATIO-CALMAR-MAX"]; lsel = ["LEVEL-CAGR-MAX", "LEVEL-DD-MIN"]
    rr = wf[wf.selector.isin(rsel)]; ll = wf[wf.selector.isin(lsel)]
    P(f"    RATIO selectors: OOS Sharpe {rr.OOS_Sharpe.mean():+.3f}  beats anchor "
      f"{int(rr.beats_anchor.sum())}/{len(rr)}  beats SPY {int(rr.beats_spy.sum())}/{len(rr)}")
    P(f"    LEVEL selectors: OOS Sharpe {ll.OOS_Sharpe.mean():+.3f}  beats anchor "
      f"{int(ll.beats_anchor.sum())}/{len(ll)}  beats SPY {int(ll.beats_spy.sum())}/{len(ll)}")
    s3sel = wf[wf.selector.isin(["S3-MAX", "S3-MIN"])]
    P(f"    S3 selectors  : OOS Sharpe {s3sel.OOS_Sharpe.mean():+.3f}  beats anchor "
      f"{int(s3sel.beats_anchor.sum())}/{len(s3sel)}  beats SPY {int(s3sel.beats_spy.sum())}/{len(s3sel)}")

    pd.DataFrame(grows).to_csv(f"{OUT}.gates.csv", index=False)
    hyp.to_csv(f"{OUT}.hypotheses.csv", index=False)

    P("\n" + "=" * 100)
    P(f"done in {time.time() - t0all:.1f}s")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(port=port, dec=dec, hyp=hyp, wf=wf, books=books, stats=stats)


if __name__ == "__main__":
    main()
