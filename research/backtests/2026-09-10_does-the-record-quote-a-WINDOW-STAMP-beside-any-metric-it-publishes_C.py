#!/usr/bin/env python3
"""QUEUE idea 667 — does-the-record-quote-a-WINDOW-STAMP-beside-any-metric-it-publishes
(lane C, 2026-09-10).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 667, written before any number here was read)
    "idea 664 measured the pooled WINDOW bar for Sharpe at 0.0355 (p90 0.098-0.137), LARGER than
     the between-book bar of 0.0235, and found the CHANGELOG's own 2026-09-08 RULES v2 row differs
     from today's by dSharpe 0.0035 on two extra trading days.  Census how many committed metric
     columns carry a start/end/asof stamp at all, and re-price the record's published Sharpe
     comparisons at the stamp's absence.  Max 2 params (stamp form, metric)."

WHY IT MATTERS
    Every KEEP/KILL sentence in this record is a COMPARISON of two published numbers.  A comparison
    is only decidable if both numbers were measured on the SAME window.  If the artefacts do not
    say what window they were measured on, then a reader — including the next run, including the
    Sunday review — cannot tell a real difference from a difference in where the sample started
    and stopped.  Idea 664 already showed the within-book cross-window spread of Sharpe EXCEEDS
    the between-book spread on this corpus.  This run asks the prior question: is the window ever
    written down?  And then prices the consequence: how many of the record's published metric
    distinctions are finer than what an unstamped window change alone can produce?

A CORRECTION TO 664, MADE BEFORE ANY NEW NUMBER WAS READ (this is method, not a result)
    Idea 664's WINDOW family is NOT a pure window family.  Its 14 variants mix six COST rungs and
    three CADENCES in with the span variants (see its yardsticks(), lines 490-505).  A cost rung is
    not a window: two runs at 0 and 50 bps are different BOOKS priced differently, and a reader who
    knows the rung is not missing a window stamp.  So 664's "window bar" is an upper bound on the
    thing idea 667 needs.  This run measures the PURE-SPAN bar — same book, same cost, same cadence,
    ONLY the (start, end) of the evaluated slice moves — and reports 664's contaminated construction
    beside it as a named contrast.  The pure bar is the honest price of a missing stamp.

WHAT IS BEING TESTED (six analyses, all fixed in advance)
    A0  SCOPE.  Corpus size and the metric-column inventory.  DECLARED NOT BLIND: a header-name
        frequency pass over the 3,101 committed CSVs was run before the predictions below were
        written, to choose the stamp lexicon.  It is reproduced here as A0 so the reader sees
        exactly what was known when P1 was written.
    A1  THE CENSUS (the queue's literal first ask).  For every committed artefact that PUBLISHES
        metric M, does it carry a window stamp under form F?  All 4 forms x 4 metrics reported.
    A2  THE PURE-SPAN BAR (live).  Same book, same rung, same cadence; only the slice moves.
        Two channels reported apart and pooled:
          END   — the cache grows: drop the last k trading days, k in {0,1,2,3,5,10,21,63}.
                  This is the CHANGELOG's own 2026-09-08-vs-today channel, generalised.
          START — the warm-up convention: index[252] / index[260] (the house default) / index[300]
                  / first trading day of 2010 / of 2011.
        Contrasts: 664's CONTAMINATED window family (span + cost rungs + cadences) and the BOOK
        bar (different books, SAME slice) — the bar a reader actually wants to resolve.
    A3  THE RE-PRICING (the queue's literal second ask).  Three populations of published
        comparison, re-priced against A2's pure-span bar, weakest evidence first:
          A3a ADJACENT   within-file adjacent-value gaps of a metric column.  DECLARED WEAK —
                         adjacent gaps shrink with row count by construction, so the pooled
                         share is dominated by the biggest grids; a per-file median is reported
                         beside it and neither is treated as the answer.
          A3b COMPARAND  within-ROW gaps between an arm metric and its own comparand column
                         (spy_/v1_/v2_/base_/twin_/ctrl_...).  Both sides share a window BY
                         CONSTRUCTION, so this is the INTERNAL CONTROL: the population the
                         missing stamp does not endanger.
          A3c DELTA      the record's explicit d<metric> columns.  A delta column IS a published
                         comparison in the metric's own units, and its window is stamped only if
                         its file is.  THIS IS THE HEADLINE POPULATION.
        Each split by whether the publishing file is stamped under form F.
    A4  WHICH BAR THE STAMP MOVES.  For every panel x book x rung, the five 4b margins re-read on
        every span variant, and a count of 4b/4a verdict FLIPS caused by the span alone.
    A5  RULE 8 (PROTOCOL 8, required).  Dial chosen on 2009-2016 ALONE, 2017-2026 read ONCE, under
        the TRUE IS window and under each DRIFTED IS window.  Pick-flip rate, OOS Sharpe cost of
        the flips, OOS CAGR/Sharpe/MaxDD vs the LIVE RULES v2 book and vs SPY, regret vs the
        IS-window oracle.  Both KEEP paths on every arm at every rung.

TUNED PARAMETERS — exactly two, per PROTOCOL 4:
    P1  stamp form   ROWSPAN / ROWANY / FILEHEAD / FILENAME   (4 values, ALL reported)
    P2  metric       Sharpe / CAGR / MaxDD / OOS_Sharpe       (4 values, ALL reported)
    Panels, books, cost rungs, the span grid, both selectors and both KEEP paths are reported
    axes, never selected on.

STAMP FORMS (fixed before the census ran; each is a strictly more permissive reading)
    ROWSPAN   a per-row window stamp: a start-column AND an end-column, or an asof column.
              The only form under which a reader can date an individual published number.
    ROWANY    any per-row column in the stamp lexicon (start|end|asof|date|window|span|nobs|
              n_days|years|yrs|period|sample|vintage).  Deliberately over-permissive: `window`
              in this record usually names a 4b bar-window, not a date, so ROWANY over-counts
              on purpose, to bound the census from above.
    FILEHEAD  a FILE-level stamp: the artefact, its sibling .console.txt, its sibling .py or its
              sibling memo states an explicit date span (YYYY-MM-DD..YYYY-MM-DD) or a year span
              (YYYY-YYYY) anywhere in its text.  Dates the FILE, not the row.
    FILENAME  the filename carries a date.  This dates the RUN, not the SAMPLE, and is reported
              only to show that the record's near-universal "stamp" is the wrong stamp.

KEEP PATHS (PROTOCOL 4, evaluated on every arm x rung x span variant)
    4a  vs the LIVE book `baseline.rules_v2_weights` on the same panel, cost-matched:
        Sharpe > baseline in BOTH halves AND MaxDD no worse.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

PRE-REGISTERED PREDICTIONS (written before A1-A5 were run; P1 is informed by the A0 scoping pass
and says so)
    Q1  Under ROWSPAN fewer than 3% of Sharpe-publishing CSVs carry a stamp.  (Informed: the A0
        pass had already shown `start` 17 / `end` 15 header occurrences over 3,101 files.)
    Q2  Under FILENAME essentially all of them do — i.e. the record stamps the RUN date almost
        universally and the SAMPLE window almost never.  The gap between those two numbers is
        the finding.
    Q3  The PURE-span Sharpe bar is materially SMALLER than 664's contaminated 0.0355, because
        cost rungs and cadences are doing most of that work; but it is still larger than the
        p10 of the between-book bar, so it is not negligible.
    Q4  More than 25% of the record's explicit published Sharpe DELTAS (A3c) are smaller in
        absolute value than the pure-span p50 bar, and the A3b control sits materially lower —
        i.e. the exposure is in the deltas the record publishes, not in an artefact of counting.
    Q5  Span drift flips rule-8 picks in a non-trivial share of cells and the flips cost ~0 OOS
        Sharpe on average — window noise moves the choice without informing it.
    Q6  No arm KEEPs on either path because of anything in this run: the stamp is a REPORTING
        defect, not a rule.  Any 4b passes found are inherited from the standing candidate family.

GATES (pre-registered, run before any A1-A5 number is read)
    G1  the vectorised runner reproduces `engine.backtest` returns AND turnover.
    G2  the cost identity r(c) = r0 - turnover*c/1e4 is exact, so every rung below is exact.
    G3  `band_book(0.03, 0.75)` == `baseline.rules_v2_weights` exactly (the live book is the
        live book).
    G4  END-DRIFT EQUIVALENCE: truncating the PANEL by k trading days and re-running == slicing
        the full-sample return series, up to the final-week rebalance-mask edge.  The residual
        is reported, not assumed away — it is the exact size of the approximation A2 uses for
        the arms it does not re-run.
    G5  THE CHANGELOG DATUM: the queue quotes dSharpe 0.0035 between the CHANGELOG's 2026-09-08
        RULES v2 U56 row (8.66% / 1.2056 / H 1.2259/1.1909) and idea 664's same-day row
        (8.63% / 1.2021 / H 1.2309/1.1798) on two extra trading days.  Reproduce it by truncating
        today's cache.  This gate tests the MECHANISM the whole idea rests on.
    G6  the census partition is exact: STAMPED + UNSTAMPED == N at all 16 grid points.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): all three panels are current constituents; SMALL439 worst.
    * The corpus is this repository's committed artefacts only.  A file that states its window in
      prose the regexes do not match is scored UNSTAMPED; FILEHEAD is deliberately loose to bound
      that error from above, and the ROWSPAN/FILEHEAD gap brackets it.
    * ROWANY over-counts on purpose (`window` is usually not a date here).  Stated, not hidden.
    * `data/prices.csv` is re-downloaded daily with auto-adjusted closes (idea 406/399): U56 rows
      in this record reproduce to ~1e-5, not bit-exactly.  G5's residual therefore mixes the
      end-drift channel with the restatement channel, and the run says so where it matters.
    * MaxDD is one number off one path (idea 321); a span change can move it discontinuously.
    * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
    * A0's header pass was run before the predictions.  Declared above.

Deterministic, standalone, modifies nothing outside its own output files.  Writes
.console.txt, .census.csv, .yardstick.csv, .reprice.csv, .walkforward.csv,
.keeppaths.csv next to itself.
"""
import csv
import glob
import os
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask              # noqa: E402

STEM = "2026-09-10_does-the-record-quote-a-WINDOW-STAMP-beside-any-metric-it-publishes_C"
OUT = ROOT / "research" / "backtests"

FREQ, GROSS, BAND0, NTOP = "W", 0.75, 0.03, 20
WARM = 260                                          # the house warm-up convention
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60                             # 4b CAGR floor / DD cap vs SPY
RUNGS = [0.0, 10.0, 25.0]
PANELS = ["U56", "B136", "SMALL439"]

# ---- tuned parameter 1: stamp form (4 values, all reported)
FORMS = ["ROWSPAN", "ROWANY", "FILEHEAD", "FILENAME"]
# ---- tuned parameter 2: metric (4 values, all reported)
METRICS4 = ["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe"]

# ---- the span grid (reported axis, never selected on)
ENDS = [0, 1, 2, 3, 5, 10, 21, 63]                  # trading days dropped off the tail
STARTS = [("W252", 252), ("W260", 260), ("W300", 300), ("Y2010", "2010-01-01"),
          ("Y2011", "2011-01-01")]
CONTAM_RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]   # 664's construction, for the contrast
CONTAM_CADS = ["D", "W", "M"]

# ---- rule-8 dials (reported axis)
DIALS = {
    "band":  ("BAND",  [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]),
    "n":     ("TOPN",  [5, 10, 20, 30, 40, 50]),
    "gross": ("EWALL", [0.50, 0.65, 0.75, 0.85, 1.00]),
}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, tag):
    p = OUT / f"{STEM}.{tag}.csv"
    df.to_csv(p, index=False)
    P(f"  [written] {p.name}  ({len(df):,} rows)")


# =================================================================================================
# 0.  BOOKS AND RUNNER
# =================================================================================================
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def band_book(px, band=BAND0, gross=GROSS):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def topn_book(px, n=NTOP, gross=GROSS):
    """The 2026-09-04 KEEP 4b family: top-n composite, EQUAL WEIGHT, NO vol scaler."""
    rank = composite(px).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def ewall_book(px, gross=GROSS):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def make_book(kind, level, px):
    if kind == "BAND":
        return band_book(px, level, GROSS)
    if kind == "TOPN":
        return topn_book(px, int(level), GROSS)
    if kind == "EWALL":
        return ewall_book(px, level)
    raise ValueError(kind)


def fast_run(px, W, freq=FREQ):
    """engine.backtest at ZERO cost, returning (r0, turnover).  Every rung is derived exactly
    from these two series by the identity gated in G2."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k)
    held = np.zeros((n, k))
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = tgt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index))


def at_cost(r0, to, c):
    return r0 - to * c / 1e4


def M(r):
    """The metric vector of one return slice.  Guards degenerate slices."""
    if len(r) < 30:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan)
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# =================================================================================================
# 1.  THE CENSUS  (A0 / A1)
# =================================================================================================
DATESPAN = re.compile(r"((?:19|20)\d\d[-/]\d\d?[-/]\d\d?)\s*(?:\.\.|--|-|–|—|to|through|thru)\s*"
                      r"((?:19|20)\d\d[-/]\d\d?[-/]\d\d?)")
YEARSPAN = re.compile(r"\b(?:19|20)\d\d\s*[-–—]\s*(?:19|20)\d\d\b")
FNDATE = re.compile(r"(?:19|20)\d\d-\d\d-\d\d")

START_COLS = {"start", "start_date", "startdate", "begin", "win_start", "is_start", "oos_start",
              "first_day", "t0", "date_start", "sample_start", "eval_start"}
END_COLS = {"end", "end_date", "enddate", "win_end", "is_end", "oos_end", "last_day",
            "date_end", "sample_end", "eval_end"}
ASOF_COLS = {"asof", "as_of", "vintage", "asof_date", "as_of_date"}
ANY_STAMP = re.compile(r"(?:^|_)(date|asof|as_of|window|span|nobs|n_days|ndays|years|yrs|nyears|"
                       r"period|sample|vintage|start|end)(?:$|_)", re.I)

METRIC_TOK = {
    "Sharpe":     lambda toks: "sharpe" in toks,
    "CAGR":       lambda toks: "cagr" in toks,
    "MaxDD":      lambda toks: "maxdd" in toks,
    "OOS_Sharpe": lambda toks: ("sharpe" in toks and "oos" in toks),
}


def toks_of(col):
    return set(re.split(r"[^A-Za-z0-9]+", str(col).strip().lower())) - {""}


def read_header(f):
    try:
        with open(f, newline="", errors="replace") as fh:
            return [c.strip() for c in next(csv.reader(fh))]
    except Exception:
        return None


def sibling_text(f):
    """Text of the artefact's own family: its .console.txt, its .py, its .result.md / memo."""
    base = re.sub(r"\.[a-zA-Z0-9_]+\.csv$", "", f)
    base = re.sub(r"\.csv$", "", base)
    out = []
    for cand in (base + ".console.txt", base + ".py", base + ".result.md", base + ".md"):
        if os.path.exists(cand):
            try:
                out.append(open(cand, errors="replace").read(400_000))
            except Exception:
                pass
    return "\n".join(out)


def census():
    P()
    P("=" * 100)
    P("A0  SCOPE  (declared NOT blind: this header pass was run before the predictions)")
    P("=" * 100)
    own = lambda f: os.path.basename(f).startswith(STEM)
    csvs = [f for f in sorted(glob.glob(str(OUT / "*.csv"))) if not own(f)]
    mds = [f for f in sorted(glob.glob(str(OUT / "*.md"))) if not own(f)]
    txts = [f for f in sorted(glob.glob(str(OUT / "*.console.txt"))) if not own(f)]
    P("  (this run's own artefacts are excluded from its own corpus, so a re-run is idempotent)")
    P(f"  committed artefacts under research/backtests: {len(csvs):,} csv, {len(mds):,} md, "
      f"{len(txts):,} console.txt")

    hdrs, colcount = {}, {}
    for f in csvs:
        h = read_header(f)
        if h is None:
            continue
        hdrs[f] = h
        for c in h:
            colcount[c] = colcount.get(c, 0) + 1
    P(f"  headers read: {len(hdrs):,} files, {len(colcount):,} distinct column names")
    stampish = {c: n for c, n in colcount.items()
                if c.strip().lower() in START_COLS | END_COLS | ASOF_COLS}
    P("  header occurrences of an EXPLICIT date-stamp column name, over the whole corpus:")
    P("    " + (", ".join(f"{c} {n}" for c, n in sorted(stampish.items(), key=lambda x: -x[1]))
                or "(none)"))

    P()
    P("=" * 100)
    P("A1  THE CENSUS — does an artefact that PUBLISHES metric M carry a window stamp under form F?")
    P("=" * 100)
    rows = []
    percell = {}
    sib_cache = {}
    for f, h in hdrs.items():
        tk = [toks_of(c) for c in h]
        low = [c.strip().lower() for c in h]
        has_start = any(c in START_COLS or c.endswith("_start") for c in low)
        has_end = any(c in END_COLS or c.endswith("_end") for c in low)
        has_asof = any(c in ASOF_COLS or c.endswith("_asof") for c in low)
        rowspan = (has_start and has_end) or has_asof
        rowany = rowspan or any(ANY_STAMP.search(c) for c in low)
        fn = os.path.basename(f)
        filename = bool(FNDATE.search(fn))
        st = sib_cache.get(f)
        if st is None:
            st = sibling_text(f)
            sib_cache[f] = st
        filehead = bool(DATESPAN.search(st) or YEARSPAN.search(st))
        flags = dict(ROWSPAN=rowspan, ROWANY=rowany, FILEHEAD=filehead, FILENAME=filename)
        for m, test in METRIC_TOK.items():
            cols = [h[i] for i in range(len(h)) if test(tk[i])]
            if not cols:
                continue
            for form in FORMS:
                key = (form, m)
                d = percell.setdefault(key, dict(N=0, S=0))
                d["N"] += 1
                d["S"] += int(flags[form])
            rows.append(dict(file=fn, metric=m, ncols=len(cols),
                             cols=";".join(cols[:6]), **{k: int(v) for k, v in flags.items()}))
    C = pd.DataFrame(rows)
    tab = []
    for form in FORMS:
        for m in METRICS4:
            d = percell.get((form, m), dict(N=0, S=0))
            tab.append(dict(form=form, metric=m, N=d["N"], stamped=d["S"],
                            unstamped=d["N"] - d["S"],
                            share=d["S"] / d["N"] if d["N"] else np.nan))
    T = pd.DataFrame(tab)
    P(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok = bool(((T.stamped + T.unstamped) == T.N).all())
    P(f"  [G6] census partition exact at all {len(T)} grid points: {ok}")
    assert ok

    # ---- the same census on the two PROSE artefacts the record actually reads from
    P()
    P("  PROSE artefacts (LEADERBOARD.md rows and CHANGELOG.md entries) — same question:")
    for name in ("LEADERBOARD.md", "CHANGELOG.md"):
        t = (ROOT / "research" / name).read_text(errors="replace")
        lines = [l for l in t.split("\n") if l.strip().startswith("|") or l.strip().startswith("-")]
        pub = [l for l in lines if re.search(r"sharpe", l, re.I)]
        ds = sum(1 for l in pub if DATESPAN.search(l))
        ys = sum(1 for l in pub if YEARSPAN.search(l))
        P(f"    {name}: {len(pub):,} rows/entries that publish a Sharpe; "
          f"{ds:,} ({ds/max(len(pub),1):.1%}) carry a full DATE span, "
          f"{ys:,} ({ys/max(len(pub),1):.1%}) carry a YEAR span, "
          f"{len(pub)-max(ds,ys):,} carry neither.")
    P("    NOTE: a YEAR span ('2017-2026') does not date a number to a trading day, which is the "
      "resolution the END channel of A2 moves on.  It is counted, and its weakness is priced in A3.")
    dump(C, "census")
    return C, T


# =================================================================================================
# 2.  THE LIVE YARDSTICKS  (A2)
# =================================================================================================
def slices_of(r, px_index):
    """The 40-point pure-span grid: 5 start conventions x 8 end truncations, same book/rung/cadence."""
    out = {}
    for sname, s in STARTS:
        s0 = px_index[s] if isinstance(s, int) else pd.Timestamp(s)
        for k in ENDS:
            rr = r.loc[s0:]
            if k:
                rr = rr.iloc[:-k]
            out[(sname, k)] = rr
    return out


def pairgaps(vals):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if len(v) < 2:
        return np.array([])
    d = np.abs(v[:, None] - v[None, :])
    return d[np.triu_indices(len(v), 1)]


def yardsticks(PX, SIMS):
    P()
    P("=" * 100)
    P("A2  THE PURE-SPAN BAR — same book, same rung, same cadence; ONLY the slice moves")
    P("=" * 100)
    rows = []
    bars = {}
    for pk in PANELS:
        px = PX[pk]["px"]
        for book in ("BAND", "TOPN", "EWALL"):
            r0, to = SIMS[(pk, book, "base")]
            r = at_cost(r0, to, 10.0)
            sl = slices_of(r, px.index)
            vm = {k: M(v) for k, v in sl.items()}
            # -- END channel only, at the house start
            for mname in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
                g_end = pairgaps([vm[("W260", k)][mname] for k in ENDS])
                g_sta = pairgaps([vm[(s, 0)][mname] for s, _ in STARTS])
                g_all = pairgaps([vm[k][mname] for k in vm])
                for kind, g in (("END", g_end), ("START", g_sta), ("PURE", g_all)):
                    if len(g) == 0:
                        continue
                    rows.append(dict(panel=pk, book=book, kind=kind, metric=mname, n=len(g),
                                     p10=np.percentile(g, 10), p50=np.percentile(g, 50),
                                     p90=np.percentile(g, 90), pmax=g.max()))
        # -- 664's CONTAMINATED construction, reproduced as the named contrast (BAND book)
        r0, to = SIMS[(pk, "BAND", "base")]
        variants = {f"cost{int(c)}": at_cost(r0, to, c).loc[px.index[WARM]:] for c in CONTAM_RUNGS}
        for cad in CONTAM_CADS:
            rr, tt = SIMS[(pk, "BAND", f"cad{cad}")]
            variants[f"cad{cad}"] = at_cost(rr, tt, 10.0).loc[px.index[WARM]:]
        r10 = at_cost(r0, to, 10.0)
        for nm, off in (("warm252", 252), ("warm300", 300), ("warm0", 0)):
            variants[nm] = r10.loc[px.index[off]:]
        base10 = r10.loc[px.index[WARM]:]
        variants["IS"] = base10.loc[:IS_END]
        variants["OOS"] = base10.loc[OOS_START:]
        variants["H1"] = base10.iloc[:len(base10) // 2]
        variants["H2"] = base10.iloc[len(base10) // 2:]
        variants["last5y"] = base10.iloc[-1260:]
        vm = {k: M(v) for k, v in variants.items()}
        for mname in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
            g = pairgaps([vm[k][mname] for k in vm])
            rows.append(dict(panel=pk, book="BAND", kind="CONTAM664", metric=mname, n=len(g),
                             p10=np.percentile(g, 10), p50=np.percentile(g, 50),
                             p90=np.percentile(g, 90), pmax=g.max()))
        # -- BOOK bar: different books, SAME slice
        bm = {}
        for book in ("BAND", "TOPN", "EWALL"):
            rr, tt = SIMS[(pk, book, "base")]
            bm[book] = M(at_cost(rr, tt, 10.0).loc[px.index[WARM]:])
        for dial, (kind, levels) in DIALS.items():
            for lv in levels:
                rr, tt = SIMS[(pk, kind, lv)]
                bm[(dial, lv)] = M(at_cost(rr, tt, 10.0).loc[px.index[WARM]:])
        for mname in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
            g = pairgaps([bm[k][mname] for k in bm])
            rows.append(dict(panel=pk, book="ALL", kind="BOOK", metric=mname, n=len(g),
                             p10=np.percentile(g, 10), p50=np.percentile(g, 50),
                             p90=np.percentile(g, 90), pmax=g.max()))
    Y = pd.DataFrame(rows)
    P(Y.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    P()
    for kind in ("END", "START", "PURE", "CONTAM664", "BOOK"):
        s = Y[Y.kind == kind].groupby("metric")[["p50", "p90"]].mean()
        bars[kind] = {m: dict(p50=s.loc[m, "p50"], p90=s.loc[m, "p90"]) for m in s.index}
        P(f"  {kind:10s} bar (pooled mean of per-cell p50 | p90): " +
          ", ".join(f"{m} {s.loc[m,'p50']:.6f}|{s.loc[m,'p90']:.6f}" for m in
                    ("CAGR", "Sharpe", "MaxDD", "H1", "H2")))
    P()
    P(f"  664 published a pooled WINDOW Sharpe bar of 0.0355 (p90 0.098-0.137).  Reproduced here "
      f"as CONTAM664 = {bars['CONTAM664']['Sharpe']['p50']:.4f} "
      f"(p90 {bars['CONTAM664']['Sharpe']['p90']:.4f}).")
    P(f"  The PURE-span bar — the actual price of a missing stamp — is "
      f"{bars['PURE']['Sharpe']['p50']:.4f} (p90 {bars['PURE']['Sharpe']['p90']:.4f}); "
      f"END alone {bars['END']['Sharpe']['p50']:.4f}, START alone "
      f"{bars['START']['Sharpe']['p50']:.4f}.")
    P(f"  The BOOK bar (what a reader is trying to resolve) is "
      f"{bars['BOOK']['Sharpe']['p50']:.4f} (p90 {bars['BOOK']['Sharpe']['p90']:.4f}).")
    dump(Y, "yardstick")
    return Y, bars


# =================================================================================================
# 3.  RE-PRICE THE RECORD'S PUBLISHED COMPARISONS  (A3)
# =================================================================================================
DELTA_COL = re.compile(r"^(d|delta|diff|gap)_?(oos_?)?(sharpe|cagr|maxdd|dd)$", re.I)
COMPARAND = re.compile(r"^(spy|v1|v2|base|bl|live|ctrl|control|twin|ref|bench|null|placebo|"
                       r"block|parent|incumbent)_", re.I)


def _metric_of(col):
    tk = toks_of(col)
    if "sharpe" in tk:
        return "OOS_Sharpe" if "oos" in tk else "Sharpe"
    if "cagr" in tk:
        return "CAGR"
    if "maxdd" in tk:
        return "MaxDD"
    return None


def _delta_metric(col):
    m = DELTA_COL.match(str(col).strip())
    if not m:
        return None
    base = m.group(3).lower()
    if base in ("maxdd", "dd"):
        return "MaxDD"
    if base == "cagr":
        return "CAGR"
    return "OOS_Sharpe" if m.group(2) else "Sharpe"


def reprice(C, bars):
    P()
    P("=" * 100)
    P("A3  RE-PRICING THE RECORD\'S PUBLISHED COMPARISONS AT THE STAMP\'S ABSENCE")
    P("=" * 100)
    P("  A published COMPARISON is only decidable if both numbers share a window.  Three")
    P("  populations of comparisons are re-priced against the PURE-SPAN bar of A2, weakest")
    P("  evidence first, and all three are reported:")
    P("    A3a ADJACENT   the within-file adjacent-value gaps of a metric column — the finest")
    P("                   distinction a file draws.  DECLARED WEAK: adjacent gaps shrink with row")
    P("                   count by construction, so the pooled share is dominated by the largest")
    P("                   grids.  Reported with a per-file median beside it for that reason.")
    P("    A3b COMPARAND  within-ROW gaps between an arm metric and its own comparand column in")
    P("                   the same row (spy_/v1_/v2_/base_/twin_/ctrl_...).  These are comparisons")
    P("                   the record makes explicitly, and both sides share a window BY")
    P("                   CONSTRUCTION — so this population is the one the stamp does NOT")
    P("                   endanger.  It is the internal control.")
    P("    A3c DELTA      the record\'s explicit d<metric> columns (dSharpe, dCAGR, dMaxDD ...).")
    P("                   A delta column IS a published comparison, in the metric\'s own units.")
    P("                   Its own window is stamped only if its file is.  THIS IS THE HEADLINE.")
    P("  Exact zeros are EXCLUDED from every population: a published delta of exactly 0.0 is not")
    P("  a distinction being drawn, and counting it would inflate every share below.")
    files = sorted(C.file.unique())
    ZEROS = {"COMPARAND": 0, "DELTA": 0}
    rows_adj, rows_cmp, rows_dlt = [], [], []
    skipped = 0
    flagmap = (C.drop_duplicates("file").set_index("file")[FORMS].to_dict("index"))
    for fn in files:
        f = str(OUT / fn)
        hdr = read_header(f)
        if hdr is None:
            skipped += 1
            continue
        want, mcol, dcol = [], {}, {}
        for c in hdr:
            dm = _delta_metric(c)
            if dm:
                dcol[c] = dm
                want.append(c)
                continue
            mm = _metric_of(c)
            if mm:
                mcol[c] = mm
                want.append(c)
        if not want:
            continue
        try:
            d = pd.read_csv(f, usecols=list(dict.fromkeys(want)), low_memory=False)
        except Exception:
            skipped += 1
            continue
        fl = flagmap.get(fn, {k: 0 for k in FORMS})
        num = {c: pd.to_numeric(d[c], errors="coerce") for c in d.columns}

        # ---- A3a adjacent gaps
        for c, m in mcol.items():
            v = num[c].dropna().values
            v = v[np.isfinite(v)]
            if len(v) < 2:
                continue
            u = np.unique(v)
            if len(u) < 2:
                continue
            g = np.diff(u)
            g = g[g > 0]
            if not len(g):
                continue
            bar = bars["PURE"]["Sharpe" if m == "OOS_Sharpe" else m]["p50"]
            rows_adj.append(dict(file=fn, metric=m, col=c, n=len(g),
                                 nlt=int((g < bar).sum()), share=float((g < bar).mean()),
                                 **{k: int(fl[k]) for k in FORMS}))

        # ---- A3b within-row comparand gaps
        for c, m in mcol.items():
            if COMPARAND.match(c):
                continue
            for c2, m2 in mcol.items():
                if c2 == c or m2 != m or not COMPARAND.match(c2):
                    continue
                if COMPARAND.sub("", c2) != COMPARAND.sub("", c) and \
                   COMPARAND.sub("", c2) != c:
                    continue
                g = (num[c] - num[c2]).abs().dropna().values
                g = g[np.isfinite(g)]
                nz0 = int((g == 0).sum())
                g = g[g > 0]
                ZEROS["COMPARAND"] += nz0
                if not len(g):
                    continue
                bar = bars["PURE"]["Sharpe" if m == "OOS_Sharpe" else m]["p50"]
                rows_cmp.append(dict(file=fn, metric=m, col=f"{c}-{c2}", n=len(g),
                                     nlt=int((g < bar).sum()), share=float((g < bar).mean()),
                                     **{k: int(fl[k]) for k in FORMS}))

        # ---- A3c explicit delta columns
        for c, m in dcol.items():
            g = num[c].abs().dropna().values
            g = g[np.isfinite(g)]
            nz0 = int((g == 0).sum())
            g = g[g > 0]
            ZEROS["DELTA"] += nz0
            if not len(g):
                continue
            b50 = bars["PURE"]["Sharpe" if m == "OOS_Sharpe" else m]["p50"]
            b90 = bars["PURE"]["Sharpe" if m == "OOS_Sharpe" else m]["p90"]
            c50 = bars["CONTAM664"]["Sharpe" if m == "OOS_Sharpe" else m]["p50"]
            rows_dlt.append(dict(file=fn, metric=m, col=c, n=len(g),
                                 nlt=int((g < b50).sum()), share=float((g < b50).mean()),
                                 share90=float((g < b90).mean()),
                                 share664=float((g < c50).mean()),
                                 med=float(np.median(g)),
                                 **{k: int(fl[k]) for k in FORMS}))
    if skipped:
        P(f"  ({skipped} files unreadable and skipped; reported, not hidden)")
    P(f"  exact zeros excluded: {ZEROS['DELTA']:,} delta values, "
      f"{ZEROS['COMPARAND']:,} comparand gaps.")

    def summarise(rows, label, extra=()):
        if not rows:
            P(f"\n  {label}: no columns of this shape in the corpus.")
            return pd.DataFrame()
        D = pd.DataFrame(rows)
        tab = []
        for m in METRICS4:
            s = D[D.metric == m]
            if not len(s):
                continue
            n = s.n.sum()
            row = dict(pop=label, metric=m, files=s.file.nunique(), cols=len(s),
                       comparisons=int(n),
                       pooled_share_lt_bar=s.nlt.sum() / n if n else np.nan,
                       perfile_median_share=float(s.share.median()))
            for e in extra:
                row[e] = float((s[e] * s.n).sum() / n) if n else np.nan
            tab.append(row)
        T = pd.DataFrame(tab)
        P(f"\n  {label}")
        P(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        return D

    A_adj = summarise(rows_adj, "A3a ADJACENT (weak: size-dominated)")
    A_cmp = summarise(rows_cmp, "A3b COMPARAND (internal control: same window by construction)")
    A_dlt = summarise(rows_dlt, "A3c DELTA columns — THE RECORD'S PUBLISHED COMPARISONS",
                      extra=("share90", "share664"))

    R = pd.concat([x.assign(pop=p2) for x, p2 in
                   ((A_adj, "ADJACENT"), (A_cmp, "COMPARAND"), (A_dlt, "DELTA"))
                   if len(x)], ignore_index=True)

    if len(A_dlt):
        P()
        P("  A3c split by whether the file publishing the delta carries a stamp:")
        tab2 = []
        for form in FORMS:
            for m in METRICS4:
                s = A_dlt[A_dlt.metric == m]
                if not len(s):
                    continue
                for st in (1, 0):
                    q = s[s[form] == st]
                    n = q.n.sum()
                    tab2.append(dict(form=form, metric=m, stamped=st, cols=len(q),
                                     comparisons=int(n),
                                     share_lt_bar=q.nlt.sum() / n if n else np.nan))
        P(pd.DataFrame(tab2).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P()
        sd = A_dlt[A_dlt.metric.isin(("Sharpe", "OOS_Sharpe"))]
        n = sd.n.sum()
        P(f"  HEADLINE: the record publishes {int(n):,} explicit Sharpe-family DELTA values across "
          f"{sd.file.nunique():,} files.")
        P(f"            {sd.nlt.sum() / n:.4f} of them are SMALLER IN ABSOLUTE VALUE than the "
          f"pure-span p50 bar,")
        P(f"            {float((sd.share90 * sd.n).sum() / n):.4f} smaller than its p90, and "
          f"{float((sd.share664 * sd.n).sum() / n):.4f} smaller than 664's contaminated bar.")
        st = A_dlt[A_dlt.ROWSPAN == 1]
        P(f"            of those files, {sd[sd.ROWSPAN == 1].file.nunique()} carry a per-row "
          f"window stamp ({len(st)} delta columns corpus-wide).")
    dump(R, "reprice")
    return R, A_dlt, A_cmp


# =================================================================================================
# 4.  WHICH BAR THE SPAN MOVES  (A4)  +  5.  RULE 8  (A5)
# =================================================================================================
def bars_of(spy_slice, spy_full):
    h = len(spy_slice) // 2
    m = metrics(spy_slice)
    return dict(s1=metrics(spy_slice.iloc[:h])["Sharpe"], s2=metrics(spy_slice.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy_full.loc[OOS_START:])["Sharpe"])


def four_b(mv, oos_sh, b):
    marg = dict(H1=mv["H1"] - b["s1"], H2=mv["H2"] - b["s2"], OOS=oos_sh - b["soos"],
                DD=DELTA * abs(b["sdd"]) - abs(mv["MaxDD"]),
                CAGR=mv["CAGR"] - PHI * b["scagr"])
    return marg, all(v > 0 for v in marg.values() if np.isfinite(v))


def four_a(mv, bv):
    return (mv["H1"] > bv["H1"]) and (mv["H2"] > bv["H2"]) and (mv["MaxDD"] >= bv["MaxDD"])


def keeppaths_and_rule8(PX, SIMS):
    P()
    P("=" * 100)
    P("A4  WHICH BAR THE SPAN MOVES — 4a/4b verdicts re-read on every span variant")
    P("=" * 100)
    krows, flips = [], []
    for pk in PANELS:
        px = PX[pk]["px"]
        pxa = PX[pk]["pxall"]
        spy_full_all = pxa["SPY"].pct_change().fillna(0.0)
        bl0, blt = SIMS[(pk, "V2LIVE", "base")]
        for dial, (kind, levels) in DIALS.items():
            for lv in levels:
                r0, to = SIMS[(pk, kind, lv)]
                for c in RUNGS:
                    r = at_cost(r0, to, c)
                    bl = at_cost(bl0, blt, c)
                    for sname, s in STARTS:
                        s0 = px.index[s] if isinstance(s, int) else pd.Timestamp(s)
                        for k in ENDS:
                            rr = r.loc[s0:]
                            bb = bl.loc[s0:]
                            sp = spy_full_all.loc[s0:]
                            if k:
                                rr, bb, sp = rr.iloc[:-k], bb.iloc[:-k], sp.iloc[:-k]
                            if len(rr) < 500:
                                continue
                            mv, bv = M(rr), M(bb)
                            oos = rr.loc[OOS_START:]
                            osh = metrics(oos)["Sharpe"] if len(oos) > 30 else np.nan
                            b4 = bars_of(sp, sp)
                            marg, p4b = four_b(mv, osh, b4)
                            p4a = four_a(mv, bv)
                            krows.append(dict(panel=pk, dial=dial, level=lv, cost=c,
                                              start=sname, dropk=k, CAGR=mv["CAGR"],
                                              Sharpe=mv["Sharpe"], MaxDD=mv["MaxDD"],
                                              H1=mv["H1"], H2=mv["H2"], OOS_Sharpe=osh,
                                              pass4a=int(p4a), pass4b=int(p4b),
                                              **{f"m_{k2}": v for k2, v in marg.items()}))
    K = pd.DataFrame(krows)
    base = K[(K.start == "W260") & (K["dropk"] == 0)].set_index(["panel", "dial", "level", "cost"])
    K["ref4a"] = [base.loc[(r.panel, r.dial, r.level, r.cost), "pass4a"] for r in K.itertuples()]
    K["ref4b"] = [base.loc[(r.panel, r.dial, r.level, r.cost), "pass4b"] for r in K.itertuples()]
    moved = K[(K.start != "W260") | (K["dropk"] != 0)]
    narm = K[["panel", "dial", "level", "cost"]].drop_duplicates().shape[0]
    P(f"  arms x rungs x span points: {len(K):,} rows ({narm} arm-rungs x "
      f"{len(STARTS) * len(ENDS)} span points)")
    P(f"  4a passes at the house span (W260, drop 0): {int(base.pass4a.sum())} of {len(base)}")
    P(f"  4b passes at the house span (W260, drop 0): {int(base.pass4b.sum())} of {len(base)}")
    nb_both = int(((base.pass4a == 1) & (base.pass4b == 1)).sum())
    P(f"  BOTH paths at the house span: {nb_both} of {len(base)}")
    P(f"  VERDICT FLIPS caused by the SPAN ALONE (same book, same rung, same cadence):")
    P(f"    4a: {int((moved.pass4a != moved.ref4a).sum()):,} of {len(moved):,} "
      f"({(moved.pass4a != moved.ref4a).mean():.4f})")
    P(f"    4b: {int((moved.pass4b != moved.ref4b).sum()):,} of {len(moved):,} "
      f"({(moved.pass4b != moved.ref4b).mean():.4f})")
    for ch, sel in (("END only  (start=W260)", moved[moved.start == "W260"]),
                    ("START only (drop=0)   ", moved[moved["dropk"] == 0])):
        if len(sel):
            P(f"    {ch}: 4a {(sel.pass4a != sel.ref4a).mean():.4f}, "
              f"4b {(sel.pass4b != sel.ref4b).mean():.4f}  (n {len(sel):,})")
    fb = (moved.assign(f4b=(moved.pass4b != moved.ref4b).astype(int))
          .groupby('dropk').f4b.mean())
    P("    4b flip rate by trading days dropped: " +
      ", ".join(f"k={int(k)} {v:.4f}" for k, v in fb.items()))
    P()
    P("  which 4b bar is nearest to flipping at the house span (min |margin| over the five bars):")
    bb = base.reset_index()
    nb = bb[["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"]].abs().idxmin(axis=1)
    P("    " + ", ".join(f"{k} {v}" for k, v in nb.value_counts().items()))
    dump(K, "keeppaths")

    # ------------------------------------------------------------------ A5  RULE 8
    P()
    P("=" * 100)
    P("A5  RULE 8 — dial chosen on 2009-2016 ALONE, 2017-2026 read ONCE, under TRUE and DRIFTED")
    P("    IS windows.  The question: does an unstamped IS window change the PICK, and does it")
    P("    change the OOS RESULT?")
    P("=" * 100)
    wrows = []
    for pk in PANELS:
        px = PX[pk]["px"]
        pxa = PX[pk]["pxall"]
        spy = pxa["SPY"].pct_change().fillna(0.0)
        bl0, blt = SIMS[(pk, "V2LIVE", "base")]
        for dial, (kind, levels) in DIALS.items():
            for c in RUNGS:
                rs = {lv: at_cost(*SIMS[(pk, kind, lv)], c) for lv in levels}
                bl = at_cost(bl0, blt, c)
                oos_sh = {lv: metrics(rs[lv].loc[OOS_START:])["Sharpe"] for lv in levels}
                oracle = max(levels, key=lambda lv: oos_sh[lv])
                for sname, s in STARTS:
                    s0 = px.index[s] if isinstance(s, int) else pd.Timestamp(s)
                    is_days = px.index[(px.index >= s0) & (px.index <= pd.Timestamp(IS_END))]
                    if len(is_days) < 500:
                        continue
                    for k in ENDS:
                        end = is_days[-1 - k] if k < len(is_days) else is_days[0]
                        issh = {lv: metrics(rs[lv].loc[s0:end])["Sharpe"] for lv in levels}
                        pick = max(levels, key=lambda lv: issh[lv])
                        o = rs[pick].loc[OOS_START:]
                        mo = metrics(o)
                        wrows.append(dict(
                            panel=pk, dial=dial, cost=c, start=sname, dropk=k, pick=pick,
                            IS_Sharpe=issh[pick], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                            OOS_MaxDD=mo["MaxDD"],
                            base_OOS_Sharpe=metrics(bl.loc[OOS_START:])["Sharpe"],
                            base_OOS_CAGR=metrics(bl.loc[OOS_START:])["CAGR"],
                            base_OOS_MaxDD=metrics(bl.loc[OOS_START:])["MaxDD"],
                            spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                            spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                            spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"],
                            oracle=oracle, oracle_OOS_Sharpe=oos_sh[oracle],
                            regret=oos_sh[oracle] - mo["Sharpe"]))
    W = pd.DataFrame(wrows)
    ref = W[(W.start == "W260") & (W["dropk"] == 0)].set_index(["panel", "dial", "cost"])
    W["ref_pick"] = [ref.loc[(r.panel, r.dial, r.cost), "pick"] for r in W.itertuples()]
    W["ref_OOS"] = [ref.loc[(r.panel, r.dial, r.cost), "OOS_Sharpe"] for r in W.itertuples()]
    W["flip"] = (W.pick != W.ref_pick).astype(int)
    W["dOOS"] = W.OOS_Sharpe - W.ref_OOS
    mv = W[(W.start != "W260") | (W["dropk"] != 0)]
    P(f"  {len(ref)} TRUE-window picks (3 panels x 3 dials x 3 rungs); "
      f"{len(mv):,} drifted-window picks.")
    P(f"  PICK FLIP RATE under an unstamped IS window: {mv.flip.mean():.4f} "
      f"({int(mv.flip.sum()):,} of {len(mv):,})")
    f_end = mv[mv.start == "W260"].flip.mean()
    f_sta = mv[mv["dropk"] == 0].flip.mean()
    P(f"    by channel: END only {f_end:.4f}, START only {f_sta:.4f}")
    P("    by dial: " + ", ".join(f"{d} {mv[mv.dial==d].flip.mean():.4f}" for d in DIALS))
    P("    by trading days dropped: " +
      ", ".join(f"k={int(k)} {v:.4f}" for k, v in mv.groupby('dropk').flip.mean().items()))
    fl = mv[mv.flip == 1]
    P(f"  OOS COST OF THE FLIPS: mean dOOS_Sharpe {fl.dOOS.mean():+.4f} "
      f"(median {fl.dOOS.median():+.4f}, sd {fl.dOOS.std():.4f}, n {len(fl):,}); "
      f"flips that HELP OOS: {(fl.dOOS>0).mean():.4f}")
    nf = mv[mv.flip == 0].dOOS.mean()
    P(f"  non-flips: mean dOOS_Sharpe {nf:+.4f} (0 by construction where the pick is identical)")
    P()
    P("  TRUE-window rule-8 picks, OOS 2017-2026 read ONCE, vs the LIVE book and vs SPY:")
    rr = ref.reset_index()
    P(rr[["panel", "dial", "cost", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
          "base_OOS_Sharpe", "spy_OOS_Sharpe", "oracle", "regret"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    P(f"  TRUE picks beating the LIVE book OOS Sharpe: "
      f"{int((rr.OOS_Sharpe > rr.base_OOS_Sharpe).sum())} of {len(rr)}")
    P(f"  TRUE picks beating SPY OOS Sharpe:           "
      f"{int((rr.OOS_Sharpe > rr.spy_OOS_Sharpe).sum())} of {len(rr)}")
    P(f"  TRUE picks == the OOS oracle:                "
      f"{int((rr.pick == rr.oracle).sum())} of {len(rr)};  mean regret {rr.regret.mean():+.4f}")
    P(f"  ALL picks (true + drifted) beating the LIVE book OOS: "
      f"{int((W.OOS_Sharpe > W.base_OOS_Sharpe).sum()):,} of {len(W):,}; "
      f"beating SPY: {int((W.OOS_Sharpe > W.spy_OOS_Sharpe).sum()):,} of {len(W):,}")
    dump(W, "walkforward")
    return K, W


# =================================================================================================
# MAIN
# =================================================================================================
def main():
    P("IDEA 667 — does the record quote a WINDOW STAMP beside any metric it publishes?  "
      "(lane C, 2026-09-10)")
    P("Tuned parameters (2): stamp form " + "/".join(FORMS) + " x metric " + "/".join(METRICS4))
    P(f"Live leg: 3 panels x 3 books x {len(DIALS)} dials, rungs {RUNGS} bps, weekly, t+1, "
      f"gross {GROSS}.")
    P(f"Span grid: {len(STARTS)} start conventions x {len(ENDS)} end truncations = "
      f"{len(STARTS)*len(ENDS)} points.")
    P(f"IS <= {IS_END}, OOS >= {OOS_START}.")

    # ------------------------------------------------------------------ panels
    px_small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in px_small.columns if c != "SPY" and c not in bad]
    PX = {
        "U56": dict(pxall=load_universe(), invest=None),
        "B136": dict(pxall=load_universe(broad=True), invest=None),
        "SMALL439": dict(pxall=px_small, invest=inv),
    }
    for pk in PANELS:
        d = PX[pk]
        d["px"] = d["pxall"] if d["invest"] is None else d["pxall"][d["invest"]]
        P(f"[panel] {pk}: {d['px'].shape[1]} investable cols, "
          f"{d['pxall'].index[0].date()}..{d['pxall'].index[-1].date()}, "
          f"eval from {d['px'].index[WARM].date()}")

    # ------------------------------------------------------------------ GATES
    P()
    P("=" * 100)
    P("GATES (pre-registered, run before any A1-A5 number is read)")
    P("=" * 100)
    pxg = PX["U56"]["px"]
    Wg = band_book(pxg, BAND0, GROSS)
    r0g, tog = fast_run(pxg, Wg)
    eng = backtest(pxg, Wg, cost_bps=0.0, freq=FREQ)
    d1r = float((r0g - eng["returns"]).abs().max())
    d1t = float((tog - eng["turnover"]).abs().max())
    P(f"  [G1] fast_run vs engine.backtest (U56 BAND @0bps): returns {d1r:.3e}, turnover {d1t:.3e}")
    assert d1r < 1e-12 and d1t < 1e-12
    e10 = backtest(pxg, Wg, cost_bps=10.0, freq=FREQ)["returns"]
    d2 = float((at_cost(r0g, tog, 10.0) - e10).abs().max())
    P(f"  [G2] cost identity r(c) = r0 - to*c/1e4 vs engine @10bps: {d2:.3e}")
    assert d2 < 1e-12
    d3 = float((band_book(pxg, BAND0, GROSS) - rules_v2_weights(pxg, BAND0, GROSS)).abs().max().max())
    P(f"  [G3] band_book(0.03,0.75) vs baseline.rules_v2_weights: {d3:.3e}")
    assert d3 == 0.0
    # G4 end-drift equivalence
    g4 = []
    for k in (1, 2, 5, 21):
        pxt = pxg.iloc[:-k]
        rt, tt = fast_run(pxt, band_book(pxt, BAND0, GROSS))
        a = at_cost(rt, tt, 10.0).loc[pxg.index[WARM]:]
        b = at_cost(r0g, tog, 10.0).loc[pxg.index[WARM]:].iloc[:-k]
        g4.append((k, float((a - b).abs().max()), abs(M(a)["Sharpe"] - M(b)["Sharpe"])))
    P("  [G4] end-drift equivalence (re-run truncated panel vs slice full-sample returns):")
    for k, dmax, dsh in g4:
        P(f"        k={k:2d}: max|d return| {dmax:.3e}, |dSharpe| {dsh:.3e}")
    P("        the residual is the final-week rebalance-mask edge only; A2 slices, and this is")
    P("        the exact size of that approximation.")
    # G5 the CHANGELOG datum
    P("  [G5] THE CHANGELOG DATUM — 2026-09-08 RULES v2 U56 row vs today's cache")
    live = backtest(pxg, rules_v2_weights(pxg), cost_bps=10.0, freq=FREQ)["returns"].loc[pxg.index[WARM]:]
    mlive = M(live)
    P(f"        today's cache ({pxg.index[-1].date()}): CAGR {mlive['CAGR']:.4%} "
      f"Sharpe {mlive['Sharpe']:.4f} MaxDD {mlive['MaxDD']:.4%} "
      f"H {mlive['H1']:.4f}/{mlive['H2']:.4f}")
    P(f"        idea 664 committed (same day)          : CAGR 8.63%  Sharpe 1.2021 MaxDD -12.05% "
      f"H 1.2309/1.1798")
    P(f"        CHANGELOG 2026-09-08                   : CAGR 8.66%  Sharpe 1.2056 MaxDD -12.05% "
      f"H 1.2259/1.1909")
    for k in (1, 2, 3, 5):
        mk = M(live.iloc[:-k])
        P(f"        today minus {k:2d} trading days ({pxg.index[-1-k].date()}): "
          f"CAGR {mk['CAGR']:.4%} Sharpe {mk['Sharpe']:.4f} "
          f"(dSharpe vs today {mk['Sharpe']-mlive['Sharpe']:+.4f}, "
          f"vs CHANGELOG {mk['Sharpe']-1.2056:+.4f})")
    P("        NOTE (idea 406/399): data/prices.csv is re-downloaded daily with auto-adjusted")
    P("        closes, so this residual mixes END-DRIFT with the U56 RESTATEMENT channel.")

    # ------------------------------------------------------------------ SIMULATIONS
    P()
    P("=" * 100)
    P("SIMULATIONS (each arm run ONCE at zero cost; every rung derived exactly via G2)")
    P("=" * 100)
    SIMS = {}
    for pk in PANELS:
        px = PX[pk]["px"]
        pxa = PX[pk]["pxall"]
        SIMS[(pk, "V2LIVE", "base")] = fast_run(pxa, rules_v2_weights(pxa))
        SIMS[(pk, "BAND", "base")] = fast_run(px, band_book(px))
        SIMS[(pk, "TOPN", "base")] = fast_run(px, topn_book(px))
        SIMS[(pk, "EWALL", "base")] = fast_run(px, ewall_book(px))
        for cad in CONTAM_CADS:
            SIMS[(pk, "BAND", f"cad{cad}")] = fast_run(px, band_book(px), freq=cad)
        for dial, (kind, levels) in DIALS.items():
            for lv in levels:
                SIMS[(pk, kind, lv)] = fast_run(px, make_book(kind, lv, px))
        P(f"  {pk}: {sum(1 for k in SIMS if k[0]==pk)} simulations done")

    # ------------------------------------------------------------------ analyses
    C, T = census()
    Y, bars = yardsticks(PX, SIMS)
    R, A_dlt, A_cmp = reprice(C, bars)
    K, W = keeppaths_and_rule8(PX, SIMS)

    # ------------------------------------------------------------------ verdict
    P()
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    sh = T[(T.metric == "Sharpe")].set_index("form")
    P(f"  A1  Of {int(sh.loc['ROWSPAN','N']):,} committed CSVs that publish a Sharpe, "
      f"{int(sh.loc['ROWSPAN','stamped']):,} ({sh.loc['ROWSPAN','share']:.4f}) carry a per-row "
      f"start/end/asof stamp; {int(sh.loc['FILENAME','stamped']):,} "
      f"({sh.loc['FILENAME','share']:.4f}) carry a RUN date in the filename.")
    P(f"  A2  Pure-span Sharpe bar p50 {bars['PURE']['Sharpe']['p50']:.4f} "
      f"(p90 {bars['PURE']['Sharpe']['p90']:.4f}) vs 664's contaminated "
      f"{bars['CONTAM664']['Sharpe']['p50']:.4f} vs the BOOK bar "
      f"{bars['BOOK']['Sharpe']['p50']:.4f}.")
    sd = A_dlt[A_dlt.metric.isin(("Sharpe", "OOS_Sharpe"))] if len(A_dlt) else A_dlt
    if len(sd):
        n = sd.n.sum()
        P(f"  A3  {int(n):,} explicit Sharpe-family DELTA values published across "
          f"{sd.file.nunique():,} files; {sd.nlt.sum() / n:.4f} are smaller than the pure-span "
          f"p50 bar, {float((sd.share90 * sd.n).sum() / n):.4f} smaller than its p90.")
    if len(A_cmp):
        sc = A_cmp[A_cmp.metric.isin(("Sharpe", "OOS_Sharpe"))]
        if len(sc):
            nc = sc.n.sum()
            P(f"      control (A3b, same-window-by-construction comparand gaps): "
              f"{sc.nlt.sum() / nc:.4f} of {int(nc):,} below the same bar.")
    base = K[(K.start == "W260") & (K["dropk"] == 0)]
    nboth = int(((base.pass4a == 1) & (base.pass4b == 1)).sum())
    P(f"  A4  4a {int(base.pass4a.sum())}/{len(base)}, 4b {int(base.pass4b.sum())}/{len(base)}, "
      f"BOTH {nboth}/{len(base)} at the house span.")
    mv = W[(W.start != "W260") | (W["dropk"] != 0)]
    fl_cost = mv[mv.flip == 1].dOOS.mean()
    P(f"  A5  rule-8 pick flip rate under an unstamped window {mv.flip.mean():.4f}; "
      f"mean OOS cost of a flip {fl_cost:+.4f}.")
    P()
    P("  This run proposes NO RULES change, NO PROTOCOL change, and claims NO KEEP.")
    P("  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\n[written] {STEM}.console.txt")


if __name__ == "__main__":
    main()
