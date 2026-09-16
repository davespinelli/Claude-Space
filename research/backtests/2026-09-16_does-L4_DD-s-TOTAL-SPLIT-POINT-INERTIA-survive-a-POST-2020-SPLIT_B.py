#!/usr/bin/env python3
"""Idea 1022 (lane B, 2026-09-16) — does `L4_DD`'s TOTAL SPLIT-POINT INERTIA survive a
POST-2020 SPLIT?

QUESTION (QUEUE idea 1022, verbatim)
    idea 1013 found SPY's |OOS MaxDD| range across all 16 legal ends is 0.0000 and `L4_DD` is
    constant on 45 of 45 books, because the 2020 crash sits inside EVERY legal OOS window on
    this tape.  That is a property of the window set, not of the leg.  Slide the split through
    2019-2022 so 2020 moves from the OOS side to the IS side and report what 4b's drawdown cap
    becomes when its one binding episode is no longer guaranteed.
    Max 2 params (end grid, panel).

WHAT IS NEW AGAINST 1013.  1013 slid the IS END across 2015Q1-2018Q4 with the start pinned,
    and measured `L4_DD` constant on 45 of 45 books with SPY's |OOS MaxDD| range 0.0000.  Both
    numbers are DEGENERATE BY CONSTRUCTION on that grid: every legal end there precedes
    2020-02-19, so the COVID crash is inside every OOS window and it is the deepest episode on
    this tape for SPY and for almost every book.  1022 slides the end THROUGH the episode
    (2019Q1-2022Q4), which is the only dial on this tape that can move the drawdown leg at all.
    Nothing else changes: the start stays pinned at the record's own `px.index[260]`, the books
    are the same 45, the cost rungs are the same.

WHY THE BAR CONVENTION IS THE WHOLE STORY.  4b's DD cap is `|book OOS MaxDD| <= 0.60 * BAR`.
    Two conventions are live in the record and BOTH are published here at every point:
      REC_FULL  BAR = SPY's FULL-sample |MaxDD| (the record's own; every committed row used
                it).  The bar is E-INVARIANT, so as the crash leaves the OOS window only the
                BOOK's side falls -> the leg gets EASIER.
      WIN       BAR = SPY's OWN OOS-window |MaxDD|.  Both sides fall -> whether the leg gets
                easier or harder is an empirical question, and it is the question 1022 asks.
    REC_FULL is the reference because it is what the record certified passes on.

WHAT IS MEASURED
    (A) THE CAP ITSELF.  SPY's |OOS MaxDD| and the implied 4b cap at every E on both panels,
        with the trough DATE of the binding episode, so the reader can see the cap step when
        the 2020 trough crosses the split.
    (B) THE LEG.  `L4_DD` per book per E under both conventions: constant / flips / direction,
        plus the leg's slack (cap minus |book OOS MaxDD|) as a continuous quantity.
    (C) THE VERDICT.  The full five-leg 4b verdict, the 4a verdict, and the binding-leg set at
        every point; how many books change verdict, and whether `L4_DD` becomes a binder.
    (D) RULE 8 (mandatory).  Three IS-only choosers x 2 panels x the end grid, picking from the
        never-memo-selected GRID pool, evaluated on the OOS window each E defines, reported as
        OOS CAGR / Sharpe / MaxDD against the LIVE baseline (RULES v2) and against SPY — and
        separately at PROTOCOL rule 8's own split 2016-12-31, which is the run's anchor.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported, none
selected.
    (1) END GRID in {END_Q, END_Y}
          END_Q  the 16 quarter-ends 2019-03-31 ... 2022-12-31                 <- HEADLINE
          END_Y  the 4 year-ends 2019-12-31 ... 2022-12-31                     <- coarse control
    (2) PANEL in {U56, B136}; both reported at every point, neither selected.  Each panel keeps
        its OWN calendar (B136's broad cache is Friday-refreshed and ends a few sessions
        earlier); every metric is within-panel, so no splice is needed and none is done.

    NOT TUNED, reported as CONTROLS at every point:
      BAR         {REC_FULL, WIN} as above; REC_FULL is the reference.
      COST        0 / 10 / 25 bps; PROTOCOL rule 2's 10 bps is the headline.
      CLAIM SET   SHELF (the record's committed memo-backed 4b passes, rebuilt from lane C's
                  own `shelf_books`) and GRID (the mechanical band x gross x QROLL ladder,
                  never memo-selected — the clean rule-8 selection pool).
      ANCHOR      PROTOCOL's own E = 2016-12-31 is carried through the whole ladder as a
                  reference row and is where the mandatory rule-8 walk-forward is reported.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_INERT   HEADLINE.  >= 0.90 of all books hold `L4_DD` at EVERY E in END_Q under REC_FULL.
              PASS => the leg's total inertia survives a post-2020 split and is a property of
              the LEG.  FAIL => 1013's 45-of-45 was a property of its WINDOW SET.
    H_INERT_W the same under the WIN convention.
    H_BAR     range(SPY |OOS MaxDD|) over END_Q >= 0.05 on at least one panel.  1013's figure
              on its own grid was 0.0000.  PASS => the cap's basis genuinely moves here.
    H_STEP    the LARGEST single-step move in SPY |OOS MaxDD| between consecutive ends is the
              step that first puts the 2020 trough on the IS side.  PASS => the cap is a
              SINGLE-EPISODE object, not a drifting one.
    H_CAPCUT  the WIN cap at the LAST end <= 0.80 x the WIN cap at the FIRST end (>= 20%
              tightening).  PASS => losing the episode TIGHTENS the cap under WIN.
    H_BIND    `L4_DD`'s share of binding-leg sets under WIN is >= 0.10 higher at post-crash
              ends than at pre-crash ends.  PASS => the leg starts DECIDING once its guaranteed
              episode is gone.
    H_VERDICT >= 0.90 of all books hold their 4b verdict at every E in END_Q under REC_FULL.
    H_PANEL   the two panels agree on the PASS/FAIL sign of H_INERT and H_VERDICT.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                   0.0
    G3  CROSS-RUN: at E = 2016-12-31 SPY's OOS triple == the record's committed 15.21% /
        0.8713 / -33.72% (idea 1009's G4, the standing comparand).
    G4  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G5  determinism: the whole E ladder rebuilt reproduces bit-for-bit.                   0.0
    G6  IS PURITY: every chooser's pick is invariant under a permutation of the OOS columns.
    G7  CROSS-RUN vs 1013: on the 2015Q1-2018Q4 grid this run reproduces 1013's two published
        degeneracies — SPY |OOS MaxDD| range 0.0000 and `L4_DD` constant on 45/45 books.
    G8  EPISODE IDENTITY: at every E before 2020-02-19 SPY's OOS trough date is the 2020 crash
        trough; at every E after it, it is not.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR
    LEVEL below is optimistic and every 4b pass count is an UPPER bound.  The measured object
    is the MOVEMENT of one leg as a single date slides over the SAME books and the SAME tape;
    the bias is a common factor across E and very largely cancels.  Where it does not cancel it
    works AGAINST this run's suspicion (survivor books are steadier), so measured instability
    is a LOWER bound and H_INERT is the EASIER hypothesis to pass.  SPY is a real index series.

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
SLUG = "does-L4_DD-s-TOTAL-SPLIT-POINT-INERTIA-survive-a-POST-2020-SPLIT"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
REC_END = "2016-12-31"                 # PROTOCOL rule 8's own split, the anchor
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
BARS = ["REC_FULL", "WIN"]
BAR_REF = "REC_FULL"
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
COVID_TROUGH = pd.Timestamp("2020-03-23")
COVID_PEAK = pd.Timestamp("2020-02-19")
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)   # idea 1009 G4, at E = REC_END
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
    "END_Q": quarter_ends("2019-01-01", "2022-12-31"),
    "END_Y": ["2019-12-31", "2020-12-31", "2021-12-31", "2022-12-31"],
}
EGRID_HEAD = "END_Q"
# 1013's own grid, re-run here only to reproduce its two published degeneracies (gate G7).
E1013 = quarter_ends("2015-01-01", "2018-12-31")


def dd_trough(r_idx, vals):
    """|MaxDD| and the DATE of its trough for a return path given as (index, values)."""
    if len(vals) < 2:
        return np.nan, pd.NaT
    eq = np.cumprod(1.0 + np.asarray(vals, float))
    dd = eq / np.maximum.accumulate(eq) - 1.0
    k = int(np.argmin(dd))
    return float(dd[k]), r_idx[k]


def metblock(r):
    """Full-sample CAGR/Sharpe/MaxDD plus the record's COUNT halves (`baseline._row`)."""
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def path_block(net, e):
    """Everything a verdict needs for one (path, E): full-sample halves plus the OOS window,
    plus the OOS drawdown's trough DATE, which is what idea 1022 is actually about."""
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):]
    i = net.loc[:pd.Timestamp(e)]
    oc, os_, od = fmet(o.values) if len(o) > 10 else (np.nan,) * 3
    ic, is_, idd = fmet(i.values) if len(i) > 10 else (np.nan,) * 3
    _, otr = dd_trough(o.index, o.values) if len(o) > 10 else (np.nan, pd.NaT)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o), OOS_trough=otr,
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, bspy, bar):
    """PROTOCOL 4b's five legs in the record's own wording; `bar` selects the DD/CAGR basis."""
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
    }, DDCAP_FRAC * dd_bar


def failstr(lg):
    f = [k for k in LEGS if not lg[k]]
    return "+".join(f) if f else "-"


def main():
    t0 = time.time()
    P(f"# Idea 1022 (lane B, {DATE}) — does L4_DD's TOTAL SPLIT-POINT INERTIA survive a "
      f"POST-2020 SPLIT?")
    P(f"# 2 tuned dials: END GRID {list(END_GRIDS)} x PANEL [U56, B136].  All points reported, "
      f"none selected.")
    P(f"# CONTROLS at every point: BAR {BARS} (ref {BAR_REF}), COST {RUNGS} bps "
      f"(head {RUNG_HEAD:.0f}), CLAIM SET [SHELF, GRID], ANCHOR E={REC_END}.")
    P(f"# START is PINNED at the record's own px.index[{WARMUP}]; only the SPLIT POINT moves, "
      f"and it now moves THROUGH the 2020 episode.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic and")
    P("#   the measured leg instability is a LOWER bound, i.e. H_INERT is the EASIER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")
    P(f"Fixed start (both panels): {REC['U56'].date()} / {REC['B136'].date()}.")

    shelf = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    shelf["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    grid = C.grid_books(U, B)
    SETS = {"SHELF": shelf, "GRID": grid}
    P(f"SHELF = {len(shelf)} committed memo-backed 4b passes; GRID = {len(grid)} "
      f"never-memo-selected ladder books ({len(shelf) + len(grid)} books, 1013's 45).")
    P(f"END grids: END_Q = {len(END_GRIDS['END_Q'])} quarter-ends {END_GRIDS['END_Q'][0]}.."
      f"{END_GRIDS['END_Q'][-1]} (headline, straddles the 2020 trough "
      f"{COVID_TROUGH.date()}); END_Y = {END_GRIDS['END_Y']}.")
    P("")

    # ---------------------------------------------------------------- net return paths
    NET = {}
    for sname, bset in SETS.items():
        for nm, b in bset.items():
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
            st = REC[b["panel"]]
            for c in RUNGS:
                NET[(sname, nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = (r - t * c / 1e4).loc[REC[p]:]

    ALLE = sorted(set(END_GRIDS["END_Q"]) | set(END_GRIDS["END_Y"]) | {REC_END} | set(E1013))
    SPYB = {(p, e): path_block(SPYR[p], e) for p in PX for e in ALLE}

    # ================================================================ GATES
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    def G(gid, what, value, ok):
        gates.append(dict(gate=gid, what=what, value=value, verdict="PASS" if ok else "FAIL"))
        P(f"{gid} {what}: {value}  {'PASS' if ok else 'FAIL'}")
        return ok

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    G("G1", "fast_run == engine.backtest (returns / turnover)", f"{d_r:.3e}/{d_t:.3e}",
      d_r < 1e-12 and d_t < 1e-10)

    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    G("G2", "rules_v2_weights(U,0.03,0.75) == baseline.rules_v2_weights(U)", f"{d2:.3e}",
      d2 == 0.0)

    sp = SPYB[("U56", REC_END)]
    trip = (sp["OOS_CAGR"], sp["OOS_Sharpe"], sp["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    G("G3", f"CROSS-RUN SPY OOS triple at E={REC_END} vs committed "
             f"{SPY_OOS_COMMITTED[0]:.2%}/{SPY_OOS_COMMITTED[1]:.4f}/{SPY_OOS_COMMITTED[2]:.2%}",
      f"{trip[0]:.4%}/{trip[1]:.4f}/{trip[2]:.4%} max|d| {d3:.3e}", d3 <= 5e-4)

    grows, ok4 = [], True
    for nm, b in shelf.items():
        c_, s_, d_ = fmet(NET[("SHELF", nm, RUNG_HEAD)].values)
        m = b["memo"]
        dc = abs(c_ - m[0]) if m[0] is not None else 0.0
        ds = abs(s_ - m[1]) if m[1] is not None else 0.0
        dv = abs(d_ - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dv <= 0.015
        ok4 &= good
        grows.append(dict(book=nm, panel=b["panel"], CAGR=c_, Sharpe=s_, MaxDD=d_,
                          memo_CAGR=m[0], memo_Sharpe=m[1], memo_MaxDD=m[2],
                          d_CAGR=dc, d_Sharpe=ds, d_MaxDD=dv,
                          verdict="PASS" if good else "FAIL", src=b["src"]))
    G("G4", "SHELF memo triples",
      f"{sum(r['verdict'] == 'PASS' for r in grows)}/{len(grows)}", ok4)
    dump(pd.DataFrame(grows), "shelf")

    # ---------------------------------------------------------------- THE LADDER
    def build_ladder(elist):
        rows = []
        for sname, bset in SETS.items():
            for nm, b in bset.items():
                p = b["panel"]
                for c in RUNGS:
                    net = NET[(sname, nm, c)]
                    v2b = metblock(V2[(p, c)].values)
                    for e in elist:
                        bk = path_block(net, e)
                        sb = SPYB[(p, e)]
                        row = dict(set=sname, book=nm, panel=p, freq=b["freq"], cost=c, E=e,
                                   OOS_years=bk["OOS_n"] / 252.0, IS_years=bk["IS_n"] / 252.0,
                                   crash_in_OOS=pd.Timestamp(e) < COVID_PEAK,
                                   **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                         "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
                                                         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")},
                                   OOS_trough=bk["OOS_trough"],
                                   spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                                   spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                   spy_OOS_trough=sb["OOS_trough"],
                                   spy_FULL_MaxDD=sb["MaxDD"], spy_FULL_CAGR=sb["CAGR"])
                        for bar in BARS:
                            lg, cap = legs_at(bk, sb, bar)
                            row[f"pass4b_{bar}"] = all(lg.values())
                            row[f"fail4b_{bar}"] = failstr(lg)
                            row[f"cap_{bar}"] = cap
                            row[f"ddslack_{bar}"] = cap - abs(bk["OOS_MaxDD"])
                            for k in LEGS:
                                row[f"{k}_{bar}"] = lg[k]
                        row["pass4a"] = (bk["H1"] > v2b["H1"] and bk["H2"] > v2b["H2"]
                                         and bk["MaxDD"] >= v2b["MaxDD"])
                        rows.append(row)
        return pd.DataFrame(rows)

    L = build_ladder(sorted(set(END_GRIDS["END_Q"]) | set(END_GRIDS["END_Y"]) | {REC_END}))
    L2 = build_ladder(sorted(set(END_GRIDS["END_Q"]) | set(END_GRIDS["END_Y"]) | {REC_END}))
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    G("G5", f"determinism over the whole {len(L):,}-row ladder", f"{d5:.3e}", d5 == 0.0)

    # G7 — reproduce 1013's two published degeneracies on ITS grid
    L13 = build_ladder(E1013)
    r13 = max(float(np.ptp([abs(SPYB[(p, e)]["OOS_MaxDD"]) for e in E1013])) for p in PX)
    sub13 = L13[L13.cost == RUNG_HEAD]
    g13 = sub13.groupby("book")["L4_DD_REC_FULL"].nunique()
    n13 = int((g13 == 1).sum())
    G("G7", f"CROSS-RUN vs 1013 on ITS grid {E1013[0]}..{E1013[-1]}: SPY |OOS MaxDD| range "
             f"(bar 0.0000) and L4_DD constant (bar {len(g13)}/{len(g13)})",
      f"range {r13:.4e}; L4_DD constant {n13}/{len(g13)}", r13 <= 1e-9 and n13 == len(g13))

    # G8 — episode identity
    bad8 = 0
    for p in PX:
        for e in END_GRIDS["END_Q"]:
            tr = SPYB[(p, e)]["OOS_trough"]
            pre = pd.Timestamp(e) < COVID_PEAK
            is_covid = (pd.Timestamp("2020-03-01") <= tr <= pd.Timestamp("2020-04-15"))
            if pre != is_covid:
                bad8 += 1
    G("G8", "EPISODE IDENTITY: SPY's OOS trough is the 2020 crash iff E precedes the crash",
      f"{bad8} disagreeing (panel, E) cells", bad8 == 0)

    # ---------------------------------------------------------------- rule-8 picks
    SPYIS = {}
    for p in PX:
        for e in sorted(set(L.E)):
            c_, s_, d_ = fmet(SPYR[p].loc[:pd.Timestamp(e)].values)
            SPYIS[(p, e)] = (c_, s_, d_)
    L["spy_IS_CAGR"] = [SPYIS[(r.panel, r.E)][0] for r in L.itertuples()]
    L["spy_IS_Sharpe"] = [SPYIS[(r.panel, r.E)][1] for r in L.itertuples()]
    L["spy_IS_MaxDD"] = [SPYIS[(r.panel, r.E)][2] for r in L.itertuples()]

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

    picks = []
    for pool in ("GRID", "ALL"):
        sel = L if pool == "ALL" else L[L.set == "GRID"]
        for p in PX:
            for e in sorted(set(L.E)):
                sub = sel[(sel.panel == p) & (sel.E == e) & (sel.cost == RUNG_HEAD)]
                v2b = metblock(V2[(p, RUNG_HEAD)].values)
                v2o = path_block(V2[(p, RUNG_HEAD)], e)
                sb = SPYB[(p, e)]
                for ch in CHOOSERS:
                    r = choose(sub, ch)
                    if r is None:
                        continue
                    picks.append(dict(pool=pool, panel=p, E=e, chooser=ch, pick=r["book"],
                                      set=r["set"], freq=r["freq"],
                                      crash_in_OOS=bool(r["crash_in_OOS"]),
                                      IS_Sharpe=r["IS_Sharpe"], IS_CAGR=r["IS_CAGR"],
                                      OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                                      OOS_MaxDD=r["OOS_MaxDD"],
                                      L4_DD=r["L4_DD_REC_FULL"], L4_DD_WIN=r["L4_DD_WIN"],
                                      pass4b=r["pass4b_REC_FULL"], fail4b=r["fail4b_REC_FULL"],
                                      pass4b_WIN=r["pass4b_WIN"], pass4a=r["pass4a"],
                                      spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                      spy_OOS_MaxDD=sb["OOS_MaxDD"], spy_CAGR=sb["CAGR"],
                                      spy_Sharpe=sb["Sharpe"], spy_MaxDD=sb["MaxDD"],
                                      v2_OOS_CAGR=v2o["OOS_CAGR"], v2_OOS_Sharpe=v2o["OOS_Sharpe"],
                                      v2_OOS_MaxDD=v2o["OOS_MaxDD"], v2_Sharpe=v2b["Sharpe"],
                                      v2_MaxDD=v2b["MaxDD"]))
    K = pd.DataFrame(picks)

    rng = np.random.default_rng(1022)
    bad6 = 0
    for p in PX:
        sub = L[(L.panel == p) & (L.E == REC_END) & (L.cost == RUNG_HEAD)
                & (L.set == "GRID")].copy()
        perm = sub.copy()
        for col in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"):
            perm[col] = rng.permutation(perm[col].values)
        for ch in CHOOSERS:
            if choose(sub, ch)["book"] != choose(perm, ch)["book"]:
                bad6 += 1
    G("G6", "IS purity (picks invariant under permuted OOS columns)", f"{bad6} disagreements",
      bad6 == 0)

    ng = sum(g["verdict"] == "PASS" for g in gates)
    P(f"\nGATES {ng} of {len(gates)} PASS.\n")
    dump(pd.DataFrame(gates), "gates")

    HQ = END_GRIDS[EGRID_HEAD]

    # ================================================================ (A) THE CAP
    P("## A. THE CAP ITSELF — SPY's |OOS MaxDD| and 4b's implied cap as the split crosses 2020")
    crows = []
    for p in PX:
        for e in HQ:
            sb = SPYB[(p, e)]
            crows.append(dict(panel=p, E=e, crash_in_OOS=pd.Timestamp(e) < COVID_PEAK,
                              OOS_years=sb["OOS_n"] / 252.0,
                              spy_OOS_MaxDD=sb["OOS_MaxDD"],
                              spy_OOS_trough=sb["OOS_trough"],
                              spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                              cap_WIN=DDCAP_FRAC * abs(sb["OOS_MaxDD"]),
                              cap_REC_FULL=DDCAP_FRAC * abs(sb["MaxDD"])))
    CAP = pd.DataFrame(crows)
    for p in PX:
        s = CAP[CAP.panel == p]
        P(f"  {p}:  E        OOSyrs  SPY|OOS DD|  trough       cap_WIN   cap_REC_FULL")
        for _, r in s.iterrows():
            P(f"        {r.E}  {r.OOS_years:5.2f}   {abs(r.spy_OOS_MaxDD):9.4f}  "
              f"{str(r.spy_OOS_trough)[:10]}   {r.cap_WIN:7.4f}   {r.cap_REC_FULL:7.4f}"
              f"{'   <- crash still in OOS' if r.crash_in_OOS else ''}")
        v = np.abs(s.spy_OOS_MaxDD.values)
        P(f"     RANGE of SPY |OOS MaxDD| over the {len(s)} ends: {v.max() - v.min():.4f} "
          f"({v.min():.4f}..{v.max():.4f})   1013's figure on its own grid: 0.0000")
        d = np.abs(np.diff(v))
        kk = int(np.argmax(d))
        P(f"     LARGEST single step: {s.E.iloc[kk]} -> {s.E.iloc[kk + 1]}  |d| {d[kk]:.4f} "
          f"(next largest {np.sort(d)[-2]:.4f})")
    dump(CAP, "cap")

    # ================================================================ (B) THE LEG
    P("\n## B. THE LEG — is `L4_DD` still constant when the episode can leave?")
    lrows = []
    for egrid, EL in END_GRIDS.items():
        for bar in BARS:
            for c in RUNGS:
                for p in list(PX) + ["BOTH"]:
                    sub = L[(L.cost == c) & (L.E.isin(EL))]
                    if p != "BOTH":
                        sub = sub[sub.panel == p]
                    for sname in ("SHELF", "GRID", "ALL"):
                        s = sub if sname == "ALL" else sub[sub.set == sname]
                        if s.empty:
                            continue
                        g = s.groupby("book")[f"L4_DD_{bar}"]
                        nb = g.ngroups
                        const = int((g.nunique() == 1).sum())
                        ever = int(g.max().sum())
                        always = int(g.min().sum())
                        lrows.append(dict(egrid=egrid, bar=bar, cost=c, panel=p, set=sname,
                                          n_books=nb, n_L4_const=const, frac_L4_const=const / nb,
                                          n_L4_ever=ever, n_L4_always=always,
                                          mean_slack=float(s[f"ddslack_{bar}"].mean()),
                                          slack_range=float(
                                              s.groupby("book")[f"ddslack_{bar}"]
                                              .apply(lambda x: x.max() - x.min()).mean())))
    LEGT = pd.DataFrame(lrows)
    for bar in BARS:
        r = LEGT[(LEGT.egrid == EGRID_HEAD) & (LEGT.bar == bar) & (LEGT.cost == RUNG_HEAD)
                 & (LEGT.panel == "BOTH") & (LEGT.set == "ALL")].iloc[0]
        P(f"  {bar:8s} (END_Q, {RUNG_HEAD:.0f} bps, all {r.n_books} books): L4_DD CONSTANT on "
          f"{r.n_L4_const}/{r.n_books} ({r.frac_L4_const:.4f})   holds at SOME E "
          f"{r.n_L4_ever}   at EVERY E {r.n_L4_always}")
        P(f"           mean leg slack {r.mean_slack:+.4f}; mean per-book slack RANGE over the "
          f"16 ends {r.slack_range:.4f}")
    for p in PX:
        for bar in BARS:
            r = LEGT[(LEGT.egrid == EGRID_HEAD) & (LEGT.bar == bar) & (LEGT.cost == RUNG_HEAD)
                     & (LEGT.panel == p) & (LEGT.set == "ALL")].iloc[0]
            P(f"    panel {p:5s} {bar:8s}: L4_DD constant {r.n_L4_const}/{r.n_books} "
              f"({r.frac_L4_const:.4f}), ever {r.n_L4_ever}, always {r.n_L4_always}")
    P("  Per-book L4_DD sequence over the 16 ends (10 bps, D = leg HOLDS, . = leg FAILS), "
      "REC_FULL | WIN:")
    seqrows = []
    for nm, g in L[(L.cost == RUNG_HEAD) & (L.E.isin(HQ))].groupby("book"):
        g = g.sort_values("E")
        s1 = "".join("D" if v else "." for v in g["L4_DD_REC_FULL"])
        s2 = "".join("D" if v else "." for v in g["L4_DD_WIN"])
        seqrows.append(dict(book=nm, panel=g.panel.iloc[0], set=g["set"].iloc[0],
                            seq_REC_FULL=s1, seq_WIN=s2,
                            n_REC_FULL=int(g["L4_DD_REC_FULL"].sum()),
                            n_WIN=int(g["L4_DD_WIN"].sum()),
                            ddslack_WIN_range=float(g["ddslack_WIN"].max()
                                                    - g["ddslack_WIN"].min()),
                            OOS_MaxDD_range=float(g["OOS_MaxDD"].max() - g["OOS_MaxDD"].min())))
        P(f"    {nm:34s} {s1} | {s2}")
    dump(pd.DataFrame(seqrows), "legseq")
    dump(LEGT, "legstability")

    # ================================================================ (C) THE VERDICT
    P("\n## C. THE VERDICT — 4b, 4a and the binding-leg set across the same ends")
    vrows = []
    for egrid, EL in END_GRIDS.items():
        for bar in BARS:
            for c in RUNGS:
                for p in list(PX) + ["BOTH"]:
                    sub = L[(L.cost == c) & (L.E.isin(EL))]
                    if p != "BOTH":
                        sub = sub[sub.panel == p]
                    for sname in ("SHELF", "GRID", "ALL"):
                        s = sub if sname == "ALL" else sub[sub.set == sname]
                        if s.empty:
                            continue
                        g = s.groupby("book")[f"pass4b_{bar}"]
                        nb = g.ngroups
                        lg = s.groupby("book")[f"fail4b_{bar}"].nunique()
                        binds = s[f"fail4b_{bar}"].str.contains("L4_DD")
                        pre = s[s.crash_in_OOS][f"fail4b_{bar}"].str.contains("L4_DD")
                        post = s[~s.crash_in_OOS][f"fail4b_{bar}"].str.contains("L4_DD")
                        vrows.append(dict(egrid=egrid, bar=bar, cost=c, panel=p, set=sname,
                                          n_books=nb, n_verdict_const=int((g.nunique() == 1).sum()),
                                          frac_const=float((g.nunique() == 1).mean()),
                                          n_legset_const=int((lg == 1).sum()),
                                          frac_legset_const=float((lg == 1).mean()),
                                          n_pass_ever=int(g.max().sum()),
                                          n_pass_always=int(g.min().sum()),
                                          pass_rate=float(s[f"pass4b_{bar}"].mean()),
                                          pass4a_rate=float(s["pass4a"].mean()),
                                          L4_bind_share=float(binds.mean()),
                                          L4_bind_pre=float(pre.mean()) if len(pre) else np.nan,
                                          L4_bind_post=float(post.mean()) if len(post) else np.nan))
    V = pd.DataFrame(vrows)
    for bar in BARS:
        r = V[(V.egrid == EGRID_HEAD) & (V.bar == bar) & (V.cost == RUNG_HEAD)
              & (V.panel == "BOTH") & (V['set'] == "ALL")].iloc[0]
        P(f"  {bar:8s}: 4b verdict CONSTANT on {r.n_verdict_const}/{r.n_books} books "
          f"({r.frac_const:.4f})   binding-leg-set constant {r.n_legset_const}/{r.n_books} "
          f"({r.frac_legset_const:.4f})")
        P(f"           4b pass rate over all (book x E) {r.pass_rate:.4f}; passes at SOME E "
          f"{r.n_pass_ever}, at EVERY E {r.n_pass_always};  4a rate {r.pass4a_rate:.4f}")
        P(f"           L4_DD in the binding set: overall {r.L4_bind_share:.4f}  |  crash IN OOS "
          f"{r.L4_bind_pre:.4f}  ->  crash OUT of OOS {r.L4_bind_post:.4f}")
    P("  4b pass count by end date (ALL books, 10 bps, REC_FULL | WIN):")
    for bar in BARS:
        cnt = (L[(L.cost == RUNG_HEAD) & (L.E.isin(HQ))].groupby("E")[f"pass4b_{bar}"]
               .sum().reindex(HQ))
        P(f"    {bar:8s} " + "  ".join(f"{e[2:7]}:{v}" for e, v in cnt.items()))
    P(f"  SHELF (the record's committed passes) at E={REC_END} vs the post-2020 ends "
      f"(REC_FULL, 10 bps):")
    sh = L[(L.set == "SHELF") & (L.cost == RUNG_HEAD)]
    shrows = []
    for nm, g in sh.groupby("book"):
        gq = g[g.E.isin(HQ)].sort_values("E")
        at_rec = bool(g[g.E == REC_END]["pass4b_REC_FULL"].iloc[0])
        shrows.append(dict(book=nm, panel=g.panel.iloc[0], pass_at_REC=at_rec,
                           n_pass=int(gq["pass4b_REC_FULL"].sum()), n_E=len(gq),
                           n_pass_WIN=int(gq["pass4b_WIN"].sum()),
                           seq="".join("P" if v else "." for v in gq["pass4b_REC_FULL"]),
                           seq_WIN="".join("P" if v else "." for v in gq["pass4b_WIN"]),
                           legsets="|".join(sorted(gq["fail4b_REC_FULL"].unique()))))
        P(f"    {nm:34s} {'PASS' if at_rec else 'FAIL'}@{REC_END}  4b at "
          f"{int(gq['pass4b_REC_FULL'].sum()):2d}/{len(gq)} post-2020 ends "
          f"(WIN {int(gq['pass4b_WIN'].sum()):2d}/{len(gq)})   leg sets "
          f"{sorted(gq['fail4b_REC_FULL'].unique())}")
    dump(pd.DataFrame(shrows), "shelfladder")
    dump(V, "verdictstability")
    dump(L, "ladder", gz=True)

    # ================================================================ (D) RULE 8
    P("\n## D. RULE 8 — the mandatory walk-forward, and the picks as the split crosses 2020")
    P(f"  Selection pool = GRID ({len(grid)} never-memo-selected books); ALL (GRID+SHELF) is a "
      f"CONTAMINATED control.")
    P(f"\n  THE MANDATORY RULE-8 WALK-FORWARD at PROTOCOL's own split E = {REC_END} "
      f"(params chosen on IS only, OOS 2017-2026 untouched; pool GRID, 10 bps):")
    P(f"    {'panel':6s} {'chooser':10s} {'pick':30s} {'OOS CAGR':>9s} {'OOS Sh':>7s} "
      f"{'OOS DD':>8s}  4b 4a  binding legs")
    for _, r in K[(K.pool == "GRID") & (K.E == REC_END)].iterrows():
        P(f"    {r.panel:6s} {r.chooser:10s} {r['pick']:30s} {r.OOS_CAGR:8.2%} "
          f"{r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%}   {'Y' if r.pass4b else 'n'}  "
          f"{'Y' if r.pass4a else 'n'}   [{r.fail4b}]")
    for p in PX:
        sb = SPYB[(p, REC_END)]
        v2o = path_block(V2[(p, RUNG_HEAD)], REC_END)
        v2f = metblock(V2[(p, RUNG_HEAD)].values)
        P(f"    {p:6s} {'SPY':10s} {'(comparand)':30s} {sb['OOS_CAGR']:8.2%} "
          f"{sb['OOS_Sharpe']:7.3f} {sb['OOS_MaxDD']:8.2%}   full Sharpe {sb['Sharpe']:.3f} / "
          f"DD {sb['MaxDD']:.2%}")
        P(f"    {p:6s} {'RULESv2':10s} {'(live baseline)':30s} {v2o['OOS_CAGR']:8.2%} "
          f"{v2o['OOS_Sharpe']:7.3f} {v2o['OOS_MaxDD']:8.2%}   full Sharpe {v2f['Sharpe']:.3f} / "
          f"DD {v2f['MaxDD']:.2%}")
    dump(K[(K.pool == "GRID") & (K.E == REC_END)], "walkforward")

    P("\n  The same picks with the split slid THROUGH 2020 (pool GRID, 10 bps) — note the OOS "
      "window is short and shrinking, which is exactly what makes these splits illegal for a\n"
      "  KEEP and legal only as a sensitivity probe:")
    prows = []
    for (p, ch), g in K[(K.pool == "GRID") & (K.E.isin(HQ))].groupby(["panel", "chooser"]):
        g = g.sort_values("E")
        prows.append(dict(panel=p, chooser=ch, n_E=len(g), n_distinct_picks=int(g["pick"].nunique()),
                          modal_pick=g["pick"].mode().iloc[0],
                          modal_share=float((g["pick"] == g["pick"].mode().iloc[0]).mean()),
                          pick_at_REC=K[(K.pool == "GRID") & (K.panel == p) & (K.chooser == ch)
                                        & (K.E == REC_END)]["pick"].iloc[0],
                          OOS_Sharpe_min=float(g.OOS_Sharpe.min()),
                          OOS_Sharpe_max=float(g.OOS_Sharpe.max()),
                          OOS_CAGR_min=float(g.OOS_CAGR.min()), OOS_CAGR_max=float(g.OOS_CAGR.max()),
                          OOS_MaxDD_min=float(g.OOS_MaxDD.min()),
                          OOS_MaxDD_max=float(g.OOS_MaxDD.max()),
                          n_4b=int(g.pass4b.sum()), n_4b_WIN=int(g.pass4b_WIN.sum()),
                          n_4a=int(g.pass4a.sum()), n_L4=int(g.L4_DD.sum()),
                          n_L4_WIN=int(g.L4_DD_WIN.sum())))
        P(f"    {p:5s} {ch:10s} {g['pick'].nunique()} distinct pick(s) (modal {g['pick'].mode().iloc[0]} "
          f"{(g['pick'] == g['pick'].mode().iloc[0]).mean():.2f})  OOS Sharpe "
          f"{g.OOS_Sharpe.min():.3f}..{g.OOS_Sharpe.max():.3f}  OOS DD "
          f"{g.OOS_MaxDD.min():.2%}..{g.OOS_MaxDD.max():.2%}  4b {int(g.pass4b.sum())}/{len(g)} "
          f"(WIN {int(g.pass4b_WIN.sum())})  L4_DD {int(g.L4_DD.sum())}/{len(g)} "
          f"(WIN {int(g.L4_DD_WIN.sum())})")
    dump(pd.DataFrame(prows), "pickstability")
    dump(K, "picks")

    # KEEP paths, both, over the whole ladder
    P("\n  BOTH KEEP PATHS over the 10 bps ladder (PROTOCOL rule 4):")
    l10 = L[L.cost == RUNG_HEAD]
    P(f"    4a (beat the live book in BOTH halves, MaxDD no worse): "
      f"{int(l10['pass4a'].sum())} of {len(l10):,} (book x E) rows; "
      f"{int(l10.groupby('book')['pass4a'].min().sum())} books pass at EVERY end.")
    for bar in BARS:
        q = l10[l10.E.isin(HQ)]
        P(f"    4b [{bar}] over the post-2020 ends: {int(q[f'pass4b_{bar}'].sum())} of {len(q):,} "
          f"rows; at E={REC_END}: "
          f"{int(l10[l10.E == REC_END][f'pass4b_{bar}'].sum())} of "
          f"{len(l10[l10.E == REC_END])} books.")
    P("    NO new KEEP is claimed by this run: it prices an EXISTING protocol leg, it does not "
      "propose a book.")

    # ================================================================ (E) MECHANISM
    P("\n## E. MECHANISM — WHICH leg the post-2020 split actually moves, and in WHICH direction")
    mrows = []
    for bar in BARS:
        for c in RUNGS:
            sub = L[(L.cost == c) & (L.E.isin(HQ))]
            for k in LEGS:
                g = sub.groupby("book")[f"{k}_{bar}"]
                up = dn = 0
                for nm, gg in sub.sort_values("E").groupby("book"):
                    v = gg[f"{k}_{bar}"].values
                    if v[0] != v[-1]:
                        up += int(bool(v[-1]) and not bool(v[0]))
                        dn += int(bool(v[0]) and not bool(v[-1]))
                bind = sub[f"fail4b_{bar}"].str.contains(k)
                pre = sub[sub.crash_in_OOS][f"fail4b_{bar}"].str.contains(k)
                post = sub[~sub.crash_in_OOS][f"fail4b_{bar}"].str.contains(k)
                sole = (sub[f"fail4b_{bar}"] == k)
                mrows.append(dict(bar=bar, cost=c, leg=k, n_books=g.ngroups,
                                  n_const=int((g.nunique() == 1).sum()),
                                  frac_const=float((g.nunique() == 1).mean()),
                                  n_first_to_last_EASIER=up, n_first_to_last_HARDER=dn,
                                  leg_pass_rate=float(sub[f"{k}_{bar}"].mean()),
                                  bind_share=float(bind.mean()),
                                  bind_pre=float(pre.mean()) if len(pre) else np.nan,
                                  bind_post=float(post.mean()) if len(post) else np.nan,
                                  sole_binder=float(sole.mean())))
    M = pd.DataFrame(mrows)
    for bar in BARS:
        P(f"  {bar} (END_Q, {RUNG_HEAD:.0f} bps, 45 books):")
        P(f"    {'leg':8s} {'const':>7s} {'pass':>7s} {'binds':>7s} {'pre':>7s} {'post':>7s} "
          f"{'sole':>7s}  first->last flips (easier/harder)")
        for _, r in M[(M.bar == bar) & (M.cost == RUNG_HEAD)].iterrows():
            P(f"    {r.leg:8s} {r.frac_const:7.4f} {r.leg_pass_rate:7.4f} {r.bind_share:7.4f} "
              f"{r.bind_pre:7.4f} {r.bind_post:7.4f} {r.sole_binder:7.4f}   "
              f"{r.n_first_to_last_EASIER}/{r.n_first_to_last_HARDER}")
    P("  L1_H1 / L2_H2 are E-INVARIANT BY CONSTRUCTION: the record's halves are a COUNT split of")
    P("    the FULL post-warm-up path (`baseline._row`), which the split point never touches.")
    dump(M, "legmechanism")

    # ================================================================ HYPOTHESES
    P("\n## HYPOTHESES (bars declared in the header, before any number above was read)")
    hyp = []

    def H(name, bar, val, ok, note=""):
        hyp.append(dict(name=name, bar=bar, value=val, verdict="PASS" if ok else "FAIL", note=note))
        P(f"  {name:10s} {'PASS' if ok else 'FAIL'}   bar: {bar}")
        P(f"             got: {val}{('   ' + note) if note else ''}")

    def cell(bar, panel="BOTH", sset="ALL", tab=None):
        t = LEGT if tab is None else tab
        return t[(t.egrid == EGRID_HEAD) & (t.bar == bar) & (t.cost == RUNG_HEAD)
                 & (t.panel == panel) & (t['set'] == sset)].iloc[0]

    r_rec, r_win = cell(BAR_REF), cell("WIN")
    H("H_INERT", ">= 0.90 of all books hold L4_DD at EVERY E in END_Q (REC_FULL)",
      f"{r_rec.frac_L4_const:.4f} ({r_rec.n_L4_const}/{r_rec.n_books})",
      r_rec.frac_L4_const >= 0.90,
      "HEADLINE — 1013 measured 45/45 = 1.0000 on the 2015-2018 grid")
    H("H_INERT_W", ">= 0.90 of all books hold L4_DD at EVERY E in END_Q (WIN)",
      f"{r_win.frac_L4_const:.4f} ({r_win.n_L4_const}/{r_win.n_books})",
      r_win.frac_L4_const >= 0.90)
    rngs = {p: float(np.ptp(np.abs(CAP[CAP.panel == p].spy_OOS_MaxDD.values))) for p in PX}
    H("H_BAR", "range(SPY |OOS MaxDD|) over END_Q >= 0.05 on at least one panel",
      "; ".join(f"{p} {v:.4f}" for p, v in rngs.items()), max(rngs.values()) >= 0.05,
      "1013's figure on its own grid: 0.0000")
    stepok, stepnote = True, []
    for p in PX:
        s = CAP[CAP.panel == p].sort_values("E")
        v = np.abs(s.spy_OOS_MaxDD.values)
        d = np.abs(np.diff(v))
        kk = int(np.argmax(d))
        e_lo, e_hi = s.E.iloc[kk], s.E.iloc[kk + 1]
        good = pd.Timestamp(e_lo) < COVID_PEAK <= pd.Timestamp(e_hi)
        stepok &= good
        stepnote.append(f"{p} {e_lo}->{e_hi} |d|={d[kk]:.4f}")
    H("H_STEP", "the largest single step in SPY |OOS MaxDD| is the one that first puts the "
                "2020 trough IS, on both panels", "; ".join(stepnote), stepok)
    capcut, capnote = True, []
    for p in PX:
        s = CAP[CAP.panel == p].sort_values("E")
        a, b_ = s.cap_WIN.iloc[0], s.cap_WIN.iloc[-1]
        capcut &= (b_ <= 0.80 * a)
        capnote.append(f"{p} {a:.4f} -> {b_:.4f} ({b_ / a:.3f}x)")
    H("H_CAPCUT", "the WIN cap at the LAST end <= 0.80 x the WIN cap at the FIRST end",
      "; ".join(capnote), capcut)
    rv_win = V[(V.egrid == EGRID_HEAD) & (V.bar == "WIN") & (V.cost == RUNG_HEAD)
               & (V.panel == "BOTH") & (V['set'] == "ALL")].iloc[0]
    H("H_BIND", "L4_DD's share of binding-leg sets (WIN) is >= 0.10 higher once the crash "
                "leaves the OOS window",
      f"pre {rv_win.L4_bind_pre:.4f} -> post {rv_win.L4_bind_post:.4f} "
      f"(d {rv_win.L4_bind_post - rv_win.L4_bind_pre:+.4f})",
      (rv_win.L4_bind_post - rv_win.L4_bind_pre) >= 0.10)
    rv_rec = V[(V.egrid == EGRID_HEAD) & (V.bar == BAR_REF) & (V.cost == RUNG_HEAD)
               & (V.panel == "BOTH") & (V['set'] == "ALL")].iloc[0]
    H("H_VERDICT", ">= 0.90 of all books hold their 4b verdict at every E in END_Q (REC_FULL)",
      f"{rv_rec.frac_const:.4f} ({rv_rec.n_verdict_const}/{rv_rec.n_books})",
      rv_rec.frac_const >= 0.90)
    pan = {}
    for p in PX:
        li = cell(BAR_REF, panel=p)
        vi = V[(V.egrid == EGRID_HEAD) & (V.bar == BAR_REF) & (V.cost == RUNG_HEAD)
               & (V.panel == p) & (V['set'] == "ALL")].iloc[0]
        pan[p] = (li.frac_L4_const >= 0.90, vi.frac_const >= 0.90)
    agree = len(set(pan.values())) == 1
    H("H_PANEL", "the two panels agree on the PASS/FAIL sign of H_INERT and H_VERDICT",
      "; ".join(f"{p} (inert={a}, verdict={b})" for p, (a, b) in pan.items()), agree)
    HY = pd.DataFrame(hyp)
    P(f"\n  {int((HY.verdict == 'PASS').sum())} of {len(HY)} hypotheses PASS.")
    dump(HY, "hypotheses")

    # ---------------------------------------------------------------- grid-point dump
    P("\n## ALL GRID POINTS (the 2 tuned dials, every combination, none selected)")
    P(f"  {'egrid':6s} {'panel':6s} {'bar':9s} {'cost':>5s}  L4 const   4b const   4b rate   "
      f"L4 bind")
    gp = []
    for egrid in END_GRIDS:
        for p in list(PX) + ["BOTH"]:
            for bar in BARS:
                for c in RUNGS:
                    a = LEGT[(LEGT.egrid == egrid) & (LEGT.bar == bar) & (LEGT.cost == c)
                             & (LEGT.panel == p) & (LEGT['set'] == "ALL")]
                    b_ = V[(V.egrid == egrid) & (V.bar == bar) & (V.cost == c)
                           & (V.panel == p) & (V['set'] == "ALL")]
                    if a.empty or b_.empty:
                        continue
                    a, b_ = a.iloc[0], b_.iloc[0]
                    gp.append(dict(egrid=egrid, panel=p, bar=bar, cost=c,
                                   frac_L4_const=a.frac_L4_const, frac_4b_const=b_.frac_const,
                                   pass4b_rate=b_.pass_rate, L4_bind_share=b_.L4_bind_share))
                    P(f"  {egrid:6s} {p:6s} {bar:9s} {c:5.1f}  {a.frac_L4_const:8.4f}  "
                      f"{b_.frac_const:8.4f}  {b_.pass_rate:8.4f}  {b_.L4_bind_share:8.4f}")
    dump(pd.DataFrame(gp), "gridpoints")

    P(f"\nRuntime {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {Path(f'{OUT}.console.txt').name}")


if __name__ == "__main__":
    main()
