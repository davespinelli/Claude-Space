#!/usr/bin/env python3
"""Idea 825 - is QROLL-ON-TOP an entirely POST-2017 fact?   (cloud lane, 2026-09-12, idea 1 of 2)

QUESTION (QUEUE idea 825, verbatim)
    idea 609 found the IS modal twin order is QEXP > QROLL > ABS at 20 of 20 (L, step) grid points
    and the OOS modal has QROLL on top at 20 of 20, with share_top 0.056-0.250 in sample against
    0.550-0.950 out of sample.  Test whether QROLL's advantage exists at all before 2017 on a
    gross-matched control, or is wholly a property of the second window.  Max 2 params (split
    date, family set).

WHAT IS BEING MEASURED
    The record's object is the MATCHED-GROSS TWIN WIN RATE: for each gated arm, whether its Sharpe
    beats a STATIC-gross twin holding the same mean gross with no timing.  The twin IS the
    gross-matched control the queue asks for - it holds the arm's own realised exposure and does
    nothing else, so any excess is the CLAUSE and not the exposure.  Idea 605 published the
    full-sample family order QROLL > QEXP > ABS; idea 609 showed a reader of a 3-year window sees
    that order rarely in the first half of the sample and usually in the second.  This run reads
    the statistic on TWO windows either side of a split date and asks the direct question: is
    QROLL's advantage present at all before the split?

    Per (panel, rung, matching, famset, split, leg in {PRE, POST}) the reported quantities are
        win[f]   the twin win rate of family f on that leg
        adv      win[QROLL] - max(win[ABS], win[QEXP])     <- the "QROLL on top" margin
        order    the descending family order, with ties in their own column, never broken silently
    A window in which QROLL is not strictly on top has adv <= 0; adv > 0 is the claim.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) SPLIT DATE in {2012-12-31, 2014-12-31, 2016-12-31, 2018-12-31, 2020-12-31}.  The record's
        IS/OOS boundary is 2016-12-31 and that is the HEADLINE, declared here before anything is
        read.  The other four exist so the answer cannot be a property of one cut.
    (2) FAMILY SET, i.e. which QROLL lookbacks are in the corpus.  FULL w in {252,504,1008,2016}
        (12 arms, idea 605's corpus, HEADLINE), SHORT {252,504}, LONG {1008,2016}, BAL {504} only
        (3 arms - the same arm count as ABS and QEXP, so an arm-count imbalance cannot carry the
        result).  5 x 4 = 20 grid points, EVERY ONE printed and written to .grid.csv.

REPORTED AXES, none of them a tune (each printed at every grid point):
    COST RUNG      {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.
    TWIN MATCHING  FULLMATCH = twin gross matched on the FULL sample, path sliced to the leg (the
                   published construction read on a leg) vs WINMATCH = twin gross re-matched on the
                   leg itself (what a reader who had only that leg would have built).  BOTH always.
    PANEL          U56, B136, SMALL663, and POOLED over all three.

THE CORPUS (idea 602/605/609's, rebuilt so every number is directly comparable)
    book      EWALL = idea 28/42 eligibility (above 200d MA, vol20 < 0.60), equal weight over
              eligible names at gross g, weekly, next-day fill.
    clause    a BREADTH de-grossing overlay: when 200d-MA breadth falls below a threshold the book
              is multiplied by (1 - depth); gated-out weight goes to CASH, never re-spread.
    families  ABS    fixed breadth level B in {0.30, 0.40, 0.50}              (3 arms)
              QEXP   expanding-quantile threshold q in {0.07, 0.12, 0.17}     (3 arms)
              QROLL  rolling-quantile q x w, w in {252, 504, 1008, 2016}      (12 arms)
              x depth {0.25, 0.50, 1.00} x cadence {D, W} x gross {0.75, 1.00} = 216 arms/panel.
    twin      the STATIC-gross EWALL at the arm's realised mean gross - same exposure, no timing.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_PRE      at the headline (split 2016-12-31, FULL, 10 bps, FULLMATCH, POOLED) QROLL is
               strictly on top on the PRE leg: adv_PRE > 0.  This is the queue's literal question.
    H_PREPOS   on the same leg win[QROLL] > 0.50 - QROLL beats its own gross-matched control more
               often than not, even if another family beats it too.  Separate from H_PRE so a
               failure of one cannot be read as a failure of the other.
    H_GAP      |adv_PRE - adv_POST| <= 0.20 - the advantage is not a property of the second window.
    H_SPLITFREE sign(adv_PRE) is the same at all 5 split dates (10 bps, FULL, FULLMATCH, POOLED).
    H_FAMSET   sign(adv_PRE) is the same at all 4 family sets - not an arm-count artefact.
    H_COSTINV  sign(adv_PRE) is the same at 0, 10 and 25 bps.
    H_MATCH    |adv_PRE(FULLMATCH) - adv_PRE(WINMATCH)| <= 0.10 - not an artefact of which twin a
               reader would have matched.
    H_PANEL    sign(adv_PRE) agrees across U56, B136 and SMALL663.
    H_R8CLAIM  RULE 8 ON THE CLAIM: the family set chosen on the first half of the sample by
               highest adv reproduces an adv within 0.10 on the second half, read once.

GATES (printed first; the verdict is not read until they are reported)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast Sharpe/CAGR/MaxDD reproduce engine.metrics to <= 1e-9 on a real series.
    G3 the 0.01-grid interpolation of the static-gross twin reproduces an EXACT run of the same
       gross to <= 1e-6 of Sharpe.
    G4 the FULL-SAMPLE family order on today's panels is idea 605's QROLL > QEXP > ABS at all
       three rungs (the thing idea 825 is about; 609 showed levels no longer reproduce because the
       small panel grew, so the ORDER is the gate, and that is stated rather than assumed).
    G5 a leg covering the whole sample reproduces the full-sample win rates exactly.

PROTOCOL RULE 8 (mandatory, run and reported) - on the BOOKS as well as on the claim:
    per (panel, family, gross, depth, cadence) the DIAL (level, w) is chosen on IS (..2016-12-31)
    by IS Sharpe alone and OOS (2017-01-01..) is read exactly ONCE, reported as CAGR/Sharpe/MaxDD
    against RULES v2 (the live baseline) and SPY on the same window.  BOTH KEEP paths (4a and 4b)
    are evaluated on all 648 arms at every cost rung, and each 4b passer is read against its own
    matched-gross twin so an exposure-only pass cannot be mistaken for a clause.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and SMALL663 worst - a sub-$2B screen read today cannot see the names that fell out
    of it (data/SMALL_PANEL_README.md).  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are
    dropped before anything is computed.  A win RATE is a within-panel agreement rate, which
    survivorship moves far less than a level, but no Sharpe or CAGR printed here is a capital claim
    on its own.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .grid.csv        20 tuned points x 3 rungs x 2 matchings x 4 panel scopes, every cell
    .arms.csv        one row per (panel, arm, rung): metrics, twin, 4a/4b, rule-8 columns
    .walkforward.csv the rule-8 picks and their OOS reads against RULES v2 and SPY
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
SLUG = "is-QROLL-ON-TOP-an-entirely-POST-2017-fact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

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
PUBLISHED = ("QROLL", "QEXP", "ABS")          # idea 605's committed full-sample order

# ---- tuned dial 1 and 2, headlines declared here, before any number is read ----------
SPLITS = ["2012-12-31", "2014-12-31", "2016-12-31", "2018-12-31", "2020-12-31"]
SPLIT_HEAD = "2016-12-31"
FAMSETS = {"FULL": [252, 504, 1008, 2016], "SHORT": [252, 504],
           "LONG": [1008, 2016], "BAL": [504]}
FAMSET_HEAD = "FULL"
MINLEG = 252                                   # a leg shorter than a year is not read

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (596/604/609's)
def fast_run(prices, weights, mask, lag=LAG):
    """(gross return path before costs, turnover path)."""
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
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


# ------------------------------------------------------------------ primitives (idea 28/42/602)
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


class CS:
    """Cumulative sums of a stack of series, so any window's Sharpe is O(1)."""

    def __init__(self, M):
        z = np.zeros((M.shape[0], 1))
        self.s1 = np.concatenate([z, np.cumsum(M, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(M * M, axis=1)], axis=1)

    def sharpe(self, a, b):
        n = b - a
        if n < 2:
            return np.full(self.s1.shape[0], np.nan)
        s1 = self.s1[:, b] - self.s1[:, a]
        s2 = self.s2[:, b] - self.s2[:, a]
        mu = s1 / n
        var = (s2 - n * mu * mu) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


class GridCS:
    """Cumsums of the static-gross twin grid incl. adjacent cross-products, so an interpolated
       twin (1-lam)*N_lo + lam*N_hi has an O(1) window Sharpe too."""

    def __init__(self, N):
        self.G, self.T = N.shape
        z = np.zeros((self.G, 1))
        self.s1 = np.concatenate([z, np.cumsum(N, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(N * N, axis=1)], axis=1)
        X = N[:-1] * N[1:]
        self.sx = np.concatenate([np.zeros((self.G - 1, 1)), np.cumsum(X, axis=1)], axis=1)

    def sharpe(self, a, b, lo, lam):
        n = b - a
        if n < 2:
            return np.full(len(lo), np.nan)
        hi = np.minimum(lo + 1, self.G - 1)
        m_lo = (self.s1[lo, b] - self.s1[lo, a]) / n
        m_hi = (self.s1[hi, b] - self.s1[hi, a]) / n
        q_lo = (self.s2[lo, b] - self.s2[lo, a]) / n
        q_hi = (self.s2[hi, b] - self.s2[hi, a]) / n
        xi = np.minimum(lo, self.G - 2)
        q_x = (self.sx[xi, b] - self.sx[xi, a]) / n
        mu = (1 - lam) * m_lo + lam * m_hi
        ey2 = (1 - lam) ** 2 * q_lo + 2 * lam * (1 - lam) * q_x + lam ** 2 * q_hi
        var = (ey2 - mu * mu) * n / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


def order_of(rates):
    v = [rates[f] for f in FAMS]
    if len(set(np.round(v, 12))) < 3:
        return ("TIED",)
    return tuple(f for f, _ in sorted(zip(FAMS, v), key=lambda t: -t[1]))


def main():
    T0 = time.time()
    P(f"# Idea 825 - {SLUG}   (cloud lane, {DATE}, idea 1 of 2)")
    P("# QUESTION: does QROLL's matched-gross-twin advantage exist at all BEFORE the split, or is")
    P("# 'QROLL on top' wholly a property of the second window?  609 measured share_top 0.056-0.250")
    P("# in sample against 0.550-0.950 out of sample and left the direct question open.")
    P(f"# TUNED: split {SPLITS} x famset {list(FAMSETS)} = {len(SPLITS)*len(FAMSETS)} points, ALL")
    P(f"#   reported; HEADLINE split {SPLIT_HEAD}, famset {FAMSET_HEAD} (605's corpus).")
    P(f"# REPORTED AXES (not tunes): rung {RUNGS} bps (headline {RUNG_HEAD:g}), matching "
      f"[FULLMATCH, WINMATCH], panel [POOLED, U56, B136, SMALL663].")
    P("# The gross-matched TWIN is the control: same realised mean exposure, no timing.")
    P("# Ties are never broken silently; a tied leg is reported as TIED.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    armrows, wfrows, gridrows = [], [], []
    PAN = {}

    for pname in ["U56", "B136", "SMALL663"]:
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

        br_full = breadth(px)
        thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
        thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS_ROLL}

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
            P(f"\n{'-'*118}\nGATES\n{'-'*118}")
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
            inn = (1 - lam) * (GR[lo] - GT[lo] * 10 / 1e4) + lam * (GR[lo + 1] - GT[lo + 1] * 10 / 1e4)
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
        w_of = np.array([k[2] for k in keys])
        gross_of = np.array([k[5] for k in keys])
        MEAN_ME = np.asarray(MEAN_ME)
        cs_me = np.concatenate([np.zeros((K, 1)), np.cumsum(MEAN_ME, axis=1)], axis=1)
        P(f"   {K} arms built ({int((fam_of=='ABS').sum())} ABS, {int((fam_of=='QEXP').sum())} "
          f"QEXP, {int((fam_of=='QROLL').sum())} QROLL); twin grid {len(gg)-1} runs")

        csA = {c: CS(np.asarray(ARM[c])) for c in RUNGS}
        csF = {c: CS(np.asarray(TWF[c])) for c in RUNGS}
        csG = {c: GridCS(GR - GT * c / 1e4) for c in RUNGS}

        # ---- full-sample arm table, rule 8 and both KEEP paths ----------------------
        h = T // 2
        is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
        oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
        sc, ss, sd_ = fmet(spy)
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:]), sd_, sc)
        v2rg, v2tn = fast_run(px, rules_v2_weights(px), mask)
        v2rg, v2tn = v2rg.loc[start:].values, v2tn.loc[start:].values
        v1rg, v1tn = fast_run(px, rules_v1_weights(px), mask)
        v1rg, v1tn = v1rg.loc[start:].values, v1tn.loc[start:].values
        P(f"   SPY {sc:.2%} / {ss:.3f} / {sd_:.2%};  4b bars: CAGR floor {0.70*sc:.2%}, "
          f"DD cap {-0.60*abs(sd_):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, "
          f"OOS {spy_pack[2]:.3f}")
        for c in RUNGS:
            v2 = v2rg - v2tn * c / 1e4
            b1, b2, bdd = fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2]
            A, F = np.asarray(ARM[c]), np.asarray(TWF[c])
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                ra, rt = A[i], F[i]
                ca, sa, da = fmet(ra)
                ct, st, dt = fmet(rt)
                oc, os_, od = fmet(ra[oos0:])
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
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
                    twin_pass_4b=bool(fsharpe(rt[:h]) > spy_pack[0] and fsharpe(rt[h:]) > spy_pack[1]
                                      and fmet(rt[oos0:])[1] > spy_pack[2]
                                      and abs(dt) <= 0.60 * abs(sd_) and ct >= 0.70 * sc),
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_, SPY_OOS_Sharpe=spy_pack[2],
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    V2_Sharpe=fsharpe(v2), V2_OOS_Sharpe=fsharpe(v2[oos0:]),
                    V2_OOS_CAGR=fmet(v2[oos0:])[0], V2_OOS_MaxDD=fmet(v2[oos0:])[2],
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
                            wfrows.append(dict(panel=pname, rung=c, family=fam, gross=g, depth=d,
                                               cadence=cad, level=pk.level, w=pk.w,
                                               IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR,
                                               OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                               OOS_dSharpe=pk.dOOS, pass_4a=bool(pk.pass_4a),
                                               pass_4b=bool(pk.pass_4b), fail_4b=pk.fail_4b,
                                               SPY_OOS_CAGR=pk.SPY_OOS_CAGR,
                                               SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                                               SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD,
                                               V2_OOS_CAGR=pk.V2_OOS_CAGR,
                                               V2_OOS_Sharpe=pk.V2_OOS_Sharpe,
                                               V2_OOS_MaxDD=pk.V2_OOS_MaxDD))

        PAN[pname] = dict(eidx=eidx, csA=csA, csF=csF, csG=csG, fam=fam_of, w=w_of,
                          gross=gross_of, cs_me=cs_me, K=K, T=T, gg=gg)
        del px, GR, GT, ARM, TWF

    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------- G4/G5: the full-sample order, and the leg machinery ------------
    P(f"\n{'='*118}\nGATES G4/G5\n{'='*118}")
    g4 = True
    for scope, sel in [("POOLED", lambda d: d), ("U56", lambda d: d[d.panel == "U56"]),
                       ("B136", lambda d: d[d.panel == "B136"]),
                       ("SMALL663", lambda d: d[d.panel == "SMALL663"])]:
        for c in RUNGS:
            s = sel(AR[AR.rung == c])
            rates = {f: float(s[s.family == f].win.mean()) for f in FAMS}
            o_ = order_of(rates)
            ok = (o_ == PUBLISHED)
            if scope == "POOLED":
                g4 &= ok
            P(f"   G4 full-sample order {scope:<9} {c:>5.0f} bps  {' > '.join(o_):<24} "
              + "  ".join(f"{f} {rates[f]:.4f}" for f in FAMS)
              + f"   {'PASS' if ok else 'FAIL'}" + ("" if scope == "POOLED" else "  (reported)"))
    P(f"   G4 (POOLED, all rungs) reproduces idea 605's order QROLL > QEXP > ABS: "
      f"{'PASS' if g4 else 'FAIL'}")

    # G5: a leg covering the whole sample must reproduce the full-sample win rates exactly
    g5max = 0.0
    for pname, d in PAN.items():
        for c in RUNGS:
            sa = d["csA"][c].sharpe(0, d["T"])
            st = d["csF"][c].sharpe(0, d["T"])
            leg = (sa - st > TIE)
            ref = AR[(AR.panel == pname) & (AR.rung == c)].win.values
            g5max = max(g5max, float(np.abs(leg.astype(float) - ref.astype(float)).max()))
    P(f"   G5 whole-sample leg == full-sample win rates      max|d| {g5max:.3e} "
      f"{'PASS' if g5max == 0 else 'FAIL'}")

    # ---------------- the grid: 20 tuned points x rung x matching x scope ------------
    P(f"\n{'='*118}\nTHE GRID - every one of the {len(SPLITS)*len(FAMSETS)} tuned points, at every")
    P("reported axis.  adv = win[QROLL] - max(win[ABS], win[QEXP]); adv > 0 is 'QROLL on top'.")
    P(f"{'='*118}")

    def leg_rates(pname, c, a, b, matching, ws):
        """win rates per family on [a,b) for one panel/rung/matching/famset."""
        d = PAN[pname]
        sa = d["csA"][c].sharpe(a, b)
        if matching == "FULLMATCH":
            st = d["csF"][c].sharpe(a, b)
        else:
            n = b - a
            gm = (d["cs_me"][:, b] - d["cs_me"][:, a]) / n * d["gross"]
            lo = np.floor(np.round(gm, 6) / GSTEP).astype(int)
            lo = np.clip(lo, 0, len(d["gg"]) - 2)
            lam = (gm - d["gg"][lo]) / GSTEP
            st = d["csG"][c].sharpe(a, b, lo, lam)
        sel = (d["fam"] != "QROLL") | np.isin(d["w"], ws)
        out = {}
        for f in FAMS:
            m = sel & (d["fam"] == f) & np.isfinite(sa) & np.isfinite(st)
            out[f] = float((sa[m] - st[m] > TIE).mean()) if m.sum() else np.nan
            out[f + "_n"] = int(m.sum())
        return out

    def pooled_rates(c, splitdate, legname, matching, ws):
        num = {f: 0 for f in FAMS}
        den = {f: 0 for f in FAMS}
        per = {}
        for pname, d in PAN.items():
            cut = int(d["eidx"].searchsorted(pd.Timestamp(splitdate), side="right"))
            a, b = (0, cut) if legname == "PRE" else (cut, d["T"])
            if b - a < MINLEG:
                per[pname] = None
                continue
            r = leg_rates(pname, c, a, b, matching, ws)
            per[pname] = r
            for f in FAMS:
                num[f] += r[f] * r[f + "_n"]
                den[f] += r[f + "_n"]
        pool = {f: (num[f] / den[f] if den[f] else np.nan) for f in FAMS}
        pool.update({f + "_n": den[f] for f in FAMS})
        return pool, per

    def adv_of(r):
        if any(not np.isfinite(r[f]) for f in FAMS):
            return np.nan
        return r["QROLL"] - max(r["ABS"], r["QEXP"])

    hdr = (f"   {'split':<11}{'famset':<7}{'rung':>5} {'match':<10}{'scope':<9}"
           f"{'leg':<5}{'ABS':>8}{'QEXP':>8}{'QROLL':>8}{'adv':>9}  order")
    for splitdate in SPLITS:
        for fsname, ws in FAMSETS.items():
            head_pt = (splitdate == SPLIT_HEAD and fsname == FAMSET_HEAD)
            P(f"\n   -- split {splitdate}  famset {fsname} (QROLL w {ws}) "
              + ("  <== HEADLINE" if head_pt else ""))
            P(hdr)
            for c in RUNGS:
                for matching in ["FULLMATCH", "WINMATCH"]:
                    for legname in ["PRE", "POST"]:
                        pool, per = pooled_rates(c, splitdate, legname, matching, ws)
                        for scope in ["POOLED", "U56", "B136", "SMALL663"]:
                            r = pool if scope == "POOLED" else per.get(scope)
                            if r is None:
                                continue
                            a_ = adv_of(r)
                            gridrows.append(dict(split=splitdate, famset=fsname, rung=c,
                                                 matching=matching, scope=scope, leg=legname,
                                                 ABS=r["ABS"], QEXP=r["QEXP"], QROLL=r["QROLL"],
                                                 adv=a_, order=" > ".join(order_of(r)),
                                                 n_ABS=r["ABS_n"], n_QEXP=r["QEXP_n"],
                                                 n_QROLL=r["QROLL_n"], headline=head_pt))
                            if scope == "POOLED" or head_pt:
                                P(f"   {splitdate:<11}{fsname:<7}{c:>5.0f} {matching:<10}"
                                  f"{scope:<9}{legname:<5}{r['ABS']:>8.4f}{r['QEXP']:>8.4f}"
                                  f"{r['QROLL']:>8.4f}{a_:>9.4f}  {' > '.join(order_of(r))}")
    GD = pd.DataFrame(gridrows)
    GD.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- hypotheses ----------------------------------------------------
    P(f"\n{'='*118}\nPRE-REGISTERED HYPOTHESES\n{'='*118}")

    def cell(split=SPLIT_HEAD, fs=FAMSET_HEAD, rung=RUNG_HEAD, match="FULLMATCH",
             scope="POOLED", leg="PRE"):
        q = GD[(GD.split == split) & (GD.famset == fs) & (GD.rung == rung)
               & (GD.matching == match) & (GD.scope == scope) & (GD.leg == leg)]
        return q.iloc[0] if len(q) else None

    H = {}
    hc = cell()
    hp = cell(leg="POST")
    H["H_PRE"] = (hc.adv > 0, f"adv_PRE {hc.adv:+.4f} at the headline "
                              f"(ABS {hc.ABS:.4f} QEXP {hc.QEXP:.4f} QROLL {hc.QROLL:.4f}; "
                              f"order {hc.order})")
    H["H_PREPOS"] = (hc.QROLL > 0.50, f"win[QROLL] on the PRE leg {hc.QROLL:.4f}")
    gap = abs(hc.adv - hp.adv)
    H["H_GAP"] = (gap <= 0.20, f"|adv_PRE - adv_POST| = |{hc.adv:+.4f} - {hp.adv:+.4f}| = {gap:.4f}"
                               f"  (POST order {hp.order})")
    sg = [cell(split=s).adv for s in SPLITS]
    H["H_SPLITFREE"] = (len({np.sign(x) for x in sg}) == 1,
                        "adv_PRE by split " + ", ".join(f"{s[:4]} {v:+.4f}" for s, v in zip(SPLITS, sg)))
    fg = [cell(fs=f).adv for f in FAMSETS]
    H["H_FAMSET"] = (len({np.sign(x) for x in fg}) == 1,
                     "adv_PRE by famset " + ", ".join(f"{f} {v:+.4f}" for f, v in zip(FAMSETS, fg)))
    cg = [cell(rung=c).adv for c in RUNGS]
    H["H_COSTINV"] = (len({np.sign(x) for x in cg}) == 1,
                      "adv_PRE by rung " + ", ".join(f"{c:g}bps {v:+.4f}" for c, v in zip(RUNGS, cg)))
    mw = cell(match="WINMATCH")
    H["H_MATCH"] = (abs(hc.adv - mw.adv) <= 0.10,
                    f"adv_PRE FULLMATCH {hc.adv:+.4f} vs WINMATCH {mw.adv:+.4f}, "
                    f"|d| {abs(hc.adv-mw.adv):.4f}")
    pg = [cell(scope=s).adv for s in ["U56", "B136", "SMALL663"]]
    H["H_PANEL"] = (len({np.sign(x) for x in pg}) == 1,
                    "adv_PRE by panel " + ", ".join(f"{s} {v:+.4f}" for s, v
                                                    in zip(["U56", "B136", "SMALL663"], pg)))

    # rule 8 on the CLAIM: choose the famset on the FIRST half by adv, read the SECOND half once
    pick = max(FAMSETS, key=lambda f: cell(fs=f, leg="PRE").adv)
    a_is = cell(fs=pick, leg="PRE").adv
    a_oos = cell(fs=pick, leg="POST").adv
    H["H_R8CLAIM"] = (abs(a_is - a_oos) <= 0.10,
                      f"famset chosen on the PRE leg = {pick} (adv_PRE {a_is:+.4f}); read ONCE on "
                      f"the POST leg adv {a_oos:+.4f}, gap {abs(a_is-a_oos):.4f}")
    for k, (ok, why) in H.items():
        P(f"   {k:<12} {'PASS' if ok else 'FAIL'}   {why}")

    # ---------------- rule 8 on the BOOKS, and both KEEP paths ----------------------
    P(f"\n{'='*118}\nPROTOCOL RULE 8 ON THE BOOKS, and BOTH KEEP PATHS\n{'='*118}")
    P(f"   dial (level, w) chosen on IS (..{IS_END}) by IS Sharpe; OOS ({OOS_START}..) read ONCE.")
    P(f"   {'panel':<9}{'rung':>5} {'family':<7}{'picks':>6}{'OOS CAGR':>10}{'OOS Sh':>8}"
      f"{'OOS DD':>9} | {'v2 CAGR':>9}{'v2 Sh':>7}{'v2 DD':>8} | {'SPY CAGR':>9}{'SPY Sh':>7}"
      f"{'SPY DD':>8} |{'4a':>4}{'4b':>4}")
    for pname in ["U56", "B136", "SMALL663"]:
        for c in RUNGS:
            for fam in FAMS:
                s = WF[(WF.panel == pname) & (WF.rung == c) & (WF.family == fam)]
                if s.empty:
                    continue
                P(f"   {pname:<9}{c:>5.0f} {fam:<7}{len(s):>6}{s.OOS_CAGR.mean():>10.2%}"
                  f"{s.OOS_Sharpe.mean():>8.3f}{s.OOS_MaxDD.mean():>9.2%} | "
                  f"{s.V2_OOS_CAGR.iloc[0]:>9.2%}{s.V2_OOS_Sharpe.iloc[0]:>7.3f}"
                  f"{s.V2_OOS_MaxDD.iloc[0]:>8.2%} | {s.SPY_OOS_CAGR.iloc[0]:>9.2%}"
                  f"{s.SPY_OOS_Sharpe.iloc[0]:>7.3f}{s.SPY_OOS_MaxDD.iloc[0]:>8.2%} |"
                  f"{int(s.pass_4a.sum()):>4}{int(s.pass_4b.sum()):>4}")
    P(f"\n   FULL-SAMPLE KEEP paths over all {len(AR)} (panel, arm, rung) rows:")
    for pname in ["U56", "B136", "SMALL663"]:
        for c in RUNGS:
            s = AR[(AR.panel == pname) & (AR.rung == c)]
            n4b = int(s.pass_4b.sum())
            twinpass = int(s[s.pass_4b].twin_pass_4b.sum()) if n4b else 0
            P(f"   {pname:<9}{c:>5.0f} bps   4a {int(s.pass_4a.sum()):>3}/{len(s):<4} "
              f"4b {n4b:>3}/{len(s):<4}  of the 4b passers, {twinpass} have a twin that ALSO "
              f"passes 4b (exposure, not clause)")
    n4a = int(AR.pass_4a.sum())
    n4b = int(AR.pass_4b.sum())
    n4bw = int(WF.pass_4b.sum())
    P(f"   TOTAL full-sample: 4a {n4a}/{len(AR)}, 4b {n4b}/{len(AR)};  rule-8 picks: "
      f"4a {int(WF.pass_4a.sum())}/{len(WF)}, 4b {n4bw}/{len(WF)}")

    # ---------------- verdict --------------------------------------------------------
    P(f"\n{'='*118}\nVERDICT\n{'='*118}")
    npass = sum(1 for ok, _ in H.values() if ok)
    P(f"   {npass} of {len(H)} pre-registered hypotheses PASS.")
    P(f"   Headline (split {SPLIT_HEAD}, famset {FAMSET_HEAD}, {RUNG_HEAD:g} bps, FULLMATCH, "
      f"POOLED):")
    P(f"     PRE  leg  {hc.order:<26} ABS {hc.ABS:.4f}  QEXP {hc.QEXP:.4f}  QROLL {hc.QROLL:.4f}"
      f"  adv {hc.adv:+.4f}")
    P(f"     POST leg  {hp.order:<26} ABS {hp.ABS:.4f}  QEXP {hp.QEXP:.4f}  QROLL {hp.QROLL:.4f}"
      f"  adv {hp.adv:+.4f}")
    ans = ("YES - QROLL-on-top is a POST-split fact" if (hc.adv <= 0 and hp.adv > 0)
           else ("NO - QROLL is on top on BOTH legs" if (hc.adv > 0 and hp.adv > 0)
                 else "NEITHER - QROLL is not on top on the POST leg either"))
    P(f"   ANSWER: {ans}")
    P(f"   KEEP claimed: none - this run prices a published ORDER, not a book; the KEEP paths above")
    P(f"   are reported for every arm as PROTOCOL requires and no arm is promoted by this script.")
    P(f"\n   runtime {time.time()-T0:.1f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return H, hc, hp, AR, WF, GD, ans


if __name__ == "__main__":
    main()
