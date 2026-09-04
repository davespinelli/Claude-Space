#!/usr/bin/env python3
"""QUEUE idea 8 — lookback-blend (lane C, 2026-09-04).

Question
--------
RULES v1 and the standing 4b KEEP-candidate (idea 2: top-20 eligible equal weight at 75%
gross, composite WITHOUT /sqrt(vol20)) both rank names by the SAME three-horizon blend:
mean pct-rank of (12-1 momentum, 6m return, 3m return).  Nobody has asked which horizon
the ranking edge actually comes from, or whether the blend beats its own components in
BOTH halves.  Idea 25 already found the traded v1 score has IC ~ 0 once /sqrt(vol20) is
applied, and idea 55 found the 200d gate — not the ranking — carries the book.  So the
live question is sharper than "which lookback wins": does the ranking horizon matter at
all, once the gate is held fixed?

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json (56 names) primary; universe_broad.json (136) as the
           robustness pass.  Both are current constituents -> survivorship, see below.
Book     : idea 2's KEEP construction held FIXED except for the ranking signal —
           eligible = (px > 200d MA) & (vol20 < 0.60), top-n equal weight at GROSS/n,
           75% gross, weekly rebalance, weights at close t applied t+1, 10 bps turnover.
Signals  : S in {12-1, 6-1, 3-1, blend-v1, blend-skip}
             12-1      px.shift(21)/px.shift(252) - 1        (classic skip-month)
             6-1       px.shift(21)/px.shift(126) - 1
             3-1       px.shift(21)/px.shift(63)  - 1
             blend-v1  mean pct-rank(12-1, 6m no-skip, 3m no-skip)  <- the incumbent
             blend-skip mean pct-rank(12-1, 6-1, 3-1)               <- skip-consistent
Params   : exactly 2 tuned — S and n in {5, 10, 20, 30}.  All 20 points reported.
Controls : (a) EW-all-eligible at the same gross (no ranking at all) — if the ranked
           arms do not beat it, the horizon question is moot; (b) REVERSED blend-v1
           (bottom-n) as a sign check; (c) 1-month reversal (px/px.shift(21)-1).
Rule 8   : parameters chosen on 2009-2016 only, evaluated untouched on 2017-2026, with
           two selection rules fixed BEFORE any OOS number is read (plain IS Sharpe;
           IS Sharpe subject to the IS 4b bars).
Both KEEP paths are evaluated at every grid point (4a vs the live book, 4b vs SPY).

SURVIVORSHIP: current constituents only, so absolute CAGRs are optimistic and a 20-name
book holds over a third of the 56-name list.  Signal-vs-signal comparisons hold names,
days, gate and gross fixed, so they are far less exposed than the level of any one arm.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST = 10
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
NS = [5, 10, 20, 30]
SIGS = ["12-1", "6-1", "3-1", "blend-v1", "blend-skip"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DATE = "2026-09-04"
SCRIPT = "research/backtests/2026-09-04_lookback-blend_C.py"


# ---------------------------------------------------------------- signals
def _pr(x):
    return x.rank(axis=1, pct=True)


def signal(px, s):
    m12 = px.shift(21) / px.shift(252) - 1
    if s == "12-1":
        return m12
    if s == "6-1":
        return px.shift(21) / px.shift(126) - 1
    if s == "3-1":
        return px.shift(21) / px.shift(63) - 1
    if s == "rev-1m":
        return -(px / px.shift(21) - 1)
    if s == "blend-v1":                      # the incumbent: 6m/3m have no skip month
        return (_pr(m12) + _pr(px / px.shift(126) - 1) + _pr(px / px.shift(63) - 1)) / 3
    if s == "blend-skip":
        return (_pr(m12) + _pr(px.shift(21) / px.shift(126) - 1)
                + _pr(px.shift(21) / px.shift(63) - 1)) / 3
    raise ValueError(s)


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def eligible(px):
    """RULES v1's eligibility gate, held fixed across every arm."""
    return (px > px.rolling(200).mean()) & (vol20(px) < MAX_VOL)


def weights_fn(s, n, reverse=False):
    def f(px):
        sc = signal(px, s).where(eligible(px))
        rank = sc.rank(axis=1, ascending=reverse)
        return (rank <= n).astype(float) * (GROSS / n)
    return f


def ew_eligible(px):
    e = eligible(px).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, _, dd = m(r); h1, h2 = halves(r)
    sc, _, sdd = m(spy); s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m(r); h1, h2 = halves(r)
    _, _, bdd = m(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def run(px, fn, start, cost=COST):
    res = backtest(px, fn(px), cost_bps=cost, freq=FREQ)
    r = res["returns"].loc[start:]
    return r, res["turnover"].loc[start:].sum() / (len(r) / 252)


def verdict(r, base, spy, ss_o):
    oos = m(r.loc[OOS_START:])[1]
    a, b = fail4a(r, base), fail4b(r, spy, oos, ss_o)
    v = ("KEEP 4a" if not a else "KILL 4a (" + ",".join(a) + ")") + " / " + \
        ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")
    return oos, v


# ---------------------------------------------------------------- IC diagnostic
def weekly_ic(px, s, mask, start):
    """Spearman IC of the signal (within eligible names) vs the NEXT week's return."""
    sc = signal(px, s).where(mask)
    fwd = px.shift(-5) / px - 1                        # forward 5 trading days
    idx = px.loc[start:].index[::5]
    ics = []
    for d in idx:
        a, b = sc.loc[d], fwd.loc[d]
        ok = a.notna() & b.notna()
        if ok.sum() >= 8:
            ics.append((d, a[ok].rank().corr(b[ok].rank())))
    ser = pd.Series(dict(ics)).dropna()
    return ser


def ic_line(ser):
    t = ser.mean() / ser.std() * np.sqrt(len(ser)) if len(ser) > 2 else np.nan
    return ser.mean(), t, len(ser)


# ---------------------------------------------------------------- one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    ss_o = m(spy.loc[OOS_START:])[1]

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED (idea 38) — results not comparable. Aborting.")

    print(f"\n{'=' * 126}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    bc, bs, bdd = m(base); b1, b2 = halves(base)
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}  |  "
          f"RULES v1 {bc:.1%}/{bs:.3f}/{bdd:.1%} halves {b1:.3f}/{b2:.3f}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}   |   4a bars: H1>{b1:.3f} H2>{b2:.3f} MaxDD>={bdd:.1%}")
    print("=" * 126)

    print(f"\n{'signal':<11}{'n':<4}{'CAGR':>7}{'Sharpe':>8}{'MaxDD':>8}   {'H1':>5}/{'H2':>5}"
          f"{'OOS':>7}{'turn':>7}   verdict")
    print("-" * 126)
    grid, rows = {}, []
    for s in SIGS:
        for n in NS:
            r, t = run(px, weights_fn(s, n), start)
            grid[(s, n)] = (r, t)
            oos, v = verdict(r, base, spy, ss_o)
            c, sh, dd = m(r); h1, h2 = halves(r)
            print(f"{s:<11}{n:<4}{c:7.1%}{sh:8.3f}{dd:8.1%}   {h1:5.3f}/{h2:5.3f}"
                  f"{oos:7.3f}{t:7.1f}x   {v}")
            rows.append((f"8 {tag} {s} n={n}", c, sh, dd, h1, h2, oos, t, v))
        print("-" * 126)

    # ---- controls
    print("\nControls (same gate, same 75% gross, weekly, 10 bps):")
    ctl = {}
    r, t = run(px, ew_eligible, start)
    ctl["EW-all-eligible"] = (r, t)
    for s in ("blend-v1", "12-1"):
        for n in (5, 20):
            r2, t2 = run(px, weights_fn(s, n, reverse=True), start)
            ctl[f"REVERSED {s} bottom-{n}"] = (r2, t2)
    for n in (5, 20):
        r3, t3 = run(px, weights_fn("rev-1m", n), start)
        ctl[f"1m-reversal n={n}"] = (r3, t3)
    for lbl, (r, t) in ctl.items():
        c, sh, dd = m(r); h1, h2 = halves(r)
        oos, v = verdict(r, base, spy, ss_o)
        print(f"  {lbl:<28} {c:6.1%} / {sh:.3f} / {dd:6.1%}  halves {h1:.3f}/{h2:.3f}  "
              f"OOS {oos:.3f}  turn {t:4.1f}x   {v}")
        rows.append((f"8 {tag} CONTROL {lbl}", c, sh, dd, h1, h2, oos, t, v))

    # ---- does any ranked arm beat the unranked control?  paired daily t-test.
    print("\nPaired test vs the EW-all-eligible control (arm minus control, daily, same days):")
    ew = ctl["EW-all-eligible"][0]
    for s in SIGS:
        line = f"  {s:<11}"
        for n in NS:
            d = (grid[(s, n)][0] - ew).dropna()
            t = d.mean() / d.std() * np.sqrt(len(d))
            line += f"  n={n}: {d.mean() * 252:+5.2%}/yr t{t:+5.2f}"
        print(line)

    # ---- does any component beat the incumbent blend?  paired daily t-test at matched n.
    print("\nPaired test vs the incumbent blend-v1 at matched n (arm minus blend-v1):")
    for s in SIGS:
        if s == "blend-v1":
            continue
        line = f"  {s:<11}"
        for n in NS:
            d = (grid[(s, n)][0] - grid[("blend-v1", n)][0]).dropna()
            t = d.mean() / d.std() * np.sqrt(len(d))
            line += f"  n={n}: {d.mean() * 252:+5.2%}/yr t{t:+5.2f}"
        print(line)

    # ---- raw signal quality, before any portfolio construction
    print("\nWeekly rank IC vs next-week return, within eligible names (mean, t, obs):")
    mask = eligible(px)
    for s in SIGS + ["rev-1m"]:
        ser = weekly_ic(px, s, mask, start)
        a, t, k = ic_line(ser)
        h = len(ser) // 2
        a1, t1, _ = ic_line(ser.iloc[:h]); a2, t2, _ = ic_line(ser.iloc[h:])
        o = ser.loc[OOS_START:]
        ao, to, _ = ic_line(o)
        print(f"  {s:<11} full {a:+.4f} (t{t:+5.2f}, {k})   H1 {a1:+.4f} (t{t1:+5.2f})   "
              f"H2 {a2:+.4f} (t{t2:+5.2f})   OOS {ao:+.4f} (t{to:+5.2f})")

    # ---- how different are the books at all?  overlap of held names at n=20.
    print("\nAverage name overlap with blend-v1 at n=20 (fraction of the 20 slots shared):")
    wb = weights_fn("blend-v1", 20)(px).loc[start:] > 0
    for s in SIGS:
        if s == "blend-v1":
            continue
        ws = weights_fn(s, 20)(px).loc[start:] > 0
        both = (wb & ws).sum(axis=1)
        anyw = wb.sum(axis=1).clip(lower=1)
        print(f"  {s:<11} {(both / anyw).mean():.1%}")

    return dict(grid=grid, rows=rows, spy=spy, base=base, start=start, ss_o=ss_o, ctl=ctl)


def walk_forward(res, tag):
    """PROTOCOL rule 8: choose on 2009-2016, evaluate untouched on 2017-2026."""
    grid, spy, base = res["grid"], res["spy"], res["base"]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc_i, ss_i, sdd_i = m(spy_is)
    sc_o, ss_o, sdd_o = m(spy_oos)
    print(f"\nWalk-forward ({tag}): IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"  IS 4b bars: Sharpe>{ss_i:.3f}  MaxDD>={0.60 * sdd_i:.1%}  CAGR>={0.70 * sc_i:.1%}")
    cand = []
    for key, (r, _) in grid.items():
        c, sh, dd = m(r.loc[:IS_END])
        cand.append(dict(key=key, sh=sh, cagr=c, dd=dd))
    print("  IS top 6 by Sharpe:")
    for c in sorted(cand, key=lambda x: -x["sh"])[:6]:
        print(f"    {c['key'][0]:<11} n={c['key'][1]:<3} Sharpe {c['sh']:6.3f}  "
              f"CAGR {c['cagr']:6.1%}  MaxDD {c['dd']:6.1%}")
    picks = {"plain-Sharpe": max(cand, key=lambda x: x["sh"])["key"]}
    ok = [c for c in cand if c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i and c["cagr"] >= 0.70 * sc_i]
    picks["4b-aware"] = max(ok, key=lambda x: x["sh"])["key"] if ok else None
    bo = m(base.loc[OOS_START:])
    print(f"  OOS SPY {sc_o:.1%}/{ss_o:.3f}/{sdd_o:.1%}  |  "
          f"RULES v1 {bo[0]:.1%}/{bo[1]:.3f}/{bo[2]:.1%}")
    print(f"  OOS 4b bars: Sharpe>{ss_o:.3f}  MaxDD>={0.60 * sdd_o:.1%}  CAGR>={0.70 * sc_o:.1%}")
    out = []
    for rule, key in picks.items():
        if key is None:
            print(f"  OOS pick[{rule}]: NOTHING — no in-sample point met the 4b bars")
            out.append((f"8 {tag} walk-forward {rule}: picks NOTHING", None))
            continue
        c, sh, dd = m(grid[key][0].loc[OOS_START:])
        flag = "beats SPY OOS" if sh > ss_o else "loses to SPY OOS"
        p4b = "clears OOS 4b" if (sh > ss_o and dd >= 0.60 * sdd_o and c >= 0.70 * sc_o) \
            else "misses OOS 4b"
        print(f"  OOS pick[{rule}] = {key[0]} n={key[1]}: {c:.1%}/{sh:.3f}/{dd:.1%}  "
              f"({flag}; {p4b})")
        out.append((f"8 {tag} walk-forward {rule}: {key[0]} n={key[1]} OOS", (c, sh, dd, f"{flag}; {p4b}")))

    # is the IS ranking of horizons informative about the OOS ranking?
    is_r = pd.Series({k: m(v[0].loc[:IS_END])[1] for k, v in grid.items()})
    oos_r = pd.Series({k: m(v[0].loc[OOS_START:])[1] for k, v in grid.items()})
    print(f"  Spearman(IS Sharpe, OOS Sharpe) across the {len(is_r)} grid points: "
          f"{is_r.rank().corr(oos_r.rank()):+.3f}")
    print("  Best OOS point (for reference only, not selectable): "
          f"{oos_r.idxmax()[0]} n={oos_r.idxmax()[1]} Sharpe {oos_r.max():.3f}")
    return out


# ---------------------------------------------------------------- main
def main():
    print("=" * 126)
    print(f"Idea 8 lookback-blend (lane C) | {SCRIPT}")
    print("Grid: signal in {12-1, 6-1, 3-1, blend-v1, blend-skip} x n in {5,10,20,30} "
          "= 20 points, all reported. 2 tuned params.")
    print("Gate (200d & vol20<0.60), 75% gross, weekly, 10 bps, next-day execution held fixed.")
    print("=" * 126)

    px = load_universe()

    # harness sanity: blend-v1 / n=20 must reproduce idea 2's KEEP row (12.7%/1.093/-18.3%)
    start = px.index[260]
    r20, _ = run(px, weights_fn("blend-v1", 20), start)
    c, sh, dd = m(r20); h1, h2 = halves(r20)
    print(f"\nHARNESS CHECK  blend-v1 n=20 -> {c:.1%}/{sh:.3f}/{dd:.1%} halves {h1:.3f}/{h2:.3f}"
          f"   (idea 2's KEEP row: 12.7%/1.093/-18.3%, halves 1.088/1.103)")
    ok = abs(c - 0.127) < 0.002 and abs(sh - 1.093) < 0.01 and abs(dd + 0.183) < 0.005
    print("HARNESS CHECK  " + ("PASS — construction reproduces the candidate"
                               if ok else "*** MISMATCH — read results with care ***"))

    main_res = sweep(px, "universe.json")
    wf_main = walk_forward(main_res, "universe.json")

    print("\nCalendar-year returns at n=20 by signal (universe.json), vs SPY and the control:")
    spy = main_res["spy"]
    yr = {"SPY": spy.groupby(spy.index.year).apply(lambda x: (1 + x).prod() - 1)}
    for s in SIGS:
        r = main_res["grid"][(s, 20)][0]
        yr[s] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    ew = main_res["ctl"]["EW-all-eligible"][0]
    yr["EW-all"] = ew.groupby(ew.index.year).apply(lambda x: (1 + x).prod() - 1)
    print(pd.DataFrame(yr).to_string(float_format=lambda x: f"{x:+.1%}"))

    pxb = load_universe(broad=True)
    broad_res = sweep(pxb, "universe_broad.json")
    wf_broad = walk_forward(broad_res, "universe_broad.json")

    # ---- cross-universe summary: which (signal, n) passes 4b on BOTH lists?
    print("\nCross-universe 4b passes (both universe.json AND universe_broad.json):")
    passes = []
    for s in SIGS:
        for n in NS:
            va = [r for r in main_res["rows"] if r[0] == f"8 universe.json {s} n={n}"][0][8]
            vb = [r for r in broad_res["rows"] if r[0] == f"8 universe_broad.json {s} n={n}"][0][8]
            if "KEEP 4b" in va and "KEEP 4b" in vb:
                passes.append((s, n))
                print(f"  {s} n={n}   [{va}] / [{vb}]")
    if not passes:
        print("  NONE")

    # ---- leaderboard
    bl = m(main_res["base"]); b1, b2 = halves(main_res["base"])
    print("\nLEADERBOARD rows:")
    for res in (main_res, broad_res):                     # each row cites ITS OWN universe's v1
        rb = m(res["base"]); r1, r2 = halves(res["base"])
        for lbl, c, sh, dd, h1, h2, oos, t, v in res["rows"]:
            print(f"| {DATE} | {lbl} | {c:.1%} | {sh:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
                  f"{rb[1]:.2f} ({r1:.2f}/{r2:.2f}) | {v} | {SCRIPT} |")
    for lbl, r in [("8 SPY buy & hold (universe.json sample) - reference", main_res["spy"]),
                   ("8 RULES v1 live (universe.json) - baseline", main_res["base"])]:
        c, sh, dd = m(r); h1, h2 = halves(r)
        print(f"| {DATE} | {lbl} | {c:.1%} | {sh:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
              f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | - | {SCRIPT} |")
    for (lbl, v), res in list(zip(wf_main, [main_res] * len(wf_main))) + \
            list(zip(wf_broad, [broad_res] * len(wf_broad))):
        bl = m(res["base"]); b1, b2 = halves(res["base"])
        if v is None:
            print(f"| {DATE} | {lbl} | - | - | - | - / - | {bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | "
                  f"no IS point met the 4b bars | {SCRIPT} |")
        else:
            c, sh, dd, flag = v
            print(f"| {DATE} | {lbl} | {c:.1%} | {sh:.2f} | {dd:.1%} | - / - | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {flag} | {SCRIPT} |")


if __name__ == "__main__":
    main()
