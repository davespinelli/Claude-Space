#!/usr/bin/env python3
"""Idea 80 - "is-52w-proximity-a-short-signal": invert idea 13's negative signal, then
control it for volatility.

The question
------------
Idea 13 killed ranking on nearness to the 52-week high (`PROX_t = P_t / max(P_{t-251..t})`)
and, in doing so, measured something stronger than a null: the weekly rank IC of PROX
against next week's return, computed over eligible names only, was NEGATIVE and significant
on both lists (-0.0208, t -2.13 on universe.json; -0.0252, t -3.34 on broad) and negative in
both halves of both.  A long-only book cannot short a negative signal, but it can flip the
ranking key.  Two readings of that negative IC have opposite consequences:

    (A) genuine short-horizon reversal INSIDE the trend gate - names that are still above
        their 200d MA but furthest below their own 52-week high bounce.  If so, inverting
        the key should beat the incumbent composite.
    (B) a low-volatility artefact - low-vol names sit closer to their highs mechanically
        (small drawdowns from the running max), so "far from the high" is a proxy for "high
        vol", and inverting the key is really buying vol... which should LOSE, not win.
        Idea 13's own numbers hint at (B): every PROX book had LOWER vol than its matched
        COMP book, i.e. high-PROX = low-vol, so low-PROX = high-vol.

This run tests both and is designed so that either answer is informative.

Books - structural variants, all reported, none picked on its own result
    v1     RULES v1 exactly as live (top 5 eligible by the composite WITH /sqrt(vol20),
           15% each), one row per universe, for 4a.
    CAND   idea 2's standing 4b KEEP construction: top-n eligible EQUAL-WEIGHT at 75%
           gross, no vol scaler.  The ranking key is swapped inside this book only.
    EWall  equal-weight ALL eligible at 75% gross, no ranking - the "is the ranking doing
           anything" control (idea 10's `B136/EWall`).

Ranking keys (arm 1 of 2 tuned parameters)
    COMP    incumbent composite (12-1 + 6m + 3m percentile ranks) x the above-200d bump.
            Control.  Not the idea.
    IPROX   -PROX: buy the eligible names FURTHEST below their own 52-week high.  The idea
            as queried.
    IPROXn  IPROX after cross-sectional neutralisation against vol20: each day, the
            percentile rank of PROX is residualised on the percentile rank of vol20 over
            eligible names (row-wise OLS, beta_t = cov/var), and the residual is inverted.
            This is the arm that separates reading (A) from reading (B).
    LOWVOL  -vol20 among eligible: the rival explanation as its own book.  If IPROX works
            only because it is a vol tilt, LOWVOL should be the better tilt (it is the
            clean version of it) - and the sign matters: IPROX buys HIGH vol, so if LOWVOL
            wins and IPROX loses, reading (B) holds with the sign against the idea.

Position count (arm 2 of 2 tuned parameters): n in {5, 10, 20, 30}, exactly idea 13's grid.
The 252-day window, the 200d / vol20 < 0.60 gate, 75% gross, weekly rebalancing, 10 bps and
next-day execution are all held fixed at RULES v1's own values and are not tuned.

Grid = 2 universes x (1 v1 + 1 EWall + 4 keys x 4 n) = 36 points, ALL reported.

Signal-level diagnostics that no verdict depends on
    - Weekly rank IC of every key vs next week's return, full sample and by half, t-stats.
    - Cross-sectional Spearman(PROX, vol20) among eligible names: is reading (B) even
      mechanically available?
    - Weekly cross-sectional (Fama-MacBeth) regression of next week's return on
      {rank(PROX), rank(vol20)} jointly over eligible names: the direct test of whether
      PROX carries anything once vol is controlled.  Univariate slopes reported alongside.
    - Realised held-name vol20 and book vol per arm: does IPROX buy volatility?
    - Turnover and flips/ticker/yr per point (this repo's recurring net-Sharpe orderer).

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number was read
    S1  over the 16 CAND (key, n) points, highest 2009-2016 Sharpe; ties -> COMP, IPROX,
        IPROXn, LOWVOL, then smaller n.
    S2  the same, restricted to points whose in-sample MaxDD is within 60% of SPY's
        in-sample MaxDD.
    Also: the best key within each n, so the key choice is auditable apart from n.
    Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Harness sanity: reproduces idea 2's published KEEP row (universe.json / CAND / COMP / n=20
-> 12.7% / 1.093 / -18.3%) and idea 13's PROX rows before any new number is reported.

Survivorship: current constituents of both lists, one-directional, and it bites this run
harder than most.  IPROX deliberately buys the names furthest below their own highs - the
exact cohort in which the missing delisted names would have lived.  Any IPROX result is
therefore biased UPWARD and a KILL is the safer conclusion than a KEEP.

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
WINDOW_52W = 252
NS = [5, 10, 20, 30]
KEYS = ["COMP", "IPROX", "IPROXn", "LOWVOL"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- signals
def prox_raw(px):
    return px / px.rolling(WINDOW_52W, min_periods=WINDOW_52W).max()


def vol20_of(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def _rowwise_residual(y, x):
    """Row-wise OLS residual of y on x (both DataFrames of percentile ranks, NaN outside
    the eligible set).  beta_t = cov_t(y,x)/var_t(x); returns y - a_t - b_t*x."""
    my, mx = y.mean(axis=1), x.mean(axis=1)
    yc, xc = y.sub(my, axis=0), x.sub(mx, axis=0)
    cov = (yc * xc).mean(axis=1)
    var = (xc * xc).mean(axis=1).replace(0, np.nan)
    b = cov / var
    return yc.sub(xc.mul(b, axis=0))


def key_frame(px, kind, elig):
    """Cross-sectional ranking key (higher = held first).  No vol scaler in any arm."""
    if kind == "COMP":
        return score(px, vol_scale=False)[0]
    v20 = vol20_of(px)
    if kind == "LOWVOL":
        return -v20
    pr = prox_raw(px)
    if kind == "IPROX":
        return -pr
    # IPROXn: neutralise PROX against vol20 among eligible names, then invert
    rp = pr.where(elig).rank(axis=1, pct=True)
    rv = v20.where(elig).rank(axis=1, pct=True)
    return -_rowwise_residual(rp, rv)


def weights(px, kind, elig, key=None, n=None):
    if kind == "v1":
        return rules_v1_weights(px)
    if kind == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = key_frame(px, key, elig)
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


def flip_rate(w, years):
    inbook = (w > 0)
    return inbook.ne(inbook.shift(1)).sum().sum() / w.shape[1] / years


# ---------------------------------------------------------------- IC / Fama-MacBeth
def weekly_panel(px, elig, start):
    """Weekly (obs, next-week-return) panel restricted to eligible names."""
    wk = px.resample("W-FRI").last()
    fwd = wk.pct_change().shift(-1).loc[start:]
    el = elig.reindex(wk.index, method="ffill").loc[start:]
    return wk.loc[start:], fwd, el


def rank_ic(sig, wk_index, fwd, el):
    s = sig.reindex(wk_index, method="ffill").where(el)
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


def fama_macbeth(px, elig, start):
    """Weekly cross-sectional regressions of next week's return on percentile ranks of
    PROX and vol20 over eligible names.  Returns the mean slope and t of the mean."""
    wk, fwd, el = weekly_panel(px, elig, start)
    pr = prox_raw(px).reindex(wk.index, method="ffill").where(el)
    v20 = vol20_of(px).reindex(wk.index, method="ffill").where(el)
    uni_p, uni_v, biv_p, biv_v = [], [], [], []
    for d in wk.index:
        y = fwd.loc[d]
        p = pr.loc[d].rank(pct=True)
        v = v20.loc[d].rank(pct=True)
        m = y.notna() & p.notna() & v.notna()
        if m.sum() < 10:
            continue
        yy, pp, vv = y[m].values, p[m].values, v[m].values
        yy = yy - yy.mean()
        pp = pp - pp.mean(); vv = vv - vv.mean()
        if pp.std() > 0: uni_p.append(float(np.dot(pp, yy) / np.dot(pp, pp)))
        if vv.std() > 0: uni_v.append(float(np.dot(vv, yy) / np.dot(vv, vv)))
        X = np.column_stack([pp, vv])
        try:
            bb = np.linalg.lstsq(X, yy, rcond=None)[0]
            biv_p.append(float(bb[0])); biv_v.append(float(bb[1]))
        except np.linalg.LinAlgError:
            pass

    def line(v):
        a = np.array(v)
        if len(a) < 3 or a.std() == 0:
            return np.nan, np.nan, len(a)
        return a.mean(), a.mean() / (a.std(ddof=1) / np.sqrt(len(a))), len(a)
    return {"PROX_uni": line(uni_p), "vol20_uni": line(uni_v),
            "PROX_biv": line(biv_p), "vol20_biv": line(biv_v)}


# ---------------------------------------------------------------- one universe
def run_universe(uname, px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms, mso = metrics(spy), metrics(spy_oos)

    print("\n" + "=" * 175)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 175)
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  OOS Sharpe {mso['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > SPY halves & OOS, MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, "
          f"CAGR >= {0.70*ms['CAGR']:.3%}")

    elig = eligible_mask(px)
    base_v1 = backtest(px, weights(px, "v1", elig), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base_v1)
    print(f"RULES v1 (live book): CAGR {mb['CAGR']:.1%}  Sharpe {mb['Sharpe']:.3f}  MaxDD {mb['MaxDD']:.1%}  "
          f"halves {half_sharpes(base_v1)[0]:.3f}/{half_sharpes(base_v1)[1]:.3f}")

    # ---- signal diagnostics
    print(f"\nSIGNAL DIAGNOSTICS ({uname})  [no verdict depends on these]")
    pr, v20 = prox_raw(px), vol20_of(px)
    sp = []
    for d in px.loc[start:].index[::5]:
        a, b = pr.loc[d].where(elig.loc[d]), v20.loc[d].where(elig.loc[d])
        m = a.notna() & b.notna()
        if m.sum() >= 8:
            sp.append(a[m].rank().corr(b[m].rank()))
    print(f"  mean cross-sectional Spearman(PROX, vol20) over eligible names = {np.mean(sp):+.3f} "
          f"(sd {np.std(sp):.3f}, n={len(sp)} days)")
    print("    negative => names near their 52w high are LOW vol, so IPROX (far from the high) "
          "is mechanically a HIGH-vol tilt")

    wk, fwd, el = weekly_panel(px, elig, start)
    print("  weekly rank IC vs next week's return (eligible names only):")
    for k in KEYS:
        ic = rank_ic(key_frame(px, k, elig), wk.index, fwd, el)
        h = len(ic) // 2
        m_, t_, n_ = ic_line(ic)
        m1, t1, _ = ic_line(ic.iloc[:h]); m2, t2, _ = ic_line(ic.iloc[h:])
        print(f"    {k:<7} IC {m_:+.4f} (t {t_:+.2f}, {n_} wks) | H1 {m1:+.4f} (t {t1:+.2f}) "
              f"| H2 {m2:+.4f} (t {t2:+.2f})")

    print("  Fama-MacBeth weekly cross-sectional slopes on NEXT week's return "
          "(percentile ranks, eligible names):")
    fm = fama_macbeth(px, elig, start)
    for k in ["PROX_uni", "vol20_uni", "PROX_biv", "vol20_biv"]:
        b_, t_, n_ = fm[k]
        print(f"    {k:<10} mean slope {b_:+.5f} (t {t_:+.2f}, {n_} wks)")
    print("    'uni' = alone, 'biv' = PROX and vol20 together.  If PROX_biv loses its "
          "significance while PROX_uni had it, the 52w signal is a vol proxy.")

    # ---- the grid
    rows, series, books = [], {}, {}
    arms = [("v1", None, None), ("EWall", None, None)] + [("CAND", k, n) for k in KEYS for n in NS]
    for kind, k, n in arms:
        w = weights(px, kind, elig, k, n)
        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        r = res["returns"].loc[start:]
        to = res["turnover"].loc[start:]
        held = res["weights"].loc[start:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
        name = kind if kind != "CAND" else f"{k}-n{n}"
        series[name], books[name] = r, held
        hv = v20.loc[start:].where(held > 0).stack().mean()
        rows.append(dict(
            point=name, kind=kind, key=(k or "-"), n=(n if n else np.nan),
            CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
            IS_Sharpe=metrics(r_is)["Sharpe"], IS_MaxDD=metrics(r_is)["MaxDD"],
            OOS_CAGR=metrics(r_oos)["CAGR"], OOS_Sharpe=metrics(r_oos)["Sharpe"],
            OOS_MaxDD=metrics(r_oos)["MaxDD"],
            held_vol20=hv, turn=to.sum() / m["Years"], flips=flip_rate(held, m["Years"]),
            p4a=verdict_4a(r, base_v1), f4b=fail_4b(r, spy, r_oos, spy_oos)))
    df = pd.DataFrame(rows).set_index("point")
    df["p4b"] = df["f4b"] == "-"

    print(f"\nFULL GRID {uname} - {len(df)} points, ALL reported (f4b lists which 4b tests fail)")
    print(fmt(df[["kind", "key", "n", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "held_vol20", "turn", "flips",
                  "p4a", "p4b", "f4b"]]))
    print(f"  4b passes: {int(df['p4b'].sum())} of {len(df)}  |  4a passes: {int(df['p4a'].sum())} of {len(df)}")

    # ---- the hypothesis test: each inverted key vs COMP at matched n
    print(f"\nHYPOTHESIS TEST ({uname}) - IPROX / IPROXn / LOWVOL vs the incumbent COMP at "
          f"matched n, same days, same gate, same gross")
    hyp = []
    for n in NS:
        b = series[f"COMP-n{n}"]
        for k in ["IPROX", "IPROXn", "LOWVOL"]:
            a = series[f"{k}-n{n}"]
            t_, dr = paired_t(a, b)
            ma, mbk = metrics(a), metrics(b)
            ov = ((books[f"{k}-n{n}"] > 0) & (books[f"COMP-n{n}"] > 0)).sum(axis=1).mean() / n
            hyp.append(dict(n=n, key=k, dCAGR=ma["CAGR"] - mbk["CAGR"], dVol=ma["Vol"] - mbk["Vol"],
                            dMaxDD=ma["MaxDD"] - mbk["MaxDD"], dSharpe=ma["Sharpe"] - mbk["Sharpe"],
                            dRet_ann=dr, t=t_, corr=a.corr(b), overlap=ov))
    hdf = pd.DataFrame(hyp)
    print(fmt(hdf.set_index(["n", "key"])))
    for k in ["IPROX", "IPROXn", "LOWVOL"]:
        s = hdf[hdf.key == k]
        print(f"  {k:<7} vs COMP: dSharpe > 0 in {(s.dSharpe > 0).sum()}/{len(s)}, "
              f"mean dRet {s.dRet_ann.mean():+.2%}/yr, t range [{s.t.min():+.2f}, {s.t.max():+.2f}], "
              f"mean overlap {s.overlap.mean():.0%}")

    # ---- IPROX vs its own vol-neutralised twin: the (A)-vs-(B) test in book space
    print(f"\nIS IT A VOL ARTEFACT? ({uname}) - IPROX vs IPROXn (same key, vol removed) and "
          f"vs LOWVOL (pure vol tilt)")
    for n in NS:
        t1, d1_ = paired_t(series[f"IPROX-n{n}"], series[f"IPROXn-n{n}"])
        t2, d2_ = paired_t(series[f"IPROX-n{n}"], series[f"LOWVOL-n{n}"])
        print(f"    n={n:<3} IPROX-IPROXn: {d1_:+.2%}/yr (t {t1:+.2f}), dVol "
              f"{metrics(series[f'IPROX-n{n}'])['Vol'] - metrics(series[f'IPROXn-n{n}'])['Vol']:+.3f} | "
              f"IPROX-LOWVOL: {d2_:+.2%}/yr (t {t2:+.2f}) | held vol20 "
              f"IPROX {df.loc[f'IPROX-n{n}','held_vol20']:.3f} / IPROXn "
              f"{df.loc[f'IPROXn-n{n}','held_vol20']:.3f} / LOWVOL "
              f"{df.loc[f'LOWVOL-n{n}','held_vol20']:.3f} / COMP {df.loc[f'COMP-n{n}','held_vol20']:.3f}")

    # ---- vs the unranked control
    print(f"\nRANKING-VALUE CONTROL ({uname}) - each key at each n vs EWall (no ranking):")
    ctl = []
    for k in KEYS:
        for n in NS:
            t_, dr = paired_t(series[f"{k}-n{n}"], series["EWall"])
            ctl.append(dict(key=k, n=n, dRet_ann=dr, t=t_,
                            dSharpe=metrics(series[f"{k}-n{n}"])["Sharpe"] - metrics(series["EWall"])["Sharpe"]))
    print(fmt(pd.DataFrame(ctl).set_index(["key", "n"])))

    # ---- calendar years
    print(f"\nCALENDAR YEARS ({uname}, n=20 books, %)")
    yr = pd.DataFrame({k: series[f"{k}-n20"] for k in KEYS})
    yr["EWall"] = series["EWall"]; yr["v1_live"] = base_v1; yr["SPY"] = spy
    print(fmt(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1) * 100))

    # ---- walk-forward
    print(f"\nWALK-FORWARD ({uname}, rule 8): chosen on 2009-2016, evaluated on 2017-2026")
    cand = df[df.kind == "CAND"].copy()
    cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD {metrics(spy_is)['MaxDD']:.1%} "
          f"-> S2 admits IS MaxDD shallower than {-cap:.1%}")
    print("  In-sample table (the only numbers either rule may look at):")
    print(fmt(cand[["key", "n", "IS_Sharpe", "IS_MaxDD"]]))
    v1o = metrics(base_v1.loc[OOS_START:])
    print(f"  OOS bars: Sharpe > {mso['Sharpe']:.3f}, MaxDD <= {0.60*abs(mso['MaxDD']):.1%}, "
          f"CAGR >= {0.70*mso['CAGR']:.2%}   (SPY OOS {mso['CAGR']:.1%}/{mso['Sharpe']:.3f}/{mso['MaxDD']:.1%}; "
          f"v1 OOS {v1o['CAGR']:.1%}/{v1o['Sharpe']:.3f}/{v1o['MaxDD']:.1%})")

    order = {k: i for i, k in enumerate(KEYS)}

    def pick(sub, label):
        if sub.empty:
            print(f"  {label}: none qualify"); return None
        s = sub.copy(); s["_o"] = s.key.map(order)
        s = s.sort_values(["IS_Sharpe", "_o", "n"], ascending=[False, True, True])
        p = s.index[0]; row = df.loc[p]
        ok = (row.OOS_Sharpe > mso["Sharpe"] and abs(row.OOS_MaxDD) <= 0.60 * abs(mso["MaxDD"])
              and row.OOS_CAGR >= 0.70 * mso["CAGR"])
        print(f"  {label}: {p:<12} -> OOS CAGR {row.OOS_CAGR:.1%}  Sharpe {row.OOS_Sharpe:.3f}  "
              f"MaxDD {row.OOS_MaxDD:.1%}   clears all OOS 4b bars? {ok}")
        return p

    pick(cand, "S1 plain-Sharpe")
    pick(cand[cand.IS_MaxDD >= -cap], "S2 4b-aware   ")
    print("  Key choice audited within each n (S1 restricted to that n):")
    for n in NS:
        pick(cand[cand.n == n], f"    n={n:<3} S1")
    rho = cand["IS_Sharpe"].rank().corr(cand["OOS_Sharpe"].rank())
    print(f"  Spearman(IS Sharpe, OOS Sharpe) over the {len(cand)} CAND points = {rho:+.3f}")

    df["universe"] = uname
    return df, base_v1, spy


# ---------------------------------------------------------------- main
def main():
    print("=" * 175)
    print(f"Idea 80  is-52w-proximity-a-short-signal (cloud) | {SCRIPT} | {COST_BPS} bps, weekly, "
          f"next-day execution")
    print("=" * 175)

    px = load_universe()
    pxb = load_universe(broad=True)
    yrs = px.index.to_series().groupby(px.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    start = px.index[260]
    el = eligible_mask(px)
    chk = backtest(px, weights(px, "CAND", el, "COMP", 20), cost_bps=COST_BPS,
                   freq=FREQ)["returns"].loc[start:]
    mc = metrics(chk)
    print("\nHARNESS CHECK vs idea 2's published KEEP row (12.7% / 1.093 / -18.3%, halves 1.088/1.103):")
    print(f"  reproduced: {mc['CAGR']:.1%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk)[0]:.3f}/{half_sharpes(chk)[1]:.3f}")

    d1, b1, s1 = run_universe("universe.json", px)
    d2, b2, s2 = run_universe("universe_broad.json", pxb)

    print("\n" + "=" * 175)
    print("CROSS-UNIVERSE 4b (a point passes only if it passes on BOTH lists)")
    print("=" * 175)
    common = d1.index.intersection(d2.index)
    both = pd.DataFrame({"universe.json": d1.loc[common, "p4b"], "broad": d2.loc[common, "p4b"]})
    both["both"] = both["universe.json"] & both["broad"]
    print(both.to_string())
    print(f"  points passing on both lists: {int(both['both'].sum())} of {len(both)}")

    print("\nSIGN CONSISTENCY ACROSS LISTS (dSharpe vs COMP at matched n):")
    for k in ["IPROX", "IPROXn", "LOWVOL"]:
        wins = 0; tot = 0
        for d in (d1, d2):
            for n in NS:
                tot += 1
                wins += int(d.loc[f"{k}-n{n}", "Sharpe"] > d.loc[f"COMP-n{n}", "Sharpe"])
        print(f"  {k:<7} beats COMP in {wins}/{tot} matched-n pairs across both lists")

    print("\nLEADERBOARD rows:")
    for d, tag in ((d1, "u56"), (d2, "broad")):
        for p, r in d.iterrows():
            v = "KEEP 4b" if r.p4b else f"KILL 4b ({r.f4b})"
            if r.p4a: v = "4a-pass, " + v
            print(f"| 2026-09-04 | 80 {tag}/{p} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
                  f"{r.H1:.2f} / {r.H2:.2f} | see v1/SPY rows | {v} | {SCRIPT} |")


if __name__ == "__main__":
    main()
