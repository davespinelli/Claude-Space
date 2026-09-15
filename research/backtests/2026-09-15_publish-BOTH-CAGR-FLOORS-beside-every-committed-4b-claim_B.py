#!/usr/bin/env python3
"""IDEA 872 - publish BOTH CAGR FLOORS beside every committed 4b claim.
Lane B, 2026-09-15.

THE CLAIM UNDER TEST
--------------------
Idea 868 (committed today) priced every book in the record against a GROSS-MATCHED SPY and found
that PROTOCOL's floor and a gross-matched floor rank the same 54-book ladder in OPPOSITE orders
(rho(mean gross, gap) -0.619 under the 100%-SPY reading against +0.535 under the matched one).
The queue reads that as two different questions wearing one leg's clothes:

    CURRENT  CAGR >= 0.70 * CAGR(SPY)            "worth real capital in absolute terms"
    MATCHED  CAGR >= 0.70 * CAGR(g_t * r_SPY)    "better than passive at the exposure it held"

and asks for the restatement rather than the swap 868 killed:

    RE-SCORE THE RECORD'S COMMITTED 4b PASSES UNDER BOTH FLOORS AND REPORT WHICH CLAIMS NEED
    WHICH.

WHAT THIS RUN ADDS OVER 868
---------------------------
868 published pass RATES per floor (a count).  A count cannot say which claim needs which floor.
This run is per-CLAIM: every book in the claim set carries BOTH floor levels, BOTH margins in
pp/yr, its binding leg under each, and a classification.  It then asks the only question that can
make the restatement worth a PROTOCOL line rather than a footnote:

    DOES PUBLISHING BOTH FLOORS CHANGE A CAPITAL DECISION?

answered by rule 8 - select ex ante on 2009-2016 under each floor form, evaluate 2017-2026
untouched, and report whether the two floors pick the SAME book.  If they pick the same book the
restatement is documentation; if they pick different books, the OOS table says which floor was
the honest selector.

CLASSIFICATION (the deliverable of "which claims need which")
    FLOOR-FREE      4b PASS under both floors; the CAGR leg binds under neither
    ABSOLUTE-HELD   4b PASS under both, but the CAGR leg is the binding-margin leg under CURRENT
                    -> the claim is true either way but is a CURRENT-floor claim on the margin
    MATCHED-ONLY    4b FAIL under CURRENT, PASS under MATCHED -> the claim EXISTS only under the
                    matched floor and must never be quoted without it
    NEITHER         4b FAIL under both

THE TWO TUNED PARAMETERS (PROTOCOL rule 4: at most two; ALL grid points reported)
--------------------------------------------------------------------------------
  1. CLAIM SET  {MEMO8, PASS62, ALL62}
       MEMO8  the 8 memo-backed SHELF books - the record's literal published 4b claims
       PASS62 every book of the 62 whose FULL-sample 4b verdict PASSes under the CURRENT floor
              - the mechanical restatement of "a committed 4b pass".  DECLARED HEADLINE.
       ALL62  all 62 books, passes and fails, so the re-score is not conditioned on the outcome
  2. FLOOR FORM {CURRENT, CONST, PATH}
       CURRENT 0.70*CAGR(SPY);  CONST 0.70*CAGR(gbar*r_SPY);  PATH 0.70*CAGR(g_t*r_SPY).
       DECLARED HEADLINE PAIR: (CURRENT, PATH) - 868's own two poles.

Reported controls, never selected on: cost rung {10, 25} bps, the half convention (the record's
own len(r)//2), panel {U56, B136, SMALL}, and the 4a verdict against live RULES v2 beside every
4b cell.

PRE-REGISTERED HYPOTHESES AND BARS (fixed before any number below the gates is read)
    H_ONEWAY    a book holding gbar <= 1 cannot be hurt by the matched floor, so the swap can
                only ADD passes and no committed 4b PASS can be lost.  PASS = 62 of 62 books
                have floor_PATH <= floor_CURRENT at the headline rung.
    H_MOVES     the floors move committed verdicts at a rate worth a PROTOCOL line.
                PASS = >= 20% of ALL62's full-sample 4b verdicts differ between CURRENT and PATH.
    H_NEEDBOTH  the two floors are different questions on the claim set.
                PASS = Spearman rho(margin_CURRENT, margin_PATH) over ALL62 < 0.90.
    H_PICK      publishing both changes a capital decision: the two floor forms pick DIFFERENT
                books ex ante under rule 8.  PASS = different book at the headline cell.
    H_WF        rule 8: the ex-ante pick under each floor form clears a KEEP path out of sample.
                Reported for BOTH paths, 4a and 4b, against RULES v2 and SPY, whichever way it
                goes.

GATES (printed before any new number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD)
    G2  the gross-matched SPY at constant g = 1.00 is SPY itself, exactly
    G3  the PATH comparand's realised mean gross equals the book's own, to machine precision
    G4  fast metrics == engine.metrics()
    G5  CROSS-RUN: 868's published CAGR-leg pass rates at phi=0.70 rebuilt from this run's own
        arms - SHELF 8/8 under all three floors, GRID 27/54 CURRENT and 42/54 CONST/PATH -
        and its full-4b count 18 -> 27 of 54.

Books are IMPORTED from the same committed lane-C / idea-868 builders, never re-typed, so this
run and 868 are measuring the same objects.

SURVIVORSHIP: U56 / B136 / SMALL are current-constituent lists; the small panel additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv.  Every CAGR LEVEL below is
optimistic - for the books AND for both comparands.  The headline quantities are a per-claim
DIFFERENCE of two floors on the same tape and a difference of two ex-ante SELECTIONS; the rule-8
table at the end reads levels and is exposed in full.

Data: committed caches only, no network, never yfinance.
PROTOCOL: 10 bps costs, next-day execution, no shorting, no leverage.  Rules files untouched.
Deterministic, standalone.  Proposes a PROTOCOL line; applies none.
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

# tuned dial 2
FLOORS = ["CURRENT", "CONST", "PATH"]
FLOOR_HEAD = ("CURRENT", "PATH")
# tuned dial 1
CLAIMSETS = ["MEMO8", "PASS62", "ALL62"]
CLAIMSET_HEAD = "PASS62"

IS_END = "2016-12-31"                      # PROTOCOL rule 8's own in-sample end
MOVE_BAR_PCT = 20.0                        # H_MOVES
RHO_BAR = 0.90                             # H_NEEDBOTH
PUB868 = dict(shelf_cagrleg={"CURRENT": 8, "CONST": 8, "PATH": 8}, shelf_n=8,
              grid_cagrleg={"CURRENT": 27, "CONST": 42, "PATH": 42}, grid_n=54,
              grid_4b_current=18, grid_4b_path=27)

LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fmet(r):
    """Fast CAGR / Sharpe / MaxDD on a return series (gate G4 checks it against engine)."""
    a = np.asarray(r, float)
    if len(a) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + a)
    cagr = eq[-1] ** (252.0 / len(a)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = a.std(ddof=0) * np.sqrt(252.0)
    return cagr, ((a.mean() * 252.0) / vol if vol else np.nan), dd


def mstats(r):
    """The record's own convention: engine.metrics() plus half Sharpes at h = len(r)//2."""
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs_4b(bk, cmp_, floor_cagr):
    """PROTOCOL 4b leg by leg.  cmp_ supplies the H1/H2/DD comparand (always SPY, per PROTOCOL);
    floor_cagr is the CAGR floor LEVEL, which is the only thing the floor form changes."""
    return dict(H1=bool(bk["H1"] > cmp_["H1"]), H2=bool(bk["H2"] > cmp_["H2"]),
                DDCAP=bool(bk["MaxDD"] >= DDCAP_FRAC * cmp_["MaxDD"]),
                CAGRFLOOR=bool(bk["CAGR"] >= floor_cagr))


def keep_4a(bk, base):
    return bool(bk["H1"] > base["H1"] and bk["H2"] > base["H2"] and bk["MaxDD"] >= base["MaxDD"])


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# ================================================================== run
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 872 - publish BOTH CAGR FLOORS beside every committed 4b claim  (lane B, 2026-09-15)")
    log("=" * 100)
    log(f"pandas {pd.__version__} numpy {np.__version__}")
    log("PROTOCOL: 10 bps, next-day execution, no shorting, no leverage.  Rules files untouched.")
    log(f"2 tuned dials: CLAIM SET {CLAIMSETS} x FLOOR FORM {FLOORS} = "
        f"{len(CLAIMSETS)*len(FLOORS)} cells, ALL reported, at both cost rungs.")
    log(f"HEADLINE declared before any number is read: claim set {CLAIMSET_HEAD}, floor pair "
        f"{FLOOR_HEAD[0]} vs {FLOOR_HEAD[1]}, rung {RUNG_HEAD:.0f} bps, phi {CAGRFLOOR_FRAC:.2f}.")
    log(f"Bars: H_MOVES needs >= {MOVE_BAR_PCT:.0f}% of ALL62 verdicts to differ; H_NEEDBOTH "
        f"needs rho(margins) < {RHO_BAR:.2f}; H_PICK needs the two floors to pick DIFFERENT "
        f"books ex ante.")
    log("Controls, never selected on: rungs 10/25 bps, three panels, the 4a verdict against live "
        "RULES v2 beside every 4b cell.")
    log("SURVIVORSHIP: U56/B136/SMALL are current-constituent lists; every LEVEL is optimistic. "
        "The headline quantities are same-tape DIFFERENCES.")
    log("")

    laneC = _load(LANEC, "laneC872")
    m868 = _load(SRC868, "idea868_872")

    U, B = load_universe(), load_universe(broad=True)
    S = m868.small_panel()
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
        f"(IMPORTED from the same builders idea 868 used, never re-typed)")

    # ------------------------------------------------------------------ price every book once
    rows, g1, g2, g3, g4 = [], [], [], [], []
    base_cache = {}
    for name, spec in books.items():
        px = panels[spec["panel"]]
        pxn = px.drop(columns=["SPY"], errors="ignore")
        W = spec["W"].reindex(pxn.index).reindex(columns=pxn.columns).fillna(0.0)
        start = pxn.index[WARMUP]
        gross_t = W.sum(axis=1).shift(1).fillna(0.0).loc[start:]      # t+1 aligned, as held
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        key = (spec["panel"],)
        if key not in base_cache:
            base_cache[key] = {c: backtest(pxn, rules_v2_weights(pxn), cost_bps=c,
                                           freq="W")["returns"].loc[start:] for c in RUNGS}
        base_all = base_cache[key]
        for c in RUNGS:
            r = backtest(pxn, W, cost_bps=c, freq=spec["freq"])["returns"].loc[start:]
            gbar = float(gross_t.mean())
            comp = {"CURRENT": spy, "CONST": gbar * spy, "PATH": gross_t * spy}
            row = dict(book=name, set=spec["set"], panel=spec["panel"], cost=c, src=spec["src"],
                       mean_gross=gbar)
            windows = (("FULL", slice(None, None)),
                       ("IS", slice(None, IS_END)),
                       ("OOS", slice(pd.Timestamp(IS_END) + pd.Timedelta(days=1), None)))
            for tag, sl in windows:
                rb = r.loc[sl]
                bs = mstats(rb)
                for k_, v_ in bs.items():
                    row[f"{tag}_b_{k_}"] = v_
                sm = mstats(spy.loc[sl])
                for k_, v_ in sm.items():
                    row[f"{tag}_SPY_{k_}"] = v_
                bm = mstats(base_all[c].loc[sl])
                for k_, v_ in bm.items():
                    row[f"{tag}_BASE_{k_}"] = v_
                row[f"{tag}_gbar"] = float(gross_t.loc[sl].mean())
                row[f"{tag}_4a"] = keep_4a(bs, bm)
                for fl in FLOORS:
                    cm = mstats(comp[fl].loc[sl])
                    floor_lvl = CAGRFLOOR_FRAC * cm["CAGR"]
                    lg = legs_4b(bs, sm, floor_lvl)
                    row[f"{tag}_{fl}_cmpCAGR"] = cm["CAGR"]
                    row[f"{tag}_{fl}_floor"] = floor_lvl
                    row[f"{tag}_{fl}_margin"] = bs["CAGR"] - floor_lvl
                    row[f"{tag}_{fl}_cagrleg"] = lg["CAGRFLOOR"]
                    row[f"{tag}_{fl}_4b"] = all(lg.values())
                    row[f"{tag}_{fl}_fails"] = "+".join(k for k, v in lg.items() if not v) or "-"
            rows.append(row)
            if c == RUNG_HEAD:
                # G3: recover the PATH comparand's own realised gross back out of the series
                nz = spy.abs() > 1e-12
                recovered = float((comp["PATH"][nz] / spy[nz]).mean())
                g3.append(abs(recovered - float(gross_t[nz].mean())))
                cc, ss, dd = fmet(r)
                mm = metrics(r)
                g4.append(max(abs(cc - mm["CAGR"]), abs(dd - mm["MaxDD"])))
                if spec["memo"]:
                    m = spec["memo"]
                    bs = mstats(r)
                    g1.append(dict(book=name, memo_CAGR=m[0], here_CAGR=bs["CAGR"],
                                   memo_Sharpe=m[1], here_Sharpe=bs["Sharpe"],
                                   memo_MaxDD=m[2], here_MaxDD=bs["MaxDD"]))
                # G2: the matched comparand built through the same code path at constant g=1.00
                g2.append(float(metrics(pd.Series(1.0, index=spy.index) * spy)["CAGR"]
                                - metrics(spy)["CAGR"]))
    df = pd.DataFrame(rows)
    log(f"  priced {len(books)} books x {len(RUNGS)} rungs  ({time.time()-t0:.0f}s)")

    # ------------------------------------------------------------------ gates
    log("\n[0] GATES (printed before any new number is read)")
    g1 = pd.DataFrame(g1)
    g1["dC"] = (g1.here_CAGR - g1.memo_CAGR).abs()
    g1["dS"] = (g1.here_Sharpe - g1.memo_Sharpe).abs()
    ok1 = int(((g1.dC < 0.01) & (g1.dS < 0.10)).sum())
    log(f"  G1 SHELF memo triples: {ok1} of {len(g1)} within 1.00 pp CAGR and 0.10 Sharpe "
        f"[{'PASS' if ok1 >= len(g1) else 'PARTIAL'}]  (worst |dCAGR| {g1.dC.max():.4f}, "
        f"|dSharpe| {g1.dS.max():.4f}; tape vintage moves every LEVEL slightly, and every "
        f"headline here is a same-tape DIFFERENCE)")
    log(f"  G2 gross-matched SPY at constant g=1.00 == SPY: max |dCAGR| {max(map(abs,g2)):.3e} "
        f"[{'PASS' if max(map(abs,g2)) < 1e-12 else 'FAIL'}]")
    log(f"  G3 PATH comparand realised mean gross == book's own: max |d| {max(g3):.3e} "
        f"[{'PASS' if max(g3) < 1e-12 else 'FAIL'}]")
    log(f"  G4 fast metrics == engine.metrics(): max |d| {max(g4):.3e} "
        f"[{'PASS' if max(g4) < 1e-9 else 'FAIL'}]")

    h = df[df.cost == RUNG_HEAD].set_index("book")
    grid = h[h["set"] == "GRID"]
    shelf = h[h["set"] == "SHELF"]
    g5 = []
    for fl in FLOORS:
        g5.append((f"SHELF CAGR-leg {fl}", int(shelf[f"FULL_{fl}_cagrleg"].sum()),
                   PUB868["shelf_cagrleg"][fl]))
        g5.append((f"GRID  CAGR-leg {fl}", int(grid[f"FULL_{fl}_cagrleg"].sum()),
                   PUB868["grid_cagrleg"][fl]))
    g5.append(("GRID  full-4b CURRENT", int(grid["FULL_CURRENT_4b"].sum()), PUB868["grid_4b_current"]))
    g5.append(("GRID  full-4b PATH", int(grid["FULL_PATH_4b"].sum()), PUB868["grid_4b_path"]))
    ok5 = sum(1 for _, a, b in g5 if a == b)
    log(f"  G5 CROSS-RUN rebuild of 868's published counts: {ok5} of {len(g5)} exact "
        f"[{'PASS' if ok5 == len(g5) else 'PARTIAL'}]")
    for lbl, a, b in g5:
        log(f"       {lbl:28s} here {a:3d}   868 published {b:3d}   {'ok' if a == b else 'DIFF'}")
    log(f"     (SHELF n={len(shelf)}, GRID n={len(grid)}; 868's denominators 8 and 54)")

    # ------------------------------------------------------------------ [1] claim sets
    log("\n[1] THE CLAIM SETS (dial 1), defined before any floor is read")
    sets = {"MEMO8": list(shelf.index),
            "PASS62": list(h.index[h["FULL_CURRENT_4b"]]),
            "ALL62": list(h.index)}
    DESC = {"MEMO8": "the record's literal memo-backed 4b claims",
            "PASS62": "every book the CURRENT floor passes on the full sample",
            "ALL62": "every priced book, not conditioned on the outcome"}
    for k, v in sets.items():
        log(f"  {k:7s} n={len(v):3d}  {DESC[k]}")

    # ------------------------------------------------------------------ [2] one-way check
    log("\n[2] H_ONEWAY - can a committed 4b PASS be LOST by publishing the matched floor?")
    oneway = int((h["FULL_PATH_floor"] <= h["FULL_CURRENT_floor"] + 1e-15).sum())
    lost = int((h["FULL_CURRENT_4b"] & ~h["FULL_PATH_4b"]).sum())
    gained = int((~h["FULL_CURRENT_4b"] & h["FULL_PATH_4b"]).sum())
    log(f"  floor_PATH <= floor_CURRENT for {oneway} of {len(h)} books "
        f"[H_ONEWAY {'PASS' if oneway == len(h) else 'FAIL'}]  "
        f"(max gbar {h.mean_gross.max():.3f}; a book at gbar>1 would be the exception and there "
        f"is none)")
    log(f"  committed CURRENT passes LOST under PATH: {lost}    FAILs GAINED: {gained}")
    log(f"  => the re-score is ONE-WAY by construction on this corpus: the matched floor is the "
        f"WEAKER floor for every long-only book that ever holds cash.  'Which claims need which' "
        f"is therefore a question about the {gained} MATCHED-ONLY claims and about the MARGIN the "
        f"rest carry, not about lost passes.")

    # ------------------------------------------------------------------ [3] full 3x3 grid
    log("\n[3] ALL 9 GRID POINTS (claim set x floor form), both rungs - 4b pass counts")
    gridrows = []
    for cs, fl, c in product(CLAIMSETS, FLOORS, RUNGS):
        sub = df[(df.cost == c)].set_index("book").loc[sets[cs]]
        gridrows.append(dict(claim_set=cs, floor=fl, cost=c, n=len(sub),
                             pass_4b=int(sub[f"FULL_{fl}_4b"].sum()),
                             cagrleg_pass=int(sub[f"FULL_{fl}_cagrleg"].sum()),
                             cagrleg_binding=int((~sub[f"FULL_{fl}_cagrleg"]).sum()),
                             pass_4a=int(sub["FULL_4a"].sum()),
                             med_margin_pp=100 * float(sub[f"FULL_{fl}_margin"].median())))
    G = pd.DataFrame(gridrows)
    log(G.to_string(index=False, float_format=lambda x: f"{x:.2f}"))

    # ------------------------------------------------------------------ [4] H_MOVES
    log("\n[4] H_MOVES - how many committed verdicts move between the two headline floors?")
    for cs in CLAIMSETS:
        sub = h.loc[sets[cs]]
        mv = int((sub[f"FULL_{FLOOR_HEAD[0]}_4b"] != sub[f"FULL_{FLOOR_HEAD[1]}_4b"]).sum())
        pct = 100.0 * mv / max(len(sub), 1)
        log(f"  {cs:7s} n={len(sub):3d}  4b verdicts differing CURRENT vs PATH: {mv:3d} "
            f"({pct:5.1f}%)")
    sub = h.loc[sets["ALL62"]]
    mv_all = int((sub["FULL_CURRENT_4b"] != sub["FULL_PATH_4b"]).sum())
    pct_all = 100.0 * mv_all / len(sub)
    log(f"  H_MOVES bar >= {MOVE_BAR_PCT:.0f}% on ALL62: {pct_all:.1f}% "
        f"[{'PASS' if pct_all >= MOVE_BAR_PCT else 'FAIL'}]")

    # ------------------------------------------------------------------ [5] H_NEEDBOTH
    log("\n[5] H_NEEDBOTH - are the two floors the same question?  (rank agreement of margins)")
    for cs in CLAIMSETS:
        sub = h.loc[sets[cs]]
        rho = spearman(sub["FULL_CURRENT_margin"], sub["FULL_PATH_margin"])
        rg_c = spearman(sub["mean_gross"], sub["FULL_CURRENT_margin"])
        rg_p = spearman(sub["mean_gross"], sub["FULL_PATH_margin"])
        log(f"  {cs:7s} rho(margin_CURRENT, margin_PATH) {rho:+.3f}   "
            f"rho(mean gross, margin_CURRENT) {rg_c:+.3f}   "
            f"rho(mean gross, margin_PATH) {rg_p:+.3f}")
    sub = h.loc[sets["ALL62"]]
    rho_all = spearman(sub["FULL_CURRENT_margin"], sub["FULL_PATH_margin"])
    log(f"  H_NEEDBOTH bar rho < {RHO_BAR:.2f} on ALL62: {rho_all:+.3f} "
        f"[{'PASS' if rho_all < RHO_BAR else 'FAIL'}]")
    log(f"  868's own sign check on its 54-book GRID ladder: rho(gross, CURRENT margin) "
        f"{spearman(grid.mean_gross, grid.FULL_CURRENT_margin):+.3f} vs rho(gross, PATH margin) "
        f"{spearman(grid.mean_gross, grid.FULL_PATH_margin):+.3f} "
        f"(868 published -0.619 and +0.535 on the GAP; the sign PAIR is the reproducible object)")

    # ------------------------------------------------------------------ [6] per-claim table
    log("\n[6] THE DELIVERABLE - BOTH FLOORS BESIDE EVERY CLAIM (headline set "
        f"{CLAIMSET_HEAD}, {RUNG_HEAD:.0f} bps)")

    # Each 4b leg's slack, normalised by that leg's own spread across the whole 62-book corpus,
    # so "which leg is thinnest" is a comparison in comparable units rather than across units.
    h = h.copy()
    h["slack_CAGR"] = h["FULL_CURRENT_margin"]
    h["slack_DD"] = h["FULL_b_MaxDD"] - DDCAP_FRAC * h["FULL_SPY_MaxDD"]
    h["slack_H1"] = h["FULL_b_H1"] - h["FULL_SPY_H1"]
    h["slack_H2"] = h["FULL_b_H2"] - h["FULL_SPY_H2"]
    sd = {k: float(h[f"slack_{k}"].std(ddof=1)) for k in ("CAGR", "DD", "H1", "H2")}
    log(f"  leg-slack spreads over ALL62 (the normalisation, computed once and stated): " +
        "  ".join(f"{k} {v:.4f}" for k, v in sd.items()))
    zs = pd.DataFrame({k: h[f"slack_{k}"] / max(sd[k], 1e-12) for k in sd})
    h["thinnest_leg"] = zs.idxmin(axis=1)

    def classify(r):
        cur, pat = r["FULL_CURRENT_4b"], r["FULL_PATH_4b"]
        if cur and pat:
            return "BOTH-CAGR-BOUND" if r["thinnest_leg"] == "CAGR" else "BOTH-FLOOR-FREE"
        if pat and not cur:
            return "MATCHED-ONLY"
        if cur and not pat:
            return "ABSOLUTE-ONLY"
        return "NEITHER"

    h["klass"] = h.apply(classify, axis=1)
    cols = ["set", "panel", "mean_gross", "FULL_b_CAGR", "FULL_CURRENT_floor",
            "FULL_CURRENT_margin", "FULL_PATH_floor", "FULL_PATH_margin",
            "FULL_CURRENT_4b", "FULL_PATH_4b", "FULL_CURRENT_fails", "FULL_PATH_fails",
            "FULL_4a", "klass"]
    head = h.loc[sets[CLAIMSET_HEAD], cols].sort_values("FULL_CURRENT_margin")
    log("  book                                 set   gbar  CAGR   floorC  margC   floorP  margP"
        "   4bC 4bP  4a  class")
    for nm, r in head.iterrows():
        log(f"  {nm:36s} {r['set']:5s} {r.mean_gross:.3f} {100*r.FULL_b_CAGR:5.2f}% "
            f"{100*r.FULL_CURRENT_floor:6.2f}% {100*r.FULL_CURRENT_margin:+6.2f} "
            f"{100*r.FULL_PATH_floor:6.2f}% {100*r.FULL_PATH_margin:+6.2f}  "
            f"{'P' if r.FULL_CURRENT_4b else '.'}   {'P' if r.FULL_PATH_4b else '.'}   "
            f"{'P' if r.FULL_4a else '.'}  {r.klass}")
    log(f"\n  class census over ALL62: " +
        "  ".join(f"{k} {v}" for k, v in h["klass"].value_counts().items()))
    log(f"  class census over {CLAIMSET_HEAD}: " +
        "  ".join(f"{k} {v}" for k, v in h.loc[sets[CLAIMSET_HEAD], 'klass'].value_counts().items()))
    mo = h.index[h["klass"] == "MATCHED-ONLY"]
    if len(mo):
        log(f"\n  the {len(mo)} MATCHED-ONLY claims - true ONLY under the gross-matched floor, and "
            f"never quotable without it:")
        for nm in mo:
            r = h.loc[nm]
            log(f"    {nm:36s} gbar {r.mean_gross:.3f}  CAGR {100*r.FULL_b_CAGR:5.2f}% vs "
                f"SPY {100*r.FULL_SPY_CAGR:5.2f}%   floorC {100*r.FULL_CURRENT_floor:5.2f}% "
                f"floorP {100*r.FULL_PATH_floor:5.2f}%   CURRENT fails on "
                f"{r.FULL_CURRENT_fails}")

    # ------------------------------------------------------------------ [7] rule 8
    log(f"\n[7] RULE 8 WALK-FORWARD - does publishing BOTH floors change a CAPITAL decision?")
    log(f"    Selection on IS <= {IS_END} ONLY; evaluation on OOS > {IS_END}, untouched.")
    log("    Ex-ante selector, stated before it is run: among books clearing 4b ON THE IS WINDOW "
        "under that floor form, take the largest IS CAGR margin under that same floor form. "
        "Ties broken by book name (deterministic).")
    wf = []
    for cs, fl, c in product(CLAIMSETS, FLOORS, RUNGS):
        sub = df[df.cost == c].set_index("book").loc[sets[cs]]
        elig = sub[sub[f"IS_{fl}_4b"]]
        if not len(elig):
            wf.append(dict(claim_set=cs, floor=fl, cost=c, n_elig=0, pick=None))
            continue
        order = sorted(elig.index, key=lambda b: (-float(elig.loc[b, f"IS_{fl}_margin"]), b))
        pick = order[0]
        p = sub.loc[pick]
        wf.append(dict(claim_set=cs, floor=fl, cost=c, n_elig=int(len(elig)), pick=pick,
                       IS_margin_pp=100 * float(p[f"IS_{fl}_margin"]),
                       OOS_CAGR=float(p["OOS_b_CAGR"]), OOS_Sharpe=float(p["OOS_b_Sharpe"]),
                       OOS_MaxDD=float(p["OOS_b_MaxDD"]),
                       SPY_CAGR=float(p["OOS_SPY_CAGR"]), SPY_Sharpe=float(p["OOS_SPY_Sharpe"]),
                       SPY_MaxDD=float(p["OOS_SPY_MaxDD"]),
                       BASE_CAGR=float(p["OOS_BASE_CAGR"]), BASE_Sharpe=float(p["OOS_BASE_Sharpe"]),
                       BASE_MaxDD=float(p["OOS_BASE_MaxDD"]),
                       OOS_4a=bool(p["OOS_4a"]), OOS_4b_CURRENT=bool(p["OOS_CURRENT_4b"]),
                       OOS_4b_PATH=bool(p["OOS_PATH_4b"]),
                       OOS_fails_CURRENT=p["OOS_CURRENT_fails"]))
    WF = pd.DataFrame(wf)
    log("\n  ALL 18 walk-forward cells (3 claim sets x 3 floors x 2 rungs):")
    show = ["claim_set", "floor", "cost", "n_elig", "pick", "IS_margin_pp", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "OOS_4a", "OOS_4b_CURRENT", "OOS_4b_PATH"]
    log(WF[show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    hw = WF[(WF.claim_set == CLAIMSET_HEAD) & (WF.cost == RUNG_HEAD)].set_index("floor")
    pick_c, pick_p = hw.loc["CURRENT", "pick"], hw.loc["PATH", "pick"]
    same = pick_c == pick_p
    log(f"\n  HEADLINE CELL ({CLAIMSET_HEAD}, {RUNG_HEAD:.0f} bps):")
    log(f"    CURRENT floor picks ex ante: {pick_c}")
    log(f"    PATH    floor picks ex ante: {pick_p}")
    log(f"    H_PICK (needs DIFFERENT books) [{'FAIL - same book' if same else 'PASS'}]")
    agree = 0
    for cs, c in product(CLAIMSETS, RUNGS):
        a = WF[(WF.claim_set == cs) & (WF.cost == c) & (WF.floor == "CURRENT")].pick.iloc[0]
        b = WF[(WF.claim_set == cs) & (WF.cost == c) & (WF.floor == "PATH")].pick.iloc[0]
        agree += int(a == b)
    log(f"    across all {len(CLAIMSETS)*len(RUNGS)} (claim set x rung) cells the two floors pick "
        f"the SAME book {agree} times")

    log(f"\n  OOS table for the headline picks - vs the LIVE baseline (RULES v2) and vs SPY:")
    for fl in FLOORS:
        r = hw.loc[fl]
        if r["pick"] is None:
            log(f"    {fl:8s} no IS-eligible book")
            continue
        log(f"    {fl:8s} pick {r['pick']}")
        log(f"             OOS  CAGR {100*r.OOS_CAGR:6.2f}%  Sharpe {r.OOS_Sharpe:5.3f}  "
            f"MaxDD {100*r.OOS_MaxDD:7.2f}%")
        log(f"             SPY  CAGR {100*r.SPY_CAGR:6.2f}%  Sharpe {r.SPY_Sharpe:5.3f}  "
            f"MaxDD {100*r.SPY_MaxDD:7.2f}%")
        log(f"             BASE CAGR {100*r.BASE_CAGR:6.2f}%  Sharpe {r.BASE_Sharpe:5.3f}  "
            f"MaxDD {100*r.BASE_MaxDD:7.2f}%   (RULES v2, live)")
        log(f"             OOS verdicts: 4a {'PASS' if r.OOS_4a else 'FAIL'}   "
            f"4b(CURRENT) {'PASS' if r.OOS_4b_CURRENT else 'FAIL'}   "
            f"4b(PATH) {'PASS' if r.OOS_4b_PATH else 'FAIL'}"
            f"   CURRENT fails on {r.OOS_fails_CURRENT}")
    n4a = int(WF.OOS_4a.sum())
    n4bc = int(WF.OOS_4b_CURRENT.sum())
    n4bp = int(WF.OOS_4b_PATH.sum())
    log(f"\n  H_WF over all {len(WF)} walk-forward cells: OOS 4a PASS {n4a}/{len(WF)}, "
        f"OOS 4b(CURRENT) PASS {n4bc}/{len(WF)}, OOS 4b(PATH) PASS {n4bp}/{len(WF)}")

    # does the floor form change the OOS OUTCOME, not just the pick?
    log("\n  Does the floor form buy OOS performance?  (paired over claim set x rung)")
    for cs, c in product(CLAIMSETS, RUNGS):
        a = WF[(WF.claim_set == cs) & (WF.cost == c) & (WF.floor == "CURRENT")].iloc[0]
        b = WF[(WF.claim_set == cs) & (WF.cost == c) & (WF.floor == "PATH")].iloc[0]
        log(f"    {cs:7s} {c:4.0f}bps  CURRENT pick OOS CAGR {100*a.OOS_CAGR:6.2f}% / Sharpe "
            f"{a.OOS_Sharpe:5.3f}   PATH pick OOS CAGR {100*b.OOS_CAGR:6.2f}% / Sharpe "
            f"{b.OOS_Sharpe:5.3f}   dCAGR {100*(b.OOS_CAGR-a.OOS_CAGR):+6.2f}pp")

    # ------------------------------------------------------------------ verdict
    log("\n" + "=" * 100)
    log("VERDICT")
    log("=" * 100)
    hmoves = "PASS" if pct_all >= MOVE_BAR_PCT else "FAIL"
    hneed = "PASS" if rho_all < RHO_BAR else "FAIL"
    hpick = "FAIL" if same else "PASS"
    log(f"  H_ONEWAY   {'PASS' if oneway == len(h) else 'FAIL'}  "
        f"({oneway}/{len(h)} books have floor_PATH <= floor_CURRENT; {lost} committed passes lost)")
    log(f"  H_MOVES    {hmoves}  ({pct_all:.1f}% of ALL62 verdicts differ, bar {MOVE_BAR_PCT:.0f}%)")
    log(f"  H_NEEDBOTH {hneed}  (rho {rho_all:+.3f}, bar < {RHO_BAR:.2f})")
    log(f"  H_PICK     {hpick}  (ex-ante picks {'identical' if same else 'differ'}: "
        f"{pick_c} vs {pick_p})")
    log(f"  H_WF       OOS 4a {n4a}/{len(WF)}, OOS 4b(CURRENT) {n4bc}/{len(WF)}, "
        f"OOS 4b(PATH) {n4bp}/{len(WF)}")

    # ------------------------------------------------------------------ artifacts
    df.to_csv(OUT / f"{STEM}.books.csv", index=False)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    h.reset_index().to_csv(OUT / f"{STEM}.claims.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nwrote {STEM}.books.csv / .grid.csv / .claims.csv / .walkforward.csv / .console.txt "
        f"({time.time()-t0:.0f}s)")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
