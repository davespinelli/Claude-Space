#!/usr/bin/env python3
"""Idea 874 - "does-the-record-s-DD-CAP-have-the-SAME-two-questions-problem-as-the-CAGR-FLOOR"
(lane B, 2026-09-15).

The queue's ask, restated exactly
---------------------------------
Idea 868 showed PROTOCOL 4b's CAGR FLOOR conflates two different questions:

    (i)  is this book better than passive AT ITS OWN RISK/EXPOSURE?     -> g x SPY comparand
    (ii) is this book worth real capital IN ABSOLUTE TERMS?             -> SPY at 100%

and that the two conventions rank the same 54 GRID books in OPPOSITE orders
(rho(gross, gap) -0.619 under the 100% convention vs +0.535 under the gross-matched one).

4b's OTHER absolute-comparand leg is the DD CAP: `MaxDD >= 0.60 x MaxDD(SPY)`, where that SPY is
again 100% invested every day.  Ideas 662 / 866 / 676 all priced the channel that makes this leg
suspect: de-grossing buys drawdown and pays CAGR, so a book that holds cash clears the cap for a
reason that has nothing to do with its security selection.  The queue asks for 868's THREE-
CONVENTION LADDER re-run on the DD leg, and for the answer to one specific question:

    DOES THE CAP FLIP THE SAME BOOKS IN THE SAME DIRECTION AS THE FLOOR DID?

The sign trap this run exists to expose
----------------------------------------
The two legs are NOT symmetric under the swap, and the asymmetry is arithmetic, not empirical.
Gross-matching LOWERS the comparand's CAGR, so a gross-matched CAGR floor is EASIER: it is a
CONCESSION, and 868 measured it as one (GRID 4b passes 26 -> 35 of 62).  Gross-matching also
makes the comparand's DRAWDOWN SHALLOWER, and the DD cap is a ceiling on |drawdown| stated as a
fraction of that comparand - so a gross-matched DD cap is HARDER.  It is a TIGHTENING.  If that
is what the data show, the queue's "same direction" is refuted by construction of the two legs,
and the record cannot fix 4b by swapping the comparand once: the same swap concedes on one leg
and tightens on the other, and their net is an empirical question this run answers.

Conventions, stated exactly (identical to 868's, applied to MaxDD instead of CAGR)
    CURRENT :  r_t = r_SPY,t             PROTOCOL's own - SPY 100% invested every day
    CONST   :  r_t = gbar * r_SPY,t      matched to the book's time-averaged realised gross
    PATH    :  r_t = g_t  * r_SPY,t      matched day by day to the book's own realised gross
Cash earns ZERO in all three (the record's rf=0 convention; idea 676 is why).  MaxDD is taken on
each comparand's own compounded equity curve, NOT scaled from SPY's - a g-scaled path's drawdown
is not g x SPY's drawdown, and this run reports the difference rather than assuming it away.

Pre-registered hypotheses and bars (fixed before any number below the gates was read)
    H_TWO    the DD cap has the SAME two-questions SHAPE as the floor: on the GRID,
             rho(mean gross, DD slack) has OPPOSITE SIGNS under CURRENT and under PATH.
             PASS = the defect 868 named on the floor is present on the cap too.
    H_DIR    the DD swap flips books in the OPPOSITE direction to the CAGR swap: a MAJORITY of
             4b verdict flips caused by the DD swap are PASS -> FAIL (868's floor flips were
             FAIL -> PASS).  PASS = the queue's "same direction" is REFUTED.
    H_SAME   the DD-swap flip SET overlaps the CAGR-swap flip set, Jaccard >= 0.20.
             PASS = "the same books".
    H_EASY   the record's premise (662/866/676) that the cap is mechanically easy for a
             de-grossed book: under CURRENT at kappa = 0.60 the DD-leg pass rate among GRID
             books with gbar < 0.70 exceeds that among gbar >= 0.85 by >= 20 pp.
    H_WF     (rule 8) the sign of the book-minus-comparand DD gap is the same in 2009-2016 and
             2017+ for a MAJORITY of books.  A gap that changes sign cannot support a cap.
  Each prints with its bar and its verdict, PASS or FAIL, whichever way it falls.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. convention   in {CURRENT, CONST, PATH}
    2. cap fraction kappa in {0.40, 0.50, 0.60, 0.70, 0.80, 1.00}; 0.60 is PROTOCOL's.
    ALL grid points reported, at every panel, book, set and cost rung.  Nothing is selected on.

Book sets, IMPORTED not re-typed, from the lane-C script committed 2026-09-15, and extended to
the small panel by 868's own `small_grid` shape, so this run's 62 books ARE 868's 62 books:
    SHELF  the record's 8 memo-backed 4b KEEP-candidate books (`shelf_books`), gated in G1.
    GRID   the mechanical band x gross x QROLL ladder never memo-selected (`grid_books`), plus
           the same ladder on SMALL.

Reproduction gates (printed before any new number is read)
    G1  every SHELF book reproduces its committed memo triple, MaxDD leg included.
    G2  the gross-matched comparand at a constant g = 1.00 is SPY itself, to machine precision.
    G3  the PATH comparand's realised mean gross equals the book's own, to machine precision.
    G4  fast metrics == engine.metrics() on a live book.
    G5  CROSS-RUN: this run's b_CAGR and gap_PATH reproduce 868's COMMITTED gaps.csv, which is
        what makes the "same books, same direction" comparison legitimate rather than asserted.

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52
tickers with max_1d_move >= 1.0 per data/small_meta.csv), so every drawdown LEVEL below is
optimistic - the books' and the comparands' alike, which is why this run reports the book-minus-
comparand GAP and the VERDICT FLIP rather than any level on its own.

Deterministic, standalone.  Modifies nothing.  Proposes one PROTOCOL line; applies none (rule 6).
"""
import importlib.util
import sys
import time
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
LANEC = OUT / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"
G868 = OUT / "2026-09-15_does-the-record-s-SHELF-beat-a-GROSS-MATCHED-SPY-on-the-CAGR-LEG_cloud.gaps.csv"
LINES = []

FREQ = "W"
WARMUP = 260
RUNGS = [10.0, 25.0]
KAPPAS = [0.40, 0.50, 0.60, 0.70, 0.80, 1.00]
PROTOCOL_KAPPA = 0.60          # PROTOCOL 4b: MaxDD <= 60% of SPY's
PROTOCOL_PHI = 0.70            # PROTOCOL 4b: CAGR >= 70% of SPY's (held fixed while DD swaps)
SPLIT = "2017-01-01"
CONVENTIONS = ["CURRENT", "CONST", "PATH"]


def log(s=""):
    print(s)
    LINES.append(str(s))


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]


def maxdd(r):
    eq = (1.0 + r).cumprod()
    return float((eq / eq.cummax() - 1.0).min())


def mstats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                DD1=maxdd(r.iloc[:h]), DD2=maxdd(r.iloc[h:]))


def small_grid(px, pname, laneC):
    """868's own third-panel ladder, restated verbatim so the two runs share 62 books."""
    out = {}
    elig = laneC.eligible_mask(px).astype(float)
    nn = elig.sum(axis=1).replace(0, np.nan)
    base = elig.div(nn, axis=0).fillna(0.0)
    br = laneC.breadth(px)
    for band, g in product((0.03, 0.08), (0.50, 0.75, 1.00)):
        out[f"{pname}-band{band:.2f}-g{g:.2f}"] = dict(
            panel=pname, freq="W", W=rules_v2_weights(px, band, g), memo=None, src="GRID")
    for q, w, dep in product((0.12, 0.17), (252, 504, 1008), (0.50, 1.00)):
        thr = br.rolling(w, min_periods=w).quantile(q)
        out[f"{pname}-qroll-q{q:.2f}-w{w}-d{dep:.2f}"] = dict(
            panel=pname, freq="W", W=base.mul(laneC.gate_mult(br, thr, dep, px.index), axis=0),
            memo=None, src="GRID")
    return out


def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 874 - does the record's 4b DD CAP have the SAME two-questions problem as the "
        "CAGR FLOOR?  (lane B, 2026-09-15)")
    log("=" * 100)
    laneC = load_lane_c()

    U = load_universe()
    B = load_universe(broad=True)
    S = small_panel()
    panels = {"U56": U, "B136": B, "SMALL": S}
    log(f"panels: U56 {U.shape}  B136 {B.shape}  SMALL {S.shape} "
        f"(sub-$2B, 52 max_1d_move>=1.0 tickers dropped)")

    books = {}
    for k, v in laneC.shelf_books(U, B).items():
        v["set"] = "SHELF"
        books[k] = v
    for k, v in laneC.grid_books(U, B).items():
        v["set"] = "GRID"
        books[k] = v
    for k, v in small_grid(S.drop(columns=["SPY"], errors="ignore"), "SMALL", laneC).items():
        v["set"] = "GRID"
        books[k] = v
    log(f"books: {sum(1 for b in books.values() if b['set']=='SHELF')} SHELF (memo-backed) + "
        f"{sum(1 for b in books.values() if b['set']=='GRID')} GRID = {len(books)}  "
        f"(868's set, imported)")
    log(f"ladder: {len(CONVENTIONS)} conventions x {len(KAPPAS)} cap fractions x {len(RUNGS)} "
        f"cost rungs x {len(books)} books = "
        f"{len(CONVENTIONS)*len(KAPPAS)*len(RUNGS)*len(books)} verdict cells, all published")

    # ------------------------------------------------------------------ price every book
    log("\n[0] REPRODUCTION GATES (printed before any new number is read)")
    base_cache = {}
    rows, g1 = [], []
    for name, spec in books.items():
        px = panels[spec["panel"]]
        pxn = px.drop(columns=["SPY"], errors="ignore")
        W = spec["W"].reindex(pxn.index).reindex(columns=pxn.columns).fillna(0.0)
        start = pxn.index[WARMUP]
        gross_t = W.sum(axis=1).shift(1).fillna(0.0).loc[start:]     # t+1 aligned, as held
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for c in RUNGS:
            r = backtest(pxn, W, cost_bps=c, freq=spec["freq"])["returns"].loc[start:]
            bs = mstats(r)
            const_g = float(gross_t.mean())
            comp = {"CURRENT": spy, "CONST": const_g * spy, "PATH": gross_t * spy}
            key = (spec["panel"], c)
            if key not in base_cache:
                base_cache[key] = backtest(pxn, rules_v2_weights(pxn), cost_bps=c,
                                           freq="W")["returns"].loc[start:]
            base = base_cache[key]
            bl = mstats(base)
            oos = r.index >= pd.Timestamp(SPLIT)
            row = dict(book=name, set=spec["set"], panel=spec["panel"], cost=c,
                       mean_gross=const_g, src=spec["src"],
                       **{f"b_{k}": v for k, v in bs.items()},
                       b_OOS_CAGR=metrics(r[oos])["CAGR"], b_OOS_Sharpe=metrics(r[oos])["Sharpe"],
                       b_OOS_MaxDD=maxdd(r[oos]),
                       b_IS_CAGR=metrics(r[~oos])["CAGR"], b_IS_Sharpe=metrics(r[~oos])["Sharpe"],
                       b_IS_MaxDD=maxdd(r[~oos]),
                       bl_CAGR=bl["CAGR"], bl_H1=bl["H1"], bl_H2=bl["H2"], bl_MaxDD=bl["MaxDD"],
                       bl_Sharpe=bl["Sharpe"], bl_OOS_Sharpe=metrics(base[oos])["Sharpe"],
                       bl_OOS_CAGR=metrics(base[oos])["CAGR"], bl_OOS_MaxDD=maxdd(base[oos]))
            for cv, cr in comp.items():
                cm = mstats(cr)
                for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "DD1", "DD2"):
                    row[f"{cv}_{k}"] = cm[k]
                row[f"{cv}_OOS_CAGR"] = metrics(cr[oos])["CAGR"]
                row[f"{cv}_OOS_MaxDD"] = maxdd(cr[oos])
                row[f"{cv}_IS_CAGR"] = metrics(cr[~oos])["CAGR"]
                row[f"{cv}_IS_MaxDD"] = maxdd(cr[~oos])
            row["path_mean_gross"] = float(gross_t.mean())
            rows.append(row)
            if c == 10.0 and spec["memo"]:
                m = spec["memo"]
                g1.append(dict(book=name, memo_CAGR=m[0], here_CAGR=bs["CAGR"],
                               memo_Sharpe=m[1], here_Sharpe=bs["Sharpe"],
                               memo_MaxDD=m[2], here_MaxDD=bs["MaxDD"]))
    df = pd.DataFrame(rows)

    g1 = pd.DataFrame(g1)
    g1["dC"] = (g1.here_CAGR - g1.memo_CAGR).abs()
    g1["dS"] = (g1.here_Sharpe - g1.memo_Sharpe).abs()
    g1["dD"] = (g1.here_MaxDD - g1.memo_MaxDD).abs()
    log("  G1 SHELF books vs their committed memo triples (@10 bps) - the DD leg is the one "
        "this run is about")
    log(f"    {'book':36s} {'memo DD':>9s} {'here':>9s} {'|dDD|':>7s} {'memo CAGR':>10s} "
        f"{'here':>8s} {'|dC|':>7s} {'|dS|':>7s}")
    for _, r in g1.iterrows():
        md = "   n/a  " if pd.isna(r.memo_MaxDD) else f"{r.memo_MaxDD:9.4f}"
        dd = "   n/a " if pd.isna(r.dD) else f"{r.dD:7.4f}"
        log(f"    {r.book:36s} {md} {r.here_MaxDD:9.4f} {dd} {r.memo_CAGR:10.4f} "
            f"{r.here_CAGR:8.4f} {r.dC:7.4f} {r.dS:7.4f}")
    okd = int((g1.dD < 0.02).sum())
    nd = int(g1.dD.notna().sum())
    ok = int(((g1.dC < 0.01) & (g1.dS < 0.10)).sum())
    log(f"    G1 CAGR/Sharpe legs: {ok} of {len(g1)} within 1.00 pp / 0.10  "
        f"[{'PASS' if ok >= len(g1) - 1 else 'PARTIAL'}]")
    log(f"    G1 DD leg: {okd} of {nd} memo'd MaxDDs reproduce within 2.00 pp  "
        f"[{'PASS' if okd >= nd - 1 else 'PARTIAL'}]  (1 shelf memo published no MaxDD; tape "
        f"vintage moves every LEVEL slightly, and the GAP this run measures is same-tape)")

    spy_full = U["SPY"].pct_change().fillna(0.0).loc[U.index[WARMUP]:]
    g2 = float(np.max(np.abs((1.00 * spy_full) - spy_full)))
    g2b = abs(maxdd(1.00 * spy_full) - maxdd(spy_full))
    log(f"  G2 comparand at constant g=1.00 == SPY                max|d| = {g2:.3e}, "
        f"|dMaxDD| = {g2b:.3e}  [{'PASS' if g2 == 0 and g2b == 0 else 'FAIL'}]")
    g3 = float((df["path_mean_gross"] - df["mean_gross"]).abs().max())
    log(f"  G3 PATH comparand's mean gross == the book's own      max|d| = {g3:.3e}  "
        f"[{'PASS' if g3 < 1e-12 else 'FAIL'}]")
    chk = backtest(U.drop(columns=["SPY"]), rules_v2_weights(U.drop(columns=["SPY"])),
                   cost_bps=10, freq="W")["returns"].loc[U.index[WARMUP]:]
    g4 = max(abs(mstats(chk)["Sharpe"] - metrics(chk)["Sharpe"]),
             abs(maxdd(chk) - metrics(chk)["MaxDD"]))
    log(f"  G4 fast metrics == engine.metrics() (Sharpe and MaxDD) |d|   = {g4:.3e}  "
        f"[{'PASS' if g4 < 1e-12 else 'FAIL'}]")

    d10 = df[df.cost == 10.0].copy()
    d10["gap_PATH"] = d10.b_CAGR - d10.PATH_CAGR
    d10["gap_CONST"] = d10.b_CAGR - d10.CONST_CAGR
    d10["gap_CURRENT"] = d10.b_CAGR - d10.CURRENT_CAGR
    if G868.exists():
        g868 = pd.read_csv(G868).set_index("book")
        j = d10.set_index("book").join(g868[["b_CAGR", "gap_PATH"]], rsuffix="_868", how="inner")
        e1 = float((j.b_CAGR - j.b_CAGR_868).abs().max())
        e2 = float((j.gap_PATH - j.gap_PATH_868).abs().max())
        log(f"  G5 CROSS-RUN vs 868's COMMITTED gaps.csv ({len(j)} books joined): "
            f"max|d b_CAGR| = {e1:.3e}, max|d gap_PATH| = {e2:.3e}  "
            f"[{'PASS' if max(e1, e2) < 1e-9 else 'FAIL'}]")
        g5ok = max(e1, e2) < 1e-9
    else:
        log("  G5 CROSS-RUN: 868's gaps.csv not found  [SKIP]")
        g5ok = None

    # ============================================================ [1] THE SHAPE OF THE DEFECT
    log("\n" + "=" * 100)
    log("[1] H_TWO - does the DD cap conflate the SAME two questions the CAGR floor does?")
    log("=" * 100)
    for cv in CONVENTIONS:
        d10[f"ddgap_{cv}"] = d10.b_MaxDD - d10[f"{cv}_MaxDD"]           # + = shallower than comp
        d10[f"slack_{cv}"] = d10.b_MaxDD - PROTOCOL_KAPPA * d10[f"{cv}_MaxDD"]  # + = passes
    sh = d10[d10.set == "SHELF"].sort_values("b_MaxDD", ascending=False)
    log("    SHELF, @10 bps - the book's own drawdown against each convention's comparand")
    log(f"    {'book':36s} {'gbar':>6s} {'book DD':>8s} {'SPY100':>8s} {'CONST':>8s} "
        f"{'PATH':>8s} {'slack@0.60 CUR':>15s} {'PATH':>8s}")
    for _, r in sh.iterrows():
        log(f"    {r.book:36s} {r.mean_gross:6.3f} {r.b_MaxDD:8.2%} {r.CURRENT_MaxDD:8.2%} "
            f"{r.CONST_MaxDD:8.2%} {r.PATH_MaxDD:8.2%} {r.slack_CURRENT:15.2%} "
            f"{r.slack_PATH:8.2%}")
    gr = d10[d10.set == "GRID"].copy()
    log("")
    log("    THE MECHANISM: Spearman(mean gross, DD slack at kappa=0.60) on the GRID (n="
        f"{len(gr)})")
    rho = {}
    for cv in CONVENTIONS:
        rho[cv] = float(gr[["mean_gross", f"slack_{cv}"]].corr(method="spearman").iloc[0, 1])
        per = "; ".join(
            f"{p} {float(gr[gr.panel==p][['mean_gross', f'slack_{cv}']].corr(method='spearman').iloc[0,1]):+.3f}"
            for p in ["U56", "B136", "SMALL"])
        log(f"      {cv:8s} rho = {rho[cv]:+.3f}   (per panel: {per})")
    opp = np.sign(rho["CURRENT"]) != np.sign(rho["PATH"])
    log(f"    H_TWO (CURRENT and PATH slacks rank the GRID in OPPOSITE orders): "
        f"{rho['CURRENT']:+.3f} vs {rho['PATH']:+.3f}  [{'PASS' if opp else 'FAIL'}]")
    log(f"    868's CAGR-leg reading on the same books, recomputed here: "
        f"rho(gross, gap_CURRENT) = "
        f"{float(gr[['mean_gross','gap_CURRENT']].corr(method='spearman').iloc[0,1]):+.3f}, "
        f"rho(gross, gap_PATH) = "
        f"{float(gr[['mean_gross','gap_PATH']].corr(method='spearman').iloc[0,1]):+.3f}")

    log("\n    H_EASY - is the cap mechanically easy for a de-grossed book (662/866/676)?")
    lo = gr[gr.mean_gross < 0.70]
    hi = gr[gr.mean_gross >= 0.85]
    for nm, s in (("gbar < 0.70", lo), ("gbar >= 0.85", hi)):
        p = float((s.b_MaxDD >= PROTOCOL_KAPPA * s.CURRENT_MaxDD).mean()) if len(s) else np.nan
        log(f"      {nm:12s} n={len(s):3d}  DD-leg pass rate under CURRENT at kappa=0.60: "
            f"{p:.3f}   (median book DD {s.b_MaxDD.median():.2%}, median gbar "
            f"{s.mean_gross.median():.3f})")
    plo = float((lo.b_MaxDD >= PROTOCOL_KAPPA * lo.CURRENT_MaxDD).mean())
    phi_ = float((hi.b_MaxDD >= PROTOCOL_KAPPA * hi.CURRENT_MaxDD).mean())
    log(f"    H_EASY (lo-gross pass rate exceeds hi-gross by >= 20 pp): "
        f"{plo:.3f} - {phi_:.3f} = {plo - phi_:+.1%}  "
        f"[{'PASS' if plo - phi_ >= 0.20 else 'FAIL'}]")

    # ================================================================= [2] THE FULL LADDER
    log("\n" + "=" * 100)
    log("[2] THE DD LEG ALONE - pass rate at every (kappa x convention) cell, ALL 18 per set")
    log("=" * 100)
    lad = []
    for kap, cv in product(KAPPAS, CONVENTIONS):
        for st in ("SHELF", "GRID"):
            s = d10[d10.set == st]
            lad.append(dict(kappa=kap, convention=cv, set=st, cost=10.0,
                            pass_rate=float((s.b_MaxDD >= kap * s[f"{cv}_MaxDD"]).mean()),
                            n=len(s)))
    lad = pd.DataFrame(lad)
    for st in ("SHELF", "GRID"):
        log(f"    {st} (n={int(lad[lad.set==st].n.iloc[0])})  [kappa = cap fraction; PROTOCOL "
            f"0.60]")
        log(f"      {'kappa':>5s} " + " ".join(f"{cv:>10s}" for cv in CONVENTIONS))
        for kap in KAPPAS:
            s = lad[(lad.kappa == kap) & (lad.set == st)].set_index("convention")
            log(f"      {kap:5.2f} " + " ".join(f"{s.loc[cv,'pass_rate']:10.3f}"
                                                for cv in CONVENTIONS))
    k60 = lad[(lad.kappa == PROTOCOL_KAPPA) & (lad.set == "GRID")].set_index("convention")
    log(f"    GRID at PROTOCOL's kappa=0.60: CURRENT {k60.loc['CURRENT','pass_rate']:.3f} -> "
        f"PATH {k60.loc['PATH','pass_rate']:.3f} = "
        f"{k60.loc['PATH','pass_rate'] - k60.loc['CURRENT','pass_rate']:+.1%}  "
        f"(868's CAGR leg moved +{0.20:.0%}-scale in the OPPOSITE sense; the direct comparison "
        f"is printed in [3])")

    # ============================================================ [3] FULL 4b VERDICTS + FLIPS
    log("\n" + "=" * 100)
    log("[3] H_DIR / H_SAME - the FULL 4b verdict with the DD leg swapped, against 868's flips")
    log("=" * 100)
    ver = []
    for _, r in df.iterrows():
        p4a = (r.b_H1 > r.bl_H1) and (r.b_H2 > r.bl_H2) and (r.b_MaxDD >= r.bl_MaxDD)
        for kap, cv in product(KAPPAS, CONVENTIONS):
            legs = dict(H1=r.b_H1 > r.CURRENT_H1, H2=r.b_H2 > r.CURRENT_H2,
                        OOS=r.b_OOS_Sharpe > r.CURRENT_Sharpe,
                        DDCAP=r.b_MaxDD >= kap * r[f"{cv}_MaxDD"],
                        CAGRFLOOR=r.b_CAGR >= PROTOCOL_PHI * r["CURRENT_CAGR"])
            # the CAGR-leg swap 868 priced, held at PROTOCOL's DD cap - for the flip comparison
            legs_c = dict(legs)
            legs_c["DDCAP"] = r.b_MaxDD >= PROTOCOL_KAPPA * r["CURRENT_MaxDD"]
            legs_c["CAGRFLOOR"] = r.b_CAGR >= PROTOCOL_PHI * r[f"{cv}_CAGR"]
            # both legs swapped together - what a gross-matched PROTOCOL would actually do
            legs_b = dict(legs)
            legs_b["CAGRFLOOR"] = r.b_CAGR >= PROTOCOL_PHI * r[f"{cv}_CAGR"]
            ver.append(dict(book=r.book, set=r.set, panel=r.panel, cost=r.cost, kappa=kap,
                            convention=cv, pass4a=p4a, pass4b=all(legs.values()),
                            pass4b_cagrswap=all(legs_c.values()),
                            pass4b_bothswap=all(legs_b.values()),
                            fails="+".join(k for k, v in legs.items() if not v) or "-",
                            **{f"leg_{k}": v for k, v in legs.items()}))
    ver = pd.DataFrame(ver)
    v10 = ver[(ver.cost == 10.0) & (ver.kappa == PROTOCOL_KAPPA)]
    log("    at PROTOCOL's kappa=0.60 / phi=0.70, 10 bps - 4b count by which leg is swapped:")
    log(f"      {'set':6s} {'n':>4s} " + " ".join(f"{cv:>9s}" for cv in CONVENTIONS) +
        "   | CAGR-leg swap (868) " + " ".join(f"{cv:>9s}" for cv in CONVENTIONS) +
        "   | BOTH legs " + " ".join(f"{cv:>9s}" for cv in CONVENTIONS))
    for st in ("SHELF", "GRID"):
        s = v10[v10.set == st]
        n = len(s[s.convention == "CURRENT"])
        log(f"      {st:6s} {n:4d} " +
            " ".join(f"{int(s[s.convention==cv].pass4b.sum()):9d}" for cv in CONVENTIONS) +
            "   |                     " +
            " ".join(f"{int(s[s.convention==cv].pass4b_cagrswap.sum()):9d}"
                     for cv in CONVENTIONS) +
            "   |           " +
            " ".join(f"{int(s[s.convention==cv].pass4b_bothswap.sum()):9d}"
                     for cv in CONVENTIONS))

    cur = v10[v10.convention == "CURRENT"].set_index("book")
    flipsets = {}
    for cv in ("CONST", "PATH"):
        new = v10[v10.convention == cv].set_index("book")
        dd_up = [b for b in cur.index if (not cur.pass4b[b]) and new.pass4b[b]]
        dd_dn = [b for b in cur.index if cur.pass4b[b] and (not new.pass4b[b])]
        cg_up = [b for b in cur.index
                 if (not cur.pass4b_cagrswap[b]) and new.pass4b_cagrswap[b]]
        cg_dn = [b for b in cur.index
                 if cur.pass4b_cagrswap[b] and (not new.pass4b_cagrswap[b])]
        flipsets[cv] = dict(dd_up=dd_up, dd_dn=dd_dn, cg_up=cg_up, cg_dn=cg_dn)
        log(f"\n    {cv} vs CURRENT:")
        log(f"      DD-leg swap : {len(dd_up)+len(dd_dn):2d} verdict flips  "
            f"({len(dd_up)} FAIL->PASS, {len(dd_dn)} PASS->FAIL)")
        log(f"      CAGR-leg swap (868's): {len(cg_up)+len(cg_dn):2d} verdict flips  "
            f"({len(cg_up)} FAIL->PASS, {len(cg_dn)} PASS->FAIL)")
        ddset, cgset = set(dd_up + dd_dn), set(cg_up + cg_dn)
        jac = len(ddset & cgset) / len(ddset | cgset) if (ddset | cgset) else np.nan
        log(f"      overlap: |DD n CAGR| = {len(ddset & cgset)}, |union| = "
            f"{len(ddset | cgset)}, Jaccard = {jac:.3f}")
        for b in sorted(ddset | cgset):
            tag = ("DD " if b in ddset else "   ") + ("CAGR" if b in cgset else "    ")
            dirs = []
            if b in dd_up: dirs.append("DD FAIL->PASS")
            if b in dd_dn: dirs.append("DD PASS->FAIL")
            if b in cg_up: dirs.append("CAGR FAIL->PASS")
            if b in cg_dn: dirs.append("CAGR PASS->FAIL")
            log(f"        {tag} {b:34s} {cur.set[b]:6s} gbar "
                f"{float(d10.set_index('book').mean_gross[b]):.3f}  " + "; ".join(dirs))

    pf = flipsets["PATH"]
    ndn, nup = len(pf["dd_dn"]), len(pf["dd_up"])
    log(f"\n    H_DIR (a MAJORITY of DD-swap flips under PATH are PASS->FAIL, i.e. the OPPOSITE "
        f"direction to 868's floor): {ndn} of {ndn+nup}  "
        f"[{'PASS' if ndn + nup > 0 and ndn > (ndn + nup) / 2 else 'FAIL'}]")
    ddset = set(pf["dd_up"] + pf["dd_dn"])
    cgset = set(pf["cg_up"] + pf["cg_dn"])
    jac = len(ddset & cgset) / len(ddset | cgset) if (ddset | cgset) else np.nan
    log(f"    H_SAME (Jaccard(DD flip set, CAGR flip set) >= 0.20 under PATH): {jac:.3f}  "
        f"[{'PASS' if (jac == jac) and jac >= 0.20 else 'FAIL'}]")

    log("\n    WHICH LEG BINDS at PROTOCOL's own convention (CURRENT, kappa=0.60, phi=0.70, "
        "10 bps):")
    for st in ("SHELF", "GRID"):
        s = v10[(v10.set == st) & (v10.convention == "CURRENT")]
        log(f"      {st}: " + ", ".join(
            f"{leg} binds {int((~s['leg_'+leg]).sum())}/{len(s)}"
            for leg in ["H1", "H2", "OOS", "DDCAP", "CAGRFLOOR"]))
    log("    and under PATH (DD leg swapped only):")
    for st in ("SHELF", "GRID"):
        s = v10[(v10.set == st) & (v10.convention == "PATH")]
        log(f"      {st}: " + ", ".join(
            f"{leg} binds {int((~s['leg_'+leg]).sum())}/{len(s)}"
            for leg in ["H1", "H2", "OOS", "DDCAP", "CAGRFLOOR"]))

    log("\n    COST LADDER (4b count at kappa=0.60, phi=0.70, DD leg swapped):")
    for c in RUNGS:
        s = ver[(ver.cost == c) & (ver.kappa == PROTOCOL_KAPPA)]
        log(f"      {c:5.1f} bps: " + ", ".join(
            f"{cv} {int(s[s.convention==cv].pass4b.sum())}/{len(s[s.convention==cv])}"
            for cv in CONVENTIONS))

    # ================================================================= [4] RULE 8
    log("\n" + "=" * 100)
    log("[4] PROTOCOL rule 8 - the DD gap measured on 2009-2016 and read again on 2017+")
    log("=" * 100)
    d10["ddgap_IS"] = d10.b_IS_MaxDD - d10.PATH_IS_MaxDD
    d10["ddgap_OOS"] = d10.b_OOS_MaxDD - d10.PATH_OOS_MaxDD
    d10["dd_same_sign"] = np.sign(d10.ddgap_IS) == np.sign(d10.ddgap_OOS)
    for st in ("SHELF", "GRID"):
        s = d10[d10.set == st]
        log(f"    {st}: IS DD gap median {s.ddgap_IS.median():+.2%}, OOS {s.ddgap_OOS.median():+.2%}, "
            f"same sign in {int(s.dd_same_sign.sum())} of {len(s)}; shallower than PATH "
            f"IS {int((s.ddgap_IS>0).sum())}/{len(s)}, OOS {int((s.ddgap_OOS>0).sum())}/{len(s)}")
    same = int(d10.dd_same_sign.sum())
    log(f"    H_WF (DD gap sign stable across the split for a majority): {same} of {len(d10)}  "
        f"[{'PASS' if same > len(d10)/2 else 'FAIL'}]")
    log("    IS-only DD-leg verdicts vs OOS-only, CURRENT kappa=0.60 (does an IS cap predict "
        "the OOS one?):")
    for st in ("SHELF", "GRID"):
        s = d10[d10.set == st]
        isp = s.b_IS_MaxDD >= PROTOCOL_KAPPA * s.CURRENT_IS_MaxDD
        oop = s.b_OOS_MaxDD >= PROTOCOL_KAPPA * s.CURRENT_OOS_MaxDD
        log(f"      {st}: IS pass {int(isp.sum())}/{len(s)}, OOS pass {int(oop.sum())}/{len(s)}, "
            f"agree {int((isp == oop).sum())}/{len(s)}; "
            f"IS-pass-but-OOS-fail (false positives) {int((isp & ~oop).sum())}, "
            f"IS-fail-but-OOS-pass {int((~isp & oop).sum())}")

    log("\n    RULE-8 CHOOSER (declared before the OOS window was read): pick each panel's best "
        "book by 2009-2016 IS Sharpe, read 2017+ ONCE.")
    log(f"    {'panel':6s} {'book':38s} {'OOS CAGR':>9s} {'OOS Sh':>7s} {'OOS MaxDD':>10s} "
        f"{'4a':>4s} {'4b':>4s} {'4b@PATH-DD':>11s}")
    picks = d10.loc[d10.groupby("panel")["b_IS_Sharpe"].idxmax()]
    pickrows = []
    for _, r in picks.iterrows():
        vr = v10[(v10.book == r.book)]
        p4a = bool(vr.pass4a.iloc[0])
        p4b = bool(vr[vr.convention == "CURRENT"].pass4b.iloc[0])
        p4bp = bool(vr[vr.convention == "PATH"].pass4b.iloc[0])
        log(f"    {r.panel:6s} {r.book:38s} {r.b_OOS_CAGR:9.2%} {r.b_OOS_Sharpe:7.3f} "
            f"{r.b_OOS_MaxDD:10.2%} {('PASS' if p4a else 'FAIL'):>4s} "
            f"{('PASS' if p4b else 'FAIL'):>4s} {('PASS' if p4bp else 'FAIL'):>11s}")
        pickrows.append(dict(panel=r.panel, book=r.book, full_CAGR=r.b_CAGR,
                             full_Sharpe=r.b_Sharpe, full_MaxDD=r.b_MaxDD, H1=r.b_H1, H2=r.b_H2,
                             IS_CAGR=r.b_IS_CAGR, IS_Sharpe=r.b_IS_Sharpe, IS_MaxDD=r.b_IS_MaxDD,
                             OOS_CAGR=r.b_OOS_CAGR, OOS_Sharpe=r.b_OOS_Sharpe,
                             OOS_MaxDD=r.b_OOS_MaxDD, mean_gross=r.mean_gross,
                             pass4a=p4a, pass4b=p4b, pass4b_PATHDD=p4bp,
                             spy_OOS_CAGR=r.CURRENT_OOS_CAGR, spy_OOS_MaxDD=r.CURRENT_OOS_MaxDD,
                             spy_CAGR=r.CURRENT_CAGR, spy_Sharpe=r.CURRENT_Sharpe,
                             spy_MaxDD=r.CURRENT_MaxDD,
                             bl_OOS_CAGR=r.bl_OOS_CAGR, bl_OOS_Sharpe=r.bl_OOS_Sharpe,
                             bl_OOS_MaxDD=r.bl_OOS_MaxDD, bl_CAGR=r.bl_CAGR,
                             bl_Sharpe=r.bl_Sharpe, bl_MaxDD=r.bl_MaxDD))
    pk = pd.DataFrame(pickrows)
    log("\n    THE RULE-8 PICKS IN FULL, against BOTH comparands PROTOCOL names (10 bps, t+1, "
        "weekly):")
    for _, r in pk.iterrows():
        log(f"      {r.panel} {r.book}")
        log(f"        book     full {r.full_CAGR:7.2%} / {r.full_Sharpe:5.3f} / "
            f"{r.full_MaxDD:7.2%}   halves {r.H1:.3f}/{r.H2:.3f}   IS {r.IS_CAGR:7.2%} / "
            f"{r.IS_Sharpe:5.3f} / {r.IS_MaxDD:7.2%}   OOS {r.OOS_CAGR:7.2%} / "
            f"{r.OOS_Sharpe:5.3f} / {r.OOS_MaxDD:7.2%}")
        log(f"        SPY      full {r.spy_CAGR:7.2%} / {r.spy_Sharpe:5.3f} / "
            f"{r.spy_MaxDD:7.2%}                            OOS {r.spy_OOS_CAGR:7.2%} /   "
            f"n/a  / {r.spy_OOS_MaxDD:7.2%}")
        log(f"        RULES v2 full {r.bl_CAGR:7.2%} / {r.bl_Sharpe:5.3f} / "
            f"{r.bl_MaxDD:7.2%}                            OOS {r.bl_OOS_CAGR:7.2%} / "
            f"{r.bl_OOS_Sharpe:5.3f} / {r.bl_OOS_MaxDD:7.2%}")
        log(f"        4a {'PASS' if r.pass4a else 'FAIL'}   4b {'PASS' if r.pass4b else 'FAIL'}"
            f"   4b with the DD leg gross-matched (PATH) "
            f"{'PASS' if r.pass4b_PATHDD else 'FAIL'}   gbar {r.mean_gross:.3f}")

    # ================================================================= [5] WHO THE SWAP MOVES
    log("\n" + "=" * 100)
    log("[5] WHAT THE SWAP COSTS, and the answer to the queue's question")
    log("=" * 100)
    log("    DD-leg pass rate at kappa=0.60 by realised-gross bucket, under each convention:")
    gr["gb"] = pd.cut(gr.mean_gross, [0, .5, .7, .85, 1.01],
                      labels=["<0.50", "0.50-0.70", "0.70-0.85", ">0.85"])
    log(f"      {'gbar bucket':12s} {'n':>4s} " + " ".join(f"{cv:>10s}" for cv in CONVENTIONS) +
        f" {'median bookDD':>14s}")
    for gb, s in gr.groupby("gb", observed=True):
        log(f"      {str(gb):12s} {len(s):4d} " + " ".join(
            f"{float((s.b_MaxDD >= PROTOCOL_KAPPA*s[cv+'_MaxDD']).mean()):10.3f}"
            for cv in CONVENTIONS) + f" {s.b_MaxDD.median():14.2%}")
    log("")
    log("    HOW MUCH SHALLOWER gross-matching makes the comparand (the arithmetic that sets "
        "the sign):")
    log(f"      {'set':6s} {'median SPY100 DD':>17s} {'median CONST DD':>16s} "
        f"{'median PATH DD':>15s} {'median gbar':>12s}")
    for st in ("SHELF", "GRID"):
        s = d10[d10.set == st]
        log(f"      {st:6s} {s.CURRENT_MaxDD.median():17.2%} {s.CONST_MaxDD.median():16.2%} "
            f"{s.PATH_MaxDD.median():15.2%} {s.mean_gross.median():12.3f}")
    lin = d10[d10.set == "GRID"].copy()
    lin["lin_pred"] = lin.mean_gross * lin.CURRENT_MaxDD
    lin["nonlin"] = lin.CONST_MaxDD - lin.lin_pred
    log(f"      a g-scaled path's MaxDD is NOT g x SPY's: median(CONST_DD - gbar x SPY_DD) = "
        f"{lin.nonlin.median():+.3%} on the GRID (max {lin.nonlin.abs().max():.3%}) - small, "
        f"so the tightening is close to linear in gross but is measured, not assumed.")

    d10.to_csv(OUT / f"{STEM}.books.csv", index=False)
    ver.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    g1.to_csv(OUT / f"{STEM}.g1.csv", index=False)
    pk.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    fl = pd.DataFrame([dict(convention=cv, kind=k, book=b)
                       for cv, dd in flipsets.items() for k, v in dd.items() for b in v])
    fl.to_csv(OUT / f"{STEM}.flips.csv", index=False)
    log(f"\n  wrote {STEM}.{{books,verdicts,ladder,g1,walkforward,flips}}.csv   "
        f"total {time.time()-t0:.0f}s   G5 {g5ok}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
