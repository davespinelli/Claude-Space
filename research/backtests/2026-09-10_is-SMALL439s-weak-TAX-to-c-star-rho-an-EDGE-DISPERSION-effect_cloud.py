#!/usr/bin/env python3
"""Idea 610 - "is-SMALL439s-weak-TAX-to-c-star-rho-an-EDGE-DISPERSION-effect" (cloud).

What this run exists to settle
------------------------------
Idea 608 reported, on the same 648 twin-pair arms idea 605 published,

    rho(switch_tax, c*)   U56 -0.755   B136 -0.724   SMALL439 -0.297   POOLED -0.5131

and separately that conditioning the POOLED number on dSharpe_0 quintiles lifts it from -0.5131
to a mean within-quintile -0.8413.  The queue's hypothesis is that these are the same fact: that
SMALL439 is the weak panel BECAUSE its arms' zero-cost edges are more dispersed, so conditioning
on the edge should close SMALL439's gap to the other two.

The algebra says exactly where to look.  Idea 608 established the closed form

    c* = dSharpe_0 / SLOPE      (rho +0.99986, median level error 0.55%)

so, on the arms where both sides are positive,

    log c* = log dSharpe_0 - log SLOPE  ==  E - S.

The tax orders c* through TWO legs and only two:

    (a) the PROXY leg      how well the tax stands in for SLOPE, i.e. rho(tax, S);
    (b) the CONTAMINATION  how much the numerator E moves log c* against S, i.e. the share of
        leg                Var(log c*) that E contributes.

The queue's hypothesis is a claim about (b) alone.  It is testable without any conditioning at
all, because SLOPE is the EXACT denominator of c* - no proxy error whatsoever - so

    rho(SLOPE, c*) per panel isolates leg (b) with leg (a) held at its ceiling.

That gives a decisive fork, pre-registered below:

    if SMALL439's rho(SLOPE, c*) is the weak one    -> the edge IS the contaminant   (CONFIRMED)
    if rho(SLOPE, c*) is flat across panels and it is rho(tax, SLOPE) that collapses on SMALL439
                                                    -> the tax is a worse PROXY there (REFUTED,
                                                       and the real cause is named)

The conditioning experiment the queue asks for is then run per panel on top of it, over a ladder
of bin counts, with a RANDOM-BIN control at every count so the lift can be read against the floor
that binning alone produces.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (THE QUEUE'S)  Per panel x bin count K, mean within-edge-bin rho(tax, c*).  Pre-registered
                      on SMALL439, whose raw |rho| is 0.297 and whose gap to the best panel
                      (U56, 0.755) is 0.458:
                        CLOSES   if some K gives SMALL439 mean within-bin |rho| >= 0.60 AND cuts
                                 the three-panel spread of |rho| by >= 50% (to <= 0.229)
                        PARTIAL  if either half holds alone (SMALL439 gains >= 0.15, or the
                                 spread falls >= 25%)
                        REFUTED  if neither
    Q2 (THE FLOOR)    The same statistic on bins drawn at random (same sizes, 200 draws per panel
                      per K).  A lift inside the random-bin band is a binning artefact, not an
                      edge effect.
    Q3 (THE FORK)     Per panel: rho(SLOPE, c*) - the contamination leg with the proxy leg
                      perfect - and rho(tax, SLOPE) - the proxy leg with the numerator removed.
                      Plus the variance decomposition of log c* = E - S into Var(E), Var(S),
                      -2Cov(E,S) and the EDGE SHARE Var(E)/(Var(E)+Var(S)).  The queue's premise
                      requires SMALL439 to carry the largest edge share.
    Q4 (RULE 8)       Every quantity rebuilt inside the IS window (<= 2016-12-31) only, K PICKED
                      on IS per panel by mean within-bin |rho|, read ONCE on OOS (2017+).  Every
                      K's OOS number reported regardless.
    Q5 (PROTOCOL)     Both KEEP paths on every arm at rungs 0/10/25, and the rule-8 book chooser
                      (IS Sharpe pick, OOS read once) with OOS CAGR/Sharpe/MaxDD against the live
                      RULES v2 baseline and SPY.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. panel     U56 / B136 / SMALL439 / POOLED, all reported everywhere, never selected on.
    2. bin count K in {2,3,4,5,6,8,10}, ALL reported at every panel, selected on only in Q4 and
                 there on the IS window alone.
Reported axes, NEVER tuned: family, level, w, depth, gross, cadence, cost rung, censoring rule.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived ladder r_gate(c) = m*r0 - (c/1e4)*(m*t0 + g*|dm|) vs a LIVE engine.backtest put
        through idea 399's own apply_gate, at every rung.  Bar 1e-12.
    G2  fast numpy CAGR/Sharpe/MaxDD vs engine.metrics on 200 real series.  Bar 1e-12.
    G3  idea 608's COMMITTED .arms.csv.gz, all 648 arms joined on every shared column.  Bar 1e-9.
    G4  idea 608's PUBLISHED per-panel rho(tax, c*) -0.755 / -0.724 / -0.297, its pooled -0.5131,
        and its pooled mean-within-quintile -0.8413, all on its own censoring rule.
    G5  the drag identity DRAG == SWITCH_TAX + TIMING on all 648 arms.  Bar 1e-15.
    G6  the closed form: rho(dSharpe_0/SLOPE, c*) >= 0.999 on the strictly-inside population, so
        the E - S decomposition Q3 rests on is the same object as the measured c*.

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is optimistic; SMALL439 in
particular is a screen of names that exist today.  Every claim this run makes is a rank statistic
comparing arms WITHIN a fixed panel, which a common level shift does not move - but the
cross-panel comparison at the heart of Q1/Q3 does inherit whatever differential the three
screens' survivorship carries, and that caveat is restated in the memo.  SMALL439 starts
2010-01-04 and drops names with max_1d_move >= 1.0 per data/small_meta.csv.

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
PARENT_ARMS = OUT / ("2026-09-10_does-the-TAX-to-c-star-rho-close-under-a-"
                     "TURNOVER-NORMALISATION_C.arms.csv.gz")

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
GSTEP = 0.01
CSTAR_TOP = 500.0

KS = [2, 3, 4, 5, 6, 8, 10]          # tuned param 2, all reported
NDRAW = 200                          # random-bin control draws
SEED = 610

# idea 608's published headlines, for G4
PUB608_PANEL = {"U56": -0.755, "B136": -0.724, "SMALL439": -0.297}
PUB608_POOLED = -0.5131
PUB608_QUINT = -0.8413

# pre-registered Q1 bars (stated before anything is read)
RAW_SMALL = 0.297
RAW_SPREAD = 0.755 - 0.297
BAR_CLOSES_LEVEL = 0.60
BAR_CLOSES_SPREAD = 0.50 * RAW_SPREAD
BAR_PARTIAL_GAIN = 0.15
BAR_PARTIAL_SPREAD = 0.75 * RAW_SPREAD

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
    """Idea 605/608's helper verbatim (+inf is notna and ranks largest)."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def crossover(rg0, Cg, rs0, Cs):
    """c* on the exact derived ladder (idea 605/608's, verbatim)."""
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

    T_panel = float(base0[1.00][1].mean())
    T_gross = {g: float(base0[g][1].mean()) for g in GROSSES}
    T_v2 = float(ref0["v2"][1].mean())

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
                    switch_tax=tax, drag=dr, cstar=cstar, dSharpe_0=d0, slope=slope,
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

    refs = []
    for c in RUNGS:
        for nm, (rr, tt) in list(ref0.items()) + [(f"NOGATE g{g:.2f}", base0[g]) for g in GROSSES]:
            p = pack(rr - tt * c / 1e4, S)
            refs.append(dict(panel=panel, rung=c, ref=nm, CAGR=p[0], Sharpe=p[1], MaxDD=p[2],
                             H1=p[3], H2=p[4], IS_Sharpe=p[5], OOS_CAGR=p[6], OOS_Sharpe=p[7],
                             OOS_MaxDD=p[8]))

    return pd.DataFrame(rows), pd.DataFrame(cells), pd.DataFrame(refs)


# ---------------------------------------------------------------- the conditioning statistic
def within_bin_rho(sub, bins, xcol, ycol):
    """Mean and n-weighted-mean within-bin Spearman, plus the per-bin table."""
    out = []
    for b in sorted(pd.Series(bins).dropna().unique()):
        s = sub[bins == b]
        out.append(dict(bin=int(b) + 1, n=len(s), rho=spearman(s[xcol], s[ycol])))
    t = pd.DataFrame(out)
    ok = t["rho"].notna()
    if not ok.any():
        return np.nan, np.nan, t
    plain = float(t.loc[ok, "rho"].mean())
    wt = float((t.loc[ok, "rho"] * t.loc[ok, "n"]).sum() / t.loc[ok, "n"].sum())
    return plain, wt, t


def edge_bins(sub, K, col="dSharpe_0"):
    return pd.qcut(sub[col], K, labels=False, duplicates="drop")


def random_bins(n, sizes, rng):
    """A permutation of the same bin SIZES over n rows - the binning-only null."""
    lab = np.concatenate([np.full(s, i) for i, s in enumerate(sizes)])
    rng.shuffle(lab)
    return pd.Series(lab[:n])


def main():
    log("=" * 185)
    log(f"Idea 610 is-SMALL439s-weak-TAX-to-c-star-rho-an-EDGE-DISPERSION-effect (cloud) | {SCRIPT}")
    log("=" * 185)
    log("Base book (idea 28/42/336/399's): EWALL(G) = equal weight every name above its own 200d")
    log("  MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.  Overlay: carry at (1-depth)")
    log("  whenever panel breadth is below the threshold.  Comparand: the MATCHED-MEAN-GROSS STATIC")
    log("  TWIN (EWALL at constant g_eff).  c* = the cost at which the gate stops beating its twin.")
    log("Tuned (2): PANEL in U56/B136/SMALL439/POOLED (all reported), BIN COUNT K in "
        f"{KS} (all reported).")
    log("Never tuned: family, level, w, depth, gross, cadence, cost rung, censoring rule.")
    log(f"Pre-registered Q1 bar on SMALL439 (raw |rho| {RAW_SMALL:.3f}, panel spread "
        f"{RAW_SPREAD:.3f}):")
    log(f"  CLOSES  mean within-bin |rho| >= {BAR_CLOSES_LEVEL:.2f} AND spread <= "
        f"{BAR_CLOSES_SPREAD:.3f}")
    log(f"  PARTIAL SMALL439 gains >= {BAR_PARTIAL_GAIN:.2f} OR spread <= {BAR_PARTIAL_SPREAD:.3f}")
    log("  REFUTED otherwise.  Q2 requires any lift to clear the RANDOM-BIN band as well.")

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
        ref = me * live - sw * G_HEAD * c / 1e4
        der = me * r0 - (me * t0 + G_HEAD * sw) * c / 1e4
        g1 = max(g1, float(np.abs(live - (r0 - t0 * c / 1e4)).max()),
                 float(np.abs(ref - der).max()))
    log(f"  G1 derived ladder == live backtest through apply_gate, 7 rungs: max |diff| = "
        f"{g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    rng0 = np.random.default_rng(SEED)
    g2 = 0.0
    for _ in range(200):
        c = float(rng0.uniform(0, 100))
        a, b = sorted(rng0.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        s = pd.Series((r0 - t0 * c / 1e4)[a:b], index=idx0[a:b])
        mm, f = metrics(s), fmet(s.values)
        g2 = max(g2, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G2 fast metrics vs engine.metrics on 200 series: max |diff| = {g2:.3e} "
        f"(bar 1e-12) -> {'PASS' if g2 < 1e-12 else 'FAIL'}")

    parent = pd.read_csv(PARENT_ARMS) if PARENT_ARMS.exists() else None
    if parent is None:
        log("  G3/G4 source: idea 608 .arms.csv.gz NOT FOUND -> G3/G4 cannot run")
    else:
        log(f"  G3/G4 source: idea 608 {PARENT_ARMS.name}, {len(parent)} arms")
        cen = np.isfinite(parent["cstar"]) & (parent["cstar"] > 0)
        log("  G4 idea 608's PUBLISHED rho(tax, c*) on its own censoring (finite c* AND c* > 0).")
        log("     PROVENANCE CHECK: the queue quotes -0.755 / -0.724 / -0.297 as 'per panel'.")
        log("     Read on the whole panel (both grosses) idea 608's OWN .rho.csv says otherwise;")
        log("     the quoted triple is its g=0.75 SLICE.  Both readings are printed and the gate")
        log("     is PASSed on whichever reproduces, with the mismatch reported as a correction.")
        g4ok = True
        for k in ["U56", "B136", "SMALL439"]:
            s = parent[cen & (parent["panel"] == k)]
            got = spearman(s["switch_tax"], s["cstar"])
            s75 = s[s["gross"] == G_HEAD]
            got75 = spearman(s75["switch_tax"], s75["cstar"])
            hit = ("g=0.75 slice" if abs(got75 - PUB608_PANEL[k]) < 1e-3
                   else ("whole panel" if abs(got - PUB608_PANEL[k]) < 1e-3 else "NEITHER"))
            g4ok &= hit != "NEITHER"
            log(f"     {k:9s} whole panel n={len(s):4d} rho {got:+.4f} | g=0.75 n={len(s75):3d} "
                f"rho {got75:+.4f} | published {PUB608_PANEL[k]:+.3f} -> reproduced by the "
                f"{hit} -> {'PASS' if hit != 'NEITHER' else 'FAIL'}")
        log("     CORRECTION for the record: idea 608's per-panel triple is a g=0.75 reading; the")
        log("     whole-panel numbers are -0.7436 / -0.7123 / -0.2741 (its own .rho.csv).  The")
        log("     gap is <= 0.023 and moves no verdict here - the pre-registered bars below were")
        log("     set on the QUOTED 0.297 / 0.458 and are NOT restated after the fact.")
        sp = parent[cen]
        gotp = spearman(sp["switch_tax"], sp["cstar"])
        okp = abs(gotp - PUB608_POOLED) < 5e-5
        g4ok &= okp
        log(f"     {'POOLED':9s} n={len(sp):4d}  rho {gotp:+.4f}  (published "
            f"{PUB608_POOLED:+.4f})  -> {'PASS' if okp else 'FAIL'}")
        q5 = edge_bins(sp, 5)
        m5, _, _ = within_bin_rho(sp, q5, "switch_tax", "cstar")
        okq = abs(m5 - PUB608_QUINT) < 1e-3
        g4ok &= okq
        log(f"     pooled mean within-dSharpe_0-QUINTILE rho {m5:+.4f}  (published "
            f"{PUB608_QUINT:+.4f})  -> {'PASS' if okq else 'FAIL'}")
        log(f"  -> G4 {'PASS' if g4ok else 'FAIL'}")
        log(f"     censoring cost, stated once (idea 612's worry): the -0.5131 population DROPS "
            f"{int((~cen).sum())} of {len(parent)} arms "
            f"({int((parent['cstar']==0).sum())} losing at 0 bps, "
            f"{int(np.isinf(parent['cstar']).sum())} never losing to {CSTAR_TOP:.0f} bps). "
            f"Every table below is reported on BOTH populations.")

    panels = [("U56", px0), ("B136", load_universe(broad=True))]
    ps, ndrop = small_panel()
    panels.append(("SMALL439", ps))
    log(f"  SMALL panel: dropped {ndrop} names with max_1d_move >= 1.0 -> {ps.shape[1]-1} names "
        f"+ SPY (idea 399/602/605/608's construction, so their rows join)")

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
    log("[0b] G3 / G5 / G6")
    g3max = np.nan
    if parent is not None:
        key = ["panel", "gross", "family", "level", "w", "depth", "cadence"]
        a, b = d.copy(), parent.copy()
        for f in (a, b):
            for k in ("gross", "level", "w", "depth"):
                f[k] = f[k].astype(float).round(6)
        j = a.merge(b, on=key, suffixes=("", "_608"))
        cols = ["switch_tax", "timing", "drag", "dSharpe_0", "g_eff", "on_share",
                "switch_per_yr", "slope", "vol_g", "vol_s", "gate_turn", "twin_turn"]
        diffs = {c: float((j[c] - j[c + "_608"]).abs().max()) for c in cols}
        fin = np.isfinite(j["cstar"]) & np.isfinite(j["cstar_608"])
        diffs["cstar(finite)"] = float((j.loc[fin, "cstar"] - j.loc[fin, "cstar_608"]).abs().max())
        same_inf = bool((np.isinf(j["cstar"]) == np.isinf(j["cstar_608"])).all())
        g3max = max(diffs.values())
        log(f"  G3 idea 608 join: {len(j)} of {len(parent)} arms matched on {key}")
        log("     max |diff|: " + "  ".join(f"{k} {v:.3e}" for k, v in diffs.items())
            + f"   +inf set identical: {same_inf}")
        log(f"  -> G3 {'PASS' if (g3max < 1e-9 and same_inf and len(j) == len(parent)) else 'FAIL'}"
            f" (bar 1e-9)")
    g5 = float(d["resid"].abs().max())
    log(f"  G5 drag identity DRAG == SWITCH_TAX + TIMING on {len(d)} arms: max |resid| {g5:.3e} "
        f"(bar 1e-15) -> {'PASS' if g5 < 1e-15 else 'FAIL'}")

    cen605 = np.isfinite(d["cstar"]) & (d["cstar"] > 0)
    fin = d[cen605]
    g6 = spearman(fin["cstar_hat"], fin["cstar"])
    log(f"  G6 closed form rho(dSharpe_0/SLOPE, c*) = {g6:+.6f} on {len(fin)} strictly-inside "
        f"arms (bar 0.999) -> {'PASS' if g6 >= 0.999 else 'FAIL'}; median |c*_hat/c* - 1| = "
        f"{float(((fin['cstar_hat']/fin['cstar'])-1).abs().median()):.4f}")
    log("     so log c* = E - S with E = log dSharpe_0, S = log SLOPE is the SAME object as the")
    log("     measured c*, and Q3's variance decomposition is a decomposition of c* itself.")

    d.to_csv(OUT / f"{STEM}.arms.csv.gz", index=False)
    cells.to_csv(OUT / f"{STEM}.cells.csv.gz", index=False)

    log("\n" + "=" * 185)
    log(f"POPULATION: {len(d)} twin-pair arms (3 panels x 18 level-arms x 3 depths x 2 cadences x "
        f"2 gross).  Per panel, on idea 605/608's censoring:")
    pop = []
    for pan in ["U56", "B136", "SMALL439"]:
        s = d[d["panel"] == pan]
        pop.append(dict(panel=pan, arms=len(s), at_zero=int((s["cstar"] == 0).sum()),
                        infinite=int(np.isinf(s["cstar"]).sum()),
                        inside=int((np.isfinite(s["cstar"]) & (s["cstar"] > 0)).sum()),
                        kept_share=float((np.isfinite(s["cstar"]) & (s["cstar"] > 0)).mean())))
    log(pd.DataFrame(pop).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # =============================================================== [1] Q1 the queue's test
    log("\n" + "=" * 185)
    log("[1] Q1 - THE QUEUE'S TEST.  mean within-dSharpe_0-bin rho(tax, c*), per PANEL x K.")
    log("    Bin 1 is the lowest-edge bin.  n-weighted mean reported beside the plain mean; the")
    log("    plain mean is the pre-registered statistic (idea 608 published the plain mean).")
    q1 = []
    for pan in ["U56", "B136", "SMALL439", "POOLED"]:
        sub = fin if pan == "POOLED" else fin[fin["panel"] == pan]
        raw = spearman(sub["switch_tax"], sub["cstar"])
        for K in KS:
            bins = edge_bins(sub, K)
            plain, wt, tab = within_bin_rho(sub, bins, "switch_tax", "cstar")
            q1.append(dict(panel=pan, K=K, n=len(sub), nbins=int(tab["rho"].notna().sum()),
                           min_bin_n=int(tab["n"].min()), raw_rho=raw, mean_rho=plain,
                           wmean_rho=wt, gain=abs(plain) - abs(raw)))
    q1 = pd.DataFrame(q1)
    q1.to_csv(OUT / f"{STEM}.q1.csv", index=False)
    log(q1.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    log("\n    the same, read as |rho| by panel across K (the queue's question is the SPREAD):")
    wide = q1.pivot_table(index="K", columns="panel", values="mean_rho")
    wide = wide[["U56", "B136", "SMALL439", "POOLED"]].abs()
    wide["spread_3panel"] = wide[["U56", "B136", "SMALL439"]].max(axis=1) - \
        wide[["U56", "B136", "SMALL439"]].min(axis=1)
    rawrow = q1.groupby("panel")["raw_rho"].first().abs()
    log(f"    raw (K=1, no conditioning): U56 {rawrow['U56']:.4f}  B136 {rawrow['B136']:.4f}  "
        f"SMALL439 {rawrow['SMALL439']:.4f}  POOLED {rawrow['POOLED']:.4f}  spread "
        f"{rawrow[['U56','B136','SMALL439']].max()-rawrow[['U56','B136','SMALL439']].min():.4f}")
    log(wide.to_string(float_format=lambda x: f"{x:.4f}"))

    sm = q1[q1["panel"] == "SMALL439"]
    bestK = int(sm.loc[sm["mean_rho"].abs().idxmax(), "K"])
    best_level = float(sm["mean_rho"].abs().max())
    best_gain = best_level - rawrow["SMALL439"]
    spread_at_best = float(wide.loc[bestK, "spread_3panel"])
    min_spread = float(wide["spread_3panel"].min())
    minK = int(wide["spread_3panel"].idxmin())
    closes = (best_level >= BAR_CLOSES_LEVEL) and (spread_at_best <= BAR_CLOSES_SPREAD)
    partial = (best_gain >= BAR_PARTIAL_GAIN) or (min_spread <= BAR_PARTIAL_SPREAD)
    verdict_q1 = "CLOSES" if closes else ("PARTIAL" if partial else "REFUTED")
    log(f"\n    SMALL439 best over K: K={bestK} at |rho| {best_level:.4f} (raw "
        f"{rawrow['SMALL439']:.4f}, gain {best_gain:+.4f}); spread there {spread_at_best:.4f}")
    log(f"    smallest 3-panel spread over K: {min_spread:.4f} at K={minK} "
        f"(raw spread {RAW_SPREAD:.3f})")
    log(f"    -> pre-registered Q1 verdict: **{verdict_q1}**  (CLOSES needs level >= "
        f"{BAR_CLOSES_LEVEL:.2f} AND spread <= {BAR_CLOSES_SPREAD:.3f}; PARTIAL needs gain >= "
        f"{BAR_PARTIAL_GAIN:.2f} OR spread <= {BAR_PARTIAL_SPREAD:.3f})")

    log("\n    and the same table on the UNCENSORED population (+inf ranked top, 0 kept), which")
    log("    idea 612 flags the record for not publishing:")
    q1u = []
    allarms = d[d["cstar"].notna()]
    for pan in ["U56", "B136", "SMALL439", "POOLED"]:
        sub = allarms if pan == "POOLED" else allarms[allarms["panel"] == pan]
        raw = spearman(sub["switch_tax"], sub["cstar"])
        for K in KS:
            plain, wt, tab = within_bin_rho(sub, edge_bins(sub, K), "switch_tax", "cstar")
            q1u.append(dict(panel=pan, K=K, n=len(sub), raw_rho=raw, mean_rho=plain,
                            gain=abs(plain) - abs(raw)))
    q1u = pd.DataFrame(q1u)
    log(q1u.pivot_table(index="K", columns="panel", values="mean_rho")[
        ["U56", "B136", "SMALL439", "POOLED"]].abs().to_string(float_format=lambda x: f"{x:.4f}"))
    log("    raw uncensored: " + "  ".join(
        f"{p} {abs(float(q1u[q1u['panel']==p]['raw_rho'].iloc[0])):.4f}"
        for p in ["U56", "B136", "SMALL439", "POOLED"]))

    # =============================================================== [2] Q2 the floor
    log("\n" + "=" * 185)
    log(f"[2] Q2 - THE BINNING FLOOR.  The SAME statistic on bins of the SAME sizes drawn at")
    log(f"    random ({NDRAW} draws per panel per K).  A lift inside this band is what BINNING")
    log("    does to a Spearman, not what the EDGE does.")
    rng = np.random.default_rng(SEED)
    q2 = []
    for pan in ["U56", "B136", "SMALL439", "POOLED"]:
        sub = (fin if pan == "POOLED" else fin[fin["panel"] == pan]).reset_index(drop=True)
        raw = spearman(sub["switch_tax"], sub["cstar"])
        for K in KS:
            bins = edge_bins(sub, K)
            real, _, tab = within_bin_rho(sub, bins, "switch_tax", "cstar")
            sizes = list(tab["n"].values)
            draws = []
            for _ in range(NDRAW):
                rb = random_bins(len(sub), sizes, rng)
                pl, _, _ = within_bin_rho(sub, rb, "switch_tax", "cstar")
                if np.isfinite(pl):
                    draws.append(abs(pl))
            draws = np.array(draws)
            q2.append(dict(panel=pan, K=K, real_abs=abs(real), null_mean=float(draws.mean()),
                           null_p95=float(np.quantile(draws, 0.95)),
                           excess=abs(real) - float(draws.mean()),
                           p_val=float((draws >= abs(real)).mean()),
                           raw_abs=abs(raw)))
    q2 = pd.DataFrame(q2)
    q2.to_csv(OUT / f"{STEM}.q2_floor.csv", index=False)
    log(q2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sm2 = q2[(q2["panel"] == "SMALL439")]
    log(f"\n    SMALL439: real vs null over K -> excess ranges "
        f"{sm2['excess'].min():+.4f} to {sm2['excess'].max():+.4f}, smallest p "
        f"{sm2['p_val'].min():.3f}")
    for pan in ["U56", "B136", "POOLED"]:
        s = q2[q2["panel"] == pan]
        log(f"    {pan:9s}: excess {s['excess'].min():+.4f} to {s['excess'].max():+.4f}, "
            f"smallest p {s['p_val'].min():.3f}")

    # =============================================================== [3] Q3 the fork
    log("\n" + "=" * 185)
    log("[3] Q3 - THE FORK.  log c* = E - S exactly (G6), E = log dSharpe_0, S = log SLOPE.")
    log("    rho(SLOPE, c*) is the CONTAMINATION leg with the proxy leg perfect (SLOPE IS the")
    log("    denominator).  rho(tax, SLOPE) is the PROXY leg with the numerator removed.")
    log("    The queue's premise requires SMALL439 to be the panel where the EDGE contaminates")
    log("    most - i.e. weakest rho(SLOPE, c*) and largest edge share of Var(log c*).")
    q3 = []
    for pan in ["U56", "B136", "SMALL439", "POOLED"]:
        s = fin if pan == "POOLED" else fin[fin["panel"] == pan]
        E = np.log(s["dSharpe_0"].where(s["dSharpe_0"] > 0))
        Sl = np.log(s["slope"].where(s["slope"] > 0))
        ok = E.notna() & Sl.notna()
        E, Sl = E[ok], Sl[ok]
        vE, vS = float(E.var(ddof=1)), float(Sl.var(ddof=1))
        cov = float(np.cov(E, Sl, ddof=1)[0, 1])
        q3.append(dict(
            panel=pan, n=len(s), n_logok=int(ok.sum()),
            rho_tax_cstar=spearman(s["switch_tax"], s["cstar"]),
            rho_slope_cstar=spearman(s["slope"], s["cstar"]),
            rho_edge_cstar=spearman(s["dSharpe_0"], s["cstar"]),
            rho_tax_slope=spearman(s["switch_tax"], s["slope"]),
            rho_tax_drag=spearman(s["switch_tax"], s["drag"]),
            sd_logE=vE ** 0.5, sd_logS=vS ** 0.5,
            edge_share=vE / (vE + vS),
            var_logcstar=vE + vS - 2 * cov,
            edge_share_of_var=vE / max(vE + vS - 2 * cov, 1e-18),
            iqr_ratio_edge=float(s["dSharpe_0"].quantile(0.75) / s["dSharpe_0"].quantile(0.25)),
            iqr_ratio_slope=float(s["slope"].quantile(0.75) / s["slope"].quantile(0.25))))
    q3 = pd.DataFrame(q3)
    q3.to_csv(OUT / f"{STEM}.q3_fork.csv", index=False)
    log(q3.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    r3 = q3.set_index("panel")
    log("\n    read the fork:")
    log(f"      CONTAMINATION leg  rho(SLOPE, c*): U56 {r3.loc['U56','rho_slope_cstar']:+.4f}  "
        f"B136 {r3.loc['B136','rho_slope_cstar']:+.4f}  "
        f"SMALL439 {r3.loc['SMALL439','rho_slope_cstar']:+.4f}")
    log(f"      PROXY leg          rho(tax, SLOPE): U56 {r3.loc['U56','rho_tax_slope']:+.4f}  "
        f"B136 {r3.loc['B136','rho_tax_slope']:+.4f}  "
        f"SMALL439 {r3.loc['SMALL439','rho_tax_slope']:+.4f}")
    log(f"      EDGE SHARE of Var(log c*):        U56 "
        f"{r3.loc['U56','edge_share_of_var']:.4f}  B136 "
        f"{r3.loc['B136','edge_share_of_var']:.4f}  SMALL439 "
        f"{r3.loc['SMALL439','edge_share_of_var']:.4f}")
    worst_cont = r3.loc[["U56", "B136", "SMALL439"], "rho_slope_cstar"].abs().idxmin()
    worst_proxy = r3.loc[["U56", "B136", "SMALL439"], "rho_tax_slope"].abs().idxmin()
    big_edge = r3.loc[["U56", "B136", "SMALL439"], "edge_share_of_var"].idxmax()
    log(f"      weakest CONTAMINATION leg: {worst_cont};  weakest PROXY leg: {worst_proxy};  "
        f"largest EDGE SHARE: {big_edge}")
    fork = ("EDGE-DISPERSION" if (worst_cont == "SMALL439" and big_edge == "SMALL439")
            else ("PROXY-QUALITY" if worst_proxy == "SMALL439" else "NEITHER-CLEANLY"))
    log(f"      -> the fork resolves to: **{fork}**")

    log("\n    per-panel edge and slope dispersion in levels (the queue's word 'dispersed'):")
    disp = fin.groupby("panel")[["dSharpe_0", "slope", "cstar"]].describe(
        percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).T
    log(disp.to_string(float_format=lambda x: f"{x:.5f}"))

    # =============================================================== [4] Q4 rule 8
    log("\n" + "=" * 185)
    log(f"[4] Q4 - RULE 8 ON THE CLAIM.  Everything rebuilt inside the IS window (<= {IS_END})")
    log(f"    only; K PICKED on IS per panel by mean within-bin |rho|, read ONCE on OOS")
    log(f"    ({OOS_START}+).  Every K's OOS number reported regardless.")
    wf = []
    for tag in ("IS", "OOS"):
        dd = d.copy()
        for c in ["switch_tax", "drag", "slope", "cstar", "dSharpe_0"]:
            src = ("tax_" + tag) if c == "switch_tax" else f"{c}_{tag}"
            dd[c] = d[src]
        sel = np.isfinite(dd["cstar"]) & (dd["cstar"] > 0)
        dw = dd[sel]
        for pan in ["U56", "B136", "SMALL439", "POOLED"]:
            sub = dw if pan == "POOLED" else dw[dw["panel"] == pan]
            raw = spearman(sub["switch_tax"], sub["cstar"])
            row = dict(window=tag, panel=pan, n=len(sub), raw_rho=raw,
                       rho_slope_cstar=spearman(sub["slope"], sub["cstar"]),
                       rho_tax_slope=spearman(sub["switch_tax"], sub["slope"]))
            for K in KS:
                pl, _, _ = within_bin_rho(sub, edge_bins(sub, K), "switch_tax", "cstar")
                row[f"K{K}"] = pl
            wf.append(row)
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log(wf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    log("\n    IS pick per panel, read once on OOS:")
    picks_k = []
    for pan in ["U56", "B136", "SMALL439", "POOLED"]:
        i = wf[(wf["window"] == "IS") & (wf["panel"] == pan)].iloc[0]
        o = wf[(wf["window"] == "OOS") & (wf["panel"] == pan)].iloc[0]
        kcols = [f"K{K}" for K in KS]
        pk = max(kcols, key=lambda c: abs(float(i[c])) if np.isfinite(i[c]) else -1)
        picks_k.append(dict(panel=pan, IS_pick=pk, IS_abs=abs(float(i[pk])),
                            OOS_at_pick=float(o[pk]), OOS_abs=abs(float(o[pk])),
                            OOS_raw=float(o["raw_rho"]),
                            OOS_gain_vs_raw=abs(float(o[pk])) - abs(float(o["raw_rho"])),
                            OOS_best_K=max(kcols, key=lambda c: abs(float(o[c]))),
                            OOS_best_abs=max(abs(float(o[c])) for c in kcols)))
    picks_k = pd.DataFrame(picks_k)
    log(picks_k.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    sm_wf = picks_k[picks_k["panel"] == "SMALL439"].iloc[0]
    log(f"\n    SMALL439 walk-forward: IS pick {sm_wf['IS_pick']} (|rho_IS| "
        f"{sm_wf['IS_abs']:.4f}) -> OOS |rho| {sm_wf['OOS_abs']:.4f} vs OOS raw "
        f"{abs(sm_wf['OOS_raw']):.4f} (gain {sm_wf['OOS_gain_vs_raw']:+.4f}); OOS regret vs the "
        f"best K in hindsight {sm_wf['OOS_abs'] - sm_wf['OOS_best_abs']:+.4f}")
    log("    the fork's own legs walk forward too (columns rho_slope_cstar / rho_tax_slope above)")

    # =============================================================== [5] Q5 PROTOCOL
    log("\n" + "=" * 185)
    log("[5] Q5 - PROTOCOL.  Both KEEP paths on all arms at rungs 0/10/25, then the rule-8 book")
    log("    chooser (IS Sharpe pick, OOS read once) against RULES v2 and SPY.")
    log("    4a passes: " + "  ".join(
        f"{c:.0f}bps {int(cells[cells['rung']==c]['p4a'].sum())}/{int((cells['rung']==c).sum())}"
        for c in RUNGS))
    log("    4b passes: " + "  ".join(
        f"{c:.0f}bps {int(cells[cells['rung']==c]['p4b'].sum())}/{int((cells['rung']==c).sum())}"
        for c in RUNGS))
    h = cells[cells["rung"] == RUNG_HEAD]
    log(f"    at PROTOCOL's own {RUNG_HEAD:.0f} bps: 4a {int(h['p4a'].sum())}, 4b "
        f"{int(h['p4b'].sum())} of {len(h)}; dominant 4b failure legs: "
        + ", ".join(f"{k} {v}" for k, v in h["fail4b"].value_counts().head(4).items()))
    log(f"    BOTH paths at {RUNG_HEAD:.0f} bps: {int((h['p4a'] & h['p4b']).sum())}")
    log("    4b by panel at 10 bps: " + "  ".join(
        f"{p} {int(h[h['panel']==p]['p4b'].sum())}/{int((h['panel']==p).sum())}"
        for p in ["U56", "B136", "SMALL439"]))

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
        f"G6 {g6:+.6f}")
    log(f"  Q1 SMALL439: raw |rho| {rawrow['SMALL439']:.4f} -> best over K "
        f"{best_level:.4f} at K={bestK} (gain {best_gain:+.4f}); 3-panel spread "
        f"{RAW_SPREAD:.3f} -> {min_spread:.4f} at best K -> **{verdict_q1}**")
    log(f"  Q2 floor: SMALL439 excess over the random-bin null {sm2['excess'].min():+.4f} to "
        f"{sm2['excess'].max():+.4f}, smallest p {sm2['p_val'].min():.3f}")
    log(f"  Q3 fork: **{fork}** - contamination leg rho(SLOPE,c*) weakest on {worst_cont}, proxy "
        f"leg rho(tax,SLOPE) weakest on {worst_proxy}, edge share largest on {big_edge}")
    log(f"  Q4 rule 8: SMALL439 IS pick {sm_wf['IS_pick']} -> OOS |rho| {sm_wf['OOS_abs']:.4f} vs "
        f"raw {abs(sm_wf['OOS_raw']):.4f} (gain {sm_wf['OOS_gain_vs_raw']:+.4f})")
    log(f"  Q5 4a {int(h['p4a'].sum())} / 4b {int(h['p4b'].sum())} of {len(h)} at 10 bps; "
        f"rule-8 picks beating RULES v2 OOS {int(hp['beats_v2'].sum())}/{len(hp)}, SPY "
        f"{int(hp['beats_spy'].sum())}/{len(hp)}")
    log("  Nothing promoted; no RULES change proposed by this run.")
    log("  SURVIVORSHIP: three current-constituent panels; levels optimistic, within-panel rank")
    log("  statistics unaffected, cross-panel comparisons inherit the screens' differential.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.{{arms,cells,q1,q2_floor,q3_fork,walkforward,picks,refs,console}}")


if __name__ == "__main__":
    main()
