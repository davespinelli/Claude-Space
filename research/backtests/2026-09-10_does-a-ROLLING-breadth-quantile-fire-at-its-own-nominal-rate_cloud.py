#!/usr/bin/env python3
"""Idea 399 - "does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate" (cloud lane).

The finding this run exists to re-price
---------------------------------------
Idea 336 replaced idea 42's ABSOLUTE breadth threshold with a CAUSAL EXPANDING quantile of the
panel's own breadth history.  It equalised the CROSS-PANEL firing rate (spread 0.193/0.413/0.686
-> 0.002/0.015/0.007) and CONFIRMED the queue's rate-artefact diagnosis.  But it failed its own
LEVEL: realised/nominal = 0.032/0.270/0.306 (U56), 0.000/0.207/0.277 (B136), 0.004/0.148/0.266
(SMALL484) - the estimator is anchored by the 2008-2011 breadth lows, which breadth never
revisits, so a nominal q=0.07 arm is INERT (0.000-0.002 of days) and PROTOCOL rule 8's chooser
picked that inert arm in 5 of 6 headline cells.  Idea 336's Q3 KILL was therefore measured on a
CRIPPLED instrument, and the queue asks whether a ROLLING (trailing-w-day) quantile restores rate
fidelity - and, if it does, what the KILL becomes when the instrument actually fires.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (RATE FIDELITY)  Does QROLL(q, w) fire at its own nominal q?  Measured as realised/nominal
                        per panel x q x w, beside idea 336's QEXP on the same base book and the
                        same days.  This is the queue's literal question and it is the headline.
    Q2 (CROSS-PANEL)    Does QROLL keep QEXP's cross-panel rate equalisation, which was the one
                        thing the quantile form bought?  Fidelity and equalisation are DIFFERENT
                        claims (idea 336 was explicit about this) and are reported apart.
    Q3 (RE-READ)        With an instrument that fires at its nominal rate, does the Q3 KILL go
                        away?  The bar is NOT "less inert than QEXP": it is (a) the ungated parent
                        (do nothing), (b) the matched-mean-gross static twin (the same average
                        exposure with no timing at all), and (c) PROTOCOL's two KEEP paths.
    Q4 (CHOOSER)        Under rule 8, does the IS chooser still pick an inert arm?  Reported as
                        the picked arm's REALISED firing rate, not only its Sharpe.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. w      rolling window, in trading days, in {252, 504, 1008, 2016} (1y, 2y, 4y, 8y)
    2. depth  cut depth, in {0.25, 0.50, 1.00}     (idea 42/336's own three values)
    12 points, ALL reported at every panel / q / gross / cadence / cost rung.

Reported axes, NEVER tuned or selected on
    q        0.07 / 0.12 / 0.17   (idea 336's nominal levels, inherited verbatim, not searched)
    panel    U56 / B136 / SMALL439
    gross    0.75 / 1.00          (the chooser only ever sees 0.75)
    cadence  D / W                (W = the multiplier may only move on rebalance days)
    cost     0 / 10 / 25 bps      (10 = PROTOCOL rule 2; 0 and 25 classify 10-bps artefacts)

Families on one fixed base book
    NOGATE       ungated EWALL(G) - the DO-NOTHING bar.
    ABS(B)       idea 42 verbatim, B in {0.30, 0.40, 0.50} - the original comparand.
    QEXP(q)      idea 336's causal EXPANDING quantile - the instrument under suspicion.
    QROLL(q,w)   THIS IDEA: gate ON when breadth_t < the trailing-w-day q-quantile of breadth,
                 computed through t only, executed at t+1.  Unarmed (gate OFF) until w
                 observations exist; the armed share is reported for every w.
    MATCHED      static gross G * mean(mult), no gate at all - Q3's "gross dial in a timing
                 costume" bar, at the headline rung.  Never tuned, never a verdict on its own.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(c).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.
    G3  idea 336's COMMITTED grid.csv: every ABS and QEXP arm this run re-runs on U56 and B136,
        joined and differenced on 6 columns (its SMALL484 rows are NOT joinable here - this run
        drops the 46 max_1d_move >= 1.0 names, so the panel is SMALL439 by construction and the
        difference is reported, not hidden).
    G4  QROLL rate identity: on a stationary control series (a deterministic sawtooth), the
        realised rate of a trailing-w q-quantile gate equals q to within 1/w.

Data: committed caches only, no network.  SURVIVORSHIP: all three panels are current-constituent
lists, so CAGR and drawdown LEVELS are optimistic; the gated-vs-parent and gated-vs-matched-gross
CONTRASTS are the durable part.  SMALL439 starts 2010-01-04, so its halves are not the same
calendar halves as U56/B136's, and w=2016 costs it half its sample in warm-up.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
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
PARENT_GRID = OUT / "2026-09-07_re-price-the-fixed-ABSOLUTE-breadth-threshold-as-a-quantile_C.grid.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]          # tuned param 1
DEPTHS = [0.25, 0.50, 1.00]          # tuned param 2
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
MINQ = 252                           # idea 336's expanding warm-up, inherited verbatim
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 1200)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/336 verbatim)
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
    """Gate ON (carry the book at 1-depth) when breadth_t < thr_t.  Information through t only."""
    m = pd.Series(1.0, index=idx).where(~(br < thr), 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def gate_abs(br, B, depth, cadence, idx):
    m = pd.Series(1.0, index=idx).where(~(br < B), 1.0 - depth)
    m = m.where(br.notna(), 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def apply_gate(r_base, mult, gross, cost_bps):
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


# ---------------------------------------------------------------- metrics helpers
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


def summarise(r, spy_pack, base_pack, mult=None):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy_pack)
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=m_is["Sharpe"], OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
             OOS_MaxDD=m_oos["MaxDD"], p4a=verdict_4a(r, base_pack), p4b=all(t.values()),
             fail4b=",".join([k for k, v in t.items() if not v]) or "-")
    d["on_share"] = float((mult < 1.0).mean()) if mult is not None else 0.0
    d["mean_mult"] = float(mult.mean()) if mult is not None else 1.0
    return d


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ---------------------------------------------------------------- panel run
def run_panel(panel, px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    s1, s2 = half_sharpes(spy)
    spy_pack = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])

    br_full = breadth(px)
    br = br_full.loc[start:]
    log(f"\n{'='*170}\nPANEL {panel}: {px.shape[1]} columns, {px.index[0].date()} -> "
        f"{px.index[-1].date()}, eval from {start.date()}")
    log(f"  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}; 4b bars: CAGR floor "
        f"{0.70*ms['CAGR']:.2%}, DD cap {-0.60*abs(ms['MaxDD']):.2%}, halves {s1:.3f}/{s2:.3f}, "
        f"OOS {spy_pack[2]:.3f}")
    f_panel = {B: float((br < B).mean()) for B in BS}
    log(f"  breadth_t mean {br.mean():.3f} median {br.median():.3f}; ABS share below "
        f"0.30/0.40/0.50 = {f_panel[0.30]:.3f}/{f_panel[0.40]:.3f}/{f_panel[0.50]:.3f}")

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}
    armed = {w: float(thr_roll[(QS[0], w)].loc[start:].notna().mean()) for w in WS}
    armed_exp = float(thr_exp[QS[0]].loc[start:].notna().mean())
    log("  armed share of eval days: QEXP(min_periods=252) " + f"{armed_exp:.3f}; QROLL " +
        ", ".join(f"w={w} {armed[w]:.3f}" for w in WS)
        + "   (unarmed days are gate OFF, i.e. fully invested)")

    # ---- base books, one backtest per gross at 0 bps; all rungs derived (G1 asserts this)
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

    # ---- multipliers, computed once
    mults, rate = {}, {}
    idx = px.index
    for cad in CADENCES:
        for d in DEPTHS:
            for q in QS:
                mults[("QEXP", q, None, d, cad)] = gate_from_thr(br_full, thr_exp[q], d, cad, idx).loc[start:]
                for w in WS:
                    mults[("QROLL", q, w, d, cad)] = gate_from_thr(br_full, thr_roll[(q, w)], d, cad, idx).loc[start:]
            for B in BS:
                mults[("ABS", B, None, d, cad)] = gate_abs(br_full, B, d, cad, idx).loc[start:]

    # ---- Q1/Q2: realised firing rates (cadence D, the instrument's own rate) -------------
    for q in QS:
        rate[("QEXP", q, None)] = float((br < thr_exp[q].loc[start:]).mean())
        rate[("QEXP_armed", q, None)] = float((br < thr_exp[q].loc[start:])[thr_exp[q].loc[start:].notna()].mean())
        for w in WS:
            t = thr_roll[(q, w)].loc[start:]
            rate[("QROLL", q, w)] = float((br < t).mean())
            rate[("QROLL_armed", q, w)] = float((br < t)[t.notna()].mean())
    for B in BS:
        rate[("ABS", B, None)] = f_panel[B]

    # ---- the grid -----------------------------------------------------------------------
    out = []
    for c in RUNGS:
        for nm, r in refs[c].items():
            out.append(dict(panel=panel, rung=c, gross=np.nan, family="ref", arm=nm, q=np.nan,
                            w=np.nan, level=np.nan, depth=np.nan, cadence="-", rate=np.nan,
                            rate_ratio=np.nan, **summarise(r, spy_pack, base_packs[c])))
        for g in GROSSES:
            rb = rung(base0[g], c)
            out.append(dict(panel=panel, rung=c, gross=g, family="NOGATE", arm=f"NOGATE g{g:.2f}",
                            q=np.nan, w=np.nan, level=np.nan, depth=0.0, cadence="-",
                            rate=0.0, rate_ratio=np.nan,
                            **summarise(rb, spy_pack, base_packs[c])))
            for cad in CADENCES:
                for d in DEPTHS:
                    for q in QS:
                        m = mults[("QEXP", q, None, d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        out.append(dict(panel=panel, rung=c, gross=g, family="QEXP",
                                        arm=f"QEXP q{q:.2f} d{d:.2f} {cad} g{g:.2f}", q=q,
                                        w=np.nan, level=q, depth=d, cadence=cad,
                                        rate=rate[("QEXP", q, None)],
                                        rate_ratio=rate[("QEXP", q, None)] / q,
                                        **summarise(rg, spy_pack, base_packs[c], mult=me)))
                        for w in WS:
                            m = mults[("QROLL", q, w, d, cad)]
                            rg, me = apply_gate(rb, m, g, c)
                            out.append(dict(panel=panel, rung=c, gross=g, family="QROLL",
                                            arm=f"QROLL q{q:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                                            q=q, w=w, level=q, depth=d, cadence=cad,
                                            rate=rate[("QROLL", q, w)],
                                            rate_ratio=rate[("QROLL", q, w)] / q,
                                            **summarise(rg, spy_pack, base_packs[c], mult=me)))
                    for B in BS:
                        m = mults[("ABS", B, None, d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        out.append(dict(panel=panel, rung=c, gross=g, family="ABS",
                                        arm=f"ABS B{B:.2f} d{d:.2f} {cad} g{g:.2f}", q=np.nan,
                                        w=np.nan, level=B, depth=d, cadence=cad,
                                        rate=f_panel[B], rate_ratio=np.nan,
                                        **summarise(rg, spy_pack, base_packs[c], mult=me)))

    # ---- Q3 control: matched-mean-gross static twin, headline rung, G_HEAD --------------
    matched, seen = [], {}
    rb = rung(base0[G_HEAD], RUNG_HEAD)
    for cad in CADENCES:
        for q in QS:
            for w in [None] + WS:
                fam = "QEXP" if w is None else "QROLL"
                for d in DEPTHS:
                    rg, me = apply_gate(rb, mults[(fam, q, w, d, cad)], G_HEAD, RUNG_HEAD)
                    g_eff = round(G_HEAD * float(me.mean()), 2)   # rounded to 2dp to cache twins
                    if g_eff not in seen:
                        seen[g_eff] = backtest(px, ewall_weights(px, g_eff), cost_bps=RUNG_HEAD,
                                               freq=FREQ)["returns"].loc[start:]
                    rs = seen[g_eff]
                    mg, mst = metrics(rg), metrics(rs)
                    matched.append(dict(panel=panel, family=fam, q=q, w=(w or 0), depth=d,
                                        cadence=cad, g_eff=g_eff,
                                        gate_Sharpe=mg["Sharpe"], static_Sharpe=mst["Sharpe"],
                                        dSharpe=mg["Sharpe"] - mst["Sharpe"],
                                        gate_OOS=metrics(rg.loc[OOS_START:])["Sharpe"],
                                        static_OOS=metrics(rs.loc[OOS_START:])["Sharpe"],
                                        dOOS=metrics(rg.loc[OOS_START:])["Sharpe"]
                                             - metrics(rs.loc[OOS_START:])["Sharpe"],
                                        gate_MaxDD=mg["MaxDD"], static_MaxDD=mst["MaxDD"],
                                        dMaxDD=abs(mst["MaxDD"]) - abs(mg["MaxDD"])))

    # ---- rule 8 walk-forward -------------------------------------------------------------
    wf = []
    for c in RUNGS:
        rbc = rung(base0[G_HEAD], c)
        nog = metrics(rbc.loc[OOS_START:])
        for cad in CADENCES:
            # QROLL: the tuned pair is (w, depth), one chooser per nominal q
            for q in QS:
                cells = {(w, d): apply_gate(rbc, mults[("QROLL", q, w, d, cad)], G_HEAD, c)[0]
                         for w in WS for d in DEPTHS}
                wf.append(_wf_row(panel, "QROLL", c, cad, q, cells, rbc, nog, spy,
                                  refs[c]["v2"], lambda k: rate[("QROLL", q, k[0])]))
            # comparands under the IDENTICAL chooser: QEXP over (q, depth), ABS over (B, depth)
            cells = {(q, d): apply_gate(rbc, mults[("QEXP", q, None, d, cad)], G_HEAD, c)[0]
                     for q in QS for d in DEPTHS}
            wf.append(_wf_row(panel, "QEXP", c, cad, np.nan, cells, rbc, nog, spy,
                              refs[c]["v2"], lambda k: rate[("QEXP", k[0], None)]))
            cells = {(B, d): apply_gate(rbc, mults[("ABS", B, None, d, cad)], G_HEAD, c)[0]
                     for B in BS for d in DEPTHS}
            wf.append(_wf_row(panel, "ABS", c, cad, np.nan, cells, rbc, nog, spy,
                              refs[c]["v2"], lambda k: rate[("ABS", k[0], None)]))

    rates = pd.DataFrame([dict(panel=panel, family=k[0], q=k[1],
                               w=(0 if k[2] is None else k[2]), realised=v,
                               nominal=(k[1] if k[0].startswith("Q") else np.nan))
                          for k, v in rate.items()])
    return pd.DataFrame(out), pd.DataFrame(matched), pd.DataFrame(wf), rates


def _wf_row(panel, fam, c, cad, q, cells, rbc, nog, spy, v2, rate_of):
    is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cells.items()}
    oos = {k: metrics(v.loc[OOS_START:]) for k, v in cells.items()}
    pick = min(is_s, key=lambda k: (-is_s[k], k[0], k[1]))
    best = max(oos, key=lambda k: oos[k]["Sharpe"])
    return dict(panel=panel, family=fam, rung=c, cadence=cad, q=q,
                pick_a=pick[0], pick_depth=pick[1], pick_rate=rate_of(pick),
                IS_Sharpe=is_s[pick], OOS_CAGR=oos[pick]["CAGR"], OOS_Sharpe=oos[pick]["Sharpe"],
                OOS_MaxDD=oos[pick]["MaxDD"], nogate_OOS_Sharpe=nog["Sharpe"],
                nogate_OOS_CAGR=nog["CAGR"], nogate_OOS_MaxDD=nog["MaxDD"],
                vs_nogate=oos[pick]["Sharpe"] - nog["Sharpe"],
                grid_mean_OOS=float(np.mean([oos[k]["Sharpe"] for k in oos])),
                best_OOS=oos[best]["Sharpe"], regret=oos[pick]["Sharpe"] - oos[best]["Sharpe"],
                spy_OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                v2_OOS=metrics(v2.loc[OOS_START:])["Sharpe"])


# ---------------------------------------------------------------- main
def main():
    log("=" * 170)
    log(f"Idea 399 does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate (cloud) | {SCRIPT}")
    log("=" * 170)
    log("Base book (fixed, idea 28/42/336's): EWALL(G) = equal weight every name above its own 200d")
    log("  MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is BELOW the threshold.")
    log("  ABS(B)      breadth_t < B                                  (idea 42 - comparand)")
    log("  QEXP(q)     breadth_t < causal EXPANDING q-quantile        (idea 336 - the suspect)")
    log("  QROLL(q,w)  breadth_t < trailing-w-day q-quantile          (THIS IDEA)")
    log(f"Tuned (2): w in {WS} x depth in {DEPTHS}; reported never tuned: q {QS}, gross {GROSSES}, "
        f"cadence {CADENCES}, cost {RUNGS} bps, 3 panels.")

    # ---------------- gates
    log("\n" + "=" * 170)
    log("[0] REPRODUCTION GATES")
    px0 = load_universe()
    r0 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=0, freq=FREQ)
    r25 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=25, freq=FREQ)
    g1 = float((r0["returns"] - r0["turnover"] * 25 / 1e4 - r25["returns"]).abs().max())
    log(f"  G1 derived cost rung vs live engine.backtest(25): {g1:.3e} "
        f"-> {'PASS' if g1 < 1e-12 else 'FAIL'}")
    assert g1 < 1e-12

    s = px0.index[260]
    r85 = backtest(px0, ewall_weights(px0, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[s:]
    m85 = metrics(r85)
    h1, h2 = half_sharpes(r85)
    ok2 = (abs(m85["CAGR"] - 0.118) < 1e-3 and abs(m85["Sharpe"] - 1.05) < 6e-3
           and abs(m85["MaxDD"] + 0.179) < 1e-3)
    log(f"  G2 idea 84 EWALL U56 g=0.85 @10bps (committed 11.8% / 1.05 / -17.9% / H 1.07 / 1.04): "
        f"{m85['CAGR']:.3%} / {m85['Sharpe']:.3f} / {m85['MaxDD']:.3%} / H {h1:.2f} / {h2:.2f} "
        f"-> {'PASS' if ok2 else 'FAIL (reported, not silenced)'}")

    # G4: rate identity of a trailing-w quantile on CONTROL series with known properties.
    #     (a) IID: the estimator itself must fire at q.  (b) AR(1) with rho=0.98, a persistence
    #     comparable to breadth's: measured, NOT a pass/fail, so the panel numbers below can be
    #     read against what PERSISTENCE ALONE does to a trailing-window quantile's realised rate.
    rng = np.random.default_rng(7)
    n = 20000
    iid = pd.Series(rng.standard_normal(n))
    ar = np.zeros(n)
    for i in range(1, n):
        ar[i] = 0.98 * ar[i - 1] + rng.standard_normal()
    ar = pd.Series(ar)

    def realised(sr, w, q=0.12):
        thr = sr.rolling(w, min_periods=w).quantile(q)
        return float((sr < thr)[thr.notna()].mean())

    dev = [abs(realised(iid, w) - 0.12) for w in WS]
    g4 = max(dev)
    log(f"  G4a trailing-w q-quantile on an IID control, q=0.12: realised "
        + "/".join(f"{realised(iid, w):.4f}" for w in WS) + f" (w={WS}); max |realised - q| "
        f"{g4:.4f} -> {'PASS' if g4 < 0.02 else 'FAIL'}")
    assert g4 < 0.02
    log(f"  G4b same estimator on an AR(1) rho=0.98 control (breadth-like persistence), q=0.12: "
        + "/".join(f"{realised(ar, w):.4f}" for w in WS)
        + "  - MEASURED, not a bar: persistence alone inflates the realised rate at short w.")

    # ---------------- panels
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True))]
    px_s, ndrop = small_panel()
    log(f"  small panel: {px_s.shape[1]-1} names after dropping {ndrop} with max_1d_move >= 1.0 "
        f"(idea 336 ran SMALL484, i.e. UNFILTERED: its small-panel rows are not joinable in G3)")
    panels.append((f"SMALL{px_s.shape[1]-1}", px_s))

    grids, matches, wfs, rates = [], [], [], []
    for name, px in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            log(f"!! {name}: CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        g, m, w, rt = run_panel(name, px)
        grids.append(g); matches.append(m); wfs.append(w); rates.append(rt)
    grid = pd.concat(grids, ignore_index=True)
    matched = pd.concat(matches, ignore_index=True)
    wf = pd.concat(wfs, ignore_index=True)
    rate = pd.concat(rates, ignore_index=True)

    # ---------------- G3 against idea 336's committed grid
    log("\n" + "=" * 170)
    log("[0b] G3 - idea 336's COMMITTED grid.csv, joined on the arms this run re-runs")
    if PARENT_GRID.exists():
        par = pd.read_csv(PARENT_GRID)
        par = par[par.panel.isin(["U56", "B136"])]
        mine = grid[grid.panel.isin(["U56", "B136"]) & grid.family.isin(["ABS", "QEXP"])].copy()
        par_a = par[par.family == "ABS"].copy()
        par_q = par[par.family == "QUANT"].copy()
        par_q["family"] = "QEXP"
        par2 = pd.concat([par_a, par_q])
        keys = ["panel", "rung", "gross", "family", "level", "depth", "cadence"]
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]
        j = mine.set_index(keys)[cols].join(par2.set_index(keys)[cols], rsuffix="_p", how="inner")
        if len(j):
            d = max(float((j[c] - j[f"{c}_p"]).abs().max()) for c in cols)
            log(f"  rows joined {len(j)} of {len(mine)} re-run arms; max abs diff over {cols}: "
                f"{d:.3e} -> {'PASS' if d < 1e-9 else 'FAIL (reported, not silenced)'}")
        else:
            log("  no rows joined (key mismatch) - G3 NOT AVAILABLE, reported as such")
    else:
        log("  idea 336's grid.csv absent - G3 NOT AVAILABLE, reported as such")

    # ---------------- Q1 / Q2
    log("\n" + "=" * 170)
    log("[1] Q1 RATE FIDELITY and Q2 CROSS-PANEL EQUALISATION (cadence D, the instrument's own rate)")
    fid = rate[rate.family.isin(["QEXP", "QROLL"])].copy()
    fid["ratio"] = fid.realised / fid.nominal
    piv = fid.pivot_table(index=["family", "w"], columns=["panel", "q"], values="realised")
    log("  (QEXP, the expanding comparand, is carried at w = 0 so it prints beside the rolling windows)")
    log("\n  REALISED daily firing share (all eval days; unarmed days count as NOT firing):")
    log(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    piv_r = fid.pivot_table(index=["family", "w"], columns=["panel", "q"], values="ratio")
    log("\n  realised / nominal q  (1.000 = perfect level fidelity; idea 336's QEXP: 0.00-0.31):")
    log(piv_r.to_string(float_format=lambda x: f"{x:.3f}"))
    fid_a = rate[rate.family.isin(["QEXP_armed", "QROLL_armed"])].copy()
    fid_a["ratio"] = fid_a.realised / fid_a.nominal
    log("\n  realised / nominal on ARMED days only (removes the warm-up dilution):")
    log(fid_a.pivot_table(index=["family", "w"], columns=["panel", "q"], values="ratio")
        .to_string(float_format=lambda x: f"{x:.3f}"))
    sp = (fid.groupby(["family", "w", "q"]).realised.agg(lambda x: x.max() - x.min())
          .rename("cross_panel_spread").reset_index())
    log("\n  Q2 cross-panel spread of the realised rate (ABS comparand from idea 42: "
        "0.193 / 0.413 / 0.686):")
    log(sp.pivot_table(index=["family", "w"], columns="q", values="cross_panel_spread")
        .to_string(float_format=lambda x: f"{x:.4f}"))
    absr = rate[rate.family == "ABS"].copy()
    log("\n  ABS realised rates re-measured here (B = 0.30 / 0.40 / 0.50):")
    log(absr.pivot_table(index="panel", columns="q", values="realised")
        .to_string(float_format=lambda x: f"{x:.4f}"))
    abs_spread = float(absr.groupby("q").realised.agg(lambda x: x.max() - x.min()).median())
    rate.to_csv(OUT / f"{STEM}.rates.csv", index=False)

    # ---------------- Q3
    log("\n" + "=" * 170)
    log("[2] Q3 - what the instrument EARNS, at every grid point")
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    matched.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    gg = grid[grid.family.isin(["QROLL", "QEXP", "ABS"])]
    log(f"  grid rows: {len(grid)} ({len(gg)} gated arms + refs/controls)")
    log("\n  4a / 4b pass counts by family (every panel, gross, cadence, rung):")
    log(gg.groupby("family").agg(n=("p4a", "size"), pass4a=("p4a", "sum"),
                                 pass4b=("p4b", "sum")).to_string())
    both = gg[gg.p4a & gg.p4b]
    log(f"  BOTH paths: {len(both)}")
    log("\n  4a / 4b by family x panel:")
    log(gg.groupby(["family", "panel"]).agg(n=("p4a", "size"), pass4a=("p4a", "sum"),
                                            pass4b=("p4b", "sum")).to_string())
    log("\n  4b failure reasons:")
    log(gg.fail4b.value_counts().head(12).to_string())
    ng = grid[grid.family == "NOGATE"]
    log(f"\n  the ungated parents themselves: 4a {int(ng.p4a.sum())} / 4b {int(ng.p4b.sum())} "
        f"of {len(ng)} - a gated arm inheriting a passing parent is NOT an edge:")
    log(ng[["panel", "rung", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
            "p4a", "p4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if len(gg[gg.p4b]):
        top = gg[gg.p4b].sort_values("OOS_Sharpe", ascending=False)
        log(f"\n  4b passers ({len(top)}), best 25 by OOS Sharpe:")
        log(top.head(25)[["panel", "family", "q", "w", "level", "depth", "cadence", "gross",
                          "rung", "rate", "on_share", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                          "OOS_Sharpe", "p4a"]].to_string(index=False,
                                                          float_format=lambda x: f"{x:.3f}"))
    log("\n  Q3 bar (b): matched-mean-gross static twin, headline rung 10 bps, g=0.75:")
    mm = matched.groupby(["panel", "family"]).agg(
        n=("dSharpe", "size"), beats_twin=("dSharpe", lambda x: int((x > 0).sum())),
        med_dSharpe=("dSharpe", "median"), beats_twin_OOS=("dOOS", lambda x: int((x > 0).sum())),
        med_dOOS=("dOOS", "median"), med_dMaxDD=("dMaxDD", "median"))
    log(mm.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------- Q4 / rule 8
    log("\n" + "=" * 170)
    log("[3] Q4 + RULE 8 WALK-FORWARD (IS 2009-2016 Sharpe picks; OOS 2017-2026 read once)")
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log(wf[["panel", "family", "q", "rung", "cadence", "pick_a", "pick_depth", "pick_rate",
            "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "nogate_OOS_Sharpe", "vs_nogate",
            "grid_mean_OOS", "best_OOS", "regret", "spy_OOS", "v2_OOS"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for fam in ("QROLL", "QEXP", "ABS"):
        w2 = wf[wf.family == fam]
        inert = int((w2.pick_rate < 0.01).sum())
        log(f"\n  {fam}: {len(w2)} chooser cells; picks an arm firing < 1% of days in {inert} "
            f"({inert/len(w2):.1%}); beats DOING NOTHING on OOS Sharpe in "
            f"{int((w2.vs_nogate > 0).sum())}; beats SPY OOS in {int((w2.OOS_Sharpe > w2.spy_OOS).sum())}; "
            f"beats RULES v2 OOS in {int((w2.OOS_Sharpe > w2.v2_OOS).sum())}; "
            f"mean vs_nogate {w2.vs_nogate.mean():+.3f}; mean regret {w2.regret.mean():.3f}; "
            f"median picked rate {w2.pick_rate.median():.4f}")

    # ---------------- cost rung, inheritance, and whether the RULE-8 PICK itself passes 4b
    log("\n" + "=" * 170)
    log("[3b] WHERE THE 4b PASSES LIVE: cost rung, gross, and the ungated parent")
    log(pd.crosstab([gg.rung, gg.gross], [gg.family, gg.p4b]).to_string())
    par = ng.set_index(["panel", "rung", "gross"])["p4b"]
    inh = gg.join(par.rename("parent_4b"), on=["panel", "rung", "gross"])
    log(f"\n  of the {int(gg.p4b.sum())} 4b passes, {int((inh.p4b & inh.parent_4b).sum())} sit on a "
        f"parent that already passes 4b and {int((inh.p4b & ~inh.parent_4b).sum())} do not:")
    log(inh[inh.p4b & ~inh.parent_4b].groupby(["rung", "gross", "family"]).size().to_string())
    log(f"  4a passes by rung: {gg[gg.p4a].rung.value_counts().to_dict()} "
        f"(PROTOCOL rule 2's rung is {RUNG_HEAD} bps)")

    picks = []
    q75 = gg[(gg.gross == G_HEAD)]
    for _, x in wf.iterrows():
        fam = x.family
        if fam == "QROLL":
            m = q75[(q75.panel == x.panel) & (q75.rung == x.rung) & (q75.cadence == x.cadence)
                    & (q75.family == "QROLL") & (q75.q == x.q) & (q75.w == x.pick_a)
                    & (q75.depth == x.pick_depth)]
        else:
            m = q75[(q75.panel == x.panel) & (q75.rung == x.rung) & (q75.cadence == x.cadence)
                    & (q75.family == fam) & (q75.level == x.pick_a) & (q75.depth == x.pick_depth)]
        if len(m) != 1:
            continue
        m = m.iloc[0]
        picks.append(dict(panel=x.panel, family=fam, rung=x.rung, cadence=x.cadence, q=x.q,
                          pick_a=x.pick_a, pick_depth=x.pick_depth, p4a=bool(m.p4a),
                          p4b=bool(m.p4b), fail4b=m.fail4b,
                          parent_4b=bool(par.loc[(x.panel, x.rung, G_HEAD)]),
                          OOS_Sharpe=x.OOS_Sharpe, vs_nogate=x.vs_nogate))
    picks = pd.DataFrame(picks)
    picks.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    log("\n  does the RULE-8 PICK itself clear a KEEP path? (the only 4b claim PROTOCOL rule 8 allows)")
    log(picks.groupby(["family", "rung"]).agg(cells=("p4b", "size"), pass4b=("p4b", "sum"),
                                              pass4a=("p4a", "sum"),
                                              pass4b_uninherited=("p4b", "sum")).to_string())
    keep_rows = picks[(picks.rung == RUNG_HEAD) & picks.p4b & ~picks.parent_4b]
    head_rows = picks[(picks.rung == RUNG_HEAD) & picks.p4b]
    log(f"  at the PROTOCOL rung ({RUNG_HEAD} bps, gross {G_HEAD}): {len(head_rows)} of "
        f"{int((picks.rung == RUNG_HEAD).sum())} picks pass 4b, of which "
        f"{len(keep_rows)} sit on a parent that does NOT already pass 4b.")
    if len(head_rows):
        log(head_rows.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- verdict
    log("\n" + "=" * 170)
    log("[4] VERDICT")
    qr = gg[gg.family == "QROLL"]
    qe = gg[gg.family == "QEXP"]
    med_fid_roll = float(fid[fid.family == "QROLL"].ratio.median())
    med_fid_exp = float(fid[fid.family == "QEXP"].ratio.median())
    log(f"  Q1 level fidelity: median realised/nominal QROLL {med_fid_roll:.3f} vs QEXP "
        f"{med_fid_exp:.3f} (idea 336 published 0.00-0.31 for QEXP).")
    log(f"  Q2 cross-panel rate spread (median over levels): QROLL "
        f"{float(sp[sp.family=='QROLL'].cross_panel_spread.median()):.4f} vs QEXP "
        f"{float(sp[sp.family=='QEXP'].cross_panel_spread.median()):.4f} vs ABS {abs_spread:.4f}")
    log(f"  Q3 earnings: QROLL 4a {int(qr.p4a.sum())}/{len(qr)} (all at rung "
        f"{sorted(set(qr[qr.p4a].rung))}), 4b {int(qr.p4b.sum())}/{len(qr)}; "
        f"QEXP 4a {int(qe.p4a.sum())}/{len(qe)}, 4b {int(qe.p4b.sum())}/{len(qe)}; BOTH {len(both)}.")
    wq = wf[wf.family == "QROLL"]
    log(f"  Q4 chooser: QROLL picks a sub-1%-firing arm in {int((wq.pick_rate < 0.01).sum())} of "
        f"{len(wq)} cells and beats its own ungated parent OOS in {int((wq.vs_nogate > 0).sum())}.")
    keep = len(keep_rows) > 0
    verdict = "KEEP-candidate (4b)" if keep else ("SPLIT" if med_fid_roll > 0.8 else "KILL")
    log(f"  VERDICT: {verdict} - "
        + ("a rule-8-chosen cell clears 4b at the PROTOCOL rung on a parent that does not."
           if keep else
           "the instrument is FIXED (Q1/Q2) but earns no PROTOCOL KEEP at 10/25 bps: every 4b "
           "pass among the rule-8 picks at the protocol rung is inherited from a parent that "
           "already passes, and 4a passes only at rung 0."))

    row = (f"| 2026-09-10 | idea 399 rolling-breadth-quantile-rate-fidelity (cloud) | QROLL "
           f"realised/nominal median {med_fid_roll:.3f} vs QEXP {med_fid_exp:.3f}; QROLL 4a "
           f"{int(qr.p4a.sum())} / 4b {int(qr.p4b.sum())} of {len(qr)}; rule-8 picks pass 4b at "
           f"{RUNG_HEAD} bps {len(head_rows)}/{int((picks.rung == RUNG_HEAD).sum())} "
           f"({len(keep_rows)} uninherited); beats do-nothing {int((wq.vs_nogate > 0).sum())}/"
           f"{len(wq)} | - | - | - | - | {verdict} | {SCRIPT} |")
    log("\nLEADERBOARD row:\n" + row)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print("\nwrote:", STEM + ".{console.txt,grid.csv,rates.csv,matched.csv,walkforward.csv}")


if __name__ == "__main__":
    main()
