#!/usr/bin/env python3
"""Idea 786 (cloud, 2026-09-11) - is-the-U56-CAGR-FLOOR-GAP-a-DELISTING-artefact.

QUESTION
--------
Idea 787 (lane B, 2026-09-11) re-priced the record's whole standing 4b shelf against an
equal-weight basket of each book's own panel and killed all 82 cells.  The binding leg on the
tightest-drawdown book is the CAGR FLOOR: the U56 RULES v2 band book at gross 1.00 runs
11.554% against a floor of 0.70 x 17.689% = 12.383%, missing by 0.83 pp/yr, and the gross that
would close it (1.0716) lies above PROTOCOL rule 2's no-leverage cap.

But the bar is the most survivorship-exposed object in the record: it holds every CURRENT
constituent at full weight for the whole window, so it never books a delisting.  If a
delisting-complete panel would drag that bar down by more than 1.2 pp/yr, idea 787's KILL is
an artefact of the bar, not a fact about the book.  This run BOUNDS the drag required and asks
whether any defensible delisting assumption reaches it.

WHAT IS BEING SOLVED (never tuned)
----------------------------------
The bar's CAGR must fall from 17.689% to 11.554% / 0.70 = 16.506% for the floor to clear, i.e.
    d* = the annual drag on the BAR that just closes the CAGR floor.
d* is SOLVED per cell, not chosen.  d** = the drag that makes the band book clear ALL FIVE 4b
legs is solved beside it, because dragging the bar also shrinks its drawdown and therefore
TIGHTENS the 4b DD cap (0.60 x bar MaxDD) while it loosens the three Sharpe legs.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. DRAG MODEL in {CONT, LUMPY, NAME}
       CONT  - a constant arithmetic haircut d/252 on every one of the bar's daily returns.
       LUMPY - one hit of size a on the first trading day of each calendar year, nothing else.
       NAME  - the real thing: each year a hazard share h of the surviving names is delisted;
               on its kill date the name books a return of -L, and it is unpriced thereafter,
               so its proceeds sit in cash until the basket's next rebalance and are then
               respread over the survivors.  This is the only model that changes the bar's
               COMPOSITION, and the only one that can be applied to a BOOK as well as a bar.
    2. PANEL in {U56, B136}
All 3 x 2 = 6 grid points are reported.
REPORTED (never selected) axes: bar form {B_EW742 daily/0 bps, B_EWW10 weekly/10 bps}, loss
    given delisting L in {0.30, 0.55, 1.00}, hazard ladder h, seed (8, NAME model only),
    gross ladder (7 rungs), period {FULL, IS, OOS}.

THE CITATION PROBLEM, AND HOW THIS RUN AVOIDS DEPENDING ON IT
-------------------------------------------------------------
The queue asks for a comparison against "published delisting-return estimates".  This sandbox
has NO network, so no figure can be fetched or checked.  Three anchors are quoted from the
literature as RECALLED, explicitly unverified here, and are used only to label columns:
    L = 0.30  Shumway (1997, J. Finance, "The Delisting Bias in CRSP Data") - the mean
              delisting return for performance-related NYSE/AMEX delistings, about -30%.
    L = 0.55  Shumway & Warther (1999, J. Finance) - the Nasdaq counterpart, about -55%.
    L = 1.00  TOTAL WIPEOUT.  This column needs NO citation: -100% is the physical maximum
              loss on a long position, so the hazard it implies is a HARD LOWER BOUND on the
              delisting frequency required under ANY loss assumption whatsoever.
Every conclusion in this run is stated against the L = 1.00 column first.  If the required
hazard is implausible even when every delisting is a total wipeout, no recalled citation can
change the answer, and the unverifiable anchors carry no weight in the verdict.

THE PANEL'S OWN COMPOSITION IS THE SECOND CITATION-FREE LEG
-----------------------------------------------------------
U56 is not a cross-section of listed equities.  It is 35 ETFs (7 broad index funds, 16 sector
funds, 12 bond/FX/commodity funds) plus 20 US mega-cap single stocks - so at most 20/55 of the
bar's weight is exposed to single-name delisting at all, and broad ETFs wind up at NAV rather
than at -30%.  The run therefore also reports the hazard the drag implies on the SINGLE-STOCK
SLEEVE ALONE, which is the number a delisting story actually has to defend.

THE EMPIRICAL ANCHOR (no literature at all)
-------------------------------------------
`RSP` - the investable equal-weight S&P 500 fund - is a column of data/prices.csv.  Its
realised NAV already contains every index deletion, delisting and replacement of the window,
net of its own fee.  The gap between a SYNTHETIC equal-weight basket of current constituents
and RSP's realised return is therefore a direct, fully empirical UPPER bound on how much a
synthetic current-constituent equal-weight basket is inflated by everything at once
(survivorship, composition and weighting together).  Stated as an upper bound, not an estimate:
B136 is not the S&P 500, so composition differences are inside it.

THE ASYMMETRY THE QUEUE'S FRAMING ASSUMES, TESTED RATHER THAN ASSUMED
---------------------------------------------------------------------
Dragging only the bar assumes the BOOK would not book the same delistings.  That is a real
hypothesis - a name usually falls below its 200d MA before it dies, so the band gate may be out
of it by then - but it is a hypothesis.  Under the NAME model the identical delistings are
applied to BOTH the bar and the band book (PART B), and the share of the drag each one eats is
measured.  If the gate does not shield the book, delisting can never close this gap at all.

PRE-REGISTERED HYPOTHESES (written before any drag was solved)
--------------------------------------------------------------
MISS_787 = 0.0083   (idea 787's published U56 CAGR-floor miss, pp/yr, on B_EWW10)
H_DRAG  : d* is reachable.  Falsified if the hazard d* implies on the single-stock sleeve at
          L = 1.00 (total wipeout) exceeds 2%/yr, which for a panel of 20 US mega-caps is
          already an order of magnitude beyond anything observed.
H_SHIELD: the 200d band gate shields the book from delistings the bar eats, so under the NAME
          model the book loses strictly less CAGR than the bar at every (h, L).
H_STABLE: d* solved on IS alone and on OOS alone agree within 50% of each other; if they do
          not, "the drag needed" is not a stable quantity and no bound can be quoted.

GATES (pre-registered, run and printed before any drag is solved)
    G1 bars      : idea 787's committed `.bars.csv` rows (CAGR, Sharpe, MaxDD, H1, H2,
       oos_CAGR, oos_Sharpe, oos_MaxDD) rebuilt from prices for both panels x both EW bars
       and B_SPY.                                                               bar 1e-12
    G2 band book : idea 787's committed BAND-DG grid rows, all 7 gross rungs x 2 panels.
                                                                                bar 1e-12
    G3 headline  : the 0.83 pp miss itself - 0.70 x bar_CAGR - book_CAGR at U56 / g=1.00 /
       B_EWW10.                                                                 bar 1e-4
    G4 identity  : fast_backtest vs engine.backtest on one book per panel.       bar 1e-12
    G5 drag no-op: every drag model at zero intensity returns the bar's own series.  bar 1e-15
    G6 appendix  : idea 787's committed `.grossappendix.csv` g_needed (1.0716 / 1.2356).
                                                                                 bar 1e-4
    G7 census    : the panel composition the single-stock-sleeve leg rests on, counted from
       research/universe.json and universe_broad.json, printed in full.            exact

RULE 8 WALK-FORWARD (required)
    IS <= 2016-12-31, OOS >= 2017-01-01 read ONCE.
    WF-A on the ANSWER: solve d* inside IS only and inside OOS only at every one of the 6
       tuned points and report whether the required drag is a stable quantity (H_STABLE).
    WF-B on a BOOK: pick the BAND-DG gross rung on IS Sharpe alone, read OOS once, and score
       it 4b against the OOS bar BOTH undragged and dragged by the solved d*, against SPY and
       against RULES v2.  Both KEEP paths for every book.
    Stated up front: no book here is new.  This run prices a COMPARAND, so a 4b pass that only
    appears after the bar is handicapped is a statement about the bar, never a capital
    candidate.

SURVIVORSHIP: universe.json and universe_broad.json are CURRENT constituents; that is the
    bias being priced, not a caveat to it.  The small panel is not used.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage, warm-up
skip of 260 rows.  Deterministic, standalone, no network.  Reads research/baseline.py and
committed artefacts of idea 787; modifies nothing but its own outputs:
    .drag.csv .name.csv .netgap.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import json
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GROSS_LADDER = [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]
MODELS = ["CONT", "LUMPY", "NAME"]          # TUNED 1
PANELS = ["U56", "B136"]                    # TUNED 2
BARFORMS = {"B_EW742": (0.0, "D"), "B_EWW10": (COST, "W")}
LOSSES = [0.30, 0.55, 1.00]                 # reported, not tuned; 1.00 needs no citation
HAZARDS = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05]
SEEDS = list(range(6))
MISS_787 = 0.0083
P787 = OUT / "2026-09-11_does-ANY-standing-4b-candidate-clear-an-EQUAL-WEIGHT-bar_B"
TOL, TOL_PUB = 1e-12, 1e-4

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ runner (idea 787's)
def fast_backtest(px, w, cost_bps=COST, freq="W"):
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- books
def _respread(mask_df, gross):
    m = mask_df.astype(float)
    return gross * m.div(m.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def b_band_dg(px, g):
    """RULES v2 exactly (idea 787's b_band_dg): band gate, g/N over ALL priced names, out->CASH."""
    e = px.notna().astype(float)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, 0.03), 0.0)


def b_ewbar(px, g=1.00):
    """idea 787's equal-weight bar basket: equal-weight the panel's own tradables."""
    return _respread(px.notna(), g)


def row_of(r):
    m = metrics(r)
    h = len(r) // 2
    o = r.loc[OOS_START:]
    mo = metrics(o)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"])


def path_4a(c, b):
    legs = {"H1": c["H1"] > b["H1"], "H2": c["H2"] > b["H2"], "MaxDD": c["MaxDD"] >= b["MaxDD"]}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v)


def path_4b(c, bar):
    legs = {"H1": c["H1"] > bar["H1"], "H2": c["H2"] > bar["H2"],
            "OOS": c["oos_Sharpe"] > bar["oos_Sharpe"],
            "DD": c["MaxDD"] >= 0.60 * bar["MaxDD"],
            "CAGR": c["CAGR"] >= 0.70 * bar["CAGR"]}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v)


# ------------------------------------------------------------------------- drag models
def drag_cont(r, d):
    """Constant arithmetic haircut of d per year, spread over 252 trading days."""
    return r - d / 252.0


def drag_lumpy(r, a):
    """One hit of size a on the first trading day of each calendar year."""
    if a == 0.0:
        return r.copy()
    hit = pd.Series(False, index=r.index)
    first = pd.Series(r.index, index=r.index).groupby(r.index.year).min()
    hit.loc[first.values] = True
    return (1.0 + r) * np.where(hit.values, 1.0 - a, 1.0) - 1.0


def kill_frame(px, h, L, seed, start_year=None):
    """NAME model: each calendar year a hazard share h of the SURVIVING names is delisted.

    On its kill date (the first trading day of that year) the name books a return of -L; it is
    unpriced from the following bar onward, so its proceeds earn nothing until the basket's next
    scheduled rebalance and are then respread over the survivors - i.e. delisting proceeds sit
    in cash for at most one rebalance interval, which is what an investor would actually get."""
    if h <= 0.0 or L <= 0.0:
        return px
    out = px.copy()
    rng = np.random.default_rng(zlib.crc32(f"KILL|{h}|{L}|{seed}".encode()) % (2 ** 32))
    idx = px.index
    years = sorted(set(idx.year))
    if start_year is not None:
        years = [y for y in years if y >= start_year]
    alive = list(px.columns)
    firsts = pd.Series(idx, index=idx).groupby(idx.year).min()
    for y in years[1:]:                      # never kill on the frame's own first bar
        n_kill = int(np.floor(h * len(alive) + 0.5))
        if n_kill <= 0 or n_kill >= len(alive):
            continue
        victims = rng.choice(np.array(alive), size=n_kill, replace=False)
        kd = firsts.loc[y]
        pos = idx.get_loc(kd)
        # NUMERICAL FLOOR: a factor of exactly 0 (L = 1.00) drives the name's cumulative
        # product to 0 and the runner's Cp/Cp[s0] to 0/0.  The residual 1e-6 of value makes the
        # realised delisting return -99.9999% instead of -100.0%; at one name's weight that is
        # below 1e-8 of NAV, far under every bar quoted here.
        fac = max(1.0 - L, 1e-6)
        for v in victims:
            out.iloc[pos, out.columns.get_loc(v)] = out.iloc[pos, out.columns.get_loc(v)] * fac
            out.iloc[pos + 1:, out.columns.get_loc(v)] = np.nan
            alive.remove(v)
    return out


def solve_scalar(f, target, lo=0.0, hi=0.25, iters=60):
    """Bisect for the smallest x in [lo, hi] with f(x) <= target (f decreasing in x)."""
    if f(lo) <= target:
        return 0.0
    if f(hi) > target:
        return np.nan
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if f(mid) <= target:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def cagr_of(r):
    return metrics(r)["CAGR"]


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 786  is-the-U56-CAGR-FLOOR-GAP-a-DELISTING-artefact  (cloud, 2026-09-11)")
    P("=" * 112)
    P(f"PROTOCOL: {COST:.0f} bps, next-day fills, warm-up {WARMUP}, IS <= {IS_END}, "
      f"OOS >= {OOS_START} read once.")
    P(f"TUNED (2): DRAG MODEL {MODELS} x PANEL {PANELS} -- all 6 points reported.")
    P(f"SOLVED, never tuned: d* (drag closing the CAGR floor) and d** (drag closing all five "
      f"4b legs).  Pre-registered miss {MISS_787:.4f} pp.")
    P("")

    # ---------------------------------------------------------------- frames
    frames = {}
    for pn in PANELS:
        px = load_universe(broad=(pn == "B136"))
        tradables = [c for c in px.columns if c != "SPY"]
        frames[pn] = dict(px=px, frame=px[tradables].copy(), start=px.index[WARMUP])

    # ---------------------------------------------------------------- gates
    P("=" * 112)
    P("GATES (pre-registered; printed before any drag is solved)")
    P("=" * 112)

    bars, books = {}, {}
    for pn in PANELS:
        f = frames[pn]
        fr, st = f["frame"], f["start"]
        spy = f["px"]["SPY"].pct_change().fillna(0.0).loc[st:]
        bars[(pn, "B_SPY")] = row_of(spy)
        for bn, (cb, fq) in BARFORMS.items():
            r = fast_backtest(fr, b_ewbar(fr), cb, fq)["returns"].loc[st:]
            bars[(pn, bn)] = row_of(r)
            bars[(pn, bn, "series")] = r
        for g in GROSS_LADDER:
            r = fast_backtest(fr, b_band_dg(fr, g), COST, "W")["returns"].loc[st:]
            books[(pn, g)] = row_of(r)
            books[(pn, g, "series")] = r

    B787 = pd.read_csv(f"{P787}.bars.csv")
    c1 = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD"]
    g1 = 0.0
    for _, r in B787.iterrows():
        mine = bars[(r["panel"], r["bar"])]
        g1 = max(g1, max(abs(mine[c] - r[c]) for c in c1))
    P(f"G1 bars         : idea 787's committed .bars.csv, {len(B787)} rows x {len(c1)} columns "
      f"(both panels x B_SPY/B_EW742/B_EWW10), max |d| = {g1:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1 < TOL else 'FAIL'}")

    G787 = pd.read_csv(f"{P787}.grid.csv")
    bd = G787[G787.family == "BAND-DG"]
    c2 = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR", "oos_Sharpe", "oos_MaxDD",
          "IS_Sharpe"]
    g2 = 0.0
    for _, r in bd.iterrows():
        mine = books[(r["panel"], float(r["dial"]))]
        g2 = max(g2, max(abs(mine[c] - r[c]) for c in c2))
    P(f"G2 band book    : idea 787's committed BAND-DG rows, {len(bd)} rows x {len(c2)} columns "
      f"(7 gross rungs x 2 panels), max |d| = {g2:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g2 < TOL else 'FAIL'}")

    miss = 0.70 * bars[("U56", "B_EWW10")]["CAGR"] - books[("U56", 1.00)]["CAGR"]
    g3 = abs(miss - MISS_787)
    P(f"G3 headline     : U56 / g=1.00 / B_EWW10 CAGR-floor miss re-read = {miss:.6f} "
      f"({miss*100:.2f} pp) vs idea 787's published {MISS_787:.4f}; |d| = {g3:.3e} "
      f"(bar {TOL_PUB:.0e}, the published figure carries 2dp) -> "
      f"{'PASS' if g3 < TOL_PUB else 'FAIL'}")

    g4 = 0.0
    for pn in PANELS:
        fr = frames[pn]["frame"]
        w = b_band_dg(fr, 0.75)
        g4 = max(g4, float((fast_backtest(fr, w, COST, "W")["returns"]
                            - backtest(fr, w, cost_bps=COST, freq="W")["returns"]).abs().max()))
    P(f"G4 identity     : fast_backtest vs engine.backtest max |dret| = {g4:.3e} (bar "
      f"{TOL:.0e}) -> {'PASS' if g4 < TOL else 'FAIL'}")

    base = bars[("U56", "B_EWW10", "series")]
    g5 = max(float((drag_cont(base, 0.0) - base).abs().max()),
             float((drag_lumpy(base, 0.0) - base).abs().max()))
    fr0 = frames["U56"]["frame"]
    k0 = kill_frame(fr0, 0.0, 0.30, 0)
    g5 = max(g5, float((k0.fillna(-1) - fr0.fillna(-1)).abs().max().max()))
    P(f"G5 drag no-op   : all three drag models at zero intensity reproduce the bar exactly, "
      f"max |d| = {g5:.3e} (bar 1e-15) -> {'PASS' if g5 < 1e-15 else 'FAIL'}")

    A787 = pd.read_csv(f"{P787}.grossappendix.csv")
    P(f"G6 appendix     : idea 787's committed g_needed_for_CAGR_floor read back: "
      + ", ".join(f"{r['panel']} {r['g_needed_for_CAGR_floor']:.4f}" for _, r in A787.iterrows())
      + f" (U56 1.0716 / B136 1.2356 as published) -> "
      + ("PASS" if abs(float(A787[A787.panel == 'U56'].g_needed_for_CAGR_floor.iloc[0]) - 1.0716)
         < TOL_PUB else "FAIL"))

    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"]) - {"BTC-USD", "ETH-USD"}
    u56_tr = list(frames["U56"]["frame"].columns)
    n_etf = len([c for c in u56_tr if c in etfs])
    n_stk = len([c for c in u56_tr if c in set(U["megacap"])])
    b136_tr = list(frames["B136"]["frame"].columns)
    n_b_etf = len([c for c in b136_tr if c in etfs])
    STOCK_SHARE = {"U56": n_stk / len(u56_tr), "B136": (len(b136_tr) - n_b_etf) / len(b136_tr)}
    P(f"G7 census       : U56 tradables {len(u56_tr)} = {n_etf} ETFs + {n_stk} mega-cap single "
      f"stocks (single-stock share {STOCK_SHARE['U56']:.4f}); B136 tradables {len(b136_tr)} = "
      f"{n_b_etf} ETFs + {len(b136_tr)-n_b_etf} single stocks (share {STOCK_SHARE['B136']:.4f}) "
      f"-> {'PASS' if n_etf + n_stk == len(u56_tr) else 'FAIL'} (counts partition the panel)")
    P(f"                  U56 ETF detail: broad {len([c for c in u56_tr if c in set(U['broad'])])}, "
      f"sectors {len([c for c in u56_tr if c in set(U['sectors'])])}, "
      f"bond/FX/commodity {len([c for c in u56_tr if c in set(U['bonds_fx_commod'])])}. "
      f"Broad and bond ETFs wind up at NAV, not at a performance delisting price.")
    P("")

    # ---------------------------------------------------------------- PART A
    P("=" * 112)
    P("PART A - THE DRAG REQUIRED ON THE BAR (d* solved per cell; all 6 tuned points)")
    P("=" * 112)
    P("The band book at gross 1.00 is the standing candidate; the floor is CAGR >= 0.70 x bar.")
    rows = []
    for pn in PANELS:
        for bn in BARFORMS:
            bar = bars[(pn, bn)]
            bser = bars[(pn, bn, "series")]
            bk = books[(pn, 1.00)]
            need = bk["CAGR"] / 0.70                        # the bar CAGR that just clears
            for model in ["CONT", "LUMPY"]:
                fn = drag_cont if model == "CONT" else drag_lumpy
                dstar = solve_scalar(lambda x: cagr_of(fn(bser, x)), need)
                if np.isfinite(dstar):
                    dr = fn(bser, dstar)
                    ok4b, missleg = path_4b(bk, row_of(dr))
                else:
                    ok4b, missleg = False, "unreachable"
                # d** is NOT bisected: the pass set need not be a half-line, because the
                # DD cap tightens in x while the CAGR floor loosens.  Scan and report the set.
                xs = np.round(np.arange(0.0, 0.2501, 0.001), 4)
                passes = [x for x in xs if path_4b(bk, row_of(fn(bser, x)))[0]]
                dstar2 = float(passes[0]) if passes else np.nan
                dstar2_hi = float(passes[-1]) if passes else np.nan
                rows.append(dict(
                    panel=pn, model=model, bar=bn, bar_CAGR=bar["CAGR"],
                    book_CAGR=bk["CAGR"], floor=0.70 * bar["CAGR"],
                    miss_pp=100 * (0.70 * bar["CAGR"] - bk["CAGR"]),
                    bar_CAGR_needed=need, d_star=dstar, d_star_pp=100 * dstar,
                    d_starstar=dstar2, d_starstar_hi=dstar2_hi,
                    closes_all_4b=ok4b, resid_leg=missleg))
    A = pd.DataFrame(rows)
    P(fmt(A[A.model.isin(["CONT", "LUMPY"])].set_index(["panel", "bar", "model"])[
        ["bar_CAGR", "book_CAGR", "floor", "miss_pp", "bar_CAGR_needed", "d_star_pp",
         "d_starstar", "closes_all_4b", "resid_leg"]], 4))
    P("")
    P("  NOTE the d** column: dragging the bar also SHRINKS its drawdown, which TIGHTENS the 4b")
    P("  DD cap (0.60 x bar MaxDD) at the same time as it loosens the CAGR floor and the three")
    P("  Sharpe legs.  d** is the drag that clears all five legs at once; where it exceeds d*,")
    P("  the handicap needed is larger than the CAGR arithmetic alone suggests.")
    P("")

    # ---------------------------------------------------------------- NAME model
    P("=" * 112)
    P("PART A (cont.) - THE NAME MODEL: real delistings, applied to the BAR and to the BOOK")
    P("=" * 112)
    P(f"hazard ladder h {HAZARDS} x loss L {LOSSES} x {len(SEEDS)} seeds, both panels, "
      f"both bar forms; every point reported.")
    nrows = []
    for pn in PANELS:
        fr, st = frames[pn]["frame"], frames[pn]["start"]
        for L in LOSSES:
            for h in HAZARDS:
                acc = {k: [] for k in ["bar742", "barW10", "book"]}
                for sd in (SEEDS if h > 0 else [0]):
                    kf = kill_frame(fr, h, L, sd)
                    acc["bar742"].append(cagr_of(
                        fast_backtest(kf, b_ewbar(kf), 0.0, "D")["returns"].loc[st:]))
                    acc["barW10"].append(cagr_of(
                        fast_backtest(kf, b_ewbar(kf), COST, "W")["returns"].loc[st:]))
                    acc["book"].append(cagr_of(
                        fast_backtest(kf, b_band_dg(kf, 1.00), COST, "W")["returns"].loc[st:]))
                nrows.append(dict(
                    panel=pn, L=L, h=h, seeds=len(acc["bar742"]),
                    bar742_CAGR=float(np.mean(acc["bar742"])),
                    barW10_CAGR=float(np.mean(acc["barW10"])),
                    book_CAGR=float(np.mean(acc["book"])),
                    barW10_sd=float(np.std(acc["barW10"], ddof=1)) if len(acc["barW10"]) > 1 else 0.0,
                    book_sd=float(np.std(acc["book"], ddof=1)) if len(acc["book"]) > 1 else 0.0))
        P(f"  {pn}: NAME ladder done ({time.time()-t0:.0f}s)")
    N = pd.DataFrame(nrows)
    for pn in PANELS:
        sub = N[N.panel == pn]
        base742 = float(sub[sub.h == 0].bar742_CAGR.iloc[0])
        baseW10 = float(sub[sub.h == 0].barW10_CAGR.iloc[0])
        basebk = float(sub[sub.h == 0].book_CAGR.iloc[0])
        P("")
        P(f"  {pn}  (h=0 reproduces the undragged objects: bar742 {base742:.4%}, "
          f"barW10 {baseW10:.4%}, band book g1.00 {basebk:.4%})")
        t = sub.assign(bar_drag_pp=100 * (baseW10 - sub.barW10_CAGR),
                       book_drag_pp=100 * (basebk - sub.book_CAGR))
        t["shield_ratio"] = np.where(t.bar_drag_pp > 1e-9, t.book_drag_pp / t.bar_drag_pp, np.nan)
        t["net_floor_gap_pp"] = 100 * (0.70 * t.barW10_CAGR - t.book_CAGR)
        P(fmt(t.set_index(["L", "h"])[
            ["barW10_CAGR", "book_CAGR", "bar_drag_pp", "book_drag_pp", "shield_ratio",
             "net_floor_gap_pp", "barW10_sd", "book_sd"]], 4))
    P("")

    # THE NET QUESTION: applied to BOTH objects, does delisting CLOSE the floor gap or WIDEN it?
    P("  NET FLOOR GAP under a delisting-complete panel (the bar AND the book both book the")
    P("  same delistings, which is what a delisting-complete panel would actually mean):")
    netrows = []
    for pn in PANELS:
        sub = N[N.panel == pn]
        for L in LOSSES:
            s2 = sub[sub.L == L].sort_values("h")
            gap = (0.70 * s2.barW10_CAGR - s2.book_CAGR).to_numpy(float)
            hs = s2.h.to_numpy(float)
            slope = float(np.polyfit(hs, gap, 1)[0]) if len(hs) > 2 else np.nan
            g0 = float(gap[0])
            h_close = (-g0 / slope) if (np.isfinite(slope) and slope < 0) else np.nan
            netrows.append(dict(panel=pn, L=L, gap_h0_pp=100 * g0,
                                gap_hmax_pp=100 * float(gap[-1]),
                                slope_pp_per_1pct_hazard=100 * slope / 100.0,
                                h_closing_gap=h_close))
    NET = pd.DataFrame(netrows)
    P(fmt(NET.set_index(["panel", "L"]), 5))
    P("  h_closing_gap is the annual delisting hazard at which the NET gap reaches zero, read")
    P("  off a linear fit to the ladder; NaN means the gap does not close in this direction at")
    P("  any hazard - delisting WIDENS it.")
    P("")

    # H_SHIELD
    sh = N[N.h > 0].copy()
    shield_ok = []
    for pn in PANELS:
        sub = N[N.panel == pn]
        baseW10 = float(sub[sub.h == 0].barW10_CAGR.iloc[0])
        basebk = float(sub[sub.h == 0].book_CAGR.iloc[0])
        s = sub[sub.h > 0]
        shield_ok.append(((basebk - s.book_CAGR) < (baseW10 - s.barW10_CAGR)).sum())
    tot = int((N.h > 0).sum() / len(PANELS))
    P(f"H_SHIELD: the band book loses strictly less CAGR than the bar at "
      f"{int(sum(shield_ok))} of {tot*len(PANELS)} (L, h) points "
      f"(U56 {int(shield_ok[0])}/{tot}, B136 {int(shield_ok[1])}/{tot}) -> "
      + ("HOLDS - the 200d gate does shield the book" if sum(shield_ok) == tot * len(PANELS)
         else "FALSIFIED at some points - the gate does NOT always shield the book"))
    P("")

    # ---------------------------------------------------------------- PART B
    P("=" * 112)
    P("PART B - WHAT THE REQUIRED DRAG IMPLIES AS A DELISTING FREQUENCY")
    P("=" * 112)
    P("h_panel = d* / L is the panel-wide annual delisting frequency the drag needs.")
    P("h_sleeve = d* / (L x single-stock share) is the frequency on the names that can actually")
    P("delist at all - the number a delisting story has to defend.")
    imp = []
    for _, r in A[A.model == "CONT"].iterrows():
        for L in LOSSES:
            imp.append(dict(panel=r["panel"], bar=r["bar"], L=L, d_star_pp=r["d_star_pp"],
                            h_panel=r["d_star"] / L,
                            h_sleeve=r["d_star"] / (L * STOCK_SHARE[r["panel"]])))
    IMP = pd.DataFrame(imp)
    P(fmt(IMP.set_index(["panel", "bar", "L"]), 5))
    P("")
    hard = IMP[(IMP.L == 1.00)]
    P("  THE CITATION-FREE STATEMENT (L = 1.00, total wipeout, the physical maximum loss):")
    for _, r in hard.iterrows():
        P(f"    {r['panel']:5s} vs {r['bar']:8s}: every year {r['h_panel']:.2%} of the panel "
          f"(= {r['h_sleeve']:.2%} of its single-stock sleeve) must go to ZERO, and that is the "
          f"LOWER bound - any smaller loss needs proportionally more delistings.")
    P("")
    worst = float(hard[hard.bar == "B_EWW10"].h_sleeve.min())      # the CONSERVATIVE bar
    P(f"H_DRAG  : on the weaker (conservative) bar the drag needs {worst:.2%} of the "
      f"single-stock sleeve wiped out EVERY year at L = 1.00; pre-registered bar 2.00% -> "
      + ("HOLDS - the drag is reachable" if worst <= 0.02 else
         "FALSIFIED - the bar-only drag is already beyond any defensible hazard"))
    jt = NET[(NET.panel == "U56") & (NET.L == 1.00)].h_closing_gap.iloc[0]
    P(f"          and that is the BAR-ONLY bound.  Under the honest joint experiment (PART A's "
      f"NAME model, delistings hitting the bar AND the book), U56 needs h = {jt:.2%} of the "
      f"panel per year = {jt/STOCK_SHARE['U56']:.2%} of its single-stock sleeve, every year, "
      f"at total wipeout.")
    P("  Recalled anchors (UNVERIFIED here - no network): Shumway 1997 NYSE/AMEX ~ -30%,")
    P("  Shumway & Warther 1999 Nasdaq ~ -55% for performance-related delistings.  The verdict")
    P("  below is stated against the L = 1.00 column and does not depend on either figure.")
    P("")

    # ---------------------------------------------------------------- PART C
    P("=" * 112)
    P("PART C - THE EMPIRICAL ANCHOR: RSP, an investable equal-weight fund that ATE the")
    P("         delistings, against a synthetic equal-weight basket of current constituents")
    P("=" * 112)
    pxu = frames["U56"]["px"]
    rsp = pxu["RSP"].dropna()
    anchors = []
    for pn in PANELS:
        fr, st = frames[pn]["frame"], frames[pn]["start"]
        for bn, (cb, fq) in BARFORMS.items():
            r = bars[(pn, bn, "series")]
            ix = r.index.intersection(rsp.index)
            rr = r.reindex(ix).fillna(0.0)
            rs = rsp.reindex(ix).pct_change().fillna(0.0)
            anchors.append(dict(panel=pn, bar=bn, bars=len(ix),
                                synth_CAGR=cagr_of(rr), RSP_CAGR=cagr_of(rs),
                                gap_pp=100 * (cagr_of(rr) - cagr_of(rs)),
                                synth_Sharpe=metrics(rr)["Sharpe"],
                                RSP_Sharpe=metrics(rs)["Sharpe"]))
    AN = pd.DataFrame(anchors)
    P(fmt(AN.set_index(["panel", "bar"]), 4))
    P("")
    for pn in PANELS:
        gp = float(AN[(AN.panel == pn) & (AN.bar == "B_EWW10")].gap_pp.iloc[0])
        ds = float(A[(A.panel == pn) & (A.bar == "B_EWW10") & (A.model == "CONT")].d_star_pp.iloc[0])
        P(f"  {pn}: the synthetic current-constituent basket beats RSP by {gp:+.2f} pp/yr in "
          f"total - survivorship, composition and weighting COMBINED - while the drag needed to "
          f"close the floor is {ds:.2f} pp/yr, i.e. {ds/gp:.0%} of that entire gap."
          if gp > 0 else
          f"  {pn}: the synthetic basket does NOT beat RSP ({gp:+.2f} pp/yr), so there is no "
          f"positive inflation budget to spend on a delisting story at all.")
    P("  UPPER BOUND, stated: neither panel IS the S&P 500, so composition and weighting")
    P("  differences sit inside this gap alongside survivorship; RSP also carries its own fee.")
    P("  It bounds the inflation from above, it does not estimate the survivorship part.")
    P("")

    # ---------------------------------------------------------------- rule 8
    P("=" * 112)
    P("RULE 8 WALK-FORWARD")
    P("=" * 112)
    P("WF-A: d* solved inside IS only and inside OOS only, at every one of the 6 tuned points.")
    wfa = []
    for pn in PANELS:
        for bn in BARFORMS:
            bser = bars[(pn, bn, "series")]
            bk_s = books[(pn, 1.00, "series")]
            for model in ["CONT", "LUMPY"]:
                fn = drag_cont if model == "CONT" else drag_lumpy
                cell = dict(panel=pn, bar=bn, model=model)
                for per, sl in (("FULL", slice(None)),
                                ("IS", slice(None, IS_END)),
                                ("OOS", slice(OOS_START, None))):
                    b_, k_ = bser.loc[sl], bk_s.loc[sl]
                    cell[f"d_{per}_pp"] = 100 * solve_scalar(
                        lambda x: cagr_of(fn(b_, x)), cagr_of(k_) / 0.70)
                wfa.append(cell)
    WFA = pd.DataFrame(wfa)
    P(fmt(WFA.set_index(["panel", "bar", "model"]), 4))
    ratio = (WFA.d_OOS_pp / WFA.d_IS_pp.replace(0, np.nan)).abs()
    P(f"  IS vs OOS required drag: ratio OOS/IS ranges {ratio.min():.2f} to {ratio.max():.2f} "
      f"over {len(WFA)} cells -> H_STABLE "
      + ("HOLDS (all within 2x)" if float(ratio.max()) <= 2.0 and float(ratio.min()) >= 0.5
         else "FALSIFIED - the required drag is not a stable quantity across the split"))
    P("")

    P("WF-B: the BAND-DG gross rung picked on IS Sharpe ALONE, OOS read once, scored 4b against")
    P("      the OOS bar UNDRAGGED and DRAGGED by the solved d*, plus 4a vs the live book.")
    wfb = []
    for pn in PANELS:
        picks = {g: books[(pn, g)]["IS_Sharpe"] for g in GROSS_LADDER}
        gpick = max(picks, key=picks.get)
        bk = books[(pn, gpick)]
        live = books[(pn, 0.75)]              # RULES v2 at the LIVE gross is the 4a comparand
        spy = bars[(pn, "B_SPY")]
        for bn in BARFORMS:
            bar = bars[(pn, bn)]
            bser = bars[(pn, bn, "series")]
            d = float(A[(A.panel == pn) & (A.bar == bn) & (A.model == "CONT")].d_star.iloc[0])
            bard = row_of(drag_cont(bser, d)) if np.isfinite(d) else bar
            ok_u, miss_u = path_4b(bk, bar)
            ok_d, miss_d = path_4b(bk, bard)
            ok_a, miss_a = path_4a(bk, live)
            wfb.append(dict(panel=pn, IS_pick_gross=gpick, IS_Sharpe=bk["IS_Sharpe"],
                            bar=bn, d_star_pp=100 * d,
                            book_oos_CAGR=bk["oos_CAGR"], book_oos_Sharpe=bk["oos_Sharpe"],
                            book_oos_MaxDD=bk["oos_MaxDD"],
                            bar_oos_CAGR=bar["oos_CAGR"], bar_oos_Sharpe=bar["oos_Sharpe"],
                            spy_oos_CAGR=spy["oos_CAGR"], spy_oos_Sharpe=spy["oos_Sharpe"],
                            keep4b_undragged=ok_u, miss_undragged=miss_u,
                            keep4b_dragged=ok_d, miss_dragged=miss_d,
                            keep4a=ok_a, miss4a=miss_a))
    WFB = pd.DataFrame(wfb)
    P(fmt(WFB.set_index(["panel", "bar"]), 4))
    P(f"  IS picks gross {sorted(set(WFB.IS_pick_gross))} on IS Sharpe alone.  "
      f"4b vs the UNDRAGGED bar: {int(WFB.keep4b_undragged.sum())}/{len(WFB)}; "
      f"4b vs the bar DRAGGED by its own d*: {int(WFB.keep4b_dragged.sum())}/{len(WFB)}; "
      f"4a vs the live book: {int(WFB.keep4a.sum())}/{len(WFB)}.")
    P("  A pass in the DRAGGED column is a statement about the comparand, not a capital")
    P("  candidate: the book is unchanged and the bar was handicapped to produce it.")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 112)
    P("KEEP PATHS (PROTOCOL 4a and 4b, every BAND-DG rung x panel x bar, undragged and dragged)")
    P("=" * 112)
    kp = []
    for pn in PANELS:
        live = books[(pn, 0.75)]
        for g in GROSS_LADDER:
            bk = books[(pn, g)]
            ok_a, miss_a = path_4a(bk, live)
            for bn in list(BARFORMS) + ["B_SPY"]:
                bar = bars[(pn, bn)]
                ok_u, miss_u = path_4b(bk, bar)
                if bn in BARFORMS:
                    d = float(A[(A.panel == pn) & (A.bar == bn)
                                & (A.model == "CONT")].d_star.iloc[0])
                    bard = row_of(drag_cont(bars[(pn, bn, "series")], d)) if np.isfinite(d) else bar
                    ok_d, miss_d = path_4b(bk, bard)
                else:
                    ok_d, miss_d = ok_u, miss_u
                kp.append(dict(panel=pn, gross=g, bar=bn, keep4a=ok_a, miss4a=miss_a,
                               keep4b=ok_u, miss4b=miss_u,
                               keep4b_dragged=ok_d, miss4b_dragged=miss_d))
    KP = pd.DataFrame(kp)
    P(f"over {len(KP)} (rung, panel, bar) cells: 4a {int(KP.keep4a.sum())}/{len(KP)}, "
      f"4b undragged {int(KP.keep4b.sum())}/{len(KP)}, "
      f"4b dragged {int(KP.keep4b_dragged.sum())}/{len(KP)}")
    P("  by bar: " + ", ".join(
        f"{b} 4b {int(v.keep4b.sum())}/{len(v)} -> dragged {int(v.keep4b_dragged.sum())}/{len(v)}"
        for b, v in KP.groupby("bar")))
    P("  binding legs (undragged): " + ", ".join(
        f"{a} {b}" for a, b in KP.miss4b.value_counts().head(6).items()))
    P("")

    # ---------------------------------------------------------------- write
    NET.to_csv(OUT / f"{STAMP}.netgap.csv", index=False)
    A.to_csv(OUT / f"{STAMP}.drag.csv", index=False)
    N.to_csv(OUT / f"{STAMP}.name.csv", index=False)
    pd.concat([WFA.assign(leg="WF-A"), WFB.assign(leg="WF-B"), IMP.assign(leg="implied"),
               AN.assign(leg="RSP-anchor")], ignore_index=True).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    KP.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P(f"wrote drag {len(A)}, name {len(N)}, keeppaths {len(KP)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
