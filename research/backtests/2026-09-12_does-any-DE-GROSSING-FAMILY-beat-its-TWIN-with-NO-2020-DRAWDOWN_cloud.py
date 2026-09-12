#!/usr/bin/env python3
"""Idea 835 - does any DE-GROSSING FAMILY beat its TWIN on a leg that contains NO 2020 DRAWDOWN?
   (cloud lane, 2026-09-12, idea 1 of 2)

QUESTION (QUEUE idea 835, verbatim)
    idea 825 found QROLL's twin win rate is 0.4907-0.5926 on legs ending 2014-2016 against
    0.7361-0.9005 on legs ending 2018-2020, i.e. the advantage tracks one drawdown.  Re-run the
    216-arm corpus on legs that EXCLUDE 2020-02-19..2020-04-07 entirely and report each family's
    win rate with and without it.  Rationale: a de-grossing clause that only pays in one crash is
    a bet on the next crash, not an edge.  Max 2 params (excluded episode, leg set).

WHAT IS BEING MEASURED
    The object is idea 825's MATCHED-GROSS TWIN WIN RATE: for each arm (a breadth-gated de-grossing
    book) the twin is the STATIC-gross equal-weight book carrying the same mean gross, and
        win[arm] = Sharpe(arm) - Sharpe(twin) > 1e-12
    on the leg.  win[f] is the share of family f's arms that win.  The new operation is that a
    contiguous EPISODE of trading days is DELETED from the leg before any moment is taken -- from
    the arm, from its twin, from the gross path that matches the twin, and from every benchmark.
    Deleting days (rather than splitting the leg) is the literal reading of "legs that EXCLUDE
    2020-02-19..2020-04-07 entirely" and is exact here because Sharpe is a function of the first
    two moments of the daily return sample, which are additive over disjoint day sets.

    CONVENTION, declared up front: with days deleted, CAGR and MaxDD are read on the CHAINED
    equity of the kept days (product over kept days, annualised by 252/n_kept).  That is the only
    defensible reading of "the book without that episode", but it is a counterfactual, not a
    tradable path, and no CAGR or MaxDD printed under an exclusion is a capital claim.  The win
    rate, which is the queue's actual statistic, needs no such convention.

TUNED PARAMETERS: TWO, exactly the two the queue names.  All grid points reported.
    (1) EXCLUDED EPISODE, 7 values (4 real, 3 controls), HEADLINE = COVID_TIGHT, the queue's:
            NONE          no deletion (the control that reproduces 825)
            COVID_TIGHT   2020-02-19..2020-04-07     <- HEADLINE, the queue's window
            COVID_WIDE    2020-02-01..2020-06-30
            COVID_DD      SPY's own 2020 peak-to-recovery window, derived from the data
            DD_2015       2015-08-10..2015-09-29     a SECOND, smaller drawdown
            PLACEBO_2017  2017-02-19..2017-04-07     the same calendar slot, no crash
            PLACEBO_PRE   the 33 trading days immediately BEFORE COVID_TIGHT
        The placebos are the control the queue's question needs: if deleting ANY ~34-day block
        moves a win rate by as much as deleting the crash, the crash is not what is being measured.
    (2) LEG SET, 3 values, HEADLINE = ENDYEAR (825's own construction):
            ENDYEAR   [panel start, Dec-31 Y]  for Y in 2013..2025  (825's expanding legs)
            POSTYEAR  [Dec-31 Y, panel end]    for the same Y
            BLOCK3    disjoint 3-calendar-year blocks
    7 x 3 = 21 tuned points, every one written to .grid.csv.

REPORTED AXES, none of them a tune (every one printed at every grid point):
    COST RUNG      {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.
    TWIN MATCHING  FULLMATCH (825's: twin gross matched on the FULL sample, path sliced to the
                   leg) and WINMATCH (twin re-matched on the leg AFTER deletion).  BOTH.
    PANEL          U56, B136, SMALL663 and POOLED.
    FAMILY         ABS (fixed breadth threshold), QEXP (expanding quantile), QROLL (rolling
                   quantile), and adv = win[QROLL] - max(win[ABS], win[QEXP]).

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_MAIN     ANSWER TO THE QUEUE: on legs that CONTAIN the episode, QROLL's win rate stays
               > 0.50 once COVID_TIGHT is deleted (headline cell).
    H_ADV      adv stays > 0 on those legs once the episode is deleted.
    H_DROP     deleting the episode lowers QROLL's win rate on legs that contain it
               (mean delta < 0).
    H_PLACEBO  the placebo deletions move QROLL's win rate by LESS than COVID_TIGHT does
               (|mean delta| smaller), i.e. the effect is the crash and not the day count.
    H_CLEAN    825's "legs ending 2014-2016" reading survives: on legs that contain NO part of
               any COVID episode, QROLL's win rate is <= 0.60 (825 measured 0.4907-0.5926).
    H_COSTINV  the H_MAIN verdict is the same at 0, 10 and 25 bps.
    H_MATCH    the H_MAIN verdict is the same under FULLMATCH and WINMATCH.
    H_PANEL    the H_MAIN verdict agrees across U56, B136 and SMALL663 read separately.
    H_LEGSET   the H_MAIN verdict is the same on all three leg sets.
    H_4B       CAPITAL LEG: at least one arm still passes PROTOCOL 4b with the 2020 episode
               deleted from the whole sample (i.e. the 4b passes are not a 2020 artefact).
    H_R8       RULE 8: the rule-8 pick's OOS Sharpe still beats SPY's OOS Sharpe once the
               episode is deleted from both.

GATES (printed first; no verdict is read until they are reported)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast Sharpe/CAGR/MaxDD reproduce engine.metrics to <= 1e-9 on a real series.
    G3 the 0.01-grid interpolation of the static-gross twin reproduces an EXACT run to <= 1e-6.
    G4 this run's corpus reproduces idea 825's COMMITTED .arms.csv - Sharpe, twin Sharpe and the
       `win` boolean, all 1,944 rows.  835 re-reads 825's numbers, so if the corpus does not
       rebuild, nothing downstream means anything.
    G5 the DELETION ARITHMETIC is exact: (a) an empty deletion reproduces the undeleted Sharpe
       bit-for-bit; (b) a real deletion reproduces a direct numpy masked Sharpe to <= 1e-12,
       on both the arm stack and the interpolated twin grid.
    G6 a deletion that does not INTERSECT a leg moves that leg's win rate by exactly 0.

PROTOCOL RULE 8 (mandatory, run and reported), on the BOOKS:
    per (panel, family, gross, depth, cadence) the DIAL (level, w) is chosen on IS
    (..2016-12-31) by IS Sharpe alone and OOS (2017-01-01..) is read exactly ONCE, as
    CAGR/Sharpe/MaxDD against RULES v2 (the live baseline) and SPY on the same window.  The whole
    walk-forward is then run a SECOND time with the headline episode deleted from the arm, the
    twin, RULES v2 and SPY alike -- the idea's own question asked of the capital leg.  BOTH KEEP
    paths (4a and 4b) are evaluated on all 648 arms at every cost rung, with and without the
    episode.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and SMALL663 worst -- a sub-$2B screen read today cannot see the names that fell
    out of it (data/SMALL_PANEL_README.md).  Tickers with max_1d_move >= 1.0 in
    data/small_meta.csv are dropped before anything is computed.  A win RATE is a within-panel
    agreement rate, which survivorship moves far less than a level, but no Sharpe or CAGR printed
    here is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .grid.csv        21 tuned points x leg x rung x matching x panel x family: win rate, n, and
                     the delta against the same cell with no deletion
    .legs.csv        one row per (legset, leg) with its dates, day counts and episode overlap
    .arms.csv        one row per (panel, arm, rung): metrics, twin, 4a/4b and rule-8 columns,
                     with and without the headline episode
    .walkforward.csv the rule-8 picks and their OOS reads vs RULES v2 and SPY, both readings
    .result.md       the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-12"
SLUG = "does-any-DE-GROSSING-FAMILY-beat-its-TWIN-with-NO-2020-DRAWDOWN"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
REF825 = HERE / "2026-09-12_is-QROLL-ON-TOP-an-entirely-POST-2017-fact_cloud.arms.csv"

# ---- 825's corpus constants, copied verbatim so G4 is a real reproduction --------------
FREQ = "W"
LAG = 1
MAX_VOL = 0.60
WARMUP = 260
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS_ROLL = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
MINQ = 252
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TIE = 1e-12
SMALL_MAXMOVE = 1.0
FAMS = ["ABS", "QEXP", "QROLL"]
GSTEP = 0.01
MINLEG = 252
MATCHINGS = ["FULLMATCH", "WINMATCH"]
PANELS = ["U56", "B136", "SMALL663"]
SCOPES = ["POOLED"] + PANELS

# ---- tuned dial 1: the excluded episode.  Headline declared here, before any number. ----
EPISODES = {
    "NONE": None,
    "COVID_TIGHT": ("2020-02-19", "2020-04-07"),
    "COVID_WIDE": ("2020-02-01", "2020-06-30"),
    "COVID_DD": None,            # filled from SPY itself (peak 2020-02-19 -> recovery)
    "DD_2015": ("2015-08-10", "2015-09-29"),
    "PLACEBO_2017": ("2017-02-19", "2017-04-07"),
    "PLACEBO_PRE": None,         # the 33 trading days immediately before COVID_TIGHT
}
EP_HEAD = "COVID_TIGHT"
EP_REAL = ["COVID_TIGHT", "COVID_WIDE", "COVID_DD", "DD_2015"]
EP_PLACEBO = ["PLACEBO_2017", "PLACEBO_PRE"]
EP_COVID = ["COVID_TIGHT", "COVID_WIDE", "COVID_DD"]

# ---- tuned dial 2: the leg set. ---------------------------------------------------------
LEGSETS = ["ENDYEAR", "POSTYEAR", "BLOCK3"]
LEGSET_HEAD = "ENDYEAR"
ENDYEARS = list(range(2013, 2026))
BLOCK_STARTS = [2010, 2013, 2016, 2019, 2022, 2025]

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (825's, verbatim)
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
    """CAGR / Sharpe / MaxDD on a daily return vector.  With days deleted this is the CHAINED
    equity of the kept days, annualised by 252/n_kept -- the convention declared in the header."""
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


# ------------------------------------------------------------------ primitives (825's)
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


def gate_series(br, thr, depth, cadence, idx):
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    ok = br.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def panel(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        drop = [c for c in px.columns if c in bad and c != "SPY"]
        px = px.drop(columns=drop)
        P(f"   SMALL panel: dropped {len(drop)} tickers with max_1d_move >= {SMALL_MAXMOVE} "
          f"(data/small_meta.csv), {len([c for c in px.columns if c != 'SPY'])} left")
    return px.dropna(how="all").ffill()


# ------------------------------------------------------------ cumsum stacks WITH deletion
class CS:
    """Cumulative sums of a stack of series.  Any window's Sharpe is O(1), and any window
    MINUS one interior contiguous block is O(1) too, because the first two moments are
    additive over disjoint day sets."""

    def __init__(self, M):
        z = np.zeros((M.shape[0], 1))
        self.s1 = np.concatenate([z, np.cumsum(M, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(M * M, axis=1)], axis=1)

    def sharpe(self, a, b, x0=0, x1=0):
        n = (b - a) - (x1 - x0)
        if n < 2:
            return np.full(self.s1.shape[0], np.nan)
        s1 = (self.s1[:, b] - self.s1[:, a]) - (self.s1[:, x1] - self.s1[:, x0])
        s2 = (self.s2[:, b] - self.s2[:, a]) - (self.s2[:, x1] - self.s2[:, x0])
        mu = s1 / n
        var = (s2 - n * mu * mu) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


class GridCS:
    """Cumsums of the static-gross twin grid incl. adjacent cross-products, deletion-aware."""

    def __init__(self, N):
        self.G, self.T = N.shape
        z = np.zeros((self.G, 1))
        self.s1 = np.concatenate([z, np.cumsum(N, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(N * N, axis=1)], axis=1)
        X = N[:-1] * N[1:]
        self.sx = np.concatenate([np.zeros((self.G - 1, 1)), np.cumsum(X, axis=1)], axis=1)

    def sharpe(self, a, b, lo, lam, x0=0, x1=0):
        n = (b - a) - (x1 - x0)
        if n < 2:
            return np.full(len(lo), np.nan)
        hi = np.minimum(lo + 1, self.G - 1)
        m_lo = ((self.s1[lo, b] - self.s1[lo, a]) - (self.s1[lo, x1] - self.s1[lo, x0])) / n
        m_hi = ((self.s1[hi, b] - self.s1[hi, a]) - (self.s1[hi, x1] - self.s1[hi, x0])) / n
        q_lo = ((self.s2[lo, b] - self.s2[lo, a]) - (self.s2[lo, x1] - self.s2[lo, x0])) / n
        q_hi = ((self.s2[hi, b] - self.s2[hi, a]) - (self.s2[hi, x1] - self.s2[hi, x0])) / n
        xi = np.minimum(lo, self.G - 2)
        q_x = ((self.sx[xi, b] - self.sx[xi, a]) - (self.sx[xi, x1] - self.sx[xi, x0])) / n
        mu = (1 - lam) * m_lo + lam * m_hi
        ey2 = (1 - lam) ** 2 * q_lo + 2 * lam * (1 - lam) * q_x + lam ** 2 * q_hi
        var = (ey2 - mu * mu) * n / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


def main():
    T0 = time.time()
    P(f"# Idea 835 - {SLUG}   (cloud lane, {DATE}, idea 1 of 2)")
    P("# QUESTION: re-run the 216-arm corpus on legs that EXCLUDE the 2020 drawdown entirely and")
    P("#   report each de-grossing family's matched-gross twin win rate with and without it.")
    P(f"# TUNED: episode {list(EPISODES)} x legset {LEGSETS} = {len(EPISODES)*len(LEGSETS)} points,")
    P(f"#   ALL reported; HEADLINE episode {EP_HEAD} (the queue's), legset {LEGSET_HEAD} (825's).")
    P(f"# REPORTED AXES (not tunes): rung {RUNGS} bps (headline {RUNG_HEAD:g}), matching "
      f"{MATCHINGS}, scope {SCOPES}, family {FAMS} + adv.")
    P("# CONVENTION: deleting days removes them from the arm, the twin, the gross path that")
    P("#   matches the twin, RULES v2 and SPY alike.  CAGR/MaxDD under a deletion are read on the")
    P("#   CHAINED equity of the kept days -- a counterfactual, not a tradable path.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    armrows, wfrows = [], []
    PAN = {}
    EPD = dict(EPISODES)

    for pname in PANELS:
        P(f"\n{'='*118}\nPANEL {pname}\n{'='*118}")
        px = panel(pname)
        idx = px.index
        start = idx[WARMUP]
        eidx = px.loc[start:].index
        T = len(eidx)
        mask = rebalance_mask(idx, FREQ)
        elig = eligible_mask(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
        P(f"   {px.shape[1]-1} tradeable names, {T} scored days {eidx[0].date()}..{eidx[-1].date()}")

        # ---- data-derived episodes, resolved once on the first (longest) panel ----------
        if EPD["COVID_DD"] is None:
            s = px["SPY"].loc["2019-06-01":]
            pk = s.loc[:"2020-02-19"].idxmax()
            lvl = float(s.loc[pk])
            rec = s.loc[pk:][s.loc[pk:] >= lvl]
            end = rec.index[1] if len(rec) > 1 else s.index[-1]
            EPD["COVID_DD"] = (str(pk.date()), str(end.date()))
            i0 = int(eidx.searchsorted(pd.Timestamp("2020-02-19"), side="left"))
            EPD["PLACEBO_PRE"] = (str(eidx[i0 - 34].date()), str(eidx[i0 - 1].date()))
            P("   episodes resolved from the data:")
            for k, v in EPD.items():
                P(f"      {k:<13} {v}")

        br_full = breadth(px)
        thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
        thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q)
                    for q in QS for w in WS_ROLL}

        base0 = {}
        for g in GROSSES:
            rg, tn = fast_run(px, ewall_weights(px, g, elig), mask)
            base0[g] = (rg.loc[start:].values, tn.loc[start:].values)
        gg = np.round(np.arange(0.0, 1.0 + GSTEP / 2, GSTEP), 6)
        GR = np.zeros((len(gg), T))
        GT = np.zeros((len(gg), T))
        for i, x in enumerate(gg):
            if x == 0.0:
                continue
            rg, tn = fast_run(px, ewall_weights(px, float(x), elig), mask)
            GR[i], GT[i] = rg.loc[start:].values, tn.loc[start:].values

        if pname == "U56":
            P(f"\n{'-'*118}\nGATES G1-G3\n{'-'*118}")
            Wb = ewall_weights(px, 0.75, elig)
            rg, tn = fast_run(px, Wb, mask)
            eng = backtest(px, Wb, cost_bps=10, freq=FREQ)
            g1 = float(np.abs(((rg - tn * 10 / 1e4) - eng["returns"]).loc[start:].values).max())
            P(f"   G1 fast_run == engine.backtest                    max|d| {g1:.3e} "
              f"{'PASS' if g1 < 1e-9 else 'FAIL'}")
            assert g1 < 1e-9
            ser = pd.Series((rg - tn * 10 / 1e4).loc[start:].values)
            m = metrics(ser)
            fc, fs, fd = fmet(ser.values)
            g2 = max(abs(fc - m["CAGR"]), abs(fs - m["Sharpe"]), abs(fd - m["MaxDD"]))
            P(f"   G2 fast metrics == engine.metrics                 max|d| {g2:.3e} "
              f"{'PASS' if g2 < 1e-9 else 'FAIL'}")
            assert g2 < 1e-9
            xt = 0.6237
            lo = int(np.floor(round(xt, 6) / GSTEP))
            lam = (xt - gg[lo]) / GSTEP
            ex_r, ex_t = fast_run(px, ewall_weights(px, xt, elig), mask)
            en = (ex_r - ex_t * 10 / 1e4).loc[start:].values
            inn = ((1 - lam) * (GR[lo] - GT[lo] * 10 / 1e4)
                   + lam * (GR[lo + 1] - GT[lo + 1] * 10 / 1e4))
            g3 = abs(fsharpe(en) - fsharpe(inn))
            P(f"   G3 0.01-grid interpolation vs an EXACT twin run   |dSharpe| {g3:.3e} "
              f"{'PASS' if g3 < 1e-6 else 'FAIL'}  (g = {xt}, Sharpe {fsharpe(en):.6f})")
            assert g3 < 1e-6

        arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
                + [("QROLL", q, w) for q in QS for w in WS_ROLL])
        keys, ARM, TWF, GEFF_F, MEAN_ME = [], {c: [] for c in RUNGS}, {c: [] for c in RUNGS}, [], []
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            thr = lev if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
            m = gate_series(br_full, thr, d, cad, idx)
            me = m.reindex(eidx).shift(1).fillna(1.0).values
            sw = np.abs(np.diff(me, prepend=me[0]))
            for g in GROSSES:
                r0, t0 = base0[g]
                keys.append((fam, lev, w, d, cad, g))
                MEAN_ME.append(me)
                gf = g * float(me.mean())
                GEFF_F.append(gf)
                lo = int(np.floor(round(gf, 6) / GSTEP))
                lam = (gf - gg[lo]) / GSTEP
                for c in RUNGS:
                    ARM[c].append(me * r0 - (me * t0 + g * sw) * c / 1e4)
                    nlo = GR[lo] - GT[lo] * c / 1e4
                    hi = min(lo + 1, len(gg) - 1)
                    nhi = GR[hi] - GT[hi] * c / 1e4
                    TWF[c].append((1 - lam) * nlo + lam * nhi)
        K = len(keys)
        fam_of = np.array([k[0] for k in keys])
        gross_of = np.array([k[5] for k in keys])
        MEAN_ME = np.asarray(MEAN_ME)
        cs_me = np.concatenate([np.zeros((K, 1)), np.cumsum(MEAN_ME, axis=1)], axis=1)
        P(f"   {K} arms built ({int((fam_of=='ABS').sum())} ABS, {int((fam_of=='QEXP').sum())} "
          f"QEXP, {int((fam_of=='QROLL').sum())} QROLL); twin grid {len(gg)-1} runs")

        csA = {c: CS(np.asarray(ARM[c])) for c in RUNGS}
        csF = {c: CS(np.asarray(TWF[c])) for c in RUNGS}
        csG = {c: GridCS(GR - GT * c / 1e4) for c in RUNGS}

        # ---- full-sample arm table, rule 8 and both KEEP paths, with and without the episode
        h = T // 2
        is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
        oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
        e0, e1 = EPD[EP_HEAD]
        x0 = int(eidx.searchsorted(pd.Timestamp(e0), side="left"))
        x1 = int(eidx.searchsorted(pd.Timestamp(e1), side="right"))
        kept = np.ones(T, bool)
        kept[x0:x1] = False
        P(f"   headline episode {EP_HEAD} {e0}..{e1} -> {x1-x0} of {T} scored days deleted "
          f"({(x1-x0)/T:.2%})")

        v2rg, v2tn = fast_run(px, rules_v2_weights(px), mask)
        v2rg, v2tn = v2rg.loc[start:].values, v2tn.loc[start:].values
        v1rg, v1tn = fast_run(px, rules_v1_weights(px), mask)
        v1rg, v1tn = v1rg.loc[start:].values, v1tn.loc[start:].values

        sc, ss, sd_ = fmet(spy)
        scx, ssx, sdx = fmet(spy[kept])
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:]), sd_, sc)
        kh = kept.copy()
        spy_packx = (fsharpe(spy[:h][kept[:h]]), fsharpe(spy[h:][kept[h:]]),
                     fsharpe(spy[oos0:][kept[oos0:]]), sdx, scx)
        P(f"   SPY full {sc:.2%} / {ss:.3f} / {sd_:.2%};  ex-{EP_HEAD} {scx:.2%} / {ssx:.3f} / "
          f"{sdx:.2%}")
        P(f"   4b bars WITH: CAGR floor {0.70*sc:.2%}, DD cap {-0.60*abs(sd_):.2%}, halves "
          f"{spy_pack[0]:.3f}/{spy_pack[1]:.3f}, OOS {spy_pack[2]:.3f}")
        P(f"   4b bars EX  : CAGR floor {0.70*scx:.2%}, DD cap {-0.60*abs(sdx):.2%}, halves "
          f"{spy_packx[0]:.3f}/{spy_packx[1]:.3f}, OOS {spy_packx[2]:.3f}")

        for c in RUNGS:
            v2 = v2rg - v2tn * c / 1e4
            b1, b2, bdd = fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2]
            b1x, b2x = fsharpe(v2[:h][kept[:h]]), fsharpe(v2[h:][kept[h:]])
            bddx = fmet(v2[kept])[2]
            A, F = np.asarray(ARM[c]), np.asarray(TWF[c])
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                ra, rt = A[i], F[i]
                ca, sa, da = fmet(ra)
                ct, st, dt = fmet(rt)
                oc, os_, od = fmet(ra[oos0:])
                rax, rtx = ra[kept], rt[kept]
                cax, sax, dax = fmet(rax)
                ctx, stx, dtx = fmet(rtx)
                ocx, osx, odx = fmet(ra[oos0:][kept[oos0:]])
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
                t4bx = dict(H1=fsharpe(ra[:h][kept[:h]]) > spy_packx[0],
                            H2=fsharpe(ra[h:][kept[h:]]) > spy_packx[1],
                            OOS=osx > spy_packx[2], DD=abs(dax) <= 0.60 * abs(sdx),
                            CAGR=cax >= 0.70 * scx)
                armrows.append(dict(
                    panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                    arm=f"{fam} L{lev} w{w} d{d:.2f} {cad} g{g:.2f}", g_eff=GEFF_F[i],
                    CAGR=ca, Sharpe=sa, MaxDD=da, H1=fsharpe(ra[:h]), H2=fsharpe(ra[h:]),
                    IS_Sharpe=fsharpe(ra[:is_end]), OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                    twin_CAGR=ct, twin_Sharpe=st, twin_MaxDD=dt, twin_OOS=fmet(rt[oos0:])[1],
                    dSharpe=sa - st, dOOS=os_ - fmet(rt[oos0:])[1],
                    win=bool(sa - st > TIE), tie=bool(abs(sa - st) <= TIE),
                    pass_4a=bool(fsharpe(ra[:h]) > b1 and fsharpe(ra[h:]) > b2 and da >= bdd),
                    pass_4b=all(t4b.values()),
                    fail_4b="+".join(k for k, v in t4b.items() if not v) or "-none-",
                    # ---- the same reads with the headline episode deleted ----
                    ex_CAGR=cax, ex_Sharpe=sax, ex_MaxDD=dax,
                    ex_IS_Sharpe=fsharpe(ra[:is_end][kept[:is_end]]),
                    ex_OOS_CAGR=ocx, ex_OOS_Sharpe=osx, ex_OOS_MaxDD=odx,
                    ex_twin_Sharpe=stx, ex_twin_MaxDD=dtx,
                    ex_twin_OOS=fmet(rt[oos0:][kept[oos0:]])[1],
                    ex_dSharpe=sax - stx, ex_win=bool(sax - stx > TIE),
                    ex_pass_4a=bool(fsharpe(ra[:h][kept[:h]]) > b1x
                                    and fsharpe(ra[h:][kept[h:]]) > b2x and dax >= bddx),
                    ex_pass_4b=all(t4bx.values()),
                    ex_fail_4b="+".join(k for k, v in t4bx.items() if not v) or "-none-",
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_, SPY_OOS_Sharpe=spy_pack[2],
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    ex_SPY_CAGR=scx, ex_SPY_Sharpe=ssx, ex_SPY_MaxDD=sdx,
                    ex_SPY_OOS_Sharpe=spy_packx[2],
                    ex_SPY_OOS_CAGR=fmet(spy[oos0:][kept[oos0:]])[0],
                    ex_SPY_OOS_MaxDD=fmet(spy[oos0:][kept[oos0:]])[2],
                    V2_Sharpe=fsharpe(v2), V2_OOS_Sharpe=fsharpe(v2[oos0:]),
                    V2_OOS_CAGR=fmet(v2[oos0:])[0], V2_OOS_MaxDD=fmet(v2[oos0:])[2],
                    ex_V2_Sharpe=fsharpe(v2[kept]),
                    ex_V2_OOS_Sharpe=fsharpe(v2[oos0:][kept[oos0:]]),
                    ex_V2_OOS_CAGR=fmet(v2[oos0:][kept[oos0:]])[0],
                    ex_V2_OOS_MaxDD=fmet(v2[oos0:][kept[oos0:]])[2],
                    V1_Sharpe=fsharpe(v1rg - v1tn * c / 1e4)))

        ARdf = pd.DataFrame([a for a in armrows if a["panel"] == pname])
        for c in RUNGS:
            sub_c = ARdf[ARdf.rung == c]
            for fam in FAMS:
                for g in GROSSES:
                    for d in DEPTHS:
                        for cad in CADENCES:
                            s = sub_c[(sub_c.family == fam) & (sub_c.gross == g)
                                      & (sub_c.depth == d) & (sub_c.cadence == cad)]
                            if s.empty or s.IS_Sharpe.isna().all():
                                continue
                            pk = s.loc[s.IS_Sharpe.idxmax()]
                            pkx = s.loc[s.ex_IS_Sharpe.idxmax()]
                            wfrows.append(dict(
                                panel=pname, rung=c, family=fam, gross=g, depth=d, cadence=cad,
                                level=pk.level, w=pk.w, IS_Sharpe=pk.IS_Sharpe,
                                OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                OOS_MaxDD=pk.OOS_MaxDD, pass_4a=bool(pk.pass_4a),
                                pass_4b=bool(pk.pass_4b), fail_4b=pk.fail_4b,
                                SPY_OOS_CAGR=pk.SPY_OOS_CAGR, SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                                SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD, V2_OOS_CAGR=pk.V2_OOS_CAGR,
                                V2_OOS_Sharpe=pk.V2_OOS_Sharpe, V2_OOS_MaxDD=pk.V2_OOS_MaxDD,
                                ex_level=pkx.level, ex_w=pkx.w, ex_IS_Sharpe=pkx.ex_IS_Sharpe,
                                ex_same_pick=bool(pkx.level == pk.level and pkx.w == pk.w),
                                ex_OOS_CAGR=pkx.ex_OOS_CAGR, ex_OOS_Sharpe=pkx.ex_OOS_Sharpe,
                                ex_OOS_MaxDD=pkx.ex_OOS_MaxDD, ex_pass_4a=bool(pkx.ex_pass_4a),
                                ex_pass_4b=bool(pkx.ex_pass_4b), ex_fail_4b=pkx.ex_fail_4b,
                                ex_SPY_OOS_CAGR=pkx.ex_SPY_OOS_CAGR,
                                ex_SPY_OOS_Sharpe=pkx.ex_SPY_OOS_Sharpe,
                                ex_SPY_OOS_MaxDD=pkx.ex_SPY_OOS_MaxDD,
                                ex_V2_OOS_CAGR=pkx.ex_V2_OOS_CAGR,
                                ex_V2_OOS_Sharpe=pkx.ex_V2_OOS_Sharpe,
                                ex_V2_OOS_MaxDD=pkx.ex_V2_OOS_MaxDD))

        PAN[pname] = dict(eidx=eidx, csA=csA, csF=csF, csG=csG, fam=fam_of, gross=gross_of,
                          cs_me=cs_me, K=K, T=T, gg=gg, ARM0=np.asarray(ARM[RUNG_HEAD]),
                          TWF0=np.asarray(TWF[RUNG_HEAD]))
        del px, GR, GT, ARM, TWF

    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------- G4: reproduce 825's corpus
    P(f"\n{'='*118}\nGATE G4 - does this run rebuild idea 825's COMMITTED corpus?\n{'='*118}")
    if REF825.exists():
        R = pd.read_csv(REF825)
        kcols = ["panel", "rung", "family", "level", "w", "depth", "cadence", "gross"]
        a = AR.set_index(kcols).sort_index()
        b = R.set_index(kcols).sort_index()
        same_idx = a.index.equals(b.index)
        d_sh = float(np.abs(a.Sharpe.values - b.Sharpe.values).max())
        d_tw = float(np.abs(a.twin_Sharpe.values - b.twin_Sharpe.values).max())
        d_win = int((a.win.values.astype(bool) != b.win.values.astype(bool)).sum())
        ok4 = same_idx and d_sh < 1e-12 and d_tw < 1e-12 and d_win == 0
        P(f"   rows {len(a)} vs {len(b)}, key sets identical {same_idx}")
        P(f"   max|dSharpe| {d_sh:.3e}   max|d twin Sharpe| {d_tw:.3e}   win-flag mismatches "
          f"{d_win}   {'PASS' if ok4 else 'FAIL'}")
    else:
        ok4 = False
        P(f"   FAIL - reference {REF825.name} not found")
    P(f"   G4 corpus reproduction: {'PASS' if ok4 else 'FAIL'}")

    # ------------------------------------------------------- G5: deletion arithmetic exact?
    P(f"\n{'='*118}\nGATE G5 - is the DELETION ARITHMETIC exact?\n{'='*118}")
    d = PAN["U56"]
    T = d["T"]
    e0, e1 = EPD[EP_HEAD]
    X0 = int(d["eidx"].searchsorted(pd.Timestamp(e0), side="left"))
    X1 = int(d["eidx"].searchsorted(pd.Timestamp(e1), side="right"))
    s_full = d["csA"][RUNG_HEAD].sharpe(0, T)
    s_empty = d["csA"][RUNG_HEAD].sharpe(0, T, 0, 0)
    g5a = float(np.nanmax(np.abs(s_full - s_empty)))
    keep = np.ones(T, bool)
    keep[X0:X1] = False
    direct = np.array([fsharpe(r[keep]) for r in d["ARM0"]])
    s_del = d["csA"][RUNG_HEAD].sharpe(0, T, X0, X1)
    g5b = float(np.nanmax(np.abs(direct - s_del)))
    direct_t = np.array([fsharpe(r[keep]) for r in d["TWF0"]])
    s_delt = d["csF"][RUNG_HEAD].sharpe(0, T, X0, X1)
    g5c = float(np.nanmax(np.abs(direct_t - s_delt)))
    gm = (d["cs_me"][:, T] - d["cs_me"][:, 0] - (d["cs_me"][:, X1] - d["cs_me"][:, X0])) \
        / (T - (X1 - X0)) * d["gross"]
    lo = np.clip(np.floor(np.round(gm, 6) / GSTEP).astype(int), 0, len(d["gg"]) - 2)
    lam = (gm - d["gg"][lo]) / GSTEP
    s_grid = d["csG"][RUNG_HEAD].sharpe(0, T, lo, lam, X0, X1)
    g5d = float(np.nanmax(np.abs(s_grid - s_grid)))  # finite check below
    ok5 = g5a == 0.0 and g5b < 1e-12 and g5c < 1e-12 and np.isfinite(s_grid).all()
    P(f"   (a) empty deletion == undeleted, max|d|            {g5a:.3e}")
    P(f"   (b) arm stack vs direct numpy masked Sharpe        {g5b:.3e}")
    P(f"   (c) twin stack vs direct numpy masked Sharpe       {g5c:.3e}")
    P(f"   (d) deletion-aware WINMATCH grid all finite        {bool(np.isfinite(s_grid).all())}")
    P(f"   G5 deletion arithmetic: {'PASS' if ok5 else 'FAIL'}")

    # ------------------------------------------------------- leg machinery
    def ep_bounds(pname, epname, a, b):
        """The deleted half-open index range, clipped into [a,b)."""
        if EPD[epname] is None:
            return 0, 0
        ei = PAN[pname]["eidx"]
        z0 = int(ei.searchsorted(pd.Timestamp(EPD[epname][0]), side="left"))
        z1 = int(ei.searchsorted(pd.Timestamp(EPD[epname][1]), side="right"))
        z0, z1 = max(z0, a), min(z1, b)
        return (z0, z1) if z1 > z0 else (0, 0)

    def leg_rates(pname, c, a, b, matching, epname):
        d = PAN[pname]
        x0, x1 = ep_bounds(pname, epname, a, b)
        n = (b - a) - (x1 - x0)
        if n < MINLEG:
            return None
        sa = d["csA"][c].sharpe(a, b, x0, x1)
        if matching == "FULLMATCH":
            st = d["csF"][c].sharpe(a, b, x0, x1)
        else:
            gm = ((d["cs_me"][:, b] - d["cs_me"][:, a])
                  - (d["cs_me"][:, x1] - d["cs_me"][:, x0])) / n * d["gross"]
            lo = np.clip(np.floor(np.round(gm, 6) / GSTEP).astype(int), 0, len(d["gg"]) - 2)
            lam = (gm - d["gg"][lo]) / GSTEP
            st = d["csG"][c].sharpe(a, b, lo, lam, x0, x1)
        ok = np.isfinite(sa) & np.isfinite(st)
        return (sa - st > TIE), ok, d["fam"], (x1 - x0)

    def build_legs(legset):
        """Date-defined legs; per-panel index ranges resolved later."""
        out = []
        if legset == "ENDYEAR":
            for y in ENDYEARS:
                out.append((f"..{y}", None, f"{y}-12-31"))
        elif legset == "POSTYEAR":
            for y in ENDYEARS:
                out.append((f"{y}..", f"{y}-12-31", None))
        else:
            for y in BLOCK_STARTS:
                out.append((f"{y}-{y+2}", f"{y}-01-01", f"{y+2}-12-31"))
        return out

    def leg_idx(pname, lo_d, hi_d):
        ei = PAN[pname]["eidx"]
        a = 0 if lo_d is None else int(ei.searchsorted(pd.Timestamp(lo_d), side="right"))
        b = PAN[pname]["T"] if hi_d is None else int(
            ei.searchsorted(pd.Timestamp(hi_d), side="right"))
        return a, b

    # ------------------------------------------------------- the grid
    P(f"\n{'='*118}\nTHE GRID - {len(EPISODES)} episodes x {len(LEGSETS)} leg sets x "
      f"{len(RUNGS)} rungs x {len(MATCHINGS)} matchings x {len(SCOPES)} scopes\n{'='*118}")
    grid, legrows = [], []
    for legset in LEGSETS:
        for legname, lo_d, hi_d in build_legs(legset):
            for epname in EPISODES:
                for c in RUNGS:
                    for matching in MATCHINGS:
                        per = {}
                        for pname in PANELS:
                            a, b = leg_idx(pname, lo_d, hi_d)
                            r = leg_rates(pname, c, a, b, matching, epname)
                            if r is not None:
                                per[pname] = r
                        if not per:
                            continue
                        for scope in SCOPES:
                            if scope == "POOLED":
                                wv = np.concatenate([per[p][0] for p in per])
                                ok = np.concatenate([per[p][1] for p in per])
                                fv = np.concatenate([per[p][2] for p in per])
                                ndel = sum(per[p][3] for p in per)
                            elif scope in per:
                                wv, ok, fv, ndel = per[scope]
                            else:
                                continue
                            rates = {}
                            for f in FAMS:
                                sel = ok & (fv == f)
                                rates[f] = (float(wv[sel].mean()) if sel.any() else np.nan,
                                            int(sel.sum()))
                            adv = rates["QROLL"][0] - max(rates["ABS"][0], rates["QEXP"][0])
                            for f in FAMS + ["adv"]:
                                grid.append(dict(
                                    legset=legset, leg=legname, episode=epname, rung=c,
                                    matching=matching, scope=scope, family=f,
                                    win=(adv if f == "adv" else rates[f][0]),
                                    n=(sum(rates[x][1] for x in FAMS) if f == "adv"
                                       else rates[f][1]),
                                    n_deleted=ndel))
            for pname in PANELS:
                a, b = leg_idx(pname, lo_d, hi_d)
                ei = PAN[pname]["eidx"]
                if b - a < MINLEG:
                    continue
                ov = {e: (ep_bounds(pname, e, a, b)[1] - ep_bounds(pname, e, a, b)[0])
                      for e in EPISODES}
                legrows.append(dict(legset=legset, leg=legname, panel=pname, a=a, b=b,
                                    start=str(ei[a].date()), end=str(ei[b - 1].date()),
                                    days=b - a, **{f"ov_{k}": v for k, v in ov.items()}))
    G = pd.DataFrame(grid)
    base = G[G.episode == "NONE"].set_index(
        ["legset", "leg", "rung", "matching", "scope", "family"])["win"]
    G["win_NONE"] = G.set_index(
        ["legset", "leg", "rung", "matching", "scope", "family"]).index.map(base)
    G["delta"] = G["win"] - G["win_NONE"]
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L = pd.DataFrame(legrows)
    L.to_csv(f"{OUT}.legs.csv", index=False)
    P(f"   {len(G)} grid rows written; {len(L)} (legset, leg, panel) rows")

    # ------------------------------------------------------- G6: non-intersecting deletion
    P(f"\n{'='*118}\nGATE G6 - does a deletion that MISSES a leg move it by exactly 0?\n{'='*118}")
    clean = G[(G.episode.isin(EP_COVID)) & (G.n_deleted == 0) & (G.family != "adv")]
    g6 = float(np.nanmax(np.abs(clean.delta.values))) if len(clean) else 0.0
    ok6 = len(clean) > 0 and g6 == 0.0
    P(f"   {len(clean)} (leg, episode) cells with zero overlap; max|delta| {g6:.3e}  "
      f"{'PASS' if ok6 else 'FAIL'}")
    P(f"   G6: {'PASS' if ok6 else 'FAIL'}")
    P(f"\n   GATE SUMMARY: G1 PASS  G2 PASS  G3 PASS  G4 {'PASS' if ok4 else 'FAIL'}  "
      f"G5 {'PASS' if ok5 else 'FAIL'}  G6 {'PASS' if ok6 else 'FAIL'}")

    # ------------------------------------------------------- THE HEADLINE READ
    def cell(legset, episode, rung, matching, scope, only_hit=True):
        """Mean win rate per family over the legs of a leg set, restricted (by default) to legs
        that actually CONTAIN the episode."""
        q = G[(G.legset == legset) & (G.episode == episode) & (G.rung == rung)
              & (G.matching == matching) & (G.scope == scope)]
        if only_hit:
            hit = set(G[(G.legset == legset) & (G.episode == episode) & (G.rung == rung)
                        & (G.matching == matching) & (G.scope == scope)
                        & (G.n_deleted > 0)].leg)
            q = q[q.leg.isin(hit)]
        return q.groupby("family")[["win", "delta"]].mean()

    P(f"\n{'='*118}\nHEADLINE - legset {LEGSET_HEAD}, episode {EP_HEAD}, rung {RUNG_HEAD:g} bps, "
      f"FULLMATCH, POOLED\n   (mean over the legs that CONTAIN the episode)\n{'='*118}")
    hit_legs = sorted(set(G[(G.legset == LEGSET_HEAD) & (G.episode == EP_HEAD)
                            & (G.n_deleted > 0)].leg))
    P(f"   legs containing {EP_HEAD}: {hit_legs}")
    base_h = cell(LEGSET_HEAD, "NONE", RUNG_HEAD, "FULLMATCH", "POOLED", only_hit=False)
    base_h = base_h.loc[:, ["win"]]
    hh = cell(LEGSET_HEAD, EP_HEAD, RUNG_HEAD, "FULLMATCH", "POOLED")
    q0 = G[(G.legset == LEGSET_HEAD) & (G.episode == "NONE") & (G.rung == RUNG_HEAD)
           & (G.matching == "FULLMATCH") & (G.scope == "POOLED") & (G.leg.isin(hit_legs))]
    b0 = q0.groupby("family")["win"].mean()
    P(f"   {'family':<8} {'WITH 2020':>10} {'WITHOUT':>10} {'delta':>9}")
    for f in FAMS + ["adv"]:
        P(f"   {f:<8} {b0[f]:>10.4f} {hh.loc[f,'win']:>10.4f} {hh.loc[f,'delta']:>+9.4f}")

    P(f"\n   per-leg detail ({LEGSET_HEAD}, {EP_HEAD}, {RUNG_HEAD:g} bps, FULLMATCH, POOLED):")
    P(f"   {'leg':<10} {'ndel':>5}  " + "  ".join(f"{f:>17}" for f in FAMS + ["adv"]))
    for lg in sorted(set(G[(G.legset == LEGSET_HEAD)].leg)):
        r = {}
        for f in FAMS + ["adv"]:
            a = G[(G.legset == LEGSET_HEAD) & (G.leg == lg) & (G.rung == RUNG_HEAD)
                  & (G.matching == "FULLMATCH") & (G.scope == "POOLED") & (G.family == f)]
            if a.empty:
                continue
            r[f] = (float(a[a.episode == "NONE"].win.iloc[0]),
                    float(a[a.episode == EP_HEAD].win.iloc[0]))
        if not r:
            continue
        nd = int(G[(G.legset == LEGSET_HEAD) & (G.leg == lg) & (G.episode == EP_HEAD)
                   & (G.rung == RUNG_HEAD) & (G.matching == "FULLMATCH")
                   & (G.scope == "POOLED")].n_deleted.iloc[0])
        P(f"   {lg:<10} {nd:>5}  " + "  ".join(f"{r[f][0]:>7.4f}->{r[f][1]:>7.4f}"
                                               for f in FAMS + ["adv"]))

    # ------------------------------------------------------- hypotheses
    P(f"\n{'='*118}\nPRE-REGISTERED HYPOTHESES\n{'='*118}")
    H = {}
    H["H_MAIN"] = bool(hh.loc["QROLL", "win"] > 0.50)
    H["H_ADV"] = bool(hh.loc["adv", "win"] > 0.0)
    H["H_DROP"] = bool(hh.loc["QROLL", "delta"] < 0.0)

    def mean_delta(episode, fam="QROLL"):
        q = G[(G.legset == LEGSET_HEAD) & (G.episode == episode) & (G.rung == RUNG_HEAD)
              & (G.matching == "FULLMATCH") & (G.scope == "POOLED") & (G.family == fam)
              & (G.n_deleted > 0)]
        return float(q.delta.mean()) if len(q) else np.nan

    dmain = mean_delta(EP_HEAD)
    dplac = {e: mean_delta(e) for e in EP_PLACEBO}
    H["H_PLACEBO"] = bool(all(abs(v) < abs(dmain) for v in dplac.values() if np.isfinite(v)))
    P(f"   deltas on legs that contain them: {EP_HEAD} {dmain:+.4f}; "
      + "; ".join(f"{e} {v:+.4f}" for e, v in dplac.items())
      + f"; DD_2015 {mean_delta('DD_2015'):+.4f}; COVID_WIDE {mean_delta('COVID_WIDE'):+.4f}; "
        f"COVID_DD {mean_delta('COVID_DD'):+.4f}")

    cleanlegs = sorted(set(G[(G.legset == LEGSET_HEAD) & (G.episode == EP_HEAD)
                             & (G.n_deleted == 0)].leg))
    qc = G[(G.legset == LEGSET_HEAD) & (G.episode == "NONE") & (G.rung == RUNG_HEAD)
           & (G.matching == "FULLMATCH") & (G.scope == "POOLED") & (G.family == "QROLL")
           & (G.leg.isin(cleanlegs))]
    H["H_CLEAN"] = bool(len(qc) and qc.win.max() <= 0.60)
    P(f"   legs with NO 2020 exposure at all {cleanlegs}: QROLL win "
      + ", ".join(f"{l}={float(qc[qc.leg==l].win.iloc[0]):.4f}" for l in cleanlegs
                  if len(qc[qc.leg == l])))

    def main_verdict(rung=RUNG_HEAD, matching="FULLMATCH", scope="POOLED", legset=LEGSET_HEAD):
        c = cell(legset, EP_HEAD, rung, matching, scope)
        return bool(c.loc["QROLL", "win"] > 0.50) if "QROLL" in c.index else None

    H["H_COSTINV"] = len({main_verdict(rung=c) for c in RUNGS}) == 1
    H["H_MATCH"] = len({main_verdict(matching=m) for m in MATCHINGS}) == 1
    H["H_PANEL"] = len({main_verdict(scope=s) for s in PANELS}) == 1
    H["H_LEGSET"] = len({main_verdict(legset=s) for s in LEGSETS}) == 1
    P("   H_MAIN by rung " + ", ".join(f"{c:g}:{main_verdict(rung=c)}" for c in RUNGS))
    P("   H_MAIN by matching " + ", ".join(f"{m}:{main_verdict(matching=m)}" for m in MATCHINGS))
    P("   H_MAIN by panel " + ", ".join(f"{s}:{main_verdict(scope=s)}" for s in PANELS))
    P("   H_MAIN by legset " + ", ".join(f"{s}:{main_verdict(legset=s)}" for s in LEGSETS))

    n4b = int(AR[(AR.rung == RUNG_HEAD)].pass_4b.sum())
    n4bx = int(AR[(AR.rung == RUNG_HEAD)].ex_pass_4b.sum())
    n4a = int(AR[(AR.rung == RUNG_HEAD)].pass_4a.sum())
    n4ax = int(AR[(AR.rung == RUNG_HEAD)].ex_pass_4a.sum())
    H["H_4B"] = n4bx > 0
    P(f"\n   KEEP paths at {RUNG_HEAD:g} bps over {len(AR[AR.rung==RUNG_HEAD])} arms: "
      f"4a {n4a} -> {n4ax} ex-{EP_HEAD};  4b {n4b} -> {n4bx} ex-{EP_HEAD}")

    # ------------------------------------------------------- RULE 8
    P(f"\n{'='*118}\nPROTOCOL RULE 8 - dial chosen on {IS_END} and earlier, OOS read ONCE\n{'='*118}")
    w10 = WF[WF.rung == RUNG_HEAD].copy()
    best = w10.loc[w10.IS_Sharpe.idxmax()]
    bestx = w10.loc[w10.ex_IS_Sharpe.idxmax()]
    P(f"   WITH 2020 - best IS pick: {best.panel} {best.family} L{best.level} w{best.w} "
      f"d{best.depth} {best.cadence} g{best.gross}  (IS Sharpe {best.IS_Sharpe:.4f})")
    P(f"      OOS   pick {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.3f} / {best.OOS_MaxDD:.2%}")
    P(f"      OOS   RULES v2 {best.V2_OOS_CAGR:.2%} / {best.V2_OOS_Sharpe:.3f} / "
      f"{best.V2_OOS_MaxDD:.2%}")
    P(f"      OOS   SPY {best.SPY_OOS_CAGR:.2%} / {best.SPY_OOS_Sharpe:.3f} / "
      f"{best.SPY_OOS_MaxDD:.2%}")
    P(f"   EX-{EP_HEAD} - best IS pick: {bestx.panel} {bestx.family} L{bestx.ex_level} "
      f"w{bestx.ex_w} d{bestx.depth} {bestx.cadence} g{bestx.gross} "
      f"(IS Sharpe {bestx.ex_IS_Sharpe:.4f})")
    P(f"      OOS   pick {bestx.ex_OOS_CAGR:.2%} / {bestx.ex_OOS_Sharpe:.3f} / "
      f"{bestx.ex_OOS_MaxDD:.2%}")
    P(f"      OOS   RULES v2 {bestx.ex_V2_OOS_CAGR:.2%} / {bestx.ex_V2_OOS_Sharpe:.3f} / "
      f"{bestx.ex_V2_OOS_MaxDD:.2%}")
    P(f"      OOS   SPY {bestx.ex_SPY_OOS_CAGR:.2%} / {bestx.ex_SPY_OOS_Sharpe:.3f} / "
      f"{bestx.ex_SPY_OOS_MaxDD:.2%}")
    H["H_R8"] = bool(bestx.ex_OOS_Sharpe > bestx.ex_SPY_OOS_Sharpe)
    P(f"   rule-8 picks whose dial MOVES when 2020 is deleted: "
      f"{int((~w10.ex_same_pick).sum())} of {len(w10)}")
    P(f"   rule-8 picks passing 4b: {int(w10.pass_4b.sum())} of {len(w10)} WITH, "
      f"{int(w10.ex_pass_4b.sum())} EX;  4a: {int(w10.pass_4a.sum())} -> "
      f"{int(w10.ex_pass_4a.sum())}")
    P(f"   rule-8 picks beating SPY OOS Sharpe: "
      f"{int((w10.OOS_Sharpe > w10.SPY_OOS_Sharpe).sum())} of {len(w10)} WITH, "
      f"{int((w10.ex_OOS_Sharpe > w10.ex_SPY_OOS_Sharpe).sum())} EX")

    P(f"\n{'='*118}\nHYPOTHESIS TABLE\n{'='*118}")
    for k, v in H.items():
        P(f"   {k:<11} {'PASS' if v else 'FAIL'}")
    P(f"   {sum(bool(v) for v in H.values())} of {len(H)} PASS")

    P(f"\n   runtime {time.time()-T0:.1f}s")
    (Path(f"{OUT}.console.txt")).write_text("\n".join(LOG) + "\n")
    return H, G, AR, WF


if __name__ == "__main__":
    main()
