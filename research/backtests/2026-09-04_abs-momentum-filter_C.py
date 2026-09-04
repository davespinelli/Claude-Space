#!/usr/bin/env python3
"""QUEUE idea 4 — abs-momentum-filter (lane C, 2026-09-04).

Question
--------
RULES v1 gates eligibility on `px > 200d MA`.  Idea 4 asks whether **absolute
(time-series) momentum** — 12-1 return > 0, the Moskowitz/Ooi/Pedersen and
Antonacci signal — is a better gate: replace the 200d MA with it, and also try
requiring both.

This is the third instrument test in a row and it inherits a sharp prior.  Idea 55
found the 200d gate's *return* contribution indistinguishable from zero on both
large-cap lists; idea 57 priced it as insurance and found it never pays, because it
flips 7.55x/ticker/yr and pays the whipsaw.  The mechanistic prediction here is
therefore specific and falsifiable: **12-1 momentum is a slower signal than a 200d
MA cross** (it compares two points a year apart rather than a price to a trailing
mean), so it should flip less often, cost less turnover, and — if idea 57's whipsaw
story is right — dominate the 200d gate at the same drawdown protection.  If it does
NOT, the whipsaw story is wrong or incomplete.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names, incl. SPY and ETFs).
           Robustness pass on universe_broad.json (136 names).  Both fully reported.
Books    : the same two books ideas 55 and 57 used, so every number here is directly
           comparable to theirs —
           * `top20` — idea 2's KEEP-candidate construction: top-20 by the composite
             (mean pct-rank of 12-1, 6m, 3m, NO /sqrt(vol20)) among eligible names,
             equal weight 0.75/20 = 3.75% each.  n=20 pre-chosen, NOT tuned here.
           * `ew-all` — equal-weight EVERY eligible name at 75% gross, no ranking.
             This is the gate-only control: it isolates the gate from the ranking,
             and it is the book idea 57's KEEP-candidate lives in.
Gate     : eligible = (vol20 < 0.60) & G, with the vol20 half held FIXED at v1's
           value (idea 56 owns that half).  G in five arms:
             none    — no trend gate at all (the uninsured control)
             200d    — px > 200d MA, weekly re-evaluated (the incumbent)
             abs     — 12-1 return > 0  (THE IDEA: px[t-21]/px[t-252] - 1 > 0)
             both    — 200d AND abs     (THE IDEA's second arm)
             band3   — px crosses +3% above MA to enter, -3% below to exit
                       (idea 57's KEEP-candidate gate; carried as a REFERENCE arm,
                       not tuned here, so the new arms are judged against the
                       standing candidate rather than only against the incumbent)
Params   : exactly 1 tuned dimension — the gate instrument (5 arms).  The 12-1
           lookback is the idea's own specification, not a swept parameter; book,
           n, gross and vol20 are all pre-chosen from earlier ideas.  Every arm is
           reported at every cost on both universes; nothing is selected on OOS.
Costs    : 5 / 10 / 25 / 50 bps.  10 bps is the PROTOCOL cost and the one verdicts
           are read at.  Costs are applied analytically —
           `returns(c) = gross_returns - turnover * c/1e4` — which is exactly what
           engine.backtest does (held/turnover do not depend on cost_bps); a harness
           check below asserts the identity against a real cost_bps=10 run.
Execution: weekly rebalance, weights decided at close t applied at t+1 (engine),
           long-only, no leverage, no shorting.
Rule 8   : gate chosen on 2009-2016 only under two selection rules fixed BEFORE any
           OOS number is read, evaluated untouched on 2017-2026.

SURVIVORSHIP: both lists are current constituents, so absolute CAGR/Sharpe are
optimistic.  The gate-vs-gate comparisons that answer the question are far less
exposed — every arm draws from the same names on the same days.
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
COSTS = [5, 10, 25, 50]
PROTO_COST = 10
GATES = ["none", "200d", "abs", "both", "band3"]
NEW = ["abs", "both"]                       # the arms idea 4 actually proposes
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SCRIPT = "research/backtests/2026-09-04_abs-momentum-filter_C.py"


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2's candidate scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def abs_mom(px):
    """12-1 total return, skipping the most recent month (the standard construction)."""
    return px.shift(21) / px.shift(252) - 1


def trend(px, gate):
    """The trend half of the eligibility filter as a boolean frame. NaN -> False."""
    if gate == "none":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "200d":
        return (px > ma).fillna(False)
    if gate == "abs":
        return (abs_mom(px) > 0).fillna(False)
    if gate == "both":
        return ((px > ma) & (abs_mom(px) > 0)).fillna(False)
    if gate.startswith("band"):
        b = int(gate[4:]) / 100.0
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + b), 1.0)
        raw = raw.mask(px < ma * (1 - b), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    raise ValueError(gate)


def eligible(px, gate):
    return (vol20(px) < MAX_VOL) & trend(px, gate)


def w_top20(gate):
    def f(px):
        rank = composite(px).where(eligible(px, gate)).rank(axis=1, ascending=False)
        return (rank <= NPOS).astype(float) * (GROSS / NPOS)
    return f


def w_ewall(gate):
    def f(px):
        e = eligible(px, gate).astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS
    return f


BOOKS = {"top20": w_top20, "ew-all": w_ewall}


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


def year_dd(r, y):
    s = r[r.index.year == y]
    return float(dd_series(s).min()) if len(s) else np.nan


def flips_per_ticker_yr(px, gate, start):
    """How often the gate changes state, per ticker per year — the whipsaw measure."""
    t = trend(px, gate).loc[start:]
    yrs = len(t) / 252
    return float(t.astype(int).diff().abs().sum().sum() / t.shape[1] / yrs)


def paired_t(a, b):
    """Annualised mean of (a-b) and its t-stat on daily differences."""
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
def gross_run(px, fn, start):
    res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
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

    print(f"\n{'=' * 132}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 132)

    G = {}
    for bk, mk in BOOKS.items():
        for g in GATES:
            G[(bk, g)] = gross_run(px, mk(g), start)
    b_gross, b_turn = gross_run(px, rules_v1_weights, start)
    bc, bs, bdd = m(at_cost(b_gross, b_turn, PROTO_COST))
    bh1, bh2 = halves(at_cost(b_gross, b_turn, PROTO_COST))
    print(f"RULES v1 baseline @{PROTO_COST}bps: {bc:.1%}/{bs:.3f}/{bdd:.1%} "
          f"halves {bh1:.3f}/{bh2:.3f} OOS Sharpe "
          f"{m(at_cost(b_gross, b_turn, PROTO_COST).loc[OOS_START:])[1]:.3f} "
          f"(4a bars: H1>{bh1:.3f}, H2>{bh2:.3f}, MaxDD>={bdd:.1%})")

    # ---- gate mechanics: how many names pass, how often the signal flips
    print("\nGate mechanics — names passing the trend half, flip rate, and resulting book:")
    print(f"  {'gate':<8}{'mean pass':>10}{'median':>8}{'min':>6}{'flips/tkr/yr':>14}"
          f"{'ew-all gross':>14}{'days<20 elig':>14}{'top20 turn':>12}{'ew-all turn':>13}")
    for g in GATES:
        t = trend(px, g).loc[start:]
        e = eligible(px, g).loc[start:].sum(axis=1)
        ewg = backtest(px, BOOKS["ew-all"](g)(px), cost_bps=0.0, freq=FREQ)["weights"].loc[start:].sum(axis=1)
        print(f"  {g:<8}{t.sum(axis=1).mean():10.1f}{t.sum(axis=1).median():8.0f}"
              f"{t.sum(axis=1).min():6.0f}{flips_per_ticker_yr(px, g, start):14.2f}"
              f"{ewg.mean():13.1%}{(e < NPOS).mean():13.1%}"
              f"{turn_per_yr(G[('top20', g)][1]):11.1f}x{turn_per_yr(G[('ew-all', g)][1]):12.1f}x")

    # ---- main grid
    print(f"\n{'book':<8}{'gate':<8}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'2020':>8}"
          f"{'2022':>8}{'22DD':>8}{'turn':>7}   {'H1':>5}/{'H2':>5}{'OOS':>7}   verdict")
    print("-" * 132)
    RET = {}
    for bk in BOOKS:
        for g in GATES:
            gr, tu = G[(bk, g)]
            for c in COSTS:
                r = at_cost(gr, tu, c)
                RET[(bk, g, c)] = r
                base = at_cost(b_gross, b_turn, c)
                cg, sh, dd = m(r)
                h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                v = verdict(r, base, spy, oos, ss_o)
                mark = " <-" if c == PROTO_COST else ""
                print(f"{bk:<8}{g:<8}{c:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}{year_ret(r, 2020):8.1%}"
                      f"{year_ret(r, 2022):8.1%}{year_dd(r, 2022):8.1%}"
                      f"{turn_per_yr(tu):6.1f}x   {h1:5.3f}/{h2:5.3f}{oos:7.3f}   {v}{mark}")
                if c == PROTO_COST:
                    results.append(dict(tag=tag, book=bk, gate=g, cagr=cg, sharpe=sh, dd=dd,
                                        h1=h1, h2=h2, oos=oos, turn=turn_per_yr(tu), verdict=v,
                                        pass4b=not fail4b(r, spy, oos, ss_o)))
        print("-" * 132)

    # ---- the idea's own question: abs / both vs the 200d incumbent
    print("\nIDEA 4's TEST — each arm minus the 200d incumbent, same book, same days "
          "(paired daily differences at 10 bps):")
    print(f"  {'book':<8}{'gate':<8}{'dCAGR':>8}{'dSharpe':>9}{'dMaxDD':>8}{'dTurn':>8}"
          f"{'ann.diff':>10}{'t':>7}")
    for bk in BOOKS:
        for g in ["none", "abs", "both", "band3"]:
            r, r0 = RET[(bk, g, PROTO_COST)], RET[(bk, "200d", PROTO_COST)]
            cg, sh, dd = m(r)
            cg0, sh0, dd0 = m(r0)
            ann, t = paired_t(r, r0)
            dturn = turn_per_yr(G[(bk, g)][1]) - turn_per_yr(G[(bk, "200d")][1])
            print(f"  {bk:<8}{g:<8}{(cg - cg0) * 100:+8.2f}{sh - sh0:+9.3f}{(dd - dd0) * 100:+8.2f}"
                  f"{dturn:+7.1f}x{ann * 100:+10.2f}{t:+7.2f}")
        print()

    print("SAME, against the UNGATED control (gate=none) — is any gate worth its cost at all?")
    print(f"  {'book':<8}{'gate':<8}{'dCAGR':>8}{'dSharpe':>9}{'dMaxDD':>8}{'dTurn':>8}"
          f"{'ann.diff':>10}{'t':>7}{'pp CAGR/pp DD':>16}")
    for bk in BOOKS:
        for g in ["200d", "abs", "both", "band3"]:
            r, r0 = RET[(bk, g, PROTO_COST)], RET[(bk, "none", PROTO_COST)]
            cg, sh, dd = m(r)
            cg0, sh0, dd0 = m(r0)
            ann, t = paired_t(r, r0)
            dturn = turn_per_yr(G[(bk, g)][1]) - turn_per_yr(G[(bk, "none")][1])
            ddd = dd - dd0
            price = (-(cg - cg0) * 100) / (ddd * 100) if ddd > 1e-9 else np.nan
            print(f"  {bk:<8}{g:<8}{(cg - cg0) * 100:+8.2f}{sh - sh0:+9.3f}{ddd * 100:+8.2f}"
                  f"{dturn:+7.1f}x{ann * 100:+10.2f}{t:+7.2f}"
                  f"{price if np.isfinite(price) else float('nan'):16.2f}")
        print()

    # ---- 4b margins: a pass by 0.001 is not a pass worth capital
    print("MARGINS on each 4b bar at 10 bps (positive = clears; the binding bar is the "
          "smallest positive or any negative):")
    print(f"  {'book':<8}{'gate':<8}{'H1-bar':>9}{'H2-bar':>9}{'OOS-bar':>9}"
          f"{'DD-slack(pp)':>14}{'CAGR-slack(pp)':>16}   binding")
    for bk in BOOKS:
        for g in GATES:
            r = RET[(bk, g, PROTO_COST)]
            cg, sh, dd = m(r)
            h1, h2 = halves(r)
            oos = m(r.loc[OOS_START:])[1]
            mg = {"H1": h1 - s1, "H2": h2 - s2, "OOS": oos - ss_o,
                  "DD": (dd - 0.60 * sdd) * 100, "CAGR": (cg - 0.70 * sc) * 100}
            binding = min(mg, key=mg.get)
            print(f"  {bk:<8}{g:<8}{mg['H1']:+9.4f}{mg['H2']:+9.4f}{mg['OOS']:+9.4f}"
                  f"{mg['DD']:+14.2f}{mg['CAGR']:+16.2f}   {binding} "
                  f"({mg[binding]:+.4f})")
    print()

    # ---- mechanism: does the Sharpe ordering follow the flip (whipsaw) ordering?
    print("WHIPSAW ORDERING — idea 57 predicts fewer flips -> better net Sharpe. "
          "Gates ranked by flip rate:")
    fl = sorted(((flips_per_ticker_yr(px, g, start), g) for g in GATES if g != "none"))
    for bk in BOOKS:
        line = "  " + f"{bk:<8}" + "  ".join(
            f"{g}({f:.2f} flips, Sh {m(RET[(bk, g, PROTO_COST)])[1]:.3f})" for f, g in fl)
        print(line)
    print()

    # ---- rule 8 walk-forward: pick the gate on 2009-2016, read 2017-2026 untouched
    print("Rule 8 walk-forward — gate (and book) chosen on IS 2009-2016 only, "
          f"evaluated untouched on {OOS_START}-2026, at {PROTO_COST} bps.")
    is_spy, oos_spy = spy.loc[:IS_END], spy.loc[OOS_START:]
    isc, iss, isdd = m(is_spy)
    print(f"  IS SPY {isc:.1%}/{iss:.3f}/{isdd:.1%}   4b-aware IS bars: "
          f"MaxDD>={0.60 * isdd:.1%}, CAGR>={0.70 * isc:.1%}")
    print(f"  {'book':<8}{'gate':<8}{'IS CAGR':>9}{'IS Sh':>8}{'IS DD':>8}   "
          f"{'OOS CAGR':>9}{'OOS Sh':>8}{'OOS DD':>8}")
    cand = []
    for bk in BOOKS:
        for g in GATES:
            r = RET[(bk, g, PROTO_COST)]
            ic, ish, idd = m(r.loc[:IS_END])
            oc, osh, odd = m(r.loc[OOS_START:])
            cand.append((bk, g, ic, ish, idd, oc, osh, odd))
            print(f"  {bk:<8}{g:<8}{ic:9.1%}{ish:8.3f}{idd:8.1%}   {oc:9.1%}{osh:8.3f}{odd:8.1%}")
    oc_s, osh_s, odd_s = m(oos_spy)
    b10 = at_cost(b_gross, b_turn, PROTO_COST)
    bic, bish, bidd = m(b10.loc[:IS_END])
    boc, bosh, bodd = m(b10.loc[OOS_START:])
    print(f"  {'RULES v1 base':<16}{bic:9.1%}{bish:8.3f}{bidd:8.1%}   {boc:9.1%}{bosh:8.3f}{bodd:8.1%}")
    print(f"  {'SPY':<16}{isc:9.1%}{iss:8.3f}{isdd:8.1%}   {oc_s:9.1%}{osh_s:8.3f}{odd_s:8.1%}")

    r1 = max(cand, key=lambda x: x[3])
    ok = [c for c in cand if c[4] >= 0.60 * isdd and c[2] >= 0.70 * isc]
    r2 = max(ok, key=lambda x: x[3]) if ok else None
    print(f"  RULE A (max IS Sharpe)      -> {r1[0]}/{r1[1]}: "
          f"OOS {r1[5]:.1%}/{r1[6]:.3f}/{r1[7]:.1%} vs SPY {oc_s:.1%}/{osh_s:.3f}/{odd_s:.1%} "
          f"[{'clears' if r1[6] > osh_s and r1[7] >= 0.60 * odd_s and r1[5] >= 0.70 * oc_s else 'FAILS'} OOS 4b bars]")
    if r2:
        print(f"  RULE B (4b-aware IS filter) -> {r2[0]}/{r2[1]}: "
              f"OOS {r2[5]:.1%}/{r2[6]:.3f}/{r2[7]:.1%} "
              f"[{'clears' if r2[6] > osh_s and r2[7] >= 0.60 * odd_s and r2[5] >= 0.70 * oc_s else 'FAILS'} OOS 4b bars]")
    else:
        print("  RULE B (4b-aware IS filter) -> NOTHING selected (no IS point met the bars)")

    return RET, G, start, spy


# ---------------------------------------------------------------- harness checks
def harness(px, start):
    """Reproduce known rows and prove the analytic cost model equals the engine's."""
    print("\nHARNESS CHECKS")
    gr, tu = gross_run(px, w_top20("200d"), start)
    real = backtest(px, w_top20("200d")(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
    err = float((at_cost(gr, tu, PROTO_COST) - real).abs().max())
    print(f"  analytic-cost identity vs engine cost_bps=10: max abs daily diff {err:.2e} "
          f"({'OK' if err < 1e-12 else 'MISMATCH'})")
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 2 row (top20, 200d gate, 75% gross, universe.json): {c:.1%}/{s:.3f}/{dd:.1%} "
          f"  [published 12.7%/1.093/-18.3%]")
    gr, tu = gross_run(px, w_ewall("band3"), start)
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 57 KEEP-candidate (ew-all, band3): {c:.1%}/{s:.3f}/{dd:.1%} "
          f"  [published 11.3%/1.136/-15.1%]")
    gr, tu = gross_run(px, w_ewall("none"), start)
    c, s, dd = m(at_cost(gr, tu, PROTO_COST))
    print(f"  idea 57 ungated control (ew-all, none): {c:.1%}/{s:.3f}/{dd:.1%}")


# ---------------------------------------------------------------- main
def main():
    results = []
    px = load_universe()
    harness(px, px.index[260])
    sweep(px, "universe.json", results)
    pxb = load_universe(broad=True)
    sweep(pxb, "universe_broad.json", results)

    # cross-universe summary: an arm only counts if it passes 4b on BOTH lists
    print(f"\n{'=' * 132}\nCROSS-UNIVERSE 4b SUMMARY at {PROTO_COST} bps "
          "(an arm is only a candidate if it passes on BOTH lists)\n" + "=" * 132)
    print(f"  {'book':<8}{'gate':<8}{'universe.json':>28}{'universe_broad.json':>30}   both?")
    df = pd.DataFrame(results)
    for bk in BOOKS:
        for g in GATES:
            a = df[(df.tag == "universe.json") & (df.book == bk) & (df.gate == g)].iloc[0]
            b = df[(df.tag == "universe_broad.json") & (df.book == bk) & (df.gate == g)].iloc[0]
            both = "YES" if a.pass4b and b.pass4b else "no"
            print(f"  {bk:<8}{g:<8}{a.cagr:9.1%}/{a.sharpe:.3f}/{a.dd:7.1%}"
                  f"{b.cagr:11.1%}/{b.sharpe:.3f}/{b.dd:7.1%}   {both}"
                  f"{'  <- IDEA 4 arm' if g in NEW else ''}")
    n_both = sum(1 for bk in BOOKS for g in GATES
                 if df[(df.tag == "universe.json") & (df.book == bk) & (df.gate == g)].iloc[0].pass4b
                 and df[(df.tag == "universe_broad.json") & (df.book == bk) & (df.gate == g)].iloc[0].pass4b)
    print(f"\n  {n_both} of {len(BOOKS) * len(GATES)} arms pass 4b on both universes at "
          f"{PROTO_COST} bps.")
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
