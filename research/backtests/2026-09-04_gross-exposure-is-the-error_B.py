#!/usr/bin/env python3
"""QUEUE idea 66 — gross-exposure-is-the-error (lane B, 2026-09-04).

Question
--------
Idea 63 diagnosed the standing 4b failure (books lose to SPY in the second half on the
broad list) as **75%-gross cash drag**, not mega-cap concentration: the concentration
factor explained R^2 0.011-0.018 of H2 excess, and ANY passive core (SPY, VTI, QQQ)
repaired the bar.  Idea 63 then fixed it by bolting a 25% passive core onto the book.

If the disease is cash drag, the direct cure is to stop holding cash.  So test gross
exposure as the design variable itself:

  (a) The two standing candidate books at gross in {0.75 ... 1.00}, both large-cap lists,
      5-50 bps, with the drawdown consequence printed at EVERY point (MaxDD, Ulcer, the
      five deepest episodes, 2020 and 2022 within-year drawdowns, worst 20-day return).
  (b) Head-to-head against idea 63's control: 75% gross with a 25% SPY core, i.e. the
      same 100% invested but a quarter of it passive.  **If 100% gross does what the 25%
      core does, the sleeve is a detour.**

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names incl. SPY and ETFs);
           robustness pass on universe_broad.json (136 names).  Both are current
           constituents -> SURVIVORSHIP, absolute CAGR/Sharpe optimistic.  The
           gross-vs-gross comparisons that answer the question are far less exposed:
           every arm draws the same names on the same days and differs only in scale.
Books    : pre-chosen from prior ideas, NOT tuned here —
           * `ew-band3`  — idea 57's candidate: equal-weight EVERY eligible name, where
             eligible = vol20 < 0.60 AND the 3% hysteresis band around the 200d MA
             (enter above 1.03*MA, exit below 0.97*MA, sticky between).
           * `top20-200d` — idea 2/55's candidate: top-20 by the composite (mean pct-rank
             of 12-1, 6m, 3m; NO /sqrt(vol20)) among names eligible under the plain 200d
             gate, equal weight gross/20 each, cash if fewer than 20 qualify.
           * `top20-band3` — the same ranked book on the band3 gate, so the gross effect
             can be read independently of which gate the book carries.
Params   : exactly 2 tuned — (1) gross g in {0.75, 0.80, 0.85, 0.90, 0.95, 1.00}, all six
           reported; (2) core fraction b in {0.00, 0.25} for the sleeve control (b=0.25
           is idea 63's pre-chosen value, not searched).  Nothing else is varied.
Costs    : 5, 10, 15, 20, 25, 50 bps.  10 bps is the PROTOCOL cost and the one verdicts
           are read at; the rest is the sensitivity the idea asks for.  Costs are applied
           analytically, returns(c) = gross_returns - turnover * c/1e4, which is exactly
           engine.backtest's arithmetic since `held` and `turnover` do not depend on
           cost_bps.  A harness check below asserts the identity against a real
           cost_bps=10 run.
Execution: weekly rebalance, weights decided at close t applied at close t+1 (engine),
           long-only, NO LEVERAGE — gross never exceeds 1.00, so "100% gross" means fully
           invested, not margined.
Rule 8   : gross chosen on 2009-2016 only under two pre-registered selection rules fixed
           before any OOS number is read; 2017-2026 evaluated untouched.

The mechanical null this run has to defeat: at fixed weights a book at gross g is very
nearly g times the fully-invested book plus (1-g) in cash, so CAGR, MaxDD and turnover
should all scale with g and Sharpe should be almost FLAT.  If Sharpe is flat, then "raise
gross" is a leverage/position-sizing decision, not an edge, and the 4b bars it clears are
cleared by scale alone.  That is tested directly (Sharpe slope in g, and the correlation
of each arm with the g=1.00 arm) rather than assumed.
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
MAX_VOL = 0.60
NPOS = 20
BAND = 0.03
GROSSES = [0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
CORES = [0.00, 0.25]
COSTS = [5, 10, 15, 20, 25, 50]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SCRIPT = "research/backtests/2026-09-04_gross-exposure-is-the-error_B.py"


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2/55's candidate scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, gate):
    ma = px.rolling(200).mean()
    if gate == "200d":
        return px > ma
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + BAND), 1.0)      # cross up through upper band -> in
        raw = raw.mask(px < ma * (1 - BAND), 0.0)      # cross down through lower -> out
        return raw.ffill().fillna(0.0) > 0.5           # sticky between; out before warm-up
    raise ValueError(gate)


def eligible(px, gate):
    return (vol20(px) < MAX_VOL) & trend(px, gate)


def w_ewall(gate, gross, b=0.0):
    """Equal-weight every eligible name at gross*(1-b); gross*b sits in SPY always.

    b is the core fraction OF GROSS, exactly as idea 63 defined it, so (g=0.75, b=0.25)
    reproduces idea 63's candidate and (g=1.00, b=0.25) is that same book fully invested.
    """
    core = gross * b
    def f(px):
        e = eligible(px, gate).astype(float)
        w = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * (gross - core)
        if core > 0:
            w["SPY"] = w["SPY"] + core
        return w
    return f


def w_top(gate, gross, b=0.0):
    core = gross * b
    def f(px):
        rank = composite(px).where(eligible(px, gate)).rank(axis=1, ascending=False)
        w = (rank <= NPOS).astype(float) * ((gross - core) / NPOS)
        if core > 0:
            w["SPY"] = w["SPY"] + core
        return w
    return f


BOOKS = {
    "ew-band3":    lambda g, b: w_ewall("band3", g, b),
    "top20-200d":  lambda g, b: w_top("200d", g, b),
    "top20-band3": lambda g, b: w_top("band3", g, b),
}
ARMS = [(bk, g, b) for bk in BOOKS for g in GROSSES for b in CORES]


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def dd_series(r):
    eq = (1 + r).cumprod()
    return eq / eq.cummax() - 1


def ulcer(r):
    return float(np.sqrt((dd_series(r) ** 2).mean()))


def top5_dd(r):
    """Mean depth of the five deepest *distinct* drawdown episodes."""
    eq = (1 + r).cumprod()
    peak = eq.cummax()
    grp = (peak != peak.shift()).cumsum()
    depths = (eq / peak - 1).groupby(grp).min().sort_values()
    return float(depths.head(5).mean())


def year_dd(r, y):
    s = r[r.index.year == y]
    return float(dd_series(s).min()) if len(s) else np.nan


def worst20(r):
    return float((1 + r).rolling(20).apply(np.prod, raw=True).min() - 1)


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r); h1, h2 = halves(r)
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")     # MaxDD is negative: "no worse than 60% of SPY's"
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


def verdict(r, base, spy, oos_sh, spy_oos_sh):
    a, b = fail4a(r, base), fail4b(r, spy, oos_sh, spy_oos_sh)
    return ("KEEP 4a" if not a else "KILL 4a") + " / " + \
           ("KEEP 4b" if not b else "KILL 4b(" + ",".join(b) + ")")


# ---------------------------------------------------------------- run helpers
def gross_run(px, fn, start):
    res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:], res["weights"].loc[start:]


def at_cost(g, t, bps):
    return g - t * bps / 1e4


def turn_per_yr(t):
    return t.sum() / (len(t) / 252)


def label(bk, g, b):
    return f"{bk} g={g:.2f} core={b:.2f}"


# ---------------------------------------------------------------- one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    _, ss_o, _ = m(spy.loc[OOS_START:])

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED (idea 38) — results not comparable. Aborting.")

    print(f"\n{'=' * 132}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%}  halves {s1:.3f}/{s2:.3f}  OOS Sharpe {ss_o:.3f}   "
          f"Ulcer {ulcer(spy):.3f} top5DD {top5_dd(spy):.1%} "
          f"2020DD {year_dd(spy, 2020):.1%} 2022DD {year_dd(spy, 2022):.1%}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 132)

    G = {}
    for bk, g, b in ARMS:
        G[(bk, g, b)] = gross_run(px, BOOKS[bk](g, b), start)
    b_gross, b_turn, _ = gross_run(px, rules_v1_weights, start)

    # harness check: analytic costs must equal a real cost_bps run
    chk_fn = BOOKS["ew-band3"](0.75, 0.00)
    chk = backtest(px, chk_fn(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
    err = float((chk - at_cost(*G[("ew-band3", 0.75, 0.00)][:2], PROTO_COST)).abs().max())
    print(f"\nHarness check — analytic {PROTO_COST} bps vs engine cost_bps={PROTO_COST}: "
          f"max |diff| {err:.2e} (must be ~0)")
    assert err < 1e-12, "analytic cost identity broken"

    # realised exposure: does gross g actually put g to work?
    print("\nRealised exposure — mean/min invested fraction and cash drag (days below target):")
    print(f"  {'arm':<28}{'mean gross':>11}{'median':>9}{'min':>7}{'days<95% of g':>15}"
          f"{'turnover':>10}")
    for bk in BOOKS:
        for g in GROSSES:
            for b in CORES:
                w = G[(bk, g, b)][2].sum(axis=1)
                print(f"  {label(bk, g, b):<28}{w.mean():11.1%}{w.median():9.1%}{w.min():7.1%}"
                      f"{(w < 0.95 * g).mean():15.1%}{turn_per_yr(G[(bk, g, b)][1]):9.1f}x")

    # ---- main grid: every arm x cost, with the drawdown consequence at every point
    print(f"\n{'book':<12}{'g':>5}{'core':>6}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
          f"{'Ulcer':>7}{'top5DD':>8}{'2020':>7}{'2022':>7}{'w20d':>8}   {'H1':>5}/{'H2':>5}"
          f"{'OOS':>7}   verdict")
    print("-" * 132)
    RET, rows = {}, []
    for bk in BOOKS:
        for g in GROSSES:
            for b in CORES:
                gr, tu, _ = G[(bk, g, b)]
                for c in COSTS:
                    r = at_cost(gr, tu, c)
                    RET[(bk, g, b, c)] = r
                    base = at_cost(b_gross, b_turn, c)
                    cg, sh, dd = m(r); h1, h2 = halves(r)
                    oos = m(r.loc[OOS_START:])[1]
                    v = verdict(r, base, spy, oos, ss_o)
                    mark = " <-" if c == PROTO_COST else ""
                    print(f"{bk:<12}{g:5.2f}{b:6.2f}{c:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}"
                          f"{ulcer(r):7.3f}{top5_dd(r):8.1%}{year_dd(r, 2020):7.1%}"
                          f"{year_dd(r, 2022):7.1%}{worst20(r):8.1%}   {h1:5.3f}/{h2:5.3f}"
                          f"{oos:7.3f}   {v}{mark}")
                    if c == PROTO_COST:
                        rows.append((f"66 {tag} {label(bk, g, b)} @{c}bps", cg, sh, dd,
                                     h1, h2, oos, turn_per_yr(tu), v))
        print("-" * 132)

    # ---- the mechanical null: is gross a pure lever?
    print("\nIS GROSS A PURE LEVER?  Each arm vs the same book at g=1.00, core=0 "
          f"({PROTO_COST} bps).")
    print("  A pure lever gives corr ~1.000, beta ~g, dSharpe ~0 (slightly negative from "
          "cost scaling).")
    print(f"  {'book':<12}{'g':>5}{'corr vs g=1':>13}{'beta':>7}{'dCAGR':>8}{'dSharpe':>9}"
          f"{'dMaxDD':>8}")
    slope = {}
    for bk in BOOKS:
        ref = RET[(bk, 1.00, 0.00, PROTO_COST)]
        cr, sr, ddr = m(ref)
        sh_by_g = []
        for g in GROSSES:
            r = RET[(bk, g, 0.00, PROTO_COST)]
            cg, sh, dd = m(r)
            sh_by_g.append(sh)
            corr = float(r.corr(ref))
            beta = float(np.polyfit(ref.values, r.values, 1)[0])
            print(f"  {bk:<12}{g:5.2f}{corr:13.4f}{beta:7.3f}{(cg - cr) * 100:+8.2f}"
                  f"{sh - sr:+9.3f}{(dd - ddr) * 100:+8.2f}")
        b1 = float(np.polyfit(GROSSES, sh_by_g, 1)[0])
        slope[bk] = b1
        print(f"  {bk:<12}  Sharpe slope d(Sharpe)/d(gross) = {b1:+.3f} per 1.00 of gross "
              f"(range {min(sh_by_g):.3f}-{max(sh_by_g):.3f})")
    print()

    # ---- the question: 100% gross vs 75% gross + 25% SPY core
    print("SLEEVE OR DETOUR?  Both arms target 100% invested; one puts a quarter of it in "
          "SPY.\n  (idea 63's own arm, g=0.75 b=0.25, is in the main grid above at "
          "75% invested.)")
    print(f"  {'book':<12}{'bps':>5}   {'g=1.00 with 25% SPY core':<34}"
          f"{'g=1.00 all-active':<34}  verdicts")
    for bk in BOOKS:
        for c in COSTS:
            a = RET[(bk, 1.00, 0.25, c)]     # 75% active + 25% SPY = 100% invested
            f_ = RET[(bk, 1.00, 0.00, c)]
            ca, sa, dda = m(a); cf, sf, ddf = m(f_)
            h1a, h2a = halves(a); h1f, h2f = halves(f_)
            oa, of = m(a.loc[OOS_START:])[1], m(f_.loc[OOS_START:])[1]
            va = "4b PASS" if not fail4b(a, spy, oa, ss_o) else \
                 "4b fail(" + ",".join(fail4b(a, spy, oa, ss_o)) + ")"
            vf = "4b PASS" if not fail4b(f_, spy, of, ss_o) else \
                 "4b fail(" + ",".join(fail4b(f_, spy, of, ss_o)) + ")"
            print(f"  {bk:<12}{c:5d}   {ca:6.1%}/{sa:.3f}/{dda:6.1%} h {h1a:.3f}/{h2a:.3f} "
                  f"O{oa:.3f}   {cf:6.1%}/{sf:.3f}/{ddf:6.1%} h {h1f:.3f}/{h2f:.3f} "
                  f"O{of:.3f}   core {va} | full {vf}")
        print()

    # paired significance: core arm minus full-gross arm, same days, same total exposure
    print(f"Paired significance at {PROTO_COST} bps — (75% active + 25% SPY) minus "
          "(100% active), both fully invested:")
    for bk in BOOKS:
        d = (RET[(bk, 1.00, 0.25, PROTO_COST)] - RET[(bk, 1.00, 0.00, PROTO_COST)]).dropna()
        t = d.mean() / d.std() * np.sqrt(len(d))
        print(f"  {bk:<12}{d.mean() * 25200:+7.2f}%/yr  t {t:+5.2f}")
    print()

    # calendar-year detail for the two ends of the gross sweep
    print("Calendar years — g=0.75 vs g=1.00 (core=0) vs the 25% core arm vs SPY, "
          f"{PROTO_COST} bps:")
    hdr = f"  {'year':<6}{'SPY':>8}"
    for bk in BOOKS:
        hdr += f"{bk[:9] + ' .75':>14}{bk[:9] + ' 1.0':>14}{bk[:9] + ' core':>15}"
    print(hdr)
    for y in sorted({d.year for d in spy.index}):
        line = f"  {y:<6}{(1 + spy[spy.index.year == y]).prod() - 1:8.1%}"
        for bk in BOOKS:
            for key in ((bk, 0.75, 0.00), (bk, 1.00, 0.00), (bk, 1.00, 0.25)):
                r = RET[(key[0], key[1], key[2], PROTO_COST)]
                w = 14 if key[2] == 0.00 else 15
                line += f"{(1 + r[r.index.year == y]).prod() - 1:{w}.1%}"
        print(line)
    print()

    return dict(G=G, RET=RET, spy=spy, ss_o=ss_o, b_gross=b_gross, b_turn=b_turn,
                start=start, rows=rows, slope=slope)


# ---------------------------------------------------------------- cross-universe
def pass4b_set(res, cost):
    spy, ss_o = res["spy"], res["ss_o"]
    out = set()
    for bk, g, b in ARMS:
        r = res["RET"][(bk, g, b, cost)]
        if not fail4b(r, spy, m(r.loc[OOS_START:])[1], ss_o):
            out.add((bk, g, b))
    return out


def cross_universe(main_res, broad_res):
    print(f"\n{'=' * 132}")
    print("CROSS-UNIVERSE 4b — arms clearing all five 4b tests on universe.json AND "
          "universe_broad.json.\nIdeas 2 and 55's candidates both fail this; idea 63's "
          "25% core arm was the first to survive it at 25 bps.")
    print("=" * 132)
    surv = {}
    for c in COSTS:
        a, b = pass4b_set(main_res, c), pass4b_set(broad_res, c)
        both = sorted(a & b)
        surv[c] = both
        print(f"\n  @{c:>2} bps: universe.json {len(a)}/{len(ARMS)}, broad {len(b)}/{len(ARMS)}"
              f", BOTH: {len(both)}")
        for key in both:
            for tag, res in (("universe.json", main_res), ("broad", broad_res)):
                r = res["RET"][(key[0], key[1], key[2], c)]
                cg, sh, dd = m(r); h1, h2 = halves(r)
                co, so, ddo = m(r.loc[OOS_START:])
                print(f"      {label(*key):<28}{tag:<14} full {cg:5.1%}/{sh:.3f}/{dd:6.1%}"
                      f"  halves {h1:.3f}/{h2:.3f}  OOS {co:5.1%}/{so:.3f}/{ddo:6.1%}"
                      f"  turn {turn_per_yr(res['G'][key][1]):.1f}x")
    return surv


# ---------------------------------------------------------------- rule 8
def walk_forward(res, tag):
    """PROTOCOL rule 8: choose gross on 2009-2016, evaluate untouched on 2017-2026.

    Two selection rules, both fixed BEFORE any OOS number is read:
      R1 — highest in-sample Sharpe among all arms.
      R2 — 4b-aware: among arms clearing SPY's in-sample Sharpe/MaxDD/CAGR 4b bars,
           the highest in-sample CAGR (the bar idea 63 said gross was there to fix).
    """
    RET, spy = res["RET"], res["spy"]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc_i, ss_i, sdd_i = m(spy_is)
    sc_o, ss_o, sdd_o = m(spy_oos)
    base_o = m(at_cost(res["b_gross"], res["b_turn"], PROTO_COST).loc[OOS_START:])
    print(f"\nWalk-forward ({tag}): IS <= {IS_END}, OOS >= {OOS_START}, {PROTO_COST} bps")
    print(f"  IS 4b bars: Sharpe>{ss_i:.3f}  MaxDD>={0.60 * sdd_i:.1%}  CAGR>={0.70 * sc_i:.1%}")
    cand = []
    for bk, g, b in ARMS:
        c_, s_, dd_ = m(RET[(bk, g, b, PROTO_COST)].loc[:IS_END])
        cand.append(dict(key=(bk, g, b), sh=s_, cagr=c_, dd=dd_))
    print(f"  {'arm':<28}{'IS CAGR':>9}{'IS Sharpe':>11}{'IS MaxDD':>10}{'clears IS 4b?':>15}")
    for c in sorted(cand, key=lambda x: -x["sh"]):
        ok = c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i and c["cagr"] >= 0.70 * sc_i
        print(f"  {label(*c['key']):<28}{c['cagr']:9.1%}{c['sh']:11.3f}{c['dd']:10.1%}"
              f"{('yes' if ok else 'no'):>15}")

    # every grid point's OOS, so the reader sees where the OOS drawdown cap bites,
    # independently of which arm the two selection rules happen to land on.
    print(f"\n  OOS for EVERY grid point ({tag}, {PROTO_COST} bps) — reported, not selected:")
    print(f"  {'arm':<28}{'OOS CAGR':>10}{'OOS Sharpe':>12}{'OOS MaxDD':>11}   OOS 4b")
    for bk, g, b in ARMS:
        ro = RET[(bk, g, b, PROTO_COST)].loc[OOS_START:]
        co, so, ddo = m(ro)
        bad = []
        if so <= ss_o: bad.append("Sharpe")
        if ddo < 0.60 * sdd_o: bad.append("MaxDD")
        if co < 0.70 * sc_o: bad.append("CAGR")
        print(f"  {label(bk, g, b):<28}{co:10.1%}{so:12.3f}{ddo:11.1%}   "
              + ("PASS" if not bad else "FAIL (" + ",".join(bad) + ")"))

    r1 = max(cand, key=lambda x: x["sh"])["key"]
    ok = [c for c in cand if c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i
          and c["cagr"] >= 0.70 * sc_i]
    r2 = max(ok, key=lambda x: x["cagr"])["key"] if ok else None

    print(f"\n  SPY OOS  {sc_o:.1%}/{ss_o:.3f}/{sdd_o:.1%}   "
          f"RULES v1 OOS {base_o[0]:.1%}/{base_o[1]:.3f}/{base_o[2]:.1%}")
    print(f"  OOS 4b bars: Sharpe>{ss_o:.3f}  MaxDD>={0.60 * sdd_o:.1%}  CAGR>={0.70 * sc_o:.1%}")
    out = {}
    for rule, key in (("R1 max IS Sharpe", r1), ("R2 4b-aware, max IS CAGR", r2)):
        if key is None:
            print(f"  {rule:<26} -> no arm clears the IS 4b bars")
            continue
        ro = RET[(key[0], key[1], key[2], PROTO_COST)].loc[OOS_START:]
        co, so, ddo = m(ro)
        bad = []
        if so <= ss_o: bad.append("Sharpe")
        if ddo < 0.60 * sdd_o: bad.append("MaxDD")
        if co < 0.70 * sc_o: bad.append("CAGR")
        print(f"  {rule:<26} -> {label(*key):<28} OOS {co:.1%}/{so:.3f}/{ddo:.1%}   "
              + ("OOS 4b PASS" if not bad else "OOS 4b FAIL (" + ",".join(bad) + ")"))
        out[rule] = (key, co, so, ddo, bad)
    return out


# ---------------------------------------------------------------- main
def main():
    print(__doc__)
    px = load_universe()
    pb = load_universe(broad=True)
    main_res = sweep(px, "universe.json")
    broad_res = sweep(pb, "universe_broad.json")
    surv = cross_universe(main_res, broad_res)
    wf_main = walk_forward(main_res, "universe.json")
    wf_broad = walk_forward(broad_res, "universe_broad.json")

    print(f"\n{'=' * 132}\nLEADERBOARD rows ({PROTO_COST} bps, headline arms)\n{'=' * 132}")
    for tag, res in (("universe.json", main_res), ("universe_broad.json", broad_res)):
        for name, cg, sh, dd, h1, h2, oos, tu, v in res["rows"]:
            if ("g=0.75 core=0.00" in name or "g=1.00 core=0.00" in name
                    or "g=1.00 core=0.25" in name):
                print(f"| 2026-09-04 | {name} | {cg:.1%} | {sh:.2f} | {dd:.1%} | "
                      f"{h1:.2f} / {h2:.2f} | OOS {oos:.2f} | turn {tu:.1f}x | {v} | "
                      f"{Path(SCRIPT).name} |")

    print(f"\n{'=' * 132}\nSUMMARY\n{'=' * 132}")
    print(f"Sharpe slope per 1.00 of gross — universe.json {main_res['slope']}, "
          f"broad {broad_res['slope']}")
    print(f"Cross-universe 4b survivors by cost: "
          f"{ {c: [label(*k) for k in v] for c, v in surv.items()} }")
    print(f"Walk-forward picks — universe.json {[(k, label(*v[0])) for k, v in wf_main.items()]}")
    print(f"Walk-forward picks — broad        {[(k, label(*v[0])) for k, v in wf_broad.items()]}")


if __name__ == "__main__":
    main()
