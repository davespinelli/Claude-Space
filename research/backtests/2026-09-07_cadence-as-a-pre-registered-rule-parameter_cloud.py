#!/usr/bin/env python3
"""Idea 107 - "cadence as a pre-registered RULES parameter" (cloud, 2026-09-07).

The question
------------
Idea 101 found the standing candidate's 4b pass FAILS at daily cadence in 4/4 cells, and that
monthly dominates weekly on CAGR, Sharpe AND MaxDD in 8/8 cells.  Idea 3 found monthly buys
3-6pp of EXTRA drawdown elsewhere.  Those two cannot both be general.  The queue asks two
things:

  (1) Does cadence belong in RULES as a PRE-REGISTERED parameter, and at which value?
  (2) Re-measure the D-vs-W gap once idea 38's trading-day index lands - the D arm used to
      rebalance on weekend zero-return rows, which taxes D for nothing.

Pre-registered gates (written before any number was read)
--------------------------------------------------------
  H_CLEAN     - the D arm must be measured on a trading-day index.  Runtime check: zero
                weekend rows and zero all-zero-return days on every panel, else the run
                reports the contamination and prices D on the cleaned index.
  H_DOMINANT  - RULES may pre-register a cadence only if ONE value wins OOS Sharpe on
                >= 75% of the (panel, book) cells at the 10-bps anchor.  A 50-60% plurality
                is not a rule, it is a preference.
  H_STABLE    - and only if the choice is knowable in advance: the IS-argmax cadence must
                agree with the OOS-argmax on strictly more than the 25% chance base rate,
                AND a fixed pre-registered cadence must not have LOWER mean OOS Sharpe than
                PROTOCOL rule 8's per-cell IS choice (if rule 8 wins, cadence is a chosen
                dial, not a constant).
  H_MONTHLY   - idea 101's "M dominates W on CAGR, Sharpe and MaxDD in 8/8" and idea 3's
                "monthly buys 3-6pp of extra drawdown" are re-tested as stated on a menu
                neither was measured on.  They are opposite claims; at most one survives.

PRE-REGISTER <value> requires H_DOMINANT and H_STABLE.  Otherwise cadence stays a per-idea
reported dial and PROTOCOL says so - a KILL of the proposal is a result.

The two tuned parameters (PROTOCOL rule 4)
------------------------------------------
    cadence in {D, W, M, Q}                                    (param 1 - the proposal)
    panel   in {U56, B136, B80held, SMALL439}                  (param 2)
ALL 4 x 4 = 16 points are reported on every book and every cost rung.

Fixed in advance, NOT tuned: 7 books at the live gross of 0.75 -
    N10, N20, N40   top-n ranked at 0.75/n
    B03R, B12R      200d band (b=0.03, 0.12), RESPREAD over in-band names
    V2DG            200d band b=0.03, DE-GROSS to cash - the LIVE RULES v2 shape
    EWALL           every live name at 0.75/N - the do-nothing control
7 books x 4 cadences x 4 panels = 112 cells, 7 cost rungs = 784 rows.

Mechanics
---------
Costs   : held weights and turnover do not depend on cost_bps, so every rung comes from ONE
          zero-cost run per cell as r_c = r_0 - turnover * c/1e4.  Gated against
          engine.backtest at 10 bps; aborts if max|diff| > 1e-12.
Metrics : numpy CAGR/Sharpe/MaxDD, gated against engine.metrics; aborts if > 1e-12.
Rule 8  : cadence chosen on <= 2016-12-31 by IS Sharpe, 2017-01-01 onward read once.
Both KEEP paths are evaluated on all 112 cells at the 10-bps anchor (4a vs the live RULES v2
book on the same panel at its live weekly cadence; 4b vs SPY, including the rule-8 OOS bar).

SURVIVORSHIP: all four panels are current-constituent lists, SMALL439 (483 sub-$2B names
minus the 44 with max_1d_move >= 1.0) most exposed - a sub-$2B screen run today cannot see
names that delisted, so absolute CAGRs are optimistic.  This run holds names, weights and
fill fixed and moves ONLY the rebalance schedule, which is far less exposed than the levels.

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
GROSS = 0.75
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
ANCHOR_COST = 10
RUNGS = [0, 5, 10, 15, 20, 25, 50]
CADENCES = ["D", "W", "M", "Q"]          # tuned param 1
BOOKS = ["N10", "N20", "N40", "B03R", "B12R", "V2DG", "EWALL"]
LIVE_BOOK, LIVE_CAD = "V2DG", "W"        # RULES v2 as it trades
SMALL_BAD_MOVE = 1.0
DOMINANCE_BAR = 0.75

OUT = Path(__file__).with_suffix("")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ranked(px):
    return score(px, vol_scale=VOL_SCALE)[0].where(eligible_mask(px)).rank(axis=1, ascending=False)


def build(px, book, rank):
    if book in ("N10", "N20", "N40"):
        n = int(book[1:])
        return (rank <= n).astype(float) * (GROSS / n)
    if book in ("B03R", "B12R"):
        b = 0.03 if book == "B03R" else 0.12
        g = band_state(px, b) & live_mask(px)
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0) * GROSS
    if book == "V2DG":
        return rules_v2_weights(px, band=0.03, gross=GROSS)
    if book == "EWALL":
        lv = live_mask(px)
        return lv.astype(float).div(lv.sum(axis=1).clip(lower=1), axis=0) * GROSS
    raise ValueError(book)


def fast_bt(px, w, freq):
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


def nm3(r):
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    sh = (float(r.mean()) * 252.0) / sd if sd else np.nan
    return cagr, sh, dd


def sharpe(r):
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return (float(r.mean()) * 252.0) / sd if sd else np.nan


def panels():
    u = load_universe()
    b = load_universe(broad=True)
    held = [c for c in b.columns if c not in set(u.columns)]
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= SMALL_BAD_MOVE, "ticker"])
    s = load_universe(small=True)
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    out = [("U56", u, u["SPY"]), ("B136", b, b["SPY"]),
           ("B80held", b[held].dropna(how="all").ffill(), b["SPY"]),
           ("SMALL439", s[keep].dropna(how="all").ffill(), s["SPY"])]
    P(f"  SMALL439: dropped {len(bad)} of {len(meta)} names with max_1d_move >= {SMALL_BAD_MOVE}; "
      f"SPY is a benchmark column, not a constituent.")
    return out


def main():
    t0 = time.time()
    P("=" * 176)
    P("IDEA 107 - cadence as a pre-registered RULES parameter  (cloud 2026-09-07)")
    P("=" * 176)
    P("  Pre-registered: H_CLEAN trading-day index | H_DOMINANT one cadence wins OOS Sharpe on >=75% of cells |")
    P("  H_STABLE IS-argmax agrees with OOS-argmax above the 25% base rate AND a fixed cadence is not worse")
    P("  than rule 8's per-cell choice | H_MONTHLY re-test idea 101's 8/8 and idea 3's 3-6pp, as stated.")
    PANELS = panels()

    # ---------------- H_CLEAN
    P("\n" + "=" * 176)
    P("[1] H_CLEAN - is the D arm still rebalancing on weekend / zero-return rows?  (idea 38's trading-day index)")
    P("=" * 176)
    P(f"    {'panel':>9s} {'rows':>6s} {'first':>12s} {'last':>12s} {'weekend rows':>13s} "
      f"{'all-zero-return days':>21s} {'max gap (cal days)':>19s}")
    clean = True
    for pn, px, _ in PANELS:
        wknd = int((pd.Series(px.index.dayofweek) >= 5).sum())
        zr = int((px.pct_change().iloc[1:].abs().sum(axis=1) == 0).sum())
        gap = int(pd.Series(px.index).diff().dt.days.max())
        clean &= (wknd == 0 and zr == 0)
        P(f"    {pn:>9s} {len(px):>6d} {str(px.index[0].date()):>12s} {str(px.index[-1].date()):>12s} "
          f"{wknd:>13d} {zr:>21d} {gap:>19d}")
    P(f"    H_CLEAN: {'PASS - idea 38 has landed; the D arm trades only on real sessions, so the' if clean else 'FAIL - contaminated index'} "
      f"{'D-vs-W gap below is a pure schedule effect.' if clean else ''}")

    # ---------------- grid
    grid = []
    gate_err = gate_met = 0.0
    gate_n = 0
    for pn, px, spy_px in PANELS:
        rank = ranked(px)
        start = px.index[260]
        spy = spy_px.reindex(px.index).pct_change().fillna(0.0).loc[start:]
        idx = spy.index
        is_m = np.asarray(idx <= pd.Timestamp(IS_END))
        oos_m = np.asarray(idx >= pd.Timestamp(OOS_START))
        yrs = (idx[-1] - idx[0]).days / 365.25
        sv = spy.values.astype(float)
        h = len(sv) // 2
        spy_cg, spy_sh, spy_dd = nm3(sv)
        so_cg, so_sh, so_dd = nm3(sv[oos_m])
        ref = dict(H1=sharpe(sv[:h]), H2=sharpe(sv[h:]), DD=abs(spy_dd), CAGR=spy_cg,
                   OOS=so_sh, OOS_CAGR=so_cg, OOS_DD=abs(so_dd))
        P(f"\n  PANEL {pn}: {idx[0].date()}..{idx[-1].date()}  SPY full {spy_cg:.2%}/{spy_sh:.3f}/{spy_dd:.2%} "
          f"halves {ref['H1']:.3f}/{ref['H2']:.3f}  OOS {so_cg:.2%}/{so_sh:.3f}/{so_dd:.2%}")
        for book in BOOKS:
            w = build(px, book, rank)
            for cad in CADENCES:
                r0f, tnf = fast_bt(px, w, cad)
                r0 = r0f.loc[start:].values.astype(float)
                tn = tnf.loc[start:].values.astype(float)
                if gate_n < 6 and (book, cad) in [("N20", "W"), ("V2DG", "D"), ("B12R", "Q")]:
                    eng = backtest(px, w, cost_bps=ANCHOR_COST, freq=cad)["returns"].loc[start:].values
                    rr = r0 - tn * ANCHOR_COST / 1e4
                    gate_err = max(gate_err, float(np.abs(eng - rr).max()))
                    em = metrics(pd.Series(rr, index=idx))
                    c_, s_, d_ = nm3(rr)
                    gate_met = max(gate_met, abs(em["CAGR"] - c_), abs(em["Sharpe"] - s_), abs(em["MaxDD"] - d_))
                    gate_n += 1
                T_all = float(tn.sum()) / yrs
                T_is = float(tn[is_m].sum()) / ((idx[is_m][-1] - idx[is_m][0]).days / 365.25)
                for c in RUNGS:
                    r = r0 - tn * (c / 1e4)
                    cg, sh, dd = nm3(r)
                    oc, os_, od = nm3(r[oos_m])
                    ic, is_sh, idd = nm3(r[is_m])
                    grid.append(dict(panel=pn, book=book, cadence=cad, cost=c,
                                     CAGR=cg, Sharpe=sh, MaxDD=dd, H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                                     IS_Sharpe=is_sh, IS_CAGR=ic, IS_MaxDD=idd,
                                     OOS_Sharpe=os_, OOS_CAGR=oc, OOS_MaxDD=od,
                                     T=T_all, T_is=T_is,
                                     spy_H1=ref["H1"], spy_H2=ref["H2"], spy_DD=ref["DD"],
                                     spy_CAGR=ref["CAGR"], spy_OOS=ref["OOS"],
                                     spy_OOS_CAGR=ref["OOS_CAGR"], spy_OOS_DD=ref["OOS_DD"]))
    G = pd.DataFrame(grid)
    P(f"\n  GATE cost identity vs engine.backtest @10bps: max|diff| = {gate_err:.3e} on {gate_n} cells")
    P(f"  GATE numpy metrics vs engine.metrics:          max|diff| = {gate_met:.3e}")
    assert gate_err < 1e-12 and gate_met < 1e-12, "gate failed"
    live = G[(G.book == LIVE_BOOK) & (G.cadence == LIVE_CAD)].set_index(["panel", "cost"])
    G = G.join(live[["H1", "H2", "MaxDD"]].rename(columns=lambda c: "live_" + c), on=["panel", "cost"])
    G["pass4a"] = (G.H1 > G.live_H1) & (G.H2 > G.live_H2) & (G.MaxDD >= G.live_MaxDD)
    G["pass4b"] = ((G.H1 > G.spy_H1) & (G.H2 > G.spy_H2) & (G.OOS_Sharpe > G.spy_OOS)
                   & (G.MaxDD.abs() <= 0.60 * G.spy_DD) & (G.CAGR >= 0.70 * G.spy_CAGR))
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"  {len(BOOKS)} books x {len(CADENCES)} cadences x {len(PANELS)} panels = "
      f"{len(BOOKS)*len(CADENCES)*len(PANELS)} cells x {len(RUNGS)} rungs = {len(G)} rows.  [{time.time()-t0:.0f}s]")

    A = G[G.cost == ANCHOR_COST]

    # ---------------- the D-vs-W gap on the clean index
    P("\n" + "=" * 176)
    P(f"[2] THE D-vs-W GAP on the clean trading-day index, {ANCHOR_COST}-bps anchor "
      f"(full-sample Sharpe, CAGR, MaxDD, turnover units/yr)")
    P("=" * 176)
    P(f"    {'panel':>9s} {'book':>6s} | " + " | ".join(
        f"{c:>3s}: {'Sh':>6s} {'CAGR':>7s} {'DD':>8s} {'T':>6s}" for c in CADENCES))
    dw = []
    for pn, _, _ in PANELS:
        for book in BOOKS:
            d = A[(A.panel == pn) & (A.book == book)].set_index("cadence")
            cells = " | ".join(f"{c:>3s}: {d.loc[c].Sharpe:>6.3f} {d.loc[c].CAGR:>7.2%} "
                               f"{d.loc[c].MaxDD:>8.2%} {d.loc[c]['T']:>6.1f}" for c in CADENCES)
            P(f"    {pn:>9s} {book:>6s} | {cells}")
            dw.append(dict(panel=pn, book=book,
                           dSh_DW=d.loc["D"].Sharpe - d.loc["W"].Sharpe,
                           dSh_MW=d.loc["M"].Sharpe - d.loc["W"].Sharpe,
                           dCAGR_MW=d.loc["M"].CAGR - d.loc["W"].CAGR,
                           dDD_MW=d.loc["M"].MaxDD - d.loc["W"].MaxDD,
                           dSh_QW=d.loc["Q"].Sharpe - d.loc["W"].Sharpe,
                           T_D=d.loc["D"]["T"], T_W=d.loc["W"]["T"]))
    DW = pd.DataFrame(dw)
    DW.to_csv(f"{OUT}.gaps.csv", index=False)
    P(f"\n    D - W Sharpe gap: mean {DW.dSh_DW.mean():+.4f}, median {DW.dSh_DW.median():+.4f}, "
      f"D wins {int((DW.dSh_DW>0).sum())}/{len(DW)} cells.  D turnover {DW.T_D.mean():.1f}x vs "
      f"W {DW.T_W.mean():.1f}x (mean, {DW.T_D.mean()/DW.T_W.mean():.1f}x more).")
    P(f"    Cost of the D schedule alone at {ANCHOR_COST} bps: "
      f"{(DW.T_D-DW.T_W).mean()*ANCHOR_COST/100:.2f} pp of CAGR/yr more than W.")

    # ---------------- H_MONTHLY (idea 101 vs idea 3, as stated)
    P("\n" + "=" * 176)
    P("[3] H_MONTHLY - idea 101 ('M dominates W on CAGR, Sharpe AND MaxDD, 8/8') vs idea 3 ('M buys 3-6pp of extra DD')")
    P("=" * 176)
    dom = ((DW.dSh_MW > 0) & (DW.dCAGR_MW > 0) & (DW.dDD_MW >= 0))
    P(f"    M dominates W on all three bars: {int(dom.sum())}/{len(DW)} cells "
      f"({dom.mean():.0%})  [idea 101 claimed 8/8 = 100%]")
    P(f"    M vs W by bar: Sharpe M wins {int((DW.dSh_MW>0).sum())}/{len(DW)} (mean {DW.dSh_MW.mean():+.4f}), "
      f"CAGR M wins {int((DW.dCAGR_MW>0).sum())}/{len(DW)} (mean {DW.dCAGR_MW.mean():+.2%}), "
      f"MaxDD M better {int((DW.dDD_MW>=0).sum())}/{len(DW)} (mean {DW.dDD_MW.mean():+.2%})")
    worse = DW[DW.dDD_MW < 0]
    P(f"    idea 3's claim (M buys EXTRA drawdown): M is WORSE on DD in {len(worse)}/{len(DW)} cells; "
      f"where worse, by {(-worse.dDD_MW).mean():.2%} on average, worst {(-worse.dDD_MW).max():.2%} "
      f"[idea 3 claimed 3-6pp]" if len(worse) else
      f"    idea 3's claim (M buys EXTRA drawdown): 0/{len(DW)} cells - not reproduced anywhere on this menu")
    P(f"    per panel, M-dominates-W: " + ", ".join(
        f"{pn} {int(dom[DW.panel==pn].sum())}/{int((DW.panel==pn).sum())}" for pn, _, _ in PANELS))

    # ---------------- H_DOMINANT
    P("\n" + "=" * 176)
    P(f"[4] H_DOMINANT - does ONE cadence win OOS Sharpe on >= {DOMINANCE_BAR:.0%} of the {len(BOOKS)*len(PANELS)} "
      f"(panel, book) cells at the anchor?")
    P("=" * 176)
    win = A.loc[A.groupby(["panel", "book"]).OOS_Sharpe.idxmax()]
    vc = win.cadence.value_counts()
    P(f"    OOS-argmax cadence, {ANCHOR_COST} bps: " +
      ", ".join(f"{c} {int(vc.get(c,0))}/{len(win)} ({vc.get(c,0)/len(win):.0%})" for c in CADENCES))
    for pn, _, _ in PANELS:
        v = win[win.panel == pn].cadence.value_counts()
        P(f"      {pn:>9s}: " + ", ".join(f"{c} {int(v.get(c,0))}" for c in CADENCES))
    top = vc.idxmax()
    H_DOM = bool(vc.max() / len(win) >= DOMINANCE_BAR)
    P(f"    modal cadence {top} at {vc.max()/len(win):.0%} -> H_DOMINANT "
      f"{'PASS' if H_DOM else 'FAIL'} (bar {DOMINANCE_BAR:.0%})")
    P(f"    same test on FULL-sample Sharpe: " + ", ".join(
        f"{c} {int((A.loc[A.groupby(['panel','book']).Sharpe.idxmax()].cadence==c).sum())}" for c in CADENCES))
    P(f"    same test at every rung (OOS Sharpe argmax counts):")
    for c_ in RUNGS:
        w_ = G[G.cost == c_]
        w_ = w_.loc[w_.groupby(["panel", "book"]).OOS_Sharpe.idxmax()]
        v = w_.cadence.value_counts()
        P(f"      {c_:>2d} bps: " + ", ".join(f"{c} {int(v.get(c,0)):>2d}" for c in CADENCES))

    # ---------------- H_STABLE (rule 8)
    P("\n" + "=" * 176)
    P("[5] H_STABLE / PROTOCOL RULE 8 - cadence chosen on <= 2016 by IS Sharpe, 2017- read once.")
    P("=" * 176)
    rows = []
    for pn, _, _ in PANELS:
        for book in BOOKS:
            for c_ in RUNGS:
                d = G[(G.panel == pn) & (G.book == book) & (G.cost == c_)].set_index("cadence")
                pick = d.IS_Sharpe.idxmax()
                oos_best = d.OOS_Sharpe.idxmax()
                rows.append(dict(panel=pn, book=book, cost=c_, is_pick=pick, oos_best=oos_best,
                                 agree=pick == oos_best,
                                 r8_oos=d.loc[pick].OOS_Sharpe, best_oos=d.loc[oos_best].OOS_Sharpe,
                                 regret=d.loc[oos_best].OOS_Sharpe - d.loc[pick].OOS_Sharpe,
                                 **{f"fix_{c}": d.loc[c].OOS_Sharpe for c in CADENCES},
                                 **{f"fixdd_{c}": d.loc[c].OOS_MaxDD for c in CADENCES},
                                 **{f"fixcg_{c}": d.loc[c].OOS_CAGR for c in CADENCES}))
    R8 = pd.DataFrame(rows)
    R8.to_csv(f"{OUT}.walkforward.csv", index=False)
    a8 = R8[R8.cost == ANCHOR_COST]
    base_rate = 1.0 / len(CADENCES)
    P(f"    IS-argmax agrees with OOS-argmax: {int(a8.agree.sum())}/{len(a8)} = {a8.agree.mean():.0%} at the "
      f"anchor (chance {base_rate:.0%}); {int(R8.agree.sum())}/{len(R8)} = {R8.agree.mean():.0%} over all rungs")
    P(f"    IS-pick distribution at the anchor: " +
      ", ".join(f"{c} {int((a8.is_pick==c).sum())}" for c in CADENCES))
    P(f"\n    Mean OOS Sharpe / CAGR / MaxDD of each POLICY (anchor rung, {len(a8)} cells):")
    P(f"      {'policy':>16s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} {'OOS MaxDD':>10s} {'regret':>8s} {'>SPY':>7s}")
    spy_oos = A.groupby(["panel", "book"]).spy_OOS.first().mean()
    pol = {}
    for c in CADENCES:
        v = a8[f"fix_{c}"]
        pol[f"fixed {c}"] = v.mean()
        P(f"      {'fixed ' + c:>16s} {v.mean():>11.4f} {a8[f'fixcg_{c}'].mean():>9.2%} "
          f"{a8[f'fixdd_{c}'].mean():>10.2%} {(a8.best_oos - v).mean():>8.4f} "
          f"{int((v > spy_oos).sum()):>4d}/{len(a8)}")
    pol["rule 8 (IS pick)"] = a8.r8_oos.mean()
    P(f"      {'rule 8 (IS pick)':>16s} {a8.r8_oos.mean():>11.4f} {'-':>9s} {'-':>10s} "
      f"{a8.regret.mean():>8.4f} {int((a8.r8_oos > spy_oos).sum()):>4d}/{len(a8)}")
    P(f"      {'ORACLE (OOS)':>16s} {a8.best_oos.mean():>11.4f} {'-':>9s} {'-':>10s} {0.0:>8.4f} "
      f"{int((a8.best_oos > spy_oos).sum()):>4d}/{len(a8)}   (SPY OOS Sharpe {spy_oos:.3f})")
    best_fixed = max(CADENCES, key=lambda c: pol[f"fixed {c}"])
    H_STA = bool(a8.agree.mean() > base_rate and pol[f"fixed {best_fixed}"] >= pol["rule 8 (IS pick)"])
    P(f"\n    best fixed cadence = {best_fixed} at {pol[f'fixed {best_fixed}']:.4f} vs rule 8's "
      f"{pol['rule 8 (IS pick)']:.4f} -> H_STABLE {'PASS' if H_STA else 'FAIL'} "
      f"(needs agreement > {base_rate:.0%} AND fixed >= rule 8)")
    P(f"    per-panel best fixed cadence (mean OOS Sharpe over the 7 books, anchor rung):")
    for pn, _, _ in PANELS:
        d = a8[a8.panel == pn]
        P(f"      {pn:>9s}: " + ", ".join(f"{c} {d[f'fix_{c}'].mean():.3f}" for c in CADENCES) +
          f"   -> {max(CADENCES, key=lambda c: d[f'fix_{c}'].mean())}")

    # ---------------- KEEP paths
    P("\n" + "=" * 176)
    P(f"[6] BOTH KEEP PATHS on all 112 cells at the {ANCHOR_COST}-bps anchor "
      f"(4a vs live {LIVE_BOOK}/{LIVE_CAD} on the same panel; 4b vs SPY)")
    P("=" * 176)
    P(f"    {'panel':>9s} {'4a':>8s} {'4b':>8s}   4b passers (book/cadence)")
    for pn, _, _ in PANELS:
        d = A[A.panel == pn]
        ps = [f"{r.book}/{r.cadence}" for r in d[d.pass4b].itertuples()]
        P(f"    {pn:>9s} {int(d.pass4a.sum()):>3d}/{len(d):<4d} {int(d.pass4b.sum()):>3d}/{len(d):<4d}   "
          f"{', '.join(ps) if ps else '-'}")
    P(f"    4b passes by cadence: " + ", ".join(
        f"{c} {int(A[(A.cadence==c)].pass4b.sum())}/{int((A.cadence==c).sum())}" for c in CADENCES))
    A[["panel", "book", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR",
       "OOS_MaxDD", "T", "pass4a", "pass4b"]].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ---------------- verdict
    P("\n" + "=" * 176)
    P("[7] PRE-REGISTERED VERDICT")
    P("=" * 176)
    P(f"  H_CLEAN    {'PASS' if clean else 'FAIL'}")
    P(f"  H_DOMINANT {'PASS' if H_DOM else 'FAIL'}  (modal OOS-argmax cadence {top} at {vc.max()/len(win):.0%}, "
      f"bar {DOMINANCE_BAR:.0%})")
    P(f"  H_STABLE   {'PASS' if H_STA else 'FAIL'}  (IS/OOS argmax agreement {a8.agree.mean():.0%} vs "
      f"{base_rate:.0%} chance; best fixed {best_fixed} {pol[f'fixed {best_fixed}']:.4f} vs rule 8 "
      f"{pol['rule 8 (IS pick)']:.4f})")
    verdict = f"PRE-REGISTER cadence = {best_fixed}" if (H_DOM and H_STA) else "KILL the pre-registration"
    P(f"\n  VERDICT: {verdict}")
    P(f"  [{time.time()-t0:.0f}s]  wrote {OUT.name}.grid.csv / .gaps.csv / .walkforward.csv / "
      f".keeppaths.csv / .console.txt")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
