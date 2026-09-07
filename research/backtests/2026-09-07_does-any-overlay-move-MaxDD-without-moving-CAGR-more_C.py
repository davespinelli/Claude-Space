#!/usr/bin/env python3
"""Idea 351: does ANY risk overlay in the record move MaxDD without moving CAGR more?

Idea 41 priced ONE overlay's depth axis (the breadth gate, cut depth) at a median **-0.90 pp of
drawdown per pp of CAGR** -- i.e. deepening the cut made the drawdown WORSE while it burned return.
The queue's question is whether that is a property of that one instrument or of the whole class:
census every risk overlay the record has run, on ONE ruler, on the SAME base books, panels and cost
rungs, and rank them.  If the GROSS dial is the only family with a positive exchange rate, that is a
negative-result clause PROTOCOL should carry and a large part of the queue can be retired.

THE RULER (one number per grid point, defined before any run):
    dCAGR_pp = 100 * (CAGR_overlay - CAGR_control)                  (usually negative: what you pay)
    dDD_pp   = 100 * (|MaxDD_control| - |MaxDD_overlay|)            (positive: drawdown you buy)
    ratio    = dDD_pp / (-dCAGR_pp)      -- pp of drawdown bought per pp of CAGR given up.
Sign convention: ratio > 0 means the overlay buys drawdown for return; ratio > 1 means it buys more
drawdown than the CAGR it costs; ratio <= 0 means it burns return and buys NO drawdown (or makes the
drawdown worse), which is idea 41's finding for the depth axis.  Points where the overlay is free or
better (dCAGR_pp >= -0.05) cannot be put on this ruler at all and are counted separately in [E] --
counting them as "infinite ratio" would be the only way to make a family look good by accident.
Every point's control is its OWN un-overlaid book on the same panel, same n, same rung.

  TUNED PARAMETERS -- exactly two, fixed before any number was read:
     1. n, the base book's position count, in {3, 20}: idea 41's own concentrated book (where the
        -0.90 was measured) and the top-20 book of the 2026-09-04 KEEP 4b candidate.
     2. the overlay's own dial (each family has exactly ONE dial, listed below).
  NOT TUNED / reported axes: panel (U56 / B136 / SMALL439), cost rung (0 / 10 / 25 bps), and the
  overlay FAMILY -- the census reports all five families at every point, which is the deliverable.

FAMILIES (5), each vs the same overlay-OFF control (mult == 1, weekly):
  GROSS    constant exposure multiplier m in {0.85, 0.75, 0.625, 0.50}                (idea 42/84's dial)
  VOLTGT   mult = clip(target / vol20(book), 0, 1), target in {0.20, 0.15, 0.12, 0.10}; no leverage
  BREADTH  mult = d while panel breadth < B, B PINNED at 0.30, d in {0.50, 0.25, 0.00}  (idea 40/41)
  DDCTRL   mult = 0 while the book's own drawdown is worse than -X, X in {0.10, 0.15, 0.20, 0.25}
  CADENCE  rebalance frequency in {M, Q}; the control's weekly cadence is the same book at freq W

All overlay signals are computed through day t and executed at t+1 (protocol 2).  Multiplier
overlays pay the rung's cost on |d(mult)| * GROSS of notional on the day the switch takes effect --
idea 41's convention, reproduced to the published digit in section [0].  DDCTRL's trigger reads the
book's SHADOW (un-overlaid) drawdown, not the overlaid equity: an overlay that zeroes exposure
freezes its own equity and could never re-enter otherwise, and a signal that depends on the dial
would not be comparable across dials.

RULE 8 walk-forward: the (n, family, dial) menu -- the overlay-OFF control INCLUDED -- is chosen on
2008-2016 at 10 bps by (a) the census's own ruler and (b) IS Sharpe, then 2017-2026 is read once,
against the control anchor, the OOS-best cell (regret), RULES v2 (live) and SPY.  Both KEEP paths
are evaluated at every one of the grid's points: 4a vs the LIVE RULES v2 book, 4b vs SPY.

REPRODUCTION GATES (section [0], asserted before any new number is read):
  * the derived rung r(c) = r(0) - turnover*c/1e4 equals engine.backtest(cost_bps=c) to 1e-12;
  * idea 41/40's published U56 rows: NONE n=3 21.9%/1.04/-25.8% (1.01/1.06), NONE n=5
    16.5%/0.95/-21.6%, and the near-miss BREADTH n=3 B=30% d=0.5 21.0%/1.03/-20.6% (0.96/1.09);
  * the GROSS family is exactly linear in the un-overlaid book (m * r), checked to 1e-12.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so the drawdown
LEVELS are optimistic; this census reads DIFFERENCES between an overlay and its own control on the
same panel, which is far less exposed to that bias than a level test, but the 4b drawdown cap in
section [C] is still a level test.  The small panel drops the 44 tickers with max_1d_move >= 1.0.
(2) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136.
(3) CADENCE is not a risk overlay in the same sense as the other four -- it changes the book, not its
exposure -- and is carried because the queue named it; it is labelled at every point of use.
(4) The ruler is a ratio of two differences; where the denominator is small it is unstable, which is
exactly why [E] quarantines |dCAGR| < 0.05pp instead of dividing by it.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                            # noqa
from engine import backtest, metrics                                                   # noqa

SLUG = "2026-09-07_does-any-overlay-move-MaxDD-without-moving-CAGR-more_C"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS = 0.60, 0.75
NS = [3, 20]                        # tuned parameter 1
B_FIXED = 0.30                      # PINNED (idea 40's pre-chosen threshold), never tuned
FAMILIES = {                        # tuned parameter 2: the dial, one per family
    "GROSS":   [0.85, 0.75, 0.625, 0.50],
    "VOLTGT":  [0.20, 0.15, 0.12, 0.10],
    "BREADTH": [0.50, 0.25, 0.00],
    "DDCTRL":  [0.10, 0.15, 0.20, 0.25],
    "CADENCE": ["M", "Q"],
}
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
FREE_EPS = 0.05                     # |dCAGR| below this pp is quarantined, not divided by


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the base book (fixed, never tuned)
def base_weights(px, n, drop_spy=False):
    """Idea 40/41's OFF book: top-n eligible by the v1 composite WITHOUT /sqrt(vol20), w = GROSS/n."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL)
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def breadth(px, drop_spy=False):
    cols = [c for c in px.columns if not (drop_spy and c == "SPY")]
    q = px[cols]
    above = q > q.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


# ---------------------------------------------------------------- overlays
def mult_series(fam, dial, r0, br_lag):
    """The exposure multiplier, decided at t and already shifted to execute at t+1."""
    if fam == "GROSS":
        return pd.Series(float(dial), index=r0.index)
    if fam == "VOLTGT":
        v = (r0.rolling(20).std() * np.sqrt(252)).shift(1)
        return (float(dial) / v).clip(upper=1.0).fillna(1.0)
    if fam == "BREADTH":
        on = br_lag.reindex(r0.index).fillna(False)
        return pd.Series(np.where(on.values, float(dial), 1.0), index=r0.index)
    if fam == "DDCTRL":
        eq = (1 + r0).cumprod()
        dd = eq / eq.cummax() - 1                       # SHADOW drawdown of the un-overlaid book
        return pd.Series(np.where(dd.shift(1).fillna(0.0).values < -float(dial), 0.0, 1.0), index=r0.index)
    raise ValueError(fam)


def apply_mult(r0, t0, mult, c):
    """Rung c with BOTH the book's turnover and the overlay's switching cost re-charged."""
    dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))       # idea 41's convention
    return mult.values * (r0.values - t0.values * c / 1e4) - dm * GROSS * c / 1e4, dm


# ---------------------------------------------------------------- metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def summarise(r, spy, base10):
    m = metrics(r); h1, h2 = hs(r)
    ok_b, fb = bars_4b(r, spy); ok_a, fa = bars_4a(r, base10)
    mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                pass4b=ok_b, fail4b=",".join(fb), pass4a=ok_a, fail4a=",".join(fa))


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson on average ranks."""
    a, b = pd.Series(a).rank(), pd.Series(b).rank()
    return float(a.corr(b))


def ratio_of(dcagr_pp, ddd_pp):
    """pp of drawdown bought per pp of CAGR given up; NaN where the overlay costs ~nothing."""
    if dcagr_pp >= -FREE_EPS:
        return np.nan
    return ddd_pp / (-dcagr_pp)


def cstar_of(make_r, hi=200):
    """Largest whole bps at which all five 4b bars still hold; scans upward, stops at the first
    failure (so a point that fails at 0 bps costs one evaluation)."""
    c, bar = None, "0bps"
    for k in range(0, hi + 1):
        ok, f = make_r(k)
        if ok:
            c = k
        else:
            bar = ",".join(f); break
    return c, bar


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print("Ruler: pp of MaxDD bought per pp of CAGR given up, vs each point's OWN un-overlaid control.")
    print(f"Tuned: n in {NS} x one dial per family.  Families: {list(FAMILIES)}.")
    print(f"Reported axes: panel (U56/B136/SMALL439), cost rung {COSTS} bps.  ALL points reported.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv = OUT / f"{SLUG}.grid.csv"
    if RESUME and gcsv.exists():
        analyse(pd.read_csv(gcsv))
        return

    rows = []
    for pname, px in panels.items():
        drop_spy = (pname == "SMALL439")
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        br_lag = (breadth(px, drop_spy) < B_FIXED).shift(1)
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f}")
        print(f"    4b bars: H1 > {s1:.3f}, H2 > {s2:.3f}, OOS > {so['Sharpe']:.3f}, "
              f"MaxDD <= {0.60*abs(ms_['MaxDD']):.2%}, CAGR >= {0.70*ms_['CAGR']:.2%}")

        bres = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
        b0, bt0 = bres["returns"].loc[start:], bres["turnover"].loc[start:]
        base10 = b0 - bt0 * 10 / 1e4
        bm = metrics(base10); bb1, bb2 = hs(base10)
        print(f"    RULES v2 (live, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {bb1:.3f}/{bb2:.3f}")

        for n in NS:
            w = base_weights(px, n, drop_spy)
            cad = {}
            for f in ["W"] + [d for d in FAMILIES["CADENCE"]]:
                res = backtest(px, w, cost_bps=0.0, freq=f)
                cad[f] = (res["returns"].loc[start:], res["turnover"].loc[start:])
            r0, t0 = cad["W"]
            cstar_cache = {}

            # ---- reproduction gates, U56 only, before any new number is read
            if pname == "U56" and n == 3:
                gate_checks(px, r0, t0, w, br_lag, start)

            for c in COSTS:
                ctl = r0 - t0 * c / 1e4
                cm = metrics(ctl)
                cs, csbar = (cstar_of(lambda k: bars_4b(r0 - t0 * k / 1e4, spy)) if c == COSTS[0]
                             else (cstar_cache[("CONTROL", "off")]))
                if c == COSTS[0]:
                    cstar_cache[("CONTROL", "off")] = (cs, csbar)
                rows.append(dict(panel=pname, n=n, family="CONTROL", dial="off", cost=c,
                                 ann_turnover=t0.sum() / cm["Years"], sw=0.0,
                                 dCAGR_pp=0.0, dDD_pp=0.0, dSharpe=0.0, ratio=np.nan,
                                 cstar=cs, cstar_bar=csbar,
                                 **summarise(ctl, spy, base10)))
                for fam, dials in FAMILIES.items():
                    for dial in dials:
                        if fam == "CADENCE":
                            rr, tt = cad[dial]
                            r = rr - tt * c / 1e4
                            sw, turn = 0.0, tt.sum() / metrics(r)["Years"]
                            mk = lambda k, rr=rr, tt=tt: bars_4b(rr - tt * k / 1e4, spy)
                        else:
                            mult = mult_series(fam, dial, r0, br_lag)
                            vals, dm = apply_mult(r0, t0, mult, c)
                            r = pd.Series(vals, index=r0.index)
                            sw = dm.sum(); turn = (mult * t0).sum() / metrics(r)["Years"]
                            mk = lambda k, mu=mult: bars_4b(
                                pd.Series(apply_mult(r0, t0, mu, k)[0], index=r0.index), spy)
                        if (fam, dial) not in cstar_cache:
                            cstar_cache[(fam, dial)] = cstar_of(mk)
                        cs, csbar = cstar_cache[(fam, dial)]
                        m = metrics(r)
                        dcagr = 100 * (m["CAGR"] - cm["CAGR"])
                        dddp = 100 * (abs(cm["MaxDD"]) - abs(m["MaxDD"]))
                        rows.append(dict(panel=pname, n=n, family=fam, dial=dial, cost=c,
                                         ann_turnover=turn, sw=sw,
                                         dCAGR_pp=dcagr, dDD_pp=dddp,
                                         dSharpe=m["Sharpe"] - cm["Sharpe"],
                                         ratio=ratio_of(dcagr, dddp),
                                         cstar=cs, cstar_bar=csbar,
                                         **summarise(r, spy, base10)))
            print(f"    n={n}: {sum(1 for x in rows if x['panel']==pname and x['n']==n)} rows "
                  f"(control + {sum(len(v) for v in FAMILIES.values())} overlays) x {len(COSTS)} rungs")

    g = pd.DataFrame(rows)
    g.to_csv(gcsv, index=False)
    print(f"\n[grid written] {gcsv.name}  ({len(g)} rows)")
    analyse(g)


def gate_checks(px, r0, t0, w, br_lag, start):
    print("\n[0] REPRODUCTION GATES (U56, n=3) -- asserted before any new number is read")
    # G1: derived rung identity
    for c in (10, 25):
        direct = backtest(px, w, cost_bps=float(c), freq="W")["returns"].loc[start:]
        err = float((direct - (r0 - t0 * c / 1e4)).abs().max())
        print(f"    G1 rung identity @{c} bps: max|derived - engine| = {err:.3e}")
        assert err < 1e-12, err
    # G2: idea 40/41's published un-gated control at 10 bps
    ctl = r0 - t0 * 10 / 1e4
    m = metrics(ctl); h1, h2 = hs(ctl)
    print(f"    G2 NONE n=3 @10 bps: {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%} "
          f"({h1:.3f}/{h2:.3f})  vs published 21.9%/1.04/-25.8% (1.01/1.06)")
    assert abs(m["CAGR"] - 0.2185) < 5e-4 and abs(m["Sharpe"] - 1.036) < 5e-3 \
        and abs(m["MaxDD"] + 0.2581) < 5e-4
    # G3: the published n=5 control
    w5 = base_weights(px, 5)
    r5 = backtest(px, w5, cost_bps=10.0, freq="W")["returns"].loc[start:]
    m5 = metrics(r5)
    print(f"    G3 NONE n=5 @10 bps: {m5['CAGR']:.2%}/{m5['Sharpe']:.3f}/{m5['MaxDD']:.2%} "
          f" vs published 16.5%/0.95/-21.6%")
    assert abs(m5["CAGR"] - 0.1652) < 5e-4 and abs(m5["Sharpe"] - 0.950) < 5e-3
    # G4: idea 41's near-miss BREADTH cell, through THIS file's overlay machinery
    mult = mult_series("BREADTH", 0.50, r0, br_lag)
    vals, _ = apply_mult(r0, t0, mult, 10)
    rb = pd.Series(vals, index=r0.index); mb = metrics(rb); b1, b2 = hs(rb)
    print(f"    G4 BREADTH n=3 B=30% d=0.5 @10 bps: {mb['CAGR']:.2%}/{mb['Sharpe']:.3f}/"
          f"{mb['MaxDD']:.2%} ({b1:.3f}/{b2:.3f})  vs published 21.0%/1.03/-20.6% (0.96/1.09)")
    assert abs(mb["CAGR"] - 0.2095) < 5e-4 and abs(mb["Sharpe"] - 1.026) < 5e-3 \
        and abs(mb["MaxDD"] + 0.2055) < 5e-4
    # G5: GROSS is exactly linear in the un-overlaid book at 0 bps
    mg = mult_series("GROSS", 0.50, r0, br_lag)
    vg, _ = apply_mult(r0, t0, mg, 0)
    err = float(np.abs(vg - 0.50 * r0.values).max())
    print(f"    G5 GROSS linearity @0 bps: max|m*r - overlay| = {err:.3e}")
    assert err < 1e-12
    print("    ALL GATES EXACT.")


# ---------------------------------------------------------------- analysis
def fam_order(g):
    return [f for f in FAMILIES if f in set(g["family"])]


def analyse(g):
    ov = g[g.family != "CONTROL"]
    print("\n" + "=" * 100)
    print("[A] THE RULER, by family and cost rung: pp of MaxDD bought per pp of CAGR given up")
    print("    (median over panels x n x dials; 'n_priced' = points with a real price, "
          f"|dCAGR| >= {FREE_EPS}pp; the rest are in [E])")
    for c in COSTS:
        sub = ov[ov.cost == c]
        print(f"\n  --- cost {c} bps")
        print(f"    {'family':9s} {'pts':>4s} {'n_priced':>8s} {'med ratio':>10s} {'best':>8s} "
              f"{'worst':>8s} {'med dCAGR':>10s} {'med dDD':>8s} {'ratio>0':>8s} {'ratio>1':>8s} {'dDD>0':>7s}")
        for fam in fam_order(ov):
            s = sub[sub.family == fam]
            pr = s.dropna(subset=["ratio"])
            med = pr["ratio"].median() if len(pr) else np.nan
            print(f"    {fam:9s} {len(s):4d} {len(pr):8d} {med:10.3f} "
                  f"{(pr['ratio'].max() if len(pr) else np.nan):8.3f} "
                  f"{(pr['ratio'].min() if len(pr) else np.nan):8.3f} "
                  f"{s['dCAGR_pp'].median():10.3f} {s['dDD_pp'].median():8.3f} "
                  f"{(pr['ratio'] > 0).sum():4d}/{len(pr):<3d} {(pr['ratio'] > 1).sum():4d}/{len(pr):<3d} "
                  f"{(s['dDD_pp'] > 0).sum():3d}/{len(s):<3d}")

    print("\n[A2] the same ruler split by panel and n (10 bps), median ratio")
    sub = ov[ov.cost == 10]
    piv = sub.dropna(subset=["ratio"]).pivot_table(index="family", columns=["panel", "n"],
                                                   values="ratio", aggfunc="median")
    print(piv.reindex(fam_order(ov)).to_string(float_format=lambda x: f"{x:7.3f}"))

    print("\n[B] RANKING (10 bps, all panels x n x dials pooled) -- the census's answer")
    sub = ov[ov.cost == 10].dropna(subset=["ratio"])
    rk = sub.groupby("family")["ratio"].agg(["count", "median", "mean", "max"]).sort_values(
        "median", ascending=False)
    rk["frac>0"] = sub.groupby("family")["ratio"].apply(lambda x: (x > 0).mean())
    rk["frac>1"] = sub.groupby("family")["ratio"].apply(lambda x: (x > 1).mean())
    print(rk.to_string(float_format=lambda x: f"{x:.3f}"))
    pos = [f for f in rk.index if rk.loc[f, "median"] > 0]
    print(f"\n    families with a POSITIVE median exchange rate at 10 bps: {pos if pos else 'NONE'}")
    print(f"    families whose median buys MORE drawdown than the CAGR it costs (>1): "
          f"{[f for f in rk.index if rk.loc[f, 'median'] > 1] or 'NONE'}")

    print("\n[C] every point, ranked by ratio (10 bps) -- top 15 and bottom 10 of "
          f"{len(sub)} priced points")
    cols = ["panel", "n", "family", "dial", "dCAGR_pp", "dDD_pp", "ratio", "dSharpe",
            "CAGR", "Sharpe", "MaxDD", "cstar", "pass4b", "fail4b", "pass4a"]
    srt = sub.sort_values("ratio", ascending=False)
    fmt = lambda d: d.to_string(index=False, float_format=lambda x: f"{x:.3f}")
    print(fmt(srt[cols].head(15)))
    print("    ...")
    print(fmt(srt[cols].tail(10)))

    print("\n[I] IS THE GROSS DIAL THE NUMERAIRE?  For a constant exposure multiplier m the exchange")
    print("    rate is close to the book's OWN |MaxDD| / CAGR -- arithmetic, not a market call.  An")
    print("    overlay is only worth having if it beats that number on the same book, so every")
    print("    non-GROSS point is scored against the GROSS family's median ratio on its OWN")
    print("    (panel, n, rung).  The GROSS ratio's spread across its four dials is printed as the")
    print("    numeraire's own stability.")
    for c in COSTS:
        sub = ov[ov.cost == c]
        print(f"\n  --- cost {c} bps")
        print(f"    {'panel':9s} {'n':>3s} {'book |DD|/CAGR':>15s} {'GROSS med':>10s} {'GROSS spread':>13s} "
              + "  ".join(f"{f:>13s}" for f in fam_order(ov) if f != "GROSS"))
        wins = {f: [0, 0] for f in fam_order(ov) if f != "GROSS"}
        for (pn, nn), q in sub.groupby(["panel", "n"]):
            ctl = g[(g.panel == pn) & (g.n == nn) & (g.cost == c) & (g.family == "CONTROL")].iloc[0]
            numer = abs(ctl["MaxDD"]) / ctl["CAGR"] if ctl["CAGR"] > 0 else np.nan
            gq = q[(q.family == "GROSS")].dropna(subset=["ratio"])
            gmed = gq["ratio"].median() if len(gq) else np.nan
            spread = (gq["ratio"].max() - gq["ratio"].min()) if len(gq) else np.nan
            cells = []
            for f in wins:
                fq = q[q.family == f].dropna(subset=["ratio"])
                if not len(fq) or not np.isfinite(gmed):
                    cells.append(f"{'n/a':>13s}"); continue
                w = int((fq["ratio"] > gmed).sum()); wins[f][0] += w; wins[f][1] += len(fq)
                cells.append(f"{fq['ratio'].median():+7.2f} {w}/{len(fq):<3d}"[:13].rjust(13))
            print(f"    {pn:9s} {nn:3d} {numer:15.2f} {gmed:10.2f} {spread:13.3f} " + "  ".join(cells))
        print("    beats the de-grossing numeraire (pooled over panels x n, priced points only): "
              + ", ".join(f"{f} {w}/{t}" for f, (w, t) in wins.items()))

    print("\n[D] KEEP-path census over the FULL grid (all families, dials, panels, n, rungs)")
    for c in COSTS:
        s = g[g.cost == c]
        print(f"    {c:2d} bps: 4b {int(s['pass4b'].sum())}/{len(s)}   4a {int(s['pass4a'].sum())}/{len(s)}")
    for c in COSTS:
        s = g[(g.cost == c) & g.pass4b]
        if len(s):
            print(f"    4b passes @{c} bps:")
            print(fmt(s[["panel", "n", "family", "dial", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "ratio", "cstar", "cstar_bar"]]))
    fb = g[(g.cost == 10) & ~g.pass4b]["fail4b"].str.split(",").explode().value_counts()
    print(f"    binding 4b bars @10 bps (count of failures by bar): {dict(fb)}")

    print("\n[E] the quarantine: points the ruler cannot price, and FREE drawdown")
    for c in COSTS:
        s = g[(g.cost == c) & (g.family != "CONTROL")]
        free = s[(s.dCAGR_pp >= -FREE_EPS)]
        good = free[free.dDD_pp > 0.05]
        print(f"    {c:2d} bps: {len(free)}/{len(s)} points cost <= {FREE_EPS}pp of CAGR; "
              f"of those {len(good)} also cut drawdown by > 0.05pp")
        if len(good):
            print(fmt(good[["panel", "n", "family", "dial", "dCAGR_pp", "dDD_pp", "dSharpe", "pass4b"]]))

    print("\n[F] does the ruler's sign depend on the DIAL's depth? (10 bps, median ratio by dial)")
    sub = ov[ov.cost == 10]
    for fam in fam_order(ov):
        s = sub[sub.family == fam]
        parts = []
        for d in FAMILIES[fam]:
            q = s[s.dial.astype(str) == str(d)].dropna(subset=["ratio"])
            parts.append(f"{d}: {q['ratio'].median():+.2f} (dDD {s[s.dial.astype(str)==str(d)]['dDD_pp'].median():+.2f})"
                         if len(q) else f"{d}: n/a")
        print(f"    {fam:9s} " + " | ".join(parts))

    print("\n[G] RULE 8 walk-forward: menu = every (n, family, dial) INCLUDING the control, "
          "chosen on IS (<=2016) at 10 bps, OOS (2017-) read once.  *The IS-ratio chooser ranks OVERLAYS "
          "only -- the control is the ratio's own reference and has no ratio -- so its control "
          "comparison below is the honest read of whether the ruler beats doing nothing.")
    s10 = g[g.cost == 10].copy()
    s10["key"] = s10.apply(lambda r: f"n={r['n']} {r['family']}:{r['dial']}", axis=1)
    for pname in s10.panel.unique():
        p = s10[s10.panel == pname]
        ctl = p[p.family == "CONTROL"]
        # IS ruler needs IS-specific deltas, recomputed from the stored IS metrics
        ctl_is = {int(nn): ctl[ctl.n == nn].iloc[0] for nn in p.n.unique()}
        def is_ratio(r):
            c0 = ctl_is[int(r["n"])]
            dc = 100 * (r["IS_CAGR"] - c0["IS_CAGR"]); dd = 100 * (abs(c0["IS_MaxDD"]) - abs(r["IS_MaxDD"]))
            return ratio_of(dc, dd)
        p = p.assign(is_ratio=p.apply(is_ratio, axis=1))
        by_sharpe = p.loc[p["IS_Sharpe"].idxmax()]
        prc = p.dropna(subset=["is_ratio"])
        by_ratio = prc.loc[prc["is_ratio"].idxmax()] if len(prc) else by_sharpe
        best_oos = p.loc[p["OOS_Sharpe"].idxmax()]
        print(f"\n    --- {pname}")
        for label, r in [("IS-Sharpe chooser", by_sharpe), ("IS-ratio chooser*", by_ratio),
                         ("OOS-best (hindsight)", best_oos)]:
            print(f"      {label:22s} {r['key']:22s} OOS CAGR {r['OOS_CAGR']:7.2%}  "
                  f"Sharpe {r['OOS_Sharpe']:.3f}  MaxDD {r['OOS_MaxDD']:7.2%}")
        for nn in sorted(p.n.unique()):
            c0 = ctl[ctl.n == nn].iloc[0]
            print(f"      {'control anchor n=' + str(nn):22s} {'(overlay OFF)':22s} "
                  f"OOS CAGR {c0['OOS_CAGR']:7.2%}  Sharpe {c0['OOS_Sharpe']:.3f}  "
                  f"MaxDD {c0['OOS_MaxDD']:7.2%}")
        for label, r in [("IS-Sharpe", by_sharpe), ("IS-ratio", by_ratio)]:
            c0 = ctl[ctl.n == int(r["n"])].iloc[0]
            print(f"      {label} chooser vs its own control: dSharpe {r['OOS_Sharpe']-c0['OOS_Sharpe']:+.3f}, "
                  f"dCAGR {100*(r['OOS_CAGR']-c0['OOS_CAGR']):+.2f}pp, "
                  f"dMaxDD {100*(abs(c0['OOS_MaxDD'])-abs(r['OOS_MaxDD'])):+.2f}pp | "
                  f"regret vs OOS-best {r['OOS_Sharpe']-best_oos['OOS_Sharpe']:+.3f}")

    print("\n[H] IS -> OOS stability of the ruler itself (10 bps): does an overlay's IS exchange "
          "rate predict its OOS one?")
    s = g[(g.cost == 10) & (g.family != "CONTROL")].copy()
    ctl = g[(g.cost == 10) & (g.family == "CONTROL")].set_index(["panel", "n"])
    def deltas(r, pre):
        c0 = ctl.loc[(r["panel"], r["n"])]
        dc = 100 * (r[pre + "CAGR"] - c0[pre + "CAGR"])
        dd = 100 * (abs(c0[pre + "MaxDD"]) - abs(r[pre + "MaxDD"]))
        return pd.Series({pre + "ratio": ratio_of(dc, dd), pre + "dDD": dd, pre + "dCAGR": dc})
    s = pd.concat([s, s.apply(lambda r: deltas(r, "IS_"), axis=1),
                   s.apply(lambda r: deltas(r, "OOS_"), axis=1)], axis=1)
    both = s.dropna(subset=["IS_ratio", "OOS_ratio"])
    print(f"    priced in BOTH halves: {len(both)} of {len(s)} points")
    print(f"    Spearman(IS ratio, OOS ratio) = {spearman(both['IS_ratio'], both['OOS_ratio']):+.3f}")
    print(f"    sign agreement (both > 0 or both <= 0): {(np.sign(both['IS_ratio'])==np.sign(both['OOS_ratio'])).mean():.1%}")
    print("    by family:")
    for fam in fam_order(s):
        q = both[both.family == fam]
        if len(q) < 3:
            print(f"      {fam:9s} n={len(q)} (too few to rank)"); continue
        print(f"      {fam:9s} n={len(q):3d}  IS med {q['IS_ratio'].median():+7.3f}  "
              f"OOS med {q['OOS_ratio'].median():+7.3f}  "
              f"rho {spearman(q['IS_ratio'], q['OOS_ratio']):+.3f}  "
              f"sign-agree {(np.sign(q['IS_ratio'])==np.sign(q['OOS_ratio'])).mean():.0%}")


if __name__ == "__main__":
    main()
