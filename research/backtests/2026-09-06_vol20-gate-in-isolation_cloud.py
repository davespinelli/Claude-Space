#!/usr/bin/env python3
"""Idea 56 - "vol20-gate-in-isolation".

The question
------------
Idea 38 decomposed RULES v1's two-clause eligibility gate on the SMALL panel at n=40 and
found the `vol20 < 0.60` half is the larger destroyer there (no gate 0.797 Sharpe, 200d
only 0.693, vol20 only 0.524, both 0.441).  The same clause has never been tested ALONE
on research/universe.json, where it is simply assumed to be part of the edge.  This run
does the 4-way decomposition at idea 2's KEEP-candidate construction, on both large-cap
universes.

  NONE   no eligibility gate at all - rank the composite over every priced name
  MA200  px > 200d moving average only
  VOL20  20d realised vol (annualised) < 0.60 only
  BOTH   RULES v1's gate, unchanged

Construction (idea 2's candidate, held fixed)
    composite score of research/scan.py with NO vol scaler, top n equal-weighted at 75%
    gross, weekly rebalancing, 10 bps per unit turnover, weights decided at close t and
    applied at t+1.  Universes: universe.json (U56) and universe_broad.json (B136).

Tuned parameters (PROTOCOL rule 4: at most two)
    1. gate in {NONE, MA200, VOL20, BOTH}       2. n in {5, 10, 20}
Two further axes are REPORTED DECOMPOSITIONS, never selected on - every cell is printed
for both and the rule-8 selection runs strictly INSIDE each (universe, convention) cell:
    universe    U56 / B136          (the idea asks for both)
    convention  dg = de-gross (hold gross/n each; gated-out weight goes to CASH, which is
                     the live convention) vs rw = re-spread (always deploy 75% across
                     however many names survive the gate).
    The dg/rw contrast is the whole point of the decomposition: a gate can help by
    CHOOSING better names (visible under rw) or by moving to CASH at the right time
    (visible only as the dg-minus-rw difference).  Reporting only one of them cannot tell
    the two apart, which is how a clause can look like "part of the edge" without being it.

Grid = 4 gates x 3 n x 2 universes x 2 conventions = 48 book cells, ALL reported,
plus RULES v2 (live), RULES v1 and SPY on each universe.

Rule 8 walk-forward: choose (gate, n) on <= 2016 by in-sample Sharpe inside each
(universe, convention), then read 2017-2026 once.  Reported against SPY, RULES v2, the
pre-registered anchor (BOTH, n=20 - idea 2's candidate) and the best OOS cell (regret).

Both KEEP paths (4a vs live RULES v2, 4b vs SPY) are evaluated on every cell.

Outputs: .grid.csv, .walkforward.csv, .console.txt, .result.md
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GATES = ["NONE", "MA200", "VOL20", "BOTH"]
NS = [5, 10, 20]
CONVS = ["dg", "rw"]
ANCHOR = ("BOTH", 20)                      # idea 2's candidate, pre-registered

def gate_mask(px, mode):
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    if mode == "NONE":  return px.notna()
    if mode == "MA200": return above
    if mode == "VOL20": return vol20 < 0.60
    if mode == "BOTH":  return above & (vol20 < 0.60)
    raise ValueError(mode)

def book(mode, n, conv):
    def f(px):
        tr = [c for c in px.columns if c != "SPY"]
        sub = px[tr]
        s, _, _ = score(sub, vol_scale=False)
        elig = s.where(gate_mask(sub, mode))
        sel = elig.rank(axis=1, ascending=False) <= n
        if conv == "dg":
            w = sel.astype(float) * (GROSS / n)
        else:
            cnt = sel.sum(axis=1)
            w = sel.astype(float).div(cnt.replace(0, np.nan), axis=0) * GROSS
        return w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    return f

def v2_book(px):
    tr = [c for c in px.columns if c != "SPY"]
    return rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)

def v1_book(px):
    tr = [c for c in px.columns if c != "SPY"]
    return rules_v1_weights(px[tr]).reindex(columns=px.columns).fillna(0.0)

def st(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def row_of(r):
    h = len(r) // 2
    c, s, d = st(r)
    oc, os_, od = st(r, OOS_START)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=metrics(r.iloc[:h])["Sharpe"],
                H2=metrics(r.iloc[h:])["Sharpe"], IS_Sharpe=st(r, None, IS_END)[1],
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)

def keep_paths(x, spy, v2):
    a = (x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])
    b = (x["H1"] > spy["H1"] and x["H2"] > spy["H2"] and x["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and x["MaxDD"] >= 0.60 * spy["MaxDD"] and x["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)

def first_failing_4b(x, spy):
    for lbl, ok in (("H1", x["H1"] > spy["H1"]), ("H2", x["H2"] > spy["H2"]),
                    ("OOS", x["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                    ("DD", x["MaxDD"] >= 0.60 * spy["MaxDD"]),
                    ("CAGR", x["CAGR"] >= 0.70 * spy["CAGR"])):
        if not ok: return lbl
    return "-"

def main():
    unis = {"U56": load_universe(), "B136": load_universe(broad=True)}
    rows, refs = [], {}
    for uname, px in unis.items():
        px = px.dropna(how="all").ffill()
        start = px.index[260]
        P(f"\n{'='*92}\n{uname}: {px.shape[1]-1} tradables + SPY, {px.index[0].date()} .. {px.index[-1].date()},"
          f" scored from {start.date()}\n{'='*92}")
        spy = row_of(px["SPY"].pct_change().fillna(0).loc[start:])
        v2 = row_of(backtest(px, v2_book(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:])
        v1 = row_of(backtest(px, v1_book(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:])
        refs[uname] = dict(SPY=spy, v2=v2, v1=v1)
        for tag, x in (("SPY", spy), ("RULES v2 (live)", v2), ("RULES v1", v1)):
            P(f"  {tag:16s} CAGR {x['CAGR']:6.2%}  Sharpe {x['Sharpe']:.3f}  MaxDD {x['MaxDD']:7.2%}"
              f"  H1/H2 {x['H1']:.3f}/{x['H2']:.3f}  OOS {x['OOS_CAGR']:6.2%}/{x['OOS_Sharpe']:.3f}/{x['OOS_MaxDD']:7.2%}")
        P(f"  4b bars on {uname}: Sharpe > SPY in both halves and OOS, MaxDD >= {0.60*spy['MaxDD']:.2%},"
          f" CAGR >= {0.70*spy['CAGR']:.2%}")

        for conv in CONVS:
            P(f"\n-- {uname} / convention {conv} "
              f"({'de-gross to cash' if conv=='dg' else 're-spread 75% over survivors'}) --")
            P(f"{'gate':6s} {'n':>3s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s}"
              f" {'IS_S':>6s} {'OOS_S':>6s} {'OOS_DD':>8s} {'turn/yr':>8s} {'gross':>6s} {'4a':>4s} {'4b':>4s} {'fail4b':>7s}")
            for mode in GATES:
                for n in NS:
                    res = backtest(px, book(mode, n, conv)(px), cost_bps=COST, freq=FREQ)
                    r = res["returns"].loc[start:]
                    x = row_of(r)
                    turn = res["turnover"].loc[start:].sum() / (len(r) / 252)
                    gross = res["weights"].loc[start:].sum(axis=1).mean()
                    a, b = keep_paths(x, spy, v2)
                    fb = first_failing_4b(x, spy)
                    rows.append(dict(universe=uname, conv=conv, gate=mode, n=n, **x,
                                     turnover_yr=turn, mean_gross=gross, pass4a=a, pass4b=b,
                                     first_fail_4b=fb, spy_S=spy["Sharpe"], spy_CAGR=spy["CAGR"],
                                     spy_DD=spy["MaxDD"], spy_OOS_S=spy["OOS_Sharpe"],
                                     v2_S=v2["Sharpe"], v2_OOS_S=v2["OOS_Sharpe"]))
                    P(f"{mode:6s} {n:3d} {x['CAGR']:7.2%} {x['Sharpe']:7.3f} {x['MaxDD']:8.2%}"
                      f" {x['H1']:6.3f} {x['H2']:6.3f} {x['IS_Sharpe']:6.3f} {x['OOS_Sharpe']:6.3f}"
                      f" {x['OOS_MaxDD']:8.2%} {turn:8.2f} {gross:6.3f} {str(a):>4s} {str(b):>4s} {fb:>7s}")
    grid = pd.DataFrame(rows); grid.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- isolate the two clauses
    P(f"\n{'='*92}\nCLAUSE ISOLATION: what each half of the gate does to Sharpe, vs NONE\n{'='*92}")
    for uname in unis:
        for conv in CONVS:
            s = grid[(grid.universe == uname) & (grid.conv == conv)].set_index(["gate", "n"])
            P(f"\n  {uname} / {conv}   dSharpe vs NONE at the same n")
            P(f"    {'n':>3s} {'NONE':>7s} {'MA200':>8s} {'VOL20':>8s} {'BOTH':>8s}   "
              f"{'dMaxDD MA200':>12s} {'dMaxDD VOL20':>12s} {'dMaxDD BOTH':>12s}")
            for n in NS:
                b0 = s.loc[("NONE", n)]
                P(f"    {n:3d} {b0.Sharpe:7.3f} " + " ".join(
                    f"{s.loc[(g,n)].Sharpe-b0.Sharpe:+8.3f}" for g in GATES[1:]) + "   " + " ".join(
                    f"{s.loc[(g,n)].MaxDD-b0.MaxDD:+12.2%}" for g in GATES[1:]))

    P("\n  SELECTION vs CASH-TIMING: rw isolates name selection (gross always 75%);")
    P("  (dg - rw) at the same (gate, n) is what the clause earns purely by holding CASH.")
    for uname in unis:
        d = grid[grid.universe == uname]
        P(f"\n  {uname}   {'gate':6s} {'n':>3s} {'rw dS vs NONE':>14s} {'dg dS vs NONE':>14s}"
          f" {'cash effect (dg-rw)':>20s} {'dg mean gross':>14s}")
        for mode in GATES[1:]:
            for n in NS:
                rw = d[(d.conv == "rw") & (d.gate == mode) & (d.n == n)].iloc[0]
                dg = d[(d.conv == "dg") & (d.gate == mode) & (d.n == n)].iloc[0]
                rw0 = d[(d.conv == "rw") & (d.gate == "NONE") & (d.n == n)].iloc[0]
                dg0 = d[(d.conv == "dg") & (d.gate == "NONE") & (d.n == n)].iloc[0]
                P(f"  {'':6s} {mode:6s} {n:3d} {rw.Sharpe-rw0.Sharpe:+14.3f}"
                  f" {dg.Sharpe-dg0.Sharpe:+14.3f} {(dg.Sharpe-dg0.Sharpe)-(rw.Sharpe-rw0.Sharpe):+20.3f}"
                  f" {dg.mean_gross:14.3f}")

    # ---------------- KEEP tallies
    P(f"\n{'='*92}\nKEEP PATHS over all 48 cells\n{'='*92}")
    P(f"  4a passes {int(grid.pass4a.sum())}/{len(grid)}   4b passes {int(grid.pass4b.sum())}/{len(grid)}")
    if grid.pass4b.any():
        P("  4b passers:")
        P(grid[grid.pass4b][["universe", "conv", "gate", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                             "OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("  first-failing 4b bar, counts: " + ", ".join(
        f"{k} {v}" for k, v in grid.first_fail_4b.value_counts().items()))

    # ---------------- rule 8
    P(f"\n{'='*92}\nRULE 8 WALK-FORWARD: choose (gate, n) on <= 2016, read 2017-2026 once\n{'='*92}")
    w = []
    for uname in unis:
        for conv in CONVS:
            s = grid[(grid.universe == uname) & (grid.conv == conv)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            best = s.loc[s.OOS_Sharpe.idxmax()]
            anc = s[(s.gate == ANCHOR[0]) & (s.n == ANCHOR[1])].iloc[0]
            spy, v2 = refs[uname]["SPY"], refs[uname]["v2"]
            w.append(dict(universe=uname, conv=conv, pick_gate=pick.gate, pick_n=int(pick.n),
                          IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                          OOS_MaxDD=pick.OOS_MaxDD, anchor_gate=ANCHOR[0], anchor_n=ANCHOR[1],
                          anchor_OOS_Sharpe=anc.OOS_Sharpe, anchor_OOS_CAGR=anc.OOS_CAGR,
                          edge_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                          best_gate=best.gate, best_n=int(best.n), best_OOS_Sharpe=best.OOS_Sharpe,
                          regret=pick.OOS_Sharpe - best.OOS_Sharpe, spy_OOS_Sharpe=spy["OOS_Sharpe"],
                          spy_OOS_CAGR=spy["OOS_CAGR"], spy_OOS_MaxDD=spy["OOS_MaxDD"],
                          v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"]))
            P(f"  {uname}/{conv}: IS pick {pick.gate}/n={int(pick.n)} (IS {pick.IS_Sharpe:.3f})"
              f" -> OOS {pick.OOS_CAGR:6.2%}/{pick.OOS_Sharpe:.3f}/{pick.OOS_MaxDD:7.2%}"
              f" | anchor {ANCHOR[0]}/n={ANCHOR[1]} OOS {anc.OOS_CAGR:6.2%}/{anc.OOS_Sharpe:.3f}"
              f" (edge {pick.OOS_Sharpe-anc.OOS_Sharpe:+.3f})"
              f" | best OOS {best.gate}/n={int(best.n)} {best.OOS_Sharpe:.3f} (regret {pick.OOS_Sharpe-best.OOS_Sharpe:+.3f})"
              f" | SPY {spy['OOS_CAGR']:6.2%}/{spy['OOS_Sharpe']:.3f}  v2 {v2['OOS_Sharpe']:.3f}")
    wf = pd.DataFrame(w); wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\n  the IS chooser picks a gate CONTAINING vol20 in "
      f"{int(wf.pick_gate.isin(['VOL20','BOTH']).sum())} of {len(wf)} cells;"
      f" it beats SPY OOS in {int((wf.OOS_Sharpe > wf.spy_OOS_Sharpe).sum())}/{len(wf)}"
      f" and the live RULES v2 OOS in {int((wf.OOS_Sharpe > wf.v2_OOS_Sharpe).sum())}/{len(wf)}")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
