#!/usr/bin/env python3
"""Idea 391: BACK-FILL THE 153 UNATTRIB BAND ROWS.

Idea 387 audited the record's band lexicon and found that of 284 band-speaking
LEADERBOARD rows, 153 (53.9%) carry NO recoverable instrument cue in their own prose, so
over half the record's band language cannot be read without opening the parent script.
The queue's task, exactly as filed: (i) resolve each of those rows against its PARENT
SCRIPT's construction and rewrite the row to name the instrument, and (ii) re-check
whether any surviving published claim pools NT and MAB.

INSTRUMENTS (idea 387's pre-registered taxonomy, reused verbatim so the two runs speak
one language):
    NT     no-trade / exit RANK buffer -- integer rank slack (sel_band `m`, RANKX `x`,
           RANKE `e`); hold a name until its rank passes n + slack
    MAB    200d MOVING-AVERAGE band WIDTH -- fractional half-width of the hysteresis
           collar around the MA (baseline.band_state `band`)
    SHARE  idea 103's fractional per-name SHARE multiplier, also written `m`
and this run adds the class idea 387's prose classifier had no room for:
    INTERVAL  the row says "band" about a STATISTICAL INTERVAL -- a null band, a
              confidence band, an admissible gross band, a +/-0.03 grid band, a
              drawdown range quoted "(band 8.85pp)".  Not an instrument at all.

THE RESOLVER, fixed priority order, applied to every band-speaking row.  Row-level
evidence outranks parent-level evidence; a construction outranks a mention:
    R4  CONTRAST: the row is explicitly about BOTH instruments ("the two instruments the
        record calls a band").  Such a row is legitimately plural and must never be
        collapsed onto one instrument by a construction rule -> POOLED.
    R3  INTERVAL sense: the band word sits inside an explicit interval phrase ("null
        band", "weak-dominance band", "band 8.85pp") -> INTERVAL.  Ahead of R2 because an
        interval phrase can quote a fraction that R2 would read as a collar half-width.
    R2  ROW-LEVEL DIAL VALUE: a number the row attaches to a band word, read through idea
        387's OWN integrality/range heuristic -- a fractional or percentage half-width in
        (0, 0.60] is MAB, an integer rank slack written as a dial (m=, x=, e=, buffer) is
        NT.  A bare integer beside the word is neither: here it is an idea number.
    R2n ROW NAMES THE CONSTRUCTION: RANKX / RANKE / sel_band / exit buffer (NT) or
        band_state / hysteresis / collar / MA re-entry band / MAB (MAB).  Narrower than
        idea 387's prose cues, whose loose `buffer` and `width` tokens are what pooled
        rows in the first place.
    R2b `BAND` as a named dial in idea 171's GROSS / N / BAND / CADENCE / SLEEVE ladder,
        whose `band` is `above_band(px, b)` -- read once out of that script -> MAB.
    R1  PARENT CONSTRUCTION: the parent script's source cues exactly one instrument
        (idea 387's CUE_NT / CUE_MAB / CUE_SHARE, unchanged) -> that instrument.
    R1c PARENT MENTIONS BOTH, CONSTRUCTS ONE: the collar arithmetic and the rank-buffer
        carry-forward matched as CODE, not prose -> the one it constructs.
    R1b IMPORT CLOSURE: a meta/census script that constructs nothing inherits the
        construction of the scripts it imports (depth 2, imports only).
    R0  otherwise: POOLED where the evidence names both, UNRESOLVED where it names
        neither.  Every UNRESOLVED row is listed in full.
The rule set was refined by reading G_BF's disagreement list (a text classifier, tuned on
text); the protocol's two-parameter budget is spent in [D], on (m, b), not here.

GATES, all run before any new count is read:
    G_REPRO  the prose census re-run on LEADERBOARD.md AS OF idea 387's own commit must
             reproduce its published 284 / 153 / 68 / 48 / 11 / 4 exactly.  Without this
             the back-fill is not back-filling the same object.
    G_CLS    idea 387's classifier gate (five hand-established constructions).
    G_BF     THE RESOLVER'S ERROR RATE, measured not asserted: run the resolver on the
             rows idea 387's PROSE classifier already attributed to a single instrument
             and report agreement.  Disagreements are read out one by one, both ways --
             they are the prose classifier's error rate against the construction.
    G1/G2    fast_backtest vs products/backtester/engine.backtest (returns AND turnover).
    G3a/G3b  sel_band(m=0) nests sel_hard(n); band_state(b=0) nests px > ma200.
    G4       (B136, n=20, g=0.75, anchor, W) reproduces idea 333/384's committed row.
    G4b      the matched NT/MAB grid reproduces idea 387's committed matched.csv.

[C] THE REWRITE.  research/LEADERBOARD.md is rewritten in place with a leading
    `[NT]` / `[MAB]` / `[SHARE]` / `[INTERVAL]` / `[POOLED]` / `[UNRESOLVED]` tag on the
    idea cell of every band-speaking row.  Idempotent (a tagged row is left alone) and
    verified byte-wise: the diff must be tag insertions and nothing else.

[D] THE LIVE LEG, with rule 8.  A census cannot say whether a POOLED claim is WRONG, only
    that it is unreadable.  So every claim that survives the back-fill still pooling the
    two instruments is priced per-instrument on idea 387's matched grid -- one book, one
    anchor, one cadence, one gross, the ONLY moving part being which dial is turned:
        parent   top-n of the v1 composite, vol scaler OFF, among RULES v1 eligible names
        NT arm   sel_band: enter at rank <= n, hold until rank passes n + m
        MAB arm  the `px > ma200` eligibility leg REPLACED by band_state at half-width b
    THE TWO TUNED PARAMETERS, and the only two:  m in {0,5,10,20,40}, b in {0,.03,.06,.12}
    Panel {U56, B136, SMALL439} and cost rung {0, 10, 25} bps are REPORTED axes, not
    choices.  Both KEEP paths at every cell (4a vs live RULES v2 on the same panel, 4b vs
    SPY).  Rule 8: dial chosen on 2008-2016 IS Sharpe at 10 bps, 2017-2026 read ONCE.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so CAGR
levels are optimistic and 4b's CAGR floor is tested in the book's favour.  (2) The
resolver reads TEXT; G_BF is its measured error rate against the construction, not a
proof.  (3) A row whose parent script is a META/census run (it reports a `BAND` dial it
never constructs) is resolvable only through R2, by the value the row quotes.  (4) The
grid in [D] is a deliberate REPRODUCTION of idea 387's leg [C], gated at G4b; its new
content is the per-instrument reading of the pooled claims, not the grid.

Deterministic, standalone.  Reads baseline.py and engine; writes only research/ outputs
and the LEADERBOARD tags.
"""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, band_state                 # noqa
from engine import backtest, metrics, rebalance_mask                                    # noqa

SLUG = "2026-09-07_back-fill-the-153-UNATTRIB-band-rows_C"
OUT = ROOT / "research" / "backtests"
BT = OUT
LB_PATH = ROOT / "research" / "LEADERBOARD.md"
P387 = "2026-09-07_split-the-band-lexicon-in-the-LEADERBOARD_C"
# idea 387's census was taken on the LEADERBOARD as it stood BEFORE its own rows were
# appended, i.e. the parent of the commit that published it (019145c^).  The published
# commit itself reads 291/157/70/48/12/4 — its own seven rows included — so the parent is
# the object, and G_REPRO fails loudly on either if that ever stops being true.
COMMIT_387 = "0123419"
PUB387 = dict(total=284, UNATTRIB=153, NT=68, MAB=48, POOLED=11, OTHER=4)

MAX_VOL, GROSS, FREQ, NFIX = 0.60, 0.75, "W", 20
MS = [0, 5, 10, 20, 40]
BS = [0.00, 0.03, 0.06, 0.12]
COSTS = [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ============================================================ idea 387's classifier, verbatim
CUE_NT = re.compile(
    r"sel_band|no-?trade|no_trade|exit buffer|entry buffer|rank buffer|"
    r"n\s*\+\s*m\b|until (?:its )?rank passes|rank <= n \+|RANKX|RANKE|hold until", re.I)
CUE_MAB = re.compile(
    r"band_state|hysteresis|ma\s*\*\s*\(1\s*[-+]\s*band|"
    r"rolling\(200\)\.mean\(\)\s*\*\s*\(1|200d\s*(?:\+/-|\+-|±)|MA band|band width|"
    r"width of the (?:200|MA)", re.I)
CUE_SHARE = re.compile(
    r"idea 103|share (?:dial|multiplier)|per-name share|share multiplier|"
    r"w\s*\*\s*m\b|weight multiplier", re.I)
PR_NT = re.compile(r"no-?trade band|rank buffer|exit buffer|entry buffer|buffer|"
                   r"\bm\s*=\s*\d+\b|n\s*\+\s*m\b|sel_band|RANKX|RANKE", re.I)
PR_MAB = re.compile(r"200d(?:\s|-)?(?:MA)?\s*band|MA band|band width|hysteresis|"
                    r"\bband\s*[=b]?\s*0?\.\d+|collar|\bwidth\b", re.I)
PR_SHARE = re.compile(r"idea 103|share dial|share multiplier|per-name share", re.I)
PR_OTHER = re.compile(r"admissible (?:gross )?band|gross band|vol(?:atility)? band|"
                      r"confidence band|turnover ratio band|ratio band", re.I)
BANDWORD = re.compile(r"\bband(?:s|ed|ing)?\b|\bbuffer\b|\bno-?trade\b|\bhysteresis\b", re.I)
CAND_COLS = ["m", "band", "b", "e", "x", "nt", "buffer", "width", "band_b", "m_band"]


def classify_source(txt):
    c = set()
    if CUE_NT.search(txt): c.add("NT")
    if CUE_MAB.search(txt): c.add("MAB")
    if CUE_SHARE.search(txt): c.add("SHARE")
    if not c: return "OTHER", c
    if len(c) == 1: return next(iter(c)), c
    return "MIXED", c


def classify_column(col, vals, parent_cls, parent_cues):
    v = pd.to_numeric(vals, errors="coerce").dropna()
    if len(v) == 0: return "OTHER", "no-numeric"
    integral = bool(np.all(np.isclose(v % 1, 0)))
    lo, hi = float(v.min()), float(v.max())
    name = col.lower()
    if name in ("nt", "buffer"): return "NT", "colname"
    if name in ("width", "band_b", "mab"): return "MAB", "colname"
    if name in ("band", "b"):
        if not integral and 0.0 <= lo and hi <= 0.60: return "MAB", "band-frac"
        if integral and hi > 1: return "NT", "band-int"
        return "OTHER", "band-other"
    if name in ("e", "x") and integral and hi <= 200:
        if parent_cls in ("NT", "MIXED") and "NT" in parent_cues: return "NT", "rank-buf"
        return "OTHER", "e-x-noparent"
    if name == "m":
        if integral and hi >= 2: return "NT", "m-int"
        if not integral: return "SHARE", "m-frac"
        if parent_cls == "NT": return "NT", "m-parent"
        if parent_cls == "SHARE": return "SHARE", "m-parent"
        return "OTHER", "m-degenerate"
    return "OTHER", "unmatched"


def prose_class(ln):
    """idea 387's [A3] row classifier, verbatim."""
    c = set()
    if PR_OTHER.search(ln): c.add("OTHER")
    if PR_NT.search(ln): c.add("NT")
    if PR_MAB.search(ln): c.add("MAB")
    if PR_SHARE.search(ln): c.add("SHARE")
    inst = c - {"OTHER"}
    cls = ("UNATTRIB" if not c else
           ("OTHER" if not inst else (next(iter(inst)) if len(inst) == 1 else "POOLED")))
    return cls, "+".join(sorted(c)) or "-"


def band_rows(txt):
    """Every band-speaking LEADERBOARD row of a given file text, in file order."""
    out = []
    for i, ln in enumerate(txt.split("\n")):
        if not ln.startswith("|") or ln.startswith("|---") or "| Date |" in ln: continue
        if not BANDWORD.search(ln): continue
        out.append((i, ln))
    return out


# ================================================================== the back-fill resolver
# R3: the band word is a STATISTICAL INTERVAL.  Every alternative names a phrase the record
# actually writes; `band` alone is never enough, and a bare number next to it never is
# either (the record writes "band 8.85pp" for a range and "3% band" for a collar).
INTERVAL = re.compile(
    r"noise[- ]?band|null band|indifference band|weak-?dominance band|confidence band|"
    r"no-content band|admissible (?:gross )?band|gross band|vol(?:atility)? band|depth band|"
    r"phase band|error band|tolerance band|equivalence band|plateau band|margin band|"
    r"ratio band|sampling band|passing band|in-sample band|published bands|band gamma|"
    r"band's own (?:draw|sampling|noise|range|law)|two-sided band|matched-null[^|]{0,14}band|"
    r"band (?:contains|empty|edges?|drift|width of the grid|at every|across|is estimated)|"
    r"non-?empty band|BAND EMPTY|as a band|inside (?:its own|a|the)[^|]{0,20}(?:null|noise|margin|"
    r"no-content|tolerance|confidence|dominance|passing|sampling|draw|phase|error|"
    r"equivalence|plateau|admissible|gross|vol|depth|IS|OOS) band|"
    r"within its own[^|]{0,22}band|outside t[^|]{0,26}band|\(band [0-9.]+ ?(?:pp|x)\)|"
    r"band [0-9.]+-[0-9.]+|band [0-9.]+ ?pp|bands? (?:overlap|averag)|"
    r"band\b[^|]{0,14}\[[0-9.a-z]|reproduces? every published band|"
    r"20-draw|rank bands", re.I)
# R2: a dial VALUE the row itself attaches to a band word, read through idea 387's own
# integrality/range heuristic -- a fractional or percentage half-width is MAB, an integer
# rank slack written as a dial (m=, x=, e=, buffer) is NT.  A bare integer next to the word
# is neither: in this record it is an idea number or a row count.
R2_MAB = [re.compile(p, re.I) for p in (
    r"([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:(?:MA|200d|re-?entry|no-?trade|hysteresis|collar)\s+){0,3}band\b",
    r"(0?\.[0-9]+)\s*band\b",
    r"\bband\s*(?:=|@|to|of|at)?\s*\*{0,2}(0?\.[0-9]+)",
    r"\bband\s*(?:=|@|to|of|at)?\s*\*{0,2}([0-9]+(?:\.[0-9]+)?)\s*%",
    r"\bband([0-9]{1,2})\b",                 # band3 / BAND12: a named MAB book
    r"\bb\s*=\s*(0?\.[0-9]+)",
)]
R2_NT = [re.compile(p, re.I) for p in (
    r"\bm\s*=\s*([0-9]+)\b", r"\b[xe]\s*=\s*([0-9]+)\b",
    r"\bbuffer\s*(?:=|of|at)?\s*([0-9]+)\b", r"\bm\s+([0-9]+)(?:\s*/\s*[0-9]+)+",
)]
# R2b: `BAND` as a NAMED DIAL in idea 171's ladder vocabulary (GROSS / N / BAND / CADENCE /
# SLEEVE).  That ladder's `band` is `above_band(px, b)` -- enter above MA*(1+b), exit below
# MA*(1-b) -- read once out of 2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C
# and therefore MAB by construction, wherever the enumeration appears.
# R2n: the row names a CONSTRUCTION, not merely a band word.  Narrower than idea 387's
# PR_NT/PR_MAB (whose loose `buffer` and `width` tokens are what pool rows in the first
# place): only the names of the two constructions count here.
NAME_NT = re.compile(r"RANKX|RANKE|sel_band|no-?trade band|exit buffer|entry buffer|"
                     r"rank buffer", re.I)
NAME_MAB = re.compile(r"band_state|hysteresis|collar|MA re-?entry band|MA band|"
                      r"200d[^|]{0,8}band|\bMAB\b", re.I)
DIALVOCAB = re.compile(
    r"\bBAND\b(?=[^|]{0,90}\b(?:GROSS|SLEEVE|CADENCE|COUNT)\b[^|]{0,90}"
    r"\b(?:GROSS|SLEEVE|CADENCE|COUNT|N)\b)|"
    r"\b(?:GROSS|SLEEVE|CADENCE|COUNT)\b[^|]{0,60}\b(?:GROSS|SLEEVE|CADENCE|COUNT|N)\b"
    r"(?=[^|]{0,90}\bBAND\b)")


def r2_value_class(ln):
    cls, why = set(), []
    for rx in R2_MAB:
        for m in rx.finditer(ln):
            v = float(m.group(1))
            pct = ("%" in m.group(0)) or rx.pattern.startswith(r"\bband([0-9]")
            if pct and v >= 1: v /= 100.0
            if 0.0 < v <= 0.60:
                cls.add("MAB"); why.append(f"{m.group(0).strip()[:14]}->MAB")
    for rx in R2_NT:
        for m in rx.finditer(ln):
            if float(m.group(1)) >= 2:
                cls.add("NT"); why.append(f"{m.group(0).strip()[:14]}->NT")
    if len(cls) == 1: return next(iter(cls)), ",".join(why)
    if len(cls) > 1: return "POOLED", ",".join(why)
    return None, ""


SCRIPTRE = re.compile(r"([A-Za-z0-9_\-./]+\.py)")
STEMRE = re.compile(r"2026-\d\d-\d\d_[A-Za-z0-9_\-]+")
IMPLINE = re.compile(r".*(?:_STEM\s*=|spec_from_file_location|module_from_spec|import_module).*")


def parent_stem(ln, src):
    m = SCRIPTRE.findall(ln)
    if not m: return None
    nm = Path(m[-1]).name[:-3]
    if nm in src: return nm
    cand = [s for s in src if s.startswith(nm)]      # LEADERBOARD truncates long names
    return cand[0] if len(cand) == 1 else None


# R4: the row is EXPLICITLY about both instruments (idea 384/387's own contrast rows).
# Such a row is not unattributable and not mis-attributed -- it is legitimately plural, and
# must never be collapsed onto one instrument by a construction rule.
CONTRAST = re.compile(r"two instruments|both instruments|\bNT\b[^|]{0,14}\bMAB\b|"
                      r"\bMAB\b[^|]{0,14}\bNT\b|no-?trade band[^|]{0,44}MA band|"
                      r"pools? (?:NT|both)|band lexicon", re.I)
# R1c: a parent that MENTIONS both instruments but CONSTRUCTS only one.  These two regexes
# match code, not prose -- the collar arithmetic and the rank-buffer carry-forward.
CONSTRUCT_MAB = re.compile(r"band_state\s*\(|ma\s*\*\s*\(1\s*[-+]\s*(?:band|b)\b|"
                           r"rolling\(200\)\.mean\(\)\s*\*\s*\(1|\*\s*\(1\s*[-+]\s*band\)")
CONSTRUCT_NT = re.compile(r"def (?:sel_band|band_weights|buffer_weights)|sel_band\s*\(|"
                          r"\b(?:n|N|NPOS|npos|NFIX|nfix|k)\s*\+\s*(?:m|x|e|buf)\b|"
                          r"rank passes|ranked worse than[^\n]{0,20}\+\s*m|"
                          r"held\s*=\s*\[j for j in held")


def construct_class(stem, src):
    t = src.get(stem, "")
    a, b = bool(CONSTRUCT_MAB.search(t)), bool(CONSTRUCT_NT.search(t))
    if a and not b: return "MAB"
    if b and not a: return "NT"
    return None


def imported_stems(stem, src):
    """Committed scripts import their parents by stem (spec_from_file_location / *_STEM)."""
    out = set()
    for ln in src.get(stem, "").split("\n"):
        if IMPLINE.match(ln):
            for c in STEMRE.findall(ln):
                if c in src and c != stem: out.add(c)
    return out


def closure_class(stem, src, depth=2):
    """R1b: the construction a meta/census script INHERITS from the scripts it imports."""
    seen, frontier = {stem}, [stem]
    for _ in range(depth):
        nxt = []
        for s in frontier:
            for c in imported_stems(s, src):
                if c not in seen: seen.add(c); nxt.append(c)
        frontier = nxt
    cues = set()
    for s in seen:
        cues |= classify_source(src[s])[1]
    if not cues: return "OTHER", cues
    if len(cues) == 1: return next(iter(cues)), cues
    return "MIXED", cues


def resolve(ln, src):
    """The pre-registered resolver, priority R4 > R3 > R2 > R2b > R1 > R1c > R1b > R0."""
    stem = parent_stem(ln, src)
    pcls, pcues = classify_source(src.get(stem, "")) if stem else ("OTHER", set())
    cm = CONTRAST.search(ln)
    if cm:
        return "POOLED", "R4", "row is explicitly about both: " + cm.group(0)[:24]
    im = INTERVAL.search(ln)
    if im:
        return "INTERVAL", "R3", im.group(0)[:40]
    v2c, v2why = r2_value_class(ln)
    if v2c in ("NT", "MAB"):
        return v2c, "R2", v2why[:56]
    nn, nm = bool(NAME_NT.search(ln)), bool(NAME_MAB.search(ln))
    if nn != nm:
        return ("NT" if nn else "MAB"), "R2n", "row names the construction"
    if DIALVOCAB.search(ln):
        return "MAB", "R2b", "BAND in idea 171's GROSS/N/BAND/CADENCE/SLEEVE ladder"
    if v2c == "POOLED":
        return "POOLED", "R2", v2why[:56]
    if pcls in ("NT", "MAB", "SHARE"):
        return pcls, "R1", f"parent {stem[:34] if stem else '-'}"
    cc = construct_class(stem, src) if stem else None
    if pcls == "MIXED" and cc:
        return cc, "R1c", f"parent mentions {'+'.join(sorted(pcues))}, constructs {cc}"
    ccls, ccues = closure_class(stem, src) if stem else ("OTHER", set())
    if ccls in ("NT", "MAB", "SHARE"):
        return ccls, "R1b", f"imports {'+'.join(sorted(ccues))}"
    if pcls == "MIXED" or ccls == "MIXED":
        return "POOLED", "R0", f"cues {'+'.join(sorted(pcues | ccues))}"
    return "UNRESOLVED", "R0", f"parent {pcls}"


def final_class(res, prose):
    """The class the row is TAGGED with: the resolver where it decides, idea 387's prose
    attribution where the resolver abstains and the prose does decide."""
    if res in ("NT", "MAB", "SHARE", "INTERVAL"): return res, "resolver"
    if prose in ("NT", "MAB", "SHARE"): return prose, "prose"
    return res, "resolver"


def read_sources():
    return {p.stem: p.read_text(errors="ignore") for p in sorted(BT.glob("*.py"))}


def gate_classifier(src):
    ok = tot = 0
    checks = [
        ("sel_band: hold until its rank passes n + m", "m", pd.Series([0, 5, 20]), "NT"),
        ("band_state hysteresis around the 200d MA", "band", pd.Series([0.0, .03, .12]), "MAB"),
        ("idea 103's share multiplier: w * m per name", "m", pd.Series([0.5, 1.0, 1.5]), "SHARE"),
        ("RANKE entry buffer e", "e", pd.Series([0, 4, 12]), "NT"),
        ("RANKX exit buffer x", "x", pd.Series([0, 40, 80]), "NT"),
    ]
    for txt, col, vals, want in checks:
        cls, cues = classify_source(txt)
        got, why = classify_column(col, vals, cls, cues)
        assert got == want, (txt, col, want, got)
        ok += 1; tot += 1
    P(f"    G_CLS PASS: {ok}/{tot} hand-established constructions reproduced")


def gate_repro():
    """G_REPRO: idea 387's published census, re-derived from the file it read."""
    txt = subprocess.run(["git", "show", f"{COMMIT_387}:research/LEADERBOARD.md"],
                         cwd=str(ROOT), capture_output=True, text=True, check=True).stdout
    rows = band_rows(txt)
    cls = pd.Series([prose_class(ln)[0] for _, ln in rows])
    got = dict(total=len(rows), **{k: int((cls == k).sum())
                                   for k in ("UNATTRIB", "NT", "MAB", "POOLED", "OTHER")})
    P(f"    G_REPRO at {COMMIT_387}: {got}")
    P(f"    published    : {PUB387}")
    assert got == PUB387, (got, PUB387)
    P("    G_REPRO PASS — the object being back-filled is idea 387's own census")
    return txt


# ============================================================ idea 387's leg [C], verbatim
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    return px[[c for c in px.columns if c not in bad]]


def rank_frame(px, b=None):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    gate = above if b is None else band_state(px, b)
    return s.where(gate & (vol20 < MAX_VOL) & px.notna()).rank(axis=1, ascending=False)


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, freq=FREQ):
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held, last = [], np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap: held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs = set(held)
                for j in order:
                    if len(held) >= cap: break
                    if r[j] != r[j]: break
                    if j not in hs: held.append(j); hs.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols)); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel, gross=GROSS):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1), index=idx),
            pd.Series(turn, index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def stats(gross_r, turn, bps, start):
    r = (gross_r - turn * bps / 1e4).loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mo, mi = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"])


def keeps(s, v2, spy):
    a = s["H1"] > v2["H1"] and s["H2"] > v2["H2"] and s["MaxDD"] >= v2["MaxDD"]
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -0.60 * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb)


TAGRE = re.compile(r"^(\s*)\[(?:NT|MAB|SHARE|INTERVAL|POOLED|UNRESOLVED)\] ")


def rewrite_leaderboard(res):
    """[C] tag every band-speaking row's idea cell; idempotent; byte-verified.

    The tag is inserted after the idea cell's leading whitespace and nothing else is
    touched, so removing the tag from every rewritten line must reproduce that line
    byte for byte.  That is asserted per line, not by a whole-file regex."""
    txt = LB_PATH.read_text()
    lines = txt.split("\n")
    tagged = already = 0
    for _, r in res.iterrows():
        i, cls = int(r["line"]), r["cls"]
        old = lines[i]
        cells = old.split("|")
        if len(cells) < 4: continue
        if TAGRE.match(cells[2]):
            already += 1
            continue
        cells[2] = re.sub(r"^(\s*)", r"\g<1>[" + cls + "] ", cells[2], count=1)
        new_line = "|".join(cells)
        assert TAGRE.sub(r"\g<1>", new_line.split("|")[2], count=1) == old.split("|")[2]
        assert new_line.replace(f"[{cls}] ", "", 1) == old
        lines[i] = new_line
        tagged += 1
    new = "\n".join(lines)
    LB_PATH.write_text(new)
    return tagged, already, len(new) - len(txt)


def main():
    P(f"# {SLUG}")
    P(f"# pandas {pd.__version__}  numpy {np.__version__}")

    src = read_sources()
    P(f"\n[0] GATES on the census object ({len(src)} committed scripts)")
    gate_classifier(src)
    txt387 = gate_repro()

    # ------------------------------------------------------------- G_BF, before any count
    P("\n[G_BF] RESOLVER ERROR RATE against idea 387's prose-attributed rows")
    rows387 = band_rows(txt387)
    bf = []
    for i, ln in rows387:
        pc, pcue = prose_class(ln)
        rc, rule, why = resolve(ln, src)
        bf.append(dict(line=i, prose=pc, res=rc, rule=rule, why=why, raw=ln))
    bf = pd.DataFrame(bf)
    att = bf[bf.prose.isin(["NT", "MAB", "SHARE"])]
    agree = int((att.prose == att.res).sum())
    nab = att[~att.res.isin(["POOLED", "UNRESOLVED"])]
    nagree = int((nab.prose == nab.res).sum())
    P(f"    {len(att)} rows idea 387's prose classifier attributed to ONE instrument.")
    P(f"    The resolver ABSTAINS (POOLED/UNRESOLVED) on {len(att)-len(nab)} of them; on "
      f"the {len(nab)} where it commits it agrees with the prose on {nagree} "
      f"({nagree/max(len(nab),1):.1%}).  Strict agreement over all {len(att)}: "
      f"{agree} ({agree/len(att):.1%}).")
    P(f"    disagreement table (prose -> resolver):")
    dis = att[att.prose != att.res]
    if len(dis):
        P("      " + dis.groupby(["prose", "res"]).size().to_string().replace("\n", "\n      "))
        for _, r in dis.iterrows():
            cell = r.raw.split("|")[2].strip()[:88]
            P(f"      * {r.prose:5s} -> {r.res:10s} [{r.rule}] {r.why[:34]:34s} | {cell}")
    else:
        P("      none")

    # ------------------------------------------------------------------ [A] the back-fill
    P("\n[A] BACK-FILL — idea 387's 284 rows, resolved against parent construction")
    P("    before (idea 387's prose classifier):")
    P("      " + bf.prose.value_counts().to_string().replace("\n", "\n      "))
    un = bf[bf.prose == "UNATTRIB"]
    P(f"    after, on the {len(un)} UNATTRIB rows only:")
    P("      " + un.res.value_counts().to_string().replace("\n", "\n      "))
    P("      by rule: " + un.rule.value_counts().to_string().replace("\n", " | "))
    P("    after, all 284 rows:")
    P("      " + bf.res.value_counts().to_string().replace("\n", "\n      "))
    nres = int((un.res != "UNRESOLVED").sum())
    P(f"    RESOLVED {nres} of {len(un)} ({nres/len(un):.1%}) previously-unattributable rows")

    P("\n    the rows the resolver CANNOT place (the irreducible residue):")
    for _, r in un[un.res == "UNRESOLVED"].iterrows():
        cell = r.raw.split("|")[2].strip()[:96]
        P(f"      * {r.why[:22]:22s} | {cell}")

    P("\n    FINAL class = the resolver where it commits, idea 387's prose attribution "
      "where it abstains:")
    fin = [final_class(r.res, r.prose) for _, r in bf.iterrows()]
    bf["final"] = [f for f, _ in fin]
    bf["src_of_class"] = [s for _, s in fin]
    P("      " + bf["final"].value_counts().to_string().replace("\n", "\n      "))

    # ------------------------------------------------- [B] does any claim still pool?
    P("\n[B] POOLING RE-CHECK — published claims that still speak of BOTH instruments")
    pooled = bf[bf["final"] == "POOLED"]
    P(f"    {len(pooled)} of {len(bf)} band-speaking rows (idea 387 published 11 POOLED "
      f"on prose alone)")
    for _, r in pooled.iterrows():
        cell = r.raw.split("|")[2].strip()[:104]
        P(f"      * [{r.rule}] {r.why[:30]:30s} | {cell}")
    inst = bf[bf["final"].isin(["NT", "MAB", "SHARE"])].copy()
    inst["stem"] = [parent_stem(x, src) for x in inst.raw]
    inst2 = inst[inst["final"] != "INTERVAL"]
    spanning = inst2.groupby("stem")["final"].nunique()
    spanning = spanning[spanning >= 2]
    P(f"\n    scripts whose OWN LEADERBOARD rows span more than one instrument: "
      f"{len(spanning)} of {inst2.stem.nunique()}")
    for s in spanning.index:
        got = inst2[inst2.stem == s]["final"].value_counts().to_dict()
        P(f"      * {str(s)[:62]:62s} {got}")

    bf_out = bf.drop(columns=["raw"]).copy()
    bf_out["idea"] = [r.split("|")[2].strip()[:120] for r in bf.raw]
    bf_out.to_csv(OUT / f"{SLUG}.backfill_387rows.csv", index=False)

    # ------------------------------------- [C] rewrite the LIVE LEADERBOARD in place
    if "--census-only" in sys.argv:            # development switch; the committed run is full
        P("\n[--census-only] stopping before the rewrite and the grid")
        return

    P("\n[C] REWRITE — tagging every band-speaking row of the CURRENT LEADERBOARD.md")
    cur = LB_PATH.read_text()
    rows_now = band_rows(cur)
    live = []
    for i, ln in rows_now:
        pc, _ = prose_class(ln)
        rc, rule, why = resolve(ln, src)
        fc, fs = final_class(rc, pc)
        live.append(dict(line=i, prose=pc, res=rc, cls=fc, src_of_class=fs,
                         rule=rule, why=why, raw=ln))
    live = pd.DataFrame(live)
    P(f"    {len(live)} band-speaking rows in the current file "
      f"(idea 387 read {PUB387['total']}; the record has grown since)")
    P("      " + live.cls.value_counts().to_string().replace("\n", "\n      "))
    tagged, already, dbytes = rewrite_leaderboard(live)
    P(f"    tagged {tagged} rows, {already} already carried a tag, +{dbytes} bytes")
    after = LB_PATH.read_text().split("\n")
    before = cur.split("\n")
    assert len(after) == len(before), "rewrite changed the line count"
    changed = [i for i in range(len(before)) if after[i] != before[i]]
    ok = all(re.sub(r"\[(?:NT|MAB|SHARE|INTERVAL|POOLED|UNRESOLVED)\] ", "",
                    after[i], count=1) == before[i] for i in changed)
    P(f"    BYTE CHECK: {len(changed)} lines changed, and removing one tag from each "
      f"reproduces the original line exactly: {ok}")
    assert ok and len(changed) == tagged, "rewrite changed something other than the tag"
    live_out = live.drop(columns=["raw"]).copy()
    live_out["idea"] = [r.split("|")[2].strip()[:120] for r in live.raw]
    live_out.to_csv(OUT / f"{SLUG}.backfill_live.csv", index=False)

    # --------------------------------------------------------- [D] the live leg + rule 8
    P("\n[D] MATCHED GRID — pricing the pooled claims per instrument "
      "(idea 387's leg [C] construction, gated)")
    u = load_universe(); bpx = load_universe(broad=True); sm = small_panel()
    panels = [("U56", u), ("B136", bpx), ("SMALL439", sm)]
    for nm, px in panels:
        P(f"    {nm}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")

    P("\n    GATES")
    rk_u = rank_frame(u)
    w_g = weights_from(sel_hard(rk_u, NFIX))
    gr, tn, _ = fast_backtest(u, w_g)
    for bps in (0, 25):
        eng = backtest(u, w_g, cost_bps=bps, freq=FREQ)
        d1 = float((eng["returns"] - (gr - tn * bps / 1e4)).abs().max())
        d2 = float((eng["turnover"] - tn).abs().max())
        P(f"    G1/G2 cost_bps={bps:>2}: |d returns| {d1:.3e}   |d turnover| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    reb = rebalance_mask(u.index, FREQ)
    dh = int((sel_band(u, rk_u, NFIX, 0).loc[reb.values]
              != sel_hard(rk_u, NFIX).fillna(False).loc[reb.values]).values.sum())
    P(f"    G3a sel_band(m=0) vs sel_hard on every rebalance day: {dh} disagreements")
    assert dh == 0
    ma = u.rolling(200).mean()
    defined = ma.notna() & u.notna()
    d3b = int(((band_state(u, 0.0) != (u > ma)) & defined).values.sum())
    P(f"    G3b band_state(b=0) vs px>ma200: {d3b} of {int(defined.values.sum())} cells")
    assert d3b / max(int(defined.values.sum()), 1) < 1e-4
    rk_b = rank_frame(bpx)
    grb, tnb, _ = fast_backtest(bpx, weights_from(sel_hard(rk_b, NFIX)))
    s_ref = stats(grb, tnb, 10, bpx.index[WARMUP])
    tgt = dict(CAGR=0.12992958836952506, Sharpe=0.9431848997615343,
               MaxDD=-0.2005204833110832, H1=1.1047866702854354,
               H2=0.8025166021122436, OOS_Sharpe=0.8836022780725372)
    dmax = max(abs(s_ref[k] - v) for k, v in tgt.items())
    P(f"    G4 (B136,n=20,g=0.75,anchor,W) vs idea 333/384's committed row: "
      f"max |d| {dmax:.3e}")
    assert dmax < 1e-9

    comp, grid = {}, []
    for nm, px in panels:
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        h = len(spy) // 2
        sp = dict(CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                  MaxDD=metrics(spy)["MaxDD"], H1=metrics(spy.iloc[:h])["Sharpe"],
                  H2=metrics(spy.iloc[h:])["Sharpe"],
                  OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                  OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                  OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
        v2r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"]
        v2 = stats(v2r, pd.Series(0.0, index=px.index), 0, start)
        comp[nm] = (sp, v2)
        P(f"\n    {nm} comparands @10bps:")
        P(f"      SPY      CAGR {sp['CAGR']:.2%} Sharpe {sp['Sharpe']:.3f} "
          f"MaxDD {sp['MaxDD']:.2%} H1/H2 {sp['H1']:.3f}/{sp['H2']:.3f} "
          f"OOS {sp['OOS_Sharpe']:.3f}")
        P(f"      RULES v2 CAGR {v2['CAGR']:.2%} Sharpe {v2['Sharpe']:.3f} "
          f"MaxDD {v2['MaxDD']:.2%} H1/H2 {v2['H1']:.3f}/{v2['H2']:.3f} "
          f"OOS {v2['OOS_Sharpe']:.3f}")

        rk_nt = rank_frame(px, b=None)
        cells = [("NT", float(m), sel_band(px, rk_nt, NFIX, m)) for m in MS]
        for bw in BS:
            rkb = rank_frame(px, b=bw)
            cells.append(("MAB", float(bw), sel_hard(rkb, NFIX).fillna(False)))
        for arm, dial, sel in cells:
            g_r, t_r, nmz = fast_backtest(px, weights_from(sel))
            for bps in COSTS:
                s = stats(g_r, t_r, bps, start)
                a, b4, fb = keeps(s, v2, sp)
                grid.append(dict(panel=nm, arm=arm, dial=dial, bps=bps,
                                 turn=float(t_r.loc[start:].sum() /
                                            ((len(t_r.loc[start:])) / 252)),
                                 names=float(nmz.loc[start:].mean()),
                                 keep4a=a, keep4b=b4, first_fail=fb, **s))
    grid = pd.DataFrame(grid)
    grid.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    # G4b: reproduce idea 387's committed matched.csv
    ref = pd.read_csv(OUT / f"{P387}.matched.csv")
    g10 = grid[grid.bps == 10]
    dd = []
    for _, r in ref.iterrows():
        cell = g10[(g10.panel == r.panel) & (g10.arm == r.arm) &
                   (np.isclose(g10.dial, r.dial))]
        if cell.empty: continue
        dd.append(abs(float(cell.iloc[0]["Sharpe"]) - r["Sharpe"]))
        dd.append(abs(float(cell.iloc[0]["MaxDD"]) - r["MaxDD"]))
    P(f"\n    G4b vs idea 387's committed matched.csv: max |d| {max(dd):.3e} "
      f"over {len(dd)} statistics ({len(ref)} cells)")
    assert max(dd) < 1e-9

    P("\n[D1] KEEP PATHS over all cells")
    for bps in COSTS:
        gb = grid[grid.bps == bps]
        P(f"    @{bps:>2} bps: 4a {int(gb.keep4a.sum())}/{len(gb)}, "
          f"4b {int(gb.keep4b.sum())}/{len(gb)}"
          + (f"  passers: " + ", ".join(f"{r.panel}/{r.arm}{r.dial:g}"
                                        for _, r in gb[gb.keep4b].iterrows())
             if gb.keep4b.any() else ""))
    fails = grid[(grid.bps == 10) & (~grid.keep4b)].first_fail.str.split(",").explode()
    P(f"    first-failing 4b bars @10 bps: "
      + ", ".join(f"{k} {v}" for k, v in fails.value_counts().items()))

    P("\n[D2] THE POOLED CLAIMS, priced per instrument @10 bps")
    P(f"    {'panel':9s} {'stat':12s} {'NT ladder':>26s} {'MAB ladder':>26s}  agree?")
    per = []
    for nm, _ in panels:
        g = grid[(grid.panel == nm) & (grid.bps == 10)]
        anch = g[(g.arm == "NT") & (g.dial == 0)].iloc[0]
        for stat, fmt, scale in (("MaxDD", "{:+.0f}bp", 1e4), ("Sharpe", "{:+.3f}", 1),
                                 ("CAGR", "{:+.2f}pp", 100), ("turn", "{:+.2f}/yr", 1)):
            row = {}
            for arm in ("NT", "MAB"):
                d = g[(g.arm == arm) & (g.dial > 0)]
                row[arm] = [ (float(r[stat]) - float(anch[stat])) * scale
                             for _, r in d.iterrows() ]
            sn = np.sign(np.median(row["NT"])); sm_ = np.sign(np.median(row["MAB"]))
            per.append(dict(panel=nm, stat=stat, nt_med=float(np.median(row["NT"])),
                            mab_med=float(np.median(row["MAB"])),
                            nt_pos=int(sum(x > 0 for x in row["NT"])), nt_n=len(row["NT"]),
                            mab_pos=int(sum(x > 0 for x in row["MAB"])), mab_n=len(row["MAB"]),
                            same_sign=bool(sn == sm_)))
            P(f"    {nm:9s} {stat:12s} "
              f"{fmt.format(np.median(row['NT'])):>12s} ({sum(x>0 for x in row['NT'])}/{len(row['NT'])} +) "
              f"{fmt.format(np.median(row['MAB'])):>12s} ({sum(x>0 for x in row['MAB'])}/{len(row['MAB'])} +) "
              f"  {'SAME' if sn == sm_ else 'OPPOSITE'}")
    per = pd.DataFrame(per)
    per.to_csv(OUT / f"{SLUG}.per_instrument.csv", index=False)
    agree = int(per.same_sign.sum())
    P(f"    the two instruments move the SAME statistic the SAME way in {agree} of "
      f"{len(per)} (panel x statistic) cells")

    P("\n[D3] RULE 8 WALK-FORWARD — dial chosen on <=2016 IS Sharpe @10 bps, "
      "2017-2026 read once")
    wf = []
    for nm, px in panels:
        sp, v2 = comp[nm]
        g = grid[(grid.panel == nm) & (grid.bps == 10)]
        anch = g[(g.arm == "NT") & (g.dial == 0)].iloc[0]
        for arm in ("NT", "MAB"):
            d = g[g.arm == arm]
            pick = d.loc[d.IS_Sharpe.idxmax()]
            wf.append(dict(panel=nm, arm=arm, pick=float(pick.dial),
                           OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                           OOS_MaxDD=float(pick.OOS_MaxDD),
                           anchor_OOS=float(anch.OOS_Sharpe),
                           best_OOS=float(d.OOS_Sharpe.max()),
                           regret=float(d.OOS_Sharpe.max() - pick.OOS_Sharpe),
                           spy_OOS=sp["OOS_Sharpe"], v2_OOS=v2["OOS_Sharpe"]))
            P(f"    {nm:9s} {arm:3s} picks {pick.dial:>5g} -> OOS CAGR "
              f"{pick.OOS_CAGR:6.2%} Sharpe {pick.OOS_Sharpe:.4f} MaxDD {pick.OOS_MaxDD:7.2%}"
              f" | anchor {anch.OOS_Sharpe:.4f}  RULES v2 {v2['OOS_Sharpe']:.4f}  "
              f"SPY {sp['OOS_Sharpe']:.4f}  regret {d.OOS_Sharpe.max()-pick.OOS_Sharpe:+.4f}")
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(f"    chooser beats its own anchor OOS in {int((wf.OOS_Sharpe>wf.anchor_OOS).sum())}"
      f"/{len(wf)}, SPY in {int((wf.OOS_Sharpe>wf.spy_OOS).sum())}/{len(wf)}, "
      f"RULES v2 in {int((wf.OOS_Sharpe>wf.v2_OOS).sum())}/{len(wf)}; "
      f"mean regret {wf.regret.mean():+.4f}")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {SLUG}.{{backfill_387rows,backfill_live,grid,per_instrument,walkforward}}.csv")


if __name__ == "__main__":
    main()
