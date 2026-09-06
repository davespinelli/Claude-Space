#!/usr/bin/env python3
"""QUEUE idea 221 - is-phase-sensitivity-a-book-property-or-a-panel-one   (cloud, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 221)
    "idea 187's 6W phase spread runs 0.1518 ALL / 0.2618 SMALL / 0.3957 U56 / 0.3862 ETF, i.e.
     it varies 2.6x across families and is LARGEST where idea 175's cadence effect was largest.
     Test whether phase sensitivity is predicted by the book's holding-episode length (idea 76)
     or by its eligible-name turnover: a book whose episodes are long relative to the block
     should be phase-insensitive.  If it is predictable, phase sensitivity is a screenable book
     property rather than a caveat.  Max 2 params."

WHAT IS AT STAKE
    Idea 187 killed idea 175's cadence headline by showing that at a FIXED cadence, merely moving
    the block grid moves mean OOS Sharpe by 0.15-0.40.  Idea 220 then priced every recoverable
    cadence verdict against its own phase spread.  Both treat phase sensitivity as a CAVEAT that
    attaches to a number after the fact.  This run asks whether it is instead a MEASURABLE BOOK
    PROPERTY, knowable in advance from the book's own holding behaviour.  If it is, PROTOCOL can
    carry a screen ("this book's episodes are short relative to the block, so its cadence
    comparison is uninterpretable") instead of a blanket warning; if it is not - if the whole
    signal is which PANEL the book trades - then the caveat is all there is and it belongs on
    the panel, not the book.

THE TWO PREDICTORS, exactly the two the idea names
    P1  PERSISTENCE  = mean holding-episode length measured in BLOCKS at the cadence under test
        (idea 76 / idea 9's episode audit, via the simulator's own holding indicator).  This IS
        the idea's phrase "episodes long relative to the block": an episode of mean length L bars
        at a block of B bars gives persistence L/B, and the parent's `persistence` column is that
        ratio.  PRE-REGISTERED SIGN: phase spread DECREASES in persistence.
    P2  ELIGIBLE-NAME TURNOVER = mean per-bar fractional churn of the book's ELIGIBLE set
        (|elig_t XOR elig_{t-1}| / mean |elig|), a cadence-free property of the panel-and-gate
        that exists before any rebalance rule is chosen.  PRE-REGISTERED SIGN: phase spread
        INCREASES in eligible-name turnover.
    Three CONTROL covariates are carried so a "prediction" cannot be a restatement of something
    duller: n_names (book size), the book's own OOS Sharpe LEVEL at phase 0 (a spread of Sharpes
    can scale with the Sharpe), and daily selected-set churn.

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4
    1. CADENCE POINT - swept over {2W, 6W, 8W, 10W, 2M} with Q as the k=1 zero control.  ALL
       points reported; nothing is picked.
    2. PREDICTOR     - P1 vs P2, both reported at every cadence point, plus the joint model.
    The screen threshold in the rule-8 arm is NOT a third parameter: it is fixed at the IS
    median of the predictor, chosen by construction rather than by search.

THE MEASUREMENTS, per book (115 books, idea 175's corpus verbatim, same seeds)
    spread_c   = max - min of OOS Sharpe over the k phases of cadence c            (the target)
    spreadF_c  = the same over FULL-SAMPLE Sharpe                                  (reported too)
    P1_c, P2, and the controls, computed FULL SAMPLE for the descriptive tests and
    IS-ONLY (<= 2016-12-31) for the screenability test, so that test uses no future information.

THE FOUR TESTS, pre-registered before any number was read
    T1 BOOK-OR-PANEL.  Variance share of log spread_c explained by FAMILY (3 levels) alone, by
       the two predictors alone, and by both.  Plus the direct question: is a book's phase
       sensitivity STABLE across independent cadences?  Spearman(spread_6W, spread_8W) etc.  A
       family effect with no within-family structure = panel property; cross-cadence rank
       stability + within-family prediction = book property.
    T2 PREDICTION.  Spearman(spread_c, P1_c) and Spearman(spread_c, P2), pooled and WITHIN each
       family (the within-family number is the one that decides T1's question), with the sign
       checked against the pre-registration.
    T3 SCREENABILITY.  Rank books by the IS-only predictor, split at the IS median, and compare
       the two halves' realised OOS spread.  This is the only test whose answer could put a
       clause in PROTOCOL, because it is the only one that uses no future information.
    T4 NEGATIVE CONTROL.  Q has k=1 phase freedom and its spread MUST be exactly 0.0000 for
       every book.  Any predictor that "explains" Q's spread is fitting noise in the machinery.
    T5 is POST-HOC and is labelled as such in the output.  It was added after T1-T3 came back
       null, and it asks the prior question those tests assume an answer to: is there any
       BOOK-LEVEL variation in phase to predict, or does every book in a panel get hit by the
       same phase on the same dates?  It is reported as a mechanism, never as a test.

REPRODUCTION CONTROLS, asserted before any conclusion
    [a] cad_mask at phase 0 equals engine.rebalance_mask at D, W, M, Q.
    [b] fast_backtest equals engine.backtest at D/W/M/Q to <1e-12 on returns.
    [c] THE decisive one: this run's (cad, phase) rows at 6W/8W/2M/Q must equal idea 187's
        committed .phase.csv OOS_Sharpe/OOS_CAGR/OOS_MaxDD/IS_Sharpe to <1e-9.  A failure here
        means the phase machinery is not idea 187's and nothing below is comparable; the run
        stops rather than reporting.
    [d] the episode machinery reproduces the committed episodes.csv of
        2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud on its shared
        (book, cadence) cells to <1e-9.  This is what makes P1 idea 76's quantity and not a
        new one invented here.

PROTOCOL rule 8 walk-forward (required)
    Per book, parameters chosen on <= 2016-12-31 only, OOS window 2017-01-01.. read once:
      CONST-W0   W at phase 0                                     the incumbent (RULES v1)
      REC        cadence by IS Sharpe at phase 0                   what the record does
      SCREENED   REC's cadence, but only where the book's IS persistence at that cadence is at
                 or above the IS median; otherwise fall back to W  <- what idea 221 implies
      PHASE-AVG  the IS-chosen cadence traded as the equal-weight blend of all its phases
    Mean OOS CAGR / Sharpe / MaxDD over books, reported against RULES v1 and SPY on each parent
    panel over the same OOS window.

BOTH KEEP PATHS (4a and 4b, PROTOCOL rule 4) evaluated on every (book, cadence, phase) row.

CAVEATS carried, not buried
    * SURVIVORSHIP.  SMALL439, U56, ETF36 and every sub-panel drawn from them are CURRENT-
      CONSTITUENT lists (data/SMALL_PANEL_README.md, idea 54); the small panel additionally
      drops max_1d_move >= 1.0 tickers per the standing rule.  No LEVEL here is an attainable
      return.  Phase and predictor inherit the bias identically, so the CROSS-BOOK RANK tests
      that carry this run's conclusion are not driven by it - but a screen calibrated on these
      books is calibrated on survivors.
    * Idea 38: data/prices*.csv are calendar-day indexed after 2014-09-17, so a large-cap "bar"
      can be a weekend.  This makes large-cap phase spreads a LOWER bound.
    * A phase is not a tradable choice; it is fixed by an arbitrary sample-start date.  Nothing
      here recommends choosing one.
    * 10 bps, t+1 execution, single cost rung (idea 188 established the cadence/phase structure
      is not a cost effect).
    * Idea 144: a re-cadenced book is the same book.

Deterministic, standalone.  Writes .console.txt, .phase.csv, .books.csv, .predict.csv,
.screen.csv, .walkforward.csv, .keep.csv.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_is-phase-sensitivity-a-book-property-or-a-panel-one_cloud"
PHASE_PARENT = "2026-09-06_is-6W-a-grid-edge-or-a-real-optimum_B"
EPI_PARENT = "2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud"
OUT = ROOT / "research" / "backtests"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
EPS = 0.05

INC_GROSS, INC_N = 0.75, 20
CONST_PT = "W"

# tuned parameter 1: the cadence point.  Q is the k=1 zero control (test T4).
PHASE_SPECS = [("2W", 2), ("6W", 6), ("8W", 8), ("10W", 10), ("2M", 2), ("Q", 4)]
MULTI = [c for c, k in PHASE_SPECS if c != "Q"]
PARENT_PHASE_CADS = ["6W", "8W", "2M", "Q"]          # control [c] cells
EPI_CADS = ["D", "2D", "W", "2W", "M", "6W", "Q"]    # control [d] cells
WF_LADDER = ["D", "2D", "W", "2W", "M", "6W", "Q"]   # rule-8 cadence menu (idea 175's ladder)

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


def flush():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


# ---------------------------------------------------------------- cadence masks (idea 187, verbatim)
_WEEK_K = {"W": 1, "2W": 2, "6W": 6, "7W": 7, "8W": 8, "10W": 10, "16W": 16}
_PER_K = {"M": ("M", 1), "2M": ("M", 2), "Q": ("Q", 1), "2Q": ("Q", 2)}


def cad_mask(idx, cad, phase=0):
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


def block_bars(idx, cad):
    """Mean bars per rebalance block at phase 0 - the B in 'episodes long relative to the block'."""
    m = cad_mask(idx, cad)
    return len(idx) / max(int(m.sum()), 1)


# ---------------------------------------------------------------- fast backtest (idea 175/187, verbatim)
def fast_backtest(prices, weights, cost_bps=COST_BPS, cad="W", phase=0):
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


# ---------------------------------------------------------------- holding-episode audit (idea 76, verbatim)
def held_mask(px, weights, cad, phase=0):
    idx = px.index
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad, phase).shift(1, fill_value=False).values.copy()
    mask[0] = True
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(len(idx)), side="right") - 1
    return wt[reb[seg]] > 1e-9, reb


def episode_stats(H, yrs):
    """Contiguous holding runs per name (idea 9's audit, vectorised).  Copied from EPI_PARENT."""
    A = H.T.astype(np.int8)
    Ap = np.pad(A, ((0, 0), (1, 1)))
    d = np.diff(Ap, axis=1)
    si = np.argwhere(d == 1)
    ei = np.argwhere(d == -1)
    if len(si) == 0:
        return dict(episodes=0, per_year=0.0, mean_len=np.nan, median_len=np.nan, frac_ge2=np.nan)
    lens = (ei[:, 1] - si[:, 1]).astype(float)
    return dict(episodes=int(len(lens)), per_year=len(lens) / yrs, mean_len=float(lens.mean()),
                median_len=float(np.median(lens)), frac_ge2=float((lens > 1).mean()))


# ---------------------------------------------------------------- book construction (idea 175, verbatim)
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


# ---------------------------------------------------------------- metric helpers (idea 187, verbatim)
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


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


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 4 or np.std(a) == 0 or np.std(b) == 0:
        return np.nan, np.nan, len(a)
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    r = np.corrcoef(ra, rb)[0, 1]
    n = len(a)
    t = r * np.sqrt((n - 2) / max(1e-12, 1 - r ** 2)) if abs(r) < 1 else np.inf
    return float(r), float(t), n


def ols_r2(y, X):
    """R^2 of y on [1|X]; X is a 2-D array (may have 0 columns)."""
    y = np.asarray(y, float)
    n = len(y)
    A = np.ones((n, 1)) if (X is None or np.size(X) == 0) else np.hstack([np.ones((n, 1)), np.asarray(X, float)])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ beta
    ss_t = ((y - y.mean()) ** 2).sum()
    return float(1 - (res ** 2).sum() / ss_t) if ss_t > 0 else np.nan


# ---------------------------------------------------------------- reproduction controls
def check_a(book):
    P("  [a] cad_mask(phase=0) vs engine.rebalance_mask, and rebalances/yr for every point used:")
    ok = True
    for cd in ["D", "2D", "W", "2W", "M", "6W", "8W", "10W", "2M", "Q"]:
        b = cad_mask(book.px.index, cd)
        yr = b.sum() / (len(b) / 252)
        if cd in ("D", "W", "M", "Q"):
            a = rebalance_mask(book.px.index, cd)
            same = bool((a.values == b.values).all())
            P(f"      {cd:4s} identical={same}   rebalances/yr={yr:6.1f}   block_bars={block_bars(book.px.index, cd):6.2f}")
            ok &= same
        else:
            P(f"      {cd:4s} (block point)   rebalances/yr={yr:6.1f}   block_bars={block_bars(book.px.index, cd):6.2f}")
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


def check_c(ph):
    P(f"  [c] phase-grid reproduction vs {PHASE_PARENT}.phase.csv (idea 187's committed control)")
    src = OUT / f"{PHASE_PARENT}.phase.csv"
    if not src.exists():
        P(f"      *** parent phase.csv not found at {src} -> FAIL")
        return False
    old = pd.read_csv(src)
    new = ph[ph.cad.isin(PARENT_PHASE_CADS)]
    m = old.merge(new, on=["book", "cad", "phase"], suffixes=("_o", "_n"), how="inner")
    cols = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "IS_Sharpe"]
    worst, wc = 0.0, ""
    for c in cols:
        d = float((m[c + "_o"] - m[c + "_n"]).abs().max())
        if d > worst:
            worst, wc = d, c
    ok = (len(m) == len(old)) and worst < 1e-9
    P(f"      rows: parent={len(old)}  matched={len(m)}   max|d| over {cols} = {worst:.3e} (worst: {wc})")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_d(epi):
    P(f"  [d] episode machinery vs {EPI_PARENT}.episodes.csv (idea 76's quantity)")
    src = OUT / f"{EPI_PARENT}.episodes.csv"
    if not src.exists():
        P(f"      *** parent episodes.csv not found -> FAIL")
        return False
    old = pd.read_csv(src)
    m = old.merge(epi, left_on=["book", "cadence"], right_on=["book", "cad"],
                  suffixes=("_o", "_n"), how="inner")
    worst, wc = 0.0, ""
    for c in ["mean_len", "persistence", "episodes", "block_bars"]:
        d = float((m[c + "_o"].astype(float) - m[c + "_n"].astype(float)).abs().max())
        if d > worst:
            worst, wc = d, c
    ok = (len(m) == len(old)) and worst < 1e-9
    P(f"      rows: parent={len(old)}  matched={len(m)}   max|d| = {worst:.3e} (worst: {wc})")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 221 - is-phase-sensitivity-a-book-property-or-a-panel-one   (cloud, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Idea 187 showed the 6W block phase moves mean OOS Sharpe by 0.15-0.40 and that the spread")
    P("varies 2.6x across FAMILIES.  This run asks whether that sensitivity is a BOOK property,")
    P("predictable from the book's own holding-episode length (idea 76) or its eligible-name")
    P("turnover, or merely a label on the panel it trades.")
    P(f"Costs {COST_BPS} bps, t+1 execution, IS <= {IS_END}, OOS >= {OOS_START}.")
    P("Two tuned params: CADENCE POINT (6, all reported) x PREDICTOR (2, both reported).")
    P("")

    books, panels = build_corpus()
    P(f"CORPUS: {len(books)} books  (3 fixed panels + {len(books)-3} sub-panels), idea 175's seeds")
    for b in books[:3]:
        P(f"   {b.name:11s} {b.px.shape[0]}d x {b.px.shape[1]}c  tradable={len(b.tradable):3d}  "
          f"{b.px.index[0].date()}..{b.px.index[-1].date()}")
    P("")

    P("REPRODUCTION CONTROLS [a] and [b]")
    okA = check_a(books[1])
    okB = check_b(books[1])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED - stopping before any number is read. ***")
        flush(); return
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

    # ---------------- the phase grid + the rule-8 ladder, one pass over the books
    P("RUNNING THE PHASE GRID (6 cadences x their phases) AND THE RULE-8 LADDER ...")
    ph_rows, epi_rows, lad_rows, book_rows = [], [], [], []
    phase_ret = {}      # (book, cad, phase) -> OOS returns, for the PHASE-AVG arm
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        idx = bk.px.loc[st:].index
        spy = SPY[bk.parent].reindex(idx).fillna(0.0)
        base = BASE[bk.parent].reindex(idx).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        w = bk.weights()
        fam = family_of(bk.name)

        # --- the phase grid
        for cad, nph in PHASE_SPECS:
            for phase in range(nph):
                res = fast_backtest(bk.px, w, COST_BPS, cad, phase)
                r = res["returns"].loc[st:]
                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
                h1, h2 = halves(r)
                ph_rows.append(dict(
                    book=bk.name, family=fam, parent=bk.parent, cad=cad, phase=phase,
                    OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                    IS_Sharpe=mi["Sharpe"], Sharpe=mf["Sharpe"], CAGR=mf["CAGR"], MaxDD=mf["MaxDD"],
                    H1=h1, H2=h2, turnover=res["turnover"].loc[st:].sum() / mf["Years"],
                    fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos)))
                phase_ret[(bk.name, cad, phase)] = r

        # --- the rule-8 ladder at phase 0 (the record's convention)
        for pt in WF_LADDER:
            r = phase_ret.get((bk.name, pt, 0))
            if r is None:
                r = fast_backtest(bk.px, w, COST_BPS, pt, 0)["returns"].loc[st:]
            lad_rows.append(dict(book=bk.name, family=fam, parent=bk.parent, point=pt,
                                 IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                 OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                 OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                 OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))

        # --- P1 PERSISTENCE: episodes per cadence, full sample and IS-only.
        # Windowed EXACTLY as EPI_PARENT does (traded window from index[260]), which is what
        # control [d] asserts; the IS-only variant re-runs the same machinery on the IS slice.
        i0 = int(bk.px.index.get_indexer([st])[0])
        widx = bk.px.index[i0:]
        yrs_w = len(widx) / 252.0
        n_is = int((widx <= pd.Timestamp(IS_END)).sum())
        for cad in sorted(set(EPI_CADS) | set(c for c, _ in PHASE_SPECS) | set(WF_LADDER)):
            H, reb = held_mask(bk.px, w, cad)
            reb_w = reb[reb >= i0]
            B = len(widx) / max(len(reb_w), 1)
            es = episode_stats(H[i0:], yrs_w)
            reb_is = reb_w[reb_w < i0 + n_is]
            B_is = n_is / max(len(reb_is), 1)
            es_is = episode_stats(H[i0:i0 + n_is], n_is / 252.0)
            epi_rows.append(dict(book=bk.name, family=fam, cad=cad, block_bars=B,
                                 n_names=len(bk.tradable),
                                 episodes=es["episodes"], mean_len=es["mean_len"],
                                 persistence=es["mean_len"] / B if B else np.nan,
                                 mean_len_IS=es_is["mean_len"],
                                 persistence_IS=es_is["mean_len"] / B_is if B_is else np.nan))

        # --- P2 ELIGIBLE-NAME TURNOVER + controls (cadence-free book properties)
        E = bk.elig[bk.tradable].loc[st:]
        Ev = E.values
        churn = np.abs(np.diff(Ev.astype(np.int8), axis=0)).sum(axis=1)
        nelig = Ev.sum(axis=1)
        denom = max(nelig.mean(), 1e-9)
        elig_turn = float(churn.mean() / 2.0 / denom)
        n_is = int((E.index <= pd.Timestamp(IS_END)).sum())
        elig_turn_IS = float(churn[:max(n_is - 1, 1)].mean() / 2.0 / max(nelig[:n_is].mean(), 1e-9))
        # selected-set churn, evaluated DAILY (independent of any cadence)
        rank = bk.comp.where(bk.elig).rank(axis=1, ascending=False).loc[st:]
        S = (rank <= INC_N).values
        sel_churn = float(np.abs(np.diff(S.astype(np.int8), axis=0)).sum(axis=1).mean() / 2.0 / INC_N)
        book_rows.append(dict(book=bk.name, family=fam, parent=bk.parent,
                              n_names=len(bk.tradable), mean_elig=float(denom),
                              elig_turn=elig_turn, elig_turn_IS=elig_turn_IS, sel_turn=sel_churn))
        if (bi + 1) % 25 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")

    ph = pd.DataFrame(ph_rows)
    epi = pd.DataFrame(epi_rows)
    lad = pd.DataFrame(lad_rows)
    bkp = pd.DataFrame(book_rows)
    ph.to_csv(OUT / f"{STEM}.phase.csv", index=False)
    P(f"   {len(ph)} phase rows -> {STEM}.phase.csv   ({time.time()-t0:.0f}s)")
    P("")

    P("REPRODUCTION CONTROLS [c] and [d] - the decisive ones")
    okC = check_c(ph)
    okD = check_d(epi)
    if not (okC and okD):
        P("\n*** PARENT REPRODUCTION FAILED - this run's phase/episode quantities are not the")
        P("*** record's.  Stopping before any conclusion is drawn. ***")
        flush(); return
    P("")

    # ---------------- per-book spreads, and the book table
    sp = ph.pivot_table(index=["book", "family", "cad"], columns="phase", values="OOS_Sharpe")
    spF = ph.pivot_table(index=["book", "family", "cad"], columns="phase", values="Sharpe")
    tab = pd.DataFrame({"spread": sp.max(axis=1) - sp.min(axis=1),
                        "spreadF": spF.max(axis=1) - spF.min(axis=1),
                        "lvl": sp[0]}).reset_index()
    tab = tab.merge(epi[["book", "cad", "persistence", "persistence_IS", "mean_len", "block_bars"]],
                    on=["book", "cad"], how="left")
    tab = tab.merge(bkp[["book", "parent", "n_names", "elig_turn", "elig_turn_IS", "sel_turn"]],
                    on="book", how="left")
    tab.to_csv(OUT / f"{STEM}.books.csv", index=False)

    P("=" * 118)
    P("T4  NEGATIVE CONTROL - Q has k=1 phase freedom, so its per-book spread must be exactly 0")
    q = tab[tab.cad == "Q"]
    P(f"    Q: books={len(q)}  max spread={q.spread.abs().max():.3e}  max spreadF={q.spreadF.abs().max():.3e}"
      f"   -> {'PASS' if q.spread.abs().max() < 1e-12 else 'FAIL'}")
    P("")

    P("=" * 118)
    P("PER-BOOK PHASE SPREAD (OOS Sharpe, max-min over the cadence's own phases)")
    P("  NOTE - this is NOT idea 187's family number.  187 averaged OOS Sharpe over books FIRST")
    P("  and spread the family MEANS; a per-book spread is necessarily larger.  Both are shown so")
    P("  the two are never confused.")
    par187 = pd.read_csv(OUT / f"{PHASE_PARENT}.phasesummary.csv").set_index("family")
    P(f"  {'family':7s} {'cad':4s} {'k':>3s} {'n':>4s} {'mean':>8s} {'median':>8s} {'p90':>8s} "
      f"{'max':>8s} {'187 family-mean spread':>23s}")
    for fam in ["ALL"] + FAMILIES:
        for cad, k in PHASE_SPECS:
            s = tab[tab.cad == cad] if fam == "ALL" else tab[(tab.cad == cad) & (tab.family == fam)]
            ref = ""
            col = f"phase_spread_{cad}"
            if col in par187.columns and fam in par187.index:
                ref = f"{par187.loc[fam, col]:.4f}"
            P(f"  {fam:7s} {cad:4s} {k:3d} {len(s):4d} {s.spread.mean():8.4f} {s.spread.median():8.4f} "
              f"{s.spread.quantile(0.9):8.4f} {s.spread.max():8.4f} {ref:>23s}")
        P("")

    # ---------------- T1 book or panel
    P("=" * 118)
    P("T1  BOOK OR PANEL?")
    P("  (i) variance share of log(spread) explained by FAMILY dummies alone, by the two")
    P("      PREDICTORS alone, and by both.  If family alone ~ both, it is a panel label.")
    P(f"  {'cad':4s} {'n':>4s} {'R2 family':>10s} {'R2 P1+P2':>10s} {'R2 both':>9s} {'R2 P1|fam':>10s} {'R2 P2|fam':>10s}")
    t1 = []
    for cad in MULTI:
        s = tab[(tab.cad == cad) & np.isfinite(tab.spread) & (tab.spread > 0)].dropna(
            subset=["persistence", "elig_turn"])
        if len(s) < 10:
            continue
        y = np.log(s.spread.values)
        D = pd.get_dummies(s.family).values[:, 1:].astype(float)
        X = np.column_stack([np.log(s.persistence.values), np.log(s.elig_turn.values)])
        r_f, r_p, r_b = ols_r2(y, D), ols_r2(y, X), ols_r2(y, np.hstack([D, X]))
        r_f1 = ols_r2(y, np.hstack([D, X[:, :1]])) - r_f
        r_f2 = ols_r2(y, np.hstack([D, X[:, 1:]])) - r_f
        P(f"  {cad:4s} {len(s):4d} {r_f:10.3f} {r_p:10.3f} {r_b:9.3f} {r_f1:10.3f} {r_f2:10.3f}")
        t1.append(dict(cad=cad, n=len(s), R2_family=r_f, R2_pred=r_p, R2_both=r_b,
                       dR2_P1_given_family=r_f1, dR2_P2_given_family=r_f2))
    P("")
    P("  (ii) is a book's phase sensitivity STABLE across INDEPENDENT cadences?  Spearman of")
    P("       per-book spread between cadence pairs (pooled, and within family).")
    piv = tab.pivot_table(index="book", columns="cad", values="spread")
    fmap = tab.drop_duplicates("book").set_index("book").family
    P(f"  {'pair':10s} {'rho pooled':>11s} {'t':>7s} " + " ".join(f"{'rho '+f:>10s}" for f in FAMILIES))
    stab = []
    for i, a in enumerate(MULTI):
        for b in MULTI[i + 1:]:
            r, t, n = spearman(piv[a], piv[b])
            row = dict(pair=f"{a}-{b}", rho=r, t=t, n=n)
            line = f"  {a+'-'+b:10s} {r:11.3f} {t:7.2f} "
            for f in FAMILIES:
                m = fmap.reindex(piv.index) == f
                rf, tf, nf = spearman(piv[a][m], piv[b][m])
                row[f"rho_{f}"] = rf
                line += f"{rf:10.3f} "
            P(line)
            stab.append(row)
    P("")

    # ---------------- T2 prediction
    P("=" * 118)
    P("T2  PREDICTION - Spearman(spread, predictor), pooled and WITHIN family")
    P("    pre-registered signs:  P1 persistence NEGATIVE   |   P2 eligible-name turnover POSITIVE")
    P(f"  {'cad':4s} {'predictor':12s} {'rho pooled':>11s} {'t':>7s} "
      + " ".join(f"{'rho '+f:>10s} {'t':>6s}" for f in FAMILIES) + f" {'sign OK':>8s}")
    pred_rows = []
    for cad in MULTI:
        s = tab[tab.cad == cad]
        for nm, col, want in [("P1 persist", "persistence", -1), ("P2 eligturn", "elig_turn", +1),
                              ("c n_names", "n_names", 0), ("c sel_turn", "sel_turn", 0),
                              ("c level", "lvl", 0)]:
            r, t, n = spearman(s.spread, s[col])
            line = f"  {cad:4s} {nm:12s} {r:11.3f} {t:7.2f} "
            row = dict(cad=cad, predictor=nm, rho_pooled=r, t_pooled=t, n=n)
            wsig = []
            for f in FAMILIES:
                sf = s[s.family == f]
                rf, tf, nf = spearman(sf.spread, sf[col])
                line += f"{rf:10.3f} {tf:6.2f} "
                row[f"rho_{f}"] = rf
                row[f"t_{f}"] = tf
                if np.isfinite(rf):
                    wsig.append(np.sign(rf) == want)
            okmark = "-" if want == 0 else ("yes" if (np.isfinite(r) and np.sign(r) == want) else "NO")
            line += f"{okmark:>8s}"
            row["sign_as_registered"] = okmark
            P(line)
            pred_rows.append(row)
        P("")
    pd.DataFrame(pred_rows).to_csv(OUT / f"{STEM}.predict.csv", index=False)

    # ---------------- T3 screenability
    P("=" * 118)
    P("T3  SCREENABILITY - the only test that could put a clause in PROTOCOL")
    P("    Books are split at the IS-ONLY median of each predictor (IS <= 2016-12-31, no future")
    P("    information).  The pre-registration says the 'predicted-insensitive' half - high IS")
    P("    persistence, or low IS eligible-name turnover - must have the LOWER realised OOS spread.")
    P(f"  {'cad':4s} {'predictor':12s} {'n':>4s} {'spread INSENS':>14s} {'spread SENS':>12s} "
      f"{'ratio':>7s} {'diff t':>8s} {'sign p':>8s} {'verdict':>9s}")
    scr = []
    for cad in MULTI:
        s = tab[tab.cad == cad].dropna(subset=["persistence_IS", "elig_turn_IS", "spread"])
        for nm, col, hi_is_insens in [("P1 persist", "persistence_IS", True),
                                      ("P2 eligturn", "elig_turn_IS", False)]:
            med = s[col].median()
            insens = s[s[col] >= med] if hi_is_insens else s[s[col] <= med]
            sens = s[s[col] < med] if hi_is_insens else s[s[col] > med]
            a, b = insens.spread.values, sens.spread.values
            if len(a) < 5 or len(b) < 5:
                continue
            # unpaired: Welch t on the difference of means
            se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            tt = (b.mean() - a.mean()) / se if se > 0 else np.nan
            # rank-based sign check: fraction of insens books below the pooled median spread
            pm = s.spread.median()
            p, w, l = sign_p(np.where(a < pm, 1.0, -1.0))
            v = "HOLDS" if (a.mean() < b.mean() and abs(tt) > 2) else ("weak" if a.mean() < b.mean() else "FAILS")
            P(f"  {cad:4s} {nm:12s} {len(s):4d} {a.mean():14.4f} {b.mean():12.4f} "
              f"{a.mean()/b.mean() if b.mean() else np.nan:7.3f} {tt:8.2f} {p:8.4f} {v:>9s}")
            scr.append(dict(cad=cad, predictor=nm, n=len(s), spread_insens=a.mean(),
                            spread_sens=b.mean(), ratio=a.mean() / b.mean() if b.mean() else np.nan,
                            t=tt, sign_p=p, verdict=v))
        P("")
    pd.DataFrame(scr).to_csv(OUT / f"{STEM}.screen.csv", index=False)

    # ---------------- T5 (POST-HOC, labelled): is there any book-level variation to predict?
    P("=" * 118)
    P("T5  POST-HOC AND LABELLED AS SUCH - it was NOT pre-registered.  T1-T3 came back null, so")
    P("    this asks the prior question they assume: is there BOOK-LEVEL variation in phase at all?")
    P("    For each (family, cadence): the share of books whose best phase is the FAMILY's best")
    P("    phase (chance = 1/k), the same for the worst, and the COMMON SHARE - the variance of")
    P("    the cross-book MEAN phase profile divided by the mean within-book variance across")
    P("    phases.  A common share near 1 means every book in the panel is hit by the SAME phase")
    P("    on the SAME dates, i.e. phase is a panel-DATE effect with no book-level residual for")
    P("    any book property to predict.")
    P(f"  {'cad':4s} {'family':7s} {'k':>3s} {'argmax agree':>13s} {'argmin agree':>13s} {'chance 1/k':>11s} "
      f"{'common share':>13s}")
    com = []
    for cad in MULTI:
        for fam in FAMILIES:
            s = ph[(ph.cad == cad) & (ph.family == fam)]
            piv = s.pivot_table(index="book", columns="phase", values="OOS_Sharpe")
            k = piv.shape[1]
            g = piv.mean()
            bp, wp = int(g.idxmax()), int(g.idxmin())
            agb = float((piv.idxmax(axis=1) == bp).mean())
            agw = float((piv.idxmin(axis=1) == wp).mean())
            cm = piv.sub(piv.mean(axis=1), axis=0)
            share = float(cm.mean().var(ddof=0) / cm.var(axis=1, ddof=0).mean())
            P(f"  {cad:4s} {fam:7s} {k:3d} {agb:13.2f} {agw:13.2f} {1/k:11.2f} {share:13.3f}")
            com.append(dict(cad=cad, family=fam, k=k, argmax_agree=agb, argmin_agree=agw,
                            chance=1 / k, common_share=share))
        P("")
    pd.DataFrame(com).to_csv(OUT / f"{STEM}.common.csv", index=False)

    # ---------------- rule 8 walk-forward
    P("=" * 118)
    P("PROTOCOL RULE 8 WALK-FORWARD - four arms, parameters on IS only, OOS read once")
    P("  CONST-W0  weekly at phase 0 (RULES v1's cadence)")
    P("  REC       cadence = IS-Sharpe argmax at phase 0 (what the record does)")
    P("  SCREENED  REC's cadence only where IS persistence at that cadence >= the IS median,")
    P("            else fall back to W  (what idea 221 implies IF the property is screenable)")
    P("  PHASE-AVG REC's cadence traded as the equal-weight blend of all its phases")
    lad_p = lad.pivot_table(index="book", columns="point", values="IS_Sharpe")
    persist_is = epi.pivot_table(index="book", columns="cad", values="persistence_IS")
    # IS median of persistence, per cadence, computed on IS only -> the screen threshold
    thr = persist_is.median()
    nph_of = dict(PHASE_SPECS)
    wf_rows = []
    for bk in books:
        st = START[bk.parent]
        w = bk.weights()
        rec = lad_p.loc[bk.name].idxmax()
        pers = persist_is.loc[bk.name, rec] if rec in persist_is.columns else np.nan
        passes = bool(np.isfinite(pers) and pers >= thr.get(rec, np.inf))
        scr_cad = rec if passes else CONST_PT

        def oos_of(cad, phase=0):
            r = phase_ret.get((bk.name, cad, phase))
            if r is None:
                r = fast_backtest(bk.px, w, COST_BPS, cad, phase)["returns"].loc[st:]
            return r.loc[OOS_START:]

        arms = {"CONST-W0": oos_of(CONST_PT, 0), "REC": oos_of(rec, 0), "SCREENED": oos_of(scr_cad, 0)}
        k = nph_of.get(rec, 1)
        blend = sum(oos_of(rec, p) for p in range(k)) / k
        arms["PHASE-AVG"] = blend
        for nm, r in arms.items():
            m = metrics(r)
            wf_rows.append(dict(book=bk.name, family=family_of(bk.name), parent=bk.parent, arm=nm,
                                rec_cad=rec, screened_cad=scr_cad, screen_passes=passes,
                                IS_persistence=pers,
                                OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"]))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    npass = int(wf[wf.arm == "SCREENED"].screen_passes.sum())
    P(f"  screen admits {npass}/{len(books)} books at their own REC cadence "
      f"(the rest fall back to W); REC cadence counts: "
      + ", ".join(f"{k}:{v}" for k, v in wf[wf.arm == 'REC'].rec_cad.value_counts().items()))
    P("")
    P(f"  {'family':7s} {'arm':10s} {'n':>4s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} "
      f"{'d vs CONST-W0':>14s} {'t (paired)':>11s}")
    base_arm = wf[wf.arm == "CONST-W0"].set_index("book").OOS_Sharpe
    for fam in ["ALL"] + FAMILIES:
        for nm in ["CONST-W0", "REC", "SCREENED", "PHASE-AVG"]:
            s = wf[wf.arm == nm] if fam == "ALL" else wf[(wf.arm == nm) & (wf.family == fam)]
            d = (s.set_index("book").OOS_Sharpe - base_arm.reindex(s.book).values).values
            P(f"  {fam:7s} {nm:10s} {len(s):4d} {s.OOS_CAGR.mean():9.2%} {s.OOS_Sharpe.mean():11.4f} "
              f"{s.OOS_MaxDD.mean():10.2%} {np.nanmean(d):+14.4f} {tstat(d):11.2f}")
        P("")
    P("  benchmarks over the SAME OOS window (per parent panel):")
    for k in SPY:
        ms, mb = metrics(SPY[k].loc[OOS_START:]), metrics(BASE[k].loc[OOS_START:])
        P(f"    {k:6s} SPY      CAGR {ms['CAGR']:6.2%}  Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:7.2%}")
        P(f"    {k:6s} RULES v1 CAGR {mb['CAGR']:6.2%}  Sharpe {mb['Sharpe']:.4f}  MaxDD {mb['MaxDD']:7.2%}")
    P("")

    # ---------------- KEEP paths
    P("=" * 118)
    P("BOTH KEEP PATHS on all phase rows (PROTOCOL rule 4)")
    ph["pass4a"] = ph.fail4a == "-"
    ph["pass4b"] = ph.fail4b == "-"
    ph[["book", "family", "cad", "phase", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
        "OOS_Sharpe", "turnover", "fail4a", "fail4b"]].to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  rows={len(ph)}   4a passes={int(ph.pass4a.sum())}   4b passes={int(ph.pass4b.sum())}")
    for fam in FAMILIES:
        s = ph[ph.family == fam]
        P(f"    {fam:6s} n={len(s):5d}  4a={int(s.pass4a.sum()):4d}  4b={int(s.pass4b.sum()):4d}")
    if int(ph.pass4b.sum()):
        g = ph[ph.pass4b].groupby(["book", "cad"]).size().rename("phases_passing").reset_index()
        tot = ph.groupby(["book", "cad"]).size().rename("phases").reset_index()
        g = g.merge(tot, on=["book", "cad"])
        P(f"  4b passes concentrate in {g.book.nunique()} books; "
          f"{int((g.phases_passing == g.phases).sum())}/{len(g)} (book,cadence) cells pass at ALL of")
        P("  their own phases - the rest are phase-conditional 4b passes and are NOT candidates.")
        P(g.sort_values("phases_passing", ascending=False).head(20).to_string(index=False))
    P("")

    # ---------------- verdict
    P("=" * 118)
    P("SUMMARY OF THE FOUR TESTS")
    t1d = pd.DataFrame(t1)
    if len(t1d):
        P(f"  T1(i)  mean R2: family alone {t1d.R2_family.mean():.3f} | predictors alone "
          f"{t1d.R2_pred.mean():.3f} | both {t1d.R2_both.mean():.3f} | "
          f"dR2 of P1 given family {t1d.dR2_P1_given_family.mean():+.3f}, P2 {t1d.dR2_P2_given_family.mean():+.3f}")
    sd = pd.DataFrame(stab)
    if len(sd):
        P(f"  T1(ii) cross-cadence rank stability of per-book spread: median pooled rho "
          f"{sd.rho.median():.3f} over {len(sd)} cadence pairs "
          f"(within-family medians: " + ", ".join(f"{f} {sd['rho_'+f].median():.3f}" for f in FAMILIES) + ")")
    pdd = pd.DataFrame(pred_rows)
    for nm in ["P1 persist", "P2 eligturn"]:
        s = pdd[pdd.predictor == nm]
        P(f"  T2     {nm:12s} pooled rho median {s.rho_pooled.median():+.3f}; "
          f"registered sign holds in {int((s.sign_as_registered=='yes').sum())}/{len(s)} cadences; "
          f"within-family medians " + ", ".join(f"{f} {s['rho_'+f].median():+.3f}" for f in FAMILIES))
    sc = pd.DataFrame(scr)
    for nm in ["P1 persist", "P2 eligturn"]:
        s = sc[sc.predictor == nm]
        if len(s):
            P(f"  T3     {nm:12s} IS-split ratio (insens/sens) median {s.ratio.median():.3f}; "
              f"HOLDS in {int((s.verdict=='HOLDS').sum())}/{len(s)} cadences, "
              f"FAILS in {int((s.verdict=='FAILS').sum())}")
    P(f"  T4     Q control spread max {q.spread.abs().max():.3e}")
    cd = pd.DataFrame(com)
    P(f"  T5(post-hoc) common share median {cd.common_share.median():.3f} "
      f"(U56 {cd[cd.family=='U56'].common_share.median():.3f}, "
      f"ETF {cd[cd.family=='ETF'].common_share.median():.3f}, "
      f"SMALL {cd[cd.family=='SMALL'].common_share.median():.3f}); "
      f"argmax agreement median {cd.argmax_agree.median():.2f} vs chance {cd.chance.median():.2f}")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    flush()


if __name__ == "__main__":
    main()
