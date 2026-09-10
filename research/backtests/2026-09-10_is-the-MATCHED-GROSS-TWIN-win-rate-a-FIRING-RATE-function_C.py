#!/usr/bin/env python3
"""Idea 602 - "is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function" (lane C).

The finding this run exists to price
-----------------------------------
Idea 399 reported that a rolling breadth quantile (QROLL) beats its MATCHED-MEAN-GROSS STATIC
TWIN in 208 of 216 cells while idea 336's expanding quantile (QEXP) manages only 31 of 54, "on
the same book and the same bar, the only difference being the realised firing rate", and drew
from it the conclusion that "a gate that actually fires is NOT merely a gross dial in a timing
costume".  The queue's question is whether that twin win rate is a MONOTONE FUNCTION OF THE
REALISED RATE across all three families - which would make every "a gate is only a gross dial"
claim in the record rate-conditional rather than family-conditional.

Read literally, idea 399's contrast is confounded three ways and this run separates them:
  (i)  QROLL and QEXP differ in rate, but QROLL also has 4x the arms and a second dial (w);
  (ii) ABS - idea 42's absolute cut, the family with the HIGHEST rates on every panel - was
       never given a twin at all, so "all three families" has never been measured;
  (iii) the twin's gross was ROUNDED TO 2dp to cache it, and dSharpe is a small number.
And, crucially, the twin test has never been run against a NULL: a gate that fires at the same
rate with the same clustering and NO information.  If a rate-matched placebo also beats its own
twin more often as its rate rises, the monotone relation is a property of the COMPARISON, not
evidence of timing, and the record's twin leg needs a placebo column.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (MONOTONE)    Is the matched-gross twin win rate monotone increasing in the realised
                     firing rate, within EACH of ABS / QEXP / QROLL and pooled?  Pre-registered
                     bar: every adjacent equal-count bucket step non-decreasing AND per-family
                     Spearman(bucket, win rate) >= +0.80, at EVERY bucket count K.
    Q2 (SUFFICIENCY) At MATCHED rate, is there any family effect left?  If rate is the whole
                     story the within-bucket family gap should vanish.  Reported as the max
                     between-family win-rate gap inside each bucket, with cell counts.
    Q3 (CONFOUNDER)  Does rate order the win label better than the two things it is entangled
                     with - the mean GROSS GAP (1 - mean multiplier = rate x depth, the
                     amplitude idea 591 found IS the record's clause label) and depth itself?
                     AUC for each, per family and pooled.  If gap wins, the finding is about
                     amplitude, not rate, and the queue's wording is wrong.
    Q4 (PLACEBO)     Do RATE-MATCHED, INFORMATION-FREE gates beat their own twins at the same
                     rate?  Two nulls at the identical g_eff and therefore the identical twin:
                     RAND (iid days, exact matched count) and BLOCK (circular shift of the real
                     multiplier - exact rate, exact run-length distribution, zero information).
                     This is the control that decides whether Q1's curve means anything.
    Q5 (RULE 8)      Both PROTOCOL KEEP paths on every grid point, plus the rule-8 chooser over
                     (level, depth) per panel x family x cadence x rung; and the CLAIM's own
                     out-of-sample test - fit the rate -> win-rate curve on IS only and read it
                     once on 2017+.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. rate bucket   K equal-count buckets of the realised firing rate, K in {3, 4, 5, 6, 8},
                     plus an equal-WIDTH reading at each K as a second unit (idea 590's point).
    2. depth         cut depth in {0.25, 0.50, 1.00} (idea 42/336/399's own three values).
    ALL grid points reported at every panel / family / level / cadence / gross / cost rung.

Reported axes, NEVER tuned or selected on
    family   ABS(B in 0.30/0.40/0.50) / QEXP(q) / QROLL(q, w)   - all three, inherited verbatim
    q        0.07 / 0.12 / 0.17      w  252 / 504 / 1008 / 2016
    panel    U56 / B136 / SMALL439   gross 0.75 / 1.00   cadence D / W   cost 0 / 10 / 25 bps

Because on_share (the fraction of days the book is de-grossed) is a function of family x level x
w x cadence ONLY and NOT of depth, rate and depth are ORTHOGONAL by construction here, which is
what makes Q3 a clean test rather than a re-parameterisation.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.
    G3  idea 399's COMMITTED .matched.csv, all 270 rows, re-run under its own 2dp convention and
        differenced on gate_Sharpe / static_Sharpe / dSharpe / dOOS / dMaxDD.
    G4  twin interpolation: the 0.01 gross cache interpolated to an exact g vs a true
        engine.backtest at that exact g, 6 off-grid values per panel.
    G5  placebo matching identity: RAND and BLOCK reproduce the real arm's on_share and
        mean multiplier to 0 (exact by construction), so they share its twin exactly.

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
current-constituent lists, so CAGR and drawdown LEVELS are optimistic; the gate-vs-twin CONTRAST
and the placebo differencing are the durable part.  SMALL439 starts 2010-01-04 (its halves are
not U56/B136's calendar halves) and w=2016 spends half its sample unarmed.

Deterministic (all placebo seeds fixed), standalone.  Reads baseline.py and engine; modifies
nothing.
"""
import hashlib
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
PARENT_MATCHED = OUT / "2026-09-10_does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate_cloud.matched.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]          # tuned param 2
KS = [3, 4, 5, 6, 8]                 # tuned param 1
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12                          # ideas 594/595: a tie is not a win
NSEED = 10
GSTEP = 0.01

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/336/399)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


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


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path, with idea 399's switch cost."""
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


def apply_gate(r_base, mult, gross, cost_bps):
    """idea 399 verbatim: multiplier decided at t, applied at t+1, switch cost on |dm|."""
    return apply_eff(r_base, mult.reindex(r_base.index).shift(1).fillna(1.0), gross, cost_bps)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def tests_4b(r, spy_pack):
    s1, s2, s_oos, s_dd, s_cagr = spy_pack
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def verdict_4a(r, base_pack):
    b1, b2, bdd = base_pack
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def summarise(r, spy_pack, base_pack):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy_pack)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=m_is["Sharpe"], OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
                OOS_MaxDD=m_oos["MaxDD"], p4a=verdict_4a(r, base_pack), p4b=all(t.values()),
                fail4b=",".join([k for k, v in t.items() if not v]) or "-")


def auc(score_v, label):
    """Rank AUC with exact tie handling; nan when a class is empty."""
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
    a, b = pd.Series(a), pd.Series(b)
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ---------------------------------------------------------------- twin machinery
class Twins:
    """Static-gross EWALL twin returns.  Exact g by linear interpolation on a GSTEP cache;
    G4 prices the interpolation error against true backtests at off-grid g."""

    def __init__(self, px, start):
        self.px, self.start = px, start
        self.cache = {}
        self.n_bt = 0

    def _grid(self, g):
        return round(round(g / GSTEP) * GSTEP, 6)

    def _exact(self, g):
        g = round(g, 6)
        if g not in self.cache:
            res = backtest(self.px, ewall_weights(self.px, g), cost_bps=0, freq=FREQ)
            self.cache[g] = (res["returns"].loc[self.start:], res["turnover"].loc[self.start:])
            self.n_bt += 1
        return self.cache[g]

    def prewarm(self, gs):
        need = set()
        for g in gs:
            lo = np.floor(g / GSTEP) * GSTEP
            need.add(round(lo, 6))
            need.add(round(lo + GSTEP, 6))
        for g in sorted(need):
            self._exact(g)

    def at(self, g, cost_bps):
        """Interpolated exact-g twin returns at the requested cost rung."""
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        hi = round(lo + GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            r0, t0 = self._exact(lo)
        else:
            rl, tl = self._exact(lo)
            rh, th = self._exact(hi)
            r0, t0 = (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th
        return r0 - t0 * cost_bps / 1e4


# ---------------------------------------------------------------- placebo multipliers
def seed_of(*parts):
    """Deterministic seed (Python's str hash is randomised per process; md5 is not)."""
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_mults(m_eff, depth, kind, seed):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff.

    RAND  : iid days, EXACTLY the same number of de-grossed days.
    BLOCK : circular shift of m_eff - exact rate AND exact run-length distribution.
    Both preserve mean(m_eff) exactly, so they share the real arm's twin exactly (G5).
    """
    v = m_eff.values
    k = int((v < 1.0).sum())
    if k == 0:
        return m_eff.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(len(v))
        out[rng.choice(len(v), size=k, replace=False)] = 1.0 - depth
        return pd.Series(out, index=m_eff.index)
    shift = int(rng.integers(1, len(v)))
    return pd.Series(np.roll(v, shift), index=m_eff.index)


# ---------------------------------------------------------------- per-panel run
def run_panel(panel, px):
    start = px.index[260]
    idx = px.index
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    s1, s2 = half_sharpes(spy)
    spy_pack = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])

    br_full = breadth(px)
    br = br_full.loc[start:]
    log(f"\n{'='*180}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(br)} days)")
    log(f"  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}; 4b bars: CAGR floor "
        f"{0.70*ms['CAGR']:.2%}, DD cap {-0.60*abs(ms['MaxDD']):.2%}, halves {s1:.3f}/{s2:.3f}, "
        f"OOS {spy_pack[2]:.3f}")

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}

    # ---- base books at 0 bps, all rungs derived (G1)
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    rv2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    rv1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)

    def rung(pair, c):
        r, t = pair
        return r - t * c / 1e4

    refs = {c: dict(v2=rung((rv2["returns"].loc[start:], rv2["turnover"].loc[start:]), c),
                    v1=rung((rv1["returns"].loc[start:], rv1["turnover"].loc[start:]), c),
                    SPY=spy) for c in RUNGS}
    base_packs = {}
    for c in RUNGS:
        b = refs[c]["v2"]
        b1, b2 = half_sharpes(b)
        base_packs[c] = (b1, b2, metrics(b)["MaxDD"])

    # ---- arms: (family, level, w) -> threshold-based multiplier per depth x cadence
    arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
            + [("QROLL", q, w) for q in QS for w in WS])
    mult, rate_inst = {}, {}
    for fam, lev, w in arms:
        if fam == "ABS":
            thr = None
            rate_inst[(fam, lev, w)] = float((br < lev).mean())
        else:
            thr = thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)]
            t = thr.loc[start:]
            rate_inst[(fam, lev, w)] = float((br < t).mean())
        for d, cad in product(DEPTHS, CADENCES):
            m = (gate_abs(br_full, lev, d, cad, idx) if fam == "ABS"
                 else gate_from_thr(br_full, thr, d, cad, idx))
            mult[(fam, lev, w, d, cad)] = m.loc[start:]

    # ---- twins: prewarm the gross cache from the exact g_eff values we will need
    tw = Twins(px, start)
    needed = []
    m_eff_cache, on_cache, gap_cache = {}, {}, {}
    for (fam, lev, w), (d, cad), g in product(arms, product(DEPTHS, CADENCES), GROSSES):
        m = mult[(fam, lev, w, d, cad)]
        me = m.reindex(base0[g][0].index).shift(1).fillna(1.0)
        m_eff_cache[(fam, lev, w, d, cad)] = me
        on_cache[(fam, lev, w, d, cad)] = float((me < 1.0).mean())
        gap_cache[(fam, lev, w, d, cad)] = 1.0 - float(me.mean())
        needed.append(g * float(me.mean()))
    tw.prewarm(needed)
    log(f"  twin gross cache: {tw.n_bt} backtests on a {GSTEP} grid spanning "
        f"{min(tw.cache):.2f}-{max(tw.cache):.2f}")

    # ---- the grid + the twin comparison ------------------------------------------------
    cells, ph = [], []
    for c in RUNGS:
        for nm, r in refs[c].items():
            cells.append(dict(panel=panel, rung=c, gross=np.nan, family="ref", arm=nm,
                              level=np.nan, w=np.nan, depth=np.nan, cadence="-",
                              rate_inst=np.nan, on_share=np.nan, gap=np.nan, g_eff=np.nan,
                              twin_Sharpe=np.nan, dSharpe=np.nan, dOOS=np.nan, dCAGR=np.nan,
                              dMaxDD=np.nan, win=False, tie=False,
                              **summarise(r, spy_pack, base_packs[c])))
        for g in GROSSES:
            rb = rung(base0[g], c)
            cells.append(dict(panel=panel, rung=c, gross=g, family="NOGATE",
                              arm=f"NOGATE g{g:.2f}", level=np.nan, w=np.nan, depth=0.0,
                              cadence="-", rate_inst=0.0, on_share=0.0, gap=0.0, g_eff=g,
                              twin_Sharpe=np.nan, dSharpe=np.nan, dOOS=np.nan, dCAGR=np.nan,
                              dMaxDD=np.nan, win=False, tie=False,
                              **summarise(rb, spy_pack, base_packs[c])))
            for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
                key = (fam, lev, w, d, cad)
                rg, me = apply_gate(rb, mult[key], g, c)
                g_eff = g * float(me.mean())
                rs = tw.at(g_eff, c)
                mg, mst = metrics(rg), metrics(rs)
                og = metrics(rg.loc[OOS_START:])["Sharpe"]
                os_ = metrics(rs.loc[OOS_START:])["Sharpe"]
                dsh = mg["Sharpe"] - mst["Sharpe"]
                cells.append(dict(
                    panel=panel, rung=c, gross=g, family=fam,
                    arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}", level=lev, w=w,
                    depth=d, cadence=cad, rate_inst=rate_inst[(fam, lev, w)],
                    on_share=on_cache[key], gap=gap_cache[key], g_eff=g_eff,
                    twin_Sharpe=mst["Sharpe"], dSharpe=dsh, dOOS=og - os_,
                    dCAGR=mg["CAGR"] - mst["CAGR"],
                    dMaxDD=abs(mst["MaxDD"]) - abs(mg["MaxDD"]),
                    win=bool(dsh > TIE), tie=bool(abs(dsh) <= TIE),
                    **summarise(rg, spy_pack, base_packs[c])))

                # ---- Q4 placebos, headline rung only, same g_eff => same twin (G5)
                if c == RUNG_HEAD:
                    for kind in ("RAND", "BLOCK"):
                        for s in range(NSEED):
                            pm = placebo_mults(me, d, kind,
                                               seed_of(panel, fam, lev, w, d, cad, g, kind, s))
                            rp, mep = apply_eff(rb, pm, g, c)
                            gp = g * float(mep.mean())
                            rsp = tw.at(gp, c) if abs(gp - g_eff) > 1e-9 else rs
                            mp, msp = metrics(rp), metrics(rsp)
                            dp = mp["Sharpe"] - msp["Sharpe"]
                            ph.append(dict(panel=panel, kind=kind, seed=s, family=fam,
                                           level=lev, w=w, depth=d, cadence=cad, gross=g,
                                           on_share=float((mep < 1.0).mean()),
                                           gap=1.0 - float(mep.mean()), g_eff=gp,
                                           real_on=on_cache[key], real_gap=gap_cache[key],
                                           real_g_eff=g_eff, dSharpe=dp,
                                           dOOS=metrics(rp.loc[OOS_START:])["Sharpe"]
                                                - metrics(rsp.loc[OOS_START:])["Sharpe"],
                                           win=bool(dp > TIE), tie=bool(abs(dp) <= TIE)))

    # ---- rule 8 book leg ---------------------------------------------------------------
    wf = []
    for c in RUNGS:
        rbc = rung(base0[G_HEAD], c)
        nog = metrics(rbc.loc[OOS_START:])
        for fam in ("ABS", "QEXP", "QROLL"):
            fam_arms = [a for a in arms if a[0] == fam]
            for cad in CADENCES:
                cellmap = {}
                for (f, lev, w), d in product(fam_arms, DEPTHS):
                    cellmap[(lev, w, d)] = apply_gate(rbc, mult[(f, lev, w, d, cad)], G_HEAD, c)[0]
                is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cellmap.items()}
                oos = {k: metrics(v.loc[OOS_START:]) for k, v in cellmap.items()}
                pick = min(is_s, key=lambda k: (-is_s[k], k[0], k[1], k[2]))
                best = max(oos, key=lambda k: oos[k]["Sharpe"])
                pk = (fam, pick[0], pick[1], pick[2], cad)
                wf.append(dict(panel=panel, family=fam, rung=c, cadence=cad,
                               pick_level=pick[0], pick_w=pick[1], pick_depth=pick[2],
                               pick_on_share=on_cache[pk], pick_gap=gap_cache[pk],
                               n_cells=len(cellmap), IS_Sharpe=is_s[pick],
                               OOS_CAGR=oos[pick]["CAGR"], OOS_Sharpe=oos[pick]["Sharpe"],
                               OOS_MaxDD=oos[pick]["MaxDD"],
                               nogate_OOS_Sharpe=nog["Sharpe"], nogate_OOS_CAGR=nog["CAGR"],
                               nogate_OOS_MaxDD=nog["MaxDD"],
                               vs_nogate=oos[pick]["Sharpe"] - nog["Sharpe"],
                               grid_mean_OOS=float(np.mean([oos[k]["Sharpe"] for k in oos])),
                               best_OOS=oos[best]["Sharpe"],
                               regret=oos[pick]["Sharpe"] - oos[best]["Sharpe"],
                               spy_OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                               v2_OOS=metrics(refs[c]["v2"].loc[OOS_START:])["Sharpe"]))

    # ---- rule 8 claim leg: the win label measured on IS only and on OOS only -----------
    claim = []
    for g in GROSSES:
        rb = rung(base0[g], RUNG_HEAD)
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            key = (fam, lev, w, d, cad)
            rg, me = apply_gate(rb, mult[key], g, RUNG_HEAD)
            g_eff = g * float(me.mean())
            rs = tw.at(g_eff, RUNG_HEAD)
            row = dict(panel=panel, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g)
            for tag, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
                rgi, rsi, mei = rg.loc[sl], rs.loc[sl], me.loc[sl]
                dsh = metrics(rgi)["Sharpe"] - metrics(rsi)["Sharpe"]
                row[f"on_share_{tag}"] = float((mei < 1.0).mean())
                row[f"gap_{tag}"] = 1.0 - float(mei.mean())
                row[f"dSharpe_{tag}"] = dsh
                row[f"win_{tag}"] = bool(dsh > TIE)
            claim.append(row)

    return (pd.DataFrame(cells), pd.DataFrame(ph), pd.DataFrame(wf), pd.DataFrame(claim),
            tw, base0, start, spy_pack, base_packs, refs, mult, on_cache, gap_cache, arms)


# ---------------------------------------------------------------- analysis helpers
def bucket(series, K, scheme):
    s = pd.Series(series).astype(float)
    if scheme == "count":
        try:
            b = pd.qcut(s.rank(method="first"), K, labels=False)
        except ValueError:
            return pd.Series(np.nan, index=s.index)
        return b
    lo, hi = s.min(), s.max()
    if not np.isfinite(lo) or hi <= lo:
        return pd.Series(np.nan, index=s.index)
    edges = np.linspace(lo, hi, K + 1)
    edges[-1] += 1e-12
    return pd.Series(np.digitize(s, edges[1:-1]), index=s.index)


def curve_table(df, K, scheme, by="family", ratecol="on_share", within=False):
    """within=False: buckets cut on the POOLED population (families compared on one ruler).
    within=True : buckets cut INSIDE each family (each family gets its own K rungs)."""
    d = df.copy()
    if within:
        d["bk"] = np.nan
        for grp, sub in d.groupby(by):
            d.loc[sub.index, "bk"] = bucket(sub[ratecol], K, scheme).values
    else:
        d["bk"] = bucket(d[ratecol], K, scheme).values
    d = d.dropna(subset=["bk"])
    rows = []
    groups = [(g, s) for g, s in d.groupby(by)]
    if not within:
        groups.append(("POOLED", d))
    for grp, gsub in groups:
        for bk, sub in gsub.groupby("bk"):
            rows.append(dict(K=K, scheme=scheme, within=within, group=grp, bk=int(bk),
                             n=len(sub), rate_lo=sub[ratecol].min(),
                             rate_mid=sub[ratecol].median(), rate_hi=sub[ratecol].max(),
                             winrate=float(sub["win"].mean()),
                             med_dSharpe=float(sub["dSharpe"].median()),
                             ties=int(sub["tie"].sum())))
    return pd.DataFrame(rows)


def monotone_report(cur):
    out = []
    for (K, scheme, within, grp), sub in cur.groupby(["K", "scheme", "within", "group"]):
        sub = sub.sort_values("bk")
        wr = sub["winrate"].values
        steps = np.diff(wr)
        out.append(dict(K=K, scheme=scheme, within=within, group=grp, nbk=len(sub),
                        n=int(sub["n"].sum()), wr_first=wr[0], wr_last=wr[-1],
                        span=wr[-1] - wr[0], up_steps=int((steps > 0).sum()),
                        down_steps=int((steps < 0).sum()),
                        min_step=float(steps.min()) if len(steps) else np.nan,
                        monotone_up=bool((steps >= 0).all()) and len(sub) == K,
                        resolvable=bool(len(sub) == K),
                        rho=spearman(sub["bk"], sub["winrate"])))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    log("=" * 180)
    log(f"Idea 602 is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function (lane C) | {SCRIPT}")
    log("=" * 180)
    log("Base book (fixed, idea 28/42/336/399's): EWALL(G) = equal weight every name above its")
    log("  own 200d MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is BELOW the threshold.")
    log("  ABS(B)      breadth_t < B                            (idea 42)")
    log("  QEXP(q)     breadth_t < causal EXPANDING q-quantile  (idea 336)")
    log("  QROLL(q,w)  breadth_t < trailing-w-day q-quantile    (idea 399)")
    log("Comparand for EVERY arm: the MATCHED-MEAN-GROSS STATIC TWIN, i.e. EWALL at the constant")
    log("  gross g_eff = gross * mean(multiplier) - the same average exposure, no timing at all.")
    log(f"Tuned (2): rate-bucket count K in {KS} (x count/width unit) and depth in {DEPTHS}.")
    log(f"Reported never tuned: family, level, w {WS}, panel, gross {GROSSES}, cadence {CADENCES},")
    log(f"  cost {RUNGS} bps.  Tie bar |dSharpe| <= {TIE:g} (ideas 594/595): a tie is NOT a win.")
    log(f"Placebos: {NSEED} seeds x RAND (iid, exact matched day count) and BLOCK (circular shift,")
    log("  exact rate AND exact run lengths).  Both share the real arm's twin exactly.")

    # =================================================================== [0] gates
    log("\n" + "=" * 180)
    log("[0] REPRODUCTION GATES (all printed before any new number is read)")
    px0 = load_universe()
    st0 = px0.index[260]

    # G1 cost-rung identity
    res0 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=0, freq=FREQ)
    g1 = 0.0
    for c in (10, 25):
        live = backtest(px0, ewall_weights(px0, 0.75), cost_bps=c, freq=FREQ)["returns"].loc[st0:]
        der = (res0["returns"] - res0["turnover"] * c / 1e4).loc[st0:]
        g1 = max(g1, float((live - der).abs().max()))
    log(f"  G1 cost-rung identity r(c) = r(0) - turnover*c/1e4: max |live - derived| = {g1:.3e} "
        f"(bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    # G2 idea 84 EWALL U56 g=0.85 @10bps
    r84 = backtest(px0, ewall_weights(px0, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[st0:]
    m84 = metrics(r84)
    h84 = half_sharpes(r84)
    ok84 = (abs(m84["CAGR"] - 0.118) < 0.004 and abs(m84["Sharpe"] - 1.05) < 0.04
            and abs(abs(m84["MaxDD"]) - 0.179) < 0.006)
    log(f"  G2 idea 84 EWALL U56 g=0.85 @10bps: {m84['CAGR']:.3%} / {m84['Sharpe']:.3f} / "
        f"{m84['MaxDD']:.3%} / H {h84[0]:.3f} / {h84[1]:.3f}   "
        f"(published 11.8% / 1.05 / -17.9% / 1.07 / 1.04) -> {'PASS' if ok84 else 'FAIL'}")

    # ================================================================ panels
    panels = [("U56", px0)]
    panels.append(("B136", load_universe(broad=True)))
    ps, ndrop = small_panel()
    panels.append(("SMALL439", ps))
    log(f"  SMALL panel: dropped {ndrop} names with max_1d_move >= 1.0 -> {ps.shape[1]-1} names "
        f"+ SPY (idea 399's construction, so its rows join)")

    CELLS, PH, WF, CLAIM, G4, G5 = [], [], [], [], [], []
    for name, px in panels:
        (cells, ph, wf, claim, tw, base0, start, spy_pack, base_packs, refs,
         mult, on_cache, gap_cache, arms) = run_panel(name, px)
        CELLS.append(cells)
        PH.append(ph)
        WF.append(wf)
        CLAIM.append(claim)

        # G4 interpolation error: 6 off-grid g per panel vs a true backtest
        rng = np.random.default_rng(602)
        lo, hi = min(tw.cache), max(tw.cache)
        for gtest in np.round(lo + (hi - lo) * rng.random(6) , 5):
            gtest = float(gtest)
            interp = tw.at(gtest, RUNG_HEAD)
            true = backtest(px, ewall_weights(px, gtest), cost_bps=0, freq=FREQ)
            tr = (true["returns"] - true["turnover"] * RUNG_HEAD / 1e4).loc[start:]
            G4.append(dict(panel=name, g=gtest,
                           interp_Sharpe=metrics(interp)["Sharpe"],
                           true_Sharpe=metrics(tr)["Sharpe"],
                           dSharpe=metrics(interp)["Sharpe"] - metrics(tr)["Sharpe"],
                           max_abs_ret=float((interp - tr).abs().max())))

        # G5 placebo matching identity
        sub = ph[ph["gross"] == G_HEAD]
        G5.append(dict(panel=name, n=len(sub),
                       max_d_on=float((sub["on_share"] - sub["real_on"]).abs().max()),
                       max_d_gap=float((sub["gap"] - sub["real_gap"]).abs().max()),
                       max_d_geff=float((sub["g_eff"] - sub["real_g_eff"]).abs().max())))

    cells = pd.concat(CELLS, ignore_index=True)
    ph = pd.concat(PH, ignore_index=True)
    wf = pd.concat(WF, ignore_index=True)
    claim = pd.concat(CLAIM, ignore_index=True)
    g4 = pd.DataFrame(G4)
    g5 = pd.DataFrame(G5)

    log("\n  G4 twin interpolation vs a true backtest at 6 off-grid gross values per panel:")
    log(g4.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    g4ok = float(g4["dSharpe"].abs().max()) < 1e-3
    log(f"     max |dSharpe| = {g4['dSharpe'].abs().max():.3e}, max |dr| = "
        f"{g4['max_abs_ret'].abs().max():.3e} (bar 1e-3 on Sharpe) -> "
        f"{'PASS' if g4ok else 'FAIL'}")
    log("\n  G5 placebo matching identity (RAND/BLOCK share the real arm's on_share, gap, g_eff):")
    log(g5.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    g5ok = float(g5[["max_d_on", "max_d_gap", "max_d_geff"]].values.max()) < 1e-12
    log(f"     -> {'PASS (exact by construction)' if g5ok else 'FAIL'}")

    # G3: join idea 399's committed matched.csv
    log("\n  G3 idea 399's committed .matched.csv, re-run under its own 2dp twin convention:")
    if PARENT_MATCHED.exists():
        par = pd.read_csv(PARENT_MATCHED)
        # rebuild idea 399's exact convention (rung 10, gross 0.75, twin gross ROUNDED to 2dp)
        mine = []
        for name, px in panels:
            start = px.index[260]
            br_full = breadth(px)
            idx = px.index
            base = backtest(px, ewall_weights(px, G_HEAD), cost_bps=0, freq=FREQ)
            rb = (base["returns"] - base["turnover"] * RUNG_HEAD / 1e4).loc[start:]
            thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
            thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q)
                        for q in QS for w in WS}
            seen = {}
            for cad in CADENCES:
                for q in QS:
                    for w in [0] + WS:
                        fam = "QEXP" if w == 0 else "QROLL"
                        thr = thr_exp[q] if w == 0 else thr_roll[(q, w)]
                        for d in DEPTHS:
                            m = gate_from_thr(br_full, thr, d, cad, idx).loc[start:]
                            rg, me = apply_gate(rb, m, G_HEAD, RUNG_HEAD)
                            ge = round(G_HEAD * float(me.mean()), 2)
                            if ge not in seen:
                                s = backtest(px, ewall_weights(px, ge), cost_bps=RUNG_HEAD,
                                             freq=FREQ)["returns"].loc[start:]
                                seen[ge] = s
                            rs = seen[ge]
                            mg, mst = metrics(rg), metrics(rs)
                            mine.append(dict(panel=name, family=fam, q=q, w=w, depth=d,
                                             cadence=cad, g_eff=ge,
                                             gate_Sharpe=mg["Sharpe"],
                                             static_Sharpe=mst["Sharpe"],
                                             dSharpe=mg["Sharpe"] - mst["Sharpe"],
                                             dOOS=metrics(rg.loc[OOS_START:])["Sharpe"]
                                                  - metrics(rs.loc[OOS_START:])["Sharpe"],
                                             dMaxDD=abs(mst["MaxDD"]) - abs(mg["MaxDD"])))
        mine = pd.DataFrame(mine)
        keys = ["panel", "family", "q", "w", "depth", "cadence"]
        j = par.merge(mine, on=keys, suffixes=("_pub", "_mine"))
        log(f"     joined {len(j)} of {len(par)} published rows")
        gcols = ["gate_Sharpe", "static_Sharpe", "dSharpe", "dOOS", "dMaxDD"]
        for pan, sub in j.groupby("panel"):
            mx = max(float((sub[c + "_pub"] - sub[c + "_mine"]).abs().max()) for c in gcols)
            log(f"     {pan:9s} n={len(sub):3d}  max |published - mine| over "
                f"{gcols} = {mx:.3e}")
        g3max = max(float((j[c + "_pub"] - j[c + "_mine"]).abs().max()) for c in gcols)
        log(f"     overall {g3max:.3e} (U56 carries a documented price-restatement channel; "
            f"B136 should be bit-identical)")
        # idea 399's own headline counts, recomputed
        for fam, sub in mine[(mine["cadence"].isin(CADENCES))].groupby("family"):
            log(f"     idea 399 headline recomputed: {fam} wins its twin in "
                f"{int((sub['dSharpe'] > TIE).sum())} of {len(sub)} cells "
                f"(published: QROLL 208/216, QEXP 31/54)")
        mine.to_csv(OUT / f"{STEM}.g3.csv", index=False)
    else:
        log("     PARENT MATCHED CSV MISSING -> G3 CANNOT RUN")
        g3max = np.nan

    # =============================================================== [1] the population
    log("\n" + "=" * 180)
    log("[1] THE CELL POPULATION")
    gc = cells[cells["family"].isin(["ABS", "QEXP", "QROLL"])].copy()
    log(f"  {len(gc)} gated cells = 3 panels x 18 level-arms x {len(DEPTHS)} depths x "
        f"{len(CADENCES)} cadences x {len(GROSSES)} gross x {len(RUNGS)} rungs; "
        f"{len(cells) - len(gc)} reference/NOGATE rows.")
    log(f"  ties (|dSharpe| <= {TIE:g}): {int(gc['tie'].sum())} of {len(gc)}")
    log("\n  Realised firing rate (on_share = fraction of eval days the book is de-grossed, "
        "post-cadence, post-shift):")
    t = gc.groupby(["panel", "family"]).agg(n=("on_share", "size"),
                                            rate_min=("on_share", "min"),
                                            rate_med=("on_share", "median"),
                                            rate_max=("on_share", "max"),
                                            gap_med=("gap", "median"),
                                            winrate=("win", "mean"),
                                            med_dSharpe=("dSharpe", "median"))
    log(t.to_string(float_format=lambda x: f"{x:.4f}"))
    log("\n  on_share does NOT depend on depth (rate and depth are orthogonal by construction): "
        f"max spread over depths = "
        f"{gc.groupby(['panel','family','level','w','cadence'])['on_share'].apply(lambda s: s.max()-s.min()).max():.2e}")

    log("\n  Twin win rate by family x cost rung x gross (the leg idea 399 published at one rung):")
    piv = gc.pivot_table(index=["family"], columns=["rung", "gross"], values="win",
                         aggfunc="mean")
    log(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    piv_n = gc.pivot_table(index=["family"], columns=["rung", "gross"], values="win",
                           aggfunc="size")
    log("  cell counts:")
    log(piv_n.to_string())

    # =============================================================== [2] Q1 monotone
    log("\n" + "=" * 180)
    log("[2] Q1 - IS THE TWIN WIN RATE MONOTONE IN THE REALISED RATE?")
    log(f"  Primary population: the PROTOCOL rung ({RUNG_HEAD} bps), both grosses, all panels, "
        "all depths, all cadences.")
    head = gc[gc["rung"] == RUNG_HEAD].copy()
    curves, monos = [], []
    for K, scheme, within in product(KS, ("count", "width"), (False, True)):
        cur = curve_table(head, K, scheme, within=within)
        curves.append(cur)
        monos.append(monotone_report(cur))
    curves = pd.concat(curves, ignore_index=True)
    monos = pd.concat(monos, ignore_index=True)
    for within in (False, True):
        tag = "WITHIN-FAMILY" if within else "POOLED-RULER"
        for scheme in ("count", "width"):
            log(f"\n  --- {tag} / {scheme.upper()} buckets ---")
            for K in KS:
                sub = curves[(curves["K"] == K) & (curves["scheme"] == scheme)
                             & (curves["within"] == within)]
                for lab, col, fmt in (("win rate", "winrate", "{:.3f}"),
                                      ("median rate", "rate_mid", "{:.3f}"),
                                      ("n", "n", "{:.0f}")):
                    piv = sub.pivot_table(index="group", columns="bk", values=col)
                    log(f"   K={K}  {lab}:")
                    log("   " + piv.to_string(
                        float_format=lambda x, f=fmt: f.format(x)).replace("\n", "\n   "))
    log("\n  MONOTONICITY (pre-registered bar: monotone_up True AND rho >= +0.80 for ALL three "
        "families at EVERY K, both units, both rulers):")
    log(monos.sort_values(["within", "scheme", "K", "group"]).to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))
    fam_only = monos[monos["group"].isin(["ABS", "QEXP", "QROLL"])]
    res = fam_only[fam_only["resolvable"]]
    h1_pass = bool(len(res) == len(fam_only) and fam_only["monotone_up"].all()
                   and (fam_only["rho"] >= 0.80).all())
    log(f"\n  Q1 VERDICT: {len(res)} of {len(fam_only)} family x K x unit x ruler cells are even "
        f"RESOLVABLE (a family that occupies fewer than K pooled buckets cannot be read); "
        f"monotone_up in {int(fam_only['monotone_up'].sum())}; rho >= 0.80 in "
        f"{int((fam_only['rho'] >= 0.80).sum())}; "
        f"min rho {fam_only['rho'].min():.3f}, median {fam_only['rho'].median():.3f} "
        f"-> H1 {'CONFIRMED' if h1_pass else 'FAILS as pre-registered'}")
    for within in (False, True):
        f2 = fam_only[fam_only["within"] == within]
        log(f"    ruler={'within-family' if within else 'pooled':13s} resolvable "
            f"{int(f2['resolvable'].sum())}/{len(f2)}  monotone_up {int(f2['monotone_up'].sum())}"
            f"  rho>=0.80 {int((f2['rho'] >= 0.80).sum())}  median rho {f2['rho'].median():.3f}")
    log(f"  Continuous reading, no buckets: Spearman(on_share, dSharpe) and AUC(on_share -> win)")
    rows = []
    for grp, sub in head.groupby("family"):
        rows.append(dict(group=grp, n=len(sub), rho_rate_dSharpe=spearman(sub["on_share"],
                                                                         sub["dSharpe"]),
                         auc_rate=auc(sub["on_share"], sub["win"]),
                         winrate=float(sub["win"].mean())))
    rows.append(dict(group="POOLED", n=len(head),
                     rho_rate_dSharpe=spearman(head["on_share"], head["dSharpe"]),
                     auc_rate=auc(head["on_share"], head["win"]),
                     winrate=float(head["win"].mean())))
    cont = pd.DataFrame(rows)
    log(cont.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # =============================================================== [3] Q2 sufficiency
    log("\n" + "=" * 180)
    log("[3] Q2 - AT MATCHED RATE, IS THERE ANY FAMILY EFFECT LEFT?")
    suff = []
    for K, scheme in product(KS, ("count", "width")):
        d = head.copy()
        d["bk"] = bucket(d["on_share"], K, scheme)
        for bk, sub in d.dropna(subset=["bk"]).groupby("bk"):
            per = sub.groupby("family")["win"].agg(["size", "mean"])
            per = per[per["size"] >= 8]
            if len(per) >= 2:
                suff.append(dict(K=K, scheme=scheme, bk=int(bk), n=len(sub),
                                 families=len(per), max_gap=float(per["mean"].max()
                                                                  - per["mean"].min()),
                                 detail="; ".join(f"{i}:{r['mean']:.2f}(n{int(r['size'])})"
                                                  for i, r in per.iterrows()),
                                 rate_lo=sub["on_share"].min(), rate_hi=sub["on_share"].max()))
    suff = pd.DataFrame(suff)
    if len(suff):
        log(suff.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        log(f"\n  Within-bucket between-family win-rate gap: median {suff['max_gap'].median():.3f}, "
            f"max {suff['max_gap'].max():.3f} over {len(suff)} comparable buckets "
            f"(a rate-sufficient story wants these near 0).")
    else:
        log("  no bucket carries two families with n >= 8 -> the families do not overlap in rate")

    # =============================================================== [4] Q3 confounder
    log("\n" + "=" * 180)
    log("[4] Q3 - RATE, OR THE MEAN GROSS GAP (rate x depth), OR DEPTH?")
    preds = ["on_share", "gap", "depth", "rate_inst", "g_eff"]
    rows = []
    for grp, sub in list(head.groupby("family")) + [("POOLED", head)]:
        r = dict(group=grp, n=len(sub), winrate=float(sub["win"].mean()))
        for p in preds:
            r[f"auc_{p}"] = auc(sub[p], sub["win"])
            r[f"rho_{p}"] = spearman(sub[p], sub["dSharpe"])
        rows.append(r)
    conf = pd.DataFrame(rows)
    log(conf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log("\n  Win rate on the depth x rate-bucket cross (K=4 equal-count), pooled over families:")
    d = head.copy()
    d["bk"] = bucket(d["on_share"], 4, "count")
    log(d.pivot_table(index="depth", columns="bk", values="win",
                      aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))
    log("  n:")
    log(d.pivot_table(index="depth", columns="bk", values="win",
                      aggfunc="size").to_string())

    # =============================================================== [5] Q4 placebo
    log("\n" + "=" * 180)
    log("[5] Q4 - THE RATE-MATCHED, INFORMATION-FREE PLACEBO")
    log(f"  {len(ph)} placebo cells ({NSEED} seeds x 2 kinds x 18 arms x {len(DEPTHS)} depths x "
        f"{len(CADENCES)} cadences x {len(GROSSES)} gross x 3 panels) at {RUNG_HEAD} bps.")
    log(f"  ties: {int(ph['tie'].sum())}")
    log("\n  Placebo win rate vs the real arms', by family:")
    a = ph.groupby(["kind", "family"])["win"].agg(["size", "mean"]).rename(
        columns={"mean": "winrate"})
    log(a.to_string(float_format=lambda x: f"{x:.4f}"))
    log("\n  REAL (same rung, both gross):")
    log(head.groupby("family")["win"].agg(["size", "mean"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    log("\n  Win rate by rate bucket (K=5 equal-count on on_share), REAL vs RAND vs BLOCK:")
    pop = pd.concat([
        head.assign(kind="REAL")[["kind", "family", "on_share", "gap", "win", "tie", "dSharpe"]],
        ph[["kind", "family", "on_share", "gap", "win", "tie", "dSharpe"]]], ignore_index=True)
    pop["bk"] = bucket(pop["on_share"], 5, "count")
    log(pop.pivot_table(index="kind", columns="bk", values="win",
                        aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))
    log("  bucket median rate:")
    log(pop.pivot_table(index="kind", columns="bk", values="on_share",
                        aggfunc="median").to_string(float_format=lambda x: f"{x:.3f}"))
    log("  n:")
    log(pop.pivot_table(index="kind", columns="bk", values="win", aggfunc="size").to_string())
    log("\n  Placebo monotonicity at every K (equal-count), pooled over families:")
    prow = []
    for K in KS:
        for kind, sub in pop.groupby("kind"):
            s = sub.copy()
            s["bk"] = bucket(s["on_share"], K, "count")
            s = s.dropna(subset=["bk"])
            wr = s.groupby("bk")["win"].mean().sort_index().values
            st = np.diff(wr)
            prow.append(dict(K=K, kind=kind, n=len(s), wr_first=wr[0], wr_last=wr[-1],
                             span=wr[-1] - wr[0], monotone_up=bool((st >= 0).all()),
                             rho=spearman(range(len(wr)), wr)))
    prow = pd.DataFrame(prow)
    log(prow.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\n  EXCESS of the real arm over its OWN rate/depth/gross/panel-matched placebo mean:")
    key = ["panel", "family", "level", "w", "depth", "cadence", "gross"]
    pm = ph.groupby(key + ["kind"])["dSharpe"].mean().unstack("kind")
    hh = head.set_index(key)["dSharpe"]
    ex = pm.join(hh.rename("REAL"))
    ex["excess_vs_RAND"] = ex["REAL"] - ex["RAND"]
    ex["excess_vs_BLOCK"] = ex["REAL"] - ex["BLOCK"]
    ex = ex.reset_index()
    log(ex.groupby("family")[["REAL", "RAND", "BLOCK", "excess_vs_RAND",
                              "excess_vs_BLOCK"]].median().to_string(
        float_format=lambda x: f"{x:+.4f}"))
    log("  share of arms whose REAL dSharpe beats its own placebo mean:")
    log(ex.groupby("family").apply(
        lambda s: pd.Series({"vs_RAND": float((s["excess_vs_RAND"] > 0).mean()),
                             "vs_BLOCK": float((s["excess_vs_BLOCK"] > 0).mean()),
                             "n": len(s)})).to_string(float_format=lambda x: f"{x:.3f}"))
    log("\n  Excess vs BLOCK by rate bucket (K=5 equal-count) - is the EXCESS rate-dependent?")
    exj = ex.merge(head[key + ["on_share"]].drop_duplicates(subset=key), on=key, how="left")
    exj["bk"] = bucket(exj["on_share"], 5, "count")
    log(exj.pivot_table(index="family", columns="bk", values="excess_vs_BLOCK",
                        aggfunc="median").to_string(float_format=lambda x: f"{x:+.4f}"))
    log("  share > 0:")
    log(exj.assign(pos=exj["excess_vs_BLOCK"] > 0).pivot_table(
        index="family", columns="bk", values="pos",
        aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))

    # =============================================================== [6] Q5 rule 8
    log("\n" + "=" * 180)
    log("[6] Q5 - PROTOCOL KEEP PATHS AND RULE 8")
    log(f"  4a (Sharpe > RULES v2 in BOTH halves and MaxDD no worse) and 4b (vs SPY) on all "
        f"{len(gc)} gated grid points:")
    gc["both"] = gc["p4a"] & gc["p4b"]
    kp = gc.groupby(["rung", "gross"]).agg(n=("p4a", "size"), pass4a=("p4a", "sum"),
                                           pass4b=("p4b", "sum"), both=("both", "sum"))
    log(kp.to_string())
    log("  by family at the PROTOCOL rung:")
    log(gc[gc["rung"] == RUNG_HEAD].groupby(["family", "gross"]).agg(
        n=("p4a", "size"), pass4a=("p4a", "sum"), pass4b=("p4b", "sum")).to_string())
    if int(gc["p4a"].sum()) or int(gc["p4b"].sum()):
        log("\n  every 4a pass:")
        pa = gc[gc["p4a"]]
        if len(pa):
            log(pa[["panel", "rung", "gross", "arm", "on_share", "CAGR", "Sharpe", "MaxDD",
                    "H1", "H2", "OOS_Sharpe", "dSharpe"]].to_string(
                index=False, float_format=lambda x: f"{x:.4f}"))
        log(f"\n  4b passes: {int(gc['p4b'].sum())}; by rung "
            f"{gc.groupby('rung')['p4b'].sum().to_dict()}")
        log("  4b failure modes (which bar cuts):")
        log(gc["fail4b"].value_counts().head(12).to_string())
    log("\n  Rule 8 walk-forward: chooser over (level, w, depth) on IS <= 2016-12-31 Sharpe, "
        "OOS 2017+ read once, g=0.75.")
    log(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"\n  picks beating DO NOTHING (their own ungated parent) on OOS Sharpe: "
        f"{int((wf['vs_nogate'] > 0).sum())} of {len(wf)}; beating SPY OOS "
        f"{int((wf['OOS_Sharpe'] > wf['spy_OOS']).sum())}; beating RULES v2 OOS "
        f"{int((wf['OOS_Sharpe'] > wf['v2_OOS']).sum())}; mean regret {wf['regret'].mean():.4f}")
    log(wf.groupby(["family", "rung"]).agg(
        n=("vs_nogate", "size"), beat_nogate=("vs_nogate", lambda s: int((s > 0).sum())),
        mean_vs_nogate=("vs_nogate", "mean"),
        mean_pick_rate=("pick_on_share", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))

    log("\n  Rule 8 CLAIM leg: the win label measured on IS only, then on OOS only (K=5 "
        "equal-count buckets fitted on IS rates, applied unchanged to OOS).")
    cl = claim.copy()
    cl["bk"] = bucket(cl["on_share_IS"], 5, "count")
    tab = cl.dropna(subset=["bk"]).groupby("bk").agg(
        n=("win_IS", "size"), rate_IS=("on_share_IS", "median"),
        rate_OOS=("on_share_OOS", "median"),
        win_IS=("win_IS", "mean"), win_OOS=("win_OOS", "mean"),
        dSh_IS=("dSharpe_IS", "median"), dSh_OOS=("dSharpe_OOS", "median"))
    log(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    for grp, sub in list(cl.groupby("family")) + [("POOLED", cl)]:
        log(f"   {grp:7s} n={len(sub):4d}  IS rho(rate,dSharpe) "
            f"{spearman(sub['on_share_IS'], sub['dSharpe_IS']):+.4f}  "
            f"OOS {spearman(sub['on_share_OOS'], sub['dSharpe_OOS']):+.4f}   "
            f"IS AUC {auc(sub['on_share_IS'], sub['win_IS']):.4f}  "
            f"OOS AUC {auc(sub['on_share_OOS'], sub['win_OOS']):.4f}   "
            f"win IS {sub['win_IS'].mean():.3f} OOS {sub['win_OOS'].mean():.3f}  "
            f"label agree {float((sub['win_IS'] == sub['win_OOS']).mean()):.3f}")
    st = np.diff(tab["win_OOS"].values)
    log(f"   IS-fitted buckets applied to OOS: monotone_up "
        f"{bool((st >= 0).all())}, rho {spearman(range(len(tab)), tab['win_OOS']):.3f}, "
        f"span {tab['win_OOS'].iloc[-1] - tab['win_OOS'].iloc[0]:+.3f}")

    # =============================================================== [7] write-out
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    ph.to_csv(OUT / f"{STEM}.placebo.csv.gz", index=False, compression="gzip")
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    claim.to_csv(OUT / f"{STEM}.claim.csv", index=False)
    curves.to_csv(OUT / f"{STEM}.curves.csv", index=False)
    monos.to_csv(OUT / f"{STEM}.monotone.csv", index=False)
    conf.to_csv(OUT / f"{STEM}.predictors.csv", index=False)
    if len(suff):
        suff.to_csv(OUT / f"{STEM}.sufficiency.csv", index=False)
    exj.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    pd.concat([g4.assign(gate="G4"), g5.assign(gate="G5")], ignore_index=True).to_csv(
        OUT / f"{STEM}.gates.csv", index=False)

    log("\n" + "=" * 180)
    log("[7] SUMMARY")
    log(f"  Q1 monotone (pre-registered bar): {'CONFIRMED' if h1_pass else 'FAILS'}  "
        f"(monotone_up {int(fam_only['monotone_up'].sum())}/{len(fam_only)}, "
        f"rho>=0.80 {int((fam_only['rho'] >= 0.80).sum())}/{len(fam_only)})")
    log(f"  Q1 continuous: pooled AUC(on_share -> win) {cont.loc[cont['group']=='POOLED','auc_rate'].iloc[0]:.4f}, "
        f"rho(rate, dSharpe) {cont.loc[cont['group']=='POOLED','rho_rate_dSharpe'].iloc[0]:+.4f}")
    if len(suff):
        log(f"  Q2 within-bucket family gap: median {suff['max_gap'].median():.3f}, "
            f"max {suff['max_gap'].max():.3f}")
    p = conf[conf["group"] == "POOLED"].iloc[0]
    log(f"  Q3 pooled AUC: on_share {p['auc_on_share']:.4f} | gap {p['auc_gap']:.4f} | "
        f"depth {p['auc_depth']:.4f} | g_eff {p['auc_g_eff']:.4f}")
    log(f"  Q4 win rate REAL {head['win'].mean():.4f} | RAND "
        f"{ph[ph['kind']=='RAND']['win'].mean():.4f} | BLOCK "
        f"{ph[ph['kind']=='BLOCK']['win'].mean():.4f}")
    log(f"  Q5 4a {int(gc['p4a'].sum())} / 4b {int(gc['p4b'].sum())} / BOTH "
        f"{int((gc['p4a'] & gc['p4b']).sum())} of {len(gc)}; rule-8 picks beating v2 OOS "
        f"{int((wf['OOS_Sharpe'] > wf['v2_OOS']).sum())} of {len(wf)}")
    log(f"  gates: G1 {g1:.2e} | G2 {'PASS' if ok84 else 'FAIL'} | G3 {g3max:.3e} | "
        f"G4 {g4['dSharpe'].abs().max():.2e} | G5 {'PASS' if g5ok else 'FAIL'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
