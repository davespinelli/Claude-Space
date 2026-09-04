#!/usr/bin/env python3
"""QUEUE idea 57 — trend-gate-as-drawdown-insurance (lane B, 2026-09-04).

Question
--------
Idea 55 established that the 200d-MA gate's *return* contribution on the two large-cap
lists is statistically indistinguishable from zero (+0.35..+1.47%/yr, t +1.42..+1.76 on
universe.json; -0.22..+0.19%/yr, t -0.50..+0.68 on the broad list), while the gate-only
control (equal-weight all eligible, no ranking) showed it reliably buying 2.5-3.1pp of
drawdown for 6.4x/yr of extra turnover.  That framing makes the gate an insurance
contract, not an alpha source.  This run prices the contract:

  (a) At 5 / 10 / 25 / 50 bps, does the drawdown reduction still pay?
  (b) Is a *cheaper instrument* — a monthly-re-evaluated gate, or a 3%/5% re-entry band
      (hysteresis, as in idea 52) — the same insurance at a fraction of the turnover?

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names, incl. SPY and ETFs).
           Robustness pass on universe_broad.json (136 names).
Books    : BOTH books the question lives in, run identically —
           * `top20` — idea 2/55's KEEP-candidate construction: top-20 by the composite
             (mean pct-rank of 12-1, 6m, 3m, NO /sqrt(vol20)) among eligible names, equal
             weight 0.75/20 = 3.75% each, cash if fewer than 20 qualify.  n=20 is
             pre-chosen from idea 2 and is NOT tuned here.
           * `ew-all` — equal-weight EVERY eligible name at 75% gross, no ranking.  This
             is the gate-only control where idea 55 actually measured the insurance; it
             isolates the gate from the momentum ranking.
Gate     : eligible = (vol20 < 0.60) & G, with the vol20 half held FIXED at v1's value.
           G in five arms:
             none    — no trend gate at all (the uninsured book)
             200d    — px > 200d MA, re-evaluated at every rebalance (the incumbent)
             200d-M  — px > 200d MA, re-evaluated on month-ends only and held constant
             band3   — hysteresis: enter when px > 1.03*MA200, exit when px < 0.97*MA200
             band5   — hysteresis at +/-5%
Params   : exactly 2 tuned — the instrument family (continuous / monthly / band) and the
           band width (3% or 5%).  All arms reported at all four cost levels.
Costs    : 5, 10, 25, 50 bps per unit turnover.  10 bps is the PROTOCOL cost and is the
           one the KEEP/KILL verdicts are read at; the others are the sensitivity the
           idea asks for.  Costs are applied analytically —
           `returns(c) = gross_returns - turnover * c / 1e4` — which is exactly what
           engine.backtest does, since `held` and `turnover` do not depend on cost_bps.
           A harness check below confirms the identity against a real cost_bps=10 run.
Execution: weekly rebalance, weights decided at close t applied at t+1, long-only, no
           leverage.
Rule 8   : instrument chosen on 2009-2016 only, evaluated untouched on 2017-2026, with
           two selection rules fixed BEFORE any OOS number is read.

Drawdown is measured with more than MaxDD, because MaxDD is a single episode and an
insurance claim resting on one number is not a claim: Ulcer index, the mean of the five
deepest drawdowns, the 2020 and 2022 within-year drawdowns, and the worst 20-day return
are all reported.

SURVIVORSHIP: both lists are current constituents, so absolute CAGR/Sharpe are
optimistic.  The gate-vs-gate comparisons that answer the question are far less exposed —
every arm draws from the same names on the same days.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
COSTS = [5, 10, 25, 50]
PROTO_COST = 10
GATES = ["none", "200d", "200d-M", "band3", "band5"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SCRIPT = "research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py"


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
    """The trend half of the eligibility filter, as a boolean frame. None -> all True."""
    if gate == "none":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "200d":
        return px > ma
    if gate == "200d-M":
        g = (px > ma).astype(float)
        me = rebalance_mask(px.index, "M")                 # last trading day of each month
        keep = pd.DataFrame(np.repeat(me.values[:, None], px.shape[1], axis=1),
                            index=px.index, columns=px.columns)
        return g.where(keep, other=np.nan).ffill().fillna(0.0) > 0.5
    if gate.startswith("band"):
        b = int(gate[4:]) / 100.0
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + b), 1.0)             # cross up through the upper band -> in
        raw = raw.mask(px < ma * (1 - b), 0.0)             # cross down through the lower -> out
        return raw.ffill().fillna(0.0) > 0.5               # sticky in between; out before warm-up
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


def ulcer(r):
    return float(np.sqrt((dd_series(r) ** 2).mean()))


def top5_dd(r):
    """Mean depth of the five deepest *distinct* drawdown episodes (peak-to-trough)."""
    d = dd_series(r)
    eq = (1 + r).cumprod()
    peak = eq.cummax()
    grp = (peak != peak.shift()).cumsum()               # a new id each time a new high is set
    depths = d.groupby(grp).min().sort_values()
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


def verdict(r, base, spy, oos_sh, spy_oos_sh):
    a, b = fail4a(r, base), fail4b(r, spy, oos_sh, spy_oos_sh)
    return ("KEEP 4a" if not a else "KILL 4a") + " / " + \
           ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")


# ---------------------------------------------------------------- run helpers
def gross_run(px, fn, start):
    """One cost-free backtest; costs are applied afterwards. Returns (gross, turnover)."""
    res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def at_cost(gross, turn, bps):
    return gross - turn * bps / 1e4


def turn_per_yr(turn):
    return turn.sum() / (len(turn) / 252)


# ---------------------------------------------------------------- one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    _, ss_o, _ = m(spy.loc[OOS_START:])

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    print(f"\n{'=' * 128}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}   "
          f"Ulcer {ulcer(spy):.3f} top5DD {top5_dd(spy):.1%} 2020DD {year_dd(spy, 2020):.1%} "
          f"2022DD {year_dd(spy, 2022):.1%}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 128)

    # cost-free runs, one per (book, gate); baselines too
    G = {}
    for bk, mk in BOOKS.items():
        for g in GATES:
            G[(bk, g)] = gross_run(px, mk(g), start)
    b_gross, b_turn = gross_run(px, rules_v1_weights, start)

    # exposure / gate mechanics
    print("\nGate mechanics — names passing the trend half per day, and book exposure "
          f"(of {px.shape[1]} tickers):")
    print(f"  {'gate':<8}{'mean':>7}{'median':>8}{'min':>6}   {'ew-all gross':>13}"
          f"{'days<20 elig':>14}{'top20 turn':>12}{'ew-all turn':>13}")
    for g in GATES:
        t = trend(px, g).loc[start:]
        e = eligible(px, g).loc[start:].sum(axis=1)
        ewg = backtest(px, BOOKS["ew-all"](g)(px), cost_bps=0.0, freq=FREQ)["weights"].loc[start:].sum(axis=1)
        print(f"  {g:<8}{t.sum(axis=1).mean():7.1f}{t.sum(axis=1).median():8.0f}"
              f"{t.sum(axis=1).min():6.0f}   {ewg.mean():12.1%}{(e < NPOS).mean():13.1%}"
              f"{turn_per_yr(G[('top20', g)][1]):11.1f}x{turn_per_yr(G[('ew-all', g)][1]):12.1f}x")

    # ---- main grid: every book x gate x cost
    print(f"\n{'book':<8}{'gate':<8}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'Ulcer':>7}"
          f"{'top5DD':>8}{'2020':>7}{'2022':>7}{'w20d':>8}   {'H1':>5}/{'H2':>5}{'OOS':>7}   verdict")
    print("-" * 128)
    rows, RET = [], {}
    for bk in BOOKS:
        for g in GATES:
            gr, tu = G[(bk, g)]
            for c in COSTS:
                r = at_cost(gr, tu, c)
                RET[(bk, g, c)] = r
                base = at_cost(b_gross, b_turn, c)
                cg, sh, dd = m(r); h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                v = verdict(r, base, spy, oos, ss_o)
                mark = " <-" if c == PROTO_COST else ""
                print(f"{bk:<8}{g:<8}{c:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}{ulcer(r):7.3f}"
                      f"{top5_dd(r):8.1%}{year_dd(r, 2020):7.1%}{year_dd(r, 2022):7.1%}"
                      f"{worst20(r):8.1%}   {h1:5.3f}/{h2:5.3f}{oos:7.3f}   {v}{mark}")
                if c == PROTO_COST:
                    rows.append((f"57 {tag} {bk} gate={g} @{c}bps", cg, sh, dd, h1, h2, oos,
                                 turn_per_yr(tu), v))
        print("-" * 128)

    # ---- the question: what does the insurance cost, and does it pay?
    print("\nINSURANCE PRICING — each gate arm minus the uninsured (gate=none) arm, same book, "
          "same days:")
    print(f"  {'book':<8}{'gate':<8}{'bps':>5}{'dCAGR':>8}{'dSharpe':>9}{'dMaxDD':>8}"
          f"{'dUlcer':>8}{'dTop5':>8}{'dTurn':>8}{'pp CAGR / pp DD':>18}   pays?")
    price = {}
    for bk in BOOKS:
        for g in GATES[1:]:
            for c in COSTS:
                r, r0 = RET[(bk, g, c)], RET[(bk, "none", c)]
                cg, sh, dd = m(r); cg0, sh0, dd0 = m(r0)
                dcagr, dsh, ddd = cg - cg0, sh - sh0, dd - dd0
                dturn = turn_per_yr(G[(bk, g)][1]) - turn_per_yr(G[(bk, "none")][1])
                px_ = (-dcagr * 100) / (ddd * 100) if ddd > 1e-9 else np.nan
                price[(bk, g, c)] = (dcagr, dsh, ddd, px_)
                pays = "yes" if dsh > 0 else "no"
                print(f"  {bk:<8}{g:<8}{c:5d}{dcagr * 100:+8.2f}{dsh:+9.3f}{ddd * 100:+8.2f}"
                      f"{ulcer(r) - ulcer(r0):+8.3f}{(top5_dd(r) - top5_dd(r0)) * 100:+8.2f}"
                      f"{dturn:+7.1f}x{px_ if np.isfinite(px_) else float('nan'):18.2f}   {pays}")
        print()

    # break-even cost: where does the arm's arithmetic return advantage over `none` vanish?
    print("Break-even cost — the bps at which each gate arm's mean return equals the "
          "uninsured arm's.\n  A gate that is behind on gross return but CHEAPER to run "
          "(negative turnover delta) catches up ABOVE its\n  break-even; one that is ahead "
          "on gross but dearer stays ahead BELOW it. Read the direction column:")
    for bk in BOOKS:
        for g in GATES[1:]:
            gr, tu = G[(bk, g)]
            gr0, tu0 = G[(bk, "none")]
            dgross = (gr - gr0).mean() * 252
            dturn = turn_per_yr(tu) - turn_per_yr(tu0)
            be = 1e4 * dgross / dturn if abs(dturn) > 1e-9 else np.nan
            if not np.isfinite(be) or not (0 <= be <= 200):
                where = "never inside 0-200 bps (gate " + \
                        ("ahead" if dgross > 0 and dturn <= 0 else "behind") + " at every cost)"
            else:
                where = ("gate ahead ABOVE" if dgross < 0 else "gate ahead BELOW") + \
                        f" {be:.0f} bps"
            print(f"  {bk:<8}{g:<8} gross edge {dgross * 100:+6.2f}%/yr, turnover "
                  f"{dturn:+5.1f}x/yr -> {where}")
    print()

    # how often does each instrument toggle?  the mechanism behind the turnover column.
    print("Gate churn — mean trend-state flips per ticker per year (the turnover mechanism):")
    for g in GATES[1:]:
        t = trend(px, g).loc[start:].astype(float)
        flips = (t.diff().abs() > 0).sum().sum() / (len(t) / 252) / px.shape[1]
        print(f"  {g:<8}{flips:5.2f} flips/ticker/yr")
    print()

    # paired significance of each instrument vs the uninsured arm, at the protocol cost
    print(f"Paired significance vs gate=none at {PROTO_COST} bps (daily difference, same days):")
    for bk in BOOKS:
        for g in GATES[1:]:
            d = (RET[(bk, g, PROTO_COST)] - RET[(bk, "none", PROTO_COST)]).dropna()
            t = d.mean() / d.std() * np.sqrt(len(d))
            print(f"  {bk:<8}{g:<8}{d.mean() * 25200:+7.2f}%/yr  t {t:+5.2f}")

    return dict(G=G, RET=RET, spy=spy, ss_o=ss_o, b_gross=b_gross, b_turn=b_turn,
                start=start, rows=rows, price=price)


def pass4b_set(res, cost):
    """Arms clearing all five 4b tests at a given cost, as a set of (book, gate) keys."""
    spy, ss_o = res["spy"], res["ss_o"]
    out = set()
    for bk in BOOKS:
        for g in GATES:
            r = res["RET"][(bk, g, cost)]
            if not fail4b(r, spy, m(r.loc[OOS_START:])[1], ss_o):
                out.add((bk, g))
    return out


def cross_universe(main_res, broad_res):
    """Which arms clear 4b on BOTH large-cap lists — the test ideas 2 and 55 both failed."""
    print(f"\n{'=' * 128}")
    print("CROSS-UNIVERSE 4b — arms clearing all five 4b tests on universe.json AND "
          "universe_broad.json.\nIdea 2's n=20 and idea 55's K=none candidate both fail this; "
          "it is the project's standing fragility.")
    print("=" * 128)
    for c in COSTS:
        a, b = pass4b_set(main_res, c), pass4b_set(broad_res, c)
        both = sorted(a & b)
        print(f"\n  @{c:>2} bps: universe.json passes {len(a)}/10, broad passes {len(b)}/10, "
              f"BOTH: {', '.join(f'{x[0]}/{x[1]}' for x in both) if both else 'NONE'}")
        for key in both:
            for tag, res in (("universe.json", main_res), ("broad", broad_res)):
                r = res["RET"][(key[0], key[1], c)]
                cg, sh, dd = m(r); h1, h2 = halves(r)
                ro = r.loc[OOS_START:]
                co, so, ddo = m(ro)
                print(f"      {key[0]:<7}{key[1]:<7}{tag:<14} full {cg:5.1%}/{sh:.3f}/{dd:6.1%}"
                      f"  halves {h1:.3f}/{h2:.3f}  OOS {co:5.1%}/{so:.3f}/{ddo:6.1%}"
                      f"  turn {turn_per_yr(res['G'][key][1]):.1f}x")


def walk_forward(res, tag):
    """PROTOCOL rule 8: choose the instrument on 2009-2016, evaluate untouched 2017-2026.

    Selection is over the 10 arms (2 books x 5 gates) at the protocol cost, fixed before
    any OOS number is read.  Two pre-registered rules: plain in-sample Sharpe, and the
    4b-aware rule (in-sample Sharpe/MaxDD/CAGR all clearing SPY's in-sample 4b bars).
    """
    RET, spy = res["RET"], res["spy"]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc_i, ss_i, sdd_i = m(spy_is)
    sc_o, ss_o, sdd_o = m(spy_oos)
    base_o = m(at_cost(res["b_gross"], res["b_turn"], PROTO_COST).loc[OOS_START:])
    print(f"\nWalk-forward ({tag}): IS <= {IS_END}, OOS >= {OOS_START}, {PROTO_COST} bps")
    print(f"  IS 4b bars: Sharpe>{ss_i:.3f}  MaxDD>={0.60 * sdd_i:.1%}  CAGR>={0.70 * sc_i:.1%}")
    cand = []
    for bk in BOOKS:
        for g in GATES:
            c, s_, dd = m(RET[(bk, g, PROTO_COST)].loc[:IS_END])
            cand.append(dict(key=(bk, g), sh=s_, cagr=c, dd=dd))
    for c in sorted(cand, key=lambda x: -x["sh"]):
        print(f"  IS  {c['key'][0]:<8}{c['key'][1]:<8} Sharpe {c['sh']:6.3f}  CAGR {c['cagr']:6.1%}"
              f"  MaxDD {c['dd']:6.1%}")
    picks = {"plain-Sharpe": max(cand, key=lambda x: x["sh"])["key"]}
    ok = [c for c in cand if c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i and c["cagr"] >= 0.70 * sc_i]
    picks["4b-aware"] = max(ok, key=lambda x: x["sh"])["key"] if ok else None
    print(f"  OOS SPY {sc_o:.1%}/{ss_o:.3f}/{sdd_o:.1%}  |  RULES v1 "
          f"{base_o[0]:.1%}/{base_o[1]:.3f}/{base_o[2]:.1%}")
    out = []
    for rule, key in picks.items():
        if key is None:
            print(f"  OOS pick[{rule}]: NOTHING — no in-sample arm met the 4b bars")
            out.append((f"57 {tag} walk-forward {rule}: picks NOTHING", None))
            continue
        r = RET[(key[0], key[1], PROTO_COST)].loc[OOS_START:]
        c, s_, dd = m(r)
        flag = "beats SPY OOS" if s_ > ss_o else "loses to SPY OOS"
        pass4b = "clears" if (s_ > ss_o and dd >= 0.60 * sdd_o and c >= 0.70 * sc_o) else "misses"
        print(f"  OOS pick[{rule}] = {key[0]} gate={key[1]}: {c:.1%}/{s_:.3f}/{dd:.1%}  "
              f"({flag}; {pass4b} the OOS 4b bars)")
        out.append((f"57 {tag} walk-forward {rule}: {key[0]} gate={key[1]} OOS",
                    (c, s_, dd, flag)))
    return out


# ---------------------------------------------------------------- main
def main():
    print("=" * 128)
    print(f"Idea 57 trend-gate-as-drawdown-insurance (lane B) | {SCRIPT}")
    print("Grid: 2 books x 5 gate instruments x 4 cost levels = 40 points per universe, "
          "all reported. 2 tuned params (instrument family, band width); n=20 pre-chosen.")
    print("=" * 128)

    px = load_universe()
    start = px.index[260]

    # ---- harness sanity 1: the analytic cost identity must equal a real cost_bps=10 run
    gr, tu = gross_run(px, w_top20("200d"), start)
    direct = backtest(px, w_top20("200d")(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
    err = float((at_cost(gr, tu, PROTO_COST) - direct).abs().max())
    print(f"\nHARNESS CHECK 1  analytic cost vs engine cost_bps=10: max abs diff {err:.2e} "
          f"({'PASS' if err < 1e-12 else '*** MISMATCH ***'})")

    # ---- harness sanity 2: top20/200d @10bps must reproduce idea 2's KEEP row
    r0 = at_cost(gr, tu, PROTO_COST)
    c, s_, dd = m(r0); h1, h2 = halves(r0)
    print(f"HARNESS CHECK 2  top20 gate=200d @10bps -> {c:.1%}/{s_:.3f}/{dd:.1%} "
          f"halves {h1:.3f}/{h2:.3f}   (idea 2's KEEP row: 12.7%/1.093/-18.3%, "
          f"halves 1.088/1.103)")
    ok = abs(c - 0.127) < 0.002 and abs(s_ - 1.093) < 0.01 and abs(dd + 0.183) < 0.005
    print(f"HARNESS CHECK 2  {'PASS' if ok else '*** MISMATCH ***'}")

    # ---- harness sanity 3: top20/none @10bps must reproduce idea 55's candidate row
    grn, tun = gross_run(px, w_top20("none"), start)
    rn = at_cost(grn, tun, PROTO_COST)
    c, s_, dd = m(rn)
    print(f"HARNESS CHECK 3  top20 gate=none @10bps -> {c:.1%}/{s_:.3f}/{dd:.1%}   "
          f"(idea 55's candidate: 13.7%/1.123/-18.5%)  "
          f"{'PASS' if abs(c - 0.137) < 0.002 and abs(s_ - 1.123) < 0.01 else '*** MISMATCH ***'}")

    main_res = sweep(px, "universe.json")
    wf_main = walk_forward(main_res, "universe.json")

    # ---- calendar-year decomposition: when does the insurance actually pay out?
    print("\nCalendar-year returns by gate instrument (universe.json), vs SPY:")
    for bk in BOOKS:
        spy = main_res["spy"]
        yr = {"SPY": spy.groupby(spy.index.year).apply(lambda x: (1 + x).prod() - 1)}
        for g in GATES:
            r = main_res["RET"][(bk, g, PROTO_COST)]
            yr[g] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
        print(f"\n  book = {bk} @{PROTO_COST} bps")
        print(pd.DataFrame(yr).to_string(float_format=lambda x: f"{x:+.1%}"))

    # ---- robustness: same grid on the broad list
    pxb = load_universe(broad=True)
    broad_res = sweep(pxb, "universe_broad.json")
    wf_broad = walk_forward(broad_res, "universe_broad.json")

    cross_universe(main_res, broad_res)

    # ---- leaderboard rows (protocol cost only; the cost sweep lives in the console log)
    bl_r = at_cost(main_res["b_gross"], main_res["b_turn"], PROTO_COST)
    bl = m(bl_r); b1, b2 = halves(bl_r)
    print("\nLEADERBOARD rows:")
    for tagrows in (main_res["rows"], broad_res["rows"]):
        for lbl, c, s_, dd, h1, h2, oos, t, v in tagrows:
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {v} | {SCRIPT} |")
    for lbl, r in [("57 SPY buy & hold (universe.json sample) - reference", main_res["spy"]),
                   ("57 RULES v1 live (universe.json) - baseline", bl_r)]:
        c, s_, dd = m(r); h1, h2 = halves(r)
        print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
              f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | - | {SCRIPT} |")
    for lbl, v in wf_main + wf_broad:
        if v is None:
            print(f"| 2026-09-04 | {lbl} | - | - | - | - / - | {bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | "
                  f"no IS arm met the 4b bars | {SCRIPT} |")
        else:
            c, s_, dd, flag = v
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | - / - | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {flag} | {SCRIPT} |")


if __name__ == "__main__":
    main()
