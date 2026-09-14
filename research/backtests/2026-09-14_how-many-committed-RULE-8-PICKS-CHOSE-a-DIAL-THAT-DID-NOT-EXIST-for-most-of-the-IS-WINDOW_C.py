#!/usr/bin/env python3
"""Idea 847 - how many committed RULE-8 PICKS chose a DIAL THAT DID NOT EXIST for most of the
IS WINDOW?   (lane C, 2026-09-14)

QUESTION (QUEUE idea 847, verbatim)
    idea 843 found the record's chooser is warm-up-blind: a live-leg chooser moves the w pick in
    82 of 108 QROLL cells and changes both KEEP-path counts (4b 68 -> 78, 4a 3 -> 0).  Census the
    committed walkforward CSVs for picks whose dial has a sub-1.0 IS live share, re-choose each on
    its own live leg, and report how many OOS reads move.  Max 2 params (pick set, liveness bar).

WHAT "LIVE SHARE" IS (843's definition, reused unchanged)
    A dial that is a ROLLING WINDOW of w observations has no threshold until w observations exist.
    Until then the gate multiplier is exactly 1.0 and the arm IS the ungated book (843's G6, proved
    bit-identically; G3 here re-proves it on this run's corpus).  For a pick made on an IS window of
    L scored days, LIVE SHARE = max(L - live_idx, 0) / L, where live_idx is the first scored day the
    threshold exists.  A pick with live share 0.13 was chosen on a window it did not exist for 87% of.

THE THREE LEGS (the first two are the census the queue asks for; the third is the price leg)
    LEG A  CENSUS.  Every committed research/backtests/*.csv that records a rule-8 pick is scanned
           for a dial that is a warm-up-bearing window length, and each such pick's IS live share is
           computed arithmetically from the panel's own scored calendar.  Nothing is re-run here;
           this is a count of what the record committed.
    LEG B  RE-CHOICE ON COMMITTED NUMBERS.  47 committed arm tables carry (window dial, IS_Sharpe,
           OOS_*) per arm, which is everything a BAR chooser needs.  Each cell is re-chosen with the
           dead dials removed and the committed OOS read of the new pick is compared with the
           committed OOS read of the old one.  These are the RECORD's own numbers, not this run's.
    LEG C  PRICE LEG / RULE 8 (mandatory).  LEG B cannot run a LIVELEG chooser, because no file but
           843's commits an IS-live-leg Sharpe.  So a corpus of warm-up-bearing arms is rebuilt from
           prices here - 843's QROLL family plus two more window-dial families - the dial is chosen
           on IS (<= 2016-12-31) under five choosers and OOS (2017-01-01..) is read exactly ONCE,
           reported as CAGR/Sharpe/MaxDD against RULES v2 (the live baseline) and SPY, with BOTH
           KEEP paths evaluated on every arm.  G4 gates this corpus against 843's COMMITTED
           walkforward picks, so LEG C contains the record's own cells and is not a private grid.

TUNED PARAMETERS: TWO, exactly the two the queue names.  Both apply to all three legs.
    (1) PICK SET   P1 / P2 / P3.
          LEG A/B  P1 NARROW  an explicitly window-named column (w, window, lookback, lb, W, ma,
                              span, halflife, vol_win, roll) whose picked value is an integer >= 20.
                   P2 MEDIUM  P1 plus lookback tokens embedded in a string dial (vol60-dg, ma200,
                              w1008, roll252, lb100 ...).
                   P3 WIDE    P2 plus any bare integer in 20..2520 appearing in a dial/pick column.
          LEG C    P1 QROLL only (843's family), P2 + VROLL, P3 + MAROLL.
    (2) LIVENESS BAR  0.50 / 0.90 / 1.00.  A pick is FLAGGED when its live share < bar; the BAR
          chooser is restricted to candidates with live share >= bar.
    3 x 3 = 9 points, ALL reported, on every leg.  The headline is declared as (P2, bar 0.90) for
    the census - P2 because it is the detector that reads a dial the way a human reader does, 0.90
    because bar 1.00 is degenerate (see H_CENSUS) - and (P3, LIVELEG) for the price leg, which is
    843's own chooser widened to every family this run can build.

REPORTED AXES, none of them a tune
    COST RUNG  {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.
    PANEL      U56 and B136 (both current-constituent lists).  SMALL663 is dropped from LEG C only
               for runtime; it is fully present in LEG A and LEG B, which read committed files.
    DEPTH {0.25, 0.50, 1.00}, CADENCE {D, W}, GROSS {0.75, 1.00} - 843's, unchanged.
    FAMILY     QROLL (843's breadth rolling-quantile), VROLL (panel realised-vol rolling-quantile),
               MAROLL (panel index vs its own w-day moving average).  All three are (level, w)
               families with a scalar gate, so the window dial is the only warm-up-bearing axis.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_CENSUS   at least 25% of ALL of the record's committed rule-8 pick values are warm-up-bearing,
               i.e. name a rolling window that did not exist for part of the IS window.
               [RESTATED BEFORE COMMIT, and the restatement is reported as such: the first draft of
               this hypothesis read "at least 25% of the picks WHOSE DIAL IS WARM-UP-BEARING have
               live share < 1.0", which is a tautology - a rolling window of w >= 20 observations
               on a window that starts at the panel's own start ALWAYS has live share < 1.0.  The
               run printed 236 of 236 (100.0%) and that number is a definition, not a measurement.
               The denominator is therefore every committed dial value, warm-up-bearing or not.
               The same construction makes LEG A's bar-1.00 column and LEG C's BAR100 chooser
               degenerate; both are still printed, and read as arithmetic rather than as evidence.]
    H_MOST     at least half of the warm-up-bearing picks are below 0.50 live share - i.e. the
               queue's title ("did not exist for MOST of the IS window") describes the typical
               flagged pick, not the extreme one.
    H_MOVEB    on the committed arm tables (LEG B) a bar-1.00 re-choice moves the pick in at least
               25% of re-choosable cells.
    H_OOSB     when a LEG B pick moves, the median |change in the committed OOS Sharpe| is >= 0.10.
    H_MOVEC    on the rebuilt corpus (LEG C) the LIVELEG chooser moves the w pick in at least 50%
               of cells, reproducing 843's 82-of-108 rate outside QROLL as well as inside it.
    H_GENERAL  the LEG C pick-move rate is family-invariant: max - min over the three families
               <= 25 percentage points.
    H_BETTER   the LIVELEG chooser is not merely different: its median OOS Sharpe >= BLIND's.
    H_KEEP     the chooser changes at least one KEEP-path count (4a or 4b) at the headline rung.
    H_EMPTY90  at bar 0.90 at least one LEG C cell has NO candidate at all (the pathological case:
               every dial on offer was dead for more than a tenth of the window it was chosen on).
               The bar-1.00 version of this is a construction fact, not a hypothesis, and is
               printed as CF_EMPTY100 instead.

GATES (printed first; no verdict is read until they are reported)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast CAGR/Sharpe/MaxDD reproduce engine.metrics to <= 1e-9 on a real series.
    G3 THE INERTNESS IDENTITY on this run's own corpus: before its threshold exists a window-dial
       arm's gate multiplier is exactly 1.0 and its daily return is BIT-IDENTICAL to the ungated
       book at the same gross.  max|d| must be exactly 0.0, on all three families.
    G4 this run's QROLL cells reproduce idea 843's COMMITTED .walkforward.csv picks and live shares
       on U56 and B136 (843's BLIND / LIVE50 / LIVELEG rows), and its .arms.csv Sharpes.
    G5 RULES v2 and SPY on U56 reproduce their committed triples (8.6282% / 1.2018 / -12.0549% and
       15.16% / 0.8861 / -33.72%).
    G6 the census detector scores a hand-written control set of dial strings, written BEFORE the
       census was run, with the expected warm-up for each.

SURVIVORSHIP, up front: U56 and B136 are CURRENT-constituent lists, so every LEVEL here is
    optimistic.  A pick-MOVE rate is a within-corpus agreement rate, which survivorship moves far
    less than a level, but no Sharpe or CAGR printed here is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt      full log
    .census.csv       LEG A - one row per committed pick the detector flags
    .recut.csv.gz     LEG B - one row per (file, cell, bar) re-choice on committed numbers
    .arms.csv         LEG C - one row per (panel, rung, family, level, w, depth, cadence, gross)
    .walkforward.csv  LEG C - the five choosers' rule-8 picks and their OOS reads vs v2 and SPY
    .grid.csv         the 9 tuned points x leg, every one printed
    .result.md        the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import re
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-14"
SLUG = "how-many-committed-RULE-8-PICKS-CHOSE-a-DIAL-THAT-DID-NOT-EXIST-for-most-of-the-IS-WINDOW"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
REF843 = HERE / "2026-09-12_is-the-QROLL-LOOKBACK-MONOTONICITY-a-WINDOW-fact-or-a-WARM-UP-fact_C"

# ---- 843's corpus constants, copied verbatim so G4 is a real reproduction --------------
FREQ = "W"
LAG = 1
MAX_VOL = 0.60
WARMUP = 260
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
WS_ROLL = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MINLEG = 252
PANELS = ["U56", "B136"]

# ---- this run's two extra window-dial families (same (level, w) shape) -----------------
WS_MA = [50, 100, 200, 400, 800]
BANDS = [0.00, 0.03, 0.06]
FAMS = ["QROLL", "VROLL", "MAROLL"]
VOL_WIN = 20

# ---- tuned dial 1 and 2 ---------------------------------------------------------------
PICKSETS = ["P1", "P2", "P3"]
PICKSET_FAMS = {"P1": ["QROLL"], "P2": ["QROLL", "VROLL"], "P3": FAMS}
BARS = [0.50, 0.90, 1.00]
PICKSET_HEAD_CENSUS, BAR_HEAD_CENSUS = "P2", 0.90
PICKSET_HEAD_PRICE, CHOOSER_HEAD = "P3", "LIVELEG"
CHOOSERS = ["BLIND", "BAR050", "BAR090", "BAR100", "LIVELEG"]
BAR_OF = {"BAR050": 0.50, "BAR090": 0.90, "BAR100": 1.00}

# committed reference triples for G5
PUB_V2 = (0.086282, 1.2018, -0.120549)
PUB_SPY = (0.1516, 0.8861, -0.3372)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (843's, verbatim)
def fast_run(prices, weights, mask, lag=LAG):
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
    return (pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx))


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
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def med(x):
    x = [v for v in x if v == v]
    return float(np.median(x)) if x else np.nan


# ------------------------------------------------------------------ primitives (843's)
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


def _cadence(m, idx):
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def gate_series(st, thr, depth, cadence, idx, side="lt"):
    """843's gate_series generalised to a side.  side='lt' with (breadth, rolling quantile) is
    843's function, argument for argument."""
    fire = (st < thr) if side == "lt" else (st > thr)
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    ok = st.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def panel(name):
    px = load_universe() if name == "U56" else load_universe(broad=True)
    return px.dropna(how="all").ffill()


# ============================================================ LEG A / B: the census detector
WINCOLS = {"w", "window", "win", "lookback", "lb", "l", "ma", "span", "halflife", "vol_win",
           "roll", "nwin", "window_days", "lookback_days", "ma_len", "n_days"}
DIALCOLS = {"pick", "dial", "arm", "book", "cell", "key", "selector", "param", "chosen",
            "family", "gate", "clause", "rule", "variant", "spec"}
METRIC_PREF = ("oos", "is_", "spy", "v1", "v2", "base", "ctl", "twin", "full", "cagr", "sharpe",
               "maxdd", "h1", "h2", "pass", "keep", "fail", "beat", "regret", "p4", "n_",
               "delta", "margin", "share", "rate", "p_", "med", "mean", "std", "min", "max")
CELLCOLS = {"panel", "universe", "scope", "rung", "cost", "cost_bps", "bps", "family", "gross",
            "depth", "cadence", "book", "conv", "selector", "grid", "level", "q", "band", "n",
            "k", "split", "chooser", "matching", "leg", "form", "state", "gate", "variant"}
MAXDIALVALS = 200        # a DIAL has few values; a free-text key column is not a dial
TOKEN = re.compile(r"(?:^|[^0-9a-z])(?:w|ma|sma|ema|vol|mom|roll|rw|lb|lookback|win|window)"
                   r"[ _\-]?(\d{2,4})(?![0-9])", re.I)
BARE = re.compile(r"(?:^|[^0-9.])(\d{2,4})(?![0-9.])")
WMIN, WMAX = 20, 2520

# G6 control set - written BEFORE the census was run
G6_CONTROLS = [
    ("vol60-dg", "P2", 60), ("ma200", "P2", 200), ("w1008", "P2", 1008), ("roll252", "P2", 252),
    ("lb100", "P2", 100), ("band3-rw", "P2", None), ("EWall", "P2", None), ("TOP20", "P2", None),
    ("0.08", "P2", None), ("SPY", "P2", None), ("season(21,14)", "P3", 21),
    ("g200-rw", "P3", 200), ("EWall", "P3", None), ("TOP20", "P3", 20), ("S2", "P3", None),
]


def dial_warmup(colname, value, pickset):
    """Warm-up in trading days implied by a committed dial, or None if the dial carries none.
    P1 narrow / P2 medium / P3 wide - the tuned PICK SET."""
    c = (colname or "").strip().lower()
    s = str(value).strip()
    if s in ("", "nan", "None", "-", "-none-"):
        return None
    if c in WINCOLS:
        try:
            v = float(s)
        except ValueError:
            v = None
        if v is not None and float(v).is_integer() and WMIN <= v <= WMAX:
            return int(v)
        if v is not None:
            return None                       # a numeric window dial out of range: not warm-up-bearing
    if pickset == "P1":
        return None
    m = TOKEN.search(s)
    if m and WMIN <= int(m.group(1)) <= WMAX:
        return int(m.group(1))
    if pickset == "P3" and (c in DIALCOLS or c in WINCOLS):
        b = BARE.findall(s)
        cand = [int(x) for x in b if WMIN <= int(x) <= WMAX]
        if cand:
            return max(cand)
    return None


def is_metric_col(c):
    cl = (c or "").strip().lower()
    return cl.startswith(METRIC_PREF) or cl in {"cagr", "sharpe", "maxdd", "turnover", "vol"}


# ------------------------------------------------------------------ main
def main():
    T0 = time.time()
    P(f"# Idea 847 - {SLUG}   (lane C, {DATE})")
    P("# QUESTION: how many of the record's committed rule-8 picks chose a dial that did not exist")
    P("#   for most of the IS window - and when they are re-chosen, how many OOS reads move?")
    P(f"# TUNED: pick set {PICKSETS} x liveness bar {BARS} = 9 points, ALL reported on every leg.")
    P(f"#   Declared headlines: census ({PICKSET_HEAD_CENSUS}, bar {BAR_HEAD_CENSUS:.2f}); "
      f"price leg ({PICKSET_HEAD_PRICE}, {CHOOSER_HEAD}).")
    P(f"# REPORTED AXES (not tunes): rung {RUNGS} bps (headline {RUNG_HEAD:g}), panel {PANELS},")
    P(f"#   depth {DEPTHS}, cadence {CADENCES}, gross {GROSSES}, family {FAMS}.")
    P("# SURVIVORSHIP: U56 and B136 are current-constituent lists; every LEVEL is optimistic and")
    P("#   no Sharpe or CAGR printed here is a capital claim.")

    # =================================================================== LEG C corpus (prices)
    armrows, wfrows = [], []
    PANDATA = {}
    P(f"\n{'='*118}\nLEG C - REBUILDING THE PRICE CORPUS\n{'='*118}")
    g3_max, g3_cells = 0.0, 0
    IS_LEN = {}
    for pname in PANELS:
        px = panel(pname)
        idx = px.index
        start = idx[WARMUP]
        eidx = px.loc[start:].index
        T = len(eidx)
        mask = rebalance_mask(idx, FREQ)
        elig = eligible_mask(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
        h = T // 2
        is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
        oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
        IS_LEN[pname] = is_end
        P(f"\nPANEL {pname}: {px.shape[1]-1} tradeable names, {T} scored days "
          f"{eidx[0].date()}..{eidx[-1].date()};  IS = {is_end} days to {IS_END}, "
          f"OOS = {T-oos0} days from {OOS_START}")

        # states
        br = breadth(px)
        ewret = px.drop(columns=["SPY"]).pct_change()
        ewret = ewret.mean(axis=1)
        vol = ewret.rolling(VOL_WIN).std() * np.sqrt(252.0)
        ewidx = (1.0 + ewret.fillna(0.0)).cumprod()

        base0 = {}
        for g in GROSSES:
            rg, tn = fast_run(px, ewall_weights(px, g, elig), mask)
            base0[g] = (rg.loc[start:].values, tn.loc[start:].values)

        if pname == "U56":
            P(f"\n{'-'*118}\nGATES G1, G2, G5\n{'-'*118}")
            Wb = ewall_weights(px, 0.75, elig)
            rg, tn = fast_run(px, Wb, mask)
            eng = backtest(px, Wb, cost_bps=10, freq=FREQ)
            g1 = float(np.abs(((rg - tn * 10 / 1e4) - eng["returns"]).loc[start:].values).max())
            P(f"   G1 fast_run == engine.backtest             max|d| {g1:.3e} "
              f"{'PASS' if g1 < 1e-9 else 'FAIL'}")
            assert g1 < 1e-9
            ser = pd.Series((rg - tn * 10 / 1e4).loc[start:].values)
            m = metrics(ser)
            fc, fs, fd = fmet(ser.values)
            g2 = max(abs(fc - m["CAGR"]), abs(fs - m["Sharpe"]), abs(fd - m["MaxDD"]))
            P(f"   G2 fast metrics == engine.metrics          max|d| {g2:.3e} "
              f"{'PASS' if g2 < 1e-9 else 'FAIL'}")
            assert g2 < 1e-9

        v2rg, v2tn = fast_run(px, rules_v2_weights(px), mask)
        v2rg, v2tn = v2rg.loc[start:].values, v2tn.loc[start:].values
        sc, ss, sd_ = fmet(spy)
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:]), sd_, sc)
        if pname == "U56":
            v2m = fmet(v2rg - v2tn * RUNG_HEAD / 1e4)
            d5 = max(abs(v2m[0] - PUB_V2[0]), abs(v2m[1] - PUB_V2[1]), abs(v2m[2] - PUB_V2[2]),
                     abs(sc - PUB_SPY[0]), abs(ss - PUB_SPY[1]), abs(sd_ - PUB_SPY[2]))
            P(f"   G5 RULES v2 {v2m[0]:.4%}/{v2m[1]:.4f}/{v2m[2]:.4%} vs committed "
              f"{PUB_V2[0]:.4%}/{PUB_V2[1]:.4f}/{PUB_V2[2]:.4%};  SPY {sc:.2%}/{ss:.4f}/{sd_:.2%} "
              f"vs {PUB_SPY[0]:.2%}/{PUB_SPY[1]:.4f}/{PUB_SPY[2]:.2%}  max|d| {d5:.3e} "
              f"{'PASS' if d5 < 5e-4 else 'FAIL'}")
            assert d5 < 5e-4
        P(f"   SPY {sc:.2%} / {ss:.3f} / {sd_:.2%};  4b bars: CAGR floor {0.70*sc:.2%}, "
          f"DD cap {-0.60*abs(sd_):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, "
          f"OOS {spy_pack[2]:.3f}")

        # ---- arms ----------------------------------------------------------------
        arms = ([("QROLL", q, w) for q in QS for w in WS_ROLL]
                + [("VROLL", q, w) for q in QS for w in WS_ROLL]
                + [("MAROLL", b, w) for b in BANDS for w in WS_MA])
        built = {}
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            if fam == "QROLL":
                st, thr, side = br, br.rolling(w, min_periods=w).quantile(lev), "lt"
            elif fam == "VROLL":
                st, thr, side = vol, vol.rolling(w, min_periods=w).quantile(1.0 - lev), "gt"
            else:
                st, thr, side = ewidx, ewidx.rolling(w, min_periods=w).mean() * (1.0 - lev), "lt"
            m = gate_series(st, thr, d, cad, idx, side)
            me = m.reindex(eidx).shift(1).fillna(1.0).values
            sw = np.abs(np.diff(me, prepend=me[0]))
            v = thr.reindex(eidx).shift(1).notna().values
            nz = np.flatnonzero(v)
            li = int(nz[0]) if len(nz) else T
            for g in GROSSES:
                r0, t0 = base0[g]
                rr = {c: me * r0 - (me * t0 + g * sw) * c / 1e4 for c in RUNGS}
                built[(fam, lev, w, d, cad, g)] = (rr, li, float(me.mean()))
                if li > 0:
                    dead = slice(0, li)
                    ung = r0[dead] - t0[dead] * RUNG_HEAD / 1e4
                    g3_max = max(g3_max, float(np.abs(rr[RUNG_HEAD][dead] - ung).max()),
                                 float(np.abs(me[dead] - 1.0).max()))
                    g3_cells += 1
        P(f"   {len(built)} arms built "
          + ", ".join(f"{f} {sum(1 for k in built if k[0]==f)}" for f in FAMS))

        for c in RUNGS:
            v2 = v2rg - v2tn * c / 1e4
            b1, b2, bdd = fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2]
            v2o = fmet(v2[oos0:])
            for (fam, lev, w, d, cad, g), (rr, li, gm) in built.items():
                ra = rr[c]
                ca, sa, da = fmet(ra)
                oc, os_, od = fmet(ra[oos0:])
                share = float(max(is_end - li, 0) / is_end) if is_end else np.nan
                isl = fsharpe(ra[li:is_end]) if is_end - li >= MINLEG else np.nan
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
                armrows.append(dict(
                    panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                    arm=f"{fam} L{lev} w{w} d{d:.2f} {cad} g{g:.2f}", mean_mult=gm,
                    live_idx=li, live_date=str(eidx[li].date()) if li < T else "never",
                    IS_live_share=share, IS_Sharpe=fsharpe(ra[:is_end]), IS_live_Sharpe=isl,
                    CAGR=ca, Sharpe=sa, MaxDD=da, H1=fsharpe(ra[:h]), H2=fsharpe(ra[h:]),
                    OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                    pass_4a=bool(fsharpe(ra[:h]) > b1 and fsharpe(ra[h:]) > b2 and da >= bdd),
                    pass_4b=all(t4b.values()),
                    fail_4b="+".join(k for k, v in t4b.items() if not v) or "-none-",
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_,
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_Sharpe=spy_pack[2],
                    SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    V2_Sharpe=fsharpe(v2), V2_OOS_CAGR=v2o[0], V2_OOS_Sharpe=v2o[1],
                    V2_OOS_MaxDD=v2o[2]))
        PANDATA[pname] = dict(is_end=is_end, T=T)
        del px, built

    P(f"\n   G3 inertness identity on {g3_cells} window-dial arms (all three families): "
      f"max|arm - ungated| on the dead region = {g3_max:.3e}  "
      f"{'PASS' if g3_max == 0.0 else 'FAIL'}")
    assert g3_max == 0.0

    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)

    # ---- the five choosers ---------------------------------------------------------
    for pname, c, fam, g, d, cad in product(PANELS, RUNGS, FAMS, GROSSES, DEPTHS, CADENCES):
        s = AR[(AR.panel == pname) & (AR.rung == c) & (AR.family == fam) & (AR.gross == g)
               & (AR.depth == d) & (AR.cadence == cad)]
        if s.empty:
            continue
        for ch in CHOOSERS:
            if ch == "BLIND":
                cand, col = s, "IS_Sharpe"
            elif ch == "LIVELEG":
                cand, col = s, "IS_live_Sharpe"
            else:
                cand, col = s[s.IS_live_share >= BAR_OF[ch]], "IS_Sharpe"
            cand = cand[cand[col].notna()]
            base = dict(panel=pname, rung=c, family=fam, gross=g, depth=d, cadence=cad, chooser=ch)
            if cand.empty:
                wfrows.append(dict(base, no_candidate=True, level=np.nan, w=np.nan))
                continue
            pk = cand.loc[cand[col].idxmax()]
            wfrows.append(dict(
                base, no_candidate=False, level=pk.level, w=pk.w,
                IS_live_share=pk.IS_live_share, IS_Sharpe=pk.IS_Sharpe,
                IS_live_Sharpe=pk.IS_live_Sharpe, CAGR=pk.CAGR, Sharpe=pk.Sharpe, MaxDD=pk.MaxDD,
                H1=pk.H1, H2=pk.H2, OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                OOS_MaxDD=pk.OOS_MaxDD, pass_4a=bool(pk.pass_4a), pass_4b=bool(pk.pass_4b),
                fail_4b=pk.fail_4b, SPY_OOS_CAGR=pk.SPY_OOS_CAGR, SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD, V2_OOS_CAGR=pk.V2_OOS_CAGR,
                V2_OOS_Sharpe=pk.V2_OOS_Sharpe, V2_OOS_MaxDD=pk.V2_OOS_MaxDD))
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- G4: reproduce 843's committed walkforward on U56 + B136 -------------------
    P(f"\n{'='*118}\nGATE G4 - does this run rebuild idea 843's COMMITTED QROLL picks?\n{'='*118}")
    g4 = "NO REFERENCE FILE"
    ref = Path(f"{REF843}.walkforward.csv")
    if ref.exists():
        R = pd.read_csv(ref)
        R = R[(R.family == "QROLL") & (R.panel.isin(PANELS)) & (~R.no_candidate.astype(bool))]
        R = R[R.chooser.isin(["BLIND", "LIVE50", "LIVELEG"])].copy()
        R["chooser"] = R.chooser.replace({"LIVE50": "BAR050"})
        k = ["panel", "rung", "family", "gross", "depth", "cadence", "chooser"]
        a = WF[(WF.family == "QROLL") & (~WF.no_candidate.astype(bool))
               & (WF.chooser.isin(["BLIND", "BAR050", "LIVELEG"]))].set_index(k).sort_index()
        b = R.set_index(k).sort_index()
        common = a.index.intersection(b.index)
        dw = int((a.loc[common, "w"].values != b.loc[common, "w"].values).sum())
        dl = int((a.loc[common, "level"].values != b.loc[common, "level"].values).sum())
        ds = float(np.abs(a.loc[common, "IS_live_share"].values
                          - b.loc[common, "IS_live_share"].values).max())
        do = float(np.abs(a.loc[common, "OOS_Sharpe"].values
                          - b.loc[common, "OOS_Sharpe"].values).max())
        ok = (dw == 0 and dl == 0 and ds < 1e-12 and do < 1e-9 and len(common) > 0)
        g4 = (f"{len(common)} common cells, w mismatches {dw}, level mismatches {dl}, "
              f"max|d live share| {ds:.3e}, max|d OOS Sharpe| {do:.3e} "
              f"{'PASS' if ok else 'FAIL'}")
        P(f"   G4 {g4}")
        assert ok, "G4 FAILED - this run does not rebuild 843's committed picks"
    else:
        P(f"   G4 {g4} ({ref.name} not found)")

    # ---- G6: the detector control set ---------------------------------------------
    P(f"\n{'='*118}\nGATE G6 - the census detector against its pre-written control set\n{'='*118}")
    g6_ok = 0
    for sval, ps, want in G6_CONTROLS:
        got = dial_warmup("pick", sval, ps)
        good = (got == want)
        g6_ok += int(good)
        P(f"   {ps} {sval!r:>18} -> {got}   expected {want}   {'ok' if good else 'MISMATCH'}")
    P(f"   G6 {g6_ok} of {len(G6_CONTROLS)} "
      f"{'PASS' if g6_ok == len(G6_CONTROLS) else 'FAIL'}")
    assert g6_ok == len(G6_CONTROLS)

    # =================================================================== LEG A: the census
    P(f"\n{'='*118}\nLEG A - CENSUS OF COMMITTED RULE-8 PICKS\n{'='*118}")
    IS_U56, IS_B136 = IS_LEN["U56"], IS_LEN["B136"]
    IS_DEFAULT = IS_U56

    def is_len_for(rowtext):
        t = (rowtext or "").lower()
        if "small" in t:
            return IS_U56          # the small panel shares the same calendar span (2009-2016)
        if "b136" in t or "broad" in t:
            return IS_B136
        return IS_DEFAULT

    files = sorted(set(list(HERE.glob("*.walkforward.csv")) + list(HERE.glob("*.wf.csv"))))
    P(f"   {len(files)} committed walkforward files under research/backtests/")
    crows = []
    TOT = {ps: dict(picks=0, rows=0, files=set()) for ps in PICKSETS}
    for f in files:
        try:
            hdr = [c.strip().strip('"') for c in f.open().readline().rstrip("\n").split(",")]
        except Exception as e:
            crows.append(dict(file=f.name, pickset="-", column="-", value="-", warmup=np.nan,
                              live_share=np.nan, note=f"UNREADABLE {type(e).__name__}"))
            continue
        if not any(c.lower() in WINCOLS | DIALCOLS and not is_metric_col(c) for c in hdr):
            continue
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception as e:                                       # unreadable, counted and skipped
            crows.append(dict(file=f.name, pickset="-", column="-", value="-", warmup=np.nan,
                              live_share=np.nan, note=f"UNREADABLE {type(e).__name__}"))
            continue
        if df.empty:
            continue
        has_oos = any(str(c).lower().startswith("oos") for c in df.columns)
        dialish = [c for c in df.columns
                   if str(c).strip().lower() in WINCOLS | DIALCOLS and not is_metric_col(c)
                   and df[c].nunique(dropna=True) <= MAXDIALVALS]
        if not dialish:
            continue
        panel_txt = ""
        for pc in ("panel", "universe", "scope"):
            if pc in df.columns:
                panel_txt = " ".join(str(v) for v in df[pc].astype(str).unique()[:5])
                break
        L = is_len_for(panel_txt + " " + f.name)
        for ps in PICKSETS:
            for c in dialish:
                vals = df[c].astype(str)
                for v, n in vals.value_counts().items():
                    if v.strip() in ("", "nan", "None", "-", "-none-"):
                        continue
                    TOT[ps]["picks"] += 1
                    TOT[ps]["rows"] += int(n)
                    TOT[ps]["files"].add(f.name)
                    wu = dial_warmup(c, v, ps)
                    if wu is None:
                        continue
                    crows.append(dict(file=f.name, pickset=ps, column=str(c), value=v,
                                      n_rows=int(n), warmup=int(wu),
                                      live_share=float(max(L - wu, 0) / L), IS_len=L,
                                      has_oos=has_oos, note=""))
    CEN = pd.DataFrame(crows)
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    bad = CEN[CEN.note.astype(str).str.startswith("UNREADABLE")] if len(CEN) else CEN
    P(f"   {len(bad)} unreadable files; {len(CEN) - len(bad)} (file, pickset, dial value) picks "
      f"detected as warm-up-bearing")

    gridrows = []
    P("\n   ALL committed dial values are the denominator.  WU = the detector calls the dial a")
    P("   rolling window; a WU dial ALWAYS has live share < 1.00, so the bar-1.00 column below is a")
    P("   definition and only the 0.90 and 0.50 bars are measurements.")
    P(f"\n   {'pickset':<9}{'bar':>6}{'files':>7}{'picks':>8}{'WU':>7}{'WU %':>8}{'rows':>9}"
      f"{'WU rows':>9}{'flagged':>9}{'flag %':>9}{'med share':>11}{'min share':>11}")
    for ps in PICKSETS:
        s = CEN[(CEN.pickset == ps) & (CEN.note == "")] if len(CEN) else CEN
        tot = TOT[ps]
        if not tot["picks"]:
            continue
        nrow = int(s.n_rows.sum()) if len(s) else 0
        wu_share = len(s) / tot["picks"]
        for bar in BARS:
            fl = s[s.live_share < bar] if len(s) else s
            gridrows.append(dict(leg="A", pickset=ps, bar=bar, files=len(tot["files"]),
                                 files_with_WU=int(s.file.nunique()) if len(s) else 0,
                                 picks=tot["picks"], rows=tot["rows"], WU=len(s), WU_rows=nrow,
                                 WU_share=wu_share, flagged=len(fl),
                                 flag_share_of_all=len(fl) / tot["picks"],
                                 flagged_rows=int(fl.n_rows.sum()) if len(fl) else 0,
                                 med_live=med(s.live_share) if len(s) else float("nan"),
                                 min_live=float(s.live_share.min()) if len(s) else float("nan")))
            P(f"   {ps:<9}{bar:>6.2f}{len(tot['files']):>7}{tot['picks']:>8}{len(s):>7}"
              f"{wu_share:>7.1%}{tot['rows']:>9}{nrow:>9}{len(fl):>9}"
              f"{len(fl)/tot['picks']:>8.1%}"
              f"{(med(s.live_share) if len(s) else float('nan')):>11.4f}"
              f"{(float(s.live_share.min()) if len(s) else float('nan')):>11.4f}")

    # =================================================================== LEG B: the re-choice
    P(f"\n{'='*118}\nLEG B - RE-CHOOSING COMMITTED ARM TABLES WITH THE DEAD DIALS REMOVED\n{'='*118}")
    P("   Every committed CSV that carries a window dial AND a per-arm IS_Sharpe AND an OOS read is")
    P("   re-chosen: cell = all non-dial, non-metric key columns; pick = argmax IS_Sharpe; the BAR")
    P("   chooser drops candidates whose live share is below the bar.  The OOS numbers compared are")
    P("   the ones the RECORD committed, not this run's.")
    rrows = []
    for f in sorted(HERE.glob("*.csv")):
        try:
            hdr = [c.strip().strip('"') for c in f.open().readline().rstrip("\n").split(",")]
        except Exception:
            continue
        hl = {c.lower() for c in hdr}
        if not ({"is_sharpe", "is_sharpe_full"} & hl) or "oos_sharpe" not in hl:
            continue
        if not (hl & WINCOLS):
            continue
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        cols = {str(c).strip().lower(): c for c in df.columns}
        isc = cols.get("is_sharpe") or cols.get("is_sharpe_full")
        oos = cols.get("oos_sharpe")
        if isc is None or oos is None or df.empty:
            continue
        dialcols = [c for c in df.columns if str(c).strip().lower() in WINCOLS]
        if not dialcols:
            continue
        panel_txt = ""
        for pc in ("panel", "universe", "scope"):
            if pc in df.columns:
                panel_txt = " ".join(str(v) for v in df[pc].astype(str).unique()[:5])
                break
        L = is_len_for(panel_txt + " " + f.name)
        for ps in PICKSETS:
            for dc in dialcols:
                wu = df[dc].map(lambda v: dial_warmup(dc, v, ps))
                if wu.notna().sum() == 0 or wu.nunique(dropna=True) < 2:
                    continue
                d2 = df.copy()
                d2["_wu"] = wu.fillna(0.0).astype(float)
                d2["_share"] = np.clip((L - d2["_wu"]) / L, 0.0, 1.0)
                d2["_is"] = pd.to_numeric(d2[isc], errors="coerce")
                d2["_oos"] = pd.to_numeric(d2[oos], errors="coerce")
                d2 = d2[d2["_is"].notna() & d2["_oos"].notna()]
                if d2.empty:
                    continue
                keys = [c for c in df.columns
                        if c != dc and not is_metric_col(c)
                        and str(c).strip().lower() in CELLCOLS
                        and d2[c].nunique(dropna=False) <= MAXDIALVALS]
                if not keys:
                    continue
                try:
                    grp = d2.groupby(keys, dropna=False, sort=False)
                except Exception:
                    continue
                for gk, s in grp:
                    if s[dc].nunique() < 2:
                        continue
                    blind = s.loc[s["_is"].idxmax()]
                    for bar in BARS:
                        cand = s[s["_share"] >= bar]
                        if cand.empty:
                            rrows.append(dict(file=f.name, pickset=ps, dial=dc, bar=bar,
                                              n_cand=len(s), moved=np.nan, empty=True,
                                              blind_dial=blind[dc], new_dial=np.nan,
                                              blind_share=float(blind["_share"]),
                                              blind_OOS=float(blind["_oos"]), new_OOS=np.nan,
                                              dOOS=np.nan))
                            continue
                        new = cand.loc[cand["_is"].idxmax()]
                        rrows.append(dict(file=f.name, pickset=ps, dial=dc, bar=bar,
                                          n_cand=len(s),
                                          moved=bool(str(new[dc]) != str(blind[dc])), empty=False,
                                          blind_dial=blind[dc], new_dial=new[dc],
                                          blind_share=float(blind["_share"]),
                                          blind_OOS=float(blind["_oos"]),
                                          new_OOS=float(new["_oos"]),
                                          dOOS=float(new["_oos"] - blind["_oos"])))
    RC = pd.DataFrame(rrows)
    RC.to_csv(f"{OUT}.recut.csv.gz", index=False, compression="gzip")
    P(f"\n   {RC.file.nunique() if len(RC) else 0} committed files re-choosable, "
      f"{len(RC)} (cell, bar, pickset) re-choices")
    P(f"\n   {'pickset':<9}{'bar':>6}{'cells':>8}{'empty':>7}{'moved':>7}{'move %':>9}"
      f"{'med |dOOS|':>12}{'max |dOOS|':>12}{'worse':>7}{'better':>8}")
    for ps in PICKSETS:
        for bar in BARS:
            s = RC[(RC.pickset == ps) & (RC.bar == bar)] if len(RC) else RC
            if not len(s):
                continue
            ne = s[~s["empty"].astype(bool)]
            mv = ne[ne["moved"].fillna(False).astype(bool)] if len(ne) else ne
            gridrows.append(dict(leg="B", pickset=ps, bar=bar, cells=len(s),
                                 empty=int(s["empty"].sum()), moved=len(mv),
                                 move_share=len(mv) / len(ne) if len(ne) else np.nan,
                                 med_abs_dOOS=med(mv.dOOS.abs()) if len(mv) else np.nan,
                                 max_abs_dOOS=float(mv.dOOS.abs().max()) if len(mv) else np.nan,
                                 worse=int((mv.dOOS < 0).sum()) if len(mv) else 0,
                                 better=int((mv.dOOS > 0).sum()) if len(mv) else 0))
            P(f"   {ps:<9}{bar:>6.2f}{len(s):>8}{int(s['empty'].sum()):>7}{len(mv):>7}"
              f"{(len(mv)/len(ne) if len(ne) else np.nan):>8.1%}"
              f"{(med(mv.dOOS.abs()) if len(mv) else np.nan):>12.4f}"
              f"{(float(mv.dOOS.abs().max()) if len(mv) else np.nan):>12.4f}"
              f"{(int((mv.dOOS<0).sum()) if len(mv) else 0):>7}"
              f"{(int((mv.dOOS>0).sum()) if len(mv) else 0):>8}")

    # =================================================================== LEG C: rule 8 report
    P(f"\n{'='*118}\nLEG C - PROTOCOL RULE 8 ON THE BOOKS (dial chosen on IS <= {IS_END}, "
      f"OOS read ONCE)\n{'='*118}")
    live = WF[~WF.no_candidate.astype(bool)]
    P(f"\n   per chooser, ALL panels and rungs, pick set {PICKSET_HEAD_PRICE} (every family):")
    P(f"   {'chooser':<9}{'cells':>7}{'empty':>7}{'4a':>5}{'4b':>5}{'med OOS CAGR':>14}"
      f"{'med OOS Sharpe':>16}{'med OOS MaxDD':>15}")
    for ch in CHOOSERS:
        s = live[live.chooser == ch]
        e = WF[(WF.chooser == ch) & (WF.no_candidate.astype(bool))]
        P(f"   {ch:<9}{len(s):>7}{len(e):>7}{int(s.pass_4a.sum()):>5}{int(s.pass_4b.sum()):>5}"
          f"{med(s.OOS_CAGR):>13.2%}{med(s.OOS_Sharpe):>16.3f}{med(s.OOS_MaxDD):>14.2%}")
    v2o = (med(AR.V2_OOS_CAGR), med(AR.V2_OOS_Sharpe), med(AR.V2_OOS_MaxDD))
    spyo = (med(AR.SPY_OOS_CAGR), med(AR.SPY_OOS_Sharpe), med(AR.SPY_OOS_MaxDD))
    P(f"   benchmarks on the same OOS window: RULES v2 {v2o[0]:.2%} / {v2o[1]:.3f} / {v2o[2]:.2%};"
      f"  SPY {spyo[0]:.2%} / {spyo[1]:.3f} / {spyo[2]:.2%}")

    P(f"\n   headline rung ({RUNG_HEAD:g} bps) only, per pick set x chooser:")
    P(f"   {'pickset':<9}{'chooser':<9}{'cells':>7}{'empty':>7}{'moved':>7}{'move %':>9}"
      f"{'4a':>5}{'4b':>5}{'med OOS Sharpe':>16}{'med |dOOS S|':>14}")
    head = WF[WF.rung == RUNG_HEAD]
    key = ["panel", "rung", "family", "gross", "depth", "cadence"]
    piv_w = head.pivot_table(index=key, columns="chooser", values="w", aggfunc="first")
    piv_s = head.pivot_table(index=key, columns="chooser", values="OOS_Sharpe", aggfunc="first")
    for ps in PICKSETS:
        fams = PICKSET_FAMS[ps]
        for ch in CHOOSERS:
            sel = [i for i in piv_w.index if i[2] in fams]
            sub_w, sub_s = piv_w.loc[sel], piv_s.loc[sel]
            if ch not in sub_w.columns:
                continue
            moved = (sub_w["BLIND"] != sub_w[ch]) & sub_w[ch].notna() & sub_w["BLIND"].notna()
            emp = int(sub_w[ch].isna().sum())
            dd = (sub_s[ch] - sub_s["BLIND"]).abs()
            s = head[(head.chooser == ch) & (head.family.isin(fams))
                     & (~head.no_candidate.astype(bool))]
            gridrows.append(dict(leg="C", pickset=ps, bar=BAR_OF.get(ch, np.nan), chooser=ch,
                                 cells=len(sub_w), empty=emp, moved=int(moved.sum()),
                                 move_share=float(moved.sum()) / max(len(sub_w) - emp, 1),
                                 pass_4a=int(s.pass_4a.sum()), pass_4b=int(s.pass_4b.sum()),
                                 med_OOS_Sharpe=med(s.OOS_Sharpe), med_OOS_CAGR=med(s.OOS_CAGR),
                                 med_OOS_MaxDD=med(s.OOS_MaxDD),
                                 med_abs_dOOS=med(dd[moved]) if moved.sum() else np.nan))
            P(f"   {ps:<9}{ch:<9}{len(sub_w):>7}{emp:>7}{int(moved.sum()):>7}"
              f"{float(moved.sum())/max(len(sub_w)-emp,1):>8.1%}"
              f"{int(s.pass_4a.sum()):>5}{int(s.pass_4b.sum()):>5}{med(s.OOS_Sharpe):>16.3f}"
              f"{(med(dd[moved]) if moved.sum() else np.nan):>14.4f}")

    P(f"\n   per family at {RUNG_HEAD:g} bps (H_GENERAL's evidence), chooser {CHOOSER_HEAD}:")
    P(f"   {'family':<8}{'cells':>7}{'moved':>7}{'move %':>9}{'med live share of BLIND pick':>31}"
      f"{'4b BLIND':>10}{'4b LIVELEG':>12}")
    fam_move = {}
    for fam in FAMS:
        sel = [i for i in piv_w.index if i[2] == fam]
        sw = piv_w.loc[sel]
        mv = (sw["BLIND"] != sw[CHOOSER_HEAD]) & sw[CHOOSER_HEAD].notna()
        fam_move[fam] = float(mv.sum()) / max(len(sw), 1)
        bl = head[(head.chooser == "BLIND") & (head.family == fam)]
        lv = head[(head.chooser == CHOOSER_HEAD) & (head.family == fam)]
        P(f"   {fam:<8}{len(sw):>7}{int(mv.sum()):>7}{fam_move[fam]:>8.1%}"
          f"{med(bl.IS_live_share):>31.4f}{int(bl.pass_4b.sum()):>10}{int(lv.pass_4b.sum()):>12}")

    P("\n   full-sample and halves of the chooser-selected books at the headline rung "
      "(PROTOCOL rule 4):")
    P(f"   {'chooser':<9}{'med CAGR':>10}{'med Sharpe':>12}{'med MaxDD':>11}{'med H1':>9}"
      f"{'med H2':>9}{'H1>SPY':>8}{'H2>SPY':>8}")
    spyh = AR.groupby("panel")[["SPY_CAGR", "SPY_Sharpe", "SPY_MaxDD"]].first()
    for ch in CHOOSERS:
        s = head[(head.chooser == ch) & (~head.no_candidate.astype(bool))]
        if not len(s):
            continue
        sb = s.panel.map(spyh.SPY_Sharpe)
        P(f"   {ch:<9}{med(s.CAGR):>9.2%}{med(s.Sharpe):>12.3f}{med(s.MaxDD):>10.2%}"
          f"{med(s.H1):>9.3f}{med(s.H2):>9.3f}"
          f"{int((s.H1 > sb).sum()):>8}{int((s.H2 > sb).sum()):>8}")
    P("   (H1>SPY / H2>SPY count cells whose half Sharpe beats SPY's FULL-sample Sharpe on the same"
      " panel; the 4b column above uses SPY's own per-half Sharpes, which is PROTOCOL 4b's bar)")

    P(f"\n   the single best-OOS-Sharpe pick per chooser at {RUNG_HEAD:g} bps (named so the "
      "leaderboard row is a BOOK, not a median):")
    for ch in CHOOSERS:
        s = head[(head.chooser == ch) & (~head.no_candidate.astype(bool))]
        if not len(s):
            P(f"   {ch:<9} no candidate")
            continue
        b = s.loc[s.OOS_Sharpe.idxmax()]
        P(f"   {ch:<9} {b.panel} {b.family} L{b.level} w{int(b.w)} d{b.depth:.2f} {b.cadence} "
          f"g{b.gross:.2f} | live share {b.IS_live_share:.4f} | FULL {b.CAGR:.2%}/{b.Sharpe:.3f}/"
          f"{b.MaxDD:.2%} halves {b.H1:.3f}/{b.H2:.3f} | OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.3f}/"
          f"{b.OOS_MaxDD:.2%} | 4a {bool(b.pass_4a)} 4b {bool(b.pass_4b)} (fail: {b.fail_4b})")
    P("   NOT a KEEP claim: these are de-grossing gate arms of the family idea 834/843 already"
      " committed and declined, and no matched-gross twin is computed here.")

    GR = pd.DataFrame(gridrows)
    GR.to_csv(f"{OUT}.grid.csv", index=False)

    # =================================================================== hypotheses
    P(f"\n{'='*118}\nPRE-REGISTERED HYPOTHESES\n{'='*118}")
    H = {}
    ch_cen = CEN[(CEN.pickset == PICKSET_HEAD_CENSUS) & (CEN.note == "")]
    tot_h = TOT[PICKSET_HEAD_CENSUS]["picks"]
    r_cen = len(ch_cen) / tot_h if tot_h else np.nan
    H["H_CENSUS"] = (r_cen >= 0.25,
                     f"{len(ch_cen)} of {tot_h} committed dial values at {PICKSET_HEAD_CENSUS} "
                     f"({r_cen:.1%}) are warm-up-bearing, over "
                     f"{ch_cen.file.nunique()} of {len(TOT[PICKSET_HEAD_CENSUS]['files'])} files "
                     f"(degenerate first draft: {len(ch_cen)} of {len(ch_cen)} of THOSE have live "
                     f"share < 1.00, by construction)")
    below = ch_cen[ch_cen.live_share < 0.50]
    r_most = len(below) / len(ch_cen) if len(ch_cen) else np.nan
    H["H_MOST"] = (r_most >= 0.50,
                   f"{len(below)} of {len(ch_cen)} warm-up-bearing picks ({r_most:.1%}) are below "
                   f"0.50 live share; {int((ch_cen.live_share < BAR_HEAD_CENSUS).sum())} "
                   f"({(ch_cen.live_share < BAR_HEAD_CENSUS).mean():.1%}) are below the "
                   f"{BAR_HEAD_CENSUS:.2f} headline bar")
    sb = RC[(RC.pickset == PICKSET_HEAD_CENSUS) & (RC.bar == 1.00)] if len(RC) else RC
    nb = sb[~sb["empty"].astype(bool)] if len(sb) else sb
    mb = nb[nb.moved.astype(bool)] if len(nb) else nb
    r_b = len(mb) / len(nb) if len(nb) else np.nan
    H["H_MOVEB"] = (r_b >= 0.25,
                    f"bar-1.00 re-choice on committed tables moves {len(mb)} of {len(nb)} cells "
                    f"({r_b:.1%}); {int(sb['empty'].sum())} cells have no live candidate")
    md = med(mb.dOOS.abs()) if len(mb) else np.nan
    H["H_OOSB"] = (md >= 0.10 if md == md else False,
                   f"median |d committed OOS Sharpe| over moved cells {md:.4f} "
                   f"(worse {int((mb.dOOS<0).sum()) if len(mb) else 0} / "
                   f"better {int((mb.dOOS>0).sum()) if len(mb) else 0})")
    swc = piv_w
    mvc = (swc["BLIND"] != swc[CHOOSER_HEAD]) & swc[CHOOSER_HEAD].notna()
    r_c = float(mvc.sum()) / max(len(swc), 1)
    H["H_MOVEC"] = (r_c >= 0.50,
                    f"LIVELEG moves the w pick in {int(mvc.sum())} of {len(swc)} cells "
                    f"({r_c:.1%}) at {RUNG_HEAD:g} bps over all three families")
    spread = max(fam_move.values()) - min(fam_move.values())
    H["H_GENERAL"] = (spread <= 0.25,
                      "move rate " + ", ".join(f"{f} {fam_move[f]:.1%}" for f in FAMS)
                      + f"; spread {spread:.1%}")
    bl_s = med(head[(head.chooser == "BLIND") & (~head.no_candidate.astype(bool))].OOS_Sharpe)
    lv_s = med(head[(head.chooser == CHOOSER_HEAD)
                    & (~head.no_candidate.astype(bool))].OOS_Sharpe)
    H["H_BETTER"] = (lv_s >= bl_s,
                     f"median OOS Sharpe BLIND {bl_s:.4f} vs {CHOOSER_HEAD} {lv_s:.4f} "
                     f"(d {lv_s-bl_s:+.4f})")
    k4 = {ch: (int(head[(head.chooser == ch) & (~head.no_candidate.astype(bool))].pass_4a.sum()),
               int(head[(head.chooser == ch) & (~head.no_candidate.astype(bool))].pass_4b.sum()))
          for ch in CHOOSERS}
    H["H_KEEP"] = (any(k4[ch] != k4["BLIND"] for ch in CHOOSERS),
                   "4a/4b at " + f"{RUNG_HEAD:g} bps: "
                   + ", ".join(f"{ch} {k4[ch][0]}/{k4[ch][1]}" for ch in CHOOSERS))
    emp90 = int(WF[(WF.chooser == "BAR090") & (WF.no_candidate.astype(bool))].shape[0])
    H["H_EMPTY90"] = (emp90 >= 1,
                      f"{emp90} of {len(WF[WF.chooser=='BAR090'])} cells have NO candidate at "
                      f"bar 0.90")
    npass = sum(1 for v in H.values() if v[0])
    P(f"   {npass} of {len(H)} PASS\n")
    for k, (v, why) in H.items():
        P(f"   {k:<11}{'PASS' if v else 'FAIL':<6}{why}")
    emp100 = int(WF[(WF.chooser == "BAR100") & (WF.no_candidate.astype(bool))].shape[0])
    P(f"\n   CF_EMPTY100 (construction fact, not a hypothesis): {emp100} of "
      f"{len(WF[WF.chooser=='BAR100'])} cells have NO fully-live candidate at bar 1.00 - every "
      f"rolling dial in this corpus carries warm-up, so a fully-live-only chooser cannot pick.")

    P(f"\n   elapsed {time.time()-T0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return H


if __name__ == "__main__":
    main()
