#!/usr/bin/env python3
"""Idea 323 - "is-every-4b-KEEP-in-the-record-a-10bps-ARTEFACT" (lane C, 2026-09-07).

The question
------------
Idea 47 swept cost x lag on FOUR books of one family (the fixed-n / fixed-fraction family)
and found **0 of 180 cells pass 4b at 25 or 50 bps** while 19/36 pass at 0-5 bps.  The queue
asks whether that is a property of that family or of PROTOCOL rule 4b itself: re-run the
record's OTHER standing 4b passes -- idea 46's F085, idea 2's N20, the band b=0.12 cell
(idea 291), the breadth CASH gate (idea 48), and RULES v2, the LIVE book -- on a cost ladder
and count how many survive 25 bps.  If ~0, 4b needs a cost rung written into it and the live
book needs a turnover budget.

What is swept (the two tuned parameters - PROTOCOL rule 4)
----------------------------------------------------------
    cost_bps in {0, 5, 10, 15, 20, 25, 30, 40, 50}      (PROTOCOL's anchor is 10)
    cadence  in {W, M, Q}                                (the record's turnover dial)
27 cells per book per panel; 7 books x 2 panels x 27 = **378 cells, ALL reported**.
Cadence is included because the queue's second clause is a TURNOVER budget: if any book can
be bought back above 25 bps, slowing it is the record's cheapest instrument for doing so.

What is FIXED in advance and NOT searched (every book is the record's own, verbatim)
-----------------------------------------------------------------------------------
    N20     top 20 at 0.75/20, de-grossing when E_t < 20        idea 2's KEEP (2026-09-03)
    F085    top ceil(0.85*E_t) at 0.75/k                        idea 46's 4b passer
    BAND12  200d band b=0.12, RESPREAD, 0.75 gross              idea 291's PARKed 4b passer
    BRCASH  N20's broad leg, flat when E_t <= causal q0.20       idea 48's by-product
    RULESv2 200d band b=0.03, DEGROSS to cash, 0.75 gross        the LIVE book
    NF20    top min(20,E_t) at 0.75/min(20,E_t)                 control (N20 minus cash sleeve)
    EWALL   every live name at 0.75/N                           do-nothing control
Scorer for the ranked books is RULES v1's composite WITHOUT /sqrt(vol20) (the candidates'
own), eligibility = above 200d MA and vol20 < 0.60, gross 0.75 everywhere, next-day fill.

Mechanics
---------
Costs : held weights and turnover do not depend on cost_bps, so the nine rungs come from ONE
        zero-cost run per (book, cadence, panel) as r_c = r_0 - turnover * c/1e4.  Gated
        against engine.backtest at 10 bps on every cell; the script aborts if max|diff| > 1e-12.
Breakeven: for each 4b bar (H1, H2, OOS, DD, CAGR) the margin is evaluated on the ladder and
        the crossing linearly interpolated between adjacent rungs -> the cost at which the
        book stops being capital-worthy.  min over bars = the book's 4b breakeven.
Budget : the Sharpe drag per 10 bps is regressed on the ladder; combined with the breakeven
        this gives the annual turnover a book may spend and still clear 4b at a 25 bps rung.
Rule 8: at EVERY (panel, cost) cell the book x cadence is chosen on 2009-2016 only, under two
        rules fixed in advance (S1 = best IS Sharpe; S2 = best IS Sharpe among cells clearing
        the IS 4b bars), and evaluated untouched on 2017-2026 against the do-nothing anchor
        (N20 weekly), RULES v2 and SPY.

SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current-constituent lists,
so absolute CAGRs are optimistic on both panels.  This run holds names, days, filter, gross
and fill fixed and moves ONLY the cost rung and the cadence, so the cost comparison is far
less exposed than the levels are -- that is the durable part.  SMALL439 is not re-run here:
idea 47 already reported 0/60 on it at every cost and lag.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

GROSS = 0.75
MAX_VOL = 0.60
VOL_SCALE = False                 # the candidates' own scorer
N0 = 20
F085 = 0.85
BAND_WIDE = 0.12                  # idea 291's cell
BAND_LIVE = 0.03                  # RULES v2
Q_NARROW = 0.20                   # idea 48's pre-registered bottom quintile
MIN_OBS = 252
COSTS = [0, 5, 10, 15, 20, 25, 30, 40, 50]        # tuned parameter 1
CADENCES = ["W", "M", "Q"]                        # tuned parameter 2
ANCHOR_COST = 10
RUNG = 25                                         # the queue's rung
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOKS = ["N20", "F085", "BAND12", "BRCASH", "RULESv2", "NF20", "EWALL"]
STANDING = ["N20", "F085", "BAND12", "BRCASH", "RULESv2"]   # the record's standing 4b passes
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- book construction
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def eligible_count(px):
    e = eligible_mask(px).sum(axis=1).astype(float)
    ma_ok = px.rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px):
    return score(px, vol_scale=VOL_SCALE)[0].where(eligible_mask(px)).rank(axis=1, ascending=False)


def weights_from_k(rank, k, gross):
    k = k.clip(lower=1.0)
    w_per = gross / k if np.isscalar(gross) else gross.div(k)
    return rank.le(k, axis=0).astype(float).mul(w_per, axis=0)


def narrow_flag(e, q=Q_NARROW):
    """Causal: E_t <= expanding q-quantile of E over history up to t-1."""
    thr = e.expanding(min_periods=MIN_OBS).quantile(q).shift(1)
    return (e <= thr).where(thr.notna() & e.notna(), False)


def build(px, book):
    rank = ranked(px)
    e = eligible_count(px).fillna(0.0)
    if book == "N20":
        return weights_from_k(rank, pd.Series(float(N0), index=px.index), GROSS)
    if book == "NF20":
        return weights_from_k(rank, np.minimum(float(N0), e), GROSS)
    if book == "F085":
        return weights_from_k(rank, np.ceil(F085 * e), GROSS)
    if book == "BRCASH":
        w = weights_from_k(rank, np.minimum(float(N0), e), GROSS)
        return w.where(~narrow_flag(eligible_count(px)), 0.0)
    if book == "BAND12":                              # RESPREAD: always 75% among IN names
        g = band_state(px, BAND_WIDE) & live_mask(px)
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0) * GROSS
    if book == "RULESv2":                             # DEGROSS: gated-out weight -> cash
        return rules_v2_weights(px, band=BAND_LIVE, gross=GROSS)
    if book == "EWALL":
        live = live_mask(px)
        return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS
    raise ValueError(book)


# ---------------------------------------------------------------- fast zero-cost backtest
def fast_bt(px, w, freq):
    """engine.backtest at cost_bps=0, in numpy.  Returns (returns, turnover, names, gross)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n); turn = np.zeros(n); nm = np.zeros(n); gr = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        nm[i] = float((cur > 0).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(nm, index=idx), pd.Series(gr, index=idx))


# ---------------------------------------------------------------- metrics / bars
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def margins_4b(r, spy):
    """Signed margin of every 4b bar; ALL must be > 0 to pass."""
    c, s, dd = m3(r); h1, h2 = halves(r)
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    return {"H1": h1 - s1,
            "H2": h2 - s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"],
            "DD": 0.60 * abs(sdd) - abs(dd),
            "CAGR": c - 0.70 * sc}


def fail_4b(mg):
    bad = [k for k, v in mg.items() if v <= 0]
    return ",".join(bad) if bad else "-"


def fail_4a(r, base):
    h1, h2 = halves(r); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if m3(r)[2] < m3(base)[2]: bad.append("DD")
    return ",".join(bad) if bad else "-"


def crossing(costs, margins):
    """Linear interpolation of the cost at which a margin first turns <= 0.
    Returns np.nan if it never crosses inside the ladder; 0.0 if already <= 0 at c=0."""
    if margins[0] <= 0:
        return 0.0
    for i in range(1, len(costs)):
        if margins[i] <= 0:
            x0, x1 = costs[i - 1], costs[i]
            y0, y1 = margins[i - 1], margins[i]
            return x0 + (x1 - x0) * y0 / (y0 - y1)
    return np.nan


# ---------------------------------------------------------------- panels
def build_panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    return [("U56", px56), ("B136", px136)]


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 170)
    P(f"Idea 323  is-every-4b-KEEP-in-the-record-a-10bps-ARTEFACT  (lane C, 2026-09-07) | {SCRIPT}")
    P("=" * 170)
    P(f"Swept (2 params): cost_bps {COSTS} x cadence {CADENCES} = {len(COSTS)*len(CADENCES)} "
      f"cells per book per panel, ALL reported.")
    P(f"Books fixed in advance, the record's own: {BOOKS}   (standing 4b passes: {STANDING})")
    P("Premise under test (idea 47): every 4b pass in the record sits at <= 10 bps, "
      "i.e. at PROTOCOL's own anchor and below.")
    P("")

    panels = build_panels()
    grid_rows, be_rows, wf_rows = [], [], []
    sig_map = {}
    gate_max = 0.0

    for panel, px in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        P("=" * 170)
        P(f"PANEL {panel}: {px.shape[1]} columns | {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval from {start.date()} | index sanity 2018={yrs.get(2018)}, 2024={yrs.get(2024)}")
        sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
        soos = metrics(spy.loc[OOS_START:])["Sharpe"]
        P(f"  SPY: CAGR {sc:.2%} Sharpe {ss:.3f} ({s1:.3f}/{s2:.3f}) MaxDD {sdd:.2%} OOS {soos:.3f}"
          f"  ->  4b bars: H1>{s1:.3f} H2>{s2:.3f} OOS>{soos:.3f} DD<{0.60*abs(sdd):.2%} "
          f"CAGR>{0.70*sc:.2%}")

        wmap = {b: build(px, b) for b in BOOKS}
        base_r = {}       # (book, cadence) -> zero-cost returns / turnover, for cost ladder

        # RULES v2 weekly is the 4a comparand (PROTOCOL rule 3), priced at the SAME rung
        v2r, v2t, _, _ = fast_bt(px, wmap["RULESv2"], "W")
        v2r, v2t = v2r.loc[start:], v2t.loc[start:]

        for book in BOOKS:
            for cad in CADENCES:
                r0, turn, nm, gg = fast_bt(px, wmap[book], cad)
                r0, turn, nm, gg = r0.loc[start:], turn.loc[start:], nm.loc[start:], gg.loc[start:]
                # harness gate: analytic cost == engine.backtest at the anchor rung
                eng = backtest(px, wmap[book], cost_bps=ANCHOR_COST, freq=cad)["returns"].loc[start:]
                d = float((r0 - turn * ANCHOR_COST / 1e4 - eng).abs().max())
                gate_max = max(gate_max, d)
                if d > 1e-12:
                    P(f"!! COST-IDENTITY GATE FAILED for {panel}/{book}/{cad}: {d:.3e} - aborting.")
                    sys.exit(1)
                base_r[(book, cad)] = (r0, turn)
                sig_map[(panel, book, cad)] = float(r0.std() * np.sqrt(252))
                yrs_n = (r0.index[-1] - r0.index[0]).days / 365.25
                to_yr = float(turn.sum()) / yrs_n
                for c in COSTS:
                    r = r0 - turn * c / 1e4
                    cg, sh, dd = m3(r); h1, h2 = halves(r)
                    mg = margins_4b(r, spy)
                    grid_rows.append(dict(panel=panel, book=book, cadence=cad, cost=c,
                                          CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                                          OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                          OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                          OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                          turnover_yr=to_yr, names=float(nm.mean()),
                                          gross=float(gg.mean()),
                                          m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"],
                                          m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                                          fail4b=fail_4b(mg), pass4b=fail_4b(mg) == "-",
                                          fail4a=fail_4a(r, v2r - v2t * c / 1e4)))

        grid = pd.DataFrame(grid_rows)
        grid["pass4a"] = grid["fail4a"] == "-"
        gp = grid[grid.panel == panel]

        # -------- the census answer
        P(f"\n  [1] 4b PASSES BY COST RUNG (rows = book, cols = bps; each cell is x/3 cadences)")
        P(f"      {'book':9s} " + " ".join(f"{c:>7d}" for c in COSTS))
        for book in BOOKS:
            d = gp[gp.book == book]
            P(f"      {book:9s} " + " ".join(
                f"{int(d[d.cost==c].pass4b.sum()):>4d}/{len(CADENCES):<2d}" for c in COSTS))
        P(f"      {'TOTAL':9s} " + " ".join(
            f"{int(gp[gp.cost==c].pass4b.sum()):>3d}/{len(BOOKS)*len(CADENCES):<3d}" for c in COSTS))
        P(f"      4a passes (vs RULES v2 at the same rung): " + " ".join(
            f"{c}bps={int(gp[gp.cost==c].pass4a.sum())}" for c in COSTS))

        # -------- per-book breakeven and turnover budget
        P(f"\n  [2] 4b BREAKEVEN COST per book x cadence (bps; interpolated on the ladder; "
          f"'never' = clears all bars at 50 bps, '0' = fails at zero cost)")
        P(f"      {'book':9s} {'cad':4s} {'turn/yr':>8s} {'names':>6s} {'gross':>6s} "
          f"{'dSh/10bp':>9s} " + " ".join(f"{k:>7s}" for k in ["H1", "H2", "OOS", "DD", "CAGR"])
          + f" {'4b BE':>7s} {'bar@10':>10s} {'pass@25':>7s}")
        for book in BOOKS:
            for cad in CADENCES:
                d = gp[(gp.book == book) & (gp.cadence == cad)].sort_values("cost")
                cs = list(d.cost)
                bes = {k: crossing(cs, list(d["m_" + k])) for k in ["H1", "H2", "OOS", "DD", "CAGR"]}
                fin = [v for v in bes.values() if not np.isnan(v)]
                be = min(fin) if fin else np.nan
                slope = np.polyfit(cs, list(d.Sharpe), 1)[0] * 10.0
                p25 = bool(d[d.cost == RUNG].pass4b.iloc[0])
                be_rows.append(dict(panel=panel, book=book, cadence=cad,
                                    turnover_yr=float(d.turnover_yr.iloc[0]),
                                    names=float(d.names.iloc[0]), gross=float(d.gross.iloc[0]),
                                    dSharpe_per_10bps=slope, be_4b=be, pass25=p25,
                                    **{f"be_{k}": v for k, v in bes.items()}))
                fs = lambda v: ("never" if np.isnan(v) else f"{v:.1f}")
                P(f"      {book:9s} {cad:4s} {d.turnover_yr.iloc[0]:8.2f} {d.names.iloc[0]:6.1f} "
                  f"{d.gross.iloc[0]:6.3f} {slope:9.4f} "
                  + " ".join(f"{fs(bes[k]):>7s}" for k in ["H1", "H2", "OOS", "DD", "CAGR"])
                  + f" {fs(be):>7s} {d[d.cost==ANCHOR_COST].fail4b.iloc[0]:>10s} "
                  f"{('YES' if p25 else 'no'):>7s}")

        # -------- the full grid, printed
        P(f"\n  [3] FULL GRID (all {len(gp)} cells on {panel})")
        show = gp[["book", "cadence", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "OOS_Sharpe", "turnover_yr", "fail4b", "fail4a"]].copy()
        P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

        # -------- rule 8 walk-forward, at every cost rung
        P(f"\n  [4] RULE 8 WALK-FORWARD on {panel}: book x cadence chosen on <= {IS_END}, "
          f"2017- read once.  S1 = best IS Sharpe, S2 = best IS Sharpe among IS-4b clearers.")
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for c in COSTS:
            cells = {}
            for book in BOOKS:
                for cad in CADENCES:
                    r0, turn = base_r[(book, cad)]
                    r = r0 - turn * c / 1e4
                    ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
                    h = len(ris) // 2
                    is_mg = {"H1": metrics(ris.iloc[:h])["Sharpe"] - metrics(spy_is.iloc[:h])["Sharpe"],
                             "H2": metrics(ris.iloc[h:])["Sharpe"] - metrics(spy_is.iloc[h:])["Sharpe"],
                             "DD": 0.60 * abs(m3(spy_is)[2]) - abs(m3(ris)[2]),
                             "CAGR": m3(ris)[0] - 0.70 * m3(spy_is)[0]}
                    cells[(book, cad)] = dict(is_sharpe=metrics(ris)["Sharpe"],
                                              is_ok=all(v > 0 for v in is_mg.values()),
                                              oos_sharpe=metrics(roos)["Sharpe"],
                                              oos_cagr=metrics(roos)["CAGR"],
                                              oos_dd=metrics(roos)["MaxDD"])
            s1 = max(cells, key=lambda k: cells[k]["is_sharpe"])
            ok = [k for k in cells if cells[k]["is_ok"]]
            s2 = max(ok, key=lambda k: cells[k]["is_sharpe"]) if ok else None
            best = max(cells, key=lambda k: cells[k]["oos_sharpe"])
            anchor = ("N20", "W")
            live = ("RULESv2", "W")
            for tag, pick in [("S1", s1), ("S2", s2)]:
                if pick is None:
                    P(f"      c={c:>2d} {tag}: no IS-4b clearer at this rung -> no pick")
                    wf_rows.append(dict(panel=panel, cost=c, rule=tag, pick="none"))
                    continue
                oo = cells[pick]
                wf_rows.append(dict(panel=panel, cost=c, rule=tag, pick=f"{pick[0]}/{pick[1]}",
                                    oos_sharpe=oo["oos_sharpe"], oos_cagr=oo["oos_cagr"],
                                    oos_dd=oo["oos_dd"],
                                    anchor_oos=cells[anchor]["oos_sharpe"],
                                    live_oos=cells[live]["oos_sharpe"],
                                    spy_oos=metrics(spy_oos)["Sharpe"],
                                    best_oos=cells[best]["oos_sharpe"],
                                    regret=cells[best]["oos_sharpe"] - oo["oos_sharpe"],
                                    beats_anchor=oo["oos_sharpe"] > cells[anchor]["oos_sharpe"],
                                    beats_spy=oo["oos_sharpe"] > metrics(spy_oos)["Sharpe"],
                                    beats_live=oo["oos_sharpe"] > cells[live]["oos_sharpe"]))
                P(f"      c={c:>2d} {tag}: pick {pick[0]}/{pick[1]:<2s} -> OOS "
                  f"{oo['oos_cagr']:7.2%} / {oo['oos_sharpe']:.3f} / {oo['oos_dd']:7.2%} | "
                  f"anchor N20/W {cells[anchor]['oos_sharpe']:.3f} | "
                  f"RULESv2/W {cells[live]['oos_sharpe']:.3f} | SPY {metrics(spy_oos)['Sharpe']:.3f} | "
                  f"OOS-best {best[0]}/{best[1]} {cells[best]['oos_sharpe']:.3f} "
                  f"(regret {cells[best]['oos_sharpe']-oo['oos_sharpe']:.4f})")

    grid = pd.DataFrame(grid_rows)
    grid["pass4a"] = grid["fail4a"] == "-"
    be = pd.DataFrame(be_rows)
    wf = pd.DataFrame(wf_rows)

    # ---------------------------------------------------------------- headline
    P("\n" + "=" * 170)
    P("ANSWER")
    P("=" * 170)
    P(f"Cost-identity gate: max|analytic - engine| = {gate_max:.3e} over all "
      f"{len(BOOKS)*len(CADENCES)*len(panels)} (book, cadence, panel) cells at {ANCHOR_COST} bps.")
    tot = len(grid)
    P(f"\nTotal cells: {tot}.  4b passes {int(grid.pass4b.sum())}/{tot}, "
      f"4a passes {int(grid.pass4a.sum())}/{tot}.")
    P("\n4b passes by cost rung, pooled over both panels, all 7 books, all 3 cadences:")
    P(f"  {'bps':>5s} " + " ".join(f"{c:>6d}" for c in COSTS))
    P(f"  {'pass':>5s} " + " ".join(f"{int(grid[grid.cost==c].pass4b.sum()):>6d}" for c in COSTS))
    P(f"  {'of':>5s} " + " ".join(f"{len(grid[grid.cost==c]):>6d}" for c in COSTS))
    st = grid[grid.book.isin(STANDING) & (grid.cadence == "W")]
    P(f"\nThe record's five STANDING 4b passes at their own WEEKLY cadence "
      f"({len(STANDING)} books x 2 panels = {len(st)//len(COSTS)} cells per rung):")
    P(f"  {'bps':>5s} " + " ".join(f"{c:>6d}" for c in COSTS))
    P(f"  {'pass':>5s} " + " ".join(f"{int(st[st.cost==c].pass4b.sum()):>6d}" for c in COSTS))
    n25 = int(st[st.cost == RUNG].pass4b.sum())
    P(f"\n=> AT {RUNG} BPS: {n25} of {len(st)//len(COSTS)} standing weekly cells survive 4b.")
    if n25:
        P("   Survivors:")
        for _, r in st[(st.cost == RUNG) & st.pass4b].iterrows():
            P(f"     {r.panel}/{r.book}: {r.CAGR:.2%} / {r.Sharpe:.3f} / {r.MaxDD:.2%} "
              f"(H1 {r.H1:.3f}, H2 {r.H2:.3f}, OOS {r.OOS_Sharpe:.3f}), turnover {r.turnover_yr:.2f}/yr")
    P("\nWhole-grid survivors at {} bps (any cadence):".format(RUNG))
    surv = grid[(grid.cost == RUNG) & grid.pass4b]
    if len(surv) == 0:
        P("   NONE.")
    else:
        for _, r in surv.iterrows():
            P(f"     {r.panel}/{r.book}/{r.cadence}: {r.CAGR:.2%} / {r.Sharpe:.3f} / {r.MaxDD:.2%} "
              f"(H1 {r.H1:.3f}, H2 {r.H2:.3f}, OOS {r.OOS_Sharpe:.3f}), turnover {r.turnover_yr:.2f}/yr")

    P("\nTURNOVER BUDGET.  Sharpe drag per 10 bps against annual turnover "
      "(theory: drag ~ -turnover*c / annualised vol):")
    bb = be.dropna(subset=["dSharpe_per_10bps"])
    sl = np.polyfit(bb.turnover_yr, bb.dSharpe_per_10bps, 1)
    P(f"  fit  dSharpe/10bps = {sl[0]:.5f} * turnover_yr + {sl[1]:.5f}   "
      f"(corr {np.corrcoef(bb.turnover_yr, bb.dSharpe_per_10bps)[0,1]:.3f}, n={len(bb)})")
    never = be[be.be_4b == 0.0]
    P(f"  {len(never)}/{len(be)} cells fail 4b already at ZERO cost (no breakeven to speak of): "
      + ", ".join(f"{r.panel}/{r.book}/{r.cadence}" for _, r in never.iterrows()))
    fin = be[(be.be_4b > 0) | be.be_4b.isna()].copy()
    fin["be_plot"] = fin.be_4b.fillna(float(max(COSTS)))     # 'never crosses' -> 50 bps floor
    if len(fin) > 1:
        P(f"  of the {len(fin)} cells that DO pass at 0 bps: breakeven vs turnover corr "
          f"{np.corrcoef(fin.turnover_yr, fin.be_plot)[0,1]:.3f}; median "
          f"{fin.be_plot.median():.1f} bps, {int(fin.be_4b.isna().sum())} never cross 50 bps")
        P("  " + fin.sort_values("be_plot", ascending=False)[
            ["panel", "book", "cadence", "turnover_yr", "be_4b"]].to_string(
            index=False, float_format=lambda x: f"{x:.2f}"))
    ok25 = be[be.pass25]
    if len(ok25):
        P(f"  cells clearing 4b at {RUNG} bps have turnover {ok25.turnover_yr.min():.2f}-"
          f"{ok25.turnover_yr.max():.2f}/yr; cells failing it, "
          f"{be[~be.pass25].turnover_yr.min():.2f}-{be[~be.pass25].turnover_yr.max():.2f}/yr")
        P(f"  => an implied TURNOVER BUDGET at a {RUNG} bps rung: <= "
          f"{ok25.turnover_yr.max():.2f}x NAV per year on these panels.")
    else:
        P(f"  no cell clears 4b at {RUNG} bps, so no turnover is small enough on these panels: "
          f"the budget is not a turnover question at this rung.")

    P("\nCLOSED FORM for the budget.  Cost enters returns as -T*c, so Sharpe(c) = (mu - T*c)/sigma"
      " and\n  c*_bps = 1e4 * margin * sigma / T   for a Sharpe bar, and 1e4 * margin / T for the"
      " CAGR floor.\n  Predicted vs measured 4b breakeven, for every cell that passes at 0 bps "
      "(DD-limited cells excepted: cost moves DD only through the equity path, not linearly):")
    P(f"  {'panel':5s} {'book':8s} {'cad':4s} {'T/yr':>6s} {'sigma':>6s} {'bar':>6s} "
      f"{'pred':>7s} {'meas':>7s} {'err':>7s}")
    pred_err = []
    for _, r in be.iterrows():
        d0 = grid[(grid.panel == r.panel) & (grid.book == r.book)
                  & (grid.cadence == r.cadence) & (grid.cost == 0)].iloc[0]
        if d0.fail4b != "-":
            continue
        sig = float(sig_map[(r.panel, r.book, r.cadence)])
        cand = {"H1": d0.m_H1 * sig, "H2": d0.m_H2 * sig, "OOS": d0.m_OOS * sig,
                "CAGR": d0.m_CAGR}
        bar = min(cand, key=cand.get)
        pred = 1e4 * cand[bar] / r.turnover_yr
        meas = r.be_4b
        err = np.nan if np.isnan(meas) else pred - meas
        if not np.isnan(err):
            pred_err.append(err)
        P(f"  {r.panel:5s} {r.book:8s} {r.cadence:4s} {r.turnover_yr:6.2f} {sig:6.3f} {bar:>6s} "
          f"{pred:7.1f} {('never' if np.isnan(meas) else f'{meas:7.1f}'):>7s} "
          f"{('  n/a' if np.isnan(err) else f'{err:7.1f}'):>7s}")
    if pred_err:
        P(f"  closed form vs interpolated crossing: mean error {np.mean(pred_err):+.1f} bps, "
          f"MAE {np.mean(np.abs(pred_err)):.1f} bps over {len(pred_err)} cells "
          f"(the gap is the DD bar and the half-sample turnover approximation)")
    P("  => TURNOVER BUDGET, usable form: a book clears 4b at c bps only if its annual turnover "
      "T <= 1e4 * (its smallest 4b margin, in sigma units) / c.")

    P("\nDoes slowing the cadence buy the rung back?  (breakeven bps by cadence)")
    P("  " + be.pivot_table(index=["panel", "book"], columns="cadence", values="be_4b",
                            dropna=False).to_string(float_format=lambda x: f"{x:.1f}"))

    P("\nRule 8 summary (chooser vs do-nothing, pooled over rungs and panels):")
    for tag in ["S1", "S2"]:
        d = wf[(wf.rule == tag) & (wf.pick != "none")]
        if not len(d):
            P(f"  {tag}: no pick at any rung"); continue
        P(f"  {tag}: beats N20/W anchor {int(d.beats_anchor.sum())}/{len(d)}, "
          f"beats RULES v2 {int(d.beats_live.sum())}/{len(d)}, "
          f"beats SPY {int(d.beats_spy.sum())}/{len(d)}, "
          f"mean OOS Sharpe {d.oos_sharpe.mean():.4f} vs anchor {d.anchor_oos.mean():.4f} "
          f"({d.oos_sharpe.mean()-d.anchor_oos.mean():+.4f}), mean regret {d.regret.mean():.4f}")
        P(f"       picks: {d.pick.value_counts().to_dict()}")

    grid.to_csv(f"{OUT}.grid.csv", index=False)
    be.to_csv(f"{OUT}.breakeven.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\nWrote {OUT.name}.grid.csv ({len(grid)} rows), .breakeven.csv ({len(be)}), "
      f".walkforward.csv ({len(wf)}).  Elapsed {time.time()-t0:.0f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
