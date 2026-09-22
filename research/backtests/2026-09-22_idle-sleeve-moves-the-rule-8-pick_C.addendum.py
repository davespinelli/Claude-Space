#!/usr/bin/env python3
"""Idea 2217 addendum (lane C, 2026-09-22): re-reads the committed grid of
`2026-09-22_idle-sleeve-moves-the-rule-8-pick_C.py` and prints the three follow-on reads the
memo cites.  Adds NO new backtest and NO new tuned parameter -- it is a pure re-read.
  (1) the LIVE cell (band 0.03, gross 0.75) under every sleeve arm, all three windows;
  (2) 4a / 4b robustness of the phi=0.00 T-bill sweep across weekday offset x cost;
  (3) where the IS Sharpe -> gross slope changes sign as phi rises (the crossover).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SLUG = "2026-09-22_idle-sleeve-moves-the-rule-8-pick_C"
OUT = ROOT / "research" / "backtests"
GROSSES = [0.50, 0.625, 0.75, 0.875, 1.00]
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08]
LAD = ["NOSLV", "phi0.00", "phi0.25", "phi0.50", "phi0.75", "phi1.00"]

df = pd.read_csv(OUT / f"{SLUG}.grid.csv.gz")
L = df[df.arm.isin(LAD)].copy()

print("########## (1) THE LIVE CELL band 0.03 / gross 0.75 UNDER EVERY ARM (d=0, 10 bps) ##########")
print("   (NOSLV at this cell IS the live RULES v2 book; every other row is that same book with")
print("    its idle NAV swept into phi*SPY + (1-phi)*SHY instead of 0% cash.)")
for pan in ["U56", "B136"]:
    for wn in ["FULL", "IS", "OOS"]:
        print(f"-- {pan} {wn} --")
        for arm in LAD:
            x = L[(L.panel == pan) & (L.arm == arm) & (L.band == 0.03) & (L.gross == 0.75)
                  & (L.offset == 0) & (L.cost == 10.0) & (L.window == wn)]
            if not len(x): continue
            r = x.iloc[0]
            print(f"   {arm:8s} CAGR {r.CAGR:7.2%}  Sharpe {r.Sharpe:.4f}  MaxDD {r.MaxDD:7.2%}  "
                  f"halves {r.H1:.4f}/{r.H2:.4f}  4a={bool(r.keep4a)} 4b={bool(r.keep4b)} "
                  f"legs H1={bool(r.leg_H1)} H2={bool(r.leg_H2)} DD={bool(r.leg_DD)} CAGR={bool(r.leg_CAGR)}")

print("\n########## (2) 4a ROBUSTNESS OF THE phi=0.00 T-BILL SWEEP (offset x cost) ##########")
for pan in ["U56", "B136"]:
    for cell, (c, g) in (("LIVE c0.03_g0.75", (0.03, 0.75)),
                         ("C1 pick c0.08_g0.50", (0.08, 0.50))):
        x = L[(L.panel == pan) & (L.arm == "phi0.00") & (L.band == c) & (L.gross == g)]
        t = x.pivot_table(index=["window", "cost"], columns="offset", values="keep4a").astype(int)
        print(f"-- {pan} phi0.00 {cell}: 4a --"); print(t.to_string())
        t2 = x.pivot_table(index=["window", "cost"], columns="offset", values="keep4b").astype(int)
        print(f"-- {pan} phi0.00 {cell}: 4b --"); print(t2.to_string())

print("\n########## (3) WHERE THE IS SHARPE -> GROSS SLOPE CHANGES SIGN ##########")
h = L[(L.offset == 0) & (L.cost == 10.0) & (L.window == "IS")]
for pan in ["U56", "B136"]:
    for arm in LAD:
        x = h[(h.panel == pan) & (h.arm == arm)]
        sl = []
        for c in BANDS:
            y = x[x.band == c].set_index("gross").Sharpe.reindex(GROSSES).values
            sl.append(np.polyfit(GROSSES, y, 1)[0])
        print(f"  {pan:4s} {arm:8s} mean d(IS Sharpe)/d(gross) = {np.mean(sl):+.4f} "
              f"(per band {[f'{v:+.3f}' for v in sl]})")

print("\n########## (4) WHAT THE SLEEVE COSTS AND BUYS AT MATCHED CELL (mean over 25 cells) ##########")
for pan in ["U56", "B136"]:
    for wn in ["FULL", "OOS"]:
        base = L[(L.panel == pan) & (L.arm == "NOSLV") & (L.offset == 0) & (L.cost == 10.0) & (L.window == wn)]
        base = base.set_index(["band", "gross"])
        for arm in LAD[1:]:
            x = L[(L.panel == pan) & (L.arm == arm) & (L.offset == 0) & (L.cost == 10.0) & (L.window == wn)]
            x = x.set_index(["band", "gross"])
            print(f"  {pan:4s} {wn:4s} {arm:8s}  dCAGR {np.mean(x.CAGR - base.CAGR):+.2%}  "
                  f"dSharpe {np.mean(x.Sharpe - base.Sharpe):+.4f}  dMaxDD {np.mean(x.MaxDD - base.MaxDD):+.2%}")

print("\n########## (5) THE DECISIVE READ: 4a AGAINST AN IDLE-NAV-MATCHED INCUMBENT ##########")
print("   PROTOCOL 4a scores against the LIVE book, whose idle NAV earns 0%.  A sleeved candidate")
print("   therefore collects a cash credit its comparand is denied.  Re-score every phi=0.00 cell")
print("   against the LIVE CELL OF ITS OWN ARM (c0.03 / g0.75 / phi=0.00) -- same sweep on both")
print("   sides -- so only the band x gross choice is being priced.")
for pan in ["U56", "B136"]:
    for wn in ["FULL", "IS", "OOS"]:
        rows = []
        for off in sorted(L.offset.unique()):
            for cost in sorted(L.cost.unique()):
                a = L[(L.panel == pan) & (L.arm == "phi0.00") & (L.window == wn)
                      & (L.offset == off) & (L.cost == cost)]
                inc = a[(a.band == 0.03) & (a.gross == 0.75)].iloc[0]
                p = a[(a.band == 0.08) & (a.gross == 0.50)].iloc[0]
                rows.append(dict(offset=off, cost=cost,
                                 matched4a=bool(p.H1 > inc.H1 and p.H2 > inc.H2 and p.MaxDD >= inc.MaxDD),
                                 dH1=p.H1 - inc.H1, dH2=p.H2 - inc.H2, dDD=p.MaxDD - inc.MaxDD,
                                 dCAGR=p.CAGR - inc.CAGR))
        r = pd.DataFrame(rows)
        base = r[(r.offset == 0) & (r.cost == 10.0)].iloc[0]
        print(f"  {pan:4s} {wn:4s} c0.08_g0.50 vs SWEPT live cell: matched-4a {int(r.matched4a.sum())}/{len(r)} "
              f"(offset x cost) | at d=0/10bps dH1 {base.dH1:+.4f} dH2 {base.dH2:+.4f} "
              f"dMaxDD {base.dDD:+.2%} dCAGR {base.dCAGR:+.2%}")
        print(f"        matched-4a by cost 0/10/25/50: "
              f"{[int(r[(r.cost==c)].matched4a.sum()) for c in [0.0,10.0,25.0,50.0]]} of 5 offsets each")
