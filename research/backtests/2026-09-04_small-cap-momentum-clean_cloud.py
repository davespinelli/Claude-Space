#!/usr/bin/env python3
"""QUEUE idea 38 — small-cap-momentum-clean (cloud lane, 2026-09-04).

Question
--------
Ideas 39/49 killed the *composite* v1 book (mean pct-rank of 12-1, 6m, 3m, with the
200d-MA + vol20<0.60 eligibility gate) on the sub-$2B panel, and traced the damage to
the eligibility gate rather than the ranking.  Idea 38 as filed asks the cleaner
question: does **plain 12-1 momentum** — the canonical Jegadeesh-Titman signal, with no
6m/3m blend and no vol20 gate — work on small caps, top-20/top-40 equal-weight, with
the 200d filter?  And, since idea 49 found the gate inverted here, the 200d filter is
carried as the second parameter (ON/OFF) so its contribution is measured, not assumed.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : data/prices_small.csv, 483 names, LESS the 44 with max_1d_move >= 1.0 in
           data/small_meta.csv (corrupted/relisted) -> 439 names.  SPY is a benchmark
           column only and is never selectable.
Signal   : mom12_1 = px.shift(21)/px.shift(252) - 1  (pure, no rank blend, no /sqrt(vol))
Book     : top-n by mom12_1 among eligible names, equal weight 0.75/n (75% gross, v1's
           own).  If fewer than n are eligible, hold all of them at 0.75/n and leave the
           rest in cash (idea 2's clause, worth +0.02 Sharpe there).
Params   : exactly 2 — n in {10,20,40,60} and FILTER in {200d ON, OFF}.  All 8 reported.
Execution: weekly rebalance, weights at close t applied at t+1, 10 bps per unit turnover.
Sample   : px.index[260] (2011-01-13) .. 2026-09-03, matching ideas 39/49 for comparability.
Controls : EW all 439 @75% (no filter, no ranking); RULES v1 on the small panel;
           RULES v1 live on universe.json; SPY buy & hold.
Rule 8   : parameters chosen on the first half only, evaluated untouched on the second,
           with two selection rules fixed BEFORE any OOS number is read.

SURVIVORSHIP: the panel is current constituents of a sub-$2B screen as of 2026-09-03;
names that crashed and delisted are absent.  Absolute CAGRs are therefore optimistic,
and the bias falls hardest on beaten-down high-vol names.  A KILL is strengthened by it;
any KEEP would have to be discounted for it.
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
COST = 10
FREQ = "W"
NS = [10, 20, 40, 60]
FILTERS = ["200d", "none"]


# ---------------------------------------------------------------- data
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    names = [c for c in px.columns if c != "SPY" and c not in bad]
    print(f"panel: {len(px.columns) - 1} names less {len(bad)} corrupted -> {len(names)}")
    return px[names + ["SPY"]], names


def mom12_1(px):
    return px.shift(21) / px.shift(252) - 1


def weights_fn(names, n, filt, ma=200, max_vol=None):
    """top-n by 12-1 momentum among eligible, 0.75/n each, cash if fewer than n eligible."""
    def f(px):
        sub = px[names]
        s = mom12_1(sub)
        if filt in ("200d", "both"):
            s = s.where(sub > sub.rolling(ma).mean())
        if filt in ("vol20", "both"):
            v = sub.pct_change().rolling(20).std() * np.sqrt(252)
            s = s.where(v < (max_vol if max_vol is not None else 0.60))
        rank = s.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


def ew_all(names):
    def f(px):
        live = px[names].notna() & (px[names].pct_change().rolling(20).count() > 0)
        w = live.astype(float)
        w = w.div(w.sum(axis=1).replace(0, np.nan), axis=0) * GROSS
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def run(px, fn, start, cost=COST):
    res = backtest(px, fn(px), cost_bps=cost, freq=FREQ)
    r = res["returns"].loc[start:]
    yrs = len(r) / 252
    return r, res["turnover"].loc[start:].sum() / yrs


def fail4b(r, spy, oos_sh=None, oos_spy_sh=None):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves and OOS, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  Returns the list of failed tests."""
    c, s, dd = m(r)
    h1, h2 = halves(r)
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh is not None and oos_spy_sh is not None and oos_sh <= oos_spy_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")          # both negative; more negative = worse
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    c, s, dd = m(r)
    h1, h2 = halves(r)
    bc, bs, bdd = m(base)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


ROWS = []


def emit(label, r, turn, spy, base, oos_sh=None, oos_spy_sh=None, note=""):
    c, s, dd = m(r)
    h1, h2 = halves(r)
    a, b = fail4a(r, base), fail4b(r, spy, oos_sh, oos_spy_sh)
    verdict = note or (
        ("KEEP 4a" if not a else "KILL 4a") + " / " + ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")
    )
    print(f"{label:<46} {c:7.1%} {s:6.3f} {dd:7.1%}  {h1:5.3f}/{h2:5.3f}  turn {turn:5.1f}x  {verdict}")
    ROWS.append((label, c, s, dd, h1, h2, verdict))
    return dict(label=label, CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2, turn=turn)


# ---------------------------------------------------------------- main
def main():
    px, names = small_panel()
    start = px.index[260]
    print(f"sample {start.date()} .. {px.index[-1].date()}  ({len(px.loc[start:])} trading days)\n")

    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    px_live = load_universe()                                   # universe.json, for the live baseline
    base_live, _ = run(px_live, rules_v1_weights, px_live.index[260])
    base_live = base_live.reindex(spy.index).dropna()
    def v1_small(p):
        w = pd.DataFrame(0.0, index=p.index, columns=p.columns)
        w[names] = rules_v1_weights(p[names])          # SPY is a benchmark, never holdable
        return w
    base_small, base_small_t = run(px, v1_small, start)

    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    print(f"4b bars vs SPY: H1>{s1:.3f}  H2>{s2:.3f}  MaxDD>={0.60 * sdd:.1%}  CAGR>={0.70 * sc:.1%}\n")

    hdr = f"{'arm':<46} {'CAGR':>7} {'Sharpe':>6} {'MaxDD':>7}  {'H1':>5}/{'H2':>5}"
    print(hdr); print("-" * 108)

    # ---- full-sample grid (all 8 points reported, no picking)
    grid = {}
    for filt in FILTERS:
        for n in NS:
            r, t = run(px, weights_fn(names, n, filt), start)
            grid[(filt, n)] = (r, t)

    # OOS numbers are filled in after the walk-forward; first pass without them
    for filt in FILTERS:
        for n in NS:
            r, t = grid[(filt, n)]
            emit(f"38 mom12-1 filt={filt:<4} n={n:<3}", r, t, spy, base_live)

    # ---- controls
    r_ew, t_ew = run(px, ew_all(names), start)
    emit("38 CONTROL EW all 439 @75% (no filt, no rank)", r_ew, t_ew, spy, base_live, note="-")
    emit("38 RULES v1 on the small panel - reference", base_small, base_small_t, spy, base_live, note="-")
    emit("38 RULES v1 live (universe.json) - baseline", base_live, float("nan"), spy, base_live, note="-")
    emit("38 SPY buy & hold - reference", spy, 0.0, spy, base_live, note="-")

    # ---- decomposition: is the 12-1 ranking worth anything without the gate?
    print("\nDecomposition (75% gross, same sample):")
    print(f"  EW all 439, no filter, no rank : {m(r_ew)[0]:6.1%} / {m(r_ew)[1]:.3f} / {m(r_ew)[2]:6.1%}  turn {t_ew:.1f}x")
    for n in NS:
        r, t = grid[("none", n)]
        print(f"  top-{n:<3} 12-1, NO 200d gate      : {m(r)[0]:6.1%} / {m(r)[1]:.3f} / {m(r)[2]:6.1%}  turn {t:.1f}x")
    for n in NS:
        r, t = grid[("200d", n)]
        print(f"  top-{n:<3} 12-1, WITH 200d gate    : {m(r)[0]:6.1%} / {m(r)[1]:.3f} / {m(r)[2]:6.1%}  turn {t:.1f}x")

    # gate cost at matched n, and the paired long-short read on the ranking
    print("\n200d gate cost at matched n (CAGR, Sharpe):")
    for n in NS:
        a = m(grid[("none", n)][0]); b = m(grid[("200d", n)][0])
        print(f"  n={n:<3} none {a[0]:6.1%}/{a[1]:.3f}   200d {b[0]:6.1%}/{b[1]:.3f}   "
              f"gate {100 * (b[0] - a[0]):+.1f}pp CAGR / {b[1] - a[1]:+.3f} Sharpe")

    # top-decile minus bottom-decile of the raw signal (no gate, no costs): does 12-1 rank at all?
    sub = px[names]
    s = mom12_1(sub)
    fwd = sub.pct_change().shift(-1)
    hi = s.rank(axis=1, pct=True, ascending=False) <= 0.10
    lo = s.rank(axis=1, pct=True, ascending=False) > 0.90
    ls = (fwd.where(hi).mean(axis=1) - fwd.where(lo).mean(axis=1)).loc[start:].dropna()
    tstat = ls.mean() / ls.std() * np.sqrt(len(ls))
    print(f"\nRaw 12-1 decile spread (no gate, no costs, arithmetic): {ls.mean() * 252:+.2%}/yr, "
          f"t {tstat:.2f}, n={len(ls)}")

    # arithmetic decile spreads are dominated by the bottom decile's vol on a survivorship
    # panel, so also compound each decile as an actual daily-rebalanced EW portfolio.
    print("Compounded EW decile portfolios by 12-1 momentum (daily rebal, 0 bps, 100% gross):")
    pctr = s.rank(axis=1, pct=True, ascending=False)
    for d in range(10):
        mask = (pctr > d / 10) & (pctr <= (d + 1) / 10)
        rd = fwd.where(mask).mean(axis=1).loc[start:].fillna(0.0)
        cd, sd, ddd = m(rd)
        print(f"  D{d + 1} ({'best' if d == 0 else 'worst' if d == 9 else '    '}): "
              f"CAGR {cd:6.1%}  Sharpe {sd:6.3f}  MaxDD {ddd:6.1%}")

    # ---- gate decomposition at a fixed n=40 (diagnostic, not a tuned parameter)
    print("\nEligibility-gate decomposition at n=40 (12-1 ranking held fixed):")
    for g in ("none", "200d", "vol20", "both"):
        r, t = run(px, weights_fn(names, 40, g), start)
        c, s_, dd = m(r)
        print(f"  gate={g:<6} {c:6.1%} / {s_:.3f} / {dd:6.1%}  turn {t:.1f}x")

    # ---- cost sensitivity on the grid's best full-sample Sharpe point (diagnostic)
    best = max(grid, key=lambda k: m(grid[k][0])[1])
    print(f"\nCost sensitivity for the grid's best point {best}:")
    for bps in (0, 10, 25, 50):
        r, t = run(px, weights_fn(names, best[1], best[0]), start, cost=bps)
        c, s_, dd = m(r)
        print(f"  {bps:>2} bps: {c:6.1%} / {s_:.3f} / {dd:6.1%}")

    # ---- rule 8 walk-forward: choose on the first half, evaluate on the second
    idx = px.loc[start:].index
    cut = idx[idx.searchsorted(pd.Timestamp("2017-01-01"))]   # PROTOCOL rule 8 boundary
    print(f"\nWalk-forward: IS {idx[0].date()}..{cut.date()}  OOS {cut.date()}..{idx[-1].date()}")
    spy_is, spy_oos = spy.loc[:cut], spy.loc[cut:]
    sc_is, ss_is, sdd_is = m(spy_is)
    print(f"  IS 4b bars: Sharpe>{ss_is:.3f}  MaxDD>={0.60 * sdd_is:.1%}  CAGR>={0.70 * sc_is:.1%}")

    cand = []
    for (filt, n), (r, t) in grid.items():
        ris = r.loc[:cut]
        c, s_, dd = m(ris)
        cand.append(dict(key=(filt, n), sh=s_, cagr=c, dd=dd))
    for c in sorted(cand, key=lambda x: -x["sh"]):
        print(f"  IS {str(c['key']):<16} Sharpe {c['sh']:6.3f}  CAGR {c['cagr']:6.1%}  MaxDD {c['dd']:6.1%}")

    picks = {}
    picks["plain-Sharpe"] = max(cand, key=lambda x: x["sh"])["key"]
    ok = [c for c in cand if c["sh"] > ss_is and c["dd"] >= 0.60 * sdd_is and c["cagr"] >= 0.70 * sc_is]
    picks["4b-aware"] = max(ok, key=lambda x: x["sh"])["key"] if ok else None

    sc_o, ss_o, sdd_o = m(spy_oos)
    print(f"\n  OOS SPY: {sc_o:.1%} / {ss_o:.3f} / {sdd_o:.1%}")
    base_oos = base_live.loc[cut:]
    print(f"  OOS RULES v1 live: {m(base_oos)[0]:.1%} / {m(base_oos)[1]:.3f} / {m(base_oos)[2]:.1%}")
    for rule, key in picks.items():
        if key is None:
            print(f"  OOS pick[{rule}]: NOTHING — no in-sample point met the 4b bars")
            ROWS.append((f"38 walk-forward {rule}: picks NOTHING", float('nan'), float('nan'),
                         float('nan'), float('nan'), float('nan'), "no IS point met the 4b bars"))
            continue
        r_o = grid[key][0].loc[cut:]
        c, s_, dd = m(r_o)
        flag = "beats SPY OOS" if s_ > ss_o else "loses to SPY OOS"
        print(f"  OOS pick[{rule}] = {key}: {c:.1%} / {s_:.3f} / {dd:.1%}   ({flag})")
        ROWS.append((f"38 walk-forward {rule}: {key} OOS", c, s_, dd, float("nan"), float("nan"),
                     f"OOS {flag} ({s_:.3f} vs {ss_o:.3f})"))

    # ---- final verdict lines with OOS attached, for the leaderboard
    print("\nFinal grid with OOS Sharpe attached (4b test complete):")
    final = []
    for filt in FILTERS:
        for n in NS:
            r, t = grid[(filt, n)]
            oos_sh = m(r.loc[cut:])[1]
            b = fail4b(r, spy, oos_sh, ss_o)
            a = fail4a(r, base_live)
            c, s_, dd = m(r); h1, h2 = halves(r)
            v = ("KEEP 4a" if not a else "KILL 4a") + " / " + ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")
            print(f"  filt={filt:<4} n={n:<3} {c:6.1%} {s_:6.3f} {dd:7.1%} {h1:5.3f}/{h2:5.3f} OOS {oos_sh:5.3f}  {v}")
            final.append((f"38 mom12-1 filt={filt} n={n}", c, s_, dd, h1, h2, oos_sh, v, t))

    print("\nLEADERBOARD rows:")
    bl = m(base_live); b1, b2 = halves(base_live)
    script = "research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py"
    for lbl, c, s_, dd, h1, h2, oos, v, t in final:
        print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
              f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {v} | {script} |")
    for lbl, r in [("38 CONTROL EW all 439 @75% (no filter, no ranking)", r_ew),
                   ("38 RULES v1 on the small panel - reference", base_small),
                   ("38 SPY buy & hold - reference", spy),
                   ("38 RULES v1 live (universe.json) - baseline", base_live)]:
        c, s_, dd = m(r); h1, h2 = halves(r)
        print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
              f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | - | {script} |")


if __name__ == "__main__":
    main()
