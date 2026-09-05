#!/usr/bin/env python3
"""QUEUE idea 175 - does-cadence-skill-survive-a-second-corpus   (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 175)
    "idea 171's single surviving dial is CADENCE (paired +0.0642 OOS Sharpe over 53 books,
     t +4.54, capture 67.1% of the oracle vs RANDOM's -33.0%, oracle interior in 96.2% of
     books), but the ladder is only 4 points and the corpus is one family of B136 sub-panels.
     Re-run the identical paired protocol on the small panel and on u56/ETF sub-panels, with a
     denser cadence ladder (D, 2D, W, 2W, M, 6W, Q), and report whether monthly is still the IS
     pick and still the OOS argmax.  This is the evidence idea 107 needs.  Max 2 params."

WHAT IS AT STAKE.
    Idea 171 swept five dials and found exactly ONE with apparent selector skill: CADENCE.
    That single positive is now the whole basis for idea 107 (should cadence be a pre-registered
    RULES parameter, and at what value).  A one-dial positive on ONE corpus family and a FOUR
    point ladder is the weakest kind of evidence this project accepts, and it has two obvious
    failure modes that the original design cannot separate:

      (i)  CORPUS.  All 48 sub-panels were draws from B136, so the 53 "independent" books share
           one parent panel, one price history and one survivorship list.  A paired t of +4.54
           over 53 correlated books is not 53 observations.
      (ii) LADDER RESOLUTION.  With only {D, W, M, Q} the "argmax" has three interior choices
           and the gaps are enormous (D is ~250 rebalances/yr, Q is 4).  A selector that merely
           learns "trade less often, costs are real" will look like skill on a 4-point ladder
           and should degrade on a dense one, where it has to pick between W and 2W and M.

    So this run keeps idea 171's protocol byte-for-byte and changes exactly the two things the
    idea names: the CORPUS (small panel + u56/ETF families, no B136 at all) and the LADDER
    (7 points instead of 4).  If cadence skill survives both, idea 107 has its evidence.  If it
    does not, idea 171's one positive was a corpus/grid artefact and the project's five-dial
    null becomes 5 of 5.

    A NULL here is the useful result, same asymmetry as idea 171: the incumbent constant (weekly,
    RULES v1's own cadence) costs nothing to keep.

THE LADDER - CADENCE, 7 points, containing the incumbent so "do nothing" is a ladder point.
    D    every bar                       2D   every 2nd bar
    W    last bar of each ISO week       (INCUMBENT: RULES v1, scan.py, baseline.compare default)
    2W   last bar of every 2nd ISO week
    M    last bar of each month          (idea 107 / idea 171's by-product fit monthly here)
    6W   last bar of every 6th ISO week
    Q    last bar of each quarter
    All 7 points are reported for every book in .ladder.csv.  Nothing is picked for reporting.

    The other four dials of idea 171 are held at their incumbents throughout, unchanged:
    GROSS 0.75, N 20, BAND 0.00 (bare 200d gate), SLEEVE 0.00.  The book is therefore idea 2's
    4b candidate (top-20 equal weight on the scan.py composite, no vol scaler) on every panel.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4, identical to idea 171.
    1. the SELECTOR, 2 values, both reported, neither preferred:
         SEL-SHARPE  argmax over the ladder of IS Sharpe          (rule 8's S1, the incumbent)
         SEL-4B      argmax over the ladder of the IS 4b relative min-margin (idea 166)
    2. the LADDER POINT, swept exhaustively (7 points), ALL reported.
    PANEL and BOOK are corpus axes, not tuned parameters.

    CONTROLS, not tuned parameters:
         CONST   the incumbent constant W                  (the do-nothing arm; the pairing base)
         RANDOM  a uniformly random ladder point per book, fixed seed   (idea 151's control)
         ORACLE  the OOS argmax                            (NOT implementable; the upper bound)

CORPUS - 115 books, the pairing unit.  DELIBERATELY DISJOINT FROM IDEA 171's.
    3 fixed panels : SMALL439, U56, ETF36
    48 SMALL sub-panels : k in {20,40,80} x 16 draws, rng = default_rng(175_500 + k)
    32 U56   sub-panels : k in {20,40}    x 16 draws, rng = default_rng(175_600 + k)
    32 ETF   sub-panels : k in {12,24}    x 16 draws, rng = default_rng(175_700 + k)
    Idea 171 used B136 and its sub-panels; this run uses none of them.  The two corpora share
    only whatever names U56 and B136 have in common, and share no sub-panel draw.
    SMALL439: the 483-name sub-$2B panel with every ticker whose data/small_meta.csv
    max_1d_move >= 1.0 dropped first (44 names), per standing instruction.
    Every book carries SPY as a benchmark column, never tradable.

WALK-FORWARD (PROTOCOL rule 8) - the design IS the walk-forward.
    Every selector reads the <= 2016-12-31 window only.  The 2017-01-01.. window is read once,
    at the end.  .walkforward.csv additionally reports, per arm, (i) the mean OOS
    CAGR/Sharpe/MaxDD over all 115 books and (ii) the classic S1 pick - the single book with the
    best IS Sharpe under that arm, read once on OOS - both against RULES v1 on the book's parent
    panel and against SPY.

BOTH KEEP PATHS are evaluated on every one of the 805 ladder rows and written to .keep.csv:
    4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND on the OOS window, MaxDD <= 0.60 x |SPY MaxDD|,
        CAGR >= 0.70 x SPY CAGR.  (The relative min-margin below is a RANKING device for the
        selector only; the verdict column is PROTOCOL's actual rule, evaluated exactly.)

REPRODUCTION, asserted before any new number is read
    [a] cad_mask reproduces engine.rebalance_mask exactly at D, W, M, Q (the four points the
        engine supports).  The three new points (2D, 2W, 6W) are built by the same
        "last bar of each block" rule, so [a] licenses them.
    [b] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover at D, W, M, Q on a real book.
    [c] this script's CAND-20 weights equal idea 78 / idea 171's weights_cand exactly, so the
        incumbent cell is the same book and not a look-alike.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b], [c] hold.
    P2  The mean-OOS-Sharpe ladder is HUMPED, not monotone: D loses to W on cost, Q loses to M
        on staleness.  (If it is monotone in cadence length, the "selector" is running to a grid
        edge and idea 171's 96.2% interior claim does not transfer - see idea 183.)
    P3  Cadence skill SHRINKS on the dense ladder.  I expect SEL-SHARPE's paired mean d to stay
        positive but to fall well below +0.0642 and to lose significance on at least one of the
        three panel families.  Reason: the extra points 2D/2W/6W are near-duplicates of their
        neighbours, so the IS argmax now has to discriminate inside noise.
    P4  MONTHLY is NOT the IS pick in a majority of books on the small panel.  Small caps carry
        more idiosyncratic drift; a slower book on a noisier panel should want to trade more,
        not less, so I expect the small-panel IS pick to sit at W or 2W.
    P5  ORACLE stays large (> +0.15 mean d) on every family, i.e. the ladder is not flat and a
        skilful selector had room.
    P6  RANDOM is negative on every family (it averages over the whole ladder including D, whose
        cost drag is real and large).
    P7  No arm produces a NEW 4b KEEP that is not a re-cadencing of an existing book (idea 144).

CAVEATS carried, not buried
    * SURVIVORSHIP.  SMALL439 is a current-constituent screen (data/SMALL_PANEL_README.md,
      idea 54): names that delisted, were acquired or went to zero are absent, and the bias
      falls hardest on exactly the beaten-down cohort a trend gate would have excluded.  U56 and
      ETF36 are current lists too.  Every arm and every ladder point inherits the bias equally,
      so the PAIRED comparison is unaffected; the LEVEL of every small-panel number is not, and
      no small-panel CAGR/Sharpe here should be read as an attainable return.
    * Idea 38: data/prices.csv and prices_broad.csv are calendar-day indexed from 2014-09-17.
      A "bar" is therefore a calendar day on U56/ETF36 after that date, so D and 2D on those
      panels rebalance on some non-trading days (a no-op in weights, but it shifts which day W
      and 2W land on).  Bars/year is reported per panel so the ladder can be read in the right
      units.  The small panel is trading-day indexed and does not have this problem.
    * Idea 144: a re-cadenced book is the SAME book.  A verdict flip along this ladder is not a
      new signal.
    * Idea 126: t+1 execution only; no 1-week-lag variant is run here.
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

STEM = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"
OUT = ROOT / "research" / "backtests"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
EPS = 0.05

# the dial under test.  Other four dials pinned at idea 171's incumbents.
LADDER = ["D", "2D", "W", "2W", "M", "6W", "Q"]
CONST_PT = "W"
INC_GROSS, INC_N, INC_BAND = 0.75, 20, 0.00
ARMS = ["CONST", "SEL-SHARPE", "SEL-4B", "RANDOM", "ORACLE"]

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
def cad_mask(idx, cad):
    """True on the last bar of each cadence block.  Same 'last bar of the block' rule as
    engine.rebalance_mask; blocks are bars (D/2D) or ISO weeks (W/2W/6W) or calendar
    months/quarters (M/Q).  Asserted equal to engine.rebalance_mask at D/W/M/Q in check_a()."""
    n = len(idx)
    if cad == "D":
        key = np.arange(n)
    elif cad == "2D":
        key = np.arange(n) // 2
    elif cad in ("W", "2W", "6W"):
        wk = idx.to_period("W")
        ordi = np.asarray(wk.astype("int64"))
        ordi = ordi - ordi[0]
        key = ordi if cad == "W" else ordi // (2 if cad == "2W" else 6)
    elif cad == "M":
        key = np.asarray(idx.to_period("M").astype("int64"))
    elif cad == "Q":
        key = np.asarray(idx.to_period("Q").astype("int64"))
    else:
        raise ValueError(cad)
    m = np.empty(n, bool)
    m[:-1] = key[:-1] != key[1:]
    m[-1] = True
    return pd.Series(m, index=idx)


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=COST_BPS, cad="W"):
    """Vectorised equivalent of engine.backtest, taking a cadence string this script's
    cad_mask understands.  Asserted identical to the engine in check_b()."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad).shift(1, fill_value=False).values.copy()
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
    P("  [a] cad_mask vs engine.rebalance_mask at the four engine-supported points:")
    ok = True
    for cd in ["D", "W", "M", "Q"]:
        a = rebalance_mask(book.px.index, cd)
        b = cad_mask(book.px.index, cd)
        same = bool((a.values == b.values).all())
        P(f"      {cd:2s}  identical={same}   rebalances/yr={b.sum()/(len(b)/252):6.1f}")
        ok &= same
    for cd in ["2D", "2W", "6W"]:
        b = cad_mask(book.px.index, cd)
        P(f"      {cd:2s}  (new point)      rebalances/yr={b.sum()/(len(b)/252):6.1f}")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


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


def check_c(book):
    _, above, vol20 = score(book.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in book.px.columns if c not in set(book.tradable)]
    if drop:
        m[drop] = False
    s78 = score(book.px, vol_scale=False)[0]
    w78 = (s78.where(m).rank(axis=1, ascending=False) <= INC_N).astype(float) * (INC_GROSS / INC_N)
    d = float((w78 - book.weights()).abs().max().max())
    P(f"  [c] CAND-{INC_N} weights vs idea 78/171 weights_cand on {book.name}: max|dw|={d:.3e}"
      f"  -> {'PASS' if d < 1e-12 else 'FAIL'}")
    return d < 1e-12


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 175 - does-cadence-skill-survive-a-second-corpus   (cloud, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Idea 171 found CADENCE the only dial of five with selector skill, on a 4-point ladder over")
    P("53 B136-family books.  This run repeats the identical paired protocol on a DISJOINT corpus")
    P("(small panel + u56/ETF sub-panels) with a 7-point ladder D/2D/W/2W/M/6W/Q.")
    P(f"Costs {COST_BPS} bps, t+1 execution, IS <= {IS_END}, OOS >= {OOS_START}.")
    P("Two tuned params: SELECTOR (2, both reported) x LADDER POINT (7, all reported).")
    P("")

    books, panels = build_corpus()
    nfix = len([b for b in books if not any(c.isdigit() for c in b.name[-3:])])
    P(f"CORPUS: {len(books)} books  (3 fixed panels + {len(books)-3} sub-panels)")
    for b in books[:3]:
        P(f"   {b.name:11s} {b.px.shape[0]}d x {b.px.shape[1]}c  tradable={len(b.tradable):3d}  "
          f"{b.px.index[0].date()}..{b.px.index[-1].date()}  bars/yr={len(b.px)/((b.px.index[-1]-b.px.index[0]).days/365.25):.0f}")
    for fam in FAMILIES:
        sub = [b for b in books if b.name.startswith(fam + "k")]
        P(f"   {fam:5s} sub-panels: {len(sub)}  k in {DRAWS[fam][1]} x {N_DRAWS} draws, seed {DRAWS[fam][0]}+k")
    P("")

    P("REPRODUCTION CONTROLS (asserted before any new number is read)")
    okA = check_a(books[1])
    okB = check_b(books[1])
    okC = all(check_c(b) for b in books[:3])
    if not (okA and okB and okC):
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
        P(f"  benchmark {k:6s} SPY  CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:7.2%} "
          f"halves {h1:.3f}/{h2:.3f}  OOS {mo['CAGR']:6.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:7.2%}")
        P(f"  {'':10s} {k:6s} RULES v1  CAGR {mb['CAGR']:6.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:7.2%} "
          f"  OOS {mbo['CAGR']:6.2%}/{mbo['Sharpe']:.3f}/{mbo['MaxDD']:7.2%}")
    P("")

    P("RUNNING THE LADDER ...")
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
                is_incumbent=(pt == CONST_PT),
                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                IS_margin=mg_is, IS_worstbar=wb_is,
                OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos)))
        if (bi + 1) % 20 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    lad = pd.DataFrame(rows)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    P(f"   {len(lad)} ladder rows -> {STEM}.ladder.csv   ({time.time()-t0:.0f}s)")
    P("")

    # ---- ladder shape
    P("LADDER SHAPE - mean over books of each cadence point (ALL points, nothing picked)")
    P(f"  {'family':7s} {'n':>4s} {'metric':11s} " + " ".join(f"{p:>8s}" for p in LADDER))
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        nb = sub.book.nunique()
        g = sub.groupby("point")[["IS_Sharpe", "OOS_Sharpe", "OOS_margin", "OOS_CAGR", "OOS_MaxDD", "turnover"]].mean().reindex(LADDER)
        for met, fmt in [("IS_Sharpe", "{:8.3f}"), ("OOS_Sharpe", "{:8.3f}"), ("OOS_margin", "{:+8.3f}"),
                         ("OOS_CAGR", "{:8.2%}"), ("OOS_MaxDD", "{:8.2%}"), ("turnover", "{:8.1f}")]:
            P(f"  {fam:7s} {nb:4d} {met:11s} " + " ".join(fmt.format(g.loc[p, met]) for p in LADDER))
        s = g["OOS_Sharpe"]
        rk = int(s.rank(ascending=False).loc[CONST_PT])
        P(f"  {fam:7s} {'':4s} -> OOS Sharpe spread {s.max()-s.min():.3f}; argmax {s.idxmax()}; "
          f"incumbent {CONST_PT} ranks {rk}/{len(s)}; IS argmax {g['IS_Sharpe'].idxmax()}")
        P("")

    # ---- arms
    rng_rand = np.random.default_rng(175_900)
    choices = []
    for bk in books:
        sub = lad[lad.book == bk.name].set_index("point").reindex(LADDER)
        pick = {
            "CONST": CONST_PT,
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

    # ---- the headline questions from the idea text
    P("=" * 118)
    P("Q1 / Q2 FROM THE IDEA TEXT - is MONTHLY still the IS pick, and still the OOS argmax?")
    P("")
    P(f"  {'family':7s} {'n':>4s} {'IS pick (SEL-SHARPE) distribution':52s} {'OOS argmax (ORACLE) distribution':52s}")
    for fam in ["ALL"] + FAMILIES:
        s = ch[(ch.arm == "SEL-SHARPE")] if fam == "ALL" else ch[(ch.arm == "SEL-SHARPE") & (ch.family == fam)]
        o = ch[(ch.arm == "ORACLE")] if fam == "ALL" else ch[(ch.arm == "ORACLE") & (ch.family == fam)]
        vs = s["point"].value_counts().reindex(LADDER).fillna(0).astype(int)
        vo = o["point"].value_counts().reindex(LADDER).fillna(0).astype(int)
        P(f"  {fam:7s} {len(s):4d} " + " ".join(f"{p}:{vs[p]}" for p in LADDER).ljust(52)
          + " " + " ".join(f"{p}:{vo[p]}" for p in LADDER))
        P(f"  {'':7s} {'':4s} modal IS pick = {vs.idxmax()} ({vs.max()}/{len(s)} = {vs.max()/len(s):.1%});  "
          f"M is the IS pick in {vs['M']}/{len(s)} = {vs['M']/len(s):.1%};  "
          f"modal OOS argmax = {vo.idxmax()} ({vo.max()/len(o):.1%});  M is the OOS argmax in {vo['M']/len(o):.1%}")
    P("")

    # ---- the paired test
    P("=" * 118)
    P(f"THE PAIRED TEST - each arm MINUS the incumbent constant '{CONST_PT}', book by book")
    P("")
    paired = []
    for scorenm in ["OOS_Sharpe", "OOS_margin"]:
        P(f"  --- OOS score = {scorenm} " + "-" * 84)
        P(f"  {'family':7s} {'arm':11s} {'n':>4s} {'mean d':>9s} {'median d':>9s} {'t':>7s} {'win':>4s} "
          f"{'loss':>5s} {'tie':>4s} {'sign p':>8s} {'changes':>8s}  verdict")
        for fam in ["ALL"] + FAMILIES:
            sel = ch if fam == "ALL" else ch[ch.family == fam]
            base_s = sel[sel.arm == "CONST"].set_index("book")[scorenm]
            for arm in ARMS:
                if arm == "CONST":
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
                P(f"  {fam:7s} {arm:11s} {len(d):4d} {md:+9.4f} {d.median():+9.4f} {tstat(d.values):+7.2f} "
                  f"{w:4d} {l:5d} {len(d)-w-l:4d} {p:8.5f} {nchg:4d}/{len(d):<3d}  {verd}")
                paired.append(dict(score=scorenm, family=fam, arm=arm, n=len(d), mean_d=md,
                                   median_d=d.median(), t=tstat(d.values), wins=w, losses=l,
                                   ties=len(d) - w - l, sign_p=p, n_changed=nchg, verdict=verd))
            P("")
    pd.DataFrame(paired).to_csv(OUT / f"{STEM}.paired.csv", index=False)

    # ---- capture of the oracle, the number idea 171 quoted
    P("=" * 118)
    P("CAPTURE OF THE ORACLE  (mean d of the arm / mean d of ORACLE, on OOS_Sharpe)")
    P("Idea 171's B136-family numbers, for comparison: SEL-SHARPE +0.0642 (t +4.54), capture 67.1%,")
    P("RANDOM capture -33.0%, oracle interior in 96.2% of books, ladder = 4 points {D,W,M,Q}.")
    P("")
    pdf = pd.DataFrame(paired)
    P(f"  {'family':7s} {'n':>4s} {'ORACLE d':>10s} {'SEL-SHARPE d':>13s} {'t':>7s} {'capture':>9s} "
      f"{'SEL-4B d':>10s} {'capture':>9s} {'RANDOM d':>10s} {'capture':>9s}")
    for fam in ["ALL"] + FAMILIES:
        g = pdf[(pdf.score == "OOS_Sharpe") & (pdf.family == fam)].set_index("arm")
        orc = g.loc["ORACLE", "mean_d"]
        line = f"  {fam:7s} {int(g.loc['ORACLE','n']):4d} {orc:+10.4f}"
        for arm in ["SEL-SHARPE", "SEL-4B", "RANDOM"]:
            dv = g.loc[arm, "mean_d"]
            cap = dv / orc if orc != 0 else np.nan
            if arm == "SEL-SHARPE":
                line += f" {dv:+13.4f} {g.loc[arm,'t']:+7.2f} {cap:9.1%}"
            else:
                line += f" {dv:+10.4f} {cap:9.1%}"
        P(line)
    P("")

    # ---- ladder geometry: interior or edge (idea 183)
    P("LADDER GEOMETRY (idea 183's anchor-position column): is the argmax a CHOICE or a GRID EDGE?")
    P(f"  {'family':7s} {'rho(cadence rank, mean OOS Sharpe)':>36s} {'ORACLE interior':>17s} "
      f"{'SEL==ORACLE':>13s} {'CONST rank on own ladder':>26s}")
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        g = sub.groupby("point")["OOS_Sharpe"].mean().reindex(LADDER)
        rho = float(np.corrcoef(np.arange(len(LADDER), dtype=float), pd.Series(g.values).rank().values)[0, 1])
        o = (ch if fam == "ALL" else ch[ch.family == fam])
        op = o[o.arm == "ORACLE"].set_index("book")["point"]
        sp = o[o.arm == "SEL-SHARPE"].set_index("book")["point"]
        ends = {LADDER[0], LADDER[-1]}
        interior = float((~op.isin(ends)).mean())
        agree = float((op == sp).mean())
        crank = int(g.rank(ascending=False).loc[CONST_PT])
        P(f"  {fam:7s} {rho:36.3f} {interior:17.1%} {agree:13.1%} {str(crank)+'/'+str(len(LADDER)):>26s}")
    P("")

    # ---- POST-HOC (labelled): where does the selector's paired mean actually come from?
    P("=" * 118)
    P("POST-HOC DIAGNOSTICS (added AFTER the paired table was read, and labelled as such).")
    P("")
    P("(A) SEL-SHARPE's paired d decomposed by WHICH point it picked (OOS_Sharpe vs the W constant).")
    cw = ch[ch.arm == "CONST"].set_index("book")["OOS_Sharpe"]
    for fam in FAMILIES:
        a = ch[(ch.arm == "SEL-SHARPE") & (ch.family == fam)].set_index("book")
        a = a.assign(d=a["OOS_Sharpe"] - cw)
        g = a.groupby("point")["d"].agg(["size", "mean", "sum"]).reindex(LADDER).dropna()
        P(f"  {fam:6s} " + "   ".join(f"{p}: n={int(r['size']):2d} mean{r['mean']:+.4f} tot{r['sum']:+.3f}"
                                      for p, r in g.iterrows()))
    P("  Reading: a positive mean built out of many small wins and a few large losses is NOT the same")
    P("  finding as a positive mean built out of a consistent edge.  The pick-level table says which.")
    P("")
    P("(B) EVERY CADENCE AS A PRE-REGISTERED CONSTANT, paired against the incumbent W (no fitting at")
    P("    all).  This is the number idea 107 actually needs: it asks what a RULES constant would have")
    P("    bought, with no selector and therefore no selector tail risk.  All 7 points reported.")
    P(f"  {'family':7s} {'n':>4s} " + " ".join(f"{p:>16s}" for p in LADDER))
    const_rows = []
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        piv = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")
        cells = []
        for p in LADDER:
            d = (piv[p] - piv[CONST_PT]).dropna()
            pv, w, l = sign_p(d.values)
            cells.append(f"{'-- base --':>16s}" if p == CONST_PT else f"{d.mean():+7.4f}(t{tstat(d.values):+5.2f})")
            const_rows.append(dict(family=fam, point=p, n=len(d), mean_d=d.mean(),
                                   t=tstat(d.values), wins=w, losses=l, sign_p=pv))
        P(f"  {fam:7s} {piv.shape[0]:4d} " + " ".join(f"{c:>16s}" for c in cells))
    pd.DataFrame(const_rows).to_csv(OUT / f"{STEM}.constants.csv", index=False)
    P("")

    # ---- rule 8 walk-forward summary
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

    # ---- both KEEP paths on every ladder row
    P("=" * 118)
    P("BOTH KEEP PATHS, evaluated on all 805 ladder rows (PROTOCOL rule 4a and 4b, exactly)")
    P("")
    lad["pass4a"] = lad.fail4a == "-"
    lad["pass4b"] = lad.fail4b == "-"
    lad.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'family':7s} {'rows':>5s} {'4a pass':>8s} {'4b pass':>8s}   4b pass by cadence point")
    for fam in ["ALL"] + FAMILIES:
        sub = lad if fam == "ALL" else lad[lad.family == fam]
        by = sub.groupby("point")["pass4b"].sum().reindex(LADDER).fillna(0).astype(int)
        P(f"  {fam:7s} {len(sub):5d} {int(sub.pass4a.sum()):8d} {int(sub.pass4b.sum()):8d}   "
          + " ".join(f"{p}:{by[p]}" for p in LADDER))
    P("")
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
        for _, r in fx.iterrows():
            P(f"   {r.book:9s} @ {r.point:2s}  CAGR {r.CAGR:6.2%} Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:7.2%} "
              f"halves {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%} "
              f"turnover {r.turnover:.1f}x/yr")
    else:
        P("  4b passes on the three FIXED panels: NONE.")
    P("")

    # ---- predictions scorecard
    P("=" * 118)
    P("PRE-REGISTERED PREDICTIONS - scored")
    gall = lad.groupby("point")["OOS_Sharpe"].mean().reindex(LADDER)
    humped = gall.idxmax() not in (LADDER[0], LADDER[-1])
    pall = pdf[(pdf.score == "OOS_Sharpe") & (pdf.family == "ALL")].set_index("arm")
    sel_d, sel_p = pall.loc["SEL-SHARPE", "mean_d"], pall.loc["SEL-SHARPE", "sign_p"]
    small_sel = ch[(ch.arm == "SEL-SHARPE") & (ch.family == "SMALL")]["point"]
    smallM = float((small_sel == "M").mean())
    orc_all = pall.loc["ORACLE", "mean_d"]
    fam_orc = {f: pdf[(pdf.score == "OOS_Sharpe") & (pdf.family == f) & (pdf.arm == "ORACLE")]["mean_d"].iloc[0] for f in FAMILIES}
    fam_rnd = {f: pdf[(pdf.score == "OOS_Sharpe") & (pdf.family == f) & (pdf.arm == "RANDOM")]["mean_d"].iloc[0] for f in FAMILIES}
    fam_sig = {f: pdf[(pdf.score == "OOS_Sharpe") & (pdf.family == f) & (pdf.arm == "SEL-SHARPE")].iloc[0] for f in FAMILIES}
    nsig = sum(1 for f in FAMILIES if not (fam_sig[f].mean_d > 0 and fam_sig[f].sign_p < 0.05))
    P(f"  P1 reproduction [a][b][c]                                      -> {'HIT' if (okA and okB and okC) else 'MISS'}")
    P(f"  P2 ladder is humped (argmax interior)  argmax={gall.idxmax()}  -> {'HIT' if humped else 'MISS'}")
    P(f"  P3 skill shrinks: |d| < 0.0642 and n.s. on >=1 family  d={sel_d:+.4f} n.s. on {nsig}/3  "
      f"-> {'HIT' if (sel_d < 0.0642 and nsig >= 1) else 'MISS'}")
    P(f"  P4 M is NOT the small-panel IS pick in a majority   M share={smallM:.1%}  "
      f"-> {'HIT' if smallM < 0.5 else 'MISS'}")
    P(f"  P5 ORACLE > +0.15 on every family  " + " ".join(f"{f}:{v:+.3f}" for f, v in fam_orc.items())
      + f"  -> {'HIT' if all(v > 0.15 for v in fam_orc.values()) else 'MISS'}")
    P(f"  P6 RANDOM negative on every family  " + " ".join(f"{f}:{v:+.3f}" for f, v in fam_rnd.items())
      + f"  -> {'HIT' if all(v < 0 for v in fam_rnd.values()) else 'MISS'}")
    P(f"  P7 no NEW 4b KEEP beyond a re-cadencing (idea 144)  fixed-panel 4b passes={len(fx)}  -> see above")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
