#!/usr/bin/env python3
"""Idea 1048 (lane C, 2026-09-16) — does ANY committed EXPONENT or SCALING claim in the record
state its own RESOLUTION?

QUESTION (QUEUE idea 1048, verbatim)
    idea 1044 found an exponent fitted on this tape carries a 0.67-0.73 wide 90% interval, so a
    published slope of -0.51 and one of -0.67 are the same measurement.  Census the record's
    committed exponent / slope / scaling claims (1012's -0.5110 / -0.5003 / -0.4943 among them)
    for whether any states the interval its own null gives, and re-express those that do not.
    Max 2 params (claim set, interval basis).

THE OBJECT.  A published exponent is a POINT.  Its RESOLUTION is the width of the interval the
    same construction would give if it were run again — on another draw (the estimator's own
    noise) or on another tape the same process could have produced (the sampling noise the
    record can never redraw).  A claim states its resolution when it publishes that width beside
    the point.  This run measures the width for the one exponent family the tree can REBUILD —
    1012's log-log fit of Sharpe SE against window length — and censuses the record for how many
    of its exponent/slope/scaling claims carry any width at all.

WHAT HAD TO BE SAID BEFORE ANY NUMBER (declared here, ahead of the gates).
    There are three different widths and they are NOT interchangeable; which one a claim owes is
    the whole question, so all three are computed at every point and none is called THE interval:
      (i)   REDRAW — the same tape, the same ladder, a fresh bootstrap seed.  This is the
            weakest possible interval: it asks only "would a re-run of this script publish this
            number again?"  It shrinks with the draw count and says nothing about the tape.
      (ii)  TAPE — a stationary block-21 resample of the underlying daily series, i.e. another
            tape the same process could have produced, put through the WHOLE ladder and fit.
            This is the interval 1044 means by "its own null", and it does NOT shrink with the
            draw count.
      (iii) OLS — the log-log regression's own residual interval (b +/- t(0.95, n-2) * SE_b).
            It is the interval the fit hands the author for free, and it is the one a 6-rung
            ladder makes look tightest, because the six rungs are read off the SAME tape and
            their errors are strongly positively correlated — a correlation OLS assumes away.
    PREDICTION, written before the numbers: OLS < REDRAW << TAPE, and only TAPE answers the
    queue's question.  A claim quoting (iii) has stated a resolution; it has not stated the one
    that decides whether -0.51 and -0.67 are the same measurement.

A CONFOUND STATED UP FRONT, not discovered later.  The record's exponent claims are not all the
    same object: 1012's is a log-log fit of a bootstrap SE on window length, others are OLS
    slopes of quite different quantities (cost tolerance against turnover, rate against
    distance, dCAGR against an exponent dial).  This run can RE-DERIVE only the 1012 family.
    Every other claim is re-expressed with a TRANSFERRED width — explicitly labelled as such in
    `.rederive.csv` — and a transferred width is an ORDER-OF-MAGNITUDE statement about what a
    6-rung log-log fit on this tape can resolve, NOT a re-derivation of that claim.  The two
    populations are reported separately everywhere and never summed into one headline.

WHAT IS MEASURED
    (A) THE CENSUS.  Every committed exponent / scaling / slope claim in the corpus, classified
        on two FIXED (untuned) taxonomies: KIND (K1_VALUED — a numeric value is asserted for the
        exponent; K0_QUAL — scaling asserted with no number) and RESOLUTION (R3_NULL — a null or
        bootstrap interval with a stated confidence level; R2_SE — a standard error, a +/-, a
        "2 SE"; R1_SPREAD — a range of fitted values across cells, which is a DISPERSION not a
        resolution; R0_NONE — nothing).  Every claim row is dumped so the classification is
        auditable line by line.
    (B) THE RE-DERIVATION.  1012's own ladder rebuilt verbatim (LAD6 = L/n_full in {0.125, 0.25,
        0.375, 0.50, 0.75, 1.00}, 1,000 stationary-bootstrap draws per rung, the three estimators
        BLOCK21 / BLOCK5 / IID, both panels, 1012's own 9-book shelf), its three published
        exponents re-derived, and each given a 90% interval on all three bases above.  COST,
        STATED: the two RESAMPLING bases (REDRAW, TAPE) are priced at the HEADLINE estimator
        BLOCK21 only — 100 reps x 2 panels x a full 6-rung x 1,000-draw ladder over 10 series
        each — while the OLS basis, which costs nothing extra, is published at all three.
    (C) THE 9-CELL GRID.  CLAIM SET x INTERVAL BASIS, every cell published: how many claims, how
        many valued, how many state any width, the basis's own measured width W, how many valued
        claims are DISTINGUISHABLE from the sqrt law at W, and what share of claim PAIRS inside
        the set are distinguishable from EACH OTHER at W.
    (D) THE RE-EXPRESSION the queue asks for: every valued claim printed as point [lo, hi] with
        its width's provenance (MEASURED for the 1012 family, TRANSFERRED otherwise).
    (E) THE RULE-8 WALK-FORWARD at PROTOCOL's declared split 2016-12-31 (IS 2009-2016 chooses,
        2017-2026 read ONCE): OOS CAGR / Sharpe / MaxDD for each of the record's three IS-only
        choosers on both panels at all three cost rungs, against the live RULES v2 book and
        against SPY, BOTH KEEP paths, every point reported.

TUNED PARAMETERS: exactly TWO, the two the queue names.  All 9 cells reported, none selected.
    (1) CLAIM SET   REC (LEADERBOARD.md + CHANGELOG.md — the record proper, HEADLINE),
                    REC+MEMO (+ every committed .md under research/ and research/backtests/),
                    ALL (+ every committed .py under research/ and research/backtests/).
    (2) INTERVAL BASIS   TAPE (HEADLINE, 1044's convention), REDRAW, OLS.

    ONE REPORTED CONTROL, not a third dial: the claim DEFINITION.  STRICT (the headline) requires
    an exponent-family keyword; WIDE additionally admits bare regression SLOPE claims.  Both are
    published at every point; STRICT decides every hypothesis.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_ANY    DECISIVE, the queue's literal question.  At least 10% of the REC claim set's VALUED
             exponent claims state a sampling interval (R2_SE or R3_NULL).  PASS => the record
             does state its resolutions.  FAIL => it does not, and the re-expression is owed.
    H_RESOLVE the headline interval (1012's SPY exponent, TAPE basis, 90%) is <= 0.10 wide — the
             resolution the queue's own framing needs to tell -0.51 from -0.67.
    H_BASIS  the three bases agree: max width / min width <= 1.5 on the headline object.
    H_SAME   1012's three published exponents (-0.5110 / -0.5003 / -0.4943) are mutually
             DISTINGUISHABLE at the headline width (every pairwise |d| > W).  FAIL => the record
             published three numbers that are one measurement.
    H_SQRT   -0.5 lies OUTSIDE the 90% TAPE interval for at least one re-derived exponent
             (panel x the headline estimator), i.e. the tape resolves its own law away from
             theory.
    H_DIGIT  the four decimal places the record prints are justified: the headline width is
             <= 2e-4.
    Bars are absolute and were fixed before the numbers.  H_SQRT and H_DIGIT are written so that
    PASS means "the record's precision is earned"; both are expected to FAIL, and a FAIL is the
    finding, not a defect.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  the pools are the record's own grid_books() (18 per panel) and shelf_books() (9).
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the committed 15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: idea 1012's committed `.ladder.csv` reproduces rung by rung (se_COMP and
        se_PAIRED), and its three published exponents reproduce to 1e-3.
    G5  determinism: the interval machinery rebuilds bit-for-bit at the same seed.
    G6  ESTIMATOR VALIDATION: on a synthetic i.i.d. control whose true exponent is EXACTLY -0.5,
        the median fitted b over independent tapes is -0.5 +/- 0.01 and the one-tape TAPE
        interval width is within 1.5x the across-tape spread of b.
    G7  CENSUS STAMP (idea 1019's proposed clause, honoured here): `.stamp.txt` carries every
        file READ with its byte length and sha256, the aggregate counts, the HEAD commit and a
        file_list_sha; the prose below quotes the manifest's own totals.
    G8  CLAIM EXTRACTION is order-independent and deterministic: a second pass over a shuffled
        file order yields an identical claim multiset.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL in the rule-8 block is optimistic and every 4b count an UPPER bound.  The
    census arm is a census of committed TEXT and inherits its sources' bias.  The measured object
    — the WIDTH of an exponent's interval — is a property of tape length and draw count; a
    survivor panel raises the Sharpe LEVEL, which raises the SE of a Sharpe and therefore makes
    the widths reported here an UPPER bound in the same direction for every basis alike.  SPY is
    a real index series and is not inflated.

LIMITS, STATED.  The STRICT regex is deliberately conservative (an exponent-family keyword plus a
    decimal within 60 characters), so every census count is a LOWER bound on the claims that
    exist and the "states no interval" share is measured on the subset most favourable to the
    record.  Only ONE exponent family is re-derivable from a committed definition; the other
    claims are not asserted wrong, only unverifiable at their own published precision.  The TAPE
    null is a stationary block-21 resample, which preserves short-range dependence and destroys
    long-range regime structure, so it is a LOWER bound on the tape's true variability.  The
    interval is 90% throughout, 1044's own convention.
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-ANY-committed-EXPONENT-or-SCALING-claim-state-its-own-RESOLUTION"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"
PUB_1012 = HERE / "2026-09-16_is-the-4b-SHARPE-LEG-DECIDABLE-AT-ALL-at-the-record-s-SAMPLE-LENGTH_B.ladder.csv"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW_CH = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
YEAR = 252.0

# ---- 1012's ladder, inherited VERBATIM (not tuned here) --------------------------------------
LAD6 = [0.125, 0.25, 0.375, 0.50, 0.75, 1.00]
ESTS = {"BLOCK21": 21, "BLOCK5": 5, "IID": 1}
EST_HEAD = "BLOCK21"
N_BOOT = 1000
SEED_1012 = 1012

# ---- the two tuned dials ---------------------------------------------------------------------
CLAIMSETS = ["REC", "REC+MEMO", "ALL"]
CS_HEAD = "REC"
BASES = ["TAPE", "REDRAW", "OLS"]
BASIS_HEAD = "TAPE"
DEFS = ["STRICT", "WIDE"]          # reported CONTROL, not a dial
DEF_HEAD = "STRICT"

NREP = 100                          # reps for the two resampling bases
NCTL = 200                          # independent zero-truth control tapes (G6)
MAX_VOL = 0.60
BLOCK_TAPE = 21
CONF = 0.90
SEED0 = 10480916

# pre-registered bars
BAR_ANY = 0.10
DRAWS_CTL = [1000, 250, 60, 15, 4, 2]     # REPORTED mechanism control, no bar, not a dial
BAR_RESOLVE = 0.10
BAR_BASIS = 1.5
BAR_DIGIT = 2e-4

# ---- THE AUDIT.  Every R2_SE / R3_NULL hit the classifier raises is adjudicated BY HAND here,
# against ONE declared rule: a hit COUNTS only if the width it quotes is a width ON THE VALUE OF
# THE EXPONENT ITSELF.  A pre-registered BAR, a theory value, an interval on some other statistic,
# and the string "SE" appearing because SE is the fitted Y-VARIABLE all FAIL that rule.  The table
# is keyed by (file basename, resolution level, value) and every hit must appear in it (gate G9),
# so nothing is silently dropped and every judgement is visible and arguable.
AUDIT = {
    ("CHANGELOG.md", "R2_SE", -0.5110):
        (False, "'SE(L) fits a log-log slope of -0.5110' — SE is the fitted Y-VARIABLE, not an "
                "interval on b; the exponent is published bare"),
    ("CHANGELOG.md", "R3_NULL", 1.0000):
        (False, "the +/-0.02 band is on SHARPE FLATNESS over a k range, not on an exponent"),
    ("2026-09-05_the-on-share-column_cloud.result.md", "R3_NULL", 0.6800):
        (False, "the band belongs to clause 11b's null and the 0.68 is a Spearman rho, not an "
                "exponent with an interval"),
    ("2026-09-16_leg-noise-basis-clause_B.memo.md", "R2_SE", -0.5110):
        (False, "the same 1012 sentence restated in a memo; SE is the fitted Y-VARIABLE"),
    ("2026-09-16_rule8-length-adjustment-clause_cloud.memo.md", "R2_SE", -0.2996):
        (True, "1044's clause: the fitted exponent -0.2996..-0.8465 published WITH its own "
               "geometry-matched null width 0.67-0.73 at 90% and the +/-0.05 it would need"),
    ("2026-09-16_is-the-4b-SHARPE-LEG-DECIDABLE-AT-ALL-at-the-record-s-SAMPLE-LENGTH_B.py",
     "R2_SE", -0.6500):
        (False, "a PRE-REGISTERED BAR ([-0.65, -0.35]) is not a measured interval"),
    ("2026-09-16_is-the-4b-SHARPE-LEG-DECIDABLE-AT-ALL-at-the-record-s-SAMPLE-LENGTH_B.py",
     "R2_SE", -0.5000):
        (False, "'b = -0.5 is the sqrt law' is a THEORY value, not a measurement"),
    ("2026-09-16_is-the-4b-SHARPE-LEG-DECIDABLE-AT-ALL-at-the-record-s-SAMPLE-LENGTH_B.py",
     "R2_SE", -0.4000):
        (False, "a code fragment inside the G9 control, not a published claim"),
    ("2026-09-16_is-the-K-FREE-NULL-SD-a-WINDOW-LENGTH-CURVE-with-a-SOLVABLE-EXPONENT_cloud.py",
     "R2_SE", -0.5000):
        (False, "'sd ~ L^-0.5 once D = 0' is a THEORY statement in a docstring"),
}

SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_EXP = {"1012_SPY_COMP": -0.5110, "1012_MEDBOOK_PAIRED": -0.5003, "1012_IID_CONTROL": -0.4943}
PUB_1044_WIDTH = (0.67, 0.73)       # 1044's committed 90% null band width for a fitted exponent
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC1048", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


# ====================================================================== ladder machinery (1012's)
def stat_idx(T, L, block, rng, n=N_BOOT):
    """Stationary (Politis-Romano) bootstrap indices, idea 1012's function verbatim."""
    out = np.empty((n, L), dtype=np.int32)
    out[:, 0] = rng.integers(0, T, n)
    if L > 1:
        p = 1.0 / block
        newstart = rng.random((n, L - 1)) < p if block > 1 else np.ones((n, L - 1), bool)
        starts = rng.integers(0, T, (n, L - 1))
        for t in range(1, L):
            prev = out[:, t - 1] + 1
            prev[prev >= T] = 0
            out[:, t] = np.where(newstart[:, t - 1], starts[:, t - 1], prev)
    return out


def sharpe_vec(x, idx):
    X = np.asarray(x, float)[idx]
    m = X.mean(axis=1)
    s = X.std(axis=1, ddof=1)
    return np.where(s > 0, m * np.sqrt(YEAR) / s, np.nan)


def fitb(L, se):
    """1012's fit: OLS of log SE on log L.  Returns the slope only."""
    L = np.asarray(L, float)
    se = np.asarray(se, float)
    ok = np.isfinite(se) & (se > 0)
    if ok.sum() < 3:
        return np.nan
    return float(np.polyfit(np.log(L[ok]), np.log(se[ok]), 1)[0])


def fit_ols_ci(L, se, conf=CONF):
    """Slope plus its OWN regression interval: b +/- t(conf, n-2) * SE_b."""
    x = np.log(np.asarray(L, float))
    y = np.log(np.asarray(se, float))
    n = len(x)
    b, a = np.polyfit(x, y, 1)
    resid = y - (a + b * x)
    sxx = float(((x - x.mean()) ** 2).sum())
    seb = float(np.sqrt((resid ** 2).sum() / (n - 2) / sxx))
    # two-sided t quantile for n-2 df at (1+conf)/2; hard-coded table (no scipy in this sandbox)
    TQ = {1: 6.314, 2: 2.920, 3: 2.353, 4: 2.132, 5: 2.015, 6: 1.943, 8: 1.860, 10: 1.812}
    t = TQ.get(n - 2, 1.645)
    return float(b), float(b - t * seb), float(b + t * seb), seb


def ladder_ses(cols, T, rng, est, fracs=LAD6, n=N_BOOT):
    """One full ladder.  `cols` is a list of 1-D arrays over the SAME tape; col 0 is SPY.
    Returns (L list, se_COMP of col 0, [se_PAIRED of each other col])."""
    blk = ESTS[est]
    Ls, se0, sep = [], [], [[] for _ in cols[1:]]
    for f in fracs:
        L = max(40, int(round(f * T)))
        idx = stat_idx(T, L, blk, rng, n=n)
        s0 = sharpe_vec(cols[0], idx)
        Ls.append(L)
        se0.append(float(np.std(s0, ddof=1)))
        for j, c in enumerate(cols[1:]):
            sj = sharpe_vec(c, idx)
            sep[j].append(float(np.std(sj - s0, ddof=1)))
    return Ls, se0, sep


def block_tape(x, T, rng, block=BLOCK_TAPE):
    """One stationary block-`block` resample of a tape of length T (index vector)."""
    return stat_idx(T, T, block, rng, n=1)[0]


def pct_interval(v, conf=CONF):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    lo = float(np.percentile(v, 100 * (1 - conf) / 2))
    hi = float(np.percentile(v, 100 * (1 + conf) / 2))
    return lo, hi, hi - lo


# ====================================================================== census machinery
KW_STRICT = re.compile(
    r"(exponent|log-?log|power[- ]?law|sqrt law|scaling law|scales? (?:like|as|with)|"
    r"falls? like|rises? like|elasticity|1\s*/\s*sqrt\s*\(\s*[nlt]\b|sqrt\(n\) law)", re.I)
KW_SLOPE = re.compile(r"\bslopes?\b", re.I)
EXCL = re.compile(r"(vol[-_ ]?scal|1/sqrt\(vol|vol_scale|scaler\b|rank tilt)", re.I)
DEC = re.compile(r"[-+−]?\d+\.\d+")
NOTVAL = re.compile(r"(n\s*=\s*|R2\s*|R\^2\s*|p\s*=\s*|t\s*=\s*)$")
RES_R3 = re.compile(r"(\d{2}\s*%\s*(interval|band|ci\b)|\b(90|95|99)%|null (band|interval)|"
                    r"bootstrap interval|percentile interval|confidence interval|\bCI\b)", re.I)
RES_R2 = re.compile(r"(\bSEs?\b|standard error|±|\+/-|\b\d\s*SE\b|its own sd\b)", re.I)
RES_R1 = re.compile(r"(\.\.[-+]?\d|\brange\b|\bspread\b|over \d+ fits|min/max|\bband\b)", re.I)
SPLIT = re.compile(r"(?<=[.;])\s+|\s*\|\s*")


def sentences(text):
    return [p.strip() for p in SPLIT.split(text.replace("\n", " ")) if p.strip()]


def corpus_files(scope):
    """Sorted, deterministic file lists.  REC < REC+MEMO < ALL, strictly nested."""
    rec = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    memo = sorted((ROOT / "research" / "backtests").glob("*.md")) + \
        [ROOT / "research" / "RULES.md", ROOT / "research" / "PROTOCOL.md"]
    py = sorted((ROOT / "research" / "backtests").glob("*.py")) + \
        sorted(p for p in (ROOT / "research").glob("*.py"))
    py = [p for p in py if p.resolve() != Path(__file__).resolve()]   # never census THIS script
    if scope == "REC":
        out = rec
    elif scope == "REC+MEMO":
        out = rec + memo
    else:
        out = rec + memo + py
    return [p for p in out if p.exists()]


def classify_value(sent, m, window=60):
    """The numeric value asserted for the exponent, or None.  Nearest decimal within `window`
    characters of the keyword, rejecting decimals that are plainly an n=, p=, t= or R2 token."""
    a, b = max(0, m.start() - window), min(len(sent), m.end() + window)
    seg = sent[a:b]
    best, bestd = None, 10 ** 9
    for d in DEC.finditer(seg):
        pre = seg[max(0, d.start() - 6):d.start()]
        if NOTVAL.search(pre):
            continue
        centre = (m.start() + m.end()) / 2 - a
        dist = abs((d.start() + d.end()) / 2 - centre)
        if dist < bestd:
            best, bestd = d.group(0).replace("−", "-"), dist
    if best is None:
        return None
    try:
        return float(best)
    except ValueError:
        return None


def resolution_level(scope_text):
    if RES_R3.search(scope_text):
        return "R3_NULL"
    if RES_R2.search(scope_text):
        return "R2_SE"
    if RES_R1.search(scope_text):
        return "R1_SPREAD"
    return "R0_NONE"


def harvest(files):
    """Every exponent/scaling/slope claim in `files`.  Deterministic in file order and position;
    G8 re-runs this on a shuffled order and compares."""
    rows = []
    for f in files:
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        sents = sentences(text)
        for i, s in enumerate(sents):
            ctx = " ".join(sents[max(0, i - 1):i + 2])
            for defn, kw in (("STRICT", KW_STRICT), ("WIDE", KW_SLOPE)):
                m = kw.search(s)
                if not m:
                    continue
                if EXCL.search(s[max(0, m.start() - 30):m.end() + 30]):
                    continue
                val = classify_value(s, m)
                rows.append(dict(
                    file=str(f.relative_to(ROOT)), sent_i=i, defn=defn,
                    keyword=m.group(0).lower(),
                    value=val, kind=("K1_VALUED" if val is not None else "K0_QUAL"),
                    res_sent=resolution_level(s), res_ctx=resolution_level(ctx),
                    text=s[:300]))
    df = pd.DataFrame(rows)
    if len(df):
        # a WIDE hit that is already a STRICT hit in the same sentence is not counted twice
        strict_keys = set(zip(df[df.defn == "STRICT"].file, df[df.defn == "STRICT"].sent_i))
        drop = (df.defn == "WIDE").values & np.array(
            [tuple(k) in strict_keys for k in zip(df.file, df.sent_i)])
        df = df[~drop].reset_index(drop=True)
    return df


def sha_file(p):
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


# ====================================================================== rule-8 machinery (record's)
def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def raw_pick(sub, ch, spy_is):
    """The record's own three IS-ONLY choosers, verbatim."""
    if ch == "IS_SHARPE":
        return sub["IS_Sharpe"].idxmax()
    if ch == "IS_CAGR":
        return sub["IS_CAGR"].idxmax()
    s = sub.copy()
    s["nlegs"] = ((s["IS_Sharpe"] > spy_is[1]).astype(int)
                  + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * spy_is[0]).astype(int)
                  + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(spy_is[2])).astype(int))
    s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
    return s.index[0]


def main():
    t0 = time.time()
    P(f"# Idea 1048 (lane C, {DATE}) — does ANY committed EXPONENT or SCALING claim in the "
      f"record state its own RESOLUTION?")
    P(f"# 2 tuned dials: CLAIM SET {CLAIMSETS} x INTERVAL BASIS {BASES} = "
      f"{len(CLAIMSETS)*len(BASES)} cells, ALL reported, none selected.  HEADLINE "
      f"{CS_HEAD} x {BASIS_HEAD}.")
    P(f"# ONE reported control, not a dial: claim DEFINITION {DEFS} (STRICT decides every "
      f"hypothesis).  Confidence {CONF:.0%} throughout (1044's convention).")
    P("# DECLARED BEFORE ANY NUMBER: three widths exist and are not interchangeable —")
    P("#   OLS (the fit's own, assuming independent rungs) < REDRAW (same tape, fresh seed)")
    P("#   << TAPE (another tape the process could have produced).  Only TAPE answers the queue.")
    P("# CONFOUND STATED UP FRONT: only the 1012 exponent family is re-derivable on this tree;")
    P("#   every other claim gets a TRANSFERRED width, labelled as such, never summed with the")
    P("#   measured ones.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every rule-8 LEVEL is optimistic")
    P("#   and every 4b count an UPPER bound; a survivor panel raises Sharpe, hence SE, hence")
    P("#   every width here alike.  Reported, not asserted.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    PANELS = ["U56", "B136"]
    REC = {p: PX[p].index[WARMUP] for p in PANELS}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    pool = C.grid_books(U, B)
    shelf = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)             # idea 1012's own 9th shelf book, verbatim
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    shelf["u56-top20-g065-M"] = dict(panel="U56", freq="M",
                                     W=(rk <= 20).astype(float) * 0.65 / 20, memo=None,
                                     src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    BOOKS = {p: sorted(b for b in pool if pool[b]["panel"] == p) for p in PANELS}
    SHELF = {p: sorted(b for b in shelf if shelf[b]["panel"] == p) for p in PANELS}
    P(f"POOL = {len(pool)} GRID books ({len(BOOKS['U56'])} U56 / {len(BOOKS['B136'])} B136); "
      f"SHELF = {len(shelf)} memo-backed books ({len(SHELF['U56'])} / {len(SHELF['B136'])}).")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    SHNET = {}
    for nm, b in shelf.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        SHNET[nm] = (r - t * RUNG_HEAD / 1e4).loc[REC[b["panel"]]:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PANELS}
    SPYB = {p: split_block(SPYR[p], REC_END) for p in PANELS}
    SPYIS = {p: (SPYB[p]["IS_CAGR"], SPYB[p]["IS_Sharpe"], SPYB[p]["IS_MaxDD"]) for p in PANELS}
    V2 = {}
    for p in PANELS:
        px = PX[p]
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = split_block((r - t * c / 1e4).loc[REC[p]:], REC_END)
    NFULL = {p: len(SPYR[p]) for p in PANELS}
    P(f"Post-warm-up series: U56 {NFULL['U56']:,} days, B136 {NFULL['B136']:,} days "
      f"(from {REC['U56'].date()} / {REC['B136'].date()}).")
    P("")

    # ================================================================ GATES
    P("=" * 100)
    P("GATES (printed before any hypothesis number)")
    P("=" * 100)
    gates = {}

    pxu = PX["U56"]
    Wt = rules_v2_weights(pxu)
    r_f, t_f = fast_run(pxu, Wt, rebalance_mask(pxu.index, "W"))
    eng = backtest(pxu, Wt, cost_bps=0.0, freq="W")
    st = REC["U56"]
    d_r = float(np.abs(r_f.loc[st:].values - eng["returns"].loc[st:].values).max())
    d_t = float(np.abs(t_f.loc[st:].values - eng["turnover"].loc[st:].values).max())
    gates["G1"] = (d_r < 1e-12 and d_t < 1e-12,
                   f"fast_run == engine.backtest  max|dret| {d_r:.2e}  max|dturn| {d_t:.2e}")

    gates["G2"] = (len(BOOKS["U56"]) == 18 and len(BOOKS["B136"]) == 18 and len(shelf) == 9,
                   f"pools = {len(BOOKS['U56'])} / {len(BOOKS['B136'])} GRID + {len(shelf)} SHELF")

    trip = (SPYB["U56"]["OOS_CAGR"], SPYB["U56"]["OOS_Sharpe"], SPYB["U56"]["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    gates["G3"] = (d3 < 5e-3, f"SPY OOS {trip[0]:.4f} / {trip[1]:.4f} / {trip[2]:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED}  max|d| {d3:.2e}")

    # ---- G4: rebuild 1012's ladder on its own rng stream and compare to its committed csv
    P("  rebuilding idea 1012's ladder on its own seed stream ...")
    rngL = np.random.default_rng(SEED_1012 + 1)
    LAD_IDX = {}
    for p in PANELS:                       # 1012's loop order: panel, frac, estimator
        T = NFULL[p]
        for f in LAD6:
            L = max(40, int(round(f * T)))
            for e in ESTS:
                LAD_IDX[(p, f, e)] = stat_idx(T, L, ESTS[e], rngL)
    lad_rows = []
    for p in PANELS:
        spv = SPYR[p].values
        for e in ESTS:
            for f in LAD6:
                idx = LAD_IDX[(p, f, e)]
                s0 = sharpe_vec(spv, idx)
                se_spy = float(np.std(s0, ddof=1))
                lad_rows.append(dict(panel=p, est=e, frac=f, L=idx.shape[1], obj="SPY",
                                     se_COMP=se_spy, se_PAIRED=np.nan, se_BOOKONLY=np.nan))
                for nm in SHELF[p]:
                    sj = sharpe_vec(SHNET[nm].values, idx)
                    lad_rows.append(dict(panel=p, est=e, frac=f, L=idx.shape[1], obj=nm,
                                         se_COMP=se_spy,          # 1012's own convention
                                         se_PAIRED=float(np.std(sj - s0, ddof=1)),
                                         se_BOOKONLY=float(np.std(sj, ddof=1))))
    LADDF = pd.DataFrame(lad_rows)
    dump(LADDF, "ladder")

    def exps_from(df):
        """The three 1012 headline exponents from a ladder frame, its own conventions."""
        out = {}
        for p in PANELS:
            s = df[(df.panel == p) & (df.est == EST_HEAD) & (df.obj == "SPY")].sort_values("frac")
            out[("SPY", p)] = fitb(s.L.values, s.se_COMP.values)
            bb = []
            for nm in SHELF[p]:
                q = df[(df.panel == p) & (df.est == EST_HEAD) & (df.obj == nm)].sort_values("frac")
                bb.append(fitb(q.L.values, q.se_PAIRED.values))
            out[("BOOK", p)] = float(np.nanmedian(bb)) if bb else np.nan
        return out

    myexp = exps_from(LADDF)
    spy_b = float(np.median([myexp[("SPY", p)] for p in PANELS]))
    book_b = float(np.median([myexp[("BOOK", p)] for p in PANELS]))

    # the i.i.d. synthetic control, 1012's G9 verbatim
    rg9 = np.random.default_rng(SEED_1012 + 9)
    x9 = rg9.normal(0.0004, 0.01, NFULL["U56"])
    l9, s9 = [], []
    for f in LAD6:
        L = int(round(f * len(x9)))
        i9 = stat_idx(len(x9), L, 1, np.random.default_rng(SEED_1012 + 900 + int(f * 1000)))
        l9.append(L)
        s9.append(float(np.std(sharpe_vec(x9, i9), ddof=1)))
    iid_b = fitb(l9, s9)

    d4a = np.nan
    if PUB_1012.exists():
        pub = pd.read_csv(PUB_1012)
        mine = LADDF.set_index(["panel", "est", "frac", "obj"])
        dmax = 0.0
        n_cmp = 0
        for _, r in pub.iterrows():
            key = (r.panel, r.est, float(r.frac), r.obj)
            if key not in mine.index:
                continue
            m = mine.loc[key]
            for col in ("se_COMP", "se_PAIRED", "se_BOOKONLY"):
                a, b = r.get(col, np.nan), m[col]
                if np.isfinite(a) and np.isfinite(b):
                    dmax = max(dmax, abs(float(a) - float(b)))
                    n_cmp += 1
        d4a = dmax
        P(f"  G4 ladder cross-run: {n_cmp:,} committed SE cells compared, max|d| {d4a:.3e}")
    d4b = max(abs(spy_b - PUB_EXP["1012_SPY_COMP"]), abs(book_b - PUB_EXP["1012_MEDBOOK_PAIRED"]),
              abs(iid_b - PUB_EXP["1012_IID_CONTROL"]))
    gates["G4"] = (np.isfinite(d4a) and d4a < 1e-9 and d4b < 1e-3,
                   f"1012 ladder max|d| {d4a:.2e}; exponents SPY {spy_b:.4f} vs "
                   f"{PUB_EXP['1012_SPY_COMP']}, median book {book_b:.4f} vs "
                   f"{PUB_EXP['1012_MEDBOOK_PAIRED']}, i.i.d. control {iid_b:.4f} vs "
                   f"{PUB_EXP['1012_IID_CONTROL']}; max|d| {d4b:.2e}")

    # ---- G5 determinism of the interval machinery (one cheap object, twice)
    def redraw_b(p, est, seed, n=N_BOOT):
        rng = np.random.default_rng(seed)
        Ls, se0, _ = ladder_ses([SPYR[p].values], NFULL[p], rng, est, n=n)
        return fitb(Ls, se0)

    g5a, g5b = redraw_b("U56", EST_HEAD, SEED0 + 7), redraw_b("U56", EST_HEAD, SEED0 + 7)
    gates["G5"] = (g5a == g5b, f"interval machinery determinism: b {g5a:.6f} twice, |d| "
                               f"{abs(g5a-g5b):.1e}")

    # ---- G6 estimator validation on a ZERO-TRUTH synthetic control
    P(f"  G6: {NCTL} independent zero-truth control tapes ...")
    rgc = np.random.default_rng(SEED0 + 11)
    T0 = NFULL["U56"]
    ctl_b = []
    for i in range(NCTL):
        xc = rgc.normal(0.0004, 0.01, T0)
        Ls, se0, _ = ladder_ses([xc], T0, np.random.default_rng(SEED0 + 2000 + i), "IID", n=200)
        ctl_b.append(fitb(Ls, se0))
    ctl_b = np.array(ctl_b)
    ctl_med = float(np.median(ctl_b))
    ctl_lo, ctl_hi, ctl_w = pct_interval(ctl_b)
    # the TAPE interval built on ONE control tape, same draw count
    xc1 = np.random.default_rng(SEED0 + 12).normal(0.0004, 0.01, T0)
    one_b = []
    for i in range(NREP):
        rr = np.random.default_rng(SEED0 + 3000 + i)
        ii = block_tape(xc1, T0, rr, block=1)
        Ls, se0, _ = ladder_ses([xc1[ii]], T0, rr, "IID", n=200)
        one_b.append(fitb(Ls, se0))
    one_lo, one_hi, one_w = pct_interval(one_b)
    rat6 = one_w / ctl_w if ctl_w else np.inf
    gates["G6"] = (abs(ctl_med + 0.5) <= 0.01 and (1 / BAR_BASIS) <= rat6 <= BAR_BASIS,
                   f"zero-truth control: median b {ctl_med:.4f} (truth -0.5); across-tape "
                   f"{CONF:.0%} spread {ctl_w:.4f} [{ctl_lo:.4f}, {ctl_hi:.4f}]; one-tape TAPE "
                   f"interval {one_w:.4f}; ratio {rat6:.3f}")

    # ---- G7 CENSUS STAMP (1019's proposed clause, honoured)
    files_all = corpus_files("ALL")
    man = []
    for f in files_all:
        bb = f.read_bytes()
        man.append((str(f.relative_to(ROOT)), len(bb), hashlib.sha256(bb).hexdigest()))
    man.sort()
    flsha = hashlib.sha256("\n".join(f"{a}\t{b}\t{c}" for a, b, c in man).encode()).hexdigest()
    try:
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        head = "UNKNOWN"
    tot_bytes = sum(b for _, b, _ in man)
    Path(f"{OUT}.stamp.txt").write_text(
        f"# census stamp for {OUT.name} (idea 1019's proposed PROTOCOL rule 5 clause)\n"
        f"HEAD\t{head}\nfiles\t{len(man)}\nbytes\t{tot_bytes}\nfile_list_sha\t{flsha}\n"
        + "".join(f"{a}\t{b}\t{c}\n" for a, b, c in man))
    gates["G7"] = (len(man) > 0, f"stamp written: {len(man):,} files, {tot_bytes:,} bytes, "
                                 f"file_list_sha {flsha[:16]}, HEAD {head[:10]}")

    # ---- the census itself (needed by G8)
    CL = {}
    for cs in CLAIMSETS:
        CL[cs] = harvest(corpus_files(cs))
    rng8 = np.random.default_rng(SEED0 + 13)
    shuf = list(corpus_files("ALL"))
    rng8.shuffle(shuf)
    alt = harvest(shuf)
    key_cols = ["file", "sent_i", "defn", "keyword", "kind", "res_ctx"]
    a1 = CL["ALL"][key_cols].astype(str).apply(tuple, axis=1).sort_values().tolist()
    a2 = alt[key_cols].astype(str).apply(tuple, axis=1).sort_values().tolist()
    gates["G8"] = (a1 == a2, f"claim extraction order-independent: {len(a1):,} rows, "
                             f"{'identical' if a1 == a2 else 'DIFFER'}")

    def audit_key(r):
        return (Path(r.file).name, r.res_ctx, round(float(r.value), 4))

    hits = CL["ALL"][(CL["ALL"].defn == DEF_HEAD) & (CL["ALL"].kind == "K1_VALUED")
                     & (CL["ALL"].res_ctx.isin(["R2_SE", "R3_NULL"]))]
    aud_rows, missing = [], []
    for _, r in hits.iterrows():
        k = audit_key(r)
        if k not in AUDIT:
            missing.append(k)
        ok, why = AUDIT.get(k, (False, "NOT IN THE AUDIT TABLE — gate G9 fails"))
        aud_rows.append(dict(file=r.file, res_ctx=r.res_ctx, value=r.value, counts=ok,
                             reason=why, text=r.text[:200]))
    AUD = pd.DataFrame(aud_rows)
    AUDKEYS = {audit_key(r) for _, r in hits.iterrows()
               if AUDIT.get(audit_key(r), (False, ""))[0]}
    gates["G9"] = (len(missing) == 0 and len(AUDIT) == len(hits),
                   f"AUDIT COVERAGE: {len(hits)} classifier hits, {len(AUDIT)} adjudicated rows, "
                   f"{len(missing)} unadjudicated; {len(AUDKEYS)} survive the audit rule")

    gp = 0
    for k in sorted(gates):
        ok, msg = gates[k]
        gp += int(ok)
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"  GATES: {gp} of {len(gates)} PASS")
    dump(pd.DataFrame([dict(gate=k, verdict="PASS" if gates[k][0] else "FAIL", detail=gates[k][1])
                       for k in sorted(gates)]), "gates")

    # ================================================================ (A) THE CENSUS
    P("")
    P("=" * 100)
    P("A. THE CENSUS — every committed exponent / scaling / slope claim, and what width it states")
    P("=" * 100)
    ALLCL = CL["ALL"].copy()
    ALLCL["claimset"] = np.where(
        ALLCL.file.isin([str(p.relative_to(ROOT)) for p in corpus_files("REC")]), "REC",
        np.where(ALLCL.file.isin([str(p.relative_to(ROOT)) for p in corpus_files("REC+MEMO")]),
                 "REC+MEMO", "ALL"))
    dump(ALLCL, "claims")

    dump(AUD, "audit")

    def audited_count(v):
        return int(sum(1 for _, r in v.iterrows()
                       if r.res_ctx in ("R2_SE", "R3_NULL") and audit_key(r) in AUDKEYS))

    cen = []
    for cs in CLAIMSETS:
        d = CL[cs]
        for defn in DEFS:
            s = d[d.defn == defn]
            v = s[s.kind == "K1_VALUED"]
            row = dict(claimset=cs, defn=defn, n_files=len(corpus_files(cs)), n_claims=len(s),
                       n_valued=len(v), n_qual=len(s) - len(v))
            for lev in ["R3_NULL", "R2_SE", "R1_SPREAD", "R0_NONE"]:
                row[f"val_{lev}"] = int((v.res_ctx == lev).sum())
                row[f"val_{lev}_sent"] = int((v.res_sent == lev).sum())
            row["n_audited_true"] = audited_count(v)
            row["share_audited"] = row["n_audited_true"] / max(1, len(v))
            row["share_stated"] = (row["val_R3_NULL"] + row["val_R2_SE"]) / max(1, len(v))
            row["share_stated_sent"] = (row["val_R3_NULL_sent"] + row["val_R2_SE_sent"]) \
                / max(1, len(v))
            cen.append(row)
    CEN = pd.DataFrame(cen)
    dump(CEN, "census")
    P("")
    for line in CEN[["claimset", "defn", "n_files", "n_claims", "n_valued", "val_R3_NULL",
                     "val_R2_SE", "val_R1_SPREAD", "val_R0_NONE", "share_stated",
                     "share_stated_sent", "n_audited_true", "share_audited"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P("")
    P("  RESOLUTION taxonomy is FIXED (not a dial): R3_NULL a null/bootstrap interval with a")
    P("  stated confidence level; R2_SE a standard error or +/-; R1_SPREAD a range ACROSS CELLS")
    P("  (a dispersion, NOT a resolution); R0_NONE nothing.  res_ctx scopes the claim's sentence")
    P("  plus its two neighbours; res_sent is the sentence alone (both published).")
    P("")
    P(f"  THE AUDIT — every one of the {len(AUD)} R2_SE/R3_NULL hits in the ALL corpus, "
      f"adjudicated against ONE declared rule (the width must be on the EXPONENT'S OWN VALUE); "
      f"{int(AUD.counts.sum())} survive:")
    for _, r in AUD.iterrows():
        P(f"    {'COUNTS ' if r.counts else 'REJECT '} {Path(r.file).name[:58]:<58} "
          f"{r.value:>9.4f}  {r.reason}")
    smp = CL[CS_HEAD][(CL[CS_HEAD].defn == DEF_HEAD) & (CL[CS_HEAD].kind == "K1_VALUED")]
    P("")
    P(f"  SAMPLE of the headline claim set ({CS_HEAD} x {DEF_HEAD}, {len(smp)} valued claims) — "
      f"every row is in .claims.csv for line-by-line audit:")
    for _, r in smp.head(12).iterrows():
        P(f"    [{r.res_ctx:<10}] {r.value:>9.4f}  {r.text[:120]}")

    # ================================================================ (B) THE RE-DERIVATION
    P("")
    P("=" * 100)
    P("B. THE RE-DERIVATION — 1012's exponent family, rebuilt, with all three widths")
    P("=" * 100)
    P(f"  ladder LAD6 {LAD6} x {N_BOOT:,} draws x {list(ESTS)} x {PANELS}, "
      f"{NREP} reps per resampling basis.")

    iv_rows = []
    # --- OLS basis: from the already-built ladder
    for p in PANELS:
        for e in ESTS:
            s = LADDF[(LADDF.panel == p) & (LADDF.est == e) & (LADDF.obj == "SPY")] \
                .sort_values("frac")
            b, lo, hi, seb = fit_ols_ci(s.L.values, s.se_COMP.values)
            iv_rows.append(dict(obj="SPY_COMP", panel=p, est=e, basis="OLS", b=b, lo=lo, hi=hi,
                                width=hi - lo, seb=seb))
            bb, ww = [], []
            for nm in SHELF[p]:
                q = LADDF[(LADDF.panel == p) & (LADDF.est == e) & (LADDF.obj == nm)] \
                    .sort_values("frac")
                bq, lq, hq, sq = fit_ols_ci(q.L.values, q.se_PAIRED.values)
                bb.append(bq)
                ww.append(hq - lq)
            if bb:
                mb, mw = float(np.median(bb)), float(np.median(ww))
                iv_rows.append(dict(obj="MEDBOOK_PAIRED", panel=p, est=e, basis="OLS", b=mb,
                                    lo=mb - mw / 2, hi=mb + mw / 2, width=mw, seb=np.nan))
    # --- REDRAW and TAPE bases
    REP_ESTS = [EST_HEAD]        # the two resampling bases run at the HEADLINE estimator only
    for basis in ["REDRAW", "TAPE"]:
        P(f"  {basis}: {NREP} reps x {len(PANELS)} panels x {len(REP_ESTS)} estimator "
          f"({EST_HEAD}) — the resampling bases are priced at the headline estimator only; OLS "
          f"is published at all {len(ESTS)}.")
        for p in PANELS:
            spv = SPYR[p].values
            bookv = [SHNET[nm].values for nm in SHELF[p]]
            T = NFULL[p]
            acc = {e: [] for e in REP_ESTS}
            accbk = {e: [] for e in REP_ESTS}
            for i in range(NREP):
                rr = np.random.default_rng(SEED0 + (0 if basis == "REDRAW" else 500000)
                                           + 97 * i + (0 if p == "U56" else 7))
                if basis == "TAPE":
                    ii = block_tape(spv, T, rr, block=BLOCK_TAPE)
                    cols = [spv[ii]] + [b[ii] for b in bookv]
                else:
                    cols = [spv] + bookv
                if i % 25 == 0:
                    P(f"    {basis} {p} rep {i}/{NREP}  ({time.time()-t0:.0f}s)")
                for e in REP_ESTS:
                    Ls, se0, sep = ladder_ses(cols, T, rr, e)
                    acc[e].append(fitb(Ls, se0))
                    bb = [fitb(Ls, sp) for sp in sep]
                    accbk[e].append(float(np.nanmedian(bb)) if bb else np.nan)
            for e in REP_ESTS:
                lo, hi, w = pct_interval(acc[e])
                iv_rows.append(dict(obj="SPY_COMP", panel=p, est=e, basis=basis,
                                    b=float(np.median(acc[e])), lo=lo, hi=hi, width=w,
                                    seb=np.nan))
                lo2, hi2, w2 = pct_interval(accbk[e])
                iv_rows.append(dict(obj="MEDBOOK_PAIRED", panel=p, est=e, basis=basis,
                                    b=float(np.nanmedian(accbk[e])), lo=lo2, hi=hi2, width=w2,
                                    seb=np.nan))
    IV = pd.DataFrame(iv_rows)
    dump(IV, "intervals")
    P("")
    for line in IV.sort_values(["obj", "basis", "panel", "est"]).to_string(
            index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)

    head_iv = IV[(IV.obj == "SPY_COMP") & (IV.est == EST_HEAD) & (IV.panel == "U56")]
    W = {r.basis: r.width for _, r in head_iv.iterrows()}
    W_HEAD = W[BASIS_HEAD]
    P("")
    P(f"  HEADLINE (1012's SPY exponent, U56, {EST_HEAD}, {CONF:.0%}): point "
      f"{float(head_iv[head_iv.basis == BASIS_HEAD].b.iloc[0]):.4f}, "
      f"TAPE [{float(head_iv[head_iv.basis == BASIS_HEAD].lo.iloc[0]):.4f}, "
      f"{float(head_iv[head_iv.basis == BASIS_HEAD].hi.iloc[0]):.4f}] width {W['TAPE']:.4f}; "
      f"REDRAW width {W['REDRAW']:.4f}; OLS width {W['OLS']:.4f}.")
    P(f"  The record publishes this number as {PUB_EXP['1012_SPY_COMP']:.4f} with NO width; "
      f"1044's committed comparand for a fitted exponent's own null band is "
      f"{PUB_1044_WIDTH[0]}-{PUB_1044_WIDTH[1]} wide at 90%.")

    # ================================================================ (C) THE 9-CELL GRID
    P("")
    P("=" * 100)
    P("C. THE 9-CELL GRID — CLAIM SET x INTERVAL BASIS (all cells, none selected)")
    P("=" * 100)
    grid = []
    for cs in CLAIMSETS:
        for basis in BASES:
            w = float(W[basis])
            for defn in DEFS:
                v = CL[cs][(CL[cs].defn == defn) & (CL[cs].kind == "K1_VALUED")]
                vals = v.value.values.astype(float)
                res_sqrt = int(np.sum(np.abs(vals + 0.5) > w))       # distinguishable from -0.5
                pairs = 0
                dpairs = 0
                if len(vals) > 1:
                    d = np.abs(vals[:, None] - vals[None, :])
                    iu = np.triu_indices(len(vals), 1)
                    pairs = len(iu[0])
                    dpairs = int(np.sum(d[iu] > w))
                grid.append(dict(claimset=cs, basis=basis, defn=defn, width=w,
                                 n_valued=len(v),
                                 n_stating=int(v.res_ctx.isin(["R2_SE", "R3_NULL"]).sum()),
                                 share_stating=float(v.res_ctx.isin(["R2_SE", "R3_NULL"]).mean())
                                 if len(v) else np.nan,
                                 n_vs_sqrt=res_sqrt,
                                 share_vs_sqrt=res_sqrt / max(1, len(v)),
                                 n_pairs=pairs, n_pairs_distinct=dpairs,
                                 share_pairs_distinct=dpairs / pairs if pairs else np.nan))
    GR = pd.DataFrame(grid)
    dump(GR, "grid")
    P("")
    for line in GR.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P("")
    P("  READ THIS COLUMN CAREFULLY: `width` is MEASURED on the 1012 exponent family and")
    P("  TRANSFERRED to every other claim in the set.  `share_vs_sqrt` and")
    P("  `share_pairs_distinct` are therefore ORDER-OF-MAGNITUDE statements for the transferred")
    P("  rows and re-derivations only for the 1012 rows, which are broken out below.")

    # ================================================================ (D) THE RE-EXPRESSION
    P("")
    P("=" * 100)
    P("D. THE RE-EXPRESSION — every valued claim as point [lo, hi], provenance stated")
    P("=" * 100)
    rex = []
    for nm, pub in sorted(PUB_EXP.items()):
        if nm == "1012_SPY_COMP":
            mine, obj = spy_b, "SPY_COMP"
        elif nm == "1012_MEDBOOK_PAIRED":
            mine, obj = book_b, "MEDBOOK_PAIRED"
        else:
            mine, obj = iid_b, "IID_CONTROL"
        for basis in BASES:
            if obj == "IID_CONTROL":
                w = float(one_w) if basis == BASIS_HEAD else float(W[basis])
                prov = "MEASURED (zero-truth control)" if basis == BASIS_HEAD else "TRANSFERRED"
            else:
                sub = IV[(IV.obj == obj) & (IV.basis == basis) & (IV.est == EST_HEAD)
                         & (IV.panel == "U56")]
                if len(sub) == 0:
                    w, prov = float(W[basis]), "TRANSFERRED"
                else:
                    w, prov = float(sub.width.iloc[0]), "MEASURED"
            rex.append(dict(claim=nm, published=pub, rederived=mine, basis=basis, width=w,
                            lo=mine - w / 2, hi=mine + w / 2, provenance=prov,
                            covers_sqrt=bool(abs(mine + 0.5) <= w / 2),
                            digits_justified=int(max(0, np.floor(-np.log10(max(w / 2, 1e-12))))),
                            published_digits=4))
    REX = pd.DataFrame(rex)
    dump(REX, "rederive")
    P("")
    for line in REX.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)

    # ================================================================ (E) MECHANISM CONTROL
    P("")
    P("=" * 100)
    P("E. REPORTED CONTROL (no bar, not a dial, NOT pre-registered) — where 1044's 0.67-0.73 "
      "comes from")
    P("=" * 100)
    P("  The queue reads 1044's width as a property of THE TAPE.  It is a property of how many")
    P("  REPLICATIONS each ladder rung is averaged over: 1012 reads every rung off 1,000")
    P("  bootstrap draws, 1044 reads its off ONE window per length.  This control walks the draw")
    P("  count k at fixed tape, fixed ladder and fixed basis (TAPE, U56, BLOCK21) by SUBSETTING")
    P("  the first k of the same 1,000 draws — an exact nesting, no new randomness.  The mapping")
    P("  to 1044 is an ANALOGY (a different estimator), so this control is reported, never scored.")
    spv = SPYR["U56"].values
    Tu = NFULL["U56"]
    kacc = {k: [] for k in DRAWS_CTL}
    for i in range(NREP):
        rr = np.random.default_rng(SEED0 + 900000 + 31 * i)
        ii = block_tape(spv, Tu, rr, block=BLOCK_TAPE)
        tape = spv[ii]
        Ls, S = [], []
        for f in LAD6:
            L = max(40, int(round(f * Tu)))
            idx = stat_idx(Tu, L, ESTS[EST_HEAD], rr, n=N_BOOT)
            Ls.append(L)
            S.append(sharpe_vec(tape, idx))
        for k in DRAWS_CTL:
            kacc[k].append(fitb(Ls, [float(np.std(x[:k], ddof=1)) for x in S]))
    krows = []
    for k in DRAWS_CTL:
        lo, hi, w = pct_interval(kacc[k])
        krows.append(dict(draws_per_rung=k, b_median=float(np.nanmedian(kacc[k])), lo=lo, hi=hi,
                          width=w, vs_1044_lo=w / PUB_1044_WIDTH[0], vs_1044_hi=w / PUB_1044_WIDTH[1]))
    KC = pd.DataFrame(krows)
    dump(KC, "drawctl")
    P("")
    for line in KC.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P("")
    P(f"  1044's committed comparand: 0.67-0.73 wide at 90%, one window per length.")

    # ================================================================ HYPOTHESES
    P("")
    P("=" * 100)
    P("HYPOTHESES (bars fixed before any number above the gates was read)")
    P("=" * 100)
    H = {}
    vhead = CL[CS_HEAD][(CL[CS_HEAD].defn == DEF_HEAD) & (CL[CS_HEAD].kind == "K1_VALUED")]
    n_stat = int(vhead.res_ctx.isin(["R2_SE", "R3_NULL"]).sum())
    sh_stat = n_stat / max(1, len(vhead))
    n_aud = audited_count(vhead)
    H["H_ANY"] = (sh_stat >= BAR_ANY,
                  f"{CS_HEAD}/{DEF_HEAD}: {n_stat} of {len(vhead)} valued exponent claims raise "
                  f"an SE/null-interval flag = {sh_stat:.4f} (bar >= {BAR_ANY}); AFTER THE AUDIT "
                  f"{n_aud} of {len(vhead)} = {n_aud/max(1,len(vhead)):.4f}; R1_SPREAD "
                  f"{int((vhead.res_ctx == 'R1_SPREAD').sum())} (a dispersion, not a resolution), "
                  f"R0_NONE {int((vhead.res_ctx == 'R0_NONE').sum())}.  Corpus-wide the audit "
                  f"leaves {int(AUD.counts.sum())} of "
                  f"{len(CL['ALL'][(CL['ALL'].defn == DEF_HEAD) & (CL['ALL'].kind == 'K1_VALUED')])}"
                  f" valued claims stating a width on the exponent's own value")
    H["H_RESOLVE"] = (W_HEAD <= BAR_RESOLVE,
                      f"headline {BASIS_HEAD} width {W_HEAD:.4f} (bar <= {BAR_RESOLVE})")
    rat = max(W.values()) / min(W.values())
    H["H_BASIS"] = (rat <= BAR_BASIS,
                    f"widths TAPE {W['TAPE']:.4f} / REDRAW {W['REDRAW']:.4f} / OLS "
                    f"{W['OLS']:.4f}; max/min {rat:.2f} (bar <= {BAR_BASIS})")
    pubs = [PUB_EXP[k] for k in sorted(PUB_EXP)]
    pd_ = [abs(a - b) for i, a in enumerate(pubs) for b in pubs[i + 1:]]
    H["H_SAME"] = (all(d > W_HEAD for d in pd_),
                   f"pairwise |d| of the record's three published exponents "
                   f"{[round(d, 4) for d in pd_]} vs headline width {W_HEAD:.4f}: "
                   f"{sum(d > W_HEAD for d in pd_)} of {len(pd_)} distinguishable")
    tap = IV[(IV.basis == BASIS_HEAD) & (IV.obj == "SPY_COMP")]
    out_sqrt = int(np.sum((tap.lo > -0.5) | (tap.hi < -0.5)))
    H["H_SQRT"] = (out_sqrt >= 1,
                   f"-0.5 outside the {CONF:.0%} {BASIS_HEAD} interval in {out_sqrt} of "
                   f"{len(tap)} re-derived (panel x estimator) exponents")
    H["H_DIGIT"] = (W_HEAD <= BAR_DIGIT,
                    f"headline width {W_HEAD:.4f} vs {BAR_DIGIT} needed for the 4 decimals the "
                    f"record prints; digits justified "
                    f"{int(max(0, np.floor(-np.log10(max(W_HEAD/2, 1e-12)))))}")
    hp = 0
    for k in ["H_ANY", "H_RESOLVE", "H_BASIS", "H_SAME", "H_SQRT", "H_DIGIT"]:
        ok, msg = H[k]
        hp += int(ok)
        P(f"  {k:<10} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"  HYPOTHESES: {hp} of {len(H)} PASS")
    dump(pd.DataFrame([dict(hyp=k, verdict="PASS" if H[k][0] else "FAIL", detail=H[k][1])
                       for k in H]), "hypotheses")

    # ================================================================ RULE 8 + BOTH KEEP PATHS
    P("")
    P("=" * 100)
    P(f"RULE 8 WALK-FORWARD — PROTOCOL's declared split {REC_END}; IS 2009-2016 ALONE chooses, "
      f"2017-2026 read ONCE")
    P("=" * 100)
    lrows = []
    for nm, b in pool.items():
        p = b["panel"]
        for c in RUNGS:
            bk = split_block(NET[(nm, c)], REC_END)
            lg = legs_at(bk, SPYB[p])
            v2 = V2[(p, c)]
            lrows.append(dict(book=nm, panel=p, cost=c, **bk, **lg, pass4b=all(lg.values()),
                              pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                          and bk["MaxDD"] >= v2["MaxDD"])))
    LAD = pd.DataFrame(lrows).set_index("book")
    dump(LAD.reset_index(), "keeppaths")
    wf = []
    for p in PANELS:
        for c in RUNGS:
            sub = LAD[(LAD.panel == p) & (LAD.cost == c)]
            for ch in RAW_CH:
                pick = raw_pick(sub, ch, SPYIS[p])
                r = sub.loc[pick]
                s, v2 = SPYB[p], V2[(p, c)]
                wf.append(dict(panel=p, cost=c, chooser=ch, pick=pick,
                               OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                               OOS_MaxDD=r.OOS_MaxDD, spy_OOS_CAGR=s["OOS_CAGR"],
                               spy_OOS_Sharpe=s["OOS_Sharpe"], spy_OOS_MaxDD=s["OOS_MaxDD"],
                               v2_OOS_CAGR=v2["OOS_CAGR"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                               v2_OOS_MaxDD=v2["OOS_MaxDD"], H1=r.H1, H2=r.H2, MaxDD=r.MaxDD,
                               pass4b=bool(r.pass4b), pass4a=bool(r.pass4a)))
    WF = pd.DataFrame(wf)
    dump(WF, "rule8")
    P("")
    for line in WF.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P(f"\n  OOS 4b {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a {int(WF.pass4a.sum())} of "
      f"{len(WF)}.  Full-sample ladder: 4b {int(LAD.pass4b.sum())} of {len(LAD)}, 4a "
      f"{int(LAD.pass4a.sum())} of {len(LAD)}.")
    best = WF.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P(f"  Best pick by OOS Sharpe: {best['pick']} ({best.panel}, {best.cost:.0f} bps, "
      f"{best.chooser}) {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.2%}")
    for p in PANELS:
        s, v = SPYB[p], V2[(p, RUNG_HEAD)]
        P(f"  {p}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:.2%};  "
          f"RULES v2 live @10 bps full {v['CAGR']:.2%} / {v['Sharpe']:.4f} / {v['MaxDD']:.2%} "
          f"(halves {v['H1']:.3f} / {v['H2']:.3f}), OOS {v['OOS_CAGR']:.2%} / "
          f"{v['OOS_Sharpe']:.4f} / {v['OOS_MaxDD']:.2%}")
    P("  NOTHING PROMOTED: every pick is a GRID ladder book the record already holds, and this "
      "run's question moves no price verdict.")

    P("")
    P(f"# done in {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.log.txt")


if __name__ == "__main__":
    main()
