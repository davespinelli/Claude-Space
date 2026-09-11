#!/usr/bin/env python3
"""
IDEA 767 - is the 4a COLUMN where the MOMENTUM SLICE actually lives?
====================================================================
Lane C, 2026-09-11.

THE QUESTION.  Idea 563 priced the daily-depth-matched momentum slice (MOM-D) against the
MA slice as a book and found the head-to-head a coin toss on Sharpe (40.3% of 648 pairs).
But its KEEP columns split: of the 33 books on its 1,296-point grid that passed path 4a
(beat the LIVE BOOK), **20 were MOM-D and all 33 were DEGROSS**, while 4b (beat SPY) went
MA-THRESH 21 / MOM-D 15.  The queue's reading is that the momentum slice "lives in the 4a
column".  This run asks the only question that could move capital:

    re-cut the 4a column DIRECTLY on the momentum slice, across panels and cadences, and
    say whether ANY of idea 563's 20 MOM-D 4a passes survives rule 8.

THREE LEGS.
  A  DIRECT RE-CUT.  The momentum slice cut on its OWN depth (top q of the rankable names
     by 12-1 momentum), with no MA gate anywhere in the construction - so nothing about the
     4a column can be inherited from the gate that idea 563 matched depth to.
  B  RULE 8 on leg A.  (cadence, construction) chosen on IS Sharpe ALONE inside every
     (panel, depth, gross) cell; OOS 2017+ read ONCE; 4a and 4b re-scored out of sample.
  C  THE 20 THEMSELVES.  Idea 563's exact 20 MOM-D 4a-passing books rebuilt (gate G1), then
     put through the same rule-8 selector inside their own (panel, theta, gross) cell.  Two
     things are reported for each: is the 4a-passing dial the one an IS selector would have
     PICKED, and does the pick pass 4a OUT OF SAMPLE?

  D  GROSS-MATCHED CONTROL (derived, not tuned).  Every 4a passer is also scored against SPY
     held at the passer's OWN realised mean gross with the rest in cash.  A 4a pass that a
     scaled index beats is a statement about exposure, not about the momentum slice.

CONSTRUCTION.
  panel         U56 (data/prices.csv) / B136 (broad) / SMALL439 (small, 44 names with
                max_1d_move >= 1.0 dropped, idea 559's filter)          REPORTED axis
  slice         top k_t = ceil(q * rankable_t) names by 12-1 momentum (px[-21]/px[-252]-1),
                recomputed EVERY day; q in {0.05,0.10,0.20,0.30,0.50}   REPORTED axis
  gross         {0.50, 0.75, 1.00}                                      REPORTED axis
  construction  RESPREAD (gross/k_t on the held names) or
                DEGROSS  (gross/n_live on the held names, remainder CASH)   TUNED (1 of 2)
  cadence       {D, W, M, Q}                                               TUNED (2 of 2)
  costs         10 bps per unit turnover, next-day execution (engine convention).
                0 and 25 bps derived EXACTLY off the same held path (gate G2) and reported.

  TUNED PARAMETERS: exactly 2 - (cadence, construction), as the queue specifies.  Panel,
  depth and gross are reported axes, never selected over.  Leg A grid = 3 x 5 x 3 x 4 x 2
  = 360 books, every point in .grid.csv.  Leg C grid = 6 cells x 3 gross x 4 cadences x 2
  constructions = 144 books, every point in .the20.csv.

KEEP PATHS (both, on every book).
  4a  Sharpe > RULES v2 (same panel) in BOTH halves AND MaxDD no worse than RULES v2's.
  4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70%.
  OOS-4a STRICT   oSharpe > base in both OOS halves AND oMaxDD >= base oMaxDD.
  OOS-4a LENIENT  oSharpe > base oSharpe AND oMaxDD >= base oMaxDD.   Both reported.

GATES (pre-registered, pass or fail reported either way).
  G0  fast_run reproduces engine.backtest returns AND turnover to 1e-12, every panel, D and W.
  G1  idea 563's committed .grid.csv MOM-D rows rebuilt here: Sharpe / MaxDD / H1 / H2 /
      oSharpe on the 144 leg-C books to 1e-9.  U56 is NOT in leg C (563 recorded no U56 4a
      pass) so the daily re-download drift it flagged cannot enter this gate.
  G2  derived cost rung == a fresh run at that rung, 1e-15.
  G3  depth identity: the leg-A slice holds exactly ceil(q * rankable) names on every day.

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only.  Dead names are absent, so
CAGR levels are inflated and BOTH KEEP columns are flattered; the 4a bar (RULES v2 on the
same panel) carries the same bias, the 4b bar (SPY) does not.  Read every SMALL439 level
with that caveat.

Deterministic, standalone.  Reads research/baseline.py; writes only its own outputs.
Outputs: .grid.csv .walkforward.csv .the20.csv .keeppaths.csv .control.csv .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
RUNGS = [0, 10, 25]
PANELS = ["U56", "B136", "SMALL439"]
DEPTHS = [0.05, 0.10, 0.20, 0.30, 0.50]          # reported axis
GROSSES = [0.50, 0.75, 1.00]                     # reported axis
CADENCES = ["D", "W", "M", "Q"]                  # tuned param 1
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]          # tuned param 2
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# idea 563's (panel, theta) cells that produced its 20 MOM-D 4a passes
THE20_CELLS = [("B136", 0.00), ("B136", -0.06),
               ("SMALL439", 0.30), ("SMALL439", 0.20),
               ("SMALL439", 0.12), ("SMALL439", 0.06)]

IDEA563 = REPO / "research" / "backtests" / (
    "2026-09-11_is-the-MA-GATE-worse-than-MOMENTUM-at-matched-daily-depth-"
    "a-book-level-fact_cloud.grid.csv")

BAR_ENGINE, BAR_RUNG, BAR_REPRO = 1e-12, 1e-15, 1e-9

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


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def fast_run(px, W, freq):
    """engine.backtest's arithmetic, returning the ZERO-COST path + turnover so any cost
    rung is exactly derivable (gate G2)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series(np.nansum(held * rets, axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


def stat(r):
    h = len(r) // 2
    o = r.loc[OOS_START:]
    ho = len(o) // 2
    m, mo = metrics(r), metrics(o)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=metrics(r.loc[:IS_END])["CAGR"],
                isSharpe=metrics(r.loc[:IS_END])["Sharpe"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                oH1=metrics(o.iloc[:ho])["Sharpe"], oH2=metrics(o.iloc[ho:])["Sharpe"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def oos_4a_strict(s, b):
    return bool(s["oH1"] > b["oH1"] and s["oH2"] > b["oH2"] and s["oMaxDD"] >= b["oMaxDD"])


def oos_4a_lenient(s, b):
    return bool(s["oSharpe"] > b["oSharpe"] and s["oMaxDD"] >= b["oMaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def mom_rank(px):
    return (px.shift(21) / px.shift(252) - 1).where(live_mask(px))


def depth_slice(px, mom, live, q):
    """top ceil(q * rankable_t) names by 12-1 momentum, recomputed every day."""
    kt = np.ceil(q * mom.notna().sum(axis=1)).clip(lower=1)
    rk = mom.rank(axis=1, ascending=False, method="first")
    return rk.le(kt, axis=0).fillna(False) & live, kt


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def daily_matched(sig, live, gm):
    """idea 559/563's daily depth match: k_t = |MA gate|_t, clipped to the rankable count."""
    kt = np.minimum(gm.sum(axis=1), sig.notna().sum(axis=1))
    return sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def book(px, g, construction, gross):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def score_book(px, W, cad, start, years, live_s, spy_s, extra):
    r0, tn, gx = fast_run(px, W, cad)
    d = dict(extra)
    d.update(cadence=cad, turn_yr=float(tn.loc[start:].sum() / years),
             mean_gross=float(gx.loc[start:].mean()))
    for c in RUNGS:
        sc = stat(rung(r0, tn, c).loc[start:])
        if c == COST_BPS:
            d.update(sc)
            d["p4a"] = verdict_4a(sc, live_s)
            d["o4a_strict"] = oos_4a_strict(sc, live_s)
            d["o4a_lenient"] = oos_4a_lenient(sc, live_s)
            d["f4b"] = fail_4b(sc, spy_s)
        else:
            d[f"Sharpe_{c}"] = sc["Sharpe"]
            d[f"CAGR_{c}"] = sc["CAGR"]
            d[f"oSharpe_{c}"] = sc["oSharpe"]
    return d


# ================================================================== main
def main():
    P("=" * 190)
    P("IDEA 767 - is the 4a COLUMN where the MOMENTUM SLICE actually lives?    lane C, 2026-09-11")
    P("=" * 190)
    P("PROTOCOL: 10 bps per unit turnover (0 and 25 derived exactly), next-day execution, no")
    P(f"shorting, no leverage.  IS = start..{IS_END}, OOS = {OOS_START}..end, read ONCE.")
    P("2 tuned params: CADENCE {D,W,M,Q} x CONSTRUCTION {RESPREAD,DEGROSS}.  Panel, depth and")
    P("gross are REPORTED axes, never selected over.  Both KEEP paths on every book.")
    P("SURVIVORSHIP: B136/SMALL439 are current constituents only - CAGR inflated, the 4a bar")
    P("carries the same bias, the 4b (SPY) bar does not.")
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

    # ---------------------------------------------------------------- G0 / G2
    P("\n" + "=" * 190)
    P("G0  fast_run vs engine.backtest        G2  derived cost rung vs a fresh run at that rung")
    P("=" * 190)
    g0 = g2 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        for freq in ("D", "W"):
            a = backtest(px, W, cost_bps=COST_BPS, freq=freq)
            r0, tn, _ = fast_run(px, W, freq)
            g0 = max(g0, float((a["returns"] - rung(r0, tn, COST_BPS)).abs().max()),
                     float((a["turnover"] - tn).abs().max()))
            a25 = backtest(px, W, cost_bps=25, freq=freq)
            g2 = max(g2, float((a25["returns"] - rung(r0, tn, 25)).abs().max()))
        P(f"  {pn:9s} running max  G0 {g0:.3e}   G2 {g2:.3e}")
    P(f"  G0 {g0:.3e} (bar {BAR_ENGINE:.0e}) {'PASS' if g0 < BAR_ENGINE else 'FAIL'}    "
      f"G2 {g2:.3e} (bar {BAR_RUNG:.0e}) {'PASS' if g2 < BAR_RUNG else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- comparands
    COMP = {}
    P("\n" + "=" * 190)
    P("COMPARANDS (per panel, over the exact window every book on that panel is scored on)")
    P("=" * 190)
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        r0, tn, _ = fast_run(px, rules_v2_weights(px), "W")
        live_s = stat(rung(r0, tn, COST_BPS).loc[start:])
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        COMP[pn] = dict(live=live_s, spy=spy_s, start=start, years=years, px=px, spy_px=spy_px)
        P(f"  {pn:9s} {start.date()}..{px.index[-1].date()}  ({years:.2f} yrs, {px.shape[1]} names)")
        P(f"      RULES v2 (4a bar) CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f}  H1/H2 {live_s['H1']:.4f}/{live_s['H2']:.4f}   "
          f"OOS {live_s['oCAGR']:.4f}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f} "
          f"oH1/oH2 {live_s['oH1']:.4f}/{live_s['oH2']:.4f}")
        P(f"      SPY      (4b bar) CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f}  H1/H2 {spy_s['H1']:.4f}/{spy_s['H2']:.4f}   "
          f"OOS {spy_s['oCAGR']:.4f}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
        P(f"      4b bars: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} OOS>{spy_s['oSharpe']:.4f} "
          f"MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%} CAGR>={0.70*spy_s['CAGR']:.2%}")
    flush_log()

    # ---------------------------------------------------------------- LEG A
    P("\n" + "=" * 190)
    P("LEG A.  THE DIRECT RE-CUT - momentum slice on its OWN depth, no MA gate anywhere")
    P("         3 panels x 5 depths x 3 gross x 4 cadences x 2 constructions = 360 books")
    P("=" * 190)
    rows, g3 = [], 0.0
    for pn in PANELS:
        px = COMP[pn]["px"]
        start, years = COMP[pn]["start"], COMP[pn]["years"]
        live_s, spy_s = COMP[pn]["live"], COMP[pn]["spy"]
        live, mom = live_mask(px), mom_rank(px)
        for q in DEPTHS:
            gate, kt = depth_slice(px, mom, live, q)
            g3 = max(g3, float((gate.sum(axis=1).loc[start:] - kt.loc[start:]).abs().max()))
            for gr in GROSSES:
                for con in CONSTRUCTIONS:
                    W = book(px, gate, con, gr)
                    for cad in CADENCES:
                        rows.append(score_book(
                            px, W, cad, start, years, live_s, spy_s,
                            dict(panel=pn, depth=q, gross=gr, construction=con,
                                 n_held=float(gate.loc[start:].sum(axis=1).mean()))))
        P(f"  {pn}: {len(DEPTHS)*len(GROSSES)*len(CONSTRUCTIONS)*len(CADENCES)} books done")
        flush_log()
    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"  G3 depth identity |held - ceil(q*rankable)| max {g3:.3e} (bar 0) "
      f"{'PASS' if g3 == 0 else 'FAIL'}")

    P(f"\n  4a passes {int(G.p4a.sum())}/{len(G)}    4b passes {int(G.p4b.sum())}/{len(G)}    "
      f"BOTH {int((G.p4a & G.p4b).sum())}")
    P("\n  4a / 4b by construction x cadence (books = 45 per cell):")
    P(fmt(G.pivot_table(index="construction", columns="cadence", values=["p4a", "p4b"],
                        aggfunc="sum").fillna(0), 0))
    P("\n  4a / 4b by panel x construction:")
    P(fmt(G.groupby(["panel", "construction"]).agg(
        books=("p4a", "size"), p4a=("p4a", "sum"), p4b=("p4b", "sum"),
        mean_gross=("mean_gross", "mean"), CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"))))
    P("\n  4a by depth x gross (both constructions, all cadences, 24 books per cell):")
    P(fmt(G.pivot_table(index="depth", columns="gross", values="p4a", aggfunc="sum").fillna(0), 0))
    fb = G[~G.p4b].f4b.str.split(",").explode().value_counts()
    P("  binding 4b bars over the 4b failures: " + "  ".join(f"{k} {v}" for k, v in fb.items()))
    if G.p4a.any():
        P("\n  EVERY 4a PASSER on the direct re-cut:")
        P(fmt(G[G.p4a].sort_values("Sharpe", ascending=False)[
            ["panel", "depth", "gross", "construction", "cadence", "mean_gross", "n_held",
             "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
             "turn_yr", "p4b", "f4b"]]))
    flush_log()

    # ---------------------------------------------------------------- LEG B
    P("\n" + "=" * 190)
    P("LEG B.  RULE 8 on the direct re-cut - (cadence, construction) chosen on IS Sharpe ALONE,")
    P("         OOS 2017+ read ONCE, 4a re-scored out of sample")
    P("=" * 190)
    wf = []
    for (pn, q, gr), g in G.groupby(["panel", "depth", "gross"]):
        pick = g.loc[g.isSharpe.idxmax()]
        lv, sp = COMP[pn]["live"], COMP[pn]["spy"]
        wf.append(dict(panel=pn, depth=q, gross=gr, cadence=pick.cadence,
                       construction=pick.construction,
                       IS_spread=float(g.isSharpe.max() - g.isSharpe.min()),
                       isSharpe=pick.isSharpe, CAGR=pick.CAGR, Sharpe=pick.Sharpe,
                       MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2, oCAGR=pick.oCAGR,
                       oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD, oH1=pick.oH1, oH2=pick.oH2,
                       mean_gross=pick.mean_gross, turn_yr=pick.turn_yr,
                       base_oSharpe=lv["oSharpe"], base_oMaxDD=lv["oMaxDD"],
                       base_oCAGR=lv["oCAGR"], spy_oSharpe=sp["oSharpe"],
                       spy_oCAGR=sp["oCAGR"], spy_oMaxDD=sp["oMaxDD"],
                       full_p4a=bool(pick.p4a), full_p4b=bool(pick.p4b),
                       o4a_strict=bool(pick.o4a_strict), o4a_lenient=bool(pick.o4a_lenient),
                       beat_base=bool(pick.oSharpe > lv["oSharpe"]),
                       beat_spy=bool(pick.oSharpe > sp["oSharpe"]), f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  {len(WF)} picks (3 panels x 5 depths x 3 gross).  Dial the IS selector chose:")
    P(fmt(WF.pivot_table(index="construction", columns="cadence", values="depth",
                         aggfunc="size").fillna(0).astype(int), 0))
    P(f"\n  picks beating RULES v2 OOS Sharpe: {int(WF.beat_base.sum())}/{len(WF)}    "
      f"beating SPY OOS: {int(WF.beat_spy.sum())}/{len(WF)}")
    P(f"  picks passing OOS-4a STRICT {int(WF.o4a_strict.sum())}/{len(WF)}    "
      f"LENIENT {int(WF.o4a_lenient.sum())}/{len(WF)}    "
      f"full-sample 4a {int(WF.full_p4a.sum())}/{len(WF)}    4b {int(WF.full_p4b.sum())}/{len(WF)}")
    P("\n  by panel:")
    P(fmt(WF.groupby("panel").agg(
        n=("oSharpe", "size"), oCAGR=("oCAGR", "mean"), oSharpe=("oSharpe", "mean"),
        oMaxDD=("oMaxDD", "mean"), beat_base=("beat_base", "mean"),
        beat_spy=("beat_spy", "mean"), o4a_s=("o4a_strict", "sum"),
        o4a_l=("o4a_lenient", "sum"), p4b=("full_p4b", "sum"))))
    P("\n  EVERY PICK:")
    P(fmt(WF[["panel", "depth", "gross", "cadence", "construction", "mean_gross", "CAGR",
              "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "base_oSharpe",
              "spy_oSharpe", "turn_yr", "full_p4a", "o4a_strict", "o4a_lenient", "f4b"]]))
    flush_log()

    # ---------------------------------------------------------------- LEG C
    P("\n" + "=" * 190)
    P("LEG C.  THE 20 THEMSELVES - idea 563's MOM-D 4a passers rebuilt and put through rule 8")
    P("=" * 190)
    c_rows = []
    for pn, th in THE20_CELLS:
        px = COMP[pn]["px"]
        start, years = COMP[pn]["start"], COMP[pn]["years"]
        live_s, spy_s = COMP[pn]["live"], COMP[pn]["spy"]
        live, mom = live_mask(px), mom_rank(px)
        gm = ma_gate(px, th)
        gate = daily_matched(mom, live, gm)
        for gr in GROSSES:
            for con in CONSTRUCTIONS:
                W = book(px, gate, con, gr)
                for cad in CADENCES:
                    c_rows.append(score_book(
                        px, W, cad, start, years, live_s, spy_s,
                        dict(panel=pn, theta=th, gross=gr, construction=con, arm="MOM-D",
                             n_held=float(gate.loc[start:].sum(axis=1).mean()))))
        P(f"  {pn} theta {th:+.2f}: {len(GROSSES)*len(CONSTRUCTIONS)*len(CADENCES)} books done")
        flush_log()
    C = pd.DataFrame(c_rows)
    C["p4b"] = C.f4b == "-"
    C.to_csv(f"{OUT}.the20.csv", index=False)

    # G1 reproduction against idea 563's committed grid
    if IDEA563.exists():
        ref = pd.read_csv(IDEA563)
        ref = ref[(ref.arm == "MOM-D")]
        k = ["panel", "theta", "construction", "cadence", "gross"]
        m = C.merge(ref, on=k, suffixes=("", "_ref"))
        cols = ["Sharpe", "MaxDD", "H1", "H2", "oSharpe", "CAGR"]
        dd = {c: float((m[c] - m[f"{c}_ref"]).abs().max()) for c in cols}
        g1 = max(dd.values())
        P(f"\n  G1 reproduction of idea 563's committed MOM-D grid on {len(m)} matched books: "
          f"max {g1:.3e} (bar {BAR_REPRO:.0e})  {'PASS' if g1 < BAR_REPRO else 'FAIL'}")
        P("     per column: " + "  ".join(f"{c} {v:.3e}" for c, v in dd.items()))
        P("     per panel:  " + "  ".join(
            f"{p} {float(max((m[m.panel == p][c] - m[m.panel == p][f'{c}_ref']).abs().max() for c in cols)):.3e}"
            for p in m.panel.unique()))
        ref4a = ref[ref.p4a & ref.construction.isin(CONSTRUCTIONS)]
        P(f"     idea 563's MOM-D 4a passers inside these cells: {int(ref4a.p4a.sum())} "
          f"(the 20 are all DEGROSS; this rebuild re-scores {int(C.p4a.sum())} 4a passes here)")
    else:
        g1 = np.nan
        P("\n  G1 SKIPPED - idea 563 .grid.csv not on disk")

    P(f"\n  Rebuilt 4a passes in leg C: {int(C.p4a.sum())}/{len(C)}   "
      f"4b {int(C.p4b.sum())}/{len(C)}   BOTH {int((C.p4a & C.p4b).sum())}")
    the20 = C[C.p4a & (C.construction == "DEGROSS")].copy()
    P(f"  THE 20 (DEGROSS 4a passers rebuilt here): {len(the20)}")
    P(fmt(the20[["panel", "theta", "gross", "cadence", "mean_gross", "n_held", "CAGR",
                 "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
                 "o4a_strict", "o4a_lenient", "turn_yr", "f4b"]]))

    # the rule-8 selector inside each (panel, theta, gross) cell
    P("\n  RULE 8 INSIDE EACH CELL - (cadence, construction) on IS Sharpe alone, OOS read once:")
    picks = []
    for (pn, th, gr), g in C.groupby(["panel", "theta", "gross"]):
        pk = g.loc[g.isSharpe.idxmax()]
        lv, sp = COMP[pn]["live"], COMP[pn]["spy"]
        n4a = int(g[g.construction == "DEGROSS"].p4a.sum())
        picks.append(dict(panel=pn, theta=th, gross=gr, pick_cadence=pk.cadence,
                          pick_construction=pk.construction, isSharpe=pk.isSharpe,
                          n_4a_in_cell=n4a, pick_is_a_4a_book=bool(pk.p4a),
                          CAGR=pk.CAGR, Sharpe=pk.Sharpe, MaxDD=pk.MaxDD,
                          oCAGR=pk.oCAGR, oSharpe=pk.oSharpe, oMaxDD=pk.oMaxDD,
                          mean_gross=pk.mean_gross, turn_yr=pk.turn_yr,
                          base_oSharpe=lv["oSharpe"], base_oMaxDD=lv["oMaxDD"],
                          spy_oSharpe=sp["oSharpe"],
                          o4a_strict=bool(pk.o4a_strict), o4a_lenient=bool(pk.o4a_lenient),
                          p4b=bool(pk.p4b), f4b=pk.f4b))
    PK = pd.DataFrame(picks)
    PK.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(fmt(PK[["panel", "theta", "gross", "pick_cadence", "pick_construction", "n_4a_in_cell",
              "pick_is_a_4a_book", "mean_gross", "CAGR", "Sharpe", "MaxDD", "oCAGR",
              "oSharpe", "base_oSharpe", "spy_oSharpe", "oMaxDD", "o4a_strict",
              "o4a_lenient", "p4b"]]))
    P(f"\n  of the {len(PK)} cells that contain a 4a pass, the IS selector lands on a "
      f"4a-passing book in {int(PK.pick_is_a_4a_book.sum())}")
    P(f"  picks passing OOS-4a STRICT {int(PK.o4a_strict.sum())}/{len(PK)}   "
      f"LENIENT {int(PK.o4a_lenient.sum())}/{len(PK)}   4b {int(PK.p4b.sum())}/{len(PK)}")

    # the survival question, asked of the 20 directly
    surv = the20[["panel", "theta", "gross", "cadence", "o4a_strict", "o4a_lenient"]].copy()
    P(f"\n  DOES ANY OF THE 20 SURVIVE RULE 8?")
    P(f"    (i)  as its own book read out of sample: OOS-4a STRICT "
      f"{int(the20.o4a_strict.sum())}/{len(the20)}   LENIENT "
      f"{int(the20.o4a_lenient.sum())}/{len(the20)}")
    chosen = 0
    for _, r in the20.iterrows():
        row = PK[(PK.panel == r.panel) & (PK.theta == r.theta) & (PK.gross == r.gross)]
        if len(row) and row.iloc[0].pick_cadence == r.cadence and \
                row.iloc[0].pick_construction == r.construction:
            chosen += 1
    P(f"    (ii) reachable at all - the (cadence, construction) an IS selector would have "
      f"picked in its own cell equals the 4a-passing dial in {chosen}/{len(the20)}")
    P(f"    (iii) BOTH (picked AND passes OOS-4a): "
      f"{int(sum(1 for _, r in the20.iterrows() if r.o4a_strict and any((PK.panel == r.panel) & (PK.theta == r.theta) & (PK.gross == r.gross) & (PK.pick_cadence == r.cadence) & (PK.pick_construction == r.construction))))}")
    flush_log()

    # ---------------------------------------------------------------- LEG D
    P("\n" + "=" * 190)
    P("LEG D.  GROSS-MATCHED CONTROL - SPY held at each 4a passer's OWN realised mean gross,")
    P("         remainder in cash, rebalanced at the same cadence, same 10 bps")
    P("=" * 190)
    ctrl = []
    allpass = pd.concat([G[G.p4a].assign(leg="A", theta=np.nan),
                         C[C.p4a].assign(leg="C", depth=np.nan)], ignore_index=True, sort=False)
    for pn, sub in allpass.groupby("panel"):
        spy_px = COMP[pn]["spy_px"]
        start = COMP[pn]["start"]
        spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
        for _, r in sub.iterrows():
            gmatch = float(r.mean_gross)
            cr = spy_r * gmatch                      # static cash blend at the SAME mean gross
            sc = stat(cr)
            lv = COMP[pn]["live"]
            ctrl.append(dict(leg=r.leg, panel=pn, depth=r.get("depth", np.nan),
                             theta=r.get("theta", np.nan), gross=r.gross,
                             construction=r.construction, cadence=r.cadence,
                             mean_gross=gmatch, book_CAGR=r.CAGR, book_Sharpe=r.Sharpe,
                             book_MaxDD=r.MaxDD, book_oSharpe=r.oSharpe,
                             ctrl_CAGR=sc["CAGR"], ctrl_Sharpe=sc["Sharpe"],
                             ctrl_MaxDD=sc["MaxDD"], ctrl_oSharpe=sc["oSharpe"],
                             book_beats_ctrl_Sharpe=bool(r.Sharpe > sc["Sharpe"]),
                             book_beats_ctrl_CAGR=bool(r.CAGR > sc["CAGR"]),
                             ctrl_passes_4a=verdict_4a(sc, lv)))
    CT = pd.DataFrame(ctrl)
    CT.to_csv(f"{OUT}.control.csv", index=False)
    if len(CT):
        P(f"  {len(CT)} 4a passers scored against their own gross-matched SPY blend:")
        P(fmt(CT.groupby(["leg", "panel"]).agg(
            n=("mean_gross", "size"), mean_gross=("mean_gross", "mean"),
            book_Sharpe=("book_Sharpe", "mean"), ctrl_Sharpe=("ctrl_Sharpe", "mean"),
            book_CAGR=("book_CAGR", "mean"), ctrl_CAGR=("ctrl_CAGR", "mean"),
            book_MaxDD=("book_MaxDD", "mean"), ctrl_MaxDD=("ctrl_MaxDD", "mean"),
            beats_Sharpe=("book_beats_ctrl_Sharpe", "sum"),
            beats_CAGR=("book_beats_ctrl_CAGR", "sum"),
            ctrl_4a=("ctrl_passes_4a", "sum"))))
        P(f"\n  the 4a passers that beat a gross-matched index on Sharpe: "
          f"{int(CT.book_beats_ctrl_Sharpe.sum())}/{len(CT)}    on CAGR: "
          f"{int(CT.book_beats_ctrl_CAGR.sum())}/{len(CT)}")
        P(f"  the trivial control itself passes 4a in {int(CT.ctrl_passes_4a.sum())}/{len(CT)} "
          f"of the same comparisons")
    else:
        P("  no 4a passers to control")
    P("\n" + "=" * 190)
    P(f"GATES: G0 {g0:.3e}  G1 {g1:.3e}  G2 {g2:.3e}  G3 {g3:.3e}")
    P("=" * 190)
    flush_log()


if __name__ == "__main__":
    main()
