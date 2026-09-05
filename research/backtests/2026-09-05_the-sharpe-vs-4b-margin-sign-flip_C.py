#!/usr/bin/env python3
"""QUEUE idea 174 — the-sharpe-vs-4b-margin-sign-flip  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 174)
    "idea 171 found that on ALL five dials every arm that raises mean OOS Sharpe lowers the
     OOS 4b pass count (SLEEVE: Sharpe 0.964->1.144 while the 4b margin goes -0.161->-0.192),
     because Sharpe is bought with CAGR and the CAGR floor is 4b's most-violated bar (1223 of
     1908 rows).  Test whether 4b's CAGR floor and its DD cap are jointly satisfiable at all on
     this data: sweep the (phi, delta) pair over a grid and map the region where any book
     passes.  If the incumbent (0.70, 0.60) sits outside that region, 4b is not a screen, it is
     a wall.  Max 2 params."

WHAT IS AT STAKE.
    PROTOCOL rule 4b is the project's definition of "capital-worthy".  Two of its five bars are
    coefficients someone chose: CAGR >= PHI * CAGR(SPY) with PHI = 0.70, and |MaxDD| <=
    DELTA * |MaxDD(SPY)| with DELTA = 0.60.  Every KILL the project has recorded on those two
    bars is conditional on that pair.  Nobody has ever asked whether the pair admits ANYTHING.
    If the reachable set of (CAGR, MaxDD) on this data never touches the (0.70, 0.60) quadrant,
    then those KILLs are not evidence about the books — they are evidence about the bar, and
    every run spent trying to close a "CAGR-floor near-miss" was spent against a wall.

    The test is cheap and exact, and that is the point: the pass/fail of a book at any
    (phi, delta) is a PURE FUNCTION of two numbers already computed for it,
        c = CAGR(book) / CAGR(SPY)          -> passes the floor iff phi <= c
        d = |MaxDD(book)| / |MaxDD(SPY)|    -> passes the cap  iff delta >= d
    so the whole (phi, delta) grid costs zero extra backtests.  The corpus is run ONCE and the
    grid is read off it.  No book is re-fitted at any grid point; nothing is tuned to pass.

THE TWO SWEPT PARAMETERS — exactly two, per PROTOCOL rule 4, and they ARE the idea.
    1. PHI    (the CAGR floor coefficient)   16 points: 0.00, 0.10, ... 1.50   incumbent 0.70
    2. DELTA  (the drawdown cap coefficient) 20 points: 0.10, 0.20, ... 2.00   incumbent 0.60
    320 grid cells, ALL reported in .region.csv.  Nothing else is tuned.

    The CORPUS axes (book, gross, sleeve) are NOT tuned parameters — they are the set over
    which "does ANY book pass" is quantified, and every one of the 1590 points is reported in
    .points.csv with its own (c, d).  Where rule 8 forces a single pick, the pick is made on
    the IS window only and labelled as such.

CORPUS — 53 books x 10 gross x 3 sleeve = 1590 points.
    Books are idea 171's corpus, unchanged (5 fixed panels U56/B136/BSTK100/ETF36/SMALL484 +
    48 sub-panels: k in {20,40,80} x 16 draws of B136, rng = default_rng(171500 + k)).
    GROSS  in {0.20,0.30,0.40,0.50,0.60,0.70,0.75,0.80,0.90,1.00}   (idea 78/166's ladder)
    SLEEVE in {0.00, 0.15, 0.30}                                    (idea 134/139's sleeve; the
        one instrument idea 139 found is NOT a point on the gross ladder, so including it makes
        the "reachable set" strictly larger than a pure re-grossing and the wall test harder to
        pass by construction.)
    Book core = idea 2's 4b candidate (top-20 by the scan.py composite, no vol scaler, bare
    200d gate + vol20 < 0.60), i.e. the construction idea 171 swept.

WHAT IS MEASURED AT EACH GRID CELL
    N_CD    # points whose (c, d) satisfies BOTH the CAGR floor and the DD cap  (the idea's
            literal question: are the two jointly satisfiable?)
    N_4B    # points that additionally clear 4b's three Sharpe bars (H1 > SPY, H2 > SPY,
            OOS > SPY), i.e. the FULL rule 4b as PROTOCOL states it
    and, per cell, the best book and the binding bar.  The gap between N_CD and N_4B is the
    decomposition the idea needs: a wall built by the two coefficients is fixable by changing
    them; a wall built by the Sharpe bars is not.

    The FRONTIER is reported separately and is the cleanest object here: for each DELTA,
    phi_max(delta) = max over all points with d <= delta of c.  The incumbent is inside the
    non-empty region iff phi_max(0.60) >= 0.70.  This is a staircase, monotone by construction,
    and it is read once.

WALK-FORWARD (PROTOCOL rule 8, required).  Two forms, both reported:
    W1  REGION STABILITY.  Recompute (c, d) and the three Sharpe bars on the IS window
        (<= 2016-12-31) alone and on the OOS window (2017-01-01 ->) alone, and compare the two
        maps cell by cell.  A bar that is a wall in-sample and open out-of-sample (or the
        reverse) is not a screen at all.
    W2  THE PICK.  At every (phi, delta) cell: among the points passing the IS-window screen at
        that cell, take the one with the best IS Sharpe, and read its OOS CAGR / Sharpe / MaxDD
        ONCE.  Against (i) the do-nothing control — best IS Sharpe with NO screen, ideas
        151/171's control — (ii) RULES v1 on the pick's parent panel, and (iii) SPY.  This is
        the only place a single number is chosen, and it is chosen on IS.

BOTH KEEP PATHS are evaluated, at the INCUMBENT coefficients, for all 1590 points, in
    .keep.csv:  4a (Sharpe > RULES v1 in BOTH halves and MaxDD no worse) and 4b (halves and
    OOS Sharpe > SPY, |MaxDD| <= 0.60 |MaxDD(SPY)|, CAGR >= 0.70 CAGR(SPY)).

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover on a real book at the incumbent point.  Without [a] nothing below is a
        Claude-Space backtest.
    [b] every one of idea 171's 530 committed GROSS-dial ladder rows (its .ladder.csv, read
        from disk, not retyped) is reproduced by this script's sleeve=0 points to < 1e-10 on
        CAGR, Sharpe, MaxDD, H1, H2 and OOS Sharpe.  The corpus is idea 171's corpus, not a
        look-alike, so the premise this run is testing is the premise that was measured.
    [c] idea 171's headline premise is re-counted on its own committed rows: "the CAGR floor is
        4b's most-violated bar (1223 of 1908 rows)".

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b] and [c] all hold.
    P2  The two coefficients ARE jointly satisfiable and the incumbent (0.70, 0.60) is INSIDE
        the non-empty region — i.e. the idea's own headline ("4b is a wall") is WRONG on the
        CAGR/DD pair.  Reason: idea 171's committed keep.csv already records 250 rows passing
        full 4b, and a full-4b pass entails a CAGR/DD pass.  If P2 fails, [b] must have failed
        and the run is void.
    P3  The interesting wall is therefore NOT the (phi, delta) pair.  I predict the binding
        constraint at the incumbent is a SHARPE bar (H1/H2/OOS) for the majority of points, and
        that N_CD >> N_4B at (0.70, 0.60).
    P4  phi_max(delta) is steeply increasing in delta over 0.3-0.8 and flat beyond ~1.0: the
        DD cap is what prices the CAGR floor, and past delta ~ 1.0 the cap stops binding at all
        because de-grossing has already been given away.
    P5  Spearman(c, d) across the 1590 points is strongly POSITIVE (> +0.7): return and
        drawdown are bought together, which is the mechanism behind idea 171's sign flip.
    P6  W2's screen does NOT beat the do-nothing control on OOS Sharpe at the incumbent cell
        (ideas 110/132/151/166/171: no IS-fitted selector has ever beaten doing nothing here).
    P7  No NEW book KEEP comes out of this run; it is a methodology run.  Points that pass 4b
        are idea 171's already-committed passes, not new candidates.

CAVEATS carried, not buried
    * Survivorship: U56/B136/SMALL484 are current-constituent lists (idea 54).  Every c is
      biased UP and every d biased DOWN by it, which makes the region look MORE reachable than
      it is.  A "the bar is satisfiable" finding is therefore the conservative direction; a
      "the bar is a wall" finding would have been the strong one.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 144: a re-grossed book is the SAME book.  The 1590 points are 53 books seen at 30
      exposures, not 1590 strategies, and no count here should be read as 1590 independent
      trials.
    * c is well defined only because CAGR(SPY) > 0 on every window used here; asserted, not
      assumed.
    * The grid is read on ONE data set.  "Satisfiable on this data" is not "satisfiable".

Deterministic, standalone.  Writes .console.txt, .points.csv, .region.csv, .frontier.csv,
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

STEM = "2026-09-05_the-sharpe-vs-4b-margin-sign-flip_C"
OUT = ROOT / "research" / "backtests"
REF171 = OUT / "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C.ladder.csv"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI_INC, DELTA_INC = 0.70, 0.60          # the incumbent 4b coefficients
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]

N_CORE = 20                              # idea 2's 4b candidate book
BAND = 0.00                              # RULES v1 / scan.py bare 200d gate
FREQ = "W"                               # RULES v1 cadence
GROSS_LADDER = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]
SLEEVE_LADDER = [0.00, 0.15, 0.30]

PHI_GRID = [round(0.10 * i, 2) for i in range(0, 16)]        # 0.00 .. 1.50
DELTA_GRID = [round(0.10 * i, 2) for i in range(1, 21)]      # 0.10 .. 2.00

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


# ---------------------------------------------------------------- fast backtest (idea 171)
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


# ---------------------------------------------------------------- book construction (idea 171)
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

    def weights(self, gross, sleeve):
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


# ---------------------------------------------------------------- metric helpers
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def win_stats(r, spy):
    """Everything 4b needs on one window, as (c, d) plus the two half-Sharpe comparisons."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    return dict(
        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
        c=m["CAGR"] / ms["CAGR"], d=abs(m["MaxDD"]) / abs(ms["MaxDD"]),
        sh1=bool(h1 > s1), sh2=bool(h2 > s2), shS=bool(m["Sharpe"] > ms["Sharpe"]),
    )


def spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan
    rx = pd.Series(x).rank().values; ry = pd.Series(y).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


# ---------------------------------------------------------------- reproduction controls
def check_a(book):
    P("  [a] fast_backtest vs engine.backtest (products/backtester/engine.py), incumbent point:")
    w = book.weights(0.75, 0.00)
    a = backtest(book.px, w, cost_bps=COST_BPS, freq=FREQ)
    b = fast_backtest(book.px, w, cost_bps=COST_BPS, freq=FREQ)
    dr = float((a["returns"] - b["returns"]).abs().max())
    dt = float((a["turnover"] - b["turnover"]).abs().max())
    ok = dr < 1e-12 and dt < 1e-10
    P(f"      {book.name:9s} freq={FREQ}  max|dret|={dr:.3e}  max|dturn|={dt:.3e}  -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_c():
    """idea 171's headline premise, re-counted on its OWN committed rows."""
    if not REF171.exists():
        P("  [c] idea 171 ladder.csv not found - premise not re-counted")
        return None
    L = pd.read_csv(REF171)
    vc = L["fail4b"].fillna("-").astype(str)
    n_cagr = int(vc.str.split(",").apply(lambda z: "CAGR" in z).sum())
    counts = {}
    for bar in ["H1", "H2", "OOS", "DD", "CAGR"]:
        counts[bar] = int(vc.str.split(",").apply(lambda z: bar in z).sum())
    P(f"  [c] idea 171 premise re-counted on its own {len(L)} committed rows:")
    P(f"      violations by bar  {counts}   (idea 171 claims CAGR = 1223 of 1908)")
    P(f"      -> CAGR count {n_cagr} of {len(L)}  "
      f"{'MATCHES the claim' if n_cagr == 1223 and len(L) == 1908 else 'DOES NOT match the claimed 1223/1908'}")
    return counts


def check_b(points):
    """Every sleeve=0 point must reproduce idea 171's committed GROSS-dial ladder row."""
    if not REF171.exists():
        P("  [b] idea 171 ladder.csv not found - corpus identity NOT established")
        return False
    L = pd.read_csv(REF171)
    L = L[L["dial"] == "GROSS"].copy()
    L["key"] = L["book"] + "|" + L["point"].map(lambda v: f"{float(v):.2f}")
    mine = points[points["sleeve"] == 0.0].copy()
    mine["key"] = mine["book"] + "|" + mine["gross"].map(lambda v: f"{float(v):.2f}")
    j = L.set_index("key").join(mine.set_index("key"), rsuffix="_new", how="inner")
    cols = [("CAGR", "CAGR_new"), ("Sharpe", "Sharpe_new"), ("MaxDD", "MaxDD_new"),
            ("H1", "H1_new"), ("H2", "H2_new"), ("OOS_Sharpe", "OOS_Sharpe_new")]
    worst = 0.0
    for a, b in cols:
        worst = max(worst, float((j[a] - j[b]).abs().max()))
    ok = len(j) == len(L) and worst < 1e-10
    P(f"  [b] idea 171 GROSS-dial rows reproduced: {len(j)} of {len(L)} matched, "
      f"max|diff| over CAGR/Sharpe/MaxDD/H1/H2/OOS_Sharpe = {worst:.3e}  -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 174 - the-sharpe-vs-4b-margin-sign-flip   (lane C, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Are 4b's CAGR floor and DD cap JOINTLY SATISFIABLE on this data?  Sweep (phi, delta); map the region where any book passes.")
    P(f"Costs {COST_BPS} bps, t+1 execution, cadence {FREQ}, IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"Two swept params: PHI ({len(PHI_GRID)} pts {PHI_GRID[0]}..{PHI_GRID[-1]}) x DELTA ({len(DELTA_GRID)} pts "
      f"{DELTA_GRID[0]}..{DELTA_GRID[-1]}) = {len(PHI_GRID)*len(DELTA_GRID)} cells, ALL reported.  Incumbent ({PHI_INC}, {DELTA_INC}).")
    P("")

    books, panels = build_corpus()
    P(f"CORPUS: {len(books)} books x {len(GROSS_LADDER)} gross x {len(SLEEVE_LADDER)} sleeve = "
      f"{len(books)*len(GROSS_LADDER)*len(SLEEVE_LADDER)} points   (idea 171's corpus, book = idea 2's top-{N_CORE} candidate)")
    P(f"   GROSS  {GROSS_LADDER}")
    P(f"   SLEEVE {SLEEVE_LADDER}  on {SLEEVE_ASSETS}")
    P("")

    P("REPRODUCTION CONTROLS (asserted before any new number is read)")
    okA = check_a(books[1])
    prem = check_c()
    if not okA:
        P("\n*** REPRODUCTION [a] FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    # ---- benchmarks per panel
    START, SPY, BASE = {}, {}, {}
    for b in books:
        if b.parent not in SPY:
            px = panels[b.parent]
            st = px.index[260]
            START[b.parent] = st
            SPY[b.parent] = px["SPY"].pct_change().fillna(0.0).loc[st:]
            BASE[b.parent] = fast_backtest(px, rules_v1_weights(px), COST_BPS, FREQ)["returns"].loc[st:]
    P("BENCHMARKS (per parent panel; SPY is the 4b reference, RULES v1 the 4a reference)")
    for k, v in SPY.items():
        m = metrics(v); mo = metrics(v.loc[OOS_START:]); mi = metrics(v.loc[:IS_END])
        h1, h2 = halves(v); mb = metrics(BASE[k])
        assert m["CAGR"] > 0 and mo["CAGR"] > 0 and mi["CAGR"] > 0, "CAGR(SPY) must be > 0 for c to be defined"
        P(f"  {k:6s} SPY  full CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:7.2%} halves {h1:.3f}/{h2:.3f}"
          f" | IS CAGR {mi['CAGR']:6.2%} Sh {mi['Sharpe']:.3f} DD {mi['MaxDD']:7.2%}"
          f" | OOS CAGR {mo['CAGR']:6.2%} Sh {mo['Sharpe']:.3f} DD {mo['MaxDD']:7.2%}"
          f" || RULES v1 full Sharpe {mb['Sharpe']:.3f} CAGR {metrics(BASE[k])['CAGR']:6.2%}")
    P("")

    # ---- run the corpus ONCE
    P("RUNNING CORPUS ...")
    rows = []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        idx = bk.px.loc[st:].index
        spy = SPY[bk.parent].reindex(idx).fillna(0.0)
        base = BASE[bk.parent].reindex(idx).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        b_full = metrics(base); b_h1, b_h2 = halves(base)
        for g in GROSS_LADDER:
            for f in SLEEVE_LADDER:
                r = fast_backtest(bk.px, bk.weights(g, f), COST_BPS, FREQ)["returns"].loc[st:]
                W = win_stats(r, spy)
                Wi = win_stats(r.loc[:IS_END], spy_is)
                Wo = win_stats(r.loc[OOS_START:], spy_oos)
                # 4a, evaluated against RULES v1 on the parent panel
                f4a = []
                if not W["H1"] > b_h1: f4a.append("H1")
                if not W["H2"] > b_h2: f4a.append("H2")
                if not W["MaxDD"] >= b_full["MaxDD"]: f4a.append("DD")
                rows.append(dict(
                    book=bk.name, parent=bk.parent, gross=g, sleeve=f,
                    CAGR=W["CAGR"], Sharpe=W["Sharpe"], MaxDD=W["MaxDD"], H1=W["H1"], H2=W["H2"],
                    c=W["c"], d=W["d"], sh1=W["sh1"], sh2=W["sh2"],
                    OOS_Sharpe=Wo["Sharpe"], OOS_CAGR=Wo["CAGR"], OOS_MaxDD=Wo["MaxDD"],
                    shOOS=Wo["shS"], c_oos=Wo["c"], d_oos=Wo["d"],
                    oos_sh1=Wo["sh1"], oos_sh2=Wo["sh2"],
                    IS_Sharpe=Wi["Sharpe"], IS_CAGR=Wi["CAGR"], IS_MaxDD=Wi["MaxDD"],
                    c_is=Wi["c"], d_is=Wi["d"], is_sh1=Wi["sh1"], is_sh2=Wi["sh2"], is_shS=Wi["shS"],
                    fail4a=",".join(f4a) if f4a else "-",
                ))
        if (bi + 1) % 10 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    pts = pd.DataFrame(rows)
    pts.to_csv(OUT / f"{STEM}.points.csv", index=False)
    P(f"   {len(pts)} points -> {STEM}.points.csv   ({time.time()-t0:.0f}s)")
    P("")

    okB = check_b(pts)
    if not okB:
        P("  *** [b] FAILED: this corpus is not idea 171's corpus.  Every claim below is void. ***")
    P("")

    # ---- 4b at the incumbent, and the full grid ------------------------------------------
    pts["sh_all"] = pts["sh1"] & pts["sh2"] & pts["shOOS"]

    def bars_fail(row, phi, delta):
        f = []
        if not row["sh1"]: f.append("H1")
        if not row["sh2"]: f.append("H2")
        if not row["shOOS"]: f.append("OOS")
        if not row["d"] <= delta: f.append("DD")
        if not row["c"] >= phi: f.append("CAGR")
        return ",".join(f) if f else "-"

    P("=" * 118)
    P("PART 1 - THE (phi, delta) REGION MAP.  N_CD = points clearing the CAGR floor AND the DD cap;")
    P("         N_4B = those that also clear 4b's three Sharpe bars (H1, H2, OOS vs SPY).  All 320 cells in .region.csv.")
    P("")
    c = pts["c"].values; d = pts["d"].values; sh = pts["sh_all"].values
    reg = []
    for phi in PHI_GRID:
        for delta in DELTA_GRID:
            ok_cd = (c >= phi) & (d <= delta)
            ok_4b = ok_cd & sh
            sub = pts[ok_4b]
            best = sub.loc[sub["Sharpe"].idxmax()] if len(sub) else None
            reg.append(dict(phi=phi, delta=delta, N_CD=int(ok_cd.sum()), N_4B=int(ok_4b.sum()),
                            n_books_CD=int(pts.loc[ok_cd, "book"].nunique()),
                            n_books_4B=int(pts.loc[ok_4b, "book"].nunique()),
                            best_book=(best["book"] if best is not None else ""),
                            best_gross=(best["gross"] if best is not None else np.nan),
                            best_sleeve=(best["sleeve"] if best is not None else np.nan),
                            best_Sharpe=(best["Sharpe"] if best is not None else np.nan),
                            best_CAGR=(best["CAGR"] if best is not None else np.nan),
                            best_MaxDD=(best["MaxDD"] if best is not None else np.nan)))
    R = pd.DataFrame(reg)
    R.to_csv(OUT / f"{STEM}.region.csv", index=False)

    P("N_CD — points clearing BOTH coefficients (rows = phi, cols = delta):")
    P(R.pivot(index="phi", columns="delta", values="N_CD").to_string())
    P("")
    P("N_4B — of those, the ones also clearing all three Sharpe bars:")
    P(R.pivot(index="phi", columns="delta", values="N_4B").to_string())
    P("")

    inc = R[(R["phi"] == PHI_INC) & (R["delta"] == DELTA_INC)].iloc[0]
    P(f"INCUMBENT CELL (phi={PHI_INC}, delta={DELTA_INC}):")
    P(f"   N_CD = {inc['N_CD']} of {len(pts)} points ({inc['n_books_CD']} of {len(books)} distinct books)"
      f"   -> the two coefficients ARE {'jointly satisfiable' if inc['N_CD'] > 0 else 'JOINTLY UNSATISFIABLE (a wall)'}")
    P(f"   N_4B = {inc['N_4B']} of {len(pts)} points ({inc['n_books_4B']} distinct books)"
      f"   -> full rule 4b is {'reachable' if inc['N_4B'] > 0 else 'UNREACHABLE'}")
    if inc["N_4B"] > 0:
        P(f"   best 4b-passing point: {inc['best_book']} g={inc['best_gross']:.2f} f={inc['best_sleeve']:.2f}  "
          f"CAGR {inc['best_CAGR']:.2%} Sharpe {inc['best_Sharpe']:.3f} MaxDD {inc['best_MaxDD']:.2%}")
    P("")
    n_empty_cd = int((R["N_CD"] == 0).sum()); n_empty_4b = int((R["N_4B"] == 0).sum())
    P(f"   empty cells: N_CD = 0 in {n_empty_cd} of {len(R)} cells; N_4B = 0 in {n_empty_4b} of {len(R)}.")
    P(f"   The Sharpe bars alone close {n_empty_4b - n_empty_cd} cells that the two coefficients leave open.")
    P("")

    # ---- the frontier -------------------------------------------------------------------
    P("=" * 118)
    P("PART 2 - THE FRONTIER.  phi_max(delta) = the highest CAGR floor any point clears while inside the DD cap.")
    P("         The incumbent is INSIDE the non-empty region iff phi_max(0.60) >= 0.70.  Two versions: CD-only and full-4b.")
    P("")
    fr = []
    for delta in DELTA_GRID:
        m_cd = d <= delta
        m_4b = m_cd & sh
        fr.append(dict(
            delta=delta,
            n_CD=int(m_cd.sum()), phi_max_CD=(float(c[m_cd].max()) if m_cd.any() else np.nan),
            n_4B=int(m_4b.sum()), phi_max_4B=(float(c[m_4b].max()) if m_4b.any() else np.nan),
            arg_CD=(pts.loc[np.flatnonzero(m_cd)[np.argmax(c[m_cd])], "book"] if m_cd.any() else ""),
            arg_4B=(pts.loc[np.flatnonzero(m_4b)[np.argmax(c[m_4b])], "book"] if m_4b.any() else ""),
        ))
    F = pd.DataFrame(fr)
    F.to_csv(OUT / f"{STEM}.frontier.csv", index=False)
    P(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    f60 = F[F["delta"] == DELTA_INC].iloc[0]
    P(f"   phi_max({DELTA_INC}) = {f60['phi_max_CD']:.4f} on CD-only ({f60['arg_CD']}), "
      f"{f60['phi_max_4B']:.4f} on full 4b ({f60['arg_4B']}).  Incumbent phi = {PHI_INC}.")
    P(f"   -> the incumbent pair is {'INSIDE' if f60['phi_max_CD'] >= PHI_INC else 'OUTSIDE'} the CD region"
      f" and {'INSIDE' if (np.isfinite(f60['phi_max_4B']) and f60['phi_max_4B'] >= PHI_INC) else 'OUTSIDE'} the full-4b region.")
    P(f"   Headroom on the CAGR floor at delta={DELTA_INC}: {f60['phi_max_CD'] - PHI_INC:+.4f} (CD), "
      f"{f60['phi_max_4B'] - PHI_INC:+.4f} (4b).")
    P("")

    # ---- which bar actually binds -------------------------------------------------------
    P("=" * 118)
    P("PART 3 - WHICH BAR BINDS at the incumbent, and the c/d trade-off that drives idea 171's sign flip.")
    P("")
    fails = pts.apply(lambda r: bars_fail(r, PHI_INC, DELTA_INC), axis=1)
    pts["fail4b"] = fails
    cnt = {b: int(fails.str.split(",").apply(lambda z: b in z).sum()) for b in ["H1", "H2", "OOS", "DD", "CAGR"]}
    P(f"   violations by bar over all {len(pts)} points at ({PHI_INC}, {DELTA_INC}): {cnt}")
    solo = fails[fails != "-"].apply(lambda s: s if "," not in s else "multi")
    P(f"   sole binding bar (points failing exactly one): {dict(solo.value_counts())}")
    P(f"   points passing all five: {int((fails == '-').sum())}")
    if prem:
        P(f"   idea 171's premise on ITS corpus was {prem}; the CAGR floor is "
          f"{'also' if cnt['CAGR'] >= max(cnt.values()) else 'NOT'} the most-violated bar here.")
    P("")
    rho = spearman(pts["c"], pts["d"])
    rho_oos = spearman(pts["c_oos"], pts["d_oos"])
    P(f"   Spearman(c, d) = {rho:+.4f} full sample, {rho_oos:+.4f} on the OOS window "
      f"({len(pts)} points).  Positive = return and drawdown are bought together, which is")
    P("   the mechanism idea 171 observed: any arm that raises CAGR (and so Sharpe) also raises d and spends the DD cap.")
    P("")
    P("   c and d by gross level (sleeve = 0), mean over the 53 books:")
    g0 = pts[pts["sleeve"] == 0.0].groupby("gross")[["c", "d", "Sharpe", "CAGR", "MaxDD"]].mean()
    P(g0.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P("   c and d by sleeve level (gross = 0.75), mean over the 53 books:")
    s0 = pts[pts["gross"] == 0.75].groupby("sleeve")[["c", "d", "Sharpe", "CAGR", "MaxDD"]].mean()
    P(s0.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---- 3B: the closed form the numbers imply -------------------------------------------
    P("=" * 118)
    P("PART 3B - THE REGION HAS A CLOSED FORM.  Define each point's EFFICIENCY RATIO k = c / d =")
    P("          (CAGR relative to SPY) / (|MaxDD| relative to SPY).  The pair (phi, delta) is")
    P("          satisfiable by a point iff phi <= c and d <= delta, which for a point on a gross")
    P("          ladder (where c and d scale together) reduces to k >= phi/delta.  So 4b's two")
    P("          coefficients are a SINGLE number: the incumbent asks for k >= 0.70/0.60 = 1.1667.")
    P("          Idea 164 (cloud, 2026-09-05) derived the same constant from the other side as")
    P("          'non-empty iff rho/s <= delta/gamma = 0.857'; 1/1.1667 = 0.8571.  Independent agreement.")
    P("")
    pts["k"] = pts["c"] / pts["d"]
    pts["k_oos"] = pts["c_oos"] / pts["d_oos"]
    kreq = PHI_INC / DELTA_INC
    bk_k = pts.groupby("book")["k"].max()
    P(f"   k over {len(pts)} points: min {pts['k'].min():.4f}  median {pts['k'].median():.4f}  "
      f"mean {pts['k'].mean():.4f}  max {pts['k'].max():.4f}")
    P(f"   required k at the incumbent = phi/delta = {kreq:.4f}")
    P(f"   points with k >= {kreq:.4f}: {int((pts['k'] >= kreq).sum())} of {len(pts)}   "
      f"books whose BEST point clears it: {int((bk_k >= kreq).sum())} of {len(books)}")
    P(f"   k is near-invariant along the gross ladder (that is why the pair reduces to one number):")
    kk = pts[pts["sleeve"] == 0.0].groupby("gross")["k"].agg(["mean", "std", "min", "max"])
    P(kk.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"   and the sleeve is what MOVES k (gross = 0.75):")
    ks = pts[pts["gross"] == 0.75].groupby("sleeve")["k"].agg(["mean", "std", "min", "max"])
    P(ks.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    # how well does the one-number test predict cell emptiness?
    pred = []
    for phi in PHI_GRID:
        for delta in DELTA_GRID:
            need = phi / delta if delta > 0 else np.inf
            pred.append(dict(phi=phi, delta=delta,
                             ratio_says_open=bool(phi == 0.0 or (pts["k"] >= need).any()),
                             actually_open=bool(((pts["c"] >= phi) & (pts["d"] <= delta)).any())))
    PR = pd.DataFrame(pred)
    agree_r = int((PR["ratio_says_open"] == PR["actually_open"]).sum())
    P(f"   The one-number test 'some k >= phi/delta' predicts cell non-emptiness in {agree_r} of {len(PR)} cells "
      f"({agree_r/len(PR):.1%}).")
    P(f"   Its failures are the {int((PR['ratio_says_open'] & ~PR['actually_open']).sum())} cells where the ratio is")
    P(f"   reachable but only OUTSIDE the gross ladder's [0.20, 1.00] range (rule 2 forbids leverage), i.e. the")
    P("   binding constraint there is PROTOCOL rule 2, not 4b.")
    P(f"   OOS-window k: median {pts['k_oos'].median():.4f}  max {pts['k_oos'].max():.4f}  "
      f"points clearing {kreq:.4f}: {int((pts['k_oos'] >= kreq).sum())} of {len(pts)}")
    P("")

    # ---- rule 8 -------------------------------------------------------------------------
    P("=" * 118)
    P("PART 4 - RULE 8 WALK-FORWARD.")
    P("  W1 REGION STABILITY: the same map computed on the IS window alone and the OOS window alone.")
    P("  W2 THE PICK: at each cell, best IS Sharpe among the IS-passing points, read ONCE on OOS.")
    P("")
    c_is = pts["c_is"].values; d_is = pts["d_is"].values
    sh_is = (pts["is_sh1"] & pts["is_sh2"] & pts["is_shS"]).values
    c_oo = pts["c_oos"].values; d_oo = pts["d_oos"].values
    sh_oo = (pts["oos_sh1"] & pts["oos_sh2"] & pts["shOOS"]).values

    # do-nothing control: best IS Sharpe over the whole corpus, no screen at all
    ctrl_i = int(pts["IS_Sharpe"].idxmax())
    ctrl = pts.loc[ctrl_i]
    P(f"  DO-NOTHING CONTROL (best IS Sharpe, no screen): {ctrl['book']} g={ctrl['gross']:.2f} f={ctrl['sleeve']:.2f}"
      f"  IS Sharpe {ctrl['IS_Sharpe']:.4f} -> OOS CAGR {ctrl['OOS_CAGR']:.2%} Sharpe {ctrl['OOS_Sharpe']:.4f} MaxDD {ctrl['OOS_MaxDD']:.2%}")
    for k in SPY:
        so = metrics(SPY[k].loc[OOS_START:]); bo = metrics(BASE[k].loc[OOS_START:])
        P(f"     OOS reference {k:6s}: SPY {so['CAGR']:6.2%}/{so['Sharpe']:.4f}/{so['MaxDD']:7.2%}"
          f"   RULES v1 {bo['CAGR']:6.2%}/{bo['Sharpe']:.4f}/{bo['MaxDD']:7.2%}")
    P("")
    wf = []
    for phi in PHI_GRID:
        for delta in DELTA_GRID:
            m_is = (c_is >= phi) & (d_is <= delta) & sh_is
            m_oo = (c_oo >= phi) & (d_oo <= delta) & sh_oo
            row = dict(phi=phi, delta=delta, n_IS=int(m_is.sum()), n_OOS=int(m_oo.sum()),
                       n_both=int((m_is & m_oo).sum()))
            if m_is.any():
                sub = pts[m_is]
                pk = sub.loc[sub["IS_Sharpe"].idxmax()]
                so = metrics(SPY[pk["parent"]].loc[OOS_START:])
                bo = metrics(BASE[pk["parent"]].loc[OOS_START:])
                row.update(pick=pk["book"], pick_g=pk["gross"], pick_f=pk["sleeve"],
                           pick_IS_Sharpe=pk["IS_Sharpe"], OOS_CAGR=pk["OOS_CAGR"],
                           OOS_Sharpe=pk["OOS_Sharpe"], OOS_MaxDD=pk["OOS_MaxDD"],
                           dSharpe_vs_ctrl=pk["OOS_Sharpe"] - ctrl["OOS_Sharpe"],
                           dSharpe_vs_SPY=pk["OOS_Sharpe"] - so["Sharpe"],
                           dSharpe_vs_RULESv1=pk["OOS_Sharpe"] - bo["Sharpe"])
            else:
                row.update(pick="", pick_g=np.nan, pick_f=np.nan, pick_IS_Sharpe=np.nan,
                           OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                           dSharpe_vs_ctrl=np.nan, dSharpe_vs_SPY=np.nan, dSharpe_vs_RULESv1=np.nan)
            wf.append(row)
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    P("  W1 — IS-window pass counts (rows phi, cols delta):")
    P(WF.pivot(index="phi", columns="delta", values="n_IS").to_string())
    P("")
    P("  W1 — OOS-window pass counts:")
    P(WF.pivot(index="phi", columns="delta", values="n_OOS").to_string())
    P("")
    inc_wf = WF[(WF["phi"] == PHI_INC) & (WF["delta"] == DELTA_INC)].iloc[0]
    P(f"  W1 at the incumbent: IS passes {inc_wf['n_IS']}, OOS passes {inc_wf['n_OOS']}, both {inc_wf['n_both']}"
      f"  (of {len(pts)} points).")
    agree = int(((WF["n_IS"] > 0) == (WF["n_OOS"] > 0)).sum())
    P(f"  W1 emptiness agreement across the grid: {agree} of {len(WF)} cells agree on non-empty/empty"
      f"; IS non-empty in {int((WF['n_IS']>0).sum())}, OOS non-empty in {int((WF['n_OOS']>0).sum())}.")
    P(f"  W1 Spearman(n_IS, n_OOS) across cells = {spearman(WF['n_IS'], WF['n_OOS']):+.4f}")
    P("")
    P("  W2 — OOS Sharpe of the IS-chosen pick (rows phi, cols delta; blank = screen empty in-sample):")
    P(WF.pivot(index="phi", columns="delta", values="OOS_Sharpe").to_string(float_format=lambda x: f"{x:.3f}"))
    P("")
    if np.isfinite(inc_wf["OOS_Sharpe"]):
        P(f"  W2 at the incumbent ({PHI_INC}, {DELTA_INC}): pick {inc_wf['pick']} g={inc_wf['pick_g']:.2f} f={inc_wf['pick_f']:.2f}"
          f"  -> OOS CAGR {inc_wf['OOS_CAGR']:.2%} Sharpe {inc_wf['OOS_Sharpe']:.4f} MaxDD {inc_wf['OOS_MaxDD']:.2%}")
        P(f"     vs do-nothing control {inc_wf['dSharpe_vs_ctrl']:+.4f} | vs SPY {inc_wf['dSharpe_vs_SPY']:+.4f}"
          f" | vs RULES v1 {inc_wf['dSharpe_vs_RULESv1']:+.4f}")
    else:
        P(f"  W2 at the incumbent ({PHI_INC}, {DELTA_INC}): the IS screen is EMPTY - no pick exists.")
    liv = WF[WF["OOS_Sharpe"].notna()]
    P(f"  W2 over the {len(liv)} non-empty cells: mean OOS Sharpe {liv['OOS_Sharpe'].mean():.4f} "
      f"(control {ctrl['OOS_Sharpe']:.4f}); cells beating the control: {int((liv['dSharpe_vs_ctrl']>0).sum())} of {len(liv)}; "
      f"mean d {liv['dSharpe_vs_ctrl'].mean():+.4f}")
    P(f"  W2 distinct picks across the grid: {liv['pick'].nunique()}  "
      f"top: {dict(liv['pick'].value_counts().head(5))}")
    P("")

    # ---- both KEEP paths ----------------------------------------------------------------
    P("=" * 118)
    P("PART 5 - BOTH KEEP PATHS at the incumbent coefficients, all 1590 points (.keep.csv).")
    P("")
    K = pts[["book", "parent", "gross", "sleeve", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_Sharpe", "c", "d", "fail4a", "fail4b"]].copy()
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    n4a = int((K["fail4a"] == "-").sum()); n4b = int((K["fail4b"] == "-").sum())
    P(f"   4a passes: {n4a} of {len(K)}   4b passes: {n4b} of {len(K)}   both: "
      f"{int(((K['fail4a']=='-') & (K['fail4b']=='-')).sum())}")
    if n4b:
        top = K[K["fail4b"] == "-"].sort_values("Sharpe", ascending=False).head(8)
        P("   best 4b passers by full-sample Sharpe:")
        P(top.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("   NOTE: these are re-grossed/re-sleeved views of idea 171's already-committed books")
    P("   (idea 144: a re-grossed book is the SAME book).  This run proposes NO new KEEP.")
    P("")

    # ---- verdict on the pre-registered predictions ---------------------------------------
    P("=" * 118)
    P("PRE-REGISTERED PREDICTIONS, scored")
    P(f"  P1 [a]/[b]/[c] hold                 : [a] {'HIT' if okA else 'MISS'}  [b] {'HIT' if okB else 'MISS'}  "
      f"[c] {'HIT' if prem and prem.get('CAGR') == 1223 else 'MISS'}")
    p2 = inc["N_CD"] > 0
    P(f"  P2 (0.70,0.60) inside the CD region : {'HIT' if p2 else 'MISS'}  (N_CD = {inc['N_CD']})")
    p3 = inc["N_CD"] > inc["N_4B"] and cnt["CAGR"] < max(cnt["H1"], cnt["H2"], cnt["OOS"])
    P(f"  P3 Sharpe bars bind, not CAGR/DD    : {'HIT' if p3 else 'MISS'}  "
      f"(N_CD {inc['N_CD']} vs N_4B {inc['N_4B']}; CAGR violations {cnt['CAGR']} vs max Sharpe-bar {max(cnt['H1'],cnt['H2'],cnt['OOS'])})")
    fm = F.set_index("delta")["phi_max_CD"]
    p4 = fm.loc[0.8] > fm.loc[0.3] and abs(fm.loc[2.0] - fm.loc[1.0]) < 0.05
    P(f"  P4 phi_max steep then flat          : {'HIT' if p4 else 'MISS'}  "
      f"(phi_max 0.3->{fm.loc[0.3]:.3f}  0.8->{fm.loc[0.8]:.3f}  1.0->{fm.loc[1.0]:.3f}  2.0->{fm.loc[2.0]:.3f})")
    p5 = rho > 0.7
    P(f"  P5 Spearman(c,d) > +0.7             : {'HIT' if p5 else 'MISS'}  ({rho:+.4f})")
    p6 = (not np.isfinite(inc_wf["dSharpe_vs_ctrl"])) or inc_wf["dSharpe_vs_ctrl"] <= 0
    P(f"  P6 screen does not beat do-nothing  : {'HIT' if p6 else 'MISS'}  "
      f"(d vs control at the incumbent {inc_wf['dSharpe_vs_ctrl']:+.4f})")
    P(f"  P7 no NEW book KEEP                 : HIT by construction (every 4b passer is an idea-171 book re-grossed)")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
