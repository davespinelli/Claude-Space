#!/usr/bin/env python3
"""Idea 2223 (lane cloud, 2026-09-22): does a NO-TRADE BAND on the CORE band book buy back
what the idle-NAV SLEEVE costs?

Idea 2213 priced the idle-NAV sleeve's turnover lift (1.92x -> 3.03x/yr) but left the CORE
weights rebalanced every week.  This run puts a drift tolerance on the core leg: at each
weekly rebalance, if the L1 distance between the rule's target and the DRIFTED holdings is
<= tol, do not trade at all.  Two tuned parameters only: tol and the band width c.

Two arms, each on the same two parameters:
  LAZY-ALL      the tolerance blocks every trade, exits included (the literal no-trade band).
  LAZY-KEEPEXIT names that have gated OUT are always sold; the tolerance governs the rest.

Panels: U56 (research/universe.json) and B136 (research/universe_broad.json).
Costs: 10 bps headline (PROTOCOL rule 2), 25/50 bps reported.  Next-day execution, weekly.
Both KEEP paths (4a vs live RULES v2, 4b vs SPY) and rule 8 (choose on IS, read OOS).

Outputs (all written next to this script):
  .grid.csv          every (arm, panel, cost, c, tol) cell, full/H1/H2/IS/OOS + turnover
  .walkforward.csv   rule-8 IS chooser picks and their untouched OOS readings
  .gates.csv         pre-registered identity checks, printed before any hypothesis is read
  .result.md         the write-up
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
WARMUP = 260
GROSS = 0.75          # live RULES v2 gross, held fixed (not a tuned parameter)
FREQ = "W"
TOLS = [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30, 0.40]
CS = [0.02, 0.03, 0.05, 0.08]
COSTS = [10.0, 25.0, 50.0]


# ---------------------------------------------------------------- runner
def run_lazy(px, band, gross, tol, arm, cost_bps=10.0, freq=FREQ):
    """engine.backtest's mechanics, with a no-trade tolerance at the rebalance step.

    tol == 0 with arm 'LAZY-ALL' must reproduce engine.backtest(px, rules_v2_weights(px))
    exactly (gate G1): `d > 0` trades on every date the engine would have traded, and on the
    dates where d == 0 the engine's own trade is a no-op.
    """
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    W = rules_v2_weights(px, band=band, gross=gross)
    Wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values     # decided t, applied t+1
    gated_in = (W > 0).reindex(idx).fillna(False).shift(1).fillna(False).values.astype(bool)
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.astype(bool)
    n = px.shape[1]
    cur = np.zeros(n)
    held = np.zeros((len(idx), n))
    turn = np.zeros(len(idx))
    for i in range(len(idx)):
        if mask[i] or i == 0:
            tgt = Wt[i]
            if arm == "LAZY-KEEPEXIT":
                # always sell what has gated OUT; the tolerance governs the remainder
                forced = cur.copy()
                forced[~gated_in[i]] = 0.0
                d_rest = np.abs(tgt - forced).sum()
                if i == 0 or d_rest > tol:
                    new = tgt
                else:
                    new = forced
            else:
                new = tgt if (i == 0 or np.abs(tgt - cur).sum() > tol) else cur
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def stats(r, turn=None):
    m = metrics(r)
    h = len(r) // 2
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
               CAGR_H1=metrics(r.iloc[:h])["CAGR"], CAGR_H2=metrics(r.iloc[h:])["CAGR"],
               MaxDD_H1=metrics(r.iloc[:h])["MaxDD"], MaxDD_H2=metrics(r.iloc[h:])["MaxDD"])
    if turn is not None:
        out["turn_yr"] = turn.sum() / (len(turn) / 252)
    return out


def keep_4a(cand, base):
    return bool(cand["H1"] > base["H1"] and cand["H2"] > base["H2"] and cand["MaxDD"] >= base["MaxDD"])


def keep_4b(cand_full, cand_oos, spy_full, spy_oos):
    return bool(cand_full["H1"] > spy_full["H1"] and cand_full["H2"] > spy_full["H2"]
                and cand_oos["Sharpe"] > spy_oos["Sharpe"]
                and cand_full["MaxDD"] >= 0.60 * spy_full["MaxDD"]
                and cand_full["CAGR"] >= 0.70 * spy_full["CAGR"])


# ---------------------------------------------------------------- panels
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    return {"U56": u, "B136": b}


def main():
    P = panels()
    gates, rows, wf = [], [], []

    # ---------------- gates, printed before any hypothesis is read
    for name, px in P.items():
        eng = backtest(px, rules_v2_weights(px, band=0.03, gross=GROSS), cost_bps=10.0, freq=FREQ)
        r0, t0 = run_lazy(px, 0.03, GROSS, 0.0, "LAZY-ALL", 10.0)
        gates.append(dict(panel=name, gate="G1 runner==engine.backtest at tol=0 (returns)",
                          value=float(np.abs(r0 - eng["returns"]).max()), ok=bool(np.abs(r0 - eng["returns"]).max() < 1e-14)))
        gates.append(dict(panel=name, gate="G2 runner==engine.backtest at tol=0 (turnover)",
                          value=float(np.abs(t0 - eng["turnover"]).max()), ok=bool(np.abs(t0 - eng["turnover"]).max() < 1e-12)))
        rbig, tbig = run_lazy(px, 0.03, GROSS, 99.0, "LAZY-ALL", 10.0)
        gates.append(dict(panel=name, gate="G3 tol=99 trades once only (sum turnover)",
                          value=float(tbig.sum()), ok=bool(tbig.iloc[1:].sum() < 1e-12)))
        r25, _ = run_lazy(px, 0.03, GROSS, 0.06, "LAZY-ALL", 25.0)
        r10, t10 = run_lazy(px, 0.03, GROSS, 0.06, "LAZY-ALL", 10.0)
        implied = r10 - t10 * 15.0 / 1e4
        gates.append(dict(panel=name, gate="G4 cost axis is an identity (25bps vs derived)",
                          value=float(np.abs(r25 - implied).max()), ok=bool(np.abs(r25 - implied).max() < 1e-15)))
        W = rules_v2_weights(px, band=0.03, gross=GROSS)
        gates.append(dict(panel=name, gate="G5 never levered (max gross of target)",
                          value=float(W.sum(axis=1).max()), ok=bool(W.sum(axis=1).max() <= GROSS + 1e-12)))
        hp, _ = run_lazy(px, 0.03, GROSS, 0.06, "LAZY-KEEPEXIT", 10.0)
        gates.append(dict(panel=name, gate="G6 KEEPEXIT != LAZY-ALL at same (c,tol)",
                          value=float(np.abs(hp - r10).max()), ok=bool(np.abs(hp - r10).max() > 0)))
        gates.append(dict(panel=name, gate="G7 sample years", value=float(len(px.loc[px.index[WARMUP]:]) / 252), ok=bool(len(px) / 252 > 10)))
        gates.append(dict(panel=name, gate="G8 names priced", value=float(px.shape[1]), ok=True))
    G = pd.DataFrame(gates)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    print("=== GATES (pre-registered, printed before any hypothesis) ===")
    print(G.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    print(f"{int(G.ok.sum())} of {len(G)} PASS\n")

    # ---------------- grid
    for pname, px in P.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        h = len(spy) // 2
        split = spy.index[h]
        spy_full, spy_oos = stats(spy), stats(spy.iloc[h:])
        spy_is = stats(spy.iloc[:h])
        for cost in COSTS:
            base_r = backtest(px, rules_v2_weights(px, band=0.03, gross=GROSS), cost_bps=cost, freq=FREQ)
            b = base_r["returns"].loc[start:]
            base_full = stats(b, base_r["turnover"].loc[start:])
            base_oos, base_is = stats(b.iloc[h:]), stats(b.iloc[:h])
            v1 = backtest(px, rules_v1_weights(px), cost_bps=cost, freq=FREQ)["returns"].loc[start:]
            for lab, d in (("SPY", spy_full), ("RULES v2 (live)", base_full), ("RULES v1", stats(v1))):
                rows.append(dict(arm="REFERENCE", panel=pname, cost_bps=cost, c=np.nan, tol=np.nan, name=lab,
                                 **d, IS_Sharpe=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                 keep4a=False, keep4b=False))
            rows[-2].update(IS_Sharpe=base_is["Sharpe"], OOS_CAGR=base_oos["CAGR"],
                            OOS_Sharpe=base_oos["Sharpe"], OOS_MaxDD=base_oos["MaxDD"])
            rows[-3].update(IS_Sharpe=spy_is["Sharpe"], OOS_CAGR=spy_oos["CAGR"],
                            OOS_Sharpe=spy_oos["Sharpe"], OOS_MaxDD=spy_oos["MaxDD"])
            for arm in ("LAZY-ALL", "LAZY-KEEPEXIT"):
                for c, tol in itertools.product(CS, TOLS):
                    r, t = run_lazy(px, c, GROSS, tol, arm, cost)
                    r, t = r.loc[start:], t.loc[start:]
                    f = stats(r, t)
                    o, i_ = stats(r.iloc[h:]), stats(r.iloc[:h])
                    rows.append(dict(arm=arm, panel=pname, cost_bps=cost, c=c, tol=tol,
                                     name=f"{arm} c={c} tol={tol}", **f,
                                     IS_Sharpe=i_["Sharpe"], OOS_CAGR=o["CAGR"],
                                     OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                                     keep4a=keep_4a(f, base_full),
                                     keep4b=keep_4b(f, o, spy_full, spy_oos)))
        print(f"{pname}: grid done ({len(rows)} rows so far), split at {split.date()}")

        # ---------------- rule 8: choose on IS only, read OOS untouched
        for cost in COSTS:
            for arm in ("LAZY-ALL", "LAZY-KEEPEXIT"):
                cand = [x for x in rows if x["arm"] == arm and x["panel"] == pname and x["cost_bps"] == cost]
                pick = max(cand, key=lambda x: x["IS_Sharpe"])
                base_r = backtest(px, rules_v2_weights(px, band=0.03, gross=GROSS), cost_bps=cost, freq=FREQ)["returns"].loc[start:]
                bo = stats(base_r.iloc[h:])
                wf.append(dict(panel=pname, arm=arm, cost_bps=cost, split=str(split.date()),
                               pick_c=pick["c"], pick_tol=pick["tol"], IS_Sharpe=pick["IS_Sharpe"],
                               OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                               base_OOS_CAGR=bo["CAGR"], base_OOS_Sharpe=bo["Sharpe"], base_OOS_MaxDD=bo["MaxDD"],
                               spy_OOS_CAGR=spy_oos["CAGR"], spy_OOS_Sharpe=spy_oos["Sharpe"], spy_OOS_MaxDD=spy_oos["MaxDD"],
                               turn_yr=pick["turn_yr"],
                               beats_base_OOS=bool(pick["OOS_Sharpe"] > bo["Sharpe"]),
                               beats_spy_OOS=bool(pick["OOS_Sharpe"] > spy_oos["Sharpe"])))

    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.grid.csv", index=False)
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\n=== REFERENCES (10 bps) ===")
    print(D[(D.arm == "REFERENCE") & (D.cost_bps == 10)][["panel", "name", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "turn_yr"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== FULL GRID, 10 bps, every point (no cherry-picking) ===")
    sub = D[(D.arm != "REFERENCE") & (D.cost_bps == 10)]
    print(sub[["arm", "panel", "c", "tol", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "turn_yr", "keep4a", "keep4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== 25 / 50 bps grid ===")
    sub2 = D[(D.arm != "REFERENCE") & (D.cost_bps != 10)]
    print(sub2[["arm", "panel", "cost_bps", "c", "tol", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "turn_yr", "keep4a", "keep4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== RULE 8 WALK-FORWARD (chosen on IS Sharpe, OOS untouched) ===")
    print(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== KEEP counts ===")
    print(D[D.arm != "REFERENCE"].groupby(["arm", "panel", "cost_bps"])[["keep4a", "keep4b"]].sum().to_string())


if __name__ == "__main__":
    main()
