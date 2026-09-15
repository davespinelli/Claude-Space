#!/usr/bin/env python3
"""Idea 871 - "should-PROTOCOL-require-a-RUN-LENGTH-MATCHED-null-by-name" (lane B, 2026-09-15).

The finding this run exists to adjudicate
------------------------------------------
Idea 815 priced five placebo kinds against the same 3,456 real gate arms and found the two
ORIGINAL kinds - idea 602/606's RAND and BLOCK - are not measuring the same thing at all:

    RAND    excess +0.17 .. +0.25   share>0 = 1.000 on ALL EIGHT gate families
    BLOCK   excess +0.01 .. +0.07   share>0 = 0.16 .. 0.98

815's reading was mechanical: RAND scatters the de-grossed days as ISOLATED singletons, so the
placebo path switches ~2x per firing day instead of ~2x per RUN, and at 10 bps it pays a switch
cost the real arm never pays.  On that reading RAND is not an information-free twin of the real
arm - it is a turnover surcharge, and every "excess" measured against it is that surcharge plus
whatever signal there is.

If that is right, PROTOCOL has a hole: it names a placebo's RATE ("rate-matched") nowhere and
its RUN LENGTHS nowhere, so a future idea may pick RAND and publish a number that is ~0.20 of
Sharpe larger than the same claim priced against BLOCK.  This run asks whether PROTOCOL should
name a matched statistic, and WHICH ONE, in a way that can come back either way.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (CENSUS)   How many committed placebo-differenced claims in the record name RAND, name
                  BLOCK, name both, or name no kind at all?  What is the exposure?
    Q2 (COST)     Is the RAND-minus-BLOCK gap a SWITCH-COST artefact?  It is priced at
                  0 / 10 / 25 bps.  If it collapses at 0 bps, the defect is cost accounting and
                  the matched statistic PROTOCOL needs is a TURNOVER statistic.  If it survives
                  at 0 bps, run-length mismatch changes the return path itself and the matched
                  statistic has to be the run-length distribution.
    Q3 (WHICH)    Two NEW rate-matched nulls separate the candidate statistics:
                    RUNPERM      exact multiset of run lengths, exact switch count, calendar
                                 placement destroyed.  If RUNPERM == BLOCK, the RUN-LENGTH
                                 DISTRIBUTION is the sufficient matched statistic and BLOCK's
                                 extra property (the run ORDER) is not needed.
                    SWITCHMATCH  exact firing-day count and exact NUMBER OF RUNS, run lengths
                                 redrawn as a random composition.  If SWITCHMATCH == BLOCK too,
                                 the SWITCH COUNT ALONE is sufficient and PROTOCOL should name
                                 the cheaper thing.
    Q4 (MECHANISM) Is the per-arm excess a monotone read of the placebo's own switch-count
                  ratio, and only at non-zero cost?
    Q5 (RULE 8 + BOOKS)  Does the gap walk forward (IS-fitted -> OOS-read)?  And do the real
                  BOOKS behind these arms clear either PROTOCOL KEEP path with parameters
                  chosen on 2009-2016 only?

Pre-registered hypotheses and bars (fixed before any number below section [0] was read)
    H_COST    The pooled median (RAND excess - BLOCK excess) at 0 bps is <= 50% of its value at
              10 bps.  PASS = the gap is mostly switch cost.
    H_ZERO    That 0 bps pooled median gap is <= 0.02 in Sharpe.  PASS = switch cost explains
              essentially ALL of it and nothing else needs naming.
    H_RUNMATCH  Pooled median |RUNPERM excess - BLOCK excess| <= 0.02 at EVERY cost rung.
              PASS = the run-length distribution is a sufficient matched statistic.
    H_SWITCH  Pooled median |SWITCHMATCH excess - BLOCK excess| <= 0.02 at EVERY cost rung.
              PASS = the switch COUNT alone is sufficient (a strictly weaker requirement to
              write into PROTOCOL than the full distribution).
    H_MECH    Spearman(placebo switch-count ratio, placebo excess) pooled >= +0.50 at 10 bps
              AND < +0.20 at 0 bps.  PASS = the excess is the turnover surcharge and nothing
              else.
    H_WF      Spearman(IS gap, OOS gap) per family >= +0.30 in >= 6 of 8 families.  PASS = the
              gap is a stable mechanical property of the null, not a window accident - which is
              what justifies naming it in PROTOCOL rather than re-measuring per idea.
  A FAIL on any of these is a result and is printed as one.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. claim set   which gate family the arm belongs to: BREADTH / VOL20 / DISP / CORR, each in
                   BOTH directions.  Both directions are ALWAYS reported, never selected on.
    2. null        RAND / BLOCK (idea 602/606's two) + RUNPERM / SWITCHMATCH (this run's two
                   matched-statistic probes).
    ALL grid points reported at every panel / level q / window w / depth / cadence / gross /
    cost rung.  Nothing is chosen on the answer.

Reported axes, NEVER tuned or selected on (inherited from idea 606/602/815 verbatim)
    level q 0.07 / 0.12 / 0.17    w 252 / 504 / 1008 / 2016    depth 0.25 / 0.50 / 1.00
    cadence D / W                 gross 0.75 / 1.00            cost 0 / 10 / 25 bps
    panel   U56 / B136 / SMALL

The four nulls, all firing-rate-matched and information-free by construction
    RAND         iid days, EXACTLY the real arm's de-grossed day count.  Run lengths are
                 geometric-ish singletons; the switch count explodes.          (idea 602/606)
    BLOCK        circular shift of the whole effective path: exact rate, exact run-length
                 multiset, exact switch count, exact run ORDER, no calendar
                 alignment.                                                    (idea 602/606)
    RUNPERM      the real path's run-length decomposition with the fire runs and the interior
                 gap runs INDEPENDENTLY PERMUTED and re-assembled: exact rate, exact run-length
                 multiset, exact switch count, run ORDER destroyed.                     (NEW)
    SWITCHMATCH  exact firing-day count k and exact number of fire runs m, but the m run
                 lengths are a uniform random composition of k and the m+1 gaps a uniform
                 random composition of n-k: exact rate, exact switch count, run-length
                 DISTRIBUTION destroyed.                                                (NEW)

    So the four differ in exactly the properties the candidate PROTOCOL clauses would name:
                      rate   switch count   run-length multiset   run order   calendar
        RAND           y          n                 n                 n          n
        SWITCHMATCH    y          y                 n                 n          n
        RUNPERM        y          y                 y                 n          n
        BLOCK          y          y                 y                 y          n

Reproduction gates (section [0], printed before any new number is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.
    G2  every null's mean effective multiplier equals the real arm's, so the matched-gross twin
        cancels and excess = Sharpe(real) - Sharpe(placebo) with the twin term identically 0.
    G3  idea 815's committed RAND-vs-BLOCK headline (+0.17..+0.25 / share>0 = 1.000 on all
        eight vs +0.01..+0.07), rebuilt here.
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  CONSTRUCTION gate: RUNPERM's sorted run-length multiset is IDENTICAL to the real arm's,
        and SWITCHMATCH's run COUNT is identical while its multiset is not.  This is what makes
        Q3 a test of the named statistic rather than of a coincidence.
        HONEST NOTE ON THIS GATE: its first draft scored SWITCHMATCH's "multiset must differ"
        leg on iid-Bernoulli synthetic paths only, where almost every fire run has length 1 and
        {1,...,1} is the ONLY composition of k into m parts - so SWITCHMATCH is RUNPERM by force
        and the leg read 18.4% same-multiset (a FAIL) for a reason that is a property of the
        test population, not of the code.  The gate now (a) draws half its paths block-structured,
        (b) scores that leg on NON-DEGENERATE paths only, and (c) prints the degenerate share
        rather than hiding it.  Section [2] reports the same share for the REAL arms and section
        [3] repeats H_RUNMATCH / H_SWITCH on the non-degenerate arms alone, because that subset
        is the honest scope of any claim that prefers one clause to the other.  The three
        arithmetic legs of G5 (firing-day count, RUNPERM multiset, SWITCHMATCH run count) passed
        at 0 violations in both drafts and are unchanged.
    G6  the fast Sharpe used on the placebo cells equals engine.metrics()["Sharpe"].

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: all three panels are current-constituent lists (the small panel additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so CAGR and drawdown
LEVELS are optimistic throughout; the null-vs-null DIFFERENCES this run is about are computed
on one fixed real arm at a time and are the durable part.

Deterministic (all placebo seeds md5-derived), standalone.  Modifies nothing.
"""
import hashlib
import re
import sys
import time
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
LINES = []

FREQ = "W"
MAX_VOL = 0.60
SMOOTH = 20
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
GROSSES = [0.75, 1.00]
RUNGS = [0, 10, 25]
STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"), "CORR": ("HI", "LO")}
KINDS = ["RAND", "SWITCHMATCH", "RUNPERM", "BLOCK"]
NSEED = 10
SPLIT = "2017-01-01"

# idea 815's committed RAND/BLOCK headline (pooled), the object G3 prices
IDEA815 = {"RAND_lo": 0.17, "RAND_hi": 0.25, "BLOCK_lo": 0.01, "BLOCK_hi": 0.07}


def log(s=""):
    print(s)
    LINES.append(str(s))


# ------------------------------------------------------------------ primitives (idea 602/606)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def state_breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    """20d average pairwise correlation, equal-weight index-vs-name variance identity."""
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def gate_mult(st, thr, side, depth, cadence, idx):
    """Fire (de-gross to 1-depth) when the state is in its named tail; 1.0 before the rolling
    threshold exists.  LO fires on st < thr, HI on st > thr.  idea 606 verbatim."""
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path with idea 399's switch cost."""
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def nswitch(m_eff):
    return int((np.abs(np.diff(np.asarray(m_eff, float), prepend=m_eff[0])) > 0).sum())


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


# --------------------------------------------------------------------------- run decomposition
def runs_of(fire):
    """(fire run lengths, gap run lengths incl. possibly-zero leading/trailing).  Exact
    reconstruction: gaps[0], fires[0], gaps[1], fires[1], ..., gaps[m]."""
    fire = np.asarray(fire, bool)
    n = len(fire)
    d = np.diff(fire.astype(np.int8))
    starts = np.flatnonzero(d == 1) + 1
    ends = np.flatnonzero(d == -1) + 1
    if fire[0]:
        starts = np.r_[0, starts]
    if fire[-1]:
        ends = np.r_[ends, n]
    if len(starts) == 0:
        return np.array([], int), np.array([n], int)
    fl = (ends - starts).astype(int)
    gl = np.empty(len(starts) + 1, int)
    gl[0] = starts[0]
    gl[1:-1] = starts[1:] - ends[:-1]
    gl[-1] = n - ends[-1]
    return fl, gl


def assemble(fl, gl, n):
    out = np.zeros(n, bool)
    p = 0
    for i, f in enumerate(fl):
        p += gl[i]
        out[p:p + f] = True
        p += f
    return out


def permute_gaps(gl, rng):
    """Permute the gap multiset while keeping every zero-length gap at an END slot, so no
    interior gap is ever 0 and the fire-run multiset survives re-assembly untouched."""
    gl = np.asarray(gl, int)
    m1 = len(gl)                       # = (number of fire runs) + 1
    zeros = int((gl == 0).sum())
    pos = rng.permutation(gl[gl > 0])
    out = np.empty(m1, int)
    if zeros == 0:
        return pos
    if zeros >= 2:                     # both ends zero (only two end slots exist)
        out[0] = out[-1] = 0
        out[1:-1] = pos
        return out
    end = 0 if rng.integers(2) == 0 else m1 - 1
    out[end] = 0
    out[[i for i in range(m1) if i != end]] = pos
    return out


def rand_composition(total, parts, rng, min_each):
    """Uniform random composition of `total` into `parts` pieces, each >= min_each."""
    if parts <= 0:
        return np.array([], int)
    rem = total - parts * min_each
    if rem < 0:
        raise ValueError("infeasible composition")
    if parts == 1:
        return np.array([total], int)
    cuts = np.sort(rng.choice(np.arange(rem + parts - 1), size=parts - 1, replace=False))
    pieces = np.diff(np.r_[-1, cuts, rem + parts - 1]) - 1
    return (pieces + min_each).astype(int)


def placebo_eff(m_eff, depth, kind, seed):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff (numpy)."""
    v = np.asarray(m_eff, float)
    n = len(v)
    fire = v < 1.0
    k = int(fire.sum())
    if k == 0 or k == n:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(n)
        out[rng.choice(n, size=k, replace=False)] = 1.0 - depth
        return out
    if kind == "BLOCK":
        return np.roll(v, int(rng.integers(1, n)))
    fl, gl = runs_of(fire)
    m = len(fl)
    if kind == "RUNPERM":
        # Exact multiset of fire runs and of gap runs, both re-ordered independently.
        # A gap of length 0 can only ever be an END gap (an interior 0 would merge the two
        # fire runs it separates and change the multiset), so the zero gaps - at most two, and
        # by construction already at the ends - are pinned to the ends and the positive gaps
        # are permuted freely over every remaining slot.  This preserves BOTH multisets exactly.
        fl2 = rng.permutation(fl)
        gl2 = permute_gaps(gl, rng)
        newfire = assemble(fl2, gl2, n)
        out = np.ones(n)
        out[newfire] = 1.0 - depth
        return out
    if kind == "SWITCHMATCH":
        # exact k and exact run COUNT m; lengths redrawn.  Interior gaps must be >= 1 for the
        # run count to survive, so m-1 units are reserved for them before the composition.
        if (n - k) < (m - 1):
            return np.roll(v, int(rng.integers(1, n)))   # infeasible; fall back (logged by G5)
        gl2 = rand_composition(n - k - (m - 1), m + 1, rng, 0)
        gl2[1:-1] += 1
        fl2 = rand_composition(k, m, rng, 1)
        newfire = assemble(fl2, gl2, n)
        out = np.ones(n)
        out[newfire] = 1.0 - depth
        return out
    raise ValueError(kind)


# ------------------------------------------------------------------------------ metric helpers
def pack(r):
    m = metrics(pd.Series(r) if not isinstance(r, pd.Series) else r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep]


# ======================================================================================= [0]
def gates(panels):
    log("\n[0] REPRODUCTION / CONSTRUCTION GATES (printed before any new number is read)")
    px = panels["U56"]
    core = px.drop(columns=["SPY"], errors="ignore")
    res = backtest(core, ewall_weights(core, 0.75), cost_bps=10, freq=FREQ)
    r_base = res["returns"].loc["2009-01-01":]
    ones = np.ones(len(r_base))
    g1 = float(np.max(np.abs(apply_eff(r_base.values, ones, 0.75, 10) - r_base.values)))
    log(f"  G1 never-firing multiplier == ungated book          max|d| = {g1:.3e}  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]  (bar 1e-12)")
    g6 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G6 fast Sharpe == engine.metrics()['Sharpe']        |d|    = {g6:.3e}  "
        f"[{'PASS' if g6 < 1e-10 else 'FAIL'}]  (bar 1e-10)")

    # G5 construction gate on synthetic + real-shaped paths
    rng = np.random.default_rng(0)
    bad_k = bad_rp = bad_sm = blk_merge = sm_same = nwide = trials = ndegen = 0
    for t in range(1500):
        n = int(rng.integers(200, 900))
        if t % 2 == 0:                       # iid days (the cadence-D, low-rate shape)
            fire = rng.random(n) < rng.uniform(0.01, 0.6)
        else:                                # persistent blocks (the cadence-W shape)
            fire = np.zeros(n, bool)
            p = int(rng.integers(0, 40))
            while p < n:
                run = int(rng.integers(2, 45))
                fire[p:p + run] = True
                p += run + int(rng.integers(2, 60))
        fl, gl = runs_of(fire)
        if len(fl) == 0 or fl.sum() == n:
            continue
        if not np.array_equal(assemble(fl, gl, n), fire):
            bad_rp += 1
        v = np.where(fire, 0.5, 1.0)
        trials += 1
        # DEGENERATE = every fire run has length 1, so {1,...,1} is the ONLY composition of k
        # into m parts and SWITCHMATCH is RUNPERM by force.  Counted, not hidden: the two
        # candidate PROTOCOL clauses are provably indistinguishable on such a path.
        degen = int(fl.sum()) == len(fl)
        ndegen += int(degen)
        wide = (len(fl) >= 5) and not degen
        nwide += int(wide)
        for kind in ("BLOCK", "RUNPERM", "SWITCHMATCH"):
            pe = placebo_eff(v, 0.5, kind, seed_of("G5", t, kind))
            pf = pe < 1.0
            if int(pf.sum()) != int(fire.sum()):
                bad_k += 1
            pfl, _ = runs_of(pf)
            same = np.array_equal(np.sort(pfl), np.sort(fl))
            if kind == "RUNPERM" and not same:
                bad_rp += 1
            if kind == "BLOCK" and not same:
                blk_merge += 1
            if kind == "SWITCHMATCH":
                if len(pfl) != len(fl):
                    bad_sm += 1
                if wide and same:
                    sm_same += 1
    log(f"  G5 every null's firing-day count == real arm's      violations = {bad_k}  "
        f"[{'PASS' if bad_k == 0 else 'FAIL'}]  (bar 0, over {trials} synthetic paths)")
    log(f"     RUNPERM run-length multiset == real arm's        violations = {bad_rp}  "
        f"[{'PASS' if bad_rp == 0 else 'FAIL'}]  (bar 0)")
    log(f"     SWITCHMATCH run COUNT == real arm's              violations = {bad_sm}  "
        f"[{'PASS' if bad_sm == 0 else 'FAIL'}]  (bar 0)")
    log(f"     SWITCHMATCH multiset differs, m>=5 NON-DEGENERATE same = {sm_same} of {nwide}  "
        f"[{'PASS' if sm_same <= 0.05 * max(nwide, 1) else 'FAIL'}]  (bar <=5%; if it matched,")
    log("        SWITCHMATCH would not separate the two candidate PROTOCOL clauses at all)")
    log(f"     MEASURED, not a gate: {ndegen} of {trials} synthetic paths are DEGENERATE (every")
    log("        fire run length 1), where {1,..,1} is the only composition and SWITCHMATCH IS")
    log("        RUNPERM by force.  On such a path the two clauses cannot be told apart at all -")
    log("        the real-arm share of that shape is reported in [2] and is the honest scope of")
    log("        any conclusion below that prefers one clause to the other.")
    log(f"     MEASURED, not a gate: BLOCK's own circular wrap splits or merges a run on "
        f"{blk_merge / max(trials, 1):.1%} of paths,")
    log("        so BLOCK is run-length-matched ONLY up to one wrap point.  RUNPERM is exact.")
    return g1, g6, bad_rp, bad_sm


# ======================================================================================= [1]
def census():
    """Q1 - which committed placebo-differenced claims name which null kind."""
    log("\n[1] CENSUS - which null does the committed record's placebo prose actually name?")
    files = sorted([p for p in (REPO / "research").rglob("*.md")] +
                   [p for p in (REPO / "research").rglob("*.py")])
    pat_claim = re.compile(r"placebo|PLACEBO", re.I)
    kinds = {"RAND": re.compile(r"\bRAND\b"), "BLOCK": re.compile(r"\bBLOCK\b"),
             "YEARBLOCK": re.compile(r"\bYEARBLOCK\b"), "EPISODEFIX": re.compile(r"\bEPISODEFIX\b"),
             "BLOCKPOST": re.compile(r"\bBLOCKPOST\b")}
    rows = []
    for p in files:
        try:
            t = p.read_text(errors="ignore")
        except Exception:
            continue
        if not pat_claim.search(t):
            continue
        d = {"file": str(p.relative_to(REPO)), "kind_sum": p.suffix}
        for k, rx in kinds.items():
            d[k] = len(rx.findall(t))
        # "excess" is the record's word for the placebo-differenced statistic
        d["excess_sites"] = len(re.findall(r"\bexcess\b", t, re.I))
        rows.append(d)
    df = pd.DataFrame(rows)
    if df.empty:
        log("  no placebo-bearing committed files found")
        return df
    df["has_RAND"] = df["RAND"] > 0
    df["has_BLOCK"] = df["BLOCK"] > 0
    n = len(df)
    only_r = int((df["has_RAND"] & ~df["has_BLOCK"]).sum())
    only_b = int((~df["has_RAND"] & df["has_BLOCK"]).sum())
    both = int((df["has_RAND"] & df["has_BLOCK"]).sum())
    neither = int((~df["has_RAND"] & ~df["has_BLOCK"]).sum())
    log(f"  committed files mentioning a placebo        : {n}")
    log(f"    name RAND only (no BLOCK anywhere)        : {only_r:4d}  ({only_r / n:.1%})"
        f"   <- the exposed set: their excess carries the turnover surcharge unpriced")
    log(f"    name BLOCK only                           : {only_b:4d}  ({only_b / n:.1%})")
    log(f"    name BOTH                                 : {both:4d}  ({both / n:.1%})")
    log(f"    name NEITHER (placebo with no kind stated): {neither:4d}  ({neither / n:.1%})"
        f"   <- unadjudicable from the file alone")
    log(f"  'excess' mention sites in RAND-only files   : {int(df.loc[df['has_RAND'] & ~df['has_BLOCK'], 'excess_sites'].sum())}")
    log(f"  'excess' mention sites in files naming BOTH : {int(df.loc[df['has_RAND'] & df['has_BLOCK'], 'excess_sites'].sum())}")
    log("  NOTE: a file naming both kinds is not thereby safe - it is safe only if its HEADLINE")
    log("        number is the BLOCK one.  The census bounds exposure; it does not clear it.")
    return df


# ======================================================================================= run
def run_panel(name, px):
    t0 = time.time()
    idx = px.index
    core = px.drop(columns=["SPY"], errors="ignore")
    spy = px["SPY"].pct_change().fillna(0.0)
    states = {s: STATE_FN[s](core) for s in STATES}

    base = {}
    for g in GROSSES:
        w = ewall_weights(core, g)
        for c in RUNGS:
            base[(g, c)] = backtest(core, w, cost_bps=c, freq=FREQ)["returns"]

    start = idx[260]
    ii = idx[idx >= start]
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos
    RB = {k: v.loc[ii].values for k, v in base.items()}   # hoisted out of the inner loops

    spy_v = spy.loc[ii].values
    spy_c, spy_s, spy_d = pack(pd.Series(spy_v, index=ii))
    spy_h1, spy_h2 = halves(spy_v)
    spy_oc, spy_os, spy_od = pack(pd.Series(spy_v[oos], index=ii[oos]))
    bl = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
    bl_c, bl_s, bl_d = pack(bl)
    bl_h1, bl_h2 = halves(bl.values)
    bl_oc, bl_os, bl_od = pack(bl.loc[ii[oos]])
    bench = dict(panel=name, spy_cagr=spy_c, spy_sh=spy_s, spy_dd=spy_d, spy_h1=spy_h1,
                 spy_h2=spy_h2, spy_oos_c=spy_oc, spy_oos_s=spy_os, spy_oos_d=spy_od,
                 bl_cagr=bl_c, bl_sh=bl_s, bl_dd=bl_d, bl_h1=bl_h1, bl_h2=bl_h2,
                 bl_oos_c=bl_oc, bl_oos_s=bl_os, bl_oos_d=bl_od)

    rows, exrows, g2 = [], [], 0.0
    for st_name in STATES:
        st_full = states[st_name]
        for side in SIDES[st_name]:
            fam = f"{st_name}-{side}"
            for q, w in product(QS, WS):
                thr = st_full.rolling(w, min_periods=max(60, w // 4)).quantile(
                    q if side == "LO" else 1 - q)
                for depth, cad in product(DEPTHS, CADENCES):
                    mult = gate_mult(st_full, thr, side, depth, cad, idx)
                    me = mult.shift(1).fillna(1.0).loc[ii].values
                    fired = me < 1.0
                    rate = float(fired.mean())
                    sw_real = nswitch(me)
                    fl_r, _ = runs_of(fired)
                    nruns = int(len(fl_r))
                    mean_rl = float(fl_r.mean()) if nruns else 0.0
                    degen = bool(nruns and int(fl_r.sum()) == nruns)
                    for g in GROSSES:
                        real = {c: apply_eff(RB[(g, c)], me, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(
                            panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                            depth=depth, cadence=cad, gross=g, rate=rate, nswitch=sw_real,
                            nruns=nruns, mean_runlen=mean_rl, degenerate=degen,
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od,
                            **{f"Sharpe_{c}bps": fast_sharpe(real[c]) for c in RUNGS}))
                        sh_real = {c: fast_sharpe(real[c]) for c in RUNGS}
                        sh_is = {c: fast_sharpe(real[c][isw]) for c in RUNGS}
                        sh_oos = {c: fast_sharpe(real[c][oos]) for c in RUNGS}
                        sd_real = float(fl_r.std(ddof=1)) if nruns > 1 else 0.0
                        for kind in KINDS:
                            acc = {c: [] for c in RUNGS}
                            acc_is, acc_oos, swr = [], [], []
                            same_ms, sd_rat = [], []
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g, kind, sd)
                                pe = placebo_eff(me, depth, kind, seed)
                                g2 = max(g2, abs(pe.mean() - me.mean()))
                                swr.append(nswitch(pe) / max(sw_real, 1))
                                pfl, _ = runs_of(pe < 1.0)
                                same_ms.append(float(len(pfl) == nruns
                                                     and np.array_equal(np.sort(pfl), np.sort(fl_r))))
                                sd_rat.append((float(pfl.std(ddof=1)) / sd_real)
                                              if (len(pfl) > 1 and sd_real > 0) else np.nan)
                                for c in RUNGS:
                                    pr = apply_eff(RB[(g, c)], pe, g, c)
                                    acc[c].append(sh_real[c] - fast_sharpe(pr))
                                    if c == 10:
                                        acc_is.append(sh_is[c] - fast_sharpe(pr[isw]))
                                        acc_oos.append(sh_oos[c] - fast_sharpe(pr[oos]))
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind, rate=rate,
                                nswitch_real=sw_real, sw_ratio=float(np.mean(swr)),
                                nruns=nruns, mean_runlen=mean_rl, degenerate=degen,
                                same_multiset=float(np.mean(same_ms)),
                                sd_runlen_ratio=float(np.nanmean(sd_rat)),
                                **{f"excess_{c}bps": float(np.median(acc[c])) for c in RUNGS},
                                **{f"share_pos_{c}bps": float(np.mean(np.array(acc[c]) > 0))
                                   for c in RUNGS},
                                excess_IS=float(np.median(acc_is)),
                                excess_OOS=float(np.median(acc_oos))))
        log(f"    {name}: {st_name} done  ({time.time() - t0:.0f}s)")

    # G4 determinism: recompute a sample of placebo cells from the same seeds
    d4 = 0.0
    sample = exrows[:8] + exrows[len(exrows) // 2:len(exrows) // 2 + 8]
    for r in sample:
        st_full = states[r["state"]]
        thr = st_full.rolling(r["w"], min_periods=max(60, r["w"] // 4)).quantile(
            r["q"] if r["side"] == "LO" else 1 - r["q"])
        me = gate_mult(st_full, thr, r["side"], r["depth"], r["cadence"], idx
                       ).shift(1).fillna(1.0).loc[ii].values
        rb = RB[(r["gross"], 10)]
        sh = fast_sharpe(apply_eff(rb, me, r["gross"], 10))
        acc = []
        for sd in range(NSEED):
            seed = seed_of(name, r["family"], r["q"], r["w"], r["depth"], r["cadence"],
                           r["gross"], r["kind"], sd)
            pe = placebo_eff(me, r["depth"], r["kind"], seed)
            acc.append(sh - fast_sharpe(apply_eff(rb, pe, r["gross"], 10)))
        d4 = max(d4, abs(float(np.median(acc)) - r["excess_10bps"]))
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, d4


# ======================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 871 - should PROTOCOL require a RUN-LENGTH-MATCHED null BY NAME?  (lane B 2026-09-15)")
    log("=" * 100)
    log(__doc__.split("The four nulls")[0].split("The finding")[0])

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    log(f"panels: U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  "
        f"SMALL {panels['SMALL'].shape} (sub-$2B, max_1d_move>=1.0 dropped)")

    g1, g6, g5a, g5b = gates(panels)
    cen = census()

    # Per-panel checkpoint: this sandbox reclaims long-running processes, so each panel's
    # results are written as soon as they exist and a re-run resumes instead of restarting.
    # Every number is md5-seeded and deterministic, so a resumed run is bit-identical.
    allrows, allex, benches, g2m, g4m = [], [], [], 0.0, 0.0
    for nm, px in panels.items():
        cf = OUT / f"{STEM}.part_{nm}.cells.csv"
        ef = OUT / f"{STEM}.part_{nm}.nulls.csv"
        bf = OUT / f"{STEM}.part_{nm}.bench.csv"
        if cf.exists() and ef.exists() and bf.exists():
            log(f"  [checkpoint] {nm} already computed - loading")
            r, e = pd.read_csv(cf), pd.read_csv(ef)
            bb = pd.read_csv(bf)
            b = bb.iloc[0].to_dict()
            g2, g4 = float(bb["g2"].iloc[0]), float(bb["g4"].iloc[0])
        else:
            r, e, b, g2, g4 = run_panel(nm, px)
            r.to_csv(cf, index=False)
            e.to_csv(ef, index=False)
            pd.DataFrame([{**b, "g2": g2, "g4": g4}]).to_csv(bf, index=False)
        b = {k: v for k, v in b.items() if k not in ("g2", "g4")}
        allrows.append(r); allex.append(e); benches.append(b)
        g2m, g4m = max(g2m, g2), max(g4m, g4)
    cells = pd.concat(allrows, ignore_index=True)
    ex = pd.concat(allex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")

    log(f"\n  G2 placebo mean multiplier == real arm's           max|d| = {g2m:.3e}  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]  (bar 1e-12; if PASS the matched-gross twin "
        f"cancels and excess = Sharpe(real) - Sharpe(placebo))")
    log(f"  G4 determinism, 48 placebo cells re-seeded          max|d| = {g4m:.3e}  "
        f"[{'PASS' if g4m < 1e-12 else 'FAIL'}]  (bar 1e-12)")

    # ------------------------------------------------------------------- G3 reproduction
    log("\n  G3 idea 815's committed RAND-vs-BLOCK headline, rebuilt here (10 bps, per family)")
    log(f"    {'family':12s} {'RAND':>9s} {'shr>0':>7s} {'BLOCK':>9s} {'shr>0':>7s} {'gap':>9s}")
    fams = sorted(ex["family"].unique())
    g3ok = 0
    for f in fams:
        sub = ex[ex["family"] == f]
        r_ = sub[sub["kind"] == "RAND"]
        b_ = sub[sub["kind"] == "BLOCK"]
        rm, bm = r_["excess_10bps"].median(), b_["excess_10bps"].median()
        rs, bs = r_["share_pos_10bps"].mean(), b_["share_pos_10bps"].mean()
        log(f"    {f:12s} {rm:+9.4f} {rs:7.3f} {bm:+9.4f} {bs:7.3f} {rm - bm:+9.4f}")
        if IDEA815["RAND_lo"] - 0.06 <= rm <= IDEA815["RAND_hi"] + 0.06 and rs >= 0.95:
            g3ok += 1
    log(f"    G3: RAND median in 815's [{IDEA815['RAND_lo']:.2f},{IDEA815['RAND_hi']:.2f}] +/-0.06 "
        f"AND share>0 >= 0.95 in {g3ok} of 8 families  "
        f"[{'PASS' if g3ok >= 6 else 'FAIL'}]  (bar >=6 of 8)")

    # ====================================================================== [2] the four nulls
    log("\n[2] THE FOUR NULLS, POOLED OVER ALL 3,456 ARMS x 3 PANELS - median excess (Sharpe)")
    log(f"    {'null':12s} {'sw_ratio':>9s} " + " ".join(f"{'ex@' + str(c) + 'bps':>11s} {'shr>0':>7s}"
                                                          for c in RUNGS))
    pooled = {}
    for k in KINDS:
        s = ex[ex["kind"] == k]
        pooled[k] = {c: s[f"excess_{c}bps"].median() for c in RUNGS}
        line = f"    {k:12s} {s['sw_ratio'].median():9.2f} "
        line += " ".join(f"{s[f'excess_{c}bps'].median():+11.4f} "
                         f"{s[f'share_pos_{c}bps'].mean():7.3f}" for c in RUNGS)
        log(line)

    log("\n  SCOPE - the real arms' own run structure (this is what the nulls have to match)")
    arms = ex[ex["kind"] == "BLOCK"]
    log(f"    arms                                     : {len(arms)}")
    log(f"    median fire runs per arm (m)             : {arms['nruns'].median():.0f}"
        f"   [min {arms['nruns'].min():.0f}, max {arms['nruns'].max():.0f}]")
    log(f"    median mean fire-run LENGTH (days)       : {arms['mean_runlen'].median():.2f}"
        f"   [p10 {arms['mean_runlen'].quantile(0.1):.2f}, p90 {arms['mean_runlen'].quantile(0.9):.2f}]")
    dg = float(arms["degenerate"].mean())
    log(f"    DEGENERATE arms (every fire run length 1): {dg:.2%}"
        f"   <- on these SWITCHMATCH IS RUNPERM by force, so they cannot")
    log("        separate the two candidate clauses; the H_RUNMATCH/H_SWITCH contrast below is")
    log(f"        carried by the remaining {1 - dg:.2%} of arms.")
    log("    by cadence (W persists the gate to weekly rebalances, so its runs are longer):")
    for cad in CADENCES:
        s = arms[arms["cadence"] == cad]
        log(f"      {cad}: median m {s['nruns'].median():6.0f}  median mean run length "
            f"{s['mean_runlen'].median():6.2f}  degenerate {s['degenerate'].mean():6.2%}")

    log("\n  SEPARATION ON THE REAL ARMS - does each matched null do what its name claims?")
    log("  (this is the leg G5's synthetic version could not settle: G5 scored it on short")
    log("   synthetic paths where a same-multiset draw is common; these are the 3,456 REAL arms)")
    log(f"    {'null':12s} {'share draws w/ multiset == real':>32s} {'mean sd(runlen) ratio':>23s}")
    for k in KINDS:
        s = ex[ex["kind"] == k]
        log(f"    {k:12s} {s['same_multiset'].mean():32.4f} {s['sd_runlen_ratio'].mean():23.3f}")
    smx = float(ex[ex["kind"] == "SWITCHMATCH"]["same_multiset"].mean())
    log(f"    -> SWITCHMATCH reproduces the real multiset in {smx:.2%} of draws on real arms, so")
    log("       H_SWITCH vs H_RUNMATCH IS a real contrast here, not a construction coincidence.")

    log("\n  per-family, per-null median excess at 10 bps (ALL grid points behind each median)")
    piv = ex.pivot_table(index="family", columns="kind", values="excess_10bps", aggfunc="median")
    log("    " + piv[KINDS].to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n    "))
    log("\n  per-panel, per-null median excess at 10 bps")
    piv2 = ex.pivot_table(index="panel", columns="kind", values="excess_10bps", aggfunc="median")
    log("    " + piv2[KINDS].to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n    "))
    log("\n  per-cadence x depth, per-null median excess at 10 bps (run length varies most here)")
    piv3 = ex.pivot_table(index=["cadence", "depth"], columns="kind",
                          values="excess_10bps", aggfunc="median")
    log("    " + piv3[KINDS].to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n    "))

    # ====================================================================== [3] hypotheses
    log("\n[3] PRE-REGISTERED HYPOTHESES")
    gap = {c: pooled["RAND"][c] - pooled["BLOCK"][c] for c in RUNGS}
    log(f"  RAND - BLOCK pooled median gap:  "
        + "   ".join(f"{c} bps {gap[c]:+.4f}" for c in RUNGS))
    ratio = gap[0] / gap[10] if gap[10] else np.nan
    h_cost = ratio <= 0.50
    log(f"  H_COST    gap(0bps)/gap(10bps) = {ratio:.3f} <= 0.50 ?              "
        f"[{'PASS' if h_cost else 'FAIL'}]")
    h_zero = abs(gap[0]) <= 0.02
    log(f"  H_ZERO    |gap(0bps)| = {abs(gap[0]):.4f} <= 0.02 ?                    "
        f"[{'PASS' if h_zero else 'FAIL'}]")

    merged = ex.pivot_table(index=["panel", "family", "q", "w", "depth", "cadence", "gross"],
                            columns="kind", values=[f"excess_{c}bps" for c in RUNGS])
    dr, ds = {}, {}
    for c in RUNGS:
        dr[c] = (merged[(f"excess_{c}bps", "RUNPERM")] - merged[(f"excess_{c}bps", "BLOCK")]).abs().median()
        ds[c] = (merged[(f"excess_{c}bps", "SWITCHMATCH")] - merged[(f"excess_{c}bps", "BLOCK")]).abs().median()
    log(f"  median |RUNPERM - BLOCK|     per-arm: "
        + "   ".join(f"{c} bps {dr[c]:.4f}" for c in RUNGS))
    log(f"  median |SWITCHMATCH - BLOCK| per-arm: "
        + "   ".join(f"{c} bps {ds[c]:.4f}" for c in RUNGS))
    h_run = all(dr[c] <= 0.02 for c in RUNGS)
    h_sw = all(ds[c] <= 0.02 for c in RUNGS)
    log(f"  H_RUNMATCH  all rungs <= 0.02 ?                              "
        f"[{'PASS' if h_run else 'FAIL'}]")
    log(f"  H_SWITCH    all rungs <= 0.02 ?                              "
        f"[{'PASS' if h_sw else 'FAIL'}]")
    for c in RUNGS:
        dm = (merged[(f"excess_{c}bps", "RAND")] - merged[(f"excess_{c}bps", "BLOCK")]).abs().median()
        log(f"     (for scale) median |RAND - BLOCK| per-arm at {c:2d} bps = {dm:.4f}")

    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    dup = int(arms.duplicated(subset=key).sum())
    log(f"  (arm-key uniqueness check: {dup} duplicate keys among {len(arms)} BLOCK rows)")
    dgm = arms.groupby(key)["degenerate"].max()
    nd = ~dgm.reindex(merged.index).fillna(False).to_numpy().astype(bool)
    log(f"  SAME TWO ROWS ON THE {int(nd.sum())} NON-DEGENERATE ARMS ONLY (where SWITCHMATCH is not")
    log("  RUNPERM by force, i.e. the only arms that can tell the two clauses apart):")
    for c in RUNGS:
        d1 = (merged[(f"excess_{c}bps", "RUNPERM")] - merged[(f"excess_{c}bps", "BLOCK")]).abs()[nd].median()
        d2 = (merged[(f"excess_{c}bps", "SWITCHMATCH")] - merged[(f"excess_{c}bps", "BLOCK")]).abs()[nd].median()
        log(f"     {c:2d} bps   |RUNPERM-BLOCK| {d1:.4f}    |SWITCHMATCH-BLOCK| {d2:.4f}")

    rho = {c: spearman(ex["sw_ratio"], ex[f"excess_{c}bps"]) for c in RUNGS}
    log(f"  Spearman(placebo switch-count ratio, excess): "
        + "   ".join(f"{c} bps {rho[c]:+.3f}" for c in RUNGS))
    h_mech = (rho[10] >= 0.50) and (rho[0] < 0.20)
    log(f"  H_MECH    rho(10bps) >= +0.50 AND rho(0bps) < +0.20 ?        "
        f"[{'PASS' if h_mech else 'FAIL'}]")

    log("\n  rule 8 on the STATISTIC: does the RAND-BLOCK gap walk forward?")
    piv_is = ex.pivot_table(index=["panel", "family", "q", "w", "depth", "cadence", "gross"],
                            columns="kind", values=["excess_IS", "excess_OOS"]).reset_index()
    piv_is.columns = ["_".join([str(a) for a in c if a != ""]) for c in piv_is.columns]
    piv_is["gap_IS"] = piv_is["excess_IS_RAND"] - piv_is["excess_IS_BLOCK"]
    piv_is["gap_OOS"] = piv_is["excess_OOS_RAND"] - piv_is["excess_OOS_BLOCK"]
    nwf = 0
    log(f"    {'family':12s} {'gap_IS':>9s} {'gap_OOS':>9s} {'rho(IS,OOS)':>12s}")
    for f in fams:
        s = piv_is[piv_is["family"] == f]
        r_ = spearman(s["gap_IS"], s["gap_OOS"])
        nwf += int(np.isfinite(r_) and r_ >= 0.30)
        log(f"    {f:12s} {s['gap_IS'].median():+9.4f} {s['gap_OOS'].median():+9.4f} {r_:+12.3f}")
    h_wf = nwf >= 6
    log(f"  H_WF      rho >= +0.30 in {nwf} of 8 families                   "
        f"[{'PASS' if h_wf else 'FAIL'}]  (bar >=6)")

    # ====================================================================== [4] books, rule 8
    log("\n[4] THE BOOKS BEHIND THESE ARMS - rule 8 walk-forward and both KEEP paths")
    log("    Selector (declared, IS-only): highest IS Sharpe on 2009-2016 among ALL arms of the")
    log("    panel; read untouched on 2017-2026.  The four nulls do not enter the selector.")
    keeprows = []
    for pn in ["U56", "B136", "SMALL"]:
        b = bench.loc[pn]
        sub = cells[cells["panel"] == pn]
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        for label, m in (("PICK(IS-Sharpe)", pick),):
            p4a = (m["H1"] > b["bl_h1"] and m["H2"] > b["bl_h2"] and m["MaxDD"] >= b["bl_dd"])
            p4b = (m["H1"] > b["spy_h1"] and m["H2"] > b["spy_h2"]
                   and m["OOS_Sharpe"] > b["spy_oos_s"]
                   and m["MaxDD"] >= 0.6 * b["spy_dd"]
                   and m["CAGR"] >= 0.7 * b["spy_cagr"])
            keeprows.append(dict(panel=pn, label=label, family=m["family"], q=m["q"], w=m["w"],
                                 depth=m["depth"], cadence=m["cadence"], gross=m["gross"],
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"], OOS_CAGR=m["OOS_CAGR"],
                                 OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                                 path4a=p4a, path4b=p4b))
        log(f"\n  {pn}: IS-pick = {pick['family']} q{pick['q']} w{int(pick['w'])} "
            f"d{pick['depth']:.2f} {pick['cadence']} g{pick['gross']:.2f}")
        log(f"    {'row':26s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1/H2':>13s} "
            f"{'OOS CAGR':>9s} {'OOS Sh':>7s} {'OOS DD':>8s}")
        log(f"    {'PICK':26s} {pick['CAGR']:8.2%} {pick['Sharpe']:7.3f} {pick['MaxDD']:8.2%} "
            f"{pick['H1']:6.3f}/{pick['H2']:6.3f} {pick['OOS_CAGR']:9.2%} "
            f"{pick['OOS_Sharpe']:7.3f} {pick['OOS_MaxDD']:8.2%}")
        log(f"    {'RULES v2 baseline (live)':26s} {b['bl_cagr']:8.2%} {b['bl_sh']:7.3f} "
            f"{b['bl_dd']:8.2%} {b['bl_h1']:6.3f}/{b['bl_h2']:6.3f} {b['bl_oos_c']:9.2%} "
            f"{b['bl_oos_s']:7.3f} {b['bl_oos_d']:8.2%}")
        log(f"    {'SPY':26s} {b['spy_cagr']:8.2%} {b['spy_sh']:7.3f} {b['spy_dd']:8.2%} "
            f"{b['spy_h1']:6.3f}/{b['spy_h2']:6.3f} {b['spy_oos_c']:9.2%} "
            f"{b['spy_oos_s']:7.3f} {b['spy_oos_d']:8.2%}")
        log(f"    KEEP 4a {keeprows[-1]['path4a']}   KEEP 4b {keeprows[-1]['path4b']}")
    kdf = pd.DataFrame(keeprows)
    log(f"\n  census over ALL {len(cells)} arms (not selected - the base rate):")
    for pn in ["U56", "B136", "SMALL"]:
        b = bench.loc[pn]
        s = cells[cells["panel"] == pn]
        n4a = int(((s["H1"] > b["bl_h1"]) & (s["H2"] > b["bl_h2"]) & (s["MaxDD"] >= b["bl_dd"])).sum())
        n4b = int(((s["H1"] > b["spy_h1"]) & (s["H2"] > b["spy_h2"])
                   & (s["OOS_Sharpe"] > b["spy_oos_s"]) & (s["MaxDD"] >= 0.6 * b["spy_dd"])
                   & (s["CAGR"] >= 0.7 * b["spy_cagr"])).sum())
        log(f"    {pn:6s} n={len(s):5d}  4a {n4a:5d} ({n4a / len(s):.1%})  "
            f"4b {n4b:5d} ({n4b / len(s):.1%})  median Sharpe {s['Sharpe'].median():.3f}")

    # ====================================================================== [5] verdict
    log("\n[5] VERDICT")
    hs = dict(H_COST=h_cost, H_ZERO=h_zero, H_RUNMATCH=h_run, H_SWITCH=h_sw,
              H_MECH=h_mech, H_WF=h_wf)
    for k, v in hs.items():
        log(f"  {k:11s} {'PASS' if v else 'FAIL'}")
    log("")
    if h_run and not h_sw:
        log("  ANSWER = YES, AND THE STATISTIC IS THE RUN-LENGTH DISTRIBUTION.  A null matched on")
        log("  the switch COUNT alone does NOT reproduce BLOCK; one matched on the full run-length")
        log("  multiset does.  PROTOCOL must name the distribution, not the count.")
    elif h_run and h_sw:
        log("  ANSWER = YES, AND THE CHEAPER STATISTIC SUFFICES.  Matching the switch COUNT already")
        log("  reproduces BLOCK to within the bar; the run-length multiset buys nothing further.")
        log("  PROTOCOL should name the switch count, which is far easier to satisfy.")
    elif not h_run and not h_sw:
        log("  ANSWER = NO NAMED STATISTIC IS SUFFICIENT.  Neither matched null reproduces BLOCK,")
        log("  so BLOCK's remaining property (the run ORDER, i.e. the path itself) is doing work a")
        log("  matched-statistic clause cannot capture.  PROTOCOL should name the CONSTRUCTION.")
    else:
        log("  ANSWER = MIXED; see the per-rung table above.")
    log("")
    log("  Capital verdict is decided in [4], not here: a PROTOCOL clause is not a trading rule.")

    # ------------------------------------------------------------------------------- artefacts
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.nulls.csv", index=False)
    kdf.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    bench.to_csv(OUT / f"{STEM}.bench.csv")
    if not cen.empty:
        cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    piv_is.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    log(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return hs, kdf, pooled, gap, dr, ds, rho


if __name__ == "__main__":
    main()
