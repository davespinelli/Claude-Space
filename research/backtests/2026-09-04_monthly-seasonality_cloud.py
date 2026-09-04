#!/usr/bin/env python3
"""QUEUE idea 16 — monthly-seasonality (cloud lane, 2026-09-04).

Question
--------
"RULES v1 with exposure reduced in historically weak months."  The QUEUE expects a KILL.
The point of running it is not to see whether one particular month-mask happens to help
on this sample -- with 12 months and a free exposure multiplier something always will --
but to answer the prior question honestly:

    Is calendar month a *stable* property of these return series at all?

So the run is built as a signal test first and a book test second:

  Step 1 (no book, no parameters).  Mean daily return by calendar month, with t-stats,
         for SPY and for each of the three candidate books, computed on the FULL sample
         and on each half separately.  Then the decisive statistic: the rank correlation
         between the H1 month ordering and the H2 month ordering.  If a "weak month" is
         not the same month in the two halves, no rule built on it can be traded, and
         every grid point below is noise by construction.

  Step 2 (the literal idea).  Scale each book's gross by f during the k historically
         weakest months, 1.0 otherwise.  Weak months are picked ONLY from in-sample data
         (rule 8: 2009-2016), never from the full sample, so the rule is implementable.
         Also reported: the two textbook fixed masks that require no fitting at all --
         `sellinmay` (May-Oct) and `sep` (September only) -- because a pre-registered
         mask is the only version of this idea with no selection freedom.

Design (PROTOCOL rules 1-8)
---------------------------
Universes: research/universe.json (56 names) PRIMARY, universe_broad.json (136) as the
           portability check.  Both are current constituents -- SURVIVORSHIP: absolute
           CAGRs are optimistic.  The month-vs-month comparison is far less exposed since
           every arm holds the same names on the same days.
Books    : `v1`   = live RULES v1 (top-5, /sqrt(vol20), 15% each)  [the QUEUE's literal ask]
           `top20`= idea 2's standing 4b KEEP (top-20 by composite, no vol scaler, 75% gross)
           `EWall`= equal-weight all eligible names at 75% gross (idea 28/72's book)
Params   : exactly 2 -- the mask m in {sellinmay, sep, worst1, worst2, worst3, worst6}
           and the weak-month exposure f in {0.00, 0.25, 0.50, 0.75}.  ALL 24 grid points
           are printed for every (universe, book); f=1.00 is the control.
Execution: weekly rebalance, weights at close t applied at t+1, 10 bps per unit turnover.
           The mask multiplies the target weights, so a month change is itself a trade and
           pays cost -- that is the honest accounting and it is where this idea dies.
Rule 8   : `worst*` masks are fitted on 2009-2016 only; (mask, f) is then selected on
           2009-2016 IS Sharpe and evaluated untouched on 2017-2026.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST, FREQ, GROSS, MAX_VOL = 10, "W", 0.75, 0.60
FS = [0.00, 0.25, 0.50, 0.75, 1.00]           # 1.00 is the control, not a grid point
MASKS = ["sellinmay", "sep", "worst1", "worst2", "worst3", "worst6"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SCRIPT = "research/backtests/2026-09-04_monthly-seasonality_cloud.py"
MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# ------------------------------------------------------------------ construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def eligible(px):
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (px > px.rolling(200).mean()) & (v < MAX_VOL)


def w_v1(px):
    return rules_v1_weights(px)


def w_top20(px):
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= 20).astype(float) * (GROSS / 20)


def w_ewall(px):
    e = eligible(px).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": w_v1, "top20": w_top20, "EWall": w_ewall}


def scaled(base_fn, months, f):
    """base book with gross multiplied by f on days whose calendar month is in `months`."""
    def g(px):
        w = base_fn(px)
        mult = pd.Series(np.where(px.index.month.isin(months), f, 1.0), index=px.index)
        return w.mul(mult, axis=0)
    return g


# ------------------------------------------------------------------ metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy):
    """PROTOCOL 4b, incl. rule-8 OOS Sharpe. Returns list of failing bars ([] = pass)."""
    c, s, dd = m(r); h1, h2 = halves(r)
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    o, so = metrics(r.loc[OOS_START:])["Sharpe"], metrics(spy.loc[OOS_START:])["Sharpe"]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if o <= so: bad.append("OOS")
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


def run(px, fn, start):
    res = backtest(px, fn(px), cost_bps=COST, freq=FREQ)
    r = res["returns"].loc[start:]
    return r, res["turnover"].loc[start:].sum() / (len(r) / 252)


# ------------------------------------------------------------------ step 1: the signal
def month_table(r, label):
    """mean daily return by calendar month with t-stats, full sample and both halves."""
    h = len(r) // 2
    r1, r2 = r.iloc[:h], r.iloc[h:]
    out = {}
    for tag, s in (("full", r), ("H1", r1), ("H2", r2)):
        g = s.groupby(s.index.month)
        out[tag] = pd.DataFrame({"mean_bp": g.mean() * 1e4, "t": g.mean() / g.std() * np.sqrt(g.count())})
    print(f"\n  --- {label}: mean daily return by month (bp) and t-stat ---")
    print("    month  " + "".join(f"{n:>8}" for n in MN))
    for tag in ("full", "H1", "H2"):
        d = out[tag]
        print(f"    {tag:<5}bp" + "".join(f"{d['mean_bp'].get(i, np.nan):8.2f}" for i in range(1, 13)))
        print(f"    {tag:<5}t " + "".join(f"{d['t'].get(i, np.nan):8.2f}" for i in range(1, 13)))
    a, b = out["H1"]["mean_bp"], out["H2"]["mean_bp"]
    common = a.index.intersection(b.index)
    rho = a[common].rank().corr(b[common].rank())          # Spearman without scipy
    isr = out["full"]["mean_bp"].reindex(range(1, 13))
    print(f"    Spearman(H1 month means, H2 month means) = {rho:+.3f}   "
          f"worst-3 full sample: {[MN[i-1] for i in isr.nsmallest(3).index]}")
    return out, rho


def worst_months(r, k, end=IS_END):
    """the k calendar months with the lowest mean daily return, using data up to `end` only."""
    s = r.loc[:end]
    return sorted(s.groupby(s.index.month).mean().nsmallest(k).index.tolist())


def mask_months(name, r_is):
    if name == "sellinmay": return [5, 6, 7, 8, 9, 10]
    if name == "sep": return [9]
    return worst_months(r_is, int(name.replace("worst", "")))


# ------------------------------------------------------------------ one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    sso = metrics(spy.loc[OOS_START:])["Sharpe"]
    base, _ = run(px, w_v1, start)

    print("\n" + "=" * 130)
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}")
    print(f"SPY  CAGR {sc:.1%}  Sharpe {ss:.3f}  MaxDD {sdd:.1%}  halves {s1:.3f}/{s2:.3f}  OOS {sso:.3f}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{sso:.3f}  MaxDD>={0.60*sdd:.1%}  CAGR>={0.70*sc:.1%}")
    print("=" * 130)

    # ---- step 1: is there a month effect to trade?
    print("\nSTEP 1 -- month effect as a raw statistic (no book parameters).")
    controls, rhos = {}, {}
    _, rhos["SPY"] = month_table(spy, "SPY")
    for bk, fn in BOOKS.items():
        r, tn = run(px, fn, start)
        controls[bk] = (r, tn)
        _, rhos[bk] = month_table(r, f"{bk} (control, f=1.00)")
    print(f"\n  Cross-half stability of the month ordering ({tag}): "
          + "  ".join(f"{k} {v:+.3f}" for k, v in rhos.items()))

    # ---- step 2: the literal idea
    print(f"\nSTEP 2 -- exposure scaling grid. All {len(MASKS)*(len(FS)-1)} points per book "
          f"plus the f=1.00 control.\n")
    rows = []
    for bk, fn in BOOKS.items():
        r0, tn0 = controls[bk]
        c0, sh0, dd0 = m(r0); a0, b0 = halves(r0)
        o0 = metrics(r0.loc[OOS_START:])["Sharpe"]
        r_is = r0.loc[:IS_END]
        print(f"  [{tag} / {bk}]  control f=1.00: CAGR {c0:.1%}  Sharpe {sh0:.3f}  MaxDD {dd0:.1%}  "
              f"halves {a0:.3f}/{b0:.3f}  OOS {o0:.3f}  turnover {tn0:.1f}x  "
              f"4a:{fail4a(r0, base) or 'PASS'}  4b:{fail4b(r0, spy) or 'PASS'}")
        print(f"  {'mask':<10}{'months':<26}{'f':>5}{'CAGR':>8}{'Sharpe':>8}{'dSh':>7}"
              f"{'MaxDD':>8}{'H1':>7}{'H2':>7}{'OOS':>7}{'turn':>7}  {'4a':<10}{'4b'}")
        for mk in MASKS:
            mo = mask_months(mk, r_is)
            for f in FS[:-1]:
                r, tn = run(px, scaled(fn, mo, f), start)
                c, sh, dd = m(r); h1, h2 = halves(r)
                o = metrics(r.loc[OOS_START:])["Sharpe"]
                A, B = fail4a(r, base), fail4b(r, spy)
                print(f"  {mk:<10}{str([MN[i-1] for i in mo]):<26}{f:5.2f}{c:8.1%}{sh:8.3f}"
                      f"{sh-sh0:+7.3f}{dd:8.1%}{h1:7.3f}{h2:7.3f}{o:7.3f}{tn:7.1f}  "
                      f"{','.join(A) or 'PASS':<10}{','.join(B) or 'PASS'}")
                rows.append(dict(universe=tag, book=bk, mask=mk, months=str(mo), f=f,
                                 CAGR=c, Sharpe=sh, dSharpe=sh - sh0, MaxDD=dd, H1=h1, H2=h2,
                                 OOS=o, turn=tn, pass4a=not A, pass4b=not B,
                                 IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"]))
            print()
        rows.append(dict(universe=tag, book=bk, mask="none", months="[]", f=1.00,
                         CAGR=c0, Sharpe=sh0, dSharpe=0.0, MaxDD=dd0, H1=a0, H2=b0, OOS=o0,
                         turn=tn0, pass4a=not fail4a(r0, base), pass4b=not fail4b(r0, spy),
                         IS_Sharpe=metrics(r_is)["Sharpe"]))
    return pd.DataFrame(rows), dict(spy=(sc, ss, sdd, s1, s2, sso), base=m(base), rhos=rhos)


# ------------------------------------------------------------------ rule 8
def walk_forward(df, tag):
    print(f"\n{'-'*130}\nRULE 8 walk-forward ({tag}): (mask, f) chosen on 2009-{IS_END[:4]} IS Sharpe, "
          f"evaluated untouched on {OOS_START[:4]}-2026.\n")
    print(f"  {'book':<8}{'IS pick':<28}{'IS Sh':>8}{'OOS Sh':>8}{'ctrl OOS':>10}{'delta':>8}   4b(full)")
    won = 0
    for bk in BOOKS:
        d = df[df.book == bk]
        pick = d.loc[d.IS_Sharpe.idxmax()]
        ctrl = d[d["mask"] == "none"].iloc[0]
        delta = pick.OOS - ctrl.OOS
        won += delta > 0
        print(f"  {bk:<8}{pick['mask'] + ' f=' + f'{pick.f:.2f}':<28}{pick.IS_Sharpe:8.3f}"
              f"{pick.OOS:8.3f}{ctrl.OOS:10.3f}{delta:+8.3f}   {'PASS' if pick.pass4b else 'FAIL'}")
    print(f"\n  Selection beats its own control out of sample in {won} of {len(BOOKS)} books.")


# ------------------------------------------------------------------ main
def main():
    all_rows, meta = [], {}
    for tag, kw in (("universe.json", {}), ("universe_broad.json", {"broad": True})):
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            sys.exit("!! CALENDAR-DAY INDEX DETECTED (idea 38) -- aborting.")
        df, mt = sweep(px, tag)
        walk_forward(df, tag)
        all_rows.append(df); meta[tag] = mt
    out = pd.concat(all_rows, ignore_index=True)
    out.to_csv(ROOT / "research" / "backtests" / "2026-09-04_monthly-seasonality_cloud.grid.csv", index=False)

    print("\n" + "=" * 130)
    print("SUMMARY")
    print("=" * 130)
    g = out[out["mask"] != "none"]
    print(f"  grid points (excl. controls): {len(g)}   improving on own control (dSharpe>0): "
          f"{(g.dSharpe > 0).sum()} ({(g.dSharpe > 0).mean():.1%})")
    print(f"  4b passes among scaled arms: {int(g.pass4b.sum())} / {len(g)};  "
          f"among controls: {int(out[out['mask']=='none'].pass4b.sum())} / {(out['mask']=='none').sum()}")
    cu = g.groupby(["book", "mask", "f"]).pass4b.sum()
    print(f"  arms passing 4b on BOTH universes: {int((cu == 2).sum())}")
    print("\n  Best dSharpe per (universe, book):")
    for (u, b), d in g.groupby(["universe", "book"]):
        r = d.loc[d.dSharpe.idxmax()]
        print(f"    {u:<20}{b:<8}{r['mask']:<10}f={r.f:.2f}  dSharpe {r.dSharpe:+.3f}  "
              f"4b {'PASS' if r.pass4b else ','.join([])+'FAIL'}")
    print("\n  Cross-half stability of the month ordering (the load-bearing number):")
    for tag, mt in meta.items():
        print(f"    {tag:<20}" + "  ".join(f"{k} {v:+.3f}" for k, v in mt["rhos"].items()))


if __name__ == "__main__":
    main()
