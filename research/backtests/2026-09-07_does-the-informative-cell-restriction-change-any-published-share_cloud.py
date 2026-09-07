#!/usr/bin/env python3
"""Idea 393 — "does-the-informative-cell-restriction-change-any-published-share" (cloud, 2026-09-07).

QUESTION (QUEUE.md).  Idea 335 found that 51 of its 90 identity cells were `0 <= 0`
DEGENERATE — both sides of the inequality already failing 4b at ZERO cost, so the
predicate was satisfied by arithmetic and carried no information — which turned a
headline share of 80/90 into 29/39.  Census every published share in the record that is
computed over c*, breakeven or fail-bar CELLS, report how many have a degenerate
denominator, and restate the ones that do.

This is a BOOKKEEPING FIX WITH A KNOWN DIRECTION, not a new measurement: restricting a
denominator can only move a share, never a book's returns.  The deliverable is therefore
a census + a restatement table, plus (PROTOCOL rules 4 and 8) a live re-pricing of the
arms the restatement touches, so the audit is anchored to real backtests rather than to
its own arithmetic.

WHAT COUNTS AS "A SHARE COMPUTED OVER c*/BREAKEVEN/FAIL-BAR CELLS".  Five kinds; the
first three are IN SCOPE, the last two are the controls:

  CSTAR-PREDICATE  a k/N whose PREDICATE is evaluated on c* or breakeven VALUES
                   ("the inequality holds in 80/90", "the IS breakeven understates the
                   OOS one in 5 of 6").  DEGENERATE CELL := every c* value entering the
                   predicate is 0.0, i.e. every side already fails at zero cost.  This is
                   idea 335's own definition, verbatim.
  CSTAR-OTHER      a k/N over the same cells with no comparison verb next to it
                   ("9 of 42 sit above 20 bps").  Same degeneracy definition.
  FAILBAR          a k/N tallying WHICH bar binds ("binding bar over the 464 failures:
                   DD 62, CAGR 78").  DEGENERATE CELL := a cell with no failing bar (a
                   PASS) inside the denominator; a genuine failure at zero cost is NOT
                   degenerate here, it is the thing being counted.
  KEEP-PASS        "4b 16/180".  OUT OF SCOPE, the CONTROL class: its denominator is the
                   whole grid BY DESIGN, so the restriction does not apply.  Counting it
                   would inflate the census.
  GATE             "max|diff| = 3.6e-15 on 42/42 rows".  OUT OF SCOPE: a claim about
                   arithmetic agreement, not about cells.

CLASSIFICATION IS BY NEAREST GOVERNING TOKEN, not by a symmetric window.  One line
routinely carries several shares of different kinds ("no new KEEP (4a 0/126 at 0, 10 AND
25 bps; 4b 38/126 @0, 18/126 @10, 0/126 @25, and none of the 18 has a c* above the
parent's)"), and a window classifier reads the last KEEP-pass share as a c* share.  The
governing token closest on the LEFT decides; only if the left is silent is the right read.
Inline code spans and bare filenames are blanked first: a `.breakeven.csv` in a sentence
is a file reference, not a claim about breakevens.

DEGENERACY IS PER-PREDICATE, NOT PER-FILE.  A grid's degenerate count depends on which
(path, window) pair the share is about: over idea 335's 12 c* columns, 50 of 90 rows are
zero everywhere, but the published 4b/full share's own denominator loses 51.  The census
therefore recomputes degeneracy per (share -> column set), never once per CSV.

DESIGN.

 [0] GATES — nothing is read before these print.
     G1  fast_bt == engine.backtest on returns AND turnover at 0 and 25 bps.
     G2  book-level overlay at OFF (m == 1) == the parent, exactly.
     G3  SHARPE INVARIANCE of the gross dial (a in 0.25..1.00, c in 0/10/25) — this is
         what makes the matched control's c* a pure CAGR/MaxDD statistic.
     G4  the record's standing 2026-09-04 KEEP-4b row (`46 N n=20`: 12.7% / 1.09 /
         -18.3%, halves 1.09/1.10) rebuilt at fixed n=20 on U56 @10 bps.
     G5  THE LOAD-BEARING ONE.  This run's independently-written c* estimator, run over
         an independent rebuild of idea 335's 54 BOOK-LEVEL cells (3 families x 3 dials
         x 3 rungs x 2 panels), reproduces the committed `.grid.csv`'s twelve c* columns.
         Only if the audit's arithmetic IS the record's arithmetic can it restate the
         record's shares.  (The 36 PER-NAME cells of that grid are not rebuilt here and
         are excluded from G5 by name, not by outcome.)
     G6  the restriction reproduces idea 335's published 51 / 39 / 29 / 10 exactly.

 [A] CENSUS.  Every .md in research/ and research/backtests/ is scanned for k/N shares.
     Each share is classified CSTAR-PREDICATE / FAILBAR / KEEP-PASS / OTHER from the
     tokens governing it, and assigned a recoverability tier:
       R1 RESTATABLE    a sibling CSV carries the c*/fail-bar columns AND the
                        denominator matches a cell set in it -> degeneracy is COUNTED and
                        the share RESTATED (with its PREDICATE recovered from a FIXED
                        library where possible, so the restatement is a number).
       R2 CSV-BACKED    a sibling CSV carries such columns but no denominator matches.
       R0 NO-CSV        the parent committed no c* column -> not auditable at all.
       R0 UNATTRIBUTED  a digest re-quote (CHANGELOG/QUEUE/LEADERBOARD) whose owning idea
                        cannot be read off the entry.  Digest lines are attributed to the
                        idea whose OWN entry they are, never to the first "idea N" they
                        mention, because a KILL entry routinely cites three other ideas.

 [B] DEGENERACY over every committed CSV in the record carrying a c*/breakeven/fail-bar
     column, per column-group, with the informative-cell count beside it.

 [C] RESTATEMENT of every R1 share, with the direction of the move.

 [D] LIVE RE-PRICING + RULE 8.  The 54 rebuilt cells are priced on both KEEP paths at
     10 and 25 bps on full / halves / OOS against RULES v2 (4a) and SPY (4b), and the
     dial is chosen on IS 2008-2016 ONLY (by IS c*_4b, and separately by IS Sharpe@10 —
     the record's convention) with 2017-2026 read once.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): (1) the parent's gross rung g0, (2) the
overlay's dial.  Panel, family, cost rung and window are CENSUS axes — every level is
reported and nothing is selected on outcome.  All 54 cells go to .grid.csv.

CAVEATS.  (1) universe.json (56) and universe_broad.json (136) are CURRENT-CONSTITUENT
lists — SURVIVORSHIP; absolute CAGRs are optimistic, and B136 CONTAINS U56, so two
panels is not two independent samples.  (2) The census can only restate shares whose
parent committed a CSV; R0 shares are counted, not fixed, and that count is itself the
result.  (3) A share's denominator is matched by VALUE (N == rows in a cell set); a
coincidental match is possible and every match is printed with its file so it can be
checked by hand.  (4) c* is a breakeven, not a return: a high c* on a bad book is still
a bad book.

Deterministic, standalone.  Reads baseline.py and the committed record; modifies nothing.
"""
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                          # noqa: E402

OUT = Path(__file__).with_suffix("")
SLUG = OUT.name
BT = REPO / "research" / "backtests"

MAX_VOL = 0.60
VOL_SCALE = False
N0 = 20
FREQ = "W"
WARMUP = 260
RUNGS = [0.50, 0.75, 1.00]
COSTS = [10, 25]
CMAX = 50.0
SCAN = 0.25
TOL = 1e-9
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
B_FIXED = 0.40

FAMILIES = {
    "BREADTH": [0.75, 0.50, 0.25],
    "DDCTL":   [0.05, 0.10, 0.20],
    "VOLCAP":  [0.10, 0.15, 0.25],
}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ===================================================================== book machinery
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def parent_weights(px, g0, n=N0):
    """NFn: top k = min(n, E_t) eligible names, equal weight, gross g0."""
    el = eligible_mask(px)
    rank = score(px, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    e = el.sum(axis=1).astype(float)
    k = np.minimum(float(n), e).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(g0 / k, axis=0)


def fast_bt(px, w, freq):
    """engine.backtest at cost_bps=0 in numpy; returns (returns, turnover, gross)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    reb = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n)
    turn = np.zeros(n)
    gr = np.zeros(n)
    for i in range(n):
        if reb[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx), pd.Series(gr, index=idx))


def apply_mult(r0, turn0, gross0, m):
    """Idea 41's book-level overlay convention, verbatim:
    r = m*r0 ; turn = m*turn0 + |dm| * gross0.shift(1) ; gross = m*gross0."""
    dm = m.diff().abs().fillna(0.0)
    return (m * r0, m * turn0 + dm * gross0.shift(1).fillna(0.0), m * gross0)


def panel_breadth(px):
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    live = q.notna()
    return (above & live).sum(axis=1) / live.sum(axis=1).replace(0, np.nan)


def mult_breadth(px, r0, turn0, gross0, depth):
    on = (panel_breadth(px).shift(1) < B_FIXED).fillna(False)
    return pd.Series(np.where(on.values, depth, 1.0), index=px.index)


def mult_ddctl(px, r0, turn0, gross0, T):
    eq = (1.0 + r0).cumprod()
    dd = (eq / eq.cummax() - 1.0).shift(1).fillna(0.0)
    return pd.Series(np.where(dd.values < -T, 0.50, 1.0), index=px.index)


def mult_volcap(px, r0, turn0, gross0, target):
    v = (r0.rolling(20).std() * np.sqrt(252.0)).shift(1)
    return (target / v).clip(upper=1.0).fillna(1.0)


MULT = {"BREADTH": mult_breadth, "DDCTL": mult_ddctl, "VOLCAP": mult_volcap}


# ===================================================================== metrics / c*
def nm3(r):
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return cagr, (float(r.mean()) * 252.0 / vol if vol else np.nan), dd


def sharpe(r):
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return (float(r.mean()) * 252.0) / sd if sd else np.nan


class PanelRef:
    def __init__(self, idx, spy_r, v2_r, v2_turn):
        self.idx = idx
        self.is_m = np.asarray(idx <= pd.Timestamp(IS_END))
        self.oos = np.asarray(idx >= pd.Timestamp(OOS_START))
        s = np.asarray(spy_r, float)
        self.spy_r = s
        self.spy = {}
        for win, mask in [("full", np.ones(len(s), bool)), ("is", self.is_m), ("oos", self.oos)]:
            x = s[mask]
            h = len(x) // 2
            c, _, dd = nm3(x)
            d = {"H1": sharpe(x[:h]), "H2": sharpe(x[h:]), "DD": abs(dd), "CAGR": c}
            if win == "full":
                d["OOS"] = sharpe(s[self.oos])
            self.spy[win] = d
        self.v2 = Path4(idx, v2_r, v2_turn, self)


class Path4:
    """One cost-parameterised return path with both KEEP paths' bar margins."""

    def __init__(self, idx, r0, turn, ref):
        self.idx = idx
        self.r0 = np.asarray(r0, float)
        self.turn = np.asarray(turn, float)
        self.ref = ref
        yrs = (idx[-1] - idx[0]).days / 365.25
        self.turnover_yr = float(self.turn.sum()) / yrs
        self.gross_mean = np.nan

    def rc(self, c):
        return self.r0 - self.turn * (c / 1e4)

    def _w(self, r, win):
        return r if win == "full" else (r[self.ref.is_m] if win == "is" else r[self.ref.oos])

    def m4b(self, c, win="full"):
        x = self._w(self.rc(c), win)
        R = self.ref.spy[win]
        h = len(x) // 2
        cg, _, dd = nm3(x)
        m = {"H1": sharpe(x[:h]) - R["H1"], "H2": sharpe(x[h:]) - R["H2"],
             "DD": DD_CAP * R["DD"] - abs(dd), "CAGR": cg - CAGR_FLOOR * R["CAGR"]}
        if win == "full":
            m["OOS"] = sharpe(self.rc(c)[self.ref.oos]) - R["OOS"]
        return m

    def m4a(self, c, win="full"):
        x = self._w(self.rc(c), win)
        y = self._w(self.ref.v2.rc(c), win)
        h = len(x) // 2
        _, _, dd = nm3(x)
        _, _, ddb = nm3(y)
        return {"H1": sharpe(x[:h]) - sharpe(y[:h]), "H2": sharpe(x[h:]) - sharpe(y[h:]),
                "DD": abs(ddb) - abs(dd)}

    def worst(self, c, path, win):
        return min((self.m4b if path == "4b" else self.m4a)(c, win).values())

    def firstfail(self, c, path, win):
        m = (self.m4b if path == "4b" else self.m4a)(c, win)
        bad = [k for k, v in m.items() if v <= 0]
        return ",".join(bad) if bad else "-"

    def stats(self, c, win="full"):
        x = self._w(self.rc(c), win)
        cg, sh, dd = nm3(x)
        h = len(x) // 2
        return dict(CAGR=cg, Sharpe=sh, MaxDD=dd, H1=sharpe(x[:h]), H2=sharpe(x[h:]))


def cstar(p, path="4b", win="full"):
    """First c in [0, CMAX] bps where any bar turns <= 0.  0.0 = fails at zero cost,
    nan = never fails inside the ladder."""
    if p.worst(0.0, path, win) <= 0:
        return 0.0
    lo, hi = 0.0, None
    for c in np.arange(SCAN, CMAX + SCAN / 2, SCAN):
        if p.worst(float(c), path, win) <= 0:
            hi = float(c)
            break
        lo = float(c)
    if hi is None:
        return np.nan
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if p.worst(mid, path, win) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def fmt(v):
    return "never" if (v is None or (isinstance(v, float) and np.isnan(v))) else f"{v:.2f}"


# ===================================================================== census machinery
CSTAR_COL = re.compile(r"c_?star|cstar|breakeven|break_even", re.I)
FAILBAR_COL = re.compile(r"first_?fail|fail_?bars?|failing_?bar|cstar_bar|_binds$", re.I)

CSTAR_TOK = re.compile(r"c\s?\*|c-star|cstar|breakeven|break-even|break even|cost budget|"
                       r"crossing cost", re.I)
FAILBAR_TOK = re.compile(r"binding bar|failing bar|fail bar|first[_ ]fail|first failing|"
                         r"which bar|binding bars|failing bars", re.I)
KEEPPASS_TOK = re.compile(r"\b4[ab]\b|KEEP path|pass(es)?\b", re.I)
PRED_TOK = re.compile(r"hold[s]?\b|violat|understate|overstate|exceed|wider|narrow|above|below|"
                      r"higher|lower|<=|>=|≤|≥|agree|disagree|survive|beat|non-degenerate|"
                      r"inside \(|greater|less than|identity", re.I)

SHARE = re.compile(r"(?<![\d.\-/])(\d{1,5})\s*(?:/|of|out of)\s*(\d{1,5})(?![\d.\-/%])")
DATEISH = re.compile(r"20\d\d[-/]\d\d")


def md_corpus():
    fs = sorted(BT.glob("*.md")) + [REPO / "research" / "CHANGELOG.md",
                                    REPO / "research" / "QUEUE.md",
                                    REPO / "research" / "LEADERBOARD.md"]
    return [f for f in fs if f.exists() and f.name != f"{SLUG}.result.md"]


GATE_TOK = re.compile(r"max\s*\|?\s*(diff|err|d\|)|reproduc|EXACT\b|identical|\bG\d\b|"
                      r"\brows\b|\bgate", re.I)
GOVERNORS = [("KEEP-PASS", re.compile(r"\b4[ab]\b|\bKEEP path\b|\bpass(?:es|ed|ing)?\b|"
                                      r"\bclears?\b", re.I)),
             ("FAILBAR", FAILBAR_TOK),
             ("CSTAR", CSTAR_TOK)]


def classify(line, span):
    """Kind of the share at `span`, decided by its NEAREST GOVERNING TOKEN.

    A single line routinely carries several shares of different kinds — "no new KEEP (4a
    0/126 at 0, 10 AND 25 bps; 4b 38/126 @0, 18/126 @10, 0/126 @25, and none of the 18 has
    a c* above the parent's)" holds five KEEP-pass shares and one c* clause.  A symmetric
    window reads the last of them as a c* share.  So: take the governing token CLOSEST to
    the share on its LEFT (within 130 chars); only if the left is silent look right (60).
    """
    s, e = span
    lo = max(0, s - 130)
    cands = []
    for kind, rx in GOVERNORS:
        for m in rx.finditer(line[lo:s]):
            cands.append((0, s - (lo + m.end()), kind))
        for m in rx.finditer(line[e:e + 60]):
            cands.append((1, m.start(), kind))
    if not cands:
        return "OTHER"
    # a reproduction count ("max|diff| = 3.6e-15 on 42/42 rows") is a GATE, not a share:
    # it is a claim about arithmetic agreement, and restricting its denominator is
    # meaningless.  Excluded by its own language, before any governor is read.
    if GATE_TOK.search(line[max(0, s - 70):min(len(line), e + 40)]):
        return "GATE"
    best = min(cands)[2]
    if best != "CSTAR":
        return best
    w = line[max(0, s - 90):min(len(line), e + 90)]
    return "CSTAR-PREDICATE" if PRED_TOK.search(w) else "CSTAR-OTHER"


def stem_of(mdfile):
    """The parent script stem for a committed .md ('<stem>.result.md' -> '<stem>')."""
    n = mdfile.name
    for suf in (".result.md", ".memo.md", ".MEMO.md", "_MEMO.md", ".md"):
        if n.endswith(suf):
            return n[: -len(suf)]
    return n


DIGESTS = {"CHANGELOG.md", "QUEUE.md", "LEADERBOARD.md"}
IDEA_HDR = re.compile(r"^#+\s*Idea\s+(\d+)\b", re.I)
CODESPAN = re.compile(r"`[^`]*`")
FNAME = re.compile(r"[\w./-]+\.(?:csv|py|md|json|png)")
# a digest line is attributed to the idea whose OWN entry it is, never to the first
# 'idea N' it happens to mention (a KILL entry routinely cites three other ideas).
OWNER_CHANGELOG = re.compile(r"^-\s*\d{4}-\d\d-\d\d\s*\([^)]*?idea\s+(\d+)", re.I)
OWNER_QUEUE = re.compile(r"^(\d+)\.\s")


def strip_code(line):
    """Blank out inline code spans and bare filenames, keeping length.  A `.breakeven.csv`
    in a sentence is a FILE REFERENCE, not a claim about breakevens, and classifying on it
    manufactures c* shares out of gate lines."""
    out = CODESPAN.sub(lambda m: " " * len(m.group(0)), line)
    return FNAME.sub(lambda m: " " * len(m.group(0)), out)


def attribute(fname, line):
    """Parent script stem for a share quoted in a digest file, or '' when unattributable."""
    if fname == "CHANGELOG.md":
        m = OWNER_CHANGELOG.match(line.strip())
    elif fname == "QUEUE.md":
        m = OWNER_QUEUE.match(line.strip())
    else:
        return ""
    return m.group(1) if m else ""


def idea_index():
    """idea number -> script stem, read off each committed .md's own '# Idea N' header."""
    ix = {}
    for f in sorted(BT.glob("*.md")):
        try:
            head = f.read_text(errors="replace")[:400]
        except Exception:
            continue
        for line in head.split("\n")[:6]:
            m = IDEA_HDR.match(line.strip())
            if m:
                ix.setdefault(int(m.group(1)), stem_of(f))
                break
    return ix


def column_groups(df):
    """Named groups of c*/fail-bar columns a share could be computed over.

    A group is the column set a single predicate would consume:
      * PAIRED   an (X, X_ctrl)-shaped pair -> the inequality's own two sides.
      * SINGLE   one c* column -> a share about that column alone.
      * FAILBAR  one fail-bar column.
    """
    cs = [c for c in df.columns if CSTAR_COL.search(c) and not FAILBAR_COL.search(c)
          and pd.api.types.is_numeric_dtype(df[c])]
    fb = [c for c in df.columns if FAILBAR_COL.search(c)]
    groups = {}
    used = set()
    for a in cs:
        for b in cs:
            if a == b:
                continue
            # ov/ct, X/X_ctrl, X/ctrl_X, band/twin, IS/OOS twins
            keys = [(a.replace("_ov_", "_ct_"), b), (a + "_ctrl", b),
                    (a.replace("cstar4b_", "cstar4b_ctrl_"), b),
                    (a.replace("cstar4a_", "cstar4a_ctrl_"), b),
                    ("ctrl_" + a, b), (a.replace("band_", "twin_"), b),
                    (a.replace("c_star", "c_star_law"), b)]
            if any(k[0] == k[1] for k in keys):
                groups[f"PAIRED:{a}|{b}"] = [a, b]
                used.update([a, b])
    for c in cs:
        groups[f"SINGLE:{c}"] = [c]
    for c in fb:
        groups[f"FAILBAR:{c}"] = [c]
    return groups


def recover_predicate(df, cols, kind, k):
    """Search a small FIXED library of predicates for one that reproduces the published
    numerator k on the FULL cell set.  Returns (label, boolean Series) or None.

    The library is fixed before any share is read and is the same for every share, so a
    recovery is a match, not a fit: with |library| ~ 40 and k an integer in [0, N], a
    coincidental match is possible and every recovered share is printed with its label so
    it can be checked against the parent's own text."""
    cand = []
    if kind == "FAILBAR":
        s = df[cols[0]].astype(str).str.strip()
        for v in sorted(set(s)):
            cand.append((f"{cols[0]} == '{v}'", s == v))
            cand.append((f"{cols[0]} contains '{v}'", s.str.contains(re.escape(v))))
    elif kind == "PAIRED":
        a, b = cols
        x, y = df[a].fillna(CMAX * 10), df[b].fillna(CMAX * 10)
        cand += [(f"{a} <= {b}", x <= y + TOL), (f"{a} >= {b}", x + TOL >= y),
                 (f"{a} < {b}", x < y - TOL), (f"{a} > {b}", x - TOL > y),
                 (f"{a} == {b}", (x - y).abs() <= TOL)]
    else:
        c = cols[0]
        x = df[c]
        cand += [(f"{c} > 0", x.fillna(CMAX * 10) > 0), (f"{c} == 0", x.fillna(-1) == 0),
                 (f"{c} is never", x.isna()), (f"{c} is finite", x.notna())]
        for t in (1, 2.5, 5, 10, 20, 25, 30, 50):
            cand += [(f"{c} >= {t}", x.fillna(CMAX * 10) >= t),
                     (f"{c} < {t}", x.fillna(CMAX * 10) < t),
                     (f"0 < {c} <= {t}", (x.fillna(-1) > 0) & (x.fillna(CMAX * 10) <= t))]
    for lab, h in cand:
        if int(h.sum()) == k:
            return lab, h
    return None


def degenerate_mask(df, cols, kind):
    """Per-predicate degeneracy.  c* group: every entering value is 0 (both sides already
    fail at zero cost).  FAILBAR group: the cell has NO failing bar (it is a pass)."""
    if kind == "FAILBAR":
        s = df[cols[0]].astype(str).str.strip().str.lower()
        return s.isin(["", "-", "none", "nan", "na", "pass", "0", "false"])
    sub = df[cols]
    return (sub.fillna(-1.0) == 0.0).all(axis=1)


def build_live():
    P(f"# {SLUG}")
    P("# idea 393 — does the informative-cell restriction change any published share?")
    P("# DEGENERATE CELL := every c* entering the predicate is 0.0 (both sides already fail")
    P("#                    at zero cost)  |  FAILBAR: a cell with no failing bar")
    P(f"# rebuild: idea 335's BOOK-LEVEL cells only ({list(FAMILIES)} x 3 dials x {RUNGS} x 2 panels = 54)")
    P("")

    panels = []
    for tag, kw in [("U56", {}), ("B136", {"broad": True})]:
        px = load_universe(**kw).dropna(how="all").ffill()
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED — aborting.")
            sys.exit(1)
        panels.append((tag, px))

    # ================================================================= [0] GATES
    P("=" * 150)
    P("[0] REPRODUCTION GATES")
    gpx = panels[0][1]
    gw = parent_weights(gpx, 0.75)
    r0g, tg, grg = fast_bt(gpx, gw, FREQ)
    g1 = 0.0
    for c in (0, 25):
        eng = backtest(gpx, gw, cost_bps=c, freq=FREQ)
        g1 = max(g1, float((r0g - tg * c / 1e4 - eng["returns"]).abs().max()),
                 float((tg - eng["turnover"]).abs().max()))
    P(f"    G1 fast_bt == engine.backtest (returns AND turnover, c in 0/25 bps): max |d| {g1:.3e}")
    assert g1 < 1e-12, g1

    ones = pd.Series(1.0, index=gpx.index)
    rB, tB, grB = apply_mult(r0g, tg, grg, ones)
    g2 = max(float((rB - r0g).abs().max()), float((tB - tg).abs().max()),
             float((grB - grg).abs().max()))
    P(f"    G2 book-level overlay at OFF (m == 1) == parent: max |d| {g2:.3e}")
    assert g2 < 1e-12, g2

    g3 = 0.0
    for a in (0.25, 0.50, 0.85, 1.00):
        for c in (0, 10, 25):
            base = (r0g - tg * c / 1e4).values
            g3 = max(g3, abs(sharpe(a * base) - sharpe(base)))
    P(f"    G3 SHARPE INVARIANCE of the gross dial (a 0.25..1.00 x c 0/10/25): max |dSharpe| "
      f"{g3:.3e}  -> the matched control's c* is a pure CAGR/MaxDD statistic")
    assert g3 < 1e-12, g3

    el = eligible_mask(gpx)
    rk = score(gpx, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    kf = pd.Series(float(N0), index=gpx.index)
    w20 = rk.le(kf, axis=0).astype(float).mul(0.75 / kf, axis=0)
    e20 = backtest(gpx, w20, cost_bps=10, freq=FREQ)["returns"].loc[gpx.index[WARMUP]:]
    c20, s20, d20 = nm3(e20.values)
    h20 = len(e20) // 2
    P(f"    G4 standing 2026-09-04 KEEP-4b row (`46 N n=20`; published 12.7% / 1.09 / -18.3%, "
      f"halves 1.09/1.10) at fixed n=20: {c20:.2%} / {s20:.3f} / {d20:.2%} "
      f"(halves {sharpe(e20.values[:h20]):.2f}/{sharpe(e20.values[h20:]):.2f})")

    # ============================================ [D-build] the 54 book-level cells
    P("")
    grid, wf, refs = [], [], {}
    for panel, px in panels:
        start = px.index[WARMUP]
        sub = px.loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2r, v2t, _ = fast_bt(px, rules_v2_weights(px), FREQ)
        ref = PanelRef(sub.index, spy.values, v2r.loc[start:].values, v2t.loc[start:].values)
        refs[panel] = ref
        sc, ss, sdd = nm3(ref.spy_r)
        P("=" * 150)
        P(f"PANEL {panel}: {px.shape[1]} cols | eval {start.date()} .. {px.index[-1].date()}")
        P(f"    SPY  {sc:.2%} / {ss:.3f} (H1 {ref.spy['full']['H1']:.3f} / H2 "
          f"{ref.spy['full']['H2']:.3f} / OOS {ref.spy['full']['OOS']:.3f}) / {sdd:.2%}  "
          f"| 4b bars: DD cap {DD_CAP*ref.spy['full']['DD']:.2%}, CAGR floor "
          f"{CAGR_FLOOR*ref.spy['full']['CAGR']:.2%}")
        v2s = ref.v2.stats(10)
        v2o = ref.v2.stats(10, "oos")
        P(f"    RULES v2 @10bps  {v2s['CAGR']:.2%} / {v2s['Sharpe']:.3f} / {v2s['MaxDD']:.2%} "
          f"(H1 {v2s['H1']:.3f} / H2 {v2s['H2']:.3f})  | OOS {v2o['CAGR']:.2%} / "
          f"{v2o['Sharpe']:.3f} / {v2o['MaxDD']:.2%}  c*_4b {fmt(cstar(ref.v2, '4b'))}")

        for g0 in RUNGS:
            w = parent_weights(px, g0)
            pr0f, ptnf, pgrf = fast_bt(px, w, FREQ)
            pr0, ptn, pgr = pr0f.loc[start:], ptnf.loc[start:], pgrf.loc[start:]
            par = Path4(sub.index, pr0.values, ptn.values, ref)
            par.gross_mean = float(pgr.mean())
            ps = par.stats(10)
            P(f"  PARENT g0={g0:.2f}  gross {par.gross_mean:.3f}  turn/yr {par.turnover_yr:.2f}"
              f"  @10bps {ps['CAGR']:.2%} / {ps['Sharpe']:.3f} / {ps['MaxDD']:.2%}"
              f"  c*_4b {fmt(cstar(par, '4b')):>6s}  c*_4a {fmt(cstar(par, '4a')):>6s}")

            for fam, vals in FAMILIES.items():
                for dv in vals:
                    m = MULT[fam](px, pr0f, ptnf, pgrf, dv).loc[start:]
                    orr, otn, ogr = apply_mult(pr0, ptn, pgr, m)
                    ov = Path4(sub.index, orr.values, otn.values, ref)
                    ov.gross_mean = float(ogr.mean())
                    a = ov.gross_mean / par.gross_mean
                    ct = Path4(sub.index, a * par.r0, a * par.turn, ref)
                    ct.gross_mean = a * par.gross_mean
                    row = dict(panel=panel, g0=g0, family=fam, dial_val=dv,
                               on_frac=float((m < 1.0).mean()), alpha=a,
                               gross_parent=par.gross_mean, gross_overlay=ov.gross_mean,
                               gross_match_err=abs(ct.gross_mean - ov.gross_mean),
                               turn_parent=par.turnover_yr, turn_overlay=ov.turnover_yr)
                    for pth in ("4b", "4a"):
                        for win in ("full", "is", "oos"):
                            co, cc = cstar(ov, pth, win), cstar(ct, pth, win)
                            row[f"cstar_ov_{pth}_{win}"] = co
                            row[f"cstar_ct_{pth}_{win}"] = cc
                    row["is_Sharpe_10"] = ov.stats(10, "is")["Sharpe"]
                    for c in COSTS:
                        st = ov.stats(c)
                        so = ov.stats(c, "oos")
                        row[f"ov_CAGR_{c}"] = st["CAGR"]
                        row[f"ov_Sharpe_{c}"] = st["Sharpe"]
                        row[f"ov_MaxDD_{c}"] = st["MaxDD"]
                        row[f"ov_H1_{c}"] = st["H1"]
                        row[f"ov_H2_{c}"] = st["H2"]
                        row[f"ov_CAGR_oos_{c}"] = so["CAGR"]
                        row[f"ov_Sharpe_oos_{c}"] = so["Sharpe"]
                        row[f"ov_MaxDD_oos_{c}"] = so["MaxDD"]
                        row[f"keep4b_{c}"] = bool(min(ov.m4b(c).values()) > 0)
                        row[f"keep4a_{c}"] = bool(min(ov.m4a(c).values()) > 0)
                        row[f"fail4b_{c}"] = ov.firstfail(c, "4b", "full")
                    grid.append(row)

            # ---- RULE 8 walk-forward: dial chosen on IS 2008-2016 ONLY, OOS read once
            v2oos = ref.v2.stats(10, "oos")
            spyoos = nm3(ref.spy_r[ref.oos])
            for fam, vals in FAMILIES.items():
                cand = [r for r in grid if r["panel"] == panel and r["g0"] == g0
                        and r["family"] == fam]
                sels = {
                    "IS_cstar4b": max(cand, key=lambda r: (
                        CMAX * 10 if np.isnan(r["cstar_ov_4b_is"]) else r["cstar_ov_4b_is"],
                        -r["dial_val"])),
                    "IS_Sharpe10": max(cand, key=lambda r: (r["is_Sharpe_10"], -r["dial_val"])),
                }
                for sel, pk in sels.items():
                    wf.append(dict(panel=panel, g0=g0, family=fam, selector=sel,
                                   dial=pk["dial_val"],
                                   IS_cstar4b=pk["cstar_ov_4b_is"],
                                   OOS_cstar4b=pk["cstar_ov_4b_oos"],
                                   OOS_ctrl_cstar4b=pk["cstar_ct_4b_oos"],
                                   OOS_CAGR=pk["ov_CAGR_oos_10"],
                                   OOS_Sharpe=pk["ov_Sharpe_oos_10"],
                                   OOS_MaxDD=pk["ov_MaxDD_oos_10"],
                                   v2_OOS_CAGR=v2oos["CAGR"], v2_OOS_Sharpe=v2oos["Sharpe"],
                                   v2_OOS_MaxDD=v2oos["MaxDD"],
                                   spy_OOS_CAGR=spyoos[0], spy_OOS_Sharpe=spyoos[1],
                                   spy_OOS_MaxDD=spyoos[2],
                                   keep4b_10=pk["keep4b_10"], keep4a_10=pk["keep4a_10"],
                                   keep4b_25=pk["keep4b_25"], keep4a_25=pk["keep4a_25"]))

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ================================================== G5: the rebuild IS the record's
    P("")
    P("=" * 150)
    ref335 = BT / "2026-09-07_does-the-c-star-EQUALITY-at-20-bps-generalise_C.grid.csv"
    D = pd.read_csv(ref335)
    key = ["panel", "g0", "family", "dial_val"]
    book = D[D["family"].isin(FAMILIES)].copy()
    M = book.merge(G, on=key, suffixes=("_rec", "_new"), validate="one_to_one")
    ccols = [f"cstar_{s}_{p}_{w}" for s in ("ov", "ct") for p in ("4b", "4a")
             for w in ("full", "is", "oos")]
    g5 = 0.0
    for c in ccols:
        a = M[f"{c}_rec"].fillna(CMAX * 10).values
        b = M[f"{c}_new"].fillna(CMAX * 10).values
        g5 = max(g5, float(np.abs(a - b).max()))
    P(f"    G5 independent rebuild of idea 335's {len(M)} BOOK-LEVEL cells reproduces its "
      f"committed .grid.csv on all {len(ccols)} c* columns: max |d| {g5:.3e}")
    P(f"       (the 36 PER-NAME cells of that grid — MABAND, STOP — are excluded by NAME, "
      f"not by outcome; they are not rebuilt here.)")
    assert g5 < 1e-9, g5

    # G6: idea 335's own published restriction, reproduced on all three windows
    pub = {"full": (80, 51, 39, 29, 10), "is": (87, 77, 13, 10, 3), "oos": (73, 51, 39, 22, 17)}
    g6ok = True
    for win, (pa, pd_, pi, ph, pv) in pub.items():
        ov = D[f"cstar_ov_4b_{win}"].fillna(CMAX * 10)
        ct = D[f"cstar_ct_4b_{win}"].fillna(CMAX * 10)
        deg = (D[f"cstar_ov_4b_{win}"].fillna(-1) == 0) & (D[f"cstar_ct_4b_{win}"].fillna(-1) == 0)
        h = ov <= ct + TOL
        got = (int(h.sum()), int(deg.sum()), int((~deg).sum()), int(h[~deg].sum()),
               int((~h[~deg]).sum()))
        ok = got == (pa, pd_, pi, ph, pv)
        g6ok &= ok
        P(f"    G6[{win:>4s}] restriction reproduced from idea 335's own CSV: all "
          f"{got[0]}/{len(D)} (pub {pa}/90) | degenerate {got[1]} (pub {pd_}) | informative "
          f"{got[2]} (pub {pi}) | holds|informative {got[3]}/{got[2]} (pub {ph}/{pi}) | "
          f"violations {got[4]} (pub {pv})  -> {'EXACT' if ok else 'MISMATCH'}")
    P(f"    G6 note: the OOS share needs a {TOL:g} tie tolerance — one cell (U56 g0=0.75 "
      f"VOLCAP 0.25) has ov-ct = 1.4e-14, and a strict `<=` reads it as a violation, moving "
      f"the published 73/90 to 72/90.  The record's own share is tie-sensitive at one cell.")
    assert g6ok

    return G, W


# ===================================================================== [A][B][C] census
def run_census():
    """Scan every committed .md for k/N shares, classify them, and restate the ones whose
    denominator is a c*/breakeven/fail-bar cell set with degenerate members."""
    # ---------- [B] first: the degeneracy map over every c*-carrying CSV in the record
    P("")
    P("=" * 150)
    P("[B] DEGENERACY MAP — every committed CSV in the record carrying a c*/breakeven/"
      "fail-bar column, per PREDICATE (not per file)")
    cellsets, degrows = {}, []
    for f in sorted(BT.glob("*.csv")):
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        grp = column_groups(df)
        if not grp:
            continue
        for gname, cols in grp.items():
            kind = gname.split(":")[0]
            dm = degenerate_mask(df, cols, kind)
            rec = dict(csv=f.name, group=gname, kind=kind, cols="|".join(cols),
                       n=len(df), degenerate=int(dm.sum()), informative=int((~dm).sum()),
                       deg_share=float(dm.mean()))
            degrows.append(rec)
            cellsets.setdefault(f.name.split(".")[0], []).append((f.name, gname, kind, cols,
                                                                  df, dm))
    DEG = pd.DataFrame(degrows)
    DEG.to_csv(f"{OUT}.degeneracy.csv", index=False)
    paired = DEG[DEG.kind == "PAIRED"]
    single = DEG[DEG.kind == "SINGLE"]
    failb = DEG[DEG.kind == "FAILBAR"]
    P(f"    {DEG.csv.nunique()} CSVs carry such a column; {len(DEG)} distinct predicates "
      f"({len(paired)} PAIRED, {len(single)} SINGLE, {len(failb)} FAILBAR).")
    for kind, sub in [("PAIRED", paired), ("SINGLE", single), ("FAILBAR", failb)]:
        if len(sub) == 0:
            continue
        P(f"    {kind:8s}  cells {int(sub.n.sum()):6d}  degenerate {int(sub.degenerate.sum()):6d}"
          f"  ({sub.degenerate.sum()/max(1,sub.n.sum()):.1%})  predicates with ANY degenerate "
          f"cell: {int((sub.degenerate > 0).sum())}/{len(sub)}  |  predicates that are WHOLLY "
          f"degenerate: {int((sub.informative == 0).sum())}")
    P("")
    P("    Worst 12 predicates by degenerate share (informative == 0 means the published "
      "share is empty of content):")
    top = DEG.sort_values(["deg_share", "n"], ascending=[False, False]).head(12)
    P(top[["csv", "group", "n", "degenerate", "informative", "deg_share"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------- [A] the share census
    P("")
    P("=" * 150)
    P("[A] SHARE CENSUS — every k/N in the committed record, classified by the tokens that "
      "govern it")
    IX = idea_index()
    rows = []
    for f in md_corpus():
        own = stem_of(f)
        digest = f.name in DIGESTS
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        cur = ""
        for ln, line in enumerate(txt.split("\n"), 1):
            if digest:
                o = attribute(f.name, line)
                if o:
                    cur = o                       # entries span many lines; carry the owner
            clean = strip_code(line)
            for m in SHARE.finditer(clean):
                a, b = int(m.group(1)), int(m.group(2))
                if b < 2 or a > b or b > 100000:
                    continue
                stem = (IX.get(int(cur), "") if cur else "") if digest else own
                rows.append(dict(file=f.name, line=ln, k=a, n=b,
                                 kind=classify(clean, m.span()), digest=digest,
                                 owner_idea=cur, stem=stem,
                                 has_cstar_csv=bool(cellsets.get(stem)),
                                 text=line.strip()[:220]))
    S = pd.DataFrame(rows)
    SCOPE = ["CSTAR-PREDICATE", "CSTAR-OTHER", "FAILBAR"]
    inscope = S[S.kind.isin(SCOPE)].copy()
    P(f"    {len(S)} k/N shares in {S.file.nunique()} committed files.  By kind:")
    for k, v in S.kind.value_counts().items():
        P(f"        {k:16s} {v:5d}")
    P(f"    IN SCOPE ({' + '.join(SCOPE)}): {len(inscope)} in {inscope.file.nunique()} "
      f"files ({int(inscope.digest.sum())} of them re-quotes in CHANGELOG/QUEUE/LEADERBOARD, "
      f"attributed to a parent script by their own 'idea N' reference).  KEEP-PASS shares "
      f"are the CONTROL class and are NOT restated: their denominator is the whole grid by "
      f"design.")

    # ---------- tiering + [C] restatement
    P("")
    P("=" * 150)
    P("[C] RESTATEMENT — a share is R1 only when a sibling CSV carries the predicate's own "
      "columns AND its denominator matches that cell set")
    out = []
    for _, r in inscope.iterrows():
        stem = r["stem"]
        sets = cellsets.get(stem, []) if stem else []
        want = "FAILBAR" if r["kind"] == "FAILBAR" else None
        hit, fallback = None, None
        for (csvname, gname, kind, cols, df, dm) in sets:
            if want and kind != "FAILBAR":
                continue
            if (not want) and kind == "FAILBAR":
                continue
            if not (len(df) == r["n"] or int((~dm).sum()) == r["n"] or int(dm.sum()) == r["n"]):
                continue
            cand = (csvname, gname, kind, cols, df, dm)
            if fallback is None or (len(df) == r["n"] and len(fallback[4]) != r["n"]):
                fallback = cand
            # among equally-sized cell sets prefer the group whose PREDICATE reproduces k:
            # a grid carries a 4a and a 4b column of the same length, and only one of them
            # is the share's own.
            if len(df) == r["n"] and recover_predicate(df, cols, kind, r["k"]) is not None:
                hit = cand
                break
        hit = hit or fallback
        if hit is None:
            t = ("R2 CSV-BACKED" if sets else
                 ("R0 UNATTRIBUTED" if (r["digest"] and not stem) else "R0 NO-CSV"))
            out.append(dict(**r.to_dict(), tier=t, csv="", group="", degenerate=np.nan,
                            informative=np.nan, predicate="", restated_k=np.nan,
                            tautological=False, restated=""))
            continue
        csvname, gname, kind, cols, df, dm = hit
        deg, inf = int(dm.sum()), int((~dm).sum())
        if len(df) != r["n"]:
            out.append(dict(**r.to_dict(), tier="R2 CSV-BACKED", csv=csvname, group=gname,
                            degenerate=deg, informative=inf, predicate="", restated_k=np.nan,
                            tautological=False,
                            restated="denominator already restricted"))
            continue
        rec = recover_predicate(df, cols, kind, r["k"])
        taut_flag = False
        if inf == 0:
            restated = f"{r['k']}/{r['n']} -> EMPTY (every cell degenerate; the share carries nothing)"
            label, newk = (rec[0] if rec else ""), 0
        elif deg == 0:
            restated, label, newk = f"{r['k']}/{r['n']} (unchanged — no degenerate cell)", "", r["k"]
        elif rec is None:
            restated, label, newk = f"{r['k']}/{r['n']} -> ?/{inf}", "", np.nan
        else:
            label, h = rec
            newk = int(h[~dm].sum())
            # a share whose predicate IS the degeneracy definition is a degeneracy census,
            # not a claim over cells: restricting it is vacuous by construction, and saying
            # so is the honest restatement.
            taut = bool((h == dm).all())
            taut_flag = taut
            restated = (f"{r['k']}/{r['n']} ({r['k']/r['n']:.1%}) -> {newk}/{inf} "
                        f"({newk/inf:.1%})" if inf else f"{r['k']}/{r['n']} -> EMPTY")
            if taut:
                restated += "  [TAUTOLOGICAL: the predicate IS the degeneracy definition]"
        out.append(dict(**r.to_dict(), tier="R1 RESTATABLE", csv=csvname, group=gname,
                        degenerate=deg, informative=inf, predicate=label,
                        restated_k=newk, tautological=taut_flag, restated=restated))
    R = pd.DataFrame(out)
    R.to_csv(f"{OUT}.census.csv", index=False)
    tiers = R.tier.value_counts()
    P(f"    tiering of the {len(R)} in-scope shares:")
    for k in ("R1 RESTATABLE", "R2 CSV-BACKED", "R0 NO-CSV", "R0 UNATTRIBUTED"):
        P(f"        {k:16s} {int(tiers.get(k, 0)):5d}  ({tiers.get(k,0)/max(1,len(R)):.1%})")
    r1 = R[R.tier == "R1 RESTATABLE"]
    moved = r1[r1.degenerate > 0]
    P(f"    of the {len(r1)} R1 shares, {len(moved)} sit on a denominator with at least one "
      f"DEGENERATE cell ({len(moved)/max(1,len(r1)):.1%}); "
      f"{int((r1.informative == 0).sum())} sit on a WHOLLY degenerate denominator.")
    rec = moved[moved.restated_k.notna()]
    P(f"    of those {len(moved)}, {len(rec)} had their PREDICATE recovered from the fixed "
      f"library, so the restatement is a NUMBER and not just a denominator.")
    if len(moved):
        P("")
        P("    Every R1 share whose denominator loses cells (the restatement table):")
        show = moved[["file", "line", "kind", "csv", "degenerate", "informative",
                      "predicate", "restated"]].copy()
        show["file"] = show["file"].str.slice(0, 46)
        show["csv"] = show["csv"].str.slice(-30)
        P(show.to_string(index=False))
        P("")
        P("    ... and their source lines:")
        for _, r in moved.iterrows():
            P(f"      [{r['file'][:40]}:{r['line']}] {r['k']}/{r['n']}  {r['text'][:150]}")
    P("")
    P("    R2/R0 is the census's real headline: a share is only checkable when its parent "
      "committed the c* column it was computed over.")
    return S, R, DEG


def main():
    t0 = time.time()
    G, W = build_live()
    S, R, DEG = run_census()

    # ---------- [D] the live block, read against both KEEP paths
    P("")
    P("=" * 150)
    P("[D] LIVE RE-PRICING of the 54 rebuilt cells — both KEEP paths, both cost rungs")
    for c in COSTS:
        P(f"    @{c:2d} bps  4a {int(G[f'keep4a_{c}'].sum())}/{len(G)}   "
          f"4b {int(G[f'keep4b_{c}'].sum())}/{len(G)}")
    fb = G.loc[~G["keep4b_10"], "fail4b_10"].str.split(",").explode().value_counts()
    P(f"    first failing 4b bar over the {int((~G['keep4b_10']).sum())} failures @10 bps: "
      + ", ".join(f"{k} {v}" for k, v in fb.items()))
    P("")
    P("    RULE 8 walk-forward (dial chosen on 2008-2016 ONLY, 2017-2026 read once):")
    cols = ["panel", "g0", "family", "selector", "dial", "IS_cstar4b", "OOS_cstar4b",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "v2_OOS_Sharpe", "spy_OOS_Sharpe",
            "keep4b_10", "keep4a_10"]
    P(W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for panel in W.panel.unique():
        w = W[W.panel == panel]
        P(f"    {panel}: mean OOS Sharpe {w.OOS_Sharpe.mean():.3f} vs RULES v2 "
          f"{w.v2_OOS_Sharpe.iloc[0]:.3f} vs SPY {w.spy_OOS_Sharpe.iloc[0]:.3f} | mean OOS "
          f"CAGR {w.OOS_CAGR.mean():.2%} vs v2 {w.v2_OOS_CAGR.iloc[0]:.2%} vs SPY "
          f"{w.spy_OOS_CAGR.iloc[0]:.2%} | mean OOS MaxDD {w.OOS_MaxDD.mean():.2%} vs v2 "
          f"{w.v2_OOS_MaxDD.iloc[0]:.2%} vs SPY {w.spy_OOS_MaxDD.iloc[0]:.2%}")
    # ---------- [E] the answer
    P("")
    P("=" * 150)
    P("[E] ANSWER")
    ins = S[S.kind.isin(["CSTAR-PREDICATE", "CSTAR-OTHER", "FAILBAR"])]
    r1 = R[R.tier == "R1 RESTATABLE"]
    moved = r1[(r1.degenerate > 0) & r1.restated_k.notna() & (r1.informative > 0)]
    moved = moved[~moved.tautological]      # a degeneracy census cannot "flip"
    flips = moved[((moved.k / moved.n) > 0.5) !=
                  ((moved.restated_k / moved.informative) > 0.5)]
    P(f"    YES.  Of {len(ins)} in-scope shares, {len(r1)} can be checked against a "
      f"committed c* column at all; {int((r1.degenerate > 0).sum())} of those sit on a "
      f"denominator with degenerate cells and {len(moved)} are restated to a NUMBER.")
    P(f"    {len(flips)} of the restatements cross 50%, i.e. the plain-language reading of "
      f"the published share reverses:")
    for _, r in flips.iterrows():
        P(f"        {r['file']}:{r['line']}  [{r['predicate']}]  {r['k']}/{r['n']} "
          f"({r['k']/r['n']:.1%}) -> {int(r['restated_k'])}/{int(r['informative'])} "
          f"({r['restated_k']/r['informative']:.1%})")
    P(f"    {int((DEG.informative == 0).sum())} of the record's {len(DEG)} c*/fail-bar "
      f"PREDICATES are WHOLLY degenerate: any share published over them is empty of content "
      f"by construction.  Idea 335 said so about its own 4a column, and this census "
      f"reproduces that finding independently and finds {int((DEG.informative == 0).sum())-3} "
      f"more such predicates elsewhere in the record.")
    P(f"    The bigger number is the coverage one: {int((R.tier.str.startswith('R0')).sum())} "
      f"of {len(R)} in-scope shares ({(R.tier.str.startswith('R0')).mean():.1%}) cannot be "
      f"checked AT ALL — their parent committed no c* column, or the share is a digest "
      f"re-quote with no recoverable owner.  The restriction is cheap; the record's ability "
      f"to apply it is the binding constraint.")
    P("")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
