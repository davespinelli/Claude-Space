#!/usr/bin/env python3
"""Idea 42 - "breadth-gate-on-v2": does idea 40's 200d-BREADTH GATE close idea 28's 4b
near-miss on the equal-weight-all-eligible book?

The question, and the pre-registered prediction that governs it
---------------------------------------------------------------
The queue pairs two near-misses that fail on OPPOSITE bars:

  * idea 40's top-n book (breadth gate, n=3, B=30%) misses 4b's DRAWDOWN cap by 0.4pp.
  * idea 28's EWALL book (equal-weight every eligible name, weekly) misses 4b's CAGR
    FLOOR by 0.23pp "with drawdown to spare".

The queue's hope is that the instrument that fixes the first miss can be carried to the
second book.  It cannot, if the arithmetic is what it looks like: the breadth gate is a
DE-GROSSING instrument - its only action is to cut exposure - and the bar EWALL fails is
the CAGR floor.  Cutting exposure lowers CAGR.  So the pre-registered prediction, written
before any number below was read, is:

    P1  For every (B, depth) with depth > 0, gated CAGR < ungated CAGR on every panel and
        every gross.  The gate cannot close a CAGR-floor miss; it can only widen it.
    P2  Therefore any new 4b pass the gate produces must come from a book that was failing
        a RISK bar (H1/H2/OOS Sharpe or MaxDD), not the CAGR bar - i.e. from a different
        near-miss than the one the queue named.
    P3  The honest comparand for a de-grossing overlay is a STATIC gross at the same mean
        exposure (the record's ladder control, ideas 66/154).  If the gate does not beat
        its own matched-gross twin, it is a gross dial wearing a timing costume.

This script is written to be able to FALSIFY P1-P3, not to confirm them: the whole grid is
reported, both cadences, three cost rungs, three panels, and the direction of the queue's
own remedy (raise gross) is run alongside as the opposite lever.

The rule family
---------------
Base book, FIXED, not tuned - idea 28's v2 candidate:
    EWALL(G):  eligible_t = {above own 200d MA} AND {vol20 < 0.60}   (RULES v1's own filter)
               hold every eligible name at G / E_t, cash otherwise; weekly; next-day.

Overlay - idea 40's instrument, verbatim in mechanism:
    breadth_t = share of panel names trading above their own 200d MA (whole panel, not the
                eligible subset - idea 40's definition).
    GATE(B, depth):  mult_t = 1 - depth   if breadth_t <  B
                     mult_t = 1           otherwise
    The book is carried at mult_t of its target exposure, the remainder in cash at 0%.
    Decision uses data through t; the multiplier changes at t+1 and pays cost_bps on
    |d mult| * G of traded notional on the day it takes effect.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. B      breadth threshold  in {0.30, 0.40, 0.50}     (idea 40's own three values)
    2. depth  cut depth          in {0.25, 0.50, 1.00}     (1.00 = gate to cash)
9 gate points, ALL reported.  Nothing else is searched.  In particular:
    * GROSS in {0.75, 0.85, 1.00} is idea 28's REQUIRED reporting axis, not a tuned
      parameter: every gross is reported at every grid point and the walk-forward chooser
      is restricted to G = 0.75 (the live gross) so it never picks on it.
    * CADENCE in {D, W} is a mechanism check, both always reported, never selected on.
    * COST in {0, 10, 25} bps: 10 is PROTOCOL's rung; 0 and 25 are reported so a pass can
      be classified as real or as a 10-bps artefact (the record's standing failure mode).
    * PANEL in {U56, B136, SMALL484}: portability, all reported, never selected on.

Controls (structural, none selected on its own result)
    NOGATE          the ungated EWALL book at the same gross - the direct parent.
    MATCHED-GROSS   static gross G * mean(mult) with no gate at all - P3's comparand.
    RULES v2 / RULES v1 / SPY  - PROTOCOL rule 3's references.

Walk-forward (PROTOCOL rule 8)
    (B, depth) chosen on 2009-2016 IS Sharpe alone, at G = 0.75, per panel and cadence;
    2017-2026 read once.  Reported against: the ungated parent OOS (the do-nothing
    control), the grid mean OOS (the anchor), the best OOS point (regret), and SPY OOS.

Verdicts, evaluated at EVERY grid point
    4a: Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2's.
    4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Data: committed caches only (no network).  Survivorship: all three panels are
current-constituent lists, so absolute CAGRs are optimistic; the gated-vs-ungated and
gated-vs-matched-gross contrasts are the durable parts.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
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
MAX_VOL = 0.60                       # RULES v1 eligibility, unchanged
GROSSES = [0.75, 0.85, 1.00]         # idea 28's required reporting axis (NOT tuned)
G_HEAD = 0.75                        # live gross; the only gross the chooser may use
BS = [0.30, 0.40, 0.50]              # tuned param 1 (idea 40's own values)
DEPTHS = [0.25, 0.50, 1.00]          # tuned param 2
RUNGS = [0, 10, 25]
RUNG_HEAD = 10                       # PROTOCOL rule 2
BE_RUNGS = sorted(set(range(10, 41, 2)) | {25})   # cost breakeven scan, 10 -> 40 bps (25 included)
CADENCES = ["D", "W"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)


# ---------------------------------------------------------------- primitives
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def breadth(px):
    """Idea 40's definition: share of the WHOLE panel trading above its own 200d MA."""
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def ewall_weights(px, gross):
    """Idea 28's book: equal weight EVERY eligible name at gross/E_t; cash when E_t == 0."""
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def static_gross_weights(px, gross):
    return ewall_weights(px, gross)


def gate_mult(px, B, depth, cadence):
    """mult_t decided from data through t.  cadence 'D' lets it change any day (idea 40's
    mechanism); 'W' lets it change only on the book's own weekly rebalance days."""
    br = breadth(px)
    m = pd.Series(1.0, index=px.index).where(~(br < B), 1.0 - depth)
    m = m.where(br.notna(), 1.0)                      # pre-warm-up: no gate
    if cadence == "W":
        mask = rebalance_mask(px.index, FREQ)
        m = m.where(mask).ffill().fillna(1.0)
    return m


def apply_gate(r_base, mult, gross, cost_bps):
    """Carry the book at mult of its exposure; the switch executes the NEXT day and pays
    cost_bps on |d mult| * gross of notional on the day it takes effect."""
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)      # decided t, effective t+1
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


def summarise(r, spy, base_v2, mult=None, turn=None):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy)
    ms = metrics(spy)
    d = dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=m_is["Sharpe"], OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
             OOS_MaxDD=m_oos["MaxDD"],
             CAGR_margin=m["CAGR"] - 0.70 * ms["CAGR"],      # + = clears the floor
             DD_margin=0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),   # + = clears the cap
             p4a=verdict_4a(r, base_v2), p4b=all(t.values()), fail4b=fail_4b(r, spy))
    d["on_share"] = float((mult < 1.0).mean()) if mult is not None else np.nan
    d["mean_mult"] = float(mult.mean()) if mult is not None else 1.0
    d["turn"] = turn if turn is not None else np.nan
    return d


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- panel run
def run_panel(panel, px, log):
    out = []
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    br = breadth(px).loc[start:]

    log(f"\n{'='*170}\nPANEL {panel}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"eval from {start.date()}")
    log(f"  SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%} | 4b bars: CAGR floor "
        f"{0.70*ms['CAGR']:.2%}, DD cap {-0.60*abs(ms['MaxDD']):.2%}, halves "
        f"{half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}, OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.3f}")
    log(f"  breadth_t: mean {br.mean():.3f}, median {br.median():.3f}, "
        f"share below 0.30/0.40/0.50 = {(br<0.30).mean():.3f}/{(br<0.40).mean():.3f}/{(br<0.50).mean():.3f}")

    # references + base books, per cost rung
    base_r, refs = {}, {}
    for rung in RUNGS:
        v2 = backtest(px, rules_v2_weights(px), cost_bps=rung, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=rung, freq=FREQ)["returns"].loc[start:]
        refs[rung] = {"RULES v2 (live)": v2, "RULES v1": v1, "SPY": spy}
        for g in GROSSES:
            res = backtest(px, ewall_weights(px, g), cost_bps=rung, freq=FREQ)
            base_r[(rung, g)] = (res["returns"].loc[start:],
                                 res["turnover"].loc[start:].sum() / metrics(res["returns"].loc[start:])["Years"])

    for rung in RUNGS:
        v2 = refs[rung]["RULES v2 (live)"]
        for nm, r in refs[rung].items():
            out.append(dict(panel=panel, rung=rung, gross=np.nan, arm=nm, family="ref",
                            B=np.nan, depth=np.nan, cadence="-", **summarise(r, spy, v2)))
        for g in GROSSES:
            rb, tb = base_r[(rung, g)]
            out.append(dict(panel=panel, rung=rung, gross=g, arm=f"NOGATE g{g:.2f}",
                            family="control", B=np.nan, depth=0.0, cadence="-",
                            **summarise(rb, spy, v2, turn=tb)))
            for cad in CADENCES:
                for B in BS:
                    for depth in DEPTHS:
                        mult = gate_mult(px, B, depth, cad).loc[start:]
                        rg, m_eff = apply_gate(rb, mult, g, rung)
                        out.append(dict(panel=panel, rung=rung, gross=g,
                                        arm=f"GATE B{B:.2f} d{depth:.2f} {cad} g{g:.2f}",
                                        family="gate", B=B, depth=depth, cadence=cad,
                                        **summarise(rg, spy, v2, mult=m_eff, turn=tb)))

    # ---- P3: matched-gross control (headline rung, headline gross, both cadences)
    matched = []
    rb, tb = base_r[(RUNG_HEAD, G_HEAD)]
    v2 = refs[RUNG_HEAD]["RULES v2 (live)"]
    for cad in CADENCES:
        for B in BS:
            for depth in DEPTHS:
                mult = gate_mult(px, B, depth, cad).loc[start:]
                rg, m_eff = apply_gate(rb, mult, G_HEAD, RUNG_HEAD)
                g_eff = G_HEAD * float(m_eff.mean())
                res = backtest(px, static_gross_weights(px, g_eff), cost_bps=RUNG_HEAD, freq=FREQ)
                rs = res["returns"].loc[start:]
                mg, mst = metrics(rg), metrics(rs)
                matched.append(dict(panel=panel, cadence=cad, B=B, depth=depth, g_eff=g_eff,
                                    gate_CAGR=mg["CAGR"], static_CAGR=mst["CAGR"],
                                    gate_Sharpe=mg["Sharpe"], static_Sharpe=mst["Sharpe"],
                                    dSharpe=mg["Sharpe"] - mst["Sharpe"],
                                    gate_MaxDD=mg["MaxDD"], static_MaxDD=mst["MaxDD"],
                                    dMaxDD=abs(mst["MaxDD"]) - abs(mg["MaxDD"]),
                                    gate_4b=all(tests_4b(rg, spy).values()),
                                    static_4b=all(tests_4b(rs, spy).values())))

    # ---- cost breakeven c*: highest rung at which 4b still passes, for a pre-registered
    #      set of arms (the ungated parent at each gross, and depth=0.50 at each B, cadence D)
    be = []
    arms = [("NOGATE", None, None)] + [(f"GATE B{B:.2f} d0.50 D", B, 0.50) for B in BS]
    for g in GROSSES:
        cache = {}
        for c in BE_RUNGS:
            cache[c] = backtest(px, ewall_weights(px, g), cost_bps=c, freq=FREQ)["returns"].loc[start:]
        for nm, B, depth in arms:
            mult = None if B is None else gate_mult(px, B, depth, "D").loc[start:]

            def at(c):
                r = cache[c]
                return r if mult is None else apply_gate(r, mult, g, c)[0]

            passes = [(c, all(tests_4b(at(c), spy).values())) for c in BE_RUNGS]
            ok = [c for c, p in passes if p]
            cstar = max(ok) if ok else np.nan          # highest rung still inside 4b
            broke = next((c for c, p in passes if not p), np.nan)   # first rung outside 4b
            m10 = metrics(at(RUNG_HEAD))
            be.append(dict(panel=panel, gross=g, arm=nm, c_star=cstar, first_fail=broke,
                           fail_at_25=fail_4b(at(25), spy), Sharpe10=m10["Sharpe"],
                           CAGR10=m10["CAGR"], MaxDD10=m10["MaxDD"]))

    # ---- rule 8 walk-forward: choose (B, depth) on IS Sharpe at G_HEAD, per cadence/rung
    wf = []
    for rung in RUNGS:
        rb, tb = base_r[(rung, G_HEAD)]
        for cad in CADENCES:
            cells = {}
            for B in BS:
                for depth in DEPTHS:
                    mult = gate_mult(px, B, depth, cad).loc[start:]
                    rg, m_eff = apply_gate(rb, mult, G_HEAD, rung)
                    cells[(B, depth)] = rg
            is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cells.items()}
            oos = {k: metrics(v.loc[OOS_START:]) for k, v in cells.items()}
            pick = min(is_s, key=lambda k: (-is_s[k], k[0], k[1]))     # ties -> smaller B, depth
            best = max(oos, key=lambda k: oos[k]["Sharpe"])
            anchor = float(np.mean([oos[k]["Sharpe"] for k in oos]))
            po = oos[pick]
            wf.append(dict(panel=panel, rung=rung, cadence=cad, pick_B=pick[0], pick_depth=pick[1],
                           IS_Sharpe=is_s[pick], OOS_CAGR=po["CAGR"], OOS_Sharpe=po["Sharpe"],
                           OOS_MaxDD=po["MaxDD"],
                           nogate_OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                           nogate_OOS_CAGR=metrics(rb.loc[OOS_START:])["CAGR"],
                           grid_mean_OOS=anchor, best_OOS=oos[best]["Sharpe"],
                           regret=po["Sharpe"] - oos[best]["Sharpe"],
                           vs_nogate=po["Sharpe"] - metrics(rb.loc[OOS_START:])["Sharpe"],
                           spy_OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                           v2_OOS=metrics(refs[rung]["RULES v2 (live)"].loc[OOS_START:])["Sharpe"]))

    return pd.DataFrame(out), pd.DataFrame(matched), pd.DataFrame(wf), pd.DataFrame(be)


# ---------------------------------------------------------------- main
def main():
    lines = []

    def log(s=""):
        print(s)
        lines.append(str(s))

    log("=" * 170)
    log(f"Idea 42 breadth-gate-on-v2 (lane B) | {SCRIPT}")
    log("=" * 170)
    log("Book: EWALL(G) = equal weight EVERY name above its 200d MA with vol20<0.60, G/E_t, weekly, next-day.")
    log("Overlay: idea 40's gate - carry the book at (1-depth) whenever panel breadth < B, cash for the rest.")
    log(f"Tuned (2): B in {BS} x depth in {DEPTHS} = 9 points, ALL reported.")
    log(f"Reported, never tuned: gross {GROSSES} (idea 28's axis), cadence {CADENCES}, cost {RUNGS} bps, 3 panels.")
    log("Pre-registered predictions P1 (gate cannot raise CAGR), P2 (any pass must come from a risk bar),")
    log("P3 (gate must beat its own matched-gross static twin).  All three are falsifiable below.")

    panels = [("U56", dict()), ("B136", dict(broad=True)), ("SMALL484", dict(small=True))]
    grids, matches, wfs, bes = [], [], [], []
    for name, kw in panels:
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            log(f"!! {name}: CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        g, m, w, b = run_panel(name, px, log)
        grids.append(g); matches.append(m); wfs.append(w); bes.append(b)

    grid = pd.concat(grids, ignore_index=True)
    matched = pd.concat(matches, ignore_index=True)
    wf = pd.concat(wfs, ignore_index=True)
    bes = pd.concat(bes, ignore_index=True)
    grid.to_csv(OUT / f"{SCRIPT[:-3]}.grid.csv", index=False)
    matched.to_csv(OUT / f"{SCRIPT[:-3]}.matched.csv", index=False)
    wf.to_csv(OUT / f"{SCRIPT[:-3]}.walkforward.csv", index=False)
    bes.to_csv(OUT / f"{SCRIPT[:-3]}.breakeven.csv", index=False)

    # ---------------- reproduction gate against the published record
    log("\n" + "=" * 170)
    log("REPRODUCTION GATE - idea 84 (2026-09-04, `which-4b-bar-binds_B`) published the ungated")
    log("EWALL book on U56 at g=0.85, 10 bps as 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.")
    rep = grid[(grid.panel == "U56") & (grid.rung == RUNG_HEAD) & (grid.arm == "NOGATE g0.85")].iloc[0]
    log(f"  this run: {rep.CAGR:.1%} / {rep.Sharpe:.2f} / {rep.MaxDD:.1%} / H {rep.H1:.2f} / {rep.H2:.2f}"
        f"  -> {'MATCH' if (abs(rep.CAGR-0.118)<5e-4 and abs(rep.Sharpe-1.05)<5e-3 and abs(rep.MaxDD+0.179)<5e-4) else 'MISMATCH'}"
        " at published precision")

    show = ["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "CAGR_margin", "DD_margin", "on_share", "mean_mult", "p4a", "p4b", "fail4b"]

    # ---------------- headline grid
    log("\n" + "=" * 170)
    log(f"HEADLINE GRID - {RUNG_HEAD} bps, all three gross levels, both cadences, all 9 gate points + controls + refs.")
    log("CAGR_margin/DD_margin are signed distances to the 4b bars (+ = clears).  on_share = share of days gated.")
    for panel, _ in panels:
        sub = grid[(grid.panel == panel) & (grid.rung == RUNG_HEAD)]
        log(f"\n--- {panel} @ {RUNG_HEAD} bps")
        log(fmt(sub[show].set_index("arm").rename_axis(f"{panel} @{RUNG_HEAD}bps")))

    # ---------------- P1: does the gate ever raise CAGR?
    log("\n" + "=" * 170)
    log("P1 - CAN THE GATE RAISE CAGR?  Every gate point vs its own ungated parent (same panel/gross/rung/cadence).")
    gd = grid[grid.family == "gate"].copy()
    nog = grid[grid.family == "control"].set_index(["panel", "rung", "gross"])
    gd["parent_CAGR"] = [nog.loc[(p, r, g), "CAGR"] for p, r, g in zip(gd.panel, gd.rung, gd.gross)]
    gd["parent_Sharpe"] = [nog.loc[(p, r, g), "Sharpe"] for p, r, g in zip(gd.panel, gd.rung, gd.gross)]
    gd["parent_MaxDD"] = [nog.loc[(p, r, g), "MaxDD"] for p, r, g in zip(gd.panel, gd.rung, gd.gross)]
    gd["dCAGR"] = gd.CAGR - gd.parent_CAGR
    gd["dSharpe"] = gd.Sharpe - gd.parent_Sharpe
    gd["dMaxDD"] = gd.parent_MaxDD.abs() - gd.MaxDD.abs()
    n = len(gd)
    log(f"  gate points: {n}.  dCAGR > 0 in {int((gd.dCAGR > 0).sum())}/{n} "
        f"({(gd.dCAGR > 0).mean():.1%});  median dCAGR {gd.dCAGR.median():+.2%}, "
        f"max {gd.dCAGR.max():+.2%}, min {gd.dCAGR.min():+.2%}")
    log(f"  dSharpe > 0 in {int((gd.dSharpe > 0).sum())}/{n}; median {gd.dSharpe.median():+.4f}, "
        f"max {gd.dSharpe.max():+.4f}")
    log(f"  dMaxDD > 0 (shallower) in {int((gd.dMaxDD > 0).sum())}/{n}; median {gd.dMaxDD.median():+.2%}")
    log("  by depth (median dCAGR / dSharpe / dMaxDD):")
    log(fmt(gd.groupby("depth")[["dCAGR", "dSharpe", "dMaxDD"]].median()))
    log("  by panel:")
    log(fmt(gd.groupby("panel")[["dCAGR", "dSharpe", "dMaxDD"]].median()))
    log("  by cost rung:")
    log(fmt(gd.groupby("rung")[["dCAGR", "dSharpe", "dMaxDD"]].median()))
    gd.to_csv(OUT / f"{SCRIPT[:-3]}.deltas.csv", index=False)

    # ---------------- the queue's premise: which bar does the UNGATED book actually fail?
    log("\n" + "=" * 170)
    log("PREMISE CHECK - the queue says idea 28's book misses the CAGR floor by 0.23pp with DD to spare.")
    log("Ungated EWALL at every panel/gross/rung, with the signed margin on each 4b bar:")
    ctl = grid[grid.family == "control"]
    log(fmt(ctl.set_index(["panel", "rung", "gross"])[
        ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "CAGR_margin", "DD_margin",
         "p4a", "p4b", "fail4b"]]))

    # ---------------- P2: 4b footprint
    log("\n" + "=" * 170)
    log("P2 - KEEP-PATH FOOTPRINT (all cells, both paths, every rung).")
    tot = grid[grid.family.isin(["gate", "control"])]
    for rung in RUNGS:
        s = tot[tot.rung == rung]
        sg = s[s.family == "gate"]; sc = s[s.family == "control"]
        log(f"  {rung:>2} bps: 4b gate {int(sg.p4b.sum())}/{len(sg)}, control {int(sc.p4b.sum())}/{len(sc)} | "
            f"4a gate {int(sg.p4a.sum())}/{len(sg)}, control {int(sc.p4a.sum())}/{len(sc)}")
    pas = tot[tot.p4b]
    if len(pas):
        log("\n  every 4b pass, with the bar its own ungated parent failed:")
        pas = pas.copy()
        pk = nog.reset_index().set_index(["panel", "rung", "gross"])
        pas["parent_fail4b"] = [pk.loc[(p, r, g), "fail4b"] if not np.isnan(g) else "-"
                                for p, r, g in zip(pas.panel, pas.rung, pas.gross)]
        log(fmt(pas.set_index(["panel", "rung", "arm"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "on_share", "parent_fail4b"]]))
    else:
        log("  no 4b pass anywhere on the grid.")

    # ---------------- P3: matched gross
    log("\n" + "=" * 170)
    log("P3 - GATE vs its own MATCHED-GROSS STATIC TWIN (headline rung/gross; g_eff = 0.75 * mean mult).")
    log(f"  gate beats static on Sharpe in {int((matched.dSharpe > 0).sum())}/{len(matched)} cells; "
        f"median dSharpe {matched.dSharpe.median():+.4f}, max {matched.dSharpe.max():+.4f}")
    log(f"  gate shallower on MaxDD in {int((matched.dMaxDD > 0).sum())}/{len(matched)}; "
        f"median dMaxDD {matched.dMaxDD.median():+.2%}")
    log(f"  4b: gate {int(matched.gate_4b.sum())}/{len(matched)} vs static twin "
        f"{int(matched.static_4b.sum())}/{len(matched)}")
    log(fmt(matched.set_index(["panel", "cadence", "B", "depth"])))

    # ---------------- rule 8
    log("\n" + "=" * 170)
    log("RULE 8 WALK-FORWARD - (B, depth) chosen on 2009-2016 IS Sharpe at gross 0.75; 2017-2026 read once.")
    log("vs_nogate = OOS Sharpe of the chosen gate minus the OOS Sharpe of DOING NOTHING (ungated parent).")
    log(fmt(wf.set_index(["panel", "rung", "cadence"])))
    log(f"\n  chooser beats do-nothing in {int((wf.vs_nogate > 0).sum())}/{len(wf)} cells; "
        f"median {wf.vs_nogate.median():+.4f}")
    log(f"  chooser beats the grid-mean anchor in {int((wf.OOS_Sharpe > wf.grid_mean_OOS).sum())}/{len(wf)}; "
        f"median regret vs best OOS {wf.regret.median():+.4f}")
    log(f"  chosen OOS Sharpe > SPY OOS in {int((wf.OOS_Sharpe > wf.spy_OOS).sum())}/{len(wf)}")

    # ---------------- cost breakeven
    log("\n" + "=" * 170)
    log(f"COST BREAKEVEN c* - highest rung in {BE_RUNGS[0]}..{BE_RUNGS[-1]} bps (step 2) at which the arm is still")
    log("inside 4b; first_fail = first rung outside it; fail_at_25 = which bars fail at 25 bps.")
    log("Pre-registered arms only: the ungated parent and depth=0.50 at each B, cadence D.")
    log(fmt(bes.set_index(["panel", "gross", "arm"])))
    gp = bes[bes.arm != "NOGATE"].merge(
        bes[bes.arm == "NOGATE"][["panel", "gross", "c_star"]].rename(columns={"c_star": "parent_c"}),
        on=["panel", "gross"])
    both = gp.dropna(subset=["c_star", "parent_c"])
    log(f"\n  does the gate buy cost tolerance?  gate c* > parent c* in "
        f"{int((gp.c_star.fillna(-1) > gp.parent_c.fillna(-1)).sum())}/{len(gp)} arms; "
        f"equal in {int((gp.c_star.fillna(-1) == gp.parent_c.fillna(-1)).sum())}, "
        f"worse in {int((gp.c_star.fillna(-1) < gp.parent_c.fillna(-1)).sum())}"
        + (f"; median gap {float((both.c_star - both.parent_c).median()):+.1f} bps" if len(both) else ""))

    (OUT / f"{SCRIPT[:-3]}.console.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
