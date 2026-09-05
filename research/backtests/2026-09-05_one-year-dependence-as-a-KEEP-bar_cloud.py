#!/usr/bin/env python3
"""QUEUE idea 98 — one-year-dependence-as-a-KEEP-bar (cloud, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 26's by-product passes 4b on both universes but its entire effect is 2022 (sleeve
contribution negative in 17/18 years). Run idea 89's leave-one-year-out harness on every standing
4b pass and report which survive deleting their single best year; propose a pre-registered bar."

WHY IT MATTERS
--------------
PROTOCOL 4b is a full-sample verdict.  If a book's whole edge over SPY is one bear market, 4b says
KEEP and the capital finds out later.  Idea 89 built the harness and ran it on 5 books; it also
found the thing that makes the naive version of this bar wrong — **12 of its 14 verdict flips were
the BAR moving, not the book weakening** (deleting 2020 raises SPY's 60%-of-MaxDD cap by 5.53pp).
So this run does not just count survivals: it decomposes every failure into book-side and bar-side,
and then asks whether any candidate bar actually SELECTS better books out of sample.

THE HARNESS (idea 89's, verbatim conventions)
----------------------------------------------
For every (book, universe, cost) cell and every calendar year y: delete every row of year y from
the book AND from SPY AND from RULES v1, chain-link the remainder, and recompute every statistic
AND every 4b bar on the retained days, so the benchmark moves with the sample.

BOOKS — every standing 4b pass the project has, each reconstructed from its own source script
   top20          idea 2   top-20 composite, 0.75/20 fixed (de-grosses when E_t<20). u56 4b KEEP.
   frac085        idea 46  top ceil(0.85 x E_t) at 0.75/k — always 75% gross.
   ew-band3       idea 57  equal-weight all eligible, 200d +/-3% band gate, 75%.
   ew-band3-g085  idea 84  the same at gross 0.85 (its 4b pass on BOTH universes).
   EWall          idea 72  equal-weight all eligible, 200d gate, 75%.  broad 4b KEEP.
   EWall+vol60dg  idea 94  ungated equal-weight, vol20<0.60 gate to CASH, no trend filter.
   top20+50S4     idea 99/101/114's rule-8 pick: 50/50 top20 and the S4 macro sleeve, re-grossed
                           to 1.00 (TLT, GLD, DBC, UUP; 60d inverse-vol x 3-horizon momentum vote).
   top20+50S3     idea 101 the same blend with DBC dropped (TLT, GLD, UUP). KEEP 4a+4b, both lists.
   v1             RULES v1, the live book — control, not a candidate.
Each book's published full-sample row is reproduced in the console before any audit number is used.

STATISTICS, DECLARED BEFORE ANY NUMBER IS COMPUTED
---------------------------------------------------
N_SURV   the number of the ~18 calendar years whose deletion leaves 4b still passing.
BEST_Y   the book's single best year = argmax over years of (book total return - SPY total return)
         in that calendar year.  Pre-registered as EXCESS, not raw: the queue's question is about
         the edge over SPY, which is what 4b prices.
SURV_BEST  does 4b still pass with BEST_Y deleted?  This is the queue's literal question.
WHO_MOVED  for every failing year, the book-side move (book Sharpe/CAGR/MaxDD ex-y minus full) and
         the bar-side move (SPY's H1/H2/OOS Sharpe, 0.60xMaxDD, 0.70xCAGR ex-y minus full).  A
         failure is BAR-SIDE if the bar moved further than the book on the binding constraint.

FOUR CANDIDATE BARS (all reported; none is adopted here — that is the Sunday review's call)
--------------------------------------------------------------------------------------------
   B0  status quo: full-sample 4b passes.
   B1  4b still passes with the book's own single best year deleted.        (the queue's proposal)
   B2  4b passes with EVERY single year deleted (N_SURV = all years).       (idea 89's strict form)
   B3  RELATIVE-ONLY 4b under B2: H1, H2 and OOS Sharpe beat SPY on the same retained days for
       every deleted year, with the two ABSOLUTE bars (0.60xMaxDD, 0.70xCAGR) checked on the full
       sample only — because idea 89 showed those two are the one-year-levered ones.

PRE-REGISTERED TEST OF THE BARS (the part that makes this more than bookkeeping)
---------------------------------------------------------------------------------
A bar is only worth adding if it SELECTS.  Each bar is applied using the IS window
(2009-2016) ALONE — the book's returns, SPY's bars and the LOYO deletions all restricted to IS —
and the books it admits are then evaluated on the UNTOUCHED 2017-2026 window.

   ADOPT bar X (recommend to the Sunday review) iff, at 10 bps,
       mean OOS Sharpe of X's admitted set  >=  mean OOS Sharpe of B0's admitted set + 0.05
       on BOTH universes, AND X admits at least one book on each.
   Otherwise REPORT-ONLY: the bar is a description of one-year dependence, not a selector.

TUNED (2, per PROTOCOL rule 4): the bar variant (4 levels) x the cost rung (10 / 25 bps).
ALL points are reported.  The books themselves are fixed by their source scripts — nothing about
any book is re-fitted here.

WALK-FORWARD (PROTOCOL rule 8, mandatory): the selection above IS the walk-forward — every bar is
applied on 2009-2016 only and judged on 2017-2026, and every book's OOS CAGR / Sharpe / MaxDD is
reported against RULES v1 and SPY, with both KEEP paths (4a beat-the-book, 4b capital-worthy).

CAVEATS
-------
SURVIVORSHIP: both equity panels are current constituents of their lists; levels are biased up.
  The bias is identical across every book, year and window compared here.
SPLICED SERIES: deleting a year and chain-linking leaves mean/std well defined; MaxDD on the
  chained curve is an APPROXIMATION (a drawdown spanning the deleted year is shortened).  This is
  idea 89's convention, kept so the two runs are comparable, and it is applied to the book and to
  SPY identically, so the 4b DD comparison stays like-for-like.
SELECTION n: 9 books x 2 universes is a small sample for judging a bar's selectivity.  The OOS
  comparison is reported with its per-book detail so the reader can see it is 2-4 books a side.
2009 and the final year are partial (the eval starts ~260 trading days in); both are flagged.

Deterministic, standalone (no network; reads the committed price caches):
    python research/backtests/2026-09-05_one-year-dependence-as-a-KEEP-bar_cloud.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
FRAC = 0.85
BAND = 0.03
FREQ = "W"
COSTS = (10, 25)
PRIMARY_BPS = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
S4 = ["TLT", "GLD", "DBC", "UUP"]
S3 = ["TLT", "GLD", "UUP"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
ADOPT_MARGIN = 0.05
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- signals (idea 89 verbatim)
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
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


# ---------------------------------------------------------------- the books
def w_top20(px):
    """idea 2's KEEP: top-20 at 0.75/20 each; de-grosses to cash when E_t < 20."""
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def w_frac085(px):
    """idea 46: top ceil(0.85 x E_t) at 0.75/k each — always 75% gross."""
    elig = eligible(px)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    k = np.ceil(FRAC * elig.sum(axis=1).astype(float)).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(GROSS / k, axis=0)


def _ewall(px, gate, gross=GROSS):
    e = eligible(px, gate).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * gross


def w_ewall(px):
    return _ewall(px, "200d")


def w_ewband3(px):
    return _ewall(px, "band3")


def w_ewband3_g085(px):
    return _ewall(px, "band3", gross=0.85)


def w_ewall_vol60dg(px):
    """idea 94's `EWall + vol60-dg`: ungated equal-weight at 0.75 gross, then every name failing
    vol20 < 0.60 is zeroed INTO CASH (the book de-grosses).  No trend filter at all."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    base = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    g = (vol20(px) < MAX_VOL).fillna(False)
    return base.where(g, 0.0)


def _book_regross(px):
    """The re-grossed top-20 used inside the sleeve blend (ideas 99/101/114's `book(...,'top20')`)."""
    s, _, _ = score(px, vol_scale=False)
    m = (px > px.rolling(200).mean()) & (vol20(px) < MAX_VOL)
    rank = s.where(m).rank(axis=1, ascending=False)
    w = (rank <= NPOS).astype(float)
    k = w.sum(axis=1)
    return w.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


def sleeve_weights(px, assets):
    sub = px[assets]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = (1.0 / vol.replace(0.0, np.nan))
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    w = (vote * rp).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


def _blend(px, assets):
    w = 0.5 * _book_regross(px) + 0.5 * sleeve_weights(px, assets)
    tot = w.sum(axis=1)
    return w.mul((1.00 / tot.where(tot > 1e-12)).fillna(0.0), axis=0)


def w_blend_S4(px):
    return _blend(px, S4)


def w_blend_S3(px):
    return _blend(px, S3)


BOOKS = {
    "v1":            rules_v1_weights,
    "top20":         w_top20,
    "frac085":       w_frac085,
    "ew-band3":      w_ewband3,
    "ew-band3-g085": w_ewband3_g085,
    "EWall":         w_ewall,
    "EWall+vol60dg": w_ewall_vol60dg,
    "top20+50S4":    w_blend_S4,
    "top20+50S3":    w_blend_S3,
}
CANDIDATES = [b for b in BOOKS if b != "v1"]     # v1 is the live book, a control not a candidate

PUBLISHED = {   # (book, universe) -> (CAGR, Sharpe, MaxDD) as printed on the leaderboard, 10 bps
    ("top20", "u56"):            (0.127, 1.093, -0.183),
    ("EWall", "broad"):          (0.107, 1.027, -0.177),
    ("ew-band3-g085", "u56"):    (0.128, 1.140, -0.171),
    ("ew-band3-g085", "broad"):  (0.126, 1.060, -0.189),
    ("EWall+vol60dg", "u56"):    (0.116, 1.130, -0.169),
    ("EWall+vol60dg", "broad"):  (0.124, 1.140, -0.187),
    ("top20+50S3", "u56"):       (0.115, 1.170, -0.133),
    ("top20+50S3", "broad"):     (0.120, 1.070, -0.146),
    ("top20+50S4", "u56"):       (0.123, 1.180, -0.143),
}


# ---------------------------------------------------------------- LOYO machinery (idea 89 verbatim)
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def drop_year(r, y):
    return r if y is None else r[r.index.year != y]


def stats(r, spy, oos_start=OOS_START, absolute=True):
    """Everything a 4b verdict needs, for a book and its benchmark on the SAME retained days."""
    c, s, dd = m3(r)
    h1, h2 = halves(r)
    ro = r.loc[oos_start:]
    oos = m3(ro)[1] if len(ro) >= 60 else np.nan
    sc, ss, sdd = m3(spy)
    s1, s2 = halves(spy)
    so = spy.loc[oos_start:]
    soos = m3(so)[1] if len(so) >= 60 else np.nan
    bad = []
    if not (h1 > s1): bad.append("H1")
    if not (h2 > s2): bad.append("H2")
    if not (oos > soos): bad.append("OOS")
    if absolute:
        if dd < 0.60 * sdd: bad.append("DD")
        if c < 0.70 * sc: bad.append("CAGR")
    return dict(cagr=c, sharpe=s, dd=dd, h1=h1, h2=h2, oos=oos,
                pass4b=(len(bad) == 0), bad=",".join(bad) if bad else "-",
                bar_H1=s1, bar_H2=s2, bar_OOS=soos, bar_DD=0.60 * sdd, bar_CAGR=0.70 * sc,
                mrg_H1=h1 - s1, mrg_H2=h2 - s2, mrg_OOS=oos - soos,
                mrg_DD=(dd - 0.60 * sdd) * 100, mrg_CAGR=(c - 0.70 * sc) * 100)


def keep_4a(bk, base):
    return bool(bk["h1"] > base["h1"] and bk["h2"] > base["h2"] and bk["dd"] >= base["dd"])


def tot_ret(r, y):
    s = r[r.index.year == y]
    return float((1 + s).prod() - 1) if len(s) else np.nan


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- one universe
def sweep(px, tag, bps, allrows, loyorows, verbose):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    years = sorted(set(spy.index.year))
    partial = {years[0], years[-1]}
    sc, ss, sdd = m3(spy)
    if verbose:
        print("\n" + "=" * 150)
        print(f"### {tag} @ {bps} bps: {px.shape[1]} tickers, eval {start.date()} -> "
              f"{px.index[-1].date()}, years {years[0]}-{years[-1]} "
              f"(partial: {sorted(partial)})")
        print(f"### SPY full sample {sc:.1%} / {ss:.3f} / {sdd:.1%}   "
              f"halves {halves(spy)[0]:.3f}/{halves(spy)[1]:.3f}   OOS {m3(spy.loc[OOS_START:])[1]:.3f}")
        print("=" * 150)

    R = {}
    for bk, fn in BOOKS.items():
        res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
        gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
        R[bk] = gr - to * bps / 1e4

    base = stats(R["v1"], spy)
    for bk in BOOKS:
        st = stats(R[bk], spy)
        pub = PUBLISHED.get((bk, tag.split()[0]))
        allrows.append(dict(universe=tag.split()[0], cost_bps=bps, book=bk, **st,
                            keep_4a=keep_4a(st, base),
                            published=("%.1f%%/%.3f/%.1f%%" % (pub[0] * 100, pub[1], pub[2] * 100))
                            if pub else ""))

    if verbose:
        A = pd.DataFrame([r for r in allrows if r["universe"] == tag.split()[0]
                          and r["cost_bps"] == bps]).set_index("book")
        print("\n--- FULL-SAMPLE ROWS (published values quoted where the leaderboard has one)")
        print(fmt(A[["cagr", "sharpe", "dd", "h1", "h2", "oos", "pass4b", "bad",
                     "keep_4a", "published"]]))

    # ---- the LOYO sweep
    for bk in BOOKS:
        r = R[bk]
        full = stats(r, spy)
        exc = {y: tot_ret(r, y) - tot_ret(spy, y) for y in years}
        best_y = int(max(exc, key=lambda y: (exc[y] if np.isfinite(exc[y]) else -9e9)))
        for y in [None] + years:
            st = stats(drop_year(r, y), drop_year(spy, y))
            st_rel = stats(drop_year(r, y), drop_year(spy, y), absolute=False)
            loyorows.append(dict(universe=tag.split()[0], cost_bps=bps, book=bk,
                                 dropped=("full" if y is None else y),
                                 is_partial=(y in partial), is_best=(y == best_y),
                                 best_year=best_y, excess_best=exc[best_y],
                                 excess=(np.nan if y is None else exc[y]),
                                 pass4b=st["pass4b"], bad=st["bad"],
                                 pass4b_rel=st_rel["pass4b"], bad_rel=st_rel["bad"],
                                 sharpe=st["sharpe"], cagr=st["cagr"], dd=st["dd"],
                                 h1=st["h1"], h2=st["h2"], oos=st["oos"],
                                 bar_H1=st["bar_H1"], bar_H2=st["bar_H2"], bar_OOS=st["bar_OOS"],
                                 bar_DD=st["bar_DD"], bar_CAGR=st["bar_CAGR"],
                                 mrg_H1=st["mrg_H1"], mrg_H2=st["mrg_H2"], mrg_OOS=st["mrg_OOS"],
                                 mrg_DD=st["mrg_DD"], mrg_CAGR=st["mrg_CAGR"],
                                 d_sharpe=st["sharpe"] - full["sharpe"],
                                 d_cagr=st["cagr"] - full["cagr"], d_dd=st["dd"] - full["dd"],
                                 d_bar_DD=st["bar_DD"] - full["bar_DD"],
                                 d_bar_CAGR=st["bar_CAGR"] - full["bar_CAGR"],
                                 d_bar_H2=st["bar_H2"] - full["bar_H2"]))
    return R, spy, years


# ---------------------------------------------------------------- IS-only bar application (rule 8)
def is_only_bars(px, tag, bps):
    """Apply every candidate bar using 2009..2016 ALONE, then report the untouched OOS numbers.
    Inside IS there is no OOS sub-window, so the IS form of 4b is: H1 > SPY H1, H2 > SPY H2 (the
    halves OF THE IS WINDOW), MaxDD >= 0.60 x SPY, CAGR >= 0.70 x SPY — checked on the IS days,
    and for B1/B2/B3 additionally with each IS year deleted."""
    start = px.index[260]
    spy_all = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is = spy_all.loc[:IS_END]
    is_years = sorted(set(spy_is.index.year))
    out = []
    for bk, fn in BOOKS.items():
        res = backtest(px, fn(px), cost_bps=0.0, freq=FREQ)
        gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
        r_all = gr - to * bps / 1e4
        r_is = r_all.loc[:IS_END]

        def st_is(y=None, absolute=True):
            a, b = drop_year(r_is, y), drop_year(spy_is, y)
            c, s, dd = m3(a)
            h1, h2 = halves(a)
            sc, ss, sdd = m3(b)
            s1, s2 = halves(b)
            bad = []
            if not (h1 > s1): bad.append("H1")
            if not (h2 > s2): bad.append("H2")
            if absolute:
                if dd < 0.60 * sdd: bad.append("DD")
                if c < 0.70 * sc: bad.append("CAGR")
            return (len(bad) == 0), ",".join(bad) if bad else "-"

        b0, b0bad = st_is()
        exc = {y: tot_ret(r_is, y) - tot_ret(spy_is, y) for y in is_years}
        best_y = int(max(exc, key=lambda y: (exc[y] if np.isfinite(exc[y]) else -9e9)))
        b1 = b0 and st_is(best_y)[0]
        b2 = b0 and all(st_is(y)[0] for y in is_years)
        b3 = b0 and all(st_is(y, absolute=False)[0] for y in is_years)

        ro, so = r_all.loc[OOS_START:], spy_all.loc[OOS_START:]
        oc, os_, odd = m3(ro)
        sc2, ss2, sdd2 = m3(so)
        out.append(dict(universe=tag, cost_bps=bps, book=bk, IS_best_year=best_y,
                        IS_excess_best=exc[best_y],
                        B0=b0, B0_bad=b0bad, B1=b1, B2=b2, B3=b3,
                        OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                        SPY_OOS_CAGR=sc2, SPY_OOS_Sharpe=ss2, SPY_OOS_MaxDD=sdd2,
                        OOS_beats_SPY=bool(os_ > ss2)))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    print("=" * 150)
    print("Idea 98  one-year-dependence-as-a-KEEP-bar (cloud, 2026-09-05) | weekly, next-day, 10 and 25 bps")
    print("PRE-REGISTERED: N_SURV, BEST_Y (max excess over SPY), SURV_BEST, WHO_MOVED;")
    print("                bars B0 status-quo / B1 ex-best-year / B2 every-year / B3 relative-only;")
    print(f"                ADOPT a bar iff its IS-admitted set beats B0's by >= {ADOPT_MARGIN} mean OOS")
    print("                Sharpe on BOTH universes at 10 bps and admits >= 1 book on each.")
    print("=" * 150)

    u56 = load_universe()
    broad = load_universe(broad=True)
    for tag, px in (("u56", u56), ("broad", broad)):
        yrs = px.index.to_series().groupby(px.index.year).count()
        print(f"[index] {tag}: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows "
              f"({'trading-day' if yrs.loc[2015:2024].max() < 300 else 'CALENDAR-DAY — idea 38 unresolved'})")

    # LOYO identity check
    rt = backtest(u56, w_top20(u56), cost_bps=10, freq=FREQ)["returns"].loc[u56.index[260]:]
    assert abs(m3(drop_year(rt, 1990))[1] - m3(rt)[1]) < 1e-12
    print("[check] LOYO drop of an absent year is a no-op (identity holds)")

    allrows, loyorows = [], []
    for bps in COSTS:
        for tag, px in (("u56 (universe.json)", u56), ("broad (universe_broad.json)", broad)):
            sweep(px, tag, bps, allrows, loyorows, verbose=(bps == PRIMARY_BPS))

    A = pd.DataFrame(allrows)
    L = pd.DataFrame(loyorows)
    A.to_csv(OUT.with_suffix(".full.csv"), index=False)
    L.to_csv(OUT.with_suffix(".loyo.csv"), index=False)

    # ============================================================ (1) survival table
    print("\n" + "=" * 150)
    print("### (1) LEAVE-ONE-YEAR-OUT SURVIVAL OF EVERY STANDING 4b PASS")
    print("###     (book, SPY and the 4b bars all recomputed on the retained days)\n")
    surv = []
    for (uni, bps, bk), sub in L.groupby(["universe", "cost_bps", "book"], sort=False):
        f = sub[sub.dropped == "full"].iloc[0]
        ys = sub[sub.dropped != "full"]
        best = ys[ys.is_best].iloc[0]
        surv.append(dict(universe=uni, cost_bps=bps, book=bk,
                         full_4b=bool(f.pass4b), full_bad=f.bad,
                         n_years=len(ys), n_surv=int(ys.pass4b.sum()),
                         n_surv_rel=int(ys.pass4b_rel.sum()),
                         best_year=int(f.best_year), excess_best=f.excess_best,
                         surv_best=bool(best.pass4b), bad_best=best.bad,
                         worst_dSharpe=float(ys.d_sharpe.min()),
                         fails=",".join(str(int(y)) for y in ys[~ys.pass4b].dropped)))
    S = pd.DataFrame(surv)
    S.to_csv(OUT.with_suffix(".survival.csv"), index=False)
    for bps in COSTS:
        print(f"--- {bps} bps")
        print(fmt(S[S.cost_bps == bps].set_index(["universe", "book"]).drop(columns="cost_bps")))
        print()

    # ============================================================ (2) the queue's literal question
    print("=" * 150)
    print("### (2) THE QUEUE'S QUESTION — WHICH STANDING 4b PASSES SURVIVE DELETING THEIR BEST YEAR?\n")
    q = S[(S.cost_bps == PRIMARY_BPS) & (S.full_4b) & (S.book != "v1")]
    print(fmt(q.set_index(["universe", "book"])[["best_year", "excess_best", "surv_best",
                                                 "bad_best", "n_surv", "n_years"]]))
    print(f"\n  {int(q.surv_best.sum())} of {len(q)} full-sample 4b passes survive deleting their own best year "
          f"(10 bps, both universes).")
    print(f"  best years chosen: {sorted(set(q.best_year))}; "
          f"mean excess in the best year {q.excess_best.mean():.1%}")

    # ============================================================ (3) who moved: book or bar
    print("\n" + "=" * 150)
    print("### (3) WHO MOVED — EVERY FAILING YEAR DECOMPOSED INTO BOOK-SIDE AND BAR-SIDE\n")
    fails = L[(L.dropped != "full") & (~L.pass4b) & (L.book != "v1") & (L.cost_bps == PRIMARY_BPS)]
    fl = []
    for _, r in fails.iterrows():
        full = L[(L.universe == r.universe) & (L.cost_bps == r.cost_bps) &
                 (L.book == r.book) & (L.dropped == "full")].iloc[0]
        if not full.pass4b:
            continue                       # only price flips away from a passing full-sample row
        binding = r.bad.split(",")[0]
        book_move = {"H1": r.h1 - full.h1, "H2": r.h2 - full.h2, "OOS": r.oos - full.oos,
                     "DD": (r.dd - full.dd) * 100, "CAGR": (r.cagr - full.cagr) * 100}[binding]
        bar_move = {"H1": r.bar_H1 - full.bar_H1, "H2": r.bar_H2 - full.bar_H2,
                    "OOS": r.bar_OOS - full.bar_OOS, "DD": (r.bar_DD - full.bar_DD) * 100,
                    "CAGR": (r.bar_CAGR - full.bar_CAGR) * 100}[binding]
        fl.append(dict(universe=r.universe, book=r.book, dropped=r.dropped, binding=binding,
                       book_move=book_move, bar_move=bar_move,
                       side=("BAR" if abs(bar_move) > abs(book_move) else "BOOK")))
    F = pd.DataFrame(fl)
    F.to_csv(OUT.with_suffix(".whomoved.csv"), index=False)
    if len(F):
        print(fmt(F.set_index(["universe", "book", "dropped"])))
        print(f"\n  {int((F.side == 'BAR').sum())} of {len(F)} verdict flips are the BAR moving, "
              f"not the book weakening (idea 89 reported 12 of 14).")
        print(fmt(F.groupby(["binding", "side"]).size().unstack(fill_value=0)))
    else:
        print("  no full-sample 4b pass flips under any single-year deletion")

    # ============================================================ (4) the four bars, IS-only (rule 8)
    print("\n" + "=" * 150)
    print("### (4) PROTOCOL RULE 8 WALK-FORWARD — EVERY BAR APPLIED ON 2009-2016 ALONE,")
    print("###     THE ADMITTED BOOKS THEN EVALUATED ON THE UNTOUCHED 2017-2026 WINDOW\n")
    W = pd.concat([is_only_bars(px, tag, bps)
                   for bps in COSTS
                   for tag, px in (("u56", u56), ("broad", broad))], ignore_index=True)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(fmt(W[W.cost_bps == PRIMARY_BPS].set_index(["universe", "book"])[
        ["IS_best_year", "IS_excess_best", "B0", "B0_bad", "B1", "B2", "B3",
         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "SPY_OOS_Sharpe", "OOS_beats_SPY"]]))

    print("\n--- ADMITTED SETS AND THEIR OOS PERFORMANCE (candidates only; v1 excluded)")
    sel = []
    for bps in COSTS:
        for uni in ("u56", "broad"):
            sub = W[(W.cost_bps == bps) & (W.universe == uni) & (W.book.isin(CANDIDATES))]
            for bar in ("B0", "B1", "B2", "B3"):
                adm = sub[sub[bar]]
                sel.append(dict(cost_bps=bps, universe=uni, bar=bar, n_admitted=len(adm),
                                books=",".join(adm.book),
                                mean_OOS_Sharpe=adm.OOS_Sharpe.mean() if len(adm) else np.nan,
                                mean_OOS_CAGR=adm.OOS_CAGR.mean() if len(adm) else np.nan,
                                mean_OOS_MaxDD=adm.OOS_MaxDD.mean() if len(adm) else np.nan,
                                frac_beat_SPY=adm.OOS_beats_SPY.mean() if len(adm) else np.nan))
    SEL = pd.DataFrame(sel)
    SEL.to_csv(OUT.with_suffix(".selection.csv"), index=False)
    for bps in COSTS:
        print(f"\n--- {bps} bps")
        print(fmt(SEL[SEL.cost_bps == bps].set_index(["universe", "bar"]).drop(columns="cost_bps")))

    print("\n--- PRE-REGISTERED ADOPTION TEST (10 bps)")
    verdicts = {}
    p10 = SEL[SEL.cost_bps == PRIMARY_BPS].set_index(["universe", "bar"])
    for bar in ("B1", "B2", "B3"):
        ok, detail = True, []
        for uni in ("u56", "broad"):
            b0 = p10.loc[(uni, "B0")]
            bx = p10.loc[(uni, bar)]
            gain = (bx.mean_OOS_Sharpe - b0.mean_OOS_Sharpe) if bx.n_admitted else np.nan
            detail.append(f"{uni}: n {int(bx.n_admitted)} vs B0 {int(b0.n_admitted)}, "
                          f"mean OOS Sharpe {bx.mean_OOS_Sharpe:.3f} vs {b0.mean_OOS_Sharpe:.3f} "
                          f"({gain:+.3f})")
            if not (bx.n_admitted >= 1 and np.isfinite(gain) and gain >= ADOPT_MARGIN):
                ok = False
        verdicts[bar] = ok
        print(f"  {bar}: {'ADOPT' if ok else 'REPORT-ONLY'}   " + " | ".join(detail))

    # ============================================================ (5) both KEEP paths, full sample
    print("\n" + "=" * 150)
    print("### (5) BOTH KEEP PATHS ON THE FULL SAMPLE, 10 AND 25 bps (4a beat-the-book, 4b capital-worthy)\n")
    print(fmt(A.set_index(["universe", "cost_bps", "book"])[
        ["cagr", "sharpe", "dd", "h1", "h2", "oos", "keep_4a", "pass4b", "bad"]]))

    # ============================================================ (6) verdict
    print("\n" + "=" * 150)
    print("### (6) VERDICT\n")
    print(f"  standing 4b passes audited : {len(q)} (10 bps, both universes)")
    print(f"  survive deleting best year : {int(q.surv_best.sum())}/{len(q)}  "
          f"(B1 — the queue's proposed bar)")
    b2n = int((S[(S.cost_bps == PRIMARY_BPS) & S.full_4b & (S.book != 'v1')].n_surv ==
               S[(S.cost_bps == PRIMARY_BPS) & S.full_4b & (S.book != 'v1')].n_years).sum())
    print(f"  survive EVERY year deleted : {b2n}/{len(q)}  (B2)")
    if len(F):
        print(f"  flips that are the BAR      : {int((F.side=='BAR').sum())}/{len(F)}")
    for bar, ok in verdicts.items():
        print(f"  bar {bar} as a SELECTOR      : {'ADOPT' if ok else 'REPORT-ONLY'}")
    print(f"\n[outputs] {OUT.name}.full.csv .loyo.csv .survival.csv .whomoved.csv "
          f".walkforward.csv .selection.csv")


if __name__ == "__main__":
    main()
