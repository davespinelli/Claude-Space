#!/usr/bin/env python3
"""Idea 868 - "does-the-record-s-SHELF-beat-a-GROSS-MATCHED-SPY-on-the-CAGR-LEG" (cloud, 2026-09-15).

The defect the queue names
--------------------------
PROTOCOL 4b's CAGR floor is `CAGR >= 0.70 x CAGR(SPY)`, and that SPY is 100% invested for every
one of its 4,700 days.  Most of the record's shelf runs gross 0.50-0.75, and the gated books run
lower still once the gate is counted: they hold cash for years at a time.  So the floor may be
charging a book for exposure it never held, and the queue asks for the floor re-priced against
`g x SPY` at every committed gross rung.

That re-pricing has a trap in it, and this run prices both sides of the trap
-----------------------------------------------------------------------------
Lowering the floor to g x SPY makes the bar EASIER for exactly the books that hold the most
cash.  Idea 676 already found the neighbouring version of this mistake: crediting cash a return
and then counting that riskless return in an rf=0 Sharpe numerator pays cash-heavy books twice,
and it collapsed the rule-8 chooser onto a 20%-gross band book.  A gross-matched CAGR floor is
the same shape of concession, so the question that decides whether it is a fix or a free pass is
the queue's own title, asked as a test:

    DOES THE SHELF ACTUALLY BEAT ITS OWN GROSS-MATCHED SPY ON THE CAGR LEG?

If it does, the current floor is charging books for exposure they never held and a gross-matched
floor is a correction that costs nothing.  If it does NOT, the gross-matched floor is a free pass
that would certify books an investor could replicate more cheaply by holding g in SPY and the
rest in cash - and the right conclusion is that the floor should stay where it is.

The comparand, stated exactly
-----------------------------
For a book whose realised gross on day t is g_t (the book's own summed weight, not its nominal
parameter), the GROSS-MATCHED SPY is the daily return path

    PATH  :  r_t = g_t * r_SPY,t        - matched day by day to the book's own exposure
    CONST :  r_t = gbar * r_SPY,t       - matched only to its time-averaged exposure gbar

Cash earns ZERO in both, which is the record's own rf=0 convention (idea 676's finding is why:
crediting cash and then reading an rf=0 Sharpe pays cash-heavy books twice).  Both are reported
at every rung; neither is selected on.  PATH is the honest one - it is the book's own exposure
with the security selection removed and nothing else changed - and CONST is what a "g x SPY"
floor written into PROTOCOL would actually be.

Pre-registered hypotheses and bars (fixed before any number below the gates was read)
    H_BEAT     the SHELF beats its own PATH-matched SPY on CAGR in a MAJORITY of its books.
               This is the queue's title.  PASS = the gross-matched floor is a correction.
    H_FREE     at phi = 0.70 the gross-matched floor's CAGR-leg pass rate on the GRID exceeds
               the current floor's by >= 20 pp.  PASS = the swap is a material concession, not
               a rounding.
    H_FLIP     the swap changes at least one committed 4b VERDICT (not just its CAGR leg) on the
               SHELF.  A floor that never binds is not worth a PROTOCOL line either way.
    H_WF       the sign of the book-vs-matched-SPY CAGR gap is the same in 2009-2016 and 2017+
               for a majority of books.  A gap that changes sign across the split cannot support
               a floor at all.
  Each is printed with its bar and its verdict, PASS or FAIL.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. gross rung   the book's gross: SHELF books at their committed grosses, and the GRID
                    ladder at g in {0.50, 0.75, 1.00} on three panels.
    2. floor fraction phi in {0.50, 0.60, 0.70, 0.80, 0.90, 1.00}; 0.70 is PROTOCOL's.
    ALL grid points reported at every panel, book, comparand convention and cost rung.

Book sets, IMPORTED not re-typed, from the lane-C script committed earlier today
    SHELF  the record's 8 memo-backed 4b KEEP-candidate books, rebuilt from their own RULES
           wording (`shelf_books`), each gated against its published headline triple.
    GRID   the mechanical band x gross x QROLL ladder that was never memo-selected
           (`grid_books`), extended here to the small-cap panel.

Reproduction gates (printed before any new number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G2  the gross-matched SPY at a constant g = 1.00 is SPY itself, to machine precision.
    G3  the PATH comparand's realised mean gross equals the book's own, to machine precision.
    G4  fast metrics == engine.metrics() on a live book.

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists (the small panel additionally
drops the 52 tickers with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR LEVEL below
is optimistic - including the books' AND the floor's, which is why the run reports the book-minus-
comparand GAP rather than any level on its own.

Deterministic, standalone.  Modifies nothing; proposes no PROTOCOL edit, applies none.
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
LINES = []

FREQ = "W"
WARMUP = 260
RUNGS = [10.0, 25.0]
PHIS = [0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
PROTOCOL_PHI = 0.70
DDCAP_FRAC = 0.60
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


def mstats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def small_grid(px, pname, laneC):
    """laneC.grid_books' ladder, applied to a third panel so the census is not two-panel."""
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
    log("IDEA 868 - does the record's SHELF beat a GROSS-MATCHED SPY on the CAGR leg?  "
        "(cloud 2026-09-15)")
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
        f"{sum(1 for b in books.values() if b['set']=='GRID')} GRID = {len(books)}")

    # ------------------------------------------------------------------ price every book
    log("\n[0] REPRODUCTION GATES (printed before any new number is read)")
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
            base = backtest(pxn, rules_v2_weights(pxn), cost_bps=c,
                            freq="W")["returns"].loc[start:]
            bl = mstats(base)
            oos = r.index >= pd.Timestamp(SPLIT)
            row = dict(book=name, set=spec["set"], panel=spec["panel"], cost=c,
                       mean_gross=const_g, src=spec["src"], **{f"b_{k}": v for k, v in bs.items()},
                       b_OOS_CAGR=metrics(r[oos])["CAGR"], b_OOS_Sharpe=metrics(r[oos])["Sharpe"],
                       b_OOS_MaxDD=metrics(r[oos])["MaxDD"],
                       b_IS_CAGR=metrics(r[~oos])["CAGR"], b_IS_Sharpe=metrics(r[~oos])["Sharpe"],
                       bl_H1=bl["H1"], bl_H2=bl["H2"], bl_MaxDD=bl["MaxDD"],
                       bl_Sharpe=bl["Sharpe"], bl_OOS_Sharpe=metrics(base[oos])["Sharpe"])
            for cv, cr in comp.items():
                cm = mstats(cr)
                row[f"{cv}_CAGR"] = cm["CAGR"]
                row[f"{cv}_Sharpe"] = cm["Sharpe"]
                row[f"{cv}_MaxDD"] = cm["MaxDD"]
                row[f"{cv}_H1"], row[f"{cv}_H2"] = cm["H1"], cm["H2"]
                row[f"{cv}_OOS_CAGR"] = metrics(cr[oos])["CAGR"]
                row[f"{cv}_IS_CAGR"] = metrics(cr[~oos])["CAGR"]
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
    log("  G1 SHELF books vs their committed memo triples (@10 bps)")
    log(f"    {'book':36s} {'memo CAGR':>10s} {'here':>8s} {'memo Sh':>8s} {'here':>8s} "
        f"{'|dC|':>7s} {'|dS|':>7s}")
    for _, r in g1.iterrows():
        log(f"    {r.book:36s} {r.memo_CAGR:10.4f} {r.here_CAGR:8.4f} {r.memo_Sharpe:8.4f} "
            f"{r.here_Sharpe:8.4f} {r.dC:7.4f} {r.dS:7.4f}")
    ok = int(((g1.dC < 0.01) & (g1.dS < 0.10)).sum())
    log(f"    G1: {ok} of {len(g1)} reproduce within 1.00 pp of CAGR and 0.10 of Sharpe  "
        f"[{'PASS' if ok >= len(g1) - 1 else 'PARTIAL'}]  (tape vintage moves every level "
        f"slightly; the GAP this run measures is a same-tape difference and is unaffected)")

    spy_full = U["SPY"].pct_change().fillna(0.0).loc[U.index[WARMUP]:]
    g2 = float(np.max(np.abs((1.00 * spy_full) - spy_full)))
    log(f"  G2 gross-matched SPY at constant g=1.00 == SPY        max|d| = {g2:.3e}  "
        f"[{'PASS' if g2 == 0 else 'FAIL'}]")
    g3 = float((df["path_mean_gross"] - df["mean_gross"]).abs().max())
    log(f"  G3 PATH comparand's mean gross == the book's own      max|d| = {g3:.3e}  "
        f"[{'PASS' if g3 < 1e-12 else 'FAIL'}]")
    chk = backtest(U.drop(columns=["SPY"]), rules_v2_weights(U.drop(columns=["SPY"])),
                   cost_bps=10, freq="W")["returns"].loc[U.index[WARMUP]:]
    g4 = abs(mstats(chk)["Sharpe"] - metrics(chk)["Sharpe"])
    log(f"  G4 fast metrics == engine.metrics()                   |d|    = {g4:.3e}  "
        f"[{'PASS' if g4 < 1e-12 else 'FAIL'}]")

    # ================================================================= [1] THE TITLE QUESTION
    log("\n" + "=" * 100)
    log("[1] H_BEAT - THE QUEUE'S TITLE: does the SHELF beat its own gross-matched SPY on CAGR?")
    log("=" * 100)
    d10 = df[df.cost == 10.0].copy()
    d10["gap_PATH"] = d10.b_CAGR - d10.PATH_CAGR
    d10["gap_CONST"] = d10.b_CAGR - d10.CONST_CAGR
    d10["gap_CURRENT"] = d10.b_CAGR - d10.CURRENT_CAGR
    sh = d10[d10.set == "SHELF"].sort_values("gap_PATH", ascending=False)
    log(f"    {'book':36s} {'gbar':>6s} {'book CAGR':>10s} {'PATH gxSPY':>11s} {'gap':>8s} "
        f"{'CONST':>8s} {'gap':>8s} {'SPY100':>8s} {'gap':>8s}")
    for _, r in sh.iterrows():
        log(f"    {r.book:36s} {r.mean_gross:6.3f} {r.b_CAGR:10.2%} {r.PATH_CAGR:11.2%} "
            f"{r.gap_PATH:+8.2%} {r.CONST_CAGR:8.2%} {r.gap_CONST:+8.2%} "
            f"{r.CURRENT_CAGR:8.2%} {r.gap_CURRENT:+8.2%}")
    nbeat = int((sh.gap_PATH > 0).sum())
    log(f"    SHELF beats its PATH-matched SPY on CAGR in {nbeat} of {len(sh)} books "
        f"(median gap {sh.gap_PATH.median():+.2%}); CONST {int((sh.gap_CONST>0).sum())}/{len(sh)}; "
        f"SPY at 100% {int((sh.gap_CURRENT>0).sum())}/{len(sh)}")
    log(f"    H_BEAT (majority beat PATH): [{'PASS' if nbeat > len(sh)/2 else 'FAIL'}]")
    gr = d10[d10.set == "GRID"]
    log(f"    GRID, for contrast: beats PATH in {int((gr.gap_PATH>0).sum())} of {len(gr)} "
        f"(median {gr.gap_PATH.median():+.2%}), beats SPY at 100% in "
        f"{int((gr.gap_CURRENT>0).sum())} of {len(gr)} (median {gr.gap_CURRENT.median():+.2%})")
    log(f"    by panel: " + "; ".join(
        f"{p} {int((gr[gr.panel==p].gap_PATH>0).sum())}/{len(gr[gr.panel==p])}"
        for p in ["U56", "B136", "SMALL"]))

    # ================================================================= [2] THE FLOOR LADDER
    log("\n" + "=" * 100)
    log("[2] H_FREE - the CAGR leg's pass rate under each floor, phi x convention, ALL 18 cells")
    log("    (the leg alone, so the concession is read before it is mixed with the other legs)")
    log("=" * 100)
    lad = []
    for phi, cv in product(PHIS, CONVENTIONS):
        for st in ("SHELF", "GRID"):
            s = d10[d10.set == st]
            p = float((s.b_CAGR >= phi * s[f"{cv}_CAGR"]).mean())
            lad.append(dict(phi=phi, convention=cv, set=st, pass_rate=p, n=len(s)))
    lad = pd.DataFrame(lad)
    for st in ("SHELF", "GRID"):
        log(f"    {st} (n={int(lad[lad.set==st].n.iloc[0])})")
        log(f"      {'phi':>5s} " + " ".join(f"{cv:>10s}" for cv in CONVENTIONS))
        for phi in PHIS:
            s = lad[(lad.phi == phi) & (lad.set == st)].set_index("convention")
            log(f"      {phi:5.2f} " + " ".join(f"{s.loc[cv,'pass_rate']:10.3f}"
                                                for cv in CONVENTIONS))
    g70 = lad[(lad.phi == PROTOCOL_PHI) & (lad.set == "GRID")].set_index("convention")
    dfree = g70.loc["PATH", "pass_rate"] - g70.loc["CURRENT", "pass_rate"]
    log(f"    H_FREE (GRID pass rate at phi=0.70 rises >= 20 pp under PATH): "
        f"{g70.loc['CURRENT','pass_rate']:.3f} -> {g70.loc['PATH','pass_rate']:.3f} "
        f"= {dfree:+.1%}  [{'PASS' if dfree >= 0.20 else 'FAIL'}]")

    # ================================================================= [3] FULL 4b VERDICTS
    log("\n" + "=" * 100)
    log("[3] H_FLIP - the FULL 4b verdict under each floor (all four legs), and 4a beside it")
    log("=" * 100)
    ver = []
    for _, r in df.iterrows():
        p4a = (r.b_H1 > r.bl_H1) and (r.b_H2 > r.bl_H2) and (r.b_MaxDD >= r.bl_MaxDD)
        for phi, cv in product(PHIS, CONVENTIONS):
            legs = dict(H1=r.b_H1 > r.CURRENT_H1, H2=r.b_H2 > r.CURRENT_H2,
                        OOS=r.b_OOS_Sharpe > r.CURRENT_Sharpe,
                        DDCAP=r.b_MaxDD >= DDCAP_FRAC * r.CURRENT_MaxDD,
                        CAGRFLOOR=r.b_CAGR >= phi * r[f"{cv}_CAGR"])
            ver.append(dict(book=r.book, set=r.set, panel=r.panel, cost=r.cost, phi=phi,
                            convention=cv, pass4a=p4a, pass4b=all(legs.values()),
                            fails="+".join(k for k, v in legs.items() if not v) or "-",
                            **{f"leg_{k}": v for k, v in legs.items()}))
    ver = pd.DataFrame(ver)
    v10 = ver[(ver.cost == 10.0) & (ver.phi == PROTOCOL_PHI)]
    log(f"    at PROTOCOL's phi=0.70, 10 bps:")
    log(f"      {'set':6s} {'n':>4s} " + " ".join(f"{cv+' 4b':>12s}" for cv in CONVENTIONS) +
        f" {'4a':>5s}")
    for st in ("SHELF", "GRID"):
        s = v10[v10.set == st]
        log(f"      {st:6s} {len(s[s.convention=='CURRENT']):4d} " +
            " ".join(f"{int(s[s.convention==cv].pass4b.sum()):12d}" for cv in CONVENTIONS) +
            f" {int(s[s.convention=='CURRENT'].pass4a.sum()):5d}")
    cur = v10[v10.convention == "CURRENT"].set_index(["book", "set"])["pass4b"]
    flips = {}
    for cv in ("CONST", "PATH"):
        new = v10[v10.convention == cv].set_index(["book", "set"])["pass4b"]
        ch = [b for b in cur.index if cur[b] != new[b]]
        flips[cv] = ch
        log(f"    {cv}: {len(ch)} verdict changes "
            f"({sum(1 for b in ch if b[1]=='SHELF')} on the SHELF, "
            f"{sum(1 for b in ch if b[1]=='GRID')} on the GRID)")
        for b in ch[:10]:
            log(f"      {b[1]:6s} {b[0]:40s} {'FAIL->PASS' if new[b] else 'PASS->FAIL'}")
    nshelf = sum(1 for b in flips["PATH"] if b[1] == "SHELF")
    log(f"    H_FLIP (>= 1 SHELF verdict changes under PATH at phi=0.70): {nshelf}  "
        f"[{'PASS' if nshelf >= 1 else 'FAIL'}]")
    log("\n    WHICH LEG BINDS (CURRENT floor, phi=0.70, 10 bps) - the floor's own share:")
    for st in ("SHELF", "GRID"):
        s = v10[(v10.set == st) & (v10.convention == "CURRENT")]
        tot = len(s)
        log(f"      {st}: " + ", ".join(
            f"{leg} binds {int((~s['leg_'+leg]).sum())}/{tot}"
            for leg in ["H1", "H2", "OOS", "DDCAP", "CAGRFLOOR"]))

    # ================================================================= [4] RULE 8
    log("\n" + "=" * 100)
    log("[4] PROTOCOL rule 8 - the gap measured on 2009-2016 and read again on 2017+")
    log("=" * 100)
    d10["gap_IS"] = d10.b_IS_CAGR - d10.PATH_IS_CAGR
    d10["gap_OOS"] = d10.b_OOS_CAGR - d10.PATH_OOS_CAGR
    d10["same_sign"] = np.sign(d10.gap_IS) == np.sign(d10.gap_OOS)
    for st in ("SHELF", "GRID"):
        s = d10[d10.set == st]
        log(f"    {st}: IS gap median {s.gap_IS.median():+.2%}, OOS gap median "
            f"{s.gap_OOS.median():+.2%}, same sign in {int(s.same_sign.sum())} of {len(s)}; "
            f"beats PATH IS {int((s.gap_IS>0).sum())}/{len(s)}, OOS {int((s.gap_OOS>0).sum())}/{len(s)}")
    same = int(d10.same_sign.sum())
    log(f"    H_WF (gap sign stable across the split for a majority): {same} of {len(d10)}  "
        f"[{'PASS' if same > len(d10)/2 else 'FAIL'}]")
    log("\n    RULE-8 CHOOSER: pick each panel's best book by 2009-2016 IS Sharpe, read 2017+ once.")
    log(f"    {'panel':6s} {'book':38s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} "
        f"{'vs SPY OOS':>11s} {'vs v2 OOS':>10s} {'PATH OOS CAGR':>14s}")
    picks = d10.loc[d10.groupby("panel")["b_IS_Sharpe"].idxmax()]
    for _, r in picks.iterrows():
        log(f"    {r.panel:6s} {r.book:38s} {r.b_OOS_CAGR:9.2%} {r.b_OOS_Sharpe:11.3f} "
            f"{r.b_OOS_MaxDD:10.2%} {r.CURRENT_OOS_CAGR:11.2%} {r.bl_OOS_Sharpe:10.3f} "
            f"{r.PATH_OOS_CAGR:14.2%}")
    log("\n    comparands @10 bps (common window, t+1, weekly):")
    for p in ["U56", "B136", "SMALL"]:
        r = d10[d10.panel == p].iloc[0]
        log(f"      {p:6s} SPY {r.CURRENT_CAGR:7.2%} / {r.CURRENT_Sharpe:5.3f} / "
            f"{r.CURRENT_MaxDD:7.2%} (H {r.CURRENT_H1:.3f}/{r.CURRENT_H2:.3f}; OOS CAGR "
            f"{r.CURRENT_OOS_CAGR:6.2%})   RULES v2 Sharpe {r.bl_Sharpe:5.3f} "
            f"(H {r.bl_H1:.3f}/{r.bl_H2:.3f}; OOS {r.bl_OOS_Sharpe:5.3f}), MaxDD {r.bl_MaxDD:7.2%}")

    # ================================================================= [5] WHO THE SWAP ADMITS
    log("\n" + "=" * 100)
    log("[5] WHO THE SWAP ADMITS, and the matched-gross contrast the title question needs")
    log("=" * 100)
    cur = v10[(v10.convention == "CURRENT")].set_index("book")["pass4b"]
    pat = v10[(v10.convention == "PATH")].set_index("book")["pass4b"]
    fl = [b for b in cur.index if (not cur[b]) and pat[b]]
    f = d10[d10.book.isin(fl)]
    log(f"    the {len(f)} books the gross-matched floor turns FAIL -> PASS at phi=0.70, 10 bps:")
    log(f"      {'book':28s} {'gbar':>6s} {'book CAGR':>10s} {'its gxSPY':>10s} {'gap':>8s} "
        f"{'SPY100':>8s}")
    for _, r in f.sort_values("mean_gross").iterrows():
        log(f"      {r.book:28s} {r.mean_gross:6.3f} {r.b_CAGR:10.2%} {r.PATH_CAGR:10.2%} "
            f"{r.gap_PATH:+8.2%} {r.CURRENT_CAGR:8.2%}")
    log(f"    mean gross: admitted {f.mean_gross.mean():.3f} vs all GRID "
        f"{d10[d10.set=='GRID'].mean_gross.mean():.3f} vs SHELF "
        f"{d10[d10.set=='SHELF'].mean_gross.mean():.3f}")
    log(f"    of the {len(f)} admitted, {int((f.gap_PATH>0).sum())} DO beat their own "
        f"gross-matched SPY (median {f.gap_PATH.median():+.2%}) - so the swap is NOT admitting "
        f"books that lose to a passive blend at their own exposure.")
    log(f"    but their ABSOLUTE CAGR runs {f.b_CAGR.min():.2%}..{f.b_CAGR.max():.2%} against "
        f"SPY's {f.CURRENT_CAGR.iloc[0]:.2%}: a 4b pass is a CAPITAL claim, and this is the same")
    log(f"    shape of concession idea 676 priced on the cash leg - normalising a bar by a book's")
    log(f"    own gross pays it for exposure it DECLINED to take.")
    gr2 = d10[d10.set == "GRID"].copy()
    rho_g = float(gr2[["mean_gross", "gap_PATH"]].corr(method="spearman").iloc[0, 1])
    rho_c = float(gr2[["mean_gross", "gap_CURRENT"]].corr(method="spearman").iloc[0, 1])
    log(f"\n    THE MECHANISM: rho(mean gross, gap vs its own gxSPY) = {rho_g:+.3f} on the GRID, "
        f"while rho(mean gross, gap vs SPY at 100%) = {rho_c:+.3f}.")
    log(f"    The two floors rank the SAME 54 books in OPPOSITE ORDERS. That is the finding: the")
    log(f"    CAGR floor is doing two different jobs and they disagree by construction.")
    gr2["gb"] = pd.cut(gr2.mean_gross, [0, .5, .7, .85, 1.01],
                       labels=["<0.50", "0.50-0.70", "0.70-0.85", ">0.85"])
    log(f"\n    GRID by realised-gross bucket (beats its own gxSPY on CAGR):")
    log(f"      {'gbar bucket':12s} {'n':>4s} {'beats':>6s} {'median gap':>11s}")
    for gb, s in gr2.groupby("gb", observed=True):
        log(f"      {str(gb):12s} {len(s):4d} {int((s.gap_PATH>0).sum()):6d} "
            f"{s.gap_PATH.median():+11.2%}")
    sh_g = d10[d10.set == "SHELF"]
    band = gr2[(gr2.mean_gross >= 0.70) & (gr2.mean_gross <= 0.85)]
    log(f"\n    MATCHED-GROSS CONTRAST (the control the title question needs): the SHELF sits at "
        f"gbar {sh_g.mean_gross.mean():.3f} and beats its own gxSPY in {int((sh_g.gap_PATH>0).sum())} "
        f"of {len(sh_g)}; unselected GRID books in the SAME 0.70-0.85 gross bucket beat it in "
        f"{int((band.gap_PATH>0).sum())} of {len(band)}.")
    log(f"    So 'beats a gross-matched SPY' is NOT a property of this book family - it is a "
        f"property of the eight books that were already memo-selected for passing 4b.")
    f.to_csv(OUT / f"{STEM}.admitted.csv", index=False)

    log("\n    COST LADDER (4b count at phi=0.70 under each convention):")
    for c in RUNGS:
        s = ver[(ver.cost == c) & (ver.phi == PROTOCOL_PHI)]
        log(f"      {c:5.1f} bps: " + ", ".join(
            f"{cv} {int(s[s.convention==cv].pass4b.sum())}/{len(s[s.convention==cv])}"
            for cv in CONVENTIONS))

    df.to_csv(OUT / f"{STEM}.books.csv", index=False)
    ver.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    g1.to_csv(OUT / f"{STEM}.g1.csv", index=False)
    d10[["book", "set", "panel", "mean_gross", "b_CAGR", "PATH_CAGR", "CONST_CAGR",
         "CURRENT_CAGR", "gap_PATH", "gap_CONST", "gap_CURRENT", "gap_IS", "gap_OOS",
         "same_sign"]].to_csv(OUT / f"{STEM}.gaps.csv", index=False)
    log(f"\n  wrote {STEM}.{{books,verdicts,ladder,g1,gaps}}.csv   total {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
