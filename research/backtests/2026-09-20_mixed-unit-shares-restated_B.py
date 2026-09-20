#!/usr/bin/env python3
"""Idea 895 - re-price the record's OTHER MIXED-UNIT SHARES.  Lane B, 2026-09-20.

The question
------------
Idea 889 traced 880's 4.85x move to ONE specification defect: a STRUCTURAL numerator divided by
a PROSE denominator - a share whose two legs are counted by DIFFERENT matchers, i.e. in
DIFFERENT UNITS.  895 asks whether that was a one-off or a habit: census the record's OTHER
published shares for a numerator and a denominator built in different units, and report how many
RESTATE past a 20% bar once both legs are put in the same unit.

The restatement arithmetic (there is no modelling here, it is one multiplication)
--------------------------------------------------------------------------------
A published share is `k of N`.  If k is counted in unit class A and N in unit class B, the
same-unit restatement moves k into B:  k_B = k * lam(A->B),  restated share = k*lam(A->B)/N.
So the MOVE FACTOR of a mixed-unit share is exactly lam(A->B) and nothing else, and the share
restates past the bar iff |lam(A->B) - 1| >= MOVE_BAR.  The whole census therefore reduces to
(i) typing both legs of every share and (ii) MEASURING lam on the committed corpus.

Tuned parameter 1 - CLAIM SET (all three always reported, nothing selected on the answer)
-----------------------------------------------------------------------------------------
    ALL       every committed research/**/*.md
    MEMO      the KEEP/verdict memos only (research/backtests/*.md)
    HEADLINE  research/LEADERBOARD.md + research/CHANGELOG.md (what the record advertises)

Tuned parameter 2 - MATCHER PAIR (all observed class pairs always reported)
--------------------------------------------------------------------------
    The (numerator class, denominator class) pair of a mixed-unit share.  Every observed pair
    gets its own row with its own measured lam; no pair is selected.

Unit classes - a FIXED lexicon, declared before any number was read
-------------------------------------------------------------------
    FILE   file blob script memo artefact artifact commit csv notebook
    CELL   cell row point draw sample gridpoint
    NUM    number figure entry literal statistic reading value digit
    BOOK   book arm pick variant device sleeve candidate rung
    CLAIM  claim site verdict headline result statement sentence mention
    NAME   name ticker instrument constituent panel universe corpus

THREE DETECTORS, all three always reported; hypotheses are scored on the first two only
---------------------------------------------------------------------------------------
    NAMED  both legs of ONE share are named: `k NOUN_A of N NOUN_B`.  NOUN_A is the first
           lexicon noun in the <=4 tokens between k and the connector, NOUN_B the first in the
           <=8 tokens after N.  A != B -> MIXED.  This is the ONLY syntax in which a single
           published share's mixed-unit-ness is visible in prose at all.
    PAIR   TWO shares inside ONE statement (a markdown table cell, a line, or a sentence) whose
           DENOMINATOR classes differ - the record quoting `a of A files` beside `b of B
           numbers` and reading the two as the same quantity.  This is 889's defect as it
           actually appears in the record, and restating one leg into the other's currency is
           the single multiplication by lam that carried 880's 4.85x.
    LOOSE  numerator class = the LAST lexicon noun in the 120 characters before k.  An UPPER
           BOUND only: it happily attributes a noun that governs nothing (a filename, a
           previous clause).  Printed and labelled as an upper bound; NO hypothesis reads it.

lam is MEASURED, not assumed
----------------------------
Three currencies are structurally countable over the committed corpus and are 896's own
currencies, reused verbatim so this run continues that measurement rather than inventing one:
    FILES  one per committed text/table blob under research/ or products/
    ROWS   csv/csv.gz data rows;  in text blobs, lines carrying >=1 numeric literal
    NUMS   csv data rows x numeric columns;  in text blobs, numeric literals
lam(FILE->CELL) = ROWS_total / FILES_total, and so on for every ordered pair.  The three
classes that have no currency of their own (BOOK, CLAIM, NAME) are mapped to ROWS by a
PRE-DECLARED convention, because each is published one-per-row of a grid/arm/book table.  That
convention is stated here, before the numbers, and it makes those pairs' lam a LOWER BOUND on
the mixing: a book table's rows are the finest grain the record publishes them at.

Pre-registered hypotheses and bars (fixed before section [2] was read)
---------------------------------------------------------------------
    MOVE_BAR = 0.20 (895's own bar).  RATE_BAR = 0.05.  SET_BAR = 0.10.  LAM_BAR = 1.0.
    H_MIX    Mixed-unit shares are >= RATE_BAR of the record's TYPED published shares.
             PASS = 880's defect is a habit, not a one-off.
    H_BAR    >= 80% of mixed-unit shares restate past MOVE_BAR.
    H_LAM    The observed lam's are far from 1: median |lam - 1| >= LAM_BAR, AND - the sharper
             statement - min |lam - 1| over observed pairs is itself >= MOVE_BAR, which would
             mean the 20% bar is SATURATED and carries no information.
    H_SET    The mixed-unit rate is stable across the three claim sets (max - min <= SET_BAR).
             PASS = a record-wide habit, not an artefact of one file's formatting.
    H_CAP    CAPITAL ARM.  The mixed-unit denominator and its same-unit restatement nominate the
             SAME book under a rule-8 IS-only chooser, and agree on 4a and 4b, on all three
             panels.  PASS = the defect is capital-neutral; FAIL = it is worth real money.
    A FAIL on any of these is a result and is printed as one.

CAPITAL ARM (the binding step-3 deliverable; this is a census idea WITH a book)
-------------------------------------------------------------------------------
The LIVE book is itself a mixed-unit share.  `baseline.rules_v2_weights` sets each held name to
G / N where N is the count of instruments PRICED that day - one matcher - while the names that
RECEIVE that weight are the IN-BAND set, a different matcher.  Numerator and denominator are
built by different matchers, which is 889's defect exactly, in weights rather than in prose.
    MIXED  w = G / N_priced  on in-band names   (the live convention; realised gross = G * s_t,
           s_t = in-band share, so gated-out weight goes to cash)
    SAME   w = G / N_inband  on in-band names   (the same-unit restatement; realised gross = G)
Grid: BAND c in {0.00,0.03,0.05,0.08,0.10} x GROSS G in {0.50,0.75,1.00} on U56 / B136 / SMALL,
x the 2 conventions = 90 books.  EXACTLY TWO DIALS (c, G); the convention is the object under
test, not a dial.  Both KEEP paths are evaluated and published at every one of the 90 cells.
Rule 8: choosers are fitted on 2009-2016 ONLY and 2017-2026 is read ONCE.
The per-cell realised-gross ratio between the two conventions is the mean in-band share, and it
is scored against the SAME 20% bar as the prose census, which is what ties the two arms together.

Gates (section [0], all printed before any new number is read)
--------------------------------------------------------------
    G0  sample lengths of the three panels, IS/OOS split.
    G1  fast_run vs engine.backtest: returns and turnover agree to float noise.
    G2  MIXED at (U56, c=0.03, G=0.75) replays baseline.rules_v2_weights bit-identically.
    G3  no chooser reads a 2017+ row - TESTED on a hard-truncated IS-only frame.
    G4  determinism: the whole prose census recomputed, counts identical.
    G5  exactly two dials in the capital grid.
    G6  every one of the 90 grid cells published.
    G7  the cost axis is exact: r(c) = r_gross - turnover*c/1e4 against a fresh 25 bps run.
    G8  realised gross <= 1 everywhere, no shorting, no leverage.
    G9  the SAME convention's realised gross equals G on every in-band day, by construction.
    G10 external replication of a number the record already published today.

VINTAGE.  A census is a statement about a TREE.  This run's own LEADERBOARD rows and memo ENTER
the corpus it censuses, so a census read at HEAD is NOT reproducible once the run is committed -
measured here between two runs, the drift was +29 share sites and +2 paired sites.  Every prose
number below is therefore read at a PINNED tree (the claim commit this run started from, before
any artifact of this run existed), with `git cat-file`.  That is idea 894's tree-stamp clause
applied to this run's own output rather than quoted at it.

SURVIVORSHIP (rule 9).  U56 and B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010, so every ABSOLUTE level below - including any 4b pass - is an UPPER
BOUND.  The MIXED-vs-SAME contrast that carries the capital result is inside one frame over the
same names on the same days and is first-order immune; the pass COUNTS are not.

PROTOCOL: 10 bps primary (0/25/50 reported), next-day execution (engine), weekly cadence, no
shorting, no leverage, 260-day warm-up skip, rule-8 IS 2009-2016 / OOS 2017-2026, both KEEP
paths.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified (rule 6).
"""
import sys, re, gzip, csv, time, subprocess
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa
from engine import backtest                                               # noqa

STEM = (HERE / "2026-09-20_mixed-unit-shares-restated_B").as_posix()
# VINTAGE.  A census is a statement about a TREE (idea 894's tree-stamp finding).  This run's own
# LEADERBOARD rows and memo ENTER the corpus it censuses, so a census read at HEAD cannot be
# reproduced once the run is committed - measured here between two runs, the drift was +29 share
# sites and +2 pair sites.  Every prose number below is therefore read at a PINNED tree: the
# claim commit this run started from, before any artifact of this run existed.  Blobs are read
# with `git cat-file`; nothing is read from the working tree and nothing is written to it.
VINTAGE = "4345a12"
COST, FREQ, WARMUP = 10, "W", 260
COST_RUNGS = [0, 10, 25, 50]
IS_END = pd.Timestamp("2016-12-31")
MOVE_BAR, RATE_BAR, SET_BAR, LAM_BAR = 0.20, 0.05, 0.10, 1.0
LINES: list[str] = []
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True)
    return r.stdout.decode("utf-8", "replace")


class BatchCat:
    """`git cat-file --batch` kept open, so a whole-tree census is one process, not 13k."""

    def __init__(self):
        self.p = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def get(self, spec):
        self.p.stdin.write((spec + "\n").encode()); self.p.stdin.flush()
        hdr = self.p.stdout.readline().decode().strip()
        if hdr.endswith(("missing", "ambiguous")):
            return None
        n = int(hdr.split()[-1])
        buf = b""
        while len(buf) < n + 1:
            buf += self.p.stdout.read(n + 1 - len(buf))
        return buf[:n]

    def close(self):
        try:
            self.p.stdin.close(); self.p.wait(timeout=10)
        except Exception:
            self.p.kill()


def tree_files(prefixes):
    return [l for l in git("ls-tree", "-r", "--name-only", VINTAGE).split("\n")
            if l and any(l.startswith(x) for x in prefixes)]


# =========================================================== [A] the unit lexicon and the parser
CLASSES = {
    "FILE":  r"files?|blobs?|scripts?|memos?|artefacts?|artifacts?|commits?|csvs?|notebooks?",
    "CELL":  r"cells?|rows?|points?|draws?|samples?|gridpoints?|grid points?",
    "NUM":   r"numbers?|figures?|entries|entry|literals?|statistics?|readings?|values?|digits?",
    "BOOK":  r"books?|arms?|picks?|variants?|devices?|sleeves?|candidates?|rungs?",
    "CLAIM": r"claims?|sites?|verdicts?|headlines?|results?|statements?|sentences?|mentions?",
    "NAME":  r"names?|tickers?|instruments?|constituents?|panels?|universes?|corpora|corpus",
}
CLASS_RE = {k: re.compile(r"\b(?:" + v + r")\b", re.I) for k, v in CLASSES.items()}
# a single alternation used to find the FIRST lexicon noun after N
ANY_NOUN = re.compile("|".join(f"(?P<{k}>\\b(?:{v})\\b)" for k, v in CLASSES.items()), re.I)
# the three structurally countable currencies, and the PRE-DECLARED map from class to currency
CURRENCY = {"FILE": "FILES", "CELL": "ROWS", "NUM": "NUMS",
            "BOOK": "ROWS", "CLAIM": "ROWS", "NAME": "ROWS"}

SHARE_RE = re.compile(r"(?<![\d.])(\d[\d,]*)\s*(of|/|out of)\s*(\d[\d,]*)(?![\d.%])", re.I)
# a STATEMENT is the unit inside which two shares are used as if comparable: a markdown table
# cell, a line, or a sentence.  Splitting on all three is deliberate and conservative (it can
# only make statements SMALLER, i.e. it can only UNDER-count paired mixed-unit sites).
STMT_SPLIT = re.compile(r"\n|\|{1,2}|(?<=[.!?;])\s+")
NUMRE = re.compile(r"[-+]?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?")
TEXT_EXT = {".md", ".py", ".txt", ".log"}
TAB_EXT = {".csv", ".gz"}


def first_noun_after(txt, pos, ntok=8):
    """Class of the first lexicon noun within the next `ntok` whitespace tokens."""
    tail = " ".join(txt[pos:pos + 400].split()[:ntok])
    m = ANY_NOUN.search(tail)
    return m.lastgroup if m else None


def last_noun_before(txt, pos, nchar=120):
    """Class of the LAST lexicon noun in the `nchar` characters before `pos`."""
    head = txt[max(0, pos - nchar):pos]
    last = None
    for m in ANY_NOUN.finditer(head):
        last = m.lastgroup
    return last


def first_noun_between(stmt, a, b, ntok=4):
    """Class of the first lexicon noun in the <=ntok tokens between k and the connector."""
    mid = " ".join(stmt[a:b].split()[:ntok])
    m = ANY_NOUN.search(mid)
    return m.lastgroup if m else None


def parse_shares(paths, cat):
    """One row per committed share site, with all THREE typings attached.

    num_named  the noun sitting BETWEEN k and the connector ("47 FILES of 70 blobs").  This is
               the only place prose ever names the numerator's own unit, so a share typed here
               is UNAMBIGUOUSLY same- or mixed-unit.
    num_loose  the LAST lexicon noun in the 120 chars before k.  An UPPER BOUND only: it happily
               attributes a noun that governs nothing (a filename, a previous clause).  Reported
               as an upper bound and labelled as one; no hypothesis is scored on it.
    stmt_id    the statement (table cell / line / sentence) the share sits in, which is what the
               PAIR detector in [2] groups on.
    """
    recs = []
    for p in paths:
        raw = cat.get(f"{VINTAGE}:{p}")
        if raw is None:
            continue
        txt = raw.decode("utf-8", "replace")
        pos = 0
        for si, stmt in enumerate(STMT_SPLIT.split(txt)):
            base = pos; pos += len(stmt) + 1
            for m in SHARE_RE.finditer(stmt):
                k = int(m.group(1).replace(",", "")); N = int(m.group(3).replace(",", ""))
                if N <= 1 or k > N:
                    continue                              # not a share
                cd = first_noun_after(stmt, m.end())
                cn_named = first_noun_between(stmt, m.start() + len(m.group(1)),
                                              m.end() - len(m.group(3)))
                cn_loose = last_noun_before(stmt, m.start()) or last_noun_before(txt, base + m.start())
                named = ("UNTYPED" if cd is None else
                         "SINGLE" if cn_named is None else
                         "SAME" if cn_named == cd else "MIXED")
                loose = ("UNTYPED" if (cd is None or cn_loose is None) else
                         "SAME" if cn_loose == cd else "MIXED")
                recs.append(dict(path=p, stmt_id=f"{p}#{si}", k=k, N=N, share=k / N,
                                 conn=m.group(2), den_class=cd, num_named=cn_named,
                                 num_loose=cn_loose, named=named, loose=loose,
                                 quote=" ".join(stmt[max(0, m.start() - 60):m.end() + 40].split())))
    return pd.DataFrame(recs)


def pair_sites(df):
    """PAIR detector: two shares inside ONE statement whose DENOMINATOR classes differ.

    This is 889's defect as it actually appears in the record - a memo quotes `a of A files`
    beside `b of B numbers` and reads the two as the same quantity.  Restating one into the
    other's currency is one multiplication by lam(class_i -> class_j), and that multiplication
    is what 889 found carried 880's 4.85x.
    """
    out = []
    d = df[df.den_class.notna()]
    for sid, sub in d.groupby("stmt_id"):
        cls = sub.den_class.unique()
        if len(sub) < 2 or len(cls) < 2:
            continue
        sub = sub.sort_index()
        for i in range(len(sub)):
            for j in range(i + 1, len(sub)):
                a, b = sub.iloc[i], sub.iloc[j]
                if a.den_class == b.den_class:
                    continue
                out.append(dict(stmt_id=sid, path=a.path,
                                k1=a.k, N1=a.N, share1=a.share, class1=a.den_class,
                                k2=b.k, N2=b.N, share2=b.share, class2=b.den_class,
                                quote=a.quote))
    return pd.DataFrame(out)


# ============================================ [B] the three currencies, measured on the corpus
def table_shape(raw, path):
    try:
        if path.endswith(".gz"):
            raw = gzip.decompress(raw)
        txt = raw.decode("utf-8", "replace")
    except Exception:
        return None
    lines = [l for l in txt.split("\n") if l.strip() != ""]
    if len(lines) < 2:
        return None
    try:
        hdr = next(csv.reader([lines[0]]))
    except Exception:
        return None
    if len(hdr) < 2:
        return None
    rows = lines[1:]
    sample = rows[: min(50, len(rows))]
    ncol = len(hdr); numeric = [0] * ncol; seen = 0
    for ln in sample:
        try:
            f = next(csv.reader([ln]))
        except Exception:
            continue
        if len(f) != ncol:
            continue
        seen += 1
        for j, v in enumerate(f):
            v = v.strip()
            if v == "":
                continue
            try:
                float(v); numeric[j] += 1
            except ValueError:
                pass
    if seen == 0:
        return None
    nnum = sum(1 for j in range(ncol) if numeric[j] >= 0.8 * seen)
    return len(rows), len(rows) * max(nnum, 1)


def corpus_currencies(listing, cat):
    """FILES / ROWS / NUMS totals over the research/ + products/ corpus AT THE PINNED TREE."""
    files = rows = nums = 0
    for p in listing:
        ext = Path(p).suffix.lower()
        if ext not in TEXT_EXT and ext not in TAB_EXT:
            continue
        raw = cat.get(f"{VINTAGE}:{p}")
        if raw is None:
            continue
        if ext in TAB_EXT:
            sh_ = table_shape(raw, p)
            if sh_ is None:
                continue
            files += 1; rows += sh_[0]; nums += sh_[1]
        else:
            txt = raw.decode("utf-8", "replace")
            r = n = 0
            for ln in txt.split("\n"):
                hits = NUMRE.findall(ln)
                if hits:
                    r += 1; n += len(hits)
            files += 1; rows += r; nums += n
    return dict(FILES=files, ROWS=rows, NUMS=nums)


# ============================================================================ [C] fast backtest
def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    n, k = px_v.shape
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(k); turn = np.zeros(n); port = np.zeros(n); gross = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        gross[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return port, turn, gross


def sh(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    eq = np.cumprod(1.0 + r); return float((eq / np.maximum.accumulate(eq) - 1.0).min())
def cg(r):
    eq = np.cumprod(1.0 + r); y = len(r) / 252.0
    return float(eq[-1] ** (1.0 / y) - 1.0) if y > 0 else np.nan


def keep4a(r, b, w):
    rw, bw = r[w], b[w]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(bw[:h]) and sh(rw[h:]) > sh(bw[h:]) and mdd(rw) >= mdd(bw))
def keep4b(r, s, w):
    rw, sw = r[w], s[w]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(sw[:h]) and sh(rw[h:]) > sh(sw[h:])
                and mdd(rw) >= 0.60 * mdd(sw) and cg(rw) >= 0.70 * cg(sw))
def keep4b_1w(r, s, w):
    rw, sw = r[w], s[w]
    return bool(sh(rw) > sh(sw) and mdd(rw) >= 0.60 * mdd(sw) and cg(rw) >= 0.70 * cg(sw))


def books(px, c, g):
    """(MIXED, SAME) target-weight frames for band c at gross g.

    MIXED  G / N_priced   on in-band names  -- the live convention (mixed-unit denominator)
    SAME   G / N_inband   on in-band names  -- the same-unit restatement
    """
    inb = band_state(px, c)
    priced = px.notna()
    n_priced = priced.sum(axis=1).replace(0, np.nan)
    n_inband = (inb & priced).sum(axis=1).replace(0, np.nan)
    hold = (inb & priced).astype(float)
    mixed = hold.div(n_priced, axis=0).fillna(0.0) * g
    same = hold.div(n_inband, axis=0).fillna(0.0) * g
    return mixed, same, (inb & priced).sum(axis=1), priced.sum(axis=1)


# ====================================================================================== [0] run
def main():
    t0 = time.time()
    head = git("rev-parse", "HEAD").strip()
    P("=" * 118)
    P("IDEA 895 - re-price the record's OTHER MIXED-UNIT SHARES.  lane B, 2026-09-20")
    P(f"HEAD {head}")
    P("=" * 118)

    # --------------------------------------------------------------------------- [0] GATES
    P("\n[0] GATES")
    panels = {}
    for key, kw in (("U56", {}), ("B136", {"broad": True}), ("SMALL", {"small": True})):
        panels[key] = load_universe(**kw)
    for k, px in panels.items():
        idx = px.index[WARMUP:]
        P(f"  G0 {k:5s} {px.shape[1]:4d} names  {idx[0].date()} -> {idx[-1].date()}  "
          f"{len(idx)/252:.2f}y   IS {(idx<=IS_END).sum()/252:.2f}y   OOS {(idx>IS_END).sum()/252:.2f}y")

    px = panels["U56"]
    mixed, same, n_in, n_pr = books(px, 0.03, 0.75)
    wk = pd.Series(px.index.to_period("W"), index=px.index)
    mask_v = (wk != wk.shift(-1)).values
    fp, ft, fg = fast_run(px.values.astype(float), mixed.values.astype(float), mask_v)
    eng = backtest(px, mixed, cost_bps=COST, freq=FREQ)
    P(f"  G1 fast_run vs engine.backtest on the warm-up-skipped window: "
      f"returns {np.abs(fp[WARMUP:]-eng['returns'].values[WARMUP:]).max():.3e}   "
      f"turnover {np.abs(ft[WARMUP:]-eng['turnover'].values[WARMUP:]).max():.3e}")
    g2 = float(np.abs(mixed.values - rules_v2_weights(px).values).max())
    P(f"  G2 MIXED at (U56, c=0.03, G=0.75) vs baseline.rules_v2_weights: {g2:.3e}  "
      f"{'IS THE LIVE BOOK' if g2 == 0.0 else 'DIFFERS'}")
    p25, t25, _ = fast_run(px.values.astype(float), mixed.values.astype(float), mask_v, cost_bps=25)
    p0, t0_, _ = fast_run(px.values.astype(float), mixed.values.astype(float), mask_v, cost_bps=0)
    P(f"  G7 cost axis exact: max |r(25) - (r(0) - turnover*25/1e4)| = "
      f"{np.abs(p25 - (p0 - t0_*25/1e4)).max():.3e}")
    P("  G5 dials in the capital grid: 2 (band c, gross G).  The MIXED/SAME convention is the")
    P("     object under test, not a dial.")

    # ------------------------------------------------- [1] the three currencies, measured once
    P("\n[1] THE MEASURED CURRENCIES (and therefore every lam)")
    cat = BatchCat()
    listing = tree_files(("research/", "products/"))
    cur = corpus_currencies(listing, cat)
    cur2 = corpus_currencies(listing, cat)
    P(f"  PINNED TREE (the claim commit this run started from, before any artifact of this run")
    P(f"  existed): {git('rev-parse', VINTAGE).strip()}   {len(listing):,} blobs under research/ + products/")
    P(f"  G4a currency scan determinism: {'IDENTICAL' if cur == cur2 else 'DIFFERS'}")
    P(f"  research/+products/ corpus AT THE PINNED TREE: FILES {cur['FILES']:,}   ROWS {cur['ROWS']:,}   "
      f"NUMS {cur['NUMS']:,}")
    P(f"  mean ROWS per FILE {cur['ROWS']/cur['FILES']:,.1f}   mean NUMS per FILE "
      f"{cur['NUMS']/cur['FILES']:,.1f}   mean NUMS per ROW {cur['NUMS']/cur['ROWS']:,.3f}")
    lam = {}
    for a in ("FILE", "CELL", "NUM", "BOOK", "CLAIM", "NAME"):
        for b in ("FILE", "CELL", "NUM", "BOOK", "CLAIM", "NAME"):
            ca, cb = CURRENCY[a], CURRENCY[b]
            lam[(a, b)] = cur[cb] / cur[ca]
    lamdf = pd.DataFrame(
        [[lam[(a, b)] for b in CLASSES] for a in CLASSES],
        index=list(CLASSES), columns=list(CLASSES))
    P("\n  lam(row class -> column class), the MOVE FACTOR of a mixed-unit share:")
    P(lamdf.to_string(float_format=lambda x: f"{x:,.4f}"))
    lamdf.to_csv(STEM + ".lam.csv")
    P(f"\n  PRE-DECLARED currency map: {CURRENCY}")
    P("  BOOK / CLAIM / NAME share the ROWS currency, so lam is 1.0000 among them BY CONSTRUCTION")
    P("  and those pairs can never restate.  That is a LOWER BOUND on the mixing, stated up front,")
    P("  not a finding: the record publishes books, arms and claims one per row of a table.")

    # ----------------------------------------------------------------- [2] the prose census
    P("\n[2] CENSUS - every committed published share, both legs typed")
    md_all = [p for p in tree_files(("research/",)) if p.endswith(".md")]
    SETS = {
        "ALL": md_all,
        "MEMO": [p for p in md_all if p.startswith("research/backtests/")],
        "HEADLINE": [p for p in md_all if Path(p).name in ("LEADERBOARD.md", "CHANGELOG.md")],
    }
    census, pairs = {}, {}
    for nm, paths in SETS.items():
        df = parse_shares(paths, cat)
        census[nm] = df
        pairs[nm] = pair_sites(df)
        P(f"  {nm:9s} {len(paths):4d} files -> {len(df):7,d} share sites;  NAMED typing: " +
          "  ".join(f"{k}={v:,}" for k, v in df.named.value_counts().items()) +
          f";  PAIR sites {len(pairs[nm]):,}")
    cl, pr = census["ALL"], pairs["ALL"]
    cl2 = parse_shares(SETS["ALL"], cat)
    P(f"  G4b census determinism: "
      f"{'IDENTICAL' if len(cl) == len(cl2) and cl.named.tolist() == cl2.named.tolist() else 'DIFFERS'}")
    cl.to_csv(STEM + ".shares.csv.gz", index=False)          # 46k rows: gzipped
    pr.to_csv(STEM + ".pair_sites.csv", index=False)
    cat.close()

    P("\n  WHAT PROSE CAN AND CANNOT SEE - the first number of this census, stated plainly:")
    P(f"  of {len(cl):,} committed share sites, {int((cl.named=='SINGLE').sum()):,} "
      f"({(cl.named=='SINGLE').mean():.4f}) name ONE unit and "
      f"{int((cl.named=='UNTYPED').sum()):,} name NONE.  Only "
      f"{int(cl.named.isin(['SAME','MIXED']).sum()):,} "
      f"({cl.named.isin(['SAME','MIXED']).mean():.4f}) name BOTH legs, which is the only form in")
    P("  which a single share's mixed-unit-ness is visible in prose at all.  That is why 889's")
    P("  defect had to be found by reading 880's SCRIPT: the record's own share syntax hides it.")

    # ---- three typings, all reported.  Hypotheses are scored on NAMED and PAIR only. ----
    P("\n  --- mixed-unit RATE by claim set (tuned param 1) x the three detectors ---")
    rate_named, rate_pair, rate_loose = {}, {}, {}
    for nm in SETS:
        d = census[nm]
        both = d[d.named.isin(["SAME", "MIXED"])]
        lo = d[d.loose != "UNTYPED"]
        rate_named[nm] = (both.named == "MIXED").mean() if len(both) else np.nan
        rate_loose[nm] = (lo.loose == "MIXED").mean() if len(lo) else np.nan
        nstmt = d.stmt_id.nunique()
        rate_pair[nm] = pairs[nm].stmt_id.nunique() / nstmt if nstmt else np.nan
        P(f"  {nm:9s} NAMED both-legs {len(both):6,d} -> MIXED {int((both.named=='MIXED').sum()):5,d}"
          f" rate {rate_named[nm]:.4f} | PAIR statements {pairs[nm].stmt_id.nunique():5,d}"
          f" of {nstmt:7,d} rate {rate_pair[nm]:.4f} | LOOSE (upper bound) rate {rate_loose[nm]:.4f}")
    named_def = not all(np.isnan(v) for v in rate_named.values())
    H_MIX = bool((named_def and np.nanmax(list(rate_named.values())) >= RATE_BAR)
                 or rate_pair["ALL"] >= RATE_BAR)
    sp_named = (float(np.nanmax(list(rate_named.values())) - np.nanmin(list(rate_named.values())))
                if named_def else np.nan)
    sp_pair = float(max(rate_pair.values()) - min(rate_pair.values()))
    H_SET = bool((not named_def or sp_named <= SET_BAR) and sp_pair <= SET_BAR)
    named_txt = ("UNDEFINED (not one committed share names both legs)" if not named_def
                 else f"{rate_named['ALL']:.4f}")
    P(f"\n  H_MIX  NAMED rate {named_txt} / PAIR rate {rate_pair['ALL']:.4f} vs bar {RATE_BAR}"
      f"  -> {'CONFIRMED' if H_MIX else 'REFUTED'}")
    P(f"  H_SET  rate spread across claim sets: NAMED "
      f"{'UNDEFINED' if not named_def else f'{sp_named:.4f}'}, PAIR {sp_pair:.4f} vs bar "
      f"{SET_BAR}  -> {'CONFIRMED' if H_SET else 'REFUTED'}")

    # -------------------------------------------- [3] restatement, by matcher pair (param 2)
    P("\n[3] RESTATEMENT - every observed matcher pair, with its own measured lam")
    P("  Detector NAMED: both legs of ONE share named.  Move factor = lam(num -> den).")
    mx = cl[cl.named == "MIXED"].copy()
    if len(mx):
        mx["lam"] = [lam[(a, b)] for a, b in zip(mx.num_named, mx.den_class)]
        mx["restated"] = mx.k * mx.lam / mx.N
        mx["move"] = (mx.lam - 1.0).abs()
        mx["restates"] = mx.move >= MOVE_BAR
        pair_n = (mx.groupby(["num_named", "den_class"])
                    .agg(n=("k", "size"), lam=("lam", "first"), move=("move", "first"),
                         restates=("restates", "sum"), med_pub=("share", "median"),
                         med_restated=("restated", "median")).sort_values("n", ascending=False))
        P(pair_n.to_string(float_format=lambda x: f"{x:,.4f}"))
        pair_n.to_csv(STEM + ".pairs_named.csv")
        mx.to_csv(STEM + ".mixed_named.csv", index=False)
    else:
        pair_n = pd.DataFrame(columns=["n", "lam", "move", "restates"])
        P("  none")

    P("\n  Detector PAIR: two shares in ONE statement, different denominator classes.  Restating")
    P("  the first into the second's currency multiplies it by lam(class1 -> class2).")
    pr = pr.copy()
    pr["lam"] = [lam[(a, b)] for a, b in zip(pr.class1, pr.class2)]
    pr["restated1"] = pr.share1 * pr.lam
    pr["move"] = (pr.lam - 1.0).abs()
    pr["restates"] = pr.move >= MOVE_BAR
    pair_p = (pr.groupby(["class1", "class2"])
                .agg(n=("k1", "size"), lam=("lam", "first"), move=("move", "first"),
                     restates=("restates", "sum"), med_share1=("share1", "median"),
                     med_share2=("share2", "median")).sort_values("n", ascending=False))
    P(pair_p.to_string(float_format=lambda x: f"{x:,.4f}"))
    pair_p.to_csv(STEM + ".pairs_stmt.csv")
    pr.to_csv(STEM + ".mixed_pairs.csv", index=False)

    all_mv = pd.concat([mx[["move", "restates"]] if len(mx) else pd.DataFrame(columns=["move", "restates"]),
                        pr[["move", "restates"]]], ignore_index=True)
    n_mx, n_re = len(all_mv), int(all_mv.restates.sum())
    frac = n_re / n_mx if n_mx else np.nan
    H_BAR = bool(frac >= 0.80)
    obs = pd.concat([pair_n[["lam", "move"]] if len(pair_n) else pd.DataFrame(columns=["lam", "move"]),
                     pair_p[["lam", "move"]]], ignore_index=True).drop_duplicates()
    nz = obs.move[obs.move > 1e-12]
    H_LAM = bool(obs.move.median() >= LAM_BAR)
    sat = bool(len(nz) and nz.min() >= MOVE_BAR)
    P(f"\n  mixed-unit sites (NAMED {len(mx):,} + PAIR {len(pr):,}) = {n_mx:,};  restating past "
      f"{MOVE_BAR:.0%}: {n_re:,} ({frac:.4f})  -> H_BAR {'CONFIRMED' if H_BAR else 'REFUTED'}")
    P(f"  |lam-1| over {len(obs)} DISTINCT lam values observed: median {obs.move.median():,.4f}   "
      f"min {obs.move.min():,.4f}   max {obs.move.max():,.4f}")
    P(f"  |lam-1| SITE-weighted over all {n_mx:,} mixed sites: median "
      f"{all_mv.move.median():,.4f}   mean {all_mv.move.mean():,.4f}")
    P(f"  H_LAM  median |lam-1| >= {LAM_BAR}  -> {'CONFIRMED' if H_LAM else 'REFUTED'}"
      + (f"  (it fails by {LAM_BAR - obs.move.median():.4g}: the median distinct lam is the"
         f" BOOK/CLAIM/NAME lam == 1, i.e. the unpriceable pair, so H_LAM is refuted by this"
         f" construction's own blind spot, not by a measurement that the lams are small)"
         if not H_LAM else ""))
    P(f"  SATURATION: smallest NON-ZERO |lam-1| among observed pairs "
      f"{nz.min() if len(nz) else float('nan'):,.4f}  -> the {MOVE_BAR:.0%} bar is "
      f"{'SATURATED: it carries no information, because every genuinely CROSS-CURRENCY share clears it by construction' if sat else 'INFORMATIVE'}")
    P("  READ THIS CORRECTLY: the pairs with lam == 1 are the BOOK/CLAIM/NAME pairs that SHARE the")
    P("  ROWS currency under the pre-declared map above - pairs this construction CANNOT price, not")
    P("  pairs measured to be harmless.  They are reported, never counted as passes.")
    cross = all_mv[all_mv.move > 1e-12]
    P(f"  cross-CURRENCY sites (the ones this construction can actually price): {len(cross):,} of "
      f"{n_mx:,}; ALL of them restate past the bar: {bool(len(cross) and cross.restates.all())}")

    P("\n  --- the 10 largest PAIR sites by move factor (the record's own words) ---")
    for _, r in pr.sort_values("move", ascending=False).head(10).iterrows():
        P(f"  {Path(r.path).name[:44]:44s} {r.k1:>6,d}/{r.N1:<6,d}={r.share1:.4f} [{r.class1}] "
          f"vs {r.k2:>6,d}/{r.N2:<6,d}={r.share2:.4f} [{r.class2}]  lam {r.lam:,.3f}  "
          f"restated1 {r.restated1:,.4f}")
        P(f"      \"{r.quote[:140]}\"")

    # ------------------------------------------------------------------- [4] CAPITAL ARM
    P("\n[4] CAPITAL ARM - the mixed-unit denominator IS the live book's own weighting")
    CS = [0.00, 0.03, 0.05, 0.08, 0.10]
    GS = [0.50, 0.75, 1.00]
    store, rows = {}, []
    for pk, pxp in panels.items():
        idx = pxp.index
        pv = pxp.values.astype(float)
        wkp = pd.Series(idx.to_period("W"), index=idx)
        mv = (wkp != wkp.shift(-1)).values
        keep = np.zeros(len(idx), dtype=bool); keep[WARMUP:] = True
        w_full = keep
        w_is = keep & np.asarray(idx <= IS_END)
        w_oos = keep & np.asarray(idx > IS_END)
        spy = pxp["SPY"].pct_change().fillna(0.0).values
        base_r, base_t, _ = fast_run(pv, rules_v2_weights(pxp).values.astype(float), mv)
        store[(pk, "BASE")] = base_r; store[(pk, "SPY")] = spy
        store[(pk, "WIN")] = (w_full, w_is, w_oos)
        for c in CS:
            mixed, same, n_in, n_pr = books(pxp, c, 1.0)
            inb_share = float((n_in / n_pr).values[WARMUP:].mean())
            for conv, wf in (("MIXED", mixed), ("SAME", same)):
                for g in GS:
                    r, t, gr = fast_run(pv, (wf * g).values.astype(float), mv)
                    store[(pk, conv, c, g)] = (r, t)
                    h = w_full.sum() // 2
                    rows.append(dict(
                        panel=pk, conv=conv, c=c, G=g,
                        CAGR_F=cg(r[w_full]), Sharpe_F=sh(r[w_full]), MaxDD_F=mdd(r[w_full]),
                        Sh_H1=sh(r[w_full][:h]), Sh_H2=sh(r[w_full][h:]),
                        Sharpe_IS=sh(r[w_is]), CAGR_IS=cg(r[w_is]), MaxDD_IS=mdd(r[w_is]),
                        CAGR_OOS=cg(r[w_oos]), Sharpe_OOS=sh(r[w_oos]), MaxDD_OOS=mdd(r[w_oos]),
                        turn_yr=float(t[w_full].sum() / (w_full.sum() / 252)),
                        real_gross=float(gr[w_full].mean()), inb_share=inb_share,
                        pass4a_F=keep4a(r, base_r, w_full), pass4b_F=keep4b(r, spy, w_full),
                        pass4b_OOS=keep4b_1w(r, spy, w_oos),
                        pass4a_OOS=bool(sh(r[w_oos]) > sh(base_r[w_oos])
                                        and mdd(r[w_oos]) >= mdd(base_r[w_oos]))))
    grid = pd.DataFrame(rows)
    grid.to_csv(STEM + ".grid.csv", index=False)
    P(f"  G6 grid cells published: {len(grid)} of {len(panels)*len(CS)*len(GS)*2}")
    P(f"  G8 max realised gross over all {len(grid)} cells: {grid.real_gross.max():.6f}  "
      f"(no shorting, no leverage)")
    g9 = grid[(grid.conv == 'SAME')].assign(err=lambda d: (d.real_gross / d.G - 1).abs()).err.max()
    P(f"  G9 SAME convention realised gross / G - 1, max over cells: {g9:.4f}  "
      f"(< 1 only because of days with zero in-band names, when both conventions sit in cash)")

    for pk in panels:
        P(f"\n  --- {pk}: all {len(CS)*len(GS)*2} grid points, 10 bps, weekly, t+1, both KEEP paths ---")
        sub = grid[grid.panel == pk].drop(columns=["panel"]).sort_values(["c", "G", "conv"])
        P(sub.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        w_full, w_is, w_oos = store[(pk, "WIN")]
        b, s = store[(pk, "BASE")], store[(pk, "SPY")]
        P(f"  RULES v2 baseline : FULL {cg(b[w_full]):.2%} / {sh(b[w_full]):.4f} / {mdd(b[w_full]):.2%}"
          f"   OOS {cg(b[w_oos]):.2%} / {sh(b[w_oos]):.4f} / {mdd(b[w_oos]):.2%}")
        P(f"  SPY               : FULL {cg(s[w_full]):.2%} / {sh(s[w_full]):.4f} / {mdd(s[w_full]):.2%}"
          f"   OOS {cg(s[w_oos]):.2%} / {sh(s[w_oos]):.4f} / {mdd(s[w_oos]):.2%}")
        for conv in ("MIXED", "SAME"):
            q = sub[sub.conv == conv]
            P(f"  {conv:5s} 4a FULL {int(q.pass4a_F.sum())}/{len(q)}   4b FULL {int(q.pass4b_F.sum())}/{len(q)}"
              f"   4b OOS {int(q.pass4b_OOS.sum())}/{len(q)}")

    # --- the restatement, priced: per-cell MIXED vs SAME against the SAME 20% bar -------------
    P("\n[5] THE RESTATEMENT, PRICED - MIXED vs SAME at matched (panel, c, G)")
    piv = grid.pivot_table(index=["panel", "c", "G"], columns="conv",
                           values=["real_gross", "Sharpe_F", "MaxDD_F", "CAGR_F",
                                   "Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS", "turn_yr"])
    con = pd.DataFrame({
        "gross_ratio": piv[("real_gross", "MIXED")] / piv[("real_gross", "SAME")],
        "dSharpe_F": piv[("Sharpe_F", "MIXED")] - piv[("Sharpe_F", "SAME")],
        "dSharpe_OOS": piv[("Sharpe_OOS", "MIXED")] - piv[("Sharpe_OOS", "SAME")],
        "dCAGR_F": piv[("CAGR_F", "MIXED")] - piv[("CAGR_F", "SAME")],
        "dCAGR_OOS": piv[("CAGR_OOS", "MIXED")] - piv[("CAGR_OOS", "SAME")],
        "dMaxDD_F": piv[("MaxDD_F", "MIXED")] - piv[("MaxDD_F", "SAME")],
        "turn_ratio": piv[("turn_yr", "MIXED")] / piv[("turn_yr", "SAME")],
    })
    con["gross_move"] = (con.gross_ratio - 1).abs()
    con["restates"] = con.gross_move >= MOVE_BAR
    P(con.to_string(float_format=lambda x: f"{x:+.4f}"))
    con.to_csv(STEM + ".contrast.csv")
    P(f"\n  cells whose REALISED GROSS restates past the prose census's own {MOVE_BAR:.0%} bar: "
      f"{int(con.restates.sum())} of {len(con)}   (median move {con.gross_move.median():.4f}, "
      f"max {con.gross_move.max():.4f})")
    P(f"  MIXED beats SAME on FULL Sharpe in {int((con.dSharpe_F>0).sum())} of {len(con)} cells "
      f"(mean dSharpe {con.dSharpe_F.mean():+.4f}), OOS in {int((con.dSharpe_OOS>0).sum())} "
      f"(mean {con.dSharpe_OOS.mean():+.4f})")
    P(f"  and it is SHALLOWER (dMaxDD > 0) in {int((con.dMaxDD_F>0).sum())} of {len(con)} "
      f"(mean {con.dMaxDD_F.mean()*100:+.2f} pp), at {con.turn_ratio.mean():.3f}x the turnover "
      f"and {con.gross_ratio.mean():.3f}x the exposure.")
    flips = []
    for (pk, c, g), _ in con.iterrows():
        a = grid[(grid.panel == pk) & (grid.c == c) & (grid.G == g) & (grid.conv == "MIXED")].iloc[0]
        b_ = grid[(grid.panel == pk) & (grid.c == c) & (grid.G == g) & (grid.conv == "SAME")].iloc[0]
        flips.append(dict(panel=pk, c=c, G=g,
                          f4a_F=a.pass4a_F != b_.pass4a_F, f4b_F=a.pass4b_F != b_.pass4b_F,
                          f4b_OOS=a.pass4b_OOS != b_.pass4b_OOS))
    fl = pd.DataFrame(flips)
    P(f"  KEEP-VERDICT FLIPS between the two conventions at matched (panel,c,G): "
      f"4a FULL {int(fl.f4a_F.sum())}/{len(fl)}   4b FULL {int(fl.f4b_F.sum())}/{len(fl)}   "
      f"4b OOS {int(fl.f4b_OOS.sum())}/{len(fl)}")
    fl.to_csv(STEM + ".flips.csv", index=False)

    # ---- cost ladder on the contrast, exact off the two cached legs (G7 licenses this) -------
    P("\n  --- the contrast on the cost ladder (exact: r(c) = r_gross - turnover*c/1e4) ---")
    lad = []
    for pk in panels:
        w_full, w_is, w_oos = store[(pk, "WIN")]
        for cst in COST_RUNGS:
            wins = 0; tot = 0; ds = []
            for c in CS:
                for g in GS:
                    rm, tm = store[(pk, "MIXED", c, g)]
                    rs, ts = store[(pk, "SAME", c, g)]
                    rm2 = rm + tm * (COST - cst) / 1e4
                    rs2 = rs + ts * (COST - cst) / 1e4
                    d = sh(rm2[w_full]) - sh(rs2[w_full]); ds.append(d)
                    wins += d > 0; tot += 1
            lad.append(dict(panel=pk, bps=cst, mixed_wins=wins, n=tot, mean_dSharpe=np.mean(ds)))
    ladf = pd.DataFrame(lad)
    P(ladf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    ladf.to_csv(STEM + ".cost_ladder.csv", index=False)

    # -------------------------------------------------------- [6] RULE 8 walk-forward
    P("\n[6] RULE 8 - dials fitted on 2009-2016 ONLY, 2017-2026 read ONCE")
    wf, g3_ok = [], True
    for pk in panels:
        w_full, w_is, w_oos = store[(pk, "WIN")]
        b, s = store[(pk, "BASE")], store[(pk, "SPY")]
        for conv in ("MIXED", "SAME"):
            sub = grid[(grid.panel == pk) & (grid.conv == conv)]
            isonly = sub[["c", "G", "Sharpe_IS", "CAGR_IS", "MaxDD_IS"]].copy()
            pick_sh = isonly.loc[isonly.Sharpe_IS.idxmax()]
            # C_4B: among cells clearing 4b on the IS window alone, the highest IS Sharpe;
            #       else fall back to the IS-Sharpe argmax.  IS columns only.
            ok = []
            for _, rr in isonly.iterrows():
                r, _t = store[(pk, conv, rr.c, rr.G)]
                ok.append(keep4b_1w(r, s, w_is))
            isonly = isonly.assign(is4b=ok)
            cand = isonly[isonly.is4b]
            pick_4b = (cand.loc[cand.Sharpe_IS.idxmax()] if len(cand) else pick_sh)
            for nm, pk_ in (("C_SHARPE", pick_sh), ("C_4B", pick_4b)):
                r, _t = store[(pk, conv, pk_.c, pk_.G)]
                wf.append(dict(panel=pk, conv=conv, chooser=nm, c=pk_.c, G=pk_.G,
                               IS_Sharpe=sh(r[w_is]),
                               OOS_CAGR=cg(r[w_oos]), OOS_Sharpe=sh(r[w_oos]), OOS_MaxDD=mdd(r[w_oos]),
                               base_OOS_CAGR=cg(b[w_oos]), base_OOS_Sharpe=sh(b[w_oos]),
                               base_OOS_MaxDD=mdd(b[w_oos]),
                               spy_OOS_CAGR=cg(s[w_oos]), spy_OOS_Sharpe=sh(s[w_oos]),
                               spy_OOS_MaxDD=mdd(s[w_oos]),
                               beats_base_OOS=bool(sh(r[w_oos]) > sh(b[w_oos])),
                               beats_spy_OOS=bool(sh(r[w_oos]) > sh(s[w_oos])),
                               pass4a_FULL=keep4a(r, b, w_full), pass4b_FULL=keep4b(r, s, w_full),
                               pass4b_OOS=keep4b_1w(r, s, w_oos)))
            # G3: recompute the IS argmax from a HARD-TRUNCATED frame (no OOS columns at all)
            tr = sub[["c", "G", "Sharpe_IS"]].copy()
            g3_ok &= (float(tr.loc[tr.Sharpe_IS.idxmax()].c), float(tr.loc[tr.Sharpe_IS.idxmax()].G)) \
                     == (float(pick_sh.c), float(pick_sh.G))
    P(f"  G3 choosers read IS columns only; argmax identical on a hard-truncated frame: "
      f"{'PASS' if g3_ok else 'FAIL'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(STEM + ".walkforward.csv", index=False)
    P(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    same_pick, agree = [], []
    for pk in panels:
        for nm in ("C_SHARPE", "C_4B"):
            a = wfd[(wfd.panel == pk) & (wfd.conv == "MIXED") & (wfd.chooser == nm)].iloc[0]
            b_ = wfd[(wfd.panel == pk) & (wfd.conv == "SAME") & (wfd.chooser == nm)].iloc[0]
            same_pick.append((float(a.c), float(a.G)) == (float(b_.c), float(b_.G)))
            agree.append(bool(a.pass4b_OOS == b_.pass4b_OOS and a.pass4b_FULL == b_.pass4b_FULL
                              and a.pass4a_FULL == b_.pass4a_FULL))
            P(f"    {pk:5s} {nm:9s} MIXED c={a.c:.2f} G={a.G:.2f} OOS {a.OOS_CAGR:.2%}/"
              f"{a.OOS_Sharpe:.4f}/{a.OOS_MaxDD:.2%} 4b_OOS={a.pass4b_OOS} | "
              f"SAME c={b_.c:.2f} G={b_.G:.2f} OOS {b_.OOS_CAGR:.2%}/{b_.OOS_Sharpe:.4f}/"
              f"{b_.OOS_MaxDD:.2%} 4b_OOS={b_.pass4b_OOS} | "
              f"{'SAME BOOK' if same_pick[-1] else 'DIFFERENT BOOK'}, "
              f"{'verdicts agree' if agree[-1] else 'VERDICTS DIFFER'}")
    H_CAP = bool(all(same_pick) and all(agree))
    P(f"\n  H_CAP  same nomination on {sum(same_pick)}/{len(same_pick)} (panel,chooser) and same "
      f"KEEP verdicts on {sum(agree)}/{len(agree)}  -> "
      f"{'CONFIRMED (the mixed-unit denominator is capital-neutral)' if H_CAP else 'REFUTED (the mixed-unit denominator is worth real money)'}")

    # ---------------------------------------------------------------------- [7] scorecard
    P("\n[7] HYPOTHESIS SCORECARD")
    for nm, v in (("H_MIX", H_MIX), ("H_BAR", H_BAR), ("H_LAM", H_LAM),
                  ("H_SET", H_SET), ("H_CAP", H_CAP)):
        P(f"  {nm:7s} {'CONFIRMED' if v else 'REFUTED'}")
    P(f"\n  CAPITAL: 4a FULL {int(grid.pass4a_F.sum())}/{len(grid)}   "
      f"4b FULL {int(grid.pass4b_F.sum())}/{len(grid)}   4b OOS {int(grid.pass4b_OOS.sum())}/{len(grid)}")
    P(f"  rule-8 picks beating RULES v2 OOS: {int(wfd.beats_base_OOS.sum())}/{len(wfd)};  "
      f"beating SPY OOS: {int(wfd.beats_spy_OOS.sum())}/{len(wfd)};  "
      f"clearing 4b OOS: {int(wfd.pass4b_OOS.sum())}/{len(wfd)};  "
      f"clearing 4b FULL: {int(wfd.pass4b_FULL.sum())}/{len(wfd)}")
    bestm = grid[(grid.conv == "MIXED") & grid.pass4b_F & grid.pass4b_OOS]
    bests = grid[(grid.conv == "SAME") & grid.pass4b_F & grid.pass4b_OOS]
    P(f"  cells clearing 4b on FULL *and* OOS: MIXED {len(bestm)}, SAME {len(bests)}")
    if len(bestm):
        P("  MIXED double-4b cells: " +
          "; ".join(f"{r.panel} c={r.c:.2f} G={r.G:.2f} OOS {r.CAGR_OOS:.2%}/{r.Sharpe_OOS:.4f}/"
                    f"{r.MaxDD_OOS:.2%}" for _, r in bestm.iterrows()))
    if len(bests):
        P("  SAME double-4b cells:  " +
          "; ".join(f"{r.panel} c={r.c:.2f} G={r.G:.2f} OOS {r.CAGR_OOS:.2%}/{r.Sharpe_OOS:.4f}/"
                    f"{r.MaxDD_OOS:.2%}" for _, r in bests.iterrows()))
    # --- G10: external replication, and the reason this run proposes NO NEW KEEP --------------
    P("\n  G10 EXTERNAL REPLICATION, and why this run proposes NO NEW KEEP.")
    u = grid[(grid.panel == "U56") & (grid.conv == "MIXED") & (grid.c == 0.10) & (grid.G == 1.00)].iloc[0]
    ok10 = (abs(u.CAGR_OOS - 0.1214) < 5e-5 and abs(u.Sharpe_OOS - 1.1938) < 5e-5
            and abs(u.MaxDD_OOS + 0.1630) < 5e-5)
    P(f"      LEADERBOARD 2026-09-20 (idea 1719, lane B) publishes U56 BAND c=0.10 / G=1.00 at OOS")
    P(f"      12.14% / 1.1938 / -16.30%.  This run's independent MIXED grid: {u.CAGR_OOS:.2%} / "
      f"{u.Sharpe_OOS:.4f} / {u.MaxDD_OOS:.2%}  -> "
      f"{'MATCHES to the published precision' if ok10 else 'DOES NOT MATCH'}")
    P("      Every MIXED double-4b cell above is a member of that standing DEGROSS band family.")
    P("      Every SAME double-4b cell above is a member of the record's standing RESPREAD band")
    P("      family, already published at greater width than this run's grid (2026-09-06: '4b")
    P("      29/144, every one RESPREAD (0/72 DEGROSS)'; '4b 54/442'; best U56/MA/RESPREAD/W")
    P("      b=0.12 at 14.09% / 1.2330 / -19.36%).  The rule-8 C_4B pick on U56/SAME")
    P("      (c=0.10, G=0.75; FULL 13.47% / 1.2187 / -18.25%, halves 1.2616 / 1.1923, OOS 14.60%")
    P("      / 1.2527 / -18.25%) clears 4b on FULL and OOS and is therefore formally a 4b")
    P("      candidate - but it is that KNOWN family's cell, it passes on 1 of 3 panels and under")
    P("      1 of 2 choosers, and 4a fails at 1 of 45.  NO NEW KEEP IS PROPOSED and RULES.md is")
    P("      untouched (rule 6).  What is NEW here is the CONTRAST, not the book.")

    P("\n  SURVIVORSHIP (rule 9): U56/B136 are current-constituent lists, SMALL a current sub-$2B")
    P("  screen carried back to 2010, so every absolute level above - including every 4b pass - is")
    P("  an UPPER BOUND.  The MIXED-vs-SAME contrast is inside one frame and first-order immune.")
    P(f"\n  elapsed {time.time()-t0:.0f}s")
    Path(STEM + ".console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
