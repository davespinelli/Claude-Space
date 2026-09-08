#!/usr/bin/env python3
"""Idea 423 — price the U56 FULL-GROSS MA book against RULES v2 on TWO dials only.

Pre-registration (fixed before any number was read):
  * Book = RULES v2's own construction with ONE clause deleted: the 0.75 de-gross.
    Hold every instrument priced that day whose close is inside/above the 200d MA band
    (band_state, hysteresis, band FIXED at v2's 3%), equally weighted at `gross`/N of NAV,
    N = instruments priced that day; gated-out weight goes to CASH (de-gross, never re-spread).
    At (gross=0.75, cadence='W') this IS `baseline.rules_v2_weights` -> reproduction gate G2.
  * TWO tuned parameters, no more:  gross in {0.500,0.625,0.750,0.875,1.000}
                                    cadence in {W, M, Q}
    = 15 arms, reported at EVERY value, selected at none outside the rule-8 walk-forward.
  * Panels: U56 (universe.json), B136 (universe_broad.json), SMALL439 (sub-$2B, tickers with
    max_1d_move >= 1.0 dropped per data/small_meta.csv).  Rungs: 10 and 25 bps.
    15 x 3 x 2 = 90 grid points, all printed.
  * Rule 8: dials chosen on IS <= 2016-12-31 by IS Sharpe, 2017-01-01.. read once.
  * Both KEEP paths evaluated: 4a vs live RULES v2 (cost-matched), 4b vs SPY.
  * De-gross pricing (ideas 296/304): the deleted clause is priced with the zero-parameter
    CONSTANT-LEVERAGE REPLAY  c * r(gross=0.75), c = 1.00/0.75, same cadence, same rung ->
    exposure leg; residual = actual(g=1.00) - replay.

Costs 10/25 bps per unit turnover, weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network. Writes .grid.csv, .walkforward.csv, .degross.csv, .console.txt.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-08_price-the-U56-FULL-GROSS-MA-book-against-RULES-v2-on-2-dials-only_cloud"
OUT = ROOT / "research" / "backtests"
GROSSES = [0.500, 0.625, 0.750, 0.875, 1.000]
CADENCES = ["W", "M", "Q"]
RUNGS = [10, 25]
BAND = 0.03
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, weights, cost_bps, freq):
    """Vectorised twin of engine.backtest (same drift, same t+1 application, same costs).

    Within a rebalance segment the unnormalised position values grow with the prices and the
    cash leg is constant, so held_t = u_t / T_t with T_t = sum(u_t) + cash; the day's gross
    return is sum(u_t * r_t) / T_t.  Gated against engine.backtest below (G1)."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)                       # growth factor at END of day i
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])     # ... at START of day i
    port = np.zeros(n); turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])                            # drifted held weights entering day i
    starts = np.flatnonzero(mask)
    bounds = list(zip(starts, list(starts[1:]) + [n]))
    for i0, i1 in bounds:
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])         # unnormalised position values
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    port = port - turn * cost_bps / 1e4
    r = pd.Series(port, index=px.index)
    return {"returns": r, "turnover": pd.Series(turn, index=px.index)}


def deg_weights(px, gross, band=BAND):
    """RULES v2 construction with `gross` as a free dial (v2 itself is gross=0.75)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def ma_weights(px, gross):
    """Idea 420's by-product: plain `close > 200d MA` gate (NO band), used only as gate G3."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(px > px.rolling(200).mean(), 0.0)


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    say(f"SMALL: dropped {len(bad & set(px.columns))} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv); {len(keep)-1} names + SPY remain")
    return px[keep]


def main():
    say("=" * 100)
    say(f"IDEA 423 — {STAMP}")
    say("=" * 100)

    panels = {}
    panels["u56"] = load_universe()
    panels["broad136"] = load_universe(broad=True)
    panels["small439"] = small_panel()
    for k, v in panels.items():
        say(f"panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")

    # ---------------- gate G1: vectorised twin vs engine.backtest
    say("\n--- G1  vectorised backtester vs engine.backtest ---")
    worst = 0.0
    for pk in panels:
        px = panels[pk]
        for g, fq in [(0.75, "W"), (1.00, "M"), (0.50, "Q")]:
            w = deg_weights(px, g)
            a = engine_backtest(px, w, cost_bps=10, freq=fq)["returns"]
            b = fast_backtest(px, w, 10, fq)["returns"]
            d = float(np.abs(a - b).max()); worst = max(worst, d)
            say(f"  {pk:9s} g={g:.3f} {fq}   max|diff| = {d:.3e}")
    say(f"  G1 worst = {worst:.3e}  -> {'PASS' if worst < 1e-12 else 'FAIL'}")
    assert worst < 1e-12, "vectorised twin does not reproduce the engine"

    # ---------------- gate G2: (g=0.75, W) is the live book, weight-for-weight
    say("\n--- G2  deg_weights(0.75, band=0.03) == baseline.rules_v2_weights ---")
    for pk, px in panels.items():
        d = float((deg_weights(px, 0.75) - rules_v2_weights(px)).abs().max().max())
        say(f"  {pk:9s} max|dW| = {d:.3e}")
        assert d == 0.0

    # ---------------- gate G3: idea 420's by-product headline (plain-MA gate, g=1.00, monthly)
    say("\n--- G3  idea 420 by-product reproduction (u56, plain MA gate, g=1.00, monthly) ---")
    px = panels["u56"]; start = px.index[260]
    r = fast_backtest(px, ma_weights(px, 1.00), 10, "M")["returns"].loc[start:]
    c, s, dd = stats(r)
    h1, h2 = halves(r)
    say(f"  full 10bps  {c:.2%} / {s:.4f} / {dd:.2%}  halves {h1:.3f}/{h2:.3f}   "
        f"(memo: 11.96% / 1.2126 / -15.49%, 1.249/1.179)")
    ro = fast_backtest(px, ma_weights(px, 1.00), 10, "M")["returns"].loc[OOS_START:]
    co, so, ddo = stats(ro)
    say(f"  OOS  10bps  {co:.2%} / {so:.4f} / {ddo:.2%}   (memo: 12.72% / 1.2750 / -15.49%)")

    # ---------------- benchmarks
    say("\n--- benchmarks (per panel, per rung; SPY is buy-and-hold, cost-free) ---")
    bench = {}
    for pk, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        for rung in RUNGS:
            v2 = fast_backtest(px, rules_v2_weights(px), rung, "W")["returns"]
            v1 = fast_backtest(px, rules_v1_weights(px), rung, "W")["returns"]
            bench[(pk, rung)] = {"v2": v2.loc[st:], "v1": v1.loc[st:], "spy": spy.loc[st:],
                                 "v2_oos": v2.loc[OOS_START:], "spy_oos": spy.loc[OOS_START:]}
            for nm in ("v2", "v1", "spy"):
                rr = bench[(pk, rung)][nm]
                c, s, dd = stats(rr); a, b = halves(rr)
                say(f"  {pk:9s} {rung:2d}bps {nm:3s}  full {c:7.2%} / {s:.4f} / {dd:7.2%}  halves {a:.3f}/{b:.3f}")
            for nm in ("v2_oos", "spy_oos"):
                rr = bench[(pk, rung)][nm]
                c, s, dd = stats(rr); a, b = halves(rr)
                say(f"  {pk:9s} {rung:2d}bps {nm:7s} OOS {c:7.2%} / {s:.4f} / {dd:7.2%}  halves {a:.3f}/{b:.3f}")

    # ---------------- the 90-point grid
    say("\n" + "=" * 100)
    say("THE GRID — 5 gross x 3 cadences x 3 panels x 2 rungs = 90 points, ALL reported")
    say("=" * 100)
    rows = []
    cache = {}
    for pk, px in panels.items():
        st = px.index[260]
        for g in GROSSES:
            w = deg_weights(px, g)
            for fq in CADENCES:
                for rung in RUNGS:
                    res = fast_backtest(px, w, rung, fq)
                    r_full = res["returns"].loc[st:]
                    r_is = res["returns"].loc[st:IS_END]
                    r_oos = res["returns"].loc[OOS_START:]
                    cache[(pk, g, fq, rung)] = res["returns"]
                    B = bench[(pk, rung)]
                    c, s, dd = stats(r_full); h1, h2 = halves(r_full)
                    ci, si, ddi = stats(r_is)
                    co, so, ddo = stats(r_oos); o1, o2 = halves(r_oos)
                    bc, bs, bdd = stats(B["v2"]); bh1, bh2 = halves(B["v2"])
                    sc, ss, sdd = stats(B["spy"]); sh1, sh2 = halves(B["spy"])
                    soc, sos, sodd = stats(B["spy_oos"])
                    # 4a: Sharpe > RULES v2 in BOTH halves and MaxDD no worse than v2
                    keep4a = (h1 > bh1) and (h2 > bh2) and (dd >= bdd)
                    # 4b: Sharpe > SPY both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% SPY's
                    keep4b_full = (h1 > sh1) and (h2 > sh2) and (dd >= 0.60 * sdd) and (c >= 0.70 * sc)
                    keep4b_oos = (so > sos) and (ddo >= 0.60 * sodd) and (co >= 0.70 * soc)
                    keep4b = keep4b_full and keep4b_oos
                    rows.append(dict(panel=pk, gross=g, cadence=fq, cost_bps=rung, band=BAND,
                                     CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2,
                                     IS_CAGR=ci, IS_Sharpe=si, IS_MaxDD=ddi,
                                     OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=ddo, OOS_H1=o1, OOS_H2=o2,
                                     turn_yr=float(res["turnover"].loc[st:].sum() / (len(r_full) / 252)),
                                     v2_Sharpe=bs, v2_H1=bh1, v2_H2=bh2, v2_MaxDD=bdd,
                                     spy_Sharpe=ss, spy_H1=sh1, spy_H2=sh2, spy_MaxDD=sdd, spy_CAGR=sc,
                                     keep4a=keep4a, keep4b_full=keep4b_full, keep4b_oos=keep4b_oos,
                                     keep4b=keep4b))
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    for pk in panels:
        for rung in RUNGS:
            sub = grid[(grid.panel == pk) & (grid.cost_bps == rung)]
            say(f"\n--- {pk} @ {rung} bps (band 3% fixed) ---")
            say(f"{'gross':>6} {'cad':>4} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} "
                f"| {'IS Shp':>7} | {'OOS CAGR':>8} {'OOS Shp':>7} {'OOS DD':>8} | {'turn':>5} | 4a 4b")
            for _, x in sub.iterrows():
                say(f"{x.gross:6.3f} {x.cadence:>4} | {x.CAGR:7.2%} {x.Sharpe:7.4f} {x.MaxDD:8.2%} "
                    f"{x.H1:6.3f} {x.H2:6.3f} | {x.IS_Sharpe:7.4f} | {x.OOS_CAGR:8.2%} {x.OOS_Sharpe:7.4f} "
                    f"{x.OOS_MaxDD:8.2%} | {x.turn_yr:5.2f} | "
                    f"{'Y' if x.keep4a else '.'}  {'Y' if x.keep4b else '.'}")

    say(f"\nGRID TOTALS: 4a {int(grid.keep4a.sum())}/90 | 4b(full) {int(grid.keep4b_full.sum())}/90 "
        f"| 4b(full+OOS) {int(grid.keep4b.sum())}/90 | BOTH PATHS {int((grid.keep4a & grid.keep4b).sum())}/90")

    # ---------------- rule 8 walk-forward
    say("\n" + "=" * 100)
    say("RULE 8 WALK-FORWARD — dials chosen on IS <= 2016-12-31 by IS Sharpe, 2017-.. read once")
    say("=" * 100)
    wf = []
    for pk in panels:
        for rung in RUNGS:
            sub = grid[(grid.panel == pk) & (grid.cost_bps == rung)]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            B = bench[(pk, rung)]
            v2c, v2s, v2dd = stats(B["v2_oos"]); v2h1, v2h2 = halves(B["v2_oos"])
            sc, ss, sdd = stats(B["spy_oos"]); sh1, sh2 = halves(B["spy_oos"])
            oos4a = (pick.OOS_H1 > v2h1) and (pick.OOS_H2 > v2h2) and (pick.OOS_MaxDD >= v2dd)
            oos4b = ((pick.OOS_H1 > sh1) and (pick.OOS_H2 > sh2) and (pick.OOS_Sharpe > ss)
                     and (pick.OOS_MaxDD >= 0.60 * sdd) and (pick.OOS_CAGR >= 0.70 * sc))
            wf.append(dict(panel=pk, cost_bps=rung, pick_gross=pick.gross, pick_cadence=pick.cadence,
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD, OOS_H1=pick.OOS_H1, OOS_H2=pick.OOS_H2,
                           v2_OOS_CAGR=v2c, v2_OOS_Sharpe=v2s, v2_OOS_MaxDD=v2dd,
                           spy_OOS_CAGR=sc, spy_OOS_Sharpe=ss, spy_OOS_MaxDD=sdd,
                           oos_keep4a=oos4a, oos_keep4b=oos4b))
            say(f"\n{pk} @ {rung} bps  IS pick: gross={pick.gross:.3f} cadence={pick.cadence} "
                f"(IS Sharpe {pick.IS_Sharpe:.4f})")
            say(f"   OOS pick     {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%}  "
                f"halves {pick.OOS_H1:.3f}/{pick.OOS_H2:.3f}")
            say(f"   OOS RULES v2 {v2c:7.2%} / {v2s:.4f} / {v2dd:7.2%}  halves {v2h1:.3f}/{v2h2:.3f}")
            say(f"   OOS SPY      {sc:7.2%} / {ss:.4f} / {sdd:7.2%}  halves {sh1:.3f}/{sh2:.3f}   "
                f"[4b bars: CAGR >= {0.70*sc:.2%}, MaxDD >= {0.60*sdd:.2%}]")
            say(f"   OOS 4a {'PASS' if oos4a else 'FAIL'}   OOS 4b {'PASS' if oos4b else 'FAIL'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------- de-gross clause pricing (ideas 296/304 decomposition)
    say("\n" + "=" * 100)
    say("PRICING THE DELETED DE-GROSS CLAUSE — constant-leverage replay c = 1.00/0.75 (idea 296/304)")
    say("REPLAY = c * r(gross=0.75) at the same cadence and rung; residual = actual(g=1.00) - REPLAY")
    say("=" * 100)
    dg = []
    c_lev = 1.00 / 0.75
    for pk, px in panels.items():
        st = px.index[260]
        for fq in CADENCES:
            for rung in RUNGS:
                r075 = cache[(pk, 0.750, fq, rung)].loc[st:]
                r100 = cache[(pk, 1.000, fq, rung)].loc[st:]
                rep = c_lev * r075
                a = dict(zip("csd", stats(r100)))
                b = dict(zip("csd", stats(r075)))
                p = dict(zip("csd", stats(rep)))
                # share of the actual move that the pure-exposure replay accounts for
                shr = lambda k: (p[k] - b[k]) / (a[k] - b[k]) if abs(a[k] - b[k]) > 1e-12 else np.nan
                dg.append(dict(panel=pk, cadence=fq, cost_bps=rung,
                               CAGR_075=b["c"], CAGR_100=a["c"], CAGR_replay=p["c"],
                               Sharpe_075=b["s"], Sharpe_100=a["s"], Sharpe_replay=p["s"],
                               MaxDD_075=b["d"], MaxDD_100=a["d"], MaxDD_replay=p["d"],
                               dCAGR=a["c"] - b["c"], dSharpe=a["s"] - b["s"], dMaxDD=a["d"] - b["d"],
                               exposure_share_CAGR=shr("c"), exposure_share_MaxDD=shr("d"),
                               resid_CAGR=a["c"] - p["c"], resid_Sharpe=a["s"] - p["s"],
                               resid_MaxDD=a["d"] - p["d"],
                               max_abs_ret_diff=float((r100 - rep).abs().max()),
                               ret_corr=float(np.corrcoef(r100, rep)[0, 1])))
                x = dg[-1]
                say(f"{pk:9s} {fq} {rung:2d}bps | g=0.75 {b['c']:6.2%}/{b['s']:.4f}/{b['d']:7.2%} "
                    f"-> g=1.00 {a['c']:6.2%}/{a['s']:.4f}/{a['d']:7.2%} | REPLAY {p['c']:6.2%}/{p['s']:.4f}/{p['d']:7.2%} "
                    f"| exposure share CAGR {x['exposure_share_CAGR']:6.1%} DD {x['exposure_share_MaxDD']:6.1%} "
                    f"| resid Shp {x['resid_Sharpe']:+.4f}")
    dgd = pd.DataFrame(dg); dgd.to_csv(OUT / f"{STAMP}.degross.csv", index=False)
    say(f"\nde-gross summary over {len(dgd)} (panel x cadence x rung) cells:")
    say(f"  dSharpe(g=1.00 vs 0.75): mean {dgd.dSharpe.mean():+.4f}  min {dgd.dSharpe.min():+.4f}  "
        f"max {dgd.dSharpe.max():+.4f}  positive in {int((dgd.dSharpe>0).sum())}/{len(dgd)}")
    say(f"  exposure share of dCAGR : mean {dgd.exposure_share_CAGR.mean():.1%}  "
        f"[{dgd.exposure_share_CAGR.min():.1%} .. {dgd.exposure_share_CAGR.max():.1%}]")
    say(f"  exposure share of dMaxDD: mean {dgd.exposure_share_MaxDD.mean():.1%}  "
        f"[{dgd.exposure_share_MaxDD.min():.1%} .. {dgd.exposure_share_MaxDD.max():.1%}]")
    say(f"  residual Sharpe (actual - replay): mean {dgd.resid_Sharpe.mean():+.4f}  "
        f"max|.| {dgd.resid_Sharpe.abs().max():.4f}")
    say(f"  daily-return corr(actual, replay): min {dgd.ret_corr.min():.6f}")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\nwrote {STAMP}.{{grid,walkforward,degross}}.csv and .console.txt")


if __name__ == "__main__":
    main()
