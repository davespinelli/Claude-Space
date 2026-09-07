#!/usr/bin/env python3
"""Idea 45: position-count COST AND LIQUIDITY — stress-test idea 2's 4b KEEP.

The book under test is idea 2's KEEP exactly as it was published (2026-09-04_position-count.py):
top-20 eligible names by the v1 composite with the /sqrt(vol20) scaler OFF, equal-weighted at a
constant 75% gross (3.75% each), RULES v1 eligibility (above 200d MA, vol20 < 0.60), weekly,
next-day execution, 10 bps.  Its published 4b drawdown margin is 1.9pp and its turnover 9.6x/yr,
so both the cost rung and the execution lag are live threats to the pass.

Two tuned parameters only:
    1. cost_bps  in {5, 10, 25, 50}      (PROTOCOL's rung is 10; 5 is the optimistic rung)
    2. lag       in {1, 2, 3, 5, 10} trading days from decision to execution
                 (1 = PROTOCOL's next-day rule; 5 ~ the "1-week execution lag" the idea asks for)
n is NOT swept: it is held at the pre-registered 20.  The two panels (U56 = research/universe.json,
B136 = research/universe_broad.json) are a structural variant, not a tuned choice; both are reported
in full.  Grid = 2 panels x 4 costs x 5 lags = 40 cells, ALL reported.

Rule 8 walk-forward: within each (panel, cost) cell the lag is chosen on 2008-2016 by IS Sharpe and
the 2017-2026 window is read once; chooser vs the lag=1 anchor vs the OOS-best regret are all printed.

SURVIVORSHIP: both universes are current-constituent lists, which flatters any momentum book; the
CAGR levels below are optimistic, the cost/lag DIFFERENCES much less so.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest, metrics                                            # noqa

SLUG = "2026-09-07_position-count-cost-and-liquidity_cloud"
OUT = ROOT / "research" / "backtests"
N, GROSS, MAX_VOL, FREQ = 20, 0.75, 0.60, "W"
COSTS = [5, 10, 25, 50]
LAGS = [1, 2, 3, 5, 10]
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# ---------------------------------------------------------------- the KEEP book, verbatim
def keep_weights(px, n=N):
    """idea 2's KEEP: top-n eligible by the v1 composite, scaler OFF, equal weight at 75% gross."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def run(px, wfn, cost, lag):
    """lag in trading days from decision to execution.  The engine already shifts by 1, so an
    extra shift of (lag-1) makes the total decision->execution delay exactly `lag` days."""
    w = wfn(px)
    if lag > 1:
        w = w.shift(lag - 1)
    res = backtest(px, w, cost_bps=cost, freq=FREQ)
    start = px.index[260]
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def main():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    recs = []
    ctx = {}
    for pname, px in panels.items():
        spy = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        ctx[pname] = dict(spy=spy, ms=ms, s1=s1, s2=s2, so=so)
        print(f"\n=== {pname}: {px.shape[1]-1} names + SPY, {px.index[0].date()} -> {px.index[-1].date()}")
        print(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS CAGR {so['CAGR']:.2%} Sharpe {so['Sharpe']:.3f} MaxDD {so['MaxDD']:.2%}")
        print(f"    4b bars: MaxDD cap {-0.60*abs(ms['MaxDD']):.2%}, CAGR floor {0.70*ms['CAGR']:.2%}")
        for cost in COSTS:
            # baselines re-priced at the SAME rung (4a must be judged like for like)
            b2, _ = run(px, rules_v2_weights, cost, 1)
            b1, _ = run(px, rules_v1_weights, cost, 1)
            mb, bh1, bh2 = metrics(b2), *hs(b2)
            ctx[(pname, cost)] = dict(b2=b2, mb=mb, bh1=bh1, bh2=bh2)
            print(f"  -- {cost} bps: RULES v2 {mb['CAGR']:6.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:7.2%} "
                  f"({bh1:.3f}/{bh2:.3f})  RULES v1 {metrics(b1)['CAGR']:6.2%}/{metrics(b1)['Sharpe']:.3f}/{metrics(b1)['MaxDD']:7.2%}")
            for lag in LAGS:
                r, to = run(px, keep_weights, cost, lag)
                m = metrics(r); h1, h2 = hs(r)
                ok4b, d, f = bars(r, spy)
                ok4a = (h1 > bh1) and (h2 > bh2) and (m["MaxDD"] >= mb["MaxDD"])
                mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[:IS_END])
                recs.append(dict(panel=pname, cost=cost, lag=lag, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                 MaxDD=m["MaxDD"], H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 m_H1=d["H1"], m_H2=d["H2"], m_OOS=d["OOS"], m_DD=d["DD"], m_CAGR=d["CAGR"],
                                 fails="+".join(f) or "none", pass4b=ok4b, pass4a=ok4a,
                                 turnover=to.sum() / m["Years"]))
                print(f"     lag={lag:>2}d | CAGR {m['CAGR']:6.2%} Sh {m['Sharpe']:.3f} DD {m['MaxDD']:7.2%} "
                      f"H1/H2 {h1:.3f}/{h2:.3f} turn {to.sum()/m['Years']:5.2f}x | margins DD {d['DD']:+.4f} "
                      f"CAGR {d['CAGR']:+.4f} H1 {d['H1']:+.3f} H2 {d['H2']:+.3f} OOS {d['OOS']:+.3f} | "
                      f"4b {'PASS' if ok4b else 'fail:'+'+'.join(f)} 4a {'PASS' if ok4a else 'fail'}")
    df = pd.DataFrame(recs)
    df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    # ------------------------------------------------------------ where the KEEP dies
    print("\n[A] 4b / 4a PASS COUNTS over all 40 cells")
    print(df.groupby(["panel", "cost"])[["pass4b", "pass4a"]].sum().to_string())
    print(f"    total 4b {df.pass4b.sum()}/{len(df)}, 4a {df.pass4a.sum()}/{len(df)}")
    print("    failure-mode tally:")
    print(df.loc[~df.pass4b, "fails"].value_counts().to_string())

    print("\n[B] THE ANCHOR CELL (lag=1) DOWN THE COST LADDER — where does the published pass die?")
    a = df[df.lag == 1].sort_values(["panel", "cost"])
    for _, r in a.iterrows():
        print(f"    {r.panel:>4} {r.cost:>2} bps | CAGR {r.CAGR:6.2%} Sh {r.Sharpe:.3f} DD {r.MaxDD:7.2%} "
              f"turn {r.turnover:.2f}x | DD margin {r.m_DD:+.4f} CAGR margin {r.m_CAGR:+.4f} "
              f"| 4b {'PASS' if r.pass4b else 'fail:'+r.fails}")

    print("\n[C] THE COST GRADIENT (per panel, lag=1): what one extra bp costs the book")
    for p in panels:
        s = df[(df.panel == p) & (df.lag == 1)].sort_values("cost")
        base = s[s.cost == 5].iloc[0]
        for _, r in s.iterrows():
            print(f"    {p:>4} {r.cost:>2} bps: dCAGR {r.CAGR-base.CAGR:+.4f} dSharpe {r.Sharpe-base.Sharpe:+.4f} "
                  f"(turnover {r.turnover:.2f}x -> implied drag {r.turnover*r.cost/1e4:.4f}/yr)")

    print("\n[D] THE LAG GRADIENT (per panel, at PROTOCOL's 10 bps): is the edge decision-day-specific?")
    for p in panels:
        s = df[(df.panel == p) & (df.cost == 10)].sort_values("lag")
        base = s[s.lag == 1].iloc[0]
        for _, r in s.iterrows():
            print(f"    {p:>4} lag {r.lag:>2}d: CAGR {r.CAGR:6.2%} ({r.CAGR-base.CAGR:+.4f}) "
                  f"Sharpe {r.Sharpe:.3f} ({r.Sharpe-base.Sharpe:+.4f}) DD {r.MaxDD:7.2%} "
                  f"turn {r.turnover:.2f}x | 4b {'PASS' if r.pass4b else 'fail:'+r.fails}")

    print("\n[E] THE JOINT SURFACE: 4b verdict by (panel, cost, lag)")
    piv = df.assign(v=np.where(df.pass4b, "PASS", df.fails)).pivot_table(
        index=["panel", "cost"], columns="lag", values="v", aggfunc="first")
    print(piv.to_string())

    # ------------------------------------------------------------ rule 8
    print("\n[F] RULE 8 WALK-FORWARD: lag chosen on 2008-2016 by IS Sharpe, 2017-2026 read once")
    wf = []
    for p in panels:
        so = ctx[p]["so"]
        for cost in COSTS:
            s = df[(df.panel == p) & (df.cost == cost)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            anc = s[s.lag == 1].iloc[0]
            best = s.loc[s.OOS_Sharpe.idxmax()]
            b2o = metrics(ctx[(p, cost)]["b2"].loc[OOS_START:])
            wf.append(dict(panel=p, cost=cost, pick_lag=pick.lag, pick_OOS=pick.OOS_Sharpe,
                           anchor_OOS=anc.OOS_Sharpe, best_lag=best.lag, best_OOS=best.OOS_Sharpe,
                           regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                           vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                           base_OOS=b2o["Sharpe"], spy_OOS=so["Sharpe"],
                           pick_OOS_CAGR=pick.OOS_CAGR, pick_OOS_DD=pick.OOS_MaxDD,
                           spy_OOS_CAGR=so["CAGR"], spy_OOS_DD=so["MaxDD"], base_OOS_CAGR=b2o["CAGR"]))
            print(f"    {p:>4} {cost:>2} bps | chooser lag={pick.lag}d OOS {pick.OOS_CAGR:6.2%}/"
                  f"{pick.OOS_Sharpe:.3f}/{pick.OOS_MaxDD:7.2%} | anchor lag=1 OOS {anc.OOS_Sharpe:.3f} "
                  f"({pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}) | OOS-best lag={best.lag}d {best.OOS_Sharpe:.3f} "
                  f"(regret {best.OOS_Sharpe-pick.OOS_Sharpe:.4f}) | RULES v2 {b2o['Sharpe']:.3f} | SPY {so['Sharpe']:.3f}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"    chooser beats the lag=1 anchor OOS in {(wfd.vs_anchor>0).sum()}/{len(wfd)}; "
          f"beats SPY OOS in {(wfd.pick_OOS>wfd.spy_OOS).sum()}/{len(wfd)}; "
          f"beats RULES v2 OOS in {(wfd.pick_OOS>wfd.base_OOS).sum()}/{len(wfd)}; "
          f"mean regret {wfd.regret.mean():.4f}, mean vs-anchor {wfd.vs_anchor.mean():+.4f}")
    print(f"    IS chooser picks lag=1 in {(wfd.pick_lag==1).sum()}/{len(wfd)} cells "
          f"(picked lags: {sorted(wfd.pick_lag.tolist())})")

    print("\n[G] BREAKEVEN COST for the 4b pass (linear interpolation of the binding margin, lag=1)")
    for p in panels:
        s = df[(df.panel == p) & (df.lag == 1)].sort_values("cost")
        for bar in ["m_DD", "m_CAGR", "m_H1", "m_H2", "m_OOS"]:
            x, y = s.cost.values.astype(float), s[bar].values
            cr = None
            for i in range(len(x) - 1):
                if (y[i] >= 0) != (y[i + 1] >= 0):
                    cr = x[i] + (-y[i] / (y[i + 1] - y[i])) * (x[i + 1] - x[i])
            print(f"    {p:>4} {bar:>6}: margin {y[0]:+.4f}@5bps -> {y[-1]:+.4f}@50bps, "
                  f"crosses zero at {'never in [5,50]' if cr is None else f'{cr:.1f} bps'}")

    print(f"\nwrote {SLUG}.grid.csv and {SLUG}.walkforward.csv")


if __name__ == "__main__":
    main()
