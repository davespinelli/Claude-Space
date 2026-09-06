#!/usr/bin/env python3
"""QUEUE idea 222 - a-phase-averaged-cadence-as-the-honest-estimator   (lane C, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 222)
    "idea 187 shows a single-phase ladder point is an alignment draw, not a cadence estimate.
     Build the phase-averaged book (equal-weight blend of all k phases at cadence k, or the mean
     of their returns) and re-run idea 175's ladder on it: does a phase-averaged ladder have the
     humped shape idea 175 claimed, and does the M-vs-6W split of idea 188 survive averaging?
     This is the estimator every future cadence claim should use.  Max 2 params."

WHAT IS AT STAKE.
    Every cadence number this project has published - idea 175's ladder, idea 107's monthly
    constant, idea 188's SMALL-wants-M / large-caps-want-6W split, idea 187's own 13-point
    re-grid - was measured at PHASE 0: the block grid anchored on the panel's first bar.  Idea
    187 then showed that holding cadence FIXED and sweeping the phase moves mean OOS Sharpe by
    0.1518 ALL / 0.2618 SMALL / 0.3957 U56 / 0.3862 ETF at 6W, which is 2.1-2.4x the entire
    6W-minus-W cadence effect idea 175 published, and that the ladder's 6W is phase 0 of 6 and
    happens to rank 1/6 on three of four families.  A phase is fixed by an arbitrary sample-start
    date; it is not a tradable choice.  So every phase-0 ladder point is one draw from a
    distribution whose spread is LARGER than the effect being measured, and the whole cadence
    record may be an alignment artefact rather than a signal-decay finding.

    The fix the queue names is to stop reading one draw.  At cadence k there are exactly k
    phases; average over all of them and the alignment draw integrates out.  What survives is
    whatever cadence LENGTH actually buys.  This run builds that estimator, re-runs the ladder
    on it, and asks whether the two published shape claims survive.

    A NULL here (the averaged ladder is smooth and FLAT, no hump, no family split) is the useful
    result: it says the cadence dial has no writable content and idea 107's monthly constant is
    a coin that landed heads.

THE FOUR ESTIMATORS.  Same book, same corpus, same costs; the ONLY thing that changes is how the
k phases of a cadence-k point are collapsed into one number.  All four reported everywhere.
    PH0        phase 0 only.  THE INCUMBENT - what ideas 175/187/188 and the whole record report.
    MEANPH     the mean ACROSS PHASES of each phase's own metric (mean Sharpe, mean CAGR, ...).
               The honest expectation of drawing a phase at random.  No diversification bonus:
               at a k=1 point it is identically PH0.  THIS is the de-confounded shape estimator.
    BLEND-DR   the mean of the k phase RETURN SERIES (the queue's "mean of their returns"), i.e.
               k equal sleeves rebalanced back to 1/k daily.  Implementable as overlapping
               tranches; exactly one sleeve trades per block, so its annual turnover equals a
               single phase's and its 10 bps are already inside the phase returns.  CAVEAT,
               declared: the daily re-levelling BETWEEN sleeves is not itself costed.
    BLEND-BH   the equal-weight blend of the k phase EQUITY CURVES, sleeves left to drift (the
               queue's "equal-weight blend").  No inter-sleeve trading at all, so nothing is
               un-costed.  BLEND-DR and BLEND-BH bracket the implementable truth.

    MEANPH and BLEND answer DIFFERENT questions and this run keeps them apart on purpose.
    Blending k sleeves diversifies away phase-idiosyncratic noise, so BLEND carries a variance
    bonus that GROWS WITH k and has nothing to do with cadence; at k=1 (D, W, M, Q) it is zero by
    construction.  Reading a BLEND ladder as a cadence curve would repeat idea 187's mistake with
    the sign reversed.  MEANPH is the shape estimator; BLEND is the implementability estimator.

THE LADDER - idea 187's 13 points (a superset of idea 175's 7), ordered by cadence length:
    D 2D W 2W M 6W 7W 8W 2M 10W Q 16W 2Q,  with 1 2 1 2 1 6 7 8 2 10 1 16 2 phases respectively
    = 59 phase-runs per book x 115 books = 6785 backtests.  Every point reported, nothing picked.
    All other dials pinned at idea 175's incumbents: GROSS 0.75, N 20, BAND 0.00, SLEEVE 0.00,
    COST 10 bps, t+1.  D/W/M/Q are k=1 points and have exactly one phase - they are the negative
    control for the whole construction (control [e]).

TUNED PARAMETERS - exactly two, per PROTOCOL rule 4, identical to ideas 175 and 187.
    1. the SELECTOR, 2 values, both reported, neither preferred:
         SEL-SHARPE  argmax over the ladder of IS Sharpe               (rule 8's S1)
         SEL-4B      argmax over the ladder of the IS 4b relative min-margin (idea 166)
    2. the LADDER POINT, swept exhaustively (13 points), ALL reported.
    The ESTIMATOR is the axis under test (all four reported, none preferred), not a tuned
    parameter; PANEL and BOOK are corpus axes.  CONST-W / CONST-M / CONST-6W / CONST-2M /
    RANDOM (seeded) / ORACLE are controls.

CORPUS - 115 books, byte-identical to ideas 175 and 187 (same seeds, same draws, same panels).
    3 fixed panels : SMALL439, U56, ETF36 + 48 SMALL / 32 U56 / 32 ETF sub-panels.
    Re-using the corpus is what makes controls [c] and [d] exact reproductions rather than re-runs.

WALK-FORWARD (PROTOCOL rule 8) - run for every estimator.
    Every selector reads the <= 2016-12-31 window only; 2017-01-01.. is read once.
    .walkforward.csv reports mean OOS CAGR/Sharpe/MaxDD per (estimator, arm, family) against
    RULES v1 on the parent panel and against SPY.

BOTH KEEP PATHS evaluated on all 13 x 115 x 4 = 5980 estimator-rows, written to .keep.csv.
    4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND on the OOS window, MaxDD <= 0.60 x |SPY MaxDD|,
        CAGR >= 0.70 x SPY CAGR.

REPRODUCTION, asserted before any new number is read
    [a] cad_mask reproduces engine.rebalance_mask exactly at D, W, M, Q; reb/yr monotone.
    [b] fast_backtest reproduces engine.backtest to < 1e-12 on returns and turnover.
    [c] the PH0 ladder equals idea 175's committed .ladder.csv on all 805 shared rows to < 1e-9,
        0 verdict mismatches.  Without [c] the averaged ladder is not comparable to the record.
    [d] the phase sweep equals idea 187's committed .phase.csv (6W/2M/8W/Q x 115 books = 2300
        rows) to < 1e-9.  This is the control that says my phase machinery IS idea 187's.
    [e] DEGENERATE-PHASE IDENTITY: at the four k=1 points (D, W, M, Q) all four estimators must
        agree to 0.0 exactly.  Zero phase freedom must produce zero averaging effect.
    Any failure stops the run before a conclusion is drawn.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a]-[e] all hold.
    P2  AVERAGING REMOVES THE JAGGEDNESS.  Idea 187's phase-0 ladder has 6W 0.780 -> 7W 0.606 ->
        8W 0.651 -> 2M 0.826 -> 10W 0.693 (neighbours 1.2 reb/yr apart differing by 0.17).  Under
        MEANPH I expect the number of interior turning points in the pooled mean-OOS-Sharpe curve
        to FALL by at least half and total variation / range to drop toward ~2 (a single hump).
    P3  BUT THE SMOOTHED CURVE IS FLAT, NOT HUMPED.  I expect the MEANPH max-minus-min over
        W..2Q to come in BELOW idea 187's 6W phase spread (0.1518 pooled), i.e. once the draw is
        integrated out there is less cadence signal than there was phase noise, and no cadence
        constant is identified.  This is the pre-registered answer to the queue's first question.
    P4  Q STOPS BEING THE WORST POINT.  Q is k=1, so PH0 gave it its only phase while giving its
        neighbours their luckiest-available one.  Its rank on the MEANPH ladder should improve.
    P5  THE M-vs-6W SPLIT DOES NOT SURVIVE ON THE LARGE CAPS.  Idea 188's U56 -0.1106 and ETF
        -0.0807 (6W better than M) were measured at 6W phase 0, which idea 187 ranks 1/6 on both
        families.  Under MEANPH I expect U56 and ETF M-minus-6W to move toward zero or flip
        positive, while SMALL's +0.1107 (M better) survives as the only sign that was not bought
        with an alignment draw.
    P6  BLEND IS NOT A CADENCE LADDER.  BLEND-DR/BH will beat MEANPH at every k>1 point by a
        bonus that rises with k, and the BLEND argmax will sit at or adjacent to the largest-k
        point (16W).  Naming that confound is part of the deliverable; a "16W is best" reading
        would be an artefact of sleeve count, not cadence.
    P7  RULE 8: the do-nothing streak continues under every estimator (SEL-SHARPE loses to the
        best constant), but the shortfall SHRINKS under MEANPH relative to PH0, because less of
        the IS ladder the selector reads is phase noise.
    P8  NO NEW 4b KEEP on the three fixed panels beyond a re-cadencing of an existing book
        (idea 144).  4b passes stay concentrated in the U56 family (idea 136, SMALL 0).

CAVEATS carried, not buried
    * SURVIVORSHIP.  SMALL439/U56/ETF36 are current-constituent lists (data/SMALL_PANEL_README.md,
      idea 54).  Every ladder point and every phase inherits it equally, so the PAIRED comparisons
      are unaffected; no LEVEL here is an attainable return.
    * Idea 38: data/prices.csv is calendar-day indexed from 2014-09-17, so D/2D rebalance on some
      non-trading days on U56/ETF36 and week-blocks land differently before and after that date.
    * BLEND-DR's inter-sleeve daily re-levelling is NOT costed (BLEND-BH is the costed bound).
    * Idea 144: a re-cadenced book is the SAME book.  A verdict flip along this ladder is not a
      new signal, and neither is one produced by re-phasing it.
    * Idea 126: t+1 execution only, 10 bps only.  Idea 188 established the cadence split is not a
      cost effect, so no cost ladder is re-run here.
    * A selector fitted on IS is one more thing fitted on IS.  The OOS window is read once.

Deterministic, standalone.  Writes .console.txt, .phaserows.csv, .ladder.csv, .shape.csv,
.split.csv, .keep.csv, .walkforward.csv, .result.md.
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

STEM = "2026-09-06_a-phase-averaged-cadence-as-the-honest-estimator_C"
LADDER_PARENT = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"   # idea 175
PHASE_PARENT = "2026-09-06_is-6W-a-grid-edge-or-a-real-optimum_B"               # idea 187
OUT = ROOT / "research" / "backtests"

COST_BPS = 10
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
EPS = 0.05

OLD_LADDER = ["D", "2D", "W", "2W", "M", "6W", "Q"]                             # idea 175's 7
LADDER = ["D", "2D", "W", "2W", "M", "6W", "7W", "8W", "2M", "10W", "Q", "16W", "2Q"]
NPHASE = {"D": 1, "2D": 2, "W": 1, "2W": 2, "M": 1, "6W": 6, "7W": 7, "8W": 8,
          "2M": 2, "10W": 10, "Q": 1, "16W": 16, "2Q": 2}
K1 = [p for p in LADDER if NPHASE[p] == 1]                                      # D W M Q
ESTS = ["PH0", "MEANPH", "BLEND-DR", "BLEND-BH"]
CONSTS = ["W", "M", "6W", "2M"]
ARMS = ["CONST-W", "CONST-M", "CONST-6W", "CONST-2M", "SEL-SHARPE", "SEL-4B", "RANDOM", "ORACLE"]

INC_GROSS, INC_N = 0.75, 20
FAMILIES = ["SMALL", "U56", "ETF"]
DRAWS = {"SMALL": (175_500, [20, 40, 80]), "U56": (175_600, [20, 40]), "ETF": (175_700, [12, 24])}
N_DRAWS = 16
RAND_SEED = 222_001

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def flush():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


# ---------------------------------------------------------------- cadence masks (idea 187 verbatim)
_WEEK_K = {"W": 1, "2W": 2, "6W": 6, "7W": 7, "8W": 8, "10W": 10, "16W": 16}
_PER_K = {"M": ("M", 1), "2M": ("M", 2), "Q": ("Q", 1), "2Q": ("Q", 2)}


def cad_mask(idx, cad, phase=0):
    """True on the last bar of each cadence block.  Copied unchanged from idea 187 so that the
    phase machinery under test IS the one that produced the phase spread (control [d])."""
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


def fast_backtest(prices, weights, cost_bps=COST_BPS, cad="W", phase=0):
    """Vectorised equivalent of engine.backtest (control [b]).  Copied from idea 175/187."""
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


# ---------------------------------------------------------------- book construction (idea 175/187)
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
                books.append(Book(f"{fam}k{k}d{d:02d}", keep(pxp, sub), set(sub),
                                  "SMALL" if fam == "SMALL" else "U56"))
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


NUMCOLS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover", "IS_Sharpe", "IS_CAGR",
           "IS_MaxDD", "IS_margin", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]


def stats_of(r, turn_yr, spy, spy_is, spy_oos):
    """Full scalar stat dict for one return series."""
    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
    mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
    mg_is, wb_is = rel_margin(r_is, spy_is)
    mg_oos, wb_oos = rel_margin(r_oos, spy_oos)
    h1, h2 = halves(r)
    return dict(CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                turnover=turn_yr, IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                IS_MaxDD=mi["MaxDD"], IS_margin=mg_is, IS_worstbar=wb_is,
                OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                OOS_margin=mg_oos, OOS_worstbar=wb_oos)


def fail4a_s(s, bs):
    f = []
    if not s["H1"] > bs["H1"]: f.append("H1")
    if not s["H2"] > bs["H2"]: f.append("H2")
    if not s["MaxDD"] >= bs["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail4b_s(s, ss):
    f = []
    if not s["H1"] > ss["H1"]: f.append("H1")
    if not s["H2"] > ss["H2"]: f.append("H2")
    if not s["OOS_Sharpe"] > ss["OOS_Sharpe"]: f.append("OOS")
    if not abs(s["MaxDD"]) <= DELTA * abs(ss["MaxDD"]): f.append("DD")
    if not s["CAGR"] >= PHI * ss["CAGR"]: f.append("CAGR")
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
    return min(1.0, 2 * sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n), w, n - w


def spearman(a, b):
    """Rank correlation without scipy (not installed in the sandbox)."""
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


def shape_stats(y):
    """Jaggedness of a ladder curve: interior turning points and total-variation / range."""
    y = np.asarray(y, float)
    d = np.diff(y)
    sg = np.sign(d)
    turns = int(sum(1 for i in range(len(sg) - 1) if sg[i] != 0 and sg[i + 1] != 0 and sg[i] != sg[i + 1]))
    rng = float(y.max() - y.min())
    tv = float(np.abs(d).sum())
    return turns, rng, tv, (tv / rng if rng > 0 else np.nan)


# ---------------------------------------------------------------- reproduction controls
def check_a(book):
    P("  [a] cad_mask vs engine.rebalance_mask at the four engine-supported points, and")
    P("      rebalances/yr for all 13 (must be monotone decreasing in ladder order):")
    ok, yr = True, {}
    for cd in LADDER:
        b = cad_mask(book.px.index, cd)
        yr[cd] = b.sum() / (len(b) / 252)
        if cd in ("D", "W", "M", "Q"):
            same = bool((rebalance_mask(book.px.index, cd).values == b.values).all())
            P(f"      {cd:3s} phases={NPHASE[cd]:2d}  identical={same}   rebalances/yr={yr[cd]:6.1f}")
            ok &= same
        else:
            P(f"      {cd:3s} phases={NPHASE[cd]:2d}  (block point)     rebalances/yr={yr[cd]:6.1f}")
    mono = all(yr[LADDER[i]] >= yr[LADDER[i + 1]] - 1e-9 for i in range(len(LADDER) - 1))
    P(f"      monotone in ladder order={mono}   -> {'PASS' if (ok and mono) else 'FAIL'}")
    return ok and mono


def check_b(book):
    P("  [b] fast_backtest vs engine.backtest (products/backtester/engine.py), same book:")
    w, ok = book.weights(), True
    for cd in ["D", "W", "M", "Q"]:
        a = backtest(book.px, w, cost_bps=COST_BPS, freq=cd)
        b = fast_backtest(book.px, w, cost_bps=COST_BPS, cad=cd)
        dr = float((a["returns"] - b["returns"]).abs().max())
        dt = float((a["turnover"] - b["turnover"]).abs().max())
        P(f"      {book.name:9s} cad={cd:2s}  max|dret|={dr:.3e}  max|dturn|={dt:.3e}")
        ok &= dr < 1e-12 and dt < 1e-10
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_c(ph0):
    P(f"  [c] PH0 ladder vs idea 175's committed {LADDER_PARENT}.ladder.csv")
    src = OUT / f"{LADDER_PARENT}.ladder.csv"
    if not src.exists():
        P(f"      *** not found: {src} -> FAIL")
        return False
    old = pd.read_csv(src)
    new = ph0[ph0.point.isin(OLD_LADDER)]
    m = old.merge(new, on=["book", "point"], suffixes=("_o", "_n"), how="inner")
    worst, wc = 0.0, ""
    for c in NUMCOLS:
        d = float((m[c + "_o"] - m[c + "_n"]).abs().max())
        if d > worst:
            worst, wc = d, c
    vm = int((m["fail4a_o"] != m["fail4a_n"]).sum() + (m["fail4b_o"] != m["fail4b_n"]).sum())
    bm = int((m["IS_worstbar_o"] != m["IS_worstbar_n"]).sum()
             + (m["OOS_worstbar_o"] != m["OOS_worstbar_n"]).sum())
    ok = (len(m) == len(old) == len(new)) and worst < 1e-9 and vm == 0 and bm == 0
    P(f"      rows: parent={len(old)}  this-run shared={len(new)}  matched={len(m)}")
    P(f"      max|d| over {len(NUMCOLS)} numeric columns = {worst:.3e} (worst: {wc});  "
      f"verdict mismatches={vm};  worst-bar mismatches={bm}")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_d(phr):
    """Idea 187 swept Q over 4 nominal phases even though Q is k=1 (that was ITS negative
    control: the spread came back exactly 0.0000).  So its file holds 20 rows/book (6+2+8+4)
    where this run holds 17 (6+2+8+1).  The control therefore has two halves: the 17 genuine
    phases must match to < 1e-9, AND the parent's own 3 surplus Q rows must be identical to its
    Q phase 0 - which is what makes them surplus.  Both halves must account for all 2300 rows."""
    P(f"  [d] phase sweep vs idea 187's committed {PHASE_PARENT}.phase.csv (6W/2M/8W/Q)")
    src = OUT / f"{PHASE_PARENT}.phase.csv"
    if not src.exists():
        P(f"      *** not found: {src} -> FAIL")
        return False
    old = pd.read_csv(src)
    new = phr[phr.point.isin(["6W", "2M", "8W", "Q"])].rename(columns={"point": "cad"})
    m = old.merge(new, on=["book", "cad", "phase"], suffixes=("_o", "_n"), how="inner")
    cols = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "IS_Sharpe"]
    worst, wc = 0.0, ""
    for c in cols:
        d = float((m[c + "_o"] - m[c + "_n"]).abs().max())
        if d > worst:
            worst, wc = d, c
    q = old[old.cad == "Q"]
    q0 = q[q.phase == 0].set_index("book")
    qs = q[q.phase > 0]
    qworst = max(float((qs.set_index("book")[c] - q0[c]).abs().max()) for c in cols)
    ok = (len(m) == len(new) == 115 * 17) and worst < 1e-9 and len(qs) == 345 and qworst == 0.0 \
        and len(m) + len(qs) == len(old)
    P(f"      rows: parent={len(old)}  genuine-phase rows matched={len(m)} (expected {115*17})   "
      f"max|d| = {worst:.3e} (worst: {wc})")
    P(f"      parent's {len(qs)} surplus Q rows (phases 1-3 of a k=1 point) vs its own Q phase 0: "
      f"max|d| = {qworst:.3e}  -> degenerate as idea 187 stated")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_e(est):
    """PH0, MEANPH and BLEND-DR must be BITWISE identical at a k=1 point (mean of one thing).
    BLEND-BH is not: it round-trips the series through a cumulative product and back, so it is
    algebraically identical and numerically equal only to float precision.  Reported separately
    rather than hidden behind one tolerance."""
    P("  [e] DEGENERATE-PHASE IDENTITY: at k=1 points (D, W, M, Q) all estimators must agree with")
    P("      PH0 (zero phase freedom -> zero averaging effect).  Negative control for the whole")
    P("      construction.  MEANPH/BLEND-DR bitwise (0.0); BLEND-BH to float precision (<1e-12),")
    P("      because it reconstructs returns from a cumulated equity curve.")
    sub = est[est.point.isin(K1)]
    piv = sub.pivot_table(index=["book", "point"], columns="est", values=NUMCOLS)
    ok = True
    for e in ESTS[1:]:
        worst, wc = 0.0, ""
        for c in NUMCOLS:
            d = float((piv[(c, e)] - piv[(c, "PH0")]).abs().max())
            if d > worst:
                worst, wc = d, c
        tol = 0.0 if e != "BLEND-BH" else 1e-12
        good = worst <= tol
        ok &= good
        P(f"      {e:9s} max|d vs PH0| = {worst:.3e} (worst column: {wc})   tol={tol:.0e}  "
          f"{'ok' if good else 'FAIL'}")
    P(f"      {len(sub)} rows over {len(K1)} k=1 points x 4 estimators -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 222 - a-phase-averaged-cadence-as-the-honest-estimator   (lane C, {pd.Timestamp.today().date()})")
    P("=" * 118)
    P("Idea 187 measured a 6W PHASE spread of 0.1518 ALL / 0.3957 U56 / 0.3862 ETF against a")
    P("published 6W-minus-W CADENCE effect of 0.0999 / 0.1640 / 0.1600, i.e. the alignment draw is")
    P("bigger than the effect.  This run collapses the draw: at cadence k it runs ALL k phases and")
    P("reports the ladder under four estimators (PH0, MEANPH, BLEND-DR, BLEND-BH).")
    P(f"13 points x 115 books x {sum(NPHASE.values())} phases-per-book = "
      f"{sum(NPHASE.values())} runs/book, {COST_BPS} bps, t+1, IS <= {IS_END}, OOS >= {OOS_START}.")
    P("Two tuned params: SELECTOR (2, both reported) x LADDER POINT (13, all reported).")
    P("")

    books, panels = build_corpus()
    P(f"CORPUS: {len(books)} books (3 fixed panels + {len(books)-3} sub-panels), seeds of ideas 175/187")
    for b in books[:3]:
        P(f"   {b.name:11s} {b.px.shape[0]}d x {b.px.shape[1]}c  tradable={len(b.tradable):3d}  "
          f"{b.px.index[0].date()}..{b.px.index[-1].date()}")
    P("")

    P("REPRODUCTION CONTROLS [a] and [b] (asserted before any new number is read)")
    if not (check_a(books[1]) and check_b(books[1])):
        P("\n*** REPRODUCTION FAILED - stopping. ***")
        flush()
        return
    P("")

    START, SPY, BASE, SPYS = {}, {}, {}, {}
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
        P(f"  benchmark {k:6s} SPY       CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.4f} MaxDD {m['MaxDD']:7.2%} "
          f"halves {h1:.3f}/{h2:.3f}  OOS {mo['CAGR']:6.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:7.2%}")
        P(f"  {'':10s} {k:6s} RULES v1  CAGR {mb['CAGR']:6.2%} Sharpe {mb['Sharpe']:.4f} MaxDD {mb['MaxDD']:7.2%} "
          f"  OOS {mbo['CAGR']:6.2%}/{mbo['Sharpe']:.4f}/{mbo['MaxDD']:7.2%}")
    P("")

    # ------------------------------------------------ the phase sweep + the four estimators
    P(f"RUNNING {sum(NPHASE.values())} phase-runs per book x {len(books)} books = "
      f"{sum(NPHASE.values())*len(books)} backtests ...")
    ph_rows, est_rows = [], []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        idx = bk.px.loc[st:].index
        spy = SPY[bk.parent].reindex(idx).fillna(0.0)
        base = BASE[bk.parent].reindex(idx).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        sstat = stats_of(spy, np.nan, spy, spy_is, spy_oos)
        bstat = stats_of(base, np.nan, spy, spy_is, spy_oos)
        w = bk.weights()
        for pt in LADDER:
            series, pstats = [], []
            for ph in range(NPHASE[pt]):
                res = fast_backtest(bk.px, w, COST_BPS, pt, ph)
                r = res["returns"].loc[st:]
                s = stats_of(r, res["turnover"].loc[st:].sum() / metrics(r)["Years"],
                             spy, spy_is, spy_oos)
                series.append(r)
                pstats.append(s)
                ph_rows.append(dict(book=bk.name, family=family_of(bk.name), point=pt, phase=ph,
                                    OOS_Sharpe=s["OOS_Sharpe"], OOS_CAGR=s["OOS_CAGR"],
                                    OOS_MaxDD=s["OOS_MaxDD"], IS_Sharpe=s["IS_Sharpe"],
                                    Sharpe=s["Sharpe"], CAGR=s["CAGR"], MaxDD=s["MaxDD"],
                                    turnover=s["turnover"]))
            # PH0
            out = {"PH0": dict(pstats[0])}
            # MEANPH: elementwise mean of the phase metrics (no diversification bonus)
            out["MEANPH"] = {c: float(np.mean([p[c] for p in pstats])) for c in NUMCOLS}
            out["MEANPH"]["IS_worstbar"] = pstats[0]["IS_worstbar"]
            out["MEANPH"]["OOS_worstbar"] = pstats[0]["OOS_worstbar"]
            # BLEND-DR: mean of the phase return series (daily-rebalanced equal sleeves)
            rdr = sum(series) / len(series)
            tdr = float(np.mean([p["turnover"] for p in pstats]))
            out["BLEND-DR"] = stats_of(rdr, tdr, spy, spy_is, spy_oos)
            # BLEND-BH: equal-weight blend of the phase equity curves, sleeves left to drift
            eq = sum((1.0 + r).cumprod() for r in series) / len(series)
            rbh = eq / eq.shift(1) - 1.0
            rbh.iloc[0] = eq.iloc[0] - 1.0
            out["BLEND-BH"] = stats_of(rbh, tdr, spy, spy_is, spy_oos)
            for e in ESTS:
                s = out[e]
                est_rows.append(dict(book=bk.name, family=family_of(bk.name), parent=bk.parent,
                                     point=pt, k=NPHASE[pt], est=e,
                                     **{c: s[c] for c in NUMCOLS},
                                     IS_worstbar=s["IS_worstbar"], OOS_worstbar=s["OOS_worstbar"],
                                     fail4a=fail4a_s(s, bstat), fail4b=fail4b_s(s, sstat)))
        if (bi + 1) % 25 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    phr = pd.DataFrame(ph_rows)
    est = pd.DataFrame(est_rows)
    phr.to_csv(OUT / f"{STEM}.phaserows.csv", index=False)
    est.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    P(f"   {len(phr)} phase rows -> .phaserows.csv;  {len(est)} estimator rows -> .ladder.csv "
      f"({time.time()-t0:.0f}s)")
    P("")

    P("REPRODUCTION CONTROLS [c], [d], [e] - the decisive ones")
    okC = check_c(est[est.est == "PH0"])
    okD = check_d(phr)
    okE = check_e(est)
    if not (okC and okD and okE):
        P("\n*** REPRODUCTION FAILED - the averaged ladder is not comparable to the record. Stopping. ***")
        flush()
        return
    P("")

    # ------------------------------------------------ Q1: the shape of the averaged ladder
    P("=" * 118)
    P("Q1  DOES THE PHASE-AVERAGED LADDER HAVE THE HUMPED SHAPE IDEA 175 CLAIMED?")
    P("")
    P("  mean OOS Sharpe over books, by ladder point.  ALL 13 points, all 4 estimators, nothing picked.")
    shape_rows = []
    for fam in ["ALL"] + FAMILIES:
        sub = est if fam == "ALL" else est[est.family == fam]
        P(f"  --- family {fam}  (n={sub.book.nunique()} books)")
        P(f"  {'est':9s} " + " ".join(f"{p:>7s}" for p in LADDER)
          + f" {'argmax':>7s} {'range':>7s} {'turns':>6s} {'TV/rng':>7s}")
        for e in ESTS:
            g = sub[sub.est == e].pivot_table(index="book", columns="point", values="OOS_Sharpe").mean()
            y = [g[p] for p in LADDER]
            turns, rng, tv, ratio = shape_stats(y)
            am = LADDER[int(np.argmax(y))]
            P(f"  {e:9s} " + " ".join(f"{v:7.3f}" for v in y)
              + f" {am:>7s} {rng:7.4f} {turns:6d} {ratio:7.2f}")
            shape_rows.append(dict(family=fam, est=e, argmax=am, rng=rng, turns=turns,
                                   tv=tv, tv_over_rng=ratio,
                                   **{f"OOS_{p}": g[p] for p in LADDER}))
        P("")
    pd.DataFrame(shape_rows).to_csv(OUT / f"{STEM}.shape.csv", index=False)

    P("  IDEA 175's THREE SHAPE CLAIMS, re-tested under each estimator (pooled, ALL books):")
    P(f"  {'est':9s} {'rises D->6W?':>13s} {'6W minus W':>11s} {'Q below 6W?':>12s} "
      f"{'Q rank/13':>10s} {'modal argmax':>13s} {'share':>7s} {'zone 6W-10W':>12s}")
    zone = ["6W", "7W", "8W", "2M", "10W"]
    claim_rows = []
    for e in ESTS:
        sub = est[est.est == e]
        piv = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")
        g = piv.mean()
        up = all(g[LADDER[i]] <= g[LADDER[i + 1]] + 1e-12 for i in range(LADDER.index("6W")))
        qrank = int(pd.Series({p: g[p] for p in LADDER}).rank(ascending=True)[("Q")])
        am = piv[LADDER].idxmax(axis=1)
        mode = am.value_counts()
        zshare = float(am.isin(zone).mean())
        P(f"  {e:9s} {str(up):>13s} {g['6W']-g['W']:11.4f} {str(bool(g['Q'] < g['6W'])):>12s} "
          f"{qrank:10d} {mode.index[0]:>13s} {mode.iloc[0]/len(am):7.1%} {zshare:12.1%}")
        claim_rows.append(dict(est=e, rises_to_6W=up, gap_6W_W=g["6W"] - g["W"],
                               Q_below_6W=bool(g["Q"] < g["6W"]), Q_rank=qrank,
                               modal_argmax=mode.index[0], modal_share=mode.iloc[0] / len(am),
                               zone_share=zshare))
    P("")
    P("  (rises D->6W? is idea 175's monotone-rise claim; 6W-minus-W is its headline gap, published")
    P("   at +0.0999 ALL / +0.1640 U56 / +0.1600 ETF; Q rank 1 = worst point on the ladder.)")
    P("")

    # ------------------------------------------------ the P6 confound: BLEND is not a cadence ladder
    P("  THE BLEND CONFOUND, measured (pre-registered P6).  BLEND minus MEANPH mean OOS Sharpe by k:")
    P(f"  {'point':>6s} {'k':>3s} " + " ".join(f"{e:>10s}" for e in ["BLEND-DR", "BLEND-BH"]))
    for pt in LADDER:
        mp = est[(est.est == "MEANPH") & (est.point == pt)].set_index("book").OOS_Sharpe
        row = []
        for e in ["BLEND-DR", "BLEND-BH"]:
            v = est[(est.est == e) & (est.point == pt)].set_index("book").OOS_Sharpe
            row.append((v - mp).mean())
        P(f"  {pt:>6s} {NPHASE[pt]:3d} " + " ".join(f"{v:10.4f}" for v in row))
    dr_bonus = [(est[(est.est == "BLEND-DR") & (est.point == p)].set_index("book").OOS_Sharpe
                 - est[(est.est == "MEANPH") & (est.point == p)].set_index("book").OOS_Sharpe).mean()
                for p in LADDER]
    ks = [NPHASE[p] for p in LADDER]
    rho = spearman(dr_bonus, ks)
    P(f"  Spearman(sleeve count k, BLEND-DR bonus over MEANPH) = {rho:+.4f}   "
      f"(bonus at k=1 must be 0.0000 by construction)")
    P("")

    # ------------------------------------------------ Q2: idea 188's M-vs-6W split
    P("=" * 118)
    P("Q2  DOES THE M-vs-6W SPLIT OF IDEA 188 SURVIVE AVERAGING?")
    P("")
    P("  idea 188 published, phase 0, paired per book:  SMALL M-6W +0.1107 (t +7.78, M better)")
    P("  U56 -0.1106 (t -13.33, 6W better)  ETF -0.0807 (t -15.28, 6W better).  Same pairing here.")
    P("")
    P(f"  {'est':9s} {'family':7s} {'M-minus-6W':>11s} {'t':>8s} {'W/L':>9s} {'sign p':>8s} "
      f"{'M':>8s} {'6W':>8s}")
    split_rows = []
    for e in ESTS:
        for fam in ["ALL"] + FAMILIES:
            sub = est[(est.est == e)] if fam == "ALL" else est[(est.est == e) & (est.family == fam)]
            piv = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")
            d = (piv["M"] - piv["6W"]).dropna()
            p, wn, ln = sign_p(d.values)
            P(f"  {e:9s} {fam:7s} {d.mean():11.4f} {tstat(d.values):8.2f} {f'{wn}/{ln}':>9s} "
              f"{p:8.4f} {piv['M'].mean():8.3f} {piv['6W'].mean():8.3f}")
            split_rows.append(dict(est=e, family=fam, d=d.mean(), t=tstat(d.values),
                                   win=wn, loss=ln, sign_p=p,
                                   M=piv["M"].mean(), sixW=piv["6W"].mean(), n=len(d)))
        P("")
    pd.DataFrame(split_rows).to_csv(OUT / f"{STEM}.split.csv", index=False)

    # ------------------------------------------------ rule 8
    P("=" * 118)
    P("RULE 8 WALK-FORWARD.  Every arm chooses on IS (<= 2016-12-31) only; OOS read once.")
    P("")
    rng = np.random.default_rng(RAND_SEED)
    rand_pick = {b: LADDER[int(rng.integers(len(LADDER)))] for b in sorted(est.book.unique())}
    wf_rows = []
    for e in ESTS:
        sub = est[est.est == e]
        isS = sub.pivot_table(index="book", columns="point", values="IS_Sharpe")[LADDER]
        isM = sub.pivot_table(index="book", columns="point", values="IS_margin")[LADDER]
        oS = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")[LADDER]
        oC = sub.pivot_table(index="book", columns="point", values="OOS_CAGR")[LADDER]
        oD = sub.pivot_table(index="book", columns="point", values="OOS_MaxDD")[LADDER]
        picks = {}
        for c in CONSTS:
            picks[f"CONST-{c}"] = pd.Series(c, index=oS.index)
        picks["SEL-SHARPE"] = isS.idxmax(axis=1)
        picks["SEL-4B"] = isM.idxmax(axis=1)
        picks["RANDOM"] = pd.Series({b: rand_pick[b] for b in oS.index})
        picks["ORACLE"] = oS.idxmax(axis=1)
        for fam in ["ALL"] + FAMILIES:
            bks = oS.index if fam == "ALL" else [b for b in oS.index if family_of(b) == fam]
            for a in ARMS:
                pk = picks[a].loc[bks]
                s = pd.Series([oS.loc[b, pk[b]] for b in bks], index=bks)
                c = pd.Series([oC.loc[b, pk[b]] for b in bks], index=bks)
                dd = pd.Series([oD.loc[b, pk[b]] for b in bks], index=bks)
                wf_rows.append(dict(est=e, family=fam, arm=a, n=len(bks),
                                    OOS_Sharpe=s.mean(), OOS_CAGR=c.mean(), OOS_MaxDD=dd.mean(),
                                    modal_pick=pk.value_counts().index[0],
                                    modal_share=pk.value_counts().iloc[0] / len(pk)))
    wf = pd.DataFrame(wf_rows)
    for k, v in SPY.items():
        mo = metrics(v.loc[OOS_START:])
        mbo = metrics(BASE[k].loc[OOS_START:])
        wf = pd.concat([wf, pd.DataFrame([
            dict(est="-", family=f"BENCH-{k}", arm="SPY", n=0, OOS_Sharpe=mo["Sharpe"],
                 OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"], modal_pick="-", modal_share=np.nan),
            dict(est="-", family=f"BENCH-{k}", arm="RULES v1", n=0, OOS_Sharpe=mbo["Sharpe"],
                 OOS_CAGR=mbo["CAGR"], OOS_MaxDD=mbo["MaxDD"], modal_pick="-", modal_share=np.nan)])],
            ignore_index=True)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    for fam in ["ALL"] + FAMILIES:
        P(f"  --- family {fam}:  mean OOS Sharpe by arm (CAGR / MaxDD in parentheses)")
        P(f"  {'est':9s} " + " ".join(f"{a:>12s}" for a in ARMS))
        for e in ESTS:
            g = wf[(wf.est == e) & (wf.family == fam)].set_index("arm")
            P(f"  {e:9s} " + " ".join(f"{g.loc[a,'OOS_Sharpe']:12.4f}" for a in ARMS))
        P("")
    P("  benchmarks over the same OOS window:")
    for k in SPY:
        b = wf[wf.family == f"BENCH-{k}"].set_index("arm")
        P(f"    {k:6s} SPY      {b.loc['SPY','OOS_CAGR']:7.2%} / {b.loc['SPY','OOS_Sharpe']:.4f} / "
          f"{b.loc['SPY','OOS_MaxDD']:7.2%}")
        P(f"    {k:6s} RULES v1 {b.loc['RULES v1','OOS_CAGR']:7.2%} / {b.loc['RULES v1','OOS_Sharpe']:.4f} / "
          f"{b.loc['RULES v1','OOS_MaxDD']:7.2%}")
    P("")
    P("  THE DECISION NUMBER - fitted selector minus the best CONSTANT, paired per book, pooled:")
    P(f"  {'est':9s} {'SEL-SHARPE - best const':>24s} {'t':>8s} {'SEL-4B - best const':>21s} "
      f"{'t':>8s} {'best const':>11s} {'capture of ORACLE':>18s}")
    for e in ESTS:
        sub = est[est.est == e]
        isS = sub.pivot_table(index="book", columns="point", values="IS_Sharpe")[LADDER]
        isM = sub.pivot_table(index="book", columns="point", values="IS_margin")[LADDER]
        oS = sub.pivot_table(index="book", columns="point", values="OOS_Sharpe")[LADDER]
        cmeans = {c: oS[c].mean() for c in CONSTS}
        bc = max(cmeans, key=cmeans.get)
        base_v = oS[bc]
        d1 = (pd.Series([oS.loc[b, isS.loc[b].idxmax()] for b in oS.index], index=oS.index) - base_v)
        d2 = (pd.Series([oS.loc[b, isM.loc[b].idxmax()] for b in oS.index], index=oS.index) - base_v)
        orc = oS.max(axis=1).mean()
        cap = (d1.mean()) / (orc - base_v.mean()) if orc > base_v.mean() else np.nan
        P(f"  {e:9s} {d1.mean():24.4f} {tstat(d1.values):8.2f} {d2.mean():21.4f} "
          f"{tstat(d2.values):8.2f} {bc:>11s} {cap:18.1%}")
    P("")

    # ------------------------------------------------ KEEP paths
    P("=" * 118)
    P("BOTH KEEP PATHS on all 5980 estimator-rows (PROTOCOL rule 4).")
    kp = est.copy()
    kp["pass4a"] = kp.fail4a == "-"
    kp["pass4b"] = kp.fail4b == "-"
    kp.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'est':9s} {'4a':>6s} {'4b':>6s} {'4b SMALL':>9s} {'4b U56':>7s} {'4b ETF':>7s} "
      f"{'4b on fixed panels':>40s}")
    for e in ESTS:
        s = kp[kp.est == e]
        fx = s[s.pass4b & s.book.isin(["SMALL439", "U56", "ETF36"])]
        names = ", ".join(sorted({f"{r.book}@{r.point}" for r in fx.itertuples()})) or "none"
        P(f"  {e:9s} {int(s.pass4a.sum()):6d} {int(s.pass4b.sum()):6d} "
          f"{int(s[s.family=='SMALL'].pass4b.sum()):9d} {int(s[s.family=='U56'].pass4b.sum()):7d} "
          f"{int(s[s.family=='ETF'].pass4b.sum()):7d} {names[:40]:>40s}")
    P("")
    P("  4b passes on the three FIXED panels, in full (idea 144: a re-cadenced or re-phased book")
    P("  is the SAME book, so these are not new candidates unless the averaging itself creates one):")
    fx = kp[kp.pass4b & kp.book.isin(["SMALL439", "U56", "ETF36"])]
    if len(fx):
        P(f"    {'book':9s} {'point':>6s} {'est':9s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
          f"{'H1/H2':>13s} {'OOS_Sh':>7s} {'turn':>7s}")
        for r in fx.sort_values(["book", "point", "est"]).itertuples():
            P(f"    {r.book:9s} {r.point:>6s} {r.est:9s} {r.CAGR:7.2%} {r.Sharpe:7.3f} "
              f"{r.MaxDD:8.2%} {f'{r.H1:.2f}/{r.H2:.2f}':>13s} {r.OOS_Sharpe:7.3f} {r.turnover:7.2f}")
    else:
        P("    none")
    P("")
    P("  DOES AVERAGING ITSELF CREATE A 4b PASS?  rows that fail 4b at PH0 and pass under an")
    P("  averaged estimator, and the reverse:")
    piv4b = kp.pivot_table(index=["book", "point"], columns="est", values="pass4b").astype(bool)
    for e in ESTS[1:]:
        gained = int((~piv4b["PH0"] & piv4b[e]).sum())
        lost = int((piv4b["PH0"] & ~piv4b[e]).sum())
        P(f"    {e:9s} PH0-fail -> pass: {gained:4d}    PH0-pass -> fail: {lost:4d}    "
          f"net {gained-lost:+4d}  of {len(piv4b)} (book,point) cells")
    P("")

    P(f"DONE in {time.time()-t0:.0f}s")
    flush()


if __name__ == "__main__":
    main()
