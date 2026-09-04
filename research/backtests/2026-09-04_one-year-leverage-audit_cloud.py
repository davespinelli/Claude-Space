#!/usr/bin/env python3
"""QUEUE idea 89 — one-year-leverage-audit (cloud, 2026-09-04).

Question
--------
Idea 15's entire full-sample t-stat turned out to be one calendar year (2017, BTC
+1425%).  Nothing in PROTOCOL would have caught that before the memo was written:
rules 4 and 8 split the sample in halves and in time, which is exactly the wrong
cut for a result carried by a single year sitting inside one half.  This run builds
the missing harness — leave-one-calendar-year-out (LOYO) — and puts every standing
candidate and every published 4b pass through it.

The pre-registered question is not "do the candidates look good" but "which 4b
passes survive the deletion of their single best year", plus a second question that
makes the audit worth more than a table: **does LOYO-robustness improve out-of-sample
selection?**  Rule 8 is therefore run with two selectors fixed in advance — plain
max-IS-Sharpe, and max-IS-worst-case-LOYO-Sharpe — and their OOS results compared.

Method
------
For a book's daily return series r and a calendar year Y, the LOYO sample is r with
every day of Y removed and the remainder chain-linked.  Every statistic (CAGR,
Sharpe, MaxDD, halves, OOS) is recomputed on the retained days, and — this is the
part that makes the verdicts comparable — SPY's 4b bars are recomputed on THE SAME
retained days, so a year that was good for the book and good for SPY does not score
as robustness.  Halves are re-split on the retained days; the OOS window is the
retained days from 2017 on (unchanged when the dropped year is in-sample).

Books (all PRE-EXISTING; nothing is constructed or tuned here)
  v1        RULES v1 exactly as live (n=5, 15% each, composite WITH /sqrt(vol20)).
  top20     idea 2's standing 4b KEEP: top-20 eligible at 0.75/20 each, cash when
            E_t < 20 (idea 2 found that clause worth +0.02 Sharpe — kept literal).
  frac085   idea 46's portability candidate: top ceil(0.85 x E_t) at 0.75/k.
  ew-band3  idea 57's candidate: equal-weight all eligible, 3% MA band gate, 75%.
  EWall     idea 72's `B136/EWall`: equal-weight all eligible, 200d gate, 75%.
  SPY       buy-and-hold — the calibration case, and the 4b benchmark.
  EWall+c10 idea 15's PARKed crypto arm (EWall, matched funding, `same` gate, 10%
            cap) on universe.json only.  This is the HARNESS VALIDATION: idea 15
            already established that its t-stat is 2017, so a working LOYO harness
            must flag this arm and must flag it on 2017.  If it does not, the
            harness is wrong and none of the other rows can be believed.

Params   : ZERO tuned parameters.  Every book, universe, and dropped year is
           reported; nothing is selected on out-of-sample data.
Costs    : 10 bps (PROTOCOL rule 2), weekly, next-day execution, long-only.
Universes: universe.json (56) and universe_broad.json (136), both fully reported.

Caveats  : (1) A spliced equity curve's MaxDD is not a real path — a drawdown that
           straddles the deleted year is shortened by the splice.  MaxDD-based LOYO
           verdicts are therefore OPTIMISTIC about drawdown and are read as such;
           the Sharpe and CAGR columns carry no such artefact.  (2) LOYO deletes a
           year from the realised path; it is a leverage/attribution diagnostic, not
           a claim about what would have happened.  (3) SURVIVORSHIP: both lists are
           current constituents, so every level is optimistic; the audit measures
           concentration of the edge in time, which survivorship does not create.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
FRAC = 0.85
BAND = 0.03
CRYPTO = ["BTC-USD", "ETH-USD"]
CRYPTO_CAP = 0.10
COST_BPS = 10
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SCRIPT = "research/backtests/2026-09-04_one-year-leverage-audit_cloud.py"


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


def eligible(px, gate="200d"):
    return (vol20(px) < MAX_VOL) & trend(px, gate)


def w_top20(px):
    """idea 2: top-20 at 0.75/20 each; de-grosses to cash when E_t < 20 (deliberate)."""
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def w_frac085(px):
    """idea 46: top ceil(0.85 x E_t) at 0.75/k each — always 75% gross."""
    elig = eligible(px)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    k = np.ceil(FRAC * elig.sum(axis=1).astype(float)).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(GROSS / k, axis=0)


def _ewall(px, gate):
    e = eligible(px, gate).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


def w_ewall(px):
    return _ewall(px, "200d")


def w_ewband3(px):
    return _ewall(px, "band3")


BOOKS = {"v1": rules_v1_weights, "top20": w_top20, "frac085": w_frac085,
         "ew-band3": w_ewband3, "EWall": w_ewall}


def w_ewall_crypto(px_all, px_eq):
    """idea 15's PARKed arm: EWall equity leg + BTC/ETH at 10% each, `same` gate
    (v1's 200d AND vol20<0.60 applied to crypto too), `matched` funding (the sleeve
    never adds gross — the equity leg is scaled down to pay for it).  Copied from
    research/backtests/2026-09-04_crypto-sleeve_C.py."""
    w_eq = w_ewall(px_eq).reindex(px_all.index).fillna(0.0)
    w = pd.DataFrame(0.0, index=px_all.index, columns=px_all.columns)
    w[w_eq.columns] = w_eq.values
    pxc = px_all[CRYPTO]
    wc = eligible(pxc).astype(float) * CRYPTO_CAP
    g = w_eq.sum(axis=1)
    wc_tot = wc.sum(axis=1)
    keep = wc_tot.clip(upper=g)
    wc = wc.mul(np.divide(keep, wc_tot.replace(0, np.nan)).fillna(0.0), axis=0)
    eq_scale = np.divide(g - keep, g.replace(0, np.nan)).fillna(0.0)
    w[w_eq.columns] = w_eq.mul(eq_scale, axis=0).values
    w[CRYPTO] = wc[CRYPTO].values
    return w


# ---------------------------------------------------------------- LOYO harness
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def drop_year(r, y):
    """The LOYO sample: every day of calendar year y removed, remainder chain-linked."""
    return r[r.index.year != y] if y is not None else r


def stats(r, spy):
    """All the numbers a 4b verdict needs, for a book and its benchmark on the SAME days."""
    c, s, dd = m(r)
    h1, h2 = halves(r)
    oos = m(r.loc[OOS_START:])[1]
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    soos = m(spy.loc[OOS_START:])[1]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos <= soos: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    marg = {"H1": h1 - s1, "H2": h2 - s2, "OOS": oos - soos,
            "DD": (dd - 0.60 * sdd) * 100, "CAGR": (c - 0.70 * sc) * 100}
    return dict(cagr=c, sharpe=s, dd=dd, h1=h1, h2=h2, oos=oos,
                pass4b=not bad, bad=bad, marg=marg,
                bars=dict(H1=s1, H2=s2, OOS=soos, DD=0.60 * sdd, CAGR=0.70 * sc))


def loyo_table(r, spy, years):
    """{year or None: stats(...)} with the benchmark recomputed on the same retained days."""
    out = {None: stats(r, spy)}
    for y in years:
        out[y] = stats(drop_year(r, y), drop_year(spy, y))
    return out


def year_ret(r, y):
    s = r[r.index.year == y]
    return float((1 + s).prod() - 1) if len(s) else np.nan


# ---------------------------------------------------------------- one universe
def sweep(px, tag, rows, extra=None):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    years = sorted(set(spy.index.year))

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    sc, ss, sdd = m(spy)
    print(f"\n{'=' * 150}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}, "
          f"{len(years)} calendar years {years[0]}-{years[-1]} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY full sample {sc:.1%}/{ss:.3f}/{sdd:.1%}")
    print("=" * 150)

    R = {}
    for bk, fn in BOOKS.items():
        res = backtest(px, fn(px), cost_bps=COST_BPS, freq="W")
        R[bk] = res["returns"].loc[start:]
    R["SPY"] = spy
    if extra:
        R.update({k: v.loc[start:] for k, v in extra.items()})

    T = {bk: loyo_table(r, spy, years) for bk, r in R.items()}

    # ---- full-sample reference
    print(f"\nFULL SAMPLE at {COST_BPS} bps (the published numbers these candidates stand on):")
    print(f"  {'book':<12}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'H1':>7}{'H2':>7}{'OOS':>7}"
          f"   4b")
    for bk in R:
        st = T[bk][None]
        print(f"  {bk:<12}{st['cagr']:8.1%}{st['sharpe']:8.3f}{st['dd']:8.1%}{st['h1']:7.3f}"
              f"{st['h2']:7.3f}{st['oos']:7.3f}   "
              f"{'PASS' if st['pass4b'] else 'FAIL (' + ','.join(st['bad']) + ')'}")

    # ---- where the return actually is
    print(f"\nWHERE THE EDGE SITS IN TIME ({tag}) — calendar-year return, and excess over SPY:")
    print(f"  {'book':<12}" + "".join(f"{y:>8}" for y in years))
    for bk in R:
        print(f"  {bk:<12}" + "".join(f"{year_ret(R[bk], y) * 100:7.1f}" for y in years))
    print(f"  {'-' * (12 + 8 * len(years))}")
    print("  excess over SPY (pp):")
    for bk in R:
        if bk == "SPY":
            continue
        print(f"  {bk:<12}" + "".join(
            f"{(year_ret(R[bk], y) - year_ret(spy, y)) * 100:7.1f}" for y in years))

    # ---- the audit itself
    print(f"\nLEAVE-ONE-YEAR-OUT ({tag}) — every statistic and every 4b bar recomputed on the "
          f"retained days, SPY included.")
    for bk in R:
        st0 = T[bk][None]
        print(f"\n  {bk}  (full: {st0['cagr']:.1%}/{st0['sharpe']:.3f}/{st0['dd']:.1%}, "
              f"4b {'PASS' if st0['pass4b'] else 'FAIL (' + ','.join(st0['bad']) + ')'})")
        print(f"    {'drop':>6}{'CAGR':>8}{'dCAGR':>8}{'Sharpe':>8}{'dSharpe':>9}{'MaxDD':>8}"
              f"{'H1':>7}{'H2':>7}{'OOS':>7}   {'4b':<24}binding bar")
        for y in years:
            st = T[bk][y]
            b = min(st["marg"], key=st["marg"].get)
            v = "PASS" if st["pass4b"] else "FAIL (" + ",".join(st["bad"]) + ")"
            flag = "  <-- flips" if st["pass4b"] != st0["pass4b"] else ""
            print(f"    {y:6d}{st['cagr']:8.1%}{(st['cagr'] - st0['cagr']) * 100:+8.2f}"
                  f"{st['sharpe']:8.3f}{st['sharpe'] - st0['sharpe']:+9.3f}{st['dd']:8.1%}"
                  f"{st['h1']:7.3f}{st['h2']:7.3f}{st['oos']:7.3f}   {v:<24}"
                  f"{b} ({st['marg'][b]:+.3f}){flag}")

    # ---- headline
    print(f"\nAUDIT VERDICT ({tag}) — a 4b pass is LOYO-ROBUST only if it survives dropping "
          f"EVERY single calendar year.")
    print(f"  {'book':<12}{'full 4b':>9}{'LOYO passes':>13}{'worst drop':>12}"
          f"{'worst Sharpe':>14}{'dSharpe':>9}{'best yr':>9}{'excess pp':>11}   "
          f"{'4b w/o best yr':<22}breaking bars")
    for bk in R:
        st0 = T[bk][None]
        n_pass = sum(1 for y in years if T[bk][y]["pass4b"])
        worst_y = min(years, key=lambda y: T[bk][y]["sharpe"])
        exc = {y: year_ret(R[bk], y) - year_ret(spy, y) for y in years}
        best_y = max(years, key=lambda y: exc[y])
        stb = T[bk][best_y]
        breaking = sorted({b for y in years for b in T[bk][y]["bad"]} - set(st0["bad"]))
        rows.append(dict(tag=tag, book=bk, full4b=st0["pass4b"], loyo_pass=n_pass,
                         n_years=len(years), worst_year=worst_y,
                         worst_sharpe=T[bk][worst_y]["sharpe"], full_sharpe=st0["sharpe"],
                         best_year=best_y, best_excess=exc[best_y],
                         pass_wo_best=stb["pass4b"], cagr=st0["cagr"], dd=st0["dd"],
                         h1=st0["h1"], h2=st0["h2"], oos=st0["oos"]))
        print(f"  {bk:<12}{('PASS' if st0['pass4b'] else 'FAIL'):>9}"
              f"{f'{n_pass}/{len(years)}':>13}{worst_y:12d}"
              f"{T[bk][worst_y]['sharpe']:14.3f}"
              f"{T[bk][worst_y]['sharpe'] - st0['sharpe']:+9.3f}{best_y:9d}"
              f"{exc[best_y] * 100:+11.1f}   "
              f"{('PASS' if stb['pass4b'] else 'FAIL (' + ','.join(stb['bad']) + ')'):<22}"
              f"{','.join(breaking) if breaking else '-'}")

    # ---- why does a verdict flip: the book weakening, or the bar moving?
    print(f"\nFLIP ATTRIBUTION ({tag}) — a 4b bar is a function of SPY on the SAME retained "
          f"days, so a verdict can flip because the BOOK got worse or because the BAR got "
          f"harder.  For every year whose deletion flips a PASS to a FAIL:")
    print(f"  {'book':<12}{'drop':>6}{'breaks':>8}{'d book':>9}{'d bar':>9}   attribution")
    any_flip = False
    for bk in R:
        st0 = T[bk][None]
        if not st0["pass4b"]:
            continue
        for y in years:
            st = T[bk][y]
            if st["pass4b"]:
                continue
            any_flip = True
            b = st["bad"][0]
            if b == "CAGR":
                dbook = (st["cagr"] - st0["cagr"]) * 100
                dbar = (st["bars"]["CAGR"] - st0["bars"]["CAGR"]) * 100
            elif b == "DD":
                dbook = (st["dd"] - st0["dd"]) * 100
                dbar = (st["bars"]["DD"] - st0["bars"]["DD"]) * 100
            else:
                dbook = st[{"H1": "h1", "H2": "h2", "OOS": "oos"}[b]] - \
                    st0[{"H1": "h1", "H2": "h2", "OOS": "oos"}[b]]
                dbar = st["bars"][b] - st0["bars"][b]
            who = "BAR moved" if abs(dbar) > abs(dbook) else "BOOK weakened"
            print(f"  {bk:<12}{y:6d}{b:>8}{dbook:+9.3f}{dbar:+9.3f}   {who}")
    if not any_flip:
        print("  (no full-sample 4b pass on this universe flips under any single-year deletion)")

    # ---- how year-dependent is any of this, relative to the benchmark itself?
    print(f"\nYEAR-DEPENDENCE CALIBRATION ({tag}) — SPY's own numbers move under LOYO too, so "
          f"the benchmark row is the noise floor.")
    print(f"  {'book':<12}{'mean dSharpe':>14}{'sd dSharpe':>12}{'worst dSharpe':>15}"
          f"{'|worst| / SPY':>15}")
    spy_worst = min(T["SPY"][y]["sharpe"] - T["SPY"][None]["sharpe"] for y in years)
    for bk in R:
        d = np.array([T[bk][y]["sharpe"] - T[bk][None]["sharpe"] for y in years])
        print(f"  {bk:<12}{d.mean():+14.4f}{d.std():12.4f}{d.min():+15.4f}"
              f"{d.min() / spy_worst:15.2f}")

    # ---- rule 8: does LOYO-robustness improve out-of-sample SELECTION?
    print(f"\nRULE 8 WALK-FORWARD ({tag}) — books ranked on IS <= {IS_END} only under two "
          f"selectors fixed before any OOS number was read, then evaluated untouched on "
          f"{OOS_START}+.")
    print("  S1 = max IS Sharpe (the incumbent rule).   S2 = max IS WORST-CASE LOYO Sharpe "
          "(this run's proposal: rank books by how they look after their best IS year is "
          "deleted).")
    is_years = [y for y in years if y <= 2016]
    cand = [bk for bk in R if bk != "SPY"]
    is_sh, is_worst = {}, {}
    for bk in cand:
        r_is = R[bk].loc[:IS_END]
        is_sh[bk] = m(r_is)[1]
        is_worst[bk] = min(m(drop_year(r_is, y))[1] for y in is_years)
    p1 = max(cand, key=lambda b: is_sh[b])
    p2 = max(cand, key=lambda b: is_worst[b])
    oos_spy = spy.loc[OOS_START:]
    osc, oss, osdd = m(oos_spy)
    print(f"  IS Sharpe / IS worst-case-LOYO Sharpe: " +
          ", ".join(f"{b} {is_sh[b]:.3f}/{is_worst[b]:.3f}" for b in cand))
    print(f"  OOS SPY {osc:.1%}/{oss:.3f}/{osdd:.1%} "
          f"(OOS 4b bars: Sharpe>{oss:.3f}, MaxDD>={0.60 * osdd:.1%}, CAGR>={0.70 * osc:.1%})")
    print(f"  {'selector':<34}{'pick':<12}{'OOS CAGR':>10}{'OOS Sharpe':>12}"
          f"{'OOS MaxDD':>11}   {'OOS 4b':<24}OOS worst-drop Sharpe")
    oos_years = [y for y in years if y >= 2017]
    for lbl, pk in (("S1 max IS Sharpe", p1), ("S2 max IS worst-case LOYO", p2)):
        r_oos = R[pk].loc[OOS_START:]
        c, s, dd = m(r_oos)
        bad = []
        if s <= oss: bad.append("Sharpe")
        if dd < 0.60 * osdd: bad.append("DD")
        if c < 0.70 * osc: bad.append("CAGR")
        wo = min(m(drop_year(r_oos, y))[1] for y in oos_years)
        print(f"  {lbl:<34}{pk:<12}{c:10.1%}{s:12.3f}{dd:11.1%}   "
              f"{('PASS' if not bad else 'FAIL (' + ','.join(bad) + ')'):<24}{wo:.3f}")
    print(f"  (S1 and S2 pick the SAME book)" if p1 == p2 else
          f"  (S1 and S2 DISAGREE — {p1} vs {p2}; the OOS rows above are the whole point of "
          f"the audit)")
    return R, T, years


# -------------------------------------------- LOYO on a DIFFERENCE (the real test)
def loyo_difference(r, ctl, years, label, ctl_label):
    """LOYO applied to the paired daily difference r - ctl, i.e. to the statistic an
    idea is actually argued on.  Idea 15's claim was a paired t on the sleeve-vs-control
    difference, not a level, so this — not the book's own Sharpe — is where a one-year
    leverage should show up.  This block is the harness's validation case: idea 15 has
    already established that its t-stat is 2017, so LOYO must find 2017 here.
    """
    d0 = (r - ctl).dropna()
    t0 = d0.mean() / (d0.std() / np.sqrt(len(d0)))
    print(f"\nLOYO ON THE PAIRED DIFFERENCE — {label} minus {ctl_label} (harness validation).")
    print(f"  full sample: {d0.mean() * 252 * 100:+.2f} pp/yr, t {t0:+.2f} over {len(d0)} days")
    print(f"    {'drop':>6}{'ann.diff':>10}{'t':>8}{'dt':>8}   {'yr diff':>9}")
    worst = (None, 1e9)
    for y in years:
        d = d0[d0.index.year != y]
        t = d.mean() / (d.std() / np.sqrt(len(d)))
        yd = (1 + r[r.index.year == y]).prod() - (1 + ctl[ctl.index.year == y]).prod()
        print(f"    {y:6d}{d.mean() * 252 * 100:+10.2f}{t:+8.2f}{t - t0:+8.2f}{yd * 100:+9.1f}")
        if t < worst[1]:
            worst = (y, t)
    print(f"  worst single year to delete: {worst[0]} -> t {worst[1]:+.2f} "
          f"(full-sample t {t0:+.2f}); "
          f"{'the effect does NOT survive it' if worst[1] < 2 else 'the effect survives it'}")
    return t0, worst


# ---------------------------------------------------------------- main
def main():
    print("=" * 150)
    print(f"Idea 89  one-year-leverage-audit (cloud) | {SCRIPT} | {COST_BPS} bps, weekly, "
          f"next-day execution")
    print("=" * 150)

    px = load_universe()                       # 56 names, crypto excluded by baseline
    pxb = load_universe(broad=True)
    px_all = load_universe(exclude=set())      # same 56 + BTC-USD/ETH-USD, for idea 15's arm

    # harness checks — the published rows must reproduce before any audit row is believed
    r2 = backtest(px, w_top20(px), cost_bps=COST_BPS, freq="W")["returns"].loc[px.index[260]:]
    c2, s2, d2 = m(r2)
    h1, h2 = halves(r2)
    print(f"harness: idea 2's KEEP reproduces as {c2:.1%}/{s2:.3f}/{d2:.1%} halves "
          f"{h1:.3f}/{h2:.3f}  (published 12.7%/1.093/-18.3%, halves 1.088/1.103)")
    rb = backtest(pxb, w_ewall(pxb), cost_bps=COST_BPS, freq="W")["returns"].loc[pxb.index[260]:]
    cb, sb, db = m(rb)
    hb1, hb2 = halves(rb)
    print(f"harness: idea 72's B136/EWall reproduces as {cb:.1%}/{sb:.3f}/{db:.1%} halves "
          f"{hb1:.3f}/{hb2:.3f}  (published 10.7%/1.027/-17.7%, halves 1.146/0.917)")
    # LOYO identity: dropping a year the book did not trade must change nothing
    rr = r2.copy()
    assert abs(m(drop_year(rr, 1990))[1] - m(rr)[1]) < 1e-12, "LOYO no-op check failed"
    print("harness: LOYO drop of an absent year is a no-op (identity holds)")

    rows = []
    # idea 15's PARKed crypto arm rides along on universe.json as the validation case
    wcx = w_ewall_crypto(px_all, px)
    rcx = backtest(px_all, wcx, cost_bps=COST_BPS, freq="W")["returns"]
    print(f"harness: idea 15's EWall/matched/same/c10 arm reproduces as "
          f"{m(rcx.loc[px_all.index[260]:])[0]:.1%}/{m(rcx.loc[px_all.index[260]:])[1]:.3f}"
          f"/{m(rcx.loc[px_all.index[260]:])[2]:.1%} (published 12.7%/1.13/-20.0% on broad; "
          f"u56 arm is the same construction on the 56-name list)")

    R56, T56, years56 = sweep(px, "universe.json (56)", rows,
                              extra={"EWall+c10": rcx.reindex(px.index).fillna(0.0)})
    loyo_difference(R56["EWall+c10"], R56["EWall"], years56,
                    "idea 15's EWall+crypto c10 (matched, same gate)", "its own EWall control")
    sweep(pxb, "universe_broad.json (136)", rows)

    df = pd.DataFrame(rows)
    df.to_csv(Path(__file__).with_suffix("").as_posix() + ".grid.csv", index=False)

    print(f"\n{'=' * 150}")
    print("CROSS-UNIVERSE SUMMARY — which published 4b passes survive the audit?")
    print("=" * 150)
    print(df[["tag", "book", "full4b", "loyo_pass", "n_years", "worst_year", "worst_sharpe",
              "full_sharpe", "best_year", "best_excess", "pass_wo_best"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    surv = df[(df.full4b) & (df.loyo_pass == df.n_years)]
    print(f"\nfull-sample 4b passes: {len(df[df.full4b])} of {len(df)} (book, universe) cells")
    print(f"LOYO-ROBUST 4b passes (survive dropping EVERY year): "
          f"{[(r.tag, r.book) for r in surv.itertuples()] or 'NONE'}")
    fragile = df[(df.full4b) & (df.loyo_pass < df.n_years)]
    for r in fragile.itertuples():
        print(f"  FRAGILE: {r.book} on {r.tag} — passes only {r.loyo_pass}/{r.n_years} LOYO "
              f"samples; best year {r.best_year} (+{r.best_excess:.1%} vs SPY)")


if __name__ == "__main__":
    main()
