#!/usr/bin/env python3
"""Idea 336 - "re-price-the-fixed-ABSOLUTE-breadth-threshold-as-a-quantile":
is idea 42's cross-panel collapse the THRESHOLD'S UNITS or the INSTRUMENT?

The finding this run exists to re-price
--------------------------------------
Idea 42 ran a 9-point grid, B in {0.30, 0.40, 0.50} x depth in {0.25, 0.50, 1.00}, where the
overlay carries the book at (1 - depth) of its exposure whenever the panel's own 200d-MA breadth
falls below the ABSOLUTE level B.  Its committed console reports that the SAME three B values fire
on wildly different shares of days across panels, because the panels' breadth distributions differ:

    U56       breadth mean 0.687   share below 0.30/0.40/0.50 = 0.070 / 0.123 / 0.167
    B136      breadth mean 0.685   share below 0.30/0.40/0.50 = 0.065 / 0.109 / 0.152
    SMALL484  breadth mean 0.386   share below 0.30/0.40/0.50 = 0.258 / 0.522 / 0.838

So on SMALL484 the depth=1.00 arms are a near-permanent flight to cash (84% of days at B=0.50),
and idea 42's walk-forward chose exactly there: OOS Sharpe 0.013 against the ungated parent's
0.416, i.e. -0.403 against DOING NOTHING.  A rule that is in cash 84% of the time is not being
tested as a timing signal at all; it is being tested as a cash position.

THE QUESTION, stated so it can be answered either way
-----------------------------------------------------
Re-run the same 9-point grid with the threshold expressed in the panel's OWN units - a CAUSAL
EXPANDING QUANTILE q of that panel's breadth history through day t - and ask:

    Q1 (mechanics)  Does the quantile form actually equalise the firing rate ACROSS PANELS?  This
                    is the claim the queue's remedy rests on and it is measured, not assumed.  A
                    SECOND, separate question - does the realised rate equal the nominal q? - is
                    measured beside it, because a causal EXPANDING quantile only delivers rate q
                    if breadth is exchangeable over the sample, and breadth is not.  The two are
                    reported apart so a pass on one is never read as a pass on the other.
    Q2 (units)      Once SMALL484 stops being 84%-in-cash, does the -0.403 collapse go away?
    Q3 (instrument) If it does, is what remains an EDGE, or merely a smaller loss?  The bar is
                    not "less bad than the collapse" - it is the ungated parent (do nothing) and
                    the matched-mean-gross static twin (a gross dial with no timing at all).

Q2 and Q3 are different questions and the record has repeatedly confused them.  A gate that stops
destroying 40 bps of Sharpe has not thereby earned anything.

The decomposition (this is the point of the run)
------------------------------------------------
For each panel and each of idea 42's three B values, three arms are run on the SAME base book:

    ABS(B)          idea 42 verbatim: gate when breadth_t < B.        Fires at f_panel(B).
    QUANT(q)        gate when breadth_t < Q_t(q), the causal expanding q-quantile, with
                    q = f_U56(B) = {0.070, 0.123, 0.167} - U56's own realised rates under idea
                    42's own B, read off idea 42's committed console.  THIS IS THE TUNED FAMILY.
    ABSMATCH(q)     an ABSOLUTE threshold B' set to the panel's own full-sample breadth quantile
                    at QUANT(q)'s REALISED daily firing rate, so ABSMATCH fires at exactly the
                    same rate as QUANT(q) on that panel.  Rate-matched by construction.

Then, on any metric X,

    dTOTAL = X[QUANT(q)] - X[ABS(B)]         what re-expressing the threshold does in total
    dFORM  = X[QUANT(q)] - X[ABSMATCH(q)]    same realised RATE, quantile vs absolute selection
    dRATE  = X[ABSMATCH(q)] - X[ABS(B)]      both ABSOLUTE, different rate

and dTOTAL = dFORM + dRATE identically.  If dRATE carries the movement and dFORM is ~0, the
queue's suspicion is right: idea 42's cross-panel result was a firing-RATE artefact and the two
threshold forms are the same instrument seen at different frequencies.  If dFORM is large, the
quantile is a genuinely different signal and the units story is wrong.

  HONESTY FLAG ON ABSMATCH: its B' is read off the panel's FULL-SAMPLE breadth distribution, so it
  carries look-ahead in the RATE (its daily gate is a plain absolute threshold).  It exists only to
  hold the firing rate fixed inside the decomposition.  It is never a tuned point, it is excluded
  from the walk-forward chooser, and NO KEEP/KILL verdict in this file is taken from it.  A third
  family, DIAG (the quantile form at the panel's own NOMINAL rate f_panel(B)), is carried in the
  grid as a secondary read and is flagged the same way.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q      expanding-quantile level, in {0.07, 0.12, 0.17}
              = U56's own realised firing rates under idea 42's B = {0.30, 0.40, 0.50}, read off
              idea 42's committed console BEFORE any number in this file was computed.  This is
              the queue's own mapping; nothing was searched to find it.
    2. depth  cut depth, in {0.25, 0.50, 1.00}   (idea 42's own three values, 1.00 = full cash)
    9 points, ALL reported, at every panel / gross / cadence / cost rung.

Reported axes, NEVER tuned or selected on
    panel    U56 / B136 / SMALL484        (idea 42's three, same construction, same SMALL484)
    gross    0.75 / 0.85 / 1.00           (0.75 = live gross; the chooser only ever sees 0.75)
    cadence  D / W                        (D = gate may move any day; W = only on rebalance days)
    cost     0 / 10 / 25 bps              (10 = PROTOCOL rule 2; 0 and 25 classify 10-bps artefacts)

Controls (structural, none selected on its own result)
    NOGATE            the ungated EWALL parent at the same gross - the DO-NOTHING bar for Q3.
    MATCHED-GROSS     static gross G * mean(mult), no gate at all - the "gross dial in a timing
                      costume" bar for Q3.
    ABS(B)            idea 42's own arms, re-run here, and asserted against its committed grid.
    RULES v2 / RULES v1 / SPY             PROTOCOL rule 3.

Rule 8 walk-forward (required)
    (q, depth) chosen on 2009-2016 by IS Sharpe alone at G=0.75, per panel / cadence / rung;
    2017-2026 read once.  Reported against the ungated parent OOS (do nothing), the grid mean OOS
    (the anchor), the best OOS cell (regret), RULES v2 OOS and SPY OOS.  The identical chooser is
    run over idea 42's ABS grid so the two forms are compared under the SAME selection rule.

Verdicts, evaluated at EVERY grid point
    4a: Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2's.
    4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.
    G3  idea 42's committed grid.csv, every ABS arm this run re-runs, joined and differenced.
    G4  the decomposition identity dTOTAL = dFORM + dRATE, to machine precision.
    G5  Q1 as a testable claim: the CROSS-PANEL SPREAD of the quantile gate's realised firing rate
        collapses relative to the absolute gate's.  Reported alongside it, NOT as a pass/fail but
        as a measured property: the LEVEL fidelity of the causal expanding quantile, i.e. realised
        rate vs nominal q.  These are two different claims and the run reports both separately.

Data: committed caches only, no network.  SURVIVORSHIP: all three panels are current-constituent
lists, so CAGR and drawdown LEVELS are optimistic; the gated-vs-parent and gated-vs-matched-gross
CONTRASTS are the durable part.  SMALL484 starts 2010-01-04, so its halves are not the same
calendar halves as U56/B136's.

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

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 0.85, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]              # tuned param 1 - U56's own realised rates under idea 42's B
BS = [0.30, 0.40, 0.50]              # idea 42's absolute levels (comparand, not tuned here)
B2Q = dict(zip(BS, QS))
DEPTHS = [0.25, 0.50, 1.00]          # tuned param 2
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
MINQ = 252                           # expanding quantile warm-up, in breadth observations
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT_GRID = OUT / "2026-09-07_breadth-gate-on-v2_B.grid.csv"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 2000)


# ---------------------------------------------------------------- primitives (idea 42 verbatim)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def breadth(px):
    """Idea 40/42's definition: share of the WHOLE panel trading above its own 200d MA."""
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def _cadence(m, idx):
    """W: the multiplier may only change on the book's own weekly rebalance days."""
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def gate_mult_abs(px, B, depth, cadence):
    br = breadth(px)
    m = pd.Series(1.0, index=px.index).where(~(br < B), 1.0 - depth)
    m = m.where(br.notna(), 1.0)
    return _cadence(m, px.index) if cadence == "W" else m


def gate_mult_quant(px, q, depth, cadence, thr=None):
    """CAUSAL expanding quantile: Q_t = q-quantile of breadth_1..t (>= MINQ observations).
    Gate ON when breadth_t < Q_t.  Uses information through t only; executed at t+1."""
    br = breadth(px)
    if thr is None:
        thr = br.expanding(min_periods=MINQ).quantile(q)
    m = pd.Series(1.0, index=px.index).where(~(br < thr), 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return _cadence(m, px.index) if cadence == "W" else m


def apply_gate(r_base, mult, gross, cost_bps):
    """Carry the book at mult of its exposure; the switch executes the NEXT day and pays
    cost_bps on |d mult| * gross of notional on the day it takes effect (idea 40/42's convention)."""
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def tests_4b(r, spy):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def fail_4b(r, spy):
    f = [k for k, v in tests_4b(r, spy).items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def summarise(r, spy, base_v2, mult=None):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy)
    ms = metrics(spy)
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=m_is["Sharpe"], OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
             OOS_MaxDD=m_oos["MaxDD"],
             CAGR_margin=m["CAGR"] - 0.70 * ms["CAGR"],
             DD_margin=0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
             p4a=verdict_4a(r, base_v2), p4b=all(t.values()), fail4b=fail_4b(r, spy))
    d["on_share"] = float((mult < 1.0).mean()) if mult is not None else np.nan
    d["mean_mult"] = float(mult.mean()) if mult is not None else 1.0
    return d


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- panel run
def run_panel(panel, px, log):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    br_full = breadth(px)
    br = br_full.loc[start:]

    log(f"\n{'='*160}\nPANEL {panel}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"eval from {start.date()}")
    log(f"  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%} | 4b bars: CAGR floor "
        f"{0.70*ms['CAGR']:.2%}, DD cap {-0.60*abs(ms['MaxDD']):.2%}, halves "
        f"{half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}, OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
    f_panel = {B: float((br < B).mean()) for B in BS}
    log(f"  breadth_t: mean {br.mean():.3f}, median {br.median():.3f}, "
        f"share below 0.30/0.40/0.50 = {f_panel[0.30]:.3f}/{f_panel[0.40]:.3f}/{f_panel[0.50]:.3f}")

    # causal expanding quantile thresholds, computed once
    thr_q = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_diag = {B: br_full.expanding(min_periods=MINQ).quantile(f_panel[B]) for B in BS}
    armed = float(thr_q[QS[0]].loc[start:].notna().mean())
    log(f"  expanding-quantile gate armed on {armed:.3f} of eval days (min_periods={MINQ} breadth obs); "
        f"before that the gate is OFF for every quantile arm.")

    # ---- base books: one backtest per (gross) at 0 bps, all rungs derived (G1 asserts this)
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    v2_0 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    v1_0 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)

    def rung(pair, c):
        r, t = pair
        return r - t * c / 1e4

    refs = {c: {"RULES v2 (live)": rung((v2_0["returns"].loc[start:], v2_0["turnover"].loc[start:]), c),
                "RULES v1": rung((v1_0["returns"].loc[start:], v1_0["turnover"].loc[start:]), c),
                "SPY": spy} for c in RUNGS}

    # ---- ABSMATCH: absolute threshold set at the panel's full-sample breadth quantile
    #      corresponding to QUANT(q)'s REALISED daily firing rate.  Look-ahead in the rate only.
    rate_q = {q: float((br < thr_q[q].loc[start:]).mean()) for q in QS}
    bprime = {q: float(br.quantile(rate_q[q])) for q in QS}
    log("  ABSMATCH construction (rate-matched control, look-ahead in the RATE, never tuned): "
        + ", ".join(f"q={q:.2f} realised {rate_q[q]:.4f} -> B'={bprime[q]:.4f}" for q in QS))

    # ---- multipliers, computed once per (family, level, depth, cadence)
    mults = {}
    for cad in CADENCES:
        for d in DEPTHS:
            for q in QS:
                mults[("QUANT", q, d, cad)] = gate_mult_quant(px, q, d, cad, thr=thr_q[q]).loc[start:]
                mults[("ABSMATCH", q, d, cad)] = gate_mult_abs(px, bprime[q], d, cad).loc[start:]
            for B in BS:
                mults[("ABS", B, d, cad)] = gate_mult_abs(px, B, d, cad).loc[start:]
                mults[("DIAG", B, d, cad)] = gate_mult_quant(px, f_panel[B], d, cad,
                                                             thr=thr_diag[B]).loc[start:]

    # ---- the full grid
    out = []
    for c in RUNGS:
        v2 = refs[c]["RULES v2 (live)"]
        for nm, r in refs[c].items():
            out.append(dict(panel=panel, rung=c, gross=np.nan, family="ref", arm=nm,
                            level=np.nan, q_used=np.nan, depth=np.nan, cadence="-",
                            **summarise(r, spy, v2)))
        for g in GROSSES:
            rb = rung(base0[g], c)
            out.append(dict(panel=panel, rung=c, gross=g, family="control", arm=f"NOGATE g{g:.2f}",
                            level=np.nan, q_used=np.nan, depth=0.0, cadence="-",
                            **summarise(rb, spy, v2)))
            for cad in CADENCES:
                for d in DEPTHS:
                    for q in QS:
                        m = mults[("QUANT", q, d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        out.append(dict(panel=panel, rung=c, gross=g, family="QUANT",
                                        arm=f"QUANT q{q:.2f} d{d:.2f} {cad} g{g:.2f}",
                                        level=q, q_used=q, depth=d, cadence=cad,
                                        **summarise(rg, spy, v2, mult=me)))
                        m = mults[("ABSMATCH", q, d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        out.append(dict(panel=panel, rung=c, gross=g, family="ABSMATCH",
                                        arm=f"ABSMATCH B'{bprime[q]:.3f} (q{q:.2f}) d{d:.2f} {cad} g{g:.2f}",
                                        level=q, q_used=q, depth=d, cadence=cad,
                                        **summarise(rg, spy, v2, mult=me)))
                    for B in BS:
                        m = mults[("ABS", B, d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        out.append(dict(panel=panel, rung=c, gross=g, family="ABS",
                                        arm=f"ABS B{B:.2f} d{d:.2f} {cad} g{g:.2f}",
                                        level=B, q_used=np.nan, depth=d, cadence=cad,
                                        **summarise(rg, spy, v2, mult=me)))
                        m = mults[("DIAG", B, d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        out.append(dict(panel=panel, rung=c, gross=g, family="DIAG",
                                        arm=f"DIAG q=f({B:.2f})={f_panel[B]:.3f} d{d:.2f} {cad} g{g:.2f}",
                                        level=B, q_used=f_panel[B], depth=d, cadence=cad,
                                        **summarise(rg, spy, v2, mult=me)))

    # ---- Q3 control: matched-mean-gross static twin, headline rung, EVERY gross, QUANT arms
    matched = []
    v2 = refs[RUNG_HEAD]["RULES v2 (live)"]
    seen = {}
    for gg in GROSSES:
      rb = rung(base0[gg], RUNG_HEAD)
      for cad in CADENCES:
        for q in QS:
            for d in DEPTHS:
                rg, me = apply_gate(rb, mults[("QUANT", q, d, cad)], gg, RUNG_HEAD)
                g_eff = gg * float(me.mean())
                key = round(g_eff, 6)
                if key not in seen:
                    res = backtest(px, ewall_weights(px, g_eff), cost_bps=RUNG_HEAD, freq=FREQ)
                    seen[key] = res["returns"].loc[start:]
                rs = seen[key]
                mg, mst = metrics(rg), metrics(rs)
                matched.append(dict(panel=panel, gross=gg, cadence=cad, q=q, depth=d, g_eff=g_eff,
                                    gate_CAGR=mg["CAGR"], static_CAGR=mst["CAGR"],
                                    gate_Sharpe=mg["Sharpe"], static_Sharpe=mst["Sharpe"],
                                    dSharpe=mg["Sharpe"] - mst["Sharpe"],
                                    gate_OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"],
                                    static_OOS_Sharpe=metrics(rs.loc[OOS_START:])["Sharpe"],
                                    dOOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"]
                                                - metrics(rs.loc[OOS_START:])["Sharpe"],
                                    gate_MaxDD=mg["MaxDD"], static_MaxDD=mst["MaxDD"],
                                    dMaxDD=abs(mst["MaxDD"]) - abs(mg["MaxDD"]),
                                    gate_4b=all(tests_4b(rg, spy).values()),
                                    static_4b=all(tests_4b(rs, spy).values())))

    # ---- rule 8 walk-forward, run identically over QUANT and over ABS
    wf = []
    for fam, levels in (("QUANT", QS), ("ABS", BS)):
        for c in RUNGS:
            rb_c = rung(base0[G_HEAD], c)
            for cad in CADENCES:
                cells = {}
                for lv in levels:
                    for d in DEPTHS:
                        rg, _ = apply_gate(rb_c, mults[(fam, lv, d, cad)], G_HEAD, c)
                        cells[(lv, d)] = rg
                is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cells.items()}
                oos = {k: metrics(v.loc[OOS_START:]) for k, v in cells.items()}
                pick = min(is_s, key=lambda k: (-is_s[k], k[0], k[1]))
                best = max(oos, key=lambda k: oos[k]["Sharpe"])
                po = oos[pick]
                nog = metrics(rb_c.loc[OOS_START:])
                wf.append(dict(panel=panel, family=fam, rung=c, cadence=cad,
                               pick_level=pick[0], pick_depth=pick[1], IS_Sharpe=is_s[pick],
                               OOS_CAGR=po["CAGR"], OOS_Sharpe=po["Sharpe"], OOS_MaxDD=po["MaxDD"],
                               nogate_OOS_Sharpe=nog["Sharpe"], nogate_OOS_CAGR=nog["CAGR"],
                               grid_mean_OOS=float(np.mean([oos[k]["Sharpe"] for k in oos])),
                               best_OOS=oos[best]["Sharpe"],
                               regret=po["Sharpe"] - oos[best]["Sharpe"],
                               vs_nogate=po["Sharpe"] - nog["Sharpe"],
                               spy_OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                               v2_OOS=metrics(refs[c]["RULES v2 (live)"].loc[OOS_START:])["Sharpe"]))

    return pd.DataFrame(out), pd.DataFrame(matched), pd.DataFrame(wf), f_panel, armed


# ---------------------------------------------------------------- main
def main():
    lines = []

    def log(s=""):
        print(s)
        lines.append(str(s))

    log("=" * 160)
    log(f"Idea 336 re-price-the-fixed-ABSOLUTE-breadth-threshold-as-a-quantile (lane C) | {SCRIPT}")
    log("=" * 160)
    log("Book (fixed, idea 28/42's): EWALL(G) = equal weight every name above its own 200d MA with")
    log("  vol20 < 0.60, at G/E_t, weekly, next-day execution.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is LOW.  Three threshold forms:")
    log("  ABS(B)        breadth_t < B                     (idea 42 verbatim - the comparand)")
    log("  QUANT(q)      breadth_t < causal expanding q-quantile of the panel's own breadth (THIS IDEA)")
    log("  ABSMATCH(q)   absolute threshold B' at the panel quantile matching QUANT(q)'s REALISED rate;")
    log("  DIAG(q=f(B))  the quantile form at the panel's own nominal rate under B.  BOTH carry")
    log("                LOOK-AHEAD IN THE RATE: controls only, never tuned, never a verdict.")
    log(f"Tuned (2): q in {QS} (= U56's realised rates under idea 42's B={BS}) x depth in {DEPTHS}.")
    log(f"Reported, never tuned: gross {GROSSES}, cadence {CADENCES}, cost {RUNGS} bps, 3 panels.")

    # ---------------- G1: derived cost rung identity
    log("\n" + "=" * 160)
    log("[0] REPRODUCTION GATES")
    px0 = load_universe()
    r0 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=0, freq=FREQ)
    r25 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=25, freq=FREQ)
    d1 = float((r0["returns"] - r0["turnover"] * 25 / 1e4 - r25["returns"]).abs().max())
    log(f"  G1 derived rung r(c)=r(0)-turnover*c/1e4 vs live engine.backtest(25): max abs diff {d1:.3e}"
        f"  -> {'PASS' if d1 < 1e-12 else 'FAIL'}")
    assert d1 < 1e-12

    panels = [("U56", dict()), ("B136", dict(broad=True)), ("SMALL484", dict(small=True))]
    grids, matches, wfs, fps, armeds = [], [], [], {}, {}
    for name, kw in panels:
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            log(f"!! {name}: CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        g, m, w, fp, ar = run_panel(name, px, log)
        grids.append(g); matches.append(m); wfs.append(w); fps[name] = fp; armeds[name] = ar

    grid = pd.concat(grids, ignore_index=True)
    matched = pd.concat(matches, ignore_index=True)
    wf = pd.concat(wfs, ignore_index=True)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    matched.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---------------- G2 / G3
    log("\n" + "=" * 160)
    rep = grid[(grid.panel == "U56") & (grid.rung == RUNG_HEAD) & (grid.arm == "NOGATE g0.85")].iloc[0]
    ok2 = abs(rep.CAGR - 0.118) < 5e-4 and abs(rep.Sharpe - 1.05) < 5e-3 and abs(rep.MaxDD + 0.179) < 5e-4
    log("  G2 idea 84's ungated EWALL U56 g=0.85 @10bps published 11.8% / 1.05 / -17.9% / H 1.07 / 1.04")
    log(f"     this run: {rep.CAGR:.1%} / {rep.Sharpe:.2f} / {rep.MaxDD:.1%} / H {rep.H1:.2f} / {rep.H2:.2f}"
        f"  -> {'PASS' if ok2 else 'FAIL'} at published precision")

    if PARENT_GRID.exists():
        par = pd.read_csv(PARENT_GRID)
        par = par[par.family == "gate"].copy()
        par["key"] = list(zip(par.panel, par.rung, par.gross, par.B, par.depth, par.cadence))
        mine = grid[grid.family == "ABS"].copy()
        mine["key"] = list(zip(mine.panel, mine.rung, mine.gross, mine.level, mine.depth, mine.cadence))
        j = par.set_index("key")[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]].join(
            mine.set_index("key")[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]],
            lsuffix="_par", rsuffix="_new", how="inner")
        dmax = max(float((j[f"{c}_par"] - j[f"{c}_new"]).abs().max())
                   for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"])
        log(f"  G3 idea 42's committed ABS grid re-run here: {len(j)} rows joined "
            f"(of {len(par)} parent gate rows), max abs diff over 6 columns {dmax:.3e}"
            f"  -> {'PASS' if dmax < 1e-9 else 'FAIL'}")
        assert len(j) == 486 and dmax < 1e-9, (len(j), dmax)
    else:
        log("  G3 parent grid CSV missing - SKIPPED (this weakens the run; noted in the result).")

    # ---------------- G5 / Q1: does the quantile equalise firing rates?
    log("\n" + "=" * 160)
    log("[Q1] MECHANICS - firing rate by form and panel (10 bps, g=0.75, cadence D, depth 0.50;")
    log("     on_share is the share of EVAL days with the gate ON; the quantile arm is unarmed for")
    log("     its first ~year, so its rate is q * armed_share, not q).")
    sel = grid[(grid.rung == RUNG_HEAD) & (grid.gross == G_HEAD) & (grid.cadence == "D")
               & (grid.depth == 0.50) & grid.family.isin(["ABS", "QUANT", "ABSMATCH", "DIAG"])]
    piv = sel.pivot_table(index=["panel", "family"], columns="level", values="on_share")
    log(fmt(piv))
    log("\n  armed share of eval days by panel: " + ", ".join(f"{k} {v:.3f}" for k, v in armeds.items()))
    q_rows = grid[(grid.family == "QUANT") & (grid.cadence == "D") & (grid.rung == RUNG_HEAD)
                  & (grid.gross == G_HEAD) & (grid.depth == 0.50)]
    a_rows = grid[(grid.family == "ABS") & (grid.cadence == "D") & (grid.rung == RUNG_HEAD)
                  & (grid.gross == G_HEAD) & (grid.depth == 0.50)]
    spread_abs = {B: float(a_rows[a_rows.level == B].on_share.max()
                           - a_rows[a_rows.level == B].on_share.min()) for B in BS}
    spread_q = {q: float(q_rows[q_rows.level == q].on_share.max()
                         - q_rows[q_rows.level == q].on_share.min()) for q in QS}
    log("  ABS   on_share SPREAD across panels (max-min, per B): "
        + ", ".join(f"B={B:.2f} {spread_abs[B]:.3f}" for B in BS))
    log("  QUANT on_share SPREAD across panels (max-min, per q): "
        + ", ".join(f"q={q:.2f} {spread_q[q]:.3f}" for q in QS))
    g5 = max(spread_q.values()) < 0.02 and max(spread_q.values()) < min(spread_abs.values())
    log(f"  G5 (Q1, the CROSS-PANEL claim): max QUANT spread {max(spread_q.values()):.3f} vs "
        f"min ABS spread {min(spread_abs.values()):.3f}  -> {'PASS' if g5 else 'FAIL'}")
    log("\n  LEVEL FIDELITY (measured, NOT a pass/fail): realised daily firing rate vs the NOMINAL q.")
    log("  A causal EXPANDING quantile only fires at rate q if breadth is exchangeable over the")
    log("  sample; it is not, so the realised rate is reported here rather than assumed.")
    for _, r in q_rows.sort_values(["panel", "level"]).iterrows():
        log(f"    {r.panel:9s} q={r.level:.2f}  realised {r.on_share:.4f}  "
            f"ratio realised/q {r.on_share / r.level:.3f}")

    # ---------------- headline grid, ALL 9 tuned points, every panel/gross/cadence at 10 bps
    show = ["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "CAGR_margin", "DD_margin", "on_share", "mean_mult", "p4a", "p4b", "fail4b"]
    log("\n" + "=" * 160)
    log(f"[A] HEADLINE GRID @ {RUNG_HEAD} bps - all 9 QUANT points + 9 ABS + 9 ABSMATCH + 9 DIAG + controls + refs,")
    log("    every panel, every gross, both cadences.  CAGR_margin/DD_margin are signed distances to")
    log("    the 4b bars (+ = clears).  Full grid (all 3 rungs) is in the .grid.csv.")
    for panel, _ in panels:
        for g in GROSSES:
            sub = grid[(grid.panel == panel) & (grid.rung == RUNG_HEAD)
                       & (grid.gross.isna() | (grid.gross == g))]
            log(f"\n--- {panel} @ {RUNG_HEAD} bps, gross {g:.2f}")
            log(fmt(sub[show].set_index("arm")))

    # ---------------- [B] the decomposition
    log("\n" + "=" * 160)
    log("[B] DECOMPOSITION - is the cross-panel behaviour the RATE or the INSTRUMENT?")
    log("    dTOTAL = QUANT(q) - ABS(B)         (what re-expressing the threshold does in total)")
    log("    dFORM  = QUANT(q) - ABSMATCH(q)    (same REALISED rate, quantile vs absolute selection)")
    log("    dRATE  = ABSMATCH(q) - ABS(B)      (both ABSOLUTE thresholds, different firing rate)")
    log("    identity: dTOTAL = dFORM + dRATE.")
    dec = []
    for panel, _ in panels:
        for c in RUNGS:
            for g in GROSSES:
                for cad in CADENCES:
                    for d in DEPTHS:
                        for B in BS:
                            q = B2Q[B]
                            def get(fam, lv):
                                s = grid[(grid.panel == panel) & (grid.rung == c) & (grid.gross == g)
                                         & (grid.cadence == cad) & (grid.depth == d)
                                         & (grid.family == fam) & (grid.level == lv)]
                                return s.iloc[0]
                            a, qq, am = get("ABS", B), get("QUANT", q), get("ABSMATCH", q)
                            row = dict(panel=panel, rung=c, gross=g, cadence=cad, depth=d, B=B, q=q,
                                       abs_on=a.on_share, quant_on=qq.on_share, absmatch_on=am.on_share,
                                       rate_gap=abs(qq.on_share - am.on_share))
                            for col in ["Sharpe", "CAGR", "OOS_Sharpe", "MaxDD"]:
                                row[f"dTOTAL_{col}"] = qq[col] - a[col]
                                row[f"dFORM_{col}"] = qq[col] - am[col]
                                row[f"dRATE_{col}"] = am[col] - a[col]
                            dec.append(row)
    dec = pd.DataFrame(dec)
    dec.to_csv(OUT / f"{STEM}.decomposition.csv", index=False)
    ident = max(float((dec[f"dTOTAL_{c}"] - dec[f"dFORM_{c}"] - dec[f"dRATE_{c}"]).abs().max())
                for c in ["Sharpe", "CAGR", "OOS_Sharpe", "MaxDD"])
    log(f"  G4 identity dTOTAL = dFORM + dRATE: max abs residual {ident:.3e} over {len(dec)} cells"
        f"  -> {'PASS' if ident < 1e-12 else 'FAIL'}")
    log(f"  rate match quality |quant_on - absmatch_on|: max {dec.rate_gap.max():.4f}, "
        f"median {dec.rate_gap.median():.4f}  (0 would be exact; cadence W smoothing is the residual)")
    for col in ["Sharpe", "OOS_Sharpe", "CAGR"]:
        log(f"\n  --- {col}: mean (and max |.|) of each component, by panel")
        t = dec.groupby("panel").agg(**{
            "dTOTAL_mean": (f"dTOTAL_{col}", "mean"), "dTOTAL_absmax": (f"dTOTAL_{col}", lambda s: s.abs().max()),
            "dFORM_mean": (f"dFORM_{col}", "mean"), "dFORM_absmax": (f"dFORM_{col}", lambda s: s.abs().max()),
            "dRATE_mean": (f"dRATE_{col}", "mean"), "dRATE_absmax": (f"dRATE_{col}", lambda s: s.abs().max())})
        log(fmt(t))
        share = dec.groupby("panel").apply(
            lambda s: float(s[f"dRATE_{col}"].abs().sum() / max(s[f"dRATE_{col}"].abs().sum()
                                                                + s[f"dFORM_{col}"].abs().sum(), 1e-15)))
        log("  share of total absolute movement carried by the RATE: "
            + ", ".join(f"{k} {v:.1%}" for k, v in share.items()))

    log("\n  The specific cell the queue names (SMALL484, B=0.50 -> q=0.17, depth=1.00, D, g=0.75, 10 bps):")
    z = dec[(dec.panel == "SMALL484") & (dec.B == 0.50) & (dec.depth == 1.00) & (dec.cadence == "D")
            & (dec.gross == G_HEAD) & (dec.rung == RUNG_HEAD)]
    log(fmt(z[["abs_on", "quant_on", "absmatch_on", "dTOTAL_OOS_Sharpe", "dFORM_OOS_Sharpe",
               "dRATE_OOS_Sharpe", "dTOTAL_Sharpe", "dFORM_Sharpe", "dRATE_Sharpe"]]))

    # ---------------- [C] Q3 - does the quantile gate EARN anything?
    log("\n" + "=" * 160)
    log("[C] Q3 - IS WHAT REMAINS AN EDGE?  Every QUANT point vs its OWN ungated parent (do nothing),")
    log("    same panel / rung / gross / cadence.  A gate that only stops destroying has earned nothing.")
    gq = grid[grid.family == "QUANT"].copy()
    nog = grid[grid.family == "control"].set_index(["panel", "rung", "gross"])
    for col in ["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "OOS_CAGR"]:
        gq[f"par_{col}"] = [nog.loc[(p, r, g), col] for p, r, g in zip(gq.panel, gq.rung, gq.gross)]
    gq["dCAGR"] = gq.CAGR - gq.par_CAGR
    gq["dSharpe"] = gq.Sharpe - gq.par_Sharpe
    gq["dOOS_Sharpe"] = gq.OOS_Sharpe - gq.par_OOS_Sharpe
    gq["dMaxDD"] = gq.par_MaxDD.abs() - gq.MaxDD.abs()
    n = len(gq)
    log(f"  QUANT points: {n}")
    for c, lab in [("dCAGR", "CAGR"), ("dSharpe", "Sharpe"), ("dOOS_Sharpe", "OOS Sharpe"),
                   ("dMaxDD", "MaxDD (+ = shallower)")]:
        log(f"    {lab:24s} > 0 in {int((gq[c] > 0).sum()):4d}/{n} ({(gq[c] > 0).mean():6.1%});  "
            f"median {gq[c].median():+.4f}, min {gq[c].min():+.4f}, max {gq[c].max():+.4f}")
    log("\n  by panel (mean deltas vs the ungated parent, all rungs/gross/cadences/depths):")
    log(fmt(gq.groupby("panel")[["dCAGR", "dSharpe", "dOOS_Sharpe", "dMaxDD"]].mean()))
    log("\n  same table for the ABS family (idea 42's own arms), for contrast:")
    ga = grid[grid.family == "ABS"].copy()
    for col in ["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]:
        ga[f"par_{col}"] = [nog.loc[(p, r, g), col] for p, r, g in zip(ga.panel, ga.rung, ga.gross)]
    ga["dCAGR"] = ga.CAGR - ga.par_CAGR
    ga["dSharpe"] = ga.Sharpe - ga.par_Sharpe
    ga["dOOS_Sharpe"] = ga.OOS_Sharpe - ga.par_OOS_Sharpe
    ga["dMaxDD"] = ga.par_MaxDD.abs() - ga.MaxDD.abs()
    log(fmt(ga.groupby("panel")[["dCAGR", "dSharpe", "dOOS_Sharpe", "dMaxDD"]].mean()))

    log("\n  MATCHED-MEAN-GROSS twin (10 bps, g=0.75): the gate vs a static gross at its own mean")
    log("  exposure.  dSharpe > 0 means the gate's TIMING adds something a plain gross dial does not.")
    log(fmt(matched.set_index(["panel", "cadence", "q", "depth"])[
        ["g_eff", "gate_Sharpe", "static_Sharpe", "dSharpe", "gate_OOS_Sharpe", "static_OOS_Sharpe",
         "dOOS_Sharpe", "dMaxDD", "gate_4b", "static_4b"]]))
    log(f"\n  dSharpe > 0 in {int((matched.dSharpe > 0).sum())}/{len(matched)}; "
        f"dOOS_Sharpe > 0 in {int((matched.dOOS_Sharpe > 0).sum())}/{len(matched)}; "
        f"median dSharpe {matched.dSharpe.median():+.4f}, median dOOS {matched.dOOS_Sharpe.median():+.4f}")
    log("  by panel (mean over gross/cadence/q/depth):")
    log(fmt(matched.groupby("panel")[["dSharpe", "dOOS_Sharpe", "dMaxDD"]].mean()))
    log("  4b passes among these 10-bps cells: gate " f"{int(matched.gate_4b.sum())}/{len(matched)}, "
        f"matched-gross twin {int(matched.static_4b.sum())}/{len(matched)}; "
        f"gate passes where the twin FAILS: {int((matched.gate_4b & ~matched.static_4b).sum())}")

    # ---------------- [D] KEEP paths over the whole grid
    log("\n" + "=" * 160)
    log("[D] KEEP PATHS over every grid point (PROTOCOL rule 4, both paths, all rungs).")
    tab = grid[grid.family.isin(["QUANT", "ABS", "ABSMATCH", "DIAG"])].groupby(["family", "rung"]).agg(
        n=("p4a", "size"), pass4a=("p4a", "sum"), pass4b=("p4b", "sum"))
    log(fmt(tab))
    p4b = grid[(grid.p4b) & grid.family.isin(["QUANT", "ABS"])]
    if len(p4b):
        log(f"\n  4b passes ({len(p4b)}):")
        log(fmt(p4b[["panel", "rung", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                     "OOS_Sharpe", "CAGR_margin", "DD_margin"]].set_index("panel")))
    else:
        log("\n  4b passes: NONE anywhere in the grid (QUANT or ABS, any panel/gross/cadence/rung).")
    p4a = grid[(grid.p4a) & grid.family.isin(["QUANT", "ABS"])]
    log(f"  4a passes: {len(p4a)}"
        + ("" if not len(p4a) else "\n" + fmt(p4a[["panel", "rung", "arm", "Sharpe", "MaxDD", "H1", "H2"]])))

    # ---------------- [E] rule 8 walk-forward
    log("\n" + "=" * 160)
    log("[E] RULE 8 WALK-FORWARD - (level, depth) chosen on 2009-2016 IS Sharpe ONLY, at g=0.75;")
    log("    2017-2026 read once.  vs_nogate is the number that matters: OOS Sharpe minus the")
    log("    ungated parent's OOS Sharpe, i.e. what the overlay earned over DOING NOTHING.")
    log(fmt(wf.set_index(["panel", "family", "rung", "cadence"])[
        ["pick_level", "pick_depth", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "nogate_OOS_Sharpe", "vs_nogate", "grid_mean_OOS", "best_OOS", "regret", "spy_OOS", "v2_OOS"]]))
    log("\n  vs_nogate summary by family x panel (mean over rungs and cadences):")
    log(fmt(wf.pivot_table(index="panel", columns="family", values="vs_nogate")))
    log("  OOS Sharpe of the walk-forward pick, by family x panel:")
    log(fmt(wf.pivot_table(index="panel", columns="family", values="OOS_Sharpe")))
    log(f"  chooser beats do-nothing OOS: QUANT {int((wf[wf.family=='QUANT'].vs_nogate>0).sum())}"
        f"/{len(wf[wf.family=='QUANT'])}, ABS {int((wf[wf.family=='ABS'].vs_nogate>0).sum())}"
        f"/{len(wf[wf.family=='ABS'])}")

    # ---------------- verdict
    log("\n" + "=" * 160)
    log("[F] VERDICT")
    sm = wf[(wf.panel == "SMALL484") & (wf.rung == RUNG_HEAD) & (wf.cadence == "D")]
    for _, r in sm.iterrows():
        log(f"  SMALL484 @10bps cadence D, family {r.family}: pick ({r.pick_level}, {r.pick_depth}) "
            f"-> OOS Sharpe {r.OOS_Sharpe:.3f} vs do-nothing {r.nogate_OOS_Sharpe:.3f} "
            f"(vs_nogate {r.vs_nogate:+.3f})")
    q_beats = int((gq.dOOS_Sharpe > 0).sum())
    log(f"  Q2 (units): see [B] - the share of cross-form movement carried by the RATE, per panel.")
    log(f"  Q3 (instrument): QUANT beats its own ungated parent on OOS Sharpe in {q_beats}/{n} points;"
        f" beats its matched-gross twin in {int((matched.dOOS_Sharpe > 0).sum())}/{len(matched)}.")
    log(f"  4b passes among tuned QUANT points: {int(grid[(grid.family=='QUANT')].p4b.sum())}")
    log(f"  4a passes among tuned QUANT points: {int(grid[(grid.family=='QUANT')].p4a.sum())}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(lines) + "\n")
    print(f"\nwrote {STEM}.grid.csv / .matched.csv / .walkforward.csv / .decomposition.csv / .console.txt")


if __name__ == "__main__":
    main()
