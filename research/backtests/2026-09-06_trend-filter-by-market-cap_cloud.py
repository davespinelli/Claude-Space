#!/usr/bin/env python3
"""Idea 51 - "trend-filter-by-market-cap" (cloud, 2026-09-06).

The question
------------
Idea 49 found the RULES v1 eligibility filter (200d MA + vol20 < 0.60) DESTROYS 5.4 pp/yr of
CAGR at 0 bps on the 439-name sub-$2B panel -- equal-weighting all 439 names with no filter
returns 10.2%/0.677/-36.2% while the all-eligible book at the SAME 75% gross returns 3.5% -- yet
the same filter is essentially the whole edge on universe.json.

QUEUE wording: "Isolate the filter alone (EW-all-eligible vs EW-all-names, no ranking, same
gross) on all three universes and, if a cap column can be built, by cap decile within the small
panel.  Where does trend-following stop working, and does that boundary belong in RULES as a
universe clause?"

Design
-------
FILT   equal weight across the names the gate admits, GROSS/k each   <- "same gross" (RESPREAD)
CTRL   equal weight across every live name, GROSS/n each             <- the no-filter control
DEGROSS  the live RULES v2 form (gated weight goes to cash, GROSS/n_live each) is reported
         alongside so the exposure channel idea 290 isolated is visible, not hidden.

The gate is decomposed into its two legs, because idea 49 only ever ran them together:
    MA      px > rolling(lb).mean()
    VOL     vol20 < 0.60
    MAVOL   both  (= RULES v1's eligibility filter, and idea 49's f=1.00 book)

Panels: U56 (universe.json), B136 (universe_broad.json), SMALL439 (sub-$2B, the 44 names with
max_1d_move >= 1.0 dropped).

Size, within SMALL439, on two proxies -- deliberately one of each kind:
    CAP   research/deepvalue/universe_under2b.csv `mktcap`, decile-sorted, membership FIXED.
          NOT point-in-time: it is TODAY's capitalisation, so the decile label peeks.  It is a
          LABELLING for reading the cross-section, never a tradable rule.
    ADV   60-day median dollar volume (close x share volume), ranked cross-sectionally EVERY
          day.  Genuinely point-in-time and tradable; this is the proxy any RULES clause would
          have to use.

Pre-registered hypotheses (bars fixed before any number was read)
------------------------------------------------------------------
H1  REPLICATION.  On SMALL439, gate MAVOL / lb 200 / weekly / RESPREAD against CTRL reproduces
    idea 49's gap to within 0.5 pp: -5.4 pp/yr at 0 bps and -6.6 pp/yr at 10 bps, on idea 49's
    own window (px.index[260]).  FAILS if either misses by more than 0.5 pp.
H2  SIGN FLIP ACROSS PANELS.  dSharpe(FILT - CTRL, RESPREAD, MAVOL, lb 200) > 0 on U56 AND B136
    at ALL THREE cadences, and < 0 on SMALL439 at all three.  6/6 and 3/3 required.
H3  MONOTONE IN SIZE.  Within SMALL439, Spearman(size decile, dSharpe) > 0 with |t| >= 2 on
    BOTH proxies (MAVOL, RESPREAD, weekly, lb 200).
H4  THE BOUNDARY.  There is a lowest decile at which dSharpe > 0 in BOTH halves AND out of
    sample, on both proxies, and the two proxies agree to within 2 deciles.  This is the number
    a RULES universe clause would have to quote.
H5  WHICH LEG.  The MA leg carries the small-cap damage, not the vol leg: on SMALL439 at 0 bps,
    dCAGR(MA-only) < dCAGR(VOL-only).

Tuned parameters (PROTOCOL rule 4: at most two)
------------------------------------------------
    cadence   {W, M, Q}
    lookback  {100, 200, 300}   (the MA leg's window)
Reported at EVERY value, selected at none except inside the rule-8 walk-forward.  Panel, gate
leg, construction and size decile are REPORTED dimensions, not tuned - the contrast across them
IS the question.

Windows
--------
The lookback dial needs a common warm-up, so the sweep is evaluated from px.index[360] on every
panel (300d MA fully formed plus 60 days).  H1's replication block is run on idea 49's own
px.index[260] window with lb = 200, so the anchor is exact.  IS <= 2016-12-31, OOS 2017+.

Grid
-----
Sweep: 3 panels x 2 constructions x 3 cadences x (MA x 3 lb + MAVOL x 3 lb + VOL) = 126 books,
each at 10 and 0 bps, plus 9 controls x 2 rungs.  Size: SMALL439 weekly lb 200, 2 proxies x 10
deciles x 2 gates x 2 constructions = 80 books plus 20 controls, each at both rungs.  Every cell
printed and written to CSV.

Walk-forward (PROTOCOL rule 8)
-------------------------------
(cadence, lookback) chosen on IS Sharpe inside each of the 18 (panel x gate x construction)
arms; 2017-2026 read once.  OOS CAGR/Sharpe/MaxDD against the live RULES v2 book, SPY and the
matched no-filter control.  Both KEEP paths evaluated on every cell.

SURVIVORSHIP: all three panels are CURRENT constituents.  data/prices_small.csv is a screen of
today's sub-$2B names - no delistings, no takeovers, no bankruptcies - so its levels are biased
UP and its cross-section is biased towards names that survived.  The headline here is a
FILT-minus-CTRL contrast on the SAME names and days, so the bias very largely cancels out of the
dSharpe/dCAGR columns; it does NOT cancel out of the 4a/4b columns, which are levels, nor out of
the CAP decile sort, whose labels are today's caps.  A KILL of the filter on this panel is
strengthened by the bias (the missing names are the ones a trend filter would have exited).

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, load_volume, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
GROSS = 0.75
MAX_VOL = 0.60
CADENCES = ["W", "M", "Q"]
LOOKBACKS = [100, 200, 300]
GATES = ["MA", "VOL", "MAVOL"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
PANELS = ["SMALL439", "U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SWEEP_IDX = 360          # common warm-up for lb up to 300
REPLI_IDX = 260          # idea 49's own window
ADV_WIN = 60             # days in the dollar-volume median
NDEC = 10
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

# pre-registered bars
H1_TOL_PP = 0.5
H3_MIN_T = 2.0

pd.set_option("display.width", 280)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 700)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


def spearman(x, y):
    x = pd.Series(np.asarray(x, float)).rank()
    y = pd.Series(np.asarray(y, float)).rank()
    n = len(x)
    rho = float(np.corrcoef(x, y)[0, 1])
    t = rho * math.sqrt((n - 2) / max(1e-12, 1 - rho ** 2)) if n > 2 else np.nan
    return rho, t


# ---------------------------------------------------------------- panels
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "SMALL439": (pxs[inv], pxs["SPY"]),
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
    }
    P(f"panels: SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0), U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, gate, lb):
    live = live_mask(px)
    if gate == "VOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (vol20 < MAX_VOL) & live
    above = px > px.rolling(lb).mean()
    if gate == "MA":
        return above & live
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return above & (vol20 < MAX_VOL) & live


def filt_book(px, gate, lb, con, member=None):
    """FILT: equal weight across admitted names.  RESPREAD holds GROSS/k (same gross as CTRL);
    DEGROSS holds GROSS/n_live and lets the gated-out weight fall to cash."""
    g = gate_mask(px, gate, lb)
    live = live_mask(px)
    if member is not None:
        g, live = g & member, live & member
    if con == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live.sum(axis=1).clip(lower=1)
    return (g & live).astype(float).div(n, axis=0) * GROSS


def ctrl_book(px, member=None):
    live = live_mask(px)
    if member is not None:
        live = live & member
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


def stat(r):
    m = metrics(r)
    h = len(r) // 2
    h1, h2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def run(px, w, cad, st):
    r10 = backtest(px, w, cost_bps=COST_BPS, freq=cad)
    r0 = backtest(px, w, cost_bps=0, freq=cad)
    return r10["returns"].loc[st:], r0["returns"].loc[st:], r10, st


# ---------------------------------------------------------------- main
def main():
    PX = panels()
    starts = {k: v[0].index[SWEEP_IDX] for k, v in PX.items()}
    P("=" * 180)
    P(f"Idea 51 trend-filter-by-market-cap (cloud) | {SCRIPT}")
    P("=" * 180)
    for k in PANELS:
        px = PX[k][0]
        P(f"  {k}: {px.index[0].date()} .. {px.index[-1].date()}; sweep evaluated from "
          f"{starts[k].date()} ({len(px.loc[starts[k]:]) / 252:.2f} yrs, {px.shape[1]} names)")
    P(f"Costs {COST_BPS} bps (and a 0-bps rung), gross {GROSS}, next-day execution, no shorting, "
      f"no leverage.  IS <= {IS_END}, OOS {OOS_START}.. .")
    P(f"Tuned: cadence {CADENCES} x MA lookback {LOOKBACKS}.  Reported: panel, gate leg "
      f"{GATES}, construction {CONSTRUCTIONS}, size decile.")
    P(f"Pre-registered bars: H1 idea-49 gap reproduced to {H1_TOL_PP} pp at both rungs; "
      f"H2 dSharpe>0 on U56 AND B136 at 3/3 cadences and <0 on SMALL439 at 3/3; "
      f"H3 Spearman(decile,dSharpe)>0 with |t|>={H3_MIN_T} on BOTH proxies; "
      f"H4 a boundary decile exists on both proxies and they agree within 2; "
      f"H5 dCAGR(MA-only) < dCAGR(VOL-only) on SMALL439 at 0 bps.")
    for k in PANELS:
        y = PX[k][0].index.to_series().groupby(PX[k][0].index.year).count()
        if y.loc[2013:2024].max() > 300:
            P(f"!! {k} has a CALENDAR-DAY index - aborting."); sys.exit(1)
    P("Index sanity: all three panels ~252 rows/yr (trading-day index confirmed).")

    # ---------------- H1 replication, idea 49's own window ----------------
    P("\n" + "-" * 180)
    P("H1 - REPLICATION OF IDEA 49's FILTER GAP (SMALL439, MAVOL, lb 200, weekly, RESPREAD, "
      "idea 49's px.index[260] window)")
    P("-" * 180)
    pxs = PX["SMALL439"][0]
    st49 = pxs.index[REPLI_IDX]
    f10, f0, _, _ = run(pxs, filt_book(pxs, "MAVOL", 200, "RESPREAD"), "W", st49)
    c10, c0, _, _ = run(pxs, ctrl_book(pxs), "W", st49)
    g10 = 100 * (metrics(f10)["CAGR"] - metrics(c10)["CAGR"])
    g0 = 100 * (metrics(f0)["CAGR"] - metrics(c0)["CAGR"])
    P(f"  FILT f=1.00  10 bps CAGR {metrics(f10)['CAGR']:.2%} (idea 49 published 3.5%), "
      f"0 bps {metrics(f0)['CAGR']:.2%}")
    P(f"  CTRL EWall   10 bps CAGR {metrics(c10)['CAGR']:.2%} (idea 49 published 10.2%), "
      f"Sharpe {metrics(c10)['Sharpe']:.4f} (0.677), MaxDD {metrics(c10)['MaxDD']:.2%} (-36.2%), "
      f"0 bps {metrics(c0)['CAGR']:.2%}")
    P(f"  gap 10 bps {g10:+.2f} pp/yr (idea 49: -6.6), gap 0 bps {g0:+.2f} pp/yr (idea 49: -5.4)")
    h1 = bool(abs(g0 + 5.4) <= H1_TOL_PP and abs(g10 + 6.6) <= H1_TOL_PP)
    P(f"H1 -> {'HOLDS' if h1 else 'FAILS'} (bar {H1_TOL_PP} pp on both rungs)")

    # ---------------- reference books -------------------------------------
    P("\n" + "-" * 180)
    P("REFERENCE BOOKS on the sweep window (10 bps)")
    P("-" * 180)
    ctrl, ctrl0, spy_stat = {}, {}, {}
    for k in PANELS:
        px, spy = PX[k]
        st = starts[k]
        for cad in CADENCES:
            r10, r0, _, _ = run(px, ctrl_book(px), cad, st)
            ctrl[(k, cad)] = stat(r10)
            ctrl0[(k, cad)] = metrics(r0)["CAGR"]
        spy_stat[k] = stat(spy.pct_change().fillna(0.0).loc[st:])
    px_u = load_universe()
    live_ret = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]
    live_s = stat(live_ret.loc[starts["U56"]:])
    ref = {f"CTRL EWall {k} {c} (no filter)": ctrl[(k, c)] for k in PANELS for c in CADENCES}
    ref["RULES v2 on universe.json (LIVE BOOK, 4a comparand)"] = live_s
    for k in PANELS:
        ref[f"SPY on {k} window (4b comparand)"] = spy_stat[k]
    P(fmt(pd.DataFrame(ref).T))

    # ---------------- the sweep -------------------------------------------
    P("\n" + "-" * 180)
    P("SWEEP - the filter alone, every cell (panel x construction x cadence x gate leg x lookback)")
    P("-" * 180)
    rows = []
    for k in PANELS:
        px, _ = PX[k]
        st = starts[k]
        years = len(px.loc[st:]) / 252
        for con in CONSTRUCTIONS:
            for cad in CADENCES:
                for gate in GATES:
                    for lb in (LOOKBACKS if gate != "VOL" else [200]):
                        w = filt_book(px, gate, lb, con)
                        r10, r0, res, _ = run(px, w, cad, st)
                        s = stat(r10)
                        rows.append(dict(panel=k, con=con, cad=cad, gate=gate, lb=lb, **s,
                                         CAGR0=metrics(r0)["CAGR"],
                                         gross_mean=float(res["weights"].loc[st:].sum(axis=1).mean()),
                                         turn_yr=res["turnover"].loc[st:].sum() / years,
                                         dCAGR=s["CAGR"] - ctrl[(k, cad)]["CAGR"],
                                         dCAGR0_pp=100 * (metrics(r0)["CAGR"] - ctrl0[(k, cad)]),
                                         dSharpe=s["Sharpe"] - ctrl[(k, cad)]["Sharpe"],
                                         dSharpe_H1=s["H1"] - ctrl[(k, cad)]["H1"],
                                         dSharpe_H2=s["H2"] - ctrl[(k, cad)]["H2"],
                                         dSharpe_OOS=s["oSharpe"] - ctrl[(k, cad)]["oSharpe"],
                                         p4a=verdict_4a(s, live_s),
                                         f4b=fail_4b(s, spy_stat[k])))
        P(f"  ... {k} swept")
    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    G.to_csv(f"{OUT}.sweep.csv", index=False)
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "gross_mean", "turn_yr",
            "dCAGR", "dCAGR0_pp", "dSharpe", "dSharpe_H1", "dSharpe_H2", "dSharpe_OOS", "p4a", "f4b"]
    for k in PANELS:
        for con in CONSTRUCTIONS:
            P(f"\n--- {k} / {con} (delta columns are FILT minus the matched EWall control) ---")
            P(fmt(G[(G.panel == k) & (G.con == con)].set_index(["cad", "gate", "lb"])[cols]))

    # ---------------- H2 / H5 ---------------------------------------------
    P("\n" + "-" * 180)
    P("H2 - DOES THE FILTER'S SIGN FLIP BETWEEN THE LARGE-CAP PANELS AND THE SUB-$2B PANEL?")
    P("-" * 180)
    core = G[(G.gate == "MAVOL") & (G.lb == 200) & (G.con == "RESPREAD")]
    P(fmt(core.set_index(["panel", "cad"])[["CAGR", "Sharpe", "dCAGR", "dCAGR0_pp", "dSharpe",
                                            "dSharpe_H1", "dSharpe_H2", "dSharpe_OOS"]]))
    pos = {k: int((core[core.panel == k].dSharpe > 0).sum()) for k in PANELS}
    h2 = bool(pos["U56"] == 3 and pos["B136"] == 3 and pos["SMALL439"] == 0)
    P(f"\ndSharpe > 0 at: U56 {pos['U56']}/3, B136 {pos['B136']}/3, SMALL439 {pos['SMALL439']}/3 "
      f"-> H2 {'HOLDS' if h2 else 'FAILS'}")
    P("\nSame table under the DEGROSS construction (the live RULES form; the gap now mixes "
      "selection with exposure):")
    P(fmt(G[(G.gate == "MAVOL") & (G.lb == 200) & (G.con == "DEGROSS")]
          .set_index(["panel", "cad"])[["CAGR", "Sharpe", "gross_mean", "dCAGR", "dCAGR0_pp",
                                        "dSharpe", "dSharpe_OOS"]]))

    P("\n" + "-" * 180)
    P("H5 - WHICH LEG OF THE FILTER DOES THE DAMAGE?  (dCAGR at 0 bps, pp/yr, RESPREAD)")
    P("-" * 180)
    legs = G[(G.con == "RESPREAD") & ((G.gate == "VOL") | (G.lb == 200))]
    P(fmt(legs.pivot_table(index=["panel", "cad"], columns="gate", values="dCAGR0_pp")))
    ma_s = float(G[(G.panel == "SMALL439") & (G.con == "RESPREAD") & (G.gate == "MA")
                   & (G.lb == 200)].dCAGR0_pp.mean())
    vol_s = float(G[(G.panel == "SMALL439") & (G.con == "RESPREAD") & (G.gate == "VOL")].dCAGR0_pp.mean())
    h5 = bool(ma_s < vol_s)
    P(f"SMALL439 mean over cadences: MA-only {ma_s:+.3f} pp/yr, VOL-only {vol_s:+.3f} pp/yr "
      f"-> H5 {'HOLDS' if h5 else 'FAILS'}")

    # ---------------- the size cross-section ------------------------------
    P("\n" + "-" * 180)
    P("SIZE CROSS-SECTION within SMALL439 (weekly, lb 200; deltas are FILT minus the SAME "
      "decile's own EWall control)")
    P("-" * 180)
    px = PX["SMALL439"][0]
    st = starts["SMALL439"]
    cap = pd.read_csv(REPO / "research" / "deepvalue" / "universe_under2b.csv")[["ticker", "mktcap"]]
    cap = cap.dropna().drop_duplicates("ticker").set_index("ticker").mktcap
    have = [c for c in px.columns if c in cap.index]
    P(f"  CAP proxy: mktcap for {len(have)} of {px.shape[1]} panel names "
      f"(median ${cap[have].median()/1e6:.0f}m, range ${cap[have].min()/1e6:.0f}m .. "
      f"${cap[have].max()/1e6:.0f}m).  TODAY's cap - the decile label is NOT point-in-time.")
    capdec = pd.qcut(cap[have].rank(method="first"), NDEC, labels=False) + 1

    vol = load_volume(small=True).reindex(px.index).ffill()
    dv = (px * vol.reindex(columns=px.columns)).rolling(ADV_WIN).median()
    advrank = dv.rank(axis=1, pct=True)
    P(f"  ADV proxy: {ADV_WIN}d median dollar volume, ranked cross-sectionally daily; "
      f"coverage {float(dv.loc[st:].notna().mean().mean()):.1%} of panel cells.  Point-in-time.")

    srows = []
    for d in range(1, NDEC + 1):
        # CAP: fixed membership, run on the sub-panel
        cols = [c for c in have if capdec[c] == d]
        sub = px[cols]
        c10, c0, _, _ = run(sub, ctrl_book(sub), "W", st)
        cs, cs0 = stat(c10), metrics(c0)["CAGR"]
        for gate in ("MA", "MAVOL"):
            for con in CONSTRUCTIONS:
                r10, r0, res, _ = run(sub, filt_book(sub, gate, 200, con), "W", st)
                s = stat(r10)
                srows.append(dict(proxy="CAP", dec=d, n=len(cols), gate=gate, con=con, **s,
                                  ctrl_CAGR=cs["CAGR"], ctrl_Sharpe=cs["Sharpe"],
                                  dCAGR=s["CAGR"] - cs["CAGR"],
                                  dCAGR0_pp=100 * (metrics(r0)["CAGR"] - cs0),
                                  dSharpe=s["Sharpe"] - cs["Sharpe"],
                                  dSharpe_H1=s["H1"] - cs["H1"], dSharpe_H2=s["H2"] - cs["H2"],
                                  dSharpe_OOS=s["oSharpe"] - cs["oSharpe"],
                                  p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_stat["SMALL439"])))
        # ADV: point-in-time membership, run on the full panel with a member mask
        mem = (advrank > (d - 1) / NDEC) & (advrank <= d / NDEC)
        c10, c0, _, _ = run(px, ctrl_book(px, mem), "W", st)
        cs, cs0 = stat(c10), metrics(c0)["CAGR"]
        for gate in ("MA", "MAVOL"):
            for con in CONSTRUCTIONS:
                r10, r0, res, _ = run(px, filt_book(px, gate, 200, con, mem), "W", st)
                s = stat(r10)
                srows.append(dict(proxy="ADV", dec=d, n=int(mem.loc[st:].sum(axis=1).mean()),
                                  gate=gate, con=con, **s,
                                  ctrl_CAGR=cs["CAGR"], ctrl_Sharpe=cs["Sharpe"],
                                  dCAGR=s["CAGR"] - cs["CAGR"],
                                  dCAGR0_pp=100 * (metrics(r0)["CAGR"] - cs0),
                                  dSharpe=s["Sharpe"] - cs["Sharpe"],
                                  dSharpe_H1=s["H1"] - cs["H1"], dSharpe_H2=s["H2"] - cs["H2"],
                                  dSharpe_OOS=s["oSharpe"] - cs["oSharpe"],
                                  p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_stat["SMALL439"])))
        P(f"  ... decile {d} done")
    S = pd.DataFrame(srows)
    S["p4b"] = S.f4b == "-"
    S.to_csv(f"{OUT}.deciles.csv", index=False)
    scols = ["n", "CAGR", "Sharpe", "MaxDD", "ctrl_CAGR", "ctrl_Sharpe", "dCAGR", "dCAGR0_pp",
             "dSharpe", "dSharpe_H1", "dSharpe_H2", "dSharpe_OOS", "p4a", "f4b"]
    for proxy in ("CAP", "ADV"):
        for con in CONSTRUCTIONS:
            P(f"\n--- SMALL439 size deciles ({proxy} proxy, {con}; decile 1 = smallest) ---")
            P(fmt(S[(S.proxy == proxy) & (S.con == con)].set_index(["gate", "dec"])[scols]))

    # ---------------- H3 / H4 ---------------------------------------------
    P("\n" + "-" * 180)
    P("H3 - IS THE FILTER'S VALUE MONOTONE IN SIZE?  (MAVOL, RESPREAD, weekly, lb 200)")
    P("-" * 180)
    h3rows, h3hits = [], {}
    for proxy in ("CAP", "ADV"):
        sub = S[(S.proxy == proxy) & (S.gate == "MAVOL") & (S.con == "RESPREAD")].sort_values("dec")
        rho, t = spearman(sub.dec, sub.dSharpe)
        rho_c, t_c = spearman(sub.dec, sub.dCAGR0_pp)
        h3hits[proxy] = bool(rho > 0 and abs(t) >= H3_MIN_T)
        h3rows.append(dict(proxy=proxy, rho_dSharpe=rho, t_dSharpe=t,
                           rho_dCAGR0=rho_c, t_dCAGR0=t_c,
                           dSharpe_dec1=float(sub.dSharpe.iloc[0]),
                           dSharpe_dec10=float(sub.dSharpe.iloc[-1]),
                           n_positive=int((sub.dSharpe > 0).sum())))
    H3 = pd.DataFrame(h3rows)
    P(fmt(H3.set_index("proxy")))
    h3 = all(h3hits.values())
    P(f"H3 -> {'HOLDS' if h3 else 'FAILS'} (CAP {h3hits['CAP']}, ADV {h3hits['ADV']})")

    P("\n" + "-" * 180)
    P("H4 - WHERE DOES TREND-FOLLOWING START WORKING?  lowest decile with dSharpe > 0 in BOTH "
      "halves AND out of sample")
    P("-" * 180)
    bnd = {}
    for proxy in ("CAP", "ADV"):
        sub = S[(S.proxy == proxy) & (S.gate == "MAVOL") & (S.con == "RESPREAD")].sort_values("dec")
        ok = sub[(sub.dSharpe_H1 > 0) & (sub.dSharpe_H2 > 0) & (sub.dSharpe_OOS > 0)]
        bnd[proxy] = int(ok.dec.min()) if len(ok) else None
        P(f"  {proxy}: deciles clearing all three = "
          f"{sorted(ok.dec.tolist()) if len(ok) else 'NONE'}; boundary = {bnd[proxy]}")
    h4 = bool(bnd["CAP"] is not None and bnd["ADV"] is not None
              and abs(bnd["CAP"] - bnd["ADV"]) <= 2)
    P(f"H4 -> {'HOLDS' if h4 else 'FAILS'}")
    P("  For reference, the same test on the two LARGE-CAP panels (whole panel, not deciles):")
    for k in ("U56", "B136"):
        c = core[core.panel == k].set_index("cad")
        P(f"    {k}: dSharpe_H1/H2/OOS at W = {c.loc['W','dSharpe_H1']:+.4f} / "
          f"{c.loc['W','dSharpe_H2']:+.4f} / {c.loc['W','dSharpe_OOS']:+.4f}")

    # ---------------- rule 8 ----------------------------------------------
    P("\n" + "-" * 180)
    P("RULE 8 WALK-FORWARD - (cadence, lookback) chosen on IS Sharpe inside each "
      "(panel x gate x construction) arm, 2017-2026 read once")
    P("-" * 180)
    wf = []
    for k in PANELS:
        for gate in GATES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == k) & (G.gate == gate) & (G.con == con)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                wf.append(dict(panel=k, gate=gate, con=con, cad=pick.cad, lb=int(pick.lb),
                               isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                               oMaxDD=pick.oMaxDD,
                               ctrl_oSharpe=ctrl[(k, pick.cad)]["oSharpe"],
                               ctrl_oCAGR=ctrl[(k, pick.cad)]["oCAGR"],
                               spy_oSharpe=spy_stat[k]["oSharpe"], spy_oCAGR=spy_stat[k]["oCAGR"],
                               live_oSharpe=live_s["oSharpe"],
                               beats_ctrl=pick.oSharpe > ctrl[(k, pick.cad)]["oSharpe"],
                               beats_spy=pick.oSharpe > spy_stat[k]["oSharpe"],
                               beats_live=pick.oSharpe > live_s["oSharpe"],
                               p4a=pick.p4a, f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    P(fmt(WF.set_index(["panel", "gate", "con"])))
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\nPicks beating the matched no-filter control OOS: {int(WF.beats_ctrl.sum())}/18; "
      f"SPY {int(WF.beats_spy.sum())}/18; the live RULES v2 book {int(WF.beats_live.sum())}/18.")

    P("\nBOTH KEEP PATHS:")
    P(f"  sweep ({len(G)} cells)   4a {int(G.p4a.sum())}  4b {int(G.p4b.sum())}")
    P(f"  deciles ({len(S)} cells) 4a {int(S.p4a.sum())}  4b {int(S.p4b.sum())}")
    for nm, df in (("sweep", G), ("deciles", S)):
        if df.p4b.any():
            P(f"  4b passes in {nm}:")
            idx = ["panel", "con", "cad", "gate", "lb"] if nm == "sweep" else ["proxy", "dec", "gate", "con"]
            P(fmt(df[df.p4b].set_index(idx)[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]]))
    P("  binding 4b bar (sweep), cells failing on each:")
    P(fmt(G.f4b.value_counts().to_frame("cells")))

    # ---------------- verdict ---------------------------------------------
    P("\n" + "=" * 180)
    held = dict(H1=h1, H2=h2, H3=h3, H4=h4, H5=h5)
    P("Pre-registered bars: " + ", ".join(f"{k} {'HOLDS' if v else 'FAILS'}" for k, v in held.items()))
    P("=" * 180)
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
