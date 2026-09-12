#!/usr/bin/env python3
"""Idea 606 (cloud lane, 2026-09-12) - does the PLACEBO-EXCESS rate slope survive outside the
BREADTH family?

QUESTION
--------
Idea 602 swept 648 matched-gross twin pairs and KILLED its own headline (the twin win rate is not a
monotone function of the firing rate).  Its ONE surviving positive result was a placebo statement:
the median EXCESS of the real gate over its own rate- and run-length-matched BLOCK placebo rises
across five equal-count firing-rate buckets for QROLL,

    QROLL  +0.0259 -> +0.0446 -> +0.0705 -> +0.0695 -> +0.1017   (share > 0: 0.925 -> 1.000)
    ABS        NaN -> +0.0248 -> +0.0241 -> +0.0371 -> +0.0171   (flat)

i.e. a gate that fires often appears to beat a gate that fires equally often at random times, by more
and more as it fires more.  Every arm in that corpus reads the SAME market state - **breadth**, the
share of names above their 200d MA.  So the slope has two possible owners:

    (a) it is a property of GATES THAT FIRE - any market state, read at any rate, carries it; or
    (b) it is a property of the BREADTH SIGNAL - and idea 602's result is a statement about one
        predictor dressed as a statement about gating.

This run separates them by re-running the identical placebo differencing on THREE non-breadth market
states, with the same families, depths, cadences, grosses, cost rung, placebo kinds and seeds.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: state, rate bucket)
    1. STATE in {BREADTH, VOL, DISP, CORR}    (BREADTH is idea 602's, carried as the anchor)
    2. K     in {3, 4, 5, 6, 8} equal-count firing-rate buckets   (idea 602's KS; K=5 is its headline)
All 4 x 5 = 20 tuned points are reported.  REPORTED-NEVER-SELECTED, inherited verbatim from idea 602
and never re-tuned here: family (ABSZ / QEXP / QROLL), level, window w, depth (0.25/0.50/1.00),
cadence (D/W), gross (0.75/1.00), cost rung (0/10/25 for the real arms, 10 for the placebos),
placebo kind (RAND/BLOCK), seed (10), panel (U56 headline, B136 reported), window (FULL/IS/OOS).

THE FOUR STATES (all market-level, all causal, all oriented LOW = RISK-OFF so one gate form serves)
    BREADTH  share of panel names above their own 200d MA                      (idea 602's, verbatim)
    VOL      -1 x SPY 20d realised vol, annualised
    DISP     -1 x the 20d mean of the daily CROSS-SECTIONAL dispersion (std across names) of returns
    CORR     -1 x the 60d sigma-weighted mean PAIRWISE correlation of daily returns, computed in
             closed form from the equal-weight index variance and the constituent variances
             (rho_bar = (N^2 var_p - sum var_i) / (sum_i sum_{j != i} sd_i sd_j)) - exact, not a
             sampled approximation, and O(T N) rather than O(T N^2).

THE FAMILIES (idea 602's two scale-free forms, plus a cross-state-comparable analogue of its ABS)
    QEXP(q)     state_t < causal EXPANDING q-quantile of the state           (idea 336, verbatim)
    QROLL(q,w)  state_t < trailing-w-day q-quantile of the state             (idea 399, verbatim)
    ABSZ(B)     z_t < B, z = (state - causal expanding mean) / causal expanding std
                *** ABSZ IS NOT IDEA 602's ABS. *** Idea 602's ABS is a fixed level in BREADTH's own
                units (0.30 / 0.40 / 0.50) and has no meaning on VOL, DISP or CORR.  ABSZ is the
                cross-state-comparable analogue - a fixed threshold in the state's own causally
                standardised units - and every ABS claim below is made about ABSZ and labelled as
                such.  Idea 602's literal ABS is carried on BREADTH ONLY, as family ABSLIT, purely
                so gate G3 can test reproduction; it never enters a cross-state comparison.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO : on BREADTH at K = 5, ABSLIT/QEXP/QROLL reproduce idea 602's published sign pattern,
              and QROLL's top bucket exceeds its bottom bucket by >= 0.05 in median excess vs BLOCK.
    H_SLOPE : *** THE DECIDING TEST. *** QROLL's median excess vs BLOCK rises with the firing-rate
              bucket on EVERY non-breadth state (Spearman(bucket, median excess) > 0 on all three,
              at the headline K = 5).  PASS => the slope belongs to gates that fire (owner a).
              FAIL => it is a breadth-signal fact (owner b) and idea 602's one positive result is
              narrower than published.
    H_FLAT  : the parent's CONTRAST reproduces outside breadth - ABSZ's excess is flat
              (|Spearman(bucket, median excess)| < 0.5) on every state.
    H_SIGN  : the median excess vs BLOCK is > 0 in the TOP rate bucket on every state.
    H_ZERO  : the honest control - the slope lives in the REAL arm, not in the placebo.  The BLOCK
              placebo's own dSharpe against the same twin carries NO rate slope
              (|Spearman(bucket, median BLOCK dSharpe)| < 0.5) on every state.
    H_WF    : rule 8 - the top-minus-bottom bucket gap has the SAME SIGN measured on the IS window
              (..2016-12-31) and on the OOS window (2017-01-01..), read once, on every state.
    H_KEEP  : the honest control on capital - no arm in this corpus earns a KEEP.  4a against
              RULES v2 is 0, and any 4b pass is reported with its own matched-gross twin's verdict
              beside it (ideas 502/504/674/767/810: 4b certifies exposure, not the clause).

GATES (printed before any verdict is read)
    G1 runner identity: apply_eff on a never-firing multiplier == engine.backtest         bar 1e-12
    G2 placebo matching: RAND and BLOCK reproduce the real arm's de-grossed-day COUNT exactly and
       BLOCK reproduces its mean multiplier exactly (so they share the real arm's twin)   bar 1e-12
    G3 reproduction: idea 602's BREADTH numbers, via ABSLIT/QEXP/QROLL at K = 5           sign pattern
    G4 determinism: the whole placebo corpus recomputed from the same md5 seeds           bar 0

RULE 8 WALK-FORWARD (required): per (panel, state) the arm is chosen on the IS window alone by IS
Sharpe and the OOS window is read ONCE - OOS CAGR / Sharpe / MaxDD against RULES v2 (the live
baseline) and against SPY buy-and-hold, with both KEEP paths evaluated.

SURVIVORSHIP: U56 and B136 are current-constituent lists; every level is optimistic.  The headline
statistic is a WITHIN-PANEL difference between a real gate and a rate-matched shuffle of itself on
the same book, which survivorship moves far less than it moves levels; the walk-forward levels carry
the full bias.

Deterministic (md5-seeded), no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
import hashlib
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score            # noqa: E402
from engine import backtest, metrics, rebalance_mask                   # noqa: E402

DATE = "2026-09-12"
SLUG = "does-the-PLACEBO-EXCESS-rate-slope-survive-outside-the-BREADTH-family"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]                 # idea 336/399/602's quantiles
WS = [252, 504, 1008, 2016]             # idea 399/602's windows
ZS = [-1.0, -0.5, 0.0]                  # ABSZ levels (causal z)
BS_LIT = [0.30, 0.40, 0.50]             # idea 602's literal BREADTH ABS levels (G3 only)
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
STATES = ["BREADTH", "VOL", "DISP", "CORR"]     # TUNED 1
KS = [3, 4, 5, 6, 8]                            # TUNED 2
K_HEAD = 5
NSEED = 10
GSTEP = 0.01
MINQ = 252
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TIE = 1e-12
WARMUP = 260
PANELS = ["U56", "B136"]
PANEL_HEAD = "U56"
# idea 602's committed BREADTH medians (K=5, pooled panels) - the G3 / H_REPRO target
P602 = {"ABS":   [np.nan, 0.0248, 0.0241, 0.0371, 0.0171],
        "QEXP":  [0.0069, 0.0438, np.nan, np.nan, np.nan],
        "QROLL": [0.0259, 0.0446, 0.0705, 0.0695, 0.1017]}

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (ideas 42/336/399/602)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def _cadence(m, idx):
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Idea 399/602's runner: an ALREADY-EFFECTIVE (t+1-aligned) multiplier, switch cost on |dm|."""
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


def apply_gate(r_base, mult, gross, cost_bps):
    return apply_eff(r_base, mult.reindex(r_base.index).shift(1).fillna(1.0), gross, cost_bps)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def tests_4b(r, sp):
    s1, s2, s_oos, s_dd, s_cagr = sp
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def verdict_4a(r, bp):
    b1, b2, bdd = bp
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def spearman(a, b):
    a, b = pd.Series(a), pd.Series(b)
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- the four market states
def state_series(name, px):
    """Market state oriented LOW = RISK-OFF, so one gate form (state < threshold) serves all four."""
    stk = [c for c in px.columns if c != "SPY"]
    if name == "BREADTH":
        above = px[stk] > px[stk].rolling(200).mean()
        return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    rets = px[stk].pct_change()
    if name == "VOL":
        return -(px["SPY"].pct_change().rolling(20).std() * np.sqrt(252))
    if name == "DISP":
        return -(rets.std(axis=1).rolling(20).mean())
    if name == "CORR":
        # sigma-weighted mean pairwise correlation, closed form from the EW index variance
        n = rets.notna().sum(axis=1)
        ew = rets.mean(axis=1)
        var_p = ew.rolling(60).var()
        var_i = rets.rolling(60).var()
        sd_i = np.sqrt(var_i)
        sum_var = var_i.sum(axis=1)
        sum_sd = sd_i.sum(axis=1)
        num = (n ** 2) * var_p - sum_var
        den = sum_sd ** 2 - (sd_i ** 2).sum(axis=1)
        return -(num / den.replace(0, np.nan))
    raise ValueError(name)


def build_mults(st, idx, fam, lev, w, depth, cad):
    """state < threshold => multiply gross by (1 - depth).  Causal thresholds only."""
    if fam == "ABSLIT":
        thr = pd.Series(lev, index=st.index)
    elif fam == "ABSZ":
        mu = st.expanding(MINQ).mean()
        sd = st.expanding(MINQ).std()
        thr = mu + lev * sd
    elif fam == "QEXP":
        thr = st.expanding(MINQ).quantile(lev)
    elif fam == "QROLL":
        thr = st.rolling(w, min_periods=MINQ).quantile(lev)
    else:
        raise ValueError(fam)
    m = pd.Series(1.0, index=idx).where(~(st < thr), 1.0 - depth)
    m = m.where(st.notna() & thr.notna(), 1.0)
    return _cadence(m, idx) if cad == "W" else m


def placebo_mults(m_eff, depth, kind, seed):
    """Idea 602's placebos, verbatim.  RAND: iid days, EXACT de-grossed-day count.  BLOCK: circular
    shift - exact rate AND exact run-length distribution, so it shares the real arm's twin."""
    v = m_eff.values
    k = int((v < 1.0).sum())
    if k == 0:
        return m_eff.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(len(v))
        out[rng.choice(len(v), size=k, replace=False)] = 1.0 - depth
        return pd.Series(out, index=m_eff.index)
    return pd.Series(np.roll(v, int(rng.integers(1, len(v)))), index=m_eff.index)


class Twins:
    """Idea 602's matched-mean-gross static EWALL twin, exact g by linear interpolation."""

    def __init__(self, px, start):
        self.px, self.start, self.cache, self.n_bt = px, start, {}, 0

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
            lo = np.floor(round(g, 6) / GSTEP) * GSTEP
            need.add(round(lo, 6))
            need.add(round(lo + GSTEP, 6))
        for g in sorted(need):
            self._exact(g)

    def at(self, g, cost_bps):
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            r0, t0 = self._exact(lo)
        else:
            rl, tl = self._exact(lo)
            rh, th = self._exact(round(lo + GSTEP, 6))
            r0, t0 = (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th
        return r0 - t0 * cost_bps / 1e4


def arms_for(state):
    a = [("ABSZ", z, 0) for z in ZS] + [("QEXP", q, 0) for q in QS] \
        + [("QROLL", q, w) for q in QS for w in WS]
    if state == "BREADTH":
        a = [("ABSLIT", b, 0) for b in BS_LIT] + a
    return a


def buckets(v, K):
    """Equal-count buckets on the firing rate, idea 602's construction.

    Returns a POSITIONAL numpy array: the caller assigns it into a frame whose index is a slice of
    a larger one, so an index-aligned Series would silently NaN every row (it did, once)."""
    try:
        return pd.qcut(pd.Series(np.asarray(v)).rank(method="first"), K, labels=False).values
    except ValueError:
        return np.full(len(v), np.nan)


# ==================================================================================== run
def main():
    t0 = time.time()
    log("=" * 150)
    log(f"# Idea 606 - {SLUG}  (cloud lane, {DATE})")
    log("=" * 150)
    log("# Idea 602's ONE surviving positive result - QROLL's median excess over its own BLOCK")
    log("# placebo rising +0.026 -> +0.102 across five firing-rate buckets - was measured on arms")
    log("# that ALL read the same market state (breadth).  This run re-runs the identical placebo")
    log("# differencing on three NON-BREADTH states and asks who owns the slope: gates that fire,")
    log("# or the breadth signal.")
    log(f"# TUNED: state {STATES} x K {KS} = {len(STATES)*len(KS)} points, ALL reported.")
    log("# REPORTED-NEVER-SELECTED (inherited verbatim from idea 602): family, level, w, depth,")
    log("#   cadence, gross, cost rung, placebo kind, seed, panel, window.")
    log("# ABSZ IS NOT idea 602's ABS - it is the cross-state-comparable causal-z analogue; idea")
    log("#   602's literal breadth ABS is carried as ABSLIT on BREADTH only, for gate G3.")
    log("# SURVIVORSHIP: U56/B136 are current-constituent lists; levels are optimistic.  The")
    log("#   headline is a within-panel real-vs-shuffled-self difference, which the bias moves less.")

    cells, ph, wf = [], [], []
    gate_rows = []

    for panel in PANELS:
        px = (load_universe() if panel == "U56" else load_universe(broad=True)).dropna(how="all").ffill()
        idx = px.index
        start = idx[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy)
        s1, s2 = half_sharpes(spy)
        spy_pack = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])
        log(f"\n{'='*150}\nPANEL {panel}: {px.shape[1]} columns, eval {start.date()}..{idx[-1].date()} "
            f"({len(spy)} days)")
        log(f"   SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}")

        v2 = backtest(px, rules_v2_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]
        mv2 = metrics(v2)
        b1, b2 = half_sharpes(v2)
        base_pack = (b1, b2, mv2["MaxDD"])
        log(f"   RULES v2 (live baseline, 10 bps) {mv2['CAGR']:.2%} / {mv2['Sharpe']:.3f} / "
            f"{mv2['MaxDD']:.2%}")

        base0 = {}
        for g in GROSSES:
            res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
            base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
        tw = Twins(px, start)

        # ---- G1 runner identity (headline panel only) -------------------------------------
        if panel == PANEL_HEAD:
            r_g1, t_g1 = base0[G_HEAD]
            never = pd.Series(1.0, index=r_g1.index)
            rg, _ = apply_eff(r_g1 - t_g1 * RUNG_HEAD / 1e4, never, G_HEAD, 0)
            eng = backtest(px, ewall_weights(px, G_HEAD), cost_bps=RUNG_HEAD,
                           freq=FREQ)["returns"].loc[start:]
            g1 = float(np.abs((rg - eng).values).max())
            gate_rows.append(("G1 never-firing multiplier == engine.backtest", g1, 1e-12))

        for state in STATES:
            st = state_series(state, px)
            arms = arms_for(state)
            mult, m_eff, on_sh, gapc = {}, {}, {}, {}
            needed = []
            for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
                m = build_mults(st, idx, fam, lev, w, d, cad).loc[start:]
                me = m.reindex(base0[G_HEAD][0].index).shift(1).fillna(1.0)
                key = (fam, lev, w, d, cad)
                mult[key], m_eff[key] = m, me
                on_sh[key] = float((me < 1.0).mean())
                gapc[key] = 1.0 - float(me.mean())
                for g in GROSSES:
                    needed.append(g * float(me.mean()))
            tw.prewarm(needed)

            for g, c in product(GROSSES, RUNGS):
                rb = base0[g][0] - base0[g][1] * c / 1e4
                for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
                    key = (fam, lev, w, d, cad)
                    rg, me = apply_gate(rb, mult[key], g, c)
                    g_eff = g * float(me.mean())
                    rs = tw.at(g_eff, c)
                    mg, mst = metrics(rg), metrics(rs)
                    t4 = tests_4b(rg, spy_pack)
                    ts4 = tests_4b(rs, spy_pack)
                    cells.append(dict(
                        panel=panel, state=state, family=fam, level=lev, w=w, depth=d,
                        cadence=cad, gross=g, rung=c, on_share=on_sh[key], gap=gapc[key],
                        g_eff=g_eff, CAGR=mg["CAGR"], Sharpe=mg["Sharpe"], MaxDD=mg["MaxDD"],
                        IS_Sharpe=metrics(rg.loc[:IS_END])["Sharpe"],
                        OOS_CAGR=metrics(rg.loc[OOS_START:])["CAGR"],
                        OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"],
                        OOS_MaxDD=metrics(rg.loc[OOS_START:])["MaxDD"],
                        twin_Sharpe=mst["Sharpe"], dSharpe=mg["Sharpe"] - mst["Sharpe"],
                        IS_dSharpe=metrics(rg.loc[:IS_END])["Sharpe"]
                        - metrics(rs.loc[:IS_END])["Sharpe"],
                        OOS_dSharpe=metrics(rg.loc[OOS_START:])["Sharpe"]
                        - metrics(rs.loc[OOS_START:])["Sharpe"],
                        p4a=verdict_4a(rg, base_pack), p4b=all(t4.values()),
                        fail4b=",".join(k for k, v in t4.items() if not v) or "-",
                        twin_4b=all(ts4.values())))

                    if c == RUNG_HEAD:
                        for kind, s in product(("RAND", "BLOCK"), range(NSEED)):
                            pm = placebo_mults(me, d, kind,
                                               seed_of(panel, state, fam, lev, w, d, cad, g, kind, s))
                            rp, mep = apply_eff(rb, pm, g, c)
                            gp = g * float(mep.mean())
                            rsp = rs if abs(gp - g_eff) < 1e-12 else tw.at(gp, c)
                            dp = metrics(rp)["Sharpe"] - metrics(rsp)["Sharpe"]
                            ph.append(dict(
                                panel=panel, state=state, kind=kind, seed=s, family=fam,
                                level=lev, w=w, depth=d, cadence=cad, gross=g,
                                on_share=float((mep < 1.0).mean()), gap=1.0 - float(mep.mean()),
                                real_on=on_sh[key], real_gap=gapc[key], g_eff=gp,
                                dSharpe=dp,
                                IS_dSharpe=metrics(rp.loc[:IS_END])["Sharpe"]
                                - metrics(rsp.loc[:IS_END])["Sharpe"],
                                OOS_dSharpe=metrics(rp.loc[OOS_START:])["Sharpe"]
                                - metrics(rsp.loc[OOS_START:])["Sharpe"]))
            log(f"   {state:<8} {len(arms)} arms x {len(DEPTHS)}d x {len(CADENCES)}cad x "
                f"{len(GROSSES)}g x {len(RUNGS)} rungs;  twin cache {tw.n_bt} backtests;  "
                f"t={time.time()-t0:.0f}s")

        # ---- rule 8: pick per (panel, state) on IS Sharpe alone, read OOS once -------------
        cdf = pd.DataFrame(cells)
        cdf = cdf[(cdf.panel == panel) & (cdf.rung == RUNG_HEAD) & (cdf.family != "ABSLIT")]
        oS, oL = metrics(spy.loc[OOS_START:]), metrics(v2.loc[OOS_START:])
        for state in STATES:
            sub = cdf[cdf.state == state]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            wf.append(dict(panel=panel, state=state,
                           arm=f"{pick.family} L{pick.level} w{int(pick.w)} d{pick.depth} "
                               f"{pick.cadence} g{pick.gross}",
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           FULL_CAGR=pick.CAGR, FULL_Sharpe=pick.Sharpe, FULL_MaxDD=pick.MaxDD,
                           p4a=pick.p4a, p4b=pick.p4b, fail4b=pick.fail4b, twin_4b=pick.twin_4b,
                           SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"],
                           SPY_OOS_MaxDD=oS["MaxDD"], V2_OOS_CAGR=oL["CAGR"],
                           V2_OOS_Sharpe=oL["Sharpe"], V2_OOS_MaxDD=oL["MaxDD"]))

    cells = pd.DataFrame(cells)
    ph = pd.DataFrame(ph)
    wf = pd.DataFrame(wf)
    cells.to_csv(f"{OUT}.cells.csv.gz", index=False)
    ph.to_csv(f"{OUT}.placebo.csv.gz", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------------ gates
    log(f"\n{'='*150}\nGATES\n{'='*150}")
    g2a = float((ph.groupby(["panel", "state", "family", "level", "w", "depth", "cadence",
                             "gross"]).apply(lambda d: (d.on_share - d.real_on).abs().max(),
                                             include_groups=False)).max())
    blk = ph[ph.kind == "BLOCK"]
    g2b = float((blk.gap - blk.real_gap).abs().max())
    gate_rows.append(("G2a placebo de-grossed-day share == the real arm's", g2a, 1e-12))
    gate_rows.append(("G2b BLOCK mean multiplier == the real arm's", g2b, 1e-12))
    # G4 determinism: recompute a slice of the placebo corpus from the same md5 seeds
    rec = []
    px = load_universe().dropna(how="all").ffill()
    st = state_series("VOL", px)
    start = px.index[WARMUP]
    r0 = backtest(px, ewall_weights(px, G_HEAD), cost_bps=0, freq=FREQ)
    rb = (r0["returns"].loc[start:] - r0["turnover"].loc[start:] * RUNG_HEAD / 1e4)
    tw2 = Twins(px, start)
    for q in QS:
        m = build_mults(st, px.index, "QEXP", q, 0, 0.50, "W").loc[start:]
        me = m.reindex(rb.index).shift(1).fillna(1.0)
        for kind, s in product(("RAND", "BLOCK"), range(3)):
            pm = placebo_mults(me, 0.50, kind,
                               seed_of("U56", "VOL", "QEXP", q, 0, 0.50, "W", G_HEAD, kind, s))
            rp, mep = apply_eff(rb, pm, G_HEAD, RUNG_HEAD)
            d = metrics(rp)["Sharpe"] - metrics(tw2.at(G_HEAD * float(mep.mean()),
                                                       RUNG_HEAD))["Sharpe"]
            got = ph[(ph.panel == "U56") & (ph.state == "VOL") & (ph.family == "QEXP")
                     & (ph.level == q) & (ph.depth == 0.50) & (ph.cadence == "W")
                     & (ph.gross == G_HEAD) & (ph.kind == kind) & (ph.seed == s)].dSharpe
            rec.append(abs(d - float(got.iloc[0])))
    gate_rows.append(("G4 determinism (18 placebos recomputed from md5 seeds)", max(rec), 0.0))
    for nm, v, bar in gate_rows:
        log(f"   {nm:<62} max|d| {v:.3e}   bar {bar:.0e}   "
            f"{'PASS' if v <= bar else 'FAIL'}")
    assert all(v <= bar for _, v, bar in gate_rows), "a gate failed - no verdict is read"

    # ------------------------------------------------------------------ the excess table
    log(f"\n{'='*150}\nTHE STATISTIC - median EXCESS of the REAL gate over its own BLOCK placebo,\n"
        f"by equal-count firing-rate bucket (idea 602's construction, on four states)\n{'='*150}")
    keys = ["panel", "state", "family", "level", "w", "depth", "cadence", "gross"]
    real = cells[cells.rung == RUNG_HEAD].set_index(keys)[
        ["dSharpe", "IS_dSharpe", "OOS_dSharpe"]].rename(
        columns={"dSharpe": "REAL", "IS_dSharpe": "REAL_IS", "OOS_dSharpe": "REAL_OOS"})
    pm = ph.groupby(keys + ["kind"])[["dSharpe", "IS_dSharpe", "OOS_dSharpe"]].median().reset_index()
    wide = pm.pivot_table(index=keys, columns="kind",
                          values=["dSharpe", "IS_dSharpe", "OOS_dSharpe"])
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    ex = wide.join(real).reset_index()
    isr = cells[cells.rung == RUNG_HEAD].set_index(keys)
    ex = ex.merge(isr[["on_share"]].reset_index(), on=keys, how="left")
    ex["excess_vs_BLOCK"] = ex["REAL"] - ex["dSharpe_BLOCK"]
    ex["excess_vs_RAND"] = ex["REAL"] - ex["dSharpe_RAND"]
    ex.to_csv(f"{OUT}.excess.csv", index=False)

    results = {}
    for K in KS:
        for state in STATES:
            for fam in ("ABSZ", "QEXP", "QROLL", "ABSLIT"):
                sub = ex[(ex.state == state) & (ex.family == fam)].copy()
                if len(sub) < K:
                    continue
                sub["bk"] = buckets(sub.on_share.values, K)
                med = sub.groupby("bk")["excess_vs_BLOCK"].median().dropna()
                if len(med) == 0:
                    continue          # every cell NaN (e.g. a gate level that never fires)
                shr = sub.groupby("bk")["excess_vs_BLOCK"].apply(lambda s: float((s > 0).mean()))
                blkmed = sub.groupby("bk")["dSharpe_BLOCK"].median().dropna()
                realmed = sub.groupby("bk")["REAL"].median().dropna()
                rndmed = sub.groupby("bk")["dSharpe_RAND"].median().dropna()
                results[(K, state, fam)] = dict(
                    med=med, share=shr, blk=blkmed, real=realmed, rnd=rndmed,
                    rho=spearman(med.index.values, med.values),
                    rho_real=spearman(realmed.index.values, realmed.values) if len(realmed) else np.nan,
                    rho_rand=spearman(rndmed.index.values, rndmed.values) if len(rndmed) else np.nan,
                    blk_top_minus_bot=(float(blkmed.iloc[-1] - blkmed.iloc[0])
                                       if len(blkmed) > 1 else np.nan),
                    real_top_minus_bot=(float(realmed.iloc[-1] - realmed.iloc[0])
                                        if len(realmed) > 1 else np.nan),
                    rho_blk=spearman(blkmed.index.values, blkmed.values) if len(blkmed) else np.nan,
                    top_minus_bot=float(med.iloc[-1] - med.iloc[0]) if len(med) > 1 else np.nan,
                    top=float(med.iloc[-1]), n=len(sub))

    log(f"\n  HEADLINE K = {K_HEAD} (idea 602's).  Median excess vs BLOCK by rate bucket "
        f"(0 = fires least):")
    for state in STATES:
        log(f"\n   --- state {state} " + "-" * 100)
        for fam in ("ABSLIT", "ABSZ", "QEXP", "QROLL"):
            r = results.get((K_HEAD, state, fam))
            if r is None:
                continue
            cellsm = "  ".join(f"b{int(b)}:{v:+.4f}" for b, v in r["med"].items())
            shm = "  ".join(f"{r['share'].get(b, np.nan):.3f}" for b in r["med"].index)
            log(f"     {fam:<7} n={r['n']:<4} {cellsm}")
            log(f"     {'':<7} share>0: {shm}      rho(bucket, excess) = {r['rho']:+.4f}   "
                f"top-bottom = {r['top_minus_bot']:+.4f}")

    # ------------------------------------------------------------------ H_REPRO / G3
    log(f"\n{'='*150}\nH_REPRO / G3 - does BREADTH reproduce idea 602's published pattern?\n{'='*150}")
    rb602 = results.get((K_HEAD, "BREADTH", "ABSLIT"))
    rq = results.get((K_HEAD, "BREADTH", "QROLL"))
    rqe = results.get((K_HEAD, "BREADTH", "QEXP"))
    log("   idea 602 (pooled panels, K=5):")
    for f, v in P602.items():
        log(f"     {f:<6} " + "  ".join("   n/a" if np.isnan(x) else f"{x:+.4f}" for x in v))
    log("   this run (U56 + B136, K=5, ABSLIT = idea 602's literal breadth ABS):")
    for f, r in (("ABS", rb602), ("QEXP", rqe), ("QROLL", rq)):
        if r is None:
            log(f"     {f:<6} (no cells)")
            continue
        log(f"     {f:<6} " + "  ".join(f"{v:+.4f}" for v in r["med"].values))
    h_repro = bool(rq is not None and rq["top_minus_bot"] >= 0.05 and rq["rho"] > 0)
    if rq is not None:
        log(f"   QROLL top-minus-bottom = {rq['top_minus_bot']:+.4f} (bar >= +0.0500), "
            f"rho = {rq['rho']:+.4f} (bar > 0)")
    else:
        log("   QROLL on BREADTH produced no scorable buckets")
    log(f"   H_REPRO / G3 -> {'PASS' if h_repro else 'FAIL'}")

    # ------------------------------------------------------------------ H_SLOPE (the deciding test)
    log(f"\n{'='*150}\nH_SLOPE - THE DECIDING TEST: does QROLL's slope survive outside BREADTH?\n"
        f"{'='*150}")
    log(f"   {'state':<9} {'rho(bucket, excess)':>21} {'top-bottom':>12} {'top bucket':>12} "
        f"{'bottom bucket':>14}  slope > 0?")
    slope_ok = {}
    for state in STATES:
        r = results.get((K_HEAD, state, "QROLL"))
        if r is None:
            continue
        slope_ok[state] = bool(r["rho"] > 0)
        log(f"   {state:<9} {r['rho']:>21.4f} {r['top_minus_bot']:>12.4f} "
            f"{r['med'].iloc[-1]:>12.4f} {r['med'].iloc[0]:>14.4f}  "
            f"{'YES' if r['rho'] > 0 else 'NO'}")
    h_slope = bool(all(slope_ok.get(s, False) for s in STATES if s != "BREADTH"))
    log(f"\n   QROLL slope positive on all three NON-BREADTH states -> "
        f"{'PASS - the slope belongs to GATES THAT FIRE' if h_slope else 'FAIL - it is a BREADTH-SIGNAL fact'}")
    log(f"   across all {len(KS)} K rungs (robustness, not a selection):")
    for K in KS:
        row = "  ".join(f"{s}:{results[(K,s,'QROLL')]['rho']:+.3f}"
                        for s in STATES if (K, s, "QROLL") in results)
        log(f"     K={K}: {row}")

    # ------------------------------------------------------------------ H_FLAT / H_SIGN / H_ZERO
    log(f"\n{'='*150}\nTHE DECOMPOSITION - excess = REAL - BLOCK.  Which leg carries the slope?\n{'='*150}")
    log("   For QROLL at K = 5, the two legs of the difference read separately:")
    log(f"   {'state':<9} {'rho(bk, REAL)':>14} {'REAL top-bot':>13} {'rho(bk, BLOCK)':>15} "
        f"{'BLOCK top-bot':>14} {'rho(bk, RAND)':>14} {'share of gap from BLOCK':>25}")
    decomp = []
    for state in STATES:
        r = results.get((K_HEAD, state, "QROLL"))
        if r is None:
            continue
        tot = r["top_minus_bot"]
        frac = (-r["blk_top_minus_bot"] / tot) if tot not in (0, np.nan) and abs(tot) > 1e-12 else np.nan
        decomp.append(dict(state=state, rho_real=r["rho_real"],
                           real_top_minus_bot=r["real_top_minus_bot"], rho_blk=r["rho_blk"],
                           blk_top_minus_bot=r["blk_top_minus_bot"], rho_rand=r["rho_rand"],
                           excess_top_minus_bot=tot, share_from_placebo=frac))
        log(f"   {state:<9} {r['rho_real']:>14.4f} {r['real_top_minus_bot']:>13.4f} "
            f"{r['rho_blk']:>15.4f} {r['blk_top_minus_bot']:>14.4f} {r['rho_rand']:>14.4f} "
            f"{frac:>25.1%}")
    pd.DataFrame(decomp).to_csv(f"{OUT}.decomposition.csv", index=False)
    log("   READING: a NEGATIVE rho(bk, BLOCK) with a FLAT-or-NEGATIVE rho(bk, REAL) means the")
    log("   'excess rises with the firing rate' is the PLACEBO DECAYING, not the real gate improving -")
    log("   a shuffled gate that de-grosses on more days pays more switch cost and mistimes more of")
    log("   them, so the gap widens with the rate under a null in which the real gate does nothing.")

    log(f"\n{'='*150}\nH_FLAT / H_SIGN / H_ZERO\n{'='*150}")
    flat_ok, sign_ok, zero_ok = {}, {}, {}
    for state in STATES:
        ra = results.get((K_HEAD, state, "ABSZ"))
        rr = results.get((K_HEAD, state, "QROLL"))
        flat_ok[state] = bool(ra is not None and np.isfinite(ra["rho"]) and abs(ra["rho"]) < 0.5)
        sign_ok[state] = bool(rr is not None and rr["top"] > 0)
        zero_ok[state] = bool(rr is not None and np.isfinite(rr["rho_blk"])
                              and abs(rr["rho_blk"]) < 0.5)
        ar = ra["rho"] if ra is not None else float("nan")
        qt = rr["top"] if rr is not None else float("nan")
        qb = rr["rho_blk"] if rr is not None else float("nan")
        log(f"   {state:<9} ABSZ rho {ar:+.4f} (flat<0.5: {flat_ok[state]})   "
            f"QROLL top bucket {qt:+.4f} (>0: {sign_ok[state]})   "
            f"BLOCK's own rho {qb:+.4f} (flat<0.5: {zero_ok[state]})")
    h_flat, h_sign, h_zero = all(flat_ok.values()), all(sign_ok.values()), all(zero_ok.values())
    for nm, v in (("H_FLAT", h_flat), ("H_SIGN", h_sign), ("H_ZERO", h_zero)):
        log(f"   {nm} -> {'PASS' if v else 'FAIL'}")

    # ------------------------------------------------------------------ H_WF (rule 8 on the slope)
    log(f"\n{'='*150}\nH_WF - rule 8 on the STATISTIC: the IS and OOS top-minus-bottom gap\n{'='*150}")
    wfslope = []
    for state in STATES:
        sub = ex[(ex.state == state) & (ex.family == "QROLL")].copy()
        sub["bk"] = buckets(sub.on_share.values, K_HEAD)
        m_is = sub.assign(e=sub["REAL_IS"] - sub["IS_dSharpe_BLOCK"]
                          ).groupby("bk")["e"].median().dropna()
        m_oos = sub.assign(e=sub["REAL_OOS"] - sub["OOS_dSharpe_BLOCK"]
                           ).groupby("bk")["e"].median().dropna()
        if len(m_is) < 2 or len(m_oos) < 2:
            log(f"   {state:<9} not scorable (fewer than 2 non-empty buckets)")
            wfslope.append(dict(state=state, IS_gap=np.nan, OOS_gap=np.nan, same_sign=False))
            continue
        gi = float(m_is.iloc[-1] - m_is.iloc[0])
        go = float(m_oos.iloc[-1] - m_oos.iloc[0])
        wfslope.append(dict(state=state, IS_gap=gi, OOS_gap=go,
                            same_sign=bool(np.sign(gi) == np.sign(go))))
        log(f"   {state:<9} IS top-bottom {gi:+.4f}   OOS top-bottom {go:+.4f}   "
            f"same sign: {np.sign(gi) == np.sign(go)}")
    h_wf = all(r["same_sign"] for r in wfslope)
    pd.DataFrame(wfslope).to_csv(f"{OUT}.wfslope.csv", index=False)
    log(f"   H_WF -> {'PASS' if h_wf else 'FAIL'}")

    # ------------------------------------------------------------------ rule 8 book leg + KEEP
    log(f"\n{'='*150}\nRULE 8 BOOK LEG - arm chosen on IS Sharpe alone, OOS read ONCE\n{'='*150}")
    log("   " + wf.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    at10 = cells[(cells.rung == RUNG_HEAD) & (cells.family != "ABSLIT")]
    n4a, n4b = int(at10.p4a.sum()), int(at10.p4b.sum())
    n_both = int((at10.p4a & at10.p4b).sum())
    n_beat = int((at10.p4b & ~at10.twin_4b).sum())
    log(f"\n   KEEP paths over all {len(at10)} arms at 10 bps: 4a {n4a}, 4b {n4b}, BOTH {n_both}")
    log(f"   4b passes whose OWN matched-gross static twin FAILS 4b: {n_beat}  "
        f"<- the only ones where 4b sees the gate rather than the exposure")
    h_keep = bool(n4a == 0)
    log(f"   H_KEEP (no arm earns 4a against RULES v2) -> {'PASS' if h_keep else 'FAIL'}")
    for _, r in wf[wf.panel == PANEL_HEAD].iterrows():
        log(f"   {r.state:<8} rule-8 pick {r.arm:<28} FULL {r.FULL_CAGR:7.2%}/{r.FULL_Sharpe:6.3f}/"
            f"{r.FULL_MaxDD:7.2%}  OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:6.3f}/{r.OOS_MaxDD:7.2%}"
            f"   vs RULES v2 OOS {r.V2_OOS_CAGR:6.2%}/{r.V2_OOS_Sharpe:5.3f}/{r.V2_OOS_MaxDD:7.2%}"
            f"   vs SPY OOS {r.SPY_OOS_CAGR:6.2%}/{r.SPY_OOS_Sharpe:5.3f}/{r.SPY_OOS_MaxDD:7.2%}"
            f"   4a={r.p4a} 4b={r.p4b}")

    # ------------------------------------------------------------------ verdict
    log(f"\n{'='*150}\nVERDICT\n{'='*150}")
    H = dict(H_REPRO=h_repro, H_SLOPE=h_slope, H_FLAT=h_flat, H_SIGN=h_sign,
             H_ZERO=h_zero, H_WF=h_wf, H_KEEP=h_keep)
    for k, v in H.items():
        log(f"   {k:<9} {'PASS' if v else 'FAIL'}")
    log(f"   {sum(H.values())} of {len(H)} pre-registered hypotheses pass.")
    log(f"   OWNER OF THE SLOPE -> "
        f"{'GATES THAT FIRE (it survives on every state)' if h_slope else 'THE BREADTH SIGNAL (it does not survive outside it)'}")
    log(f"   CAPITAL -> {'KEEP-candidate' if (n_both > 0 and n_beat > 0) else 'KILL (no book earns capital here)'}")
    pd.DataFrame([H]).to_csv(f"{OUT}.hypotheses.csv", index=False)
    log(f"\n   elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
