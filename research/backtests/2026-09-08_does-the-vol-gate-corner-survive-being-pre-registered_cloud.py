#!/usr/bin/env python3
"""Idea 232 — does-the-vol-gate-corner-survive-being-pre-registered   (cloud lane, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 228's rule-8 premium is ENTIRELY the vol-cap dial choosing max_vol = off (+0.1049 mean
    OOS Sharpe; +0.213..+0.376 on the small panel), i.e. the in-sample chooser rediscovering
    ideas 38/49.  Excluding that one dial the chooser is -0.0113 over 63 cells and wins 50.8%.
    So test the corner DIRECTLY as a pre-registered arm rather than a selected one: no vol gate
    vs max_vol = 0.60, on all three panels at all 7 cost rungs, with the 200d gate held fixed,
    and report both KEEP paths.  If the corner is real it should not need a selector.

WHAT THIS RUN DOES
    Idea 228's book imported verbatim (research/backtests/2026-09-06_does-any-dial-argmax-move-
    with-cost_C.py):  eligible = (px > 200d MA, band g = 0 held fixed) AND (vol20 < max_vol);
    rank the eligible names by the scan.py composite with NO vol tilt; hold the top n; weekly
    (k = 1), t+1 execution, 260-bar warm-up skip.  Idea 228's defaults are n = 20, g = 0,
    max_vol = 0.60, k = 1, and gross convention "dg" (w = 1/n per name, so the book de-grosses
    into cash whenever fewer than n names are eligible).

    THE PRE-REGISTERED PAIR, the whole question:
        VOLCAP-0.60   idea 228's default and RULES v1's own clause
        VOLCAP-OFF    no vol gate at all (max_vol = +inf)
    The full cap ladder {0.30, 0.45, 0.60, 0.80, 1.00, off} is run and reported beside it so the
    pair can be read in context; no point on the ladder is ever selected.

    THE EXPOSURE CONFOUND, and its control.  Removing the vol cap ENLARGES the eligible set, so
    under idea 228's "dg" convention the OFF arm is mechanically MORE INVESTED than the 0.60 arm
    (idea 157's cash channel).  A Sharpe difference between the two arms is therefore not by
    itself a selection result.  Every cell is run under BOTH gross conventions:
        dg   w = 1/n per name          idea 228's convention; exposure floats with breadth
        rw   w = 1/count_held          gross rebuilt to 1.00 whenever anything is held, so the
                                       two caps are matched on exposure and only SELECTION
                                       differs
    Mean invested is reported for every cell.  If the corner is a selection fact it survives
    under rw; if it only exists under dg it is an exposure fact and idea 228's dial was buying
    beta, not information.

TUNED PARAMETERS (exactly two; every grid point reported)
    P1  max_vol in {0.30, 0.45, 0.60, 0.80, 1.00, off}  — the dial under test.
    P2  cost rung in {0, 5, 10, 15, 20, 25, 30} bps.  10 bps is the protocol rung and the only
        rung a KEEP verdict is read at.
    Panel, gross convention and the held count n in {10, 20, 40} are PRE-REGISTERED REPORTING
    AXES, printed at every point and never chosen on; n = 20 is idea 228's default and carries
    the headline.  The 200d band g = 0 and the weekly cadence k = 1 are held fixed, as the
    queue specifies.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    R1  Under dg the OFF arm beats the 0.60 arm on most panel x n x rung cells, reproducing
        idea 228's dial premium as a pre-registered arm.
    R2  Under rw the gap shrinks by more than half, because most of it is the cash channel.
    R3  On SMALL439 the gap is the largest under dg (idea 228 measured +0.213..+0.376 there),
        and the largest share of it disappears under rw, because the vol cap bites hardest on
        the panel with the most volatile names.
    R4  The pre-registered OFF arm produces no 4a KEEP on any panel (the live RULES v2 book's
        -12% MaxDD is out of reach for a fully invested equity book).
    R5  SMALL439 gives 0 4b passes — idea 136 again.

CONFOUNDS / CAVEATS declared up front
    * The cap ladder is not a random treatment: vol20 correlates with the composite's own
      ranking, so removing the cap changes WHICH names rank as well as HOW MANY are eligible.
      No claim of orthogonality is made; the dg/rw pair separates exposure from selection, not
      selection from ranking.
    * Sharpe differences on overlapping samples; no significance is claimed from the ladder's
      shape.  The rule-8 read is a single untouched OOS window, not a distribution.
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md) with every ticker
      whose max_1d_move >= 1.0 in data/small_meta.csv dropped first.  SURVIVORSHIP BIAS — a
      shape check, never a tradable return.
    * The fast backtester is validated against products/backtester/engine.backtest on 6 books
      to < 1e-12 before any grid number is read.

Deterministic (no randomness), standalone, no network.
Writes .console.txt .grid.csv .pair.csv .walkforward.csv .keep.csv .result.md
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, metrics, rebalance_mask                           # noqa: E402

STEM = "2026-09-08_does-the-vol-gate-corner-survive-being-pre-registered_cloud"
OUT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"

FREQ = "W"
CAPS = [0.30, 0.45, 0.60, 0.80, 1.00, np.inf]      # P1 (inf = OFF)
COSTS = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]   # P2
PROTO = 10.0
NS = [10, 20, 40]                                  # reporting axis, n=20 = idea 228's default
CONV = ["dg", "rw"]                                # reporting axis

pd.set_option("display.width", 250)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def capname(c):
    return "OFF" if not np.isfinite(c) else f"{c:.2f}"


# --------------------------------------------------------------------------- fast backtester
def fast_backtest(px, w, freq=FREQ):
    """Exact vectorised replica of engine.backtest(cost_bps=0); also returns mean invested."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    starts = np.flatnonzero(mask)
    ends = np.append(starts[1:], len(idx))
    port = np.zeros(len(idx))
    tno = np.zeros(len(idx))
    inv = np.zeros(len(idx))
    carry = np.zeros(px.shape[1])
    for s, e in zip(starts, ends):
        w0 = wt[s]
        tno[s] = np.abs(w0 - carry).sum()
        c0 = 1.0 - w0.sum()
        g = np.cumprod(1.0 + rets[s:e], axis=0)
        gs = np.vstack([np.ones((1, px.shape[1])), g])
        v = w0[None, :] * gs
        tot = v.sum(axis=1) + c0
        tot = np.where(tot > 0, tot, np.nan)
        held = v / tot[:, None]
        port[s:e] = np.nansum(held[:-1] * rets[s:e], axis=1)
        inv[s:e] = np.nansum(held[:-1], axis=1)
        carry = held[-1]
    return (pd.Series(port, index=idx), pd.Series(tno, index=idx),
            pd.Series(inv, index=idx))


# --------------------------------------------------------------------------- panels & book
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[keep + ["SPY"]]
    return {
        "U56": (px56, set(px56.columns), "universe.json(56)"),
        "B136": (px136, set(px136.columns), "universe_broad.json(136)"),
        "SMALL439": (pxs, set(keep), f"prices_small({len(keep)}, SPY held out)"),
    }


def ingredients(px, tradable):
    """Idea 228's exact ingredients: composite with NO vol tilt, raw 200d gate, vol20."""
    s_ns, above, vol20 = score(px, vol_scale=False)
    comp = s_ns / (0.5 + 0.5 * above.astype(float))          # recover the pure composite
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        above = above.copy()
        above[drop] = False
    return comp, above, vol20


def book_weights(comp, above, vol20, n, max_vol, conv):
    elig = comp.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n)
    if conv == "dg":
        return sel.astype(float) / n
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).fillna(0.0)


def net(r0, tno, c):
    return r0 - tno * c / 1e4


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# --------------------------------------------------------------------------- pre-checks
def validate_fast(PANELS):
    P("\n  pre-check [a]: fast backtester vs products/backtester/engine.backtest (6 books)")
    wr = wt_ = 0.0
    for pk, (px, tradable, _) in PANELS.items():
        start = px.index[260]
        comp, above, vol20 = ingredients(px, tradable)
        for w in (rules_v1_weights(px), book_weights(comp, above, vol20, 20, 0.60, "dg")):
            ref = backtest(px, w, cost_bps=0.0, freq=FREQ)
            r, t, _ = fast_backtest(px, w)
            wr = max(wr, float((ref["returns"].loc[start:] - r.loc[start:]).abs().max()))
            wt_ = max(wt_, float((ref["turnover"].loc[start:] - t.loc[start:]).abs().max()))
    P(f"      max |d returns| = {wr:.3e}   max |d turnover| = {wt_:.3e}   (both < 1e-12)")
    assert wr < 1e-12 and wt_ < 1e-12, "fast backtester does not replicate the engine"


def check_identity(PANELS):
    P("\n  pre-check [b]: cost identity net(c) = gross - turnover * c / 1e4")
    worst = 0.0
    for pk, (px, tradable, _) in PANELS.items():
        start = px.index[260]
        comp, above, vol20 = ingredients(px, tradable)
        for cap in (0.60, np.inf):
            w = book_weights(comp, above, vol20, 20, cap, "dg")
            r0, tn, _ = fast_backtest(px, w)
            direct = backtest(px, w, cost_bps=PROTO, freq=FREQ)["returns"].loc[start:]
            worst = max(worst, float((direct - net(r0.loc[start:], tn.loc[start:],
                                                   PROTO)).abs().max()))
    P(f"      max |direct 10-bps backtest - net(gross, turnover, 10)| = {worst:.3e} (< 1e-12)")


def check_premise(G):
    """[c] idea 228's own published OOS do-nothing row, re-derived from this grid."""
    P("\n  pre-check [c]: idea 228 published OOS Sharpe at 10 bps for the do-nothing book")
    P("      (n=20, g=0, max_vol=0.60, k=1, dg): U56 1.1683 (19.2% CAGR, -24.0% MaxDD),")
    P("      B136 0.8937, SMALL484 0.5116.  The small panel differs (439 vs 484 names) so only")
    P("      U56 and B136 are gates; SMALL439 is reported for the record.")
    for pk, pub in (("U56", 1.1683), ("B136", 0.8937), ("SMALL439", 0.5116)):
        r = G[(G.panel == pk) & (G.n == 20) & (G.cap == 0.60) & (G.conv == "dg")
              & (G.cost == PROTO)]
        if not len(r):
            continue
        r = r.iloc[0]
        P(f"      {pk:9s} published {pub:.4f}   this run {r.OOS_Sharpe:.4f}   "
          f"|d| = {abs(r.OOS_Sharpe - pub):.4f}   (OOS CAGR {r.OOS_CAGR:.2%}, "
          f"MaxDD {r.OOS_MaxDD:.2%})")


# --------------------------------------------------------------------------- grid
def run_grid(PANELS):
    rows, REF = [], {}
    t0 = time.time()
    for pk, (px, tradable, desc) in PANELS.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2r, v2t, _ = fast_backtest(px, rules_v2_weights(px))
        v1r, v1t, _ = fast_backtest(px, rules_v1_weights(px))
        REF[pk] = dict(px=px, start=start, spy=spy, desc=desc,
                       v2=(v2r.loc[start:], v2t.loc[start:]),
                       v1=(v1r.loc[start:], v1t.loc[start:]))
        sm, so = metrics(spy), metrics(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}")
        P(f"      SPY {sm['CAGR']:.2%}/{sm['Sharpe']:.3f}/{sm['MaxDD']:.2%} | "
          f"OOS {so['CAGR']:.2%}/{so['Sharpe']:.3f}/{so['MaxDD']:.2%}")
        for c in (PROTO, 25.0):
            a = metrics(net(*REF[pk]["v2"], c))
            b = metrics(net(*REF[pk]["v1"], c))
            P(f"      RULES v2 @{c:.0f}bps {a['CAGR']:.2%}/{a['Sharpe']:.3f}/{a['MaxDD']:.2%}"
              f"   RULES v1 @{c:.0f}bps {b['CAGR']:.2%}/{b['Sharpe']:.3f}/{b['MaxDD']:.2%}")
        comp, above, vol20 = ingredients(px, tradable)
        for cap in CAPS:
            e_t = (above & (vol20 < cap)).sum(axis=1).loc[start:]
            P(f"      cap {capname(cap):>4s}: eligible count mean {e_t.mean():6.2f}  "
              f"range {int(e_t.min())}-{int(e_t.max())}  "
              f"weeks with <20 eligible: {float((e_t < 20).mean()):.1%}")
            for n in NS:
                for conv in CONV:
                    w = book_weights(comp, above, vol20, n, cap, conv)
                    r0, tn, iv = fast_backtest(px, w)
                    r0, tn, iv = r0.loc[start:], tn.loc[start:], iv.loc[start:]
                    for c in COSTS:
                        r = net(r0, tn, c)
                        s = stats(r)
                        o = metrics(r.loc[OOS_START:])
                        rows.append(dict(
                            panel=pk, cap=cap, capname=capname(cap), n=n, conv=conv, cost=c,
                            invested=float(iv.mean()), turnover=float(tn.mean() * 52),
                            elig_mean=float(e_t.mean()),
                            CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                            H1=s["H1"], H2=s["H2"],
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                            OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
        P(f"      {len(CAPS)*len(NS)*len(CONV)} books done ({time.time()-t0:.0f}s cum.)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\n  grid: {len(G)} rows -> {STEM}.grid.csv")
    return G, REF


# --------------------------------------------------------------------------- part 1
def the_pair(G):
    P("\n" + "=" * 118)
    P("PART 1 — THE PRE-REGISTERED PAIR.  gap = Sharpe(max_vol OFF) - Sharpe(max_vol 0.60) at")
    P("         the same panel, n, gross convention and rung.  Idea 228's SELECTED dial premium")
    P("         was +0.1049 mean OOS Sharpe overall and +0.213..+0.376 on the small panel.")
    P("=" * 118)
    off = G[~np.isfinite(G.cap)].set_index(["panel", "n", "conv", "cost"])
    six = G[G.cap == 0.60].set_index(["panel", "n", "conv", "cost"])
    pair = pd.DataFrame({
        "S_off": off.Sharpe, "S_060": six.Sharpe, "gap": off.Sharpe - six.Sharpe,
        "gap_H1": off.H1 - six.H1, "gap_H2": off.H2 - six.H2,
        "gap_OOS": off.OOS_Sharpe - six.OOS_Sharpe,
        "gap_CAGR": off.CAGR - six.CAGR, "gap_MaxDD": off.MaxDD - six.MaxDD,
        "inv_off": off.invested, "inv_060": six.invested,
        "tno_off": off.turnover, "tno_060": six.turnover,
    }).reset_index()
    pair.to_csv(OUT / f"{STEM}.pair.csv", index=False)
    for conv in CONV:
        lab = ("dg = w 1/n, exposure floats (idea 228's convention)" if conv == "dg"
               else "rw = gross rebuilt to 1.00, exposure MATCHED")
        P(f"\n  [{conv}]  {lab}")
        P(f"      {'panel':9s} {'n':>3s} " + " ".join(f"{int(c):>7d}bp" for c in COSTS)
          + f"   {'gapH1':>7s} {'gapH2':>7s} {'gapOOS':>7s}  {'inv OFF':>8s} {'inv 0.60':>8s}")
        for pk in G.panel.unique():
            for n in NS:
                r = pair[(pair.panel == pk) & (pair.n == n)
                         & (pair.conv == conv)].set_index("cost").reindex(COSTS)
                p10 = r.loc[PROTO]
                P(f"      {pk:9s} {n:3d} " + " ".join(f"{v:+9.4f}" for v in r.gap.values)
                  + f"   {p10.gap_H1:+7.4f} {p10.gap_H2:+7.4f} {p10.gap_OOS:+7.4f}"
                  + f"  {p10.inv_off:8.3f} {p10.inv_060:8.3f}")
    P(f"\n  SUMMARY OF THE PAIR (all 63 cells per convention = 3 panels x 3 n x 7 rungs):")
    P(f"      {'conv':5s} {'cells':>6s} {'gap>0':>9s} {'mean gap':>10s} {'median':>9s} "
      f"{'min':>9s} {'max':>9s} {'mean gapOOS':>12s} {'OOS gap>0':>10s}")
    for conv in CONV:
        s = pair[pair.conv == conv]
        P(f"      {conv:5s} {len(s):6d} {f'{int((s.gap>0).sum())}/{len(s)}':>9s} "
          f"{s.gap.mean():+10.4f} {s.gap.median():+9.4f} {s.gap.min():+9.4f} "
          f"{s.gap.max():+9.4f} {s.gap_OOS.mean():+12.4f} "
          f"{f'{int((s.gap_OOS>0).sum())}/{len(s)}':>10s}")
    P(f"\n      by panel at the protocol rung, both conventions side by side:")
    P(f"      {'panel':9s} {'n':>3s} {'gap dg':>9s} {'gap rw':>9s} {'share of dg gap':>16s} "
      f"{'gapOOS dg':>10s} {'gapOOS rw':>10s}")
    for pk in G.panel.unique():
        for n in NS:
            d = pair[(pair.panel == pk) & (pair.n == n) & (pair.cost == PROTO)
                     & (pair.conv == "dg")].iloc[0]
            r = pair[(pair.panel == pk) & (pair.n == n) & (pair.cost == PROTO)
                     & (pair.conv == "rw")].iloc[0]
            sh = f"{r.gap/d.gap:.0%}" if abs(d.gap) > 1e-9 else "n/a"
            P(f"      {pk:9s} {n:3d} {d.gap:+9.4f} {r.gap:+9.4f} {sh:>16s} "
              f"{d.gap_OOS:+10.4f} {r.gap_OOS:+10.4f}")
    P(f"\n  THE FULL CAP LADDER at the protocol rung (Sharpe; no point is ever selected):")
    for conv in CONV:
        P(f"\n      [{conv}]  {'panel':9s} {'n':>3s} " +
          " ".join(f"{capname(c):>8s}" for c in CAPS) + "     mean invested (OFF / 0.60)")
        for pk in G.panel.unique():
            for n in NS:
                r = G[(G.panel == pk) & (G.n == n) & (G.conv == conv)
                      & (G.cost == PROTO)].set_index("capname").reindex(
                          [capname(c) for c in CAPS])
                P(f"            {pk:9s} {n:3d} " +
                  " ".join(f"{v:8.4f}" for v in r.Sharpe.values) +
                  f"     {float(r.loc['OFF','invested']):.3f} / "
                  f"{float(r.loc['0.60','invested']):.3f}")
    return pair


# --------------------------------------------------------------------------- part 2
def walkforward(G, REF, pair):
    P("\n" + "=" * 118)
    P("PART 2 — RULE 8.  Two reads.  (i) the PRE-REGISTERED arm: OFF is committed before any")
    P("         number, so its OOS is read straight, no selection.  (ii) the SELECTED arm:")
    P("         the cap chosen on IS <= 2016-12-31 by IS Sharpe, OOS read once — idea 228's")
    P("         procedure, repeated here so the two can be compared on the same books.")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        so = metrics(REF[pk]["spy"].loc[OOS_START:])
        for conv in CONV:
            for n in NS:
                for cost in COSTS:
                    lad = G[(G.panel == pk) & (G.n == n) & (G.conv == conv)
                            & (G.cost == cost)]
                    s060 = lad[lad.cap == 0.60].iloc[0]
                    soff = lad[~np.isfinite(lad.cap)].iloc[0]
                    pick = lad.loc[lad.IS_Sharpe.idxmax()]
                    best = lad.loc[lad.OOS_Sharpe.idxmax()]
                    v2 = net(*REF[pk]["v2"], cost)
                    v1 = net(*REF[pk]["v1"], cost)
                    rows.append(dict(
                        panel=pk, conv=conv, n=n, cost=cost,
                        prereg_OOS=soff.OOS_Sharpe, base_OOS=s060.OOS_Sharpe,
                        prereg_margin=soff.OOS_Sharpe - s060.OOS_Sharpe,
                        IS_pick=pick.capname, pick_OOS=pick.OOS_Sharpe,
                        pick_margin=pick.OOS_Sharpe - s060.OOS_Sharpe,
                        pick_is_off=bool(not np.isfinite(pick.cap)),
                        oos_argmax=best.capname, best_OOS=best.OOS_Sharpe,
                        regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                        prereg_OOS_CAGR=soff.OOS_CAGR, prereg_OOS_MaxDD=soff.OOS_MaxDD,
                        base_OOS_CAGR=s060.OOS_CAGR, base_OOS_MaxDD=s060.OOS_MaxDD,
                        spy_OOS_CAGR=so["CAGR"], spy_OOS_Sharpe=so["Sharpe"],
                        spy_OOS_MaxDD=so["MaxDD"],
                        v2_OOS_Sharpe=metrics(v2.loc[OOS_START:])["Sharpe"],
                        v1_OOS_Sharpe=metrics(v1.loc[OOS_START:])["Sharpe"]))
    WF = pd.DataFrame(rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  (i) the PRE-REGISTERED OFF arm's OOS margin over max_vol = 0.60, all 126 cells:")
    P(f"      {'conv':5s} {'cells':>6s} {'margin>0':>10s} {'mean':>9s} {'median':>9s} "
      f"{'min':>9s} {'max':>9s}")
    for conv in CONV:
        s = WF[WF.conv == conv]
        P(f"      {conv:5s} {len(s):6d} {f'{int((s.prereg_margin>0).sum())}/{len(s)}':>10s} "
          f"{s.prereg_margin.mean():+9.4f} {s.prereg_margin.median():+9.4f} "
          f"{s.prereg_margin.min():+9.4f} {s.prereg_margin.max():+9.4f}")
    P(f"\n      by panel (protocol rung):")
    P(f"      {'panel':9s} {'n':>3s} {'conv':5s} {'OOS OFF':>8s} {'OOS 0.60':>9s} "
      f"{'margin':>8s} {'IS pick':>8s} {'OOS pick':>9s} {'sel. margin':>12s} "
      f"{'OOS argmax':>11s}")
    for r in WF[WF.cost == PROTO].itertuples():
        P(f"      {r.panel:9s} {r.n:3d} {r.conv:5s} {r.prereg_OOS:8.4f} {r.base_OOS:9.4f} "
          f"{r.prereg_margin:+8.4f} {r.IS_pick:>8s} {r.pick_OOS:9.4f} "
          f"{r.pick_margin:+12.4f} {r.oos_argmax:>11s}")
    P(f"\n  (ii) does the CHOOSER pick OFF?  (idea 228 said its whole rule-8 premium was this)")
    for conv in CONV:
        s = WF[WF.conv == conv]
        P(f"      {conv:5s}: IS chooser picks OFF in {int(s.pick_is_off.sum())} of {len(s)} "
          f"cells; mean selected margin {s.pick_margin.mean():+.4f} vs pre-registered "
          f"{s.prereg_margin.mean():+.4f}; mean REGRET {s.regret.mean():.4f}")
    P(f"\n  (iii) OOS CAGR / Sharpe / MaxDD at 10 bps, n = 20 (idea 228's default):")
    for r in WF[(WF.cost == PROTO) & (WF.n == 20)].itertuples():
        P(f"      {r.panel:9s} {r.conv:5s}  OFF {r.prereg_OOS_CAGR:7.2%}/{r.prereg_OOS:6.3f}/"
          f"{r.prereg_OOS_MaxDD:7.2%}   0.60 {r.base_OOS_CAGR:7.2%}/{r.base_OOS:6.3f}/"
          f"{r.base_OOS_MaxDD:7.2%}   SPY {r.spy_OOS_CAGR:7.2%}/{r.spy_OOS_Sharpe:6.3f}/"
          f"{r.spy_OOS_MaxDD:7.2%}   v2 {r.v2_OOS_Sharpe:6.3f}  v1 {r.v1_OOS_Sharpe:6.3f}")
    return WF


# --------------------------------------------------------------------------- part 3
def keep_paths(G, REF):
    P("\n" + "=" * 118)
    P("PART 3 — BOTH KEEP PATHS on every grid point (4a vs the live RULES v2; 4b vs SPY).")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        spy = REF[pk]["spy"]
        sm, so = metrics(spy), metrics(spy.loc[OOS_START:])
        ss = stats(spy)
        for cost in COSTS:
            v2 = net(*REF[pk]["v2"], cost)
            vs = stats(v2)
            for r in G[(G.panel == pk) & (G.cost == cost)].itertuples():
                f4a = []
                if not r.H1 > vs["H1"]:
                    f4a.append("H1")
                if not r.H2 > vs["H2"]:
                    f4a.append("H2")
                if not r.MaxDD >= vs["MaxDD"]:
                    f4a.append("DD")
                f4b = []
                if not r.H1 > ss["H1"]:
                    f4b.append("H1")
                if not r.H2 > ss["H2"]:
                    f4b.append("H2")
                if not r.OOS_Sharpe > so["Sharpe"]:
                    f4b.append("OOS")
                if not r.MaxDD >= 0.60 * sm["MaxDD"]:
                    f4b.append("DD")
                if not r.CAGR >= 0.70 * sm["CAGR"]:
                    f4b.append("CAGR")
                rows.append(dict(panel=pk, cap=r.capname, n=r.n, conv=r.conv, cost=cost,
                                 CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1,
                                 H2=r.H2, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                 OOS_MaxDD=r.OOS_MaxDD, invested=r.invested,
                                 keep4a=not f4a, keep4b=not f4b,
                                 fail4a="|".join(f4a) or "none",
                                 fail4b="|".join(f4b) or "none"))
    KP = pd.DataFrame(rows)
    KP.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  {len(KP)} points.  4a {int(KP.keep4a.sum())}   4b {int(KP.keep4b.sum())}   "
      f"both {int((KP.keep4a & KP.keep4b).sum())}")
    P(f"\n      {'panel':9s} {'conv':5s} {'points':>7s} {'4a':>9s} {'4b':>9s}")
    for pk in G.panel.unique():
        for conv in CONV:
            g = KP[(KP.panel == pk) & (KP.conv == conv)]
            P(f"      {pk:9s} {conv:5s} {len(g):7d} {f'{int(g.keep4a.sum())}/{len(g)}':>9s} "
              f"{f'{int(g.keep4b.sum())}/{len(g)}':>9s}")
    P(f"\n      binding 4b bar over all failing points:")
    fc = {}
    for f in KP[~KP.keep4b].fail4b:
        for t in f.split("|"):
            fc[t] = fc.get(t, 0) + 1
    for t, k in sorted(fc.items(), key=lambda x: -x[1]):
        P(f"          {t:6s} binds on {k:4d} points")
    P(f"\n      4b pass rate by cap (protocol rung, both conventions, all n):")
    P(f"      {'cap':>6s} " + " ".join(f"{pk:>12s}" for pk in G.panel.unique()))
    for cap in CAPS:
        vals = []
        for pk in G.panel.unique():
            g = KP[(KP.panel == pk) & (KP.cost == PROTO) & (KP.cap == capname(cap))]
            vals.append(f"{int(g.keep4b.sum())}/{len(g)}")
        P(f"      {capname(cap):>6s} " + " ".join(f"{v:>12s}" for v in vals))
    pas = KP[KP.keep4b & (KP.cost == PROTO)]
    P(f"\n      4b passes at the protocol rung: {len(pas)}")
    for r in pas.sort_values("Sharpe", ascending=False).itertuples():
        P(f"          {r.panel:9s} cap {r.cap:>4s} n={r.n:3d} {r.conv:3s}  "
          f"{r.CAGR:7.2%}/{r.Sharpe:6.3f}/{r.MaxDD:7.2%}  halves {r.H1:.3f}/{r.H2:.3f}  "
          f"OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:6.3f}/{r.OOS_MaxDD:7.2%}  "
          f"inv {r.invested:.3f}")
    return KP


def main():
    t0 = time.time()
    P("# Idea 232 — does-the-vol-gate-corner-survive-being-pre-registered")
    P(f"# cloud lane, {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}")
    P(f"# idea 228's book: composite (no vol tilt), 200d gate g=0 FIXED, top-n, weekly, t+1.")
    P(f"# P1 max_vol in {[capname(c) for c in CAPS]}; P2 cost rung in {COSTS} bps.")
    P(f"# reporting axes (never chosen on): panel, n in {NS}, gross convention in {CONV}.")
    PANELS = build_panels()
    validate_fast(PANELS)
    G, REF = run_grid(PANELS)
    check_identity(PANELS)
    check_premise(G)
    pair = the_pair(G)
    walkforward(G, REF, pair)
    keep_paths(G, REF)
    P(f"\n\n[done in {time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
