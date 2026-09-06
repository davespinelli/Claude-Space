#!/usr/bin/env python3
"""Idea 282: is the vol20 half the whole small-panel inversion?

Idea 60's four-way decomposition attributed 4.26 of the sub-$2B panel's 5.31 pp/yr
gate damage to the `vol20 < 0.60` half and only 2.79 pp to the trend half, and found
the vol half subtracts Sharpe from 8 of 9 gated arms on U56 too.  This run sweeps the
volatility ceiling in {0.30, 0.45, 0.60, 0.90, off} crossed with {trend gate on, off}
on SMALL439 and U56 and asks whether the record's "trend is inverted on small caps"
finding is really a VOLATILITY-filter finding.

Two tuned parameters: the vol ceiling and the trend on/off switch.  Everything else is
pre-registered: EWall book (equal weight over the eligible set), gross 0.75, weekly
cadence, next-day execution, SPY excluded from every tradable set (benchmark only).

Reported axes that are NOT tuned (both values always reported):
  * convention `rw` (re-weight survivors to a constant 0.75 gross) and `dg` (gated-out
    weight goes to cash, so realised gross falls).  Idea 277 showed a gate comparison
    that does not hold realised gross fixed is comparing exposure, not information;
    `rw` is the information-only channel, `dg` is what the live book actually does.
  * cost rung 0 bps (idea 60's attribution convention) and PROTOCOL's binding 10 bps.

Rule 8 walk-forward: the (vol ceiling, trend) arm is chosen on IS <= 2016-12-31 by IS
Sharpe and read once on 2017-01-01..2026, against SPY, the live RULES v2 baseline, the
do-nothing (no-gate) control and the pre-registered RULES-like constant (0.60, trend on).

SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); names that delisted or were acquired are absent, which
biases the *un-gated* arm upward most, i.e. against the gates.  Tickers with
max_1d_move >= 1.0 in data/small_meta.csv are dropped first (44 of 483 -> SMALL439).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, backtest, metrics  # noqa

GROSS, FREQ, SPLIT, WARM = 0.75, "W", "2016-12-31", 260
VOLCAPS = [0.30, 0.45, 0.60, 0.90, None]
TRENDS = [True, False]
CONVS = ["rw", "dg"]
COSTS = [0, 10]
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- panels
def panels():
    u = load_universe()                                  # U56 (ETF/mega-cap panel)
    s = load_universe(small=True)                        # sub-$2B panel + SPY benchmark
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in s.columns if c == "SPY" or c not in bad]
    s = s[keep]
    return {"U56": u, "SMALL439": s}


def eligible(px, trend, volcap):
    """Boolean eligibility over the tradable columns (SPY excluded everywhere)."""
    tk = [c for c in px.columns if c != "SPY"]
    p = px[tk]
    e = p.notna()
    if trend:
        e &= p > p.rolling(200).mean()
    if volcap is not None:
        vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
        e &= vol20 < volcap
    return e.reindex(columns=px.columns).fillna(False)


def weights(px, trend, volcap, conv):
    e = eligible(px, trend, volcap).astype(float)
    n = e.sum(axis=1)
    if conv == "rw":                                     # constant gross, survivors re-weighted
        return GROSS * e.div(n.replace(0, np.nan), axis=0).fillna(0.0)
    live = pd.DataFrame(1.0, index=px.index, columns=px.columns)
    live = live.where(px.notna() & (px.columns != "SPY"), 0.0)
    return GROSS * e.div(live.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


# ---------------------------------------------------------------- evaluation
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def run(px, w, cost):
    res = backtest(px, w, cost_bps=cost, freq=FREQ)
    start = px.index[WARM]
    r = res["returns"].loc[start:]
    d = stats(r)
    d["Turnover"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
    d["Gross"] = res["weights"].loc[start:].sum(axis=1).mean()
    return r, d


def main():
    P = panels()
    rows, series = [], {}
    for pname, px in P.items():
        spy = px["SPY"].pct_change().fillna(0).loc[px.index[WARM]:]
        for cost in COSTS:
            _, d = run(px, rules_v2_weights(px), cost)
            rows.append(dict(panel=pname, cost=cost, conv="-", trend="-", volcap="RULESv2", **d))
            series[(pname, cost, "-", "RULESv2")] = None
        for cost in COSTS:
            rows.append(dict(panel=pname, cost=cost, conv="-", trend="-", volcap="SPY", **stats(spy),
                             Turnover=0.0, Gross=1.0))
        series[(pname, "spy")] = spy
        for conv in CONVS:
            for trend in TRENDS:
                for vc in VOLCAPS:
                    w = weights(px, trend, vc, conv)
                    for cost in COSTS:
                        r, d = run(px, w, cost)
                        rows.append(dict(panel=pname, cost=cost, conv=conv,
                                         trend="on" if trend else "off",
                                         volcap="off" if vc is None else f"{vc:.2f}", **d))
                        series[(pname, cost, conv, "on" if trend else "off",
                                "off" if vc is None else f"{vc:.2f}")] = r
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}_grid.csv", index=False)

    fmt = dict(float_format=lambda x: f"{x:.4f}")
    print("=" * 100)
    print("ALL GRID POINTS (EWall, gross 0.75, weekly, next-day execution; SPY never held)")
    print("=" * 100)
    for pname in P:
        for cost in COSTS:
            g = grid[(grid.panel == pname) & (grid.cost == cost)]
            print(f"\n--- {pname} @ {cost} bps ---")
            print(g.drop(columns=["panel", "cost"]).to_string(index=False, **fmt))

    # ------------------------------------------------ attribution: which half is the damage?
    print("\n" + "=" * 100)
    print("P1 DAMAGE ATTRIBUTION vs the un-gated control (trend off, volcap off), pp/yr of CAGR")
    print("=" * 100)
    att = []
    for pname in P:
        for cost in COSTS:
            for conv in CONVS:
                g = grid[(grid.panel == pname) & (grid.cost == cost) & (grid.conv == conv)]
                base = g[(g.trend == "off") & (g.volcap == "off")].iloc[0]
                for _, r0 in g.iterrows():
                    att.append(dict(panel=pname, cost=cost, conv=conv, trend=r0.trend,
                                    volcap=r0.volcap,
                                    d_CAGR_pp=(r0.CAGR - base.CAGR) * 100,
                                    d_Sharpe=r0.Sharpe - base.Sharpe,
                                    Gross=r0.Gross))
    att = pd.DataFrame(att)
    att.to_csv(f"{OUT}_attribution.csv", index=False)
    for pname in P:
        for conv in CONVS:
            a = att[(att.panel == pname) & (att.conv == conv)]
            print(f"\n--- {pname} / {conv} ---")
            print(a.pivot_table(index=["trend", "volcap"], columns="cost",
                                values=["d_CAGR_pp", "d_Sharpe"]).to_string(**fmt))

    print("\n" + "=" * 100)
    print("P2 THE TWO HALVES, SEPARATED (pp/yr CAGR and dSharpe of adding each half alone)")
    print("=" * 100)
    halves = []
    for pname in P:
        for cost in COSTS:
            for conv in CONVS:
                g = grid[(grid.panel == pname) & (grid.cost == cost) & (grid.conv == conv)]
                def cell(t, v):
                    return g[(g.trend == t) & (g.volcap == v)].iloc[0]
                for v in ["0.30", "0.45", "0.60", "0.90"]:
                    # trend half priced AT this vol ceiling; vol half priced at each trend state
                    halves.append(dict(panel=pname, cost=cost, conv=conv, volcap=v,
                        trend_half_pp=(cell("on", v).CAGR - cell("off", v).CAGR) * 100,
                        trend_half_dS=cell("on", v).Sharpe - cell("off", v).Sharpe,
                        vol_half_pp_trendon=(cell("on", v).CAGR - cell("on", "off").CAGR) * 100,
                        vol_half_dS_trendon=cell("on", v).Sharpe - cell("on", "off").Sharpe,
                        vol_half_pp_trendoff=(cell("off", v).CAGR - cell("off", "off").CAGR) * 100,
                        vol_half_dS_trendoff=cell("off", v).Sharpe - cell("off", "off").Sharpe))
                halves.append(dict(panel=pname, cost=cost, conv=conv, volcap="off",
                    trend_half_pp=(cell("on", "off").CAGR - cell("off", "off").CAGR) * 100,
                    trend_half_dS=cell("on", "off").Sharpe - cell("off", "off").Sharpe,
                    vol_half_pp_trendon=0.0, vol_half_dS_trendon=0.0,
                    vol_half_pp_trendoff=0.0, vol_half_dS_trendoff=0.0))
    halves = pd.DataFrame(halves)
    halves.to_csv(f"{OUT}_halves.csv", index=False)
    print(halves.to_string(index=False, **fmt))

    print("\nP2b THE QUEUED QUESTION — trend-half damage with the vol filter REMOVED vs PRESENT:")
    for pname in P:
        for cost in COSTS:
            for conv in CONVS:
                h = halves[(halves.panel == pname) & (halves.cost == cost) & (halves.conv == conv)]
                off = h[h.volcap == "off"].iloc[0]
                at60 = h[h.volcap == "0.60"].iloc[0]
                print(f"  {pname:9s} {cost:2d}bps {conv}: trend half alone (no vol cap) "
                      f"{off.trend_half_pp:+7.3f} pp / {off.trend_half_dS:+.4f} Sh | "
                      f"trend half at volcap 0.60 {at60.trend_half_pp:+7.3f} pp / "
                      f"{at60.trend_half_dS:+.4f} Sh | vol half alone (trend off) "
                      f"{at60.vol_half_pp_trendoff:+7.3f} pp / {at60.vol_half_dS_trendoff:+.4f} Sh")

    # ------------------------------------------------ rule 8 walk-forward
    print("\n" + "=" * 100)
    print("P3 RULE 8 WALK-FORWARD — arm chosen on IS <= 2016 by IS Sharpe, OOS 2017-2026 read once")
    print("=" * 100)
    wf = []
    for pname, px in P.items():
        spy = series[(pname, "spy")]
        spy_oos, spy_is = spy.loc[SPLIT:], spy.loc[:SPLIT]
        for cost in COSTS:
            for conv in CONVS:
                cands = {}
                for trend in ["on", "off"]:
                    for vc in ["0.30", "0.45", "0.60", "0.90", "off"]:
                        cands[(trend, vc)] = series[(pname, cost, conv, trend, vc)]
                is_sh = {k: metrics(v.loc[:SPLIT])["Sharpe"] for k, v in cands.items()}
                pick = max(is_sh, key=is_sh.get)
                for label, k in [("IS-chooser pick", pick),
                                 ("do-nothing (no gate)", ("off", "off")),
                                 ("RULES-like (0.60, trend on)", ("on", "0.60")),
                                 ("trend only (no vol cap)", ("on", "off")),
                                 ("vol only 0.60 (no trend)", ("off", "0.60"))]:
                    o = metrics(cands[k].loc[SPLIT:])
                    wf.append(dict(panel=pname, cost=cost, conv=conv, arm=label,
                                   chosen=f"{k[0]}/{k[1]}", IS_Sharpe=is_sh[k],
                                   OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
                b = metrics(backtest(px, rules_v2_weights(px), cost_bps=cost,
                                     freq=FREQ)["returns"].loc[px.index[WARM]:].loc[SPLIT:])
                wf.append(dict(panel=pname, cost=cost, conv=conv, arm="RULES v2 baseline",
                               chosen="-", IS_Sharpe=np.nan, OOS_CAGR=b["CAGR"],
                               OOS_Sharpe=b["Sharpe"], OOS_MaxDD=b["MaxDD"]))
                s = metrics(spy_oos)
                wf.append(dict(panel=pname, cost=cost, conv=conv, arm="SPY", chosen="-",
                               IS_Sharpe=metrics(spy_is)["Sharpe"], OOS_CAGR=s["CAGR"],
                               OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"]))
    wf = pd.DataFrame(wf)
    wf.to_csv(f"{OUT}_walkforward.csv", index=False)
    print(wf.to_string(index=False, **fmt))

    # ------------------------------------------------ KEEP paths
    print("\n" + "=" * 100)
    print("P4 BOTH KEEP PATHS at 10 bps (4a vs live RULES v2, 4b vs SPY incl. rule-8 OOS)")
    print("=" * 100)
    keep = []
    for pname, px in P.items():
        spy = series[(pname, "spy")]
        sp = stats(spy); sp_oos = metrics(spy.loc[SPLIT:])["Sharpe"]
        b = grid[(grid.panel == pname) & (grid.cost == 10) & (grid.volcap == "RULESv2")].iloc[0]
        for conv in CONVS:
            for trend in ["on", "off"]:
                for vc in ["0.30", "0.45", "0.60", "0.90", "off"]:
                    g = grid[(grid.panel == pname) & (grid.cost == 10) & (grid.conv == conv) &
                             (grid.trend == trend) & (grid.volcap == vc)].iloc[0]
                    oos = metrics(series[(pname, 10, conv, trend, vc)].loc[SPLIT:])["Sharpe"]
                    p4a = g.H1 > b.H1 and g.H2 > b.H2 and g.MaxDD >= b.MaxDD
                    bars = dict(H1=g.H1 > sp["H1"], H2=g.H2 > sp["H2"], OOS=oos > sp_oos,
                                DD=g.MaxDD >= 0.60 * sp["MaxDD"], CAGR=g.CAGR >= 0.70 * sp["CAGR"])
                    keep.append(dict(panel=pname, conv=conv, trend=trend, volcap=vc,
                                     CAGR=g.CAGR, Sharpe=g.Sharpe, MaxDD=g.MaxDD, H1=g.H1, H2=g.H2,
                                     OOS=oos, path4a=p4a, path4b=all(bars.values()),
                                     failing=",".join(k for k, v in bars.items() if not v) or "-"))
    keep = pd.DataFrame(keep)
    keep.to_csv(f"{OUT}_keeppaths.csv", index=False)
    print(keep.to_string(index=False, **fmt))
    print(f"\n4a passes: {int(keep.path4a.sum())}/{len(keep)}   4b passes: "
          f"{int(keep.path4b.sum())}/{len(keep)}")
    if keep.path4b.any():
        print(keep[keep.path4b].to_string(index=False, **fmt))
    print("\nBinding bar census over 4b failures:")
    print(pd.Series([b for f in keep.loc[~keep.path4b, "failing"] for b in f.split(",")]
                    ).value_counts().to_string())


if __name__ == "__main__":
    main()
