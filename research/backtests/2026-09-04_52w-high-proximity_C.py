#!/usr/bin/env python3
"""Idea 13 - "52w-high-proximity": rank by closeness to the 52-week high instead of by returns.

The question
------------
George & Hwang (2004) argue the nearness of a stock's price to its 52-week high predicts
returns better than past return itself, because investors anchor on the high and under-react
to news that would push the price through it.  RULES v1 ranks on a return composite
(12-1 + 6m + 3m percentile ranks); this run replaces that ranking signal with

    PROX_t = P_t / max(P_{t-251..t})            (1.0 = sitting at its 52-week high)

and keeps everything else identical, so the only thing that changes is the ranking key.

Why it is worth a run beyond the citation
    (a) PROX is a *level* statistic, not a difference, so it is far slower-moving than a
        12-1 momentum rank.  Ideas 55/57/4/3/9 all found the same thing on this repo -
        in the ew-all book, net Sharpe orders by flip rate and slower is better - so a
        slower ranking key is exactly the kind of instrument the project's own evidence
        says to try.  Turnover is reported for every point.
    (b) It is a genuine alternative to the incumbent composite rather than a tweak of it,
        which is what idea 8 (lookback-blend) could not supply: idea 8 varied the horizon
        of the same return signal and the walk-forward could not tell the variants apart
        (Spearman(IS,OOS) = +0.000 on universe.json).

Books - structural variants, all reported, none picked on its own result
    v1     RULES v1 exactly as live: top 5 eligible by the composite WITH /sqrt(vol20),
           15% each.  One row per universe (the live book, for 4a).
    CAND   idea 2's standing 4b KEEP construction: top-n eligible EQUAL-WEIGHT at 75%
           gross, no vol scaler.  This is the book the ranking key is swapped inside.
    EWall  equal-weight ALL eligible names at 75% gross, no ranking at all.  The project's
           standard "is the ranking doing anything" control.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. signal in {COMP, PROX, BLEND}   - COMP is the incumbent composite (control), PROX is
       the idea as queried, BLEND is the equal average of the two cross-sectional percentile
       ranks (the pre-registered "both" arm).
    2. n in {5, 10, 20, 30} for the CAND construction.
The 52-week window is 252 trading days - George & Hwang's own definition, NOT a tuned
choice, and no other window is tried.  The 200d / vol20 < 0.60 eligibility gate, 75% gross,
weekly rebalancing, 10 bps costs and next-day execution are RULES v1's own and are held
fixed everywhere.

Grid = 2 universes x (1 v1 + 1 EWall + 3 signals x 4 n) = 28 points, ALL reported.

Diagnostics that do not depend on any verdict
    - Weekly rank IC of each signal against the following week's return, full sample and by
      half, with t-stats: does PROX carry information at all on this panel?
    - Mean cross-sectional Spearman between PROX and COMP ranks: is this a different signal
      or a re-labelling of the same one?
    - Held-name overlap and flip rate (ranking-key changes per ticker per year).
    - Paired daily t of PROX vs COMP at matched n and matched days.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number was read
    S1 (Sharpe):   over the 12 CAND (signal, n) points, the one with the highest 2009-2016
                   Sharpe; ties -> COMP, then smaller n.
    S2 (4b-aware): the same, restricted to points whose in-sample MaxDD is within 60% of
                   SPY's in-sample MaxDD.  "none" if nothing qualifies.
    Also reported: the best signal within each n, so the signal choice can be audited
    separately from the position-count choice.
Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Harness sanity: the script reproduces idea 2's published KEEP row (universe.json / CAND /
COMP / n=20 -> 12.7% / 1.093 / -18.3%, halves 1.088/1.103) and the live RULES v1 row before
any new number is reported.

Survivorship: current constituents of both lists, one-directional.  It bites this run in a
specific direction worth stating: names that spent years far below a 52-week high and then
delisted are absent, so a signal that *avoids* such names (PROX) is flattered less than one
that would have held them, but the whole panel is winners either way.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
WINDOW_52W = 252
NS = [5, 10, 20, 30]
SIGNALS = ["COMP", "PROX", "BLEND"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 300)


# ---------------------------------------------------------------- signals
def prox_raw(px):
    """P_t / rolling 252d max(P).  1.0 = at the 52-week high."""
    return px / px.rolling(WINDOW_52W, min_periods=WINDOW_52W).max()


def signal_frame(px, kind):
    """Cross-sectional ranking key (higher = better).  No vol scaler in any arm."""
    comp = score(px, vol_scale=False)[0]          # incumbent composite x above-200d bump
    if kind == "COMP":
        return comp
    pr = prox_raw(px)
    if kind == "PROX":
        return pr
    # BLEND: equal average of the two cross-sectional percentile ranks
    return (comp.rank(axis=1, pct=True) + pr.rank(axis=1, pct=True)) / 2


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def weights(px, kind, signal=None, n=None):
    if kind == "v1":
        return rules_v1_weights(px)
    elig = eligible_mask(px)
    if kind == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = signal_frame(px, signal)
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def paired_t(a, b):
    d = (a - b).dropna()
    if len(d) < 3 or d.std() == 0:
        return 0.0, 0.0
    return d.mean() / (d.std() / np.sqrt(len(d))), d.mean() * 252


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- IC machinery
def weekly_rank_ic(sig, px, elig, start):
    """Spearman of signal rank vs NEXT week's return, computed weekly on eligible names."""
    wk = px.resample("W-FRI").last()
    fwd = wk.pct_change().shift(-1)                       # return of the week AFTER the obs
    s = sig.reindex(wk.index, method="ffill").where(elig.reindex(wk.index, method="ffill"))
    s, fwd = s.loc[start:], fwd.loc[start:]
    out = []
    for d in s.index:
        a, b = s.loc[d], fwd.loc[d]
        m = a.notna() & b.notna()
        if m.sum() >= 8:
            out.append((d, a[m].rank().corr(b[m].rank())))
    return pd.Series(dict(out)).dropna()


def ic_line(ic):
    t = ic.mean() / (ic.std() / np.sqrt(len(ic))) if len(ic) > 2 and ic.std() > 0 else np.nan
    return ic.mean(), t, len(ic)


def flip_rate(w, years):
    """Ranking-key changes per ticker per year: how often a name enters or leaves."""
    inbook = (w > 0)
    return inbook.ne(inbook.shift(1)).sum().sum() / w.shape[1] / years


# ---------------------------------------------------------------- one universe
def run_universe(uname, px, base_note):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms = metrics(spy)

    print("\n" + "=" * 170)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 170)
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  OOS Sharpe "
          f"{metrics(spy_oos)['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > SPY halves & OOS, MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, "
          f"CAGR >= {0.70*ms['CAGR']:.3%}")

    base_v1 = backtest(px, weights(px, "v1"), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base_v1)
    print(f"RULES v1 (live book): CAGR {mb['CAGR']:.1%}  Sharpe {mb['Sharpe']:.3f}  "
          f"MaxDD {mb['MaxDD']:.1%}  halves {half_sharpes(base_v1)[0]:.3f}/{half_sharpes(base_v1)[1]:.3f}")

    elig = eligible_mask(px)

    # ---- signal diagnostics (no verdict depends on these)
    print(f"\nSIGNAL DIAGNOSTICS ({uname})")
    prox = prox_raw(px)
    comp = score(px, vol_scale=False)[0]
    sp = []
    idx = px.loc[start:].index
    for d in idx[::5]:
        a, b = prox.loc[d].where(elig.loc[d]), comp.loc[d].where(elig.loc[d])
        m = a.notna() & b.notna()
        if m.sum() >= 8:
            sp.append(a[m].rank().corr(b[m].rank()))
    print(f"  mean cross-sectional Spearman(PROX, COMP) over eligible names = {np.mean(sp):+.3f} "
          f"(sd {np.std(sp):.3f}, n={len(sp)} days)")
    print(f"  mean PROX of eligible names = {prox.where(elig).loc[start:].stack().mean():.3f}; "
          f"of ALL names = {prox.loc[start:].stack().mean():.3f}  "
          f"(the 200d gate already selects high-PROX names)")
    print("  weekly rank IC vs next week's return (eligible names only):")
    for sname in SIGNALS:
        ic = weekly_rank_ic(signal_frame(px, sname), px, elig, start)
        h = len(ic) // 2
        m_, t_, n_ = ic_line(ic)
        m1, t1, _ = ic_line(ic.iloc[:h])
        m2, t2, _ = ic_line(ic.iloc[h:])
        print(f"    {sname:<6} IC {m_:+.4f} (t {t_:+.2f}, {n_} wks) | H1 {m1:+.4f} (t {t1:+.2f}) "
              f"| H2 {m2:+.4f} (t {t2:+.2f})")

    # ---- the grid
    rows, series, books = [], {}, {}
    arms = [("v1", None, None), ("EWall", None, None)] + \
           [("CAND", s, n) for s in SIGNALS for n in NS]
    for kind, sname, n in arms:
        w = weights(px, kind, sname, n)
        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        r = res["returns"].loc[start:]
        to = res["turnover"].loc[start:]
        held = res["weights"].loc[start:]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
        key = kind if kind != "CAND" else f"{sname}-n{n}"
        series[key] = r
        books[key] = held
        rows.append(dict(
            point=key, kind=kind, signal=(sname or "-"), n=(n if n else np.nan),
            CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
            IS_Sharpe=metrics(r_is)["Sharpe"], IS_MaxDD=metrics(r_is)["MaxDD"],
            OOS_CAGR=metrics(r_oos)["CAGR"], OOS_Sharpe=metrics(r_oos)["Sharpe"],
            OOS_MaxDD=metrics(r_oos)["MaxDD"],
            turn=to.sum() / m["Years"], flips=flip_rate(held, m["Years"]),
            gross=held.sum(axis=1).mean(),
            p4a=verdict_4a(r, base_v1), f4b=fail_4b(r, spy, r_oos, spy_oos)))
    df = pd.DataFrame(rows).set_index("point")
    df["p4b"] = df["f4b"] == "-"

    print(f"\nFULL GRID {uname} - {len(df)} points, all reported (f4b lists which 4b tests fail)")
    cols = ["kind", "signal", "n", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turn", "flips", "p4a", "p4b", "f4b"]
    print(fmt(df[cols]))
    print(f"  4b passes: {int(df['p4b'].sum())} of {len(df)}  |  4a passes: {int(df['p4a'].sum())} of {len(df)}")

    # ---- PROX vs COMP at matched n
    print(f"\nHYPOTHESIS TEST ({uname}) - PROX (and BLEND) vs the incumbent COMP at matched n,")
    print("same days, same gate, same gross.  dRet = annualised paired mean, t = paired daily t.")
    hyp = []
    for n in NS:
        b = series[f"COMP-n{n}"]
        for sname in ["PROX", "BLEND"]:
            a = series[f"{sname}-n{n}"]
            t_, dr = paired_t(a, b)
            ma, mbk = metrics(a), metrics(b)
            ov = ((books[f"{sname}-n{n}"] > 0) & (books[f"COMP-n{n}"] > 0)).sum(axis=1).mean() / n
            hyp.append(dict(n=n, test=sname, dCAGR=ma["CAGR"] - mbk["CAGR"],
                            dVol=ma["Vol"] - mbk["Vol"], dMaxDD=ma["MaxDD"] - mbk["MaxDD"],
                            dSharpe=ma["Sharpe"] - mbk["Sharpe"], dRet_ann=dr, t=t_,
                            corr=a.corr(b), name_overlap=ov))
    hdf = pd.DataFrame(hyp)
    print(fmt(hdf.set_index(["n", "test"])))
    for sname in ["PROX", "BLEND"]:
        s = hdf[hdf.test == sname]
        print(f"  {sname:<6} vs COMP: dSharpe > 0 in {(s.dSharpe > 0).sum()}/{len(s)}, "
              f"mean dRet {s.dRet_ann.mean():+.2%}/yr, t range [{s.t.min():+.2f}, {s.t.max():+.2f}], "
              f"mean held-name overlap {s.name_overlap.mean():.0%}")

    # ---- vs the unranked control
    print(f"\nRANKING-VALUE CONTROL ({uname}) - each signal at each n vs EWall (no ranking):")
    ctl = []
    for sname in SIGNALS:
        for n in NS:
            t_, dr = paired_t(series[f"{sname}-n{n}"], series["EWall"])
            ctl.append(dict(signal=sname, n=n, dRet_ann=dr, t=t_,
                            dSharpe=metrics(series[f"{sname}-n{n}"])["Sharpe"] - metrics(series["EWall"])["Sharpe"]))
    print(fmt(pd.DataFrame(ctl).set_index(["signal", "n"])))

    # ---- calendar years
    print(f"\nCALENDAR YEARS ({uname}, n=20 books, %)")
    yr = pd.DataFrame({s: series[f"{s}-n20"] for s in SIGNALS})
    yr["EWall"] = series["EWall"]
    yr["v1_live"] = base_v1
    yr["SPY"] = spy
    print(fmt(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1) * 100))

    # ---- walk-forward
    print(f"\nWALK-FORWARD ({uname}, rule 8): chosen on 2009-2016, evaluated on 2017-2026")
    cand = df[df.kind == "CAND"].copy()
    cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD {metrics(spy_is)['MaxDD']:.1%} "
          f"-> S2 admits IS MaxDD shallower than {-cap:.1%}")
    print("  In-sample table (the only numbers either rule may look at):")
    print(fmt(cand[["signal", "n", "IS_Sharpe", "IS_MaxDD"]]))
    v1_oos = metrics(base_v1.loc[OOS_START:])
    so = metrics(spy_oos)
    print(f"  OOS bars: Sharpe > {so['Sharpe']:.3f}, MaxDD <= {0.60*abs(so['MaxDD']):.1%}, "
          f"CAGR >= {0.70*so['CAGR']:.2%}   (SPY OOS {so['CAGR']:.1%}/{so['Sharpe']:.3f}/{so['MaxDD']:.1%}; "
          f"v1 OOS {v1_oos['CAGR']:.1%}/{v1_oos['Sharpe']:.3f}/{v1_oos['MaxDD']:.1%})")

    order = {"COMP": 0, "PROX": 1, "BLEND": 2}

    def pick(sub, label):
        if sub.empty:
            print(f"  {label}: none qualify"); return None
        s = sub.copy()
        s["_o"] = s.signal.map(order)
        s = s.sort_values(["IS_Sharpe", "_o", "n"], ascending=[False, True, True])
        p = s.index[0]
        row = df.loc[p]
        ok = (row.OOS_Sharpe > so["Sharpe"] and abs(row.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"])
              and row.OOS_CAGR >= 0.70 * so["CAGR"])
        print(f"  {label}: {p:<10} -> OOS CAGR {row.OOS_CAGR:.1%}  Sharpe {row.OOS_Sharpe:.3f}  "
              f"MaxDD {row.OOS_MaxDD:.1%}   clears all OOS 4b bars? {ok}")
        return p

    pick(cand, "S1 plain-Sharpe")
    pick(cand[cand.IS_MaxDD >= -cap], "S2 4b-aware   ")
    print("  Signal choice audited within each n (S1 rule restricted to that n):")
    for n in NS:
        pick(cand[cand.n == n], f"    n={n:<3} S1")
    rho = cand["IS_Sharpe"].rank().corr(cand["OOS_Sharpe"].rank())
    print(f"  Spearman(IS Sharpe, OOS Sharpe) over the {len(cand)} CAND points = {rho:+.3f}")

    df["universe"] = uname
    return df, base_v1, spy, mb


# ---------------------------------------------------------------- main
def main():
    print("=" * 170)
    print(f"Idea 13  52w-high-proximity (lane C) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    print("=" * 170)

    px = load_universe()
    pxb = load_universe(broad=True)
    yrs = px.index.to_series().groupby(px.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    start = px.index[260]
    chk = backtest(px, weights(px, "CAND", "COMP", 20), cost_bps=COST_BPS,
                   freq=FREQ)["returns"].loc[start:]
    mc = metrics(chk)
    print("\nHARNESS CHECK vs idea 2's published KEEP row (12.7% / 1.093 / -18.3%, halves 1.088/1.103):")
    print(f"  reproduced: {mc['CAGR']:.1%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk)[0]:.3f}/{half_sharpes(chk)[1]:.3f}")

    d1, b1, spy1, mb1 = run_universe("universe.json", px, "primary")
    d2, b2, spy2, mb2 = run_universe("universe_broad.json", pxb, "broad")

    # ---- cross-universe 4b (the bar that has killed every previous candidate)
    print("\n" + "=" * 170)
    print("CROSS-UNIVERSE 4b (a point passes only if it passes on BOTH lists)")
    print("=" * 170)
    common = [i for i in d1.index if i in d2.index]
    cu = pd.DataFrame({
        "u56_Sharpe": d1.loc[common, "Sharpe"], "u56_4b": d1.loc[common, "p4b"],
        "u56_fail": d1.loc[common, "f4b"],
        "broad_Sharpe": d2.loc[common, "Sharpe"], "broad_4b": d2.loc[common, "p4b"],
        "broad_fail": d2.loc[common, "f4b"]})
    cu["both"] = cu.u56_4b & cu.broad_4b
    print(fmt(cu))
    print(f"  passes on both lists: {int(cu['both'].sum())} of {len(cu)}")

    # ---- leaderboard rows
    print("\n" + "=" * 170)
    print("LEADERBOARD rows")
    print("=" * 170)
    for uname, d, mb, base in (("u56", d1, mb1, b1), ("broad", d2, mb2, b2)):
        bh1, bh2 = half_sharpes(base)
        for p in d.index:
            r = d.loc[p]
            v = "KEEP 4b" if r.p4b else ("4a-pass, KILL 4b (%s)" % r.f4b if r.p4a
                                         else "KILL 4b (%s)" % r.f4b)
            print(f"| 2026-09-04 | 13 {uname}/{p} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
                  f"{r.H1:.2f} / {r.H2:.2f} | {mb['Sharpe']:.2f} ({bh1:.2f}/{bh2:.2f}) | {v} | {SCRIPT} |")

    out = pd.concat([d1, d2])
    out.to_csv(REPO / "research" / "backtests" / f"{SCRIPT[:-3]}.grid.csv")
    print(f"\nGrid written to research/backtests/{SCRIPT[:-3]}.grid.csv")


if __name__ == "__main__":
    main()
