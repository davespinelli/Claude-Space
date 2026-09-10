#!/usr/bin/env python3
"""Idea 399 - "does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate".

The finding this run exists to re-price
---------------------------------------
Idea 336 re-expressed idea 42's ABSOLUTE breadth gate (`breadth_t < B`) as a CAUSAL EXPANDING
quantile (`breadth_t < Q_t(q)`, Q_t computed on breadth_1..t) and published, as its Q1 LEVEL
fidelity row:

    realised firing rate / nominal q, q = 0.07 / 0.12 / 0.17
        U56       0.032 / 0.270 / 0.306
        B136      0.000 / 0.207 / 0.277
        SMALL484  0.004 / 0.148 / 0.266

i.e. the estimator under-fires its own nominal level by 3-30x on every panel, and q = 0.07 is
INERT (fires on ~0.2% of days, or never).  The mechanism idea 336 named: an EXPANDING quantile is
anchored by the 2008-2011 breadth lows, breadth never revisits them, so the low quantiles of the
expanding distribution sit permanently below anything the later sample produces.

That matters because idea 336's rule-8 chooser then PICKED q = 0.07 in 5 of 6 cells: it selected
an arm that does nothing, in-sample Sharpe being indistinguishable from the ungated parent's.  Its
Q3 KILL ("on the panel the idea was raised for the gate is worth exactly nothing", dOOS Sharpe
-0.001 on SMALL484) was therefore measured on an instrument that, at the level the chooser liked,
never fired.

THE QUESTION, stated so it can be answered either way
-----------------------------------------------------
Replace the EXPANDING estimator with a ROLLING one - Q_t(q) computed on breadth over the trailing
w trading days only, so the anchor rolls off - and ask, in this order:

    Q1 (mechanics, pure measurement, nothing tuned)
        Does a rolling window restore RATE FIDELITY, realised/nominal -> 1?  And does it keep the
        property idea 336 bought the quantile form for in the first place, a firing rate that is
        EQUAL ACROSS PANELS (its Q1 "ABS spread 0.193/0.413/0.686 -> QUANT spread 0.002/0.015/
        0.007")?  These are two different claims - level fidelity and cross-panel equality - and
        the expanding form passes the second while failing the first.  Both are reported apart.

    Q2 (does it change the KILL)  If ROLL fires at its nominal rate, the gate is finally being
        tested as a timing signal rather than as a permanently-off clause.  Re-run idea 336's Q3
        comparison on the ROLL family: gate vs its own UNGATED parent (do nothing), and gate vs
        its MATCHED-MEAN-GROSS static twin (a gross dial in a timing costume).  If ROLL still
        earns nothing, idea 336's KILL survives its own diagnosis and is now measured on a live
        instrument.  If ROLL earns something, the KILL was an estimator artefact.

    Q3 (rule 8)  Does the chooser stop picking an inert arm, and does that buy any OOS Sharpe?

Q1 passing does NOT imply Q2 passing.  The record has repeatedly read "the instrument now fires"
as "the instrument now works"; those are separate and are reported separately here.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. w      rolling-window length, in {252, 504, 756, 1260} trading days (1y, 2y, 3y, 5y)
    2. depth  cut depth, in {0.25, 0.50, 1.00}      (idea 42/336's own three; 1.00 = full cash)
    12 points, ALL reported, at every panel / q / gross / cadence / cost rung.

    q is NOT a tuned parameter here and the chooser never sees more than one value of it.  It is
    PRE-REGISTERED at q = 0.12, the middle of idea 336's own {0.07, 0.12, 0.17} (which are U56's
    realised rates under idea 42's B = {0.30, 0.40, 0.50}, read off idea 42's committed console).
    q = 0.07 and q = 0.17 are carried through the whole grid as a REPORTED, NEVER-SELECTED-ON
    robustness axis; the rule-8 chooser is re-run inside each of them separately so a q-dependence
    is visible, but no q is chosen by any result in this file.

Reported axes, never tuned or selected on
    panel    U56 / B136 / SMALL484   (idea 336's three panels, same construction, SMALL484 = the
                                      un-filtered small cache, NOT the record's later SMALL439)
    gross    0.75 / 0.85 / 1.00      (0.75 = live gross; the chooser only ever sees 0.75)
    cadence  D / W                   (D = gate may move any day; W = only on rebalance days)
    cost     0 / 10 / 25 bps         (10 = PROTOCOL rule 2; 0 and 25 classify 10-bps artefacts)

Families
    EXP(q)      idea 336 verbatim, expanding min_periods=252.  The COMPARAND, re-run here and
                asserted against idea 336's committed fidelity triple (gate G2).
    ROLL(w,q)   this run's instrument: trailing-w quantile, min_periods=w.
    NOGATE      the ungated EWALL parent at the same gross - the DO-NOTHING bar.
    MGROSS      matched-mean-gross twin, built idea 336's way: engine.backtest re-run with EW
                weights at static gross g * mean(mult), no gate at all.
    MGSCALE     the same idea built by SCALING the parent's return series by mean(mult).  Carried
                because Sharpe is scale-invariant, so THIS twin's Sharpe is identically the
                parent's - running both measures how much of the record's "gate beats its
                matched-gross twin" bar is a real second bar and how much is the do-nothing bar
                wearing a different name.
    RULES v2 (live) / RULES v1 / SPY   - PROTOCOL rule 3.

Rule 8 walk-forward (required, PROTOCOL rule 8)
    (w, depth) chosen on 2009-2016 by IS Sharpe alone, at g = 0.75 and the pre-registered q, per
    panel / cadence / rung; 2017-2026 read ONCE.  Reported against the ungated parent OOS (do
    nothing), the grid mean OOS (anchor), the best OOS cell (regret), RULES v2 OOS and SPY OOS.
    The identical chooser is run over the EXP family's (q, depth) grid so the two estimators are
    compared under the SAME selection rule, exactly as idea 336 compared QUANT against ABS.

Verdicts, evaluated at EVERY grid point (PROTOCOL rule 4)
    4a: Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2's.
    4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

Reproduction gates, printed in section [0] before any new number is read
    G1  derived cost rung r(c) = r(0) - turnover * c / 1e4 vs a live engine.backtest(cost_bps=c).
    G2  idea 336's committed EXP rate-fidelity triple, per panel, re-computed here.
    G3  the firing-rate arithmetic: realised rate == mean(breadth_t < thr_t) over the same day set
        the summary tables use, computed two independent ways.
    G4  idea 84's ungated EWALL U56 g=0.85 @10bps reference book: 11.8% / 1.05 / -17.9%.

Data: committed caches only, no network.  SURVIVORSHIP: all three panels are current-constituent
lists, so CAGR and drawdown LEVELS are optimistic; the gated-vs-parent and gated-vs-matched-gross
CONTRASTS are the durable part.  Panels are truncated to their common last date so the three are
read over the same tail; SMALL484 starts 2010-01-04, so its halves are not the same calendar
halves as U56/B136's.

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
QS = [0.07, 0.12, 0.17]              # idea 336's own three levels; REPORTED axis, never chosen
Q_REG = 0.12                         # PRE-REGISTERED q for the headline / rule-8 chooser
WS = [252, 504, 756, 1260]           # tuned param 1
DEPTHS = [0.25, 0.50, 1.00]          # tuned param 2
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
MINQ = 252                           # idea 336's expanding warm-up, in breadth observations
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# idea 336's committed Q1 LEVEL-fidelity row (realised rate / nominal q), for gate G2
IDEA336_FIDELITY = {"U56": [0.032, 0.270, 0.306],
                    "B136": [0.000, 0.207, 0.277],
                    "SMALL484": [0.004, 0.148, 0.266]}
IDEA336_ABS_SPREAD = [0.193, 0.413, 0.686]      # its ABS on_share cross-panel spreads
IDEA336_QUANT_SPREAD = [0.002, 0.015, 0.007]    # its QUANT on_share cross-panel spreads
IDEA84_U56_EW085 = (0.118, 1.05, -0.179)        # gate G4

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- primitives (idea 42/336 verbatim)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def breadth(px):
    """Idea 40/42/336's definition: share of the WHOLE panel trading above its own 200d MA.
    SPY is a benchmark column, never a constituent, and is dropped."""
    p = px.drop(columns=["SPY"], errors="ignore")
    above = p > p.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def _cadence(m, idx):
    """W: the multiplier may only change on the book's own weekly rebalance days."""
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def gate_mult(px, thr, depth, cadence):
    """Gate ON (carry the book at 1 - depth) when breadth_t < thr_t.  thr uses information
    through t only; the switch executes at t+1 (apply_gate shifts)."""
    br = breadth(px)
    m = pd.Series(1.0, index=px.index).where(~(br < thr), 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return _cadence(m, px.index) if cadence == "W" else m


def apply_gate(r_base, mult, gross, cost_bps):
    """Carry the book at mult of its exposure; the switch executes the NEXT day and pays
    cost_bps on |d mult| * gross of notional on the day it takes effect (idea 40/42/336's
    convention, reproduced verbatim so the two runs are comparable)."""
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def tests_4b(r, spy_stats):
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > spy_stats["H1"], "H2": h2 > spy_stats["H2"],
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > spy_stats["OOS_Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(spy_stats["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * spy_stats["CAGR"]}


def summarise(r, spy_stats, base_v2, mult=None):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy_stats)
    fails = [k for k, v in t.items() if not v]
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=m_is["Sharpe"], OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
             OOS_MaxDD=m_oos["MaxDD"],
             CAGR_margin=m["CAGR"] - 0.70 * spy_stats["CAGR"],
             DD_margin=0.60 * abs(spy_stats["MaxDD"]) - abs(m["MaxDD"]),
             p4a=verdict_4a(r, base_v2), p4b=not fails, fail4b=",".join(fails) if fails else "-")
    d["on_share"] = float((mult < 1.0).mean()) if mult is not None else np.nan
    d["mean_mult"] = float(mult.mean()) if mult is not None else 1.0
    return d


def spy_summary(spy):
    m = metrics(spy)
    h1, h2 = half_sharpes(spy)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"])


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- panels
def load_panels():
    u = load_universe()
    b = load_universe(broad=True)
    s = load_universe(small=True)                   # SMALL484: idea 336's panel, unfiltered
    last = min(u.index[-1], b.index[-1], s.index[-1])
    return {n: p.loc[:last].dropna(how="all").ffill()
            for n, p in (("U56", u), ("B136", b), ("SMALL484", s))}, last


# ================================================================ [0] reproduction gates
def gates(panels, last):
    log("=" * 170)
    log("[0] REPRODUCTION GATES (printed before any new number is read)")
    log(f"    panels truncated to the common last date {last.date()}")
    ok = []

    # G1: derived cost rungs
    px = panels["U56"]
    res0 = backtest(px, ewall_weights(px, G_HEAD), cost_bps=0, freq=FREQ)
    worst = 0.0
    for c in RUNGS[1:]:
        live = backtest(px, ewall_weights(px, G_HEAD), cost_bps=c, freq=FREQ)["returns"]
        der = res0["returns"] - res0["turnover"] * c / 1e4
        worst = max(worst, float((live - der).abs().max()))
    ok.append((worst < 1e-12, f"G1 derived cost rung == live engine cost, max|diff| {worst:.3e}"))

    # G4: idea 84's ungated EWALL U56 g=0.85 @10bps
    r84 = backtest(px, ewall_weights(px, 0.85), cost_bps=10, freq=FREQ)["returns"].iloc[260:]
    m84 = metrics(r84)
    got = (m84["CAGR"], m84["Sharpe"], m84["MaxDD"])
    tol = [0.004, 0.05, 0.010]
    ok.append((all(abs(g - e) <= t for g, e, t in zip(got, IDEA84_U56_EW085, tol)),
               f"G4 idea 84 EWALL U56 g0.85 @10bps = {got[0]:.2%} / {got[1]:.3f} / {got[2]:.2%} "
               f"(published {IDEA84_U56_EW085[0]:.1%} / {IDEA84_U56_EW085[1]:.2f} / {IDEA84_U56_EW085[2]:.1%})"))

    # G2 + G3: idea 336's EXP fidelity triple, and the firing-rate arithmetic two ways
    log("")
    log("    G2 idea 336's committed EXP (expanding, min_periods=252) LEVEL fidelity, re-computed:")
    g2rows = []
    g3worst = 0.0
    for name, p in panels.items():
        start = p.index[260]
        br_full = breadth(p)
        br = br_full.loc[start:]
        for i, q in enumerate(QS):
            thr = br_full.expanding(min_periods=MINQ).quantile(q)
            rate = float((br < thr.loc[start:]).mean())              # way 1
            rate2 = float(np.mean((br.values < thr.loc[start:].values)))  # way 2, independent
            g3worst = max(g3worst, abs(rate - rate2))
            pub = IDEA336_FIDELITY[name][i]
            g2rows.append(dict(panel=name, q=q, realised=rate, ratio=rate / q,
                               idea336_ratio=pub, diff=rate / q - pub))
    g2 = pd.DataFrame(g2rows)
    log(fmt(g2.set_index(["panel", "q"]), 4))
    ok.append((float(g2["diff"].abs().max()) <= 0.035,
               f"G2 max |ratio - idea336 published ratio| = {g2['diff'].abs().max():.4f} "
               f"(tolerance 0.035; idea 336 ran on the 2026-09-07 cache and published 3 d.p.)"))
    ok.append((g3worst == 0.0, f"G3 firing-rate arithmetic, two independent computations agree to {g3worst:.3e}"))

    log("")
    for good, msg in ok:
        log(f"    [{'PASS' if good else 'FAIL'}] {msg}")
    if not all(g for g, _ in ok):
        log("    !! a gate FAILED - every number below is reported anyway and flagged in the memo")
    return g2


# ================================================================ [1] Q1 rate fidelity
def q1_fidelity(panels):
    log("\n" + "=" * 170)
    log("[1] Q1 - RATE FIDELITY and CROSS-PANEL EQUALITY.  Pure measurement: no book is run here,")
    log("    nothing is tuned, and neither claim is used to select anything.")
    rows = []
    for name, p in panels.items():
        start = p.index[260]
        br_full = breadth(p)
        br = br_full.loc[start:]
        for q in QS:
            thr = br_full.expanding(min_periods=MINQ).quantile(q)
            t = thr.loc[start:]
            rows.append(dict(panel=name, family="EXP", w=np.nan, q=q,
                             armed=float(t.notna().mean()),
                             rate_all=float((br < t).mean()),
                             rate_armed=float((br[t.notna()] < t[t.notna()]).mean())))
            for w in WS:
                thr = br_full.rolling(w, min_periods=w).quantile(q)
                t = thr.loc[start:]
                rows.append(dict(panel=name, family="ROLL", w=w, q=q,
                                 armed=float(t.notna().mean()),
                                 rate_all=float((br < t).mean()),
                                 rate_armed=float((br[t.notna()] < t[t.notna()]).mean())))
    f = pd.DataFrame(rows)
    f["ratio_all"] = f["rate_all"] / f["q"]
    f["ratio_armed"] = f["rate_armed"] / f["q"]

    log("\n    (a) realised firing rate / nominal q.  'all' = over every eval day (idea 336's own")
    log("        convention, which counts the un-armed warm-up as non-firing); 'armed' = over the")
    log("        days the estimator actually exists.  The second is the fair read of the ESTIMATOR.")
    piv = f.pivot_table(index=["family", "w"], columns=["panel", "q"], values="ratio_armed", dropna=False)
    log(fmt(piv, 3))
    log("\n    the same table on idea 336's 'all-days' convention (this is what G2 reproduces):")
    log(fmt(f.pivot_table(index=["family", "w"], columns=["panel", "q"], values="ratio_all", dropna=False), 3))
    log("\n    share of eval days on which the estimator is ARMED at all:")
    log(fmt(f.pivot_table(index=["family", "w"], columns="panel", values="armed", dropna=False), 3))

    log("\n    (b) CROSS-PANEL SPREAD of the realised firing rate (max - min over the three panels).")
    log("        This is the property idea 336 bought the quantile form FOR; its published ABS")
    log(f"        spreads were {IDEA336_ABS_SPREAD} and its EXP spreads {IDEA336_QUANT_SPREAD}.")
    sp = (f.groupby(["family", "w", "q"], dropna=False)["rate_armed"]
            .agg(lambda s: s.max() - s.min()).rename("spread").reset_index())
    log(fmt(sp.pivot_table(index=["family", "w"], columns="q", values="spread", dropna=False), 4))

    # ---- cross-check against the cloud lane's independent same-day run of this idea
    xc = OUT / "2026-09-10_does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate_cloud.rates.csv"
    if xc.exists():
        cl = pd.read_csv(xc)
        cl = cl[cl["family"].str.endswith("_armed")].copy()
        cl["family"] = cl["family"].str.replace("_armed", "", regex=False).map({"QEXP": "EXP",
                                                                               "QROLL": "ROLL"})
        cl["w"] = cl["w"].replace(0, np.nan)
        j = f[["panel", "family", "w", "q", "rate_armed"]].merge(
            cl[["panel", "family", "w", "q", "realised"]], on=["panel", "family", "w", "q"])
        j["diff"] = j["rate_armed"] - j["realised"]
        log(f"\n    CROSS-CHECK vs the cloud lane's independent same-day run of idea 399 "
            f"({len(j)} shared cells).")
        log("    It used SMALL439 and w in {252, 504, 1008, 2016}, so only U56/B136 at w in")
        log("    {252, 504} plus the EXP comparand are shared.  Two independently written")
        log("    estimators, same realised firing rate on armed days:")
        log(fmt(j.set_index(["panel", "family", "w", "q"]), 6))
        log(f"    max |diff| = {float(j['diff'].abs().max()):.2e} over {len(j)} shared cells")
    else:
        log("\n    (cloud-lane rates.csv not present in this checkout; cross-check skipped)")

    log("\n    (c) the headline read, at the PRE-REGISTERED q = 0.12, armed days:")
    h = f[(f["q"] == Q_REG)].pivot_table(index=["family", "w"], columns="panel",
                                         values="ratio_armed", dropna=False)
    log(fmt(h, 3))
    return f


# ================================================================ [2]-[3] the grid
def run_panel(name, px, spy_stats_out):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ss = spy_summary(spy)
    spy_stats_out[name] = ss
    br_full = breadth(px)
    br = br_full.loc[start:]

    log("\n" + "=" * 170)
    log(f"PANEL {name}: {px.shape[1] - 1} names + SPY, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"eval from {start.date()} ({len(br)} days)")
    log(f"  SPY {ss['CAGR']:.2%} / {ss['Sharpe']:.3f} / {ss['MaxDD']:.2%} | 4b bars: CAGR floor "
        f"{0.70 * ss['CAGR']:.2%}, DD cap {-0.60 * abs(ss['MaxDD']):.2%}, halves "
        f"{ss['H1']:.3f}/{ss['H2']:.3f}, OOS {ss['OOS_Sharpe']:.3f}")
    log(f"  breadth_t: mean {br.mean():.3f}, median {br.median():.3f}, sd {br.std():.3f}")

    # thresholds, computed once
    thr = {}
    for q in QS:
        thr[("EXP", np.nan, q)] = br_full.expanding(min_periods=MINQ).quantile(q)
        for w in WS:
            thr[("ROLL", w, q)] = br_full.rolling(w, min_periods=w).quantile(q)

    # base books: one backtest per gross at 0 bps, all rungs derived (G1 asserts this)
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    v1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)

    def rung(pair, c):
        r, t = pair
        return r - t * c / 1e4

    refs = {c: {"RULES v2 (live)": rung((v2["returns"].loc[start:], v2["turnover"].loc[start:]), c),
                "RULES v1": rung((v1["returns"].loc[start:], v1["turnover"].loc[start:]), c),
                "SPY": spy} for c in RUNGS}

    # multipliers
    mults = {}
    for cad in CADENCES:
        for d in DEPTHS:
            for key, t in thr.items():
                mults[(key, d, cad)] = gate_mult(px, t, d, cad).loc[start:]

    rows, twins = [], {}
    for c in RUNGS:
        v2c = refs[c]["RULES v2 (live)"]
        for nm, r in refs[c].items():
            rows.append(dict(panel=name, rung=c, gross=np.nan, family="ref", arm=nm,
                             w=np.nan, q=np.nan, depth=np.nan, cadence="-",
                             **summarise(r, spy_stats_out[name], v2c)))
        for g in GROSSES:
            rb = rung(base0[g], c)
            rows.append(dict(panel=name, rung=c, gross=g, family="control", arm=f"NOGATE g{g:.2f}",
                             w=np.nan, q=np.nan, depth=0.0, cadence="-",
                             **summarise(rb, spy_stats_out[name], v2c)))
            for cad in CADENCES:
                for d in DEPTHS:
                    for (fam, w, q), t in thr.items():
                        m = mults[((fam, w, q), d, cad)]
                        rg, me = apply_gate(rb, m, g, c)
                        wl = "" if fam == "EXP" else f" w{w}"
                        rows.append(dict(panel=name, rung=c, gross=g, family=fam,
                                         arm=f"{fam}{wl} q{q:.2f} d{d:.2f} {cad} g{g:.2f}",
                                         w=w, q=q, depth=d, cadence=cad,
                                         **summarise(rg, spy_stats_out[name], v2c, mult=me)))
                        # matched-mean-gross static twins: same average exposure, zero timing.
                        # TWO constructions, because they are NOT the same object:
                        #   SCALE   - multiply the parent's return series by mean(mult).  This is
                        #             literally "hold mean(mult) of the book and the rest in cash".
                        #             Sharpe is scale-invariant, so this twin's Sharpe EQUALS the
                        #             parent's exactly; it can only separate on CAGR and MaxDD.
                        #   REGROSS - re-run engine.backtest with EW weights at gross g*mean(mult).
                        #             This is idea 336's own construction (and the cloud lane's
                        #             same-day run's).  It differs from SCALE through the engine's
                        #             drift/cash renormalisation and the cost term, so it is NOT
                        #             degenerate - but how far from degenerate is measured, not
                        #             assumed.
                        mm = float(me.mean())
                        rows.append(dict(panel=name, rung=c, gross=g, family=f"MGSCALE-{fam}",
                                         arm=f"MGSCALE {fam}{wl} q{q:.2f} d{d:.2f} {cad} g{g:.2f}",
                                         w=w, q=q, depth=d, cadence=cad,
                                         **summarise(rb * mm, spy_stats_out[name], v2c,
                                                     mult=pd.Series(mm, index=me.index))))
                        # g_eff rounded to 2dp so the twin books cache (the cloud lane's own
                        # convention); the 0-bps book is cached once and every rung derived
                        # from it by G1's identity, so no rung re-runs the engine.
                        key = round(g * mm, 2)
                        if key not in twins:
                            res = backtest(px, ewall_weights(px, key), cost_bps=0, freq=FREQ)
                            twins[key] = (res["returns"].loc[start:], res["turnover"].loc[start:])
                        rows.append(dict(panel=name, rung=c, gross=g, family=f"MGROSS-{fam}",
                                         arm=f"MGROSS {fam}{wl} q{q:.2f} d{d:.2f} {cad} g{g:.2f}",
                                         w=w, q=q, depth=d, cadence=cad,
                                         **summarise(rung(twins[key], c), spy_stats_out[name], v2c,
                                                     mult=pd.Series(mm, index=me.index))))
    return pd.DataFrame(rows)


# ================================================================ [4] rule 8
def walk_forward(grid, spy_stats):
    """(w, depth) chosen on 2009-2016 IS Sharpe ONLY, at g=0.75 and each q separately; the
    EXP family's (q, depth) chooser is idea 336's own, run here under the identical rule."""
    log("\n" + "=" * 170)
    log("[4] RULE 8 WALK-FORWARD - parameters chosen on IS Sharpe (<= 2016-12-31) alone, at")
    log("    g = 0.75; 2017-2026 read ONCE.  The chooser NEVER sees an OOS number and never")
    log("    crosses q: inside each q it picks (w, depth) for ROLL, and idea 336's EXP chooser")
    log("    picks (q, depth) over its own 9-point grid exactly as idea 336 ran it.")
    out = []
    for panel, ss in spy_stats.items():
        gp = grid[(grid["panel"] == panel) & (grid["gross"] == G_HEAD)]
        for c in RUNGS:
            for cad in CADENCES:
                nog = gp[(gp["family"] == "control") & (gp["rung"] == c)]
                nog_oos = float(nog["OOS_Sharpe"].iloc[0]); nog_cagr = float(nog["OOS_CAGR"].iloc[0])
                nog_dd = float(nog["OOS_MaxDD"].iloc[0])
                # ROLL, per q
                for q in QS:
                    cand = gp[(gp["family"] == "ROLL") & (gp["rung"] == c) &
                              (gp["cadence"] == cad) & (gp["q"] == q)]
                    pick = cand.loc[cand["IS_Sharpe"].idxmax()]
                    out.append(dict(panel=panel, rung=c, cadence=cad, family="ROLL", q=q,
                                    pick=f"w{int(pick['w'])} d{pick['depth']:.2f}",
                                    IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                                    OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                                    on_share=pick["on_share"],
                                    grid_mean_OOS=cand["OOS_Sharpe"].mean(),
                                    best_OOS=cand["OOS_Sharpe"].max(),
                                    regret=cand["OOS_Sharpe"].max() - pick["OOS_Sharpe"],
                                    vs_nogate=pick["OOS_Sharpe"] - nog_oos,
                                    nogate_OOS=nog_oos, nogate_OOS_CAGR=nog_cagr,
                                    nogate_OOS_MaxDD=nog_dd, spy_OOS=ss["OOS_Sharpe"],
                                    p4a=bool(pick["p4a"]), p4b=bool(pick["p4b"])))
                # EXP: idea 336's own (q, depth) chooser
                cand = gp[(gp["family"] == "EXP") & (gp["rung"] == c) & (gp["cadence"] == cad)]
                pick = cand.loc[cand["IS_Sharpe"].idxmax()]
                out.append(dict(panel=panel, rung=c, cadence=cad, family="EXP", q=np.nan,
                                pick=f"q{pick['q']:.2f} d{pick['depth']:.2f}",
                                IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                                OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                                on_share=pick["on_share"],
                                grid_mean_OOS=cand["OOS_Sharpe"].mean(),
                                best_OOS=cand["OOS_Sharpe"].max(),
                                regret=cand["OOS_Sharpe"].max() - pick["OOS_Sharpe"],
                                vs_nogate=pick["OOS_Sharpe"] - nog_oos,
                                nogate_OOS=nog_oos, nogate_OOS_CAGR=nog_cagr,
                                nogate_OOS_MaxDD=nog_dd, spy_OOS=ss["OOS_Sharpe"],
                                p4a=bool(pick["p4a"]), p4b=bool(pick["p4b"])))
    return pd.DataFrame(out)


# ================================================================ main
def main():
    panels, last = load_panels()
    g2 = gates(panels, last)
    fid = q1_fidelity(panels)

    spy_stats = {}
    grid = pd.concat([run_panel(n, p, spy_stats) for n, p in panels.items()], ignore_index=True)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    fid.to_csv(OUT / f"{STEM}.fidelity.csv", index=False)

    head = grid[(grid["rung"] == RUNG_HEAD) & (grid["gross"] == G_HEAD)]

    log("\n" + "=" * 170)
    log(f"[2] Q2 - DOES THE GATE EARN ANYTHING?  Headline rung {RUNG_HEAD} bps, g = {G_HEAD:.2f}, "
        f"pre-registered q = {Q_REG}.")
    log("    Two bars, both structural: NOGATE (do nothing) and the MATCHED-MEAN-GROSS twin")
    log("    (identical average exposure, zero timing).  A gate that beats neither is not an")
    log("    instrument, however faithfully it fires.")
    for panel in panels:
        hp = head[head["panel"] == panel]
        nog = hp[hp["family"] == "control"].iloc[0]
        log(f"\n  --- {panel}: NOGATE g{G_HEAD} = {nog['CAGR']:.2%} / {nog['Sharpe']:.3f} / "
            f"{nog['MaxDD']:.2%} | H {nog['H1']:.3f}/{nog['H2']:.3f} | OOS {nog['OOS_CAGR']:.2%} / "
            f"{nog['OOS_Sharpe']:.3f} / {nog['OOS_MaxDD']:.2%}")
        sub = hp[(hp["family"].isin(["ROLL", "EXP"])) & (hp["q"] == Q_REG)].copy()
        sub["d_vs_nogate"] = sub["Sharpe"] - nog["Sharpe"]
        sub["dOOS_vs_nogate"] = sub["OOS_Sharpe"] - nog["OOS_Sharpe"]
        mg = hp[(hp["family"].str.startswith("MGROSS")) & (hp["q"] == Q_REG)].set_index("arm")
        sub["d_vs_mgross"] = [s - mg.loc["MGROSS " + a, "Sharpe"] for a, s in
                              zip(sub["arm"], sub["Sharpe"])]
        sub["dOOS_vs_mgross"] = [s - mg.loc["MGROSS " + a, "OOS_Sharpe"] for a, s in
                                 zip(sub["arm"], sub["OOS_Sharpe"])]
        cols = ["family", "w", "depth", "cadence", "on_share", "mean_mult", "CAGR", "Sharpe",
                "MaxDD", "H1", "H2", "OOS_Sharpe", "d_vs_nogate", "dOOS_vs_nogate",
                "d_vs_mgross", "dOOS_vs_mgross", "p4a", "p4b", "fail4b"]
        log(fmt(sub[cols].sort_values(["cadence", "family", "w", "depth"]).set_index("family"), 3))

    log("\n  ROLL vs its own bars, MEANS over all 12 (w, depth) points, both cadences, at each")
    log("  q / rung / gross - the whole grid summarised, every point already in grid.csv:")
    roll = grid[grid["family"] == "ROLL"].copy()
    mgi = grid[grid["family"] == "MGROSS-ROLL"].set_index(["panel", "rung", "arm"])
    nogi = grid[grid["family"] == "control"].set_index(["panel", "rung", "gross"])
    roll["dOOS_nogate"] = [r["OOS_Sharpe"] - nogi.loc[(r["panel"], r["rung"], r["gross"]), "OOS_Sharpe"]
                           for _, r in roll.iterrows()]
    roll["dS_nogate"] = [r["Sharpe"] - nogi.loc[(r["panel"], r["rung"], r["gross"]), "Sharpe"]
                         for _, r in roll.iterrows()]
    roll["dS_mgross"] = [r["Sharpe"] - mgi.loc[(r["panel"], r["rung"], "MGROSS " + r["arm"]), "Sharpe"]
                         for _, r in roll.iterrows()]
    roll["dOOS_mgross"] = [r["OOS_Sharpe"] - mgi.loc[(r["panel"], r["rung"], "MGROSS " + r["arm"]), "OOS_Sharpe"]
                           for _, r in roll.iterrows()]
    log(fmt(roll.groupby(["panel", "rung", "q"])[["dS_nogate", "dOOS_nogate", "dS_mgross",
                                                  "dOOS_mgross", "on_share"]].mean(), 4))

    exp = grid[grid["family"] == "EXP"].copy()
    mge = grid[grid["family"] == "MGROSS-EXP"].set_index(["panel", "rung", "arm"])
    exp["dS_nogate"] = [r["Sharpe"] - nogi.loc[(r["panel"], r["rung"], r["gross"]), "Sharpe"]
                        for _, r in exp.iterrows()]
    exp["dOOS_nogate"] = [r["OOS_Sharpe"] - nogi.loc[(r["panel"], r["rung"], r["gross"]), "OOS_Sharpe"]
                          for _, r in exp.iterrows()]
    exp["dS_mgross"] = [r["Sharpe"] - mge.loc[(r["panel"], r["rung"], "MGROSS " + r["arm"]), "Sharpe"]
                        for _, r in exp.iterrows()]
    exp["dOOS_mgross"] = [r["OOS_Sharpe"] - mge.loc[(r["panel"], r["rung"], "MGROSS " + r["arm"]), "OOS_Sharpe"]
                          for _, r in exp.iterrows()]
    log("\n  the SAME table for idea 336's EXP family (its Q3 numbers, re-run here):")
    log(fmt(exp.groupby(["panel", "rung", "q"])[["dS_nogate", "dOOS_nogate", "dS_mgross",
                                                 "dOOS_mgross", "on_share"]].mean(), 4))

    log("\n" + "=" * 170)
    log("[3] KEEP PATHS over the WHOLE tuned grid (PROTOCOL rule 4; every point reported in")
    log("    grid.csv).  Counts are over gated arms only; controls and refs excluded.")
    gated = grid[grid["family"].isin(["ROLL", "EXP"])]
    cnt = gated.groupby(["family", "rung"]).agg(points=("p4a", "size"), pass4a=("p4a", "sum"),
                                                pass4b=("p4b", "sum"))
    log(fmt(cnt, 0))
    log("\n    by panel, at the headline rung:")
    log(fmt(gated[gated["rung"] == RUNG_HEAD].groupby(["panel", "family"])
            .agg(points=("p4a", "size"), pass4a=("p4a", "sum"), pass4b=("p4b", "sum")), 0))
    log("\n    INHERITANCE check - does the UNGATED parent pass 4b on its own?")
    log(fmt(grid[grid["family"] == "control"].groupby(["panel", "rung", "gross"])[["p4a", "p4b"]].sum(), 0))
    par = grid[grid["family"] == "control"].set_index(["panel", "rung", "gross"])["p4b"]
    gg = gated.copy()
    gg["parent4b"] = [bool(par.loc[(r["panel"], r["rung"], r["gross"])]) for _, r in gg.iterrows()]
    gg["inherited"] = gg["p4b"] & gg["parent4b"]
    gg["earned"] = gg["p4b"] & ~gg["parent4b"]
    log("\n    of the 4b passes, how many are INHERITED (the ungated parent passes too) vs EARNED")
    log("    by the gate?  A gate whose passes are all inherited has bought nothing.")
    log(fmt(gg.groupby(["family", "rung"]).agg(pass4b=("p4b", "sum"), inherited=("inherited", "sum"),
                                               earned=("earned", "sum")), 0))
    log("\n    EARNED 4b passes by panel at the headline rung:")
    log(fmt(gg[gg["rung"] == RUNG_HEAD].groupby(["panel", "family"])
            .agg(pass4b=("p4b", "sum"), inherited=("inherited", "sum"), earned=("earned", "sum")), 0))

    log("\n    THE TWO MATCHED-MEAN-GROSS TWINS.  De-grossing to CASH by SCALING the parent's")
    log("    return series multiplies it by a constant, and Sharpe is scale-invariant, so the")
    log("    SCALE twin's Sharpe EQUALS the parent's exactly - it cannot be a second bar on the")
    log("    Sharpe leg at all.  Idea 336's own twin (and the cloud lane's same-day run of this")
    log("    idea) is the REGROSS construction: engine.backtest re-run with EW weights at gross")
    log("    g*mean(mult), which differs from SCALE only through the engine's drift/cash")
    log("    renormalisation and the cost term.  Both are run here so the size of that difference")
    log("    is measured rather than assumed.")
    mgs = grid[grid["family"].str.startswith("MGSCALE")].set_index(["panel", "rung", "arm"])
    mgr = grid[grid["family"].str.startswith("MGROSS")].set_index(["panel", "rung", "arm"])
    gsc = gated.copy()
    for tag, tbl in (("scale", mgs), ("regross", mgr)):
        pre = "MGSCALE " if tag == "scale" else "MGROSS "
        for col in ("Sharpe", "OOS_Sharpe", "CAGR", "MaxDD"):
            gsc[f"d{col}_{tag}"] = [r[col] - tbl.loc[(r["panel"], r["rung"], pre + r["arm"]), col]
                                    for _, r in gsc.iterrows()]
    log("\n    (i) how far apart are the two twin CONSTRUCTIONS themselves?")
    both = mgs.reset_index()[["panel", "rung", "arm", "Sharpe", "OOS_Sharpe", "MaxDD"]].copy()
    both["arm"] = both["arm"].str.replace("MGSCALE ", "MGROSS ", regex=False)
    both = both.merge(mgr.reset_index()[["panel", "rung", "arm", "Sharpe", "OOS_Sharpe", "MaxDD"]],
                      on=["panel", "rung", "arm"], suffixes=("_scale", "_regross"))
    log(f"        max |SCALE - REGROSS|: Sharpe "
        f"{float((both['Sharpe_scale'] - both['Sharpe_regross']).abs().max()):.4f}, OOS "
        f"{float((both['OOS_Sharpe_scale'] - both['OOS_Sharpe_regross']).abs().max()):.4f}, MaxDD "
        f"{float((both['MaxDD_scale'] - both['MaxDD_regross']).abs().max()):.4f}, over {len(both)} "
        f"matched twin pairs")
    log("\n    (ii) the gate against EACH twin, headline rung.  'beats' counts SIGNS, which is how")
    log("         the record reports this bar; the medians beside them are the MAGNITUDES.")
    h = gsc[gsc["rung"] == RUNG_HEAD]
    log(fmt(h.groupby(["panel", "family"]).agg(
        n=("dSharpe_scale", "size"),
        beats_SCALE=("dSharpe_scale", lambda x: int((x > 0).sum())),
        med_dS_SCALE=("dSharpe_scale", "median"),
        beats_REGROSS=("dSharpe_regross", lambda x: int((x > 0).sum())),
        med_dS_REGROSS=("dSharpe_regross", "median"),
        med_dMaxDD_REGROSS=("dMaxDD_regross", "median"),
        beats_REGROSS_DD=("dMaxDD_regross", lambda x: int((x > 0).sum()))), 4))
    log("\n    (iii) the same, split by cost rung, ROLL only - the sign count is what moves:")
    log(fmt(gsc[gsc["family"] == "ROLL"].groupby(["panel", "rung"]).agg(
        n=("dSharpe_regross", "size"),
        beats_REGROSS=("dSharpe_regross", lambda x: int((x > 0).sum())),
        med_dS_REGROSS=("dSharpe_regross", "median"),
        beats_SCALE=("dSharpe_scale", lambda x: int((x > 0).sum())),
        med_dS_SCALE=("dSharpe_scale", "median")), 4))
    log("\n    4b failure reasons across gated arms (headline rung):")
    log(gated[gated["rung"] == RUNG_HEAD]["fail4b"].value_counts().to_string())

    wf = walk_forward(grid, spy_stats)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log("")
    log(f"    HEADLINE rung {RUNG_HEAD} bps, the 12 cells the PROTOCOL rung actually names:")
    log(fmt(wf[wf["rung"] == RUNG_HEAD].set_index(["panel", "cadence", "family", "q"]), 3))
    log("\n    ALL 72 cells (3 rungs x 2 cadences x 3 panels x 4 families):")
    log(fmt(wf.set_index(["panel", "rung", "cadence", "family", "q"]), 3))
    log("\n    SUMMARY of the chooser, by family (all 3 rungs x 2 cadences x 3 panels):")
    s = wf.groupby(["family", "q"], dropna=False).agg(
        cells=("vs_nogate", "size"), beats_nogate=("vs_nogate", lambda x: int((x > 0).sum())),
        mean_vs_nogate=("vs_nogate", "mean"), median_vs_nogate=("vs_nogate", "median"),
        mean_regret=("regret", "mean"), mean_on_share=("on_share", "mean"),
        beats_SPY=("OOS_Sharpe", lambda x: np.nan))
    s["beats_SPY"] = [int((wf[(wf["family"] == f) & ((wf["q"] == q) if not pd.isna(q) else wf["q"].isna())]["OOS_Sharpe"] >
                           wf[(wf["family"] == f) & ((wf["q"] == q) if not pd.isna(q) else wf["q"].isna())]["spy_OOS"]).sum())
                      for f, q in s.index]
    log(fmt(s, 4))
    log("\n    the queue's specific charge - does the chooser still pick an INERT arm?")
    log("    (idea 336: 'picks the INERT q=0.07 arm in 5 of 6 cells').  on_share of the PICK:")
    log(fmt(wf.groupby(["family", "q"], dropna=False)["on_share"]
            .agg(["min", "median", "max", lambda x: int((x < 0.01).sum())])
            .rename(columns={"<lambda_0>": "n_inert(<1%)"}), 4))

    log("\n" + "=" * 170)
    log("[5] VERDICT")
    roll12 = fid[(fid["family"] == "ROLL")]
    exp12 = fid[(fid["family"] == "EXP")]
    log(f"    Q1 rate fidelity (armed days, ratio realised/nominal): EXP median "
        f"{exp12['ratio_armed'].median():.3f} (min {exp12['ratio_armed'].min():.3f}, "
        f"max {exp12['ratio_armed'].max():.3f}) -> ROLL median {roll12['ratio_armed'].median():.3f} "
        f"(min {roll12['ratio_armed'].min():.3f}, max {roll12['ratio_armed'].max():.3f})")
    hr = roll.groupby("panel")[["dS_nogate", "dOOS_nogate", "dS_mgross", "dOOS_mgross"]].mean()
    log(f"    Q2 ROLL vs do-nothing / vs matched-gross, mean over the whole grid, by panel:")
    log(fmt(hr, 4))
    log(f"    Q3 chooser beats do-nothing in {int((wf['vs_nogate'] > 0).sum())} of {len(wf)} cells; "
        f"ROLL alone {int((wf[wf['family'] == 'ROLL']['vs_nogate'] > 0).sum())} of "
        f"{len(wf[wf['family'] == 'ROLL'])}, EXP alone "
        f"{int((wf[wf['family'] == 'EXP']['vs_nogate'] > 0).sum())} of {len(wf[wf['family'] == 'EXP'])}")
    log(f"    KEEP: 4a {int(gated['p4a'].sum())} of {len(gated)} gated points; "
        f"4b {int(gated['p4b'].sum())} of {len(gated)}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
