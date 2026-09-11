#!/usr/bin/env python3
"""Idea 779 (lane C, 2026-09-11) - does-the-MIN-GAP-PAIR-restatement-change-any-published-VERDICT-not-just-the-count.

QUESTION
--------
Idea 778 re-scored idea 567/774's 607-claim panel-ordering census against the MIN-GAP PAIR
bar (RSS restricted to the two panels that bracket the margin, rho = 0) instead of idea 774's
RSS-over-every-named-parent, and reported the movement as a COUNT: net vs POOLED +21/+18/
+20/+21 at D = 3/6/12/24.  The queue's objection is that a moved count is not a moved
conclusion.  This run READS the claims that move and asks whether any of them carries a
headline the rest of the record LEANS ON - i.e. whether the restatement retires anything the
record is still using, or only reshuffles sentences nobody cites.

WHAT "RELIED ON ELSEWHERE" IS MADE TO MEAN (declared before any count is read)
-----------------------------------------------------------------------------
Reliance is measured from the committed corpus only, never from judgement, on four legs:
    VENUE  the claim sits in a CONTROL document - RULES.md, PROTOCOL.md, CHANGELOG.md,
           LEADERBOARD.md, QUEUE.md or a *MEMO.md.  These are the documents the project
           acts from, so a claim living in one is load-bearing by construction.
    CITED  the claim's source file is named, or its idea number is cited as "idea NNN", in
           at least CITE_MIN OTHER committed files.  Self-citations, same-run artefacts, and
           the two INDEX documents (LEADERBOARD.md, QUEUE.md, which name every committed
           script by PROTOCOL rule 5) are excluded from the CITING side by construction.
    ECHO   at least one of the claim's own DISTINCTIVE numbers (>= 4 significant digits, so
           "2.0" and "0.75" cannot qualify), in its own committed spelling, re-appears in a
           DIFFERENT run's committed file - a downstream restatement of that number.
    QUEUED the claim's file backs an idea still OPEN or IN PROGRESS in QUEUE.md, i.e. work
           is scheduled on top of it right now.
    ANY    = VENUE or CITED or ECHO or QUEUED           (the permissive reading)
    STRICT = VENUE and (CITED or ECHO)                  (the demanding reading)
The headline answer is reported at every leg, and - this is the part that makes the number
mean anything - always beside the SAME leg measured on the claims that do NOT move.  A
mover-reliance rate is uninformative on its own: if 60% of the whole census is "relied on",
a 60% rate among movers is the base rate, not a finding.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. CLAIM SET in {ALL, 2PANEL, 3PANEL, NESTED_PAIR, NZ}
         ALL          all 607 census claims
         2PANEL       claims quoting exactly two panels
         3PANEL       claims quoting all three
         NESTED_PAIR  claims whose min-gap pair is B136|U56 (the nested pair 778 isolated)
         NZ           claims with a strictly positive margin
    2. BAR b in {1.0, 2.0} sd
All 5 x 2 = 10 grid points are reported.  REPORTED (never selected) axes: draw count
D in {3, 6, 12, 24}, period (FULL / IS / OOS), reliance leg (6), direction (OUT->IN vs
IN->OUT), statistic family (5).

PRE-REGISTERED HYPOTHESES (written before any new number was read)
-----------------------------------------------------------------
H_MOVE : the movers are a small, stable set - the PAIR_INDEP vs POOLED mover set at bar 1.0
         is under 10% of the census at every (claim set, D).  Falsified above 10%.
H_LEAN : the movers are ENRICHED in relied-on claims relative to the non-movers (mover ANY
         rate exceeds non-mover ANY rate by more than 10 pp at the headline point, D=6,
         FULL, ALL, bar 1.0).  This is the queue's worry stated as a testable claim.
         Falsified if the movers are at or below the base rate.
H_HEAD : at least one mover carries a STRICT headline, i.e. lives in a control document AND
         is cited or echoed elsewhere - so the restatement would retire something the record
         is actually using.  Falsified if the STRICT mover count is 0 at every grid point.

GATES (pre-registered, run and printed before any new number is read)
    G1 harvest   : a fresh harvest of the committed record reproduces idea 567/774/778's 607
                   census rows exactly.                                    bar 607 of 607
    G2 floors    : per-parent floors rebuilt from prices match idea 774/778's committed
                   .floors.csv on all 60 (statistic, D, period) rows.             bar 1e-12
    G3 identity  : fast_backtest vs engine.backtest on one book per parent.       bar 1e-12
    G4 headline  : idea 778's published PAIR_INDEP net-vs-POOLED counts (+21/+18/+20/+21 at
                   D=3/6/12/24, bar 1.0, ALL) re-derived TWICE - once from 778's own
                   committed .moves.csv and once rebuilt from prices by this run.  bar exact
    G5 reliance  : the reliance measurement is self-exclusive and non-degenerate - no file
                   counts as citing itself or its own run's artefacts, every leg is computed
                   on the full census (not just movers) so a base rate exists, and each of
                   VENUE / CITED / ECHO must sit strictly inside 2%-98% or it measures
                   nothing.  The first version of this script FAILED this gate (CITED
                   100.0%, ANY 100.0%) because it let the two index documents count as
                   citers; the leg was rebuilt before any answer was read and the failure is
                   printed by the run.                                        bar exact

RULE 8 WALK-FORWARD (required, run whatever the census says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: rebuild the floors on IS returns only and on OOS returns only,
       recompute the mover set and every reliance count in each period, and report whether
       the moved-AND-relied-on claims are the SAME OBJECT out of sample (set overlap /
       Jaccard between the IS and OOS mover sets, and the rate in each period).
    WF-B on a BOOK: the restatement is a DECISION RULE about which panel-ordering claims may
       be acted on, so it is priced as one.  In each (gross, cadence) cell rank the three
       parents by IS MA-gate premium; ACT on the IS-best parent (trade MA-RS there) only if
       the IS span clears bar b times the MIN-GAP PAIR floor AND the claim set backing that
       pair survives the reliance filter, else STAND DOWN to the live book (RULES v2 on U56).
       OOS is read ONCE for all 10 decision books and compared to RULES v2 U56 and SPY.
       778's always-act and full-stand-down books are the controls.
    KEEP paths 4a and 4b are evaluated for every book on the price grid (REAL panels and
       idea 774's independent draws) AND for every decision book.  Stated up front: a DRAW
       panel is a seeded random 36-name subset, not a rule anyone can trade, so a 4b pass on
       a draw is a diagnostic, not a candidate.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents, so every
    stock-side level carries a survivorship premium; the LEVEL floors (SHARPE, CAGR, MAXDD)
    are lower bounds on true dispersion.  An arm-minus-arm premium on the same panel largely
    cancels it.  The three parents also start on different dates (U56/B136 2008, SMALL 2010).

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and the committed
artefacts of ideas 774/778; modifies nothing but its own outputs:
    .grid.csv .floors.csv .census.csv .movers.csv .reliance.csv .verdicts.csv
    .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import collections
import itertools
import re
import sys
import time
import zlib
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

COST = 10.0
MA_WIN = 200
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
K_DRAW = 36
N_SEED = 24
DRAW_COUNTS = [3, 6, 12, 24]
BARS = [1.0, 2.0]
CLAIM_SETS = ["ALL", "2PANEL", "3PANEL", "NESTED_PAIR", "NZ"]
LEGS = ["VENUE", "CITED", "ECHO", "QUEUED", "ANY", "STRICT"]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]
PERIODS = ("FULL", "IS", "OOS")
CITE_MIN = 1                      # declared, not tuned: "cited by at least one OTHER file"
CONTROL_DOCS = ("RULES.md", "PROTOCOL.md", "CHANGELOG.md", "LEADERBOARD.md", "QUEUE.md")
# named every committed script by PROTOCOL rule 5, so they cite everything by construction
INDEX_DOCS = ("LEADERBOARD.md", "QUEUE.md")

P774 = OUT / "2026-09-11_how-many-of-the-record-s-TWO-PANEL-claims-would-flip-under-a-PARENT-SPECIFIC-floor_C"
P778 = OUT / "2026-09-11_is-the-RSS-BAR-the-right-object-when-the-two-parents-OVERLAP_cloud"
# idea 778's published PAIR_INDEP net-vs-POOLED counts, bar 1.0, subset ALL, FULL period
PUB778 = {3: 21, 6: 18, 12: 20, 24: 21}
TOL = 1e-12

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G3)."""
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


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


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


# ------------------------------------------------------------------------- panels
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


def draws(parent, names, n_seed=N_SEED, k=K_DRAW):
    """crc32-seeded k-matched INDEPENDENT draws, `DRAW|{parent}|{seed}` (312/567/774 scheme)."""
    pool = np.array(sorted(names))
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"DRAW|{parent}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        pick = sorted(rng.choice(pool, size=min(k, len(pool)), replace=False).tolist())
        out.append((sd, pick))
    return out


# ------------------------------------------------------------------------- census
# idea 567/774/778's harvester, verbatim (778 added the MIN-GAP pair column).
PANELS_RE = re.compile(r"\b(U56|B136|SMALL\d{2,4}|SMALL)\b")
NUM_RE = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")
FAMILY_KEYS = [
    ("PREM_SHARPE", ("premium", "dsharpe", "d sharpe", "advantage", "gate premium", "selection")),
    ("PREM_CAGR", ("dcagr", "d cagr", "pp/yr", "pp / yr")),
    ("SHARPE", ("sharpe",)),
    ("CAGR", ("cagr", "return")),
    ("MAXDD", ("maxdd", "max dd", "drawdown", "dd")),
]


def classify(text):
    t = text.lower()
    for fam, keys in FAMILY_KEYS:
        if any(k in t for k in keys):
            return fam
    return None


def sentences(txt):
    txt = txt.replace("\n", " ")
    return re.split(r"(?<=[.;!?])\s+|\|", txt)


def harvest(paths):
    """Committed sentences quoting a number against >=2 of the three panels."""
    rows = []
    for p in paths:
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        for s in sentences(txt):
            if len(s) > 600:
                continue
            found = PANELS_RE.findall(s)
            fams = {("SMALL" if f.startswith("SMALL") else f) for f in found}
            if len(fams) < 2:
                continue
            fam = classify(s)
            if fam is None:
                continue
            vals = {}
            for m in PANELS_RE.finditer(s):
                key = "SMALL" if m.group(1).startswith("SMALL") else m.group(1)
                tail = s[m.end(): m.end() + 40]
                nums = [float(x) for x in NUM_RE.findall(tail)
                        if not re.fullmatch(r"[-+]?\d{2,4}", x)]
                if nums and key not in vals:
                    vals[key] = nums[0]
            if len(vals) < 2:
                continue
            pairs = sorted(vals.items(), key=lambda kv: kv[1])
            order = [v for _, v in pairs]
            gaps = [b - a for a, b in zip(order, order[1:])]
            margin = min(gaps) if gaps else np.nan
            if not np.isfinite(margin):
                continue
            j = int(np.argmin(gaps))
            mpair = "|".join(sorted((pairs[j][0], pairs[j + 1][0])))
            rows.append(dict(file=p.name, family=fam, n_panels=len(vals),
                             margin=abs(margin), span=abs(order[-1] - order[0]),
                             parents="+".join(sorted(vals)), mpair=mpair,
                             claim=s.strip()[:240]))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------- bars
def pkey(name, small_name):
    return small_name if name == "SMALL" else name


def bar_rss_indep(named, stat, floors_pp, small_name):
    """idea 774's incumbent: RSS over EVERY named parent."""
    f = floors_pp[stat]
    v = [f[pkey(p, small_name)] for p in named if pkey(p, small_name) in f]
    return float(np.sqrt(np.sum(np.square(v)))) if v else np.nan


def bar_pair_indep(mpair, stat, floors_pp, small_name):
    """idea 778's restatement: RSS over the TWO panels bracketing the margin."""
    f = floors_pp[stat]
    i, j = [pkey(x, small_name) for x in mpair.split("|")]
    if i not in f or j not in f:
        return np.nan
    return float(np.sqrt(f[i] ** 2 + f[j] ** 2))


def bar_pooled(stat, floors_pp):
    """idea 567's incumbent: one pooled floor for every claim in the family."""
    return float(np.nanmean(list(floors_pp[stat].values())))


# --------------------------------------------------------------- reliance machinery
IDEA_RE = re.compile(r"\bidea\s+(\d{2,4})\b", re.IGNORECASE)
STEM_IDEA_RE = re.compile(r"^\s*(\d{2,4})\.\s")


def corpus_files():
    """Every committed markdown file in research/ (the record), deduplicated."""
    paths = sorted({p for p in (list((ROOT / "research").glob("*.md"))
                                + list((ROOT / "research" / "backtests").glob("*.md")))
                    if p.is_file()})
    return paths


def file_idea_numbers(paths):
    """Map file -> the idea numbers the RECORD assigns to it (from QUEUE 'Done' rows and
    LEADERBOARD rows that name the script), so 'idea NNN' citations resolve to a file."""
    f2i = collections.defaultdict(set)
    for src in (ROOT / "research" / "QUEUE.md", ROOT / "research" / "LEADERBOARD.md"):
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
                stem = m.group(1)[:-3]
                for n in nums:
                    f2i[stem].add(n)
    return f2i


def sigdigits(tok):
    """Significant digits of a committed decimal token ('0.2464' -> 4, '2.0' -> 1)."""
    t = tok.lstrip("+-")
    if "." not in t:
        return 0
    body = t.replace(".", "").lstrip("0")
    return len(body.rstrip("0")) if body.rstrip("0") else 0


def build_reliance(census, paths):
    """Per-CLAIM reliance flags, measured from the corpus.

    Two exclusions make the measure mean something rather than saturate at 100%:
      * SELF: a file is never evidence for its own claims, and neither is any other
        artefact of the SAME run (same stem), which is written by the same script.
      * INDEX: LEADERBOARD.md and QUEUE.md name every committed script by PROTOCOL rule 5,
        so they cite everything by construction.  They are excluded from the CITING side
        (they remain eligible as VENUES, which is a different claim about a claim).
    Both exclusions were declared before any rate was read; the first version of this run
    omitted the INDEX exclusion, gate G5 read CITED at 100.0% and failed it, and the leg was
    rebuilt.  That failure is reported, not hidden.
    """
    texts = {p.name: p.read_text(errors="ignore") for p in paths}
    stem_of = {p.name: p.name.split(".")[0] for p in paths}
    citers = {n: t for n, t in texts.items() if n not in INDEX_DOCS}

    f2i = file_idea_numbers(paths)
    ideas_in = {n: {m.group(1) for m in IDEA_RE.finditer(t)} for n, t in citers.items()}

    # queue reliance: file/stem/idea named in an OPEN or IN PROGRESS queue entry
    qtxt = (ROOT / "research" / "QUEUE.md").read_text(errors="ignore")
    head = qtxt.split("## Done")[0]
    open_ideas = {m.group(1) for m in IDEA_RE.finditer(head)}
    open_stems = set(re.findall(r"research/backtests/([^\s`|)]+)\.py", head))

    cite_cache, echo_cache = {}, {}
    rows = []
    for _, r in census.iterrows():
        fn = r.file
        stem = stem_of.get(fn, fn.split(".")[0])
        venue = bool(fn in CONTROL_DOCS or "MEMO" in fn.upper())
        # the idea numbers this CLAIM is attributable to
        if fn in INDEX_DOCS or fn in CONTROL_DOCS:
            src_ideas = {m.group(1) for m in IDEA_RE.finditer(r.claim)}
            m0 = STEM_IDEA_RE.match(r.claim)
            if m0:
                src_ideas.add(m0.group(1))
            ck = ("CLAIM", tuple(sorted(src_ideas)))
        else:
            src_ideas = set(f2i.get(stem, set()))
            ck = ("FILE", stem, tuple(sorted(src_ideas)))
        if ck not in cite_cache:
            hits = set()
            for other, txt in citers.items():
                if other == fn or stem_of.get(other, "") == stem:
                    continue                               # self / same-run excluded
                if ck[0] == "FILE" and stem and stem in txt:
                    hits.add(other)
                    continue
                if src_ideas and (src_ideas & ideas_in[other]):
                    hits.add(other)
            cite_cache[ck] = len(hits)
        cited = cite_cache[ck]
        # ECHO: a DISTINCTIVE number of this claim (>=4 significant digits, so 2.0 and 0.75
        # cannot qualify) re-appears in a different run's committed file
        toks = [t for t in dict.fromkeys(NUM_RE.findall(r.claim)) if sigdigits(t) >= 4]
        echo = 0
        for t in toks:
            k = (t, stem)
            if k not in echo_cache:
                echo_cache[k] = any(t in txt for other, txt in citers.items()
                                    if other != fn and stem_of.get(other, "") != stem)
            echo += int(echo_cache[k])
        queued = bool(stem in open_stems or (src_ideas & open_ideas))
        rows.append(dict(file=fn, venue=venue, cited=cited, echo=echo, queued=queued,
                         n_numbers=len(toks), src_ideas="|".join(sorted(src_ideas))))
    rel = pd.DataFrame(rows)
    rel["VENUE"] = rel.venue
    rel["CITED"] = rel.cited >= CITE_MIN
    rel["ECHO"] = rel.echo >= 1
    rel["QUEUED"] = rel.queued
    rel["ANY"] = rel.VENUE | rel.CITED | rel.ECHO | rel.QUEUED
    rel["STRICT"] = rel.VENUE & (rel.CITED | rel.ECHO)
    return rel


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 779 - does the MIN-GAP-PAIR restatement change any published VERDICT, "
      "not just the count?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}")
    P("# TUNED (2): CLAIM SET in " + str(CLAIM_SETS) + " x BAR in " + str(BARS)
      + "  -- all 10 points reported")
    P("# RELIANCE legs (declared, not tuned): " + str(LEGS)
      + f"; CITED bar = {CITE_MIN} other file(s)")
    P("")

    parents = real_panels()
    pnames = list(parents)
    small_name = [p for p in pnames if p.startswith("SMALL")][0]
    P("PARENTS: " + ", ".join(
        f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
        for k, v in parents.items()))
    P("")

    P("=" * 100)
    P("GATES (pre-registered; printed before any new number is read)")
    P("=" * 100)

    # ------------------------------------------------------------------ G1 harvest
    paths = corpus_files()
    fresh = harvest(paths)
    old = pd.read_csv(f"{P778}.census.csv")

    def key(d):
        return list(zip(d.file, d.family, d.n_panels, d.margin.round(12), d.span.round(12),
                        d.claim.str[:200]))

    ca, cb = collections.Counter(key(old)), collections.Counter(key(fresh))
    g1 = sum(min(v, cb[k]) for k, v in ca.items())
    P(f"G1 harvest   : idea 567/774/778's committed census rows reproduced by a fresh harvest "
      f"of {len(paths)} committed markdown files: {g1} of {len(old)} "
      f"(this run harvests {len(fresh)}; the surplus is files committed after 778 ran) -> "
      f"{'PASS' if g1 == len(old) == 607 else 'FAIL'}")
    cen = old.copy()

    # ------------------------------------------------------------------ G3 identity
    g3 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        a = fast_backtest(px, bk, freq="W")["returns"]
        b = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g3 = max(g3, float(np.abs(a.values - b.values).max()))
    P(f"G3 identity  : fast_backtest vs engine.backtest max |dret| = {g3:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g3 <= TOL else 'FAIL'}")

    # ------------------------------------------------------------------ price leg
    P("")
    P("=" * 100)
    P("PRICE LEG - REAL panels + idea 774's INDEPENDENT draws (rebuilds the floors)")
    P("=" * 100)
    rows = []
    spy_cache = {}

    def run_unit(pn, px, pick, kind, sd):
        cols = list(dict.fromkeys(list(pick) + ["SPY"]))
        sub = px[cols].dropna(how="all").ffill()
        out = []
        for g in GROSS:
            bks = make_books(sub, set(pick), g)
            for cad in CADENCE:
                res = {a: fast_backtest(sub, w, freq=cad) for a, w in bks.items()}
                warm = sub.index[260]
                base = {a: r["returns"].loc[warm:] for a, r in res.items()}
                for arm in ("EWall", "MA-RS"):
                    r = base[arm]
                    d = rowify(r, res[arm]["turnover"].loc[warm:])
                    d.update(parent=pn, kind=kind, seed=sd, arm=arm, gross=g, cadence=cad,
                             k=len(pick))
                    d["dSharpe_vs_EWall"] = d["Sharpe"] - metrics(base["EWall"])["Sharpe"]
                    d["dCAGR_vs_EWall"] = d["CAGR"] - metrics(base["EWall"])["CAGR"]
                    d["IS_dSharpe"] = (metrics(r.loc[:IS_END])["Sharpe"]
                                       - metrics(base["EWall"].loc[:IS_END])["Sharpe"])
                    d["OOS_dSharpe"] = (metrics(r.loc[OOS_START:])["Sharpe"]
                                        - metrics(base["EWall"].loc[OOS_START:])["Sharpe"])
                    d["IS_dCAGR"] = (metrics(r.loc[:IS_END])["CAGR"]
                                     - metrics(base["EWall"].loc[:IS_END])["CAGR"])
                    d["OOS_dCAGR"] = (metrics(r.loc[OOS_START:])["CAGR"]
                                      - metrics(base["EWall"].loc[OOS_START:])["CAGR"])
                    out.append(d)
        return out

    for pn, (px, names) in parents.items():
        spy_cache[pn] = px["SPY"].pct_change().fillna(0.0)
        rows += run_unit(pn, px, sorted(names), "REAL", -1)
        for sd, pick in draws(pn, names):
            rows += run_unit(pn, px, pick, "DRAW", sd)
        P(f"  {pn}: 1 REAL + {N_SEED} independent draws x {len(GROSS)} gross x "
          f"{len(CADENCE)} cadence x 2 arms ({time.time()-t0:.0f}s)")
    grid = pd.DataFrame(rows)

    bases, spys = {}, {}
    P("")
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b = fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:]
        bases[pn] = b
        s = spy_cache[pn].loc[warm:]
        spys[pn] = s
        P(f"  BASE {pn}: RULES v2 {metrics(b)['CAGR']:.2%} / {metrics(b)['Sharpe']:.4f} / "
          f"{metrics(b)['MaxDD']:.2%} (OOS {metrics(b.loc[OOS_START:])['Sharpe']:.4f})   "
          f"SPY {metrics(s)['CAGR']:.2%} / {metrics(s)['Sharpe']:.4f} / "
          f"{metrics(s)['MaxDD']:.2%} (OOS {metrics(s.loc[OOS_START:])['Sharpe']:.4f})")
    P("")

    # ------------------------------------------------------------------ floors (G2)
    def stat_series(sub, stat, period="FULL"):
        pre = {"FULL": "", "IS": "IS_", "OOS": "OOS_"}[period]
        ma = sub[sub.arm == "MA-RS"].set_index("seed")
        if stat == "PREM_SHARPE":
            col = {"FULL": "dSharpe_vs_EWall", "IS": "IS_dSharpe", "OOS": "OOS_dSharpe"}[period]
            return ma[col]
        if stat == "PREM_CAGR":
            col = {"FULL": "dCAGR_vs_EWall", "IS": "IS_dCAGR", "OOS": "OOS_dCAGR"}[period]
            return ma[col]
        return ma[pre + {"SHARPE": "Sharpe", "CAGR": "CAGR", "MAXDD": "MaxDD"}[stat]]

    fl_rows = []
    dr = grid[grid.kind == "DRAW"]
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in PERIODS:
                per_parent = {}
                for pn in pnames:
                    vals = []
                    for g in GROSS:
                        for cad in CADENCE:
                            sub = dr[(dr.parent == pn) & (dr.gross == g) & (dr.cadence == cad)
                                     & (dr.seed < D)]
                            v = stat_series(sub, stat, period).to_numpy(float)
                            if len(v) >= 2:
                                vals.append(np.std(v, ddof=1))
                    per_parent[pn] = float(np.mean(vals)) if vals else np.nan
                row = dict(statistic=stat, D=D, period=period,
                           floor_pooled=float(np.nanmean(list(per_parent.values()))),
                           floor_max=float(np.nanmax(list(per_parent.values()))),
                           floor_min=float(np.nanmin(list(per_parent.values()))))
                row.update({f"floor_{k}": v for k, v in per_parent.items()})
                row["parent_ratio"] = (row["floor_max"] / row["floor_min"]
                                       if row["floor_min"] else np.nan)
                fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)
    fl_old = pd.read_csv(f"{P778}.floors.csv")
    mg = floors.merge(fl_old, on=["statistic", "D", "period"], suffixes=("_r", "_c"))
    assert len(mg) == len(fl_old) == len(floors), (len(mg), len(fl_old), len(floors))
    cols = ["floor_pooled", "floor_max", "floor_min"] + [f"floor_{p}" for p in pnames]
    g2 = max(float(np.abs(mg[c + "_r"] - mg[c + "_c"]).max()) for c in cols)
    P(f"G2 floors    : per-parent floors rebuilt from prices vs idea 774/778's committed "
      f".floors.csv, all {len(mg)} rows, max |d| = {g2:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g2 <= TOL else 'FAIL'}")

    # ------------------------------------------------------------------ mover sets
    def maps(D, period):
        fsub = floors[(floors.D == D) & (floors.period == period)].set_index("statistic")
        return {s: {p: float(fsub.loc[s, f"floor_{p}"]) for p in pnames} for s in STATS}

    cen = cen[cen.mpair.notna()].reset_index(drop=True)
    m0 = cen.margin.to_numpy(float)
    inside = {}                          # (period, D, est, bar) -> bool array
    for period in PERIODS:
        for D in DRAW_COUNTS:
            fpp = maps(D, period)
            b_pool = np.array([bar_pooled(r.family, fpp) for _, r in cen.iterrows()])
            b_rss = np.array([bar_rss_indep(r.parents.split("+"), r.family, fpp, small_name)
                              for _, r in cen.iterrows()])
            b_pair = np.array([bar_pair_indep(r.mpair, r.family, fpp, small_name)
                               for _, r in cen.iterrows()])
            for b in BARS:
                inside[(period, D, "POOLED", b)] = m0 < b * b_pool
                inside[(period, D, "RSS_INDEP", b)] = m0 < b * b_rss
                inside[(period, D, "PAIR_INDEP", b)] = m0 < b * b_pair

    # ------------------------------------------------------------------ G4 headline
    mv778 = pd.read_csv(f"{P778}.moves.csv")
    g4_rows = []
    for D in DRAW_COUNTS:
        pub = PUB778[D]
        row = mv778[(mv778.period == "FULL") & (mv778.D == D) & (mv778.bar == 1.0)
                    & (mv778.subset == "ALL") & (mv778.est == "PAIR_INDEP")]
        committed = int(row.net.iloc[0])
        was = inside[("FULL", D, "POOLED", 1.0)]
        now = inside[("FULL", D, "PAIR_INDEP", 1.0)]
        rebuilt = int((~was & now).sum()) - int((was & ~now).sum())
        g4_rows.append(dict(D=D, published=pub, committed_778=committed, rebuilt_here=rebuilt))
        P(f"                D={D:2d}: 778 published {pub:+3d}, its committed .moves.csv "
          f"{committed:+3d}, rebuilt from prices here {rebuilt:+3d}")
    g4df = pd.DataFrame(g4_rows)
    g4 = bool((g4df.published == g4df.committed_778).all()
              and (g4df.published == g4df.rebuilt_here).all())
    P(f"G4 headline  : idea 778's PAIR_INDEP net-vs-POOLED counts re-derived from its own "
      f"artefacts AND rebuilt from prices -> {'PASS' if g4 else 'FAIL'} (exact integers)")

    # ------------------------------------------------------------------ reliance (G5)
    rel = build_reliance(cen, paths)
    assert len(rel) == len(cen)
    degen = [lg for lg in ("VENUE", "CITED", "ECHO")
             if not (0.02 < float(rel[lg].mean()) < 0.98)]
    g5 = bool(len(paths) > 0 and rel[LEGS].notna().all().all() and not degen)
    P(f"G5 reliance  : corpus {len(paths)} committed md files; census spans "
      f"{cen.file.nunique()} distinct source files; base rates over ALL {len(cen)} claims - "
      + ", ".join(f"{lg} {rel[lg].mean():.1%}" for lg in LEGS)
      + f" -> {'PASS' if g5 else 'FAIL'}  (self and same-run citation excluded by "
      "construction; every leg must sit strictly inside 2%-98% or it measures nothing"
      + (f"; DEGENERATE: {degen}" if degen else "") + ")")
    P("                NOTE, reported not hidden: the first version of this run let "
      "LEADERBOARD.md and QUEUE.md count as CITING files.  They name every committed script "
      "by PROTOCOL rule 5, so CITED read 100.0% and ANY read 100.0%, G5 FAILED, and the leg "
      "was rebuilt with the INDEX exclusion above before any answer was read.")
    P("")

    # ------------------------------------------------------------------ THE ANSWER
    P("=" * 100)
    P("THE MOVERS - claims whose VERDICT changes under the MIN-GAP-PAIR restatement")
    P("=" * 100)

    def subset_mask(nm):
        if nm == "ALL":
            return np.ones(len(cen), bool)
        if nm == "2PANEL":
            return (cen.n_panels == 2).to_numpy()
        if nm == "3PANEL":
            return (cen.n_panels == 3).to_numpy()
        if nm == "NESTED_PAIR":
            return (cen.mpair == "B136|U56").to_numpy()
        if nm == "NZ":
            return (cen.margin > 0).to_numpy()
        raise KeyError(nm)

    ver_rows, mover_rows = [], []
    for period in PERIODS:
        for D in DRAW_COUNTS:
            for cs in CLAIM_SETS:
                msk = subset_mask(cs)
                for b in BARS:
                    was = inside[(period, D, "POOLED", b)]
                    now = inside[(period, D, "PAIR_INDEP", b)]
                    moved = (was != now) & msk
                    to_in = (~was & now) & msk
                    to_out = (was & ~now) & msk
                    d = dict(period=period, D=D, claim_set=cs, bar=b, n=int(msk.sum()),
                             moved=int(moved.sum()), to_inside=int(to_in.sum()),
                             to_outside=int(to_out.sum()),
                             net=int(to_in.sum()) - int(to_out.sum()),
                             moved_share=float(moved.sum() / max(msk.sum(), 1)))
                    for lg in LEGS:
                        v = rel[lg].to_numpy(bool)
                        d[f"mv_{lg}"] = int((moved & v).sum())
                        d[f"mv_{lg}_rate"] = (float(v[moved].mean()) if moved.sum() else np.nan)
                        nonmv = msk & ~moved
                        d[f"nm_{lg}_rate"] = (float(v[nonmv].mean()) if nonmv.sum() else np.nan)
                        d[f"lift_{lg}"] = d[f"mv_{lg}_rate"] - d[f"nm_{lg}_rate"]
                    ver_rows.append(d)
                    if period == "FULL" and D == 6 and cs == "ALL":
                        for i in np.flatnonzero(moved):
                            mover_rows.append(dict(
                                bar=b, idx=int(i), file=cen.file.iloc[i],
                                family=cen.family.iloc[i], n_panels=int(cen.n_panels.iloc[i]),
                                mpair=cen.mpair.iloc[i], margin=float(cen.margin.iloc[i]),
                                direction="OUT->IN" if to_in[i] else "IN->OUT",
                                venue=bool(rel.VENUE.iloc[i]), cited=int(rel.cited.iloc[i]),
                                echo=int(rel.echo.iloc[i]), queued=bool(rel.QUEUED.iloc[i]),
                                ANY=bool(rel.ANY.iloc[i]), STRICT=bool(rel.STRICT.iloc[i]),
                                claim=cen.claim.iloc[i]))
    verd = pd.DataFrame(ver_rows)
    movers = pd.DataFrame(mover_rows)

    head = verd[(verd.period == "FULL") & (verd.D == 6)]
    P("HEADLINE GRID (D=6, FULL) - the 10 tuned points, all shown")
    P(fmt(head.set_index(["claim_set", "bar"])[
        ["n", "moved", "to_inside", "to_outside", "net", "moved_share",
         "mv_ANY", "mv_STRICT"]], 4))
    P("")
    P("H_MOVE  : max moved_share over all (claim set, D, bar) at FULL = "
      f"{verd[verd.period=='FULL'].moved_share.max():.2%} -> "
      + ("HOLDS - the mover set is a small slice of the census"
         if verd[verd.period == 'FULL'].moved_share.max() < 0.10
         else "FALSIFIED - more than 10% of the census moves"))
    P("")
    P("RELIANCE OF THE MOVERS vs THE NON-MOVERS (D=6, FULL, every claim set x bar)")
    for lg in LEGS:
        P(f"  leg {lg}:")
        piv = head.pivot_table(index="claim_set", columns="bar",
                               values=[f"mv_{lg}", f"mv_{lg}_rate", f"nm_{lg}_rate",
                                       f"lift_{lg}"])
        P(fmt(piv.reindex(CLAIM_SETS), 4))
    P("")
    h = head[(head.claim_set == "ALL") & (head.bar == 1.0)].iloc[0]
    P(f"H_LEAN  : headline point (ALL, bar 1.0, D=6, FULL): movers {int(h.moved)} of {int(h.n)}, "
      f"ANY-relied {int(h.mv_ANY)} ({h.mv_ANY_rate:.1%}) vs non-mover base rate "
      f"{h.nm_ANY_rate:.1%}, lift {h.lift_ANY:+.1%} -> "
      + ("HOLDS - the movers are enriched in relied-on claims"
         if h.lift_ANY > 0.10 else
         "FALSIFIED - the movers are at or below the base rate, so the restatement "
         "does not preferentially hit load-bearing claims"))
    strict_tot = int(verd.mv_STRICT.sum())
    P(f"H_HEAD  : STRICT movers (control document AND cited-or-echoed) summed over every "
      f"grid point x period x D = {strict_tot} -> "
      + ("HOLDS - at least one moved claim is load-bearing" if strict_tot > 0 else
         "FALSIFIED - no moved claim is both in a control document and cited elsewhere"))
    P("")

    P("=" * 100)
    P("THE MOVED CLAIMS, READ (D=6, FULL, bar 1.0) - what each one actually says")
    P("=" * 100)
    mv1 = movers[movers.bar == 1.0]
    P(f"  {len(mv1)} moved claims, by source file:")
    P(fmt(mv1.groupby("file").size().rename("moved").to_frame().sort_values(
        "moved", ascending=False), 0))
    P("")
    P("  by family x direction:")
    P(fmt(mv1.pivot_table(index="family", columns="direction", values="idx",
                          aggfunc="count").fillna(0), 0))
    P("")
    P("  by reliance leg:  VENUE %d, CITED>=%d %d, ECHO %d, QUEUED %d, ANY %d, STRICT %d"
      % (int(mv1.venue.sum()), CITE_MIN, int((mv1.cited >= CITE_MIN).sum()),
         int((mv1.echo >= 1).sum()), int(mv1.queued.sum()), int(mv1.ANY.sum()),
         int(mv1.STRICT.sum())))
    P("")
    P("  EVERY moved claim (file | family | dir | margin | relied? | text):")
    for _, r in mv1.iterrows():
        tag = ("VENUE," if r.venue else "") + (f"cited{r.cited}," if r.cited else "") \
            + (f"echo{r.echo}," if r.echo else "") + ("queued" if r.queued else "")
        P(f"   - {r.file[:64]:<64s} {r.family:<11s} {r.direction:<8s} m={r.margin:.4f} "
          f"[{tag.strip(',') or 'NONE'}]")
        P(f"       {r.claim[:200]}")
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 100)
    P("KEEP PATHS over the full price grid (PROTOCOL rule 4a and 4b, every book)")
    P("=" * 100)
    kp_rows = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b, s = bases[pn], spys[pn]
        units = ([("REAL", -1, sorted(names))]
                 + [("DRAW", sd, pick) for sd, pick in draws(pn, names)])
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(list(pick) + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    for arm, w in bks.items():
                        r = fast_backtest(sub, w, freq=cad)["returns"].loc[warm:]
                        f4b = fail_4b(r, s)
                        kp_rows.append(dict(parent=pn, kind=kind, seed=sd, arm=arm, gross=g,
                                            cadence=cad, keep4a=keep_4a(r, b), fail4b=f4b,
                                            keep4b=(f4b == "-")))
    kp = pd.DataFrame(kp_rows)
    P(f"over {len(kp)} books: 4a {int(kp.keep4a.sum())}/{len(kp)}, "
      f"4b {int(kp.keep4b.sum())}/{len(kp)}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}/{len(kp)}")
    P("  by kind: " + ", ".join(
        f"{k} 4a {int(v.keep4a.sum())}/{len(v)} 4b {int(v.keep4b.sum())}/{len(v)}"
        for k, v in kp.groupby("kind")))
    real4b = [f"{r.parent}/{r.arm}/g{r.gross}/{r.cadence}"
              for _, r in kp[(kp.kind == "REAL") & kp.keep4b].iterrows()]
    P("  4b REAL books: " + (", ".join(real4b) if real4b else "none"))
    P("  4b binding failure legs: " + ", ".join(
        f"{k} {v}" for k, v in kp.fail4b.value_counts().head(6).items()))
    P("")

    # ------------------------------------------------------------------ RULE 8
    P("=" * 100)
    P("RULE 8 WALK-FORWARD")
    P("=" * 100)
    P("WF-A: the ANSWER out of sample - floors rebuilt on IS only / OOS only, mover set and")
    P("      every reliance count recomputed in each period.")
    wfa = verd[(verd.D == 6) & (verd.bar == 1.0) & (verd.claim_set == "ALL")].set_index("period")
    P(fmt(wfa[["n", "moved", "net", "moved_share", "mv_ANY", "mv_ANY_rate", "nm_ANY_rate",
               "lift_ANY", "mv_STRICT"]].loc[list(PERIODS)], 4))
    setF = set(np.flatnonzero((inside[("FULL", 6, "POOLED", 1.0)]
                               != inside[("FULL", 6, "PAIR_INDEP", 1.0)])))
    setI = set(np.flatnonzero((inside[("IS", 6, "POOLED", 1.0)]
                               != inside[("IS", 6, "PAIR_INDEP", 1.0)])))
    setO = set(np.flatnonzero((inside[("OOS", 6, "POOLED", 1.0)]
                               != inside[("OOS", 6, "PAIR_INDEP", 1.0)])))
    jac = len(setI & setO) / max(len(setI | setO), 1)
    P(f"  mover sets at D=6, bar 1.0: FULL {len(setF)}, IS {len(setI)}, OOS {len(setO)}; "
      f"IS n OOS {len(setI & setO)}, Jaccard {jac:.4f}")
    P(f"  IS-only movers {len(setI - setO)}, OOS-only movers {len(setO - setI)} -> "
      + ("the moved set IS the same object out of sample" if jac >= 0.5 else
         "the moved set is NOT the same object out of sample"))
    P("  net vs POOLED by period x D (bar 1.0, ALL):")
    P(fmt(verd[(verd.bar == 1.0) & (verd.claim_set == "ALL")].pivot_table(
        index="period", columns="D", values="net").loc[list(PERIODS)], 1))
    P("")

    P("WF-B: the restatement as a DECISION RULE, priced - act on the IS-best parent only if")
    P("      the IS span clears bar x the MIN-GAP PAIR floor AND the backing claim set")
    P("      survives the reliance filter, else stand down to the live book.")
    real = grid[grid.kind == "REAL"]
    u56 = "U56"
    base56, spy56 = bases[u56], spys[u56]
    oos_series, full_series = {}, {}
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        for g in GROSS:
            bks = make_books(px, set(names), g)
            for cad in CADENCE:
                r = fast_backtest(px, bks["MA-RS"], freq=cad)["returns"].loc[warm:]
                full_series[(pn, g, cad)] = r
                oos_series[(pn, g, cad)] = r.loc[OOS_START:]
    fppIS = maps(6, "IS")

    # reliance filter per min-gap pair: does that pair still have any UNMOVED backing claim?
    wasI = inside[("IS", 6, "POOLED", 1.0)]
    nowI = inside[("IS", 6, "PAIR_INDEP", 1.0)]
    movedI = wasI != nowI
    pair_ok = {}
    for mp in cen.mpair.unique():
        m = (cen.mpair == mp).to_numpy()
        backing = m & ~movedI & rel.ANY.to_numpy(bool)
        pair_ok[mp] = bool(backing.sum() > 0)

    def decide(cs, b):
        picks, segsO, segsF, acted = [], [], [], 0
        for g in GROSS:
            for cad in CADENCE:
                prem = {pn: float(real[(real.parent == pn) & (real.gross == g)
                                       & (real.cadence == cad)
                                       & (real.arm == "MA-RS")].IS_dSharpe.iloc[0])
                        for pn in pnames}
                order = sorted(prem, key=prem.get, reverse=True)
                span = prem[order[0]] - prem[order[-1]]
                a, z = order[0], order[-1]
                mp = "|".join(sorted((("SMALL" if a.startswith("SMALL") else a),
                                      ("SMALL" if z.startswith("SMALL") else z))))
                fl = bar_pair_indep(mp, "PREM_SHARPE", fppIS, small_name)
                clears = span >= b * fl
                # the reliance filter: only claim sets whose backing survives may be acted on
                relied = pair_ok.get(mp, True)
                gate = {"ALL": True, "2PANEL": True, "3PANEL": True,
                        "NESTED_PAIR": (mp == "B136|U56"), "NZ": span > 0}[cs]
                act = bool(clears and relied and gate)
                acted += int(act)
                picks.append(order[0] if act else "STANDDOWN")
                segsO.append(oos_series[(order[0], g, cad)] if act else base56.loc[OOS_START:])
                segsF.append(full_series[(order[0], g, cad)] if act else base56)
        mk = lambda segs: pd.concat([s.reindex(segs[0].index).fillna(0.0) for s in segs],
                                    axis=1).mean(axis=1)
        return acted, picks, mk(segsO), mk(segsF)

    wf_rows, dk = [], []
    for cs in CLAIM_SETS:
        for b in BARS:
            acted, picks, bo, bf = decide(cs, b)
            mo = metrics(bo)
            wf_rows.append(dict(claim_set=cs, bar=b, acted=acted, cells=len(picks),
                                picks="/".join(picks), OOS_CAGR=mo["CAGR"],
                                OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
            sp = spy56.reindex(bf.index).fillna(0.0)
            f4 = fail_4b(bf, sp)
            dk.append(dict(claim_set=cs, bar=b, CAGR=metrics(bf)["CAGR"],
                           Sharpe=metrics(bf)["Sharpe"], MaxDD=metrics(bf)["MaxDD"],
                           keep4a=keep_4a(bf, base56.reindex(bf.index).fillna(0.0)),
                           fail4b=f4, keep4b=(f4 == "-")))
    segs = [oos_series[(max(pnames, key=lambda pn: float(real[(real.parent == pn)
            & (real.gross == g) & (real.cadence == cad) & (real.arm == "MA-RS")]
            .IS_dSharpe.iloc[0])), g, cad)] for g in GROSS for cad in CADENCE]
    ungated = pd.concat([s.reindex(segs[0].index).fillna(0.0) for s in segs], axis=1).mean(axis=1)
    ctrl = []
    for nm, r in (("ALWAYS-ACT (778's control)", ungated),
                  ("RULES v2 U56 (live book)", base56.loc[OOS_START:]),
                  ("SPY", spy56.loc[OOS_START:])):
        m = metrics(r)
        ctrl.append(dict(claim_set=nm, bar=np.nan, acted=np.nan, cells=np.nan, picks="-",
                         OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    wf = pd.DataFrame(wf_rows + ctrl)
    P(fmt(wf.set_index(["claim_set", "bar"])[["acted", "cells", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD"]], 4))
    bsh = metrics(base56.loc[OOS_START:])["Sharpe"]
    ssh = metrics(spy56.loc[OOS_START:])["Sharpe"]
    bcg = metrics(base56.loc[OOS_START:])["CAGR"]
    scg = metrics(spy56.loc[OOS_START:])["CAGR"]
    beat_b = int((wf.iloc[:len(wf_rows)].OOS_Sharpe > bsh).sum())
    beat_s = int((wf.iloc[:len(wf_rows)].OOS_Sharpe > ssh).sum())
    P(f"  decision books beating RULES v2 U56 OOS Sharpe ({bsh:.4f}, CAGR {bcg:.2%}): "
      f"{beat_b}/{len(wf_rows)}; beating SPY ({ssh:.4f}, CAGR {scg:.2%}): "
      f"{beat_s}/{len(wf_rows)}")
    dkf = pd.DataFrame(dk)
    P("")
    P("  KEEP paths for the decision books (full-sample twin of each rule, 4a vs RULES v2 U56):")
    P(fmt(dkf.set_index(["claim_set", "bar"]), 4))
    P(f"  decision books: 4a {int(dkf.keep4a.sum())}/{len(dkf)}, "
      f"4b {int(dkf.keep4b.sum())}/{len(dkf)}, "
      f"BOTH {int((dkf.keep4a & dkf.keep4b).sum())}/{len(dkf)}")
    P("")

    # ------------------------------------------------------------------ write
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    floors.to_csv(OUT / f"{STAMP}.floors.csv", index=False)
    cen.join(rel[["venue", "cited", "echo", "queued"] + LEGS]).to_csv(
        OUT / f"{STAMP}.census.csv", index=False)
    rel.to_csv(OUT / f"{STAMP}.reliance.csv", index=False)
    movers.to_csv(OUT / f"{STAMP}.movers.csv", index=False)
    verd.to_csv(OUT / f"{STAMP}.verdicts.csv", index=False)
    g4df.to_csv(OUT / f"{STAMP}.g4.csv", index=False)
    pd.concat([wf.assign(leg="WF-B_OOS"), dkf.assign(leg="WF-B_KEEP")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P(f"wrote grid {len(grid)}, floors {len(floors)}, census {len(cen)}, "
      f"reliance {len(rel)}, movers {len(movers)}, verdicts {len(verd)}, "
      f"keeppaths {len(kp)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
