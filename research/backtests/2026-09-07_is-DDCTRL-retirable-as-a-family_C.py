#!/usr/bin/env python3
"""Idea 366: is DDCTRL (the equity stop) retirable as a FAMILY, or does a re-entry rule save it?

Idea 351 priced the DDCTRL overlay -- exposure to 0 while the book's own drawdown is worse than
-X -- at a median **-1.58 pp of drawdown bought per pp of CAGR given up** (3 of 18 priced points
positive at 10 bps) with a NEGATIVE median dDD: the stop sells the bottom and buys back higher, so
it burns return AND deepens the drawdown it was bought to fix.  That verdict was measured with ONE
re-entry rule (immediate: re-arm the moment the shadow drawdown recovers above -X).  Before the
record retires the family and PROTOCOL carries a 'no equity stop' clause, the queue asks the one
question that could rescue it: does ANY re-entry rule flip the sign, at the SAME trigger levels, on
the SAME two books?

  TUNED PARAMETERS -- exactly two, fixed before any number was read:
     1. trigger X in {0.10, 0.15, 0.20, 0.25}      -- idea 351's own dial, unchanged.
     2. re-entry lag k in {0, 1, 3, 5, 10, 21, 63} trading days of CONFIRMATION: once stopped out,
        the book re-enters only after the shadow drawdown has been above -X for k consecutive days.
        k = 0 IS idea 351's immediate rule and is asserted to reproduce its committed grid exactly.
  NOT TUNED / reported axes: n in {3, 20} (idea 351's two books), panel (U56 / B136 / SMALL439),
  cost rung (0 / 10 / 25 bps).  ALL 4 x 7 x 2 x 3 x 3 = 504 overlay points are written to the grid
  CSV and summarised; nothing is filtered out of the census.

THE RULER (identical to idea 351's, so the two files' numbers are directly comparable):
    dCAGR_pp = 100 * (CAGR_stop - CAGR_control)              (usually negative: what you pay)
    dDD_pp   = 100 * (|MaxDD_control| - |MaxDD_stop|)         (positive: drawdown you buy)
    ratio    = dDD_pp / (-dCAGR_pp)                           (pp of DD bought per pp of CAGR)
Points where the stop is free or better (dCAGR_pp >= -0.05) cannot be put on the ruler and are
quarantined in [E] rather than counted as infinite.  Every point's control is its OWN un-overlaid
book: same panel, same n, same weekly cadence, same rung.

THE NUMERAIRE BAR (idea 351's decision form, carried here): a constant exposure multiplier buys
drawdown at exactly the book's own |MaxDD| / CAGR at zero Sharpe cost.  A stop is only worth having
if it beats that free alternative, so every point is also scored against its own book's numeraire.

MECHANICS.  The stop's trigger reads the SHADOW (un-overlaid) drawdown of the base book, not the
overlaid equity -- an overlay that zeroes exposure freezes its own equity and could never re-enter
otherwise, and a signal that depended on the dial would not be comparable across dials.  This is
idea 351's convention, reproduced.  The state machine runs on the shadow drawdown through day t and
is shifted one day, so the switch executes at t+1 (protocol 2).  Switching costs are charged on
|d(mult)| * GROSS of notional at the rung, idea 41's convention.

RULE 8 walk-forward: the (X, k) menu -- the stop-OFF control INCLUDED as a menu item -- is chosen on
2008-2016 at 10 bps by (a) the census ruler and (b) IS Sharpe, then 2017-2026 is read once against
the do-nothing control, the OOS-best cell (regret), RULES v2 (live) and SPY.  Both KEEP paths are
evaluated at every one of the 504 points: 4a vs the LIVE RULES v2 book, 4b vs SPY.

REPRODUCTION GATES (section [0], asserted before any new number is read):
  * derived rung r(c) = r(0) - turnover*c/1e4 equals engine.backtest(cost_bps=c) to 1e-12;
  * idea 40/41's published U56 controls: NONE n=3 21.9%/1.04/-25.8% (1.01/1.06), NONE n=5
    16.5%/0.95/-21.6%;
  * EVERY k=0 cell reproduces idea 351's committed DDCTRL grid rows (dCAGR_pp, dDD_pp, CAGR, MaxDD,
    Sharpe) to 1e-9 -- 72 cells, the full published DDCTRL block.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so drawdown LEVELS
are optimistic; the ruler reads DIFFERENCES against a control on the same panel, but the 4b DD cap
is still a level test.  SMALL439 drops the 44 tickers with max_1d_move >= 1.0.  (2) SMALL439 starts
2010-01-04, so its halves are not the same calendar halves as U56/B136.  (3) A longer k is a strictly
LATER re-entry: it cannot help a V-shaped recovery and can only help if drawdowns continue after the
first recovery day.  That asymmetry is the hypothesis being priced, not a bug.  (4) The ruler is a
ratio of two differences and is unstable where the denominator is small, which is why [E] quarantines
|dCAGR| < 0.05pp instead of dividing by it.

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

SLUG = "2026-09-07_is-DDCTRL-retirable-as-a-family_C"
PARENT = "2026-09-07_does-any-overlay-move-MaxDD-without-moving-CAGR-more_C"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS = 0.60, 0.75
NS = [3, 20]                                     # idea 351's two books (reported axis, not tuned)
TRIGGERS = [0.10, 0.15, 0.20, 0.25]              # tuned parameter 1 (idea 351's dial, unchanged)
LAGS = [0, 1, 3, 5, 10, 21, 63]                  # tuned parameter 2 (re-entry confirmation days)
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
FREE_EPS = 0.05                                  # |dCAGR| below this pp is quarantined


# ---------------------------------------------------------------- panels (idea 351's three)
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the base book (idea 40/41/351)
def base_weights(px, n, drop_spy=False):
    """Top-n eligible by the v1 composite WITHOUT /sqrt(vol20), w = GROSS/n."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL)
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


# ---------------------------------------------------------------- the stop, with a re-entry lag
def stop_mult(r0, trigger, lag):
    """Exposure multiplier for the equity stop with a k-day re-entry confirmation.

    Signal: dd_t = shadow drawdown of the UN-overlaid book through day t.  State machine:
        dd_t < -trigger            -> OUT (immediately), confirmation counter reset
        dd_t >= -trigger while OUT -> counter += 1; back IN once counter >= lag
    lag = 0 re-enters on the first recovered day, which is idea 351's immediate rule exactly.
    The state is then shifted one day so the switch executes at t+1.
    """
    eq = (1 + r0).cumprod()
    dd = (eq / eq.cummax() - 1).values
    state = np.ones(len(dd))
    cur, cnt = 1.0, 0
    for i in range(len(dd)):
        if dd[i] < -trigger:
            cur, cnt = 0.0, 0
        elif cur == 0.0:
            cnt += 1
            if cnt >= lag:
                cur = 1.0
        state[i] = cur
    s = pd.Series(state, index=r0.index).shift(1).fillna(1.0)
    return s


def apply_mult(r0, t0, mult, c):
    """Rung c with BOTH the book's turnover and the stop's switching cost re-charged."""
    dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))       # idea 41/351's convention
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


def ratio_of(dcagr_pp, ddd_pp):
    if dcagr_pp >= -FREE_EPS:
        return np.nan
    return ddd_pp / (-dcagr_pp)


def spearman(a, b):
    a, b = pd.Series(a).rank(), pd.Series(b).rank()
    return float(a.corr(b))


def fmt(x, p=3):
    return "nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{p}f}"


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print("Q: does ANY re-entry rule flip the sign of the equity stop's DD-per-CAGR exchange rate?")
    print(f"Tuned: trigger X in {TRIGGERS} x re-entry lag k in {LAGS} days.  k=0 == idea 351.")
    print(f"Reported axes: n in {NS}, panel (U56/B136/SMALL439), rung {COSTS} bps.  ALL points reported.")

    gcsv = OUT / f"{SLUG}.grid.csv"
    if RESUME and gcsv.exists():
        analyse(pd.read_csv(gcsv))
        return

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    parent = pd.read_csv(OUT / f"{PARENT}.grid.csv")

    rows, gates = [], []
    for pname, px in panels.items():
        drop_spy = (pname == "SMALL439")
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
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
            res = backtest(px, w, cost_bps=0.0, freq="W")
            r0, t0 = res["returns"].loc[start:], res["turnover"].loc[start:]

            if pname == "U56" and n == 3:
                gate_checks(px, r0, t0, w, start)

            for c in COSTS:
                ctl = r0 - t0 * c / 1e4
                cm = metrics(ctl)
                numeraire = abs(cm["MaxDD"]) / cm["CAGR"] if cm["CAGR"] > 0 else np.nan
                rows.append(dict(panel=pname, n=n, trigger=np.nan, lag=np.nan, arm="CONTROL", cost=c,
                                 ann_turnover=t0.sum() / cm["Years"], switches=0.0, days_out=0.0,
                                 episodes=0.0, dCAGR_pp=0.0, dDD_pp=0.0, dSharpe=0.0, ratio=np.nan,
                                 numeraire=numeraire, beats_numeraire=False,
                                 **summarise(ctl, spy, base10)))
                for X in TRIGGERS:
                    for k in LAGS:
                        mult = stop_mult(r0, X, k)
                        vals, dm = apply_mult(r0, t0, mult, c)
                        r = pd.Series(vals, index=r0.index)
                        m = metrics(r)
                        dcagr = 100 * (m["CAGR"] - cm["CAGR"])
                        dddp = 100 * (abs(cm["MaxDD"]) - abs(m["MaxDD"]))
                        rat = ratio_of(dcagr, dddp)
                        rows.append(dict(
                            panel=pname, n=n, trigger=X, lag=k, arm=f"X{X:.2f}_k{k}", cost=c,
                            ann_turnover=(mult * t0).sum() / m["Years"], switches=dm.sum(),
                            days_out=float((mult == 0).mean()),
                            episodes=float(((mult == 0) & (mult.shift(1) != 0)).sum()),
                            dCAGR_pp=dcagr, dDD_pp=dddp, dSharpe=m["Sharpe"] - cm["Sharpe"],
                            ratio=rat, numeraire=numeraire,
                            beats_numeraire=bool(rat > numeraire) if not np.isnan(rat) and not np.isnan(numeraire) else False,
                            **summarise(r, spy, base10)))

                        if c == 10 and k == 0:                       # gate against the parent grid
                            pdial = pd.to_numeric(parent.dial, errors="coerce")  # CADENCE dials are strings
                            pr = parent[(parent.panel == pname) & (parent.n == n) &
                                        (parent.family == "DDCTRL") & (np.isclose(pdial.fillna(-9), X)) &
                                        (parent.cost == 10)]
                            if len(pr) == 1:
                                pr = pr.iloc[0]
                                gates.append(dict(panel=pname, n=n, X=X,
                                                  d_cagr=abs(dcagr - pr.dCAGR_pp),
                                                  d_dd=abs(dddp - pr.dDD_pp),
                                                  d_S=abs(m["Sharpe"] - pr.Sharpe),
                                                  d_lvl=abs(m["CAGR"] - pr.CAGR)))
            print(f"    n={n}: {len(TRIGGERS)*len(LAGS)} arms x {len(COSTS)} rungs written")

    gd = pd.DataFrame(gates)
    worst = gd[["d_cagr", "d_dd", "d_S", "d_lvl"]].max().max()
    print(f"\n[0d] PARENT GRID GATE: {len(gd)} k=0 cells vs idea 351's committed DDCTRL rows, "
          f"worst abs diff {worst:.3e}")
    assert worst < 1e-9, gd.sort_values("d_cagr").tail()

    g = pd.DataFrame(rows)
    g.to_csv(gcsv, index=False)
    print(f"[grid written] {gcsv.name}  ({len(g)} rows)")
    analyse(g)


def gate_checks(px, r0, t0, w, start):
    print("\n[0] REPRODUCTION GATES (U56, n=3) -- asserted before any new number is read")
    for c in (10, 25):
        direct = backtest(px, w, cost_bps=float(c), freq="W")["returns"].loc[start:]
        err = float((direct - (r0 - t0 * c / 1e4)).abs().max())
        print(f"    G1 rung identity @{c} bps: max|derived - engine| = {err:.3e}")
        assert err < 1e-12, err
    ctl = r0 - t0 * 10 / 1e4
    m = metrics(ctl); h1, h2 = hs(ctl)
    print(f"    G2 NONE n=3 @10 bps: {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%} "
          f"({h1:.3f}/{h2:.3f})  vs published 21.9%/1.04/-25.8% (1.01/1.06)")
    assert abs(m["CAGR"] - 0.2185) < 5e-4 and abs(m["Sharpe"] - 1.036) < 5e-3 \
        and abs(m["MaxDD"] + 0.2581) < 5e-4
    w5 = base_weights(px, 5)
    r5 = backtest(px, w5, cost_bps=10.0, freq="W")["returns"].loc[start:]
    m5 = metrics(r5)
    print(f"    G3 NONE n=5 @10 bps: {m5['CAGR']:.2%}/{m5['Sharpe']:.3f}/{m5['MaxDD']:.2%} "
          f" vs published 16.5%/0.95/-21.6%")
    assert abs(m5["CAGR"] - 0.1652) < 5e-4 and abs(m5["Sharpe"] - 0.950) < 5e-3


# ---------------------------------------------------------------- analysis
def analyse(g):
    ov = g[g.arm != "CONTROL"].copy()
    ct = g[g.arm == "CONTROL"].copy()

    print("\n[A] THE HEADLINE: does any re-entry lag flip the sign of the exchange rate?")
    print("    Ruler = pp of MaxDD bought per pp of CAGR given up, vs each point's own control.")
    for c in COSTS:
        sub = ov[ov.cost == c]
        print(f"\n    --- {c} bps ({len(sub)} points; {sub.ratio.notna().sum()} priceable) ---")
        print("      lag |  median ratio  n>0/n |  median dDD_pp  n>0/n |  median dCAGR_pp | med dSharpe")
        for k in LAGS:
            s = sub[sub.lag == k]
            pr = s.ratio.dropna()
            print(f"      {k:>3} | {fmt(pr.median()):>13}  {int((pr>0).sum()):>2}/{len(pr):<3} | "
                  f"{fmt(s.dDD_pp.median()):>13}  {int((s.dDD_pp>0).sum()):>2}/{len(s):<3} | "
                  f"{fmt(s.dCAGR_pp.median()):>15} | {fmt(s.dSharpe.median())}")
        base = sub[sub.lag == 0].ratio.dropna()
        best = max(LAGS, key=lambda k: sub[sub.lag == k].ratio.dropna().median()
                   if len(sub[sub.lag == k].ratio.dropna()) else -9e9)
        bs = sub[sub.lag == best].ratio.dropna()
        print(f"      -> best lag by median ratio: k={best} ({fmt(bs.median())}) vs k=0 "
              f"({fmt(base.median())}); sign flipped: {bool(bs.median() > 0)}")

    print("\n[B] SIGN-FLIP CENSUS: per (panel, n, trigger) cell at 10 bps, does ANY lag give ratio > 0?")
    sub = ov[ov.cost == 10]
    cells, flipped, flipped_from_neg = 0, 0, 0
    print("      panel      n     X | k=0 ratio | best k | best ratio | any k>0? | dDD>0 at best k")
    for (p, n, X), s in sub.groupby(["panel", "n", "trigger"]):
        cells += 1
        r0r = s[s.lag == 0].ratio.iloc[0]
        pr = s.dropna(subset=["ratio"])
        if len(pr) == 0:
            print(f"      {p:<9} {n:>2} {X:>5.2f} | {fmt(r0r):>9} |    --  |         -- | "
                  f"{'no (all free)':>8} | --")
            continue
        b = pr.loc[pr.ratio.idxmax()]
        anyp = bool((pr.ratio > 0).any())
        flipped += anyp
        if anyp and not (r0r > 0):
            flipped_from_neg += 1
        print(f"      {p:<9} {n:>2} {X:>5.2f} | {fmt(r0r):>9} | {int(b.lag):>6} | {b.ratio:>10.3f} | "
              f"{str(anyp):>8} | {b.dDD_pp:>6.2f}")
    print(f"    -> {flipped} of {cells} (panel, n, trigger) cells have SOME lag with ratio > 0; "
          f"{flipped_from_neg} of those were negative at k=0 (a genuine rescue).")

    print("\n[C] KEEP paths at every point (all 504 overlay points + controls)")
    for c in COSTS:
        s = ov[ov.cost == c]; cc = ct[ct.cost == c]
        print(f"    {c:>2} bps: overlay 4b {int(s.pass4b.sum())}/{len(s)}, 4a {int(s.pass4a.sum())}/{len(s)}"
              f" | control 4b {int(cc.pass4b.sum())}/{len(cc)}, 4a {int(cc.pass4a.sum())}/{len(cc)}")
    p4 = ov[(ov.cost == 10) & (ov.pass4b)]
    if len(p4):
        print("    4b passes @10 bps:")
        print(p4[["panel", "n", "trigger", "lag", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "ratio"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        print("    4b passes @10 bps: NONE")
    fb = ov[(ov.cost == 10) & (~ov.pass4b)].fail4b.value_counts()
    print(f"    binding 4b bars @10 bps (failing-bar sets): {dict(fb.head(8))}")

    print("\n[D] THE NUMERAIRE BAR (idea 351): a constant exposure multiplier buys DD at |MaxDD|/CAGR")
    for c in COSTS:
        s = ov[ov.cost == c]
        print(f"    {c:>2} bps: {int(s.beats_numeraire.sum())} of {len(s)} stop points beat their "
              f"book's own numeraire ({int(s.ratio.notna().sum())} priceable)")
    bn = ov[(ov.cost == 10) & (ov.beats_numeraire)]
    if len(bn):
        print(bn[["panel", "n", "trigger", "lag", "ratio", "numeraire", "dSharpe"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n[E] QUARANTINE: points too cheap to put on the ruler (|dCAGR| < 0.05 pp)")
    s = ov[ov.cost == 10]
    free = s[s.dCAGR_pp >= -FREE_EPS]
    print(f"    @10 bps: {len(free)} of {len(s)}; of those, dDD_pp > 0 in {int((free.dDD_pp>0).sum())} "
          f"(median dDD {fmt(free.dDD_pp.median())} pp). These are stops that never fire, or fire "
          f"almost never; a free overlay that buys nothing is not an instrument.")
    print(f"    fired-never count (days_out == 0): {int((s.days_out == 0).sum())} of {len(s)}")

    print("\n[F] MECHANISM: what the lag actually does (10 bps, pooled over panels/n/triggers)")
    print("      lag | mean days_out | mean episodes | mean switches | mean ann_turnover | mean dSharpe")
    for k in LAGS:
        s = ov[(ov.cost == 10) & (ov.lag == k)]
        print(f"      {k:>3} | {s.days_out.mean():>13.3f} | {s.episodes.mean():>13.1f} | "
              f"{s.switches.mean():>13.1f} | {s.ann_turnover.mean():>17.3f} | {s.dSharpe.mean():>11.3f}")
    print(f"    rank corr(lag, dSharpe) @10 bps = {spearman(ov[ov.cost==10].lag, ov[ov.cost==10].dSharpe):+.3f}")
    print(f"    rank corr(lag, dDD_pp)  @10 bps = {spearman(ov[ov.cost==10].lag, ov[ov.cost==10].dDD_pp):+.3f}")
    print(f"    rank corr(lag, dCAGR_pp)@10 bps = {spearman(ov[ov.cost==10].lag, ov[ov.cost==10].dCAGR_pp):+.3f}")

    print("\n[G] RULE 8 WALK-FORWARD: menu = {control} + 28 (X, k) arms, chosen on 2008-2016 @10 bps")
    wf = []
    for (p, n), s in g[g.cost == 10].groupby(["panel", "n"]):
        ctlrow = s[s.arm == "CONTROL"].iloc[0]
        cand = s.copy()
        # (a) chooser = the census ruler on IS (best IS ratio among priceable arms; else control)
        isr = cand.copy()
        isr["IS_ratio"] = np.where(
            (isr.IS_CAGR - ctlrow.IS_CAGR) * 100 < -FREE_EPS,
            (abs(ctlrow.IS_MaxDD) - abs(isr.IS_MaxDD)) * 100 /
            np.maximum(-((isr.IS_CAGR - ctlrow.IS_CAGR) * 100), 1e-9), np.nan)
        pri = isr[isr.arm != "CONTROL"].dropna(subset=["IS_ratio"])
        a_pick = pri.loc[pri.IS_ratio.idxmax()] if len(pri) and pri.IS_ratio.max() > 0 else ctlrow
        # (b) chooser = IS Sharpe over the whole menu, control included
        b_pick = cand.loc[cand.IS_Sharpe.idxmax()]
        best_oos = cand.loc[cand.OOS_Sharpe.idxmax()]
        for tag, pick in (("ruler", a_pick), ("IS_Sharpe", b_pick)):
            wf.append(dict(panel=p, n=n, chooser=tag, pick=pick.arm,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           vs_control=pick.OOS_Sharpe - ctlrow.OOS_Sharpe,
                           regret=pick.OOS_Sharpe - best_oos.OOS_Sharpe,
                           best_oos_arm=best_oos.arm, best_oos_S=best_oos.OOS_Sharpe,
                           control_OOS_S=ctlrow.OOS_Sharpe))
    wfd = pd.DataFrame(wf)
    print(wfd.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for tag, s in wfd.groupby("chooser"):
        print(f"    {tag}: beats do-nothing on {int((s.vs_control > 0).sum())}/{len(s)} books "
              f"(mean {s.vs_control.mean():+.3f}), mean regret {s.regret.mean():+.3f}, "
              f"picks the control in {int((s['pick'] == 'CONTROL').sum())}/{len(s)}")
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    print("\n[H] OOS-ONLY sign check: is the exchange rate negative out of sample too? (10 bps)")
    for k in LAGS:
        s = g[(g.cost == 10) & (g.lag == k)]
        rr = []
        for (p, n), ss in s.groupby(["panel", "n"]):
            c0 = g[(g.cost == 10) & (g.panel == p) & (g.n == n) & (g.arm == "CONTROL")].iloc[0]
            dc = (ss.OOS_CAGR - c0.OOS_CAGR) * 100
            dd = (abs(c0.OOS_MaxDD) - ss.OOS_MaxDD.abs()) * 100
            rr += [ratio_of(a, b) for a, b in zip(dc, dd)]
        rr = pd.Series(rr).dropna()
        print(f"      k={k:>2}: OOS median ratio {fmt(rr.median()):>8}  positive {int((rr>0).sum())}/{len(rr)}")

    print("\n[VERDICT INPUTS]")
    s10 = ov[ov.cost == 10]
    med0 = s10[s10.lag == 0].ratio.dropna().median()
    bestk = max(LAGS, key=lambda k: s10[s10.lag == k].ratio.dropna().median()
                if len(s10[s10.lag == k].ratio.dropna()) else -9e9)
    medb = s10[s10.lag == bestk].ratio.dropna().median()
    print(f"    median ratio @10 bps: k=0 {fmt(med0)} (idea 351 published -1.582), best k={bestk} {fmt(medb)}")
    print(f"    any lag with a POSITIVE pooled median ratio: "
          f"{any(s10[s10.lag==k].ratio.dropna().median() > 0 for k in LAGS)}")
    print(f"    median dDD_pp @10 bps by lag: "
          f"{ {k: round(float(s10[s10.lag==k].dDD_pp.median()), 3) for k in LAGS} }")
    print(f"    4b @10 bps: {int(s10.pass4b.sum())}/{len(s10)}; 4a: {int(s10.pass4a.sum())}/{len(s10)}")


if __name__ == "__main__":
    main()
