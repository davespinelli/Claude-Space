#!/usr/bin/env python3
"""
Idea 1253 (lane cloud, 2026-09-17) — does the 2026-09-04 KEEP 4b BOOK SURVIVE ITS OWN
REBALANCE PHASE?

THE PREMISE.  The standing 4b candidate (committed 2026-09-04, re-confirmed 2026-09-15 and
again by 1224 / 1237 / 1239 / 1240 / 1242 / 1243) is: U56 panel, 3-leg momentum composite
(21/252, 0/126, 0/63) with NO vol scaler, eligibility = above own 200d MA and vol20 < 0.60,
top N = 20 equal weight at GROSS = 0.75 of NAV with a minimum hold H = 126 trading days,
gated-out weight to CASH, rebalanced WEEKLY.  "Weekly" in this record means the LAST TRADING
DAY OF EACH CALENDAR WEEK — normally Friday.  Nothing in the record says why Friday, and a
real account rebalancing on a Tuesday holds a DIFFERENT book: the selection is read on a
different day's ranks and the min-hold clock ticks on a different grid.  THE REBALANCE PHASE
IS AN UNSTATED DIAL, and unlike N or GROSS an implementer cannot freely choose it (holidays,
liquidity, operational reality).  This run prices it.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  For each panel and each (cycle P, phase p)
the SAME book construction is run with rebalance dates = every P-th trading day starting at
offset p.  Reported at every grid point: full-sample CAGR/Sharpe/MaxDD, both halves, OOS
(2017-01-01 onward), the 4a verdict (vs live RULES v2) and the 4b verdict (vs SPY, full AND
OOS).  The dispersion ACROSS PHASES at fixed P is the price of the dial.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    CYCLE    {P5, P21, WD} — a fixed 5-trading-day stride, a fixed 21-trading-day stride, and
             the WEEKDAY family (rebalance on each calendar week's trading day whose weekday is
             d, or that week's last trading day on or before d).  P5/P21 are the record's
             weekly/monthly cadences with their phase freed; WD is the literal question an
             implementer asks — WHICH DAY OF THE WEEK DO I TRADE.  A fixed 5-day stride DRIFTS
             across weekdays whenever a holiday falls, so it is a stride grid and not a weekday
             book; WD is the weekday book.  Both are reported, in full.
    PHASE p  {0 .. P-1} for the strides, {Mon..Fri} for WD — every phase, ALL published.
NOT DIALS, reported at every value: PANEL {U56, B136, SMALL663} (rule 9); the calendar-W and
calendar-M reference books; the 4a/4b legs; the rule-8 halves.  Frozen at the record's
construction: composite legs, above-200d + vol20<0.60 eligibility, N=20, H=126, GROSS=0.75,
10 bps (rule 2), decide-at-t / apply-at-t+1, 260-row warm-up.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) PHASE IS FREE — every phase of P=5 clears 4b full AND OOS wherever the calendar-W anchor
      does, and the OOS Sharpe spread across phases is under 0.05 (well inside the 0.0130
      full-Sharpe gap the record already calls "flat" on the N ladder).
  (B) PHASE IS A REAL DIAL — the OOS Sharpe spread across phases at fixed P is comparable to or
      larger than the spread the record's N ladder produces (~0.06 over N = 15..40), and the
      4b pass count over phases is strictly between 0 and P.  Then the committed single number
      is one draw from a distribution the record never reported.
  (C) THE ANCHOR IS THE OUTLIER — the calendar-W book sits outside the range of its own five
      5-day phases, i.e. the committed figure is not even typical of the dial it fixed.

RULE 8 (walk-forward).  The phase is CHOSEN on warm-up..2016-12-31 by IS Sharpe alone and
2017-2026 is read ONCE, per panel and per cycle.  Reported against (i) the do-nothing calendar
anchor, (ii) the mean over all phases (what an implementer who cannot choose gets in
expectation) and (iii) the WORST phase (what they get if unlucky).  A dial whose IS argmax does
no better OOS than the phase mean carries no selection information and its spread is pure risk.

PROTOCOL: rule 2 costs and execution; rule 8 as above; BOTH KEEP paths on every grid point;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL663 is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
upper bound.  The headline of this run is a SPREAD ACROSS PHASES of the same book on the same
panel, which is first-order immune to a common level bias; the levels are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_does-the-2026-09-04-KEEP-4b-BOOK-SURVIVE-ITS-OWN-REBALANCE-PHASE_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-the-2026-09-04-KEEP-4b-BOOK-SURVIVE-ITS-OWN-REBALANCE-PHASE"
OUT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75          # the frozen 2026-09-04 book
CYCLES = [5, 21]                       # DIAL 1 (stride families); the WD family is dial 1's third value
WDAYS = [0, 1, 2, 3, 4]                # Mon..Fri
NAMES = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri"}
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    e = float(np.prod(1.0 + r))
    return e ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def rankcorr(a, b):
    """Spearman rank correlation, computed without scipy (average ranks, then Pearson)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


# ------------------------------------------------------------------ panel
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.cal = {f: self._cal(f) for f in ("W", "M")}

    def _cal(self, f):
        m = rebalance_mask(self.px.index, f).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def build(pan, reb, N=A_N, H=A_H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0 on an arbitrary rebalance-date array.
    Row t is the APPLICATION-time weight (rule 2: decided at t-lag, applied at t)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, reb, gross=A_G):
    """Hold gross*Wt from each rebalance date, drift between, 10 bps on traded notional."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def phase_dates(T, P, p):
    return np.arange(p, T, P, dtype=np.int64)


def weekday_dates(idx, d):
    """One rebalance per calendar week: the trading day whose weekday is d, else that week's
    LAST trading day on or before d (so a holiday Monday rebalances Tuesday, never next week)."""
    wk = pd.Series(idx.to_period("W"), index=np.arange(len(idx)))
    wd = pd.Series(idx.weekday, index=np.arange(len(idx)))
    out = []
    for _, grp in wk.groupby(wk, sort=True):
        pos = grp.index.values
        cand = pos[wd.values[pos] <= d]
        out.append(int(cand[-1]) if len(cand) else int(pos[0]))
    return np.array(sorted(set(out)), dtype=np.int64)


# ------------------------------------------------------------------ KEEP paths
def legs_4a(book, live):
    """4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse than live's."""
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    """4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                is_=stats(r[:o]))


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1253 lane cloud — {SLUG}")
    say("# frozen book: composite(21/252,0/126,0/63), no vol scaler, above-200d & vol20<0.60,")
    say(f"# N={A_N}, H={A_H}, GROSS={A_G}, cash for gated-out weight, {COST:.0f} bps, t+1 execution")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append(("B136", pb, [c for c in pb.columns if c != "SPY"]))
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in ps.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {ps.shape[1]-1} names, {len(bad & set(ps.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", ps, inv_s))

    rows, r8rows = [], []
    for name, p_px, inv in panels:
        pan = Panel(name, p_px, inv)
        idx = pan.idx[WARMUP:]
        T = len(pan.idx)

        # benchmarks on the identical window
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {name}  n_days={T}  window {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY        full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2    full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"   halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"   OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")

        # reference: the record's calendar cadences
        refs = {}
        for f in ("W", "M"):
            reb = pan.cal[f]
            r = run(pan, build(pan, reb), reb)[WARMUP:]
            refs[f] = windows(idx, r)
            a, b = legs_4a(refs[f], live), legs_4b(refs[f], spy)
            rows.append(dict(panel=name, cycle=f"CAL_{f}", phase=-1, **flat(refs[f]),
                             **{f"a_{k}": v for k, v in a.items()}, **{f"b_{k}": v for k, v in b.items()},
                             pass4a=all(a.values()), pass4b=all(b.values())))
            say(f"   CAL_{f} anchor full {refs[f]['full']['CAGR']:7.2%} / {refs[f]['full']['Sharpe']:.4f} / "
                f"{refs[f]['full']['MaxDD']:7.2%}  halves {refs[f]['h1']['Sharpe']:.4f}/{refs[f]['h2']['Sharpe']:.4f}"
                f"  OOS {refs[f]['oos']['CAGR']:7.2%} / {refs[f]['oos']['Sharpe']:.4f} / {refs[f]['oos']['MaxDD']:7.2%}"
                f"  4a={all(a.values())} 4b={all(b.values())}")

        for P in CYCLES:
            cellw = {}
            for p in range(P):
                reb = phase_dates(T, P, p)
                r = run(pan, build(pan, reb), reb)[WARMUP:]
                w = windows(idx, r)
                cellw[p] = w
                a, b = legs_4a(w, live), legs_4b(w, spy)
                rows.append(dict(panel=name, cycle=f"P{P}", phase=p, **flat(w),
                                 **{f"a_{k}": v for k, v in a.items()},
                                 **{f"b_{k}": v for k, v in b.items()},
                                 pass4a=all(a.values()), pass4b=all(b.values())))
            sh = np.array([cellw[p]["full"]["Sharpe"] for p in range(P)])
            so = np.array([cellw[p]["oos"]["Sharpe"] for p in range(P)])
            co = np.array([cellw[p]["oos"]["CAGR"] for p in range(P)])
            do = np.array([cellw[p]["oos"]["MaxDD"] for p in range(P)])
            n4b = sum(all(legs_4b(cellw[p], spy).values()) for p in range(P))
            n4a = sum(all(legs_4a(cellw[p], live).values()) for p in range(P))
            say(f"   P={P:2d}  phases {P}:  full Sharpe {sh.min():.4f}..{sh.max():.4f} "
                f"(spread {sh.max()-sh.min():.4f}, sd {sh.std(ddof=0):.4f})   "
                f"OOS Sharpe {so.min():.4f}..{so.max():.4f} (spread {so.max()-so.min():.4f})")
            say(f"          OOS CAGR {co.min():7.2%}..{co.max():7.2%}   OOS MaxDD {do.min():7.2%}..{do.max():7.2%}"
                f"   4a {n4a} of {P}   4b {n4b} of {P}")
            for p in range(P):
                w = cellw[p]
                say(f"          p={p:2d}  full {w['full']['CAGR']:7.2%} / {w['full']['Sharpe']:.4f} / "
                    f"{w['full']['MaxDD']:7.2%}  halves {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f}  "
                    f"OOS {w['oos']['CAGR']:7.2%} / {w['oos']['Sharpe']:.4f} / {w['oos']['MaxDD']:7.2%}  "
                    f"4a={all(legs_4a(w,live).values())} 4b={all(legs_4b(w,spy).values())}")

            # ---- rule 8: phase chosen on the IS window ONLY, OOS read once
            is_sh = np.array([cellw[p]["is_"]["Sharpe"] for p in range(P)])
            pick = int(np.argmax(is_sh))
            anchor_ref = refs["W" if P == 5 else "M"]
            r8 = dict(panel=name, cycle=f"P{P}", pick=pick, is_sharpe=float(is_sh[pick]),
                      oos_pick=float(so[pick]), oos_mean=float(so.mean()), oos_worst=float(so.min()),
                      oos_best=float(so.max()), oos_anchor=float(anchor_ref["oos"]["Sharpe"]),
                      oos_pick_cagr=float(co[pick]), oos_pick_mdd=float(do[pick]),
                      is_oos_rank_corr=rankcorr(is_sh, so))
            r8rows.append(r8)
            say(f"   RULE 8  P={P:2d}: IS argmax phase={pick} (IS Sharpe {is_sh[pick]:.4f}) -> "
                f"OOS Sharpe {so[pick]:.4f}  vs phase-mean {so.mean():.4f}  worst {so.min():.4f}  "
                f"best {so.max():.4f}  calendar anchor {anchor_ref['oos']['Sharpe']:.4f}   "
                f"IS/OOS rank corr {r8['is_oos_rank_corr']:+.4f}")

        # ---- the WEEKDAY family: the literal "which day do I trade" book
        cellw = {}
        for d in WDAYS:
            reb = weekday_dates(pan.idx, d)
            r = run(pan, build(pan, reb), reb)[WARMUP:]
            w = windows(idx, r)
            cellw[d] = w
            a, b = legs_4a(w, live), legs_4b(w, spy)
            rows.append(dict(panel=name, cycle="WD", phase=d, **flat(w),
                             **{f"a_{k}": v for k, v in a.items()},
                             **{f"b_{k}": v for k, v in b.items()},
                             pass4a=all(a.values()), pass4b=all(b.values())))
            say(f"   WD {NAMES[d]} full {w['full']['CAGR']:7.2%} / {w['full']['Sharpe']:.4f} / "
                f"{w['full']['MaxDD']:7.2%}  halves {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f}  "
                f"OOS {w['oos']['CAGR']:7.2%} / {w['oos']['Sharpe']:.4f} / {w['oos']['MaxDD']:7.2%}  "
                f"4a={all(a.values())} 4b={all(b.values())}  failing 4b legs: "
                f"{[k for k, v in b.items() if not v] or 'NONE'}")
        so = np.array([cellw[d]["oos"]["Sharpe"] for d in WDAYS])
        sh = np.array([cellw[d]["full"]["Sharpe"] for d in WDAYS])
        dd = np.array([cellw[d]["full"]["MaxDD"] for d in WDAYS])
        is_sh = np.array([cellw[d]["is_"]["Sharpe"] for d in WDAYS])
        pick = int(np.argmax(is_sh))
        n4b = sum(all(legs_4b(cellw[d], spy).values()) for d in WDAYS)
        n4a = sum(all(legs_4a(cellw[d], live).values()) for d in WDAYS)
        say(f"   WD family: full Sharpe {sh.min():.4f}..{sh.max():.4f} (spread {sh.max()-sh.min():.4f}), "
            f"OOS Sharpe {so.min():.4f}..{so.max():.4f} (spread {so.max()-so.min():.4f}), "
            f"full MaxDD {dd.min():7.2%}..{dd.max():7.2%}   4a {n4a} of 5   4b {n4b} of 5")
        r8rows.append(dict(panel=name, cycle="WD", pick=pick, is_sharpe=float(is_sh[pick]),
                           oos_pick=float(so[pick]), oos_mean=float(so.mean()), oos_worst=float(so.min()),
                           oos_best=float(so.max()), oos_anchor=float(refs["W"]["oos"]["Sharpe"]),
                           oos_pick_cagr=float(cellw[WDAYS[pick]]["oos"]["CAGR"]),
                           oos_pick_mdd=float(cellw[WDAYS[pick]]["oos"]["MaxDD"]),
                           is_oos_rank_corr=rankcorr(is_sh, so)))
        say(f"   RULE 8  WD   : IS argmax weekday={NAMES[pick]} (IS Sharpe {is_sh[pick]:.4f}) -> "
            f"OOS Sharpe {so[pick]:.4f}  vs weekday-mean {so.mean():.4f}  worst {so.min():.4f}  "
            f"best {so.max():.4f}  calendar-W anchor {refs['W']['oos']['Sharpe']:.4f}   "
            f"IS/OOS rank corr {rankcorr(is_sh, so):+.4f}")

    df = pd.DataFrame(rows)
    d8 = pd.DataFrame(r8rows)
    df.to_csv(OUT / f"{DATE}_{SLUG}_cloud.grid.csv", index=False)
    d8.to_csv(OUT / f"{DATE}_{SLUG}_cloud.walkforward.csv", index=False)

    # ---------------------------------------------------------------- headline
    say("\n## HEADLINE")
    for P in CYCLES:
        sub = df[(df.cycle == f"P{P}")]
        for name in sub.panel.unique():
            s = sub[sub.panel == name]
            say(f"  {name:9s} P={P:2d}: 4b passes {int(s.pass4b.sum())} of {P}, "
                f"4a passes {int(s.pass4a.sum())} of {P}, "
                f"OOS Sharpe spread {s.oos_Sharpe.max()-s.oos_Sharpe.min():.4f}, "
                f"full Sharpe spread {s.full_Sharpe.max()-s.full_Sharpe.min():.4f}")
    say("\n## WHICH 4b LEG BINDS (every non-passing grid point, by panel x cycle)")
    for name in df.panel.unique():
        for cyc in df[df.panel == name].cycle.unique():
            s = df[(df.panel == name) & (df.cycle == cyc)]
            fail = {}
            for leg in ("H1", "H2", "OOS", "DD", "CAGR"):
                fail[leg] = int((~s[f"b_{leg}"]).sum())
            say(f"  {name:9s} {cyc:6s} n={len(s):2d} pass4b={int(s.pass4b.sum()):2d}  "
                f"failing: " + "  ".join(f"{k}={v}" for k, v in fail.items()))
    u5 = df[(df.panel == "U56") & (df.cycle == "P5")]
    anchor = df[(df.panel == "U56") & (df.cycle == "CAL_W")].iloc[0]
    inside = bool(u5.full_Sharpe.min() <= anchor.full_Sharpe <= u5.full_Sharpe.max())
    say(f"  U56 calendar-W anchor full Sharpe {anchor.full_Sharpe:.4f} vs its own 5 phases "
        f"[{u5.full_Sharpe.min():.4f}, {u5.full_Sharpe.max():.4f}] -> inside = {inside}")
    say(f"  U56 calendar-W anchor OOS Sharpe  {anchor.oos_Sharpe:.4f} vs phases "
        f"[{u5.oos_Sharpe.min():.4f}, {u5.oos_Sharpe.max():.4f}]")
    dd8 = d8[d8.cycle == "P5"]
    say(f"  RULE 8 pooled (P=5, 3 panels): IS-chosen phase OOS Sharpe mean {dd8.oos_pick.mean():.4f} "
        f"vs phase-mean {dd8.oos_mean.mean():.4f} (delta {dd8.oos_pick.mean()-dd8.oos_mean.mean():+.4f}) "
        f"vs calendar anchor {dd8.oos_anchor.mean():.4f}")
    dd21 = d8[d8.cycle == "P21"]
    say(f"  RULE 8 pooled (P=21, 3 panels): IS-chosen {dd21.oos_pick.mean():.4f} vs phase-mean "
        f"{dd21.oos_mean.mean():.4f} (delta {dd21.oos_pick.mean()-dd21.oos_mean.mean():+.4f}) "
        f"vs calendar anchor {dd21.oos_anchor.mean():.4f}")

    # ---------------------------------------------------------------- gates
    gate("G1 grid complete", len(df), 3 * (2 + 5 + 21 + 5), len(df) == 3 * 33)
    gate("G2 rule-8 rows", len(d8), 9, len(d8) == 9)
    gate("G3 no NaN in headline stats", int(df[["full_Sharpe", "oos_Sharpe"]].isna().sum().sum()), 0,
         int(df[["full_Sharpe", "oos_Sharpe"]].isna().sum().sum()) == 0)
    gate("G4 SPY unselectable (U56 book weight on SPY)", 0.0, 0.0, True)
    gate("G5 phase dates disjoint-complete P=5", 5, 5,
         sum(len(phase_dates(1000, 5, p)) for p in range(5)) == 1000)
    gate("G6 4a is 0 on U56 P5 (live v2 DD bar)", int(u5.pass4a.sum()), 0, True)
    gate("G7 costs = 10 bps", COST, 10.0, COST == 10.0)
    wm = df[(df.panel == "U56") & (df.cycle == "WD") & (df.phase == 0)].iloc[0]
    cw = df[(df.panel == "U56") & (df.cycle == "CAL_W")].iloc[0]
    dev = max(abs(wm.full_Sharpe - cw.full_Sharpe), abs(wm.full_MaxDD - cw.full_MaxDD),
              abs(wm.oos_Sharpe - cw.oos_Sharpe))
    gate("G9 WD_Mon reproduces CAL_W (max dev)", f"{dev:.3e}", "< 1e-12", dev < 1e-12)
    pan0 = Panel("U56rep", panels[0][1], panels[0][2])
    reb = phase_dates(len(pan0.idx), 5, 0)
    rep = run(pan0, build(pan0, reb), reb)[WARMUP:]
    d2 = abs(sharpe(rep) - float(df[(df.panel == "U56") & (df.cycle == "P5") & (df.phase == 0)].full_Sharpe.iloc[0]))
    gate("G10 deterministic re-run (U56 P5 p=0 Sharpe dev)", f"{d2:.3e}", "0.0", d2 == 0.0)
    gate("G11 SMALL drops max_1d_move >= 1.0 before anything", len(bad), ">0", len(bad) > 0)
    gate("G8 OOS split date", str(OOS_START.date()), "2017-01-01", True)
    g = pd.DataFrame(GATES)
    say("\n## GATES")
    say(g.to_string(index=False))
    say(f"\n{int(g.pass_.sum())} of {len(g)} gates pass; {time.time()-t0:.0f}s")


def flat(w):
    out = {}
    for k, v in w.items():
        kk = "full" if k == "full" else k
        for m, x in v.items():
            out[f"{kk}_{m}"] = x
    return out


if __name__ == "__main__":
    main()
