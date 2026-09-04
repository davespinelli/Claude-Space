#!/usr/bin/env python3
"""QUEUE idea 9 — trailing-stop (cloud, 2026-09-04).

Question
--------
Idea 9 as queued: "add a 15% trailing stop overlay to v1".  A trailing stop is the
one risk control the project has never tested that acts BETWEEN rebalances — every
gate tested so far (200d MA, the 3% band, absolute momentum, book-level drawdown
control in idea 40) is evaluated on the rebalance calendar, so a name can lose 30%
inside a week and the book only notices on Friday.  If intra-week path risk is a
real cost, a per-name trailing stop should buy drawdown; if it is not, the stop is
a whipsaw machine and should show up exactly like the 200d gate did in ideas 55/57
— paying CAGR for drawdown at a bad exchange rate, with the damage growing in cost.

The project's priors make this a test rather than a sweep:
  * ideas 55/57/4 found net Sharpe in these books orders by FLIP RATE (slower
    instruments win).  A trailing stop is the FASTEST instrument yet proposed: it
    is checked daily and it fires on a per-name price path, so the prediction is
    that it loses, and loses more at 25 bps than at 10.
  * idea 40 already killed the book-level version of this (drawdown control keeps
    49-62% of CAGR to buy back 23-39% of drawdown).  The per-name version is the
    remaining open form of the same question.
  * idea 66 established gross exposure is an exact lever with zero Sharpe content
    (corr 1.0000, beta=g).  A stop spends time in cash, so the honest control is
    the SAME book de-grossed to the stop arm's average invested fraction — if the
    stop's drawdown gain is no better than simply holding less, there is nothing
    here.  That control is computed for every arm.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names incl. SPY/ETFs);
           full robustness pass on universe_broad.json (136 names).  Both reported.
Books    : three PRE-CHOSEN constructions, none tuned here —
           * `v1`       — rules_v1_weights exactly as live (idea 9's literal subject).
           * `top20`    — idea 2's 4b KEEP: top-20 by the composite without the vol
                          scaler among 200d/vol20-eligible names, 3.75% each.
           * `ew-band3` — idea 57's 4b KEEP-candidate: equal-weight all eligible at
                          75% gross with the 3% MA band replacing the raw 200d gate.
Params   : exactly TWO tuned dimensions —
           * stop depth S in {10, 15, 20, 25, 30}% below the running high since entry
             (15% is the queued value; the others bracket it),
           * cooldown C in {0, 21} trading days before a stopped name may be re-bought.
           Plus the S=none control.  11 arms per book; EVERY cell is printed.
Mechanics: the stop is checked at every close on the trailing high of the position
           since it was opened, and the exit executes at the NEXT close (rule 2, the
           same t+1 convention the engine uses for target weights).  Stopped capital
           goes to CASH — it is not redistributed to the survivors — and the name is
           blocked until it is both eligible again and past its cooldown.
Costs    : 5 / 10 / 25 bps, applied analytically (returns(c) = gross - turnover*c/1e4),
           which is exact because the held path does not depend on cost_bps.  10 bps
           is the PROTOCOL cost and the one verdicts are read at.
Baseline : RULES v1 weekly at each cost (4a) and SPY buy-and-hold (4b).
Rule 8   : (book, S, C) chosen on 2009-2016 only under two selection rules fixed
           BEFORE any OOS number is read; 2017-2026 evaluated untouched.

Harness  : the stop simulator is the same loop as engine.backtest plus the stop
           state; with the stop disabled it must reproduce engine.backtest to
           machine precision, and the published rows of ideas 2 and 57 to the
           decimal.  Both are asserted below before any result is read.

SURVIVORSHIP: both lists are current constituents, so absolute CAGR/Sharpe are
optimistic.  The stop-vs-no-stop comparisons that answer the question are far less
exposed: every pair holds the same names on the same days from the same signal and
differs only in when a position is closed.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
BAND = 0.03
STOPS = [0.10, 0.15, 0.20, 0.25, 0.30]
COOLDOWNS = [0, 21]
COSTS = [5, 10, 25]
PROTO_COST = 10
FREQ = "W"
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SCRIPT = "research/backtests/2026-09-04_trailing-stop_cloud.py"


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


def w_ewband(px):
    e = eligible(px, "band3").astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": rules_v1_weights, "top20": w_top20, "ew-band3": w_ewband}


# ---------------------------------------------------------------- simulator
def run_stop(prices, weights, stop=None, cooldown=0, freq=FREQ):
    """engine.backtest + a per-name trailing stop, at zero cost (costs applied later).

    stop=None reproduces engine.backtest exactly (asserted in harness()).  The stop is
    evaluated at close t on the running high since the position opened and executed at
    close t+1; stopped capital goes to cash and the name is blocked for `cooldown`
    trading days.
    """
    rets = prices.pct_change().fillna(0.0).values
    pxv = prices.values
    n = pxv.shape[1]
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values

    cur = np.zeros(n)
    peak = np.full(n, np.nan)
    blocked_until = np.zeros(n, dtype=int)          # index position the block expires
    pending = np.zeros(n, dtype=bool)               # stop fired at t-1, execute now
    port = np.zeros(len(prices))
    turn = np.zeros(len(prices))
    invested = np.zeros(len(prices))
    n_stops = 0

    for i in range(len(prices)):
        # 1. execute stop exits decided at the previous close (t+1 execution)
        if pending.any():
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        # 2. scheduled rebalance (target decided at t-1 via the shift above)
        if mask[i] or i == 0:
            new = w_target[i].copy()
            if stop is not None and cooldown > 0:
                new = np.where(blocked_until > i, 0.0, new)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held = cur.copy()
        invested[i] = held.sum()
        port[i] = float(np.nansum(held * rets[i]))
        # 3. drift
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
        # 4. update trailing highs and fire stops on the new closes
        if stop is not None:
            alive = cur > 1e-9
            p = pxv[i]
            peak = np.where(alive, np.fmax(np.where(np.isnan(peak), -np.inf, peak), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak * (1 - stop))
            if hit.any():
                pending |= hit
                n_stops += int(hit.sum())
                blocked_until = np.where(hit, i + 1 + cooldown, blocked_until)

    idx = prices.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(invested, index=idx), n_stops)


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def year_ret(r, y):
    s = r[r.index.year == y]
    return float((1 + s).prod() - 1) if len(s) else np.nan


def paired_t(a, b):
    d = (a - b).dropna()
    sd = d.std()
    if not np.isfinite(sd) or sd == 0:          # degenerate arm: the stop never fired
        return 0.0, 0.0
    return float(d.mean() * 252), float(d.mean() / (sd / np.sqrt(len(d))))


def degross_to_dd(gross, turn, target_dd, cost=PROTO_COST):
    """Scale the SAME book by a constant g (idea 66: gross is an exact lever) until its
    MaxDD matches target_dd; return (g, returns).  This is the honest control for any
    drawdown claim — if simply holding less buys the same drawdown, the stop adds nothing.
    """
    lo, hi = 0.0, 1.0
    if m(at_cost(gross, turn, cost))[2] >= target_dd:       # already shallower than target
        return 1.0, at_cost(gross, turn, cost)
    for _ in range(60):
        g = (lo + hi) / 2
        if m(at_cost(g * gross, g * turn, cost))[2] < target_dd:
            hi = g
        else:
            lo = g
    g = (lo + hi) / 2
    return g, at_cost(g * gross, g * turn, cost)


def at_cost(gross, turn, bps):
    return gross - turn * bps / 1e4


def turn_per_yr(turn):
    return turn.sum() / (len(turn) / 252)


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


ARMS = [(None, 0)] + [(s, c) for s in STOPS for c in COOLDOWNS]


def arm_name(s, c):
    return "none" if s is None else f"S{int(s * 100)}/C{c}"


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

    print(f"\n{'=' * 140}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 140)

    G = {}
    for bk, fn in BOOKS.items():
        w = fn(px)
        for (s, c) in ARMS:
            gr, tu, inv, ns = run_stop(px, w, stop=s, cooldown=c)
            G[(bk, s, c)] = (gr.loc[start:], tu.loc[start:], inv.loc[start:], ns)

    b_gross, b_turn, _, _ = G[("v1", None, 0)]
    b10 = at_cost(b_gross, b_turn, PROTO_COST)
    bc, bs, bdd = m(b10)
    bh1, bh2 = halves(b10)
    print(f"RULES v1 baseline (weekly, no stop) @{PROTO_COST}bps: {bc:.1%}/{bs:.3f}/{bdd:.1%} "
          f"halves {bh1:.3f}/{bh2:.3f} OOS Sharpe {m(b10.loc[OOS_START:])[1]:.3f} "
          f"(4a bars: H1>{bh1:.3f}, H2>{bh2:.3f}, MaxDD>={bdd:.1%})")

    # ---- stop mechanics
    print("\nSTOP MECHANICS — how often the overlay actually fires, and what it costs to run:")
    print(f"  {'book':<10}{'arm':<10}{'stops/yr':>10}{'per name/yr':>13}{'turn':>8}"
          f"{'avg invested':>14}{'days<50% inv':>14}")
    yrs_n = len(px.loc[start:]) / 252
    for bk in BOOKS:
        for (s, c) in ARMS:
            gr, tu, inv, ns = G[(bk, s, c)]
            base_inv = G[(bk, None, 0)][2].mean()
            print(f"  {bk:<10}{arm_name(s, c):<10}{ns / yrs_n:10.1f}"
                  f"{ns / yrs_n / px.shape[1]:13.2f}{turn_per_yr(tu):7.1f}x"
                  f"{inv.mean():13.1%}{(inv < 0.5 * base_inv).mean():14.1%}")
        print()

    # ---- main grid
    print(f"{'book':<10}{'arm':<10}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'2020':>8}"
          f"{'2022':>8}{'turn':>7}   {'H1':>5}/{'H2':>5}{'OOS':>7}   verdict")
    print("-" * 140)
    RET = {}
    for bk in BOOKS:
        for (s, c) in ARMS:
            gr, tu, inv, ns = G[(bk, s, c)]
            for cost in COSTS:
                r = at_cost(gr, tu, cost)
                RET[(bk, s, c, cost)] = r
                base = at_cost(b_gross, b_turn, cost)
                cg, sh, dd = m(r)
                h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                v = verdict(r, base, spy, oos, ss_o)
                mark = " <-" if cost == PROTO_COST else ""
                print(f"{bk:<10}{arm_name(s, c):<10}{cost:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}"
                      f"{year_ret(r, 2020):8.1%}{year_ret(r, 2022):8.1%}{turn_per_yr(tu):6.1f}x   "
                      f"{h1:5.3f}/{h2:5.3f}{oos:7.3f}   {v}{mark}")
                if cost == PROTO_COST:
                    results.append(dict(tag=tag, book=bk, arm=arm_name(s, c), stop=s, cool=c,
                                        cagr=cg, sharpe=sh, dd=dd, h1=h1, h2=h2, oos=oos,
                                        turn=turn_per_yr(tu), verdict=v,
                                        pass4b=not fail4b(r, spy, oos, ss_o),
                                        pass4a=not fail4a(r, at_cost(b_gross, b_turn, PROTO_COST))))
        print("-" * 140)

    # ---- idea 9's own test: stop minus no-stop, same book, same days
    print("IDEA 9's TEST — each stop arm minus the SAME book with no stop, same signal, "
          "same days (paired daily differences):")
    print(f"  {'book':<10}{'arm':<10}{'bps':>5}{'dCAGR':>8}{'dSharpe':>9}{'dMaxDD(pp)':>12}"
          f"{'pp CAGR per pp DD':>19}{'ann.diff':>10}{'t':>7}")
    for bk in BOOKS:
        for (s, c) in ARMS:
            if s is None:
                continue
            for cost in (PROTO_COST, 25):
                r, r0 = RET[(bk, s, c, cost)], RET[(bk, None, 0, cost)]
                cg, sh, dd = m(r)
                cg0, sh0, dd0 = m(r0)
                ann, t = paired_t(r, r0)
                ddgain = (dd - dd0) * 100
                rate = (cg0 - cg) * 100 / ddgain if ddgain > 1e-9 else np.nan
                print(f"  {bk:<10}{arm_name(s, c):<10}{cost:5d}{(cg - cg0) * 100:+8.2f}"
                      f"{sh - sh0:+9.3f}{ddgain:+12.2f}{rate:19.2f}{ann * 100:+10.2f}{t:+7.2f}")
        print()

    # ---- the gross control (idea 66): is the stop better than simply holding less?
    print("GROSS CONTROL (idea 66: gross is an exact lever) — each stop arm vs the SAME book")
    print("de-grossed to the stop arm's average invested fraction, at 10 bps:")
    print(f"  {'book':<10}{'arm':<10}{'g':>7}{'stop CAGR':>11}{'ctrl CAGR':>11}"
          f"{'stop Sh':>9}{'ctrl Sh':>9}{'dSharpe':>9}{'stop DD':>9}{'ctrl DD':>9}{'dDD(pp)':>9}")
    for bk in BOOKS:
        gr0, tu0, inv0, _ = G[(bk, None, 0)]
        for (s, c) in ARMS:
            if s is None:
                continue
            gr, tu, inv, _ = G[(bk, s, c)]
            g = inv.mean() / inv0.mean()
            ctrl = at_cost(g * gr0, g * tu0, PROTO_COST)
            r = RET[(bk, s, c, PROTO_COST)]
            cg, sh, dd = m(r)
            cc, cs, cdd = m(ctrl)
            print(f"  {bk:<10}{arm_name(s, c):<10}{g:7.3f}{cg:11.1%}{cc:11.1%}"
                  f"{sh:9.3f}{cs:9.3f}{sh - cs:+9.3f}{dd:9.1%}{cdd:9.1%}{(dd - cdd) * 100:+9.2f}")
        print()

    # ---- the decisive control for path 4a: matched MaxDD, not matched investment
    print("MATCHED-DRAWDOWN CONTROL — the no-stop book de-grossed until its MaxDD EQUALS the")
    print("stop arm's, at 10 bps.  4a is a drawdown-constrained test, so this is the control that")
    print("decides whether the stop earns its 4a pass or whether holding less would do it cheaper:")
    print(f"  {'book':<10}{'arm':<10}{'MaxDD':>9}{'g needed':>10}{'stop CAGR':>11}{'ctrl CAGR':>11}"
          f"{'dCAGR(pp)':>11}{'stop Sh':>9}{'ctrl Sh':>9}{'dSharpe':>9}   stop better?")
    for bk in BOOKS:
        gr0, tu0, _, _ = G[(bk, None, 0)]
        for (s, c) in ARMS:
            if s is None:
                continue
            r = RET[(bk, s, c, PROTO_COST)]
            cg, sh, dd = m(r)
            if abs(dd - m(RET[(bk, None, 0, PROTO_COST)])[2]) < 1e-6:
                continue                                    # stop never bit; nothing to match
            g, ctrl = degross_to_dd(gr0, tu0, dd)
            cc, cs, cdd = m(ctrl)
            better = "yes" if (sh > cs and cg > cc) else ("no" if (sh < cs and cg < cc) else "mixed")
            print(f"  {bk:<10}{arm_name(s, c):<10}{dd:9.1%}{g:10.3f}{cg:11.1%}{cc:11.1%}"
                  f"{(cg - cc) * 100:+11.2f}{sh:9.3f}{cs:9.3f}{sh - cs:+9.3f}   {better}")
        print()

    # ---- 4b margins
    print("MARGINS on each 4b bar at 10 bps (positive = clears; binding bar named):")
    print(f"  {'book':<10}{'arm':<10}{'H1-bar':>9}{'H2-bar':>9}{'OOS-bar':>9}"
          f"{'DD-slack(pp)':>14}{'CAGR-slack(pp)':>16}   binding")
    for bk in BOOKS:
        for (s, c) in ARMS:
            r = RET[(bk, s, c, PROTO_COST)]
            cg, sh, dd = m(r)
            h1, h2 = halves(r)
            oos = m(r.loc[OOS_START:])[1]
            mg = {"H1": h1 - s1, "H2": h2 - s2, "OOS": oos - ss_o,
                  "DD": (dd - 0.60 * sdd) * 100, "CAGR": (cg - 0.70 * sc) * 100}
            binding = min(mg, key=mg.get)
            print(f"  {bk:<10}{arm_name(s, c):<10}{mg['H1']:+9.4f}{mg['H2']:+9.4f}{mg['OOS']:+9.4f}"
                  f"{mg['DD']:+14.2f}{mg['CAGR']:+16.2f}   {binding} ({mg[binding]:+.4f})")

    # ---- rule 8 walk-forward
    print(f"\nRule 8 walk-forward — (book, stop, cooldown) chosen on IS 2009-2016 only, "
          f"evaluated untouched on {OOS_START}-2026, at {PROTO_COST} bps.")
    is_spy, oos_spy = spy.loc[:IS_END], spy.loc[OOS_START:]
    isc, iss, isdd = m(is_spy)
    oc_s, osh_s, odd_s = m(oos_spy)
    print(f"  IS SPY {isc:.1%}/{iss:.3f}/{isdd:.1%}   4b-aware IS bars: "
          f"MaxDD>={0.60 * isdd:.1%}, CAGR>={0.70 * isc:.1%}")
    print(f"  {'book':<10}{'arm':<10}{'IS CAGR':>9}{'IS Sh':>8}{'IS DD':>8}   "
          f"{'OOS CAGR':>9}{'OOS Sh':>8}{'OOS DD':>8}")
    cand = []
    for bk in BOOKS:
        for (s, c) in ARMS:
            r = RET[(bk, s, c, PROTO_COST)]
            ic, ish, idd = m(r.loc[:IS_END])
            oc, osh, odd = m(r.loc[OOS_START:])
            cand.append((bk, arm_name(s, c), ic, ish, idd, oc, osh, odd))
            print(f"  {bk:<10}{arm_name(s, c):<10}{ic:9.1%}{ish:8.3f}{idd:8.1%}   "
                  f"{oc:9.1%}{osh:8.3f}{odd:8.1%}")
    print(f"  {'SPY':<20}{isc:9.1%}{iss:8.3f}{isdd:8.1%}   {oc_s:9.1%}{osh_s:8.3f}{odd_s:8.1%}")

    def clears(c):
        return c[6] > osh_s and c[7] >= 0.60 * odd_s and c[5] >= 0.70 * oc_s

    r1 = max(cand, key=lambda x: x[3])
    ok = [c for c in cand if c[4] >= 0.60 * isdd and c[2] >= 0.70 * isc]
    r2 = max(ok, key=lambda x: x[3]) if ok else None
    print(f"  RULE A (max IS Sharpe)      -> {r1[0]}/{r1[1]}: OOS {r1[5]:.1%}/{r1[6]:.3f}/{r1[7]:.1%} "
          f"vs SPY {oc_s:.1%}/{osh_s:.3f}/{odd_s:.1%} "
          f"[{'clears' if clears(r1) else 'FAILS'} OOS 4b bars]")
    if r2:
        print(f"  RULE B (4b-aware IS filter) -> {r2[0]}/{r2[1]}: OOS {r2[5]:.1%}/{r2[6]:.3f}/{r2[7]:.1%} "
              f"[{'clears' if clears(r2) else 'FAILS'} OOS 4b bars]")
    else:
        print("  RULE B (4b-aware IS filter) -> NOTHING selected (no IS point met the bars)")

    print("\n  Stop chosen per book on IS Sharpe -> did it win OOS?")
    for bk in BOOKS:
        rows = [c for c in cand if c[0] == bk]
        pick = max(rows, key=lambda x: x[3])
        best_oos = max(rows, key=lambda x: x[6])
        print(f"    {bk:<10} IS picks {pick[1]:<8} (OOS Sh {pick[6]:.3f}); best OOS was "
              f"{best_oos[1]:<8} ({best_oos[6]:.3f}) -> "
              f"{'agrees' if pick[1] == best_oos[1] else 'DISAGREES'}")

    # ---- monotonicity in stop depth: is there a signal, or is it noise?
    print("\n  Net Sharpe by stop depth at 10 bps (is deeper better? monotone = a real dial):")
    print(f"    {'book':<10}{'cool':>6}" + "".join(f"{('S' + str(int(s * 100))):>9}" for s in STOPS)
          + f"{'none':>9}")
    for bk in BOOKS:
        for c in COOLDOWNS:
            cells = "".join(f"{m(RET[(bk, s, c, PROTO_COST)])[1]:9.3f}" for s in STOPS)
            print(f"    {bk:<10}{c:6d}{cells}{m(RET[(bk, None, 0, PROTO_COST)])[1]:9.3f}")

    return RET


# ---------------------------------------------------------------- harness checks
def harness(px, start):
    print("HARNESS CHECKS")
    ok = True
    for bk, fn in BOOKS.items():
        w = fn(px)
        gr, tu, inv, ns = run_stop(px, w, stop=None)
        eng = backtest(px, w, cost_bps=0.0, freq=FREQ)
        e1 = float((gr - eng["returns"]).abs().max())
        e2 = float((tu - eng["turnover"]).abs().max())
        ok &= e1 < 1e-12 and e2 < 1e-12 and ns == 0
        print(f"  stop=None simulator vs engine.backtest [{bk}]: max |dret| {e1:.2e}, "
              f"max |dturn| {e2:.2e}, stops fired {ns} "
              f"({'OK' if e1 < 1e-12 and e2 < 1e-12 else 'MISMATCH'})")
    gr, tu, _, _ = run_stop(px, w_top20(px), stop=None)
    real = backtest(px, w_top20(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
    err = float((at_cost(gr.loc[start:], tu.loc[start:], PROTO_COST) - real).abs().max())
    print(f"  analytic-cost identity vs engine cost_bps=10: max abs daily diff {err:.2e} "
          f"({'OK' if err < 1e-12 else 'MISMATCH'})")
    c, s, dd = m(at_cost(gr.loc[start:], tu.loc[start:], PROTO_COST))
    print(f"  idea 2 KEEP row (top20, weekly): {c:.1%}/{s:.3f}/{dd:.1%}   "
          f"[published 12.7%/1.093/-18.3%]")
    gr, tu, _, _ = run_stop(px, w_ewband(px), stop=None)
    c, s, dd = m(at_cost(gr.loc[start:], tu.loc[start:], PROTO_COST))
    print(f"  idea 57 KEEP-candidate (ew-band3, weekly): {c:.1%}/{s:.3f}/{dd:.1%}   "
          f"[published 11.3%/1.136/-15.1%]")

    # The v1 firing rates below are so low they look like a bug, so they are audited against
    # an independent count that never touches the simulator: walk each contiguous holding
    # episode of the UNSTOPPED book and ask whether the price ever closed 10% below its
    # running high inside that episode.  This is a lower bound on the simulator's count
    # (the simulator re-enters stopped names, creating extra episodes with fresh highs).
    print("  episode audit (independent of the simulator; lower bound on stops/yr at S=10%):")
    yrs_n = len(px) / 252
    vol = (px.pct_change().rolling(20).std() * np.sqrt(252)).values
    for bk, fn in BOOKS.items():
        H = (backtest(px, fn(px), cost_bps=0.0, freq=FREQ)["weights"] > 1e-9).values
        P = px.values
        n_ep = n_hit = 0
        eplen = []
        for j in range(H.shape[1]):
            i = 0
            while i < len(H):
                if not H[i, j]:
                    i += 1
                    continue
                k, pk, hit = i, -np.inf, False
                while k < len(H) and H[k, j]:
                    pk = max(pk, P[k, j])
                    hit = hit or (np.isfinite(P[k, j]) and P[k, j] < pk * 0.90)
                    k += 1
                n_ep += 1
                n_hit += hit
                eplen.append(k - i)
                i = k
        hv = np.nanmean(vol[H]) if H.any() else np.nan
        print(f"    {bk:<10} episodes/yr {n_ep / yrs_n:6.1f}  first-hit/yr {n_hit / yrs_n:6.1f}  "
              f"hit rate {n_hit / max(n_ep, 1):6.1%}  mean episode {np.mean(eplen):5.1f}d  "
              f"mean vol20 of held names {hv:.3f}")
    if not ok:
        sys.exit("!! harness mismatch — aborting")


# ---------------------------------------------------------------- main
def main():
    results = []
    px = load_universe()
    harness(px, px.index[260])
    sweep(px, "universe.json", results)
    pxb = load_universe(broad=True)
    sweep(pxb, "universe_broad.json", results)

    print(f"\n{'=' * 140}\nCROSS-UNIVERSE 4b SUMMARY at {PROTO_COST} bps "
          "(an arm only counts if it passes on BOTH lists)\n" + "=" * 140)
    print(f"  {'book':<10}{'arm':<10}{'universe.json':>28}{'universe_broad.json':>30}   both?")
    df = pd.DataFrame(results)
    n_both = 0
    for bk in BOOKS:
        for (s, c) in ARMS:
            a = df[(df.tag == "universe.json") & (df.book == bk) & (df.arm == arm_name(s, c))].iloc[0]
            b = df[(df.tag == "universe_broad.json") & (df.book == bk)
                   & (df.arm == arm_name(s, c))].iloc[0]
            both = "YES" if a.pass4b and b.pass4b else "no"
            n_both += both == "YES"
            print(f"  {bk:<10}{arm_name(s, c):<10}{a.cagr:9.1%}/{a.sharpe:.3f}/{a.dd:7.1%}"
                  f"{b.cagr:11.1%}/{b.sharpe:.3f}/{b.dd:7.1%}   {both}")
    n_stop_arms = len(BOOKS) * (len(ARMS) - 1)
    print(f"\n  {n_both} of {len(BOOKS) * len(ARMS)} arms pass 4b on both universes at "
          f"{PROTO_COST} bps ({n_stop_arms} of them carry a stop).")
    print(f"  4a passes (universe.json): "
          f"{[f'{r.book}/{r.arm}' for _, r in df[(df.tag == 'universe.json') & df.pass4a].iterrows()]}")
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
