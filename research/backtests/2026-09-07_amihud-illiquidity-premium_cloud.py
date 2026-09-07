#!/usr/bin/env python3
"""Idea 33: the Amihud (2002) illiquidity premium inside the sub-$2B small-cap panel.

Claim under test: within a small-cap universe, the LEAST liquid names (highest Amihud ratio)
earn a premium; with a momentum filter on top it should be tradeable.  The queue asks the one
question that decides it: does the premium survive 10-25 bps of cost?

Amihud ratio, computed causally, per name per day:
        ILLIQ_t = mean over the last 60 trading days of  |r_d| / (close_d * volume_d)
scaled by 1e6 for readability.  High ILLIQ = illiquid.  Only names with >= 45 valid days in the
window and a positive median dollar volume are scored; everything else is ineligible that day.

Two tuned parameters only:
    1. Q  -- the ILLIQ quintile held, in {Q1 (most liquid) .. Q5 (least liquid)}   (5 values)
    2. M  -- the momentum filter, in {NONE, MA200 (above its 200d mean),
             MOM (top half of the panel on 12-1 month momentum), BOTH}             (4 values)
Grid = 5 x 4 = 20 books, ALL reported, on ONE panel.  Every book is equal-weighted at a constant
75% gross, weekly, next-day execution -- the record's KEEP-4b book form, so the only thing that
varies against the rest of the record is the SELECTION key.

Cost is a reporting RUNG, not a tuned parameter: every book is priced at 10 / 25 / 50 / 100 bps,
and each book's c* (largest whole bps at which all five 4b bars still hold) is reported.  The
100 bps rung is here because a 10 bps assumption on the least-liquid quintile of sub-$2B names is
not a realistic execution cost -- it is the assumption the idea is asking us to stress.

Controls, all on the same tape:
    EWALL     equal-weight every priced name at 75% gross (the do-nothing, no-selection control)
    Q1 vs Q5  the long-only halves of the premium; their difference is reported as a DIAGNOSTIC
              spread only (PROTOCOL rule 2 forbids shorting, so the spread is not a book)
    RULES v2  the live baseline (4a), SPY (4b)

Rule 8 walk-forward: (Q, M) chosen on 2010-2016 by IS Sharpe, the 2017-2026 window read once.
Reported against the OOS in-grid oracle, against EWALL and against SPY.

SURVIVORSHIP, and it bites hardest exactly here: data/prices_small.csv is the CURRENT
constituent list of the sub-$2B screen (see data/SMALL_PANEL_README.md), so every name in it
survived to 2026.  The least-liquid quintile is the part of a small-cap panel where delistings,
bankruptcies and acquisitions concentrate, so Q5's returns below are biased UP by an unknown but
certainly large amount, and any Q5-minus-Q1 premium is biased up too.  A positive result here
would need a delisted-inclusive tape before it could be believed; a NEGATIVE result is the
informative direction, because the bias runs against it.  The 44 tickers with max_1d_move >= 1.0
in data/small_meta.csv are dropped first (483 -> 439).

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights   # noqa
from engine import backtest, metrics                                # noqa

SLUG = "2026-09-07_amihud-illiquidity-premium_cloud"
OUT = ROOT / "research" / "backtests"
GROSS, FREQ = 0.75, "W"
WIN, MINOBS = 60, 45
QS = [1, 2, 3, 4, 5]                       # 1 = most liquid, 5 = least liquid
MFILTS = ["NONE", "MA200", "MOM", "BOTH"]
RUNGS = [10, 25, 50, 100]
IS_END, OOS_START = "2016-12-31", "2017-01-01"


def load_panel():
    px = load_universe(small=True)
    vol = load_volume(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    px = px[keep]
    vol = vol[[c for c in vol.columns if c in keep]].reindex(px.index)
    print(f"    dropped {len(bad)} tickers with max_1d_move >= 1.0; panel = {px.shape[1]-1} names + SPY")
    return px, vol


def amihud(px, vol):
    """Causal 60-day Amihud illiquidity, x1e6.  NaN where coverage is thin or DV is zero."""
    names = [c for c in px.columns if c != "SPY"]
    p, v = px[names], vol[names]
    r = p.pct_change()
    dv = (p * v).replace(0, np.nan)
    ratio = (r.abs() / dv) * 1e6
    ill = ratio.rolling(WIN, min_periods=MINOBS).mean()
    ok = dv.rolling(WIN, min_periods=MINOBS).median() > 0
    return ill.where(ok)


def build(px, ill, q, mfilt):
    """Equal weight, 75% gross, over the names in ILLIQ quintile q that pass the momentum filter."""
    names = [c for c in px.columns if c != "SPY"]
    p = px[names]
    elig = ill.notna() & p.notna()
    if mfilt in ("MA200", "BOTH"):
        elig &= p > p.rolling(200).mean()
    if mfilt in ("MOM", "BOTH"):
        mom = p.shift(21) / p.shift(252) - 1
        elig &= mom.rank(axis=1, pct=True) > 0.5
    # quintile is cut on the FULL scored cross-section that day, then intersected with the filter,
    # so Q means the same thing at every filter setting.
    pct = ill.rank(axis=1, pct=True)                      # low pct = most liquid
    lo, hi = (q - 1) / 5.0, q / 5.0
    inq = (pct > lo) & (pct <= hi) if q > 1 else (pct <= hi)
    sel = (inq & elig).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    w = (sel.div(k, axis=0) * GROSS).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0), (sel.sum(axis=1))


def ewall(px):
    names = [c for c in px.columns if c != "SPY"]
    e = px[names].notna().astype(float)
    w = (e.div(e.sum(axis=1).replace(0, np.nan), axis=0) * GROSS).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]), "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    return (h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def cstar(px, w, spy, start, hi=200):
    """Largest whole bps in 0..hi at which all five 4b bars still hold. -1 if none (fails at 0).
    Every 4b bar is monotone in cost, so the passing set is a down-set and a binary search on it
    is exact (and ~25x cheaper than the linear scan on this panel)."""
    ok = lambda c: bars4b(backtest(px, w, cost_bps=c, freq=FREQ)["returns"].loc[start:], spy)[0]
    if not ok(0):
        return -1
    if ok(hi):
        return hi
    lo, up = 0, hi                       # ok(lo) True, ok(up) False
    while up - lo > 1:
        mid = (lo + up) // 2
        if ok(mid): lo = mid
        else: up = mid
    return lo


def main():
    print("=== panel")
    px, vol = load_panel()
    ill = amihud(px, vol)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
    print(f"    SMALL439 {px.index[0].date()} -> {px.index[-1].date()}, scored from {start.date()}")
    print(f"    SPY   CAGR {ms['CAGR']:7.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:8.2%} "
          f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f}")
    print(f"    4b bars: H1>{s1:.3f} H2>{s2:.3f} OOS>{so['Sharpe']:.3f} "
          f"MaxDD>={-0.60*abs(ms['MaxDD']):.2%} CAGR>={0.70*ms['CAGR']:.2%}")

    base = backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base); b1, b2 = hs(base)
    print(f"    RULESv2 CAGR {mb['CAGR']:6.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:8.2%} "
          f"H1/H2 {b1:.3f}/{b2:.3f}")
    ew = ewall(px)
    ewr = {c: backtest(px, ew, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in RUNGS}
    me = metrics(ewr[10])
    print(f"    EWALL   CAGR {me['CAGR']:6.2%} Sharpe {me['Sharpe']:.3f} MaxDD {me['MaxDD']:8.2%} "
          f"| @10 bps (the do-nothing control)")

    # ---- ILLIQ level sanity: what does each quintile actually contain?
    print("\n=== ILLIQ quintile character (median over days of the cross-sectional median, "
          "x1e6; higher = less liquid)")
    pct = ill.rank(axis=1, pct=True)
    for q in QS:
        lo, hi = (q - 1) / 5.0, q / 5.0
        inq = (pct > lo) & (pct <= hi) if q > 1 else (pct <= hi)
        med = ill.where(inq).median(axis=1).median()
        dv = (px[[c for c in px.columns if c != 'SPY']] *
              vol[[c for c in vol.columns if c != 'SPY']]).where(inq).median(axis=1).median()
        print(f"    Q{q}: median ILLIQ {med:12.4f} | median daily dollar volume ${dv:,.0f} | "
              f"mean names/day {inq.sum(axis=1).mean():.1f}")

    # ---- the 20-book grid
    books, recs = {}, []
    print(f"\n=== the 5 x 4 grid @ 10 bps (ALL 20 books reported)")
    print(f"    {'Q':>2} {'filter':>6} | {'names':>6} {'turn/yr':>8} | {'CAGR':>7} {'Sharpe':>7} "
          f"{'MaxDD':>8} | {'H1':>6} {'H2':>6} | {'OOSshr':>7} | 4a 4b  failing bars")
    for q in QS:
        for mf in MFILTS:
            w, nsel = build(px, ill, q, mf)
            books[(q, mf)] = w
            res = backtest(px, w, cost_bps=10, freq=FREQ)
            r = res["returns"].loc[start:]
            t = res["turnover"].loc[start:].sum() / (len(r) / 252)
            m = metrics(r); h1, h2 = hs(r); o = metrics(r.loc[OOS_START:])["Sharpe"]
            p4b, d4b, f4b = bars4b(r, spy); p4a = bars4a(r, base)
            print(f"    Q{q} {mf:>6} | {nsel.loc[start:].mean():6.1f} {t:8.2f} | {m['CAGR']:7.2%} "
                  f"{m['Sharpe']:7.3f} {m['MaxDD']:8.2%} | {h1:6.3f} {h2:6.3f} | {o:7.3f} | "
                  f"{'Y' if p4a else 'n'}  {'Y' if p4b else 'n'}  {','.join(f4b)}")
            recs.append(dict(Q=q, filt=mf, cost=10, names=nsel.loc[start:].mean(), turnover=t,
                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                             OOS_Sharpe=o, pass4a=p4a, pass4b=p4b, fail4b=",".join(f4b),
                             **{f"marg_{k}": v for k, v in d4b.items()}))

    # ---- cost ladder
    print(f"\n=== cost ladder: Sharpe (and 4b) at {RUNGS} bps -- the question the idea asks")
    print(f"    {'Q':>2} {'filter':>6} | " + " | ".join(f"{c:>3} bps" for c in RUNGS) + " |    c*")
    for q in QS:
        for mf in MFILTS:
            w = books[(q, mf)]
            cells = []
            for c in RUNGS:
                r = backtest(px, w, cost_bps=c, freq=FREQ)["returns"].loc[start:]
                m = metrics(r); p4b = bars4b(r, spy)[0]
                cells.append(f"{m['Sharpe']:6.3f}{'Y' if p4b else ' '}")
                recs.append(dict(Q=q, filt=mf, cost=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                 MaxDD=m["MaxDD"], pass4b=p4b))
            cs = cstar(px, w, spy, start)
            print(f"    Q{q} {mf:>6} | " + " | ".join(cells) + f" | {cs:5d}")
    print(f"    {'EWALL':>9} | " + " | ".join(
        f"{metrics(ewr[c])['Sharpe']:6.3f}{'Y' if bars4b(ewr[c], spy)[0] else ' '}"
        for c in RUNGS) + f" | {cstar(px, ew, spy, start):5d}")

    # ---- the premium itself, as a diagnostic
    print(f"\n=== the PREMIUM as a diagnostic (long-only legs; the Q5-Q1 difference is NOT a book "
          f"-- PROTOCOL rule 2 forbids shorting)")
    for mf in MFILTS:
        r5 = backtest(px, books[(5, mf)], cost_bps=10, freq=FREQ)["returns"].loc[start:]
        r1 = backtest(px, books[(1, mf)], cost_bps=10, freq=FREQ)["returns"].loc[start:]
        d = r5 - r1
        m5, m1 = metrics(r5), metrics(r1)
        is_d = d.loc[:IS_END]; oos_d = d.loc[OOS_START:]
        print(f"    {mf:>6}: Q5 CAGR {m5['CAGR']:7.2%} Sharpe {m5['Sharpe']:6.3f} | "
              f"Q1 CAGR {m1['CAGR']:7.2%} Sharpe {m1['Sharpe']:6.3f} | "
              f"spread {252*d.mean():+7.2%}/yr (t {d.mean()/d.std()*np.sqrt(len(d)):+5.2f}) | "
              f"IS {252*is_d.mean():+7.2%} OOS {252*oos_d.mean():+7.2%}")

    # ---- rule 8
    print(f"\n=== rule 8: (Q, M) chosen on <= {IS_END} by IS Sharpe, OOS {OOS_START}- read once")
    full = {k: backtest(px, w, cost_bps=10, freq=FREQ)["returns"].loc[start:] for k, w in books.items()}
    is_sh = {k: metrics(r.loc[:IS_END])["Sharpe"] for k, r in full.items()}
    oos_sh = {k: metrics(r.loc[OOS_START:])["Sharpe"] for k, r in full.items()}
    pick = max(is_sh, key=is_sh.get); oracle = max(oos_sh, key=oos_sh.get)
    ew_oos = metrics(ewr[10].loc[OOS_START:])["Sharpe"]
    spy_oos = so["Sharpe"]
    r = full[pick]; mo = metrics(r.loc[OOS_START:])
    print(f"    IS pick      : Q{pick[0]} {pick[1]}  (IS Sharpe {is_sh[pick]:.3f})")
    print(f"    OOS of pick  : CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:.3f} MaxDD {mo['MaxDD']:8.2%}")
    print(f"    OOS oracle   : Q{oracle[0]} {oracle[1]} Sharpe {oos_sh[oracle]:.3f}  "
          f"-> regret {oos_sh[pick]-oos_sh[oracle]:+.4f}")
    print(f"    vs EWALL OOS {ew_oos:.3f} -> {oos_sh[pick]-ew_oos:+.4f} | "
          f"vs SPY OOS {spy_oos:.3f} -> {oos_sh[pick]-spy_oos:+.4f} | "
          f"vs RULESv2 OOS {metrics(base.loc[OOS_START:])['Sharpe']:.3f} -> "
          f"{oos_sh[pick]-metrics(base.loc[OOS_START:])['Sharpe']:+.4f}")
    print(f"    IS-Sharpe ranking of the 5 quintiles at M=NONE: " +
          "  ".join(f"Q{q} {is_sh[(q,'NONE')]:.3f}" for q in QS))
    print(f"    OOS ranking   of the 5 quintiles at M=NONE: " +
          "  ".join(f"Q{q} {oos_sh[(q,'NONE')]:.3f}" for q in QS))
    rk = lambda xs: pd.Series(xs).rank()          # scipy is not installed in the sandbox;
    sp = rk([is_sh[(q, "NONE")] for q in QS]).corr(rk([oos_sh[(q, "NONE")] for q in QS]))
    print(f"    is the IS quintile ORDERING preserved OOS? Spearman (rank-Pearson) {sp:+.3f}")

    # ---------------------------------------------------------------- diagnostic A: CAPACITY
    print(f"\n=== DIAGNOSTIC A: capacity. What fraction of a day's volume is one position?")
    names = [c for c in px.columns if c != "SPY"]
    dvol = (px[names] * vol[names])
    for q in (1, 3, 5):
        lo, hi = (q - 1) / 5.0, q / 5.0
        inq = (pct > lo) & (pct <= hi) if q > 1 else (pct <= hi)
        med_dv = dvol.where(inq).median(axis=1).median()
        k = (inq & ill.notna()).sum(axis=1).loc[start:].mean()
        print(f"    Q{q}: {k:5.1f} names, {GROSS/k:6.2%} of NAV each, median name ${med_dv:12,.0f}/day"
              + "".join(f" | ${aum/1e6:4.0f}M AUM -> {GROSS/k*aum/med_dv:7.1%} of a day"
                        for aum in (1e6, 1e7, 1e8)))
    print("    (a position needing >5-10% of a day's volume cannot be built or exited at 10 bps;")
    print("     PROTOCOL's 10 bps rung is an assumption about liquidity that Q5 does not meet)")

    # ---------------------------------------------------------------- diagnostic B: SURVIVORSHIP
    print(f"\n=== DIAGNOSTIC B: survivorship probe. Q5 restricted to names priced from day one of")
    print(f"    the panel (first_date <= 2010-01-05), i.e. no later entrants, vs Q5 as built.")
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv", parse_dates=["first_date"])
    old = set(meta.loc[meta.first_date <= "2010-01-05", "ticker"])
    print(f"    {len(old & set(names))} of {len(names)} names have full history.")
    for mf in ("NONE", "MOM"):
        w = books[(5, mf)].copy()
        drop = [c for c in w.columns if c != "SPY" and c not in old]
        w2 = w.copy(); w2[drop] = 0.0
        s = w2.sum(axis=1).replace(0, np.nan)
        w2 = w2.div(s, axis=0).fillna(0.0) * GROSS       # re-spread over the survivors-from-2010
        r2 = backtest(px, w2, cost_bps=10, freq=FREQ)["returns"].loc[start:]
        r1 = full[(5, mf)]
        m1, m2 = metrics(r1), metrics(r2)
        print(f"    Q5 {mf:>4}: as built CAGR {m1['CAGR']:7.2%} Sharpe {m1['Sharpe']:6.3f} | "
              f"full-history only CAGR {m2['CAGR']:7.2%} Sharpe {m2['Sharpe']:6.3f} "
              f"(d {m2['Sharpe']-m1['Sharpe']:+.3f})  [this removes LATE ENTRANTS only; it cannot "
              f"remove the panel's real bias, which is that every name survived TO 2026]")

    # ---------------------------------------------------------------- diagnostic C: the DD bar
    print(f"\n=== DIAGNOSTIC C: Q5's only failing 4b bar is DRAWDOWN. Idea 351 established the")
    print(f"    constant-gross dial as the record's NUMERAIRE for buying drawdown, so walk it.")
    print(f"    This is a LADDER, not a third tuned parameter: all points reported, and a pass")
    print(f"    here is a dial placement, not an edge (idea 311/351).")
    print(f"    {'gross':>6} {'filter':>6} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} | {'H1':>6} "
          f"{'H2':>6} {'OOS':>6} | 4b  failing bars")
    for mf in ("NONE", "MOM"):
        for g in (0.75, 0.60, 0.50, 0.45, 0.40):
            w = books[(5, mf)] * (g / GROSS)
            r = backtest(px, w, cost_bps=10, freq=FREQ)["returns"].loc[start:]
            m = metrics(r); h1, h2 = hs(r); o = metrics(r.loc[OOS_START:])["Sharpe"]
            p4b, d4b, f4b = bars4b(r, spy)
            print(f"    {g:6.2f} {mf:>6} | {m['CAGR']:7.2%} {m['Sharpe']:7.3f} {m['MaxDD']:8.2%} | "
                  f"{h1:6.3f} {h2:6.3f} {o:6.3f} | {'Y' if p4b else 'n'}  {','.join(f4b)}")
            recs.append(dict(Q=5, filt=f"{mf}_g{g:.2f}", cost=10, CAGR=m["CAGR"],
                             Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=o,
                             pass4b=p4b, fail4b=",".join(f4b)))

    df = pd.DataFrame(recs)
    df.to_csv(OUT / f"{SLUG}_grid.csv", index=False)
    g10 = df[(df.cost == 10) & df.filt.isin(MFILTS) & df.fail4b.notna()]  # the 20-book grid only
    print(f"\n=== KEEP paths: 4b {int(g10.pass4b.sum())}/20 @10 bps, 4a {int(g10.pass4a.sum())}/20; "
          f"4b at 25/50/100 bps: " + " / ".join(
              f"{int(df[(df.cost==c) & df.filt.isin(MFILTS)].pass4b.sum())}/20" for c in RUNGS[1:]))
    fails = pd.Series([b for s in g10.fail4b for b in (s.split(",") if s else [])]).value_counts()
    print(f"    failing-bar census @10 bps: " + ", ".join(f"{k}:{v}" for k, v in fails.items()))
    print(f"    wrote {SLUG}_grid.csv ({len(df)} rows)")


if __name__ == "__main__":
    main()
