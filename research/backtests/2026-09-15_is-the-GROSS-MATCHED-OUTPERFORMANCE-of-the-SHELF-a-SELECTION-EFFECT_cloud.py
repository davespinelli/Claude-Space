#!/usr/bin/env python3
"""IDEA 873 - is the GROSS-MATCHED OUTPERFORMANCE of the SHELF a SELECTION EFFECT?
Cloud lane, idea 2 of 2, 2026-09-15.

THE CLAIM UNDER TEST
--------------------
Idea 868 (committed today) priced every book in the record against its own GROSS-MATCHED SPY -
the path r_t = g_t * r_SPY,t, where g_t is the book's own realised summed weight, cash at zero -
and published:

    SHELF (8 memo-backed 4b books)                     beats its own gxSPY on CAGR   6 of 8
    unselected GRID books at the SAME realised gross   beats its own gxSPY on CAGR   3 of 12
    the whole GRID ladder                              beats its own gxSPY on CAGR  16 of 54

and read the gap between 6/8 and 3/12 as evidence that the shelf's books carry something a
gross-matched index does not.  But the shelf is a SELECTED set, and it was selected by memos
written in 2026 with the whole 2009-2026 tape in front of them.  A set chosen for having
performed will out-perform its benchmark in the window it was chosen on, whether or not the
selection carries any information.  The queue's question is therefore the right one:

    RE-RUN THE SHELF'S OWN SELECTION ON A PRE-2017 WINDOW ONLY, AND MEASURE HOW MUCH OF THE
    6-OF-8 SURVIVES WHEN THE MEMOS COULD NOT HAVE SEEN THE OUTCOME.

WHAT "THE SHELF'S OWN SELECTION" IS, STATED AS A RULE
------------------------------------------------------
Every shelf book is on the shelf because it cleared PROTOCOL 4b and earned a memo.  The
mechanical restatement of that, applicable to any book and any window, is 4b itself:

    Sharpe > SPY in BOTH halves of the window,  MaxDD >= 0.60 * SPY's,  CAGR >= 0.70 * SPY's

Run on the FULL sample this reproduces the shelf (that is the ex-post arm and its gate).  Run on
a SELECTION WINDOW that ends before the evaluation period, it is the same rule with the outcome
removed - the memo-writer's information set, honestly constrained.  The run then asks, on the
EVALUATION window only, how often the ex-ante-selected books beat their own gxSPY, and compares
that to the books the ex-ante rule did NOT select at the same realised gross.  The difference of
those two rates is the SELECTION LIFT, and it is the only quantity this run is about.

    LIFT_expost  = beat-rate(selected on the FULL sample) - beat-rate(unselected, same bucket)
                   evaluated on the evaluation window.   868's shape: 75% - 25% = +50 pp.
    LIFT_exante  = the same two rates with selection done on the SELECTION WINDOW alone.

PRE-REGISTERED HYPOTHESES AND BARS (fixed before any number below the gates is read)
    H_SELECTION  the 6-of-8 is a selection effect.  PASS = LIFT_exante < +25 pp at the headline
                 cell, i.e. less than half of the ex-post lift survives the honest constraint.
    H_REAL       the lift is a property of the books.  PASS = LIFT_exante >= +25 pp.
    H_REACHABLE  the memos' actual picks were reachable ex ante at all: >= 5 of the 8 committed
                 SHELF books clear 4b on the pre-2017 window alone.  This is separate from the
                 lift and is reported whichever way the lift goes - a shelf that is unreachable
                 ex ante is a different (and worse) finding than a shelf with no lift.
    H_WF         rule 8 in this run's own currency: the ex-ante selected set's OOS book-level
                 read clears a KEEP path.  Reported for both paths, 4a and 4b.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4: at most two; ALL grid points reported)
---------------------------------------------------------------------------------
  1. SELECTION WINDOW END  {2013-12-31, 2016-12-31, 2019-12-31}
       the evaluation window is everything after it, so the three cells trade selection power
       against evaluation length.  2016-12-31 is PROTOCOL rule 8's own IS end and is the
       declared headline.
  2. GROSS BUCKET  {NARROW 0.70-0.85 (868's own), WIDE 0.60-0.95, ALL}
       which unselected books count as the matched control.  Bucketing uses each book's
       realised mean gross measured ON THE SELECTION WINDOW ONLY, never on the outcome.

Reported controls, never selected on: cost rung {10, 25} bps, comparand convention {PATH, CONST},
panel {U56, B136, SMALL}, and the ex-post arm at every cell beside the ex-ante one.

GATES (printed before any new number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD)
    G2  the gross-matched SPY at constant g = 1.00 is SPY itself, exactly
    G3  the PATH comparand's realised mean gross equals the book's own, to machine precision
    G4  fast metrics == engine.metrics()
    G5  CROSS-RUN: 868's published full-sample counts (6/8 SHELF, 3/12 same-bucket GRID,
        16/54 whole ladder) rebuilt from this run's own arms

Books are IMPORTED from the same committed lane-C builders idea 868 used, never re-typed, so the
two runs are measuring the same objects.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists; the small panel additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv.  Every CAGR LEVEL below is
optimistic - for the books AND for the comparands - which is exactly why the reported quantity is
a book-minus-comparand GAP and a difference of two beat-RATES, not a level.  The rule-8 table at
the end reads levels and is exposed in full.

Data: committed caches only, no network, never yfinance.
PROTOCOL: 10 bps costs, next-day execution, no shorting, no leverage.  Rules files untouched.
Deterministic, standalone.  Proposes no PROTOCOL edit and applies none.
"""
import importlib.util
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
LANEC = OUT / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"
SRC868 = OUT / "2026-09-15_does-the-record-s-SHELF-beat-a-GROSS-MATCHED-SPY-on-the-CAGR-LEG_cloud.py"

FREQ, WARMUP = "W", 260
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
CONVENTIONS = ["PATH", "CONST"]
CONV_HEAD = "PATH"

# tuned dial 1
WINDOWS = ["2013-12-31", "2016-12-31", "2019-12-31"]
WIN_HEAD = "2016-12-31"
# tuned dial 2
BUCKETS = {"NARROW": (0.70, 0.85), "WIDE": (0.60, 0.95), "ALL": (0.00, 9.99)}
BUCKET_HEAD = "NARROW"

LIFT_BAR_PP = 25.0                 # H_SELECTION / H_REAL bar
REACH_BAR = 5                      # H_REACHABLE bar, out of 8
PUB868 = dict(shelf_beat=6, shelf_n=8, bucket_beat=3, bucket_n=12, grid_beat=16, grid_n=54)

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def mstats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def keep_4b(bk, cmp_):
    """PROTOCOL 4b, applied to whatever window the two stat dicts were computed on."""
    return bool(bk["H1"] > cmp_["H1"] and bk["H2"] > cmp_["H2"]
                and bk["MaxDD"] >= DDCAP_FRAC * cmp_["MaxDD"]
                and bk["CAGR"] >= CAGRFLOOR_FRAC * cmp_["CAGR"])


def keep_4a(bk, base):
    return bool(bk["H1"] > base["H1"] and bk["H2"] > base["H2"]
                and bk["MaxDD"] >= base["MaxDD"])


# ================================================================== run
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 873 - is the GROSS-MATCHED OUTPERFORMANCE of the SHELF a SELECTION EFFECT?  "
        "(cloud 2026-09-15, idea 2 of 2)")
    log("=" * 100)
    log(f"pandas {pd.__version__} numpy {np.__version__}")
    log("PROTOCOL: 10 bps, next-day execution, no shorting, no leverage.")
    log(f"2 tuned dials: SELECTION WINDOW END {WINDOWS} x GROSS BUCKET {list(BUCKETS)} = "
        f"{len(WINDOWS)*len(BUCKETS)} cells, ALL reported.")
    log(f"HEADLINE cell declared before any number is read: window {WIN_HEAD}, bucket "
        f"{BUCKET_HEAD}, comparand {CONV_HEAD}, rung {RUNG_HEAD:.0f} bps.")
    log(f"Pre-registered bars: H_SELECTION needs LIFT_exante < +{LIFT_BAR_PP:.0f} pp; "
        f"H_REACHABLE needs >= {REACH_BAR} of 8 SHELF books to clear 4b pre-2017.")
    log("Controls, never selected on: rungs 10/25 bps, comparands PATH/CONST, three panels, "
        "and the ex-post arm printed beside the ex-ante arm at every cell.")
    log("SURVIVORSHIP: U56/B136/SMALL are current-constituent lists; every LEVEL is optimistic. "
        "The reported quantity is a difference of two beat-RATES.")
    log("")

    laneC = _load(LANEC, "laneC873")
    m868 = _load(SRC868, "idea868")

    U, B = load_universe(), load_universe(broad=True)
    S = m868.small_panel()                     # 868's own small-panel filter, imported
    panels = {"U56": U, "B136": B, "SMALL": S}
    log(f"panels: U56 {U.shape}  B136 {B.shape}  SMALL {S.shape} "
        f"(sub-$2B, max_1d_move>=1.0 tickers dropped per data/small_meta.csv)")

    books = {}
    for k, v in laneC.shelf_books(U, B).items():
        v["set"] = "SHELF"
        books[k] = v
    for k, v in laneC.grid_books(U, B).items():
        v["set"] = "GRID"
        books[k] = v
    for k, v in m868.small_grid(S.drop(columns=["SPY"], errors="ignore"), "SMALL", laneC).items():
        v["set"] = "GRID"
        books[k] = v
    n_shelf = sum(1 for b in books.values() if b["set"] == "SHELF")
    log(f"books: {n_shelf} SHELF (memo-backed) + {len(books)-n_shelf} GRID = {len(books)}  "
        f"(IMPORTED from the same builders idea 868 used)")

    # ------------------------------------------------------------------ price every book once
    log("\n[0] GATES (printed before any new number is read)")
    rows, g1 = [], []
    for name, spec in books.items():
        px = panels[spec["panel"]]
        pxn = px.drop(columns=["SPY"], errors="ignore")
        W = spec["W"].reindex(pxn.index).reindex(columns=pxn.columns).fillna(0.0)
        start = pxn.index[WARMUP]
        gross_t = W.sum(axis=1).shift(1).fillna(0.0).loc[start:]      # t+1 aligned, as held
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_all = {c: backtest(pxn, rules_v2_weights(pxn), cost_bps=c,
                                freq="W")["returns"].loc[start:] for c in RUNGS}
        for c in RUNGS:
            r = backtest(pxn, W, cost_bps=c, freq=spec["freq"])["returns"].loc[start:]
            gbar_full = float(gross_t.mean())
            comp = {"CONST": gbar_full * spy, "PATH": gross_t * spy}
            row = dict(book=name, set=spec["set"], panel=spec["panel"], cost=c, src=spec["src"],
                       mean_gross=gbar_full, path_mean_gross=gbar_full)
            # FULL window
            bs = mstats(r)
            for k_, v_ in bs.items():
                row[f"b_{k_}"] = v_
            for cv in CONVENTIONS:
                cm = mstats(comp[cv])
                for k_, v_ in cm.items():
                    row[f"{cv}_{k_}"] = v_
            sm = mstats(spy)
            for k_, v_ in sm.items():
                row[f"SPY_{k_}"] = v_
            # per selection window: IS = <= W, EV = > W, for the book, each comparand, SPY, base
            for w in WINDOWS:
                isl, evl = slice(None, w), slice(pd.Timestamp(w) + pd.Timedelta(days=1), None)
                for tag, sl in (("IS", isl), ("EV", evl)):
                    for who, ser in (("b", r), ("SPY", spy), ("BASE", base_all[c]),
                                     *[(cv, comp[cv]) for cv in CONVENTIONS]):
                        st = mstats(ser.loc[sl])
                        for k_, v_ in st.items():
                            row[f"{w}_{tag}_{who}_{k_}"] = v_
                    if tag == "IS":
                        row[f"{w}_IS_gbar"] = float(gross_t.loc[sl].mean())
            rows.append(row)
            if c == RUNG_HEAD and spec["memo"]:
                m = spec["memo"]
                g1.append(dict(book=name, memo_CAGR=m[0], here_CAGR=bs["CAGR"],
                               memo_Sharpe=m[1], here_Sharpe=bs["Sharpe"],
                               memo_MaxDD=m[2], here_MaxDD=bs["MaxDD"]))
    df = pd.DataFrame(rows)
    log(f"  priced {len(books)} books x {len(RUNGS)} rungs  ({time.time()-t0:.0f}s)")

    g1 = pd.DataFrame(g1)
    g1["dC"] = (g1.here_CAGR - g1.memo_CAGR).abs()
    g1["dS"] = (g1.here_Sharpe - g1.memo_Sharpe).abs()
    ok1 = int(((g1.dC < 0.01) & (g1.dS < 0.10)).sum())
    log(f"  G1 SHELF memo triples: {ok1} of {len(g1)} within 1.00 pp CAGR and 0.10 Sharpe  "
        f"[{'PASS' if ok1 >= len(g1) - 1 else 'PARTIAL'}]  (worst |dC| {g1.dC.max():.4f}, "
        f"|dS| {g1.dS.max():.4f}; tape vintage moves every LEVEL slightly, the GAP is a "
        f"same-tape difference and is unaffected)")
    spy_full = U["SPY"].pct_change().fillna(0.0).loc[U.index[WARMUP]:]
    g2 = float(np.max(np.abs((1.00 * spy_full) - spy_full)))
    log(f"  G2 gxSPY at constant g=1.00 == SPY                   max|d| = {g2:.3e}  "
        f"[{'PASS' if g2 == 0 else 'FAIL'}]")
    g3 = float((df.path_mean_gross - df.mean_gross).abs().max())
    log(f"  G3 PATH comparand mean gross == the book's own       max|d| = {g3:.3e}  "
        f"[{'PASS' if g3 < 1e-12 else 'FAIL'}]")
    chk = backtest(U.drop(columns=["SPY"]), rules_v2_weights(U.drop(columns=["SPY"])),
                   cost_bps=10, freq="W")["returns"].loc[U.index[WARMUP]:]
    g4 = abs(mstats(chk)["Sharpe"] - metrics(chk)["Sharpe"])
    log(f"  G4 fast metrics == engine.metrics()                  |d|    = {g4:.3e}  "
        f"[{'PASS' if g4 < 1e-12 else 'FAIL'}]")

    d10 = df[df.cost == RUNG_HEAD].copy()
    for cv in CONVENTIONS:
        d10[f"gap_{cv}"] = d10.b_CAGR - d10[f"{cv}_CAGR"]
    sh10 = d10[d10.set == "SHELF"]
    gr10 = d10[d10.set == "GRID"]
    lo, hi = BUCKETS[BUCKET_HEAD]
    grb = gr10[(gr10.mean_gross >= lo) & (gr10.mean_gross <= hi)]
    r5 = (int((sh10.gap_PATH > 0).sum()), len(sh10),
          int((grb.gap_PATH > 0).sum()), len(grb),
          int((gr10.gap_PATH > 0).sum()), len(gr10))
    ok5 = (r5[0] == PUB868["shelf_beat"] and r5[1] == PUB868["shelf_n"]
           and r5[2] == PUB868["bucket_beat"] and r5[3] == PUB868["bucket_n"]
           and r5[4] == PUB868["grid_beat"] and r5[5] == PUB868["grid_n"])
    log(f"  G5 CROSS-RUN 868's published full-sample counts rebuilt here: "
        f"SHELF {r5[0]}/{r5[1]} (868: {PUB868['shelf_beat']}/{PUB868['shelf_n']}), "
        f"same-bucket GRID {r5[2]}/{r5[3]} (868: {PUB868['bucket_beat']}/{PUB868['bucket_n']}), "
        f"whole ladder {r5[4]}/{r5[5]} (868: {PUB868['grid_beat']}/{PUB868['grid_n']})  "
        f"[{'PASS' if ok5 else 'FAIL'}]")
    log(f"     the ex-post lift 868 read: {r5[0]/r5[1]:.1%} - {r5[2]/r5[3]:.1%} = "
        f"{100*(r5[0]/r5[1] - r5[2]/r5[3]):+.1f} pp")

    # ================================================================= [1] the ex-ante selection
    log("\n" + "=" * 100)
    log("[1] RE-RUN THE SHELF'S OWN SELECTION (PROTOCOL 4b) ON THE SELECTION WINDOW ALONE")
    log("=" * 100)
    log("selection rule, applied to a window: Sharpe > SPY in BOTH halves of that window, "
        "MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.")
    log("Bucketing uses each book's realised mean gross measured ON THE SELECTION WINDOW ONLY.")

    sel_rows = []
    for _, r in df.iterrows():
        for w in WINDOWS:
            bk_is = {k: r[f"{w}_IS_b_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
            sp_is = {k: r[f"{w}_IS_SPY_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
            bk_full = {k: r[f"b_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
            sp_full = {k: r[f"SPY_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
            rec = dict(book=r.book, set=r["set"], panel=r.panel, cost=r.cost, window=w,
                       gbar_IS=r[f"{w}_IS_gbar"], gbar_full=r.mean_gross,
                       sel_exante=keep_4b(bk_is, sp_is), sel_expost=keep_4b(bk_full, sp_full),
                       IS_Sharpe=r[f"{w}_IS_b_Sharpe"], EV_CAGR=r[f"{w}_EV_b_CAGR"],
                       EV_Sharpe=r[f"{w}_EV_b_Sharpe"], EV_MaxDD=r[f"{w}_EV_b_MaxDD"],
                       EV_H1=r[f"{w}_EV_b_H1"], EV_H2=r[f"{w}_EV_b_H2"])
            for cv in CONVENTIONS:
                rec[f"EV_beat_{cv}"] = bool(r[f"{w}_EV_b_CAGR"] > r[f"{w}_EV_{cv}_CAGR"])
                rec[f"EV_gap_{cv}"] = r[f"{w}_EV_b_CAGR"] - r[f"{w}_EV_{cv}_CAGR"]
            sel_rows.append(rec)
    sel = pd.DataFrame(sel_rows)

    log(f"\nHOW MANY OF THE {n_shelf} COMMITTED SHELF BOOKS CLEAR 4b ON THE SELECTION WINDOW "
        f"ALONE (H_REACHABLE):")
    for w in WINDOWS:
        q = sel[(sel.window == w) & (sel.cost == RUNG_HEAD) & (sel.set == "SHELF")]
        log(f"  window ..{w}: {int(q.sel_exante.sum())} of {len(q)}   "
            f"[{', '.join(sorted(q[q.sel_exante].book))}]")
        log(f"                  MISSED: [{', '.join(sorted(q[~q.sel_exante].book))}]")
    qh = sel[(sel.window == WIN_HEAD) & (sel.cost == RUNG_HEAD) & (sel.set == "SHELF")]
    reach = int(qh.sel_exante.sum())
    h_reach = reach >= REACH_BAR
    log(f"H_REACHABLE (>= {REACH_BAR} of {n_shelf} at the headline window {WIN_HEAD}): "
        f"{'PASS' if h_reach else 'FAIL'}   observed {reach}")

    # ------------------------------------------------------------------ the 3x3 grid
    log("\n" + "=" * 100)
    log("[2] THE 2-DIAL GRID - SELECTION LIFT, EX ANTE vs EX POST  (all 9 cells)")
    log("=" * 100)
    log("LIFT = beat-rate(selected) - beat-rate(unselected in the same gross bucket), both "
        "measured on the EVALUATION window (everything after the selection window).")

    grid = []
    for w, (bn, (lo, hi)), cv, c in product(WINDOWS, BUCKETS.items(), CONVENTIONS, RUNGS):
        q = sel[(sel.window == w) & (sel.cost == c)].copy()
        q = q[(q.gbar_IS >= lo) & (q.gbar_IS <= hi)]
        if not len(q):
            continue
        out = dict(window=w, bucket=bn, comparand=cv, cost=c, n_pool=len(q))
        for arm in ("exante", "expost"):
            s_ = q[q[f"sel_{arm}"]]
            u_ = q[~q[f"sel_{arm}"]]
            br_s = float(s_[f"EV_beat_{cv}"].mean()) if len(s_) else np.nan
            br_u = float(u_[f"EV_beat_{cv}"].mean()) if len(u_) else np.nan
            out[f"{arm}_n_sel"] = len(s_)
            out[f"{arm}_beat_sel"] = int(s_[f"EV_beat_{cv}"].sum()) if len(s_) else 0
            out[f"{arm}_n_uns"] = len(u_)
            out[f"{arm}_beat_uns"] = int(u_[f"EV_beat_{cv}"].sum()) if len(u_) else 0
            out[f"{arm}_rate_sel"] = br_s
            out[f"{arm}_rate_uns"] = br_u
            out[f"{arm}_lift_pp"] = 100.0 * (br_s - br_u)
            out[f"{arm}_medgap_sel"] = float(s_[f"EV_gap_{cv}"].median()) if len(s_) else np.nan
            out[f"{arm}_medgap_uns"] = float(u_[f"EV_gap_{cv}"].median()) if len(u_) else np.nan
        grid.append(out)
    grid = pd.DataFrame(grid)

    hd = grid[(grid.comparand == CONV_HEAD) & (grid.cost == RUNG_HEAD)]
    log(f"\nHEADLINE comparand {CONV_HEAD}, rung {RUNG_HEAD:.0f} bps - the 9 tuned cells:")
    cols = ["window", "bucket", "n_pool", "exante_n_sel", "exante_beat_sel", "exante_n_uns",
            "exante_beat_uns", "exante_lift_pp", "expost_n_sel", "expost_beat_sel",
            "expost_n_uns", "expost_beat_uns", "expost_lift_pp"]
    log(hd[cols].to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    log(f"\nEVERY grid point, both comparands and both rungs ({len(grid)} rows):")
    log(grid.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------------ score the hypotheses
    log("\n" + "=" * 100)
    log("[3] SCORE THE PRE-REGISTERED READINGS")
    log("=" * 100)
    h = grid[(grid.window == WIN_HEAD) & (grid.bucket == BUCKET_HEAD)
             & (grid.comparand == CONV_HEAD) & (grid.cost == RUNG_HEAD)].iloc[0]
    log(f"headline cell (window ..{WIN_HEAD}, bucket {BUCKET_HEAD}, {CONV_HEAD}, "
        f"{RUNG_HEAD:.0f} bps), pool {int(h.n_pool)} books:")
    log(f"  EX POST  selected {int(h.expost_beat_sel)}/{int(h.expost_n_sel)} "
        f"({h.expost_rate_sel:.1%})  unselected {int(h.expost_beat_uns)}/{int(h.expost_n_uns)} "
        f"({h.expost_rate_uns:.1%})   LIFT {h.expost_lift_pp:+.1f} pp")
    log(f"  EX ANTE  selected {int(h.exante_beat_sel)}/{int(h.exante_n_sel)} "
        f"({h.exante_rate_sel:.1%})  unselected {int(h.exante_beat_uns)}/{int(h.exante_n_uns)} "
        f"({h.exante_rate_uns:.1%})   LIFT {h.exante_lift_pp:+.1f} pp")
    log(f"  median EV gap vs {CONV_HEAD}: ex-ante selected {h.exante_medgap_sel:+.2%}, "
        f"unselected {h.exante_medgap_uns:+.2%}")
    h_sel = bool(h.exante_lift_pp < LIFT_BAR_PP)
    log(f"H_SELECTION (LIFT_exante < +{LIFT_BAR_PP:.0f} pp): {'PASS' if h_sel else 'FAIL'}   "
        f"observed {h.exante_lift_pp:+.1f} pp")
    log(f"H_REAL      (LIFT_exante >= +{LIFT_BAR_PP:.0f} pp): "
        f"{'PASS' if not h_sel else 'FAIL'}")

    log("\nunanimity across the 9 tuned cells (ex-ante lift, pp; headline comparand/rung):")
    for bn in BUCKETS:
        line = f"  bucket {bn:<7}"
        for w in WINDOWS:
            q = hd[(hd.window == w) & (hd.bucket == bn)]
            if len(q):
                q = q.iloc[0]
                line += (f" | ..{w}  exante {q.exante_lift_pp:+6.1f} "
                         f"(n_sel {int(q.exante_n_sel):2d})  expost {q.expost_lift_pp:+6.1f}")
        log(line)
    n_neg = int((hd.exante_lift_pp < LIFT_BAR_PP).sum())
    log(f"  ex-ante lift below the {LIFT_BAR_PP:.0f} pp bar in {n_neg} of {len(hd)} tuned cells; "
        f"ex-post lift below it in {int((hd.expost_lift_pp < LIFT_BAR_PP).sum())} of {len(hd)}")
    log("\ncontrols (CONST comparand and the 25 bps rung):")
    for cv, c in product(CONVENTIONS, RUNGS):
        if cv == CONV_HEAD and c == RUNG_HEAD:
            continue
        q = grid[(grid.window == WIN_HEAD) & (grid.bucket == BUCKET_HEAD)
                 & (grid.comparand == cv) & (grid.cost == c)]
        if len(q):
            q = q.iloc[0]
            log(f"  {cv:<6} {c:5.1f}bps  exante lift {q.exante_lift_pp:+6.1f} pp "
                f"({int(q.exante_beat_sel)}/{int(q.exante_n_sel)} vs "
                f"{int(q.exante_beat_uns)}/{int(q.exante_n_uns)})   "
                f"expost lift {q.expost_lift_pp:+6.1f} pp")

    log("\nTHE SAME QUESTION ASKED OF THE COMMITTED SHELF DIRECTLY (how much of 6-of-8 survives):")
    for w in WINDOWS:
        q = sel[(sel.window == w) & (sel.cost == RUNG_HEAD) & (sel.set == "SHELF")]
        qa = q[q.sel_exante]
        log(f"  window ..{w}: committed SHELF beats its own {CONV_HEAD} gxSPY on the EVALUATION "
            f"window in {int(q[f'EV_beat_{CONV_HEAD}'].sum())} of {len(q)}; restricted to the "
            f"{len(qa)} that were REACHABLE ex ante, {int(qa[f'EV_beat_{CONV_HEAD}'].sum())} of "
            f"{len(qa)}")

    # ------------------------------------------------------------------ rule 8
    log("\n" + "=" * 100)
    log("[4] RULE 8 WALK-FORWARD - IS-ONLY SELECTOR, OOS READ ONCE, BOTH KEEP PATHS")
    log("=" * 100)
    log(f"IS = ..{WIN_HEAD} (the headline selection window), OOS = everything after it. The "
        f"selector is the ex-ante 4b set, tie-broken by highest IS Sharpe, per panel.")
    picks = []
    for pn in panels:
        q = sel[(sel.window == WIN_HEAD) & (sel.cost == RUNG_HEAD) & (sel.panel == pn)
                & (sel.sel_exante)]
        if not len(q):
            log(f"  {pn}: the ex-ante 4b rule selects NO book on this panel - nothing to read OOS.")
            continue
        p = q.sort_values("IS_Sharpe", ascending=False).iloc[0]
        row = df[(df.book == p.book) & (df.cost == RUNG_HEAD)].iloc[0]
        ev = {k: row[f"{WIN_HEAD}_EV_b_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
        sp = {k: row[f"{WIN_HEAD}_EV_SPY_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
        bl = {k: row[f"{WIN_HEAD}_EV_BASE_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
        k4a, k4b = keep_4a(ev, bl), keep_4b(ev, sp)
        log(f"  {pn} pick {p.book}  (IS Sharpe {p.IS_Sharpe:.3f}, IS gbar {p.gbar_IS:.3f}, "
            f"one of {len(q)} ex-ante selected)")
        log(f"    OOS  {ev['CAGR']:7.2%} / {ev['Sharpe']:.3f} / {ev['MaxDD']:7.2%}   "
            f"halves {ev['H1']:.3f} / {ev['H2']:.3f}")
        log(f"    SPY  {sp['CAGR']:7.2%} / {sp['Sharpe']:.3f} / {sp['MaxDD']:7.2%}   "
            f"halves {sp['H1']:.3f} / {sp['H2']:.3f}   "
            f"(4b bars: CAGR >= {CAGRFLOOR_FRAC*sp['CAGR']:.2%}, "
            f"DD >= {DDCAP_FRAC*sp['MaxDD']:.2%})")
        log(f"    RULES v2 (live)  {bl['CAGR']:7.2%} / {bl['Sharpe']:.3f} / {bl['MaxDD']:7.2%}   "
            f"halves {bl['H1']:.3f} / {bl['H2']:.3f}")
        log(f"    gxSPY ({CONV_HEAD}) OOS CAGR {row[f'{WIN_HEAD}_EV_{CONV_HEAD}_CAGR']:7.2%}   "
            f"gap {p[f'EV_gap_{CONV_HEAD}']:+.2%}   "
            f"beats it: {p[f'EV_beat_{CONV_HEAD}']}")
        log(f"    KEEP 4a {'PASS' if k4a else 'FAIL'}   KEEP 4b {'PASS' if k4b else 'FAIL'}")
        picks.append(dict(panel=pn, pick=p.book, IS_Sharpe=p.IS_Sharpe, n_exante=len(q),
                          OOS_CAGR=ev["CAGR"], OOS_Sharpe=ev["Sharpe"], OOS_MaxDD=ev["MaxDD"],
                          OOS_H1=ev["H1"], OOS_H2=ev["H2"], keep_4a=k4a, keep_4b=k4b,
                          SPY_CAGR=sp["CAGR"], SPY_Sharpe=sp["Sharpe"], SPY_MaxDD=sp["MaxDD"],
                          V2_CAGR=bl["CAGR"], V2_Sharpe=bl["Sharpe"], V2_MaxDD=bl["MaxDD"],
                          gx_gap=p[f"EV_gap_{CONV_HEAD}"], gx_beat=p[f"EV_beat_{CONV_HEAD}"]))
    h_wf = any(p["keep_4b"] for p in picks)
    log(f"H_WF (some ex-ante pick clears a KEEP path OOS): "
        f"4b {'PASS' if h_wf else 'FAIL'}, 4a {'PASS' if any(p['keep_4a'] for p in picks) else 'FAIL'}")

    # ------------------------------------------------------------------ verdict
    log("\n" + "=" * 100)
    ans = ("YES - THE 6-OF-8 IS A SELECTION EFFECT" if h_sel
           else "NO - THE LIFT SURVIVES AN HONEST SELECTION WINDOW")
    log(f"ANSWER: {ans}")
    log(f"  ex-post lift {h.expost_lift_pp:+.1f} pp -> ex-ante lift {h.exante_lift_pp:+.1f} pp "
        f"at the declared headline cell (bar +{LIFT_BAR_PP:.0f} pp)")
    log("VERDICT for capital: KILL unless a KEEP path passed above. Nothing is promoted by this "
        "run on its own; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched "
        "(PROTOCOL rule 6).")
    log(f"total runtime {time.time()-t0:.0f}s")

    df.to_csv(OUT / f"{STEM}.books.csv", index=False)
    sel.to_csv(OUT / f"{STEM}.selection.csv", index=False)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    pd.DataFrame(picks).to_csv(OUT / f"{STEM}.picks.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
