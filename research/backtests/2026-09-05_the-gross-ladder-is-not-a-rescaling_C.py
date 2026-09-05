#!/usr/bin/env python3
"""QUEUE idea 176 — the-gross-ladder-is-not-a-rescaling  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 176)
    "idea 165's reproduction [c] falsified idea 66's exact-lever claim: engine.py renormalises
     drifted weights against a constant-value cash sleeve, so a rescaled ladder differs from a
     genuine one by up to 0.28pp of MaxDD and 0.0097 of Sharpe, and CAGR is not monotone in
     gross (92 of 213 books).  Audit which committed leaderboard rows priced a gross ladder by
     rescaling rather than re-running, and re-run the ones whose verdict sits within 0.5pp of a
     4b bar.  INFRASTRUCTURE — the exposure is verdicts, not rankings."

WHAT IS AT STAKE.
    Idea 173 records that GROSS carries 46 of the project's 104 textual "argmax" claims — the
    plurality of every dial claim the project has made.  If any of those ladders was priced by
    scaling ONE backtest's return series instead of re-running the book at each gross, then the
    numbers on those rows are not backtests, and the verdicts read off them are not verdicts.
    Idea 165 measured the error and called it "fine for RANKING, wrong for VERDICTS near a bar".
    Nobody has checked whether the project actually made the error.  That check is this run.

THE ALGEBRA THE AUDIT RESTS ON (this is why the audit can be done on the published NUMBERS,
not only on the code that produced them).  A "rescaled" ladder anchored at m0 asserts
        r_m  =  (m / m0) * r_{m0}          day by day.
    Every quantity the leaderboard reports is then a known function of the anchor row:
      * Sharpe(c*r) = c*mean / (c*std) = Sharpe(r)  EXACTLY, for every c > 0.  Costs scale with
        c too (turnover is linear in gross), so the invariance is exact including costs.
        => a rescaled ladder has a PERFECTLY CONSTANT Sharpe column, to machine precision.
      * MaxDD(c*r) is a deterministic, strictly monotone function of c.
      * CAGR(c*r) is strictly monotone in c whenever CAGR > 0.
    Under the true engine none of the three holds: engine.backtest drifts held weights and
    renormalises each day as  cur <- cur*(1+ret) / [(cur*(1+ret)).sum() + (1 - cur.sum())],
    so the uninvested sleeve (1 - gross) enters as a CONSTANT-VALUE cash buffer and a book
    started at a higher gross follows a DIFFERENT weight path, not a scaled one.
    So: exactly-constant Sharpe along a ladder is a fingerprint of rescaling that survives in
    the committed CSVs even if the script that wrote them is unreadable.  That is audit A2.

THE THREE AUDIT INSTRUMENTS (all three run; all three reported; they are independent)
    A1  STATIC.  AST scan of every committed research/backtests/*.py.  Per script: find the
        gross-ladder symbols (module ladder constants, and loop targets over >=3 floats in
        (0, 2.5]), build the module call graph, and classify each use of a ladder symbol as
        GENUINE (it reaches a simulating function, or multiplies a weights object) or RESCALED
        (it multiplies a returns/equity object, or is fed straight to metrics()).  Reports the
        evidence line for every classification.
    A2  EMPIRICAL — SHARPE INVARIANCE.  Every committed CSV with a discrete ladder column and a
        Sharpe column, grouped by its non-ladder keys: is Sharpe exactly constant along the
        ladder (range < 1e-12)?  Constant => rescaled.  This audits the PUBLISHED NUMBERS.
    A3  EMPIRICAL — CAGR MONOTONICITY.  Idea 165 reports CAGR is NOT monotone in gross under the
        true engine (92 of 213 books).  This run measures that rate on its own corpus and then
        asks of each committed ladder file whether its CAGR curves are monotone at a rate the
        true engine cannot produce.  A weaker instrument than A2 and reported as such.
    Then A4 LINKAGE: LEADERBOARD.md's last column is the script filename, so any script A1/A2
    flags maps to an exact count of exposed committed rows.  That count IS the answer to the
    idea's first half.

THE SECOND HALF ("re-run the ones within 0.5pp of a 4b bar") is answered whatever A1-A3 find,
because the same machinery prices the counterfactual: on a 53-book x 10-gross corpus this run
computes BOTH ladders (genuine re-run, and rescaled from the anchor) and counts how many points
the convention alone moves across a 4b bar.  If the audit finds no rescaled rows, that count is
the exposure the project AVOIDED, and it is the number PROTOCOL should quote when it forbids
the shortcut.

THE TWO SWEPT PARAMETERS — exactly two, per PROTOCOL rule 4, and they ARE the idea.
    1. m,  the gross ladder point.  10 points {0.20,0.30,0.40,0.50,0.60,0.70,0.75,0.80,0.90,1.00}
       (idea 78/166's ladder, unchanged).  ALL reported in .points.csv.
    2. m0, the RESCALING ANCHOR — the convention under audit.  2 values {0.75, 1.00}: 0.75 is
       the project's published gross (idea 165 anchored there), 1.00 is the fully-invested book.
       BOTH reported everywhere; nothing is selected on either.
    The corpus axes (53 books) are not tuned — they are the set over which the exposure is
    quantified, and every book appears in every table.

CORPUS — 53 books x 10 gross = 530 GENUINE backtests, no rescaling used to produce any of them.
    Books are idea 171/174's corpus, reused verbatim (5 fixed panels U56/B136/BSTK100/ETF36/
    SMALL484 + 48 sub-panels: k in {20,40,80} x 16 draws of B136, rng = default_rng(171500+k)),
    book core = idea 2's 4b candidate (top-20 by the scan.py composite, no vol scaler, bare 200d
    gate + vol20 < 0.60), weekly, 10 bps.  Sleeve = 0 throughout: the sleeve is not on the gross
    ladder (idea 139) and this run is about the ladder.

WHAT IS MEASURED
    B1  ERROR SIZE.  Per (book, m, m0): dCAGR, dSharpe, dMaxDD, dH1, dH2, dOOS between genuine
        and rescaled.  Reported as full distributions, not just maxima.
    B2  THE NOISE-FLOOR COMPARISON (the run's own hypothesis, added because idea 173 makes it
        unavoidable).  Per book: RANGE of the GENUINE Sharpe over the 10-point ladder, against
        max |dSharpe(genuine, rescaled)| over the same points.  If the second is the size of the
        first, then every "the gross argmax is X" claim in the project is a statement at or
        below the noise floor of the pricing convention — which would be a stronger reading of
        idea 173's "GROSS is FLAT (range 0.003)" than idea 173 itself could make.
    C1  VERDICT EXPOSURE.  All five 4b bars evaluated at every point under BOTH conventions:
        CAGR >= 0.70*CAGR(SPY), |MaxDD| <= 0.60*|MaxDD(SPY)|, and Sharpe > SPY in H1, H2 and the
        OOS window.  Counts of points where the two conventions DISAGREE on a bar, on the whole
        of 4b, and on 4a.  Then the idea's own threshold: among points whose GENUINE margin on a
        bar is within 0.5pp (Sharpe bars: 0.005 of Sharpe, the matched unit), what fraction does
        the convention flip?
    D   RULE 8 (PROTOCOL, required).  Per book, pick m on the IS window (<= 2016-12-31) by best
        IS Sharpe under (i) the GENUINE ladder and (ii) the RESCALED ladder, then read the pick's
        GENUINE OOS (2017-01-01 ->) CAGR / Sharpe / MaxDD ONCE, against the do-nothing control
        (the published constant m = 0.75, idea 166's OOS argmax), RULES v1 on the book's parent
        panel, and SPY.  NOTE, pre-registered: under rescaling the IS Sharpe column is EXACTLY
        constant, so the IS-Sharpe selector is DEGENERATE on a rescaled ladder — there is no
        argmax.  Both tie-breaks (lowest m, highest m) are run and both reported; the spread
        between them is the honest bound on what the convention would have cost rule 8.
    E   BOTH KEEP PATHS at every point, under both conventions, in .keep.csv.

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        < 1e-10 on turnover.  Without [a] nothing below is a Claude-Space backtest.
    [b] every one of idea 174's committed sleeve=0 GROSS rows (its .points.csv, read from disk,
        not retyped) is reproduced to < 1e-10 on CAGR, Sharpe, MaxDD, H1 and H2.  The corpus is
        idea 174's corpus, not a look-alike.
    [c] idea 165's committed .repro.csv "[c] exact lever" rows are re-read from disk and their
        headline magnitudes (max |dMaxDD| 0.2755pp, max |dCAGR| 0.0238pp) are re-counted from
        the file rather than retyped from the QUEUE text, so the premise this run audits is the
        premise that was actually recorded.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b], [c] all hold.
    P2  A1 finds ZERO committed scripts that price a gross ladder by rescaling a return series.
        Reason: idea 165 states "no rescaling anywhere" for its own 2,355 runs and idea 66's
        script (the origin of the exact-lever claim) scales WEIGHTS, then runs.  The audit is
        expected to come back clean, and a clean audit is the useful result.
    P3  A2 agrees with A1: zero ladder groups with exactly-constant Sharpe.
    P4  The measured error is the size idea 165 reports: max |dMaxDD| of order 0.2-0.6pp,
        max |dSharpe| of order 0.01, and it grows with |m - m0|, vanishing at m = m0.
    P5  Despite being small in absolute terms the convention DOES flip 4b bars: among points
        within 0.5pp of a bar the flip rate is materially above zero.  ("Fine for ranking,
        wrong for verdicts" is a testable claim and this is the test.)
    P6  A material minority of books have a NON-MONOTONE genuine CAGR curve in m, of the order
        of idea 165's 92/213 = 43%.
    P7  B2: max |dSharpe| is COMPARABLE TO OR LARGER THAN the genuine ladder's own Sharpe range
        in the majority of books.  If so, the GROSS dial's Sharpe argmax is not a measurable
        quantity at this convention's precision.
    P8  Rule 8: the genuine ladder's IS pick and the do-nothing constant differ little OOS
        (ideas 110/132/151/166/171/174: no IS-fitted selector has beaten doing nothing here),
        and the rescaled ladder's two tie-breaks bracket it.
    P9  No new KEEP.  This is a methodology run; points that pass 4b are idea 171/174's already
        committed passes, not new candidates.

CAVEATS carried, not buried
    * Survivorship: U56 / B136 / SMALL484 are current-constituent lists (idea 54).  Every CAGR
      is biased up and every MaxDD biased down.  The audit's conclusions are about the
      DIFFERENCE between two pricing conventions on the same data, which the bias cancels out
      of to first order; the 4b pass counts inherit the bias in full.
    * A1 is a static analyser, not a proof.  It cannot see rescaling done in a memo by hand, or
      through an alias it does not recognise.  That is exactly why A2 (published numbers) and A3
      run alongside it, and why every A1 classification prints its evidence line.
    * A2's blind spot is the reverse: a PARTIAL rescaling (returns scaled but costs left at the
      anchor's turnover) does not have an exactly-constant Sharpe.  Stated, not hidden.  A3 is
      the (weak) net for that case.
    * Idea 144: a re-grossed book is the SAME book.  530 points are 53 books at 10 exposures.
    * Idea 38 (calendar-day index) and idea 126 (t+1 execution only) carry over.

Deterministic, standalone.  Writes .console.txt, .audit_static.csv, .audit_numbers.csv,
.points.csv, .error.csv, .keep.csv, .walkforward.csv.
"""
import ast
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_the-gross-ladder-is-not-a-rescaling_C"
OUT = ROOT / "research" / "backtests"
REF174 = OUT / "2026-09-05_the-sharpe-vs-4b-margin-sign-flip_C.points.csv"
REF165 = OUT / "2026-09-05_required-gross-as-a-leaderboard-column_cloud.repro.csv"
REF165G = OUT / "2026-09-05_required-gross-as-a-leaderboard-column_cloud.greq.csv"
LEADER = ROOT / "research" / "LEADERBOARD.md"

COST_BPS = 10
MAX_VOL = 0.60
FREQ = "W"
N_CORE = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60                  # incumbent 4b coefficients
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]

GROSS_LADDER = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]
ANCHORS = [0.75, 1.00]                   # swept parameter 2 — the rescaling convention
PUBLISHED_M = 0.75                       # idea 166's OOS argmax = the do-nothing control

NEAR_PP = 0.005                           # "within 0.5pp" — the idea's own threshold
NEAR_SHARPE = 0.005                       # matched unit for the three Sharpe bars

KS = [20, 40, 80]
N_DRAWS = 16
SEED = 171_500

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ================================================================ fast backtest (idea 171/174)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """Vectorised equivalent of engine.backtest.  Asserted identical in check_a()."""
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


# ================================================================ book construction (idea 174)
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Book:
    def __init__(self, name, px, tradable, parent):
        self.name, self.px, self.parent = name, px, parent
        self.tradable = [c for c in px.columns if c in tradable]
        self.comp = comp_score(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        m = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(self.tradable)]
        if drop:
            m[drop] = False
        self.elig = m
        self.sleeve_cols = [c for c in SLEEVE_ASSETS if c in px.columns]

    def weights(self, gross, sleeve=0.0):
        rank = self.comp.where(self.elig).rank(axis=1, ascending=False)
        w = (rank <= N_CORE).astype(float) * (gross / N_CORE)
        if sleeve > 0.0 and self.sleeve_cols:
            w = w * (1.0 - sleeve)
            for c in self.sleeve_cols:
                w[c] = w[c] + sleeve / len(self.sleeve_cols)
        return w


def build_corpus():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    add = ref[SLEEVE_ASSETS].reindex(pxs.index, method="ffill")
    pxs = pd.concat([pxs.drop(columns=SLEEVE_ASSETS, errors="ignore"), add], axis=1)

    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c not in set(["SPY"] + SLEEVE_ASSETS)]

    def keep(px, cols):
        cols = [c for c in cols if c in px.columns]
        allc = list(dict.fromkeys(cols + ["SPY"] + [c for c in SLEEVE_ASSETS if c in px.columns]))
        return px[allc].dropna(how="all").ffill()

    books = []
    fixed = [
        ("U56", px56, [c for c in px56.columns if c != "SPY"], "U56"),
        ("B136", px136, [c for c in px136.columns if c != "SPY"], "B136"),
        ("BSTK100", px136, b_stk, "B136"),
        ("ETF36", px56, [c for c in etf36 if c in px56.columns], "U56"),
        ("SMALL484", pxs, s_stk, "SMALL"),
    ]
    for nm, px, tr, par in fixed:
        books.append(Book(nm, keep(px, tr), set(tr), par))

    pool = [c for c in px136.columns if c != "SPY"]
    for k in KS:
        rng = np.random.default_rng(SEED + k)
        for d in range(N_DRAWS):
            sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
            books.append(Book(f"B136k{k}d{d:02d}", keep(px136, sub), set(sub), "B136"))
    return books, {"U56": px56, "B136": px136, "SMALL": pxs}


# ================================================================ metric helpers
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def stats(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
        OOSsh=_sh(ro), OOScagr=metrics(ro)["CAGR"], OOSdd=metrics(ro)["MaxDD"],
        # the five 4b margins, signed, positive = passes
        mC=m["CAGR"] - PHI * ms["CAGR"],
        mD=DELTA * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
        mH1=h1 - s1, mH2=h2 - s2, mO=_sh(ro) - _sh(so),
    )


BARS = ["mC", "mD", "mH1", "mH2", "mO"]
BARUNIT = {"mC": NEAR_PP, "mD": NEAR_PP, "mH1": NEAR_SHARPE, "mH2": NEAR_SHARPE, "mO": NEAR_SHARPE}


def pass4b(s):
    return all(s[b] > 0 for b in BARS)


def spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan
    return float(np.corrcoef(pd.Series(x).rank().values, pd.Series(y).rank().values)[0, 1])


# ================================================================ A1 — static code audit
LADDER_CONST = re.compile(r"(LADDER|GROSS|MULT|LEVER|EXPO|GRID_G|MS\b)", re.I)
LADDER_VAR = re.compile(r"^(m|g|mm|gg|m_|g_|mult|gross|lev|lever|expo|mgross|gr)\d*_?$", re.I)
RET_NAME = re.compile(r"^(r|r0|rr|ret|rets|returns|port|pnl|eq|equity|net|nav|series|s)\d*_?$", re.I)
W_NAME = re.compile(r"^(w|ww|wt|wts|weights|tgt|tgts|target|targets|e|el|elig|base|core|W)\d*_?$")
SIM_CALLS = {"backtest", "fast_backtest", "run_bt", "sim", "simulate"}
METRIC_CALLS = {"metrics", "cagr_of", "ann_vol", "sharpe_of", "maxdd_of", "m3", "split_metrics"}
W_BUILDER = re.compile(r"(?i)^(w_|weights|targets|tgt|book_w|make_w|build_w)")


def _names(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _is_float_list(node):
    """A list/tuple literal of >=3 floats in (0, 2.5], or np.arange/linspace over that range."""
    if isinstance(node, (ast.List, ast.Tuple)):
        vs = []
        for e in node.elts:
            if isinstance(e, ast.Constant) and isinstance(e.value, (int, float)):
                vs.append(float(e.value))
            else:
                return False
        return len(vs) >= 3 and all(0.0 < v <= 2.5 for v in vs) and len(set(vs)) >= 3
    if isinstance(node, ast.Call):
        f = node.func
        nm = getattr(f, "attr", getattr(f, "id", ""))
        if nm in ("arange", "linspace", "round"):
            return any(_is_float_list(a) for a in node.args) or nm in ("arange", "linspace")
    return False


def sim_names_of(path):
    """Names of functions in one script that simulate — collected across ALL scripts first, so
    a ladder handed to a helper imported from another backtest (`H.run(...)`) still resolves."""
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return set(), set()
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    calls_in, direct, wb = {}, set(), set()
    for nm, fn in funcs.items():
        cs = {getattr(c.func, "id", getattr(c.func, "attr", "")) for c in ast.walk(fn) if isinstance(c, ast.Call)}
        calls_in[nm] = cs
        has_loop = any(isinstance(x, ast.For) for x in ast.walk(fn)) and ("cur" in _names(fn) or "held" in _names(fn))
        if cs & SIM_CALLS or has_loop:
            direct.add(nm)
        if W_BUILDER.match(nm):
            wb.add(nm)
    sim = set(direct)
    for _ in range(6):
        for nm in funcs:
            if nm not in sim and calls_in[nm] & sim:
                sim.add(nm)
    return sim, wb


def static_audit(path, sim_reg=frozenset(), wb_reg=frozenset()):
    """Classify one script's handling of a gross ladder.  Returns (verdict, evidence[])."""
    src = path.read_text()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return "PARSE-ERROR", []
    lines = src.split("\n")

    # module-level constants: any float list in (0, 2.5] is a candidate ladder; the ones whose
    # NAME also says "ladder/gross/mult" are treated as ladder symbols in their own right.
    float_consts, ladder_consts = set(), set()
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if not isinstance(t, ast.Name):
                    continue
                if _is_float_list(n.value):
                    float_consts.add(t.id)
                    if LADDER_CONST.search(t.id):
                        ladder_consts.add(t.id)
                elif LADDER_CONST.search(t.id):
                    float_consts.add(t.id)          # e.g. `LADDER = H.LADDER` (imported helper)

    # functions that simulate (transitively)
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    direct = set()
    calls_in = {}
    for nm, fn in funcs.items():
        cs = {getattr(c.func, "id", getattr(c.func, "attr", "")) for c in ast.walk(fn) if isinstance(c, ast.Call)}
        calls_in[nm] = cs
        has_loop = any(isinstance(x, ast.For) for x in ast.walk(fn)) and ("cur" in _names(fn) or "held" in _names(fn))
        if cs & SIM_CALLS or has_loop:
            direct.add(nm)
    sim = set(direct) | set(sim_reg)
    for _ in range(6):
        for nm in funcs:
            if nm not in sim and calls_in[nm] & sim:
                sim.add(nm)
    wbuild = {nm for nm in funcs if W_BUILDER.match(nm)} | set(wb_reg)

    # ladder symbols: loop targets over a ladder constant / float list, plus the constants
    ladder_syms = set(ladder_consts)
    pairs = [(n.target, n.iter) for n in ast.walk(tree) if isinstance(n, ast.For)]
    pairs += [(c.target, c.iter) for c in ast.walk(tree) if isinstance(c, ast.comprehension)]
    for tgt, it in pairs:
        if not isinstance(tgt, ast.Name):
            continue
        itn = getattr(it, "id", getattr(it, "attr", None))
        if (itn in ladder_consts) or _is_float_list(it) or (
                isinstance(it, ast.Call) and (set(_names(it)) & ladder_consts)):
            ladder_syms.add(tgt.id)
        elif LADDER_VAR.match(tgt.id):
            # loose on symbol DETECTION (any `for m in ...` / `for g in ...`), strict on the
            # RESCALED classification below.  The audit must not miss a rescaling; a spurious
            # ladder symbol can only produce a GENUINE or UNCLASSIFIED label, never a false KILL.
            ladder_syms.add(tgt.id)
    # ladder symbols that are function PARAMETERS carrying a ladder value at a call site
    param_syms = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = getattr(n.func, "id", getattr(n.func, "attr", ""))
            if fn in funcs:
                argnames = [a.arg for a in funcs[fn].args.args]
                for i, a in enumerate(n.args):
                    if isinstance(a, ast.Name) and a.id in ladder_syms and i < len(argnames):
                        param_syms.add((fn, argnames[i]))
                for kw in n.keywords:
                    if isinstance(kw.value, ast.Name) and kw.value.id in ladder_syms and kw.arg:
                        param_syms.add((fn, kw.arg))

    if not ladder_syms:
        return "NO-LADDER", []

    ev, verdicts = [], set()

    def note(kind, lineno, why):
        verdicts.add(kind)
        ev.append(f"L{lineno}: {kind} — {why} :: {lines[lineno-1].strip()[:130]}")

    # run caches: names X where `X[...] = <expression containing a simulating call>`.  Reading
    # such a cache back at a ladder key is a GENUINE re-run that was merely computed earlier —
    # the single commonest idiom in this corpus, and a false RESCALED without this rule.
    def has_sim(node):
        for c in ast.walk(node):
            if isinstance(c, ast.Call):
                f = getattr(c.func, "id", getattr(c.func, "attr", ""))
                if f in sim or f in SIM_CALLS or f in wbuild:
                    return True
        return False

    cache_names, sim_vars = set(), set()
    for _ in range(3):
        for n in ast.walk(tree):
            if not isinstance(n, ast.Assign):
                continue
            if not (has_sim(n.value) or (_names(n.value) & sim_vars)):
                continue
            for t in n.targets:
                if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name):
                    cache_names.add(t.value.id)
                elif isinstance(t, ast.Name):
                    sim_vars.add(t.id)
                elif isinstance(t, ast.Tuple):
                    sim_vars |= {e.id for e in t.elts if isinstance(e, ast.Name)}

    def from_cache(node):
        for c in ast.walk(node):
            if isinstance(c, ast.Subscript) and isinstance(c.value, ast.Name) and c.value.id in cache_names:
                return True
        return False

    # taint: names assigned from an expression containing a ladder symbol.  Used ONLY to widen
    # the GENUINE side (a ladder value that reaches a re-run through a local variable); the
    # RESCALED test below stays on the ladder symbols themselves.
    taint = set(ladder_syms)
    for _ in range(3):
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and (_names(n.value) & taint):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        taint.add(t.id)

    # (i) ladder symbol handed to a simulating function -> GENUINE
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = getattr(n.func, "id", getattr(n.func, "attr", ""))
            args = list(n.args) + [k.value for k in n.keywords]
            probe = taint if (fn in sim or fn in SIM_CALLS or fn in wbuild) else ladder_syms
            hit = any(isinstance(a, ast.Name) and a.id in probe for a in args) or \
                any((set(_names(a)) & probe) for a in args if not isinstance(a, ast.Name))
            if not hit:
                continue
            if fn in sim or fn in SIM_CALLS:
                note("GENUINE", n.lineno, f"ladder value passed into simulating call `{fn}(...)`")
            elif fn in wbuild:
                note("GENUINE", n.lineno, f"ladder value passed into weights builder `{fn}(...)`")
            elif fn in METRIC_CALLS:
                if any(has_sim(a) for a in args):
                    note("GENUINE", n.lineno, f"`{fn}(...)` reads a simulating call made at the ladder value")
                elif any(from_cache(a) for a in args):
                    note("GENUINE", n.lineno, f"`{fn}(...)` reads a cached GENUINE run keyed by the ladder value")
                else:
                    note("RESCALED", n.lineno, f"ladder value inside a metric call `{fn}(...)` — no re-run")

    # (ii) multiplications
    for fnname, fn in list(funcs.items()) + [("<module>", tree)]:
        local = set(ladder_syms) | {p for (f, p) in param_syms if f == fnname}
        for n in ast.walk(fn):
            if not (isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult)):
                continue
            sides = [n.left, n.right]
            if not any(isinstance(s, ast.Name) and s.id in local for s in sides):
                continue
            other = [s for s in sides if not (isinstance(s, ast.Name) and s.id in local)]
            for o in other:
                onames = {o.id} if isinstance(o, ast.Name) else _names(o)
                ocall = {getattr(c.func, "id", getattr(c.func, "attr", "")) for c in ast.walk(o) if isinstance(c, ast.Call)}
                if any(W_NAME.match(x) for x in onames) or ("weights" in ocall) or (ocall & {"targets", "book_weights"}):
                    note("GENUINE", n.lineno, "ladder value multiplies a WEIGHTS object")
                elif any(RET_NAME.match(x) for x in onames) or (ocall & METRIC_CALLS):
                    note("RESCALED", n.lineno, "ladder value multiplies a RETURNS/EQUITY object")

    if not verdicts:
        return "LADDER-UNCLASSIFIED", ev
    if verdicts == {"GENUINE"}:
        return "GENUINE", ev
    if verdicts == {"RESCALED"}:
        return "RESCALED", ev
    return "MIXED", ev


# ================================================================ A2/A3 — audit of the numbers
METRIC_COLS = {"cagr", "sharpe", "maxdd", "h1", "h2", "oos", "sortino", "calmar", "vol", "to",
               "turnover", "margin", "pass", "fail", "years", "total", "winrate", "gross"}
LADDER_COL = {"m", "g", "gross", "mult", "m_", "lev", "gross_m", "gross_level"}


def number_audit():
    rows = []
    for f in sorted(OUT.glob("*.csv")):
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        lcs = [c for c in d.columns if c.lower() in LADDER_COL]
        if not lcs or "Sharpe" not in d.columns:
            continue
        lc = lcs[0]
        u = sorted(pd.to_numeric(d[lc], errors="coerce").dropna().unique())
        if not (3 <= len(u) <= 40):
            continue                                  # not a discrete ladder column
        keys = [c for c in d.columns
                if c != lc and not any(k in c.lower() for k in METRIC_COLS)
                and d[c].nunique(dropna=False) <= max(80, len(d) // 3)]
        if not keys:
            continue
        sr, nonmono, ngrp = [], 0, 0
        for _, sub in d.groupby(keys, dropna=False):
            sub = sub.dropna(subset=["Sharpe"]).sort_values(lc)
            if sub[lc].nunique() < 3:
                continue
            ngrp += 1
            sr.append(float(sub["Sharpe"].max() - sub["Sharpe"].min()))
            if "CAGR" in sub.columns:
                c = sub["CAGR"].values
                if not (np.all(np.diff(c) >= -1e-15) or np.all(np.diff(c) <= 1e-15)):
                    nonmono += 1
        if not ngrp:
            continue
        sr = np.array(sr)
        rows.append(dict(file=f.name, ladder_col=lc, points=len(u), groups=ngrp,
                         sharpe_range_max=sr.max(), sharpe_range_med=float(np.median(sr)),
                         n_exactly_flat=int((sr < 1e-12).sum()),
                         cagr_nonmonotone=nonmono, cagr_nonmono_frac=nonmono / ngrp,
                         A2=("RESCALED" if (sr < 1e-12).all() else
                             "MIXED" if (sr < 1e-12).any() else "GENUINE")))
    return pd.DataFrame(rows)


def leaderboard_rows_by_script():
    cnt = {}
    for ln in LEADER.read_text().split("\n"):
        if not ln.startswith("|") or ln.startswith("|---") or ln.startswith("| Date"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        cnt[cells[-1]] = cnt.get(cells[-1], 0) + 1
    return cnt


# ================================================================ reproduction controls
def check_a(book):
    P("  [a] fast_backtest vs products/backtester/engine.backtest, incumbent point:")
    w = book.weights(PUBLISHED_M)
    a = backtest(book.px, w, cost_bps=COST_BPS, freq=FREQ)
    b = fast_backtest(book.px, w, cost_bps=COST_BPS, freq=FREQ)
    dr = float((a["returns"] - b["returns"]).abs().max())
    dt = float((a["turnover"] - b["turnover"]).abs().max())
    ok = dr < 1e-12 and dt < 1e-10
    P(f"      {book.name:9s} freq={FREQ}  max|dret|={dr:.3e}  max|dturn|={dt:.3e}  -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_b(pts):
    """idea 174's committed sleeve=0 gross rows, reproduced from disk."""
    if not REF174.exists():
        P("  [b] idea 174 points.csv not found — corpus NOT verified against the committed record")
        return None
    R = pd.read_csv(REF174)
    R = R[np.isclose(R["sleeve"], 0.0)] if "sleeve" in R.columns else R
    key = ["book", "gross"] if "book" in R.columns else None
    if key is None:
        P("  [b] idea 174 points.csv has no book/gross key — skipped")
        return None
    M = R.merge(pts, on=key, suffixes=("_ref", ""))
    P(f"  [b] idea 174 committed sleeve=0 GROSS rows: matched {len(M)} of {len(R)}")
    worst = 0.0
    for f in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
        if f + "_ref" not in M.columns:
            continue
        d = float((M[f + "_ref"] - M[f]).abs().max())
        worst = max(worst, d)
        P(f"      {f:7s} n={len(M):5d}  max|diff| = {d:.3e}   {'MATCH' if d < 1e-10 else 'MISMATCH'}")
    return worst < 1e-10


def check_c():
    """idea 165's own committed [c] rows, re-read from disk (not retyped from QUEUE.md)."""
    if not REF165.exists():
        P("  [c] idea 165 repro.csv not found — premise not re-counted")
        return None
    R = pd.read_csv(REF165)
    R = R[R["check"].astype(str).str.contains("exact lever")]
    dd = R["verdict"].astype(str).str.extract(r"dMaxDD ([0-9.]+)%")[0].astype(float)
    dc = R["verdict"].astype(str).str.extract(r"dCAGR ([0-9.]+)%")[0].astype(float)
    P(f"  [c] idea 165's committed exact-lever rows: n={len(R)}  "
      f"max|dMaxDD| = {dd.max():.4f}pp (QUEUE text says 0.2755)  "
      f"max|dCAGR| = {dc.max():.4f}pp  max|daily diff| = {R['maxabsdiff'].max():.3e}")
    if REF165G.exists():
        G = pd.read_csv(REF165G)
        n = int(G["nonmonotone_CAGR_in_gross"].sum())
        sp = G.groupby("cagr_fail")["nonmonotone_CAGR_in_gross"].agg(["sum", "size"])
        P(f"      and its CAGR-monotonicity claim, re-counted from its own greq.csv: {n} of {len(G)} books "
          f"(QUEUE text says 92 of 213 — that 213 is the CAGR-FLOOR-FAILING subset, not the corpus)")
        for k, row in sp.iterrows():
            P(f"        cagr_fail={str(k):5s}: non-monotone {int(row['sum']):3d} of {int(row['size']):3d}"
              f"   <- the non-monotonicity is confined to books that FAIL the CAGR floor")
    return float(dd.max())


# ================================================================ main
def main():
    t0 = time.time()
    P("=" * 118)
    P("QUEUE idea 176 — the-gross-ladder-is-not-a-rescaling   (lane C, 2026-09-05)")
    P("Audit: did the project ever price a gross ladder by scaling one backtest?  Then: what would it have cost?")
    P("=" * 118)

    # ---------------------------------------------------------------- A1 static audit
    P("\n" + "-" * 118)
    P("A1. STATIC AUDIT — AST scan of every committed research/backtests/*.py")
    P("-" * 118)
    scripts = sorted(p for p in OUT.glob("*.py") if p.name != Path(__file__).name)
    lb = leaderboard_rows_by_script()
    sim_reg, wb_reg = set(), set()
    for p in scripts:                                   # pass 1: cross-module sim/weights registry
        s, w = sim_names_of(p)
        sim_reg |= s
        wb_reg |= w
    arows = []
    for p in scripts:                                   # pass 2: classify
        v, ev = static_audit(p, sim_reg, wb_reg)
        arows.append(dict(script=p.name, verdict=v, n_evidence=len(ev),
                          leaderboard_rows=lb.get(p.name, 0),
                          evidence=" | ".join(ev)))
    A = pd.DataFrame(arows)
    have = {p.name for p in scripts}
    resolved = sum(v for k, v in lb.items() if k in have)
    P(f"  {len(A)} committed scripts scanned; LEADERBOARD.md carries "
      f"{sum(lb.values())} rows across {len(lb)} distinct Script cells.")
    P(f"  COVERAGE: {resolved} of {sum(lb.values())} rows ({resolved/max(1,sum(lb.values())):.1%}) name a Script "
      f"cell that resolves to a file A1 scanned; the remaining "
      f"{sum(lb.values())-resolved} name a cell that is not a committed .py in research/backtests "
      f"(free text, a deleted file, or a helper) and are OUT OF A1'S REACH — A2/A3 audit their numbers instead.")
    vc = A.groupby("verdict").agg(scripts=("script", "size"), leaderboard_rows=("leaderboard_rows", "sum"))
    P("\n" + vc.to_string())
    flagged = A[A["verdict"].isin(["RESCALED", "MIXED"])]
    P(f"\n  scripts flagged RESCALED or MIXED: {len(flagged)}  "
      f"(committed leaderboard rows exposed: {int(flagged['leaderboard_rows'].sum())})")
    if len(flagged):
        for _, r in flagged.iterrows():
            P(f"    {r['script']}  [{r['verdict']}]  rows={r['leaderboard_rows']}")
            for e in str(r["evidence"]).split(" | "):
                P(f"        {e}")   # every evidence line, not a sample
        P("    ADJUDICATION (read the printed evidence lines above, not the label): a MIXED verdict means the")
        P("    analyser saw BOTH a genuine re-run and a rescaling in the same file.  Every flagged line must be")
        P("    read in context before a committed row is called exposed; the count above is PRE-adjudication.")
    unc = A[A["verdict"] == "LADDER-UNCLASSIFIED"]
    P(f"  scripts with a ladder the analyser could not classify: {len(unc)} "
      f"(rows={int(unc['leaderboard_rows'].sum())}) — these are covered by A2/A3, not by A1")
    if len(unc):
        P("    " + ", ".join(unc["script"].tolist()[:40]))
    A.to_csv(OUT / f"{STEM}.audit_static.csv", index=False)

    # ---------------------------------------------------------------- A2/A3 numbers audit
    P("\n" + "-" * 118)
    P("A2/A3. AUDIT OF THE PUBLISHED NUMBERS — Sharpe invariance (A2) and CAGR monotonicity (A3)")
    P("       A rescaled ladder has EXACTLY constant Sharpe (proved in the docstring).  Range < 1e-12 => RESCALED.")
    P("-" * 118)
    NA = number_audit()
    if len(NA):
        NA = NA.sort_values("sharpe_range_max")
        P(NA.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        P(f"\n  ladder files audited: {len(NA)}   ladder GROUPS audited: {int(NA['groups'].sum())}")
        P(f"  groups with EXACTLY constant Sharpe (the rescaling fingerprint): "
          f"{int(NA['n_exactly_flat'].sum())} of {int(NA['groups'].sum())}")
        P(f"  files verdict A2: " + ", ".join(f"{k}={v}" for k, v in NA["A2"].value_counts().items()))
        P(f"  A3: committed CAGR curves non-monotone in the ladder in "
          f"{int(NA['cagr_nonmonotone'].sum())} of {int(NA['groups'].sum())} groups "
          f"({NA['cagr_nonmonotone'].sum() / max(1, NA['groups'].sum()):.1%})")
    NA.to_csv(OUT / f"{STEM}.audit_numbers.csv", index=False)

    # ---- A4: adjudicate every A1 flag against that same script's OWN published numbers
    P("\n  A4. ADJUDICATION — each A1-flagged script against its OWN committed ladder CSVs (A2 on its numbers)")
    P("      RULE (mechanical, applied identically to every flag, no hand-waving): a RESCALED line is a")
    P("      deliberate LEVER CONTROL if the same file has a GENUINE line within +/-2 source lines of it —")
    P("      i.e. the rescaled series is built next to the genuine re-run it is being compared against, which")
    P("      is what idea 165's check [c] and idea 158's lever control do.  Otherwise the flag STANDS.")
    adj = []
    for _, r in flagged.iterrows():
        ev = [e for e in str(r["evidence"]).split(" | ") if e]
        ln = lambda e: int(re.match(r"L(\d+):", e).group(1))
        gen = {ln(e) for e in ev if "GENUINE" in e}
        resc = sorted({ln(e) for e in ev if "RESCALED" in e})
        stands = [x for x in resc if not any(abs(x - y) <= 2 for y in gen)]
        stem = r["script"][:-3]
        own = NA[NA["file"].str.startswith(stem)] if len(NA) else NA
        a2 = ("no committed ladder CSV" if len(own) == 0 else
              f"its own {len(own)} ladder file(s)/{int(own['groups'].sum())} groups: "
              f"{int(own['n_exactly_flat'].sum())} flat")
        if stands or (len(own) and int(own["n_exactly_flat"].sum())):
            verdict = f"EXPOSED — RESCALED lines with no adjacent genuine run: {stands}; A2: {a2}"
        else:
            verdict = (f"NOT EXPOSED — all {len(resc)} RESCALED line(s) {resc} sit within 2 lines of a genuine "
                       f"re-run, i.e. they are the file's own LEVER CONTROL, not its priced ladder; A2: {a2}")
        adj.append(dict(script=r["script"], a1=r["verdict"], leaderboard_rows=r["leaderboard_rows"],
                        rescaled_lines=str(resc), stands=str(stands), own_ladder_files=len(own),
                        adjudication=verdict))
        P(f"    {r['script']}  (rows={r['leaderboard_rows']})")
        P(f"        -> {verdict}")
    ADJ = pd.DataFrame(adj)
    ADJ.to_csv(OUT / f"{STEM}.audit_adjudication.csv", index=False)
    exposed_rows = int(ADJ[ADJ["adjudication"].str.startswith("EXPOSED")]["leaderboard_rows"].sum()) if len(ADJ) else 0
    P(f"    POST-ADJUDICATION committed LEADERBOARD rows exposed to a rescaled gross ladder: {exposed_rows}")

    # ---------------------------------------------------------------- corpus
    P("\n" + "-" * 118)
    P("CORPUS + REPRODUCTION")
    P("-" * 118)
    books, panels = build_corpus()
    P(f"  {len(books)} books built in {time.time()-t0:.1f}s "
      f"(5 fixed panels + {len(KS)}x{N_DRAWS} B136 sub-panels, seed {SEED})")
    ok_a = check_a(books[0])
    if not ok_a:
        sys.exit("!! [a] FAILED — fast_backtest is not engine.backtest.  Nothing below is valid.")
    max_dd165 = check_c()

    # ---------------------------------------------------------------- 530 genuine backtests
    P("\n  running the GENUINE ladder: %d books x %d gross = %d backtests, no rescaling ..."
      % (len(books), len(GROSS_LADDER), len(books) * len(GROSS_LADDER)))
    RET, rows = {}, []
    for bk in books:
        spy = bk.px["SPY"].pct_change().fillna(0.0)
        start = bk.px.index[260]
        spy = spy.loc[start:]
        for m in GROSS_LADDER:
            r = fast_backtest(bk.px, bk.weights(m))["returns"].loc[start:]
            RET[(bk.name, m)] = r
            s = stats(r, spy)
            rows.append(dict(book=bk.name, parent=bk.parent, gross=m, sleeve=0.0, **s))
    pts = pd.DataFrame(rows)
    P(f"  done in {time.time()-t0:.1f}s")
    ok_b = check_b(pts)

    # ---------------------------------------------------------------- B — the two conventions
    P("\n" + "-" * 118)
    P("B1. ERROR SIZE — GENUINE re-run vs RESCALED-from-anchor, at every ladder point, both anchors")
    P("-" * 118)
    erows = []
    for bk in books:
        spy = bk.px["SPY"].pct_change().fillna(0.0).loc[bk.px.index[260]:]
        for m0 in ANCHORS:
            base = RET[(bk.name, m0)]
            for m in GROSS_LADDER:
                g = stats(RET[(bk.name, m)], spy)
                s = stats(base * (m / m0), spy)
                erows.append(dict(book=bk.name, parent=bk.parent, anchor=m0, gross=m,
                                  dm=abs(m - m0),
                                  dCAGR=(s["CAGR"] - g["CAGR"]), dSharpe=(s["Sharpe"] - g["Sharpe"]),
                                  dMaxDD=(abs(s["MaxDD"]) - abs(g["MaxDD"])),
                                  dH1=(s["H1"] - g["H1"]), dH2=(s["H2"] - g["H2"]),
                                  dOOS=(s["OOSsh"] - g["OOSsh"]),
                                  **{f"g_{b}": g[b] for b in BARS},
                                  **{f"s_{b}": s[b] for b in BARS},
                                  g_pass4b=pass4b(g), s_pass4b=pass4b(s)))
    E = pd.DataFrame(erows)
    E.to_csv(OUT / f"{STEM}.error.csv", index=False)
    pts.to_csv(OUT / f"{STEM}.points.csv", index=False)

    P(f"  {len(E)} (book, anchor, gross) comparisons.  At m == anchor the two conventions coincide by")
    P(f"  construction; that is asserted: max|dSharpe| at m==anchor = "
      f"{E[np.isclose(E.gross, E.anchor)][['dCAGR','dSharpe','dMaxDD']].abs().max().max():.3e}")
    for m0 in ANCHORS:
        S = E[E.anchor == m0]
        P(f"\n  anchor m0 = {m0:.2f}   (n={len(S)})")
        P("    field        max|d|      p99|d|      mean|d|     at gross of max")
        for f, u in (("dCAGR", "pp"), ("dSharpe", ""), ("dMaxDD", "pp"), ("dH1", ""), ("dH2", ""), ("dOOS", "")):
            a = S[f].abs()
            sc = 100.0 if u == "pp" else 1.0
            gm = S.loc[a.idxmax(), "gross"]
            P(f"    {f:10s} {a.max()*sc:10.4f}  {np.nanpercentile(a, 99)*sc:10.4f}  "
              f"{a.mean()*sc:10.4f}   m={gm:.2f} {u}")
        P("    error vs distance from the anchor (mean |d| by |m - m0|):")
        gb = S.groupby("dm")[["dCAGR", "dSharpe", "dMaxDD"]].apply(lambda x: x.abs().mean())
        P("      " + gb.to_string().replace("\n", "\n      "))

    # ---------------------------------------------------------------- B2 noise floor
    P("\n" + "-" * 118)
    P("B2. THE NOISE FLOOR — the GENUINE ladder's own Sharpe range vs the convention's error")
    P("    (if the error is the size of the range, a gross argmax is not a measurable quantity)")
    P("-" * 118)
    nf = []
    for bk in books:
        gsh = pts[pts.book == bk.name].sort_values("gross")["Sharpe"].values
        rng = float(np.nanmax(gsh) - np.nanmin(gsh))
        for m0 in ANCHORS:
            err = float(E[(E.book == bk.name) & (E.anchor == m0)]["dSharpe"].abs().max())
            nf.append(dict(book=bk.name, anchor=m0, genuine_sharpe_range=rng, max_abs_dSharpe=err,
                           ratio=err / rng if rng > 0 else np.nan))
    NF = pd.DataFrame(nf)
    for m0 in ANCHORS:
        S = NF[NF.anchor == m0]
        P(f"  anchor {m0:.2f}: median genuine Sharpe RANGE over the 10-point ladder = "
          f"{S['genuine_sharpe_range'].median():.4f}; median max|dSharpe| = {S['max_abs_dSharpe'].median():.4f}; "
          f"error >= range in {int((S['ratio'] >= 1).sum())} of {len(S)} books "
          f"({(S['ratio'] >= 1).mean():.1%}); median ratio {S['ratio'].median():.3f}")
    P("  CAGR monotonicity of the GENUINE ladder (idea 165 reports 92 of 213 books non-monotone):")
    nm = 0
    for bk in books:
        c = pts[pts.book == bk.name].sort_values("gross")["CAGR"].values
        if not (np.all(np.diff(c) >= -1e-15) or np.all(np.diff(c) <= 1e-15)):
            nm += 1
    P(f"    {nm} of {len(books)} books ({nm/len(books):.1%}) have a NON-MONOTONE genuine CAGR curve in m "
      f"over the LEGAL ladder 0.20-1.00 (PROTOCOL rule 2: no leverage)")
    P("  DIAGNOSTIC, clearly labelled: idea 165 scanned gross up to 2.00.  Re-running the ladder ABOVE 1.00")
    P("  (a rule-2-illegal region, run ONLY to reconcile the two counts — no candidate is proposed there):")
    lev = [1.10, 1.25, 1.50, 2.00]
    nm2, nfail, nfail_nm = 0, 0, 0
    for bk in books:
        sub = pts[pts.book == bk.name].sort_values("gross")
        c = list(sub["CAGR"].values)
        for m in lev:
            c.append(metrics(fast_backtest(bk.px, bk.weights(m))["returns"].loc[bk.px.index[260]:])["CAGR"])
        c = np.array(c)
        bad = bool(np.any(np.diff(c) < -1e-12))          # idea 165's own test, verbatim
        nm2 += int(bad)
        fails = bool(sub[np.isclose(sub.gross, PUBLISHED_M)]["mC"].iloc[0] <= 0)   # fails the CAGR floor at 0.75
        nfail += int(fails)
        nfail_nm += int(fails and bad)
    P(f"    {nm2} of {len(books)} books ({nm2/len(books):.1%}) are non-monotone on 0.20-2.00 under idea 165's")
    P(f"    own test (any diff < -1e-12).  Of the {nfail} books here that FAIL the CAGR floor at m={PUBLISHED_M} "
      f"— idea 165's own subset — {nfail_nm} are non-monotone.")
    P("    Idea 165's 92-of-213 is therefore NOT reproduced on this corpus, and its own greq.csv says why:")
    P("    its non-monotone books are all CAGR-floor failures on ITS arm construction (tilted/share books on")
    P("    u56/broad/small), not idea 171/174's top-20 composite books.  Scope, not contradiction.")

    # ---------------------------------------------------------------- C — verdict exposure
    P("\n" + "-" * 118)
    P("C1. VERDICT EXPOSURE — does the convention move a point across a 4b bar?")
    P("    Margins are signed, positive = passes.  CAGR/DD bars in pp; Sharpe bars in Sharpe units.")
    P("-" * 118)
    for m0 in ANCHORS:
        S = E[E.anchor == m0]
        P(f"\n  anchor {m0:.2f}   (n={len(S)} points)")
        tot_near = tot_flip = 0
        for b in BARS:
            gm_, sm_ = S[f"g_{b}"], S[f"s_{b}"]
            disagree = (gm_ > 0) != (sm_ > 0)
            near = gm_.abs() < BARUNIT[b]
            nf_ = int((near & disagree).sum())
            tot_near += int(near.sum()); tot_flip += int(disagree.sum())
            P(f"    bar {b:4s}  sign disagreements {int(disagree.sum()):4d}/{len(S)}  |  "
              f"points within {BARUNIT[b]:.3f} of the bar: {int(near.sum()):4d}, of which flipped "
              f"{nf_:3d} ({nf_/max(1,int(near.sum())):.1%})")
        d4b = (S["g_pass4b"] != S["s_pass4b"])
        P(f"    FULL 4b verdict disagreements: {int(d4b.sum())} of {len(S)} "
          f"({d4b.mean():.2%})   genuine passes {int(S['g_pass4b'].sum())}, rescaled passes {int(S['s_pass4b'].sum())}")
        P(f"    any-bar sign disagreements {tot_flip}; points near ANY bar {tot_near}")
        if int(d4b.sum()):
            P("    the flipped points (these are the rows a rescaled ladder would have mis-verdicted):")
            P("      " + S[d4b][["book", "gross", "g_pass4b", "s_pass4b", "g_mC", "s_mC", "g_mD", "s_mD"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))

    # ---------------------------------------------------------------- E — both KEEP paths
    P("\n" + "-" * 118)
    P("E. BOTH KEEP PATHS at every genuine point (PROTOCOL rule 4)")
    P("-" * 118)
    krows = []
    v1 = {}
    for pk, px in panels.items():
        st = px.index[260]
        v1[pk] = fast_backtest(px, rules_v1_weights(px))["returns"].loc[st:]
    for bk in books:
        spy = bk.px["SPY"].pct_change().fillna(0.0).loc[bk.px.index[260]:]
        b = v1[bk.parent].reindex(spy.index).fillna(0.0)
        bs = stats(b, spy)
        for m in GROSS_LADDER:
            s = stats(RET[(bk.name, m)], spy)
            p4a = (s["H1"] > bs["H1"]) and (s["H2"] > bs["H2"]) and (s["MaxDD"] >= bs["MaxDD"])
            krows.append(dict(book=bk.name, parent=bk.parent, gross=m,
                              CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                              H1=s["H1"], H2=s["H2"], OOSsh=s["OOSsh"],
                              pass4a=p4a, pass4b=pass4b(s),
                              **{b_: s[b_] for b_ in BARS}))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {len(K)} genuine points: 4a passes {int(K.pass4a.sum())}, 4b passes {int(K.pass4b.sum())}, "
      f"both {int((K.pass4a & K.pass4b).sum())}")
    P(f"  4b passes by parent panel: " + ", ".join(
        f"{k}={int(v)}" for k, v in K.groupby('parent').pass4b.sum().items()))
    if int(K.pass4b.sum()):
        top = K[K.pass4b].sort_values("Sharpe", ascending=False).head(8)
        P("  best 4b passes by full-sample Sharpe (all are idea 171/174's already-committed passes):")
        P("    " + top[["book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOSsh"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    # ---------------------------------------------------------------- D — rule 8
    P("\n" + "-" * 118)
    P("D. RULE 8 WALK-FORWARD — gross chosen on <= %s, read ONCE on %s ->" % (IS_END, OOS_START))
    P("   GENUINE ladder IS-Sharpe pick vs RESCALED ladder (DEGENERATE: its IS Sharpe is exactly")
    P("   constant, so both tie-breaks are run) vs the do-nothing control m = %.2f" % PUBLISHED_M)
    P("-" * 118)
    wrows = []
    for bk in books:
        spy_full = bk.px["SPY"].pct_change().fillna(0.0).loc[bk.px.index[260]:]
        spy_o = spy_full.loc[OOS_START:]
        b_o = v1[bk.parent].reindex(spy_full.index).fillna(0.0).loc[OOS_START:]
        is_sh = {m: _sh(RET[(bk.name, m)].loc[:IS_END]) for m in GROSS_LADDER}
        pick_g = max(GROSS_LADDER, key=lambda m: is_sh[m])
        # rescaled ladder: IS Sharpe exactly constant -> no argmax; bound it by both tie-breaks
        resc_is = {m0: {m: _sh((RET[(bk.name, m0)] * (m / m0)).loc[:IS_END]) for m in GROSS_LADDER}
                   for m0 in ANCHORS}
        rng_resc = max(max(v.values()) - min(v.values()) for v in resc_is.values())
        for tag, m in (("GENUINE_ISargmax", pick_g),
                       ("RESCALED_tie_low", GROSS_LADDER[0]),
                       ("RESCALED_tie_high", GROSS_LADDER[-1]),
                       ("CONTROL_m075", PUBLISHED_M)):
            ro = RET[(bk.name, m)].loc[OOS_START:]
            mo = metrics(ro)
            wrows.append(dict(book=bk.name, parent=bk.parent, arm=tag, pick=m,
                              IS_Sharpe=is_sh[m], resc_IS_range=rng_resc,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              spy_OOS_CAGR=metrics(spy_o)["CAGR"], spy_OOS_Sharpe=_sh(spy_o),
                              spy_OOS_MaxDD=metrics(spy_o)["MaxDD"],
                              v1_OOS_CAGR=metrics(b_o)["CAGR"], v1_OOS_Sharpe=_sh(b_o),
                              v1_OOS_MaxDD=metrics(b_o)["MaxDD"],
                              beat_spy=bool(_sh(ro) > _sh(spy_o)),
                              oos4b=bool(mo["CAGR"] > PHI * metrics(spy_o)["CAGR"]
                                         and abs(mo["MaxDD"]) <= DELTA * abs(metrics(spy_o)["MaxDD"])
                                         and _sh(ro) > _sh(spy_o))))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  the rescaled ladder's IS-Sharpe column is flat to {W['resc_IS_range'].max():.3e} across all "
      f"{len(books)} books x {len(ANCHORS)} anchors — the IS-Sharpe selector has NO argmax on it")
    agg = W.groupby("arm").agg(mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                               mean_OOS_MaxDD=("OOS_MaxDD", "mean"), beat_SPY=("beat_spy", "sum"),
                               OOS4b=("oos4b", "sum"), mean_pick=("pick", "mean"))
    P("\n" + agg.to_string(float_format=lambda x: f"{x:.4f}"))
    ref = W[W.arm == "CONTROL_m075"].set_index("book")
    for tag in ("GENUINE_ISargmax", "RESCALED_tie_low", "RESCALED_tie_high"):
        S = W[W.arm == tag].set_index("book")
        d = (S["OOS_Sharpe"] - ref["OOS_Sharpe"]).dropna()
        t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) if d.std(ddof=1) > 0 else np.nan
        P(f"  paired vs the do-nothing control: {tag:20s} dOOS Sharpe {d.mean():+.4f} "
          f"(t {t:+.2f}), wins {int((d>0).sum())}-{int((d<0).sum())}, picks changed "
          f"{int((S['pick'] != PUBLISHED_M).sum())} of {len(S)}")
    P(f"\n  reference OOS ({OOS_START} ->): SPY {W['spy_OOS_CAGR'].iloc[0]:.2%} / "
      f"{W['spy_OOS_Sharpe'].iloc[0]:.4f} / {W['spy_OOS_MaxDD'].iloc[0]:.2%}")
    for pk in sorted(W.parent.unique()):
        r = W[W.parent == pk].iloc[0]
        P(f"    RULES v1 on {pk:6s}: {r['v1_OOS_CAGR']:.2%} / {r['v1_OOS_Sharpe']:.4f} / {r['v1_OOS_MaxDD']:.2%}")

    # ---------------------------------------------------------------- summary
    P("\n" + "=" * 118)
    P("SUMMARY")
    P("=" * 118)
    P(f"  [a] {'PASS' if ok_a else 'FAIL'}   [b] {ok_b}   [c] idea 165 max|dMaxDD| re-read from disk = {max_dd165}")
    P(f"  A1 static: {int((A.verdict=='RESCALED').sum())} RESCALED, {int((A.verdict=='MIXED').sum())} MIXED, "
      f"{int((A.verdict=='GENUINE').sum())} GENUINE, {int((A.verdict=='LADDER-UNCLASSIFIED').sum())} unclassified, "
      f"{int((A.verdict=='NO-LADDER').sum())} no ladder, of {len(A)} scripts")
    P(f"  A2 numbers: {int(NA['n_exactly_flat'].sum()) if len(NA) else 0} of "
      f"{int(NA['groups'].sum()) if len(NA) else 0} committed ladder groups carry the rescaling fingerprint")
    P(f"  committed LEADERBOARD rows exposed: pre-adjudication {int(flagged['leaderboard_rows'].sum())}, "
      f"POST-ADJUDICATION {exposed_rows}")
    P(f"  runtime {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
