#!/usr/bin/env python3
"""Idea 605 - "is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic" (lane C).

The finding this run exists to price
-----------------------------------
Idea 602 measured the MATCHED-MEAN-GROSS STATIC TWIN win rate on 1 944 gated cells and found
that the one dial that moves it hardest is not the firing rate the queue suspected but COST:

    QROLL  0.991 -> 0.963 -> 0.833      ABS  0.574 -> 0.481 -> 0.278      at 0 / 10 / 25 bps

while the same numbers are IDENTICAL at gross 0.75 and 1.00 (3dp in 5 of 6 cells).  Idea 602 read
that as "the twin win rate is largely a switching-cost statistic" and filed this idea to test it.
If the FAMILY ORDERING itself (QROLL > QEXP > ABS) is manufactured by the switching cost, then
every "a gate that fires is not merely a gross dial" claim in the record is a 10-bps-specific
statement about turnover, not a statement about timing information, and the record's twin leg has
been reading a cost ranking as an information ranking.

The algebra makes this exactly testable rather than approximately so.  With r0/t0 the base book's
zero-cost return and turnover, m the EFFECTIVE (t+1-aligned) multiplier and s = |dm| its switch
path, idea 399's overlay convention gives, for EVERY cost rung c, EXACTLY

    r_gate(c) = m*r0 - (c/1e4) * [ m*t0 + g*s ]          r_twin(c) = r0(g_eff) - (c/1e4)*t0(g_eff)

so the whole ladder is derivable from one zero-cost pass (G1), and the gate-minus-twin cost drag
splits with NO residual into two named terms:

    DRAG = mean(m*t0) + g*mean(s) - mean(t0(g_eff))  ==  TIMING + SWITCH_TAX
    SWITCH_TAX = g*mean(s)   >= 0 always, the pure tax for moving the dial
    TIMING     = mean(m*t0) - mean(t0(g_eff))        , what de-grossing SAVES on the base's own
                 turnover when it de-grosses on days the base is churning

"The twin win rate is a switching-cost statistic" is then a testable claim about which term
carries the ladder, and "the family ordering is a switching-cost ranking" is a testable claim
about what the ordering looks like at c = 0.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (LADDER)      Is the twin win rate monotone DECREASING in cost, within each of
                     ABS / QEXP / QROLL and pooled, over a 15-rung ladder 0 -> 100 bps?
                     Pre-registered bar: every adjacent rung step non-increasing AND
                     per-family Spearman(cost, win rate) <= -0.80.
    Q2 (ORDERING)    THE DECIDING TEST.  Is the family ordering a switching-cost ranking?
                     Pre-registered, either leg suffices:
                       (a) the between-family win-rate spread at c = 0 is <= 0.10 (the families
                           are indistinguishable before cost is charged), OR
                       (b) the ordering INVERTS at some rung on the ladder (Spearman of the
                           family win-rate vector against its c=0 order goes <= 0).
                     If neither holds, the ordering is present at ZERO cost and the queue's
                     worry is refuted: cost moves the LEVEL of the win rate, not its ORDER.
                     Also reported: the arm-level rank stability of dSharpe across the ladder,
                     and the crossing cost c* at which each family's win rate falls below 0.50.
    Q3 (MECHANISM)   Decompose every arm's drag into SWITCH_TAX + TIMING (exact, no residual).
                     Which carries it?  Does SWITCH_TAX order the arm-level crossover cost c*
                     (the cost at which dSharpe changes sign)?  And the sufficiency leg: at
                     MATCHED switch tax, does the family gap in the win rate survive?  If the
                     mechanism is switching cost, matching on it should erase the family label.
    Q4 (CADENCE)     Tuned param 2.  Weekly cadence caps the dial at ~52 switches a year and
                     daily does not, so cadence is a direct experimental handle on the switch
                     count at an UNCHANGED signal.  Does the cost decay track the cadence?
                     Reported as the per-cadence win-rate ladder, switch tax and half-cost.
    Q5 (PROTOCOL)    Both KEEP paths on every one of the 9 720 gated grid points, the rule-8
                     chooser (IS <= 2016 pick, OOS 2017+ read once) at EVERY rung, and rule 8
                     on the CLAIM itself: fit the cost -> win relation on IS only and read it
                     once out of sample.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. cost      15 rungs, 0 / 1 / 2 / 3 / 5 / 7.5 / 10 / 15 / 20 / 25 / 30 / 40 / 50 / 75 / 100
                 bps, ALL reported at every panel / family / level / depth / cadence / gross.
    2. cadence   D / W, both reported everywhere.

Reported axes, NEVER tuned or selected on (inherited verbatim from idea 602 so the population is
literally the same one, joined row-for-row at rungs 0/10/25 in G3)
    family   ABS(B in 0.30/0.40/0.50) / QEXP(q) / QROLL(q, w)
    q        0.07 / 0.12 / 0.17      w  252 / 504 / 1008 / 2016
    depth    0.25 / 0.50 / 1.00      panel  U56 / B136 / SMALL439      gross  0.75 / 1.00

Reproduction gates (section [0], printed before any new number is read)
    G1  the derived ladder r_gate(c) = m*r0 - (c/1e4)*(m*t0 + g*s) vs a LIVE engine.backtest of
        the base at cost c put through idea 399's own apply_gate, at every rung.
    G2  fast numpy metrics (CAGR / Sharpe / MaxDD) vs engine.metrics on 200 real series.
    G3  idea 602's COMMITTED .cells.csv, all 1 944 gated rows joined at rungs 0/10/25 and
        differenced on dSharpe / Sharpe / twin_Sharpe / on_share / g_eff - and its published
        family x rung win-rate headline (QROLL .991/.963/.833, ABS .574/.481/.278) reproduced.
    G4  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.
    G5  the drag identity DRAG == SWITCH_TAX + TIMING on all 648 arms (bar 1e-15).

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
current-constituent lists, so CAGR and drawdown LEVELS are optimistic; the gate-minus-twin
contrast and its cost slope are the durable part.  SMALL439 starts 2010-01-04 (its halves are not
U56/B136's calendar halves) and w=2016 spends half its sample unarmed.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
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
PARENT_CELLS = OUT / "2026-09-10_is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function_C.cells.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]                                    # tuned param 2
RUNGS = [0.0, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 75.0, 100.0]  # tuned 1
PARENT_RUNGS = [0.0, 10.0, 25.0]                               # idea 602's three, for G3
RUNG_HEAD = 10.0
C0, CTOP = 0.0, 100.0
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12                                              # ideas 594/595: a tie is NOT a win

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/336/399)
_ELIG = {}


def eligible_mask(px):
    """idea 28/42's eligibility, memoised per panel (the twin cache calls it ~40x a panel;
    the memo is keyed on the panel's shape and endpoints and changes no number)."""
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


# ---------------------------------------------------------------- fast metrics (G2)
def fmet(r):
    """CAGR / Sharpe / MaxDD on a float array, identical to engine.metrics (gate G2)."""
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


class Slices:
    """Index positions reused for every series on a panel."""

    def __init__(self, idx):
        self.n = len(idx)
        self.h = self.n // 2
        self.is_end = int(idx.searchsorted(pd.Timestamp(IS_END), side="right"))
        self.oos = int(idx.searchsorted(pd.Timestamp(OOS_START), side="left"))


def pack(r, S):
    """(CAGR, Sharpe, MaxDD, H1, H2, IS_Sharpe, OOS_CAGR, OOS_Sharpe, OOS_MaxDD)."""
    c, s, d = fmet(r)
    h1 = fsharpe(r[:S.h])
    h2 = fsharpe(r[S.h:])
    is_s = fsharpe(r[:S.is_end])
    oc, os_, od = fmet(r[S.oos:])
    return c, s, d, h1, h2, is_s, oc, os_, od


def auc(score_v, label):
    s = np.asarray(score_v, float)
    y = np.asarray(label, bool)
    ok = np.isfinite(s)
    s, y = s[ok], y[ok]
    if y.sum() == 0 or (~y).sum() == 0:
        return np.nan
    r = pd.Series(s).rank().values
    n1, n0 = y.sum(), (~y).sum()
    return (r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


# ---------------------------------------------------------------- twin machinery (idea 602)
GSTEP = 0.01


class Twins:
    """Static-gross EWALL twin (returns, turnover) at cost 0.  Exact g by linear interpolation
    on a GSTEP cache; idea 602's G4 priced the interpolation error at <= 4e-07 of Sharpe."""

    def __init__(self, px, start):
        self.px, self.start = px, start
        self.cache = {}
        self.n_bt = 0

    def _exact(self, g):
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
            self._exact(g)

    def at0(self, g):
        """Zero-cost (returns, turnover) arrays at exact gross g."""
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            return self._exact(lo)
        rl, tl = self._exact(lo)
        rh, th = self._exact(round(lo + GSTEP, 6))
        return (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th


# ---------------------------------------------------------------- per-panel run
def run_panel(panel, px, parent):
    start = px.index[260]
    idx = px.index
    eval_idx = px.loc[start:].index
    S = Slices(eval_idx)
    spy = px["SPY"].pct_change().fillna(0).loc[start:].values
    sc, ss, sd = fmet(spy)
    spy_pack = (fsharpe(spy[:S.h]), fsharpe(spy[S.h:]), fsharpe(spy[S.oos:]), sd, sc)

    br_full = breadth(px)
    br = br_full.loc[start:]
    log(f"\n{'='*185}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(br)} days)")
    log(f"  SPY {sc:.2%} / {ss:.3f} / {sd:.2%}; 4b bars: CAGR floor {0.70*sc:.2%}, DD cap "
        f"{-0.60*abs(sd):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, OOS {spy_pack[2]:.3f}")

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}

    # ---- references and base books, zero cost + turnover (every rung derived, G1)
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:].values, res["turnover"].loc[start:].values)
    rv2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    rv1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)
    ref0 = {"v2": (rv2["returns"].loc[start:].values, rv2["turnover"].loc[start:].values),
            "v1": (rv1["returns"].loc[start:].values, rv1["turnover"].loc[start:].values),
            "SPY": (spy, np.zeros(len(spy)))}
    base_packs = {}
    for c in RUNGS:
        b = ref0["v2"][0] - ref0["v2"][1] * c / 1e4
        base_packs[c] = (fsharpe(b[:S.h]), fsharpe(b[S.h:]), fmet(b)[2])

    # ---- arms
    arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
            + [("QROLL", q, w) for q in QS for w in WS])
    m_eff, switch, on_share, rate_inst = {}, {}, {}, {}
    for fam, lev, w in arms:
        thr = None if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
        rate_inst[(fam, lev, w)] = float((br < lev).mean()) if fam == "ABS" \
            else float((br < thr.loc[start:]).mean())
        for d, cad in product(DEPTHS, CADENCES):
            m = (gate_abs(br_full, lev, d, cad, idx) if fam == "ABS"
                 else gate_from_thr(br_full, thr, d, cad, idx))
            me = m.reindex(eval_idx).shift(1).fillna(1.0).values
            m_eff[(fam, lev, w, d, cad)] = me
            switch[(fam, lev, w, d, cad)] = np.abs(np.diff(me, prepend=me[0]))
            on_share[(fam, lev, w, d, cad)] = float((me < 1.0).mean())

    tw = Twins(px, start)
    tw.prewarm([g * float(m_eff[(f, l, w, d, cad)].mean())
                for (f, l, w), (d, cad), g in
                product(arms, product(DEPTHS, CADENCES), GROSSES)])
    log(f"  twin gross cache: {tw.n_bt} backtests on a {GSTEP} grid spanning "
        f"{min(tw.cache):.2f}-{max(tw.cache):.2f}")

    # ---- the 216 twin pairs, then the whole cost ladder derived on each
    cells, drag = [], []
    for g in GROSSES:
        r0, t0 = base0[g]
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            key = (fam, lev, w, d, cad)
            me, sw = m_eff[key], switch[key]
            g_eff = g * float(me.mean())
            rg0, Cg = me * r0, me * t0 + g * sw
            rs0, Cs = tw.at0(g_eff)
            tax = g * float(sw.mean())
            timing = float((me * t0).mean()) - float(Cs.mean())
            dr = float(Cg.mean() - Cs.mean())
            drag.append(dict(panel=panel, gross=g, family=fam, level=lev, w=w, depth=d,
                             cadence=cad, arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                             on_share=on_share[key], rate_inst=rate_inst[(fam, lev, w)],
                             g_eff=g_eff, gap=1.0 - float(me.mean()),
                             n_switch=float((sw > 1e-12).sum()),
                             switch_per_yr=float((sw > 1e-12).sum()) / (len(sw) / 252.0),
                             switch_tax=tax, timing=timing, drag=dr,
                             resid=dr - (tax + timing),
                             tax_share=tax / abs(dr) if abs(dr) > 1e-18 else np.nan))

            def dsh(c):
                return fsharpe(rg0 - Cg * c / 1e4) - fsharpe(rs0 - Cs * c / 1e4)

            # crossover cost c*: bisection on the exact derived ladder, 0 -> 500 bps
            d0 = dsh(0.0)
            cstar = np.nan
            if np.isfinite(d0):
                if d0 <= 0:
                    cstar = 0.0
                elif dsh(500.0) > 0:
                    cstar = np.inf
                else:
                    lo, hi = 0.0, 500.0
                    for _ in range(45):
                        mid = 0.5 * (lo + hi)
                        if dsh(mid) > 0:
                            lo = mid
                        else:
                            hi = mid
                    cstar = 0.5 * (lo + hi)
            drag[-1]["dSharpe_0"] = d0
            drag[-1]["cstar"] = cstar

            for c in RUNGS:
                rg, rs = rg0 - Cg * c / 1e4, rs0 - Cs * c / 1e4
                pg, ps = pack(rg, S), pack(rs, S)
                dsv = pg[1] - ps[1]
                b1, b2, bdd = base_packs[c]
                s1, s2, so, sdd, scg = spy_pack
                t4b = dict(H1=pg[3] > s1, H2=pg[4] > s2, OOS=pg[7] > so,
                           DD=abs(pg[2]) <= 0.60 * abs(sdd), CAGR=pg[0] >= 0.70 * scg)
                cells.append(dict(
                    panel=panel, rung=c, gross=g, family=fam, level=lev, w=w, depth=d,
                    cadence=cad, arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                    rate_inst=rate_inst[(fam, lev, w)], on_share=on_share[key],
                    gap=1.0 - float(me.mean()), g_eff=g_eff, switch_tax=tax, drag=dr,
                    CAGR=pg[0], Sharpe=pg[1], MaxDD=pg[2], H1=pg[3], H2=pg[4],
                    IS_Sharpe=pg[5], OOS_CAGR=pg[6], OOS_Sharpe=pg[7], OOS_MaxDD=pg[8],
                    twin_Sharpe=ps[1], twin_OOS=ps[7], twin_IS=ps[5],
                    dSharpe=dsv, dOOS=pg[7] - ps[7], dCAGR=pg[0] - ps[0],
                    dMaxDD=abs(ps[2]) - abs(pg[2]),
                    dIS=pg[5] - ps[5], win=bool(dsv > TIE), tie=bool(abs(dsv) <= TIE),
                    p4a=bool(pg[3] > b1 and pg[4] > b2 and pg[2] >= bdd),
                    p4b=all(t4b.values()),
                    fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))

    # ---- ungated parents and references, at every rung (context rows, family="ref"/"NOGATE")
    for c in RUNGS:
        for nm, (r0, t0) in ref0.items():
            r = r0 - t0 * c / 1e4
            p = pack(r, S)
            cells.append(dict(panel=panel, rung=c, gross=np.nan, family="ref", level=np.nan,
                              w=np.nan, depth=np.nan, cadence="-", arm=nm, rate_inst=np.nan,
                              on_share=np.nan, gap=np.nan, g_eff=np.nan, switch_tax=np.nan,
                              drag=np.nan, CAGR=p[0], Sharpe=p[1], MaxDD=p[2], H1=p[3], H2=p[4],
                              IS_Sharpe=p[5], OOS_CAGR=p[6], OOS_Sharpe=p[7], OOS_MaxDD=p[8],
                              twin_Sharpe=np.nan, twin_OOS=np.nan, twin_IS=np.nan,
                              dSharpe=np.nan, dOOS=np.nan, dCAGR=np.nan, dMaxDD=np.nan,
                              dIS=np.nan, win=False, tie=False, p4a=False, p4b=False,
                              fail4b="-"))
        for g in GROSSES:
            r0, t0 = base0[g]
            r = r0 - t0 * c / 1e4
            p = pack(r, S)
            s1, s2, so, sdd, scg = spy_pack
            b1, b2, bdd = base_packs[c]
            t4b = dict(H1=p[3] > s1, H2=p[4] > s2, OOS=p[7] > so,
                       DD=abs(p[2]) <= 0.60 * abs(sdd), CAGR=p[0] >= 0.70 * scg)
            cells.append(dict(panel=panel, rung=c, gross=g, family="NOGATE", level=np.nan,
                              w=np.nan, depth=0.0, cadence="-", arm=f"NOGATE g{g:.2f}",
                              rate_inst=0.0, on_share=0.0, gap=0.0, g_eff=g, switch_tax=0.0,
                              drag=0.0, CAGR=p[0], Sharpe=p[1], MaxDD=p[2], H1=p[3], H2=p[4],
                              IS_Sharpe=p[5], OOS_CAGR=p[6], OOS_Sharpe=p[7], OOS_MaxDD=p[8],
                              twin_Sharpe=np.nan, twin_OOS=np.nan, twin_IS=np.nan,
                              dSharpe=np.nan, dOOS=np.nan, dCAGR=np.nan, dMaxDD=np.nan,
                              dIS=np.nan, win=False, tie=False,
                              p4a=bool(p[3] > b1 and p[4] > b2 and p[2] >= bdd),
                              p4b=all(t4b.values()),
                              fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))

    cells = pd.DataFrame(cells)
    drag = pd.DataFrame(drag)

    # ---- G3: join idea 602's committed rows at its three rungs
    g3 = pd.DataFrame()
    if parent is not None:
        p = parent[(parent["panel"] == panel) & (~parent["family"].isin(["ref", "NOGATE"]))].copy()
        key = ["panel", "rung", "gross", "family", "level", "w", "depth", "cadence"]
        mine = cells[cells["rung"].isin(PARENT_RUNGS)].copy()
        for df in (p, mine):
            for k in ("rung", "gross", "level", "w", "depth"):
                df[k] = df[k].astype(float).round(6)
        g3 = mine.merge(p, on=key, suffixes=("", "_602"))
        for col in ("dSharpe", "Sharpe", "twin_Sharpe", "on_share", "g_eff", "dOOS", "dMaxDD"):
            g3["d_" + col] = (g3[col] - g3[col + "_602"]).abs()

    # ---- rule 8: chooser over (level, w, depth) on IS Sharpe, per family x cadence x rung
    wf = []
    ng = cells[(cells["family"] == "NOGATE") & (cells["gross"] == G_HEAD)].set_index("rung")
    for c in RUNGS:
        for fam in ("ABS", "QEXP", "QROLL"):
            for cad in CADENCES:
                sub = cells[(cells["rung"] == c) & (cells["gross"] == G_HEAD)
                            & (cells["family"] == fam) & (cells["cadence"] == cad)]
                if not len(sub):
                    continue
                pick = sub.loc[sub["IS_Sharpe"].idxmax()]
                best = sub.loc[sub["OOS_Sharpe"].idxmax()]
                v2 = cells[(cells["rung"] == c) & (cells["family"] == "ref")
                           & (cells["arm"] == "v2")].iloc[0]
                sp = cells[(cells["rung"] == c) & (cells["family"] == "ref")
                           & (cells["arm"] == "SPY")].iloc[0]
                wf.append(dict(panel=panel, rung=c, family=fam, cadence=cad, pick=pick["arm"],
                               pick_on_share=pick["on_share"], pick_tax=pick["switch_tax"],
                               IS_Sharpe=pick["IS_Sharpe"], OOS_Sharpe=pick["OOS_Sharpe"],
                               OOS_CAGR=pick["OOS_CAGR"], OOS_MaxDD=pick["OOS_MaxDD"],
                               OOS_dSharpe=pick["dOOS"], OOS_win=bool(pick["dOOS"] > TIE),
                               nogate_OOS=ng.loc[c, "OOS_Sharpe"],
                               vs_nogate=pick["OOS_Sharpe"] - ng.loc[c, "OOS_Sharpe"],
                               v2_OOS=v2["OOS_Sharpe"], spy_OOS=sp["OOS_Sharpe"],
                               p4a=bool(pick["p4a"]), p4b=bool(pick["p4b"]),
                               fail4b=pick["fail4b"],
                               regret=pick["OOS_Sharpe"] - best["OOS_Sharpe"]))

    return cells, drag, pd.DataFrame(wf), g3, S


# ---------------------------------------------------------------- main
def main():
    log("=" * 185)
    log(f"Idea 605 is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic (lane C) | {SCRIPT}")
    log("=" * 185)
    log("Base book (fixed, idea 28/42/336/399's): EWALL(G) = equal weight every name above its")
    log("  own 200d MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is BELOW the threshold.")
    log("Comparand for EVERY arm: the MATCHED-MEAN-GROSS STATIC TWIN (EWALL at constant g_eff).")
    log(f"Tuned (2): cost rung in {RUNGS} bps, and cadence in {CADENCES}.")
    log("Reported never tuned: family, level, w, depth, panel, gross.  Population is idea 602's,")
    log(f"  joined row-for-row at rungs {PARENT_RUNGS} in G3.  Tie bar |dSharpe| <= {TIE:g}.")
    log("Exact ladder algebra: r_gate(c) = m*r0 - (c/1e4)*(m*t0 + g*|dm|), r_twin(c) = r0(g_eff)")
    log("  - (c/1e4)*t0(g_eff); DRAG = SWITCH_TAX + TIMING with no residual (G5).")

    # =================================================================== [0] gates
    log("\n" + "=" * 185)
    log("[0] REPRODUCTION GATES (all printed before any new number is read)")
    px0 = load_universe()
    st0 = px0.index[260]
    idx0 = px0.loc[st0:].index

    # G1 - the derived ladder against a live backtest put through idea 399's apply_gate
    res0 = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=0, freq=FREQ)
    r0 = res0["returns"].loc[st0:].values
    t0 = res0["turnover"].loc[st0:].values
    brf = breadth(px0)
    mtest = gate_abs(brf, 0.40, 0.50, "W", px0.index).reindex(idx0).shift(1).fillna(1.0)
    me = mtest.values
    sw = np.abs(np.diff(me, prepend=me[0]))
    g1 = 0.0
    for c in RUNGS:
        live = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=c,
                        freq=FREQ)["returns"].loc[st0:].values
        ref = me * live - sw * G_HEAD * c / 1e4                 # idea 399's apply_gate verbatim
        der = me * r0 - (me * t0 + G_HEAD * sw) * c / 1e4       # this run's derived ladder
        g1 = max(g1, float(np.abs(live - (r0 - t0 * c / 1e4)).max()),
                 float(np.abs(ref - der).max()))
    log(f"  G1 derived ladder == live backtest through apply_gate, all {len(RUNGS)} rungs: "
        f"max |diff| = {g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    # G2 - fast metrics vs engine.metrics on 200 real series
    rng = np.random.default_rng(605)
    g2 = 0.0
    for k in range(200):
        c = float(rng.uniform(0, 100))
        a, b = sorted(rng.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        s = pd.Series((r0 - t0 * c / 1e4)[a:b], index=idx0[a:b])
        mm = metrics(s)
        f = fmet(s.values)
        g2 = max(g2, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G2 fast metrics vs engine.metrics on 200 series: max |diff| = {g2:.3e} "
        f"(bar 1e-12) -> {'PASS' if g2 < 1e-12 else 'FAIL'}")

    # G4 - idea 84
    r84 = backtest(px0, ewall_weights(px0, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[st0:]
    c84, s84, d84 = fmet(r84.values)
    S0 = Slices(idx0)
    h84 = (fsharpe(r84.values[:S0.h]), fsharpe(r84.values[S0.h:]))
    ok84 = (abs(c84 - 0.118) < 0.004 and abs(s84 - 1.05) < 0.04 and abs(abs(d84) - 0.179) < 0.006)
    log(f"  G4 idea 84 EWALL U56 g=0.85 @10bps: {c84:.3%} / {s84:.3f} / {d84:.3%} / "
        f"H {h84[0]:.3f} / {h84[1]:.3f}  (published 11.8% / 1.05 / -17.9% / 1.07 / 1.04) -> "
        f"{'PASS' if ok84 else 'FAIL'}")

    parent = None
    if PARENT_CELLS.exists():
        parent = pd.read_csv(PARENT_CELLS)
        log(f"  G3 source: idea 602 {PARENT_CELLS.name}, {len(parent)} rows "
            f"({int((~parent['family'].isin(['ref','NOGATE'])).sum())} gated)")
    else:
        log("  G3 source: idea 602 cells.csv NOT FOUND -> G3 cannot run")

    # ================================================================ panels
    panels = [("U56", px0), ("B136", load_universe(broad=True))]
    ps, ndrop = small_panel()
    panels.append(("SMALL439", ps))
    log(f"  SMALL panel: dropped {ndrop} names with max_1d_move >= 1.0 -> {ps.shape[1]-1} names "
        f"+ SPY (idea 399/602's construction, so their rows join)")

    CELLS, DRAG, WF, G3 = [], [], [], []
    for name, px in panels:
        cells, drag, wf, g3, _ = run_panel(name, px, parent)
        CELLS.append(cells)
        DRAG.append(drag)
        WF.append(wf)
        if len(g3):
            G3.append(g3)
    cells = pd.concat(CELLS, ignore_index=True)
    drag = pd.concat(DRAG, ignore_index=True)
    wf = pd.concat(WF, ignore_index=True)
    g3 = pd.concat(G3, ignore_index=True) if G3 else pd.DataFrame()

    gc = cells[~cells["family"].isin(["ref", "NOGATE"])].copy()
    log("\n" + "=" * 185)
    log(f"POPULATION: {len(gc)} gated cells = {len(drag)} twin pairs x {len(RUNGS)} cost rungs "
        f"({gc['panel'].nunique()} panels x 18 arms x {len(DEPTHS)} depths x {len(CADENCES)} "
        f"cadences x {len(GROSSES)} gross).  Ties: {int(gc['tie'].sum())}.")

    # ---- G3 / G5 verdicts, still before any new number
    log("\n" + "=" * 185)
    log("[0b] G3 / G5")
    if len(g3):
        cols = [c for c in g3.columns if c.startswith("d_")]
        g3max = float(g3[cols].max().max())
        log(f"  G3 idea 602 join: {len(g3)} rows on "
            f"{['dSharpe','Sharpe','twin_Sharpe','on_share','g_eff','dOOS','dMaxDD']}")
        log("     max |diff| by column: " + "  ".join(
            f"{c[2:]} {g3[c].max():.3e}" for c in cols))
        log(f"     per panel: " + "  ".join(
            f"{p} {g3[g3['panel']==p][cols].max().max():.3e}" for p in sorted(g3["panel"].unique())))
        log(f"  -> G3 {'PASS' if g3max < 1e-9 else 'FAIL'} (bar 1e-9)")
        pub = g3.groupby(["family", "rung"])["win"].mean().unstack()
        log("     idea 602's published family x rung win rate, recomputed here:")
        log(pub.to_string(float_format=lambda x: f"{x:.3f}"))
        log("     published: QROLL 0.991 / 0.963 / 0.833, QEXP 0.750 / 0.574* / --, "
            "ABS 0.574 / 0.481 / 0.278  (*idea 602 quotes ABS at 0/10/25)")
    else:
        g3max = np.nan
        log("  G3 skipped")
    g5 = float(drag["resid"].abs().max())
    log(f"  G5 drag identity DRAG == SWITCH_TAX + TIMING on {len(drag)} arms: max |resid| "
        f"{g5:.3e} (bar 1e-15) -> {'PASS' if g5 < 1e-15 else 'FAIL'}")

    # =============================================================== [1] Q1 the ladder
    log("\n" + "=" * 185)
    log("[1] Q1 - THE COST LADDER.  Twin win rate at every rung, by family (all panels, both")
    log("    gross, both cadences, all depths pooled - i.e. the same population at every rung).")
    lad = gc.pivot_table(index="family", columns="rung", values="win", aggfunc="mean")
    lad.loc["POOLED"] = gc.groupby("rung")["win"].mean()
    log(lad.to_string(float_format=lambda x: f"{x:.3f}"))
    log("\n  median dSharpe at every rung:")
    med = gc.pivot_table(index="family", columns="rung", values="dSharpe", aggfunc="median")
    med.loc["POOLED"] = gc.groupby("rung")["dSharpe"].median()
    log(med.to_string(float_format=lambda x: f"{x:+.4f}"))

    mono = []
    for fam in list(lad.index):
        v = lad.loc[fam].values
        st = np.diff(v)
        mono.append(dict(family=fam, w0=v[0], w10=lad.loc[fam, RUNG_HEAD], w100=v[-1],
                         span=v[0] - v[-1], monotone_down=bool((st <= 1e-12).all()),
                         n_up_steps=int((st > 1e-12).sum()),
                         rho=spearman(lad.columns.values, v)))
    mono = pd.DataFrame(mono)
    log("\n  pre-registered Q1 bar: every adjacent step non-increasing AND rho <= -0.80")
    log(mono.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    q1_pass = bool(mono["monotone_down"].all() and (mono["rho"] <= -0.80).all())
    log(f"  -> Q1 {'CONFIRMED' if q1_pass else 'FAILS'}")

    log("\n  the same ladder split by panel (the population is fixed, only cost moves):")
    log(gc.pivot_table(index=["panel", "family"], columns="rung", values="win",
                       aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))

    # =============================================================== [2] Q2 the ordering
    log("\n" + "=" * 185)
    log("[2] Q2 - IS THE FAMILY ORDERING A SWITCHING-COST RANKING?  (the deciding test)")
    fam0 = lad.drop(index="POOLED")[C0]
    spread0 = float(fam0.max() - fam0.min())
    order0 = fam0.rank()
    ordering = []
    for c in RUNGS:
        v = lad.drop(index="POOLED")[c]
        ordering.append(dict(rung=c, spread=float(v.max() - v.min()),
                             rho_vs_c0=spearman(order0.values, v.rank().values),
                             top=v.idxmax(), bottom=v.idxmin(),
                             **{f"win_{k}": float(v[k]) for k in v.index}))
    ordering = pd.DataFrame(ordering)
    log(ordering.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    leg_a = spread0 <= 0.10
    leg_b = bool((ordering["rho_vs_c0"] <= 0).any())
    log(f"\n  leg (a) between-family spread at 0 bps <= 0.10:  spread = {spread0:.4f} -> "
        f"{'TRUE' if leg_a else 'FALSE'}")
    log(f"  leg (b) ordering inverts at some rung (rho vs the 0-bps order <= 0):  min rho = "
        f"{ordering['rho_vs_c0'].min():+.4f} -> {'TRUE' if leg_b else 'FALSE'}")
    log(f"  => the family ordering IS{'' if (leg_a or leg_b) else ' NOT'} a switching-cost "
        f"ranking (pre-registered).")
    inv = ordering[ordering["rho_vs_c0"] <= 0]
    first_inv = float(inv["rung"].min()) if len(inv) else np.nan
    band = ordering[ordering["rung"] <= 25.0]
    log(f"  WHERE it inverts: first rung with rho <= 0 is {first_inv} bps; inside the TRADABLE "
        f"band (0-25 bps, PROTOCOL charges 10) min rho = {band['rho_vs_c0'].min():+.4f}, "
        f"top family {sorted(set(band['top']))}, spread {band['spread'].min():.3f}-"
        f"{band['spread'].max():.3f}.  A ranking that only inverts above the band is not a")
    log("  ranking any live book could observe; report both numbers, never just the inversion.")

    log("\n  crossing cost: the first rung at which each family's win rate falls below 0.50")
    for fam in lad.index:
        v = lad.loc[fam]
        below = [c for c in RUNGS if v[c] < 0.50]
        log(f"    {fam:7s} win@0 {v[C0]:.3f}  win@10 {v[RUNG_HEAD]:.3f}  win@100 {v[CTOP]:.3f}  "
            f"first rung < 0.50: {below[0] if below else 'never on this ladder'}")

    log("\n  arm-level rank stability: Spearman of the 648 arms' dSharpe at rung c against "
        "rung 0")
    piv = gc.pivot_table(index=["panel", "arm"], columns="rung", values="dSharpe")
    stab = pd.DataFrame([dict(rung=c, rho_vs_0=spearman(piv[C0], piv[c]),
                              sign_agree=float((np.sign(piv[C0]) == np.sign(piv[c])).mean()))
                         for c in RUNGS])
    log(stab.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # =============================================================== [3] Q3 mechanism
    log("\n" + "=" * 185)
    log("[3] Q3 - MECHANISM: DRAG = SWITCH_TAX + TIMING (exact, G5), and what orders c*")
    log("    Units: drag terms are daily return per 1 bp of cost, x1e-4; i.e. a drag of 1.0 costs")
    log("    1 bp of daily return at 1e4 bps.  Positive drag = the GATE pays more than its twin.")
    dsum = drag.groupby("family").agg(
        n=("drag", "size"), switch_yr=("switch_per_yr", "median"),
        tax=("switch_tax", "median"), timing=("timing", "median"), drag_=("drag", "median"),
        tax_share=("tax_share", "median"), cstar=("cstar", "median"),
        dSh0=("dSharpe_0", "median"))
    log(dsum.to_string(float_format=lambda x: f"{x:+.5f}"))
    log("\n  by family x cadence (Q4's handle):")
    log(drag.groupby(["family", "cadence"]).agg(
        n=("drag", "size"), switch_yr=("switch_per_yr", "median"),
        tax=("switch_tax", "median"), timing=("timing", "median"), drag_=("drag", "median"),
        cstar_med=("cstar", "median"),
        cstar_finite=("cstar", lambda s: int(np.isfinite(s).sum()))).to_string(
        float_format=lambda x: f"{x:+.5f}"))
    log(f"\n  share of arms where TIMING (not the switch tax) carries the sign of the drag: "
        f"{float((np.sign(drag['timing']) == np.sign(drag['drag'])).mean()):.3f}; "
        f"where |timing| > |tax|: {float((drag['timing'].abs() > drag['switch_tax']).mean()):.3f}")
    log(f"  median tax / |drag| = {drag['tax_share'].median():+.3f}; "
        f"arms with drag <= 0 (the gate is CHEAPER than its own twin): "
        f"{int((drag['drag'] <= 0).sum())} of {len(drag)}")

    log("\n  does the switch tax order the crossover cost c*?  (finite c* only)")
    fin = drag[np.isfinite(drag["cstar"]) & (drag["cstar"] > 0)]
    for grp, sub in list(fin.groupby("family")) + [("POOLED", fin)]:
        log(f"    {grp:7s} n={len(sub):4d}  rho(tax, c*) {spearman(sub['switch_tax'], sub['cstar']):+.4f}"
            f"   rho(drag, c*) {spearman(sub['drag'], sub['cstar']):+.4f}"
            f"   rho(dSharpe_0, c*) {spearman(sub['dSharpe_0'], sub['cstar']):+.4f}"
            f"   median c* {sub['cstar'].median():7.2f} bps")
    log(f"  arms never crossing on 0-500 bps: {int(np.isinf(drag['cstar']).sum())}; "
        f"already <= 0 at zero cost: {int((drag['cstar'] == 0).sum())}")

    log("\n  SUFFICIENCY: at MATCHED switch tax, does the family gap in the win rate survive?")
    hd = gc[gc["rung"] == RUNG_HEAD].copy()
    hd["tb"] = pd.qcut(hd["switch_tax"], 5, labels=False, duplicates="drop")
    suf = hd.pivot_table(index="tb", columns="family", values="win", aggfunc="mean")
    cnt = hd.pivot_table(index="tb", columns="family", values="win", aggfunc="size")
    suf["tax_med"] = hd.groupby("tb")["switch_tax"].median()
    suf["max_gap"] = suf[["ABS", "QEXP", "QROLL"]].max(axis=1) - suf[["ABS", "QEXP", "QROLL"]].min(axis=1)
    log("   win rate at 10 bps inside equal-count switch-tax buckets:")
    log(suf.to_string(float_format=lambda x: f"{x:.4f}"))
    log("   cell counts:")
    log(cnt.to_string())
    log(f"   median within-bucket family gap {suf['max_gap'].median():.3f}, "
        f"max {suf['max_gap'].max():.3f}  -> the family label "
        f"{'survives' if suf['max_gap'].median() > 0.10 else 'does NOT survive'} matching on "
        f"the switch tax")
    log("\n   pooled AUC for the win label at 10 bps: "
        f"switch_tax {auc(-hd['switch_tax'], hd['win']):.4f} (sign-flipped: less tax -> win) | "
        f"drag {auc(-hd['drag'], hd['win']):.4f} | on_share {auc(hd['on_share'], hd['win']):.4f} | "
        f"g_eff {auc(hd['g_eff'], hd['win']):.4f}")

    # =============================================================== [4] Q4 cadence
    log("\n" + "=" * 185)
    log("[4] Q4 - CADENCE (tuned param 2): the same signal, a different switch count")
    cad = gc.pivot_table(index=["family", "cadence"], columns="rung", values="win",
                         aggfunc="mean")
    log(cad.to_string(float_format=lambda x: f"{x:.3f}"))
    log("\n  median dSharpe:")
    log(gc.pivot_table(index=["family", "cadence"], columns="rung", values="dSharpe",
                       aggfunc="median").to_string(float_format=lambda x: f"{x:+.4f}"))
    cc = []
    for (fam, cd), sub in gc.groupby(["family", "cadence"]):
        v = sub.groupby("rung")["win"].mean()
        d = drag[(drag["family"] == fam) & (drag["cadence"] == cd)]
        cc.append(dict(family=fam, cadence=cd, switch_yr=d["switch_per_yr"].median(),
                       tax=d["switch_tax"].median(), win0=v[C0], win10=v[RUNG_HEAD],
                       win100=v[CTOP], decay_0_100=v[C0] - v[CTOP], rho=spearman(v.index.values, v.values),
                       cstar_med=d["cstar"].median()))
    cc = pd.DataFrame(cc)
    log("\n  decay by cadence (if the win rate is a switching-cost statistic, D - which switches "
        "far\n  more often - must decay far faster than W at the same signal):")
    log(cc.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    log("\n  switch-count ratio D:W vs decay ratio D:W  (the switching-cost story predicts the")
    log("  two ratios move together; a decay ratio near 1 at a switch ratio far from 1 refutes it)")
    for fam in sorted(cc["family"].unique()):
        d_ = cc[(cc["family"] == fam) & (cc["cadence"] == "D")].iloc[0]
        w_ = cc[(cc["family"] == fam) & (cc["cadence"] == "W")].iloc[0]
        sr = d_["switch_yr"] / max(w_["switch_yr"], 1e-9)
        dr = (d_["decay_0_100"] / w_["decay_0_100"]) if abs(w_["decay_0_100"]) > 1e-12 else np.nan
        log(f"    {fam:7s} switches/yr D {d_['switch_yr']:7.2f} vs W {w_['switch_yr']:7.2f} "
            f"(ratio {sr:5.2f}x)   decay 0->100bps D {d_['decay_0_100']:+.3f} vs W "
            f"{w_['decay_0_100']:+.3f} (ratio {dr:5.2f}x)   tax D {d_['tax']:.5f} vs W "
            f"{w_['tax']:.5f}")

    # =============================================================== [5] Q5 PROTOCOL + rule 8
    log("\n" + "=" * 185)
    log("[5] Q5 - PROTOCOL KEEP PATHS AND RULE 8")
    log(f"  4a (Sharpe > RULES v2 both halves, MaxDD no worse) and 4b (vs SPY) on all {len(gc)} "
        f"gated grid points:")
    gc["both"] = gc["p4a"] & gc["p4b"]
    kp = gc.groupby("rung").agg(n=("p4a", "size"), pass4a=("p4a", "sum"),
                                pass4b=("p4b", "sum"), both=("both", "sum"))
    log(kp.to_string())
    log("\n  by gross at the PROTOCOL rung (10 bps):")
    log(gc[gc["rung"] == RUNG_HEAD].groupby(["gross", "family"]).agg(
        n=("p4a", "size"), pass4a=("p4a", "sum"), pass4b=("p4b", "sum")).to_string())
    if int(gc["p4a"].sum()):
        pa = gc[gc["p4a"]]
        log(f"\n  every 4a pass ({len(pa)}):")
        log(pa[["panel", "rung", "gross", "arm", "on_share", "CAGR", "Sharpe", "MaxDD", "H1",
                "H2", "OOS_Sharpe", "dSharpe"]].to_string(index=False,
                                                          float_format=lambda x: f"{x:.4f}"))
    else:
        log("\n  4a passes: NONE anywhere on the ladder.")
    log(f"\n  4b passes {int(gc['p4b'].sum())}; the ungated parents' own 4b at each rung "
        "(inheritance check):")
    log(cells[cells["family"] == "NOGATE"].pivot_table(
        index=["panel", "gross"], columns="rung", values="p4b",
        aggfunc="max").to_string())
    log("  4b failure modes:")
    log(gc["fail4b"].value_counts().head(10).to_string())

    log(f"\n  Rule 8: chooser over (level, w, depth) on IS <= {IS_END} Sharpe, OOS {OOS_START}+ "
        f"read once, g={G_HEAD}.  {len(wf)} picks (3 panels x 3 families x 2 cadences x "
        f"{len(RUNGS)} rungs).")
    log(wf.groupby("rung").agg(
        n=("vs_nogate", "size"),
        beat_nogate=("vs_nogate", lambda s: int((s > 0).sum())),
        mean_vs_nogate=("vs_nogate", "mean"),
        OOS_twin_win=("OOS_win", "mean"),
        pass4b=("p4b", "sum"), pass4a=("p4a", "sum"),
        regret=("regret", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))
    wf["beat_spy"] = wf["OOS_Sharpe"] > wf["spy_OOS"]
    wf["beat_v2"] = wf["OOS_Sharpe"] > wf["v2_OOS"]
    log("\n  by family x rung, share of picks whose OOS Sharpe beats their own ungated parent:")
    log(wf.pivot_table(index="family", columns="rung", values="vs_nogate",
                       aggfunc=lambda s: float((s > 0).mean())).to_string(
        float_format=lambda x: f"{x:.3f}"))
    log("\n  and the OOS twin win (does the pick beat its OWN matched-gross twin out of sample):")
    log(wf.pivot_table(index="family", columns="rung", values="OOS_win",
                       aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))
    log(f"\n  picks beating SPY OOS {int(wf['beat_spy'].sum())} of {len(wf)}; beating RULES v2 "
        f"OOS {int(wf['beat_v2'].sum())}; mean regret {wf['regret'].mean():.4f}; "
        f"4b passes {int(wf['p4b'].sum())}, 4a {int(wf['p4a'].sum())}")
    log("\n  does the PICK ITSELF change with cost?  (per panel x family x cadence: how many "
        "distinct arms are picked across the 15 rungs)")
    pk = wf.groupby(["panel", "family", "cadence"])["pick"].nunique()
    log(f"    distinct picks per chooser: median {pk.median():.1f}, max {pk.max()}, "
        f"unchanged across the whole ladder in {int((pk == 1).sum())} of {len(pk)} choosers")
    if int(wf["p4b"].sum()):
        log("\n  every rule-8 pick clearing 4b:")
        log(wf[wf["p4b"]][["panel", "rung", "family", "cadence", "pick", "OOS_Sharpe",
                           "OOS_CAGR", "OOS_MaxDD", "vs_nogate", "OOS_dSharpe",
                           "p4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- rule 8 on the CLAIM itself
    log("\n  Rule 8 on the CLAIM: the cost -> win relation fitted on IS Sharpes only, then read "
        "once on OOS.")
    cl = gc.copy()
    cl["win_IS"] = cl["dIS"] > TIE
    cl["win_OOS"] = cl["dOOS"] > TIE
    tab = cl.groupby(["family", "rung"])[["win_IS", "win_OOS"]].mean().unstack()
    log(tab.to_string(float_format=lambda x: f"{x:.3f}"))
    claim = []
    for grp, sub in list(cl.groupby("family")) + [("POOLED", cl)]:
        vi = sub.groupby("rung")["win_IS"].mean()
        vo = sub.groupby("rung")["win_OOS"].mean()
        claim.append(dict(group=grp, n=len(sub), rho_IS=spearman(vi.index.values, vi.values),
                          rho_OOS=spearman(vo.index.values, vo.values),
                          span_IS=vi[C0] - vi[CTOP], span_OOS=vo[C0] - vo[CTOP],
                          win_IS_10=vi[RUNG_HEAD], win_OOS_10=vo[RUNG_HEAD],
                          label_agree=float((sub["win_IS"] == sub["win_OOS"]).mean())))
    claim = pd.DataFrame(claim)
    log(claim.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    log("  the IS-fitted family ORDERING applied unchanged to OOS:")
    oi = cl[cl["rung"] == RUNG_HEAD].groupby("family")["win_IS"].mean().rank()
    oo = cl[cl["rung"] == RUNG_HEAD].groupby("family")["win_OOS"].mean().rank()
    log(f"    IS order {oi.to_dict()}  OOS order {oo.to_dict()}  rho "
        f"{spearman(oi.values, oo.values):+.3f}")

    # =============================================================== [6] write-out
    cells.to_csv(OUT / f"{STEM}.cells.csv.gz", index=False, compression="gzip")
    drag.to_csv(OUT / f"{STEM}.drag.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    lad.to_csv(OUT / f"{STEM}.ladder.csv")
    ordering.to_csv(OUT / f"{STEM}.ordering.csv", index=False)
    claim.to_csv(OUT / f"{STEM}.claim.csv", index=False)
    stab.to_csv(OUT / f"{STEM}.stability.csv", index=False)
    cc.to_csv(OUT / f"{STEM}.cadence.csv", index=False)
    if len(g3):
        g3.to_csv(OUT / f"{STEM}.g3.csv.gz", index=False, compression="gzip")

    log("\n" + "=" * 185)
    log("[6] SUMMARY")
    log(f"  gates: G1 {g1:.2e} | G2 {g2:.2e} | G3 {g3max:.2e} | G4 "
        f"{'PASS' if ok84 else 'FAIL'} | G5 {g5:.2e}")
    log(f"  Q1 ladder monotone-down (pre-registered): {'CONFIRMED' if q1_pass else 'FAILS'}  "
        f"(pooled {lad.loc['POOLED',C0]:.3f} @0 -> {lad.loc['POOLED',RUNG_HEAD]:.3f} @10 -> "
        f"{lad.loc['POOLED',CTOP]:.3f} @100 bps)")
    log(f"  Q2 ordering: spread at 0 bps {spread0:.4f} (leg a {'TRUE' if leg_a else 'FALSE'}), "
        f"min rho vs the 0-bps order {ordering['rho_vs_c0'].min():+.3f} "
        f"(leg b {'TRUE' if leg_b else 'FALSE'}) -> the ordering is"
        f"{'' if (leg_a or leg_b) else ' NOT'} a switching-cost ranking")
    log(f"  Q3 median tax/|drag| {drag['tax_share'].median():+.3f}; within-switch-tax-bucket "
        f"family gap median {suf['max_gap'].median():.3f}; median c* "
        f"{drag['cstar'].replace(np.inf, np.nan).median():.1f} bps")
    log(f"  Q4 cadence: D switches {cc[cc['cadence']=='D']['switch_yr'].median():.1f}/yr vs W "
        f"{cc[cc['cadence']=='W']['switch_yr'].median():.1f}/yr; decay 0->100 bps D "
        f"{cc[cc['cadence']=='D']['decay_0_100'].median():+.3f} vs W "
        f"{cc[cc['cadence']=='W']['decay_0_100'].median():+.3f}")
    log(f"  Q5 4a {int(gc['p4a'].sum())} / 4b {int(gc['p4b'].sum())} of {len(gc)}; rule-8 picks "
        f"beating RULES v2 OOS {int(wf['beat_v2'].sum())} of {len(wf)}, 4b {int(wf['p4b'].sum())}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
