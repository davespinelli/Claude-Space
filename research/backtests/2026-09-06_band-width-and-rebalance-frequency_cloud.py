#!/usr/bin/env python3
"""Idea 59: band width vs rebalance frequency — is the band doing anything the cadence isn't?

Idea 57 tested 3% and 5% bands at weekly cadence only, and reported that a
monthly-re-evaluated gate performed as well as either.  Both instruments do the same thing
mechanically: they slow the gate down.  This run separates them.

Design (two tuned parameters: band width, cadence; everything else pre-registered):
  * book      EWall — equal weight over every name the gate admits, gross 0.75, SPY never held
  * band      {none (ungated), 0%, 2%, 3%, 5%, 8%}  — `none` is the ungated control, 0% is the
              plain 200d crossing, the rest are baseline.band_state hysteresis bands
  * cadence   weekly / monthly (the gate and the rebalance move together — the realistic form)
  * panels    U56 (research/universe.json) and B136 (research/universe_broad.json)
  * costs     10 bps (PROTOCOL) and 25 bps, both always reported
  * convention `rw` (survivors re-weighted to a constant 0.75 gross — the information channel)
              and `dg` (gated-out weight goes to cash, what RULES v2 actually does).  Idea 277:
              a gate comparison that does not hold realised gross fixed compares exposure.

  => 6 x 2 x 2 x 2 x 2 = 96 grid points, all reported.

Separation panel (pre-registered, not tuned): at band 0% and 3%, the 2x2 of
{gate re-evaluated weekly, monthly} x {rebalanced weekly, monthly}, so the slowing done by the
band, by the gate's sampling rate and by the trade schedule are three separate columns.

Speed axis: gate flip rate (state changes per ticker-year) is measured for every arm, so band
arms and cadence arms can be placed on one curve (idea 61's design variable).

Rule 8: (band, cadence) chosen on IS <= 2016-12-31 by IS Sharpe, 2017-2026 read once, against
SPY, the live RULES v2 baseline, the ungated control and the pre-registered constant b=3%/weekly.

SURVIVORSHIP: B136 is current constituents of a large-cap list (PROTOCOL rule 9).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, backtest, metrics  # noqa
from engine import rebalance_mask  # noqa

GROSS, WARM, SPLIT = 0.75, 260, "2016-12-31"
BANDS = [None, 0.00, 0.02, 0.03, 0.05, 0.08]
CADENCES = ["W", "M"]
CONVS = ["rw", "dg"]
COSTS = [10, 25]
OUT = Path(__file__).with_suffix("")
lab = lambda b: "none" if b is None else f"{b:.2f}"


def tradable(px):
    return [c for c in px.columns if c != "SPY"]


def gate(px, band, eval_freq=None):
    """Gate state on the tradable columns; eval_freq slows the gate's SAMPLING (not the trades)."""
    tk = tradable(px)
    p = px[tk]
    g = pd.DataFrame(True, index=p.index, columns=p.columns) if band is None else band_state(p, band)
    g = g & p.notna()
    if eval_freq:
        m = rebalance_mask(p.index, eval_freq)
        g = g.where(m).ffill().fillna(False).astype(bool)
    return g.reindex(columns=px.columns).fillna(False)


def weights(px, g, conv):
    e = g.astype(float)
    if conv == "rw":
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    live = px[tradable(px)].notna().astype(float).reindex(columns=px.columns).fillna(0.0)
    return GROSS * e.div(live.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def flips_per_ticker_year(g, px):
    """Gate state changes per ticker-year over the columns that are actually priced."""
    tk = tradable(px)
    g = g[tk].loc[px.index[WARM]:]
    live = px[tk].loc[px.index[WARM]:].notna()
    ch = (g.astype(int).diff().abs() == 1) & live & live.shift(1)
    years = live.sum().sum() / 252
    return ch.sum().sum() / years if years else np.nan


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def run(px, w, cost, freq):
    res = backtest(px, w, cost_bps=cost, freq=freq)
    start = px.index[WARM]
    r = res["returns"].loc[start:]
    d = stats(r)
    d["Turnover"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
    d["Gross"] = res["weights"].loc[start:].sum(axis=1).mean()
    return r, d


def main():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    rows, series, spys = [], {}, {}

    for pname, px in P.items():
        spy = px["SPY"].pct_change().fillna(0).loc[px.index[WARM]:]
        spys[pname] = spy
        for cost in COSTS:
            _, d = run(px, rules_v2_weights(px), cost, "W")
            rows.append(dict(panel=pname, cost=cost, conv="-", band="RULESv2", cad="W", flips=np.nan, **d))
            rows.append(dict(panel=pname, cost=cost, conv="-", band="SPY", cad="-", flips=0.0,
                             **stats(spy), Turnover=0.0, Gross=1.0))
        for band in BANDS:
            g = gate(px, band)
            fl = flips_per_ticker_year(g, px)
            for conv in CONVS:
                w = weights(px, g, conv)
                for cad in CADENCES:
                    for cost in COSTS:
                        r, d = run(px, w, cost, cad)
                        rows.append(dict(panel=pname, cost=cost, conv=conv, band=lab(band),
                                         cad=cad, flips=fl, **d))
                        series[(pname, cost, conv, lab(band), cad)] = r
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}_grid.csv", index=False)

    fmt = dict(float_format=lambda x: f"{x:.4f}")
    print("=" * 104)
    print("ALL 96 GRID POINTS — EWall, gross 0.75, next-day execution, SPY never held")
    print("=" * 104)
    for pname in P:
        for cost in COSTS:
            g = grid[(grid.panel == pname) & (grid.cost == cost)]
            print(f"\n--- {pname} @ {cost} bps ---")
            print(g.drop(columns=["panel", "cost"]).to_string(index=False, **fmt))

    # -------------------------------------------------- P1: the two effects, side by side
    print("\n" + "=" * 104)
    print("P1 WHAT EACH INSTRUMENT BUYS — dSharpe / dCAGR(pp) / dMaxDD(pp) vs the SAME arm one step faster")
    print("=" * 104)
    eff = []
    for pname in P:
        for cost in COSTS:
            for conv in CONVS:
                g = grid[(grid.panel == pname) & (grid.cost == cost) & (grid.conv == conv)]
                cell = lambda b, c: g[(g.band == b) & (g.cad == c)].iloc[0]
                for b in ["0.00", "0.02", "0.03", "0.05", "0.08"]:
                    eff.append(dict(panel=pname, cost=cost, conv=conv, instrument=f"band {b} (W)",
                                    ref="band 0.00 W",
                                    dS=cell(b, "W").Sharpe - cell("0.00", "W").Sharpe,
                                    dCAGR=(cell(b, "W").CAGR - cell("0.00", "W").CAGR) * 100,
                                    dDD=(cell(b, "W").MaxDD - cell("0.00", "W").MaxDD) * 100,
                                    flips=cell(b, "W").flips, turn=cell(b, "W").Turnover))
                for b in ["none", "0.00", "0.02", "0.03", "0.05", "0.08"]:
                    eff.append(dict(panel=pname, cost=cost, conv=conv, instrument=f"monthly @ band {b}",
                                    ref=f"weekly @ band {b}",
                                    dS=cell(b, "M").Sharpe - cell(b, "W").Sharpe,
                                    dCAGR=(cell(b, "M").CAGR - cell(b, "W").CAGR) * 100,
                                    dDD=(cell(b, "M").MaxDD - cell(b, "W").MaxDD) * 100,
                                    flips=cell(b, "M").flips, turn=cell(b, "M").Turnover))
    eff = pd.DataFrame(eff)
    eff.to_csv(f"{OUT}_effects.csv", index=False)
    print(eff.to_string(index=False, **fmt))
    print("\nP1b THE QUEUED QUESTION — does the band beat the cadence, and does either beat NEITHER?")
    for pname in P:
        for cost in COSTS:
            for conv in CONVS:
                g = grid[(grid.panel == pname) & (grid.cost == cost) & (grid.conv == conv)]
                cell = lambda b, c: g[(g.band == b) & (g.cad == c)].iloc[0]
                base = cell("0.00", "W")
                b3w, b0m, b3m = cell("0.03", "W"), cell("0.00", "M"), cell("0.03", "M")
                ung = cell("none", "W")
                print(f"  {pname:5s} {cost:2d}bps {conv}: 200d/W {base.Sharpe:.4f} | "
                      f"band3/W {b3w.Sharpe:+.4f} ({b3w.Sharpe-base.Sharpe:+.4f}) | "
                      f"200d/M {b0m.Sharpe:.4f} ({b0m.Sharpe-base.Sharpe:+.4f}) | "
                      f"band3/M {b3m.Sharpe:.4f} ({b3m.Sharpe-base.Sharpe:+.4f}) | "
                      f"UNGATED/W {ung.Sharpe:.4f} ({ung.Sharpe-base.Sharpe:+.4f})")

    # -------------------------------------------------- P2: one speed curve or two instruments?
    print("\n" + "=" * 104)
    print("P2 ARE BAND AND CADENCE THE SAME INSTRUMENT? Sharpe vs gate flip rate, band arms vs cadence arms")
    print("(`stat` = Sharpe SPAN across the 5 band widths for a band family; for the cadence family it is")
    print(" the MEAN dSharpe of weekly -> monthly over those same 5 bands, at an unchanged gate.)")
    print("=" * 104)
    sp = []
    for pname in P:
        for cost in COSTS:
            for conv in CONVS:
                g = grid[(grid.panel == pname) & (grid.cost == cost) & (grid.conv == conv)]
                g = g[g.band != "none"]
                for cad in CADENCES:
                    h = g[g.cad == cad]
                    sp.append(dict(panel=pname, cost=cost, conv=conv, family=f"band sweep @ {cad}",
                                   rho=h.flips.rank().corr(h.Sharpe.rank()),   # Spearman, no scipy
                                   stat=h.Sharpe.max() - h.Sharpe.min(),
                                   span_flips=h.flips.max() - h.flips.min()))
                # the same slowing measured through cadence at fixed band
                d = [(g[(g.band == b) & (g.cad == "M")].Sharpe.iloc[0]
                      - g[(g.band == b) & (g.cad == "W")].Sharpe.iloc[0]) for b in
                     ["0.00", "0.02", "0.03", "0.05", "0.08"]]
                sp.append(dict(panel=pname, cost=cost, conv=conv, family="cadence W->M (fixed band)",
                               rho=np.nan, stat=float(np.mean(d)), span_flips=0.0))
    sp = pd.DataFrame(sp)
    sp.to_csv(f"{OUT}_speed.csv", index=False)
    print(sp.to_string(index=False, **fmt))

    # -------------------------------------------------- P3: gate sampling vs trade schedule
    print("\n" + "=" * 104)
    print("P3 SEPARATION PANEL @10 bps — {gate re-evaluated W,M} x {rebalanced W,M}, bands 0% and 3%")
    print("=" * 104)
    sep = []
    for pname, px in P.items():
        for band in [0.00, 0.03]:
            for ev in CADENCES:
                g = gate(px, band, eval_freq=ev)
                fl = flips_per_ticker_year(g, px)
                for conv in CONVS:
                    w = weights(px, g, conv)
                    for cad in CADENCES:
                        _, d = run(px, w, 10, cad)
                        sep.append(dict(panel=pname, conv=conv, band=lab(band), gate_eval=ev,
                                        rebal=cad, flips=fl, **d))
    sep = pd.DataFrame(sep)
    sep.to_csv(f"{OUT}_separation.csv", index=False)
    print(sep.to_string(index=False, **fmt))

    # -------------------------------------------------- P4: rule 8
    print("\n" + "=" * 104)
    print("P4 RULE 8 — (band, cadence) chosen on IS <= 2016 by IS Sharpe, OOS 2017-2026 read once")
    print("=" * 104)
    wf = []
    for pname, px in P.items():
        spy = spys[pname]
        for cost in COSTS:
            for conv in CONVS:
                cands = {(b, c): series[(pname, cost, conv, b, c)]
                         for b in [lab(x) for x in BANDS] for c in CADENCES}
                is_sh = {k: metrics(v.loc[:SPLIT])["Sharpe"] for k, v in cands.items()}
                pick = max(is_sh, key=is_sh.get)
                for label, k in [("IS-chooser pick", pick),
                                 ("constant band3 / weekly", ("0.03", "W")),
                                 ("plain 200d / weekly", ("0.00", "W")),
                                 ("plain 200d / monthly", ("0.00", "M")),
                                 ("ungated / weekly", ("none", "W"))]:
                    o = metrics(cands[k].loc[SPLIT:])
                    wf.append(dict(panel=pname, cost=cost, conv=conv, arm=label,
                                   chosen=f"{k[0]}/{k[1]}", IS=is_sh[k], OOS_CAGR=o["CAGR"],
                                   OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
                b = metrics(backtest(px, rules_v2_weights(px), cost_bps=cost, freq="W")["returns"]
                            .loc[px.index[WARM]:].loc[SPLIT:])
                wf.append(dict(panel=pname, cost=cost, conv=conv, arm="RULES v2 baseline", chosen="-",
                               IS=np.nan, OOS_CAGR=b["CAGR"], OOS_Sharpe=b["Sharpe"], OOS_MaxDD=b["MaxDD"]))
                s = metrics(spy.loc[SPLIT:])
                wf.append(dict(panel=pname, cost=cost, conv=conv, arm="SPY", chosen="-",
                               IS=metrics(spy.loc[:SPLIT])["Sharpe"], OOS_CAGR=s["CAGR"],
                               OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"]))
    wf = pd.DataFrame(wf)
    wf.to_csv(f"{OUT}_walkforward.csv", index=False)
    print(wf.to_string(index=False, **fmt))

    # -------------------------------------------------- P5: both KEEP paths
    print("\n" + "=" * 104)
    print("P5 BOTH KEEP PATHS at 10 bps (4a vs live RULES v2, 4b vs SPY incl. rule-8 OOS)")
    print("=" * 104)
    keep = []
    for pname, px in P.items():
        spy = spys[pname]; sp_ = stats(spy); sp_oos = metrics(spy.loc[SPLIT:])["Sharpe"]
        b = grid[(grid.panel == pname) & (grid.cost == 10) & (grid.band == "RULESv2")].iloc[0]
        for conv in CONVS:
            for bd in [lab(x) for x in BANDS]:
                for cad in CADENCES:
                    g = grid[(grid.panel == pname) & (grid.cost == 10) & (grid.conv == conv) &
                             (grid.band == bd) & (grid.cad == cad)].iloc[0]
                    oos = metrics(series[(pname, 10, conv, bd, cad)].loc[SPLIT:])["Sharpe"]
                    bars = dict(H1=g.H1 > sp_["H1"], H2=g.H2 > sp_["H2"], OOS=oos > sp_oos,
                                DD=g.MaxDD >= 0.60 * sp_["MaxDD"], CAGR=g.CAGR >= 0.70 * sp_["CAGR"])
                    keep.append(dict(panel=pname, conv=conv, band=bd, cad=cad, CAGR=g.CAGR,
                                     Sharpe=g.Sharpe, MaxDD=g.MaxDD, H1=g.H1, H2=g.H2, OOS=oos,
                                     Turnover=g.Turnover,
                                     path4a=bool(g.H1 > b.H1 and g.H2 > b.H2 and g.MaxDD >= b.MaxDD),
                                     path4b=all(bars.values()),
                                     failing=",".join(k for k, v in bars.items() if not v) or "-"))
    keep = pd.DataFrame(keep)
    keep.to_csv(f"{OUT}_keeppaths.csv", index=False)
    print(keep.to_string(index=False, **fmt))
    print(f"\n4a passes: {int(keep.path4a.sum())}/{len(keep)}   4b passes: {int(keep.path4b.sum())}/{len(keep)}")
    if keep.path4b.any():
        print("\n4b passes:")
        print(keep[keep.path4b].to_string(index=False, **fmt))
    print("\nBinding bar census over 4b failures:")
    print(pd.Series([x for f in keep.loc[~keep.path4b, "failing"] for x in f.split(",")]
                    ).value_counts().to_string())


if __name__ == "__main__":
    main()
