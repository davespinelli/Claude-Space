#!/usr/bin/env python3
"""QUEUE idea 187 - is-6W-a-grid-edge-or-a-real-optimum   (lane B, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 187)
    "idea 175 found the OOS argmax sits at 6W in 60.9% of 115 books (97% on u56/ETF) on a
     ladder whose last point is Q, i.e. the winner is ONE STEP from the edge and idea 183's
     anchor-position caveat applies to it directly.  Extend the ladder past 6W (7W, 8W, 2M,
     10W, Q) on the same corpus and report whether the argmax moves again.  If it does,
     'slower is better' is a truncation artefact and the monthly constant is the safe read.
     Max 2 params."

WHAT IS AT STAKE.
    Idea 175's headline geometric fact is that mean OOS Sharpe RISES monotonically from D
    (0.621) to 6W (0.780) and then COLLAPSES at Q (0.539), and that 6W is the OOS argmax in
    60.9% of 115 books.  Two readings are observationally identical on a 7-point ladder whose
    penultimate point is 6W (8.7 rebalances/yr) and whose last is Q (4.0):

      (i)  REAL INTERIOR OPTIMUM.  There is a genuine hump; the signal decays over ~6-8 weeks
           and rebalancing slower than that is stale.  6W wins because it sits on the hump.
      (ii) TRUNCATION ARTEFACT.  "Slower is better" is still running when the ladder stops.
           6W wins because it is the slowest point that is not Q, and Q is so far away
           (a 2.2x cadence jump, the largest gap on the whole ladder) that the ladder cannot
           see where the curve actually turns.  If the true argmax is 8W or 2M, then every
           "6W beats M" claim in the record is a statement about grid resolution and idea 175's
           96.2%-interior / 60.9%-modal numbers do not survive re-gridding.

    Idea 183's anchor-position caveat is exactly this: a claim that instrument X beats control C
    is partly a claim about where C sits on X's ladder, and 6W's rank is an artefact of the
    ladder's endpoint.  This run changes ONE thing about idea 175 - the GRID - and nothing else.

    A NULL here (the argmax stays in the 6W neighbourhood and does NOT run to the new edge) is
    the useful result: it converts idea 175's 6W from a grid coordinate into a measured hump.

THE LADDER - CADENCE, 13 points.  The 7 original points UNCHANGED, 6 new ones added.
    ORIGINAL 7 (idea 175, reproduced bar-for-bar in control [c]):
      D  every bar | 2D every 2nd bar | W ISO week (INCUMBENT, RULES v1) | 2W | M | 6W | Q
    NEW 6, filling the 6W->Q gap AND extending PAST Q so the new argmax can be interior:
      7W  8W  2M  10W        (the four the idea names, between 6W and Q)
      16W 2Q                 (added BEYOND Q, without which this run would repeat idea 175's
                              own mistake: if the argmax lands on Q the answer is undefined.
                              Pre-registered before any number was read.)
    Ladder order is by cadence LENGTH: D,2D,W,2W,M,6W,7W,8W,2M,10W,Q,16W,2Q.
    ALL 13 points are reported for every book.  Nothing is picked for reporting.

    Every other dial is pinned at idea 175's incumbents, unchanged, so the book is identical:
    GROSS 0.75, N 20, BAND 0.00 (bare 200d + vol20 gate), SLEEVE 0.00, COST 10 bps, t+1.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4, identical to idea 175.
    1. the SELECTOR, 2 values, both reported, neither preferred:
         SEL-SHARPE  argmax over the ladder of IS Sharpe          (rule 8's S1, the incumbent)
         SEL-4B      argmax over the ladder of the IS 4b relative min-margin (idea 166)
    2. the LADDER POINT, swept exhaustively (13 points), ALL reported.
    PANEL and BOOK are corpus axes, not tuned parameters.  Extending a swept grid is not a
    third parameter; it is the whole content of the idea.

    CONTROLS, not tuned parameters:
         CONST-W   the incumbent constant W        (RULES v1's cadence; idea 175's pairing base)
         CONST-6W  the point under test            (the SECOND pairing base, added by this idea)
         RANDOM    a uniformly random ladder point per book, fixed seed   (idea 151's control)
         ORACLE    the OOS argmax                  (NOT implementable; the upper bound)

CORPUS - 115 books, byte-identical to idea 175's (same seeds, same draws, same panels).
    3 fixed panels : SMALL439, U56, ETF36
    48 SMALL sub-panels : k in {20,40,80} x 16 draws, rng = default_rng(175_500 + k)
    32 U56   sub-panels : k in {20,40}    x 16 draws, rng = default_rng(175_600 + k)
    32 ETF   sub-panels : k in {12,24}    x 16 draws, rng = default_rng(175_700 + k)
    SMALL439: the sub-$2B panel with every ticker whose data/small_meta.csv max_1d_move >= 1.0
    dropped first, per standing instruction.  SPY is a benchmark column, never tradable.
    Re-using the corpus is deliberate: the idea says "on the same corpus", and holding it fixed
    is what makes the 7 shared points an exact reproduction control rather than a re-run.

WALK-FORWARD (PROTOCOL rule 8) - the design IS the walk-forward.
    Every selector reads the <= 2016-12-31 window only.  The 2017-01-01.. window is read once.
    .walkforward.csv reports, per arm, mean OOS CAGR/Sharpe/MaxDD over all 115 books and the
    classic S1 pick (best IS Sharpe book), against RULES v1 on the parent panel and against SPY.

BOTH KEEP PATHS are evaluated on every one of the 1495 ladder rows and written to .keep.csv:
    4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND on the OOS window, MaxDD <= 0.60 x |SPY MaxDD|,
        CAGR >= 0.70 x SPY CAGR.

REPRODUCTION, asserted before any new number is read
    [a] cad_mask reproduces engine.rebalance_mask exactly at D, W, M, Q.  The nine block points
        (2D, 2W, 6W, 7W, 8W, 2M, 10W, 16W, 2Q) are built by the same "last bar of each block"
        rule, so [a] licenses them.  Rebalances/yr is printed for all 13 so the ladder can be
        read in cadence units and the new points confirmed monotone in length.
    [b] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover at D, W, M, Q on a real book.
    [c] THE DECISIVE CONTROL: on the 7 points idea 175 ran, this script's ladder rows must equal
        idea 175's committed .ladder.csv to < 1e-9 on every numeric column, on all 805 shared
        rows, with 0 verdict mismatches.  If [c] fails, the corpus or the book has moved and the
        comparison of new points to old ones is meaningless.  Run stops.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b], [c] all hold.
    P2  THE ARGMAX MOVES OFF 6W on the pooled ladder.  With 7W/8W/2M/10W available I expect the
        mean-OOS-Sharpe argmax to land in {7W, 8W, 2M} rather than staying at 6W, simply because
        6W's win was measured against a 2.2x-distant Q.  This alone does NOT settle the idea.
    P3  BUT the argmax is INTERIOR on the extended ladder: it does not land on 2Q (the new edge)
        and the curve turns over by 10W at the latest.  Ergo (ii) TRUNCATION is REFUTED and the
        hump is real, just mis-located by one grid step.  This is the pre-registered answer.
    P4  The MODAL-ARGMAX SHARE COLLAPSES from 60.9% by pure grid dilution - four near-duplicate
        neighbours split one mode - so the honest statistic is the ZONE share (fraction of books
        whose OOS argmax lies in the 6W..10W band), which I expect to be HIGHER than idea 175's
        60.9%, not lower.  Any "modal share fell" reading of this run would be an artefact.
    P5  The plateau is flat (idea 128): the mean OOS Sharpe spread across {6W,7W,8W,2M,10W} is
        smaller than the 6W-minus-M gap idea 175 published (+0.024 pooled, +0.117 U56, +0.087
        ETF), i.e. the five slow points are not distinguishable from each other and NO single
        one of them is writable into RULES.
    P6  The small family still wants M (idea 188's finding): SMALL's argmax stays at or faster
        than M while U56/ETF sit in the 6W..2M zone.  The three-way family split survives.
    P7  SEL-SHARPE's IS pick stays modal at M (IS Sharpe peaked at M in all 3 families in idea
        175 and the new points are all slower than M), so the selector does NOT chase the OOS
        hump and the IS/OOS disagreement idea 175 found gets WIDER, not narrower.
    P8  No NEW 4b KEEP on the three fixed panels beyond a re-cadencing of an existing book
        (idea 144: a re-cadenced book is the same book).

CAVEATS carried, not buried
    * SURVIVORSHIP.  SMALL439/U56/ETF36 are current-constituent lists (data/SMALL_PANEL_README.md,
      idea 54).  Every ladder point inherits the bias equally so the PAIRED comparison is
      unaffected; no LEVEL here is an attainable return.
    * Idea 38: data/prices.csv is calendar-day indexed from 2014-09-17, so a "bar" on U56/ETF36
      is a calendar day after that date.  D and 2D therefore rebalance on some non-trading days
      (a no-op in weights) and it shifts which day the week-block points land on.  The small
      panel is trading-day indexed.  Rebalances/yr is printed per point.
    * BLOCK PHASE.  Week-block points (2W,6W,7W,8W,10W,16W) are anchored on the first ISO week
      of the panel and month/quarter-block points (2M,2Q) on the first month/quarter, i.e. the
      block grid has a PHASE that is a property of the sample start.  A 7W ladder point is
      "every 7th week counting from 2008/2010", not "the best 7-week phase".  No phase is
      optimised; that would be a third parameter.
    * Idea 144: a re-cadenced book is the SAME book.  A verdict flip along this ladder is not a
      new signal.
    * Idea 126: t+1 execution only, 10 bps only.  Idea 188 established the D/M/6W split is NOT a
      cost effect (it survives at 0 bps), so a cost ladder is not re-run here.
    * A selector fitted on IS is one more thing fitted on IS.  The OOS window is read once.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .shape.csv, .choices.csv,
.paired.csv, .constants.csv, .walkforward.csv, .keep.csv, .zone.csv, and (post-hoc, labelled)
.phase.csv / .phasesummary.csv.
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

STEM = "2026-09-06_is-6W-a-grid-edge-or-a-real-optimum_B"
PARENT_STEM = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"
OUT = ROOT / "research" / "backtests"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
EPS = 0.05

# ---- the dial under test.  Idea 175's 7 points + the 6 this idea adds, ordered by length.
OLD_LADDER = ["D", "2D", "W", "2W", "M", "6W", "Q"]
LADDER = ["D", "2D", "W", "2W", "M", "6W", "7W", "8W", "2M", "10W", "Q", "16W", "2Q"]
NEW_POINTS = [p for p in LADDER if p not in OLD_LADDER]
CONST_PT = "W"          # RULES v1's cadence; idea 175's pairing base
TEST_PT = "6W"          # the point idea 187 is about; the second pairing base
ZONE = ["6W", "7W", "8W", "2M", "10W"]   # the "slow hump" zone, pre-registered

INC_GROSS, INC_N, INC_BAND = 0.75, 20, 0.00
ARMS = ["CONST-W", "CONST-6W", "SEL-SHARPE", "SEL-4B", "RANDOM", "ORACLE"]

FAMILIES = ["SMALL", "U56", "ETF"]
DRAWS = {"SMALL": (175_500, [20, 40, 80]), "U56": (175_600, [20, 40]), "ETF": (175_700, [12, 24])}
N_DRAWS = 16

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- cadence masks
# week-block and period-block specs.  D/2D are bar-count blocks.
_WEEK_K = {"W": 1, "2W": 2, "6W": 6, "7W": 7, "8W": 8, "10W": 10, "16W": 16}
_PER_K = {"M": ("M", 1), "2M": ("M", 2), "Q": ("Q", 1), "2Q": ("Q", 2)}


def cad_mask(idx, cad, phase=0):
    """True on the last bar of each cadence block.  Same 'last bar of the block' rule as
    engine.rebalance_mask; blocks are bars (D/2D), ISO weeks (W..16W) or calendar months /
    quarters (M,2M,Q,2Q).  Asserted equal to engine.rebalance_mask at D/W/M/Q in check_a().

    phase shifts the block grid by `phase` weeks (week points) or periods (month/quarter
    points).  phase=0 anchors on the first bar of the panel and IS the ladder convention used
    everywhere above; phase>0 is used ONLY by the labelled post-hoc phase control."""
    n = len(idx)
    if cad == "D":
        key = np.arange(n)
    elif cad == "2D":
        key = (np.arange(n) + phase) // 2
    elif cad in _WEEK_K:
        ordi = np.asarray(idx.to_period("W").astype("int64"))
        ordi = ordi - ordi[0]
        key = (ordi + phase) // _WEEK_K[cad]
    elif cad in _PER_K:
        f, k = _PER_K[cad]
        ordi = np.asarray(idx.to_period(f).astype("int64"))
        key = ordi if (k == 1 and phase == 0) else (ordi - ordi[0] + phase) // k
    else:
        raise ValueError(cad)
    m = np.empty(n, bool)
    m[:-1] = key[:-1] != key[1:]
    m[-1] = True
    return pd.Series(m, index=idx)


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=COST_BPS, cad="W", phase=0):
    """Vectorised equivalent of engine.backtest, taking a cadence string cad_mask understands.
    Asserted identical to the engine in check_b().  Copied unchanged from idea 175."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad, phase).shift(1, fill_value=False).values.copy()
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


# ---------------------------------------------------------------- book construction
def comp_score(px):
    """The composite of research/scan.py, no vol scaler (idea 2's 4b candidate ranks on this)."""
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

    def weights(self, n=INC_N, gross=INC_GROSS):
        rank = self.comp.where(self.elig).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (gross / n)


def build_corpus():
    """Byte-identical to idea 175's build_corpus (same seeds, same order)."""
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    pxs = load_universe(small=True)

    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  small panel: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} tradable")
    pxs = pxs[s_stk + ["SPY"]]

    u_stk = [c for c in px56.columns if c != "SPY"]
    e_stk = [t for t in etf36 if t in px56.columns and t != "SPY"]

    def keep(px, cols):
        cols = [c for c in cols if c in px.columns]
        return px[list(dict.fromkeys(cols + ["SPY"]))].dropna(how="all").ffill()

    books = [
        Book("SMALL439", keep(pxs, s_stk), set(s_stk), "SMALL"),
        Book("U56", keep(px56, u_stk), set(u_stk), "U56"),
        Book("ETF36", keep(px56, e_stk), set(e_stk), "U56"),
    ]
    pools = {"SMALL": (pxs, s_stk), "U56": (px56, u_stk), "ETF": (px56, e_stk)}
    for fam in FAMILIES:
        seed, ks = DRAWS[fam]
        pxp, pool = pools[fam]
        for k in ks:
            rng = np.random.default_rng(seed + k)
            for d in range(N_DRAWS):
                sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
                par = "SMALL" if fam == "SMALL" else "U56"
                books.append(Book(f"{fam}k{k}d{d:02d}", keep(pxp, sub), set(sub), par))
    return books, {"U56": px56, "SMALL": pxs}


def family_of(name):
    if name.startswith("SMALL"):
        return "SMALL"
    if name.startswith("U56"):
        return "U56"
    return "ETF"


# ---------------------------------------------------------------- metric helpers
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def rel_margin(r, spy):
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
    P("  [a] cad_mask vs engine.rebalance_mask at the four engine-supported points, and")
    P("      rebalances/yr for all 13 (must be monotone decreasing in ladder order):")
    ok = True
    yr = {}
    for cd in LADDER:
        b = cad_mask(book.px.index, cd)
        yr[cd] = b.sum() / (len(b) / 252)
        if cd in ("D", "W", "M", "Q"):
            a = rebalance_mask(book.px.index, cd)
            same = bool((a.values == b.values).all())
            P(f"      {cd:3s} identical={same}   rebalances/yr={yr[cd]:6.1f}")
            ok &= same
        else:
            P(f"      {cd:3s} (block point)   rebalances/yr={yr[cd]:6.1f}")
    mono = all(yr[LADDER[i]] >= yr[LADDER[i + 1]] - 1e-9 for i in range(len(LADDER) - 1))
    P(f"      monotone in ladder order={mono}   -> {'PASS' if (ok and mono) else 'FAIL'}")
    return ok and mono


def check_b(book):
    P("  [b] fast_backtest vs engine.backtest (products/backtester/engine.py), same book:")
    w = book.weights()
    ok = True
    for cd in ["D", "W", "M", "Q"]:
        a = backtest(book.px, w, cost_bps=COST_BPS, freq=cd)
        b = fast_backtest(book.px, w, cost_bps=COST_BPS, cad=cd)
        dr = float((a["returns"] - b["returns"]).abs().max())
        dt = float((a["turnover"] - b["turnover"]).abs().max())
        P(f"      {book.name:9s} cad={cd:2s}  max|dret|={dr:.3e}  max|dturn|={dt:.3e}")
        ok &= dr < 1e-12 and dt < 1e-10
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_c(lad):
    """THE decisive control: the 7 shared points must equal idea 175's committed ladder.csv."""
    P(f"  [c] shared-point reproduction vs {PARENT_STEM}.ladder.csv")
    src = OUT / f"{PARENT_STEM}.ladder.csv"
    if not src.exists():
        P(f"      *** parent ladder.csv not found at {src} -> FAIL")
        return False
    old = pd.read_csv(src)
    new = lad[lad.point.isin(OLD_LADDER)].copy()
    keys = ["book", "point"]
    num = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
           "IS_margin", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]
    m = old.merge(new, on=keys, suffixes=("_o", "_n"), how="inner")
    P(f"      rows: parent={len(old)}  this-run shared={len(new)}  matched={len(m)}")
    worst, worstcol = 0.0, ""
    for c in num:
        d = float((m[c + "_o"] - m[c + "_n"]).abs().max())
        if d > worst:
            worst, worstcol = d, c
    vm = int((m["fail4a_o"] != m["fail4a_n"]).sum() + (m["fail4b_o"] != m["fail4b_n"]).sum())
    bm = int((m["IS_worstbar_o"] != m["IS_worstbar_n"]).sum() + (m["OOS_worstbar_o"] != m["OOS_worstbar_n"]).sum())
    ok = (len(m) == len(old) == len(new)) and worst < 1e-9 and vm == 0 and bm == 0
    P(f"      max|d| over {len(num)} numeric columns = {worst:.3e} (worst column: {worstcol})")
    P(f"      verdict-string mismatches (fail4a+fail4b) = {vm};  worst-bar mismatches = {bm}")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 187 - is-6W-a-grid-edge-or-a-real-optimum   (lane B, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Idea 175's OOS argmax sat at 6W in 60.9% of 115 books on a ladder whose LAST point was Q,")
    P("i.e. one step from the edge across the ladder's largest cadence gap (8.7 -> 4.0 reb/yr).")
    P("This run holds the corpus and the book FIXED and changes only the GRID: the 7 original")
    P("points plus 7W, 8W, 2M, 10W (the four the idea names) and 16W, 2Q (BEYOND Q, so the new")
    P("argmax can be interior).  13 points x 115 books = 1495 runs.")
    P(f"Costs {COST_BPS} bps, t+1 execution, IS <= {IS_END}, OOS >= {OOS_START}.")
    P("Two tuned params: SELECTOR (2, both reported) x LADDER POINT (13, all reported).")
    P("")

    books, panels = build_corpus()
    P(f"CORPUS: {len(books)} books  (3 fixed panels + {len(books)-3} sub-panels), same seeds as idea 175")
    for b in books[:3]:
        P(f"   {b.name:11s} {b.px.shape[0]}d x {b.px.shape[1]}c  tradable={len(b.tradable):3d}  "
          f"{b.px.index[0].date()}..{b.px.index[-1].date()}")
    for fam in FAMILIES:
        sub = [b for b in books if b.name.startswith(fam + "k")]
        P(f"   {fam:5s} sub-panels: {len(sub)}  k in {DRAWS[fam][1]} x {N_DRAWS} draws, seed {DRAWS[fam][0]}+k")
    P("")

    P("REPRODUCTION CONTROLS [a] and [b] (asserted before any new number is read)")
    okA = check_a(books[1])
    okB = check_b(books[1])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    START, SPY, BASE = {}, {}, {}
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
        mb, mbo = metrics(BASE[k]), metrics(BASE[k].loc[OOS_START:])
        P(f"  benchmark {k:6s} SPY       CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:7.2%} "
          f"halves {h1:.3f}/{h2:.3f}  OOS {mo['CAGR']:6.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:7.2%}")
        P(f"  {'':10s} {k:6s} RULES v1  CAGR {mb['CAGR']:6.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:7.2%} "
          f"  OOS {mbo['CAGR']:6.2%}/{mbo['Sharpe']:.3f}/{mbo['MaxDD']:7.2%}")
    P("")

    P("RUNNING THE 13-POINT LADDER ...")
    rows = []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        idx = bk.px.loc[st:].index
        spy = SPY[bk.parent].reindex(idx).fillna(0.0)
        base = BASE[bk.parent].reindex(idx).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        w = bk.weights()
        for pt in LADDER:
            res = fast_backtest(bk.px, w, COST_BPS, pt)
            r = res["returns"].loc[st:]
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
            mg_is, wb_is = rel_margin(r_is, spy_is)
            mg_oos, wb_oos = rel_margin(r_oos, spy_oos)
            h1, h2 = halves(r)
            rows.append(dict(
                book=bk.name, family=family_of(bk.name), parent=bk.parent, point=pt,
                is_new=(pt in NEW_POINTS), is_incumbent=(pt == CONST_PT),
                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                IS_margin=mg_is, IS_worstbar=wb_is,
                OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos)))
        if (bi + 1) % 25 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    lad = pd.DataFrame(rows)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    P(f"   {len(lad)} ladder rows -> {STEM}.ladder.csv   ({time.time()-t0:.0f}s)")
    P("")

    P("REPRODUCTION CONTROL [c] - the decisive one")
    okC = check_c(lad)
    if not okC:
        P("\n*** SHARED-POINT REPRODUCTION FAILED - the new points are not comparable to idea 175's.")
        P("*** Stopping before any conclusion is drawn. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    # ---- ladder shape: THE headline table
    P("=" * 118)
    P("LADDER SHAPE - mean over books of each cadence point (ALL 13 points, nothing picked)")
    P("  '*' marks a point idea 175 did not run.")
    P("")
    star = "".join("")
    hdr = " ".join(f"{p + ('*' if p in NEW_POINTS else ''):>8s}" for p in LADDER)
    shape_rows = []
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        nb = sub.book.nunique()
        g = sub.groupby("point")[["IS_Sharpe", "OOS_Sharpe", "OOS_margin", "OOS_CAGR", "OOS_MaxDD",
                                  "turnover"]].mean().reindex(LADDER)
        P(f"  {'family':7s} {'n':>4s} {'metric':11s} " + hdr)
        for met, fmt in [("IS_Sharpe", "{:8.3f}"), ("OOS_Sharpe", "{:8.3f}"), ("OOS_margin", "{:+8.3f}"),
                         ("OOS_CAGR", "{:8.2%}"), ("OOS_MaxDD", "{:8.2%}"), ("turnover", "{:8.1f}")]:
            P(f"  {fam:7s} {nb:4d} {met:11s} " + " ".join(fmt.format(g.loc[p, met]) for p in LADDER))
        s = g["OOS_Sharpe"]
        rkW = int(s.rank(ascending=False).loc[CONST_PT])
        rk6 = int(s.rank(ascending=False).loc[TEST_PT])
        amax = s.idxmax()
        P(f"  {fam:7s}      -> OOS Sharpe spread {s.max()-s.min():.3f};  argmax {amax}"
          f"{' (NEW POINT)' if amax in NEW_POINTS else ''};  6W ranks {rk6}/13;  W ranks {rkW}/13;"
          f"  IS argmax {g['IS_Sharpe'].idxmax()}")
        P(f"  {fam:7s}      -> argmax interior on the EXTENDED ladder? "
          f"{amax not in (LADDER[0], LADDER[-1])}   (idea 175's argmax was "
          f"{'6W' if fam != 'SMALL' else 'M'}, one step from its edge)")
        P("")
        for p in LADDER:
            shape_rows.append(dict(family=fam, n_books=nb, point=p, is_new=p in NEW_POINTS,
                                   **{k: g.loc[p, k] for k in g.columns}))
    pd.DataFrame(shape_rows).to_csv(OUT / f"{STEM}.shape.csv", index=False)

    # ---- arms
    rng_rand = np.random.default_rng(187_900)
    choices = []
    for bk in books:
        sub = lad[lad.book == bk.name].set_index("point").reindex(LADDER)
        pick = {
            "CONST-W": CONST_PT,
            "CONST-6W": TEST_PT,
            "SEL-SHARPE": sub["IS_Sharpe"].idxmax(),
            "SEL-4B": sub["IS_margin"].idxmax(),
            "RANDOM": LADDER[int(rng_rand.integers(len(LADDER)))],
            "ORACLE": sub["OOS_Sharpe"].idxmax(),
        }
        for arm, pt in pick.items():
            r = sub.loc[pt]
            choices.append(dict(book=bk.name, family=family_of(bk.name), parent=bk.parent,
                                arm=arm, point=pt, IS_Sharpe=r.IS_Sharpe, IS_margin=r.IS_margin,
                                OOS_Sharpe=r.OOS_Sharpe, OOS_margin=r.OOS_margin,
                                OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                                fail4a=r.fail4a, fail4b=r.fail4b))
    ch = pd.DataFrame(choices)
    ch.to_csv(OUT / f"{STEM}.choices.csv", index=False)

    # ---- Q1: does the argmax move off 6W?
    P("=" * 118)
    P("Q1 (THE IDEA'S QUESTION) - DOES THE ARGMAX MOVE ONCE THE LADDER IS EXTENDED PAST 6W?")
    P("")
    P("  per-book OOS argmax (ORACLE) distribution, and the IS pick (SEL-SHARPE) distribution")
    P(f"  {'family':7s} {'n':>4s} arm         " + " ".join(f"{p:>5s}" for p in LADDER))
    zone_rows = []
    for fam in ["ALL"] + FAMILIES:
        s = ch[(ch.arm == "SEL-SHARPE")] if fam == "ALL" else ch[(ch.arm == "SEL-SHARPE") & (ch.family == fam)]
        o = ch[(ch.arm == "ORACLE")] if fam == "ALL" else ch[(ch.arm == "ORACLE") & (ch.family == fam)]
        vs = s["point"].value_counts().reindex(LADDER).fillna(0).astype(int)
        vo = o["point"].value_counts().reindex(LADDER).fillna(0).astype(int)
        P(f"  {fam:7s} {len(o):4d} OOS argmax  " + " ".join(f"{vo[p]:5d}" for p in LADDER))
        P(f"  {fam:7s} {len(s):4d} IS pick     " + " ".join(f"{vs[p]:5d}" for p in LADDER))
        zo = float(o["point"].isin(ZONE).mean())
        z_new = float(o["point"].isin([p for p in ZONE if p in NEW_POINTS]).mean())
        slower = float(o["point"].isin(["Q", "16W", "2Q"]).mean())
        P(f"  {'':7s}      modal OOS argmax = {vo.idxmax()} ({vo.max()}/{len(o)} = {vo.max()/len(o):.1%})"
          f"{'  [NEW POINT]' if vo.idxmax() in NEW_POINTS else ''};"
          f"  6W alone = {vo['6W']/len(o):.1%} (idea 175: 60.9% ALL);"
          f"  ZONE {'/'.join(ZONE)} = {zo:.1%};  of which new points = {z_new:.1%};"
          f"  slower than 10W = {slower:.1%}")
        P(f"  {'':7s}      modal IS pick    = {vs.idxmax()} ({vs.max()/len(s):.1%});  "
          f"M is the IS pick in {vs['M']/len(s):.1%};  IS pick in ZONE = {float(s['point'].isin(ZONE).mean()):.1%}")
        P("")
        zone_rows.append(dict(family=fam, n=len(o), modal_oos_argmax=vo.idxmax(),
                              modal_share=vo.max() / len(o), share_6W=vo["6W"] / len(o),
                              zone_share=zo, zone_new_share=z_new, share_slower_than_10W=slower,
                              modal_is_pick=vs.idxmax(), is_pick_M_share=vs["M"] / len(s),
                              is_pick_zone_share=float(s["point"].isin(ZONE).mean())))
    pd.DataFrame(zone_rows).to_csv(OUT / f"{STEM}.zone.csv", index=False)

    # ---- Q2: EVERY point as a pre-registered constant, paired against W AND against 6W
    P("=" * 118)
    P("Q2 - EVERY CADENCE AS A PRE-REGISTERED CONSTANT (no fitting).  Paired, book by book.")
    P("     Anchor 1 = W (RULES v1's cadence, idea 175's base).  Anchor 2 = 6W (the point on trial).")
    P("     If ANY point slower than 6W beats it significantly, 'slower is better' was still")
    P("     running when idea 175's ladder stopped and 6W is a truncation artefact.")
    P("")
    const_rows = []
    for anchor in [CONST_PT, TEST_PT]:
        P(f"  --- anchor = {anchor}  (mean OOS_Sharpe difference, t in brackets) " + "-" * 40)
        P(f"  {'family':7s} {'n':>4s} " + " ".join(f"{p + ('*' if p in NEW_POINTS else ''):>16s}" for p in LADDER))
        for fam in ["ALL"] + FAMILIES:
            sub = lad if fam == "ALL" else lad[lad.family == fam]
            piv = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")
            cells = []
            for p in LADDER:
                d = (piv[p] - piv[anchor]).dropna()
                pv, w, l = sign_p(d.values)
                cells.append("-- base --" if p == anchor else f"{d.mean():+7.4f}(t{tstat(d.values):+5.2f})")
                const_rows.append(dict(anchor=anchor, family=fam, point=p, n=len(d), mean_d=d.mean(),
                                       t=tstat(d.values), wins=w, losses=l, sign_p=pv))
            P(f"  {fam:7s} {piv.shape[0]:4d} " + " ".join(f"{c:>16s}" for c in cells))
        P("")
    cdf = pd.DataFrame(const_rows)
    cdf.to_csv(OUT / f"{STEM}.constants.csv", index=False)

    P("  VERDICT ON THE IDEA'S OWN TEST - points SLOWER than 6W, anchored on 6W:")
    slower_pts = LADDER[LADDER.index(TEST_PT) + 1:]
    for fam in ["ALL"] + FAMILIES:
        g = cdf[(cdf.anchor == TEST_PT) & (cdf.family == fam) & (cdf.point.isin(slower_pts))]
        wins = g[(g.mean_d > 0) & (g.sign_p < 0.05)]
        best = g.loc[g.mean_d.idxmax()]
        P(f"   {fam:7s} slower-than-6W points beating 6W at sign p<0.05: {len(wins)}/{len(g)}"
          f"   best slower point = {best.point} ({best.mean_d:+.4f}, t {best.t:+.2f}, p {best.sign_p:.4f})")
    P("")

    # ---- Q3: the plateau test (idea 128)
    P("=" * 118)
    P("Q3 - PLATEAU TEST (idea 128): is any single slow point writable, or are they one plateau?")
    P(f"     ZONE = {ZONE}.  Compared against idea 175's published 6W-minus-M gap.")
    P("")
    P(f"  {'family':7s} {'zone spread':>12s} {'zone best':>10s} {'zone worst':>11s} {'6W-M gap':>10s} "
      f"{'spread/gap':>11s}  pairwise |t| inside zone (max)")
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        piv = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")
        g = piv[ZONE].mean()
        spread = g.max() - g.min()
        gap6M = float((piv["6W"] - piv["M"]).mean())
        tmax, tpair = 0.0, ""
        for i in range(len(ZONE)):
            for j in range(i + 1, len(ZONE)):
                d = (piv[ZONE[i]] - piv[ZONE[j]]).dropna()
                tv = abs(tstat(d.values))
                if tv > tmax:
                    tmax, tpair = tv, f"{ZONE[i]}-{ZONE[j]}"
        P(f"  {fam:7s} {spread:12.4f} {g.idxmax():>10s} {g.idxmin():>11s} {gap6M:+10.4f} "
          f"{spread/abs(gap6M) if gap6M else np.nan:11.2f}  {tmax:.2f} ({tpair})")
    P("")

    # ---- the paired selector test (idea 175's protocol, on the wider ladder)
    P("=" * 118)
    P(f"Q4 - THE PAIRED SELECTOR TEST - each arm MINUS the incumbent constant '{CONST_PT}'")
    P("     (idea 175's protocol, unchanged, on the 13-point ladder).  Idea 175's ALL row on")
    P("     its 7-point ladder: SEL-SHARPE +0.0388 (t +3.26), RANDOM and ORACLE for reference.")
    P("")
    paired = []
    for scorenm in ["OOS_Sharpe", "OOS_margin"]:
        P(f"  --- OOS score = {scorenm} " + "-" * 84)
        P(f"  {'family':7s} {'arm':11s} {'n':>4s} {'mean d':>9s} {'median d':>9s} {'t':>7s} {'win':>4s} "
          f"{'loss':>5s} {'tie':>4s} {'sign p':>8s} {'changes':>8s}  verdict")
        for fam in ["ALL"] + FAMILIES:
            sel = ch if fam == "ALL" else ch[ch.family == fam]
            base_s = sel[sel.arm == "CONST-W"].set_index("book")[scorenm]
            for arm in ARMS:
                if arm == "CONST-W":
                    continue
                a = sel[sel.arm == arm].set_index("book")
                d = (a[scorenm] - base_s).reindex(base_s.index)
                p, w, l = sign_p(d.values)
                nchg = int((a["point"] != CONST_PT).sum())
                md = d.mean()
                verd = ("FITTING WINS" if (md > 0 and p < 0.05) else
                        "fitting ahead (n.s.)" if md > 0 else
                        "FITTING LOSES" if p < 0.05 else "fitting behind (n.s.)")
                if arm == "ORACLE":
                    verd = "(upper bound)"
                if arm == "RANDOM":
                    verd = "(control) " + verd
                if arm == "CONST-6W":
                    verd = "(constant) " + verd
                P(f"  {fam:7s} {arm:11s} {len(d):4d} {md:+9.4f} {d.median():+9.4f} {tstat(d.values):+7.2f} "
                  f"{w:4d} {l:5d} {len(d)-w-l:4d} {p:8.5f} {nchg:4d}/{len(d):<3d}  {verd}")
                paired.append(dict(score=scorenm, family=fam, arm=arm, n=len(d), mean_d=md,
                                   median_d=d.median(), t=tstat(d.values), wins=w, losses=l,
                                   ties=len(d) - w - l, sign_p=p, n_changed=nchg, verdict=verd))
            P("")
    pdf = pd.DataFrame(paired)
    pdf.to_csv(OUT / f"{STEM}.paired.csv", index=False)

    P("CAPTURE OF THE ORACLE  (mean d of the arm / mean d of ORACLE, on OOS_Sharpe)")
    P("  A WIDER ladder raises the oracle (more points to be right about) and should LOWER capture.")
    P(f"  {'family':7s} {'n':>4s} {'ORACLE d':>10s} {'SEL-SHARPE d':>13s} {'t':>7s} {'capture':>9s} "
      f"{'SEL-4B d':>10s} {'capture':>9s} {'RANDOM d':>10s} {'capture':>9s} {'CONST-6W d':>11s} {'capture':>9s}")
    for fam in ["ALL"] + FAMILIES:
        g = pdf[(pdf.score == "OOS_Sharpe") & (pdf.family == fam)].set_index("arm")
        orc = g.loc["ORACLE", "mean_d"]
        line = f"  {fam:7s} {int(g.loc['ORACLE','n']):4d} {orc:+10.4f}"
        for arm in ["SEL-SHARPE", "SEL-4B", "RANDOM", "CONST-6W"]:
            dv = g.loc[arm, "mean_d"]
            cap = dv / orc if orc != 0 else np.nan
            if arm == "SEL-SHARPE":
                line += f" {dv:+13.4f} {g.loc[arm,'t']:+7.2f} {cap:9.1%}"
            elif arm == "CONST-6W":
                line += f" {dv:+11.4f} {cap:9.1%}"
            else:
                line += f" {dv:+10.4f} {cap:9.1%}"
        P(line)
    P("")

    # ---- ladder geometry (idea 183)
    P("LADDER GEOMETRY (idea 183's anchor-position column) on the EXTENDED grid")
    P(f"  {'family':7s} {'rho(rank(cadence), rank(mean OOS Sh))':>38s} {'ORACLE interior':>16s} "
      f"{'SEL==ORACLE':>12s} {'W rank':>8s} {'6W rank':>8s}")
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        g = sub.groupby("point")["OOS_Sharpe"].mean().reindex(LADDER)
        rho = float(np.corrcoef(np.arange(len(LADDER), dtype=float), pd.Series(g.values).rank().values)[0, 1])
        o = (ch if fam == "ALL" else ch[ch.family == fam])
        op = o[o.arm == "ORACLE"].set_index("book")["point"]
        sp = o[o.arm == "SEL-SHARPE"].set_index("book")["point"]
        ends = {LADDER[0], LADDER[-1]}
        P(f"  {fam:7s} {rho:38.3f} {float((~op.isin(ends)).mean()):16.1%} "
          f"{float((op == sp).mean()):12.1%} {int(g.rank(ascending=False).loc[CONST_PT]):5d}/13 "
          f"{int(g.rank(ascending=False).loc[TEST_PT]):5d}/13")
    P("  (idea 175 read rho on 7 points; a rho near +1 means 'slower is monotonically better' and")
    P("   the ladder is still truncated.  A rho well below +1 with an interior argmax is a hump.)")
    P("")

    # ---- rule 8 walk-forward
    P("=" * 118)
    P("PROTOCOL RULE 8 WALK-FORWARD - parameters chosen on <= 2016-12-31, OOS window read once")
    P("")
    wf = []
    P(f"  {'family':7s} {'arm':11s} {'mean OOS CAGR':>14s} {'mean OOS Sharpe':>16s} {'mean OOS MaxDD':>15s} "
      f"| {'S1 pick (best IS Sharpe book)':32s} {'OOS CAGR':>9s} {'Sharpe':>8s} {'MaxDD':>8s}")
    for fam in ["ALL"] + FAMILIES:
        sel = ch if fam == "ALL" else ch[ch.family == fam]
        for arm in ARMS:
            a = sel[sel.arm == arm]
            i = a["IS_Sharpe"].idxmax()
            pick = a.loc[i]
            P(f"  {fam:7s} {arm:11s} {a.OOS_CAGR.mean():14.2%} {a.OOS_Sharpe.mean():16.3f} "
              f"{a.OOS_MaxDD.mean():15.2%} | {pick.book+' @ '+str(pick.point):32s} "
              f"{pick.OOS_CAGR:9.2%} {pick.OOS_Sharpe:8.3f} {pick.OOS_MaxDD:8.2%}")
            wf.append(dict(family=fam, arm=arm, mean_OOS_CAGR=a.OOS_CAGR.mean(),
                           mean_OOS_Sharpe=a.OOS_Sharpe.mean(), mean_OOS_MaxDD=a.OOS_MaxDD.mean(),
                           s1_book=pick.book, s1_point=pick.point, s1_OOS_CAGR=pick.OOS_CAGR,
                           s1_OOS_Sharpe=pick.OOS_Sharpe, s1_OOS_MaxDD=pick.OOS_MaxDD,
                           s1_fail4a=pick.fail4a, s1_fail4b=pick.fail4b))
        P("")
    for par in ["U56", "SMALL"]:
        b, s = BASE[par], SPY[par]
        mb, ms = metrics(b.loc[OOS_START:]), metrics(s.loc[OOS_START:])
        P(f"  reference {par:6s} OOS  RULES v1 {mb['CAGR']:7.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:7.2%}   "
          f"SPY {ms['CAGR']:7.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:7.2%}")
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("")

    # ---- both KEEP paths
    P("=" * 118)
    P(f"BOTH KEEP PATHS, evaluated on all {len(lad)} ladder rows (PROTOCOL rule 4a and 4b, exactly)")
    P("")
    lad["pass4a"] = lad.fail4a == "-"
    lad["pass4b"] = lad.fail4b == "-"
    lad.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'family':7s} {'rows':>5s} {'4a':>4s} {'4b':>4s}   4b passes by cadence point")
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        by = sub.groupby("point")["pass4b"].sum().reindex(LADDER).fillna(0).astype(int)
        P(f"  {fam:7s} {len(sub):5d} {int(sub.pass4a.sum()):4d} {int(sub.pass4b.sum()):4d}   "
          + " ".join(f"{p}:{by[p]}" for p in LADDER))
    P("")
    newrows = lad[lad.is_new]
    P(f"  of the {int(lad.pass4b.sum())} 4b passes, {int(newrows.pass4b.sum())} are on the SIX NEW points "
      f"({', '.join(NEW_POINTS)}); of the {int(lad.pass4a.sum())} 4a passes, {int(newrows.pass4a.sum())} are.")
    P("  most-violated 4b bar, counted over failing rows:")
    bars = {}
    for f in lad.loc[~lad.pass4b, "fail4b"]:
        for b in f.split(","):
            bars[b] = bars.get(b, 0) + 1
    P("   " + "  ".join(f"{k}:{v}" for k, v in sorted(bars.items(), key=lambda kv: -kv[1])))
    P("")
    fx = lad[lad.pass4b & lad.book.isin(["SMALL439", "U56", "ETF36"])]
    if len(fx):
        P("  4b passes on the three FIXED panels (sub-panel passes are in .keep.csv):")
        for _, r in fx.sort_values("OOS_Sharpe", ascending=False).iterrows():
            P(f"   {r.book:9s} @ {r.point:3s}{'*' if r.is_new else ' '} CAGR {r.CAGR:6.2%} "
              f"Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:7.2%} halves {r.H1:.3f}/{r.H2:.3f}  "
              f"OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%} turnover {r.turnover:.1f}x/yr")
    else:
        P("  4b passes on the three FIXED panels: NONE.")
    P("")

    # ---- POST-HOC (labelled): the phase control
    P("=" * 118)
    P("POST-HOC CONTROL (added AFTER the ladder table above was read, and labelled as such).")
    P("")
    P("WHY.  The ladder came back JAGGED, not humped: pooled OOS Sharpe runs 6W 0.780 -> 7W 0.606")
    P("-> 8W 0.651 -> 2M 0.826 -> 10W 0.693, i.e. neighbouring points 1.2 rebalances/yr apart")
    P("differ by 0.17 of Sharpe, and Q (4.0/yr) is the WORST point on the whole ladder while 2Q")
    P("(2.0/yr, half Q's frequency) beats it.  No signal-decay mechanism can do that.  The obvious")
    P("alternative is that what moves is not cadence LENGTH but block PHASE - WHICH weeks a point")
    P("lands on.  Every ladder point above is phase 0 (anchored on the panel's first bar), so the")
    P("ladder has been confounding the two all along.  This control separates them by holding the")
    P("cadence FIXED and sweeping the phase, on the same 115 books, nothing picked.")
    P("")
    ph_specs = [("6W", 6), ("2M", 2), ("8W", 8), ("Q", 4)]
    ph_rows = []
    for cad, nph in ph_specs:
        for bk in books:
            st = START[bk.parent]
            w = bk.weights()
            for ph in range(nph):
                r = fast_backtest(bk.px, w, COST_BPS, cad, ph)["returns"].loc[st:]
                mo = metrics(r.loc[OOS_START:])
                ph_rows.append(dict(book=bk.name, family=family_of(bk.name), cad=cad, phase=ph,
                                    OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                                    IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"]))
        P(f"   ... phase sweep {cad} done ({time.time()-t0:.0f}s)")
    phd = pd.DataFrame(ph_rows)
    phd.to_csv(OUT / f"{STEM}.phase.csv", index=False)
    P("")
    P("  mean OOS Sharpe by PHASE, cadence held fixed (phase 0 is the ladder point reported above)")
    for cad, nph in ph_specs:
        P(f"  {'family':7s} cad={cad:3s} " + " ".join(f"{'ph'+str(i):>8s}" for i in range(nph))
          + f" {'spread':>9s} {'best-worst t':>13s}")
        for fam in ["ALL"] + FAMILIES:
            sub = phd[(phd.cad == cad)] if fam == "ALL" else phd[(phd.cad == cad) & (phd.family == fam)]
            piv = sub.pivot_table(index="book", columns="phase", values="OOS_Sharpe")
            g = piv.mean()
            bi, wi = int(g.idxmax()), int(g.idxmin())
            d = (piv[bi] - piv[wi]).dropna()
            P(f"  {fam:7s} {'':7s} " + " ".join(f"{g[i]:8.3f}" for i in range(nph))
              + f" {g.max()-g.min():9.4f} {tstat(d.values):13.2f}")
        P("")
    P("  Q IS A DEGENERATE CONTROL, NOT A BUG: Q is a k=1 calendar-period point, so it has exactly")
    P("  ONE phase by construction (a calendar quarter is a calendar quarter) and its spread MUST")
    P("  be 0.0000.  That it is exactly 0.0000 is the negative control for this sweep: the machinery")
    P("  returns zero phase effect where zero phase freedom exists, so the non-zero spreads at")
    P("  6W / 2M / 8W are phase and not sweep noise.")
    P("")
    P("  THE COMPARISON THAT MATTERS - phase spread vs the cadence effects this project publishes:")
    P(f"  {'family':7s} {'phase spread 6W':>16s} {'phase spread 2M':>16s} {'ZONE cadence spread':>20s} "
      f"{'6W-minus-W (idea175)':>21s} {'phase/cadence':>14s}")
    phase_tab = []
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        piv = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")
        zsp = float(piv[ZONE].mean().max() - piv[ZONE].mean().min())
        d6w = float((piv["6W"] - piv["W"]).mean())
        sp = {}
        for cad, nph in ph_specs:
            s2 = phd[(phd.cad == cad)] if fam == "ALL" else phd[(phd.cad == cad) & (phd.family == fam)]
            g = s2.pivot_table(index="book", columns="phase", values="OOS_Sharpe").mean()
            sp[cad] = float(g.max() - g.min())
        P(f"  {fam:7s} {sp['6W']:16.4f} {sp['2M']:16.4f} {zsp:20.4f} {d6w:+21.4f} "
          f"{max(sp['6W'], sp['2M'])/abs(d6w) if d6w else np.nan:14.2f}")
        phase_tab.append(dict(family=fam, phase_spread_6W=sp["6W"], phase_spread_2M=sp["2M"],
                              phase_spread_8W=sp["8W"], phase_spread_Q=sp["Q"],
                              zone_cadence_spread=zsp, gap_6W_minus_W=d6w))
    pd.DataFrame(phase_tab).to_csv(OUT / f"{STEM}.phasesummary.csv", index=False)
    P("")
    P("  Reading: if the PHASE spread at a fixed cadence is of the same order as the spread ACROSS")
    P("  cadences, then 'which weeks the book rebalances on' explains as much as 'how often', and")
    P("  no cadence constant is identified by this data.  A phase is not a tradable choice: it is")
    P("  fixed by an arbitrary sample-start date, so a point that wins on phase wins on nothing.")
    P("")
    P("  DIRECT CONSEQUENCE for idea 175's headline, stated as a checkable count:")
    for cad in ["6W", "2M"]:
        for fam in ["ALL", "U56", "ETF", "SMALL"]:
            sub = lad if fam == "ALL" else lad[lad.family == fam]
            wmean = float(sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")[CONST_PT].mean())
            s2 = phd[(phd.cad == cad)] if fam == "ALL" else phd[(phd.cad == cad) & (phd.family == fam)]
            g = s2.pivot_table(index="book", columns="phase", values="OOS_Sharpe").mean()
            nb = int((g > wmean).sum())
            P(f"   {cad:3s} on {fam:6s}: beats the incumbent W (mean OOS Sharpe {wmean:.3f}) at "
              f"{nb}/{len(g)} of its own phases;  ladder phase 0 ranks "
              f"{int(g.rank(ascending=False).loc[0])}/{len(g)}")
    P("")

    # ---- predictions scorecard
    P("=" * 118)
    P("PRE-REGISTERED PREDICTIONS - scored")
    gall = lad.groupby("point")["OOS_Sharpe"].mean().reindex(LADDER)
    amax = gall.idxmax()
    interior = amax not in (LADDER[0], LADDER[-1])
    moved = amax != TEST_PT
    zdf = pd.DataFrame(zone_rows).set_index("family")
    zone_all = zdf.loc["ALL", "zone_share"]
    modal_all = zdf.loc["ALL", "modal_share"]
    pivall = lad.pivot_table(index="book", columns="point", values="OOS_Sharpe")
    zspread = float(pivall[ZONE].mean().max() - pivall[ZONE].mean().min())
    gap6M = float((pivall["6W"] - pivall["M"]).mean())
    small_arg = lad[lad.family == "SMALL"].groupby("point")["OOS_Sharpe"].mean().reindex(LADDER).idxmax()
    u56_arg = lad[lad.family == "U56"].groupby("point")["OOS_Sharpe"].mean().reindex(LADDER).idxmax()
    etf_arg = lad[lad.family == "ETF"].groupby("point")["OOS_Sharpe"].mean().reindex(LADDER).idxmax()
    is_modal = zdf.loc["ALL", "modal_is_pick"]
    slower_beat = int(((cdf.anchor == TEST_PT) & (cdf.family == "ALL") &
                       (cdf.point.isin(slower_pts)) & (cdf.mean_d > 0) & (cdf.sign_p < 0.05)).sum())
    P(f"  P1 reproduction [a][b][c]                                              -> "
      f"{'HIT' if (okA and okB and okC) else 'MISS'}")
    P(f"  P2 pooled OOS argmax MOVES off 6W    argmax={amax}                      -> {'HIT' if moved else 'MISS'}")
    P(f"  P3 argmax INTERIOR on the extended ladder (not 2Q); truncation refuted  -> "
      f"{'HIT' if interior else 'MISS'}   [slower-than-6W points beating 6W, ALL: {slower_beat}/{len(slower_pts)}]")
    P(f"  P4 ZONE share > idea 175's 60.9% while 6W-alone share falls   zone={zone_all:.1%} "
      f"modal={modal_all:.1%}  -> {'HIT' if zone_all > 0.609 else 'MISS'}")
    P(f"  P5 zone spread {zspread:.4f} < |6W-M gap| {abs(gap6M):.4f} (one plateau)      -> "
      f"{'HIT' if zspread < abs(gap6M) else 'MISS'}")
    P(f"  P6 family split survives: SMALL argmax={small_arg}, U56={u56_arg}, ETF={etf_arg}  -> "
      f"{'HIT' if (small_arg in ('W','2W','M')) and (u56_arg in ZONE) and (etf_arg in ZONE) else 'MISS'}")
    P(f"  P7 SEL-SHARPE modal IS pick still M   modal={is_modal}                  -> "
      f"{'HIT' if is_modal == 'M' else 'MISS'}")
    P(f"  P8 no NEW 4b KEEP on the fixed panels beyond a re-cadencing (idea 144)  -> see the KEEP table")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
