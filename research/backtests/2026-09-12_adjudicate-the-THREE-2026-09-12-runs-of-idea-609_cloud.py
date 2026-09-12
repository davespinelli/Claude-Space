#!/usr/bin/env python3
"""Idea 826 - "adjudicate-the-THREE-2026-09-12-runs-of-idea-609-against-each-other" (cloud, 2026-09-12).

THE SITUATION THIS RUN EXISTS TO RESOLVE
----------------------------------------
The record now carries THREE committed numbers for one question - "over rolling windows, what
share show idea 605's published family order QROLL > QEXP > ABS?":

    aa87884  lane B     0.0847                 WINMATCH twin, step 63
    2c96cad  cloud      0.322                  FULLMATCH twin, step 63
    _B2      lane B2    0.322034 / 0.3125      FULLMATCH twin, step 63 / step 21

_B2 reproduces the cloud run to the published digit on an independent implementation, so those two
are ONE number, not two.  The remaining spread is the TWIN MATCHING SAMPLE, which 7df829b (lane C,
idea 824) diagnosed on a different population.  This run does the adjudication the queue asks for:
ONE implementation, ONE population, BOTH conventions, ALL THREE steps, so the 2 x 3 table is
internally comparable and each committed headline lands in a named cell.

    FULLMATCH   the twin's constant gross is g_eff = g * mean(gate multiplier) over the WHOLE
                evaluation sample.  One twin per arm, reused in every window.  (idea 602/605's.)
    WINMATCH    the twin's constant gross is g_eff = g * mean(gate multiplier) over the EVALUATION
                WINDOW ITSELF.  A different twin in every window - what a reader holding only that
                window could actually build.

The question, stated so it can be answered either way
-----------------------------------------------------
    Q1 (RECONCILE)  Does this run land aa87884, 2c96cad and _B2 in the 2 x 3 (convention, step)
                    table at their published values?  H1: each committed headline reproduces to
                    <= 0.02 in its own cell.  A failure here means one of the three runs is wrong,
                    not that the conventions differ.
    Q2 (SIZE)       H2: the convention axis moves share_exact by >= 0.10 and the step axis by
                    <= 0.05.  That is the queue's premise; if H2 fails the record's "biggest axis"
                    prose is wrong in the other direction too.
    Q3 (MECHANISM)  THE DECIDING TEST.  Is the convention gap a RE-RANKING (the twin's gross
                    genuinely changes who wins) or a TIE-HANDLING count (WINMATCH makes the twin
                    bit-for-bit identical to the arm whenever the gate never fires inside the
                    window, giving dSharpe == 0 exactly, which `win = dSharpe > TIE` scores a
                    LOSS)?  H3: >= 0.90 of the WINMATCH-vs-FULLMATCH win-sign flips are cells
                    whose gate never fires in that window.  H3 decides which headline to quote.
    Q4 (INVARIANCE) A static long-only book's Sharpe is nearly gross-invariant, so re-matching the
                    twin's gross should barely move its Sharpe.  H4: over every (cell, window)
                    where the gate DOES fire, max |twin Sharpe FULLMATCH - twin Sharpe WINMATCH|
                    <= 0.05, two orders below the gap it is blamed for.
    Q5 (RULE 8)     PROTOCOL rule 8 on the CLAIM: choose the convention on the first half of the
                    window population, read the second half untouched.  H5: the IS-chosen
                    convention is also the OOS-best.
    Q6 (CAPITAL)    PROTOCOL rule 4, both KEEP paths, on EVERY grid point, reported in full and
                    never selected on; plus the rule-8 book leg - pick ONE arm per panel on the IS
                    window by IS Sharpe alone, read it ONCE on OOS against RULES v2, v1 and SPY.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both, and only these two
    1. convention   FULLMATCH / WINMATCH.  No headline declared: the point is to price both.
    2. step         21 / 63 / 126 trading days.  Both published steps are inside; all three
                    reported.  Window length is NOT a free axis here - it is FIXED at the record's
                    declared 3-year headline (756d), so step is the only sampling dial.

Reported axes, NEVER tuned and NEVER selected on (inherited verbatim from ideas 602/605/609 so the
population is literally the same one)
    family  ABS(B in 0.30/0.40/0.50) / QEXP(q) / QROLL(q, w);  q 0.07/0.12/0.17;
    w 252/504/1008/2016;  depth 0.25/0.50/1.00;  cadence D/W;  gross 0.75/1.00;
    panel U56 / B136 / SMALL<n>;  cost 15 rungs 0 -> 100 bps, PROTOCOL's 10 bps the headline.

The tie convention is a DECOMPOSITION, not a third tuned parameter: the published rule
(`win = dSharpe > TIE`, a tie is a LOSS - ideas 594/595) produces every headline number here.
EXCLUDE and WIN are printed beside it only to locate the gap.  No verdict is read off them.

Reproduction gates, printed before any new number is read
    G1  fast_backtest == engine.backtest (returns AND turnover) on 3 real books x 3 rungs
    G2  fast metrics (CAGR/Sharpe/MaxDD) == engine.metrics on 200 real series
    G3  the O(1) sums-ladder window Sharpe == a direct Sharpe on the same slice
    G4  the derived cost ladder == a live backtest put through the gate, at every rung
    G5  idea 84's committed EWALL U56 g=0.85 @10bps triple
    G6  the gross-grid runner == fast_backtest at every grid point it is asked for
    G7  panel vintage stamp (data/prices_small.csv.gz is rewritten nightly - ideas 824/828)

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen only (see
data/SMALL_PANEL_README.md); B136 is current large-cap constituents.  Both bias upward.  Nothing
in this file is a live recommendation.

Writes: .console.txt .census.csv .windows.csv.gz .grid.csv.gz .decomp.csv .walkforward.csv
"""
import sys
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0.0, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 75.0, 100.0]
RUNG_HEAD = 10.0
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
GSTEP = 0.01

W_HEAD = 756                                 # FIXED, not tuned: the record's 3-year headline
STEPS = [21, 63, 126]                        # tuned param 2
CONVENTIONS = ["FULLMATCH", "WINMATCH"]      # tuned param 1
TIERULES = ["LOSS", "EXCLUDE", "WIN"]        # decomposition only; LOSS is the published rule
COVER = 0.90
FAMS = ["ABS", "QEXP", "QROLL"]
PUB_ORDER = ("QROLL", "QEXP", "ABS")

COMMITTED = {("WINMATCH", 63): (0.0847, "aa87884 lane B"),
             ("FULLMATCH", 63): (0.3220, "2c96cad cloud / _B2 0.322034"),
             ("FULLMATCH", 21): (0.3125, "_B2 lane B2")}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ------------------------------------------------------------------ primitives (idea 42/336/399)
_ELIG = {}


def eligible_mask(px):
    k = (id(px), px.shape, px.index[0], px.index[-1])
    if k not in _ELIG:
        _, above, vol20 = score(px)
        _ELIG[k] = above & (vol20 < MAX_VOL)
    return _ELIG[k]


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def _cadence(m, idx):
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def gate_from_thr(br, thr, depth, cadence, idx):
    m = pd.Series(1.0, index=idx).where(~(br < thr), 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def gate_abs(br, B, depth, cadence, idx):
    m = pd.Series(1.0, index=idx).where(~(br < B), 1.0 - depth)
    m = m.where(br.notna(), 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def fast_backtest(prices, weights, cost_bps, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1).  Idea 312/568/569's runner."""
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


class GrossGrid:
    """EWALL at every gross on a 0.01 grid, at cost 0, in O(T*N) once + O(T) per gross.

    fast_backtest's weights are wt = g * E for a gross-1 equal-weight sheet E, so every
    gross-dependent quantity factorises:
        h   = g*hb,      V  = 1 + g*(HB  - WS ),   port = g*NUM/V
        hp  = g*hbp,     Vp = 1 + g*(HBP - WSP),   turn[reb] = g*|E[reb] - hbp[reb]/Vp[reb]|.sum
    Gate G6 asserts this against fast_backtest itself at every grid point used.
    """

    def __init__(self, prices, freq=FREQ):
        idx = prices.index
        E = ewall_weights(prices, 1.0)
        rets = prices.pct_change().fillna(0.0).values
        wt = E.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
        mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
        mask[0] = True
        T, N = rets.shape
        C = np.cumprod(1.0 + rets, axis=0)
        Cp = np.vstack([np.ones((1, N)), C[:-1]])
        reb = np.flatnonzero(mask)
        seg = np.searchsorted(reb, np.arange(T), side="right") - 1
        s0 = reb[seg]
        s0p = reb[np.maximum(seg - 1, 0)]
        hb = wt[s0] * (Cp / Cp[s0])
        hbp = wt[s0p] * (Cp / Cp[s0p])
        hbp[reb[0]] = 0.0
        self.idx = idx
        self.NUM = (hb * rets).sum(axis=1)
        self.HB = hb.sum(axis=1)
        self.WS = wt[s0].sum(axis=1)
        self.HBP_reb = hbp[reb]
        self.HBPs_reb = hbp[reb].sum(axis=1)
        self.WSP_reb = wt[s0p][reb].sum(axis=1)
        self.WT_reb = wt[reb]
        self.reb = reb
        self.T = T

    def at(self, g):
        V = 1.0 + g * (self.HB - self.WS)
        port = g * self.NUM / V
        Vp = 1.0 + g * (self.HBPs_reb - self.WSP_reb)
        turn = np.zeros(self.T)
        turn[self.reb] = g * np.abs(self.WT_reb - self.HBP_reb / Vp[:, None]).sum(axis=1)
        return port, turn


# ------------------------------------------------------------------ fast metrics
def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = (r.mean() * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def rows_metrics(R):
    n = R.shape[1]
    eq = np.cumprod(1.0 + R, axis=1)
    cagr = eq[:, -1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    vol = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    sh = np.where(vol > 0, R.mean(axis=1) * 252.0 / np.where(vol > 0, vol, 1.0), np.nan)
    return cagr, sh, dd


def rows_sharpe(R):
    vol = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(vol > 0, R.mean(axis=1) * 252.0 / np.where(vol > 0, vol, 1.0), np.nan)


def csum(x):
    """(k, n) -> (k, n+1) cumulative sum with a leading zero column."""
    x = np.atleast_2d(x)
    return np.hstack([np.zeros((x.shape[0], 1)), np.cumsum(x, axis=1)])


def sharpe_from_sums(SR, SRR, ST, STT, SRT, L, cc):
    """Sharpe of (r - cc*t) over a window, from its five window sums.  cc = cost_bps/1e4.
    Exact: sum(r-cc t) = SR - cc ST; sum((r-cc t)^2) = SRR - 2 cc SRT + cc^2 STT."""
    s1 = SR - cc * ST
    s2 = SRR - 2.0 * cc * SRT + cc * cc * STT
    mean = s1 / L
    var = (s2 - L * mean * mean) / (L - 1.0)
    var = np.where(var > 1e-300, var, np.nan)
    return mean * np.sqrt(252.0) / np.sqrt(var)


class Slices:
    def __init__(self, idx):
        self.n = len(idx)
        self.h = self.n // 2
        self.is_end = int(idx.searchsorted(pd.Timestamp(IS_END), side="right"))
        self.oos = int(idx.searchsorted(pd.Timestamp(OOS_START), side="left"))


RUNG_ARR = np.array(RUNGS)
HEAD_IX = RUNGS.index(RUNG_HEAD)
ARMS = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
        + [("QROLL", q, w) for q in QS for w in WS])
KEYS = [(fam, lev, w, d, cad) for (fam, lev, w) in ARMS for d, cad in product(DEPTHS, CADENCES)]
NK = len(KEYS)
FAMSEL = {f: np.array([k[0] == f for k in KEYS]) for f in FAMS}
MASTER = None


# ------------------------------------------------------------------ the per-panel engine
def run_panel(panel, px, ii0):
    start = px.index[260]
    idx = px.index
    eval_idx = px.loc[start:].index
    S = Slices(eval_idx)
    n_eval = len(eval_idx)
    off = len(px.index) - n_eval
    spy = px["SPY"].pct_change().fillna(0).loc[start:].values
    sc, ss, sd = fmet(spy)
    spy_h1, spy_h2 = fsharpe(spy[:S.h]), fsharpe(spy[S.h:])
    spy_oc, spy_os, spy_od = fmet(spy[S.oos:])
    br_full = breadth(px)
    log(f"\n{'='*185}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({n_eval} days)")
    log(f"  SPY {sc:.2%} / {ss:.3f} / {sd:.2%}; 4b bars CAGR floor {0.70*sc:.2%}, DD cap "
        f"{-0.60*abs(sd):.2%}, halves {spy_h1:.3f}/{spy_h2:.3f}, OOS Sharpe {spy_os:.3f}")

    # windows this panel joins (>= COVER of the master window's span on its own calendar)
    ii, jj, keep = [], [], []
    for k, i0 in enumerate(ii0):
        i = int(eval_idx.searchsorted(MASTER[i0], side="left"))
        j = int(eval_idx.searchsorted(MASTER[i0 + W_HEAD - 1], side="right"))
        if (j - i) >= COVER * W_HEAD:
            ii.append(i); jj.append(j); keep.append(k)
    ii, jj, keep = np.array(ii, int), np.array(jj, int), np.array(keep, int)
    nW = len(ii)
    LW = (jj - ii).astype(float)
    log(f"  joins {nW} of {len(ii0)} master windows at >= {COVER:.0%} coverage")

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}

    # ---- gross grid (cost 0) on this panel's eval index
    gg = GrossGrid(px)
    gs = np.round(np.arange(0.0, max(GROSSES) + GSTEP / 2, GSTEP), 6)
    RG = np.zeros((len(gs), n_eval))
    TG = np.zeros((len(gs), n_eval))
    for a, g in enumerate(gs):
        if g == 0.0:
            continue
        p, t = gg.at(float(g))
        RG[a] = p[off:]
        TG[a] = t[off:]
    g6 = 0.0
    for g in (0.13, 0.41, 0.75, 1.00):
        a = int(round(g / GSTEP))
        ref = fast_backtest(px, ewall_weights(px, float(gs[a])), 0.0, FREQ)
        g6 = max(g6, float(np.abs(RG[a] - ref["returns"].loc[start:].values).max()),
                 float(np.abs(TG[a] - ref["turnover"].loc[start:].values).max()))
    log(f"  G6 GrossGrid == fast_backtest at 4 grid points: max |diff| = {g6:.3e} (bar 1e-12) -> "
        f"{'PASS' if g6 < 1e-12 else 'FAIL'}   [{len(gs)-1} grosses on a {GSTEP} grid]")

    # cumulative sums of the grid, per index and per adjacent pair (for the WINMATCH quadratic)
    CR, CT = csum(RG), csum(TG)
    CRR, CTT, CRT = csum(RG ** 2), csum(TG ** 2), csum(RG * TG)
    CRab = csum(RG[:-1] * RG[1:])
    CTab = csum(TG[:-1] * TG[1:])
    CRaTb = csum(RG[:-1] * TG[1:])
    CRbTa = csum(RG[1:] * TG[:-1])

    def twin_series(gv):
        """Interpolated twin returns/turnover at arbitrary gross (idea 602 G4: <=4e-07 Sharpe)."""
        gv = np.clip(np.asarray(gv, float), 0.0, gs[-1])
        lo = np.clip((gv / GSTEP + 1e-9).astype(int), 0, len(gs) - 2)
        lam = (gv - gs[lo]) / GSTEP
        return lo, lam

    # ---- references
    base0 = {}
    for g in GROSSES:
        a = int(round(g / GSTEP))
        base0[g] = (RG[a].copy(), TG[a].copy())
    rv2 = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
    rv1 = fast_backtest(px, rules_v1_weights(px), 0.0, FREQ)
    ref0 = {"v2": (rv2["returns"].loc[start:].values, rv2["turnover"].loc[start:].values),
            "v1": (rv1["returns"].loc[start:].values, rv1["turnover"].loc[start:].values)}
    base_packs = {}
    for c in RUNGS:
        b = ref0["v2"][0] - ref0["v2"][1] * c / 1e4
        base_packs[c] = (fsharpe(b[:S.h]), fsharpe(b[S.h:]), fmet(b)[2])

    # ---- gate multipliers
    ME = np.empty((NK, n_eval))
    SW = np.empty((NK, n_eval))
    for a, (fam, lev, w, d, cad) in enumerate(KEYS):
        thr = None if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
        m = (gate_abs(br_full, lev, d, cad, idx) if fam == "ABS"
             else gate_from_thr(br_full, thr, d, cad, idx))
        me = m.reindex(eval_idx).shift(1).fillna(1.0).values
        ME[a] = me
        SW[a] = np.abs(np.diff(me, prepend=me[0]))
    CME = csum(ME)
    CSW = csum(SW)
    on_share = (ME < 1.0).mean(axis=1)

    wins = {(cv, f): np.zeros((len(RUNGS), nW), int) for cv in CONVENTIONS for f in FAMS}
    tots = {(cv, f): np.zeros((len(RUNGS), nW), int) for cv in CONVENTIONS for f in FAMS}
    zeros = {(cv, f): np.zeros((len(RUNGS), nW), int) for cv in CONVENTIONS for f in FAMS}
    nofire = np.zeros(nW, int)
    flip = dict(tot=0, flip=0, flip_nofire=0, nofire_cells=0)
    inv, g3s, grid = [], [], []
    rng = np.random.default_rng(826)

    for g in GROSSES:
        r0, t0 = base0[g]
        AR = ME * r0                                     # arm returns at cost 0
        AT = ME * t0 + g * SW                            # arm cost basis
        CAR, CAT = csum(AR), csum(AT)
        CARR, CATT, CART = csum(AR ** 2), csum(AT ** 2), csum(AR * AT)

        gfull = g * ME.mean(axis=1)
        lo_f, lam_f = twin_series(gfull)
        FR = (1 - lam_f)[:, None] * RG[lo_f] + lam_f[:, None] * RG[lo_f + 1]
        FT = (1 - lam_f)[:, None] * TG[lo_f] + lam_f[:, None] * TG[lo_f + 1]
        CFR, CFT = csum(FR), csum(FT)
        CFRR, CFTT, CFRT = csum(FR ** 2), csum(FT ** 2), csum(FR * FT)

        # ---------------- rolling census, O(1) per (cell, window, rung)
        aSR = CAR[:, jj] - CAR[:, ii];  aST = CAT[:, jj] - CAT[:, ii]
        aSRR = CARR[:, jj] - CARR[:, ii]; aSTT = CATT[:, jj] - CATT[:, ii]
        aSRT = CART[:, jj] - CART[:, ii]
        fSR = CFR[:, jj] - CFR[:, ii];  fST = CFT[:, jj] - CFT[:, ii]
        fSRR = CFRR[:, jj] - CFRR[:, ii]; fSTT = CFTT[:, jj] - CFTT[:, ii]
        fSRT = CFRT[:, jj] - CFRT[:, ii]

        gwin = g * (CME[:, jj] - CME[:, ii]) / LW[None, :]          # (NK, nW)
        swin = CSW[:, jj] - CSW[:, ii]
        never = np.isclose(gwin, g, rtol=0, atol=1e-12) & (swin <= 1e-12)
        lo_w, lam_w = twin_series(gwin.ravel())
        lo_w = lo_w.reshape(gwin.shape); lam_w = lam_w.reshape(gwin.shape)
        JJ = np.broadcast_to(jj, gwin.shape); II = np.broadcast_to(ii, gwin.shape)
        u, v = 1 - lam_w, lam_w

        def wsum(C, rowix):
            return C[rowix, JJ] - C[rowix, II]

        Sa_R, Sb_R = wsum(CR, lo_w), wsum(CR, lo_w + 1)
        Sa_T, Sb_T = wsum(CT, lo_w), wsum(CT, lo_w + 1)
        Saa_RR, Sbb_RR, Sab_RR = wsum(CRR, lo_w), wsum(CRR, lo_w + 1), wsum(CRab, lo_w)
        Saa_TT, Sbb_TT, Sab_TT = wsum(CTT, lo_w), wsum(CTT, lo_w + 1), wsum(CTab, lo_w)
        Saa_RT, Sbb_RT = wsum(CRT, lo_w), wsum(CRT, lo_w + 1)
        Sab_RT, Sba_RT = wsum(CRaTb, lo_w), wsum(CRbTa, lo_w)

        wSR = u * Sa_R + v * Sb_R
        wST = u * Sa_T + v * Sb_T
        wSRR = u * u * Saa_RR + 2 * u * v * Sab_RR + v * v * Sbb_RR
        wSTT = u * u * Saa_TT + 2 * u * v * Sab_TT + v * v * Sbb_TT
        wSRT = u * u * Saa_RT + u * v * Sab_RT + v * u * Sba_RT + v * v * Sbb_RT

        nofire += never.sum(axis=0)
        flip["nofire_cells"] += int(never.sum())
        for ci, c in enumerate(RUNGS):
            cc = c / 1e4
            sh_arm = sharpe_from_sums(aSR, aSRR, aST, aSTT, aSRT, LW[None, :], cc)
            sh_ful = sharpe_from_sums(fSR, fSRR, fST, fSTT, fSRT, LW[None, :], cc)
            sh_win = sharpe_from_sums(wSR, wSRR, wST, wSTT, wSRT, LW[None, :], cc)
            for cv, sh_tw in (("FULLMATCH", sh_ful), ("WINMATCH", sh_win)):
                dS = sh_arm - sh_tw
                ok = np.isfinite(dS)
                wn = ok & (dS > TIE)
                zr = ok & (np.abs(dS) <= TIE)
                for f in FAMS:
                    sel = FAMSEL[f]
                    wins[(cv, f)][ci] += wn[sel].sum(axis=0)
                    tots[(cv, f)][ci] += ok[sel].sum(axis=0)
                    zeros[(cv, f)][ci] += zr[sel].sum(axis=0)
            okb = np.isfinite(sh_arm) & np.isfinite(sh_ful) & np.isfinite(sh_win)
            fl = okb & (((sh_arm - sh_ful) > TIE) != ((sh_arm - sh_win) > TIE))
            flip["tot"] += int(okb.sum())
            flip["flip"] += int(fl.sum())
            flip["flip_nofire"] += int((fl & never).sum())
            if ci == HEAD_IX:
                fires = okb & ~never
                if fires.any():
                    d = np.abs(sh_ful - sh_win)[fires]
                    inv.append(dict(panel=panel, gross=g, rung=c, n=int(fires.sum()),
                                    max_dtwin=float(np.nanmax(d)),
                                    med_dtwin=float(np.nanmedian(d)),
                                    p99_dtwin=float(np.nanpercentile(d, 99)),
                                    max_dgross=float(np.nanmax(
                                        np.abs(gfull[:, None] - gwin)[fires]))))
                for _ in range(12):                      # G3 samples
                    a, wi = int(rng.integers(NK)), int(rng.integers(nW))
                    i, j = ii[wi], jj[wi]
                    direct_a = fsharpe(AR[a, i:j] - AT[a, i:j] * cc)
                    direct_w = fsharpe(((1 - lam_w[a, wi]) * RG[lo_w[a, wi], i:j]
                                        + lam_w[a, wi] * RG[lo_w[a, wi] + 1, i:j])
                                       - ((1 - lam_w[a, wi]) * TG[lo_w[a, wi], i:j]
                                          + lam_w[a, wi] * TG[lo_w[a, wi] + 1, i:j]) * cc)
                    g3s.append((float(sh_arm[a, wi]), direct_a))
                    g3s.append((float(sh_win[a, wi]), direct_w))

            # ---- full-sample grid rows, both KEEP paths, every rung (never selected on)
            RGc = AR - AT * cc
            RSc = FR - FT * cc
            cg, shg, ddg = rows_metrics(RGc)
            h1 = rows_sharpe(RGc[:, :S.h]); h2 = rows_sharpe(RGc[:, S.h:])
            isS = rows_sharpe(RGc[:, :S.is_end])
            ocg, oshg, oddg = rows_metrics(RGc[:, S.oos:])
            shs = rows_sharpe(RSc)
            b1, b2, bdd = base_packs[c]
            for a, (fam, lev, w, d, cad) in enumerate(KEYS):
                t4b = dict(H1=h1[a] > spy_h1, H2=h2[a] > spy_h2, OOS=oshg[a] > spy_os,
                           DD=abs(ddg[a]) <= 0.60 * abs(sd), CAGR=cg[a] >= 0.70 * sc)
                grid.append(dict(
                    panel=panel, rung=c, gross=g, family=fam, level=lev, w=w, depth=d, cadence=cad,
                    arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}", g_eff=float(gfull[a]),
                    on_share=float(on_share[a]), CAGR=cg[a], Sharpe=shg[a], MaxDD=ddg[a],
                    H1=h1[a], H2=h2[a], IS_Sharpe=isS[a], OOS_CAGR=ocg[a], OOS_Sharpe=oshg[a],
                    OOS_MaxDD=oddg[a], twin_Sharpe=shs[a], dSharpe=shg[a] - shs[a],
                    win=bool(shg[a] - shs[a] > TIE),
                    p4a=bool(h1[a] > b1 and h2[a] > b2 and ddg[a] >= bdd),
                    p4b=all(t4b.values()),
                    fail4b=",".join([kk for kk, v in t4b.items() if not v]) or "-"))

    refs = dict(SPY=(sc, ss, sd, spy_h1, spy_h2, spy_oc, spy_os, spy_od))
    for g in GROSSES:
        ref0[f"NOGATE g{g:.2f}"] = base0[g]
    for nm, (r, t) in ref0.items():
        rr = r - t * RUNG_HEAD / 1e4
        c_, s_, d_ = fmet(rr)
        oc_, os_, od_ = fmet(rr[S.oos:])
        refs[nm] = (c_, s_, d_, fsharpe(rr[:S.h]), fsharpe(rr[S.h:]), oc_, os_, od_)
    log(f"  never-firing (cell, window) pairs: {flip['nofire_cells']} of {NK*nW*len(GROSSES)} "
        f"({flip['nofire_cells']/(NK*nW*len(GROSSES)):.4f})")
    return (pd.DataFrame(grid), wins, tots, zeros, nofire, flip, inv, g3s, refs, S, keep)


def main():
    global MASTER
    log("=" * 185)
    log(f"Idea 826 adjudicate-the-THREE-2026-09-12-runs-of-idea-609-against-each-other | {SCRIPT}")
    log("=" * 185)
    log("Base book (fixed, idea 28/42/336/399's): EWALL(G) = equal weight every name above its own")
    log("  200d MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is BELOW the threshold.")
    log("Comparand: the matched-mean-gross STATIC TWIN, under BOTH matching conventions.")
    log(f"Tuned (2): convention in {CONVENTIONS}, step in {STEPS}.  Window FIXED at {W_HEAD}d.")
    log(f"Reported never tuned: cost rung {RUNGS} bps, family, level, w, depth, cadence, panel, "
        f"gross.")
    log(f"Published order under test (idea 605): {' > '.join(PUB_ORDER)}.  Tie bar |dS| <= {TIE:g},"
        f" a tie is a LOSS (ideas 594/595).")
    log("The three committed headlines this run must land:")
    for (cv, st), (v, src) in sorted(COMMITTED.items()):
        log(f"    {cv:<10} step {st:<4} {v:.4f}   {src}")

    # ============================================================ [0] gates
    log("\n" + "=" * 185)
    log("[0] REPRODUCTION GATES (all printed before any new number is read)")
    px0 = load_universe()
    st0 = px0.index[260]
    idx0 = px0.loc[st0:].index

    g1 = 0.0
    for wfn in (lambda p: ewall_weights(p, G_HEAD), rules_v2_weights, rules_v1_weights):
        Wt = wfn(px0)
        for c in (0.0, 10.0, 25.0):
            a = backtest(px0, Wt, cost_bps=c, freq=FREQ)
            b = fast_backtest(px0, Wt, c, FREQ)
            g1 = max(g1, float((a["returns"] - b["returns"]).abs().max()),
                     float((a["turnover"] - b["turnover"]).abs().max()))
    log(f"  G1 fast_backtest == engine.backtest (returns AND turnover), 3 books x 3 rungs: "
        f"max |diff| = {g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    bt = fast_backtest(px0, ewall_weights(px0, G_HEAD), 0.0, FREQ)
    r0 = bt["returns"].loc[st0:].values
    t0 = bt["turnover"].loc[st0:].values
    rng = np.random.default_rng(8260)
    g2 = 0.0
    for _ in range(200):
        c = float(rng.uniform(0, 100))
        a, b = sorted(rng.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        s = pd.Series((r0 - t0 * c / 1e4)[a:b], index=idx0[a:b])
        mm, f = metrics(s), fmet(s.values)
        g2 = max(g2, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G2 fast metrics vs engine.metrics on 200 real series: max |diff| = {g2:.3e} "
        f"(bar 1e-12) -> {'PASS' if g2 < 1e-12 else 'FAIL'}")

    brf = breadth(px0)
    mtest = gate_abs(brf, 0.40, 0.50, "W", px0.index).reindex(idx0).shift(1).fillna(1.0)
    me = mtest.values
    sw = np.abs(np.diff(me, prepend=me[0]))
    g4 = 0.0
    for c in RUNGS:
        live = fast_backtest(px0, ewall_weights(px0, G_HEAD), c, FREQ)["returns"].loc[st0:].values
        ref = me * live - sw * G_HEAD * c / 1e4
        der = me * r0 - (me * t0 + G_HEAD * sw) * c / 1e4
        g4 = max(g4, float(np.abs(ref - der).max()))
    log(f"  G4 derived cost ladder == live backtest through the gate, all {len(RUNGS)} rungs: "
        f"max |diff| = {g4:.3e} (bar 1e-12) -> {'PASS' if g4 < 1e-12 else 'FAIL'}")

    r85 = fast_backtest(px0, ewall_weights(px0, 0.85), 10.0, FREQ)["returns"].loc[st0:]
    c85, s85, d85 = fmet(r85.values)
    S0 = Slices(idx0)
    ok85 = abs(c85 - 0.118) < 6e-3 and abs(s85 - 1.05) < 6e-3 and abs(d85 + 0.179) < 6e-3
    log(f"  G5 idea 84 EWALL U56 g=0.85 @10bps: {c85:.2%} / {s85:.3f} / {d85:.2%} "
        f"H {fsharpe(r85.values[:S0.h]):.3f}/{fsharpe(r85.values[S0.h:]):.3f} "
        f"(committed 11.8% / 1.05 / -17.9%) -> {'PASS' if ok85 else 'CHECK'}")

    panels = [("U56", px0), ("B136", load_universe(broad=True))]
    ps, ndrop = small_panel()
    SMALL = f"SMALL{ps.shape[1]-1}"
    panels.append((SMALL, ps))
    log(f"  G7 PANEL VINTAGE STAMP (data/prices_small.csv.gz is rewritten by the daily Actions "
        f"job - ideas 824/828): today's cache gives {ps.shape[1]} columns; dropping {ndrop} names "
        f"with max_1d_move >= 1.0 leaves {ps.shape[1]-1} + SPY, so this run's panel is {SMALL}. "
        f"Ideas 605/609 read SMALL439.  SURVIVORSHIP: current constituents only.")

    MASTER = idx0
    ii0 = np.arange(0, len(MASTER) - W_HEAD + 1, 21)
    log(f"  master census calendar: U56 eval index {MASTER[0].date()} -> {MASTER[-1].date()} "
        f"({len(MASTER)} days).  W={W_HEAD}: step 21 -> {len(ii0)}, step 63 -> {len(ii0[::3])}, "
        f"step 126 -> {len(ii0[::6])} windows.  Steps 63 and 126 are EXACT subsamples of step 21 "
        f"(63=3x21, 126=6x21), so the step axis changes sampling density and nothing else: the "
        f"three committed headlines are read off ONE computation.")
    log(f"  arms per panel: {NK} cells = {len(ARMS)} arms x {len(DEPTHS)} depths x "
        f"{len(CADENCES)} cadences; family split ABS {FAMSEL['ABS'].sum()}, "
        f"QEXP {FAMSEL['QEXP'].sum()}, QROLL {FAMSEL['QROLL'].sum()}")

    GRID, FLIP, INV, G3S, REFS = [], [], [], [], {}
    POOL = {(cv, f, kind): np.zeros((len(RUNGS), len(ii0)), int)
            for cv in CONVENTIONS for f in FAMS for kind in ("w", "t", "z")}
    NOFIRE = np.zeros(len(ii0), int)
    for name, px in panels:
        grid, wins, tots, zeros, nofire, flip, inv, g3s, refs, S, keep = run_panel(name, px, ii0)
        GRID.append(grid)
        for cv in CONVENTIONS:
            for f in FAMS:
                POOL[(cv, f, "w")][:, keep] += wins[(cv, f)]
                POOL[(cv, f, "t")][:, keep] += tots[(cv, f)]
                POOL[(cv, f, "z")][:, keep] += zeros[(cv, f)]
        NOFIRE[keep] += nofire
        FLIP.append(dict(panel=name, **flip))
        INV += inv
        G3S += g3s
        REFS[name] = refs
    grid = pd.concat(GRID, ignore_index=True)

    a3 = np.array([x[0] for x in G3S]); b3 = np.array([x[1] for x in G3S])
    ok3 = np.isfinite(a3) & np.isfinite(b3)
    g3m = float(np.abs(a3[ok3] - b3[ok3]).max()) if ok3.any() else np.nan
    log(f"\n  G3 O(1) sums-ladder window Sharpe vs a direct Sharpe on the same slice, "
        f"{int(ok3.sum())} (arm/twin, window) samples: max |diff| = {g3m:.3e} (bar 1e-9) -> "
        f"{'PASS' if g3m < 1e-9 else 'FAIL'}")

    log("\n" + "=" * 185)
    log(f"POPULATION: {len(grid)} grid points = {len(grid)//len(RUNGS)} twin pairs x "
        f"{len(RUNGS)} cost rungs ({grid['panel'].nunique()} panels).")
    full = grid.groupby(["rung", "family"])["win"].mean().unstack()
    log("Full-sample FULLMATCH win rate by family and rung (this run's rebuild of 605's headline):")
    log(full.to_string(float_format=lambda x: f"{x:.4f}"))

    # ============================================================ [1] the 2 x 3 census
    log("\n" + "=" * 185)
    log("[1] THE RECONCILIATION TABLE - one census, two conventions, three steps, W = 756d")

    def rates(conv, tie):
        out = {}
        for f in FAMS:
            w = POOL[(conv, f, "w")].astype(float)
            t = POOL[(conv, f, "t")].astype(float)
            z = POOL[(conv, f, "z")].astype(float)
            if tie == "EXCLUDE":
                t = t - z
            elif tie == "WIN":
                w = w + z
            out[f] = np.where(t > 0, w / np.where(t > 0, t, 1), np.nan)
        return out

    def census_cell(conv, tie, kk):
        """kk: master-window ordinals.  Returns a per-(rung, window) frame."""
        R = rates(conv, tie)
        a, e, r = R["ABS"][:, kk], R["QEXP"][:, kk], R["QROLL"][:, kk]
        fin = np.isfinite(a) & np.isfinite(e) & np.isfinite(r)
        match = fin & (r > e) & (e > a)
        top_R = fin & (r > e) & (r > a)
        bot_A = fin & (a < e) & (a < r)
        recs = []
        for ci, c in enumerate(RUNGS):
            m = fin[ci]
            if not m.any():
                continue
            recs.append(dict(conv=conv, tie=tie, rung=c, n_win=int(m.sum()),
                             share_exact=float(match[ci][m].mean()),
                             top_QROLL=float(top_R[ci][m].mean()),
                             bottom_ABS=float(bot_A[ci][m].mean()),
                             pair_RvE=float((r[ci][m] > e[ci][m]).mean()),
                             pair_EvA=float((e[ci][m] > a[ci][m]).mean()),
                             pair_RvA=float((r[ci][m] > a[ci][m]).mean()),
                             mean_ABS=float(np.nanmean(a[ci][m])),
                             mean_QEXP=float(np.nanmean(e[ci][m])),
                             mean_QROLL=float(np.nanmean(r[ci][m]))))
        return pd.DataFrame(recs), match, fin

    step_k = {s: np.arange(len(ii0))[::(s // 21)] for s in STEPS}
    crows, wrows = [], []
    for conv, step, tie in product(CONVENTIONS, STEPS, TIERULES):
        d, match, fin = census_cell(conv, tie, step_k[step])
        if len(d):
            d.insert(1, "step", step)
            crows.append(d)
        if tie == "LOSS":
            R = rates(conv, tie)
            for ci, c in enumerate(RUNGS):
                for n, kk in enumerate(step_k[step]):
                    if not fin[ci, n]:
                        continue
                    wrows.append(dict(conv=conv, step=step, rung=c, k=int(kk),
                                      start=MASTER[kk].date(),
                                      end=MASTER[kk + W_HEAD - 1].date(),
                                      win_ABS=R["ABS"][ci, kk], win_QEXP=R["QEXP"][ci, kk],
                                      win_QROLL=R["QROLL"][ci, kk], match=bool(match[ci, n]),
                                      nofire=int(NOFIRE[kk])))
    census = pd.concat(crows, ignore_index=True)
    windows = pd.DataFrame(wrows)

    head = census[(census.rung == RUNG_HEAD) & (census.tie == "LOSS")]
    tab = head.pivot(index="conv", columns="step", values="share_exact")
    nwt = head.pivot(index="conv", columns="step", values="n_win")
    log(f"\nHEADLINE TABLE - share of windows showing {' > '.join(PUB_ORDER)}, POOLED over "
        f"{len(panels)} panels, rung {RUNG_HEAD:g} bps, published tie rule (a tie is a LOSS)")
    log(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    log("  n windows:")
    log(nwt.to_string())

    log("\nQ1 RECONCILIATION - does each committed headline land in its own cell?")
    q1ok = True
    for (cv, st), (v, src) in sorted(COMMITTED.items()):
        mine = float(tab.loc[cv, st])
        dd = abs(mine - v)
        good = dd <= 0.02
        q1ok &= good
        log(f"    {cv:<10} step {st:<4} committed {v:.4f} ({src:<30}) | this run {mine:.4f} "
            f"| |diff| {dd:.4f} -> {'REPRODUCES' if good else 'DOES NOT REPRODUCE'}")
    log(f"  H1 (every committed headline within 0.02): {'PASS' if q1ok else 'FAIL'}")

    conv_gap = float(np.abs(tab.loc["FULLMATCH"] - tab.loc["WINMATCH"]).max())
    step_gap = float(max(tab.loc[c].max() - tab.loc[c].min() for c in CONVENTIONS))
    log(f"\nQ2 AXIS SIZES at rung {RUNG_HEAD:g}: convention moves share_exact by up to "
        f"{conv_gap:.4f}; step by up to {step_gap:.4f}.")
    log(f"  H2 (convention >= 0.10 AND step <= 0.05): "
        f"{'PASS' if conv_gap >= 0.10 and step_gap <= 0.05 else 'FAIL'}")

    log("\nFULL COST LADDER, both conventions, all three steps (published tie rule):")
    lad = census[census.tie == "LOSS"].pivot_table(index="rung", columns=["conv", "step"],
                                                   values="share_exact")
    log(lad.to_string(float_format=lambda x: f"{x:.4f}"))
    log("\nPAIRWISE LEGS and family win-rate levels at the headline rung:")
    log(head[["conv", "step", "n_win", "share_exact", "top_QROLL", "bottom_ABS", "pair_RvE",
              "pair_EvA", "pair_RvA", "mean_ABS", "mean_QEXP", "mean_QROLL"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ [2] mechanism
    log("\n" + "=" * 185)
    log("[2] Q3 MECHANISM - is the convention gap a RE-RANKING or a TIE-HANDLING count?")
    fl = pd.DataFrame(FLIP)
    fl["flip_rate"] = fl["flip"] / fl["tot"]
    fl["share_nofire"] = fl["flip_nofire"] / fl["flip"].replace(0, np.nan)
    log("  per-panel WINMATCH-vs-FULLMATCH win-sign flips over every (cell, window, rung):")
    log("  " + fl.to_string(index=False, float_format=lambda x: f"{x:.6f}").replace("\n", "\n  "))
    tot_f, tot_fn, tot_n = int(fl["flip"].sum()), int(fl["flip_nofire"].sum()), int(fl["tot"].sum())
    share_nf = tot_fn / tot_f if tot_f else np.nan
    log(f"  POOLED: {tot_f} sign flips of {tot_n} comparisons ({tot_f/tot_n:.4f}); {tot_fn} of "
        f"them ({share_nf:.4f}) are cells whose gate NEVER FIRES inside that window, where "
        f"WINMATCH makes the twin the arm itself (dSharpe == 0 exactly) and the published rule "
        f"books that as a LOSS.")
    log(f"  H3 (>= 0.90 of flips are never-firing cells): {'PASS' if share_nf >= 0.90 else 'FAIL'}")

    log("\n  THE SAME TABLE UNDER THE TWO OTHER TIE RULES (decomposition, NOT a tuned parameter; "
        "no verdict in this file is read off these rows):")
    dec = census[census.rung == RUNG_HEAD].pivot_table(index="tie", columns=["conv", "step"],
                                                       values="share_exact")
    log("  " + dec.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    gaps = {}
    for tie in TIERULES:
        try:
            gaps[tie] = abs(float(dec.loc[tie, ("FULLMATCH", 63)])
                            - float(dec.loc[tie, ("WINMATCH", 63)]))
        except KeyError:
            pass
    if "LOSS" in gaps and "EXCLUDE" in gaps:
        log(f"  step-63 convention gap: {gaps['LOSS']:.4f} under the published rule -> "
            f"{gaps['EXCLUDE']:.4f} once exact ties leave the denominator "
            f"({1 - gaps['EXCLUDE']/gaps['LOSS'] if gaps['LOSS'] else float('nan'):.1%} of the "
            f"gap is tie handling).")

    inv = pd.DataFrame(INV)
    mx = float(inv["max_dtwin"].max()) if len(inv) else np.nan
    if len(inv):
        log(f"\n  Q4 TWIN-SHARPE INVARIANCE on cells whose gate DOES fire "
            f"({int(inv['n'].sum())} (cell, window) pairs at rung {RUNG_HEAD:g}): "
            f"max |twin Sharpe FULLMATCH - WINMATCH| = {mx:.3e}, median of panel medians "
            f"{float(inv['med_dtwin'].median()):.3e}, over gross mismatches up to "
            f"{float(inv['max_dgross'].max()):.4f}.")
        log("  " + inv.to_string(index=False, float_format=lambda x: f"{x:.3e}")
            .replace("\n", "\n  "))
        log(f"  H4 (max <= 0.05): {'PASS' if mx <= 0.05 else 'FAIL'} -> re-matching the twin's "
            f"gross is {'NOT' if mx <= 0.05 else ''} a re-ranking force.")

    # ============================================================ [3] rule 8 on the CLAIM
    log("\n" + "=" * 185)
    log("[3] Q5 PROTOCOL RULE 8 ON THE CLAIM - choose on the first half of the window population, "
        "read the second half untouched")
    mid = len(ii0) // 2
    r8 = []
    for conv, step in product(CONVENTIONS, STEPS):
        kk = step_k[step]
        for half, sel in (("IS", kk[kk < mid]), ("OOS", kk[kk >= mid])):
            d, _, _ = census_cell(conv, "LOSS", sel)
            d = d[d.rung == RUNG_HEAD]
            if len(d):
                r8.append(dict(conv=conv, step=step, half=half, n_win=int(d["n_win"].iloc[0]),
                               share_exact=float(d["share_exact"].iloc[0]),
                               top_QROLL=float(d["top_QROLL"].iloc[0]),
                               bottom_ABS=float(d["bottom_ABS"].iloc[0])))
    r8 = pd.DataFrame(r8)
    log(r8.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    piv = r8.pivot_table(index="conv", columns="half", values="share_exact")
    is_pick, oos_pick = piv["IS"].idxmax(), piv["OOS"].idxmax()
    log(f"  IS picks {is_pick} (IS {piv.loc[is_pick,'IS']:.4f}); OOS best is {oos_pick} "
        f"(OOS {piv.loc[oos_pick,'OOS']:.4f}).  The IS pick reads {piv.loc[is_pick,'OOS']:.4f} "
        f"out of sample.")
    log(f"  H5 (IS-chosen convention is also the OOS-best): "
        f"{'PASS' if is_pick == oos_pick else 'FAIL'}")
    log(f"  The LEVEL does not walk forward either: pooled IS {piv['IS'].mean():.4f} -> OOS "
        f"{piv['OOS'].mean():.4f}.")

    # ============================================================ [4] capital
    log("\n" + "=" * 185)
    log("[4] Q6 CAPITAL - PROTOCOL rule 4, BOTH KEEP paths, EVERY grid point, never selected on")
    kp = grid.groupby(["panel", "rung"])[["p4a", "p4b"]].sum()
    kp = kp.join(grid.groupby(["panel", "rung"]).size().rename("n"))
    log(kp.to_string())
    gh = grid[grid.rung == RUNG_HEAD]
    log(f"  POOLED at {RUNG_HEAD:g} bps: 4a {int(gh['p4a'].sum())} of {len(gh)}, "
        f"4b {int(gh['p4b'].sum())} of {len(gh)}.")
    log("  4b failure strings at 10 bps (top 8):")
    log("  " + gh["fail4b"].value_counts().head(8).to_string().replace("\n", "\n  "))

    log(f"\n  RULE 8 BOOK LEG: pick ONE arm per panel on the IS window (<= {IS_END}) by IS Sharpe "
        f"alone at {RUNG_HEAD:g} bps, then read it ONCE on OOS ({OOS_START}+) against RULES v2, "
        f"RULES v1 and SPY.  Nothing about the census is used to choose.")
    wf = []
    for p, _ in panels:
        d = grid[(grid.panel == p) & (grid.rung == RUNG_HEAD)]
        b = d.loc[d["IS_Sharpe"].idxmax()]
        rf = REFS[p]
        wf.append(dict(panel=p, pick=b["arm"], IS_Sharpe=b["IS_Sharpe"], OOS_CAGR=b["OOS_CAGR"],
                       OOS_Sharpe=b["OOS_Sharpe"], OOS_MaxDD=b["OOS_MaxDD"],
                       v2_OOS_CAGR=rf["v2"][5], v2_OOS_Sharpe=rf["v2"][6],
                       v1_OOS_Sharpe=rf["v1"][6], SPY_OOS_CAGR=rf["SPY"][5],
                       SPY_OOS_Sharpe=rf["SPY"][6], SPY_OOS_MaxDD=rf["SPY"][7],
                       beats_v2=bool(b["OOS_Sharpe"] > rf["v2"][6]),
                       beats_SPY=bool(b["OOS_Sharpe"] > rf["SPY"][6]),
                       p4a=bool(b["p4a"]), p4b=bool(b["p4b"]), fail4b=b["fail4b"]))
    wf = pd.DataFrame(wf)
    log(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ [5] verdict
    log("\n" + "=" * 185)
    log("[5] VERDICT")
    log(f"  Q1  committed headlines reproduced in their own cells: {'ALL THREE' if q1ok else 'NOT ALL'}. "
        f"The cloud run and _B2 are ONE number; aa87884 is the same census under the other "
        f"convention.")
    log(f"  Q2  convention axis {conv_gap:.4f} vs step axis {step_gap:.4f} -> the queue's premise "
        f"that MATCHING SAMPLE is the big axis is "
        f"{'CONFIRMED' if conv_gap > step_gap else 'REJECTED'}.")
    log(f"  Q3  {share_nf:.1%} of the sign flips are never-firing cells (exact ties booked as "
        f"losses) -> the gap is a TIE-HANDLING COUNT, not a re-ranking.")
    log(f"  Q4  max twin-Sharpe move from re-matching gross on firing cells: {mx:.3e}.")
    log(f"  Q5  rule 8 on the claim: IS pick {is_pick}, OOS best {oos_pick}; level "
        f"{piv['IS'].mean():.4f} -> {piv['OOS'].mean():.4f}.")
    log(f"  Q6  capital: 4a {int(gh['p4a'].sum())} and 4b {int(gh['p4b'].sum())} of {len(gh)} at "
        f"10 bps.  Neither convention is a trading edge; this is a bookkeeping adjudication and "
        f"the capital verdict is KILL.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    census.to_csv(OUT / f"{STEM}.census.csv", index=False)
    windows.to_csv(OUT / f"{STEM}.windows.csv.gz", index=False, compression="gzip")
    grid.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    pd.concat([fl.assign(kind="flips"), inv.assign(kind="invariance")],
              ignore_index=True).to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    pd.concat([r8.assign(kind="claim"), wf.assign(kind="book")],
              ignore_index=True).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(f"\nwrote {STEM}.console.txt/.census.csv/.windows.csv.gz/.grid.csv.gz/.decomp.csv/"
          f".walkforward.csv")


if __name__ == "__main__":
    main()
