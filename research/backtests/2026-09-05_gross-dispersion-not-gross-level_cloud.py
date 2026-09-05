#!/usr/bin/env python3
"""IDEA 143 — gross-DISPERSION, not gross LEVEL, as 4b's exposure-adequacy bar.  (cloud, 2026-09-05)

PRE-REGISTERED QUESTION (from QUEUE, written before any number here was read)
    Idea 131 KILLED the mean-gross bar: no gamma both (i) admits the 27 arm-rows the CAGR floor
    throws away and (ii) empties the 342-row static-gross ladder, because the two families
    OVERLAP on the gross LEVEL axis ([0.519,0.750] vs [0.075,0.673]).  It then noticed,
    POST HOC and explicitly refusing to adopt it, that cv(daily gross) nearly separates them:
    victims mean 0.268 (max 0.335) vs ladder mean 0.014 (max 0.022), 25 of 27 victims and
    11 of 11 Pareto-best above EVERY ladder point, the 2 exceptions being `-rw` full-gross
    REBUILDS that never de-gross.

    This run pre-registers that bar and asks the three questions idea 131 was not allowed to:
      Q1  Sweep kappa (a MINIMUM cv-of-daily-gross bar) on the SAME 306-row corpus and the SAME
          342-row ladder.  Report the whole separation frontier, ALL grid points.
      Q2  Does ANY kappa do BOTH jobs (all 27 victims admitted AND 0 ladder points admitted)?
          The gross LEVEL bar managed 0 of 34 grid points.
      Q3  Does it survive rule 8?  kappa re-chosen on the IS window ONLY (2009-2016), the pick
          read once on 2017-2026, against the published CAGR floor, the gross-level bar, and
          no adequacy bar at all.

TUNED PARAMETERS: ONE — kappa, the cv bar.  delta (DD cap 0.60), phi (CAGR floor 0.70) and
gamma (gross level 0.50) are all HELD at their published/idea-131 values and are never searched.
Every kappa grid point is printed.

HARNESS: idea 94's simulator and idea 131's corpus builder are IMPORTED, not re-implemented.
Idea 131's 306 arm-rows and 342 ladder rows are reproduced column-by-column against the
committed CSVs before any new number is read (reproduction gate below).

WHAT IS NEW HERE: cv(daily gross) computed on THREE windows (full / IS / OOS) for every arm row
AND every ladder row.  Idea 131 only carried the full-sample cv, which cannot answer Q3.

CAVEATS carried forward, stated not buried:
  - SURVIVORSHIP (idea 54): all three panels are current-constituent lists.  The small panel
    (data/prices_small.csv) is sub-$2B names screened TODAY and back-filled to 2010; tickers with
    max_1d_move >= 1.0 in data/small_meta.csv are dropped first (idea 118).  Delisted and
    acquired names are absent, which inflates CAGR most for ungated high-gross books.  The
    separation result is a statement about the DISPERSION OF GROSS, not about returns, so it is
    structurally insensitive to this; the rule-8 OOS numbers are not.
  - Idea 128: the IS window's SPY MaxDD is shallower than the full sample's, so every IS
    drawdown cap admits too much.  This biases all four selectors identically.
  - Idea 38: u56/broad still carry the calendar-day index.
  - Idea 126: t+1 execution only, no lag band.
  - cv is measured on the SAME window the bar is applied to (full for the adoption question,
    IS-only for the rule-8 screen).  Like mean gross and unlike a CAGR floor, it is directly
    observable prospectively -- that is the whole reason the bar is worth testing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_gross-dispersion-not-gross-level_cloud"
OUT = ROOT / "research" / "backtests"
I131 = OUT / "2026-09-05_gross-as-the-missing-third-bar_B.py"

_spec = importlib.util.spec_from_file_location("i131", I131)
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)          # main() is __main__-guarded; this only defines
H = J.H                              # idea 94's simulator, via idea 131

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS, LADDER, PANELS = H.BOOKS, H.LADDER, J.PANELS
PHI0, DELTA0, GAMMA0 = J.PHI0, J.DELTA0, J.GAMMA0

# tuned parameter 1 (the only one): the cv bar.  Fine grid, every point reported.
KAPPAS = np.round(np.arange(0.000, 0.4001, 0.005), 4)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 1500)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def cv(g):
    g = g.dropna()
    m = float(g.mean())
    return float(g.std() / m) if m > 0 else np.nan


def cvs(g):
    """cv of daily gross on the three windows."""
    return dict(gross_cv=cv(g), IS_gross_cv=cv(H.window(g, "IS")), OOS_gross_cv=cv(H.window(g, "OOS")))


def verdict_cv(row, kappa, win="full"):
    """4b-CV = the four CORE bars (H1,H2,OOS,DD) + cv(daily gross) >= kappa."""
    core = all(row[k] > 0 for k in ("m_H1", "m_H2", "m_OOS", "m_DD")) if win == "full" else \
        all(row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD"))
    c = row["gross_cv"] if win == "full" else row["IS_gross_cv"]
    return bool(core and np.isfinite(c) and c >= kappa)


# ============================================================ build the corpus (idea 131 verbatim + cv)
def build():
    GR, LD, RET, WF = [], [], {}, []
    V1, SPY, BARS = {}, {}, {}
    for pname in PANELS:
        px, spy, desc = J.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        SPY[pname] = spy
        bfull, bIS = J.bars_win(spy, "full"), J.bars_win(spy, "IS")
        BARS[pname] = (bfull, bIS)
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  MaxDD {bfull['sdd']:.2%}"
            f"  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  OOS Sharpe {bfull['soos']:.3f}")
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        V1[pname] = v1
        for book in BOOKS:
            for c in COSTS:
                D, rets, grs = J.do_cell(pname, px, spy, book, c, bfull, bIS, v1[c])
                for k in ("gross_cv", "IS_gross_cv", "OOS_gross_cv"):
                    D[k] = [cvs(grs[a])[k] for a in D["arm"]]
                GR.append(D)
                RET[(pname, book, c)] = rets
                # ladder with the SAME construction as idea 131's ladder_cell, plus window cvs
                W = H.targets(px, book)
                lr = []
                for m_ in LADDER:
                    res = H.run(px, W, m=m_, bps=c)
                    r = res["r"].loc[start:]
                    g = res["gross"].loc[start:]
                    mm = metrics(r)
                    mg = J.margins_at(r, g, bfull, PHI0, DELTA0, GAMMA0, "full")
                    mgi = J.margins_at(r, g, bIS, PHI0, DELTA0, GAMMA0, "IS")
                    p_fl, f_fl = J.verdict(mg, "floor")
                    p_gr, f_gr = J.verdict(mg, "gross")
                    p_ne, _ = J.verdict(mg, "neither")
                    lr.append(dict(panel=pname, book=book, cost=c, m=float(m_),
                                   CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                   gross=float(g.mean()), gross_sd=float(g.std()),
                                   m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                                   m_CAGR=mg["CAGR"], m_GROSS=mg["GROSS"],
                                   IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"],
                                   pass4b_floor=p_fl, fail_floor=",".join(f_fl) or "-",
                                   pass4b_gross=p_gr, fail_gross=",".join(f_gr) or "-",
                                   pass4b_neither=p_ne,
                                   floor_only=(f_fl == ["CAGR"]), gross_only=(f_gr == ["GROSS"]),
                                   **cvs(g)))
                LD.append(pd.DataFrame(lr))
        say(f"    ... {pname} done")
    G = pd.concat(GR, ignore_index=True)
    L = pd.concat(LD, ignore_index=True)
    return G, L, RET, V1, SPY, BARS


# ============================================================ main
def main():
    say("=" * 190)
    say("IDEA 143 — is gross DISPERSION the exposure-adequacy bar that gross LEVEL failed to be?")
    say(f"corpus = 3 panels x 3 books x 17 arms x 2 costs = 306 arm-rows; ladder = "
        f"3 x 3 x {len(LADDER)} x 2 = {3*3*len(LADDER)*2} rows.  IS <= {IS_END}, OOS >= {OOS_START}, "
        f"weekly, t+1, {GROSS:.0%} target gross, costs {COSTS} bps.")
    say(f"Bars held: DD cap {DELTA0} x |SPY|, CAGR floor {PHI0} x SPY, gross level {GAMMA0}.  "
        f"ONE tuned parameter: kappa in [{KAPPAS[0]:.3f}, {KAPPAS[-1]:.3f}] step 0.005 ({len(KAPPAS)} points).")
    say("=" * 190)

    G, L, RET, V1, SPY, BARS = build()

    # ---------------------------------------------------------- reproduction gate
    say("\n" + "=" * 190)
    say("REPRODUCTION GATE — idea 131's committed corpus must come back column-for-column")
    ok = []
    g131 = pd.read_csv(OUT / "2026-09-05_gross-as-the-missing-third-bar_B.grid.csv")
    l131 = pd.read_csv(OUT / "2026-09-05_gross-as-the-missing-third-bar_B.ladder.csv")
    key_g = ["panel", "book", "cost", "arm"]
    key_l = ["panel", "book", "cost", "m"]
    A = G.set_index(key_g).sort_index()
    B = g131.set_index(key_g).sort_index()
    num = [c for c in B.columns if pd.api.types.is_numeric_dtype(B[c])
           and not pd.api.types.is_bool_dtype(B[c]) and c in A.columns]
    d = float(max(np.nanmax(np.abs(A[c].values.astype(float) - B[c].values.astype(float))) for c in num))
    say(f"  (a) 306 arm-rows, {len(num)} numeric columns vs .grid.csv: max|diff| = {d:.2e} "
        f"-> {'PASS' if d < 1e-9 else 'FAIL'}   (shapes {A.shape} vs {B.shape})")
    ok.append(d < 1e-9)
    A2 = L.set_index(key_l).sort_index()
    B2 = l131.set_index(key_l).sort_index()
    num2 = [c for c in B2.columns if pd.api.types.is_numeric_dtype(B2[c])
            and not pd.api.types.is_bool_dtype(B2[c]) and c in A2.columns]
    d2 = float(max(np.nanmax(np.abs(A2[c].values.astype(float) - B2[c].values.astype(float))) for c in num2))
    say(f"  (b) {len(L)} ladder rows, {len(num2)} numeric columns vs .ladder.csv: max|diff| = {d2:.2e} "
        f"-> {'PASS' if d2 < 1e-9 else 'FAIL'}   (shapes {A2.shape} vs {B2.shape})")
    ok.append(d2 < 1e-9)
    census = dict(rows=len(G), pass4b=int(G.pass4b_floor.sum()), floor_only=int(G.floor_only.sum()),
                  lad_rows=len(L), lad_floor_only=int(L.floor_only.sum()))
    tgt = dict(rows=306, pass4b=29, floor_only=27, lad_rows=342, lad_floor_only=97)
    ok_c = all(census[k] == tgt[k] for k in tgt)
    say(f"  (c) census {census} vs target {tgt} -> {'PASS' if ok_c else 'FAIL'}")
    ok.append(ok_c)
    say(f"  GATE: {'ALL PASS' if all(ok) else 'FAILURE — numbers below are not comparable to idea 131'}")

    # the 11 "Pareto-best victims": per-cell Pareto flag taken straight from idea 131's committed grid
    par = g131.set_index(key_g)["pareto"].astype(bool)
    G["pareto131"] = [bool(par.loc[(r.panel, r.book, r.cost, r.arm)]) for r in G.itertuples()]
    VIC = G[G.floor_only]
    PVIC = G[G.floor_only & G.pareto131]
    say(f"\n  victims (floor_only) n={len(VIC)}   Pareto-best among them n={len(PVIC)} "
        f"(idea 131 targets 27 / 11 -> {'PASS' if (len(VIC), len(PVIC)) == (27, 11) else 'FAIL'})")

    # ---------------------------------------------------------- Q0: the two distributions
    say("\n" + "=" * 190)
    say("Q0 — the two families on the DISPERSION axis (this is what idea 131 saw post hoc)")
    CORE_L = L[(L.m_H1 > 0) & (L.m_H2 > 0) & (L.m_OOS > 0) & (L.m_DD > 0)]      # core-admissible ladder
    for nm, s in [("floor's victims (27)", VIC.gross_cv), ("  of which Pareto-best (11)", PVIC.gross_cv),
                  ("static-gross ladder (342)", L.gross_cv),
                  (f"core-admissible ladder ({len(CORE_L)})", CORE_L.gross_cv),
                  ("whole arm corpus (306)", G.gross_cv)]:
        say(f"  {nm:32s} cv  min {s.min():.4f}  median {s.median():.4f}  mean {s.mean():.4f}  max {s.max():.4f}")
    say(f"\n  LEVEL axis (idea 131's failure): victims mean-gross [{VIC.gross.min():.3f}, {VIC.gross.max():.3f}]  "
        f"vs core-admissible ladder [{CORE_L.gross.min():.3f}, {CORE_L.gross.max():.3f}]  -> OVERLAP")
    say(f"  DISPERSION axis:               victims cv [{VIC.gross_cv.min():.4f}, {VIC.gross_cv.max():.4f}]  "
        f"vs WHOLE ladder cv [{L.gross_cv.min():.4f}, {L.gross_cv.max():.4f}]")
    below = VIC[VIC.gross_cv <= L.gross_cv.max()]
    say(f"  victims at or below every ladder point's cv: {len(below)} of 27 -> "
        f"{sorted(zip(below.arm, below.panel, below.book, np.round(below.gross_cv, 4)))}")

    # ---------------------------------------------------------- Q1/Q2: the separation frontier
    say("\n" + "=" * 190)
    say("Q1/Q2 — SEPARATION FRONTIER, every kappa grid point (bar = the four CORE bars + cv >= kappa)")
    say(f"  reference: the published CAGR floor (phi={PHI0}) admits {int(G.pass4b_floor.sum())} corpus rows, "
        f"{int(L.pass4b_floor.sum())} ladder rows, and saves 0 of its own 27 victims.")
    say(f"  reference: idea 131's best gross LEVEL bar admitted 0 of 34 grid points with BOTH jobs done.")
    fr = []
    for k in KAPPAS:
        adm = G.apply(lambda r: verdict_cv(r, k), axis=1)
        ladm = L.apply(lambda r: verdict_cv(r, k), axis=1)
        lost = int((G.pass4b_floor & ~adm).sum())
        fr.append(dict(kappa=float(k), corpus_admits=int(adm.sum()),
                       floor_admits_lost=lost,
                       victims_admitted=int((G.floor_only & adm).sum()),
                       pareto_victims_admitted=int((G.floor_only & G.pareto131 & adm).sum()),
                       ladder_admitted=int(ladm.sum()),
                       core_ladder_admitted=int((ladm & L.index.isin(CORE_L.index)).sum()),
                       both_jobs=bool(int((G.floor_only & adm).sum()) == 27 and int(ladm.sum()) == 0),
                       pass4a_among_admitted=int((G.pass4a & adm).sum())))
    FR = pd.DataFrame(fr)
    say(FR.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    nboth = int(FR.both_jobs.sum())
    say(f"\n  kappa doing BOTH jobs (all 27 victims AND 0 ladder points): {nboth} of {len(FR)} grid points"
        + (f"  -> kappa in [{FR[FR.both_jobs].kappa.min():.3f}, {FR[FR.both_jobs].kappa.max():.3f}]" if nboth else ""))
    z = FR[FR.ladder_admitted == 0]
    if len(z):
        say(f"  first kappa emptying the ladder: {z.kappa.min():.3f}; there victims_admitted = "
            f"{int(z.loc[z.kappa.idxmin(), 'victims_admitted'])} of 27, Pareto "
            f"{int(z.loc[z.kappa.idxmin(), 'pareto_victims_admitted'])} of 11, "
            f"floor admissions lost {int(z.loc[z.kappa.idxmin(), 'floor_admits_lost'])}")
    a27 = FR[FR.victims_admitted == 27]
    if len(a27):
        say(f"  last kappa admitting all 27 victims: {a27.kappa.max():.3f}; there ladder_admitted = "
            f"{int(a27.loc[a27.kappa.idxmax(), 'ladder_admitted'])} of 342")

    # ---------------------------------------------------------- Q3: rule 8
    say("\n" + "=" * 190)
    say("Q3 — RULE 8 WALK-FORWARD.  Every screen reads the IS window (<=2016-12-31) ONLY; the pick "
        "(argmax IS Sharpe) is read once on 2017-2026.")
    kIS = []
    for k in KAPPAS:
        adm = G.apply(lambda r: verdict_cv(r, k, "IS"), axis=1)
        ladm = L.apply(lambda r: verdict_cv(r, k, "IS"), axis=1)
        isvic = G.apply(lambda r: all(r[f"IS_m_{x}"] > 0 for x in ("H1", "H2", "DD")) and r["IS_m_CAGR"] <= 0, axis=1)
        kIS.append(dict(kappa=float(k), IS_corpus_admits=int(adm.sum()),
                        IS_victims_admitted=int((isvic & adm).sum()), IS_victims=int(isvic.sum()),
                        IS_ladder_admitted=int(ladm.sum())))
    KIS = pd.DataFrame(kIS)
    say("\n  kappa chosen ON THE IS WINDOW ONLY — separation frontier of the IS window:")
    say(KIS.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    zero = KIS[KIS.IS_ladder_admitted == 0]
    KSTAR = float(zero.kappa.min()) if len(zero) else float(KIS.kappa.max())
    say(f"\n  IS-CHOSEN kappa* = {KSTAR:.3f}  (smallest kappa emptying the ladder on the IS window; "
        f"there IS victims admitted {int(zero.loc[zero.kappa.idxmin(), 'IS_victims_admitted']) if len(zero) else 0} "
        f"of {int(KIS.IS_victims.iloc[0])}).  Nothing OOS was read to pick it.")

    def core_IS(r):
        return all(r[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD"))

    WF = []
    for (pname, book, c), rets in RET.items():
        sub = G[(G.panel == pname) & (G.book == book) & (G.cost == c)]
        bIS = BARS[pname][1]
        spy, v1n = SPY[pname], V1[pname][c]
        cand = {
            "S0 none": sub,
            "S1 CAGR floor": sub[sub.apply(lambda r: core_IS(r) and r["IS_m_CAGR"] > 0, axis=1)],
            "S2 no adequacy bar": sub[sub.apply(core_IS, axis=1)],
            "S3 gross level 0.50": sub[sub.apply(lambda r: core_IS(r) and r["IS_gross"] - GAMMA0 > 0, axis=1)],
            f"S4 cv bar {KSTAR:.3f}": sub[sub.apply(lambda r: core_IS(r) and r["IS_gross_cv"] >= KSTAR, axis=1)],
        }
        mc = metrics(H.window(rets["control"], "OOS"))
        ms = metrics(spy.loc[OOS_START:])
        mv = metrics(H.window(v1n, "OOS"))
        best = sub.loc[sub.OOS_Sharpe.idxmax(), "arm"]
        for s, cd in cand.items():
            base = dict(sel=s, panel=pname, book=book, cost=c, ctl_OOS_Sharpe=mc["Sharpe"],
                        spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_CAGR=ms["CAGR"], spy_OOS_MaxDD=ms["MaxDD"],
                        v1_OOS_Sharpe=mv["Sharpe"], v1_OOS_CAGR=mv["CAGR"], v1_OOS_MaxDD=mv["MaxDD"])
            if len(cd) == 0:
                WF.append(dict(base, pick="(none)", n_admitted=0, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                               OOS_MaxDD=np.nan, beat_spy=np.nan, beat_v1=np.nan, beat_ctl=np.nan,
                               oos_best=np.nan))
                continue
            p = cd.loc[cd.IS_Sharpe.idxmax()]
            m = metrics(H.window(rets[p["arm"]], "OOS"))
            WF.append(dict(base, pick=p["arm"], n_admitted=len(cd), OOS_CAGR=m["CAGR"],
                           OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                           beat_spy=bool(m["Sharpe"] > ms["Sharpe"]), beat_v1=bool(m["Sharpe"] > mv["Sharpe"]),
                           beat_ctl=bool(m["Sharpe"] > mc["Sharpe"]), oos_best=bool(p["arm"] == best)))
    W = pd.DataFrame(WF)

    say("\n  per-selector OOS summary (cells where the selector picks at all):")
    rows = []
    S0 = W[W.sel == "S0 none"].set_index(["panel", "book", "cost"])
    for s in W.sel.unique():
        d = W[W.sel == s]
        e = d[d.pick != "(none)"]
        moved = sum(1 for r in e.itertuples()
                    if S0.loc[(r.panel, r.book, r.cost), "pick"] != r.pick)
        rows.append(dict(selector=s, cells_picking=len(e), OOS_CAGR=e.OOS_CAGR.mean(),
                         OOS_Sharpe=e.OOS_Sharpe.mean(), OOS_MaxDD=e.OOS_MaxDD.mean(),
                         beat_SPY=f"{int(e.beat_spy.sum())}/{len(e)}",
                         beat_v1=f"{int(e.beat_v1.sum())}/{len(e)}",
                         beat_ctl=f"{int(e.beat_ctl.sum())}/{len(e)}",
                         picks_moved_vs_S0=moved))
    SUM = pd.DataFrame(rows)
    say(SUM.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # paired reading: only the cells the cv bar enters
    ent = set(map(tuple, W[(W.sel.str.startswith("S4")) & (W.pick != "(none)")][["panel", "book", "cost"]].values))
    say(f"\n  PAIRED on the {len(ent)} cells the cv bar enters:")
    prows = []
    for s in W.sel.unique():
        d = W[(W.sel == s) & W.apply(lambda r: (r.panel, r.book, r.cost) in ent, axis=1) & (W.pick != "(none)")]
        prows.append(dict(selector=s, cells=len(d), OOS_CAGR=d.OOS_CAGR.mean(), OOS_Sharpe=d.OOS_Sharpe.mean(),
                          OOS_MaxDD=d.OOS_MaxDD.mean(), beat_SPY=f"{int(d.beat_spy.sum())}/{len(d)}"))
    say(pd.DataFrame(prows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    sref = W[W.sel == "S0 none"]
    say(f"\n  OOS references (mean over the 18 cells): SPY CAGR {sref.spy_OOS_CAGR.mean():.2%} / Sharpe "
        f"{sref.spy_OOS_Sharpe.mean():.3f} / MaxDD {sref.spy_OOS_MaxDD.mean():.2%};  RULES v1 CAGR "
        f"{sref.v1_OOS_CAGR.mean():.2%} / Sharpe {sref.v1_OOS_Sharpe.mean():.3f} / MaxDD "
        f"{sref.v1_OOS_MaxDD.mean():.2%};  ungated control Sharpe {sref.ctl_OOS_Sharpe.mean():.3f}")

    # sensitivity of the rule-8 answer to kappa: does ANY kappa move a pick?
    say("\n  Rule-8 SENSITIVITY — picks moved vs S2 (core-only) at every kappa, all 18 cells:")
    srows = []
    for k in KAPPAS[::2]:
        mv_, empt = 0, 0
        for (pname, book, c), rets in RET.items():
            sub = G[(G.panel == pname) & (G.book == book) & (G.cost == c)]
            base = sub[sub.apply(core_IS, axis=1)]
            cd = sub[sub.apply(lambda r: core_IS(r) and r["IS_gross_cv"] >= k, axis=1)]
            if len(cd) == 0:
                empt += 1
                continue
            if len(base) == 0:
                continue
            if cd.loc[cd.IS_Sharpe.idxmax(), "arm"] != base.loc[base.IS_Sharpe.idxmax(), "arm"]:
                mv_ += 1
        srows.append(dict(kappa=float(k), cells_emptied=empt, picks_moved_vs_S2=mv_))
    SENS = pd.DataFrame(srows)
    say(SENS.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------- both KEEP paths
    say("\n" + "=" * 190)
    say("BOTH KEEP PATHS over all 306 rows (no new book is proposed — this re-scores an existing corpus)")
    kb = FR.loc[(FR.kappa - KSTAR).abs().idxmin()]
    say(f"  4a (beat the live book): {int(G.pass4a.sum())} of 306")
    say(f"  4b as published (CAGR floor):     {int(G.pass4b_floor.sum())} of 306, of which "
        f"{int((G.pass4a & G.pass4b_floor).sum())} also pass 4a")
    say(f"  4b with the gross LEVEL bar 0.50: {int(G.pass4b_gross.sum())} of 306, of which "
        f"{int((G.pass4a & G.pass4b_gross).sum())} also pass 4a")
    admk = G.apply(lambda r: verdict_cv(r, KSTAR), axis=1)
    say(f"  4b with the cv bar kappa*={KSTAR:.3f}:      {int(admk.sum())} of 306, of which "
        f"{int((G.pass4a & admk).sum())} also pass 4a;  ladder admitted {int(L.apply(lambda r: verdict_cv(r, KSTAR), axis=1).sum())} of 342")
    for nm, sel in [("4b-FLOOR", G.pass4b_floor), ("4b-GROSS(0.50)", G.pass4b_gross), (f"4b-CV({KSTAR:.3f})", admk)]:
        d = G[sel]
        say(f"    admitted-set OOS quality {nm:16s} n={len(d):3d}  CAGR {d.OOS_CAGR.mean():.2%}  "
            f"Sharpe {d.OOS_Sharpe.mean():.3f}  MaxDD {d.OOS_MaxDD.mean():.2%}  4a {int((d.pass4a).sum())}")

    # ---------------------------------------------------------- write
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    FR.to_csv(OUT / f"{STEM}.frontier.csv", index=False)
    KIS.to_csv(OUT / f"{STEM}.is_frontier.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    SENS.to_csv(OUT / f"{STEM}.sensitivity.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.[grid|ladder|frontier|is_frontier|walkforward|sensitivity].csv + .console.txt")


if __name__ == "__main__":
    main()
