#!/usr/bin/env python3
"""IDEA 768 - is the 4b DD CAP decided by WEIGHT HANDLING on more than 3 of 240 books?
Cloud lane, 2026-09-11.

THE QUESTION
------------
Idea 562 priced the engine's weight-handling channel two ways -
    DRIFT = the engine's native behaviour (held weights drift between rebalance days and are
            renormalised by the book's OWN total each bar), and
    RTT   = "rebalance to target", the same cadence targets RESTORED EVERY DAY (freq='D' on
            the cadence-ffilled target matrix), paying 10 bps on the extra turnover
- and found the choice worth a median +0.0000 of Sharpe yet enough to FLIP 3 of 240 KEEP
verdicts, every one of them the 4b DRAWDOWN CAP at a 0.13-0.26 pp margin against a -20.23%
bar.  That is a claim about a BAR, not about a strategy: if a book's realised MaxDD sits
closer to 0.60 x |SPY MaxDD| than the handling convention is wide, then the published 4b
verdict is a statement about which convention the script happened to use.

This run re-cuts the question directly on prices rather than on the record's markdown, so it
can carry the mandatory rule-8 leg.  It builds a book grid, runs EVERY book under BOTH
handlings, and measures

    dDD_pp   = |MaxDD_RTT| - |MaxDD_DRIFT|                 (the handling difference, pp)
    margin   = 0.60 x |MaxDD_SPY| - |MaxDD_book|           (pp of room under the 4b DD cap)

A book is INSIDE-ONE-HANDLING when |margin| <= |dDD_pp| on its own row: its DD-cap verdict is
not separable from the convention.  A book FLIPS when the DD cap passes under one handling and
fails under the other.  The headline is the count of each, full sample and out of sample.

PRE-REGISTERED GATES (all bars fixed before any number was read)
---------------------------------------------------------------
  G0  run() reproduces engine.backtest returns AND turnover                  bar 1e-12
  G1  at cadence D, DRIFT and RTT are the SAME BOOK by construction
      (held == target on every bar), so max|d returns| and max|d turnover|   bar 0.0 EXACT
  G2  the derived cost rung r0 - turn*c/1e4 equals a fresh run at that rung  bar 1e-15
  G3  RTT turnover >= DRIFT turnover on every book at W/M/Q (restoring a
      drifted book can only add trades)                                      bar 0.0

GRID.  2 TUNED PARAMS ONLY: CADENCE {D,W,M,Q} x GROSS {0.50,0.75,1.00}.
PANEL {U56,B136,SMALL439}, CONSTRUCTION {DEGROSS,RESPREAD}, GATE {BAND3,MA200} and HANDLING
{DRIFT,RTT} are REPORTED axes, never selected over.  That is 3x2x2 = 12 families x 12 tuned
points = 144 books, 288 runs; every grid point is written to .grid.csv and none is hidden.
Costs 10 bps per unit turnover (0 and 25 derived exactly and reported).  Next-day execution.
No shorting, no leverage.  IS = start..2016-12-31, OOS = 2017-01-01..end, read ONCE (rule 8).

BOTH KEEP PATHS are scored on every book against that book's own panel:
  4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2
  4b  Sharpe > SPY in BOTH halves AND out of sample, |MaxDD| <= 0.60 x |SPY|, CAGR >= 0.70 x SPY

SURVIVORSHIP.  B136 and SMALL439 are CURRENT constituents only: dead names are absent, CAGR
levels are inflated and MaxDD levels are understated, which flatters the 4b DD cap in
particular.  The 44 SMALL names with max_1d_move >= 1.0 are dropped (data/small_meta.csv).
The headline (a handling DIFFERENCE inside one panel, same names both arms) is very largely
immune to that bias; the KEEP columns and the rule-8 levels are NOT, and are read as such.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .margins.csv .walkforward.csv .keeppaths.csv .rungs.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights, band_state
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
RUNGS = [0, 10, 25]
PANELS = ["U56", "B136", "SMALL439"]
CADENCES = ["D", "W", "M", "Q"]                 # tuned param 1
GROSSES = [0.50, 0.75, 1.00]                    # tuned param 2
CONSTRUCTIONS = ["DEGROSS", "RESPREAD"]         # reported
GATES = ["BAND3", "MA200"]                      # reported
HANDLING = ["DRIFT", "RTT"]                     # reported
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

BAR_ENGINE = 1e-12
BAR_EXACT = 0.0
BAR_RUNG = 1e-15

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def run(px, W, freq):
    """engine.backtest's arithmetic, returning the ZERO-COST path, turnover, the HELD weight
    matrix and the TARGET-IN-FORCE matrix (gate G0 checks it against engine.backtest)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    tgt = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    t_cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
            t_cur = new
        held[i] = cur
        tgt[i] = t_cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    r0 = pd.Series(np.nansum(held * rets, axis=1), index=px.index)
    return r0, pd.Series(turn, index=px.index), held, tgt


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


def rtt_weights(W, idx, freq):
    """The cadence's targets restored EVERY day: sample W on the cadence schedule, hold flat."""
    m = rebalance_mask(idx, freq)
    return W.where(m, np.nan).ffill().fillna(0.0)


def run_handled(px, W, freq, handling):
    """One book under one handling.  DRIFT = native engine at `freq`.  RTT = the same cadence
    targets restored every day, i.e. the cadence-ffilled target matrix run at freq='D'."""
    if handling == "DRIFT":
        return run(px, W, freq)
    return run(px, rtt_weights(W, px.index, freq), "D")


def gate_mask(px, gate):
    if gate == "BAND3":
        return band_state(px, 0.03) & live_mask(px)
    return (px > px.rolling(200).mean()) & live_mask(px)


def book(px, g, construction, gross):
    """DEGROSS: gated-out weight goes to cash (divide by the live panel count).
    RESPREAD: the same gross is re-spread over the survivors (divide by the gate count)."""
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


# ================================================================== main
def main():
    P("=" * 170)
    P("IDEA 768 - is the 4b DD CAP decided by WEIGHT HANDLING on more than 3 of 240 books?"
      "   (cloud lane, 2026-09-11)")
    P("=" * 170)
    P("PROTOCOL: 10 bps per unit turnover (0/25 derived exactly and reported), next-day")
    P(f"execution, no shorting, no leverage.  IS = start..{IS_END}, OOS = {OOS_START}..end.")
    P(f"2 tuned params: CADENCE {CADENCES} x GROSS {GROSSES}.")
    P(f"PANEL {PANELS}, CONSTRUCTION {CONSTRUCTIONS}, GATE {GATES}, HANDLING {HANDLING} are")
    P("REPORTED axes, never selected over.  Both KEEP paths on every book; every grid point")
    P("is written to .grid.csv.")
    P("SURVIVORSHIP: B136/SMALL439 are current constituents only; CAGR inflated, MaxDD")
    P("understated, which FLATTERS the 4b DD cap.  The handling DIFFERENCE is immune; the")
    P("KEEP columns and rule-8 levels are not.")
    flush_log()

    u, b = load_universe(), load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL439": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "  ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")

    # ------------------------------------------------------------------ gates
    P("\n" + "=" * 170)
    P("PRE-REGISTERED GATES")
    P("=" * 170)
    g0 = g2 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        for freq in ("D", "W", "Q"):
            a = backtest(px, W, cost_bps=COST_BPS, freq=freq)
            r0, tn, _, _ = run(px, W, freq)
            g0 = max(g0, float((a["returns"] - rung(r0, tn, COST_BPS)).abs().max()),
                     float((a["turnover"] - tn).abs().max()))
            for c in RUNGS:
                fresh = backtest(px, W, cost_bps=c, freq=freq)["returns"]
                g2 = max(g2, float((fresh - rung(r0, tn, c)).abs().max()))
    P(f"  G0  run() vs engine.backtest (returns AND turnover, 3 panels x 3 cadences)"
      f"   max |d| = {g0:.3e}   bar {BAR_ENGINE:.0e}   {'PASS' if g0 <= BAR_ENGINE else 'FAIL'}")
    P(f"  G2  derived cost rung vs a fresh run at that rung (rungs {RUNGS})"
      f"        max |d| = {g2:.3e}   bar {BAR_RUNG:.0e}   {'PASS' if g2 <= BAR_RUNG else 'FAIL'}")

    g1 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        a0, t0, _, _ = run_handled(px, W, "D", "DRIFT")
        a1, t1, _, _ = run_handled(px, W, "D", "RTT")
        g1 = max(g1, float((a0 - a1).abs().max()), float((t0 - t1).abs().max()))
    P(f"  G1  at cadence D, DRIFT == RTT by construction (returns AND turnover)"
      f"        max |d| = {g1:.3e}   bar EXACT 0   {'PASS' if g1 <= BAR_EXACT else 'FAIL'}")
    flush_log()

    # ------------------------------------------------------------------ grid
    P("\n" + "=" * 170)
    P("THE GRID - every point reported")
    P("=" * 170)
    rows, g3_viol, g3_min = [], 0, np.inf
    bench = {}
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        spy_r = spy_px.pct_change().fillna(0).loc[start:]
        bench[pn] = dict(SPY=stat(spy_r))
        for cad in CADENCES:
            bR = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
            bench[pn]["RULESv2"] = stat(bR)
        gm = {gt: gate_mask(px, gt) for gt in GATES}
        for gt in GATES:
            for con in CONSTRUCTIONS:
                for gr in GROSSES:
                    W = book(px, gm[gt], con, gr)
                    for cad in CADENCES:
                        for hnd in HANDLING:
                            r0, tn, _, _ = run_handled(px, W, cad, hnd)
                            r0, tn = r0.loc[start:], tn.loc[start:]
                            st = stat(rung(r0, tn, COST_BPS))
                            row = dict(panel=pn, gate=gt, con=con, gross=gr, cad=cad, hnd=hnd,
                                       turn=float(tn.sum()), **st)
                            for c in RUNGS:
                                row[f"Sharpe{c}"] = metrics(rung(r0, tn, c))["Sharpe"]
                                row[f"CAGR{c}"] = metrics(rung(r0, tn, c))["CAGR"]
                            rows.append(row)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"  {len(G)} runs = {len(G)//2} books x {len(HANDLING)} handlings "
      f"({len(PANELS)} panels x {len(GATES)} gates x {len(CONSTRUCTIONS)} constructions "
      f"x {len(GROSSES)} gross x {len(CADENCES)} cadences).  Written to .grid.csv")

    # G3: RTT turnover >= DRIFT turnover at W/M/Q
    key = ["panel", "gate", "con", "gross", "cad"]
    piv = G.pivot_table(index=key, columns="hnd", values="turn")
    wmq = piv.loc[piv.index.get_level_values("cad") != "D"]
    d = wmq["RTT"] - wmq["DRIFT"]
    g3_viol = int((d < -BAR_EXACT).sum())
    g3_min = float(d.min())
    P(f"  G3  RTT turnover >= DRIFT turnover on all {len(wmq)} W/M/Q books"
      f"   min (RTT-DRIFT) = {g3_min:.4f}   violations {g3_viol}   "
      f"{'PASS' if g3_viol == 0 else 'FAIL'}")
    flush_log()

    # ------------------------------------------------------------------ the headline
    P("\n" + "=" * 170)
    P("A.  THE HANDLING DIFFERENCE IN MaxDD, AND THE 4b DD CAP MARGIN")
    P("=" * 170)
    M = G.pivot_table(index=key, columns="hnd",
                      values=["MaxDD", "oMaxDD", "Sharpe", "oSharpe", "CAGR"]).reset_index()
    M.columns = ["_".join([c for c in t if c]) for t in M.columns.to_flat_index()]
    M["ddDRIFT"] = M["MaxDD_DRIFT"].abs() * 100
    M["ddRTT"] = M["MaxDD_RTT"].abs() * 100
    M["dDD_pp"] = M["ddRTT"] - M["ddDRIFT"]
    M["oddDRIFT"] = M["oMaxDD_DRIFT"].abs() * 100
    M["oddRTT"] = M["oMaxDD_RTT"].abs() * 100
    M["odDD_pp"] = M["oddRTT"] - M["oddDRIFT"]
    M["dSharpe"] = M["Sharpe_RTT"] - M["Sharpe_DRIFT"]
    M["spy_dd"] = M["panel"].map({p: abs(bench[p]["SPY"]["MaxDD"]) * 100 for p in PANELS})
    M["spy_odd"] = M["panel"].map({p: abs(bench[p]["SPY"]["oMaxDD"]) * 100 for p in PANELS})
    M["cap"] = 0.60 * M["spy_dd"]
    M["ocap"] = 0.60 * M["spy_odd"]
    M["marginDRIFT"] = M["cap"] - M["ddDRIFT"]
    M["marginRTT"] = M["cap"] - M["ddRTT"]
    M["omarginDRIFT"] = M["ocap"] - M["oddDRIFT"]
    M["omarginRTT"] = M["ocap"] - M["oddRTT"]
    M["ddpassDRIFT"] = M["marginDRIFT"] >= 0
    M["ddpassRTT"] = M["marginRTT"] >= 0
    M["flipDD"] = M["ddpassDRIFT"] != M["ddpassRTT"]
    M["oddpassDRIFT"] = M["omarginDRIFT"] >= 0
    M["oddpassRTT"] = M["omarginRTT"] >= 0
    M["oflipDD"] = M["oddpassDRIFT"] != M["oddpassRTT"]
    M["inside"] = M["marginDRIFT"].abs() <= M["dDD_pp"].abs()
    M["oinside"] = M["omarginDRIFT"].abs() <= M["odDD_pp"].abs()
    M.to_csv(f"{OUT}.margins.csv", index=False)

    nb = len(M)
    P(f"  {nb} books.  SPY MaxDD by panel (full / OOS), and the 0.60x cap:")
    for p in PANELS:
        P(f"    {p:9s} SPY MaxDD {abs(bench[p]['SPY']['MaxDD'])*100:7.2f}%  cap "
          f"{0.60*abs(bench[p]['SPY']['MaxDD'])*100:6.2f}%   |   OOS SPY "
          f"{abs(bench[p]['SPY']['oMaxDD'])*100:7.2f}%  cap "
          f"{0.60*abs(bench[p]['SPY']['oMaxDD'])*100:6.2f}%")
    dsub = M.loc[M.cad != "D"]
    P(f"\n  |dDD_pp| = | |MaxDD_RTT| - |MaxDD_DRIFT| |, the width of the handling convention.")
    P(f"    all {nb} books        median {M.dDD_pp.abs().median():.4f} pp   "
      f"mean {M.dDD_pp.abs().mean():.4f}   p90 {M.dDD_pp.abs().quantile(.90):.4f}   "
      f"max {M.dDD_pp.abs().max():.4f}")
    P(f"    W/M/Q only ({len(dsub)})     median {dsub.dDD_pp.abs().median():.4f} pp   "
      f"mean {dsub.dDD_pp.abs().mean():.4f}   p90 {dsub.dDD_pp.abs().quantile(.90):.4f}   "
      f"max {dsub.dDD_pp.abs().max():.4f}")
    P(f"    d Sharpe (RTT-DRIFT), W/M/Q     median {dsub.dSharpe.median():+.4f}   "
      f"mean {dsub.dSharpe.mean():+.4f}   max |.| {dsub.dSharpe.abs().max():.4f}")
    P("\n  by cadence (W/M/Q; D is the identity leg, gate G1):")
    P(M.groupby("cad").agg(books=("dDD_pp", "size"), med_absdDD=("dDD_pp", lambda x: x.abs().median()),
                           max_absdDD=("dDD_pp", lambda x: x.abs().max()),
                           med_dSharpe=("dSharpe", "median")).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  by panel:")
    P(M.groupby("panel").agg(books=("dDD_pp", "size"), med_absdDD=("dDD_pp", lambda x: x.abs().median()),
                             max_absdDD=("dDD_pp", lambda x: x.abs().max())).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  by construction:")
    P(M.groupby("con").agg(books=("dDD_pp", "size"), med_absdDD=("dDD_pp", lambda x: x.abs().median()),
                           max_absdDD=("dDD_pp", lambda x: x.abs().max())).to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n" + "-" * 170)
    P("  THE HEADLINE - DD-cap verdicts that the handling convention decides")
    P("-" * 170)
    P(f"    full sample:  DD cap PASS under DRIFT {int(M.ddpassDRIFT.sum())}/{nb},"
      f"  under RTT {int(M.ddpassRTT.sum())}/{nb},  FLIPPED {int(M.flipDD.sum())}")
    P(f"    OOS 2017+  :  DD cap PASS under DRIFT {int(M.oddpassDRIFT.sum())}/{nb},"
      f"  under RTT {int(M.oddpassRTT.sum())}/{nb},  FLIPPED {int(M.oflipDD.sum())}")
    P(f"    INSIDE-ONE-HANDLING (|margin| <= |dDD_pp|):  full {int(M.inside.sum())}/{nb}"
      f" ({M.inside.mean():.1%}),   OOS {int(M.oinside.sum())}/{nb} ({M.oinside.mean():.1%})")
    nz = M.loc[M.cad != "D"]
    P(f"    restricted to the {len(nz)} W/M/Q books (where the channel is live at all):"
      f"  INSIDE full {int(nz.inside.sum())} ({nz.inside.mean():.1%}),"
      f"  OOS {int(nz.oinside.sum())} ({nz.oinside.mean():.1%}),"
      f"  FLIPPED full {int(nz.flipDD.sum())}, OOS {int(nz.oflipDD.sum())}")
    if M.flipDD.any() or M.oflipDD.any():
        P("\n    every flipped book:")
        P(M.loc[M.flipDD | M.oflipDD,
                ["panel", "gate", "con", "gross", "cad", "ddDRIFT", "ddRTT", "dDD_pp", "cap",
                 "marginDRIFT", "marginRTT", "oddDRIFT", "oddRTT", "ocap", "omarginDRIFT",
                 "omarginRTT"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("\n    NO book flips its DD-cap verdict on handling, full sample or OOS.")
    P("\n    the 8 books sitting closest to the cap (|marginDRIFT| smallest), with the")
    P("    handling width beside the margin:")
    P(M.reindex(M.marginDRIFT.abs().sort_values().index)[
        ["panel", "gate", "con", "gross", "cad", "ddDRIFT", "cap", "marginDRIFT", "dDD_pp",
         "inside"]].head(8).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # ------------------------------------------------------------------ keep paths
    P("\n" + "=" * 170)
    P("B.  BOTH KEEP PATHS ON EVERY BOOK (4a vs RULES v2 on the same panel, 4b vs SPY)")
    P("=" * 170)
    K = []
    for _, r in G.iterrows():
        s = r.to_dict()
        bm, sp = bench[r.panel]["RULESv2"], bench[r.panel]["SPY"]
        K.append(dict(panel=r.panel, gate=r.gate, con=r.con, gross=r.gross, cad=r.cad, hnd=r.hnd,
                      CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                      oCAGR=r.oCAGR, oSharpe=r.oSharpe, oMaxDD=r.oMaxDD,
                      keep4a=verdict_4a(s, bm), fail4b=fail_4b(s, sp)))
    K = pd.DataFrame(K)
    K["keep4b"] = K.fail4b == "-"
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(f"  benchmarks per panel (full sample, from px.index[260]):")
    for p in PANELS:
        bm, sp = bench[p]["RULESv2"], bench[p]["SPY"]
        P(f"    {p:9s} RULES v2  CAGR {bm['CAGR']:7.2%}  Sharpe {bm['Sharpe']:.4f} "
          f"({bm['H1']:.4f}/{bm['H2']:.4f})  MaxDD {bm['MaxDD']:7.2%}  | OOS "
          f"{bm['oCAGR']:7.2%}/{bm['oSharpe']:.4f}/{bm['oMaxDD']:7.2%}")
        P(f"    {'':9s} SPY       CAGR {sp['CAGR']:7.2%}  Sharpe {sp['Sharpe']:.4f} "
          f"({sp['H1']:.4f}/{sp['H2']:.4f})  MaxDD {sp['MaxDD']:7.2%}  | OOS "
          f"{sp['oCAGR']:7.2%}/{sp['oSharpe']:.4f}/{sp['oMaxDD']:7.2%}")
    P(f"\n  4a PASS {int(K.keep4a.sum())}/{len(K)}    4b PASS {int(K.keep4b.sum())}/{len(K)}")
    P("\n  counts by handling:")
    P(K.groupby("hnd").agg(n=("keep4a", "size"), pass4a=("keep4a", "sum"),
                           pass4b=("keep4b", "sum")).to_string())
    P("\n  4b first-fail tokens (SET semantics: every failing bar listed):")
    P(K.fail4b.value_counts().to_string())
    kp = K.pivot_table(index=key, columns="hnd", values=["keep4a", "keep4b"])
    fl4a = int((kp[("keep4a", "DRIFT")] != kp[("keep4a", "RTT")]).sum())
    fl4b = int((kp[("keep4b", "DRIFT")] != kp[("keep4b", "RTT")]).sum())
    P(f"\n  KEEP verdicts FLIPPED by handling:  4a {fl4a}/{nb}    4b {fl4b}/{nb}")
    if K.keep4b.any():
        P("\n  every 4b passer:")
        P(K.loc[K.keep4b, ["panel", "gate", "con", "gross", "cad", "hnd", "CAGR", "Sharpe",
                           "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if K.keep4a.any():
        P(f"\n  4a passers ({int(K.keep4a.sum())}), first 20:")
        P(K.loc[K.keep4a, ["panel", "gate", "con", "gross", "cad", "hnd", "CAGR", "Sharpe",
                           "MaxDD", "H1", "H2"]].head(20)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # ------------------------------------------------------------------ rule 8
    P("\n" + "=" * 170)
    P("C.  RULE 8 WALK-FORWARD - (cadence, gross) chosen on IS Sharpe ALONE, OOS read ONCE")
    P("=" * 170)
    WF = []
    for (pn, gt, con, hnd), grp in G.groupby(["panel", "gate", "con", "hnd"]):
        pick = grp.loc[grp.isSharpe.idxmax()]
        bm, sp = bench[pn]["RULESv2"], bench[pn]["SPY"]
        so = dict(H1=pick.oSharpe, H2=pick.oSharpe, Sharpe=pick.oSharpe, CAGR=pick.oCAGR,
                  MaxDD=pick.oMaxDD, oSharpe=pick.oSharpe)
        bo = dict(H1=bm["oSharpe"], H2=bm["oSharpe"], MaxDD=bm["oMaxDD"])
        spo = dict(H1=sp["oSharpe"], H2=sp["oSharpe"], MaxDD=sp["oMaxDD"], CAGR=sp["oCAGR"],
                   oSharpe=sp["oSharpe"])
        WF.append(dict(panel=pn, gate=gt, con=con, hnd=hnd, pick_cad=pick.cad,
                       pick_gross=pick.gross, isSharpe=pick.isSharpe,
                       oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                       base_oCAGR=bm["oCAGR"], base_oSharpe=bm["oSharpe"], base_oMaxDD=bm["oMaxDD"],
                       spy_oCAGR=sp["oCAGR"], spy_oSharpe=sp["oSharpe"], spy_oMaxDD=sp["oMaxDD"],
                       oos4a=verdict_4a(so, bo), oos4b_fail=fail_4b(so, spo)))
    WF = pd.DataFrame(WF)
    WF["oos4b"] = WF.oos4b_fail == "-"
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  {len(WF)} selector cells (panel x gate x construction x handling), each choosing one")
    P(f"  of {len(CADENCES)*len(GROSSES)} (cadence,gross) points on IS Sharpe alone.")
    P(WF[["panel", "gate", "con", "hnd", "pick_cad", "pick_gross", "isSharpe", "oCAGR",
          "oSharpe", "oMaxDD", "base_oSharpe", "spy_oSharpe", "oos4a", "oos4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  OOS 4a PASS {int(WF.oos4a.sum())}/{len(WF)}   OOS 4b PASS {int(WF.oos4b.sum())}/{len(WF)}")
    P("  OOS 4b fail tokens: " + WF.oos4b_fail.value_counts().to_string().replace("\n", " | "))
    same = WF.pivot_table(index=["panel", "gate", "con"], columns="hnd",
                          values=["pick_cad", "pick_gross"], aggfunc="first")
    agree = int((same[("pick_cad", "DRIFT")] == same[("pick_cad", "RTT")]).sum())
    P(f"\n  the IS selector picks the SAME cadence under both handlings in {agree}/"
      f"{len(same)} cells; OOS Sharpe spread between handlings at the picked point: "
      f"median {WF.pivot_table(index=['panel','gate','con'], columns='hnd', values='oSharpe').pipe(lambda d: (d['RTT']-d['DRIFT']).abs().median()):.4f}")
    P("\n  OOS levels vs benchmarks, best cell per panel (by OOS Sharpe):")
    for p in PANELS:
        w = WF.loc[WF.panel == p].sort_values("oSharpe", ascending=False).iloc[0]
        P(f"    {p:9s} best {w.gate}/{w.con}/{w.hnd} @ ({w.pick_cad},{w.pick_gross})  "
          f"OOS CAGR {w.oCAGR:7.2%} Sharpe {w.oSharpe:.4f} MaxDD {w.oMaxDD:7.2%}   vs "
          f"RULES v2 {w.base_oCAGR:7.2%}/{w.base_oSharpe:.4f}/{w.base_oMaxDD:7.2%}   vs SPY "
          f"{w.spy_oCAGR:7.2%}/{w.spy_oSharpe:.4f}/{w.spy_oMaxDD:7.2%}")
    flush_log()

    # ------------------------------------------------------------------ rungs
    P("\n" + "=" * 170)
    P("D.  COST RUNGS - the handling channel at 0 / 10 / 25 bps")
    P("=" * 170)
    R = []
    for c in RUNGS:
        pv = G.pivot_table(index=key, columns="hnd", values=f"Sharpe{c}")
        cv = G.pivot_table(index=key, columns="hnd", values=f"CAGR{c}")
        w = pv.loc[pv.index.get_level_values("cad") != "D"]
        wc = cv.loc[cv.index.get_level_values("cad") != "D"]
        R.append(dict(bps=c, med_dSharpe=float((w["RTT"] - w["DRIFT"]).median()),
                      max_absdSharpe=float((w["RTT"] - w["DRIFT"]).abs().max()),
                      med_dCAGR_pp=float((wc["RTT"] - wc["DRIFT"]).median() * 100),
                      min_dCAGR_pp=float((wc["RTT"] - wc["DRIFT"]).min() * 100)))
    R = pd.DataFrame(R)
    R.to_csv(f"{OUT}.rungs.csv", index=False)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  (W/M/Q books only; at D the two handlings are the same book, gate G1.)")

    # ------------------------------------------------------------------ verdict
    P("\n" + "=" * 170)
    P("VERDICT")
    P("=" * 170)
    P(f"  Handling flips the 4b DD cap on {int(M.flipDD.sum())} of {nb} books full sample and "
      f"{int(M.oflipDD.sum())} OOS;")
    P(f"  {int(M.inside.sum())} of {nb} ({M.inside.mean():.1%}) sit INSIDE one handling-width "
      f"of their own cap full sample,")
    P(f"  {int(M.oinside.sum())} ({M.oinside.mean():.1%}) OOS.  Median |dDD| over the "
      f"{len(dsub)} W/M/Q books is {dsub.dDD_pp.abs().median():.4f} pp "
      f"(max {dsub.dDD_pp.abs().max():.4f}).")
    P(f"  KEEP: 4b {int(K.keep4b.sum())}/{len(K)} in sample, OOS 4b {int(WF.oos4b.sum())}/"
      f"{len(WF)} under rule 8; 4a {int(K.keep4a.sum())}/{len(K)}, OOS 4a "
      f"{int(WF.oos4a.sum())}/{len(WF)}.")
    flush_log()
    P("\nwrote: " + ", ".join(f"{OUT.name}{e}" for e in
                              (".grid.csv", ".margins.csv", ".keeppaths.csv",
                               ".walkforward.csv", ".rungs.csv", ".console.txt")))
    flush_log()


if __name__ == "__main__":
    main()
