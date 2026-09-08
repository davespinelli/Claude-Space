#!/usr/bin/env python3
"""Idea 206 — does U56 + REBASED/POS survive its OWN book's static-gross ladder?

Idea 196's PARKed by-product: idea 2's top-20 EW composite book (gross 0.75, weekly, t+1) with
the score tilted by `comp + m * rankpct(REBASED)` clears 4b at all three tilt strengths on U56
and improves the standing 4b candidate on Sharpe, CAGR, MaxDD and turnover at once.  Idea 206
asks the only question that can make it real: **is the tilt anything a gross change does not
already buy?**  Idea 423 (2026-09-08) showed the gross dial is ~pure exposure (99.6% of dCAGR,
97.6% of dMaxDD, dSharpe -0.0006), so a tilt whose whole content is exposure must be reproducible
by re-grossing the UNTILTED control.

Pre-registration (fixed before any number was read):
  * Book, verbatim from idea 196/193/181: composite = mean of rank-pct(MOM, R6, R3), NO vol
    scaler; eligibility = close > 200d MA AND vol20 < 0.60; top N=20 equal weight at gross/N;
    weekly cadence; weights at close t applied t+1.
  * ARM      TILT(m):    score = comp + m * rankpct(px / px[first bar]),  gross 0.75.
  * CONTROL  LADDER(g):  score = comp (untilted),                        gross g.
  * TWO tuned parameters, no more: m in {0.20, 0.50, 1.00}; g in {0.500, 0.625, 0.750, 0.875,
    1.000}.  15 combos x 3 panels x 2 rungs = 90 grid points, every one reported.
  * Zero-parameter matched-risk controls (derived by bisection, never fitted): g_vol matches the
    control's annualised vol to the tilt's; g_dd matches its MaxDD.  Mean realised gross is
    reported for both arms (the tilt cannot change it — same eligibility, same count).
  * Rule 8: (m, g) chosen on IS <= 2016-12-31 by IS Sharpe, 2017-01-01.. read once.
  * Both KEEP paths: 4a vs live RULES v2 (cost-matched), 4b vs SPY (phi 0.70, delta 0.60).
  * Panels: U56, broad136, SMALL439 (44 tickers with max_1d_move >= 1.0 dropped; SURVIVORSHIP:
    current constituents only, no delistings — data/SMALL_PANEL_README.md).  Rungs 10 / 25 bps.

Metric convention is idea 196's verbatim (260-bar warm-up skip, `px.index[260]:`) so its published
numbers are a binding reproduction gate.  Deterministic, no network.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest as engine_backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-08_does-REBASED-POS-survive-the-gross-ladder-on-U56_cloud"
OUT = ROOT / "research" / "backtests"
N, GROSS0, FREQ, MAX_VOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
GS = [0.500, 0.625, 0.750, 0.875, 1.000]
COSTS = [10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); _lines.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 196's fast_backtest verbatim (asserted == engine.backtest in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def first_valid_row(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


class Book:
    """Idea 196's Book, verbatim."""
    def __init__(self, name, px, tradable):
        self.name, self.px = name, px
        self.tradable = [c for c in px.columns if c in tradable]
        self.comp = comp_score(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        m = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(self.tradable)]
        if drop: m[drop] = False
        self.elig = m
        self.rebased = rankpct(px / first_valid_row(px))
        self.st = px.index[260]                      # idea 196's warm-up skip, verbatim

    def weights(self, score, gross):
        rank = score.where(self.elig).rank(axis=1, ascending=False)
        return (rank <= N).astype(float) * (gross / N)

    def run(self, score, gross, cost_bps=0.0):
        r = fast_backtest(self.px, self.weights(score, gross), cost_bps=cost_bps)
        return {k: v.loc[self.st:] for k, v in r.items()}   # idea 196 truncates at index[260]


def row_stats(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", r.loc[:IS_END]), ("OOS", r.loc[OOS_LO:])):
        mm = metrics(x)
        out[f"CAGR_{tag}"] = mm["CAGR"]; out[f"Sharpe_{tag}"] = mm["Sharpe"]
        out[f"MaxDD_{tag}"] = mm["MaxDD"]; out[f"Vol_{tag}"] = mm["Vol"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy, oos=True):
    ok = (row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
          and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"] and row["CAGR_F"] >= PHI * spy["CAGR_F"])
    if oos:
        ok = ok and (row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                     and row["MaxDD_OOS"] >= DELTA * spy["MaxDD_OOS"]
                     and row["CAGR_OOS"] >= PHI * spy["CAGR_OOS"])
    return bool(ok)


def bisect_gross(book, target, fn, cost_bps=0.0, lo=0.05, hi=3.0, tol=1e-9, iters=45):
    """Solve for the control gross g whose fn(stats) equals `target`. Zero tuned parameters.
    Standard bisection with cached endpoints (one backtest per iteration)."""
    def f(g):
        r = book.run(book.comp, g, 0.0)
        return fn(row_stats(r["returns"] - r["turnover"] * cost_bps / 1e4)) - target
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return np.nan, np.nan
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if abs(fm) < tol:
            return mid, fm + target
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    g = 0.5 * (lo + hi)
    return g, f(g) + target


def main():
    P("=" * 110); P(f"IDEA 206 — {STAMP}"); P("=" * 110)

    px56 = load_universe()
    pxb = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"SMALL: {len([c for c in pxs.columns if c!='SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} tradable "
      "(SURVIVORSHIP: current constituents only, no delistings — data/SMALL_PANEL_README.md)")
    pxs = pxs[s_stk + ["SPY"]].dropna(how="all").ffill()

    books = {"u56": Book("U56", px56, {c for c in px56.columns if c != "SPY"}),
             "broad136": Book("B136", pxb, {c for c in pxb.columns if c != "SPY"}),
             "small439": Book("SMALL439", pxs, set(s_stk))}
    for k, b in books.items():
        P(f"panel {k:9s} {b.px.shape[1]:4d} cols ({len(b.tradable)} tradable)  "
          f"{b.px.index[0].date()} .. {b.px.index[-1].date()}  ({len(b.px)} rows)")

    # ---------------- G1: vectorised twin vs engine.backtest
    P("\n--- G1  fast_backtest vs engine.backtest ---")
    worst = 0.0
    for k, b in books.items():
        w = b.weights(b.comp + 1.0 * b.rebased, 0.75)
        a = engine_backtest(b.px, w, cost_bps=10, freq=FREQ)["returns"]
        c = fast_backtest(b.px, w, 10.0)["returns"]
        d = float(np.abs(a - c).max()); worst = max(worst, d)
        P(f"  {k:9s} max|diff| = {d:.3e}")
    P(f"  G1 worst = {worst:.3e} -> {'PASS' if worst < 1e-12 else 'FAIL'}")
    assert worst < 1e-12

    # ---------------- G2: RULES v1 on u56 @10 bps, idea 196's published digits
    P("\n--- G2  RULES v1 on u56 @10bps (idea 196: 6.45305% / 0.66418 / -13.82780%) ---")
    rv1 = fast_backtest(px56, rules_v1_weights(px56), 10.0)["returns"].loc[px56.index[260]:]
    m1 = metrics(rv1)
    P(f"  {m1['CAGR']*100:.5f}% / {m1['Sharpe']:.5f} / {m1['MaxDD']*100:.5f}%")
    P(f"  deviation vs idea 196 (2026-09-05 price vintage): dCAGR "
      f"{(m1['CAGR']-0.0645305)*100:+.5f} pp, dSharpe {m1['Sharpe']-0.66418:+.5f}, dMaxDD "
      f"{(m1['MaxDD']+0.1382780)*100:+.7f} pp.  MaxDD is the shape statistic and is unchanged to "
      "1e-7; the CAGR/Sharpe drift is the data vintage (data/prices.csv has been re-cached since), "
      "so it is REPORTED, not asserted away.  The construction gate is the MaxDD digit.")
    assert abs(m1["MaxDD"] + 0.1382780) < 1e-6, "RULES v1 shape does not reproduce"
    assert abs(m1["CAGR"] - 0.0645305) < 5e-4 and abs(m1["Sharpe"] - 0.66418) < 5e-3

    # ---------------- G3: idea 196's published by-product arm
    P("\n--- G3  U56 + REBASED/POS m=1.00, gross 0.75 @10bps "
      "(idea 196: 13.30% / 1.1327 / -18.44%, halves 1.189/1.107, OOS 1.2007 / 15.60%, 7.9x/yr) ---")
    res = books["u56"].run(books["u56"].comp + 1.0 * books["u56"].rebased, 0.75, 10.0)
    s = row_stats(res["returns"])
    yrs = len(res["returns"]) / 252
    P(f"  {s['CAGR_F']:.2%} / {s['Sharpe_F']:.4f} / {s['MaxDD_F']:.2%}  halves "
      f"{s['Sharpe_H1']:.3f}/{s['Sharpe_H2']:.3f}  OOS {s['Sharpe_OOS']:.4f} / {s['CAGR_OOS']:.2%}  "
      f"turn {res['turnover'].sum()/yrs:.1f}x/yr")

    # ---------------- benchmarks
    P("\n--- benchmarks (idea 196's window convention: 260-bar warm-up skip) ---")
    bench = {}
    for k, b in books.items():
        spy = row_stats(b.px["SPY"].pct_change().fillna(0.0).loc[b.st:])
        bench[(k, "spy")] = spy
        for cb in COSTS:
            bench[(k, "v2", cb)] = row_stats(
                fast_backtest(b.px, rules_v2_weights(b.px), cb)["returns"].loc[b.st:])
        P(f"  {k:9s} SPY  full {spy['CAGR_F']:7.2%} / {spy['Sharpe_F']:.4f} / {spy['MaxDD_F']:7.2%}  "
          f"halves {spy['Sharpe_H1']:.3f}/{spy['Sharpe_H2']:.3f}  |  OOS {spy['CAGR_OOS']:7.2%} / "
          f"{spy['Sharpe_OOS']:.4f} / {spy['MaxDD_OOS']:7.2%}")
        for cb in COSTS:
            v = bench[(k, "v2", cb)]
            P(f"  {k:9s} RULES v2 @{int(cb)}bps full {v['CAGR_F']:7.2%} / {v['Sharpe_F']:.4f} / "
              f"{v['MaxDD_F']:7.2%}  halves {v['Sharpe_H1']:.3f}/{v['Sharpe_H2']:.3f}  |  OOS "
              f"{v['CAGR_OOS']:7.2%} / {v['Sharpe_OOS']:.4f} / {v['MaxDD_OOS']:7.2%}")

    # ---------------- the grid: 3 m x 5 g x 3 panels x 2 rungs
    P("\n" + "=" * 110)
    P("THE GRID — TILT(m) at gross 0.75  vs  untilted CONTROL on its own static-gross LADDER(g)")
    P("3 m x 5 g x 3 panels x 2 rungs = 90 points, ALL reported")
    P("=" * 110)
    rows = []
    for k, b in books.items():
        spy = bench[(k, "spy")]
        yrs = len(b.px.loc[b.st:]) / 252
        ctl0 = {g: b.run(b.comp, g, 0.0) for g in GS}
        tilt0 = {m: b.run(b.comp + m * b.rebased, 0.75, 0.0) for m in MS}
        for m in MS:
            for g in GS:
                for cb in COSTS:
                    tr = tilt0[m]["returns"] - tilt0[m]["turnover"] * cb / 1e4
                    cr = ctl0[g]["returns"] - ctl0[g]["turnover"] * cb / 1e4
                    t, c = row_stats(tr), row_stats(cr)
                    v2 = bench[(k, "v2", cb)]
                    rows.append(dict(
                        panel=k, m=m, g=g, cost_bps=cb,
                        tilt_CAGR=t["CAGR_F"], tilt_Sharpe=t["Sharpe_F"], tilt_MaxDD=t["MaxDD_F"],
                        tilt_H1=t["Sharpe_H1"], tilt_H2=t["Sharpe_H2"], tilt_Vol=t["Vol_F"],
                        tilt_IS_Sharpe=t["Sharpe_IS"], tilt_OOS_CAGR=t["CAGR_OOS"],
                        tilt_OOS_Sharpe=t["Sharpe_OOS"], tilt_OOS_MaxDD=t["MaxDD_OOS"],
                        ctl_CAGR=c["CAGR_F"], ctl_Sharpe=c["Sharpe_F"], ctl_MaxDD=c["MaxDD_F"],
                        ctl_H1=c["Sharpe_H1"], ctl_H2=c["Sharpe_H2"], ctl_Vol=c["Vol_F"],
                        ctl_IS_Sharpe=c["Sharpe_IS"], ctl_OOS_CAGR=c["CAGR_OOS"],
                        ctl_OOS_Sharpe=c["Sharpe_OOS"], ctl_OOS_MaxDD=c["MaxDD_OOS"],
                        dSharpe=t["Sharpe_F"] - c["Sharpe_F"],
                        dSharpe_OOS=t["Sharpe_OOS"] - c["Sharpe_OOS"],
                        tilt_turn=tilt0[m]["turnover"].sum() / yrs,
                        ctl_turn=ctl0[g]["turnover"].sum() / yrs,
                        tilt_meangross=tilt0[m]["gross"].mean(), ctl_meangross=ctl0[g]["gross"].mean(),
                        tilt_4a=pass4a(t, v2), tilt_4b=pass4b(t, spy),
                        ctl_4a=pass4a(c, v2), ctl_4b=pass4b(c, spy)))
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    for k in books:
        for cb in COSTS:
            sub = grid[(grid.panel == k) & (grid.cost_bps == cb)]
            P(f"\n--- {k} @ {int(cb)} bps ---")
            P(f"{'m':>5} {'g':>6} | {'TILT CAGR':>9} {'Shp':>7} {'MaxDD':>8} {'turn':>5} "
              f"| {'CTL CAGR':>9} {'Shp':>7} {'MaxDD':>8} {'turn':>5} | {'dShp':>8} {'dShpOOS':>8} "
              f"| tilt4a/4b ctl4a/4b")
            for _, x in sub.iterrows():
                P(f"{x.m:5.2f} {x.g:6.3f} | {x.tilt_CAGR:9.2%} {x.tilt_Sharpe:7.4f} {x.tilt_MaxDD:8.2%} "
                  f"{x.tilt_turn:5.1f} | {x.ctl_CAGR:9.2%} {x.ctl_Sharpe:7.4f} {x.ctl_MaxDD:8.2%} "
                  f"{x.ctl_turn:5.1f} | {x.dSharpe:+8.4f} {x.dSharpe_OOS:+8.4f} | "
                  f"{'Y' if x.tilt_4a else '.'}{'Y' if x.tilt_4b else '.'}        "
                  f"{'Y' if x.ctl_4a else '.'}{'Y' if x.ctl_4b else '.'}")

    P(f"\nGRID TOTALS (90 points): tilt 4a {int(grid.tilt_4a.sum())} / 4b {int(grid.tilt_4b.sum())} "
      f"| control-ladder 4a {int(grid.ctl_4a.sum())} / 4b {int(grid.ctl_4b.sum())}")
    P(f"dSharpe(tilt - control) over 90 points: mean {grid.dSharpe.mean():+.4f} "
      f"[{grid.dSharpe.min():+.4f} .. {grid.dSharpe.max():+.4f}], positive in "
      f"{int((grid.dSharpe>0).sum())}/90; OOS mean {grid.dSharpe_OOS.mean():+.4f}, positive in "
      f"{int((grid.dSharpe_OOS>0).sum())}/90")
    same = grid[grid.g == 0.750]
    P(f"mean realised gross, tilt vs control at g=0.75: max|diff| = "
      f"{float((same.tilt_meangross - same.ctl_meangross).abs().max()):.3e}  "
      f"-> the tilt cannot be a gross change (same eligibility, same count)")

    # ---------------- matched-risk bisection (zero tuned parameters)
    P("\n" + "=" * 110)
    P("MATCHED-RISK CONTROL — solve the control's gross so it carries the TILT's risk (bisection)")
    P("=" * 110)
    mr = []
    for k, b in books.items():
        spy = bench[(k, "spy")]
        for m in MS:
            t0 = b.run(b.comp + m * b.rebased, 0.75, 0.0)
            for cb in COSTS:
                t = row_stats(t0["returns"] - t0["turnover"] * cb / 1e4)
                gv, hitv = bisect_gross(b, t["Vol_F"], lambda s: s["Vol_F"], cost_bps=cb)
                gd, hitd = bisect_gross(b, t["MaxDD_F"], lambda s: s["MaxDD_F"], cost_bps=cb)
                out = dict(panel=k, m=m, cost_bps=cb, tilt_Vol=t["Vol_F"], tilt_MaxDD=t["MaxDD_F"],
                           tilt_CAGR=t["CAGR_F"], tilt_Sharpe=t["Sharpe_F"],
                           tilt_OOS_CAGR=t["CAGR_OOS"], tilt_OOS_Sharpe=t["Sharpe_OOS"],
                           g_volmatch=gv, g_ddmatch=gd)
                for tag, gg in (("vol", gv), ("dd", gd)):
                    if np.isnan(gg):
                        continue
                    c0 = b.run(b.comp, gg, 0.0)
                    c = row_stats(c0["returns"] - c0["turnover"] * cb / 1e4)
                    out[f"ctl{tag}_CAGR"] = c["CAGR_F"]; out[f"ctl{tag}_Sharpe"] = c["Sharpe_F"]
                    out[f"ctl{tag}_MaxDD"] = c["MaxDD_F"]; out[f"ctl{tag}_Vol"] = c["Vol_F"]
                    out[f"ctl{tag}_OOS_CAGR"] = c["CAGR_OOS"]; out[f"ctl{tag}_OOS_Sharpe"] = c["Sharpe_OOS"]
                    out[f"ctl{tag}_4b"] = pass4b(c, spy)
                    out[f"d{tag}_CAGR"] = t["CAGR_F"] - c["CAGR_F"]
                    out[f"d{tag}_Sharpe"] = t["Sharpe_F"] - c["Sharpe_F"]
                mr.append(out)
                P(f"{k:9s} m={m:.2f} {int(cb):2d}bps | TILT {t['CAGR_F']:6.2%}/{t['Sharpe_F']:.4f}/"
                  f"{t['MaxDD_F']:7.2%} vol {t['Vol_F']:.4f} | vol-matched CTL g*={gv:.4f} "
                  f"{out.get('ctlvol_CAGR', np.nan):6.2%}/{out.get('ctlvol_Sharpe', np.nan):.4f}/"
                  f"{out.get('ctlvol_MaxDD', np.nan):7.2%} (dCAGR {out.get('dvol_CAGR', np.nan):+.2%}, "
                  f"dShp {out.get('dvol_Sharpe', np.nan):+.4f}) | dd-matched g*={gd:.4f} "
                  f"dCAGR {out.get('ddd_CAGR', np.nan):+.2%} dShp {out.get('ddd_Sharpe', np.nan):+.4f}")
    mrd = pd.DataFrame(mr); mrd.to_csv(OUT / f"{STAMP}.matched.csv", index=False)
    P(f"\nmatched-risk summary over {len(mrd)} cells:")
    for tag, lab in (("vol", "vol-matched"), ("dd", "MaxDD-matched")):
        P(f"  {lab:14s} dCAGR mean {mrd[f'd{tag}_CAGR'].mean():+.2%} "
          f"[{mrd[f'd{tag}_CAGR'].min():+.2%} .. {mrd[f'd{tag}_CAGR'].max():+.2%}], positive in "
          f"{int((mrd[f'd{tag}_CAGR']>0).sum())}/{len(mrd)}   |   dSharpe mean "
          f"{mrd[f'd{tag}_Sharpe'].mean():+.4f} [{mrd[f'd{tag}_Sharpe'].min():+.4f} .. "
          f"{mrd[f'd{tag}_Sharpe'].max():+.4f}], positive in "
          f"{int((mrd[f'd{tag}_Sharpe']>0).sum())}/{len(mrd)}")
        P(f"  {lab:14s} control clears 4b in {int(mrd[f'ctl{tag}_4b'].sum())}/{len(mrd)} cells")

    # ---------------- rule 8
    P("\n" + "=" * 110)
    P("RULE 8 WALK-FORWARD — (m, g) chosen on IS <= 2016-12-31 by IS Sharpe, 2017-.. read once")
    P("=" * 110)
    wf = []
    for k in books:
        spy = bench[(k, "spy")]
        for cb in COSTS:
            sub = grid[(grid.panel == k) & (grid.cost_bps == cb)]
            tp = sub.loc[sub.tilt_IS_Sharpe.idxmax()]
            cp = sub.loc[sub.ctl_IS_Sharpe.idxmax()]
            v2 = bench[(k, "v2", cb)]
            t_row = {"Sharpe_H1": tp.tilt_H1, "Sharpe_H2": tp.tilt_H2, "MaxDD_F": tp.tilt_MaxDD,
                     "CAGR_F": tp.tilt_CAGR, "Sharpe_OOS": tp.tilt_OOS_Sharpe,
                     "MaxDD_OOS": tp.tilt_OOS_MaxDD, "CAGR_OOS": tp.tilt_OOS_CAGR}
            oos4b_t = (tp.tilt_OOS_Sharpe > spy["Sharpe_OOS"]
                       and tp.tilt_OOS_MaxDD >= DELTA * spy["MaxDD_OOS"]
                       and tp.tilt_OOS_CAGR >= PHI * spy["CAGR_OOS"])
            oos4b_c = (cp.ctl_OOS_Sharpe > spy["Sharpe_OOS"]
                       and cp.ctl_OOS_MaxDD >= DELTA * spy["MaxDD_OOS"]
                       and cp.ctl_OOS_CAGR >= PHI * spy["CAGR_OOS"])
            oos4a_t = (tp.tilt_OOS_Sharpe > v2["Sharpe_OOS"] and tp.tilt_OOS_MaxDD >= v2["MaxDD_OOS"])
            wf.append(dict(panel=k, cost_bps=cb, pick_m=tp.m, pick_g=cp.g,
                           tilt_IS_Sharpe=tp.tilt_IS_Sharpe, ctl_IS_Sharpe=cp.ctl_IS_Sharpe,
                           tilt_OOS_CAGR=tp.tilt_OOS_CAGR, tilt_OOS_Sharpe=tp.tilt_OOS_Sharpe,
                           tilt_OOS_MaxDD=tp.tilt_OOS_MaxDD,
                           ctl_OOS_CAGR=cp.ctl_OOS_CAGR, ctl_OOS_Sharpe=cp.ctl_OOS_Sharpe,
                           ctl_OOS_MaxDD=cp.ctl_OOS_MaxDD,
                           v2_OOS_Sharpe=v2["Sharpe_OOS"], v2_OOS_CAGR=v2["CAGR_OOS"],
                           v2_OOS_MaxDD=v2["MaxDD_OOS"], spy_OOS_Sharpe=spy["Sharpe_OOS"],
                           spy_OOS_CAGR=spy["CAGR_OOS"], spy_OOS_MaxDD=spy["MaxDD_OOS"],
                           tilt_oos4b=oos4b_t, ctl_oos4b=oos4b_c, tilt_oos4a=oos4a_t,
                           dSharpe_OOS=tp.tilt_OOS_Sharpe - cp.ctl_OOS_Sharpe))
            P(f"\n{k} @ {int(cb)} bps   IS picks: tilt m={tp.m:.2f} (IS Shp {tp.tilt_IS_Sharpe:.4f}) | "
              f"control g={cp.g:.3f} (IS Shp {cp.ctl_IS_Sharpe:.4f})")
            P(f"   OOS TILT     {tp.tilt_OOS_CAGR:7.2%} / {tp.tilt_OOS_Sharpe:.4f} / {tp.tilt_OOS_MaxDD:7.2%}")
            P(f"   OOS CONTROL  {cp.ctl_OOS_CAGR:7.2%} / {cp.ctl_OOS_Sharpe:.4f} / {cp.ctl_OOS_MaxDD:7.2%}"
              f"   -> dSharpe_OOS {tp.tilt_OOS_Sharpe - cp.ctl_OOS_Sharpe:+.4f}")
            P(f"   OOS RULES v2 {v2['CAGR_OOS']:7.2%} / {v2['Sharpe_OOS']:.4f} / {v2['MaxDD_OOS']:7.2%}")
            P(f"   OOS SPY      {spy['CAGR_OOS']:7.2%} / {spy['Sharpe_OOS']:.4f} / {spy['MaxDD_OOS']:7.2%}"
              f"   [4b bars: CAGR >= {PHI*spy['CAGR_OOS']:.2%}, MaxDD >= {DELTA*spy['MaxDD_OOS']:.2%}]")
            P(f"   OOS 4b: tilt {'PASS' if oos4b_t else 'FAIL'} | control-ladder "
              f"{'PASS' if oos4b_c else 'FAIL'}   OOS 4a(tilt) {'PASS' if oos4a_t else 'FAIL'}")
    pd.DataFrame(wf).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_lines) + "\n")
    P(f"\nwrote {STAMP}.{{grid,matched,walkforward}}.csv and .console.txt")


if __name__ == "__main__":
    main()
