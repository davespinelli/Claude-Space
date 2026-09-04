#!/usr/bin/env python3
"""QUEUE idea 67 — core-sleeve-walk-forward-repair (lane B, 2026-09-04).

Question
--------
Idea 63 produced a 4b KEEP-candidate — replace a fraction b of the book with a
passive core at matched 75% gross — and chose b = 0.25 with the *sample-wide*
cross-universe 4b test.  Its rule-8 walk-forward disagreed: both of its IS
selection rules picked `top20 / b = 0.50`, which clears every OOS 4b bar on
universe.json but FAILS the OOS drawdown cap on the broad list by 1.8pp
(-22.0% vs a -20.2% cap).

The queue's hypothesis: idea 63's "4b-aware" IS rule (rule B) constrains IS
drawdown only *relative to SPY's own IS drawdown*, and 2009-2016 contains no
severe bear (SPY IS MaxDD ~ -19%, vs -33.7% OOS).  A relative cap calibrated on
a benign window may be too loose to keep the selection out of the high-beta
arms.  If a defensible, pre-registrable IS rule that caps drawdown at an
absolute mandate level picks b = 0.25, the walk-forward's disagreement with the
candidate is an artefact of a benign IS window.  If NO such rule picks b = 0.25,
the walk-forward genuinely disagrees and the candidate should be downgraded.

Method
------
Arms are idea 63's exactly, nothing re-tuned here: books `v1`, `top20`,
`ew-all`, `ew-band3` x b in {0, 0.25, 0.50} x core in {QQQ, SPY}, weekly, t+1,
10 bps, both universes.  The QQQ-core set is the primary candidate set (it is
the one idea 63's walk-forward searched); the SPY-core set is the control, since
idea 63 showed the H2 repair is plain beta rather than mega caps.

1. HARNESS CHECK against idea 63's published rows.
2. IS/OOS MAP: for every arm, IS (2009-2016) CAGR/Sharpe/MaxDD/Calmar and OOS
   (2017-2026) CAGR/Sharpe/MaxDD, the OOS 4b verdict, and the full-sample 4b
   verdict.  Plus the Spearman rank correlation across arms between each IS
   statistic and each OOS statistic — i.e. is the IS window informative at all?
3. SELECTION-RULE GRID (the two tuned parameters, all points reported):
     param 1 = IS objective in {IS Sharpe, IS Calmar}
     param 2 = IS drawdown cap in {none, SPY-relative (idea 63's rule B),
               -20%, -15%, -12%, -10%}
   All grid points additionally carry idea 63's IS CAGR floor (>= 70% of SPY's
   IS CAGR); idea 63's unconstrained rule A is reported as a labelled extra row.
   For each point: which arm is selected on IS only, and does that selection
   clear the OOS 4b bars.
4. SPLIT STABILITY: re-run the selection with IS ending 2013..2018 and report
   the picked b at each split.  A candidate the walk-forward never picks at any
   split is genuinely rejected, not rejected by one arbitrary cut date.
5. BOTH KEEP PATHS for the b = 0.25 candidate: 4a (vs the live RULES v1 book in
   both halves, MaxDD no worse) and 4b (vs SPY, halves + OOS + DD + CAGR).
6. Rule-8 headline: OOS CAGR/Sharpe/MaxDD for the selected arm vs the RULES v1
   baseline OOS and SPY OOS.

SURVIVORSHIP: both universes are current constituents.  This run does not create
new exposure to that bias beyond idea 63's, but every absolute return level here
is an upper bound.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
BAND = 0.03
PROTO_COST = 10
BLENDS = [0.0, 0.25, 0.50]
CORES = ["QQQ", "SPY"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SPLIT_YEARS = [2013, 2014, 2015, 2016, 2017, 2018]
DD_CAPS = [None, "spy-rel", -0.20, -0.15, -0.12, -0.10]
OBJECTIVES = ["IS-Sharpe", "IS-Calmar"]
SCRIPT = "research/backtests/2026-09-04_core-sleeve-walk-forward-repair_B.py"


# ---------------------------------------------------------------- construction (idea 63, verbatim)
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, gate):
    ma = px.rolling(200).mean()
    if gate == "200d":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + BAND), 1.0)
        raw = raw.mask(px < ma * (1 - BAND), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    raise ValueError(gate)


def eligible(px, gate):
    return (vol20(px) < MAX_VOL) & trend(px, gate)


def w_top20(px):
    rank = composite(px).where(eligible(px, "200d")).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def _ewall(px, gate):
    e = eligible(px, gate).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


def w_ewall(px):
    return _ewall(px, "200d")


def w_ewband(px):
    return _ewall(px, "band3")


BOOKS = {"v1": rules_v1_weights, "top20": w_top20, "ew-all": w_ewall, "ew-band3": w_ewband}


def blended(fn, b, core):
    def f(px):
        w = fn(px) * (1.0 - b)
        if b > 0:
            w = w.copy()
            w[core] = w[core] + b * GROSS
        return w
    return f


# ---------------------------------------------------------------- helpers
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def sharpe(r):
    return metrics(r)["Sharpe"]


def calmar(r):
    d = metrics(r)
    return d["CAGR"] / abs(d["MaxDD"]) if d["MaxDD"] else np.nan


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def gross_run(px, fn, start):
    res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def fail4b(r, spy, oos, spy_oos):
    """Full-sample 4b: Sharpe > SPY in both halves and OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY."""
    c, s, dd = r if isinstance(r, tuple) else m(r)
    return None


def bars4b(spy):
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    return dict(h1=sharpe(s1), h2=sharpe(s2), oos=sharpe(spy.loc[OOS_START:]),
                dd=0.60 * sdd, cagr=0.70 * sc)


def test4b(r, bar):
    c, s, dd = m(r)
    r1, r2 = halves(r)
    bad = []
    if sharpe(r1) <= bar["h1"]: bad.append("H1")
    if sharpe(r2) <= bar["h2"]: bad.append("H2")
    if sharpe(r.loc[OOS_START:]) <= bar["oos"]: bad.append("OOS")
    if dd < bar["dd"]: bad.append("DD")
    if c < bar["cagr"]: bad.append("CAGR")
    return bad


def test4a(r, base):
    """4a: Sharpe > live rules in BOTH halves and MaxDD no worse than the live rules."""
    r1, r2 = halves(r)
    b1, b2 = halves(base)
    bad = []
    if sharpe(r1) <= sharpe(b1): bad.append("H1")
    if sharpe(r2) <= sharpe(b2): bad.append("H2")
    if m(r)[2] < m(base)[2]: bad.append("DD")
    return bad


def oos4b(r, spy):
    """OOS-only 4b bars, exactly as idea 63 applied them."""
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    c, s, dd = m(ro)
    sc, ss, sdd = m(so)
    bad = []
    if s <= ss: bad.append("Sharpe")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def spearman(a, b):
    sa = pd.Series(a).rank()
    sb = pd.Series(b).rank()
    return float(sa.corr(sb))


# ---------------------------------------------------------------- selection rules
def select(arms, stats, objective, cap, spy_is, cagr_floor=True):
    """Choose one arm using IS statistics only. Returns key or None."""
    isc_spy, iss_spy, isdd_spy = m(spy_is)
    ok = []
    for k in arms:
        ic, ish, idd, ical = stats[k]
        if cagr_floor and ic < 0.70 * isc_spy:
            continue
        if cap == "spy-rel" and idd < 0.60 * isdd_spy:
            continue
        if isinstance(cap, float) and idd < cap:
            continue
        ok.append(k)
    if not ok:
        return None
    key = (lambda k: stats[k][1]) if objective == "IS-Sharpe" else (lambda k: stats[k][3])
    return max(ok, key=key)


def cap_label(cap):
    if cap is None: return "none"
    if cap == "spy-rel": return "SPY-rel(60%)"
    return f"{cap:.0%} abs"


# ---------------------------------------------------------------- per-universe run
def run(tag, px, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bar = bars4b(spy)
    base_g, base_t = gross_run(px, rules_v1_weights, start)
    base = base_g - base_t * PROTO_COST / 1e4
    b1, b2 = halves(base)

    print(f"\n{'=' * 138}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}, "
          f"weekly, t+1, {PROTO_COST} bps")
    sc, ss, sdd = m(spy)
    print(f"  SPY full {sc:.1%}/{ss:.3f}/{sdd:.1%}   4b bars: H1>{bar['h1']:.3f} H2>{bar['h2']:.3f} "
          f"OOS>{bar['oos']:.3f} MaxDD>={bar['dd']:.1%} CAGR>={bar['cagr']:.1%}")
    print(f"  RULES v1 baseline full {m(base)[0]:.1%}/{m(base)[1]:.3f}/{m(base)[2]:.1%} "
          f"(H1 {sharpe(b1):.2f} / H2 {sharpe(b2):.2f})   <- the 4a bar")
    print(f"  IS  = {start.date()} -> {IS_END}     OOS = {OOS_START} -> {px.index[-1].date()}")
    isc, iss, isdd = m(spy.loc[:IS_END])
    oc, osh, odd = m(spy.loc[OOS_START:])
    print(f"  SPY IS  {isc:.1%}/{iss:.3f}/{isdd:.1%}     SPY OOS {oc:.1%}/{osh:.3f}/{odd:.1%}"
          f"     <- the IS window has {abs(isdd) / abs(odd):.0%} of the OOS drawdown")
    print("=" * 138)

    # ---- build every arm once
    R = {}
    for bk, fn in BOOKS.items():
        for b in BLENDS:
            for core in (CORES if b > 0 else ["-"]):
                g, t = gross_run(px, blended(fn, b, core if core != "-" else "QQQ"), start)
                R[(bk, b, core)] = g - t * PROTO_COST / 1e4

    if tag == "universe_broad.json":
        pub = {("top20", 0.0, "-"): "13.1%/0.958/-20.1%", ("ew-all", 0.0, "-"): "10.7%/1.027/-17.7%",
               ("ew-band3", 0.0, "-"): "11.1%/1.064/-16.8%",
               ("top20", 0.25, "QQQ"): "13.8%/1.016/-19.9%", ("ew-band3", 0.25, "QQQ"): "12.3%/1.086/-18.5%"}
        print("\nHARNESS CHECK vs idea 63's published rows:")
        for k, s in pub.items():
            c, sh, dd = m(R[k])
            print(f"  {k[0]:<9} b={k[1]:.2f} {k[2]:<4} here {c:.1%}/{sh:.3f}/{dd:.1%}   published {s}")

    # ---- 2. IS/OOS map
    print("\nIS / OOS MAP — every arm, IS 2009-2016 and OOS 2017-2026, 10 bps:")
    print(f"  {'book':<10}{'b':>5} {'core':<5}{'IS CAGR':>9}{'IS Sh':>8}{'IS DD':>8}{'IS Cal':>8}"
          f"{'OOS CAGR':>10}{'OOS Sh':>8}{'OOS DD':>8}   {'OOS 4b':<18}{'full 4b':<20}{'4a'}")
    stats, keys = {}, []
    for bk in BOOKS:
        for b in BLENDS:
            for core in (CORES if b > 0 else ["-"]):
                k = (bk, b, core)
                keys.append(k)
                r = R[k]
                ic, ish, idd = m(r.loc[:IS_END])
                ical = calmar(r.loc[:IS_END])
                stats[k] = (ic, ish, idd, ical)
                oc_, osh_, odd_ = m(r.loc[OOS_START:])
                bo, bf, ba = oos4b(r, spy), test4b(r, bar), test4a(r, base)
                print(f"  {bk:<10}{b:5.2f} {core:<5}{ic:9.1%}{ish:8.3f}{idd:8.1%}{ical:8.2f}"
                      f"{oc_:10.1%}{osh_:8.3f}{odd_:8.1%}   "
                      f"{('PASS' if not bo else 'fail ' + ','.join(bo)):<18}"
                      f"{('PASS' if not bf else 'fail ' + ','.join(bf)):<20}"
                      f"{('PASS' if not ba else 'fail ' + ','.join(ba))}")
                c_, s_, d_ = m(r)
                h1_, h2_ = halves(r)
                rows.append(dict(tag=tag, book=bk, b=b, core=core, cagr=c_, sharpe=s_, dd=d_,
                                 h1=sharpe(h1_), h2=sharpe(h2_), oos_c=oc_, oos_s=osh_, oos_d=odd_,
                                 full4b=("KEEP 4b" if not bf else "KILL 4b (" + ",".join(bf) + ")"),
                                 keep4a=not ba,
                                 base_s=m(base)[1], base_h1=sharpe(b1), base_h2=sharpe(b2)))

    # ---- is IS informative about OOS at all?
    print("\n  Is the IS window informative? Spearman rank corr across the "
          f"{len(keys)} arms (IS statistic vs OOS statistic):")
    for isl, isi in (("IS Sharpe", 1), ("IS CAGR", 0), ("IS MaxDD", 2), ("IS Calmar", 3)):
        xs = [stats[k][isi] for k in keys]
        print(f"    {isl:<11}"
              + "".join(f"  vs OOS {lbl}: {spearman(xs, [m(R[k].loc[OOS_START:])[j] for k in keys]):+.2f}"
                        for lbl, j in (("Sharpe", 1), ("CAGR", 0), ("MaxDD", 2))))

    # ---- 3. selection-rule grid
    for cset, label in ((["-", "QQQ"], "QQQ core (idea 63's candidate set)"),
                        (["-", "SPY"], "SPY core (control: plain beta)")):
        arms = [k for k in keys if k[2] in cset]
        print(f"\nSELECTION-RULE GRID — {label}. Chosen on IS only; OOS verdict is the test.")
        print(f"  {'objective':<11}{'IS DD cap':<15}{'selected arm':<24}"
              f"{'OOS CAGR':>10}{'OOS Sh':>8}{'OOS DD':>8}   OOS 4b        picks b=0.25?")
        # idea 63's rule A, unconstrained, as a labelled reference
        for obj in OBJECTIVES:
            for cap in DD_CAPS:
                for floor in ([True] if not (cap is None and obj == "IS-Sharpe") else [False, True]):
                    k = select(arms, stats, obj, cap, spy.loc[:IS_END], cagr_floor=floor)
                    lab = cap_label(cap) + ("" if floor else "  [rule A]")
                    if k is None:
                        print(f"  {obj:<11}{lab:<15}{'-- nothing selected --':<24}")
                        continue
                    r = R[k]
                    oc_, osh_, odd_ = m(r.loc[OOS_START:])
                    bo = oos4b(r, spy)
                    print(f"  {obj:<11}{lab:<15}{f'{k[0]} b={k[1]:.2f} {k[2]}':<24}"
                          f"{oc_:10.1%}{osh_:8.3f}{odd_:8.1%}   "
                          f"{('PASS' if not bo else 'FAIL ' + ','.join(bo)):<14}"
                          f"{'YES' if k[1] == 0.25 else 'no'}")

    # ---- 4. split stability
    print("\nSPLIT STABILITY — 4b-aware IS rule (SPY-relative cap, IS Sharpe objective) at "
          "six IS end-years, QQQ core:")
    print(f"  {'IS end':<9}{'selected arm':<24}{'IS Sh':>8}{'OOS CAGR':>10}{'OOS Sh':>8}"
          f"{'OOS DD':>8}   OOS 4b        b")
    arms_q = [k for k in keys if k[2] in ("-", "QQQ")]
    for y in SPLIT_YEARS:
        e, s0 = f"{y}-12-31", f"{y + 1}-01-01"
        st = {}
        for k in arms_q:
            rr = R[k].loc[:e]
            st[k] = (m(rr)[0], m(rr)[1], m(rr)[2], calmar(rr))
        k = select(arms_q, st, "IS-Sharpe", "spy-rel", spy.loc[:e])
        if k is None:
            print(f"  {y:<9}{'-- nothing selected --':<24}")
            continue
        ro, so = R[k].loc[s0:], spy.loc[s0:]
        oc_, osh_, odd_ = m(ro)
        sc_, ssh_, sdd_ = m(so)
        bad = ([] if osh_ > ssh_ else ["Sharpe"]) + ([] if odd_ >= 0.60 * sdd_ else ["DD"]) \
            + ([] if oc_ >= 0.70 * sc_ else ["CAGR"])
        print(f"  {y:<9}{f'{k[0]} b={k[1]:.2f} {k[2]}':<24}{st[k][1]:8.3f}{oc_:10.1%}{osh_:8.3f}"
              f"{odd_:8.1%}   {('PASS' if not bad else 'FAIL ' + ','.join(bad)):<14}{k[1]:.2f}")

    # ---- 5/6. the candidate arms head to head, both KEEP paths + rule-8 headline
    print("\nCANDIDATE vs WALK-FORWARD PICK — both KEEP paths, full sample and OOS:")
    print(f"  {'arm':<24}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'H1':>7}{'H2':>7}"
          f"{'OOS CAGR':>10}{'OOS Sh':>8}{'OOS DD':>8}   {'4b':<20}4a")
    for k in [("top20", 0.25, "QQQ"), ("top20", 0.50, "QQQ"), ("ew-band3", 0.25, "QQQ"),
              ("ew-band3", 0.25, "SPY"), ("ew-band3", 0.0, "-"), ("top20", 0.0, "-")]:
        r = R[k]
        c_, s_, d_ = m(r)
        h1_, h2_ = halves(r)
        oc_, osh_, odd_ = m(r.loc[OOS_START:])
        bf, ba = test4b(r, bar), test4a(r, base)
        print(f"  {f'{k[0]} b={k[1]:.2f} {k[2]}':<24}{c_:8.1%}{s_:8.3f}{d_:8.1%}"
              f"{sharpe(h1_):7.3f}{sharpe(h2_):7.3f}{oc_:10.1%}{osh_:8.3f}{odd_:8.1%}   "
              f"{('KEEP' if not bf else 'KILL ' + ','.join(bf)):<20}"
              f"{'KEEP' if not ba else 'KILL ' + ','.join(ba)}")
    print(f"  {'RULES v1 baseline':<24}{m(base)[0]:8.1%}{m(base)[1]:8.3f}{m(base)[2]:8.1%}"
          f"{sharpe(b1):7.3f}{sharpe(b2):7.3f}{m(base.loc[OOS_START:])[0]:10.1%}"
          f"{m(base.loc[OOS_START:])[1]:8.3f}{m(base.loc[OOS_START:])[2]:8.1%}")
    print(f"  {'SPY buy & hold':<24}{sc:8.1%}{ss:8.3f}{sdd:8.1%}"
          f"{sharpe(halves(spy)[0]):7.3f}{sharpe(halves(spy)[1]):7.3f}{oc:10.1%}{osh:8.3f}{odd:8.1%}")
    return R, spy, base, bar


def main():
    rows = []
    for tag, kw in (("universe_broad.json", dict(broad=True)), ("universe.json", {})):
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            sys.exit("!! CALENDAR-DAY INDEX DETECTED — aborting (see QUEUE idea 38).")
        run(tag, px, rows)

    df = pd.DataFrame(rows)
    print(f"\n{'=' * 138}\nCROSS-UNIVERSE 4b SUMMARY at {PROTO_COST} bps (both lists must pass)\n"
          + "=" * 138)
    print(f"  {'book':<10}{'b':>5} {'core':<5}{'universe.json':>30}{'universe_broad.json':>30}   both?")
    for bk in BOOKS:
        for b in BLENDS:
            for core in (CORES if b > 0 else ["-"]):
                a = df[(df.tag == "universe.json") & (df.book == bk) & (df.b == b) & (df.core == core)].iloc[0]
                c = df[(df.tag == "universe_broad.json") & (df.book == bk) & (df.b == b) & (df.core == core)].iloc[0]
                both = "YES" if a.full4b == "KEEP 4b" and c.full4b == "KEEP 4b" else "no"
                print(f"  {bk:<10}{b:5.2f} {core:<5}{a.cagr:11.1%}/{a.sharpe:.3f}/{a.dd:7.1%}"
                      f"{c.cagr:11.1%}/{c.sharpe:.3f}/{c.dd:7.1%}   {both}")
    print(f"\nScript: {SCRIPT}")

    # leaderboard rows for the arms this idea is about
    print("\nLEADERBOARD rows:")
    want = [("top20", 0.25, "QQQ"), ("top20", 0.50, "QQQ"), ("ew-band3", 0.25, "QQQ"),
            ("ew-band3", 0.25, "SPY")]
    for tag in ("universe.json", "universe_broad.json"):
        for bk, b, core in want:
            a = df[(df.tag == tag) & (df.book == bk) & (df.b == b) & (df.core == core)].iloc[0]
            short = tag.replace("universe_broad.json", "broad").replace("universe.json", "u.json")
            print(f"| 2026-09-04 | 67 {short} {bk} b={b:.2f} {core} core | {a.cagr:.1%} | "
                  f"{a.sharpe:.2f} | {a.dd:.1%} | {a.h1:.2f} / {a.h2:.2f} | "
                  f"{a.base_s:.2f} ({a.base_h1:.2f}/{a.base_h2:.2f}) | {a.full4b} | {SCRIPT} |")


if __name__ == "__main__":
    main()
