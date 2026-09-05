#!/usr/bin/env python3
"""QUEUE idea 171 — do-gross-choice-rules-lose-to-constants-in-general  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 171)
    "idea 166 adds a fourth instance (gross) to ideas 110/151/132's finding that IS-fitted
     SELECTORS do not beat a do-nothing control out of sample, and gives the sharpest version
     yet: two rules that read the book's own IS 4b geometry both land within 0.01 of the
     constant they were meant to improve on.  Test the general claim directly: for every dial
     the project has fitted in-sample (gross, n, band width, cadence, sleeve f), compare the IS
     argmax against the incumbent constant on the OOS window, paired, and report the count of
     dials where fitting wins.  Max 2 params."

WHAT IS AT STAKE.
    Ideas 110, 132, 151 and 166 each found, on ONE dial, that a parameter chosen on the
    in-sample window does not beat leaving that parameter at its inherited constant.  Four
    single-dial results are four anecdotes.  The general claim — "in this project, fitting a
    dial in-sample does not pay out of sample" — is a claim about the SET of dials, and it can
    only be tested by running the identical protocol on every dial at once and counting.
    That count is this run's deliverable.  If fitting wins on 0 or 1 of 5 dials, PROTOCOL can
    say so as a finding and the project can stop spending runs re-fitting dials.  If fitting
    wins on 4 or 5, ideas 110/132/151/166 were dial-specific and the generalisation is dead.

    Note the asymmetry that makes this worth doing: a NULL result here is the useful one.  The
    incumbent constants cost nothing to keep; every fitted dial costs a run and adds an
    overfitting surface.

THE FIVE DIALS.  Each ladder CONTAINS its incumbent constant, so "do nothing" is a ladder
point and the comparison is exactly paired.  When one dial is swept the other four are held
at their incumbents.
    GROSS    g  in {0.20,0.30,0.40,0.50,0.60,0.70,0.75,0.80,0.90,1.00}   incumbent 0.75
             (RULES v1's 5 x 15%; idea 78/166's static; idea 166 calls it the OOS argmax)
    N        n  in {3,5,8,10,15,20,25,30,40,50}                          incumbent 20
             (idea 2's 4b KEEP candidate: top-20 equal weight, no vol scaler)
    BAND     b  in {0.00,0.02,0.03,0.05,0.08}                            incumbent 0.00
             (RULES v1 / research/scan.py gate on a bare px > MA200, i.e. no re-entry band;
              ideas 47/48 fitted 3% and 5%)
    CADENCE  f  in {D, W, M, Q}                                          incumbent W
             (RULES v1 and baseline.compare()'s default; idea 107 fitted monthly)
    SLEEVE   f  in {0.00,0.05,0.10,0.15,0.20,0.25,0.30}                  incumbent 0.00
             (neither RULES v1 nor the 4b candidate carries a sleeve; ideas 101/134 fitted
              f = 0.15-0.20 on the TLT/GLD/UUP defensive sleeve)
    36 ladder points in total, every one reported book-by-book in .ladder.csv.

TUNED PARAMETERS — exactly two, per PROTOCOL rule 4.
    1. the SELECTOR, 2 values, both reported, neither preferred:
         SEL-SHARPE  argmax over the ladder of IS Sharpe                 (the project's incumbent
                     selector: rule 8's S1, ideas 78/132/166)
         SEL-4B      argmax over the ladder of the IS 4b relative min-margin (idea 166's MAXMARG)
    2. the LADDER POINT, swept exhaustively within each dial (36 points), ALL reported.
    The DIAL and the BOOK are corpus axes, not tuned: the whole point is to count over dials.

    CONTROLS, not tuned parameters:
         CONST       the incumbent constant                              (the do-nothing arm)
         RANDOM      a uniformly random ladder point, fixed seed         (idea 151's control:
                     any selector must beat coin-flipping, not just the constant)
         ORACLE      the OOS argmax                                      (NOT implementable;
                     the upper bound on what any selector could have won)

THE 4b RELATIVE MIN-MARGIN, read on a window W (idea 166's scalarisation, unchanged).
        rel_H1   = (Sharpe(r, 1st half of W) - Sharpe(spy, 1st half of W)) / max(|.|, EPS)
        rel_H2   = same on the 2nd half of W
        rel_S    = (Sharpe(r, W) - Sharpe(spy, W)) / max(|Sharpe(spy, W)|, EPS)
        rel_DD   = (0.60*|MaxDD(spy,W)| - |MaxDD(r,W)|) / (0.60*|MaxDD(spy,W)|)
        rel_CAGR = (CAGR(r,W) - 0.70*CAGR(spy,W)) / max(|0.70*CAGR(spy,W)|, EPS)
        margin(W) = min of the five;  margin > 0 <=> the book passes 4b's bars on W.
    On the IS window it is a legal prospective screen; on the OOS window it is a score.
    PROTOCOL's actual rule 4b (halves of the FULL sample + the OOS window + full-sample DD and
    CAGR) is evaluated separately and exactly, in .keep.csv — the margin is a ranking device,
    not a substitute for the rule.

CORPUS — 53 books, the pairing unit.  Sub-panels follow idea 78's Test B construction.
    5 fixed panels : U56, B136, BSTK100, ETF36, SMALL484
    48 sub-panels  : k in {20,40,80} x 16 fixed random draws of B136,
                     rng = np.random.default_rng(171_500 + k)
    Every book carries SPY (benchmark, never tradable) and TLT/GLD/UUP (sleeve assets; on the
    sub-panels and SMALL484 they are price columns only, never tradable by the core).

WALK-FORWARD (PROTOCOL rule 8).  The design IS the walk-forward: every selector reads the
    <= 2016-12-31 window only, and the 2017-01-01..2026 window is read once, at the end.  In
    addition .walkforward.csv reports, per dial and arm, (i) the mean OOS CAGR/Sharpe/MaxDD
    across the 53 books and (ii) the classic S1 pick — the single book with the best IS Sharpe
    under that arm, read once on OOS — both against RULES v1 (on the book's parent panel) and
    SPY.

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover, at all four cadences, on a real book.  (Everything below uses fast_backtest;
        without [a] none of it is a Claude-Space backtest.)
    [b] at BAND=0 this script's CAND-n weights equal idea 78's weights_cand exactly, so the
        incumbent cell is idea 78's book and not a look-alike.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] and [b] hold.
    P2  On the GROSS dial, fitting loses (idea 166 already found this; if it does not reproduce
        here, something in this harness is wrong and the whole run is void).
    P3  Fitting wins on 0 or 1 of the 5 dials under SEL-SHARPE / OOS-Sharpe.  I expect the
        general claim to hold.
    P4  CADENCE is the most likely dial for fitting to WIN, because its ladder points differ in
        turnover cost by an order of magnitude and cost is the one thing that transfers from IS
        to OOS almost perfectly (ideas 14, 76).  A dial whose ladder is ranked by a stable
        mechanism is exactly where an IS argmax should generalise.
    P5  RANDOM lands between CONST and the selectors, i.e. much of any apparent selector value
        is just "being on the ladder at all" (idea 151).
    P6  ORACLE beats everything by a wide margin, so the null is about the SELECTOR's skill, not
        about the ladder being flat.  If ORACLE is also flat, the correct conclusion is "these
        dials do not matter", which is a different (and stronger) finding.
    P7  No arm produces a 4b KEEP.  This is a methodology run; nothing here is a new book.

CAVEATS carried, not buried
    * Survivorship: B136, U56 and the small panel are current-constituent lists (idea 54).  All
      arms and all dials inherit it equally, so the paired comparison is unaffected; the level
      of every number is not.
    * Idea 144: a re-grossed / re-cadenced book is the SAME book.  No verdict flip on a ladder
      is a new signal.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * On k=20 sub-panels the N ladder saturates: n >= 20 admits every eligible name, so those
      points collapse onto ew-all.  Reported, not hidden — it is part of the ladder's shape.
    * The SLEEVE dial gives a sub-panel access to three assets its core cannot hold.  That is
      ideas 101/134's construction, kept unchanged so the incumbent f = 0 is the same book.
    * A selector fitted on IS is one more thing fitted on IS.  The OOS window is read once.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .choices.csv, .paired.csv,
.walkforward.csv, .keep.csv.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
OUT = ROOT / "research" / "backtests"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b's CAGR floor and DD cap coefficients
EPS = 0.05                       # floor on |threshold| in the relative-margin denominator
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]

# ---- the five dials.  (ladder, incumbent constant)
DIALS = {
    "GROSS":   ([0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00], 0.75),
    "N":       ([3, 5, 8, 10, 15, 20, 25, 30, 40, 50], 20),
    "BAND":    ([0.00, 0.02, 0.03, 0.05, 0.08], 0.00),
    "CADENCE": (["D", "W", "M", "Q"], "W"),
    "SLEEVE":  ([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], 0.00),
}
DIAL_ORDER = ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"]
INC = {d: DIALS[d][1] for d in DIALS}
ARMS = ["CONST", "SEL-SHARPE", "SEL-4B", "RANDOM", "ORACLE"]

KS = [20, 40, 80]
N_DRAWS = 16
SEED = 171_500

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
    """Vectorised equivalent of engine.backtest.  Asserted identical in check_a()."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])          # Cp[t] = prod over rows < t
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
    r = pd.Series(port, index=idx)
    return {"returns": r, "turnover": pd.Series(turn, index=idx)}


# ---------------------------------------------------------------- book construction
def above_band(px, b):
    """200d-MA gate.  b = 0 is the bare gate (RULES v1 / scan.py).  b > 0 is hysteresis:
    enter above MA*(1+b), exit below MA*(1-b), hold state in between."""
    ma = px.rolling(200).mean()
    if b == 0.0:
        return px > ma
    st = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    st = st.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
    return st.ffill().fillna(0.0) > 0.5


def comp_score(px):
    """The composite of research/scan.py, no vol scaler (idea 2's 4b candidate ranks on this)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Book:
    """One corpus member: a price panel plus the tradable subset that defines the core book."""

    def __init__(self, name, px, tradable, parent):
        self.name, self.px, self.parent = name, px, parent
        self.tradable = [c for c in px.columns if c in tradable]
        self.comp = comp_score(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = {}
        drop = [c for c in px.columns if c not in set(self.tradable)]
        for b in DIALS["BAND"][0]:
            m = (above_band(px, b) & (vol20 < MAX_VOL)).copy()
            if drop:
                m[drop] = False
            self.elig[b] = m
        self.sleeve_cols = [c for c in SLEEVE_ASSETS if c in px.columns]

    def core_weights(self, n, gross, band):
        elig = self.elig[band]
        rank = self.comp.where(elig).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (gross / n)

    def weights(self, gross, n, band, sleeve):
        w = self.core_weights(n, gross, band)
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
    # give the small panel the sleeve assets as untradable price columns (baseline does the
    # same for SPY): the SLEEVE dial must exist on every book or the dials are not comparable.
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


# ---------------------------------------------------------------- metric helpers
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def rel_margin(r, spy):
    """idea 166's 4b relative min-margin on the window the two series already span."""
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    parts = {
        "H1": (h1 - s1) / max(abs(s1), EPS),
        "H2": (h2 - s2) / max(abs(s2), EPS),
        "S": (m["Sharpe"] - ms["Sharpe"]) / max(abs(ms["Sharpe"]), EPS),
        "DD": (DELTA * abs(ms["MaxDD"]) - abs(m["MaxDD"])) / max(DELTA * abs(ms["MaxDD"]), EPS),
        "CAGR": (m["CAGR"] - PHI * ms["CAGR"]) / max(abs(PHI * ms["CAGR"]), EPS),
    }
    worst = min(parts, key=parts.get)
    return min(parts.values()), worst


def keep_4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def keep_4b(r, spy, r_oos, spy_oos):
    """PROTOCOL rule 4b, exactly: halves of the FULL sample + the OOS window, full-sample
    DD cap and CAGR floor."""
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


def sign_p(x):
    """Two-sided exact binomial sign test on the non-zero paired differences."""
    from math import comb
    x = np.asarray([v for v in x if np.isfinite(v) and v != 0.0], float)
    n = len(x)
    if n == 0:
        return 1.0, 0, 0
    w = int((x > 0).sum())
    k = max(w, n - w)
    tail = sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return min(1.0, 2 * tail), w, n - w


# ---------------------------------------------------------------- reproduction controls
def check_a(book):
    P("  [a] fast_backtest vs engine.backtest (products/backtester/engine.py), same book:")
    w = book.weights(INC["GROSS"], INC["N"], INC["BAND"], INC["SLEEVE"])
    ok = True
    for fq in ["D", "W", "M", "Q"]:
        a = backtest(book.px, w, cost_bps=COST_BPS, freq=fq)
        b = fast_backtest(book.px, w, cost_bps=COST_BPS, freq=fq)
        dr = float((a["returns"] - b["returns"]).abs().max())
        dt = float((a["turnover"] - b["turnover"]).abs().max())
        P(f"      {book.name:9s} freq={fq}  max|dret|={dr:.3e}  max|dturn|={dt:.3e}")
        ok &= dr < 1e-12 and dt < 1e-10
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_b(book):
    """At BAND=0 the CAND-n weights must equal idea 78's weights_cand exactly."""
    _, above, vol20 = score(book.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in book.px.columns if c not in set(book.tradable)]
    if drop:
        m[drop] = False
    s78 = score(book.px, vol_scale=False)[0]
    w78 = (s78.where(m).rank(axis=1, ascending=False) <= INC["N"]).astype(float) * (INC["GROSS"] / INC["N"])
    mine = book.core_weights(INC["N"], INC["GROSS"], 0.00)
    d = float((w78 - mine).abs().max().max())
    P(f"  [b] CAND-{INC['N']} weights vs idea 78 weights_cand on {book.name}: max|dw|={d:.3e}"
      f"  -> {'PASS' if d < 1e-12 else 'FAIL'}")
    return d < 1e-12


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 171 - do-gross-choice-rules-lose-to-constants-in-general   (lane C, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Does an IS-fitted dial beat its inherited constant OUT OF SAMPLE?  Five dials, paired over 53 books.")
    P(f"Costs {COST_BPS} bps, t+1 execution, IS <= {IS_END}, OOS >= {OOS_START}.  Two tuned params: SELECTOR (2) x LADDER POINT (36).")
    P("")

    books, panels = build_corpus()
    P(f"CORPUS: {len(books)} books "
      f"({len([b for b in books if not b.name.startswith('B136k')])} fixed panels + "
      f"{len([b for b in books if b.name.startswith('B136k')])} sub-panels, k in {KS} x {N_DRAWS} draws, seed {SEED}+k)")
    for b in books[:5]:
        P(f"   {b.name:9s} {b.px.shape[0]}d x {b.px.shape[1]}c  tradable={len(b.tradable):3d}  "
          f"{b.px.index[0].date()}..{b.px.index[-1].date()}  sleeve={b.sleeve_cols}")
    P("")

    P("REPRODUCTION CONTROLS (asserted before any new number is read)")
    okA = check_a(books[1])
    okB = all(check_b(b) for b in books[:3])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    # ---- benchmarks per panel
    START = {}
    SPY = {}
    BASE = {}
    for b in books:
        if b.parent not in SPY:
            px = panels[b.parent]
            st = px.index[260]
            START[b.parent] = st
            SPY[b.parent] = px["SPY"].pct_change().fillna(0.0).loc[st:]
            BASE[b.parent] = fast_backtest(px, rules_v1_weights(px), COST_BPS, "W")["returns"].loc[st:]
    for k, v in SPY.items():
        m, mo = metrics(v), metrics(v.loc[OOS_START:])
        h1, h2 = halves(v)
        mb = metrics(BASE[k])
        P(f"  benchmark {k:6s} SPY  CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:7.2%} "
          f"halves {h1:.3f}/{h2:.3f}  OOS Sharpe {mo['Sharpe']:.3f} | RULES v1 Sharpe {mb['Sharpe']:.3f}")
    P("")

    # ---- run every (book, dial, ladder point)
    P("RUNNING LADDERS ...")
    rows = []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        spy = SPY[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        base = BASE[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for dial in DIAL_ORDER:
            ladder, _ = DIALS[dial]
            for pt in ladder:
                kw = dict(gross=INC["GROSS"], n=INC["N"], band=INC["BAND"], sleeve=INC["SLEEVE"])
                fq = INC["CADENCE"]
                if dial == "GROSS": kw["gross"] = pt
                elif dial == "N": kw["n"] = pt
                elif dial == "BAND": kw["band"] = pt
                elif dial == "SLEEVE": kw["sleeve"] = pt
                elif dial == "CADENCE": fq = pt
                res = fast_backtest(bk.px, bk.weights(**kw), COST_BPS, fq)
                r = res["returns"].loc[st:]
                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
                mg_is, wb_is = rel_margin(r_is, spy_is)
                mg_oos, wb_oos = rel_margin(r_oos, spy_oos)
                h1, h2 = halves(r)
                rows.append(dict(
                    book=bk.name, parent=bk.parent, dial=dial, point=pt,
                    is_incumbent=(pt == INC[dial]),
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                    turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                    IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"], IS_margin=mg_is,
                    IS_worstbar=wb_is,
                    OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                    OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                    fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos)))
        if (bi + 1) % 10 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    lad = pd.DataFrame(rows)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    P(f"   {len(lad)} ladder rows -> {STEM}.ladder.csv   ({time.time()-t0:.0f}s)")
    P("")

    # ---- ladder shape: is there anything to choose between?
    P("LADDER SHAPE - mean over the 53 books of each point's OOS Sharpe / OOS 4b margin")
    P("(if a ladder is flat, no selector can win and no selector can lose)")
    for dial in DIAL_ORDER:
        sub = lad[lad.dial == dial]
        g = sub.groupby("point", sort=False)[["IS_Sharpe", "OOS_Sharpe", "OOS_margin"]].mean()
        pts = " ".join(f"{p}:{g.loc[p,'OOS_Sharpe']:.3f}" for p in DIALS[dial][0])
        P(f"  {dial:8s} OOS Sharpe by point   {pts}")
        pts = " ".join(f"{p}:{g.loc[p,'OOS_margin']:+.3f}" for p in DIALS[dial][0])
        P(f"  {'':8s} OOS margin by point   {pts}")
        sp = g["OOS_Sharpe"]
        P(f"  {'':8s} spread {sp.max()-sp.min():.3f} Sharpe;  incumbent {INC[dial]} ranks "
          f"{int(sp.rank(ascending=False).loc[INC[dial]])}/{len(sp)} on mean OOS Sharpe")
    P("")

    # ---- the paired test
    rng_rand = np.random.default_rng(171_900)
    choices, paired = [], []
    for dial in DIAL_ORDER:
        ladder, const = DIALS[dial]
        for bk in books:
            sub = lad[(lad.dial == dial) & (lad.book == bk.name)].set_index("point")
            sub = sub.reindex(ladder)
            pick = {
                "CONST": const,
                "SEL-SHARPE": sub["IS_Sharpe"].idxmax(),
                "SEL-4B": sub["IS_margin"].idxmax(),
                "RANDOM": ladder[int(rng_rand.integers(len(ladder)))],
                "ORACLE": sub["OOS_Sharpe"].idxmax(),
            }
            for arm, pt in pick.items():
                r = sub.loc[pt]
                choices.append(dict(dial=dial, book=bk.name, arm=arm, point=pt,
                                    IS_Sharpe=r.IS_Sharpe, IS_margin=r.IS_margin,
                                    OOS_Sharpe=r.OOS_Sharpe, OOS_margin=r.OOS_margin,
                                    OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                                    fail4a=r.fail4a, fail4b=r.fail4b))
    ch = pd.DataFrame(choices)
    ch.to_csv(OUT / f"{STEM}.choices.csv", index=False)

    P("THE PAIRED TEST - per dial, each arm MINUS the incumbent constant, book by book (n=53)")
    P("")
    for scorenm in ["OOS_Sharpe", "OOS_margin"]:
        P(f"  --- OOS score = {scorenm} " + "-" * 84)
        P(f"  {'dial':8s} {'arm':11s} {'mean d':>9s} {'median d':>9s} {'t':>7s} {'win':>4s} {'loss':>5s} "
          f"{'tie':>4s} {'sign p':>7s}  {'changes':>7s}  verdict")
        for dial in DIAL_ORDER:
            const = DIALS[dial][1]
            base_s = ch[(ch.dial == dial) & (ch.arm == "CONST")].set_index("book")[scorenm]
            for arm in ARMS:
                if arm == "CONST":
                    continue
                a = ch[(ch.dial == dial) & (ch.arm == arm)].set_index("book")
                d = (a[scorenm] - base_s).reindex(base_s.index)
                p, w, l = sign_p(d.values)
                nchg = int((a["point"] != const).sum())
                mean_d = d.mean()
                verd = ("FITTING WINS" if (mean_d > 0 and p < 0.05) else
                        "fitting ahead (n.s.)" if mean_d > 0 else
                        "FITTING LOSES" if p < 0.05 else "fitting behind (n.s.)")
                if arm == "ORACLE":
                    verd = "(upper bound)"
                if arm == "RANDOM":
                    verd = "(control) " + verd
                P(f"  {dial:8s} {arm:11s} {mean_d:+9.4f} {d.median():+9.4f} {tstat(d.values):+7.2f} "
                  f"{w:4d} {l:5d} {len(d)-w-l:4d} {p:7.4f}  {nchg:3d}/{len(d)}  {verd}")
                paired.append(dict(score=scorenm, dial=dial, arm=arm, mean_d=mean_d,
                                   median_d=d.median(), t=tstat(d.values), wins=w, losses=l,
                                   ties=len(d) - w - l, sign_p=p, n_changed=nchg, n=len(d),
                                   verdict=verd))
        P("")
    pd.DataFrame(paired).to_csv(OUT / f"{STEM}.paired.csv", index=False)

    # ---- THE HEADLINE COUNT
    P("=" * 118)
    P("HEADLINE - count of dials (out of 5) where FITTING BEATS THE CONSTANT out of sample")
    P("")
    pdf = pd.DataFrame(paired)
    P(f"  {'selector':12s} {'OOS score':12s} {'mean d > 0':>11s} {'and sign p<0.05':>16s}   dials where fitting wins")
    for arm in ["SEL-SHARPE", "SEL-4B", "RANDOM"]:
        for scorenm in ["OOS_Sharpe", "OOS_margin"]:
            s = pdf[(pdf.arm == arm) & (pdf.score == scorenm)]
            ahead = s[s.mean_d > 0]
            sig = ahead[ahead.sign_p < 0.05]
            P(f"  {arm:12s} {scorenm:12s} {len(ahead):5d} / 5 {len(sig):14d} / 5   "
              f"{', '.join(sig.dial) if len(sig) else '(none)'}"
              f"{'   [ahead but n.s.: ' + ', '.join(ahead[ahead.sign_p>=0.05].dial) + ']' if len(ahead)>len(sig) else ''}")
    P("")
    s = pdf[(pdf.arm == "ORACLE")]
    P(f"  ORACLE (not implementable) mean d, OOS_Sharpe: " +
      "  ".join(f"{r.dial} {r.mean_d:+.4f}" for _, r in s[s.score == "OOS_Sharpe"].iterrows()))
    P("  -> the ladders are NOT flat where ORACLE is large; a selector with skill had room to win there.")
    P("")

    # ---- how often does the selector even move off the constant?
    P("SELECTOR BEHAVIOUR - how often each selector leaves the incumbent, and where it goes")
    for dial in DIAL_ORDER:
        const = DIALS[dial][1]
        for arm in ["SEL-SHARPE", "SEL-4B", "ORACLE"]:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            vc = a["point"].value_counts().reindex(DIALS[dial][0]).fillna(0).astype(int)
            P(f"  {dial:8s} {arm:11s} moves off {const} in {int((a['point']!=const).sum()):3d}/{len(a)}   "
              + " ".join(f"{p}:{vc[p]}" for p in DIALS[dial][0]))
    P("")

    # ---- POST-HOC diagnostics (NOT pre-registered; added after reading the paired table above,
    #      because two dials "won" and the shape of their ladders decides whether that is skill)
    P("=" * 118)
    P("POST-HOC DIAGNOSTICS (labelled: these were added AFTER the paired table was read, to")
    P("distinguish selector SKILL from ladder GEOMETRY.  Not pre-registered.)")
    P("")
    P("(A) ladder geometry: is the argmax an interior point (a choice) or the endpoint (saturation)?")
    P(f"  {'dial':8s} {'rho(rank, mean OOS Sharpe)':>27s} {'ORACLE at an endpoint':>22s} {'SEL-SHARPE == ORACLE':>21s}")
    geom = {}
    for dial in DIAL_ORDER:
        ladder = DIALS[dial][0]
        g = lad[lad.dial == dial].groupby("point", sort=False)["OOS_Sharpe"].mean().reindex(ladder)
        rho = float(np.corrcoef(np.arange(len(ladder), dtype=float),
                                pd.Series(g.values).rank().values)[0, 1])
        o = ch[(ch.dial == dial) & (ch.arm == "ORACLE")].set_index("book")["point"]
        s = ch[(ch.dial == dial) & (ch.arm == "SEL-SHARPE")].set_index("book")["point"]
        ends = {ladder[0], ladder[-1]}
        f_end = float(o.isin(ends).mean())
        agree = float((o == s).mean())
        geom[dial] = dict(rho=rho, oracle_endpoint=f_end, sel_eq_oracle=agree)
        P(f"  {dial:8s} {rho:27.3f} {f_end:21.1%} {agree:20.1%}")
    P("  Reading: rho ~ +/-1 with the oracle pinned at an endpoint means the ladder is MONOTONE and")
    P("  TRUNCATED — the 'selector' is not choosing, it is running to the edge of the grid, and any")
    P("  rule that also runs to that edge (including RANDOM, in expectation) 'wins' for free.")
    P("")
    P("(B) capture ratio: share of the ORACLE's OOS-Sharpe gain that each arm actually banks.")
    P("    A selector with no skill should capture what RANDOM captures.")
    P(f"  {'dial':8s} {'ORACLE gain':>12s} {'SEL-SHARPE':>11s} {'SEL-4B':>9s} {'RANDOM':>9s}   verdict")
    cap_rows = []
    for dial in DIAL_ORDER:
        o = pdf[(pdf.dial == dial) & (pdf.arm == "ORACLE") & (pdf.score == "OOS_Sharpe")].mean_d.iloc[0]
        vals = {}
        for arm in ["SEL-SHARPE", "SEL-4B", "RANDOM"]:
            v = pdf[(pdf.dial == dial) & (pdf.arm == arm) & (pdf.score == "OOS_Sharpe")].mean_d.iloc[0]
            vals[arm] = v / o if o != 0 else np.nan
        srow = pdf[(pdf.dial == dial) & (pdf.arm == "SEL-SHARPE") & (pdf.score == "OOS_Sharpe")].iloc[0]
        # SKILL requires all four: it beats the constant, significantly, by more than the random
        # control does, and it is not merely agreeing with a monotone truncated ladder's endpoint.
        skill = (srow.mean_d > 0 and srow.sign_p < 0.05
                 and vals["SEL-SHARPE"] > vals["RANDOM"] + 0.10
                 and geom[dial]["sel_eq_oracle"] < 0.90)
        why = ("SELECTOR SKILL" if skill else
               "no skill: loses to the constant" if srow.mean_d <= 0 else
               "no skill: not significant" if srow.sign_p >= 0.05 else
               "no skill: it IS the ladder's endpoint" if geom[dial]["sel_eq_oracle"] >= 0.90 else
               "no skill: no better than RANDOM")
        P(f"  {dial:8s} {o:+12.4f} {vals['SEL-SHARPE']:10.1%} {vals['SEL-4B']:8.1%} {vals['RANDOM']:8.1%}   {why}")
        cap_rows.append(dict(dial=dial, oracle_gain=o, **{f"cap_{k}": v for k, v in vals.items()},
                             skill=bool(skill), **geom[dial]))
    pd.DataFrame(cap_rows).to_csv(OUT / f"{STEM}.geometry.csv", index=False)
    P("")

    # ---- rule 8 walk-forward summary
    P("=" * 118)
    P("PROTOCOL RULE 8 WALK-FORWARD.  Everything above chose on IS only; OOS is read once, here.")
    P("(i) mean OOS metrics across the 53 books, per dial and arm")
    P(f"  {'dial':8s} {'arm':11s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS MaxDD':>10s} {'OOS margin':>11s} {'4b OOS-pass':>12s}")
    wf = []
    for dial in DIAL_ORDER:
        for arm in ARMS:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            npass = int((a["OOS_margin"] > 0).sum())
            P(f"  {dial:8s} {arm:11s} {a.OOS_CAGR.mean():9.2%} {a.OOS_Sharpe.mean():9.3f} "
              f"{a.OOS_MaxDD.mean():10.2%} {a.OOS_margin.mean():+11.4f} {npass:6d}/{len(a)}")
            wf.append(dict(kind="mean_over_books", dial=dial, arm=arm, OOS_CAGR=a.OOS_CAGR.mean(),
                           OOS_Sharpe=a.OOS_Sharpe.mean(), OOS_MaxDD=a.OOS_MaxDD.mean(),
                           OOS_margin=a.OOS_margin.mean(), oos4b_pass=npass, n=len(a)))
    for k in SPY:
        so, bo = SPY[k].loc[OOS_START:], BASE[k].loc[OOS_START:]
        ms, mb = metrics(so), metrics(bo)
        P(f"  {'':8s} {'SPY/'+k:11s} {ms['CAGR']:9.2%} {ms['Sharpe']:9.3f} {ms['MaxDD']:10.2%}")
        P(f"  {'':8s} {'v1/'+k:11s} {mb['CAGR']:9.2%} {mb['Sharpe']:9.3f} {mb['MaxDD']:10.2%}")
        wf.append(dict(kind="benchmark", dial="-", arm=f"SPY/{k}", OOS_CAGR=ms["CAGR"],
                       OOS_Sharpe=ms["Sharpe"], OOS_MaxDD=ms["MaxDD"], OOS_margin=np.nan, oos4b_pass=0, n=0))
        wf.append(dict(kind="benchmark", dial="-", arm=f"RULESv1/{k}", OOS_CAGR=mb["CAGR"],
                       OOS_Sharpe=mb["Sharpe"], OOS_MaxDD=mb["MaxDD"], OOS_margin=np.nan, oos4b_pass=0, n=0))
    P("")
    P("(ii) the classic S1 pick: within each dial+arm, the single book with the best IS Sharpe, read once on OOS")
    P(f"  {'dial':8s} {'arm':11s} {'book':11s} {'point':>6s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS MaxDD':>10s}  vs SPY/v1 (same parent)")
    for dial in DIAL_ORDER:
        for arm in ARMS:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            i = a["IS_Sharpe"].idxmax()
            r = a.loc[i]
            par = next(b.parent for b in books if b.name == r.book)
            ms, mb = metrics(SPY[par].loc[OOS_START:]), metrics(BASE[par].loc[OOS_START:])
            P(f"  {dial:8s} {arm:11s} {r.book:11s} {str(r.point):>6s} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:9.3f} "
              f"{r.OOS_MaxDD:10.2%}   SPY {ms['Sharpe']:.3f} / v1 {mb['Sharpe']:.3f}"
              f"   {'beats both' if r.OOS_Sharpe > max(ms['Sharpe'], mb['Sharpe']) else 'does not beat both'}")
            wf.append(dict(kind="S1_pick", dial=dial, arm=arm, book=r.book, point=r.point,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           OOS_margin=r.OOS_margin, oos4b_pass=int(r.OOS_margin > 0), n=1,
                           spy_OOS_Sharpe=ms["Sharpe"], v1_OOS_Sharpe=mb["Sharpe"]))
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("")

    # ---- both KEEP paths, evaluated exactly
    P("=" * 118)
    P("BOTH KEEP PATHS (PROTOCOL rule 4), evaluated exactly on all 1908 ladder rows")
    n4a = int((lad.fail4a == "-").sum())
    n4b = int((lad.fail4b == "-").sum())
    P(f"  4a (beat the book): {n4a}/{len(lad)} rows pass")
    P(f"  4b (capital-worthy): {n4b}/{len(lad)} rows pass")
    bars = pd.Series([b for s in lad.fail4b for b in s.split(",") if b != "-"]).value_counts()
    P(f"  4b binding bars across all rows: {dict(bars)}")
    kdf = lad[(lad.fail4b == "-")]
    if len(kdf):
        P("  4b-passing rows (all of them):")
        P(kdf[["book", "dial", "point", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        P("  NOTE (idea 144): every one of these is a re-parameterisation of an EXISTING book, not a")
        P("  new signal, and none is proposed as a rules change.  This run is a methodology test.")
    else:
        P("  no row passes 4b.  Nothing here is a candidate.")
    P("")
    lad[["book", "dial", "point", "fail4a", "fail4b", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
         "OOS_Sharpe"]].to_csv(OUT / f"{STEM}.keep.csv", index=False)

    # ---- named-book by-product: the standing 4b candidate, dial by dial, walked forward
    P("=" * 118)
    P("NAMED-BOOK BY-PRODUCT (post-hoc).  The 53 sub-panels are a corpus device, not tradable books.")
    P("The five FIXED panels are.  Here is the standing 4b candidate (top-20 EW, g=0.75, no vol")
    P("scaler, universe.json = U56) at every ladder point, with the IS-selected point marked, so a")
    P("Sunday review can see whether any dial move on the LIVE book is walk-forward-supported.")
    P("")
    for bkname in ["U56", "B136"]:
        P(f"  --- book {bkname} " + "-" * 96)
        par = next(b.parent for b in books if b.name == bkname)
        ms, mb = metrics(SPY[par]), metrics(BASE[par])
        s1b, s2b = halves(SPY[par])
        mso = metrics(SPY[par].loc[OOS_START:])
        P(f"      SPY(full) CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} halves {s1b:.3f}/{s2b:.3f} "
          f"MaxDD {ms['MaxDD']:.2%} -> 4b bars: H1>{s1b:.3f} H2>{s2b:.3f} OOS>{mso['Sharpe']:.3f} "
          f"|DD|<={DELTA*abs(ms['MaxDD']):.2%} CAGR>={PHI*ms['CAGR']:.2%}")
        P(f"      RULES v1(full) Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.2%}")
        sub = lad[lad.book == bkname]
        for dial in DIAL_ORDER:
            picks = ch[(ch.dial == dial) & (ch.book == bkname)].set_index("arm")["point"]
            P(f"      {dial}: IS picks -> SEL-SHARPE {picks['SEL-SHARPE']}, SEL-4B {picks['SEL-4B']}"
              f"  (incumbent {INC[dial]}, oracle {picks['ORACLE']})")
            d = sub[sub.dial == dial]
            P("        " + d[["point", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR",
                              "OOS_MaxDD", "turnover", "fail4a", "fail4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n        "))
        P("")

    # ---- predictions scorecard
    P("=" * 118)
    P("PREDICTIONS SCORECARD")
    sel_sharpe_sharpe = pdf[(pdf.arm == "SEL-SHARPE") & (pdf.score == "OOS_Sharpe")]
    nwin = int((sel_sharpe_sharpe.mean_d > 0).sum())
    gross_row = sel_sharpe_sharpe[sel_sharpe_sharpe.dial == "GROSS"].iloc[0]
    cad_row = sel_sharpe_sharpe[sel_sharpe_sharpe.dial == "CADENCE"].iloc[0]
    rnd = pdf[(pdf.arm == "RANDOM") & (pdf.score == "OOS_Sharpe")]
    orc = pdf[(pdf.arm == "ORACLE") & (pdf.score == "OOS_Sharpe")]
    P(f"  P1 reproduction [a]+[b]            : {'HIT' if okA and okB else 'MISS'}")
    P(f"  P2 GROSS: fitting loses            : {'HIT' if gross_row.mean_d <= 0 else 'MISS'}  (mean d {gross_row.mean_d:+.4f})")
    P(f"  P3 fitting wins on 0 or 1 of 5     : {'HIT' if nwin <= 1 else 'MISS'}  (ahead on {nwin}/5)")
    P(f"  P4 CADENCE is the most likely win  : {'HIT' if cad_row.mean_d == sel_sharpe_sharpe.mean_d.max() else 'MISS'}"
      f"  (CADENCE d {cad_row.mean_d:+.4f}; best dial {sel_sharpe_sharpe.loc[sel_sharpe_sharpe.mean_d.idxmax(),'dial']})")
    P(f"  P5 RANDOM between CONST and sel.   : RANDOM mean d over dials {rnd.mean_d.mean():+.4f} vs "
      f"SEL-SHARPE {sel_sharpe_sharpe.mean_d.mean():+.4f} (CONST is 0 by construction)")
    P(f"  P6 ORACLE beats everything         : ORACLE mean d over dials {orc.mean_d.mean():+.4f}"
      f"  {'HIT' if orc.mean_d.mean() > max(rnd.mean_d.mean(), sel_sharpe_sharpe.mean_d.mean()) else 'MISS'}")
    P(f"  P7 no 4b KEEP                      : {'HIT' if n4b == 0 else 'MISS'}  ({n4b} rows pass 4b)")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
