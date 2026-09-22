#!/usr/bin/env python3
"""Idea 2105 (lane C, 2026-09-22) — COMPANION VERIFICATION of the one cell this run's grid shows
clearing BOTH KEEP paths: B136 / TURNBUDGET / t = 0.08, B = 3.0.

It is priced here on the two ladders the record requires of any 4a claim (COST and EXECUTION
DELAY), against the LIVE RULES v2 book at the SAME cost and the SAME delay, and against SPY.
Nothing is tuned here: the cell, the panel and the family all come from the main script's grid.
Run after `2026-09-22_chooser-ensemble-vs-every-single-chooser_C.py`.
"""
import sys, importlib.util
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
MAIN = HERE / "2026-09-22_chooser-ensemble-vs-every-single-chooser_C.py"
spec = importlib.util.spec_from_file_location("ens2105", MAIN)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

OUT = HERE / "2026-09-22_chooser-ensemble-vs-every-single-chooser_C.verify"
CELL, TGT, BUD = "t=0.08|B=3.0", 0.08, 3.0
lines = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    lines.append(s)


px = M.load_universe(broad=True)
st = px.index[M.WARMUP]
S = M.spy_bars(px, st)
rows = []
log(f"# Idea 2105 companion — B136 / TURNBUDGET / {CELL} on the COST x DELAY ladder")
log(f"   SPY B136: FULL {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
    f"{S['full']['MaxDD']:.2%}   halves {S['h1']:.4f}/{S['h2']:.4f}   "
    f"OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%}")
log(f"   4b bars: CAGR floor {0.70*S['full']['CAGR']:.2%}, MaxDD cap "
    f"{0.60*S['full']['MaxDD']:.2%}\n")
for delay in (1, 2, 3):
    P = M.Panel(px, list(px.columns), delay=delay, hold_spy=True)
    r0, t0, gs = P.turnbudget(TGT, BUD)
    # live RULES v2 at the SAME delay, priced at each cost rung
    W = M.rules_v2_weights(px, 0.03, 0.75)
    lr0, lt0, _ = M.bt_sched(P.R, P._lag(W), P.mW)
    lr0 = pd.Series(lr0, index=px.index).loc[st:]
    lt0 = pd.Series(lt0, index=px.index).loc[st:]
    for c in M.COSTS_LADDER:
        r = M.net(r0.loc[st:], t0.loc[st:], c)
        lr = M.net(lr0, lt0, c)
        m, mo = M.mets(r), M.mets(r.loc[M.OOS_START:])
        h1, h2 = M.halves(r)
        lm, lmo = M.mets(lr), M.mets(lr.loc[M.OOS_START:])
        lh1, lh2 = M.halves(lr)
        k4b = (h1 > S["h1"] and h2 > S["h2"]
               and m["MaxDD"] >= 0.60 * S["full"]["MaxDD"]
               and m["CAGR"] >= 0.70 * S["full"]["CAGR"])
        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                and mo["MaxDD"] >= 0.60 * S["oos"]["MaxDD"]
                and mo["CAGR"] >= 0.70 * S["oos"]["CAGR"])
        k4a = (h1 > lh1 and h2 > lh2 and m["MaxDD"] >= lm["MaxDD"])
        k4ao = (mo["Sharpe"] > lmo["Sharpe"] and mo["MaxDD"] >= lmo["MaxDD"])
        rows.append(dict(delay=delay, cost=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                         MaxDD=m["MaxDD"], H1=h1, H2=h2, oos_CAGR=mo["CAGR"],
                         oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                         turn_py=float(t0.loc[st:].sum() / (len(r) / 252.0)),
                         gross_mean=float(gs.loc[st:].mean()),
                         live_Sharpe=lm["Sharpe"], live_H1=lh1, live_H2=lh2,
                         live_MaxDD=lm["MaxDD"], live_oos_Sharpe=lmo["Sharpe"],
                         keep4b_full=k4b, keep4b_oos=k4bo, keep4b=(k4b and k4bo),
                         keep4a=k4a, keep4a_oos=k4ao))
        log(f"   t+{delay}  {c:>2} bps  FULL {m['CAGR']:>7.2%}/{m['Sharpe']:>6.4f}/"
            f"{m['MaxDD']:>8.2%}  halves {h1:.4f}/{h2:.4f}  "
            f"OOS {mo['CAGR']:>7.2%}/{mo['Sharpe']:>6.4f}/{mo['MaxDD']:>8.2%}   "
            f"live {lm['Sharpe']:.4f} ({lh1:.4f}/{lh2:.4f}, {lm['MaxDD']:.2%})   "
            f"4b {str(k4b and k4bo):<5} 4a {str(k4a):<5} 4a_oos {k4ao}")
D = pd.DataFrame(rows)
D.to_csv(f"{OUT}.csv", index=False)
log(f"\n   turnover {D.turn_py.iloc[0]:.2f}x/yr, mean gross {D.gross_mean.iloc[0]:.3f}")
log(f"   4b holds on {int(D.keep4b.sum())} of {len(D)} (delay x cost) cells; "
    f"4a on {int(D.keep4a.sum())} of {len(D)}")
sub = D[D.delay == 1]
log(f"   at t+1: 4b {int(sub.keep4b.sum())}/{len(sub)} cost rungs, "
    f"4a {int(sub.keep4a.sum())}/{len(sub)}")
Path(f"{OUT}.log.txt").write_text("\n".join(lines) + "\n")
