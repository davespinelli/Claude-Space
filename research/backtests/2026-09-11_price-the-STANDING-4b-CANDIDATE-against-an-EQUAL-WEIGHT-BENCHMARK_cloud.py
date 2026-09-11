#!/usr/bin/env python3
"""IDEA 742  price the STANDING 4b CANDIDATE against an EQUAL-WEIGHT BENCHMARK.

QUESTION
--------
The standing KEEP-candidate (idea 733, memo `2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md`)
is the live RULES v2 band book with one dial moved: gross 0.75 -> 1.00.  Its 4b case is scored
against **cap-weighted SPY**, the PROTOCOL rule-4 bar.  Idea 548 then showed that bar is worth
**+0.2388 of Sharpe** on a large-cap pool before any skill, because every book in the record is
EQUAL-WEIGHT and SPY is not, and that 36 of 46 fresh-block 4b passers die once the bar is
cap-matched (0 of 60 out of sample).  Idea 548 did NOT re-score the standing candidate.
This run does exactly that: the candidate's five 4b legs, on its own panels, against an
equal-weight version of its own panel.

TWO TUNED PARAMETERS (the queue's own, nothing else is searched)
---------------------------------------------------------------
  1. BENCHMARK FORM (5 levels, all reported)
        B_SPY     cap-weighted SPY buy-and-hold.  PROTOCOL rule 4's bar today.
        B_EW      equal-weight of THE PANEL'S OWN names, daily-rebalanced, 0 bps.
                  The "equal-weight version of its own panel" the queue asks for.
        B_EW10    the same basket charged the book's own 10 bps of rebalancing cost.
                  (B_EW at 0 bps flatters the bar; B_EW10 is the cost-matched reading.)
        B_EWBH    equal-weight BUY-AND-HOLD from day one (weights drift).  The cheapest
                  honest equal-weight bar: no rebalancing, no cost, no turnover.
        B_HALF    0.5*B_SPY + 0.5*B_EW - halfway between the PROTOCOL bar and the match.
  2. PANEL (3 levels, all reported): U56 (universe.json), B136 (universe_broad.json),
     SMALL439 (the sub-$2B panel with the 44 names of max_1d_move >= 1.0 dropped).

The book itself is NOT searched: band 0.03, weekly, 10 bps, next-day, de-gross to cash, exactly
as the memo specifies.  The gross ladder {0.50,0.60,0.75,0.90,1.00} appears only (i) as context
and (ii) inside rule 8, where gross is chosen on the IS window alone - which is the candidate's
OWN selector, not a third tuned parameter.

FRAME.  Memo line 9c identifies the candidate's frame as **SPY-FREE**: SPY is a benchmark, not a
constituent.  Every book here is built on the panel with SPY removed, so the memo's own numbers
are reproducible (gate G1).

PRE-REGISTERED GATES
--------------------
G1 MEMO REPRODUCTION.  U56 g1.00 SPY-free full-sample (CAGR,Sharpe,MaxDD,H1,H2) and OOS
   (CAGR,Sharpe,MaxDD) must match memo lines 3-4 to < 1e-3.
G2 THE PROTOCOL BAR.  U56 SPY buy-and-hold must read memo line 3's 15.11% / 0.8835 / -33.72%
   to < 1e-3.
G3 EW SANITY.  ew_index over one column == that column's pct_change (< 1e-12); ew_index over
   all names at 0 bps == the cross-sectional mean of live daily returns (< 1e-12).
G4 THE BARS ARE DISTINCT.  |Sharpe(B_EW) - Sharpe(B_SPY)| > 0.01 on U56 - otherwise the swap
   is not a real test.
G5 BLEND.  B_HALF == 0.5*(B_SPY + B_EW) to < 1e-15.

WHAT WOULD FALSIFY THE QUEUE'S PREMISE
--------------------------------------
If the candidate clears 4b against B_EW / B_EW10 / B_EWBH on U56 with the same legs binding,
the +0.2388 large-cap equal-weight premium is NOT what the candidate is harvesting and the
memo's case survives the swap.  If it fails, the memo's five numbers are a comparand fact.
Reported either way; a documented KILL is the result.

SURVIVORSHIP.  universe.json and universe_broad.json are CURRENT constituents; the small panel
is a current screen (data/SMALL_PANEL_README.md).  This cuts BOTH ways here - the equal-weight
bar is built from the same survivors as the book, so the swap is survivorship-NEUTRAL even
though each individual number is survivorship-inflated.

Run:  python3 research/backtests/2026-09-11_price-the-STANDING-4b-CANDIDATE-against-an-EQUAL-WEIGHT-BENCHMARK_cloud.py
"""
import sys, time, json
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v2_weights                      # noqa: E402
from engine import metrics, rebalance_mask                                # noqa: E402

OUT = Path(__file__).with_suffix("")
def out_path(ext): return Path(str(OUT) + ext)

COST_BPS, FREQ, BAND = 10, "W", 0.03
GROSS_LADDER = [0.50, 0.60, 0.75, 0.90, 1.00]
CANDIDATE_G, LIVE_G = 1.00, 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BENCHES = ["B_SPY", "B_EW", "B_EW10", "B_EWBH", "B_HALF"]
PANELS = ["U56", "B136", "SMALL439"]
WARMUP = 260

MEMO_FULL = dict(CAGR=0.1155, Sharpe=1.2067, MaxDD=-0.1570, H1=1.2405, H2=1.1798)
MEMO_OOS = dict(OOS_CAGR=0.1270, OOS_Sharpe=1.2827, OOS_MaxDD=-0.1570)
MEMO_SPY = dict(CAGR=0.1511, Sharpe=0.8835, MaxDD=-0.3372)

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def flush_log(): out_path(".console.txt").write_text("\n".join(LOG) + "\n")


# --------------------------------------------------------------------- machinery (record's own)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """engine.backtest's arithmetic: weights decided at close t, applied t+1; costs on turnover."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(pr - turn * cost_bps / 1e4, index=prices.index)


def stat_block(r):
    h = len(r) // 2
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
    out["IS_CAGR"] = metrics(ris)["CAGR"] if len(ris) > 60 else np.nan
    out["IS_Sharpe"] = metrics(ris)["Sharpe"] if len(ris) > 60 else np.nan
    out["IS_MaxDD"] = metrics(ris)["MaxDD"] if len(ris) > 60 else np.nan
    mo = metrics(ros) if len(ros) > 60 else dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    out["OOS_CAGR"], out["OOS_Sharpe"], out["OOS_MaxDD"] = mo["CAGR"], mo["Sharpe"], mo["MaxDD"]
    return out


def legs4b(row, bm, oos=False):
    """PROTOCOL rule 4b's five legs, in the record's own order/wording.
    oos=True restates the three window-bound legs on the OOS window alone (H1/H2 of the OOS
    window are its own halves, supplied by the caller as row/bm already sliced)."""
    f = []
    if not row["H1"] > bm["H1"]: f.append("H1")
    if not row["H2"] > bm["H2"]: f.append("H2")
    if not row["OOS_Sharpe"] > bm["OOS_Sharpe"]: f.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(bm["MaxDD"]): f.append("DD")
    if not row["CAGR"] >= 0.70 * bm["CAGR"]: f.append("CAGR")
    return f


def margins4b(row, bm):
    """Signed slack on each leg: >0 means the leg passes.  Sharpe legs in Sharpe units,
    DD in pp of NAV, CAGR in pp/yr."""
    return dict(m_H1=row["H1"] - bm["H1"], m_H2=row["H2"] - bm["H2"],
                m_OOS=row["OOS_Sharpe"] - bm["OOS_Sharpe"],
                m_DD=(0.60 * abs(bm["MaxDD"]) - abs(row["MaxDD"])) * 100.0,
                m_CAGR=(row["CAGR"] - 0.70 * bm["CAGR"]) * 100.0)


def ew_index(px, cols, cost_bps=0.0, drift=False):
    """Equal-weight index over `cols` (idea 548's helper, verbatim).
    drift=False -> daily-rebalanced fixed weights; drift=True -> buy-and-hold from day one."""
    sub = px[list(cols)]
    r = sub.pct_change().fillna(0.0)
    live = sub.notna() & sub.shift(1).notna()
    if not drift:
        w = live.astype(float)
        w = w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        out = (r * w).sum(axis=1)
        turn = w.diff().abs().sum(axis=1).fillna(0.0)
        return out - turn * cost_bps / 1e4
    eq = (1.0 + r.where(live, 0.0)).cumprod()
    tot = eq.mean(axis=1)
    return tot.pct_change().fillna(0.0)


# --------------------------------------------------------------------------------- panels
def load_panels():
    out = {}
    px = load_universe()
    out["U56"] = px
    out["B136"] = load_universe(broad=True)
    small = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in small.columns if c == "SPY" or c not in bad]
    out["SMALL439"] = small[keep]
    return out, len(bad)


def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 742  price the STANDING 4b CANDIDATE against an EQUAL-WEIGHT BENCHMARK")
    P("cloud lane, 2026-09-11.  Candidate = RULES v2 band book at gross 1.00 (idea 733 memo).")
    P("two tuned parameters: BENCHMARK FORM (5) x PANEL (3).  Every grid point published.")
    P("Book fixed at band 0.03 / weekly / 10 bps / next-day / de-gross-to-cash, SPY-FREE frame.")
    P("=" * 104)
    P("pre-registered gates:")
    P("  G1 MEMO REPRO   U56 g1.00 full + OOS reproduce memo lines 3-4 to < 1e-3")
    P("  G2 PROTOCOL BAR U56 SPY buy-and-hold reads 15.11% / 0.8835 / -33.72% to < 1e-3")
    P("  G3 EW SANITY    ew_index(1 col) == that col; ew_index(all,0bps) == mean live return")
    P("  G4 DISTINCT     |Sharpe(B_EW) - Sharpe(B_SPY)| > 0.01 on U56")
    P("  G5 BLEND        B_HALF == 0.5*(B_SPY+B_EW) to < 1e-15")
    P("=" * 104)

    panels, n_dropped = load_panels()
    P(f"\nPANELS (SMALL: {n_dropped} names with max_1d_move >= 1.0 dropped per this run's mandate)")
    for k, v in panels.items():
        names = [c for c in v.columns if c != "SPY"]
        P(f"  {k:<9} {len(names):>4} investable names + SPY benchmark | "
          f"{v.index.min().date()} .. {v.index.max().date()} | {len(v)} rows")

    # ---------------------------------------------------------------- build books + benchmarks
    grid_rows, gate_notes = [], {}
    BOOKS, BMS, STARTS = {}, {}, {}
    for pname, px in panels.items():
        names = [c for c in px.columns if c != "SPY"]
        px_book = px[names]                                   # SPY-FREE frame (memo line 9c)
        start = px.index[WARMUP]
        STARTS[pname] = start
        # books on the gross ladder + the live baseline for 4a
        for g in GROSS_LADDER:
            r = fast_backtest(px_book, rules_v2_weights(px_book, band=BAND, gross=g))
            BOOKS[(pname, g)] = stat_block(r.loc[start:])
        r_live = fast_backtest(px_book, rules_v2_weights(px_book, band=BAND, gross=LIVE_G))
        BOOKS[(pname, "RULESv2")] = stat_block(r_live.loc[start:])
        # benchmarks
        spy = px["SPY"].pct_change().fillna(0.0)
        ew = ew_index(px, names, cost_bps=0.0, drift=False)
        ew10 = ew_index(px, names, cost_bps=COST_BPS, drift=False)
        ewbh = ew_index(px, names, cost_bps=0.0, drift=True)
        half = 0.5 * spy + 0.5 * ew
        series = dict(B_SPY=spy, B_EW=ew, B_EW10=ew10, B_EWBH=ewbh, B_HALF=half)
        BMS[pname] = {b: stat_block(s.loc[start:]) for b, s in series.items()}
        gate_notes[pname] = dict(series=series, start=start, px=px, names=names)

    # --------------------------------------------------------------------------------- gates
    P("\n" + "=" * 104)
    P("GATES")
    P("=" * 104)
    c = BOOKS[("U56", CANDIDATE_G)]
    d1 = max(abs(c[k] - v) for k, v in MEMO_FULL.items())
    d2 = max(abs(c[k] - v) for k, v in MEMO_OOS.items())
    G1 = max(d1, d2) < 1e-3
    P(f"  G1 MEMO REPRO   full max|d| {d1:.3e}  OOS max|d| {d2:.3e}  -> {'PASS' if G1 else 'FAIL'}")
    P(f"     memo 3: {MEMO_FULL['CAGR']:.2%} / {MEMO_FULL['Sharpe']:.4f} / {MEMO_FULL['MaxDD']:.2%} / "
      f"{MEMO_FULL['H1']:.4f} / {MEMO_FULL['H2']:.4f}")
    P(f"     here  : {c['CAGR']:.2%} / {c['Sharpe']:.4f} / {c['MaxDD']:.2%} / {c['H1']:.4f} / {c['H2']:.4f}")
    s = BMS["U56"]["B_SPY"]
    d3 = max(abs(s[k] - v) for k, v in MEMO_SPY.items())
    G2 = d3 < 1e-3
    P(f"  G2 PROTOCOL BAR max|d| {d3:.3e}  (here {s['CAGR']:.2%} / {s['Sharpe']:.4f} / "
      f"{s['MaxDD']:.2%})  -> {'PASS' if G2 else 'FAIL'}")

    gn = gate_notes["U56"]; pxU, nmU = gn["px"], gn["names"]
    one = ew_index(pxU, [nmU[0]], cost_bps=0.0)
    e_one = float((one - pxU[nmU[0]].pct_change().fillna(0.0)).abs().max())
    sub = pxU[nmU]; rr = sub.pct_change().fillna(0.0)
    live = sub.notna() & sub.shift(1).notna()
    manual = (rr.where(live)).mean(axis=1).fillna(0.0)
    e_all = float((ew_index(pxU, nmU, 0.0) - manual).abs().max())
    G3 = e_one < 1e-12 and e_all < 1e-12
    P(f"  G3 EW SANITY    single-name {e_one:.3e}, all-name mean {e_all:.3e} -> {'PASS' if G3 else 'FAIL'}")
    dS = abs(BMS["U56"]["B_EW"]["Sharpe"] - BMS["U56"]["B_SPY"]["Sharpe"])
    G4 = dS > 0.01
    P(f"  G4 DISTINCT     |dSharpe(B_EW,B_SPY)| on U56 = {dS:.4f} -> {'PASS' if G4 else 'FAIL'}")
    sr = gn["series"]
    e_h = float((sr["B_HALF"] - 0.5 * (sr["B_SPY"] + sr["B_EW"])).abs().max())
    G5 = e_h < 1e-15
    P(f"  G5 BLEND        max|d| {e_h:.3e} -> {'PASS' if G5 else 'FAIL'}")
    P(f"\n  GATES: G1 {G1} G2 {G2} G3 {G3} G4 {G4} G5 {G5}")

    # ------------------------------------------------------------------- the benchmark table
    P("\n" + "=" * 104)
    P("THE FIVE BARS, PANEL BY PANEL (full sample from the panel's own warm-up day)")
    P("=" * 104)
    P(f"{'panel':<9} {'bar':<8} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
      f"{'oCAGR':>8} {'oSharpe':>8} | {'4b CAGR floor':>13} {'4b DD cap':>10}")
    for pname in PANELS:
        for b in BENCHES:
            m = BMS[pname][b]
            P(f"{pname:<9} {b:<8} {m['CAGR']:>7.2%} {m['Sharpe']:>8.4f} {m['MaxDD']:>7.2%} "
              f"{m['H1']:>7.4f} {m['H2']:>7.4f} {m['OOS_CAGR']:>7.2%} {m['OOS_Sharpe']:>8.4f} | "
              f"{0.70*m['CAGR']:>12.2%} {0.60*abs(m['MaxDD']):>9.2%}")
        P("")

    # ----------------------------------------------------------- the candidate's five 4b legs
    P("=" * 104)
    P("THE CANDIDATE (gross 1.00) — ITS FIVE 4b LEGS UNDER EACH BAR.  margins: >0 = leg passes")
    P("Sharpe legs in Sharpe units; DD in pp of NAV; CAGR in pp/yr.")
    P("=" * 104)
    P(f"{'panel':<9} {'bar':<8} {'H1':>8} {'H2':>8} {'OOS':>8} {'DD(pp)':>8} {'CAGR(pp)':>9}  "
      f"{'verdict':<9} failed legs")
    for pname in PANELS:
        bk = BOOKS[(pname, CANDIDATE_G)]
        for b in BENCHES:
            bm = BMS[pname][b]
            f = legs4b(bk, bm); mg = margins4b(bk, bm)
            P(f"{pname:<9} {b:<8} {mg['m_H1']:>8.4f} {mg['m_H2']:>8.4f} {mg['m_OOS']:>8.4f} "
              f"{mg['m_DD']:>8.2f} {mg['m_CAGR']:>9.2f}  "
              f"{'4b PASS' if not f else '4b FAIL':<9} {','.join(f) if f else '-'}")
        P("")

    # ------------------------------------------------------------------------- the full grid
    for pname in PANELS:
        for g in GROSS_LADDER:
            bk = BOOKS[(pname, g)]
            for b in BENCHES:
                bm = BMS[pname][b]
                f = legs4b(bk, bm); mg = margins4b(bk, bm)
                base = BOOKS[(pname, "RULESv2")]
                p4a = (bk["H1"] > base["H1"] and bk["H2"] > base["H2"]
                       and bk["MaxDD"] >= base["MaxDD"])
                grid_rows.append(dict(panel=pname, gross=g, bench=b,
                                      CAGR=bk["CAGR"], Sharpe=bk["Sharpe"], MaxDD=bk["MaxDD"],
                                      H1=bk["H1"], H2=bk["H2"],
                                      OOS_CAGR=bk["OOS_CAGR"], OOS_Sharpe=bk["OOS_Sharpe"],
                                      OOS_MaxDD=bk["OOS_MaxDD"],
                                      bm_CAGR=bm["CAGR"], bm_Sharpe=bm["Sharpe"],
                                      bm_MaxDD=bm["MaxDD"], bm_H1=bm["H1"], bm_H2=bm["H2"],
                                      bm_OOS_Sharpe=bm["OOS_Sharpe"], bm_OOS_CAGR=bm["OOS_CAGR"],
                                      **mg,
                                      pass4b=len(f) == 0, failed_legs="|".join(f),
                                      pass4a=p4a))
    G = pd.DataFrame(grid_rows)
    G.to_csv(out_path(".grid.csv"), index=False)

    P("=" * 104)
    P("FULL GRID — 4b pass counts (5 gross rungs x 5 bars x 3 panels = 75 cells, all above in CSV)")
    P("=" * 104)
    piv = G.pivot_table(index="panel", columns="bench", values="pass4b", aggfunc="sum")
    P(piv.reindex(index=PANELS, columns=BENCHES).to_string())
    P(f"\n  4b total: {int(G.pass4b.sum())}/{len(G)}   4a total: {int(G.pass4a.sum())}/{len(G)}")
    P("  binding leg counts among the 4b failures:")
    from collections import Counter
    cnt = Counter(l for s in G.loc[~G.pass4b, "failed_legs"] for l in s.split("|") if l)
    for k, v in cnt.most_common(): P(f"    {k:<5} {v}")

    # --------------------------------------------------------------- RULE 8  walk-forward
    P("\n" + "=" * 104)
    P("RULE 8 WALK-FORWARD — gross chosen on the IS window (<= 2016-12-31) ALONE by max IS")
    P("Sharpe (the candidate's own selector, memo line 8), 2017-2026 read once.  ALL rungs")
    P("reported; the OOS 4b verdict is restated under every bar.")
    P("=" * 104)
    wf_rows = []
    P(f"{'panel':<9} {'gross':>6} {'IS Sharpe':>10} {'IS CAGR':>8} | {'OOS CAGR':>9} "
      f"{'OOS Sharpe':>11} {'OOS MaxDD':>10}  pick")
    picks = {}
    for pname in PANELS:
        best, bestg = -np.inf, None
        for g in GROSS_LADDER:
            bk = BOOKS[(pname, g)]
            if bk["IS_Sharpe"] > best: best, bestg = bk["IS_Sharpe"], g
        picks[pname] = bestg
        for g in GROSS_LADDER:
            bk = BOOKS[(pname, g)]
            P(f"{pname:<9} {g:>6.2f} {bk['IS_Sharpe']:>10.4f} {bk['IS_CAGR']:>7.2%} | "
              f"{bk['OOS_CAGR']:>8.2%} {bk['OOS_Sharpe']:>11.4f} {bk['OOS_MaxDD']:>9.2%}  "
              f"{'<== IS PICK' if g == bestg else ''}")
        sp = BOOKS[(pname, GROSS_LADDER[0])]["IS_Sharpe"]
        spread = max(BOOKS[(pname, g)]["IS_Sharpe"] for g in GROSS_LADDER) - \
                 min(BOOKS[(pname, g)]["IS_Sharpe"] for g in GROSS_LADDER)
        P(f"{'':<9} IS-Sharpe spread across the ladder: {spread:.2e}  "
          f"(memo line 8: the selector is near-indifferent)")
        P("")

    P(f"{'panel':<9} {'gross':>6} {'bar':<8} {'oH1':>8} {'oH2':>8} {'oSharpe':>9} {'oDD(pp)':>9} "
      f"{'oCAGR(pp)':>10}  verdict   failed legs")
    for pname in PANELS:
        px = panels[pname]; start = STARTS[pname]
        names = [c for c in px.columns if c != "SPY"]
        px_book = px[names]
        for g in GROSS_LADDER:
            r = fast_backtest(px_book, rules_v2_weights(px_book, band=BAND, gross=g))
            ros = r.loc[max(pd.Timestamp(OOS_START), start):]
            bk_o = stat_block(ros)
            for b in BENCHES:
                s = gate_notes[pname]["series"][b]
                bm_o = stat_block(s.loc[max(pd.Timestamp(OOS_START), start):])
                f = legs4b(bk_o, bm_o); mg = margins4b(bk_o, bm_o)
                is_pick = (g == picks[pname])
                wf_rows.append(dict(panel=pname, gross=g, bench=b, is_pick=is_pick,
                                    OOS_CAGR=bk_o["CAGR"], OOS_Sharpe=bk_o["Sharpe"],
                                    OOS_MaxDD=bk_o["MaxDD"], OOS_H1=bk_o["H1"], OOS_H2=bk_o["H2"],
                                    bm_OOS_CAGR=bm_o["CAGR"], bm_OOS_Sharpe=bm_o["Sharpe"],
                                    bm_OOS_MaxDD=bm_o["MaxDD"], **mg,
                                    pass4b_oos=len(f) == 0, failed_legs="|".join(f)))
                if is_pick:
                    P(f"{pname:<9} {g:>6.2f} {b:<8} {mg['m_H1']:>8.4f} {mg['m_H2']:>8.4f} "
                      f"{mg['m_OOS']:>9.4f} {mg['m_DD']:>9.2f} {mg['m_CAGR']:>10.2f}  "
                      f"{'4b PASS' if not f else '4b FAIL':<9} {','.join(f) if f else '-'}")
        P("")
    W = pd.DataFrame(wf_rows)
    W.to_csv(out_path(".walkforward.csv"), index=False)
    P("OOS 4b pass counts over ALL 75 walk-forward cells:")
    pw = W.pivot_table(index="panel", columns="bench", values="pass4b_oos", aggfunc="sum")
    P(pw.reindex(index=PANELS, columns=BENCHES).to_string())
    Wp = W[W.is_pick]
    P(f"\n  at the IS pick only ({len(Wp)} cells): OOS 4b {int(Wp.pass4b_oos.sum())}/{len(Wp)}")
    P(f"  over all cells: OOS 4b {int(W.pass4b_oos.sum())}/{len(W)}")

    # --------------------------------------------------------------------------- 4a leg
    P("\n" + "=" * 104)
    P("KEEP PATH 4a (vs RULES v2 live, gross 0.75, same frame) — benchmark-swap-INVARIANT")
    P("=" * 104)
    for pname in PANELS:
        base = BOOKS[(pname, "RULESv2")]
        bk = BOOKS[(pname, CANDIDATE_G)]
        ok = bk["H1"] > base["H1"] and bk["H2"] > base["H2"] and bk["MaxDD"] >= base["MaxDD"]
        P(f"  {pname:<9} cand H1/H2/MaxDD {bk['H1']:.4f}/{bk['H2']:.4f}/{bk['MaxDD']:.2%}  vs "
          f"RULES v2 {base['H1']:.4f}/{base['H2']:.4f}/{base['MaxDD']:.2%}  -> "
          f"{'4a PASS' if ok else '4a FAIL'}")
    P(f"  4a over the full 75-cell grid: {int(G.pass4a.sum())}/{len(G)}")

    # ------------------------------------------------------------------------- the answer
    P("\n" + "=" * 104)
    P("ANSWER")
    P("=" * 104)
    cand = G[(G.gross == CANDIDATE_G)]
    for pname in PANELS:
        sub = cand[cand.panel == pname]
        sp = sub[sub.bench == "B_SPY"].iloc[0]
        P(f"  {pname}: under B_SPY {'PASS' if sp.pass4b else 'FAIL'}; under the equal-weight bars "
          + ", ".join(f"{r.bench}={'PASS' if r.pass4b else 'FAIL(' + r.failed_legs + ')'}"
                      for _, r in sub[sub.bench != "B_SPY"].iterrows()))
    surv = int(cand[cand.bench.isin(["B_EW", "B_EW10", "B_EWBH"])].pass4b.sum())
    P(f"\n  the candidate's 4b survives {surv} of 9 (3 panels x 3 equal-weight bars) full-sample.")
    Wc = W[(W.gross == CANDIDATE_G) & W.bench.isin(["B_EW", "B_EW10", "B_EWBH"])]
    P(f"  out of sample it survives {int(Wc.pass4b_oos.sum())} of {len(Wc)}.")

    json.dump(dict(gates=dict(G1=bool(G1), G2=bool(G2), G3=bool(G3), G4=bool(G4), G5=bool(G5)),
                   memo_repro_full=float(d1), memo_repro_oos=float(d2), spy_repro=float(d3),
                   ew_minus_spy_sharpe_U56=float(BMS["U56"]["B_EW"]["Sharpe"]
                                                 - BMS["U56"]["B_SPY"]["Sharpe"]),
                   pass4b_grid=int(G.pass4b.sum()), n_grid=int(len(G)),
                   pass4a_grid=int(G.pass4a.sum()),
                   pass4b_oos=int(W.pass4b_oos.sum()), n_oos=int(len(W)),
                   cand_ew_full=surv, cand_ew_oos=int(Wc.pass4b_oos.sum()),
                   is_picks={k: float(v) for k, v in picks.items()}),
              out_path(".summary.json").open("w"), indent=2)
    P(f"\nwrote {out_path('.grid.csv').name}, {out_path('.walkforward.csv').name}, "
      f"{out_path('.summary.json').name}")
    P(f"elapsed {time.time() - t0:.1f}s")
    flush_log()


if __name__ == "__main__":
    main()
