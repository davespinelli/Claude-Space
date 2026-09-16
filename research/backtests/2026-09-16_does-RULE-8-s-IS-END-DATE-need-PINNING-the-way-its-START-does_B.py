#!/usr/bin/env python3
"""Idea 1013 (lane B, 2026-09-16) — does RULE 8's IS END DATE need PINNING the way its START
does?

QUESTION (QUEUE idea 1013, verbatim)
    idea 1001 found 971's whole window effect is a WINDOW-END object: inside `[w, 2016-12-31]`
    SPY's `L_H1` bar moves 1.0717 over the legal starts against 0.1975 on the full tape
    (5.43x), and at w=2012 SEVEN of the record's nine committed 4b passes lose `L_H1`.
    PROTOCOL rule 8 fixes the end at 2016-12-31 by fiat.  Slide the IS END across 2015-2018 at
    a fixed start and report how many committed passes and rule-8 picks change.
    Max 2 params (IS end grid, chooser).

WHAT IS NEW AGAINST 1001.  1001 slid the window START with the end PINNED at 2016-12-31, and
    found the effect lives at the window END.  That run could not separate two things, because
    moving the start moves the IS window AND the halves AND nothing else: the OOS window never
    moved.  1013 does the complementary experiment — START pinned at the record's own
    `px.index[260]`, END slid — which moves the IS window and the OOS window in opposite
    directions at once.  Every number below is therefore about the SPLIT POINT, the one dial
    PROTOCOL rule 8 sets by fiat and never justifies.

    Concretely, sliding E changes four things and leaves one alone:
      L1_H1, L2_H2   the record's halves are a COUNT split of the FULL post-warm-up path
                     (`baseline._row`, `h = len(r)//2`), so they do NOT move with E.  Stated
                     here because it bounds the whole result: at most THREE of 4b's five legs
                     can respond to the IS end at all.
      L3_OOS         book OOS Sharpe vs SPY OOS Sharpe — BOTH sides move with E.
      L4_DD, L5_CAGR the book's OOS drawdown and OOS CAGR move with E; whether the BAR moves
                     is a convention, and both conventions are published (see BAR below).
      the rule-8 PICK moves with E through the IS window the chooser reads.

WHAT IS MEASURED
    (A) THE VERDICT LADDER.  Every book in both claim sets, re-read at every E in the grid:
        the five 4b legs, the 4b verdict, the 4a verdict, and the binding (failed) leg set.
        The deliverable is an integer — how many books change 4b verdict as E slides — and,
        for the committed shelf, WHICH ones and at WHICH E.
    (B) THE COMPARAND'S OWN MOVEMENT.  SPY's OOS Sharpe bar over the E grid, printed beside
        1001's published START-dial numbers (1.0717 over legal starts, 0.1975 on the full
        tape) so the two dials are read in the same units.
    (C) THE ATTRIBUTION.  Pass count over E against (i) SPY's own OOS Sharpe at that E and
        (ii) the OOS window's LENGTH.  If the benchmark's bar carries it, the split point is a
        BENCHMARK dial; if length carries it, it is a POWER dial.  They are not the same
        defect and they do not have the same fix.
    (D) THE RULE-8 PICKS.  Three IS-only choosers x 2 panels x the E grid, picking from the
        never-memo-selected GRID ladder, evaluated once on the OOS window that E defines.
        Reported as pick identity, pick stability, and OOS CAGR/Sharpe/MaxDD vs the live
        baseline and vs SPY.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported, none
selected.
    (1) IS END GRID in {END_Q, END_Y}
          END_Q  the 16 quarter-ends 2015-03-31 ... 2018-12-31            <- HEADLINE
          END_Y  the 4 year-ends 2015-12-31 ... 2018-12-31                <- coarse control
          PROTOCOL's own 2016-12-31 ("REC") is a member of both and is the reference everywhere.
    (2) CHOOSER in {IS_SHARPE, IS_LEGS, IS_CAGR}, all three reported at every E.

    NOT TUNED, reported as CONTROLS at every point:
      CLAIM SET   SHELF (the record's committed memo-backed 4b passes, rebuilt from lane C's
                  own `shelf_books`) and GRID (the mechanical band x gross x QROLL ladder,
                  never memo-selected).  SHELF answers "how many committed passes change";
                  GRID is the clean selection pool for the picks, because the SHELF was chosen
                  on the full tape and cannot be picked from without contamination.
      BAR         the 4b DD/CAGR bar convention.  REC_FULL is the record's own (`L4_DD` and
                  `L5_CAGR` read against SPY's FULL-sample MaxDD/CAGR, so the BAR is
                  E-invariant and only the book's OOS side moves); WIN reads the same two legs
                  against SPY's OWN OOS-window MaxDD/CAGR, so both sides move.  Both are
                  published at every point; REC_FULL is the reference because it is what every
                  committed row in this record used.
      COST        0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL       U56 (binding) and B136 (labelled replication).  Each keeps its OWN calendar
                  (B136's broad cache is Friday-refreshed and ends 4 sessions earlier); every
                  metric here is within-panel, so no splice is needed and none is done.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_PIN     HEADLINE.  >= 0.90 of all books hold the SAME 4b verdict at every E in END_Q.
              PASS => the IS end does NOT need pinning; the fiat is harmless.
              FAIL => it does, and PROTOCOL rule 8 has an unpinned dial.
    H_SHELF   >= 0.90 of the committed memo-backed SHELF holds its 4b verdict at every E.
              1001's analogue on the START dial failed 7 of 9 at w=2012.
    H_PICK    the rule-8 PICK is E-invariant across END_Q for ALL THREE choosers on BOTH
              panels (6 of 6 cells constant).
    H_BAR     the END dial moves SPY's OOS Sharpe bar LESS than 1001's START dial moved its
              L_H1 bar: range(SPY OOS Sharpe over END_Q) <= 0.1975, 1001's own full-tape
              figure.  PASS => the end is the tamer half of the window.
    H_MONO    the 4b pass COUNT is monotone in E (non-increasing or non-decreasing) over
              END_Q.  PASS => the split point is a LENGTH dial; FAIL => it is a REGIME dial
              and no amount of "use more data" fixes it.
    H_LEG     the BINDING leg set is E-invariant for >= 0.90 of books over END_Q.
    H_COMP    |Pearson(pass count, SPY OOS Sharpe)| > |Pearson(pass count, OOS years)| over
              END_Q.  PASS => the benchmark's bar carries the split-point effect, as 1001
              found for the start.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                  0.0
    G3  CROSS-RUN: at E = REC, SPY's OOS triple == the record's committed 15.21% / 0.8713 /
        -33.72% (idea 1009's G4, itself the standing comparand).
    G4  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G5  determinism: the whole E ladder rebuilt reproduces bit-for-bit.                  0.0
    G6  IS PURITY: every chooser's pick is invariant under a permutation of the OOS returns.
    G7  LEG IDENTITY: at E = REC the five legs equal the record's own `legs_rec` block
        computed independently from full/IS/OOS metric dicts.                     0 rows

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b pass count is an UPPER bound.  The measured
    object is the MOVEMENT of a verdict as one date slides on the SAME books over the SAME
    tape; the survivorship bias is a common factor to every E and very largely cancels.  Where
    it does not cancel it works AGAINST this run's own suspicion: a survivor panel's books are
    steadier than real-time ones, so the verdict instability measured here is a LOWER bound and
    H_PIN is the EASIER hypothesis to pass.  SPY is a real index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-RULE-8-s-IS-END-DATE-need-PINNING-the-way-its-START-does"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
BARS = ["REC_FULL", "WIN"]
BAR_REF = "REC_FULL"
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
# 1001's published START-dial numbers, quoted so the two dials are read in the same units.
START_LEGAL_RANGE, START_FULLTAPE_RANGE = 1.0717, 0.1975
# the record's committed SPY OOS triple at E = REC (idea 1009 G4)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC865", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load_lane_c()
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_GRIDS = {
    "END_Q": quarter_ends("2015-01-01", "2018-12-31"),
    "END_Y": ["2015-12-31", "2016-12-31", "2017-12-31", "2018-12-31"],
}
EGRID_HEAD = "END_Q"


def metblock(r):
    """Full-sample CAGR/Sharpe/MaxDD plus the record's COUNT halves (`baseline._row`)."""
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def legs_at(bk, bspy, bar):
    """PROTOCOL 4b's five legs, in the record's own wording.

    bk / bspy carry keys H1, H2 (FULL-sample count halves, E-invariant), OOS_Sharpe, OOS_CAGR,
    OOS_MaxDD, and the bar side also FULL MaxDD/CAGR.  `bar` selects which SPY window the DD
    cap and the CAGR floor are read against; both are published.
    """
    if bar == "REC_FULL":
        dd_bar, cagr_bar = abs(bspy["MaxDD"]), bspy["CAGR"]
    else:
        dd_bar, cagr_bar = abs(bspy["OOS_MaxDD"]), bspy["OOS_CAGR"]
    return {
        "L1_H1": bk["H1"] > bspy["H1"],
        "L2_H2": bk["H2"] > bspy["H2"],
        "L3_OOS": bk["OOS_Sharpe"] > bspy["OOS_Sharpe"],
        "L4_DD": abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * dd_bar,
        "L5_CAGR": bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * cagr_bar,
    }


def failstr(lg):
    f = [k for k in LEGS if not lg[k]]
    return "+".join(f) if f else "-"


def path_block(net, spy, e):
    """Everything a verdict needs for one (book, E): full-sample halves plus the OOS window."""
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o) if len(o) > 10 else (np.nan,) * 3
    ic, is_, idd = fmet(i) if len(i) > 10 else (np.nan,) * 3
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def main():
    t0 = time.time()
    P(f"# Idea 1013 (lane B, {DATE}) — does RULE 8's IS END DATE need PINNING the way its "
      f"START does?")
    P(f"# 2 tuned dials: IS END GRID {list(END_GRIDS)} x CHOOSER {CHOOSERS}.  All points "
      f"reported, none selected.")
    P(f"# CONTROLS at every point: CLAIM SET [SHELF, GRID], BAR {BARS} (ref {BAR_REF}), "
      f"COST {RUNGS} bps (head {RUNG_HEAD:.0f}), PANEL [U56, B136].")
    P(f"# START is PINNED at the record's own px.index[{WARMUP}]; only the SPLIT POINT moves.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic and")
    P("#   the measured verdict instability is a LOWER bound, i.e. H_PIN is the EASIER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")
    P(f"Fixed start (both panels): {REC['U56'].date()} / {REC['B136'].date()}.  Panels keep "
      f"their OWN calendars; every metric here is within-panel.")

    shelf = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    shelf["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    grid = C.grid_books(U, B)
    SETS = {"SHELF": shelf, "GRID": grid}
    P(f"SHELF = {len(shelf)} committed memo-backed 4b passes; GRID = {len(grid)} "
      f"never-memo-selected ladder books (the clean selection pool for rule 8).")
    P(f"IS END grids: END_Q = {len(END_GRIDS['END_Q'])} quarter-ends "
      f"{END_GRIDS['END_Q'][0]}..{END_GRIDS['END_Q'][-1]} (headline); "
      f"END_Y = {END_GRIDS['END_Y']}.  PROTOCOL's own {REC_END} is in both.")
    P("")

    # ---------------------------------------------------------------- net return paths
    NET, TURN = {}, {}
    for sname, bset in SETS.items():
        for nm, b in bset.items():
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
            st = REC[b["panel"]]
            for c in RUNGS:
                NET[(sname, nm, c)] = (r - t * c / 1e4).loc[st:]
            TURN[(sname, nm)] = t.loc[st:].sum() / (len(t.loc[st:]) / 252.0)
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = (r - t * c / 1e4).loc[REC[p]:]

    # ================================================================ GATES
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    # G1 fast runner == engine.backtest
    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    g1 = d_r < 1e-12 and d_t < 1e-10
    P(f"G1 fast_run == engine.backtest (returns / turnover): {d_r:.3e} / {d_t:.3e}  "
      f"{'PASS' if g1 else 'FAIL'}")
    gates.append(dict(gate="G1", what="fast runner == engine.backtest",
                      value=f"{d_r:.3e}/{d_t:.3e}", verdict="PASS" if g1 else "FAIL"))

    # G2 the band book IS the live baseline
    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    g2 = d2 == 0.0
    P(f"G2 rules_v2_weights(U,0.03,0.75) == baseline.rules_v2_weights(U): {d2:.3e}  "
      f"{'PASS' if g2 else 'FAIL'}")
    gates.append(dict(gate="G2", what="band book == live baseline", value=f"{d2:.3e}",
                      verdict="PASS" if g2 else "FAIL"))

    # G3 SPY's committed OOS triple at E = REC
    sp = path_block(SPYR["U56"], None, REC_END)
    trip = (sp["OOS_CAGR"], sp["OOS_Sharpe"], sp["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    g3 = d3 <= 5e-4
    P(f"G3 CROSS-RUN SPY OOS at E={REC_END}: {trip[0]:.4%} / {trip[1]:.4f} / {trip[2]:.4%} "
      f"vs committed {SPY_OOS_COMMITTED[0]:.2%} / {SPY_OOS_COMMITTED[1]:.4f} / "
      f"{SPY_OOS_COMMITTED[2]:.2%}  max|d| {d3:.3e}  {'PASS' if g3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY OOS triple vs record", value=f"{d3:.3e}",
                      verdict="PASS" if g3 else "FAIL"))

    # G4 shelf memo triples
    grows, ok4 = [], True
    for nm, b in shelf.items():
        n = NET[("SHELF", nm, RUNG_HEAD)].values
        c, s, d = fmet(n)
        m = b["memo"]
        dc = abs(c - m[0]) if m[0] is not None else 0.0
        ds = abs(s - m[1]) if m[1] is not None else 0.0
        dv = abs(d - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dv <= 0.015
        ok4 &= good
        grows.append(dict(book=nm, panel=b["panel"], CAGR=c, Sharpe=s, MaxDD=d,
                          memo_CAGR=m[0], memo_Sharpe=m[1], memo_MaxDD=m[2],
                          d_CAGR=dc, d_Sharpe=ds, d_MaxDD=dv,
                          verdict="PASS" if good else "FAIL", src=b["src"]))
    P(f"G4 SHELF memo triples: {sum(r['verdict'] == 'PASS' for r in grows)}/{len(grows)}  "
      f"{'PASS' if ok4 else 'FAIL'}")
    for r in grows:
        if r["verdict"] == "FAIL":
            P(f"     {r['book']:34s} d {r['d_CAGR']:.4f}/{r['d_Sharpe']:.4f}/{r['d_MaxDD']:.4f}")
    gates.append(dict(gate="G4", what="SHELF memo triples",
                      value=f"{sum(r['verdict']=='PASS' for r in grows)}/{len(grows)}",
                      verdict="PASS" if ok4 else "FAIL"))
    dump(pd.DataFrame(grows), "shelf")

    # ---------------------------------------------------------------- THE VERDICT LADDER
    ALLE = sorted(set(END_GRIDS["END_Q"]) | set(END_GRIDS["END_Y"]))
    SPYB = {(p, e): path_block(SPYR[p], None, e) for p in PX for e in ALLE}

    def build_ladder():
        rows = []
        for sname, bset in SETS.items():
            for nm, b in bset.items():
                p = b["panel"]
                for c in RUNGS:
                    net = NET[(sname, nm, c)]
                    for e in ALLE:
                        bk = path_block(net, None, e)
                        sb = SPYB[(p, e)]
                        row = dict(set=sname, book=nm, panel=p, freq=b["freq"], cost=c, E=e,
                                   OOS_years=bk["OOS_n"] / 252.0, IS_years=bk["IS_n"] / 252.0,
                                   **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                         "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
                                                         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                   spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                                   spy_OOS_MaxDD=sb["OOS_MaxDD"])
                        for bar in BARS:
                            lg = legs_at(bk, sb, bar)
                            row[f"pass4b_{bar}"] = all(lg.values())
                            row[f"fail4b_{bar}"] = failstr(lg)
                            for k in LEGS:
                                row[f"{k}_{bar}"] = lg[k]
                        v2 = metblock(V2[(p, c)].values)
                        row["pass4a"] = (bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                         and bk["MaxDD"] >= v2["MaxDD"])
                        rows.append(row)
        return pd.DataFrame(rows)

    L = build_ladder()

    # G5 determinism
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    g5 = d5 == 0.0
    P(f"G5 determinism over the whole {len(L):,}-row ladder: {d5:.3e}  {'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="ladder determinism", value=f"{d5:.3e}",
                      verdict="PASS" if g5 else "FAIL"))

    # G7 leg identity at E = REC against an independently computed block
    bad7 = 0
    for _, r in L[(L.E == REC_END) & (L.cost == RUNG_HEAD)].iterrows():
        sb = SPYB[(r["panel"], REC_END)]
        lg = {"L1_H1": r["H1"] > sb["H1"], "L2_H2": r["H2"] > sb["H2"],
              "L3_OOS": r["OOS_Sharpe"] > sb["OOS_Sharpe"],
              "L4_DD": abs(r["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"]),
              "L5_CAGR": r["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]}
        if any(bool(lg[k]) != bool(r[f"{k}_REC_FULL"]) for k in LEGS):
            bad7 += 1
    g7 = bad7 == 0
    P(f"G7 leg identity at E={REC_END} (independent recomputation): {bad7} disagreeing rows  "
      f"{'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="leg identity at REC", value=f"{bad7} rows",
                      verdict="PASS" if g7 else "FAIL"))

    # ---------------------------------------------------------------- RULE 8: the picks
    def choose(sub, ch):
        if sub.empty:
            return None
        if ch == "IS_SHARPE":
            k = sub["IS_Sharpe"].idxmax()
        elif ch == "IS_CAGR":
            k = sub["IS_CAGR"].idxmax()
        else:
            s = sub.copy()
            s["nlegs"] = ((s["IS_Sharpe"] > s["spy_IS_Sharpe"]).astype(int)
                          + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * s["spy_IS_CAGR"]).astype(int)
                          + (s["IS_MaxDD"] >= DDCAP_FRAC * s["spy_IS_MaxDD"]).astype(int))
            s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
            k = s.index[0]
        return sub.loc[k]

    SPYIS = {}
    for p in PX:
        for e in ALLE:
            i = SPYR[p].loc[:pd.Timestamp(e)].values
            c, s, d = fmet(i)
            SPYIS[(p, e)] = (c, s, d)
    L["spy_IS_CAGR"] = [SPYIS[(r.panel, r.E)][0] for r in L.itertuples()]
    L["spy_IS_Sharpe"] = [SPYIS[(r.panel, r.E)][1] for r in L.itertuples()]
    L["spy_IS_MaxDD"] = [SPYIS[(r.panel, r.E)][2] for r in L.itertuples()]

    picks = []
    for pool in ("GRID", "ALL"):
        sel = L if pool == "ALL" else L[L.set == "GRID"]
        for p in PX:
            for e in ALLE:
                for ch in CHOOSERS:
                    sub = sel[(sel.panel == p) & (sel.E == e) & (sel.cost == RUNG_HEAD)]
                    r = choose(sub, ch)
                    if r is None:
                        continue
                    v2 = metblock(V2[(p, RUNG_HEAD)].values)
                    v2o = path_block(V2[(p, RUNG_HEAD)], None, e)
                    sb = SPYB[(p, e)]
                    picks.append(dict(pool=pool, panel=p, E=e, chooser=ch, pick=r["book"],
                                      set=r["set"], freq=r["freq"],
                                      IS_Sharpe=r["IS_Sharpe"], IS_CAGR=r["IS_CAGR"],
                                      OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                                      OOS_MaxDD=r["OOS_MaxDD"],
                                      pass4b=r["pass4b_REC_FULL"], fail4b=r["fail4b_REC_FULL"],
                                      pass4b_WIN=r["pass4b_WIN"], pass4a=r["pass4a"],
                                      spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                      spy_OOS_MaxDD=sb["OOS_MaxDD"], spy_CAGR=sb["CAGR"],
                                      spy_Sharpe=sb["Sharpe"], spy_MaxDD=sb["MaxDD"],
                                      v2_OOS_CAGR=v2o["OOS_CAGR"], v2_OOS_Sharpe=v2o["OOS_Sharpe"],
                                      v2_OOS_MaxDD=v2o["OOS_MaxDD"], v2_Sharpe=v2["Sharpe"],
                                      v2_MaxDD=v2["MaxDD"]))
    K = pd.DataFrame(picks)

    # G6 IS purity: permuting the OOS block must not move a pick
    rng = np.random.default_rng(1013)
    bad6 = 0
    for p in PX:
        e = REC_END
        sub = L[(L.panel == p) & (L.E == e) & (L.cost == RUNG_HEAD) & (L.set == "GRID")].copy()
        perm = sub.copy()
        for col in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"):
            perm[col] = rng.permutation(perm[col].values)
        for ch in CHOOSERS:
            if choose(sub, ch)["book"] != choose(perm, ch)["book"]:
                bad6 += 1
    g6 = bad6 == 0
    P(f"G6 IS purity (picks invariant under permuted OOS columns): {bad6} disagreements  "
      f"{'PASS' if g6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="IS purity of choosers", value=f"{bad6}",
                      verdict="PASS" if g6 else "FAIL"))

    ng = sum(g["verdict"] == "PASS" for g in gates)
    P(f"\nGATES {ng} of {len(gates)} PASS.\n")
    dump(pd.DataFrame(gates), "gates")

    # ================================================================ (A) THE VERDICT LADDER
    P("## A. THE VERDICT LADDER — how many books change 4b verdict as the IS END slides")
    HQ = END_GRIDS[EGRID_HEAD]
    stab_rows = []
    for egrid, EL in END_GRIDS.items():
        for bar in BARS:
            for c in RUNGS:
                sub = L[(L.cost == c) & (L.E.isin(EL))]
                for sname in ("SHELF", "GRID", "ALL"):
                    s = sub if sname == "ALL" else sub[sub.set == sname]
                    g = s.groupby("book")[f"pass4b_{bar}"]
                    nb = g.ngroups
                    const = int((g.nunique() == 1).sum())
                    lg = s.groupby("book")[f"fail4b_{bar}"].nunique()
                    stab_rows.append(dict(egrid=egrid, bar=bar, cost=c, set=sname, n_books=nb,
                                          n_verdict_const=const, frac_const=const / nb,
                                          n_legset_const=int((lg == 1).sum()),
                                          frac_legset_const=float((lg == 1).mean()),
                                          n_pass_at_REC=int(s[(s.E == REC_END)][f"pass4b_{bar}"].sum()),
                                          n_pass_ever=int((s.groupby("book")[f"pass4b_{bar}"]
                                                           .max()).sum()),
                                          n_pass_always=int((s.groupby("book")[f"pass4b_{bar}"]
                                                             .min()).sum())))
    S = pd.DataFrame(stab_rows)
    head = S[(S.egrid == EGRID_HEAD) & (S.bar == BAR_REF) & (S.cost == RUNG_HEAD)]
    P(f"  Headline cell (END_Q x {BAR_REF} x {RUNG_HEAD:.0f} bps):")
    for _, r in head.iterrows():
        P(f"    {r['set']:5s}  {r.n_books:3d} books   verdict CONSTANT over the 16 ends "
          f"{r.n_verdict_const:3d} ({r.frac_const:.3f})   binding-leg-set constant "
          f"{r.n_legset_const:3d} ({r.frac_legset_const:.3f})")
        P(f"           4b passes: at E={REC_END} {r.n_pass_at_REC:3d} | at SOME E "
          f"{r.n_pass_ever:3d} | at EVERY E {r.n_pass_always:3d}")
    P("  Same cell under the WIN bar convention (SPY's own OOS drawdown/CAGR):")
    for _, r in S[(S.egrid == EGRID_HEAD) & (S.bar == "WIN") & (S.cost == RUNG_HEAD)].iterrows():
        P(f"    {r['set']:5s}  verdict constant {r.n_verdict_const:3d}/{r.n_books:3d} "
          f"({r.frac_const:.3f})   passes at REC {r.n_pass_at_REC:3d} | ever {r.n_pass_ever:3d} "
          f"| always {r.n_pass_always:3d}")
    dump(S, "stability")

    P("\n  SHELF book by book (END_Q, REC_FULL, 10 bps) — the committed passes the queue asks about:")
    sh = L[(L.set == "SHELF") & (L.cost == RUNG_HEAD) & (L.E.isin(HQ))]
    shelf_rows = []
    for nm, g in sh.groupby("book"):
        g = g.sort_values("E")
        np_ = int(g["pass4b_REC_FULL"].sum())
        at_rec = bool(g[g.E == REC_END]["pass4b_REC_FULL"].iloc[0])
        first_fail = [e for e, v in zip(g.E, g["pass4b_REC_FULL"]) if not v]
        shelf_rows.append(dict(book=nm, panel=g.panel.iloc[0], pass_at_REC=at_rec,
                               n_pass=np_, n_E=len(g), frac_pass=np_ / len(g),
                               fails_at=",".join(first_fail[:4]),
                               legset_n=int(g["fail4b_REC_FULL"].nunique())))
        P(f"    {nm:34s} {'PASS' if at_rec else 'FAIL'}@REC   4b passes at "
          f"{np_:2d}/{len(g)} ends   distinct binding-leg-sets {g['fail4b_REC_FULL'].nunique()}")
    dump(pd.DataFrame(shelf_rows), "shelfladder")
    dump(L, "ladder", gz=True)

    # ================================================================ (B) THE COMPARAND
    P("\n## B. THE COMPARAND'S OWN MOVEMENT — the END dial in 1001's units")
    brows = []
    for p in PX:
        for egrid, EL in END_GRIDS.items():
            v = np.array([SPYB[(p, e)]["OOS_Sharpe"] for e in EL])
            vc = np.array([SPYB[(p, e)]["OOS_CAGR"] for e in EL])
            vd = np.array([abs(SPYB[(p, e)]["OOS_MaxDD"]) for e in EL])
            brows.append(dict(panel=p, egrid=egrid, n=len(EL),
                              spy_OOS_Sharpe_min=v.min(), spy_OOS_Sharpe_max=v.max(),
                              spy_OOS_Sharpe_range=v.max() - v.min(),
                              spy_OOS_Sharpe_at_REC=SPYB[(p, REC_END)]["OOS_Sharpe"],
                              spy_OOS_CAGR_range=vc.max() - vc.min(),
                              spy_OOS_MaxDD_range=vd.max() - vd.min(),
                              spy_FULL_Sharpe=SPYB[(p, REC_END)]["Sharpe"],
                              spy_FULL_MaxDD=SPYB[(p, REC_END)]["MaxDD"]))
    BR = pd.DataFrame(brows)
    for _, r in BR[BR.egrid == EGRID_HEAD].iterrows():
        P(f"  {r.panel}: SPY OOS Sharpe over the 16 ends {r.spy_OOS_Sharpe_min:.4f} .. "
          f"{r.spy_OOS_Sharpe_max:.4f}  RANGE {r.spy_OOS_Sharpe_range:.4f}  "
          f"(at E={REC_END}: {r.spy_OOS_Sharpe_at_REC:.4f})")
        P(f"      OOS CAGR range {r.spy_OOS_CAGR_range:.4f}   |OOS MaxDD| range "
          f"{r.spy_OOS_MaxDD_range:.4f}")
    P(f"  1001's START dial, quoted: L_H1 bar moves {START_LEGAL_RANGE:.4f} over the legal "
      f"starts against {START_FULLTAPE_RANGE:.4f} on the full tape (5.43x).")
    dump(BR, "comparand")

    # ================================================================ (C) ATTRIBUTION
    P("\n## C. ATTRIBUTION — is the split point a BENCHMARK dial or a POWER dial?")
    crows = []
    for sname in ("SHELF", "GRID", "ALL"):
        for bar in BARS:
            sub = L[(L.cost == RUNG_HEAD) & (L.E.isin(HQ))]
            if sname != "ALL":
                sub = sub[sub.set == sname]
            cnt = sub.groupby("E")[f"pass4b_{bar}"].sum().reindex(HQ)
            spyv = pd.Series([np.mean([SPYB[(p, e)]["OOS_Sharpe"] for p in PX]) for e in HQ],
                             index=HQ)
            lenv = pd.Series([np.mean([SPYB[(p, e)]["OOS_n"] for p in PX]) / 252.0 for e in HQ],
                             index=HQ)
            r_spy = float(np.corrcoef(cnt.values, spyv.values)[0, 1])
            r_len = float(np.corrcoef(cnt.values, lenv.values)[0, 1])
            dcnt = np.diff(cnt.values)
            crows.append(dict(set=sname, bar=bar, n_E=len(HQ), pass_min=int(cnt.min()),
                              pass_max=int(cnt.max()), pass_at_REC=int(cnt.loc[REC_END]),
                              r_spy_OOS_Sharpe=r_spy, r_OOS_years=r_len,
                              monotone=bool(np.all(dcnt >= 0) or np.all(dcnt <= 0)),
                              n_sign_changes=int(np.sum(np.sign(dcnt[:-1]) * np.sign(dcnt[1:]) < 0))))
    CC = pd.DataFrame(crows)
    for _, r in CC[CC.bar == BAR_REF].iterrows():
        P(f"  {r['set']:5s} 4b pass count over the 16 ends: {r.pass_min}..{r.pass_max} "
          f"(at E={REC_END}: {r.pass_at_REC})   monotone {r.monotone}   sign changes "
          f"{r.n_sign_changes}")
        P(f"          Pearson vs SPY OOS Sharpe {r.r_spy_OOS_Sharpe:+.4f} | vs OOS years "
          f"{r.r_OOS_years:+.4f}")
    cnt_head = (L[(L.cost == RUNG_HEAD) & (L.E.isin(HQ))].groupby("E")[f"pass4b_{BAR_REF}"]
                .sum().reindex(HQ))
    P("  Pass count by end date (ALL books, REC_FULL, 10 bps):")
    P("    " + "  ".join(f"{e[2:7]}:{v}" for e, v in cnt_head.items()))
    dump(CC, "attribution")

    # ================================================================ (D) RULE 8
    P("\n## D. RULE 8 — the walk-forward, and the picks as the IS END slides")
    P(f"  Selection pool = GRID ({len(grid)} never-memo-selected books); ALL "
      f"(GRID+SHELF) is reported as a CONTAMINATED control.")
    prows = []
    for pool in ("GRID", "ALL"):
        for p in PX:
            for ch in CHOOSERS:
                s = K[(K.pool == pool) & (K.panel == p) & (K.chooser == ch)
                      & (K.E.isin(HQ))].sort_values("E")
                prows.append(dict(pool=pool, panel=p, chooser=ch, n_E=len(s),
                                  n_distinct_picks=int(s["pick"].nunique()),
                                  pick_at_REC=s[s.E == REC_END]["pick"].iloc[0],
                                  modal_pick=s["pick"].mode().iloc[0],
                                  modal_share=float((s["pick"] == s["pick"].mode().iloc[0]).mean()),
                                  n_4b=int(s["pass4b"].sum()), n_4a=int(s["pass4a"].sum()),
                                  OOS_Sharpe_min=float(s["OOS_Sharpe"].min()),
                                  OOS_Sharpe_max=float(s["OOS_Sharpe"].max()),
                                  OOS_Sharpe_at_REC=float(s[s.E == REC_END]["OOS_Sharpe"].iloc[0])))
    PKS = pd.DataFrame(prows)
    for _, r in PKS[PKS.pool == "GRID"].iterrows():
        P(f"  {r.panel:5s} {r.chooser:10s} distinct picks over the 16 ends {r.n_distinct_picks:2d} "
          f"(modal {r.modal_pick} at {r.modal_share:.2f}); pick at E={REC_END}: {r.pick_at_REC}")
        P(f"           OOS Sharpe {r.OOS_Sharpe_min:.3f}..{r.OOS_Sharpe_max:.3f} "
          f"(at REC {r.OOS_Sharpe_at_REC:.3f});  OOS 4b {r.n_4b}/16   OOS 4a {r.n_4a}/16")
    dump(PKS, "pickstability")
    dump(K, "picks")

    P(f"\n  THE MANDATORY RULE-8 WALK-FORWARD at PROTOCOL's own E = {REC_END} "
      f"(pool GRID, 10 bps):")
    P(f"    {'panel':6s} {'chooser':10s} {'pick':32s} {'OOS CAGR':>9s} {'OOS Sh':>7s} "
      f"{'OOS DD':>8s}  4b  4a")
    wf = []
    for _, r in K[(K.pool == "GRID") & (K.E == REC_END)].iterrows():
        P(f"    {r.panel:6s} {r.chooser:10s} {r['pick']:32s} {r.OOS_CAGR:8.2%} "
          f"{r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%}  {'Y' if r.pass4b else 'n'}   "
          f"{'Y' if r.pass4a else 'n'}   [{r.fail4b}]")
        wf.append(r)
    for p in PX:
        sb = SPYB[(p, REC_END)]
        v2o = path_block(V2[(p, RUNG_HEAD)], None, REC_END)
        v2f = metblock(V2[(p, RUNG_HEAD)].values)
        P(f"    {p:6s} {'SPY':10s} {'(comparand)':32s} {sb['OOS_CAGR']:8.2%} "
          f"{sb['OOS_Sharpe']:7.3f} {sb['OOS_MaxDD']:8.2%}   full {sb['Sharpe']:.3f} / "
          f"{sb['MaxDD']:.2%}")
        P(f"    {p:6s} {'RULESv2':10s} {'(live baseline)':32s} {v2o['OOS_CAGR']:8.2%} "
          f"{v2o['OOS_Sharpe']:7.3f} {v2o['OOS_MaxDD']:8.2%}   full {v2f['Sharpe']:.3f} / "
          f"{v2f['MaxDD']:.2%}")
    P(f"    KEEP path 4a over the {len(K[K.pool=='GRID'])} GRID picks: "
      f"{int(K[K.pool=='GRID']['pass4a'].sum())}; over the whole "
      f"{len(L[L.cost==RUNG_HEAD]):,}-row 10 bps ladder: "
      f"{int(L[L.cost==RUNG_HEAD]['pass4a'].sum())}.")
    P(f"    KEEP path 4b over the GRID picks: {int(K[K.pool=='GRID']['pass4b'].sum())}; over "
      f"the 10 bps ladder: {int(L[L.cost==RUNG_HEAD]['pass4b_REC_FULL'].sum())} "
      f"(WIN bar: {int(L[L.cost==RUNG_HEAD]['pass4b_WIN'].sum())}).")
    dump(K[(K.pool == "GRID") & (K.E == REC_END)], "walkforward")

    # ================================================================ (E) MECHANISM
    P("\n## E. MECHANISM — WHICH leg the split point can move, and what the fiat costs")
    erows = []
    for bar in BARS:
        for c in RUNGS:
            sub = L[(L.cost == c) & (L.E.isin(HQ))]
            for k in LEGS:
                g = sub.groupby("book")[f"{k}_{bar}"]
                erows.append(dict(bar=bar, cost=c, leg=k, n_books=g.ngroups,
                                  n_leg_const=int((g.nunique() == 1).sum()),
                                  frac_leg_const=float((g.nunique() == 1).mean())))
    LS = pd.DataFrame(erows)
    P(f"  Per-leg E-sensitivity (END_Q, {BAR_REF}, {RUNG_HEAD:.0f} bps) — how many of the 45 "
      f"books hold that leg at every end:")
    for _, r in LS[(LS.bar == BAR_REF) & (LS.cost == RUNG_HEAD)].iterrows():
        P(f"    {r.leg:8s} constant on {r.n_leg_const:3d}/{r.n_books} books "
          f"({r.frac_leg_const:.3f})")
    P("  L1_H1 / L2_H2 are E-INVARIANT BY CONSTRUCTION: the record's halves are a COUNT split")
    P("    of the FULL post-warm-up path (`baseline._row`), which the split point never touches.")
    dump(LS, "legsensitivity")

    frows = []
    for bar in BARS:
        for c in RUNGS:
            sub = L[(L.cost == c) & (L.E.isin(HQ))]
            g = sub.groupby(["set", "book"])[f"pass4b_{bar}"]
            for (sname, nm), n in g.nunique().items():
                if n > 1:
                    r = sub[sub.book == nm].sort_values("E")
                    frows.append(dict(bar=bar, cost=c, set=sname, book=nm,
                                      panel=r.panel.iloc[0],
                                      seq="".join("P" if v else "." for v in r[f"pass4b_{bar}"]),
                                      n_pass=int(r[f"pass4b_{bar}"].sum()), n_E=len(r),
                                      legsets="|".join(sorted(r[f"fail4b_{bar}"].unique()))))
    F = pd.DataFrame(frows)
    P(f"\n  Every book whose 4b verdict FLIPS across the 16 ends ({BAR_REF}, {RUNG_HEAD:.0f} bps), "
      f"in end order 2015Q1..2018Q4:")
    for _, r in F[(F.bar == BAR_REF) & (F.cost == RUNG_HEAD)].iterrows():
        P(f"    {r['set']:5s} {r.book:32s} {r.seq}  {r.n_pass}/{r.n_E} ends   "
          f"leg sets seen: {r.legsets}")
    P(f"\n  COST-RUNG CONTROL — the same stability at every rung ({BAR_REF}, ALL books):")
    for c in RUNGS:
        rr = S[(S.egrid == EGRID_HEAD) & (S.bar == BAR_REF) & (S.cost == c) & (S.set == "ALL")]
        rr = rr.iloc[0]
        P(f"    {c:5.1f} bps: verdict constant {rr.n_verdict_const}/{rr.n_books} "
          f"({rr.frac_const:.4f})   4b passes at E={REC_END}: {rr.n_pass_at_REC}")
    dump(F, "flippers")

    P(f"\n  THE PRICE OF THE FIAT — the rule-8 pick's PUBLISHED numbers across the 16 legal "
      f"split points (pool GRID, {RUNG_HEAD:.0f} bps):")
    srows = []
    for (p, ch), g in K[(K.pool == "GRID") & (K.E.isin(HQ))].groupby(["panel", "chooser"]):
        srows.append(dict(panel=p, chooser=ch, n_distinct_picks=int(g["pick"].nunique()),
                          OOS_Sharpe_spread=float(g.OOS_Sharpe.max() - g.OOS_Sharpe.min()),
                          OOS_CAGR_spread=float(g.OOS_CAGR.max() - g.OOS_CAGR.min()),
                          OOS_MaxDD_spread=float(g.OOS_MaxDD.max() - g.OOS_MaxDD.min()),
                          n_4b=int(g.pass4b.sum()), n_E=len(g)))
        P(f"    {p:5s} {ch:10s} {g['pick'].nunique()} distinct pick(s)   OOS Sharpe spread "
          f"{g.OOS_Sharpe.max() - g.OOS_Sharpe.min():.4f}   OOS CAGR spread "
          f"{g.OOS_CAGR.max() - g.OOS_CAGR.min():.4f}   OOS MaxDD spread "
          f"{g.OOS_MaxDD.max() - g.OOS_MaxDD.min():.4f}   4b {int(g.pass4b.sum())}/{len(g)}")
    SP = pd.DataFrame(srows)
    P(f"    Worst cell: OOS Sharpe moves {SP.OOS_Sharpe_spread.max():.4f} purely from the split "
      f"date.  For scale, idea 1001's median SHELF HALFMIN leg margin is 0.2102 against")
    P("    comparand bootstrap SEs of 0.2877 / 0.3350 — the split-point swing is the same order")
    P("    as the leg margins the record certifies passes on.")
    dump(SP, "fiatprice")

    # ================================================================ HYPOTHESES
    P("\n## HYPOTHESES (bars declared in the header, before any number above was read)")
    hyp = []

    def H(name, bar, val, ok, note=""):
        hyp.append(dict(name=name, bar=bar, value=val, verdict="PASS" if ok else "FAIL",
                        note=note))
        P(f"  {name:9s} {'PASS' if ok else 'FAIL'}   bar: {bar}")
        P(f"            got: {val}{('   ' + note) if note else ''}")

    rall = head[head.set == "ALL"].iloc[0]
    H("H_PIN", ">= 0.90 of ALL books hold the same 4b verdict at every E in END_Q",
      f"{rall.frac_const:.4f} ({rall.n_verdict_const}/{rall.n_books})",
      rall.frac_const >= 0.90,
      "HEADLINE — PASS means the IS end does not need pinning")
    rsh = head[head.set == "SHELF"].iloc[0]
    H("H_SHELF", ">= 0.90 of the committed SHELF holds its 4b verdict at every E",
      f"{rsh.frac_const:.4f} ({rsh.n_verdict_const}/{rsh.n_books})", rsh.frac_const >= 0.90,
      f"passes at E={REC_END}: {rsh.n_pass_at_REC}; at every E: {rsh.n_pass_always}; "
      f"at some E: {rsh.n_pass_ever}")
    gp = PKS[PKS.pool == "GRID"]
    nconst = int((gp["n_distinct_picks"] == 1).sum())
    H("H_PICK", "the rule-8 pick is E-invariant in ALL 6 (panel x chooser) cells",
      f"{nconst}/6 cells constant; distinct picks "
      f"{sorted(gp['n_distinct_picks'].tolist())}", nconst == 6)
    rng_spy = float(BR[(BR.egrid == EGRID_HEAD)]["spy_OOS_Sharpe_range"].max())
    H("H_BAR", f"range(SPY OOS Sharpe over END_Q) <= {START_FULLTAPE_RANGE:.4f} "
                f"(1001's full-tape START figure)",
      f"{rng_spy:.4f} (worst panel)", rng_spy <= START_FULLTAPE_RANGE,
      f"1001's legal-start range was {START_LEGAL_RANGE:.4f}")
    rc = CC[(CC.set == "ALL") & (CC.bar == BAR_REF)].iloc[0]
    H("H_MONO", "the 4b pass count is monotone in E over END_Q",
      f"monotone={rc.monotone}, {rc.n_sign_changes} sign changes, count "
      f"{rc.pass_min}..{rc.pass_max}", bool(rc.monotone))
    H("H_LEG", ">= 0.90 of ALL books hold the same binding-leg set at every E",
      f"{rall.frac_legset_const:.4f} ({rall.n_legset_const}/{rall.n_books})",
      rall.frac_legset_const >= 0.90)
    H("H_COMP", "|Pearson(pass count, SPY OOS Sharpe)| > |Pearson(pass count, OOS years)|",
      f"|{rc.r_spy_OOS_Sharpe:+.4f}| vs |{rc.r_OOS_years:+.4f}|",
      abs(rc.r_spy_OOS_Sharpe) > abs(rc.r_OOS_years))
    HY = pd.DataFrame(hyp)
    P(f"\n  {int((HY.verdict == 'PASS').sum())} of {len(HY)} hypotheses PASS.")
    dump(HY, "hypotheses")

    P(f"\nRuntime {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {Path(f'{OUT}.console.txt').name}")


if __name__ == "__main__":
    main()
