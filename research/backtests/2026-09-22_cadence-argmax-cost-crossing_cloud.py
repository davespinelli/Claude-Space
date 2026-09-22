#!/usr/bin/env python3
"""Idea 1017 (lane cloud, 2026-09-22): at what COST RUNG does the CADENCE ARGMAX actually
INVERT, and does PROTOCOL rule 2's standing 10 bps convention sit at an EDGE of the monthly
plateau or in its MIDDLE?

Idea 1009 read four rungs (0 / 10 / 25 / 50 bps) and found the `base4b` argmax moves
D (0 bps) -> M (10, 25) -> Q (50).  Four rungs cannot locate a crossing.  This run solves
for the crossings on a FINE ladder and measures the width of each cadence's plateau, so the
record can say whether its own cost convention is a knife-edge choice or a safe interior one.

EXACT COST LADDER.  `engine.backtest` computes `held` and `turnover` independently of
cost_bps and then subtracts `turnover * cost_bps / 1e4`, so a single zero-cost run per
(panel, cadence, band, gross) yields EVERY rung exactly:  r(c) = r(0) - turnover * c / 1e4.
No re-simulation, no approximation.

Two tuned dials and no more: the COST-RUNG LADDER and the PANEL.  Cadence {D,W,M,Q}, band
(0.03, live) and gross (0.75, live) are REPORTED at every point, never selected on; the
band x gross ladder exists only to give the 4b pass COUNT a denominator.

Rule 8: the cadence is chosen on 2009-2016 ONLY at each rung; 2017-2026 is read ONCE.
Deterministic, no network.
"""
import sys, pickle
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
from engine import backtest  # noqa

CADENCES = ["D", "W", "M", "Q"]
COSTS = [0, 1, 2, 3, 4, 5, 6, 7.5, 9, 10, 11, 12.5, 15, 17.5, 20, 25, 30, 35, 40, 50]
BANDS = [0.01, 0.03, 0.08]          # reported denominator for the 4b/4a pass count
GROSS = [0.50, 0.75, 1.00]
LIVE = (0.03, 0.75)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
pd.set_option("display.width", 240)


def cagr(r):
    eq = float(np.prod(1.0 + r)); yrs = len(r) / 252.0
    return eq ** (1.0 / yrs) - 1.0 if eq > 0 else -1.0


def sharpe(r):
    sd = r.std()
    return float(r.mean() * 252.0 / (sd * np.sqrt(252.0))) if sd > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def trip(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"SMALL: dropped {len(px.columns)-len(keep)} tickers with max_1d_move >= 1.0; "
          f"{len(keep)-1} names + SPY")
    return px[keep]


PANELS = {"U56": lambda: load_universe(),
          "B136": lambda: load_universe(broad=True),
          "SMALL": small_panel}


def keep4b(r, spy, h_r, h_s):
    """4b: Sharpe > SPY in BOTH halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    return (sharpe(r[:h_r]) > sharpe(spy[:h_s]) and sharpe(r[h_r:]) > sharpe(spy[h_s:])
            and maxdd(r) >= 0.60 * maxdd(spy) and cagr(r) >= 0.70 * cagr(spy))


def keep4a(r, base):
    h = len(r) // 2; hb = len(base) // 2
    return (sharpe(r[:h]) > sharpe(base[:hb]) and sharpe(r[h:]) > sharpe(base[hb:])
            and maxdd(r) >= maxdd(base))


CACHE = ROOT / "research" / "backtests" / ".cache_1017"


def build(pname):
    """zero-cost returns + turnover for every (cadence, band, gross); cached per panel.

    The sandbox throttles background work, so each panel is computed in its own invocation.
    """
    px = PANELS[pname]()
    print(f"PANEL {pname}: {px.shape[0]} x {px.shape[1]}  "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    start = px.index[260]
    out = {}
    for b in BANDS:
        for g in GROSS:
            w = rules_v2_weights(px, band=b, gross=g)
            for f in CADENCES:
                res = backtest(px, w, cost_bps=0.0, freq=f)
                out[(f, b, g)] = (res["returns"].loc[start:].astype(float),
                                  res["turnover"].loc[start:].astype(float))
    CACHE.mkdir(exist_ok=True)
    with open(CACHE / f"{pname}.pkl", "wb") as fh:
        pickle.dump(dict(books=out, spy=px["SPY"].pct_change().fillna(0.0).loc[start:]), fh)
    print(f"cached {pname}: {len(out)} (cadence, band, gross) books")


def at_cost(pair, c, sl=None):
    r0, tv = pair
    r = r0 - tv * c / 1e4
    return (r.loc[sl] if sl is not None else r).values


def main():
    rows_live, rows_cnt, rows_r8, rows_keep = [], [], [], []
    panels = {}

    for pname in PANELS:
        with open(CACHE / f"{pname}.pkl", "rb") as fh:
            P = pickle.load(fh)
        books, spy = P["books"], P["spy"]
        panels[pname] = (books, spy, None)
        spy_f, spy_i, spy_o = spy.values, spy.loc[:IS_END].values, spy.loc[OOS_START:].values
        base_w = books[("W",) + LIVE]                       # the live book = W, 0.03, 0.75

        for c in COSTS:
            base_f = at_cost(base_w, c)
            base_o = at_cost(base_w, c, slice(OOS_START, None))
            # ---- A. the LIVE book at each cadence, full sample
            for f in CADENCES:
                r = at_cost(books[(f,) + LIVE], c)
                tv = books[(f,) + LIVE][1]
                rows_live.append(dict(panel=pname, cost=c, cadence=f, **trip(r),
                                      turn_yr=float(tv.sum() / (len(tv) / 252.0)),
                                      KEEP_4a=keep4a(r, base_f),
                                      KEEP_4b=keep4b(r, spy_f, len(r) // 2, len(spy_f) // 2)))
            # ---- B. 4b PASS COUNT per cadence over the band x gross ladder (1009's base4b)
            for f in CADENCES:
                n4b = n4a = 0
                for b in BANDS:
                    for g in GROSS:
                        r = at_cost(books[(f, b, g)], c)
                        n4b += keep4b(r, spy_f, len(r) // 2, len(spy_f) // 2)
                        n4a += keep4a(r, base_f)
                rows_cnt.append(dict(panel=pname, cost=c, cadence=f, n4b=n4b, n4a=n4a,
                                     denom=len(BANDS) * len(GROSS)))
            # ---- C. rule 8: pick the cadence on IS only, read OOS once
            is_sh = {f: sharpe(at_cost(books[(f,) + LIVE], c, slice(None, IS_END)))
                     for f in CADENCES}
            pick = max(CADENCES, key=lambda f: is_sh[f])
            oos = at_cost(books[(pick,) + LIVE], c, slice(OOS_START, None))
            rows_r8.append(dict(panel=pname, cost=c, pick=pick,
                                is_sharpe={k: round(v, 4) for k, v in is_sh.items()},
                                **{f"oos_{k}": v for k, v in trip(oos).items()},
                                base_oos_Sharpe=sharpe(base_o), spy_oos_Sharpe=sharpe(spy_o),
                                KEEP_4a_oos=keep4a(oos, base_o),
                                KEEP_4b_oos=keep4b(oos, spy_o, len(oos) // 2, len(spy_o) // 2)))

    LIVEDF = pd.DataFrame(rows_live)
    CNT = pd.DataFrame(rows_cnt)
    R8 = pd.DataFrame(rows_r8)

    print("\n" + "#" * 110)
    print("# A.  THE LIVE BOOK (band 0.03, gross 0.75) AT FOUR CADENCES, EVERY RUNG ON THE LADDER.")
    print("#" * 110)
    for p in PANELS:
        sub = LIVEDF[LIVEDF.panel == p].pivot_table(index="cost", columns="cadence",
                                                    values="Sharpe")
        sub = sub[CADENCES]
        sub["argmax"] = sub.idxmax(axis=1)
        print(f"\n--- {p}: FULL-SAMPLE SHARPE by cadence ---")
        print(sub.to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n--- annual turnover by cadence (cost-independent) ---")
    print(LIVEDF[LIVEDF.cost == 0].pivot_table(index="panel", columns="cadence",
          values="turn_yr")[CADENCES].to_string(float_format=lambda x: f"{x:.2f}"))

    print("\n" + "#" * 110)
    print("# B.  CROSSINGS AND PLATEAU WIDTHS.  Where does the argmax invert, and where does")
    print("#     PROTOCOL's 10 bps sit inside the winning cadence's plateau?")
    print("#" * 110)
    for crit, df, col in (("full-sample Sharpe (live book)", LIVEDF, "Sharpe"),
                          ("4b pass count (band x gross ladder)", CNT, "n4b"),
                          ("4a pass count (band x gross ladder)", CNT, "n4a")):
        print(f"\n--- argmax criterion: {crit} ---")
        for p in PANELS:
            sub = df[df.panel == p].pivot_table(index="cost", columns="cadence", values=col)[CADENCES]
            am = sub.idxmax(axis=1)
            seq, edges = [], []
            for c, v in am.items():
                if not seq or seq[-1][0] != v:
                    seq.append((v, c, c))
                else:
                    seq[-1] = (v, seq[-1][1], c)
            txt = " -> ".join(f"{v}[{lo:g}..{hi:g}]" for v, lo, hi in seq)
            win = am.get(10)
            seg = [s for s in seq if s[0] == win and s[1] <= 10 <= s[2]]
            if seg:
                v, lo, hi = seg[0]
                pos = (10 - lo) / (hi - lo) if hi > lo else 0.0
                lo_n = COSTS[max(0, COSTS.index(lo) - 1)] if lo > COSTS[0] else None
                hi_n = COSTS[min(len(COSTS) - 1, COSTS.index(hi) + 1)] if hi < COSTS[-1] else None
                where = (f"10 bps sits in {v}'s plateau [{lo:g},{hi:g}] at relative position "
                         f"{pos:.2f}; nearest inversions at {lo_n} and {hi_n} bps")
            else:
                where = f"10 bps -> {win} (no contiguous plateau)"
            print(f"  {p:6s} {txt}")
            print(f"         {where}")

    print("\n" + "#" * 110)
    print("# C.  4b / 4a PASS COUNTS over the 9-book band x gross ladder (3 bands x 3 gross), EVERY rung.")
    print("#" * 110)
    for p in PANELS:
        print(f"\n--- {p}: 4b passes of {len(BANDS)*len(GROSS)} ---")
        print(CNT[CNT.panel == p].pivot_table(index="cost", columns="cadence",
              values="n4b")[CADENCES].to_string())
        print(f"--- {p}: 4a passes of {len(BANDS)*len(GROSS)} ---")
        print(CNT[CNT.panel == p].pivot_table(index="cost", columns="cadence",
              values="n4a")[CADENCES].to_string())

    print("\n" + "#" * 110)
    print("# D.  BOTH KEEP PATHS for the live book at every (panel, cadence, cost).")
    print("#" * 110)
    print(LIVEDF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nFULL-SAMPLE: 4a passes {int(LIVEDF.KEEP_4a.sum())} of {len(LIVEDF)}; "
          f"4b passes {int(LIVEDF.KEEP_4b.sum())} of {len(LIVEDF)}")

    print("\n" + "#" * 110)
    print("# E.  RULE 8.  Cadence chosen on 2009-2016 ONLY at each rung; 2017-2026 read ONCE.")
    print("#" * 110)
    print(R8.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n--- OOS comparands (live RULES v2 weekly book, and SPY) ---")
    for p, (books, spy, start) in panels.items():
        so = spy.loc[OOS_START:].values
        bo = at_cost(books[("W",) + LIVE], 10, slice(OOS_START, None))
        print(f"{p:6s} live v2 W OOS@10bps {cagr(bo):7.2%} / {sharpe(bo):6.4f} / {maxdd(bo):7.2%}"
              f"   SPY OOS {cagr(so):7.2%} / {sharpe(so):6.4f} / {maxdd(so):7.2%}")

    out = ROOT / "research" / "backtests" / "2026-09-22_cadence-argmax-cost-crossing_cloud.csv"
    LIVEDF.to_csv(out, index=False)
    CNT.to_csv(str(out).replace(".csv", "_counts.csv"), index=False)
    R8.to_csv(str(out).replace(".csv", "_rule8.csv"), index=False)
    print(f"\nwrote {out.name} ({len(LIVEDF)} rows), _counts.csv, _rule8.csv")


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "REPORT"
    if a == "REPORT":
        main()
    elif a == "ALL":
        for n in PANELS:
            build(n)
        main()
    else:
        build(a)
