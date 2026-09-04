#!/usr/bin/env python3
"""QUEUE idea 14 — rsi2-sleeve (cloud, 2026-09-04).

Question
--------
Allocate 25% of the book to a short-horizon mean-reversion sleeve (Connors RSI(2)
< 10 while the instrument is above its 200d MA) on the 16 sector/industry ETFs,
funding it by scaling the trend book down.  The claim being tested is
diversification: a 2-day mean-reversion signal is close to orthogonal to a 3-12
month momentum signal, so even a mediocre sleeve could raise book Sharpe.

The prior from this repo is hostile and makes the run worth doing rather than a
formality.  RSI(2) fires often and holds for days: ideas 55/57/4/3/9 all found that
in these books NET Sharpe orders by FLIP RATE, and idea 76 found cost sensitivity
is governed by mean holding-episode length.  A sleeve that turns over ~50x/yr is
the fastest instrument the project has ever tested.  The pre-registered question is
therefore not "does RSI(2) predict returns" (it does, in the literature) but
"does it survive 10 bps at this holding period, and does the 25% allocation buy
more diversification than it gives up in return".

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names) as primary;
           universe_broad.json (136 names) as the robustness pass.  Both reported.
           The SLEEVE always trades the same 16 sector/industry ETFs
           (XLK XLF XLV XLE XLI XLY XLP XLU XLB XLRE XLC SMH XBI KRE ITB GDX),
           which are present in both lists; only the CORE changes with universe.
Cores    : three PRE-CHOSEN books, none tuned here —
           * `v1`     — rules_v1_weights exactly as live (the idea's literal subject).
           * `top20`  — idea 2's standing 4b KEEP: top-20 by the composite without
                        the vol scaler among 200d/vol20-eligible names, 3.75% each.
           * `ew-all` — equal-weight every eligible name at 75% gross (ideas 28/25).
Sleeve   : entry  px > 200d MA AND RSI(2) < THR      (Wilder RSI, 2-day)
           exit   RSI(2) > 50                        (Connors' canonical exit; FIXED,
                                                      not tuned — the no-hysteresis
                                                      variant is reported as a
                                                      labelled sensitivity only)
           equal weight across signalling names, sleeve fully invested when >=1
           name signals and in CASH otherwise, re-evaluated DAILY.
Params   : exactly TWO tuned dimensions —
             THR    in {5, 10, 20}      (10 is the queued value)
             f      in {0.25, 0.50}     (0.25 is the queued value; 0.00 = control)
           Every (universe, core, THR, f, cost) cell is printed.  Nothing is chosen
           on out-of-sample data.  Everything else (exit level, allocation, idle
           handling, sleeve cadence, sleeve universe) is fixed a priori; the
           alternatives appear only in the clearly-marked SENSITIVITY block, which
           no verdict and no walk-forward is allowed to read.
Costs    : 5 / 10 / 25 / 50 bps on BOTH legs and on the split rebalance.  10 bps is
           the PROTOCOL cost and the one verdicts are read at.
Execution: weights decided at close t, applied at t+1 (engine).  Long-only, no
           leverage, no shorting.  The core keeps its live WEEKLY cadence and is
           bit-identical to the published books; the sleeve rebalances daily; the
           SPLIT between the two legs drifts within the week and is reset weekly,
           paying turnover cost like any other trade.
Baseline : RULES v1 at its live weekly cadence (4a) and SPY (4b), at each cost.
Rule 8   : (THR, f) chosen on 2009-2016 only under two selection rules fixed BEFORE
           any OOS number is read; 2017-2026 evaluated untouched.

SURVIVORSHIP: both lists are current constituents, so absolute CAGR/Sharpe are
optimistic.  The sleeve leg is the least exposed part of the run — the sector ETFs
are index products that existed throughout and none of them was selected on
performance — but the CORE it is blended with carries the usual bias, so the
sleeve-vs-control differences are the trustworthy numbers here, not the levels.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

SECTORS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB",
           "XLRE", "XLC", "SMH", "XBI", "KRE", "ITB", "GDX"]
GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
THRS = [5, 10, 20]
FRACS = [0.25, 0.50]
COSTS = [5, 10, 25, 50]
PROTO_COST = 10
EXIT_RSI = 50.0
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
SCRIPT = "research/backtests/2026-09-04_rsi2-sleeve_cloud.py"


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2's candidate scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def above200(px):
    return (px > px.rolling(200).mean()).fillna(False)


def eligible(px):
    return (vol20(px) < MAX_VOL) & above200(px)


def w_top20(px):
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def w_ewall(px):
    e = eligible(px).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


CORES = {"v1": rules_v1_weights, "top20": w_top20, "ew-all": w_ewall}


def rsi(px, n=2):
    """Wilder's RSI over n days, computed per column on the given price panel."""
    d = px.diff()
    up = d.clip(lower=0.0)
    dn = (-d).clip(lower=0.0)
    au = up.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    ad = dn.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    rs = au / ad.replace(0.0, np.nan)
    out = 100.0 - 100.0 / (1.0 + rs)
    return out.where(ad != 0.0, 100.0).where(au.notna())


def sleeve_state(pxs, thr, hysteresis=True):
    """Boolean holding matrix for the RSI(2) sleeve.

    hysteresis=True  : enter when (above 200d) & RSI2 < thr, exit when RSI2 > EXIT_RSI
                       (Connors' canonical rule; PRE-REGISTERED primary).
    hysteresis=False : hold exactly on the days the entry condition is true
                       (sensitivity only).
    """
    r2 = rsi(pxs, 2)
    entry = above200(pxs) & (r2 < thr)
    if not hysteresis:
        return entry.fillna(False)
    exit_ = (r2 > EXIT_RSI) | (~above200(pxs))
    raw = pd.DataFrame(np.nan, index=pxs.index, columns=pxs.columns)
    raw = raw.mask(entry, 1.0)
    raw = raw.mask(exit_ & ~entry, 0.0)
    return (raw.ffill().fillna(0.0) > 0.5)


def sleeve_weights(pxs, thr, hysteresis=True, alloc="full"):
    """Sleeve target weights summing to <=1 of SLEEVE capital (rest is cash)."""
    h = sleeve_state(pxs, thr, hysteresis).astype(float)
    n = h.sum(axis=1)
    if alloc == "full":                       # equal weight across signalling names
        den = n.replace(0, np.nan)
    elif alloc == "div4":                     # never more than 25% of sleeve per name
        den = n.clip(lower=4).replace(0, np.nan)
    else:
        raise ValueError(alloc)
    return h.div(den, axis=0).fillna(0.0)


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
    return float(d.mean() * 252), float(d.mean() / (d.std() / np.sqrt(len(d))))


def turn_per_yr(t):
    return t.sum() / (len(t) / 252)


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


# ---------------------------------------------------------------- blending
def blend(gc, tc, gs, ts, f, bps, rb_mask):
    """Two-leg book: (1-f) core + f sleeve, split reset on rb_mask, drifting between.

    gc/gs are GROSS (cost-free) daily return streams of the two legs and tc/ts their
    turnover streams; costs for both legs and for the split rebalance are charged at
    `bps`.  Returns the net daily return stream of the blended book.
    """
    if f == 0.0:
        return gc - tc * bps / 1e4
    rc = gc - tc * bps / 1e4
    rs = gs - ts * bps / 1e4
    idx = gc.index
    a, b = 1.0 - f, f                                   # capital in core / sleeve
    out = np.empty(len(idx))
    rc_v, rs_v, mk = rc.values, rs.values, rb_mask.reindex(idx).fillna(False).values
    for i in range(len(idx)):
        if mk[i]:
            tot = a + b
            new_a, new_b = (1.0 - f) * tot, f * tot
            cost = (abs(new_a - a) + abs(new_b - b)) * bps / 1e4
            a, b = new_a, new_b
            tot_after = a + b - cost
            a, b = a * tot_after / tot, b * tot_after / tot
        pre = a + b
        a *= (1.0 + rc_v[i])
        b *= (1.0 + rs_v[i])
        out[i] = (a + b) / pre - 1.0
    return pd.Series(out, index=idx)


# ---------------------------------------------------------------- one universe
def sweep(px, tag, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m(spy)
    s1, s2 = halves(spy)
    ss_o = m(spy.loc[OOS_START:])[1]

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    print(f"\n{'=' * 138}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 138)

    pxs = px[[t for t in SECTORS if t in px.columns]]
    wk = rebalance_mask(px.index, "W")

    # --- legs (cost-free; costs applied analytically, identity asserted in main)
    CORE = {}
    for bk, fn in CORES.items():
        res = backtest(px, fn(px), cost_bps=0.0, freq="W")
        CORE[bk] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    SLV = {}
    for thr in THRS:
        res = backtest(pxs, sleeve_weights(pxs, thr), cost_bps=0.0, freq="D")
        SLV[thr] = (res["returns"].reindex(px.index).fillna(0.0).loc[start:],
                    res["turnover"].reindex(px.index).fillna(0.0).loc[start:])

    b_g, b_t = CORE["v1"]
    b10 = b_g - b_t * PROTO_COST / 1e4
    bc, bs, bdd = m(b10)
    bh1, bh2 = halves(b10)
    print(f"RULES v1 baseline (weekly) @{PROTO_COST}bps: {bc:.1%}/{bs:.3f}/{bdd:.1%} "
          f"halves {bh1:.3f}/{bh2:.3f} OOS Sharpe {m(b10.loc[OOS_START:])[1]:.3f} "
          f"(4a bars: H1>{bh1:.3f}, H2>{bh2:.3f}, MaxDD>={bdd:.1%})")

    # ---- what the sleeve IS, standalone.  This is the crux of the idea.
    print(f"\nTHE SLEEVE STANDALONE ({tag}) — 100% of capital in the RSI(2) sleeve, "
          f"daily, sector ETFs only.  Cash when flat.")
    print(f"  {'thr':>4}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'2020':>8}{'2022':>8}"
          f"{'turn/yr':>9}{'%days in':>10}{'avg names':>11}{'avg hold(d)':>13}{'corr(core)':>12}")
    for thr in THRS:
        gs, ts = SLV[thr]
        h = sleeve_state(pxs, thr).loc[start:]
        holding = h.sum(axis=1)
        # mean holding-episode length across names (idea 76's variable)
        eps, lens = 0, 0
        for c in h.columns:
            v = h[c].values.astype(int)
            starts = int(((v[1:] == 1) & (v[:-1] == 0)).sum()) + int(v[0] == 1)
            eps += starts
            lens += int(v.sum())
        avg_hold = lens / eps if eps else np.nan
        for c_bps in (PROTO_COST, 25):
            r = gs - ts * c_bps / 1e4
            cg, sh, dd = m(r)
            print(f"  {thr:4d}{c_bps:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}{year_ret(r, 2020):8.1%}"
                  f"{year_ret(r, 2022):8.1%}{turn_per_yr(ts):8.1f}x{(holding > 0).mean():10.1%}"
                  f"{holding[holding > 0].mean():11.2f}{avg_hold:13.1f}"
                  f"{r.corr(b_g - b_t * c_bps / 1e4):12.3f}")

    # ---- main grid
    print(f"\nBLENDED BOOKS ({tag}) — (1-f) core + f sleeve, split reset weekly.  "
          f"f=0.00 is the untouched control.")
    print(f"{'core':<8}{'f':>6}{'thr':>5}{'bps':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
          f"{'2020':>8}{'2022':>8}{'H1':>7}{'H2':>7}{'OOS':>7}   verdict")
    print("-" * 138)
    RET = {}
    for bk in CORES:
        gc, tc = CORE[bk]
        for f in [0.0] + FRACS:
            for thr in (THRS if f > 0 else [0]):
                for c_bps in COSTS:
                    gs, ts = SLV[thr] if f > 0 else (gc * 0.0, tc * 0.0)
                    r = blend(gc, tc, gs, ts, f, c_bps, wk.loc[start:])
                    RET[(bk, f, thr, c_bps)] = r
                    base = b_g - b_t * c_bps / 1e4
                    cg, sh, dd = m(r)
                    h1, h2 = halves(r)
                    oos = m(r.loc[OOS_START:])[1]
                    v = verdict(r, base, spy, oos, ss_o)
                    mark = " <-" if c_bps == PROTO_COST else ""
                    print(f"{bk:<8}{f:6.2f}{thr:5d}{c_bps:5d}{cg:8.1%}{sh:8.3f}{dd:8.1%}"
                          f"{year_ret(r, 2020):8.1%}{year_ret(r, 2022):8.1%}"
                          f"{h1:7.3f}{h2:7.3f}{oos:7.3f}   {v}{mark}")
                    if c_bps == PROTO_COST:
                        rows.append(dict(tag=tag, core=bk, f=f, thr=thr, cagr=cg, sharpe=sh,
                                         dd=dd, h1=h1, h2=h2, oos=oos, verdict=v,
                                         pass4a=not fail4a(r, base),
                                         pass4b=not fail4b(r, spy, oos, ss_o)))
            print("-" * 138)

    # ---- the idea's own test: each sleeve arm vs its OWN control, same days
    print(f"IDEA 14's TEST ({tag}) — each blended arm minus its own f=0 control, "
          f"paired daily differences.")
    print(f"  {'core':<8}{'f':>6}{'thr':>5}{'bps':>5}{'dCAGR':>8}{'dSharpe':>9}{'dMaxDD':>9}"
          f"{'ann.diff':>10}{'t':>7}")
    for bk in CORES:
        for f in FRACS:
            for thr in THRS:
                for c_bps in (PROTO_COST, 25):
                    r, r0 = RET[(bk, f, thr, c_bps)], RET[(bk, 0.0, 0, c_bps)]
                    cg, sh, dd = m(r)
                    cg0, sh0, dd0 = m(r0)
                    ann, t = paired_t(r, r0)
                    print(f"  {bk:<8}{f:6.2f}{thr:5d}{c_bps:5d}{(cg - cg0) * 100:+8.2f}"
                          f"{sh - sh0:+9.3f}{(dd - dd0) * 100:+9.2f}{ann * 100:+10.2f}{t:+7.2f}")
        print()

    # ---- 4b margins at 10 bps
    print(f"MARGINS on each 4b bar at {PROTO_COST} bps ({tag}; positive = clears):")
    print(f"  {'core':<8}{'f':>6}{'thr':>5}{'H1-bar':>9}{'H2-bar':>9}{'OOS-bar':>9}"
          f"{'DD-slack(pp)':>14}{'CAGR-slack(pp)':>16}   binding")
    for bk in CORES:
        for f in [0.0] + FRACS:
            for thr in (THRS if f > 0 else [0]):
                r = RET[(bk, f, thr, PROTO_COST)]
                cg, sh, dd = m(r)
                h1, h2 = halves(r)
                oos = m(r.loc[OOS_START:])[1]
                mg = {"H1": h1 - s1, "H2": h2 - s2, "OOS": oos - ss_o,
                      "DD": (dd - 0.60 * sdd) * 100, "CAGR": (cg - 0.70 * sc) * 100}
                bind = min(mg, key=mg.get)
                print(f"  {bk:<8}{f:6.2f}{thr:5d}{mg['H1']:+9.4f}{mg['H2']:+9.4f}"
                      f"{mg['OOS']:+9.4f}{mg['DD']:+14.2f}{mg['CAGR']:+16.2f}   "
                      f"{bind} ({mg[bind]:+.4f})")

    # ---- rule 8 walk-forward
    print(f"\nRULE 8 WALK-FORWARD ({tag}) — (thr, f) chosen on IS <= {IS_END} only, "
          f"evaluated untouched on {OOS_START}+, at {PROTO_COST} bps.")
    is_spy = spy.loc[:IS_END]
    isc, iss, isdd = m(is_spy)
    oosc, ooss, oosdd = m(spy.loc[OOS_START:])
    print(f"  IS SPY {isc:.1%}/{iss:.3f}/{isdd:.1%};  OOS SPY {oosc:.1%}/{ooss:.3f}/{oosdd:.1%} "
          f"(OOS 4b bars: Sharpe>{ooss:.3f}, MaxDD>={0.60 * oosdd:.1%}, CAGR>={0.70 * oosc:.1%})")
    print(f"  {'core':<8}{'rule':<22}{'picked':<16}{'IS Sharpe':>10}   "
          f"{'OOS CAGR':>9}{'OOS Sharpe':>11}{'OOS MaxDD':>10}   OOS 4b")
    for bk in CORES:
        arms = [(f, thr) for f in FRACS for thr in THRS] + [(0.0, 0)]
        is_sh = {a: m(RET[(bk, a[0], a[1], PROTO_COST)].loc[:IS_END])[1] for a in arms}
        # two selection rules, both fixed before any OOS number was read
        pick_sharpe = max(arms, key=lambda a: is_sh[a])
        ok = [a for a in arms
              if m(RET[(bk, a[0], a[1], PROTO_COST)].loc[:IS_END])[2] >= 0.60 * isdd]
        pick_dd = max(ok, key=lambda a: is_sh[a]) if ok else pick_sharpe
        for rule, a in (("max IS Sharpe", pick_sharpe), ("max IS Sh | IS DD cap", pick_dd)):
            r_oos = RET[(bk, a[0], a[1], PROTO_COST)].loc[OOS_START:]
            cg, sh, dd = m(r_oos)
            bad = []
            if sh <= ooss: bad.append("Sharpe")
            if dd < 0.60 * oosdd: bad.append("DD")
            if cg < 0.70 * oosc: bad.append("CAGR")
            print(f"  {bk:<8}{rule:<22}{f'f={a[0]:.2f} thr={a[1]}':<16}{is_sh[a]:10.3f}   "
                  f"{cg:9.1%}{sh:11.3f}{dd:10.1%}   "
                  f"{'PASS' if not bad else 'FAIL (' + ','.join(bad) + ')'}")
        r_ctl = RET[(bk, 0.0, 0, PROTO_COST)].loc[OOS_START:]
        cg, sh, dd = m(r_ctl)
        print(f"  {bk:<8}{'(control f=0)':<22}{'-':<16}{is_sh[(0.0, 0)]:10.3f}   "
              f"{cg:9.1%}{sh:11.3f}{dd:10.1%}")

    return RET, CORE, SLV, start, wk


# ---------------------------------------------------------------- sensitivities
def sensitivities(px, tag, CORE, start, wk):
    """NOT read by any verdict or walk-forward.  Fixed-a-priori choices, varied once."""
    pxs = px[[t for t in SECTORS if t in px.columns]]
    print(f"\nSENSITIVITY ({tag}) — the three a-priori sleeve choices, varied one at a "
          f"time at f=0.25, {PROTO_COST} bps.  DIAGNOSTIC ONLY: no verdict reads this block.")
    print(f"  {'variant':<26}{'thr':>5}{'sleeve CAGR':>13}{'sleeve Sh':>11}{'turn/yr':>9}"
          f"   {'v1 dSharpe':>11}{'top20 dSharpe':>14}{'ew-all dSharpe':>15}")
    variants = [("primary (hyst, full, cash)", dict(hysteresis=True, alloc="full")),
                ("no-hysteresis exit", dict(hysteresis=False, alloc="full")),
                ("div4 allocation", dict(hysteresis=True, alloc="div4"))]
    for label, kw in variants:
        for thr in THRS:
            res = backtest(pxs, sleeve_weights(pxs, thr, **kw), cost_bps=0.0, freq="D")
            gs = res["returns"].reindex(px.index).fillna(0.0).loc[start:]
            ts = res["turnover"].reindex(px.index).fillna(0.0).loc[start:]
            rs = gs - ts * PROTO_COST / 1e4
            cg, sh, _ = m(rs)
            cells = []
            for bk in CORES:
                gc, tc = CORE[bk]
                r = blend(gc, tc, gs, ts, 0.25, PROTO_COST, wk.loc[start:])
                r0 = blend(gc, tc, gs * 0, ts * 0, 0.0, PROTO_COST, wk.loc[start:])
                cells.append(m(r)[1] - m(r0)[1])
            print(f"  {label:<26}{thr:5d}{cg:13.1%}{sh:11.3f}{turn_per_yr(ts):8.1f}x   "
                  f"{cells[0]:+11.3f}{cells[1]:+14.3f}{cells[2]:+15.3f}")


# ------------------------------------------------- is it the signal or the lag?
def execution_lag_decomposition(px, start):
    """Separate three possible causes of a KILL: no signal / costs / next-day execution.

    Note on the engine's convention: `backtest` sets held(t+1) = weights(t) and lets it
    earn close(t)->close(t+1), i.e. the fill happens AT the signal close, so the run
    already captures h=0 below — the most valuable day of a dip-buy.  Two extra arms
    bound that: a one-day EXECUTION LAG (fill one close later, forfeiting h=0), which is
    the realistic downside, and a one-day-EARLY arm, which is a look-ahead sign check —
    if the signal really is a dip-buy, buying the day before an entry must lose badly.
    Neither extra arm is used in any verdict.
    """
    pxs = px[[t for t in SECTORS if t in px.columns]]
    rets = pxs.pct_change()
    print("\nEXECUTION-LAG DECOMPOSITION (sector ETF panel; diagnostic, not a verdict).")
    print("Event study on ENTRY days (first day of an episode): mean forward daily return "
          "of the signalling name.")
    print(f"  h=0 is close(t)->close(t+1) — the day the engine's fill DOES capture; "
          f"h>=1 is what a one-day-later fill would get.")
    print(f"  {'thr':>4}{'entries':>9}" + "".join(f"{'h=' + str(h):>10}" for h in range(5))
          + f"{'sum h0-4':>11}{'uncond.':>10}")
    unc = rets.loc[start:].stack().mean()
    for thr in THRS:
        h = sleeve_state(pxs, thr)
        ent = h & ~h.shift(1, fill_value=False)
        ent = ent.loc[start:]
        cells, n = [], int(ent.values.sum())
        for lag in range(5):
            fwd = rets.shift(-1 - lag).loc[start:]
            cells.append(float(fwd.where(ent).stack().mean()))
        print(f"  {thr:4d}{n:9d}" + "".join(f"{c * 100:9.3f}%" for c in cells)
              + f"{sum(cells) * 100:10.3f}%{unc * 100:9.3f}%")

    print("\nSLEEVE UNDER BOTH EXECUTION CONVENTIONS (100% sleeve capital, daily):")
    print(f"  {'thr':>4}  {'execution':<30}{'0bps CAGR':>11}{'0bps Sh':>9}"
          f"{'10bps CAGR':>12}{'10bps Sh':>10}{'25bps Sh':>10}{'turn/yr':>9}")
    for thr in THRS:
        w = sleeve_weights(pxs, thr)
        for label, ww in (("as run (fill at signal close)", w),
                          ("+1 day execution lag", w.shift(1)),
                          ("1 day early (LOOK-AHEAD chk)", w.shift(-1))):
            res = backtest(pxs, ww, cost_bps=0.0, freq="D")
            gs = res["returns"].loc[start:]
            ts = res["turnover"].loc[start:]
            r0 = gs
            r10 = gs - ts * 10 / 1e4
            r25 = gs - ts * 25 / 1e4
            print(f"  {thr:4d}  {label:<30}{m(r0)[0]:11.1%}{m(r0)[1]:9.3f}"
                  f"{m(r10)[0]:12.1%}{m(r10)[1]:10.3f}{m(r25)[1]:10.3f}"
                  f"{turn_per_yr(ts):8.1f}x")


# ---------------------------------------------------------------- main
def main():
    print("=" * 138)
    print(f"Idea 14  rsi2-sleeve (cloud) | {SCRIPT} | {PROTO_COST} bps, next-day execution")
    print("=" * 138)

    px = load_universe()
    pxb = load_universe(broad=True)

    # harness check: analytic costs == engine costs (held/turnover do not depend on cost_bps)
    w = w_top20(px)
    a = backtest(px, w, cost_bps=10.0, freq="W")["returns"]
    b0 = backtest(px, w, cost_bps=0.0, freq="W")
    b = b0["returns"] - b0["turnover"] * 10 / 1e4
    assert float((a - b).abs().max()) < 1e-12, "analytic cost identity failed"
    print(f"harness: analytic-cost identity holds (max |diff| {float((a - b).abs().max()):.2e})")
    r2 = rsi(px[["SPY"]], 2)["SPY"]
    print(f"harness: RSI(2) on SPY — min {r2.min():.1f} max {r2.max():.1f} "
          f"median {r2.median():.1f}, %<10 {(r2 < 10).mean():.1%}, %>50 {(r2 > 50).mean():.1%}")

    rows = []
    execution_lag_decomposition(px, px.index[260])
    RET, CORE, SLV, start, wk = sweep(px, "universe.json (56)", rows)
    sensitivities(px, "universe.json (56)", CORE, start, wk)
    RETb, COREb, SLVb, startb, wkb = sweep(pxb, "universe_broad.json (136)", rows)
    sensitivities(pxb, "universe_broad.json (136)", COREb, startb, wkb)

    df = pd.DataFrame(rows)
    df.to_csv(Path(__file__).with_suffix("").as_posix() + ".grid.csv", index=False)

    print(f"\n{'=' * 138}")
    print("CROSS-UNIVERSE SUMMARY at 10 bps — an arm counts only if it passes on BOTH lists.")
    print("=" * 138)
    piv = df.pivot_table(index=["core", "f", "thr"], columns="tag",
                         values=["sharpe", "pass4a", "pass4b"])
    print(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    both4b = (df.groupby(["core", "f", "thr"])["pass4b"].sum() == 2)
    both4a = (df.groupby(["core", "f", "thr"])["pass4a"].sum() == 2)
    print(f"\narms passing 4b on BOTH universes: "
          f"{[k for k, v in both4b.items() if v] or 'NONE'}")
    print(f"arms passing 4a on BOTH universes: "
          f"{[k for k, v in both4a.items() if v] or 'NONE'}")
    sleeve_arms = df[df.f > 0]
    ctl = df[df.f == 0].set_index(["tag", "core"])["sharpe"]
    d = sleeve_arms.apply(lambda r: r.sharpe - ctl.loc[(r.tag, r.core)], axis=1)
    print(f"\nsleeve dSharpe vs own control over all {len(d)} (universe, core, f, thr) cells: "
          f"mean {d.mean():+.3f}, median {d.median():+.3f}, "
          f"positive in {int((d > 0).sum())}/{len(d)}")


if __name__ == "__main__":
    main()
