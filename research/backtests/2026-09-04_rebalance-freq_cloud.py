#!/usr/bin/env python3
"""QUEUE idea 3 — rebalance-freq (cloud, 2026-09-04).

Question
--------
Every result in this project rebalances WEEKLY, a choice nobody has ever tested.
Idea 3 asks the plain version: daily vs weekly vs monthly vs quarterly, for RULES
v1 and — because the live book is not where capital would go — for the two standing
4b candidates as well.

The prior from ideas 55/57/4 is sharp and makes this a real test rather than a
parameter sweep.  Those runs found that in the gate-only book net Sharpe orders by
FLIP RATE: the cheapest (slowest) trend instrument wins, and the incumbent 200d
gate loses because it flips 7.55x/ticker/yr and pays the whipsaw.  Rebalance
frequency is the other, cruder way to slow a book down: it cuts turnover directly
AND it re-evaluates the gate less often.  If the whipsaw story is right, monthly
should beat weekly at 10 bps in the gate-driven books, and the advantage should
widen with cost.  If monthly does NOT win, the whipsaw story is about the signal,
not about trading frequency, and idea 57's band gate is doing something a slower
calendar cannot do.  Idea 57 already noted in passing that a monthly-re-evaluated
gate "performed as well as either" band — this run measures it properly.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names, incl. SPY/ETFs).
           Full robustness pass on universe_broad.json (136 names).  Both reported.
Books    : four PRE-CHOSEN constructions, none tuned here —
           * `v1`        — rules_v1_weights exactly as live (n=5, 15% each, composite
                           WITH /sqrt(vol20)).  This is idea 3's literal subject.
           * `top20`     — idea 2's 4b KEEP: top-20 by the composite without the vol
                           scaler, among 200d/vol20-eligible names, 3.75% each.
           * `ew-all`    — equal-weight every eligible name at 75% gross (idea 28/25).
           * `ew-band3`  — idea 57's 4b KEEP-candidate: same, with the 3% MA band
                           replacing the raw 200d gate.
Params   : exactly ONE tuned dimension — rebalance frequency, 4 arms {D, W, M, Q}.
           Book, n, gross, gate and vol20 are all inherited from earlier ideas.
           Every (book, freq, cost, universe) cell is printed; nothing is selected
           on out-of-sample data.
Costs    : 5 / 10 / 25 / 50 bps.  10 bps is the PROTOCOL cost and the one verdicts
           are read at.  Costs are applied analytically —
           returns(c) = gross_returns - turnover*c/1e4 — which is exactly what
           engine.backtest does (held/turnover do not depend on cost_bps); the
           harness check below asserts the identity against a real cost_bps=10 run.
Execution: weights decided at close t, applied at t+1 (engine), long-only, no
           leverage, no shorting.  Frequency changes the rebalance calendar only;
           between rebalances the book drifts, as the engine already models.
Baseline : RULES v1 at its live WEEKLY cadence, for the 4a comparison, at each cost.
Rule 8   : frequency (and book) chosen on 2009-2016 only under two selection rules
           fixed BEFORE any OOS number is read; 2017-2026 evaluated untouched.

SURVIVORSHIP: both lists are current constituents, so absolute CAGR/Sharpe are
optimistic.  The freq-vs-freq comparisons that answer the question are far less
exposed — every arm holds the same names on the same days, differing only in when
it trades.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
BAND = 0.03
COSTS = [5, 10, 25, 50]
PROTO_COST = 10
FREQS = ["D", "W", "M", "Q"]
REF_FREQ = "W"                       # the incumbent cadence every result so far used
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SCRIPT = "research/backtests/2026-09-04_rebalance-freq_cloud.py"


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2's candidate scorer)."""
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


def year_ret(r, y):
    s = r[r.index.year == y]
    return float((1 + s).prod() - 1) if len(s) else np.nan


def paired_t(a, b):
    d = (a - b).dropna()
    return float(d.mean() * 252), float(d.mean() / (d.std() / np.sqrt(len(d))))


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r)
    h1, h2 = halves(r)
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m(r)
    h1, h2 = halves(r)
    _, _, bdd = m(base)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def verdict(r, base, spy, oos_sh, spy_oos_sh):
    a, b = fail4a(r, base), fail4b(r, spy, oos_sh, spy_oos_sh)
    return ("KEEP 4a" if not a else "KILL 4a") + " / " + \
           ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")


# ---------------------------------------------------------------- run helpers
def gross_run(px, fn, freq, start):
    res = backtest(px, fn(px), cost_bps=0.0, freq=freq)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def at_cost(gross, turn, bps):
    return gross - turn * bps / 1e4


def turn_per_yr(turn):
    return turn.sum() / (len(turn) / 252)


# ---------------------------------------------------------------- one universe
def sweep(px, tag, results):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    _, ss_o, _ = m(spy.loc[OOS_START:])

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    print(f"\n{'=' * 134}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 134)

    G = {}
    for bk, fn in BOOKS.items():
        for f in FREQS:
            G[(bk, f)] = gross_run(px, fn, f, start)
    b_gross, b_turn = G[("v1", REF_FREQ)]                  # live book, live cadence
    b10 = at_cost(b_gross, b_turn, PROTO_COST)
    bc, bs, bdd = m(b10)
    bh1, bh2 = halves(b10)
    print(f"RULES v1 baseline (weekly) @{PROTO_COST}bps: {bc:.1%}/{bs:.3f}/{bdd:.1%} "
          f"halves {bh1:.3f}/{bh2:.3f} OOS Sharpe {m(b10.loc[OOS_START:])[1]:.3f} "
          f"(4a bars: H1>{bh1:.3f}, H2>{bh2:.3f}, MaxDD>={bdd:.1%})")

    # ---- rebalance mechanics
    print("\nRebalance mechanics — trades per year and resulting turnover per book:")
    print(f"  {'freq':<6}{'rebal/yr':>10}   " + "".join(f"{bk + ' turn':>16}" for bk in BOOKS))
    from engine import rebalance_mask
    for f in FREQS:
        n_rb = rebalance_mask(px.index, f).loc[start:].sum() / (len(px.loc[start:]) / 252)
        print(f"  {f:<6}{n_rb:10.1f}   " +
              "".join(f"{turn_per_yr(G[(bk, f)][1]):15.1f}x" for bk in BOOKS))

    # ---- main grid
    print(f"\n{'book':<10}{'freq':<6}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'2020':>8}"
          f"{'2022':>8}{'turn':>7}   {'H1':>5}/{'H2':>5}{'OOS':>7}   verdict")
    print("-" * 134)
    RET = {}
    for bk in BOOKS:
        for f in FREQS:
            gr, tu = G[(bk, f)]
            for c in COSTS:
                r = at_cost(gr, tu, c)
                RET[(bk, f, c)] = r
                base = at_cost(b_gross, b_turn, c)
                cg, sh, dd = m(r)
                h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                v = verdict(r, base, spy, oos, ss_o)
                mark = " <-" if c == PROTO_COST else ""
                print(f"{bk:<10}{f:<6}{c:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}{year_ret(r, 2020):8.1%}"
                      f"{year_ret(r, 2022):8.1%}{turn_per_yr(tu):6.1f}x   "
                      f"{h1:5.3f}/{h2:5.3f}{oos:7.3f}   {v}{mark}")
                if c == PROTO_COST:
                    results.append(dict(tag=tag, book=bk, freq=f, cagr=cg, sharpe=sh, dd=dd,
                                        h1=h1, h2=h2, oos=oos, turn=turn_per_yr(tu), verdict=v,
                                        pass4b=not fail4b(r, spy, oos, ss_o),
                                        pass4a=not fail4a(r, at_cost(b_gross, b_turn, PROTO_COST))))
        print("-" * 134)

    # ---- the idea's own test: each cadence minus WEEKLY, same book, same days
    print("IDEA 3's TEST — each cadence minus the incumbent WEEKLY, same book, same days "
          "(paired daily differences):")
    print(f"  {'book':<10}{'freq':<6}{'bps':>5}{'dCAGR':>8}{'dSharpe':>9}{'dMaxDD':>8}"
          f"{'dTurn':>9}{'ann.diff':>10}{'t':>7}")
    for bk in BOOKS:
        for f in FREQS:
            if f == REF_FREQ:
                continue
            for c in (PROTO_COST, 25):
                r, r0 = RET[(bk, f, c)], RET[(bk, REF_FREQ, c)]
                cg, sh, dd = m(r)
                cg0, sh0, dd0 = m(r0)
                ann, t = paired_t(r, r0)
                dturn = turn_per_yr(G[(bk, f)][1]) - turn_per_yr(G[(bk, REF_FREQ)][1])
                print(f"  {bk:<10}{f:<6}{c:5d}{(cg - cg0) * 100:+8.2f}{sh - sh0:+9.3f}"
                      f"{(dd - dd0) * 100:+8.2f}{dturn:+8.1f}x{ann * 100:+10.2f}{t:+7.2f}")
        print()

    # ---- cost-crossover: at which cost does the best cadence change?
    print("BEST CADENCE BY COST (by net Sharpe) — does the ranking flip as costs rise?")
    print(f"  {'book':<10}" + "".join(f"{str(c) + 'bps':>26}" for c in COSTS))
    for bk in BOOKS:
        cells = []
        for c in COSTS:
            best = max(FREQS, key=lambda f: m(RET[(bk, f, c)])[1])
            cells.append(f"{best} ({m(RET[(bk, best, c)])[1]:.3f})")
        print(f"  {bk:<10}" + "".join(f"{x:>26}" for x in cells))

    # ---- 4b margins
    print("\nMARGINS on each 4b bar at 10 bps (positive = clears; binding bar named):")
    print(f"  {'book':<10}{'freq':<6}{'H1-bar':>9}{'H2-bar':>9}{'OOS-bar':>9}"
          f"{'DD-slack(pp)':>14}{'CAGR-slack(pp)':>16}   binding")
    for bk in BOOKS:
        for f in FREQS:
            r = RET[(bk, f, PROTO_COST)]
            cg, sh, dd = m(r)
            h1, h2 = halves(r)
            oos = m(r.loc[OOS_START:])[1]
            mg = {"H1": h1 - s1, "H2": h2 - s2, "OOS": oos - ss_o,
                  "DD": (dd - 0.60 * sdd) * 100, "CAGR": (cg - 0.70 * sc) * 100}
            binding = min(mg, key=mg.get)
            print(f"  {bk:<10}{f:<6}{mg['H1']:+9.4f}{mg['H2']:+9.4f}{mg['OOS']:+9.4f}"
                  f"{mg['DD']:+14.2f}{mg['CAGR']:+16.2f}   {binding} ({mg[binding]:+.4f})")

    # ---- rule 8 walk-forward
    print(f"\nRule 8 walk-forward — cadence (and book) chosen on IS 2009-2016 only, "
          f"evaluated untouched on {OOS_START}-2026, at {PROTO_COST} bps.")
    is_spy, oos_spy = spy.loc[:IS_END], spy.loc[OOS_START:]
    isc, iss, isdd = m(is_spy)
    print(f"  IS SPY {isc:.1%}/{iss:.3f}/{isdd:.1%}   4b-aware IS bars: "
          f"MaxDD>={0.60 * isdd:.1%}, CAGR>={0.70 * isc:.1%}")
    print(f"  {'book':<10}{'freq':<6}{'IS CAGR':>9}{'IS Sh':>8}{'IS DD':>8}   "
          f"{'OOS CAGR':>9}{'OOS Sh':>8}{'OOS DD':>8}")
    cand = []
    for bk in BOOKS:
        for f in FREQS:
            r = RET[(bk, f, PROTO_COST)]
            ic, ish, idd = m(r.loc[:IS_END])
            oc, osh, odd = m(r.loc[OOS_START:])
            cand.append((bk, f, ic, ish, idd, oc, osh, odd))
            print(f"  {bk:<10}{f:<6}{ic:9.1%}{ish:8.3f}{idd:8.1%}   {oc:9.1%}{osh:8.3f}{odd:8.1%}")
    oc_s, osh_s, odd_s = m(oos_spy)
    bic, bish, bidd = m(b10.loc[:IS_END])
    boc, bosh, bodd = m(b10.loc[OOS_START:])
    print(f"  {'RULES v1 (W)':<16}{bic:9.1%}{bish:8.3f}{bidd:8.1%}   {boc:9.1%}{bosh:8.3f}{bodd:8.1%}")
    print(f"  {'SPY':<16}{isc:9.1%}{iss:8.3f}{isdd:8.1%}   {oc_s:9.1%}{osh_s:8.3f}{odd_s:8.1%}")

    def clears(c):
        return c[6] > osh_s and c[7] >= 0.60 * odd_s and c[5] >= 0.70 * oc_s

    r1 = max(cand, key=lambda x: x[3])
    ok = [c for c in cand if c[4] >= 0.60 * isdd and c[2] >= 0.70 * isc]
    r2 = max(ok, key=lambda x: x[3]) if ok else None
    print(f"  RULE A (max IS Sharpe)      -> {r1[0]}/{r1[1]}: OOS {r1[5]:.1%}/{r1[6]:.3f}/{r1[7]:.1%} "
          f"vs SPY {oc_s:.1%}/{osh_s:.3f}/{odd_s:.1%} [{'clears' if clears(r1) else 'FAILS'} OOS 4b bars]")
    if r2:
        print(f"  RULE B (4b-aware IS filter) -> {r2[0]}/{r2[1]}: OOS {r2[5]:.1%}/{r2[6]:.3f}/{r2[7]:.1%} "
              f"[{'clears' if clears(r2) else 'FAILS'} OOS 4b bars]")
    else:
        print("  RULE B (4b-aware IS filter) -> NOTHING selected (no IS point met the bars)")

    # ---- freq choice within each book: does IS pick the OOS winner?
    print("\n  Cadence chosen per book on IS Sharpe -> did it win OOS?")
    for bk in BOOKS:
        rows = [c for c in cand if c[0] == bk]
        pick = max(rows, key=lambda x: x[3])
        best_oos = max(rows, key=lambda x: x[6])
        print(f"    {bk:<10} IS picks {pick[1]} (OOS Sh {pick[6]:.3f}); "
              f"best OOS was {best_oos[1]} ({best_oos[6]:.3f}) -> "
              f"{'agrees' if pick[1] == best_oos[1] else 'DISAGREES'}")

    return RET


# ---------------------------------------------------------------- harness checks
def harness(px, start):
    print("\nHARNESS CHECKS")
    gr, tu = gross_run(px, w_top20, REF_FREQ, start)
    real = backtest(px, w_top20(px), cost_bps=PROTO_COST, freq=REF_FREQ)["returns"].loc[start:]
    err = float((at_cost(gr, tu, PROTO_COST) - real).abs().max())
    print(f"  analytic-cost identity vs engine cost_bps=10: max abs daily diff {err:.2e} "
          f"({'OK' if err < 1e-12 else 'MISMATCH'})")
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 2 KEEP row (top20, weekly): {c:.1%}/{s:.3f}/{dd:.1%}   [published 12.7%/1.093/-18.3%]")
    gr, tu = gross_run(px, w_ewband, REF_FREQ, start)
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 57 KEEP-candidate (ew-band3, weekly): {c:.1%}/{s:.3f}/{dd:.1%}"
          f"   [published 11.3%/1.136/-15.1%]")
    gr, tu = gross_run(px, w_ewall, REF_FREQ, start)
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 28/4 ew-all 200d control (weekly): {c:.1%}/{s:.3f}/{dd:.1%}"
          f"   [published 10.4%/1.05/-15.9%]")


# ---------------------------------------------------------------- main
def main():
    results = []
    px = load_universe()
    harness(px, px.index[260])
    sweep(px, "universe.json", results)
    pxb = load_universe(broad=True)
    sweep(pxb, "universe_broad.json", results)

    print(f"\n{'=' * 134}\nCROSS-UNIVERSE 4b SUMMARY at {PROTO_COST} bps "
          "(an arm only counts if it passes on BOTH lists)\n" + "=" * 134)
    print(f"  {'book':<10}{'freq':<6}{'universe.json':>28}{'universe_broad.json':>30}   both?")
    df = pd.DataFrame(results)
    n_both = 0
    for bk in BOOKS:
        for f in FREQS:
            a = df[(df.tag == "universe.json") & (df.book == bk) & (df.freq == f)].iloc[0]
            b = df[(df.tag == "universe_broad.json") & (df.book == bk) & (df.freq == f)].iloc[0]
            both = "YES" if a.pass4b and b.pass4b else "no"
            n_both += both == "YES"
            print(f"  {bk:<10}{f:<6}{a.cagr:9.1%}/{a.sharpe:.3f}/{a.dd:7.1%}"
                  f"{b.cagr:11.1%}/{b.sharpe:.3f}/{b.dd:7.1%}   {both}")
    print(f"\n  {n_both} of {len(BOOKS) * len(FREQS)} arms pass 4b on both universes at "
          f"{PROTO_COST} bps.")
    print(f"  4a passes (universe.json): "
          f"{[f'{r.book}/{r.freq}' for _, r in df[(df.tag == 'universe.json') & df.pass4a].iterrows()]}")
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
