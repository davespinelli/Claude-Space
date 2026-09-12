#!/usr/bin/env python3
"""Idea 826 - adjudicate the THREE 2026-09-12 runs of idea 609 against each other (lane C).

THE PROBLEM
-----------
The record now carries three numbers for one question - "how often is idea 605's published family
ordering QROLL > QEXP > ABS the ordering a reader standing in a rolling 3-year window would
actually have seen?":

    aa87884  lane B    0.0847    (5 of 59)        headline: WINDOW-matched twin, AS-OF corpus
    2c96cad  cloud     0.322     (19 of 59)       headline: FULL-matched twin, TODAY's corpus
    _B2      lane B    0.322034 / 0.3125          FULL-matched, TODAY, step 63 / step 21

The _B2 run reproduces the cloud run to the published digit, so two of the three are one number.
7df829b (lane C, idea 824) then diagnosed the remaining spread as the twin's MATCHING SAMPLE, and
found that 714 of 717 verdict flips it produces are arms whose gate NEVER FIRES in the evaluation
window - for which WINMATCH makes the twin the arm itself (dSharpe identically 0, scored a LOSS by
`win = dSharpe > TIE`) while FULLMATCH returns a win by <= 1.31e-03.  That diagnosis was made on
the record's SIX committed claim windows.  It has never been applied to the ROLLING census that
produced 0.0847 and 0.322, which is the object actually in dispute.

WHAT THIS RUN DOES
------------------
A fourth, independent implementation that (a) rebuilds all three published headlines inside ONE
code path, (b) decomposes the 0.0847 -> 0.322 spread into its named legs, (c) applies idea 824's
never-fires diagnosis to the rolling census itself, and (d) publishes ONE reconciled headline per
convention plus a recommendation for which the record should quote.

    Q1 (REPRODUCE)  Do all three published numbers fall out of one implementation with only the
                    two dials moved?  Gates GR1/GR2/GR3 below.
    Q2 (DECOMPOSE)  Split 0.0847 -> 0.3220 into a CONVENTION leg, a VINTAGE leg and an
                    interaction, at every one of the 9 (window, step) points and 3 cost rungs.
    Q3 (ADJUDICATE) THE DECIDING TEST.  Restrict the census to (arm, window) cells whose gate
                    actually FIRES inside that window - the cells where the twin is a genuinely
                    different object under both conventions - and re-read both numbers.  If the
                    two conventions agree there, neither published number is wrong: the gap is a
                    scoring convention over degenerate cells, and the record should quote the
                    fire-only number with both conventions beside it.  If they still disagree,
                    the convention is a real modelling choice and the record must pick one.
    Q4 (RULE 8)     PROTOCOL rule 8 on the claim (IS windows only -> read OOS once) and on a book
                    (IS census picks the family, IS Sharpe picks the arm, 2017-2026 read once),
                    under BOTH conventions, against RULES v2, RULES v1 and SPY.
    Q5 (PROTOCOL)   Both KEEP paths on every arm x rung, reported in full, never selected on.

PRE-REGISTERED HYPOTHESES (declared here, before any number below was read)
--------------------------------------------------------------------------
    GR1  WINMATCH / ASOF / 756d / step 63 / 10 bps / POOLED  == 0.0847   (lane B's aa87884)
    GR2  FULLMATCH / TODAY / 756d / step 63 / 10 bps / POOLED == 0.3220  (cloud 2c96cad, _B2)
    GR3  FULLMATCH / TODAY / 756d / step 21 / 10 bps / POOLED == 0.3125  (_B2's denser census)
         Bar for all three: |diff| <= 0.0001 (they are ratios of small integers; anything above
         that is a different population, not a rounding difference).
    H_CONV    the CONVENTION leg is the dominant one: |FULLMATCH - WINMATCH| >= 0.15 at the
              headline cell, on both vintages.
    H_VINT    the VINTAGE leg is minor: |TODAY - ASOF| <= 0.05 at the headline cell, on both
              conventions.  (If both hold, the queue's premise - "the spread is the matching
              sample" - is confirmed and the three numbers are two numbers.)
    H_STEP    the tuned step moves the answer less than the convention does: the span of the
              exact share over step in {21, 63, 126} is <= 0.10 at fixed (window, convention).
    H_FIRE    THE DECIDING BAR.  On the FIRE-only population the two conventions agree within
              0.05 at the headline cell.  A pass says the dispute is about degenerate cells and
              the record can quote one reconciled number; a fail says it is a real modelling
              choice.
    H_DEGEN   never-firing cells are not a rounding detail: >= 0.20 of (arm, window) cells in the
              headline census have a gate that never fires inside the window.
    H_ONE     there is a statement both conventions support at >= 0.90: QROLL > QEXP.
    H_WF      rule 8 on the claim: |OOS exact share - IS exact share| <= 0.10 under both
              conventions.
    H_BOOK    rule 8 on a book: the IS-selected book beats RULES v2 AND SPY on OOS Sharpe.

TUNED PARAMETERS (PROTOCOL rule 4: at most two) - the queue names both, and only these two
    1. convention  FULLMATCH (g_eff matched once on the full evaluation sample, path sliced into
                   the window - idea 605's own, nowhere stated in its memo) vs WINMATCH (g_eff
                   re-matched on the evaluation window itself - what a reader holding only that
                   window would build).  BOTH reported everywhere; neither is a headline.
    2. step        21 / 63 / 126 trading days.  Headline 63, because that is the step all three
                   disputed runs used; 21 reported because _B2 headlined it.

REPORTED AXES, NEVER TUNED AND NEVER SELECTED ON
    vintage   ASOF (the caches idea 605 actually read: prices.csv / prices_broad.csv truncated to
              its last dates, prices_small.csv.gz + small_meta.csv restored from git blob
              e02949d) and TODAY.  This is a REPRODUCTION axis: without it lane B's headline
              cannot be rebuilt at all, because the nightly Actions job took the small panel from
              439 to 663 tradable names on 2026-09-11 (commit 56e08b1).
    window    504 / 756 / 1008 trading days (lane B's own three; 756 = "3-year" is the shared
              headline of all three disputed runs).
    rung      0 / 10 / 25 bps, headline PROTOCOL's 10.
    scope     POOLED (3 panels) / POOLED_REPRO (U56 + B136, the two that reproduce idea 605) /
              per panel.
    pop       ALL cells vs FIRE-only cells (the Q3 diagnosis).
    family, level, w, depth, cadence, panel, gross - inherited verbatim from ideas 602/605.

GATES (printed before any new number is read)
    G1  derived cost ladder r(c) = m*r0 - (c/1e4)*(m*t0 + g*|dm|) vs a live engine.backtest.
    G2  fast CAGR/Sharpe/MaxDD vs engine.metrics on real series.
    G3  the 0.01 twin-gross grid + quadratic-in-lambda window variance vs an EXACT twin run.
    G4  idea 84's ungated EWALL U56 g=0.85 @ 10 bps: 11.8% / 1.05 / -17.9%.
    G5  the O(1) cumsum window-Sharpe vs a direct numpy Sharpe on the same slice.
    GR1/GR2/GR3 above: the three published headlines.

Data: committed caches and git blobs only.  No network, never yfinance.
SURVIVORSHIP: all three panels are current-constituent lists, so CAGR and drawdown LEVELS are
optimistic.  Every statistic here is a WITHIN-panel contrast between arms sharing a panel, or a
count of orderings, which the bias does not move.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import subprocess
import sys
import tempfile
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-12"
SLUG = "adjudicate-the-THREE-2026-09-12-runs-of-idea-609-against-each-other"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

FREQ, LAG, WARMUP, MAX_VOL, MINQ = "W", 1, 260, 0.60, 252
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS_ROLL = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
WINDOWS = [504, 756, 1008]
STEPS = [21, 63, 126]                      # tuned 2
W_HEAD, S_HEAD, S_ALT = 756, 63, 21
CONVS = ["FULLMATCH", "WINMATCH"]          # tuned 1
POPS = ["ALL", "FIRE"]
VINTAGES = ["ASOF", "TODAY"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TIE = 1e-12
GSTEP = 0.01
MIN_GEFF = 0.005
MIN_COVER = 0.80                           # lane B's; _B2 used 0.90, checked at the headline cell
FAMS = ["QROLL", "QEXP", "ABS"]            # idea 605's published order, best -> worst
PUB_RANK = {"ABS": 1.0, "QEXP": 2.0, "QROLL": 3.0}
SMALL_MAXMOVE = 1.0
ASOF_BLOB = "e02949d"
ASOF_END = {"U56": "2026-09-09", "B136": "2026-09-04", "SMALL": "2026-09-04"}

# the three published headlines under adjudication
PUBLISHED_CLAIMS = [
    ("GR1", "aa87884 lane B", "WINMATCH", "ASOF", W_HEAD, S_HEAD, RUNG_HEAD, 0.0847),
    ("GR2", "2c96cad cloud / _B2", "FULLMATCH", "TODAY", W_HEAD, S_HEAD, RUNG_HEAD, 0.3220),
    ("GR3", "_B2 dense census", "FULLMATCH", "TODAY", W_HEAD, S_ALT, RUNG_HEAD, 0.3125),
]
# the record's standing 4b candidate (idea 609's by-product), re-read here for continuity
CAND = dict(panel="B136", family="QROLL", level=0.17, w=252, depth=0.50, cadence="D", gross=1.00)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- primitives (596/604/811/813)
def fast_run(prices, weights, mask, lag=LAG):
    """(gross return path before costs, turnover path) - engine.backtest, vectorised."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
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
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def rows_metrics(R):
    n = R.shape[1]
    eq = np.cumprod(1.0 + R, axis=1)
    cagr = eq[:, -1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    vol = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    return cagr, np.where(vol > 0, R.mean(axis=1) * 252.0 / np.where(vol > 0, vol, 1.0), np.nan), dd


def rows_sharpe(R):
    vol = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(vol > 0, R.mean(axis=1) * 252.0 / np.where(vol > 0, vol, 1.0), np.nan)


def cs(x):
    return np.concatenate([[0.0], np.cumsum(x)])


def win_sharpe(C1, C2, s, e):
    """Sharpe of every row over [s, e) from cumulative sums of r and r**2."""
    L = float(e - s)
    m = (C1[:, e] - C1[:, s]) / L
    var = ((C2[:, e] - C2[:, s]) - L * m * m) / (L - 1.0)
    return np.where(var > 1e-300, m * 252.0 / np.sqrt(np.maximum(var, 1e-300) * 252.0), np.nan)


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross, elig):
    e = elig.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_series(br, thr, depth, cadence, idx):
    m = pd.Series(1.0, index=idx).where(~(br < thr), 1.0 - depth)
    ok = br.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0) if cadence == "W" else m


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def order_token(wr):
    items = sorted(wr.items(), key=lambda kv: (-kv[1], kv[0]))
    out = ""
    for i, (f, v) in enumerate(items):
        out += f[0] if i == 0 else (("=" if abs(v - items[i - 1][1]) <= TIE else ">") + f[0])
    return out


# ---------------------------------------------------------------- panel construction
def panel_today(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(REPO / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        px = px.drop(columns=[c for c in px.columns if c in bad and c != "SPY"])
    return px.dropna(how="all").ffill()


def panels_asof(tmp):
    """The caches idea 605 actually read (lane B's G4a construction, rebuilt independently)."""
    out = [("U56", load_universe().loc[:ASOF_END["U56"]]),
           ("B136", load_universe(broad=True).loc[:ASOF_END["B136"]])]
    blobs = {}
    for f in ("data/prices_small.csv.gz", "data/small_meta.csv"):
        p = tmp / Path(f).name
        p.write_bytes(subprocess.run(["git", "-C", str(REPO), "show", f"{ASOF_BLOB}:{f}"],
                                     capture_output=True, check=True).stdout)
        blobs[f] = p
    ps = pd.read_csv(blobs["data/prices_small.csv.gz"], index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    spy = pd.read_csv(REPO / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"),
                    spy.reindex(ps.index, method="ffill").rename("SPY")], axis=1)
    meta = pd.read_csv(blobs["data/small_meta.csv"])
    bad = set(meta.loc[meta["max_1d_move"] >= SMALL_MAXMOVE, "ticker"])
    ps = ps[[c for c in ps.columns if c == "SPY" or c not in bad]].loc[:ASOF_END["SMALL"]]
    out.append(("SMALL", ps))
    return out


def build_panel(name, px):
    """Everything the census needs for one panel: arms, gate cumsums, twin grid cumsums."""
    idx = px.index
    start = idx[WARMUP]
    eidx = px.loc[start:].index
    n = len(eidx)
    elig = eligible_mask(px)
    mask = rebalance_mask(idx, FREQ)
    br_full = breadth(px)

    base0 = {}
    for g in GROSSES:
        r, t = fast_run(px, ewall_weights(px, g, elig), mask)
        base0[g] = (r.loc[start:].values, t.loc[start:].values)

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS_ROLL}
    forms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
             + [("QROLL", q, w) for q in QS for w in WS_ROLL])

    arms, ME, rg0, Cg = [], [], [], []
    for (fam, lev, w), d, cad in product(forms, DEPTHS, CADENCES):
        thr = lev if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
        me = gate_series(br_full, thr, d, cad, idx).reindex(eidx).shift(1).fillna(1.0).values
        sw = np.abs(np.diff(me, prepend=me[0]))
        for g in GROSSES:
            r0, t0 = base0[g]
            arms.append(dict(family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                             arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}"))
            ME.append(me)
            rg0.append(me * r0)
            Cg.append(me * t0 + g * sw)
    ME = np.asarray(ME)
    rg0 = np.asarray(rg0)
    Cg = np.asarray(Cg)
    garr = np.array([a["gross"] for a in arms])
    geff_full = np.maximum(garr * ME.mean(axis=1), MIN_GEFF)
    me_cs = np.vstack([cs(ME[i]) for i in range(len(arms))])

    Pk = dict(panel=name, px=px, start=start, eidx=eidx, n=n, arms=arms, ME=ME, me_cs=me_cs,
              garr=garr, geff_full=geff_full, elig=elig, mask=mask, base0=base0,
              fam_idx={f: np.array([i for i, a in enumerate(arms) if a["family"] == f])
                       for f in FAMS})
    Pk["NET"] = {c: rg0 - Cg * c / 1e4 for c in RUNGS}
    Pk["CG"] = {c: np.vstack([cs(Pk["NET"][c][i]) for i in range(len(arms))]) for c in RUNGS}
    Pk["CG2"] = {c: np.vstack([cs(Pk["NET"][c][i] ** 2) for i in range(len(arms))]) for c in RUNGS}
    return Pk


def attach_twins(Pk, need):
    """Exact EWALL twin runs on the 0.01 gross grid, plus cumsums of r, r^2 and adjacent products
    so a window Sharpe at an interpolated gross is O(1) and quadratic in lambda."""
    px, start, elig, mask = Pk["px"], Pk["start"], Pk["elig"], Pk["mask"]
    want = set()
    for g in need:
        lo = round(np.floor(round(float(g), 6) / GSTEP) * GSTEP, 6)
        want.add(lo)
        want.add(round(lo + GSTEP, 6))
    vals = sorted(v for v in want if v >= 0.0)
    R0, T0 = [], []
    for v in vals:
        if v <= 0.0:
            R0.append(np.zeros(Pk["n"]))
            T0.append(np.zeros(Pk["n"]))
            continue
        r, t = fast_run(px, ewall_weights(px, float(v), elig), mask)
        R0.append(r.loc[start:].values)
        T0.append(t.loc[start:].values)
    R0, T0 = np.asarray(R0), np.asarray(T0)
    Pk["gvals"] = vals
    Pk["gidx"] = {v: i for i, v in enumerate(vals)}
    Pk["CA"], Pk["CA2"], Pk["CAB"] = {}, {}, {}
    for c in RUNGS:
        A = R0 - T0 * c / 1e4
        Pk["CA"][c] = np.vstack([cs(A[k]) for k in range(len(vals))])
        Pk["CA2"][c] = np.vstack([cs(A[k] ** 2) for k in range(len(vals))])
        AB = np.zeros((len(vals), Pk["n"] + 1))
        for k, v in enumerate(vals):
            hv = round(v + GSTEP, 6)
            if hv in Pk["gidx"]:
                AB[k] = cs(A[k] * A[Pk["gidx"][hv]])
        Pk["CAB"][c] = AB
    Pk["n_exact"] = int(len(vals))
    return Pk


def twin_sharpe(Pk, c, geff, s, e):
    L = float(e - s)
    lo = np.round(np.floor(np.round(geff, 6) / GSTEP) * GSTEP, 6)
    lam = (np.round(geff, 6) - lo) / GSTEP
    li = np.array([Pk["gidx"][round(float(v), 6)] for v in lo])
    hi = np.array([Pk["gidx"][round(float(v) + GSTEP, 6)] for v in lo])
    CA, CA2, CAB = Pk["CA"][c], Pk["CA2"][c], Pk["CAB"][c]
    S1 = (1 - lam) * (CA[li, e] - CA[li, s]) + lam * (CA[hi, e] - CA[hi, s])
    S2 = ((1 - lam) ** 2 * (CA2[li, e] - CA2[li, s])
          + 2 * lam * (1 - lam) * (CAB[li, e] - CAB[li, s])
          + lam ** 2 * (CA2[hi, e] - CA2[hi, s]))
    m = S1 / L
    var = (S2 - L * m * m) / (L - 1.0)
    return np.where(var > 1e-300, m * 252.0 / np.sqrt(np.maximum(var, 1e-300) * 252.0), np.nan)


def twin_path(Pk, c, g):
    lo = round(np.floor(round(float(g), 6) / GSTEP) * GSTEP, 6)
    lam = (round(float(g), 6) - lo) / GSTEP
    li, hi = Pk["gidx"][lo], Pk["gidx"][round(lo + GSTEP, 6)]
    A = np.diff(Pk["CA"][c], axis=1)
    return (1 - lam) * A[li] + lam * A[hi]


# ---------------------------------------------------------------- the census
def window_positions(Pk, master, W, S):
    pos = []
    ei = Pk["eidx"]
    for i in range(0, len(master) - W + 1, S):
        d0, d1 = master[i], master[i + W - 1]
        s = int(ei.searchsorted(d0, side="left"))
        e = int(ei.searchsorted(d1, side="right"))
        pos.append((s, e) if (e - s) >= MIN_COVER * W and (e - s) > 2 else None)
    return pos


def run_census(vintage, PANELS, master):
    rows = []
    repro = [p["panel"] for p in PANELS if p["panel"] != "SMALL"]
    for W, S in product(WINDOWS, STEPS):
        posn = {p["panel"]: window_positions(p, master, W, S) for p in PANELS}
        nwin = len(next(iter(posn.values())))
        for wi in range(nwin):
            d0, d1 = master[wi * S], master[wi * S + W - 1]
            # per panel: dSharpe under both conventions, at every rung
            per = {}
            for Pk in PANELS:
                se = posn[Pk["panel"]][wi]
                if se is None:
                    continue
                s, e = se
                mm = (Pk["me_cs"][:, e] - Pk["me_cs"][:, s]) / (e - s)
                fire = mm < 1.0 - 1e-12
                geff_w = np.maximum(Pk["garr"] * mm, MIN_GEFF)
                d = {}
                for c in RUNGS:
                    gs = win_sharpe(Pk["CG"][c], Pk["CG2"][c], s, e)
                    d[("FULLMATCH", c)] = gs - twin_sharpe(Pk, c, Pk["geff_full"], s, e)
                    d[("WINMATCH", c)] = gs - twin_sharpe(Pk, c, geff_w, s, e)
                per[Pk["panel"]] = (d, fire, Pk["fam_idx"])
            if not per:
                continue
            scopes = {"POOLED": list(per), "POOLED_REPRO": [p for p in repro if p in per]}
            scopes.update({p: [p] for p in per})
            for conv, c, pop in product(CONVS, RUNGS, POPS):
                for sc, members in scopes.items():
                    if not members:
                        continue
                    wr, ns, ok = {}, {}, True
                    for f in FAMS:
                        nw = na = 0
                        for p in members:
                            d, fire, fidx = per[p]
                            sel = fidx[f]
                            dv = d[(conv, c)][sel]
                            keep = np.isfinite(dv)
                            if pop == "FIRE":
                                keep = keep & fire[sel]
                            nw += int((dv[keep] > TIE).sum())
                            na += int(keep.sum())
                        if na == 0:
                            ok = False
                        wr[f] = nw / na if na else np.nan
                        ns[f] = na
                    if not ok:
                        continue
                    rows.append(dict(
                        vintage=vintage, scope=sc, window=W, step=S, conv=conv, rung=c, pop=pop,
                        wi=wi, start=d0.date(), end=d1.date(),
                        win_QROLL=wr["QROLL"], win_QEXP=wr["QEXP"], win_ABS=wr["ABS"],
                        n_QROLL=ns["QROLL"], n_QEXP=ns["QEXP"], n_ABS=ns["ABS"],
                        order=order_token(wr),
                        exact=bool(wr["QROLL"] - wr["QEXP"] > TIE and wr["QEXP"] - wr["ABS"] > TIE),
                        QR_gt_QE=bool(wr["QROLL"] - wr["QEXP"] > TIE),
                        QE_gt_AB=bool(wr["QEXP"] - wr["ABS"] > TIE),
                        QR_gt_AB=bool(wr["QROLL"] - wr["ABS"] > TIE),
                        rho=spearman([PUB_RANK[f] for f in FAMS], [wr[f] for f in FAMS])))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- full-sample arm table
def arm_table(vintage, Pk):
    n = Pk["n"]
    eidx = Pk["eidx"]
    h = n // 2
    is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
    oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
    px = Pk["px"]
    spy = px["SPY"].pct_change().fillna(0).loc[Pk["start"]:].values
    sc, ss, sd = fmet(spy)
    spy_h1, spy_h2, spy_oos = fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:])
    v2r, v2t = fast_run(px, rules_v2_weights(px), Pk["mask"])
    v1r, v1t = fast_run(px, rules_v1_weights(px), Pk["mask"])
    v2r, v2t = v2r.loc[Pk["start"]:].values, v2t.loc[Pk["start"]:].values
    v1r, v1t = v1r.loc[Pk["start"]:].values, v1t.loc[Pk["start"]:].values
    refs, rows = {}, []
    for c in RUNGS:
        v2 = v2r - v2t * c / 1e4
        v1 = v1r - v1t * c / 1e4
        refs[c] = dict(v2=(fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2], fmet(v2[oos0:]),
                           fmet(v2)),
                       v1=(fsharpe(v1[:h]), fsharpe(v1[h:]), fmet(v1)[2], fmet(v1[oos0:]),
                           fmet(v1)))
        R = Pk["NET"][c]
        cg, shg, ddg = rows_metrics(R)
        h1, h2 = rows_sharpe(R[:, :h]), rows_sharpe(R[:, h:])
        iss = rows_sharpe(R[:, :is_end])
        ocg, oshg, oddg = rows_metrics(R[:, oos0:])
        b1, b2, bdd = refs[c]["v2"][0], refs[c]["v2"][1], refs[c]["v2"][2]
        for i, a in enumerate(Pk["arms"]):
            t4b = dict(H1=h1[i] > spy_h1, H2=h2[i] > spy_h2, OOS=oshg[i] > spy_oos,
                       DD=abs(ddg[i]) <= 0.60 * abs(sd), CAGR=cg[i] >= 0.70 * sc)
            rows.append(dict(vintage=vintage, panel=Pk["panel"], rung=c, **{k: a[k] for k in
                             ("family", "level", "w", "depth", "cadence", "gross", "arm")},
                             g_eff=Pk["geff_full"][i], on_share=float((Pk["ME"][i] < 1.0).mean()),
                             CAGR=cg[i], Sharpe=shg[i], MaxDD=ddg[i], H1=h1[i], H2=h2[i],
                             IS_Sharpe=iss[i], OOS_CAGR=ocg[i], OOS_Sharpe=oshg[i],
                             OOS_MaxDD=oddg[i],
                             p4a=bool(h1[i] > b1 and h2[i] > b2 and ddg[i] >= bdd),
                             p4b=all(t4b.values()),
                             fail4b=",".join(k for k, v in t4b.items() if not v) or "-"))
    spy_pack = dict(CAGR=sc, Sharpe=ss, MaxDD=sd, H1=spy_h1, H2=spy_h2, OOS_Sharpe=spy_oos,
                    OOS=fmet(spy[oos0:]))
    return pd.DataFrame(rows), spy_pack, refs, (h, is_end, oos0)


def main():
    t0 = time.time()
    P("=" * 150)
    P(f"Idea 826 - {SLUG}  (lane C, {DATE})")
    P("=" * 150)
    P("OBJECT: three committed numbers for one question (rolling-window agreement with idea 605's")
    P("  published family order QROLL > QEXP > ABS): 0.0847 / 0.322 / 0.322034-0.3125.")
    P(f"TUNED (2): convention {CONVS} x step {STEPS}.  Headline step {S_HEAD} (all three disputed")
    P(f"  runs used it); neither convention is a headline - that is the question.")
    P(f"REPORTED, never selected on: vintage {VINTAGES} (reproduction axis), window {WINDOWS}d,")
    P(f"  rung {RUNGS} bps (headline {RUNG_HEAD:g}), scope, population {POPS}, and the 216-arm")
    P("  family/level/w/depth/cadence/gross grid inherited from ideas 602/605.")
    P("SURVIVORSHIP: current-constituent panels; LEVELS optimistic, within-panel contrasts are not.")

    # ================================================================== [0] gates
    P("\n" + "=" * 150)
    P("[0] REPRODUCTION GATES")
    px0 = load_universe()
    st0 = px0.index[WARMUP]
    e0 = px0.loc[st0:].index
    el0 = eligible_mask(px0)
    mk0 = rebalance_mask(px0.index, FREQ)
    Wb = ewall_weights(px0, 0.75, el0)
    rg, tn = fast_run(px0, Wb, mk0)
    br0 = breadth(px0)
    me = gate_series(br0, 0.40, 0.50, "W", px0.index).reindex(e0).shift(1).fillna(1.0).values
    sw = np.abs(np.diff(me, prepend=me[0]))
    g1 = 0.0
    for c in [0.0, 10.0, 25.0, 100.0]:
        live = backtest(px0, Wb, cost_bps=c, freq=FREQ)["returns"].loc[st0:].values
        ref = me * live - sw * 0.75 * c / 1e4
        der = me * rg.loc[st0:].values - (me * tn.loc[st0:].values + 0.75 * sw) * c / 1e4
        g1 = max(g1, float(np.abs(ref - der).max()))
    P(f"   G1 derived gate ladder == live engine.backtest through apply_gate, 4 rungs: "
      f"max|d| {g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    ser = pd.Series((rg - tn * 10 / 1e4).loc[st0:].values, index=e0)
    m = metrics(ser)
    fc, fs, fd = fmet(ser.values)
    g2 = max(abs(fc - m["CAGR"]), abs(fs - m["Sharpe"]), abs(fd - m["MaxDD"]))
    P(f"   G2 fast metrics == engine.metrics: max|d| {g2:.3e} (bar 1e-12) -> "
      f"{'PASS' if g2 < 1e-12 else 'FAIL'}")

    r84 = backtest(px0, ewall_weights(px0, 0.85, el0), cost_bps=10, freq=FREQ)["returns"].loc[st0:]
    c84, s84, d84 = fmet(r84.values)
    P(f"   G4 idea 84 EWALL U56 g=0.85 @10bps: {c84:.2%} / {s84:.3f} / {d84:.2%} "
      f"(committed 11.8% / 1.05 / -17.9%) -> "
      f"{'PASS' if abs(c84-0.118) < 6e-3 and abs(s84-1.05) < 6e-3 and abs(d84+0.179) < 6e-3 else 'CHECK'}")

    # ================================================================== corpora
    tmp = Path(tempfile.mkdtemp())
    CORP = {}
    for vintage in VINTAGES:
        plist = panels_asof(tmp) if vintage == "ASOF" else [(n, panel_today(n)) for n in
                                                            ("U56", "B136", "SMALL")]
        P(f"\n   corpus {vintage}:")
        built = [build_panel(name, px) for name, px in plist]
        master = built[0]["eidx"]                 # U56's eval calendar drives the census
        for Pk in built:
            need = list(Pk["geff_full"])
            for W, S in product(WINDOWS, STEPS):
                for se in window_positions(Pk, master, W, S):
                    if se is None:
                        continue
                    s, e = se
                    mm = (Pk["me_cs"][:, e] - Pk["me_cs"][:, s]) / (e - s)
                    need += list(np.maximum(Pk["garr"] * mm, MIN_GEFF))
            attach_twins(Pk, need)
            P(f"     {Pk['panel']:6s} {Pk['px'].shape[1]-1:4d} tradable + SPY, "
              f"{Pk['px'].index[0].date()} -> {Pk['px'].index[-1].date()}, eval {Pk['n']} days, "
              f"{len(Pk['arms'])} arms, {Pk['n_exact']} exact twin runs")
        CORP[vintage] = built

    # G3 / G5 on U56 TODAY
    Pk = CORP["TODAY"][0]
    gx = 0.6237
    exr, ext = fast_run(Pk["px"], ewall_weights(Pk["px"], gx, Pk["elig"]), Pk["mask"])
    exn = (exr - ext * RUNG_HEAD / 1e4).loc[Pk["start"]:].values
    itp = twin_path(Pk, RUNG_HEAD, gx)
    g3 = abs(fsharpe(exn) - fsharpe(itp))
    P(f"\n   G3 0.01 twin grid + quadratic-lambda variance vs an EXACT twin run at g={gx}: "
      f"|dSharpe| {g3:.3e} (bar 1e-6) -> {'PASS' if g3 < 1e-6 else 'FAIL'}")
    rng = np.random.default_rng(826)
    g5 = 0.0
    for _ in range(200):
        c = float(rng.choice(RUNGS))
        s = int(rng.integers(0, Pk["n"] - 800))
        e = s + int(rng.integers(400, 800))
        i = int(rng.integers(len(Pk["arms"])))
        a = win_sharpe(Pk["CG"][c][i:i + 1], Pk["CG2"][c][i:i + 1], s, e)[0]
        b = fsharpe(Pk["NET"][c][i, s:e])
        g5 = max(g5, abs(a - b))
        pairs = [v for v in Pk["gvals"] if round(v + GSTEP, 6) in Pk["gidx"] and v > 0.05]
        gq = float(pairs[int(rng.integers(len(pairs)))] + GSTEP * rng.uniform(0.0, 0.999))
        a2 = twin_sharpe(Pk, c, np.array([gq]), s, e)[0]
        b2 = fsharpe(twin_path(Pk, c, gq)[s:e])
        g5 = max(g5, abs(a2 - b2))
    P(f"   G5 O(1) window Sharpe (gate AND twin) vs direct numpy, 400 slices: max|d| {g5:.3e} "
      f"(bar 1e-9) -> {'PASS' if g5 < 1e-9 else 'FAIL'}")

    # ================================================================== [1] census
    P("\n" + "=" * 150)
    P("[1] THE CENSUS - one implementation, both conventions, both vintages, all 9 (window, step)")
    CEN = []
    for vintage in VINTAGES:
        master = CORP[vintage][0]["eidx"]
        P(f"   {vintage}: master calendar {master[0].date()} -> {master[-1].date()} "
          f"({len(master)} days)")
        CEN.append(run_census(vintage, CORP[vintage], master))
    cen = pd.concat(CEN, ignore_index=True)
    grid = (cen.groupby(["vintage", "scope", "window", "step", "conv", "rung", "pop"])
            .agg(n_win=("exact", "size"), exact=("exact", "mean"), QR_gt_QE=("QR_gt_QE", "mean"),
                 QE_gt_AB=("QE_gt_AB", "mean"), QR_gt_AB=("QR_gt_AB", "mean"),
                 mean_rho=("rho", "mean"), mean_QROLL=("win_QROLL", "mean"),
                 mean_QEXP=("win_QEXP", "mean"), mean_ABS=("win_ABS", "mean"))
            .reset_index())

    def cell(vintage, conv, W=W_HEAD, S=S_HEAD, c=RUNG_HEAD, sc="POOLED", pop="ALL"):
        q = grid[(grid.vintage == vintage) & (grid.conv == conv) & (grid.window == W)
                 & (grid.step == S) & (grid.rung == c) & (grid.scope == sc) & (grid["pop"] == pop)]
        return q.iloc[0] if len(q) else None

    P("\n   GR1-GR3: the three published headlines, rebuilt here")
    P(f"   {'gate':<5} {'source':<22} {'conv':<10} {'vint':<6} {'W/step':<9} "
      f"{'published':>10} {'this run':>10} {'n_win':>6} {'diff':>10}  verdict")
    gr_ok = {}
    for tag, src, conv, vint, W, S, c, pub in PUBLISHED_CLAIMS:
        r = cell(vint, conv, W, S, c)
        got = float(r["exact"]) if r is not None else np.nan
        d = abs(got - pub)
        gr_ok[tag] = bool(d <= 1e-4)
        P(f"   {tag:<5} {src:<22} {conv:<10} {vint:<6} {W}/{S:<5} {pub:>10.4f} {got:>10.4f} "
          f"{int(r['n_win']) if r is not None else 0:>6} {d:>10.2e}  "
          f"{'PASS' if gr_ok[tag] else 'FAIL'}")

    P(f"\n   the 2 x 2 (vintage x convention) at the headline cell "
      f"({W_HEAD}d / step {S_HEAD} / {RUNG_HEAD:g} bps / POOLED / ALL cells):")
    P(f"   {'vintage':<8} {'conv':<10} {'n':>4} {'exact':>8} {'QR>QE':>8} {'QE>AB':>8} "
      f"{'QR>AB':>8} {'rho':>8}")
    for vint, conv in product(VINTAGES, CONVS):
        r = cell(vint, conv)
        P(f"   {vint:<8} {conv:<10} {int(r['n_win']):>4} {r['exact']:>8.4f} "
          f"{r['QR_gt_QE']:>8.4f} {r['QE_gt_AB']:>8.4f} {r['QR_gt_AB']:>8.4f} "
          f"{r['mean_rho']:>+8.4f}")

    # ---- Q2 decomposition
    a_w = cell("ASOF", "WINMATCH")["exact"]
    a_f = cell("ASOF", "FULLMATCH")["exact"]
    t_w = cell("TODAY", "WINMATCH")["exact"]
    t_f = cell("TODAY", "FULLMATCH")["exact"]
    conv_leg = 0.5 * ((a_f - a_w) + (t_f - t_w))
    vint_leg = 0.5 * ((t_w - a_w) + (t_f - a_f))
    inter = (t_f - a_f) - (t_w - a_w)
    P(f"\n   Q2 DECOMPOSITION of the disputed spread {a_w:.4f} (lane B) -> {t_f:.4f} (cloud/_B2) "
      f"= {t_f - a_w:+.4f}")
    P(f"      CONVENTION leg (mean over vintages, WINMATCH -> FULLMATCH) {conv_leg:+.4f}")
    P(f"      VINTAGE    leg (mean over conventions, ASOF -> TODAY)      {vint_leg:+.4f}")
    P(f"      interaction                                                {inter:+.4f}")
    P(f"      -> the convention explains {abs(conv_leg)/abs(t_f-a_w):.1%} of the spread; the "
      f"panel-vintage rewrite {abs(vint_leg)/abs(t_f-a_w):.1%}.")

    P(f"\n   ALL 9 (window, step) points x both conventions, POOLED, {RUNG_HEAD:g} bps, ALL cells "
      f"(nothing selected on):")
    for vint in VINTAGES:
        g = grid[(grid.vintage == vint) & (grid.scope == "POOLED") & (grid["pop"] == "ALL")
                 & (grid.rung == RUNG_HEAD)]
        P(f"     vintage {vint}   exact share")
        P("     " + g.pivot(index=["window"], columns=["conv", "step"], values="exact")
          .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n     "))
    P("\n   n windows behind each (window, step):")
    P("   " + grid[(grid.vintage == "TODAY") & (grid.scope == "POOLED") & (grid["pop"] == "ALL")
                   & (grid.rung == RUNG_HEAD) & (grid.conv == "FULLMATCH")]
      .pivot(index="window", columns="step", values="n_win").to_string().replace("\n", "\n   "))

    P(f"\n   COST LADDER (POOLED, {W_HEAD}d / step {S_HEAD}, ALL cells), every rung:")
    P("   " + grid[(grid.scope == "POOLED") & (grid["pop"] == "ALL") & (grid.window == W_HEAD)
                   & (grid.step == S_HEAD)]
      .pivot(index="rung", columns=["vintage", "conv"], values="exact")
      .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))

    P(f"\n   PER SCOPE ({W_HEAD}d / step {S_HEAD} / {RUNG_HEAD:g} bps, ALL cells):")
    P("   " + grid[(grid["pop"] == "ALL") & (grid.window == W_HEAD) & (grid.step == S_HEAD)
                   & (grid.rung == RUNG_HEAD)]
      .pivot(index="scope", columns=["vintage", "conv"], values="exact")
      .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))

    # ================================================================== [2] the deciding test
    P("\n" + "=" * 150)
    P("[2] Q3 THE DECIDING TEST - what the two conventions do to cells whose gate never fires")
    P("   Idea 824 (7df829b) found 714 of 717 verdict flips between the conventions are arms whose")
    P("   gate never fires in the evaluation window.  For such a cell WINMATCH sets g_eff to the")
    P("   arm's own gross, so the twin IS the arm, dSharpe is identically 0, and `win = dSharpe >")
    P("   TIE` scores it a LOSS.  FULLMATCH holds the twin at a different gross and returns a")
    P("   near-zero win.  FIRE-only drops those cells from both sides.")
    hw = cen[(cen.vintage == "TODAY") & (cen.scope == "POOLED") & (cen.window == W_HEAD)
             & (cen.step == S_HEAD) & (cen.rung == RUNG_HEAD)]
    nall = hw[(hw["pop"] == "ALL") & (hw.conv == "FULLMATCH")][["n_QROLL", "n_QEXP", "n_ABS"]].sum()
    nfire = hw[(hw["pop"] == "FIRE") & (hw.conv == "FULLMATCH")][["n_QROLL", "n_QEXP",
                                                                 "n_ABS"]].sum()
    P(f"\n   (arm, window) cell counts at the headline cell, TODAY, POOLED:")
    P(f"   {'family':<8} {'ALL':>9} {'FIRE':>9} {'never-fires':>12} {'share never':>12}")
    tot_a = tot_f = 0
    for f in FAMS:
        a, b = int(nall[f"n_{f}"]), int(nfire[f"n_{f}"])
        tot_a += a
        tot_f += b
        P(f"   {f:<8} {a:>9} {b:>9} {a-b:>12} {(a-b)/a if a else np.nan:>12.4f}")
    degen = (tot_a - tot_f) / tot_a
    P(f"   {'TOTAL':<8} {tot_a:>9} {tot_f:>9} {tot_a-tot_f:>12} {degen:>12.4f}")

    P(f"\n   the census on the FIRE-only population ({W_HEAD}d / step {S_HEAD} / {RUNG_HEAD:g} "
      f"bps / POOLED):")
    P(f"   {'vintage':<8} {'conv':<10} {'pop':<5} {'n':>4} {'exact':>8} {'QR>QE':>8} "
      f"{'QE>AB':>8} {'QR>AB':>8}")
    for vint, conv, pop in product(VINTAGES, CONVS, POPS):
        r = cell(vint, conv, pop=pop)
        if r is None:
            continue
        P(f"   {vint:<8} {conv:<10} {pop:<5} {int(r['n_win']):>4} {r['exact']:>8.4f} "
          f"{r['QR_gt_QE']:>8.4f} {r['QE_gt_AB']:>8.4f} {r['QR_gt_AB']:>8.4f}")
    fire_gap = abs(cell("TODAY", "FULLMATCH", pop="FIRE")["exact"]
                   - cell("TODAY", "WINMATCH", pop="FIRE")["exact"])
    all_gap = abs(t_f - t_w)
    P(f"\n   convention gap at the headline cell: ALL cells {all_gap:.4f}  ->  FIRE-only "
      f"{fire_gap:.4f}")

    P(f"\n   FIRE-only over all 9 (window, step) points, POOLED, {RUNG_HEAD:g} bps:")
    for vint in VINTAGES:
        g = grid[(grid.vintage == vint) & (grid.scope == "POOLED") & (grid["pop"] == "FIRE")
                 & (grid.rung == RUNG_HEAD)]
        P(f"     vintage {vint}")
        P("     " + g.pivot(index="window", columns=["conv", "step"], values="exact")
          .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n     "))

    # ================================================================== [3] rule 8
    P("\n" + "=" * 150)
    P("[3] PROTOCOL RULE 8")
    P("   (a) ON THE CLAIM: windows ending <= 2016-12-31 are IS; windows starting >= 2017-01-01")
    P("       are OOS, read once.  Parameters chosen on IS cannot see the OOS share.")
    cen["is_win"] = pd.to_datetime(cen["end"]) <= pd.Timestamp(IS_END)
    cen["oos_win"] = pd.to_datetime(cen["start"]) >= pd.Timestamp(OOS_START)
    wfc = []
    for (vint, conv, W, S, c, pop), g in cen[(cen.scope == "POOLED")].groupby(
            ["vintage", "conv", "window", "step", "rung", "pop"]):
        i, o = g[g.is_win], g[g.oos_win]
        wfc.append(dict(vintage=vint, conv=conv, window=W, step=S, rung=c, pop=pop,
                        n_IS=len(i), n_OOS=len(o),
                        IS_exact=float(i["exact"].mean()) if len(i) else np.nan,
                        OOS_exact=float(o["exact"].mean()) if len(o) else np.nan,
                        IS_QRgtQE=float(i["QR_gt_QE"].mean()) if len(i) else np.nan,
                        OOS_QRgtQE=float(o["QR_gt_QE"].mean()) if len(o) else np.nan))
    wfc = pd.DataFrame(wfc)
    wfc["gap"] = (wfc["OOS_exact"] - wfc["IS_exact"]).abs()
    P(f"\n   headline grid point ({W_HEAD}d / step {S_HEAD} / {RUNG_HEAD:g} bps, POOLED):")
    P("   " + wfc[(wfc.window == W_HEAD) & (wfc.step == S_HEAD) & (wfc.rung == RUNG_HEAD)]
      [["vintage", "conv", "pop", "n_IS", "n_OOS", "IS_exact", "OOS_exact", "gap",
        "IS_QRgtQE", "OOS_QRgtQE"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P(f"\n   worst |OOS - IS| over all 9 grid points x 3 rungs, per (vintage, conv, pop):")
    P("   " + wfc.groupby(["vintage", "conv", "pop"])["gap"].agg(["mean", "max"])
      .to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))

    # ---- (b) a book
    P("\n   (b) ON A BOOK: the IS rolling census picks the FAMILY (highest mean IS window win")
    P("       rate), IS Sharpe picks the ARM inside it, 2017-2026 is read once.")
    ARMS, SPY, REFS, SPL = [], {}, {}, {}
    for vint in VINTAGES:
        for Pk in CORP[vint]:
            t, sp, rf, spl = arm_table(vint, Pk)
            ARMS.append(t)
            SPY[(vint, Pk["panel"])] = sp
            REFS[(vint, Pk["panel"])] = rf
            SPL[(vint, Pk["panel"])] = spl
    arms = pd.concat(ARMS, ignore_index=True)

    picks = []
    for (vint, conv, W, S, c, pop), g in cen[(cen.scope != "POOLED")
                                             & (cen.scope != "POOLED_REPRO")].groupby(
            ["vintage", "conv", "window", "step", "rung", "pop"]):
        if pop != "ALL" or c != RUNG_HEAD:
            continue
        for panel, gp in g.groupby("scope"):
            i = gp[gp.is_win]
            if not len(i):
                continue
            famwin = {f: float(i[f"win_{f}"].mean()) for f in FAMS}
            fam = max(famwin, key=lambda k: famwin[k])
            pool = arms[(arms.vintage == vint) & (arms.panel == panel) & (arms.rung == c)
                        & (arms.family == fam)]
            if not len(pool):
                continue
            pick = pool.loc[pool["IS_Sharpe"].idxmax()]
            sp = SPY[(vint, panel)]
            v2 = REFS[(vint, panel)][c]["v2"]
            v1 = REFS[(vint, panel)][c]["v1"]
            # hindsight check: which family actually led OOS?
            o = gp[gp.oos_win]
            hfam = (max({f: float(o[f"win_{f}"].mean()) for f in FAMS}.items(),
                        key=lambda kv: kv[1])[0] if len(o) else "-")
            picks.append(dict(vintage=vint, conv=conv, window=W, step=S, rung=c, panel=panel,
                              IS_family=fam, OOS_family=hfam, same_family=bool(fam == hfam),
                              arm=pick["arm"], IS_Sharpe=pick["IS_Sharpe"],
                              OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                              OOS_MaxDD=pick["OOS_MaxDD"],
                              v2_OOS_Sharpe=fsharpe_of(v2), v2_OOS_CAGR=v2[3][0],
                              v2_OOS_MaxDD=v2[3][2], v1_OOS_Sharpe=fsharpe_of(v1),
                              spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_OOS_CAGR=sp["OOS"][0],
                              spy_OOS_MaxDD=sp["OOS"][2],
                              beats_v2=bool(pick["OOS_Sharpe"] > fsharpe_of(v2)),
                              beats_spy=bool(pick["OOS_Sharpe"] > sp["OOS_Sharpe"]),
                              p4b_OOS=bool(pick["OOS_Sharpe"] > sp["OOS_Sharpe"]
                                           and abs(pick["OOS_MaxDD"]) <= 0.60 * abs(sp["OOS"][2])
                                           and pick["OOS_CAGR"] >= 0.70 * sp["OOS"][0])))
    picks = pd.DataFrame(picks)
    P(f"\n   {len(picks)} (vintage x convention x grid point x panel) picks at {RUNG_HEAD:g} bps:")
    P("   " + picks.groupby(["vintage", "conv"]).agg(
        n=("panel", "size"), same_family=("same_family", "mean"),
        mean_OOS_Sharpe=("OOS_Sharpe", "mean"), mean_OOS_CAGR=("OOS_CAGR", "mean"),
        mean_OOS_MaxDD=("OOS_MaxDD", "mean"), beats_v2=("beats_v2", "mean"),
        beats_SPY=("beats_spy", "mean"), pass_4b_OOS=("p4b_OOS", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P("\n   comparands (OOS 2017-2026, 10 bps), per vintage x panel:")
    P(f"   {'vintage':<8} {'panel':<7} {'RULESv2 Sh':>11} {'RULESv1 Sh':>11} {'SPY Sh':>8} "
      f"{'SPY CAGR':>9} {'SPY MaxDD':>10}")
    for (vint, panel), rf in sorted(REFS.items()):
        sp = SPY[(vint, panel)]
        P(f"   {vint:<8} {panel:<7} {fsharpe_of(rf[RUNG_HEAD]['v2']):>11.4f} "
          f"{fsharpe_of(rf[RUNG_HEAD]['v1']):>11.4f} {sp['OOS_Sharpe']:>8.4f} "
          f"{sp['OOS'][0]:>9.2%} {sp['OOS'][2]:>10.2%}")

    # ================================================================== [4] KEEP paths
    P("\n" + "=" * 150)
    P("[4] BOTH KEEP PATHS on every arm x rung (reported in full, never selected on)")
    kp = arms.groupby(["vintage", "panel", "rung"]).agg(
        n=("p4a", "size"), pass_4a=("p4a", "sum"), pass_4b=("p4b", "sum")).reset_index()
    P("   " + kp.to_string(index=False).replace("\n", "\n   "))
    P(f"\n   TOTAL at {RUNG_HEAD:g} bps: 4a "
      f"{int(arms[(arms.rung == RUNG_HEAD) & (arms.vintage == 'TODAY')]['p4a'].sum())} of "
      f"{int((arms.rung == RUNG_HEAD).sum() // 2)}, 4b "
      f"{int(arms[(arms.rung == RUNG_HEAD) & (arms.vintage == 'TODAY')]['p4b'].sum())} "
      f"(TODAY corpus).")
    fl = arms[(arms.rung == RUNG_HEAD) & (arms.vintage == "TODAY")]["fail4b"].value_counts()
    P("   4b failure legs (TODAY, 10 bps): " + ", ".join(f"{k} x{v}" for k, v in fl.items()))

    cnd = arms[(arms.vintage == "TODAY") & (arms.panel == CAND["panel"])
               & (arms.family == CAND["family"]) & (arms.level == CAND["level"])
               & (arms.w == CAND["w"]) & (arms.depth == CAND["depth"])
               & (arms.cadence == CAND["cadence"]) & (arms.gross == CAND["gross"])]
    P("\n   the record's standing 4b candidate, re-read here for continuity (not proposed):")
    P("   " + cnd[["rung", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                   "OOS_MaxDD", "p4a", "p4b", "fail4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))

    # ================================================================== [5] verdict
    P("\n" + "=" * 150)
    P("[5] HYPOTHESES AND THE RECONCILED HEADLINES")
    step_span = max(abs(grid[(grid.vintage == v) & (grid.conv == cv) & (grid.scope == "POOLED")
                             & (grid["pop"] == "ALL") & (grid.rung == RUNG_HEAD)
                             & (grid.window == W)]["exact"].max()
                        - grid[(grid.vintage == v) & (grid.conv == cv) & (grid.scope == "POOLED")
                               & (grid["pop"] == "ALL") & (grid.rung == RUNG_HEAD)
                               & (grid.window == W)]["exact"].min())
                    for v, cv, W in product(VINTAGES, CONVS, WINDOWS))
    qrqe = min(cell(v, cv, pop=p)["QR_gt_QE"] for v, cv, p in product(VINTAGES, CONVS, POPS))
    wf_head = wfc[(wfc.window == W_HEAD) & (wfc.step == S_HEAD) & (wfc.rung == RUNG_HEAD)
                  & (wfc["pop"] == "ALL")]
    wf_gap = float(wf_head["gap"].max())
    book_ok = bool(picks["beats_v2"].mean() > 0.5 and picks["beats_spy"].mean() > 0.5)
    H = [
        ("GR1", "lane B 0.0847 reproduces (<=1e-4)", gr_ok["GR1"]),
        ("GR2", "cloud/_B2 0.3220 reproduces (<=1e-4)", gr_ok["GR2"]),
        ("GR3", "_B2 step-21 0.3125 reproduces (<=1e-4)", gr_ok["GR3"]),
        ("H_CONV", f"convention leg >= 0.15 on both vintages "
                   f"(ASOF {a_f-a_w:+.4f}, TODAY {t_f-t_w:+.4f})",
         bool(abs(a_f - a_w) >= 0.15 and abs(t_f - t_w) >= 0.15)),
        ("H_VINT", f"vintage leg <= 0.05 on both conventions "
                   f"(WINMATCH {t_w-a_w:+.4f}, FULLMATCH {t_f-a_f:+.4f})",
         bool(abs(t_w - a_w) <= 0.05 and abs(t_f - a_f) <= 0.05)),
        ("H_STEP", f"step span <= 0.10 at fixed (window, conv) — worst {step_span:.4f}",
         bool(step_span <= 0.10)),
        ("H_FIRE", f"conventions agree within 0.05 on FIRE-only cells — gap {fire_gap:.4f} "
                   f"(ALL-cells gap {all_gap:.4f})", bool(fire_gap <= 0.05)),
        ("H_DEGEN", f"never-firing cells >= 0.20 of the census — {degen:.4f}", bool(degen >= 0.20)),
        ("H_ONE", f"QROLL > QEXP >= 0.90 under both conventions — min {qrqe:.4f}",
         bool(qrqe >= 0.90)),
        ("H_WF", f"|OOS - IS| exact share <= 0.10 — worst {wf_gap:.4f}", bool(wf_gap <= 0.10)),
        ("H_BOOK", f"IS-selected book beats RULES v2 ({picks['beats_v2'].mean():.4f}) AND SPY "
                   f"({picks['beats_spy'].mean():.4f}) on OOS Sharpe", book_ok),
    ]
    P(f"   {'id':<9} {'bar':<78} verdict")
    for k, txt, ok in H:
        P(f"   {k:<9} {txt:<78} {'PASS' if ok else 'FAIL'}")
    P(f"\n   {sum(1 for _,_,o in H if o)} of {len(H)} pass.")

    P("\n   ONE RECONCILED HEADLINE PER CONVENTION (TODAY's corpus, 756d / step 63 / 10 bps,")
    P("   POOLED over three panels, the cell all three disputed runs share):")
    for conv in CONVS:
        rA, rF = cell("TODAY", conv), cell("TODAY", conv, pop="FIRE")
        P(f"     {conv:<10} ALL cells  exact {rA['exact']:.4f} ({int(round(rA['exact']*rA['n_win']))}"
          f" of {int(rA['n_win'])})   QR>QE {rA['QR_gt_QE']:.4f}  QE>AB {rA['QE_gt_AB']:.4f}")
        P(f"     {'':<10} FIRE only  exact {rF['exact']:.4f} ({int(round(rF['exact']*rF['n_win']))}"
          f" of {int(rF['n_win'])})   QR>QE {rF['QR_gt_QE']:.4f}  QE>AB {rF['QE_gt_AB']:.4f}")

    # ================================================================== outputs
    cen.to_csv(f"{OUT}.census.csv.gz", index=False)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    wfc.to_csv(f"{OUT}.walkforward.csv", index=False)
    picks.to_csv(f"{OUT}.picks.csv", index=False)
    arms.to_csv(f"{OUT}.arms.csv.gz", index=False)
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n   wrote census/grid/walkforward/picks/arms + console log.  {time.time()-t0:.1f}s")


def fsharpe_of(pack):
    """OOS Sharpe from an arm_table reference pack (h1, h2, maxdd, fmet(OOS), fmet(full))."""
    oc, os_, od = pack[3]
    return os_


if __name__ == "__main__":
    main()
