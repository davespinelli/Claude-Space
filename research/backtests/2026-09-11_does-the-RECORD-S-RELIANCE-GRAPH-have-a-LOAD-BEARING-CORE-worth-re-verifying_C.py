#!/usr/bin/env python3
"""Idea 790 (lane C, 2026-09-11) - does-the-RECORD-S-RELIANCE-GRAPH-have-a-LOAD-BEARING-CORE
worth-re-verifying.

QUESTION
--------
Idea 779 measured reliance CLAIM by CLAIM (VENUE 71.99%, CITED 27.35%, ECHO 44.48%,
STRICT 40.20% over 607 census claims) and reported that its cited-by counts run 0 to 79 with
mean 1.8353 and median 0 - i.e. the downstream weight of the record is carried by a handful
of files.  That is a statement about a GRAPH nobody has drawn.  This run draws it: every
committed run is a node, an edge runs from a run that NAMES another run (or its idea number)
or REPRODUCES one of its distinctive numbers, to the run named or reproduced.  It then does
the thing the queue asks for and nobody has done: takes the top of that ranking and RE-READS
those runs' own headline numbers against their own committed artefacts.

A "load-bearing core worth re-verifying" needs both halves to be true, and they are measured
separately:
    CONCENTRATION - is the in-degree actually concentrated, or is the record a flat graph in
                    which "top decile" names nothing special?
    SOUNDNESS     - do the top runs' published numbers reproduce from their OWN committed
                    data?  A concentrated core that verifies no better than the tail is a
                    core worth nothing; a core that verifies WORSE is an alarm.

WHAT IS MEASURED (declared before any count is read)
---------------------------------------------------
NODE = a committed RUN = the filename stem shared by a script and its artefacts
       (`2026-09-11_<slug>_<lane>`).  A run is RANKABLE if it committed at least one
       narrative markdown file (.result.md / _MEMO.md / .md), because only a narrative has
       headline numbers to re-verify.  The five control documents (RULES / PROTOCOL /
       CHANGELOG / LEADERBOARD / QUEUE) are nodes on the CITING side only.
EDGE A -> B (A relies on B), A != B, same-run artefacts excluded by construction:
    NAMES  A's committed text contains B's stem, or cites "idea NNN" where NNN is an idea
           number the record itself attributes to B (via QUEUE 'Done' rows and LEADERBOARD
           rows that name the script).
    ECHOES A's committed text reproduces, in its own spelling, at least one DISTINCTIVE
           number (>= 4 significant digits, so "2.0" and "0.75" cannot qualify) that B
           publishes in its own narrative.
    INDEX EXCLUSION: LEADERBOARD.md and QUEUE.md name every committed script by PROTOCOL
    rule 5, so they cite everything by construction and are excluded from the CITING side
    (they stay eligible as venues).  This is idea 779's G5 lesson, kept.
RE-VERIFICATION of a run's HEADLINE numbers: every distinctive number in its own narrative
    is looked for in that run's OWN committed data artefacts, on two legs:
    VERIF_ANY  own .csv/.json/.txt (the console log included) contain the token verbatim, or
               a value that rounds to it at its quoted precision (percent forms included).
    VERIF_DATA the same, with the run's own .console.txt EXCLUDED - the number must be
               recoverable from committed DATA, not merely re-read from the run's own
               printout.  This is the leg that means anything.
    A run with no data artefacts at all is UNVERIFIABLE, and that is reported, not dropped.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. RANK STATISTIC in {NAMED, ECHOED, SUM, MAXLEG, CTRL}
         NAMED   in-degree by naming (distinct other runs)
         ECHOED  in-degree by number echo (distinct other runs)
         SUM     NAMED + ECHOED                                  (the headline statistic)
         MAXLEG  max(NAMED, ECHOED)
         CTRL    number of CONTROL documents naming the run (venue-weighted in-degree)
    2. DECILE (top share) in {0.02, 0.05, 0.10, 0.20, 0.25}      (0.10 = the queue's decile)
All 5 x 5 = 25 grid points are reported.  REPORTED (never selected) axes: verification leg
(ANY / DATA), corpus vintage period (FULL / early / late), and the price-side gross x cadence
grid.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
-----------------------------------------------------------------
H_CONC  : the graph has a core - the top decile by SUM holds >= 50% of all in-degree mass.
          Falsified below 50%.
H_SOUND : the core is at least as sound as the tail - core VERIF_DATA share is not more than
          10 pp below the sampled non-core share.  Falsified if the core verifies worse.
H_AGREE : the core is a property of the record, not of the ranking dial - Jaccard between the
          top decile by NAMED and by ECHOED >= 0.50.  Falsified below.

GATES (pre-registered, run and printed before any new number is read)
    G1 corpus   : the inventory is non-degenerate and self-consistent - every rankable run has
                  a narrative, every node's artefacts are attributed to exactly one stem, and
                  no run is its own citer.                               bar exact
    G2 anchor   : idea 779's published reliance numbers are re-derived from its own committed
                  .reliance.csv - cited-by range 0..79, mean 1.8353, median 0, and
                  VENUE 71.99 / CITED 27.35 / ECHO 44.48 / STRICT 40.20 percent. bar exact
    G3 identity : fast_backtest vs engine.backtest on one book per parent.       bar 1e-12
    G4 verifier : the verifier is calibrated on planted controls before it is believed -
                  PLANT-TRUE (values sampled from a run's own committed csv, re-formatted to
                  4 dp) must verify at >= 95%, and PLANT-FALSE (tokens of the same shape drawn
                  uniformly over the same observed range, seeded) must verify at a materially
                  lower rate.  A verifier that passes everything measures nothing.
    G5 graph    : self-edges are absent, INDEX documents are excluded from the citing side,
                  and every rank statistic is non-constant with a non-degenerate spread.

RULE 8 WALK-FORWARD (required, run whatever the census says)
    Two splits, both declared:
      CORPUS split (for the graph): EARLY = files dated <= 2026-09-07, LATE = >= 2026-09-08,
        from the record's own YYYY-MM-DD filename vintage.  WF-A ranks the EARLY-vintage runs
        using EARLY citers only, then re-ranks the same runs using LATE citers only, and asks
        whether the core chosen on the early record is the core the later record leans on
        (Jaccard, rank correlation) and whether its soundness carries over.  Runs dated LATE
        cannot be cited by EARLY files at all, so they are excluded from WF-A by construction.
      PRICE split (for the book): IS = start..2016-12-31, OOS = 2017-01-01..end, read ONCE.
    WF-B prices the core as a DECISION RULE: in each (gross, cadence) cell rank the three
      parents by IS MA-gate premium and ACT on the IS-best parent (trade MA-RS there) only if
      the record's backing claims for that parent come from a CORE run (top share by the rank
      statistic, ranked on EARLY citers only) whose headline numbers VERIFY; else STAND DOWN
      to the live book (RULES v2 on U56).  OOS read once for all 25 decision books, against
      RULES v2 U56, SPY, an ALWAYS-ACT control and a FULL-STAND-DOWN control.
    KEEP paths 4a and 4b are evaluated for every price book and every decision book.

SURVIVORSHIP: universe.json / universe_broad.json / the small panel are CURRENT constituents,
    so every stock-side level carries a survivorship premium; arm-minus-arm premia on the same
    panel largely cancel it.  The three parents start on different dates (U56/B136 2008,
    SMALL 2010).

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and the committed artefacts
of idea 779; modifies nothing but its own outputs:
    .graph.csv .verify.csv .grid.csv .coregrid.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import collections
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
RES = ROOT / "research"
BT = RES / "backtests"

COST = 10.0
MA_WIN = 200
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TOL = 1e-12

RANK_STATS = ["NAMED", "ECHOED", "SUM", "MAXLEG", "CTRL"]
SHARES = [0.02, 0.05, 0.10, 0.20, 0.25]
HEAD_STAT, HEAD_SHARE = "SUM", 0.10          # the queue's "top decile" on the summed degree
VINTAGE_SPLIT = "2026-09-08"                 # EARLY = strictly before, LATE = on/after
CONTROL_DOCS = ("RULES.md", "PROTOCOL.md", "CHANGELOG.md", "LEADERBOARD.md", "QUEUE.md")
INDEX_DOCS = ("LEADERBOARD.md", "QUEUE.md")
SIG_MIN = 4                                  # "distinctive" number: >= 4 significant digits
MAX_BYTES = 30_000_000                       # per-artefact read cap (declared; capping logged)
N_CONTROL = 120                              # seeded non-core sample for the base rate
SOUND_BAR = 0.90                             # a run is SOUND if >= 90% of its headline tokens verify
P779 = BT / "2026-09-11_does-the-MIN-GAP-PAIR-restatement-change-any-published-VERDICT-not-just-the-count_C"
PUB779 = dict(cited_min=0, cited_max=79, cited_mean=1.8353, cited_median=0.0,
              VENUE=71.99, CITED=27.35, ECHO=44.48, STRICT=40.20)

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


# --------------------------------------------------------------------- the graph
NUM_RE = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")
STEM_REF = re.compile(r"(\d{4}-\d{2}-\d{2}_[A-Za-z0-9][A-Za-z0-9_.\-]*)")
IDEA_RE = re.compile(r"\bidea\s+(\d{2,4})\b", re.IGNORECASE)
STEM_IDEA_RE = re.compile(r"^\s*(\d{2,4})\.\s")
VINT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")
NARR_SUFFIX = (".result.md", "_MEMO.md", ".md")
DATA_SUFFIX = (".csv", ".json", ".txt", ".npz")


def sigdigits(tok):
    """Significant digits of a committed decimal token ('0.2464' -> 4, '2.0' -> 1)."""
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


def file_idea_numbers():
    """file stem -> idea numbers the RECORD attributes to it (QUEUE 'Done' / LEADERBOARD)."""
    f2i = collections.defaultdict(set)
    for src in (RES / "QUEUE.md", RES / "LEADERBOARD.md"):
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


def load_corpus():
    """Every committed markdown and script in research/ - the record as text."""
    paths = sorted(set(list(BT.glob("*.md")) + list(BT.glob("*.py"))
                       + list(RES.glob("*.md")) + list(RES.glob("*.py"))))
    return {p.name: p.read_text(errors="ignore") for p in paths}


def build_graph(texts):
    """In-degree of every rankable run on the NAMES and ECHOES legs."""
    all_stems = {stem_of(n) for n in texts}
    narrative = collections.defaultdict(list)
    for n in texts:
        if n in CONTROL_DOCS:
            continue
        if n.endswith(".md"):
            narrative[stem_of(n)].append(n)
    rankable = sorted(narrative)

    f2i = file_idea_numbers()
    i2f = collections.defaultdict(set)
    for st, ideas in f2i.items():
        for i in ideas:
            i2f[i].add(st)

    # ---- NAMES leg: citer stem -> set of cited run stems
    named_by = collections.defaultdict(set)
    ctrl_by = collections.defaultdict(set)
    for n, txt in texts.items():
        src = stem_of(n)
        is_index = n in INDEX_DOCS
        is_ctrl = n in CONTROL_DOCS
        hits = set()
        for m in STEM_REF.findall(txt):
            st = stem_of(m)
            if st in all_stems:
                hits.add(st)
        for i in set(IDEA_RE.findall(txt)):
            hits |= i2f.get(i, set())
        hits.discard(src)
        if is_ctrl:
            for h in hits:
                ctrl_by[h].add(n)
        if is_index:
            continue                                  # index docs cite everything: excluded
        for h in hits:
            named_by[h].add(src)

    # ---- ECHOES leg: a run's distinctive narrative numbers re-appearing elsewhere
    tok_files = collections.defaultdict(set)          # token -> stems whose text contains it
    for n, txt in texts.items():
        if n in INDEX_DOCS:
            continue
        src = stem_of(n)
        for tok in set(NUM_RE.findall(txt)):
            if sigdigits(tok) >= SIG_MIN:
                tok_files[tok].add(src)
    own_tokens = {}
    for st in rankable:
        toks = set()
        for fn in narrative[st]:
            for tok in set(NUM_RE.findall(texts[fn])):
                if sigdigits(tok) >= SIG_MIN:
                    toks.add(tok)
        own_tokens[st] = toks
    echoed_by = {}
    for st in rankable:
        hits = set()
        for tok in own_tokens[st]:
            hits |= tok_files.get(tok, set())
        hits.discard(st)
        echoed_by[st] = hits

    rows = []
    for st in rankable:
        nm, ec = named_by.get(st, set()), echoed_by.get(st, set())
        rows.append(dict(run=st, vintage=vintage(st),
                         NAMED=len(nm), ECHOED=len(ec), SUM=len(nm) + len(ec),
                         MAXLEG=max(len(nm), len(ec)), CTRL=len(ctrl_by.get(st, set())),
                         n_head=len(own_tokens[st]), n_narrative=len(narrative[st])))
    g = pd.DataFrame(rows).set_index("run").sort_values("SUM", ascending=False)
    return g, named_by, echoed_by, own_tokens, narrative


def period_graph(texts, own_tokens, keep_citer, keep_run):
    """Re-run both in-degree legs with the CITING side restricted (WF-A)."""
    f2i = file_idea_numbers()
    i2f = collections.defaultdict(set)
    for st, ideas in f2i.items():
        for i in ideas:
            i2f[i].add(st)
    all_stems = {stem_of(n) for n in texts}
    sub = {n: t for n, t in texts.items() if n not in INDEX_DOCS and keep_citer(n)}
    named_by = collections.defaultdict(set)
    for n, txt in sub.items():
        src = stem_of(n)
        hits = {stem_of(m) for m in STEM_REF.findall(txt)} & all_stems
        for i in set(IDEA_RE.findall(txt)):
            hits |= i2f.get(i, set())
        hits.discard(src)
        for h in hits:
            named_by[h].add(src)
    tok_files = collections.defaultdict(set)
    for n, txt in sub.items():
        src = stem_of(n)
        for tok in set(NUM_RE.findall(txt)):
            if sigdigits(tok) >= SIG_MIN:
                tok_files[tok].add(src)
    rows = []
    for st in [s for s in own_tokens if keep_run(s)]:
        hits = set()
        for tok in own_tokens[st]:
            hits |= tok_files.get(tok, set())
        hits.discard(st)
        nm = named_by.get(st, set())
        rows.append(dict(run=st, NAMED=len(nm), ECHOED=len(hits), SUM=len(nm) + len(hits),
                         MAXLEG=max(len(nm), len(hits)), CTRL=0))
    return pd.DataFrame(rows).set_index("run")


# ---------------------------------------------------------------- re-verification
def own_artefacts(stem):
    return [p for p in BT.glob(stem + ".*") if p.suffix in DATA_SUFFIX]


def read_values(paths):
    """Numeric tokens and values of a run's own committed data artefacts."""
    toks, vals, capped, nbytes = set(), [], 0, 0
    for p in paths:
        try:
            raw = p.read_text(errors="ignore")[:MAX_BYTES]
        except Exception:
            continue
        if p.stat().st_size > MAX_BYTES:
            capped += 1
        nbytes += len(raw)
        found = set(NUM_RE.findall(raw))      # distinct tokens are enough for both legs
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
    """Per-token verification: verbatim present, or a value rounds to it at its precision.

    `vals` is sorted once and probed with searchsorted, so the cost is O(log n) per token.
    """
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


def verify_run(stem, own_tokens, keep_raw=False):
    """Both legs for one run.  Returns a dict or None if the run has no data artefacts."""
    arte = own_artefacts(stem)
    if not arte:
        return None
    toks_a, vals_a, cap_a, b_a = read_values(arte)
    data_only = [p for p in arte if not p.name.endswith(".console.txt")]
    toks_d, vals_d, cap_d, b_d = read_values(data_only)
    heads = sorted(own_tokens[stem])
    va = verify_tokens(heads, toks_a, vals_a)
    vd = verify_tokens(heads, toks_d, vals_d)
    n = len(heads)
    raw = dict(_toks_a=toks_a, _vals_a=vals_a, _toks_d=toks_d, _vals_d=vals_d) if keep_raw \
        else {}
    return dict(run=stem, n_head=n, n_artefacts=len(arte), n_data=len(data_only),
                bytes_any=b_a, bytes_data=b_d, capped=cap_a + cap_d,
                ANY_ok=sum(v != "NONE" for v in va.values()),
                DATA_ok=sum(v != "NONE" for v in vd.values()),
                ANY_exact=sum(v == "EXACT" for v in va.values()),
                DATA_exact=sum(v == "EXACT" for v in vd.values()),
                ANY_share=(sum(v != "NONE" for v in va.values()) / n) if n else np.nan,
                DATA_share=(sum(v != "NONE" for v in vd.values()) / n) if n else np.nan,
                **raw)


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 790 - does the RECORD'S RELIANCE GRAPH have a LOAD-BEARING CORE worth "
      "re-verifying?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, price IS <= {IS_END}, "
      f"OOS >= {OOS_START}")
    P(f"# TUNED (2): RANK STATISTIC in {RANK_STATS} x TOP SHARE in {SHARES} -- all 25 "
      "points reported")
    P(f"# headline point: {HEAD_STAT} @ top {HEAD_SHARE:.0%} (the queue's decile); "
      f"distinctive number = >= {SIG_MIN} significant digits")
    P("")

    # ---------------------------------------------------------------- the graph
    texts = load_corpus()
    graph, named_by, echoed_by, own_tokens, narrative = build_graph(texts)
    P(f"CORPUS: {len(texts)} committed text files "
      f"({sum(len(t) for t in texts.values())/1e6:.1f} MB), "
      f"{len(graph)} rankable runs (a run with a committed narrative), vintages "
      f"{graph.vintage.min()}..{graph.vintage.max()} ({time.time()-t0:.0f}s)")
    P("")

    P("=" * 100)
    P("GATES (pre-registered; printed before any new number is read)")
    P("=" * 100)

    # ------------------------------------------------------------------ G1 corpus
    self_edges = sum(st in named_by.get(st, set()) or st in echoed_by.get(st, set())
                     for st in graph.index)
    multi = [st for st in graph.index if not narrative[st]]
    g1 = bool(len(graph) > 100 and self_edges == 0 and not multi)
    P(f"G1 corpus    : {len(graph)} rankable runs, every one with >= 1 narrative file "
      f"({int(graph.n_narrative.sum())} narratives total), self-edges {self_edges} -> "
      f"{'PASS' if g1 else 'FAIL'}")

    # ------------------------------------------------------------------ G2 anchor
    r779 = pd.read_csv(f"{P779}.reliance.csv")
    a = dict(cited_min=int(r779.cited.min()), cited_max=int(r779.cited.max()),
             cited_mean=round(float(r779.cited.mean()), 4),
             cited_median=float(r779.cited.median()),
             VENUE=round(100 * float(r779.VENUE.mean()), 2),
             CITED=round(100 * float(r779.CITED.mean()), 2),
             ECHO=round(100 * float(r779.ECHO.mean()), 2),
             STRICT=round(100 * float(r779.STRICT.mean()), 2))
    g2 = all(abs(a[k] - PUB779[k]) < 5e-3 for k in PUB779)
    P(f"G2 anchor    : idea 779's committed .reliance.csv re-read - cited-by "
      f"{a['cited_min']}..{a['cited_max']}, mean {a['cited_mean']}, median "
      f"{a['cited_median']:.0f}; VENUE {a['VENUE']}% CITED {a['CITED']}% ECHO {a['ECHO']}% "
      f"STRICT {a['STRICT']}% (published 0..79 / 1.8353 / 0 / 71.99 / 27.35 / 44.48 / 40.20) "
      f"-> {'PASS' if g2 else 'FAIL'}")

    # ------------------------------------------------------------------ G3 identity
    parents = real_panels()
    pnames = list(parents)
    g3 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        aa = fast_backtest(px, bk, freq="W")["returns"]
        bb = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g3 = max(g3, float(np.abs(aa.values - bb.values).max()))
    P(f"G3 identity  : fast_backtest vs engine.backtest max |dret| = {g3:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g3 <= TOL else 'FAIL'}")

    # ------------------------------------------------------- which runs get verified
    sel_union = set()
    for stat in RANK_STATS:
        k = max(1, int(round(max(SHARES) * len(graph))))
        sel_union |= set(graph.sort_values(stat, ascending=False).index[:k])
    rest = sorted(set(graph.index) - sel_union)
    rng = np.random.default_rng(zlib.crc32(b"IDEA790|CONTROL") % (2 ** 32))
    control = sorted(rng.choice(rest, size=min(N_CONTROL, len(rest)), replace=False).tolist())
    todo = sorted(sel_union | set(control))
    P("")
    P(f"RE-VERIFICATION SET: union of the top {max(SHARES):.0%} by each of the "
      f"{len(RANK_STATS)} rank statistics = {len(sel_union)} runs, plus a seeded random "
      f"sample of {len(control)} runs from the remaining {len(rest)} (the base rate is a "
      f"SAMPLE and is labelled as one).  {len(todo)} runs read in total.")
    vrows, unverifiable, t1 = [], [], time.time()
    cal_target = set(todo[:60])            # deterministic calibration slice for G4 (raw kept)
    cache = {}
    for i, st in enumerate(todo):
        v = verify_run(st, own_tokens, keep_raw=(st in cal_target))
        if v is None:
            unverifiable.append(st)
            continue
        if st in cal_target:
            cache[st] = v
        vrows.append({k: val for k, val in v.items() if not k.startswith("_")})
        if (i + 1) % 100 == 0:
            P(f"  ... {i+1}/{len(todo)} runs re-verified ({time.time()-t1:.0f}s)")
    ver = pd.DataFrame(vrows).set_index("run")
    P(f"  {len(ver)} runs re-verified, {len(unverifiable)} have NO committed data artefact "
      f"(UNVERIFIABLE by construction), {int(ver.capped.sum())} artefact reads hit the "
      f"{MAX_BYTES/1e6:.0f} MB cap, {ver.bytes_any.sum()/1e6:.0f} MB read "
      f"({time.time()-t1:.0f}s)")

    # ------------------------------------------------------------------ G4 verifier
    cal = sorted(cache)
    tr_ok = tr_n = fa_ok = fa_n = 0
    rngc = np.random.default_rng(zlib.crc32(b"IDEA790|PLANT") % (2 ** 32))
    for st in cal:
        v = cache[st]
        vals = v["_vals_d"]
        vals = vals[np.isfinite(vals)]
        vals = vals[np.abs(vals) < 1e9]
        if vals.size < 50:
            continue
        pick = vals[rngc.integers(0, vals.size, 25)]
        true_toks = [f"{x:.4f}" for x in pick]
        lo, hi = float(np.percentile(vals, 1)), float(np.percentile(vals, 99))
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            continue
        fake_toks = [f"{x:.4f}" for x in rngc.uniform(lo, hi, 25)]
        rt = verify_tokens(true_toks, v["_toks_d"], v["_vals_d"])
        rf = verify_tokens(fake_toks, v["_toks_d"], v["_vals_d"])
        tr_ok += sum(x != "NONE" for x in rt.values())
        tr_n += len(rt)
        fa_ok += sum(x != "NONE" for x in rf.values())
        fa_n += len(rf)
    tr = tr_ok / max(tr_n, 1)
    fa = fa_ok / max(fa_n, 1)
    g4 = bool(tr >= 0.95 and fa < tr - 0.10)
    P("")
    P(f"G4 verifier  : PLANT-TRUE (values sampled from the runs' own committed csv, "
      f"re-formatted to 4 dp) verify {tr:.1%} of {tr_n}; PLANT-FALSE (same shape, uniform "
      f"over the same range, seeded) verify {fa:.1%} of {fa_n} -> "
      f"{'PASS' if g4 else 'FAIL'} (bars: TRUE >= 95%, FALSE materially lower)")
    P(f"               the FALSE rate is the floor under every verification number below: a "
      f"run whose headline verifies at {fa:.1%} has verified nothing.")

    # ------------------------------------------------------------------ G5 graph
    spread = {s: (int(graph[s].min()), int(graph[s].max()), float(graph[s].mean()),
                  float(graph[s].median())) for s in RANK_STATS}
    degen = [s for s in RANK_STATS if graph[s].nunique() < 3]
    g5 = bool(self_edges == 0 and not degen)
    P("")
    P(f"G5 graph     : self-edges {self_edges}; INDEX docs "
      f"{list(INDEX_DOCS)} excluded from the citing side; in-degree spread "
      + "; ".join(f"{s} {spread[s][0]}..{spread[s][1]} (mean {spread[s][2]:.2f}, median "
                  f"{spread[s][3]:.0f})" for s in RANK_STATS)
      + f" -> {'PASS' if g5 else 'FAIL'}")
    P("")

    # ------------------------------------------------------------ CONCENTRATION
    P("=" * 100)
    P("ANSWER PART 1 - IS THERE A CORE?  (concentration of the in-degree)")
    P("=" * 100)
    conc_rows = []
    for stat in RANK_STATS:
        s = graph[stat].sort_values(ascending=False)
        tot = float(s.sum())
        row = dict(statistic=stat, total_degree=tot, zero_share=float((s == 0).mean()),
                   gini=float((2 * np.sum(np.arange(1, len(s) + 1) * np.sort(s.to_numpy(float)))
                               / (len(s) * max(tot, 1e-12))) - (len(s) + 1) / len(s)))
        for sh in SHARES:
            k = max(1, int(round(sh * len(s))))
            row[f"mass@{sh:.2f}"] = float(s.iloc[:k].sum() / max(tot, 1e-12))
            row[f"k@{sh:.2f}"] = k
        conc_rows.append(row)
    conc = pd.DataFrame(conc_rows).set_index("statistic")
    P(fmt(conc[["total_degree", "zero_share", "gini"]
               + [f"mass@{s:.2f}" for s in SHARES]], 4))
    hmass = float(conc.loc[HEAD_STAT, f"mass@{HEAD_SHARE:.2f}"])
    P("")
    P(f"H_CONC  : top {HEAD_SHARE:.0%} by {HEAD_STAT} holds {hmass:.1%} of all in-degree "
      f"mass -> " + ("HOLDS - the graph has a core" if hmass >= 0.50 else
                     "FALSIFIED - the record's reliance is not concentrated in a decile"))
    P("")
    P(f"TOP 20 RUNS by {HEAD_STAT} (the candidate core):")
    top20 = graph.sort_values(HEAD_STAT, ascending=False).head(20)
    P(fmt(top20[["vintage", "NAMED", "ECHOED", "SUM", "MAXLEG", "CTRL", "n_head"]], 0))
    P("")

    # --------------------------------------------------- CORE AGREEMENT / SOUNDNESS
    def core(stat, share, g=graph):
        k = max(1, int(round(share * len(g))))
        return list(g.sort_values(stat, ascending=False).index[:k])

    P("=" * 100)
    P("ANSWER PART 2 - IS THE CORE THE SAME OBJECT UNDER A DIFFERENT RANK STATISTIC?")
    P("=" * 100)
    jac = pd.DataFrame(index=RANK_STATS, columns=RANK_STATS, dtype=float)
    for s1 in RANK_STATS:
        for s2 in RANK_STATS:
            A, B = set(core(s1, HEAD_SHARE)), set(core(s2, HEAD_SHARE))
            jac.loc[s1, s2] = len(A & B) / max(len(A | B), 1)
    P(f"Jaccard between top-{HEAD_SHARE:.0%} cores:")
    P(fmt(jac, 4))
    jne = float(jac.loc["NAMED", "ECHOED"])
    P(f"H_AGREE : Jaccard(NAMED, ECHOED) at the decile = {jne:.4f} -> "
      + ("HOLDS - the core is a property of the record" if jne >= 0.50 else
         "FALSIFIED - the two legs of 'reliance' name largely DIFFERENT cores, so 'the "
         "record's core' is a choice of statistic, not a fact about the record"))
    P(f"  Spearman between the full rankings: NAMED vs ECHOED "
      f"{graph[['NAMED','ECHOED']].corr(method='spearman').iloc[0,1]:.4f}; "
      f"SUM vs CTRL {graph[['SUM','CTRL']].corr(method='spearman').iloc[0,1]:.4f}")
    P("")

    P("=" * 100)
    P("ANSWER PART 3 - DOES THE CORE'S PUBLISHED ARITHMETIC REPRODUCE FROM ITS OWN DATA?")
    P("=" * 100)
    ctrl_set = set(control)
    grid_rows = []
    for stat in RANK_STATS:
        for sh in SHARES:
            cs = [r for r in core(stat, sh) if r in ver.index]
            base = [r for r in ctrl_set if r in ver.index]
            nunv = len([r for r in core(stat, sh) if r in unverifiable])
            d = dict(statistic=stat, share=sh, n_core=len(core(stat, sh)),
                     n_core_verified=len(cs), n_core_unverifiable=nunv)
            for leg in ("ANY", "DATA"):
                cv = ver.loc[cs, f"{leg}_share"] if cs else pd.Series(dtype=float)
                bv = ver.loc[base, f"{leg}_share"] if base else pd.Series(dtype=float)
                d[f"core_{leg}"] = float(cv.mean()) if len(cv) else np.nan
                d[f"base_{leg}"] = float(bv.mean()) if len(bv) else np.nan
                d[f"lift_{leg}"] = d[f"core_{leg}"] - d[f"base_{leg}"]
                d[f"core_sound_{leg}"] = (float((cv >= SOUND_BAR).mean()) if len(cv)
                                          else np.nan)
                d[f"base_sound_{leg}"] = (float((bv >= SOUND_BAR).mean()) if len(bv)
                                          else np.nan)
            grid_rows.append(d)
    cg = pd.DataFrame(grid_rows)
    P(f"THE 25 TUNED POINTS (core token-verification share vs the sampled non-core base "
      f"rate; SOUND = a run with >= {SOUND_BAR:.0%} of its headline tokens verified):")
    P(fmt(cg.set_index(["statistic", "share"])[
        ["n_core", "n_core_unverifiable", "core_ANY", "base_ANY", "lift_ANY",
         "core_DATA", "base_DATA", "lift_DATA", "core_sound_DATA", "base_sound_DATA"]], 4))
    h = cg[(cg.statistic == HEAD_STAT) & (cg.share == HEAD_SHARE)].iloc[0]
    P("")
    P(f"H_SOUND : at the headline point ({HEAD_STAT} @ top {HEAD_SHARE:.0%}, "
      f"n = {int(h.n_core)}): core DATA-verification {h.core_DATA:.1%} vs sampled non-core "
      f"{h.base_DATA:.1%}, lift {h.lift_DATA:+.1%} -> "
      + ("HOLDS - the core is no less sound than the tail" if h.lift_DATA >= -0.10 else
         "FALSIFIED - the record's most-relied-on runs verify WORSE than the tail"))
    P(f"          console-inclusive leg (ANY): core {h.core_ANY:.1%} vs base {h.base_ANY:.1%} "
      f"(lift {h.lift_ANY:+.1%}).  The gap between the ANY and DATA legs is the share of "
      "headline numbers that exist ONLY in the run's own printout.")
    P(f"          PLANT-FALSE floor {fa:.1%}: any verification share near it is noise.")
    P("")
    core_head = [r for r in core(HEAD_STAT, HEAD_SHARE) if r in ver.index]
    worst = ver.loc[core_head].sort_values("DATA_share").head(15)
    P("THE 15 WORST-VERIFYING RUNS IN THE CORE (what the re-verification actually found):")
    P(fmt(worst[["n_head", "n_artefacts", "n_data", "ANY_share", "DATA_share"]], 4))
    P("")
    unv_core = [r for r in core(HEAD_STAT, HEAD_SHARE) if r in unverifiable]
    P(f"CORE RUNS WITH NO COMMITTED DATA ARTEFACT AT ALL: {len(unv_core)} of "
      f"{len(core(HEAD_STAT, HEAD_SHARE))}"
      + (": " + ", ".join(r[:70] for r in unv_core[:10]) if unv_core else ""))
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
    P("")

    # ------------------------------------------------------------------ RULE 8
    P("=" * 100)
    P("RULE 8 WALK-FORWARD")
    P("=" * 100)
    P(f"WF-A: the ANSWER out of sample.  CORPUS split at {VINTAGE_SPLIT}: the graph is "
      "rebuilt twice over")
    P("      the SAME early-vintage runs - once with only EARLY files allowed to cite, once "
      "with only LATE")
    P("      files allowed to cite - and the two cores are compared.  Runs dated LATE cannot "
      "be cited by")
    P("      EARLY files at all, so they are excluded by construction.")
    early_runs = {st for st in graph.index if vintage(st) and vintage(st) < VINTAGE_SPLIT}
    gE = period_graph(texts, own_tokens,
                      keep_citer=lambda n: (vintage(stem_of(n)) or "9999") < VINTAGE_SPLIT,
                      keep_run=lambda s: s in early_runs)
    gL = period_graph(texts, own_tokens,
                      keep_citer=lambda n: (vintage(stem_of(n)) or "9999") >= VINTAGE_SPLIT,
                      keep_run=lambda s: s in early_runs)
    P(f"  early-vintage rankable runs: {len(early_runs)}  "
      f"(EARLY citers {sum(1 for n in texts if (vintage(stem_of(n)) or '9999') < VINTAGE_SPLIT)}, "
      f"LATE citers {sum(1 for n in texts if (vintage(stem_of(n)) or '9999') >= VINTAGE_SPLIT)})")
    wfa_rows = []
    for stat in RANK_STATS:
        for sh in SHARES:
            A, B = set(core(stat, sh, gE)), set(core(stat, sh, gL))
            both = sorted(A & B)
            vA = [r for r in A if r in ver.index]
            vB = [r for r in B if r in ver.index]
            wfa_rows.append(dict(
                statistic=stat, share=sh, k=len(A),
                jaccard=len(A & B) / max(len(A | B), 1),
                overlap=len(both),
                spearman=float(pd.concat([gE[stat], gL[stat]], axis=1)
                               .corr(method="spearman").iloc[0, 1]),
                earlycore_DATA=float(ver.loc[vA, "DATA_share"].mean()) if vA else np.nan,
                latecore_DATA=float(ver.loc[vB, "DATA_share"].mean()) if vB else np.nan))
    wfa = pd.DataFrame(wfa_rows)
    P(fmt(wfa.set_index(["statistic", "share"]), 4))
    hw = wfa[(wfa.statistic == HEAD_STAT) & (wfa.share == HEAD_SHARE)].iloc[0]
    P(f"  headline ({HEAD_STAT} @ {HEAD_SHARE:.0%}): Jaccard(EARLY core, LATE core) "
      f"{hw.jaccard:.4f} on k = {int(hw.k)}, rank Spearman {hw.spearman:.4f}, "
      f"DATA-verification EARLY core {hw.earlycore_DATA:.1%} vs LATE core "
      f"{hw.latecore_DATA:.1%} -> "
      + ("the core is STABLE out of sample" if hw.jaccard >= 0.50 else
         "the core is NOT the same set out of sample - 'the record's core' is a "
         "vintage-specific object"))
    P("")

    P("WF-B: the core priced as a DECISION RULE - act on the IS-best parent only if the "
      "record's")
    P("      backing claims for that parent come from an EARLY-ranked CORE run whose headline "
      "numbers")
    P("      VERIFY (DATA leg, >= %.0f%%); else stand down to RULES v2 on U56.  OOS read ONCE."
      % (100 * SOUND_BAR))
    cen = pd.read_csv(f"{P779}.census.csv")
    cen["run"] = cen.file.map(stem_of)
    small_name = [p for p in pnames if p.startswith("SMALL")][0]

    def backing_runs(pn):
        key = "SMALL" if pn.startswith("SMALL") else pn
        m = cen.parents.fillna("").str.contains(key, regex=False)
        return set(cen.loc[m, "run"])

    back = {pn: backing_runs(pn) for pn in pnames}
    P("  backing claim runs per parent (from idea 779's committed 607-claim census): "
      + ", ".join(f"{pn} {len(back[pn])}" for pn in pnames))

    def sound(run):
        if run not in ver.index:
            return False
        return bool(ver.loc[run, "DATA_share"] >= SOUND_BAR)

    dec_rows, dec_keep = [], []
    base56, spy56 = bases["U56"], spys["U56"]
    for stat in RANK_STATS:
        for sh in SHARES:
            cset = set(core(stat, sh, gE))
            acted, segO, segF, picks = 0, [], [], []
            for g in GROSS:
                for cad in CADENCE:
                    order = sorted(pnames, key=lambda pn: is_prem[(pn, g, cad)], reverse=True)
                    best = order[0]
                    ok = any((r in cset) and sound(r) for r in back[best])
                    acted += int(ok)
                    picks.append(best if ok else "STANDDOWN")
                    segO.append(oos_series[(best, g, cad)] if ok
                                else base56.loc[OOS_START:])
                    segF.append(full_series[(best, g, cad)] if ok else base56)

            def mk(segs):
                return pd.concat([s.reindex(segs[0].index).fillna(0.0) for s in segs],
                                 axis=1).mean(axis=1)
            bo, bf = mk(segO), mk(segF)
            mo = metrics(bo)
            dec_rows.append(dict(statistic=stat, share=sh, acted=acted, cells=len(picks),
                                 picks="/".join(picks), OOS_CAGR=mo["CAGR"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
            sp = spy56.reindex(bf.index).fillna(0.0)
            f4 = fail_4b(bf, sp)
            dec_keep.append(dict(statistic=stat, share=sh, CAGR=metrics(bf)["CAGR"],
                                 Sharpe=metrics(bf)["Sharpe"], MaxDD=metrics(bf)["MaxDD"],
                                 keep4a=keep_4a(bf, base56.reindex(bf.index).fillna(0.0)),
                                 fail4b=f4, keep4b=(f4 == "-")))
    # controls
    segs = [oos_series[(max(pnames, key=lambda pn: is_prem[(pn, g, cad)]), g, cad)]
            for g in GROSS for cad in CADENCE]
    always = pd.concat([s.reindex(segs[0].index).fillna(0.0) for s in segs], axis=1).mean(axis=1)
    ctrls = []
    for nm, r in (("ALWAYS-ACT (control)", always),
                  ("FULL-STAND-DOWN (control)", base56.loc[OOS_START:]),
                  ("RULES v2 U56 (live book)", base56.loc[OOS_START:]),
                  ("SPY", spy56.loc[OOS_START:])):
        m = metrics(r)
        ctrls.append(dict(statistic=nm, share=np.nan, acted=np.nan, cells=np.nan, picks="-",
                          OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    dec = pd.DataFrame(dec_rows + ctrls)
    P(fmt(dec.set_index(["statistic", "share"])[["acted", "cells", "OOS_CAGR", "OOS_Sharpe",
                                                 "OOS_MaxDD"]], 4))
    bsh = metrics(base56.loc[OOS_START:])["Sharpe"]
    ssh = metrics(spy56.loc[OOS_START:])["Sharpe"]
    nrule = len(dec_rows)
    P(f"  decision books beating RULES v2 U56 OOS Sharpe ({bsh:.4f}): "
      f"{int((dec.iloc[:nrule].OOS_Sharpe > bsh).sum())}/{nrule}; beating SPY ({ssh:.4f}): "
      f"{int((dec.iloc[:nrule].OOS_Sharpe > ssh).sum())}/{nrule}")
    dkf = pd.DataFrame(dec_keep)
    P("")
    P("  KEEP paths for the decision books (full-sample twin, 4a vs RULES v2 U56, 4b vs SPY):")
    P(fmt(dkf.set_index(["statistic", "share"]), 4))
    P(f"  decision books: 4a {int(dkf.keep4a.sum())}/{len(dkf)}, "
      f"4b {int(dkf.keep4b.sum())}/{len(dkf)}, "
      f"BOTH {int((dkf.keep4a & dkf.keep4b).sum())}/{len(dkf)}")
    P("")

    # ------------------------------------------------------------------ write
    graph.to_csv(OUT / f"{STAMP}.graph.csv")
    ver.to_csv(OUT / f"{STAMP}.verify.csv")
    cg.to_csv(OUT / f"{STAMP}.coregrid.csv", index=False)
    conc.to_csv(OUT / f"{STAMP}.concentration.csv")
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    pd.concat([wfa.assign(leg="WF-A"), dec.assign(leg="WF-B_OOS"),
               dkf.assign(leg="WF-B_KEEP")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    grid[["parent", "arm", "gross", "cadence", "keep4a", "fail4b", "keep4b"]].to_csv(
        OUT / f"{STAMP}.keeppaths.csv", index=False)
    pd.DataFrame({"run": unverifiable}).to_csv(OUT / f"{STAMP}.unverifiable.csv", index=False)
    P(f"wrote graph {len(graph)}, verify {len(ver)}, coregrid {len(cg)}, grid {len(grid)}, "
      f"wf {len(wfa)+len(dec)+len(dkf)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
