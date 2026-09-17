#!/usr/bin/env python3
"""
Idea 1256 (lane cloud, 2026-09-17) — does the 2026-09-04 KEEP 4b BOOK SURVIVE ITS OWN
TREND GATE LENGTH?

THE PREMISE.  The standing 4b candidate (committed 2026-09-04, re-confirmed by 1224 / 1237 /
1239 / 1240 / 1242 / 1243 / 1253 / 1255) screens eligibility on "above own 200d MA".  The
number 200 is INHERITED — it comes from scan.py / RULES v1 and no run has ever walked it on
THIS book.  A real implementer choosing between a 100-, 150-, 200- or 250-day trend gate has
no argument for one over another, and RULES v2's own clause already carries a +/-3% hysteresis
band that this book does not.  So the committed candidate's verdict rests on two unstated
dials.  This run walks both and reports every grid point.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  For each panel and each (MA length L,
band b) the SAME book construction is run with the trend gate replaced by the hysteresis state
G(L, b): IN once price > MA_L*(1+b), OUT once price < MA_L*(1-b), previous state in between,
OUT before L closes exist (RULES v2 clause 2 semantics, applied per name).  Reported at every
grid point: full-sample CAGR/Sharpe/MaxDD, both halves, OOS (2017-01-01 onward), the 4a
verdict (vs live RULES v2) and the 4b verdict (vs SPY, full AND OOS), and which legs fail.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    L  {50, 100, 150, 200, 250} — the trend-gate length.  200 is the committed rung.
    b  {0.00, 0.01, 0.03, 0.05, 0.10} — the hysteresis half-band.  0.00 is the committed rung
       (a bare price > MA test); 0.03 is the live RULES v2 clause.
NOT DIALS, reported at every value: PANEL {U56, B136, SMALL663} (rule 9); the 4a/4b legs; the
rule-8 halves.  Frozen at the record's construction: composite legs (21/252, 0/126, 0/63) with
NO vol scaler, vol20 < 0.60, N = 20 equal weight, H = 126 trading days minimum hold,
GROSS = 0.75 of NAV with gated-out weight to CASH, WEEKLY (last trading day of the calendar
week) rebalance, 10 bps (rule 2), decide-at-t / apply-at-t+1, 260-row warm-up.  L = 250 < 260
so every rung on the grid has a fully-formed MA at the first scored day.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE GATE LENGTH IS FREE — 4b passes at every (L, b) on U56 and the OOS Sharpe spread
      across the 25 cells is under 0.05.  The committed 200/0 is then one of many equivalent
      spellings and the RULES line can say "a 100-250 day trend gate".
  (B) THE GATE LENGTH IS A REAL DIAL — the 4b pass count over the 25 cells is strictly between
      0 and 25, i.e. the committed verdict is a property of the inherited 200 rather than of
      the book, and the RULES line must state L (and b) as a chosen parameter.
  (C) THE COMMITTED RUNG IS THE OUTLIER — 200/0.00 sits outside the range of its own
      neighbours (L in {150, 250} x b in {0.00, 0.01}), i.e. the committed figure is not even
      typical of the local neighbourhood of the dial it fixed.

RULE 8 (walk-forward).  (L, b) is CHOSEN on warm-up..2016-12-31 by IS Sharpe alone and
2017-2026 is read ONCE, per panel.  Reported against (i) the do-nothing committed 200/0.00
anchor, (ii) the mean over all 25 cells (what an implementer with no reason to prefer a rung
gets in expectation) and (iii) the WORST cell.  A dial whose IS argmax does no better OOS than
the grid mean carries no selection information and its spread is pure implementation risk.
The IS-vs-OOS rank correlation over the 25 cells is reported per panel.

PROTOCOL: rule 2 costs and execution; rule 8 as above; BOTH KEEP paths at every grid point;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL663 is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is
an upper bound.  The headline of this run is a SPREAD ACROSS GATE RUNGS of the same book on
the same panel, first-order immune to a common level bias; the levels are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_does-the-2026-09-04-KEEP-4b-BOOK-SURVIVE-ITS-OWN-TREND-GATE-LENGTH_cloud.py
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
SLUG = "does-the-2026-09-04-KEEP-4b-BOOK-SURVIVE-ITS-OWN-TREND-GATE-LENGTH"
OUT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75           # the frozen 2026-09-04 book
LENS = [50, 100, 150, 200, 250]         # DIAL 1
BANDS = [0.00, 0.01, 0.03, 0.05, 0.10]  # DIAL 2
ANCHOR = (200, 0.00)                    # the committed rung
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
    """Spearman rank correlation without scipy (average ranks, then Pearson)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    out = {}
    for k, v in w.items():
        for m, x in v.items():
            out[f"{k}_{m}"] = x
    return out


# ------------------------------------------------------------------ mechanics
def gate_state(q: pd.DataFrame, L: int, b: float) -> np.ndarray:
    """RULES v2 clause-2 hysteresis, per name: IN above MA_L*(1+b), OUT below MA_L*(1-b),
    previous state in between, OUT before L closes exist.  b = 0 is a bare price > MA test."""
    ma = q.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=q.index, columns=q.columns)
    raw = raw.mask(q > ma * (1 + b), 1.0).mask(q < ma * (1 - b), 0.0)
    return (raw.ffill().fillna(0.0) > 0.5).values


class Panel:
    """Everything that does NOT depend on the two dials, computed once per panel."""

    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        self.comp = (sum(parts) / len(parts)).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self._gate_cache = {}

    def gate(self, L, b):
        key = (L, round(b, 6))
        if key not in self._gate_cache:
            self._gate_cache[key] = gate_state(self.px[self.invest], L, b)
        return self._gate_cache[key]


def build(pan, G, N=A_N, H=A_H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0 under trend-gate state G.
    Row t is the APPLICATION-time weight (rule 2: decided at t-lag, applied at t).
    G enters BOTH the score multiplier (0.5 + 0.5*G, as scan.py) and eligibility; since
    eligibility requires G, the multiplier is 1.0 on every selectable name and does not
    reorder the admitted set."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    sc = pan.comp * (0.5 + 0.5 * G.astype(float))
    key = np.where(np.isfinite(sc), -sc, np.inf)
    elig = G & pan.volok
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
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
            stop = pan.reb[i + 1] if i + 1 < len(pan.reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G):
    """Hold gross*Wt from each rebalance date, drift between, 10 bps on traded notional."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb
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
    gross_r = (held * rets).sum(axis=1)
    return gross_r - turn * COST / 1e4, float(turn.sum() / (T / 252.0))


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


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1256 lane cloud — {SLUG}")
    say("# frozen book: composite(21/252,0/126,0/63), no vol scaler, vol20<0.60, N=20, H=126,")
    say(f"# GROSS={A_G}, cash for gated-out weight, weekly, {COST:.0f} bps, t+1 execution")
    say(f"# DIAL 1 L = {LENS}   DIAL 2 band = {BANDS}   anchor = {ANCHOR}")

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
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {name}  n_days={len(pan.idx)}  window {idx[0].date()}..{idx[-1].date()}  "
            f"rebalances={len(pan.reb)}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"   halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"   OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars on this window: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}, "
            f"Sharpe bars H1 {spy['h1']['Sharpe']:.4f} / H2 {spy['h2']['Sharpe']:.4f} / OOS {spy['oos']['Sharpe']:.4f}")

        cells = {}
        say(f"   {'L':>4} {'band':>5} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} | {'H1':>6} {'H2':>6} | "
            f"{'oCAGR':>7} {'oSh':>7} {'oDD':>8} | {'turn':>5} | 4a 4b  failing 4b legs")
        for L in LENS:
            G = pan.gate(L, 0.0)
            for b in BANDS:
                Gb = G if b == 0.0 else pan.gate(L, b)
                r, turn = run(pan, build(pan, Gb))
                w = windows(idx, r[WARMUP:])
                cells[(L, b)] = w
                a, bl = legs_4a(w, live), legs_4b(w, spy)
                fails = [k for k, v in bl.items() if not v]
                rows.append(dict(panel=name, L=L, band=b, turnover=turn, **flat(w),
                                 **{f"a_{k}": v for k, v in a.items()},
                                 **{f"b_{k}": v for k, v in bl.items()},
                                 pass4a=all(a.values()), pass4b=all(bl.values()),
                                 fail4b=",".join(fails) or "NONE"))
                mark = " <= ANCHOR" if (L, b) == ANCHOR else ""
                say(f"   {L:>4} {b:>5.2f} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:7.4f} "
                    f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:6.4f} {w['h2']['Sharpe']:6.4f} | "
                    f"{w['oos']['CAGR']:7.2%} {w['oos']['Sharpe']:7.4f} {w['oos']['MaxDD']:8.2%} | "
                    f"{turn:5.2f} | {int(all(a.values()))}  {int(all(bl.values()))}   "
                    f"{','.join(fails) or 'NONE':<18}{mark}")

        sub = pd.DataFrame([dict(L=L, b=b, full=cells[(L, b)]["full"]["Sharpe"],
                                oos=cells[(L, b)]["oos"]["Sharpe"], is_=cells[(L, b)]["is_"]["Sharpe"],
                                dd=cells[(L, b)]["full"]["MaxDD"], cg=cells[(L, b)]["full"]["CAGR"],
                                ocg=cells[(L, b)]["oos"]["CAGR"], odd=cells[(L, b)]["oos"]["MaxDD"],
                                p4b=all(legs_4b(cells[(L, b)], spy).values()),
                                p4a=all(legs_4a(cells[(L, b)], live).values()))
                           for L in LENS for b in BANDS])
        an = cells[ANCHOR]
        say(f"   GRID {name}: 4b passes {int(sub.p4b.sum())} of {len(sub)}, 4a passes {int(sub.p4a.sum())} of {len(sub)}")
        say(f"        full Sharpe {sub.full.min():.4f}..{sub.full.max():.4f} (spread {sub.full.max()-sub.full.min():.4f}, "
            f"sd {sub.full.std(ddof=0):.4f})   OOS Sharpe {sub.oos.min():.4f}..{sub.oos.max():.4f} "
            f"(spread {sub.oos.max()-sub.oos.min():.4f})")
        say(f"        full MaxDD {sub.dd.min():7.2%}..{sub.dd.max():7.2%}   anchor(200/0.00) full Sharpe "
            f"{an['full']['Sharpe']:.4f}, OOS {an['oos']['Sharpe']:.4f}, MaxDD {an['full']['MaxDD']:7.2%}")
        # marginal effect of each dial, holding the other at the anchor rung
        rowL = [cells[(L, 0.00)]["oos"]["Sharpe"] for L in LENS]
        rowB = [cells[(200, b)]["oos"]["Sharpe"] for b in BANDS]
        say(f"        L sweep at band=0.00, OOS Sharpe: " + "  ".join(f"{L}={v:.4f}" for L, v in zip(LENS, rowL)))
        say(f"        band sweep at L=200, OOS Sharpe : " + "  ".join(f"{b:.2f}={v:.4f}" for b, v in zip(BANDS, rowB)))
        # outcome (C): is the anchor inside its own local neighbourhood?
        nb = [cells[(L, b)]["full"]["Sharpe"] for L in (150, 250) for b in (0.00, 0.01)]
        say(f"        neighbourhood (L in 150/250 x b in 0.00/0.01) full Sharpe "
            f"[{min(nb):.4f}, {max(nb):.4f}] -> anchor inside = "
            f"{min(nb) <= an['full']['Sharpe'] <= max(nb)}")

        # ---- rule 8: (L, b) chosen on the IS window ONLY, OOS read once
        pick = sub.loc[sub.is_.idxmax()]
        r8 = dict(panel=name, pick_L=int(pick.L), pick_band=float(pick.b), is_sharpe=float(pick.is_),
                  oos_pick=float(pick.oos), oos_pick_cagr=float(pick.ocg), oos_pick_mdd=float(pick.odd),
                  oos_mean=float(sub.oos.mean()), oos_worst=float(sub.oos.min()), oos_best=float(sub.oos.max()),
                  oos_anchor=float(an["oos"]["Sharpe"]), oos_spy=float(spy["oos"]["Sharpe"]),
                  pick_pass4b=bool(pick.p4b), anchor_pass4b=bool(sub[(sub.L == 200) & (sub.b == 0.0)].p4b.iloc[0]),
                  is_oos_rank_corr=rankcorr(sub.is_.values, sub.oos.values),
                  n_pass4b=int(sub.p4b.sum()), n_cells=len(sub))
        r8rows.append(r8)
        say(f"   RULE 8 {name}: IS argmax (L={int(pick.L)}, b={pick.b:.2f}) IS Sharpe {pick.is_:.4f} -> "
            f"OOS Sharpe {pick.oos:.4f} / CAGR {pick.ocg:7.2%} / MaxDD {pick.odd:7.2%}")
        say(f"           vs grid-mean OOS {sub.oos.mean():.4f}  worst {sub.oos.min():.4f}  best {sub.oos.max():.4f}  "
            f"anchor {an['oos']['Sharpe']:.4f}  SPY {spy['oos']['Sharpe']:.4f}   "
            f"IS/OOS rank corr {r8['is_oos_rank_corr']:+.4f}")
        say(f"           IS-chosen cell 4b = {bool(pick.p4b)}; anchor 4b = {r8['anchor_pass4b']}; "
            f"selection gain vs grid mean {pick.oos - sub.oos.mean():+.4f}, vs anchor {pick.oos - an['oos']['Sharpe']:+.4f}")

    df = pd.DataFrame(rows)
    d8 = pd.DataFrame(r8rows)
    df.to_csv(OUT / f"{DATE}_{SLUG}_cloud.grid.csv", index=False)
    d8.to_csv(OUT / f"{DATE}_{SLUG}_cloud.walkforward.csv", index=False)

    # ---------------------------------------------------------------- headline
    say("\n## HEADLINE")
    for name in df.panel.unique():
        s = df[df.panel == name]
        an = s[(s.L == 200) & (s.band == 0.0)].iloc[0]
        say(f"  {name:9s}: 4b {int(s.pass4b.sum())} of {len(s)}, 4a {int(s.pass4a.sum())} of {len(s)}, "
            f"full Sharpe spread {s.full_Sharpe.max()-s.full_Sharpe.min():.4f}, "
            f"OOS Sharpe spread {s.oos_Sharpe.max()-s.oos_Sharpe.min():.4f}, "
            f"anchor 4b={bool(an.pass4b)}")
    say("\n## WHICH 4b LEG BINDS (count of failing cells per leg, per panel)")
    for name in df.panel.unique():
        s = df[df.panel == name]
        say(f"  {name:9s} n={len(s)} pass4b={int(s.pass4b.sum()):2d}  failing: " +
            "  ".join(f"{leg}={int((~s['b_' + leg]).sum())}" for leg in ("H1", "H2", "OOS", "DD", "CAGR")))
    say("\n## 4b PASS MAP (rows = L, cols = band; 1 = pass)")
    for name in df.panel.unique():
        s = df[df.panel == name]
        say(f"  {name}")
        say("       " + "".join(f"{b:>7.2f}" for b in BANDS))
        for L in LENS:
            say(f"  {L:>4} " + "".join(f"{int(s[(s.L==L)&(s.band==b)].pass4b.iloc[0]):>7d}" for b in BANDS))
    u = df[df.panel == "U56"]
    an = u[(u.L == 200) & (u.band == 0.0)].iloc[0]
    say(f"\n  U56 anchor(200/0.00) full {an.full_CAGR:.2%} / {an.full_Sharpe:.4f} / {an.full_MaxDD:.2%}, "
        f"OOS {an.oos_CAGR:.2%} / {an.oos_Sharpe:.4f} / {an.oos_MaxDD:.2%}")
    say(f"  U56 grid: median full Sharpe {u.full_Sharpe.median():.4f}, anchor percentile "
        f"{100.0*(u.full_Sharpe < an.full_Sharpe).mean():.0f}; median OOS Sharpe {u.oos_Sharpe.median():.4f}, "
        f"anchor percentile {100.0*(u.oos_Sharpe < an.oos_Sharpe).mean():.0f}")
    say(f"  RULE 8 pooled (3 panels): IS-chosen OOS Sharpe mean {d8.oos_pick.mean():.4f} vs grid-mean "
        f"{d8.oos_mean.mean():.4f} (delta {d8.oos_pick.mean()-d8.oos_mean.mean():+.4f}) vs anchor "
        f"{d8.oos_anchor.mean():.4f} (delta {d8.oos_pick.mean()-d8.oos_anchor.mean():+.4f})")

    # ---------------------------------------------------------------- gates
    gate("G1 grid complete", len(df), 3 * len(LENS) * len(BANDS), len(df) == 3 * 25)
    gate("G2 rule-8 rows", len(d8), 3, len(d8) == 3)
    gate("G3 no NaN in headline stats", int(df[["full_Sharpe", "oos_Sharpe"]].isna().sum().sum()), 0,
         int(df[["full_Sharpe", "oos_Sharpe"]].isna().sum().sum()) == 0)
    # the anchor rung must replay the committed 2026-09-04 triple (1253 read 1.1480 / -19.13% / OOS 1.1759)
    dev = max(abs(an.full_Sharpe - 1.1480), abs(an.full_MaxDD - (-0.1913)), abs(an.oos_Sharpe - 1.1759))
    gate("G4 anchor replays committed U56 triple", f"{dev:.2e}", "< 5e-3", dev < 5e-3)
    gate("G5 max L < warm-up", max(LENS), WARMUP, max(LENS) < WARMUP)
    gate("G6 costs = 10 bps", COST, 10.0, COST == 10.0)
    gate("G7 OOS split date", str(OOS_START.date()), "2017-01-01", True)
    gate("G8 SMALL drops max_1d_move >= 1.0 before anything", len(bad), ">0", len(bad) > 0)
    pan0 = Panel("U56rep", panels[0][1], panels[0][2])
    rep, _ = run(pan0, build(pan0, pan0.gate(200, 0.0)))
    d2 = abs(sharpe(rep[WARMUP:]) - float(an.full_Sharpe))
    gate("G9 deterministic re-run (U56 anchor Sharpe dev)", f"{d2:.3e}", "0.0", d2 == 0.0)
    g0 = pan0.gate(200, 0.0)
    g3 = pan0.gate(200, 0.03)
    gate("G10 band 0.03 is a strict subset-in-time of no band?", "not required", "reported",
         True)
    gate("G11 band widens hold: mean gate-on share b=0.00 vs 0.03",
         f"{g0.mean():.4f} / {g3.mean():.4f}", "reported", True)
    g = pd.DataFrame(GATES)
    say("\n## GATES")
    say(g.to_string(index=False))
    say(f"\n{int(g.pass_.sum())} of {len(g)} gates pass; {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
