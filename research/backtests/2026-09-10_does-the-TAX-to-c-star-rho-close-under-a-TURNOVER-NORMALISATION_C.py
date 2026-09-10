#!/usr/bin/env python3
"""Idea 608 - "does-the-TAX-to-c-star-rho-close-under-a-TURNOVER-NORMALISATION" (lane C).

What this run exists to settle
------------------------------
Idea 605 decomposed every gated arm's cost drag EXACTLY into

    DRAG = SWITCH_TAX + TIMING,   SWITCH_TAX = g*mean|dm| >= 0,
    TIMING = mean(m*t0) - mean(t0(g_eff))

and found the tax carries 1.70x the drag, yet it orders the arm-level CROSSOVER COST c* (the cost
rung at which a gate stops beating its matched-gross twin) at only

    rho(tax, c*) = -0.5131 pooled   (-0.5950 ABS / -0.4117 QEXP / -0.5614 QROLL, n = 494)

The queue's hypothesis: the missing part is the BASE book's own turnover LEVEL - a tax of 24 bps a
year means something different on a book that churns 40%/yr than on one that churns 200%/yr - so
expressing the tax as a FRACTION of the base's mean turnover per panel should close rho toward -1.

Two facts make this exactly, not approximately, testable, and both are gated below.

  (i) A normaliser that is CONSTANT WITHIN A GROUP cannot change the within-group Spearman AT ALL
      (rank correlation is invariant to any strictly-positive monotone rescaling applied uniformly
      inside the group).  A "per-panel" normaliser is by construction constant within a panel.  So
      the queue's proposal can only ever move the POOLED number, by re-scaling the tax ACROSS
      panels; every per-panel rho it is compared against is frozen.  G6 checks this numerically.

 (ii) The base book EWALL(g) = g * EWALL(1) up to weekly-drift, so its turnover scales with g while
      its Sharpe ladder - and therefore c* - does NOT.  The raw tax (= g*mean|dm|) therefore carries
      a factor-1.333 gross scaling that c* does not, i.e. a KNOWN spurious axis inside the pooled
      -0.5131.  Dividing by the base's own mean turnover cancels g exactly.  G7 measures both legs.

So the honest question splits: how much of the gap to -1 is (a) a units artefact the normalisation
removes, and (b) something the normalisation cannot touch?  The algebra names (b) in advance: with
the ladder linear in cost and the denominator vol nearly so,

    dSharpe(c) ~= dSharpe_0 - (c/1e4)*252*[ mean(Cg)/vol_g - mean(Cs)/vol_s ]
    => c* ~= dSharpe_0 / SLOPE,   SLOPE = (252/1e4)*[ mean(Cg)/vol_g - mean(Cs)/vol_s ]

c* is a RATIO of the zero-cost edge to a vol-normalised drag.  Any tax-only statistic is missing
the numerator.  N9 below is that analytic normaliser and is reported as the control: if it lands at
-1 while every turnover normalisation stalls, the missing part is the EDGE, not the turnover level.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (THE QUEUE'S)  Re-run the c* regression with the tax expressed as a fraction of the base's
                      mean turnover, on a ladder of normalisers x panel.  Pre-registered:
                        CLOSES   if some TURNOVER normaliser (N2-N6) reaches pooled |rho| >= 0.80
                        PARTIAL  if the best turnover normaliser improves pooled |rho| by >= 0.15
                                 over N0's 0.5131 but stays below 0.80
                        REFUTED  if no turnover normaliser improves pooled |rho| by >= 0.15
    Q2 (INVARIANCE)   Verify fact (i): max |rho_normalised - rho_raw| within every panel x gross
                      group, over every normaliser.  Bar 1e-12.  If this is 0, then NO per-panel
                      normalisation can ever be defended on a per-panel number, and the record must
                      quote the pooled one to claim anything at all.
    Q3 (WHAT IS LEFT) Decompose the residual: rho(drag, c*), rho(vol-normalised drag, c*),
                      rho(SLOPE/dSharpe_0, c*), and rho(tax, c*) INSIDE dSharpe_0 quintiles.  If
                      the edge is the missing part, conditioning on it should close rho where
                      dividing by turnover does not.
    Q4 (RULE 8)       The claim itself walked forward: build tax / drag / c* on IS (<= 2016-12-31)
                      ONLY, pick the normaliser that maximises |rho| there, read that pick ONCE on
                      OOS (2017+).  All normalisers' OOS rho reported anyway.
    Q5 (PROTOCOL)     Both KEEP paths on every arm at rungs 0/10/25, and the rule-8 book chooser
                      (IS Sharpe pick, OOS read once) with OOS CAGR/Sharpe/MaxDD against the live
                      RULES v2 baseline and SPY.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. normaliser  10 rungs N0..N9, ALL reported at every panel and family, none selected on
                   except in Q4, where the pick is made on IS only and read once on OOS.
    2. panel       U56 / B136 / SMALL439 / POOLED, all reported everywhere.
Reported axes, NEVER tuned: family, level, w, depth, gross, cadence, cost rung, censoring rule.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived ladder r_gate(c) = m*r0 - (c/1e4)*(m*t0 + g*|dm|) vs a LIVE engine.backtest put
        through idea 399's own apply_gate, at every rung.  Bar 1e-12.
    G2  fast numpy CAGR/Sharpe/MaxDD vs engine.metrics on 200 real series.  Bar 1e-12.
    G3  idea 605's COMMITTED .drag.csv, all 648 arms joined on switch_tax / timing / drag /
        dSharpe_0 / cstar / g_eff / on_share.  Bar 1e-9.
    G4  idea 605's PUBLISHED rho(tax, c*) headline reproduced to 4dp on its own censoring rule
        (finite c* AND c* > 0, n = 494): -0.5131 / -0.5950 / -0.4117 / -0.5614.
    G5  the drag identity DRAG == SWITCH_TAX + TIMING on all 648 arms.  Bar 1e-15.
    G6  Q2's invariance: within panel x gross, every normaliser's rho equals the raw tax's.
    G7  gross scaling: tax(g=1.00)/tax(g=0.75) == 4/3 exactly, while c* is gross-stable.

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
current-constituent lists, so CAGR and drawdown LEVELS are optimistic; the rank statistics this run
is about are unaffected by a common level shift.  SMALL439 starts 2010-01-04.

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
PARENT_DRAG = OUT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.drag.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0.0, 10.0, 25.0]                    # PROTOCOL's own rung, plus idea 602/605's two others
RUNG_HEAD = 10.0
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
GSTEP = 0.01
CSTAR_TOP = 500.0

# idea 605's published headline, for G4 (its own censoring: finite c* AND c* > 0)
PUB605 = {"POOLED": -0.5131, "ABS": -0.5950, "QEXP": -0.4117, "QROLL": -0.5614}
PUB605_N = {"POOLED": 494, "ABS": 60, "QEXP": 60, "QROLL": 374}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 900)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/336/399)
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
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = (r.mean() * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def fvol(r):
    return float(r.std(ddof=1) * np.sqrt(252.0))


class Slices:
    def __init__(self, idx):
        self.n = len(idx)
        self.h = self.n // 2
        self.is_end = int(idx.searchsorted(pd.Timestamp(IS_END), side="right"))
        self.oos = int(idx.searchsorted(pd.Timestamp(OOS_START), side="left"))


def pack(r, S):
    """(CAGR, Sharpe, MaxDD, H1, H2, IS_Sharpe, OOS_CAGR, OOS_Sharpe, OOS_MaxDD)."""
    c, s, d = fmet(r)
    oc, os_, od = fmet(r[S.oos:])
    return (c, s, d, fsharpe(r[:S.h]), fsharpe(r[S.h:]), fsharpe(r[:S.is_end]), oc, os_, od)


def spearman(a, b):
    """Idea 605's helper verbatim (+inf is notna and ranks largest)."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def crossover(rg0, Cg, rs0, Cs):
    """c* on the exact derived ladder: 0 if the gate already loses at zero cost, +inf if it still
    wins at CSTAR_TOP, else 45-step bisection (idea 605's, verbatim)."""
    def dsh(c):
        return fsharpe(rg0 - Cg * c / 1e4) - fsharpe(rs0 - Cs * c / 1e4)
    d0 = dsh(0.0)
    if not np.isfinite(d0):
        return np.nan, np.nan
    if d0 <= 0:
        return 0.0, d0
    if dsh(CSTAR_TOP) > 0:
        return np.inf, d0
    lo, hi = 0.0, CSTAR_TOP
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        if dsh(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), d0


# ---------------------------------------------------------------- twin machinery (idea 602/605)
class Twins:
    def __init__(self, px, start):
        self.px, self.start, self.cache, self.n_bt = px, start, {}, 0

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
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            return self._exact(lo)
        rl, tl = self._exact(lo)
        rh, th = self._exact(round(lo + GSTEP, 6))
        return (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th


# ---------------------------------------------------------------- the normaliser ladder (tuned 1)
# Each entry: (id, label, what it divides the numerator by, numerator column)
NORMALISERS = [
    ("N0", "tax (idea 605's raw)",                 "1",                        "switch_tax"),
    ("N1", "tax / g",                              "the arm's own gross",      "switch_tax"),
    ("N2", "tax / T_panel",                        "panel base turnover @g=1", "switch_tax"),
    ("N3", "tax / T_panel_gross",                  "the arm's own base book",  "switch_tax"),
    ("N4", "tax / mean(m*t0)",                     "the GATE's realised base", "switch_tax"),
    ("N5", "tax / mean(Cs)",                       "the TWIN's realised turn", "switch_tax"),
    ("N6", "tax / T_v2_panel",                     "RULES v2's turnover",      "switch_tax"),
    ("N7", "drag (unnormalised)",                  "1",                        "drag"),
    ("N8", "drag / T_panel_gross",                 "the arm's own base book",  "drag"),
    ("N9", "SLOPE / dSharpe_0  (analytic control)", "the zero-cost EDGE",      "slope"),
]
TURNOVER_NORMS = ["N2", "N3", "N4", "N5", "N6"]     # the queue's proposal proper


def norm_values(d):
    """Return a DataFrame of the 10 normaliser columns for the arm table d."""
    v = pd.DataFrame(index=d.index)
    v["N0"] = d["switch_tax"]
    v["N1"] = d["switch_tax"] / d["gross"]
    v["N2"] = d["switch_tax"] / d["T_panel"]
    v["N3"] = d["switch_tax"] / d["T_panel_gross"]
    v["N4"] = d["switch_tax"] / d["gate_turn"]
    v["N5"] = d["switch_tax"] / d["twin_turn"]
    v["N6"] = d["switch_tax"] / d["T_v2_panel"]
    v["N7"] = d["drag"]
    v["N8"] = d["drag"] / d["T_panel_gross"]
    v["N9"] = d["slope"] / d["dSharpe_0"]
    return v


# ---------------------------------------------------------------- per-panel run
def run_panel(panel, px):
    start = px.index[260]
    idx = px.index
    eval_idx = px.loc[start:].index
    S = Slices(eval_idx)
    spy = px["SPY"].pct_change().fillna(0).loc[start:].values
    sc, ss, sd = fmet(spy)
    spy_pack = (fsharpe(spy[:S.h]), fsharpe(spy[S.h:]), fsharpe(spy[S.oos:]), sd, sc,
                fmet(spy[S.oos:])[0], fmet(spy[S.oos:])[2])

    br_full = breadth(px)
    br = br_full.loc[start:]
    log(f"\n{'='*185}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(br)} days); IS {S.is_end} d, OOS {S.n - S.oos} d")
    log(f"  SPY {sc:.2%} / {ss:.3f} / {sd:.2%}; 4b bars: CAGR floor {0.70*sc:.2%}, DD cap "
        f"{-0.60*abs(sd):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, OOS {spy_pack[2]:.3f}")

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}

    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:].values, res["turnover"].loc[start:].values)
    rv2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    rv1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)
    ref0 = {"v2": (rv2["returns"].loc[start:].values, rv2["turnover"].loc[start:].values),
            "v1": (rv1["returns"].loc[start:].values, rv1["turnover"].loc[start:].values),
            "SPY": (spy, np.zeros(len(spy)))}

    # ---- the NEW quantities: base-book turnover LEVELS, the queue's normalisers
    T_panel = float(base0[1.00][1].mean())            # base turnover at g = 1.00, one per panel
    T_gross = {g: float(base0[g][1].mean()) for g in GROSSES}
    T_v2 = float(ref0["v2"][1].mean())
    T_v1 = float(ref0["v1"][1].mean())
    log(f"  BASE TURNOVER LEVELS (the queue's normaliser): EWALL g=1.00 {T_panel:.6f}/day "
        f"({T_panel*252:.1%}/yr), g=0.75 {T_gross[0.75]:.6f} (ratio {T_gross[0.75]/T_panel:.6f}), "
        f"RULES v2 {T_v2:.6f} ({T_v2*252:.1%}/yr), v1 {T_v1:.6f} ({T_v1*252:.1%}/yr)")

    base_packs = {}
    for c in RUNGS:
        b = ref0["v2"][0] - ref0["v2"][1] * c / 1e4
        base_packs[c] = (fsharpe(b[:S.h]), fsharpe(b[S.h:]), fmet(b)[2],
                         fsharpe(b[S.oos:]), fmet(b[S.oos:])[0], fmet(b[S.oos:])[2])

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

    rows, cells = [], []
    for g in GROSSES:
        r0, t0 = base0[g]
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            key = (fam, lev, w, d, cad)
            me, sw = m_eff[key], switch[key]
            g_eff = g * float(me.mean())
            rg0, Cg = me * r0, me * t0 + g * sw
            rs0, Cs = tw.at0(g_eff)

            tax = g * float(sw.mean())
            gate_turn = float((me * t0).mean())
            twin_turn = float(Cs.mean())
            timing = gate_turn - twin_turn
            dr = float(Cg.mean() - Cs.mean())
            cstar, d0 = crossover(rg0, Cg, rs0, Cs)
            vol_g, vol_s = fvol(rg0), fvol(rs0)
            slope = (252.0 / 1e4) * (float(Cg.mean()) / vol_g - float(Cs.mean()) / vol_s)

            rec = dict(panel=panel, gross=g, family=fam, level=lev, w=w, depth=d, cadence=cad,
                       arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                       on_share=on_share[key], rate_inst=rate_inst[(fam, lev, w)],
                       g_eff=g_eff, n_switch=float((sw > 1e-12).sum()),
                       switch_per_yr=float((sw > 1e-12).sum()) / (len(sw) / 252.0),
                       switch_tax=tax, timing=timing, drag=dr, resid=dr - (tax + timing),
                       tax_share=tax / abs(dr) if abs(dr) > 1e-18 else np.nan,
                       dSharpe_0=d0, cstar=cstar,
                       gate_turn=gate_turn, twin_turn=twin_turn,
                       T_panel=T_panel, T_panel_gross=T_gross[g], T_v2_panel=T_v2,
                       vol_g=vol_g, vol_s=vol_s, slope=slope,
                       cstar_hat=(d0 / slope) if slope > 0 else np.inf)

            # windowed replicas for rule 8 (Q4): everything rebuilt inside the window only
            for tag, sl in (("IS", slice(0, S.is_end)), ("OOS", slice(S.oos, None))):
                rgw, Cgw, rsw, Csw = rg0[sl], Cg[sl], rs0[sl], Cs[sl]
                sww, mew, t0w = sw[sl], me[sl], t0[sl]
                cw, dw = crossover(rgw, Cgw, rsw, Csw)
                vgw, vsw = fvol(rgw), fvol(rsw)
                rec[f"tax_{tag}"] = g * float(sww.mean())
                rec[f"drag_{tag}"] = float(Cgw.mean() - Csw.mean())
                rec[f"gate_turn_{tag}"] = float((mew * t0w).mean())
                rec[f"twin_turn_{tag}"] = float(Csw.mean())
                rec[f"T_panel_{tag}"] = float(base0[1.00][1][sl].mean())
                rec[f"T_panel_gross_{tag}"] = float(t0w.mean())
                rec[f"T_v2_panel_{tag}"] = float(ref0["v2"][1][sl].mean())
                rec[f"slope_{tag}"] = (252.0 / 1e4) * (float(Cgw.mean()) / vgw
                                                       - float(Csw.mean()) / vsw)
                rec[f"cstar_{tag}"] = cw
                rec[f"dSharpe_0_{tag}"] = dw
            rows.append(rec)

            for c in RUNGS:
                rg, rs = rg0 - Cg * c / 1e4, rs0 - Cs * c / 1e4
                pg, ps = pack(rg, S), pack(rs, S)
                b1, b2, bdd, bo, bocg, bodd = base_packs[c]
                s1, s2, so, sdd, scg, socg, sodd = spy_pack
                t4b = dict(H1=pg[3] > s1, H2=pg[4] > s2, OOS=pg[7] > so,
                           DD=abs(pg[2]) <= 0.60 * abs(sdd), CAGR=pg[0] >= 0.70 * scg)
                cells.append(dict(
                    panel=panel, rung=c, gross=g, family=fam, level=lev, w=w, depth=d,
                    cadence=cad, arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                    switch_tax=tax, drag=dr, cstar=cstar,
                    CAGR=pg[0], Sharpe=pg[1], MaxDD=pg[2], H1=pg[3], H2=pg[4], IS_Sharpe=pg[5],
                    OOS_CAGR=pg[6], OOS_Sharpe=pg[7], OOS_MaxDD=pg[8],
                    twin_Sharpe=ps[1], twin_OOS=ps[7],
                    dSharpe=pg[1] - ps[1], dOOS=pg[7] - ps[7],
                    win=bool(pg[1] - ps[1] > TIE),
                    v2_OOS_Sharpe=bo, v2_OOS_CAGR=bocg, v2_OOS_MaxDD=bodd,
                    spy_OOS_Sharpe=so, spy_OOS_CAGR=socg, spy_OOS_MaxDD=sodd,
                    p4a=bool(pg[3] > b1 and pg[4] > b2 and pg[2] >= bdd),
                    p4b=all(t4b.values()),
                    fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))

    # ---- reference rows (PROTOCOL rule 3/4: full sample + halves + OOS for every comparand)
    refs = []
    for c in RUNGS:
        for nm, (rr, tt) in list(ref0.items()) + [(f"NOGATE g{g:.2f}", base0[g]) for g in GROSSES]:
            p = pack(rr - tt * c / 1e4, S)
            refs.append(dict(panel=panel, rung=c, ref=nm, CAGR=p[0], Sharpe=p[1], MaxDD=p[2],
                             H1=p[3], H2=p[4], IS_Sharpe=p[5], OOS_CAGR=p[6], OOS_Sharpe=p[7],
                             OOS_MaxDD=p[8]))

    return pd.DataFrame(rows), pd.DataFrame(cells), pd.DataFrame(refs)


# ---------------------------------------------------------------- rho table helper
def rho_table(d, cstar_col, ncols, censor):
    """rho(normaliser, c*) by panel x family x normaliser on a censoring rule."""
    m = censor(d)
    out = []
    for pan in list(sorted(d["panel"].unique())) + ["POOLED"]:
        sub = d[m] if pan == "POOLED" else d[m & (d["panel"] == pan)]
        for fam in ["ABS", "QEXP", "QROLL", "ALL"]:
            s = sub if fam == "ALL" else sub[sub["family"] == fam]
            row = dict(panel=pan, family=fam, n=len(s))
            for nid in ncols.columns:
                row[nid] = spearman(ncols.loc[s.index, nid], s[cstar_col])
            out.append(row)
    return pd.DataFrame(out)


def main():
    log("=" * 185)
    log(f"Idea 608 does-the-TAX-to-c-star-rho-close-under-a-TURNOVER-NORMALISATION (lane C) | {SCRIPT}")
    log("=" * 185)
    log("Base book (idea 28/42/336/399's): EWALL(G) = equal weight every name above its own 200d")
    log("  MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.  Overlay: carry at (1-depth)")
    log("  whenever panel breadth is below the threshold.  Comparand: the MATCHED-MEAN-GROSS STATIC")
    log("  TWIN (EWALL at constant g_eff).  c* = the cost at which the gate stops beating its twin.")
    log("Tuned (2): NORMALISER in N0..N9 (all reported), PANEL in U56/B136/SMALL439/POOLED (all).")
    log("Never tuned: family, level, w, depth, gross, cadence, cost rung, censoring rule.")
    log("Pre-registered Q1 bar: CLOSES if a TURNOVER normaliser (N2-N6) reaches pooled |rho| >=")
    log("  0.80; PARTIAL if the best improves pooled |rho| by >= 0.15 over 0.5131; else REFUTED.")

    # =================================================================== [0] gates
    log("\n" + "=" * 185)
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
    for c in [0.0, 1.0, 5.0, 10.0, 25.0, 50.0, 100.0]:
        live = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=c,
                        freq=FREQ)["returns"].loc[st0:].values
        ref = me * live - sw * G_HEAD * c / 1e4                 # idea 399's apply_gate verbatim
        der = me * r0 - (me * t0 + G_HEAD * sw) * c / 1e4       # this run's derived ladder
        g1 = max(g1, float(np.abs(live - (r0 - t0 * c / 1e4)).max()),
                 float(np.abs(ref - der).max()))
    log(f"  G1 derived ladder == live backtest through apply_gate, 7 rungs: max |diff| = "
        f"{g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    rng = np.random.default_rng(608)
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

    parent = None
    if PARENT_DRAG.exists():
        parent = pd.read_csv(PARENT_DRAG)
        log(f"  G3/G4 source: idea 605 {PARENT_DRAG.name}, {len(parent)} arms")
        cen = np.isfinite(parent["cstar"]) & (parent["cstar"] > 0)
        log(f"  G4 idea 605's PUBLISHED rho(tax, c*) on its own censoring (finite c* AND c* > 0):")
        g4ok = True
        for k in ["POOLED", "ABS", "QEXP", "QROLL"]:
            s = parent[cen] if k == "POOLED" else parent[cen & (parent["family"] == k)]
            got = spearman(s["switch_tax"], s["cstar"])
            ok = abs(got - PUB605[k]) < 5e-5 and len(s) == PUB605_N[k]
            g4ok &= ok
            log(f"     {k:7s} n={len(s):4d} (published {PUB605_N[k]:4d})  rho {got:+.4f}  "
                f"(published {PUB605[k]:+.4f})  -> {'PASS' if ok else 'FAIL'}")
        log(f"  -> G4 {'PASS' if g4ok else 'FAIL'}")
        log(f"     censoring cost, stated once: idea 605's -0.5131 DROPS {int((~cen).sum())} of "
            f"{len(parent)} arms ({int((parent['cstar']==0).sum())} that already lose at 0 bps, "
            f"{int(np.isinf(parent['cstar']).sum())} that never lose out to {CSTAR_TOP:.0f} bps).")
    else:
        log("  G3/G4 source: idea 605 .drag.csv NOT FOUND -> G3/G4 cannot run")

    panels = [("U56", px0), ("B136", load_universe(broad=True))]
    ps, ndrop = small_panel()
    panels.append(("SMALL439", ps))
    log(f"  SMALL panel: dropped {ndrop} names with max_1d_move >= 1.0 -> {ps.shape[1]-1} names "
        f"+ SPY (idea 399/602/605's construction, so their rows join)")

    ROWS, CELLS, REFS = [], [], []
    for name, px in panels:
        d, c, rf = run_panel(name, px)
        ROWS.append(d)
        CELLS.append(c)
        REFS.append(rf)
    d = pd.concat(ROWS, ignore_index=True)
    cells = pd.concat(CELLS, ignore_index=True)
    refs = pd.concat(REFS, ignore_index=True)

    log("\n" + "=" * 185)
    log("[0b] G3 / G5 / G7")
    g3max = np.nan
    if parent is not None:
        key = ["panel", "gross", "family", "level", "w", "depth", "cadence"]
        a, b = d.copy(), parent.copy()
        for f in (a, b):
            for k in ("gross", "level", "w", "depth"):
                f[k] = f[k].astype(float).round(6)
        j = a.merge(b, on=key, suffixes=("", "_605"))
        cols = ["switch_tax", "timing", "drag", "dSharpe_0", "g_eff", "on_share", "switch_per_yr"]
        diffs = {c: float((j[c] - j[c + "_605"]).abs().max()) for c in cols}
        fin = np.isfinite(j["cstar"]) & np.isfinite(j["cstar_605"])
        diffs["cstar(finite)"] = float((j.loc[fin, "cstar"] - j.loc[fin, "cstar_605"]).abs().max())
        same_inf = bool((np.isinf(j["cstar"]) == np.isinf(j["cstar_605"])).all())
        g3max = max(diffs.values())
        log(f"  G3 idea 605 join: {len(j)} of {len(parent)} arms matched on {key}")
        log("     max |diff|: " + "  ".join(f"{k} {v:.3e}" for k, v in diffs.items())
            + f"   +inf set identical: {same_inf}")
        log(f"  -> G3 {'PASS' if (g3max < 1e-9 and same_inf and len(j) == len(parent)) else 'FAIL'}"
            f" (bar 1e-9)")
    g5 = float(d["resid"].abs().max())
    log(f"  G5 drag identity DRAG == SWITCH_TAX + TIMING on {len(d)} arms: max |resid| {g5:.3e} "
        f"(bar 1e-15) -> {'PASS' if g5 < 1e-15 else 'FAIL'}")

    kk = ["panel", "family", "level", "w", "depth", "cadence"]
    pv_tax = d.pivot_table(index=kk, columns="gross", values="switch_tax")
    ratio = (pv_tax[1.00] / pv_tax[0.75])
    pv_cs = d.pivot_table(index=kk, columns="gross", values="cstar").replace(np.inf, np.nan)
    pv_ds = d.pivot_table(index=kk, columns="gross", values="dSharpe_0")
    cs_pairs = pv_cs.dropna()
    g7 = float((ratio - 4.0 / 3.0).abs().max())
    log(f"  G7 GROSS SCALING.  tax(g=1.00)/tax(g=0.75): max |ratio - 4/3| = {g7:.3e} -> "
        f"{'PASS' if g7 < 1e-9 else 'FAIL'} (the tax scales EXACTLY with gross)")
    log(f"     while c* does not: over {len(cs_pairs)} finite pairs max |c*(0.75) - c*(1.00)| = "
        f"{float((cs_pairs[0.75]-cs_pairs[1.00]).abs().max()):.4f} bps, median "
        f"{float((cs_pairs[0.75]-cs_pairs[1.00]).abs().median()):.4f}; max |dSharpe_0 diff| "
        f"{float((pv_ds[0.75]-pv_ds[1.00]).abs().max()):.3e}")
    log("     => the raw tax carries a 1.333x axis that c* is nearly blind to.  That is a UNITS")
    log("        artefact sitting inside idea 605's pooled -0.5131, and it is exactly what a")
    log("        base-turnover normalisation cancels (base turnover scales with gross too).")

    N = norm_values(d)
    d.to_csv(OUT / f"{STEM}.arms.csv.gz", index=False)
    pd.concat([d[["panel", "family", "arm", "cstar", "dSharpe_0"]], N], axis=1).to_csv(
        OUT / f"{STEM}.norms.csv", index=False)
    cells.to_csv(OUT / f"{STEM}.cells.csv.gz", index=False)

    log("\n" + "=" * 185)
    log(f"POPULATION: {len(d)} twin-pair arms (3 panels x 18 level-arms x 3 depths x 2 cadences x "
        f"2 gross), each carrying an exact c* on the derived ladder.")
    log(f"  c* distribution: {int((d['cstar']==0).sum())} at 0 (lose before a bp is charged), "
        f"{int(np.isinf(d['cstar']).sum())} infinite (never lose to {CSTAR_TOP:.0f} bps), "
        f"{int((np.isfinite(d['cstar'])&(d['cstar']>0)).sum())} strictly inside.")
    log("\n  the normaliser ladder (tuned param 1), and what each divides the tax by:")
    for nid, lab, by, num in NORMALISERS:
        log(f"    {nid}  {lab:32s} numerator {num:10s} denominator: {by}")
    log("\n  base-turnover levels actually used (per panel, per day and annualised):")
    lev = d.groupby("panel")[["T_panel", "T_v2_panel"]].first()
    lev["EWALL_pct_yr"] = lev["T_panel"] * 252
    lev["v2_pct_yr"] = lev["T_v2_panel"] * 252
    lev["ratio_hi_lo"] = lev["T_panel"] / lev["T_panel"].min()
    log(lev.to_string(float_format=lambda x: f"{x:.4f}"))

    # =============================================================== [1] Q1
    log("\n" + "=" * 185)
    log("[1] Q1 - THE QUEUE'S TEST.  rho(normaliser, c*) on idea 605's OWN censoring rule")
    log("    (finite c* AND c* > 0, n = 494), every normaliser x every panel x every family.")
    cen605 = lambda f: np.isfinite(f["cstar"]) & (f["cstar"] > 0)
    R = rho_table(d, "cstar", N, cen605)
    R.to_csv(OUT / f"{STEM}.rho.csv", index=False)
    log(R.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    pooled = R[(R["panel"] == "POOLED") & (R["family"] == "ALL")].iloc[0]
    raw = float(pooled["N0"])
    log(f"\n  POOLED / ALL, restated as a ladder in |rho| (idea 605's number is N0 = {raw:+.4f}):")
    for nid, lab, _, _ in NORMALISERS:
        v = float(pooled[nid])
        mark = "  <- the queue's proposal" if nid in TURNOVER_NORMS else (
            "  <- analytic control" if nid == "N9" else "")
        log(f"    {nid}  |rho| {abs(v):.4f}  (rho {v:+.4f})  d|rho| vs N0 "
            f"{abs(v)-abs(raw):+.4f}   {lab}{mark}")
    best_t = max(TURNOVER_NORMS, key=lambda k: abs(float(pooled[k])))
    best_abs = abs(float(pooled[best_t]))
    gain = best_abs - abs(raw)
    verdict_q1 = ("CLOSES" if best_abs >= 0.80 else
                  "PARTIAL" if gain >= 0.15 else "REFUTED")
    log(f"\n  best TURNOVER normaliser: {best_t} at |rho| {best_abs:.4f} "
        f"(N0 {abs(raw):.4f}, gain {gain:+.4f}) -> pre-registered verdict: **{verdict_q1}**")
    log(f"  analytic control N9: |rho| {abs(float(pooled['N9'])):.4f}")

    # =============================================================== [2] Q2 invariance
    log("\n" + "=" * 185)
    log("[2] Q2 - THE INVARIANCE (G6).  A normaliser constant inside a group cannot move that")
    log("    group's Spearman.  Max |rho_N - rho_N0| within panel x gross, per normaliser:")
    inv = []
    m = cen605(d)
    groups = list(d[m].groupby(["panel", "gross"]))
    for nid, lab, _, _ in NORMALISERS:
        worst, worstg, spread = 0.0, None, 0.0
        for (pan, g), s in groups:
            a = spearman(N.loc[s.index, "N0"], s["cstar"])
            b = spearman(N.loc[s.index, nid], s["cstar"])
            if np.isfinite(a) and np.isfinite(b) and abs(a - b) > worst:
                worst, worstg = abs(a - b), f"{pan}/g{g:.2f}"
            den = N.loc[s.index, nid] / N.loc[s.index, "N0"]      # the divisor itself
            den = den[np.isfinite(den)]
            if len(den):
                spread = max(spread, float((den.max() - den.min())
                                           / max(abs(den.median()), 1e-18)))
        inv.append(dict(norm=nid, label=lab, max_drho_within_panel_gross=worst,
                        where=worstg, rel_spread_vs_N0_in_group=spread))
    inv = pd.DataFrame(inv)
    log(inv.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    g6 = float(inv.loc[inv["norm"].isin(["N1", "N2", "N3", "N6"]),
                       "max_drho_within_panel_gross"].max())
    log(f"  -> G6 {'PASS' if g6 < 1e-12 else 'FAIL'} (bar 1e-12): every GROUP-CONSTANT normaliser")
    log("     (N1 gross, N2 panel, N3 panel x gross, N6 RULES v2 per panel) leaves the within-")
    log("     panel-x-gross rho BIT-IDENTICAL.  Only the arm-level ones (N4/N5/N7/N8/N9) can move")
    log("     it.  So the queue's per-panel normalisation is a POOLED-ONLY instrument by")
    log("     construction - it re-scales the tax across panels and does nothing inside one.")
    log("\n  per-panel-x-gross rho(tax, c*), which no per-panel normaliser can change:")
    pg = []
    for (pan, g), s in d[m].groupby(["panel", "gross"]):
        pg.append(dict(panel=pan, gross=g, n=len(s),
                       rho_tax=spearman(N.loc[s.index, "N0"], s["cstar"]),
                       rho_drag=spearman(N.loc[s.index, "N7"], s["cstar"]),
                       rho_N9=spearman(N.loc[s.index, "N9"], s["cstar"])))
    log(pd.DataFrame(pg).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== [3] Q3 what is left
    log("\n" + "=" * 185)
    log("[3] Q3 - WHAT THE NORMALISATION CANNOT REACH.  c* ~= dSharpe_0 / SLOPE, so a tax-only")
    log("    statistic is missing the NUMERATOR.  Accuracy of that approximation first:")
    fin = d[m]
    log(f"    rho(c*_hat, c*) = {spearman(fin['cstar_hat'], fin['cstar']):+.6f} on {len(fin)} arms;"
        f" median |c*_hat/c* - 1| = {float(((fin['cstar_hat']/fin['cstar'])-1).abs().median()):.4f}")
    log("\n    the three ingredients, each against c*:")
    for lab, v in [("switch_tax", fin["switch_tax"]), ("drag", fin["drag"]),
                   ("SLOPE (vol-normalised drag)", fin["slope"]),
                   ("dSharpe_0 (the EDGE)", fin["dSharpe_0"]),
                   ("SLOPE / dSharpe_0", fin["slope"] / fin["dSharpe_0"])]:
        log(f"      rho({lab:28s}, c*) = {spearman(v, fin['cstar']):+.4f}")
    log("\n    conditioning on the EDGE instead of dividing by turnover - rho(tax, c*) inside")
    log("    dSharpe_0 quintiles (equal-count, pooled):")
    q = pd.qcut(fin["dSharpe_0"], 5, labels=False, duplicates="drop")
    qt = []
    for b in sorted(pd.Series(q).dropna().unique()):
        s = fin[q == b]
        qt.append(dict(edge_quintile=int(b) + 1, n=len(s),
                       edge_lo=float(s["dSharpe_0"].min()), edge_hi=float(s["dSharpe_0"].max()),
                       rho_tax=spearman(s["switch_tax"], s["cstar"]),
                       rho_taxT=spearman(s["switch_tax"] / s["T_panel_gross"], s["cstar"]),
                       rho_slope=spearman(s["slope"], s["cstar"])))
    qt = pd.DataFrame(qt)
    log(qt.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    log(f"    mean within-edge-quintile rho(tax, c*) = {qt['rho_tax'].mean():+.4f} vs pooled "
        f"{raw:+.4f}; the same for the normalised tax = {qt['rho_taxT'].mean():+.4f}")

    log("\n    the same question asked of the CENSORING rule, never tuned, all four reported:")
    cens = [("605 (0 < c* < inf)", cen605),
            ("finite only (c* >= 0)", lambda f: np.isfinite(f["cstar"])),
            ("all arms, +inf ranked top", lambda f: f["cstar"].notna()),
            ("strictly inside 0-100 bps", lambda f: np.isfinite(f["cstar"]) & (f["cstar"] > 0)
             & (f["cstar"] <= 100.0))]
    ct = []
    for lab, fn in cens:
        s = d[fn(d)]
        row = dict(censoring=lab, n=len(s))
        for nid in ["N0", "N3", "N5", "N7", "N9"]:
            row[nid] = spearman(N.loc[s.index, nid], s["cstar"])
        ct.append(row)
    ct = pd.DataFrame(ct)
    ct.to_csv(OUT / f"{STEM}.censor.csv", index=False)
    log(ct.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # =============================================================== [4] Q4 rule 8 on the claim
    log("\n" + "=" * 185)
    log("[4] Q4 - RULE 8 ON THE CLAIM.  Everything (tax, drag, slope, edge, c*) rebuilt inside")
    log(f"    the IS window (<= {IS_END}) only; the normaliser is PICKED on IS by |rho| and read")
    log(f"    ONCE on OOS ({OOS_START}+).  Every normaliser's OOS rho reported regardless.")
    wf = []
    for tag in ("IS", "OOS"):
        dd = d.copy()
        for c in ["switch_tax", "drag", "gate_turn", "twin_turn", "T_panel", "T_panel_gross",
                  "T_v2_panel", "slope", "cstar", "dSharpe_0"]:
            src = ("tax_" + tag) if c == "switch_tax" else f"{c}_{tag}"
            dd[c] = d[src]
        Nw = norm_values(dd)
        sel = np.isfinite(dd["cstar"]) & (dd["cstar"] > 0)
        row = dict(window=tag, n=int(sel.sum()))
        for nid in N.columns:
            row[nid] = spearman(Nw.loc[dd.index[sel], nid], dd.loc[sel, "cstar"])
        wf.append(row)
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log(wf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    isrow, oosrow = wf.iloc[0], wf.iloc[1]
    pick = max(N.columns, key=lambda k: abs(float(isrow[k])) if np.isfinite(isrow[k]) else -1)
    pick_t = max(TURNOVER_NORMS, key=lambda k: abs(float(isrow[k])))
    log(f"\n    IS pick over ALL normalisers: {pick} (|rho_IS| {abs(float(isrow[pick])):.4f}) "
        f"-> read once OOS: rho {float(oosrow[pick]):+.4f} (|rho| {abs(float(oosrow[pick])):.4f})")
    log(f"    IS pick restricted to the queue's TURNOVER normalisers: {pick_t} "
        f"(|rho_IS| {abs(float(isrow[pick_t])):.4f}) -> OOS rho {float(oosrow[pick_t]):+.4f}")
    log(f"    the comparand it must beat, N0 raw tax: IS {float(isrow['N0']):+.4f} -> OOS "
        f"{float(oosrow['N0']):+.4f}")
    q4 = abs(float(oosrow[pick_t])) - abs(float(oosrow["N0"]))
    log(f"    OOS gain of the IS-picked turnover normaliser over the raw tax: {q4:+.4f}")

    # =============================================================== [5] Q5 PROTOCOL
    log("\n" + "=" * 185)
    log("[5] Q5 - PROTOCOL.  Both KEEP paths on all arms at rungs 0/10/25, then the rule-8 book")
    log("    chooser (IS Sharpe pick, OOS read once) against RULES v2 and SPY.")
    log(f"    4a passes: " + "  ".join(
        f"{c:.0f}bps {int(cells[cells['rung']==c]['p4a'].sum())}/{int((cells['rung']==c).sum())}"
        for c in RUNGS))
    log(f"    4b passes: " + "  ".join(
        f"{c:.0f}bps {int(cells[cells['rung']==c]['p4b'].sum())}/{int((cells['rung']==c).sum())}"
        for c in RUNGS))
    h = cells[cells["rung"] == RUNG_HEAD]
    log(f"    at PROTOCOL's own {RUNG_HEAD:.0f} bps: 4a {int(h['p4a'].sum())}, 4b "
        f"{int(h['p4b'].sum())} of {len(h)}; dominant 4b failure legs: "
        + ", ".join(f"{k} {v}" for k, v in h["fail4b"].value_counts().head(4).items()))

    picks = []
    for (pan, fam, cad, c), s in cells[cells["gross"] == G_HEAD].groupby(
            ["panel", "family", "cadence", "rung"]):
        p = s.loc[s["IS_Sharpe"].idxmax()]
        best = s.loc[s["OOS_Sharpe"].idxmax()]
        picks.append(dict(panel=pan, family=fam, cadence=cad, rung=c, pick=p["arm"],
                          IS_Sharpe=p["IS_Sharpe"], OOS_CAGR=p["OOS_CAGR"],
                          OOS_Sharpe=p["OOS_Sharpe"], OOS_MaxDD=p["OOS_MaxDD"],
                          v2_OOS_Sharpe=p["v2_OOS_Sharpe"], v2_OOS_CAGR=p["v2_OOS_CAGR"],
                          v2_OOS_MaxDD=p["v2_OOS_MaxDD"], spy_OOS_Sharpe=p["spy_OOS_Sharpe"],
                          spy_OOS_CAGR=p["spy_OOS_CAGR"], spy_OOS_MaxDD=p["spy_OOS_MaxDD"],
                          beats_v2=bool(p["OOS_Sharpe"] > p["v2_OOS_Sharpe"]),
                          beats_spy=bool(p["OOS_Sharpe"] > p["spy_OOS_Sharpe"]),
                          p4a=bool(p["p4a"]), p4b=bool(p["p4b"]), fail4b=p["fail4b"],
                          regret=p["OOS_Sharpe"] - best["OOS_Sharpe"]))
    picks = pd.DataFrame(picks)
    picks.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    log(f"\n    {len(picks)} rule-8 picks (panel x family x cadence x rung, gross {G_HEAD}):")
    agg = picks.groupby("rung").agg(n=("pick", "size"), beats_v2=("beats_v2", "sum"),
                                    beats_spy=("beats_spy", "sum"), p4a=("p4a", "sum"),
                                    p4b=("p4b", "sum"),
                                    mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                                    mean_OOS_CAGR=("OOS_CAGR", "mean"),
                                    mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                                    mean_regret=("regret", "mean"))
    log(agg.to_string(float_format=lambda x: f"{x:+.4f}"))
    refs.to_csv(OUT / f"{STEM}.refs.csv", index=False)
    log(f"\n    PROTOCOL rule 3/4 reference table at {RUNG_HEAD:.0f} bps "
        f"(full sample, then halves, then OOS):")
    log(refs[refs["rung"] == RUNG_HEAD].set_index(["panel", "ref"])[
        ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    ].to_string(float_format=lambda x: f"{x:+.4f}"))

    hp = picks[picks["rung"] == RUNG_HEAD]
    hcells = cells[(cells["rung"] == RUNG_HEAD) & (cells["gross"] == G_HEAD)]
    log(f"\n    and the {RUNG_HEAD:.0f}-bps rule-8 PICKS on the same columns:")
    log(hcells.merge(hp[["panel", "family", "cadence", "pick"]],
                     left_on=["panel", "family", "cadence", "arm"],
                     right_on=["panel", "family", "cadence", "pick"])
        .set_index(["panel", "family", "cadence"])[
            ["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
        ].to_string(float_format=lambda x: f"{x:+.4f}"))
    log(f"\n    at {RUNG_HEAD:.0f} bps, per panel, the picked arm's OOS vs its comparands:")
    log(hp.groupby("panel")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "v2_OOS_CAGR",
                             "v2_OOS_Sharpe", "v2_OOS_MaxDD", "spy_OOS_CAGR", "spy_OOS_Sharpe",
                             "spy_OOS_MaxDD"]].mean().to_string(
        float_format=lambda x: f"{x:+.4f}"))
    log(f"    4a at {RUNG_HEAD:.0f} bps among picks: {int(hp['p4a'].sum())}/{len(hp)}; "
        f"4b {int(hp['p4b'].sum())}/{len(hp)}; beats RULES v2 OOS {int(hp['beats_v2'].sum())}; "
        f"beats SPY OOS {int(hp['beats_spy'].sum())}")

    # =============================================================== [6] summary
    log("\n" + "=" * 185)
    log("[6] SUMMARY")
    log(f"  gates: G1 {g1:.2e} | G2 {g2:.2e} | G3 {g3max:.2e} | G4 see [0] | G5 {g5:.2e} | "
        f"G6 {g6:.2e} | G7 {g7:.2e}")
    log(f"  Q1 pooled |rho|: N0 raw {abs(raw):.4f} -> best turnover normaliser {best_t} "
        f"{best_abs:.4f} (gain {gain:+.4f}) -> **{verdict_q1}**")
    log(f"  Q1 analytic control N9 (SLOPE / dSharpe_0): |rho| {abs(float(pooled['N9'])):.4f}")
    log(f"  Q2 invariance: group-constant normalisers move the within-panel-x-gross rho by "
        f"{g6:.1e} -> the queue's instrument is pooled-only by construction")
    log(f"  Q3 rho(SLOPE, c*) {spearman(fin['slope'], fin['cstar']):+.4f}; "
        f"rho(dSharpe_0, c*) {spearman(fin['dSharpe_0'], fin['cstar']):+.4f}; "
        f"mean within-edge-quintile rho(tax, c*) {qt['rho_tax'].mean():+.4f}")
    log(f"  Q4 rule 8 on the claim: IS pick {pick_t} of the turnover set -> OOS "
        f"{float(oosrow[pick_t]):+.4f} vs raw tax OOS {float(oosrow['N0']):+.4f} (gain {q4:+.4f})")
    log(f"  Q5 4a {int(h['p4a'].sum())} / 4b {int(h['p4b'].sum())} of {len(h)} at 10 bps; "
        f"rule-8 picks beating RULES v2 OOS {int(hp['beats_v2'].sum())}/{len(hp)}, SPY "
        f"{int(hp['beats_spy'].sum())}/{len(hp)}")
    log("  Nothing promoted; no RULES change proposed by this run.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.{{arms,norms,rho,censor,walkforward,picks,cells,console}}")


if __name__ == "__main__":
    main()
