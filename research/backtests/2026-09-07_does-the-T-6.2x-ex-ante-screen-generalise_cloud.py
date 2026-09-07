#!/usr/bin/env python3
"""Idea 377 - "does the T <= 6.2x EX-ANTE SCREEN generalise beyond idea 352's menu?" (cloud, 2026-09-07).

The question
------------
Idea 356 (script `2026-09-07_price-c-star-as-a-required-LEADERBOARD-column_C.py`) killed the
c* mandate but reported a by-product: used as a PROTOCOL rule-8 SCREEN, a turnover budget
("S5 = best IS Sharpe among cells with turnover <= 6.2x/yr") lifted the record's default
best-IS-Sharpe chooser from 1.1301 to 1.1992 mean OOS Sharpe, cut mean regret 0.1030 ->
0.0339 and beat the live book 7/14 rungs vs 1/14.

That was measured on idea 352's 42-cell menu (7 named books x 3 cadences x 2 panels) - the
same menu the 6.2x number was read off in the first place.  A screen fitted near its own
menu is worth nothing until it is run on a menu it has never seen.

Pre-registered gates (written before any number was read)
--------------------------------------------------------
  G1 GENERALISES - on a NEW menu (the record's band/gross/n dials, factorial) and on a
                   HELD-OUT panel, S5 at the inherited budget T = 6.2x must have mean OOS
                   Sharpe >= S1's AND mean regret <= S1's, at the 10-bps anchor, pooled
                   over panels.
  G2 BUDGET STABLE - the lift must not be a knife edge: sweeping T, the set of budgets that
                   beat S1 must be a contiguous run containing 6.2x and covering >= 3 of the
                   11 swept values.  If the argmax sits at an unrelated T and 6.2x itself
                   loses, the budget is menu-specific.
  G3 EX-ANTE     - the lift must survive an honest ex-ante turnover.  Idea 356 screened on
                   FULL-SAMPLE turnover (`turnover_yr` over the whole index), which a 2016
                   reporter could not have known.  Primary here is IS-ONLY turnover; the
                   full-sample version is reported beside it as the parent's comparand.

ADOPT (protocol-grade ex-ante screen) requires all three.  Any failure names the clause and
the proposal is PARKed or KILLED.  A KILL is a result: it says the budget was a property of
idea 352's menu, not of portfolios.

The two tuned parameters (PROTOCOL rule 4)
------------------------------------------
    budget T in {2, 3, 4, 5, 6.2, 8, 10, 12, 15, 20, inf} turnover units/yr   (param 1)
    panel   in {U56, B136, B80held, SMALL439}                                 (param 2)
ALL 11 x 4 = 44 (T, panel) points are reported, at all 7 cost rungs.

The menu (fixed in advance, NOT tuned - and NOT idea 352's)
-----------------------------------------------------------
7 books x 3 gross x 3 cadences = 63 cells per panel, 252 cells total:
    N10, N20, N40   top-n ranked at gross/n (the record's n dial)
    B03R, B12R      200d band, RESPREAD over in-band names (the record's band-width dial)
    V2DG            200d band b=0.03, DE-GROSS to cash - the LIVE RULES v2 shape
    EWALL           every live name at gross/N - the do-nothing control
    gross g in {0.50, 0.75, 1.00}     (the record's gross dial)
    cadence in {W, M, Q}
Idea 352's menu was 7 NAMED books (N20, F085, BAND12, BRCASH, RULESv2, NF20, EWALL) x 3
cadences at a single gross of 0.75.  Only N20/0.75, V2DG/0.75 and EWALL/0.75 are shared;
the gross dial and the n/band dials are new to the screen.

Panels
------
    U56       research/universe.json           (the parent's, for comparability)
    B136      research/universe_broad.json     (the parent's second panel)
    B80held   the 80 B136 names NOT in U56     - THE HELD-OUT PANEL (never carried a menu)
    SMALL439  data/prices_small.csv, 483 sub-$2B names minus the 44 with max_1d_move >= 1.0
SURVIVORSHIP: all four are current-constituent lists, so absolute CAGRs are optimistic -
SMALL439 worst of all (a sub-$2B screen run today cannot see names that delisted).  This
run compares CHOOSERS on the same cells, which is far less exposed than the levels are.

Mechanics
---------
Costs   : held weights and turnover do not depend on cost_bps, so every rung comes from ONE
          zero-cost run per cell as r_c = r_0 - turnover * c/1e4.  Gated against
          engine.backtest at 10 bps; aborts if max|diff| > 1e-12.
Metrics : numpy CAGR/Sharpe/MaxDD, gated against engine.metrics; aborts if > 1e-12.
Rule 8  : choosers fitted on <= 2016-12-31 only, 2017-01-01 onward read once.
          S1  best IS Sharpe (the record's default)
          S5_T best IS Sharpe among cells with IS turnover <= T  (THE PROPOSAL)
          S5F_T the same on FULL-SAMPLE turnover (idea 356's version, lookahead)
Both KEEP paths are evaluated on all 252 cells at the 10-bps anchor (4a vs the live RULES v2
book on the same panel; 4b vs SPY, including the rule-8 OOS bar).

Deterministic, standalone.  Reads baseline.py + engine.py and data/; modifies nothing.
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

MAX_VOL = 0.60
VOL_SCALE = False
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
ANCHOR_COST = 10
RUNGS = [0, 5, 10, 15, 20, 25, 50]
BUDGETS = [2.0, 3.0, 4.0, 5.0, 6.2, 8.0, 10.0, 12.0, 15.0, 20.0, np.inf]   # tuned param 1
INHERITED_T = 6.2
GROSSES = [0.50, 0.75, 1.00]
CADENCES = ["W", "M", "Q"]
BOOKS = ["N10", "N20", "N40", "B03R", "B12R", "V2DG", "EWALL"]
LIVE_CELL = ("V2DG", 0.75, "W")      # RULES v2 as it trades
ANCHOR_CELL = ("N20", 0.75, "W")     # the record's do-nothing anchor
SMALL_BAD_MOVE = 1.0

OUT = Path(__file__).with_suffix("")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- books
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ranked(px):
    return score(px, vol_scale=VOL_SCALE)[0].where(eligible_mask(px)).rank(axis=1, ascending=False)


def build(px, book, gross, rank_cache):
    if book in ("N10", "N20", "N40"):
        n = int(book[1:])
        rank = rank_cache
        return (rank <= n).astype(float) * (gross / n)
    if book in ("B03R", "B12R"):
        b = 0.03 if book == "B03R" else 0.12
        g = band_state(px, b) & live_mask(px)
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0) * gross
    if book == "V2DG":
        return rules_v2_weights(px, band=0.03, gross=gross)
    if book == "EWALL":
        live = live_mask(px)
        return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * gross
    raise ValueError(book)


def fast_bt(px, w, freq):
    """engine.backtest at cost_bps=0, in numpy.  Returns (returns, turnover)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


# ---------------------------------------------------------------- metrics
def nm3(r):
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    sh = (float(r.mean()) * 252.0) / sd if sd else np.nan
    return cagr, sh, dd


def spear(a, b):
    """Spearman rho without scipy: Pearson correlation of the (average-tied) ranks."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    return float(a.rank().corr(b.rank()))


def sharpe(r):
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return (float(r.mean()) * 252.0) / sd if sd else np.nan


# ---------------------------------------------------------------- panels
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    held = [c for c in b.columns if c not in set(u.columns)]
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= SMALL_BAD_MOVE, "ticker"])
    s = load_universe(small=True)
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    out = []
    out.append(("U56", u, u["SPY"]))                                  # SPY is a constituent (parent's convention)
    out.append(("B136", b, b["SPY"]))                                 # SPY is a constituent
    out.append(("B80held", b[held].dropna(how="all").ffill(), b["SPY"]))   # SPY not a member
    out.append(("SMALL439", s[keep].dropna(how="all").ffill(), s["SPY"]))  # SPY benchmark only
    P(f"  panels: " + ", ".join(f"{n} {p.shape[1]}x{p.shape[0]} {p.index[0].date()}..{p.index[-1].date()}"
                                for n, p, _ in out))
    P(f"  SMALL439: dropped {len(bad)} of {len(meta)} names with max_1d_move >= {SMALL_BAD_MOVE} "
      f"(split/adjustment artefacts); SPY is a benchmark column, not a constituent.")
    return out


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 170)
    P("IDEA 377 - does the T <= 6.2x ex-ante screen generalise beyond idea 352's menu?  (cloud 2026-09-07)")
    P("=" * 170)
    P("  Pre-registered: G1 lift at T=6.2 on a new menu + held-out panel | G2 contiguous >=3-value winning")
    P("  run containing 6.2 | G3 lift survives IS-ONLY turnover (idea 356 screened on full-sample turnover).")
    PANELS = panels()

    grid = []
    cellstore = {}
    gate_err = 0.0
    gate_met = 0.0
    gate_n = 0
    for pname, px, spy_px in PANELS:
        rank = ranked(px)
        start = px.index[260]
        spy = spy_px.reindex(px.index).pct_change().fillna(0.0).loc[start:]
        idx = spy.index
        is_m = np.asarray(idx <= pd.Timestamp(IS_END))
        oos_m = np.asarray(idx >= pd.Timestamp(OOS_START))
        yrs_all = (idx[-1] - idx[0]).days / 365.25
        yrs_is = (idx[is_m][-1] - idx[is_m][0]).days / 365.25
        sv = spy.values.astype(float)
        h = len(sv) // 2
        spy_ref = dict(H1=sharpe(sv[:h]), H2=sharpe(sv[h:]))
        spy_cg, spy_sh, spy_dd = nm3(sv)
        spy_ref.update(CAGR=spy_cg, DD=abs(spy_dd))
        so_cg, so_sh, so_dd = nm3(sv[oos_m])
        spy_ref.update(OOS=so_sh, OOS_CAGR=so_cg, OOS_DD=abs(so_dd))
        P(f"\n  PANEL {pname}: sample {idx[0].date()}..{idx[-1].date()}  IS {idx[is_m][0].date()}..{idx[is_m][-1].date()} "
          f"({is_m.sum()}d) OOS {idx[oos_m][0].date()}..{idx[oos_m][-1].date()} ({oos_m.sum()}d)")
        P(f"    SPY full {spy_cg:.2%}/{spy_sh:.3f}/{spy_dd:.2%}  halves {spy_ref['H1']:.3f}/{spy_ref['H2']:.3f}  "
          f"OOS {so_cg:.2%}/{so_sh:.3f}/{so_dd:.2%}")
        for book in BOOKS:
            for g in GROSSES:
                w = build(px, book, g, rank)
                for cad in CADENCES:
                    r0f, turnf = fast_bt(px, w, cad)
                    r0 = r0f.loc[start:].values.astype(float)
                    tn = turnf.loc[start:].values.astype(float)
                    # ---- gate 1: cost identity vs engine.backtest (a sample of cells)
                    if gate_n < 8 and (book, g, cad) in [("N20", 0.75, "W"), ("V2DG", 0.75, "M"),
                                                         ("B12R", 0.50, "Q"), ("EWALL", 1.00, "W")]:
                        eng = backtest(px, w, cost_bps=ANCHOR_COST, freq=cad)["returns"].loc[start:].values
                        gate_err = max(gate_err, float(np.abs(eng - (r0 - tn * ANCHOR_COST / 1e4)).max()))
                        em = metrics(pd.Series(r0 - tn * ANCHOR_COST / 1e4, index=idx))
                        c_, s_, d_ = nm3(r0 - tn * ANCHOR_COST / 1e4)
                        gate_met = max(gate_met, abs(em["CAGR"] - c_), abs(em["Sharpe"] - s_), abs(em["MaxDD"] - d_))
                        gate_n += 1
                    cellstore[(pname, book, g, cad)] = (r0, tn)
                    T_full = float(tn.sum()) / yrs_all
                    T_is = float(tn[is_m].sum()) / yrs_is
                    for c in RUNGS:
                        r = r0 - tn * (c / 1e4)
                        cg, sh, dd = nm3(r)
                        oc, os_, od = nm3(r[oos_m])
                        grid.append(dict(panel=pname, book=book, gross=g, cadence=cad, cost=c,
                                         CAGR=cg, Sharpe=sh, MaxDD=dd,
                                         H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                                         IS_Sharpe=sharpe(r[is_m]),
                                         OOS_Sharpe=os_, OOS_CAGR=oc, OOS_MaxDD=od,
                                         T_is=T_is, T_full=T_full,
                                         spy_H1=spy_ref["H1"], spy_H2=spy_ref["H2"],
                                         spy_DD=spy_ref["DD"], spy_CAGR=spy_ref["CAGR"],
                                         spy_OOS=spy_ref["OOS"], spy_OOS_CAGR=spy_ref["OOS_CAGR"],
                                         spy_OOS_DD=spy_ref["OOS_DD"]))
    G = pd.DataFrame(grid)
    P(f"\n  GATE cost identity vs engine.backtest @10bps: max|diff| = {gate_err:.3e} on {gate_n} cells")
    P(f"  GATE numpy metrics vs engine.metrics:          max|diff| = {gate_met:.3e}")
    assert gate_err < 1e-12 and gate_met < 1e-12, "gate failed"
    P(f"  menu: {G[['panel','book','gross','cadence']].drop_duplicates().shape[0]} cells "
      f"({len(BOOKS)} books x {len(GROSSES)} gross x {len(CADENCES)} cadences x {len(PANELS)} panels), "
      f"{len(RUNGS)} cost rungs -> {len(G)} rows.  [{time.time()-t0:.0f}s]")

    # ---------------- KEEP paths on the whole menu at the anchor rung
    live = G[(G.book == LIVE_CELL[0]) & (G.gross == LIVE_CELL[1]) & (G.cadence == LIVE_CELL[2])]
    liv = live.set_index(["panel", "cost"])[["H1", "H2", "MaxDD", "Sharpe"]]
    G = G.join(liv.rename(columns=lambda c: "live_" + c), on=["panel", "cost"])
    G["pass4a"] = (G.H1 > G.live_H1) & (G.H2 > G.live_H2) & (G.MaxDD >= G.live_MaxDD)
    G["pass4b"] = ((G.H1 > G.spy_H1) & (G.H2 > G.spy_H2) & (G.OOS_Sharpe > G.spy_OOS)
                   & (G.MaxDD.abs() <= 0.60 * G.spy_DD) & (G.CAGR >= 0.70 * G.spy_CAGR))
    G.to_csv(f"{OUT}.grid.csv", index=False)
    a = G[G.cost == ANCHOR_COST]
    P("\n" + "=" * 170)
    P(f"[1] BOTH KEEP PATHS on the new menu at the {ANCHOR_COST}-bps anchor (4a vs live RULES v2 on the same panel; 4b vs SPY)")
    P("=" * 170)
    P(f"    {'panel':>9s} {'cells':>6s} {'4a':>7s} {'4b':>7s}   4b passers")
    for pn, _, _ in PANELS:
        d = a[a.panel == pn]
        pas = [f"{r.book}/{r.gross:.2f}/{r.cadence}" for r in d[d.pass4b].itertuples()]
        P(f"    {pn:>9s} {len(d):>6d} {int(d.pass4a.sum()):>3d}/{len(d):<3d} {int(d.pass4b.sum()):>3d}/{len(d):<3d}   "
          f"{', '.join(pas[:8]) + (' ...' if len(pas) > 8 else '') if pas else '-'}")
    a[["panel", "book", "gross", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
       "OOS_CAGR", "OOS_MaxDD", "T_is", "T_full", "pass4a", "pass4b"]].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ---------------- turnover: is it even a stable column on this menu?
    P("\n" + "=" * 170)
    P("[2] IS the turnover column stable IS -> OOS on the new menu?  (idea 356 reported spearman +0.994 on its own)")
    P("=" * 170)
    tw = []
    for pn, px, spy_px in PANELS:
        start = px.index[260]
        idx = spy_px.reindex(px.index).loc[start:].index
        oos_m = np.asarray(idx >= pd.Timestamp(OOS_START))
        is_m = np.asarray(idx <= pd.Timestamp(IS_END))
        yi = (idx[is_m][-1] - idx[is_m][0]).days / 365.25
        yo = (idx[oos_m][-1] - idx[oos_m][0]).days / 365.25
        for book in BOOKS:
            for g in GROSSES:
                for cad in CADENCES:
                    _, tn = cellstore[(pn, book, g, cad)]
                    tw.append(dict(panel=pn, book=book, gross=g, cadence=cad,
                                   T_is=tn[is_m].sum() / yi, T_oos=tn[oos_m].sum() / yo))
    TW = pd.DataFrame(tw)
    TW.to_csv(f"{OUT}.turnover.csv", index=False)
    P(f"    {'panel':>9s} {'spearman(T_is,T_oos)':>21s} {'pearson':>8s} {'medianT_is':>11s} {'min':>7s} {'max':>8s}")
    for pn, _, _ in PANELS:
        d = TW[TW.panel == pn]
        P(f"    {pn:>9s} {spear(d.T_is, d.T_oos):>21.3f} {d.T_is.corr(d.T_oos):>8.3f} "
          f"{d.T_is.median():>11.2f} {d.T_is.min():>7.2f} {d.T_is.max():>8.2f}")
    P(f"    {'POOLED':>9s} {spear(TW.T_is, TW.T_oos):>21.3f} {TW.T_is.corr(TW.T_oos):>8.3f} "
      f"{TW.T_is.median():>11.2f} {TW.T_is.min():>7.2f} {TW.T_is.max():>8.2f}")
    P(f"    cells with T_is <= {INHERITED_T}: {int((TW.T_is <= INHERITED_T).sum())}/{len(TW)} "
      f"(by panel: " + ", ".join(f"{pn} {int((TW[TW.panel==pn].T_is<=INHERITED_T).sum())}/{len(TW[TW.panel==pn])}"
                                 for pn, _, _ in PANELS) + ")")

    # ---------------- rule 8: choosers
    P("\n" + "=" * 170)
    P("[3] PROTOCOL RULE 8 - choosers fitted on <= 2016 only, 2017- read once.  ALL 11 budgets x 4 panels reported.")
    P("=" * 170)
    wf = []
    for pn, _, _ in PANELS:
        for c in RUNGS:
            d = G[(G.panel == pn) & (G.cost == c)].set_index(["book", "gross", "cadence"])
            best = d.OOS_Sharpe.idxmax()
            anc, lv = ANCHOR_CELL, LIVE_CELL
            spy_oos = d.spy_OOS.iloc[0]

            def emit(tag, pk):
                if pk is None:
                    wf.append(dict(panel=pn, cost=c, rule=tag, pick="none")); return
                r = d.loc[pk]
                wf.append(dict(panel=pn, cost=c, rule=tag, pick=f"{pk[0]}/{pk[1]:.2f}/{pk[2]}",
                               is_sharpe=r.IS_Sharpe, oos_sharpe=r.OOS_Sharpe, oos_cagr=r.OOS_CAGR,
                               oos_dd=r.OOS_MaxDD, T_is=r.T_is,
                               anchor_oos=d.loc[anc].OOS_Sharpe, live_oos=d.loc[lv].OOS_Sharpe,
                               spy_oos=spy_oos, best_oos=d.loc[best].OOS_Sharpe,
                               regret=d.loc[best].OOS_Sharpe - r.OOS_Sharpe,
                               beats_anchor=r.OOS_Sharpe > d.loc[anc].OOS_Sharpe,
                               beats_live=r.OOS_Sharpe > d.loc[lv].OOS_Sharpe,
                               beats_spy=r.OOS_Sharpe > spy_oos,
                               pass4a=bool(r.pass4a), pass4b=bool(r.pass4b)))

            emit("S1", d.IS_Sharpe.idxmax())
            for T in BUDGETS:
                e = d[d.T_is <= T]
                emit(f"S5_{T}", e.IS_Sharpe.idxmax() if len(e) else None)
                e2 = d[d.T_full <= T]
                emit(f"S5F_{T}", e2.IS_Sharpe.idxmax() if len(e2) else None)
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    def summ(df, tags):
        P(f"    {'rule':>10s} {'n':>3s} {'meanOOS_Sh':>10s} {'meanCAGR':>9s} {'meanDD':>8s} {'regret':>7s} "
          f"{'>anchor':>8s} {'>live':>7s} {'>SPY':>6s} {'4b':>5s}  modal pick")
        out = {}
        for tag in tags:
            x = df[(df.rule == tag) & (df.pick != "none")]
            if not len(x):
                P(f"    {tag:>10s}  no pick at any rung"); continue
            out[tag] = (x.oos_sharpe.mean(), x.regret.mean())
            P(f"    {tag:>10s} {len(x):>3d} {x.oos_sharpe.mean():>10.4f} {x.oos_cagr.mean():>9.2%} "
              f"{x.oos_dd.mean():>8.2%} {x.regret.mean():>7.4f} {int(x.beats_anchor.sum()):>4d}/{len(x):<3d} "
              f"{int(x.beats_live.sum()):>3d}/{len(x):<3d} {int(x.beats_spy.sum()):>2d}/{len(x):<3d} "
              f"{int(x.pass4b.sum()):>2d}/{len(x):<2d}  {x.pick.value_counts().idxmax()}")
        return out

    tags_is = ["S1"] + [f"S5_{T}" for T in BUDGETS]
    tags_full = [f"S5F_{T}" for T in BUDGETS]
    P(f"\n  (a) ANCHOR RUNG {ANCHOR_COST} bps, pooled over all {len(PANELS)} panels - IS-ONLY turnover (G3-honest):")
    A = WF[WF.cost == ANCHOR_COST]
    sA = summ(A, tags_is)
    P(f"\n  (b) ANCHOR RUNG {ANCHOR_COST} bps - FULL-SAMPLE turnover (idea 356's version, has lookahead):")
    sAF = summ(A, tags_full)
    P("\n  (c) ALL 7 cost rungs pooled - IS-ONLY turnover:")
    sP = summ(WF, tags_is)
    P("\n  (d) ALL 7 cost rungs pooled - FULL-SAMPLE turnover:")
    sPF = summ(WF, tags_full)

    P(f"\n  (e) PER-PANEL at the anchor, IS-only turnover (S1 vs S5 at the inherited T={INHERITED_T}):")
    P(f"    {'panel':>9s} {'S1 pick':>18s} {'S1 OOS':>7s} | {'S5 pick':>18s} {'S5 OOS':>7s} {'S5 T_is':>8s} | "
      f"{'anchor':>7s} {'live':>7s} {'SPY':>7s} {'OOSbest':>8s}")
    for pn, _, _ in PANELS:
        s1 = A[(A.panel == pn) & (A.rule == "S1")].iloc[0]
        s5 = A[(A.panel == pn) & (A.rule == f"S5_{INHERITED_T}")]
        s5 = s5.iloc[0] if len(s5) and s5.iloc[0]["pick"] != "none" else None
        P(f"    {pn:>9s} {s1['pick']:>18s} {s1['oos_sharpe']:>7.3f} | "
          f"{(s5['pick'] if s5 is not None else 'none'):>18s} "
          f"{(f'{s5.oos_sharpe:.3f}' if s5 is not None else '   -   '):>7s} "
          f"{(f'{s5.T_is:.2f}' if s5 is not None else '  -  '):>8s} | "
          f"{s1['anchor_oos']:>7.3f} {s1['live_oos']:>7.3f} {s1['spy_oos']:>7.3f} {s1['best_oos']:>8.3f}")

    # ---------------- the budget sweep, panel by panel (all 44 grid points)
    P(f"\n  (f) THE BUDGET SWEEP - mean OOS Sharpe of S5_T minus S1, by panel and pooled, at the anchor rung.")
    P(f"      (IS-only turnover.  '+' = the screen helped, '-' = it hurt.  n/a = no cell under the budget.)")
    hdr = "      " + f"{'T':>6s} " + " ".join(f"{pn:>11s}" for pn, _, _ in PANELS) + f" {'POOLED':>9s} {'regret':>8s} {'wins':>6s}"
    P(hdr)
    sweep = []
    for T in BUDGETS:
        row = {"T": T}
        cells_ = []
        for pn, _, _ in PANELS:
            s1 = A[(A.panel == pn) & (A.rule == "S1")].iloc[0].oos_sharpe
            x = A[(A.panel == pn) & (A.rule == f"S5_{T}") & (A.pick != "none")]
            row[pn] = (x.iloc[0].oos_sharpe - s1) if len(x) else np.nan
            cells_.append(f"{row[pn]:>+11.4f}" if not np.isnan(row[pn]) else f"{'n/a':>11s}")
        d5 = A[(A.rule == f"S5_{T}") & (A.pick != "none")]
        d1 = A[A.rule == "S1"]
        row["POOLED"] = d5.oos_sharpe.mean() - d1.oos_sharpe.mean() if len(d5) else np.nan
        row["regret"] = d5.regret.mean() if len(d5) else np.nan
        row["n_pan"] = len(d5)
        row["wins"] = int(sum(1 for pn, _, _ in PANELS if not np.isnan(row[pn]) and row[pn] > 0))
        sweep.append(row)
        P(f"      {T:>6.1f} " + " ".join(cells_) +
          f" {row['POOLED']:>+9.4f}" + (f" {row['regret']:>8.4f}" if not np.isnan(row['regret']) else f" {'n/a':>8s}") +
          f" {row['wins']:>4d}/{len(PANELS)}")
    SW = pd.DataFrame(sweep)
    SW.to_csv(f"{OUT}.sweep.csv", index=False)
    s1_regret = A[A.rule == "S1"].regret.mean()
    P(f"      S1 reference: mean OOS Sharpe {A[A.rule=='S1'].oos_sharpe.mean():.4f}, mean regret {s1_regret:.4f}")

    # ---------------- verdicts
    P("\n" + "=" * 170)
    P("[4] PRE-REGISTERED GATES")
    P("=" * 170)
    s1_sh = A[A.rule == "S1"].oos_sharpe.mean()
    key = f"S5_{INHERITED_T}"
    d6 = A[(A.rule == key) & (A.pick != "none")]
    g1_sh = d6.oos_sharpe.mean() if len(d6) else np.nan
    g1_rg = d6.regret.mean() if len(d6) else np.nan
    G1 = bool(len(d6) == len(PANELS) and g1_sh >= s1_sh and g1_rg <= s1_regret)
    binds_anchor = int((A[A.rule == key].pick.values != A[A.rule == "S1"].pick.values).sum())
    binds_all = int((WF[WF.rule == key].pick.values != WF[WF.rule == "S1"].pick.values).sum())
    P(f"  G1 GENERALISES  : S5 at T={INHERITED_T} mean OOS Sharpe {g1_sh:.4f} vs S1 {s1_sh:.4f} "
      f"(delta {g1_sh-s1_sh:+.4f}); regret {g1_rg:.4f} vs {s1_regret:.4f} -> {'PASS' if G1 else 'FAIL'}")
    P(f"                    BINDING: the budget changes S1's pick on {binds_anchor}/{len(PANELS)} panels at the "
      f"anchor and {binds_all}/{len(WF[WF.rule=='S1'])} (panel,rung) points overall.  A gate passed at "
      f"delta == 0 with 0 binds is passed VACUOUSLY: the screen is INERT on this menu, not helpful.")
    if binds_anchor == 0 and abs(g1_sh - s1_sh) < 1e-9:
        P("                    -> G1 is recorded as VACUOUS PASS (no lift, no harm, no effect).")
    winners = [r for r in sweep if not np.isnan(r["POOLED"]) and r["POOLED"] > 0]
    wset = [r["T"] for r in winners]
    # contiguity of the winning run containing 6.2
    order = [r["T"] for r in sweep]
    run = []
    if INHERITED_T in wset:
        i = order.index(INHERITED_T)
        lo = i
        while lo - 1 >= 0 and order[lo - 1] in wset:
            lo -= 1
        hi = i
        while hi + 1 < len(order) and order[hi + 1] in wset:
            hi += 1
        run = order[lo:hi + 1]
    G2 = bool(len(run) >= 3)
    P(f"  G2 BUDGET STABLE: budgets with a positive pooled lift {wset if wset else '(none)'}; "
      f"contiguous run containing {INHERITED_T} = {run if run else '(none)'} (len {len(run)}, need >=3) "
      f"-> {'PASS' if G2 else 'FAIL'}")
    keyF = f"S5F_{INHERITED_T}"
    dF = A[(A.rule == keyF) & (A.pick != "none")]
    G3 = bool(len(d6) and len(dF) and (g1_sh - s1_sh) >= (dF.oos_sharpe.mean() - s1_sh) - 1e-12 and g1_sh >= s1_sh)
    P(f"  G3 EX-ANTE      : IS-only lift {g1_sh-s1_sh:+.4f} vs full-sample (lookahead) lift "
      f"{dF.oos_sharpe.mean()-s1_sh:+.4f} -> {'PASS' if G3 else 'FAIL'}")
    verdict = "ADOPT" if (G1 and G2 and G3) else ("PARK" if (G1 or G2) else "KILL")
    P(f"\n  VERDICT: {verdict}  (G1 {'PASS' if G1 else 'FAIL'} / G2 {'PASS' if G2 else 'FAIL'} / "
      f"G3 {'PASS' if G3 else 'FAIL'})")

    # ---------------- what does the screen actually pick, and is it just a gross dial?
    P("\n  [5] WHAT THE BUDGET SELECTS (does 'low turnover' just mean 'low gross'?)")
    P(f"    {'T':>6s} {'picks (anchor rung, all panels)':>66s}   {'mean gross of eligible set':>27s}")
    for T in BUDGETS:
        x = A[(A.rule == f"S5_{T}") & (A.pick != "none")]
        elig_g = TW[TW.T_is <= T].gross.mean() if (TW.T_is <= T).any() else np.nan
        P(f"    {T:>6.1f} {', '.join(x.pick.tolist()) if len(x) else 'none':>66s}   {elig_g:>27.3f}")
    P(f"    corr(T_is, gross) pooled = {TW.T_is.corr(TW.gross):.3f}; "
      f"corr(T_is, cadence rank W<M<Q) = "
      f"{TW.T_is.corr(TW.cadence.map({'W':0,'M':1,'Q':2}).astype(float)):.3f}; "
      f"corr(T_is, n-book rank EWALL<B03R<B12R<V2DG<N40<N20<N10) = "
      f"{TW.T_is.corr(TW.book.map({'EWALL':0,'B03R':1,'B12R':2,'V2DG':3,'N40':4,'N20':5,'N10':6}).astype(float)):.3f}")

    # ---------------- the full 11 x 4 grid, pooled over all 7 cost rungs (every grid point)
    P("\n  [6] THE FULL 11 BUDGETS x 4 PANELS GRID, pooled over all 7 cost rungs (IS-only turnover).")
    P("      Each cell: mean OOS Sharpe of S5_T minus S1 on that panel | eligible cells / 63 | binds?")
    P(f"      {'T':>6s} {'#cells<=T':>9s} " + " ".join(f"{pn:>19s}" for pn, _, _ in PANELS) + f" {'POOLED':>9s}")
    full_rows = []
    for T in BUDGETS:
        cells_ = []
        for pn, _, _ in PANELS:
            s1 = WF[(WF.panel == pn) & (WF.rule == "S1")].oos_sharpe.mean()
            x = WF[(WF.panel == pn) & (WF.rule == f"S5_{T}") & (WF.pick != "none")]
            ne = int((TW[TW.panel == pn].T_is <= T).sum())
            nb = int((WF[(WF.panel == pn) & (WF.rule == f"S5_{T}")].pick.values !=
                      WF[(WF.panel == pn) & (WF.rule == "S1")].pick.values).sum())
            d_ = (x.oos_sharpe.mean() - s1) if len(x) else np.nan
            full_rows.append(dict(T=T, panel=pn, delta=d_, n_elig=ne, n_binds=nb, n_rungs=len(x)))
            cells_.append(f"{d_:>+8.4f} {ne:>2d}/63 {nb}/7" if not np.isnan(d_) else f"{'n/a':>19s}")
        pooled = (WF[(WF.rule == f"S5_{T}") & (WF.pick != "none")].oos_sharpe.mean()
                  - WF[WF.rule == "S1"].oos_sharpe.mean())
        P(f"      {T:>6.1f} {int((TW.T_is <= T).sum()):>9d} " + " ".join(cells_) + f" {pooled:>+9.4f}")
    pd.DataFrame(full_rows).to_csv(f"{OUT}.fullgrid.csv", index=False)
    P("      ('binds' = rungs out of 7 where the budget changed S1's pick on that panel.)")

    P(f"\n  [{time.time()-t0:.0f}s]  wrote {OUT.name}.grid.csv / .keeppaths.csv / .turnover.csv / "
      f".walkforward.csv / .sweep.csv / .console.txt")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
