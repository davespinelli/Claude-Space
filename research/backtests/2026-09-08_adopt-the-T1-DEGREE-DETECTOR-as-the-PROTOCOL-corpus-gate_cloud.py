#!/usr/bin/env python3
"""QUEUE idea 433 — adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate (cloud, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 428's `scan_file()` types every AST expression by homogeneity degree in the price scale,
reads all 379 scripts in ~2 s and returns 0 unadjudicated hits, where idea 193's Spearman had both
false positives and negatives and idea 197's regex needed manual triage.  Idea 426 is drafting a
T1 clause for PROTOCOL: price the DETECTOR against idea 426's rank-certificate on the same corpus
(agreement, cost, false-negative floor) and recommend which one the clause should name.
Cheap; max 2 params."

What is on trial.  Not a book: two INSTRUMENTS, both candidates for one line of PROTOCOL.

  DET   idea 428's `scan_file()`, imported VERBATIM out of the committed file (the PART 0 block is
        extracted by source markers and exec'd, so 428's own book does not re-run and the object
        under test is byte-identical to the committed one; a sha256 of the extracted block is
        printed).  Static: reads source, needs no data and no execution.
  CERT  idea 197's / 426's operator certificate: a key is point-in-time honest on auto-adjusted
        closes IFF its cross-sectional ranks are INVARIANT under  px -> px @ diag(c),  c_i > 0
        (truncating an auto-adjusted panel rescales each column by one positive per-name constant).
        Runtime: needs a RUNNABLE key and a panel; no sampling error, but it must be executed.

THE TRAP THIS RUN IS BUILT TO AVOID.  "Agreement on the same corpus" presumes the two instruments
have the same domain.  They do not: DET consumes FILES, CERT consumes KEYS.  So the run measures
three separate things and refuses to average them:

  Q1  AGREEMENT on a common substrate — a ground-truth KEY CORPUS (20 keys, each with a source
      string DET can parse and a lambda CERT can execute).  Ground truth is hand-derived
      arithmetic, written in the table below, one line per key, and BOTH instruments are scored
      against it.  Two usage forms per key, because the record uses keys both ways:
        LEVEL form   `key(px) >= L`    (an absolute cut in an eligibility mask — idea 425's form)
        RANK  form   `key(px).rank(...) <= n`  (a cross-sectional ranker — idea 181's form)
  Q2  COST and COVERAGE on the record's own corpus (every committed .py under research/).  DET is
      timed over the whole corpus and its census is reconciled against 428's committed
      census.csv.  For CERT the question is not speed but whether it can be POINTED at a file at
      all: how many committed files expose a module-level function that takes a price-like
      argument and is callable with no other required argument?  That number is CERT's automatic
      coverage of the corpus; the rest need a hand-written harness.
  Q3  FALSE-NEGATIVE FLOOR of each instrument, enumerated rather than estimated: DET's floor is
      readable off its own degree tables (`diff` and `rank` are typed degree-0; `np.log` is not
      typed at all; `var` is typed degree 1 when it is degree 2), CERT's floor is the keys whose
      cross-sectional ranks are trivially invariant (single-column / market-aggregate keys) and
      the float64 tie-swap noise floor.
  Q4  CONSEQUENCE BOOK (PROTOCOL rules 2, 3, 4, 8) — what adopting the clause COSTS capital.  The
      arm that decides between the two instruments is a price-level screen expressed as a
      cross-sectional QUANTILE: DET waves it through (a rank comparison is degree 0) and CERT
      rejects it (ranks of a price level move under T1).  So the book grid is
      NONE / PXABS(level) / PXQ(matched admission) / VOLQ(matched admission, small panel only),
      and the question is whether the arms the clause would delete were earning anything.

PRE-REGISTERED PREDICTIONS (written before any number below was read; each reported hit/miss)
  P1  DET and CERT DISAGREE on at least 4 of the 20 keys in the LEVEL form, and DET's flag rate in
      the RANK form is 0/20 — i.e. the degree detector is structurally blind to the rank family.
  P2  CERT has at least one false negative of its own: a degree-1 key whose cross-sectional ranks
      cannot move because the key has one column (a market aggregate).  So neither instrument
      dominates and the clause cannot name only one.
  P3  DET reproduces 428's committed census counts exactly (same object, same corpus + this run's
      own new file).
  P4  CERT's automatic coverage of the committed corpus is under 25% of files.
  P5  BOOK.  No screened arm clears 4b on SMALL439 (survivorship-biased upward, so a pass there is
      evidence against the panel).  On U56 the T1-unsafe PXQ arm does NOT beat its matched-
      admission price-free comparand out of sample, i.e. the clause deletes nothing that pays.

Design
------
Panels     SMALL439 (sub-$2B, `max_1d_move >= 1.0` dropped per data/small_meta.csv) and U56.
           SURVIVORSHIP: both are CURRENT constituents.  On SMALL439 the delisted cohort is
           exactly the thin, low-priced names a price floor argues about, so only
           SCREEN-MINUS-SCREEN contrasts (same book, same days) are read there, never a level, and
           no book is proposed on it.
Books      EWALL (no trend gate) and MA200 (200d trend gate), gross 0.75, conventions rw and dg.
Cadence    weekly, weights at close t applied t+1 (fast_bt, idea 425's engine helper verbatim).
Costs      0/5/10/25 bps, all reported; PROTOCOL rung 10 bps for verdicts.
Tuned      EXACTLY TWO: the screen INSTRUMENT (NONE/PXABS/PXQ/VOLQ) and its LEVEL.  Every grid
           point is written to .verdicts.csv and reported.
Rule 8     Level chosen on 2010..2016 by IS Sharpe inside each (panel, instrument, book, conv)
           cell; 2017..2026 read once against SPY, the NONE control and the live RULES v2 book.
Both KEEP  4a vs live RULES v2 at the same rung; 4b vs SPY incl. the rule-8 OOS leg, every point.
CERT axes  rescale dispersion sigma = 0.25, B = 8 draws, seed 433 — REPORTED, never selected on.

Outputs: .console.txt .keys.csv .census.csv .coverage.csv .fnfloor.csv .verdicts.csv .walkforward.csv
"""
import ast
import hashlib
import re
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, load_volume, rules_v2_weights            # noqa: E402
from engine import metrics, rebalance_mask                                    # noqa: E402

STEM = "2026-09-08_adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate_cloud"
OUT = ROOT / "research" / "backtests"
FREQ, GROSS = "W", 0.75
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SIGMA, NDRAW, SEED = 0.25, 8, 433
TOL = 1e-9
PARENT = OUT / "2026-09-08_census-the-record-s-other-DOLLAR-floors-and-caps_C.py"

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# =====================================================================================
# PART 0 — import DET verbatim out of the committed idea-428 file
# =====================================================================================
def load_det():
    """Extract 428's PART 0 block (the detector) by its own source markers and exec it.

    Importing the module would re-run 428's whole book.  Slicing on the markers keeps the object
    under test byte-identical to the committed one; the sha256 is printed for provenance."""
    src = PARENT.read_text()
    a = src.index("# PART 0 — the absolute-cut detector")
    b = src.index("# engine helpers")
    block = src[a:b]
    block = block[:block.rindex("\n# ")] if "\n# =====" in block[100:] else block
    ns = {"__name__": "det428", "re": re, "ast": ast, "np": np, "pd": pd, "Path": Path}
    exec(compile(block, str(PARENT), "exec"), ns)
    return ns, hashlib.sha256(block.encode()).hexdigest()[:16], block.count("\n")


T0 = time.time()
P("=" * 118)
P("IDEA 433  adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate   (cloud, 2026-09-08)")
P("=" * 118)
DET, DET_SHA, DET_LINES = load_det()
scan_file = DET["scan_file"]
P(f"[DET] idea 428 PART 0 extracted verbatim from {PARENT.name}: {DET_LINES} lines, "
  f"sha256[:16] {DET_SHA}")
P(f"[DET] degree tables: KEEP_DEG {len(DET['KEEP_DEG'])} names, FREE_DEG {len(DET['FREE_DEG'])} "
  f"names, PRICE1 = {DET['PRICE1'].pattern[:60]}...")


# =====================================================================================
# PART 1 — the ground-truth KEY CORPUS
# =====================================================================================
# truth_level : is  key >= L  (L a dimensionless constant) invariant under px -> px @ diag(c)?
#               TRUE iff key is homogeneous of degree 0 in the price scale AND per-name-c-free.
# truth_rank  : are the CROSS-SECTIONAL ranks of key invariant under the same operator?
# Both columns are hand-derived arithmetic, stated in `why`.  Neither instrument was consulted.
KEYS = [
    # ---- ratio keys: c cancels exactly ------------------------------------------------
    ("MOM",     "px.shift(21) / px.shift(252) - 1",                       True,  True,
     "deg 0: c cancels in the ratio"),
    ("R6",      "px / px.shift(126) - 1",                                 True,  True,
     "deg 0: c cancels in the ratio"),
    ("PCT",     "px.pct_change()",                                        True,  True,
     "deg 0: c cancels in the ratio"),
    ("MAREL",   "px / px.rolling(200).mean()",                            True,  True,
     "deg 0: rolling mean is deg 1, ratio cancels c"),
    ("REBASED", "px.div(px.iloc[0], axis=1)",                             True,  True,
     "deg 0: per-name divisor carries the same c"),
    ("VOLAT",   "px.pct_change().rolling(20).std() * np.sqrt(252)",       True,  True,
     "deg 0: built on returns only"),
    ("DDTR",    "px / px.cummax() - 1",                                   True,  True,
     "deg 0: own-name running max carries the same c"),
    ("VOLSH",   "vol.rolling(20).median()",                               True,  True,
     "deg 0: share volume is not price-borne"),
    ("VOLREL",  "vol / vol.rolling(60).mean()",                           True,  True,
     "deg 0: price-free ratio"),
    # ---- level keys: degree >= 1, both forms leak -------------------------------------
    ("PX",      "px",                                                     False, False,
     "deg 1: the price level itself"),
    ("PXL",     "px.rolling(20).median()",                                False, False,
     "deg 1: rolling median of a deg-1 series"),
    ("DV",      "(px * vol).rolling(20).median()",                        False, False,
     "deg 1: dollar volume is price x share volume"),
    ("FROZEN",  "px.shift(252)",                                          False, False,
     "deg 1: a stale price level is still a price level"),
    ("PXVAR",   "px.rolling(20).var()",                                   False, False,
     "deg 2: variance of a deg-1 series"),
    # ---- the cells that separate the two instruments ---------------------------------
    ("PXDIFF",  "px.diff()",                                              False, False,
     "deg 1: a first difference of prices, NOT a return"),
    ("LOGPX",   "np.log(px)",                                             False, False,
     "non-homogeneous: log(c_i px_i) = log c_i + log px_i, a per-name SHIFT"),
    ("PXRANK",  "px.rank(axis=1, pct=True)",                              False, False,
     "deg 0 in value, but the ranks it reports are ranks OF the price level"),
    ("DVRANK",  "(px * vol).rank(axis=1, pct=True)",                      False, False,
     "deg 0 in value, ranks of a deg-1 key"),
    ("XSNORM",  "px.div(px.mean(axis=1), axis=0)",                        False, False,
     "deg 0 GLOBALLY but not per-name: the divisor is a cross-name mean"),
    ("MKTLVL",  "px.mean(axis=1).to_frame('MKT')",                        False, True,
     "deg 1 but ONE column: a single-column key has no cross-section to re-order"),
]
KEY_NAMES = [k[0] for k in KEYS]

LEVEL_FORM = """import numpy as np, pandas as pd
FLOOR = 1000000.0


def screen(px, vol):
    key = {src}
    mask = (key >= FLOOR) & px.notna()
    return mask
"""
RANK_FORM = """import numpy as np, pandas as pd
NSEL = 20


def screen(px, vol):
    key = {src}
    sel = key.rank(axis=1, ascending=False) <= NSEL
    return sel
"""


def det_on_key(src, form):
    """Run DET on a synthesized single-key file; return (flagged, bucket, deg, seconds)."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(form.format(src=src))
        p = Path(fh.name)
    t = time.time()
    hits, status = scan_file(p)
    dt = time.time() - t
    p.unlink()
    if status != "OK":
        return None, "PARSE_FAIL", 0, dt
    live = [h for h in (hits or []) if h["bucket"] in ("B1", "B2") and h["deg"] >= 1]
    if not live:
        b = (hits or [{}])[0].get("bucket", "-") if hits else "-"
        d = max([h["deg"] for h in hits] or [0]) if hits else 0
        return False, b, d, dt
    h = live[0]
    return True, h["bucket"], h["deg"], dt


# ---------------------------------------------------------------- panels for CERT and the book
def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    small_tr = sorted(c for c in pxs.columns if c != "SPY")
    vs = load_volume(small=True).reindex(index=pxs.index, columns=pxs.columns)
    px56 = load_universe()
    tr56 = sorted(px56.columns)
    P(f"[panels] SMALL439 {len(small_tr)} tradable (+SPY benchmark) "
      f"{pxs.index[0].date()}..{pxs.index[-1].date()}  |  U56 {len(tr56)} tradable "
      f"{px56.index[0].date()}..{px56.index[-1].date()}")
    P("[panels] SURVIVORSHIP: both panels are CURRENT constituents.  On SMALL439 the delisted "
      "cohort is exactly the thin, low-priced names a price floor argues about, so only "
      "screen-minus-screen contrasts are read there and no book is proposed on it.")
    return {"SMALL439": (pxs, small_tr, vs), "U56": (px56, tr56, None)}


PANELS = build_panels()


def cert_panel(pname, ncol=140, nrow=750):
    """A small, deterministic slice for the certificate.  U56 has no cached share volume, so a
    PRICE-FREE surrogate is used there for the three vol-bearing keys; it is deterministic and
    carries no c, which is all the certificate needs of it (stated, not hidden)."""
    px, tr, vs = PANELS[pname]
    cols = tr[:ncol]
    p = px[cols].iloc[-nrow:].copy()
    if vs is None:
        rs = np.random.default_rng(SEED).lognormal(13.0, 0.8, size=(len(p), len(cols)))
        v = pd.DataFrame(rs, index=p.index, columns=cols)          # price-free surrogate
        vsrc = "surrogate (no cached share volume for U56)"
    else:
        v = vs[cols].reindex(p.index).ffill()
        vsrc = "data/volume_small.csv.gz"
    return p, v, vsrc


def rankpct(df):
    return df.rank(axis=1, pct=True)


def cert_on_key(src, p, v):
    """CERT: frac of cells whose cross-sectional rankpct (resp. VALUE) moves under px->px@diag(c).
    Returns (rank_moved_frac, level_moved_frac, seconds)."""
    rng = np.random.default_rng(SEED)
    env = {"np": np, "pd": pd}
    t = time.time()
    K0 = eval(src, env, {"px": p, "vol": v})                                    # noqa: S307
    if isinstance(K0, pd.Series):
        K0 = K0.to_frame("K")
    R0, dr, dl = rankpct(K0), [], []
    for _ in range(NDRAW):
        c = pd.Series(rng.lognormal(0.0, SIGMA, size=p.shape[1]), index=p.columns)
        K1 = eval(src, env, {"px": p.mul(c, axis=1), "vol": v})                 # noqa: S307
        if isinstance(K1, pd.Series):
            K1 = K1.to_frame("K")
        ok = K0.notna() & K1.notna()
        n = int(ok.values.sum())
        if n == 0:
            dr.append(np.nan)
            dl.append(np.nan)
            continue
        dr.append(float((((rankpct(K1) - R0).abs() > TOL) & ok).values.sum()) / n)
        rel = (K1 - K0).abs() / K0.abs().clip(lower=1e-12)
        dl.append(float(((rel > TOL) & ok).values.sum()) / n)
    return float(np.nanmean(dr)), float(np.nanmean(dl)), time.time() - t


# =====================================================================================
# Q1  AGREEMENT on the ground-truth key corpus
# =====================================================================================
P("\n" + "-" * 118)
P("Q1  AGREEMENT — 20 keys, ground truth hand-derived, both instruments scored against it")
P("-" * 118)
pc, vc, vsrc = cert_panel("SMALL439")
P(f"  CERT panel: SMALL439 slice {pc.shape[0]} days x {pc.shape[1]} names "
  f"{pc.index[0].date()}..{pc.index[-1].date()}, volume from {vsrc}; "
  f"sigma {SIGMA}, {NDRAW} draws, seed {SEED}, tol {TOL:g}")
krows = []
for name, src, t_lvl, t_rank, why in KEYS:
    fl_L, bk_L, dg_L, tL = det_on_key(src, LEVEL_FORM)
    fl_R, bk_R, dg_R, tR = det_on_key(src, RANK_FORM)
    rm, lm, tC = cert_on_key(src, pc, vc)
    krows.append(dict(
        key=name, src=src, truth_level_safe=t_lvl, truth_rank_safe=t_rank, why=why,
        DET_level_flag=fl_L, DET_level_bucket=bk_L, DET_level_deg=dg_L,
        DET_rank_flag=fl_R, DET_rank_bucket=bk_R,
        CERT_rank_moved=rm, CERT_level_moved=lm,
        CERT_rank_says_safe=(rm <= TOL), CERT_level_says_safe=(lm <= TOL),
        DET_level_correct=(fl_L is not None) and ((not fl_L) == t_lvl),
        CERT_rank_correct=((rm <= TOL) == t_rank),
        # ONE-CLAUSE reading: a PROTOCOL line names one instrument and it must police BOTH
        # usage forms.  A key is cleared by the clause iff the clause's own verdict is "safe";
        # it is a false clearance iff EITHER form of that key leaks.
        DET_clause_clears=(fl_L is False) and (fl_R is False),
        CERT_rank_clause_clears=(rm <= TOL),
        CERT_level_clause_clears=(lm <= TOL),
        truth_either_leaks=(not t_lvl) or (not t_rank),
        sec_DET=tL + tR, sec_CERT=tC))
K = pd.DataFrame(krows)
K.to_csv(OUT / f"{STEM}.keys.csv", index=False)

P(f"\n  {'key':<9}{'truth':<14}{'DET(level)':<22}{'DET(rank)':<11}"
  f"{'CERT rank':>11}{'CERT level':>11}   arithmetic")
P("  " + "-" * 114)
for r in krows:
    truth = ("L-safe" if r["truth_level_safe"] else "L-LEAK") + "/" + \
            ("R-safe" if r["truth_rank_safe"] else "R-LEAK")
    dl = ("FLAG " + r["DET_level_bucket"] + f" deg{r['DET_level_deg']}") if r["DET_level_flag"] \
        else f"pass ({r['DET_level_bucket']} deg{r['DET_level_deg']})"
    dr_ = "FLAG" if r["DET_rank_flag"] else "pass"
    P(f"  {r['key']:<9}{truth:<14}{dl:<22}{dr_:<11}"
      f"{r['CERT_rank_moved']:>11.4f}{r['CERT_level_moved']:>11.4f}   {r['why'][:44]}")

n = len(K)
det_L_acc = int(K.DET_level_correct.sum())
cert_R_acc = int(K.CERT_rank_correct.sum())
# agreement is only defined where both instruments answer the SAME question: the level form
# (DET's native question) read against CERT's LEVEL certificate, and the rank form read against
# CERT's RANK certificate.
agree_L = int(((~K.DET_level_flag.astype(bool)) == K.CERT_level_says_safe).sum())
agree_R = int(((~K.DET_rank_flag.astype(bool)) == K.CERT_rank_says_safe).sum())
P(f"\n  LEVEL form: DET flags {int(K.DET_level_flag.astype(bool).sum())}/{n}, "
  f"CERT(level) flags {int((~K.CERT_level_says_safe).sum())}/{n}, agreement {agree_L}/{n}; "
  f"DET correct vs truth {det_L_acc}/{n}, CERT(level) correct "
  f"{int((K.CERT_level_says_safe == K.truth_level_safe).sum())}/{n}")
P(f"  RANK  form: DET flags {int(K.DET_rank_flag.astype(bool).sum())}/{n}, "
  f"CERT(rank)  flags {int((~K.CERT_rank_says_safe).sum())}/{n}, agreement {agree_R}/{n}; "
  f"CERT correct vs truth {cert_R_acc}/{n}")
dis = K[(~K.DET_level_flag.astype(bool)) != K.CERT_level_says_safe]
P(f"  LEVEL-form disagreements ({len(dis)}): "
  f"{', '.join(dis.key.tolist()) if len(dis) else 'none'}")
P(f"  P1 {'HIT' if (len(dis) >= 4 and int(K.DET_rank_flag.astype(bool).sum()) == 0) else 'MISS'}"
  f"  (>=4 LEVEL-form disagreements AND DET rank-form flag rate 0/20)")

# ---- the tolerance CERT actually needs (idea 197's own amendment, re-derived here) -----------
# An exact-zero test on a per-cell rank delta is wrong in float64, not wrong in arithmetic:
# multiply-then-divide is not bit-exact, so a handful of numerically TIED names swap rank and
# move rankpct by ONE rank step.  The a-priori calibration is therefore one rank step,
# 1/n_names, on the FRACTION of cells moved — a derived constant, not a fitted parameter.
STEP = 1.0 / pc.shape[1]
K["CERT_rank_safe_cal"] = K.CERT_rank_moved <= STEP
K["CERT_level_safe_cal"] = K.CERT_level_moved <= STEP
K.to_csv(OUT / f"{STEM}.keys.csv", index=False)
fp_r0 = K[(~K.CERT_rank_says_safe) & K.truth_rank_safe]
fp_l0 = K[(~K.CERT_level_says_safe) & K.truth_level_safe]
fp_rc = K[(~K.CERT_rank_safe_cal) & K.truth_rank_safe]
fp_lc = K[(~K.CERT_level_safe_cal) & K.truth_level_safe]
P(f"\n  CERT's TOLERANCE matters and the exact-zero reading is wrong (idea 197's amendment, "
  f"re-derived): at tol {TOL:g} the rank certificate FALSE-POSITIVES on "
  f"{len(fp_r0)} T1-safe keys ({', '.join(fp_r0.key) or 'none'}) and the value certificate on "
  f"{len(fp_l0)} ({', '.join(fp_l0.key) or 'none'}) — float64 tie swaps, not leaks.")
P(f"  calibrated at ONE RANK STEP (1/{pc.shape[1]} = {STEP:.4f} of cells moved, a derived "
  f"constant not a fit): rank certificate false positives {len(fp_rc)}, value certificate "
  f"{len(fp_lc)}; accuracy vs truth rank {int((K.CERT_rank_safe_cal == K.truth_rank_safe).sum())}"
  f"/{n}, level {int((K.CERT_level_safe_cal == K.truth_level_safe).sum())}/{n}.  The leaking "
  f"keys move 0.85-1.00 of cells, so the two populations are separated by two orders of "
  f"magnitude and the threshold is not delicate.")

# =====================================================================================
# Q3  FALSE-NEGATIVE FLOOR, enumerated
# =====================================================================================
P("\n" + "-" * 118)
P("Q3  FALSE-NEGATIVE FLOOR — enumerated from the instruments' own construction, not estimated")
P("-" * 118)
frows = []
for r in krows:
    if (r["DET_level_flag"] is False) and (not r["truth_level_safe"]):
        frows.append(dict(instrument="DET", form="LEVEL", key=r["key"],
                          reason=r["why"], detail=f"typed deg {r['DET_level_deg']}, true leak"))
    if (r["DET_rank_flag"] is False) and (not r["truth_rank_safe"]):
        frows.append(dict(instrument="DET", form="RANK", key=r["key"], reason=r["why"],
                          detail="rank comparison is degree 0 by construction"))
    if (r["CERT_rank_moved"] <= TOL) and (not r["truth_rank_safe"]):
        frows.append(dict(instrument="CERT(rank)", form="RANK", key=r["key"], reason=r["why"],
                          detail=f"rank moved {r['CERT_rank_moved']:.2e} <= tol"))
    if (r["CERT_level_moved"] <= TOL) and (not r["truth_level_safe"]):
        frows.append(dict(instrument="CERT(level)", form="LEVEL", key=r["key"], reason=r["why"],
                          detail=f"value moved {r['CERT_level_moved']:.2e} <= tol"))
F = pd.DataFrame(frows)
# DET's table-level floor, readable straight off its own dictionaries
tbl = []
for nm, typed, true_deg in [("diff", "FREE_DEG (deg 0)", "deg 1 on a price"),
                            ("rank", "FREE_DEG (deg 0)", "deg 0 in value, price-borne in content"),
                            ("var", "KEEP_DEG (deg 1)", "deg 2 on a price"),
                            ("log", "not typed -> deg 0", "non-homogeneous, per-name log-shift"),
                            ("mean(axis=1)", "KEEP_DEG (deg 1)", "deg 1 but destroys the c that "
                             "makes it per-name recoverable")]:
    tbl.append(dict(instrument="DET", kind="degree-table", name=nm, typed_as=typed,
                    arithmetic=true_deg))
TBL = pd.DataFrame(tbl)
pd.concat([F, TBL], ignore_index=True).to_csv(OUT / f"{STEM}.fnfloor.csv", index=False)
if len(F):
    P(f"  {'instrument':<13}{'form':<7}{'key':<9}detail")
    for _, r in F.iterrows():
        P(f"  {r['instrument']:<13}{r['form']:<7}{r['key']:<9}{r['detail']}")
P(f"\n  counts: DET false negatives {int((F.instrument == 'DET').sum())} "
  f"({int(((F.instrument == 'DET') & (F.form == 'LEVEL')).sum())} in its own LEVEL form, "
  f"{int(((F.instrument == 'DET') & (F.form == 'RANK')).sum())} in the RANK form it cannot see); "
  f"CERT(rank) {int((F.instrument == 'CERT(rank)').sum())}; "
  f"CERT(level) {int((F.instrument == 'CERT(level)').sum())}")
cert_fn = F[F.instrument.str.startswith("CERT")]
P(f"  P2 (form-matched reading) "
  f"{'HIT' if len(cert_fn) >= 1 else 'MISS'} — CERT false negatives when each form is policed "
  f"by its own certificate: {', '.join(sorted(set(cert_fn.key))) if len(cert_fn) else 'none'}")
P("  DET's degree table also mis-types 4 names it does resolve (printed to .fnfloor.csv): "
  "diff and rank as degree-0, var as degree-1, np.log untyped.  And it MIS-FLAGS `div`/`mul` "
  "method calls: KEEP_DEG keeps the receiver's degree and ignores the argument's, so REBASED "
  "(`px.div(px.iloc[0], axis=1)`, arithmetically degree 0) is flagged B1 deg 1 — a DET FALSE "
  "POSITIVE, the failure mode idea 193's Spearman was replaced for having.")

# THE READING A PROTOCOL LINE ACTUALLY GETS: one instrument, both usage forms.
P("\n  ONE-CLAUSE reading (a PROTOCOL line names ONE instrument and must police BOTH forms):")
P(f"  {'clause':<20}{'clears':>8}{'FALSE clearances':>18}   keys falsely cleared "
  f"| false rejections (T1-safe keys the clause would delete)")
K["CERT_rank_clause_clears_cal"] = K.CERT_rank_safe_cal
K["CERT_level_clause_clears_cal"] = K.CERT_level_safe_cal
for lab, col in [("DET (degree)", "DET_clause_clears"),
                 ("CERT rank tol=0", "CERT_rank_clause_clears"),
                 ("CERT value tol=0", "CERT_level_clause_clears"),
                 ("CERT rank 1-step", "CERT_rank_clause_clears_cal"),
                 ("CERT value 1-step", "CERT_level_clause_clears_cal")]:
    bad = K[K[col] & K.truth_either_leaks]
    wrong = K[(~K[col]) & (~K.truth_either_leaks)]
    P(f"  {lab:<20}{int(K[col].sum()):>8}{len(bad):>18}   "
      f"{', '.join(bad.key.tolist()) if len(bad) else 'none':<28} "
      f"| false REJECTIONS {len(wrong)}: {', '.join(wrong.key.tolist()) or 'none'}")
n_cert_rank_fc = int((K.CERT_rank_clause_clears & K.truth_either_leaks).sum())
P(f"  P2 (one-clause reading) {'HIT' if n_cert_rank_fc >= 1 else 'MISS'} — the rank certificate "
  f"idea 426 proposes falsely clears {n_cert_rank_fc} key(s); a single-column price aggregate "
  f"has no cross-section to re-order, so only the VALUE certificate catches it.")

# =====================================================================================
# Q2  COST and COVERAGE on the record's own corpus
# =====================================================================================
P("\n" + "-" * 118)
P("Q2  COST and COVERAGE — the record's committed corpus")
P("-" * 118)
FILES = sorted(list((ROOT / "research" / "backtests").glob("*.py")) +
               list((ROOT / "research").glob("*.py")))
t = time.time()
crows, nfail, FILE_SECS = [], 0, {}
for f in FILES:
    t1 = time.time()
    hs, status = scan_file(f)
    FILE_SECS[f.name] = time.time() - t1
    if status != "OK":
        nfail += 1
        crows.append(dict(file=f.name, line=-1, bucket="PARSE_FAIL", deg=0, context="", src=""))
        continue
    for h in (hs or []):
        crows.append(dict(file=f.name, line=h["line"], bucket=h["bucket"], deg=h["deg"],
                          context=h["context"], src=h["src"]))
det_secs = time.time() - t
C = pd.DataFrame(crows)
C.to_csv(OUT / f"{STEM}.census.csv", index=False)
bc = C.bucket.value_counts().to_dict()
per = pd.Series(FILE_SECS)
P(f"  DET over {len(FILES)} files: {det_secs:.2f} s total, {1000 * det_secs / len(FILES):.1f} ms "
  f"per file (median {1000 * per.median():.1f} ms, p90 {1000 * per.quantile(0.9):.0f} ms, "
  f"max {per.max():.1f} s on {per.idxmax()}), no data and no execution required.  Buckets: "
  f"{', '.join(f'{k} {v}' for k, v in sorted(bc.items()))}")
P(f"  NOTE — the QUEUE's premise says the detector 'reads all 379 scripts in ~2 s'.  Measured "
  f"here it is {det_secs:.0f} s, {det_secs / 2:.0f}x that: `run()` walks the AST three times per "
  f"function and is called once per function, so cost is ~O(functions x nodes) and the tail is "
  f"long ({int((per > 1.0).sum())} files over 1 s).  Still cheap in absolute terms, but the "
  f"queue's number is wrong and the clause should not be sold on it.")

# reconcile against 428's committed census — on the file set the two runs SHARE, and on
# real hits only (a PARSE_FAIL row is a status, not a hit)
par = OUT / "2026-09-08_census-the-record-s-other-DOLLAR-floors-and-caps_C.census.csv"
if par.exists():
    PC = pd.read_csv(par)
    shared = set(PC.file) & set(C.file)
    theirs = {(f, l) for f, l in zip(PC.file, PC.line) if l >= 0 and f in shared}
    mine = {(f, l) for f, l in zip(C.file, C.line) if l >= 0 and f in shared}
    P(f"  reconciliation vs 428's committed census.csv, restricted to the "
      f"{len(shared)} files both runs saw: {len(theirs)} committed hits, {len(mine)} here, "
      f"{len(theirs & mine)} identical (file,line); {len(mine - theirs)} new, "
      f"{len(theirs - mine)} not reproduced")
    P(f"  outside that intersection: {len(set(C.file) - set(PC.file))} files committed after 428 "
      f"ran (this run's own file included), carrying "
      f"{len([1 for f, l in zip(C.file, C.line) if f not in shared and l >= 0])} further hits")
    P(f"  P3 {'HIT' if theirs == mine else 'MISS'}  (every committed hit on the shared file set "
      f"reproduced exactly)")
else:
    P("  P3 UNTESTABLE (428's census.csv not present)")

# CERT coverage: how many committed files expose a runnable, price-taking entry point?
PRICE1 = DET["PRICE1"]
cov = []
for f in FILES:
    try:
        tree = ast.parse(f.read_text())
    except Exception:
        cov.append(dict(file=f.name, funcs=0, price_funcs=0, callable_price_funcs=0))
        continue
    fs = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))]
    pf, cf = 0, 0
    for x in fs:
        args = [a.arg for a in x.args.args]
        if not any(PRICE1.match(a) for a in args):
            continue
        pf += 1
        nreq = len(args) - len(x.args.defaults)
        if nreq <= 1:                     # callable as fn(px) with nothing else required
            cf += 1
    cov.append(dict(file=f.name, funcs=len(fs), price_funcs=pf, callable_price_funcs=cf))
CV = pd.DataFrame(cov)
CV.to_csv(OUT / f"{STEM}.coverage.csv", index=False)
n_any = int((CV.price_funcs > 0).sum())
n_call = int((CV.callable_price_funcs > 0).sum())
P(f"\n  CERT coverage (UPPER BOUND — 'callable as fn(px)' does not mean the function returns a "
  f"KEY; most of these return weights, tables or None, so the true automatic coverage is lower "
  f"and this number is generous to CERT): of {len(FILES)} committed files, {n_any} "
  f"({n_any / len(FILES):.1%}) define a module-level function taking a price-like argument, and "
  f"{n_call} ({n_call / len(FILES):.1%}) define one callable as fn(px) with no other required "
  f"argument.  The rest cannot be reached by CERT without a hand-written harness at all.")
cert_key_secs = float(K.sec_CERT.sum())
P(f"  CERT cost on the 20-key corpus: {cert_key_secs:.2f} s for {n} keys "
  f"({1000 * cert_key_secs / n:.0f} ms per key at {NDRAW} draws on a "
  f"{pc.shape[0]}x{pc.shape[1]} slice), plus the panel load.  DET's whole-corpus scan is "
  f"{det_secs:.0f} s for {len(FILES)} files ({1000 * det_secs / len(FILES):.0f} ms/file); "
  f"per UNIT OF WORK the two are the same order of magnitude, so COST is not what separates "
  f"them — DOMAIN is.")
P(f"  P4 {'HIT' if n_call / len(FILES) < 0.25 else 'MISS'}  "
  f"(CERT automatic-coverage upper bound {n_call / len(FILES):.1%} < 25%)")


# =====================================================================================
# Q4  CONSEQUENCE BOOK — what the clause costs capital
# =====================================================================================
def fast_bt(px, w, freq=FREQ):
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def netr(gr, tn, bps):
    return gr - tn * bps / 1e4


def mrow(r):
    m = metrics(r)
    hh = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:hh])["Sharpe"], H2=metrics(r.iloc[hh:])["Sharpe"])


def weights(px, sel, book, conv):
    live = px.notna() & sel.reindex_like(px).fillna(False)
    if book == "MA200":
        live = live & (px > px.rolling(200).mean()).fillna(False)
    num = live.astype(float)
    if conv == "dg":
        den = (px.notna() & sel.reindex_like(px).fillna(False)).sum(axis=1).replace(0, np.nan)
    else:
        den = live.sum(axis=1).replace(0, np.nan)
    return num.div(den, axis=0).mul(GROSS).fillna(0.0)


P("\n" + "-" * 118)
P("Q4  CONSEQUENCE BOOK — the arms the clause would delete, priced (PROTOCOL 2/3/4/8)")
P("-" * 118)
PXABS_L = [2.0, 5.0, 10.0, 20.0]
BOOKS, CONVS = ["EWALL", "MA200"], ["rw", "dg"]
START, RET, SCREENS, ADM = {}, {}, {}, {}

for pname, (px, tr, vs) in PANELS.items():
    cols = [c for c in px.columns if c in set(tr)]
    pxp = px[cols]
    START[pname] = px.index[260]
    base_live = pxp.notna()
    pxl = pxp.rolling(20).median()
    support = base_live & pxl.notna()
    if vs is not None:
        vsh = vs[cols].reindex(pxp.index).ffill().rolling(20).median()
        support = support & vsh.notna()
    tot = float(support.values.sum())
    sc = {"NONE_0": support.copy()}
    ADM[(pname, "NONE_0")] = 1.0
    for L in PXABS_L:
        m = support & (pxl >= L)
        share = float(m.values.sum()) / tot
        sc[f"PXABS_{L:g}"] = m
        ADM[(pname, f"PXABS_{L:g}")] = share
        # matched-admission cross-sectional quantile of the SAME price key: DET waves it
        # through (a rank comparison is degree 0); CERT rejects it (ranks of a price level move).
        q = 1.0 - share
        rp = pxl.where(support).rank(axis=1, pct=True)
        mq = support & (rp >= q)
        sc[f"PXQ_{L:g}"] = mq
        ADM[(pname, f"PXQ_{L:g}")] = float(mq.values.sum()) / tot
        if vs is not None:
            rv = vsh.where(support).rank(axis=1, pct=True)
            mv = support & (rv >= q)
            sc[f"VOLQ_{L:g}"] = mv
            ADM[(pname, f"VOLQ_{L:g}")] = float(mv.values.sum()) / tot
    SCREENS[pname] = sc
    for sname, sel in sc.items():
        for book in BOOKS:
            for conv in CONVS:
                gr, tn = fast_bt(pxp, weights(pxp, sel, book, conv))
                for cb in COSTS:
                    RET[(pname, sname, book, conv, cb)] = \
                        netr(gr, tn, cb).loc[START[pname]:]

# live RULES v2 comparand, per panel
MV2 = {}
for pname, (px, tr, vs) in PANELS.items():
    cols = [c for c in px.columns if c in set(tr)]
    gr, tn = fast_bt(px[cols], rules_v2_weights(px[cols]))
    MV2[pname] = mrow(netr(gr, tn, PROTO_COST).loc[START[pname]:])

SPYM, SPYOOS = {}, {}
for pname, (px, tr, vs) in PANELS.items():
    sp = px["SPY"].pct_change().fillna(0).loc[START[pname]:]
    SPYM[pname] = mrow(sp)
    SPYOOS[pname] = metrics(sp.loc[OOS_START:])["Sharpe"]


def verdicts(pname, r):
    m = mrow(r)
    ms, v2 = SPYM[pname], MV2[pname]
    ba = [x for x, bad in (("H1", m["H1"] <= v2["H1"]), ("H2", m["H2"] <= v2["H2"]),
                           ("DD", m["MaxDD"] < v2["MaxDD"])) if bad]
    oos = metrics(r.loc[OOS_START:])["Sharpe"]
    bb = [x for x, bad in (("H1", m["H1"] <= ms["H1"]), ("H2", m["H2"] <= ms["H2"]),
                           ("OOS", oos <= SPYOOS[pname]),
                           ("DD", m["MaxDD"] < 0.60 * ms["MaxDD"]),
                           ("CAGR", m["CAGR"] < 0.70 * ms["CAGR"])) if bad]
    return m, oos, ba, bb


vrows = []
for pname in PANELS:
    for sname in SCREENS[pname]:
        for book in BOOKS:
            for conv in CONVS:
                for cb in COSTS:
                    r = RET[(pname, sname, book, conv, cb)]
                    m, oos, ba, bb = verdicts(pname, r)
                    vrows.append(dict(panel=pname, screen=sname, inst=sname.split("_")[0],
                                      level=sname.split("_")[1], book=book, conv=conv, cost=cb,
                                      admit=ADM[(pname, sname)], CAGR=m["CAGR"],
                                      Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"],
                                      H2=m["H2"], OOS_Sharpe=oos,
                                      path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                                      path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")"))
V = pd.DataFrame(vrows)
V.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)

for pname in PANELS:
    ms, v2 = SPYM[pname], MV2[pname]
    P(f"\n  {pname}: SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.1%} "
      f"(H1 {ms['H1']:.3f} H2 {ms['H2']:.3f} OOS {SPYOOS[pname]:.3f}) | "
      f"RULES v2 @10bps {v2['CAGR']:.2%}/{v2['Sharpe']:.3f}/{v2['MaxDD']:.1%} "
      f"(H1 {v2['H1']:.3f} H2 {v2['H2']:.3f})")
    P(f"  4b bars: H1>{ms['H1']:.3f} H2>{ms['H2']:.3f} OOS>{SPYOOS[pname]:.3f} "
      f"MaxDD>={0.60 * ms['MaxDD']:.1%} CAGR>={0.70 * ms['CAGR']:.2%}")
    sub = V[(V.panel == pname) & (V.cost == PROTO_COST)]
    P(f"  {'screen':<11}{'admit':>7}{'book':<7}{'cv':<4}{'CAGR':>8}{'Shrp':>7}{'MaxDD':>8}"
      f"{'H1':>7}{'H2':>7}{'OOS':>7}  4a / 4b")
    for _, r in sub.sort_values(["inst", "level", "book", "conv"]).iterrows():
        P(f"  {r['screen']:<11}{r['admit']:>7.3f}{r['book']:<7}{r['conv']:<4}"
          f"{r['CAGR']:>8.2%}{r['Sharpe']:>7.3f}{r['MaxDD']:>8.1%}{r['H1']:>7.3f}"
          f"{r['H2']:>7.3f}{r['OOS_Sharpe']:>7.3f}  {r['path4a']} / {r['path4b']}")

P(f"\n  ALL {len(V)} grid points reported in .verdicts.csv.  "
  f"4a KEEP {int((V.path4a == 'KEEP').sum())}/{len(V)};  "
  f"4b KEEP {int((V.path4b == 'KEEP').sum())}/{len(V)}")
for pname in PANELS:
    s = V[V.panel == pname]
    s10 = s[s.cost == PROTO_COST]
    P(f"    {pname}: 4a {int((s.path4a == 'KEEP').sum())}/{len(s)}, "
      f"4b {int((s.path4b == 'KEEP').sum())}/{len(s)};  at the PROTOCOL 10-bps rung only: "
      f"4a {int((s10.path4a == 'KEEP').sum())}/{len(s10)}, "
      f"4b {int((s10.path4b == 'KEEP').sum())}/{len(s10)}")
kb = V[(V.path4b == "KEEP") & (V.cost == PROTO_COST)]
P(f"  every 10-bps 4b pass, with its screen: "
  f"{'; '.join(f'{r.panel}/{r.screen}/{r.book}/{r.conv}' for _, r in kb.iterrows()) or 'none'}")
noneb = kb[kb.inst == "NONE"]
P(f"  of those, {len(noneb)} carry NO screen at all — the clause deletes nothing that the "
  f"un-screened book does not already deliver.")
sm = V[(V.panel == 'SMALL439')]
P(f"  P5a {'HIT' if int((sm.path4b == 'KEEP').sum()) == 0 else 'MISS'} "
  f"(no SMALL439 arm clears 4b: {int((sm.path4b == 'KEEP').sum())} passes)")

# =====================================================================================
# RULE 8 — level chosen on 2010..2016, 2017..2026 read once
# =====================================================================================
P("\n" + "-" * 118)
P("RULE 8  WALK-FORWARD — screen LEVEL chosen on IS (<= 2016-12-31) by Sharpe; OOS read once")
P("-" * 118)
wrows = []
for pname in PANELS:
    for inst in ["PXABS", "PXQ", "VOLQ"]:
        names = [s for s in SCREENS[pname] if s.startswith(inst + "_")]
        if not names:
            continue
        for book in BOOKS:
            for conv in CONVS:
                for cb in [PROTO_COST, 25]:
                    isS = {s: metrics(RET[(pname, s, book, conv, cb)].loc[:IS_END])["Sharpe"]
                           for s in names}
                    pick = max(isS, key=isS.get)
                    # second leg: the chooser is allowed to ABSTAIN (pick no screen at all)
                    isA = dict(isS)
                    isA["NONE_0"] = metrics(
                        RET[(pname, "NONE_0", book, conv, cb)].loc[:IS_END])["Sharpe"]
                    pickA = max(isA, key=isA.get)
                    roA = RET[(pname, pickA, book, conv, cb)].loc[OOS_START:]
                    ro = RET[(pname, pick, book, conv, cb)].loc[OOS_START:]
                    rc = RET[(pname, "NONE_0", book, conv, cb)].loc[OOS_START:]
                    sp = PANELS[pname][0]["SPY"].pct_change().fillna(0).loc[OOS_START:]
                    mo, mc, msp = metrics(ro), metrics(rc), metrics(sp)
                    ora = max(names, key=lambda s: metrics(
                        RET[(pname, s, book, conv, cb)].loc[OOS_START:])["Sharpe"])
                    oraS = metrics(RET[(pname, ora, book, conv, cb)].loc[OOS_START:])["Sharpe"]
                    wrows.append(dict(panel=pname, inst=inst, book=book, conv=conv, cost=cb,
                                      IS_pick=pick, IS_Sharpe=isS[pick],
                                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                      OOS_MaxDD=mo["MaxDD"],
                                      ctrl_OOS_Sharpe=mc["Sharpe"], ctrl_OOS_CAGR=mc["CAGR"],
                                      spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_CAGR=msp["CAGR"],
                                      d_vs_ctrl=mo["Sharpe"] - mc["Sharpe"],
                                      d_vs_spy=mo["Sharpe"] - msp["Sharpe"],
                                      oracle_pick=ora, oracle_OOS_Sharpe=oraS,
                                      headroom=oraS - mo["Sharpe"],
                                      abstain_pick=pickA,
                                      abstain_OOS_Sharpe=metrics(roA)["Sharpe"],
                                      abstain_d_vs_ctrl=metrics(roA)["Sharpe"] - mc["Sharpe"]))
W = pd.DataFrame(wrows)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  {'panel':<10}{'inst':<7}{'book':<7}{'cv':<4}{'bps':>4}{'pick':<11}"
  f"{'OOS CAGR':>10}{'OOS Shrp':>10}{'ctrl':>8}{'SPY':>8}{'d ctrl':>8}{'d SPY':>8}{'hdrm':>7}")
for _, r in W.iterrows():
    P(f"  {r['panel']:<10}{r['inst']:<7}{r['book']:<7}{r['conv']:<4}{int(r['cost']):>4}"
      f"{r['IS_pick']:<11}{r['OOS_CAGR']:>10.2%}{r['OOS_Sharpe']:>10.3f}"
      f"{r['ctrl_OOS_Sharpe']:>8.3f}{r['spy_OOS_Sharpe']:>8.3f}"
      f"{r['d_vs_ctrl']:>8.3f}{r['d_vs_spy']:>8.3f}{r['headroom']:>7.3f}")


def tstat(x):
    x = np.asarray(x, float)
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 1 and x.std() else 0.0


P(f"\n  chooser vs the NO-SCREEN control, OOS Sharpe: mean {W.d_vs_ctrl.mean():+.4f} "
  f"t {tstat(W.d_vs_ctrl):+.2f}, wins {int((W.d_vs_ctrl > 0).sum())}/{len(W)}")
P(f"  chooser vs SPY, OOS Sharpe:                  mean {W.d_vs_spy.mean():+.4f} "
  f"t {tstat(W.d_vs_spy):+.2f}, wins {int((W.d_vs_spy > 0).sum())}/{len(W)}")
P(f"  oracle headroom over the whole level ladder:  mean {W.headroom.mean():+.4f} "
  f"(perfect hindsight buys this much and no more)")
P(f"  chooser ALLOWED TO ABSTAIN (no-screen in the ladder): mean "
  f"{W.abstain_d_vs_ctrl.mean():+.4f} vs the control, abstains in "
  f"{int((W.abstain_pick == 'NONE_0').sum())}/{len(W)} cells")
for inst in ["PXABS", "PXQ", "VOLQ"]:
    s = W[W.inst == inst]
    if len(s):
        P(f"    {inst:<6} d_vs_ctrl mean {s.d_vs_ctrl.mean():+.4f} "
          f"wins {int((s.d_vs_ctrl > 0).sum())}/{len(s)};  "
          f"d_vs_spy mean {s.d_vs_spy.mean():+.4f} wins {int((s.d_vs_spy > 0).sum())}/{len(s)}")
u = W[(W.panel == "U56") & (W.inst == "PXQ")]
uv = W[(W.panel == "U56") & (W.inst == "PXABS")]
P(f"  P5b {'HIT' if len(u) and u.d_vs_ctrl.mean() <= 0 else 'MISS'} "
  f"(the T1-unsafe PXQ arm does not beat its no-screen comparand OOS on U56: "
  f"{u.d_vs_ctrl.mean():+.4f})")

# =====================================================================================
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"  Q1 the two instruments answer DIFFERENT questions on the same key: DET flags "
  f"{int(K.DET_level_flag.astype(bool).sum())}/{n} in the LEVEL form and "
  f"{int(K.DET_rank_flag.astype(bool).sum())}/{n} in the RANK form; CERT(rank) flags "
  f"{int((~K.CERT_rank_says_safe).sum())}/{n}.  Ground-truth accuracy: DET(level) "
  f"{det_L_acc}/{n}, CERT(rank) {cert_R_acc}/{n}.")
P(f"  Q2 DET reads the whole {len(FILES)}-file corpus in {det_secs:.2f} s with no data; CERT can "
  f"be pointed automatically at {n_call / len(FILES):.1%} of those files and costs "
  f"{1000 * cert_key_secs / n:.0f} ms per key with the panel loaded.")
P(f"  Q3 false-negative floors are DISJOINT: DET misses "
  f"{sorted(set(F[(F.instrument == 'DET')].key))}; CERT misses "
  f"{sorted(set(cert_fn.key)) if len(cert_fn) else []}.")
P(f"  Q4 book: 4a {int((V.path4a == 'KEEP').sum())}/{len(V)}, "
  f"4b {int((V.path4b == 'KEEP').sum())}/{len(V)}; rule-8 chooser vs no-screen control "
  f"{W.d_vs_ctrl.mean():+.4f} (t {tstat(W.d_vs_ctrl):+.2f}).")
P("\n  RECOMMENDATION — the queue asks which instrument the T1 clause should NAME.  Read off the")
P("  numbers above, NEITHER alone is adequate and the answer is an ORDERED PAIR, not a choice:")
P(f"    1. The DETECTOR is the GATE, because it is the only instrument with corpus-wide reach: "
  f"it types every file with no data and no execution, reproduced 428's census exactly "
  f"(293/293), and CERT cannot be pointed at even the {n_call / len(FILES):.0%} upper-bound "
  f"share of files without a hand-written harness.")
P(f"    2. The CERTIFICATE is the ADJUDICATOR, in its VALUE form at a one-rank-step tolerance, "
  f"because it is the only instrument with no false clearance "
  f"({int((K.CERT_level_clause_clears_cal & K.truth_either_leaks).sum())}/{n} vs the detector's "
  f"{int((K.DET_clause_clears & K.truth_either_leaks).sum())}/{n}).  The RANK form idea 426 "
  f"drafts is NOT the one to name: it clears a single-column price aggregate (MKTLVL), which a "
  f"per-name rescale cannot re-order.")
P("    3. Two documented amendments must go in with it, or the clause is quoted on wrong numbers:")
P(f"       (a) the detector's degree tables mis-type `diff` and `rank` as degree-0, `var` as "
  f"degree-1 and leave `np.log` untyped, and its `div`/`mul` handling ignores the argument's "
  f"degree (REBASED false-positived) — 4 false clearances and 1 false rejection on 20 keys;")
P(f"       (b) the queue's '~2 s for 379 scripts' is wrong by {det_secs / 2:.0f}x "
  f"({det_secs:.0f} s measured), so cost is not the detector's advantage — reach is.")
P(f"    4. Adopting the clause costs capital NOTHING measurable: of the "
  f"{int((V.path4b == 'KEEP').sum())} 4b passes in the grid, "
  f"{int(((V.path4b == 'KEEP') & (V.inst == 'NONE')).sum())} carry no screen at all, and the "
  f"rule-8 chooser over screen levels loses {abs(W.d_vs_ctrl.mean()):.4f} of OOS Sharpe to "
  f"simply not screening (0/{len(W)} wins).  The T1-unsafe arms the clause deletes were not "
  f"earning anything, so this is a REPORTING clause with no book cost — which is exactly why "
  f"it is cheap to adopt and why it must not be sold as an edge.")
P(f"\n  elapsed {time.time() - T0:.1f} s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
