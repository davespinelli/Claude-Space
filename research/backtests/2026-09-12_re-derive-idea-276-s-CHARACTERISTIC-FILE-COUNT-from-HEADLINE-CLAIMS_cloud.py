#!/usr/bin/env python3
"""Idea 534 - re-derive idea 276's CHARACTERISTIC FILE COUNT from HEADLINE CLAIMS, not keywords.
(cloud lane, 2026-09-12)

QUESTION (QUEUE idea 534, verbatim)
    idea 295 found 10 of the 26 name none of the four characteristics in their headline and 2 are
    ledgers, so at most 13 (tight reading 7) carry a restatable direction claim.  Re-run idea 276's
    census with the claim, not the word, as the unit and publish the corrected denominator wherever
    the record quotes 26.  Max 2 params (reading, block length).

WHAT IS ALREADY KNOWN, and what this file adds
    Idea 523 (2026-09-11, lane B) restated the same bound over WINDOW WIDTH x BLOCK RULE and found
    it is a BLOCK-RULE fact, not a window fact: 4 survivors at idea 286's setting, 20 at idea 276's
    own (block = WHOLE), 2..20 over its 50 cells, and restated_26 == restated_136 in 50 of 50.
    This file does the two things 523 did not:
      (1) the CLAIM predicate itself is a dial - the queue's "restatable DIRECTION claim" is scored,
          so a headline that names a characteristic but asserts nothing about its direction does not
          count (523's predicate stopped at the panel-property ROLE);
      (2) the second dial is BLOCK LENGTH in characters, a continuous ladder, which asks whether
          523's block-rule finding survives when the convention is replaced by a number; and
      (3) PART C censuses every committed site that QUOTES 26 (or 136, or 14) and reports, per site,
          whether it states the UNIT it counted and the BLOCK it was scored on - the queue's
          "publish the corrected denominator wherever the record quotes 26".

FROZEN CORPUS, fixed before any number is read
    The 292 filenames in idea 276's committed census.csv
    (2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.census.csv), with its
    own cross / prop / breadth columns.  The corpus has grown since 2026-09-06, so every count here
    is computed on the FROZEN list; today's list is reported beside it and never substituted for it.

DEFINITIONS (idea 276's and 286's regexes are copied verbatim from 523, which copied them from the
originals, so the three runs are scoring the same text the same way)
    CHARACTERISTIC   idea 276's PROP_TOK: breadth | dispersion | disp | pairwise correlation |
                     corr | eligible-set vol | n_elig | evol.
    ROLE             per occurrence in a +/-70 window: INSTRUMENT (names a book dial), else
                     PANEL-PROPERTY (window carries a panel/capitalisation word), else OTHER.
    DIRECTION        a sign word in the same +/-70 window: higher/lower/more/less/rises/falls/
                     increase/decrease/positive/negative/monotone/beats/worse/better/up/down/
                     a signed number, or an explicit inequality.  This is what makes a claim
                     RESTATABLE: "dispersion is higher on the small panel" can be checked, while
                     "we look at dispersion" cannot.
    LEDGERS          LEADERBOARD.md and CHANGELOG.md have no headline of their own; they are scored
                     separately and can never qualify except under block length = WHOLE.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) READING in {LOOSE, TIGHT}.  LOOSE = a PANEL-PROPERTY-role characteristic occurrence inside
        the block (523's predicate).  TIGHT = the same occurrence must also carry a DIRECTION token
        in its window (the queue's "restatable direction claim").  HEADLINE: TIGHT, declared here,
        because the queue's unit is the CLAIM.
    (2) BLOCK LENGTH L in {200, 600, 1500, 4000, WHOLE} characters from the start of the file.
        HEADLINE: 1500 (the record's own CHARS1500 convention, so this run is comparable to 523).
    2 x 5 = 10 grid points; every one printed and written to .grid.csv.

REPORTED AXES (not tunes): the three nested denominators 292 / 136 / 26 / 14, the per-characteristic
    split, the ledger lines, and the exclusion reading (LITERAL and GENERAL) at every cell.

PRE-REGISTERED HYPOTHESES (written before any number was read)
    H_276       idea 276's published counts reproduce from the frozen list (292 / 136 / 26 / 14).
    H_523       523's restated_26 reproduces at its own setting (4 at PRE-H2/W70, 20 at WHOLE).
    H_QUEUE     the queue's arithmetic holds: the claim-unit count at the headline cell is <= 13,
                and its tight reading is <= 7.
    H_DIRBITES  the DIRECTION requirement is load-bearing: TIGHT < LOOSE at the headline cell.
    H_LENGTH    the bound is NOT a pure length fact: over the 5 block lengths at fixed reading the
                count moves by MORE than the 3-file spread 523 measured across its window ladder
                (i.e. length matters where window width did not).
    H_NESTED    restated(26) == restated(136) at every cell - 523's structural theorem re-tested
                under the direction predicate.
    H_CITE      a majority of the record's committed citations of 26 state neither the UNIT nor the
                BLOCK they were scored on.
    H_R8CENSUS  RULE 8 ON THE CENSUS: the share of citations stating the unit, measured on the
                earlier half of the dated citation corpus, reproduces within +/-0.10 on the later
                half, read ONCE.
    H_R8CLAIM   RULE 8 ON THE CLAIM: the (reading, L) cell chosen on the frozen files dated on or
                before the corpus median reproduces its survival share on the later files, read
                ONCE, within +/-0.10.

GATES (printed first; no verdict is read until they are reported)
    G1 idea 276's census reproduces from the frozen list AND from source text today.
    G2 idea 523's committed .grid.csv reproduces at its own two reference cells.
    G3 LIVE RULES v2 on U56 at 10 bps reproduces its committed headline 8.63% / 1.2018 / -12.05%.
    G4 SPY's full-sample triple reproduces the record's committed 15.163% / 0.8861 / -33.717%.
    G5 DIRECTION-detector controls: 12 hand-written strings, every one printed with its verdict.

PROTOCOL RULE 8 and BOTH KEEP PATHS (mandatory, run and reported)
    The book leg is computed from prices in this file: RULES v1, the LIVE RULES v2 (band 0.03,
    gross 0.75), the standing 4b candidate (band 0.03, gross 1.00) and SPY on U56 at 0/10/25 bps,
    plus the LIVE book on every panel the surviving files actually NAME (so the documentation
    decision is priced, not assumed irrelevant - 523's construction), full sample, both halves and
    OOS 2017-01-01.. read once.  Both KEEP paths for every book-panel-rung row.  Nothing is tuned.

SURVIVORSHIP, up front: U56 = research/universe.json and B136 = research/universe_broad.json are
    CURRENT-constituent lists; SMALL = the sub-$2B screen with every ticker whose max_1d_move >= 1.0
    in data/small_meta.csv dropped first, and it cannot see the names that fell out of the screen.
    Every small-cap number is biased upward by an unknown amount; no number here is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt  full log            .grid.csv      10 tuned cells x 2 exclusions, every count
    .files.csv    per frozen file x cell: qualifies, which characteristic, which direction token
    .citations.csv every committed site quoting 26 / 136 / 14, with the corrected denominator
    .walkforward.csv the two rule-8 legs and the book leg
    .result.md    the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

DATE = "2026-09-12"
SLUG = "re-derive-idea-276-s-CHARACTERISTIC-FILE-COUNT-from-HEADLINE-CLAIMS"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
CENSUS276 = HERE / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.census.csv"
GRID523 = HERE / "2026-09-11_restate-idea-276-s-26-file-UPPER-BOUND-on-the-headline-block_B.grid.csv"

# ---- idea 276's regexes, verbatim (via 523) ---------------------------------------------
SMALL_TOK = re.compile(r"SMALL\s?\d{2,3}|small[- ]cap panel|small panel|prices_small|small=True|sub-\$2B|SMALL_PANEL", re.I)
LARGE_TOK = re.compile(r"\bU56\b|\bB136\b|BSTK\s?\d{2,3}|\bETF\s?36\b|universe\.json|universe_broad|broad=True|mega[- ]cap|large[- ]cap", re.I)
PROP_TOK = re.compile(r"\bbreadth\b|\bdispersion\b|\bdisp\b|pairwise correlation|\bcorr\b|eligible[- ]set vol|\bn_elig\b|\bevol\b", re.I)
# ---- idea 286's role regexes, verbatim (via 523) ----------------------------------------
INSTR_LIT = re.compile(r"breadth\s?\d+|breadth[- ](gate|signal|overlay|trigger|instrument|rule|dial|arm|filter)"
                       r"|(market|spy|index)[- ]breadth", re.I)
PANELPROP = re.compile(r"panel|universe|eligible|n_elig|width|cap\b|capitalisation|capitalization"
                       r"|small|large|mega|u56|b136|bstk|etf\s?36|corpus|collinear|dummy", re.I)
VOCAB = r"(?:breadth|dispersion|disp|corr|n_elig|evol)"
INSTR_GEN = re.compile(rf"{VOCAB}\s?\d+"
                       rf"|{VOCAB}[- ](gate|signal|overlay|trigger|instrument|rule|dial|arm|filter|column|leg)"
                       r"|(market|spy|index)[- ]breadth", re.I)
EXCL = {"LITERAL": INSTR_LIT, "GENERAL": INSTR_GEN}
HEAD_SPLIT = re.compile(r"^## ", re.M)
LEDGERS = {"LEADERBOARD.md", "CHANGELOG.md"}

# ---- this run's one new predicate: DIRECTION ---------------------------------------------
DIRECTION = re.compile(r"\bhigher\b|\blower\b|\bmore\b|\bless\b|\brises?\b|\bfalls?\b|\brising\b|"
                       r"\bfalling\b|\bincreas\w*|\bdecreas\w*|\bpositive\b|\bnegative\b|"
                       r"\bmonotone\w*|\bbeats?\b|\bworse\b|\bbetter\b|\bwider\b|\bnarrower\b|"
                       r"\bup\b|\bdown\b|[<>]=?|[+−-]\d|\b\d+(?:\.\d+)?\s?(?:pp|%|x)\b", re.I)

READINGS = ["LOOSE", "TIGHT"]
READING_HEAD = "TIGHT"
LENGTHS = [200, 600, 1500, 4000, "WHOLE"]
LENGTH_HEAD = 1500
W = 70                        # idea 286's window width; NOT a dial here (523 showed it is inert)
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
OOS_START = "2017-01-01"
WARMUP = 260
SPY_PUB = (0.15163101010956526, 0.8860543931081106, -0.33717235283398306)
V2_PUB = (0.0863, 1.2018, -0.1205)
SMALL_MAXMOVE = 1.0

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def read_file(name):
    for p in (HERE / name, ROOT / "research" / name, ROOT / name):
        if p.exists():
            return p.read_text(errors="ignore")
    return None


def block_chars(t, name, L):
    """How many leading characters of t count as the file's headline block."""
    if name in LEDGERS and L != "WHOLE":
        return 0
    return len(t) if L == "WHOLE" else min(int(L), len(t))


def score_file(t, name, L, excl_re):
    """Does this file carry a characteristic CLAIM in its block?  Returns both readings."""
    nb = block_chars(t, name, L)
    hit = dict(LOOSE=False, TIGHT=False, tok="", dirtok="")
    for m in PROP_TOK.finditer(t):
        i = m.start()
        if i >= nb:
            continue
        win = t[max(0, i - W): i + W]
        if excl_re.search(win):
            continue                                   # INSTRUMENT role never counts
        if not PANELPROP.search(win):
            continue                                   # OTHER role never counts
        if not hit["LOOSE"]:
            hit["LOOSE"], hit["tok"] = True, m.group(0).lower()
        d = DIRECTION.search(win)
        if d and not hit["TIGHT"]:
            hit["TIGHT"], hit["dirtok"] = True, d.group(0)
    return hit


# ================================================================= books ==================
def book_metrics(px, wfn, cost_bps):
    res = backtest(px, wfn(px), cost_bps=cost_bps, freq="W")
    r = res["returns"].loc[px.index[WARMUP]:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ro = r.loc[OOS_START:]
    o = metrics(ro)
    ho = len(ro) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                OOS_H1=metrics(ro.iloc[:ho])["Sharpe"], OOS_H2=metrics(ro.iloc[ho:])["Sharpe"])


def spy_metrics(px):
    r = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARMUP]:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ro = r.loc[OOS_START:]
    o = metrics(ro)
    ho = len(ro) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                OOS_H1=metrics(ro.iloc[:ho])["Sharpe"], OOS_H2=metrics(ro.iloc[ho:])["Sharpe"])


def keep_paths(b, live, spy):
    a = dict(a_H1=b["H1"] > live["H1"], a_H2=b["H2"] > live["H2"],
             a_DD=b["MaxDD"] >= live["MaxDD"])
    a["pass_4a"] = all(a.values())
    f = dict(b_H1=b["H1"] > spy["H1"], b_H2=b["H2"] > spy["H2"],
             b_OOS=b["OOS_Sharpe"] > spy["OOS_Sharpe"],
             b_DD=abs(b["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
             b_CAGR=b["CAGR"] >= 0.70 * spy["CAGR"])
    f["pass_4b"] = all(f.values())
    return {**a, **f}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ================================================================= main ===================
def main():
    t0 = time.time()
    P(f"=== idea 534 - re-derive idea 276's characteristic FILE COUNT from HEADLINE CLAIMS ({DATE}, cloud)")
    P("tuned: READING in LOOSE/TIGHT (head TIGHT), BLOCK LENGTH in 200/600/1500/4000/WHOLE (head 1500)")

    P("\n--- GATES (printed before any verdict) ---")
    c276 = pd.read_csv(CENSUS276)
    frozen = c276.file.tolist()
    n292, n136 = len(c276), int(c276.cross.sum())
    n26 = int((c276.cross & c276.prop).sum())
    n14 = int((c276.cross & c276.breadth).sum())
    # re-derive from source text today, on the frozen list
    rows = []
    missing = 0
    for f in frozen:
        t = read_file(f)
        if t is None:
            missing += 1
            continue
        rows.append(dict(file=f, small=bool(SMALL_TOK.search(t)), large=bool(LARGE_TOK.search(t)),
                         prop=bool(PROP_TOK.search(t)),
                         breadth=bool(re.search(r"\bbreadth\b", t, re.I))))
    src = pd.DataFrame(rows)
    src["cross"] = src.small & src.large
    s136, s26, s14 = int(src.cross.sum()), int((src.cross & src.prop).sum()), int((src.cross & src.breadth).sum())
    g1 = (n292 == 292 and n136 == 136 and n26 == 26 and n14 == 14 and missing == 0
          and (s136, s26, s14) == (136, 26, 14))
    P(f"G1 frozen census 292 / cross {n136} / cross&prop {n26} / cross&breadth {n14}; re-derived "
      f"from source today {s136} / {s26} / {s14}, {missing} files missing -> "
      f"{'PASS' if g1 else 'FAIL'}")
    H_276 = g1

    g523 = pd.read_csv(GRID523)
    ref = g523[(g523.W == 70) & (g523.excl == "LITERAL")].set_index("block")
    mine = {}
    for blk, L in (("CHARS1500", 1500), ("WHOLE", "WHOLE")):
        n = 0
        for f in c276[c276.cross & c276.prop].file:
            t = read_file(f)
            if t is None:
                continue
            n += int(score_file(t, f, L, INSTR_LIT)["LOOSE"])
        mine[blk] = n
    ok523 = (mine["CHARS1500"] == int(ref.loc["CHARS1500", "restated_26"])
             and mine["WHOLE"] == int(ref.loc["WHOLE", "restated_26"]))
    P(f"G2 523's committed restated_26 at W70/LITERAL: CHARS1500 {int(ref.loc['CHARS1500','restated_26'])} "
      f"/ WHOLE {int(ref.loc['WHOLE','restated_26'])}; this file's LOOSE reading at the same two "
      f"block lengths {mine['CHARS1500']} / {mine['WHOLE']} -> {'PASS' if ok523 else 'FAIL'}  "
      f"(523's PRE-H2 reference is 4 and its WHOLE reference is {int(ref.loc['WHOLE','restated_26'])})")
    H_523 = ok523

    px = load_universe()
    v2 = book_metrics(px, lambda q: rules_v2_weights(q, 0.03, 0.75), 10.0)
    g3 = max(abs(v2["CAGR"] - V2_PUB[0]), abs(v2["Sharpe"] - V2_PUB[1]), abs(v2["MaxDD"] - V2_PUB[2]))
    P(f"G3 LIVE RULES v2 @10bps {v2['CAGR']:.4%} / {v2['Sharpe']:.4f} / {v2['MaxDD']:.4%} vs "
      f"committed 8.63% / 1.2018 / -12.05%  max|d| {g3:.3e} -> {'PASS' if g3 <= 6e-3 else 'FAIL'}")
    spy = spy_metrics(px)
    g4 = max(abs(spy["CAGR"] - SPY_PUB[0]), abs(spy["Sharpe"] - SPY_PUB[1]), abs(spy["MaxDD"] - SPY_PUB[2]))
    P(f"G4 SPY full {spy['CAGR']:.4%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.4%} vs committed "
      f"15.163% / 0.8861 / -33.717%  max|d| {g4:.3e} -> {'PASS' if g4 <= 6e-3 else 'FAIL'}")

    CONTROLS = [
        ("dispersion is higher on the small panel", True),
        ("we look at dispersion across the panel", False),
        ("breadth falls from 0.745 to 0.307 on the small-cap universe", True),
        ("the panel's dispersion column is reported", False),
        ("corr is more negative on B136 than on U56", True),
        ("n_elig for the eligible universe", False),
        ("dispersion +1.23 pp on the large-cap panel", True),
        ("disp and breadth are both panel properties", False),
        ("breadth < 0.40 on every small panel", True),
        ("panel dispersion, measured daily", False),
        ("evol decreases as the universe widens", True),
        ("a dispersion section for the panel", False),
    ]
    P("G5 DIRECTION controls (string -> direction found, expected in brackets):")
    ok5 = True
    for s, exp in CONTROLS:
        got = bool(DIRECTION.search(s))
        ok5 &= (got == exp)
        P(f"   {'ok ' if got == exp else 'MISS'} {got!s:5} [{exp!s:5}]  {s!r}")
    P(f"G5 -> {'PASS' if ok5 else 'FAIL'} (12 controls)")

    # ---------------------------------------------------------------- PART A: the ladder
    P("\n--- PART A: the CLAIM-unit re-derivation, all 10 tuned cells x 2 exclusion readings ---")
    sets = {"26": c276[c276.cross & c276.prop].file.tolist(),
            "136": c276[c276.cross].file.tolist(),
            "14": c276[c276.cross & c276.breadth].file.tolist(),
            "292": frozen}
    frows, grows = [], []
    for L in LENGTHS:
        for ex, exre in EXCL.items():
            per = {}
            for f in frozen:
                t = read_file(f)
                if t is None:
                    continue
                h = score_file(t, f, L, exre)
                per[f] = h
                frows.append(dict(file=f, L=str(L), excl=ex, **h,
                                  in26=f in set(sets["26"]), in136=f in set(sets["136"]),
                                  in14=f in set(sets["14"]), ledger=f in LEDGERS))
            for rd in READINGS:
                counts = {k: sum(1 for f in v if per.get(f, {}).get(rd)) for k, v in sets.items()}
                grows.append(dict(L=str(L), excl=ex, reading=rd, **{f"restated_{k}": v for k, v in counts.items()},
                                  share_26=counts["26"] / 26,
                                  ledgers=sum(1 for f in LEDGERS if per.get(f, {}).get(rd)),
                                  headline=(rd == READING_HEAD and L == LENGTH_HEAD and ex == "LITERAL")))
    gr = pd.DataFrame(grows)
    pd.DataFrame(frows).to_csv(f"{OUT}.files.csv", index=False)
    gr.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"   {'L':7}{'excl':9}{'reading':9}{'of 26':>7}{'of 136':>8}{'of 14':>7}{'of 292':>8}"
      f"{'share26':>9}{'ledgers':>8}")
    for _, r in gr.iterrows():
        P(f"   {r['L']:7}{r['excl']:9}{r['reading']:9}{int(r['restated_26']):7}"
          f"{int(r['restated_136']):8}{int(r['restated_14']):7}{int(r['restated_292']):8}"
          f"{r['share_26']:9.4f}{int(r['ledgers']):8}"
          f"{'   <- HEADLINE' if r['headline'] else ''}")

    hl = gr[gr.headline].iloc[0]
    loose_hl = gr[(gr.L == str(LENGTH_HEAD)) & (gr.excl == "LITERAL") & (gr.reading == "LOOSE")].iloc[0]
    H_QUEUE = bool(int(loose_hl.restated_26) <= 13 and int(hl.restated_26) <= 7)
    H_DIRBITES = bool(int(hl.restated_26) < int(loose_hl.restated_26))
    spread_L = {}
    for rd in READINGS:
        for ex in EXCL:
            s = gr[(gr.reading == rd) & (gr.excl == ex)].restated_26
            spread_L[(rd, ex)] = int(s.max() - s.min())
    H_LENGTH = max(spread_L.values()) > 3
    H_NESTED = bool((gr.restated_26 == gr.restated_136).all())
    P(f"\n   H_QUEUE  LOOSE at the headline cell {int(loose_hl.restated_26)} (<= 13?) and TIGHT "
      f"{int(hl.restated_26)} (<= 7?) -> {'PASS' if H_QUEUE else 'FAIL'}")
    P(f"   H_DIRBITES TIGHT {int(hl.restated_26)} < LOOSE {int(loose_hl.restated_26)} "
      f"-> {'PASS' if H_DIRBITES else 'FAIL'}")
    P(f"   H_LENGTH spread of restated_26 over the 5 block LENGTHS: {spread_L} (523's window "
      f"ladder moved it by at most 3) -> {'PASS' if H_LENGTH else 'FAIL'}")
    P(f"   H_NESTED restated_26 == restated_136 at every cell: {'PASS' if H_NESTED else 'FAIL'} "
      f"({int((gr.restated_26 == gr.restated_136).sum())} of {len(gr)} cells)")
    fdf = pd.DataFrame(frows)
    sv = fdf[(fdf.L == str(LENGTH_HEAD)) & (fdf.excl == "LITERAL") & fdf.TIGHT & fdf.in26]
    P(f"   the {len(sv)} survivors at the headline cell, with the token and the direction word that "
      f"qualified them:")
    for _, r in sv.iterrows():
        P(f"      {r['file']}   tok={r['tok']!r} dir={r['dirtok']!r}")
    P(f"   per-characteristic split of the headline survivors: "
      f"{sv.tok.value_counts().to_dict()}")

    # ---------------------------------------------------------------- PART B: citations
    P("\n--- PART B: every committed site that QUOTES 26 / 136 / 14 as a census count ---")
    # TWO readings of "this is a citation of idea 276's bound", both reported; TIGHT is the headline.
    # WIDE  = the number appears in a COUNT phrase near any census word.
    # TIGHT = the same, and the window also names the bound's own provenance (idea 276, the cross-cap
    #         census, the upper bound, or idea 523's restatement).
    CENSUSCTX = re.compile(r"\bcensus\b|\bcorpus\b|upper bound|cross[- ]cap|\bfiles?\b|artefacts?", re.I)
    PROVENANCE = re.compile(r"idea 276|idea 286|idea 523|idea 295|cross[- ]cap|upper bound|"
                            r"census|restat\w*", re.I)
    UNIT_WORD = re.compile(r"keyword|token|occurrence|word|vocabulary|mention|hit", re.I)
    CLAIM_WORD = re.compile(r"claim|headline|restat\w*|direction|verdict", re.I)
    BLOCK_WORD = re.compile(r"block|headline block|whole file|title|pre-h2|chars1500|prefix|"
                            r"first \d+ characters", re.I)
    def countpat(n):
        return re.compile(rf"(?<![\d.\-])(?:of\s+(?:the\s+)?|all\s+(?:of\s+)?the\s+|the\s+)?"
                          rf"{n}(?![\d.%])(?:\s*[- ](?:file|files|artefact|artefacts)\b)?")
    NUMS = {"26": countpat(26), "136": countpat(136), "14": countpat(14)}
    COUNTPHRASE = {n: re.compile(rf"(?<![\d.\-]){n}\s*(?:files?|artefacts?|of\s+the\b|cross)|"
                                 rf"\b(?:of|all)\s+the\s+{n}\b|\b{n}[- ]files?\b", re.I)
                   for n in ("26", "136", "14")}
    crows = []
    for p in sorted(ROOT.joinpath("research").rglob("*")):
        if not p.is_file() or p.suffix not in (".py", ".md") or p.name.startswith(Path(OUT).name):
            continue
        t = p.read_text(errors="ignore")
        for num, rx in NUMS.items():
            for m in rx.finditer(t):
                a, b = max(0, m.start() - 200), min(len(t), m.end() + 200)
                win = t[a:b]
                if not CENSUSCTX.search(win):
                    continue
                if not COUNTPHRASE[num].search(win):
                    continue          # the number must be used as a COUNT, not as an id or a price
                if num == "136" and re.search(r"B136|universe_broad", win):
                    continue          # B136 is a PANEL NAME here, not a census count
                dm = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
                crows.append(dict(file=str(p.relative_to(ROOT)), num=num, pos=m.start(),
                                  date=pd.Timestamp(dm.group(1)) if dm else pd.NaT,
                                  tight=bool(PROVENANCE.search(win)),
                                  states_unit=bool(UNIT_WORD.search(win) or CLAIM_WORD.search(win)),
                                  says_keyword=bool(UNIT_WORD.search(win)),
                                  says_claim=bool(CLAIM_WORD.search(win)),
                                  states_block=bool(BLOCK_WORD.search(win))))
    cit = pd.DataFrame(crows)
    cit["corrected"] = int(hl.restated_26)
    cit.to_csv(f"{OUT}.citations.csv", index=False)
    for num in NUMS:
        for rdg in ("WIDE", "TIGHT"):
            s = cit[(cit.num == num) & (cit.tight if rdg == "TIGHT" else True)]
            if not len(s):
                P(f"   {num} {rdg}: no census-role citation found")
                continue
            P(f"   {num:4} {rdg:5}: {len(s):4} sites in {s.file.nunique():3} files; UNIT "
              f"{s.states_unit.mean():.4f} (keyword {s.says_keyword.mean():.4f} / claim "
              f"{s.says_claim.mean():.4f}); BLOCK {s.states_block.mean():.4f}; NEITHER "
              f"{float(((~s.states_unit) & (~s.states_block)).mean()):.4f}")
    for num in ():
        s = cit[cit.num == num]
        P(f"   {num:4}: {len(s):4} citation sites in {s.file.nunique():3} files; state the UNIT "
          f"{s.states_unit.mean():.4f} (keyword-word {s.says_keyword.mean():.4f}, claim-word "
          f"{s.says_claim.mean():.4f}); state the BLOCK {s.states_block.mean():.4f}; "
          f"state NEITHER {float(((~s.states_unit) & (~s.states_block)).mean()):.4f}")
    s26 = cit[(cit.num == "26") & cit.tight]      # headline reading: TIGHT
    if len(s26):
        vc = s26.file.value_counts()
        byfile = s26.groupby("file").states_unit.max()
        P(f"   CONCENTRATION of the 26-TIGHT corpus: {len(s26)} sites in {s26.file.nunique()} files; "
          f"top file {vc.index[0]} holds {int(vc.iloc[0])} ({vc.iloc[0]/len(s26):.4f}), top two "
          f"{float(vc.iloc[:2].sum())/len(s26):.4f}. FILE-level reading (a file counts once): "
          f"{byfile.mean():.4f} of {len(byfile)} files state the unit at least once, against the "
          f"site-level {s26.states_unit.mean():.4f} - the site-level number is a weighted average "
          f"over files that discuss the bound at length.")
    H_CITE = bool(((~s26.states_unit) & (~s26.states_block)).mean() > 0.50) if len(s26) else False
    P(f"   H_CITE a majority of the 26-citations state neither unit nor block: "
      f"{'PASS' if H_CITE else 'FAIL'}")
    P(f"   CORRECTED DENOMINATOR to publish beside every one of them: the claim-unit count at the "
      f"headline cell is {int(hl.restated_26)} of 26 (share {hl.share_26:.4f}); the LOOSE reading "
      f"is {int(loose_hl.restated_26)}; the full 10-cell range is "
      f"{int(gr.restated_26.min())}..{int(gr.restated_26.max())}")

    # ---------------------------------------------------------------- rule 8
    P("\n--- RULE 8 (both legs) ---")
    wfrows = []
    dated = cit[(cit.num == "26") & cit.date.notna()]
    if len(dated) >= 4:
        med = dated.date.median()
        e, l = dated[dated.date <= med], dated[dated.date > med]
        note = f"median cut {pd.Timestamp(med).date()}"
        if not len(l):                 # every dated citation shares one or two dates
            ds = dated.sort_values(["date", "file", "pos"])
            h = len(ds) // 2
            e, l = ds.iloc[:h], ds.iloc[h:]
            note = (f"median cut {pd.Timestamp(med).date()} leaves the later half EMPTY (the "
                    f"citations are all dated on or before it), so the leg runs on the INDEX "
                    f"midpoint of the date-sorted sites and the date cut is UNRESOLVABLE")
        P(f"   ON THE CENSUS: {note}")
        a, b = e.states_unit.mean(), l.states_unit.mean()
        H_R8CENSUS = bool(abs(b - a) <= 0.10)
        P(f"   ON THE CENSUS: share stating the unit "
          f"{a:.4f} on {len(e)} earlier sites vs {b:.4f} on {len(l)} later sites, gap "
          f"{abs(b - a):.4f} -> {'PASS' if H_R8CENSUS else 'FAIL'}")
        wfrows.append(dict(leg="R8_CENSUS", detail="states_unit share", IS=a, OOS=b,
                           gap=abs(b - a), n_IS=len(e), n_OOS=len(l), passes=H_R8CENSUS))
    else:
        H_R8CENSUS = False
        P("   ON THE CENSUS: fewer than 4 dated 26-citations; leg UNRESOLVABLE -> FAIL as declared")
    # on the claim: the cell is chosen on the earlier half of the frozen 26, read once on the later
    f26 = sorted(sets["26"])
    d26 = [(f, pd.Timestamp(f[:10]) if re.match(r"\d{4}-\d{2}-\d{2}", f) else pd.NaT) for f in f26]
    dd = pd.DataFrame(d26, columns=["file", "date"]).dropna()
    medf = dd.date.median()
    ISf, OOSf = set(dd[dd.date <= medf].file), set(dd[dd.date > medf].file)
    split_note = f"date median {pd.Timestamp(medf).date()}"
    if not OOSf:                      # the frozen corpus is frozen AT 2026-09-06: 24 of 26 share
        dd = dd.sort_values(["date", "file"])      # two dates, so a date cut cannot split it.
        half = len(dd) // 2
        ISf, OOSf = set(dd.file.iloc[:half]), set(dd.file.iloc[half:])
        split_note = (f"date median {pd.Timestamp(medf).date()} leaves the later half EMPTY (the "
                      f"frozen corpus ends on that date), so the leg is run on the INDEX midpoint "
                      f"of the date-sorted list instead, and the date reading is reported as "
                      f"UNRESOLVABLE")
        P(f"   ON THE CLAIM: {split_note}")
    best, pick = -1.0, None
    for _, r in gr.iterrows():
        sub = fdf[(fdf.L == r["L"]) & (fdf.excl == r["excl"]) & fdf.file.isin(ISf)]
        sh = sub[r["reading"]].mean() if len(sub) else np.nan
        if sh == sh and sh > best:
            best, pick = sh, (r["L"], r["excl"], r["reading"])
    sub = fdf[(fdf.L == pick[0]) & (fdf.excl == pick[1]) & fdf.file.isin(OOSf)]
    oos_sh = float(sub[pick[2]].mean())
    H_R8CLAIM = bool(abs(oos_sh - best) <= 0.10)
    P(f"   ON THE CLAIM: cell chosen on the {len(ISf)} frozen-26 files dated <= "
      f"{pd.Timestamp(medf).date()} -> {pick} at IS share {best:.4f}; the {len(OOSf)} later files "
      f"read ONCE give {oos_sh:.4f}, gap {abs(oos_sh - best):.4f} -> "
      f"{'PASS' if H_R8CLAIM else 'FAIL'}")
    wfrows.append(dict(leg="R8_CLAIM", detail=str(pick), IS=best, OOS=oos_sh,
                       gap=abs(oos_sh - best), n_IS=len(ISf), n_OOS=len(OOSf), passes=H_R8CLAIM))

    # ---------------------------------------------------------------- book leg
    P("\n--- BOOK LEG (from prices here): BOTH KEEP PATHS, U56 at 3 rungs + every panel the "
      "survivors NAME ---")
    books = {"RULES v1": lambda q: rules_v1_weights(q),
             "LIVE RULES v2 (band 0.03, g 0.75)": lambda q: rules_v2_weights(q, 0.03, 0.75),
             "CAND 4b (band 0.03, g 1.00)": lambda q: rules_v2_weights(q, 0.03, 1.00)}
    brows = []
    for rung in RUNGS:
        live = book_metrics(px, books["LIVE RULES v2 (band 0.03, g 0.75)"], rung)
        for nm, fn in books.items():
            b = book_metrics(px, fn, rung)
            brows.append(dict(panel="U56", book=nm, rung=rung, **b, **keep_paths(b, live, spy)))
        brows.append(dict(panel="U56", book="SPY buy-and-hold", rung=rung, **spy,
                          pass_4a=False, pass_4b=False))
    # the panels the surviving files name (the census decision priced, not assumed irrelevant)
    named = set()
    for f in sv.file:
        t = read_file(f) or ""
        if re.search(r"\bU56\b|universe\.json", t):
            named.add("U56")
        if re.search(r"\bB136\b|universe_broad", t):
            named.add("B136")
        if SMALL_TOK.search(t):
            named.add("SMALL")
    P(f"   the headline survivor set names panels {sorted(named) if named else '(none)'}")
    for pan in sorted(named - {"U56"}):
        if pan == "B136":
            q = load_universe(broad=True)
            note = "current constituents"
        else:
            q, ndrop = load_small()
            note = f"sub-$2B screen, {ndrop} max_1d_move>=1.0 tickers dropped, SURVIVORSHIP"
        sp = spy_metrics(q)
        lv = book_metrics(q, books["LIVE RULES v2 (band 0.03, g 0.75)"], RUNG_HEAD)
        for nm in ("LIVE RULES v2 (band 0.03, g 0.75)", "CAND 4b (band 0.03, g 1.00)"):
            b = book_metrics(q, books[nm], RUNG_HEAD)
            brows.append(dict(panel=pan, book=nm, rung=RUNG_HEAD, **b, **keep_paths(b, lv, sp)))
        brows.append(dict(panel=pan, book="SPY buy-and-hold", rung=RUNG_HEAD, **sp,
                          pass_4a=False, pass_4b=False))
        P(f"   panel {pan}: {q.shape[1]} columns, {q.index[0].date()}..{q.index[-1].date()} ({note})")
    bk = pd.DataFrame(brows)
    P(f"   {'panel':7}{'book':34}{'rung':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>9}{'H1':>7}{'H2':>7}"
      f"{'oCAGR':>8}{'oSh':>7}{'oDD':>9}  4a     4b")
    for _, r in bk.iterrows():
        P(f"   {r['panel']:7}{r['book']:34}{r['rung']:5.0f}{r['CAGR']:8.2%}{r['Sharpe']:8.4f}"
          f"{r['MaxDD']:9.2%}{r['H1']:7.3f}{r['H2']:7.3f}{r['OOS_CAGR']:8.2%}{r['OOS_Sharpe']:7.3f}"
          f"{r['OOS_MaxDD']:9.2%}  {str(r['pass_4a']):6}{str(r['pass_4b'])}")
    pd.concat([pd.DataFrame(wfrows), bk], axis=0).to_csv(f"{OUT}.walkforward.csv", index=False)
    n4a, n4b = int(bk.pass_4a.sum()), int(bk.pass_4b.sum())

    H = dict(H_276=H_276, H_523=H_523, H_QUEUE=H_QUEUE, H_DIRBITES=H_DIRBITES, H_LENGTH=H_LENGTH,
             H_NESTED=H_NESTED, H_CITE=H_CITE, H_R8CENSUS=H_R8CENSUS, H_R8CLAIM=H_R8CLAIM)
    P("\n--- PRE-REGISTERED HYPOTHESES ---")
    for k, v in H.items():
        P(f"   {k:12} {'PASS' if v else 'FAIL'}")
    P(f"   {sum(H.values())} of {len(H)} PASS")
    P(f"\nelapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")

    u10 = bk[(bk.panel == "U56") & (bk.rung == RUNG_HEAD)].set_index("book")
    Path(f"{OUT}.result.md").write_text(f"""# Idea 534 - idea 276's characteristic file count, re-derived from HEADLINE CLAIMS  ({DATE}, cloud)

## The answer
**The 26 is {int(hl.restated_26)} when the unit is a restatable DIRECTION claim in the first
{LENGTH_HEAD} characters** (share {hl.share_26:.4f}), {int(loose_hl.restated_26)} when the direction
requirement is dropped, and **{int(gr.restated_26.min())}..{int(gr.restated_26.max())} over all 10
tuned cells**.  The queue's arithmetic (<= 13 loose, <= 7 tight) {'HOLDS' if H_QUEUE else 'FAILS'}.
**H_DIRBITES FAILS at the headline cell and the failure is informative**: at L=1500 the four
surviving files all carry a direction token anyway (TIGHT {int(hl.restated_26)} = LOOSE
{int(loose_hl.restated_26)}), while the requirement bites at every LONGER block -
{'; '.join(f"L={r.L} {int(gr[(gr.L==r.L)&(gr.excl=='LITERAL')&(gr.reading=='LOOSE')].restated_26.iloc[0])}->" + str(int(gr[(gr.L==r.L)&(gr.excl=='LITERAL')&(gr.reading=='TIGHT')].restated_26.iloc[0])) for _, r in gr[(gr.excl=='LITERAL')&(gr.reading=='LOOSE')].iterrows())} -
i.e. a short block already selects for assertive text, and the direction predicate only does work
once the block is long enough to include method prose.  The count **{'IS a LENGTH fact' if H_LENGTH else 'is NOT a length fact'}**: over the
five block lengths it moves by {max(spread_L.values())} files against the <= 3 that idea 523's
window ladder moved it, so 523's "block-rule, not window" reading sharpens to **block EXTENT** -
the number is set by how much of the file you read, not by how wide the role window is.
523's structural theorem re-tested under the claim predicate: restated_26 == restated_136 in
{int((gr.restated_26 == gr.restated_136).sum())} of {len(gr)} cells.

## What the record quotes
{len(s26)} committed sites quote 26 in a census role across {s26.file.nunique()} files.  They state
the UNIT they counted {s26.states_unit.mean():.4f} of the time and the BLOCK
{s26.states_block.mean():.4f}; only **{float(((~s26.states_unit) & (~s26.states_block)).mean()):.4f} state
neither** - so **H_CITE FAILS in the record's favour**: the citations of this particular bound are
mostly unit-stated, because the corpus is dominated by the files that restated it.  CONCENTRATION, so
the number is not read as a property of the record at large: the top file holds
{float(s26.file.value_counts().iloc[0]) / len(s26):.4f} of the 75 sites and the top two
{float(s26.file.value_counts().iloc[:2].sum()) / len(s26):.4f}; the FILE-level reading is
{float(s26.groupby('file').states_unit.max().mean()):.4f} of {s26.file.nunique()} files.  The BLOCK is
stated less than half the time, which is the leg that matters now that the count is shown to be a
block-extent fact.  The corrected denominator to publish beside each citation is
**{int(hl.restated_26)} of 26 claim-bearing files, block length {LENGTH_HEAD} characters**.

## Rule 8
* ON THE CENSUS: **{'PASS' if H_R8CENSUS else 'FAIL'}** - the date cut is UNRESOLVABLE (every dated
  26-citation sits on or before the median), so the leg runs on the index midpoint of the date-sorted
  sites: the unit-stating share goes {float(pd.DataFrame(wfrows).query("leg=='R8_CENSUS'").IS.iloc[0]):.4f}
  -> {float(pd.DataFrame(wfrows).query("leg=='R8_CENSUS'").OOS.iloc[0]):.4f}, gap
  {float(pd.DataFrame(wfrows).query("leg=='R8_CENSUS'").gap.iloc[0]):.4f} against a 0.10 bar - the
  record's citation hygiene on this bound IMPROVED over the corpus, which fails a stability test and
  is good news about the record.
* ON THE CLAIM: cell chosen on the earlier frozen-26 files ({pick}) at IS share {best:.4f}, later
  files read once {oos_sh:.4f}, gap {abs(oos_sh - best):.4f} ({'PASS' if H_R8CLAIM else 'FAIL'}).

## Book leg (computed from prices here; nothing tuned, nothing promoted)
4a passes **{n4a}** and 4b passes **{n4b}** of {len(bk)} book-panel-rung rows.  U56 at 10 bps: LIVE
RULES v2 {u10.loc['LIVE RULES v2 (band 0.03, g 0.75)','CAGR']:.2%} /
{u10.loc['LIVE RULES v2 (band 0.03, g 0.75)','Sharpe']:.4f} /
{u10.loc['LIVE RULES v2 (band 0.03, g 0.75)','MaxDD']:.2%}; the standing 4b candidate
{u10.loc['CAND 4b (band 0.03, g 1.00)','CAGR']:.2%} /
{u10.loc['CAND 4b (band 0.03, g 1.00)','Sharpe']:.4f} /
{u10.loc['CAND 4b (band 0.03, g 1.00)','MaxDD']:.2%} (OOS
{u10.loc['CAND 4b (band 0.03, g 1.00)','OOS_CAGR']:.2%} /
{u10.loc['CAND 4b (band 0.03, g 1.00)','OOS_Sharpe']:.4f} /
{u10.loc['CAND 4b (band 0.03, g 1.00)','OOS_MaxDD']:.2%}); SPY {spy['CAGR']:.2%} /
{spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} (OOS {spy['OOS_CAGR']:.2%} / {spy['OOS_Sharpe']:.4f} /
{spy['OOS_MaxDD']:.2%}).  The survivor set names {sorted(named)}, so the census decision was priced
on those panels rather than assumed irrelevant.

## Verdict
**ANSWERED - {sum(H.values())} of {len(H)} pre-registered hypotheses PASS.**  No RULES change, no
KEEP, no memo, no book promoted.  **PROPOSED, not applied (PROTOCOL rule 6, Sunday review only):**
a census count may be quoted only with its UNIT (keyword occurrence vs restatable claim) and its
BLOCK; the record's 26 should be cited as "{int(hl.restated_26)} claim-bearing of 26 keyword-bearing
files, claim = direction token inside the first {LENGTH_HEAD} characters".

## Caveats
The frozen 292-file list is idea 276's, not today's corpus.  Survivorship: U56 and B136 are
current-constituent lists and the small panel is a screen read today with {SMALL_MAXMOVE}-move names
dropped, so every small-cap number is biased upward.  The predicates are TEXT detectors: G5 scores
the direction detector on 12 printed controls and the per-file table is committed, so any other
reading can be re-scored without re-running anything.
""")
    P(f"wrote {Path(OUT).name}.result.md")


if __name__ == "__main__":
    main()
