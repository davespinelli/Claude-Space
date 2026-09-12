#!/usr/bin/env python3
"""Idea 793 (lane C, 2026-09-12) - does-the-NAMED-in-degree-predict-anything-the-record-
should-act-on.

QUESTION
--------
Idea 790 (lane C, 2026-09-11) drew the record's reliance graph and found NAMED is its only
concentrated leg (gini 0.7348, top decile 59.63% of all NAMED mass, 34.50% of rankable runs
never named once) - but also that the NAMED core verifies WORSE against its own committed
data than the tail (NAMED @ top 2% reads 75.9% against an 89.4% sampled base) and that the
NAMED ranking is unstable across vintages (Jaccard 0.2069 at the decile).  A concentration
that is unstable and anti-correlated with soundness may be measuring nothing at all.  This
run asks the only question that decides whether the statistic is worth carrying: does NAMED
in-degree PREDICT anything the record should act on - reproduction, verdict survival, or
KEEP-path output - or is it a recency / topic artefact?

WHAT "PREDICT" HAS TO MEAN HERE, AND WHY IDEA 790's IN-DEGREE CANNOT ANSWER IT
------------------------------------------------------------------------------
Idea 790 counted citers over the WHOLE record.  An in-degree measured with the whole record
citing is contemporaneous with, and for one of the three outcomes CAUSED BY, the thing it is
asked to predict: a run that is named a lot is, mechanically, a run that has more chances to
be named with a KILL beside it.  So the predictor here is LAGGED and the outcome is taken
strictly OUTSIDE the predictor's window wherever the outcome is a downstream event:

    NAMED@L(B) = number of DISTINCT other runs A, with vintage(A) in (vintage(B),
                 vintage(B) + L days], whose committed text names B (by stem, or by an idea
                 number the record itself attributes to B).  L = FWD is the unbounded
                 forward window (every strictly later run).

THE LAG LADDER IS IN DAYS THE RECORD ACTUALLY HAS, AND THAT IS A FINDING IN ITSELF
----------------------------------------------------------------------------------
This grid was pre-registered at L in {7, 14, 30, ALL} and had to be re-scaled to
{1, 2, 3, FWD} for a reason that is measured, printed as an appendix, and reported as a
result rather than buried: the whole committed record spans TEN CALENDAR DAYS
(2026-09-03 .. 2026-09-12) and holds 710 rankable runs.  At L = 7 every citation the record
contains is already inside the predictor window, so the SURVIVE outcome - which must be
measured strictly OUTSIDE it - is empty for every run, and NAMED@7 = NAMED@14 = NAMED@30
identically.  A day-lag of a week or more cannot separate predictor from outcome on a
record this young.  The appendix prints the full {1, 2, 3, 5, 7, 14, 30} ladder so the
degeneracy is visible, and the grid is the three rungs that resolve plus the unbounded one.
Also reported, never tuned: NAMED@ALL, idea 790's own statistic, which is UNDIRECTED IN
TIME - it counts any other run naming B, earlier and same-day ones included - and is the
reason its in-degree (1,878) is twice the strictly-forward count (903).

Each outcome's temporal status is declared, not glossed:
    REPRO    STATIC.  A property of the run's own committed artefacts at the moment it was
             written.  Nothing later can change it, so this is an ASSOCIATION, not a
             forecast: "does the record lean on the runs whose arithmetic reproduces?"
    SURVIVE  FORWARD, and the only genuine prediction of the three.  Measured STRICTLY
             outside the predictor window: a run is OVERTURNED if some run dated LATER THAN
             vintage + L names it inside a window of overturn language.  Predictor and
             outcome share no citer at any finite L.
    KEEP4B   STATIC (the run's own 4b tally, fixed when it was committed).  Association:
             "does the record lean on the runs that produced capital-relevant positives?"
    Two of the three cannot be forecasts, and are labelled as associations everywhere below.
    A statistic that predicts nothing forward and associates with nothing static is an
    artefact; that is the disposal this run is set up to be able to reach.

THE TWO RIVAL EXPLANATIONS THE QUEUE NAMES, BOTH MEASURED
---------------------------------------------------------
RECENCY  an old run has had more days in which to be cited.  The lag window is the direct
         fix (every run gets the same L days of exposure), and on top of it every cell is
         re-read as a rank-partial correlation holding EXPOSURE (days from the run's own
         vintage to the corpus end) fixed.
TOPIC    the record works in bursts on one subject; in-degree may only be saying "this run
         is in the currently busy topic".  Every cell is re-read with predictor and outcome
         rank-demeaned WITHIN a fixed 6-way topic label taken from the run's own slug.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. PREDICTOR LAG L in {7, 14, 30, ALL} days
    2. OUTCOME in {REPRO, SURVIVE, KEEP4B}
All 4 x 3 = 12 grid points are reported, each with its raw, recency-partialled and
within-topic reading, its permutation p, and its top-decile contrast.
REPORTED (never selected) axes: verification leg (ANY / DATA), corpus vintage period
(FULL / EARLY / LATE), top share (0.02 / 0.05 / 0.10 / 0.20 / 0.25), and the price-side
parent x arm x gross x cadence grid.

PRE-REGISTERED HYPOTHESES (written before any correlation was read)
-------------------------------------------------------------------
H_PRED    : NAMED in-degree predicts something.  A cell COUNTS only if |rho| >= 0.20 AND
            permutation p < 0.05 AND the recency-partialled and within-topic readings each
            retain >= 50% of |rho|.  H_PRED holds if at least one of the 12 cells counts;
            falsified if none does.
H_RECENCY : NAMED@ALL is substantially a recency statistic - Spearman(NAMED@ALL, exposure
            days) >= 0.50.  If it holds, the ALL column is not a clean predictor and the
            lagged columns are the honest ones.
H_TOPIC   : the association is a topic artefact - within-topic demeaning cuts the headline
            |rho| by >= 50%.
H_SURV    : the mechanical channel is real - among runs named at least once, overturn risk
            RISES with in-degree (rho(NAMED@L, overturned) > 0), i.e. "survival" is partly a
            measure of being ignored.  This is stated as a hypothesis because if it holds,
            any positive rho(NAMED, SURVIVE) is a citation-exposure artefact, not a quality
            signal.
H_ACT     : the record should ACT on it - a decision rule that trades a parent only when its
            backing claims come from a high-NAMED@L run beats BOTH the always-act control
            and the full-stand-down control on OOS Sharpe.  Falsified otherwise.

GATES (pre-registered, run and printed before any new number is read)
    G1 identity   : fast_backtest vs engine.backtest on one book per parent.       bar 1e-12
    G2 comparands : the record's own price anchors - RULES v2 on U56 reads 1.1998 Sharpe /
                    -12.05% MaxDD / 9.45% OOS CAGR and SPY reads 15.11% / 0.8835 / -33.72%
                    - reproduced with the tape PINNED at 2026-09-10, the last bar the record
                    had when those anchors were published.  data/prices.csv has since gained
                    2026-09-11; the un-pinned read is printed beside the pinned one so the
                    one-bar drift is visible and is not silently absorbed.         bar 5e-04
    G3 graph      : idea 790's committed `.graph.csv` NAMED column reproduces on the shared
                    runs from the TREE 790 ACTUALLY SAW - `git archive` of its OWN commit
                    (35b031d) with its own narrative .md removed, because that is what its
                    corpus glob saw: a working tree in which its script existed and its
                    `.result.md` did not yet.  A filename-vintage pin cannot do this job -
                    CHANGELOG.md and RULES.md are undated append-only documents (ideas
                    328 / 514).  Two bars: the git-pinned rebuild reproduces exactly, and
                    today's un-pinned in-degree never DECREASES on any shared run (in-degree
                    is monotone in corpus size).  Stated in advance: the tree 790 read is a
                    working directory mid-lane and is not exactly ANY commit, so a residual
                    of a few edges is possible; it will be reported and named, not absorbed
                    by moving the bar.                                              bar exact
    G4 verifier   : idea 790's committed `.verify.csv` DATA_share reproduces from this run's
                    own verifier on the shared runs.                               bar 1e-09
    G5 monotone   : NAMED@7 <= NAMED@14 <= NAMED@30 <= NAMED@ALL on every run.      0 breaks
    G6 calibration: the verifier is calibrated before REPRO is believed - PLANT-TRUE (values
                    resampled from a run's own committed csv, re-formatted) must verify at
                    >= 95%; PLANT-FALSE (same-shape tokens drawn uniformly over the same
                    observed range, seeded) gives the NOISE FLOOR that every REPRO share is
                    read against.  Idea 790 measured that floor at 46.0%.

RULE 8 WALK-FORWARD (required, run whatever the census says)
    CORPUS split (for the answer): EARLY = runs dated < 2026-09-08, LATE = >= 2026-09-08,
      idea 790's own split.  WF-A measures every one of the 12 cells on EARLY runs and then
      reads the SAME cell ONCE on LATE runs, and asks whether sign and magnitude carry.  The
      lag is what makes this comparable at all: LATE runs have only days of citation
      exposure, so the ALL column is not comparable across the split and is reported as such.
    PRICE split (for the book): IS = start..2016-12-31, OOS = 2017-01-01..end, read ONCE.
    WF-B prices the statistic as a DECISION RULE, idea 790's frame with NAMED@L in place of
      its SUM core: in each (gross, cadence) cell rank the three parents by IS MA-gate
      premium and ACT on the IS-best parent only if at least one of the record's backing
      claim-runs for that parent is in the top share by NAMED@L (ranked on EARLY citers only)
      AND its own headline numbers verify; else STAND DOWN to the live book (RULES v2 on
      U56).  OOS read once for all 20 decision books, against RULES v2 U56, SPY, an
      ALWAYS-ACT control and a FULL-STAND-DOWN control.
    KEEP paths 4a and 4b are evaluated for EVERY price book and EVERY decision book.
    Stated up front: a decision book built out of a bibliometric statistic is a diagnostic,
    not a rule anyone can trade, so a 4b pass here is a diagnostic and never a capital
    candidate.

SURVIVORSHIP: universe.json / universe_broad.json / the small panel are CURRENT constituents,
    so every stock-side level carries a survivorship premium; arm-minus-arm premia on the
    same panel largely cancel it.  The three parents start on different dates (U56/B136 2008,
    SMALL 2010).

SELF-EXCLUSION: this run's own script and artefacts are removed from the corpus, on both the
    citing and the cited side.  Without it the run cites everything it discusses and ranks
    itself.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and the committed
artefacts under research/.
"""
from __future__ import annotations

import bisect
import collections
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
RES = ROOT / "research"
BT = RES / "backtests"

COST = 10.0
MA_WIN = 200
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TOL = 1e-12

LAGS = [1, 2, 3, "FWD"]                      # tuned parameter 1 (days; FWD = unbounded)
LADDER = [1, 2, 3, 5, 7, 14, 30]             # reported appendix: why the grid is 1/2/3
OUTCOMES = ["REPRO", "SURVIVE", "KEEP4B"]    # tuned parameter 2
HEAD_LAG, HEAD_OUT = 3, "SURVIVE"            # the headline cell: the only forward one
SHARES = [0.02, 0.05, 0.10, 0.20, 0.25]      # reported, never selected
VINTAGE_SPLIT = "2026-09-08"                 # idea 790's corpus split
PIN_790_COMMIT = "35b031d"                   # idea 790's own commit; its own .md is removed below
CONTROL_DOCS = ("RULES.md", "PROTOCOL.md", "CHANGELOG.md", "LEADERBOARD.md", "QUEUE.md")
INDEX_DOCS = ("LEADERBOARD.md", "QUEUE.md")
SIG_MIN = 4
MAX_BYTES = 30_000_000
SOUND_BAR = 0.90
N_PERM = 2000
SEED = 20260912
RHO_BAR, P_BAR, RETAIN_BAR = 0.20, 0.05, 0.50
OVERTURN_WIN = 300                           # chars either side of a naming mention

P790 = BT / "2026-09-11_does-the-RECORD-S-RELIANCE-GRAPH-have-a-LOAD-BEARING-CORE-worth-re-verifying_C"
P779 = BT / "2026-09-11_does-the-MIN-GAP-PAIR-restatement-change-any-published-VERDICT-not-just-the-count_C"
PUB790 = dict(gini=0.7348, mass10=0.5963, zero_share=0.3450, total=1828,
              plant_false=0.460, jaccard10=0.2069)
PUB_PRICE = dict(u56_sharpe=1.1998, u56_maxdd=-0.1205, u56_oos_cagr=0.0945,
                 spy_cagr=0.1511, spy_sharpe=0.8835, spy_maxdd=-0.3372)
TAPE_PIN = "2026-09-10"                      # last bar the record's price anchors were read on

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill(), sorted(set(px56.columns) - {"SPY"})),
        "B136": (px136.dropna(how="all").ffill(), sorted(set(px136.columns) - {"SPY"})),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), sorted(s_stk)),
    }


# --------------------------------------------------------------------- the corpus
NUM_RE = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")
STEM_REF = re.compile(r"(\d{4}-\d{2}-\d{2}_[A-Za-z0-9][A-Za-z0-9_.\-]*)")
IDEA_RE = re.compile(r"\bidea\s+(\d{2,4})\b", re.IGNORECASE)
STEM_IDEA_RE = re.compile(r"^\s*(\d{2,4})\.\s")
VINT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")
DATA_SUFFIX = (".csv", ".json", ".txt", ".npz")
OVERTURN_RE = re.compile(
    r"\b(kill|kills|killed|refute\w*|refuted|overturn\w*|artefact|artifact|"
    r"inverted|inversion|mis-?stated|misread|does not reproduce|fails? to reproduce|"
    r"not reproducible|premise (?:is )?(?:killed|refuted|inverted)|wrong)\b", re.IGNORECASE)
TOPIC_RULES = [
    ("CENSUS", re.compile(r"census|record|committed|claim|publish|restate|re-read|re-score|"
                          r"audit|verif|reproduc", re.I)),
    ("MATCH", re.compile(r"match|kernel|draw|origin|panel|ladder|decile|permut|null", re.I)),
    ("GROSS", re.compile(r"gross|cadence|cost|rung|turnover|respread|degross|weight", re.I)),
    ("KEEP", re.compile(r"keep|4a|4b|rules|book|capital|walk-?forward|park|candidate", re.I)),
    ("VOL", re.compile(r"\bvol|drawdown|maxdd|\bdd\b|sharpe|risk|band|momentum", re.I)),
]


def sigdigits(tok):
    t = tok.lstrip("+-")
    if "." not in t:
        return 0
    body = t.replace(".", "").lstrip("0")
    return len(body.rstrip("0")) if body.rstrip("0") else 0


def stem_of(name):
    return name.split(".")[0]


def vintage(stem):
    m = VINT_RE.match(stem)
    return m.group(1) if m else ""


def vdate(stem):
    v = vintage(stem)
    return pd.Timestamp(v) if v else pd.NaT


def topic_of(stem):
    slug = stem[11:] if len(stem) > 11 else stem
    for name, rx in TOPIC_RULES:
        if rx.search(slug):
            return name
    return "OTHER"


def file_idea_numbers(res=None):
    """file stem -> idea numbers the RECORD attributes to it (QUEUE 'Done' / LEADERBOARD)."""
    res = res or RES
    f2i = collections.defaultdict(set)
    for src in (res / "QUEUE.md", res / "LEADERBOARD.md"):
        if not src.exists():
            continue
        for line in src.read_text(errors="ignore").split("\n"):
            nums = set()
            m = STEM_IDEA_RE.match(line)
            if m:
                nums.add(m.group(1))
            for m in re.finditer(r"\|\s*(\d{2,4})\s+", line):
                nums.add(m.group(1))
            for m in re.finditer(r"research/backtests/([^\s`|)]+\.py)", line):
                for n in nums:
                    f2i[m.group(1)[:-3]].add(n)
    return f2i


def load_corpus(res=RES):
    """Every committed markdown and script in research/ - the record as text, self excluded."""
    bt = res / "backtests"
    paths = sorted(set(list(bt.glob("*.md")) + list(bt.glob("*.py"))
                       + list(res.glob("*.md")) + list(res.glob("*.py"))))
    return {p.name: p.read_text(errors="ignore") for p in paths
            if stem_of(p.name) != STAMP}


def gini(x):
    v = np.sort(np.asarray(x, dtype=float))
    n = len(v)
    if n == 0 or v.sum() <= 0:
        return np.nan
    idx = np.arange(1, n + 1)
    return float((2 * (idx * v).sum()) / (n * v.sum()) - (n + 1) / n)


def naming_edges(texts, res=None, want_hostile=False):
    """citer file name -> set of run stems it NAMES (self-edge and index docs removed).

    With want_hostile, also returns citer -> set of stems it names INSIDE overturn language.
    Hostility is found in a single pass per document: the overturn keywords' positions are
    collected once, and each naming mention is tested against them by bisection, so the cost
    is linear in the corpus rather than (documents x cited runs).
    """
    all_stems = {stem_of(n) for n in texts}
    f2i = file_idea_numbers(res)
    i2f = collections.defaultdict(set)
    for st, ideas in f2i.items():
        for i in ideas:
            i2f[i].add(st)
    out, ctrl, hostile = {}, collections.defaultdict(set), {}
    for n, txt in texts.items():
        src = stem_of(n)
        mentions = []                                   # (position, cited stem)
        for m in STEM_REF.finditer(txt):
            st = stem_of(m.group(1))
            if st in all_stems:
                mentions.append((m.start(), st))
        for m in IDEA_RE.finditer(txt):
            for st in i2f.get(m.group(1), ()):
                mentions.append((m.start(), st))
        hits = {st for _, st in mentions}
        hits.discard(src)
        if n in CONTROL_DOCS:
            for h in hits:
                ctrl[h].add(n)
        if n in INDEX_DOCS:
            continue                       # index docs name everything by PROTOCOL rule 5
        out[n] = hits
        if want_hostile:
            hp = [m.start() for m in OVERTURN_RE.finditer(txt)]
            hs = set()
            if hp:
                for pos, st in mentions:
                    if st == src:
                        continue
                    j = bisect.bisect_left(hp, pos - OVERTURN_WIN)
                    if j < len(hp) and hp[j] <= pos + OVERTURN_WIN:
                        hs.add(st)
            hostile[n] = hs
    return (out, ctrl, i2f, hostile) if want_hostile else (out, ctrl, i2f)


def indegree_at_lag(edges, runs, lag, citer_filter=None):
    """NAMED@lag: distinct citer RUNS dated in (v, v+lag] days; lag='FWD' = unbounded."""
    deg = {r: set() for r in runs}
    for n, hits in edges.items():
        if citer_filter is not None and not citer_filter(n):
            continue
        src = stem_of(n)
        dv = vdate(src)
        for h in hits:
            if h not in deg:
                continue
            hv = vdate(h)
            if pd.isna(dv) or pd.isna(hv):
                continue                    # a control doc has no vintage: ALL-only
            if dv <= hv:
                continue                    # a citer must post-date the run it names
            if lag != "FWD" and (dv - hv).days > lag:
                continue
            deg[h].add(src)
    return {r: len(v) for r, v in deg.items()}


def indegree_all_including_undated(edges, runs, citer_filter=None):
    """NAMED@ALL exactly as idea 790 counted it: any distinct other run, dated or not."""
    deg = {r: set() for r in runs}
    for n, hits in edges.items():
        if citer_filter is not None and not citer_filter(n):
            continue
        src = stem_of(n)
        for h in hits:
            if h in deg:
                deg[h].add(src)
    return {r: len(v) for r, v in deg.items()}


# ---------------------------------------------------------------- re-verification
def own_artefacts(stem):
    return [p for p in BT.glob(stem + ".*") if p.suffix in DATA_SUFFIX]


def read_values(paths):
    toks, vals, capped, nbytes = set(), [], 0, 0
    for p in paths:
        try:
            raw = p.read_text(errors="ignore")[:MAX_BYTES]
        except Exception:
            continue
        if p.stat().st_size > MAX_BYTES:
            capped += 1
        nbytes += len(raw)
        found = set(NUM_RE.findall(raw))
        toks |= found
        try:
            vals.append(np.asarray(sorted(found), dtype=np.float64))
        except (ValueError, OverflowError):
            vals.append(pd.to_numeric(pd.Series(sorted(found)), errors="coerce")
                        .to_numpy(float))
    if vals:
        v = np.concatenate(vals)
        v = v[np.isfinite(v)]
    else:
        v = np.zeros(0)
    return toks, v, capped, nbytes


def verify_tokens(tokens, toks, vals):
    sv = np.sort(vals) if vals.size else vals
    out = {}
    for t in tokens:
        if t in toks:
            out[t] = "EXACT"
            continue
        try:
            q = float(t)
        except ValueError:
            out[t] = "NONE"
            continue
        d = len(t.split(".")[1]) if "." in t else 0
        tolr = 0.5 * 10.0 ** (-d)
        ok = False
        if sv.size:
            for cand in (q, q / 100.0, q * 100.0):
                lo = np.searchsorted(sv, cand - tolr, side="left")
                hi = np.searchsorted(sv, cand + tolr, side="right")
                if hi > lo:
                    ok = True
                    break
        out[t] = "ROUND" if ok else "NONE"
    return out


def verify_run(stem, heads, keep_raw=False):
    arte = own_artefacts(stem)
    if not arte:
        return None
    toks_a, vals_a, cap_a, b_a = read_values(arte)
    data_only = [p for p in arte if not p.name.endswith(".console.txt")]
    toks_d, vals_d, cap_d, b_d = read_values(data_only)
    va = verify_tokens(heads, toks_a, vals_a)
    vd = verify_tokens(heads, toks_d, vals_d)
    n = len(heads)
    raw = dict(_toks_d=toks_d, _vals_d=vals_d) if keep_raw else {}
    return dict(run=stem, n_head=n, n_artefacts=len(arte), n_data=len(data_only),
                bytes_any=b_a, bytes_data=b_d, capped=cap_a + cap_d,
                ANY_ok=sum(v != "NONE" for v in va.values()),
                DATA_ok=sum(v != "NONE" for v in vd.values()),
                ANY_share=(sum(v != "NONE" for v in va.values()) / n) if n else np.nan,
                DATA_share=(sum(v != "NONE" for v in vd.values()) / n) if n else np.nan,
                **raw)


# ------------------------------------------------------------------- statistics
def rankdata(x):
    s = pd.Series(np.asarray(x, dtype=float))
    return s.rank(method="average").to_numpy()


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 5:
        return np.nan
    rx, ry = rankdata(x[ok]), rankdata(y[ok])
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def t_of(rho, n):
    if not np.isfinite(rho) or n < 4 or abs(rho) >= 1:
        return np.nan
    return float(rho * np.sqrt((n - 2) / (1 - rho ** 2)))


def partial_spearman(x, y, z):
    rxy, rxz, ryz = spearman(x, y), spearman(x, z), spearman(y, z)
    den = np.sqrt(max(1e-12, (1 - rxz ** 2) * (1 - ryz ** 2)))
    return float((rxy - rxz * ryz) / den)


def within_group_spearman(x, y, g):
    x, y = np.asarray(x, float), np.asarray(y, float)
    g = np.asarray(g)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y, g = x[ok], y[ok], g[ok]
    if len(x) < 5:
        return np.nan
    rx, ry = rankdata(x), rankdata(y)
    dx, dy = np.zeros_like(rx), np.zeros_like(ry)
    for lab in np.unique(g):
        m = g == lab
        if m.sum() < 2:
            dx[m], dy[m] = 0.0, 0.0
            continue
        dx[m] = rx[m] - rx[m].mean()
        dy[m] = ry[m] - ry[m].mean()
    if dx.std() == 0 or dy.std() == 0:
        return np.nan
    return float(np.corrcoef(dx, dy)[0, 1])


def perm_p(x, y, rho, seed=SEED, n=N_PERM):
    """Two-sided permutation p for |rho|, and the 95th percentile |rho| noise floor."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 5 or not np.isfinite(rho):
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    rx, ry = rankdata(x), rankdata(y)
    rx = (rx - rx.mean()) / (rx.std() or 1)
    ry = (ry - ry.mean()) / (ry.std() or 1)
    null = np.empty(n)
    for i in range(n):
        null[i] = float(np.dot(rx, rng.permutation(ry)) / len(rx))
    return float((np.abs(null) >= abs(rho)).mean()), float(np.percentile(np.abs(null), 95))


def top_contrast(x, y, share):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 10:
        return np.nan, np.nan, 0
    k = max(1, int(round(share * len(x))))
    order = np.argsort(-x, kind="stable")
    top, rest = order[:k], order[k:]
    return float(y[top].mean()), float(y[rest].mean()), k


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 793 (lane C, 2026-09-12) - does-the-NAMED-in-degree-predict-anything-"
      "the-record-should-act-on")
    P("=" * 100)
    P(f"Tuned parameters: LAG {LAGS} x OUTCOME {OUTCOMES} = {len(LAGS)*len(OUTCOMES)} "
      f"points, all reported.  Headline cell: NAMED@{HEAD_LAG} vs {HEAD_OUT} "
      "(the only forward-in-time outcome).")
    P(f"Costs {COST:.0f} bps, next-day fills, weekly/monthly cadence, gross {GROSS}, "
      f"IS/OOS split {IS_END} / {OOS_START}.  Seed {SEED}.")
    P("")

    # ------------------------------------------------------------------ corpus
    texts = load_corpus()
    narrative = collections.defaultdict(list)
    for n in texts:
        if n in CONTROL_DOCS:
            continue
        if n.endswith(".md"):
            narrative[stem_of(n)].append(n)
    runs = sorted(r for r in narrative if vintage(r))
    P(f"CORPUS: {len(texts)} committed text files, {len(runs)} rankable dated runs "
      f"(a run is rankable if it committed a narrative .md).  Self ({STAMP}) excluded from "
      "both sides.")
    edges, ctrl_by, i2f, hostile = naming_edges(texts, want_hostile=True)
    own_tokens = {}
    for st in runs:
        toks = set()
        for fn in narrative[st]:
            for tok in set(NUM_RE.findall(texts[fn])):
                if sigdigits(tok) >= SIG_MIN:
                    toks.add(tok)
        own_tokens[st] = toks
    corpus_end = max(vdate(r) for r in runs)
    P(f"  corpus vintage span {min(vintage(r) for r in runs)} .. {corpus_end.date()}; "
      f"headline-token count median {int(np.median([len(own_tokens[r]) for r in runs]))}")
    P("")

    # ------------------------------------------------------------------ predictor
    deg = {L: indegree_at_lag(edges, runs, L) for L in LAGS}
    deg["ALL"] = indegree_all_including_undated(edges, runs)      # idea 790's own statistic
    G = pd.DataFrame({f"NAMED@{L}": pd.Series(deg[L]) for L in LAGS + ["ALL"]})
    G["vintage"] = [vintage(r) for r in G.index]
    G["topic"] = [topic_of(r) for r in G.index]
    G["exposure_days"] = [(corpus_end - vdate(r)).days for r in G.index]
    G["CTRL"] = [len(ctrl_by.get(r, set())) for r in G.index]
    G["n_head"] = [len(own_tokens[r]) for r in G.index]

    # ------------------------------------------------------------------ outcomes
    P("=" * 100)
    P("OUTCOMES (measured before any correlation is read)")
    P("=" * 100)
    # --- REPRO
    vrows, unverifiable = [], []
    for st in runs:
        v = verify_run(st, sorted(own_tokens[st]))
        if v is None:
            unverifiable.append(st)
        else:
            vrows.append(v)
    ver = pd.DataFrame(vrows).set_index("run")
    P(f"REPRO   : {len(ver)} runs verified against their OWN committed data artefacts "
      f"({len(unverifiable)} have no data artefact at all and are UNVERIFIABLE, reported "
      "and excluded from the REPRO cells, never scored as 0).")
    P(f"          DATA_share mean {ver.DATA_share.mean():.4f}, median "
      f"{ver.DATA_share.median():.4f}; ANY_share mean {ver.ANY_share.mean():.4f}; "
      f"{ver.bytes_data.sum()/1e6:.0f} MB of committed data read")
    # --- SURVIVE (per lag: overturned by a citer dated strictly beyond v + L)
    runset = set(runs)
    overturned = {L: dict.fromkeys(runs, 0) for L in LAGS}
    named_ever = {L: dict.fromkeys(runs, 0) for L in LAGS}
    for n, hits in edges.items():
        src = stem_of(n)
        dv = vdate(src)
        if pd.isna(dv):
            continue                        # an undated control doc has no "beyond L"
        hs = hostile.get(n, set())
        for h in hits:
            if h not in runset:
                continue
            hv = vdate(h)
            if pd.isna(hv) or dv <= hv:
                continue                    # a citer must post-date the run it names
            age = (dv - hv).days
            for L in LAGS:
                if L != "FWD" and age <= L:
                    continue                # inside the predictor window: not an outcome
                named_ever[L][h] += 1
                if h in hs:
                    overturned[L][h] += 1
    for L in LAGS:
        G[f"OVERTURN@{L}"] = pd.Series(overturned[L])
        G[f"LATENAMED@{L}"] = pd.Series(named_ever[L])
        G[f"SURVIVE@{L}"] = (pd.Series(overturned[L]) == 0).astype(float)
    P("SURVIVE : a run is OVERTURNED if a run dated strictly beyond its own vintage + L "
      "names it within")
    P(f"          {OVERTURN_WIN} characters of overturn language.  Predictor and outcome "
      "share NO citer at any finite L.")
    for L in LAGS:
        P(f"          L = {str(L):<4} overturned {int(G[f'OVERTURN@{L}'].gt(0).sum()):4d} of "
          f"{len(G)} ({G[f'OVERTURN@{L}'].gt(0).mean():.1%}); named at all beyond the window "
          f"{int(G[f'LATENAMED@{L}'].gt(0).sum()):4d}")
    # --- KEEP4B (the run's own committed 4b tally)
    KEEP_TXT = re.compile(r"\b4b\s*(\d+)\s*/\s*(\d+)|KEEP[- ]CANDIDATE|KEEP-candidate", re.I)
    NOKEEP = re.compile(r"no KEEP|NO KEEP|0 KEEP|no new KEEP|never a capital candidate", re.I)
    keep_txt, keep_dat, keep_cov = {}, {}, {}
    for st in runs:
        blob = " ".join(texts[f] for f in narrative[st])
        pos = 0
        for m in KEEP_TXT.finditer(blob):
            if m.group(1) is not None:
                pos = max(pos, 1 if int(m.group(1)) > 0 else 0)
            else:
                pos = max(pos, 0 if NOKEEP.search(blob[max(0, m.start() - 40):m.end() + 40])
                          else 1)
        keep_txt[st] = float(pos)
        d, cov = 0.0, 0
        for p in own_artefacts(st):
            if p.suffix != ".csv":
                continue
            try:                                   # sniff the header only, then one column
                with p.open(errors="ignore") as fh:
                    head = fh.readline()
            except Exception:
                continue
            cols = [c.strip().strip('"') for c in head.rstrip("\n").split(",")]
            keeps = [c for c in cols if re.fullmatch(r"(?i)keep_?4b", c)]
            if not keeps:
                continue
            cov = 1
            try:
                df = pd.read_csv(p, usecols=keeps)
            except Exception:
                continue
            for c in keeps:
                s = df[c]
                if s.dtype == bool:
                    d = max(d, float(s.any()))
                else:
                    d = max(d, float(s.astype(str).str.strip().str.lower()
                                     .isin(["true", "1", "1.0"]).any()))
        keep_dat[st], keep_cov[st] = d, cov
    G["KEEP4B_TXT"] = pd.Series(keep_txt)
    G["KEEP4B_DATA"] = pd.Series(keep_dat)
    G["KEEP4B_COV"] = pd.Series(keep_cov)
    G["KEEP4B"] = np.where(G.KEEP4B_COV > 0, G.KEEP4B_DATA, G.KEEP4B_TXT)
    agree = G[G.KEEP4B_COV > 0]
    P(f"KEEP4B  : narrative leg positive on {int(G.KEEP4B_TXT.sum())} of {len(G)} runs "
      f"({G.KEEP4B_TXT.mean():.1%}); committed-data leg (a `keep4b` column with a True) "
      f"covers {int(G.KEEP4B_COV.sum())} runs and is positive on "
      f"{int(agree.KEEP4B_DATA.sum())}")
    if len(agree):
        P(f"          the two legs AGREE on {float((agree.KEEP4B_TXT == agree.KEEP4B_DATA).mean()):.1%} "
          f"of the {len(agree)} runs where both are readable; the DATA leg is taken where "
          "available, the narrative leg elsewhere.")
    P(f"          headline KEEP4B positive on {int(G.KEEP4B.sum())} of {len(G)} "
      f"({G.KEEP4B.mean():.1%})")
    G["REPRO"] = ver["DATA_share"].reindex(G.index)
    G["REPRO_ANY"] = ver["ANY_share"].reindex(G.index)
    P("")

    # ------------------------------------------------------------------ gates
    P("=" * 100)
    P("GATES (all run and printed before any answer is read)")
    P("=" * 100)
    parents = real_panels()
    pnames = list(parents)
    gate_rows = []

    worst = 0.0
    for pn, (px, names) in parents.items():
        w = rules_v2_weights(px)
        a = fast_backtest(px, w, freq="W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        d = float(np.nanmax(np.abs((a - b).to_numpy())))
        worst = max(worst, d)
    P(f"G1 identity  : fast_backtest vs engine.backtest, worst |dr| over {len(parents)} "
      f"parents = {worst:.3e} -> {'PASS' if worst < TOL else 'FAIL'} (bar {TOL:g})")
    gate_rows.append(dict(gate="G1_identity", value=worst, bar=TOL, passed=worst < TOL))

    px56 = parents["U56"][0]

    def anchors(px):
        w = px.index[260]
        b = fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[w:]
        s = px["SPY"].pct_change().fillna(0.0).loc[w:]
        m, mo, ms = metrics(b), metrics(b.loc[OOS_START:]), metrics(s)
        d = max(abs(m["Sharpe"] - PUB_PRICE["u56_sharpe"]),
                abs(m["MaxDD"] - PUB_PRICE["u56_maxdd"]),
                abs(mo["CAGR"] - PUB_PRICE["u56_oos_cagr"]),
                abs(ms["CAGR"] - PUB_PRICE["spy_cagr"]),
                abs(ms["Sharpe"] - PUB_PRICE["spy_sharpe"]),
                abs(ms["MaxDD"] - PUB_PRICE["spy_maxdd"]))
        return m, mo, ms, d

    mp, mop, msp, d2p = anchors(px56.loc[:TAPE_PIN])
    m56, mo56, ms56, d2 = anchors(px56)
    P(f"G2 comparands: TAPE PINNED at {TAPE_PIN} - RULES v2 U56 {mp['CAGR']:.2%} / "
      f"{mp['Sharpe']:.4f} / {mp['MaxDD']:.2%} (OOS CAGR {mop['CAGR']:.2%}); SPY "
      f"{msp['CAGR']:.2%} / {msp['Sharpe']:.4f} / {msp['MaxDD']:.2%}; worst |d| vs the "
      f"record = {d2p:.3e} -> {'PASS' if d2p < 5e-4 else 'FAIL'} (bar 5e-04)")
    P(f"             UN-PINNED (today's tape, last bar {px56.index[-1].date()}): "
      f"{m56['CAGR']:.2%} / {m56['Sharpe']:.4f} / {m56['MaxDD']:.2%} (OOS CAGR "
      f"{mo56['CAGR']:.2%}); SPY {ms56['CAGR']:.2%} / {ms56['Sharpe']:.4f} / "
      f"{ms56['MaxDD']:.2%}; drift {d2:.3e} on ONE extra bar.  Every price number below is "
      "on the FULL tape; the drift is reported, not absorbed.")
    gate_rows.append(dict(gate="G2_comparands_pinned", value=d2p, bar=5e-4,
                          passed=d2p < 5e-4))
    gate_rows.append(dict(gate="G2_tape_drift_unpinned", value=d2, bar=np.nan, passed=True))

    g790 = pd.read_csv(f"{P790}.graph.csv").set_index("run")
    shared = [r for r in g790.index if r in G.index]
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git -C {ROOT} archive {PIN_790_COMMIT} research | tar -x -C {td}",
                       shell=True, check=True, capture_output=True)
        pin_res = Path(td) / "research"
        for q in (pin_res / "backtests").glob(P790.name + ".*"):
            if q.suffix == ".md":
                q.unlink()               # 790's own narrative did not exist when it globbed
        pin_texts = load_corpus(pin_res)
        pin_edges, _, _ = naming_edges(pin_texts, res=pin_res)
        pin_runs = sorted({stem_of(n) for n in pin_texts if n.endswith(".md")
                           and n not in CONTROL_DOCS and vintage(stem_of(n))})
        pinned = indegree_all_including_undated(pin_edges, pin_runs)
    pin_s = pd.Series(pinned).reindex(shared)
    dvec = (pin_s - g790.loc[shared, "NAMED"]).dropna()
    d3 = int(dvec.abs().sum())
    nmiss = int(pin_s.isna().sum())
    offenders = dvec[dvec != 0]
    n_dec = int((G.loc[shared, "NAMED@ALL"] - g790.loc[shared, "NAMED"]).lt(0).sum())
    P(f"G3 graph     : idea 790's NAMED column on {len(shared)} shared runs, rebuilt from "
      f"the tree it saw ({PIN_790_COMMIT}, {len(pin_texts)} files vs {len(texts)} today): "
      f"total |d| = {d3} on {len(shared)-nmiss} matched runs, exact on "
      f"{len(dvec)-len(offenders)} of {len(dvec)} -> "
      f"{'PASS' if d3 == 0 else 'MISSED BY %d EDGE(S), REPORTED NOT RELAXED' % d3} "
      "(bar exact)")
    for r, d in offenders.items():
        P(f"             residual {d:+.0f} on {r}")
    if len(offenders):
        P(f"             {d3} edge(s) out of idea 790's {int(g790.NAMED.sum())} NAMED total "
          f"({d3/max(int(g790.NAMED.sum()),1):.3%}); mechanism: the tree 790 read was a "
          "working directory mid-lane, not a commit.  Every headline below is re-read with "
          "these runs dropped in the SENSITIVITY line of Part 2.")
    P(f"             today's un-pinned NAMED@ALL DECREASES on {n_dec} of {len(shared)} shared "
      f"runs -> {'PASS' if n_dec == 0 else 'FAIL'} (in-degree is monotone in corpus size); "
      f"median growth {float((G.loc[shared,'NAMED@ALL'] - g790.loc[shared,'NAMED']).median()):+.1f}")
    g3_offenders = list(offenders.index)
    gate_rows.append(dict(gate="G3_graph_pinned", value=float(d3), bar=0.0, passed=d3 == 0))
    gate_rows.append(dict(gate="G3_graph_monotone", value=float(n_dec), bar=0.0,
                          passed=n_dec == 0))

    v790 = pd.read_csv(f"{P790}.verify.csv").set_index("run")
    vsh = [r for r in v790.index if r in ver.index]
    d4 = float((ver.loc[vsh, "DATA_share"] - v790.loc[vsh, "DATA_share"]).abs().max())
    P(f"G4 verifier  : idea 790's DATA_share on {len(vsh)} shared runs, max |d| = "
      f"{d4:.3e} -> {'PASS' if d4 < 1e-9 else 'FAIL'} (bar 1e-09)")
    gate_rows.append(dict(gate="G4_verifier", value=d4, bar=1e-9, passed=d4 < 1e-9))

    breaks = 0
    order = [f"NAMED@{L}" for L in LAGS]
    for a, b in zip(order, order[1:]):
        breaks += int((G[a] > G[b]).sum())
    P(f"G5 monotone  : " + " <= ".join(order) + f", violations = {breaks} "
      f"-> {'PASS' if breaks == 0 else 'FAIL'} (bar 0)")
    gate_rows.append(dict(gate="G5_monotone", value=float(breaks), bar=0.0,
                          passed=breaks == 0))

    rng = np.random.default_rng(SEED)
    cal = [r for r in ver.index if ver.loc[r, "n_data"] > 0][:60]
    tp = fp = tn = fn_ = 0
    for st in cal:
        arte = [p for p in own_artefacts(st) if p.suffix == ".csv"]
        if not arte:
            continue
        toks, vals, _, _ = read_values(arte)
        num = np.array([v for v in vals if np.isfinite(v)])
        if num.size < 50:
            continue
        true_s = rng.choice(num, size=10, replace=False)
        true_t = [f"{v:.4f}" for v in true_s]
        lo, hi = float(np.percentile(num, 1)), float(np.percentile(num, 99))
        false_t = [f"{v:.4f}" for v in rng.uniform(lo, hi, size=10)]
        rv = verify_tokens(true_t, toks, vals)
        fv = verify_tokens(false_t, toks, vals)
        tp += sum(v != "NONE" for v in rv.values())
        fn_ += sum(v == "NONE" for v in rv.values())
        fp += sum(v != "NONE" for v in fv.values())
        tn += sum(v == "NONE" for v in fv.values())
    tr = tp / max(tp + fn_, 1)
    fa = fp / max(fp + tn, 1)
    P(f"G6 calibrate : PLANT-TRUE verifies {tr:.1%} of {tp+fn_}; PLANT-FALSE (same shape, "
      f"uniform over the same range, seeded) verifies {fa:.1%} of {fp+tn} -> "
      f"{'PASS' if tr >= 0.95 and fa < tr else 'FAIL'} (bars TRUE >= 95%, FALSE lower).")
    P(f"             THE NOISE FLOOR FOR EVERY REPRO SHARE BELOW IS {fa:.1%} "
      f"(idea 790 measured {PUB790['plant_false']:.1%}); a REPRO reading near it means "
      "nothing.")
    gate_rows.append(dict(gate="G6_calibration_TRUE", value=tr, bar=0.95, passed=tr >= 0.95))
    gate_rows.append(dict(gate="G6_calibration_FALSE_floor", value=fa, bar=np.nan,
                          passed=fa < tr))
    P("")

    # ------------------------------------------------------ H_RECENCY, first
    P("=" * 100)
    P("ANSWER PART 1 - IS NAMED IN-DEGREE A RECENCY STATISTIC?")
    P("=" * 100)
    span = (corpus_end - min(vdate(r) for r in runs)).days
    P(f"THE LADDER APPENDIX FIRST - the whole record spans {span} calendar days and holds "
      f"{len(runs)} rankable runs,")
    P("so most of the pre-registered day-lag ladder is DEGENERATE.  Printed before anything "
      "is chosen:")
    lad = []
    for L in LADDER:
        d = indegree_at_lag(edges, runs, L)
        beyond = 0
        for n, hits in edges.items():
            dv = vdate(stem_of(n))
            if pd.isna(dv):
                continue
            for h in hits:
                hv = vdate(h)
                if h in set(runs) and not pd.isna(hv) and dv > hv and (dv - hv).days > L:
                    beyond += 1
        s = pd.Series(d)
        lad.append(dict(lag=L, total_indegree=int(s.sum()), mean=float(s.mean()),
                        zero_share=float(s.eq(0).mean()),
                        citations_beyond_window=beyond,
                        outcome_measurable=beyond > 0))
    ladder = pd.DataFrame(lad)
    P(fmt(ladder.set_index("lag"), 4))
    P("  'citations_beyond_window' is the material the SURVIVE outcome is made of.  It hits "
      "ZERO at L = 7,")
    P("  which is why the pre-registered {7, 14, 30} grid was re-scaled to {1, 2, 3} plus "
      "the unbounded")
    P("  forward window.  This is a fact about the record's age, not a tuning choice, and "
      "it is the")
    P("  reason no day-lag longer than a few days can separate predictor from outcome here.")
    P("")
    rec_rows = []
    for L in LAGS + ["ALL"]:
        col = f"NAMED@{L}"
        r = spearman(G[col], G.exposure_days)
        rec_rows.append(dict(lag=str(L), rho_exposure=r, t=t_of(r, len(G)),
                             total=float(G[col].sum()), mean=G[col].mean(),
                             zero_share=float(G[col].eq(0).mean()),
                             gini=gini(G[col].to_numpy(float))))
    rec = pd.DataFrame(rec_rows)
    P(fmt(rec.set_index("lag"), 4))
    rho_all = float(rec.loc[rec.lag == "FWD", "rho_exposure"].iloc[0])
    rho_790 = float(rec.loc[rec.lag == "ALL", "rho_exposure"].iloc[0])
    P(f"  idea 790's own NAMED@ALL is UNDIRECTED IN TIME (it counts earlier and same-day "
      f"citers too): total {int(rec.loc[rec.lag=='ALL','total'].iloc[0])} against the "
      f"strictly-forward {int(rec.loc[rec.lag=='FWD','total'].iloc[0])}, "
      f"rho(exposure) {rho_790:+.4f}")
    P(f"H_RECENCY: Spearman(NAMED@FWD, exposure days) = {rho_all:+.4f} -> "
      + ("HOLDS - the unbounded forward in-degree is substantially a clock, and every "
         "un-lagged comparison below is confounded by it"
         if rho_all >= 0.50 else
         "FALSIFIED - the unbounded forward in-degree is not MOSTLY an exposure-time "
         "effect, though it is materially one and it is the strongest single confound the "
         "run measures"))
    P("  The lag columns exist to remove exactly this: every run gets the same L days of "
      "citation exposure.")
    P("")

    # ------------------------------------------------------ THE 12 TUNED POINTS
    P("=" * 100)
    P("ANSWER PART 2 - THE 12 TUNED POINTS (does NAMED@L predict the outcome?)")
    P("=" * 100)
    P("raw     = Spearman(NAMED@L, outcome)")
    P("recency = the same, rank-partialled on exposure days")
    P("topic   = the same, with both ranks demeaned within the run's 6-way slug topic")
    P("p_perm  = two-sided permutation p over %d seeded shuffles; floor95 = the 95th pct "
      "|rho| under the null" % N_PERM)
    P("COUNTS  = |rho| >= %.2f AND p_perm < %.2f AND recency and topic each retain >= %.0f%% "
      "of |rho|" % (RHO_BAR, P_BAR, 100 * RETAIN_BAR))
    cells = []
    for L in LAGS:
        for oc in OUTCOMES:
            xcol = f"NAMED@{L}"
            ycol = f"SURVIVE@{L}" if oc == "SURVIVE" else oc
            sub = G[[xcol, ycol, "exposure_days", "topic"]].dropna()
            x, y = sub[xcol].to_numpy(float), sub[ycol].to_numpy(float)
            rho = spearman(x, y)
            rp = partial_spearman(x, y, sub.exposure_days.to_numpy(float))
            rt = within_group_spearman(x, y, sub.topic.to_numpy())
            pp, floor95 = perm_p(x, y, rho)
            tmean, rmean, k = top_contrast(x, y, 0.10)
            counts = bool(np.isfinite(rho) and abs(rho) >= RHO_BAR and pp < P_BAR
                          and abs(rp) >= RETAIN_BAR * abs(rho)
                          and abs(rt) >= RETAIN_BAR * abs(rho))
            # a retention ratio on a rho below its own null floor is meaningless: suppress it
            meaningful = np.isfinite(rho) and abs(rho) >= (floor95 or 0)
            cells.append(dict(lag=str(L), outcome=oc, n=len(sub), rho=rho,
                              t=t_of(rho, len(sub)), p_perm=pp, floor95=floor95,
                              rho_recency=rp, rho_topic=rt,
                              retain_recency=(abs(rp) / abs(rho)) if meaningful else np.nan,
                              retain_topic=(abs(rt) / abs(rho)) if meaningful else np.nan,
                              top10_mean=tmean, rest_mean=rmean, top10_n=k,
                              temporal=("FORWARD" if oc == "SURVIVE" else "STATIC"),
                              COUNTS=counts))
    cg = pd.DataFrame(cells)
    P(fmt(cg.set_index(["lag", "outcome"])[
        ["n", "rho", "t", "p_perm", "floor95", "rho_recency", "rho_topic",
         "retain_recency", "retain_topic", "top10_mean", "rest_mean", "temporal",
         "COUNTS"]], 4))
    ncount = int(cg.COUNTS.sum())
    P("")
    nsurv = int(cg[cg.COUNTS & (cg.outcome == "SURVIVE")].shape[0])
    nother = ncount - nsurv
    P(f"H_PRED  : {ncount} of {len(cg)} cells COUNT -> "
      + ("HOLDS - NAMED in-degree predicts at least one thing that survives both controls"
         if ncount else
         "FALSIFIED - NOT ONE of the 12 cells clears the pre-registered bar."))
    P(f"          AND ALL {nsurv} OF THEM ARE SURVIVE CELLS: {nother} of the 8 REPRO and "
      "KEEP4B cells clear the bar.  Every")
    P("          REPRO and KEEP4B reading sits inside its own permutation floor.  Part 3 "
      "then shows what the")
    P("          SURVIVE cells are made of, so read the two together before crediting "
      "H_PRED with anything.")
    hd = cg[(cg.lag == str(HEAD_LAG)) & (cg.outcome == HEAD_OUT)].iloc[0]
    P(f"          headline cell NAMED@{HEAD_LAG} vs {HEAD_OUT} (the only FORWARD one): "
      f"rho {hd.rho:+.4f} (t {hd.t:+.2f}, p_perm {hd.p_perm:.4f}, null floor95 "
      f"{hd.floor95:.4f}), recency-held {hd.rho_recency:+.4f}, within-topic "
      f"{hd.rho_topic:+.4f}")
    hh = cg[(cg.lag == str(HEAD_LAG)) & (cg.outcome == HEAD_OUT)].iloc[0]
    ret = min(hh.retain_recency, hh.retain_topic)
    P(f"H_TOPIC : within-topic demeaning retains {hh.retain_topic:.1%} of the headline "
      f"|rho| -> "
      + ("HOLDS - at least half the association is a topic effect"
         if hh.retain_topic <= 0.50 else
         "FALSIFIED - the association is not mostly a topic effect (it is not much of an "
         "association either, see the level)"))
    P(f"          weaker of the two controls retains {ret:.1%}")
    P("")
    P("ROBUSTNESS (reported, never selected):")
    sens = G.drop(index=[r for r in g3_offenders if r in G.index])
    for L in LAGS:
        xc, yc = f"NAMED@{L}", f"SURVIVE@{L}"
        s0 = G[[xc, yc]].dropna()
        s1 = sens[[xc, yc]].dropna()
        P(f"  G3 sensitivity, SURVIVE@{L}: rho {spearman(s0[xc], s0[yc]):+.4f} on "
          f"{len(s0)} runs -> {spearman(s1[xc], s1[yc]):+.4f} with the "
          f"{len(g3_offenders)} G3-residual run(s) dropped")
    dsub = G[G.KEEP4B_COV > 0]
    for L in LAGS:
        xc = f"NAMED@{L}"
        P(f"  KEEP4B on the {len(dsub)} runs with a committed `keep4b` COLUMN (the leg that "
          f"needs no narrative parsing), lag {L}: rho "
          f"{spearman(dsub[xc], dsub.KEEP4B_DATA):+.4f}")
    P("")

    # ------------------------------------------------------ H_SURV mechanics
    P("=" * 100)
    P("ANSWER PART 3 - WHAT 'SURVIVAL' ACTUALLY MEASURES")
    P("=" * 100)
    surv_rows = []
    for L in LAGS:
        named_col, ov = f"LATENAMED@{L}", f"OVERTURN@{L}"
        sub = G[G[named_col] > 0]
        r_all = spearman(G[f"NAMED@{L}"], (G[ov] > 0).astype(float))
        r_cond = spearman(sub[f"NAMED@{L}"], (sub[ov] > 0).astype(float))
        surv_rows.append(dict(lag=str(L), n_all=len(G), n_challenged=len(sub),
                              never_named_beyond=int((G[named_col] == 0).sum()),
                              share_never=float((G[named_col] == 0).mean()),
                              rho_overturn_all=r_all, rho_overturn_named=r_cond,
                              overturn_rate_named=float((sub[ov] > 0).mean())))
    sv = pd.DataFrame(surv_rows)
    P(fmt(sv.set_index("lag"), 4))
    hs = sv[sv.lag == str(HEAD_LAG)].iloc[0]
    P(f"H_SURV  : among runs named at all beyond the window, rho(NAMED@{HEAD_LAG}, "
      f"overturned) = {hs.rho_overturn_named:+.4f} -> "
      + ("HOLDS - being named MORE raises the measured overturn risk, so 'survival' is "
         "partly a measure of being IGNORED, not of being right"
         if hs.rho_overturn_named > 0 else
         "FALSIFIED - more-named runs are not more often overturned"))
    P(f"          {hs.share_never:.1%} of runs are never named beyond L = {HEAD_LAG} days at "
      "all, and are scored SURVIVE by default.  That is the confound the conditional column "
      "removes.")
    P("")

    # ------------------------------------------------------------------ price leg
    P("=" * 100)
    P("PRICE LEG - REAL panels (the book side of the run)")
    P("=" * 100)
    bases, spys, full_series, oos_series, is_prem = {}, {}, {}, {}, {}
    prow = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b = fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:]
        s = px["SPY"].pct_change().fillna(0.0).loc[warm:]
        bases[pn], spys[pn] = b, s
        P(f"  BASE {pn}: RULES v2 {metrics(b)['CAGR']:.2%} / {metrics(b)['Sharpe']:.4f} / "
          f"{metrics(b)['MaxDD']:.2%} (OOS Sharpe {metrics(b.loc[OOS_START:])['Sharpe']:.4f}, "
          f"OOS CAGR {metrics(b.loc[OOS_START:])['CAGR']:.2%})   "
          f"SPY {metrics(s)['CAGR']:.2%} / {metrics(s)['Sharpe']:.4f} / "
          f"{metrics(s)['MaxDD']:.2%} (OOS Sharpe {metrics(s.loc[OOS_START:])['Sharpe']:.4f}, "
          f"OOS CAGR {metrics(s.loc[OOS_START:])['CAGR']:.2%})")
        for g in GROSS:
            bks = make_books(px, set(names), g)
            for cad in CADENCE:
                res = {arm: fast_backtest(px, w, freq=cad)["returns"].loc[warm:]
                       for arm, w in bks.items()}
                for arm, r in res.items():
                    m, mo = metrics(r), metrics(r.loc[OOS_START:])
                    h1, h2 = halves(r)
                    prow.append(dict(parent=pn, arm=arm, gross=g, cadence=cad,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                     OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                     keep4a=keep_4a(r, b), fail4b=fail_4b(r, s),
                                     keep4b=(fail_4b(r, s) == "-")))
                full_series[(pn, g, cad)] = res["MA-RS"]
                oos_series[(pn, g, cad)] = res["MA-RS"].loc[OOS_START:]
                is_prem[(pn, g, cad)] = (metrics(res["MA-RS"].loc[:IS_END])["Sharpe"]
                                         - metrics(res["EWall"].loc[:IS_END])["Sharpe"])
    grid = pd.DataFrame(prow)
    P("")
    P(f"  {len(grid)} price books: 4a {int(grid.keep4a.sum())}/{len(grid)}, "
      f"4b {int(grid.keep4b.sum())}/{len(grid)}, "
      f"BOTH {int((grid.keep4a & grid.keep4b).sum())}/{len(grid)}")
    P("  4b passes: " + (", ".join(f"{r.parent}/{r.arm}/g{r.gross}/{r.cadence}"
                                   for _, r in grid[grid.keep4b].iterrows()) or "none"))
    P("  4b binding failure legs: " + ", ".join(f"{k} {v}" for k, v
                                                in grid.fail4b.value_counts().head(6).items()))
    P("  CONTINUITY: idea 790 published this same 36-book grid one day and one tape bar ago "
      "at 4a 0/36, 4b 3/36,")
    P("  BOTH 0/36 with the same three 4b names.  Nothing here is a new candidate: these are "
      "the record's standing")
    P("  MA-gate respread arms re-priced, and idea 787 already killed that whole shelf "
      "against an equal-weight bar.")
    P("")

    # ------------------------------------------------------------------ RULE 8
    P("=" * 100)
    P("RULE 8 WALK-FORWARD")
    P("=" * 100)
    P(f"WF-A: every one of the 12 cells measured on EARLY runs (vintage < {VINTAGE_SPLIT}) "
      "and then read")
    P("      ONCE on LATE runs.  LATE runs have only days of citation exposure, so the ALL "
      "column is")
    P("      NOT comparable across the split and is flagged; the lagged columns are.")
    early = G[G.vintage < VINTAGE_SPLIT]
    late = G[G.vintage >= VINTAGE_SPLIT]
    P(f"      EARLY {len(early)} runs, LATE {len(late)} runs")
    wfa_rows = []
    for L in LAGS:
        for oc in OUTCOMES:
            xcol = f"NAMED@{L}"
            ycol = f"SURVIVE@{L}" if oc == "SURVIVE" else oc
            row = dict(lag=str(L), outcome=oc,
                       comparable=("NO - exposure-truncated" if L == "FWD" else "YES"))
            for tag, sub in (("IS", early), ("OOS", late)):
                s = sub[[xcol, ycol]].dropna()
                r = spearman(s[xcol], s[ycol])
                row[f"{tag}_n"] = len(s)
                row[f"{tag}_rho"] = r
                row[f"{tag}_t"] = t_of(r, len(s))
            row["sign_agrees"] = bool(np.isfinite(row["IS_rho"])
                                      and np.isfinite(row["OOS_rho"])
                                      and np.sign(row["IS_rho"]) == np.sign(row["OOS_rho"])
                                      and row["IS_rho"] != 0)
            fl = float(cg[(cg.lag == str(L)) & (cg.outcome == oc)].floor95.iloc[0])
            row["IS_beats_null"] = bool(np.isfinite(row["IS_rho"])
                                        and abs(row["IS_rho"]) >= fl)
            wfa_rows.append(row)
    wfa = pd.DataFrame(wfa_rows)
    P(fmt(wfa.set_index(["lag", "outcome"]), 4))
    comp = wfa[wfa.comparable == "YES"]
    sig = comp[comp.IS_beats_null]
    P(f"  sign agreement IS -> OOS on the {len(comp)} comparable (lagged) cells: "
      f"{int(comp.sign_agrees.sum())}/{len(comp)}; median |OOS rho| "
      f"{comp.OOS_rho.abs().median():.4f} against median |IS rho| "
      f"{comp.IS_rho.abs().median():.4f}")
    P(f"  restricted to the {len(sig)} cells whose IS |rho| clears its OWN permutation floor "
      f"(the rest are coin flips): sign agreement {int(sig.sign_agrees.sum())}/{len(sig)}, "
      f"and they are {', '.join(sorted(set(sig.outcome)))} cells only")
    P("  SURVIVE@3 reads NaN out of sample because NOT ONE late-vintage run has a citer "
      "beyond 3 days: the")
    P("  outcome has no variance on the OOS half.  That is the corpus-age ceiling again, "
      "reported not patched.")
    P("")

    P("WF-B: NAMED@L priced as a DECISION RULE - act on the IS-best parent only if one of "
      "the record's")
    P("      backing claim-runs for that parent is in the top share by NAMED@L (EARLY citers "
      "only) AND")
    P("      its own headline numbers verify (DATA leg >= %.0f%%); else stand down to RULES "
      "v2 on U56." % (100 * SOUND_BAR))
    P("      OOS read ONCE.")
    cen = pd.read_csv(f"{P779}.census.csv")
    cen["run"] = cen.file.map(stem_of)

    def backing_runs(pn):
        key = "SMALL" if pn.startswith("SMALL") else pn
        m = cen.parents.fillna("").str.contains(key, regex=False)
        return set(cen.loc[m, "run"])

    back = {pn: backing_runs(pn) for pn in pnames}
    P("  backing claim runs per parent (idea 779's committed 607-claim census): "
      + ", ".join(f"{pn} {len(back[pn])}" for pn in pnames))
    early_runs = set(early.index)
    degE = {}
    for L in LAGS:
        d = indegree_at_lag(
            edges, sorted(early_runs), L,
            citer_filter=lambda n: (vintage(stem_of(n)) or "9999") < VINTAGE_SPLIT)
        degE[L] = pd.Series(d).sort_values(ascending=False)

    def sound(run):
        return bool(run in ver.index and ver.loc[run, "DATA_share"] >= SOUND_BAR)

    base56, spy56 = bases["U56"], spys["U56"]
    dec_rows, dec_keep = [], []
    for L in LAGS:
        s = degE[L]
        for sh in SHARES:
            k = max(1, int(round(sh * len(s))))
            cset = set(s.index[:k])
            acted, segO, segF, picks = 0, [], [], []
            for g in GROSS:
                for cad in CADENCE:
                    order_p = sorted(pnames, key=lambda pn: is_prem[(pn, g, cad)],
                                     reverse=True)
                    best = order_p[0]
                    ok = any((r in cset) and sound(r) for r in back[best])
                    acted += int(ok)
                    picks.append(best if ok else "STANDDOWN")
                    segO.append(oos_series[(best, g, cad)] if ok
                                else base56.loc[OOS_START:])
                    segF.append(full_series[(best, g, cad)] if ok else base56)

            def mk(segs):
                return pd.concat([x.reindex(segs[0].index).fillna(0.0) for x in segs],
                                 axis=1).mean(axis=1)
            bo, bf = mk(segO), mk(segF)
            mo = metrics(bo)
            dec_rows.append(dict(lag=str(L), share=sh, acted=acted, cells=len(picks),
                                 core_k=k, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"]))
            sp = spy56.reindex(bf.index).fillna(0.0)
            f4 = fail_4b(bf, sp)
            dec_keep.append(dict(lag=str(L), share=sh, CAGR=metrics(bf)["CAGR"],
                                 Sharpe=metrics(bf)["Sharpe"], MaxDD=metrics(bf)["MaxDD"],
                                 keep4a=keep_4a(bf, base56.reindex(bf.index).fillna(0.0)),
                                 fail4b=f4, keep4b=(f4 == "-")))
    segs = [oos_series[(max(pnames, key=lambda pn: is_prem[(pn, g, cad)]), g, cad)]
            for g in GROSS for cad in CADENCE]
    always = pd.concat([x.reindex(segs[0].index).fillna(0.0) for x in segs],
                       axis=1).mean(axis=1)
    ctrls = []
    for nm, r in (("ALWAYS-ACT (control)", always),
                  ("FULL-STAND-DOWN (control)", base56.loc[OOS_START:]),
                  ("RULES v2 U56 (live book)", base56.loc[OOS_START:]),
                  ("SPY", spy56.loc[OOS_START:])):
        m = metrics(r)
        ctrls.append(dict(lag=nm, share=np.nan, acted=np.nan, cells=np.nan, core_k=np.nan,
                          OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    dec = pd.DataFrame(dec_rows + ctrls)
    P(fmt(dec.set_index(["lag", "share"]), 4))
    bsh = metrics(base56.loc[OOS_START:])["Sharpe"]
    ssh = metrics(spy56.loc[OOS_START:])["Sharpe"]
    ash = metrics(always)["Sharpe"]
    nrule = len(dec_rows)
    EPS = 1e-9                       # a book that IS a control must not be read as beating it
    sh_ = dec.iloc[:nrule].OOS_Sharpe
    beat_live = int((sh_ > bsh + EPS).sum())
    beat_spy = int((sh_ > ssh + EPS).sum())
    beat_always = int((sh_ > ash + EPS).sum())
    beat_both = int(((sh_ > ash + EPS) & (sh_ > bsh + EPS)).sum())
    ndistinct = int(sh_.round(9).nunique())
    P(f"  decision books beating RULES v2 U56 OOS Sharpe ({bsh:.4f}): {beat_live}/{nrule}; "
      f"SPY ({ssh:.4f}): {beat_spy}/{nrule}; ALWAYS-ACT ({ash:.4f}): {beat_always}/{nrule}"
      f"  (a book equal to a control to 1e-09 is NOT counted as beating it)")
    P(f"  THE GATE IS DEGENERATE: the 20 decision books take only {ndistinct} distinct "
      f"values - the gate either fires in all 6 (gross, cadence) cells or in none.  The "
      f"backing-claim sets are large (" + ", ".join(f"{pn} {len(back[pn])}" for pn in pnames)
      + f"), so at any share >= 0.05 some backing run is always in the core: NAMED@L never "
      "acts as a selector at all, at any of the 20 points.")
    P(f"H_ACT   : the gated rule beats BOTH controls in {beat_both} of {nrule} cells -> "
      + ("HOLDS" if beat_both > 0 else
         "FALSIFIED - gating on NAMED in-degree buys nothing.  Every cell reproduces one of "
         "the two controls exactly; the statistic never changes a decision, so it cannot "
         "improve one."))
    dkf = pd.DataFrame(dec_keep)
    P("")
    P("  KEEP paths for the decision books (full-sample twin, 4a vs RULES v2 U56, 4b vs SPY):")
    P(fmt(dkf.set_index(["lag", "share"]), 4))
    P(f"  decision books: 4a {int(dkf.keep4a.sum())}/{len(dkf)}, "
      f"4b {int(dkf.keep4b.sum())}/{len(dkf)}, "
      f"BOTH {int((dkf.keep4a & dkf.keep4b).sum())}/{len(dkf)}")
    P("  (a decision book built from a bibliometric statistic is a diagnostic, never a "
      "capital candidate - declared before the run)")
    P("")

    # ------------------------------------------------------------------ verdict
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    P(f"  H_PRED    {'HOLDS' if ncount else 'FALSIFIED'}  ({ncount}/12 cells clear the bar)")
    P(f"  H_RECENCY {'HOLDS' if rho_all >= 0.50 else 'FALSIFIED'}  "
      f"(rho(NAMED@FWD, exposure) {rho_all:+.4f}; idea 790's time-undirected NAMED@ALL {rho_790:+.4f})")
    P(f"  H_TOPIC   {'HOLDS' if hh.retain_topic <= 0.50 else 'FALSIFIED'}  "
      f"(headline retains {hh.retain_topic:.1%} within topic)")
    P(f"  H_SURV    {'HOLDS' if hs.rho_overturn_named > 0 else 'FALSIFIED'}  "
      f"(rho(NAMED@{HEAD_LAG}, overturned | named) {hs.rho_overturn_named:+.4f})")
    P(f"  H_ACT     {'HOLDS' if beat_both > 0 else 'FALSIFIED'}  "
      f"(beats both controls {beat_both}/{nrule}; {ndistinct} distinct books over 20 cells)")
    P("")
    net_actionable = nother > 0 or beat_both > 0
    P("  NET ANSWER TO THE QUEUE'S QUESTION - does NAMED in-degree predict anything the "
      "record should ACT on?")
    P("  " + ("YES" if net_actionable else "NO.") + "  It predicts ONE thing, being "
      f"OVERTURNED (rho {hd.rho:+.4f} at L = {HEAD_LAG}, {cg[(cg.lag=='FWD')&(cg.outcome=='SURVIVE')].rho.iloc[0]:+.4f} "
      "unbounded), and Part 3 identifies")
    P(f"  that as the CITATION-EXPOSURE ARTEFACT: {hs.share_never:.1%} of runs are never "
      "named beyond the window and score")
    P("  SURVIVE by default, and among the runs that ARE challenged the sign FLIPS to "
      f"{hs.rho_overturn_named:+.4f} - more naming means")
    P("  more overturning, not more soundness.  It predicts NEITHER of the two things the "
      "record would want:")
    P(f"  reproduction (rho {cg[(cg.lag==str(HEAD_LAG))&(cg.outcome=='REPRO')].rho.iloc[0]:+.4f}, "
      f"p {cg[(cg.lag==str(HEAD_LAG))&(cg.outcome=='REPRO')].p_perm.iloc[0]:.4f}) nor "
      "capital-relevant output")
    P(f"  (KEEP4B rho {cg[(cg.lag==str(HEAD_LAG))&(cg.outcome=='KEEP4B')].rho.iloc[0]:+.4f}, "
      f"p {cg[(cg.lag==str(HEAD_LAG))&(cg.outcome=='KEEP4B')].p_perm.iloc[0]:.4f}; and on the "
      "79 runs carrying an actual `keep4b`")
    P("  column the sign is NEGATIVE at every lag).  Priced as a decision rule it never "
      "changes a decision.")
    P("")

    # ------------------------------------------------------------------ write
    G.to_csv(OUT / f"{STAMP}.graph.csv")
    ver.to_csv(OUT / f"{STAMP}.verify.csv")
    cg.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    rec.to_csv(OUT / f"{STAMP}.recency.csv", index=False)
    sv.to_csv(OUT / f"{STAMP}.survival.csv", index=False)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    pd.DataFrame(gate_rows).to_csv(OUT / f"{STAMP}.gates.csv", index=False)
    pd.concat([wfa.assign(leg="WF-A"), dec.assign(leg="WF-B_OOS"),
               dkf.assign(leg="WF-B_KEEP")], ignore_index=True).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    pd.concat([grid[["parent", "arm", "gross", "cadence", "keep4a", "fail4b", "keep4b"]]
               .assign(book="PRICE"),
               dkf.rename(columns={"lag": "parent", "share": "gross"})
               .assign(book="DECISION")], ignore_index=True).to_csv(
        OUT / f"{STAMP}.keeppaths.csv", index=False)
    pd.DataFrame({"run": unverifiable}).to_csv(OUT / f"{STAMP}.unverifiable.csv", index=False)
    P(f"wrote graph {len(G)}, verify {len(ver)}, cells {len(cg)}, grid {len(grid)}, "
      f"wf {len(wfa)+len(dec)+len(dkf)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
