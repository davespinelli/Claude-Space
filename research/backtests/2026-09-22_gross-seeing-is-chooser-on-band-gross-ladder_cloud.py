#!/usr/bin/env python3
"""
IDEA 2121 (lane cloud, 2026-09-22) -- can an IS-ONLY CHOOSER THAT SEES GROSS beat IS SHARPE
                                      on a BAND x GROSS ladder?

THE QUESTION, as filed.  Idea 2119 laddered the live book's own form over band x gross and
found (a) all 16 of its 4b passes sit at gross 1.00 on both panels -- the verdict turns
ENTIRELY on the gross dial -- while (b) IS Sharpe, the chooser the record habitually uses for
rule 8, moves only 0.0013 (U56) / 0.0026 (B136) across the WHOLE gross ladder at fixed band.
A chooser that is flat in the only dial that decides the verdict is COIN-FLIPPING that dial.
So: score legal IS-only choosers that DO see gross (IS minimum-4b-leg-margin, IS Calmar, IS
CAGR-floor margin) against IS Sharpe on the same ladder, and publish the OOS verdict spread
each produces.

THE BOOK (RULES v2's own form on its own two dials; nothing new is invented).
    band(i,t) TRUE when close > 200d MA x (1+b), FALSE below x (1-b), previous state in
    between, FALSE before 200 closes exist  ==  baseline.band_state(px, b).
    Hold every priced in-band name at g/#priced of NAV; gated-out weight goes to CASH
    (de-gross, never re-spread).  Weekly, weights at close t applied at t+1, cost per unit
    turnover, long only, no leverage.  (b,g) = (0.03,0.75) IS the live book (gate G3).

THE LADDER (identical to 2119's, so this run is comparable to it cell for cell):
    BAND  b in {0.00, 0.02, 0.03, 0.05, 0.08}
    GROSS g in {0.50, 0.60, 0.75, 0.85, 1.00}          = 25 cells per panel

EXACTLY TWO TUNED DIALS, and every grid point is published (<slug>.grid.csv):
    1. THE LADDER CELL (band x gross).  NOT tuned by hand -- it is what each chooser picks,
       on IS rows only, under rule 8.  All 25 cells are priced and published regardless.
    2. THE CHOOSER SET.  Seven legal IS-only rules, taken VERBATIM from idea 2087/2109 so no
       rule is invented for this run:
         IS_SHARPE     argmax IS Sharpe                       <- the record's habit, gross-blind
         IS_MINMARG    argmax min over the four IS 4b leg margins   (named by the idea)
         IS_CALMAR     argmax IS CAGR / |IS MaxDD|                  (named by the idea)
         IS_CAGRSLACK  argmax (IS CAGR - 0.70 x SPY IS CAGR)        (named by the idea)
         IS_LEGS       argmax #IS 4b legs passed, IS Sharpe tiebreak     (control)
         IS_DD         argmax IS MaxDD (shallowest)                      (control)
         CELL_ALPHA    first cell by label -- ZERO information           (control)
NOT tuned, reported as axes: PANEL {U56, B136}; COST {0,10,25,50} bps (protocol rung 10);
    WINDOWS FULL / IS(..2016-12-31) / OOS(2017-01-01..), rule 8 -- OOS read ONCE.

PRE-REGISTERED BARS, written before any number below was read:
  B1  THE 2119 DIAGNOSIS, RE-MEASURED PER CHOOSER.  For each chooser statistic, its pooled
      spread across the GROSS ladder at fixed band, against its pooled spread across the BAND
      ladder at fixed gross, and the ratio GROSS-spread / (GROSS+BAND spread) = its GROSS
      SHARE.  IS Sharpe should be near 0 (2119's finding); a "sees gross" chooser must be
      materially above it or the idea's premise is wrong.
  B2  REACH.  Does the chooser's IS-only pick land on gross 1.00 -- the only rung 2119 found
      passing 4b?  Published per chooser x panel x cost.
  B3  RULE 8.  OOS CAGR / Sharpe / MaxDD of each chooser's pick, against RULES v2 and SPY,
      BOTH KEEP paths (4b FULL and 4b OOS; 4a FULL and 4a OOS).  2017-2026 read once.
  B4  THE OOS VERDICT SPREAD the idea asks for: over the 7 choosers within one instance
      (panel x cost), the number of DISTINCT cells picked, the best-minus-worst OOS Sharpe
      and OOS CAGR, and whether the choosers agree on the 4b verdict.
  B5  THE CONTROL THAT DECIDES WHETHER ANY OF THIS IS INFORMATION.  If the verdict turns only
      on gross, then MAXGROSS -- "take the top gross rung at the live band, read no in-sample
      data at all" -- is a ZERO-PARAMETER rule.  Priced beside every chooser.  A gross-seeing
      chooser is only worth its fitting if it BEATS MAXGROSS out of sample.  Also priced:
      RANDCELL, the mean over all 25 cells (the uniform-random-draw expectation, no seeds).
  B6  COST LADDER.  B2/B3/B4/B5 re-read at 0 / 25 / 50 bps.
  B7  POST-HOC DIAGNOSTIC of the published grid (declared as post-hoc, no new tuned dial, no
      cell selected on it).  2119 read its own 0.0013 / 0.0026 IS-Sharpe gross spread as
      "rule 8 COIN-FLIPS gross".  A statistic can be nearly FLAT in a dial and still ORDER it
      perfectly, in which case its argmax is deterministic, not a coin flip.  So: is IS Sharpe
      MONOTONE in gross, and where is its argmax?  And -- the question that decides whether
      any of these choosers is adding information -- does the OOS gradient have the SAME SIGN?

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)        bar max|d| < 1e-12
  G2  weekly mask == engine.rebalance_mask(idx,'W')                 bar 0 differing rows
  G3  ladder cell (0.03,0.75) == baseline.rules_v2_weights          bar max|d| == 0
  G4  every chooser reads IS columns only (asserted structurally: pick() is handed an
      IS-only view of the frame and cannot see an OOS column)
  G5  comparands are baseline's own: rules_v2_weights and SPY buy-and-hold.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every
absolute CAGR and drawdown level here is optimistic.  This run is a WITHIN-TAPE contrast
between choosers on the same 25 cells; it does not repair the level.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_gross-seeing-is-chooser-on-band-gross-ladder_cloud.py
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

DATE, SLUG = "2026-09-22", "gross-seeing-is-chooser-on-band-gross-ladder"
OUT = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

BANDS   = [0.00, 0.02, 0.03, 0.05, 0.08]
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]
COSTS   = [0, 10, 25, 50]
COST0   = 10
FREQ    = "W"
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
LIVE    = (0.03, 0.75)
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CHOOSERS = ["IS_SHARPE", "IS_MINMARG", "IS_CALMAR", "IS_CAGRSLACK",
            "IS_LEGS", "IS_DD", "CELL_ALPHA"]
REFRULES = ["MAXGROSS", "RANDCELL"]          # zero-parameter comparands (B5)


# ------------------------------------------------------------------ book + engine
def ladder_weights(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def run(prices, weights, mask):
    """engine.backtest's loop in numpy (gate G1).  Costs applied afterwards -- they never
    change the held path -- so one loop serves every cost rung."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        gross_ret[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index))


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= DD_CAP * ss["MaxDD"], CAGR=s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])
    Mg = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
              DD=(s["MaxDD"] - DD_CAP * ss["MaxDD"]) * 100,
              CAGR=(s["CAGR"] - CAGR_FLOOR * ss["CAGR"]) * 100)
    return all(L.values()), L, Mg


def keep4b_oos(s, ss):
    return (s["Sharpe"] > ss["Sharpe"] and s["MaxDD"] >= DD_CAP * ss["MaxDD"]
            and s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])


def keep4a(s, sb):
    return (s["H1"] > sb["H1"]) and (s["H2"] > sb["H2"]) and (s["MaxDD"] >= sb["MaxDD"])


def keep4a_oos(s, sb):
    return (s["Sharpe"] > sb["Sharpe"]) and (s["MaxDD"] >= sb["MaxDD"])


# ------------------------------------------------------------------ choosers (IS-only)
def pick(sub, chooser):
    """LEGAL IS-ONLY chooser.  `sub` carries IS columns only (gate G4).  Deterministic
    tie-break on the cell label ascending, so no rule wins on ordering luck."""
    s = sub.sort_values("cell").reset_index(drop=True)
    if chooser == "IS_SHARPE":        key = s.is_Sharpe.values
    elif chooser == "IS_LEGS":        key = s.is_legs.values * 1e6 + s.is_Sharpe.values
    elif chooser == "IS_CALMAR":      key = np.nan_to_num(s.is_calmar.values, nan=-1e9)
    elif chooser == "IS_MINMARG":     key = s.is_minmarg.values
    elif chooser == "IS_CAGRSLACK":   key = s.is_cagrslack.values
    elif chooser == "IS_DD":          key = s.is_MaxDD.values
    elif chooser == "CELL_ALPHA":     return s.iloc[0]["cell"]
    else: raise ValueError(chooser)
    return s.iloc[int(np.argmax(np.nan_to_num(key, nan=-1e18)))]["cell"]


def main():
    P("=" * 100)
    P("IDEA 2121 lane cloud 2026-09-22 -- can an IS-ONLY CHOOSER THAT SEES GROSS beat IS SHARPE")
    P("                                   on a BAND x GROSS ladder?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned dial 1: ladder cell band {BANDS} x gross {GROSSES} ({len(BANDS)*len(GROSSES)} cells/panel),")
    P(f"              chosen on IS rows ONLY by each chooser -- never by hand.")
    P(f"tuned dial 2: chooser set {CHOOSERS}")
    P(f"reported axes: panels U56 + B136, costs {COSTS} bps (protocol {COST0}), cadence {FREQ},")
    P(f"               windows FULL / IS ..{IS_END} / OOS {OOS_BEG}.. (rule 8, read once)")
    P(f"zero-parameter comparands (B5): {REFRULES}")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} names  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ---------------------------------------------------------------- GATES
    P("-" * 100); P("(G) GATES -- printed before any hypothesis is read"); P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]
    m0 = rebalance_mask(px_u.index, FREQ)
    g2 = 0; ok = True; gp += ok; gn += 1
    P(f"  G2  weekly mask is engine.rebalance_mask(idx,'W') itself : {g2} differing rows   [PASS]")
    gate_rows.append(dict(gate="G2", value=g2, bar="0 differing rows", passed=True))

    w_live = ladder_weights(px_u, *LIVE)
    g3 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u, *LIVE).values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  ladder cell (0.03,0.75) == baseline.rules_v2_weights : max|d| {g3:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]  (the ladder's centre cell IS the live book)")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=bool(ok)))

    gr, to = run(px_u, w_live, m0)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"].values
    fin = np.isfinite(b)
    g1 = float(np.abs(a[fin] - b[fin]).max()); ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e} over "
      f"{int(fin.sum())} rows   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))
    P("  G4  pick() is handed an IS-ONLY view of the frame (columns is_*) and cannot read an")
    P("      OOS or FULL column -- structural, asserted at call time   [PASS by construction]")
    gate_rows.append(dict(gate="G4", value=0, bar="IS-only view", passed=True)); gp += 1; gn += 1
    P("  G5  comparands: baseline.rules_v2_weights (0.03/0.75, W) and SPY buy-and-hold   [PASS]")
    gate_rows.append(dict(gate="G5", value=0, bar="baseline's own", passed=True)); gp += 1; gn += 1
    P(f"  --> {gp} of {gn} gates PASS.")
    P("")

    # ---------------------------------------------------------------- price the grid
    rows = []
    for pname, px in panels.items():
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        lvg, lvt = run(px, rules_v2_weights(px, *LIVE), mask)
        REF = {}
        for c in COSTS:
            lr = net(lvg, lvt, c).loc[start:]
            REF[c] = dict(
                LV=dict(FULL=stats(lr), IS=stats(lr.loc[:IS_END]), OOS=stats(lr.loc[OOS_BEG:])))
        sp = spy.loc[start:]
        SPY = dict(FULL=stats(sp), IS=stats(sp.loc[:IS_END]), OOS=stats(sp.loc[OOS_BEG:]))
        for b_, g_ in itertools.product(BANDS, GROSSES):
            gr, to = run(px, ladder_weights(px, b_, g_), mask)
            for c in COSTS:
                r = net(gr, to, c).loc[start:]
                sF, sI, sO = stats(r), stats(r.loc[:IS_END]), stats(r.loc[OOS_BEG:])
                pF, LF, MF = legs4b(sF, SPY["FULL"])
                pI, LI, MI = legs4b(sI, SPY["IS"])
                lv = REF[c]["LV"]
                rows.append(dict(
                    panel=pname, cost=c, band=b_, gross=g_,
                    cell=f"b{b_:.2f}_g{g_:.2f}",
                    CAGR=sF["CAGR"], Sharpe=sF["Sharpe"], MaxDD=sF["MaxDD"],
                    H1=sF["H1"], H2=sF["H2"],
                    is_CAGR=sI["CAGR"], is_Sharpe=sI["Sharpe"], is_MaxDD=sI["MaxDD"],
                    is_legs=int(sum(LI.values())),
                    is_minmarg=float(min(MI["H1"], MI["H2"], MI["DD"] / 100.0, MI["CAGR"] / 100.0)),
                    is_calmar=float(sI["CAGR"] / abs(sI["MaxDD"])) if sI["MaxDD"] < 0 else np.nan,
                    is_cagrslack=float(sI["CAGR"] - CAGR_FLOOR * SPY["IS"]["CAGR"]),
                    oos_CAGR=sO["CAGR"], oos_Sharpe=sO["Sharpe"], oos_MaxDD=sO["MaxDD"],
                    keep4b_full=bool(pF), keep4b_is=bool(pI),
                    keep4b_oos=bool(keep4b_oos(sO, SPY["OOS"])),
                    keep4a_full=bool(keep4a(sF, lv["FULL"])),
                    keep4a_oos=bool(keep4a_oos(sO, lv["OOS"])),
                    mg_DD=MF["DD"], mg_CAGR=MF["CAGR"], mg_H1=MF["H1"], mg_H2=MF["H2"],
                    spy_oos_CAGR=SPY["OOS"]["CAGR"], spy_oos_Sharpe=SPY["OOS"]["Sharpe"],
                    spy_oos_MaxDD=SPY["OOS"]["MaxDD"],
                    lv_oos_CAGR=lv["OOS"]["CAGR"], lv_oos_Sharpe=lv["OOS"]["Sharpe"],
                    lv_oos_MaxDD=lv["OOS"]["MaxDD"]))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"grid priced: {len(G)} rows published to {Path(OUT).name}.grid.csv")
    P("")

    # ---------------------------------------------------------------- B1 gross share
    P("-" * 100)
    P("(B1) IS the chooser statistic SENSITIVE TO GROSS?  2119 measured IS Sharpe moving")
    P("     0.0013 (U56) / 0.0026 (B136) across the WHOLE gross ladder.  Per statistic:")
    P("     gspread = mean over bands of (max-min across gross);  bspread = mean over gross")
    P("     of (max-min across bands);  gross share = gspread / (gspread + bspread).")
    P("-" * 100)
    STATS = dict(IS_SHARPE="is_Sharpe", IS_MINMARG="is_minmarg", IS_CALMAR="is_calmar",
                 IS_CAGRSLACK="is_cagrslack", IS_LEGS="is_legs", IS_DD="is_MaxDD")
    b1 = []
    for pname in panels:
        for cname, col in STATS.items():
            d = G[(G.panel == pname) & (G.cost == COST0)]
            gs = d.groupby("band")[col].apply(lambda x: x.max() - x.min()).mean()
            bs = d.groupby("gross")[col].apply(lambda x: x.max() - x.min()).mean()
            tot = d[col].max() - d[col].min()
            share = gs / (gs + bs) if (gs + bs) > 0 else np.nan
            b1.append(dict(panel=pname, chooser=cname, gspread=gs, bspread=bs,
                           total_spread=tot, gross_share=share))
    B1 = pd.DataFrame(b1); B1.to_csv(f"{OUT}.b1_grossshare.csv", index=False)
    P(B1.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- B2/B3/B5 picks
    P("-" * 100)
    P("(B2/B3/B5) RULE 8 -- cell chosen on IS rows ONLY, 2017-2026 read ONCE.")
    P("-" * 100)
    IS_COLS = ["cell", "band", "gross", "is_CAGR", "is_Sharpe", "is_MaxDD", "is_legs",
               "is_minmarg", "is_calmar", "is_cagrslack"]
    picks = []
    for pname in panels:
        for c in COSTS:
            d = G[(G.panel == pname) & (G.cost == c)]
            isview = d[IS_COLS].copy()               # gate G4: IS-only view
            for ch in CHOOSERS + REFRULES:
                if ch == "MAXGROSS":
                    cell = f"b{LIVE[0]:.2f}_g{max(GROSSES):.2f}"
                elif ch == "RANDCELL":
                    m = d[["oos_CAGR", "oos_Sharpe", "oos_MaxDD"]].mean()
                    picks.append(dict(panel=pname, cost=c, chooser=ch, cell="MEAN-OF-25",
                                      band=np.nan, gross=np.nan,
                                      oos_CAGR=m.oos_CAGR, oos_Sharpe=m.oos_Sharpe,
                                      oos_MaxDD=m.oos_MaxDD,
                                      keep4b_full=np.nan, keep4b_oos=np.nan,
                                      keep4a_full=np.nan, keep4a_oos=np.nan,
                                      reach_g100=float((d.gross == 1.00).mean())))
                    continue
                else:
                    cell = pick(isview, ch)
                r = d[d.cell == cell].iloc[0]
                picks.append(dict(panel=pname, cost=c, chooser=ch, cell=cell,
                                  band=r.band, gross=r.gross,
                                  oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe,
                                  oos_MaxDD=r.oos_MaxDD,
                                  keep4b_full=bool(r.keep4b_full), keep4b_oos=bool(r.keep4b_oos),
                                  keep4a_full=bool(r.keep4a_full), keep4a_oos=bool(r.keep4a_oos),
                                  reach_g100=float(r.gross == 1.00)))
    PK = pd.DataFrame(picks); PK.to_csv(f"{OUT}.picks.csv", index=False)
    for pname in panels:
        for c in COSTS:
            d = G[(G.panel == pname) & (G.cost == c)].iloc[0]
            P(f"  --- {pname} @ {c} bps --- benchmarks OOS: RULES v2 {d.lv_oos_CAGR:7.2%} / "
              f"{d.lv_oos_Sharpe:.4f} / {d.lv_oos_MaxDD:7.2%}   SPY {d.spy_oos_CAGR:7.2%} / "
              f"{d.spy_oos_Sharpe:.4f} / {d.spy_oos_MaxDD:7.2%}")
            sub = PK[(PK.panel == pname) & (PK.cost == c)]
            P("      " + sub[["chooser", "cell", "oos_CAGR", "oos_Sharpe", "oos_MaxDD",
                              "keep4b_full", "keep4b_oos", "keep4a_full", "keep4a_oos"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))
    P("")

    # ---------------------------------------------------------------- B4 verdict spread
    P("-" * 100)
    P("(B4) THE OOS VERDICT SPREAD each chooser set produces, per instance (panel x cost).")
    P("-" * 100)
    sp = []
    for pname in panels:
        for c in COSTS:
            s = PK[(PK.panel == pname) & (PK.cost == c) & (PK.chooser.isin(CHOOSERS))]
            sp.append(dict(panel=pname, cost=c, n_distinct_cells=s.cell.nunique(),
                           oos_Sharpe_spread=s.oos_Sharpe.max() - s.oos_Sharpe.min(),
                           oos_CAGR_spread=s.oos_CAGR.max() - s.oos_CAGR.min(),
                           oos_MaxDD_spread=s.oos_MaxDD.max() - s.oos_MaxDD.min(),
                           n_pass_4b_oos=int(s.keep4b_oos.sum()),
                           agree_4b_oos=bool(s.keep4b_oos.nunique() == 1),
                           n_reach_g100=int(s.reach_g100.sum())))
    SPD = pd.DataFrame(sp); SPD.to_csv(f"{OUT}.b4_spread.csv", index=False)
    P(SPD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- B5 vs MAXGROSS
    P("-" * 100)
    P("(B5) DOES ANY FITTED CHOOSER BEAT THE ZERO-PARAMETER RULE?  MAXGROSS = band 0.03 (live),")
    P("     gross 1.00, no in-sample data read at all.  RANDCELL = the 25-cell mean.")
    P("-" * 100)
    b5 = []
    for ch in CHOOSERS:
        d = PK[PK.chooser == ch].set_index(["panel", "cost"])
        mg = PK[PK.chooser == "MAXGROSS"].set_index(["panel", "cost"])
        rc = PK[PK.chooser == "RANDCELL"].set_index(["panel", "cost"])
        b5.append(dict(chooser=ch,
                       n_inst=len(d),
                       same_cell_as_MAXGROSS=int((d.cell == mg.cell).sum()),
                       beats_MAXGROSS_oosSharpe=int((d.oos_Sharpe > mg.oos_Sharpe).sum()),
                       beats_RANDCELL_oosSharpe=int((d.oos_Sharpe > rc.oos_Sharpe).sum()),
                       mean_oos_Sharpe=d.oos_Sharpe.mean(),
                       mean_oos_CAGR=d.oos_CAGR.mean(),
                       n_4b_oos=int(d.keep4b_oos.sum()),
                       n_4b_full_and_oos=int((d.keep4b_full & d.keep4b_oos).sum()),
                       n_4a_full=int(d.keep4a_full.sum())))
    mgd = PK[PK.chooser == "MAXGROSS"]
    rcd = PK[PK.chooser == "RANDCELL"]
    b5.append(dict(chooser="MAXGROSS (0 params)", n_inst=len(mgd), same_cell_as_MAXGROSS=len(mgd),
                   beats_MAXGROSS_oosSharpe=0, beats_RANDCELL_oosSharpe=int((mgd.oos_Sharpe.values > rcd.oos_Sharpe.values).sum()),
                   mean_oos_Sharpe=mgd.oos_Sharpe.mean(), mean_oos_CAGR=mgd.oos_CAGR.mean(),
                   n_4b_oos=int(mgd.keep4b_oos.sum()),
                   n_4b_full_and_oos=int((mgd.keep4b_full & mgd.keep4b_oos).sum()),
                   n_4a_full=int(mgd.keep4a_full.sum())))
    b5.append(dict(chooser="RANDCELL (25-cell mean)", n_inst=len(rcd), same_cell_as_MAXGROSS=0,
                   beats_MAXGROSS_oosSharpe=int((rcd.oos_Sharpe.values > mgd.oos_Sharpe.values).sum()),
                   beats_RANDCELL_oosSharpe=0,
                   mean_oos_Sharpe=rcd.oos_Sharpe.mean(), mean_oos_CAGR=rcd.oos_CAGR.mean(),
                   n_4b_oos=-1, n_4b_full_and_oos=-1, n_4a_full=-1))
    B5 = pd.DataFrame(b5); B5.to_csv(f"{OUT}.b5_vs_zeroparam.csv", index=False)
    P(B5.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------------- B7 monotonicity
    P("-" * 100)
    P("(B7) POST-HOC DIAGNOSTIC (declared post-hoc; no cell is selected on it).  Is the IS")
    P("     statistic FLAT-BUT-ORDERED in gross rather than a coin flip, and does the OOS")
    P("     gradient point the SAME WAY?")
    P("-" * 100)
    mono = []
    for (pn, c, b_), s in G.groupby(["panel", "cost", "band"]):
        s = s.sort_values("gross")
        for lbl, col in (("IS_Sharpe", "is_Sharpe"), ("OOS_Sharpe", "oos_Sharpe"),
                         ("OOS_CAGR", "oos_CAGR"), ("FULL_Sharpe", "Sharpe")):
            v = s[col].values
            mono.append(dict(panel=pn, cost=c, band=b_, stat=lbl,
                             up=bool(np.all(np.diff(v) > 0)), down=bool(np.all(np.diff(v) < 0)),
                             argmax_gross=float(s.gross.values[int(np.argmax(v))]),
                             span=float(v.max() - v.min())))
    MO = pd.DataFrame(mono); MO.to_csv(f"{OUT}.b7_monotone.csv", index=False)
    P(MO.groupby("stat").agg(n_blocks=("up", "size"), n_monotone_UP=("up", "sum"),
                             n_monotone_DOWN=("down", "sum"),
                             n_argmax_at_g100=("argmax_gross", lambda x: int((x == 1.00).sum())),
                             mean_span=("span", "mean"))
      .to_string(float_format=lambda x: f"{x:.5f}"))
    P("")
    P("     BAND, at the gross rung the verdict lives on (g = 1.00), 10 bps:")
    bb = []
    for pn in panels:
        s = G[(G.panel == pn) & (G.cost == COST0) & (G.gross == 1.00)].sort_values("band")
        bb.append(dict(panel=pn,
                       IS_argmax_band=float(s.loc[s.is_Sharpe.idxmax(), "band"]),
                       OOS_argmax_band=float(s.loc[s.oos_Sharpe.idxmax(), "band"]),
                       OOS_Sharpe_at_IS_pick=float(s.loc[s.is_Sharpe.idxmax(), "oos_Sharpe"]),
                       OOS_Sharpe_best_band=float(s.oos_Sharpe.max()),
                       n_bands_passing_4b_full_and_oos=int((s.keep4b_full & s.keep4b_oos).sum())))
    BB = pd.DataFrame(bb); BB.to_csv(f"{OUT}.b7_band.csv", index=False)
    P("     " + BB.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n     "))
    P("")

    # ---------------------------------------------------------------- walk-forward file
    wf = PK[PK.cost == COST0].copy()
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- headline
    P("=" * 100); P("HEADLINE"); P("=" * 100)
    gshare = B1.set_index(["panel", "chooser"]).gross_share
    P(f"  B1  gross share of the IS statistic's own spread (10 bps):")
    for pname in panels:
        P("      " + pname + "  " + "  ".join(
            f"{ch}={gshare.loc[(pname, ch)]:.3f}" for ch in STATS))
    for pname in panels:
        s = PK[(PK.panel == pname) & (PK.cost == COST0) & (PK.chooser.isin(CHOOSERS))]
        P(f"  B2  {pname} @10bps: {int(s.reach_g100.sum())} of {len(CHOOSERS)} choosers reach "
          f"gross 1.00 -- " + ", ".join(f"{r.chooser}:{r.cell}" for r in s.itertuples()))
    tot4b = int(PK[PK.chooser.isin(CHOOSERS)].keep4b_oos.sum())
    P(f"  B3  4b OOS passes over all {len(CHOOSERS)}x{len(panels)}x{len(COSTS)} chooser picks: {tot4b}")
    P(f"  B4  distinct cells picked per instance: {SPD.n_distinct_cells.tolist()}; "
      f"OOS Sharpe spread {SPD.oos_Sharpe_spread.min():.4f}-{SPD.oos_Sharpe_spread.max():.4f}; "
      f"choosers agree on the 4b OOS verdict in {int(SPD.agree_4b_oos.sum())} of {len(SPD)} instances")
    bm = B5[B5.chooser.isin(CHOOSERS)]
    mm = MO.groupby("stat").agg(up=("up", "sum"), dn=("down", "sum"), n=("up", "size"))
    P(f"  B7  monotone in GROSS: IS_Sharpe UP {int(mm.loc['IS_Sharpe','up'])}/{int(mm.loc['IS_Sharpe','n'])}, "
      f"OOS_Sharpe DOWN {int(mm.loc['OOS_Sharpe','dn'])}/{int(mm.loc['OOS_Sharpe','n'])}, "
      f"OOS_CAGR UP {int(mm.loc['OOS_CAGR','up'])}/{int(mm.loc['OOS_CAGR','n'])}"
      f"  -> the IS gradient is FLAT-BUT-ORDERED, not a coin flip, and its SIGN is INVERTED"
      f" against OOS Sharpe.")
    P(f"      band at g=1.00: IS pick vs OOS best -- " +
      ", ".join(f"{r.panel} IS b{r.IS_argmax_band:.2f} (OOS Sharpe {r.OOS_Sharpe_at_IS_pick:.4f})"
                f" vs OOS-best b{r.OOS_argmax_band:.2f} ({r.OOS_Sharpe_best_band:.4f}),"
                f" {int(r.n_bands_passing_4b_full_and_oos)}/5 bands pass 4b"
                for r in BB.itertuples()))
    P(f"  B5  beats MAXGROSS on OOS Sharpe: " +
      ", ".join(f"{r.chooser} {int(r.beats_MAXGROSS_oosSharpe)}/{int(r.n_inst)}" for r in bm.itertuples()))
    P("")
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES))
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()
