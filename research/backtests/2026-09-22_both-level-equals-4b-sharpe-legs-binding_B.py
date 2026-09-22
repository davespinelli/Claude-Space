#!/usr/bin/env python3
"""Idea 906 (lane B, 2026-09-22) — is BOTH-LEVEL == 4b a record-wide fact, i.e. are the
three 4b SHARPE legs EVER binding once the two LEVEL legs hold?

Idea 887 found, on its own 1,710-book grid, that a book clearing the two LEVEL legs
(L4_DD MaxDD <= 60% of SPY's, L5_CAGR CAGR >= 70% of SPY's) ALWAYS also cleared the three
SHARPE legs (H1 > SPY, H2 > SPY, OOS > SPY): 57/57 at 10 bps, 24/24 at 25 bps, 92 vs 89 at
0 bps.  If that is a record-wide fact then every committed 4b verdict is really a TWO-leg
verdict and PROTOCOL rule 4b's three Sharpe legs do no work.

The queue files 906 as a census of the record's committed 4b grids (prose).  This run
answers it with a FRESHLY PRICED grid instead, so it carries its own price leg:

  panel   {U56, B136}                                   (published, not tuned)
  book    {BAND0, BAND3, BAND8, TOP5, TOP10, TOP20,     (published, not tuned)
           TOP40, ALLELIG}
  gross   {0.50, 0.75, 1.00}                            (published, not tuned)
  cadence {W, M, Q}                                     (published, not tuned)
  = 144 books, every one priced and published.

TWO TUNED PARAMETERS, exactly as the idea names them:
  (1) GRID SET   — the 144-book family above.
  (2) COST RUNG  — {0, 10, 25, 50} bps.  PROTOCOL's rung is 10 bps; the other three are
                   reported because 887's one non-equality was at 0 bps.
  => 144 x 4 = 576 grid rows, ALL published.

Cost is applied analytically (returns = gross returns - turnover * bps/1e4), which is an
exact identity with engine.backtest because the drift path does not depend on cost; gate
G1 below checks it against engine.backtest at max|d| tolerance.

PROTOCOL rule 8 walk-forward is run on the SAME grid: per panel and per cost rung, the
IS-only chooser (argmax Sharpe on 2009-2016) picks one book, 2017-2026 is read once, and
both KEEP paths are evaluated for the pick against the LIVE RULES v2 book and SPY.

Deterministic, no network, no randomness.  Does not modify RULES.md / scan.py / bot.py /
baseline.py.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state, score  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

pd.set_option("display.width", 200)

COSTS = [0, 10, 25, 50]
GROSSES = [0.50, 0.75, 1.00]
CADENCES = ["W", "M", "Q"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
WARMUP = 260


# ----------------------------------------------------------------------------- books
def w_band(px, band, gross):
    return rules_v2_weights(px, band=band, gross=gross)


def w_topk(px, k, gross):
    """Top-k by 12-1 momentum among names inside the 200d +/-3% band; gross RE-SPREAD
    over the k held names (gross/k each), so this family is the concentrated,
    full-exposure counterpart of the de-grossing band book."""
    mom = px.shift(21) / px.shift(252) - 1
    elig = mom.where(band_state(px, 0.03) & px.notna())
    rank = elig.rank(axis=1, ascending=False)
    held = (rank <= k).astype(float)
    n = held.sum(axis=1).replace(0, np.nan)
    return held.div(n, axis=0).fillna(0.0) * gross


def w_allelig(px, gross):
    """RULES v1's eligibility screen (above 200d AND vol20 < 0.60), equal weight, gross
    re-spread over the eligible set (the 2026-09-03 memo's Finding 2 book)."""
    s, above, vol20 = score(px, vol_scale=True)
    e = (above & (vol20 < 0.60) & px.notna()).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).fillna(0.0) * gross


BOOKS = (
    [(f"BAND{int(b*100):02d}", (lambda b: (lambda px, g: w_band(px, b, g)))(b)) for b in (0.00, 0.03, 0.08)]
    + [(f"TOP{k}", (lambda k: (lambda px, g: w_topk(px, k, g)))(k)) for k in (5, 10, 20, 40)]
    + [("ALLELIG", lambda px, g: w_allelig(px, g))]
)


# ----------------------------------------------------------------------------- pricing
def gross_path(px, weights, freq):
    """engine.backtest at zero cost -> (gross returns, turnover). Cost is separable."""
    res = backtest(px, weights, cost_bps=0.0, freq=freq)
    return res["returns"], res["turnover"]


def net(rg, to, bps):
    return rg - to * bps / 1e4


def legs(r, spy, bars):
    """The five PROTOCOL 4b legs for a return series r, plus the raw numbers."""
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ro = r.loc[OOS_START:]
    mo = metrics(ro)
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
             IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"])
    d["L1_H1"] = d["H1"] > bars["spy_H1"]
    d["L2_H2"] = d["H2"] > bars["spy_H2"]
    d["L3_OOS"] = d["OOS_Sharpe"] > bars["spy_OOS_Sharpe"]
    d["L4_DD"] = d["MaxDD"] >= 0.60 * bars["spy_MaxDD"]              # MaxDD is negative
    d["L5_CAGR"] = d["CAGR"] >= 0.70 * bars["spy_CAGR"]
    d["L4_DD_OOS"] = d["OOS_MaxDD"] >= 0.60 * bars["spy_OOS_MaxDD"]
    d["L5_CAGR_OOS"] = d["OOS_CAGR"] >= 0.70 * bars["spy_OOS_CAGR"]
    d["BOTHLEVEL"] = d["L4_DD"] and d["L5_CAGR"]
    d["ALLSHARPE"] = d["L1_H1"] and d["L2_H2"] and d["L3_OOS"]
    d["PASS4b"] = d["BOTHLEVEL"] and d["ALLSHARPE"]
    d["BOTHLEVEL_OOS"] = d["L4_DD_OOS"] and d["L5_CAGR_OOS"]
    d["PASS4b_OOS"] = d["BOTHLEVEL_OOS"] and d["ALLSHARPE"]
    return d


def run_panel(name, px):
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    ms, ms1, ms2 = metrics(spy), metrics(spy.iloc[:len(spy) // 2]), metrics(spy.iloc[len(spy) // 2:])
    mso = metrics(spy.loc[OOS_START:])
    bars = dict(spy_H1=ms1["Sharpe"], spy_H2=ms2["Sharpe"], spy_OOS_Sharpe=mso["Sharpe"],
                spy_MaxDD=ms["MaxDD"], spy_CAGR=ms["CAGR"],
                spy_OOS_MaxDD=mso["MaxDD"], spy_OOS_CAGR=mso["CAGR"])
    print(f"\n### panel {name}: SPY FULL {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}"
          f" | halves {ms1['Sharpe']:.4f} / {ms2['Sharpe']:.4f} | OOS {mso['CAGR']:.2%} / {mso['Sharpe']:.4f} / {mso['MaxDD']:.2%}")
    print(f"    4b bars: CAGR floor {0.70*ms['CAGR']:.2%}, MaxDD cap {0.60*ms['MaxDD']:.2%}"
          f" (OOS: floor {0.70*mso['OOS_CAGR'] if False else 0.70*mso['CAGR']:.2%}, cap {0.60*mso['MaxDD']:.2%})")

    # live baseline, one per cadence (the live book is weekly; other cadences priced for 4a at matched cadence)
    base = {}
    for cad in CADENCES:
        rg, to = gross_path(px, rules_v2_weights(px), cad)
        base[cad] = (rg.loc[start:], to.loc[start:])
    base_rows = {}
    for cad in CADENCES:
        for c in COSTS:
            rb = net(*base[cad], c)
            hb = len(rb) // 2
            base_rows[(cad, c)] = dict(CAGR=metrics(rb)["CAGR"], Sharpe=metrics(rb)["Sharpe"],
                                       MaxDD=metrics(rb)["MaxDD"], H1=metrics(rb.iloc[:hb])["Sharpe"],
                                       H2=metrics(rb.iloc[hb:])["Sharpe"],
                                       OOS_CAGR=metrics(rb.loc[OOS_START:])["CAGR"],
                                       OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                                       OOS_MaxDD=metrics(rb.loc[OOS_START:])["MaxDD"])

    rows = []
    for bname, bfn in BOOKS:
        for g in GROSSES:
            w = bfn(px, g)
            for cad in CADENCES:
                rg, to = gross_path(px, w, cad)
                rg, to = rg.loc[start:], to.loc[start:]
                turns = to.sum() / (len(rg) / 252)
                for c in COSTS:
                    r = net(rg, to, c)
                    d = legs(r, spy, bars)
                    b = base_rows[(cad, c)]
                    d.update(panel=name, book=bname, gross=g, cadence=cad, cost=c, turnover=turns)
                    # PROTOCOL 4a.  TWO readings, both published:
                    #   PASS4a_LIVE    — vs the LIVE book as RULES v2 actually runs it (WEEKLY),
                    #                    at the same cost rung.  This is PROTOCOL's own reading.
                    #   PASS4a_MATCHED — vs RULES v2 re-priced at the CANDIDATE's cadence.  Looser,
                    #                    reported only so the cadence channel is visible.
                    bl_ = base_rows[("W", c)]
                    d["PASS4a_LIVE"] = (d["H1"] > bl_["H1"]) and (d["H2"] > bl_["H2"]) and (d["MaxDD"] >= bl_["MaxDD"])
                    d["PASS4a_MATCHED"] = (d["H1"] > b["H1"]) and (d["H2"] > b["H2"]) and (d["MaxDD"] >= b["MaxDD"])
                    d["PASS4a"] = d["PASS4a_LIVE"]
                    rows.append(d)
    return pd.DataFrame(rows), bars, base_rows, spy, start


def census(df, tag, level="BOTHLEVEL", allsharpe="ALLSHARPE", p4b="PASS4b"):
    print(f"\n--- CENSUS ({tag}) : does a SHARPE leg ever bind once BOTH LEVEL legs hold? ---")
    print(f"{'panel':6} {'cost':>5} {'N':>5} {'BOTHLEVEL':>10} {'4b':>5} {'BINDING':>8} "
          f"{'L1 fail':>8} {'L2 fail':>8} {'L3 fail':>8}")
    for panel, gp in df.groupby("panel", sort=False):
        for c in COSTS:
            s = gp[gp.cost == c]
            bl = s[s[level]]
            binding = int((~bl[allsharpe]).sum())
            print(f"{panel:6} {c:5d} {len(s):5d} {len(bl):10d} {int(s[p4b].sum()):5d} {binding:8d} "
                  f"{int((~bl.L1_H1).sum()):8d} {int((~bl.L2_H2).sum()):8d} {int((~bl.L3_OOS).sum()):8d}")
    s = df
    bl = s[s[level]]
    print(f"{'BOTH':6} {'all':>5} {len(s):5d} {len(bl):10d} {int(s[p4b].sum()):5d} "
          f"{int((~bl[allsharpe]).sum()):8d} {int((~bl.L1_H1).sum()):8d} {int((~bl.L2_H2).sum()):8d} {int((~bl.L3_OOS).sum()):8d}")
    return bl


def main():
    out = []
    allrows = []
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True))]

    # ---- GATE G1: the analytic cost identity vs engine.backtest -------------------
    px0 = panels[0][1]
    w0 = rules_v2_weights(px0)
    rg, to = gross_path(px0, w0, "W")
    for c in COSTS:
        ref = backtest(px0, w0, cost_bps=c, freq="W")["returns"]
        d = float((net(rg, to, c) - ref).abs().max())
        print(f"GATE G1 cost identity @ {c:>2} bps: max|d| = {d:.3e}")
        assert d < 1e-12

    for name, px in panels:
        df, bars, base_rows, spy, start = run_panel(name, px)
        allrows.append(df)
        out.append((name, df, bars, base_rows, spy, start))
    df = pd.concat(allrows, ignore_index=True)

    # ---- ALL 576 GRID ROWS -------------------------------------------------------
    print("\n\n================ ALL 576 GRID ROWS (every point published) ================")
    cols = ["panel", "book", "gross", "cadence", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover",
            "L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR", "BOTHLEVEL", "ALLSHARPE", "PASS4b",
            "PASS4a_LIVE", "PASS4a_MATCHED"]
    show = df[cols].copy()
    for c in ("CAGR", "MaxDD", "OOS_CAGR", "OOS_MaxDD"):
        show[c] = show[c].map(lambda x: f"{x:.2%}")
    for c in ("Sharpe", "H1", "H2", "OOS_Sharpe", "turnover"):
        show[c] = show[c].map(lambda x: f"{x:.4f}")
    print(show.to_string(index=False))

    # ---- THE CENSUS --------------------------------------------------------------
    bl_full = census(df, "FULL-window level legs, PROTOCOL reading")
    bl_oos = census(df, "OOS-window level legs (2090's L4_DD_OOS / L5_CAGR_OOS)",
                    level="BOTHLEVEL_OOS", p4b="PASS4b_OOS")

    print("\n--- THE BINDING ROWS (BOTH LEVEL legs hold, at least one SHARPE leg FAILS), FULL reading ---")
    b = df[df.BOTHLEVEL & ~df.ALLSHARPE]
    if len(b) == 0:
        print("NONE — BOTH-LEVEL == 4b on all 576 rows.")
    else:
        bb = b[["panel", "book", "gross", "cadence", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "L1_H1", "L2_H2", "L3_OOS"]].copy()
        for c in ("CAGR", "MaxDD"):
            bb[c] = bb[c].map(lambda x: f"{x:.2%}")
        for c in ("Sharpe", "H1", "H2", "OOS_Sharpe"):
            bb[c] = bb[c].map(lambda x: f"{x:.4f}")
        print(bb.to_string(index=False))

    # ---- MARGINAL LEG FAIL RATES over the whole grid ------------------------------
    print("\n--- MARGINAL FAIL RATE of each leg over all 576 rows (unconditional) ---")
    for L in ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"):
        print(f"  {L:9} fail {1-df[L].mean():.4f}   ({int((~df[L]).sum())} of {len(df)})")
    print(f"  BOTHLEVEL  hold {df.BOTHLEVEL.mean():.4f}   4b pass {df.PASS4b.mean():.4f}   "
          f"4a pass (LIVE weekly book) {df.PASS4a_LIVE.mean():.4f}   "
          f"4a pass (cadence-matched) {df.PASS4a_MATCHED.mean():.4f}")
    print(f"  rows clearing BOTH KEEP paths: 4b & 4a_LIVE {int((df.PASS4b & df.PASS4a_LIVE).sum())}, "
          f"4b & 4a_MATCHED {int((df.PASS4b & df.PASS4a_MATCHED).sum())}")

    # ---- WHY: the implied Calmar constraint --------------------------------------
    print("\n--- MECHANISM: the two LEVEL legs imply a Calmar floor; is that what carries Sharpe? ---")
    for name, _df, bars, *_ in out:
        implied = (0.70 * bars["spy_CAGR"]) / abs(0.60 * bars["spy_MaxDD"])
        spy_calmar = bars["spy_CAGR"] / abs(bars["spy_MaxDD"])
        s = df[df.panel == name]
        bl = s[s.BOTHLEVEL]
        print(f"  {name}: implied Calmar floor {implied:.4f} vs SPY Calmar {spy_calmar:.4f} "
              f"({implied/spy_calmar:.2f}x). Among BOTHLEVEL rows: min FULL Sharpe {bl.Sharpe.min():.4f}, "
              f"min H1 {bl.H1.min():.4f} (bar {bars['spy_H1']:.4f}), min H2 {bl.H2.min():.4f} "
              f"(bar {bars['spy_H2']:.4f}), min OOS {bl.OOS_Sharpe.min():.4f} (bar {bars['spy_OOS_Sharpe']:.4f})")
        nb = s[~s.BOTHLEVEL]
        print(f"        non-BOTHLEVEL rows: {int(nb.ALLSHARPE.sum())} of {len(nb)} clear all three SHARPE legs "
              f"(i.e. the SHARPE legs alone would admit them)")

    # ---- SLACK: how close does the nearest row come to binding? --------------------
    print("\n--- HOW CLOSE: minimum SHARPE-leg slack among BOTHLEVEL rows (pp of Sharpe) ---")
    for name, _df, bars, *_ in out:
        bl = df[(df.panel == name) & df.BOTHLEVEL]
        if not len(bl):
            print(f"  {name}: no BOTHLEVEL rows"); continue
        sl = pd.DataFrame({"H1": bl.H1 - bars["spy_H1"], "H2": bl.H2 - bars["spy_H2"],
                           "OOS": bl.OOS_Sharpe - bars["spy_OOS_Sharpe"]})
        mn = sl.min(axis=1)
        i = mn.idxmin()
        print(f"  {name}: min over rows of min-over-legs slack = {mn.min():+.4f} at "
              f"{bl.loc[i,'book']}/g{bl.loc[i,'gross']:.2f}/{bl.loc[i,'cadence']}/{int(bl.loc[i,'cost'])}bps "
              f"(H1 {sl.loc[i,'H1']:+.4f}, H2 {sl.loc[i,'H2']:+.4f}, OOS {sl.loc[i,'OOS']:+.4f})")
        print(f"        per-leg minimum slack across BOTHLEVEL rows: H1 {sl.H1.min():+.4f}, "
              f"H2 {sl.H2.min():+.4f}, OOS {sl.OOS.min():+.4f}")

    # ---- PROTOCOL RULE 8 WALK-FORWARD --------------------------------------------
    print("\n\n================ PROTOCOL RULE 8 WALK-FORWARD ================")
    print("IS-only chooser: argmax Sharpe on 2009-2016 over the panel's own 72-book shelf at the")
    print("SAME cost rung; 2017-2026 read ONCE.  Both KEEP paths evaluated for the pick.")
    wf = []
    for name, _dfp, bars, base_rows, spy, start in out:
        mso = metrics(spy.loc[OOS_START:])
        for c in COSTS:
            s = df[(df.panel == name) & (df.cost == c)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            b = base_rows[(pick.cadence, c)]
            blw = base_rows[("W", c)]
            p4a_oos = (pick.OOS_Sharpe > blw["OOS_Sharpe"]) and (pick.OOS_MaxDD >= blw["OOS_MaxDD"])
            p4b_oos = (pick.L1_H1 and pick.L2_H2 and pick.L3_OOS
                       and pick.OOS_MaxDD >= 0.60 * mso["MaxDD"] and pick.OOS_CAGR >= 0.70 * mso["CAGR"])
            wf.append(dict(panel=name, cost=c, pick=f"{pick.book}/g{pick.gross:.2f}/{pick.cadence}",
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD, base_OOS_Sharpe=blw["OOS_Sharpe"], base_OOS_MaxDD=blw["OOS_MaxDD"],
                           base_OOS_CAGR=blw["OOS_CAGR"], spy_OOS_CAGR=mso["CAGR"], spy_OOS_Sharpe=mso["Sharpe"],
                           spy_OOS_MaxDD=mso["MaxDD"], FULL_4a=bool(pick.PASS4a), FULL_4b=bool(pick.PASS4b),
                           OOS_4a=bool(p4a_oos), OOS_4b=bool(p4b_oos),
                           BOTHLEVEL=bool(pick.BOTHLEVEL), ALLSHARPE=bool(pick.ALLSHARPE)))
    wfd = pd.DataFrame(wf)
    sh = wfd.copy()
    for c in ("OOS_CAGR", "OOS_MaxDD", "base_OOS_MaxDD", "base_OOS_CAGR", "spy_OOS_CAGR", "spy_OOS_MaxDD"):
        sh[c] = sh[c].map(lambda x: f"{x:.2%}")
    for c in ("IS_Sharpe", "OOS_Sharpe", "base_OOS_Sharpe", "spy_OOS_Sharpe"):
        sh[c] = sh[c].map(lambda x: f"{x:.4f}")
    print(sh.to_string(index=False))
    print(f"\nwalk-forward cells clearing 4a on OOS: {int(wfd.OOS_4a.sum())} of {len(wfd)}; "
          f"clearing 4b on OOS: {int(wfd.OOS_4b.sum())} of {len(wfd)}")
    print(f"walk-forward picks where BOTHLEVEL holds: {int(wfd.BOTHLEVEL.sum())} of {len(wfd)}; "
          f"of those, SHARPE legs binding: {int((wfd.BOTHLEVEL & ~wfd.ALLSHARPE).sum())}")

    # ---- the grid's own best 4b rows, for the record ------------------------------
    print("\n--- ALL 4b PASSES ON THE GRID (FULL reading), sorted by OOS Sharpe ---")
    p = df[df.PASS4b].sort_values("OOS_Sharpe", ascending=False)
    if len(p) == 0:
        print("NONE")
    else:
        pp = p[["panel", "book", "gross", "cadence", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover", "PASS4a_LIVE", "PASS4a_MATCHED"]].copy()
        for c in ("CAGR", "MaxDD", "OOS_CAGR", "OOS_MaxDD"):
            pp[c] = pp[c].map(lambda x: f"{x:.2%}")
        for c in ("Sharpe", "H1", "H2", "OOS_Sharpe", "turnover"):
            pp[c] = pp[c].map(lambda x: f"{x:.4f}")
        print(pp.to_string(index=False))

    df.to_csv(Path(__file__).with_suffix(".grid.csv"), index=False)
    print(f"\ngrid written to {Path(__file__).with_suffix('.grid.csv').name}")


if __name__ == "__main__":
    main()
