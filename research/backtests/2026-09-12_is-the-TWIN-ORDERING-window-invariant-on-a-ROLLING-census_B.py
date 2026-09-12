#!/usr/bin/env python3
"""Idea 609 - "is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census" (lane B).

The claim this run exists to price
----------------------------------
Idea 605 published, as a headline, that the MATCHED-MEAN-GROSS STATIC TWIN win rate orders the
three breadth-gate families

        QROLL  >  QEXP  >  ABS

and that this ordering is COST-invariant: rho(+1.000) against its own c=0 order at all 15 rungs
from 0 to 100 bps, spread 0.4167 at zero cost.  In the same section it filed one honest caveat:

    "the ordering is cost-invariant but NOT window-invariant.  Ranked on the IS window alone the
     families read ABS < QROLL < QEXP; on OOS they read QEXP < ABS < QROLL (rho -0.500).  The
     full-sample ordering QROLL > QEXP > ABS holds at all 15 rungs; the half-window orderings
     disagree with each other."

Two halves is two draws.  The queue's question (idea 609) is the resolution question: re-rank the
three families on a ROLLING window and report how often the PUBLISHED full-sample order is the
one a reader would actually have seen.  A published ordering that a reader sees in 95% of rolling
windows is a fact about the families; one they see in 40% is a fact about the 2009-2026 sample.

Stated so it can be answered either way
---------------------------------------
    Q1 (REPRO)     Does a fresh 648-arm rebuild reproduce idea 605's committed ordering.csv win
                   rates at all 15 rungs?  If not, nothing below is about idea 605's claim.
    Q2 (HEADLINE)  On a rolling window, what share of windows read QROLL > QEXP > ABS exactly?
    Q3 (PAIRWISE)  Which of the three pairwise legs carries the instability?  A reader may care
                   only about "QROLL beats ABS", which is a weaker and possibly stabler claim.
    Q4 (GRID)      Is the answer a property of the window length / step, i.e. of the two tuned
                   dials?  All 9 grid points reported.
    Q5 (RULE 8)    Two legs, both required by PROTOCOL rule 8.
                   (a) ON THE CLAIM: measure the reproduction share on IS windows (<= 2016) only,
                       then read the OOS (2017+) share ONCE.
                   (b) ON A BOOK: use the IS rolling census as a SELECTOR - take the family that
                       leads on IS windows, take its best-IS-Sharpe arm, and read that book's
                       2017-2026 CAGR / Sharpe / MaxDD once, against the RULES v2 baseline, SPY,
                       and its own matched-gross twin.  Both KEEP paths on every arm.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. window   504 / 756 / 1008 trading days (2y / 3y / 4y).  Headline 756 = the queue's "3-year".
    2. step     21 / 63 / 126 trading days (monthly / quarterly / semiannual).  Headline 63.
    ALL 9 grid points are reported at every scope, rung and matching convention.

Reported axes, NEVER tuned or selected on (inherited verbatim from ideas 602/605 so the arm
population is literally the same one, joined row-for-row against 605's committed ordering.csv)
    family    ABS(B in 0.30/0.40/0.50) / QEXP(q) / QROLL(q, w)
    q         0.07 / 0.12 / 0.17      w  252 / 504 / 1008 / 2016
    depth     0.25 / 0.50 / 1.00      panel  U56 / B136 / SMALL439      gross  0.75 / 1.00
    cadence   D / W                   rung   0 / 10 / 25 bps (10 = PROTOCOL's, the headline)
    twin      WINDOW-matched gross (a reader inside the window matches on the window) and
              FULL-matched gross (idea 605's convention).  Both reported everywhere.

Reproduction gates, printed before any new number is read
    G1  the derived cost ladder r_gate(c) = m*r0 - (c/1e4)*(m*t0 + g*|dm|) against a LIVE
        engine.backtest put through idea 399's apply_gate, at every rung.
    G2  fast numpy CAGR/Sharpe/MaxDD against engine.metrics on 200 real series.
    G3  idea 84's committed EWALL U56 g=0.85 @10bps book.
    G4a THE ONE THAT MATTERS: an AS-OF replica of the corpus idea 605 actually read (today's
        price caches truncated to its last dates, plus the SMALL panel restored from the git
        blob it loaded) against its committed cells.csv.gz, per panel x rung x family, bar 1e-9.
        Necessary because the nightly jobs have since rewritten data/prices_small.csv.gz: the
        sub-$2B screen went from 439 tradable names to 663 in two days (idea 565's hazard).
    G4b the same statistic on TODAY's caches - the population the census below actually runs on -
        against idea 605's committed .ordering.csv, all 15 rungs x 3 families.
    G5  the O(1) window-Sharpe recursion (cumulative sums, with the twin's quadratic-in-lambda
        second moment) against a direct numpy Sharpe on 400 random (arm, window) slices.

Pre-registered hypotheses (written before the numbers, all reported either way)
    H1  G4a passes: the as-of replica reproduces idea 605's committed cells to 1e-9.  (G4b, on
        today's caches, is reported in passing and is NOT a pre-registered bar.)
    H2  The published order QROLL > QEXP > ABS is the modal reading: >= 50% of rolling windows
        at the headline grid point (756/63), pooled, 10 bps, WINDOW-matched.
    H3  Strong invariance: >= 90% of those windows.
    H4  Every pairwise leg holds in >= 50% of windows.
    H5  Grid stability: the exact-match share spans <= 0.10 across all 9 (window, step) points.
    H6  Rule 8 on the claim: the IS-window share predicts the OOS-window share to within 0.10.
    H7  Rule 8 on a book: the IS-selected arm beats BOTH the RULES v2 baseline and SPY on OOS
        Sharpe.
    H8  Some arm clears 4a or 4b at 10 bps.

Costs 10 bps per unit turnover (PROTOCOL rule 2), weights at close t applied t+1 (the engine),
no shorting, no leverage.  Survivorship: all three panels are current-constituent lists, so CAGR
and drawdown LEVELS are optimistic; every statistic here is a WITHIN-panel contrast between arms
that share the panel, which the bias does not move.
"""
import sys
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT_ORDER = OUT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.ordering.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
FULL_RUNGS = [0.0, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 75.0, 100.0]
RUNGS = [0.0, 10.0, 25.0]          # the census rungs; 10 bps is PROTOCOL's and the headline
RUNG_HEAD = 10.0
WINDOWS = [504, 756, 1008]         # tuned 1
STEPS = [21, 63, 126]              # tuned 2
W_HEAD, S_HEAD = 756, 63
CONVS = ["WINDOW", "FULL"]
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
GSTEP = 0.01
MIN_GEFF = 0.005                   # below this the twin is ~cash and its Sharpe is not defined
MIN_COVER = 0.80                   # a panel joins a window only if it prices >= 80% of its days
PUBLISHED = ["QROLL", "QEXP", "ABS"]        # idea 605's published order, best -> worst
PUB_RANK = {"ABS": 1.0, "QEXP": 2.0, "QROLL": 3.0}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (ideas 42/336/399)
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


# ---------------------------------------------------------------- fast metrics
def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    yrs = n / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = (r.mean() * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


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


def cs(x):
    """cumulative sum with a leading 0, so sum over [s, e) is c[e] - c[s]."""
    out = np.zeros(len(x) + 1, dtype=float)
    np.cumsum(x, out=out[1:])
    return out


def win_sharpe(c1, c2, s, e):
    """Annualised Sharpe over [s, e) from cumsums of r and r**2 (gate G5).  c1/c2 may be 1-D
    (one series) or 2-D (one row per arm)."""
    L = e - s
    S1 = c1[..., e] - c1[..., s]
    S2 = c2[..., e] - c2[..., s]
    mean = S1 / L
    var = (S2 - L * mean * mean) / (L - 1)
    return np.where(var > 0, mean * np.sqrt(252.0) / np.sqrt(np.maximum(var, 1e-300)), np.nan)


class Twins:
    """Static-gross EWALL twin (returns, turnover) at cost 0, exact g by linear interpolation on
    a GSTEP cache (idea 602's G4 priced the interpolation error at <= 4e-07 of Sharpe)."""

    def __init__(self, px, start):
        self.px, self.start = px, start
        self.cache = {}
        self.n_bt = 0

    def exact(self, g):
        g = round(g, 6)
        if g not in self.cache:
            res = backtest(self.px, ewall_weights(self.px, g), cost_bps=0, freq=FREQ)
            self.cache[g] = (res["returns"].loc[self.start:].values,
                             res["turnover"].loc[self.start:].values)
            self.n_bt += 1
        return self.cache[g]

    def prewarm(self, gs):
        need = set()
        for g in gs:
            lo = np.floor(round(g, 6) / GSTEP) * GSTEP
            need.add(round(lo, 6))
            need.add(round(lo + GSTEP, 6))
        for g in sorted(need):
            self.exact(g)
        return need

    def at0(self, g):
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            return self.exact(lo)
        rl, tl = self.exact(lo)
        rh, th = self.exact(round(lo + GSTEP, 6))
        return (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th


def lo_lam(g):
    lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
    return lo, (round(g, 6) - lo) / GSTEP


# ---------------------------------------------------------------- per-panel build
def build_panel(panel, px):
    """Return everything the census needs for one panel: the 216 arms' gate series at every
    census rung, the twin grid cumsums, and the per-arm window-mean multiplier."""
    start = px.index[260]
    idx = px.index
    eval_idx = px.loc[start:].index
    n = len(eval_idx)
    spy = px["SPY"].pct_change().fillna(0).loc[start:].values

    br_full = breadth(px)
    br = br_full.loc[start:]
    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}

    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:].values, res["turnover"].loc[start:].values)

    gate_specs = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
                  + [("QROLL", q, w) for q in QS for w in WS])
    arms = []
    for (fam, lev, w), d, cad, g in product(gate_specs, DEPTHS, CADENCES, GROSSES):
        thr = None if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
        m = (gate_abs(br_full, lev, d, cad, idx) if fam == "ABS"
             else gate_from_thr(br_full, thr, d, cad, idx))
        me = m.reindex(eval_idx).shift(1).fillna(1.0).values
        sw = np.abs(np.diff(me, prepend=me[0]))
        r0, t0 = base0[g]
        arms.append(dict(panel=panel, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                         arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                         me=me, rg0=me * r0, Cg=me * t0 + g * sw,
                         on_share=float((me < 1.0).mean()),
                         switch_tax=g * float(sw.mean())))
    return dict(panel=panel, px=px, start=start, eval_idx=eval_idx, n=n, spy=spy,
                base0=base0, arms=arms, br=br)


def map_windows(P, master_windows):
    """Map each master (date) window onto this panel's own eval index; None when the panel does
    not price at least MIN_COVER of the window's days (SMALL439 starts later than U56/B136)."""
    idx = P["eval_idx"]
    P["winpos"] = {}
    for (W, S), wins in master_windows.items():
        pos = []
        for d0, d1 in wins:
            s = int(idx.searchsorted(d0, side="left"))
            e = int(idx.searchsorted(d1, side="right"))
            pos.append((s, e) if (e - s) >= MIN_COVER * W and (e - s) > 2 else None)
        P["winpos"][(W, S)] = pos
    return P


def attach_twins(P):
    """Prewarm the twin gross grid for both matching conventions and build the O(1) cumsums."""
    px, start, n = P["px"], P["start"], P["n"]
    arms = P["arms"]
    me_cs = np.vstack([cs(a["me"]) for a in arms])                       # (A, n+1)
    P["me_cs"] = me_cs
    garr = np.array([a["gross"] for a in arms])
    P["fam_idx"] = {f: np.array([i for i, a in enumerate(arms) if a["family"] == f])
                    for f in PUBLISHED}

    # every g_eff the census can ask for, over BOTH conventions and ALL 9 grid points
    need = [float(garr[i] * arms[i]["me"].mean()) for i in range(len(arms))]
    for key, pos in P["winpos"].items():
        for se in pos:
            if se is None:
                continue
            s, e = se
            mm = (me_cs[:, e] - me_cs[:, s]) / (e - s)
            need += list(np.maximum(garr * mm, MIN_GEFF))
    tw = Twins(px, start)
    tw.prewarm(need)
    P["n_bt"] = tw.n_bt

    vals = sorted(tw.cache)
    P["gidx"] = {v: i for i, v in enumerate(vals)}
    P["gvals"] = vals
    # A[c][k] cumsums of a_k = r0_k - t0_k*c/1e4 ; A2 of a_k**2 ; AB of a_k * a_{k+GSTEP}
    P["CA"], P["CA2"], P["CAB"] = {}, {}, {}
    for c in RUNGS:
        A = np.vstack([tw.cache[v][0] - tw.cache[v][1] * c / 1e4 for v in vals])
        P["CA"][c] = np.vstack([cs(A[k]) for k in range(len(vals))])
        P["CA2"][c] = np.vstack([cs(A[k] ** 2) for k in range(len(vals))])
        AB = np.zeros((len(vals), n + 1))
        for k, v in enumerate(vals):
            hv = round(v + GSTEP, 6)
            if hv in P["gidx"]:
                AB[k] = cs(A[k] * A[P["gidx"][hv]])
        P["CAB"][c] = AB
    # gate cumsums per arm per rung
    P["CG"], P["CG2"] = {}, {}
    for c in RUNGS:
        R = np.vstack([a["rg0"] - a["Cg"] * c / 1e4 for a in arms])
        P["CG"][c] = np.vstack([cs(R[i]) for i in range(len(arms))])
        P["CG2"][c] = np.vstack([cs(R[i] ** 2) for i in range(len(arms))])
    P["tw"] = tw
    P["garr"] = garr
    return P


def twin_sharpe(P, c, geff, s, e):
    """Vectorised Sharpe of the matched-gross twin over [s, e) at gross geff (array over arms)."""
    L = e - s
    lo = np.round(np.floor(np.round(geff, 6) / GSTEP) * GSTEP, 6)
    lam = (np.round(geff, 6) - lo) / GSTEP
    li = np.array([P["gidx"][round(float(v), 6)] for v in lo])
    hi = np.array([P["gidx"][round(float(v) + GSTEP, 6)] for v in lo])
    CA, CA2, CAB = P["CA"][c], P["CA2"][c], P["CAB"][c]
    S1 = (1 - lam) * (CA[li, e] - CA[li, s]) + lam * (CA[hi, e] - CA[hi, s])
    S2 = ((1 - lam) ** 2 * (CA2[li, e] - CA2[li, s])
          + 2 * lam * (1 - lam) * (CAB[li, e] - CAB[li, s])
          + lam ** 2 * (CA2[hi, e] - CA2[hi, s]))
    mean = S1 / L
    var = (S2 - L * mean * mean) / (L - 1)
    return np.where(var > 1e-300, mean * np.sqrt(252.0) / np.sqrt(np.maximum(var, 1e-300)), np.nan)


def order_of(wr):
    """Family order best -> worst from a {family: win rate} dict, with an explicit tie token."""
    items = sorted(wr.items(), key=lambda kv: (-kv[1], kv[0]))
    toks = []
    for i, (f, v) in enumerate(items):
        toks.append(("=" if i and abs(v - items[i - 1][1]) <= TIE else ">") + f if i else f)
    return "".join(toks), items


# ---------------------------------------------------------------- full-sample rebuild (G4)
def full_sample_table(P, spy_pack, base_packs):
    """Idea 605's own statistic, rebuilt: per arm, dSharpe vs the FULL-matched twin at every one
    of the 15 published rungs, plus the 10-bps KEEP-path columns."""
    arms, tw = P["arms"], P["tw"]
    n = P["n"]
    h = n // 2
    is_end = int(P["eval_idx"].searchsorted(pd.Timestamp(IS_END), side="right"))
    oos = int(P["eval_idx"].searchsorted(pd.Timestamp(OOS_START), side="left"))
    geff_full = np.array([a["gross"] * float(a["me"].mean()) for a in arms])
    P["geff_full"] = np.maximum(geff_full, MIN_GEFF)
    rows = []
    for i, a in enumerate(arms):
        rs0, Cs = tw.at0(float(P["geff_full"][i]))
        for c in FULL_RUNGS:
            rg = a["rg0"] - a["Cg"] * c / 1e4
            rs = rs0 - Cs * c / 1e4
            sg, ss_ = fsharpe(rg), fsharpe(rs)
            r = dict(panel=P["panel"], arm=a["arm"], family=a["family"], level=a["level"],
                     w=a["w"], depth=a["depth"], cadence=a["cadence"], gross=a["gross"],
                     rung=c, Sharpe=sg, twin_Sharpe=ss_, dSharpe=sg - ss_,
                     win=bool(sg - ss_ > TIE), tie=bool(abs(sg - ss_) <= TIE))
            if c == RUNG_HEAD:
                cg, sh, dd = fmet(rg)
                oc, os_, od = fmet(rg[oos:])
                s1, s2, so, sdd, scg = spy_pack
                b1, b2, bdd = base_packs[c]
                t4b = dict(H1=fsharpe(rg[:h]) > s1, H2=fsharpe(rg[h:]) > s2, OOS=os_ > so,
                           DD=abs(dd) <= 0.60 * abs(sdd), CAGR=cg >= 0.70 * scg)
                r.update(CAGR=cg, MaxDD=dd, H1=fsharpe(rg[:h]), H2=fsharpe(rg[h:]),
                         IS_Sharpe=fsharpe(rg[:is_end]), OOS_CAGR=oc, OOS_Sharpe=os_,
                         OOS_MaxDD=od, on_share=a["on_share"], switch_tax=a["switch_tax"],
                         g_eff=P["geff_full"][i],
                         p4a=bool(fsharpe(rg[:h]) > b1 and fsharpe(rg[h:]) > b2 and dd >= bdd),
                         p4b=all(t4b.values()),
                         fail4b=",".join([k for k, v in t4b.items() if not v]) or "-")
            rows.append(r)
    P["slices"] = (h, is_end, oos)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- the rolling census
def run_census(corpus, PANELS, master_windows):
    """For every (window, step, convention, rung), every rolling window and every scope, the
    three family win rates, the order a reader would have seen, and its agreement with the
    published QROLL > QEXP > ABS."""
    rows = []
    for (W, S), wins in master_windows.items():
        for conv, c in product(CONVS, RUNGS):
            for wi, (d0, d1) in enumerate(wins):
                pooled = {f: [0, 0] for f in PUBLISHED}
                for P in PANELS:
                    se = P["winpos"][(W, S)][wi]
                    if se is None:
                        continue
                    s, e = se
                    gs = win_sharpe(P["CG"][c], P["CG2"][c], s, e)
                    if conv == "WINDOW":
                        mm = (P["me_cs"][:, e] - P["me_cs"][:, s]) / (e - s)
                        geff = np.maximum(P["garr"] * mm, MIN_GEFF)
                    else:
                        geff = P["geff_full"]
                    ts = twin_sharpe(P, c, geff, s, e)
                    d = gs - ts
                    wr = {}
                    for f in PUBLISHED:
                        sel = P["fam_idx"][f]
                        dv = d[sel]
                        ok = np.isfinite(dv)
                        nw, na = int((dv[ok] > TIE).sum()), int(ok.sum())
                        wr[f] = nw / na if na else np.nan
                        pooled[f][0] += nw
                        pooled[f][1] += na
                    rows.append(_census_row(corpus, P["panel"], W, S, conv, c, wi, d0, d1, wr,
                                            sum(len(P["fam_idx"][f]) for f in PUBLISHED)))
                if all(pooled[f][1] for f in PUBLISHED):
                    wr = {f: pooled[f][0] / pooled[f][1] for f in PUBLISHED}
                    rows.append(_census_row(corpus, "POOLED", W, S, conv, c, wi, d0, d1, wr,
                                            sum(pooled[f][1] for f in PUBLISHED)))
    return pd.DataFrame(rows)


def _census_row(corpus, scope, W, S, conv, c, wi, d0, d1, wr, n_arms):
    tok, items = order_of(wr)
    rho = spearman([PUB_RANK[f] for f in PUBLISHED], [wr[f] for f in PUBLISHED])
    return dict(corpus=corpus, scope=scope, window=W, step=S, conv=conv, rung=c, wi=wi,
                start=d0.date(), end=d1.date(), n_arms=n_arms,
                win_ABS=wr["ABS"], win_QEXP=wr["QEXP"], win_QROLL=wr["QROLL"],
                order=tok, rho_vs_published=rho,
                exact=bool(wr["QROLL"] - wr["QEXP"] > TIE and wr["QEXP"] - wr["ABS"] > TIE),
                weak=bool(wr["QROLL"] - wr["QEXP"] >= -TIE and wr["QEXP"] - wr["ABS"] >= -TIE),
                QR_gt_QE=bool(wr["QROLL"] - wr["QEXP"] > TIE),
                QE_gt_AB=bool(wr["QEXP"] - wr["ABS"] > TIE),
                QR_gt_AB=bool(wr["QROLL"] - wr["ABS"] > TIE),
                top_QROLL=bool(max(wr, key=lambda f: wr[f]) == "QROLL"),
                bottom_ABS=bool(min(wr, key=lambda f: wr[f]) == "ABS"),
                spread=max(wr.values()) - min(wr.values()),
                is_win=bool(pd.Timestamp(d1) <= pd.Timestamp(IS_END)),
                oos_win=bool(pd.Timestamp(d0) >= pd.Timestamp(OOS_START)))


# ---------------------------------------------------------------- rule 8, book leg
def walk_forward(corpus, PANELS, cen, master_windows, spy_oos, base_oos):
    """Rule 8 (b): the IS rolling census picks the family, IS Sharpe picks the arm inside it,
    2017-2026 is read once.  Reported against the RULES v2 baseline, SPY and the arm's own twin,
    with the hindsight (OOS-leading) family beside it as the size of what the selector missed."""
    rows = []
    c = RUNG_HEAD
    for P in PANELS:
        h, is_end, oos = P["slices"]
        arms = P["arms"]
        fam = np.array([a["family"] for a in arms])
        is_sh = np.array([fsharpe((a["rg0"] - a["Cg"] * c / 1e4)[:is_end]) for a in arms])
        for (W, S) in master_windows:
            sub = cen[(cen["scope"] == P["panel"]) & (cen["window"] == W) & (cen["step"] == S)
                      & (cen["conv"] == "WINDOW") & (cen["rung"] == c)]
            isw, oosw = sub[sub["is_win"]], sub[sub["oos_win"]]
            if not len(isw) or not len(oosw):
                continue
            is_rate = {f: float(isw[f"win_{f}"].mean()) for f in PUBLISHED}
            oos_rate = {f: float(oosw[f"win_{f}"].mean()) for f in PUBLISHED}
            pick_f = max(is_rate, key=lambda f: is_rate[f])
            best_f = max(oos_rate, key=lambda f: oos_rate[f])
            cand = np.where((fam == pick_f) & np.isfinite(is_sh))[0]
            i = int(cand[np.argmax(is_sh[cand])])
            a = arms[i]
            rg = a["rg0"] - a["Cg"] * c / 1e4
            rs0, Cs = P["tw"].at0(float(P["geff_full"][i]))
            rs = rs0 - Cs * c / 1e4
            oc, os_, od = fmet(rg[oos:])
            tc, ts_, td = fmet(rs[oos:])
            sc, ss_, sd = spy_oos[P["panel"]]
            bc, bs_, bd = base_oos[P["panel"]]
            # hindsight arm inside the OOS-leading family, on the same IS-Sharpe rule
            cand2 = np.where((fam == best_f) & np.isfinite(is_sh))[0]
            j = int(cand2[np.argmax(is_sh[cand2])])
            rj = arms[j]["rg0"] - arms[j]["Cg"] * c / 1e4
            hc, hs_, hd = fmet(rj[oos:])
            rows.append(dict(corpus=corpus, panel=P["panel"], window=W, step=S, rung=c,
                             n_is_win=len(isw), n_oos_win=len(oosw),
                             is_ABS=is_rate["ABS"], is_QEXP=is_rate["QEXP"],
                             is_QROLL=is_rate["QROLL"], oos_ABS=oos_rate["ABS"],
                             oos_QEXP=oos_rate["QEXP"], oos_QROLL=oos_rate["QROLL"],
                             pick_family=pick_f, oos_best_family=best_f,
                             selector_right=bool(pick_f == best_f), pick_arm=a["arm"],
                             pick_IS_Sharpe=is_sh[i], OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                             twin_OOS_CAGR=tc, twin_OOS_Sharpe=ts_, twin_OOS_MaxDD=td,
                             base_OOS_CAGR=bc, base_OOS_Sharpe=bs_, base_OOS_MaxDD=bd,
                             spy_OOS_CAGR=sc, spy_OOS_Sharpe=ss_, spy_OOS_MaxDD=sd,
                             hind_arm=arms[j]["arm"], hind_OOS_Sharpe=hs_, hind_OOS_CAGR=hc,
                             hind_OOS_MaxDD=hd,
                             beats_base=bool(os_ > bs_), beats_spy=bool(os_ > ss_),
                             beats_twin=bool(os_ > ts_)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- as-of replica (gate G4a)
# Idea 605 ran on 2026-09-10.  Since then the nightly jobs have appended two trading days to
# data/prices.csv and REWRITTEN data/prices_small.csv.gz: the sub-$2B screen it caches went from
# 439 tradable names to 663.  So "re-run idea 605's corpus" is two different corpora depending on
# when you run it, which is exactly the hazard idea 565 filed.  G4a rebuilds the panels idea 605
# actually read - today's price caches truncated to its last dates, and the SMALL panel restored
# from the git blob it loaded - and joins the rebuild to its committed rows.  G4b then reports the
# same statistic on TODAY's caches, which is the population the census below runs on.
ASOF_BLOB = "e02949d"                      # the prices_small.csv.gz / small_meta.csv idea 605 read
ASOF_END = {"U56": "2026-09-09", "B136": "2026-09-04", "SMALL439": "2026-09-04"}


def asof_panels(tmp):
    import subprocess
    out = []
    out.append(("U56", load_universe().loc[:ASOF_END["U56"]]))
    out.append(("B136", load_universe(broad=True).loc[:ASOF_END["B136"]]))
    blobs = {}
    for f in ("data/prices_small.csv.gz", "data/small_meta.csv"):
        p = tmp / Path(f).name
        p.write_bytes(subprocess.run(["git", "-C", str(REPO), "show", f"{ASOF_BLOB}:{f}"],
                                     capture_output=True, check=True).stdout)
        blobs[f] = p
    ps = pd.read_csv(blobs["data/prices_small.csv.gz"], index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":]
    ps = ps.dropna(how="all").ffill()
    spy = pd.read_csv(REPO / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"),
                    spy.reindex(ps.index, method="ffill").rename("SPY")], axis=1)
    meta = pd.read_csv(blobs["data/small_meta.csv"])
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    ps = ps[[c for c in ps.columns if c == "SPY" or c not in bad]].loc[:ASOF_END["SMALL439"]]
    out.append(("SMALL439", ps))
    return out


def build_corpus(corpus, panel_list):
    """One complete corpus: its own master rolling-window calendar (taken from its first panel),
    every panel built, twin-prewarmed and window-mapped, and the full-sample arm table."""
    master = panel_list[0][1].index[260:]
    mw = {}
    for W, S in product(WINDOWS, STEPS):
        mw[(W, S)] = [(master[s], master[s + W - 1])
                      for s in range(0, len(master) - W + 1, S)]
    log(f"  master calendar {master[0].date()} -> {master[-1].date()} ({len(master)} days); "
        + "  ".join(f"{W}/{S}:{len(v)}" for (W, S), v in mw.items()))
    PANELS, FULL = [], []
    for name, px in panel_list:
        P = build_panel(name, px)
        P = map_windows(P, mw)
        P = attach_twins(P)
        h = P["n"] // 2
        oos = int(P["eval_idx"].searchsorted(pd.Timestamp(OOS_START), side="left"))
        spy = P["spy"]
        sc, ss_, sd = fmet(spy)
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos:]), sd, sc)
        rv2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
        b0 = rv2["returns"].loc[P["start"]:].values
        bt0 = rv2["turnover"].loc[P["start"]:].values
        base_packs = {c: (fsharpe((b0 - bt0 * c / 1e4)[:h]), fsharpe((b0 - bt0 * c / 1e4)[h:]),
                          fmet(b0 - bt0 * c / 1e4)[2]) for c in FULL_RUNGS}
        P["spy_pack"], P["base_packs"] = spy_pack, base_packs
        P["spy_oos"] = fmet(spy[oos:])
        P["base_oos"] = fmet((b0 - bt0 * RUNG_HEAD / 1e4)[oos:])
        FULL.append(full_sample_table(P, spy_pack, base_packs))
        PANELS.append(P)
        cov = sum(x is not None for x in P["winpos"][(W_HEAD, S_HEAD)])
        log(f"    {P['panel']:9s} {px.shape[1]:4d} cols, eval {P['eval_idx'][0].date()} -> "
            f"{P['eval_idx'][-1].date()} ({P['n']} days), {len(P['arms'])} arms, "
            f"{P['n_bt']} twin backtests on a {GSTEP} grid "
            f"[{min(P['tw'].cache):.2f}, {max(P['tw'].cache):.2f}], windows covered "
            f"{cov}/{len(mw[(W_HEAD, S_HEAD)])} at the headline grid point; "
            f"SPY {sc:.2%}/{ss_:.3f}/{sd:.2%}")
    return dict(panels=PANELS, full=pd.concat(FULL, ignore_index=True), mw=mw)


# ---------------------------------------------------------------- main
def main():
    log("=" * 190)
    log(f"Idea 609 is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census (lane B) | {SCRIPT}")
    log("=" * 190)
    log("Base book (fixed, ideas 28/42/336/399): EWALL(G) = equal weight every name above its own")
    log("  200d MA with vol20 < 0.60, at G/E_t, weekly, next-day execution, 10 bps.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is BELOW the threshold.")
    log("Comparand for EVERY arm: the MATCHED-MEAN-GROSS STATIC TWIN (EWALL at constant g_eff).")
    log(f"Published claim under test (idea 605): family win-rate order {' > '.join(PUBLISHED)}.")
    log(f"Tuned (2): window in {WINDOWS} trading days, step in {STEPS}.  All 9 reported.")
    log(f"Reported never tuned: family, level, w, depth, cadence, panel, gross, rung {RUNGS}, "
        f"matching convention {CONVS}.  Tie bar |dSharpe| <= {TIE:g}.")

    # =================================================================== [0] gates
    log("\n" + "=" * 190)
    log("[0] REPRODUCTION GATES (all printed before any new number is read)")
    px0 = load_universe()
    st0 = px0.index[260]
    idx0 = px0.loc[st0:].index

    res0 = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=0, freq=FREQ)
    r0 = res0["returns"].loc[st0:].values
    t0 = res0["turnover"].loc[st0:].values
    brf = breadth(px0)
    mtest = gate_abs(brf, 0.40, 0.50, "W", px0.index).reindex(idx0).shift(1).fillna(1.0)
    me = mtest.values
    sw = np.abs(np.diff(me, prepend=me[0]))
    g1 = 0.0
    for c in FULL_RUNGS:
        live = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=c,
                        freq=FREQ)["returns"].loc[st0:].values
        ref = me * live - sw * G_HEAD * c / 1e4                 # idea 399's apply_gate verbatim
        der = me * r0 - (me * t0 + G_HEAD * sw) * c / 1e4       # this run's derived ladder
        g1 = max(g1, float(np.abs(live - (r0 - t0 * c / 1e4)).max()),
                 float(np.abs(ref - der).max()))
    log(f"  G1 derived ladder == live backtest through apply_gate, all {len(FULL_RUNGS)} rungs: "
        f"max |diff| = {g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    rng = np.random.default_rng(609)
    g2 = 0.0
    for _ in range(200):
        c = float(rng.uniform(0, 100))
        a, b = sorted(rng.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        s = pd.Series((r0 - t0 * c / 1e4)[a:b], index=idx0[a:b])
        mm, f = metrics(s), fmet(s.values)
        g2 = max(g2, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G2 fast metrics vs engine.metrics on 200 series: max |diff| = {g2:.3e} "
        f"(bar 1e-12) -> {'PASS' if g2 < 1e-12 else 'FAIL'}")

    r84 = backtest(px0, ewall_weights(px0, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[st0:]
    c84, s84, d84 = fmet(r84.values)
    ok84 = (abs(c84 - 0.118) < 0.004 and abs(s84 - 1.05) < 0.04 and abs(abs(d84) - 0.179) < 0.006)
    log(f"  G3 idea 84 EWALL U56 g=0.85 @10bps: {c84:.3%} / {s84:.3f} / {d84:.3%}  "
        f"(published 11.8% / 1.05 / -17.9%) -> {'PASS' if ok84 else 'FAIL'}")
    # ================================================================ [1] the two corpora
    log("\n" + "=" * 190)
    log("[1] THE TWO CORPORA AND THE ROLLING WINDOW GRID")
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    ps, ndrop = small_panel()
    log(f"  TODAY's SMALL panel: dropped {ndrop} names with max_1d_move >= 1.0 -> "
        f"{ps.shape[1]-1} names + SPY")
    lists = {"ASOF": asof_panels(tmp),
             "TODAY": [("U56", px0), ("B136", load_universe(broad=True)), ("SMALL439", ps)]}
    CORP = {}
    for corpus in ("ASOF", "TODAY"):
        log(f"\n  --- corpus {corpus} "
            f"({'idea 605 read this one' if corpus == 'ASOF' else 'the current caches'})")
        CORP[corpus] = build_corpus(corpus, lists[corpus])

    # ---- G4a / G4b
    log("\n" + "=" * 190)
    log("[0b] G4a - does the AS-OF corpus reproduce idea 605's committed rows?")
    parent_cells = OUT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.cells.csv.gz"
    g4a, g4b = np.nan, np.nan
    if parent_cells.exists():
        pc = pd.read_csv(parent_cells)
        pc = pc[~pc["family"].isin(["ref", "NOGATE"])]
        b = pc.groupby(["panel", "rung", "family"])["win"].mean()
        for corpus, tag in (("ASOF", "G4a"), ("TODAY", "G4b")):
            a = CORP[corpus]["full"].groupby(["panel", "rung", "family"])["win"].mean()
            j = (a - b).abs().dropna()
            v = float(j.max())
            if corpus == "ASOF":
                g4a = v
            else:
                g4b = v
            log(f"  {tag} {corpus:5s}: {len(j)} (panel, rung, family) cells; max |diff| "
                + "  ".join(f"{pn} {j.xs(pn, level='panel').max():.3e}"
                            for pn in sorted(j.index.get_level_values("panel").unique()))
                + f"  -> overall {v:.3e}, {'PASS' if v < 1e-9 else 'FAIL'} (bar 1e-9)")
    else:
        log(f"  {parent_cells.name} NOT FOUND -> G4a/G4b cannot run")
    log("\n  full-sample family win rate by rung, both corpora (648 arms: 108 ABS / 108 QEXP / "
        "432 QROLL)")
    PUBTAB = {}
    for corpus in ("ASOF", "TODAY"):
        t = (CORP[corpus]["full"].groupby(["rung", "family"])["win"].mean()
             .unstack()[["ABS", "QEXP", "QROLL"]])
        PUBTAB[corpus] = t
        fsx = {f: float(t.loc[RUNG_HEAD, f]) for f in PUBLISHED}
        log(f"\n  corpus {corpus}: full-sample order at {RUNG_HEAD:.0f} bps -> "
            f"{order_of(fsx)[0]}  (published {' > '.join(PUBLISHED)}), spread "
            f"{max(fsx.values())-min(fsx.values()):.4f}")
        log(t.to_string(float_format=lambda x: f"{x:.4f}"))
    if PARENT_ORDER.exists():
        po = pd.read_csv(PARENT_ORDER).set_index("rung")[["win_ABS", "win_QEXP", "win_QROLL"]]
        po.columns = ["ABS", "QEXP", "QROLL"]
        log("\n  idea 605's committed ordering.csv, for the same rungs:")
        log(po.to_string(float_format=lambda x: f"{x:.4f}"))
    fs = {f: float(PUBTAB["ASOF"].loc[RUNG_HEAD, f]) for f in PUBLISHED}

    # ---- G5: the O(1) window recursion against a direct Sharpe
    P = CORP["ASOF"]["panels"][0]
    g5 = 0.0
    g5pos = [se for key in P["winpos"] for se in P["winpos"][key] if se is not None]
    for _ in range(400):
        i = int(rng.integers(0, len(P["arms"])))
        c = float(RUNGS[int(rng.integers(0, len(RUNGS)))])
        s, e = g5pos[int(rng.integers(0, len(g5pos)))]
        a = P["arms"][i]
        direct_g = fsharpe((a["rg0"] - a["Cg"] * c / 1e4)[s:e])
        fast_g = float(win_sharpe(P["CG"][c][i], P["CG2"][c][i], s, e))
        mm = float((P["me_cs"][i, e] - P["me_cs"][i, s]) / (e - s))
        geff = max(a["gross"] * mm, MIN_GEFF)
        rs0, Cs = P["tw"].at0(geff)
        direct_t = fsharpe((rs0 - Cs * c / 1e4)[s:e])
        fast_t = float(twin_sharpe(P, c, np.array([geff]), s, e)[0])
        g5 = max(g5, abs(direct_g - fast_g), abs(direct_t - fast_t))
    log(f"\n  G5 O(1) window Sharpe (gate and twin) vs direct numpy on 400 random slices: "
        f"max |diff| = {g5:.3e} (bar 1e-9) -> {'PASS' if g5 < 1e-9 else 'FAIL'}")

    # ================================================================ [2] the rolling census
    log("\n" + "=" * 190)
    log("[2] ROLLING CENSUS - what order would a reader have seen?")
    cen = pd.concat([run_census(k, CORP[k]["panels"], CORP[k]["mw"]) for k in CORP],
                    ignore_index=True)
    log(f"  {len(cen)} census rows = 2 corpora x 9 (window,step) x {len(CONVS)} conventions x "
        f"{len(RUNGS)} rungs x 4 scopes x windows")

    def head_slice(corpus):
        return cen[(cen["corpus"] == corpus) & (cen["scope"] == "POOLED")
                   & (cen["window"] == W_HEAD) & (cen["step"] == S_HEAD)
                   & (cen["conv"] == "WINDOW") & (cen["rung"] == RUNG_HEAD)]

    hd = head_slice("ASOF")
    for corpus in ("ASOF", "TODAY"):
        q = head_slice(corpus)
        log(f"\n  HEADLINE ({corpus}): pooled, window {W_HEAD} step {S_HEAD}, "
            f"{RUNG_HEAD:.0f} bps, WINDOW-matched twin, {len(q)} windows")
        log(f"    exact {' > '.join(PUBLISHED)}      {q['exact'].mean():.4f}  "
            f"({int(q['exact'].sum())} of {len(q)})")
        log(f"    QROLL > QEXP                {q['QR_gt_QE'].mean():.4f}")
        log(f"    QEXP  > ABS                 {q['QE_gt_AB'].mean():.4f}")
        log(f"    QROLL > ABS                 {q['QR_gt_AB'].mean():.4f}")
        log(f"    QROLL on top                {q['top_QROLL'].mean():.4f}")
        log(f"    ABS at the bottom           {q['bottom_ABS'].mean():.4f}")
        log(f"    mean rho vs published       {q['rho_vs_published'].mean():+.4f}  "
            f"(rho = +1 in {(q['rho_vs_published'] > 0.99).mean():.4f} of windows)")
        log(f"    mean win-rate spread        {q['spread'].mean():.4f}")
        log(f"    mean win rates ABS / QEXP / QROLL  {q['win_ABS'].mean():.4f} / "
            f"{q['win_QEXP'].mean():.4f} / {q['win_QROLL'].mean():.4f}")
        log("    every order a reader would have seen:")
        for k, v in q["order"].value_counts().items():
            log(f"      {k:34s} {v:4d}  {v/len(q):.4f}")

    log("\n  the ASOF headline census window by window (the reader's own view):")
    log(hd[["start", "end", "win_ABS", "win_QEXP", "win_QROLL", "order", "rho_vs_published",
            "exact"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- all 9 grid points, both corpora, both conventions, all rungs, all scopes
    log("\n  ALL 9 (window, step) GRID POINTS - exact-match share (PROTOCOL rule 4: every grid"
        " point reported)")
    for corpus in ("ASOF", "TODAY"):
        for conv in CONVS:
            for c in RUNGS:
                g = cen[(cen["corpus"] == corpus) & (cen["conv"] == conv) & (cen["rung"] == c)]
                log(f"\n  corpus={corpus}  conv={conv}  rung={c:.0f} bps")
                log(g.pivot_table(index=["scope"], columns=["window", "step"], values="exact")
                    .to_string(float_format=lambda x: f"{x:.3f}"))
    grid = (cen.groupby(["corpus", "scope", "conv", "rung", "window", "step"])
            .agg(n_windows=("exact", "size"), exact=("exact", "mean"), weak=("weak", "mean"),
                 QR_gt_QE=("QR_gt_QE", "mean"), QE_gt_AB=("QE_gt_AB", "mean"),
                 QR_gt_AB=("QR_gt_AB", "mean"), top_QROLL=("top_QROLL", "mean"),
                 bottom_ABS=("bottom_ABS", "mean"), mean_rho=("rho_vs_published", "mean"),
                 mean_spread=("spread", "mean"), win_ABS=("win_ABS", "mean"),
                 win_QEXP=("win_QEXP", "mean"), win_QROLL=("win_QROLL", "mean")).reset_index())
    ph = grid[(grid["corpus"] == "ASOF") & (grid["scope"] == "POOLED")
              & (grid["conv"] == "WINDOW") & (grid["rung"] == RUNG_HEAD)]
    span = float(ph["exact"].max() - ph["exact"].min())
    log(f"\n  exact-match share over the 9 grid points (ASOF, pooled, WINDOW, "
        f"{RUNG_HEAD:.0f} bps): min {ph['exact'].min():.4f}  max {ph['exact'].max():.4f}  "
        f"span {span:.4f}")
    log("  pairwise legs over the same 9 grid points:")
    log(ph[["window", "step", "n_windows", "exact", "QR_gt_QE", "QE_gt_AB", "QR_gt_AB",
            "mean_rho", "mean_spread"]].to_string(index=False,
                                                  float_format=lambda x: f"{x:.4f}"))
    log("\n  matching convention and corpus at the headline grid point (pooled, 10 bps):")
    for corpus in ("ASOF", "TODAY"):
        for conv in CONVS:
            v = grid[(grid["corpus"] == corpus) & (grid["scope"] == "POOLED")
                     & (grid["conv"] == conv) & (grid["rung"] == RUNG_HEAD)
                     & (grid["window"] == W_HEAD) & (grid["step"] == S_HEAD)].iloc[0]
            log(f"    {corpus:5s} {conv:7s} exact {v['exact']:.4f}  QR>QE {v['QR_gt_QE']:.4f}  "
                f"QE>AB {v['QE_gt_AB']:.4f}  QR>AB {v['QR_gt_AB']:.4f}  rho {v['mean_rho']:+.4f}"
                f"  win {v['win_ABS']:.3f}/{v['win_QEXP']:.3f}/{v['win_QROLL']:.3f}")
    log("\n  per panel (ASOF, WINDOW, 10 bps, headline grid point):")
    log(grid[(grid["corpus"] == "ASOF") & (grid["conv"] == "WINDOW")
             & (grid["rung"] == RUNG_HEAD) & (grid["window"] == W_HEAD)
             & (grid["step"] == S_HEAD)][["scope", "n_windows", "exact", "QR_gt_QE", "QE_gt_AB",
                                          "QR_gt_AB", "mean_rho", "win_ABS", "win_QEXP",
                                          "win_QROLL"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ [3] rule 8 on the claim
    log("\n" + "=" * 190)
    log("[3] RULE 8 (a) ON THE CLAIM - IS windows (<= 2016) read first, OOS windows (2017+) once")
    wf_claim = []
    for corpus in CORP:
        for (W, S) in CORP[corpus]["mw"]:
            for conv in CONVS:
                for c in RUNGS:
                    sub = cen[(cen["corpus"] == corpus) & (cen["scope"] == "POOLED")
                              & (cen["window"] == W) & (cen["step"] == S) & (cen["conv"] == conv)
                              & (cen["rung"] == c)]
                    i_, o_ = sub[sub["is_win"]], sub[sub["oos_win"]]
                    if not len(i_) or not len(o_):
                        continue
                    wf_claim.append(dict(corpus=corpus, window=W, step=S, conv=conv, rung=c,
                                         n_is=len(i_), n_oos=len(o_),
                                         is_exact=i_["exact"].mean(),
                                         oos_exact=o_["exact"].mean(),
                                         gap=o_["exact"].mean() - i_["exact"].mean(),
                                         is_QRAB=i_["QR_gt_AB"].mean(),
                                         oos_QRAB=o_["QR_gt_AB"].mean(),
                                         is_rho=i_["rho_vs_published"].mean(),
                                         oos_rho=o_["rho_vs_published"].mean()))
    wfc = pd.DataFrame(wf_claim)
    log(wfc[wfc["conv"] == "WINDOW"].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log("\n  (FULL-matched convention)")
    log(wfc[wfc["conv"] == "FULL"].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    hdc = wfc[(wfc["corpus"] == "ASOF") & (wfc["conv"] == "WINDOW") & (wfc["rung"] == RUNG_HEAD)
              & (wfc["window"] == W_HEAD) & (wfc["step"] == S_HEAD)]
    h6_gap = float(hdc["gap"].abs().iloc[0]) if len(hdc) else np.nan

    # ================================================================ [4] rule 8 on a book
    log("\n" + "=" * 190)
    log("[4] RULE 8 (b) ON A BOOK - the IS rolling census picks the family, IS Sharpe picks the "
        "arm, 2017-2026 read once")
    wf = pd.concat([walk_forward(k, CORP[k]["panels"], cen, CORP[k]["mw"],
                                 {P["panel"]: P["spy_oos"] for P in CORP[k]["panels"]},
                                 {P["panel"]: P["base_oos"] for P in CORP[k]["panels"]})
                    for k in CORP], ignore_index=True)
    cols = ["corpus", "panel", "window", "step", "is_ABS", "is_QEXP", "is_QROLL", "oos_ABS",
            "oos_QEXP", "oos_QROLL", "pick_family", "oos_best_family", "selector_right",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "twin_OOS_Sharpe", "base_OOS_Sharpe",
            "spy_OOS_Sharpe", "hind_OOS_Sharpe", "beats_base", "beats_spy", "beats_twin"]
    log(wf[wf["corpus"] == "ASOF"][cols].to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))
    for corpus in ("ASOF", "TODAY"):
        w = wf[wf["corpus"] == corpus]
        log(f"\n  corpus {corpus}: {len(w)} (panel x grid point) picks")
        log(f"    selector picked the OOS-leading family in {int(w['selector_right'].sum())} "
            f"of {len(w)}")
        log(f"    IS-picked book beats the RULES v2 baseline on OOS Sharpe in "
            f"{int(w['beats_base'].sum())} of {len(w)}; SPY in {int(w['beats_spy'].sum())}; "
            f"its own matched-gross twin in {int(w['beats_twin'].sum())}")
        log(f"    mean OOS Sharpe: pick {w['OOS_Sharpe'].mean():.4f}  twin "
            f"{w['twin_OOS_Sharpe'].mean():.4f}  hindsight-family pick "
            f"{w['hind_OOS_Sharpe'].mean():.4f}  RULES v2 {w['base_OOS_Sharpe'].mean():.4f}  "
            f"SPY {w['spy_OOS_Sharpe'].mean():.4f}")
        log(f"    mean OOS CAGR:   pick {w['OOS_CAGR'].mean():.2%}  RULES v2 "
            f"{w['base_OOS_CAGR'].mean():.2%}  SPY {w['spy_OOS_CAGR'].mean():.2%}")
        log(f"    mean OOS MaxDD:  pick {w['OOS_MaxDD'].mean():.2%}  RULES v2 "
            f"{w['base_OOS_MaxDD'].mean():.2%}  SPY {w['spy_OOS_MaxDD'].mean():.2%}")
    wfa = wf[wf["corpus"] == "ASOF"]

    # ================================================================ [5] KEEP paths
    log("\n" + "=" * 190)
    log(f"[5] BOTH KEEP PATHS on every arm at {RUNG_HEAD:.0f} bps (PROTOCOL rule 4)")
    full = pd.concat([CORP[k]["full"].assign(corpus=k) for k in CORP], ignore_index=True)
    at10 = full[full["rung"] == RUNG_HEAD]
    for corpus in ("ASOF", "TODAY"):
        a = at10[at10["corpus"] == corpus]
        log(f"  corpus {corpus}: 4a {int(a['p4a'].sum())} of {len(a)};  "
            f"4b {int(a['p4b'].sum())} of {len(a)}")
        log("    4b failure legs: " + "  ".join(
            f"{k}={v}" for k, v in a["fail4b"].value_counts().items()))
        log("    by panel: " + "  ".join(
            f"{p} 4a={int(r['p4a'])}/4b={int(r['p4b'])}"
            for p, r in a.groupby("panel")[["p4a", "p4b"]].sum().iterrows()))
        if int(a["p4b"].sum()):
            log(a[a["p4b"]][["panel", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                             "dSharpe"]].to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))
    ka = at10[at10["corpus"] == "ASOF"]
    pick_4b = 0
    for _, rr in wfa.iterrows():
        m = ka[(ka["panel"] == rr["panel"]) & (ka["arm"] == rr["pick_arm"])]
        pick_4b += int(m["p4b"].sum() > 0)
    log(f"  of the {len(wfa)} ASOF rule-8 picks, {pick_4b} sit on an arm that clears 4b "
        f"full-sample")

    # ================================================================ [6] hypotheses
    log("\n" + "=" * 190)
    log("[6] PRE-REGISTERED HYPOTHESES")
    h = float(hd["exact"].mean())
    H = [
        ("H1  G4a: as-of corpus reproduces idea 605's committed cells to 1e-9",
         bool(np.isfinite(g4a) and g4a < 1e-9), f"max |diff| {g4a:.3e}"),
        ("H1b in passing: TODAY's caches reproduce the same rows (NOT a bar)",
         bool(np.isfinite(g4b) and g4b < 1e-9), f"max |diff| {g4b:.3e}"),
        ("H2  published order is the modal reading (>= 0.50 of windows)", bool(h >= 0.50),
         f"exact {h:.4f}"),
        ("H3  strong invariance (>= 0.90 of windows)", bool(h >= 0.90), f"exact {h:.4f}"),
        ("H4  every pairwise leg holds in >= 0.50 of windows",
         bool(hd["QR_gt_QE"].mean() >= 0.5 and hd["QE_gt_AB"].mean() >= 0.5
              and hd["QR_gt_AB"].mean() >= 0.5),
         f"QR>QE {hd['QR_gt_QE'].mean():.4f}  QE>AB {hd['QE_gt_AB'].mean():.4f}  "
         f"QR>AB {hd['QR_gt_AB'].mean():.4f}"),
        ("H5  exact-match share spans <= 0.10 over the 9 grid points", bool(span <= 0.10),
         f"span {span:.4f}"),
        ("H6  rule 8 on the claim: |OOS - IS| exact share <= 0.10",
         bool(np.isfinite(h6_gap) and h6_gap <= 0.10), f"|gap| {h6_gap:.4f}"),
        ("H7  rule 8 on a book: IS pick beats baseline AND SPY on OOS Sharpe",
         bool(wfa["beats_base"].all() and wfa["beats_spy"].all()),
         f"beats RULES v2 {int(wfa['beats_base'].sum())}/{len(wfa)}, "
         f"SPY {int(wfa['beats_spy'].sum())}/{len(wfa)}"),
        ("H8  some arm clears 4a or 4b at 10 bps",
         bool(ka["p4a"].sum() or ka["p4b"].sum()),
         f"4a {int(ka['p4a'].sum())}, 4b {int(ka['p4b'].sum())}"),
    ]
    for name, ok, note in H:
        log(f"  {'PASS' if ok else 'FAIL'}  {name:64s}  {note}")
    log(f"  {sum(1 for _, ok, _ in H if ok)} of {len(H)} pass")

    # ================================================================ writes
    cen.to_csv(OUT / f"{STEM}.windows.csv.gz", index=False, compression="gzip")
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    at10.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    pd.concat([PUBTAB[k].assign(corpus=k) for k in PUBTAB]).to_csv(OUT / f"{STEM}.fullorder.csv")
    wfc.to_csv(OUT / f"{STEM}.wfclaim.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame([dict(gate=k, value=v, bar=b, verdict="PASS" if p else "FAIL") for k, v, b, p in
                  [("G1", g1, 1e-12, g1 < 1e-12), ("G2", g2, 1e-12, g2 < 1e-12),
                   ("G3", s84, 0.04, ok84),
                   ("G4a", g4a, 1e-9, np.isfinite(g4a) and g4a < 1e-9),
                   ("G4b", g4b, 1e-9, np.isfinite(g4b) and g4b < 1e-9),
                   ("G5", g5, 1e-9, g5 < 1e-9)]]).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    (OUT / f"{STEM}.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.[windows.csv.gz|grid.csv|arms.csv|fullorder.csv|wfclaim.csv|"
          f"walkforward.csv|gates.csv|txt]")


if __name__ == "__main__":
    main()
