#!/usr/bin/env python3
"""QUEUE idea 63 — broad-H2-binding-bar (cloud, 2026-09-04).

Question
--------
Every cross-universe near-miss in this project now dies on the SAME bar: the second
half of the sample on `universe_broad.json`, where SPY's Sharpe is 0.837.  Idea 4
found H2 (or MaxDD) binding for 9 of 10 arms there, three of them within 0.03 of the
bar.  Idea 43 asked the same question of H1.  Idea 63 asks what H2 is actually made
of: is the shortfall concentrated in specific years — 2023-24 mega-cap leadership
that an equal-weight book structurally cannot hold — or is it a broad, persistent
failure that no amount of construction will fix?

This matters because it decides whether 4b is reachable on the broad list at all,
and therefore whether the standing candidates should be scoped to `universe.json`.

Method (diagnostic first, one remedy second)
--------------------------------------------
Books (all pre-chosen, none tuned here): `v1` (live rules), `top20` (idea 2's 4b
KEEP), `ew-all` (equal-weight all eligible @75%), `ew-band3` (idea 57's 4b
KEEP-candidate).  Weekly, t+1, 10 bps, both universes reported.

1. **Halves, exactly as the protocol computes them** — the eval sample split in two
   by row count.  H2's actual dates are printed, not assumed.
2. **Year-by-year decomposition of H2**: each book's return and Sharpe vs SPY's, and
   the annualised daily excess with its t-stat, per calendar year.
3. **Leave-one-year-out H2 Sharpe**: drop one year at a time and re-test the book
   against SPY's Sharpe on the SAME reduced sample.  If one year is responsible,
   dropping it flips the test; if no single year does, the shortfall is broad.
4. **The concentration test, using a tradable yardstick**: RSP (equal-weight S&P
   500) is in both universes.  `RSP - SPY` is the concentration factor — negative
   when mega-caps lead.  Every book's daily excess return over SPY is regressed on
   it (H1 and H2 separately): a beta near 1 with alpha near 0 says the book's
   shortfall IS the equal-weight tilt, i.e. structural, not fixable by construction.
5. **One remedy, one tuned parameter**: replace a fraction b of the book with QQQ
   (in both universes) at MATCHED 75% gross — an explicit mega-cap sleeve —
   b in {0, 0.25, 0.50}.  All points reported at 5/10/25/50 bps, both universes,
   with the full 4b test and a rule-8 walk-forward that chooses b on 2009-2016 only.

SURVIVORSHIP: both lists are current constituents, which biases this test in a
specific and important direction — the mega-caps whose 2023-24 run the books miss are
in the list *because* they won.  Any conclusion that concentration is structural is
therefore an upper bound on the effect, and the leave-one-year-out and regression
results should be read with that in mind.
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
COSTS = [5, 10, 25, 50]
PROTO_COST = 10
BLENDS = [0.0, 0.25, 0.50]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SCRIPT = "research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py"


# ---------------------------------------------------------------- construction
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


def blended(fn, b, core="QQQ"):
    """Replace fraction b of the book with a passive core, holding total gross at 75%."""
    def f(px):
        w = fn(px) * (1.0 - b)
        if b > 0:
            w = w.copy()
            w[core] = w[core] + b * GROSS
        return w
    return f


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def sharpe(r):
    return metrics(r)["Sharpe"]


def halves_idx(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def ann_t(d):
    d = d.dropna()
    return float(d.mean() * 252), float(d.mean() / (d.std() / np.sqrt(len(d))))


def ols(y, x):
    """Simple OLS y = a + b x on daily series; returns a (annualised), b, t(b), R2."""
    df = pd.concat([y.rename("y"), x.rename("x")], axis=1).dropna()
    X = np.column_stack([np.ones(len(df)), df["x"].values])
    beta, *_ = np.linalg.lstsq(X, df["y"].values, rcond=None)
    resid = df["y"].values - X @ beta
    s2 = resid @ resid / (len(df) - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    ss_tot = ((df["y"].values - df["y"].values.mean()) ** 2).sum()
    return float(beta[0] * 252), float(beta[1]), float(beta[1] / se), float(1 - resid @ resid / ss_tot)


def gross_run(px, fn, start):
    res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def at_cost(g, t, bps):
    return g - t * bps / 1e4


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r)
    r1, r2 = halves_idx(r)
    sc, ss, sdd = m(spy)
    s1, s2 = halves_idx(spy)
    bad = []
    if sharpe(r1) <= sharpe(s1): bad.append("H1")
    if sharpe(r2) <= sharpe(s2): bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


# ---------------------------------------------------------------- diagnosis
def diagnose(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    rsp = px["RSP"].pct_change().fillna(0).loc[start:]
    qqq = px["QQQ"].pct_change().fillna(0).loc[start:]
    spy1, spy2 = halves_idx(spy)

    print(f"\n{'=' * 132}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}")
    print(f"  H1 = {spy1.index[0].date()} -> {spy1.index[-1].date()}   "
          f"H2 = {spy2.index[0].date()} -> {spy2.index[-1].date()}")
    print(f"  SPY H1 Sharpe {sharpe(spy1):.3f}  H2 Sharpe {sharpe(spy2):.3f}  (the 4b bars)")
    print(f"  RSP (equal-weight S&P) H1 {sharpe(halves_idx(rsp)[0]):.3f}  H2 {sharpe(halves_idx(rsp)[1]):.3f}"
          f"   QQQ H1 {sharpe(halves_idx(qqq)[0]):.3f}  H2 {sharpe(halves_idx(qqq)[1]):.3f}")
    print("=" * 132)

    R = {}
    for bk, fn in BOOKS.items():
        g, t = gross_run(px, fn, start)
        R[bk] = at_cost(g, t, PROTO_COST)

    # ---- 1. where does each book stand on the two bars
    print("\nHALVES at 10 bps (the 4b Sharpe bars are SPY's own halves):")
    print(f"  {'book':<10}{'H1 Sh':>8}{'H2 Sh':>8}{'H1-bar':>9}{'H2-bar':>9}"
          f"{'H1 CAGR':>9}{'H2 CAGR':>9}{'SPY H1':>9}{'SPY H2':>9}")
    for bk in BOOKS:
        r1, r2 = halves_idx(R[bk])
        print(f"  {bk:<10}{sharpe(r1):8.3f}{sharpe(r2):8.3f}{sharpe(r1) - sharpe(spy1):+9.3f}"
              f"{sharpe(r2) - sharpe(spy2):+9.3f}{m(r1)[0]:9.1%}{m(r2)[0]:9.1%}"
              f"{m(spy1)[0]:9.1%}{m(spy2)[0]:9.1%}")

    # ---- 2. H2 year by year
    h2_years = sorted(set(halves_idx(R["ew-all"])[1].index.year))
    print(f"\nH2 YEAR BY YEAR — book return, SPY return, excess (annualised daily mean) and t.")
    print(f"  {'year':<6}{'SPY':>8}{'RSP':>8}{'RSP-SPY':>9}   " +
          "".join(f"{bk:>21}" for bk in BOOKS))
    for y in h2_years:
        cells = []
        for bk in BOOKS:
            r2 = halves_idx(R[bk])[1]
            ry = r2[r2.index.year == y]
            sy = spy[spy.index.year == y].reindex(ry.index)
            ann, t = ann_t(ry - sy)
            cells.append(f"{float((1 + ry).prod() - 1):+7.1%} ({ann * 100:+6.1f} t{t:+5.2f})")
        sy_all = spy[spy.index.year == y]
        ry_all = rsp[rsp.index.year == y]
        print(f"  {y:<6}{float((1 + sy_all).prod() - 1):+8.1%}{float((1 + ry_all).prod() - 1):+8.1%}"
              f"{float((1 + ry_all).prod() - (1 + sy_all).prod()) * 100:+8.1f}   " +
              "".join(f"{c:>21}" for c in cells))

    # ---- 3. leave-one-year-out H2
    print("\nLEAVE-ONE-YEAR-OUT H2 Sharpe (book vs SPY on the same reduced sample; "
          "'flips' = book clears the bar without that year):")
    print(f"  {'book':<10}{'H2 (all)':>10}{'bar':>8}   " + "".join(f"{y:>16}" for y in h2_years))
    for bk in BOOKS:
        r2 = halves_idx(R[bk])[1]
        base_ok = sharpe(r2) > sharpe(spy2)
        cells = []
        for y in h2_years:
            keep = r2.index.year != y
            rr, ss = r2[keep], spy2[spy2.index.year != y]
            ok = sharpe(rr) > sharpe(ss)
            flag = "*" if ok and not base_ok else (" " if ok == base_ok else "-")
            cells.append(f"{sharpe(rr):.3f}/{sharpe(ss):.3f}{flag}")
        print(f"  {bk:<10}{sharpe(r2):10.3f}{sharpe(spy2):8.3f}   " +
              "".join(f"{c:>16}" for c in cells))
    print("   * = dropping that year alone flips the book from failing to clearing the H2 bar")

    # ---- 4. concentration regression
    print("\nCONCENTRATION TEST — daily (book - SPY) regressed on (RSP - SPY), the "
          "equal-weight-minus-cap-weight factor:")
    print(f"  {'book':<10}{'half':<6}{'alpha/yr':>10}{'beta':>8}{'t(beta)':>9}{'R2':>7}"
          f"{'excess/yr':>11}{'t':>7}")
    conc = rsp - spy
    for bk in BOOKS:
        for lbl, sl in (("H1", 0), ("H2", 1)):
            rr = halves_idx(R[bk])[sl]
            ss = halves_idx(spy)[sl]
            cc = halves_idx(conc)[sl]
            a, b, tb, r2_ = ols(rr - ss, cc)
            ann, t = ann_t(rr - ss)
            print(f"  {bk:<10}{lbl:<6}{a * 100:+10.2f}{b:8.2f}{tb:+9.2f}{r2_:7.3f}"
                  f"{ann * 100:+11.2f}{t:+7.2f}")
    a, b, tb, r2_ = ols(halves_idx(qqq - spy)[1], halves_idx(conc)[1])
    print(f"  {'QQQ':<10}{'H2':<6}{a * 100:+10.2f}{b:8.2f}{tb:+9.2f}{r2_:7.3f}"
          f"{ann_t(halves_idx(qqq - spy)[1])[0] * 100:+11.2f}"
          f"{ann_t(halves_idx(qqq - spy)[1])[1]:+7.2f}   (reference: the mega-cap sleeve itself)")

    return R, spy, start


# ---------------------------------------------------------------- remedy
def remedy(px, tag, start, spy, results):
    sc, ss, sdd = m(spy)
    spy1, spy2 = halves_idx(spy)
    ss_o = sharpe(spy.loc[OOS_START:])
    print(f"\nREMEDY — replace fraction b of the book with QQQ at matched 75% gross ({tag}).")
    print(f"  4b bars: H1>{sharpe(spy1):.3f}  H2>{sharpe(spy2):.3f}  OOS>{ss_o:.3f}  "
          f"MaxDD>={0.60 * sdd:.1%}  CAGR>={0.70 * sc:.1%}")
    print(f"  {'book':<10}{'b':>6}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
          f"{'H1':>7}{'H2':>7}{'OOS':>7}   verdict")
    RET = {}
    for bk, fn in BOOKS.items():
        for b in BLENDS:
            g, t = gross_run(px, blended(fn, b), start)
            for c in COSTS:
                r = at_cost(g, t, c)
                RET[(bk, b, c)] = r
                cg, sh, dd = m(r)
                r1, r2 = halves_idx(r)
                oos = sharpe(r.loc[OOS_START:])
                bad = fail4b(r, spy, oos, ss_o)
                v = "KEEP 4b" if not bad else "KILL 4b (" + ",".join(bad) + ")"
                mark = " <-" if c == PROTO_COST else ""
                print(f"  {bk:<10}{b:6.2f}{c:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}"
                      f"{sharpe(r1):7.3f}{sharpe(r2):7.3f}{oos:7.3f}   {v}{mark}")
                if c == PROTO_COST:
                    results.append(dict(tag=tag, book=bk, b=b, cagr=cg, sharpe=sh, dd=dd,
                                        h1=sharpe(r1), h2=sharpe(r2), oos=oos, verdict=v,
                                        pass4b=not bad))
        print()

    # rule 8: choose b (and book) on IS only
    print(f"  Rule 8 walk-forward — b (and book) chosen on IS 2009-2016, evaluated on "
          f"{OOS_START}-2026 at {PROTO_COST} bps.")
    is_spy, oos_spy = spy.loc[:IS_END], spy.loc[OOS_START:]
    isc, iss, isdd = m(is_spy)
    oc_s, osh_s, odd_s = m(oos_spy)
    cand = []
    for bk in BOOKS:
        for b in BLENDS:
            r = RET[(bk, b, PROTO_COST)]
            ic, ish, idd = m(r.loc[:IS_END])
            oc, osh, odd = m(r.loc[OOS_START:])
            cand.append((bk, b, ic, ish, idd, oc, osh, odd))
    r1 = max(cand, key=lambda x: x[3])
    ok = [c for c in cand if c[4] >= 0.60 * isdd and c[2] >= 0.70 * isc]
    r2 = max(ok, key=lambda x: x[3]) if ok else None
    cl = lambda c: c[6] > osh_s and c[7] >= 0.60 * odd_s and c[5] >= 0.70 * oc_s
    print(f"    SPY OOS {oc_s:.1%}/{osh_s:.3f}/{odd_s:.1%}")
    print(f"    RULE A (max IS Sharpe)      -> {r1[0]}/b={r1[1]:.2f}: "
          f"OOS {r1[5]:.1%}/{r1[6]:.3f}/{r1[7]:.1%} [{'clears' if cl(r1) else 'FAILS'} OOS 4b bars]")
    if r2:
        print(f"    RULE B (4b-aware IS filter) -> {r2[0]}/b={r2[1]:.2f}: "
              f"OOS {r2[5]:.1%}/{r2[6]:.3f}/{r2[7]:.1%} [{'clears' if cl(r2) else 'FAILS'} OOS 4b bars]")
    else:
        print("    RULE B (4b-aware IS filter) -> NOTHING selected")

    # ---- the decisive control: is the fix mega-cap-specific, or just more beta?
    print(f"\n  CORE-INSTRUMENT CONTROL at b=0.25 ({tag}) — QQQ is the best-performing liquid US "
          "index OF THIS SAMPLE,\n  so a QQQ sleeve is a hindsight tilt 4b cannot detect. If a "
          "SPY or VTI sleeve fixes the same bar,\n  the books are simply under-invested at 75% "
          "gross and the finding is not about mega caps at all.")
    print(f"  {'book':<10}{'core':<6}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
          f"{'H1':>7}{'H2':>7}{'OOS':>7}   verdict")
    for bk, fn in BOOKS.items():
        for core in ("QQQ", "SPY", "VTI"):
            g, t = gross_run(px, blended(fn, 0.25, core), start)
            for c in (PROTO_COST, 25):
                r = at_cost(g, t, c)
                cg, sh, dd = m(r)
                q1, q2 = halves_idx(r)
                oos = sharpe(r.loc[OOS_START:])
                bad = fail4b(r, spy, oos, ss_o)
                print(f"  {bk:<10}{core:<6}{c:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}"
                      f"{sharpe(q1):7.3f}{sharpe(q2):7.3f}{oos:7.3f}   "
                      f"{'KEEP 4b' if not bad else 'KILL 4b (' + ','.join(bad) + ')'}")
        print()
    return RET


# ---------------------------------------------------------------- main
def main():
    results = []
    for tag, kw in (("universe_broad.json", dict(broad=True)), ("universe.json", {})):
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            sys.exit("!! CALENDAR-DAY INDEX DETECTED — aborting.")
        R, spy, start = diagnose(px, tag)
        if tag == "universe_broad.json":
            print("\nHARNESS CHECK (broad, 10 bps): "
                  + ", ".join(f"{bk} {m(R[bk])[0]:.1%}/{m(R[bk])[1]:.3f}/{m(R[bk])[2]:.1%}"
                              for bk in BOOKS)
                  + "   [published: top20 13.1%/0.958/-20.1%, ew-all 10.7%/1.027/-17.7%, "
                    "ew-band3 11.1%/1.064/-16.8%]")
        remedy(px, tag, start, spy, results)

    df = pd.DataFrame(results)
    print(f"\n{'=' * 132}\nCROSS-UNIVERSE 4b SUMMARY at {PROTO_COST} bps\n" + "=" * 132)
    print(f"  {'book':<10}{'b':>6}{'universe.json':>28}{'universe_broad.json':>30}   both?")
    n_both = 0
    for bk in BOOKS:
        for b in BLENDS:
            a = df[(df.tag == "universe.json") & (df.book == bk) & (df.b == b)].iloc[0]
            c = df[(df.tag == "universe_broad.json") & (df.book == bk) & (df.b == b)].iloc[0]
            both = "YES" if a.pass4b and c.pass4b else "no"
            n_both += both == "YES"
            print(f"  {bk:<10}{b:6.2f}{a.cagr:9.1%}/{a.sharpe:.3f}/{a.dd:7.1%}"
                  f"{c.cagr:11.1%}/{c.sharpe:.3f}/{c.dd:7.1%}   {both}")
    print(f"\n  {n_both} of {len(BOOKS) * len(BLENDS)} (book, b) arms pass 4b on both lists.")
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
