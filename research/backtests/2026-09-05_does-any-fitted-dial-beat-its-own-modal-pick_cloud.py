#!/usr/bin/env python3
"""IDEA 189  does-any-fitted-dial-beat-its-own-modal-pick   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 175 found that on the CADENCE dial the pre-registered constant M beats the IS selector
that PICKS M in 79% of books (+0.0761 against +0.0388), because the selector's rare off-modal
picks are catastrophic: its 27 monthly picks earn +0.0531 each and its 4 quarterly picks lose
-0.3368 each.  The queue asks whether that generalises to every dial in idea 171's five:

    for each dial, compare the IS selector against a CONSTANT FIXED AT THE SELECTOR'S OWN
    MODAL PICK.  If the constant wins on all five, "fit the dial" is dominated by "read the
    mode once and write it down" -- which is a PROTOCOL clause, not a backtest.

This is a sharper test than idea 171's, which compared the selector against its INHERITED
incumbent (g=0.75, n=20, band=0, W, sleeve=0).  A selector can lose to its inherited constant
merely because the incumbent happens to sit in a good place on the ladder (idea 183's
anchor-position caveat).  The modal-pick constant removes that defence entirely: it is the
selector's OWN answer, held fixed, so any gap is pure choice variance.

  Q1  REPRODUCTION.  Rebuild idea 171's 1908-row ladder with its own code and match the
      committed CSV before any new number is read; re-derive its published headline.
  Q2  THE MODE.  Per dial, what does SEL-SHARPE pick, how concentrated is that distribution,
      and how often does the selector agree with its own mode?
  Q3  THE ANSWER.  MODAL-CONST vs SEL-SHARPE, paired over books, on all five dials, under
      three mode definitions and two OOS scores -- every grid point reported.
  Q4  THE MECHANISM.  Conditional on the selector going OFF-mode, what does it earn?  If the
      modal constant wins only through rare disasters, the clause to write is about tail
      picks, not about fitting per se.
  Q5  A SECOND, DISJOINT CORPUS.  115 books built on idea 175's panel definitions
      (SMALL439 / U56 / ETF36 + 112 sub-panels), all five dials, so the answer is not one
      corpus's property.
  Q6  RULE 8 (PROTOCOL clause 8) and BOTH KEEP PATHS.

DESIGN
------
Idea 171's script is IMPORTED, not re-implemented: `Book`, `build_corpus`, `fast_backtest`,
`rel_margin`, `keep_4a`, `keep_4b`, `tstat`, `sign_p`, the five dials and their ladders all
execute the parent's own code, so every number sits on the simulator being audited.

  dials (idea 171's, unchanged)
      GROSS   [0.20 .. 1.00], 10 points, incumbent 0.75
      N       [3 .. 50],      10 points, incumbent 20
      BAND    [0.00 .. 0.08],  5 points, incumbent 0.00
      CADENCE [D, W, M, Q],    4 points, incumbent W
      SLEEVE  [0.00 .. 0.30],  7 points, incumbent 0.00
  corpus A : idea 171's 53 books (5 fixed panels + 48 seeded B136 sub-panels)
  corpus B : 115 books on idea 175's panel definitions, rebuilt under idea 171's Book class
  costs    : 10 bps, t+1, IS <= 2016-12-31, OOS >= 2017-01-01 read ONCE

  ARMS, per dial and book
      CONST-INC     idea 171's inherited incumbent                     (its do-nothing arm)
      SEL-SHARPE    argmax of IS Sharpe over the ladder                (the incumbent fit)
      SEL-4B        argmax of the IS 4b relative margin                (the other fit)
      MODE-GLOBAL   the modal SEL-SHARPE pick over the whole corpus
      MODE-LOO      the modal SEL-SHARPE pick over the OTHER books     (no self-vote)
      MODE-XCORPUS  corpus A's mode applied to corpus B, and vice versa (out-of-corpus)
      RANDOM        a uniformly random ladder point, fixed seed        (idea 151's control)
      ORACLE        the OOS argmax                                     (not implementable)

  TUNED PARAMETER 1: the mode definition   {GLOBAL, LOO, XCORPUS}   (all three reported)
  TUNED PARAMETER 2: the OOS score         {OOS Sharpe, OOS 4b margin} (both reported)
  The dials, their ladders, the corpora and the 10 bps cost are INHERITED, not chosen here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  Idea 171's ladder reproduces at < 1e-12 on OOS Sharpe over all 1908 rows, and its
      published CADENCE headline (SEL-SHARPE +0.0642, t +4.54) re-derives to within 0.001.
  P2  On CADENCE, MODE-LOO beats SEL-SHARPE on corpus A (idea 175 found this on its own).
  P3  The queue's "if" fires: MODE-LOO beats SEL-SHARPE on 5 of 5 dials on OOS Sharpe,
      corpus A.
  P4  The selector agrees with its own mode in more than 50% of books on at least 3 of the
      5 dials, so the gap is carried by a minority of off-modal picks.
  P5  Conditional on disagreement, SEL-SHARPE's mean dOOS against MODE-LOO is NEGATIVE on
      every one of the five dials.
  P6  No arm produces a 4b KEEP on either corpus.

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): B136, U56 and the small panel are current-constituent lists.  All
    arms inherit it equally, so the PAIRED comparison is unaffected; every LEVEL is biased
    upward and is not a tradable estimate.
  * The mode is a statistic of the corpus.  MODE-GLOBAL uses a book's own vote to build the
    constant applied to that book -- a mild leak, which is exactly why MODE-LOO and
    MODE-XCORPUS are reported beside it and why the headline is read off MODE-LOO.
  * The books in a corpus are NOT independent: 48 of corpus A's 53 are sub-panels of B136 and
    112 of corpus B's 115 are sub-panels of three parents, so every paired t here is over
    correlated units and its nominal size is optimistic.  The sign test is reported beside it
    for that reason, and neither is treated as a p-value on a fresh sample.
  * Corpus B is built on idea 175's PANEL DEFINITIONS under idea 171's `Book` class, with the
    sleeve assets attached as price columns so that all five dials exist.  Attaching columns
    perturbs the composite's cross-sectional pct-ranks, so corpus B's books are near-copies of
    idea 175's and NOT identical to them: no number here is claimed to reproduce idea 175, and
    the reproduction control is against idea 171 only.
  * Idea 144: a re-grossed / re-cadenced / re-sleeved book is the SAME book.  Nothing here is
    a new signal and nothing is proposed.
  * On k=20 sub-panels the N ladder saturates (n >= 20 admits every eligible name), so those
    points collapse onto ew-all.  Inherited from idea 171, reported not hidden.
  * Idea 38's calendar-day index and idea 126's t+1-only execution carry over.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .modes.csv, .paired.csv,
.walkforward.csv  (the KEEP columns fail4a/fail4b live in .ladder.csv).
"""
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import metrics  # noqa: E402

STEM = "2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_cloud"
OUT = ROOT / "research" / "backtests"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
P175_STEM = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ import idea 171 verbatim
spec = importlib.util.spec_from_file_location("p171", OUT / f"{P171_STEM}.py")
p171 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p171)

DIALS, DIAL_ORDER, INC = p171.DIALS, p171.DIAL_ORDER, p171.INC
COST_BPS, IS_END, OOS_START = p171.COST_BPS, p171.IS_END, p171.OOS_START
SLEEVE_ASSETS, MAX_VOL = p171.SLEEVE_ASSETS, p171.MAX_VOL
fast_backtest, rel_margin, halves = p171.fast_backtest, p171.rel_margin, p171.halves
keep_4a, keep_4b, tstat, sign_p = p171.keep_4a, p171.keep_4b, p171.tstat, p171.sign_p
p171.P = P                     # idea 171's reproduction controls print into THIS console

MODE_ARMS = ["MODE-GLOBAL", "MODE-LOO", "MODE-XCORPUS"]
SCORES = ["OOS_Sharpe", "OOS_margin"]
RAND_SEED = 189_900


# ---------------------------------------------------------- corpus B: idea 175's panels
def build_corpus_B():
    """Idea 175's 115 book definitions, rebuilt under idea 171's Book class.  Sleeve assets are
    attached as price columns wherever they are missing so that all five dials exist on every
    book -- which makes these NEAR-COPIES of idea 175's books, not identical ones (see the
    caveat in the docstring).  Seeds and draw counts are idea 175's, read from its module."""
    spec5 = importlib.util.spec_from_file_location("p175", OUT / f"{P175_STEM}.py")
    p175 = importlib.util.module_from_spec(spec5)
    spec5.loader.exec_module(p175)

    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  corpus B small panel: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} "
      "tradable (SURVIVORSHIP: current constituents only, no delistings)")
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    add = ref[SLEEVE_ASSETS].reindex(pxs.index, method="ffill")
    pxs = pd.concat([pxs[s_stk + ["SPY"]], add], axis=1).ffill()

    u_stk = [c for c in px56.columns if c != "SPY"]
    e_stk = [t for t in etf36 if t in px56.columns and t != "SPY"]

    def keep(px, cols):
        cols = [c for c in cols if c in px.columns]
        allc = list(dict.fromkeys(cols + ["SPY"]
                                  + [c for c in SLEEVE_ASSETS if c in px.columns]))
        return px[allc].dropna(how="all").ffill()

    books = [p171.Book("SMALL439", keep(pxs, s_stk), set(s_stk), "SMALL"),
             p171.Book("U56", keep(px56, u_stk), set(u_stk), "U56"),
             p171.Book("ETF36", keep(px56, e_stk), set(e_stk), "U56")]
    pools = {"SMALL": (pxs, s_stk), "U56": (px56, u_stk), "ETF": (px56, e_stk)}
    for fam in p175.FAMILIES:
        seed, ks = p175.DRAWS[fam]
        pxp, pool = pools[fam]
        for k in ks:
            rng = np.random.default_rng(seed + k)
            for d in range(p175.N_DRAWS):
                sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
                par = "SMALL" if fam == "SMALL" else "U56"
                books.append(p171.Book(f"{fam}k{k}d{d:02d}", keep(pxp, sub), set(sub), par))
    return books, {"U56": px56, "SMALL": pxs}


# ------------------------------------------------------------------------- ladder runner
def run_ladder(books, panels, tag, t0):
    START, SPY, BASE = {}, {}, {}
    for b in books:
        if b.parent not in SPY:
            px = panels[b.parent]
            st = px.index[260]
            START[b.parent] = st
            SPY[b.parent] = px["SPY"].pct_change().fillna(0.0).loc[st:]
            BASE[b.parent] = fast_backtest(px, rules_v1_weights(px), COST_BPS,
                                           "W")["returns"].loc[st:]
    rows = []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        spy = SPY[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        base = BASE[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for dial in DIAL_ORDER:
            ladder, _ = DIALS[dial]
            for pt in ladder:
                kw = dict(gross=INC["GROSS"], n=INC["N"], band=INC["BAND"],
                          sleeve=INC["SLEEVE"])
                fq = INC["CADENCE"]
                if dial == "GROSS":
                    kw["gross"] = pt
                elif dial == "N":
                    kw["n"] = pt
                elif dial == "BAND":
                    kw["band"] = pt
                elif dial == "SLEEVE":
                    kw["sleeve"] = pt
                elif dial == "CADENCE":
                    fq = pt
                res = fast_backtest(bk.px, bk.weights(**kw), COST_BPS, fq)
                r = res["returns"].loc[st:]
                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
                mg_is, wb_is = rel_margin(r_is, spy_is)
                mg_oos, wb_oos = rel_margin(r_oos, spy_oos)
                h1, h2 = halves(r)
                rows.append(dict(
                    corpus=tag, book=bk.name, parent=bk.parent, dial=dial, point=pt,
                    is_incumbent=(pt == INC[dial]),
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                    turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                    IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                    IS_margin=mg_is, IS_worstbar=wb_is,
                    OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                    OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                    fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos)))
        if (bi + 1) % 25 == 0:
            P(f"   ... {tag} {bi + 1}/{len(books)} books  ({time.time() - t0:.0f}s)")
    return pd.DataFrame(rows), SPY, BASE


def picks_of(lad, books):
    """SEL-SHARPE / SEL-4B / ORACLE picks per (dial, book), on the ladder's own order."""
    rng = np.random.default_rng(RAND_SEED)
    out = []
    for dial in DIAL_ORDER:
        ladder, const = DIALS[dial]
        for bk in books:
            sub = lad[(lad.dial == dial) & (lad.book == bk)].set_index("point").reindex(ladder)
            out.append(dict(dial=dial, book=bk,
                            CONST_INC=const,
                            SEL_SHARPE=sub["IS_Sharpe"].idxmax(),
                            SEL_4B=sub["IS_margin"].idxmax(),
                            RANDOM=ladder[int(rng.integers(len(ladder)))],
                            ORACLE=sub["OOS_Sharpe"].idxmax()))
    return pd.DataFrame(out)


_IDX: dict = {}


def index_ladder(lad, tag):
    """(tag, dial, book, str(point)) -> the ladder row, so the paired tests below are dict
    lookups rather than 20k boolean scans over a 6000-row frame."""
    for rec in lad.to_dict("records"):
        _IDX[(tag, rec["dial"], rec["book"], str(rec["point"]))] = rec


def score_of(tag, dial, book, point, col):
    r = _IDX.get((tag, dial, book, str(point)))
    return float(r[col]) if r is not None else np.nan


def row_of(tag, dial, book, point):
    return _IDX[(tag, dial, book, str(point))]


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 189  does-any-fitted-dial-beat-its-own-modal-pick   (cloud, 2026-09-05)")
    P("=" * 118)

    # ------------------------------------------------------------------ corpus A + repro
    P("\nbuilding corpus A (idea 171's build_corpus, imported) ...")
    booksA, panelsA = p171.build_corpus()
    P(f"  corpus A: {len(booksA)} books")
    P("\nREPRODUCTION CONTROLS (asserted before any new number is read)")
    okA = p171.check_a(booksA[1])
    okB = all(p171.check_b(b) for b in booksA[:3])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED -- not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    P("\nrunning corpus A ladders ...")
    ladA, SPYA, BASEA = run_ladder(booksA, panelsA, "A", t0)
    P(f"   {len(ladA)} ladder rows  ({time.time() - t0:.0f}s)")
    index_ladder(ladA, "A")

    C171 = pd.read_csv(OUT / f"{P171_STEM}.ladder.csv")
    key = ["book", "dial", "point"]
    m = ladA.astype({"point": str}).merge(C171.astype({"point": str}), on=key,
                                          suffixes=("", "_c"))
    P(f"\n  [c] rebuilt ladder vs idea 171's committed ladder.csv: {len(m)}/{len(C171)} rows matched")
    dmax = 0.0
    for col in ["IS_Sharpe", "OOS_Sharpe", "OOS_margin", "OOS_CAGR", "OOS_MaxDD"]:
        d = float((m[col] - m[f"{col}_c"]).abs().max())
        dmax = max(dmax, d)
        P(f"      max |d{col}| = {d:.3e}")
    v4 = int((m["fail4b"] != m["fail4b_c"]).sum()) + int((m["fail4a"] != m["fail4a_c"]).sum())
    P(f"      4a/4b verdict mismatches: {v4}")
    repro = (len(m) == len(C171)) and dmax < 1e-12 and v4 == 0
    P(f"      -> {'PASS' if repro else 'FAIL'}")
    if not repro:
        P("\n*** idea 171's corpus does not reproduce.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ------------------------------------------------------------------ corpus B
    P("\nbuilding corpus B (idea 175's panel definitions, idea 171's Book class) ...")
    booksB, panelsB = build_corpus_B()
    P(f"  corpus B: {len(booksB)} books")
    P("\nrunning corpus B ladders ...")
    ladB, SPYB, BASEB = run_ladder(booksB, panelsB, "B", t0)
    P(f"   {len(ladB)} ladder rows  ({time.time() - t0:.0f}s)")
    index_ladder(ladB, "B")
    LAD = pd.concat([ladA, ladB], ignore_index=True)
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

    nameA = [b.name for b in booksA]
    nameB = [b.name for b in booksB]
    P(f"\n  corpus A and corpus B share {len(set(nameA) & set(nameB))} book names "
      f"(U56 appears in both by construction; its panels differ in tradable set)")

    pkA, pkB = picks_of(ladA, nameA), picks_of(ladB, nameB)

    # ------------------------------------------------------- reproduce idea 171's headline
    P("\n" + "=" * 118)
    P("Q1  idea 171's published headline, re-derived from the rebuilt ladder")
    P("=" * 118)
    P(f"  {'dial':8s} {'SEL-SHARPE - CONST-INC':>24s} {'t':>8s} {'W/L':>9s}   (idea 171 published: "
      "CADENCE +0.0642 t +4.54, SLEEVE +0.1801)")
    for dial in DIAL_ORDER:
        d = []
        for bk in nameA:
            pt = pkA[(pkA.dial == dial) & (pkA.book == bk)]["SEL_SHARPE"].iloc[0]
            d.append(score_of("A", dial, bk, pt, "OOS_Sharpe")
                     - score_of("A", dial, bk, INC[dial], "OOS_Sharpe"))
        d = np.array(d)
        P(f"  {dial:8s} {d.mean():+24.4f} {tstat(d):+8.2f} {int((d>0).sum()):4d}/"
          f"{int((d<0).sum()):<4d}")

    # ------------------------------------------------------------------ Q2 the modes
    P("\n" + "=" * 118)
    P("Q2  THE MODE.  What does SEL-SHARPE pick, how concentrated is it, and how often does")
    P("    the selector agree with its own mode?")
    P("=" * 118)
    modes = {}
    mrows = []
    for tag, pk, names in [("A", pkA, nameA), ("B", pkB, nameB)]:
        for dial in DIAL_ORDER:
            s = pk[pk.dial == dial]["SEL_SHARPE"]
            vc = s.value_counts()
            modes[(tag, dial)] = vc.index[0]
            share = float(vc.iloc[0] / len(s))
            dist = " ".join(f"{p}:{int(vc.get(p, 0))}" for p in DIALS[dial][0])
            mrows.append(dict(corpus=tag, dial=dial, mode=vc.index[0], mode_share=share,
                              n_books=len(s), distinct=int(len(vc)),
                              incumbent=INC[dial], mode_is_incumbent=vc.index[0] == INC[dial]))
            P(f"  corpus {tag}  {dial:8s} mode={str(vc.index[0]):>6s} in {share:5.1%} of "
              f"{len(s):3d} books  (incumbent {str(INC[dial]):>6s}"
              f"{', SAME' if vc.index[0] == INC[dial] else ', DIFFERENT'})   picks  {dist}")
    MD = pd.DataFrame(mrows)
    MD.to_csv(OUT / f"{STEM}.modes.csv", index=False)

    # ------------------------------------------------------------------ arms and pairing
    def mode_pick(tag, dial, book, variant, pk):
        if variant == "MODE-GLOBAL":
            return modes[(tag, dial)]
        if variant == "MODE-LOO":
            s = pk[(pk.dial == dial) & (pk.book != book)]["SEL_SHARPE"]
            return s.value_counts().index[0]
        if variant == "MODE-XCORPUS":
            return modes[("B" if tag == "A" else "A", dial)]
        raise ValueError(variant)

    P("\n" + "=" * 118)
    P("Q3  THE ANSWER.  Every arm MINUS SEL-SHARPE, paired over books, per dial, per corpus,")
    P("    on both OOS scores.  A POSITIVE number means the arm beats the fit.")
    P("=" * 118)
    prows = []
    for tag, lad, pk, names in [("A", ladA, pkA, nameA), ("B", ladB, pkB, nameB)]:
        for dial in DIAL_ORDER:
            for arm in ["CONST-INC", "SEL-4B", "RANDOM", "ORACLE"] + MODE_ARMS:
                for score in SCORES:
                    d, agree, off_d, off_n = [], 0, [], 0
                    for bk in names:
                        row = pk[(pk.dial == dial) & (pk.book == bk)].iloc[0]
                        sel = row["SEL_SHARPE"]
                        if arm == "CONST-INC":
                            pt = INC[dial]
                        elif arm == "SEL-4B":
                            pt = row["SEL_4B"]
                        elif arm == "RANDOM":
                            pt = row["RANDOM"]
                        elif arm == "ORACLE":
                            pt = row["ORACLE"]
                        else:
                            pt = mode_pick(tag, dial, bk, arm, pk)
                        a = score_of(tag, dial, bk, pt, score)
                        b = score_of(tag, dial, bk, sel, score)
                        d.append(a - b)
                        if pt == sel:
                            agree += 1
                        else:
                            off_d.append(a - b)
                            off_n += 1
                    d = np.array(d)
                    p, w, l = sign_p(d)
                    prows.append(dict(
                        corpus=tag, dial=dial, arm=arm, score=score, n=len(d),
                        mean_d=float(d.mean()), median_d=float(np.median(d)),
                        t=tstat(d), wins=w, losses=l, ties=int(len(d) - w - l), sign_p=p,
                        agree_share=agree / len(d),
                        off_n=off_n,
                        off_mean_d=float(np.mean(off_d)) if off_d else np.nan))
    PR = pd.DataFrame(prows)
    PR.to_csv(OUT / f"{STEM}.paired.csv", index=False)

    for tag in ("A", "B"):
        for score in SCORES:
            P(f"\n  --- corpus {tag}, OOS score = {score} " + "-" * 60)
            P(f"  {'dial':8s} {'arm':13s} {'mean d':>9s} {'t':>7s} {'W':>4s} {'L':>4s} "
              f"{'T':>3s} {'sign p':>8s} {'agree':>7s} {'off-mode n':>11s} {'off-mode d':>11s}")
            sub = PR[(PR.corpus == tag) & (PR.score == score)]
            for dial in DIAL_ORDER:
                for arm in MODE_ARMS + ["CONST-INC", "SEL-4B", "RANDOM", "ORACLE"]:
                    r = sub[(sub.dial == dial) & (sub.arm == arm)].iloc[0]
                    P(f"  {dial:8s} {arm:13s} {r.mean_d:+9.4f} {r.t:+7.2f} {r.wins:4d} "
                      f"{r.losses:4d} {r.ties:3d} {r.sign_p:8.4f} {r.agree_share:7.1%} "
                      f"{r.off_n:11d} "
                      f"{'' if not np.isfinite(r.off_mean_d) else f'{r.off_mean_d:+11.4f}'}")

    P("\n  HEADLINE — dials (of 5) where the MODAL CONSTANT beats the fit, by variant/score:")
    P(f"  {'corpus':7s} {'variant':13s} {'score':12s} {'dials won':>10s}   detail")
    for tag in ("A", "B"):
        for arm in MODE_ARMS:
            for score in SCORES:
                sub = PR[(PR.corpus == tag) & (PR.arm == arm) & (PR.score == score)]
                won = [d for d in DIAL_ORDER
                       if float(sub[sub.dial == d]["mean_d"].iloc[0]) > 0]
                det = " ".join(f"{d}:{float(sub[sub.dial==d]['mean_d'].iloc[0]):+.4f}"
                               for d in DIAL_ORDER)
                P(f"  {tag:7s} {arm:13s} {score:12s} {len(won):6d}/5     {det}")

    # ------------------------------------------------------------------ Q4 the mechanism
    P("\n" + "=" * 118)
    P("Q4  THE MECHANISM.  Restricted to books where the selector goes OFF its own mode, what")
    P("    does it earn?  (MODE-LOO, OOS Sharpe.)  A large negative off-mode number means the")
    P("    modal constant wins through rare disasters, not through fitting being useless.")
    P("=" * 118)
    P(f"  {'corpus':7s} {'dial':8s} {'agree':>7s} {'off n':>6s} {'off-mode mean d':>16s} "
      f"{'on-mode mean d':>15s} {'overall':>9s}   worst single book")
    for tag, lad, pk, names in [("A", ladA, pkA, nameA), ("B", ladB, pkB, nameB)]:
        for dial in DIAL_ORDER:
            offs, ons, worst = [], [], (0.0, "", "")
            for bk in names:
                row = pk[(pk.dial == dial) & (pk.book == bk)].iloc[0]
                sel = row["SEL_SHARPE"]
                pt = mode_pick(tag, dial, bk, "MODE-LOO", pk)
                dd = (score_of(tag, dial, bk, pt, "OOS_Sharpe")
                      - score_of(tag, dial, bk, sel, "OOS_Sharpe"))
                (ons if pt == sel else offs).append(dd)
                if pt != sel and dd > worst[0]:
                    worst = (dd, bk, f"{sel} -> {pt}")
            allv = offs + ons
            P(f"  {tag:7s} {dial:8s} {len(ons)/len(allv):7.1%} {len(offs):6d} "
              f"{(np.mean(offs) if offs else np.nan):+16.4f} "
              f"{(np.mean(ons) if ons else 0.0):+15.4f} {np.mean(allv):+9.4f}   "
              f"{worst[1]} {worst[2]} {worst[0]:+.4f}")

    # ------------------------------------------------- corpus split-half validation
    P("\n" + "=" * 118)
    P("Q5  IS THE MODE ITSELF STABLE?  Split each corpus into two seeded halves, read the mode")
    P("    on one half and score it on the other.  This is the mode's own walk-forward.")
    P("=" * 118)
    rng = np.random.default_rng(189_500)
    P(f"  {'corpus':7s} {'dial':8s} {'mode(half1)':>12s} {'mode(half2)':>12s} {'agree':>6s} "
      f"{'mean d vs SEL on the held-out half':>36s}")
    for tag, lad, pk, names in [("A", ladA, pkA, nameA), ("B", ladB, pkB, nameB)]:
        perm = rng.permutation(len(names))
        h1 = [names[i] for i in perm[: len(names) // 2]]
        h2 = [names[i] for i in perm[len(names) // 2:]]
        for dial in DIAL_ORDER:
            s1 = pk[(pk.dial == dial) & (pk.book.isin(h1))]["SEL_SHARPE"].value_counts()
            s2 = pk[(pk.dial == dial) & (pk.book.isin(h2))]["SEL_SHARPE"].value_counts()
            m1, m2 = s1.index[0], s2.index[0]
            d = []
            for bk, mo in [(b, m1) for b in h2] + [(b, m2) for b in h1]:
                sel = pk[(pk.dial == dial) & (pk.book == bk)]["SEL_SHARPE"].iloc[0]
                d.append(score_of(tag, dial, bk, mo, "OOS_Sharpe")
                         - score_of(tag, dial, bk, sel, "OOS_Sharpe"))
            P(f"  {tag:7s} {dial:8s} {str(m1):>12s} {str(m2):>12s} "
              f"{'YES' if m1 == m2 else 'NO':>6s} {np.mean(d):+36.4f}")

    # ------------------------------------------------------------------ Q6 rule 8 + KEEP
    P("\n" + "=" * 118)
    P("Q6  RULE 8 and BOTH KEEP PATHS.  Every pick above is made on <= 2016-12-31 and the")
    P("    2017-01-01 -> window is read ONCE.  Absolute OOS levels per arm, against RULES v1")
    P("    and SPY on each book's parent panel.")
    P("=" * 118)
    wf = []
    for tag, lad, pk, names in [("A", ladA, pkA, nameA), ("B", ladB, pkB, nameB)]:
        for dial in DIAL_ORDER:
            for arm in ["SEL-SHARPE", "SEL-4B", "CONST-INC", "RANDOM", "ORACLE"] + MODE_ARMS:
                rows_ = []
                for bk in names:
                    row = pk[(pk.dial == dial) & (pk.book == bk)].iloc[0]
                    pt = {"SEL-SHARPE": row["SEL_SHARPE"], "SEL-4B": row["SEL_4B"],
                          "CONST-INC": INC[dial], "RANDOM": row["RANDOM"],
                          "ORACLE": row["ORACLE"]}.get(
                              arm, None)
                    if pt is None:
                        pt = mode_pick(tag, dial, bk, arm, pk)
                    rows_.append(row_of(tag, dial, bk, pt))
                R = pd.DataFrame(rows_)
                wf.append(dict(corpus=tag, dial=dial, arm=arm, n=len(R),
                               OOS_Sharpe=float(R.OOS_Sharpe.mean()),
                               OOS_CAGR=float(R.OOS_CAGR.mean()),
                               OOS_MaxDD=float(R.OOS_MaxDD.mean()),
                               OOS_margin=float(R.OOS_margin.mean()),
                               pass4a=int((R.fail4a == "-").sum()),
                               pass4b=int((R.fail4b == "-").sum())))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n  mean OOS level per arm, pooled over the five dials:")
    P(WF.groupby(["corpus", "arm"]).agg(
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), OOS_margin=("OOS_margin", "mean"),
        pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"))
      .sort_values(["corpus", "OOS_Sharpe"], ascending=[True, False])
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  per dial and arm:")
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  BENCHMARKS on the same OOS window:")
    bm = []
    for tag, SPYd, BASEd in [("A", SPYA, BASEA), ("B", SPYB, BASEB)]:
        for pan in SPYd:
            for nm, s in [("SPY", SPYd[pan]), ("RULES v1 @10bps", BASEd[pan])]:
                mo = metrics(s.loc[OOS_START:])
                bm.append(dict(corpus=tag, parent=pan, series=nm, OOS_CAGR=mo["CAGR"],
                               OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    P(pd.DataFrame(bm).drop_duplicates().to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))

    P(f"\n  BOTH KEEP PATHS over all {len(LAD)} ladder rows: 4a "
      f"{int((LAD.fail4a == '-').sum())}, 4b {int((LAD.fail4b == '-').sum())}")
    P(LAD.assign(p4a=LAD.fail4a == "-", p4b=LAD.fail4b == "-")
      .groupby(["corpus", "parent"]).agg(rows=("p4a", "size"), pass4a=("p4a", "sum"),
                                         pass4b=("p4b", "sum")).to_string())
    k4b = LAD[LAD.fail4b == "-"]
    if len(k4b):
        P("\n  every 4b pass (idea 144: a re-dialled book is the same book; nothing is proposed):")
        P(k4b[["corpus", "book", "dial", "point", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_Sharpe"]].head(40).to_string(index=False,
                                                 float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    loA = PR[(PR.corpus == "A") & (PR.arm == "MODE-LOO") & (PR.score == "OOS_Sharpe")]
    won5 = int((loA["mean_d"] > 0).sum())
    cad = float(loA[loA.dial == "CADENCE"]["mean_d"].iloc[0])
    agree_ge_half = int((loA["agree_share"] > 0.5).sum())
    off_neg = int((loA["off_mean_d"] > 0).sum())          # arm - sel > 0 means SEL loses
    n4b = int((LAD.fail4b == "-").sum())
    preds = [
        ("P1 idea 171's ladder and headline reproduce", repro, f"max |d| {dmax:.1e}, {v4} verdict mismatches"),
        ("P2 CADENCE: MODE-LOO beats SEL-SHARPE on corpus A", cad > 0, f"{cad:+.4f}"),
        ("P3 MODE-LOO beats SEL-SHARPE on 5 of 5 dials (corpus A, OOS Sharpe)", won5 == 5,
         f"{won5}/5"),
        ("P4 selector agrees with its own mode >50% on >=3 of 5 dials", agree_ge_half >= 3,
         f"{agree_ge_half}/5"),
        ("P5 off-mode: SEL-SHARPE loses on all 5 dials", off_neg == 5, f"{off_neg}/5"),
        ("P6 no arm produces a 4b KEEP on either corpus", n4b == 0, f"{n4b} 4b passes among ladder rows"),
    ]
    for nm, hit, det in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:<62s} {det}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
