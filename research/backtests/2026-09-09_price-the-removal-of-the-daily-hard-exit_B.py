#!/usr/bin/env python3
"""Idea 275 (lane B, 2026-09-09): price the removal of RULES v1's 'hard exit any day' clause.

RULES v2 clause 6 removes v1's daily hard exit on the grounds that no backtest in the record
ever priced it: every book in the corpus applies its weights on the rebalance schedule only,
so a name that leaves the gate on a Tuesday is sold on Friday.  This run builds the daily-exit
variant of BOTH books and prices the clause.

Mechanics (faithful to the engine's conventions):
  * weights decided at close t, applied at close t+1  (engine.backtest does this by shift(1))
  * the daily exit is a SELL ONLY: a held name whose exit trigger fires at close t is sold in
    full at close t+1 and the proceeds sit in cash; nothing is bought back until the next
    scheduled rebalance.  The book therefore de-grosses between rebalances, exactly like v2's
    OUT names do on a rebalance day.
  * every exit is charged 10 bps of the sold weight through the same turnover accumulator.

Two tuned parameters, both ladders reported in full:
  x  exit depth below the 200d MA at which a held name is dumped:  {0.00, 0.01, 0.03, 0.05, 0.10}
     x = 0.00 is the literal v1 clause (close below its own ma200).
     x = 0.03 under v2 is the literal restatement (sell the day the name leaves the band).
  c  confirmation days: consecutive closes below the trigger required before the exit fires,
     {1, 2, 3}.  c = 1 is the literal clause.

Corpus: 2 books (RULES v1, RULES v2) x 2 panels (U56, BROAD136) x 15 grid points, each against
its own no-daily-exit control, at 0 / 10 / 25 bps.  Rule 8 walk-forward: (x, c) chosen on
2009-2016 IS Sharpe, evaluated untouched on 2017-2026 against the live baseline and SPY.

Deterministic, standalone, no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (  # noqa: E402
    load_universe, rules_v1_weights, rules_v2_weights, score, band_state, metrics, backtest,
)
from engine import rebalance_mask  # noqa: E402

X_GRID = [0.00, 0.01, 0.03, 0.05, 0.10]
C_GRID = [1, 2, 3]
COST_RUNGS = [0.0, 10.0, 25.0]
FREQ = "W"
OOS_START = "2017-01-01"
IS_END = "2016-12-31"


# ---------------------------------------------------------------- backtester with a daily exit
def backtest_exit(prices, weights, exit_sig, cost_bps=10.0, freq="W"):
    """engine.backtest plus a sell-only daily exit.

    exit_sig: bool DataFrame, True at close t when a HELD name must be sold at close t+1.
              Pass None to disable (then this must reproduce engine.backtest exactly).
    """
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    if exit_sig is None:
        ex = pd.DataFrame(False, index=prices.index, columns=prices.columns)
    else:
        ex = exit_sig.reindex(prices.index).fillna(False).shift(1, fill_value=False).astype(bool)
    ex_v = ex.values
    held = np.zeros((len(prices), prices.shape[1]))
    cur = np.zeros(prices.shape[1])
    turnover = np.zeros(len(prices))
    r_v = rets.values
    wt_v = w_target.values
    mk = mask.values
    for i in range(len(prices)):
        if mk[i] or i == 0:
            new = np.nan_to_num(wt_v[i])
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        else:                                   # sell-only daily exit, never a buy
            hit = ex_v[i] & (cur > 0)
            if hit.any():
                turnover[i] += cur[hit].sum()
                cur = cur.copy()
                cur[hit] = 0.0
        held[i] = cur
        growth = cur * (1 + r_v[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    turnover = pd.Series(turnover, index=prices.index)
    held = pd.DataFrame(held, index=prices.index, columns=prices.columns)
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "turnover": turnover}


# ---------------------------------------------------------------- exit signals per book
def exit_signal_v1(px, x, c, max_vol=0.60):
    """v1 eligibility evaluated DAILY with the MA leg moved to ma200*(1-x); vol leg unchanged."""
    ma = px.rolling(200).mean()
    bad = (px < ma * (1 - x)) | (px.pct_change().rolling(20).std() * np.sqrt(252) >= max_vol)
    return _confirm(bad.fillna(False), c)


def exit_signal_v2(px, x, c):
    """v2 membership evaluated DAILY: sell once the close is x below its own ma200."""
    ma = px.rolling(200).mean()
    return _confirm((px < ma * (1 - x)).fillna(False), c)


def _confirm(bad, c):
    if c <= 1:
        return bad
    out = bad.copy()
    for k in range(1, c):
        out &= bad.shift(k).fillna(False)
    return out


BOOKS = {
    "v1": (lambda px: rules_v1_weights(px), exit_signal_v1),
    "v2": (lambda px: rules_v2_weights(px), exit_signal_v2),
}


# ---------------------------------------------------------------- metric helpers
def stats(r, turn=None, years=None):
    m = metrics(r)
    h = len(r) // 2
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
             H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    if turn is not None:
        d["Turn"] = turn.sum() / (len(turn) / 252)
    return d


def fmt(d):
    return (f"CAGR {d['CAGR']:6.2%}  Sharpe {d['Sharpe']:6.4f}  MaxDD {d['MaxDD']:7.2%}  "
            f"H1/H2 {d['H1']:.4f}/{d['H2']:.4f}" + (f"  turn {d['Turn']:.2f}x" if "Turn" in d else ""))


def main():
    print(__doc__)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}

    # ---------------- gate 1: the exit-disabled path must reproduce engine.backtest exactly
    print("\n" + "=" * 100)
    print("GATE 1 — backtest_exit(exit=None) vs engine.backtest, max abs return difference")
    for pname, px in panels.items():
        for bname, (wfn, _) in BOOKS.items():
            w = wfn(px)
            a = backtest_exit(px, w, None, cost_bps=10.0, freq=FREQ)["returns"]
            b = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"]
            print(f"  {pname:5s} {bname}: {np.abs(a - b).max():.3e}")

    # ---------------- gate 2: the live RULES v2 u56 row reproduces the published record
    px = panels["U56"]
    start = px.index[260]
    base = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    v1r = backtest(px, rules_v1_weights(px), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    print("\nGATE 2 — published RULES.md row is 8.66% / 1.2056 / -12.05%, halves 1.2259/1.1908")
    print(f"  v2 live   {fmt(stats(base))}")
    print(f"  v1 prev   {fmt(stats(v1r))}   (published 6.45% / 0.6642 / -13.83%)")
    print(f"  SPY       {fmt(stats(spy))}")

    # ---------------- the full grid, every point reported
    rows = []
    for pname, pxp in panels.items():
        s0 = pxp.index[260]
        for bname, (wfn, exfn) in BOOKS.items():
            w = wfn(pxp)
            ctl = {}
            for cb in COST_RUNGS:
                res = backtest_exit(pxp, w, None, cost_bps=cb, freq=FREQ)
                ctl[cb] = stats(res["returns"].loc[s0:], res["turnover"].loc[s0:])
            rows.append(dict(panel=pname, book=bname, x=np.nan, c=0, cost=10.0,
                             kind="control", **ctl[10.0]))
            for x in X_GRID:
                for c in C_GRID:
                    sig = exfn(pxp, x, c)
                    for cb in COST_RUNGS:
                        res = backtest_exit(pxp, w, sig, cost_bps=cb, freq=FREQ)
                        st = stats(res["returns"].loc[s0:], res["turnover"].loc[s0:])
                        rows.append(dict(panel=pname, book=bname, x=x, c=c, cost=cb,
                                         kind="exit", **st,
                                         dSharpe=st["Sharpe"] - ctl[cb]["Sharpe"],
                                         dMaxDD=st["MaxDD"] - ctl[cb]["MaxDD"],
                                         dCAGR=st["CAGR"] - ctl[cb]["CAGR"],
                                         dTurn=st["Turn"] - ctl[cb]["Turn"]))
    G = pd.DataFrame(rows)

    print("\n" + "=" * 100)
    print("FULL GRID at 10 bps — daily-exit arm minus its own no-exit control (same book/panel)")
    for pname in panels:
        for bname in BOOKS:
            sub = G[(G.panel == pname) & (G.book == bname) & (G.cost == 10.0)]
            ctlrow = sub[sub.kind == "control"].iloc[0]
            print(f"\n  {pname} / RULES {bname}  control: {fmt(ctlrow)}")
            print("    x      c   CAGR    Sharpe    MaxDD    H1      H2     turn   dSharpe  dMaxDD   dCAGR   dTurn")
            for _, r in sub[sub.kind == "exit"].iterrows():
                print(f"    {r.x:.2f}  {int(r.c)}  {r.CAGR:6.2%}  {r.Sharpe:7.4f}  {r.MaxDD:7.2%}  "
                      f"{r.H1:.3f}  {r.H2:.3f}  {r.Turn:5.2f}  {r.dSharpe:+7.4f}  {r.dMaxDD:+6.2%}  "
                      f"{r.dCAGR:+6.2%}  {r.dTurn:+5.2f}")

    print("\n" + "=" * 100)
    print("COST-RUNG SENSITIVITY of the clause (dSharpe of the daily-exit arm vs its control)")
    piv = G[G.kind == "exit"].pivot_table(index=["panel", "book"], columns="cost", values="dSharpe",
                                          aggfunc=["mean", "max", lambda s: (s > 0).mean()])
    print(piv.to_string(float_format=lambda v: f"{v:.4f}"))

    print("\nLITERAL CLAUSE (the wording v2 removed) at 10 bps:")
    print("  v1 literal = x 0.00 / c 1 (close below its own ma200, no confirmation)")
    print("  v2 literal = x 0.03 / c 1 (sell the day the name leaves the band)")
    for pname in panels:
        for bname, xlit in (("v1", 0.00), ("v2", 0.03)):
            sub = G[(G.panel == pname) & (G.book == bname) & (G.cost == 10.0)]
            ctl = sub[sub.kind == "control"].iloc[0]
            lit = sub[(sub.kind == "exit") & (np.isclose(sub.x, xlit)) & (sub.c == 1)].iloc[0]
            print(f"  {pname:5s} {bname}: control {fmt(ctl)}")
            print(f"            literal {fmt(lit)}")
            print(f"            worth   dSharpe {lit.dSharpe:+.4f}  dMaxDD {lit.dMaxDD:+.2%}  "
                  f"dCAGR {lit.dCAGR:+.2%}  dTurnover {lit.dTurn:+.2f}x/yr")

    # ---------------- rule 8 walk-forward: pick (x, c) on 2009-2016, evaluate 2017-2026
    print("\n" + "=" * 100)
    print("RULE 8 WALK-FORWARD — (x, c) chosen on IS 2009-2016 Sharpe, OOS 2017- untouched, 10 bps")
    wf = []
    for pname, pxp in panels.items():
        s0 = pxp.index[260]
        spy_p = pxp["SPY"].pct_change().fillna(0)
        base_p = backtest(pxp, rules_v2_weights(pxp), cost_bps=10.0, freq=FREQ)["returns"]
        for bname, (wfn, exfn) in BOOKS.items():
            w = wfn(pxp)
            ctl_r = backtest_exit(pxp, w, None, cost_bps=10.0, freq=FREQ)["returns"]
            best, best_is = None, -np.inf
            cand = {}
            for x in X_GRID:
                for c in C_GRID:
                    r = backtest_exit(pxp, w, exfn(pxp, x, c), cost_bps=10.0, freq=FREQ)["returns"]
                    cand[(x, c)] = r
                    is_sh = metrics(r.loc[s0:IS_END])["Sharpe"]
                    if is_sh > best_is:
                        best_is, best = is_sh, (x, c)
            r_oos = cand[best].loc[OOS_START:]
            print(f"\n  {pname} / RULES {bname}: IS argmax (x, c) = {best}  IS Sharpe {best_is:.4f}")
            for lbl, series in (("daily-exit " + str(best), r_oos),
                                ("no-exit control", ctl_r.loc[OOS_START:]),
                                ("RULES v2 baseline (live)", base_p.loc[OOS_START:]),
                                ("SPY", spy_p.loc[OOS_START:])):
                m = metrics(series)
                print(f"    OOS {lbl:28s} CAGR {m['CAGR']:6.2%}  Sharpe {m['Sharpe']:7.4f}  MaxDD {m['MaxDD']:7.2%}")
            m_e, m_c = metrics(r_oos), metrics(ctl_r.loc[OOS_START:])
            print(f"    OOS clause worth: dSharpe {m_e['Sharpe'] - m_c['Sharpe']:+.4f}  "
                  f"dMaxDD {m_e['MaxDD'] - m_c['MaxDD']:+.2%}  dCAGR {m_e['CAGR'] - m_c['CAGR']:+.2%}")
            # OOS across the WHOLE grid, so the IS pick is not the only number reported
            allo = pd.Series({k: metrics(v.loc[OOS_START:])["Sharpe"] - m_c["Sharpe"]
                              for k, v in cand.items()})
            print(f"    OOS dSharpe over all 15 grid points: mean {allo.mean():+.4f}  "
                  f"median {allo.median():+.4f}  best {allo.max():+.4f}  positive {int((allo > 0).sum())}/15")
            wf.append(dict(panel=pname, book=bname, best=best, is_sharpe=best_is,
                           oos_dSharpe=m_e["Sharpe"] - m_c["Sharpe"],
                           oos_pos=int((allo > 0).sum())))

    # ---------------- KEEP paths 4a and 4b for the best daily-exit arm on the live panel
    print("\n" + "=" * 100)
    print("KEEP PATHS on U56 at 10 bps (4a vs live RULES v2; 4b vs SPY, incl. rule-8 OOS)")
    pxp = panels["U56"]
    s0 = pxp.index[260]
    b_full = stats(base)
    spy_full = stats(spy)
    spy_oos = metrics(spy.loc[OOS_START:])
    base_oos = metrics(base.loc[OOS_START:])
    print(f"  live v2  {fmt(b_full)}   OOS Sharpe {base_oos['Sharpe']:.4f}")
    print(f"  SPY      {fmt(spy_full)}   OOS Sharpe {spy_oos['Sharpe']:.4f}")
    print(f"  4b bars: SPY H1 {spy_full['H1']:.4f} / H2 {spy_full['H2']:.4f} / OOS {spy_oos['Sharpe']:.4f}; "
          f"MaxDD floor {0.6 * spy_full['MaxDD']:.2%}; CAGR floor {0.7 * spy_full['CAGR']:.2%}")
    for bname, (wfn, exfn) in BOOKS.items():
        w = wfn(pxp)
        for x in X_GRID:
            for c in C_GRID:
                r = backtest_exit(pxp, w, exfn(pxp, x, c), cost_bps=10.0, freq=FREQ)["returns"].loc[s0:]
                st = stats(r)
                oos = metrics(r.loc[OOS_START:])
                p4a = (st["H1"] > b_full["H1"] and st["H2"] > b_full["H2"]
                       and st["MaxDD"] >= b_full["MaxDD"])
                p4b = (st["H1"] > spy_full["H1"] and st["H2"] > spy_full["H2"]
                       and oos["Sharpe"] > spy_oos["Sharpe"]
                       and st["MaxDD"] >= 0.6 * spy_full["MaxDD"]
                       and st["CAGR"] >= 0.7 * spy_full["CAGR"])
                tag = ("4a " if p4a else "   ") + ("4b" if p4b else "  ")
                print(f"  {bname} x={x:.2f} c={c}  {fmt(st)}  OOS Sh {oos['Sharpe']:.4f}  [{tag}]")

    G.to_csv(Path(__file__).with_suffix(".csv"), index=False)
    print("\ngrid written to", Path(__file__).with_suffix(".csv").name)


if __name__ == "__main__":
    main()
